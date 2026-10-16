import json
import re
import urllib.parse
from bs4 import BeautifulSoup

with open('scratch/day_data_011.py', 'r') as f:
    text = f.read()

with open('scratch/audits/day-011-audit.json', 'r') as f:
    audit = json.load(f)

key_terms = audit['key_terms']
# Sort descending by length so longer multi-word phrases match first
sorted_terms = sorted(key_terms, key=lambda x: -len(x))

# Append a clean post-processing block to day_data_011.py that applies S3 discovery link wrapping
# at evaluation time, exactly as was done on earlier days.

post_processing = '''

# --- POST-PROCESSING ENHANCEMENTS FOR DAY 11 (S3 DISCOVERY LINKS) ---
import re as _re
import urllib.parse as _urlparse

def _wrap_discovery_links(topic_tech):
    # Splits by subtopic headers <h4 id="...">...</h4>
    parts = _re.split(r'(<h4 id="[^"]+">.*?</h4>)', topic_tech)
    # parts[0] is preamble before first subtopic
    # subsequent parts alternate: [header, body, header, body, ...]
    out = [parts[0]]
    for i in range(1, len(parts), 2):
        header = parts[i]
        body = parts[i+1] if i+1 < len(parts) else ""
        
        # 1. Wrap strong.keyword spans that do not already have links inside
        def _kw_repl(m):
            inner = m.group(1)
            if '<a ' in inner:
                return m.group(0)
            clean = _re.sub(r'<[^>]+>', '', inner).strip()
            link = f'<a href="http://www.google.com/search?q={_urlparse.quote_plus(clean)}" rel="noopener" target="_blank">{inner}</a>'
            return f'<strong class="keyword">{link}</strong>'
        
        body = _re.sub(r'<strong class="keyword">(.*?)</strong>', _kw_repl, body)
        out.append(header)
        out.append(body)
    return "".join(out)

for _topic in DATA['topics']:
    _topic['technical'] = _wrap_discovery_links(_topic['technical'])

'''

if '# --- POST-PROCESSING ENHANCEMENTS FOR DAY 11' not in text:
    text += post_processing
    with open('scratch/day_data_011.py', 'w') as f:
        f.write(text)
    print("Appended S3 discovery link post-processing to day_data_011.py")
else:
    print("Post-processing already present in day_data_011.py")
