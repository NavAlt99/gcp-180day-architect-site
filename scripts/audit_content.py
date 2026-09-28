#!/usr/bin/env python3
"""Inventory generated-content defects across every rendered day and topic.

This is a provenance and template audit, not a claim that a matched template is
technically correct. A human subject-matter review is still required.
"""
from __future__ import annotations

import csv
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

from bs4 import BeautifulSoup

SITE = Path(__file__).resolve().parents[1]
OUTPUT = SITE / "data" / "content-audit.csv"
REPORT = SITE / "CONTENT_AUDIT.md"
DIRECTIVE = re.compile(
    r"\b(optional|when needed|throughout the course|not a new|no new|this day|"
    r"do not|without installing|introduced when|review and remediate|"
    r"maintain them|full course are optional)\b",
    re.I,
)


def content(node) -> str:
    return node.get_text(" ", strip=True) if node else ""


@lru_cache(maxsize=None)
def authored_day_topics(day: int) -> set[int]:
    path = SITE / "content" / f"day-{day:03d}.md"
    if not path.exists():
        return set()
    return {int(value) for value in re.findall(r"^<!-- topic-(\d{2}):overview -->", path.read_text(encoding="utf-8"), re.M)}


rows = []
for page in sorted((SITE / "days").glob("day-*.html")):
    soup = BeautifulSoup(page.read_text(), "html.parser")
    day = int(page.stem.split("-")[1])
    sections = [soup.select(f"#part-{part} .topic-card") for part in range(1, 5)]
    if len({len(section) for section in sections}) != 1:
        raise RuntimeError(f"Four-part mismatch on {page.name}")
    for index, cards in enumerate(zip(*sections), 1):
        overview, technical, problem, lab = cards
        title = content(overview.h3)
        overview_text = content(overview)
        technical_text = content(technical)
        problem_text = content(problem)
        lab_text = content(lab)
        refs = technical.select(".callout a[href]")
        authored_externally = (SITE / "content" / f"day-{day:03d}-topic-{index:02d}-overview.md").exists() or index in authored_day_topics(day)
        authored = authored_externally or day in (1, 11) or (day == 3 and index == 1)
        row = {
            "day": day,
            "topic": index,
            "title": title,
            "page": f"days/{page.name}",
            "heading_looks_like_instruction": bool(DIRECTIVE.search(title)),
            "overview_fallback": "Map the actors, input, control boundary" in overview_text,
            "technical_fallback": "Break the topic into a request or decision path" in technical_text,
            "technical_shared_template": not authored,
            "scenario_shared_template": not authored,
            "scenario_brightloaf_placeholder": "Brightloaf's order API, fulfillment consumer or analytics feed has an unexplained result involving" in problem_text,
            "lab_shared_worksheet": "Draw a three-column table headed" in lab_text,
            "lab_says_no_cloud_needed": "No cloud resources or credentials are required for this exercise." in lab_text,
            "lab_has_commands": bool(lab.select("pre code.language-sh")),
            "lab_has_copyable_blocks": bool(lab.select("pre code")),
            "publisher_deep_link_verified": False,
            "source_urls": " | ".join(a.get("href", "") for a in refs if a.get("href", "").startswith("http")),
        }
        rows.append(row)

with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

counts = Counter()
by_day = {}
for row in rows:
    counts["topics"] += 1
    for field in ("heading_looks_like_instruction", "overview_fallback", "technical_fallback", "technical_shared_template", "scenario_shared_template", "scenario_brightloaf_placeholder", "lab_shared_worksheet", "lab_says_no_cloud_needed", "lab_has_commands", "lab_has_copyable_blocks"):
        counts[field] += bool(row[field])
    by_day.setdefault(row["day"], []).append(row)

lines = [
    "# Content audit — 180-day site",
    "",
    f"This audit reads all 180 rendered day pages and all {counts['topics']} topic sections. It checks template provenance and obvious mismatches, not the technical accuracy of a matched template. The site passes structural navigation checks but **does not pass a topic-level teaching review**.",
    "",
    f"- {counts['technical_shared_template']} / {counts['topics']} technical discussions outside the authored lessons come from shared domain templates; {counts['technical_fallback']} contain the generic 'input, actor, control boundary' fallback.",
    f"- {counts['scenario_shared_template']} / {counts['topics']} scenarios outside the authored lessons come from shared templates; {counts['scenario_brightloaf_placeholder']} use the same inserted-title Brightloaf problem.",
    f"- {counts['lab_shared_worksheet']} / {counts['topics']} labs use the same three-column worksheet; {counts['lab_has_commands']} topic labs include shell command blocks and {counts['lab_has_copyable_blocks']} include any copyable code or fixture block.",
    f"- {counts['lab_says_no_cloud_needed']} labs say no cloud resources or credentials are needed, including cloud-setup and managed-service days.",
    f"- 0 / {counts['topics']} publisher links have a verified topic-level section or video timestamp in the coverage manifest.",
    f"- {counts['heading_looks_like_instruction']} headings look like roadmap instructions or caveats rather than a subject to teach. This is a heuristic lower bound.",
    "",
    "The common cause is the generator: it splits each Study line at semicolons, treats every resulting clause as a topic, matches keywords to broad explanation templates, and falls back to architecture boilerplate when there is no match. Its ordinary-day case and worksheet are then reused with the title inserted. Matching a keyword does **not** establish that the discussion fits the exact topic or stage.",
    "",
    "Examples observed in rendered pages:",
    "",
    "- Day 18 previously paired trial-credit material with generic architecture text and a no-cloud worksheet. Its three topics now have authored definitions, failure cases and Console walkthroughs; the remaining days still require the same treatment.",
    "- Day 42 names Kubernetes architecture and cluster choices, but all three labs are the same worksheet, with no cluster-specific exercise or observable check.",
    "- Day 68's business requirements get generic request-path language instead of a stakeholder discovery method and worked requirement trace.",
    "- The roadmap's Day 175–179 caveat about review versus implementation was previously made into a topic; it is now excluded from the topic list.",
    "- Day 180 uses the request-path fallback for a final review and rest day.",
    "",
    "## Per-day inventory",
    "",
    "| Day | Topics | Fallback discussions | Reused scenarios | Worksheet labs | Command labs | Directive-like headings |",
    "|---:|---:|---:|---:|---:|---:|---:|",
]
for day, day_rows in by_day.items():
    total = len(day_rows)
    counts_for = [sum(bool(row[field]) for row in day_rows) for field in ("technical_fallback", "scenario_shared_template", "lab_shared_worksheet", "lab_has_commands", "heading_looks_like_instruction")]
    lines.append(f"| {day} | {total} | " + " | ".join(str(value) for value in counts_for) + " |")
lines += [
    "",
    "The detailed topic-level flags are in [data/content-audit.csv](data/content-audit.csv). Days 1–12 and 18 are hand-written and materially better aligned, though publisher-section links still need verification across the site. The remaining topics need editorial review against their roadmap Study, Practice and Exit evidence before they can be treated as completed lessons. Rewriting requires topic-specific mechanisms, worked examples, realistic problems, exercises with observable acceptance checks and exact further-study links; adding more generic paragraphs will not repair the mismatch.",
    "",
]
REPORT.write_text("\n".join(lines), encoding="utf-8")
print(f"Audited {len(by_day)} pages and {len(rows)} topics")
for key, value in sorted(counts.items()):
    print(f"{key}: {value}")
print(f"Wrote {OUTPUT.relative_to(SITE)} and {REPORT.name}")
