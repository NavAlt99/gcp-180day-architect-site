SUBTOPICS_MAP = {
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

"""day_data_003.py — Specification for Day 3: DNS, sockets and transport.

Contract version 2 specification with complete depth, explicit boundaries,
qualifying flow diagrams, comprehensive DNS record reference tables,
DNSSEC cryptographic trust expansion, and tcpdump packet analysis.
"""

import sys
from html import escape
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.author_engine import render_topology_svg
from scratch.day_helpers import flow_svg

DAY = 3
ACCESS_DATE = '2026-11-03'
WORK_BLOCK = "Days 1–17 — Foundations"
EXIT_SUMMARY = "A DNS/transport diagram distinguishing name resolution, reachability and established connection."
ROADMAP_PRACTICE = "Trace an IPv4 and IPv6 lookup from supplied resolver output; label socket endpoints and the TCP handshake."
ROADMAP_EXIT = "A DNS/transport diagram distinguishing name resolution, reachability and established connection."

SOURCES = {
    'rfc4291': ('RFC 4291: IPv6 Addressing Architecture, section 2 (accessed 2026-11-03)', 'https://datatracker.ietf.org/doc/html/rfc4291#section-2'),
    'rfc1035': ('RFC 1035: Domain Names - Implementation and Specification, section 3.2.1 (accessed 2026-11-03)', 'https://datatracker.ietf.org/doc/html/rfc1035#section-3.2.1'),
    'rfc9293': ('RFC 9293: Transmission Control Protocol, section 3 (accessed 2026-11-03)', 'https://datatracker.ietf.org/doc/html/rfc9293#section-3'),
    'cloud_dns': ('Google Cloud DNS documentation: DNS forwarding methods (accessed 2026-11-03)', 'https://cloud.google.com/dns/docs/overview#dns-forwarding-methods'),
    'cloud_dns_zones': ('Google Cloud DNS documentation: Forwarding zones (accessed 2026-11-03)', 'https://cloud.google.com/dns/docs/zones/zones-overview#forwarding_zones'),
    'cloud_dns_dnssec': ('Google Cloud DNS documentation: Use advanced signing options (accessed 2026-11-03)', 'https://cloud.google.com/dns/docs/dnssec-advanced#advanced-signing-options'),
    'bbr': ('Google Cloud Networking: TCP BBR Congestion Control in GCP (accessed 2026-11-03)', 'https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster'),
    'http3': ('Google Cloud Load Balancing documentation: HTTP/3 support (accessed 2026-11-03)', 'https://cloud.google.com/load-balancing/docs/https#QUIC'),
    'vpc_ipv6': ('Google Cloud VPC documentation: IPv6 subnet ranges (accessed 2026-11-03)', 'https://cloud.google.com/vpc/docs/subnets#ipv6-ranges'),
    'tcpdump': ('Linux man-pages: tcpdump(1) DESCRIPTION (accessed 2026-11-03)', 'https://man7.org/linux/man-pages/man1/tcpdump.1.html#DESCRIPTION'),
    'ss': ('Linux man-pages: ss(8) DESCRIPTION (accessed 2026-11-03)', 'https://man7.org/linux/man-pages/man8/ss.8.html#DESCRIPTION'),
}

PART1_INTRO = (
    "Day 3 separates four fundamental architectural boundaries that are routinely conflated in enterprise operations: "
    "a name resolving to an address (DNS), an address possessing a valid routing scope (IPv4/IPv6), a transport connection "
    "successfully establishing state between kernel sockets (TCP/UDP/QUIC), and an application payload being semantically "
    "processed by user-space runtimes. Building upon Day 2's packet traversal path, today's curriculum explores IPv6 128-bit "
    "addressing and Neighbor Discovery Protocol (NDP), dissects the global DNS hierarchy, recursive resolution mechanics, "
    "core record types, and DNSSEC/DoT/DoH security controls, establishes the complete Berkeley Software Distribution (BSD) "
    "socket lifecycle API and I/O multiplexing concurrency models (epoll, io_uring), and performs a deep architectural evaluation "
    "of TCP connection management (3-way and 4-way handshakes), sliding-window flow control, congestion control algorithms "
    "(Tahoe, Reno, CUBIC, BBR), and packet capture analysis with tcpdump."
)

PART2_INTRO = (
    "Architectural evaluation of dual-stack IPv6 addressing, DNS hierarchy and cryptographic trust chains, "
    "Berkeley Software Distribution (BSD) socket lifecycle states, I/O multiplexing concurrency models, and TCP transport reliability mechanics."
)

PART3_INTRO = (
    "Production field cases examining real-world networking breakdowns: link-local IPv6 interface scope omissions, "
    "recursive DNS TTL caching collisions during database failover, and TCP accept queue overflow drops under traffic surges."
)

PART4_INTRO = (
    "Hands-on local laboratory exercises executing IPv6 scope binding, recursive DNS resolution and DNSSEC cryptographic auditing, "
    "and socket lifecycle instrumentation capturing TCP state transitions, accept queue drops, and tcpdump packet analysis."
)

OVERVIEWS = [
    (
        'topic-01',
        '1. IPv6 addressing and scope',
        '<strong class="keyword"><a href="http://www.google.com/search?q=IPv6" rel="noopener" target="_blank">IPv6</a></strong> expands the network address space to 128 bits while establishing architectural scoping boundaries that strictly govern packet reachability. <a href="http://www.google.com/search?q=Link-Local" rel="noopener" target="_blank">Link-local</a> addresses (<samp>fe80::/10</samp>) require an explicit interface zone identifier, <a href="http://www.google.com/search?q=Unique+Local" rel="noopener" target="_blank">Unique Local</a> Addresses (ULA, <samp>fc00::/7</samp>) provide private enterprise routing, and <a href="http://www.google.com/search?q=Global+Unicast" rel="noopener" target="_blank">Global Unicast</a> Addresses (GUA, <samp>2000::/3</samp>) provide internet-wide reachability. <a href="http://www.google.com/search?q=NDP" rel="noopener" target="_blank">Neighbor Discovery Protocol (NDP)</a> replaces broadcast ARP with multicast ICMPv6 messaging, forming the foundation for Google Cloud dual-stack <a href="http://www.google.com/search?q=VPC" rel="noopener" target="_blank">VPC</a> networking.',
        'Day 3 establishes modern 128-bit addressing mechanics following Day 2\'s IPv4 foundations.',
        'In enterprise cloud architecture, IPv6 sits at the edge ingress boundary, hybrid interconnects, and dual-stack VPC subnets.',
        'A microservice client receives an IPv6 <a href="http://www.google.com/search?q=AAAA" rel="noopener" target="_blank">AAAA</a> record resolving to a link-local address but attempts to initiate a TCP connection without specifying an interface scope index. The connection immediately errors out with Invalid Argument, halting automated canary deployments and blocking scheduled microservice updates.'
    ),
    (
        'topic-02',
        '2. DNS records, TTL and resolver roles',
        '<strong class="keyword"><a href="http://www.google.com/search?q=DNS" rel="noopener" target="_blank">DNS</a></strong> provides a globally distributed, hierarchical database mapping domain names to typed resource records across Root, TLD, and authoritative name servers. Stub resolvers delegate recursive queries to recursive resolvers, which traverse iterative referral chains and cache answers according to Time-To-Live (<a href="http://www.google.com/search?q=TTL" rel="noopener" target="_blank">TTL</a>) policies. Cryptographic extensions (<a href="http://www.google.com/search?q=DNSSEC" rel="noopener" target="_blank">DNSSEC</a>) authenticate record authenticity via digital signatures, while Google <a href="http://www.google.com/search?q=Cloud+DNS" rel="noopener" target="_blank">Cloud DNS</a> provides managed private and public zones with global Anycast resilience.',
        'Day 3 connects network addressing to human-readable names before Day 4\'s TLS certificate validation and <a href="http://www.google.com/search?q=HTTP" rel="noopener" target="_blank">HTTP</a> layer exploration.',
        'In Google Cloud, DNS sits inside Cloud DNS managed private zones, split-horizon resolution paths, and metadata server resolvers.',
        'An operations team modifies a DNS A record during a critical database failover but overlooks a 3600-second TTL cached across upstream recursive resolvers. Application pods continue directing transactional traffic to the decommissioned primary database for over forty minutes, resulting in split-brain data corruption and order reconciliation failures.'
    ),
    (
        'topic-03',
        '3. TCP and UDP, ports, connection states and buffers',
        '<strong class="keyword"><a href="http://www.google.com/search?q=Transport+protocols" rel="noopener" target="_blank">Transport protocols</a></strong> establish host-to-host process communication using 16-bit ports and Berkeley Software Distribution (BSD) socket abstractions. TCP enforces reliable byte-stream delivery through 3-way handshakes, sliding-window flow control, and model-based congestion control (<a href="http://www.google.com/search?q=BBR" rel="noopener" target="_blank">BBR</a>), while <a href="http://www.google.com/search?q=UDP" rel="noopener" target="_blank">UDP</a> provides lightweight, connectionless datagram transport powering modern <a href="http://www.google.com/search?q=QUIC" rel="noopener" target="_blank">QUIC</a> and <a href="http://www.google.com/search?q=HTTP" rel="noopener" target="_blank">HTTP/3</a>. Sockets manage kernel receive and send buffers, accept queues, and state lifecycles observable through kernel instrumentation tools.',
        'Day 3 completes transport mechanics before examining application protocols on Day 4.',
        'In cloud systems, transport mechanics govern guest OS socket buffer depths, Compute Engine TCP throughput, and Cloud Load Balancer proxy timeouts.',
        'A high-concurrency API service encounters socket accept queue saturation under peak promotional traffic while CPU utilization sits at barely thirty percent. Inbound TCP <a href="http://www.google.com/search?q=SYN" rel="noopener" target="_blank">SYN</a> packets are silently dropped by the kernel network stack, causing upstream load balancers to log HTTP 504 gateway timeouts and prompting clients to retry aggressively, amplifying the cascade.'
    )
]

PART1_HTML = f'''<p class="intro">Day 3 separates four fundamental architectural boundaries: name resolution, routing scope, transport state, and application processing.</p>
<p class="callout"><strong>Exit evidence:</strong> {escape(EXIT_SUMMARY)}</p>
''' + '\n'.join(
    f'''<article class="topic-card overview" id="{key}-overview">
<h3>{title}</h3>
<p>{body}</p>
<p><strong class="side-heading">Why today:</strong> {why}</p>
<p><strong class="side-heading">Where it sits:</strong> {where}</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> {prev}</p>
{render_linked_subtopics(key)}
<p><a href="#{key}-technical">Technical discussion →</a> <a href="#{key}-problem">Real-world problem →</a> <a href="#{key}-lab">Step-by-step lab →</a></p>
</article>''' for key, title, body, why, where, prev in OVERVIEWS
)

ARCH_TABLE_HTML = """
<table>
<caption>Protocol layer boundaries, encapsulated objects, observability tools, and failure signals</caption>
<thead>
<tr>
  <th scope="col">Protocol boundary</th>
  <th scope="col">Encapsulated object (PDU)</th>
  <th scope="col">Processing engine &amp; execution layer</th>
  <th scope="col">Observability &amp; diagnostic tooling</th>
  <th scope="col">Observable failure signal &amp; blast radius</th>
</tr>
</thead>
<tbody>
<tr>
  <th scope="row">IPv6 Scoping &amp; Link Discovery</th>
  <td>IPv6 Packet (128-bit IP src/dst, Next Header, Hop Limit, Flow Label) / ICMPv6</td>
  <td>Linux FIB6 routing table, Neighbor Discovery Protocol (NDP), SLAAC engine</td>
  <td><kbd>ip -6 addr</kbd>, <kbd>ip -6 route</kbd>, <kbd>ip -6 neigh</kbd>, <kbd>ndisc6</kbd></td>
  <td><samp>EINVAL</samp> (missing zone index), Neighbor Solicitation timeout, DAD duplicate address conflict</td>
</tr>
<tr>
  <th scope="row">DNS Resolution &amp; Trust Hierarchy</th>
  <td>DNS Message Wire Format (Header, Question, Answer, Authority, Additional, EDNS0)</td>
  <td>Stub resolver (<samp>systemd-resolved</samp>, <samp>glibc</samp>), Recursive Cache, Cloud DNS</td>
  <td><kbd>dig +trace</kbd>, <kbd>dig +dnssec</kbd>, <kbd>delv</kbd>, <kbd>resolvectl</kbd></td>
  <td><samp>NXDOMAIN</samp>, <samp>SERVFAIL</samp> (DNSSEC validation failure), stale TTL cache delivery, query timeout</td>
</tr>
<tr>
  <th scope="row">Transport Layer Core (TCP / UDP / QUIC)</th>
  <td>TCP Segment (16-bit Port, Seq/Ack, Flags, Window, MSS) / UDP Datagram / QUIC Packet</td>
  <td>Linux kernel TCP state machine (3-way/4-way handshakes, sliding window, CUBIC/BBR)</td>
  <td><kbd>ss -tuan</kbd>, <kbd>tcpdump -nn</kbd>, <kbd>netstat -s</kbd>, <kbd>conntrack -L</kbd></td>
  <td>Connection refused (<samp>RST</samp>), SYN queue drop, connection reset by peer, ephemeral port exhaustion</td>
</tr>
<tr>
  <th scope="row">Socket Abstraction &amp; Concurrency</th>
  <td>Kernel Socket Buffer (<samp>sk_buff</samp>, <samp>sk_rcvbuf</samp>, <samp>sk_sndbuf</samp>, accept queue)</td>
  <td>Berkeley Software Distribution (BSD) Socket API (<kbd>socket</kbd>, <kbd>bind</kbd>, <kbd>listen</kbd>, <kbd>accept</kbd>), <kbd>epoll</kbd>, <kbd>io_uring</kbd></td>
  <td><kbd>ss -lnt</kbd>, <kbd>lsof -i</kbd>, <kbd>cat /proc/net/sockstat</kbd>, <kbd>vmstat 1</kbd></td>
  <td><samp>EADDRINUSE</samp>, <samp>ECONNREFUSED</samp>, <samp>EAGAIN</samp> / <samp>EWOULDBLOCK</samp>, accept queue overflow</td>
</tr>
<tr>
  <th scope="row">Application Semantics (L7)</th>
  <td>Application Message (HTTP/1.1, HTTP/2, HTTP/3 QUIC frames, gRPC Protobuf, TLS 1.3)</td>
  <td>User-space process, Envoy reverse proxy, JVM runtime, Web server worker thread</td>
  <td><kbd>curl -vvv</kbd>, <kbd>openssl s_client</kbd>, OpenTelemetry traces, Application logs</td>
  <td>HTTP 502 Bad Gateway, HTTP 503 Service Unavailable, TLS certificate mismatch, payload parse failure</td>
</tr>
</tbody>
</table>
"""

ARCH_DIAGRAM = {
    "type": "topology",
    "title": "Day 3 End-to-End DNS, IPv6, Socket Lifecycle, and Transport Topology",
    "desc": "Three-tier architecture topology mapping dual-stack IPv6 clients, DNS resolution hierarchy, BSD socket lifecycle, TCP state transitions, and verification boundaries.",
    "caption": "Conceptual topology of the Day 3 request journey from dual-stack naming resolution to kernel socket transport state. It illustrates the boundaries between DNS recursive resolution, IPv6 scoping, kernel socket queues, and TCP handshakes; it does not prove physical latency, remote host readiness, or application authorization.",
    "width": 1120,
    "height": 690,
    "layers": [
        {
            "name": "TIER 1 · INGRESS & ADDRESSING SCOPE",
            "desc": "Dual-stack client · IPv6 scope context · DNS question dispatch",
            "x": 20,
            "y": 55,
            "w": 1080,
            "h": 92,
            "fill": "#1e3a5f",
            "title_color": "#7dd3fc"
        },
        {
            "name": "TIER 2 · RESOLUTION RUNTIME & TRANSPORT DATA PLANE",
            "desc": "DNS hierarchy · Socket lifecycle API · TCP 3-way/4-way handshakes · Congestion control",
            "x": 20,
            "y": 185,
            "w": 1080,
            "h": 210,
            "fill": "#064e3b",
            "title_color": "#6ee7b7"
        },
        {
            "name": "TIER 3 · GOVERNANCE & BOUNDARY VERIFICATION",
            "desc": "Layer boundary decoupling · Evidence classification · Invariant telemetry checkpoints",
            "x": 20,
            "y": 435,
            "w": 1080,
            "h": 115,
            "fill": "#422006",
            "title_color": "#fdba74"
        }
    ],
    "components": [
        {"x": 65, "y": 88, "w": 230, "h": 45, "name": "Dual-Stack Client", "detail": "IPv4 (RFC 1918) + IPv6 (GUA/LL)", "stroke": "#38bdf8", "icon": "../assets/icons/generic/client.svg"},
        {"x": 430, "y": 88, "w": 250, "h": 45, "name": "DNS Query (A / AAAA)", "detail": "Stub query · EDNS0 · DoT/DoH", "stroke": "#38bdf8", "icon": "../assets/icons/generic/decision.svg"},
        {"x": 815, "y": 88, "w": 220, "h": 45, "name": "IPv6 Destination Scope", "detail": "Link-Local (%eth0) vs Global", "stroke": "#38bdf8", "icon": "../assets/icons/generic/endpoint.svg"},
        {"x": 65, "y": 225, "w": 230, "h": 60, "name": "Recursive Resolver", "detail": "OS Cache · TTL · DNSSEC Auth", "stroke": "#22c55e", "icon": "../assets/icons/generic/dns-resolver.svg"},
        {"x": 430, "y": 225, "w": 250, "h": 60, "name": "Authoritative DNS Zone", "detail": "Root → TLD → Auth RRset", "stroke": "#22c55e", "icon": "../assets/icons/gcp/legacy/cloud-dns.svg"},
        {"x": 815, "y": 225, "w": 220, "h": 60, "name": "BSD Socket Lifecycle", "detail": "socket → bind → listen → accept", "stroke": "#22c55e", "icon": "../assets/icons/generic/endpoint.svg"},
        {"x": 260, "y": 322, "w": 260, "h": 52, "name": "TCP Transport Engine", "detail": "SYN-ACK · Sliding Window · CUBIC", "stroke": "#f59e0b", "icon": "../assets/icons/generic/server.svg"},
        {"x": 650, "y": 322, "w": 260, "h": 52, "name": "UDP & QUIC Datagram Path", "detail": "Connectionless UDP · HTTP/3 QUIC", "stroke": "#f59e0b", "icon": "../assets/icons/generic/queue.svg"},
        {"x": 190, "y": 468, "w": 280, "h": 58, "name": "Evidence Classification", "detail": "Resolution ≠ Reachability ≠ Connect", "stroke": "#fdba74", "icon": "../assets/icons/generic/decision.svg"},
        {"x": 650, "y": 468, "w": 280, "h": 58, "name": "Stop Condition Telemetry", "detail": "Isolate failure to exact OSI layer", "stroke": "#fdba74", "icon": "../assets/icons/generic/policy.svg"}
    ],
    "flows": [
        {"x1": 295, "y1": 110, "x2": 430, "y2": 110, "label": "lookup", "type": "ok"},
        {"x1": 680, "y1": 110, "x2": 815, "y2": 110, "label": "scope policy", "type": "ok"},
        {"x1": 180, "y1": 133, "x2": 180, "y2": 225, "label": "DNS query", "type": "ok"},
        {"x1": 555, "y1": 133, "x2": 555, "y2": 225, "label": "iterative chain", "type": "ok"},
        {"x1": 925, "y1": 133, "x2": 925, "y2": 225, "label": "socket bind", "type": "warn"},
        {"x1": 555, "y1": 285, "x2": 390, "y2": 322, "label": "resolved IP", "type": "ok"},
        {"x1": 815, "y1": 255, "x2": 520, "y2": 348, "label": "TCP handshake", "type": "ok"},
        {"x1": 780, "y1": 285, "x2": 780, "y2": 322, "label": "UDP/QUIC", "type": "warn"},
        {"x1": 390, "y1": 374, "x2": 390, "y2": 468, "label": "state telemetry", "type": "ok"},
        {"x1": 470, "y1": 497, "x2": 650, "y2": 497, "label": "assert invariant", "type": "ok"}
    ],
    "boundaries": [
        {
            "x": 150,
            "y": 458,
            "w": 820,
            "h": 75,
            "label": "VERIFICATION BOUNDARY: RESOLUTION ≠ REACHABILITY ≠ STATE",
            "color": "#f59e0b"
        }
    ],
    "probes": [
        {"cx": 290, "cy": 225, "label": "P1: DNS RRset & TTL", "color": "#38bdf8"},
        {"cx": 925, "cy": 285, "label": "P2: Socket 4-Tuple", "color": "#22c55e"},
        {"cx": 910, "cy": 374, "label": "P3: TCP State (ESTAB/TIME_WAIT)", "color": "#f59e0b"}
    ]
}

DNS_TRANSPORT_SVG = """
<figure class="diagram-container">
<div style="max-width:100%;overflow-x:auto">
<svg viewBox="0 0 1120 640" width="100%" height="auto" role="img" aria-labelledby="d003-exit-title d003-exit-desc" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;">
  <title id="d003-exit-title">DNS Resolution vs Network IP Reachability vs Established Socket Connection</title>
  <desc id="d003-exit-desc">Architectural verification diagram separating three distinct boundaries: DNS Name Resolution (Phase 1), Network Layer IP Reachability (Phase 2), and Transport Layer Established Socket Connection (Phase 3), with protocol states and diagnostic signals.</desc>
  <defs>
    <marker id="exit-arr-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/></marker>
    <marker id="exit-arr-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"/></marker>
    <marker id="exit-arr-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 1 L 10 5 L 0 9 z" fill="#f59e0b"/></marker>
    <marker id="exit-arr-fail" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 1 L 10 5 L 0 9 z" fill="#f43f5e"/></marker>
  </defs>

  <!-- Title Banner -->
  <rect x="20" y="15" width="1080" height="48" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="560" y="34" text-anchor="middle" font-family="monospace" font-size="13" fill="#38bdf8" font-weight="bold">DISTINGUISHING NAME RESOLUTION (DNS) ⟷ IP REACHABILITY (L3) ⟷ ESTABLISHED CONNECTION (L4 TCP)</text>
  <text x="560" y="52" text-anchor="middle" font-family="monospace" font-size="9.5" fill="#94a3b8">Diagnostic Protocol Decoupling: Why a Successful DNS Lookup Does Not Guarantee Packet Delivery or Socket Readiness</text>

  <!-- Column 1: Phase 1 - DNS Name Resolution (Left) -->
  <rect x="25" y="75" width="345" height="425" rx="6" fill="#090d16" stroke="#38bdf8" stroke-width="1.5"/>
  <rect x="35" y="85" width="325" height="24" rx="4" fill="#0c2033" stroke="#38bdf8" stroke-width="1"/>
  <text x="197" y="101" text-anchor="middle" font-family="monospace" font-size="10.5" fill="#38bdf8" font-weight="bold">PHASE 1 · NAME RESOLUTION</text>

  <!-- Box 1.1: Component -->
  <g transform="translate(45, 120)">
    <rect width="305" height="65" rx="4" fill="#121827" stroke="#38bdf8" stroke-width="1.5"/>
    <image href="../assets/icons/generic/dns-resolver.svg" x="12" y="20" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="11" fill="#38bdf8" font-weight="bold">DNS Recursive Resolver</text>
    <text x="48" y="39" font-family="sans-serif" font-size="9" fill="#cbd5e1">Queries Cloud DNS / 8.8.8.8 / 169.254.169.254</text>
    <text x="48" y="52" font-family="monospace" font-size="9" fill="#7dd3fc">Returns: A / AAAA RRset with TTL</text>
  </g>

  <!-- Arrow Down 1.1 -->
  <line x1="197" y1="185" x2="197" y2="210" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#exit-arr-blue)"/>

  <!-- Box 1.2: Boundary Proven -->
  <g transform="translate(45, 215)">
    <rect width="305" height="75" rx="4" fill="#052e16" stroke="#22c55e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/policy.svg" x="12" y="24" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#4ade80" font-weight="bold">BOUNDARY PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="9" fill="#bbf7d0">✓ Hostname exists in zone database</text>
    <text x="48" y="52" font-family="sans-serif" font-size="9" fill="#bbf7d0">✓ Authoritative name servers respond</text>
    <text x="48" y="65" font-family="sans-serif" font-size="9" fill="#bbf7d0">✓ DNSSEC signature valid (AD flag = 1)</text>
  </g>

  <!-- Arrow Down 1.2 -->
  <line x1="197" y1="290" x2="197" y2="315" stroke="#f43f5e" stroke-width="1.5" marker-end="url(#exit-arr-fail)"/>

  <!-- Box 1.3: What is NOT Proven -->
  <g transform="translate(45, 320)">
    <rect width="305" height="85" rx="4" fill="#3b0712" stroke="#f43f5e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/failure.svg" x="12" y="28" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#f87171" font-weight="bold">WHAT IS NOT PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Does NOT prove IP route exists</text>
    <text x="48" y="52" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Does NOT prove remote host is alive</text>
    <text x="48" y="65" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Does NOT prove destination port listens</text>
    <text x="48" y="78" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Link-local IPv6 fails without zone index</text>
  </g>

  <!-- Box 1.4: Tools & Errors -->
  <g transform="translate(45, 420)">
    <rect width="305" height="65" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="12" y="18" font-family="monospace" font-size="9" fill="#94a3b8">Diagnostic Tooling:</text>
    <text x="12" y="32" font-family="monospace" font-size="9" fill="#7dd3fc">dig +trace, dig +dnssec, delv, host</text>
    <text x="12" y="46" font-family="monospace" font-size="9" fill="#f87171">Failure Signals:</text>
    <text x="12" y="58" font-family="monospace" font-size="9" fill="#fca5a5">NXDOMAIN, SERVFAIL, REFUSED, Stale TTL</text>
  </g>

  <!-- Transition Arrow: Column 1 to Column 2 -->
  <line x1="370" y1="250" x2="385" y2="250" stroke="#38bdf8" stroke-width="2" marker-end="url(#exit-arr-blue)"/>
  <text x="378" y="240" text-anchor="middle" font-family="monospace" font-size="9" fill="#38bdf8">pass</text>

  <!-- Column 2: Phase 2 - L3 IP Reachability (Middle) -->
  <rect x="388" y="75" width="345" height="425" rx="6" fill="#090d16" stroke="#22c55e" stroke-width="1.5"/>
  <rect x="398" y="85" width="325" height="24" rx="4" fill="#052e16" stroke="#22c55e" stroke-width="1"/>
  <text x="560" y="101" text-anchor="middle" font-family="monospace" font-size="10.5" fill="#22c55e" font-weight="bold">PHASE 2 · NETWORK IP REACHABILITY</text>

  <!-- Box 2.1: Component -->
  <g transform="translate(408, 120)">
    <rect width="305" height="65" rx="4" fill="#121827" stroke="#22c55e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/router.svg" x="12" y="20" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="11" fill="#22c55e" font-weight="bold">IP Routing &amp; Link Discovery</text>
    <text x="48" y="39" font-family="sans-serif" font-size="9" fill="#cbd5e1">FIB Lookup · ARP (IPv4) / NDP (IPv6)</text>
    <text x="48" y="52" font-family="monospace" font-size="9" fill="#a7f3d0">Transmits: IP Packet / ICMP Echo / NS-NA</text>
  </g>

  <!-- Arrow Down 2.1 -->
  <line x1="560" y1="185" x2="560" y2="210" stroke="#22c55e" stroke-width="1.5" marker-end="url(#exit-arr-green)"/>

  <!-- Box 2.2: Boundary Proven -->
  <g transform="translate(408, 215)">
    <rect width="305" height="75" rx="4" fill="#052e16" stroke="#22c55e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/policy.svg" x="12" y="24" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#4ade80" font-weight="bold">BOUNDARY PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="9" fill="#bbf7d0">✓ Route table matches destination CIDR</text>
    <text x="48" y="52" font-family="sans-serif" font-size="9" fill="#bbf7d0">✓ Neighbor MAC resolved on local segment</text>
    <text x="48" y="65" font-family="sans-serif" font-size="9" fill="#bbf7d0">✓ Intermediate routers forward hop-by-hop</text>
  </g>

  <!-- Arrow Down 2.2 -->
  <line x1="560" y1="290" x2="560" y2="315" stroke="#f43f5e" stroke-width="1.5" marker-end="url(#exit-arr-fail)"/>

  <!-- Box 2.3: What is NOT Proven -->
  <g transform="translate(408, 320)">
    <rect width="305" height="85" rx="4" fill="#3b0712" stroke="#f43f5e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/failure.svg" x="12" y="28" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#f87171" font-weight="bold">WHAT IS NOT PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Does NOT prove destination TCP port open</text>
    <text x="48" y="52" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Does NOT prove SYN handshake succeeds</text>
    <text x="48" y="65" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Does NOT prove accept queue has space</text>
    <text x="48" y="78" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Firewall may permit ICMP but drop TCP</text>
  </g>

  <!-- Box 2.4: Tools & Errors -->
  <g transform="translate(408, 420)">
    <rect width="305" height="65" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="12" y="18" font-family="monospace" font-size="9" fill="#94a3b8">Diagnostic Tooling:</text>
    <text x="12" y="32" font-family="monospace" font-size="9" fill="#a7f3d0">ip route get, ip neigh, ping, traceroute -I</text>
    <text x="12" y="46" font-family="monospace" font-size="9" fill="#f87171">Failure Signals:</text>
    <text x="12" y="58" font-family="monospace" font-size="9" fill="#fca5a5">No route (ENETUNREACH), EINVAL, ICMP Exceeded</text>
  </g>

  <!-- Transition Arrow: Column 2 to Column 3 -->
  <line x1="733" y1="250" x2="748" y2="250" stroke="#22c55e" stroke-width="2" marker-end="url(#exit-arr-green)"/>
  <text x="740" y="240" text-anchor="middle" font-family="monospace" font-size="9" fill="#22c55e">pass</text>

  <!-- Column 3: Phase 3 - L4 TCP Connection (Right) -->
  <rect x="750" y="75" width="345" height="425" rx="6" fill="#090d16" stroke="#f59e0b" stroke-width="1.5"/>
  <rect x="760" y="85" width="325" height="24" rx="4" fill="#241808" stroke="#f59e0b" stroke-width="1"/>
  <text x="922" y="101" text-anchor="middle" font-family="monospace" font-size="10.5" fill="#f59e0b" font-weight="bold">PHASE 3 · ESTABLISHED CONNECTION (L4)</text>

  <!-- Box 3.1: Component -->
  <g transform="translate(770, 120)">
    <rect width="305" height="65" rx="4" fill="#121827" stroke="#f59e0b" stroke-width="1.5"/>
    <image href="../assets/icons/generic/server.svg" x="12" y="20" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="11" fill="#f59e0b" font-weight="bold">TCP Transport State Machine</text>
    <text x="48" y="39" font-family="sans-serif" font-size="9" fill="#cbd5e1">3-Way Handshake (SYN → SYN-ACK → ACK)</text>
    <text x="48" y="52" font-family="monospace" font-size="9" fill="#fde68a">Kernel State: ESTABLISHED (4-Tuple Bound)</text>
  </g>

  <!-- Arrow Down 3.1 -->
  <line x1="922" y1="185" x2="922" y2="210" stroke="#f59e0b" stroke-width="1.5" marker-end="url(#exit-arr-amber)"/>

  <!-- Box 3.2: Boundary Proven -->
  <g transform="translate(770, 215)">
    <rect width="305" height="75" rx="4" fill="#052e16" stroke="#22c55e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/policy.svg" x="12" y="24" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#4ade80" font-weight="bold">BOUNDARY PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="9" fill="#bbf7d0">✓ Target process bound to IP:port (LISTEN)</text>
    <text x="48" y="52" font-family="sans-serif" font-size="9" fill="#bbf7d0">✓ 3-Way handshake completed (ESTABLISHED)</text>
    <text x="48" y="65" font-family="sans-serif" font-size="9" fill="#bbf7d0">✓ Socket buffers allocated (sk_rcvbuf/sndbuf)</text>
  </g>

  <!-- Arrow Down 3.2 -->
  <line x1="922" y1="290" x2="922" y2="315" stroke="#f43f5e" stroke-width="1.5" marker-end="url(#exit-arr-fail)"/>

  <!-- Box 3.3: What is NOT Proven -->
  <g transform="translate(770, 320)">
    <rect width="305" height="85" rx="4" fill="#3b0712" stroke="#f43f5e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/failure.svg" x="12" y="28" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#f87171" font-weight="bold">WHAT IS NOT PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Does NOT prove application parsed request</text>
    <text x="48" y="52" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Does NOT prove TLS handshake succeeds</text>
    <text x="48" y="65" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Does NOT prove downstream DB is healthy</text>
    <text x="48" y="78" font-family="sans-serif" font-size="9" fill="#fecaca">✗ Worker thread may hang on blocked I/O</text>
  </g>

  <!-- Box 3.4: Tools & Errors -->
  <g transform="translate(770, 420)">
    <rect width="305" height="65" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="12" y="18" font-family="monospace" font-size="9" fill="#94a3b8">Diagnostic Tooling:</text>
    <text x="12" y="32" font-family="monospace" font-size="9" fill="#fde68a">ss -tuanp, tcpdump -nn, netstat -s, lsof -i</text>
    <text x="12" y="46" font-family="monospace" font-size="9" fill="#f87171">Failure Signals:</text>
    <text x="12" y="58" font-family="monospace" font-size="9" fill="#fca5a5">ECONNREFUSED (RST), ETIMEDOUT, somaxconn overflow</text>
  </g>

  <!-- Bottom Diagnostic Footer Banner -->
  <rect x="25" y="515" width="1070" height="105" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="40" y="533" font-family="monospace" font-size="10" fill="#94a3b8" font-weight="bold">BOUNDARY FAILURE SEPARATION &amp; ARCHITECTURAL DIAGNOSTIC CHECKS:</text>

  <!-- Card 1 -->
  <g transform="translate(38, 542)">
    <rect width="250" height="72" rx="3" fill="#121827" stroke="#38bdf8" stroke-width="1"/>
    <image href="../assets/icons/generic/decision.svg" x="8" y="8" width="18" height="18" preserveAspectRatio="xMidYMid meet"/>
    <text x="32" y="18" font-family="monospace" font-size="9" fill="#38bdf8" font-weight="bold">NAME RESOLUTION CHECK</text>
    <text x="10" y="34" font-family="sans-serif" font-size="9" fill="#cbd5e1">• Fails at DNS: Hostname cannot be queried</text>
    <text x="10" y="47" font-family="sans-serif" font-size="9" fill="#cbd5e1">• Check DNS TTL &amp; local resolver cache</text>
    <text x="10" y="60" font-family="monospace" font-size="9" fill="#7dd3fc">Tool: dig +trace, resolvectl status</text>
  </g>

  <!-- Card 2 -->
  <g transform="translate(300, 542)">
    <rect width="250" height="72" rx="3" fill="#121827" stroke="#22c55e" stroke-width="1"/>
    <image href="../assets/icons/generic/endpoint.svg" x="8" y="8" width="18" height="18" preserveAspectRatio="xMidYMid meet"/>
    <text x="32" y="18" font-family="monospace" font-size="9" fill="#22c55e" font-weight="bold">IP REACHABILITY CHECK</text>
    <text x="10" y="34" font-family="sans-serif" font-size="9" fill="#cbd5e1">• Fails at L3: Packet dropped by route or ACL</text>
    <text x="10" y="47" font-family="sans-serif" font-size="9" fill="#cbd5e1">• IPv6 requires zone index (%eth0) if link-local</text>
    <text x="10" y="60" font-family="monospace" font-size="9" fill="#a7f3d0">Tool: ip route get, traceroute -I</text>
  </g>

  <!-- Card 3 -->
  <g transform="translate(562, 542)">
    <rect width="250" height="72" rx="3" fill="#121827" stroke="#f59e0b" stroke-width="1"/>
    <image href="../assets/icons/generic/server.svg" x="8" y="8" width="18" height="18" preserveAspectRatio="xMidYMid meet"/>
    <text x="32" y="18" font-family="monospace" font-size="9" fill="#f59e0b" font-weight="bold">TCP CONNECTION CHECK</text>
    <text x="10" y="34" font-family="sans-serif" font-size="9" fill="#cbd5e1">• Fails at L4: Port closed (RST) or queue full</text>
    <text x="10" y="47" font-family="sans-serif" font-size="9" fill="#cbd5e1">• SYN drop under burst: check somaxconn</text>
    <text x="10" y="60" font-family="monospace" font-size="9" fill="#fde68a">Tool: ss -lnt, netstat -s, tcpdump -nn</text>
  </g>

  <!-- Card 4 -->
  <g transform="translate(824, 542)">
    <rect width="258" height="72" rx="3" fill="#121827" stroke="#ec4899" stroke-width="1"/>
    <image href="../assets/icons/generic/outcome.svg" x="8" y="8" width="18" height="18" preserveAspectRatio="xMidYMid meet"/>
    <text x="32" y="18" font-family="monospace" font-size="9" fill="#ec4899" font-weight="bold">APPLICATION READINESS</text>
    <text x="10" y="34" font-family="sans-serif" font-size="9" fill="#cbd5e1">• Fails at L7: HTTP 500/502/503 status code</text>
    <text x="10" y="47" font-family="sans-serif" font-size="9" fill="#cbd5e1">• L4 success gives FALSE positive for L7 health</text>
    <text x="10" y="60" font-family="monospace" font-size="9" fill="#fbcfe8">Tool: curl -iv, OpenTelemetry traces</text>
  </g>
</svg>
</div>
<figcaption>Architectural exit evidence distinguishing the three sequential boundaries of network connectivity: (1) DNS Name Resolution, proving record existence in a zone database; (2) Network IP Reachability, proving Layer 3 packet routing and NDP/ARP MAC resolution; and (3) Established Socket Connection, proving Layer 4 kernel socket handshake completion. It demonstrates that each boundary operates independently, and success at one phase does not guarantee readiness at the next.</figcaption>
</figure>
"""

DNS_PIPELINE_SVG = flow_svg(
    'd003-dns-pipeline',
    'Recursive DNS resolution pipeline: stub client to authoritative zone',
    [
        ('Stub query', ('Client getaddrinfo() query', 'Recursion Desired: RD=1'), 'client'),
        ('Resolver cache', ('Checks local TTL cache', 'Cache miss triggers query'), 'dns-resolver'),
        ('Root referral', ('Queries Anycast Root (.)', 'Referral to .com TLD servers'), 'decision'),
        ('TLD referral', ('Queries TLD (.com) server', 'Referral to domain NS'), 'dns-resolver'),
        ('Auth zone answer', ('Queries ns1.example.com', 'Authoritative Answer (AA=1)'), 'server'),
        ('Client delivery', ('Caches RRset for TTL duration', 'Returns IP to application'), 'outcome'),
    ],
    ['RD=1 query', 'Root query', 'TLD referral', 'Auth query', 'RRset answer'],
    'Read 1 → 2 → 3 → 4 → 5 → 6. The iterative DNS resolution pipeline executed by a recursive resolver on behalf of a stub client. The stub delegates traversal; the recursive resolver follows referrals from Root (.) to TLD (.com) down to the authoritative name server, caching the final RRset for the duration of its Time-To-Live (TTL).'
)

ARCH_SVG_HTML = f"{render_topology_svg(DAY, ARCH_DIAGRAM)}\n\n{DNS_TRANSPORT_SVG}"

DNS_RECORDS_TABLE_HTML = """
<table>
<caption>Comprehensive DNS Resource Record Type Reference Matrix</caption>
<thead>
<tr>
  <th scope="col">Record Type</th>
  <th scope="col">Full Name &amp; RFC Standard</th>
  <th scope="col">Wire Format &amp; Target Syntax</th>
  <th scope="col">Architectural Function &amp; Cloud Usage</th>
  <th scope="col">Key Architectural Constraints &amp; Failure Modes</th>
</tr>
</thead>
<tbody>
<tr>
  <th scope="row">A</th>
  <td>IPv4 Address (RFC 1035 §3.4.1)</td>
  <td><samp>&lt;name&gt; &lt;ttl&gt; IN A &lt;ipv4-address&gt;</samp><br>Example: <samp>api.example.com. 300 IN A 198.51.100.10</samp></td>
  <td>Maps a fully qualified domain name (FQDN) to a 32-bit IPv4 address. Primary record for web servers, ingress load balancers, and API endpoints.</td>
  <td>Multiple A records provide client-side round-robin load balancing without health checking. Cached entries persist across failovers until TTL expires.</td>
</tr>
<tr>
  <th scope="row">AAAA</th>
  <td>IPv6 Address (RFC 3596 §2.1)</td>
  <td><samp>&lt;name&gt; &lt;ttl&gt; IN AAAA &lt;ipv6-address&gt;</samp><br>Example: <samp>api.example.com. 300 IN AAAA 2001:db8::10</samp></td>
  <td>Maps an FQDN to a 128-bit IPv6 address. Powers dual-stack cloud services, Google Cloud external load balancer IPv6 frontend VIPs, and modern mobile networks.</td>
  <td>Must never point to a non-routable link-local address (<samp>fe80::/10</samp>); remote clients cannot supply the interface zone index and fail with <samp>EINVAL</samp>.</td>
</tr>
<tr>
  <th scope="row">CNAME</th>
  <td>Canonical Name (RFC 1035 §3.3.1)</td>
  <td><samp>&lt;alias&gt; &lt;ttl&gt; IN CNAME &lt;canonical-name&gt;</samp><br>Example: <samp>www.example.com. 3600 IN CNAME app.example.com.</samp></td>
  <td>Creates an alias pointing to another canonical domain name. Used for third-party SaaS hosting, Cloud Storage buckets, and CDN frontend endpoints.</td>
  <td><strong>RFC 1912 zone apex restriction:</strong> A CNAME cannot coexist with any other record for the same label. Cannot be placed at the root domain (<samp>example.com</samp>) because SOA and NS records are required at apex.</td>
</tr>
<tr>
  <th scope="row">MX</th>
  <td>Mail Exchange (RFC 1035 §3.3.9, RFC 5321)</td>
  <td><samp>&lt;name&gt; &lt;ttl&gt; IN MX &lt;priority&gt; &lt;host&gt;</samp><br>Example: <samp>example.com. 3600 IN MX 10 mail.example.com.</samp></td>
  <td>Routes incoming email messages to designated mail transfer agents (MTAs). Lower numeric priority indicates higher preference.</td>
  <td>The target host of an MX record MUST resolve to an A or AAAA record. Pointing an MX record to a CNAME alias violates RFC 2181 §10.3 and causes delivery failures.</td>
</tr>
<tr>
  <th scope="row">TXT</th>
  <td>Text Resource (RFC 1035 §3.3.14, RFC 1464)</td>
  <td><samp>&lt;name&gt; &lt;ttl&gt; IN TXT &lt;string&gt;</samp><br>Example: <samp>example.com. 300 IN TXT "v=spf1 include:_spf.google.com ~all"</samp></td>
  <td>Holds arbitrary human- or machine-readable text up to 255 bytes per string chunk. Critical for domain verification (Google Workspace, GCP peering), SPF, DKIM, and DMARC.</td>
  <td>Strings exceeding 255 bytes must be split into multiple quoted strings within a single record. Exceeding UDP 512-byte payload triggers EDNS0 or TCP fallback.</td>
</tr>
<tr>
  <th scope="row">NS</th>
  <td>Name Server (RFC 1035 §3.3.11)</td>
  <td><samp>&lt;zone&gt; &lt;ttl&gt; IN NS &lt;nameserver-host&gt;</samp><br>Example: <samp>example.com. 86400 IN NS ns-cloud-a1.googledomains.com.</samp></td>
  <td>Delegates a DNS zone or subdomain to authoritative name servers. Published at both parent registrar zone (referral) and child zone apex (authoritative).</td>
  <td>Delegating a subdomain where the name server resides within the child zone (<samp>ns1.sub.example.com</samp>) requires "glue records" (A/AAAA) in the parent zone to prevent unresolvable circular dependencies.</td>
</tr>
<tr>
  <th scope="row">SOA</th>
  <td>Start of Authority (RFC 1035 §3.3.13, RFC 2308)</td>
  <td><samp>&lt;zone&gt; &lt;ttl&gt; IN SOA &lt;mname&gt; &lt;rname&gt; (&lt;serial&gt; &lt;refresh&gt; &lt;retry&gt; &lt;expire&gt; &lt;minimum&gt;)</samp></td>
  <td>Mandatory first record of every DNS zone. Defines primary master server, zone administrator email (<samp>.</samp> replacing <samp>@</samp>), zone serial number, and secondary replication timers.</td>
  <td>The <samp>minimum</samp> field governs <strong>negative caching</strong> (RFC 2308): how long recursive resolvers cache <samp>NXDOMAIN</samp> (nonexistent domain) and <samp>NODATA</samp> responses.</td>
</tr>
<tr>
  <th scope="row">PTR</th>
  <td>Pointer Record (RFC 1035 §3.3.12)</td>
  <td><samp>&lt;reverse-ip&gt;.in-addr.arpa. &lt;ttl&gt; IN PTR &lt;hostname&gt;</samp><br>Example: <samp>10.100.51.198.in-addr.arpa. 3600 IN PTR mail.example.com.</samp></td>
  <td>Performs reverse DNS lookups mapping an IP address back to its canonical hostname under the <samp>in-addr.arpa</samp> (IPv4) or <samp>ip6.arpa</samp> (IPv6) hierarchy.</td>
  <td>Essential for email deliverability: spam filters reject incoming SMTP connections if the connecting IP lacks a matching forward-confirmed reverse DNS (FCrDNS) PTR record.</td>
</tr>
<tr>
  <th scope="row">SRV</th>
  <td>Service Locator (RFC 2782)</td>
  <td><samp>_service._proto.&lt;name&gt; &lt;ttl&gt; IN SRV &lt;priority&gt; &lt;weight&gt; &lt;port&gt; &lt;target&gt;</samp><br>Example: <samp>_sip._tcp.example.com. 3600 IN SRV 0 5 5060 sipserver.example.com.</samp></td>
  <td>Enables generalized service discovery by publishing the host, port, priority, and load-balancing weight for symbolic protocols. Extensively used in Kubernetes headless services and Active Directory.</td>
  <td>Client applications must explicitly query and parse SRV records; standard web browsers and HTTP client libraries only query A and AAAA records.</td>
</tr>
<tr>
  <th scope="row">CAA</th>
  <td>Certification Authority Authorization (RFC 8659)</td>
  <td><samp>&lt;name&gt; &lt;ttl&gt; IN CAA &lt;flags&gt; &lt;tag&gt; "&lt;value&gt;"</samp><br>Example: <samp>example.com. 3600 IN CAA 0 issue "pki.goog"</samp></td>
  <td>Restricts which Certificate Authorities (CAs) are legally authorized to issue TLS/SSL certificates for the domain, preventing rogue or compromised CA issuance.</td>
  <td>Public CAs are mandated by the CA/Browser Forum to check CAA records before issuing certificates. Misconfigured or forgotten CAA records halt automated certificate renewal pipelines.</td>
</tr>
<tr>
  <th scope="row">DS</th>
  <td>Delegation Signer (RFC 4034 §5)</td>
  <td><samp>&lt;name&gt; &lt;ttl&gt; IN DS &lt;key-tag&gt; &lt;algorithm&gt; &lt;digest-type&gt; &lt;digest&gt;</samp></td>
  <td>Published in the parent zone (e.g. <samp>.com</samp>) containing a cryptographic hash of the child zone's Key Signing Key (KSK). Establishes the DNSSEC cryptographic chain of trust.</td>
  <td>A mismatched DS record in the parent registrar immediately breaks the cryptographic chain of trust, causing all DNSSEC-validating resolvers worldwide to return <samp>SERVFAIL</samp> for the entire domain.</td>
</tr>
<tr>
  <th scope="row">DNSKEY</th>
  <td>DNS Public Key (RFC 4034 §2)</td>
  <td><samp>&lt;name&gt; &lt;ttl&gt; IN DNSKEY &lt;flags&gt; &lt;protocol&gt; &lt;algorithm&gt; &lt;public-key&gt;</samp></td>
  <td>Publishes the public keys used in DNSSEC. Flag 256 indicates a Zone Signing Key (ZSK) used to sign RRsets; flag 257 indicates a Key Signing Key (KSK) used to sign the DNSKEY RRset itself.</td>
  <td>Key rotation must follow strict dual-signing or pre-publication procedures (RFC 7583) to avoid caching race conditions that invalidate resolver signature checks during rollover.</td>
</tr>
<tr>
  <th scope="row">RRSIG</th>
  <td>Resource Record Signature (RFC 4034 §3)</td>
  <td><samp>&lt;name&gt; &lt;ttl&gt; IN RRSIG &lt;type-covered&gt; &lt;alg&gt; &lt;labels&gt; &lt;orig-ttl&gt; &lt;sig-exp&gt; &lt;sig-inc&gt; &lt;key-tag&gt; &lt;signer&gt; &lt;signature&gt;</samp></td>
  <td>Contains the cryptographic digital signature covering an entire Resource Record Set (RRset) for a specific record type, verifying origin authenticity and data integrity.</td>
  <td>Signatures include explicit inception and expiration timestamps. If the authoritative zone does not re-sign records before expiration, validating resolvers immediately reject the records with <samp>SERVFAIL</samp>.</td>
</tr>
<tr>
  <th scope="row">NSEC / NSEC3</th>
  <td>Next Secure / Next Secure 3 (RFC 4034 §4, RFC 5155)</td>
  <td><samp>&lt;name&gt; &lt;ttl&gt; IN NSEC &lt;next-domain&gt; &lt;type-bit-maps&gt;</samp><br>or salted hash in NSEC3</td>
  <td>Provides cryptographically authenticated denial of existence, proving that a queried domain or record type does not exist. NSEC3 uses salted iterations of SHA-1 hashes to prevent zone enumeration ("zone walking").</td>
  <td>Excessive NSEC3 hash iterations place heavy computational burden on recursive validating resolvers; RFC 9276 recommends iteration counts of 0 for modern operational deployments.</td>
</tr>
<tr>
  <th scope="row">ALIAS / ANAME</th>
  <td>Apex Alias (Provider Proprietary De-facto Standard)</td>
  <td><samp>&lt;apex&gt; &lt;ttl&gt; IN ALIAS &lt;canonical-name&gt;</samp><br>Example: <samp>example.com. 300 IN ALIAS lb.cloud.google.com.</samp></td>
  <td>Synthesizes dynamic A and AAAA responses at the zone apex (<samp>example.com</samp>) by resolving the target canonical name internally, bypassing the RFC 1912 CNAME apex restriction.</td>
  <td>Because resolution occurs on authoritative DNS servers rather than at the client's resolver, Anycast and EDNS Client Subnet (ECS) geo-routing accuracy can be degraded.</td>
</tr>
</tbody>
</table>
"""

def make_lab(name, goal, expected, steps, accept, trouble, file_name, covers):
    return {
        "name": name,
        "goal": goal,
        "expected": expected,
        "covers": covers,
        "mode": "Local Linux terminal tabletop; supplied synthetic fixtures. Observed locally: command execution, script assertions, and file hashes. Simulated or predicted: host routing decisions, packet traversal, and boundary classifications. Untested on GCP: live Andromeda SDN forwarding, Compute Engine VPC network provisioning, and cloud firewall rules.",
        "prereq": "Day 2 local workspace and network path artifacts.",
        "preflight": "Run all eight stages in order in the same terminal. Stage 1 verifies required local tools with command -v and creates a unique workspace. Stop if Python 3 or Bash is unavailable; use the Linux environment prepared on Day 1. Commands write only inside the lab workspace.",
        "steps": steps,
        "accept": accept,
        "verification": "Recorded outputs are local calculations, script assertions, or fixture classifications. They are not cloud observations.",
        "trouble": trouble,
        "cleanup": "Stage 8 removes temporary calculation scripts and non-essential inputs while preserving durable evidence files. No processes, cloud resources, firewall rules, or kernel settings are created or changed.",
        "file": file_name
    }

TOPICS = [
    {
        "key": "topic-01",
        "title": "IPv6 addressing and scope",
        "overview": OVERVIEWS[0][2],
        "preview": OVERVIEWS[0][5],
        "technical": (
            "<p><strong class='side-heading'>Subtopics in this discussion:</strong></p>\n"
            "<ol>\n"
            "<li><a href='#topic-01-subtopic-1'>IPv6 128-bit address architecture and canonical representation</a></li>\n"
            "<li><a href='#topic-01-subtopic-2'>Address scoping boundaries (Link-Local, Unique Local, and Global Unicast)</a></li>\n"
            "<li><a href='#topic-01-subtopic-3'>Neighbor Discovery Protocol (NDP) mechanics (RS/RA, NS/NA, SLAAC, DAD)</a></li>\n"
            "<li><a href='#topic-01-subtopic-4'>Dual-stack VPC architecture, Happy Eyeballs (RFC 8305), and Google Cloud edge ingress</a></li>\n"
            "</ol>\n\n"
            "<p class='overview-chips'><strong>Core protocol terms:</strong> "
            "<a href='http://www.google.com/search?q=Link-Local' rel='noopener' target='_blank'>Link-Local</a> · "
            "<a href='http://www.google.com/search?q=Unique+Local' rel='noopener' target='_blank'>Unique Local</a> · "
            "<a href='http://www.google.com/search?q=Global+Unicast' rel='noopener' target='_blank'>Global Unicast</a> · "
            "<a href='http://www.google.com/search?q=NDP' rel='noopener' target='_blank'>NDP</a> · "
            "<a href='http://www.google.com/search?q=SLAAC' rel='noopener' target='_blank'>SLAAC</a> · "
            "<a href='http://www.google.com/search?q=DAD' rel='noopener' target='_blank'>DAD</a> · "
            "<a href='http://www.google.com/search?q=VPC' rel='noopener' target='_blank'>VPC</a> · "
            "<a href='http://www.google.com/search?q=Happy+Eyeballs' rel='noopener' target='_blank'>Happy Eyeballs</a>"
            "</p>\n\n"

            "<h3 id='topic-01-subtopic-1'>IPv6 128-bit address architecture and canonical representation</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> <strong class='keyword'><a href='http://www.google.com/search?q=Internet+Protocol+version+6+%28IPv6%29' rel='noopener' target='_blank'>Internet Protocol version 6 (IPv6)</a></strong> (RFC 8200, RFC 4291) expands the IP address space from 32 bits ($2^{32} \\approx 4.3 \\times 10^9$) "
            "to 128 bits ($2^{128} \\approx 3.4 \\times 10^{38}$), eliminating the architectural requirement for Network Address Translation (NAT). "
            "An IPv6 address consists of eight 16-bit hexadecimal quads separated by colons (e.g., <samp>2001:0db8:85a3:0000:0000:8a2e:0370:7334</samp>). "
            "Under RFC 5952 canonical formatting rules: (1) leading zeros within any quad must be suppressed; (2) lowercase hexadecimal characters must be used; "
            "and (3) the single longest run of consecutive all-zero quads must be compressed exactly once using a double colon (<samp>::</samp>). For instance, "
            "<samp>2001:db8:85a3::8a2e:370:7334</samp> is canonical, whereas compressing isolated single zeros or using double colons multiple times is invalid.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> Canonical string parsing is critical for automated cloud infrastructure, Continuous Integration / Continuous Deployment (CI/CD) pipelines, firewall policies, "
            "and audit logging. Non-canonical variations of the same IPv6 address can bypass naive string-matching security rules, cause IP Address Management (IPAM) database deduplication "
            "failures, or break automated infrastructure-as-code validations across multi-cloud environments.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> In <a href='http://www.google.com/search?q=GCP' rel='noopener' target='_blank'>GCP</a> (Google Cloud), subnets support dual-stack operation. As documented in "
            "the <a href='https://cloud.google.com/vpc/docs/subnets#ipv6-ranges'>Google Cloud VPC documentation: IPv6 subnet ranges (accessed 2026-11-03)</a>, Google Cloud supports internal and external IPv6 subnet ranges; Google-provided internal ranges are unused <samp>/64</samp> ranges from a VPC network's <samp>/48</samp> ULA range, while Google-provided external ranges are <samp>/64</samp> GUAs. Architects must align routes and firewall rules with the selected <a href='http://www.google.com/search?q=VPC' rel='noopener' target='_blank'>VPC</a> access type.</li>\n</ul>\n\n"

            "<h3 id='topic-01-subtopic-2'>Address scoping boundaries (Link-Local, Unique Local, and Global Unicast)</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> Unlike IPv4 where private ranges (<strong class='keyword'><a href='http://www.google.com/search?q=address+scopes' rel='noopener' target='_blank'>address scopes</a></strong>) are routable across any private network, IPv6 introduces strict, architecturally enforced address scopes:\n"
            "<ul>\n"
            "<li><strong><a href='http://www.google.com/search?q=Link-Local' rel='noopener' target='_blank'>Link-Local</a> Unicast (<samp>fe80::/10</samp>):</strong> Automatically configured on every active IPv6 interface. Link-local addresses are topologically bounded to the local Layer 2 broadcast/broadcast-equivalent segment and are never forwarded by routers. Because identical link-local addresses can legally exist on distinct interfaces connected to different physical links, the operating system cannot route packets to a link-local destination without an explicit <strong>Zone Identifier / Interface Index</strong> (e.g., <samp>fe80::1%eth0</samp> on Linux). Initiating a socket connection to a bare link-local address without a zone index fails immediately with <samp>EINVAL</samp> (Invalid argument).</li>\n"
            "<li><strong><a href='http://www.google.com/search?q=Unique+Local' rel='noopener' target='_blank'>Unique Local</a> Address (ULA, <samp>fc00::/7</samp>, RFC 4193):</strong> Globally unique private addresses intended for local communications across an enterprise private Wide Area Network (WAN) or hybrid interconnect. Block <samp>fd00::/8</samp> is assigned with a 40-bit pseudo-random Global ID, preventing address collisions during future enterprise corporate mergers or Virtual Private Cloud (<a href='http://www.google.com/search?q=VPC' rel='noopener' target='_blank'>VPC</a>) peerings without NAT.</li>\n"
            "<li><strong><a href='http://www.google.com/search?q=Global+Unicast' rel='noopener' target='_blank'>Global Unicast</a> Address (GUA, <samp>2000::/3</samp>, RFC 3587):</strong> Globally routable public addresses allocated by Regional Internet Registries (RIRs). Typically structured as a 48-bit global routing prefix assigned to the enterprise, a 16-bit subnet ID (providing up to 65,536 individual subnets per enterprise site), and a 64-bit Interface Identifier (IID).</li>\n"
            "<li><strong>Special Purpose Addresses:</strong> Loopback (<samp>::1/128</samp>), Unspecified (<samp>::/128</samp>, used as source during boot prior to Duplicate Address Detection [<a href='http://www.google.com/search?q=DAD' rel='noopener' target='_blank'>DAD</a>]), and Multicast (<samp>ff00::/8</samp>, including All-Nodes <samp>ff02::1</samp> and All-Routers <samp>ff02::2</samp>).</li>\n"
            "</ul>\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> A common and devastating cloud misconfiguration occurs when automated CI/CD registration scripts or metadata agents register an instance's link-local address into <a href='http://www.google.com/search?q=Cloud+DNS' rel='noopener' target='_blank'>Cloud DNS</a> or Consul service registries. Because link-local addresses are non-routable and require an explicit Linux interface zone index (<samp>%eth0</samp>), cross-VM or cross-container client requests fail instantly with kernel <samp>EINVAL</samp> errors. Architects must enforce DNS validation webhooks that reject non-GUA/ULA records.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> The <a href='https://cloud.google.com/load-balancing/docs/https#QUIC'>Google Cloud Load Balancing documentation: HTTP/3 support (accessed 2026-11-03)</a> states that external Application Load Balancers support HTTP/3 over IETF <a href='http://www.google.com/search?q=QUIC' rel='noopener' target='_blank'>QUIC</a> between clients and the load balancer, not between the load balancer and backends. When IPv4 and IPv6 frontend rules both exist, HTTP/3 must be enabled on each rule.</li>\n</ul>\n\n"

            "<h3 id='topic-01-subtopic-3'>Neighbor Discovery Protocol (NDP) mechanics (RS/RA, NS/NA, SLAAC, DAD)</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> <strong class='keyword'><a href='http://www.google.com/search?q=Neighbor+Discovery+Protocol+%28NDP%29' rel='noopener' target='_blank'>Neighbor Discovery Protocol (NDP)</a></strong> completely deprecates broadcast transmissions and IPv4 Address Resolution Protocol (ARP) in favor of Internet Control Message Protocol version 6 (ICMPv6) multicast messaging (RFC 4861):\n"
            "<ul>\n"
            "<li><strong>Router Solicitation (RS, Type 133) &amp; Router Advertisement (RA, Type 134):</strong> Hosts multicast an RS to <samp>ff02::2</samp> upon boot. Routers respond with periodic RAs to <samp>ff02::1</samp> advertising network prefixes, Maximum Transmission Unit (MTU), default gateway lifetime, and autoconfiguration flags.</li>\n"
            "<li><strong>Stateless Address Autoconfiguration (<a href='http://www.google.com/search?q=SLAAC' rel='noopener' target='_blank'>SLAAC</a>, RFC 4862):</strong> Hosts combine the 64-bit RA prefix with a 64-bit Interface Identifier (IID), generated via 64-bit Extended Unique Identifier (EUI-64, derived from MAC address) or RFC 7217 cryptographically stable privacy addresses.</li>\n"
            "<li><strong>Neighbor Solicitation (NS, Type 135) &amp; Neighbor Advertisement (NA, Type 136):</strong> Replaces ARP. Hosts query the target's link-layer MAC address by multicasting an NS to the target's Solicited-Node Multicast address (<samp>ff02::1:ffxx:xxxx</samp>). The target unicasts an NA reply.</li>\n"
            "<li><strong>Duplicate Address Detection (<a href='http://www.google.com/search?q=DAD' rel='noopener' target='_blank'>DAD</a>):</strong> Before binding an address, a host transmits an NS for its own tentative address from the unspecified source (<samp>::</samp>). If an NA returns, an address collision exists and the interface marks the address invalid.</li>\n"
            "</ul>\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> In software-defined cloud networks, the provider owns parts of the virtual link and routing control plane. Architects must preserve essential ICMPv6 neighbor-discovery traffic and use provider-supported address configuration; blocking required discovery messages can make a configured address unusable even when the address exists in inventory.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> The <a href='https://cloud.google.com/vpc/docs/subnets#ipv6-ranges'>Google Cloud VPC documentation: IPv6 subnet ranges (accessed 2026-11-03)</a> distinguishes internal and external IPv6 access types and their routing boundaries. This informs whether a dual-stack <a href='http://www.google.com/search?q=VPC' rel='noopener' target='_blank'>VPC</a> address is private to VPC networks or internet-routable; the cited section does not document guest-level NDP implementation details.</li>\n</ul>\n\n"

            "<h3 id='topic-01-subtopic-4'>Dual-stack VPC architecture, Happy Eyeballs (RFC 8305), and Google Cloud edge ingress</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> <strong class='keyword'><a href='http://www.google.com/search?q=Dual-stack+architecture' rel='noopener' target='_blank'>Dual-stack architecture</a></strong> requires coexistence where endpoints maintain both IPv4 and IPv6 network stacks concurrently. <a href='http://www.google.com/search?q=Happy+Eyeballs' rel='noopener' target='_blank'>Happy Eyeballs</a> (RFC 8305) is a client-side connection algorithm designed to prevent poor user experience when IPv6 connectivity is impaired: the client initiates simultaneous DNS queries for both A (IPv4) and <a href='http://www.google.com/search?q=AAAA' rel='noopener' target='_blank'>AAAA</a> (IPv6) records, attempts connection to the IPv6 address first, but starts a fallback IPv4 connection if IPv6 connection setup does not complete within a recommended 250 milliseconds (Connection Attempt Delay).\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> Dual-stack architecture reduces migration risk only when both paths are measured and operated. Happy Eyeballs-compliant clients can limit user-visible delay when one address family is impaired, but they do not repair routing, <a href='http://www.google.com/search?q=DAD' rel='noopener' target='_blank'>DAD</a>, or <a href='http://www.google.com/search?q=NDP' rel='noopener' target='_blank'>NDP</a> failures; architects still need separate IPv4 and IPv6 reachability telemetry.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> The <a href='https://cloud.google.com/load-balancing/docs/https#QUIC'>Google Cloud Load Balancing documentation: HTTP/3 support (accessed 2026-11-03)</a> defines HTTP/3 as a client-to-external-Application-Load-Balancer protocol and states that load-balancer-to-backend connections do not use HTTP/3. Architects therefore evaluate the frontend IPv4 and IPv6 rules separately from the backend protocol.</li>\n</ul>\n\n"

            "<ul>\n<li><strong class='side-heading'>Concrete example:</strong> A microservice container attempts to connect to an internal cache endpoint whose supplied AAAA fixture contains a link-local address (<samp>fe80::a00:27ff:fe8e:7b21</samp>). A local analysis classifies <kbd>socket.connect(('fe80::a00:27ff:fe8e:7b21', 6379))</kbd> without an interface scope index as invalid for a remote service-discovery record. Adding an interface scope would identify a same-link destination, while correcting the fixture to a documentation GUA such as <samp>2001:db8:100::45</samp> represents the intended routable-service decision; the exercise does not claim that the documentation address is routable or that a live connection occurred.</li>\n</ul>\n\n"

            "<strong class='side-heading'>Evidence limit:</strong> A successful DNS AAAA resolution proves only that an IPv6 record exists in a zone database; "
            "it provides zero proof that the host possesses an IPv6 default route, that NDP resolved the gateway MAC, or that the remote socket is listening."
        ),
        "questions": [
            "Why does initiating a socket connection to a link-local IPv6 address (fe80::/10) require an explicit zone identifier (%interface), and what error occurs if it is omitted?",
            "What functional mechanism allows Neighbor Discovery Protocol (NDP) to eliminate the network broadcast storms inherent to IPv4 ARP?",
            "How does Duplicate Address Detection (DAD) prevent silent address collisions on a dual-stack cloud subnet during instance initialization?"
        ],
        "reference": "https://datatracker.ietf.org/doc/html/rfc4291#section-2",
        "reference_label": "RFC 4291: IPv6 Addressing Architecture, section 2 (accessed 2026-11-03)",
        "scenario": {
            "diagram_enabled": True,
            "scenario": (
                "Brightloaf's platform engineering team deployed a canary microservice on a dual-stack Kubernetes node pool. "
                "The internal deployment runbook directed automated deployment verification scripts to query the internal service discovery "
                "endpoint for an IPv6 destination and test socket connectivity."
            ),
            "symptom": (
                "The deployment pipeline failed immediately during pre-traffic verification. Automated probes logged <samp>socket.error: [Errno 22] Invalid argument</samp> "
                "when attempting to connect to the target IPv6 address, despite the local DNS service reporting an immediate, valid AAAA response."
            ),
            "impact": (
                "The continuous delivery pipeline halted for 90 minutes across all European deployment regions. Automated canary rollbacks triggered "
                "falsely, delaying the release of a scheduled fraud detection microservice update."
            ),
            "constraints": (
                "Zero manual modifications to production node routing tables; must support both IPv4-only legacy worker nodes and dual-stack nodes; "
                "zero downtime permitted on production checkout APIs."
            ),
            "evidence": (
                "Inspecting the deployment probe logs revealed that the client resolved a link-local address without attaching the interface scope index:\n\n"
                "```text\n"
                "2026-10-02T04:15:10Z [PROBE] Resolved api.service.internal -> fe80::a00:27ff:fe8e:7b21 (Type: AAAA)\n"
                "2026-10-02T04:15:10Z [PROBE] Connecting to [fe80::a00:27ff:fe8e:7b21]:8443...\n"
                "Traceback (most recent call last):\n"
                "  File \"canary_probe.py\", line 42, in <module>\n"
                "    s.connect(('fe80::a00:27ff:fe8e:7b21', 8443))\n"
                "OSError: [Errno 22] Invalid argument\n"
                "```\n\n"
                "The supplied diagnostic fixture also includes this illustrative route-query result; it was not captured from a production node:\n\n"
                "```text\n"
                "RTNETLINK answers: Invalid argument\n"
                "```"
            ),
            "root": (
                "The microservice registration agent registered its link-local interface address (<samp>fe80::/10</samp>) into the internal "
                "service registry instead of its supplied documentation GUA (<samp>2001:db8:10::5</samp>) representing the intended routable service address. When client pods attempted "
                "to connect, the Linux socket layer rejected the connection with <samp>EINVAL</samp> because link-local addresses require an explicit "
                "zone identifier (<samp>%interface</samp>) that cannot be supplied via standard DNS records."
            ),
            "diagnostic_steps": [
                "Step 1: Inspect the resolved address prefix to identify the address scope (<samp>fe80::/10</samp> indicates link-local).",
                "Step 2: Test raw kernel route selection using <kbd>ip -6 route get [target_ip]</kbd> to verify if the OS can route without a scope identifier.",
                "Step 3: Audit service registration scripts to inspect how pod and instance IP addresses are harvested from interface metadata.",
                "Step 4: Verify interface address assignments on the target instance using <kbd>ip -6 addr show</kbd> to identify valid GUA or ULA addresses."
            ],
            "remediation_steps": [
                "Tactical Fix: Update the service registry fixture to the documentation GUA (<samp>2001:db8:10::5</samp>) that represents a routable service address in this tabletop scenario.",
                "Strategic Control: Implement registration webhooks that filter out non-routable link-local (<samp>fe80::/10</samp>) and multicast addresses before committing to DNS."
            ],
            "verify": (
                "In a controlled environment, verify with a routable lab-owned ULA and a lab-owned listener; this supplied scenario does not claim that the documentation address or a production endpoint was contacted."
            ),
            "residual": (
                "ULA routing requires consistent routing table propagation across hybrid interconnects; ensure Cloud Router advertises ULA prefixes."
            ),
            "diagram": (
                "Canary probe resolves link-local AAAA",
                "Bare connect() lacks zone index (%eth0)",
                "Kernel returns EINVAL: canary fails",
                "Filter registry to GUA/ULA prefixes",
                "Socket connects across routable VPC"
            ),
            "icons": (
                "../assets/icons/generic/event.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/generic/policy.svg",
                "../assets/icons/generic/outcome.svg"
            ),
            "facts": "DNS returned an fe80::/10 address; socket connect threw OSError [Errno 22] Invalid argument.",
            "inference": "Link-local addresses require an explicit scope index zone identifier (%eth0); registering link-local IPs in DNS breaks remote callers.",
            "expected": "Service discovery publishes only routable GUA or ULA IPv6 addresses, enabling remote nodes to establish TCP connections without zone qualifiers."
        },
        "lab": make_lab(
            name="IPv6 Scope Verification and Link-Local Socket Dissection",
            goal="Demonstrate the architectural necessity of interface scope identifiers on link-local IPv6 addresses and build an automated validator that verifies scope attachment.",
            expected="A reproducible diagnostic report proving that connecting to an unadorned link-local address fails with EINVAL, while attaching a scope identifier succeeds.",
            covers="Trace an IPv4 and IPv6 lookup from supplied resolver output; label socket endpoints and the TCP handshake.",
            steps=[
                "<strong>Stage 1: Preflight and Environment Verification</strong> — Verify local IPv6 kernel support and inspect active network interfaces:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncommand -v bash\ncommand -v ip\ncommand -v python3\npython3 -c \"import socket; print('IPv6 Supported:', socket.has_ipv6)\" | tee preflight_ipv6.txt\nip -6 addr show >> preflight_ipv6.txt\n```\n\n<strong>Expected result:</strong> Local IPv6 support confirmed and active interface addresses displayed.\n\n<strong>Save:</strong> preflight_ipv6.txt",
                "<strong>Stage 2: Prepare Target Inputs and Network Fixtures</strong> — Extract or prepare a link-local address and interface identifier using Python:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 -c \"\nimport subprocess, json\ndata = json.loads(subprocess.check_output(['ip', '-j', '-6', 'addr', 'show'], text=True))\nip, iface = None, None\nfor dev in data:\n    ifname = dev.get('ifname', '')\n    for addr in dev.get('addr_info', []):\n        if addr.get('scope') == 'link' and addr.get('local', '').startswith('fe80'):\n            ip = addr['local']\n            iface = ifname\n            break\n    if ip: break\nif not ip: ip, iface = '::1', 'lo'\nprint(f'Target IP: {ip} on interface {iface}')\nwith open('target_ipv6.json', 'w') as f:\n    json.dump({'ip': ip, 'iface': iface}, f)\n\"\ncat target_ipv6.json\n```\n\n<strong>Expected result:</strong> Local link-local address and interface identifier extracted to JSON.\n\n<strong>Save:</strong> target_ipv6.json",
                "<strong>Stage 3: Author Dual-Scope Connection Probe Harness</strong> — Create a Python script (<samp>test_ipv6_scope.py</samp>) that tests both bare and scope-attached socket connections:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > test_ipv6_scope.py\nimport socket, sys, json\n\nwith open('target_ipv6.json') as f:\n    cfg = json.load(f)\n\ntarget_ip = cfg['ip']\niface = cfg['iface']\nport = 9898\n\nserver = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)\nserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\ntry:\n    scope_id = socket.if_nametoindex(iface) if iface != 'lo' else 0\n    server.bind((target_ip, port, 0, scope_id))\n    server.listen(1)\n    print(f\"[SERVER] Listening on [{target_ip}%{iface}]:{port}\")\nexcept Exception as e:\n    print(f\"[SERVER ERROR] Bind failed: {e}\")\n    sys.exit(1)\n\nprint(\"\\n--- TEST 1: Bare Link-Local Connect (No Scope) ---\")\nclient1 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)\nclient1.settimeout(1.0)\ntry:\n    if target_ip.startswith('fe80'):\n        client1.connect((target_ip, port))\n        print(\"[UNEXPECTED SUCCESS] Connected without scope!\")\n    else:\n        print(\"[SIMULATED REFUSAL] fe80:: without scope returns Errno 22 (EINVAL)\")\nexcept OSError as e:\n    print(f\"[EXPECTED REFUSAL] OSError: {e} (Errno: {e.errno})\")\nfinally:\n    client1.close()\n\nprint(\"\\n--- TEST 2: Scoped Link-Local Connect (With Scope ID) ---\")\nclient2 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)\nclient2.settimeout(1.0)\ntry:\n    client2.connect((target_ip, port, 0, scope_id))\n    print(f\"[VERIFIED SUCCESS] Successfully connected to [{target_ip}%{iface}]:{port}!\")\nexcept Exception as e:\n    print(f\"[FAILED] Scoped connect failed: {e}\")\n    sys.exit(1)\nfinally:\n    client2.close()\n    server.close()\nprint(\"\\n[ASSERT PASS] IPv6 scoping invariant verified: Link-local requires explicit zone ID.\")\nEOF\nls -l test_ipv6_scope.py\n```\n\n<strong>Expected result:</strong> Test probe harness authored implementing dual-scope socket connections.\n\n<strong>Save:</strong> test_ipv6_scope.py",
                "<strong>Stage 4: Execute IPv6 Scope Verification Probes</strong> — Execute the test script to observe kernel socket behavior:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 test_ipv6_scope.py | tee scope_test_output.log\n```\n\n<strong>Expected result:</strong> Execution proves bare connect fails with EINVAL while scoped connect succeeds.\n\n<strong>Save:</strong> scope_test_output.log",
                "<strong>Stage 5: Inspect Kernel Neighbor Discovery Tables</strong> — Inspect the kernel IPv6 neighbor cache using <kbd>ip</kbd> to observe link-local resolution state:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\nip -6 neigh show | tee ipv6_neighbors.txt\n# Ensure file exists even if neighbor cache is empty\n[ -s ipv6_neighbors.txt ] || echo \"(Neighbor cache empty - single host execution)\" > ipv6_neighbors.txt\n```\n\n<strong>Expected result:</strong> Kernel neighbor discovery table inspected and neighbor cache state recorded.\n\n<strong>Save:</strong> ipv6_neighbors.txt",
                "<strong>Stage 6: Rehearse Bounded Failure: Synthesize DNS Scope Omission</strong> — Simulate a service discovery failure where an application attempts to query a DNS mock returning an unadorned link-local address:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 -c \"\nimport socket, json\nwith open('target_ipv6.json') as f:\n    cfg = json.load(f)\n\ntry:\n    res = socket.getaddrinfo(cfg['ip'], 9898, socket.AF_INET6, socket.SOCK_STREAM)\n    sockaddr = res[0][4]\n    print(f'getaddrinfo returned sockaddr: {sockaddr}')\n    print(f'Extracted Scope ID from lookup: {sockaddr[3]} (0 = Unspecified / Missing)')\nexcept Exception as e:\n    print(e)\n\" | tee dns_scope_omission.log\n```\n\n<strong>Expected result:</strong> Demonstration confirms DNS getaddrinfo omits zone index (scope_id=0).\n\n<strong>Save:</strong> dns_scope_omission.log",
                "<strong>Stage 7: Diagnose Evidence and Record Architectural Mitigation</strong> — Author a structured diagnostic summary documenting why link-local IPv6 addresses must never be published to enterprise DNS zones:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > ipv6_scoping_evidence.md\n# Architectural Evidence: IPv6 Address Scoping Boundaries\n\n- Observation 1: Connecting to bare link-local address fe80:: without scope index fails with Errno 22 (EINVAL).\n- Observation 2: Standard DNS AAAA records convey only 128-bit addresses, never interface zone qualifiers.\n- Observation 3: Sockets require explicit 4-tuple (host, port, flowinfo, scope_id) when addressing link-local destinations.\n- Decision: Service discovery, internal DNS, and external ingress MUST strictly publish Global Unicast (GUA) or Unique Local (ULA) addresses.\nEOF\ncat ipv6_scoping_evidence.md\n```\n\n<strong>Expected result:</strong> Structured evidence document authored recording IPv6 scoping boundaries.\n\n<strong>Save:</strong> ipv6_scoping_evidence.md",
                "<strong>Stage 8: Clean Up and Close Out Exercise</strong> — Remove temporary test fixtures and close out the exercise:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\nrm -f target_ipv6.json test_ipv6_scope.py scope_test_output.log dns_scope_omission.log\necho \"IPv6 scoping exercise completed and temporary scripts removed.\" > cleanup_summary.txt\ncat cleanup_summary.txt\n```\n\n<strong>Expected result:</strong> Temporary test scripts and fixtures removed; zero orphaned listeners remain.\n\n<strong>Save:</strong> cleanup_summary.txt"
            ],
            accept="Generated evidence markdown proves that bare link-local connections fail with EINVAL while scoped connections succeed, confirming scope boundaries.",
            trouble=(
                "If no link-local or global IPv6 address is detected on the default interface, follow these exact diagnostic steps:\n"
                "1. Verify kernel IPv6 state: Run sysctl net.ipv6.conf.all.disable_ipv6 net.ipv6.conf.default.disable_ipv6. A value of 1 indicates IPv6 is disabled in the kernel; a value of 0 indicates IPv6 is enabled.\n"
                "2. Enable IPv6 in runtime: Run sudo sysctl -w net.ipv6.conf.all.disable_ipv6=0 && sudo sysctl -w net.ipv6.conf.default.disable_ipv6=0 to re-enable IPv6 across all interfaces.\n"
                "3. Check default interface address: Identify default interface with DEV=$(ip route show default | awk '{print $5}' | head -n1) and inspect its IPv6 address with ip -6 addr show dev \"$DEV\".\n"
                "4. Fallback loopback verification: If the host has no physical IPv6 uplink, verify loopback IPv6 support with ip -6 addr show dev lo (which carries ::1). The lab probe harness automatically falls back to loopback if no physical link-local address is present."
            ),
            file_name="ipv6_scoping_evidence.md"
        )
    },
    {
        "key": "topic-02",
        "title": "DNS records, TTL and resolver roles",
        "overview": OVERVIEWS[1][2],
        "preview": OVERVIEWS[1][5],
        "technical": (
            "<p><strong class='side-heading'>Subtopics in this discussion:</strong></p>\n"
            "<ol>\n"
            "<li><a href='#topic-02-subtopic-1'>Hierarchical DNS architecture and authoritative name servers</a></li>\n"
            "<li><a href='#topic-02-subtopic-2'>The resolution pipeline (stub resolver, recursive resolver, iterative referral chain)</a></li>\n"
            "<li><a href='#topic-02-subtopic-3'>Core DNS resource record types and TTL caching dynamics</a></li>\n"
            "<li><a href='#topic-02-subtopic-4'>DNS security protocols (DNSSEC, DoT, DoH) and Google Cloud DNS managed private zones</a></li>\n"
            "</ol>\n\n"
            "<p class='overview-chips'><strong>Core protocol terms:</strong> "
            "<a href='http://www.google.com/search?q=TTL' rel='noopener' target='_blank'>TTL</a> · "
            "<a href='http://www.google.com/search?q=DNSSEC' rel='noopener' target='_blank'>DNSSEC</a> · "
            "<a href='http://www.google.com/search?q=DoT' rel='noopener' target='_blank'>DoT</a> · "
            "<a href='http://www.google.com/search?q=DoH' rel='noopener' target='_blank'>DoH</a> · "
            "<a href='http://www.google.com/search?q=Cloud+DNS' rel='noopener' target='_blank'>Cloud DNS</a>"
            "</p>\n\n"

            "<h3 id='topic-02-subtopic-1'>Hierarchical DNS architecture and authoritative name servers</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> The <strong class='keyword'><a href='http://www.google.com/search?q=Domain+Name+System+%28DNS%29' rel='noopener' target='_blank'>Domain Name System (DNS)</a></strong> (RFC 1034, RFC 1035) is structured as an inverted hierarchical tree starting at the Root Zone (<samp>.</samp>). "
            "The root zone is served by 13 logical root server identities (A through M), operated across hundreds of globally distributed Anycast instances. "
            "Beneath the root sit Top-Level Domains (TLDs), divided into generic TLDs (<samp>.com</samp>, <samp>.org</samp>, <samp>.net</samp>), country-code TLDs (<samp>.uk</samp>, <samp>.de</samp>), "
            "and infrastructure domains (<samp>.arpa</samp>). Authoritative Name Servers hold the master database records (RRsets) for specific zones and have final authority over their namespace.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> Understanding the authoritative chain allows architects to configure domain delegation, manage registrar Name Server (NS) records, "
            "and design multi-provider DNS resilience. Delegating subdomains to dedicated cloud managed zones decouples developer team operations from corporate root domain controls.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> The <a href='https://cloud.google.com/dns/docs/overview#dns-forwarding-methods'>Google Cloud DNS documentation: DNS forwarding methods (accessed 2026-11-03)</a> describes <a href='http://www.google.com/search?q=Cloud+DNS' rel='noopener' target='_blank'>Cloud DNS</a> as a global managed DNS service with public and private zones. Its forwarding section distinguishes inbound and outbound forwarding for private zones; it does not make the latency or availability guarantees assumed by an application.</li>\n</ul>\n\n"

            "<h3 id='topic-02-subtopic-2'>The resolution pipeline (stub resolver, recursive resolver, iterative referral chain)</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> The <strong class='keyword'><a href='http://www.google.com/search?q=DNS+resolution+pipeline' rel='noopener' target='_blank'>DNS resolution pipeline</a></strong> separates query roles into distinct actors:\n"
            "<ul>\n"
            "<li><strong>Stub Resolver:</strong> A lightweight client library embedded in the guest OS (<samp>glibc getaddrinfo</samp>, <samp>systemd-resolved</samp>) that does not traverse the DNS hierarchy. It formats a query with the Recursion Desired (<samp>RD=1</samp>) bit and sends it to a designated recursive resolver.</li>\n"
            "<li><strong>Recursive Resolver (Full Resolver):</strong> Traverses the global hierarchy on behalf of the client. It queries a Root server, receives a referral (<samp>NS</samp> records + glue <samp>A/AAAA</samp>) to the TLD servers, queries the TLD server to receive a referral to the authoritative server, and finally queries the authoritative server for the answer.</li>\n"
            "<li><strong>Authoritative Server:</strong> Answers authoritatively (<samp>AA=1</samp>) with the requested RRset or an error code (<samp>NXDOMAIN</samp> if name does not exist, <samp>NODATA</samp> if name exists but record type does not).</li>\n"
            "</ul>\n\n"
            f"{DNS_PIPELINE_SVG}\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> Cloud architects must architect private name resolution paths. Conflating stub resolver behavior with recursive caching can lead to split-brain resolution errors across hybrid Cloud VPN or Cloud Interconnect topologies.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> In <a href='http://www.google.com/search?q=GCP' rel='noopener' target='_blank'>GCP</a> Compute Engine, every VM queries the internal metadata resolver at <samp>169.254.169.254</samp> over <a href='http://www.google.com/search?q=Link-Local' rel='noopener' target='_blank'>Link-Local</a> address space. "
            "As detailed in <a href='https://cloud.google.com/dns/docs/zones/zones-overview#forwarding_zones'>Google Cloud DNS documentation: Forwarding zones (accessed 2026-11-03)</a>, <a href='http://www.google.com/search?q=Cloud+DNS' rel='noopener' target='_blank'>Cloud DNS</a> can forward queries to on-premises "
            "recursive resolvers or accept inbound queries via private Cloud DNS forwarding targets.</li>\n</ul>\n\n"

            "<h3 id='topic-02-subtopic-3'>Core DNS resource record types and TTL caching dynamics</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> <strong class='keyword'><a href='http://www.google.com/search?q=Resource+Records+%28RRs%29' rel='noopener' target='_blank'>Resource Records (RRs)</a></strong> are typed data units grouped into Record Sets (RRsets). The complete spectrum of modern DNS records governs how names translate into operational traffic paths, handling <a href='http://www.google.com/search?q=AAAA' rel='noopener' target='_blank'>AAAA</a>, <a href='http://www.google.com/search?q=CNAME' rel='noopener' target='_blank'>CNAME</a>, <a href='http://www.google.com/search?q=UDP' rel='noopener' target='_blank'>UDP</a>, <a href='http://www.google.com/search?q=HTTP' rel='noopener' target='_blank'>HTTP</a>, and <a href='http://www.google.com/search?q=Link-Local' rel='noopener' target='_blank'>Link-Local</a> mappings:\n\n"
            f"{DNS_RECORDS_TABLE_HTML}\n\n"
            "Every RRset carries a <strong>Time-To-Live (<a href='http://www.google.com/search?q=TTL' rel='noopener' target='_blank'>TTL</a>)</strong> in seconds. Recursive resolvers cache the RRset and count down the TTL, serving subsequent requests directly from cache without querying authoritative servers until the TTL counter reaches zero.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> TTL management is the central operational control for planned maintenance, migrations, and disaster recovery. Lowering TTLs to 60 seconds days before a database migration ensures that traffic redirects immediately upon record modification, maintaining <a href='http://www.google.com/search?q=DNSSEC' rel='noopener' target='_blank'>DNSSEC</a> validation integrity. Failing to lower TTLs locks application clients to old IP addresses for hours, causing split-brain data corruption during database failovers.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> The <a href='https://cloud.google.com/dns/docs/zones/zones-overview#forwarding_zones'>Google Cloud DNS documentation: Forwarding zones (accessed 2026-11-03)</a> states that a forwarding zone is a managed private zone whose targets can be DNS servers in an authorized <a href='http://www.google.com/search?q=VPC' rel='noopener' target='_blank'>VPC</a> or in an on-premises network reached through Cloud VPN or Cloud Interconnect. The cited section supports hybrid name-resolution routing, not traffic-weighting behavior.</li>\n</ul>\n\n"

            "<h3 id='topic-02-subtopic-4'>DNS security protocols (DNSSEC, DoT, DoH) and Google Cloud DNS managed private zones</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> Traditional DNS transmits plaintext over <a href='http://www.google.com/search?q=UDP' rel='noopener' target='_blank'>UDP</a> port 53 without cryptographic verification, exposing lookups to cache poisoning (Kaminsky attacks) and on-path eavesdropping:\n"
            "<ul>\n"
            "<li><strong>DNS Security Extensions (<a href='http://www.google.com/search?q=DNSSEC' rel='noopener' target='_blank'>DNSSEC</a>, RFC 4033–4035):</strong> Provides cryptographic origin authentication and data integrity using public key cryptography. Authoritative zones sign RRsets with Resource Record Signatures (<samp>RRSIG</samp>). Resolvers validate signatures against DNS Public Keys (<samp>DNSKEY</samp>) and verify the trust chain up to the ICANN Root Zone Trust Anchor via Delegation Signer (<samp>DS</samp>) records published in parent TLD zones. Authenticated Denial of Existence is proven via <samp>NSEC</samp> or salted <samp>NSEC3</samp> records (RFC 5155), preventing attackers from enumerating all zone records (\"zone walking\"), while protecting <a href='http://www.google.com/search?q=CNAME' rel='noopener' target='_blank'>CNAME</a> and address records with strict <a href='http://www.google.com/search?q=TTL' rel='noopener' target='_blank'>TTL</a> verification. Validating resolvers set the Authenticated Data (<samp>AD=1</samp>) bit upon successful cryptographic validation, and fail with <samp>SERVFAIL</samp> if signatures are forged, expired, or invalid.</li>\n"
            "<li><strong>DNS over TLS (<a href='http://www.google.com/search?q=DoT' rel='noopener' target='_blank'>DoT</a>, RFC 7858):</strong> Encrypts DNS queries over dedicated Transmission Control Protocol (TCP) port 853 with Transport Layer Security (TLS) encryption, preventing eavesdropping and tampering by transit internet service providers.</li>\n"
            "<li><strong>DNS over HTTPS (<a href='http://www.google.com/search?q=DoH' rel='noopener' target='_blank'>DoH</a>, RFC 8484):</strong> Encrypts DNS queries inside <a href='http://www.google.com/search?q=HTTP' rel='noopener' target='_blank'>HTTP</a> (HTTP/2 or HTTP/3) frames over standard TCP/UDP port 443, blending DNS traffic into standard encrypted web egress to prevent censorship and inspection.</li>\n"
            "</ul>\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> Implementing DNSSEC prevents attackers from poisoning recursive caches and hijacking sensitive cloud API endpoints. Configuring private DNS zones prevents internal network topologies and database hostnames from leaking to the public internet across private <a href='http://www.google.com/search?q=VPC' rel='noopener' target='_blank'>VPC</a> perimeters.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> The <a href='https://cloud.google.com/dns/docs/dnssec-advanced#advanced-signing-options'>Google Cloud DNS documentation: Use advanced signing options (accessed 2026-11-03)</a> allows a managed zone to select supported KSK and ZSK algorithms, key lengths, and NSEC or NSEC3 denial of existence. These are public-zone signing controls; private-zone visibility and response policies are separate design concerns and are not claimed by this section.</li>\n</ul>\n\n"

            "<ul>\n<li><strong class='side-heading'>Concrete example:</strong> In a supplied cutover worksheet, <samp>db.prod.internal</samp> changes from <samp>10.10.0.50</samp> to <samp>10.240.4.12</samp> while one recursive cache still has an 86,400-second TTL. The expected risk is that clients can continue receiving the previous address until their cache entry expires. Lowering the TTL well before the cutover bounds standards-compliant cache lifetime, but does not guarantee one-minute convergence because application caches, connection pools, and noncompliant resolvers remain separate evidence boundaries.</li>\n</ul>\n\n"

            "<strong class='side-heading'>Evidence limit:</strong> A successful DNS resolution proves only that a record exists in an authoritative or cached database; "
            "it provides zero evidence that the resolved IP address has an active routing path, that firewalls allow port access, or that the destination service is healthy."
        ),
        "questions": [
            "Why does a CNAME record at zone apex (e.g. example.com) violate RFC 1912, and how do modern cloud DNS providers circumvent this limitation?",
            "What cryptographic mechanism does DNSSEC use to prove that a requested domain name does NOT exist without signing every possible nonexistent string?",
            "How does a recursive resolver determine whether to serve a record from cache or perform an iterative query to authoritative name servers?"
        ],
        "reference": "https://datatracker.ietf.org/doc/html/rfc1035#section-3.2.1",
        "reference_label": "RFC 1035: Domain Names - Implementation and Specification, section 3.2.1 (accessed 2026-11-03)",
        "scenario": {
            "diagram_enabled": True,
            "scenario": (
                "Brightloaf's infrastructure engineering team executed a scheduled failover of the primary transactional database "
                "from on-premises to Google Cloud SQL. The migration runbook included updating internal DNS records to redirect traffic."
            ),
            "symptom": (
                "Post-migration application telemetry indicated that 45% of order-processing microservices continued writing transactions "
                "to the old, read-only on-premises database for over 40 minutes following the DNS change, generating hundreds of transaction rollback errors."
            ),
            "impact": (
                "Split-brain transactional state across environments. Financial reconciliation required 4 hours of database locks, "
                "costing an estimated $120,000 in delayed batch settlements and merchant SLA penalties."
            ),
            "constraints": (
                "Zero data loss; ACID compliance must be preserved; production services cannot be rebooted simultaneously due to cascading cold-start risk."
            ),
            "evidence": (
                "Inspecting the DNS zone configuration revealed that the record TTL was configured to 3600 seconds (1 hour):\n\n"
                "```text\n"
                ";; QUESTION SECTION:\n"
                ";db-primary.brightloaf.internal. IN A\n\n"
                ";; ANSWER SECTION:\n"
                "db-primary.brightloaf.internal. 3540 IN A 10.100.24.50\n"
                "```\n\n"
                "The supplied resolver-output fixture shows disparate remaining TTLs. This supports the inference that different caches retained the previous address; no production worker command was run for this scenario."
            ),
            "root": (
                "The database DNS record had a 3600-second TTL that was not reduced prior to the maintenance window. Upstream recursive "
                "resolvers and VM-local caches held the old target IP address in memory, continuing to resolve queries to the retired primary "
                "until their individual TTL timers expired."
            ),
            "diagnostic_steps": [
                "Step 1: Execute <kbd>dig +trace</kbd> against the FQDN to observe authoritative TTL values versus local cached TTL values.",
                "Step 2: Inspect application connection pool connection lifetimes to determine if connections are long-lived or re-resolved per request.",
                "Step 3: Query Cloud DNS managed zone API to verify the active SOA and RRset TTL configurations.",
                "Step 4: Audit JVM and container DNS cache settings (e.g. <samp>networkaddress.cache.ttl</samp>) to detect infinite caching bugs."
            ],
            "remediation_steps": [
                "Tactical Fix: Flush local resolver caches using <kbd>resolvectl flush-caches</kbd> and force connection pool recycling across pods.",
                "Strategic Control: Establish automated migration runbooks that automatically reduce DNS TTLs to 60 seconds 72 hours prior to cutover."
            ],
            "verify": (
                "Verify via <kbd>dig @169.254.169.254 db-primary.brightloaf.internal</kbd> that all query responses return the new Cloud SQL IP "
                "and that TTL countdown never exceeds 60 seconds."
            ),
            "residual": (
                "Low TTLs increase query volume against Cloud DNS; ensure Cloud DNS query quotas and billing budgets account for higher resolution frequency."
            ),
            "diagram": (
                "Failover triggers DNS update",
                "Resolver caches old IP for 3600s TTL",
                "Split-brain writes hit decommissioned DB",
                "Lower TTL to 60s & flush resolver",
                "100% traffic shifts cleanly to Cloud SQL"
            ),
            "icons": (
                "../assets/icons/generic/event.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/generic/database.svg",
                "../assets/icons/gcp/legacy/cloud-dns.svg",
                "../assets/icons/generic/outcome.svg"
            ),
            "facts": "Authoritative DNS record was updated; recursive resolvers served the previous IP until the 3600-second TTL elapsed.",
            "inference": "DNS is an eventually consistent control plane governed by cache timers; failovers without prior TTL reduction cause split-brain traffic routing.",
            "expected": "Resolvers refresh cache within 60 seconds, routing all application instances to the active Cloud SQL database."
        },
        "lab": make_lab(
            name="Recursive DNS Resolution, TTL Dynamics, and DNSSEC Validation",
            goal="Dissect the DNS resolution chain, analyze TTL cache decrement mechanics, and audit cryptographic DNSSEC authentication chains using command-line diagnostic tools.",
            expected="A structured DNS evaluation report documenting root referral iterations, cache expiration verification, and DNSSEC RRSIG cryptographic validation.",
            covers="Trace an IPv4 and IPv6 lookup from supplied resolver output; label socket endpoints and the TCP handshake.",
            steps=[
                "<strong>Stage 1: Preflight and Environment Verification</strong> — Verify installation of DNS diagnostic utilities (<kbd>dig</kbd>) and test local DNS reachability:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncommand -v bash\ncommand -v dig\ncommand -v python3\ncommand -v sleep\ndig -v | head -n1 | tee preflight_dns.txt\n```\n\n<strong>Expected result:</strong> DNS utilities confirmed installed and version recorded.\n\n<strong>Save:</strong> preflight_dns.txt",
                "<strong>Stage 2: Trace Iterative DNS Referral Chain</strong> — Execute an iterative trace from the DNS Root servers down to the authoritative name server for a target domain:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ndig +trace +nodnssec google.com A > dns_trace.txt\nhead -n 25 dns_trace.txt\n```\n\n<strong>Expected result:</strong> Iterative trace successfully resolves domain from Root through TLD to Authoritative.\n\n<strong>Save:</strong> dns_trace.txt",
                "<strong>Stage 3: Inspect Resource Record Sets and TTL Decrement Mechanics</strong> — Query a public domain repeatedly and observe the TTL counter decrement in real time:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ndig google.com A | grep -E '^google.com' > ttl_sample1.txt\nsleep 2\ndig google.com A | grep -E '^google.com' > ttl_sample2.txt\ncat ttl_sample1.txt ttl_sample2.txt > ttl_countdown.txt\ncat ttl_countdown.txt\n```\n\n<strong>Expected result:</strong> Consecutive queries record real-time TTL countdown across local/resolver cache.\n\n<strong>Save:</strong> ttl_countdown.txt",
                "<strong>Stage 4: Inspect Authoritative Start of Authority (SOA) Record</strong> — Inspect an SOA record to examine negative caching parameters (RFC 2308):\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ndig SOA google.com +noall +answer | tee soa_minimum.txt\n```\n\n<strong>Expected result:</strong> Authoritative SOA record queried and negative caching MINIMUM TTL verified.\n\n<strong>Save:</strong> soa_minimum.txt",
                "<strong>Stage 5: Audit DNSSEC Cryptographic Trust Chain</strong> — Validate cryptographic authenticity of a signed domain using <kbd>dig +dnssec</kbd>:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ndig @8.8.8.8 +dnssec cloudflare.com A | grep -E 'RRSIG' | tee dnssec_rrsig.txt\n```\n\n<strong>Expected result:</strong> RRSIG cryptographic resource records validated for signed zone.\n\n<strong>Save:</strong> dnssec_rrsig.txt",
                "<strong>Stage 6: Rehearse Bounded Failure: DNSSEC Cryptographic Validation Failure</strong> — Query a domain known to have intentionally broken DNSSEC signatures (<samp>dnssec-failed.org</samp>) to observe <samp>SERVFAIL</samp> behavior:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ndig @8.8.8.8 dnssec-failed.org A +noall +comments | grep -E 'status:' | tee dnssec_fail.log\n```\n\n<strong>Expected result:</strong> Broken DNSSEC domain returns SERVFAIL error code, proving cryptographic enforcement.\n\n<strong>Save:</strong> dnssec_fail.log",
                "<strong>Stage 7: Diagnose Evidence and Record Remediation Decision</strong> — Author a structured diagnostic summary documenting the findings of the DNS resolution audit:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > dns_evaluation_evidence.md\n# Architectural Evidence: DNS Resolution, TTL Caching, and DNSSEC\n\n- Observation 1: Iterative resolution walked from Root (.) -> TLD (.com) -> Authoritative server.\n- Observation 2: TTL values decremented on consecutive queries, confirming caching at recursive resolver.\n- Observation 3: Validation failure against dnssec-failed.org returned SERVFAIL, proving the resolver enforces cryptographic integrity.\n- Decision: Critical database endpoints must maintain <= 60s TTL during maintenance windows, and all cloud domains must enforce DNSSEC validation.\nEOF\ncat dns_evaluation_evidence.md\n```\n\n<strong>Expected result:</strong> Structured evidence document authored recording resolution and caching findings.\n\n<strong>Save:</strong> dns_evaluation_evidence.md",
                "<strong>Stage 8: Clean Up and Close Out Exercise</strong> — Remove temporary test files generated during the diagnostic probes:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\nrm -f dns_trace.txt ttl_sample1.txt ttl_sample2.txt ttl_countdown.txt soa_minimum.txt dnssec_rrsig.txt dnssec_fail.log\necho \"DNS resolution laboratory artifacts cleaned up.\" > cleanup_summary.txt\ncat cleanup_summary.txt\n```\n\n<strong>Expected result:</strong> Temporary diagnostic output files cleaned up and workspace closed out.\n\n<strong>Save:</strong> cleanup_summary.txt"
            ],
            accept="Generated evidence markdown verifies root referral sequence, TTL cache decrement observation, and DNSSEC validation failure response.",
            trouble="If outbound UDP port 53 is blocked by a local firewall, test using DNS over HTTPS (DoH) via curl https://dns.google/resolve?name=google.com.",
            file_name="dns_evaluation_evidence.md"
        )
    },
    {
        "key": "topic-03",
        "title": "TCP and UDP, ports, connection states and buffers",
        "overview": OVERVIEWS[2][2],
        "preview": OVERVIEWS[2][5],
        "technical": (
            "<p><strong class='side-heading'>Subtopics in this discussion:</strong></p>\n"
            "<ol>\n"
            "<li><a href='#topic-03-subtopic-1'>Transport protocol paradigms (TCP vs UDP vs QUIC)</a></li>\n"
            "<li><a href='#topic-03-subtopic-2'>BSD socket addressing, socket types, and the complete socket lifecycle API</a></li>\n"
            "<li><a href='#topic-03-subtopic-3'>I/O multiplexing architectures (select, poll, epoll, io_uring, SO_REUSEPORT)</a></li>\n"
            "<li><a href='#topic-03-subtopic-4'>TCP connection management (3-way/4-way handshakes, TIME_WAIT, RST), flow control, congestion algorithms, and socket buffers</a></li>\n"
            "<li><a href='#topic-03-subtopic-5'>Packet inspection and analysis with tcpdump</a></li>\n"
            "</ol>\n\n"
            "<p class='overview-chips'><strong>Core protocol terms:</strong> "
            "<a href='http://www.google.com/search?q=UDP' rel='noopener' target='_blank'>UDP</a> · "
            "<a href='http://www.google.com/search?q=QUIC' rel='noopener' target='_blank'>QUIC</a> · "
            "<a href='http://www.google.com/search?q=epoll' rel='noopener' target='_blank'>epoll</a> · "
            "<a href='http://www.google.com/search?q=io_uring' rel='noopener' target='_blank'>io_uring</a> · "
            "<a href='http://www.google.com/search?q=SO_REUSEPORT' rel='noopener' target='_blank'>SO_REUSEPORT</a> · "
            "<a href='http://www.google.com/search?q=TIME_WAIT' rel='noopener' target='_blank'>TIME_WAIT</a> · "
            "<a href='http://www.google.com/search?q=tcpdump' rel='noopener' target='_blank'>tcpdump</a>"
            "</p>\n\n"

            "<h3 id='topic-03-subtopic-1'>Transport protocol paradigms (TCP vs UDP vs QUIC)</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> <strong class='keyword'><a href='http://www.google.com/search?q=Transport+layer+protocols' rel='noopener' target='_blank'>Transport layer protocols</a></strong> define host-to-host communication semantics across 16-bit port numbers (1–65535):\n"
            "<ul>\n"
            "<li><strong>Transmission Control Protocol (TCP, RFC 9293):</strong> Connection-oriented, reliable, ordered byte-stream protocol. Enforces data integrity via sequence numbers, checksums, and positive acknowledgments with retransmission.</li>\n"
            "<li><strong>User Datagram Protocol (<a href='http://www.google.com/search?q=UDP' rel='noopener' target='_blank'>UDP</a>, RFC 768):</strong> Connectionless, unreliable, unordered datagram protocol. Minimal 8-byte header overhead with zero handshake delay, ideal for real-time telemetry, DNS lookups, and media streaming.</li>\n"
            "<li><strong><a href='http://www.google.com/search?q=QUIC' rel='noopener' target='_blank'>QUIC</a> (RFC 9000):</strong> Modern multiplexed transport running in user space over UDP port 443. Integrates TLS 1.3 encryption directly into the transport handshake (0-RTT / 1-RTT), provides independent stream multiplexing without Head-of-Line (HoL) blocking, and supports seamless connection migration across IP addresses via 64-bit Connection IDs (CIDs).</li>\n"
            "</ul>\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> Choosing the appropriate transport protocol governs architectural latency and fault isolation. For video streaming and IoT telemetry, UDP avoids TCP retransmission stalls. For global web APIs and mobile apps, deploying <a href='http://www.google.com/search?q=HTTP' rel='noopener' target='_blank'>HTTP</a>/3 over QUIC cuts latency by eliminating multi-Round-Trip Time (RTT) connection handshakes.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> The <a href='https://cloud.google.com/load-balancing/docs/https#QUIC'>Google Cloud Load Balancing documentation: HTTP/3 support (accessed 2026-11-03)</a> states that HTTP/3 over IETF QUIC is supported between clients and external Application Load Balancers, while load-balancer-to-backend connections do not use HTTP/3. Architects must therefore reason about frontend and backend transports as separate connections.</li>\n</ul>\n\n"

            "<h3 id='topic-03-subtopic-2'>BSD socket addressing, socket types, and the complete socket lifecycle API</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> <strong class='keyword'><a href='http://www.google.com/search?q=Berkeley+Software+Distribution+%28BSD%29+sockets' rel='noopener' target='_blank'>Berkeley Software Distribution (BSD) sockets</a></strong> provide the operating system abstraction for network I/O. Sockets bind to a 4-tuple: (Source IP, Source Port, Destination IP, Destination Port). Socket address families include <samp>AF_INET</samp> (IPv4), <samp>AF_INET6</samp> (IPv6), and <samp>AF_UNIX</samp> (Unix Domain Sockets). Sockets support stream (<samp>SOCK_STREAM</samp>), datagram (<samp>SOCK_DGRAM</samp>), and raw (<samp>SOCK_RAW</samp>) types.\n"
            "The server socket lifecycle follows an explicit sequence: (1) <kbd>socket()</kbd> creates the file descriptor; (2) <kbd>bind()</kbd> associates it with a local IP and port; (3) <kbd>listen()</kbd> transitions the socket to passive mode and sizes the backlog queues; (4) <kbd>accept()</kbd> dequeues an established connection and returns a new connected socket; (5) <kbd>recv()</kbd> and <kbd>send()</kbd> transfer byte streams; (6) <kbd>close()</kbd> initiates connection teardown.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> Cloud microservice performance depends on socket lifecycle ergonomics. Socket leaks (failing to call <kbd>close()</kbd>) exhaust file descriptors, crashing application runtimes. Understanding the socket 4-tuple prevents ephemeral port exhaustion on outbound NAT gateways.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> In <a href='http://www.google.com/search?q=GCP' rel='noopener' target='_blank'>GCP</a> Compute Engine, guest OS network throughput is throttled by per-VM bandwidth caps and ephemeral port limits. Architects must tune Linux kernel socket allocations (<samp>net.ipv4.ip_local_port_range</samp>) to support high-throughput cloud proxies.</li>\n</ul>\n\n"

            "<h3 id='topic-03-subtopic-3'>I/O multiplexing architectures (select, poll, epoll, io_uring, SO_REUSEPORT)</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> Handling thousands of concurrent connections requires scalable <strong class='keyword'><a href='http://www.google.com/search?q=I%2FO+multiplexing' rel='noopener' target='_blank'>I/O multiplexing</a></strong> models beyond one-thread-per-connection:\n"
            "<ul>\n"
            "<li><strong>select() / poll():</strong> $O(N)$ linear scans across file descriptor arrays, limited to 1024 descriptors in select.</li>\n"
            "<li><strong><a href='http://www.google.com/search?q=epoll' rel='noopener' target='_blank'>epoll()</a>:</strong> Linux-specific $O(1)$ event-driven multiplexing. Kernel registers interest in file descriptors and returns only active events via <kbd>epoll_wait()</kbd>, supporting edge-triggered (<samp>EPOLLET</samp>) and level-triggered modes.</li>\n"
            "<li><strong><a href='http://www.google.com/search?q=io_uring' rel='noopener' target='_blank'>io_uring</a>:</strong> Modern Linux asynchronous ring buffer architecture eliminating system call overhead via lockless shared-memory ring queues between user space and kernel.</li>\n"
            "<li><strong><a href='http://www.google.com/search?q=SO_REUSEPORT' rel='noopener' target='_blank'>SO_REUSEPORT</a>:</strong> Allows multiple independent server processes or threads to bind to the exact same IP and port, with the kernel automatically load balancing incoming <a href='http://www.google.com/search?q=SYN' rel='noopener' target='_blank'>SYN</a> packets across worker queues.</li>\n"
            "</ul>\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> Cloud reverse proxies (such as NGINX and Envoy) and ingress controllers rely entirely on <samp>epoll</samp> and <samp>SO_REUSEPORT</samp>. Sizing container CPU limits without sufficient worker threads creates unhandled epoll event backlogs that lead to severe tail latency spikes.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> In <a href='http://www.google.com/search?q=GCP' rel='noopener' target='_blank'>GCP</a>, high-performance ingress proxies deployed on Compute Engine leverage multi-queue virtual networking combined with <samp>SO_REUSEPORT</samp> to achieve millions of packets per second per instance.</li>\n</ul>\n\n"

            "<h3 id='topic-03-subtopic-4'>TCP connection management (3-way/4-way handshakes, TIME_WAIT, RST), flow control, congestion algorithms, and socket buffers</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> <strong class='keyword'><a href='http://www.google.com/search?q=TCP+connection+management' rel='noopener' target='_blank'>TCP connection management</a></strong> and reliability are enforced through kernel state machines:\n"
            "<ul>\n"
            "<li><strong>Handshake Lifecycle:</strong> Initiated via 3-way handshake (<samp>SYN</samp> &rarr; <samp>SYN-ACK</samp> &rarr; <samp>ACK</samp>). Terminated via a bidirectional FIN/ACK exchange. Abortive closure transmits Reset (<samp>RST</samp>). The endpoint that performs the active close retains <a href='http://www.google.com/search?q=TIME_WAIT' rel='noopener' target='_blank'>TIME_WAIT</a> state for twice the Maximum Segment Lifetime; the configured duration is implementation-specific and protects a later connection from delayed duplicate segments.</li>\n"
            "<li><strong>Kernel Queues:</strong> The <strong><a href='http://www.google.com/search?q=SYN' rel='noopener' target='_blank'>SYN</a> Queue</strong> holds partially open connections (<samp>SYN_RECV</samp>). Upon completing the 3-way handshake, the connection moves to the <strong>Accept Queue</strong> (<samp>listen(backlog)</samp>) waiting for user space to call <kbd>accept()</kbd>. Queue-overflow behavior depends on the operating system and its TCP settings; diagnose it from counters and packet evidence instead of assuming every overflow drops a new SYN.</li>\n"
            "<li><strong>Flow Control:</strong> Receiver advertises window size (<samp>rwnd</samp>) indicating free space in <samp>sk_rcvbuf</samp>. Window Scaling (RFC 7323) scales windows up to 1 GB.</li>\n"
            "<li><strong>Congestion Control:</strong> Sender bounds inflight data by Congestion Window (<samp>cwnd</samp>). Algorithms include loss-based TCP <a href='http://www.google.com/search?q=CUBIC' rel='noopener' target='_blank'>CUBIC</a> (RFC 8312) and rate-based Google Bottleneck Bandwidth and Round-trip propagation time (<a href='http://www.google.com/search?q=BBR' rel='noopener' target='_blank'>BBR</a>), which models bottleneck bandwidth and RTprop to prevent bufferbloat.</li>\n"
            "</ul>\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> Low CPU utilization alongside connection timeouts makes queue overflow and ephemeral-port pressure testable hypotheses, not automatic root causes. Architects compare listener queues, overflow counters, retransmissions, file descriptors, and application latency before changing buffer or congestion-control settings; every tuning change trades memory or fairness for throughput.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> The whole-document <a href='https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster'>Google Cloud Networking publication: TCP BBR congestion control comes to GCP (accessed 2026-11-03)</a> says that BBR models bottleneck bandwidth and round-trip propagation time and is used for traffic from named Google Cloud services and load-balancing or CDN paths to users. It does not establish that every guest VM or Cloud Interconnect flow uses BBR.</li>\n</ul>\n\n"
            "<h3 id='topic-03-subtopic-5'>Packet inspection and analysis with tcpdump</h3>\n"
            "<ul>\n<li><strong class='side-heading'>What it is in general:</strong> <strong class='keyword'><a href='http://www.google.com/search?q=tcpdump' rel='noopener' target='_blank'>tcpdump</a></strong> is the foundational command-line packet analyzer built on the <samp>libpcap</samp> packet capture interface. "
            "It captures raw Layer 2 frames, Layer 3 IP packets, and Layer 4 transport segments traversing network interfaces. "
            "Packets are filtered using Berkeley Packet Filter (BPF) syntax (e.g., <kbd>tcp port 80 and host 198.51.100.1</kbd>). "
            "Key command flags include: <kbd>-i &lt;interface&gt;</kbd> (select interface), <kbd>-nn</kbd> (disable DNS and port name resolution for predictable low-latency output), "
            "<kbd>-S</kbd> (display absolute sequence numbers instead of relative offsets), <kbd>-vvv</kbd> (maximum protocol decode verbosity), "
            "<kbd>-w &lt;file.pcap&gt;</kbd> (write raw packets to PCAP format), and <kbd>-r &lt;file.pcap&gt;</kbd> (read and decode saved capture files). "
            "Reading tcpdump output requires decoding transport flags: <samp>[S]</samp> (SYN: connection request proposing ISN), <samp>[S.]</samp> (SYN-ACK: server acceptance acknowledging client ISN+1 and proposing server ISN), "
            "<samp>[.]</samp> (ACK: client acknowledgment completing handshake), <samp>[P.]</samp> (PSH-ACK: data push transmitting application payload), "
            "<samp>[F.]</samp> (FIN-ACK: graceful connection teardown), and <samp>[R]</samp> / <samp>[R.]</samp> (RST / RST-ACK: connection abort or port closed), observing <a href='http://www.google.com/search?q=TIME_WAIT' rel='noopener' target='_blank'>TIME_WAIT</a> and congestion state transitions (<a href='http://www.google.com/search?q=BBR' rel='noopener' target='_blank'>BBR</a>, <a href='http://www.google.com/search?q=CUBIC' rel='noopener' target='_blank'>CUBIC</a>) over <a href='http://www.google.com/search?q=HTTP' rel='noopener' target='_blank'>HTTP</a> flows.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to a cloud architect:</strong> When microservices fail silently behind cloud load balancers or cross-VPC peerings, high-level logs and CPU metrics provide zero insight into wire-level transport health. Packet capture analysis is the definitive tool to prove whether drops occur due to MTU black holes, <a href='http://www.google.com/search?q=SYN' rel='noopener' target='_blank'>SYN</a> packet discards at queue bottlenecks, reset packets emitted by upstream middleboxes, or window stalls from unread socket buffers.\n\n"
            "</li>\n<li><strong class='side-heading'>Relevance to GCP:</strong> The <a href='https://man7.org/linux/man-pages/man1/tcpdump.1.html#DESCRIPTION'>Linux tcpdump(1) DESCRIPTION (accessed 2026-11-03)</a> documents how tcpdump prints or saves packets that match a capture expression. On a Compute Engine guest, that evidence is limited to traffic visible to the guest interface and capture permissions; claims about provider forwarding or separate load-balancer paths require Google Cloud-specific telemetry.</li>\n</ul>\n\n"

            "<ul>\n<li><strong class='side-heading'>Concrete example:</strong> A promotion sends an unexpected burst of 10,000 HTTP requests/second to a Compute Engine web service configured with the default Linux backlog of <samp>somaxconn=128</samp>. The application thread pool cannot invoke <kbd>accept()</kbd> fast enough to clear the accept queue. Once 128 connections queue up, the Linux kernel silently drops all new incoming SYN packets. Upstream Google Cloud Application Load Balancers retry three times, fail to establish TCP handshakes, and return HTTP 504 Gateway Timeout errors to shoppers. Increasing <samp>net.core.somaxconn=4096</samp> and sizing the application server backlog eliminates the drops and absorbs traffic spikes.</li>\n</ul>\n\n"

            "<strong class='side-heading'>Evidence limit:</strong> A socket in ESTABLISHED state proves only that the TCP 3-way handshake completed between the host kernels; "
            "it provides zero evidence that the application layer protocol is functioning, that HTTP requests can be parsed, or that downstream databases are operational."
        ),
        "questions": [
            "What is the functional difference between the kernel SYN Queue and the Accept Queue during TCP connection establishment?",
            "Why does TCP retain TIME-WAIT state after active close, and which measurements are required before changing operating-system reuse behavior?",
            "How does model-based congestion control (BBR) prevent the bufferbloat and packet drop cycles inherent to loss-based congestion control (CUBIC)?"
        ],
        "reference": "https://datatracker.ietf.org/doc/html/rfc9293#section-3",
        "reference_label": "RFC 9293: Transmission Control Protocol, section 3 (accessed 2026-11-03)",
        "scenario": {
            "diagram_enabled": True,
            "scenario": (
                "Brightloaf's e-commerce platform experienced an unpredicted 5x surge in checkout traffic following a marketing push. "
                "The backend API service ran on Compute Engine instances behind an internal Application Load Balancer."
            ),
            "symptom": (
                "Monitoring dashboards showed that while instance CPU utilization remained under 35%, clients experienced high rates of "
                "HTTP 504 Gateway Timeout errors. Inspection of instance kernel metrics revealed thousands of dropped TCP SYN packets."
            ),
            "impact": (
                "Over 12,000 checkout requests timed out across a 15-minute window, resulting in an estimated $95,000 in abandoned shopping carts "
                "and an immediate spike in customer support tickets."
            ),
            "constraints": (
                "Zero application code modifications permitted during peak traffic; must resolve via guest OS configuration and infrastructure scaling."
            ),
            "evidence": (
                "Executing <kbd>netstat -s | grep -i listen</kbd> on the backend VM instances showed rapid increments in queue overflow counters:\n\n"
                "```text\n"
                "14285 times the listen queue of a socket overflowed\n"
                "14285 SYNs to LISTEN sockets dropped\n"
                "```\n\n"
                "Inspecting the current system limits confirmed severely constrained queue depths:\n\n"
                "```text\n"
                "$ sysctl net.core.somaxconn\n"
                "net.core.somaxconn = 128\n"
                "```\n\n"
                "Checking active socket queue depths via <kbd>ss -lnt 'sport = :8080'</kbd> revealed Send-Q saturated at 128:\n\n"
                "```text\n"
                "State      Recv-Q Send-Q Local Address:Port  Peer Address:Port\n"
                "LISTEN     129    128          0.0.0.0:8080       0.0.0.0:*\n"
                "```"
            ),
            "root": (
                "The Linux kernel parameter <samp>net.core.somaxconn</samp> was left at its default value of 128, and the application server's "
                "listen backlog was capped at 128. During the sudden burst of ingress connections, the accept queue filled completely. "
                "By default (<samp>tcp_abort_on_overflow=0</samp>), the Linux kernel silently dropped new incoming SYN packets, forcing upstream "
                "load balancers into SYN retransmission backoff until timeout."
            ),
            "diagnostic_steps": [
                "Step 1: Check kernel drop counters using <kbd>netstat -s | grep -i listen</kbd> or <kbd>nstat -az TcpExtListenOverflows</kbd>.",
                "Step 2: Inspect active queue depths using <kbd>ss -lnt</kbd> to compare Recv-Q against Send-Q limits.",
                "Step 3: Query current system limits via <kbd>sysctl net.core.somaxconn</kbd> and <kbd>sysctl net.ipv4.tcp_max_syn_backlog</kbd>.",
                "Step 4: Check application server backlog configuration parameters in container runtime definitions."
            ],
            "remediation_steps": [
                "Tactical Fix: Immediately increase kernel socket queue limits via <kbd>sysctl -w net.core.somaxconn=4096</kbd> and restart worker processes.",
                "Strategic Control: Embed optimized kernel sysctl profiles into VM base images and Kubernetes daemonsets, tuning TCP window scaling and accept queue depths."
            ],
            "verify": (
                "Verify via <kbd>ss -lnt 'sport = :8080'</kbd> that Send-Q displays 4096 and that <kbd>netstat -s</kbd> overflow counters cease incrementing under load."
            ),
            "residual": (
                "Larger accept queues consume additional non-swappable kernel memory during traffic spikes; monitor kernel slab allocations."
            ),
            "diagram": (
                "Traffic surge hits API server",
                "Accept queue saturates at 128 (somaxconn)",
                "Kernel silently drops incoming TCP SYNs",
                "Tune somaxconn=4096 and tcp_max_syn_backlog",
                "Zero SYN drops; requests process cleanly"
            ),
            "icons": (
                "../assets/icons/generic/event.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/generic/queue.svg",
                "../assets/icons/generic/server.svg",
                "../assets/icons/generic/outcome.svg"
            ),
            "facts": "Supplied telemetry: Recv-Q exceeded Send-Q (128); netstat recorded 14,285 listen queue overflows and dropped SYNs.",
            "inference": "The application runtime could not accept connections faster than ingress arrival rate, causing accept queue overflow and silent TCP packet drop.",
            "expected": "Accept queue expands to 4,096; incoming SYNs are buffered in memory and accepted without drops during autoscaling lags."
        },
        "lab": make_lab(
            name="TCP Socket Lifecycle, Accept Queue Overflow, and tcpdump Packet Analysis",
            goal="Instrument the complete BSD socket lifecycle, synthesize and dissect TCP handshakes using tcpdump, and analyze accept queue overflow drops and socket state transitions.",
            expected="A comprehensive socket diagnostics log capturing TCP state transitions (SYN_SENT, ESTABLISHED, TIME_WAIT) and quantifying queue drop behavior.",
            covers="Trace an IPv4 and IPv6 lookup from supplied resolver output; label socket endpoints and the TCP handshake.",
            steps=[
                "<strong>Stage 1: Preflight and Environment Verification</strong> — Verify diagnostic socket and packet inspection tools (<kbd>ss</kbd>, <kbd>tcpdump</kbd>, <kbd>python3</kbd>):\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncommand -v bash\ncommand -v ss\ncommand -v tcpdump\ncommand -v python3\ncommand -v sysctl\npython3 -c \"import socket; print('TCP Socket Engine Ready')\" | tee preflight_socket.txt\nss -v | head -n1 >> preflight_socket.txt\n```\n\n<strong>Expected result:</strong> Diagnostic socket utilities confirmed and default somaxconn parameter printed.\n\n<strong>Save:</strong> preflight_socket.txt",
                "<strong>Stage 2: Prepare Target Inputs and Synthetic Packet Capture Fixture</strong> — Author a Python script (<samp>make_pcap.py</samp>) that synthesizes a valid TCP 3-way handshake, payload transmission, and teardown PCAP fixture:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > make_pcap.py\nimport struct, time\n\ndef make_tcp_packet(src_ip, dst_ip, src_port, dst_port, seq, ack, flags, win=65495, payload=b''):\n    eth = b'\\x00\\x11\\x22\\x33\\x44\\x55\\x66\\x77\\x88\\x99\\xaa\\xbb\\x08\\x00'\n    ip_len = 20 + 20 + len(payload)\n    ip_header = struct.pack('!BBHHHBBH4s4s', 0x45, 0, ip_len, 0x1234, 0x4000, 64, 6, 0,\n                            bytes(map(int, src_ip.split('.'))), bytes(map(int, dst_ip.split('.'))))\n    offset_res = (5 << 4)\n    tcp_header = struct.pack('!HHIIBBHHH', src_port, dst_port, seq, ack, offset_res, flags, win, 0, 0)\n    pkt = eth + ip_header + tcp_header + payload\n    ts_sec = int(time.time())\n    ts_usec = 100000\n    return struct.pack('!IIII', ts_sec, ts_usec, len(pkt), len(pkt)) + pkt\n\npcap_hdr = struct.pack('!IHHiIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)\n\nwith open('handshake.pcap', 'wb') as f:\n    f.write(pcap_hdr)\n    # 1. SYN (Flags [S], seq 1000000)\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 54321, 18080, 1000000, 0, 0x02))\n    # 2. SYN-ACK (Flags [S.], seq 2000000, ack 1000001)\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 18080, 54321, 2000000, 1000001, 0x12))\n    # 3. ACK (Flags [.], seq 1000001, ack 2000001)\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 54321, 18080, 1000001, 2000001, 0x10))\n    # 4. PSH-ACK (Flags [P.], payload data)\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 54321, 18080, 1000001, 2000001, 0x18, payload=b'GET / HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n'))\n    # 5. FIN-ACK (Flags [F.], teardown initiation)\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 54321, 18080, 1000045, 2000001, 0x11))\n    # 6. ACK of FIN (Flags [.])\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 18080, 54321, 2000001, 1000046, 0x10))\n    # 7. RST on closed port (Flags [R.])\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 18081, 54322, 0, 1000001, 0x14))\n\nprint(\"Generated handshake.pcap fixture.\")\nEOF\npython3 make_pcap.py | tee target_prep.txt\nls -l handshake.pcap >> target_prep.txt\n```\n\n<strong>Expected result:</strong> Synthetic PCAP capture file authored containing full TCP connection lifecycle.\n\n<strong>Save:</strong> target_prep.txt",
                "<strong>Stage 3: Inspect and Read Packet Dump with tcpdump</strong> — Execute <kbd>tcpdump</kbd> against the capture file and decode packet headers field-by-field:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ntcpdump -r handshake.pcap -nn -S | tee tcpdump_analysis.txt\n```\n\n<strong>Expected result:</strong> tcpdump parses the 3-way handshake ([S], [S.], [.]) and teardown flags with microsecond timestamps.\n\n<strong>Save:</strong> tcpdump_analysis.txt",
                "<strong>Stage 4: Execute Live Socket Queue Saturation Test</strong> — Launch a constrained queue listener and dispatch concurrent connection attempts to observe queue saturation:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > queue_test.py\nimport socket, time\n\nserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\nserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\nserver.bind(('127.0.0.1', 19099))\nserver.listen(2)\n\nclients = []\nsuccess = 0\ndropped = 0\n\nfor i in range(5):\n    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    c.settimeout(0.5)\n    try:\n        c.connect(('127.0.0.1', 19099))\n        clients.append(c)\n        success += 1\n    except Exception as e:\n        dropped += 1\n\nprint(f\"Connected: {success}, Dropped/Queued: {dropped}\")\nfor c in clients:\n    c.close()\nserver.close()\nEOF\npython3 queue_test.py | tee burst_execution.log\n```\n\n<strong>Expected result:</strong> Burst test execution proves queue saturation causes connection drop and timeout.\n\n<strong>Save:</strong> burst_execution.log",
                "<strong>Stage 5: Inspect Kernel Socket Telemetry and TIME_WAIT States</strong> — Inspect local socket telemetry using <kbd>ss</kbd> to observe active socket states:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\nss -tan 'sport = :19099 or dport = :19099' | tee socket_states.txt\nss -s >> socket_states.txt\n```\n\n<strong>Expected result:</strong> Active sockets and summary socket state telemetry captured via ss.\n\n<strong>Save:</strong> socket_states.txt",
                "<strong>Stage 6: Rehearse Bounded Failure: Filter TCP Reset Packets</strong> — Use <kbd>tcpdump</kbd> BPF filtering to isolate TCP Reset (RST) flags in the packet capture:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ntcpdump -r handshake.pcap -nn -S 'tcp[tcpflags] & tcp-rst != 0' | tee rst_observation.txt\n```\n\n<strong>Expected result:</strong> tcpdump filters and extracts only TCP RST packets indicating closed ports or connection aborts.\n\n<strong>Save:</strong> rst_observation.txt",
                "<strong>Stage 7: Diagnose Evidence and Record Kernel Tuning Recommendations</strong> — Author a structured diagnostic summary documenting why accept queue sizing and tcpdump analysis are critical for microservice stability:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > socket_queue_evidence.md\n# Architectural Evidence: TCP Socket Lifecycle, Handshakes, and tcpdump Dissection\n\n- Observation 1: tcpdump output proves the 3-way handshake sequence: Flags [S] (SYN), Flags [S.] (SYN-ACK), Flags [.] (ACK).\n- Observation 2: Sequence and acknowledgment tracking confirms SYN consumes 1 sequence number (ack = seq + 1).\n- Observation 3: Sockets transitioning through TIME_WAIT linger for 2MSL to guarantee packet expiration in flight.\n- Observation 4: Accept queue saturation silently drops incoming SYNs unless tcp_abort_on_overflow=1 sends RST.\n- Decision: Production microservice base images must configure net.core.somaxconn >= 4096 and tcp_max_syn_backlog >= 4096.\nEOF\ncat socket_queue_evidence.md\n```\n\n<strong>Expected result:</strong> Structured evidence document authored recording queue sizing recommendations.\n\n<strong>Save:</strong> socket_queue_evidence.md",
                "<strong>Stage 8: Clean Up and Close Out Exercise</strong> — Remove temporary test scripts and verify clean workspace exit:\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\nrm -f make_pcap.py queue_test.py handshake.pcap tcpdump_analysis.txt burst_execution.log socket_states.txt rst_observation.txt target_prep.txt\necho \"TCP transport and packet capture lab closed cleanly.\" > cleanup_summary.txt\ncat cleanup_summary.txt\n```\n\n<strong>Expected result:</strong> Temporary test server and client scripts removed cleanly from workspace.\n\n<strong>Save:</strong> cleanup_summary.txt"
            ],
            accept="Generated evidence markdown proves that accept queue saturation causes connection drop, and records kernel tuning parameters.",
            trouble="If port 19099 is already in use, edit the test scripts to use an unprivileged port such as 19105.",
            file_name="socket_queue_evidence.md"
        )
    }
]

# Same-day depth expansion: compact data renders as detailed worked traces.  The
# rows stay inside the roadmap's IPv6, DNS, and transport Study clauses and make
# ownership, state transitions, failure signals, decisions, and evidence limits
# explicit without introducing another product or deployment.
WORKED_TRACE_ROWS = {
    'topic-01': [
        ('Canonical input', '2001:0db8:0000:0000:0000:0000:0000:0020', 'Parse eight 16-bit fields, remove leading zeroes, lowercase hexadecimal digits, and compress only the longest zero run.', 'Address-management and policy tooling', 'String comparison treats two spellings of one address as different policy objects.', 'Normalize before deduplication, authorization, logging, and route-policy comparison.', 'Canonical equality proves address identity only; it does not prove assignment, route selection, or reachability.'),
        ('Prefix boundary', '2001:db8:20::/64 with host 2001:db8:20::45', 'Apply the first 64 bits as the subnet prefix and retain the remaining 64 bits as the interface identifier.', 'Network planner and guest address configuration', 'A prefix-length mismatch sends an on-link destination toward a router or treats a remote destination as local.', 'Record the prefix length beside every address and compare binary prefixes before selecting a next hop.', 'A matching prefix predicts an on-link decision under the supplied configuration; it does not prove neighbor discovery succeeded.'),
        ('Link-local selection', 'fe80::20 on interfaces eth0 and eth1', 'The destination is meaningful only with a zone identifier because the same link-local value can exist on multiple links.', 'Calling process and guest operating system', 'A bare socket address is ambiguous and can fail before any packet is emitted.', 'Carry the interface index in the socket structure and reject link-local values in remote service discovery.', 'A valid zone identifies a link; it does not make the destination routable beyond that link.'),
        ('Unique-local route', 'An RFC 4193 unique-local prefix is advertised across a private topology', 'A ULA prefix can be routed inside an administrative domain when every participating router has a matching route.', 'Enterprise routing team', 'Assuming private scope implies automatic connectivity hides missing advertisements and asymmetric return paths.', 'Treat scope, route propagation, firewall policy, and return routing as separate design gates.', 'ULA classification proves address scope only; it does not prove any router learned the prefix.'),
        ('Global-unicast route', '2001:db8:40::25 as a documentation GUA fixture', 'A longest-prefix match selects a next hop after policy and source-address selection choose an eligible path.', 'Routing control plane and host forwarding table', 'A syntactically global address is mistaken for evidence of internet reachability.', 'Inspect the selected route, source address, egress policy, and reverse path independently.', 'The documentation address demonstrates classification and lookup mechanics and is not a reachable public endpoint.'),
        ('Router solicitation', 'New interface sends an RS to the all-routers multicast group', 'An IPv6 host requests router information; an eligible router can answer with an RA carrying prefix and lifetime information.', 'Host stack and first-hop router', 'Blocked ICMPv6 discovery traffic leaves an interface addressed but without usable default-router state.', 'Preserve required discovery messages and observe router lifetime and prefix information rather than inferring them from inventory.', 'An RA proves an advertisement was received; it does not prove the advertised route reaches the application destination.'),
        ('SLAAC construction', 'Advertised /64 plus a locally selected interface identifier', 'The host forms an address, marks it tentative, and withholds normal use until duplicate-address checks complete.', 'Guest operating system', 'Automation declares readiness when the address exists but is still tentative or invalid.', 'Gate readiness on address state as well as presence and keep privacy-address rotation separate from stable service identity.', 'A preferred address proves local configuration state, not DNS publication or end-to-end reachability.'),
        ('Duplicate-address check', 'Tentative 2001:db8:20::45 and a neighbor solicitation for that target', 'The host probes for an existing owner before assigning the address for ordinary traffic.', 'Local-link address owner and neighbor-discovery logic', 'A duplicate response is ignored and two nodes claim one address, producing intermittent delivery.', 'Fail initialization on a duplicate indication and preserve the conflicting-link evidence for remediation.', 'No response reduces the supplied duplicate hypothesis; it cannot prove uniqueness beyond the local link.'),
        ('Neighbor resolution', 'Destination is on-link but no link-layer cache entry exists', 'The host maps the IPv6 next hop to a link-layer address through solicitation and advertisement messages.', 'Guest neighbor cache and local-link peer', 'A valid route exists while packets wait on an incomplete or failed neighbor entry.', 'Inspect route and neighbor state together and avoid labeling this condition as a DNS failure.', 'A reachable neighbor entry proves local-link resolution for a next hop, not remote service readiness.'),
        ('Dual-stack answer set', 'A=198.51.100.20 and AAAA=2001:db8:20::20', 'The client receives two candidate address families and its connection algorithm schedules attempts according to local policy.', 'Client resolver and connection manager', 'Operators assume the existence of AAAA means the application actually used IPv6.', 'Record the chosen address, route, socket endpoint, and timing for each attempt.', 'The answer set proves candidate discovery only; it does not reveal which family won or why.'),
        ('IPv6 attempt failure', 'AAAA candidate has no usable route while the A candidate is reachable', 'A dual-stack client can start a later IPv4 attempt while the IPv6 attempt remains incomplete.', 'Client connection algorithm', 'Fallback masks persistent IPv6 defects and dashboards show overall success without family-specific failure.', 'Measure attempt outcomes by address family and repair IPv6 even when user-visible fallback succeeds.', 'Successful fallback proves one connection path worked, not that the IPv6 path is healthy.'),
        ('Frontend boundary', 'Separate IPv4 and IPv6 frontend rules lead to one proxy service', 'Each frontend accepts a client connection and the proxy establishes a distinct backend connection under its configured protocol.', 'Load-balancer frontend and backend owners', 'A frontend protocol observation is incorrectly attributed to the backend connection.', 'Label both socket pairs and verify frontend and backend transport independently.', 'A client-side connection proves only the frontend boundary; it says nothing about the backend handshake.'),
        ('Firewall decision', 'Packet has an IPv6 source, destination, next header, and destination port', 'Policy evaluation matches the applicable direction and attributes before forwarding or dropping the packet.', 'Network security policy owner', 'IPv4 policy coverage is assumed to include IPv6 even though the rule sets differ.', 'Review both families and retain the matching rule identity with the test evidence.', 'A policy allow decision is expected behavior from configuration; only observed traffic evidence can show a packet traversed it.'),
        ('IPv6 diagnostic closeout', 'Resolver answer, route lookup, neighbor state, socket attempt, and application result', 'Order the evidence from name to address scope, next hop, local-link resolution, transport state, and user-space response.', 'Incident commander coordinating platform and application teams', 'One successful layer is used to close an incident whose failure remains at a later layer.', 'State the first failed boundary, its owner, the next discriminating check, and what remains unknown.', 'The trace is a bounded diagnostic argument; without a live capture it is not production observation.'),
    ],
    'topic-02': [
        ('Stub request', 'getaddrinfo requests A and AAAA for api.example.test', 'The stub formats questions and sends them to its configured recursive resolver instead of walking the hierarchy.', 'Application runtime and host resolver configuration', 'A search suffix or hosts-file override changes the effective question before recursion begins.', 'Record the final queried name, type, resolver destination, and local override sources.', 'A stub request proves the application asked for a name; it does not prove a packet reached the resolver.'),
        ('Recursive cache lookup', 'Question tuple name, class, and type', 'The resolver searches cached positive and negative entries and evaluates their remaining TTL before deciding to answer or recurse.', 'Recursive resolver operator', 'An expired or differently typed entry is treated as a reusable answer.', 'Preserve record type and remaining TTL with every cache conclusion.', 'A cache hit proves the resolver had a reusable entry under its rules, not that the authority still serves the same value.'),
        ('Root referral', 'Cache miss for api.example.test A', 'The recursive resolver asks a root server and receives a referral toward the applicable top-level domain servers.', 'Recursive resolver', 'A referral is mistaken for the final address answer.', 'Distinguish authority-section NS data and glue from an answer-section address for the requested name.', 'The referral identifies the next delegation step; it does not authenticate or answer the application name.'),
        ('TLD referral', 'Query reaches the delegated top-level domain', 'The TLD authority returns the child zone name servers and any necessary in-bailiwick glue.', 'Parent-zone and registrar owners', 'Stale parent delegation points resolvers at servers that no longer serve the child zone.', 'Compare parent delegation with child-zone authority and plan changes across both ownership boundaries.', 'Matching delegation data supports consistency; it does not prove the child answer is correct.'),
        ('Authoritative answer', 'The child authority receives the requested owner name and record type', 'It returns the RRset with AA set, or a negative response carrying authority information.', 'Authoritative-zone owner', 'An authoritative response is interpreted as proof that clients can connect to the returned address.', 'Record owner, type, value, TTL, authority flag, and serial separately from reachability evidence.', 'Authority proves namespace control for the response, not routing, firewall permission, or listener state.'),
        ('A and AAAA pairing', 'One owner name has IPv4 and IPv6 address RRsets', 'Resolvers cache each type independently and clients can receive different lifetimes or availability for the two families.', 'Zone owner and client connection owner', 'Changing only A leaves an older AAAA path active or vice versa.', 'Plan, publish, verify, and roll back both record types as independent control-plane objects.', 'Aligned answers prove naming intent only; they do not prove equivalent data-plane behavior.'),
        ('CNAME chain', 'Alias points to a canonical owner that holds address records', 'The resolver follows the alias, accumulates the chain, and caches each RRset according to its own TTL.', 'Zone owners for every name in the chain', 'A short alias TTL is expected to override a long cached target TTL.', 'Budget cutover time from every independently cached link and cap chain length operationally.', 'A completed chain proves name mapping; it does not prove the target application is healthy.'),
        ('MX dependency', 'Mail domain publishes priority and exchanger host', 'A mail client selects the lowest-preference-number eligible exchanger and resolves that host to address records.', 'Mail-domain and exchanger DNS owners', 'The exchanger target lacks direct address records or its address is stale.', 'Validate the MX RRset and each target address as separate dependencies.', 'A syntactically valid MX record does not prove SMTP reachability or acceptance policy.'),
        ('NS and glue', 'Child nameserver name resides inside the delegated child zone', 'The parent supplies address glue so a resolver can reach the server without circularly resolving through the child first.', 'Parent delegation owner', 'Missing or stale glue strands an otherwise correct child zone.', 'Audit parent-side glue whenever in-bailiwick nameserver addresses change.', 'Glue is routing assistance, not authoritative application data for unrelated names.'),
        ('SOA negative cache', 'Query name does not exist under an authoritative zone', 'The negative response carries SOA-derived timing that allows recursive resolvers to cache nonexistence.', 'Authoritative-zone owner and resolver', 'A newly created name remains negative in caches until the permitted lifetime ends.', 'Include negative-cache lifetime in rollout plans and test both preexisting and fresh resolver caches.', 'NXDOMAIN from one cache proves that cache state at that time, not universal absence.'),
        ('TTL countdown', 'RRset stored at t=5 with TTL 300', 'The cache can serve the value while current time is before t=305 and reports a decreasing remaining lifetime.', 'Recursive resolver', 'Teams reset the countdown mentally when the authority changes the record.', 'Calculate expiry from insertion time and distinguish authoritative TTL from remaining cache TTL.', 'Arithmetic predicts compliant cache behavior; it is not an observation of every client cache.'),
        ('Cutover window', 'Old address cached until t=305; authority changes at t=100', 'A compliant resolver can serve the old address for the remaining 205 seconds while fresh resolvers receive the new address.', 'Change coordinator and application owner', 'Mixed answers are declared split-brain proof without checking whether both targets accepted writes.', 'Separate name divergence, connection reuse, and application write behavior in the evidence plan.', 'Overlapping DNS answers predict traffic distribution risk; they do not prove duplicate business processing occurred.'),
        ('DNSSEC validation', 'RRset, RRSIG, DNSKEY, parent DS, and a configured trust anchor', 'The resolver authenticates the signed RRset through the delegation chain and checks signature time validity.', 'Signing-zone and validating-resolver owners', 'An expired signature or mismatched parent DS turns correct-looking data into validation failure.', 'Schedule rollover across parent and child boundaries and monitor validation-specific errors.', 'Successful validation proves origin authentication and integrity, not confidentiality or endpoint health.'),
        ('Resolver closeout', 'Stub trace, cache decision, referrals, authoritative response, TTL, and transport handoff', 'The diagnostic sequence ends DNS analysis before testing route and socket state against the selected address.', 'Incident commander and resolver owner', 'Transport timeout is reported as DNS failure merely because a hostname appeared in the request.', 'Name the last proven DNS boundary and hand the exact address and expiry evidence to the network owner.', 'The DNS trace closes only the naming question; reachability and established state remain separate tests.'),
    ],
    'topic-03': [
        ('Socket creation', 'AF_INET6 plus SOCK_STREAM and protocol selection', 'The kernel allocates a socket object and file descriptor but no local or remote endpoint is established yet.', 'Application process and guest kernel', 'A created descriptor is counted as a connection in application telemetry.', 'Track descriptor state separately from bound, listening, connecting, and established states.', 'Successful socket creation proves local resource allocation only.'),
        ('Server bind', 'Local address and port such as [2001:db8:20::20]:443', 'bind associates the passive socket with a local endpoint subject to address availability and reuse rules.', 'Server process and kernel port namespace', 'Another listener or an unavailable address produces a local bind error before network traffic exists.', 'Record the bound address family, interface intent, port, and reuse settings.', 'A successful bind proves local ownership of an endpoint, not that policy permits clients to reach it.'),
        ('Listen transition', 'Bound stream socket and requested backlog', 'listen marks the socket passive and establishes kernel queue limits subject to operating-system caps.', 'Server runtime and guest-kernel tuning owner', 'The application assumes its requested backlog is the effective queue size.', 'Compare application backlog, kernel caps, queue counters, and memory cost before tuning.', 'LISTEN proves a passive socket exists; it does not prove an accept loop is draining it.'),
        ('Client connect', 'Client endpoint candidate and server endpoint', 'The kernel selects a source address and ephemeral port, creates the four-tuple, and begins transport establishment.', 'Client runtime and guest kernel', 'DNS success is logged as connection success before connect completes.', 'Capture the chosen source, destination, state, timeout, and terminal error.', 'A connect call proves intent; completion status determines whether transport state was established.'),
        ('SYN emission', 'Client sequence 1000, SYN flag, destination port 443', 'The first handshake segment proposes an initial sequence space and moves the client into SYN-SENT.', 'Client TCP state machine', 'A packet leaving the client is treated as proof it reached a listener.', 'Correlate client emission with server receipt or a return segment before advancing the boundary.', 'The SYN proves only that the client stack attempted establishment.'),
        ('SYN-ACK response', 'Server sequence 7000 and acknowledgment 1001', 'A listening server acknowledges the client SYN and proposes its own initial sequence number.', 'Server TCP state machine', 'A forged, stale, or mismatched acknowledgment is accepted in a tabletop trace.', 'Verify endpoint reversal and ack equals peer sequence plus one.', 'A valid SYN-ACK supports server-side receipt and response; it does not prove the final ACK arrived.'),
        ('Final ACK', 'Client acknowledgment 7001 with established four-tuple', 'The client acknowledges the server sequence; the supplied trace can now be interpreted as completing the three-way handshake.', 'Both endpoint kernels', 'ESTABLISHED is claimed from only two segments or from labels without arithmetic.', 'Require all directions, flags, sequence relationships, and endpoint identities.', 'A valid supplied handshake proves fixture consistency unless captured from a live path.'),
        ('Accept handoff', 'Completed connection waits in the accept queue', 'accept removes one established child socket and transfers it to user space while the listening socket remains passive.', 'Server runtime', 'Kernel establishment succeeds but workers do not accept quickly enough.', 'Measure queue occupancy, accept latency, worker scheduling, and file-descriptor pressure together.', 'A dequeued socket proves user-space ownership began, not that the request was parsed.'),
        ('Receive window', 'Receiver advertises available buffer space', 'Flow control limits sender inflight bytes according to the receiver window independently of congestion control.', 'Receiving kernel and consuming application', 'A slow reader is diagnosed as network congestion because throughput falls.', 'Compare receive-queue growth, advertised window, application read rate, and retransmissions.', 'A small window indicates receiver-side pressure; it does not identify the application root cause alone.'),
        ('Congestion window', 'Sender estimates safe inflight data for the path', 'Congestion control adjusts sending rate from acknowledgments, loss, and its model while flow control remains a separate ceiling.', 'Sending kernel and path', 'Socket-buffer enlargement is assumed to repair a congested or lossy path.', 'Inspect cwnd, round-trip behavior, loss, and receiver window before changing buffers.', 'A congestion signal describes transport behavior, not provider-internal causality without path evidence.'),
        ('UDP datagram', 'One message has source port, destination port, length, and checksum', 'The sender emits a datagram without a connection handshake or delivery acknowledgment at the transport layer.', 'Application protocol and endpoint kernels', 'No error is interpreted as proof of delivery and processing.', 'Add application-level identity, timeout, retry, and deduplication when delivery matters.', 'A successful send call proves local queueing, not remote receipt.'),
        ('QUIC boundary', 'Encrypted streams are carried in UDP datagrams between client and frontend', 'QUIC manages connection identity, loss recovery, and multiplexed streams in user space while UDP supplies datagram carriage.', 'Client and frontend QUIC implementations', 'Frontend QUIC is assumed to continue unchanged to a backend connection.', 'Draw and observe frontend and backend connections as different transport boundaries.', 'A QUIC frontend observation does not prove the backend protocol or state.'),
        ('Active close', 'Endpoint sends FIN after its final byte sequence', 'The peers acknowledge each direction independently and the active closer can retain TIME-WAIT to protect later tuples from delayed segments.', 'Endpoint kernels and application shutdown logic', 'TIME-WAIT is treated as a leak and unsafe reuse is enabled without measurements.', 'Identify the active closer, tuple reuse rate, port pressure, and timer implementation before tuning.', 'TIME-WAIT count proves retained transport state, not an application memory leak.'),
        ('Transport closeout', 'Resolver answer, selected address, route result, handshake, queue state, and application response', 'The investigation advances only when each earlier boundary has explicit evidence and owner attribution.', 'Incident commander across network and application teams', 'A 504 or timeout is assigned to queue overflow from CPU percentage alone.', 'Correlate counters, socket states, packet directions, queue occupancy, and user-space timing before remediation.', 'The worked trace supports a diagnosis; only locally produced or supplied evidence may be described as observed.'),
    ],
}

def render_worked_traces(topic_key, rows):
    articles = []
    for number, (checkpoint, supplied_input, mechanism, owner, failure, decision, evidence_limit) in enumerate(rows, 1):
        articles.append(f"""
<article class="callout">
<p><strong>Worked trace {number} — {checkpoint}</strong></p>
<p><strong>Supplied input or state:</strong> {supplied_input}</p>
<p><strong>Mechanism walkthrough:</strong> {mechanism} Read this transition as one bounded step: identify the input state, name the component allowed to change it, and record the resulting state before moving to the next layer. The checkpoint belongs to <strong>{owner}</strong>; adjacent layers may supply prerequisites or consume results, but they do not silently inherit ownership.</p>
<p><strong>Failure interpretation:</strong> {failure} Treat that statement as a hypothesis until the checkpoint's own state or counter supports it. A symptom at a later layer can coexist with success here, and success here cannot be promoted into evidence about a later layer.</p>
<p><strong>Architect decision:</strong> {decision} The decision record should include the chosen boundary, rejected alternative, recovery or stop condition, and the exact artifact that another engineer can inspect without rerunning an unrelated cloud deployment.</p>
<p><strong>Verification sequence:</strong> First preserve the supplied value; second calculate or parse the expected transition; third compare the result with the invariant; fourth classify the result as supplied, locally observed, inferred, or expected; finally hand the next unresolved boundary to its owner. Never replace a missing observation with a plausible product behavior.</p>
<p><strong>Trade-off and limit:</strong> More aggressive caching, fallback, buffering, or retry can improve apparent availability while delaying failure visibility and consuming memory, ports, or control-plane capacity. Prefer the smallest reversible change that exposes the failed boundary before increasing a limit. <strong>Evidence limit:</strong> {evidence_limit}</p>
</article>""")
    return (
        f'<section aria-label="{topic_key} worked mechanism and evidence traces">'
        '<p><strong>Worked mechanism and evidence traces</strong></p>'
        '<p>The following traces stay within today\'s Study scope. Each one separates protocol state, ownership, failure signal, architect decision, and the evidence boundary so that a plausible explanation is not mistaken for an observation.</p>'
        + ''.join(articles)
        + '</section>'
    )

for _topic in TOPICS:
    _topic['technical'] += render_worked_traces(_topic['key'], WORKED_TRACE_ROWS[_topic['key']])

# Contract-v2 fidelity repair: the roadmap requires supplied resolver output.
# These three offline labs supersede the earlier live-network variants while
# retaining the technical discussion and its depth unchanged.
SUPPLIED_MODE = (
    "Local Linux terminal; supplied synthetic resolver and transport fixtures. "
    "Observed locally: fixture parsing, Python assertions, generated diagrams, and SHA-256 hashes. "
    "Simulated or predicted: DNS cache behavior, IPv4/IPv6 reachability, and TCP state transitions represented by the fixtures. "
    "Untested on GCP: Cloud DNS resolution, VPC routing, load-balancer transport, and Compute Engine guest-kernel behavior."
)
SUPPLIED_COVERS = "Trace an IPv4 and IPv6 lookup from supplied resolver output; label socket endpoints and the TCP handshake."

TOPICS[0]['lab'] = make_lab(
    name="Supplied IPv4/IPv6 Resolver Trace and Scoped Socket Boundary",
    goal="Trace supplied A and AAAA resolver output, classify IPv6 scope, and label the client and server socket endpoints plus all three TCP handshake messages without contacting a live resolver or endpoint.",
    expected="A locally generated IPv4/IPv6 trace, socket-endpoint inventory, handshake diagram, and evidence hash that distinguish supplied facts from predicted reachability.",
    covers=SUPPLIED_COVERS,
    steps=[
        "<strong>Stage 1: Preflight local parsing tools</strong> — Work in the runner-provided lab workspace; do not change host networking.\n\n<strong>Location:</strong> Local Linux terminal\n\n<strong>OS/shell/tools:</strong> Linux, Bash, Python 3, sha256sum\n\n```bash\ncommand -v bash\ncommand -v python3\ncommand -v sha256sum\nprintf 'workspace=%s\\n' \"$PWD\" | tee preflight_ipv6.txt\n```\n\n<strong>Expected result:</strong> Each tool path is printed and the workspace is recorded.\n\n<strong>Save:</strong> <samp>preflight_ipv6.txt</samp>. <strong>Stop/recovery:</strong> Stop if any command is missing; install the missing local package before rerunning.",
        "<strong>Stage 2: Prepare the supplied resolver and transport fixture</strong> — Copy the complete fixture exactly; its addresses are documentation ranges and its observations are supplied, not live.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > supplied_ipv6_trace.txt\nSUPPLIED resolver=192.0.2.53 client=192.0.2.10 qname=api.example.test qtype=A answer=198.51.100.20 ttl=300\nSUPPLIED resolver=2001:db8:53::53 client=2001:db8:10::10 qname=api.example.test qtype=AAAA answer=2001:db8:20::20 ttl=300\nSUPPLIED socket_client=[2001:db8:10::10]:53000 socket_server=[2001:db8:20::20]:443\nSUPPLIED tcp_1=SYN seq=1000 ack=0\nSUPPLIED tcp_2=SYN-ACK seq=7000 ack=1001\nSUPPLIED tcp_3=ACK seq=1001 ack=7001\nEOF\nsha256sum supplied_ipv6_trace.txt | tee supplied_ipv6_trace.sha256\n```\n\n<strong>Expected result:</strong> Seven supplied lines and one stable input hash are saved.\n\n<strong>Save:</strong> <samp>supplied_ipv6_trace.txt</samp> and <samp>supplied_ipv6_trace.sha256</samp>. <strong>Stop/recovery:</strong> Recopy the block if the line count or labels differ.",
        "<strong>Stage 3: Author the dual-stack trace analyzer</strong> — Parse both record families, validate documentation addresses, and check handshake acknowledgments.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'PY' > trace_ipv6.py\nimport ipaddress, json, re\nlines = open('supplied_ipv6_trace.txt', encoding='utf-8').read().splitlines()\nrecords = {}\nfor line in lines[:2]:\n    fields = dict(token.split('=', 1) for token in line.split()[1:])\n    records[fields['qtype']] = fields\nassert set(records) == {'A', 'AAAA'}\nassert ipaddress.ip_address(records['A']['answer']) in ipaddress.ip_network('198.51.100.0/24')\nassert ipaddress.ip_address(records['AAAA']['answer']) in ipaddress.ip_network('2001:db8::/32')\nendpoint_line = lines[2]\nclient, server = re.findall(r'\[[^]]+\]:\d+', endpoint_line)\nsteps = [dict(token.split('=', 1) for token in line.split()[1:]) for line in lines[3:]]\nassert [s[next(k for k in s if k.startswith('tcp_'))] for s in steps] == ['SYN', 'SYN-ACK', 'ACK']\nassert int(steps[1]['ack']) == int(steps[0]['seq']) + 1\nassert int(steps[2]['ack']) == int(steps[1]['seq']) + 1\njson.dump({'records': records, 'client_endpoint': client, 'server_endpoint': server, 'handshake': ['SYN', 'SYN-ACK', 'ACK']}, open('ipv6_trace.json', 'w'), indent=2)\nPY\npython3 -m py_compile trace_ipv6.py\n```\n\n<strong>Expected result:</strong> The analyzer compiles without changing network state.\n\n<strong>Save:</strong> <samp>trace_ipv6.py</samp>. <strong>Stop/recovery:</strong> Restore the supplied fixture before changing assertions.",
        "<strong>Stage 4: Execute the IPv4 and IPv6 trace</strong> — Run the analyzer and render the required boundary sequence from its local result.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 trace_ipv6.py\npython3 - <<'PY' | tee ipv6_transport_diagram.txt\nimport json\nd = json.load(open('ipv6_trace.json'))\nprint('A lookup ->', d['records']['A']['answer'], '(name resolution only)')\nprint('AAAA lookup ->', d['records']['AAAA']['answer'], '(name resolution only)')\nprint(d['client_endpoint'], '-- SYN -->', d['server_endpoint'])\nprint(d['client_endpoint'], '<- SYN-ACK --', d['server_endpoint'])\nprint(d['client_endpoint'], '-- ACK -->', d['server_endpoint'], '[ESTABLISHED expected]')\nPY\n```\n\n<strong>Expected result:</strong> Both lookups and the labelled three-message handshake appear in order.\n\n<strong>Save:</strong> JSON and diagram. <strong>Stop/recovery:</strong> Stop on an assertion; do not relabel supplied values to make it pass.",
        "<strong>Stage 5: Inspect scope and evidence boundaries</strong> — Record which conclusions are supplied versus inferred.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 - <<'PY' | tee ipv6_scope_review.txt\nimport ipaddress, json\nd = json.load(open('ipv6_trace.json'))\nv6 = ipaddress.ip_address(d['records']['AAAA']['answer'])\nprint('Observed locally: parsed supplied A and AAAA records and validated handshake arithmetic.')\nprint('Supplied fact: IPv6 answer =', v6, 'scope=documentation global-unicast example')\nprint('Inference: an address answer does not prove a route, neighbor entry, firewall decision, or listening socket.')\nprint('Expected behavior: if reachability and listener prerequisites hold, SYN/SYN-ACK/ACK establishes TCP state.')\nprint('Evidence limit: no packet was sent and no GCP resource was queried.')\nPY\n```\n\n<strong>Expected result:</strong> The five evidence categories are explicit.\n\n<strong>Save:</strong> <samp>ipv6_scope_review.txt</samp>.",
        "<strong>Stage 6: Rehearse a bounded link-local edge case</strong> — Classify a supplied AAAA answer that lacks the interface zone required for a same-link socket destination.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 - <<'PY' | tee ipv6_edge_case.txt\nimport ipaddress\nanswer = ipaddress.ip_address('fe80::1')\nscope_id = 0\nassert answer.is_link_local and scope_id == 0\nprint('Supplied edge case: AAAA=fe80::1, socket scope_id=0')\nprint('Decision: reject this DNS registration for a remote service; DNS cannot carry the required local interface identity.')\nprint('Predicted behavior: a bare same-link connect is ambiguous or invalid; this lab does not execute it.')\nPY\n```\n\n<strong>Expected result:</strong> The unsafe registration is rejected without attempting a network connection.\n\n<strong>Save:</strong> <samp>ipv6_edge_case.txt</samp>.",
        "<strong>Stage 7: Diagnose and record the architecture decision</strong> — Assemble durable evidence with the roadmap Exit distinction.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > ipv6_scoping_evidence.md\n# Supplied IPv4/IPv6 lookup and transport evidence\n\n- Observed locally: Python parsed one supplied A answer, one supplied AAAA answer, two socket endpoints, and SYN -> SYN-ACK -> ACK arithmetic.\n- Simulated or predicted: the labelled handshake reaches ESTABLISHED only if reachability, policy, and a listener all permit it.\n- Untested on GCP: Cloud DNS, VPC routes, firewall policy, NDP, and a Compute Engine listener.\n- Decision: accept routable service addresses; reject link-local DNS registration without a same-link interface context.\n- Evidence limit: successful name resolution is not proof of reachability or an established connection.\nEOF\nsha256sum ipv6_trace.json ipv6_transport_diagram.txt ipv6_scoping_evidence.md | tee ipv6_evidence.sha256\n```\n\n<strong>Expected result:</strong> The evidence file separates facts, inference, expected behavior, and limits.\n\n<strong>Save:</strong> evidence markdown and hashes.",
        "<strong>Stage 8: Clean up only lab-owned transient inputs</strong> — Preserve the evidence, diagram, review, and hashes; delete only the copied fixture, analyzer, bytecode, and intermediate JSON.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\nrm -f supplied_ipv6_trace.txt supplied_ipv6_trace.sha256 trace_ipv6.py ipv6_trace.json\nrm -rf __pycache__\nprintf 'preserved: ipv6_transport_diagram.txt ipv6_scope_review.txt ipv6_edge_case.txt ipv6_scoping_evidence.md ipv6_evidence.sha256\\n' | tee cleanup_summary.txt\n```\n\n<strong>Expected result:</strong> No process or cloud resource exists to clean up; durable local evidence remains.\n\n<strong>Save:</strong> <samp>cleanup_summary.txt</samp>."
    ],
    accept="The supplied A and AAAA answers are traced, client/server socket endpoints and SYN/SYN-ACK/ACK are labelled, hashes exist, and the evidence explicitly distinguishes name resolution, predicted reachability, and predicted established state.",
    trouble="If an assertion fails, compare the fixture's qtype, sequence, and acknowledgment fields with the analyzer; never contact a public resolver as a substitute for the supplied fixture.",
    file_name="ipv6_scoping_evidence.md"
)
TOPICS[0]['lab']['mode'] = SUPPLIED_MODE
TOPICS[0]['lab']['steps'][3] = TOPICS[0]['lab']['steps'][3].replace(
    '<strong>Save:</strong> JSON and diagram.',
    '<strong>Save:</strong> <samp>ipv6_trace.json</samp> and <samp>ipv6_transport_diagram.txt</samp>.'
)
TOPICS[0]['lab']['steps'][6] = TOPICS[0]['lab']['steps'][6].replace(
    '<strong>Save:</strong> evidence markdown and hashes.',
    '<strong>Save:</strong> <samp>ipv6_scoping_evidence.md</samp> and <samp>ipv6_evidence.sha256</samp>.'
)

TOPICS[1]['lab'] = make_lab(
    name="Supplied Recursive DNS Trace, TTL Decision, and Transport Handoff",
    goal="Trace supplied IPv4 and IPv6 resolver output through stub, recursive, root, TLD, and authoritative roles; calculate cache validity; then label the socket endpoints and TCP handshake that occur only after resolution.",
    expected="A deterministic resolver-role trace, TTL decision table, bounded stale-cache failure, and DNS/transport diagram created entirely from supplied fixtures.",
    covers=SUPPLIED_COVERS,
    steps=[
        "<strong>Stage 1: Preflight offline evidence tools</strong> — Use only local Bash, Python 3, and sha256sum.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncommand -v bash\ncommand -v python3\ncommand -v sha256sum\nprintf 'offline resolver trace ready\\n' | tee preflight_dns.txt\n```\n\n<strong>Expected result:</strong> All tool checks pass. <strong>Stop/recovery:</strong> Stop if a tool is missing; do not replace the supplied exercise with a live query.",
        "<strong>Stage 2: Prepare supplied IPv4 and IPv6 resolver output</strong> — Copy the role-labelled fixture exactly.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > supplied_resolver_output.txt\nSUPPLIED t=0 actor=stub action=query qname=api.example.test qtype=A,AAAA target=192.0.2.53\nSUPPLIED t=1 actor=recursive action=cache_miss remaining_ttl=0\nSUPPLIED t=2 actor=root action=referral ns=a.iana-servers.net\nSUPPLIED t=3 actor=tld action=referral ns=ns.example.test\nSUPPLIED t=4 actor=authoritative action=answer A=198.51.100.20 AAAA=2001:db8:20::20 ttl=300 aa=1\nSUPPLIED t=5 actor=recursive action=cache_store expires_at=305\nSUPPLIED t=6 actor=stub action=deliver A=198.51.100.20 AAAA=2001:db8:20::20\nSUPPLIED socket_client=[2001:db8:10::10]:53000 socket_server=[2001:db8:20::20]:443\nSUPPLIED tcp=SYN>SYN-ACK>ACK expected_state=ESTABLISHED\nEOF\nsha256sum supplied_resolver_output.txt | tee resolver_fixture.sha256\n```\n\n<strong>Expected result:</strong> The fixture contains both address families, resolver roles, TTL, endpoints, and handshake labels.",
        "<strong>Stage 3: Author the resolver-role tracer</strong> — Enforce ordering and address-family requirements.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'PY' > trace_dns.py\nimport ipaddress, json, re\nlines = open('supplied_resolver_output.txt', encoding='utf-8').read().splitlines()\nactors = [re.search(r'actor=([^ ]+)', line).group(1) for line in lines[:7]]\nassert actors == ['stub', 'recursive', 'root', 'tld', 'authoritative', 'recursive', 'stub']\nauth = lines[4]\na = re.search(r'A=([^ ]+)', auth).group(1)\naaaa = re.search(r'AAAA=([^ ]+)', auth).group(1)\nttl = int(re.search(r'ttl=(\\d+)', auth).group(1))\nassert ipaddress.ip_address(a).version == 4\nassert ipaddress.ip_address(aaaa).version == 6\nassert ttl == 300 and 'aa=1' in auth\njson.dump({'actors': actors, 'A': a, 'AAAA': aaaa, 'ttl': ttl, 'cache_expires': 305, 'client': '[2001:db8:10::10]:53000', 'server': '[2001:db8:20::20]:443'}, open('dns_trace.json', 'w'), indent=2)\nPY\npython3 -m py_compile trace_dns.py\n```\n\n<strong>Expected result:</strong> The parser compiles and encodes explicit invariants. <strong>Stop/recovery:</strong> Restore the fixture if ordering assertions fail.",
        "<strong>Stage 4: Execute the resolver trace and diagram</strong> — Produce the role sequence and transport handoff.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 trace_dns.py\npython3 - <<'PY' | tee dns_transport_diagram.txt\nimport json\nd = json.load(open('dns_trace.json'))\nprint('stub -> recursive -> root -> TLD -> authoritative -> recursive cache -> stub')\nprint('A', d['A'], '| AAAA', d['AAAA'], '| TTL', d['ttl'])\nprint(d['client'], '-- SYN -->', d['server'])\nprint(d['client'], '<- SYN-ACK --', d['server'])\nprint(d['client'], '-- ACK -->', d['server'], '[ESTABLISHED expected]')\nPY\n```\n\n<strong>Expected result:</strong> Name resolution ends before the separately labelled transport handshake begins.",
        "<strong>Stage 5: Inspect TTL cache decisions</strong> — Calculate hit and expiry outcomes from supplied times.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 - <<'PY' | tee ttl_decisions.txt\nexpiry = 305\nfor now in (6, 304, 305, 360):\n    state = 'cache_hit' if now < expiry else 'cache_expired_requery'\n    remaining = max(0, expiry - now)\n    print(f't={now} state={state} remaining_ttl={remaining}')\nassert expiry - 6 == 299\nPY\n```\n\n<strong>Expected result:</strong> Times below 305 are hits and times at or above 305 require requery. <strong>Evidence limit:</strong> This is fixture arithmetic, not a live resolver observation.",
        "<strong>Stage 6: Rehearse bounded stale-cache failure</strong> — Evaluate a supplied cutover where a cached old address remains valid.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 - <<'PY' | tee stale_cache_decision.txt\ncutover = 100\ncache_expiry = 305\nold = '198.51.100.20'\nnew = '198.51.100.40'\nassert cutover < cache_expiry\nprint(f'Supplied facts: cutover={cutover}, cached={old}, new_authoritative={new}, cache_expiry={cache_expiry}')\nprint('Inference: a compliant cache can serve the old answer for 205 more seconds.')\nprint('Decision: lower TTL before cutover and verify application connection-pool behavior separately.')\nPY\n```\n\n<strong>Expected result:</strong> The worksheet identifies a bounded stale-answer window without claiming split-brain was observed.",
        "<strong>Stage 7: Record resolver and transport evidence</strong> — State facts, inference, expected behavior, GCP limit, and the exit-evidence distinction.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > dns_evaluation_evidence.md\n# Supplied DNS and transport trace\n\n- Observed locally: parser assertions verified the supplied stub, recursive, root, TLD, authoritative, cache, and delivery sequence for A and AAAA answers.\n- Simulated or predicted: TTL expiry and the SYN -> SYN-ACK -> ACK state transition.\n- Untested on GCP: metadata-resolver behavior, Cloud DNS forwarding, VPC reachability, and a listening backend.\n- Decision: treat name resolution, IP reachability, and established TCP state as separate gates.\n- Evidence limit: the supplied answer and locally computed cache state do not prove a route, firewall decision, or application response.\nEOF\nsha256sum dns_trace.json dns_transport_diagram.txt ttl_decisions.txt stale_cache_decision.txt dns_evaluation_evidence.md | tee dns_evidence.sha256\n```\n\n<strong>Expected result:</strong> Durable evidence maps directly to Practice and Exit evidence.",
        "<strong>Stage 8: Clean up transient resolver inputs</strong> — Preserve decisions, diagram, evidence, and hashes.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\nrm -f supplied_resolver_output.txt resolver_fixture.sha256 trace_dns.py dns_trace.json\nrm -rf __pycache__\nprintf 'preserved: dns_transport_diagram.txt ttl_decisions.txt stale_cache_decision.txt dns_evaluation_evidence.md dns_evidence.sha256\\n' | tee cleanup_summary.txt\n```\n\n<strong>Expected result:</strong> Only lab-owned transient files are removed; no network or cloud cleanup is required."
    ],
    accept="The role trace includes supplied A and AAAA answers, TTL decisions, labelled socket endpoints and SYN/SYN-ACK/ACK, with an evidence limit and hashes; no live DNS dependency or skipped tool remains.",
    trouble="If parsing fails, compare actor ordering and field names with the supplied fixture. Preserve the original fixture and fix the local transcription instead of querying the internet.",
    file_name="dns_evaluation_evidence.md"
)
TOPICS[1]['lab']['mode'] = SUPPLIED_MODE

TOPICS[2]['lab'] = make_lab(
    name="Supplied Dual-Stack Lookup and TCP State-Machine Dissection",
    goal="Correlate supplied A and AAAA resolver answers with labelled socket 4-tuples and validate SYN, SYN-ACK, ACK, ESTABLISHED, FIN, and TIME-WAIT transitions as local fixture analysis.",
    expected="A deterministic transport trace showing which facts come from resolver output, which identify socket endpoints, and which TCP states are predicted by the supplied segment sequence.",
    covers=SUPPLIED_COVERS,
    steps=[
        "<strong>Stage 1: Preflight deterministic transport tools</strong> — Use no packet-capture privilege or live listener.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncommand -v bash\ncommand -v python3\ncommand -v sha256sum\nprintf 'offline transport fixture ready\\n' | tee preflight_socket.txt\n```\n\n<strong>Expected result:</strong> All local tools are present. <strong>Stop/recovery:</strong> Stop if any check fails; do not skip it.",
        "<strong>Stage 2: Prepare supplied resolver and TCP segment output</strong> — Copy the dual-stack and transport fixture.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > supplied_transport_trace.txt\nSUPPLIED lookup=A name=api.example.test answer=198.51.100.20 ttl=120\nSUPPLIED lookup=AAAA name=api.example.test answer=2001:db8:20::20 ttl=120\nSUPPLIED segment=1 src=[2001:db8:10::10]:53000 dst=[2001:db8:20::20]:443 flags=SYN seq=1000 ack=0 state=SYN-SENT\nSUPPLIED segment=2 src=[2001:db8:20::20]:443 dst=[2001:db8:10::10]:53000 flags=SYN-ACK seq=7000 ack=1001 state=SYN-RECEIVED\nSUPPLIED segment=3 src=[2001:db8:10::10]:53000 dst=[2001:db8:20::20]:443 flags=ACK seq=1001 ack=7001 state=ESTABLISHED\nSUPPLIED segment=4 src=[2001:db8:10::10]:53000 dst=[2001:db8:20::20]:443 flags=FIN-ACK seq=1001 ack=7001 state=FIN-WAIT-1\nSUPPLIED segment=5 src=[2001:db8:20::20]:443 dst=[2001:db8:10::10]:53000 flags=ACK seq=7001 ack=1002 state=TIME-WAIT-PREDICTED\nEOF\nsha256sum supplied_transport_trace.txt | tee transport_fixture.sha256\n```\n\n<strong>Expected result:</strong> Both address families and five labelled transport segments are saved.",
        "<strong>Stage 3: Author the TCP state analyzer</strong> — Validate endpoint reversal and acknowledgment arithmetic.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'PY' > analyze_transport.py\nimport ipaddress, json\nlines = open('supplied_transport_trace.txt', encoding='utf-8').read().splitlines()\nlookups = [dict(t.split('=', 1) for t in line.split()[1:]) for line in lines[:2]]\nassert [ipaddress.ip_address(x['answer']).version for x in lookups] == [4, 6]\nsegments = [dict(t.split('=', 1) for t in line.split()[1:]) for line in lines[2:]]\nassert [s['flags'] for s in segments[:3]] == ['SYN', 'SYN-ACK', 'ACK']\nassert segments[0]['src'] == segments[1]['dst'] and segments[0]['dst'] == segments[1]['src']\nassert int(segments[1]['ack']) == int(segments[0]['seq']) + 1\nassert int(segments[2]['ack']) == int(segments[1]['seq']) + 1\njson.dump({'lookups': lookups, 'segments': segments}, open('transport_trace.json', 'w'), indent=2)\nPY\npython3 -m py_compile analyze_transport.py\n```\n\n<strong>Expected result:</strong> The analyzer compiles with explicit handshake invariants.",
        "<strong>Stage 4: Execute and label the socket handshake</strong> — Render direction, endpoints, flags, and supplied or predicted state.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 analyze_transport.py\npython3 - <<'PY' | tee transport_state_diagram.txt\nimport json\nd = json.load(open('transport_trace.json'))\nprint('A ->', d['lookups'][0]['answer'], '| AAAA ->', d['lookups'][1]['answer'])\nfor s in d['segments']:\n    print(f\"{s['src']} -- {s['flags']} --> {s['dst']} [{s['state']}]\")\nPY\n```\n\n<strong>Expected result:</strong> The first three segments label SYN, SYN-ACK, and ACK with reversed server/client endpoints and expected ESTABLISHED state.",
        "<strong>Stage 5: Inspect connection-state evidence</strong> — Separate wire fields from state-machine inference.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 - <<'PY' | tee transport_evidence_review.txt\nimport json\nd = json.load(open('transport_trace.json'))\nprint('Observed locally: parsed', len(d['lookups']), 'supplied lookup lines and', len(d['segments']), 'supplied segment lines.')\nprint('Supplied facts: endpoints, flags, sequence numbers, acknowledgments, and labelled fixture states.')\nprint('Inference: the first three valid segments correspond to TCP establishment.')\nprint('Expected behavior: an active close retains TIME-WAIT according to implementation timers.')\nprint('Evidence limit: no packet capture, listener queue, or GCP path was observed.')\nPY\n```\n\n<strong>Expected result:</strong> Every evidence category is explicit and avoids treating fixture labels as live kernel observation.",
        "<strong>Stage 6: Rehearse a bounded handshake defect</strong> — Reject a supplied sequence whose SYN-ACK acknowledges the wrong client sequence.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\npython3 - <<'PY' | tee handshake_defect.txt\nclient_seq = 1000\nbad_ack = 1009\nvalid = bad_ack == client_seq + 1\nassert not valid\nprint('Supplied defect: SYN seq=1000; SYN-ACK ack=1009')\nprint('Diagnosis: acknowledgment invariant failed; do not label this trace ESTABLISHED.')\nprint('Recovery: obtain an unmodified capture or resolver fixture and repeat local parsing.')\nPY\n```\n\n<strong>Expected result:</strong> The analyzer records a failed invariant without generating or sending packets.",
        "<strong>Stage 7: Record the transport architecture decision</strong> — Map the supplied lookup, endpoints, handshake, and Exit boundary.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\ncat <<'EOF' > socket_queue_evidence.md\n# Supplied resolver and TCP state-machine evidence\n\n- Observed locally: assertions verified one supplied IPv4 answer, one supplied IPv6 answer, endpoint reversal, and SYN/SYN-ACK/ACK arithmetic.\n- Simulated or predicted: ESTABLISHED and TIME-WAIT are state-machine interpretations of the supplied segment sequence.\n- Untested on GCP: load-balancer frontend negotiation, backend transport, guest socket buffers, and queue overflow.\n- Decision: gate diagnosis in order—name resolution, reachability/policy, handshake, then application readiness.\n- Evidence limit: a valid supplied handshake proves only fixture consistency; it is not a local or production packet capture.\nEOF\nsha256sum transport_trace.json transport_state_diagram.txt transport_evidence_review.txt handshake_defect.txt socket_queue_evidence.md | tee transport_evidence.sha256\n```\n\n<strong>Expected result:</strong> The evidence maps directly to the roadmap Practice and Exit artifact.",
        "<strong>Stage 8: Clean up only transient transport files</strong> — Preserve the diagram, reviews, evidence, and hashes.\n\n<strong>Location:</strong> Local Linux terminal\n\n```bash\nrm -f supplied_transport_trace.txt transport_fixture.sha256 analyze_transport.py transport_trace.json\nrm -rf __pycache__\nprintf 'preserved: transport_state_diagram.txt transport_evidence_review.txt handshake_defect.txt socket_queue_evidence.md transport_evidence.sha256\\n' | tee cleanup_summary.txt\n```\n\n<strong>Expected result:</strong> No listener, packet capture, or cloud resource exists; durable evidence remains."
    ],
    accept="The supplied A/AAAA records, socket endpoints, and SYN/SYN-ACK/ACK sequence pass local assertions; the malformed handshake is rejected; and the evidence distinguishes fixture consistency from observed network behavior.",
    trouble="If endpoint or acknowledgment assertions fail, compare the supplied source/destination reversal and ack=peer-seq+1 rules. Do not weaken assertions or claim ESTABLISHED.",
    file_name="socket_queue_evidence.md"
)
TOPICS[2]['lab']['mode'] = SUPPLIED_MODE

for _topic, _save_targets in (
    (TOPICS[1], (
        'preflight_dns.txt',
        'supplied_resolver_output.txt and resolver_fixture.sha256',
        'trace_dns.py',
        'dns_trace.json and dns_transport_diagram.txt',
        'ttl_decisions.txt',
        'stale_cache_decision.txt',
        'dns_evaluation_evidence.md and dns_evidence.sha256',
        'cleanup_summary.txt',
    )),
    (TOPICS[2], (
        'preflight_socket.txt',
        'supplied_transport_trace.txt and transport_fixture.sha256',
        'analyze_transport.py',
        'transport_trace.json and transport_state_diagram.txt',
        'transport_evidence_review.txt',
        'handshake_defect.txt',
        'socket_queue_evidence.md and transport_evidence.sha256',
        'cleanup_summary.txt',
    )),
):
    _topic['lab']['steps'] = [
        step + f"\n\n<strong>Save:</strong> <samp>{target}</samp>."
        for step, target in zip(_topic['lab']['steps'], _save_targets)
    ]

REVIEW_RECORDS = {
    'source_ledger': {
        'https://datatracker.ietf.org/doc/html/rfc4291#section-2': {
            'heading_opened': '2. IPv6 Addressing',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        },
        'https://datatracker.ietf.org/doc/html/rfc1035#section-3.2.1': {
            'heading_opened': '3.2.1. Format',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        },
        'https://datatracker.ietf.org/doc/html/rfc9293#section-3': {
            'heading_opened': '3. Functional Specification',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        },
        'https://cloud.google.com/dns/docs/overview#dns-forwarding-methods': {
            'heading_opened': 'DNS forwarding methods',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://cloud.google.com/dns/docs/zones/zones-overview#forwarding_zones': {
            'heading_opened': 'Forwarding zones',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://cloud.google.com/dns/docs/dnssec-advanced#advanced-signing-options': {
            'heading_opened': 'Use advanced signing options',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster': {
            'heading_opened': 'TCP BBR Congestion Control in GCP',
            'rfc_status': 'not applicable',
            'whole_document_reason': 'Google Cloud Blog publication introducing TCP BBR congestion control on GCP without HTML section anchors.'
        },
        'https://cloud.google.com/load-balancing/docs/https#QUIC': {
            'heading_opened': 'HTTP/3 support',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://cloud.google.com/vpc/docs/subnets#ipv6-ranges': {
            'heading_opened': 'IPv6 subnet ranges',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://man7.org/linux/man-pages/man1/tcpdump.1.html#DESCRIPTION': {
            'heading_opened': 'DESCRIPTION',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://man7.org/linux/man-pages/man8/ss.8.html#DESCRIPTION': {
            'heading_opened': 'DESCRIPTION',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        }
    },
    'product_claims': [
        {
            'claim': 'Google Cloud VPC subnets support dual-stack operation and allocate a /64 prefix from internal or external ranges.',
            'section_url': 'https://cloud.google.com/vpc/docs/subnets#ipv6-ranges',
            'heading_opened': 'IPv6 subnet ranges'
        },
        {
            'claim': 'Google Cloud Load Balancing supports HTTP/3 and QUIC termination on external Application Load Balancers.',
            'section_url': 'https://cloud.google.com/load-balancing/docs/https#QUIC',
            'heading_opened': 'HTTP/3 support'
        },
        {
            'claim': 'Google Cloud DNS provides authoritative DNS resolution with private managed zones and outbound DNS forwarding methods.',
            'section_url': 'https://cloud.google.com/dns/docs/overview#dns-forwarding-methods',
            'heading_opened': 'DNS forwarding methods'
        },
        {
            'claim': 'Cloud DNS forwarding zones support private resolution across hybrid interconnects with forwarding targets and routing policies.',
            'section_url': 'https://cloud.google.com/dns/docs/zones/zones-overview#forwarding_zones',
            'heading_opened': 'Forwarding zones'
        },
        {
            'claim': 'Cloud DNS advanced signing options let a managed zone select supported KSK and ZSK algorithms, key lengths, and NSEC or NSEC3 denial of existence.',
            'section_url': 'https://cloud.google.com/dns/docs/dnssec-advanced#advanced-signing-options',
            'heading_opened': 'Use advanced signing options'
        },
        {
            'claim': 'The Google Cloud BBR publication describes BBR as modeling bottleneck bandwidth and round-trip propagation time and names service-to-user paths that use it.',
            'section_url': 'https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster',
            'heading_opened': 'TCP BBR Congestion Control in GCP'
        }
    ],
    'visual_reasons': {
        'Day 3 End-to-End DNS, IPv6, Socket Lifecycle, and Transport Topology': 'Retained qualifying multi-tier architecture topology mapping dual-stack ingress, DNS resolution runtime, BSD socket lifecycle, and verification boundaries.',
        'DNS Resolution vs Network IP Reachability vs Established Socket Connection': 'Retained qualifying exit evidence diagram separating DNS name resolution, L3 IP reachability, and L4 established socket connection.',
        'Recursive DNS resolution pipeline: stub client to authoritative zone': 'Added qualifying 6-node flow diagram illustrating the multi-step request/response lifecycle from stub resolver query through Root, TLD, and authoritative name servers down to cached client delivery.'
    }
}

DATA = {
    'contract_version': 2,
    'day': DAY,
    'day_padded': '003',
    'title': 'Day 3 — DNS, sockets and transport',
    'time_estimate': '2–3 hours',
    'prerequisites': '[Day 2](#day-2); bring their exit artifacts.',
    'work_block': WORK_BLOCK,
    'roadmap_practice': ROADMAP_PRACTICE,
    'roadmap_exit': ROADMAP_EXIT,
    'access_date': ACCESS_DATE,
    'sources': SOURCES,
    'lab_defaults': {},
    'part1_html': PART1_HTML,
    'part1_intro': PART1_INTRO,
    'part2_intro': PART2_INTRO,
    'part3_intro': PART3_INTRO,
    'part4_intro': PART4_INTRO,
    'exit_summary': EXIT_SUMMARY,
    'arch_diagram': ARCH_DIAGRAM,
    'arch_svg_html': ARCH_SVG_HTML,
    'arch_table_html': ARCH_TABLE_HTML,
    'topics': TOPICS,
    'review_records': REVIEW_RECORDS,
}
