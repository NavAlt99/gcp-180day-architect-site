"""Convert the existing Days 153–163 case/exam pages to the Day 142 format.

The existing authored prose is retained and normalized into author_engine's
data contract. The compiler then supplies the common accessible topology and
incident diagrams, source blocks, and eight-stage lab shell.
"""

from __future__ import annotations

import csv
import html
from pathlib import Path

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
COVERAGE = ROOT / "data" / "coverage.csv"
ACCESS_DATE = "2026-09-30"


def text(node: Tag | None) -> str:
    return node.get_text(" ", strip=True) if node else ""


def inner_html(article: Tag, skip_classes: set[str] | None = None) -> str:
    skip_classes = skip_classes or set()
    chunks = []
    for child in article.contents:
        if not isinstance(child, Tag):
            continue
        if child.name == "h3":
            continue
        if skip_classes.intersection(child.get("class", [])):
            continue
        chunks.append(str(child))
    return "".join(chunks)


def paragraphs(article: Tag) -> list[str]:
    return [text(p) for p in article.find_all("p") if text(p)]


def labeled(paras: list[str], *labels: str) -> str:
    for value in paras:
        low = value.lower()
        if any(low.startswith(label.lower()) for label in labels):
            return value
    return ""


def source_rows() -> dict[tuple[int, str], dict[str, str]]:
    with COVERAGE.open(newline="", encoding="utf-8") as stream:
        result = {}
        for row in csv.DictReader(stream):
            day = int(row["day"])
            index = sum(1 for (existing_day, _), _value in result.items() if existing_day == day) + 1
            result[(day, f"topic-{index:02d}")] = row
        return result


def source_url(row: dict[str, str]) -> str:
    return row["publisher_url"]


def source_topic(row: dict[str, str]) -> str:
    return row["source_topic_ids"]


def topology(day: int, title: str, topics: list[dict]) -> dict:
    day_label = html.escape(title)
    topic_hint = " / ".join(html.escape(t["title"][:42]) for t in topics[:3])
    return {
        "type": "topology",
        "title": f"Day {day}: {title} — evidence and decision path",
        "desc": f"Three-tier architecture path for {day_label}, showing case or exam inputs, requirements and trade-off evidence, then acceptance and ownership controls.",
        "caption": f"Scope: a synthetic evidence path for Day {day} covering {topic_hint}. It shows reasoning boundaries and verification ownership; it does not prove a production deployment, exam result, price, quota, eligibility or customer outcome.",
        "width": 1120,
        "height": 690,
        "layers": [
            {"name": "TIER 1 · INPUTS / DEMAND", "desc": "case facts, prompts and constraints", "x": 10, "y": 55, "w": 1100, "h": 92, "fill": "#0c2033", "title_color": "#38bdf8", "opacity": 0.72},
            {"name": "TIER 2 · EVIDENCE / REASONING", "desc": "requirements, alternatives and failure checks", "x": 10, "y": 185, "w": 1100, "h": 210, "fill": "#241808", "title_color": "#f59e0b", "opacity": 0.64},
            {"name": "TIER 3 · GOVERNANCE / ACCEPTANCE", "desc": "owners, acceptance and revisit triggers", "x": 10, "y": 435, "w": 1100, "h": 115, "fill": "#062316", "title_color": "#22c55e", "opacity": 0.68},
        ],
        "components": [
            {"name": "Case or prompt", "detail": f"Day {day} supplied scope", "x": 60, "y": 78, "w": 250, "h": 56, "stroke": "#38bdf8", "fill": "#102a42"},
            {"name": "Prior artifacts", "detail": "facts + decisions + errors", "x": 435, "y": 78, "w": 250, "h": 56, "stroke": "#38bdf8", "fill": "#102a42"},
            {"name": "Changed constraint", "detail": "cost / risk / scope", "x": 810, "y": 78, "w": 250, "h": 56, "stroke": "#38bdf8", "fill": "#102a42"},
            {"name": "Requirements map", "detail": "fact to acceptance", "x": 60, "y": 220, "w": 250, "h": 105, "stroke": "#f59e0b", "fill": "#3b2508"},
            {"name": "Option matrix", "detail": "choice + alternative", "x": 435, "y": 220, "w": 250, "h": 105, "stroke": "#f59e0b", "fill": "#3b2508"},
            {"name": "Failure rehearsal", "detail": "signal + safe response", "x": 810, "y": 220, "w": 250, "h": 105, "stroke": "#f59e0b", "fill": "#3b2508"},
            {"name": "Evidence owner", "detail": "source + artifact", "x": 245, "y": 455, "w": 250, "h": 70, "stroke": "#22c55e", "fill": "#064e3b"},
            {"name": "Acceptance gate", "detail": "observed / predicted", "x": 625, "y": 455, "w": 250, "h": 70, "stroke": "#22c55e", "fill": "#064e3b"},
        ],
        "flows": [
            {"x1": 185, "y1": 134, "x2": 185, "y2": 220, "type": "ok", "label": "extract"},
            {"x1": 560, "y1": 134, "x2": 560, "y2": 220, "type": "ok", "label": "trace"},
            {"x1": 935, "y1": 134, "x2": 935, "y2": 220, "type": "warn", "label": "challenge"},
            {"x1": 310, "y1": 272, "x2": 435, "y2": 272, "type": "ok", "label": "compare"},
            {"x1": 685, "y1": 272, "x2": 810, "y2": 272, "type": "ok", "label": "rehearse"},
            {"x1": 935, "y1": 325, "x2": 750, "y2": 455, "type": "ok", "label": "accept"},
            {"x1": 560, "y1": 325, "x2": 370, "y2": 455, "type": "warn", "label": "evidence"},
            {"x1": 495, "y1": 490, "x2": 625, "y2": 490, "type": "ok", "label": "review"},
        ],
        "boundaries": [
            {"x": 42, "y": 205, "w": 1036, "h": 140, "color": "#f59e0b", "label": "EVIDENCE CHECK"},
            {"x": 220, "y": 442, "w": 680, "h": 94, "color": "#22c55e", "label": "DECISION OWNER"},
        ],
        "probes": [
            {"cx": 185, "cy": 106, "label": "PROBE 1 · input classified", "badge": "P1", "color": "#38bdf8"},
            {"cx": 560, "cy": 272, "label": "PROBE 2 · trade-off recorded", "badge": "P2", "color": "#f59e0b"},
            {"cx": 750, "cy": 490, "label": "PROBE 3 · acceptance result", "badge": "P3", "color": "#22c55e"},
        ],
    }


def table_for(topics: list[dict]) -> str:
    rows = []
    for topic in topics:
        title = html.escape(topic["title"])
        rows.append(
            f"<tr><td>{title}</td><td>Separate supplied fact, requirement and proposed control.</td>"
            f"<td>One artifact, one rejected alternative and one changed-constraint result.</td>"
            f"<td>Local/tabletop evidence cannot prove production behavior or exam performance.</td></tr>"
        )
    return """
<table><caption>Day-specific architecture and evidence path</caption><thead><tr><th>Topic boundary</th><th>Decision rule</th><th>Acceptance evidence</th><th>Limit</th></tr></thead><tbody>
""" + "".join(rows) + "</tbody></table>"


def make_lab_steps(day: int, title: str, old_steps: list[str], file_name: str) -> list[str]:
    labels = [
        "Preflight and validate assumptions/environment",
        "Prepare the target, inputs, or backing resources",
        "Author the plan, configuration, or analysis",
        "Execute or simulate the planned change",
        "Inspect expected state and verify outcomes",
        "Rehearse a bounded failure, edge case, or decision challenge",
        "Diagnose evidence and record remediation/decision",
        "Clean up or close out the exercise",
    ]
    if len(old_steps) >= 8:
        bodies = old_steps[:8]
    else:
        bodies = [
            f"Open the existing Day {day} artifact and record the source, date, lab mode, owner and synthetic-data boundary. Do not add credentials or protected exam material.",
            f"Copy the fixed facts and constraints for **{title}** into a table with `input | owner | evidence | limit` columns. Mark missing values as questions.",
            "Add one selected option, one rejected alternative, an acceptance signal, a rollback or stop condition, and the artifact file name.",
            old_steps[0] if old_steps else f"Complete the local/tabletop exercise for **{title}** using a small synthetic fixture and save the exact decision or classification.",
            old_steps[1] if len(old_steps) > 1 else "Compare the result with the day's exit evidence. Label every claim as supplied, observed locally, or predicted and check the invariant that matters.",
            old_steps[2] if len(old_steps) > 2 else "Change one material constraint or replay one synthetic input. Record the first changed signal and the safe response.",
            old_steps[3] if len(old_steps) > 3 else "Write the causal diagnosis, remediation owner, verification result, rejected alternative and unresolved risk.",
            old_steps[-1] if len(old_steps) > 4 else f"Save `{file_name}`, link it from the daily artifact, remove disposable copies and record what still needs authorized verification.",
        ]
    result = []
    for index, label in enumerate(labels):
        result.append(f"**Stage {index + 1} — {label}.** {bodies[index]}")
    return result


def parse_day(day: int, rows: dict[tuple[int, str], dict[str, str]]) -> dict:
    path = CONTENT / f"day-{day:03d}-page.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    title = text(soup.select_one("main h1")).split(" — ", 1)[-1]
    exit_summary = text(soup.select_one(".callout.success p")) or "A saved, source-linked design artifact and remaining risk list."
    topics = []
    overview_articles = soup.select("#part-1 > article")
    technical_articles = soup.select("#part-2 > article")
    problem_articles = soup.select("#part-3 > article")
    lab_articles = soup.select("#part-4 > article")

    for index, overview in enumerate(overview_articles, 1):
        key = f"topic-{index:02d}"
        topic_title = text(overview.find("h3"))
        overview_paras = paragraphs(overview)
        overview_text = " ".join(p for p in overview_paras if "Technical discussion" not in p and "Step-by-step lab" not in p)
        preview = next((p for p in overview_paras if p.lower().startswith("problem preview:")), "")
        if preview.lower().startswith("problem preview:"):
            preview = preview.split(":", 1)[1].strip()
        if "." not in preview:
            preview = f"Symptom: the {topic_title.lower()} decision has an unverified boundary. Effect: the team may choose a path without a reproducible acceptance result."
        elif preview.count(".") < 2:
            preview += " Effect: the team may choose a path without a reproducible acceptance result."

        technical = technical_articles[index - 1] if index <= len(technical_articles) else None
        problem = problem_articles[index - 1] if index <= len(problem_articles) else None
        lab = lab_articles[index - 1] if index <= len(lab_articles) else None
        row = rows.get((day, f"topic-{index:02d}"), rows.get((day, "topic-01")))

        tech_html = inner_html(technical, {"further"}) if technical else f"<p>{html.escape(overview_text)}</p>"
        tech_html += f'<p><a href="../sources.html#topic-{source_topic(row).split(",")[0].zfill(3)}">Local source-topic section</a>; classify source facts, local observations and proposals separately. Access checked {ACCESS_DATE}.</p>'

        problem_paras = paragraphs(problem) if problem else []
        scenario_text = problem_paras[0] if problem_paras else f"Synthetic teaching case for {topic_title}."
        impact = labeled(problem_paras, "situation and impact:", "failure symptoms and impact:") or (problem_paras[1] if len(problem_paras) > 1 else "The decision cannot be accepted until its boundary and evidence are visible.")
        constraints = labeled(problem_paras, "constraints:", "business and operational constraints:") or "Use synthetic data, preserve the prior artifact and keep unverified claims explicitly labeled."
        root = labeled(problem_paras, "diagnosis:", "root cause:", "architectural inference:") or "The design treated a plausible conclusion as evidence without a reproducible acceptance check."
        fix = labeled(problem_paras, "defensible solution:", "defensible fix:", "fix:") or "Add a bounded control at the owning boundary, retain the rejected alternative and define a measurable acceptance signal."
        verify = labeled(problem_paras, "verification:", "verification and residual risk:") or "Re-run the fixed synthetic input, compare it with the expected state and save the decision trace."
        residual = labeled(problem_paras, "residual risk:", "residual:") or "A tabletop or local result does not prove production scale, permissions, pricing, exam eligibility or customer acceptance."
        if "residual risk" in verify.lower() and not residual.startswith("Residual"):
            residual = "The remaining limitation is that a synthetic or tabletop result does not prove production behavior."

        old_steps = [text(li) for li in lab.select("ol li")] if lab else []
        lab_paras = paragraphs(lab) if lab else []
        goal = labeled(lab_paras, "goal:") or f"Produce a source-linked artifact for {topic_title}."
        mode = labeled(lab_paras, "mode:") or "local/tabletop with synthetic data; no cloud access or spend"
        prereq = labeled(lab_paras, "prerequisite:") or "Bring the prior day artifact and mark it unavailable if missing."
        callout_text = " ".join(text(x) for x in lab.select(".callout") if text(x)) if lab else ""
        file_match = next((c.get_text(strip=True) for c in lab.select("code") if ".md" in c.get_text()), f"day-{day:03d}-{key}.md") if lab else f"day-{day:03d}-{key}.md"

        topics.append({
            "key": key,
            "title": topic_title,
            "overview": overview_text or f"Study {topic_title.lower()} and connect it to the day's exit evidence.",
            "preview": preview,
            "technical": tech_html,
            "questions": [
                f"Which supplied fact or requirement controls the {topic_title.lower()} decision?",
                "What alternative remains credible, and what evidence would make it preferable?",
                "What signal would show that the chosen boundary has failed?",
                "Which result is observed, supplied or predicted?",
            ],
            "reference": source_url(row),
            "reference_label": f"Official source for Topic {source_topic(row)} (checked {ACCESS_DATE})",
            "scenario": {
                "scenario": scenario_text,
                "impact": impact,
                "constraints": constraints,
                "facts": "The supplied case or study prompt is a teaching input; no production incident is claimed.",
                "inference": root,
                "root": root,
                "fix": fix,
                "verify": verify,
                "residual": residual,
                "diagram": ("supplied input", "unverified boundary", "business or operational impact", "bounded control", "verified artifact"),
            },
            "lab": {
                "name": topic_title,
                "goal": goal,
                "expected": exit_summary,
                "mode": mode,
                "prereq": prereq,
                "preflight": f"Use a local note named `{file_match}`; record the date, prior artifact, source and synthetic-data boundary.",
                "steps": make_lab_steps(day, topic_title, old_steps, file_match),
                "verification": callout_text or "The saved artifact contains the input, decision, evidence classification, negative case, acceptance result and remaining risk.",
                "accept": "Another architect can reproduce the decision, locate the source and artifact, identify the rejected alternative and see what remains unproven.",
                "trouble": "If the result is only a plausible explanation, mark it predicted and add the missing observation or acceptance test. Do not turn a page completion or green command into proof.",
                "cleanup": "No chargeable resource is created unless the roadmap explicitly requires one. Keep the artifact and remove only disposable working copies; never store credentials or protected exam content.",
                "file": file_match,
            },
        })

    return {
        "day": day,
        "part1_intro": f"Day {day} — {title} — turns the existing case or exam material into a source-linked architecture decision. Preserve the original requirements and keep every inference, observation and open question visible.",
        "part2_intro": "Use the same path as Day 142: inputs become requirements, requirements become alternatives, and alternatives are accepted only with evidence, an owner and a bounded failure response.",
        "part3_intro": "These are synthetic field cases. They separate supplied facts from architectural inference and do not represent observed production incidents, exam results or customer outcomes.",
        "part4_intro": "Every exercise follows the eight-stage execution contract and uses the existing artifact as its starting point. Use local or tabletop work unless the roadmap explicitly requires a cloud operation.",
        "exit_summary": exit_summary,
        "arch_table_html": table_for(topics),
        "arch_diagram": topology(day, title, topics),
        "topics": topics,
    }


def write_module(day: int, data: dict) -> None:
    path = ROOT / "scratch" / f"day_data_{day:03d}.py"
    path.write_text("DAY_DATA = " + repr(data) + "\n", encoding="utf-8")
    print(f"wrote {path}")


def main() -> None:
    rows = source_rows()
    for day in range(153, 164):
        write_module(day, parse_day(day, rows))


if __name__ == "__main__":
    main()
