"""Reproduce scratch-only Day 002 conversion and diagram review documents."""
import ast
from pathlib import Path
from pprint import pformat
import runpy

from scripts.compact_flow import render_compact_flow

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'scratch/baseline/diagram-compare'
DEST.mkdir(parents=True, exist_ok=True)
source = (ROOT / 'scratch/day_data_002.py').read_text()
module = ast.parse(source)
changes = []
for item in module.body:
    if isinstance(item, ast.Assign) and isinstance(item.targets[0], ast.Name) and item.targets[0].id in ('NEXT_HOP_SVG', 'NIC_SVG'):
        name = item.targets[0].id
        uid, title, nodes, steps, caption = [ast.literal_eval(argument) for argument in item.value.args]
        flow = {'title': title, 'desc': caption, 'caption': caption,
                'nodes': [{'id': f'n{i+1}', 'label': label, 'detail': detail, 'icon': f'../assets/icons/generic/{icon}.svg'} for i,(label,detail,icon) in enumerate(nodes)],
                'steps': [{'from': f'n{i+1}', 'to': f'n{i+2}', 'label': label} for i,label in enumerate(steps)]}
        flow_name = name.replace('_SVG','_FLOW')
        changes.append((item.lineno-1, item.end_lineno, flow_name+' = '+pformat(flow, width=105,sort_dicts=False)+'\n'+name+f' = render_compact_flow({uid!r}, {flow_name})\n'))
lines=source.splitlines(keepends=True)
for start,end,replacement in reversed(changes): lines[start:end]=[replacement]
converted='from scripts.compact_flow import render_compact_flow\n'+''.join(lines)
# Keep the original docstring first and use a root-relative execution context.
converted=converted.replace('from scripts.compact_flow import render_compact_flow\n','',1).replace('DAY = 2','from scripts.compact_flow import render_compact_flow\n\nDAY = 2',1)
fixture=ROOT / 'scratch/spec-fixtures/phase-d-day-002-compact.py'
fixture.write_text(converted)
before=runpy.run_path(str(ROOT / 'scratch/day_data_002.py'))
after=runpy.run_path(str(fixture))
for diagram in ('NEXT_HOP_SVG','NIC_SVG'):
    slug=diagram.lower().replace('_svg','')
    for state,values in [('before',before),('after',after)]:
        html=values[diagram].replace('../assets/', '../../../assets/')
        for theme in ('dark','light'):
            document=f'''<!doctype html><html data-theme="{theme}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="../../../assets/site.css"><style>body{{margin:0}}main{{padding:18px;max-width:1160px;margin:auto}}.topic-card{{padding:18px}}</style></head><body><main class="day foundation-refresh"><article class="topic-card"><h3>{slug}: {state} — {theme} theme</h3>{html}</article></main></body></html>'''
            (DEST/f'{slug}-{state}-{theme}.html').write_text(document)
print('Durable Day 002 remains raw/helper SVG; converted scratch spec:',fixture)
print('Spec bytes before', len(source.encode()), 'scratch converted',len(converted.encode()))
