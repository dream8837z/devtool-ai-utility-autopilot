"""Builds 80 Non-YMYL high-search-volume pSEO pages + core/legal/hub pages."""
from __future__ import annotations

import html

from .config import ToolForgeConfig
from .recipes_db import CRON_RECIPES, HTTP_CODES, PROMPT_RECIPES, REGEX_RECIPES
from .templates import render_ad, render_page


def build_cron_pages(cfg: ToolForgeConfig, updated: str) -> list[tuple[str, str, str]]:
    pages = []
    for item in CRON_RECIPES:
        rel = f"cron/cron-{item['slug']}.html"
        title = f"Cron Expression for {item['title']} ({item['expr']})"
        desc = f"Copy-paste cron schedule {item['expr']} to run a task {item['title'].lower()}. Includes Linux crontab and GitHub Actions YAML."
        related = "".join(
            f'<a class="pill" href="cron-{x["slug"]}.html">{html.escape(x["title"])}</a>'
            for x in CRON_RECIPES if x["slug"] != item["slug"]
        )[:1800]
        body = f"""
        <section class="hero"><span class="badge">Cron Schedule Recipe • {updated}</span>
        <h1>{html.escape(title)}</h1>
        <p class="muted">{html.escape(item['desc'])} <strong>Best for:</strong> {html.escape(item['use'])}</p>
        <a class="btn btn-sm" href="../tools/cron-expression-builder.html">Customize in Interactive Cron Builder →</a></section>
        <section class="card"><h2>Copy-Paste Crontab &amp; GitHub Actions YAML</h2>
        <pre>{html.escape(item['expr'])} /usr/bin/python3 /path/to/job.py</pre>
        <pre>on:
  schedule:
    - cron: "{html.escape(item['expr'])}"</pre>
        <button class="btn green btn-sm" onclick="navigator.clipboard.writeText('{html.escape(item['expr'])}')">Copy Cron Expression</button>
        </section>
        {render_ad(cfg, "cron-seo")}
        <section class="card"><h3>Related Cron Schedules</h3><div class="pills">{related}</div></section>"""
        pages.append((rel, title, render_page(cfg, rel, title, desc, body, updated)))
    return pages


def build_regex_pages(cfg: ToolForgeConfig, updated: str) -> list[tuple[str, str, str]]:
    pages = []
    for item in REGEX_RECIPES:
        rel = f"regex/regex-{item['slug']}.html"
        title = f"Regex for {item['name']} (JavaScript & Python Copy-Paste)"
        desc = f"Tested regular expression for {item['name'].lower()}: {item['note']} Includes JS and Python code snippets."
        related = "".join(
            f'<a class="pill" href="regex-{x["slug"]}.html">{html.escape(x["name"])}</a>'
            for x in REGEX_RECIPES if x["slug"] != item["slug"]
        )[:1800]
        body = f"""
        <section class="hero"><span class="badge green">Tested Regex Pattern • {updated}</span>
        <h1>{html.escape(title)}</h1>
        <p class="muted">{html.escape(item['note'])} Sample match: <code>{html.escape(item['sample'])}</code></p>
        <a class="btn btn-sm" href="../tools/regex-tester-cheatsheet.html">Test Live in Regex Tester →</a></section>
        <section class="card"><h2>Pattern &amp; Code Examples</h2>
        <pre id="rxP">{html.escape(item['pattern'])}</pre>
        <pre>import re
pattern = re.compile(r"{html.escape(item['pattern'])}")
print(bool(pattern.search("{html.escape(item['sample'])}")))</pre>
        <button class="btn green btn-sm" onclick="navigator.clipboard.writeText(document.getElementById('rxP').textContent)">Copy Regex Pattern</button>
        </section>
        {render_ad(cfg, "regex-seo")}
        <section class="card"><h3>More Production Regex Patterns</h3><div class="pills">{related}</div></section>"""
        pages.append((rel, title, render_page(cfg, rel, title, desc, body, updated)))
    return pages


def build_prompt_pages(cfg: ToolForgeConfig, updated: str) -> list[tuple[str, str, str]]:
    pages = []
    for item in PROMPT_RECIPES:
        rel = f"prompts/prompt-{item['slug']}.html"
        title = f"{item['name']} — Ready-to-Use AI Prompt ({item['cat']})"
        desc = f"Copy this high-converting {item['cat']} prompt template for ChatGPT, Claude, and Gemini: {item['name']}."
        related = "".join(
            f'<a class="pill" href="prompt-{x["slug"]}.html">{html.escape(x["name"])}</a>'
            for x in PROMPT_RECIPES if x["slug"] != item["slug"]
        )[:1800]
        body = f"""
        <section class="hero"><span class="badge">AI Prompt Template • {html.escape(item['cat'])}</span>
        <h1>{html.escape(item['name'])}</h1>
        <p class="muted">Optimized for ChatGPT, Claude, and Gemini. Replace bracketed placeholders and run immediately.</p>
        <a class="btn btn-sm" href="../tools/ai-prompt-optimizer.html">Customize &amp; Count Tokens →</a></section>
        <section class="card"><h2>Copy-Paste Prompt</h2>
        <pre id="prBox">{html.escape(item['prompt'])}</pre>
        <button class="btn green btn-sm" onclick="navigator.clipboard.writeText(document.getElementById('prBox').textContent)">Copy Prompt</button>
        </section>
        {render_ad(cfg, "prompt-seo")}
        <section class="card"><h3>More High-Impact AI Prompts</h3><div class="pills">{related}</div></section>"""
        pages.append((rel, title, render_page(cfg, rel, title, desc, body, updated)))
    return pages


def build_http_pages(cfg: ToolForgeConfig, updated: str) -> list[tuple[str, str, str]]:
    pages = []
    for item in HTTP_CODES:
        rel = f"http/http-{item['slug']}.html"
        title = f"HTTP {item['code']} {item['name']} — Meaning, Causes & How to Fix"
        desc = f"What HTTP status code {item['code']} ({item['name']}) means and step-by-step backend/API troubleshooting fixes."
        related = "".join(
            f'<a class="pill" href="http-{x["slug"]}.html">HTTP {x["code"]} {html.escape(x["name"])}</a>'
            for x in HTTP_CODES if x["slug"] != item["slug"]
        )[:1800]
        body = f"""
        <section class="hero"><span class="badge">HTTP Status Reference • {item['code']}</span>
        <h1>HTTP {item['code']} {html.escape(item['name'])}</h1>
        <p class="muted">{html.escape(item['meaning'])}</p></section>
        <section class="card"><h2>How to Fix HTTP {item['code']}</h2>
        <p>{html.escape(item['fix'])}</p>
        <a class="btn btn-sm" href="../tools/json-formatter-validator.html">Inspect API JSON Response →</a></section>
        {render_ad(cfg, "http-seo")}
        <section class="card"><h3>Other HTTP Status Codes</h3><div class="pills">{related}</div></section>"""
        pages.append((rel, title, render_page(cfg, rel, title, desc, body, updated)))
    return pages


def build_core_pages(
    cfg: ToolForgeConfig,
    updated: str,
    tools: list[tuple[str, str, str]],
    crons: list[tuple[str, str, str]],
    regexes: list[tuple[str, str, str]],
    prompts: list[tuple[str, str, str]],
    https: list[tuple[str, str, str]],
) -> list[tuple[str, str]]:
    total = len(tools) + len(crons) + len(regexes) + len(prompts) + len(https) + 5
    tool_cards = "".join(
        f'<div class="card" style="margin:0;background:var(--surface-2)"><h3>{html.escape(t)}</h3>'
        f'<a class="btn btn-sm" href="{rel}">Open Tool →</a></div>'
        for rel, t, _ in tools
    )
    cron_pills = "".join(f'<a class="pill" href="{rel}">{html.escape(t.replace("Cron Expression for ", ""))}</a>' for rel, t, _ in crons[:10])
    regex_pills = "".join(f'<a class="pill" href="{rel}">{html.escape(t.split("(")[0].replace("Regex for ", ""))}</a>' for rel, t, _ in regexes[:10])
    prompt_pills = "".join(f'<a class="pill" href="{rel}">{html.escape(t.split("—")[0].strip())}</a>' for rel, t, _ in prompts[:10])
    http_pills = "".join(f'<a class="pill" href="{rel}">{html.escape(t.split("—")[0].strip())}</a>' for rel, t, _ in https[:10])

    idx_body = f"""
    <section class="hero">
      <span class="badge green">100% Client-Side • {total} Free Developer &amp; AI Utilities • Updated {updated}</span>
      <h1>ToolForge Pro — Free Online DevTools, Cron, Regex &amp; AI Prompt Suite</h1>
      <p class="muted">Zero sign-up, zero server uploads. Format JSON, decode JWTs, build Cron expressions, test Regex, optimize AI prompts, and troubleshoot HTTP status codes directly in your browser.</p>
    </section>
    <section class="card"><h2>10 Interactive Client-Side Web Tools</h2><div class="grid">{tool_cards}</div></section>
    {render_ad(cfg, "home-mid")}
    <section class="card"><h2>Popular Cron Schedule Recipes (20)</h2><div class="pills">{cron_pills}</div></section>
    <section class="card"><h2>Production Regex Patterns (20)</h2><div class="pills">{regex_pills}</div></section>
    <section class="card"><h2>Copy-Paste AI Prompt Templates (20)</h2><div class="pills">{prompt_pills}</div></section>
    <section class="card"><h2>HTTP Status Code Troubleshooting (20)</h2><div class="pills">{http_pills}</div></section>
    """
    about = '<section class="card"><h1>About ToolForge Pro</h1><p>ToolForge Pro provides fast, privacy-first browser utilities for developers, marketers, and AI builders. Every interactive tool executes 100% locally in your browser.</p></section>'
    privacy = f'<section class="card"><h1>Privacy Policy</h1><p>All tools run strictly client-side. Inputs (JSON, JWT, Regex, Prompts) are never transmitted to any server. This site displays ads via Google AdSense ({html.escape(cfg.adsense_client_id)}).</p></section>'
    disclaimer = '<section class="card"><h1>Disclaimer</h1><p>All code snippets, cron schedules, regex patterns, and prompts are provided for educational and productivity purposes without warranty. Always test before deploying to production.</p></section>'
    terms = '<section class="card"><h1>Terms of Use</h1><p>Free for personal and commercial productivity use. Provided as-is.</p></section>'
    return [
        ("index.html", render_page(cfg, "index.html", "Free Online DevTools, Cron, Regex & AI Prompt Suite", "95 free browser-based developer tools, Cron recipes, Regex patterns, HTTP guides, and AI prompt templates.", idx_body, updated)),
        ("about.html", render_page(cfg, "about.html", "About ToolForge Pro", "About ToolForge Pro client-side developer utilities.", about, updated)),
        ("privacy.html", render_page(cfg, "privacy.html", "Privacy Policy", "Privacy policy for ToolForge Pro.", privacy, updated)),
        ("disclaimer.html", render_page(cfg, "disclaimer.html", "Disclaimer", "Technical disclaimer for ToolForge Pro.", disclaimer, updated)),
        ("terms.html", render_page(cfg, "terms.html", "Terms of Use", "Terms of use for ToolForge Pro.", terms, updated)),
    ]
