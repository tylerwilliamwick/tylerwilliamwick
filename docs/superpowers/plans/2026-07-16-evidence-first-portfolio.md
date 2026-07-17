# Evidence-First Portfolio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the live portfolio's unsupported banking/RFP story with a resume-backed civic-platform, GIS, and AI-assisted-discovery one-pager.

**Architecture:** Preserve the dependency-free GitHub Pages site and keep the implementation in the existing `index.html`, public assets, profile `README.md`, and standard-library validator. Delete the interactive explorer, link each featured metric to one of three semantic case articles, and generate the social preview from a temporary SVG using macOS `sips`.

**Tech Stack:** HTML5, CSS, SVG, PNG, Python 3 standard library, GitHub Pages

## Global Constraints

- `public/resume.pdf` is the source of truth.
- Use exactly three featured proof points: `350+ agencies`, `0-to-1 launch`, and `$2.17M ARR retained`.
- Use exactly three cases with the visible labels `Context`, `My role`, `Decision`, and `Outcome`.
- Remove unsupported digital banking, BECU, member-workflow, RFP, four-team, customer-win, recurring C-suite-readout, pen-test-style-review, Claude/Codex, 23-vendor, and AI-product-operations claims.
- Add no JavaScript, framework, analytics, CMS, animation library, or runtime/build dependency.
- Preserve the current GitHub Pages URL, resume, email, LinkedIn, GitHub, automatic dark mode, visible focus, and reduced-motion support.
- Publishing or merging is a separate explicit finish choice; do not push automatically.

---

### Task 1: Replace the portfolio with resume-backed evidence

**Files:**
- Modify: `scripts/validate_site.py`
- Modify: `index.html`
- Modify: `README.md`
- Create: `public/favicon.svg`
- Modify: `public/og-image.png`
- Temporary: `tmp/og-image.svg` (delete after rendering)

**Interfaces:**
- Consumes: `public/resume.pdf`, the approved design spec, and the existing static GitHub Pages workflow
- Produces: an evidence-first one-pager, aligned profile README, 64×64 SVG favicon, 1200×630 PNG social preview, and exit code 0 from `python3 scripts/validate_site.py`

- [ ] **Step 1: Replace the validator with the failing direction-1 contract**

Replace `scripts/validate_site.py` with:

```python
import re
import struct
from html.parser import HTMLParser
from pathlib import Path


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.section_ids = []
        self.hrefs = []
        self.hero_links = []
        self.skip_links = []
        self.metric_links = []
        self.case_ids = []
        self.case_labels = {}
        self.meta = {}
        self.canonical = None
        self.icons = []
        self.details = 0
        self.generic_labelledby = []
        self.images = []
        self.in_hero = False
        self.current_case = None
        self.in_case_label = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set(attrs.get("class", "").split())
        element_id = attrs.get("id")

        if element_id:
            self.ids.add(element_id)
        if tag == "section" and element_id:
            self.section_ids.append(element_id)
        if tag == "header" and "hero" in classes:
            self.in_hero = True
        if tag == "article" and "case-study" in classes:
            self.current_case = element_id
            self.case_ids.append(element_id)
            self.case_labels[element_id] = []
        if tag == "dt" and self.current_case:
            self.in_case_label = True
        if tag == "details":
            self.details += 1
        if tag == "div" and attrs.get("aria-labelledby"):
            self.generic_labelledby.append(attrs["aria-labelledby"])

        if tag == "a" and attrs.get("href"):
            href = attrs["href"]
            self.hrefs.append(href)
            if self.in_hero:
                self.hero_links.append(href)
            if "skip-link" in classes:
                self.skip_links.append(href)
            if "metric-link" in classes:
                self.metric_links.append(href)
        elif tag == "meta":
            key = attrs.get("property") or attrs.get("name")
            if key and attrs.get("content"):
                self.meta[key] = attrs["content"]
        elif tag == "link":
            rel = set(attrs.get("rel", "").split())
            if "canonical" in rel:
                self.canonical = attrs.get("href")
            if "icon" in rel and attrs.get("href"):
                self.icons.append(attrs["href"])
        elif tag == "img":
            self.images.append(attrs)

    def handle_endtag(self, tag):
        if tag == "header":
            self.in_hero = False
        elif tag == "article" and self.current_case:
            self.current_case = None
        elif tag == "dt":
            self.in_case_label = False

    def handle_data(self, data):
        if self.current_case and self.in_case_label and data.strip():
            self.case_labels[self.current_case].append(data.strip())


def png_size(path):
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{path} is not PNG"
    return struct.unpack(">II", data[16:24])


root = Path(__file__).resolve().parents[1]
html = (root / "index.html").read_text()
readme = (root / "README.md").read_text()
parser = SiteParser()
parser.feed(html)

assert "system-explorer" not in html, "interactive explorer still present"
assert parser.details == 0, "details disclosures remain"
assert parser.generic_labelledby == [], parser.generic_labelledby
assert parser.section_ids == ["outcomes", "cases", "capabilities", "contact"]
assert parser.hero_links == ["#cases", "public/resume.pdf"]
assert parser.skip_links == ["#content"]
assert parser.skip_links[0][1:] in parser.ids

case_ids = ["case-arcgis", "case-damage-assessment", "case-crm-eol"]
assert parser.case_ids == case_ids
assert parser.metric_links == [f"#{case_id}" for case_id in case_ids]
for case_id in case_ids:
    assert parser.case_labels[case_id] == [
        "Context",
        "My role",
        "Decision",
        "Outcome",
    ], (case_id, parser.case_labels[case_id])

required_hrefs = {
    "public/resume.pdf",
    "mailto:tylerwilliamwick@gmail.com",
    "https://www.linkedin.com/in/tylerwilliamwick/",
    "https://github.com/tylerwilliamwick",
}
assert required_hrefs.issubset(parser.hrefs)

site_url = "https://tylerwilliamwick.github.io/tylerwilliamwick/"
social_image = f"{site_url}public/og-image.png"
assert parser.canonical == site_url
assert parser.icons == ["public/favicon.svg"]
assert parser.meta["og:type"] == "website"
assert parser.meta["og:url"] == site_url
assert parser.meta["og:image"] == social_image
assert parser.meta["og:image:width"] == "1200"
assert parser.meta["og:image:height"] == "630"
assert parser.meta["twitter:image"] == social_image
assert parser.meta["og:image:alt"] == parser.meta["twitter:image:alt"]

for image in parser.images:
    assert image.get("alt") is not None, image
    assert image.get("width") and image.get("height"), image

copy = f"{html}\n{readme}".lower()
for pattern in (
    r"\bdigital banking\b",
    r"\bbecu\b",
    r"\bmember workflows?\b",
    r"\brfp\b",
    r"\bclaude code\b",
    r"\bcodex\b",
    r"\b23 vendors?\b",
):
    assert not re.search(pattern, copy), pattern

assert "civic platforms" in readme.lower()
assert "gis" in readme.lower()
assert "@media (prefers-reduced-motion: reduce)" in html
assert "public/portfolio-systems.png" not in html
assert (root / "public/resume.pdf").is_file()
assert (root / "public/favicon.svg").is_file()
assert png_size(root / "public/og-image.png") == (1200, 630)

print("site validation passed")
```

- [ ] **Step 2: Run the validator and verify the contract is red**

Run:

```bash
python3 scripts/validate_site.py
```

Expected: exit 1 with `AssertionError: interactive explorer still present`. This proves the new check rejects the live interactive baseline for the intended reason.

- [ ] **Step 3: Replace the page metadata**

In `index.html`, replace lines 6–18 with:

```html
    <title>Tyler Wick | Senior Product Manager | Civic Platforms, GIS &amp; AI</title>
    <meta
      name="description"
      content="Senior product manager for civic platforms, GIS, AI-assisted discovery, platform modernization, and customer transitions."
    >
    <link rel="canonical" href="https://tylerwilliamwick.github.io/tylerwilliamwick/">
    <link rel="icon" href="public/favicon.svg" type="image/svg+xml">
    <meta property="og:title" content="Tyler Wick | Senior Product Manager">
    <meta property="og:description" content="Civic-platform product leadership grounded in GIS, AI-assisted discovery, and measurable delivery outcomes.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tylerwilliamwick.github.io/tylerwilliamwick/">
    <meta property="og:image" content="https://tylerwilliamwick.github.io/tylerwilliamwick/public/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="Tyler Wick, Senior Product Manager for civic platforms, GIS, and AI-assisted discovery. Featured outcomes: 350+ agencies, a 0-to-1 launch, and $2.17M ARR retained.">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Tyler Wick | Senior Product Manager">
    <meta name="twitter:description" content="Civic-platform product leadership grounded in GIS, AI-assisted discovery, and measurable delivery outcomes.">
    <meta name="twitter:image" content="https://tylerwilliamwick.github.io/tylerwilliamwick/public/og-image.png">
    <meta name="twitter:image:alt" content="Tyler Wick, Senior Product Manager for civic platforms, GIS, and AI-assisted discovery. Featured outcomes: 350+ agencies, a 0-to-1 launch, and $2.17M ARR retained.">
    <meta name="theme-color" content="#047d75">
```

- [ ] **Step 4: Replace the page CSS**

Replace the entire existing `<style>...</style>` block with the following. This deletes every explorer, disclosure, tagline, skill-list, and non-interactive card-hover rule instead of leaving dead CSS.

```html
    <style>
      :root {
        --bg: #f5f7f3;
        --bg-alt: #e8efeb;
        --surface: #ffffff;
        --text: #14201c;
        --muted: #607069;
        --accent: #047d75;
        --accent-strong: #075e59;
        --on-accent: #ffffff;
        --copper: #8f4315;
        --border: #d5dfda;
        --grid: #e2e9e5;
        --shadow: 0 18px 42px rgba(28, 61, 50, 0.1);
      }

      @media (prefers-color-scheme: dark) {
        :root {
          --bg: #0f1715;
          --bg-alt: #17221f;
          --surface: #1a2824;
          --text: #f1f6f2;
          --muted: #a1b0aa;
          --accent: #62d0c3;
          --accent-strong: #8de3d8;
          --on-accent: #062a27;
          --copper: #f2a766;
          --border: #2d3c37;
          --grid: #1d2a26;
          --shadow: 0 18px 42px rgba(0, 0, 0, 0.26);
        }
      }

      * {
        box-sizing: border-box;
      }

      html {
        scroll-behavior: smooth;
      }

      body {
        margin: 0;
        background:
          radial-gradient(circle at 85% 4%, color-mix(in srgb, var(--accent) 12%, transparent), transparent 30rem),
          linear-gradient(90deg, var(--grid) 1px, transparent 1px),
          linear-gradient(0deg, var(--grid) 1px, transparent 1px),
          var(--bg);
        background-size: auto, 72px 72px, 72px 72px, auto;
        color: var(--text);
        font: 16px/1.65 Avenir, "Avenir Next", Inter, system-ui, -apple-system, sans-serif;
      }

      a {
        color: inherit;
      }

      a:focus-visible {
        outline: 3px solid var(--accent);
        outline-offset: 3px;
      }

      .skip-link {
        position: fixed;
        top: 8px;
        left: 8px;
        z-index: 20;
        transform: translateY(-160%);
        border-radius: 8px;
        padding: 9px 13px;
        background: var(--accent);
        color: var(--on-accent);
        font-weight: 700;
        text-decoration: none;
      }

      .skip-link:focus {
        transform: none;
      }

      .wrap {
        width: min(1120px, calc(100% - 40px));
        margin: 0 auto;
      }

      .nav {
        position: sticky;
        top: 0;
        z-index: 10;
        border-bottom: 1px solid color-mix(in srgb, var(--border) 78%, transparent);
        background: color-mix(in srgb, var(--bg) 86%, transparent);
        backdrop-filter: blur(16px);
      }

      .nav-inner,
      .footer-inner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
      }

      .nav-inner {
        min-height: 68px;
      }

      .mark {
        width: 40px;
        height: 40px;
        flex: 0 0 auto;
        border: 1px solid var(--border);
        border-radius: 12px;
        display: grid;
        place-items: center;
        background: var(--surface);
        color: var(--accent);
        font-family: Georgia, serif;
        font-size: 15px;
        text-decoration: none;
        box-shadow: 0 5px 18px color-mix(in srgb, var(--text) 7%, transparent);
      }

      .links,
      .footer-links {
        display: flex;
        flex-wrap: wrap;
        gap: 12px 22px;
        color: var(--muted);
        font-size: 14px;
      }

      .links {
        justify-content: flex-end;
      }

      .links a,
      .footer-links a {
        text-decoration: none;
      }

      .links a:hover,
      .footer-links a:hover {
        color: var(--accent);
      }

      .hero {
        padding: 76px 0 62px;
      }

      .eyebrow,
      .case-kicker {
        color: var(--copper);
        font-size: 12px;
        font-weight: 750;
        letter-spacing: 0.1em;
        text-transform: uppercase;
      }

      .eyebrow {
        margin: 0 0 18px;
      }

      h1,
      h2,
      h3 {
        font-family: Georgia, "Times New Roman", serif;
        font-weight: 400;
        line-height: 1.08;
      }

      h1 {
        max-width: 840px;
        margin: 0;
        font-size: clamp(2.75rem, 9vw, 6.75rem);
        letter-spacing: -0.045em;
      }

      .hero-copy {
        max-width: 820px;
        margin: 26px 0 0;
        color: color-mix(in srgb, var(--text) 80%, var(--muted));
        font-family: Georgia, "Times New Roman", serif;
        font-size: clamp(1.5rem, 3.4vw, 2.5rem);
        font-style: italic;
        line-height: 1.27;
      }

      .cta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 11px;
        margin-top: 32px;
      }

      .btn {
        border: 1px solid var(--border);
        border-radius: 11px;
        padding: 10px 15px;
        background: var(--surface);
        color: var(--text);
        font-size: 14px;
        font-weight: 650;
        overflow-wrap: anywhere;
        text-decoration: none;
        transition: transform 160ms ease, border-color 160ms ease, color 160ms ease, background 160ms ease;
      }

      .btn.primary {
        border-color: var(--accent);
        background: var(--accent);
        color: var(--on-accent);
      }

      .btn:hover {
        border-color: var(--accent);
        color: var(--accent);
        transform: translateY(-2px);
      }

      .btn.primary:hover {
        background: var(--accent-strong);
        color: var(--on-accent);
      }

      section {
        padding: 68px 0;
      }

      section[id],
      main[id] {
        scroll-margin-top: 84px;
      }

      .band {
        border-top: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
        background: color-mix(in srgb, var(--bg-alt) 78%, transparent);
      }

      .section-head {
        display: grid;
        grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
        gap: 34px;
        align-items: end;
        margin-bottom: 34px;
      }

      h2 {
        margin: 0;
        font-size: clamp(2.125rem, 4vw, 3.125rem);
        letter-spacing: -0.025em;
      }

      .section-head p,
      .lead {
        margin: 0;
        color: var(--muted);
      }

      .metrics,
      .cases,
      .capability-list {
        margin: 0;
        padding: 0;
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
        list-style: none;
      }

      .metric-link,
      .case-study,
      .capability {
        border: 1px solid var(--border);
        border-radius: 16px;
        background: color-mix(in srgb, var(--surface) 96%, transparent);
      }

      .metric-link {
        min-height: 164px;
        padding: 24px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 12px 30px color-mix(in srgb, var(--text) 5%, transparent);
        text-decoration: none;
        transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
      }

      .metric-link:hover {
        border-color: var(--accent);
        box-shadow: var(--shadow);
        transform: translateY(-2px);
      }

      .metric-link strong {
        color: var(--accent);
        font: 400 clamp(2.125rem, 4vw, 3.125rem)/1 Georgia, "Times New Roman", serif;
      }

      .metric-link span {
        margin-top: 14px;
        color: var(--muted);
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }

      .metric-link small {
        margin-top: 6px;
        color: var(--accent);
        font-weight: 700;
      }

      .case-study,
      .capability {
        padding: 25px;
      }

      .case-kicker {
        margin: 0 0 9px;
      }

      .case-study h3,
      .capability h3 {
        margin: 0;
        font-size: 25px;
      }

      .case-details {
        margin: 22px 0 0;
      }

      .case-details div {
        border-top: 1px solid var(--border);
        padding: 14px 0;
      }

      .case-details div:last-child {
        padding-bottom: 0;
      }

      .case-details dt {
        color: var(--copper);
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }

      .case-details dd {
        margin: 5px 0 0;
        color: var(--muted);
      }

      .capability p {
        margin: 12px 0 0;
        color: var(--muted);
      }

      .contact {
        display: grid;
        grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
        gap: 34px;
        align-items: center;
      }

      footer {
        border-top: 1px solid var(--border);
        padding: 28px 0;
        color: var(--muted);
        font-size: 14px;
      }

      .footer-links {
        justify-content: flex-end;
      }

      .visually-hidden {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
      }

      @media (max-width: 900px) {
        .section-head,
        .contact {
          grid-template-columns: 1fr;
        }

        .cases {
          grid-template-columns: 1fr;
        }
      }

      @media (max-width: 600px) {
        .wrap {
          width: min(100% - 28px, 1120px);
        }

        .nav {
          position: static;
        }

        .nav-inner,
        .footer-inner {
          align-items: flex-start;
          flex-wrap: wrap;
          padding-block: 10px;
        }

        .hero {
          padding: 54px 0 42px;
        }

        .links {
          gap: 9px 14px;
          font-size: 13px;
        }

        section {
          padding: 52px 0;
        }

        .metrics,
        .capability-list {
          grid-template-columns: 1fr;
        }

        .footer-links {
          justify-content: flex-start;
        }
      }

      @media (prefers-reduced-motion: reduce) {
        html {
          scroll-behavior: auto;
        }

        *,
        *::before,
        *::after {
          scroll-behavior: auto !important;
          transition-duration: 0.01ms !important;
        }
      }
    </style>
```

- [ ] **Step 5: Replace the page body**

Replace everything from `<body>` through `</body>` with:

```html
  <body>
    <a class="skip-link" href="#content">Skip to main content</a>
    <nav class="nav" aria-label="Primary">
      <div class="wrap nav-inner">
        <a class="mark" href="#content" aria-label="Tyler Wick home">TW</a>
        <div class="links">
          <a href="#cases">Cases</a>
          <a href="#capabilities">Capabilities</a>
          <a href="#contact">Contact</a>
        </div>
      </div>
    </nav>

    <main id="content">
      <header class="hero">
        <div class="wrap">
          <p class="eyebrow">Senior Product Manager | Civic Platforms | GIS | AI-Assisted Discovery</p>
          <h1>Tyler Wick</h1>
          <p class="hero-copy">
            I lead civic-platform products through modernization, discovery,
            and high-stakes customer transitions.
          </p>
          <div class="cta-row">
            <a class="btn primary" href="#cases">Selected work</a>
            <a class="btn" href="public/resume.pdf">Resume PDF</a>
          </div>
        </div>
      </header>

      <section id="outcomes" class="band" aria-labelledby="outcomes-title">
        <div class="wrap">
          <h2 id="outcomes-title" class="visually-hidden">Selected outcomes</h2>
          <ul class="metrics">
            <li>
              <a class="metric-link" href="#case-arcgis">
                <strong>350+</strong>
                <span>Government agencies</span>
                <small>View ArcGIS case</small>
              </a>
            </li>
            <li>
              <a class="metric-link" href="#case-damage-assessment">
                <strong>0-to-1</strong>
                <span>Spatial emergency-response launch</span>
                <small>View launch case</small>
              </a>
            </li>
            <li>
              <a class="metric-link" href="#case-crm-eol">
                <strong>$2.17M</strong>
                <span>ARR retained</span>
                <small>View transition case</small>
              </a>
            </li>
          </ul>
        </div>
      </section>

      <section id="cases" aria-labelledby="cases-title">
        <div class="wrap">
          <div class="section-head">
            <h2 id="cases-title">Selected Work</h2>
            <p>
              Three examples of product decisions with the context, ownership,
              and outcomes kept together.
            </p>
          </div>
          <div class="cases">
            <article id="case-arcgis" class="case-study">
              <p class="case-kicker">Platform continuity</p>
              <h3>ArcGIS compatibility at scale</h3>
              <dl class="case-details">
                <div>
                  <dt>Context</dt>
                  <dd>ArcGIS Enterprise upgrades affected Accela Civic Platform integrations used by more than 350 government agencies.</dd>
                </div>
                <div>
                  <dt>My role</dt>
                  <dd>As Product Manager, GIS &amp; Platform, I directed the upgrade posture.</dd>
                </div>
                <div>
                  <dt>Decision</dt>
                  <dd>Coordinate compatibility analysis, endpoint validation, customer communications, and rollout planning across the integrations.</dd>
                </div>
                <div>
                  <dt>Outcome</dt>
                  <dd>A compatibility program spanning 350+ government agencies.</dd>
                </div>
              </dl>
            </article>

            <article id="case-damage-assessment" class="case-study">
              <p class="case-kicker">Product discovery</p>
              <h3>Rapid Damage Assessment</h3>
              <dl class="case-details">
                <div>
                  <dt>Context</dt>
                  <dd>Accela was launching a Rapid Damage Assessment solution for state and local government agencies.</dd>
                </div>
                <div>
                  <dt>My role</dt>
                  <dd>I drove go-to-market and AI-assisted discovery with approximately 30 agencies and 150 interviews.</dd>
                </div>
                <div>
                  <dt>Decision</dt>
                  <dd>Shape the solution as a spatial-first emergency-response product.</dd>
                </div>
                <div>
                  <dt>Outcome</dt>
                  <dd>A successful 0-to-1 launch and early customer onboarding.</dd>
                </div>
              </dl>
            </article>

            <article id="case-crm-eol" class="case-study">
              <p class="case-kicker">Lifecycle strategy</p>
              <h3>Legacy CRM end-of-life</h3>
              <dl class="case-details">
                <div>
                  <dt>Context</dt>
                  <dd>Accela was retiring a legacy CRM application through an end-of-life program.</dd>
                </div>
                <div>
                  <dt>My role</dt>
                  <dd>I headed the program and secured executive and board approval.</dd>
                </div>
                <div>
                  <dt>Decision</dt>
                  <dd>Execute the transition through approximately 15 features across 12 epics, 100+ defect fixes, and management of approximately 50 customer incidents.</dd>
                </div>
                <div>
                  <dt>Outcome</dt>
                  <dd>121 customers and $2.17M ARR retained.</dd>
                </div>
              </dl>
            </article>
          </div>
        </div>
      </section>

      <section id="capabilities" class="band" aria-labelledby="capabilities-title">
        <div class="wrap">
          <div class="section-head">
            <h2 id="capabilities-title">Relevant Capabilities</h2>
            <p>
              The capabilities behind the work, grounded in shipped government
              platform products and customer programs.
            </p>
          </div>
          <ul class="capability-list">
            <li class="capability">
              <h3>Product Direction</h3>
              <p>Product strategy, roadmapping, go-to-market, analytics-driven prioritization, and product lifecycle management.</p>
            </li>
            <li class="capability">
              <h3>GIS &amp; Discovery</h3>
              <p>ArcGIS, spatial data, AI-assisted discovery, discovery interviews, user research, and competitive analysis.</p>
            </li>
            <li class="capability">
              <h3>Platform Delivery</h3>
              <p>API integration, workflow automation, Agile delivery, stakeholder communication, executive communication, customer onboarding, and revenue retention.</p>
            </li>
          </ul>
        </div>
      </section>

      <section id="contact" aria-labelledby="contact-title">
        <div class="wrap contact">
          <div>
            <h2 id="contact-title">Get In Touch</h2>
            <p class="lead">
              Open to senior product conversations in civic technology,
              government software, GIS-enabled platforms, and adjacent platform roles.
            </p>
          </div>
          <div class="cta-row">
            <a class="btn primary" href="mailto:tylerwilliamwick@gmail.com">tylerwilliamwick@gmail.com</a>
            <a class="btn" href="public/resume.pdf">Resume PDF</a>
            <a class="btn" href="https://www.linkedin.com/in/tylerwilliamwick/">LinkedIn</a>
            <a class="btn" href="https://github.com/tylerwilliamwick">GitHub</a>
          </div>
        </div>
      </section>
    </main>

    <footer>
      <div class="wrap footer-inner">
        <span>&copy; 2026 Tyler Wick</span>
        <div class="footer-links">
          <a href="mailto:tylerwilliamwick@gmail.com">Email</a>
          <a href="https://www.linkedin.com/in/tylerwilliamwick/">LinkedIn</a>
          <a href="https://github.com/tylerwilliamwick">GitHub</a>
        </div>
      </div>
    </footer>
  </body>
```

- [ ] **Step 6: Align the public profile README**

Replace `README.md` with:

```markdown
# Tyler Wick

Senior Product Manager focused on civic platforms, GIS, AI-assisted product discovery, platform modernization, and customer transitions.

Portfolio: https://tylerwilliamwick.github.io/tylerwilliamwick/

## Focus

- GIS-enabled platform strategy and roadmapping
- AI-assisted discovery and a 0-to-1 product launch
- Platform compatibility, API integration, and workflow automation
- Customer migration, lifecycle, onboarding, and revenue retention
- Go-to-market strategy and cross-functional delivery

## Connect

- Email: [tylerwilliamwick@gmail.com](mailto:tylerwilliamwick@gmail.com)
- LinkedIn: [linkedin.com/in/tylerwilliamwick](https://linkedin.com/in/tylerwilliamwick)
- GitHub: [github.com/tylerwilliamwick](https://github.com/tylerwilliamwick)
```

- [ ] **Step 7: Add the favicon**

Create `public/favicon.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="title">
  <title id="title">Tyler Wick</title>
  <rect width="64" height="64" rx="12" fill="#047d75"/>
  <text x="32" y="41" fill="#fff" font-family="Georgia,serif" font-size="25" text-anchor="middle">TW</text>
</svg>
```

- [ ] **Step 8: Regenerate the social preview**

Create the temporary directory:

```bash
mkdir -p tmp
```

Create temporary `tmp/og-image.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0V48" fill="none" stroke="#dfe7e2" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="1200" height="630" fill="#f5f7f3"/>
  <rect width="1200" height="630" fill="url(#grid)"/>
  <rect width="1200" height="10" fill="#047d75"/>
  <text x="80" y="148" fill="#14201c" font-family="Georgia,serif" font-size="76">Tyler Wick</text>
  <text x="80" y="214" fill="#14201c" font-family="Avenir,Arial,sans-serif" font-size="32">Senior Product Manager</text>
  <text x="80" y="264" fill="#607069" font-family="Avenir,Arial,sans-serif" font-size="25">Civic Platforms  |  GIS  |  AI-Assisted Discovery</text>

  <g transform="translate(80 350)">
    <rect width="300" height="150" rx="14" fill="#fff" stroke="#d5dfda"/>
    <text x="24" y="68" fill="#047d75" font-family="Georgia,serif" font-size="52">350+</text>
    <text x="24" y="108" fill="#607069" font-family="Avenir,Arial,sans-serif" font-size="18">GOVERNMENT AGENCIES</text>
  </g>
  <g transform="translate(450 350)">
    <rect width="300" height="150" rx="14" fill="#fff" stroke="#d5dfda"/>
    <text x="24" y="68" fill="#047d75" font-family="Georgia,serif" font-size="52">0-to-1</text>
    <text x="24" y="108" fill="#607069" font-family="Avenir,Arial,sans-serif" font-size="18">PRODUCT LAUNCH</text>
  </g>
  <g transform="translate(820 350)">
    <rect width="300" height="150" rx="14" fill="#fff" stroke="#d5dfda"/>
    <text x="24" y="68" fill="#047d75" font-family="Georgia,serif" font-size="52">$2.17M</text>
    <text x="24" y="108" fill="#607069" font-family="Avenir,Arial,sans-serif" font-size="18">ARR RETAINED</text>
  </g>

  <text x="80" y="574" fill="#8f4315" font-family="Avenir,Arial,sans-serif" font-size="19">Evidence-led product leadership for government platforms</text>
</svg>
```

Render and remove only the known temporary source:

```bash
sips -s format png tmp/og-image.svg --out public/og-image.png
rm tmp/og-image.svg
rmdir tmp
```

Expected: `public/og-image.png` is 1200×630 and `tmp/` no longer exists.

- [ ] **Step 9: Run the validator and whitespace check**

Run:

```bash
python3 scripts/validate_site.py
git diff --check
```

Expected:

```text
site validation passed
```

Both commands exit 0 with no warnings.

- [ ] **Step 10: Inspect the generated social preview**

Open `public/og-image.png` with the local image viewer. Confirm all text is readable, the three metric cards fit inside the 1200×630 canvas, no glyphs are clipped, and the image contains no banking or RFP language.

- [ ] **Step 11: Verify the page in a local browser**

Run:

```bash
python3 -m http.server 4173
```

Open `http://127.0.0.1:4173/` and verify:

- desktop at 1440×900;
- narrow layout at 320 CSS pixels;
- 200% zoom without horizontal scrolling or obscured content;
- keyboard focus reaches the skip link, navigation, metrics, hero actions, and Contact links in document order;
- each metric link lands on its matching case;
- automatic dark mode remains readable;
- non-interactive cases and capabilities do not lift or imply click behavior.

Stop the local server after verification.

- [ ] **Step 12: Run final checks and commit**

Run:

```bash
python3 scripts/validate_site.py
git diff --check
git status --short
```

Expected: validation passes, whitespace check exits 0, and status lists only `README.md`, `index.html`, `public/favicon.svg`, `public/og-image.png`, and `scripts/validate_site.py`.

Commit:

```bash
git add README.md index.html public/favicon.svg public/og-image.png scripts/validate_site.py
git commit -m "feat: make portfolio evidence-first"
```

## Post-review addendum

The final review hardened `scripts/validate_site.py` to preserve approved copy, metric values and order, case outcomes, local fragment targets, labelled semantic sections, the semantic metric list, script-free markup, and evidence-first public positioning.
