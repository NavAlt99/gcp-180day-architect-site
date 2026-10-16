#!/usr/bin/env python3
"""Deterministic page-rule checks R1-R4, R7, R8 on a built day page.

Usage:
  python3 scripts/check_page_rules.py --day 3
  python3 scripts/check_page_rules.py --day 3 --diagrams keep --terms "hypervisor,KVM" --json scratch/day-003-rules.json
  python3 scripts/check_page_rules.py --page /path/to/day-003.html

Reads days/day-NNN.html (or --page). Standard library only; Pillow with DejaVu fonts is used for
text widths when available (otherwise an average-character-width estimate, and the method is printed).
Exit status 1 when a gated rule fails. R4/R8 are gated only with --diagrams allow (default).
R5 is reported, never gated.
"""
import argparse, collections, glob, json, os, re, sys
from html.parser import HTMLParser

VOID = {'br', 'hr', 'img', 'meta', 'link', 'input', 'source', 'wbr', 'col', 'area', 'base', 'embed', 'param', 'track'}
STRUCT = {'Why today:', 'Where it sits:', 'Problem preview:', 'Subtopics in this discussion:',
          'Evidence limit:', 'Linked subtopics:'}
GOOGLE = 'http://www.google.com/search?q='
SKIP = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'code', 'samp', 'kbd', 'pre', 'figcaption', 'a', 'script', 'style', 'svg', 'title'}
STOP = {'RFC', 'NOT', 'AND', 'THE', 'FOR', 'YES', 'FALSE', 'TRUE'}


class Node:
    __slots__ = ('tag', 'attrs', 'kids', 'parent')

    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.kids, self.parent = tag, attrs, [], parent

    def cls(self):
        return (self.attrs.get('class') or '').split()

    def text(self):
        return ''.join(k if isinstance(k, str) else k.text() for k in self.kids)


def nodes(n):
    yield n
    for k in n.kids:
        if isinstance(k, Node):
            yield from nodes(k)


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('#root', {}, None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, {k: (v or '') for k, v in attrs}, self.cur)
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(Node(tag, {k: (v or '') for k, v in attrs}, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, d):
        self.cur.kids.append(d)


# ---------------------------------------------------------------- fonts
def load_fonts():
    try:
        from PIL import ImageFont
        sans = glob.glob('/usr/share/fonts/**/DejaVuSans.ttf', recursive=True)
        mono = glob.glob('/usr/share/fonts/**/DejaVuSansMono.ttf', recursive=True)
        if sans and mono:
            return ImageFont.truetype(sans[0], 100), ImageFont.truetype(mono[0], 100), 'Pillow DejaVuSans / DejaVuSansMono (bold x1.07)'
    except Exception:
        pass
    return None, None, 'average character width estimate (0.56em sans, 0.60em mono; Pillow/DejaVu not found)'


FSANS, FMONO, METHOD = load_fonts()


def text_width(s, fs, bold, mono):
    f = FMONO if mono else FSANS
    w = f.getlength(s) * fs / 100 if f else len(s) * fs * (0.60 if mono else 0.56)
    return w * (1.07 if bold else 1)


# ---------------------------------------------------------------- helpers
def num(v, d=0.0):
    try:
        return float(re.sub(r'[a-z%]+$', '', str(v).strip()))
    except Exception:
        return d


def style_get(n, key):
    if key in n.attrs:
        return n.attrs[key]
    m = re.search(r'(?:^|;)\s*' + key + r'\s*:\s*([^;]+)', n.attrs.get('style', ''))
    return m.group(1).strip() if m else None


def is_google(a):
    return a.tag == 'a' and a.attrs.get('href', '').startswith(('http://www.google.com/search', 'https://www.google.com/search'))


def exact_google(a):
    return a.attrs.get('href', '').startswith(GOOGLE) and a.attrs.get('rel') == 'noopener' and a.attrs.get('target') == '_blank'


def scan(card):
    """Per subtopic section: linkable text chunks, google link texts, keyword spans (text, linked, exact)."""
    secs = collections.OrderedDict()
    st = {'sid': '(intro)'}

    def sec():
        return secs.setdefault(st['sid'], {'text': [], 'links': [], 'spans': []})

    def walk(n, skip):
        if isinstance(n, str):
            if not skip:
                sec()['text'].append(n)
            return
        if n.tag in ('h3', 'h4') and re.fullmatch(r'topic-\d+-subtopic-\d+', n.attrs.get('id', '')):
            st['sid'] = n.attrs['id']
        if is_google(n):
            sec()['links'].append(n.text().strip().lower())
        if n.tag == 'strong' and 'keyword' in n.cls():
            ga = [x for x in nodes(n) if isinstance(x, Node) and is_google(x)]
            sec()['spans'].append((n.text().strip(), bool(ga), bool(ga) and all(exact_google(x) for x in ga)))
        sk = skip or n.tag in SKIP or (n.tag == 'strong' and 'side-heading' in n.cls()) or n.tag in ('table', 'div')
        for k in n.kids:
            walk(k, sk)

    walk(card, False)
    return secs


def result(rule, status, gated, summary, items=None):
    return {'rule': rule, 'status': status, 'gated': gated, 'summary': summary, 'items': (items or [])[:25]}


# ---------------------------------------------------------------- R1 / R2 / R3
def check_r1(root, ids):
    items, fails = [], 0
    ov = {n.attrs['id']: n for n in nodes(root) if n.tag == 'article' and re.fullmatch(r'topic-\d+-overview', n.attrs.get('id', ''))}
    te = {n.attrs['id']: n for n in nodes(root) if n.tag == 'article' and re.fullmatch(r'topic-\d+-technical', n.attrs.get('id', ''))}
    counts = []
    for oid, card in ov.items():
        xx = re.search(r'topic-(\d+)-overview', oid).group(1)
        tech = te.get(f'topic-{xx}-technical')
        heads = [h.attrs['id'] for h in nodes(tech) if h.tag in ('h3', 'h4') and re.fullmatch(r'topic-\d+-subtopic-\d+', h.attrs.get('id', ''))] if tech else []
        label = any(n.tag == 'strong' and 'side-heading' in n.cls() and n.text().strip() == 'Linked subtopics:' for n in nodes(card))
        links = {n.attrs['href'][1:] for n in nodes(card) if n.tag == 'a' and re.fullmatch(r'#topic-\d+-subtopic-\d+', n.attrs.get('href', ''))}
        if not heads:
            fails += 1; items.append(f'{oid}: technical discussion has no subtopic heading ids')
        if not label:
            fails += 1; items.append(f'{oid}: no "Linked subtopics:" list')
        miss = [h for h in heads if h not in links]
        if label and miss:
            fails += 1; items.append(f'{oid}: list lacks links to {len(miss)} of {len(heads)} subtopics')
        counts.append(f'{xx}:{len(links & set(heads))}/{len(heads)}')
        # list at the start of the technical discussion
        if tech:
            for p in nodes(tech):
                if p.tag == 'strong' and 'side-heading' in p.cls() and p.text().strip() == 'Subtopics in this discussion:':
                    par = p.parent
                    sib = par.parent.kids if par and par.parent else []
                    ul = next((s for s in sib[sib.index(par) + 1:] if isinstance(s, Node) and s.tag in ('ul', 'ol')), None) if par in sib else None
                    nli = len([x for x in nodes(ul) if isinstance(x, Node) and x.tag == 'li']) if ul else 0
                    nlk = len([x for x in nodes(ul) if isinstance(x, Node) and x.tag == 'a' and x.attrs.get('href', '').startswith('#topic-')]) if ul else 0
                    if nli == 0 or nlk < nli:
                        fails += 1; items.append(f'{tech.attrs["id"]}: "Subtopics in this discussion:" list has {nlk} links for {nli} items')
                    break
    if not ov:
        fails += 1; items.append('no topic overview cards found (article id topic-XX-overview)')
    dang = sorted({a.attrs['href'][1:] for a in nodes(root) if a.tag == 'a' and a.attrs.get('href', '').startswith('#') and len(a.attrs['href']) > 1 and a.attrs['href'][1:] not in ids})
    if dang:
        fails += 1; items.append(f'dangling #links: {dang[:6]}')
    return result('R1 linked subtopics', 'FAIL' if fails else 'PASS', True,
                  f'{len(ov)} overview cards, per-topic overview links/subtopics {" ".join(counts) or "-"}; {fails} problem(s)', items)


def check_r2(root):
    paras, lis, labels = 0, 0, collections.Counter()
    for card in (n for n in nodes(root) if n.tag == 'article' and re.fullmatch(r'topic-\d+-technical', n.attrs.get('id', ''))):
        for p in nodes(card):
            if p.tag == 'p':
                first = next((k for k in p.kids if not (isinstance(k, str) and not k.strip())), None)
                if isinstance(first, Node) and first.tag == 'strong' and 'side-heading' in first.cls() and first.text().strip() not in STRUCT:
                    paras += 1; labels[first.text().strip()] += 1
            if p.tag == 'li':
                first = next((k for k in p.kids if not (isinstance(k, str) and not k.strip())), None)
                if isinstance(first, Node) and first.tag == 'strong' and 'side-heading' in first.cls():
                    lis += 1
    return result('R2 bullets', 'FAIL' if paras else 'PASS', True,
                  f'{lis} side-heading bullets; {paras} subtopic side-heading paragraphs not yet bullets',
                  [f'{k} x{v}' for k, v in labels.items()])


def check_r3(root, terms):
    cards = [n for n in nodes(root) if n.tag == 'article' and re.fullmatch(r'topic-\d+-(overview|technical)', n.attrs.get('id', ''))]
    spans = unlinked = nonexact = 0
    items, termmiss = [], []
    alltext, alllinks = [], []
    for card in cards:
        for sid, s in scan(card).items():
            for t, linked, ex in s['spans']:
                spans += 1
                if not linked:
                    unlinked += 1; items.append(f'unlinked keyword span in {card.attrs["id"]} / {sid}: {t[:50]}')
                elif not ex:
                    nonexact += 1; items.append(f'link not in exact form: {t[:50]}')
            for term in terms:
                pat = re.compile(r'(?<!\w)' + re.escape(term) + r'(?!\w)', re.I)
                n = sum(len(pat.findall(c)) for c in s['text'])
                if n and not any(term.lower() in l for l in s['links']):
                    termmiss.append(f'{card.attrs["id"]} / {sid}: "{term}" {n} mention(s), none linked')
            if card.attrs['id'].endswith('technical'):
                alltext += s['text']
            alllinks += s['links']
    blob = ' '.join(alllinks)
    cnt = collections.Counter(t for t in re.findall(r'\b[A-Z][A-Z0-9]{2,}\b|\b[a-z]+(?:_[a-z0-9]+)+\b', ' '.join(alltext)) if t not in STOP)
    adv = [f'{t} ({n} mentions)' for t, n in cnt.most_common(40) if n >= 3 and t.lower() not in blob][:15]
    bad = unlinked + nonexact + len(termmiss)
    r = result('R3 keyword links', 'FAIL' if bad else 'PASS', True,
               f'{spans} keyword spans, {unlinked} unlinked, {nonexact} not in exact form; {len(termmiss)} listed-term misses',
               items + termmiss)
    r['advisory'] = adv
    return r


# ---------------------------------------------------------------- R4 / R8
def measure_svg(svg, title):
    vb = svg.attrs.get('viewbox')
    W = None
    if vb:
        p = [num(x) for x in re.split(r'[ ,]+', vb.strip())]
        W = p[2] if len(p) == 4 else None
    rects, icons, lines = [], [], []
    st = {'nm': 0, 'small': []}

    def walk(n, ox, oy, fs, fam, bold, anc, ok):
        if not isinstance(n, Node):
            return
        tr = n.attrs.get('transform', '')
        if tr:
            m = re.fullmatch(r'\s*translate\(\s*(-?[\d.]+)(?:[ ,]+(-?[\d.]+))?\s*\)\s*', tr)
            if m:
                ox += float(m.group(1)); oy += float(m.group(2) or 0)
            else:
                ok = False
        f = style_get(n, 'font-size'); fs = num(f, fs) if f else fs
        fa = style_get(n, 'font-family'); fam = fa or fam
        fw = style_get(n, 'font-weight'); bold = (fw in ('600', '700', '800', '900', 'bold', 'bolder')) if fw else bold
        ta = style_get(n, 'text-anchor'); anc = ta or anc
        if n.tag == 'rect' and ok and n.attrs.get('width'):
            x, y = ox + num(n.attrs.get('x')), oy + num(n.attrs.get('y'))
            w, h = num(n.attrs['width']), num(n.attrs.get('height'))
            if w >= 40 and h >= 14:
                rects.append((x, y, x + w, y + h))
        elif n.tag == 'image' and ok:
            x, y = ox + num(n.attrs.get('x')), oy + num(n.attrs.get('y'))
            icons.append((x, y, x + num(n.attrs.get('width')), y + num(n.attrs.get('height'))))
        elif n.tag == 'text':
            tfs = num(style_get(n, 'font-size'), fs) if style_get(n, 'font-size') else fs
            tb = (style_get(n, 'font-weight') in ('600', '700', '800', '900', 'bold', 'bolder')) if style_get(n, 'font-weight') else bold
            tanc = style_get(n, 'text-anchor') or anc
            mono = 'mono' in (fam or '').lower()
            x, y = ox + num(n.attrs.get('x')), oy + num(n.attrs.get('y'))
            tsp = [k for k in n.kids if isinstance(k, Node) and k.tag == 'tspan']
            segs = []
            if tsp:
                cx, cy = x, y
                for t in tsp:
                    if 'x' in t.attrs: cx = ox + num(t.attrs['x'])
                    if 'y' in t.attrs: cy = oy + num(t.attrs['y'])
                    cy += num(t.attrs.get('dy'))
                    segs.append((t.text(), cx, cy))
            else:
                segs.append((n.text(), x, y))
            for s, sx, sy in segs:
                s = ' '.join(s.split())
                if not s:
                    continue
                if tfs < 9:
                    st['small'].append(s)
                if not ok:
                    st['nm'] += 1
                    continue
                w = text_width(s, tfs, tb, mono)
                x0 = sx - w / 2 if tanc == 'middle' else (sx - w if tanc == 'end' else sx)
                lines.append((s, x0, sy - tfs * 0.8, x0 + w, sy + tfs * 0.25))
            return
        for k in n.kids:
            walk(k, ox, oy, fs, fam, bold, anc, ok)

    walk(svg, 0, 0, 16.0, style_get(svg, 'font-family') or '', False, 'start', True)
    defects, border = collections.Counter(), []
    eg = []
    for i, (s, x0, y0, x1, y1) in enumerate(lines):
        def rec(kind, ov, w=None):
            if ov > 6:
                defects[kind] += 1; eg.append(f'{title}: {kind} "{s[:40]}" (~{ov:.0f}px)')
            elif ov > 0:
                border.append(f'{title}: borderline {kind} "{s[:40]}" (~{ov:.0f}px)')
        if W:
            rec('outside viewBox', max(-x0, x1 - W))
        for ix0, iy0, ix1, iy1 in icons:
            ow, oh = min(x1, ix1) - max(x0, ix0), min(y1, iy1) - max(y0, iy0)
            if ow > 0 and oh > 2:
                rec('text/icon overlap', ow)
        for rx0, ry0, rx1, ry1 in rects:
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            if rx0 <= cx <= rx1 and ry0 <= cy <= ry1:
                rec('text past node border', max(rx0 + 4 - x0, x1 - (rx1 - 4)))
        for j in range(i + 1, len(lines)):
            s2, a0, b0, a1, b1 = lines[j]
            ow, oh = min(x1, a1) - max(x0, a0), min(y1, b1) - max(y0, b0)
            if ow > 0 and oh > 3:
                if ow > 6:
                    defects['text/text overlap'] += 1; eg.append(f'{title}: text/text "{s[:25]}" | "{s2[:25]}"')
                else:
                    border.append(f'{title}: borderline text/text "{s[:25]}" | "{s2[:25]}"')
    return {'title': title, 'measured': len(lines), 'not_measured': st['nm'], 'icons': len(icons), 'small': st['small'],
            'defects': dict(defects), 'borderline': len(border), 'examples': eg, 'border_examples': border}


def check_diagrams(root, gate):
    out = []
    for i, svg in enumerate((n for n in nodes(root) if n.tag == 'svg'), 1):
        t = next((x.text().strip() for x in nodes(svg) if isinstance(x, Node) and x.tag == 'title'), '') or svg.attrs.get('id', '')
        out.append(measure_svg(svg, f'SVG {i}' + (f' ({t[:40]})' if t else '')))
    d = sum(sum(m['defects'].values()) for m in out)
    s = sum(len(m['small']) for m in out)
    nm = sum(m['not_measured'] for m in out)
    ex = [e for m in out for e in m['examples']]
    r4 = result('R4 diagram collisions', 'FAIL' if d else 'PASS', gate, f'{len(out)} diagrams, {sum(m["measured"] for m in out)} texts measured, {d} defect(s), {sum(m["borderline"] for m in out)} borderline, {nm} text(s) not measured', ex)
    r8 = result('R8 text below 9px', 'FAIL' if s else 'PASS', gate, f'{s} label(s) below 9px across {sum(1 for m in out if m["small"])} diagram(s)',
                [f'{m["title"]}: {len(m["small"])} (e.g. "{m["small"][0][:35]}")' for m in out if m['small']])
    return r4, r8, out


# ---------------------------------------------------------------- R5 / R7
def check_r5(root):
    css = ' '.join(n.text() for n in nodes(root) if n.tag == 'style')
    hit = re.search(r'[^{}]*technical[^{}]*\{[^}]*(max-width\s*:\s*(none|100%)|(?<![-\w])width\s*:\s*100%)', css)
    return result('R5 full width', 'FOUND' if hit else 'NOT FOUND', False,
                  'page-level width rule for the technical discussion ' + ('present' if hit else 'not in the page styles (shared stylesheet not inspected)'))


def check_r7(html):
    body = re.sub(r'<(pre|code|samp|kbd|script|style)\b.*?</\1>', ' ', html, flags=re.S | re.I)
    pats = {
        'list marker inside paragraph': r'[.:;)\]]\s+[-*]\s+(?:<(?:strong|a|em|b|span)\b|[A-Z][a-z])',
        'paragraph starting with list marker': r'<p>\s*(?:[-*]|\d+\.)\s+\S',
        '**bold** markers': r'\*\*[^*\n<]{2,}\*\*',
        'backtick spans': r'`[^`\n<]+`',
        '# heading markers': r'>\s*#{1,6}\s+[A-Za-z]',
    }
    items, total = [], 0
    for k, p in pats.items():
        ms = list(re.finditer(p, body))
        total += len(ms)
        if ms:
            m = ms[0]
            items.append(f'{k}: {len(ms)} (e.g. "{" ".join(body[max(0, m.start() - 35):m.end() + 25].split())}")')
    return result('R7 leaked markup', 'FAIL' if total else 'PASS', True, f'{total} leaked markup marker(s)', items)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--day', type=int)
    ap.add_argument('--page')
    ap.add_argument('--diagrams', choices=['keep', 'allow'], default='allow')
    ap.add_argument('--terms', default='', help='comma-separated terms that must be linked (R3)')
    ap.add_argument('--terms-file')
    ap.add_argument('--json')
    a = ap.parse_args()
    if not a.page and not a.day:
        ap.error('give --day or --page')
    path = a.page or f'days/day-{a.day:03d}.html'
    html = open(path, encoding='utf-8').read()
    b = Builder(); b.feed(html); root = b.root
    ids = {n.attrs['id'] for n in nodes(root) if isinstance(n, Node) and 'id' in n.attrs}
    terms = [t.strip() for t in a.terms.split(',') if t.strip()]
    if a.terms_file:
        terms += [l.strip() for l in open(a.terms_file) if l.strip() and not l.startswith('#')]
    gate = a.diagrams == 'allow'
    r4, r8, diag = check_diagrams(root, gate)
    res = [check_r1(root, ids), check_r2(root), check_r3(root, terms), r4, check_r5(root), check_r7(html), r8]
    print(f'{path} ({len(html)} bytes) | diagram method: {METHOD} | DIAGRAMS={a.diagrams}')
    for r in res:
        tag = r['status'] + ('' if r['gated'] or r['status'] in ('PASS',) else ' (not gated)')
        print(f'{r["rule"]:<24} {tag:<22} {r["summary"]}')
        for it in r['items'][:8]:
            print(f'    - {it}')
        if len(r['items']) > 8:
            print(f'    ... {len(r["items"]) - 8} more')
        for it in r.get('advisory', [])[:1]:
            print('    advisory, unlinked technical terms (add the ones that matter to --terms):', '; '.join(r['advisory'][:10]))
    print('\nPer-diagram measurements (evidence for R4/R8):')
    for m in diag:
        print(f'  {m["title"]}: {m["measured"]} texts measured, {m["not_measured"]} not measured, {len(m["small"])} under 9px, defects {m["defects"] or 0}, borderline {m["borderline"]}')
    failed = [r['rule'] for r in res if r['gated'] and r['status'] == 'FAIL']
    print('\nGATE:', 'FAIL: ' + ', '.join(failed) if failed else 'PASS')
    if a.json:
        os.makedirs(os.path.dirname(a.json) or '.', exist_ok=True)
        json.dump({'page': path, 'method': METHOD, 'diagrams': a.diagrams, 'results': res, 'diagram_measurements': diag, 'gate_failed': failed}, open(a.json, 'w'), indent=1)
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
