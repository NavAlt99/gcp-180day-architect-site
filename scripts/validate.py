#!/usr/bin/env python3
"""Audit generated page, topic, and local-link coverage."""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

SITE = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--day', type=int, choices=range(1, 181), help='Also enforce authoring/render markup guards on the updated day')
args = parser.parse_args()
pages = sorted(SITE.glob("*.html")) + sorted((SITE / "days").glob("*.html"))
errors = []
documents = {}
for page in pages:
    soup = BeautifulSoup(page.read_text(), "html.parser")
    ids = [x.get("id") for x in soup.select("[id]")]
    if len(ids) != len(set(ids)):
        errors.append(f"{page.name}: duplicate IDs")
    documents[page.resolve()] = (soup, set(ids))

day_pages = sorted((SITE / "days").glob("day-*.html"))
if len(day_pages) != 180:
    errors.append(f"Expected 180 day pages, got {len(day_pages)}")

with (SITE / "data" / "coverage.csv").open(newline="") as stream:
    coverage = list(csv.DictReader(stream))
mapped = set()
for row in coverage:
    n = int(row["day"])
    page = SITE / "days" / f"day-{n:03d}.html"
    soup, ids = documents[page.resolve()]
    for field in ("overview_anchor", "technical_anchor", "problem_anchor", "lab_anchor"):
        if row[field] not in ids:
            errors.append(f"Day {n}: missing {field} {row[field]}")
    mapped.update(int(x) for x in row["source_topic_ids"].split(",") if x)
if mapped != set(range(1, 84)):
    errors.append(f"Source topic IDs missing: {sorted(set(range(1,84))-mapped)}")

for n, page in enumerate(day_pages, 1):
    soup, ids = documents[page.resolve()]
    if page.name != f"day-{n:03d}.html":
        errors.append(f"Misnumbered page {page.name}")
    for i in range(1, 5):
        if f"part-{i}" not in ids:
            errors.append(f"{page.name}: missing part {i}")
    for phrase in ("Outcome:", "Entry prerequisites:", "Exit artifact", "Daily evidence"):
        if phrase not in soup.get_text(" "):
            errors.append(f"{page.name}: missing {phrase}")
    if n > 1 and not soup.select_one(f'a[href="day-{n-1:03d}.html"]'):
        errors.append(f"{page.name}: missing previous")
    if n < 180 and not soup.select_one(f'a[href="day-{n+1:03d}.html"]'):
        errors.append(f"{page.name}: missing next")
    if len(soup.select("#day-jump option[value^='day-']")) != 180:
        errors.append(f"{page.name}: day jump incomplete")
    for code in soup.select("code"):
        value = code.get_text(" ", strip=True)
        if code.parent.name != "pre" and re.match(r"^(?:sudo |git |gcloud |terraform |kubectl |docker |python3? |curl |ssh |cat |printf |mkdir |cd |pwd$|ls(?: |$)|command |ip |dig |nslookup |systemctl |journalctl )", value):
            errors.append(f"{page.name}: runnable command outside a code block: {value[:60]}")
    for pre in soup.select("pre"):
        if not pre.select_one("code"):
            errors.append(f"{page.name}: <pre> element missing child <code> element (breaks copy button)")
        if pre.select_one("kbd"):
            errors.append(f"{page.name}: <pre> element contains <kbd> instead of <code>")

if args.day:
    target = SITE / 'days' / f'day-{args.day:03d}.html'
    soup, ids = documents[target.resolve()]
    if not soup.select_one('strong.keyword') or not soup.select_one('strong.side-heading'):
        errors.append(f'{target.name}: missing keyword highlights or blue bold side-heading markup')
    for term in soup.select('.keyword'):
        if term.name != 'strong' or term.find_parent(['pre', 'code']):
            errors.append(f'{target.name}: highlight must be strong.keyword in prose, not code')
    for svg in soup.select('figure svg'):
        refs = svg.get('aria-labelledby', '').split()
        if svg.get('role') != 'img' or not (svg.get('viewbox') or svg.get('viewBox')) or len(refs) < 2 or any(x not in ids for x in refs):
            errors.append(f'{target.name}: SVG requires viewBox, role=img and existing title/description IDs')
        figure = svg.find_parent('figure')
        if not figure.select_one('figcaption'):
            errors.append(f'{target.name}: diagram missing evidence caption')
        for image in svg.select('image'):
            href = image.get('href') or image.get('xlink:href', '')
            parsed = urlsplit(href)
            if not href or parsed.scheme or parsed.netloc or not (target.parent / unquote(parsed.path)).is_file():
                errors.append(f'{target.name}: SVG icon must be an existing local asset: {href}')

for path, (soup, ids) in documents.items():
    for link in soup.select("a[href], link[href], script[src]"):
        target = link.get("href") or link.get("src")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        if destination not in documents and not destination.exists():
            errors.append(f"{path.name}: missing local target {target}")
        elif parsed.fragment and destination in documents and unquote(parsed.fragment) not in documents[destination][1]:
            errors.append(f"{path.name}: missing fragment {target}")

print(f"Pages: {len(day_pages)} day + {len(pages)-len(day_pages)} support")
print(f"Topic sections: {len(coverage)}; mapped source IDs: {len(mapped)}")
print("Gate days: 17, 35, 67, 82, 118, 174; capstones: 175–179")
print(f"Local link/structure errors: {len(errors)}")
for error in errors[:30]:
    print("ERROR", error)
if errors:
    raise SystemExit(1)
