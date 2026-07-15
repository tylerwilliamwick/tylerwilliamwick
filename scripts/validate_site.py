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
assert "@media (prefers-reduced-motion: reduce)" in html

print("site validation passed")
