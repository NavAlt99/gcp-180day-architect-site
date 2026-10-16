"""Shared structure only: caller owns every explanation, source and lab context.

Functions preserve Day 002 byte output. No topic-specific teaching defaults.
"""
from html import escape
from textwrap import dedent
from scripts.author_engine import LAB_DEFAULTS

def source(key, *, sources):
    label, url = sources[key]
    return f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'


def keyword(term):
    return f'<strong class="keyword">{escape(term)}</strong>'


def subtopic(title, general, architect, gcp, refs, *, sources, access_date):
    return f'''\n<h4>{escape(title)}</h4>
<p><strong class="side-heading">What it is in general:</strong> {general}</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> {architect}</p>
<p><strong class="side-heading">Relevance to GCP:</strong> {gcp}</p>
<p><strong class="side-heading">Further study:</strong> {'; '.join(source(k, sources=sources) for k in refs)}. Accessed {access_date}.</p>\n'''


def discussion(titles, sections, example, limit):
    return '<p><strong class="side-heading">Subtopics in this discussion:</strong></p><ol>' + ''.join(
        f'<li>{escape(t)}</li>' for t in titles
    ) + '</ol>\n' + ''.join(sections) + f'''\n<p><strong class="side-heading">Concrete example:</strong> {example}</p>
<p><strong class="side-heading">Evidence limit:</strong> {limit}</p>'''


def flow_svg(uid, title, nodes, transitions, caption):
    """A focused six-node sequence, arranged as two rows of three (snake order)."""
    positions = [(30, 80), (420, 80), (810, 80), (810, 310), (420, 310), (30, 310)]
    cards = []
    for i, (label, detail, icon) in enumerate(nodes):
        x, y = positions[i]
        cards.append(f'''<g transform="translate({x},{y})"><rect width="280" height="110" rx="10" fill="#121526" stroke="#38bdf8"/>
<image href="../assets/icons/generic/{icon}.svg" x="15" y="17" width="30" height="30" preserveAspectRatio="xMidYMid meet"/>
<text x="54" y="35" fill="#7dd3fc" font-size="16" font-weight="700">{i+1}. {escape(label)}</text>
<text x="16" y="70" fill="#e2e8f0" font-size="14">{escape(detail[0])}</text>
<text x="16" y="92" fill="#e2e8f0" font-size="14">{escape(detail[1])}</text></g>''')
    arrows = []
    for i, (x1, y1, x2, y2, tx, ty) in enumerate([
        (310,135,410,135,360,118), (700,135,800,135,750,118),
        (950,190,950,300,950,248), (810,365,710,365,760,348), (420,365,320,365,370,348),
    ]):
        arrows.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#38bdf8" stroke-width="2" marker-end="url(#{uid}-arrow)"/>')
        # The vertical label sits to the left of the arrow, not across it.
        if i == 2:
            tx, ty = 864, 246
        arrows.append(f'<text x="{tx}" y="{ty}" fill="#cbd5e1" font-size="12" text-anchor="middle">{escape(transitions[i])}</text>')
    return f'''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg role="img" aria-labelledby="{uid}-title {uid}-desc" viewBox="0 0 1120 455" style="display:block;width:100%;height:auto;background:#090d16;font-family:ui-monospace,monospace">
<title id="{uid}-title">{escape(title)}</title><desc id="{uid}-desc">{escape(caption)}</desc>
<defs><marker id="{uid}-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#38bdf8"/></marker></defs>
<text x="30" y="38" fill="#f8fafc" font-size="20" font-weight="700">{escape(title)}</text>
{''.join(arrows)}{''.join(cards)}</svg></div><figcaption>{escape(caption)}</figcaption></figure>'''


def stage(number, name, action, result, evidence, commands='', *, location='TODO: execution location'):
    text = f'**Stage {number}: {name}**\n\n**Location:** {location}\n\n{action}\n\n'
    if commands:
        text += '```bash\n' + dedent(commands).strip() + '\n```\n\n'
    return text + f'**Expected result:** {result}\n\n**Save:** {evidence}'


def workspace(prefix, *, preflight_text):
    return f'''python3 --version
LAB_DIR=$(mktemp -d /tmp/{prefix}.XXXXXX)
export LAB_DIR
cd "$LAB_DIR"
python3 -c 'import os, pathlib; pathlib.Path("preflight.txt").write_text("{preflight_text}\\n"); print(os.getcwd())'
'''


def write_file(name, content):
    return f"cat > {name} <<'EOF'\n{dedent(content).strip()}\nEOF\n"


def lab(name, goal, expected, steps, accept, trouble, files, *, defaults=None):
    """Assemble slots; absent contextual content remains explicitly unfinished."""
    return {**LAB_DEFAULTS, **(defaults or {}), 'name': name, 'goal': goal,
            'expected': expected, 'steps': steps, 'accept': accept,
            'trouble': trouble, 'file': files}


def case(scenario, impact, constraints, records, root, diagnostics, fixes, verify, residual, enabled=False, diagram=None, *, evidence_label='TODO: evidence provenance', facts='TODO: supplied facts', inference='TODO: architectural inference', expected='TODO: expected behavior'):
    result = {'scenario': scenario, 'impact': impact, 'constraints': constraints,
        'evidence': '**' + evidence_label + '**\n\n```text\n' + records + '\n```',
        'root': root, 'diagnostic_steps': diagnostics, 'remediation_steps': fixes,
        'verify': verify, 'residual': residual, 'diagram_enabled': enabled}
    if enabled:
        result.update({'diagram': diagram, 'icons': ['../assets/icons/generic/' + name + '.svg' for name in ('event', 'failure', 'failure', 'policy', 'outcome')],
            'facts': facts,
            'inference': inference,
            'expected': expected})
    return result


