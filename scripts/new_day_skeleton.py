#!/usr/bin/env python3
"""Create an unfinished single-file specification; never overwrite authored input."""
from __future__ import annotations

import argparse
import csv
from html import escape
from pathlib import Path
from pprint import pformat

SITE = Path(__file__).resolve().parents[1]


def skeleton(day: int) -> dict:
    with (SITE / 'data/coverage.csv').open(newline='', encoding='utf-8') as stream:
        rows = [row for row in csv.DictReader(stream) if int(row['day']) == day]
    if not rows:
        raise ValueError(f'No coverage rows for Day {day}')
    topics, overviews = [], []
    for row in rows:
        key, title = row['topic_key'], row['topic']
        anchors = {part: row[f'{part}_anchor'] for part in ('overview', 'technical', 'problem', 'lab')}
        if any(anchor != f'{key}-{part}' for part, anchor in anchors.items()):
            raise ValueError(f'Engine key-derived anchors differ from coverage for {key}')
        overviews.append(f'<article class="topic-card overview" id="{anchors["overview"]}">'
                         f'<h3>{escape(title)}</h3><p><strong class="keyword">TODO: key term</strong> TODO: explanation.</p>'
                         '<p><strong class="side-heading">Why today:</strong> TODO: scope and position.</p>'
                         '<p class="problem-preview">TODO: concrete symptom. TODO: user/business effect.</p></article>')
        topics.append({
            'key': key, 'title': title, 'anchors': anchors,
            'overview': 'TODO: definition, why today, where it sits',
            'preview': 'TODO: concrete symptom. TODO: user/business effect.',
            'technical': '<h4>TODO: subtopic</h4><p><strong class="side-heading">What it is in general:</strong> '
                         '<strong class="keyword">TODO: term</strong> TODO: list ALL subtopics, then define/mechanism/example, '
                         'architect/GCP relevance with sources, concrete example and Evidence limit.</p>',
            'questions': ['TODO: topic-specific architectural question'],
            'reference': 'TODO: verify ' + row['publisher_url'], 'reference_label': 'TODO: verified source label and access date',
            'scenario': {field: 'TODO: '+field for field in (
                'scenario', 'impact', 'constraints', 'evidence', 'root', 'verify', 'residual',
                'diagram_enabled', 'facts', 'inference', 'expected')},
            'lab': {field: 'TODO: topic-specific '+field for field in (
                'name', 'goal', 'expected', 'mode', 'prereq', 'preflight', 'verification', 'trouble', 'cleanup', 'accept')},
        })
        topics[-1]['lab']['file'] = f'day-{day:03d}-{key}.md'
        topics[-1]['scenario'].update(diagnostic_steps=['TODO: diagnostic action'],
                                      remediation_steps=['TODO: fix action'])
        topics[-1]['lab']['steps'] = [f'**Stage {i}: TODO: stage name**\n\n**Location:** TODO: environment.\n\n'
                                     '**Actions:** TODO: ordered commands/file contents or exact manual steps.\n\n'
                                     '**Expected result:** TODO: observable outcome.\n\n**Save:** TODO: evidence path.'
                                     for i in range(1, 9)]
    return {'day': day, 'work_block': 'TODO: work block', 'topics': topics,
            'lab_defaults': {},
            'part1_html': '\n'.join(overviews),
            **{f'part{i}_intro': 'TODO: day-specific introduction' for i in range(1, 5)},
            'exit_summary': 'TODO: exact roadmap exit evidence', 'completion_html': 'TODO: acceptance and progress controls',
            'arch_diagram': {}, 'arch_svg_html': '', 'arch_table_html': '',
            'sources': {row['topic_key']: ('TODO: label', 'TODO: verified primary URL') for row in rows},
            'access_date': 'TODO: access date'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day', type=int, required=True, choices=range(1, 181))
    parser.add_argument('--output', type=Path, help='Optional new scratch fixture; existing paths are refused')
    args = parser.parse_args()
    destination = args.output or SITE / 'scratch' / f'day_data_{args.day:03d}.py'
    try:
        data = skeleton(args.day)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('x', encoding='utf-8') as stream:
            stream.write('"""Unfinished coverage-based spec. Replace every TODO; see SPEC_SCHEMA.md.\n'
                         'Empty architecture fields are deliberate: author only eligible flows.\n"""\n\nSOURCES = ')
            sources = data.pop('sources')
            access_date = data.pop('access_date')
            stream.write('{}\nACCESS_DATE = {!r}\nDATA = '.format(
                pformat(sources, width=105, sort_dicts=False), access_date))
            stream.write(pformat(data, width=105, sort_dicts=False))
            stream.write('\nDATA.update(sources=SOURCES, access_date=ACCESS_DATE)\n')
    except (FileExistsError, ValueError) as error:
        parser.error(str(error))
    print(f'Created unfinished Day {args.day} spec: {destination}')


if __name__ == '__main__':
    main()
