#!/usr/bin/env python3
"""Generate review records from the durable spec and git; never invent reviews."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from scripts.validate_spec import load_spec, soup, strings
from scripts.author_engine import render_architecture_svg, render_incident_svg
from scripts.compact_flow import render_compact_flow


def git(*args, root=ROOT):
    return subprocess.run(['git', *args], cwd=root, text=True, capture_output=True, check=True).stdout


def visuals(data, day):
    markup = [text for _, text in strings(data) if '<svg' in text]
    arch = data.get('arch_diagram', {})
    if arch and not data.get('arch_svg_html') and not data.get('arch_diagram_html'):
        markup.append(render_architecture_svg(day, arch, data))
    for i, topic in enumerate(data.get('topics', []), 1):
        if topic.get('flow'): markup.append(render_compact_flow(f'handoff-topic-{i}', topic['flow']))
        scenario = topic.get('scenario', {})
        if scenario.get('diagram_enabled') and not scenario.get('incident_svg_html') and not scenario.get('svg_html'):
            markup.append(render_incident_svg(day, i, topic))
    result = {}
    for html in markup:
        for svg in soup(html).select('svg'):
            title = svg.select_one('title')
            name = title.get_text(' ', strip=True) if title else '(untitled figure)'
            result[name] = hashlib.sha256(str(svg).encode()).hexdigest()
    return result


def old_spec(path, root=ROOT):
    relative = path.relative_to(root).as_posix()
    with tempfile.TemporaryDirectory(prefix='handoff-spec-') as temporary:
        target = Path(temporary) / path.name
        if path.is_dir():
            target.mkdir()
            files = git('ls-tree', '-r', '--name-only', 'HEAD', '--', relative, root=root).splitlines()
            if not files: raise ValueError('No committed spec baseline')
            for name in files:
                dest = target / Path(name).relative_to(relative)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(git('show', f'HEAD:{name}', root=root))
        else:
            target.write_text(git('show', f'HEAD:{relative}', root=root))
        return load_spec(target)[0]


def generate(day, path, root=ROOT):
    data, _, metadata = load_spec(path)
    data = {**metadata, **data}
    lines = [f'# Day {day:03d} handoff', '', 'Generated from the durable spec and git HEAD. Missing review evidence remains explicit.', '',
             '## Practice-to-lab map', '', f"Practice: {data.get('roadmap_practice', 'UNRECORDED')}",
             f"Exit: {data.get('roadmap_exit', 'UNRECORDED')}", '']
    for topic in data.get('topics', []):
        lab = topic.get('lab', {})
        lines.append(f"- {topic['key']} / {lab.get('name', topic['title'])}: {lab.get('covers', 'UNRECORDED Practice clause')}; artifact: {lab.get('file', 'UNRECORDED')}")
    sources = {}
    for key, source in data.get('sources', {}).items():
        if isinstance(source, (list, tuple)) and len(source) >= 2: sources[source[1]] = source[0]
        elif isinstance(source, dict): sources[source.get('url', '')] = source.get('label', key)
    for _, text in strings(data):
        if text.startswith('https://'): sources.setdefault(text, '(no source label)')
        for a in soup(text).select('a[href^="https://"]'):
            sources.setdefault(a['href'], a.get_text(' ', strip=True))
    review = data.get('review_records', {})
    ledger = review.get('source_ledger', {})
    lines += ['', '## Source ledger', '']
    for url, label in sorted(sources.items()):
        record = ledger.get(url, {})
        parsed = urlsplit(url)
        scope = f'fragment: {parsed.fragment}' if parsed.fragment else 'whole-document reason: ' + record.get('whole_document_reason', 'UNRECORDED')
        lines.append(f"- {label} — {url}; {scope}; heading actually opened: {record.get('heading_opened', 'UNRECORDED')}; RFC status: {record.get('rfc_status', 'UNRECORDED' if 'rfc-editor.org' in url else 'not applicable')}")
    lines += ['', '## Product-claim list', '', 'GCP relevance passages are extracted as claim candidates; section support requires manual review.', '']
    for topic in data.get('topics', []):
        doc = soup(topic.get('technical', ''))
        for paragraph in doc.select('p'):
            if 'Relevance to GCP:' in paragraph.get_text():
                links = [a['href'] for a in paragraph.select('a[href]')]
                heading = paragraph.find_previous(['h3', 'h4', 'h5', 'h6'])
                if heading:
                    for sibling in heading.next_siblings:
                        if getattr(sibling, 'name', None) in ('h3', 'h4', 'h5', 'h6'): break
                        for anchor in soup(str(sibling)).select('a[href]'):
                            if 'cloud.google.com' in urlsplit(anchor['href']).netloc:
                                links.append(anchor['href'])
                links = list(dict.fromkeys(links))
                lines.append(f"- {topic['key']}: {paragraph.get_text(' ', strip=True)} Cited supporting sections in subtopic (support unreviewed): {', '.join(links) or 'UNRECORDED'}")
    for claim in review.get('product_claims', []):
        lines.append('- Explicit reviewed claim: ' + json.dumps(claim, ensure_ascii=False))
    current = visuals(data, day)
    try:
        previous = visuals(old_spec(path, root), day)
        comparison_error = None
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        previous, comparison_error = {}, str(exc)
    reasons = review.get('visual_reasons', {})
    lines += ['', '## Visuals list', '']
    if comparison_error: lines.append('Baseline unavailable: ' + comparison_error)
    for name in sorted(current.keys() | previous.keys()):
        change = ('baseline unavailable' if comparison_error else 'addition' if name not in previous else
                  'removal' if name not in current else 'replacement' if current[name] != previous[name] else 'unchanged')
        reason = 'retained from committed spec' if change == 'unchanged' else reasons.get(name, 'UNRECORDED reason')
        lines.append(f'- {name}: {change}; reason: {reason}')
    if not current and not previous: lines.append('- No spec visuals.')
    relative = path.relative_to(root).as_posix()
    lines += ['', '## Spec diff stat', '', '```text']
    try:
        stat = git('diff', 'HEAD', '--stat', '--', relative, root=root)
        tracked = git('ls-files', '--', relative, root=root).strip()
        if not tracked: stat += 'UNTRACKED spec: not included in git diff HEAD; review required.\n'
        lines.append(stat.strip() or 'No spec diff against HEAD.')
        # Report actual removed source lines; do not claim they are non-explanatory.
        diff = git('diff', 'HEAD', '--', relative, root=root)
        removed = sum(line.startswith('-') and not line.startswith('---') for line in diff.splitlines())
        prose = 'No source lines removed.' if removed == 0 and tracked else f'{removed} source lines removed; manual no-explanatory-prose-removal review required.'
    except (OSError, subprocess.CalledProcessError) as exc:
        lines.append(f'UNVERIFIED git diff: {exc}'); prose = 'UNVERIFIED prose-removal review.'
    lines += ['```', '', prose, '']
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day', required=True, type=int, choices=range(1, 181))
    args = parser.parse_args(argv)
    directory = ROOT / 'scratch' / f'day_data_{args.day:03d}'
    path = directory if directory.is_dir() else directory.with_suffix('.py')
    output = ROOT / 'scratch/handoffs' / f'day-{args.day:03d}.md'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generate(args.day, path) + '\n')
    print(output)
    return 0


if __name__ == '__main__': raise SystemExit(main())
