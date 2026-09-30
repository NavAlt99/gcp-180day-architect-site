#!/usr/bin/env python3
"""Generate complete content/day-001-page.html complying with all PAGE_AUTHORING_CONTRACT.md requirements."""

import re
from pathlib import Path

SITE = Path(".")
orig_path = SITE / "content" / "day-001-page.html"
orig_text = orig_path.read_text(encoding="utf-8")

# Extract the header and head
header_end = orig_text.find("</header>") + len("</header>")
head_and_header = orig_text[:header_end]

# Extract footer and closing tags
footer_start = orig_text.find('<footer class="site-footer">')
footer_and_end = orig_text[footer_start:]

print("Head and header length:", len(head_and_header))
print("Footer and end length:", len(footer_and_end))
