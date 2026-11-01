#!/usr/bin/env python3
"""Measure deterministic structural metrics for every rendered day page."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT.parent / "roadmap-180-days.md"
JSON_OUTPUT = ROOT / "data" / "site-metrics.json"
MARKDOWN_OUTPUT = ROOT / "data" / "site-metrics.md"
BLOCK_RE = re.compile(r"^## Days? (\d+)(?:[–-](\d+))? — (.+)$")
STAGE_RE = re.compile(r"^Stage\s+([1-8])\b", re.I)


def roadmap_blocks(path: Path = ROADMAP) -> dict[int, str]:
    """Map every roadmap day to its canonical block, failing on gaps."""
    blocks = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = BLOCK_RE.match(line)
        if not match:
            continue
        start = int(match.group(1))
        end = int(match.group(2) or start)
        for day in range(start, end + 1):
            if day in blocks:
                raise ValueError(f"Day {day} occurs in multiple roadmap blocks")
            blocks[day] = match.group(3)
    expected = set(range(1, 181))
    if set(blocks) != expected:
        missing = sorted(expected - set(blocks))
        extra = sorted(set(blocks) - expected)
        raise ValueError(f"Roadmap block coverage mismatch; missing={missing}, extra={extra}")
    return blocks


def measure_day(day: int, page: Path, override: Path, block: str) -> dict:
    raw = page.read_bytes()
    soup = BeautifulSoup(raw, "html.parser")
    stage_headers = sum(
        bool(STAGE_RE.match(tag.get_text(" ", strip=True)))
        for tag in soup.find_all(("h3", "h4", "h5", "h6", "strong", "b"))
    )
    text = soup.get_text(" ", strip=True)
    return {
        "day": day,
        "block": block,
        "bytes": len(raw),
        "pre": len(soup.select("pre")),
        "svg": len(soup.select("svg")),
        "external_links": sum(
            (anchor.get("href") or "").startswith(("http://", "https://"))
            for anchor in soup.select("a[href]")
        ),
        "stage_headers": stage_headers,
        "tabletop": len(re.findall(r"\btabletop\b", text, re.I)),
        "override_present": override.is_file(),
    }


def collect(root: Path = ROOT, roadmap: Path | None = None) -> list[dict]:
    blocks = roadmap_blocks(roadmap or root.parent / "roadmap-180-days.md")
    metrics = []
    for day in range(1, 181):
        page = root / "days" / f"day-{day:03d}.html"
        if not page.is_file():
            raise FileNotFoundError(f"Missing rendered page: {page}")
        metrics.append(measure_day(
            day,
            page,
            root / "content" / f"day-{day:03d}-page.html",
            blocks[day],
        ))
    return metrics


def payload(days: list[dict]) -> dict:
    return {
        "schema_version": 1,
        "source": "rendered day pages and canonical roadmap block headings",
        "summary": {
            "days": len(days),
            "zero_pre": sum(row["pre"] == 0 for row in days),
            "zero_svg": sum(row["svg"] == 0 for row in days),
            "stage_headers_below_8": sum(row["stage_headers"] < 8 for row in days),
            "overrides_present": sum(row["override_present"] for row in days),
        },
        "days": days,
    }


def markdown(data: dict) -> str:
    summary = data["summary"]
    lines = [
        "# Site metrics baseline",
        "",
        (f"Days: {summary['days']} · zero `<pre>`: {summary['zero_pre']} · "
         f"zero `<svg>`: {summary['zero_svg']} · fewer than 8 stage headers: "
         f"{summary['stage_headers_below_8']} · overrides present: {summary['overrides_present']}"),
        "",
        "| Day | Block | Bytes | `<pre>` | `<svg>` | External links | Stage headers | Tabletop | Override |",
        "|---:|---|---:|---:|---:|---:|---:|---:|:---:|",
    ]
    for row in data["days"]:
        lines.append(
            f"| {row['day']} | {row['block']} | {row['bytes']} | {row['pre']} | "
            f"{row['svg']} | {row['external_links']} | {row['stage_headers']} | "
            f"{row['tabletop']} | {'yes' if row['override_present'] else 'no'} |"
        )
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=JSON_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=MARKDOWN_OUTPUT)
    args = parser.parse_args(argv)
    data = payload(collect())
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.markdown.write_text(markdown(data), encoding="utf-8")
    summary = data["summary"]
    print(
        f"Measured {summary['days']} days: zero pre={summary['zero_pre']}, "
        f"zero svg={summary['zero_svg']}, stage headers below 8={summary['stage_headers_below_8']}, "
        f"overrides={summary['overrides_present']}"
    )
    print(f"Wrote {args.json.relative_to(ROOT)} and {args.markdown.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
