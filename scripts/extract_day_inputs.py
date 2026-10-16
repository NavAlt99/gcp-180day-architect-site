#!/usr/bin/env python3
"""Extract exactly one day's canonical inputs; fail before writing on missing input."""
import argparse
import csv
import io
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def section(text, day, level, name):
    pattern = re.compile(r'^' + '#' * level + r'\s+Day\s+(\d+)\s+[—–-].*$', re.M)
    headings = list(pattern.finditer(text))
    matches = [i for i, m in enumerate(headings) if int(m.group(1)) == day]
    if len(matches) != 1:
        raise ValueError(f'{name}: expected one Day {day} heading, found {len(matches)}')
    i = matches[0]
    value = text[headings[i].start():headings[i+1].start() if i+1 < len(headings) else len(text)].strip()
    if not text[headings[i].end():headings[i+1].start() if i+1 < len(headings) else len(text)].strip():
        raise ValueError(f'{name}: Day {day} section is empty')
    return value


def extract(day, root=ROOT):
    roadmap = section((root.parent / 'roadmap-180-days.md').read_text(), day, 3, 'roadmap')
    brief = section((root.parent / 'gcp-architect-180-day-page-prompts.md').read_text(), day, 2, 'compact brief')
    with (root / 'data/coverage.csv').open(newline='') as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        rows = [r for r in reader if int(r['day']) == day]
    if not rows or any(not r.get('topic_key') or not r.get('topic') for r in rows):
        raise ValueError(f'coverage.csv: Day {day} rows missing or empty')
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    return f'# Day {day} inputs\n\n## Roadmap entry\n\n{roadmap}\n\n## Compact brief\n\n{brief}\n\n## Coverage rows\n\n```csv\n{output.getvalue()}```\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day', type=int, required=True, choices=range(1, 181))
    args = parser.parse_args()
    try:
        content = extract(args.day)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'ERROR extracting Day {args.day}: {exc}; no output written\n')
    target = ROOT / 'scratch' / f'day-{args.day:03d}-inputs.md'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    print(target)


if __name__ == '__main__':
    main()
