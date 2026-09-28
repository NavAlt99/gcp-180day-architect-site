#!/usr/bin/env python3
"""Build high-quality elevated Day 58 page for GCP 180-day study site."""
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DAY58 = ROOT / "content" / "day-058-page.html"

# Extract the header and day-jump from the existing day-058-page.html to preserve exact site structure
original_soup = BeautifulSoup(CONTENT_DAY58.read_text(encoding="utf-8"), "html.parser")
header_html = str(original_soup.header)

print(f"Header length: {len(header_html)} bytes")
