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
    workspace as _workspace, write_file, lab as _lab, case as _case)

from scripts.compact_flow import render_compact_flow

DAY = 2
ACCESS_DATE = '2026-10-03'
EXIT_SUMMARY = 'Four correct ranges with network/broadcast addresses and a labeled next-hop path.'
SOURCES = {
    'layers': ('RFC 1122: Internet protocol suite, section 1.1.3 (page 8)', 'https://datatracker.ietf.org/doc/html/rfc1122#page-8'),
    'tcp': ('RFC 9293: TCP introduction', 'https://www.rfc-editor.org/rfc/rfc9293.html#section-2'),
    'private': ('RFC 1918: private address space, section 3', 'https://www.rfc-editor.org/rfc/rfc1918.html#section-3'),
    'arp': ('RFC 826: Address Resolution Protocol', 'https://www.rfc-editor.org/rfc/rfc826.html'),
    'ndp': ('RFC 4861: Neighbor Discovery comparison with IPv4, section 3.1', 'https://www.rfc-editor.org/rfc/rfc4861.html#section-3.1'),
    'subnets': ('Google Cloud: primary IPv4 subnet ranges and unusable addresses', 'https://docs.cloud.google.com/vpc/docs/subnets#unusable-ip-addresses-in-every-subnet'),
    'routes': ('Google Cloud: routes overview', 'https://docs.cloud.google.com/vpc/docs/routes'),
    'lb': ('Google Cloud: load balancer types', 'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#load-balancer-types'),
    'health': ('Google Cloud: health check protocols and criteria', 'https://docs.cloud.google.com/load-balancing/docs/health-check-concepts'),
    'napi': ('Linux kernel: NAPI driver API', 'https://docs.kernel.org/networking/napi.html#driver-api'),
    'gvnic': ('Compute Engine: Google Virtual NIC', 'https://docs.cloud.google.com/compute/docs/networking/using-gvnic'),
    'unix': ('Linux unix(7): local sockets and pathname permissions', 'https://man7.org/linux/man-pages/man7/unix.7.html'),
    'grpc': ('gRPC: introduction to remote procedure calls', 'https://grpc.io/docs/what-is-grpc/introduction/'),
    'api': ('Google Cloud: API design guide', 'https://docs.cloud.google.com/apis/design'),
    'proxy': ('Cloud SQL Auth Proxy: local TCP and Unix socket options', 'https://docs.cloud.google.com/sql/docs/mysql/connect-auth-proxy#unix-sockets'),
    'python': ('Python: IPv4Network subnet calculation', 'https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Network.subnets'),
}


source = partial(_source, sources=SOURCES)
subtopic = partial(_subtopic, sources=SOURCES, access_date=ACCESS_DATE)
stage = partial(_stage, location='Local Linux Bash terminal / text editor.')
workspace = partial(_workspace, preflight_text='Python available; local/tabletop only; GCP untested')
LAB_CONTEXT = {'mode': 'Local/offline tabletop; supplied fixtures, no live GCP deployment',
 'prereq': 'Day 1 workspace/evidence repository; local Linux Bash, Python 3 standard library, text editor',
 'preflight': 'Run all eight stages in order in the same terminal. Stage 1 creates a unique workspace. Stop '
              'if Python is unavailable; use the Linux environment prepared on Day 1. Commands write only '
              'inside the lab workspace.',
 'verification': 'Recorded outputs are local calculation or fixture classifications. They are not cloud '
                 'observations.',
 'cleanup': 'Stage 8 removes named lab input/script files only, preserving evidence. No processes, cloud '
            'resources, firewall rules, or kernel settings are created or changed. Copy the listed evidence '
            'to the Day 1 repository before discarding the workspace.'}
lab = partial(_lab, defaults=LAB_CONTEXT)
case = partial(_case,
    evidence_label='Supplied synthetic records (literal fixture, not observed logs):',
    facts='Synthetic fixture: socket bytes queued=yes; application reads=no.',
    inference='The first missing progress signal is the process-read boundary; worker blockage remains a hypothesis.',
    expected='After the actual blockage is diagnosed and repaired, observe a read and valid response; neither is established here.')

NEXT_HOP_FLOW = {'title': 'Supplied Ethernet model: host A to host B',
 'desc': 'Read 1 → 2 → 3 → 4 → 5 → 6. Supplied conventional Ethernet teaching topology, with no NAT and '
         'connected router interfaces. IP endpoints stay A and B; link-layer addresses change at the '
         'router. This is a tabletop path, not a capture of Google Cloud physical forwarding.',
 'caption': 'Read 1 → 2 → 3 → 4 → 5 → 6. Supplied conventional Ethernet teaching topology, with no NAT '
            'and connected router interfaces. IP endpoints stay A and B; link-layer addresses change at '
            'the router. This is a tabletop path, not a capture of Google Cloud physical forwarding.',
 'nodes': [{'id': 'n1',
            'label': 'Host A selects route',
            'detail': ('10.240.0.10/26 → .75', 'Destination outside A subnet'),
            'icon': '../assets/icons/generic/client.svg'},
           {'id': 'n2',
            'label': 'Resolve next hop',
            'detail': ('Gateway IP: 10.240.0.1', 'ARP learns gateway MAC'),
            'icon': '../assets/icons/generic/router.svg'},
           {'id': 'n3',
            'label': 'Send local frame',
            'detail': ('IP destination stays .75', 'Frame destination: gateway'),
            'icon': '../assets/icons/generic/switch.svg'},
           {'id': 'n4',
            'label': 'Router forwards',
            'detail': ('Connected 10.240.0.64/26', 'Outgoing interface: 10.240.0.65'),
            'icon': '../assets/icons/generic/router.svg'},
           {'id': 'n5',
            'label': 'Resolve host B',
            'detail': ('Router ARPs for 10.240.0.75', 'New frame destination: B MAC'),
            'icon': '../assets/icons/generic/endpoint.svg'},
           {'id': 'n6',
            'label': 'Host B receives',
            'detail': ('IP destination: 10.240.0.75', 'Transport delivers to socket'),
            'icon': '../assets/icons/generic/server.svg'}],
 'steps': [{'from': 'n1', 'to': 'n2', 'label': 'off-link'},
           {'from': 'n2', 'to': 'n3', 'label': 'encapsulate'},
           {'from': 'n3', 'to': 'n4', 'label': 'route lookup'},
           {'from': 'n4', 'to': 'n5', 'label': 'neighbor'},
           {'from': 'n5', 'to': 'n6', 'label': 'deliver'}]}
NEXT_HOP_SVG = render_compact_flow('d002-next-hop', NEXT_HOP_FLOW)

NIC_FLOW = {'title': 'Receive sequence: NIC to application socket',
 'desc': 'Read 1 → 2 → 3 → 4 → 5 → 6. A simplified Linux receive path for established TCP traffic '
         'addressed to this host. Driver offloads and kernel versions can change processing details; '
         'SYN/accept queues belong to connection establishment. Loopback skips physical NIC/DMA, and '
         'this drawing does not reveal Google Cloud fabric internals.',
 'caption': 'Read 1 → 2 → 3 → 4 → 5 → 6. A simplified Linux receive path for established TCP traffic '
            'addressed to this host. Driver offloads and kernel versions can change processing details; '
            'SYN/accept queues belong to connection establishment. Loopback skips physical NIC/DMA, and '
            'this drawing does not reveal Google Cloud fabric internals.',
 'nodes': [{'id': 'n1',
            'label': 'NIC receive queue',
            'detail': ('Frame arrives at interface', 'Driver-managed receive buffers'),
            'icon': '../assets/icons/generic/endpoint.svg'},
           {'id': 'n2',
            'label': 'Driver processing',
            'detail': ('DMA: device transfers to RAM', 'Interrupt / polling notification'),
            'icon': '../assets/icons/generic/queue.svg'},
           {'id': 'n3',
            'label': 'NAPI polling',
            'detail': ('Linux processes receive work', 'Scheduling varies by driver'),
            'icon': '../assets/icons/generic/queue.svg'},
           {'id': 'n4',
            'label': 'IP input checks',
            'detail': ('Headers, policy, local delivery', 'Transit packets use forwarding'),
            'icon': '../assets/icons/generic/firewall.svg'},
           {'id': 'n5',
            'label': 'Transport + socket',
            'detail': ('TCP matches connection tuple', 'Bytes wait in receive buffer'),
            'icon': '../assets/icons/generic/server.svg'},
           {'id': 'n6',
            'label': 'Application reads',
            'detail': ('Process reads socket bytes', 'Parses request; may still fail'),
            'icon': '../assets/icons/generic/user.svg'}],
 'steps': [{'from': 'n1', 'to': 'n2', 'label': 'notify'},
           {'from': 'n2', 'to': 'n3', 'label': 'poll'},
           {'from': 'n3', 'to': 'n4', 'label': 'IP input'},
           {'from': 'n4', 'to': 'n5', 'label': 'demux'},
           {'from': 'n5', 'to': 'n6', 'label': 'read'}]}
NIC_SVG = render_compact_flow('d002-nic-socket', NIC_FLOW)

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
        f'An IPv4 address has 32 bits. In {keyword("/N prefix notation")}, N bits identify the network and 32−N remain for addresses within it. Thus /24 has 256 addresses, /20 has 4,096, and /16 has 65,536. A /24 mask is 255.255.255.0; /20 is 255.255.240.0; /16 is 255.255.0.0. Prefix length is a bit boundary, so a /20 does not end at an octet boundary. For 10.240.0.0/24, splitting into four equal blocks borrows two bits: /24 + 2 = /26, with 64 addresses per block.',
        'Separate total addresses from assignable host addresses. Budget enough space for growth and provider reservations, and verify that a proposed subnet starts on its prefix boundary; 10.240.0.65/26 is a host-with-prefix rather than a canonical network identifier.',
        'A VPC (Virtual Private Cloud) subnet range is expressed in CIDR notation. Use the same arithmetic for its address plan, then apply the documented provider rules before assigning VM addresses.', ['python', 'subnets']),
    '''<div class="callout"><strong>Worked binary boundary: where does .75 belong?</strong><p>For a /26, the last-octet mask is 11000000 (decimal 192). Address .75 is 01001011; bitwise AND with 11000000 gives 01000000 (decimal 64), so the network is .64. The six remaining bits span offsets 0–63, making its broadcast .127. The four borrowed-bit combinations 00, 01, 10, and 11 therefore start at .0, .64, .128, and .192.</p><p>For 10.240.0.0/20, the third octet ranges from 0 through 15 and the full block ends at 10.240.15.255. For 10.240.0.0/16, the final two octets vary and the block ends at 10.240.255.255. These are address calculations, not allocated cloud networks.</p></div>''',
    subtopic(T2_TITLES[1],
        f'{keyword("RFC 1918")} defines three private blocks: 10.0.0.0/8, 172.16.0.0/12 (172.16 through 172.31), and 192.168.0.0/16. Different isolated organizations may reuse them. For example, 172.20.1.1 is in a private block; 172.40.1.1 is not in an RFC 1918 block. A private address does not by itself make an application secure.',
        'Record ownership of each allocated range. If two networks that must communicate reuse the same destination space, ordinary address-based routing cannot distinguish them without additional design. Non-overlapping allocations make future connectivity easier.',
        'Google Cloud permits private IPv4 ranges for subnets. The address plan must account for the other networks that will connect to the VPC; creating a private CIDR is not proof that routes, firewall policy, or authentication are correct.', ['private']),
    subtopic(T2_TITLES[2],
        f'{keyword("ARP")} (Address Resolution Protocol) learns the link-layer address for an IPv4 neighbor on a local Ethernet segment. For an off-subnet destination, that neighbor is usually the selected gateway, not the remote host. {keyword("NDP")} (Neighbor Discovery Protocol) uses IPv6 control messages for neighbor discovery and other functions such as router discovery; it is not an IPv4 ARP broadcast.',
        'Keep final destination and next hop separate. In the supplied model, A=10.240.0.10/26 and B=10.240.0.75/26: A resolves 10.240.0.1, sends to that gateway’s MAC (Media Access Control) address, and retains .75 as the IP destination.',
        'This conventional Ethernet model teaches address selection. A VPC uses software-defined networking; its virtual gateway behavior is documented separately. Do not treat a guest neighbor entry as a discovery of physical cloud topology.', ['arp', 'ndp']),
    subtopic(T2_TITLES[3],
        'The four /26 network addresses are .0, .64, .128, and .192; their broadcast addresses are .63, .127, .191, and .255. Each covers 64 addresses. In conventional IPv4 subnet arithmetic, the network and broadcast addresses are excluded from host assignment for these /26 examples.',
        'A complete allocation artifact records network, broadcast, range size, and ownership. Do not copy one provider’s reservation formula to another provider or equate a mathematically valid range with an approved production allocation.',
        'For a primary IPv4 subnet range, Google Cloud reserves its first two and last two addresses. In 10.240.0.64/26 these are .64, .65, .126, and .127, leaving .66–.125 (60 addresses). This is a primary-range comparison; do not apply it indiscriminately to secondary or IPv6 ranges.', ['subnets']),
    '''<table><caption>Worked /24 split: conventional subnet boundaries and GCP primary-range comparison</caption><thead><tr><th>Network</th><th>Broadcast</th><th>Conventional host span (62)</th><th>GCP primary assignable span (60)</th></tr></thead><tbody>
<tr><td>10.240.0.0/26</td><td>10.240.0.63</td><td>.1–.62</td><td>.2–.61</td></tr>
<tr><td>10.240.0.64/26</td><td>10.240.0.127</td><td>.65–.126</td><td>.66–.125</td></tr>
<tr><td>10.240.0.128/26</td><td>10.240.0.191</td><td>.129–.190</td><td>.130–.189</td></tr>
<tr><td>10.240.0.192/26</td><td>10.240.0.255</td><td>.193–.254</td><td>.194–.253</td></tr>
</tbody></table>''',
    subtopic(T2_TITLES[4],
        f'The {keyword("next hop")} is the immediate neighbor to which a host sends a packet. In the supplied model, A first checks its routes, resolves gateway .1, and sends a frame to it. Router R has interfaces .1/26 and .65/26, so it can forward to B=.75 on the second subnet. The router resolves B’s MAC and sends a new frame. The IP destination remains B when no NAT is involved.',
        'Label both forward and return paths. On A, a default route via .1 handles off-subnet traffic; on B, the default route via .65 enables the reply. For the simplified route table used here, the longest matching prefix chooses the more specific destination route.',
        'Use this as a foundation for reading VPC routes, whose selection also has documented categories and priorities. The VPC virtual gateway is not the physical router drawn in this supplied lab and does not behave like an ordinary pingable router.', ['routes']),
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


LAYER_CHECK = '''import csv
from pathlib import Path
rows = list(csv.DictReader(Path("classification.csv").open()))
expected = {"no_route": "L3", "tcp_refused": "L4", "http_503": "L7"}
assert {r["case"]: r["first_failed_boundary"] for r in rows} == expected, "Recheck the responsibility map"
assert all(r["not_proven"].strip() for r in rows), "Record an evidence limit per row"
Path("layer-check.txt").write_text("PASS: 3 supplied cases classified; each has an evidence limit\\n")
print(Path("layer-check.txt").read_text(), end="")'''
LAYER_LAB = lab('Classify evidence at the L3, L4, and L7 boundaries',
    'Classify supplied records and identify what each successful lower-layer observation does not establish.',
    'Three classified cases plus a readiness design note, labeled synthetic/tabletop.', [
    stage(1, 'Preflight and isolate the worksheet', 'Run the commands in a fresh terminal. Record the printed workspace path; all following relative files belong there.', 'Python version and a unique local workspace.', 'preflight.txt and the workspace path.', workspace('d002-layers')),
    stage(2, 'Prepare supplied diagnostic records', 'Create this literal fixture. The strings are teaching records, not actual terminal output from a network test.', 'Three records: no route, refused connection, and HTTP 503.', 'cases.txt.', write_file('cases.txt', '''SOURCE=synthetic teaching fixture
no_route: destination=10.240.0.75 route_match=none
tcp_refused: route_match=yes connect=refused
http_503: route_match=yes connect=success HTTP=503''')),
    stage(3, 'Author boundary classifications', '1. Open a new local file named classification.csv in your text editor.\n2. Use the header below and add rows for no_route, tcp_refused, and http_503.\n3. Set first_failed_boundary to L3, L4, or L7 after reading the responsibility table; write one concrete unproved fact in not_proven for each.\n4. Save in the printed workspace. These manual worksheet steps implement the concepts in the [RFC 1122 responsibility model](https://datatracker.ietf.org/doc/html/rfc1122#page-8).\n\n```csv\ncase,first_failed_boundary,not_proven\n```', 'Exactly three case rows with a layer classification and evidence limit.', 'classification.csv.'),
    stage(4, 'Check the planned classifications', 'Create and run this offline checker. If an assertion fails, correct the worksheet; do not alter the expected classifications to hide an error.', 'PASS for the three classifications; mismatches stop execution.', 'layer-check.txt.', write_file('check_layers.py', LAYER_CHECK) + 'python3 check_layers.py'),
    stage(5, 'Inspect the classified evidence', 'Print your worksheet and compare it with cases.txt: no route is L3, refusal is L4 given a route, and HTTP 503 is L7 given successful transport. Confirm each row names a distinct unproved fact.', 'Classification includes boundaries and limits rather than just layer names.', 'The reviewed classification.csv.', 'cat cases.txt\ncat classification.csv\ncat layer-check.txt'),
    stage(6, 'Challenge a port-only readiness decision', 'Create the supplied decision challenge. In an editor add an answer line explaining why the port signal cannot certify checkout readiness.', 'The answer states that a reachable port does not establish successful HTTP/business operation.', 'readiness-challenge.txt.', write_file('readiness-challenge.txt', '''SOURCE=synthetic design challenge
TCP probe=success
checkout request=HTTP 503
Question: Does the port probe prove checkout readiness? Explain using the failed boundary.''')),
    stage(7, 'Record the fix and GCP design question', '1. Open readiness-challenge.txt and append a proposed application investigation plus an HTTP readiness condition relevant to this case.\n2. Open the [GCP health-check overview](https://docs.cloud.google.com/load-balancing/docs/health-check-concepts).\n3. Record that a future load-balancer design must verify supported probe protocol and readiness semantics; note GCP=not deployed/tested.\n4. Do not claim changing the probe fixes the underlying HTTP 503.', 'A topic-specific decision distinguishes detection from repair.', 'readiness-challenge.txt with the design note.'),
    stage(8, 'Close out and preserve evidence', 'Remove only the supplied fixture and checker. Copy classification.csv, layer-check.txt, and readiness-challenge.txt into the Day 1 evidence repository’s Day 002 folder using the file manager or editor. Keep their synthetic/local labels.', 'Evidence remains; temporary script and input are removed.', 'Three evidence files and preflight.txt.', 'python3 - <<\'EOF\'\nfrom pathlib import Path\nfor name in ("cases.txt", "check_layers.py"):\n    Path(name).unlink(missing_ok=True)\nprint("Evidence retained:", sorted(p.name for p in Path.cwd().iterdir()))\nEOF'),
], 'classification.csv has all three correct boundaries and evidence limits; layer-check.txt passes; the readiness note distinguishes detection from remediation. This supports the next-hop artifact’s evidence-limit statement.',
    'File not found: run from the Stage 1 workspace. CSV mismatch: use the exact case identifiers and header. A port success plus HTTP 503 belongs to the application boundary; it does not establish the dependency root cause.',
    'classification.csv; layer-check.txt; readiness-challenge.txt')

SUBNET_SCRIPT = '''import csv, ipaddress, json
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
    print(row["network"], row["broadcast"], "total=", row["total"], "GCP primary assignable=", row["gcp_primary_count"])'''
SUBNET_VERIFY = '''import ipaddress, json
from pathlib import Path
rows = json.loads(Path("subnet-ranges.json").read_text())
networks = [ipaddress.ip_network(r["network"]) for r in rows]
assert len(networks) == 4 and sum(n.num_addresses for n in networks) == 256
assert [str(n.network_address) for n in networks] == ["10.240.0.0", "10.240.0.64", "10.240.0.128", "10.240.0.192"]
assert [str(n.broadcast_address) for n in networks] == ["10.240.0.63", "10.240.0.127", "10.240.0.191", "10.240.0.255"]
assert all(not a.overlaps(b) for i,a in enumerate(networks) for b in networks[i+1:])
assert all(r["gcp_primary_count"] == 60 for r in rows)
Path("subnet-check.txt").write_text("PASS: four /26 blocks, 256 total addresses, no overlap, correct boundaries\\n")
print(Path("subnet-check.txt").read_text(), end="")'''
SUBNET_LAB = lab('Split 10.240.0.0/24 into four equal networks',
    'Calculate four ranges and compare conventional host arithmetic with GCP primary IPv4 reservations.',
    'A checked subnet table with correct network/broadcast addresses; no VPC resources created.', [
    stage(1, 'Verify the calculation environment', 'Run the commands. Python’s ipaddress module is included in its standard library; no package installation is needed.', 'A unique workspace; the parent contains 256 addresses.', 'preflight.txt.', workspace('d002-subnets') + 'python3 -c \'import ipaddress; print(ipaddress.ip_network("10.240.0.0/24").num_addresses)\''),
    stage(2, 'Prepare the allocation inputs', 'Create this planning brief. Before continuing, calculate the new prefix: four equal blocks require two additional network bits.', 'Parent /24, four children, /26 prediction.', 'allocation-inputs.txt.', write_file('allocation-inputs.txt', '''parent=10.240.0.0/24
children=4
new_prefix=26
owners=web,app,database,management
mode=offline planning; no deployed subnets''')),
    stage(3, 'Author the calculation', 'Write the complete script below. Read how new_prefix=26 yields four blocks and how the primary-range comparison excludes four reserved addresses.', 'A script with explicit inputs and two output formats.', 'subnet_math.py until closeout.', write_file('subnet_math.py', SUBNET_SCRIPT)),
    stage(4, 'Calculate the four ranges', 'Run the script and view the CSV. Match the network/broadcast pairs to the worked table in Part 2.', 'Networks .0, .64, .128, .192; broadcasts .63, .127, .191, .255; 64 addresses each.', 'subnet-ranges.csv and subnet-ranges.json.', 'python3 subnet_math.py\ncat subnet-ranges.csv'),
    stage(5, 'Verify boundaries and reservations', 'Run the complete checker below. Then open the [GCP unusable primary-range address section](https://docs.cloud.google.com/vpc/docs/subnets#unusable-ip-addresses-in-every-subnet), compare first two/last two reservations with the CSV, and record the access date in allocation-inputs.txt. This is the GCP documentation step; there is no Console deployment.', 'No overlapping children; 256 total addresses; 60 primary-range assignable addresses per /26.', 'subnet-check.txt and the documented comparison.', write_file('verify_subnets.py', SUBNET_VERIFY) + 'python3 verify_subnets.py'),
    stage(6, 'Challenge a nonaligned network input', 'Run a strict parse of 10.240.0.65/26. This is a host address with network bits set in the host portion; record the rejection and distinguish it from the canonical .64/26 network.', 'host bits set rejection; the normalized network is 10.240.0.64/26.', 'alignment-check.txt.', '''python3 - <<'EOF'
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
EOF'''),
    stage(7, 'Record allocation ownership and limits', '1. In the editor create subnet-plan.md.\n2. Assign web=.0/26, app=.64/26, database=.128/26, management=.192/26 using the full 10.240.0 prefix.\n3. Link the saved CSV/JSON and alignment check.\n4. State “primary IPv4 GCP comparison only; local calculation; GCP untested”.\n5. Record that .75 belongs to app and that the next exercise must establish a labeled route to it.', 'A reviewable owner map linked to numerical evidence.', 'subnet-plan.md, a component of the roadmap exit evidence.'),
    stage(8, 'Clean calculation inputs and preserve ranges', 'Remove only the named scripts/input. Copy subnet-plan.md, CSV, JSON, subnet-check.txt, and alignment-check.txt into the Day 1 evidence repository’s Day 002 folder. The next exercise reuses their numerical values, not this terminal’s variables.', 'Five durable evidence files remain in the workspace.', 'All five files plus preflight.txt.', '''python3 - <<'EOF'
from pathlib import Path
for name in ("subnet_math.py", "verify_subnets.py", "allocation-inputs.txt"):
    Path(name).unlink(missing_ok=True)
print("Evidence retained:", sorted(p.name for p in Path.cwd().iterdir()))
EOF'''),
], 'Four /26 rows, explicit network/broadcast addresses, 64 total addresses each, no overlap; primary-range comparison uses four reservations. Save alongside the labeled next-hop path from Exercise 3.',
    'Module missing: confirm this is Python 3. Wrong boundaries: verify parent=.0/24 and new_prefix=26. GCP counts apply only to primary IPv4 ranges; conventional ipaddress.hosts() alone does not model provider reservations.',
    'subnet-plan.md; subnet-ranges.csv; subnet-ranges.json; subnet-check.txt; alignment-check.txt')

PATH_CHECK = '''import csv
from pathlib import Path
rows = list(csv.DictReader(Path("next-hop-path.csv").open()))
expected = [("A", "10.240.0.75", "10.240.0.1", "R-left"),
            ("R", "10.240.0.75", "10.240.0.75", "B"),
            ("B-reply", "10.240.0.10", "10.240.0.65", "R-right")]
actual = [(r["sender"],r["ip_destination"],r["next_hop_ip"],r["frame_destination"]) for r in rows]
assert actual == expected, "Revisit subnet membership and the supplied router interfaces"
Path("path-check.txt").write_text("PASS: A forwards via .1; R delivers to .75; B replies via .65\\nTabletop only; no packet capture or live connectivity evidence\\n")
print(Path("path-check.txt").read_text(), end="")'''
PATH_LAB = lab('Trace the next hop and the destination receive path',
    'Trace A to B using the supplied Ethernet diagram, then locate the first unproved receive boundary.',
    'A labeled next-hop CSV, return-path note, NIC/socket sequence, and evidence-limit statement.', [
    stage(1, 'Preflight the supplied model', 'Create a separate workspace. Bring the Exercise 2 table as a reference; no system routes or interfaces will be modified.', 'A separate path workspace and a clear tabletop mode.', 'preflight.txt.', workspace('d002-path')),
    stage(2, 'Prepare explicit host and router inputs', 'Create the supplied topology record and compare its values to the host-to-host diagram in Part 2. MAC names below are symbolic labels, not captured addresses.', 'Two /26 segments and a router directly attached to both.', 'topology.txt.', write_file('topology.txt', '''SOURCE=synthetic conventional Ethernet model; no NAT
A=10.240.0.10/26 default_via=10.240.0.1 MAC=A
R-left=10.240.0.1/26 MAC=R-left
R-right=10.240.0.65/26 MAC=R-right
B=10.240.0.75/26 default_via=10.240.0.65 MAC=B
R has connected routes to 10.240.0.0/26 and 10.240.0.64/26''')),
    stage(3, 'Author the labeled next-hop path', '1. In the editor create next-hop-path.csv with the header below.\n2. Add three rows with sender A, R, and B-reply.\n3. For A/R use destination 10.240.0.75; for B-reply use 10.240.0.10.\n4. Fill next_hop_ip and frame_destination using the six-step supplied diagram.\n5. Record why A resolves the gateway rather than B in a new path-notes.md file. This applies the [ARP specification](https://www.rfc-editor.org/rfc/rfc826.html) to the supplied model.\n\n```csv\nsender,ip_destination,next_hop_ip,frame_destination\n```', 'A route labeled with both final IP destination and local frame destination.', 'next-hop-path.csv and path-notes.md.'),
    stage(4, 'Check the trace', 'Create/run the offline checker. A wrong next hop stops the check. Correct the worksheet using subnet membership; do not alter the checker’s model.', 'PASS: A uses .1, R resolves .75, B replies via .65.', 'path-check.txt.', write_file('check_path.py', PATH_CHECK) + 'python3 check_path.py'),
    stage(5, 'Inspect destination NIC-to-socket boundaries', '1. Open the NIC-to-socket diagram in Part 2.\n2. Append its six numbered steps to path-notes.md in order.\n3. Mark NIC/driver, NAPI, IP input, transport/socket, and process-read ownership.\n4. Add “Loopback does not traverse physical NIC/DMA” and “queued bytes do not prove the application read them”.\n5. Compare the guest processing explanation with the [Linux NAPI documentation](https://docs.kernel.org/networking/napi.html#driver-api).', 'Six receive steps plus two explicit limits; no physical capture is claimed.', 'path-notes.md.'),
    stage(6, 'Challenge the incorrect /24 mask', 'Run the calculation comparing A’s correct /26 with an erroneous /24. Record why the latter makes the off-subnet destination appear local. This modifies only a Python input.', '/26 says B is off-link; /24 incorrectly says it is on-link for this supplied segmented topology.', 'mask-challenge.txt.', '''python3 - <<'EOF'
import ipaddress
from pathlib import Path
destination = ipaddress.ip_address("10.240.0.75")
text = "".join(f"A prefix {prefix}: destination on-link={destination in ipaddress.ip_network(prefix)}\\n" for prefix in ("10.240.0.0/26", "10.240.0.0/24"))
Path("mask-challenge.txt").write_text(text)
print(text, end="")
EOF'''),
    stage(7, 'Diagnose the mask and document the GCP boundary', '1. Append a remediation note to path-notes.md: in the supplied model use A=.10/26 and gateway=.1; verify B’s return gateway=.65.\n2. Open [GCP routes](https://docs.cloud.google.com/vpc/docs/routes) and the [subnet gateway note](https://docs.cloud.google.com/vpc/docs/subnets#unusable-ip-addresses-in-every-subnet).\n3. Record that the drawing is conventional Ethernet and the GCP virtual gateway is not an ordinary pingable physical router.\n4. Add the supplied receive challenge “socket bytes queued=yes, process read=no”; record stalled process as a hypothesis, not a proved root cause. State GCP=untested.', 'A next-hop repair, return-path check, and honest cloud/receive limits.', 'Completed path-notes.md and mask-challenge.txt.'),
    stage(8, 'Close the trace and assemble exit evidence', 'Remove only the checker and supplied topology file. Copy next-hop-path.csv, path-check.txt, path-notes.md, and mask-challenge.txt into the same Day 002 evidence folder as Exercise 2. Confirm that the range table and labeled path are present together before marking the day complete.', 'The roadmap exit evidence combines four correct ranges with a labeled next-hop path.', 'Four path evidence files alongside Exercise 2’s subnet evidence.', '''python3 - <<'EOF'
from pathlib import Path
for name in ("check_path.py", "topology.txt"):
    Path(name).unlink(missing_ok=True)
print("Evidence retained:", sorted(p.name for p in Path.cwd().iterdir()))
EOF'''),
], 'A→R uses gateway .1 and R-left frame destination; R→B uses .75/B; reply uses .65/R-right. Six receive steps are correctly ordered. The saved evidence labels supplied model, local calculation, GCP untested, and no physical capture.',
    'Wrong next hop: compare destination .75 with A’s .0–.63 block. Missing return path: use B’s .65 gateway in this model. A successful fixture check is not a real ping result or a verification of Google Cloud’s network fabric.',
    'next-hop-path.csv; path-check.txt; path-notes.md; mask-challenge.txt')

IPC_CHECK = '''import csv
from pathlib import Path
rows = list(csv.DictReader(Path("ipc-decisions.csv").open()))
expected = {"same_host_path": "UDS", "same_namespace_port": "loopback_TCP", "different_host": "network_RPC"}
assert {r["case"]:r["mechanism"] for r in rows} == expected, "Check locality before choosing an endpoint"
assert all(r["limit"].strip() for r in rows)
Path("ipc-check.txt").write_text("PASS: three communication boundaries classified; performance unmeasured\\n")
print(Path("ipc-check.txt").read_text(), end="")'''
IPC_LAB = lab('Choose a process-communication boundary',
    'Classify local path, loopback port, and remote application communication without promising performance.',
    'Three mechanism decisions plus a locality change note; no service or database deployed.', [
    stage(1, 'Prepare the companion worksheet', 'Run the commands in a fresh terminal. This short coverage checkpoint does not extend the day into RPC deployment or benchmarking.', 'A unique offline worksheet workspace.', 'preflight.txt.', workspace('d002-ipc')),
    stage(2, 'Prepare the three locality cases', 'Create the exact inputs. Each names the endpoint requirement rather than prescribing a universal best mechanism.', 'Three explicit locality conditions.', 'ipc-inputs.txt.', write_file('ipc-inputs.txt', '''SOURCE=synthetic design inputs
same_host_path: Linux peers on same host; client/server support a pathname socket
same_namespace_port: peers share one network namespace; client requires an IP/port API
different_host: peers are on different VMs; client invokes a remote operation''')),
    stage(3, 'Author mechanism choices and limits', '1. In the editor create ipc-decisions.csv using the header below.\n2. Add each exact case identifier from ipc-inputs.txt.\n3. Choose UDS, loopback_TCP, or network_RPC using the Part 2 comparison table.\n4. Record one case-specific limit: permissions/path visibility, local namespace scope, or remote authentication/message contract.\n5. Consult [Linux unix(7)](https://man7.org/linux/man-pages/man7/unix.7.html) for the local socket boundary.\n\n```csv\ncase,mechanism,limit\n```', 'Three rows, each with a concrete compatibility/reachability limit.', 'ipc-decisions.csv.'),
    stage(4, 'Check the design classifications', 'Create/run the complete offline checker. It verifies this fixture’s classifications, not latency or cloud compatibility.', 'Three choices pass; missing limits or wrong locality choices fail.', 'ipc-check.txt.', write_file('check_ipc.py', IPC_CHECK) + 'python3 check_ipc.py'),
    stage(5, 'Inspect local versus remote ownership', 'Print the worksheet. In an editor create ipc-note.md and explain why a local proxy endpoint and a remote database endpoint are different boundaries. Do not state that a Unix socket makes a remote database local.', 'The note names both process and network boundaries.', 'ipc-note.md and the reviewed CSV.', 'cat ipc-inputs.txt\ncat ipc-decisions.csv\ncat ipc-check.txt'),
    stage(6, 'Challenge a move to another machine', 'Append the supplied change to your note, then answer it: helper B moves from A’s host to another VM; A still uses /tmp/helper.sock. Identify why that local path cannot reach B, and name the new remote endpoint/authentication questions.', 'UDS locality is identified as the failed design assumption; no speed claim is made.', 'ipc-note.md with the changed-locality answer.', '''printf '\nLocality challenge: helper B moved to another VM; A still uses /tmp/helper.sock.\n' >> ipc-note.md'''),
    stage(7, 'Record the GCP design review', '1. Open the [Cloud SQL Auth Proxy Unix socket section](https://docs.cloud.google.com/sql/docs/mysql/connect-auth-proxy#unix-sockets).\n2. In ipc-note.md record that local TCP/Unix socket choices depend on supported platforms and clients.\n3. State that deployment would additionally require the product’s connection/authentication prerequisites, which this day does not perform.\n4. Add “GCP=untested; latency and throughput=unmeasured”.', 'A compatibility question and explicit evidence limits instead of an invented benchmark.', 'Completed ipc-note.md.'),
    stage(8, 'Close out the design checkpoint', 'Remove the input and checker only. Copy ipc-decisions.csv, ipc-check.txt, and ipc-note.md into the Day 1 repository’s Day 002 evidence folder. No socket files, background servers, or paid resources need cleanup.', 'Three companion evidence files remain.', 'Three IPC evidence files plus preflight.txt.', '''python3 - <<'EOF'
from pathlib import Path
for name in ("check_ipc.py", "ipc-inputs.txt"):
    Path(name).unlink(missing_ok=True)
print("Evidence retained:", sorted(p.name for p in Path.cwd().iterdir()))
EOF'''),
], 'Correct UDS/loopback_TCP/network_RPC fixture choices, one limit per row, a locality-change diagnosis, and explicit unmeasured/untested labels. This companion checkpoint is additional to the roadmap’s subnet/path exit evidence.',
    'CSV parse failure: use the exact header and quote fields containing commas. Wrong choice: a local pathname cannot directly address a listener on another VM. Do not resolve a compatibility question by asserting an unrun performance benchmark.',
    'ipc-decisions.csv; ipc-check.txt; ipc-note.md')


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

for i, (overview, tech, topic, exercise) in enumerate(zip(OVERVIEWS, [T1_TECH, T2_TECH, T3_TECH, T4_TECH], TOPICS, [LAYER_LAB, SUBNET_LAB, PATH_LAB, IPC_LAB])):
    key, title, intro, why, where, preview = overview
    ref_key = ['layers', 'private', 'napi', 'unix'][i]
    label, url = SOURCES[ref_key]
    topic.update({'key': key, 'title': title, 'overview': intro, 'preview': preview,
        'technical': tech, 'reference': url, 'reference_label': f'{label} (accessed {ACCESS_DATE})',
        'questions': [
            ['Which successful lower-layer fact still leaves the application outcome unproved?', 'Which probe tests the actual readiness condition?'],
            ['Which two bits are borrowed to split /24 into four equal blocks?', 'Is the frame destination the gateway or the remote host on A’s first hop?'],
            ['What is the first missing progress signal between socket delivery and process read?', 'Which stages does local loopback bypass?'],
            ['Can the endpoint reach a process on another host?', 'Which compatibility/security fact needs documentation or observation?'],
        ][i], 'scenario': topic['scenario'], 'lab': exercise})

COMPLETION_HTML = '''<p>Save <strong>subnet-ranges.csv</strong> and <strong>next-hop-path.csv</strong> together with their check reports and notes in the Day 1 evidence repository. The four /26 network/broadcast pairs and the A → R → B path must be reviewable. Retain source dates and label all tabletop predictions and untested GCP behavior.</p>
<label class="check"><input type="checkbox" data-progress="read-2"> I read and reviewed the day</label>
<label class="check"><input type="checkbox" data-progress="artifact-2"> I saved the exit artifact</label>'''
DATA = {'day': DAY, 'lab_defaults': {}, 'work_block': 'Days 1–17 — Foundations', 'part1_html': PART1_HTML,
        'part1_intro': PART1_INTRO, 'part2_intro': PART2_INTRO, 'part3_intro': PART3_INTRO,
        'part4_intro': PART4_INTRO, 'exit_summary': EXIT_SUMMARY,
        'arch_diagram': ARCH_DIAGRAM, 'arch_svg_html': ARCH_SVG_HTML,
        'arch_table_html': ARCH_TABLE_HTML, 'topics': TOPICS, 'completion_html': COMPLETION_HTML}
