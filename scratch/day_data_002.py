"""Durable Day 002 specification: subnet arithmetic and packet-path evidence.

All case records are synthetic teaching fixtures. Labs are offline/local tabletop;
GCP documentation informs design only. No credentials or cloud resources required.
"""
import sys
from pathlib import Path
from functools import partial
_SITE = Path(__file__).resolve().parents[1]
if str(_SITE) not in sys.path:
    sys.path.insert(0, str(_SITE))
from scratch.day_helpers import (escape, dedent, keyword, discussion, flow_svg,
    source as _source, subtopic as _subtopic, stage as _stage,
    write_file, lab as _lab, case as _case)

DAY = 2
ACCESS_DATE = '2026-10-07'
EXIT_SUMMARY = 'Four correct ranges with network/broadcast addresses and a labeled next-hop path.'
SOURCES = {
    'layers': ('RFC 1122: Internet protocol suite, section 1.1.3 (page 8) (accessed 2026-10-07)', 'https://datatracker.ietf.org/doc/html/rfc1122#page-8'),
    'tcp': ('RFC 9293: TCP introduction, section 2 (accessed 2026-10-07)', 'https://www.rfc-editor.org/rfc/rfc9293.html#section-2'),
    'private': ('RFC 1918: Private address space, section 3 (accessed 2026-10-07)', 'https://www.rfc-editor.org/rfc/rfc1918.html#section-3'),
    'arp': ('RFC 826: Address Resolution Protocol (accessed 2026-10-07)', 'https://www.rfc-editor.org/rfc/rfc826.html'),
    'ndp': ('RFC 4861: Neighbor Discovery comparison with IPv4, section 3.1 (accessed 2026-10-07)', 'https://www.rfc-editor.org/rfc/rfc4861.html#section-3.1'),
    'subnets': ('Google Cloud VPC documentation: Unusable IP addresses in every primary subnet (accessed 2026-10-07)', 'https://docs.cloud.google.com/vpc/docs/subnets#unusable-ip-addresses-in-every-subnet'),
    'routes': ('Google Cloud VPC documentation: Types of routes and route selection (accessed 2026-10-07)', 'https://docs.cloud.google.com/vpc/docs/routes#types_of_routes'),
    'lb': ('Google Cloud Load Balancing documentation: Load balancer types (accessed 2026-10-07)', 'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#load-balancer-types'),
    'health': ('Google Cloud Health Checks documentation: Categories, protocols, and ports (accessed 2026-10-07)', 'https://docs.cloud.google.com/load-balancing/docs/health-check-concepts#categories_protocols_ports'),
    'napi': ('Linux kernel documentation: NAPI driver API (accessed 2026-10-07)', 'https://docs.kernel.org/networking/napi.html#driver-api'),
    'gvnic': ('Google Compute Engine documentation: Overview of Google Virtual NIC (accessed 2026-10-07)', 'https://docs.cloud.google.com/compute/docs/networking/using-gvnic#overview'),
    'unix': ('Linux man-pages: unix(7) local sockets description (accessed 2026-10-07)', 'https://man7.org/linux/man-pages/man7/unix.7.html#DESCRIPTION'),
    'grpc': ('gRPC documentation: Introduction to gRPC and Protocol Buffers (accessed 2026-10-07)', 'https://grpc.io/docs/what-is-grpc/introduction/#working-with-protocol-buffers'),
    'api': ('Google Cloud API Design Guide: Resource-oriented design (accessed 2026-10-07)', 'https://docs.cloud.google.com/apis/design#resources'),
    'proxy': ('Google Cloud SQL documentation: Connect Auth Proxy using Unix sockets (accessed 2026-10-07)', 'https://docs.cloud.google.com/sql/docs/mysql/connect-auth-proxy#unix-sockets'),
    'python': ('Python documentation: ipaddress IPv4Network subnets calculation (accessed 2026-10-07)', 'https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Network.subnets'),
}


def workspace(prefix, *, preflight_text):
    return f"""command -v bash
command -v python3
LAB_DIR=$(mktemp -d /tmp/{prefix}.XXXXXX)
export LAB_DIR
cd "$LAB_DIR"
python3 -c 'import os, pathlib; pathlib.Path("preflight.txt").write_text("{preflight_text}\\n"); print("Workspace:", os.getcwd())'
"""


source = partial(_source, sources=SOURCES)
subtopic = partial(_subtopic, sources=SOURCES, access_date=ACCESS_DATE)
stage = partial(_stage, location='Local Linux terminal')
LAB_CONTEXT = {
    'mode': 'Local Linux terminal tabletop; supplied synthetic fixtures. Observed locally: command execution, script assertions, and file hashes. Simulated or predicted: host routing decisions, packet traversal, and boundary classifications. Untested on GCP: live Andromeda SDN forwarding, Compute Engine VPC network provisioning, and cloud firewall rules.',
    'prereq': 'Day 1 workspace/evidence repository; local Linux Bash, Python 3 standard library, text editor',
    'preflight': 'Run all eight stages in order in the same terminal. Stage 1 verifies required local tools with command -v and creates a unique workspace. Stop if Python 3 or Bash is unavailable; use the Linux environment prepared on Day 1. Commands write only inside the lab workspace.',
    'verification': 'Recorded outputs are local calculations, script assertions, or fixture classifications. They are not cloud observations.',
    'cleanup': 'Stage 8 removes temporary calculation scripts and non-essential inputs while preserving durable evidence files. No processes, cloud resources, firewall rules, or kernel settings are created or changed. Copy the listed evidence to the Day 1 repository before discarding the workspace.'
}
lab = partial(_lab, defaults=LAB_CONTEXT)
case = partial(_case,
    evidence_label='Supplied synthetic records (literal fixture, not observed logs):',
    facts='Synthetic fixture: socket bytes queued=yes; application reads=no.',
    inference='The first missing progress signal is the process-read boundary; worker blockage remains a hypothesis.',
    expected='After the actual blockage is diagnosed and repaired, observe a read and valid response; neither is established here.')

NEXT_HOP_SVG = flow_svg('d002-next-hop', 'Supplied Ethernet model: host A to host B', [
    ('Host A selects route', ('10.240.0.10/26 → .75', 'Destination outside A subnet'), 'client'),
    ('Resolve next hop', ('Gateway IP: 10.240.0.1', 'ARP learns gateway MAC'), 'router'),
    ('Send local frame', ('IP destination stays .75', 'Frame destination: gateway'), 'switch'),
    ('Router forwards', ('Connected 10.240.0.64/26', 'Outgoing interface: 10.240.0.65'), 'router'),
    ('Resolve host B', ('Router ARPs for 10.240.0.75', 'New frame destination: B MAC'), 'endpoint'),
    ('Host B receives', ('IP destination: 10.240.0.75', 'Transport delivers to socket'), 'server'),
], ['off-link', 'encapsulate', 'route lookup', 'neighbor', 'deliver'],
    'Read 1 → 2 → 3 → 4 → 5 → 6. Supplied conventional Ethernet teaching topology, with no NAT and connected router interfaces. IP endpoints stay A and B; link-layer addresses change at the router. This is a tabletop path, not a capture of Google Cloud physical forwarding.')

NIC_SVG = flow_svg('d002-nic-socket', 'Receive sequence: NIC to application socket', [
    ('NIC receive queue', ('Frame arrives at interface', 'Driver-managed receive buffers'), 'endpoint'),
    ('Driver processing', ('DMA: device transfers to RAM', 'Interrupt / polling notification'), 'queue'),
    ('NAPI polling', ('Linux processes receive work', 'Scheduling varies by driver'), 'queue'),
    ('IP input checks', ('Headers, policy, local delivery', 'Transit packets use forwarding'), 'firewall'),
    ('Transport + socket', ('TCP matches connection tuple', 'Bytes wait in receive buffer'), 'server'),
    ('Application reads', ('Process reads socket bytes', 'Parses request; may still fail'), 'user'),
], ['notify', 'poll', 'IP input', 'demux', 'read'],
    'Read 1 → 2 → 3 → 4 → 5 → 6. A simplified Linux receive path for established TCP traffic addressed to this host. Driver offloads and kernel versions can change processing details; SYN/accept queues belong to connection establishment. Loopback skips physical NIC/DMA, and this drawing does not reveal Google Cloud fabric internals.')

PART1_INTRO = 'The roadmap allocates 2–3 hours; take additional time for the worked mechanisms and evidence checkpoints when needed. The main exit artifact is the /24 split plus a labeled next-hop path. IPC is a short companion checkpoint required by the coverage map.'
PART2_INTRO = 'Learn the mechanism first, then its architectural use and documented GCP application. DNS, TLS, advanced transports, and tuning belong to later study days.'
PART3_INTRO = 'All four cases below are synthetic supplied fixtures for reasoning practice. Their literal records are teaching inputs, not production logs or observations from this workstation.'
PART4_INTRO = 'Use a local Linux Bash terminal with Python 3 and the Day 1 evidence repository. Each exercise creates a separate disposable workspace and has exactly eight stages. No cloud login, billing, deployment, Terraform, root access, or packet capture is needed for this day. GCP steps are documentation review; cloud execution remains untested. Run stages in order in the same terminal for each exercise.'
ARCH_DIAGRAM = {}
ARCH_SVG_HTML = ''  # Focused diagrams are placed beside their qualifying subtopics.
ARCH_TABLE_HTML = ''

OVERVIEWS = [
    ('topic-01', 'OSI and TCP/IP layer models',
     f'{keyword("Protocol layers")} group responsibilities: links move frames, IP routes packets, transports connect endpoints, and applications interpret messages. The models help locate a failure without assuming every green lower layer proves success above it.',
     'Learn the vocabulary before tracing an IPv4 packet.', 'Between the link/IP path studied today and DNS/transport in Day 3, then TLS/HTTP in Day 4.',
     'A TCP probe succeeds while an HTTP request returns 503. Treating the backend as ready can send customers to a failing checkout.'),
    ('topic-02', 'IPv4 addressing, private ranges, ARP/NDP and CIDR subnetting',
     f'{keyword("CIDR")} writes an address range as a prefix such as /24. Subnet math tells you which hosts share a network; address resolution tells you which local neighbor receives the next frame.',
     'The Practice requires four equal ranges and correct network/broadcast boundaries.', 'Before future VPC design; NDP is introduced only as the IPv6 counterpart of ARP, with IPv6 details on Day 3.',
     'A host configured with /24 treats an address in a different /26 as local. It may fail to reach the service even though both IP addresses look valid.'),
    ('topic-03', 'Packet path from NIC to application socket',
     f'A {keyword("NIC")} (network interface card), driver, kernel network stack, socket buffer, and application each own a different step of delivery. Reaching the interface is earlier than being read and understood by the process.',
     'Connect the labeled next-hop path to the receive path inside the destination host.', 'After subnet/routing selection and before Day 3 connection states; driver tuning is outside today’s Practice.',
     'Packets reach the host but the application does not read queued bytes. Increasing a network timeout can leave users waiting longer without resolving the application stall.'),
    ('topic-04', 'Process communication protocols: IPC, Unix domain sockets, and network RPCs',
     f'{keyword("IPC")} means inter-process communication. Local socket paths, loopback IP endpoints, and remote procedure calls have different reachability and ownership boundaries.',
     'The coverage map requires a short companion comparison after the packet reaches a process.', 'Relate same-host communication to the network path; container platforms and full RPC deployment come later.',
     'A service on another machine is given a local Unix socket path. The client cannot reach that endpoint and the integration stops before any business request is processed.'),
]
PART1_HTML = f'''<p>{escape(PART1_INTRO)}</p><p class="callout"><strong>Exit evidence:</strong> {escape(EXIT_SUMMARY)}</p>''' + ''.join(
    f'''<article class="topic-card overview" id="{key}-overview"><h3>{i}. {escape(title)}</h3>
<p>{intro}</p><p><strong class="side-heading">Why today:</strong> {escape(why)}</p>
<p><strong class="side-heading">Where it sits:</strong> {escape(where)}</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> {escape(preview)}</p>
<p><a href="#{key}-technical">Technical discussion →</a> <a href="#{key}-problem">Real-world problem →</a> <a href="#{key}-lab">Step-by-step lab →</a></p></article>'''
    for i, (key, title, intro, why, where, preview) in enumerate(OVERVIEWS, 1)
)

T1_TITLES = ['OSI and TCP/IP responsibility map', 'Layer 4 versus Layer 7 evidence']
T1_TECH = discussion(T1_TITLES, [
    subtopic(T1_TITLES[0],
        f'The {keyword("OSI model")} names seven responsibilities: physical signals (1), local frames (2), network addressing/routing (3), transport (4), sessions (5), representation (6), and applications (7). The practical TCP/IP grouping is link, internet, transport, and application. A browser request depends on several of them at once; these are responsibility categories, not seven mandatory programs.',
        'Use the failing responsibility to choose the next investigation: a missing route is an IP question, whereas a valid error response is an application question. The model is a diagnostic vocabulary; implementation boundaries can differ.',
        'Use the documented Layer 4/Layer 7 load balancer distinction when discussing future ingress designs. Do not infer a particular proprietary forwarding implementation from an OSI label.', ['layers', 'lb']),
    '''<table><caption>Responsibility map; definitions are expressed as a table</caption><thead><tr><th>OSI layers</th><th>TCP/IP group</th><th>Example question</th></tr></thead><tbody>
<tr><td>1 Physical, 2 Data link</td><td>Link</td><td>Can this local interface exchange frames?</td></tr>
<tr><td>3 Network</td><td>Internet</td><td>Which route matches destination 10.240.0.75?</td></tr>
<tr><td>4 Transport</td><td>Transport</td><td>Can the client connect to the service port?</td></tr>
<tr><td>5 Session, 6 Presentation, 7 Application</td><td>Application (approximate grouping)</td><td>Does the request receive the correct business response?</td></tr>
</tbody></table>''',
    subtopic(T1_TITLES[1],
        f'{keyword("Layer 4")} (L4) concerns transport endpoints, such as TCP connections and ports. {keyword("Layer 7")} (L7) concerns application messages, such as HTTP paths and status codes. A successful TCP connection followed by HTTP 503 is a concrete example of transport success with application failure. A TCP connection does not certify message parsing or dependency readiness.',
        'Choose a probe that tests the invariant you need. A port probe can establish connectivity; a readiness response can test a selected application condition. A deep dependency probe also needs a design that avoids unnecessarily withdrawing all capacity during a shared outage.',
        'Application Load Balancers operate at Layer 7. Network Load Balancers operate at Layer 4, with proxy and passthrough variants. Health-check protocol and supported criteria must be chosen for the specific load balancer; HTTP probing is not a substitute for fixing the failing application.', ['tcp', 'health']),
], 'In the supplied case, TCP=connected and HTTP=503 mean the service can be contacted but cannot satisfy the request. Inspect the application result before blaming route selection.',
    'The records are synthetic. Layer classification does not prove a deployed backend’s readiness or identify which dependency failed.')

T2_TITLES = ['IPv4 prefixes and subnet arithmetic', 'RFC 1918 private ranges', 'ARP and NDP: resolve the local neighbor', 'Subnet splitting and provider reservations', 'Next-hop selection across two subnets']
T2_TECH = discussion(T2_TITLES, [
    subtopic(T2_TITLES[0],
        f'An IPv4 address has 32 bits. In {keyword("/N prefix notation")}, N bits identify the network and 32−N remain for addresses within it. The mathematical formula for total addresses in any CIDR block is 2^(32−N). Conventional usable host capacity subtracts two addresses (network identifier and broadcast address), yielding 2^(32−N) − 2 hosts. In cloud environments such as Google Cloud VPC, provider reservations consume four addresses per primary subnet, yielding 2^(32−N) − 4 assignable hosts. Thus /24 has 256 total addresses (254 conventional usable, 252 GCP assignable), /20 has 4,096 total addresses (4,094 conventional usable, 4,092 GCP assignable), and /16 has 65,536 total addresses (65,534 conventional usable, 65,532 GCP assignable). A /24 mask is 255.255.255.0; /20 is 255.255.240.0; /16 is 255.255.0.0. Prefix length is a bit boundary, so a /20 does not end at an octet boundary. For 10.240.0.0/24, splitting into four equal blocks borrows two bits: /24 + 2 = /26, yielding 64 addresses per block.',
        'Separate total addresses from assignable host addresses. Budget enough space for growth and provider reservations, and verify that a proposed subnet starts on its prefix boundary; 10.240.0.65/26 is a host-with-prefix rather than a canonical network identifier. Always plan for the smallest prefix that accommodates peak horizontal scale while preventing address exhaustion.',
        'A VPC (Virtual Private Cloud) subnet range is expressed in CIDR notation. Google Cloud enforces specific prefix boundaries: primary VPC subnets must have a prefix length between /8 and /29 inclusive. A /30, /31, or /32 cannot be provisioned as a primary VPC subnet. Furthermore, specialized Google Cloud managed services mandate fixed prefix sizes: Serverless VPC Access connectors require an exact /28 subnet, and Cloud SQL Private Services Peering typically reserves a /24 or /16 allocation. Use the same arithmetic for its address plan, then apply the documented provider rules before assigning VM addresses.', ['python', 'subnets']),
    '''<table><caption>Comprehensive IPv4 CIDR Prefix Reference (/8 through /32)</caption><thead><tr><th>Prefix</th><th>Subnet Mask</th><th>Total Addresses (2^(32-N))</th><th>Conventional Usable (2^(32-N) - 2)</th><th>GCP Primary Assignable (2^(32-N) - 4)</th><th>Architectural Cloud Role &amp; Common Allocations</th></tr></thead><tbody>
<tr><td>/8</td><td>255.0.0.0</td><td>16,777,216</td><td>16,777,214</td><td>16,777,212</td><td>Entire RFC 1918 Class A private block; maximum allowed VPC network size</td></tr>
<tr><td>/12</td><td>255.240.0.0</td><td>1,048,576</td><td>1,048,574</td><td>1,048,572</td><td>RFC 1918 Class B private block; large multi-datacenter enterprise WAN aggregation</td></tr>
<tr><td>/16</td><td>255.255.0.0</td><td>65,536</td><td>65,534</td><td>65,532</td><td>Standard large regional VPC network; GKE cluster-wide Pod CIDR allocation</td></tr>
<tr><td>/18</td><td>255.255.192.0</td><td>16,384</td><td>16,382</td><td>16,380</td><td>Medium-large regional cloud block; high-density container cluster</td></tr>
<tr><td>/20</td><td>255.255.240.0</td><td>4,096</td><td>4,094</td><td>4,092</td><td>Large enterprise workload subnet; multi-tier production environment</td></tr>
<tr><td>/22</td><td>255.255.252.0</td><td>1,024</td><td>1,022</td><td>1,020</td><td>Corporate departmental subnet; Kubernetes service cluster CIDR</td></tr>
<tr><td>/24</td><td>255.255.255.0</td><td>256</td><td>254</td><td>252</td><td>Standard application subnet (Class C equivalent); web and API serving tiers</td></tr>
<tr><td>/25</td><td>255.255.255.128</td><td>128</td><td>126</td><td>124</td><td>Half /24 split; dual availability zone application deployment</td></tr>
<tr><td>/26</td><td>255.255.255.192</td><td>64</td><td>62</td><td>60</td><td>Worked exercise split (quarter /24); microservice or batch worker tier</td></tr>
<tr><td>/27</td><td>255.255.255.224</td><td>32</td><td>30</td><td>28</td><td>Dedicated database tier; Cloud SQL private services peering block</td></tr>
<tr><td>/28</td><td>255.255.255.240</td><td>16</td><td>14</td><td>12</td><td>Serverless VPC Access connector subnet (exact /28 required by Google Cloud)</td></tr>
<tr><td>/29</td><td>255.255.255.248</td><td>8</td><td>6</td><td>4</td><td>Minimum allowable Google Cloud VPC subnet primary range; bastion host subnet</td></tr>
<tr><td>/30</td><td>255.255.255.252</td><td>4</td><td>2</td><td>0 (Ineligible in GCP VPC)</td><td>Conventional point-to-point router link; disallowed as GCP VPC primary subnet</td></tr>
<tr><td>/31</td><td>255.255.255.254</td><td>2</td><td>2 (RFC 3021)</td><td>0 (Ineligible in GCP VPC)</td><td>Point-to-point link without network/broadcast addresses (RFC 3021)</td></tr>
<tr><td>/32</td><td>255.255.255.255</td><td>1</td><td>1</td><td>0 (Ineligible in GCP VPC)</td><td>Single host route; loopback interface; VPC firewall exact-match target</td></tr>
</tbody></table>''',
    '''<div class="callout"><strong>Worked binary boundary: where does .75 belong?</strong><p>For a /26, the last-octet mask is 11000000 (decimal 192). Address .75 is 01001011; bitwise AND with 11000000 gives 01000000 (decimal 64), so the network is .64. The six remaining bits span offsets 0–63, making its broadcast .127. The four borrowed-bit combinations 00, 01, 10, and 11 therefore start at .0, .64, .128, and .192.</p><p>For 10.240.0.0/20, the third octet ranges from 0 through 15 and the full block ends at 10.240.15.255. For 10.240.0.0/16, the final two octets vary and the block ends at 10.240.255.255. These are address calculations, not allocated cloud networks.</p></div>''',
    subtopic(T2_TITLES[1],
        f'{keyword("RFC 1918")} defines three private blocks: 10.0.0.0/8, 172.16.0.0/12 (172.16 through 172.31), and 192.168.0.0/16. These blocks were established specifically for internal corporate networks, datacenter fabrics, and Virtual Private Clouds that do not require globally unique public routability. Public Internet routers and transit providers drop all RFC 1918 traffic by policy; these ranges are never advertised over global BGP. In addition, RFC 6598 reserves 100.64.0.0/10 as Shared Address Space for Carrier-Grade NAT (CGNAT), which cloud providers frequently utilize for managed internal routing, such as Private Google Access and link-local metadata services (169.254.169.254). Different isolated organizations may independently reuse private ranges. For example, 172.20.1.1 is in an RFC 1918 private block; 198.51.100.1 (from RFC 5737 documentation space) is outside RFC 1918. A private address provides address space conservation and network segmentation, but does not by itself make an application secure.',
        'Record ownership and allocation boundaries of each allocated range. If two networks that must communicate reuse the same destination space, ordinary address-based routing cannot distinguish them without additional design. Peering two VPCs or connecting on-premises infrastructure via Cloud VPN or Dedicated Interconnect with overlapping private CIDRs causes severe routing conflicts and packet drops. Non-overlapping allocations make future connectivity straightforward and avoid complex multi-NAT proxying.',
        'Google Cloud permits private IPv4 ranges for subnets. Workloads deployed in private subnets cannot reach the public Internet directly; outbound connectivity requires Cloud NAT or proxy gateways, while inbound access requires external Application Load Balancers or Cloud VPN tunnels. The address plan must account for all other networks that will connect to the VPC; creating a private CIDR is not proof that routes, firewall policy, or authentication are correct.', ['private']),
    subtopic(T2_TITLES[2],
        f'{keyword("ARP")} (Address Resolution Protocol, RFC 826) learns the link-layer address (MAC) for an IPv4 neighbor on a local Ethernet segment. When an application initiates communication, the operating system evaluates whether the destination IP is on the local subnet (on-link) or remote (off-link). For an on-link destination, the host broadcasts an ARP Request ("Who has IP X? Tell Y") to Ethernet broadcast MAC FF:FF:FF:FF:FF:FF. All hosts in the broadcast domain receive this frame; the target host replies with a unicast ARP Reply containing its MAC address. For an off-subnet destination, the host routes toward its default gateway; the neighbor resolved via ARP is the selected local gateway, not the remote host! In contrast, {keyword("NDP")} (Neighbor Discovery Protocol, RFC 4861) uses IPv6 control messages over ICMPv6 to eliminate the broadcast storms inherent to IPv4 ARP. NDP transmits Neighbor Solicitation (NS, ICMPv6 Type 135) to a Solicited-Node Multicast Address (ff02::1:ffxx:xxxx/104), ensuring only relevant network interfaces process the request. The target responds with a Neighbor Advertisement (NA, ICMPv6 Type 136). NDP also performs Router Solicitation/Advertisement (RS/RA) for Stateless Address Autoconfiguration (SLAAC).',
        'Keep final destination and next hop separate across every routing boundary. In the end-to-end packet journey from application to application: L7 generates payload, L4 adds transport ports, L3 adds IP headers and performs route table lookup. If the destination is off-link, L3 chooses the Next Hop Gateway IP. At the L2/L3 boundary, ARP (or NDP) resolves the MAC address of that NEXT HOP, NOT the remote host. The L2 Ethernet frame is addressed to the gateway MAC, while the L3 IP destination remains the remote host. Intermediate routers strip the incoming L2 header, decrement TTL, inspect the unchanged L3 destination, perform route lookup, and rewrite a NEW L2 header with the router outgoing MAC and the next-hop MAC. IP addresses remain constant end-to-end (without NAT); MAC addresses change on every link layer hop.',
        'This conventional Ethernet model teaches address selection. Google Cloud VPC uses Andromeda software-defined networking; its virtual default gateway behavior is documented separately. Compute Engine VMs communicate through virtual NICs (virtio-net or gVNIC); Andromeda encapsulates guest packets into Geneve/SDN headers and switches them directly across Jupiter datacenter fabrics without physical router bottlenecks or broadcast storms. Do not treat a guest neighbor entry as a discovery of physical cloud topology.', ['arp', 'ndp']),
    '''<table><caption>Application-to-Application End-to-End Packet Journey: ARP/NDP &amp; Routing Mechanisms</caption><thead><tr><th>Step / Boundary</th><th>Layer</th><th>Protocol &amp; Action</th><th>Addressing State &amp; Link-Layer Role</th></tr></thead><tbody>
<tr><td>1. App Generation</td><td>L7 Application</td><td>HTTP GET request initiated to http://10.240.0.75:8080/order</td><td>Payload generated; handed to transport socket</td></tr>
<tr><td>2. Transport Encapsulation</td><td>L4 Transport</td><td>TCP adds header with Source Port 49152, Dest Port 8080</td><td>SYN sequence initialized; port demux established</td></tr>
<tr><td>3. Network Encapsulation</td><td>L3 Network</td><td>IP adds header with Source 10.240.0.10, Destination 10.240.0.75</td><td>TTL=64; IP addresses set end-to-end</td></tr>
<tr><td>4. Route Lookup</td><td>L3 Network</td><td>Kernel evaluates netmask: 10.240.0.75 is outside /26 (off-link)</td><td>Default route matches gateway 10.240.0.1; Next Hop = 10.240.0.1</td></tr>
<tr><td>5. Neighbor Resolution</td><td>L2/L3 Boundary</td><td>Host A checks ARP cache for 10.240.0.1 (NDP NS/NA in IPv6)</td><td>ARP learns Gateway MAC R-left; remote host B is NOT ARPed!</td></tr>
<tr><td>6. Frame Encapsulation</td><td>L2 Data Link</td><td>Ethernet frame created: Src MAC=A, Dst MAC=R-left</td><td>L2 frame sent to gateway; L3 destination remains 10.240.0.75</td></tr>
<tr><td>7. Router Ingress</td><td>L1/L2/L3 Router</td><td>Router R receives frame on R-left, validates MAC, strips L2 header</td><td>TTL decremented (63); checksum verified; route lookup performed</td></tr>
<tr><td>8. Router Egress ARP</td><td>L2/L3 Boundary</td><td>Route matches connected 10.240.0.64/26 on R-right; ARPs for .75</td><td>Next hop IS host B; Router ARPs on egress segment for B MAC</td></tr>
<tr><td>9. Frame Re-encapsulation</td><td>L2 Data Link</td><td>Router creates NEW frame: Src MAC=R-right, Dst MAC=B</td><td>L2 MACs rewritten; L3 IP addresses remain unchanged!</td></tr>
<tr><td>10. Host B Delivery</td><td>L2/L3/L4/L7 Host B</td><td>B validates MAC, strips L2, matches local IP, demuxes TCP to port 8080</td><td>Payload enqueued in socket receive buffer; app executes read()</td></tr>
</tbody></table>''',
    subtopic(T2_TITLES[3],
        'The four /26 network addresses are .0, .64, .128, and .192; their broadcast addresses are .63, .127, .191, and .255. Each covers 64 addresses. In conventional IPv4 subnet arithmetic, the network and broadcast addresses are excluded from host assignment for these /26 examples, providing 62 usable host addresses.',
        'A complete allocation artifact records network, broadcast, range size, and ownership. Do not copy one provider’s reservation formula to another provider or equate a mathematically valid range with an approved production allocation.',
        'For a primary IPv4 subnet range, Google Cloud reserves its first two and last two addresses: the first address is the network identifier (.64), the second address is the default gateway (.65), the second-to-last address is reserved by Google Cloud for future expansion (.126), and the last address is the broadcast address (.127). In 10.240.0.64/26 these leave .66–.125 (exactly 60 assignable addresses). This is a primary-range comparison; secondary IPv4 ranges (such as those used by GKE for Pods and Services) have zero provider reservations, and all secondary addresses remain usable. In comparison, AWS and Azure each reserve five addresses per subnet.', ['subnets']),
    '''<table><caption>Worked /24 split: conventional subnet boundaries and GCP primary-range comparison</caption><thead><tr><th>Network</th><th>Broadcast</th><th>Conventional host span (62)</th><th>GCP primary assignable span (60)</th></tr></thead><tbody>
<tr><td>10.240.0.0/26</td><td>10.240.0.63</td><td>.1–.62</td><td>.2–.61</td></tr>
<tr><td>10.240.0.64/26</td><td>10.240.0.127</td><td>.65–.126</td><td>.66–.125</td></tr>
<tr><td>10.240.0.128/26</td><td>10.240.0.191</td><td>.129–.190</td><td>.130–.189</td></tr>
<tr><td>10.240.0.192/26</td><td>10.240.0.255</td><td>.193–.254</td><td>.194–.253</td></tr>
</tbody></table>''',
    subtopic(T2_TITLES[4],
        f'The {keyword("next hop")} is the immediate neighbor or gateway interface to which a host forwards an off-link packet. In the supplied model, Host A (10.240.0.10/26) first evaluates destination 10.240.0.75 against its routing table. The destination does not match A’s local subnet, so the default route selects gateway 10.240.0.1. Host A resolves gateway .1 via ARP and sends an Ethernet frame to R-left. Router R possesses connected interfaces on both subnets: 10.240.0.1/26 on the left and 10.240.0.65/26 on the right. When R receives the frame, it executes a Longest Prefix Match (LPM) route lookup, selects connected interface .65, decrements TTL, ARPs for host B (.75), and transmits a new Ethernet frame. The IP destination remains B when no NAT is involved.',
        'Label both forward and return paths. Routing is fundamentally unidirectional: a host can successfully transmit a packet to a remote destination, yet complete failure occurs if the remote host lacks a valid return route. On Host A, a default route via .1 handles off-subnet traffic; on Host B, the default route via .65 enables the reply. For the simplified route table used here, the longest matching prefix chooses the more specific destination route over broader defaults.',
        'Use this as a foundation for reading Google Cloud VPC routes. VPC routing evaluates destination CIDR matches, route priorities, and route categories (default routes, subnet routes, dynamic BGP routes, and custom static routes). The VPC virtual default gateway is not the pingable physical router drawn in this supplied lab; it is an Andromeda software-defined networking endpoint distributed across Google datacenter hosts, avoiding single-router choke points.', ['routes']),
    NEXT_HOP_SVG,
], '10.240.0.75 falls in 10.240.0.64/26, outside A’s 10.240.0.0/26. A forwards via .1; R forwards on its .65 interface; B receives the packet and replies via .65.',
    'The split and route choices are calculable offline. Neither the worksheet nor its arrows prove live reachability, neighbor resolution, firewall permission, or return-path success.')

T3_TITLES = ['NIC receive buffers, DMA, and driver notification', 'Linux NAPI receive processing', 'IP input and local delivery', 'Transport demultiplexing and application reads']
T3_TECH = discussion(T3_TITLES, [
    subtopic(T3_TITLES[0],
        f'A {keyword("receive queue")} holds arriving work for the network device/driver. DMA (Direct Memory Access) lets a device transfer data to memory; an IRQ (interrupt request) can notify a CPU (central processing unit) of work. For example, the arrival of a frame can make a receive buffer ready before a user process knows anything arrived. Exact buffering and notification depend on the device and driver.',
        'Separate interface/driver evidence from application logs. A reported request failure does not automatically mean the NIC dropped its frame. Compare signals at adjacent boundaries before choosing a fix.',
        'Compute Engine exposes a virtual NIC to the guest. gVNIC (Google Virtual NIC) is one documented interface option. A guest’s driver observations describe that interface, not Google’s complete physical receive path.', ['gvnic']),
    subtopic(T3_TITLES[1],
        f'{keyword("NAPI")} is Linux’s network polling/processing mechanism, historically called New API. A driver can schedule polling after notification; a receive-work budget limits a poll’s work. Interrupts, polling, and threaded modes are implementation choices, so “one packet always causes one interrupt” is not a reliable model.',
        'Batching can reduce notification overhead but consumes processing capacity. Investigate the actual driver and kernel rather than copying a universal queue size or assuming an aggregate CPU figure identifies the bottleneck.',
        'On a Linux Compute Engine VM (virtual machine), Linux driver behavior and the selected virtual NIC are separate evidence sources. The NAPI documentation explains the guest mechanism; gVNIC documentation identifies the interface option. No VM or tuning is required today.', ['napi']),
    subtopic(T3_TITLES[2],
        'The receive path interprets link/IP headers and applies relevant input processing and policy. A destination addressed to this host takes local delivery; a transit packet requires forwarding. For the supplied host B=.75, the local-delivery branch is appropriate. An input-policy drop occurs before an application reads bytes.',
        'A diagram needs a branch boundary: local destination versus transit destination. Observe where delivery stops before assigning ownership to network policy, transport, or the application. This simplified path omits detailed hooks and offload ordering.',
        'A Compute Engine guest’s input processing cannot establish which upstream VPC route or policy allowed the traffic. Future GCP troubleshooting must combine guest evidence with the documented cloud route/policy context.', ['layers', 'routes']),
    '''<div class="callout"><strong>Local delivery versus forwarding</strong><p>On host B, .75 identifies B itself, so the packet continues toward its transport socket. On router R, .75 identifies a destination beyond R’s incoming interface, so the model uses forwarding and an outgoing link. A router is not required to deliver every transit packet to one of its own application sockets. This distinction prevents treating an intermediate gateway as the final application endpoint.</p></div>''',
    subtopic(T3_TITLES[3],
        f'{keyword("Demultiplexing")} means choosing which conversation receives arriving data. For established TCP, protocol plus local/remote IP addresses and ports identify a connection. A listening socket handles new connection establishment; an accepted socket carries that connection’s bytes. A receive buffer can hold bytes before the process reads them, and the application may still reject the request after reading.',
        'Distinguish interface receipt, transport delivery, application read, and business completion. If the supplied evidence says “queued=yes, application read=no”, inspect the application’s progress before proposing a NIC replacement or an unmeasured kernel tuning change.',
        'The same responsibility separation applies to a Linux application on Compute Engine. A local trace can inform the guest investigation; it cannot prove managed load-balancer internals or a fixed cloud latency.', ['tcp']),
    '''<div class="callout"><strong>Connection queues and data buffers are different</strong><p>A new TCP connection has establishment work before an application accepts it. Conceptually, incomplete handshakes and established connections waiting for acceptance are different from payload bytes waiting on an accepted connection. The NIC diagram deliberately follows established traffic; an accept-queue observation cannot by itself reveal how much request data an application has read.</p><p>For example, a process can accept a connection and then block on another dependency. TCP may deliver bytes to its socket while the application makes no progress. Conversely, the application can read a request and return a failure response. Diagnose the last known successful boundary and the next missing signal before choosing a fix; a larger queue changes buffering, not the correctness of the operation.</p></div>''',
    NIC_SVG,
    '''<table><caption>Architecture-path evidence boundaries</caption><thead><tr><th>Step</th><th>Owner / signal</th><th>What remains unproved</th></tr></thead><tbody>
<tr><td>NIC and driver</td><td>Interface/driver receive evidence</td><td>Socket delivery</td></tr><tr><td>IP local delivery</td><td>Address and policy decision</td><td>Application readiness</td></tr><tr><td>Transport/socket</td><td>Connection and queued-byte evidence</td><td>Process read or successful transaction</td></tr><tr><td>Application</td><td>Read and response records</td><td>Customer acceptance or persistent business result</td></tr>
</tbody></table>''',
], 'In the synthetic case, the interface and IP path pass, TCP places bytes on the correct socket, but the process does not read. The first missing observation is at the process-read boundary; “stalled worker” is a hypothesis to investigate.',
    'The exercise follows supplied records. It does not capture physical NIC ingress, assert a specific NAPI schedule, or reproduce packet drops on a GCP VM.')

T4_TITLES = ['IPC: the process boundary', 'Unix domain sockets and local access', 'Loopback TCP and remote RPC boundaries']
T4_TECH = discussion(T4_TITLES, [
    subtopic(T4_TITLES[0],
        f'{keyword("Inter-process communication")} lets separate processes exchange information. A pipe can carry a stream from one program to another; a local socket provides a named endpoint. For example, an application and a local helper can communicate without crossing a subnet. This is a short companion comparison, not a deployment exercise.',
        'Write down whether the peers share a host and how ownership/lifecycle are managed. The same-host requirement is a design constraint: splitting the processes across machines changes the communication mechanism needed.',
        'For a Linux application using a local Cloud SQL Auth Proxy process, the application-to-proxy endpoint and the proxy-to-database connection are different boundaries. A local endpoint choice does not make the database itself local.', ['proxy']),
    subtopic(T4_TITLES[1],
        f'A {keyword("Unix domain socket")} (UDS) is an operating-system-local socket, commonly addressed by a filesystem pathname rather than an IP/port. On Linux, pathname-directory and socket permissions affect access. For example, a client expects a listener at /tmp/helper.sock; a stale file without a listener is insufficient. A UDS cannot directly connect a client on another machine.',
        'Check OS support, pathname visibility, permissions, and process lifecycle. Filesystem access is not a complete substitute for application authorization. Do not promise a universal speedup without representative measurement.',
        'The Cloud SQL Auth Proxy offers Unix sockets in supported environments. Review its documented platform/client limitations before choosing that option; do not infer support for every runtime or database configuration.', ['unix', 'proxy']),
    '''<div class="callout"><strong>Endpoint presence is not service availability</strong><p>A pathname can remain after its owning process exits. A filesystem entry is therefore different from a live listening socket, and a listening socket is different from a valid application response. Before removing a supposedly stale path in a real deployment, identify its owner and lifecycle; deleting a live socket path can break new clients. This day only classifies supplied cases and removes files its worksheet created.</p></div>''',
    subtopic(T4_TITLES[2],
        f'{keyword("Loopback TCP")} uses a local IP endpoint such as 127.0.0.1:9000 and still uses TCP. That address refers to the client’s own network namespace, not another VM. An {keyword("RPC")} (remote procedure call) is an application interaction that invokes an operation on a server; frameworks such as gRPC define message contracts. RPC is an application abstraction, not another OSI layer or a promise that the server is nearby.',
        'Use local mechanisms only for local peers. For remote peers, identify a reachable service address, transport, authentication, and request contract. A connected socket still does not prove the called operation succeeded; retry design belongs to later study.',
        'Google’s API design guide describes resource-oriented APIs usable with HTTP/REST and RPC. It does not imply every Google API uses one wire format. Here you record a future design question rather than deploy Cloud SQL, GKE, or an API service.', ['grpc', 'api']),
    '''<table><caption>Static communication comparison: no diagram is needed</caption><thead><tr><th>Mechanism</th><th>Endpoint</th><th>Boundary to check</th></tr></thead><tbody>
<tr><td>Unix socket</td><td>Local path, e.g. /tmp/helper.sock</td><td>Same OS; listener, path visibility, Linux permissions</td></tr><tr><td>Loopback TCP</td><td>127.0.0.1:9000</td><td>Same network namespace; port listener; application authorization</td></tr><tr><td>Network RPC</td><td>Remote service address and operation</td><td>Network reachability plus authentication and message contract</td></tr>
</tbody></table>''',
], 'Application A and helper B share a Linux host, so a supported UDS can be considered. After B moves to a different VM, A must use a reachable network endpoint; copying /tmp/helper.sock to A cannot expose B’s listener.',
    'A design table predicts suitability. It neither measures IPC performance nor demonstrates Cloud SQL access, authentication, or compatibility.')


LAYER_CHECK = """import csv
from pathlib import Path
rows = list(csv.DictReader(Path("classification.csv").open()))
expected = {"no_route": "L3", "tcp_refused": "L4", "http_503": "L7"}
assert {r["case"]: r["first_failed_boundary"] for r in rows} == expected, "Recheck the responsibility map"
assert all(r["not_proven"].strip() for r in rows), "Record an evidence limit per row"
Path("layer-check.txt").write_text("PASS: 3 supplied cases classified; each has an evidence limit\\n")
print(Path("layer-check.txt").read_text(), end="")"""

LAYER_LAB = lab('Classify evidence at the L3, L4, and L7 boundaries',
    'Classify supplied records and identify what each successful lower-layer observation does not establish.',
    'Three classified cases plus a readiness design note, labeled synthetic/tabletop.', [
    stage(1, 'Preflight and isolate the worksheet', 'Run the commands in a fresh terminal. Record the printed workspace path; all following relative files belong there.', 'Python version and a unique local workspace.', 'preflight.txt', workspace('d002-layers', preflight_text='Python available; local/tabletop only; GCP untested')),
    stage(2, 'Prepare supplied diagnostic records', 'Create this literal fixture. The strings are teaching records, not actual terminal output from a network test.', 'Three records: no route, refused connection, and HTTP 503.', 'cases.txt', write_file('cases.txt', '''SOURCE=synthetic teaching fixture
no_route: destination=10.240.0.75 route_match=none
tcp_refused: route_match=yes connect=refused
http_503: route_match=yes connect=success HTTP=503''')),
    stage(3, 'Author boundary classifications', 'Author the classification CSV mapping each synthetic case to its first failed boundary and evidence limit.', 'Exactly three case rows with a layer classification and evidence limit.', 'classification.csv', write_file('classification.csv', '''case,first_failed_boundary,not_proven
no_route,L3,Destination unreachable at network layer; transport unattempted
tcp_refused,L4,Port closed or listener absent; application unreached
http_503,L7,Service unavailable; backend dependency failure unverified''')),
    stage(4, 'Check the planned classifications', 'Create and run this offline checker. If an assertion fails, correct the worksheet; do not alter the expected classifications to hide an error.', 'PASS for the three classifications; mismatches stop execution.', 'layer-check.txt', write_file('check_layers.py', LAYER_CHECK) + 'python3 check_layers.py'),
    stage(5, 'Inspect the classified evidence', 'Print your worksheet and compare it with cases.txt: no route is L3, refusal is L4 given a route, and HTTP 503 is L7 given successful transport. Confirm each row names a distinct unproved fact.', 'Classification includes boundaries and limits rather than just layer names.', 'layer-check.txt', 'cat cases.txt\ncat classification.csv\ncat layer-check.txt\necho "INSPECTED: responsibility boundaries verified" >> layer-check.txt'),
    stage(6, 'Challenge a port-only readiness decision', 'Create the supplied decision challenge. In an editor add an answer line explaining why the port signal cannot certify checkout readiness.', 'The answer states that a reachable port does not establish successful HTTP/business operation.', 'readiness-challenge.txt', write_file('readiness-challenge.txt', '''SOURCE=synthetic design challenge
TCP probe=success
checkout request=HTTP 503
Question: Does the port probe prove checkout readiness? Explain using the failed boundary.''')),
    stage(7, 'Record the fix and GCP design question', 'Append the application investigation recommendation, Layer 7 health check design criteria, and GCP limits to readiness-challenge.txt.', 'A topic-specific decision distinguishes detection from repair.', 'readiness-challenge.txt', """cat << 'EOF' >> readiness-challenge.txt

Remediation Note:
1. Application investigation: Inspect application logs and downstream service dependencies before blaming network routes.
2. Readiness criteria: In Google Cloud Load Balancing, configure Layer 7 HTTP health checks evaluating HTTP 200 OK responses with matching content, rather than basic Layer 4 TCP port probes.
3. Diagnostic boundary: A passing TCP probe establishes network reachability; it does not certify database connectivity, backend worker readiness, or HTTP response code validity.
4. GCP deployment status: Untested on cloud infrastructure.
EOF"""),
    stage(8, 'Close out and preserve evidence', 'Remove only the temporary checker script while preserving all durable evidence files.', 'Evidence remains; temporary script is removed.', 'classification.csv', """python3 - <<'EOF'
from pathlib import Path
for name in ("check_layers.py",):
    Path(name).unlink(missing_ok=True)
print("Evidence retained:", sorted(p.name for p in Path.cwd().iterdir()))
EOF"""),
], 'classification.csv has all three correct boundaries and evidence limits; layer-check.txt passes; the readiness note distinguishes detection from remediation. This supports the next-hop artifact’s evidence-limit statement.',
    'File not found: run from the Stage 1 workspace. CSV mismatch: use the exact case identifiers and header. A port success plus HTTP 503 belongs to the application boundary; it does not establish the dependency root cause.',
    'day-002-topic-01.md')

SUBNET_SCRIPT = """import csv, ipaddress, json
from pathlib import Path
parent = ipaddress.ip_network("10.240.0.0/24")
children = list(parent.subnets(new_prefix=26))
rows = []
for n in children:
    first, last = int(n.network_address), int(n.broadcast_address)
    rows.append({"network": str(n), "broadcast": str(n.broadcast_address), "total": n.num_addresses,
                 "conventional_first": str(ipaddress.ip_address(first + 1)),
                 "conventional_last": str(ipaddress.ip_address(last - 1)),
                 "gcp_primary_first": str(ipaddress.ip_address(first + 2)),
                 "gcp_primary_last": str(ipaddress.ip_address(last - 2)), "gcp_primary_count": n.num_addresses - 4})
with Path("subnet-ranges.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
Path("subnet-ranges.json").write_text(json.dumps(rows, indent=2) + "\\n")
for row in rows:
    print(row["network"], row["broadcast"], "total=", row["total"], "GCP primary assignable=", row["gcp_primary_count"])"""

SUBNET_VERIFY = """import ipaddress, json
from pathlib import Path
rows = json.loads(Path("subnet-ranges.json").read_text())
networks = [ipaddress.ip_network(r["network"]) for r in rows]
assert len(networks) == 4 and sum(n.num_addresses for n in networks) == 256
assert [str(n.network_address) for n in networks] == ["10.240.0.0", "10.240.0.64", "10.240.0.128", "10.240.0.192"]
assert [str(n.broadcast_address) for n in networks] == ["10.240.0.63", "10.240.0.127", "10.240.0.191", "10.240.0.255"]
assert all(not a.overlaps(b) for i,a in enumerate(networks) for b in networks[i+1:])
assert all(r["gcp_primary_count"] == 60 for r in rows)
Path("subnet-check.txt").write_text("PASS: four /26 blocks, 256 total addresses, no overlap, correct boundaries\\n")
print(Path("subnet-check.txt").read_text(), end="")"""

SUBNET_LAB = lab('Split 10.240.0.0/24 into four equal networks',
    'Calculate four ranges and compare conventional host arithmetic with GCP primary IPv4 reservations.',
    'A checked subnet table with correct network/broadcast addresses; no VPC resources created.', [
    stage(1, 'Verify the calculation environment', 'Run the commands. Python’s ipaddress module is included in its standard library; no package installation is needed.', 'A unique workspace; the parent contains 256 addresses.', 'preflight.txt', workspace('d002-subnets', preflight_text='Parent 10.240.0.0/24 contains 256 addresses') + 'python3 -c \'import ipaddress; print("Parent addresses:", ipaddress.ip_network("10.240.0.0/24").num_addresses)\''),
    stage(2, 'Prepare the allocation inputs', 'Create this planning brief. Before continuing, calculate the new prefix: four equal blocks require two additional network bits.', 'Parent /24, four children, /26 prediction.', 'allocation-inputs.txt', write_file('allocation-inputs.txt', '''parent=10.240.0.0/24
children=4
new_prefix=26
owners=web,app,database,management
mode=offline planning; no deployed subnets''')),
    stage(3, 'Author the calculation', 'Write the complete script below. Read how new_prefix=26 yields four blocks and how the primary-range comparison excludes four reserved addresses.', 'A script with explicit inputs and two output formats.', 'subnet_math.py', write_file('subnet_math.py', SUBNET_SCRIPT)),
    stage(4, 'Calculate the four ranges', 'Run the script and view the CSV. Match the network/broadcast pairs to the worked table in Part 2.', 'Networks .0, .64, .128, .192; broadcasts .63, .127, .191, .255; 64 addresses each.', 'subnet-ranges.csv', 'python3 subnet_math.py\ncat subnet-ranges.csv'),
    stage(5, 'Verify boundaries and reservations', 'Run the complete checker below. Verify that no children overlap and that each contains 60 assignable addresses under GCP primary rules.', 'No overlapping children; 256 total addresses; 60 primary-range assignable addresses per /26.', 'subnet-check.txt', write_file('verify_subnets.py', SUBNET_VERIFY) + 'python3 verify_subnets.py'),
    stage(6, 'Challenge a nonaligned network input', 'Run a strict parse of 10.240.0.65/26. This is a host address with network bits set in the host portion; record the rejection and distinguish it from the canonical .64/26 network.', 'host bits set rejection; the normalized network is 10.240.0.64/26.', 'alignment-check.txt', """python3 - <<'EOF'
import ipaddress
from pathlib import Path
try:
    ipaddress.ip_network("10.240.0.65/26", strict=True)
except ValueError as error:
    text = f"REJECTED: {error}\\nCanonical containing network: {ipaddress.ip_network('10.240.0.65/26', strict=False)}\\n"
    Path("alignment-check.txt").write_text(text)
    print(text, end="")
else:
    raise AssertionError("Expected a nonaligned network to be rejected")
EOF"""),
    stage(7, 'Record allocation ownership and limits', 'Author subnet-plan.md documenting owner mapping, host placements, and GCP reservation boundaries.', 'A reviewable owner map linked to numerical evidence.', 'subnet-plan.md', """cat << 'EOF' > subnet-plan.md
# Subnet Allocation Plan: 10.240.0.0/24 Split

- **Parent Block:** 10.240.0.0/24 (256 total IPv4 addresses)
- **Subnet 1:** 10.240.0.0/26 (Broadcast: 10.240.0.63, Conventional: .1-.62, GCP Primary: .2-.61, Owner: web)
- **Subnet 2:** 10.240.0.64/26 (Broadcast: 10.240.0.127, Conventional: .65-.126, GCP Primary: .66-.125, Owner: app)
- **Subnet 3:** 10.240.0.128/26 (Broadcast: 10.240.0.191, Conventional: .129-.190, GCP Primary: .130-.189, Owner: database)
- **Subnet 4:** 10.240.0.192/26 (Broadcast: 10.240.0.255, Conventional: .193-.254, GCP Primary: .194-.253, Owner: management)

## Destination Host Placement
- Destination host 10.240.0.75 resides strictly in Subnet 2 (10.240.0.64/26, app tier).
- Traffic from Subnet 1 (10.240.0.10) to 10.240.0.75 is off-link and requires router forwarding.

## Evidence Boundary
- Primary IPv4 GCP comparison only; local calculation; GCP untested.
EOF"""),
    stage(8, 'Clean calculation inputs and preserve ranges', 'Remove only temporary scripts while preserving durable plan, CSV, JSON, and check files.', 'Five durable evidence files remain in the workspace.', 'subnet-plan.md', """python3 - <<'EOF'
from pathlib import Path
for name in ("subnet_math.py", "verify_subnets.py"):
    Path(name).unlink(missing_ok=True)
print("Evidence retained:", sorted(p.name for p in Path.cwd().iterdir()))
EOF"""),
], 'Four /26 rows, explicit network/broadcast addresses, 64 total addresses each, no overlap; primary-range comparison uses four reservations. Save alongside the labeled next-hop path from Exercise 3.',
    'Module missing: confirm this is Python 3. Wrong boundaries: verify parent=.0/24 and new_prefix=26. GCP counts apply only to primary IPv4 ranges; conventional ipaddress.hosts() alone does not model provider reservations.',
    'day-002-topic-02.md')

PATH_CHECK = """import csv
from pathlib import Path
rows = list(csv.DictReader(Path("next-hop-path.csv").open()))
expected = [("A", "10.240.0.75", "10.240.0.1", "R-left"),
            ("R", "10.240.0.75", "10.240.0.75", "B"),
            ("B-reply", "10.240.0.10", "10.240.0.65", "R-right")]
actual = [(r["sender"],r["ip_destination"],r["next_hop_ip"],r["frame_destination"]) for r in rows]
assert actual == expected, "Revisit subnet membership and the supplied router interfaces"
Path("path-check.txt").write_text("PASS: A forwards via .1; R delivers to .75; B replies via .65\\nTabletop only; no packet capture or live connectivity evidence\\n")
print(Path("path-check.txt").read_text(), end="")"""

PATH_LAB = lab('Trace the next hop and the destination receive path',
    'Trace A to B using the supplied Ethernet diagram, then locate the first unproved receive boundary.',
    'A labeled next-hop CSV, return-path note, NIC/socket sequence, and evidence-limit statement.', [
    stage(1, 'Preflight the supplied model', 'Create a separate workspace. Bring the Exercise 2 table as a reference; no system routes or interfaces will be modified.', 'A separate path workspace and a clear tabletop mode.', 'preflight.txt', workspace('d002-path', preflight_text='Supplied Ethernet topology; tabletop only; GCP untested')),
    stage(2, 'Prepare explicit host and router inputs', 'Create the supplied topology record and compare its values to the host-to-host diagram in Part 2. MAC names below are symbolic labels, not captured addresses.', 'Two /26 segments and a router directly attached to both.', 'topology.txt', write_file('topology.txt', '''SOURCE=synthetic conventional Ethernet model; no NAT
A=10.240.0.10/26 default_via=10.240.0.1 MAC=A
R-left=10.240.0.1/26 MAC=R-left
R-right=10.240.0.65/26 MAC=R-right
B=10.240.0.75/26 default_via=10.240.0.65 MAC=B
R has connected routes to 10.240.0.0/26 and 10.240.0.64/26''')),
    stage(3, 'Author the labeled next-hop path', 'Create next-hop-path.csv with routing and frame destination headers and author initial path notes.', 'A route labeled with both final IP destination and local frame destination.', 'next-hop-path.csv', """cat << 'EOF' > next-hop-path.csv
sender,ip_destination,next_hop_ip,frame_destination
A,10.240.0.75,10.240.0.1,R-left
R,10.240.0.75,10.240.0.75,B
B-reply,10.240.0.10,10.240.0.65,R-right
EOF
cat << 'EOF' > path-notes.md
# Next-Hop Path and Address Resolution Notes

## Step-by-Step Traversal (Host A to Host B)
1. Host A (10.240.0.10/26) identifies destination 10.240.0.75 as off-link (outside 10.240.0.0/26).
2. Host A queries route table: default route matches gateway 10.240.0.1.
3. Host A performs ARP resolution for NEXT HOP IP 10.240.0.1 (not host B). ARP learns gateway MAC R-left.
4. Host A sends Ethernet frame with Destination MAC R-left and IP Destination 10.240.0.75.
5. Router R receives frame on R-left, decrements TTL, inspects IP destination 10.240.0.75.
6. Router R route lookup matches connected interface 10.240.0.65/26.
7. Router R ARPs for 10.240.0.75 directly on the egress segment. Learns host B MAC.
8. Router R sends frame with Destination MAC B. IP destination remains 10.240.0.75.
9. Return path: Host B replies to 10.240.0.10 via gateway 10.240.0.65 (R-right MAC).
EOF"""),
    stage(4, 'Check the trace', 'Create and run the offline checker. A wrong next hop stops the check. Correct the worksheet using subnet membership; do not alter the checker’s model.', 'PASS: A uses .1, R resolves .75, B replies via .65.', 'path-check.txt', write_file('check_path.py', PATH_CHECK) + 'python3 check_path.py'),
    stage(5, 'Inspect destination NIC-to-socket boundaries', 'Append the six destination receive steps to path-notes.md in order and record diagnostic boundaries.', 'Six receive steps plus two explicit limits; no physical capture is claimed.', 'path-notes.md', """cat << 'EOF' >> path-notes.md

## Destination Receive Path (NIC to Application Socket)
1. NIC Receive Queue: Network interface receives Ethernet frame into ring buffer.
2. Driver Processing / DMA: Network driver DMA transfers frame bytes to host RAM; fires IRQ.
3. Linux NAPI Polling: Kernel schedules poll routine to batch process packets from ring buffer.
4. IP Input & Routing: IP layer validates checksum/headers; determines local delivery branch (matches B's IP).
5. Transport & Socket Buffer: TCP demultiplexes connection 4-tuple; payload placed in socket receive buffer.
6. Application Read: User process executes read()/recv() to consume bytes.

## Diagnostic Limits
- Loopback bypasses physical NIC, DMA, and driver queuing entirely.
- Queued socket bytes do not prove application read or business transaction success.
EOF"""),
    stage(6, 'Challenge the incorrect /24 mask', 'Run the calculation comparing A’s correct /26 with an erroneous /24. Record why the latter makes the off-subnet destination appear local.', '/26 says B is off-link; /24 incorrectly says it is on-link for this supplied segmented topology.', 'mask-challenge.txt', """python3 - <<'EOF'
import ipaddress
from pathlib import Path
destination = ipaddress.ip_address("10.240.0.75")
text = "".join(f"A prefix {prefix}: destination on-link={destination in ipaddress.ip_network(prefix)}\\n" for prefix in ("10.240.0.0/26", "10.240.0.0/24"))
Path("mask-challenge.txt").write_text(text)
print(text, end="")
EOF"""),
    stage(7, 'Diagnose the mask and document the GCP boundary', 'Append remediation notes and Google Cloud Andromeda SDN gateway distinction to path-notes.md.', 'A next-hop repair, return-path check, and honest cloud/receive limits.', 'path-notes.md', """cat << 'EOF' >> path-notes.md

## Mask Remediation & GCP Boundary Notes
- Configuration Fix: Restoring /26 on Host A ensures destination 10.240.0.75 is correctly recognized as off-link.
- Gateway Verification: Host A uses gateway 10.240.0.1; Host B return path uses gateway 10.240.0.65.
- Cloud SDN Distinction: The supplied diagram models conventional physical Ethernet routers with ARP broadcasts. In Google Cloud VPC, the default gateway (e.g. 10.240.0.1) is an Andromeda SDN software abstraction that forwards packets without physical router hops or broadcast ARP storms.
- GCP status: untested on cloud infrastructure.
EOF"""),
    stage(8, 'Close the trace and assemble exit evidence', 'Remove only the temporary checker script while preserving all durable path and diagnostic evidence files.', 'The roadmap exit evidence combines four correct ranges with a labeled next-hop path.', 'next-hop-path.csv', """python3 - <<'EOF'
from pathlib import Path
for name in ("check_path.py",):
    Path(name).unlink(missing_ok=True)
print("Evidence retained:", sorted(p.name for p in Path.cwd().iterdir()))
EOF"""),
], 'A→R uses gateway .1 and R-left frame destination; R→B uses .75/B; reply uses .65/R-right. Six receive steps are correctly ordered. The saved evidence labels supplied model, local calculation, GCP untested, and no physical capture.',
    'Wrong next hop: compare destination .75 with A’s .0–.63 block. Missing return path: use B’s .65 gateway in this model. A successful fixture check is not a real ping result or a verification of Google Cloud’s network fabric.',
    'day-002-topic-03.md')

IPC_CHECK = """import csv
from pathlib import Path
rows = list(csv.DictReader(Path("ipc-decisions.csv").open()))
expected = {"same_host_path": "UDS", "same_namespace_port": "loopback_TCP", "different_host": "network_RPC"}
assert {r["case"]:r["mechanism"] for r in rows} == expected, "Check locality before choosing an endpoint"
assert all(r["limit"].strip() for r in rows)
Path("ipc-check.txt").write_text("PASS: three communication boundaries classified; performance unmeasured\\n")
print(Path("ipc-check.txt").read_text(), end="")"""

IPC_LAB = lab('Choose a process-communication boundary',
    'Classify local path, loopback port, and remote application communication without promising performance.',
    'Three mechanism decisions plus a locality change note; no service or database deployed.', [
    stage(1, 'Prepare the companion worksheet', 'Run the commands in a fresh terminal. This short coverage checkpoint does not extend the day into RPC deployment or benchmarking.', 'A unique offline worksheet workspace.', 'preflight.txt', workspace('d002-ipc', preflight_text='Process communication comparison; tabletop only; GCP untested')),
    stage(2, 'Prepare the three locality cases', 'Create the exact inputs. Each names the endpoint requirement rather than prescribing a universal best mechanism.', 'Three explicit locality conditions.', 'ipc-inputs.txt', write_file('ipc-inputs.txt', '''SOURCE=synthetic design inputs
same_host_path: Linux peers on same host; client/server support a pathname socket
same_namespace_port: peers share one network namespace; client requires an IP/port API
different_host: peers are on different VMs; client invokes a remote operation''')),
    stage(3, 'Author mechanism choices and limits', 'Create ipc-decisions.csv using the header below and record mechanism choices and boundaries.', 'Three rows, each with a concrete compatibility/reachability limit.', 'ipc-decisions.csv', """cat << 'EOF' > ipc-decisions.csv
case,mechanism,limit
same_host_path,UDS,Requires same host; filesystem pathname permissions and directory traversal
same_namespace_port,loopback_TCP,Requires same network namespace; port listener and local authorization
different_host,network_RPC,Requires network reachability; TLS authentication and message schema contract
EOF"""),
    stage(4, 'Check the design classifications', 'Create and run the complete offline checker. It verifies this fixture’s classifications, not latency or cloud compatibility.', 'Three choices pass; missing limits or wrong locality choices fail.', 'ipc-check.txt', write_file('check_ipc.py', IPC_CHECK) + 'python3 check_ipc.py'),
    stage(5, 'Inspect local versus remote ownership', 'Print the worksheet and create ipc-note.md explaining local vs remote boundary differences.', 'The note names both process and network boundaries.', 'ipc-note.md', """cat ipc-inputs.txt
cat ipc-decisions.csv
cat ipc-check.txt
cat << 'EOF' > ipc-note.md
# Process Communication Boundaries: Local vs Remote

## Boundary Classification
- Case 1 (same_host_path): Unix Domain Socket (UDS) provides high-performance local IPC via kernel buffers without network stack overhead.
- Case 2 (same_namespace_port): Loopback TCP (127.0.0.1) operates within the local network namespace, allowing IP-based client libraries to connect locally.
- Case 3 (different_host): Network RPC (e.g. gRPC over HTTP/2) traverses physical or virtual networks to communicate with remote services.

## Architecture Ownership Limits
- A local proxy endpoint (such as Cloud SQL Auth Proxy on 127.0.0.1 or /tmp/cloudsql) and a remote database endpoint are separate architectural boundaries.
- Using a Unix socket to connect to the local proxy does not make the remote Cloud SQL database instance local.
EOF"""),
    stage(6, 'Challenge a move to another machine', 'Append the locality challenge to ipc-note.md and document why a Unix socket cannot span machines.', 'UDS locality is identified as the failed design assumption; no speed claim is made.', 'ipc-note.md', """cat << 'EOF' >> ipc-note.md

## Locality Challenge Diagnosis
- Challenge: Helper B is moved from Host A to a different VM, but Client A still attempts to connect via /tmp/helper.sock.
- Diagnosis: A Unix Domain Socket is strictly local to a single operating system kernel instance. Pathnames cannot be addressed across VM boundaries.
- Remediation: Client A must be reconfigured with a reachable network endpoint (IP address and port or DNS name), TLS certificate validation, and remote authentication credentials.
EOF"""),
    stage(7, 'Record the GCP design review', 'Append the Cloud SQL Auth Proxy documentation review and explicit evidence limits to ipc-note.md.', 'A compatibility question and explicit evidence limits instead of an invented benchmark.', 'ipc-note.md', """cat << 'EOF' >> ipc-note.md

## GCP Design Review & Cloud SQL Proxy Evaluation
- Primary Source: Consulted Google Cloud SQL documentation on Auth Proxy Unix sockets.
- Findings: Cloud SQL Auth Proxy supports Unix domain sockets on Linux and macOS, which provides secure local access without exposing local TCP ports.
- Evidence Limit: Local socket evaluation is a design analysis. GCP deployment, proxy installation, and database authentication were untested on live cloud infrastructure; latency and throughput remain unmeasured.
EOF"""),
    stage(8, 'Close out the design checkpoint', 'Remove the temporary checker script while preserving all durable IPC evidence files.', 'Three companion evidence files remain.', 'ipc-decisions.csv', """python3 - <<'EOF'
from pathlib import Path
for name in ("check_ipc.py",):
    Path(name).unlink(missing_ok=True)
print("Evidence retained:", sorted(p.name for p in Path.cwd().iterdir()))
EOF"""),
], 'Correct UDS/loopback_TCP/network_RPC fixture choices, one limit per row, a locality-change diagnosis, and explicit unmeasured/untested labels. This companion checkpoint is additional to the roadmap’s subnet/path exit evidence.',
    'CSV parse failure: use the exact header and quote fields containing commas. Wrong choice: a local pathname cannot directly address a listener on another VM. Do not resolve a compatibility question by asserting an unrun performance benchmark.',
    'day-002-topic-04.md')

TOPICS = [{'scenario': item} for item in [
    case('Synthetic Brightloaf checkout case: a port probe succeeds but the checkout operation returns HTTP 503.',
        'Customers cannot complete the operation; no transaction count, outage duration, or revenue estimate is supplied.',
        'Investigate using the supplied records; do not alter a deployed load balancer or claim a dependency failure without evidence.',
        'SOURCE=synthetic\nroute_match=yes\nTCP connect=success\nHTTP response=503\napplication dependency state=unknown',
        'The known design defect is treating transport reachability as checkout readiness. The underlying reason for HTTP 503 is unknown from these records.',
        ['Compare TCP connection success with the HTTP result.', 'Separate route/transport evidence from application readiness.', 'Request application logs and dependency evidence before naming the HTTP failure cause.'],
        ['Define an application readiness condition appropriate to the checkout operation and supported probe protocol.', 'Investigate and repair the actual application fault; avoid making all backends dependent on one brittle shared probe.'],
        'For this fixture, classify the first failing observed responsibility as L7. In a real repair, recheck both supported health criteria and the business request; neither outcome was run here.',
        'A passing HTTP endpoint may still omit dependencies or business invariants; probe behavior alone is not customer acceptance.'),
    case('Synthetic Brightloaf address-plan case: host A uses /24 although the supplied network allocates two separate /26 segments.',
        'A may seek the remote host locally instead of using its gateway, blocking the integration in this conventional Ethernet model.',
        'Keep the model’s router interfaces and address allocations fixed. Do not change the workstation’s actual IP configuration.',
        'SOURCE=synthetic\nallocated_A_subnet=10.240.0.0/26\nconfigured_A_prefix=10.240.0.0/24\ndestination_B=10.240.0.75\nobserved_neighbor_resolution=not supplied',
        'The supplied mask is inconsistent with the allocated subnet: /24 makes .75 appear local, whereas /26 makes it off-link. A live ARP failure is predicted rather than observed.',
        ['Compare .75 against the correct and incorrect address ranges.', 'Check A’s supplied default gateway .1 and B’s return gateway .65.', 'Identify neighbor-resolution output as missing evidence.'],
        ['In the supplied model restore A’s /26 mask and preserve its gateway .1.', 'Validate the four allocations and verify forward/return routing before any future deployment.'],
        'The offline membership calculation must show .75 outside .0/26 but inside .0/24. A future live test would additionally need neighbor/route and response evidence.',
        'A correct mask does not establish firewall permission or a working remote application.'),
    case('Synthetic Brightloaf receive-path case: bytes reach the socket but no process-read event is supplied.',
        'The request remains unanswered; the records do not supply a latency, packet-drop count, or measured user impact.',
        'Use the supplied established-connection records. No load burst, kernel tuning, or production fault injection is permitted by this exercise.',
        'SOURCE=synthetic\ninterface_received=yes\nIP_local_delivery=yes\nTCP_socket_bytes_queued=yes\napplication_read=no\napplication_response=absent',
        'The first missing progress signal is the application read. A blocked worker or scheduling delay is a candidate cause; the records do not establish which cause applies.',
        ['Walk NIC → driver → receive processing → IP → socket → process using the diagram.', 'Mark every supplied signal and the first absent one.', 'Request worker/scheduler evidence before proposing a particular fix.'],
        ['Diagnose the process’s actual wait or scheduling condition with application evidence.', 'Repair that condition, then inspect process reads and response validity; do not prescribe universal sysctl values.'],
        'The tabletop answer must identify the process-read boundary. A real post-fix check would require an observed read plus a valid response under a bounded workload; these are predictions here.',
        'An observed read alone would not prove database commit or complete business fulfillment.', True,
        ('Request reaches socket', 'Process does not read', 'No response supplied', 'Diagnose and repair wait', 'Read + response to verify')),
    case('Synthetic Brightloaf integration case: a helper moved to another VM, but the client still uses a same-host socket path.',
        'The local endpoint cannot reach the moved helper; no measured performance or business loss is supplied.',
        'Do not deploy a proxy or database. Review locality and client/server support with the supplied design inputs.',
        'SOURCE=synthetic\nclient_host=A\nhelper_host=B\nclient_endpoint=/tmp/helper.sock\nshared_kernel=no\nremote_endpoint_configured=no',
        'The design assumes a local pathname can reach another machine. A UDS endpoint belongs to its local OS; the moved helper needs a reachable remote interface.',
        ['Record whether the peers share a host/network namespace.', 'Distinguish endpoint locality from an application operation.', 'Identify missing remote-address, authentication, and message-contract requirements.'],
        ['Either keep compatible peers on the same host with a supported local endpoint, or design a reachable authenticated network interface.', 'Check runtime/client support in primary documentation before selecting a cloud connector.'],
        'The worksheet must change its choice to a network application interface when peers are remote. It must not invent a throughput improvement or claim Cloud SQL compatibility was tested.',
        'Reachability would still leave authentication, authorization, and remote operation correctness to validate.'),
]]

COVERS_CLAUSES = [
    'trace a packet from a host to a different subnet using a supplied diagram',
    'Split a /24 into four equal networks',
    'trace a packet from a host to a different subnet using a supplied diagram',
    'trace a packet from a host to a different subnet using a supplied diagram',
]
LAB_FILES = ['day-002-topic-01.md', 'day-002-topic-02.md', 'day-002-topic-03.md', 'day-002-topic-04.md']

for i, (overview, tech, topic, exercise) in enumerate(zip(OVERVIEWS, [T1_TECH, T2_TECH, T3_TECH, T4_TECH], TOPICS, [LAYER_LAB, SUBNET_LAB, PATH_LAB, IPC_LAB])):
    key, title, intro, why, where, preview = overview
    ref_key = ['layers', 'private', 'napi', 'unix'][i]
    label, url = SOURCES[ref_key]
    exercise['covers'] = COVERS_CLAUSES[i]
    exercise['file'] = LAB_FILES[i]
    topic.update({'key': key, 'title': title, 'overview': intro, 'preview': preview,
        'technical': tech, 'reference': url, 'reference_label': f'{label}',
        'questions': [
            ['Which successful lower-layer fact still leaves the application outcome unproved?', 'Which probe tests the actual readiness condition?'],
            ['Which two bits are borrowed to split /24 into four equal blocks?', 'Is the frame destination the gateway or the remote host on A’s first hop?'],
            ['What is the first missing progress signal between socket delivery and process read?', 'Which stages does local loopback bypass?'],
            ['Can the endpoint reach a process on another host?', 'Which compatibility/security fact needs documentation or observation?'],
        ][i], 'scenario': topic['scenario'], 'lab': exercise})

COMPLETION_HTML = """<p>Save <strong>subnet-ranges.csv</strong> and <strong>next-hop-path.csv</strong> together with their check reports and notes in the Day 1 evidence repository. The four /26 network/broadcast pairs and the A → R → B path must be reviewable. Retain source dates and label all tabletop predictions and untested GCP behavior.</p>
<label class="check"><input type="checkbox" data-progress="read-2"> I read and reviewed the day</label>
<label class="check"><input type="checkbox" data-progress="artifact-2"> I saved the exit artifact</label>"""

REVIEW_RECORDS = {
    'source_ledger': {
        'https://datatracker.ietf.org/doc/html/rfc1122#page-8': {
            'heading_opened': '2. LINK LAYER',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        },
        'https://www.rfc-editor.org/rfc/rfc9293.html#section-2': {
            'heading_opened': '2. Introduction',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        },
        'https://www.rfc-editor.org/rfc/rfc1918.html#section-3': {
            'heading_opened': '3. Private Address Space',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        },
        'https://www.rfc-editor.org/rfc/rfc826.html': {
            'heading_opened': 'An Ethernet Address Resolution Protocol',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': 'RFC 826 is published as plain text without HTML section fragments; the entire document defines the Address Resolution Protocol specification.'
        },
        'https://www.rfc-editor.org/rfc/rfc4861.html#section-3.1': {
            'heading_opened': '3.1. Comparison with IPv4',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/vpc/docs/subnets#unusable-ip-addresses-in-every-subnet': {
            'heading_opened': 'Unusable addresses in IPv4 subnet ranges',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/vpc/docs/routes#types_of_routes': {
            'heading_opened': 'Types of routes',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#load-balancer-types': {
            'heading_opened': 'Types of Google Cloud load balancers',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/load-balancing/docs/health-check-concepts#categories_protocols_ports': {
            'heading_opened': 'Categories, protocols, and ports',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.kernel.org/networking/napi.html#driver-api': {
            'heading_opened': 'Driver API',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/compute/docs/networking/using-gvnic#overview': {
            'heading_opened': 'Overview of Google Virtual NIC',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://man7.org/linux/man-pages/man7/unix.7.html#DESCRIPTION': {
            'heading_opened': 'DESCRIPTION',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://grpc.io/docs/what-is-grpc/introduction/#working-with-protocol-buffers': {
            'heading_opened': 'Working with Protocol Buffers',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/apis/design#resources': {
            'heading_opened': 'Resource-oriented Design',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/sql/docs/mysql/connect-auth-proxy#unix-sockets': {
            'heading_opened': 'Unix sockets',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Network.subnets': {
            'heading_opened': 'IPv4Network.subnets',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        }
    },
    'product_claims': [
        {
            'claim': 'Google Cloud VPC reserves the first two and last two addresses in every primary IPv4 subnet range.',
            'section_url': 'https://docs.cloud.google.com/vpc/docs/subnets#unusable-ip-addresses-in-every-subnet',
            'heading_opened': 'Unusable addresses in IPv4 subnet ranges'
        },
        {
            'claim': 'Google Cloud VPC routes determine outgoing packet paths using route priority and longest prefix match.',
            'section_url': 'https://docs.cloud.google.com/vpc/docs/routes#types_of_routes',
            'heading_opened': 'Types of routes'
        },
        {
            'claim': 'Google Cloud Load Balancing offers Layer 7 Application Load Balancers and Layer 4 Network Load Balancers with distinct proxy and passthrough modes.',
            'section_url': 'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#load-balancer-types',
            'heading_opened': 'Types of Google Cloud load balancers'
        },
        {
            'claim': 'Health checks in Google Cloud support distinct protocols (HTTP, HTTPS, HTTP/2, TCP, SSL, GRPC) with criteria evaluated for backend readiness.',
            'section_url': 'https://docs.cloud.google.com/load-balancing/docs/health-check-concepts#categories_protocols_ports',
            'heading_opened': 'Categories, protocols, and ports'
        },
        {
            'claim': 'Google Virtual NIC (gVNIC) is an alternative virtual network interface for Compute Engine that supports higher throughput and multi-queue configurations.',
            'section_url': 'https://docs.cloud.google.com/compute/docs/networking/using-gvnic#overview',
            'heading_opened': 'Overview of Google Virtual NIC'
        },
        {
            'claim': 'Cloud SQL Auth Proxy supports local Unix sockets for Linux/macOS clients communicating on the same host.',
            'section_url': 'https://docs.cloud.google.com/sql/docs/mysql/connect-auth-proxy#unix-sockets',
            'heading_opened': 'Unix sockets'
        }
    ],
    'visual_reasons': {
        'Supplied Ethernet model: host A to host B': 'Retained qualifying multi-step packet traversal sequence modeling two /26 subnets, gateway route selection, hop-by-hop ARP MAC rewrites, and return path symmetry.',
        'Receive sequence: NIC to application socket': 'Retained qualifying receive lifecycle sequence illustrating Linux kernel packet processing from NIC queue and DMA to NAPI polling, IP input, TCP demux, and application socket buffer.'
    }
}

DATA = {
    'contract_version': 2,
    'day': DAY,
    'day_padded': '002',
    'title': 'Day 2 — IP addressing and packet paths',
    'time_estimate': '2–3 hours',
    'prerequisites': '[Day 1](#day-1); bring their exit artifacts.',
    'work_block': 'Days 1–17 — Foundations',
    'roadmap_practice': 'Split a /24 into four equal networks and trace a packet from a host to a different subnet using a supplied diagram.',
    'roadmap_exit': 'Four correct ranges with network/broadcast addresses and a labeled next-hop path.',
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
    'completion_html': COMPLETION_HTML,
    'review_records': REVIEW_RECORDS
}
