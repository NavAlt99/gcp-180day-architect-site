#!/usr/bin/env python3
"""Assemble and validate Day 58 page."""
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

from blocks_intro import HERO_HTML, TOC_HTML, PART1_HTML
from blocks_svg import FIG_58_1_ARCH_SVG
from blocks_technical import PART2_TOPIC1_HTML, PART2_TOPIC2_HTML
from blocks_problems import PART3_HTML
from blocks_labs import PART4_HTML

ROOT = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site")
ORIGINAL = ROOT / "content" / "day-058-page.html"
OUTPUT = ROOT / "content" / "day-058-page.html"

# Extract header from original
soup_orig = BeautifulSoup(ORIGINAL.read_text(encoding="utf-8"), "html.parser")
header_html = str(soup_orig.header)

pre_main = f"""<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark light"><title>Day 58: Object storage and local durability · GCP 180 days</title><link rel="stylesheet" href="../assets/site.css"><script defer src="../assets/site.js"></script></head><body><a class="skip" href="#main">Skip to content</a>{header_html}<div class="audit-banner"><strong>Draft content:</strong> Most lessons use generated templates and have not passed topic-level review. <a href="../CONTENT_AUDIT.md">Read the content audit</a>.</div><main id="main" class="container day" data-day="58" data-prev="day-057.html" data-next="day-059.html" data-index="../index.html"><div class="crumb"><a href="../index.html">Roadmap index</a> / <a href="../index.html#block-core-services-and-integrated-practice">Core services and integrated practice</a> / Day 58 of 180</div>"""

part2_full = f"""<section id="part-2" class="part">
<h2>2 · Technical discussion of each topic</h2>

{FIG_58_1_ARCH_SVG}

{PART2_TOPIC1_HTML}

{PART2_TOPIC2_HTML}
</section>"""

full_html = f"""{pre_main}
{HERO_HTML}

{TOC_HTML}

{PART1_HTML}

{part2_full}

{PART3_HTML}

{PART4_HTML}
"""

# Validation checks on full_html
soup = BeautifulSoup(full_html, "html.parser")

# 1. Check duplicate IDs
ids = [x.get("id") for x in soup.select("[id]")]
seen = set()
duplicates = []
for i in ids:
    if i in seen:
        duplicates.append(i)
    seen.add(i)

if duplicates:
    print(f"ERROR: Duplicate IDs found: {duplicates}")
    sys.exit(1)
else:
    print(f"SUCCESS: All {len(ids)} IDs are unique!")

# 2. Check required IDs
required_ids = {
    "main", "day-jump", "part-1", "part-2", "part-3", "part-4",
    "topic-01-overview", "topic-01-technical", "topic-01-problem", "topic-01-lab",
    "topic-02-overview", "topic-02-technical", "topic-02-problem", "topic-02-lab",
}
missing = required_ids - set(ids)
if missing:
    print(f"ERROR: Missing required IDs: {missing}")
    sys.exit(1)
else:
    print("SUCCESS: All required IDs present!")

# 3. Check day jump options
day_jump_options = soup.select("#day-jump option[value^='day-']")
if len(day_jump_options) != 180:
    print(f"ERROR: Expected 180 day options, got {len(day_jump_options)}")
    sys.exit(1)
else:
    print("SUCCESS: Exactly 180 day options present!")

# 4. Check runnable commands outside pre
cmd_pattern = r"^(?:sudo |git |gcloud |terraform |kubectl |docker |python3? |curl |ssh |cat |printf |mkdir |cd |pwd$|ls(?: |$)|command |ip |dig |nslookup |systemctl |journalctl )"
cmd_errors = []
for code in soup.select("code"):
    val = code.get_text(" ", strip=True)
    if code.parent.name != "pre" and re.match(cmd_pattern, val):
        cmd_errors.append(val)

if cmd_errors:
    print(f"ERROR: Runnable commands outside pre: {cmd_errors}")
    sys.exit(1)
else:
    print("SUCCESS: No runnable commands outside <pre><code>!")

# 5. Check pre tags without code
pre_errors = []
for pre in soup.select("pre"):
    if not pre.select_one("code"):
        pre_errors.append(pre.get_text()[:40])
    if pre.select_one("kbd"):
        pre_errors.append("kbd inside pre")

if pre_errors:
    print(f"ERROR: Malformed pre elements: {pre_errors}")
    sys.exit(1)
else:
    print("SUCCESS: All <pre> elements have <code> and no <kbd>!")

# 6. Check required phrases
required_phrases = ["Outcome:", "Entry prerequisites:", "Exit artifact", "Daily evidence"]
for phrase in required_phrases:
    if phrase not in soup.get_text(" "):
        print(f"ERROR: Missing required phrase: '{phrase}'")
        sys.exit(1)
print("SUCCESS: All required phrases present!")

# Write file
OUTPUT.write_text(full_html, encoding="utf-8")
print(f"Successfully wrote {len(full_html)} bytes to {OUTPUT}")
