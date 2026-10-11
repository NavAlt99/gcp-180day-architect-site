import re
import urllib.parse
import json

with open('scratch/day_data_003.py', 'r') as f:
    text = f.read()

subtopics_map = {
    'topic-01': [
        ('topic-01-subtopic-1', 'IPv6 128-bit address architecture and canonical representation'),
        ('topic-01-subtopic-2', 'Address scoping boundaries (Link-Local, Unique Local, and Global Unicast)'),
        ('topic-01-subtopic-3', 'Neighbor Discovery Protocol (NDP) mechanics (RS/RA, NS/NA, SLAAC, DAD)'),
        ('topic-01-subtopic-4', 'Dual-stack VPC architecture, Happy Eyeballs (RFC 8305), and Google Cloud edge ingress')
    ],
    'topic-02': [
        ('topic-02-subtopic-1', 'Hierarchical DNS architecture and authoritative name servers'),
        ('topic-02-subtopic-2', 'The resolution pipeline (stub resolver, recursive resolver, iterative referral chain)'),
        ('topic-02-subtopic-3', 'Core DNS resource record types and TTL caching dynamics'),
        ('topic-02-subtopic-4', 'DNS security protocols (DNSSEC, DoT, DoH) and Google Cloud DNS managed private zones')
    ],
    'topic-03': [
        ('topic-03-subtopic-1', 'Transport protocol paradigms (TCP vs UDP vs QUIC)'),
        ('topic-03-subtopic-2', 'BSD socket addressing, socket types, and the complete socket lifecycle API'),
        ('topic-03-subtopic-3', 'I/O multiplexing architectures (select, poll, epoll, io_uring, SO_REUSEPORT)'),
        ('topic-03-subtopic-4', 'TCP connection management (3-way/4-way handshakes, TIME_WAIT, RST), flow control, congestion algorithms, and socket buffers'),
        ('topic-03-subtopic-5', 'Packet inspection and analysis with tcpdump')
    ]
}

# 1. R1: Add Linked subtopics to PART1_HTML
old_part1_card = '''<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> {prev}</p>
<p><a href="#{key}-technical">Technical discussion →</a> <a href="#{key}-problem">Real-world problem →</a> <a href="#{key}-lab">Step-by-step lab →</a></p>'''

subtopics_dict_code = """SUBTOPICS_MAP = {
    'topic-01': [
        ('topic-01-subtopic-1', 'IPv6 128-bit address architecture and canonical representation'),
        ('topic-01-subtopic-2', 'Address scoping boundaries (Link-Local, Unique Local, and Global Unicast)'),
        ('topic-01-subtopic-3', 'Neighbor Discovery Protocol (NDP) mechanics (RS/RA, NS/NA, SLAAC, DAD)'),
        ('topic-01-subtopic-4', 'Dual-stack VPC architecture, Happy Eyeballs (RFC 8305), and Google Cloud edge ingress')
    ],
    'topic-02': [
        ('topic-02-subtopic-1', 'Hierarchical DNS architecture and authoritative name servers'),
        ('topic-02-subtopic-2', 'The resolution pipeline (stub resolver, recursive resolver, iterative referral chain)'),
        ('topic-02-subtopic-3', 'Core DNS resource record types and TTL caching dynamics'),
        ('topic-02-subtopic-4', 'DNS security protocols (DNSSEC, DoT, DoH) and Google Cloud DNS managed private zones')
    ],
    'topic-03': [
        ('topic-03-subtopic-1', 'Transport protocol paradigms (TCP vs UDP vs QUIC)'),
        ('topic-03-subtopic-2', 'BSD socket addressing, socket types, and the complete socket lifecycle API'),
        ('topic-03-subtopic-3', 'I/O multiplexing architectures (select, poll, epoll, io_uring, SO_REUSEPORT)'),
        ('topic-03-subtopic-4', 'TCP connection management (3-way/4-way handshakes, TIME_WAIT, RST), flow control, congestion algorithms, and socket buffers'),
        ('topic-03-subtopic-5', 'Packet inspection and analysis with tcpdump')
    ]
}

def render_linked_subtopics(key):
    items = SUBTOPICS_MAP.get(key, [])
    lis = ''.join(f'<li><a href="#{sid}">{stitle}</a></li>' for sid, stitle in items)
    return f'<p><strong class="side-heading">Linked subtopics:</strong></p><ul>{lis}</ul>'
"""

new_part1_card = '''<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> {prev}</p>
{render_linked_subtopics(key)}
<p><a href="#{key}-technical">Technical discussion →</a> <a href="#{key}-problem">Real-world problem →</a> <a href="#{key}-lab">Step-by-step lab →</a></p>'''

assert old_part1_card in text, "old_part1_card not found!"
text = subtopics_dict_code + "\n" + text.replace(old_part1_card, new_part1_card, 1)

# 2. R1: Add anchor IDs to subtopic headers using HTML <h3 id="...">
for tkey, items in subtopics_map.items():
    for sid, stitle in items:
        old_h3 = f'### {stitle}\\n"'
        new_h3 = f'<h3 id=\'{sid}\'>{stitle}</h3>\\n"'
        assert old_h3 in text, f"Header {stitle} not found!"
        text = text.replace(old_h3, new_h3, 1)

# 3. R2: Convert side-headings in technical discussions to bullet points
text = text.replace(
    '"<strong class=\'side-heading\'>What it is in general:</strong> ',
    '"<ul>\\n<li><strong class=\'side-heading\'>What it is in general:</strong> '
)
text = text.replace(
    '"<strong class=\'side-heading\'>Relevance to a cloud architect:</strong> ',
    '"</li>\\n<li><strong class=\'side-heading\'>Relevance to a cloud architect:</strong> '
)
text = text.replace(
    '"<strong class=\'side-heading\'>Relevance to GCP:</strong> ',
    '"</li>\\n<li><strong class=\'side-heading\'>Relevance to GCP:</strong> '
)

gcp_ends = [
    'and firewall rules across Andromeda virtual network fabrics.\\n\\n"\n\n            "<h3 id=\'topic-01-subtopic-2\'>',
    'ne instances or GKE pods over IPv4 or internal ULA/GUA IPv6.\\n\\n"\n\n            "<h3 id=\'topic-01-subtopic-3\'>',
    'ges](https://cloud.google.com/vpc/docs/subnets#ipv6-ranges).\\n\\n"\n\n            "<h3 id=\'topic-01-subtopic-4\'>',
    'Compute Engine VMs or GKE clusters.\\n\\n"\n\n            "<strong class=\'side-heading\'>Concrete example:</strong>',
    '00% availability SLA and ultra-low lookup latency worldwide.\\n\\n"\n\n            "<h3 id=\'topic-02-subtopic-2\'>',
    'pt inbound queries via private Cloud DNS forwarding targets.\\n\\n"\n\n            "<h3 id=\'topic-02-subtopic-3\'>',
    'fic percentages dynamically between regions during releases.\\n\\n"\n\n            "<h3 id=\'topic-02-subtopic-4\'>',
    'block malicious egress domains.\\n\\n"\n\n            "<strong class=\'side-heading\'>Concrete example:</strong>',
    'al TCP backbones to backend Compute Engine or GKE workloads.\\n\\n"\n\n            "<h3 id=\'topic-03-subtopic-2\'>',
    'port_range</samp>) to support high-throughput cloud proxies.\\n\\n"\n\n            "<h3 id=\'topic-03-subtopic-3\'>',
    'amp> to achieve millions of packets per second per instance.\\n\\n"\n\n            "<h3 id=\'topic-03-subtopic-4\'>',
    'via sysctl to maximize transfer speeds over long-haul paths.\\n\\n"\n\n            "<h3 id=\'topic-03-subtopic-5\'>',
    'ectors running tcpdump or Zeek.\\n\\n"\n\n            "<strong class=\'side-heading\'>Concrete example:</strong>'
]

for item in gcp_ends:
    assert item in text, f"GCP ending item not found: {item[:40]}"
    new_item = item.replace('.\\n\\n"', '.</li>\\n</ul>\\n\\n"')
    text = text.replace(item, new_item, 1)

# Concrete examples
text = text.replace(
    '"<strong class=\'side-heading\'>Concrete example:</strong> ',
    '"<ul>\\n<li><strong class=\'side-heading\'>Concrete example:</strong> '
)
concrete_ends = [
    'stores immediate socket connectivity.\\n\\n"\n\n            "<strong class=\'side-heading\'>Evidence limit:</strong>',
    'seamless cutover within one minute.\\n\\n"\n\n            "<strong class=\'side-heading\'>Evidence limit:</strong>',
    'he drops and absorbs traffic spikes.\\n\\n"\n\n            "<strong class=\'side-heading\'>Evidence limit:</strong>'
]

for item in concrete_ends:
    assert item in text, f"Concrete ending item not found: {item[:40]}"
    new_item = item.replace('.\\n\\n"', '.</li>\\n</ul>\\n\\n"')
    text = text.replace(item, new_item, 1)

# 4. R3: Wrap discovery search links in OVERVIEWS
text = text.replace(
    '<strong class="keyword">IPv6</strong>',
    '<strong class="keyword"><a href="http://www.google.com/search?q=IPv6" rel="noopener" target="_blank">IPv6</a></strong>'
)
text = text.replace(
    '<strong class="keyword">DNS</strong>',
    '<strong class="keyword"><a href="http://www.google.com/search?q=DNS" rel="noopener" target="_blank">DNS</a></strong>'
)
text = text.replace(
    '<strong class="keyword">Transport protocols</strong>',
    '<strong class="keyword"><a href="http://www.google.com/search?q=Transport+protocols" rel="noopener" target="_blank">Transport protocols</a></strong>'
)

# In technical discussions:
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
    q = urllib.parse.quote_plus(kw)
    new_span = f"<strong class='keyword'><a href=\'http://www.google.com/search?q={q}\' rel=\'noopener\' target=\'_blank\'>{kw}</a></strong>"
    assert old_span in text, f"Keyword span not found: {old_span}"
    text = text.replace(old_span, new_span, 1)

with open('scratch/day_data_003.py', 'w') as f:
    f.write(text)

print("Applied R1, R2, R3 with <h3 id='...'> successfully!")
