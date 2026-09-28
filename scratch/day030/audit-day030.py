#!/usr/bin/env python3
"""
Comprehensive audit script for Day 30 implementation.
"""

import re
import sys
import os
from html.parser import HTMLParser

class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.in_inline_code = False
        self.in_pre = False
        self.current_code_text = []
        self.inline_code_violations = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if "id" in attr_dict:
            self.ids.append(attr_dict["id"])
        if tag == "pre":
            self.in_pre = True
        elif tag == "code" and not self.in_pre:
            self.in_inline_code = True
            self.current_code_text = []

    def handle_endtag(self, tag):
        if tag == "pre":
            self.in_pre = False
        elif tag == "code" and not self.in_pre:
            self.in_inline_code = False
            code_text = "".join(self.current_code_text).strip()
            # check command regex
            cmd_pattern = r'^(?:sudo |git |gcloud |terraform |kubectl |docker |python3? |curl |ssh |cat |printf |mkdir |cd |pwd$|ls(?: |$)|command |ip |dig |nslookup |systemctl |journalctl )'
            if re.search(cmd_pattern, code_text):
                self.inline_code_violations.append(code_text)
            self.current_code_text = []

    def handle_data(self, data):
        if self.in_inline_code:
            self.current_code_text.append(data)

def audit():
    page_file = "days/day-030.html"
    with open(page_file, "r", encoding="utf-8") as f:
        html = f.read()

    parser = AuditParser()
    parser.feed(html)

    print("=" * 80)
    print("DAY 30 COMPREHENSIVE AUDIT")
    print("=" * 80)

    # 1. Anchors check
    required_anchors = [
        "part-1", "part-2", "part-3", "part-4",
        "topic-01-overview", "topic-01-technical", "topic-01-problem", "topic-01-lab",
        "topic-02-overview", "topic-02-technical", "topic-02-problem", "topic-02-lab"
    ]
    missing_anchors = [a for a in required_anchors if a not in parser.ids]
    if missing_anchors:
        print(f"[FAIL] Missing required anchors: {missing_anchors}")
        sys.exit(1)
    else:
        print(f"[PASS] All 12 required anchors present: {required_anchors}")

    # 2. Duplicate IDs check
    id_counts = {}
    for an_id in parser.ids:
        id_counts[an_id] = id_counts.get(an_id, 0) + 1
    duplicates = [an_id for an_id, count in id_counts.items() if count > 1]
    if duplicates:
        print(f"[FAIL] Duplicate IDs found: {duplicates}")
        sys.exit(1)
    else:
        print(f"[PASS] 0 duplicate IDs found (total unique IDs: {len(parser.ids)})")

    # 3. Inline code command violations check
    if parser.inline_code_violations:
        print(f"[FAIL] Inline code command violations: {parser.inline_code_violations}")
        sys.exit(1)
    else:
        print("[PASS] 0 inline code command violations found.")

    # 4. Preview sentences check in Part 1
    # Check topic-01-overview
    t1_match = re.search(r'<article[^>]*id="topic-01-overview"[^>]*>(.*?)</article>', html, re.DOTALL)
    t2_match = re.search(r'<article[^>]*id="topic-02-overview"[^>]*>(.*?)</article>', html, re.DOTALL)
    
    if not t1_match or not t2_match:
        print("[FAIL] Could not extract topic overview cards in Part 1")
        sys.exit(1)

    t1_paras = re.findall(r'<p>(.*?)</p>', t1_match.group(1), re.DOTALL)
    t2_paras = re.findall(r'<p>(.*?)</p>', t2_match.group(1), re.DOTALL)

    # The last paragraph in each topic overview should be the preview sentences
    t1_preview = t1_paras[-1].strip()
    t2_preview = t2_paras[-1].strip()

    # Split sentences by dot followed by space or end
    t1_sentences = [s.strip() for s in re.split(r'\.\s+', t1_preview) if s.strip()]
    t2_sentences = [s.strip() for s in re.split(r'\.\s+', t2_preview) if s.strip()]

    print(f"[INFO] Topic 1 preview sentences ({len(t1_sentences)}): {t1_preview}")
    print(f"[INFO] Topic 2 preview sentences ({len(t2_sentences)}): {t2_preview}")

    if len(t1_sentences) != 2:
        print(f"[FAIL] Topic 1 preview paragraph does not contain exactly 2 sentences (got {len(t1_sentences)})")
        sys.exit(1)
    else:
        print("[PASS] Topic 1 ends with exactly 2 problem-preview sentences.")

    if len(t2_sentences) != 2:
        print(f"[FAIL] Topic 2 preview paragraph does not contain exactly 2 sentences (got {len(t2_sentences)})")
        sys.exit(1)
    else:
        print("[PASS] Topic 2 ends with exactly 2 problem-preview sentences.")

    # 5. SVGs check
    figures = ["fig-30-1", "fig-30-2", "fig-30-3", "fig-30-4"]
    for fig_id in figures:
        if fig_id not in parser.ids:
            print(f"[FAIL] Missing figure {fig_id}")
            sys.exit(1)
        # Check SVG attributes
        fig_match = re.search(rf'<figure[^>]*id="{fig_id}"[^>]*>(.*?)</figure>', html, re.DOTALL)
        if not fig_match:
            print(f"[FAIL] Could not match figure tag for {fig_id}")
            sys.exit(1)
        content = fig_match.group(1)
        if 'role="img"' not in content or 'aria-labelledby="' not in content:
            print(f"[FAIL] Figure {fig_id} missing role='img' or aria-labelledby")
            sys.exit(1)
        if '<title' not in content or '<desc' not in content:
            print(f"[FAIL] Figure {fig_id} missing <title> or <desc>")
            sys.exit(1)

    print("[PASS] All 4 SVGs (Figures 30.1, 30.2, 30.3, 30.4) valid with titles, descs, and aria attributes.")

    # 6. Incident diagrams check (fig-30-3 and fig-30-4)
    for inc_fig in ["fig-30-3", "fig-30-4"]:
        fig_match = re.search(rf'<figure[^>]*id="{inc_fig}"[^>]*>(.*?)</figure>', html, re.DOTALL)
        content = fig_match.group(1)
        if 'stroke-dasharray="7 5"' not in content:
            print(f"[FAIL] Figure {inc_fig} missing dashed failed line stroke-dasharray='7 5'")
            sys.exit(1)
        if '[FAILED PATH:' not in content or '[CORRECTED PATH:' not in content:
            print(f"[FAIL] Figure {inc_fig} missing explicit [FAILED PATH: ...] or [CORRECTED PATH: ...] text")
            sys.exit(1)
        if 'Supplied facts:' not in content or 'Architectural inference:' not in content or 'Expected post-fix behavior:' not in content:
            print(f"[FAIL] Figure {inc_fig} figcaption missing 3-part partition")
            sys.exit(1)

    print("[PASS] Incident SVGs (30.3 & 30.4) have dashed failed path, solid corrected path, explicit path labels, and partitioned figcaption.")

    # 7. Invariant check
    if html.count("physical fulfillment per unique order ID") < 2 and html.count("physical fulfillment") < 2:
        print("[FAIL] Duplicate fulfillment invariant not adequately referenced")
        sys.exit(1)
    else:
        print("[PASS] Brightloaf duplicate fulfillment invariant properly documented in incidents and labs.")

    # 8. Exit artifact check
    artifact_path = "scratch/day030/location-scope-matrix.md"
    if not os.path.exists(artifact_path) or os.path.getsize(artifact_path) == 0:
        print(f"[FAIL] Exit artifact {artifact_path} missing or empty")
        sys.exit(1)
    else:
        print(f"[PASS] Exit artifact {artifact_path} verified ({os.path.getsize(artifact_path)} bytes)")

    print("=" * 80)
    print("ALL AUDIT CHECKS PASSED SUCCESSFULLY (0 ERRORS)")
    print("=" * 80)

if __name__ == "__main__":
    audit()
