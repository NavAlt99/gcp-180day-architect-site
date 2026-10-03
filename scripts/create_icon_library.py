"""Import official SVG archives and create reusable generic diagram icons.

Usage: python3 scripts/create_icon_library.py --core /tmp/gcp-core-icons.zip
       --legacy /tmp/gcp-legacy-icons.zip
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / 'assets' / 'icons'
NS = 'http://www.w3.org/2000/svg'
GENERIC = {
    'client': '<rect x="8" y="10" width="48" height="32" rx="3"/><path d="M24 42v10m16-10v10M18 54h28"/>',
    'server': '<rect x="14" y="8" width="36" height="48" rx="4"/><path d="M14 24h36M14 40h36"/><circle cx="22" cy="16" r="1"/><circle cx="22" cy="32" r="1"/><circle cx="22" cy="48" r="1"/>',
    'router': '<rect x="8" y="20" width="48" height="24" rx="5"/><path d="M32 6v14m-6-8 6-6 6 6M32 44v14m-6-6 6 6 6-6M6 32h14m-8-6-6 6 6 6M44 32h14m-6-6 6 6-6 6"/>',
    'switch': '<rect x="6" y="18" width="52" height="28" rx="4"/><path d="M14 34h6v6h-6zm12 0h6v6h-6zm12 0h6v6h-6zM16 25h30m-6-4 6 4-6 4"/>',
    'firewall': '<rect x="10" y="10" width="44" height="44" rx="2"/><path d="M10 24h44M10 40h44M26 10v14m16 0v16M26 40v14"/>',
    'load-balancer': '<rect x="6" y="25" width="14" height="14" rx="2"/><rect x="44" y="6" width="14" height="12" rx="2"/><rect x="44" y="26" width="14" height="12" rx="2"/><rect x="44" y="46" width="14" height="12" rx="2"/><path d="M20 32h12V12h12M32 32h12M32 32v20h12"/>',
    'dns-resolver': '<circle cx="32" cy="32" r="24"/><ellipse cx="32" cy="32" rx="10" ry="24"/><path d="M8 32h48M12 20h40M12 44h40"/>',
    'internet': '<path d="M18 48h30a12 12 0 0 0 2-24 18 18 0 0 0-35-1 13 13 0 0 0 3 25Z"/>',
    'endpoint': '<circle cx="32" cy="32" r="12"/><path d="M32 4v16m0 24v16M4 32h16m24 0h16"/>',
    'database': '<ellipse cx="32" cy="14" rx="20" ry="8"/><path d="M12 14v36c0 11 40 11 40 0V14M12 32c0 11 40 11 40 0"/>',
    'storage': '<path d="M12 16h40l-4 40H16Z"/><ellipse cx="32" cy="16" rx="20" ry="7"/>',
    'subnet': '<rect x="6" y="6" width="52" height="52" rx="5" stroke-dasharray="4 3"/><rect x="14" y="16" width="12" height="12"/><rect x="38" y="36" width="12" height="12"/><path d="M20 28v14h18"/>',
    'vpn': '<path d="M32 6 52 14v17c0 12-12 22-20 27-8-5-20-15-20-27V14Z"/><rect x="23" y="28" width="18" height="15" rx="2"/><path d="M26 28v-5a6 6 0 0 1 12 0v5"/>',
    'user': '<circle cx="32" cy="19" r="11"/><path d="M12 56v-6a20 20 0 0 1 40 0v6Z"/>',
    'event': '<path d="m36 4-23 32h17l-2 24 23-34H34Z"/>',
    'decision': '<path d="m32 4 28 28-28 28L4 32Z"/><path d="M25 24a7 7 0 0 1 14 0c0 6-7 5-7 12m0 6v2"/>',
    'policy': '<path d="M16 6h24l10 10v42H16ZM40 6v12h10M23 28h20M23 36h20M23 44h14"/>',
    'artifact': '<path d="M16 6h24l10 10v42H16ZM40 6v12h10m-26 8-5 6 5 6m16-12 5 6-5 6m-8-14-4 16"/>',
    'outcome': '<circle cx="32" cy="32" r="25"/><path d="m18 32 10 10 20-22"/>',
    'failure': '<path d="m32 6 28 50H4Z"/><path d="M32 23v16m0 6v2"/>',
    'monitoring': '<rect x="6" y="10" width="52" height="38" rx="3"/><path d="M10 32h10l6-12 10 22 6-10h12M32 48v8M20 58h24"/>',
    'queue': '<rect x="7" y="18" width="12" height="28" rx="2"/><rect x="26" y="18" width="12" height="28" rx="2"/><rect x="45" y="18" width="12" height="28" rx="2"/>',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core', required=True, type=Path)
    parser.add_argument('--legacy', required=True, type=Path)
    args = parser.parse_args()
    entries = []
    for collection, archive, url in (
        ('gcp/core', args.core, 'https://services.google.com/fh/files/misc/core-products-icons.zip'),
        ('gcp/legacy', args.legacy, 'https://services.google.com/fh/files/misc/google-cloud-legacy-icons.zip'),
    ):
        with zipfile.ZipFile(archive) as bundle:
            for name in sorted(bundle.namelist()):
                if not name.lower().endswith('.svg') or name.startswith('__MACOSX/'):
                    continue
                label = name.split('/')[1] if collection == 'gcp/core' else Path(name).stem.replace('_', ' ')
                slug = re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-')
                path = ROOT / collection / (slug + '.svg')
                if any(e['path'] == str(path.relative_to(ROOT)) for e in entries):
                    raise ValueError(f'Duplicate icon: {path}')
                raw = bundle.read(name)
                element = ET.fromstring(raw)
                if element.tag != '{' + NS + '}svg':
                    raise ValueError(f'Not an SVG: {name}')
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
                entries.append(dict(id=collection.replace('/', '-') + '-' + slug, label=label,
                                    path=str(path.relative_to(ROOT)), collection=collection,
                                    source=url, archive_path=name, sha256=hashlib.sha256(raw).hexdigest()))
    for name, shapes in GENERIC.items():
        path = ROOT / 'generic' / (name + '.svg')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'<svg xmlns="{NS}" viewBox="0 0 64 64" width="64" height="64" role="img" aria-labelledby="title"><title id="title">{name.replace("-", " ").title()}</title><g fill="none" stroke="#2563eb" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{shapes}</g></svg>\n')
        entries.append(dict(id='generic-' + name, label=name.replace('-', ' ').title(),
                            path=str(path.relative_to(ROOT)), collection='generic', source='Project-authored SVG'))
    (ROOT / 'manifest.json').write_text(json.dumps(entries, indent=2) + '\n')
    cards = ''.join(f'<figure><img src="{html.escape(e["path"])}" alt="{html.escape(e["label"])}" loading="lazy"><figcaption>{html.escape(e["label"])}<small>{e["collection"]}</small><code>{html.escape(e["path"])}</code></figcaption></figure>' for e in entries)
    (ROOT / 'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reusable diagram icons</title><style>body{font:16px system-ui;margin:32px;background:#f1f5f9;color:#0f172a}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:16px}figure{margin:0;padding:20px;background:white;border:1px solid #cbd5e1;border-radius:12px}img{width:64px;height:64px;object-fit:contain}small,code{display:block;margin-top:8px;font-size:12px;overflow-wrap:anywhere}small{color:#475569}</style><h1>Reusable diagram icons</h1><p>Official GCP core and legacy assets plus project-authored generic icons. Use current core icons when available. See README.md for embedding and attribution.</p><main>' + cards + '</main></html>\n')
    print(f'Created {len(entries)} SVG icons and catalog at {ROOT}')


if __name__ == '__main__':
    main()
