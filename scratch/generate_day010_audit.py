import json
import hashlib
import re
import urllib.parse
from bs4 import BeautifulSoup
from PIL import ImageFont

spec_path = "scratch/day_data_010.py"
spec_text = open(spec_path).read()
spec_sha256 = hashlib.sha256(open(spec_path, "rb").read()).hexdigest()

html_path = "days/day-010.html"
html_text = open(html_path).read()
soup = BeautifulSoup(html_text, "html.parser")

font_cache = {}
def get_font(size, bold=False):
    key = (size, bold)
    if key not in font_cache:
        font_cache[key] = ImageFont.truetype('DejaVuSans.ttf', size)
    return font_cache[key]

def get_text_width(text, size, bold=False):
    f = get_font(size, bold)
    bbox = f.getbbox(text)
    w = bbox[2] - bbox[0]
    if bold:
        w *= 1.07
    return w

def get_matrix_transform(el):
    tx, ty = 0.0, 0.0
    curr = el
    while curr and curr.name != 'svg':
        trans = curr.get('transform', '')
        if 'translate' in trans:
            m = re.search(r'translate\(\s*([0-9.-]+)[,\s]+([0-9.-]+)\s*\)', trans)
            if m:
                tx += float(m.group(1))
                ty += float(m.group(2))
        curr = curr.parent
    return tx, ty

# Extract all unlinked strong.keyword
unlinked_keywords = []
for t_idx in [1, 2, 3]:
    tech = soup.find(id=f'topic-0{t_idx}-technical')
    subtopic_headers = tech.find_all('h4', id=re.compile(f'topic-0{t_idx}-subtopic-'))
    for s_idx, h4 in enumerate(subtopic_headers):
        sub_id = h4.get('id')
        curr = h4.next_sibling
        seen_terms = set()
        while curr:
            if getattr(curr, 'name', None) == 'h4':
                break
            if hasattr(curr, 'find_all'):
                kws = curr.find_all('strong', class_='keyword')
                for kw in kws:
                    txt = kw.get_text().strip()
                    if txt not in seen_terms:
                        seen_terms.add(txt)
                        if not kw.find('a'):
                            term_q = urllib.parse.quote_plus(txt)
                            old_str = str(kw)
                            new_str = f'<strong class="keyword"><a href="http://www.google.com/search?q={term_q}" rel="noopener" target="_blank">{txt}</a></strong>'
                            unlinked_keywords.append({
                                'topic': f'topic-0{t_idx}',
                                'subtopic': sub_id,
                                'term': txt,
                                'old_str': old_str,
                                'new_str': new_str
                            })
            curr = curr.next_sibling

all_key_terms = sorted(list(set(x['term'] for x in unlinked_keywords)))

# SVG Collisions
svgs = soup.find_all('svg')
svg_collisions = []
for idx, svg in enumerate(svgs):
    vb = svg.get('viewBox') or svg.get('viewbox') or '0 0 1000 1000'
    vb_parts = [float(x) for x in vb.split()]
    vb_w, vb_h = vb_parts[2], vb_parts[3]
    texts = svg.find_all('text')
    images = svg.find_all('image')
    title = svg.get('aria-labelledby', f'SVG-{idx+1}')
    
    for t in texts:
        txt = t.get_text().strip()
        if not txt:
            continue
        try:
            x_local = float(t.get('x', 0))
            y_local = float(t.get('y', 0))
        except ValueError:
            continue
        tx, ty = get_matrix_transform(t)
        x = x_local + tx
        y = y_local + ty
        anchor = t.get('text-anchor', 'start')
        fs = float(re.sub(r'[^0-9.]', '', t.get('font-size', '12')) or 12)
        fw = t.get('font-weight', 'normal')
        is_bold = (fw == 'bold' or 'bold' in t.get('class', []))
        w = get_text_width(txt, int(fs), is_bold)
        h = fs
        
        if anchor == 'middle':
            x0 = x - w/2
            x1 = x + w/2
        elif anchor == 'end':
            x0 = x - w
            x1 = x
        else:
            x0 = x
            x1 = x + w
        y0 = y - h
        y1 = y
        
        # Check outside viewBox (with 4px margin)
        if x0 < 0 or y0 < 0 or x1 > vb_w or y1 > vb_h:
            svg_collisions.append({
                'svg_idx': idx + 1,
                'title': title,
                'type': 'viewbox_clip',
                'desc': f'Text "{txt}" extends outside viewBox ({vb_w}x{vb_h}) with bounds ({x0:.1f}, {y0:.1f}, {x1:.1f}, {y1:.1f})'
            })
            
        for img in images:
            try:
                ix_loc = float(img.get('x', 0))
                iy_loc = float(img.get('y', 0))
                iw = float(img.get('width', 0))
                ih = float(img.get('height', 0))
            except ValueError:
                continue
            itx, ity = get_matrix_transform(img)
            ix = ix_loc + itx
            iy = iy_loc + ity
            
            if not (x1 + 4 < ix or x0 - 4 > ix + iw or y1 + 4 < iy or y0 - 4 > iy + ih):
                dx = max(0, min(x1, ix+iw) - max(x0, ix))
                dy = max(0, min(y1, iy+ih) - max(y0, iy))
                svg_collisions.append({
                    'svg_idx': idx + 1,
                    'title': title,
                    'type': 'icon_collision',
                    'desc': f'Text "{txt}" intersects icon at ({ix}, {iy}, {iw}x{ih}) with overlap dx={dx:.1f}, dy={dy:.1f}'
                })

print(f'Total key terms: {len(all_key_terms)}')
print(f'Total unlinked keyword occurrences: {len(unlinked_keywords)}')
print(f'Total SVG collision issues: {len(svg_collisions)}')
