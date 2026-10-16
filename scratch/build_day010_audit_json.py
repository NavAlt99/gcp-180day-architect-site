import json
import hashlib
import re
import urllib.parse
from bs4 import BeautifulSoup
from PIL import ImageFont

spec_path = "scratch/day_data_010.py"
spec_bytes = open(spec_path, "rb").read()
spec_sha256 = hashlib.sha256(spec_bytes).hexdigest()

html_path = "days/day-010.html"
html_text = open(html_path).read()
soup = BeautifulSoup(html_text, "html.parser")

font_cache = {}
def get_font(size, bold=False):
    key = (size, bold)
    if key not in font_cache:
        font_cache[key] = ImageFont.truetype('DejaVuSans.ttf', size)
    return font_cache[key]

def get_text_width(text, size, bold=False):
    f = get_font(size, bold)
    bbox = f.getbbox(text)
    w = bbox[2] - bbox[0]
    if bold:
        w *= 1.07
    return w

def get_matrix_transform(el):
    tx, ty = 0.0, 0.0
    curr = el
    while curr and curr.name != 'svg':
        trans = curr.get('transform', '')
        if 'translate' in trans:
            m = re.search(r'translate\(\s*([0-9.-]+)[,\s]+([0-9.-]+)\s*\)', trans)
            if m:
                tx += float(m.group(1))
                ty += float(m.group(2))
        curr = curr.parent
    return tx, ty

# Extract all unlinked strong.keyword
unlinked_keywords = []
for t_idx in [1, 2, 3]:
    tech = soup.find(id=f'topic-0{t_idx}-technical')
    subtopic_headers = tech.find_all('h4', id=re.compile(f'topic-0{t_idx}-subtopic-'))
    for s_idx, h4 in enumerate(subtopic_headers):
        sub_id = h4.get('id')
        curr = h4.next_sibling
        seen_terms = set()
        while curr:
            if getattr(curr, 'name', None) == 'h4':
                break
            if hasattr(curr, 'find_all'):
                kws = curr.find_all('strong', class_='keyword')
                for kw in kws:
                    txt = kw.get_text().strip()
                    if txt not in seen_terms:
                        seen_terms.add(txt)
                        if not kw.find('a'):
                            term_q = urllib.parse.quote_plus(txt)
                            old_str = str(kw)
                            new_str = f'<strong class="keyword"><a href="http://www.google.com/search?q={term_q}" rel="noopener" target="_blank">{txt}</a></strong>'
                            unlinked_keywords.append({
                                'topic': f'topic-0{t_idx}',
                                'subtopic': sub_id,
                                'term': txt,
                                'old_str': old_str,
                                'new_str': new_str
                            })
            curr = curr.next_sibling

all_key_terms = sorted(list(set(x['term'] for x in unlinked_keywords)))

findings = [
    {
        "id": "F1",
        "kind": "defect",
        "area": "exercises",
        "type": "fix-lab-runner",
        "location": "scratch/day_data_010.py:DATA['topics'][0]['lab']['steps'][7]",
        "rule": "PAGE_AUTHORING_CONTRACT.md & scripts/run_labs.py: Stage 8 must execute declared commands without runner timeout and ensure all declared artifacts exist.",
        "status": "open",
        "old_str": "DATA['topics'][0]['lab']['steps'][7] contains appended _EXTRA_IMAGE_LAB causing 60s timeout under run_labs.py",
        "new_str": "Decouple _EXTRA_IMAGE_LAB from execution chain or adjust runner harness timeout/prerequisites"
    },
    {
        "id": "F2",
        "kind": "defect",
        "area": "diagrams",
        "type": "diagram-collision",
        "location": "scratch/day_data_010.py:SVG-3 (day10-reconcile-title)",
        "rule": "PAGE_AUTHORING_CONTRACT.md & DIAGRAMS=allow: No text element extends outside the viewBox. Detected via Pillow ImageFont with DejaVuSans.",
        "status": "open",
        "old_str": "viewbox=\"0 0 940 300\" with right-edge text ('Pulls Image & Starts Pod', 'Executes Health Probes', 'Reports Status to API', 'Observed Actual State') reaching x=962",
        "new_str": "Widen viewBox to 980 or wrap node text to prevent right boundary overflow"
    },
    {
        "id": "F3",
        "kind": "defect",
        "area": "diagrams",
        "type": "diagram-collision",
        "location": "scratch/day_data_010.py:SVG-4 (day10-objects-title)",
        "rule": "PAGE_AUTHORING_CONTRACT.md & DIAGRAMS=allow: No text element extends outside the viewBox. Detected via Pillow ImageFont with DejaVuSans.",
        "status": "open",
        "old_str": "viewbox=\"0 0 940 320\" with text ('ConfigMap: app-config', 'Secret: db-credentials', 'Encrypted auth tokens') reaching x=946",
        "new_str": "Widen viewBox or wrap labels inside right cards"
    },
    {
        "id": "F4",
        "kind": "defect",
        "area": "diagrams",
        "type": "diagram-collision",
        "location": "scratch/day_data_010.py:SVG-5 (day10-volume-incident-title)",
        "rule": "PAGE_AUTHORING_CONTRACT.md & DIAGRAMS=allow: Text intersects icon (4px margin) and extends outside viewBox. Detected via Pillow ImageFont with DejaVuSans.",
        "status": "open",
        "old_str": "Text '[FAILED: Ephemeral Layer]' collides with icon at (503,38) and '[CORRECTED: Persistent Volume]' collides with icon at (503,193); text extends to x=990 vs vb=940",
        "new_str": "Reposition header text above or left of icon with >=4px margin, widen viewBox to 1020"
    },
    {
        "id": "F5",
        "kind": "defect",
        "area": "diagrams",
        "type": "diagram-collision",
        "location": "scratch/day_data_010.py:SVG-7 (day10-sched-incident-title)",
        "rule": "PAGE_AUTHORING_CONTRACT.md & DIAGRAMS=allow: Text extends outside viewBox. Detected via Pillow ImageFont with DejaVuSans.",
        "status": "open",
        "old_str": "Text '5/5 Replicas Running' and 'Zero dropped checkouts' extend to x=995 vs vb=940",
        "new_str": "Widen viewBox to 1020 or wrap outcome text"
    },
    {
        "id": "F6",
        "kind": "defect",
        "area": "diagrams",
        "type": "diagram-collision",
        "location": "scratch/day_data_010.py:SVG-9 (day10-selector-incident-title)",
        "rule": "PAGE_AUTHORING_CONTRACT.md & DIAGRAMS=allow: Text collides with icon and extends outside viewBox. Detected via Pillow ImageFont with DejaVuSans.",
        "status": "open",
        "old_str": "Text '[CORRECTED: Matched Label Selector]' collides with icon at (503,193); text 'Order processed cleanly' extends to x=995 vs vb=940",
        "new_str": "Reposition header text and expand viewBox"
    },
    {
        "id": "F7",
        "kind": "defect",
        "area": "scenarios",
        "type": "scenario-evidence-limit",
        "location": "scratch/day_data_010.py:topics[*]['scenario']",
        "rule": "PAGE_AUTHORING_CONTRACT.md: Each incident case must state an 'Evidence limit:' and distinguish supplied facts from local/production observations.",
        "status": "open",
        "old_str": "Scenarios omit explicit 'Evidence limit:' and log distinction labels",
        "new_str": "Append explicit 'Evidence limit:' paragraph and label illustrative logs in each scenario"
    },
    {
        "id": "F8",
        "kind": "enhancement",
        "area": "content",
        "type": "add-links",
        "location": "scratch/day_data_010.py:topics[*]['technical']",
        "rule": "Standing Improvement S3: Wrap first occurrence per subtopic of each key term in Google search link <a href=\"http://www.google.com/search?q=TERM\" rel=\"noopener\" target=\"_blank\">TERM</a>.",
        "status": "open",
        "anchor_str": "All 72 unlinked strong.keyword occurrences across 15 subtopics",
        "drafted_text": json.dumps(unlinked_keywords[:5], indent=2) + f" ... and {len(unlinked_keywords)-5} more terms",
        "study_clause": "Docker: images, layers, Dockerfile, registries, mounts, inodes, volumes, POSIX filesystem sync/fsync semantics; Container orchestration; Kubernetes core objects",
        "learner_time_delta": "+5m"
    },
    {
        "id": "F9",
        "kind": "enhancement",
        "area": "content",
        "type": "set-width",
        "location": "scratch/day_data_010.py:page_level_styling",
        "rule": "Standing Improvement S4: The technical discussion uses the full container width on the Day 10 page only via page-level styling.",
        "status": "open",
        "anchor_str": ".topic-card.technical styling",
        "drafted_text": "Ensure .topic-card.technical uses full 100% available container width without artificial line-length constraints.",
        "study_clause": "Day 10 full layout presentation",
        "learner_time_delta": "+0m"
    }
]

audit_data = {
    "day": 10,
    "spec_path": spec_path,
    "spec_sha256": spec_sha256,
    "summary": {
        "status": "audit-complete",
        "checks_run": {
            "validate_spec": "PASS (0 errors, 21 warnings)",
            "validate": "PASS (0 local link/structure errors)",
            "check_study_links": "FAIL (14 PASS, 1 UNVERIFIED due to man7.org timeout)",
            "run_labs": "FAIL (Topic 1 exit=-9 due to 60s timeout in appended multistage lab Stage 8)"
        },
        "built_page_checks": {
            "linked_subtopics": "PASS (all 3 overview cards have 'Linked subtopics:' pointing to existing anchors)",
            "keyword_links": f"NEEDS_ENHANCEMENT ({len(unlinked_keywords)} first-occurrence key terms unlinked in technical discussions)",
            "diagram_collisions": f"FAIL ({len(findings[1:6])} collision/viewBox overflow defect classes identified across SVGs)"
        },
        "improvements_coverage": {
            "S1 Linked subtopics": "Covered (already satisfied on built page)",
            "S2 Bullets": "Covered (already satisfied in spec and built page)",
            "S3 Discovery links": "Covered by finding F8 (72 unlinked keyword instances identified)",
            "S4 Width": "Covered by finding F9 (page-level full width confirmation)"
        }
    },
    "key_terms": all_key_terms,
    "unlinked_occurrences_count": len(unlinked_keywords),
    "unlinked_occurrences": unlinked_keywords,
    "findings": findings
}

import os
os.makedirs("scratch/audits", exist_ok=True)
with open("scratch/audits/day-010-audit.json", "w") as f:
    json.dump(audit_data, f, indent=2)

print("Audit ledger successfully written to scratch/audits/day-010-audit.json")
