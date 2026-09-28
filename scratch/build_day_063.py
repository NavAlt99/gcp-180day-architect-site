# scratch/build_day_063.py
"""
Assemble and write content/day-063-page.html from scratch/*.html pieces.
"""
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = SITE_DIR / "content" / "day-063-page.html"
SCRATCH_DIR = SITE_DIR / "scratch"

# Read existing header from days/day-063.html or backup
DAYS_FILE = SITE_DIR / "days" / "day-063.html"
source_file = DAYS_FILE if DAYS_FILE.exists() else OUTPUT_FILE

with open(source_file, "r", encoding="utf-8") as f:
    existing_content = f.read()

header_end = existing_content.find("</header>") + len("</header>")
HEADER_NAV = existing_content[:header_end]

AUDIT_BANNER = '<div class="audit-banner"><strong>Draft content:</strong> Most lessons use generated templates and have not passed topic-level review. <a href="../CONTENT_AUDIT.md">Read the content audit</a>.</div>'

part1 = (SCRATCH_DIR / "part1.html").read_text(encoding="utf-8")
part2_svg = (SCRATCH_DIR / "part2_svg.html").read_text(encoding="utf-8")
part2_tech = (SCRATCH_DIR / "part2_tech.html").read_text(encoding="utf-8")
part3 = (SCRATCH_DIR / "part3.html").read_text(encoding="utf-8")
part4 = (SCRATCH_DIR / "part4.html").read_text(encoding="utf-8")

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
print(f"Successfully generated {OUTPUT_FILE} ({len(full_html)} bytes)")
