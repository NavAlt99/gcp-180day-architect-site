import json
import re
import urllib.parse
from html import escape

with open('scratch/day_data_011.py', 'r') as f:
    text = f.read()

# Load key terms from audit ledger
with open('scratch/audits/day-011-audit.json', 'r') as f:
    audit = json.load(f)

key_terms = audit['key_terms']
sorted_terms = sorted(key_terms, key=lambda x: -len(x))

# We will apply S3 to the technical text of each topic.
# In scratch/day_data_011.py, each topic technical discussion contains subtopics:
# topic-01-subtopic-1..5 and topic-02-subtopic-1..5.

def link_subtopic_text(sub_html, terms):
    # Within each subtopic, link first occurrence of each term outside headings, kbd, code, figcaption, or existing link
    # If the term is inside strong.keyword, place the anchor inside the strong.keyword span:
    # <strong class="keyword"><a href="http://www.google.com/search?q=TERM" rel="noopener" target="_blank">TERM</a></strong>
    
    # First, handle all strong.keyword spans that are not already linked:
    def kw_repl(m):
        inner = m.group(1)
        if '<a ' in inner:
            return m.group(0)
        clean = re.sub(r'<[^>]+>', '', inner).strip()
        url = 'http://www.google.com/search?q=' + urllib.parse.quote_plus(clean)
        return f'<strong class="keyword"><a href="{url}" rel="noopener" target="_blank">{inner}</a></strong>'
    
    sub_html = re.sub(r'<strong class="keyword">(.*?)</strong>', kw_repl, sub_html)
    return sub_html

# Let's inspect DATA['topics'][0]['technical'] and DATA['topics'][1]['technical']
# We can do this cleanly via a post-processing helper appended to day_data_011.py or by modifying technical strings.
