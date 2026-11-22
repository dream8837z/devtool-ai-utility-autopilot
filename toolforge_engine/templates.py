"""Shared responsive HTML layout, SEO/JSON-LD, AdSense, share/embed hooks for ToolForge Pro."""
from __future__ import annotations

import html
import json
from typing import Any

from .config import ToolForgeConfig

CSS = """
:root {
  --bg: #090d16; --surface: #111827; --surface-2: #1f2937;
  --border: #374151; --text: #f9fafb; --muted: #9ca3af;
  --accent: #60a5fa; --green: #34d399; --warn: #fbbf24; --danger: #f87171;
}
body.light {
  --bg: #f8fafc; --surface: #ffffff; --surface-2: #f1f5f9;
  --border: #cbd5e1; --text: #0f172a; --muted: #475569;
  --accent: #2563eb; --green: #059669;
}
* { box-sizing: border-box; }
body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Inter","Noto Sans KR",sans-serif; background:var(--bg); color:var(--text); line-height:1.65; }
a { color:var(--accent); text-decoration:none; }
a:hover { text-decoration:underline; }
.topbar { background:var(--surface); border-bottom:1px solid var(--border); position:sticky; top:0; z-index:40; }
.topbar-in { max-width:1140px; margin:0 auto; padding:12px 20px; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px; }
.brand { font-weight:800; font-size:1.06rem; color:var(--text); }
.brand span { color:var(--accent); }
.nav { display:flex; flex-wrap:wrap; gap:12px; font-size:0.88rem; align-items:center; }
.nav a { color:var(--muted); font-weight:600; }
.nav a:hover { color:var(--text); text-decoration:none; }
.wrap { max-width:1140px; margin:0 auto; padding:26px 20px 60px; }
.hero { background:linear-gradient(135deg, rgba(96,165,250,0.14), rgba(52,211,153,0.10)); border:1px solid var(--border); border-radius:16px; padding:26px; margin-bottom:20px; }
.badge { display:inline-block; font-size:0.76rem; font-weight:700; padding:4px 10px; border-radius:999px; background:rgba(96,165,250,0.18); color:var(--accent); margin-bottom:8px; }
.badge.green { background:rgba(52,211,153,0.18); color:var(--green); }
h1 { margin:0 0 10px; font-size:clamp(1.5rem, 3vw, 2.1rem); line-height:1.25; }
h2 { margin:0 0 12px; font-size:1.25rem; }
h3 { margin:0 0 8px; font-size:1.02rem; }
.muted { color:var(--muted); }
.card { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:20px; margin-bottom:18px; }
.grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(250px, 1fr)); gap:14px; }
.grid-2 { display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:16px; }
.btn { display:inline-block; background:var(--accent); color:#090d16; font-weight:700; padding:9px 15px; border-radius:9px; border:none; cursor:pointer; font-size:0.9rem; }
.btn:hover { opacity:0.92; text-decoration:none; }
.btn.sec { background:var(--surface-2); color:var(--text); border:1px solid var(--border); }
.btn.green { background:var(--green); color:#052e16; }
.btn-sm { padding:6px 11px; font-size:0.82rem; border-radius:8px; }
textarea, input, select { width:100%; padding:10px 12px; border-radius:9px; border:1px solid var(--border); background:var(--surface-2); color:var(--text); font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:0.92rem; margin-top:4px; }
label { display:block; font-size:0.84rem; color:var(--muted); margin-bottom:10px; font-weight:600; }
pre, code { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }
pre { background:var(--surface-2); border:1px solid var(--border); border-radius:10px; padding:14px; overflow-x:auto; white-space:pre-wrap; word-break:break-word; }
.pills { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }
.pill { display:inline-block; padding:6px 12px; border-radius:999px; background:var(--surface-2); border:1px solid var(--border); color:var(--text); font-size:0.84rem; }
.pill:hover { border-color:var(--accent); text-decoration:none; }
.ad-slot { margin:20px 0; padding:10px; border-radius:12px; background:var(--surface-2); border:1px dashed var(--border); text-align:center; min-height:94px; }
.ad-lbl { font-size:0.68rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px; }
.share-bar { display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }
table { width:100%; border-collapse:collapse; margin-top:8px; font-size:0.9rem; }
th, td { padding:9px 11px; border-bottom:1px solid var(--border); text-align:left; }
th { color:var(--muted); font-size:0.8rem; text-transform:uppercase; }
footer { border-top:1px solid var(--border); margin-top:36px; padding-top:20px; font-size:0.84rem; color:var(--muted); }
""".strip()


def render_ad(cfg: ToolForgeConfig, slot: str = "mid") -> str:
    if not cfg.adsense_client_id:
        return ""
    cid = html.escape(cfg.adsense_client_id)
    return (
        f'<div class="ad-slot" data-slot="{html.escape(slot)}">'
        f'<div class="ad-lbl">Advertisement</div>'
        f'<ins class="adsbygoogle" style="display:block" data-ad-client="{cid}" '
        f'data-ad-format="auto" data-full-width-responsive="true"></ins>'
        f'<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>'
        f'</div>'
    )


def render_page(
    cfg: ToolForgeConfig,
    rel_path: str,
    title: str,
    description: str,
    body_html: str,
    updated_date: str,
    json_ld: dict[str, Any] | None = None,
) -> str:
    canonical = f"{cfg.site_url}/" if rel_path == "index.html" else f"{cfg.site_url}/{rel_path.lstrip('/')}"
    prefix = "../" * rel_path.count("/")
    cid = html.escape(cfg.adsense_client_id)
    adsense_head = (
        f'<meta name="google-adsense-account" content="{cid}">\n'
        f'  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={cid}" crossorigin="anonymous"></script>'
        if cid else ""
    )
    ld_html = (
        '<script type="application/ld+json">\n' + json.dumps(json_ld, ensure_ascii=False, indent=2) + "\n</script>"
        if json_ld else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} | ToolForge Pro</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{html.escape(canonical)}">
  <link rel="alternate" type="application/rss+xml" title="ToolForge Pro RSS" href="{prefix}feed.xml">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{html.escape(canonical)}">
  {adsense_head}
  <style>{CSS}</style>
  {ld_html}
</head>
<body>
  <header class="topbar">
    <div class="topbar-in">
      <a class="brand" href="{prefix}index.html">ToolForge <span>Pro</span></a>
      <nav class="nav">
        <a href="{prefix}tools/json-formatter-validator.html">JSON</a>
        <a href="{prefix}tools/cron-expression-builder.html">Cron</a>
        <a href="{prefix}tools/regex-tester-cheatsheet.html">Regex</a>
        <a href="{prefix}tools/jwt-decoder-inspector.html">JWT</a>
        <a href="{prefix}tools/ai-prompt-optimizer.html">AI Prompts</a>
        <a href="{html.escape(cfg.wealthstack_url)}">WealthStack</a>
        <a href="{html.escape(cfg.kr_hub_url)}">KR Finance</a>
        <button class="btn sec btn-sm" type="button" onclick="document.body.classList.toggle('light')">Theme</button>
      </nav>
    </div>
  </header>
  <main class="wrap">
    {body_html}
    <section class="card" style="margin-top:20px;border-color:rgba(96,165,250,0.45);background:linear-gradient(135deg,rgba(96,165,250,0.10),rgba(52,211,153,0.08))">
      <div class="grid-2">
        <div>
          <span class="badge green">Pro Digital Vault &amp; Chrome Extension</span>
          <h3>ToolForge Pro — AI Prompt Vault &amp; Offline Chrome Extension</h3>
          <p class="muted" style="font-size:0.86rem">Download the complete offline CSV, Notion, and JSON bundle of 80 prompts/cron/regex/HTTP guides plus the Manifest V3 Chrome Extension package.</p>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <a class="btn green btn-sm" href="{html.escape(cfg.gumroad_vault_url)}" target="_blank" rel="noopener">Download AI &amp; DevOps Vault (.ZIP) →</a>
            <a class="btn sec btn-sm" href="{html.escape(cfg.chrome_ext_url)}" target="_blank" rel="noopener">Chrome Extension (.ZIP) →</a>
          </div>
        </div>
        <div>
          <span class="badge">쿠팡 파트너스 개발자·데스크셋업 특가 (ID: {html.escape(cfg.coupang_partner_id)})</span>
          <h3>오늘의 쿠팡 로켓배송 IT·노트북·모니터·골드박스 특가</h3>
          <p class="muted" style="font-size:0.86rem">개발자·크리에이터 홈오피스 장비 및 매일 업데이트되는 쿠팡 로켓배송·골드박스 일일특가를 확인하세요.</p>
          <a class="btn btn-sm" href="{html.escape(cfg.affiliate_cloud_url)}" target="_blank" rel="nofollow sponsored noopener">쿠팡 로켓배송·골드박스 특가 바로가기 →</a>
          <p class="muted" style="font-size:0.74rem;margin-top:8px">※ 이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>
        </div>
      </div>
    </section>
    <section class="card" style="margin-top:20px">
      <h3>Share or Bookmark This Free Client-Side Tool</h3>
      <p class="muted" style="font-size:0.86rem">100% browser-based — your data never leaves your device. Copy a direct link or Markdown citation for your README/blog:</p>
      <div class="share-bar">
        <button class="btn sec btn-sm" type="button" onclick="navigator.clipboard.writeText(location.href).then(()=>alert('Copied URL!'))">Copy Link</button>
        <button class="btn sec btn-sm" type="button" onclick="navigator.clipboard.writeText('['+document.title+']('+location.href+')').then(()=>alert('Copied Markdown link!'))">Copy Markdown Link</button>
      </div>
    </section>
    <footer>
      <p><strong>ToolForge Pro</strong> — Free Browser DevTools, Cron, Regex, HTTP &amp; AI Prompt Suite. Updated {html.escape(updated_date)}.</p>
      <p>
        <a href="{prefix}index.html">Home</a> ·
        <a href="{prefix}about.html">About</a> ·
        <a href="{prefix}privacy.html">Privacy</a> ·
        <a href="{prefix}disclaimer.html">Disclaimer</a> ·
        <a href="{prefix}terms.html">Terms</a> ·
        <a href="{prefix}llms.txt">llms.txt</a> ·
        <a href="{html.escape(cfg.root_portal_url)}">Main Portal</a>
      </p>
    </footer>
  </main>
</body>
</html>
"""
