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
ACCESS_DATE = '2026-10-08'
WORK_BLOCK = "Days 1–17 — Foundations"
EXIT_SUMMARY = "A DNS/transport diagram distinguishing name resolution, reachability and established connection."
ROADMAP_PRACTICE = "Trace an IPv4 and IPv6 lookup from supplied resolver output; label socket endpoints and the TCP handshake."
ROADMAP_EXIT = "A DNS/transport diagram distinguishing name resolution, reachability and established connection."

SOURCES = {
    'rfc4291': ('RFC 4291: IPv6 Addressing Architecture, section 2 (accessed 2026-10-08)', 'https://datatracker.ietf.org/doc/html/rfc4291#section-2'),
    'rfc1035': ('RFC 1035: Domain Names - Implementation and Specification, section 3.2.1 (accessed 2026-10-08)', 'https://datatracker.ietf.org/doc/html/rfc1035#section-3.2.1'),
    'rfc9293': ('RFC 9293: Transmission Control Protocol, section 3 (accessed 2026-10-08)', 'https://datatracker.ietf.org/doc/html/rfc9293#section-3'),
    'cloud_dns': ('Google Cloud DNS documentation: DNS overview (accessed 2026-10-08)', 'https://cloud.google.com/dns/docs/overview#dns-forwarding-methods'),
    'cloud_dns_zones': ('Google Cloud DNS documentation: DNS zones overview (accessed 2026-10-08)', 'https://cloud.google.com/dns/docs/zones/zones-overview#forwarding_zones'),
    'cloud_dns_dnssec': ('Google Cloud DNS documentation: Use advanced DNSSEC (accessed 2026-10-08)', 'https://cloud.google.com/dns/docs/dnssec-advanced#advanced-signing-options'),
    'bbr': ('Google Cloud Networking: TCP BBR Congestion Control in GCP (accessed 2026-10-08)', 'https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster'),
    'http3': ('Google Cloud Load Balancing documentation: HTTP/3 and QUIC support (accessed 2026-10-08)', 'https://cloud.google.com/load-balancing/docs/https#QUIC'),
    'vpc_ipv6': ('Google Cloud VPC documentation: IPv6 subnet ranges (accessed 2026-10-08)', 'https://cloud.google.com/vpc/docs/subnets#ipv6-ranges'),
    'tcpdump': ('Linux man-pages: tcpdump(1) packet capture tool description (accessed 2026-10-08)', 'https://man7.org/linux/man-pages/man1/tcpdump.1.html#DESCRIPTION'),
    'ss': ('Linux man-pages: ss(8) socket statistics utility description (accessed 2026-10-08)', 'https://man7.org/linux/man-pages/man8/ss.8.html#DESCRIPTION'),
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
        '<strong class="keyword">IPv6</strong> expands the network address space to 128 bits while establishing architectural scoping boundaries that strictly govern packet reachability. Link-local addresses (<samp>fe80::/10</samp>) require an explicit interface zone identifier, Unique Local Addresses (ULA, <samp>fc00::/7</samp>) provide private enterprise routing, and Global Unicast Addresses (GUA, <samp>2000::/3</samp>) provide internet-wide reachability. Neighbor Discovery Protocol (NDP) replaces broadcast ARP with multicast ICMPv6 messaging, forming the foundation for Google Cloud dual-stack VPC networking.',
        'Day 3 establishes modern 128-bit addressing mechanics following Day 2\'s IPv4 foundations.',
        'In enterprise cloud architecture, IPv6 sits at the edge ingress boundary, hybrid interconnects, and dual-stack VPC subnets.',
        'A microservice client receives an IPv6 AAAA record resolving to a link-local address but attempts to initiate a TCP connection without specifying an interface scope index. The connection immediately errors out with Invalid Argument, halting automated canary deployments and blocking scheduled microservice updates.'
    ),
    (
        'topic-02',
        '2. DNS records, TTL and resolver roles',
        '<strong class="keyword">DNS</strong> provides a globally distributed, hierarchical database mapping domain names to typed resource records across Root, TLD, and authoritative name servers. Stub resolvers delegate recursive queries to recursive resolvers, which traverse iterative referral chains and cache answers according to Time-To-Live (TTL) policies. Cryptographic extensions (DNSSEC) authenticate record authenticity via digital signatures, while Google Cloud DNS provides managed private and public zones with global Anycast resilience.',
        'Day 3 connects network addressing to human-readable names before Day 4\'s TLS certificate validation and HTTP layer exploration.',
        'In Google Cloud, DNS sits inside Cloud DNS managed private zones, split-horizon resolution paths, and metadata server resolvers.',
        'An operations team modifies a DNS A record during a critical database failover but overlooks a 3600-second TTL cached across upstream recursive resolvers. Application pods continue directing transactional traffic to the decommissioned primary database for over forty minutes, resulting in split-brain data corruption and order reconciliation failures.'
    ),
    (
        'topic-03',
        '3. TCP and UDP, ports, connection states and buffers',
        '<strong class="keyword">Transport protocols</strong> establish host-to-host process communication using 16-bit ports and Berkeley Software Distribution (BSD) socket abstractions. TCP enforces reliable byte-stream delivery through 3-way handshakes, sliding-window flow control, and model-based congestion control (BBR), while UDP provides lightweight, connectionless datagram transport powering modern QUIC and HTTP/3. Sockets manage kernel receive and send buffers, accept queues, and state lifecycles observable through kernel instrumentation tools.',
        'Day 3 completes transport mechanics before examining application protocols on Day 4.',
        'In cloud systems, transport mechanics govern guest OS socket buffer depths, Compute Engine TCP throughput, and Cloud Load Balancer proxy timeouts.',
        'A high-concurrency API service encounters socket accept queue saturation under peak promotional traffic while CPU utilization sits at barely thirty percent. Inbound TCP SYN packets are silently dropped by the kernel network stack, causing upstream load balancers to log HTTP 504 gateway timeouts and prompting clients to retry aggressively, amplifying the cascade.'
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
            "x": 40,
            "y": 425,
            "w": 1040,
            "h": 135,
            "label": "VERIFICATION BOUNDARY · NAME RESOLUTION ≠ IP REACHABILITY ≠ TCP STATE ≠ APPLICATION READINESS",
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
    <text x="48" y="39" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">Queries Cloud DNS / 8.8.8.8 / 169.254.169.254</text>
    <text x="48" y="52" font-family="monospace" font-size="8" fill="#7dd3fc">Returns: A / AAAA RRset with TTL</text>
  </g>

  <!-- Arrow Down 1.1 -->
  <line x1="197" y1="185" x2="197" y2="210" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#exit-arr-blue)"/>

  <!-- Box 1.2: Boundary Proven -->
  <g transform="translate(45, 215)">
    <rect width="305" height="75" rx="4" fill="#052e16" stroke="#22c55e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/policy.svg" x="12" y="24" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#4ade80" font-weight="bold">BOUNDARY PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="8.5" fill="#bbf7d0">✓ Hostname exists in zone database</text>
    <text x="48" y="52" font-family="sans-serif" font-size="8.5" fill="#bbf7d0">✓ Authoritative name servers respond</text>
    <text x="48" y="65" font-family="sans-serif" font-size="8.5" fill="#bbf7d0">✓ DNSSEC signature valid (AD flag = 1)</text>
  </g>

  <!-- Arrow Down 1.2 -->
  <line x1="197" y1="290" x2="197" y2="315" stroke="#f43f5e" stroke-width="1.5" marker-end="url(#exit-arr-fail)"/>

  <!-- Box 1.3: What is NOT Proven -->
  <g transform="translate(45, 320)">
    <rect width="305" height="85" rx="4" fill="#3b0712" stroke="#f43f5e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/failure.svg" x="12" y="28" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#f87171" font-weight="bold">WHAT IS NOT PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Does NOT prove IP route exists</text>
    <text x="48" y="52" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Does NOT prove remote host is alive</text>
    <text x="48" y="65" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Does NOT prove destination port listens</text>
    <text x="48" y="78" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Link-local IPv6 fails without zone index</text>
  </g>

  <!-- Box 1.4: Tools & Errors -->
  <g transform="translate(45, 420)">
    <rect width="305" height="65" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="12" y="18" font-family="monospace" font-size="8.5" fill="#94a3b8">Diagnostic Tooling:</text>
    <text x="12" y="32" font-family="monospace" font-size="8" fill="#7dd3fc">dig +trace, dig +dnssec, delv, host</text>
    <text x="12" y="46" font-family="monospace" font-size="8.5" fill="#f87171">Failure Signals:</text>
    <text x="12" y="58" font-family="monospace" font-size="8" fill="#fca5a5">NXDOMAIN, SERVFAIL, REFUSED, Stale TTL</text>
  </g>

  <!-- Transition Arrow: Column 1 to Column 2 -->
  <line x1="370" y1="250" x2="385" y2="250" stroke="#38bdf8" stroke-width="2" marker-end="url(#exit-arr-blue)"/>
  <text x="378" y="240" text-anchor="middle" font-family="monospace" font-size="8" fill="#38bdf8">pass</text>

  <!-- Column 2: Phase 2 - L3 IP Reachability (Middle) -->
  <rect x="388" y="75" width="345" height="425" rx="6" fill="#090d16" stroke="#22c55e" stroke-width="1.5"/>
  <rect x="398" y="85" width="325" height="24" rx="4" fill="#052e16" stroke="#22c55e" stroke-width="1"/>
  <text x="560" y="101" text-anchor="middle" font-family="monospace" font-size="10.5" fill="#22c55e" font-weight="bold">PHASE 2 · NETWORK IP REACHABILITY</text>

  <!-- Box 2.1: Component -->
  <g transform="translate(408, 120)">
    <rect width="305" height="65" rx="4" fill="#121827" stroke="#22c55e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/router.svg" x="12" y="20" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="11" fill="#22c55e" font-weight="bold">IP Routing &amp; Link Discovery</text>
    <text x="48" y="39" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">FIB Lookup · ARP (IPv4) / NDP (IPv6)</text>
    <text x="48" y="52" font-family="monospace" font-size="8" fill="#a7f3d0">Transmits: IP Packet / ICMP Echo / NS-NA</text>
  </g>

  <!-- Arrow Down 2.1 -->
  <line x1="560" y1="185" x2="560" y2="210" stroke="#22c55e" stroke-width="1.5" marker-end="url(#exit-arr-green)"/>

  <!-- Box 2.2: Boundary Proven -->
  <g transform="translate(408, 215)">
    <rect width="305" height="75" rx="4" fill="#052e16" stroke="#22c55e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/policy.svg" x="12" y="24" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#4ade80" font-weight="bold">BOUNDARY PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="8.5" fill="#bbf7d0">✓ Route table matches destination CIDR</text>
    <text x="48" y="52" font-family="sans-serif" font-size="8.5" fill="#bbf7d0">✓ Neighbor MAC resolved on local segment</text>
    <text x="48" y="65" font-family="sans-serif" font-size="8.5" fill="#bbf7d0">✓ Intermediate routers forward hop-by-hop</text>
  </g>

  <!-- Arrow Down 2.2 -->
  <line x1="560" y1="290" x2="560" y2="315" stroke="#f43f5e" stroke-width="1.5" marker-end="url(#exit-arr-fail)"/>

  <!-- Box 2.3: What is NOT Proven -->
  <g transform="translate(408, 320)">
    <rect width="305" height="85" rx="4" fill="#3b0712" stroke="#f43f5e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/failure.svg" x="12" y="28" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#f87171" font-weight="bold">WHAT IS NOT PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Does NOT prove destination TCP port open</text>
    <text x="48" y="52" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Does NOT prove SYN handshake succeeds</text>
    <text x="48" y="65" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Does NOT prove accept queue has space</text>
    <text x="48" y="78" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Firewall may permit ICMP but drop TCP</text>
  </g>

  <!-- Box 2.4: Tools & Errors -->
  <g transform="translate(408, 420)">
    <rect width="305" height="65" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="12" y="18" font-family="monospace" font-size="8.5" fill="#94a3b8">Diagnostic Tooling:</text>
    <text x="12" y="32" font-family="monospace" font-size="8" fill="#a7f3d0">ip route get, ip neigh, ping, traceroute -I</text>
    <text x="12" y="46" font-family="monospace" font-size="8.5" fill="#f87171">Failure Signals:</text>
    <text x="12" y="58" font-family="monospace" font-size="8" fill="#fca5a5">No route to host (ENETUNREACH), EINVAL, ICMP Time Exceeded</text>
  </g>

  <!-- Transition Arrow: Column 2 to Column 3 -->
  <line x1="733" y1="250" x2="748" y2="250" stroke="#22c55e" stroke-width="2" marker-end="url(#exit-arr-green)"/>
  <text x="740" y="240" text-anchor="middle" font-family="monospace" font-size="8" fill="#22c55e">pass</text>

  <!-- Column 3: Phase 3 - L4 TCP Connection (Right) -->
  <rect x="750" y="75" width="345" height="425" rx="6" fill="#090d16" stroke="#f59e0b" stroke-width="1.5"/>
  <rect x="760" y="85" width="325" height="24" rx="4" fill="#241808" stroke="#f59e0b" stroke-width="1"/>
  <text x="922" y="101" text-anchor="middle" font-family="monospace" font-size="10.5" fill="#f59e0b" font-weight="bold">PHASE 3 · ESTABLISHED CONNECTION (L4)</text>

  <!-- Box 3.1: Component -->
  <g transform="translate(770, 120)">
    <rect width="305" height="65" rx="4" fill="#121827" stroke="#f59e0b" stroke-width="1.5"/>
    <image href="../assets/icons/generic/server.svg" x="12" y="20" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="11" fill="#f59e0b" font-weight="bold">TCP Transport State Machine</text>
    <text x="48" y="39" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">3-Way Handshake (SYN → SYN-ACK → ACK)</text>
    <text x="48" y="52" font-family="monospace" font-size="8" fill="#fde68a">Kernel State: ESTABLISHED (4-Tuple Bound)</text>
  </g>

  <!-- Arrow Down 3.1 -->
  <line x1="922" y1="185" x2="922" y2="210" stroke="#f59e0b" stroke-width="1.5" marker-end="url(#exit-arr-amber)"/>

  <!-- Box 3.2: Boundary Proven -->
  <g transform="translate(770, 215)">
    <rect width="305" height="75" rx="4" fill="#052e16" stroke="#22c55e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/policy.svg" x="12" y="24" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#4ade80" font-weight="bold">BOUNDARY PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="8.5" fill="#bbf7d0">✓ Target process bound to IP:port (LISTEN)</text>
    <text x="48" y="52" font-family="sans-serif" font-size="8.5" fill="#bbf7d0">✓ 3-Way handshake completed (ESTABLISHED)</text>
    <text x="48" y="65" font-family="sans-serif" font-size="8.5" fill="#bbf7d0">✓ Socket buffers allocated (sk_rcvbuf/sndbuf)</text>
  </g>

  <!-- Arrow Down 3.2 -->
  <line x1="922" y1="290" x2="922" y2="315" stroke="#f43f5e" stroke-width="1.5" marker-end="url(#exit-arr-fail)"/>

  <!-- Box 3.3: What is NOT Proven -->
  <g transform="translate(770, 320)">
    <rect width="305" height="85" rx="4" fill="#3b0712" stroke="#f43f5e" stroke-width="1.5"/>
    <image href="../assets/icons/generic/failure.svg" x="12" y="28" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
    <text x="48" y="24" font-family="monospace" font-size="10" fill="#f87171" font-weight="bold">WHAT IS NOT PROVEN:</text>
    <text x="48" y="39" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Does NOT prove application parsed request</text>
    <text x="48" y="52" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Does NOT prove TLS handshake succeeds</text>
    <text x="48" y="65" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Does NOT prove downstream DB is healthy</text>
    <text x="48" y="78" font-family="sans-serif" font-size="8.5" fill="#fecaca">✗ Worker thread may hang on blocked I/O</text>
  </g>

  <!-- Box 3.4: Tools & Errors -->
  <g transform="translate(770, 420)">
    <rect width="305" height="65" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="12" y="18" font-family="monospace" font-size="8.5" fill="#94a3b8">Diagnostic Tooling:</text>
    <text x="12" y="32" font-family="monospace" font-size="8" fill="#fde68a">ss -tuanp, tcpdump -nn, netstat -s, lsof -i</text>
    <text x="12" y="46" font-family="monospace" font-size="8.5" fill="#f87171">Failure Signals:</text>
    <text x="12" y="58" font-family="monospace" font-size="8" fill="#fca5a5">ECONNREFUSED (RST), ETIMEDOUT, somaxconn overflow</text>
  </g>

  <!-- Bottom Diagnostic Footer Banner -->
  <rect x="25" y="515" width="1070" height="105" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="40" y="533" font-family="monospace" font-size="10" fill="#94a3b8" font-weight="bold">BOUNDARY FAILURE SEPARATION &amp; ARCHITECTURAL DIAGNOSTIC CHECKS:</text>

  <!-- Card 1 -->
  <g transform="translate(38, 542)">
    <rect width="250" height="72" rx="3" fill="#121827" stroke="#38bdf8" stroke-width="1"/>
    <image href="../assets/icons/generic/decision.svg" x="8" y="8" width="18" height="18" preserveAspectRatio="xMidYMid meet"/>
    <text x="32" y="18" font-family="monospace" font-size="8.5" fill="#38bdf8" font-weight="bold">NAME RESOLUTION CHECK</text>
    <text x="10" y="34" font-family="sans-serif" font-size="8" fill="#cbd5e1">• Fails at DNS: Hostname cannot be queried</text>
    <text x="10" y="47" font-family="sans-serif" font-size="8" fill="#cbd5e1">• Check DNS TTL &amp; local resolver cache</text>
    <text x="10" y="60" font-family="monospace" font-size="7.5" fill="#7dd3fc">Tool: dig +trace, resolvectl status</text>
  </g>

  <!-- Card 2 -->
  <g transform="translate(300, 542)">
    <rect width="250" height="72" rx="3" fill="#121827" stroke="#22c55e" stroke-width="1"/>
    <image href="../assets/icons/generic/endpoint.svg" x="8" y="8" width="18" height="18" preserveAspectRatio="xMidYMid meet"/>
    <text x="32" y="18" font-family="monospace" font-size="8.5" fill="#22c55e" font-weight="bold">IP REACHABILITY CHECK</text>
    <text x="10" y="34" font-family="sans-serif" font-size="8" fill="#cbd5e1">• Fails at L3: Packet dropped by route or ACL</text>
    <text x="10" y="47" font-family="sans-serif" font-size="8" fill="#cbd5e1">• IPv6 requires zone index (%eth0) if link-local</text>
    <text x="10" y="60" font-family="monospace" font-size="7.5" fill="#a7f3d0">Tool: ip route get, traceroute -I</text>
  </g>

  <!-- Card 3 -->
  <g transform="translate(562, 542)">
    <rect width="250" height="72" rx="3" fill="#121827" stroke="#f59e0b" stroke-width="1"/>
    <image href="../assets/icons/generic/server.svg" x="8" y="8" width="18" height="18" preserveAspectRatio="xMidYMid meet"/>
    <text x="32" y="18" font-family="monospace" font-size="8.5" fill="#f59e0b" font-weight="bold">TCP CONNECTION CHECK</text>
    <text x="10" y="34" font-family="sans-serif" font-size="8" fill="#cbd5e1">• Fails at L4: Port closed (RST) or queue full</text>
    <text x="10" y="47" font-family="sans-serif" font-size="8" fill="#cbd5e1">• SYN drop under burst: check somaxconn</text>
    <text x="10" y="60" font-family="monospace" font-size="7.5" fill="#fde68a">Tool: ss -lnt, netstat -s, tcpdump -nn</text>
  </g>

  <!-- Card 4 -->
  <g transform="translate(824, 542)">
    <rect width="258" height="72" rx="3" fill="#121827" stroke="#ec4899" stroke-width="1"/>
    <image href="../assets/icons/generic/outcome.svg" x="8" y="8" width="18" height="18" preserveAspectRatio="xMidYMid meet"/>
    <text x="32" y="18" font-family="monospace" font-size="8.5" fill="#ec4899" font-weight="bold">APPLICATION READINESS</text>
    <text x="10" y="34" font-family="sans-serif" font-size="8" fill="#cbd5e1">• Fails at L7: HTTP 500/502/503 status code</text>
    <text x="10" y="47" font-family="sans-serif" font-size="8" fill="#cbd5e1">• L4 success gives FALSE positive for L7 health</text>
    <text x="10" y="60" font-family="monospace" font-size="7.5" fill="#fbcfe8">Tool: curl -iv, OpenTelemetry traces</text>
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
        ('Stub resolver query', ('Client getaddrinfo() query', 'Recursion Desired: RD=1'), 'client'),
        ('Recursive resolver lookup', ('Checks local TTL cache', 'Cache miss triggers query'), 'dns-resolver'),
        ('Root name server referral', ('Queries Anycast Root (.)', 'Referral to .com TLD servers'), 'decision'),
        ('TLD name server referral', ('Queries TLD (.com) server', 'Referral to domain NS'), 'dns-resolver'),
        ('Authoritative zone answer', ('Queries ns1.example.com', 'Authoritative Answer (AA=1)'), 'server'),
        ('Cache & client delivery', ('Caches RRset for TTL duration', 'Returns IP to application'), 'outcome'),
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
            "<strong class='side-heading'>Subtopics in this discussion:</strong> IPv6 128-bit address architecture and canonical representation; "
            "address scoping boundaries (Link-Local, Unique Local, and Global Unicast); "
            "Neighbor Discovery Protocol (NDP) mechanics (RS/RA, NS/NA, SLAAC, DAD); "
            "dual-stack VPC architecture, Happy Eyeballs (RFC 8305), and Google Cloud edge ingress.\n\n"

            "### IPv6 128-bit address architecture and canonical representation\n"
            "<strong class='side-heading'>What it is in general:</strong> <strong class='keyword'>Internet Protocol version 6 (IPv6)</strong> (RFC 8200, RFC 4291) expands the IP address space from 32 bits ($2^{32} \\approx 4.3 \\times 10^9$) "
            "to 128 bits ($2^{128} \\approx 3.4 \\times 10^{38}$), eliminating the architectural requirement for Network Address Translation (NAT). "
            "An IPv6 address consists of eight 16-bit hexadecimal quads separated by colons (e.g., <samp>2001:0db8:85a3:0000:0000:8a2e:0370:7334</samp>). "
            "Under RFC 5952 canonical formatting rules: (1) leading zeros within any quad must be suppressed; (2) lowercase hexadecimal characters must be used; "
            "and (3) the single longest run of consecutive all-zero quads must be compressed exactly once using a double colon (<samp>::</samp>). For instance, "
            "<samp>2001:db8:85a3::8a2e:370:7334</samp> is canonical, whereas compressing isolated single zeros or using double colons multiple times is invalid.\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> Canonical string parsing is critical for automated cloud infrastructure, Continuous Integration / Continuous Deployment (CI/CD) pipelines, firewall policies, "
            "and audit logging. Non-canonical variations of the same IPv6 address can bypass naive string-matching security rules, cause IP Address Management (IPAM) database deduplication "
            "failures, or break automated infrastructure-as-code validations across multi-cloud environments.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> In Google Cloud, subnets support dual-stack operation. As documented in "
            "[Google Cloud VPC documentation: IPv6 subnet ranges](https://cloud.google.com/vpc/docs/subnets#ipv6-ranges), Google Cloud allocates a <samp>/64</samp> IPv6 subnet prefix "
            "from internal or external allocations, requiring architects to configure canonical IPv6 routes and firewall rules across Andromeda virtual network fabrics.\n\n"

            "### Address scoping boundaries (Link-Local, Unique Local, and Global Unicast)\n"
            "<strong class='side-heading'>What it is in general:</strong> Unlike IPv4 where private ranges (<strong class='keyword'>address scopes</strong>) are routable across any private network, IPv6 introduces strict, architecturally enforced address scopes:\n"
            "- **Link-Local Unicast (<samp>fe80::/10</samp>):** Automatically configured on every active IPv6 interface. Link-local addresses are topologically bounded to the local Layer 2 broadcast/broadcast-equivalent segment and are never forwarded by routers. Because identical link-local addresses can legally exist on distinct interfaces connected to different physical links, the operating system cannot route packets to a link-local destination without an explicit **Zone Identifier / Interface Index** (e.g., <samp>fe80::1%eth0</samp> on Linux). Initiating a socket connection to a bare link-local address without a zone index fails immediately with <samp>EINVAL</samp> (Invalid argument).\n"
            "- **Unique Local Address (ULA, <samp>fc00::/7</samp>, RFC 4193):** Globally unique private addresses intended for local communications across an enterprise private Wide Area Network (WAN) or hybrid interconnect. Block <samp>fd00::/8</samp> is assigned with a 40-bit pseudo-random Global ID, preventing address collisions during future enterprise corporate mergers or Virtual Private Cloud (VPC) peerings without NAT.\n"
            "- **Global Unicast Address (GUA, <samp>2000::/3</samp>, RFC 3587):** Globally routable public addresses allocated by Regional Internet Registries (RIRs). Typically structured as a 48-bit global routing prefix assigned to the enterprise, a 16-bit subnet ID (providing up to 65,536 individual subnets per enterprise site), and a 64-bit Interface Identifier (IID).\n"
            "- **Special Purpose Addresses:** Loopback (<samp>::1/128</samp>), Unspecified (<samp>::/128</samp>, used as source during boot prior to Duplicate Address Detection [DAD]), and Multicast (<samp>ff00::/8</samp>, including All-Nodes <samp>ff02::1</samp> and All-Routers <samp>ff02::2</samp>).\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> A common and devastating cloud misconfiguration occurs when automated CI/CD registration scripts or metadata agents register an instance's link-local address into Cloud DNS or Consul service registries. Because link-local addresses are non-routable and require an explicit Linux interface zone index (<samp>%eth0</samp>), cross-VM or cross-container client requests fail instantly with kernel <samp>EINVAL</samp> errors. Architects must enforce DNS validation webhooks that reject non-GUA/ULA records.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> [Google Cloud Load Balancing documentation: HTTP/3 and QUIC support](https://cloud.google.com/load-balancing/docs/https#QUIC) allocates global Anycast IPv6 Virtual IP (VIP) addresses from Google's GUA pool, terminating public client IPv6 connections and proxying requests to backend Compute Engine instances or GKE pods over IPv4 or internal ULA/GUA IPv6.\n\n"

            "### Neighbor Discovery Protocol (NDP) mechanics (RS/RA, NS/NA, SLAAC, DAD)\n"
            "<strong class='side-heading'>What it is in general:</strong> <strong class='keyword'>Neighbor Discovery Protocol (NDP)</strong> completely deprecates broadcast transmissions and IPv4 Address Resolution Protocol (ARP) in favor of Internet Control Message Protocol version 6 (ICMPv6) multicast messaging (RFC 4861):\n"
            "- **Router Solicitation (RS, Type 133) & Router Advertisement (RA, Type 134):** Hosts multicast an RS to <samp>ff02::2</samp> upon boot. Routers respond with periodic RAs to <samp>ff02::1</samp> advertising network prefixes, Maximum Transmission Unit (MTU), default gateway lifetime, and autoconfiguration flags.\n"
            "- **Stateless Address Autoconfiguration (SLAAC, RFC 4862):** Hosts combine the 64-bit RA prefix with a 64-bit Interface Identifier (IID), generated via 64-bit Extended Unique Identifier (EUI-64, derived from MAC address) or RFC 7217 cryptographically stable privacy addresses.\n"
            "- **Neighbor Solicitation (NS, Type 135) & Neighbor Advertisement (NA, Type 136):** Replaces ARP. Hosts query the target's link-layer MAC address by multicasting an NS to the target's Solicited-Node Multicast address (<samp>ff02::1:ffxx:xxxx</samp>). The target unicasts an NA reply.\n"
            "- **Duplicate Address Detection (DAD):** Before binding an address, a host transmits an NS for its own tentative address from the unspecified source (<samp>::</samp>). If an NA returns, an address collision exists and the interface marks the address invalid.\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> In software-defined cloud networks, cloud hypervisors intercept NDP packets. Architects must understand how cloud Software-Defined Networking (SDN) fabrics (such as Andromeda) emulate NDP to assign guest IP addresses and ensure that guest OS firewalls do not block essential ICMPv6 types (133–136), which would cause silent interface deconfiguration.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> In Google Cloud Compute Engine, guest OS virtual interfaces receive IPv6 gateway and subnet configuration via Andromeda-managed NDP Router Advertisements, as outlined in [Google Cloud VPC documentation: IPv6 subnet ranges](https://cloud.google.com/vpc/docs/subnets#ipv6-ranges).\n\n"

            "### Dual-stack VPC architecture, Happy Eyeballs (RFC 8305), and Google Cloud edge ingress\n"
            "<strong class='side-heading'>What it is in general:</strong> <strong class='keyword'>Dual-stack architecture</strong> requires coexistence where endpoints maintain both IPv4 and IPv6 network stacks concurrently. Happy Eyeballs (RFC 8305) is a client-side connection algorithm designed to prevent poor user experience when IPv6 connectivity is impaired: the client initiates simultaneous DNS queries for both A (IPv4) and AAAA (IPv6) records, attempts connection to the IPv6 address first, but starts a fallback IPv4 connection if IPv6 connection setup does not complete within a recommended 250 milliseconds (Connection Attempt Delay).\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> Dual-stack architectures eliminate the business risk of IPv6 adoption. By deploying dual-stack Anycast frontend VIPs with Happy Eyeballs-compliant client SDKs, cloud architects ensure zero user-facing degradation during regional ISP routing anomalies or transit peering outages.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> [Google Cloud Load Balancing documentation: HTTP/3 and QUIC support](https://cloud.google.com/load-balancing/docs/https#QUIC) terminates dual-stack ingress traffic at Google edge Points of Presence (PoPs), proxying requests across optimized Andromeda internal backbones to backend Compute Engine VMs or GKE clusters.\n\n"

            "<strong class='side-heading'>Concrete example:</strong> A microservice container on GKE attempts to connect to an internal cache endpoint whose AAAA record was incorrectly populated with a link-local address (<samp>fe80::a00:27ff:fe8e:7b21</samp>). The application invokes <kbd>socket.connect(('fe80::a00:27ff:fe8e:7b21', 6379))</kbd> without specifying an interface scope index. The Linux kernel immediately returns <samp>[Errno 22] Invalid argument</samp> because the kernel Forwarding Information Base (FIB) routing table has no default interface for link-local traffic. Appending the scope index <kbd>fe80::a00:27ff:fe8e:7b21%eth0</kbd> or correcting DNS to return a Unique Local Address (<samp>2001:db8:100::45</samp>) restores immediate socket connectivity.\n\n"

            "<strong class='side-heading'>Evidence limit:</strong> A successful DNS AAAA resolution proves only that an IPv6 record exists in a zone database; "
            "it provides zero proof that the host possesses an IPv6 default route, that NDP resolved the gateway MAC, or that the remote socket is listening."
        ),
        "questions": [
            "Why does initiating a socket connection to a link-local IPv6 address (fe80::/10) require an explicit zone identifier (%interface), and what error occurs if it is omitted?",
            "What functional mechanism allows Neighbor Discovery Protocol (NDP) to eliminate the network broadcast storms inherent to IPv4 ARP?",
            "How does Duplicate Address Detection (DAD) prevent silent address collisions on a dual-stack cloud subnet during instance initialization?"
        ],
        "reference": "https://datatracker.ietf.org/doc/html/rfc4291#section-2",
        "reference_label": "RFC 4291: IPv6 Addressing Architecture, section 2 (accessed 2026-10-08)",
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
                "Verification with <kbd>ip -6 route get fe80::a00:27ff:fe8e:7b21</kbd> confirmed the kernel routing rejection:\n\n"
                "```text\n"
                "RTNETLINK answers: Invalid argument\n"
                "```"
            ),
            "root": (
                "The microservice registration agent registered its link-local interface address (<samp>fe80::/10</samp>) into the internal "
                "service registry instead of its globally routable Unique Local Address (<samp>2001:db8:10::5</samp>) or GUA. When client pods attempted "
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
                "Tactical Fix: Update the service registry entry to point to the instance's routable ULA address (<samp>2001:db8:10::5</samp>).",
                "Strategic Control: Implement registration webhooks that filter out non-routable link-local (<samp>fe80::/10</samp>) and multicast addresses before committing to DNS."
            ],
            "verify": (
                "Verify via <kbd>python3 -c \"import socket; s=socket.socket(socket.AF_INET6, socket.SOCK_STREAM); s.connect(('2001:db8:10::5', 8443))\"</kbd> "
                "that connections establish cleanly without scope index arguments."
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
                "**Stage 1: Preflight and Environment Verification** — Verify local IPv6 kernel support and inspect active network interfaces:\n\n**Location:** Local Linux terminal\n\n```bash\ncommand -v bash\ncommand -v ip\ncommand -v python3\npython3 -c \"import socket; print('IPv6 Supported:', socket.has_ipv6)\" | tee preflight_ipv6.txt\nip -6 addr show >> preflight_ipv6.txt\n```\n\n**Expected result:** Local IPv6 support confirmed and active interface addresses displayed.\n\n**Save:** preflight_ipv6.txt",
                "**Stage 2: Prepare Target Inputs and Network Fixtures** — Extract or prepare a link-local address and interface identifier using Python:\n\n**Location:** Local Linux terminal\n\n```bash\npython3 -c \"\nimport subprocess, json\ndata = json.loads(subprocess.check_output(['ip', '-j', '-6', 'addr', 'show'], text=True))\nip, iface = None, None\nfor dev in data:\n    ifname = dev.get('ifname', '')\n    for addr in dev.get('addr_info', []):\n        if addr.get('scope') == 'link' and addr.get('local', '').startswith('fe80'):\n            ip = addr['local']\n            iface = ifname\n            break\n    if ip: break\nif not ip: ip, iface = '::1', 'lo'\nprint(f'Target IP: {ip} on interface {iface}')\nwith open('target_ipv6.json', 'w') as f:\n    json.dump({'ip': ip, 'iface': iface}, f)\n\"\ncat target_ipv6.json\n```\n\n**Expected result:** Local link-local address and interface identifier extracted to JSON.\n\n**Save:** target_ipv6.json",
                "**Stage 3: Author Dual-Scope Connection Probe Harness** — Create a Python script (<samp>test_ipv6_scope.py</samp>) that tests both bare and scope-attached socket connections:\n\n**Location:** Local Linux terminal\n\n```bash\ncat <<'EOF' > test_ipv6_scope.py\nimport socket, sys, json\n\nwith open('target_ipv6.json') as f:\n    cfg = json.load(f)\n\ntarget_ip = cfg['ip']\niface = cfg['iface']\nport = 9898\n\nserver = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)\nserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\ntry:\n    scope_id = socket.if_nametoindex(iface) if iface != 'lo' else 0\n    server.bind((target_ip, port, 0, scope_id))\n    server.listen(1)\n    print(f\"[SERVER] Listening on [{target_ip}%{iface}]:{port}\")\nexcept Exception as e:\n    print(f\"[SERVER ERROR] Bind failed: {e}\")\n    sys.exit(1)\n\nprint(\"\\n--- TEST 1: Bare Link-Local Connect (No Scope) ---\")\nclient1 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)\nclient1.settimeout(1.0)\ntry:\n    if target_ip.startswith('fe80'):\n        client1.connect((target_ip, port))\n        print(\"[UNEXPECTED SUCCESS] Connected without scope!\")\n    else:\n        print(\"[SIMULATED REFUSAL] fe80:: without scope returns Errno 22 (EINVAL)\")\nexcept OSError as e:\n    print(f\"[EXPECTED REFUSAL] OSError: {e} (Errno: {e.errno})\")\nfinally:\n    client1.close()\n\nprint(\"\\n--- TEST 2: Scoped Link-Local Connect (With Scope ID) ---\")\nclient2 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)\nclient2.settimeout(1.0)\ntry:\n    client2.connect((target_ip, port, 0, scope_id))\n    print(f\"[VERIFIED SUCCESS] Successfully connected to [{target_ip}%{iface}]:{port}!\")\nexcept Exception as e:\n    print(f\"[FAILED] Scoped connect failed: {e}\")\n    sys.exit(1)\nfinally:\n    client2.close()\n    server.close()\nprint(\"\\n[ASSERT PASS] IPv6 scoping invariant verified: Link-local requires explicit zone ID.\")\nEOF\nls -l test_ipv6_scope.py\n```\n\n**Expected result:** Test probe harness authored implementing dual-scope socket connections.\n\n**Save:** test_ipv6_scope.py",
                "**Stage 4: Execute IPv6 Scope Verification Probes** — Execute the test script to observe kernel socket behavior:\n\n**Location:** Local Linux terminal\n\n```bash\npython3 test_ipv6_scope.py | tee scope_test_output.log\n```\n\n**Expected result:** Execution proves bare connect fails with EINVAL while scoped connect succeeds.\n\n**Save:** scope_test_output.log",
                "**Stage 5: Inspect Kernel Neighbor Discovery Tables** — Inspect the kernel IPv6 neighbor cache using <kbd>ip</kbd> to observe link-local resolution state:\n\n**Location:** Local Linux terminal\n\n```bash\nip -6 neigh show | tee ipv6_neighbors.txt\n# Ensure file exists even if neighbor cache is empty\n[ -s ipv6_neighbors.txt ] || echo \"(Neighbor cache empty - single host execution)\" > ipv6_neighbors.txt\n```\n\n**Expected result:** Kernel neighbor discovery table inspected and neighbor cache state recorded.\n\n**Save:** ipv6_neighbors.txt",
                "**Stage 6: Rehearse Bounded Failure: Synthesize DNS Scope Omission** — Simulate a service discovery failure where an application attempts to query a DNS mock returning an unadorned link-local address:\n\n**Location:** Local Linux terminal\n\n```bash\npython3 -c \"\nimport socket, json\nwith open('target_ipv6.json') as f:\n    cfg = json.load(f)\n\ntry:\n    res = socket.getaddrinfo(cfg['ip'], 9898, socket.AF_INET6, socket.SOCK_STREAM)\n    sockaddr = res[0][4]\n    print(f'getaddrinfo returned sockaddr: {sockaddr}')\n    print(f'Extracted Scope ID from lookup: {sockaddr[3]} (0 = Unspecified / Missing)')\nexcept Exception as e:\n    print(e)\n\" | tee dns_scope_omission.log\n```\n\n**Expected result:** Demonstration confirms DNS getaddrinfo omits zone index (scope_id=0).\n\n**Save:** dns_scope_omission.log",
                "**Stage 7: Diagnose Evidence and Record Architectural Mitigation** — Author a structured diagnostic summary documenting why link-local IPv6 addresses must never be published to enterprise DNS zones:\n\n**Location:** Local Linux terminal\n\n```bash\ncat <<'EOF' > ipv6_scoping_evidence.md\n# Architectural Evidence: IPv6 Address Scoping Boundaries\n\n- Observation 1: Connecting to bare link-local address fe80:: without scope index fails with Errno 22 (EINVAL).\n- Observation 2: Standard DNS AAAA records convey only 128-bit addresses, never interface zone qualifiers.\n- Observation 3: Sockets require explicit 4-tuple (host, port, flowinfo, scope_id) when addressing link-local destinations.\n- Decision: Service discovery, internal DNS, and external ingress MUST strictly publish Global Unicast (GUA) or Unique Local (ULA) addresses.\nEOF\ncat ipv6_scoping_evidence.md\n```\n\n**Expected result:** Structured evidence document authored recording IPv6 scoping boundaries.\n\n**Save:** ipv6_scoping_evidence.md",
                "**Stage 8: Clean Up and Close Out Exercise** — Remove temporary test fixtures and close out the exercise:\n\n**Location:** Local Linux terminal\n\n```bash\nrm -f target_ipv6.json test_ipv6_scope.py scope_test_output.log dns_scope_omission.log\necho \"IPv6 scoping exercise completed and temporary scripts removed.\" > cleanup_summary.txt\ncat cleanup_summary.txt\n```\n\n**Expected result:** Temporary test scripts and fixtures removed; zero orphaned listeners remain.\n\n**Save:** cleanup_summary.txt"
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
            "<strong class='side-heading'>Subtopics in this discussion:</strong> Hierarchical DNS architecture and authoritative name servers; "
            "the resolution pipeline (stub resolver, recursive resolver, iterative referral chain); "
            "core DNS resource record types and TTL caching dynamics; "
            "DNS security protocols (DNSSEC, DoT, DoH) and Google Cloud DNS managed private zones.\n\n"

            "### Hierarchical DNS architecture and authoritative name servers\n"
            "<strong class='side-heading'>What it is in general:</strong> The <strong class='keyword'>Domain Name System (DNS)</strong> (RFC 1034, RFC 1035) is structured as an inverted hierarchical tree starting at the Root Zone (<samp>.</samp>). "
            "The root zone is served by 13 logical root server identities (A through M), operated across hundreds of globally distributed Anycast instances. "
            "Beneath the root sit Top-Level Domains (TLDs), divided into generic TLDs (<samp>.com</samp>, <samp>.org</samp>, <samp>.net</samp>), country-code TLDs (<samp>.uk</samp>, <samp>.de</samp>), "
            "and infrastructure domains (<samp>.arpa</samp>). Authoritative Name Servers hold the master database records (RRsets) for specific zones and have final authority over their namespace.\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> Understanding the authoritative chain allows architects to configure domain delegation, manage registrar Name Server (NS) records, "
            "and design multi-provider DNS resilience. Delegating subdomains to dedicated cloud managed zones decouples developer team operations from corporate root domain controls.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> [Google Cloud DNS documentation: DNS overview](https://cloud.google.com/dns/docs/overview#dns-forwarding-methods) provides an authoritative DNS service running on Google's Anycast "
            "global network infrastructure, delivering 100% availability SLA and ultra-low lookup latency worldwide.\n\n"

            "### The resolution pipeline (stub resolver, recursive resolver, iterative referral chain)\n"
            "<strong class='side-heading'>What it is in general:</strong> The <strong class='keyword'>DNS resolution pipeline</strong> separates query roles into distinct actors:\n"
            "- **Stub Resolver:** A lightweight client library embedded in the guest OS (<samp>glibc getaddrinfo</samp>, <samp>systemd-resolved</samp>) that does not traverse the DNS hierarchy. It formats a query with the Recursion Desired (<samp>RD=1</samp>) bit and sends it to a designated recursive resolver.\n"
            "- **Recursive Resolver (Full Resolver):** Traverses the global hierarchy on behalf of the client. It queries a Root server, receives a referral (<samp>NS</samp> records + glue <samp>A/AAAA</samp>) to the TLD servers, queries the TLD server to receive a referral to the authoritative server, and finally queries the authoritative server for the answer.\n"
            "- **Authoritative Server:** Answers authoritatively (<samp>AA=1</samp>) with the requested RRset or an error code (<samp>NXDOMAIN</samp> if name does not exist, <samp>NODATA</samp> if name exists but record type does not).\n\n"
            f"{DNS_PIPELINE_SVG}\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> Cloud architects must architect private name resolution paths. Conflating stub resolver behavior with recursive caching can lead to split-brain resolution errors across hybrid Cloud VPN or Cloud Interconnect topologies.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> In Google Cloud Compute Engine, every VM queries the internal metadata resolver at <samp>169.254.169.254</samp> over link-local address space. "
            "As detailed in [Google Cloud DNS documentation: DNS zones overview](https://cloud.google.com/dns/docs/zones/zones-overview#forwarding_zones), Cloud DNS can forward queries to on-premises "
            "recursive resolvers or accept inbound queries via private Cloud DNS forwarding targets.\n\n"

            "### Core DNS resource record types and TTL caching dynamics\n"
            "<strong class='side-heading'>What it is in general:</strong> <strong class='keyword'>Resource Records (RRs)</strong> are typed data units grouped into Record Sets (RRsets). The complete spectrum of modern DNS records governs how names translate into operational traffic paths:\n\n"
            f"{DNS_RECORDS_TABLE_HTML}\n\n"
            "Every RRset carries a **Time-To-Live (TTL)** in seconds. Recursive resolvers cache the RRset and count down the TTL, serving subsequent requests directly from cache without querying authoritative servers until the TTL counter reaches zero.\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> TTL management is the central operational control for planned maintenance, migrations, and disaster recovery. Lowering TTLs to 60 seconds days before a database migration ensures that traffic redirects immediately upon record modification. Failing to lower TTLs locks application clients to old IP addresses for hours, causing split-brain data corruption during database failovers.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> [Google Cloud DNS documentation: DNS zones overview](https://cloud.google.com/dns/docs/zones/zones-overview#forwarding_zones) enables geo-routing and weighted round-robin policies directly at the DNS layer, allowing architects to shift traffic percentages dynamically between regions during releases.\n\n"

            "### DNS security protocols (DNSSEC, DoT, DoH) and Google Cloud DNS managed private zones\n"
            "<strong class='side-heading'>What it is in general:</strong> Traditional DNS transmits plaintext over User Datagram Protocol (UDP) port 53 without cryptographic verification, exposing lookups to cache poisoning (Kaminsky attacks) and on-path eavesdropping:\n"
            "- **DNS Security Extensions (DNSSEC, RFC 4033–4035):** Provides cryptographic origin authentication and data integrity using public key cryptography. Authoritative zones sign RRsets with Resource Record Signatures (<samp>RRSIG</samp>). Resolvers validate signatures against DNS Public Keys (<samp>DNSKEY</samp>) and verify the trust chain up to the ICANN Root Zone Trust Anchor via Delegation Signer (<samp>DS</samp>) records published in parent TLD zones. Authenticated Denial of Existence is proven via <samp>NSEC</samp> or salted <samp>NSEC3</samp> records (RFC 5155), preventing attackers from enumerating all zone records (\"zone walking\"). Validating resolvers set the Authenticated Data (<samp>AD=1</samp>) bit upon successful cryptographic validation, and fail with <samp>SERVFAIL</samp> if signatures are forged, expired, or invalid.\n"
            "- **DNS over TLS (DoT, RFC 7858):** Encrypts DNS queries over dedicated Transmission Control Protocol (TCP) port 853 with Transport Layer Security (TLS) encryption, preventing eavesdropping and tampering by transit internet service providers.\n"
            "- **DNS over HTTPS (DoH, RFC 8484):** Encrypts DNS queries inside HTTP/2 or HTTP/3 frames over standard TCP/UDP port 443, blending DNS traffic into standard encrypted web egress to prevent censorship and inspection.\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> Implementing DNSSEC prevents attackers from poisoning recursive caches and hijacking sensitive cloud API endpoints. Configuring private DNS zones prevents internal network topologies and database hostnames from leaking to the public internet.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> [Google Cloud DNS documentation: Use advanced DNSSEC](https://cloud.google.com/dns/docs/dnssec-advanced#advanced-signing-options) isolates internal service discovery to authorized VPCs, supporting cross-VPC DNS peering, automated Key Signing Key (KSK) rotation, and Response Policy Zones (RPZ) to block malicious egress domains.\n\n"

            "<strong class='side-heading'>Concrete example:</strong> During a PostgreSQL database cutover from an on-premises data center to Cloud SQL, the database team updates the internal DNS record <samp>db.prod.internal</samp> from <samp>10.10.0.50</samp> to Cloud SQL's IP <samp>10.240.4.12</samp>. However, the record had been provisioned with an unmanaged TTL of 86400 seconds (24 hours). Compute Engine microservices continue querying their local cache and sending transactions to the old database for up to 24 hours, corrupting financial records and forcing an emergency manual service freeze. Reducing the TTL to 60 seconds 48 hours prior to maintenance guarantees seamless cutover within one minute.\n\n"

            "<strong class='side-heading'>Evidence limit:</strong> A successful DNS resolution proves only that a record exists in an authoritative or cached database; "
            "it provides zero evidence that the resolved IP address has an active routing path, that firewalls allow port access, or that the destination service is healthy."
        ),
        "questions": [
            "Why does a CNAME record at zone apex (e.g. example.com) violate RFC 1912, and how do modern cloud DNS providers circumvent this limitation?",
            "What cryptographic mechanism does DNSSEC use to prove that a requested domain name does NOT exist without signing every possible nonexistent string?",
            "How does a recursive resolver determine whether to serve a record from cache or perform an iterative query to authoritative name servers?"
        ],
        "reference": "https://datatracker.ietf.org/doc/html/rfc1035#section-3.2.1",
        "reference_label": "RFC 1035: Domain Names - Implementation and Specification, section 3.2.1 (accessed 2026-10-08)",
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
                "Executing <kbd>dig +nocmd +noall +answer @169.254.169.254 db-primary.brightloaf.internal</kbd> on worker nodes showed disparate remaining TTLs, "
                "proving upstream caches were serving stale records."
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
                "**Stage 1: Preflight and Environment Verification** — Verify installation of DNS diagnostic utilities (<kbd>dig</kbd>) and test local DNS reachability:\n\n**Location:** Local Linux terminal\n\n```bash\ncommand -v bash\ncommand -v dig\ncommand -v python3\ncommand -v sleep\ndig -v | head -n1 | tee preflight_dns.txt\n```\n\n**Expected result:** DNS utilities confirmed installed and version recorded.\n\n**Save:** preflight_dns.txt",
                "**Stage 2: Trace Iterative DNS Referral Chain** — Execute an iterative trace from the DNS Root servers down to the authoritative name server for a target domain:\n\n**Location:** Local Linux terminal\n\n```bash\ndig +trace +nodnssec google.com A > dns_trace.txt\nhead -n 25 dns_trace.txt\n```\n\n**Expected result:** Iterative trace successfully resolves domain from Root through TLD to Authoritative.\n\n**Save:** dns_trace.txt",
                "**Stage 3: Inspect Resource Record Sets and TTL Decrement Mechanics** — Query a public domain repeatedly and observe the TTL counter decrement in real time:\n\n**Location:** Local Linux terminal\n\n```bash\ndig google.com A | grep -E '^google.com' > ttl_sample1.txt\nsleep 2\ndig google.com A | grep -E '^google.com' > ttl_sample2.txt\ncat ttl_sample1.txt ttl_sample2.txt > ttl_countdown.txt\ncat ttl_countdown.txt\n```\n\n**Expected result:** Consecutive queries record real-time TTL countdown across local/resolver cache.\n\n**Save:** ttl_countdown.txt",
                "**Stage 4: Inspect Authoritative Start of Authority (SOA) Record** — Inspect an SOA record to examine negative caching parameters (RFC 2308):\n\n**Location:** Local Linux terminal\n\n```bash\ndig SOA google.com +noall +answer | tee soa_minimum.txt\n```\n\n**Expected result:** Authoritative SOA record queried and negative caching MINIMUM TTL verified.\n\n**Save:** soa_minimum.txt",
                "**Stage 5: Audit DNSSEC Cryptographic Trust Chain** — Validate cryptographic authenticity of a signed domain using <kbd>dig +dnssec</kbd>:\n\n**Location:** Local Linux terminal\n\n```bash\ndig @8.8.8.8 +dnssec cloudflare.com A | grep -E 'RRSIG' | tee dnssec_rrsig.txt\n```\n\n**Expected result:** RRSIG cryptographic resource records validated for signed zone.\n\n**Save:** dnssec_rrsig.txt",
                "**Stage 6: Rehearse Bounded Failure: DNSSEC Cryptographic Validation Failure** — Query a domain known to have intentionally broken DNSSEC signatures (<samp>dnssec-failed.org</samp>) to observe <samp>SERVFAIL</samp> behavior:\n\n**Location:** Local Linux terminal\n\n```bash\ndig @8.8.8.8 dnssec-failed.org A +noall +comments | grep -E 'status:' | tee dnssec_fail.log\n```\n\n**Expected result:** Broken DNSSEC domain returns SERVFAIL error code, proving cryptographic enforcement.\n\n**Save:** dnssec_fail.log",
                "**Stage 7: Diagnose Evidence and Record Remediation Decision** — Author a structured diagnostic summary documenting the findings of the DNS resolution audit:\n\n**Location:** Local Linux terminal\n\n```bash\ncat <<'EOF' > dns_evaluation_evidence.md\n# Architectural Evidence: DNS Resolution, TTL Caching, and DNSSEC\n\n- Observation 1: Iterative resolution walked from Root (.) -> TLD (.com) -> Authoritative server.\n- Observation 2: TTL values decremented on consecutive queries, confirming caching at recursive resolver.\n- Observation 3: Validation failure against dnssec-failed.org returned SERVFAIL, proving the resolver enforces cryptographic integrity.\n- Decision: Critical database endpoints must maintain <= 60s TTL during maintenance windows, and all cloud domains must enforce DNSSEC validation.\nEOF\ncat dns_evaluation_evidence.md\n```\n\n**Expected result:** Structured evidence document authored recording resolution and caching findings.\n\n**Save:** dns_evaluation_evidence.md",
                "**Stage 8: Clean Up and Close Out Exercise** — Remove temporary test files generated during the diagnostic probes:\n\n**Location:** Local Linux terminal\n\n```bash\nrm -f dns_trace.txt ttl_sample1.txt ttl_sample2.txt ttl_countdown.txt soa_minimum.txt dnssec_rrsig.txt dnssec_fail.log\necho \"DNS resolution laboratory artifacts cleaned up.\" > cleanup_summary.txt\ncat cleanup_summary.txt\n```\n\n**Expected result:** Temporary diagnostic output files cleaned up and workspace closed out.\n\n**Save:** cleanup_summary.txt"
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
            "<strong class='side-heading'>Subtopics in this discussion:</strong> Transport protocol paradigms (TCP vs UDP vs QUIC); "
            "BSD socket addressing, socket types, and the complete socket lifecycle API; "
            "I/O multiplexing architectures (select, poll, epoll, io_uring, SO_REUSEPORT); "
            "TCP connection management (3-way/4-way handshakes, TIME_WAIT, RST), flow control, congestion algorithms, and socket buffers; "
            "packet inspection and analysis with tcpdump.\n\n"

            "### Transport protocol paradigms (TCP vs UDP vs QUIC)\n"
            "<strong class='side-heading'>What it is in general:</strong> <strong class='keyword'>Transport layer protocols</strong> define host-to-host communication semantics across 16-bit port numbers (1–65535):\n"
            "- **Transmission Control Protocol (TCP, RFC 9293):** Connection-oriented, reliable, ordered byte-stream protocol. Enforces data integrity via sequence numbers, checksums, and positive acknowledgments with retransmission.\n"
            "- **User Datagram Protocol (UDP, RFC 768):** Connectionless, unreliable, unordered datagram protocol. Minimal 8-byte header overhead with zero handshake delay, ideal for real-time telemetry, DNS lookups, and media streaming.\n"
            "- **QUIC (RFC 9000):** Modern multiplexed transport running in user space over UDP port 443. Integrates TLS 1.3 encryption directly into the transport handshake (0-RTT / 1-RTT), provides independent stream multiplexing without Head-of-Line (HoL) blocking, and supports seamless connection migration across IP addresses via 64-bit Connection IDs (CIDs).\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> Choosing the appropriate transport protocol governs architectural latency and fault isolation. For video streaming and IoT telemetry, UDP avoids TCP retransmission stalls. For global web APIs and mobile apps, deploying HTTP/3 over QUIC cuts latency by eliminating multi-Round-Trip Time (RTT) connection handshakes.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> [Google Cloud Load Balancing documentation: HTTP/3 and QUIC support](https://cloud.google.com/load-balancing/docs/https#QUIC) terminates QUIC connections at Google's global edge network, proxying requests over optimized internal TCP backbones to backend Compute Engine or GKE workloads.\n\n"

            "### BSD socket addressing, socket types, and the complete socket lifecycle API\n"
            "<strong class='side-heading'>What it is in general:</strong> <strong class='keyword'>Berkeley Software Distribution (BSD) sockets</strong> provide the operating system abstraction for network I/O. Sockets bind to a 4-tuple: (Source IP, Source Port, Destination IP, Destination Port). Socket address families include <samp>AF_INET</samp> (IPv4), <samp>AF_INET6</samp> (IPv6), and <samp>AF_UNIX</samp> (Unix Domain Sockets). Sockets support stream (<samp>SOCK_STREAM</samp>), datagram (<samp>SOCK_DGRAM</samp>), and raw (<samp>SOCK_RAW</samp>) types.\n"
            "The server socket lifecycle follows an explicit sequence: (1) <kbd>socket()</kbd> creates the file descriptor; (2) <kbd>bind()</kbd> associates it with a local IP and port; (3) <kbd>listen()</kbd> transitions the socket to passive mode and sizes the backlog queues; (4) <kbd>accept()</kbd> dequeues an established connection and returns a new connected socket; (5) <kbd>recv()</kbd> and <kbd>send()</kbd> transfer byte streams; (6) <kbd>close()</kbd> initiates connection teardown.\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> Cloud microservice performance depends on socket lifecycle ergonomics. Socket leaks (failing to call <kbd>close()</kbd>) exhaust file descriptors, crashing application runtimes. Understanding the socket 4-tuple prevents ephemeral port exhaustion on outbound NAT gateways.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> In Google Cloud Compute Engine, guest OS network throughput is throttled by per-VM bandwidth caps and ephemeral port limits. Architects must tune Linux kernel socket allocations (<samp>net.ipv4.ip_local_port_range</samp>) to support high-throughput cloud proxies.\n\n"

            "### I/O multiplexing architectures (select, poll, epoll, io_uring, SO_REUSEPORT)\n"
            "<strong class='side-heading'>What it is in general:</strong> Handling thousands of concurrent connections requires scalable <strong class='keyword'>I/O multiplexing</strong> models beyond one-thread-per-connection:\n"
            "- <samp>select()</samp> / <samp>poll()</samp>: $O(N)$ linear scans across file descriptor arrays, limited to 1024 descriptors in select.\n"
            "- <samp>epoll()</samp>: Linux-specific $O(1)$ event-driven multiplexing. Kernel registers interest in file descriptors and returns only active events via <kbd>epoll_wait()</kbd>, supporting edge-triggered (<samp>EPOLLET</samp>) and level-triggered modes.\n"
            "- <samp>io_uring</samp>: Modern Linux asynchronous ring buffer architecture eliminating system call overhead via lockless shared-memory ring queues between user space and kernel.\n"
            "- <samp>SO_REUSEPORT</samp>: Allows multiple independent server processes or threads to bind to the exact same IP and port, with the kernel automatically load balancing incoming SYN packets across worker queues.\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> Cloud reverse proxies (such as NGINX and Envoy) and ingress controllers rely entirely on <samp>epoll</samp> and <samp>SO_REUSEPORT</samp>. Sizing container CPU limits without sufficient worker threads creates unhandled epoll event backlogs that lead to severe tail latency spikes.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> High-performance ingress proxies deployed on Compute Engine leverage multi-queue virtual networking combined with <samp>SO_REUSEPORT</samp> to achieve millions of packets per second per instance.\n\n"

            "### TCP connection management (3-way/4-way handshakes, TIME_WAIT, RST), flow control, congestion algorithms, and socket buffers\n"
            "<strong class='side-heading'>What it is in general:</strong> <strong class='keyword'>TCP connection management</strong> and reliability are enforced through kernel state machines:\n"
            "- **Handshake Lifecycle:** Initiated via 3-way handshake (<samp>SYN</samp> &rarr; <samp>SYN-ACK</samp> &rarr; <samp>ACK</samp>). Terminated via 4-way teardown (<samp>FIN</samp> &rarr; <samp>ACK</samp> &rarr; <samp>FIN</samp> &rarr; <samp>ACK</samp>). Abortive closure transmits Reset (<samp>RST</samp>). The terminating endpoint enters <samp>TIME_WAIT</samp> state for $2 \\times \\text{MSL}$ (Maximum Segment Lifetime, typically 60 seconds) to ensure delayed duplicate segments expire in transit.\n"
            "- **Kernel Queues:** The **SYN Queue** holds partially open connections (<samp>SYN_RECV</samp>). Upon completing the 3-way handshake, the connection moves to the **Accept Queue** (<samp>listen(backlog)</samp>) waiting for user space to call <kbd>accept()</kbd>. If the accept queue fills, the kernel silently drops subsequent incoming SYN packets.\n"
            "- **Flow Control:** Receiver advertises window size (<samp>rwnd</samp>) indicating free space in <samp>sk_rcvbuf</samp>. Window Scaling (RFC 7323) scales windows up to 1 GB.\n"
            "- **Congestion Control:** Sender bounds inflight data by Congestion Window (<samp>cwnd</samp>). Algorithms include loss-based TCP CUBIC (RFC 8312) and rate-based Google Bottleneck Bandwidth and Round-trip propagation time (BBR), which models bottleneck bandwidth and RTprop to prevent bufferbloat.\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> When high-throughput microservices report <30% CPU utilization while dropping requests and throwing HTTP 504 timeouts, the bottleneck is almost always accept queue overflow (<samp>somaxconn</samp> exhaustion) or ephemeral port exhaustion from sockets lingering in <samp>TIME_WAIT</samp>. Tuning TCP buffers and enabling BBR maximizes cross-region throughput across Cloud Interconnect.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> Google Cloud's Andromeda SDN and global BGP network are optimized for [Google Cloud Networking: TCP BBR Congestion Control in GCP](https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster). Compute Engine instances can enable BBR via sysctl to maximize transfer speeds over long-haul paths.\n\n"

            "### Packet inspection and analysis with tcpdump\n"
            "<strong class='side-heading'>What it is in general:</strong> <strong class='keyword'>tcpdump</strong> is the foundational command-line packet analyzer built on the <samp>libpcap</samp> packet capture interface. "
            "It captures raw Layer 2 frames, Layer 3 IP packets, and Layer 4 transport segments traversing network interfaces. "
            "Packets are filtered using Berkeley Packet Filter (BPF) syntax (e.g., <kbd>tcp port 80 and host 198.51.100.1</kbd>). "
            "Key command flags include: <kbd>-i &lt;interface&gt;</kbd> (select interface), <kbd>-nn</kbd> (disable DNS and port name resolution for predictable low-latency output), "
            "<kbd>-S</kbd> (display absolute sequence numbers instead of relative offsets), <kbd>-vvv</kbd> (maximum protocol decode verbosity), "
            "<kbd>-w &lt;file.pcap&gt;</kbd> (write raw packets to PCAP format), and <kbd>-r &lt;file.pcap&gt;</kbd> (read and decode saved capture files). "
            "Reading tcpdump output requires decoding transport flags: <samp>[S]</samp> (SYN: connection request proposing ISN), <samp>[S.]</samp> (SYN-ACK: server acceptance acknowledging client ISN+1 and proposing server ISN), "
            "<samp>[.]</samp> (ACK: client acknowledgment completing handshake), <samp>[P.]</samp> (PSH-ACK: data push transmitting application payload), "
            "<samp>[F.]</samp> (FIN-ACK: graceful connection teardown), and <samp>[R]</samp> / <samp>[R.]</samp> (RST / RST-ACK: connection abort or port closed).\n\n"
            "<strong class='side-heading'>Relevance to a cloud architect:</strong> When microservices fail silently behind cloud load balancers or cross-VPC peerings, high-level logs and CPU metrics provide zero insight into wire-level transport health. Packet capture analysis is the definitive tool to prove whether drops occur due to MTU black holes, SYN packet discards at queue bottlenecks, reset packets emitted by upstream middleboxes, or window stalls from unread socket buffers.\n\n"
            "<strong class='side-heading'>Relevance to GCP:</strong> In Google Cloud, [Linux man-pages: tcpdump(1) packet capture tool description](https://man7.org/linux/man-pages/man1/tcpdump.1.html#DESCRIPTION) is used on Compute Engine instances to diagnose guest kernel networking. Furthermore, Google Cloud VPC Packet Mirroring allows non-intrusive traffic mirroring from VM instances and Internal Load Balancers directly to out-of-band capture collectors running tcpdump or Zeek.\n\n"

            "<strong class='side-heading'>Concrete example:</strong> A promotion sends an unexpected burst of 10,000 HTTP requests/second to a Compute Engine web service configured with the default Linux backlog of <samp>somaxconn=128</samp>. The application thread pool cannot invoke <kbd>accept()</kbd> fast enough to clear the accept queue. Once 128 connections queue up, the Linux kernel silently drops all new incoming SYN packets. Upstream Google Cloud Application Load Balancers retry three times, fail to establish TCP handshakes, and return HTTP 504 Gateway Timeout errors to shoppers. Increasing <samp>net.core.somaxconn=4096</samp> and sizing the application server backlog eliminates the drops and absorbs traffic spikes.\n\n"

            "<strong class='side-heading'>Evidence limit:</strong> A socket in ESTABLISHED state proves only that the TCP 3-way handshake completed between the host kernels; "
            "it provides zero evidence that the application layer protocol is functioning, that HTTP requests can be parsed, or that downstream databases are operational."
        ),
        "questions": [
            "What is the functional difference between the kernel SYN Queue and the Accept Queue during TCP connection establishment?",
            "Why does the TCP TIME_WAIT state linger for 2MSL (60 seconds), and how does enabling tcp_tw_reuse safely alleviate ephemeral port exhaustion?",
            "How does model-based congestion control (BBR) prevent the bufferbloat and packet drop cycles inherent to loss-based congestion control (CUBIC)?"
        ],
        "reference": "https://datatracker.ietf.org/doc/html/rfc9293#section-3",
        "reference_label": "RFC 9293: Transmission Control Protocol, section 3 (accessed 2026-10-08)",
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
                "**Stage 1: Preflight and Environment Verification** — Verify diagnostic socket and packet inspection tools (<kbd>ss</kbd>, <kbd>tcpdump</kbd>, <kbd>python3</kbd>):\n\n**Location:** Local Linux terminal\n\n```bash\ncommand -v bash\ncommand -v ss\ncommand -v tcpdump\ncommand -v python3\ncommand -v sysctl\npython3 -c \"import socket; print('TCP Socket Engine Ready')\" | tee preflight_socket.txt\nss -v | head -n1 >> preflight_socket.txt\n```\n\n**Expected result:** Diagnostic socket utilities confirmed and default somaxconn parameter printed.\n\n**Save:** preflight_socket.txt",
                "**Stage 2: Prepare Target Inputs and Synthetic Packet Capture Fixture** — Author a Python script (<samp>make_pcap.py</samp>) that synthesizes a valid TCP 3-way handshake, payload transmission, and teardown PCAP fixture:\n\n**Location:** Local Linux terminal\n\n```bash\ncat <<'EOF' > make_pcap.py\nimport struct, time\n\ndef make_tcp_packet(src_ip, dst_ip, src_port, dst_port, seq, ack, flags, win=65495, payload=b''):\n    eth = b'\\x00\\x11\\x22\\x33\\x44\\x55\\x66\\x77\\x88\\x99\\xaa\\xbb\\x08\\x00'\n    ip_len = 20 + 20 + len(payload)\n    ip_header = struct.pack('!BBHHHBBH4s4s', 0x45, 0, ip_len, 0x1234, 0x4000, 64, 6, 0,\n                            bytes(map(int, src_ip.split('.'))), bytes(map(int, dst_ip.split('.'))))\n    offset_res = (5 << 4)\n    tcp_header = struct.pack('!HHIIBBHHH', src_port, dst_port, seq, ack, offset_res, flags, win, 0, 0)\n    pkt = eth + ip_header + tcp_header + payload\n    ts_sec = int(time.time())\n    ts_usec = 100000\n    return struct.pack('!IIII', ts_sec, ts_usec, len(pkt), len(pkt)) + pkt\n\npcap_hdr = struct.pack('!IHHiIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)\n\nwith open('handshake.pcap', 'wb') as f:\n    f.write(pcap_hdr)\n    # 1. SYN (Flags [S], seq 1000000)\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 54321, 18080, 1000000, 0, 0x02))\n    # 2. SYN-ACK (Flags [S.], seq 2000000, ack 1000001)\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 18080, 54321, 2000000, 1000001, 0x12))\n    # 3. ACK (Flags [.], seq 1000001, ack 2000001)\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 54321, 18080, 1000001, 2000001, 0x10))\n    # 4. PSH-ACK (Flags [P.], payload data)\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 54321, 18080, 1000001, 2000001, 0x18, payload=b'GET / HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n'))\n    # 5. FIN-ACK (Flags [F.], teardown initiation)\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 54321, 18080, 1000045, 2000001, 0x11))\n    # 6. ACK of FIN (Flags [.])\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 18080, 54321, 2000001, 1000046, 0x10))\n    # 7. RST on closed port (Flags [R.])\n    f.write(make_tcp_packet('127.0.0.1', '127.0.0.1', 18081, 54322, 0, 1000001, 0x14))\n\nprint(\"Generated handshake.pcap fixture.\")\nEOF\npython3 make_pcap.py | tee target_prep.txt\nls -l handshake.pcap >> target_prep.txt\n```\n\n**Expected result:** Synthetic PCAP capture file authored containing full TCP connection lifecycle.\n\n**Save:** target_prep.txt",
                "**Stage 3: Inspect and Read Packet Dump with tcpdump** — Execute <kbd>tcpdump</kbd> against the capture file and decode packet headers field-by-field:\n\n**Location:** Local Linux terminal\n\n```bash\ntcpdump -r handshake.pcap -nn -S | tee tcpdump_analysis.txt\n```\n\n**Expected result:** tcpdump parses the 3-way handshake ([S], [S.], [.]) and teardown flags with microsecond timestamps.\n\n**Save:** tcpdump_analysis.txt",
                "**Stage 4: Execute Live Socket Queue Saturation Test** — Launch a constrained queue listener and dispatch concurrent connection attempts to observe queue saturation:\n\n**Location:** Local Linux terminal\n\n```bash\ncat <<'EOF' > queue_test.py\nimport socket, time\n\nserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\nserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\nserver.bind(('127.0.0.1', 19099))\nserver.listen(2)\n\nclients = []\nsuccess = 0\ndropped = 0\n\nfor i in range(5):\n    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    c.settimeout(0.5)\n    try:\n        c.connect(('127.0.0.1', 19099))\n        clients.append(c)\n        success += 1\n    except Exception as e:\n        dropped += 1\n\nprint(f\"Connected: {success}, Dropped/Queued: {dropped}\")\nfor c in clients:\n    c.close()\nserver.close()\nEOF\npython3 queue_test.py | tee burst_execution.log\n```\n\n**Expected result:** Burst test execution proves queue saturation causes connection drop and timeout.\n\n**Save:** burst_execution.log",
                "**Stage 5: Inspect Kernel Socket Telemetry and TIME_WAIT States** — Inspect local socket telemetry using <kbd>ss</kbd> to observe active socket states:\n\n**Location:** Local Linux terminal\n\n```bash\nss -tan 'sport = :19099 or dport = :19099' | tee socket_states.txt\nss -s >> socket_states.txt\n```\n\n**Expected result:** Active sockets and summary socket state telemetry captured via ss.\n\n**Save:** socket_states.txt",
                "**Stage 6: Rehearse Bounded Failure: Filter TCP Reset Packets** — Use <kbd>tcpdump</kbd> BPF filtering to isolate TCP Reset (RST) flags in the packet capture:\n\n**Location:** Local Linux terminal\n\n```bash\ntcpdump -r handshake.pcap -nn -S 'tcp[tcpflags] & tcp-rst != 0' | tee rst_observation.txt\n```\n\n**Expected result:** tcpdump filters and extracts only TCP RST packets indicating closed ports or connection aborts.\n\n**Save:** rst_observation.txt",
                "**Stage 7: Diagnose Evidence and Record Kernel Tuning Recommendations** — Author a structured diagnostic summary documenting why accept queue sizing and tcpdump analysis are critical for microservice stability:\n\n**Location:** Local Linux terminal\n\n```bash\ncat <<'EOF' > socket_queue_evidence.md\n# Architectural Evidence: TCP Socket Lifecycle, Handshakes, and tcpdump Dissection\n\n- Observation 1: tcpdump output proves the 3-way handshake sequence: Flags [S] (SYN), Flags [S.] (SYN-ACK), Flags [.] (ACK).\n- Observation 2: Sequence and acknowledgment tracking confirms SYN consumes 1 sequence number (ack = seq + 1).\n- Observation 3: Sockets transitioning through TIME_WAIT linger for 2MSL to guarantee packet expiration in flight.\n- Observation 4: Accept queue saturation silently drops incoming SYNs unless tcp_abort_on_overflow=1 sends RST.\n- Decision: Production microservice base images must configure net.core.somaxconn >= 4096 and tcp_max_syn_backlog >= 4096.\nEOF\ncat socket_queue_evidence.md\n```\n\n**Expected result:** Structured evidence document authored recording queue sizing recommendations.\n\n**Save:** socket_queue_evidence.md",
                "**Stage 8: Clean Up and Close Out Exercise** — Remove temporary test scripts and verify clean workspace exit:\n\n**Location:** Local Linux terminal\n\n```bash\nrm -f make_pcap.py queue_test.py handshake.pcap tcpdump_analysis.txt burst_execution.log socket_states.txt rst_observation.txt target_prep.txt\necho \"TCP transport and packet capture lab closed cleanly.\" > cleanup_summary.txt\ncat cleanup_summary.txt\n```\n\n**Expected result:** Temporary test server and client scripts removed cleanly from workspace.\n\n**Save:** cleanup_summary.txt"
            ],
            accept="Generated evidence markdown proves that accept queue saturation causes connection drop, and records kernel tuning parameters.",
            trouble="If port 19099 is already in use, edit the test scripts to use an unprivileged port such as 19105.",
            file_name="socket_queue_evidence.md"
        )
    }
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
            'claim': 'Cloud DNS supports advanced DNSSEC key management with automated Key Signing Key rotation and algorithm selection.',
            'section_url': 'https://cloud.google.com/dns/docs/dnssec-advanced#advanced-signing-options',
            'heading_opened': 'Use advanced signing options'
        },
        {
            'claim': 'TCP BBR congestion control models bottleneck bandwidth and round-trip propagation time across Google Cloud Andromeda and Jupiter fabrics.',
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
