#!/usr/bin/env python3
"""Assemble and validate content/day-062-page.html."""
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

SITE_ROOT = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site")
ORIG_PAGE = SITE_ROOT / "content" / "day-062-page.html"

# Import parts
sys.path.insert(0, str(SITE_ROOT / "scratch" / "day62"))
from part1_topics import get_part1_html
from part2_svg import get_part2_svg
from part2_technical import get_part2_technical_html
from part3_incidents import get_part3_incidents_html

def get_part4_labs_html():
    return (SITE_ROOT / "scratch" / "day62" / "part4_labs.html").read_text(encoding="utf-8")

# Extract header from original day-062-page.html to preserve all 180 navigation options
orig_content = ORIG_PAGE.read_text(encoding="utf-8")
header_start = orig_content.find('<header class="site-nav">')
header_end = orig_content.find('</header>') + len('</header>')
site_header = orig_content[header_start:header_end]

html_parts = []

# DOCTYPE and HEAD
html_parts.append("""<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark light"><title>Day 62: Distributed and nonrelational database choices · GCP 180 days</title><link rel="stylesheet" href="../assets/site.css"><script defer src="../assets/site.js"></script></head><body><a class="skip" href="#main">Skip to content</a>""")

# SITE HEADER
html_parts.append(site_header)

# AUDIT BANNER & MAIN OPENING & HERO
html_parts.append("""<div class="audit-banner"><strong>Draft content:</strong> Most lessons use generated templates and have not passed topic-level review. <a href="../CONTENT_AUDIT.md">Read the content audit</a>.</div><main id="main" class="container day" data-day="62" data-prev="day-061.html" data-next="day-063.html" data-index="../index.html"><div class="crumb"><a href="../index.html">Roadmap index</a> / <a href="../index.html#block-core-services-and-integrated-practice">Core services and integrated practice</a> / Day 62 of 180</div><section class="hero"><div class="pills"><span class="pill">DAY 62</span><span class="pill">3–4 hours</span><span class="pill">tabletop / design</span><span class="pill">Topics 020</span></div><h1>Day 62 — Distributed and nonrelational database choices</h1><p class="lead"><strong>Outcome:</strong> Compare Spanner, Firestore and Bigtable using the retailer's access patterns; model a hotspot and trace leader/replica/quorum behavior from public documentation.</p><div><strong>Entry prerequisites:</strong> <p><a href="day-061.html">Day 61</a>; bring their exit artifacts.</p></div><div class="callout success"><strong>Exit artifact</strong><p>Three schema/key sketches, one selection ADR and an explicit consistency/failover assumption per option saved to <code>day-062-distributed-db-adr.md</code>.</p></div><p class="small">Source curriculum checked 2026-09-26; external documentation links are selected reading and may change. A tabletop result is a design exercise, not a production test.</p></section>""")

# TOC ASIDE
html_parts.append("""<aside class="toc" aria-label="On this page"><strong>On this page</strong><a href="#part-1">1 · Topics</a><a href="#part-2">2 · Technical discussion</a><a href="#part-3">3 · Problems and solutions</a><a href="#part-4">4 · Labs</a><div class="toc-topic"><span>Spanner external consistency and regional/multi-region choices</span><a href="#topic-01-overview">overview</a> · <a href="#topic-01-technical">discussion</a> · <a href="#topic-01-problem">problem</a> · <a href="#topic-01-lab">lab</a></div><div class="toc-topic"><span>Firestore document/index patterns</span><a href="#topic-02-overview">overview</a> · <a href="#topic-02-technical">discussion</a> · <a href="#topic-02-problem">problem</a> · <a href="#topic-02-lab">lab</a></div><div class="toc-topic"><span>Bigtable wide-column/row-key/replication patterns</span><a href="#topic-03-overview">overview</a> · <a href="#topic-03-technical">discussion</a> · <a href="#topic-03-problem">problem</a> · <a href="#topic-03-lab">lab</a></div><div class="toc-topic"><span>Implement only the selected store, with algorithm depth on Day 145</span><a href="#topic-04-overview">overview</a> · <a href="#topic-04-technical">discussion</a> · <a href="#topic-04-problem">problem</a> · <a href="#topic-04-lab">lab</a></div></aside>""")

# PART 1: TOPICS OF THE DAY
html_parts.append(get_part1_html())

# PART 2: TECHNICAL DISCUSSION
html_parts.append("""<section id="part-2" class="part"><h2>2 · Technical discussion of each topic</h2>""" + get_part2_svg() + get_part2_technical_html() + """</section>""")

# PART 3: REAL-WORLD PROBLEMS
html_parts.append(get_part3_incidents_html())

# PART 4: STEP-BY-STEP LABS
html_parts.append(get_part4_labs_html())

# COMPLETION SECTION
html_parts.append("""<section class="completion"><h2>Daily evidence</h2><p>Assemble your three distributed database schema and key sketches (Cloud Spanner interleaved schema with bit-reversed primary keys, Cloud Firestore sharded counter document model with composite indexing rules, and Cloud Bigtable salted reverse-timestamp row key design), your production consistency and failover evaluation (Spanner TrueTime Paxos quorum vs Firestore delta sync vs Bigtable multi-cluster routing), and your completed enterprise database selection architectural decision record into <code>day-062-distributed-db-adr.md</code>.</p><label class="check"><input type="checkbox" data-progress="read-62"> I read and reviewed the day</label><label class="check"><input type="checkbox" data-progress="artifact-62"> I saved the exit artifact</label></section>""")

# PAGER & FOOTER
html_parts.append("""<nav class="pager" aria-label="Day pagination"><a href="day-061.html">← Day 61<small>Relational databases and transactions</small></a><a href="../index.html">All 180 days<small>Browse the roadmap</small></a><a href="day-063.html">Day 63 →<small>Caching, CDC and database selection</small></a></nav><p class="shortcut">Keyboard: P or [ previous · N or ] next · I index</p></main><footer class="site-footer">GCP Architect · 180-day independent study · Roadmap dated 2026-09-26. Local progress remains in this browser.</footer></body></html>""")

full_html = "".join(html_parts)

# Write to file
ORIG_PAGE.write_text(full_html, encoding="utf-8")
print(f"Successfully wrote {len(full_html)} bytes to {ORIG_PAGE}")

# Run internal audit on the generated HTML
soup = BeautifulSoup(full_html, "html.parser")
ids = [x.get("id") for x in soup.select("[id]")]
duplicates = [x for x in ids if ids.count(x) > 1]
print("Unique IDs count:", len(set(ids)), "Total IDs:", len(ids))
if duplicates:
    print("ERROR: Duplicate IDs found:", set(duplicates))
    sys.exit(1)

required_ids = [
    "main", "day-jump", "part-1", "part-2", "part-3", "part-4",
    "topic-01-overview", "topic-01-technical", "topic-01-problem", "topic-01-lab",
    "topic-02-overview", "topic-02-technical", "topic-02-problem", "topic-02-lab",
    "topic-03-overview", "topic-03-technical", "topic-03-problem", "topic-03-lab",
    "topic-04-overview", "topic-04-technical", "topic-04-problem", "topic-04-lab"
]
missing_ids = [rid for rid in required_ids if rid not in ids]
if missing_ids:
    print("ERROR: Missing required IDs:", missing_ids)
    sys.exit(1)
else:
    print("All required IDs present!")

for phrase in ("Outcome:", "Entry prerequisites:", "Exit artifact", "Daily evidence"):
    if phrase not in soup.get_text(" "):
        print(f"ERROR: Missing phrase: '{phrase}'")
        sys.exit(1)

for code in soup.select("code"):
    value = code.get_text(" ", strip=True)
    if code.parent.name != "pre" and re.match(r"^(?:sudo |git |gcloud |terraform |kubectl |docker |python3? |curl |ssh |cat |printf |mkdir |cd |pwd$|ls(?: |$)|command |ip |dig |nslookup |systemctl |journalctl )", value):
        print(f"ERROR: Runnable command outside a code block: {value[:60]}")
        sys.exit(1)

for pre in soup.select("pre"):
    if not pre.select_one("code"):
        print(f"ERROR: <pre> element missing child <code> element: {pre}")
        sys.exit(1)
    if pre.select_one("kbd"):
        print(f"ERROR: <pre> contains <kbd>: {pre}")
        sys.exit(1)

print("Internal audit completed successfully!")
