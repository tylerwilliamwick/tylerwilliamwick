import re
import struct
from html.parser import HTMLParser
from pathlib import Path


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.sections = []
        self.hrefs = []
        self.hero_links = []
        self.skip_links = []
        self.metric_links = []
        self.metrics = False
        self.metric_values = []
        self.case_ids = []
        self.case_labels = {}
        self.case_values = {}
        self.capability_copy = {}
        self.meta = {}
        self.canonical = None
        self.icons = []
        self.details = 0
        self.generic_labelledby = []
        self.images = []
        self.in_hero = False
        self.in_metrics = False
        self.in_metric_value = False
        self.current_case = None
        self.in_case_label = False
        self.current_case_label = None
        self.in_case_value = False
        self.in_capability = False
        self.current_capability = None
        self.in_capability_heading = False
        self.in_capability_copy = False
        self.scripts = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set(attrs.get("class", "").split())
        element_id = attrs.get("id")

        if element_id:
            self.ids.add(element_id)
        if tag == "section":
            self.sections.append((element_id, attrs.get("aria-labelledby")))
        if tag == "header" and "hero" in classes:
            self.in_hero = True
        if tag == "ul" and attrs.get("class") == "metrics":
            self.metrics = True
            self.in_metrics = True
        if tag == "strong" and self.in_metrics:
            self.in_metric_value = True
        if tag == "article" and "case-study" in classes:
            self.current_case = element_id
            self.case_ids.append(element_id)
            self.case_labels[element_id] = []
            self.case_values[element_id] = {}
        if tag == "dt" and self.current_case:
            self.in_case_label = True
        if tag == "dd" and self.current_case and self.case_labels[self.current_case]:
            self.current_case_label = self.case_labels[self.current_case][-1]
            self.in_case_value = True
        if tag == "li" and "capability" in classes:
            self.in_capability = True
            self.current_capability = None
        if tag == "h3" and self.in_capability:
            self.in_capability_heading = True
        if tag == "p" and self.in_capability and self.current_capability:
            self.in_capability_copy = True
        if tag == "details":
            self.details += 1
        if tag == "script":
            self.scripts += 1
        if tag == "div" and attrs.get("aria-labelledby"):
            self.generic_labelledby.append(attrs["aria-labelledby"])

        if attrs.get("href"):
            href = attrs["href"]
            self.hrefs.append(href)
            if tag == "a":
                if self.in_hero:
                    self.hero_links.append(href)
                if "skip-link" in classes:
                    self.skip_links.append(href)
                if "metric-link" in classes:
                    self.metric_links.append(href)
        if tag == "meta":
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
        elif tag == "ul" and self.in_metrics:
            self.in_metrics = False
        elif tag == "strong":
            self.in_metric_value = False
        elif tag == "dd":
            self.in_case_value = False
            self.current_case_label = None
        elif tag == "h3":
            self.in_capability_heading = False
        elif tag == "p":
            self.in_capability_copy = False
        elif tag == "li" and self.in_capability:
            self.in_capability = False
            self.current_capability = None
        elif tag == "article" and self.current_case:
            self.current_case = None
        elif tag == "dt":
            self.in_case_label = False

    def handle_data(self, data):
        if data.strip():
            self.text.append(data.strip())
            if self.in_metric_value:
                self.metric_values.append(data.strip())
            if self.current_case and self.in_case_label:
                self.case_labels[self.current_case].append(data.strip())
            if self.current_case and self.in_case_value:
                self.case_values[self.current_case].setdefault(
                    self.current_case_label, []
                ).append(data.strip())
            if self.in_capability_heading:
                self.current_capability = data.strip()
            if self.in_capability_copy:
                self.capability_copy.setdefault(self.current_capability, []).append(
                    data.strip()
                )


def png_size(path):
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{path} is not PNG"
    return struct.unpack(">II", data[16:24])


root = Path(__file__).resolve().parents[1]
html = (root / "index.html").read_text()
readme = (root / "README.md").read_text()
parser = SiteParser()
parser.feed(html)
page_copy = "\n".join(parser.text)
readme_copy = re.sub(r"<!--.*?-->", "", readme, flags=re.S)
focus = re.search(r"(?ms)^## Focus\n\n(.*?)(?=^## |\Z)", readme_copy)

assert "system-explorer" not in html, "interactive explorer still present"
assert parser.details == 0, "details disclosures remain"
assert parser.generic_labelledby == [], parser.generic_labelledby
sections = [
    ("outcomes", "outcomes-title"),
    ("cases", "cases-title"),
    ("capabilities", "capabilities-title"),
    ("contact", "contact-title"),
]
assert parser.sections == sections
assert all(label in parser.ids for _, label in sections)
assert parser.hero_links == ["#cases", "public/resume.pdf"]
assert parser.skip_links == ["#content"]
assert parser.skip_links[0][1:] in parser.ids
assert all(href[1:] in parser.ids for href in parser.hrefs if href.startswith("#"))
assert parser.metrics, 'metrics must be a semantic <ul class="metrics">'
assert parser.metric_values == ["350+", "0-to-1", "$2.17M"]
assert parser.scripts == 0, "script tag present"

case_ids = ["case-arcgis", "case-damage-assessment", "case-crm-eol"]
assert parser.case_ids == case_ids
assert re.search(
    r"\.case-study\[id\]\s*\{[^}]*scroll-margin-top:\s*84px",
    html,
), "case anchors lack scroll margin"
assert parser.metric_links == [f"#{case_id}" for case_id in case_ids]
for case_id in case_ids:
    assert parser.case_labels[case_id] == [
        "Context",
        "My role",
        "Decision",
        "Outcome",
    ], (case_id, parser.case_labels[case_id])
assert [
    parser.case_values[case_id].get("Outcome") for case_id in case_ids
] == [
    ["A compatibility program spanning 350+ government agencies."],
    ["A successful 0-to-1 launch and early customer onboarding."],
    ["121 customers and $2.17M ARR retained."],
], "approved case outcome missing or altered"
assert parser.case_values["case-crm-eol"].get("Context") == [
    "Accela was retiring a legacy CRM application through an end-of-life program."
], "approved CRM context missing or altered"
assert "stakeholder communication, executive communication" in " ".join(
    parser.capability_copy.get("Platform Delivery", [])
), (
    "executive communication missing from Platform Delivery"
)
assert focus and re.search(
    r"(?m)^- AI-assisted discovery and a 0-to-1 product launch$", focus.group(1)
), (
    "singular README wording missing"
)
assert focus and "0-to-1 product launches" not in focus.group(1), (
    "plural README wording remains in Focus"
)

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

copy = f"{page_copy}\n{readme_copy}".lower()
for pattern in (
    r"\bbanking\b",
    r"\bbecu\b",
    r"\bmembers?\b",
    r"\brfps?\b",
    r"\bfour[- ]teams?\b",
    r"\bcustomer[- ]wins?\b",
    r"\brecurring c[- ]suite[- ]readouts?\b",
    r"\bpen[- ]test[- ]style[- ]reviews?\b",
    r"\bclaude\b",
    r"\bcodex\b",
    r"\b23[- ]vendors?\b",
    r"\bai(?:[- ]assisted)?[- ]product[- ]operations?\b",
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
