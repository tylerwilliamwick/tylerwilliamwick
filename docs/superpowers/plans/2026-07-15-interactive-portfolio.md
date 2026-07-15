# Interactive Portfolio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the hero’s static systems image with an accessible interactive product-system explorer and ship a cohesive visual polish pass to the live GitHub Pages portfolio.

**Architecture:** Preserve the dependency-free single-page site. Use grouped native `<details>` elements for interaction, CSS for the map-like presentation and motion, and one standard-library Python validator for structural regression coverage.

**Implementation refinement:** Visual QA favored a full-width guided sequence over the original two-column draft. The stacked layout preserves the Frame-to-Learn reading order and avoids uneven grid rows when a disclosure expands; all native interaction and responsive requirements remain unchanged.

**Tech Stack:** HTML5, CSS, Python 3 standard library, GitHub Actions, GitHub Pages

## Global Constraints

- Keep the existing public URL and GitHub Pages workflow.
- Add no runtime or build dependencies.
- Preserve the résumé, email, LinkedIn, GitHub, dark mode, responsive layout, and existing employer-facing proof.
- Use semantic native controls with visible focus and reduced-motion support.
- Retain `public/og-image.png`; remove the unused `public/portfolio-systems.png`.

---

### Task 1: Add the structural regression check

**Files:**
- Create: `scripts/validate_site.py`
- Test: `scripts/validate_site.py`

**Interfaces:**
- Consumes: repository-root `index.html` and `public/resume.pdf`
- Produces: exit code 0 plus `site validation passed`, or an assertion failure describing the broken invariant

- [ ] **Step 1: Write the validator**

```python
from html.parser import HTMLParser
from pathlib import Path


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.details = []
        self.hrefs = set()
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "details" and "system-stage" in attrs.get("class", "").split():
            self.details.append(attrs)
        elif tag == "a" and attrs.get("href"):
            self.hrefs.add(attrs["href"])
        elif tag == "img" and attrs.get("src"):
            self.images.append(attrs["src"])


root = Path(__file__).resolve().parents[1]
html = (root / "index.html").read_text()
parser = SiteParser()
parser.feed(html)

assert len(parser.details) == 4, parser.details
assert {item.get("name") for item in parser.details} == {"product-system"}
assert sum("open" in item for item in parser.details) == 1
assert "public/portfolio-systems.png" not in parser.images
assert "public/resume.pdf" in parser.hrefs
assert "mailto:tylerwilliamwick@gmail.com" in parser.hrefs
assert (root / "public/resume.pdf").is_file()
assert "prefers-reduced-motion" in html
print("site validation passed")
```

- [ ] **Step 2: Run the validator to prove the current page fails**

Run: `python3 scripts/validate_site.py`

Expected: FAIL at `assert len(parser.details) == 4` because the current page still contains the static image.

- [ ] **Step 3: Commit the failing check with the implementation task**

Do not commit a permanently red branch; stage this file with Task 2 after the page passes.

---

### Task 2: Replace the image and polish the visual system

**Files:**
- Modify: `index.html`
- Delete: `public/portfolio-systems.png`
- Include: `scripts/validate_site.py`

**Interfaces:**
- Consumes: the existing hero, proof, evidence, skills, contact, and theme tokens
- Produces: four grouped `.system-stage` disclosures and a responsive `.system-explorer` presentation

- [ ] **Step 1: Replace the static figure with the explorer**

Insert a `.system-intro` header followed by four grouped disclosures:

```html
<section class="system-explorer" aria-labelledby="system-title">
  <div class="system-intro">
    <p class="kicker">Interactive product system</p>
    <h2 id="system-title">From ambiguity to measurable outcomes.</h2>
    <p>Select a stage to see how I move regulated product work forward.</p>
  </div>
  <div class="system-map">
    <details class="system-stage" name="product-system" open>
      <summary><span>01</span><strong>Frame</strong><small>Turn signals into a decision</small></summary>
      <div class="stage-detail"><p>Customer evidence, market context, and constraints become a crisp problem statement.</p><ul><li>Discovery and feedback synthesis</li><li>Competitive and vendor evaluation</li></ul><b>Proof: analysis across 23 vendors</b></div>
    </details>
    <details class="system-stage" name="product-system">
      <summary><span>02</span><strong>Align</strong><small>Make the tradeoffs legible</small></summary>
      <div class="stage-detail"><p>Outcomes, sequencing, and risk are translated into roadmaps teams and executives can use.</p><ul><li>Roadmap and Agile planning</li><li>RFP and executive readouts</li></ul><b>Proof: roadmap ownership across 4 teams</b></div>
    </details>
    <details class="system-stage" name="product-system">
      <summary><span>03</span><strong>Ship</strong><small>Deliver through constraints</small></summary>
      <div class="stage-detail"><p>Cross-functional delivery stays anchored to customer value, security, and adoption.</p><ul><li>API migration and lifecycle delivery</li><li>QA, security, and accessibility review</li></ul><b>Proof: 97% API migration conversion</b></div>
    </details>
    <details class="system-stage" name="product-system">
      <summary><span>04</span><strong>Learn</strong><small>Close the operating loop</small></summary>
      <div class="stage-detail"><p>Results and feedback reshape priorities, messaging, and the next product decision.</p><ul><li>Adoption and retention feedback</li><li>AI-assisted product operations</li></ul><b>Proof: $2.17M ARR retained</b></div>
    </details>
  </div>
</section>
```

- [ ] **Step 2: Apply the cohesive CSS polish**

Update theme tokens to include `--shadow`, `--glow`, and `--radius`; increase the hero/section rhythm; style `.system-explorer`, `.system-map`, `.system-stage`, `summary`, and `.stage-detail`; give `.metric`, `.card`, and `.btn` consistent transitions and focus states; collapse the explorer to one column below 760px; and disable nonessential transitions inside `@media (prefers-reduced-motion: reduce)`.

Use these exact interaction rules:

```css
.system-map { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.system-stage { border: 1px solid var(--border); border-radius: var(--radius); background: var(--surface); overflow: clip; transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease; }
.system-stage[open] { border-color: var(--accent); box-shadow: var(--shadow); transform: translateY(-2px); }
.system-stage summary { min-height: 112px; padding: 20px; display: grid; grid-template-columns: auto 1fr; gap: 2px 14px; cursor: pointer; list-style: none; }
.system-stage summary::-webkit-details-marker { display: none; }
.system-stage summary span { grid-row: 1 / 3; color: var(--copper); font: 700 12px/1 system-ui, sans-serif; }
.system-stage summary strong { font: 400 28px/1.05 Georgia, serif; }
.system-stage summary small { color: var(--muted); font-size: 13px; }
.stage-detail { border-top: 1px solid var(--border-light); padding: 0 20px 20px; }
summary:focus-visible, a:focus-visible { outline: 3px solid color-mix(in srgb, var(--accent) 55%, transparent); outline-offset: 4px; }
@media (max-width: 760px) { .system-map { grid-template-columns: 1fr; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { scroll-behavior: auto !important; transition-duration: 0.01ms !important; } }
```

- [ ] **Step 3: Remove the obsolete asset**

Run: `rm public/portfolio-systems.png`

Expected: only `public/og-image.png` and `public/resume.pdf` remain under `public/`.

- [ ] **Step 4: Run the validator**

Run: `python3 scripts/validate_site.py`

Expected: `site validation passed`.

- [ ] **Step 5: Run static quality checks**

Run: `git diff --check && python3 -m http.server 4173`

Expected: no whitespace errors; the local server reports port 4173.

- [ ] **Step 6: Verify the local page**

Open `http://127.0.0.1:4173`, confirm the four summaries work with click and keyboard, the first stage is initially open, one stage remains open at a time, focus is visible, and the layout remains readable at desktop and narrow widths.

- [ ] **Step 7: Commit**

```bash
git add index.html scripts/validate_site.py public/portfolio-systems.png
git commit -m "feat: add interactive product system"
```

---

### Task 3: Publish and verify production

**Files:**
- Verify: `.github/workflows/pages-static.yml`

**Interfaces:**
- Consumes: committed static source on `main`
- Produces: successful GitHub Pages deployment at `https://tylerwilliamwick.github.io/tylerwilliamwick/`

- [ ] **Step 1: Push the validated commits**

Run: `git push origin main`

Expected: remote `main` advances to the interactive portfolio commit.

- [ ] **Step 2: Wait for the Pages workflow**

Check the workflow run for the pushed commit until it reaches `completed/success`.

- [ ] **Step 3: Verify production**

Fetch the live page and assert HTTP 200, four `.system-stage` disclosures, no `portfolio-systems.png` reference, and HTTP 200 for `public/og-image.png` and `public/resume.pdf`.

- [ ] **Step 4: Open the finished site**

Open `https://tylerwilliamwick.github.io/tylerwilliamwick/` in the in-app browser and present it to the user.
