#!/usr/bin/env python3
"""Warn or fail when rendered page depth is below its frozen block floor.

The gated measure is rendered bytes. Other site metrics are printed for
diagnosis but are not monotonic quality signals: an eligible SVG is optional,
and more links or uses of "tabletop" do not necessarily mean more depth.

Floors were frozen from the phase-1 baseline. For each block, authored pages
(full-page overrides) were ranked by rendered bytes, the largest three were
selected, and their exact median became the floor. Blocks with no authored
override inherit the immediately preceding block's authored median so a
current skeleton cannot define its own acceptance threshold.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts import site_metrics


FLOORS = {
    "Foundations": {"bytes": 265647, "source_days": [4, 10, 7]},
    "Cloud environment and identity": {"bytes": 183940, "source_days": [19, 21, 24]},
    "Core services and integrated practice": {"bytes": 163676, "source_days": [62, 45, 63]},
    "Requirements, migration and architecture": {"bytes": 158876, "source_days": [74, 80, 77]},
    "Reliability and security": {"bytes": 165047, "source_days": [92, 112, 99]},
    "Performance, delivery and operations": {"bytes": 138875, "source_days": [130, 124, 128]},
    "Data, AI and distributed correctness": {"bytes": 100906, "source_days": [139, 137, 138]},
    "Discovery, cases and exam preparation": {"bytes": 112037, "source_days": [150, 163, 151]},
    "Multi-team architecture and synthesis": {
        "bytes": 112037, "source_days": [150, 163, 151], "inherited_from": "Discovery, cases and exam preparation"
    },
    "Final gate and capstone defenses": {"bytes": 61393, "source_days": [179, 178]},
    "Final review and rest": {
        "bytes": 61393, "source_days": [179, 178], "inherited_from": "Final gate and capstone defenses"
    },
}


def evaluate(row: dict) -> dict:
    floor = FLOORS.get(row["block"])
    if floor is None:
        raise ValueError(f"No depth floor for block: {row['block']}")
    return {
        **row,
        "floor_bytes": floor["bytes"],
        "source_days": floor["source_days"],
        "inherited_from": floor.get("inherited_from"),
        "deficit_bytes": max(0, floor["bytes"] - row["bytes"]),
        "passes": row["bytes"] >= floor["bytes"],
    }


def format_result(result: dict, status: str) -> str:
    inheritance = (
        f"; inherited from {result['inherited_from']}"
        if result.get("inherited_from") else ""
    )
    return (
        f"{status} Day {result['day']:03d} depth: bytes={result['bytes']} "
        f"floor={result['floor_bytes']} deficit={result['deficit_bytes']} "
        f"block={result['block']!r} source_days={result['source_days']}{inheritance}; "
        f"pre={result['pre']} svg={result['svg']} external_links={result['external_links']} "
        f"stage_headers={result['stage_headers']} tabletop={result['tabletop']} "
        f"override={'yes' if result['override_present'] else 'no'}"
    )


def current_rows(root: Path, day: int | None) -> list[dict]:
    blocks = site_metrics.roadmap_blocks(root.parent / "roadmap-180-days.md")
    selected = [day] if day is not None else list(range(1, 181))
    rows = []
    for number in selected:
        rows.append(site_metrics.measure_day(
            number,
            root / "days" / f"day-{number:03d}.html",
            root / "content" / f"day-{number:03d}-page.html",
            blocks[number],
        ))
    return rows


def main(argv=None, *, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day", type=int, choices=range(1, 181))
    parser.add_argument("--strict", action="store_true", help="Exit nonzero for any page below its block floor")
    args = parser.parse_args(argv)
    results = [evaluate(row) for row in current_rows(root, args.day)]
    failures = [result for result in results if not result["passes"]]
    if args.day is not None and not failures:
        print(format_result(results[0], "PASS"))
    else:
        status = "FAIL" if args.strict else "WARN"
        for result in failures:
            print(format_result(result, status))
    print(f"Depth summary: {len(results) - len(failures)} pass, {len(failures)} below floor; strict={'yes' if args.strict else 'no'}")
    return int(args.strict and bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
