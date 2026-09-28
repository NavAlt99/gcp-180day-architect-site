#!/usr/bin/env python3
"""Build and validate content/day-061-page.html for Day 61."""
from pathlib import Path
import re
import html

SITE_ROOT = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site")
ORIG_PAGE = SITE_ROOT / "content" / "day-061-page.html"

# Extract header from original day-061-page.html to preserve all 180 navigation options
orig_content = ORIG_PAGE.read_text(encoding="utf-8")
header_start = orig_content.find('<header class="site-nav">')
header_end = orig_content.find('</header>') + len('</header>')
site_header = orig_content[header_start:header_end]

print(f"Extracted site header: {len(site_header)} characters")
