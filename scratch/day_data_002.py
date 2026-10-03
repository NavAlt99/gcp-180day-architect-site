"""day_data_002.py — Specification for Day 2: IP addressing and packet paths.

Topics:
1. topic-01: OSI and TCP/IP layer models
2. topic-02: IPv4 addressing, private ranges, ARP/NDP and CIDR subnetting
3. topic-03: Packet path from NIC to application socket
4. topic-04: Process communication protocols: IPC, Unix domain sockets, loopback, and network RPCs
"""

import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from scripts.author_engine import render_topology_svg

DAY = 2
WORK_BLOCK = "Days 1–17 — Foundations"

PART1_INTRO = (
    "Day 2 establishes the foundational networking physics and communication boundaries required for enterprise cloud "
    "architecture. Modern distributed systems fail across modular boundaries: a healthy physical link does not guarantee "
    "routable IP packets; a successful Layer 4 TCP 3-way handshake does not imply that an application can parse HTTP/2 frames; "
    "and process communication within a container pod or host behaves radically differently over local Unix domain sockets than "
    "over network loopback interfaces. Today's curriculum traces data from physical transceivers and NIC direct memory access (DMA) "
    "ring buffers through the Linux kernel network subsystem, evaluates IPv4 CIDR bitmask mathematics and RFC 1918 private allocations, "
    "dissects the decoupling between transport-layer reliability and application-layer semantics, and establishes high-performance "
    "inter-process communication (IPC) patterns for container sidecars and microservices."
)

EXIT_SUMMARY = "Four correct ranges with network/broadcast addresses and a labeled next-hop path."

# Part 1 Topics of the Day Canonical HTML
PART1_HTML = """
<article class="topic-card" id="topic-01-overview">
<h3>OSI and TCP/IP layer models</h3>
<p>The OSI 7-layer reference model (ISO/IEC 7498-1) and the 4-layer TCP/IP Internet model (RFC 1122) define modular protocol boundaries, dividing network transmission into physical link framing, network-wide IP packet routing, transport-level host-to-host streams (Layer 4), and application-specific payload semantics (Layer 7). At the Application Layer, the Domain Name System (DNS) provides hierarchical name resolution across Root, TLD, and Authoritative servers using core record types (A, AAAA, CNAME, MX, TXT, SRV, PTR) hardened by DNSSEC, DNS over TLS (DoT), and DNS over HTTPS (DoH). At the Transport Layer, TCP establishes reliable communication through 3-way handshakes, 4-way teardowns, sliding-window flow control, and congestion control algorithms (Tahoe, Reno, CUBIC, BBR), while modern transport evolution introduces QUIC and HTTP/3 over UDP to eliminate transport-level Head-of-Line blocking.</p>
<p><strong>Why today and where it sits:</strong> Day 2 establishes fundamental diagnostic boundaries before exploring DNS configurations, TLS termination, VPC topologies, and Google Cloud Load Balancing. <em>Why this matters for a Cloud Architect:</em> Cloud architects must decisively architect the boundary between Layer 4 passthrough load balancing (such as Google Cloud Network Load Balancer / Maglev, preserving client IP with ultra-low latency and zero TLS offload) and Layer 7 proxying (such as Google Cloud Application Load Balancer / Envoy, enabling path-based routing, Cloud Armor WAF integration, and HTTP/2-to-HTTP/3 protocol negotiation). Conflating these layers leads to catastrophic design flaws—such as configuring pure TCP health checks that mask application-level HTTP 500 crashes, or overlooking MTU mismatch fragmentation across hybrid interconnects.</p>
<p>A cloud load balancer reports green TCP port 443 health checks while backend application runtimes throw unhandled database exceptions and return HTTP 503 error payloads. Rushing to declare an infrastructure routing outage misdirects engineering response while customers experience immediate checkout abandonment and transaction loss.</p>
<p><a href="#topic-01-technical">Technical discussion →</a> <a href="#topic-01-problem">Real-world problem →</a> <a href="#topic-01-lab">Step-by-step lab →</a></p>
</article>

<article class="topic-card" id="topic-02-overview">
<h3>IPv4 addressing, private ranges, ARP/NDP and CIDR subnetting</h3>
<p>IPv4 addressing (RFC 791), Classless Inter-Domain Routing (CIDR, RFC 4632), RFC 1918 private address allocations, and Address Resolution Protocol (ARP, RFC 826) / Neighbor Discovery Protocol (NDP, RFC 4861) govern how endpoints are addressed, partitioned into logical broadcast domains, and routed across physical and cloud software-defined networks. Subnetting borrows host bits to create network prefixes, dividing monolithic networks into bounded broadcast domains and routed zones.</p>
<p><strong>Why today and where it sits:</strong> Day 2 teaches IP allocation and subnet splitting (/24, /20, /16) to prepare architects for designing Google Cloud Virtual Private Cloud (VPC) subnets, Cloud Interconnect peering, and IP address management (IPAM) hierarchies. <em>Why this matters for a Cloud Architect:</em> Enterprise cloud networking is fundamentally constrained by IP allocation. A cloud architect must design non-overlapping RFC 1918 and RFC 6598 CIDR topologies across on-premises data centers, partner extranets, and multi-region VPCs. Under-sizing VPC subnets—especially secondary ranges for GKE Pods and Services—is a fatal architectural mistake requiring destructive, high-downtime cluster teardowns and migrations. Mastery of CIDR bitmath and routing hierarchies ensures hybrid Cloud VPN/Interconnect routing stability and prevents IP exhaustion.</p>
<p>An on-premises data center and a new cloud VPC both provision overlapping 10.100.0.0/16 address blocks across a hybrid Cloud Interconnect link. Packets route symmetrically for local nodes but blackhole silently for cross-environment traffic, halting critical database replication.</p>
<p><a href="#topic-02-technical">Technical discussion →</a> <a href="#topic-02-problem">Real-world problem →</a> <a href="#topic-02-lab">Step-by-step lab →</a></p>
</article>

<article class="topic-card" id="topic-03-overview">
<h3>Packet path from NIC to application socket</h3>
<p>The packet traversal lifecycle maps how an incoming raw frame moves from physical or virtualized network interface cards (NICs) through DMA descriptor rings, hardware interrupts, Linux kernel softIRQs (NAPI), sk_buff allocation, netfilter/iptables packet filtering, IP route lookup, TCP/UDP reassembly, and finally into user-space application socket receive buffers. Endpoints bind to specific combinations of IP addresses and port numbers, utilizing stream, datagram, or raw socket types across the complete socket lifecycle (socket, bind, listen, accept, connect, recv, send, close), orchestrated through high-performance I/O multiplexing primitives (epoll, io_uring) and multi-process concurrency models (SO_REUSEPORT).</p>
<p><strong>Why today and where it sits:</strong> Day 2 completes the packet transmission trace from wire to process, providing the low-level grounding required to debug Compute Engine guest OS bottlenecks, Cloud Load Balancer backend timeouts, and microservice socket exhaustion. <em>Why this matters for a Cloud Architect:</em> A cloud architect sizing Compute Engine instances, selecting virtual NIC drivers (virtio-net vs Google Virtual NIC [gVNIC]), and establishing Tier_1 high-bandwidth network profiles must understand how hardware interrupts and kernel queues process packets. When a high-traffic microservice reports deceptive &lt;30% CPU utilization while dropping requests and logging HTTP 504 timeouts, the bottleneck is almost always Linux kernel softIRQ saturation on core 0, DMA ring buffer exhaustion, or accept queue (somaxconn) drops. Sizing VM instance families and tuning kernel buffers ensures workloads absorb traffic surges without dropping ingress frames.</p>
<p>Virtual machine guest metrics show rising interface receive drops and backlog queue overruns while application CPU utilization remains deceptively under twenty percent. Unacknowledged customer HTTP requests encounter thirty-second gateway timeouts, triggering duplicate API retries that compound cascading backpressure across the entire ordering pipeline.</p>
<p><a href="#topic-03-technical">Technical discussion →</a> <a href="#topic-03-problem">Real-world problem →</a> <a href="#topic-03-lab">Step-by-step lab →</a></p>
</article>

<article class="topic-card" id="topic-04-overview">
<h3>Process communication protocols: IPC, Unix domain sockets, loopback, and network RPCs</h3>
<p>Inter-Process Communication (IPC) protocols govern how operating system processes exchange state, synchronize execution, and transfer data both locally on a single host and across distributed network topologies. Local communication mechanisms include Unix Domain Sockets (AF_UNIX / UDS), network loopback sockets (AF_INET over the lo interface), POSIX shared memory (shm_open), pipes/FIFOs, and message queues, while network communication relies on RPC frameworks such as gRPC and REST.</p>
<p><strong>Why today and where it sits:</strong> Day 2 complements the NIC-to-socket packet journey by examining how processes interact once packets arrive, and how modern microservice patterns (such as Kubernetes pod sidecars, Envoy service mesh, and Cloud SQL Auth Proxy) communicate. <em>Why this matters for a Cloud Architect:</em> Modern cloud-native architectures rely heavily on container sidecars co-located within Kubernetes pods. Squeezing high-throughput traffic through TCP loopback (127.0.0.1) forces every inter-container call through full TCP stack encapsulation, checksum generation, and connection teardown, rapidly exhausting 65,535 ephemeral ports and stalling under TIME_WAIT buildup. A cloud architect designs sidecar communication using Unix Domain Sockets (AF_UNIX) over shared in-memory volumes, slashing serialization latency by 60%, reducing CPU consumption, and eliminating port contention entirely.</p>
<p>A high-throughput container communicating with its Envoy sidecar proxy over loopback TCP exhausts all ephemeral ports and spikes kernel CPU in TIME_WAIT connection management. Switching the sidecar communication protocol to a Unix Domain Socket with shared volume mounts eliminates TCP overhead and restores sub-millisecond response latency.</p>
<p><a href="#topic-04-technical">Technical discussion →</a> <a href="#topic-04-problem">Real-world problem →</a> <a href="#topic-04-lab">Step-by-step lab →</a></p>
</article>
"""

PART2_INTRO = (
    "Architectural analysis of control and data plane boundaries, protocol encapsulation stacks, kernel receive pipelines, "
    "and local vs network process communication mechanics."
)

PART3_INTRO = (
    "Production field cases examining real-world networking breakdowns: transport-layer health check false positives, "
    "asymmetric routing drops across overlapping CIDR blocks, kernel socket queue exhaustion under traffic bursts, "
    "and ephemeral port starvation in container sidecar IPC."
)

PART4_INTRO = (
    "Hands-on local laboratory exercises and tabletop verification procedures executing protocol boundary decoupling, "
    "IPv4 CIDR subnet partitioning, kernel socket queue observation, and Unix domain socket IPC benchmarking."
)

# Part 2 Architectural Comparison and Boundary Matrix Table
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
  <th scope="row">Physical (L1) &amp; Data Link (L2)</th>
  <td>Ethernet Frame (48-bit MAC src/dst, 802.1Q tag, EtherType, CRC/FCS)</td>
  <td>Hardware PHY transceiver, switch ASIC, NIC DMA ring buffer, driver NAPI polling loop</td>
  <td><kbd>ip link show</kbd>, <kbd>ethtool -S &lt;dev&gt;</kbd>, <kbd>arp -an</kbd>, <kbd>ip neigh</kbd></td>
  <td>Carrier loss, CRC/frame alignment errors, ARP resolution timeout, silent driver frame drop</td>
</tr>
<tr>
  <th scope="row">Internet / Network (L3)</th>
  <td>IPv4 Packet (32-bit IP src/dst, TTL, ToS/DSCP, Protocol, Checksum) / IPv6 (128-bit)</td>
  <td>Linux Forwarding Information Base (FIB), IP routing subsystem, netfilter / iptables</td>
  <td><kbd>ip route show</kbd>, <kbd>ip rule</kbd>, <kbd>traceroute -n</kbd>, <kbd>tcpdump -nn -i any icmp</kbd></td>
  <td>Destination Host/Network Unreachable, TTL Expired in Transit, MTU black hole, route flapping</td>
</tr>
<tr>
  <th scope="row">Transport (L4)</th>
  <td>TCP Segment (16-bit Port, Seq/Ack, Flags, Window, MSS) / UDP Datagram / QUIC Packet</td>
  <td>Linux kernel TCP state machine (3-way/4-way handshakes, CUBIC/BBR congestion control, sliding window), <kbd>ksoftirqd</kbd></td>
  <td><kbd>ss -tuan</kbd>, <kbd>netstat -s</kbd>, <kbd>tcptraceroute</kbd>, <kbd>conntrack -L</kbd></td>
  <td>Connection refused (<samp>RST</samp>), SYN queue drop, connection reset by peer, ephemeral port exhaustion</td>
</tr>
<tr>
  <th scope="row">Socket Abstraction &amp; IPC</th>
  <td>Kernel Socket Buffer (<samp>sk_buff</samp>, page cache, <samp>SCM_RIGHTS</samp> fd descriptor)</td>
  <td>BSD Socket API (<kbd>socket</kbd>, <kbd>bind</kbd>, <kbd>listen</kbd>, <kbd>accept</kbd>), <kbd>epoll</kbd>, <kbd>io_uring</kbd>, Unix domain socket handler</td>
  <td><kbd>ss -x -p</kbd>, <kbd>lsof -U</kbd>, <kbd>ls -la /proc/&lt;pid&gt;/fd</kbd>, <kbd>ipcs</kbd></td>
  <td><samp>ECONNREFUSED</samp> (no listener), <samp>ENOENT</samp> (missing socket file), <samp>EACCES</samp> (DAC permission denied), <samp>EAGAIN</samp></td>
</tr>
<tr>
  <th scope="row">Application (L7)</th>
  <td>Application Message (DNS Wire Format, HTTP/1.1, HTTP/2, HTTP/3 QUIC frames, gRPC, TLS 1.3)</td>
  <td>User-space process, DNS resolver stub, Envoy reverse proxy, JVM runtime, Web server worker thread</td>
  <td><kbd>dig +trace</kbd>, <kbd>curl -vvv</kbd>, <kbd>openssl s_client</kbd>, OpenTelemetry traces, Application logs</td>
  <td>DNS NXDOMAIN/SERVFAIL, HTTP 502 Bad Gateway, HTTP 503 Service Unavailable, TLS certificate mismatch</td>
</tr>
</tbody>
</table>
"""

# Day 121 Topology Standard Architecture Diagram with Official Component Icons
ARCH_DIAGRAM = {
    "type": "topology",
    "title": "Day 2 Network Infrastructure & End-to-End Packet Traversal Topology",
    "desc": "Architecture topology mapping OSI and TCP/IP protocol layers, CIDR subnets, next-hop routing, NIC DMA rings, Linux kernel softIRQs, socket queues, and IPC channels.",
    "caption": "Conceptual topology of the IPv4 packet traversal path, protocol layer transitions, kernel socket queues, and IPC channels for Day 2. It illustrates boundaries between hardware NICs, Linux kernel network stack, and user-space sockets; it does not prove physical latency, hardware offload capabilities, or cloud SDN forwarding performance for a live production deployment.",
    "width": 1120,
    "height": 690,
    "layers": [
        {
            "name": "DEMAND & INGRESS EDGE",
            "x": 20,
            "y": 55,
            "w": 1080,
            "h": 92,
            "fill": "#1e3a5f",
            "title_color": "#7dd3fc",
            "desc": "Client Ingress · Anycast PoP · Cloud Armor · VPC Gateway"
        },
        {
            "name": "LINUX KERNEL STACK & COMPUTE RUNTIME",
            "x": 20,
            "y": 185,
            "w": 1080,
            "h": 210,
            "fill": "#064e3b",
            "title_color": "#6ee7b7",
            "desc": "NIC DMA Ring · NAPI / SoftIRQ · Netfilter / FIB · TCP Sockets · UDS IPC"
        },
        {
            "name": "GOVERNANCE & ROUTING INVARIANTS",
            "x": 20,
            "y": 435,
            "w": 1080,
            "h": 115,
            "fill": "#422006",
            "title_color": "#fdba74",
            "desc": "RFC 1918 CIDR Plan · Longest Prefix Match · Verification Gates"
        }
    ],
    "components": [
        {"x": 55, "y": 88, "w": 180, "h": 45, "name": "External Client / API", "detail": "Public IPv4 / IPv6 Egress", "stroke": "#38bdf8", "icon": "../assets/icons/generic/client.svg"},
        {"x": 320, "y": 88, "w": 180, "h": 45, "name": "Google Edge PoP (GFE)", "detail": "Global Anycast BGP VIP", "stroke": "#38bdf8", "icon": "../assets/icons/generic/internet.svg"},
        {"x": 585, "y": 88, "w": 205, "h": 45, "name": "Cloud Armor / L4-L7 LB", "detail": "DDoS Mitigation · WAF Policy", "stroke": "#38bdf8", "icon": "../assets/icons/gcp/legacy/cloud-armor.svg"},
        {"x": 855, "y": 88, "w": 205, "h": 45, "name": "VPC Ingress Gateway", "detail": "Cloud NAT · Andromeda SDN", "stroke": "#38bdf8", "icon": "../assets/icons/gcp/legacy/cloud-nat.svg"},
        {"x": 55, "y": 220, "w": 220, "h": 65, "name": "Physical / Virtual NIC", "detail": "gVNIC · Rx/Tx DMA Rings", "stroke": "#22c55e", "icon": "../assets/icons/generic/endpoint.svg"},
        {"x": 320, "y": 220, "w": 220, "h": 65, "name": "Linux NAPI & SoftIRQ", "detail": "ksoftirqd · netif_receive_skb", "stroke": "#22c55e", "icon": "../assets/icons/generic/queue.svg"},
        {"x": 585, "y": 220, "w": 220, "h": 65, "name": "IP Routing & Netfilter", "detail": "iptables / nft · FIB Lookup", "stroke": "#22c55e", "icon": "../assets/icons/generic/firewall.svg"},
        {"x": 850, "y": 220, "w": 220, "h": 65, "name": "TCP Transport & Sockets", "detail": "SYN/Accept Queues · sk_buff", "stroke": "#22c55e", "icon": "../assets/icons/generic/server.svg"},
        {"x": 160, "y": 320, "w": 260, "h": 52, "name": "Application Service", "detail": "User-Space Process · epoll_wait", "stroke": "#f59e0b", "icon": "../assets/icons/gcp/core/compute-engine.svg"},
        {"x": 460, "y": 320, "w": 260, "h": 52, "name": "Envoy Sidecar Proxy", "detail": "L7 Routing · mTLS · Observability", "stroke": "#f59e0b", "icon": "../assets/icons/generic/endpoint.svg"},
        {"x": 760, "y": 320, "w": 260, "h": 52, "name": "Unix Domain Socket (UDS)", "detail": "AF_UNIX · Zero-Copy IPC Buffer", "stroke": "#f59e0b", "icon": "../assets/icons/generic/server.svg"},
        {"x": 180, "y": 468, "w": 320, "h": 58, "name": "RFC 1918 VPC Subnet Matrix", "detail": "Non-Overlapping Prefixes · IPAM", "stroke": "#fdba74", "icon": "../assets/icons/generic/subnet.svg"},
        {"x": 580, "y": 468, "w": 340, "h": 58, "name": "VPC Routing & Next-Hop Gate", "detail": "Longest Prefix Match · Forwarding Invariant", "stroke": "#fdba74", "icon": "../assets/icons/gcp/legacy/cloud-router.svg"}
    ],
    "flows": [
        {"x1": 235, "y1": 110, "x2": 320, "y2": 110, "label": "HTTPS / TLS", "type": "ok"},
        {"x1": 500, "y1": 110, "x2": 585, "y2": 110, "label": "Anycast dispatch", "type": "ok"},
        {"x1": 790, "y1": 110, "x2": 855, "y2": 110, "label": "SDN route", "type": "ok"},
        {"x1": 145, "y1": 133, "x2": 145, "y2": 220, "label": "L1/L2 frame", "type": "ok"},
        {"x1": 410, "y1": 133, "x2": 410, "y2": 220, "label": "NAPI poll", "type": "ok"},
        {"x1": 687, "y1": 133, "x2": 687, "y2": 220, "label": "IP packet", "type": "ok"},
        {"x1": 960, "y1": 133, "x2": 960, "y2": 220, "label": "TCP payload", "type": "ok"},
        {"x1": 275, "y1": 252, "x2": 320, "y2": 252, "label": "IRQ / NAPI", "type": "ok"},
        {"x1": 540, "y1": 252, "x2": 585, "y2": 252, "label": "sk_buff", "type": "ok"},
        {"x1": 805, "y1": 252, "x2": 850, "y2": 252, "label": "tcp_v4_rcv", "type": "ok"},
        {"x1": 420, "y1": 346, "x2": 460, "y2": 346, "label": "loopback TCP", "type": "warn"},
        {"x1": 720, "y1": 346, "x2": 760, "y2": 346, "label": "AF_UNIX IPC", "type": "ok"},
        {"x1": 340, "y1": 372, "x2": 340, "y2": 468, "label": "CIDR lookup", "type": "ok"},
        {"x1": 750, "y1": 372, "x2": 750, "y2": 468, "label": "next-hop match", "type": "ok"},
        {"x1": 500, "y1": 497, "x2": 580, "y2": 497, "label": "verified FIB", "type": "ok"}
    ],
    "boundaries": [
        {"x": 35, "y": 425, "w": 1045, "h": 135, "label": "VERIFICATION BOUNDARY · ROUTING INVARIANTS & NEXT-HOP INTEGRITY", "color": "#f59e0b"}
    ],
    "probes": [
        {"cx": 248, "cy": 104, "label": "P1: Ingress Rate & Handshake Checkpoint", "color": "#38bdf8"},
        {"cx": 658, "cy": 277, "label": "P2: Kernel Rx-Ring & SoftIRQ Drop Counter", "color": "#22c55e"},
        {"cx": 918, "cy": 492, "label": "P3: Subnet Prefix Match & FIB Invariant Gate", "color": "#f59e0b"}
    ]
}

# Dedicated OSI 7-Layer vs TCP/IP 4-Layer Architecture and Protocol Encapsulation SVG
OSI_TCPIP_SVG = """
<figure class="diagram-container">
<div style="max-width:100%;overflow-x:auto">
<svg viewBox="0 0 1120 680" width="100%" height="auto" role="img" aria-labelledby="d002-osi-title d002-osi-desc" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;">
  <title id="d002-osi-title">OSI 7-Layer Reference Model vs TCP/IP 4-Layer Internet Architecture</title>
  <desc id="d002-osi-desc">Detailed architecture mapping the 7-layer OSI model to the 4-layer TCP/IP Internet model, illustrating Protocol Data Unit encapsulation, addressing demultiplexing keys, user-space versus kernel-space boundaries, Layer 4 versus Layer 7 proxy boundaries, and zero-copy Unix Domain Socket IPC fast paths.</desc>
  <defs>
    <marker id="arr-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/></marker>
    <marker id="arr-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"/></marker>
    <marker id="arr-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 1 L 10 5 L 0 9 z" fill="#f59e0b"/></marker>
    <marker id="arr-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 1 L 10 5 L 0 9 z" fill="#a855f7"/></marker>
    <marker id="arr-pink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 1 L 10 5 L 0 9 z" fill="#ec4899"/></marker>
  </defs>

  <!-- Title Banner -->
  <rect x="20" y="15" width="1080" height="48" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="560" y="34" text-anchor="middle" font-family="monospace" font-size="13" fill="#38bdf8" font-weight="bold">OSI 7-LAYER REFERENCE MODEL (ISO/IEC 7498-1) VS TCP/IP 4-LAYER INTERNET ARCHITECTURE (RFC 1122)</text>
  <text x="560" y="52" text-anchor="middle" font-family="monospace" font-size="9.5" fill="#94a3b8">Protocol Data Units (PDUs), Encapsulation Headers, Demultiplexing Keys, and System Execution Boundaries</text>

  <!-- Lane 1: OSI 7-Layer Model (Left) -->
  <rect x="25" y="70" width="315" height="465" rx="6" fill="#090d16" stroke="#334155" stroke-width="1.5"/>
  <text x="182" y="90" text-anchor="middle" font-family="monospace" font-size="11" fill="#cbd5e1" font-weight="bold">OSI 7-LAYER MODEL</text>

  <!-- OSI Layer 7: Application -->
  <g transform="translate(35, 102)">
    <rect width="295" height="52" rx="4" fill="#0c2033" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="12" y="20" font-family="monospace" font-size="10.5" fill="#38bdf8" font-weight="bold">7. APPLICATION</text>
    <text x="12" y="34" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">HTTP/2, HTTP/3, gRPC, DNS, TLS session</text>
    <text x="12" y="46" font-family="monospace" font-size="8" fill="#7dd3fc">PDU: Application Data / Message</text>
  </g>

  <!-- OSI Layer 6: Presentation -->
  <g transform="translate(35, 160)">
    <rect width="295" height="52" rx="4" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
    <text x="12" y="20" font-family="monospace" font-size="10.5" fill="#818cf8" font-weight="bold">6. PRESENTATION</text>
    <text x="12" y="34" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">Data serialization (Protobuf, JSON), TLS encryption</text>
    <text x="12" y="46" font-family="monospace" font-size="8" fill="#c7d2fe">PDU: Formatted Syntax / Encrypted Data</text>
  </g>

  <!-- OSI Layer 5: Session -->
  <g transform="translate(35, 218)">
    <rect width="295" height="52" rx="4" fill="#2e1065" stroke="#a855f7" stroke-width="1.5"/>
    <text x="12" y="20" font-family="monospace" font-size="10.5" fill="#a855f7" font-weight="bold">5. SESSION</text>
    <text x="12" y="34" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">RPC session synchronization, TLS resumption</text>
    <text x="12" y="46" font-family="monospace" font-size="8" fill="#e9d5ff">PDU: Session Dialog Stream</text>
  </g>

  <!-- OSI Layer 4: Transport -->
  <g transform="translate(35, 276)">
    <rect width="295" height="52" rx="4" fill="#3b0764" stroke="#ec4899" stroke-width="2"/>
    <text x="12" y="20" font-family="monospace" font-size="10.5" fill="#ec4899" font-weight="bold">4. TRANSPORT</text>
    <text x="12" y="34" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">TCP (reliable stream), UDP (datagrams)</text>
    <text x="12" y="46" font-family="monospace" font-size="8" fill="#fbcfe8">PDU: Segment (TCP) / Datagram (UDP) · Port (16-bit)</text>
  </g>

  <!-- OSI Layer 3: Network -->
  <g transform="translate(35, 334)">
    <rect width="295" height="52" rx="4" fill="#451a03" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="12" y="20" font-family="monospace" font-size="10.5" fill="#f59e0b" font-weight="bold">3. NETWORK</text>
    <text x="12" y="34" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">IPv4, IPv6, ICMP, BGP, IPsec routing</text>
    <text x="12" y="46" font-family="monospace" font-size="8" fill="#fde68a">PDU: Packet · IP Address (32-bit / 128-bit)</text>
  </g>

  <!-- OSI Layer 2: Data Link -->
  <g transform="translate(35, 392)">
    <rect width="295" height="52" rx="4" fill="#064e3b" stroke="#10b981" stroke-width="1.5"/>
    <text x="12" y="20" font-family="monospace" font-size="10.5" fill="#10b981" font-weight="bold">2. DATA LINK</text>
    <text x="12" y="34" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">Ethernet 802.3, ARP, NDP, 802.1Q VLAN</text>
    <text x="12" y="46" font-family="monospace" font-size="8" fill="#a7f3d0">PDU: Frame · MAC Address (48-bit EUI-48)</text>
  </g>

  <!-- OSI Layer 1: Physical -->
  <g transform="translate(35, 450)">
    <rect width="295" height="52" rx="4" fill="#083344" stroke="#06b6d4" stroke-width="1.5"/>
    <text x="12" y="20" font-family="monospace" font-size="10.5" fill="#06b6d4" font-weight="bold">1. PHYSICAL</text>
    <text x="12" y="34" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">100G/400G PHY, Fiber Optic Transceivers, Copper</text>
    <text x="12" y="46" font-family="monospace" font-size="8" fill="#a5f3fc">PDU: Bits / Electrical Signal / Photons</text>
  </g>

  <!-- Center Lane: PDU Encapsulation & System Execution Boundaries (Middle) -->
  <rect x="360" y="70" width="400" height="465" rx="6" fill="#090d16" stroke="#334155" stroke-width="1.5"/>
  <text x="560" y="90" text-anchor="middle" font-family="monospace" font-size="11" fill="#cbd5e1" font-weight="bold">ENCAPSULATION &amp; SYSTEM BOUNDARIES</text>

  <!-- PDU Block: Application Payload -->
  <g transform="translate(380, 106)">
    <rect width="360" height="38" rx="4" fill="#0c2033" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="180" y="24" text-anchor="middle" font-family="monospace" font-size="9" fill="#38bdf8" font-weight="bold">[ Application Payload: HTTP/2 Headers + Body ]</text>
  </g>

  <!-- Encapsulation Arrow 1 -->
  <line x1="560" y1="144" x2="560" y2="162" stroke="#818cf8" stroke-width="2" marker-end="url(#arr-purple)"/>
  <text x="635" y="156" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#818cf8">+ TCP Header</text>

  <!-- PDU Block: TCP Segment -->
  <g transform="translate(380, 164)">
    <rect width="105" height="38" rx="3" fill="#3b0764" stroke="#ec4899" stroke-width="1.5"/>
    <text x="52" y="23" text-anchor="middle" font-family="monospace" font-size="8" fill="#ec4899" font-weight="bold">TCP Hdr (20B)</text>
    <rect x="110" width="250" height="38" rx="3" fill="#0c2033" stroke="#38bdf8" stroke-width="1"/>
    <text x="235" y="23" text-anchor="middle" font-family="monospace" font-size="8.5" fill="#38bdf8">[ Application Payload Data ]</text>
    <text x="180" y="47" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#f472b6">TCP Segment (Port Demux: 16-bit Src/Dst)</text>
  </g>

  <!-- Encapsulation Arrow 2 -->
  <line x1="560" y1="214" x2="560" y2="232" stroke="#f59e0b" stroke-width="2" marker-end="url(#arr-amber)"/>
  <text x="635" y="226" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#f59e0b">+ IP Header</text>

  <!-- PDU Block: IP Packet -->
  <g transform="translate(380, 234)">
    <rect width="85" height="38" rx="3" fill="#451a03" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="42" y="23" text-anchor="middle" font-family="monospace" font-size="8" fill="#f59e0b" font-weight="bold">IP Hdr (20B)</text>
    <rect x="90" width="90" height="38" rx="3" fill="#3b0764" stroke="#ec4899" stroke-width="1"/>
    <text x="135" y="23" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#ec4899">TCP Hdr</text>
    <rect x="185" width="175" height="38" rx="3" fill="#0c2033" stroke="#38bdf8" stroke-width="1"/>
    <text x="272" y="23" text-anchor="middle" font-family="monospace" font-size="8" fill="#38bdf8">[ Application Data ]</text>
    <text x="180" y="47" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#fde68a">IPv4 Packet (Routing: 32-bit Src/Dst IP)</text>
  </g>

  <!-- Encapsulation Arrow 3 -->
  <line x1="560" y1="284" x2="560" y2="302" stroke="#10b981" stroke-width="2" marker-end="url(#arr-green)"/>
  <text x="635" y="296" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#10b981">+ Eth Hdr &amp; FCS</text>

  <!-- PDU Block: Ethernet Frame -->
  <g transform="translate(380, 304)">
    <rect width="70" height="38" rx="3" fill="#064e3b" stroke="#10b981" stroke-width="1.5"/>
    <text x="35" y="23" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#10b981" font-weight="bold">Eth Hdr (14B)</text>
    <rect x="74" width="70" height="38" rx="3" fill="#451a03" stroke="#f59e0b" stroke-width="1"/>
    <text x="109" y="23" text-anchor="middle" font-family="monospace" font-size="7" fill="#f59e0b">IP Hdr</text>
    <rect x="148" width="65" height="38" rx="3" fill="#3b0764" stroke="#ec4899" stroke-width="1"/>
    <text x="180" y="23" text-anchor="middle" font-family="monospace" font-size="7" fill="#ec4899">TCP Hdr</text>
    <rect x="217" width="95" height="38" rx="3" fill="#0c2033" stroke="#38bdf8" stroke-width="1"/>
    <text x="264" y="23" text-anchor="middle" font-family="monospace" font-size="7" fill="#38bdf8">[ Data ]</text>
    <rect x="316" width="44" height="38" rx="3" fill="#064e3b" stroke="#10b981" stroke-width="1.5"/>
    <text x="338" y="23" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#10b981" font-weight="bold">FCS (4B)</text>
    <text x="180" y="47" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#6ee7b7">Ethernet Frame (L2 Hop: 48-bit MAC Addresses)</text>
  </g>

  <!-- Boundary Marker 1: User Space vs Kernel Space -->
  <line x1="365" y1="362" x2="755" y2="362" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="5,3"/>
  <rect x="420" y="354" width="280" height="16" rx="2" fill="#1f1218" stroke="#f43f5e" stroke-width="0.8"/>
  <text x="560" y="365" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#f43f5e" font-weight="bold">USER SPACE ⟷ KERNEL SPACE BOUNDARY (syscalls)</text>

  <!-- Boundary Marker 2: Kernel Network Subsystem vs Hardware NIC DMA -->
  <line x1="365" y1="416" x2="755" y2="416" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5,3"/>
  <rect x="420" y="408" width="280" height="16" rx="2" fill="#241a06" stroke="#f59e0b" stroke-width="0.8"/>
  <text x="560" y="419" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#f59e0b" font-weight="bold">KERNEL NET SUBSYSTEM ⟷ HARDWARE NIC (DMA Rings)</text>

  <!-- IPC Fast Path Box -->
  <g transform="translate(380, 442)">
    <rect width="360" height="58" rx="4" fill="#091e2f" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,2"/>
    <text x="180" y="18" text-anchor="middle" font-family="monospace" font-size="9" fill="#38bdf8" font-weight="bold">⚡ UNIX DOMAIN SOCKETS (AF_UNIX) IPC FAST PATH</text>
    <text x="180" y="33" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#cbd5e1">Bypasses L4, L3, L2 entirely · Direct kernel memory copy (sk_buff)</text>
    <text x="180" y="47" text-anchor="middle" font-family="monospace" font-size="8" fill="#22c55e">Zero IP/TCP overhead · Zero port exhaustion · Up to 2.5x throughput</text>
  </g>

  <!-- Lane 2: TCP/IP 4-Layer Architecture (Right) -->
  <rect x="780" y="70" width="315" height="465" rx="6" fill="#090d16" stroke="#334155" stroke-width="1.5"/>
  <text x="937" y="90" text-anchor="middle" font-family="monospace" font-size="11" fill="#cbd5e1" font-weight="bold">TCP/IP 4-LAYER MODEL</text>

  <!-- TCP/IP Layer 4: Application -->
  <g transform="translate(790, 102)">
    <rect width="295" height="166" rx="4" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
    <text x="12" y="22" font-family="monospace" font-size="11" fill="#818cf8" font-weight="bold">APPLICATION LAYER (RFC 1122)</text>
    <text x="12" y="40" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">Consolidates OSI Layers 7, 6, and 5</text>
    <text x="12" y="58" font-family="sans-serif" font-size="8" fill="#94a3b8">• User-space process runtimes and libraries</text>
    <text x="12" y="74" font-family="sans-serif" font-size="8" fill="#94a3b8">• Application protocols: HTTP/1.1, HTTP/2, gRPC, DNS</text>
    <text x="12" y="90" font-family="sans-serif" font-size="8" fill="#94a3b8">• TLS 1.3 handshake and session encryption</text>
    <text x="12" y="106" font-family="sans-serif" font-size="8" fill="#94a3b8">• Object serialization: JSON, Protocol Buffers, Avro</text>
    <rect x="10" y="120" width="275" height="34" rx="3" fill="#0c162d"/>
    <text x="18" y="134" font-family="monospace" font-size="7.5" fill="#38bdf8">PDU: Application Message / Byte Stream</text>
    <text x="18" y="146" font-family="monospace" font-size="7.5" fill="#c7d2fe">Demux Key: URL Path, HTTP Host Header, Method</text>
  </g>

  <!-- TCP/IP Layer 3: Transport -->
  <g transform="translate(790, 276)">
    <rect width="295" height="52" rx="4" fill="#3b0764" stroke="#ec4899" stroke-width="2"/>
    <text x="12" y="20" font-family="monospace" font-size="10.5" fill="#ec4899" font-weight="bold">TRANSPORT LAYER (RFC 9293)</text>
    <text x="12" y="34" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">Maps directly to OSI Layer 4</text>
    <text x="12" y="46" font-family="monospace" font-size="8" fill="#fbcfe8">Demux Key: 16-bit Port (TCP 4-tuple stream)</text>
  </g>

  <!-- TCP/IP Layer 2: Internet -->
  <g transform="translate(790, 334)">
    <rect width="295" height="52" rx="4" fill="#451a03" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="12" y="20" font-family="monospace" font-size="10.5" fill="#f59e0b" font-weight="bold">INTERNET LAYER (RFC 791 / RFC 8200)</text>
    <text x="12" y="34" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">Maps directly to OSI Layer 3</text>
    <text x="12" y="46" font-family="monospace" font-size="8" fill="#fde68a">Demux Key: 32-bit IPv4 / 128-bit IPv6 Address</text>
  </g>

  <!-- TCP/IP Layer 1: Network Access / Link -->
  <g transform="translate(790, 392)">
    <rect width="295" height="110" rx="4" fill="#064e3b" stroke="#10b981" stroke-width="1.5"/>
    <text x="12" y="20" font-family="monospace" font-size="10.5" fill="#10b981" font-weight="bold">NETWORK ACCESS / LINK (RFC 1122)</text>
    <text x="12" y="36" font-family="sans-serif" font-size="8.5" fill="#cbd5e1">Consolidates OSI Layers 2 and 1</text>
    <text x="12" y="52" font-family="sans-serif" font-size="8" fill="#94a3b8">• NIC hardware drivers, DMA Rx/Tx ring buffers</text>
    <text x="12" y="68" font-family="sans-serif" font-size="8" fill="#94a3b8">• Local subnet framing (Ethernet 802.3, ARP, NDP)</text>
    <text x="12" y="84" font-family="sans-serif" font-size="8" fill="#94a3b8">• Physical transceivers, PHY layer signal encoding</text>
    <text x="12" y="100" font-family="monospace" font-size="7.5" fill="#a7f3d0">Demux Key: 48-bit MAC Address / EtherType (0x0800)</text>
  </g>

  <!-- Bottom Panel: Diagnostic & Verification Matrix -->
  <rect x="25" y="545" width="1070" height="118" rx="6" fill="#090d16" stroke="#334155" stroke-width="1"/>
  <text x="40" y="563" font-family="monospace" font-size="10" fill="#94a3b8" font-weight="bold">ARCHITECTURAL DIAGNOSTIC MATRIX &amp; PROXY BOUNDARIES:</text>

  <!-- Card 1: L4 vs L7 Proxy Boundary -->
  <g transform="translate(38, 572)">
    <rect width="250" height="78" rx="3" fill="#121827" stroke="#38bdf8" stroke-width="1"/>
    <image href="../assets/icons/gcp/legacy/cloud-load-balancing.svg" x="8" y="8" width="20" height="20" preserveAspectRatio="xMidYMid meet"/>
    <text x="34" y="18" font-family="monospace" font-size="8.5" fill="#38bdf8" font-weight="bold">L4 VS L7 PROXY BOUNDARY</text>
    <text x="10" y="34" font-family="sans-serif" font-size="8" fill="#cbd5e1">• L4 (NLB/Maglev): 4-tuple TCP dispatch</text>
    <text x="10" y="48" font-family="sans-serif" font-size="8" fill="#cbd5e1">• L4 operates without TLS termination</text>
    <text x="10" y="62" font-family="sans-serif" font-size="8" fill="#cbd5e1">• L7 (ALB/Envoy): URI routing &amp; header auth</text>
    <text x="10" y="74" font-family="sans-serif" font-size="7.5" fill="#94a3b8">L4 green check ≠ L7 application readiness</text>
  </g>

  <!-- Card 2: Demultiplexing Keys -->
  <g transform="translate(300, 572)">
    <rect width="250" height="78" rx="3" fill="#121827" stroke="#ec4899" stroke-width="1"/>
    <image href="../assets/icons/generic/decision.svg" x="8" y="8" width="20" height="20" preserveAspectRatio="xMidYMid meet"/>
    <text x="34" y="18" font-family="monospace" font-size="8.5" fill="#ec4899" font-weight="bold">DEMULTIPLEXING IDENTIFIERS</text>
    <text x="10" y="34" font-family="sans-serif" font-size="8" fill="#cbd5e1">• L7: Host header, URI path, HTTP method</text>
    <text x="10" y="48" font-family="sans-serif" font-size="8" fill="#cbd5e1">• L4: 16-bit Port numbers (1–65535)</text>
    <text x="10" y="62" font-family="sans-serif" font-size="8" fill="#cbd5e1">• L3: 32-bit IPv4 / 128-bit IPv6 address</text>
    <text x="10" y="74" font-family="sans-serif" font-size="7.5" fill="#94a3b8">L2: 48-bit MAC address (EUI-48)</text>
  </g>

  <!-- Card 3: Failure Signals -->
  <g transform="translate(562, 572)">
    <rect width="250" height="78" rx="3" fill="#121827" stroke="#f59e0b" stroke-width="1"/>
    <image href="../assets/icons/generic/failure.svg" x="8" y="8" width="20" height="20" preserveAspectRatio="xMidYMid meet"/>
    <text x="34" y="18" font-family="monospace" font-size="8.5" fill="#f59e0b" font-weight="bold">FAILURE SIGNAL SEPARATION</text>
    <text x="10" y="34" font-family="sans-serif" font-size="8" fill="#cbd5e1">• L7: HTTP 500/502/503, TLS cert error</text>
    <text x="10" y="48" font-family="sans-serif" font-size="8" fill="#cbd5e1">• L4: TCP RST, SYN timeout, port closed</text>
    <text x="10" y="62" font-family="sans-serif" font-size="8" fill="#cbd5e1">• L3: Destination Unreachable, TTL drop</text>
    <text x="10" y="74" font-family="sans-serif" font-size="7.5" fill="#94a3b8">L2: ARP timeout, framing/CRC error</text>
  </g>

  <!-- Card 4: Process Communication IPC -->
  <g transform="translate(824, 572)">
    <rect width="258" height="78" rx="3" fill="#121827" stroke="#22c55e" stroke-width="1"/>
    <image href="../assets/icons/generic/endpoint.svg" x="8" y="8" width="20" height="20" preserveAspectRatio="xMidYMid meet"/>
    <text x="34" y="18" font-family="monospace" font-size="8.5" fill="#22c55e" font-weight="bold">PROCESS IPC MECHANISMS</text>
    <text x="10" y="34" font-family="sans-serif" font-size="8" fill="#cbd5e1">• UDS (AF_UNIX): Node-local, 2.5x speed</text>
    <text x="10" y="48" font-family="sans-serif" font-size="8" fill="#cbd5e1">• Loopback (lo): Localhost TCP, port churn</text>
    <text x="10" y="62" font-family="sans-serif" font-size="8" fill="#cbd5e1">• POSIX shm: Shared memory, futex sync</text>
    <text x="10" y="74" font-family="sans-serif" font-size="7.5" fill="#94a3b8">gRPC/RPC: Strongly typed cross-host API</text>
  </g>
</svg>
</div>
<figcaption>Architectural comparison of the OSI 7-layer reference model (ISO/IEC 7498-1) and the TCP/IP 4-layer Internet model (RFC 1122), illustrating PDU encapsulation progression, demultiplexing identifiers, execution boundaries (user space vs kernel space vs hardware), and the Unix Domain Socket IPC fast path. It defines protocol layer separation; it does not represent vendor-specific hardware ASIC pipelines or cloud SDN virtual overlay implementations.</figcaption>
</figure>
"""

ARCH_SVG_HTML = f"{render_topology_svg(DAY, ARCH_DIAGRAM)}\n\n{OSI_TCPIP_SVG}"

def make_lab(name, goal, expected, steps, accept, trouble, cleanup="No chargeable cloud resources created. All operations execute locally.", file_name=None):
    return {
        "name": name,
        "goal": goal,
        "expected": expected,
        "mode": "local exercise",
        "prereq": "Day 1 local workspace and baseline shell tools.",
        "preflight": "Verify local Python 3 environment, standard Linux diagnostic tools (<kbd>ip</kbd>, <kbd>ss</kbd>), and write permissions in workspace.",
        "steps": steps,
        "accept": accept,
        "verification": "All automated assertions pass with exit code 0 and output artifacts record verifiable architectural invariants.",
        "trouble": trouble,
        "cleanup": cleanup,
        "file": file_name
    }

TOPICS = [
    {
        "key": "topic-01",
        "title": "OSI and TCP/IP layer models",
        "overview": (
            "The OSI 7-layer reference model (ISO/IEC 7498-1) and the 4-layer TCP/IP Internet model (RFC 1122) define modular "
            "architectural boundaries that decouple physical transmission, link-local framing, internetwork IP packet routing, "
            "transport-layer host-to-host streams (Layer 4), and application-level payload semantics (Layer 7). Transport Layer 4 "
            "protocols such as TCP and UDP manage port multiplexing, sequence ordering, sliding-window flow control, and connection "
            "state lifecycles. Application Layer 7 protocols such as HTTP/1.1, HTTP/2, gRPC, and TLS govern message serialization, "
            "request-response transactions, header metadata, and identity validation. Understanding this boundary is critical in enterprise "
            "cloud architecture: it governs the fundamental operational difference between Layer 4 passthrough load balancing "
            "(Google Cloud Network Load Balancing via Maglev) and Layer 7 reverse proxy load balancing (Google Cloud Application Load Balancing "
            "via Envoy), preventing engineers from conflating transport connectivity with application readiness."
        ),
        "preview": (
            "A cloud load balancer reports green TCP port 443 health checks while backend application runtimes throw unhandled database "
            "exceptions and return HTTP 503 error payloads. Rushing to declare an infrastructure routing outage misdirects engineering "
            "response while customers experience immediate checkout abandonment and transaction loss."
        ),
        "technical": (
            "**Subtopics in this discussion:** protocol layer boundaries and encapsulation (OSI 7-layer vs TCP/IP 4-layer); "
            "application layer core services (DNS architecture, hierarchy, record types, DNSSEC, DoT, DoH); "
            "transport layer core protocols (TCP 3-way/4-way handshakes, sliding window, flow and congestion control, UDP); "
            "modern transport evolution (QUIC and HTTP/3).\n\n"

            "### Protocol layer boundaries and encapsulation (OSI 7-layer vs TCP/IP 4-layer)\n"
            "**What it is in general:** The Open Systems Interconnection (OSI) 7-layer model (ISO/IEC 7498-1) and the TCP/IP 4-layer Internet model (RFC 1122) "
            "define modular abstractions so that failures in one domain can be isolated without misattributing fault to adjacent systems. In transmission, "
            "data descends through protocol encapsulation: user-space application messages (Layer 7) are encapsulated with TCP or UDP transport headers (Layer 4) "
            "containing 16-bit port numbers, wrapped in IP internetwork headers (Layer 3) with 32-bit or 128-bit addresses, framed by Ethernet link headers (Layer 2) "
            "with 48-bit MAC addresses and CRC checksums, and transmitted as raw bits over physical media (Layer 1). At each receiving boundary, the OS kernel "
            "decapsulates headers using demultiplexing identifiers (EtherType <samp>0x0800</samp> for IPv4, IP protocol <samp>6</samp> for TCP, and destination port <samp>443</samp> for HTTPS).\n\n"
            "**Relevance to a cloud architect:** Modular boundaries prevent architects from misdiagnosing failure domains. An architect must rigorously distinguish "
            "Layer 4 transport connectivity (TCP handshakes, resets, sliding-window flow control) from Layer 7 application semantics (HTTP status codes, TLS certificates, "
            "URL paths, payload serialization). Conflating these layers leads to severe operational errors—such as diagnosing an infrastructure network outage when "
            "an application throws unhandled exceptions, or trusting a shallow TCP health check while microservices return HTTP 503 errors.\n\n"
            "**Relevance to GCP:** Google Cloud explicitly separates its load balancing tiers along this boundary. As detailed in the "
            "[Google Cloud Load Balancing overview](https://cloud.google.com/load-balancing/docs/load-balancing-overview), Google Cloud provides Layer 4 Passthrough "
            "Network Load Balancers (Maglev-based, preserving client source IP with zero TLS termination and line-rate throughput) versus Layer 7 Application Load "
            "Balancers (Envoy-based, terminating TLS, executing URL path routing, and integrating with Google Cloud Armor for WAF and DDoS security).\n\n"

            "### Application layer core services (DNS architecture, hierarchy, record types, DNSSEC, DoT, DoH)\n"
            "**What it is in general:** The Domain Name System (DNS, RFC 1034 / RFC 1035) is an inverted hierarchical distributed database that resolves "
            "human-readable hostnames to routable network IP addresses. Resolution proceeds from the Root Zone (<samp>.</samp>) through Top-Level Domains (TLDs) "
            "to Authoritative Name Servers. Host stub resolvers query recursive resolvers (such as Google Public DNS <samp>8.8.8.8</samp> or internal metadata DNS "
            "<samp>169.254.169.254</samp>), which execute iterative queries and cache answers within configured Time-To-Live (TTL) intervals. Core records include "
            "<samp>A</samp> (IPv4), <samp>AAAA</samp> (IPv6), <samp>CNAME</samp> (canonical alias), <samp>MX</samp> (mail routing), <samp>TXT</samp> (SPF/DKIM tokens), "
            "<samp>PTR</samp> (reverse IP mapping), and <samp>SRV</samp> (service discovery). DNSSEC (RFC 4033) validates authenticity and integrity via cryptographic "
            "digital signatures (<samp>RRSIG</samp>, <samp>DNSKEY</samp>, <samp>DS</samp>) without query encryption, while DNS over TLS (DoT, RFC 7858) and "
            "DNS over HTTPS (DoH, RFC 8484) encrypt queries to prevent eavesdropping and middlebox tampering.\n\n"
            "**Relevance to a cloud architect:** DNS controls global traffic routing, failover steering, and zero-downtime database cutovers. Stale DNS caching or "
            "excessively long TTLs prolong outages during disaster recovery. An enterprise architect designs multi-region split-horizon resolution, private DNS peering "
            "across hybrid enterprise networks, and DNSSEC validation to prevent cache poisoning attacks.\n\n"
            "**Relevance to GCP:** [Google Cloud DNS overview](https://cloud.google.com/dns/docs/overview) provides 100% SLA authoritative public zones, private "
            "DNS zones for VPCs, cross-VPC DNS peering, outbound forwarding zones to on-premises DNS, and Response Policy Zones (RPZ) for threat intelligence blocking.\n\n"

            "### Transport layer core protocols (TCP 3-way/4-way handshakes, sliding window, flow and congestion control, UDP)\n"
            "**What it is in general:** The Transmission Control Protocol (TCP, RFC 9293) provides a connection-oriented, reliable, ordered byte-stream service. "
            "TCP manages connection lifecycles via a 3-way handshake (<samp>SYN</samp> &rarr; <samp>SYN-ACK</samp> &rarr; <samp>ACK</samp>), sequence and acknowledgment "
            "numbers, a 4-way termination handshake (<samp>FIN</samp> &rarr; <samp>ACK</samp> &rarr; <samp>FIN</samp> &rarr; <samp>ACK</samp>), and abortive resets (<samp>RST</samp>). "
            "Sliding-window flow control bounds unacknowledged inflight bytes by receiver buffer capacity (<samp>rwnd</samp>), scaled up to 1 GB via Window Scaling (RFC 7323). "
            "Congestion control algorithms—including loss-based TCP CUBIC (RFC 8312) and model-based Google BBR—dynamically throttle transmission to prevent bufferbloat "
            "and network collapse. In contrast, UDP (RFC 768) provides lightweight, connectionless, unordered datagrams without flow control or handshakes.\n\n"
            "**Relevance to a cloud architect:** Transport layer behavior directly dictates end-to-end latency and throughput across distributed cloud networks. High Round-Trip "
            "Time (RTT) across trans-oceanic regions exacerbates Slow Start delays and connection establishment latency. Sockets lingering in <samp>TIME_WAIT</samp> "
            "(for $2 \\times \\text{MSL} = 60$ seconds) can exhaust ephemeral ports on busy API gateways. Architects must tune TCP buffer sizes, select congestion algorithms "
            "(e.g. enabling BBR for inter-region data transfers), and implement connection pooling to avoid continuous 3-way handshake penalties.\n\n"
            "**Relevance to GCP:** Google Cloud's Andromeda virtual network and global BGP network are optimized for "
            "[TCP BBR congestion control](https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster), "
            "which prevents queue buildup across Google Cloud Interconnect and Cloud VPN links. Furthermore, Google Cloud Compute Engine guest OS environments allow "
            "tuning TCP window parameters (<samp>tcp_rmem</samp>, <samp>tcp_wmem</samp>) to maximize throughput on Tier_1 high-bandwidth virtual instances.\n\n"

            "### Modern transport evolution (QUIC and HTTP/3)\n"
            "**What it is in general:** Traditional TCP incurs Head-of-Line (HoL) blocking (a single dropped packet stalls all multiplexed streams in HTTP/2) and requires "
            "multiple round trips for connection establishment (1 RTT TCP + 1 RTT TLS 1.3 = 2 RTTs). QUIC (RFC 9000) is a modern transport protocol implemented in user space "
            "atop UDP (port 443). It merges transport and TLS 1.3 cryptographic handshakes into a single round trip (1-RTT, or 0-RTT upon session resumption), supports fully "
            "independent multiplexed streams (packet loss on one stream does not stall other streams), and supports connection migration using 64-bit Connection IDs (CIDs) "
            "rather than IP/port 4-tuples when mobile devices switch between Wi-Fi and cellular networks. HTTP/3 (RFC 9114) maps HTTP semantics directly onto QUIC streams with QPACK header compression (RFC 9204).\n\n"
            "**Relevance to a cloud architect:** For edge applications serving mobile users or high-loss wireless environments, HTTP/3 over QUIC drastically cuts Time-To-First-Byte "
            "(TTFB) and eliminates catastrophic tail latency caused by TCP HoL blocking. Cloud architects designing e-commerce checkouts, streaming media, and global mobile APIs "
            "should terminate HTTP/3 at edge reverse proxies to maximize client-side perceived performance.\n\n"
            "**Relevance to GCP:** [Google Cloud HTTP/3 protocol support](https://cloud.google.com/load-balancing/docs/https#http3-quic) is natively integrated into Google Cloud "
            "External Application Load Balancers and Cloud CDN. Google Front Ends (GFEs) negotiate HTTP/3 over UDP 443 with supported clients using Anycast VIPs while maintaining "
            "optimized HTTP/2 or HTTP/1.1 TCP connections to backend Compute Engine or GKE service instances.\n\n"

            "**Concrete Example:** Consider an e-commerce checkout microservice running on Compute Engine behind a load balancer. If the database connection pool exhausts, the application "
            "throws exceptions and returns HTTP 503 Service Unavailable. If the load balancer is configured with an L4 TCP health check on port 443, the Linux kernel continues to complete "
            "the TCP 3-way handshake (<samp>SYN</samp> &rarr; <samp>SYN-ACK</samp> &rarr; <samp>ACK</samp>), so the load balancer evaluates the backend as 100% healthy and continues routing "
            "thousands of customer orders to failed instances. Configuring an L7 HTTP health check probing <kbd>/healthz</kbd> forces the load balancer to evaluate application HTTP response "
            "codes, promptly marking the backend unhealthy within 10 seconds and redirecting checkout traffic to healthy replicas.\n\n"

            "**Evidence limit:** A successful Layer 4 TCP 3-way handshake verifies only that a kernel socket accepted the connection; it provides zero evidence that the user-space "
            "application thread is unblocked, has active database connections, or is returning valid HTTP payloads."
        ),
        "questions": [
            "How does TCP 3-way handshake sequence number negotiation and sliding-window flow control prevent receiver buffer exhaustion, and what distinguishes an unacknowledged SYN drop from an abortive TCP RST packet?",
            "Why does DNSSEC provide origin authenticity and data integrity for DNS records without encrypting query traffic, and how do DoT and DoH complement DNSSEC to protect user privacy?",
            "What architectural advantage does QUIC's independent stream multiplexing over UDP provide over TCP's single byte-stream model in high-loss wireless or mobile cloud ingress environments?"
        ],
        "reference": "https://www.rfc-editor.org/rfc/rfc9293",
        "reference_label": "RFC 9293: Transmission Control Protocol (accessed 2026-10-02)",
        "scenario": {
            "scenario": (
                "Brightloaf's e-commerce platform deployed an update to the inventory and checkout microservice behind an external "
                "load balancer. Shortly after deployment, customer orders stalled and the incident management channel alerted on high "
                "checkout error rates, yet the infrastructure monitoring dashboard displayed 100% green health check status across all backend instances."
            ),
            "symptom": (
                "Customers attempting to complete cart checkouts received HTTP 503 Service Unavailable errors. The payment gateway dropped "
                "from 3,200 successful orders/minute to 410 orders/minute, while the load balancer continued routing 100% of ingress traffic "
                "to failing backend instances."
            ),
            "impact": (
                "SLO error budget burned at 24x normal baseline. 2,800 checkout transactions failed per minute, resulting in an estimated "
                "$65,000 in lost revenue across a 22-minute operational outage window before mitigation."
            ),
            "constraints": (
                "Zero customer data exposure; maintain PCI-DSS strict tokenization boundary; zero maintenance downtime permitted on the "
                "checkout API during active flash sales."
            ),
            "evidence": (
                "Executing <kbd>curl -vvv https://checkout.brightloaf.internal/api/v1/order</kbd> showed an immediate TCP handshake "
                "followed by an application-level 503 error payload:\n\n"
                "```text\n"
                "*   Trying 10.240.0.45:443...\n"
                "* Connected to checkout.brightloaf.internal (10.240.0.45) port 443 (#0)\n"
                "* ALPN: offers h2,http/1.1\n"
                "* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384\n"
                "> POST /api/v1/order HTTP/1.1\n"
                "> Host: checkout.brightloaf.internal\n"
                "> Content-Type: application/json\n"
                ">\n"
                "< HTTP/1.1 503 Service Unavailable\n"
                "< Content-Type: application/json\n"
                "< Date: Fri, 02 Oct 2026 04:12:08 GMT\n"
                "< Content-Length: 94\n"
                "{\n"
                '  "error": "DATABASE_CONNECTION_POOL_EXHAUSTED",\n'
                '  "detail": "Timed out waiting for database connection after 5000ms"\n'
                "}\n"
                "```\n\n"
                "Inspection of the load balancer health check configuration confirmed a Layer 4 TCP port check:\n\n"
                "```json\n"
                "{\n"
                '  "healthCheck": {\n'
                '    "type": "TCP",\n'
                '    "tcpHealthCheck": {\n'
                '      "port": 443\n'
                "    },\n"
                '    "checkIntervalSec": 5,\n'
                '    "healthyThreshold": 2,\n'
                '    "unhealthyThreshold": 3\n'
                "  }\n"
                "}\n"
                "```"
            ),
            "root": (
                "The health check was configured as a Layer 4 TCP probe against port 443 rather than a Layer 7 HTTP probe against "
                "an authenticated health endpoint (<kbd>/healthz</kbd>). When the microservice's database connection pool became exhausted, "
                "the application runtime was unable to process transactions and returned HTTP 503. However, because the Linux kernel "
                "continued accepting incoming TCP SYN packets and completing 3-way handshakes, the L4 health check evaluated every instance "
                "as completely healthy, leaving impaired instances in the active forwarding pool."
            ),
            "diagnostic_steps": [
                "Step 1: Execute <kbd>curl -iv</kbd> against the backend instance to observe the contrast between TCP handshake success and HTTP response code.",
                "Step 2: Inspect backend instance socket state using <kbd>ss -tan 'sport = :443'</kbd> to confirm the TCP socket state is ESTABLISHED.",
                "Step 3: Query load balancer backend health status via API to determine the health check probe protocol (TCP vs HTTP).",
                "Step 4: Check application container logs for unhandled database connection pool exceptions and error status codes."
            ],
            "remediation_steps": [
                "Tactical Fix: Immediately update the load balancer health check from L4 TCP to L7 HTTP querying <kbd>/healthz</kbd> with expected HTTP 200 response.",
                "Strategic Control: Implement deep readiness checks separating shallow liveness from downstream dependency readiness; configure automatic connection draining."
            ],
            "verify": (
                "Verify via <kbd>curl -iv https://checkout.brightloaf.internal/healthz</kbd> that unhealthy instances return HTTP 503 and are removed "
                "from the load balancer forwarding pool within two check intervals (10 seconds)."
            ),
            "residual": (
                "Deep L7 health checks introduce database query overhead if executed too frequently; mitigate by caching health check evaluation "
                "state for 2–3 seconds within the application memory."
            ),
            "diagram": (
                "Database pool exhausted",
                "L4 TCP health check ignores L7 state",
                "LB routes orders to failing backends",
                "Deploy L7 HTTP /healthz probe",
                "Unhealthy backends drained from pool"
            ),
            "icons": (
                "../assets/icons/generic/event.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/gcp/legacy/cloud-load-balancing.svg",
                "../assets/icons/generic/outcome.svg"
            ),
            "facts": "L4 TCP port 443 handshake succeeded; application returned HTTP 503 with database pool exhaustion payload.",
            "inference": "The architectural failure stemmed from decoupling transport health check telemetry from application operational readiness.",
            "expected": "Load balancer detects HTTP 503 within 10s, marks instance unhealthy, and routes traffic exclusively to healthy nodes."
        },
        "lab": make_lab(
            name="OSI vs TCP/IP Protocol Boundary Dissection and Transport-Application Decoupling",
            goal="Demonstrate that Layer 4 TCP connectivity is independent of Layer 7 application readiness by building an automated test harness that compares raw socket probes against HTTP semantic evaluations.",
            expected="A reproducible diagnostic report proving that a service can accept TCP connections while failing application requests, validating layer decoupling.",
            steps=[
                "**Stage 1: Preflight and Environment Verification** — Verify local Python 3 environment, standard socket capabilities, and inspect available ports:\n\n```bash\npython3 --version\npython3 -c \"import socket; print('Socket subsystem operational: AF_INET =', socket.AF_INET)\"\n```",
                "**Stage 2: Prepare Target Inputs and Network Fixtures** — Author a mock application server script (<samp>mock_l4_l7_service.py</samp>) that listens on TCP port 8088, accepts incoming TCP 3-way handshakes, but returns HTTP 503 Service Unavailable for all HTTP requests:\n\n```bash\ncat <<'EOF' > mock_l4_l7_service.py\nimport socket, threading, time\n\ndef handle_client(conn, addr):\n    try:\n        data = conn.recv(1024)\n        # Simulate application-level failure response (HTTP 503)\n        body = b'{\"status\": \"error\", \"detail\": \"Database connection pool exhausted\"}\\n'\n        headers = (\n            b\"HTTP/1.1 503 Service Unavailable\\r\\n\"\n            b\"Content-Type: application/json\\r\\n\"\n            b\"Content-Length: \" + str(len(body)).encode(\"ascii\") + b\"\\r\\n\"\n            b\"Connection: close\\r\\n\\r\\n\"\n        )\n        conn.sendall(headers + body)\n    finally:\n        conn.close()\n\ndef start_server(port=8088):\n    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n    s.bind(('127.0.0.1', port))\n    s.listen(5)\n    print(f\"[SERVER] Mock L4/L7 service listening on 127.0.0.1:{port}\")\n    while True:\n        conn, addr = s.accept()\n        t = threading.Thread(target=handle_client, args=(conn, addr))\n        t.daemon = True\n        t.start()\n\nif __name__ == '__main__':\n    start_server()\nEOF\n```",
                "**Stage 3: Author Decoupled L4 and L7 Test Harness** — Create a dual-probe diagnostic script (<samp>probe_layers.py</samp>) that executes both an L4 TCP connection probe and an L7 HTTP semantic probe against the target endpoint:\n\n```bash\ncat <<'EOF' > probe_layers.py\nimport socket, urllib.request, urllib.error, sys, time\n\ndef probe_l4(host, port):\n    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    s.settimeout(2.0)\n    try:\n        s.connect((host, port))\n        s.close()\n        return True, \"TCP Handshake Completed (SYN/ACK)\"\n    except Exception as e:\n        return False, str(e)\n\ndef probe_l7(url):\n    req = urllib.request.Request(url)\n    try:\n        with urllib.request.urlopen(req, timeout=2.0) as resp:\n            return resp.status, resp.read().decode('utf-8')\n    except urllib.error.HTTPError as e:\n        return e.code, e.read().decode('utf-8')\n    except Exception as e:\n        return 0, str(e)\n\nif __name__ == '__main__':\n    host, port = '127.0.0.1', 8088\n    l4_ok, l4_msg = probe_l4(host, port)\n    l7_code, l7_body = probe_l7(f\"http://{host}:{port}/\")\n    print(f\"L4 TCP Probe Result: success={l4_ok} ({l4_msg})\")\n    print(f\"L7 HTTP Probe Result: statusCode={l7_code}\")\n    print(f\"L7 Response Body: {l7_body.strip()}\")\n    if l4_ok and l7_code == 503:\n        print(\"[ASSERT PASS] Verified layer decoupling: L4 TCP succeeded while L7 application failed.\")\n    else:\n        print(\"[ASSERT FAIL] Expected L4 success with L7 failure.\")\n        sys.exit(1)\nEOF\n```",
                "**Stage 4: Execute Protocol Layer Verification Probes** — Start the mock server in the background and execute the dual-probe test harness:\n\n```bash\npython3 mock_l4_l7_service.py &\nSERVER_PID=$!\nsleep 1\npython3 probe_layers.py\n```",
                "**Stage 5: Inspect Expected State and Verify Boundary Independence** — Inspect local socket telemetry using <kbd>ss</kbd> to observe the connection state transitions on port 8088:\n\n```bash\nss -tan 'sport = :8088 or dport = :8088'\n```",
                "**Stage 6: Rehearse Bounded Failure: Total L4 Refusal vs L7 Degradation** — Terminate the server process to observe a true Layer 4 failure (connection refused / RST packet) compared against the previous Layer 7 failure:\n\n```bash\nkill $SERVER_PID 2>/dev/null || pkill -f mock_l4_l7_service.py || true\nsleep 1\npython3 -c \"\nimport socket\ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\ntry:\n    s.connect(('127.0.0.1', 8088))\n    print('Connected')\nexcept ConnectionRefusedError as e:\n    print(f'[L4 REFUSAL CONFIRMED] {e} (RST packet returned)')\n\"\n```",
                "**Stage 7: Diagnose Evidence and Record Remediation Decision** — Author a structured diagnostic summary documenting why an L4 health check gives a false sense of reliability and recording the remediation design:\n\n```bash\ncat <<'EOF' > layer_decoupling_evidence.md\n# Architectural Evidence: OSI L4 vs L7 Decoupling\n\n- Observation 1: When mock server ran, L4 TCP connection succeeded (3-way handshake completed).\n- Observation 2: L7 HTTP request returned HTTP 503 Service Unavailable.\n- Observation 3: An L4 load balancer health check would mark this instance HEALTHY, routing traffic to failure.\n- Decision: Load balancers routing application traffic must use L7 HTTP/HTTPS health checks with explicit expected response status codes (HTTP 200).\nEOF\ncat layer_decoupling_evidence.md\n```",
                "**Stage 8: Clean Up and Close Out Exercise** — Remove temporary test scripts and verify no orphaned processes remain on port 8088:\n\n```bash\nrm -f mock_l4_l7_service.py probe_layers.py\npkill -f mock_l4_l7_service.py || true\n```"
            ],
            accept="Generated evidence markdown proves that Layer 4 TCP connection state does not guarantee Layer 7 application readiness, with explicit test verification results.",
            trouble="If port 8088 is already bound by an existing process, modify the test scripts to use an unprivileged port such as 8095.",
            file_name="layer_decoupling_evidence.md"
        )
    },
    {
        "key": "topic-02",
        "title": "IPv4 addressing, private ranges, ARP/NDP and CIDR subnetting",
        "overview": (
            "IPv4 addressing (RFC 791), Classless Inter-Domain Routing (CIDR, RFC 4632), RFC 1918 private address allocations, "
            "and Address Resolution Protocol (ARP, RFC 826) / Neighbor Discovery Protocol (NDP, RFC 4861) govern how endpoints "
            "are identified, partitioned into logical broadcast domains, and routed across physical and cloud software-defined networks (SDN). "
            "An IPv4 address is a 32-bit unsigned integer represented in dotted-decimal notation. Subnetting borrows host bits to lengthen "
            "the network prefix, dividing larger networks into smaller broadcast domains and routed zones. Understanding CIDR math "
            "and RFC 1918 allocations (<samp>10.0.0.0/8</samp>, <samp>172.16.0.0/12</samp>, <samp>192.168.0.0/16</samp>) is fundamental "
            "for cloud architects designing Google Cloud Virtual Private Cloud (VPC) subnets, Cloud VPN tunnels, Cloud Interconnects, "
            "and Google Kubernetes Engine (GKE) IP address management (IPAM)."
        ),
        "preview": (
            "An on-premises data center and a new cloud VPC both provision overlapping 10.100.0.0/16 address blocks across a hybrid Cloud Interconnect link. "
            "Packets route symmetrically for local nodes but blackhole silently for cross-environment traffic, halting critical database replication."
        ),
        "technical": (
            "**Subtopics in this discussion:** IPv4 address structure, CIDR bitmask math, and subnet prefix boundaries; "
            "RFC 1918 private address allocations and CGNAT (RFC 6598); "
            "address resolution mechanics (ARP for IPv4 and NDP for IPv6); "
            "subnet splitting, address reservations, and Longest Prefix Match (LPM) routing.\n\n"

            "### IPv4 address structure, CIDR bitmask math, and subnet prefix boundaries\n"
            "**What it is in general:** An IPv4 address (RFC 791) is a 32-bit unsigned integer formatted as four decimal octets separated by dots (<samp>X.X.X.X</samp>). "
            "Classless Inter-Domain Routing (CIDR, RFC 4632) uses a variable-length prefix (<samp>/N</samp>) to denote the contiguous network bits ($N$), leaving the remaining "
            "$32 - N$ bits for host identification. Total IP addresses in a CIDR block equal $2^{32 - N}$. For example, a <samp>/24</samp> prefix yields $2^8 = 256$ addresses; "
            "a <samp>/26</samp> yields $2^6 = 64$ addresses; a <samp>/28</samp> yields $2^4 = 16$ addresses. Subnetting borrows bits from the host space to create smaller, "
            "isolated broadcast domains and routed zones.\n\n"
            "**Relevance to a cloud architect:** CIDR calculations govern enterprise IP allocation and subnet partitioning. Sizing subnets too small causes IP exhaustion "
            "that blocks autoscaling or requires high-downtime cluster re-provisioning. Sizing subnets too large wastes scarce RFC 1918 address space and fragments the enterprise "
            "network topology. Architects must calculate network boundaries, broadcast boundaries, and usable host counts before provisioning any virtual private cloud.\n\n"
            "**Relevance to GCP:** In Google Cloud Virtual Private Cloud (VPC), all subnets are regional and defined by a primary IPv4 CIDR range. As documented in "
            "[Google Cloud VPC subnet ranges](https://cloud.google.com/vpc/docs/subnets#subnet-ranges), VPC subnet masks must be between <samp>/29</samp> (8 addresses) "
            "and <samp>/8</samp> (16,777,216 addresses).\n\n"

            "### RFC 1918 private address allocations and CGNAT (RFC 6598)\n"
            "**What it is in general:** RFC 1918 reserves three address blocks for private, non-globally routable networks: <samp>10.0.0.0/8</samp> (Class A, 16.7M IPs), "
            "<samp>172.16.0.0/12</samp> (Class B, 1.04M IPs, spanning <samp>172.16.0.0</samp>–<samp>172.31.255.255</samp>), and <samp>192.168.0.0/16</samp> (Class C, 65,536 IPs). "
            "Additionally, RFC 6598 allocates Shared Address Space <samp>100.64.0.0/10</samp> (4.19M IPs, <samp>100.64.0.0</samp>–<samp>100.127.255.255</samp>) for Carrier-Grade NAT (CGNAT). "
            "These blocks can be reused across isolated networks but cannot route across the public internet without Network Address Translation (NAT).\n\n"
            "**Relevance to a cloud architect:** Multi-region cloud environments, on-premises data centers, corporate branch offices, and third-party SaaS integrations must not have "
            "overlapping CIDR blocks if they communicate via VPN, direct interconnects, or VPC peering. If two networks use overlapping <samp>10.100.0.0/16</samp> blocks, standard Layer 3 "
            "IP routing fails, requiring complex 1:1 Private NAT or proxy workarounds. An enterprise architect designs a global IP Address Management (IPAM) hierarchy to partition RFC 1918 blocks cleanly.\n\n"
            "**Relevance to GCP:** Google Cloud VPC networks natively support all RFC 1918 ranges as well as RFC 6598 ranges for primary and secondary subnet allocations. Furthermore, "
            "[Google Cloud Cloud NAT overview](https://cloud.google.com/nat/docs/overview) enables Compute Engine instances without public IP addresses to securely access public internet "
            "APIs by translating private RFC 1918 addresses into allocated regional external IP addresses.\n\n"

            "### Address resolution mechanics (ARP for IPv4 and NDP for IPv6)\n"
            "**What it is in general:** When an operating system transmits an IP packet, it consults its local routing table. If the destination IP is on the local subnet, the host must discover "
            "the target's Layer 2 MAC address. In IPv4, Address Resolution Protocol (ARP, RFC 826) broadcasts an <samp>ARP request</samp> (<samp>who-has IP tell Source-MAC</samp>) across the local "
            "Ethernet broadcast domain. The target host replies with a unicast <samp>ARP reply</samp>, and the sender caches the mapping in its local ARP cache (<kbd>ip neigh</kbd> or <kbd>arp -an</kbd>). "
            "If the destination IP is external to the local subnet, the host ARPs exclusively for its default gateway's MAC address. In IPv6, Neighbor Discovery Protocol (NDP, RFC 4861) replaces ARP "
            "using ICMPv6 multicast neighbor solicitation and advertisement messages, eliminating disruptive network-wide broadcasts.\n\n"
            "**Relevance to a cloud architect:** Physical enterprise networks suffer from ARP storms when broadcast domains are oversized (e.g. <samp>/16</samp> subnets containing thousands of hosts). "
            "In cloud environments, software-defined networks (SDNs) intercept ARP queries. An architect must understand that while traditional Layer 2 broadcasts are emulated or filtered by cloud virtual "
            "switches, local host routing decisions still depend on identifying whether a target is on-link or routed through a gateway.\n\n"
            "**Relevance to GCP:** In Google Cloud's Andromeda SDN virtualization stack, traditional physical broadcast domains do not exist. As detailed in "
            "[Google Cloud VPC network overview](https://cloud.google.com/vpc/docs/vpc), Andromeda acts as a proxy for ARP requests: it intercepts guest OS ARP queries and returns the virtual gateway "
            "MAC address (<samp>42:01:0a:f0:00:01</samp>), routing packets purely at the software overlay layer without Layer 2 broadcast traffic on the underlying physical network.\n\n"

            "### Subnet splitting, address reservations, and Longest Prefix Match (LPM) routing\n"
            "**What it is in general:** Subnet splitting partitions a parent CIDR block into smaller equal or variable subnets by borrowing host bits. When routing packets, IP routers apply the "
            "Longest Prefix Match (LPM) algorithm: if a destination IP matches multiple route entries (e.g. <samp>0.0.0.0/0</samp>, <samp>10.240.0.0/24</samp>, and <samp>10.240.0.64/26</samp>), "
            "the router forwards the packet to the next hop associated with the most specific prefix (the largest prefix length, <samp>/26</samp>). Furthermore, network architectures impose mandatory "
            "address reservations: standard RFC networking reserves the first address as the Network identifier and the last address as the Broadcast address.\n\n"
            "**Relevance to a cloud architect:** Sizing subnets requires accounting for provider-specific IP reservations. Sizing a subnet too small (e.g. assigning a <samp>/29</samp> providing only 3 "
            "usable IPs) can stall node provisioning. Furthermore, routing priority and LPM govern traffic transit across hybrid interconnects: an overly specific route advertised over Cloud VPN will override "
            "a summarized route over Cloud Interconnect, creating unintended asymmetric routing and firewall packet drops.\n\n"
            "**Relevance to GCP:** Google Cloud enforces a strict 5-IP reservation rule in every VPC subnet. As documented in "
            "[Google Cloud VPC reserved IP addresses](https://cloud.google.com/vpc/docs/subnets#reserved_addresses), Google reserves: (1) Network address (first IP, <samp>.0</samp>), "
            "(2) Default gateway (second IP, <samp>.1</samp>), (3) Google internal infrastructure (third IP, <samp>.2</samp>), (4) Google Cloud internal DNS (fourth IP, <samp>.3</samp>), and "
            "(5) Broadcast address (last IP, <samp>.255</samp> in a <samp>/24</samp>). Therefore, usable host IPs in a GCP subnet equal $2^{32 - N} - 5$. Additionally, Google Kubernetes Engine (GKE) "
            "requires secondary CIDR ranges for Pods and Services.\n\n"

            "**Concrete Example:** An enterprise partitions <samp>10.240.0.0/24</samp> (256 addresses) into four <samp>/26</samp> subnets (64 addresses each) for a 3-tier architecture: "
            "Web (<samp>10.240.0.0/26</samp>), App (<samp>10.240.0.64/26</samp>), DB (<samp>10.240.0.128/26</samp>), and Management (<samp>10.240.0.192/26</samp>). In the App subnet "
            "(<samp>10.240.0.64/26</samp>), Google Cloud reserves: Network (<samp>10.240.0.64</samp>), Gateway (<samp>10.240.0.65</samp>), Internal infrastructure (<samp>10.240.0.66</samp>), "
            "DNS (<samp>10.240.0.67</samp>), and Broadcast (<samp>10.240.0.127</samp>), leaving 59 usable host IPs (<samp>10.240.0.68</samp> through <samp>10.240.0.126</samp>). "
            "When an ingress packet targets <samp>10.240.0.75</samp>, the router matches default <samp>0.0.0.0/0</samp>, summary <samp>10.240.0.0/24</samp>, and specific <samp>10.240.0.64/26</samp>. "
            "By LPM, the <samp>/26</samp> route wins, forwarding the packet directly to the App tier gateway <samp>10.240.0.65</samp>.\n\n"

            "**Evidence limit:** Mathematical CIDR planning validates non-overlapping address allocations on paper; it does not prove that an upstream BGP peering session, on-premises edge router, "
            "or Cloud Router lacks an conflicting static route or unauthorized more-specific prefix advertisement."
        ),
        "questions": [
            "How does the Longest Prefix Match (LPM) rule resolve traffic when both a /24 subnet and a /16 summarization route match a destination IP in a hybrid network?",
            "Why does Google Cloud reserve the first four IP addresses and the last IP address in every VPC subnet, and how does that constrain minimum subnet sizing for GKE nodes?",
            "What operational failure occurs when two disparate VPCs interconnected via VPC Peering attempt to configure overlapping RFC 1918 CIDR blocks?"
        ],
        "reference": "https://www.rfc-editor.org/rfc/rfc1918",
        "reference_label": "RFC 1918: Address Allocation for Private Internets (accessed 2026-10-02)",
        "scenario": {
            "scenario": (
                "Brightloaf established a Dedicated Cloud Interconnect connecting its on-premises logistics facility with its Google Cloud VPC. "
                "The cloud platform team provisioned a new subnet for database replication using <kbd>192.168.10.0/24</kbd>. However, an on-premises "
                "storage cluster was already operating on <kbd>192.168.10.128/25</kbd>."
            ),
            "symptom": (
                "Cloud database nodes could ping certain on-premises hosts in <kbd>192.168.10.0/25</kbd>, but cross-environment traffic to the "
                "storage cluster in <kbd>192.168.10.128/25</kbd> suffered from asymmetric routing, silent packet drops, and complete replication failure."
            ),
            "impact": (
                "Warehouse order dispatch data was delayed by up to 4 hours. 4,200 warehouse picking lists failed to synchronize, threatening "
                "next-day shipping SLAs and triggering penalty clauses from logistics partners."
            ),
            "constraints": (
                "No downtime permitted for active warehouse operations; legacy on-premises barcode scanners cannot be re-IPed without vendor firmware reflash."
            ),
            "evidence": (
                "Inspecting the host routing table on the cloud database instance via <kbd>ip route show</kbd> revealed conflicting prefix matches:\n\n"
                "```text\n"
                "default via 10.240.0.1 dev eth0 proto dhcp src 10.240.0.50 metric 100\n"
                "10.240.0.0/24 dev eth0 proto kernel scope link src 10.240.0.50\n"
                "192.168.10.0/24 via 10.240.0.1 dev eth0 metric 200\n"
                "192.168.10.128/25 via 10.240.0.254 dev eth0 metric 150\n"
                "```\n\n"
                "VPC Flow Logs in Cloud Logging captured asymmetric packet drops with action REJECT:\n\n"
                "```json\n"
                "{\n"
                '  "jsonPayload": {\n'
                '    "src_ip": "10.240.0.50",\n'
                '    "dest_ip": "192.168.10.130",\n'
                '    "protocol": 6,\n'
                '    "src_port": 49152,\n'
                '    "dest_port": 5432,\n'
                '    "action": "REJECT",\n'
                '    "reporter": "DESTINATION",\n'
                '    "disposition": "STATEFUL_FIREWALL_ASYMMETRIC_ROUTE_DROP"\n'
                "  }\n"
                "}\n"
                "```"
            ),
            "root": (
                "The destination IP <samp>192.168.10.130</samp> fell into both the <samp>/24</samp> and <samp>/25</samp> subnets. "
                "By the Longest Prefix Match (LPM) rule, outbound traffic from the cloud host was routed to the more specific <samp>/25</samp> gateway. "
                "However, the on-premises firewall returned packets via its default <samp>/24</samp> gateway. The stateful firewall dropped "
                "the return packets because it saw TCP SYN-ACK replies for connections that had never traversed its state table."
            ),
            "diagnostic_steps": [
                "Step 1: Execute <kbd>ip route get 192.168.10.130</kbd> to inspect the Longest Prefix Match next-hop decision.",
                "Step 2: Inspect ARP and neighbor tables using <kbd>ip neigh show</kbd> to verify Layer 2 gateway MAC mappings.",
                "Step 3: Analyze Cloud Logging VPC Flow Logs filtering for dropped TCP packets across the interconnect gateway.",
                "Step 4: Audit on-premises BGP advertised routes and route summarizations."
            ],
            "remediation_steps": [
                "Tactical Fix: Renumber the cloud subnet to non-overlapping RFC 1918 block <kbd>10.250.10.0/24</kbd> and update routing advertisements.",
                "Strategic Control: Implement centralized IP Address Management (IPAM) with automated policy guards preventing VPC subnet overlap."
            ],
            "verify": (
                "Execute bidirectional ping and TCP handshake probes between <samp>10.250.10.50</samp> and <samp>192.168.10.130</samp>, "
                "confirming symmetric packet transit and zero firewall drops."
            ),
            "residual": (
                "Static routes configured on legacy on-premises switches must be manually purged to prevent routing loops during convergence."
            ),
            "diagram": (
                "Subnet provisioned with /24 overlap",
                "LPM selects /25 while return uses /24",
                "Asymmetric route drops by stateful firewall",
                "Renumber cloud subnet to 10.250.10.0/24",
                "Symmetric routing restored across hybrid link"
            ),
            "icons": (
                "../assets/icons/generic/event.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/gcp/legacy/cloud-router.svg",
                "../assets/icons/generic/outcome.svg"
            ),
            "facts": "Destination IP matched both /24 and /25 routes; stateful firewall rejected return packets due to asymmetric path.",
            "inference": "The outage was caused by violation of non-overlapping CIDR boundaries in hybrid routing.",
            "expected": "Renumbering to a unique prefix eliminates route collision and restores bidirectional TCP flow."
        },
        "lab": make_lab(
            name="IPv4 CIDR Subnet Partitioning, RFC 1918 Planning, and Next-Hop Routing Engine",
            goal="Implement an automated IPv4 bitmask calculation engine that splits a monolithic /24 network into four equal /26 subnets, identifies network, broadcast, and Google Cloud reserved IP addresses, and simulates Longest Prefix Match (LPM) routing.",
            expected="Four accurately partitioned /26 subnets with exact network/broadcast boundaries, Google Cloud reserved IP maps, and a verified next-hop routing decision table.",
            steps=[
                "**Stage 1: Preflight and Environment Verification** — Verify Python 3 standard library `ipaddress` module and review base network assumptions:\n\n```bash\npython3 -c \"import ipaddress; net = ipaddress.ip_network('192.168.1.0/24'); print(f'Base network verified: {net} with {net.num_addresses} addresses')\"\n```",
                "**Stage 2: Prepare Target Inputs and Network Fixtures** — Define the target parent network <samp>10.240.0.0/24</samp> to be partitioned into four equal subnets for enterprise microservices (Web, App, DB, Management):\n\n```bash\ncat <<'EOF' > subnet_planning_inputs.json\n{\n  \"parent_network\": \"10.240.0.0/24\",\n  \"required_subnets\": 4,\n  \"tier_names\": [\"web-tier\", \"app-tier\", \"db-tier\", \"mgmt-tier\"]\n}\nEOF\n```",
                "**Stage 3: Author CIDR Subnet Calculation and Bitmask Engine** — Author an automated calculation script (<samp>cidr_engine.py</samp>) that computes subnets, calculates Google Cloud reserved IPs, and outputs an IPAM allocation matrix:\n\n```bash\ncat <<'EOF' > cidr_engine.py\nimport ipaddress, json\n\nwith open('subnet_planning_inputs.json') as f:\n    config = json.load(f)\n\nparent = ipaddress.ip_network(config['parent_network'])\n# Splitting /24 into 4 equal networks requires borrowing 2 bits -> /26\nchildren = list(parent.subnets(prefixlen_diff=2))\n\nresults = []\nfor i, net in enumerate(children):\n    tier = config['tier_names'][i]\n    # Google Cloud reserves 5 IPs per subnet:\n    # 1. Network: net.network_address\n    # 2. Gateway: net.network_address + 1\n    # 3. Cloud internal: net.network_address + 2\n    # 4. Cloud DNS: net.network_address + 3\n    # 5. Broadcast: net.broadcast_address\n    gcp_reserved = {\n        \"network\": str(net.network_address),\n        \"default_gateway\": str(net.network_address + 1),\n        \"google_internal\": str(net.network_address + 2),\n        \"google_dns\": str(net.network_address + 3),\n        \"broadcast\": str(net.broadcast_address)\n    }\n    usable_hosts = [str(ip) for ip in net.hosts()][3:] # Remaining usable\n    \n    entry = {\n        \"tier\": tier,\n        \"cidr\": str(net),\n        \"netmask\": str(net.netmask),\n        \"network_address\": str(net.network_address),\n        \"broadcast_address\": str(net.broadcast_address),\n        \"total_addresses\": net.num_addresses,\n        \"usable_host_count_standard\": net.num_addresses - 2,\n        \"usable_host_count_gcp\": net.num_addresses - 5,\n        \"gcp_reserved\": gcp_reserved,\n        \"usable_host_range\": f\"{usable_hosts[0]} - {usable_hosts[-1]}\"\n    }\n    results.append(entry)\n\nwith open('subnet_allocation_matrix.json', 'w') as f:\n    json.dump(results, f, indent=2)\n\nprint(\"[CIDR ENGINE] Generated 4 /26 subnets successfully.\")\nfor r in results:\n    print(f\"Tier: {r['tier']:10} CIDR: {r['cidr']:18} Usable: {r['usable_host_range']} (GCP Capacity: {r['usable_host_count_gcp']})\")\nEOF\n```",
                "**Stage 4: Execute Subnet Partitioning and Output Range Map** — Run the CIDR calculation engine and inspect the generated allocation matrix:\n\n```bash\npython3 cidr_engine.py\n```",
                "**Stage 5: Inspect Expected State and Verify CIDR Invariants** — Author an assertion script (<samp>verify_cidr_invariants.py</samp>) to verify that all subnets are contiguous, non-overlapping, and mathematically exact:\n\n```bash\ncat <<'EOF' > verify_cidr_invariants.py\nimport json, ipaddress\n\nwith open('subnet_allocation_matrix.json') as f:\n    subnets = json.load(f)\n\nassert len(subnets) == 4, \"Must have exactly 4 subnets\"\nseen_ranges = []\n\nfor s in subnets:\n    net = ipaddress.ip_network(s['cidr'])\n    assert net.prefixlen == 26, f\"Expected /26, got {net.prefixlen}\"\n    assert s['total_addresses'] == 64, \"/26 must contain 64 addresses\"\n    assert s['usable_host_count_gcp'] == 59, \"GCP usable host count must be 64 - 5 = 59\"\n    seen_ranges.append(net)\n\n# Verify zero overlap between all pairs\nfor i in range(len(seen_ranges)):\n    for j in range(i + 1, len(seen_ranges)):\n        assert not seen_ranges[i].overlaps(seen_ranges[j]), f\"Overlap detected between {seen_ranges[i]} and {seen_ranges[j]}\"\n\nprint(\"[ASSERT PASS] All 4 /26 subnets are contiguous, non-overlapping, and satisfy GCP 5-IP reservation rules.\")\nEOF\npython3 verify_cidr_invariants.py\n```",
                "**Stage 6: Rehearse Bounded Failure: Overlapping CIDR Route Collision** — Simulate a routing table failure where a conflicting <samp>10.240.0.32/27</samp> route causes an LPM routing override:\n\n```bash\ncat <<'EOF' > simulate_lpm_routing.py\nimport ipaddress\n\nroutes = [\n    {\"prefix\": ipaddress.ip_network(\"0.0.0.0/0\"), \"next_hop\": \"internet-gateway\", \"desc\": \"Default route\"},\n    {\"prefix\": ipaddress.ip_network(\"10.240.0.0/24\"), \"next_hop\": \"vpc-peering-gateway\", \"desc\": \"Summarized VPC route\"},\n    {\"prefix\": ipaddress.ip_network(\"10.240.0.0/26\"), \"next_hop\": \"web-tier-gateway\", \"desc\": \"Specific web subnet route\"},\n    {\"prefix\": ipaddress.ip_network(\"10.240.0.32/27\"), \"next_hop\": \"rogue-test-gateway\", \"desc\": \"Conflicting rogue route\"},\n]\n\ndef lookup(dest_ip_str):\n    ip = ipaddress.ip_address(dest_ip_str)\n    matching = [r for r in routes if ip in r['prefix']]\n    # Longest prefix match selects route with largest prefixlen\n    best = max(matching, key=lambda r: r['prefix'].prefixlen)\n    return best\n\ntest_ip = \"10.240.0.40\"\nmatched = lookup(test_ip)\nprint(f\"Destination IP: {test_ip}\")\nprint(f\"Selected Route: {matched['prefix']} -> Next Hop: {matched['next_hop']} ({matched['desc']})\")\nif matched['next_hop'] == 'rogue-test-gateway':\n    print(\"[SIMULATION WARNING] Longest Prefix Match diverted traffic to rogue /27 gateway over valid /26 gateway!\")\nEOF\npython3 simulate_lpm_routing.py\n```",
                "**Stage 7: Diagnose Evidence and Record Next-Hop Routing Decision** — Generate a comprehensive next-hop routing decision record and subnet map artifact:\n\n```bash\ncat <<'EOF' > subnet_routing_plan.md\n# IPv4 CIDR Subnet Partitioning & Next-Hop Routing Plan\n\n## Subnet Allocations (Parent: 10.240.0.0/24)\n\n| Tier Name | CIDR Prefix | Network Address | Default Gateway | Google DNS | Broadcast | Usable Host Range | GCP Usable IPs |\n|---|---|---|---|---|---|---|---|\n| web-tier | 10.240.0.0/26 | 10.240.0.0 | 10.240.0.1 | 10.240.0.3 | 10.240.0.63 | 10.240.0.4 - 10.240.0.62 | 59 |\n| app-tier | 10.240.0.64/26 | 10.240.0.64 | 10.240.0.65 | 10.240.0.67 | 10.240.0.127 | 10.240.0.68 - 10.240.0.126 | 59 |\n| db-tier | 10.240.0.128/26 | 10.240.0.128 | 10.240.0.129 | 10.240.0.131 | 10.240.0.191 | 10.240.0.132 - 10.240.0.190 | 59 |\n| mgmt-tier | 10.240.0.192/26 | 10.240.0.192 | 10.240.0.193 | 10.240.0.195 | 10.240.0.255 | 10.240.0.196 - 10.240.0.254 | 59 |\n\n## Labeled Next-Hop Forwarding Path\n- Ingress Packet: Destination `10.240.0.75` (App Tier)\n- Route Evaluation: Matches `0.0.0.0/0` (/0), `10.240.0.0/24` (/24), and `10.240.0.64/26` (/26).\n- Forwarding Decision: Longest Prefix Match selects `10.240.0.64/26` with next-hop `10.240.0.65`.\nEOF\ncat subnet_routing_plan.md\n```",
                "**Stage 8: Clean Up and Close Out Exercise** — Remove scratch scripts while preserving the final exit evidence document:\n\n```bash\nrm -f subnet_planning_inputs.json cidr_engine.py verify_cidr_invariants.py simulate_lpm_routing.py subnet_allocation_matrix.json\n```"
            ],
            accept="Subnet routing plan artifact contains four correct /26 ranges with exact network, broadcast, and Google Cloud reserved addresses alongside a labeled next-hop path.",
            trouble="Ensure the parent CIDR prefix length is exactly /24; dividing a /24 by 4 requires borrowing 2 bits to produce /26 subnets.",
            file_name="subnet_routing_plan.md"
        )
    },
    {
        "key": "topic-03",
        "title": "Packet path from NIC to application socket",
        "overview": (
            "The packet traversal lifecycle maps how an incoming raw electrical or optical signal on a physical network interface "
            "card (NIC) or virtual NIC (such as Google Cloud gVNIC) transforms into application-level bytes delivered to a user-space "
            "socket. This traversal crosses hardware Direct Memory Access (DMA) ring buffers, CPU hardware interrupts (IRQs), "
            "Linux kernel New API (NAPI) polling loops, software interrupts (<samp>ksoftirqd</samp>), the network core subsystem "
            "(<samp>netif_receive_skb</samp>), netfilter connection tracking, IP routing lookup, transport protocol demultiplexing, "
            "and socket receive queues (<samp>sk_rcvbuf</samp>). Understanding this pathway allows cloud architects to diagnose "
            "packet drops that occur before user-space code ever executes, tune kernel parameters (<samp>net.core.somaxconn</samp>, "
            "<samp>tcp_max_syn_backlog</samp>), and avoid mysterious connection timeouts during peak traffic bursts."
        ),
        "preview": (
            "Virtual machine guest metrics show rising interface receive drops and backlog queue overruns while application CPU utilization remains deceptively under twenty percent. "
            "Unacknowledged customer HTTP requests encounter thirty-second gateway timeouts, triggering duplicate API retries that compound cascading backpressure across the entire ordering pipeline."
        ),
        "technical": (
            "**Subtopics in this discussion:** NIC hardware ingress, DMA ring buffers, hardware IRQs, and NAPI polling; "
            "kernel network core traversal (SoftIRQs, sk_buff allocation, netfilter hooks, routing table lookup); "
            "socket abstractions, addressing tuples (2-tuple bind, 4-tuple demux), and socket types (SOCK_STREAM, SOCK_DGRAM, SOCK_RAW); "
            "socket queues (SYN queue, Accept queue) and I/O multiplexing concurrency models (epoll, io_uring).\n\n"

            "### NIC hardware ingress, DMA ring buffers, hardware IRQs, and NAPI polling\n"
            "**What it is in general:** When an Ethernet frame arrives at a Network Interface Card (NIC), the physical transceiver deserializes bits, verifies the Cyclic "
            "Redundancy Check (CRC/FCS), and writes the packet directly into host RAM via Direct Memory Access (DMA) into a circular Receive Ring Buffer (<samp>rx-ring</samp>). "
            "If the ring descriptors are exhausted, the NIC hardware drops the frame immediately (recorded as <samp>rx_no_buffer_count</samp> in <kbd>ethtool -S</kbd>). "
            "To notify the operating system, the NIC fires a hardware interrupt (IRQ) to a CPU core. To prevent interrupt thrashing under high packet rates, the Linux kernel "
            "uses the New API (NAPI) subsystem: the device driver disables hardware IRQs for that ring and schedules a Software Interrupt (<samp>NET_RX_SOFTIRQ</samp>), "
            "causing <samp>ksoftirqd</samp> to poll the ring buffer in batches bounded by <samp>net.core.netdev_budget</samp> (default 300 packets) before re-enabling interrupts.\n\n"
            "**Relevance to a cloud architect:** Packet drops frequently occur at the hardware or virtual driver level before user-space processes or application monitoring can detect them. "
            "When a VM experiences sudden traffic surges, a saturated single-core softIRQ or an under-sized NIC ring buffer causes silent packet drops while aggregate VM CPU utilization "
            "appears deceptively low (<20%). Architects must size VM instance types, select multi-queue virtual NICs, and ensure ring buffers are tuned to absorb ingress bursts.\n\n"
            "**Relevance to GCP:** Google Cloud provides the [Google Virtual NIC (gVNIC)](https://cloud.google.com/compute/docs/networking/using-gvnic), an optimized virtual network "
            "interface driver designed specifically for Compute Engine. gVNIC supports multi-queue NIC architectures and higher packet-per-second (PPS) rates than legacy VirtIO, "
            "and is mandatory for Compute Engine Tier_1 high-bandwidth networking (up to 200 Gbps on C3 and N2 instances).\n\n"

            "### Kernel network core traversal (SoftIRQs, sk_buff allocation, netfilter hooks, routing table lookup)\n"
            "**What it is in general:** Once retrieved from the DMA ring by NAPI, the packet is encapsulated into a kernel socket buffer structure (<samp>sk_buff</samp>) and passed to "
            "<samp>netif_receive_skb()</samp>. The packet traverses packet capture taps (<samp>AF_PACKET</samp> for tcpdump), enters the Netfilter subsystem (<samp>iptables</samp>/<samp>nftables</samp> "
            "evaluating <samp>PREROUTING</samp> rules and connection tracking <samp>conntrack</samp>), and enters the IP routing subsystem. The kernel checks the destination IP in the Forwarding "
            "Information Base (FIB): if the packet is destined for another host and forwarding is enabled (<samp>net.ipv4.ip_forward = 1</samp>), it is routed to an egress interface; if destined "
            "for a local IP, it passes to Netfilter <samp>INPUT</samp> rules and is delivered to the transport protocol handler (<samp>tcp_v4_rcv</samp> or <samp>udp_rcv</samp>).\n\n"
            "**Relevance to a cloud architect:** Netfilter connection tracking tables (<samp>nf_conntrack</samp>) maintain state for every active TCP and UDP flow. In high-concurrency environments "
            "(e.g. Kubernetes worker nodes running thousands of pods), an exhausted <samp>nf_conntrack_max</samp> table causes the kernel to immediately drop all new inbound connections "
            "(<samp>nf_conntrack: table full, dropping packet</samp>). Architects must monitor connection tracking capacity and size worker nodes appropriately.\n\n"
            "**Relevance to GCP:** Google Cloud's Andromeda virtual switch offloads routing and security policy enforcement outside the guest VM. However, within Compute Engine instances and GKE nodes, "
            "guest Netfilter rules (such as <samp>kube-proxy</samp> iptables/IPVS chains) execute inside the Linux kernel. Understanding <samp>sk_buff</samp> processing is critical when diagnosing "
            "[Compute Engine network bandwidth limits and monitoring drops](https://cloud.google.com/compute/docs/networking/monitor-bandwidth#bandwidth-monitoring).\n\n"

            "### Socket abstractions, addressing tuples (2-tuple bind, 4-tuple demux), and socket types (SOCK_STREAM, SOCK_DGRAM, SOCK_RAW)\n"
            "**What it is in general:** Sockets provide the POSIX API bridging kernel network stacks to user-space applications. A server socket binds to a 2-tuple: local IP address and port number. "
            "Binding to <samp>0.0.0.0</samp> (<samp>INADDR_ANY</samp>) accepts traffic on all interfaces, while binding to a specific IP (e.g. <samp>127.0.0.1</samp> or internal VPC IP <samp>10.240.0.50</samp>) "
            "restricts ingress to that interface. Established TCP connections are demultiplexed in a kernel hash table keyed by the 4-tuple: "
            "<samp>(source_ip, source_port, destination_ip, destination_port)</samp>, allowing tens of thousands of concurrent client connections on port 443. Socket types define transmission semantics: "
            "<samp>SOCK_STREAM</samp> (TCP: reliable, sequenced byte streams without message boundaries), <samp>SOCK_DGRAM</samp> (UDP: unreliable, connectionless datagrams preserving discrete message boundaries), "
            "and <samp>SOCK_RAW</samp> (bypassing transport layers for direct IP header manipulation, requiring <samp>CAP_NET_RAW</samp>). Socket flags like <samp>SO_REUSEADDR</samp> permit binding to ports in "
            "<samp>TIME_WAIT</samp>, while <samp>SO_REUSEPORT</samp> enables multiple worker processes to bind to the same port and share connection load via kernel hashing.\n\n"
            "**Relevance to a cloud architect:** Modern container runtimes and ingress proxies utilize <samp>SO_REUSEPORT</samp> to distribute thousands of incoming connections across multiple CPU cores "
            "without lock contention in user space. Furthermore, architects must restrict container capabilities (e.g. dropping <samp>CAP_NET_RAW</samp> in Kubernetes security contexts) to prevent "
            "compromised pods from spoofing IP packets or sniffing raw network traffic.\n\n"
            "**Relevance to GCP:** In Google Kubernetes Engine (GKE), dropping <samp>NET_RAW</samp> via Pod Security Standards is an enterprise security baseline. In Compute Engine, multi-threaded "
            "web servers (like Nginx or Envoy) bind to VPC interface IPs with <samp>SO_REUSEPORT</samp> to saturate multi-vCPU instances efficiently, as recommended in "
            "[Google Cloud networking best practices for Compute Engine](https://cloud.google.com/compute/docs/networking/network-tuning).\n\n"

            "### Socket queues (SYN queue, Accept queue) and I/O multiplexing concurrency models (epoll, io_uring)\n"
            "**What it is in general:** For incoming TCP connections, the Linux kernel manages two distinct socket queues: (1) **SYN Queue (Half-Open):** Stores incoming <samp>SYN</samp> packets "
            "awaiting client <samp>ACK</samp>; bounded by <samp>net.ipv4.tcp_max_syn_backlog</samp>. If full, incoming SYNs are dropped or answered with SYN Cookies. (2) **Accept Queue (Fully Established):** "
            "Stores completed 3-way handshakes awaiting the application to call <kbd>accept()</kbd>; bounded by $\\min(\\text{backlog}, \\text{net.core.somaxconn})$. If full, established connections "
            "are dropped or reset, logged as listen queue overflows. For handling high concurrency, blocking thread-per-connection architectures fail due to thread memory overhead and context switching. "
            "Linux provides $O(1)$ I/O multiplexing via <kbd>epoll</kbd> (<kbd>epoll_create</kbd>, <kbd>epoll_ctl</kbd>, <kbd>epoll_wait</kbd> using kernel Red-Black trees and ready-lists in level-triggered "
            "or edge-triggered mode) and <kbd>io_uring</kbd> (asynchronous ring buffers shared between user space and kernel space, eliminating syscall overhead).\n\n"
            "**Relevance to a cloud architect:** Cloud autoscaling cannot prevent outages if individual VM socket queues drop connections during sudden spikes. When an API experiences a burst, "
            "Managed Instance Groups (MIGs) take 1–2 minutes to scale out. If backend VM listen backlogs are left at standard Linux defaults (128 connections), the accept queue overflows in milliseconds, "
            "rejecting clients before autoscaled VMs launch. Architects must harden kernel queue depths (<samp>somaxconn = 4096</samp>, <samp>tcp_max_syn_backlog = 8192</samp>) in VM startup scripts to "
            "provide an absorption buffer.\n\n"
            "**Relevance to GCP:** Tuning kernel socket queues is a core requirement for [Google Cloud Compute Engine guest OS optimization](https://cloud.google.com/solutions/best-practices-compute-engine-operations). "
            "Compute Engine instance startup scripts should apply tuned sysctl settings (<samp>net.core.somaxconn = 4096</samp>) to ensure high-concurrency workloads absorb traffic spikes gracefully behind Cloud Load Balancing.\n\n"

            "**Concrete Example:** During a flash sale, 45,000 concurrent connection requests arrive at an authentication microservice running on an N2 Compute Engine instance. The application server uses "
            "default Linux kernel settings (<samp>net.core.somaxconn = 128</samp>). In less than 50 milliseconds, the accept queue fills to capacity (129 entries in <samp>Recv-Q</samp>). The kernel begins "
            "silently dropping inbound TCP SYN packets. Upstream Cloud Load Balancers log HTTP 504 Gateway Timeouts, while the VM CPU sits deceptively idle at 35% utilization. Inspecting telemetry via "
            "<kbd>ss -lnt</kbd> and <kbd>netstat -s</kbd> reveals thousands of 'times the listen queue of a socket overflowed'. Tuning <samp>net.core.somaxconn = 4096</samp> and expanding the application "
            "listen backlog eliminates drops and allows the VM to absorb the traffic spike cleanly.\n\n"

            "**Evidence limit:** Local socket queue listings (<kbd>ss -lnt</kbd>) and drop counters (<kbd>netstat -s</kbd>) reflect kernel state inside a single guest OS; they cannot reveal packet drops "
            "occurring upstream in Cloud Armor WAF rules, Cloud Load Balancer proxies, or Andromeda SDN flow tables."
        ),
        "questions": [
            "How does Linux kernel I/O multiplexing with epoll edge-triggered mode (EPOLLET) solve the C10K concurrency bottleneck that causes thread-per-connection architectures to exhaust memory?",
            "How do the Linux kernel net.core.somaxconn setting and the application listen(fd, backlog) parameter interact to constrain maximum concurrent connection establishment?",
            "What is the operational difference between SO_REUSEADDR and SO_REUSEPORT, and how does SO_REUSEPORT distribute incoming connection loads across multiple worker processes in kernel space?"
        ],
        "reference": "https://www.kernel.org/doc/Documentation/networking/scaling.rst",
        "reference_label": "Linux Kernel Networking: Scaling Network Stack (accessed 2026-10-02)",
        "scenario": {
            "scenario": (
                "Brightloaf launched an omnichannel promotional campaign driving a massive traffic spike to its authentication API "
                "running on Compute Engine instances. Within 3 minutes of campaign launch, API latency spiked from 15ms to over 8,000ms, "
                "and client connection timeouts skyrocketed despite the VM reporting less than 50% CPU and memory utilization."
            ),
            "symptom": (
                "Clients experienced connection timeouts (<samp>ETIMEDOUT</samp>) and reset by peer (<samp>ECONNRESET</samp>). Upstream "
                "Cloud Load Balancer logged HTTP 504 Gateway Timeout errors. The application service itself remained responsive when queried "
                "locally, but new external connections were dropped at a rate of 4,000/sec."
            ),
            "impact": (
                "Over 85,000 users were unable to authenticate. Checkout conversion dropped by 72% over a 35-minute duration, resulting "
                "in an estimated $140,000 in abandoned shopping carts and brand reputation impairment."
            ),
            "constraints": (
                "Zero reboot permitted during flash sale; cannot migrate to larger VM machine type without interrupting active connections; "
                "all tuning must be applied via dynamic kernel runtime interfaces (<samp>/proc/sys</samp>)."
            ),
            "evidence": (
                "Executing <kbd>ss -lnt 'sport = :8080'</kbd> revealed that the socket Send-Q (which for listening sockets represents the "
                "maximum accept queue backlog) was clamped at 128, and Recv-Q (current backlog) was constantly maxed at 129:\n\n"
                "```text\n"
                "State      Recv-Q Send-Q Local Address:Port Peer Address:Port\n"
                "LISTEN     129    128          0.0.0.0:8080      0.0.0.0:*\n"
                "```\n\n"
                "Checking kernel protocol drop telemetry using <kbd>netstat -s | grep -i listen</kbd> confirmed massive queue overflow drops:\n\n"
                "```text\n"
                "    48921 times the listen queue of a socket overflowed\n"
                "    48921 SYNs to LISTEN sockets dropped\n"
                "```\n\n"
                "Inspecting NIC ring buffer statistics using <kbd>ethtool -S eth0 | grep -E 'drop|overflow'</kbd> confirmed additional driver drops:\n\n"
                "```text\n"
                "    rx_no_buffer_count: 14209\n"
                "    rx_queue_drop_cnt: 14209\n"
                "```"
            ),
            "root": (
                "The Compute Engine VM instance was running standard default Linux kernel parameters with <samp>net.core.somaxconn = 128</samp> "
                "and the application server was initialized with a default backlog of 128. When 45,000 concurrent connection requests arrived, "
                "the accept queue filled in milliseconds. In accordance with TCP queue overflow semantics, the kernel silently dropped incoming "
                "SYN and ACK packets, forcing clients into exponential retransmission backoff and eventual timeout."
            ),
            "diagnostic_steps": [
                "Step 1: Run <kbd>ss -lnt</kbd> to inspect the listen socket backlog (<samp>Send-Q</samp>) and current pending connections (<samp>Recv-Q</samp>).",
                "Step 2: Inspect kernel network drop counters via <kbd>netstat -s</kbd> filtering for listen queue overflows.",
                "Step 3: Check virtual NIC ring buffer status via <kbd>ethtool -g eth0</kbd> and drop counters via <kbd>ethtool -S eth0</kbd>.",
                "Step 4: Audit system-wide kernel limits in <samp>/proc/sys/net/core/somaxconn</samp> and <samp>/proc/sys/net/ipv4/tcp_max_syn_backlog</samp>."
            ],
            "remediation_steps": [
                "Tactical Fix: Dynamically expand the kernel socket accept queue limit via <kbd>sudo sysctl -w net.core.somaxconn=4096</kbd> and <kbd>sudo sysctl -w net.ipv4.tcp_max_syn_backlog=8192</kbd>.",
                "Strategic Control: Expand the NIC Rx ring buffer to maximum capacity via <kbd>sudo ethtool -G eth0 rx 4096</kbd>; update application startup flags to request a backlog of 4096."
            ],
            "verify": (
                "Run high-concurrency connection stress tests and verify via <kbd>netstat -s</kbd> that 'times the listen queue of a socket overflowed' "
                "remains zero while <kbd>ss -lnt</kbd> shows Send-Q expanded to 4096."
            ),
            "residual": (
                "Expanding socket queue depths increases kernel memory consumption under heavy traffic; monitor <samp>slabtop</samp> and "
                "<samp>TCP: inuse</samp> allocations to ensure the VM does not exceed physical RAM limits."
            ),
            "diagram": (
                "Traffic burst floods VM network stack",
                "Default somaxconn=128 accept queue overflows",
                "Kernel silently drops incoming SYNs & ACKs",
                "Expand somaxconn to 4096 & rx-ring to 4096",
                "Zero listen drops under 45k concurrent flows"
            ),
            "icons": (
                "../assets/icons/generic/event.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/generic/policy.svg",
                "../assets/icons/generic/outcome.svg"
            ),
            "facts": "Socket listen queue was clamped at 128; netstat recorded 48,921 listen queue overflow drops.",
            "inference": "The outage was caused by mismatch between kernel socket buffer configuration and production concurrency demands.",
            "expected": "Tuning somaxconn and tcp_max_syn_backlog eliminates queue overflow drops during traffic surges."
        },
        "lab": make_lab(
            name="Packet Traversal Lifecycle Tracing from Physical NIC to Application Socket Buffer",
            goal="Trace and benchmark the Linux kernel packet path from network interface receive queues through SoftIRQ processing to socket accept queues, observing queue backlog behavior and tuning kernel parameters.",
            expected="Telemetry record capturing socket queue states (Send-Q, Recv-Q), kernel backlog saturation metrics, and validated sysctl parameter calculations for production server tuning.",
            steps=[
                "**Stage 1: Preflight and Environment Telemetry Discovery** — Inspect current host socket limits and network device capabilities:\n\n```bash\nif [ -f /proc/sys/net/core/somaxconn ]; then\n  cat /proc/sys/net/core/somaxconn\n  cat /proc/sys/net/ipv4/tcp_max_syn_backlog\nelse\n  sysctl kern.ipc.somaxconn 2>/dev/null || true\nfi\npython3 -c \"import socket; print('Kernel socket interface available; SO_RCVBUF =', socket.SO_RCVBUF)\"\n```",
                "**Stage 2: Prepare Target Sockets and Descriptor Baseline** — Author a socket listener test harness (<samp>socket_queue_monitor.py</samp>) that allows configurable listen backlog sizes:\n\n```bash\ncat <<'EOF' > socket_queue_monitor.py\nimport socket, sys, time\n\nbacklog = int(sys.argv[1]) if len(sys.argv) > 1 else 5\ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\ns.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\ns.bind(('127.0.0.1', 9099))\ns.listen(backlog)\nprint(f\"[MONITOR] Listening on 127.0.0.1:9099 with backlog={backlog}\")\nprint(\"[MONITOR] Holding socket open without calling accept()...\")\ntry:\n    while True:\n        time.sleep(1)\nexcept KeyboardInterrupt:\n    s.close()\nEOF\n```",
                "**Stage 3: Author Kernel Packet Path Trace and Simulator** — Author a fast client burst simulator (<samp>simulate_connection_burst.py</samp>) that attempts 8 concurrent connections against the backlog-5 socket with a 0.3s timeout, demonstrating immediate accept queue saturation:\n\n```bash\ncat <<'EOF' > simulate_connection_burst.py\nimport socket, time\n\nconnections = []\nnum_conns = 8\nprint(f\"[SIMULATOR] Attempting to open {num_conns} concurrent TCP connections to 127.0.0.1:9099...\")\n\nfor i in range(num_conns):\n    try:\n        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n        s.settimeout(0.3)\n        s.connect(('127.0.0.1', 9099))\n        connections.append(s)\n        print(f\"  Connection {i+1}: ESTABLISHED (in accept queue)\")\n    except Exception as e:\n        print(f\"  Connection {i+1}: REJECTED/TIMEOUT ({type(e).__name__} - queue saturated)\")\n\nprint(f\"[SIMULATOR] Active established connections: {len(connections)}/{num_conns}\")\nprint(\"[SIMULATOR] Holding connections open for 15 seconds to allow queue telemetry inspection...\")\ntime.sleep(15)\nfor s in connections:\n    s.close()\nprint(\"[SIMULATOR] Closed all connections.\")\nEOF\n```",
                "**Stage 4: Execute Packet Dispatch and Socket Delivery** — Start the listener with a restricted backlog of 5, then launch the client burst simulator in the background:\n\n```bash\npython3 socket_queue_monitor.py 5 &\nMONITOR_PID=$!\nsleep 1\npython3 simulate_connection_burst.py &\nSIM_PID=$!\nsleep 1\n```",
                "**Stage 5: Inspect Expected State and Buffer Metrics** — While the connections are held open, execute <kbd>ss</kbd> to inspect the listen queue depth and observe the saturated <samp>Send-Q</samp> / <samp>Recv-Q</samp> metrics:\n\n```bash\nss -lnt 'sport = :9099'\n```",
                "**Stage 6: Rehearse Bounded Failure: Socket Buffer Saturation and Listen Drop** — Terminate the background processes and confirm queue release:\n\n```bash\nkill $MONITOR_PID $SIM_PID 2>/dev/null || pkill -f socket_queue_monitor.py || true\npkill -f simulate_connection_burst.py 2>/dev/null || true\nsleep 1\n```",
                "**Stage 7: Diagnose Evidence and Formulate Kernel Tuning Remediation** — Author a system tuning guide (<samp>kernel_network_tuning.md</samp>) detailing production parameters for high-throughput cloud environments:\n\n```bash\ncat <<'EOF' > kernel_network_tuning.md\n# Linux Kernel Network Stack & Socket Queue Production Tuning Guide\n\n## Core Socket Queue Parameters\n\n| Parameter | Default (Standard Linux) | Production Cloud Recommendation | Architectural Mechanism |\n|---|---|---|---|\n| `net.core.somaxconn` | 128 | 4096 | Upper ceiling for the listen accept queue depth |\n| `net.ipv4.tcp_max_syn_backlog` | 128 - 512 | 8192 | Maximum half-open connections in SYN queue |\n| `net.core.netdev_budget` | 300 | 600 | Max packets processed in one NAPI softIRQ polling cycle |\n| `net.ipv4.tcp_rmem` | 4096 87380 6291456 | 4096 87380 16777216 | Min, default, and max TCP receive buffer sizes |\n\n## Verification Command\nTo inspect socket drop counters:\n```bash\nnetstat -s | grep -i listen\nss -lnt\n```\nEOF\ncat kernel_network_tuning.md\n```",
                "**Stage 8: Clean Up and Close Out Exercise** — Remove temporary socket test scripts and verify port 9099 is released:\n\n```bash\nrm -f socket_queue_monitor.py simulate_connection_burst.py\npkill -f socket_queue_monitor.py || true\n```"
            ],
            accept="Kernel network tuning artifact contains documented explanations of somaxconn, tcp_max_syn_backlog, and netdev_budget, with empirical observations of socket queue depths.",
            trouble="If ss output shows empty socket listings, verify that the monitor process started cleanly and that port 9099 was not blocked.",
            file_name="kernel_network_tuning.md"
        )
    },
    {
        "key": "topic-04",
        "title": "Process communication protocols: IPC, Unix domain sockets, loopback, and network RPCs",
        "overview": (
            "Inter-Process Communication (IPC) protocols govern how operating system processes exchange state, synchronize execution, "
            "and transfer data both locally on a single host and across distributed network topologies. Local communication mechanisms "
            "include Unix Domain Sockets (<samp>AF_UNIX</samp> / UDS), network loopback sockets (<samp>AF_INET</samp> over the <samp>lo</samp> interface), "
            "POSIX shared memory (<samp>shm_open</samp>), pipes/FIFOs, and message queues. In modern cloud architecture—particularly inside "
            "Google Kubernetes Engine (GKE) Pods, service mesh sidecars (Envoy / Istio), and database proxies (Cloud SQL Auth Proxy)—the "
            "architectural choice between Unix Domain Sockets and loopback TCP directly dictates CPU consumption, connection concurrency limits, "
            "and security boundaries. Unix domain sockets bypass the entire TCP/IP network stack (no IP headers, no TCP handshakes, no checksumming, "
            "and no routing lookups), transferring data directly via kernel memory buffers and enforcing POSIX filesystem permissions."
        ),
        "preview": (
            "A high-throughput container communicating with its Envoy sidecar proxy over loopback TCP exhausts all ephemeral ports and spikes kernel CPU in TIME_WAIT connection management. "
            "Switching the sidecar communication protocol to a Unix Domain Socket with shared volume mounts eliminates TCP overhead and restores sub-millisecond response latency."
        ),
        "technical": (
            "**Subtopics in this discussion:** local IPC mechanisms (Unix domain sockets, pipes, FIFOs, POSIX shared memory); "
            "network loopback sockets (AF_INET over 127.0.0.1) vs Unix domain sockets (AF_UNIX) stack bypass; "
            "microservice RPCs (gRPC, REST over HTTP/2 and HTTP/3) across network boundaries; "
            "security isolation, access controls (POSIX DAC permissions vs port exposure), and file descriptor passing (SCM_RIGHTS).\n\n"

            "### Local IPC mechanisms (Unix domain sockets, pipes, FIFOs, POSIX shared memory)\n"
            "**What it is in general:** Inter-Process Communication (IPC) mechanisms enable processes on the same operating system to exchange data and synchronize execution. "
            "These include: (1) **Pipes and FIFOs:** Unidirectional byte streams managed by the kernel with bounded internal buffer sizes (typically 64 KB). "
            "(2) **POSIX Shared Memory (<samp>shm_open</samp>, <samp>mmap</samp>):** Maps identical physical RAM pages into the address spaces of multiple processes, "
            "enabling zero-copy data exchange at raw memory speeds, requiring user-space synchronization primitives like mutexes or Linux <samp>futex</samp> calls. "
            "(3) **Unix Domain Sockets (UDS, <samp>AF_UNIX</samp>):** Bidirectional stream (<samp>SOCK_STREAM</samp>) or datagram (<samp>SOCK_DGRAM</samp>) communication "
            "using standard POSIX socket APIs bound to filesystem pathnames or the Linux abstract socket namespace.\n\n"
            "**Relevance to a cloud architect:** Microservice decomposition often co-locates multiple processes on the same host or within the same Kubernetes Pod "
            "(e.g. primary application container, service mesh sidecar, log forwarder, local cache). Selecting the wrong IPC mechanism introduces substantial CPU "
            "and serialization overhead. Cloud architects choose between shared memory (for ultra-high-speed zero-copy analytics) and Unix Domain Sockets (for structured, "
            "robust, low-latency inter-process messaging).\n\n"
            "**Relevance to GCP:** In Google Kubernetes Engine (GKE) and Cloud Run multi-container pods, local IPC is enabled using shared in-memory volumes "
            "(<samp>emptyDir: { medium: Memory }</samp>). For example, [Cloud SQL Auth Proxy documentation](https://cloud.google.com/sql/docs/mysql/connect-auth-proxy) "
            "recommends configuring the proxy to listen on a Unix Domain Socket instead of TCP <samp>127.0.0.1</samp> when co-located with application containers in GKE.\n\n"

            "### Network loopback sockets (AF_INET over 127.0.0.1) vs Unix domain sockets (AF_UNIX) stack bypass\n"
            "**What it is in general:** Network loopback sockets (<samp>AF_INET</samp> over <samp>127.0.0.1</samp> or <samp>::1</samp> on interface <samp>lo</samp>) treat "
            "local inter-process communication as network traffic. Packets traverse the entire TCP/IP stack: generating TCP headers, computing checksums, tracking sequence numbers, "
            "maintaining sliding windows, executing routing lookups, and managing TCP connection state lifecycles (<samp>TIME_WAIT</samp>). Sockets lingering in <samp>TIME_WAIT</samp> "
            "consume ephemeral ports from <samp>net.ipv4.ip_local_port_range</samp> (typically ~28,232 usable ports), causing ephemeral port exhaustion under high QPS. In contrast, "
            "Unix Domain Sockets (<samp>AF_UNIX</samp>) bypass the IP and TCP stacks entirely: data is copied directly between process memory buffers in the kernel page cache without "
            "IP headers, checksums, TCP handshakes, or ephemeral port allocations, yielding 2x to 3x higher throughput and lower CPU utilization.\n\n"
            "**Relevance to a cloud architect:** High-traffic container sidecar patterns (such as Envoy in Anthos Service Mesh, Istio, or Datadog agents) routing thousands of requests "
            "per second over loopback TCP frequently trigger <samp>TIME_WAIT</samp> saturation and <samp>EADDRNOTAVAIL</samp> connection failures. A cloud architect designs sidecar communication "
            "architectures to use Unix Domain Sockets over shared memory volumes, eliminating TCP stack overhead, preventing ephemeral port exhaustion, and reducing latency.\n\n"
            "**Relevance to GCP:** In Google Kubernetes Engine (GKE), workloads utilizing Envoy sidecars or [Anthos Service Mesh](https://cloud.google.com/service-mesh/docs/overview) "
            "can route traffic between the application and sidecar proxy over Unix Domain Sockets mounted on an in-memory <samp>emptyDir</samp> volume, significantly reducing CPU throttling on high-density nodes.\n\n"

            "### Microservice RPCs (gRPC, REST over HTTP/2 and HTTP/3) across network boundaries\n"
            "**What it is in general:** While IPC handles local on-host communication, distributed microservices communicating across VM, cluster, or cloud boundaries require network "
            "Remote Procedure Call (RPC) frameworks. Modern cloud architectures rely on **gRPC** (an open-source RPC framework utilizing Protocol Buffers for compact binary serialization, "
            "HTTP/2 for multiplexed bi-directional streaming, and strongly typed interface definition language [IDL] contracts) or **REST** (stateless HTTP/1.1 or HTTP/2 APIs using JSON payloads). "
            "gRPC provides multiplexing over a single persistent TCP connection, native deadlocks and cancellation propagation, and high serialization efficiency compared to text-based JSON.\n\n"
            "**Relevance to a cloud architect:** Selecting between REST and gRPC defines the operational envelope of an enterprise cloud architecture. While external client-facing APIs typically "
            "expose REST/JSON for universal compatibility, internal service-to-service communication across microservices should standardize on gRPC to reduce serialization CPU overhead by up to "
            "70% and slash network bandwidth across VPCs and cloud interconnects.\n\n"
            "**Relevance to GCP:** Google Cloud's own public and internal APIs are built entirely on gRPC and Protocol Buffers. In Google Cloud, "
            "[Cloud Endpoints and API Gateway](https://cloud.google.com/endpoints/docs/grpc/about-grpc) natively support gRPC service deployment, protocol transcoding (translating REST/JSON "
            "into gRPC/Protobuf), and integration with Cloud Load Balancing.\n\n"

            "### Security isolation, access controls (POSIX DAC permissions vs port exposure), and file descriptor passing (SCM_RIGHTS)\n"
            "**What it is in general:** Network loopback sockets (<samp>127.0.0.1</samp>) lack native process-level access controls: any unprivileged process sharing the network namespace can "
            "connect to an open loopback port unless complex local firewall (<samp>iptables</samp>) rules are applied. In contrast, Unix Domain Sockets are represented as filesystem nodes and enforce "
            "standard POSIX Discretionary Access Control (DAC) permissions: read and write permissions (<kbd>chmod 0660</kbd>, <kbd>chown app:proxy</kbd>) restrict connections exclusively to "
            "authorized users or groups. Furthermore, Unix Domain Sockets support **File Descriptor Passing via <samp>SCM_RIGHTS</samp>**: one process can transfer open file descriptors (such as "
            "connected client sockets or open files) to another process via <samp>sendmsg()</samp> and <samp>recvmsg()</samp> ancillary control messages, enabling zero-downtime binary reloads "
            "and seamless process handoffs.\n\n"
            "**Relevance to a cloud architect:** In multi-tenant container hosts or shared compute environments, binding unauthenticated services to loopback TCP ports creates security "
            "vulnerabilities where malicious co-located processes probe internal APIs. Architects enforce zero-trust local boundaries using Unix Domain Sockets with restricted POSIX permissions. "
            "Additionally, <samp>SCM_RIGHTS</samp> enables graceful upgrades for proxy infrastructure (e.g. Envoy or Nginx reloads) without dropping active customer TCP connections.\n\n"
            "**Relevance to GCP:** Compute Engine and GKE environments leverage POSIX file permissions on shared volumes to enforce principle-of-least-privilege communication between sidecars "
            "and applications, aligning with the [Google Cloud Architecture Framework: Security, privacy, and compliance](https://cloud.google.com/architecture/framework/security).\n\n"

            "**Concrete Example:** In a GKE Pod running an e-commerce checkout service, an application container communicates with a co-located Envoy sidecar proxy. Under peak load of 6,000 "
            "requests/second, the application opens a new TCP connection to <samp>127.0.0.1:8080</samp> for every HTTP request. Within 20 seconds, the 28,000 available ephemeral ports are "
            "exhausted and linger in <samp>TIME_WAIT</samp> state for 60 seconds. The application begins logging <samp>Cannot assign requested address (EADDRNOTAVAIL)</samp> errors and container "
            "CPU throttles. Re-architecting the inter-container communication to use a Unix Domain Socket at <samp>/var/run/envoy/envoy.sock</samp> mounted via an <samp>emptyDir: { medium: Memory }</samp> "
            "volume eliminates the TCP handshake, bypasses ephemeral port allocation entirely, drops <samp>TIME_WAIT</samp> count to zero, and cuts pod CPU utilization by 35%.\n\n"

            "**Evidence limit:** Inspecting local Unix domain socket inodes via <kbd>ss -x</kbd> or <kbd>lsof -U</kbd> verifies socket binding, filesystem permissions, and connected peer endpoints; "
            "it does not verify application payload deserialization, gRPC schema compatibility, or processing latency inside the recipient process."
        ),
        "questions": [
            "Why does communicating between an application container and an Envoy sidecar proxy via a Unix Domain Socket (UDS) reduce CPU utilization and tail latency compared to loopback TCP (127.0.0.1)?",
            "How do POSIX filesystem permissions (chmod and chown) on a Unix Domain Socket file enforce security boundaries that cannot be natively enforced by loopback TCP port bindings?",
            "Under what system failure conditions does an unhandled SIGPIPE signal terminate a producer process writing to an orphaned Unix Domain Socket or named pipe?"
        ],
        "reference": "https://man7.org/linux/man-pages/man7/unix.7.html",
        "reference_label": "Linux Programmer's Manual: unix(7) - Sockets for local interprocess communication (accessed 2026-10-02)",
        "scenario": {
            "scenario": (
                "Brightloaf deployed an Envoy service mesh sidecar inside each Kubernetes Pod to handle mTLS encryption, rate limiting, "
                "and distributed tracing for the order fulfillment service. The main application container communicated with the Envoy sidecar "
                "via HTTP/1.1 over loopback TCP (<samp>127.0.0.1:8080</samp>)."
            ),
            "symptom": (
                "During a flash sale promotion, the order fulfillment pods experienced severe CPU throttling. Application response times degraded "
                "from 3.8ms to 320ms, and the Envoy proxy began logging connection failures with <samp>upstream_reset_before_response_started</samp>. "
                "The kernel log on GKE nodes reported TCP SYN flooding drops on the loopback interface."
            ),
            "impact": (
                "Checkout validations stalled, dropping order completion rates by 48%. Over 12,000 customers abandoned checkout over a 25-minute window, "
                "costing an estimated $78,000 in immediate lost revenue."
            ),
            "constraints": (
                "No increase in container CPU limits permitted due to node pool capacity constraints; must maintain strict end-to-end mTLS "
                "encryption between nodes; zero modifications to external API endpoints."
            ),
            "evidence": (
                "Inspecting socket summary state inside the pod using <kbd>ss -s</kbd> revealed over 26,000 sockets lingering in TIME_WAIT on loopback:\n\n"
                "```text\n"
                "Total: 27150\n"
                "TCP:   26840 (estab 320, closed 26400, orphaned 0, timewait 26380)\n"
                "\n"
                "Transport Total     IP        IPv6\n"
                "RAW       0         0         0\n"
                "UDP       4         4         0\n"
                "TCP       460       460       0\n"
                "INET      464       464       0\n"
                "FRAG      0         0         0\n"
                "```\n\n"
                "Inspecting node kernel ring buffer via <kbd>dmesg | grep -i syn</kbd> showed drops:\n\n"
                "```text\n"
                "[42180.124582] TCP: request_sock_TCP: Possible SYN flooding on port 127.0.0.1:8080. Dropping request. Check SNMP counters.\n"
                "```"
            ),
            "root": (
                "The application runtime was opening a new TCP connection to the Envoy sidecar for every HTTP request instead of reusing "
                "persistent connections via an HTTP keep-alive connection pool. At 5,000 requests/second, the ephemeral port range (<samp>32768–60999</samp>) "
                "was completely exhausted within seconds. Sockets were trapped in the 60-second kernel <samp>TIME_WAIT</samp> state. The kernel "
                "spent massive CPU time managing TCP connection tables and dropping new connection requests."
            ),
            "diagnostic_steps": [
                "Step 1: Check pod socket distribution using <kbd>ss -tan 'sport = :8080 or dport = :8080'</kbd> to identify TIME_WAIT concentration.",
                "Step 2: Inspect kernel ephemeral port range via <kbd>cat /proc/sys/net/ipv4/ip_local_port_range</kbd>.",
                "Step 3: Measure container CPU utilization attributed to softirq and system call overhead using <kbd>top</kbd> and <kbd>vmstat 1</kbd>.",
                "Step 4: Audit client HTTP client configuration for missing connection pooling and keep-alive settings."
            ],
            "remediation_steps": [
                "Tactical Fix: Configure the application HTTP client to use persistent connection pooling with keep-alive to reduce connection churn.",
                "Strategic Control: Migrate sidecar communication from loopback TCP to a Unix Domain Socket (<samp>/var/run/envoy/envoy.sock</samp>) "
                "mounted via an in-memory volume (<samp>emptyDir: { medium: Memory }</samp>), eliminating TCP handshakes and ephemeral port allocation entirely."
            ],
            "verify": (
                "Benchmark pod under 10,000 QPS load: verify via <kbd>ss -s</kbd> that TCP TIME_WAIT sockets drop to near zero, "
                "Unix domain socket connections handle traffic with sub-millisecond latency, and pod CPU consumption drops by over 35%."
            ),
            "residual": (
                "Unix domain socket files must be unlinked (<kbd>unlink()</kbd> / <kbd>rm</kbd>) prior to process bind, or subsequent process startups "
                "will fail with <samp>EADDRINUSE</samp>; configure container startup hooks or socket deletion handlers."
            ),
            "diagram": (
                "App opens new TCP connection per request",
                "Loopback exhausts 28k ephemeral ports",
                "TIME_WAIT saturation causes SYN drops",
                "Migrate to Unix Domain Socket on shm volume",
                "Zero port churn & 35% lower CPU usage"
            ),
            "icons": (
                "../assets/icons/generic/event.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/generic/failure.svg",
                "../assets/icons/generic/endpoint.svg",
                "../assets/icons/generic/outcome.svg"
            ),
            "facts": "26,380 sockets in TIME_WAIT on 127.0.0.1; kernel reported SYN flooding drop on port 8080.",
            "inference": "Using network loopback sockets for high-frequency sidecar IPC created unnecessary TCP state overhead and port exhaustion.",
            "expected": "Migrating to Unix Domain Sockets eliminates network stack overhead and provides deterministic sub-millisecond IPC."
        },
        "lab": make_lab(
            name="Inter-Process Communication Benchmarking and Unix Domain Socket Hardening",
            goal="Author, benchmark, and secure an inter-process communication pipeline, quantitatively comparing Unix Domain Sockets (AF_UNIX) against loopback network sockets (127.0.0.1), inspecting socket inodes, and enforcing POSIX filesystem permissions.",
            expected="Benchmark demonstrating 2x+ throughput and lower latency for Unix Domain Sockets over loopback TCP, with verified file permission access controls and clean socket lifecycle management.",
            steps=[
                "**Stage 1: Preflight and Environment Telemetry Discovery** — Inspect local system support for Unix Domain Sockets and loopback interface telemetry:\n\n```bash\nip link show lo 2>/dev/null || ifconfig lo 2>/dev/null || true\npython3 -c \"import socket; print('Unix Domain Sockets available: AF_UNIX =', hasattr(socket, 'AF_UNIX'))\"\n```",
                "**Stage 2: Prepare Target Directory and IPC Fixtures** — Create a dedicated secure temporary directory for socket files and verify permissions:\n\n```bash\nmkdir -p /tmp/ipc_lab\nchmod 0700 /tmp/ipc_lab\nls -ld /tmp/ipc_lab\n```",
                "**Stage 3: Author High-Performance Unix Domain Socket and Loopback Test Harness** — Create a dual-mode benchmark server and client (<samp>ipc_benchmark.py</samp>) that transfers 10,000 message payloads over both Unix Domain Sockets and loopback TCP, with connection retry logic for robust execution across any hardware:\n\n```bash\ncat <<'EOF' > ipc_benchmark.py\nimport socket, os, time, sys\n\nMSG_COUNT = 10000\nMSG_PAYLOAD = b\"PING:ORDER_VALIDATE:\" + b\"X\" * 256\nUDS_PATH = \"/tmp/ipc_lab/test_ipc.sock\"\nTCP_PORT = 9188\n\ndef run_uds_server():\n    if os.path.exists(UDS_PATH):\n        os.unlink(UDS_PATH)\n    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)\n    s.bind(UDS_PATH)\n    os.chmod(UDS_PATH, 0o660)\n    s.listen(5)\n    conn, _ = s.accept()\n    for _ in range(MSG_COUNT):\n        data = conn.recv(len(MSG_PAYLOAD))\n        conn.sendall(b\"PONG:OK\")\n    conn.close()\n    s.close()\n    if os.path.exists(UDS_PATH):\n        os.unlink(UDS_PATH)\n\ndef run_uds_client():\n    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)\n    for _ in range(50):\n        try:\n            s.connect(UDS_PATH)\n            break\n        except (FileNotFoundError, ConnectionRefusedError):\n            time.sleep(0.05)\n    start = time.time()\n    for _ in range(MSG_COUNT):\n        s.sendall(MSG_PAYLOAD)\n        resp = s.recv(7)\n    duration = time.time() - start\n    s.close()\n    return duration\n\ndef run_tcp_server():\n    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n    s.bind(('127.0.0.1', TCP_PORT))\n    s.listen(5)\n    conn, _ = s.accept()\n    for _ in range(MSG_COUNT):\n        data = conn.recv(len(MSG_PAYLOAD))\n        conn.sendall(b\"PONG:OK\")\n    conn.close()\n    s.close()\n\ndef run_tcp_client():\n    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    for _ in range(50):\n        try:\n            s.connect(('127.0.0.1', TCP_PORT))\n            break\n        except ConnectionRefusedError:\n            time.sleep(0.05)\n    start = time.time()\n    for _ in range(MSG_COUNT):\n        s.sendall(MSG_PAYLOAD)\n        resp = s.recv(7)\n    duration = time.time() - start\n    s.close()\n    return duration\n\nif __name__ == '__main__':\n    import multiprocessing\n    mode = sys.argv[1] if len(sys.argv) > 1 else \"all\"\n    \n    if mode in (\"all\", \"uds\"):\n        p = multiprocessing.Process(target=run_uds_server)\n        p.start()\n        time.sleep(0.1)\n        uds_time = run_uds_client()\n        p.join()\n        uds_qps = MSG_COUNT / uds_time\n        print(f\"[BENCHMARK] Unix Domain Socket: {MSG_COUNT} msgs in {uds_time:.3f}s ({uds_qps:.0f} QPS)\")\n    \n    if mode in (\"all\", \"tcp\"):\n        p = multiprocessing.Process(target=run_tcp_server)\n        p.start()\n        time.sleep(0.1)\n        tcp_time = run_tcp_client()\n        p.join()\n        tcp_qps = MSG_COUNT / tcp_time\n        print(f\"[BENCHMARK] Loopback TCP (127.0.0.1): {MSG_COUNT} msgs in {tcp_time:.3f}s ({tcp_qps:.0f} QPS)\")\n    \n    if mode == \"all\":\n        ratio = uds_qps / tcp_qps\n        print(f\"[RESULT] Unix Domain Socket is {ratio:.2f}x faster than Loopback TCP\")\nEOF\n```",
                "**Stage 4: Execute IPC Benchmark Comparing UDS vs Loopback TCP** — Execute the benchmark suite transferring 10,000 requests across both IPC mechanisms:\n\n```bash\npython3 ipc_benchmark.py all\n```",
                "**Stage 5: Inspect Expected State and Performance Metrics** — Bind an active Unix Domain Socket and inspect its inode entry in the kernel socket table using <kbd>ss -xl</kbd>:\n\n```bash\npython3 -c \"\nimport socket, os\npath = '/tmp/ipc_lab/inspect.sock'\ns = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)\ns.bind(path)\ns.listen(1)\nprint(f'[UDS BIND] Socket active at {path}')\nos.system('ss -xl | grep -E \"(State|/tmp/ipc_lab)\"')\ns.close()\nos.unlink(path)\n\"\n```",
                "**Stage 6: Rehearse Bounded Failure: Socket Permission Denial and Stale File Lockout** — Simulate a permission denial failure by restricting socket permissions to <samp>0000</samp> and testing connection rejection:\n\n```bash\ncat <<'EOF' > test_socket_permissions.py\nimport socket, os\n\nUDS_PATH = \"/tmp/ipc_lab/test_perm.sock\"\nif os.path.exists(UDS_PATH):\n    os.unlink(UDS_PATH)\n\ns = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)\ns.bind(UDS_PATH)\n# Intentionally lock out permissions\nos.chmod(UDS_PATH, 0o000)\n\ntry:\n    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)\n    client.connect(UDS_PATH)\n    if os.geteuid() == 0:\n        print(\"[NOTE] Running as root (UID 0) bypasses standard DAC permissions as designed.\")\n    else:\n        print(\"[FAIL] Connection succeeded unexpectedly without permission.\")\nexcept PermissionError as e:\n    print(f\"[ASSERT PASS] POSIX DAC Permission Denied verified: {e}\")\nfinally:\n    s.close()\n    if os.path.exists(UDS_PATH):\n        os.unlink(UDS_PATH)\nEOF\npython3 test_socket_permissions.py\n```",
                "**Stage 7: Diagnose Evidence and Record Remediation Decision** — Author a sidecar IPC architecture recommendation document detailing why UDS is preferred for Kubernetes sidecars:\n\n```bash\ncat <<'EOF' > ipc_architecture_decision.md\n# Architectural Decision Record: Process Communication Protocols for Container Sidecars\n\n## Quantitative Benchmark Findings\n- Unix Domain Sockets demonstrated >2x throughput compared to loopback TCP (127.0.0.1).\n- UDS eliminated TCP 3-way handshakes, sequence tracking, and ephemeral port allocation.\n- Sockets in `TIME_WAIT` on loopback were reduced to zero.\n\n## Security Boundary Enforcement\n- Unix Domain Sockets enforce native POSIX filesystem permissions (chmod 0660 with dedicated GID).\n- Unlike loopback TCP (which binds to ports accessible by any process sharing the network namespace), UDS restricts access using filesystem Discretionary Access Control (DAC).\n\n## Recommendation\nConfigure high-throughput container sidecars (Envoy, Cloud SQL Auth Proxy) to communicate via Unix Domain Sockets mounted on an in-memory `emptyDir` volume.\nEOF\ncat ipc_architecture_decision.md\n```",
                "**Stage 8: Clean Up and Close Out Exercise** — Remove test scripts, delete temporary socket directory, and verify filesystem cleanliness:\n\n```bash\nrm -f ipc_benchmark.py test_socket_permissions.py\nrm -rf /tmp/ipc_lab\n```"
            ],
            accept="Generated architectural decision record contains verified quantitative benchmark metrics comparing UDS against loopback TCP, with confirmed POSIX DAC permission enforcement.",
            trouble="If socket file binding fails with EADDRINUSE, ensure existing socket files are unlinked using os.unlink() before calling bind().",
            file_name="ipc_architecture_decision.md"
        )
    }
]

DATA = {
    "day": DAY,
    "work_block": WORK_BLOCK,
    "part1_html": PART1_HTML,
    "part1_intro": PART1_INTRO,
    "exit_summary": EXIT_SUMMARY,
    "part2_intro": PART2_INTRO,
    "arch_table_html": ARCH_TABLE_HTML,
    "arch_diagram": ARCH_DIAGRAM,
    "arch_svg_html": ARCH_SVG_HTML,
    "part3_intro": PART3_INTRO,
    "part4_intro": PART4_INTRO,
    "topics": TOPICS
}
