#!/usr/bin/env python3
"""Build and elevate content/day-057-page.html to highest architectural standard."""
import re
from pathlib import Path

SITE = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site")
ORIGINAL = SITE / "days" / "day-057.html"

content = ORIGINAL.read_text(encoding="utf-8")

# Extract the header and select#day-jump block from original to ensure 100% preservation of all 180 options
header_match = re.search(r'(<!doctype html>.*?<header class="site-nav">.*?</header>)', content, re.DOTALL)
if not header_match:
    raise ValueError("Could not extract header from days/day-057.html")
header_html = header_match.group(1)

# Ensure day 57 is selected in the day-jump dropdown
header_html = re.sub(r'<option value="day-\d{3}\.html" selected>', lambda m: m.group(0).replace(' selected', ''), header_html)
header_html = header_html.replace('<option value="day-057.html">Day 57: BGP, MTU and NAT diagnosis</option>',
                                  '<option value="day-057.html" selected>Day 57: BGP, MTU and NAT diagnosis</option>')

print("Header ready.")
