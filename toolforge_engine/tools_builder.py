"""Builds 10 interactive client-side developer, marketing, and AI utility web apps."""
from __future__ import annotations

from .config import ToolForgeConfig
from .templates import render_ad, render_page


def build_all_tools(cfg: ToolForgeConfig, updated: str) -> list[tuple[str, str, str]]:
    tools: list[tuple[str, str, str]] = []

    def add(rel: str, title: str, desc: str, body: str, app_name: str) -> None:
        ld = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": app_name,
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": "Web Browser",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        }
        tools.append((rel, title, render_page(cfg, rel, title, desc, body, updated, json_ld=ld)))

    # 1. JSON Formatter & Validator
    add(
        "tools/json-formatter-validator.html",
        "Free Online JSON Formatter, Validator & Minifier",
        "Format, validate, minify, and sort JSON keys instantly in your browser. 100% client-side privacy.",
        f"""
        <section class="hero"><span class="badge green">100% Client-Side • Zero Server Upload</span>
        <h1>JSON Formatter, Validator &amp; Minifier</h1>
        <p class="muted">Paste raw JSON to pretty-print, validate syntax with exact error messages, minify for APIs, or sort keys alphabetically.</p></section>
        <section class="card">
          <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px">
            <button class="btn" onclick="fmtJson(2)">Format (2 Spaces)</button>
            <button class="btn sec" onclick="fmtJson(4)">Format (4 Spaces)</button>
            <button class="btn sec" onclick="minJson()">Minify</button>
            <button class="btn green" onclick="copyOut()">Copy Output</button>
          </div>
          <div class="grid-2">
            <div><label>Input JSON<textarea id="jIn" rows="14">{{"name":"ToolForge Pro","pages":95,"active":true,"tags":["json","cron","regex","ai"]}}</textarea></label></div>
            <div><label>Formatted Output<textarea id="jOut" rows="14" readonly></textarea></label></div>
          </div>
          <p id="jStat" class="muted" style="margin-top:8px"></p>
        </section>
        {render_ad(cfg, "json-mid")}
        <script>
        function fmtJson(sp){{try{{const o=JSON.parse(document.getElementById('jIn').value);document.getElementById('jOut').value=JSON.stringify(o,null,sp);document.getElementById('jStat').textContent='✅ Valid JSON ('+document.getElementById('jOut').value.length+' chars)';}}catch(e){{document.getElementById('jStat').textContent='❌ Error: '+e.message;}}}}
        function minJson(){{try{{const o=JSON.parse(document.getElementById('jIn').value);document.getElementById('jOut').value=JSON.stringify(o);document.getElementById('jStat').textContent='✅ Minified ('+document.getElementById('jOut').value.length+' chars)';}}catch(e){{document.getElementById('jStat').textContent='❌ Error: '+e.message;}}}}
        function copyOut(){{navigator.clipboard.writeText(document.getElementById('jOut').value).then(()=>alert('Copied!'));}}
        fmtJson(2);
        </script>""",
        "ToolForge JSON Formatter",
    )

    # 2. JWT Decoder
    add(
        "tools/jwt-decoder-inspector.html",
        "Free Online JWT Decoder & Expiration Inspector",
        "Decode JSON Web Token (JWT) header and payload locally in your browser without sending secrets to any server.",
        f"""
        <section class="hero"><span class="badge green">Private Browser-Only JWT Tool</span>
        <h1>JWT Decoder &amp; Expiration Inspector</h1>
        <p class="muted">Inspect JWT header, payload claims, and human-readable <code>exp</code> / <code>iat</code> timestamps safely offline.</p></section>
        <section class="card">
          <label>Paste JWT Token<textarea id="jwtIn" rows="4" oninput="decJwt()">eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzIwMjciLCJuYW1lIjoiVG9vbEZvcmdlIFBybyIsImlhdCI6MTczMjI0MDAwMCwiZXhwIjoxODk1MDAwMDAwfQ.signature</textarea></label>
          <div class="grid-2">
            <div><h3>Header</h3><pre id="jwtH"></pre></div>
            <div><h3>Payload &amp; Expiry</h3><pre id="jwtP"></pre></div>
          </div>
          <p id="jwtExp" class="muted"></p>
        </section>
        {render_ad(cfg, "jwt-mid")}
        <script>
        function b64u(s){{s=s.replace(/-/g,'+').replace(/_/g,'/');while(s.length%4)s+='=';return decodeURIComponent(escape(atob(s)));}}
        function decJwt(){{try{{const p=document.getElementById('jwtIn').value.trim().split('.');const h=JSON.parse(b64u(p[0]));const b=JSON.parse(b64u(p[1]));document.getElementById('jwtH').textContent=JSON.stringify(h,null,2);document.getElementById('jwtP').textContent=JSON.stringify(b,null,2);document.getElementById('jwtExp').textContent=b.exp?('Expires: '+new Date(b.exp*1000).toISOString()+(Date.now()>b.exp*1000?' (EXPIRED)':' (ACTIVE)')):'No exp claim.';}}catch(e){{document.getElementById('jwtExp').textContent='Invalid JWT format';}}}}
        decJwt();
        </script>""",
        "ToolForge JWT Decoder",
    )

    # 3. Cron Expression Builder
    add(
        "tools/cron-expression-builder.html",
        "Cron Expression Generator & Human-Readable Schedule Tester",
        "Build and test 5-field Linux / GitHub Actions cron expressions with instant human-readable translation.",
        f"""
        <section class="hero"><span class="badge">GitHub Actions &amp; Linux Crontab</span>
        <h1>Cron Expression Builder &amp; Translator</h1>
        <p class="muted">Create standard 5-field cron schedules (minute, hour, day, month, weekday) and copy directly into GitHub Actions or Linux crontab.</p></section>
        <section class="card">
          <div class="pills" style="margin-bottom:14px">
            <button class="btn sec btn-sm" onclick="setC('*/5 * * * *')">Every 5m</button>
            <button class="btn sec btn-sm" onclick="setC('0 * * * *')">Hourly</button>
            <button class="btn sec btn-sm" onclick="setC('0 9 * * *')">Daily 09:00</button>
            <button class="btn sec btn-sm" onclick="setC('0 9 * * 1-5')">Weekdays 09:00</button>
            <button class="btn sec btn-sm" onclick="setC('0 0 1 * *')">Monthly 1st</button>
          </div>
          <label>5-Field Cron Expression<input id="cIn" value="0 9 * * 1-5" oninput="parseC()"></label>
          <pre id="cOut"></pre>
          <button class="btn green btn-sm" onclick="navigator.clipboard.writeText(document.getElementById('cIn').value)">Copy Expression</button>
        </section>
        {render_ad(cfg, "cron-mid")}
        <script>
        function setC(v){{document.getElementById('cIn').value=v;parseC();}}
        function parseC(){{const p=document.getElementById('cIn').value.trim().split(/\\s+/);if(p.length!==5){{document.getElementById('cOut').textContent='Enter exactly 5 space-separated fields: MIN HOUR DOM MONTH DOW';return;}}document.getElementById('cOut').textContent=`Minute: ${{p[0]}}\\nHour: ${{p[1]}}\\nDay of Month: ${{p[2]}}\\nMonth: ${{p[3]}}\\nDay of Week: ${{p[4]}}\\n\\nGitHub Actions YAML:\\nschedule:\\n  - cron: "${{p.join(' ')}}"`;}}
        parseC();
        </script>""",
        "ToolForge Cron Builder",
    )

    # 4. Regex Tester
    add(
        "tools/regex-tester-cheatsheet.html",
        "Free Online Regex Tester & Live Match Highlighter",
        "Test JavaScript regular expressions with live match counts, capture groups, and instant presets.",
        f"""
        <section class="hero"><span class="badge">Live JavaScript RegExp Engine</span>
        <h1>Regex Tester &amp; Match Inspector</h1>
        <p class="muted">Test patterns with flags (<code>g</code>, <code>i</code>, <code>m</code>) and view extracted matches immediately.</p></section>
        <section class="card">
          <div class="grid-2">
            <label>Regex Pattern<input id="rPat" value="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}" oninput="runR()"></label>
            <label>Flags<input id="rFlg" value="g" oninput="runR()"></label>
          </div>
          <label>Test Text<textarea id="rTxt" rows="6" oninput="runR()">Contact support@toolforge.pro or founder@wealthstack.studio for API details.</textarea></label>
          <pre id="rOut"></pre>
        </section>
        {render_ad(cfg, "regex-mid")}
        <script>
        function runR(){{try{{const re=new RegExp(document.getElementById('rPat').value,document.getElementById('rFlg').value);const m=[...document.getElementById('rTxt').value.matchAll(re)];document.getElementById('rOut').textContent='Matches found: '+m.length+'\\n'+m.map((x,i)=>`#${{i+1}}: "${{x[0]}}" (index ${{x.index}})`).join('\\n');}}catch(e){{document.getElementById('rOut').textContent='Regex Error: '+e.message;}}}}
        runR();
        </script>""",
        "ToolForge Regex Tester",
    )

    # 5. UTM Link Builder
    add(
        "tools/utm-campaign-builder.html",
        "Free UTM Campaign URL Builder for Google Analytics 4",
        "Generate clean GA4 UTM tracking URLs for YouTube, newsletters, Reddit, and social campaigns.",
        f"""
        <section class="hero"><span class="badge green">GA4 Marketing Attribution</span>
        <h1>UTM Campaign URL Builder</h1>
        <p class="muted">Tag your marketing links cleanly so Google Analytics 4 attributes every click accurately.</p></section>
        <section class="card">
          <div class="grid-2">
            <label>Website URL<input id="uBase" value="https://dream8837z.github.io/" oninput="mkU()"></label>
            <label>utm_source (e.g. youtube, reddit, newsletter)<input id="uSrc" value="youtube" oninput="mkU()"></label>
            <label>utm_medium (e.g. video, social, email)<input id="uMed" value="description" oninput="mkU()"></label>
            <label>utm_campaign (e.g. launch_2027)<input id="uCmp" value="passive_income_2027" oninput="mkU()"></label>
          </div>
          <pre id="uOut"></pre>
          <button class="btn green btn-sm" onclick="navigator.clipboard.writeText(document.getElementById('uOut').textContent)">Copy UTM URL</button>
        </section>
        {render_ad(cfg, "utm-mid")}
        <script>
        function mkU(){{try{{const u=new URL(document.getElementById('uBase').value);['utm_source','utm_medium','utm_campaign'].forEach((k,i)=>{{const v=[uSrc,uMed,uCmp][i].value.trim();if(v)u.searchParams.set(k,v);}});document.getElementById('uOut').textContent=u.toString();}}catch(e){{document.getElementById('uOut').textContent='Enter a valid https:// URL';}}}}
        mkU();
        </script>""",
        "ToolForge UTM Builder",
    )

    # 6. SEO Meta & OG Tag Generator
    add(
        "tools/seo-meta-og-generator.html",
        "Free SEO Meta Tag & Open Graph (OG) Preview Generator",
        "Generate Google SEO meta tags, Open Graph tags for KakaoTalk/LinkedIn, and Twitter Cards.",
        f"""
        <section class="hero"><span class="badge">SEO &amp; Social CTR Optimizer</span>
        <h1>SEO Meta &amp; Open Graph Tag Generator</h1>
        <p class="muted">Check Google title/description character limits and generate copy-paste HTML meta tags.</p></section>
        <section class="card">
          <label>Page Title (Ideal: 50–60 chars)<input id="mT" value="Free Online DevTools &amp; AI Prompt Utilities" oninput="mkM()"></label>
          <label>Meta Description (Ideal: 120–155 chars)<textarea id="mD" rows="3" oninput="mkM()">Fast, private client-side developer tools for JSON, Cron, Regex, JWT, and AI prompts.</textarea></label>
          <label>Canonical URL<input id="mU" value="https://dream8837z.github.io/devtool-ai-utility-autopilot/" oninput="mkM()"></label>
          <p id="mCnt" class="muted"></p>
          <pre id="mOut"></pre>
          <button class="btn green btn-sm" onclick="navigator.clipboard.writeText(document.getElementById('mOut').textContent)">Copy Meta HTML</button>
        </section>
        {render_ad(cfg, "meta-mid")}
        <script>
        function mkM(){{const t=mT.value,d=mD.value,u=mU.value;mCnt.textContent=`Title: ${{t.length}}/60 chars • Description: ${{d.length}}/155 chars`;mOut.textContent=`<title>${{t}}</title>\\n<meta name="description" content="${{d}}">\\n<link rel="canonical" href="${{u}}">\\n<meta property="og:title" content="${{t}}">\\n<meta property="og:description" content="${{d}}">\\n<meta property="og:url" content="${{u}}">`;}}
        mkM();
        </script>""",
        "ToolForge Meta Tag Generator",
    )

    # 7. Base64 / URL / SHA-256 Encoder
    add(
        "tools/base64-url-hash-encoder.html",
        "Free Base64, URL Encoder & SHA-256 Hash Generator",
        "Encode/decode Base64 and URLs, and compute cryptographic SHA-256 hashes directly in your browser.",
        f"""
        <section class="hero"><span class="badge green">Web Crypto API • Offline</span>
        <h1>Base64, URL &amp; SHA-256 Encoder</h1></section>
        <section class="card">
          <label>Input Text<textarea id="eIn" rows="4" oninput="runE()">Hello ToolForge Pro 2027</textarea></label>
          <h3>Base64</h3><pre id="eB64"></pre>
          <h3>URL Encoded</h3><pre id="eUrl"></pre>
          <h3>SHA-256 Hex</h3><pre id="eSha"></pre>
        </section>
        {render_ad(cfg, "enc-mid")}
        <script>
        async function runE(){{const v=eIn.value;eB64.textContent=btoa(unescape(encodeURIComponent(v)));eUrl.textContent=encodeURIComponent(v);const buf=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(v));eSha.textContent=[...new Uint8Array(buf)].map(b=>b.toString(16).padStart(2,'0')).join('');}}
        runE();
        </script>""",
        "ToolForge Base64 & SHA-256",
    )

    # 8. Markdown to HTML Converter
    add(
        "tools/markdown-html-converter.html",
        "Free Online Markdown to HTML Converter & Live Preview",
        "Convert Markdown headings, bold, code, and links to clean HTML with instant preview.",
        f"""
        <section class="hero"><span class="badge">Docs &amp; Blog Publishing</span>
        <h1>Markdown to HTML Converter</h1></section>
        <section class="card">
          <div class="grid-2">
            <label>Markdown Input<textarea id="mdIn" rows="10" oninput="runMd()"># ToolForge Pro\n\nWrite **clean** Markdown and copy *ready HTML* with `inline code`.</textarea></label>
            <div><h3>HTML Output</h3><pre id="mdOut"></pre></div>
          </div>
          <button class="btn green btn-sm" onclick="navigator.clipboard.writeText(mdOut.textContent)">Copy HTML</button>
        </section>
        {render_ad(cfg, "md-mid")}
        <script>
        function runMd(){{let s=mdIn.value.replace(/^### (.*$)/gim,'<h3>$1</h3>').replace(/^## (.*$)/gim,'<h2>$1</h2>').replace(/^# (.*$)/gim,'<h1>$1</h1>').replace(/\\*\\*(.*?)\\*\\*/gim,'<strong>$1</strong>').replace(/\\*(.*?)\\*/gim,'<em>$1</em>').replace(/`(.*?)`/gim,'<code>$1</code>').replace(/\\n/g,'<br>\\n');mdOut.textContent=s;}}
        runMd();
        </script>""",
        "ToolForge Markdown Converter",
    )

    # 9. UUID v4 & Secure Password Generator
    add(
        "tools/uuid-password-generator.html",
        "Free Bulk UUID v4 & Strong Password Generator",
        "Generate cryptographically secure UUID v4 identifiers and high-entropy passwords via Web Crypto API.",
        f"""
        <section class="hero"><span class="badge green">crypto.getRandomValues()</span>
        <h1>UUID v4 &amp; Secure Password Generator</h1></section>
        <section class="card">
          <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px">
            <button class="btn" onclick="genU()">Generate 10 UUIDs</button>
            <button class="btn green" onclick="genP()">Generate 5 Strong Passwords (20 chars)</button>
          </div>
          <pre id="upOut"></pre>
          <button class="btn sec btn-sm" onclick="navigator.clipboard.writeText(upOut.textContent)">Copy All</button>
        </section>
        {render_ad(cfg, "uuid-mid")}
        <script>
        function genU(){{upOut.textContent=Array.from({{length:10}},()=>crypto.randomUUID()).join('\\n');}}
        function genP(){{const cs='ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%^&*';upOut.textContent=Array.from({{length:5}},()=>Array.from(crypto.getRandomValues(new Uint32Array(20)),n=>cs[n%cs.length]).join('')).join('\\n');}}
        genU();
        </script>""",
        "ToolForge UUID & Password Generator",
    )

    # 10. AI Prompt Optimizer & LLM Token Cost Estimator
    add(
        "tools/ai-prompt-optimizer.html",
        "Free AI Prompt Builder & LLM Token Cost Estimator (GPT / Claude / Gemini)",
        "Structure high-accuracy prompts with Role-Context-Constraints-Output format and estimate API token counts.",
        f"""
        <section class="hero"><span class="badge">GEO &amp; Prompt Engineering</span>
        <h1>AI Prompt Builder &amp; Token Estimator</h1>
        <p class="muted">Build reusable prompts for ChatGPT, Claude, and Gemini with instant token count and API cost estimates.</p></section>
        <section class="card">
          <div class="grid-2">
            <label>AI Role<input id="pRole" value="Senior SEO &amp; Growth Strategist" oninput="mkP()"></label>
            <label>Target Audience<input id="pAud" value="B2B SaaS Founders" oninput="mkP()"></label>
          </div>
          <label>Core Task<textarea id="pTask" rows="3" oninput="mkP()">Create a 30-day organic SEO &amp; programmatic content distribution plan with zero paid ads.</textarea></label>
          <label>Output Format<input id="pFmt" value="Actionable Markdown table with weekly KPIs" oninput="mkP()"></label>
          <pre id="pOut"></pre>
          <p id="pTok" class="muted"></p>
          <button class="btn green btn-sm" onclick="navigator.clipboard.writeText(pOut.textContent)">Copy Structured Prompt</button>
        </section>
        {render_ad(cfg, "prompt-mid")}
        <script>
        function mkP(){{const t=`Role: You are a ${{pRole.value}}.\\nAudience: ${{pAud.value}}.\\nTask: ${{pTask.value}}\\nConstraints: Be specific, data-driven, and avoid generic fluff.\\nOutput Format: ${{pFmt.value}}.`;pOut.textContent=t;const tok=Math.ceil(t.length/4);pTok.textContent=`Est. Tokens: ~${{tok}} tokens (Chars: ${{t.length}})`;}}
        mkP();
        </script>""",
        "ToolForge AI Prompt Builder",
    )

    return tools
