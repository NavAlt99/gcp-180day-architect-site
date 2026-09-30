"""Build deep, topic-specific Day 142-style specs for Days 153–163."""

from __future__ import annotations

import csv
import importlib.util
import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag

from upgrade_days_153_163_rich import table_for, topology

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
ACCESS_DATE = "2026-09-30"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


OLD_CASES = load(ROOT / "scratch" / "redo_days_153_154.py", "old_cases")
OLD_DATA = load(ROOT / "scratch" / "redo_days_155_163.py", "old_data")


def clean(value: str) -> str:
    value = re.sub(r"^(?:Situation and impact|Failure symptoms and impact|Constraints|Diagnosis and solution|Diagnosis|Defensible solution|Defensible fix|Fix|Verification and residual risk|Verification|Residual risk|Goal|Mode|Prerequisite|Expected state|Expected result)\s*:\s*", "", value, flags=re.I)
    return " ".join(value.split())


def text(node: Tag | None) -> str:
    return clean(node.get_text(" ", strip=True)) if node else ""


def source_rows() -> dict[tuple[int, int], dict[str, str]]:
    result = {}
    with (ROOT / "data" / "coverage.csv").open(newline="", encoding="utf-8") as stream:
        seen: dict[int, int] = {}
        for row in csv.DictReader(stream):
            day = int(row["day"])
            seen[day] = seen.get(day, 0) + 1
            result[(day, seen[day])] = row
    return result


SOURCES = source_rows()


def source_details(day: int, index: int) -> tuple[str, str, str]:
    row = SOURCES[(day, index)]
    topic_id = row["source_topic_ids"].split(",")[0].zfill(3)
    return row["publisher_url"], f"Official Topic {row['source_topic_ids']} source (checked {ACCESS_DATE})", topic_id


def extract_labs(article: Tag) -> tuple[str, str, str, str, list[str], str, str]:
    paragraphs = [p.get_text(" ", strip=True) for p in article.find_all("p")]
    goal = next((clean(p) for p in paragraphs if p.lower().startswith("goal:")), "Produce a source-linked decision artifact.")
    mode_raw = next((clean(p) for p in paragraphs if p.lower().startswith("mode:")), "local/tabletop with synthetic data; no cloud access or spend")
    if re.search(r"\bPrerequisite:\s*", mode_raw, re.I):
        mode, prereq = re.split(r"\bPrerequisite:\s*", mode_raw, maxsplit=1, flags=re.I)
        mode, prereq = mode.strip(" ·; "), prereq.strip()
    else:
        mode = mode_raw
        prereq = next((clean(p) for p in paragraphs if "prerequisite:" in p.lower()), "Bring the prior artifact and record it unavailable if missing.")
    expected = next((clean(p) for p in paragraphs if p.lower().startswith("expected state:") or p.lower().startswith("expected result:")), "A saved decision, negative case and evidence classification.")
    steps = [li.get_text(" ", strip=True) for li in article.select("ol li")]
    trouble = " ".join(x.get_text(" ", strip=True) for x in article.select(".callout.caution"))
    accept = " ".join(x.get_text(" ", strip=True) for x in article.select(".callout.success, .callout:not(.caution)"))
    if expected == "A saved decision, negative case and evidence classification." and accept:
        expected = clean(accept)
    file_name = next((c.get_text(strip=True) for c in article.select("code") if ".md" in c.get_text()), "day-artifact.md")
    return goal, mode, prereq, expected, steps, trouble, accept or file_name


def eight_steps(day: int, index: int, title: str, source_url: str, old_steps: list[str], file_name: str) -> list[str]:
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
    bodies = [
        f"Create `{file_name}`. Record Day {day}, the prior artifact, the source `{source_url}`, the access date, a named owner and the statement that the exercise uses synthetic or tabletop evidence only.",
        old_steps[0] if len(old_steps) > 0 else f"Write the fixed inputs and requirements for **{title}** in an `input | owner | evidence | limit` table; label gaps as questions.",
        old_steps[1] if len(old_steps) > 1 else "Draft the selected option, rejected alternative, acceptance signal and the condition that would change the choice.",
        old_steps[2] if len(old_steps) > 2 else "Apply the decision to the fixed synthetic input and record the exact classification, calculation or design outcome.",
        old_steps[3] if len(old_steps) > 3 else "Compare the result against the stated acceptance signal and mark each claim as supplied, observed locally or predicted.",
        old_steps[4] if len(old_steps) > 4 else "Change one material constraint or replay one synthetic input. Record the first changed signal and the safe stop or fallback.",
        old_steps[5] if len(old_steps) > 5 else "Write the root cause, remediation owner, verification result, residual risk and next review date.",
        old_steps[6] if len(old_steps) > 6 else f"Save `{file_name}`, link it from the daily artifact, keep the evidence, remove only disposable copies and state what needs an authorized or production verification.",
    ]
    return [f"**Stage {i + 1} — {labels[i]}.** {clean(bodies[i])}" for i in range(8)]


def scenario_from_paragraphs(paras: list[str], title: str) -> dict:
    values = [clean(p) for p in paras]
    def find(*prefixes: str, default: str) -> str:
        for raw in paras:
            low = raw.lower()
            if any(low.startswith(prefix.lower()) for prefix in prefixes):
                return clean(raw)
        return default
    scenario = find("Situation and impact:", "Enterprise scenario:", default=values[0] if values else f"Synthetic field case for {title}.")
    separate_impact = next((clean(raw) for raw in paras if raw.lower().startswith("failure symptoms and impact:")), "")
    impact = separate_impact
    constraints = find("Constraints:", default="Use synthetic data, preserve the prior artifact and keep unknown behavior explicitly labeled.")
    root = find("Diagnosis and solution:", "Diagnosis:", "Root cause:", default="The design made a claim before assigning an evidence owner, acceptance signal or changed-constraint test.")
    fix = find("Defensible solution:", "Defensible fix:", "Diagnosis and solution:", default="Add the smallest control at the owning boundary, retain a credible alternative and make the acceptance result observable.")
    verify = find("Verification and residual risk:", "Verification:", default="Re-run the bounded case, compare it with the declared acceptance signal and save the resulting decision trace.")
    residual = find("Residual risk:", "Verification and residual risk:", default="A local or tabletop result does not prove production permissions, scale, pricing, compliance approval or exam performance.")
    return {
        "scenario": scenario,
        "impact": impact,
        "constraints": constraints,
        "facts": "The case statement and artifact are teaching inputs; no production incident or learner result is claimed.",
        "inference": root,
        "root": root,
        "fix": fix,
        "verify": verify,
        "residual": residual,
        "diagram": ("supplied trigger", "missing or untested control", "business and operating impact", "bounded defensive control", "verified evidence artifact"),
    }


def overview_preview(problem: dict, title: str) -> str:
    symptom = problem["scenario"].split(".", 1)[0].strip()
    impact = problem["impact"].split(".", 1)[0].strip()
    return f"Symptom: {symptom}. Effect: {impact or f'The {title.lower()} decision remains unverified.'}"


def topic_from_html(day: int, index: int, overview: Tag, technical: Tag, problem: Tag, lab: Tag) -> dict:
    title = text(overview.find("h3"))
    overview_text = " ".join(text(p) for p in overview.find_all("p") if "Technical discussion" not in text(p) and "Step-by-step lab" not in text(p))
    technical_html = "".join(str(child) for child in technical.contents if not (isinstance(child, Tag) and child.name == "h3"))
    source_url, source_label, source_topic = source_details(day, index)
    technical_html += f'<p><a href="../sources.html#topic-{source_topic}">Topic {source_topic} source section</a>; current publisher material was checked {ACCESS_DATE}. Separate supplied facts, local observations and proposed controls.</p>'
    scenario = scenario_from_paragraphs([p.get_text(" ", strip=True) for p in problem.find_all("p")], title)
    goal, mode, prereq, expected, old_steps, trouble, accept = extract_labs(lab)
    file_name = next((c.get_text(strip=True) for c in lab.select("code") if ".md" in c.get_text()), f"day-{day:03d}-{index:02d}-artifact.md")
    return {
        "key": f"topic-{index:02d}", "title": title, "overview": overview_text,
        "preview": overview_preview(scenario, title), "technical": technical_html,
        "questions": [
            "Which supplied fact, requirement or artifact controls the choice?",
            "Which credible alternative is rejected, and what evidence would make it preferable?",
            "Which failure signal reveals the first broken boundary?",
            "What is observed, supplied, predicted or still unknown?",
        ],
        "reference": source_url, "reference_label": source_label, "scenario": scenario,
        "lab": {
            "name": title, "goal": goal, "expected": expected, "mode": mode, "prereq": prereq,
            "preflight": f"Use `{file_name}` and record the source, access date, prior artifact, owner and synthetic-data boundary.",
            "steps": eight_steps(day, index, title, source_url, old_steps, file_name),
            "verification": expected, "accept": accept,
            "trouble": clean(trouble) or "Record the missing evidence rather than inventing a service behavior, score, price, permission or production result.",
            "cleanup": "Keep the evidence artifact and remove only disposable copies. No cloud resource, credential, payment detail or protected exam content belongs in this exercise.", "file": file_name,
        },
    }


def topic_from_dict(day: int, index: int, item: dict) -> dict:
    title = item["title"]
    source_url, source_label, source_topic = source_details(day, index)
    overview = BeautifulSoup(item["overview"], "html.parser").get_text(" ", strip=True)
    technical = item["technical"] + f'<p><a href="../sources.html#topic-{source_topic}">Topic {source_topic} source section</a>; current publisher material was checked {ACCESS_DATE}. Separate supplied facts, local observations and proposed controls.</p>'
    problem_soup = BeautifulSoup(item["problem"], "html.parser")
    scenario = scenario_from_paragraphs([p.get_text(" ", strip=True) for p in problem_soup.find_all("p")], title)
    old_steps = [li.get_text(" ", strip=True) for li in BeautifulSoup(item["steps"], "html.parser").find_all("li")]
    file_name = f"day-{day:03d}-{index:02d}-{'-'.join(re.findall('[a-z0-9]+', item['lab_title'].lower()))[:36]}.md"
    return {
        "key": f"topic-{index:02d}", "title": title, "overview": overview,
        "preview": overview_preview(scenario, title), "technical": technical,
        "questions": [
            "Which requirement bounds the selected option?", "What observable evidence supports the decision?",
            "Which changed constraint would reverse the choice?", "Who owns the failure response and review?",
        ],
        "reference": source_url, "reference_label": source_label, "scenario": scenario,
        "lab": {
            "name": item["lab_title"], "goal": item["lab_goal"], "expected": item["expected"],
            "mode": "local/tabletop with synthetic data; no cloud access or spend", "prereq": "Bring the prior case or exam artifact and record it unavailable if missing.",
            "preflight": f"Use `{file_name}`; record the source, access date, prior artifact, owner and synthetic-data boundary.",
            "steps": eight_steps(day, index, title, source_url, old_steps, file_name),
            "verification": item["expected"],
            "accept": "The saved artifact identifies the requirement, selected and rejected options, acceptance evidence, failure response, owner and residual risk.",
            "trouble": item["trouble"],
            "cleanup": "Keep the evidence artifact and remove only disposable copies. No cloud resource, credential, payment detail or protected exam content belongs in this exercise.", "file": file_name,
        },
    }


def hero(day: int) -> tuple[str, str]:
    soup = BeautifulSoup((CONTENT / f"day-{day:03d}-page.html").read_text(), "html.parser")
    title = text(soup.select_one("main h1")).split(" — ", 1)[-1]
    exit_node = soup.select_one(".hero .callout.success p")
    return title, text(exit_node) or "A source-linked artifact with a decision, evidence and remaining risk."


def old_html_topics(day: int) -> list[dict]:
    raw = getattr(OLD_CASES, f"DAY{day}")
    soup = BeautifulSoup(raw, "html.parser")
    overviews = soup.select("#part-1 > article")
    technicals = soup.select("#part-2 > article")
    problems = soup.select("#part-3 > article")
    labs = soup.select("#part-4 > article")
    return [topic_from_html(day, i, overviews[i - 1], technicals[i - 1], problems[i - 1], labs[i - 1]) for i in range(1, len(overviews) + 1)]


def deep_data(day: int) -> dict:
    title, exit_summary = hero(day)
    topics = old_html_topics(day) if day in (153, 154) else [topic_from_dict(day, i, value) for i, value in enumerate(getattr(OLD_DATA, f"DAY{day}"), 1)]
    return {
        "day": day,
        "part1_intro": f"Day {day} — {title} — uses the roadmap's case or exam scope as the input. Each topic names the decision boundary, evidence owner and business effect; no product choice or score is treated as a fact without supporting evidence.",
        "part2_intro": "Trace the full reasoning path: supplied fact or requirement, candidate design or study rule, acceptance evidence, failure signal, owner and condition that would change the choice. The topology is a teaching model, not evidence of a live system or exam result.",
        "part3_intro": "These deep-dive cases preserve the original case or exam reasoning while separating supplied facts from architectural inference. The incident diagrams are synthetic exercises, not observed production events.",
        "part4_intro": "The labs retain each day's original decision work, expanded into the eight execution stages used on Day 142. Complete them with prior artifacts and synthetic inputs unless an earlier roadmap page explicitly authorizes a cloud test.",
        "exit_summary": exit_summary,
        "arch_table_html": table_for(topics), "arch_diagram": topology(day, title, topics), "topics": topics,
    }


def main() -> None:
    for day in range(153, 164):
        path = ROOT / "scratch" / f"day_data_{day:03d}.py"
        path.write_text("DAY_DATA = " + repr(deep_data(day)) + "\n", encoding="utf-8")
        print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
