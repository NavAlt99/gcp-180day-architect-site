"""Bounded, non-truncating linear-flow layout; unsupported flows require raw SVG."""
from html import escape
from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parents[1]


def lines(text, width):
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Compact flow labels/details must be non-empty strings')
    wrapped = [line for paragraph in text.splitlines()
               for line in textwrap.wrap(paragraph, width, break_long_words=True, break_on_hyphens=False)]
    if len(wrapped) > 32:
        raise ValueError('Compact flow label cannot fit bounded layout; author raw SVG')
    return wrapped


def render_compact_flow(uid, flow):
    """Render an ordered chain (2–12 nodes), preserving every label character."""
    if not re.fullmatch(r'[A-Za-z][\w-]*', uid):
        raise ValueError('Compact flow needs an XML-safe unique prefix')
    nodes, steps = flow['nodes'], flow['steps']
    if not 2 <= len(nodes) <= 12 or len(steps) != len(nodes) - 1:
        raise ValueError('Compact flow supports 2–12 ordered chain nodes; use raw SVG otherwise')
    ids = [node['id'] for node in nodes]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r'[A-Za-z][\w-]*', node_id) for node_id in ids):
        raise ValueError('Compact node IDs must be unique XML-safe strings')
    for i, step in enumerate(steps):
        if (step['from'], step['to']) != (ids[i], ids[i + 1]):
            raise ValueError('Compact flow steps must match ordered nodes; branches require raw SVG')
    title, caption = flow['title'], flow['caption']
    desc = flow.get('desc', caption)
    title_lines = lines(title, 72)
    lines(caption, 160)
    lines(desc, 160)
    prepared = []
    for i, node in enumerate(nodes):
        icon = node['icon']
        path = (ROOT / 'days' / icon).resolve()
        if not path.is_relative_to(ROOT / 'assets/icons') or not path.is_file() or path.suffix != '.svg':
            raise ValueError(f'Compact node {node["id"]}: icon must exist under local assets/icons')
        details = node.get('detail', '')
        if isinstance(details, (list, tuple)):
            detail_lines = [line for detail in details for line in lines(detail, 29)]
        else:
            detail_lines = lines(details, 29) if details else []
        name_lines = lines(f'{i + 1}. {node["label"]}', 22)
        if len(detail_lines) > 32:
            raise ValueError('Compact flow detail cannot fit bounded layout; author raw SVG')
        height = max(110, 30 + len(name_lines) * 20 + 14 + len(detail_lines) * 20)
        prepared.append((name_lines, detail_lines, height))
    step_lines = [lines(f'{i+1} → {i+2}: {step["label"]}', 12) for i, step in enumerate(steps)]
    rows = (len(nodes) + 2) // 3
    row_height = max(max(p[2] for p in prepared), max(map(len, step_lines)) * 32 + 80)
    gap = max(140, max(map(len, step_lines)) * 16 + 36)
    top = 60 + len(title_lines) * 26
    positions = []
    for i in range(len(nodes)):
        row, col = divmod(i, 3)
        col = 2 - col if row % 2 else col
        positions.append((30 + col * 390, top + row * (row_height + gap)))
    canvas_h = top + rows * row_height + (rows - 1) * gap + 30
    if canvas_h > 5000:
        raise ValueError('Compact flow cannot fit bounded canvas; author raw SVG')
    cards, arrows = [], []
    for i, (node, (names, details, _), (x, y)) in enumerate(zip(nodes, prepared, positions)):
        texts = ''.join(f'<text x="54" y="{32+j*20}" fill="#7dd3fc" font-size="16" font-weight="700">{escape(line)}</text>' for j, line in enumerate(names))
        texts += ''.join(f'<text x="16" y="{46+len(names)*20+j*20}" fill="#e2e8f0" font-size="14">{escape(line)}</text>' for j, line in enumerate(details))
        cards.append(f'<g id="{uid}-node-{node["id"]}" data-node="{node["id"]}" aria-label="{escape(node["label"], quote=True)}" transform="translate({x},{y})"><rect width="280" height="{row_height}" rx="10" fill="#121526" stroke="#38bdf8"/><image href="{escape(node["icon"], quote=True)}" x="15" y="14" width="30" height="30" preserveAspectRatio="xMidYMid meet"/>{texts}</g>')
    for i, ((x, y), (nx, ny), label_lines) in enumerate(zip(positions, positions[1:], step_lines)):
        if ny == y:
            right = nx > x
            x1, x2 = (x+280, nx-10) if right else (x, nx+290)
            y1 = y2 = y + row_height / 2
            tx, ty, anchor = (x1+x2)/2, y1 - len(label_lines)*16 - 8, 'middle'
        else:
            x1 = x2 = x + 140
            y1, y2 = y + row_height, ny - 10
            tx, ty, anchor = x1 - 22, (y1+y2)/2 - len(label_lines)*8, 'end'
        arrows.append(f'<g id="{uid}-step-{i+1}" aria-label="{escape(steps[i]["label"], quote=True)}"><line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#38bdf8" stroke-width="2" marker-end="url(#{uid}-arrow)"/>' + ''.join(f'<text x="{tx}" y="{ty+j*16}" fill="#cbd5e1" font-size="12" text-anchor="{anchor}">{escape(line)}</text>' for j,line in enumerate(label_lines)) + '</g>')
    heading = ''.join(f'<text x="30" y="{32+i*26}" fill="#f8fafc" font-size="20" font-weight="700">{escape(line)}</text>' for i,line in enumerate(title_lines))
    prose = ''.join(f'<li>{i+1} → {i+2}: {escape(step["label"])}</li>' for i,step in enumerate(steps))
    return f'<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg role="img" aria-labelledby="{uid}-title {uid}-desc" viewBox="0 0 1120 {canvas_h}" style="display:block;width:100%;height:auto;min-width:1120px;background:#090d16;font-family:ui-monospace,monospace"><title id="{uid}-title">{escape(title)}</title><desc id="{uid}-desc">{escape(desc)}</desc><defs><marker id="{uid}-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#38bdf8"/></marker></defs>{heading}{"".join(arrows)}{"".join(cards)}</svg></div><figcaption>{escape(caption)}<ol class="flow-transitions">{prose}</ol></figcaption></figure>'
