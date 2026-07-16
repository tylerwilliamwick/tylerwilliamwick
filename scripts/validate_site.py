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
