import re
import urllib.parse
import json

with open('scratch/day_data_003.py', 'r') as f:
    text = f.read()

with open('scratch/audits/day-003-audit.json', 'r') as f:
    audit = json.load(f)

key_terms = audit['key_terms']
# Sort key_terms descending by length so longer phrases match before substrings
key_terms = sorted(key_terms, key=len, reverse=True)

# Helper function to wrap term in Google search link
def make_search_link(term, display_text):
    q = urllib.parse.quote_plus(term)
    return f'<a href="http://www.google.com/search?q={q}" rel="noopener" target="_blank">{display_text}</a>'

# 1. Wrap key terms in OVERVIEWS cards (in body text)
# In OVERVIEWS:
# (key, title, body, why, where, prev)
# Let's inspect OVERVIEWS in day_data_003.py:
# body starts with '<strong class="keyword">TERM</strong>'
# Let's replace '<strong class="keyword">TERM</strong>' with '<strong class="keyword"><a href="...">TERM</a></strong>'

text = text.replace(
    '<strong class="keyword">IPv6</strong>',
    f'<strong class="keyword">{make_search_link("IPv6", "IPv6")}</strong>'
)
text = text.replace(
    '<strong class="keyword">DNS</strong>',
    f'<strong class="keyword">{make_search_link("DNS", "DNS")}</strong>'
)
text = text.replace(
    '<strong class="keyword">Transport protocols</strong>',
    f'<strong class="keyword">{make_search_link("Transport protocols", "Transport protocols")}</strong>'
)

# 2. In technical discussions, wrap the strong.keyword occurrences:
tech_keywords = [
    'Internet Protocol version 6 (IPv6)',
    'address scopes',
    'Neighbor Discovery Protocol (NDP)',
    'Dual-stack architecture',
    'Domain Name System (DNS)',
    'DNS resolution pipeline',
    'Resource Records (RRs)',
    'Transport layer protocols',
    'Berkeley Software Distribution (BSD) sockets',
    'I/O multiplexing',
    'TCP connection management',
    'tcpdump'
]

for kw in tech_keywords:
    old_span = f"<strong class='keyword'>{kw}</strong>"
    new_span = f"<strong class='keyword'>{make_search_link(kw, kw)}</strong>"
    assert old_span in text, f"Keyword span not found: {old_span}"
    text = text.replace(old_span, new_span, 1)

with open('scratch/day_data_003.py', 'w') as f:
    f.write(text)

print("Applied R3 discovery links to scratch/day_data_003.py successfully!")
