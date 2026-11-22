"""Main orchestrator: build 95 pages, llms.txt, RSS feed, IndexNow key & ping, SEO audit."""
from __future__ import annotations

import html as html_lib
import json
import re
import shutil
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import Any

from .config import ToolForgeConfig, load_config
from .pseo_builder import (
    build_core_pages,
    build_cron_pages,
    build_http_pages,
    build_prompt_pages,
    build_regex_pages,
)
from .tools_builder import build_all_tools


def _write(base: Path, rel: str, content: str) -> None:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def audit_dist(cfg: ToolForgeConfig) -> dict[str, Any]:
    dist = cfg.dist_dir
    files = sorted(dist.rglob("*.html"))
    errors: list[str] = []
    if len(files) < 90:
        errors.append(f"Expected >= 90 pages, found {len(files)}")
    for req in ("sitemap.xml", "robots.txt", "ads.txt", "llms.txt", "feed.xml", f"{cfg.indexnow_key}.txt"):
        if not (dist / req).exists():
            errors.append(f"Missing required root file: {req}")
    for xml_name in ("sitemap.xml", "feed.xml"):
        xp = dist / xml_name
        if xp.exists():
            try:
                ET.fromstring(xp.read_bytes())
            except Exception as e:
                errors.append(f"{xml_name}: invalid XML ({e})")
    seen: set[str] = set()
    for f in files:
        txt = f.read_text(encoding="utf-8")
        rel = f.relative_to(dist).as_posix()
        m = re.search(r"<title>(.*?)</title>", txt, re.S)
        if not m:
            errors.append(f"{rel}: missing title")
        else:
            t = m.group(1).strip()
            if t in seen:
                errors.append(f"{rel}: duplicate title {t}")
            seen.add(t)
        if cfg.adsense_client_id and cfg.adsense_client_id not in txt:
            errors.append(f"{rel}: missing AdSense ID")
        for href in re.findall(r'href="([^"]+)"', txt):
            if href.startswith(("http://", "https://", "#", "mailto:", "javascript:", "${")):
                continue
            target = (f.parent / href.split("#")[0].split("?")[0]).resolve()
            if not target.exists():
                errors.append(f"{rel}: broken link {href}")
    return {"status": "PASS" if not errors else "FAIL", "page_count": len(files), "error_count": len(errors), "errors": errors[:20]}


def ping_indexnow(cfg: ToolForgeConfig, urls: list[str]) -> str:
    if not cfg.enable_indexnow:
        return "disabled"
    payload = {
        "host": cfg.host,
        "key": cfg.indexnow_key,
        "keyLocation": f"{cfg.site_url}/{cfg.indexnow_key}.txt",
        "urlList": urls[:100],
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/IndexNow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            return f"http_{resp.status}"
    except Exception as e:
        return f"skipped({e.__class__.__name__})"


def run_pipeline(cfg: ToolForgeConfig | None = None) -> dict[str, Any]:
    cfg = cfg or load_config()
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if cfg.dist_dir.exists():
        shutil.rmtree(cfg.dist_dir)
    cfg.dist_dir.mkdir(parents=True, exist_ok=True)

    tools = build_all_tools(cfg, updated)
    crons = build_cron_pages(cfg, updated)
    regexes = build_regex_pages(cfg, updated)
    prompts = build_prompt_pages(cfg, updated)
    https = build_http_pages(cfg, updated)
    cores = build_core_pages(cfg, updated, tools, crons, regexes, prompts, https)

    all_rel: list[str] = []
    for group in (tools, crons, regexes, prompts, https):
        for rel, _, doc in group:
            _write(cfg.dist_dir, rel, doc)
            all_rel.append(rel)
    for rel, doc in cores:
        _write(cfg.dist_dir, rel, doc)
        all_rel.append(rel)

    full_urls = [f"{cfg.site_url}/" if r == "index.html" else f"{cfg.site_url}/{r}" for r in sorted(all_rel)]
    sitemap_entries = [
        f"  <url><loc>{u}</loc><lastmod>{updated}</lastmod><priority>{'1.0' if u.endswith('/') else ('0.9' if '/tools/' in u else '0.75')}</priority></url>"
        for u in full_urls
    ]
    _write(cfg.dist_dir, "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(sitemap_entries) + "\n</urlset>\n")
    _write(cfg.dist_dir, "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {cfg.site_url}/sitemap.xml\n")
    _write(cfg.dist_dir, "ads.txt", f"google.com, {cfg.adsense_pub_id}, DIRECT, f08c47fec0942fa0\n")
    _write(cfg.dist_dir, f"{cfg.indexnow_key}.txt", f"{cfg.indexnow_key}\n")
    _write(cfg.dist_dir, ".nojekyll", "")

    # llms.txt for AI search engines (ChatGPT / Perplexity / Claude GEO)
    llms_lines = [
        "# ToolForge Pro",
        "> Free 100% client-side developer tools, Cron schedules, Regex patterns, HTTP status guides, and AI prompt templates.",
        "",
        "## Interactive Tools",
        *[f"- [{t}]({cfg.site_url}/{r})" for r, t, _ in tools],
        "",
        "## Sister Hubs",
        f"- [WealthStack Studio (Micro-SaaS & Passive Income)]({cfg.wealthstack_url})",
        f"- [MoneyFinLab (KR Finance & Subsidy Calculators)]({cfg.kr_hub_url})",
    ]
    _write(cfg.dist_dir, "llms.txt", "\n".join(llms_lines) + "\n")

    # RSS 2.0 feed (strict XML-escaped with pubDate & description for Naver/Bing validators)
    pub_rfc = format_datetime(datetime.now(timezone.utc))
    rss_items = "".join(
        f"    <item>\n"
        f"      <title>{html_lib.escape(t)}</title>\n"
        f"      <link>{html_lib.escape(cfg.site_url + '/' + r)}</link>\n"
        f"      <guid isPermaLink=\"true\">{html_lib.escape(cfg.site_url + '/' + r)}</guid>\n"
        f"      <description>{html_lib.escape(t)} — Free 100% client-side web utility on ToolForge Pro.</description>\n"
        f"      <pubDate>{pub_rfc}</pubDate>\n"
        f"    </item>\n"
        for r, t, _ in (tools + prompts[:10])
    )
    _write(
        cfg.dist_dir,
        "feed.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0">\n'
        '  <channel>\n'
        '    <title>ToolForge Pro</title>\n'
        f'    <link>{html_lib.escape(cfg.site_url)}/</link>\n'
        '    <description>Free Browser DevTools, Cron, Regex, HTTP &amp; AI Prompt Utilities</description>\n'
        '    <language>en</language>\n'
        f'    <lastBuildDate>{pub_rfc}</lastBuildDate>\n'
        f'{rss_items}'
        '  </channel>\n'
        '</rss>\n',
    )

    audit = audit_dist(cfg)
    indexnow_res = ping_indexnow(cfg, full_urls)
    result = {"updated_date": updated, "indexnow": indexnow_res, "audit": audit}
    if audit["status"] != "PASS":
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)
    return result
