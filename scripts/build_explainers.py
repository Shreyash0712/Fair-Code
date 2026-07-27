#!/usr/bin/env python3
"""Generate static, crawlable explainer pages from explainers/*.md.

Contributors only ever touch two files: explainers/<slug>.md and one entry
in assets/explainers-data.json. This script (run by CI on every push that
touches those files) does everything else:

  - renders each markdown file to HTML using the same rendering rules as
    the browser-side renderer in assets/explainers-ui.js, so output matches
    what the site already looks like
  - writes one real, pre-rendered page per explainer to explainers/<slug>.html
    (title/description/canonical/JSON-LD baked into the raw HTML, not
    loaded in afterward by JS)
  - regenerates assets/explainers-data.js from assets/explainers-data.json
    so the two never drift apart
  - regenerates sitemap.xml

Nothing here is contributor-facing. Run with: python3 scripts/build_explainers.py
"""
import json
import re
from html import escape as _escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPLAINERS_DIR = ROOT / "explainers"
DATA_JSON = ROOT / "assets" / "explainers-data.json"
DATA_JS = ROOT / "assets" / "explainers-data.js"
SITEMAP = ROOT / "sitemap.xml"
SITE_URL = "https://www.thefaircode.xyz"
REPO_URL = "https://github.com/yakew7/Fair-Code"

PROJECT_ANCHORS = {
    "COMPAS": "project-compas",
    "AI Fair Recruitment": "project-hiring",
    "Ai Fair Recrutment Dataset": "project-hiring",
    "German Credit Lending": "project-credit",
    "Insurance Denial": "project-insurance",
    "Benefits Denial": "project-benefits",
    "Healthcare Readmission": "project-readmission",
}


def escape_html(value):
    return _escape(str(value), quote=True)


def slugify_heading(text):
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def resolve_link_target(url, known_slugs):
    if re.match(r"^(?:[a-z]+:|#|/)", url, flags=re.IGNORECASE):
        return url

    hash_index = url.find("#")
    query_index = url.find("?")
    candidates = [i for i in (hash_index, query_index) if i != -1]
    path_end = min(candidates) if candidates else len(url)
    raw_path = url[:path_end]
    suffix = url[path_end:]

    normalized_path = re.sub(r"^\.\./", "", raw_path)
    normalized_path = re.sub(r"^\./", "", normalized_path)
    from urllib.parse import unquote

    normalized_path = unquote(normalized_path)
    clean_path = normalized_path.rstrip("/")
    basename = clean_path.split("/")[-1] if clean_path else clean_path
    base_without_ext = re.sub(r"\.md$", "", basename, flags=re.IGNORECASE)

    if re.search(r"\.md$", basename, flags=re.IGNORECASE) and base_without_ext in known_slugs:
        # Generated pages live as siblings inside explainers/, so a link to
        # another explainer is just "<slug>.html" in the same directory.
        return f"{base_without_ext}.html{suffix}"

    if clean_path in PROJECT_ANCHORS or basename in PROJECT_ANCHORS:
        anchor = PROJECT_ANCHORS.get(clean_path) or PROJECT_ANCHORS.get(basename)
        return f"../index.html#{anchor}{suffix}"

    if re.search(r"\.md$", basename, flags=re.IGNORECASE):
        return f"{base_without_ext}.html{suffix}"

    return clean_path if url.startswith("../") else url


def inline_markdown(text, known_slugs):
    escaped = escape_html(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)

    def replace_link(match):
        label, url = match.group(1), match.group(2)
        trimmed = url.strip()
        is_external = bool(re.match(r"^(?:[a-z]+:)", trimmed, flags=re.IGNORECASE))
        resolved = resolve_link_target(trimmed, known_slugs)
        target_attr = ' target="_blank" rel="noreferrer noopener"' if is_external else ""
        return f'<a href="{escape_html(resolved)}"{target_attr}>{label}</a>'

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, escaped)
    return escaped


def parse_table(lines, start_index):
    rows = []
    index = start_index
    while index < len(lines) and re.match(r"^\s*\|", lines[index]):
        rows.append(lines[index].strip())
        index += 1

    if len(rows) < 2 or not re.match(
        r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$", rows[1]
    ):
        return None

    def split_row(row):
        return [cell.strip() for cell in row.split("|")[1:-1]]

    headers = split_row(rows[0])
    body_rows = [split_row(row) for row in rows[2:]]
    return headers, body_rows, index - 1


def render_markdown(markdown_text, known_slugs):
    lines = markdown_text.replace("\r\n", "\n").split("\n")
    blocks = []
    paragraph = []
    list_items = []
    quote_lines = []
    code_lines = []
    code_lang = ""
    in_code = False
    heading_counts = {}

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            text = re.sub(r"\s+", " ", " ".join(paragraph)).strip()
            blocks.append(f"<p>{inline_markdown(text, known_slugs)}</p>")
            paragraph = []

    def flush_list():
        nonlocal list_items
        if list_items:
            items = "".join(f"<li>{inline_markdown(item, known_slugs)}</li>" for item in list_items)
            blocks.append(f"<ul>{items}</ul>")
            list_items = []

    def flush_quote():
        nonlocal quote_lines
        if quote_lines:
            paras = "".join(f"<p>{inline_markdown(line, known_slugs)}</p>" for line in quote_lines)
            blocks.append(f"<blockquote>{paras}</blockquote>")
            quote_lines = []

    def flush_code():
        nonlocal code_lines, code_lang
        if code_lines:
            lang_attr = f' class="language-{escape_html(code_lang)}"' if code_lang else ""
            blocks.append(f"<pre><code{lang_attr}>{escape_html(chr(10).join(code_lines))}</code></pre>")
            code_lines = []
            code_lang = ""

    index = 0
    while index < len(lines):
        line = lines[index]
        trimmed = line.strip()

        if in_code:
            if trimmed.startswith("```"):
                in_code = False
                flush_code()
            else:
                code_lines.append(line)
            index += 1
            continue

        table = parse_table(lines, index)
        if table:
            flush_paragraph()
            flush_list()
            flush_quote()
            headers, body_rows, next_index = table
            header_html = "".join(f"<th>{inline_markdown(cell, known_slugs)}</th>" for cell in headers)
            body_html = "".join(
                "<tr>" + "".join(f"<td>{inline_markdown(cell, known_slugs)}</td>" for cell in row) + "</tr>"
                for row in body_rows
            )
            blocks.append(
                f'<div class="explainer-table-wrap"><table class="explainer-table">'
                f"<thead><tr>{header_html}</tr></thead><tbody>{body_html}</tbody></table></div>"
            )
            index = next_index + 1
            continue

        if trimmed.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_quote()
            in_code = True
            code_lang = trimmed[3:].strip()
            index += 1
            continue

        if not trimmed:
            flush_paragraph()
            flush_list()
            flush_quote()
            index += 1
            continue

        if re.match(r"^---+$", trimmed):
            flush_paragraph()
            flush_list()
            flush_quote()
            blocks.append("<hr>")
            index += 1
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", trimmed)
        if heading_match:
            flush_paragraph()
            flush_list()
            flush_quote()
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2)
            base_id = slugify_heading(heading_text)
            next_count = heading_counts.get(base_id, 0) + 1
            heading_counts[base_id] = next_count
            heading_id = base_id if next_count == 1 else f"{base_id}-{next_count}"
            blocks.append(
                f'<h{level} id="{escape_html(heading_id)}">{inline_markdown(heading_text, known_slugs)}</h{level}>'
            )
            index += 1
            continue

        if re.match(r"^>\s?", trimmed):
            flush_paragraph()
            flush_list()
            quote_lines.append(re.sub(r"^>\s?", "", trimmed))
            index += 1
            continue

        if re.match(r"^[-*]\s+", trimmed):
            flush_paragraph()
            flush_quote()
            list_items.append(re.sub(r"^[-*]\s+", "", trimmed))
            index += 1
            continue

        flush_quote()
        flush_list()
        paragraph.append(trimmed)
        index += 1

    flush_paragraph()
    flush_list()
    flush_quote()
    flush_code()

    return "\n".join(blocks)


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · Fair Code</title>
<meta name="description" content="{summary}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title} · Fair Code">
<meta property="og:description" content="{summary}">
<meta property="og:type" content="article">
<meta name="author" content="Yash Kewlani">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title} · Fair Code">
<meta name="twitter:description" content="{summary}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<script>
  (function () {{
    const saved = localStorage.getItem('fc-theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
  }})();
</script>
<link rel="stylesheet" href="../assets/explainers.css">
<style>
  :root {{
    --bg: #f4f1e8;
    --surface: #ebe7d9;
    --border: #d9d3c0;
    --border2: #bdb59c;
    --accent: #a63a22;
    --accent3: #2f6b4f;
    --text: #36321f;
    --muted: #7d7459;
    --white: #1d1910;
    --bias-track-bg: #e2dcc9;

    --serif: 'Instrument Serif', 'Iowan Old Style', Georgia, serif;
    --sans: 'Archivo', 'Helvetica Neue', sans-serif;
    --mono: 'IBM Plex Mono', 'SF Mono', monospace;
  }}

  html[data-theme="dark"] {{
    --bg: #15130d;
    --surface: #1c1912;
    --border: #2e2a1f;
    --border2: #443e2d;
    --accent: #cf6f49;
    --accent3: #79b294;
    --text: #cfc7b0;
    --muted: #8d8367;
    --white: #f1e9d4;
    --bias-track-bg: #242013;
  }}

  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: var(--sans);
    background: var(--bg);
    color: var(--text);
    -webkit-font-smoothing: antialiased;
    transition: background 0.3s, color 0.3s;
  }}
  a {{ color: inherit; }}
  ::selection {{ background: var(--accent); color: var(--bg); }}
  :focus-visible {{ outline: 2px solid var(--accent); outline-offset: 3px; }}
</style>
<script type="application/ld+json">
{jsonld}
</script>
<script>
  window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
</script>
<script defer src="/_vercel/insights/script.js"></script>
<script>
  window.si = window.si || function () {{ (window.siq = window.siq || []).push(arguments); }};
</script>
<script defer src="/_vercel/speed-insights/script.js"></script>
<script defer src="https://cloud.umami.is/script.js" data-website-id="84e0aebf-44e1-466e-b2c6-62f75e1c36c7"></script>
</head>
<body class="explainer-page">
  <main class="explainer-shell is-ready" data-explainer-shell>
    <div class="explainer-topbar">
      <a class="explainer-back" href="../index.html#explainers">← Back to explainers</a>
      <div class="explainer-topbar-actions">
        <a class="explainer-source" href="{source_url}" target="_blank" rel="noopener noreferrer">View source on GitHub</a>
        <button class="explainer-theme-toggle" id="explainerThemeToggle" aria-label="Toggle theme">☀</button>
      </div>
    </div>

    <section class="explainer-hero">
      <div class="explainer-kicker">Explainer</div>
      <h1 class="explainer-headline">{title}</h1>
      <p class="explainer-lede">{subtitle}</p>
      <p class="explainer-lede">{summary}</p>
    </section>

    <article class="explainer-content">{content}</article>
  </main>

  <script>
    (function () {{
      const toggle = document.getElementById('explainerThemeToggle');
      const html = document.documentElement;

      function syncTheme() {{
        const current = html.getAttribute('data-theme') || 'dark';
        toggle.textContent = current === 'light' ? '☾' : '☀';
        toggle.setAttribute('aria-label', current === 'light' ? 'Switch to dark mode' : 'Switch to light mode');
      }}

      syncTheme();

      toggle.addEventListener('click', () => {{
        const current = html.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem('fc-theme', next);
        syncTheme();
      }});
    }})();
  </script>
</body>
</html>
"""


def build_jsonld(entry, canonical):
    data = {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "author": {
            "@type": "Person",
            "name": "Yash Kewlani",
            "url": "https://github.com/yakew7",
        },
        "name": entry["title"],
        "description": entry["summary"],
        "url": canonical,
        "inDefinedTermSet": {
            "@type": "DefinedTermSet",
            "name": "Fair Code Explainers",
            "url": f"{SITE_URL}/index.html#explainers",
        },
    }
    return json.dumps(data, indent=2)


def build_page(entry, known_slugs):
    slug = entry["slug"]
    md_path = EXPLAINERS_DIR / f"{slug}.md"
    markdown_text = md_path.read_text(encoding="utf-8")
    content_html = render_markdown(markdown_text, known_slugs)
    canonical = f"{SITE_URL}/explainers/{slug}.html"

    return PAGE_TEMPLATE.format(
        title=escape_html(entry["title"]),
        summary=escape_html(entry["summary"]),
        canonical=canonical,
        subtitle=escape_html(entry["subtitle"]),
        content=content_html,
        source_url=f"{REPO_URL}/blob/main/explainers/{slug}.md",
        jsonld=build_jsonld(entry, canonical),
    )


def build_sitemap(entries):
    urls = [f"{SITE_URL}/", f"{SITE_URL}/profiler.html"]
    urls += [f"{SITE_URL}/explainers/{entry['slug']}.html" for entry in entries]
    body = "\n".join(f"  <url>\n    <loc>{escape_html(u)}</loc>\n  </url>" for u in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )


def build_data_js(entries):
    payload = json.dumps(entries, indent=2)
    return f"window.FAIR_CODE_EXPLAINERS = {payload};\n"


def main():
    entries = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    known_slugs = {entry["slug"] for entry in entries}

    missing = [e["slug"] for e in entries if not (EXPLAINERS_DIR / f"{e['slug']}.md").exists()]
    if missing:
        raise SystemExit(f"Missing markdown file(s) for: {', '.join(missing)}")

    for entry in entries:
        page_html = build_page(entry, known_slugs)
        out_path = EXPLAINERS_DIR / f"{entry['slug']}.html"
        out_path.write_text(page_html, encoding="utf-8")

    DATA_JS.write_text(build_data_js(entries), encoding="utf-8")
    SITEMAP.write_text(build_sitemap(entries), encoding="utf-8")

    print(f"Generated {len(entries)} explainer pages, assets/explainers-data.js, and sitemap.xml")


if __name__ == "__main__":
    main()
