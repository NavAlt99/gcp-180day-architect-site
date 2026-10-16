"""Focused fidelity checks: v2 required fields fail, historical specs warn."""
import ipaddress
import re
import subprocess
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

TOOLS = ('ping', 'openssl', 'curl', 'dig', 'nslookup', 'ip', 'ss', 'tcpdump', 'traceroute', 'nc')
MODES = ('Observed locally:', 'Simulated or predicted:', 'Untested on GCP:')
ALLOWED = tuple(ipaddress.ip_network(n) for n in (
    '192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24', '10.0.0.0/8',
    '172.16.0.0/12', '192.168.0.0/16', '127.0.0.0/8', '169.254.0.0/16',
    '2001:db8::/32', '::1/128', 'fe80::/10'))


def leaves(value, path='spec'):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from leaves(item, f'{path}.{key}')
    elif isinstance(value, (list, tuple)):
        for i, item in enumerate(value):
            yield from leaves(item, f'{path}[{i}]')


def code(text):
    html = BeautifulSoup(text, 'html.parser')
    return '\n'.join(re.findall(r'```[^\n]*\n(.*?)```', text, re.S) +
                     [p.get_text() for p in html.select('pre')])


TEMPLATE_PATTERNS = (
    'CEL Attribute Rule',
    'Cryptographic Check',
    'Boundary under study',
    'Protocol: HTTPS / TLS 1.3',
    'TIERED PIPELINE',
)


def figure_titles(html):
    document = BeautifulSoup(html, 'html.parser')
    titles = []
    for s in document.select('svg[role="img"]'):
        s_raw = str(s)
        t = s.title.get_text(' ', strip=True) if s.title else '(untitled figure)'
        if any(p in s_raw for p in TEMPLATE_PATTERNS) or re.search(r'Day \d+ foundation path', t, re.I):
            continue
        titles.append(t)
    return titles


def check(data, rows=(), allowlist=()):
    errors, warnings = [], []
    strict = data.get('contract_version', 1) == 2
    def required(field, reason):
        (errors if strict else warnings).append(f'{"ERROR" if strict else "WARN"} {field}: {reason}')
    for field in ('roadmap_practice', 'roadmap_exit'):
        if not isinstance(data.get(field), str) or not data[field].strip():
            required(field, 'required non-empty verbatim roadmap field')
    for topic in data.get('topics', []):
        key = topic.get('key', 'unknown')
        lab = topic.get('lab', {})
        if not lab.get('covers') or isinstance(lab.get('covers'), str) and not lab['covers'].strip():
            required(f'{key}.lab.covers', 'name the Practice clause covered')
        for label in MODES:
            if label not in lab.get('mode', ''):
                required(f'{key}.lab.mode', f'missing {label}')
        stages = lab.get('steps', [])[:7]
        commands = '\n'.join(code(s) for s in stages)
        for i, stage in enumerate(stages, 1):
            if '|| true' in code(stage):
                required(f'{key}.lab.steps[{i-1}]', 'Stage 1-7 must not mask failures with || true')
        preflight = code(stages[0]) if stages else ''
        for tool in TOOLS:
            # Command position only, not prose, Python strings, or grep patterns.
            if re.search(r'(?:^|[\n;|&()]|\$\()\s*(?:(?:if|then|sudo|!)\s+)*' + tool + r'(?=\s|$)', commands) and not re.search(r'(?:^|[\n;|&])\s*(?:(?:if|!)\s+)*command\s+-v\s+' + tool + r'\b', preflight):
                warnings.append(f'WARN {key}.lab: external tool {tool} lacks command -v in Stage 1')
    urls = set()
    for field, text in leaves(data):
        evidence = [(field, text)] if re.search(r'\.(?:facts|caption|evidence)(?:\[|\.|$)', field) else []
        if '<figcaption' in text:
            evidence += [(field + f'.figcaption[{i}]', c.get_text(' ', strip=True))
                         for i, c in enumerate(BeautifulSoup(text, 'html.parser').select('figcaption'))]
        for evidence_field, value in evidence:
            if re.search(r'\b(proved|recorded|captured|observed)\b', value, re.I) and not re.search(r'\b(illustrative|supplied)\b', value, re.I):
                warnings.append(f'WARN {evidence_field}: observation language lacks illustrative or supplied qualifier')
        for literal in re.findall(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])|(?<![\w:])(?:[0-9a-fA-F]{0,4}:){2,}[0-9a-fA-F:.]*(?![\w:])', text):
            try:
                address = ipaddress.ip_address(literal)
            except ValueError:
                continue
            if str(address) not in allowlist and not any(address.version == n.version and address in n for n in ALLOWED):
                warnings.append(f'WARN {field}: address literal {literal} outside allowed example ranges')
        if '<a ' in text:
            for anchor in BeautifulSoup(text, 'html.parser').select('a[href]'):
                if anchor['href'].startswith('https://') and not re.search(r'\(accessed \d{4}-\d{2}-\d{2}\)', anchor.get_text(' ', strip=True)):
                    required(field + '.source_label', 'requires (accessed YYYY-MM-DD)')
        source_text = ''
        if '.sources.' in field or field.endswith('.reference'):
            source_text = text
        elif '<a ' in text:
            source_text = '\n'.join(a.get('href', '') for a in BeautifulSoup(text, 'html.parser').select('a[href]'))
        for url in re.findall(r'https://[^\s<>"\)]+', source_text):
            url = url.rstrip("',;")
            urls.add(url)
            if not urlsplit(url).fragment:
                warnings.append(f'WARN {field}: whole-document link {url}')
    sources = data.get('sources', {})
    for key, item in sources.items():
        label = item[0] if isinstance(item, (list, tuple)) else item.get('label', '') if isinstance(item, dict) else ''
        if not re.search(r'\(accessed \d{4}-\d{2}-\d{2}\)', label):
            required(f'sources.{key}.label', 'requires (accessed YYYY-MM-DD)')
    for topic in data.get('topics', []):
        if topic.get('reference') and not re.search(r'\(accessed \d{4}-\d{2}-\d{2}\)', topic.get('reference_label', '')):
            required(f'{topic.get("key")}.reference_label', 'requires (accessed YYYY-MM-DD)')
    for row in rows:
        if row.get('publisher_url') and row['publisher_url'] not in urls:
            warnings.append(f'WARN {row["topic_key"]}.publisher_url: coverage publisher_url not among spec source URLs')
    return errors, list(dict.fromkeys(warnings))


def file_checks(day, data, path, root):
    warnings = []
    files = list(path.glob('*.py')) if path.is_dir() else [path]
    if sum(p.stat().st_size for p in files) > 100 * 1024:
        warnings.append('WARN spec size: over 100 KB; use directory form for revisions')
    try:
        old = subprocess.run(['git', 'show', f'HEAD:days/day-{day:03d}.html'], cwd=root,
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return warnings + ['NOTE diagram comparison skipped: git or day file at HEAD unavailable']
    # Render only spec diagrams, never read current rendered files.
    from scripts.author_engine import render_architecture_svg, render_incident_svg
    from scripts.compact_flow import render_compact_flow
    markup = [text for _, text in leaves(data) if '<svg' in text]
    arch = data.get('arch_diagram', {})
    if arch and not data.get('arch_svg_html'):
        markup.append(render_architecture_svg(day, arch, data))
    for i, topic in enumerate(data.get('topics', []), 1):
        if topic.get('flow'):
            markup.append(render_compact_flow(f'check-topic-{i}', topic['flow']))
        scenario = topic.get('scenario', {})
        if scenario.get('diagram_enabled') and not scenario.get('incident_svg_html') and not scenario.get('svg_html'):
            markup.append(render_incident_svg(day, i, topic))
    new = '\n'.join(markup)
    previous, current = figure_titles(old), figure_titles(new)
    if len(current) < len(previous):
        missing = list(previous)
        for title in current:
            if title in missing: missing.remove(title)
        warnings.append('WARN diagram count below committed page; missing figure titles: ' + '; '.join(missing))
    return warnings
