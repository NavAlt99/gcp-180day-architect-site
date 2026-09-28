#!/usr/bin/env python3
"""author_engine.py — Deterministic compiler for 180-day GCP Architect curriculum pages.

Combines high-density architectural content (pure Python data specification)
with the site shell and generates accessible, responsive SVGs.
Eliminates LLM token waste on HTML/SVG boilerplate and prevents model drift.
"""

from __future__ import annotations

import argparse
from html import escape
import importlib.util
from pathlib import Path
import re
import subprocess
import sys

from bs4 import BeautifulSoup
import markdown

ROOT = Path(__file__).resolve().parents[1]
SITE_CONTENT = ROOT / "content"
SITE_DAYS = ROOT / "days"
SCRIPTS = ROOT / "scripts"


def wrap_svg(text: str, limit: int = 22, max_lines: int = 2) -> list[str]:
    """Break text into wrapped lines for SVG boxes without overflowing."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > limit:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines[:max_lines]


def render_incident_svg(day: int, index: int, topic: dict) -> str:
    """Generate dual-lane incident SVG diagram: Failed Path vs Corrected Path."""
    scenario = topic.get("scenario", {})
    diagram = scenario.get("diagram", ("Trigger event", "Root cause", "Impact", "Corrected control", "Expected outcome"))
    event, cause, impact, control, outcome = diagram

    uid = f"d{day:03d}-case-{index}"
    labels = [
        (25, 61, "Initiating event", event, "#94a3b8"),
        (280, 61, "ROOT CAUSE", cause, "#fb7185"),
        (535, 61, "Affected outcome", impact, "#fb7185"),
        (25, 221, "Same trigger", event, "#94a3b8"),
        (280, 221, "CORRECTED CONTROL", control, "#4ade80"),
        (535, 221, "Expected outcome", outcome, "#4ade80"),
    ]

    box_html = []
    for x, y, label, detail, color in labels:
        lines = wrap_svg(detail, limit=22, max_lines=2)
        y_offset = 57 if len(lines) == 1 else 49
        detail_html = "".join(
            f'<text x="{x + 95}" y="{y + y_offset + j * 17}" text-anchor="middle" style="font:12px ui-monospace,monospace;fill:#cbd5e1">{escape(line)}</text>'
            for j, line in enumerate(lines)
        )
        box_html.append(
            f'<g>'
            f'<rect x="{x}" y="{y}" width="190" height="88" rx="12" fill="#121526" stroke="{color}" stroke-width="2"/>'
            f'<text x="{x + 95}" y="{y + 27}" text-anchor="middle" style="font:700 14px ui-monospace,monospace;fill:#e2e8f0">{escape(label)}</text>'
            f'{detail_html}'
            f'</g>'
        )

    boxes = "".join(box_html)
    title = f"{topic['title']}: synthetic failed and corrected paths"
    desc = (
        "The dashed upper path runs from the initiating event through the labeled root cause to customer impact. "
        "The solid lower path shows the proposed control, expected outcome, and verification boundary. "
        "This is a synthetic case, not a measured incident."
    )

    facts = scenario.get("facts", "Synthetic case scenario.")
    inference = scenario.get("inference", "Architectural inference based on constraints.")
    expected = scenario.get("expected", "Expected post-fix behavior once verified.")

    return f'''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg viewBox="0 0 960 365" width="960" height="365" role="img" aria-labelledby="{uid}-title {uid}-desc" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block">
<title id="{uid}-title">{escape(title)}</title>
<desc id="{uid}-desc">{escape(desc)}</desc>
<defs>
  <marker id="{uid}-rose-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0 L10 4 L0 8 Z" fill="#fb7185"/></marker>
  <marker id="{uid}-green-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0 L10 4 L0 8 Z" fill="#4ade80"/></marker>
</defs>
<text x="25" y="35" style="font:700 17px ui-monospace,monospace;fill:#fb7185">FAILED PATH · dashed</text>
<text x="25" y="195" style="font:700 17px ui-monospace,monospace;fill:#4ade80">CORRECTED PATH · solid</text>
<path d="M215 105 H275 M470 105 H530 M725 105 H785" stroke="#fb7185" stroke-width="3" stroke-dasharray="9 7" fill="none" marker-end="url(#{uid}-rose-arrow)"/>
<path d="M215 265 H275 M470 265 H530 M725 265 H785" stroke="#4ade80" stroke-width="3" fill="none" marker-end="url(#{uid}-green-arrow)"/>
{boxes}
<line x1="800" y1="50" x2="800" y2="320" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5 5"/>
<text x="820" y="92" transform="rotate(90 820 92)" style="font:700 13px ui-monospace,monospace;fill:#cbd5e1">VERIFICATION BOUNDARY</text>
<text x="25" y="350" style="font:13px ui-monospace,monospace;fill:#94a3b8">Synthetic case; the lower lane is a proposed control pending workload-specific verification.</text>
</svg></div>
<figcaption><strong>Supplied facts:</strong> {escape(facts)}<br><strong>Architectural inference:</strong> {escape(inference)}<br><strong>Expected post-fix behavior:</strong> {escape(expected)}</figcaption>
</figure>'''


def render_architecture_svg(day: int, arch_diagram: dict) -> str:
    """Generate responsive architecture workflow SVG diagram."""
    uid = f"d{day:03d}-arch-path"
    title = arch_diagram.get("title", f"Day {day} Architecture Flow")
    desc = arch_diagram.get("desc", "Architecture workflow from requirements to verification.")
    nodes = arch_diagram.get("nodes", [
        ("Inputs", "Scope & Requirements"),
        ("Architecture", "Design Decisions"),
        ("Trade-offs", "Analysis & Matrix"),
        ("Verification", "Observable Evidence"),
    ])

    # Position 4 boxes evenly across 960px width
    step = 240
    start_x = 24
    box_width = 190
    box_height = 106
    y = 88

    boxes_html = []
    arrows_html = []

    for i, (node_title, node_sub) in enumerate(nodes):
        x = start_x + (i * step)
        sub_lines = wrap_svg(node_sub, limit=24, max_lines=2)
        sub_html = "".join(
            f'<text x="{x + 95}" y="{155 + j * 16}" text-anchor="middle" style="font:12px ui-monospace,monospace;fill:#94a3b8">{escape(line)}</text>'
            for j, line in enumerate(sub_lines)
        )
        boxes_html.append(
            f'<g>'
            f'<rect x="{x}" y="{y}" width="{box_width}" height="{box_height}" rx="14" fill="#121526" stroke="#334155" stroke-width="2"/>'
            f'<text x="{x + 95}" y="128" text-anchor="middle" style="font:700 15px ui-monospace,monospace;fill:#e2e8f0">{escape(node_title)}</text>'
            f'{sub_html}'
            f'</g>'
        )
        if i < len(nodes) - 1:
            arrow_start = x + box_width
            arrow_end = arrow_start + (step - box_width) - 7
            arrows_html.append(f'<path d="M{arrow_start} 141 H{arrow_end}" stroke="#38bdf8" stroke-width="3" fill="none" marker-end="url(#{uid}-arrow)"/>')

    caption = arch_diagram.get("caption", "Architecture decision flow and boundary verification.")

    return f'''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg viewBox="0 0 960 280" width="960" height="280" role="img" aria-labelledby="{uid}-title {uid}-desc" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block">
<title id="{uid}-title">{escape(title)}</title>
<desc id="{uid}-desc">{escape(desc)}</desc>
<defs>
  <marker id="{uid}-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0 L10 4 L0 8 Z" fill="#38bdf8"/></marker>
</defs>
{"".join(boxes_html)}
{"".join(arrows_html)}
<text x="24" y="245" style="font:13px ui-monospace,monospace;fill:#94a3b8">Decisions must cite observable constraints and trade-offs rather than unmeasured assumptions.</text>
</svg></div>
<figcaption>{escape(caption)}</figcaption>
</figure>'''


def render_code_blocks(text: str) -> str:
    """Ensure all markdown code blocks and inline code follow validate.py rules."""
    return markdown.markdown(text, extensions=["tables", "fenced_code"])


def compile_day_page(day_num: int, data: dict) -> None:
    """Compile the day page override from data specification."""
    override_file = SITE_CONTENT / f"day-{day_num:03d}-page.html"
    source_day_file = SITE_DAYS / f"day-{day_num:03d}.html"

    if not override_file.exists():
        if not source_day_file.exists():
            raise FileNotFoundError(f"Source file {source_day_file} missing.")
        override_file.write_text(source_day_file.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Initialized Day {day_num} override from {source_day_file.name}")

    soup = BeautifulSoup(override_file.read_text(encoding="utf-8"), "html.parser")

    def put_section(section_id: str, inner_markup: str) -> None:
        section = soup.select_one(f"#{section_id}")
        if not section:
            raise ValueError(f"Section #{section_id} not found in page shell.")
        heading = section.find("h2", recursive=False)
        for child in list(section.contents):
            if child is not heading:
                child.extract()
        section.append(BeautifulSoup(inner_markup, "html.parser"))

    topics = data.get("topics", [])

    # ─── PART 1: Topics of the Day ──────────────────────────────────────
    part1_intro = data.get("part1_intro", f"Day {day_num} examines core architecture principles and trade-offs.")
    exit_summary = data.get("exit_summary", "Completed exercises and verified architecture decisions.")

    p1_html = [
        f'<p class="intro">{escape(part1_intro)}</p>',
        f'<p class="callout"><strong>Exit evidence:</strong> {escape(exit_summary)}</p>'
    ]
    for i, t in enumerate(topics, 1):
        key = t["key"]
        p1_html.append(
            f'<article id="{key}-overview" class="topic-card overview">'
            f'<h3>{i}. {escape(t["title"])}</h3>'
            f'<p>{escape(t["overview"])}</p>'
            f'<p class="problem-preview"><strong>Problem preview:</strong> {escape(t["preview"])}</p>'
            f'<p><a href="#{key}-technical">Technical discussion →</a> <a href="#{key}-problem">Real-world problem →</a> <a href="#{key}-lab">Step-by-step lab →</a></p>'
            f'</article>'
        )
    put_section("part-1", "".join(p1_html))

    # ─── PART 2: Technical Discussion ───────────────────────────────────
    part2_intro = data.get("part2_intro", "Trace technical control and data boundaries, observable signals, and trade-offs.")
    arch_diagram = data.get("arch_diagram", {})
    arch_svg_html = render_architecture_svg(day_num, arch_diagram) if arch_diagram else ""
    table_html = data.get("arch_table_html", "")

    p2_html = [
        f'<p class="intro">{escape(part2_intro)}</p>',
        table_html,
        arch_svg_html
    ]
    for i, t in enumerate(topics, 1):
        key = t["key"]
        questions = "".join(f"<li>{escape(q)}</li>" for q in t.get("questions", []))
        q_section = f'<h4>Architectural evaluation questions</h4><ul>{questions}</ul>' if questions else ""
        ref_link = t.get("reference", "")
        ref_label = t.get("reference_label", "Google Cloud Documentation")
        ref_html = f'<p><strong>Further study:</strong> <a href="{escape(ref_link)}" target="_blank" rel="noopener">{escape(ref_label)}</a>.</p>' if ref_link else ""
        tech_body = render_code_blocks(t.get("technical", ""))

        p2_html.append(
            f'<article id="{key}-technical" class="topic-card technical">'
            f'<h3>{i}. {escape(t["title"])}: technical mechanics</h3>'
            f'{tech_body}'
            f'{q_section}'
            f'{ref_html}'
            f'</article>'
        )
    put_section("part-2", "".join(p2_html))

    # ─── PART 3: Problem and Solution ───────────────────────────────────
    part3_intro = data.get("part3_intro", "Illustrative real-world scenarios and diagnostic failure investigations.")
    p3_html = [f'<p class="intro">{escape(part3_intro)}</p>']

    for i, t in enumerate(topics, 1):
        key = t["key"]
        scenario = t.get("scenario", {})
        diag_steps = "".join(f"<li>{escape(s)}</li>" for s in scenario.get("diagnostic_steps", []))
        diag_html = f'<p><strong>Diagnostic sequence:</strong></p><ol>{diag_steps}</ol>' if diag_steps else ""

        fix_steps = "".join(f"<li>{escape(s)}</li>" for s in scenario.get("remediation_steps", []))
        if fix_steps:
            fix_html = f'<p><strong>Defensible remediation:</strong></p><ol>{fix_steps}</ol>'
        else:
            fix_html = f'<p><strong>Defensible remediation:</strong> {escape(scenario.get("fix", ""))}</p>'

        inc_svg = render_incident_svg(day_num, i, t)

        scenario_text = scenario.get("scenario", scenario.get("symptom", ""))
        impact_text = scenario.get("impact", "")
        impact_p = f'<p><strong>Failure symptoms and impact:</strong> {escape(impact_text)}</p>' if impact_text else ""
        constraints_text = scenario.get("constraints", "")
        constraints_p = f'<p><strong>Constraints:</strong> {escape(constraints_text)}</p>' if constraints_text else ""

        p3_html.append(
            f'<article id="{key}-problem" class="topic-card problem">'
            f'<h3>{i}. {escape(t["title"])} · field case</h3>'
            f'<p><strong>Enterprise scenario:</strong> {escape(scenario_text)}</p>'
            f'{impact_p}'
            f'{constraints_p}'
            f'{diag_html}'
            f'<p><strong>Root cause:</strong> {escape(scenario.get("root", ""))}</p>'
            f'{fix_html}'
            f'<p><strong>Verification:</strong> {escape(scenario.get("verify", ""))}</p>'
            f'<p><strong>Residual risk:</strong> {escape(scenario.get("residual", ""))}</p>'
            f'{inc_svg}'
            f'</article>'
        )
    put_section("part-3", "".join(p3_html))

    # ─── PART 4: Step-by-Step Labs ──────────────────────────────────────
    part4_intro = data.get("part4_intro", "Hands-on exercises and tabletop verification procedures.")
    p4_html = [f'<p class="intro">{escape(part4_intro)}</p>']

    for i, t in enumerate(topics, 1):
        key = t["key"]
        lab = t.get("lab", {})
        steps_html = []
        for step in lab.get("steps", []):
            rendered_step = render_code_blocks(step)
            # Remove wrapping <p> if single paragraph inside <li>
            rendered_step = re.sub(r"^<p>(.*?)</p>$", r"\1", rendered_step, flags=re.S)
            steps_html.append(f'<li>{rendered_step}</li>')

        p4_html.append(
            f'<article id="{key}-lab" class="topic-card lab">'
            f'<h3>Exercise {i}: {escape(lab.get("name", t["title"]))}</h3>'
            f'<p><strong>Goal:</strong> {escape(lab.get("goal", ""))}</p>'
            f'<p><strong>Expected result:</strong> {escape(lab.get("expected", ""))}</p>'
            f'<p><strong>Mode:</strong> {escape(lab.get("mode", "local exercise"))} · <strong>Prerequisite:</strong> {escape(lab.get("prereq", "Prior day artifacts"))}</p>'
            f'<p><strong>Preflight:</strong> {escape(lab.get("preflight", "Review environment and open editor."))}</p>'
            f'<h4>Exact execution</h4>'
            f'<ol>{"".join(steps_html)}</ol>'
            f'<h4>Verification</h4>'
            f'{render_code_blocks(lab.get("verification", "Verify expected state against baseline."))}'
            f'<h4>Troubleshooting</h4>'
            f'{render_code_blocks(lab.get("trouble", "Inspect system logs and check configuration syntax."))}'
            f'<h4>Cleanup and cost</h4>'
            f'{render_code_blocks(lab.get("cleanup", "No chargeable resources created."))}'
            f'<h4>Artifact acceptance</h4>'
            f'<p>{escape(lab.get("accept", "Completed artifact saved."))} File: <code>{escape(lab.get("file", f"day-{day_num:03d}-{key}.md"))}</code>.</p>'
            f'<label class="check"><input type="checkbox" data-progress="lab-{day_num}-{key}"> I completed and checked this topic exercise</label>'
            f'</article>'
        )
    put_section("part-4", "".join(p4_html))

    # ─── COMPLETION SUMMARY ─────────────────────────────────────────────
    completion = soup.select_one(".completion")
    if completion:
        for old in completion.select(".exit-summary"):
            old.decompose()
        completion.append(BeautifulSoup(f'<p class="exit-summary">Exit artifact: {escape(exit_summary)}</p>', "html.parser"))

    override_file.write_text(str(soup), encoding="utf-8")
    print(f"Updated override: {override_file}")


def build_and_validate(day_num: int) -> None:
    """Build day page and run site-wide validator."""
    print(f"\nBuilding Day {day_num}...")
    res = subprocess.run(
        [sys.executable, str(SCRIPTS / "build.py"), "--day", str(day_num)],
        cwd=str(ROOT),
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        print("Build failed:\n", res.stderr or res.stdout)
        sys.exit(res.returncode)
    print(res.stdout.strip())

    print("\nRunning validator...")
    res_val = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True
    )
    if res_val.returncode != 0:
        print("Validation errors:\n", res_val.stderr or res_val.stdout)
        sys.exit(res_val.returncode)
    print("Validation passed successfully! 0 errors.")


def load_day_module(path: Path) -> dict:
    """Dynamically load day data module."""
    spec = importlib.util.spec_from_file_location("day_data_module", path)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "DAY_DATA"):
        return getattr(module, "DAY_DATA")
    if hasattr(module, "DATA"):
        return getattr(module, "DATA")
    # Alternatively collect variables
    return {
        "day": getattr(module, "DAY", None),
        "topics": getattr(module, "TOPICS", []),
        "part1_intro": getattr(module, "PART1_INTRO", ""),
        "part2_intro": getattr(module, "PART2_INTRO", ""),
        "part3_intro": getattr(module, "PART3_INTRO", ""),
        "part4_intro": getattr(module, "PART4_INTRO", ""),
        "arch_diagram": getattr(module, "ARCH_DIAGRAM", {}),
        "arch_table_html": getattr(module, "ARCH_TABLE_HTML", ""),
        "exit_summary": getattr(module, "EXIT_SUMMARY", ""),
    }


def parse_range(range_str: str) -> list[int]:
    """Parse range string like '1-93', '1 - 93', '83..92', or '1,2,5'."""
    clean = range_str.replace(" ", "").replace("..", "-")
    days = []
    for part in clean.split(","):
        if "-" in part:
            start, end = part.split("-", 1)
            days.extend(range(int(start), int(end) + 1))
        else:
            days.append(int(part))
    return sorted(list(set(days)))


def process_single_day(day_num: int, data_path_override: str = "") -> None:
    data_path = Path(data_path_override) if data_path_override else ROOT / "scratch" / f"day_data_{day_num:03d}.py"
    if data_path.exists():
        print(f"Loading data from {data_path}...")
        data = load_day_module(data_path)
        compile_day_page(day_num, data)
        res = subprocess.run(
            [sys.executable, str(SCRIPTS / "build.py"), "--day", str(day_num)],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        if res.returncode != 0:
            sys.exit(f"Build failed for Day {day_num}:\n{res.stderr or res.stdout}")
        print(f"Built Day {day_num}: {SITE_DAYS / f'day-{day_num:03d}.html'}")
    else:
        override_file = ROOT / "content" / f"day-{day_num:03d}-page.html"
        if not override_file.exists():
            print(f"Skipping Day {day_num}: neither {data_path} nor {override_file} exists.")
            return
        soup = BeautifulSoup(override_file.read_text(encoding="utf-8"), "html.parser")
        labs = soup.select("article.lab")
        modified = False
        for lab in labs:
            for p in lab.select("p"):
                p_text = p.get_text()
                if "Skill Level:" in p_text or "Difficulty:" in p_text:
                    p.decompose()
                    modified = True
        if modified:
            override_file.write_text(str(soup), encoding="utf-8")
            print(f"Removed exercise difficulty labels in {override_file.name}")
        res = subprocess.run(
            [sys.executable, str(SCRIPTS / "build.py"), "--day", str(day_num)],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        if res.returncode != 0:
            sys.exit(f"Build failed for Day {day_num}:\n{res.stderr or res.stdout}")
        print(f"Built Day {day_num}: {SITE_DAYS / f'day-{day_num:03d}.html'}")


def main():
    parser = argparse.ArgumentParser(description="Deterministic authoring engine for 180-day GCP curriculum.")
    parser.add_argument("--day", type=int, default=None, help="Day number (1-180)")
    parser.add_argument("--range", type=str, default="", help="Range of days to author/update (e.g. '1-93' or '1 - 93')")
    parser.add_argument("--data", type=str, default="", help="Path to day data file (defaults to scratch/day_data_NNN.py)")
    args = parser.parse_args()

    if not args.day and not args.range:
        parser.error("Must specify either --day or --range.")

    if args.range:
        target_days = parse_range(args.range)
        print(f"Processing {len(target_days)} days in range {args.range}: {target_days[0]} to {target_days[-1]}...")
        for d in target_days:
            process_single_day(d)
        print("\nAll target days built. Running site-wide validator...")
        res_val = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        if res_val.returncode != 0:
            print("Validation errors:\n", res_val.stderr or res_val.stdout)
            sys.exit(res_val.returncode)
        print(res_val.stdout.strip())
        print("Validation passed successfully! 0 errors.")
    else:
        process_single_day(args.day, args.data)
        print("\nRunning validator...")
        res_val = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        if res_val.returncode != 0:
            print("Validation errors:\n", res_val.stderr or res_val.stdout)
            sys.exit(res_val.returncode)
        print(res_val.stdout.strip())
        print("Validation passed successfully! 0 errors.")


if __name__ == "__main__":
    main()
