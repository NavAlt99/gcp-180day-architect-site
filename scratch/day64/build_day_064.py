from pathlib import Path

SITE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_FILE = SITE_DIR / "content" / "day-064-page.html"
DAY64_DIR = SITE_DIR / "scratch" / "day64"
DAYS_FILE = SITE_DIR / "days" / "day-064.html"

with open(DAYS_FILE, "r", encoding="utf-8") as f:
    existing_content = f.read()

header_end = existing_content.find("</header>") + len("</header>")
HEADER_NAV = existing_content[:header_end]

AUDIT_BANNER = '<div class="audit-banner"><strong>Draft content:</strong> Most lessons use generated templates and have not passed topic-level review. <a href="../CONTENT_AUDIT.md">Read the content audit</a>.</div>'

part1 = (DAY64_DIR / "part1.html").read_text(encoding="utf-8")
part2_svg = (DAY64_DIR / "part2_svg.html").read_text(encoding="utf-8")
part2_tech = (DAY64_DIR / "part2_tech.html").read_text(encoding="utf-8")
part3 = (DAY64_DIR / "part3.html").read_text(encoding="utf-8")
part4 = (DAY64_DIR / "part4.html").read_text(encoding="utf-8")

part2_full = part2_tech.replace("<!-- PART_2_SVG_PLACEHOLDER -->", part2_svg)

full_html = (
    HEADER_NAV
    + AUDIT_BANNER
    + part1
    + part2_full
    + part3
    + part4
)

OUTPUT_FILE.write_text(full_html, encoding="utf-8")
print(f"Successfully generated {OUTPUT_FILE} ({len(full_html)} bytes, {len(full_html.splitlines())} lines)")
