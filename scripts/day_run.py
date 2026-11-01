#!/usr/bin/env python3
"""Run one curriculum day through resolve, preflight, checks, gate, and commit."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT.parent / "roadmap-180-days.md"
PYTHON = sys.executable

URL_CREDENTIAL = re.compile(r"(?P<scheme>https?://)[^/@\s]+@", re.I)
SECRET_PATTERNS = (
    re.compile(r"\b(?:gh[opusr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"(?i)\b(Bearer\s+)[A-Za-z0-9._~+/=-]+"),
    re.compile(r"(?i)\b((?:access_?token|api_?key|password|passwd|secret)\s*[=:]\s*)[^\s]+"),
)


def mask_credentials(value: str) -> str:
    """Mask URL userinfo and common token forms before any subprocess output is shown."""
    value = URL_CREDENTIAL.sub(r"\g<scheme>***@", value)
    for pattern in SECRET_PATTERNS:
        value = pattern.sub(lambda match: (match.group(1) if match.lastindex else "") + "***", value)
    return value


def emit(value: str) -> None:
    if not value:
        return
    print(mask_credentials(value), end="" if value.endswith("\n") else "\n", flush=True)


def command(script: str, day: int, *extra: str) -> list[str]:
    return [PYTHON, "-B", str(ROOT / "scripts" / script), "--day", str(day), *extra]


def run(command_line: list[str], *, runner=subprocess.run) -> int:
    result = runner(
        command_line,
        cwd=ROOT,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    emit(result.stdout or "")
    return result.returncode


def day_paths(day: int) -> dict[str, Path]:
    nnn = f"{day:03d}"
    return {
        "inputs": ROOT / "scratch" / f"day-{nnn}-inputs.md",
        "spec": ROOT / "scratch" / f"day_data_{nnn}.py",
        "spec_directory": ROOT / "scratch" / f"day_data_{nnn}",
        "override": ROOT / "content" / f"day-{nnn}-page.html",
        "page": ROOT / "days" / f"day-{nnn}.html",
        "terms": ROOT / "scratch" / "audits" / f"day-{nnn}-terms.txt",
        "handoff": ROOT / "scratch" / "handoffs" / f"day-{nnn}.md",
    }


def resolve(day: int) -> int:
    emit(f"Day {day:03d} workflow paths:\n")
    for label, path in day_paths(day).items():
        state = "present" if path.exists() else "missing"
        emit(f"  {label}: {path.relative_to(ROOT)} ({state})\n")
    return 0


def git(*args: str, runner=subprocess.run) -> subprocess.CompletedProcess[str]:
    return runner(
        ["git", *args], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )


def preflight(day: int, *, allow_dirty: bool = False, runner=subprocess.run) -> int:
    failures = []
    if not ROADMAP.is_file():
        failures.append(f"missing roadmap: {ROADMAP}")
    required = (
        "extract_day_inputs.py", "validate_spec.py", "author_engine.py", "build.py",
        "validate.py", "check_study_links.py", "run_labs.py", "write_handoff.py",
        "check_page_rules.py", "batch_gate.py",
    )
    for name in required:
        if not (ROOT / "scripts" / name).is_file():
            failures.append(f"missing workflow script: scripts/{name}")

    branch_result = git("branch", "--show-current", runner=runner)
    branch = branch_result.stdout.strip()
    if branch_result.returncode:
        failures.append("unable to resolve current Git branch")
    elif not branch or branch in {"main", "master"}:
        failures.append(f"unsafe branch: {branch or 'detached HEAD'}")

    status_result = git("status", "--porcelain", runner=runner)
    if status_result.returncode:
        failures.append("unable to inspect working tree")
    elif status_result.stdout.strip() and not allow_dirty:
        failures.append("working tree is not clean (use --allow-dirty only for an intentional resumed day)")

    remote_result = git("remote", "-v", runner=runner)
    if remote_result.returncode == 0 and URL_CREDENTIAL.search(remote_result.stdout):
        emit("WARNING: a Git remote contains an embedded credential; revoke it. The URL is masked and unchanged.\n")

    if failures:
        for failure in failures:
            emit(f"FAIL: {failure}\n")
        return 1
    emit(f"PASS: Day {day:03d} preflight on {branch}\n")
    return 0


def check(day: int, *, diagrams: str = "allow", skip_labs: bool = False,
          runner=subprocess.run) -> int:
    paths = day_paths(day)
    steps: list[list[str]] = [command("extract_day_inputs.py", day)]
    if not paths["spec"].exists() and not paths["spec_directory"].is_dir():
        steps.append(command("new_day_skeleton.py", day))
    steps.extend((
        command("validate_spec.py", day),
        command("author_engine.py", day),
        command("build.py", day),
        command("validate.py", day),
        command("check_study_links.py", day, "--report", str(ROOT / "scratch" / f"day-{day:03d}-study-links.json")),
    ))
    if not skip_labs:
        steps.append(command("run_labs.py", day))
    page_rule = command("check_page_rules.py", day, "--diagrams", diagrams)
    if paths["terms"].is_file():
        page_rule.extend(("--terms-file", str(paths["terms"])))
    steps.append(page_rule)
    steps.append(command("write_handoff.py", day))

    for step in steps:
        if run(step, runner=runner):
            emit(f"FAIL: stopped at {Path(step[2]).name}\n")
            return 1
    emit(f"PASS: Day {day:03d} checks\n")
    if skip_labs:
        emit("NOT CHECKED: labs were explicitly skipped; record the cloud/tool reason in the handoff.\n")
    return 0


def gate(day: int, *, skip_labs: bool = False, runner=subprocess.run) -> int:
    step = command("batch_gate.py", day, "--contract-hash")
    if skip_labs:
        step.append("--skip-labs")
    return run(step, runner=runner)


def permitted_day_path(path: str, day: int) -> bool:
    nnn = f"{day:03d}"
    exact = {
        f"scratch/day_data_{nnn}.py",
        f"content/day-{nnn}-page.html",
        f"days/day-{nnn}.html",
        "data/coverage.csv",
        f"scratch/handoffs/day-{nnn}.md",
    }
    prefixes = (
        f"scratch/day_data_{nnn}/",
        f"scratch/day-{nnn}-",
        f"scratch/audits/day-{nnn}-",
    )
    return path in exact or path.startswith(prefixes)


def changed_paths(*, runner=subprocess.run) -> list[str]:
    result = git("status", "--porcelain", "-z", runner=runner)
    if result.returncode:
        raise RuntimeError("git status failed")
    paths = []
    entries = result.stdout.split("\0")
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if not entry:
            continue
        status, path = entry[:2], entry[3:]
        if status[0] in "RC" or status[1] in "RC":
            if index < len(entries):
                index += 1
        paths.append(path)
    return paths


def commit(day: int, message: str | None, *, runner=subprocess.run) -> int:
    paths = changed_paths(runner=runner)
    unexpected = [path for path in paths if not permitted_day_path(path, day)]
    if unexpected:
        emit("FAIL: refusing to commit out-of-scope changes:\n")
        for path in unexpected:
            emit(f"  {path}\n")
        return 1
    if not paths:
        emit("FAIL: no Day-specific changes to commit\n")
        return 1
    add_result = git("add", "--", *paths, runner=runner)
    emit(add_result.stdout or "")
    if add_result.returncode:
        return add_result.returncode
    commit_result = git("commit", "-m", message or f"Update Day {day:03d} curriculum page", runner=runner)
    emit(commit_result.stdout or "")
    return commit_result.returncode


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("action", choices=("resolve", "preflight", "check", "gate", "commit"))
    result.add_argument("--day", type=int, required=True, choices=range(1, 181))
    result.add_argument("--diagrams", choices=("keep", "allow"), default="allow")
    result.add_argument("--skip-labs", action="store_true")
    result.add_argument("--allow-dirty", action="store_true")
    result.add_argument("--message")
    return result


def main(argv: Iterable[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.action == "resolve":
        return resolve(args.day)
    if args.action == "preflight":
        return preflight(args.day, allow_dirty=args.allow_dirty)
    if args.action == "check":
        return check(args.day, diagrams=args.diagrams, skip_labs=args.skip_labs)
    if args.action == "gate":
        return gate(args.day, skip_labs=args.skip_labs)
    return commit(args.day, args.message)


if __name__ == "__main__":
    raise SystemExit(main())
