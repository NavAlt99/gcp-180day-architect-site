"""Read-only authored-spec checks; no compiler, build, or rendered-page traversal."""
import argparse
import ast
import csv
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.author_engine import find_todo, load_day_module, render_code_blocks, render_architecture_svg
from scripts.compact_flow import render_compact_flow
from bs4 import BeautifulSoup

# Kept identical to validate.py's inline-command pattern (tested for drift).
COMMAND_PATTERN = r"^(?:sudo |git |gcloud |terraform |kubectl |docker |python3? |curl |ssh |cat |printf |mkdir |cd |pwd$|ls(?: |$)|command |ip |dig |nslookup |systemctl |journalctl )"
LABELS = ('What it is in general:', 'Relevance to a cloud architect:', 'Relevance to GCP:')


def coverage(day):
    with (ROOT / 'data/coverage.csv').open(newline='') as stream:
        return [r for r in csv.DictReader(stream) if int(r['day']) == day]


def strings(value, path='spec'):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from strings(item, f'{path}.{key}')
    elif isinstance(value, (list, tuple)):
        for i, item in enumerate(value):
            yield from strings(item, f'{path}[{i}]')


def soup(text):
    return BeautifulSoup(render_code_blocks(text), 'html.parser')


def metrics(topic):
    tech = soup(topic.get('technical', ''))
    steps = topic.get('lab', {}).get('steps', [])
    return (len(tech.get_text(' ', strip=True)), len(tech.select('h3,h4,h5,h6')), len(steps),
            sum(len(soup(s).get_text(' ', strip=True)) for s in steps))


def depth_ranges():
    """Per-topic min/max metrics from the read-only Day 4 durable spec."""
    baseline, _, _ = load_spec(ROOT / 'scratch/day_data_004.py')
    return tuple((min(values), max(values)) for values in
                 zip(*(metrics(topic) for topic in baseline['topics'])))


def sentence_count(text):
    text = soup(text).get_text(' ', strip=True)
    # Decimal numbers/IPs and common abbreviations are not sentence boundaries.
    text = re.sub(r'\b(?:e\.g\.|i\.e\.|Mr\.|Dr\.)', 'abbr', text)
    return len([s for s in re.split(r'[.!?]+(?:\s+|$)', text) if s.strip()])


def load_spec(path):
    """Engine data plus literal module metadata, never engine compilation."""
    data = load_day_module(path)
    source = path / 'meta.py' if path.is_dir() else path
    tree = ast.parse(source.read_text())
    names = {target.id for node in tree.body if isinstance(node, ast.Assign)
             for target in node.targets if isinstance(target, ast.Name)}
    legacy = not bool(names & {'DATA', 'DAY_DATA'})
    metadata = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ('ACCESS_DATE', 'SOURCES'):
                    try:
                        metadata[target.id.lower()] = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        pass
    return data, legacy, metadata


def validate_data(day, data, *, legacy=False, metadata=None, reference=None):
    errors, warnings = [], []
    metadata = metadata or {}
    contract_v2 = (data.get('contract_version') or metadata.get('contract_version', 1)) == 2
    def error(key, field, reason):
        errors.append(f'ERROR {key} {field}: {reason}')
    def p1_issue(key, field, reason):
        if contract_v2:
            error(key, field, reason)
        else:
            warnings.append(f'WARN {key} {field}: {reason}')
    def diagrams(key, field, markup):
        document = soup(markup)
        for svg in document.select('svg'):
            if not svg.select_one('path,rect,circle,line,polyline,polygon,ellipse,image,use'):
                error(key, field, 'empty SVG diagram/placeholder')
            title, desc = svg.select_one('title[id]'), svg.select_one('desc[id]')
            if not svg.has_attr('viewbox') or svg.get('role') != 'img' or not title or not desc:
                error(key, field, 'SVG requires viewBox, role=img, and title/desc IDs')
            labelled = svg.get('aria-labelledby', '').split()
            if not title or not desc or title.get('id') not in labelled or desc.get('id') not in labelled or any(not document.find(id=target) for target in labelled):
                error(key, field, 'SVG title/desc IDs must resolve through aria-labelledby')
            figure = svg.find_parent('figure')
            if not figure or not figure.select_one('figcaption') or not figure.select_one('figcaption').get_text(strip=True):
                error(key, field, 'SVG requires a non-empty figcaption')
            for image in svg.select('image,use'):
                href = image.get('href', image.get('xlink:href', ''))
                if href.startswith('#'):
                    if not document.find(id=href[1:]): error(key, field, 'SVG icon reference does not resolve')
                else:
                    path = (ROOT / 'days' / href.split('#')[0]).resolve()
                    if not href or not path.is_relative_to(ROOT / 'assets/icons') or not path.is_file():
                        error(key, field, 'SVG icon must exist locally under assets/icons')
        for wrapper in document.select('.diagram-container'):
            if not wrapper.select_one('svg'):
                error(key, field, 'empty diagram wrapper/placeholder')
        for heading in document.select('h3,h4,h5,h6'):
            if re.fullmatch(r'(?:technical |incident |architecture )?diagram', heading.get_text(strip=True), re.I):
                following = []
                for sibling in heading.next_siblings:
                    if getattr(sibling, 'name', None) in ('h3', 'h4', 'h5', 'h6'): break
                    following.append(str(sibling))
                if not soup(''.join(following)).select_one('svg'):
                    error(key, field, 'empty diagram heading/placeholder')
    def authored(key, obj, field, prefix=''):

        if field not in obj or not obj[field]:
            error(key, prefix + field, 'engine fallback would insert generic prose; supply an authored value')
    topics = data.get('topics', [])
    for key, value in [('day', {k: v for k, v in data.items() if k != 'topics'}),
                       *[(t.get('key', f'index-{i}'), t) for i, t in enumerate(topics)]]:
        # Reuse the engine recursive scanner on each leaf/key to report all TODOs.
        def todos(item, path):
            if isinstance(item, dict):
                for k, v in item.items():
                    if find_todo(str(k)):
                        error(key, f'{path}.{k}', 'TODO: in field key')
                    todos(v, f'{path}.{k}')
            elif isinstance(item, (tuple, list)):
                for i, v in enumerate(item): todos(v, f'{path}[{i}]')
            elif find_todo(item, path):
                error(key, path, 'unfinished TODO:')
        todos(value, 'spec' if key == 'day' else 'topic')
    key = 'day'
    todos(metadata, 'metadata')
    rows = {r['topic_key']: r for r in coverage(day)}
    keys = [t.get('key') for t in topics]
    for key in rows.keys() - set(keys): error(key, 'key', 'missing coverage topic')
    for topic in topics:
        key = topic.get('key', 'unknown')
        row = rows.get(key)
        if row is None: error(key, 'key', 'extra topic not in coverage')
        elif keys.count(key) > 1: error(key, 'key', 'duplicate coverage topic')
        if row:
            if topic.get('title') != row['topic']: error(key, 'title', 'does not match coverage')
            for part in ('overview', 'technical', 'problem', 'lab'):
                expected = row[f'{part}_anchor']
                explicit = topic.get('anchors', {}).get(part, topic.get(f'{part}_anchor', f'{key}-{part}'))
                if explicit != expected: error(key, f'anchors.{part}', 'does not match coverage')
        scenario, lab = topic.get('scenario', {}), topic.get('lab', {})
        if type(scenario.get('diagram_enabled')) is not bool:
            error(key, 'scenario.diagram_enabled', 'required boolean missing or invalid')
        steps = lab.get('steps', [])
        if len(steps) != 8: error(key, 'lab.steps', 'requires exactly eight steps')
        for i, step in enumerate(steps):
            text = soup(step).get_text('\n', strip=True)
            # Markdown bold labels become separate text nodes; normalize whitespace.
            flat = re.sub(r'\s+', ' ', text)
            field = f'lab.steps[{i}]'
            for marker in ('Location:', 'Expected result:', 'Save:'):
                if marker not in flat: error(key, field, f'missing {marker} marker')
            location = re.search(r'Location:\s*(.*?)(?:Expected result:|Save:|$)', flat, re.I)
            if location:
                line = re.search(r'Location:\s*([^\n]+)', re.sub(r'\*\*|<[^>]+>', '', step), re.I)
                env = line.group(1).strip() if line else location.group(1)
                recognized = re.match(r'(?:local(?: [\w-]+){0,3} terminal|Cloud Shell|GCP VM terminal|Console|local/tabletop worksheet|local worksheet|tabletop worksheet)\b', env, re.I)
                if not recognized: error(key, field, 'Location is not a recognised environment')
            body = re.sub(r'^.*?(?:Location:[^\n]*\n)', '', re.sub(r'\*\*', '', step), flags=re.S)
            body = re.split(r'Expected result:|Save:', body)[0].strip()
            has_code = bool(soup(body).select('pre code'))
            manual = bool(re.search(r'(?:^|\n)\s*\d+[.)]\s+\S', body))
            if not has_code and not manual:
                error(key, field, 'missing command/file-content or numbered manual-step body')
        if not legacy:
            for field in ('title', 'reference_label'): authored(key, topic, field)
            for field in ('mode', 'prereq', 'preflight', 'trouble', 'cleanup'): authored(key, lab, field, 'lab.')
            raw = scenario.get('incident_svg_html') or scenario.get('svg_html')
            if scenario.get('diagram_enabled') is not False and not raw and not scenario.get('flow'):
                for field in ('diagram', 'facts', 'inference', 'expected'): authored(key, scenario, field, 'scenario.')
        tech = soup(topic.get('technical', ''))
        headings = tech.select('h3,h4,h5,h6')
        listing = tech.find(['ol', 'ul'])
        intro = tech.get_text(' ', strip=True)
        first = tech.find(['p', 'ol', 'ul', 'h3', 'h4', 'h5', 'h6'])
        lead = first.get_text(' ', strip=True) if first else ''
        listed = [li.get_text(' ', strip=True) for li in listing.select('li')] if listing else []
        if not listing and lead.startswith('Subtopics in this discussion:'):
            listed = lead.split(':', 1)[1].strip().split(';')
        if not listed or not lead.startswith('Subtopics in this discussion:') or (listing and headings and list(tech.descendants).index(listing) > list(tech.descendants).index(headings[0])):
            error(key, 'technical', 'missing subtopic list at the start')
        normalize = lambda text: text.strip().rstrip('.').casefold()
        if not headings or list(map(normalize, listed)) != [normalize(h.get_text(' ', strip=True)) for h in headings]:
            error(key, 'technical', 'subtopic list must match all subtopic headings in order')
        for heading in headings:
            region = []
            for sibling in heading.next_siblings:
                if getattr(sibling, 'name', None) in ('h3', 'h4', 'h5', 'h6'): break
                region.append(str(sibling))
            text = soup(''.join(region)).get_text(' ', strip=True)
            for label in LABELS:
                if label not in text: error(key, 'technical', f'{heading.get_text(strip=True)} missing {label}')
        for label in ('Concrete example:', 'Evidence limit:'):
            if label not in intro: error(key, 'technical', f'missing {label}')
        preview = topic.get('preview', '')
        if data.get('part1_html'):
            card = soup(data['part1_html']).find(id=f'{key}-overview')
            if not card:
                error(key, 'anchors.overview', 'Part 1 HTML missing coverage anchor')
            else:
                side_headings = [re.sub(r'\s+', ' ', h.get_text().strip()) for h in card.select('strong.side-heading')]
                if any(re.search(r'why today.*where it sits|where it sits.*why today|\bcombined\b', s, re.I) for s in side_headings):
                    p1_issue(key, 'part1', 'combined Why today / Where it sits label not permitted')
                has_why = any(s == 'Why today:' or s.startswith('Why today:') for s in side_headings)
                has_where = any(s == 'Where it sits:' or s.startswith('Where it sits:') for s in side_headings)
                has_prev = any(s == 'Problem preview:' or s.startswith('Problem preview:') for s in side_headings)
                if not has_why:
                    p1_issue(key, 'part1', 'missing <strong class="side-heading">Why today:</strong>')
                if not has_where:
                    p1_issue(key, 'part1', 'missing <strong class="side-heading">Where it sits:</strong>')
                if not has_prev:
                    p1_issue(key, 'part1', 'missing <strong class="side-heading">Problem preview:</strong>')
                if has_why and has_where and has_prev:
                    why_idx = next(i for i, s in enumerate(side_headings) if s == 'Why today:' or s.startswith('Why today:'))
                    where_idx = next(i for i, s in enumerate(side_headings) if s == 'Where it sits:' or s.startswith('Where it sits:'))
                    prev_idx = next(i for i, s in enumerate(side_headings) if s == 'Problem preview:' or s.startswith('Problem preview:'))
                    if not (why_idx < where_idx < prev_idx):
                        p1_issue(key, 'part1', 'Part 1 labels out of order; expected Why today:, Where it sits:, Problem preview:')
                paragraph = card.select_one('.problem-preview')
                if paragraph:
                    preview = paragraph.get_text(' ', strip=True)
                    preview = re.sub(r'^Problem preview:\s*', '', preview)
                else:
                    error(key, 'preview', 'Part 1 HTML missing problem-preview')
        else:
            p1_issue(key, 'part1_html', 'Part 1 HTML missing')
        if sentence_count(preview) != 2:
            error(key, 'preview', 'Part 1 requires exactly two sentences')
        if topic.get('reference_label', '').startswith('TODO: verify'):
            error(key, 'reference_label', 'unverified source label')
        url = topic.get('reference', '')
        if url.startswith('TODO: verify') or urlsplit(url).scheme != 'https':
            error(key, 'reference', 'requires verified metadata and https URL')
        incident_fields = ('flow', 'incident_svg_html', 'svg_html', 'diagram', 'icons')
        if scenario.get('diagram_enabled') is False and any(f in scenario for f in incident_fields):
            error(key, 'scenario', 'diagram present with diagram_enabled False')
        if scenario.get('diagram_enabled') is True and not any(scenario.get(f) for f in incident_fields[:-1]):
            error(key, 'scenario', 'diagram_enabled True requires incident diagram data')
        technical_diagram = bool(topic.get('flow') or tech.select('svg'))
        if technical_diagram:
            warnings.append(f'WARN {key} technical diagram present; confirm it is a multi-step sequence, packet traversal or request/response lifecycle (manual eligibility review)')
        if reference:
            values = metrics(topic)
            for name, value, bounds in zip(('technical text length', 'subtopic count', 'lab stage count', 'stage text length'), values, reference):
                minimum, maximum = bounds if isinstance(bounds, (tuple, list)) else (bounds, bounds)
                if value < minimum * .5:
                    warnings.append(f'WARN {key} depth: {name} {value} far below Day 4 range {minimum}–{maximum}; signal only, not a quality threshold')
    if not legacy:
        for field in ('part1_intro', 'part2_intro', 'part3_intro', 'part4_intro', 'exit_summary'):
            if field == 'part1_intro' and data.get('part1_html'): continue
            if field == 'exit_summary' and data.get('completion_html'): continue
            authored('day', data, field)
        arch = data.get('arch_diagram', {})
        if isinstance(arch, dict) and arch and not data.get('arch_svg_html') and not data.get('arch_diagram_html') and not arch.get('flow') and 'steps' not in arch:
            for field in ('title', 'desc', 'caption', 'nodes'): authored('day', arch, field, 'arch_diagram.')
    access = data.get('access_date') or metadata.get('access_date')
    if not access: error('day', 'access_date', 'missing source access date')
    for field, value in strings(data.get('sources', metadata.get('sources', {}))):
        if value.startswith('TODO: verify'): error('day', field, 'unverified source metadata')
        if (field.endswith('[1]') or field.endswith('.url') or re.match(r'^[a-zA-Z][\w+.-]*://', value)) and urlsplit(value).scheme != 'https': error('day', field, 'source URL scheme must be https')
    all_soup = soup('\n'.join(v for _, v in strings(data)))
    for cls in ('keyword', 'side-heading'):
        if not all_soup.select_one(f'strong.{cls}'): error('day', 'markup', f'missing strong.{cls}')
    for element in all_soup.select('strong.keyword'):
        if element.find_parent(['pre', 'code']): error('day', 'markup', 'keyword inside pre/code')
    for code in all_soup.select('code'):
        if not code.find_parent('pre') and re.match(COMMAND_PATTERN, code.get_text(' ', strip=True)):
            error('day', 'markup', 'inline command must use kbd instead of code')
    for field, value in strings(data):
        if '<svg' in value or 'diagram-container' in value or re.search(r'<h[3-6][^>]*>[^<]*diagram', value, re.I):
            match = re.search(r'\.topics\[(\d+)\]', field)
            owner = topics[int(match.group(1))].get('key', 'unknown') if match else 'day'
            diagrams(owner, field, value)
    architecture = data.get('arch_diagram')
    if isinstance(architecture, dict) and architecture and not data.get('arch_svg_html') and not data.get('arch_diagram_html'):
        if not architecture.get('flow') and 'steps' not in architecture:
            if not architecture.get('nodes') and not architecture.get('components'):
                error('day', 'arch_diagram', 'empty diagram data/placeholder')
            try:
                diagrams('day', 'arch_diagram', render_architecture_svg(day, architecture, data))
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                error('day', 'arch_diagram', f'diagram structure: {exc}')
    if data.get('arch_diagram') or data.get('arch_svg_html') or data.get('arch_diagram_html'):
        warnings.append('WARN day technical diagram present; confirm it is a multi-step sequence, packet traversal or request/response lifecycle (manual eligibility review)')
    def flows(value, field='spec'):
        if isinstance(value, dict):
            if 'nodes' in value and 'steps' in value:
                try:
                    rendered = render_compact_flow('validation-flow', value)
                    diagrams('day', field, rendered)
                except (KeyError, TypeError, ValueError) as exc:
                    error('day', field, f'compact flow structure: {exc}')
                for i, node in enumerate(value['nodes']):
                    icon = node.get('icon', '')
                    path = (ROOT / 'days' / icon).resolve()
                    if not path.is_relative_to(ROOT / 'assets/icons') or not path.is_file():
                        error('day', f'{field}.nodes[{i}].icon', 'compact flow icon must exist locally under assets/icons')
            for k, v in value.items(): flows(v, f'{field}.{k}')
        elif isinstance(value, (list, tuple)):
            for i, v in enumerate(value): flows(v, f'{field}[{i}]')
    flows(data)
    from scripts.spec_v2_checks import check
    allow_path = ROOT / 'data/address_allowlist.txt'
    allow = [line.split()[0] for line in allow_path.read_text().splitlines()
             if line.strip() and not line.lstrip().startswith('#')] if allow_path.exists() else []
    strict_errors, strict_warnings = check({**metadata, **data}, list(rows.values()), allow)
    return errors + strict_errors, warnings + strict_warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day', type=int, required=True, choices=range(1, 181))
    parser.add_argument('--spec', type=Path)
    args = parser.parse_args(argv)
    directory = ROOT / 'scratch' / f'day_data_{args.day:03d}'
    path = args.spec or (directory if directory.is_dir() else directory.with_suffix('.py'))
    try:
        data, legacy, metadata = load_spec(path)
        reference = depth_ranges()
        errors, warnings = validate_data(args.day, data, legacy=legacy, metadata=metadata, reference=reference)
        from scripts.spec_v2_checks import file_checks
        if path.exists():
            warnings.extend(file_checks(args.day, data, path, ROOT))
    except Exception as exc:
        errors, warnings, legacy = [f'ERROR day spec: {type(exc).__name__}: {exc}'], [], False
    for line in errors[:30]: print(line.replace('\n', ' '))
    for line in warnings: print(line)
    if legacy:
        print('INFO legacy: generic-prose fallback presence checks do not apply; all other checks apply and existing engine builds remain unchanged.')
    print(f'Summary: {len(errors)} errors ({min(30, len(errors))} shown), {len(warnings)} warnings; source relevance, technical accuracy and visual clarity require manual review.')
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
