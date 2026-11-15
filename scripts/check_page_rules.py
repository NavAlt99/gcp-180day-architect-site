#!/usr/bin/env python3
"""Deterministic page-rule checks R1-R5 and R7-R13 on a built day page.

Usage:
  python3 scripts/check_page_rules.py --day 3
  python3 scripts/check_page_rules.py --day 3 --diagrams keep --terms "hypervisor,KVM" --json scratch/day-003-rules.json
  python3 scripts/check_page_rules.py --page /path/to/day-003.html

Reads days/day-NNN.html (or --page). Standard library only; Pillow with DejaVu fonts is used for
text widths when available (otherwise an average-character-width estimate, and the method is printed).
Exit status 1 when a gated rule fails. R4/R8 are gated only with --diagrams allow
(default); R12 is informational; R13 is gated only with --baseline; the remaining
implemented rules are gated.
"""
import argparse, collections, glob, hashlib, json, os, re, sys
from html.parser import HTMLParser

VOID = {'br', 'hr', 'img', 'meta', 'link', 'input', 'source', 'wbr', 'col', 'area', 'base', 'embed', 'param', 'track'}
STRUCT = {'Why today:', 'Where it sits:', 'Problem preview:', 'Subtopics in this discussion:',
          'Evidence limit:', 'Linked subtopics:'}
GOOGLE = 'http://www.google.com/search?q='
SKIP = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'code', 'samp', 'kbd', 'pre', 'figcaption', 'a', 'script', 'style', 'svg', 'title'}
STOP = {'RFC', 'NOT', 'AND', 'THE', 'FOR', 'YES', 'FALSE', 'TRUE'}
JACCARD_STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'have',
    'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was',
    'were', 'with', 'worked', 'dossier', 'starting', 'point',
}
SHELL_TAGS = {'nav', 'header', 'footer'}
SHELL_CLASS_PARTS = ('sprint-rail', 'foundation-rail', 'day-selector')


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
    links = [n.attrs.get('href', '') for n in nodes(root)
             if n.tag == 'link' and 'stylesheet' in n.attrs.get('rel', '').split()]
    shared = any(re.search(r'(?:^|/)assets/site\.css(?:[?#].*)?$', href) for href in links)
    items = []
    for style in (n for n in nodes(root) if n.tag == 'style'):
        for match in re.finditer(r'([^{}]+)\{([^}]*)\}', style.text()):
            selector, declarations = match.group(1).strip(), match.group(2)
            targets_day_content = re.search(r'(?:\.container\b|\.topic-card\b|technical|\.day\b)', selector, re.I)
            sets_width = re.search(r'(?<![-\w])(?:min-|max-)?width\s*:', declarations, re.I)
            if targets_day_content and sets_width:
                items.append(f'inline style width rule: {selector[:100]}')
    for n in nodes(root):
        if 'style' not in n.attrs:
            continue
        target = (n.attrs.get('id', '') + ' ' + n.attrs.get('class', '')).lower()
        if (re.search(r'(container|topic-card|technical)', target)
                and re.search(r'(?<![-\w])(?:min-|max-)?width\s*:', n.attrs['style'], re.I)):
            items.append(f'inline style attribute width rule on {n.tag}#{n.attrs.get("id", "")}')
    overrides = len(items)
    if not shared:
        items.insert(0, 'missing linked assets/site.css')
    return result('R5 shared width', 'FAIL' if items else 'PASS', True,
                  f'assets/site.css linked={shared}; {overrides} inline/per-day width override(s)', items)


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


# ---------------------------------------------------------------- R10 / R11 / R12
def content_text(n):
    """Visible text excluding command/code descendants."""
    if isinstance(n, str):
        return n
    if n.tag in ('pre', 'code', 'samp', 'kbd'):
        return ''
    return ''.join(content_text(k) for k in n.kids)


def is_shell(n):
    classes = ' '.join(n.cls())
    return n.tag in SHELL_TAGS or any(part in classes for part in SHELL_CLASS_PARTS)


def main_content_roots(root):
    mains = [n for n in nodes(root) if n.tag == 'main']
    if mains:
        return mains
    bodies = [n for n in nodes(root) if n.tag == 'body']
    return bodies or [root]


def normalize_prose(text):
    return re.sub(r'\s+', ' ', text).strip().lower()


def r10_repeats(root):
    occurrences = collections.defaultdict(list)

    def walk(n, heading_id=None, shell=False):
        if isinstance(n, str):
            return heading_id
        shell = shell or is_shell(n)
        if shell or n.tag in ('pre', 'code', 'samp', 'kbd'):
            return heading_id
        if n.tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            heading_id = n.attrs.get('id') or heading_id
        if n.tag in ('p', 'li', 'td', 'th', 'dd', 'figcaption'):
            prose = normalize_prose(content_text(n))
            if len(prose) >= 80:
                occurrences[prose].append({'tag': n.tag, 'heading_id': heading_id or '(no heading id)'})
        for kid in n.kids:
            heading_id = walk(kid, heading_id, shell)
        return heading_id

    for content_root in main_content_roots(root):
        walk(content_root)
    repeated = {}
    for prose, occurrences_for_text in occurrences.items():
        if len(occurrences_for_text) > 1:
            repeated[hashlib.sha256(prose.encode()).hexdigest()[:16]] = {
                'text': prose,
                'count': len(occurrences_for_text),
                'preview': prose[:60],
                'occurrences': occurrences_for_text,
            }
    return repeated


def r10_baseline_entry(repeated):
    return {digest: {'count': item['count'], 'preview': item['preview']}
            for digest, item in sorted(repeated.items())}


def check_r10(root, baseline=None, gated=True):
    repeated = r10_repeats(root)
    grandfathered, failures, items = 0, 0, []
    baseline = baseline or {}
    for digest, item in sorted(repeated.items(), key=lambda pair: (-pair[1]['count'], pair[0])):
        prior = baseline.get(digest)
        allowed = prior is not None and item['count'] <= prior.get('count', -1)
        grandfathered += int(allowed)
        failures += int(not allowed)
        headings = ','.join(occurrence['heading_id'] for occurrence in item['occurrences'])
        state = f'grandfathered baseline={prior["count"]}' if allowed else 'new' if prior is None else f'increased baseline={prior["count"]}'
        items.append(f'{digest} "{item["preview"]}" count={item["count"]} {state}; headings={headings}')
    return result('R10 repeated paragraphs', 'FAIL' if failures else 'PASS', gated,
                  f'{len(repeated)} total repeat(s), {grandfathered} grandfathered, {failures} new/increased', items)


def word_set(text):
    return {word for word in re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower())
            if word not in JACCARD_STOPWORDS}


def jaccard(left, right):
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def dossier_block(n):
    current = n
    while current is not None:
        if 'worked-example' in current.cls():
            return current
        current = current.parent
    return n.parent or n


def dossier_heading(block):
    return next((candidate for candidate in dossier_nodes(block)
                 if isinstance(candidate, Node)
                 and candidate.tag in ('strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6')
                 and re.match(r'^Worked dossier\s+\d+\s*:', candidate.text().strip(), re.I)), None)


def dossier_nodes(block):
    yield block
    for kid in block.kids:
        if not isinstance(kid, Node):
            continue
        if kid is not block and 'worked-example' in kid.cls():
            continue
        yield from dossier_nodes(kid)


def check_r11(root, gated=True):
    starts = []
    for n in nodes(root):
        if n.tag not in ('p', 'li', 'dd'):
            continue
        text = normalize_prose(content_text(n))
        if text.startswith('worked starting point:'):
            starts.append(n)
    if not starts:
        return result('R11 starting point evidence', 'N/A', gated, 'no worked dossiers found')
    failures, items = 0, []
    for start in starts:
        block = dossier_block(start)
        heading_node = dossier_heading(block)
        heading = re.sub(r'^Worked dossier\s+\d+\s*:\s*', '', heading_node.text().strip(), flags=re.I) if heading_node else ''
        starting = re.sub(r'^Worked starting point:\s*', '', content_text(start).strip(), flags=re.I)
        digit = bool(re.search(r'\d', starting))
        quoted = bool(re.search(r'(["\u201c\u201d][^"\u201c\u201d]+["\u201c\u201d]|\'[^\']+\'|[\u2018\u2019][^\u2018\u2019]+[\u2018\u2019])', starting))
        code = any(candidate.tag in ('samp', 'code', 'kbd', 'pre') for candidate in dossier_nodes(block))
        concrete = digit or quoted or code
        overlap = jaccard(word_set(starting), word_set(heading))
        failed = heading_node is None or not concrete or overlap >= 0.6
        failures += int(failed)
        marker = 'digit' if digit else 'quoted string' if quoted else 'code element' if code else 'none'
        items.append(f'{heading or "(dossier heading missing)"}: concrete={marker}; jaccard={overlap:.3f}')
    return result('R11 starting point evidence', 'FAIL' if failures else 'PASS', gated,
                  f'{len(starts)} starting point(s), {failures} failure(s); requires concrete marker and Jaccard < 0.600', items)


def dossier_counts(root):
    counts = {}
    for topic in (n for n in nodes(root)
                  if n.tag == 'article' and re.fullmatch(r'topic-\d+-technical', n.attrs.get('id', ''))):
        dossier_headings = [candidate for candidate in nodes(topic)
                            if isinstance(candidate, Node)
                            and candidate.tag in ('strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6')
                            and re.match(r'^Worked dossier\s+\d+\s*:', candidate.text().strip(), re.I)]
        counts[topic.attrs['id']] = len(dossier_headings)
    return dict(sorted(counts.items()))


def check_r12(root):
    counts = dossier_counts(root)
    items = [f'{topic}: {count}' for topic, count in counts.items()]
    return result('R12 dossier counts', 'N/A', False,
                  f'{len(counts)} topic(s); informational only, no maximum', items)


# ---------------------------------------------------------------- R13
def first_child_node(n):
    return next((kid for kid in n.kids if not (isinstance(kid, str) and not kid.strip())), None)


def protected_snapshot(root, page):
    topic_ids = sorted({n.attrs['id'] for n in nodes(root)
                        if re.fullmatch(r'topic-\d+-(?:overview|technical|problem|lab)', n.attrs.get('id', ''))})
    subtopic_ids = sorted({n.attrs['id'] for n in nodes(root)
                           if n.tag in ('h3', 'h4', 'h5', 'h6')
                           and re.fullmatch(r'topic-\d+-subtopic-\d+', n.attrs.get('id', ''))})
    bullets = {subtopic_id: 0 for subtopic_id in subtopic_ids}
    for technical in (n for n in nodes(root)
                      if n.tag == 'article' and re.fullmatch(r'topic-\d+-technical', n.attrs.get('id', ''))):
        current = None
        for candidate in nodes(technical):
            if candidate.tag in ('h3', 'h4', 'h5', 'h6') and candidate.attrs.get('id') in bullets:
                current = candidate.attrs['id']
            elif current and candidate.tag == 'li':
                first = first_child_node(candidate)
                if isinstance(first, Node) and first.tag == 'strong' and 'side-heading' in first.cls():
                    bullets[current] += 1
    labs = {}
    for lab in (n for n in nodes(root)
                if n.tag == 'article' and re.fullmatch(r'topic-\d+-lab', n.attrs.get('id', ''))):
        labs[lab.attrs['id']] = sum(1 for candidate in nodes(lab)
                                     if candidate.tag == 'li'
                                     and re.match(r'^Stage\s+[1-8]\s*:', candidate.text().strip(), re.I))
    urls = sorted({n.attrs.get('href', '') for n in nodes(root)
                   if n.tag == 'a' and re.match(r'https?://', n.attrs.get('href', '')) and not is_google(n)})
    evidence_limits = sum(1 for n in nodes(root)
                          if n.tag in ('strong', 'th') and normalize_prose(n.text()).rstrip(':') == 'evidence limit')
    incidents = sum(1 for n in nodes(root)
                    if n.tag == 'article' and re.fullmatch(r'topic-\d+-problem', n.attrs.get('id', '')))
    return {
        'schema_version': 2,
        'page': page,
        'topic_ids': topic_ids,
        'subtopic_heading_ids': subtopic_ids,
        'labelled_bullets_per_subtopic': bullets,
        'dossiers_per_topic': dossier_counts(root),
        'lab_stages_per_lab': dict(sorted(labs.items())),
        'source_urls': urls,
        'code_blocks': sum(1 for n in nodes(root) if n.tag == 'pre'),
        'evidence_limits': evidence_limits,
        'incidents': incidents,
    }


def check_r13(current, baseline):
    if baseline is None:
        return result('R13 preservation guard', 'N/A', False, 'no baseline supplied')
    items = []
    for key in ('topic_ids', 'subtopic_heading_ids', 'source_urls'):
        missing = sorted(set(baseline.get(key, [])) - set(current.get(key, [])))
        if missing:
            items.append(f'{key}: missing {missing}')
    for key in ('labelled_bullets_per_subtopic', 'dossiers_per_topic', 'lab_stages_per_lab'):
        for identifier, old_count in baseline.get(key, {}).items():
            if identifier not in current.get(key, {}):
                items.append(f'{key}: missing ID {identifier}')
            elif current[key][identifier] < old_count:
                items.append(f'{key}: {identifier} decreased {old_count} -> {current[key][identifier]}')
    for key in ('code_blocks', 'evidence_limits', 'incidents'):
        if current.get(key, 0) < baseline.get(key, 0):
            items.append(f'{key}: decreased {baseline.get(key, 0)} -> {current.get(key, 0)}')
    return result('R13 preservation guard', 'FAIL' if items else 'PASS', True,
                  f'{len(items)} protected decrease(s) or missing ID(s)', items)


# ---------------------------------------------------------------- main
def read_json(path):
    with open(path, encoding='utf-8') as stream:
        return json.load(stream)


def write_json(path, value):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as stream:
        json.dump(value, stream, indent=1, sort_keys=True)
        stream.write('\n')


def page_day(path, day=None):
    if day:
        return day
    match = re.search(r'day-(\d{3})\.html$', path)
    return int(match.group(1)) if match else None


def initialize_r10_baseline(path):
    if os.path.exists(path):
        raise SystemExit(f'REFUSED: R10 baseline already exists: {path}')
    baseline = {}
    for page in sorted(glob.glob('days/day-[0-9][0-9][0-9].html')):
        day = page_day(page)
        html = open(page, encoding='utf-8').read()
        builder = Builder(); builder.feed(html)
        baseline[str(day)] = r10_baseline_entry(r10_repeats(builder.root))
    write_json(path, baseline)
    print(f'Initialized R10 baseline for {len(baseline)} day(s): {path} ({os.path.getsize(path)} bytes)')


def refresh_r10_baseline(path, day, repeated):
    if not os.path.exists(path):
        raise SystemExit(f'REFUSED: R10 baseline does not exist: {path}')
    baseline = read_json(path)
    old = baseline.get(str(day))
    if old is None:
        raise SystemExit(f'REFUSED: R10 baseline has no Day {day} entry')
    current = r10_baseline_entry(repeated)
    new_or_higher = []
    for digest, item in current.items():
        if digest not in old:
            new_or_higher.append(f'{digest} new: {item["preview"]}')
        elif item['count'] > old[digest].get('count', -1):
            new_or_higher.append(f'{digest} increased {old[digest].get("count")} -> {item["count"]}: {item["preview"]}')
    if new_or_higher:
        raise SystemExit('REFUSED: R10 baseline refresh may only shrink:\n  ' + '\n  '.join(new_or_higher[:25]))
    baseline[str(day)] = current
    write_json(path, baseline)
    print(f'Refreshed Day {day} R10 baseline shrink-only: {len(old)} -> {len(current)} repeat(s)')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--day', type=int)
    ap.add_argument('--page')
    ap.add_argument('--diagrams', choices=['keep', 'allow'], default='allow')
    ap.add_argument('--terms', default='', help='comma-separated terms that must be linked (R3)')
    ap.add_argument('--terms-file')
    ap.add_argument('--json')
    ap.add_argument('--snapshot', help='write the current R13 protected-content snapshot')
    ap.add_argument('--baseline', help='compare R13 protected content with this snapshot')
    ap.add_argument('--r10-baseline', help='R10 repeat baseline; defaults to scratch/baseline/r10-existing-repeats.json when present')
    ap.add_argument('--init-r10-baseline', action='store_true', help='initialize the R10 baseline once from all built day pages')
    ap.add_argument('--refresh-r10-baseline', action='store_true', help='refresh this day in the R10 baseline, refusing new or increased repeats')
    a = ap.parse_args()
    default_r10 = 'scratch/baseline/r10-existing-repeats.json'
    r10_path = a.r10_baseline or (default_r10 if os.path.exists(default_r10) else None)
    if a.init_r10_baseline:
        initialize_r10_baseline(a.r10_baseline or default_r10)
        return
    if not a.page and not a.day:
        ap.error('give --day or --page')
    path = a.page or f'days/day-{a.day:03d}.html'
    html = open(path, encoding='utf-8').read()
    b = Builder(); b.feed(html); root = b.root
    ids = {n.attrs['id'] for n in nodes(root) if isinstance(n, Node) and 'id' in n.attrs}
    terms = [t.strip() for t in a.terms.split(',') if t.strip()]
    if a.terms_file:
        terms += [l.strip() for l in open(a.terms_file) if l.strip() and not l.startswith('#')]
    day = page_day(path, a.day)
    repeated = r10_repeats(root)
    if a.refresh_r10_baseline:
        if not r10_path:
            raise SystemExit('REFUSED: --refresh-r10-baseline needs an existing --r10-baseline')
        if day is None:
            raise SystemExit('REFUSED: cannot derive day for R10 baseline refresh')
        refresh_r10_baseline(r10_path, day, repeated)
        return
    r10_data = read_json(r10_path) if r10_path else {}
    r10_for_day = r10_data.get(str(day), {}) if day is not None else {}
    protected = protected_snapshot(root, path)
    r13_baseline = read_json(a.baseline) if a.baseline else None
    gate = a.diagrams == 'allow'
    r4, r8, diag = check_diagrams(root, gate)
    res = [check_r1(root, ids), check_r2(root), check_r3(root, terms), r4, check_r5(root),
           check_r7(html), r8, check_r10(root, r10_for_day), check_r11(root), check_r12(root),
           check_r13(protected, r13_baseline)]
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
    print('\nNot checked: semantic distinctness of dossiers; meaning preservation of rewritten text (manual review).')
    failed = [r['rule'] for r in res if r['gated'] and r['status'] == 'FAIL']
    print('\nGATE:', 'FAIL: ' + ', '.join(failed) if failed else 'PASS')
    if a.json:
        write_json(a.json, {'page': path, 'method': METHOD, 'diagrams': a.diagrams,
                            'r10_baseline': r10_path, 'results': res,
                            'diagram_measurements': diag, 'protected_snapshot': protected,
                            'gate_failed': failed})
    if a.snapshot:
        write_json(a.snapshot, protected)
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
