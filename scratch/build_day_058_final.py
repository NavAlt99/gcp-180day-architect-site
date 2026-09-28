#!/usr/bin/env python3
"""Build the comprehensive, production-grade Day 58 page for the GCP 180-Day platform."""
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site")
ORIGINAL = ROOT / "content" / "day-058-page.html"
OUTPUT = ROOT / "content" / "day-058-page.html"

# Extract header from original
soup_orig = BeautifulSoup(ORIGINAL.read_text(encoding="utf-8"), "html.parser")
header_html = str(soup_orig.header)

print(f"Loaded original header ({len(header_html)} bytes)")
