#!/usr/bin/env python3
"""Script to build complete content/day-001-page.html matching all contract requirements."""

import sys
from pathlib import Path

# Read the existing head + header to preserve the exact site nav, theme toggle, and 180 options
orig_path = Path("content/day-001-page.html")
orig_text = orig_path.read_text(encoding="utf-8")

header_end = orig_text.find("</header>") + len("</header>")
head_and_header = orig_text[:header_end]

print(f"Preserved head & header of length: {len(head_and_header)}")
