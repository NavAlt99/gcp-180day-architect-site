#!/usr/bin/env python3
"""Assemble and validate Day 57 page."""
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

SITE = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site")
ORIGINAL = SITE / "days" / "day-057.html"
TARGET = SITE / "content" / "day-057-page.html"

from build_day57_complete import header_html, hero_and_toc
from part1_topics import part1_html
from part2_svg import part2_svg
from part2_technical import part2_text
from part3_incidents import part3_html
from part4_labs import part4_html
from completion_and_pager import completion_and_pager_html

part2_combined = part2_text.replace("__PART2_SVG__", part2_svg)

full_html = header_html + hero_and_toc + part1_html + part2_combined + part3_html + part4_html + completion_and_pager_html

print(f"Generated full HTML: {len(full_html)} characters.")

# Validate with BeautifulSoup
soup = BeautifulSoup(full_html, "html.parser")
ids = [x.get("id") for x in soup.select("[id]")]
id_counts = {}
for i in ids:
    id_counts[i] = id_counts.get(i, 0) + 1
duplicates = [i for i, c in id_counts.items() if c > 1]
if duplicates:
    print("ERROR: Duplicate IDs found:", duplicates)
    sys.exit(1)
else:
    print(f"Unique IDs: {len(ids)}, zero duplicates.")

# Check required phrases
for phrase in ("Outcome:", "Entry prerequisites:", "Exit artifact", "Daily evidence"):
    if phrase not in soup.get_text(" "):
        print(f"ERROR: Missing phrase '{phrase}'")
        sys.exit(1)
print("All required phrases present.")

# Check for runnable commands outside code block
cmd_errors = []
for code in soup.select("code"):
    value = code.get_text(" ", strip=True)
    if code.parent.name != "pre" and re.match(r"^(?:sudo |git |gcloud |terraform |kubectl |docker |python3? |curl |ssh |cat |printf |mkdir |cd |pwd$|ls(?: |$)|command |ip |dig |nslookup |systemctl |journalctl )", value):
        cmd_errors.append(value[:60])

if cmd_errors:
    print("ERROR: Runnable commands outside pre/code:", cmd_errors)
    sys.exit(1)
else:
    print("Zero runnable commands outside <pre><code>.")

# Check build.py validate_day_override
sys.path.insert(0, str(SITE / "scripts"))
from build import parse_days, validate_day_override

days = parse_days()
day57 = [d for d in days if d["number"] == 57][0]
try:
    validate_day_override(full_html, day57)
    print("validate_day_override passed!")
except Exception as e:
    print("ERROR in validate_day_override:", e)
    sys.exit(1)

# Write to TARGET
TARGET.write_text(full_html, encoding="utf-8")
print(f"Successfully wrote {TARGET} ({len(full_html)} bytes)")

