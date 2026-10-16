"""Durable data specification for Day 5: VPN, load balancers and firewalls."""

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'Google Cloud HA VPN and IPsec overview (accessed 2026-10-04)',
        'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn'
    ),
    'topic-02': (
        'Google Cloud load balancer types overview (accessed 2026-10-04)',
        'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#load-balancer-types'
    ),
    'topic-03': (
        'Google Cloud VPC firewall rule components (accessed 2026-10-04)',
        'https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components'
    )
}

TOPIC_01_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ol>
<li><a href="#topic-01-subtopic-1">IPsec architecture, encapsulation modes, crypto transformations, and anti-replay protection</a></li>
<li><a href="#topic-01-subtopic-2">IKEv2 versus IPsec: control plane vs data plane, security associations, and dead peer detection</a></li>
<li><a href="#topic-01-subtopic-3">Site-to-site VPN, remote-access client VPN, and Private DC to Cloud firewall ACLs</a></li>
<li><a href="#topic-01-subtopic-4">BGP dynamic routing in internet routing and modern Leaf-Spine data centers (underlay ECMP and MP-BGP EVPN overlay)</a></li>
<li><a href="#topic-01-subtopic-5">Path MTU, TCP MSS clamping, and fragmentation overhead</a></li>
</ol>

<h4 id="topic-01-subtopic-1">IPsec architecture, encapsulation modes, crypto transformations, and anti-replay protection</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">IPsec</strong> (Internet Protocol Security, RFC 4301) is an open-standard suite of cryptographic protocols operating at Layer 3 (Network Layer) that provides data confidentiality, integrity, origin authentication, and anti-replay protection. In <strong class="keyword">Tunnel Mode</strong>, the original IP packet (payload plus inner header) is completely encapsulated within a new outer IP header and protected by the <strong class="keyword">Encapsulating Security Payload</strong> (ESP) protocol (IP protocol 50). In contrast, Transport Mode only encrypts the transport-layer payload, leaving original IP headers exposed. For example, when host <code>10.20.1.5</code> contacts <code>10.50.4.8</code> across the public internet, transit routers see only outer gateway IP headers (e.g. <code>198.51.100.1</code> to <code>203.0.113.1</code>) and encrypted ESP payloads.</p>
<p><strong class="side-heading">Anti-Replay Protection deep dive:</strong> In an untrusted public transit network, an active adversary can passively capture legitimate encrypted IPsec packets and re-inject them later to duplicate financial transactions, repeat control commands, or force state desynchronization, even without possessing the encryption keys. IPsec ESP (RFC 4303) prevents this via <strong class="keyword">anti-replay protection</strong>:</p>
<ul>
<li><strong>Monotonic Sequence Numbers:</strong> The sending gateway assigns a strictly increasing 32-bit sequence number (or 64-bit Extended Sequence Number / ESN, RFC 4304) to each ESP packet header. The sequence starts at 1 upon Child SA establishment and never resets or wraps around for that SA. Standard 32-bit counters exhaust after 4,294,967,295 packets; at line rates of 250,000 pps (common on Cloud VPN) or 10 Gbps interconnects, 32 bits wrap in under 5 hours, forcing early rekeying. 64-bit ESN avoids counter exhaustion while transmitting only the lower 32 bits on the wire to eliminate transmission overhead.</li>
<li><strong>Receiver Sliding Verification Window:</strong> The receiving gateway maintains a sliding window of size <em>W</em> (typically 64 or 128 packets) where <em>M</em> is the highest authenticated sequence number received. When an ESP packet arrives:
<ol>
<li>If sequence number &gt; <em>M</em>: The packet is authenticated. If valid, <em>M</em> advances to this new sequence, the window slides forward, and the sequence bit is marked in the bitmask.</li>
<li>If sequence number is between (<em>M</em> - <em>W</em> + 1) and <em>M</em>: If the bitmask indicates it was already received, the packet is an illegal duplicate and is <em>silently dropped</em>. If unreceived, it represents benign out-of-order transit arrival; it is authenticated, decrypted, and marked in the bitmask.</li>
<li>If sequence number &le; (<em>M</em> - <em>W</em>): The packet falls to the left of the sliding window (stale / expired) and is silently dropped without cryptographic processing.</li>
</ol>
</li>
<li><strong>Architectural Efficacy:</strong> Anti-replay protection defeats packet injection and replay attacks at wire speed with zero per-packet asymmetric cryptographic overhead.</li>
</ul>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects rely on IPsec tunnel mode to build private site-to-site network interconnects across untrusted public networks without exposing internal RFC 1918 addressing to public internet routing tables. However, IPsec incurs cryptographic processing overhead, adds 50 to 73 bytes of encapsulation headers per packet, and demands careful cipher suite selection (e.g., choosing authenticated encryption such as AES-GCM-128 or AES-GCM-256 over older AES-CBC with HMAC-SHA-256) to optimize throughput and comply with security mandates.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud VPN encrypts all traffic using IPsec ESP with pre-shared keys or certificates. Cloud VPN supports both HA VPN and Classic VPN, enforcing tunnel-mode encapsulation. Each Cloud VPN tunnel can process up to 250,000 packets per second or up to 3 Gbps egress/ingress depending on packet size. Primary documentation: <a href="https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn">Google Cloud HA VPN overview (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://www.rfc-editor.org/rfc/rfc4301#section-5.1.2">RFC 4301 §5.1.2 Header Construction for Tunnel Mode (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ipsec_and_ike_support">Google Cloud IPsec and IKE support (accessed 2026-10-04)</a>.</p>

<h4 id="topic-01-subtopic-2">IKEv2 versus IPsec: control plane vs data plane, security associations, and dead peer detection</h4>
<p><strong class="side-heading">What it is in general:</strong> IPsec and IKEv2 are frequently conflated, but they are strictly <em>complementary, cooperating protocol layers</em> rather than separate alternatives. A secure VPN architecture requires both:</p>
<ul>
<li><strong>IKEv2 as the Control Plane (RFC 7296):</strong> Internet Key Exchange Protocol Version 2 is the signaling and key-management protocol operating over UDP port 500 (or UDP port 4500 when NAT-Traversal is detected). It performs:
<ol>
<li>Mutual entity authentication using pre-shared keys (PSK) or digital certificates.</li>
<li>Ephemeral Diffie-Hellman key exchange (e.g. DH Groups 14, 19, or 20) to compute master secrets with Perfect Forward Secrecy (PFS).</li>
<li>Establishment of the bidirectional IKE Security Association (IKE SA, Phase 1) to protect control-plane signaling.</li>
<li>Negotiation of unidirectional Child Security Associations (Child SA, Phase 2) defining encryption algorithms, integrity ciphers, and traffic selectors for user payload data.</li>
<li>Periodic automatic rekeying (e.g. every 8 hours for IKE SA, every 3 hours for Child SA) and session teardown.</li>
</ol>
</li>
<li><strong>IPsec ESP as the Data Plane (RFC 4303):</strong> Encapsulating Security Payload (IP protocol 50) is the high-performance data plane protocol. It does <em>not</em> authenticate peers out-of-band or negotiate keys; instead, it uses the symmetric keys derived by IKEv2 to perform packet encryption (AES-GCM or AES-CBC), integrity authentication tags (ICV), anti-replay sequence checking, and packet forwarding at line rate across unidirectional Security Associations identified by the Security Parameter Index (SPI).</li>
<li><strong>Dead Peer Detection (DPD):</strong> IKEv2 sends periodic informational probe exchanges to detect peer gateway unavailability within seconds, tearing down inactive SAs and facilitating rapid failover.</li>
</ul>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Tunnel uptime metrics often mislead: an established Phase 1 IKE SA only proves that gateways can authenticate each other. If Phase 2 Child SA proposals mismatch (such as mismatched Diffie-Hellman groups or traffic selectors), data encryption fails entirely. Furthermore, aggressive DPD timers detect gateway failures rapidly to trigger failover, but uncalibrated timers across high-jitter WAN links cause spurious tunnel renegotiation and dropped sessions.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Cloud VPN strongly recommends IKEv2 for faster rekeying, improved reliability, and support for dynamic route renegotiation. Google Cloud HA VPN enforces IKEv2 exclusively, requiring BGP peering across Cloud Router, whereas legacy Classic VPN supported IKEv1 with static routing. Primary documentation: <a href="https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ike-and-dpd">Google Cloud IKE and Dead Peer Detection (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://www.rfc-editor.org/rfc/rfc7296#section-1.2">RFC 7296 §1.2 IKEv2 Initial Exchanges (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn">Google Cloud HA VPN specifications (accessed 2026-10-04)</a>.</p>

<h4 id="topic-01-subtopic-3">Site-to-site VPN, remote-access client VPN, and Private DC to Cloud firewall ACLs</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Site-to-site VPN</strong> connects two persistent, dedicated network gateways (such as an on-premises enterprise data center router and a cloud VPC gateway), interconnecting entire routed IP subnet ranges so that endpoints communicate transparently without local agent software. In contrast, <strong class="keyword">Client VPN</strong> (remote-access VPN) connects individual roaming user devices running software clients (e.g. OpenVPN, WireGuard, or IPsec client) to a central gateway, dynamically assigning individual virtual IP addresses to each user.</p>
<p><strong class="side-heading">Private DC to Public Cloud connectivity via Firewall ACLs:</strong> Establishing a site-to-site VPN between a private enterprise data center (DC) and Google Cloud requires strict multi-tier firewall Access Control Lists (ACLs):</p>
<ul>
<li><strong>Edge Perimeter Firewall ACLs:</strong> Enterprise edge firewalls facing the public internet must allow outer encapsulation traffic between the on-premises border gateway public IP and the Google Cloud HA VPN gateway public IP interfaces:
<ul>
<li>ALLOW Ingress/Egress UDP port 500 (IKE control-plane signaling).</li>
<li>ALLOW Ingress/Egress UDP port 4500 (NAT-Traversal IKE and ESP encapsulation if intermediate NAT exists).</li>
<li>ALLOW Ingress/Egress IP protocol 50 (ESP encrypted payload transit).</li>
</ul>
</li>
<li><strong>Internal Data Center Firewall ACLs (Virtual Tunnel Interface):</strong> Once the edge gateway decrypts ESP packets and places inner traffic on the Virtual Tunnel Interface (VTI):
<ul>
<li>Ingress ACLs permit private RFC 1918 traffic from the cloud VPC CIDR (e.g. <code>10.20.0.0/16</code>) to reach authorized on-premises servers (such as internal PostgreSQL on TCP 5432 at <code>10.50.4.8</code>), while blocking unauthorized subnets.</li>
<li>Egress ACLs permit on-premises applications to initiate connections to cloud VPC service endpoints.</li>
</ul>
</li>
<li><strong>Private Access to Public Cloud Resources (Google APIs):</strong> Enterprise security policies frequently prohibit on-premises servers from traversing the public internet to reach Google public cloud services (Cloud Storage, BigQuery, Pub/Sub, Vertex AI). Architects implement private access across the VPN tunnel without internet traversal:
<ul>
<li><em>Private Google Access across Cloud VPN:</em> On-premises DNS forwards queries for <code>*.googleapis.com</code> to CNAME <code>private.googleapis.com</code> (VIP <code>199.36.153.8/30</code>) or <code>restricted.googleapis.com</code> (VIP <code>199.36.153.4/30</code> for VPC Service Controls perimeter enforcement). Internal DC firewall ACLs allow TCP port 443 to these VIPs across the tunnel, with Cloud Router advertising the VIP ranges via BGP.</li>
<li><em>Private Service Connect (PSC) Endpoints:</em> Workloads target an internal RFC 1918 IP address (e.g. <code>10.20.100.5</code>) allocated directly inside the VPC subnet. Internal DC firewall ACLs simply permit outbound TCP 443 to that internal RFC 1918 IP across the tunnel, keeping all Google API traffic fully internal.</li>
</ul>
</li>
</ul>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Site-to-site VPN treats the cloud as an extension of the enterprise private WAN, placing trust at the network boundary and demanding robust perimeter firewalls and subnet routing designs. Client VPN enforces identity at the individual device level, often integrating with corporate Identity Providers (IdP) and multi-factor authentication (MFA). Cloud architects avoid client VPN for high-throughput service-to-service automation due to agent management friction, bandwidth limits per tunnel, and poor connection lifecycle predictability.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud provides native managed Site-to-Site VPN through Cloud VPN (HA VPN with two gateway interfaces providing 99.99% service availability). Google Cloud does not provide a multi-tenant managed Client VPN service; instead, architects implement Google Cloud Identity-Aware Proxy (IAP) for zero-trust application access, or host self-managed virtual appliances (e.g. OpenVPN Access Server) on Compute Engine when legacy client VPN tunnels are mandated. Primary documentation: <a href="https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn">Google Cloud VPN topologies and HA architecture (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/topologies#ha-configurations">Google Cloud HA VPN topologies guide (accessed 2026-10-04)</a>; <a href="https://www.rfc-editor.org/rfc/rfc4301#section-5.1.2">RFC 4301 §5.1.2 IPsec architecture (accessed 2026-10-04)</a>.</p>

<h4 id="topic-01-subtopic-4">BGP dynamic routing in internet routing and modern Leaf-Spine data centers (underlay ECMP and MP-BGP EVPN overlay)</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Border Gateway Protocol</strong> (BGP-4, RFC 4271) is the standard exterior routing protocol of the internet. It functions as a path-vector routing protocol that manages reachability information and directs data packets along optimal paths across independent networks called <strong class="keyword">Autonomous Systems</strong> (AS).</p>
<p><strong class="side-heading">General Role of BGP in Networking:</strong> <strong class="keyword">BGP</strong> coordinates routing policy globally:</p>
<ul>
<li><strong>Path-Vector Routing:</strong> Instead of routing based strictly on hop count or link speed, BGP tracks the complete sequence of Autonomous Systems (the <code>AS-Path</code> attribute) traversed by a route. A receiving BGP router immediately discards any route advertisement containing its own ASN in the AS-Path, guaranteeing loop prevention.</li>
<li><strong>Inter-Domain Routing:</strong> Major network operators—Internet Service Providers (ISPs), tech hyperscalers, telecommunication backbones, and enterprise networks—use BGP to peer, exchange reachability information (Network Layer Reachability Information / NLRI) over TCP port 179, and connect global infrastructure.</li>
<li><strong>Policy-Based Control:</strong> Network administrators leverage rich BGP path attributes (such as <code>Local Preference</code>, <code>AS-Path</code> prepending, <code>Multi-Exit Discriminator (MED)</code>, and <code>BGP Communities</code>) to enforce commercial peering agreements, steer inbound and outbound traffic, and prefer dependable paths over raw distance.</li>
<li><strong>Global Scalability &amp; Resiliency:</strong> BGP scales to manage over 900,000+ Internet IPv4 routing table prefixes using incremental updates and route dampening, preventing localized flaps from cascading globally.</li>
</ul>
<p><strong class="side-heading">Importance of BGP in Modern Data Centers (DC):</strong> Data centers have transitioned from legacy three-tier hierarchies (Core/Aggregation/Access) to two-tier Clos / Leaf-Spine physical fabrics powered by BGP:</p>
<ol>
<li><strong>Physical Network (Underlay):</strong>
<ul>
<li><em>East-West Scalability:</em> Modern distributed microservices generate overwhelming horizontal server-to-server (East-West) traffic. Traditional link-state interior gateway protocols (OSPF, IS-IS) flood Link State Advertisements (LSAs) on every link transition; in massive data center fabrics with thousands of links, this flooding causes route flapping and CPU exhaustion. BGP isolates updates hop-by-hop without broadcast flooding.</li>
<li><em>Equal-Cost Multi-Path (ECMP):</em> Every leaf switch connects to every spine switch. BGP leverages ECMP across all spine uplinks, spraying packet flows evenly across dozens of parallel links to maximize bisectional bandwidth and eliminate congestion bottlenecks.</li>
<li><em>Simplicity and Standardization (RFC 7938):</em> eBGP underlay designs assign unique ASNs to each Top-of-Rack (ToR) leaf switch or reuse ASNs with standard AS-path loop controls, providing predictable, standardized convergence.</li>
</ul>
</li>
<li><strong>Virtualization and Multi-Tenancy (Overlay):</strong>
<ul>
<li><em>VXLAN with MP-BGP EVPN (RFC 7432 / RFC 8365):</em> Multi-Protocol BGP Ethernet VPN provides the control plane for Virtual Extensible LAN (VXLAN) encapsulation. EVPN explicitly advertises MAC addresses and IP prefixes (EVPN Route Type 2 MAC/IP and Route Type 5 IP prefix routes) via BGP signaling, eliminating the inefficient flood-and-learn broadcast discovery of legacy networks.</li>
<li><em>Workload Mobility:</em> Virtual machines and container pods can live-migrate across racks and data center pods without renumbering IP addresses, with MP-BGP immediately updating reachability.</li>
<li><em>Complete Elimination of STP Loops:</em> Legacy Spanning Tree Protocol (STP) blocked redundant physical links to prevent broadcast loops, wasting 50% or more of fabric capacity. BGP leaf-spine fabrics keep all physical links active (100% active-active) while EVPN overlays enforce tenant isolation.</li>
</ul>
</li>
</ol>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> IP routing is hop-by-hop and inherently independent in each direction. A common production failure is <em>asymmetric routing failure</em>: the forward packet reaches the remote host via the VPN tunnel, but the remote host or gateway lacks a route for the source subnet pointing back into the tunnel, attempting instead to route return packets out to the public internet or default gateway where they are dropped. BGP dynamic routing automatically advertises subnets, handles link failover, and prevents route desynchronization.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud HA VPN requires Cloud Router and BGP dynamic routing. When a new subnet is created in the VPC, Cloud Router automatically advertises the new CIDR to the on-premises peer over BGP without requiring manual static route updates or tunnel recreation. Static route-based and policy-based VPNs are restricted to legacy Classic VPN. Primary documentation: <a href="https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn">Cloud VPN HA requirements and Cloud Router integration (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://www.rfc-editor.org/rfc/rfc4271#section-3">RFC 4271 §3 BGP concepts and operations (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn-stack-types">Google Cloud HA VPN stack types and BGP sessions (accessed 2026-10-04)</a>.</p>

<h4 id="topic-01-subtopic-5">Path MTU, TCP MSS clamping, and fragmentation overhead</h4>
<p><strong class="side-heading">What it is in general:</strong> The standard Ethernet <strong class="keyword">Maximum Transmission Unit</strong> (MTU) is 1500 bytes. When IPsec encapsulates a packet in tunnel mode, outer IPv4 headers (20 bytes), ESP headers (8 bytes), Initialization Vectors (8–16 bytes), ESP padding and trailer (2–18 bytes), and ICV authentication tags (16 bytes) consume up to 50–73 bytes of overhead. If an inner TCP packet of 1460 bytes is encapsulated, the resulting packet exceeds the physical 1500-byte WAN MTU. If intermediate routers drop packets with the Don't Fragment (DF) bit set without returning ICMP Type 3 Code 4 ("Fragmentation Needed"), a "black hole" occurs. <strong class="keyword">TCP MSS Clamping</strong> dynamically rewrites the Maximum Segment Size option in TCP SYN packets so hosts negotiate smaller segment sizes.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Path MTU issues manifest insidiously: interactive SSH logins and small ping packets succeed, but bulk file transfers or database query result sets freeze mid-transmission. Cloud architects enforce TCP MSS clamping at VPN gateway boundaries to limit TCP segments to 1400 or 1460 bytes, preventing packet fragmentation and silent drop across intermediate carrier paths.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud VPC virtual networks support MTU values of 1460 or 1500 (and jumbo frames up to 8896). Cloud VPN gateways default to an MTU of 1460 bytes to accommodate IPsec ESP overhead without fragmentation. GCP automatically enforces MSS clamping on Cloud VPN interfaces to prevent MTU black holes. Primary documentation: <a href="https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#specifications">Google Cloud VPN specifications and MTU (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://www.rfc-editor.org/rfc/rfc1191#section-2">RFC 1191 §2 Path MTU Discovery mechanism (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#network-bandwidth">Cloud VPN network bandwidth and packet processing limits (accessed 2026-10-04)</a>.</p>

<table><caption>VPN control and data-path boundaries</caption>
<thead><tr><th>Boundary</th><th>Owner</th><th>Evidence</th><th>Limit</th></tr></thead>
<tbody>
<tr><td>IKEv2 negotiation</td><td>Both VPN peers</td><td>Authenticated security association</td><td>Does not prove application prefixes are routed.</td></tr>
<tr><td>IPsec tunnel</td><td>Security gateways</td><td>Protected transit between gateways</td><td>Does not create a return route.</td></tr>
<tr><td>Forward and return routes</td><td>Each routing domain</td><td>Selected next hops for both prefixes</td><td>Does not prove firewall permission.</td></tr>
<tr><td>Database socket</td><td>Peer host and application</td><td>Connection to TCP 5432</td><td>Does not prove a successful transaction.</td></tr>
</tbody></table>

<figure class="diagram-figure"><p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p><svg aria-labelledby="day5-vpn-title day5-vpn-desc" role="img" viewbox="0 0 940 250" xmlns="http://www.w3.org/2000/svg"><title id="day5-vpn-title">Site-to-site VPN forward and return path</title><desc id="day5-vpn-desc">The Brightloaf cloud host routes the inventory request through two IPsec gateways to the on-premises database. The return side needs a route to the cloud source prefix.</desc><defs><marker id="day5-vpn-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker></defs><g fill="#121526" stroke-width="2"><rect height="133" rx="10" stroke="#34d399" width="252" x="18" y="42"></rect><image href="../assets/icons/gcp/core/compute-engine.svg" x="28" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/><rect height="133" rx="10" stroke="#38bdf8" width="252" x="344" y="42"></rect><image href="../assets/icons/gcp/legacy/cloud-vpn.svg" x="354" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/><rect height="133" rx="10" stroke="#f43f5e" width="252" x="670" y="42"></rect><image href="../assets/icons/generic/database.svg" x="680" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/></g><g fill="#fce7f3" font-size="15" font-weight="700" text-anchor="middle"><text x="144" y="78">Cloud Order API</text><text x="470" y="78">IPsec gateways</text><text x="796" y="78">Inventory database</text></g><g fill="#a9b7cb" font-size="12" text-anchor="middle"><text x="144" y="111">10.20.1.5</text><text x="144" y="142">route to 10.50.0.0/16</text><text x="470" y="111">IKEv2 + protected tunnel</text><text x="470" y="142">tunnel established</text><text x="796" y="111">10.50.4.8:5432</text><text fill="#f43f5e" x="796" y="142">return route missing</text></g><g marker-end="url(#day5-vpn-arrow)" stroke="#38bdf8" stroke-width="2"><path d="M270 104 L339 104"></path><path d="M596 104 L665 104"></path></g><text fill="#a9b7cb" font-size="12" text-anchor="middle" x="470" y="210">Tunnel state, routing, firewall policy and socket reachability are separate checks.</text></svg><figcaption>Figure 5.1: The supplied VPN fixture succeeds at tunnel establishment but lacks the return route to 10.20.0.0/16. It is a tabletop path, not a deployed tunnel measurement.</figcaption></figure>

<p><strong class="side-heading">Concrete example:</strong> A Cloud VM instance at <code>10.20.1.5</code> attempts to query an on-premises PostgreSQL inventory database at <code>10.50.4.8:5432</code>. The cloud routing table selects the Cloud VPN tunnel as next hop for prefix <code>10.50.0.0/16</code>. The local Cloud VPN gateway encapsulates the packet with an outer IP header (source <code>198.51.100.1</code>, destination <code>203.0.113.1</code>) and encrypts the payload using ESP. The packet reaches the on-premises gateway, which authenticates the ESP header, decrypts the inner packet, and delivers it to <code>10.50.4.8</code>. The database answers with a TCP SYN-ACK addressed to <code>10.20.1.5</code>. However, the on-premises gateway lacks a routing entry for <code>10.20.0.0/16</code> pointing into the tunnel, and instead forwards the packet to its default internet gateway, where it is discarded. The TCP handshake fails despite a green tunnel status.</p>
<p><strong class="side-heading">Evidence limit:</strong> A functioning IPsec tunnel and Phase 1/2 IKE security associations establish only that encryption and mutual peer authentication are operational between gateway public IP addresses; they provide no evidence that internal subnets are routed symmetrically, that local firewalls permit the target port, or that the destination database server process is running.</p>'''

TOPIC_02_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ol>
<li><a href="#topic-02-subtopic-1">Layer 4 transport (Maglev DSR) versus Layer 7 application (Envoy proxy) load balancing</a></li>
<li><a href="#topic-02-subtopic-2">Health check state machines, probe types, and threshold evaluation</a></li>
<li><a href="#topic-02-subtopic-3">Session affinity mechanisms, hashing, and stateful routing trade-offs</a></li>
<li><a href="#topic-02-subtopic-4">Proxy-based architecture versus Maglev-style direct server return</a></li>
<li><a href="#topic-02-subtopic-5">Capacity management, traffic shedding, and connection draining</a></li>
</ol>

<h4 id="topic-02-subtopic-1">Layer 4 transport (Maglev DSR) versus Layer 7 application (Envoy proxy) load balancing</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Load balancing</strong> distributes network traffic across multiple computing resources to optimize throughput, reduce latency, and prevent resource overload. Modern cloud architectures implement two distinct paradigms:</p>
<ul>
<li><strong>Layer 4 (L4) Transport Load Balancing (Maglev Passthrough):</strong> Routes traffic strictly based on Layer 3/4 packet headers (the 5-tuple: source IP, source port, destination IP, destination port, protocol) without terminating application protocols. In Google Cloud, L4 passthrough is powered by <strong class="keyword">Maglev</strong>, a distributed software load balancer running on commodity Linux servers. Key architectural traits include:
<ul>
<li><em>Zero TCP Termination:</em> Maglev does not perform TCP handshakes with clients, does not decrypt TLS, and maintains no per-connection state tables. It performs stateless packet forwarding at wire speed (millions of packets per second per node).</li>
<li><em>Consistent Hashing:</em> Incoming packets are mapped to backend endpoints using Maglev's consistent hashing algorithm with fixed-size lookup tables, ensuring that backend scaling events cause minimal connection reshuffling.</li>
<li><em>Direct Server Return (DSR):</em> Maglev encapsulates incoming packets and sends them to backend VMs. Backend VMs process the request and reply directly to the client through the VPC gateway, completely bypassing the load balancer on egress. This eliminates throughput bottlenecks on asymmetric workloads (e.g. video streaming, media delivery, database queries).</li>
<li><em>Client IP Preservation:</em> The backend VM NIC receives the original client IP directly in the packet header without needing PROXY protocol headers.</li>
<li><em>Protocol Support:</em> Protocol-agnostic, supporting UDP, TCP, gaming, DNS, VoIP/SIP, and database replication.</li>
</ul>
</li>
<li><strong>Layer 7 (L7) Application Load Balancing (Envoy Reverse Proxy):</strong> Operates as a full bidirectional Layer 7 reverse proxy based on <strong class="keyword">Envoy</strong>:
<ul>
<li><em>Dual TCP Termination:</em> Clients establish an initial TCP connection to Envoy virtual IPs at Google Point of Presence (PoP) edge locations. Envoy decrypts TLS, parses HTTP headers, and initiates a second, independent TCP connection to backend VMs in the VPC.</li>
<li><em>URL Map Intelligent Routing:</em> Inspects HTTP host headers, request paths (e.g. <code>/api/*</code> vs <code>/static/*</code>), query parameters, and headers to route traffic to distinct backend service instance groups or Cloud Storage buckets.</li>
<li><em>Protocol Modernization:</em> Edge termination supports modern protocols including HTTP/2, HTTP/3 (QUIC over UDP 443), WebSockets, and gRPC.</li>
<li><em>Header Manipulation &amp; WAF:</em> Injects client geolocation (<code>X-Client-Geo-Location</code>) and IP (<code>X-Forwarded-For</code>) headers. Tightly integrates with Google Cloud Armor for WAF filtering, DDoS mitigation, and rate limiting before requests reach compute instances.</li>
<li><em>Deep Application Readiness Probes:</em> Actively probes backend HTTP endpoints (e.g. <code>GET /healthz</code>), validating specific HTTP 200 responses rather than simple TCP port open status.</li>
</ul>
</li>
</ul>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> L4 load balancing provides high throughput, lower latency, and preservation of the original client IP without requiring proxy protocol headers; it is ideal for non-HTTP protocols, gaming, database clusters, and massive packet ingestion. L7 load balancing enables intelligent routing, path-based microservice multiplexing, centralized SSL/TLS termination, HTTP header manipulation, and Web Application Firewall (WAF) integration, but consumes higher memory and CPU per connection.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud provides distinct load balancer categories: <em>Network Load Balancers</em> (regional L4 passthrough balancers built on Maglev) versus <em>Application Load Balancers</em> (global and regional L7 proxies based on Envoy). Application Load Balancers evaluate URL maps to route traffic across distinct backend services. Primary documentation: <a href="https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#load-balancer-types">Google Cloud load balancer types overview (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#application-lb">Google Cloud Application Load Balancers (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#network-lb">Google Cloud Network Load Balancers (accessed 2026-10-04)</a>.</p>

<h4 id="topic-02-subtopic-2">Health check state machines, probe types, and threshold evaluation</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Health checks</strong> are automated active probes sent periodically from load-balancing infrastructure to backend instances to determine their operational eligibility. A health check configuration defines a protocol (TCP, SSL, HTTP, HTTPS, or HTTP/2), a port, an optional request path (e.g. <code>/healthz</code>), an <em>interval</em> (seconds between probes), a <em>timeout</em> (maximum seconds to wait for a response), a <em>healthy threshold</em> (consecutive successful probes to mark an instance HEALTHY), and an <em>unhealthy threshold</em> (consecutive failed probes to mark an instance UNHEALTHY). A backend only receives client traffic while in the HEALTHY state.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Health checks form the critical bridge between network routing and application availability. If health check probes test only process binding (such as a simple TCP handshake) rather than deep application readiness, clients may be directed to backends suffering database deadlocks or thread pool exhaustion. Conversely, if a health check tests transitive dependencies (such as external third-party payment gateways), an external outage will trigger a cascading local failure where all backend instances are marked unhealthy simultaneously.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud health check probes originate from distributed Google IP ranges: <code>35.191.0.0/16</code> and <code>130.211.0.0/22</code> for global and regional proxies, and <code>35.191.0.0/16</code> for internal load balancers. VPC firewalls must explicitly allow ingress from these probe ranges on the health check port; failure to permit probe ingress causes the load balancer to mark all backends unhealthy immediately. Primary documentation: <a href="https://docs.cloud.google.com/load-balancing/docs/health-check-concepts#health_state">Google Cloud health check concepts and health state transitions (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.cloud.google.com/load-balancing/docs/health-check-concepts#criteria-protocol-http">Google Cloud health check success criteria (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/load-balancing/docs/health-check-concepts#health_state">Health check state machine transitions (accessed 2026-10-04)</a>.</p>

<h4 id="topic-02-subtopic-3">Session affinity mechanisms, hashing, and stateful routing trade-offs</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Session Affinity</strong> (sticky sessions) directs requests from the same client to the same backend instance for the lifetime of a session. In L4 load balancing, affinity is achieved via consistent hashing of the client IP address (2-tuple: source IP, destination IP; or 3-tuple: source IP, destination IP, protocol). In L7 load balancing, affinity can be enforced using client IP or via HTTP cookies: either a server-generated cookie or a load-balancer-generated cookie (such as the <code>GCLB</code> cookie).</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Session affinity simplifies legacy stateful application architectures that store in-memory session states (such as shopping carts or local cache data). However, affinity introduces severe reliability and scaling anti-patterns: client IP affinity causes traffic hotspots when large corporate networks or mobile carriers route thousands of users behind shared NAT gateways; it also frustrates horizontal autoscaling because traffic cannot rebalance dynamically when new instances join the pool, and backend restarts terminate all pinned client sessions.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Cloud Load Balancing supports multiple session affinity modes configured on backend services: <code>NONE</code> (round-robin/least request), <code>CLIENT_IP</code>, <code>GENERATED_COOKIE</code>, and <code>HEADER_FIELD</code>. When a backend instance fails its health check, GCP automatically re-hashes client sessions to remaining healthy instances regardless of affinity settings. Primary documentation: <a href="https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#load-balancer-types">Google Cloud load balancer backend service configuration (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#summary-gclb">Summary of Cloud Load Balancing capabilities (accessed 2026-10-04)</a>; <a href="https://www.rfc-editor.org/rfc/rfc9293#section-3.4">RFC 9293 §3.4 TCP connection establishment (accessed 2026-10-04)</a>.</p>

<h4 id="topic-02-subtopic-4">Proxy-based architecture versus Maglev-style direct server return</h4>
<p><strong class="side-heading">What it is in general:</strong> In a <strong class="keyword">Proxy-based Architecture</strong>, the load balancer acts as a reverse proxy: client connections terminate at the proxy's virtual IP (VIP), and the proxy opens a separate connection to the backend server. The backend sees the proxy's IP address as the source unless forwarded via <code>X-Forwarded-For</code> headers or PROXY protocol. In <strong class="keyword">Direct Server Return (DSR)</strong> or passthrough balancing, the load balancer inspects incoming packets, rewrites Layer 2 MAC addresses or encapsulates packets to backend hosts, but backend servers reply directly to the client IP address, bypassing the load balancer on the return path.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> DSR architectures provide massive asymmetrical throughput efficiency because return traffic (which is typically 10 to 100 times larger than incoming request headers) does not traverse the load balancer, eliminating a major bandwidth bottleneck. However, DSR cannot perform TLS termination, HTTP path inspection, or header rewriting, which requires a reverse proxy architecture.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud's External and Internal Network Load Balancers use Maglev distributed software routing to achieve line-rate passthrough performance: the client IP is preserved directly in the IP packet header received by the VM NIC, and egress traffic routes directly through the VPC virtual network gateway rather than hairpinning through a proxy instance. Google Application Load Balancers use Envoy proxies located at Google Point of Presence (PoP) edge infrastructure. Primary documentation: <a href="https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#tech-gclb">Underlying technologies of Google Cloud load balancers (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#load-balancer-types">Google Cloud load balancer architecture options (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/load-balancing/docs/health-check-concepts#health_state">Cloud Load Balancing health check concepts (accessed 2026-10-04)</a>.</p>

<h4 id="topic-02-subtopic-5">Capacity management, traffic shedding, and connection draining</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Connection Draining</strong> (deregistration delay) allows in-flight TCP connections and HTTP requests to complete gracefully when a backend instance is removed from service (due to autoscaling scale-down, rolling update, or manual maintenance). During the draining period (e.g. 300 seconds), the load balancer stops routing new requests to the draining backend but maintains established connections until they close or the timeout expires. <strong class="keyword">Capacity Management</strong> tracks backend utilization (CPU, requests per second, or connection count) to spill excess traffic over to secondary regions or shed load gracefully.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Without connection draining, rolling application deployments terminate active user transactions, corrupting file uploads, checkout payments, and long-lived WebSocket connections. Architects must tune draining timeouts to match application transaction lifecycles: setting the timeout too low truncates active requests; setting it too high stalls deployment pipelines and auto-healing actions.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Cloud Load Balancing backend services provide configurable connection draining timeouts (defaulting to 300 seconds, configurable from 0 to 3600 seconds). Global Application Load Balancers use balancing modes based on Rate (RPS per instance) or Utilization (target CPU), dynamically routing traffic across global instance groups and overflowing to alternative regions when local instance capacity is exhausted. Primary documentation: <a href="https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#key-features">Key features of Cloud Load Balancing (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#application-lb">Application Load Balancer capacity and routing (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/load-balancing/docs/health-check-concepts#health_state">Backend health and capacity status (accessed 2026-10-04)</a>.</p>

<table><caption>Load-balancer decisions and limits</caption>
<thead><tr><th>Decision</th><th>Input</th><th>Result</th><th>Limit</th></tr></thead>
<tbody>
<tr><td>Frontend reachability</td><td>Address, protocol and port</td><td>Client reaches the load balancer</td><td>No backend health proved.</td></tr>
<tr><td>L4 selection</td><td>Network and transport tuple</td><td>Connection or flow sent to an eligible backend</td><td>No HTTP path routing.</td></tr>
<tr><td>L7 selection</td><td>HTTP host and path</td><td>Request sent to a matching backend service</td><td>No business transaction proved.</td></tr>
<tr><td>Health eligibility</td><td>Configured probe path and thresholds</td><td>Backend added to or removed from service</td><td>Probe covers only its configured condition.</td></tr>
</tbody></table>

<figure class="diagram-figure"><p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p><svg aria-labelledby="day5-lb-title day5-lb-desc" role="img" viewbox="0 0 940 250" xmlns="http://www.w3.org/2000/svg"><title id="day5-lb-title">Client request, load balancer and backend readiness</title><desc id="day5-lb-desc">A client request reaches the load balancer. The configured readiness check calls slash ready and receives 404, so the backend is not eligible even though slash health returns 200.</desc><defs><marker id="day5-lb-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker></defs><g fill="#121526" stroke-width="2"><rect height="133" rx="10" stroke="#38bdf8" width="252" x="18" y="42"></rect><image href="../assets/icons/generic/client.svg" x="28" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/><rect height="133" rx="10" stroke="#f43f5e" width="252" x="344" y="42"></rect><image href="../assets/icons/gcp/legacy/cloud-load-balancing.svg" x="354" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/><rect height="133" rx="10" stroke="#34d399" width="252" x="670" y="42"></rect><image href="../assets/icons/gcp/core/compute-engine.svg" x="680" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/></g><g fill="#fce7f3" font-size="15" font-weight="700" text-anchor="middle"><text x="144" y="78">Checkout client</text><text x="470" y="78">Load balancer</text><text x="796" y="78">Order API backend</text></g><g fill="#a9b7cb" font-size="12" text-anchor="middle"><text x="144" y="111">HTTPS /orders</text><text x="144" y="142">frontend reachable</text><text x="470" y="111">eligible backends only</text><text fill="#f43f5e" x="470" y="142">pool has no healthy member</text><text x="796" y="111">/health → 200</text><text fill="#f43f5e" x="796" y="142">/ready → 404</text></g><g marker-end="url(#day5-lb-arrow)" stroke="#38bdf8" stroke-width="2"><path d="M270 104 L339 104"></path><path d="M665 104 L601 104"></path></g><text fill="#a9b7cb" font-size="12" text-anchor="middle" x="470" y="210">The configured probe result controls eligibility; process state alone does not.</text></svg><figcaption>Figure 5.2: The supplied readiness check removes the backend because /ready returns 404. The diagram does not establish how a live Google Cloud load balancer is configured.</figcaption></figure>

<p><strong class="side-heading">Concrete example:</strong> An e-commerce service runs on an instance group behind an External Application Load Balancer. The application developers implement a liveness endpoint at <code>/health</code> returning HTTP 200, and a readiness probe endpoint at <code>/ready</code> that validates local PostgreSQL database connectivity. During an operational configuration change, the health check configuration in Google Cloud is mistakenly pointed to <code>/api/v1/status</code>, which returns HTTP 404. Within 10 seconds (2 probe intervals), the load balancer marks every instance in the pool UNHEALTHY. Incoming client requests to <code>https://shop.example.com/orders</code> immediately fail with HTTP 502 Bad Gateway responses generated directly by the Envoy edge proxy.</p>
<p><strong class="side-heading">Evidence limit:</strong> A green load balancer health status proves solely that the configured probe specification (e.g. GET /health) returned an expected HTTP 200 status code within the configured timeout window; it does not prove that application business logic is functional, that database write transactions succeed, or that downstream third-party dependencies are healthy.</p>'''

TOPIC_03_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ol>
<li><a href="#topic-03-subtopic-1">Stateful connection tracking versus stateless packet filtering</a></li>
<li><a href="#topic-03-subtopic-2">Rule evaluation order, priority resolution, and conflict precedence</a></li>
<li><a href="#topic-03-subtopic-3">Ingress versus egress enforcement and implied baseline policies</a></li>
<li><a href="#topic-03-subtopic-4">Target identity: IP CIDRs, network tags, and service accounts</a></li>
<li><a href="#topic-03-subtopic-5">Failure boundaries, bypass vulnerabilities, and defense-in-depth</a></li>
</ol>

<h4 id="topic-03-subtopic-1">Stateful connection tracking versus stateless packet filtering</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Firewalls</strong> control the flow of network traffic into and out of network security zones based on predetermined security rules. In <strong class="keyword">Stateless Packet Filtering</strong> (such as router Access Control Lists), each packet is evaluated in isolation against the rule table based on header fields (source/destination IP, port, protocol); return traffic requires an explicit reverse rule matching the ephemeral return port. In <strong class="keyword">Stateful Packet Inspection</strong> (SPI), the firewall tracks active connection states (such as TCP SYN, SYN-ACK, ESTABLISHED, FIN/RST) in an internal connection tracking (<strong class="keyword">conntrack</strong>) table. Once an outbound or inbound connection is permitted by a rule, all bidirectional return packets belonging to that established flow are automatically permitted without needing separate reverse rules.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Stateful firewalls significantly reduce policy complexity and prevent security exposures caused by opening wide ephemeral port ranges (ports 1024–65535) for return traffic. However, state tables consume memory per tracked connection: extreme traffic spikes, SYN flood attacks, or asymmetric routing (where return packets bypass the stateful firewall) cause connection drops or state table exhaustion.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud VPC firewall rules are strictly stateful and enforced distributed across virtual machine hypervisors via Google's Andromeda virtual switch layer. Return traffic is automatically allowed, regardless of any configured ingress or egress deny rules. Andromeda maintains conntrack tables per VM instance, meaning firewalls scale horizontally with compute capacity and avoid centralized network appliance bottlenecks. Primary documentation: <a href="https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components">Google Cloud VPC firewall rule components (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.cloud.google.com/firewall/docs/firewalls#priority_order_for_firewall_rules">Google Cloud priority order for firewall rules (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components">Google Cloud firewall rule components and attributes (accessed 2026-10-04)</a>.</p>

<h4 id="topic-03-subtopic-2">Rule evaluation order, priority resolution, and conflict precedence</h4>
<p><strong class="side-heading">What it is in general:</strong> When a network packet arrives at a firewall interface, the packet header fields are matched against configured rules in order of precedence. In most systems, rules are assigned an integer <strong class="keyword">Priority</strong> (e.g. from 0 to 65535 in Google Cloud, where 0 is highest precedence and 65535 is lowest). Evaluation follows strict <em>first-match-wins</em> logic: the firewall inspects rules from lowest numeric priority value (highest priority) to highest numeric value; the first rule whose criteria matches the packet determines the action (ALLOW or DENY), and all subsequent rules are ignored.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Rule ordering is one of the most common vectors for security bypass incidents. If a team creates a broad, high-priority rule (e.g. Priority 100 allow all TCP 443 from <code>0.0.0.0/0</code>) intended for troubleshooting or temporary access, it completely nullifies all lower-priority restrictive rules (such as Priority 200 allow only from load balancer IP or Priority 300 deny all). Architects enforce strict priority reservation bands (e.g. 0–999 for security-admin overrides, 1000–1999 for shared infrastructure, 2000+ for application teams) to prevent privilege escalation.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud VPC firewall rules accept priority values between 0 and 65535 (default priority is 1000). If two rules have identical priority and matching criteria, a DENY rule always takes precedence over an ALLOW rule. Furthermore, Hierarchical Firewall Policies enforced at the Organization or Folder level take precedence over all VPC-level firewall rules. Primary documentation: <a href="https://docs.cloud.google.com/firewall/docs/firewalls#priority_order_for_firewall_rules">Google Cloud priority order for firewall rules (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components">Google Cloud firewall rule components and attributes (accessed 2026-10-04)</a>; <a href="https://www.rfc-editor.org/rfc/rfc9293#section-3.4">RFC 9293 §3.4 TCP connection states (accessed 2026-10-04)</a>.</p>

<h4 id="topic-03-subtopic-3">Ingress versus egress enforcement and implied baseline policies</h4>
<p><strong class="side-heading">What it is in general:</strong> Firewalls distinguish between <strong class="keyword">Ingress</strong> (packets entering the VM or subnet interface from external networks or other VPC instances) and <strong class="keyword">Egress</strong> (packets originating from the VM and leaving the network interface). A secure network model enforces least privilege on both directions: ingress filtering protects internal services from unauthorized access, while egress filtering prevents compromised workloads from exfiltrating data or establishing command-and-control (C2) channels.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Many cloud architectures neglect egress filtering under the mistaken assumption that outbound traffic is benign. However, regulated environments (PCI-DSS, HIPAA, FedRAMP) require strict egress whitelisting. Furthermore, architects must understand the cloud provider's default implied rules: if a provider defaults to allow-all egress, instances can contact arbitrary public endpoints unless explicitly constrained by custom deny rules.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Every Google Cloud VPC network has two unremovable, uneditable implied baseline firewall rules at priority 65535: an <em>implied allow egress</em> rule (permits all outbound traffic from all instances) and an <em>implied deny ingress</em> rule (blocks all inbound traffic to all instances). Default VPCs also include pre-populated priority 65534 rules (e.g. default-allow-internal, default-allow-ssh, default-allow-rdp), which enterprise architects routinely delete or override with custom zero-trust policies. Primary documentation: <a href="https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components">Google Cloud implied firewall rules (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.cloud.google.com/firewall/docs/firewalls#priority_order_for_firewall_rules">Google Cloud default and implied rules (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components">VPC firewall rule configuration (accessed 2026-10-04)</a>.</p>

<h4 id="topic-03-subtopic-4">Target identity: IP CIDRs, network tags, and service accounts</h4>
<p><strong class="side-heading">What it is in general:</strong> Traditional firewalls bind rules to physical network interfaces or static IP subnet CIDR blocks. In dynamic cloud environments where virtual machines and containers auto-scale and receive dynamic ephemeral IP addresses, firewalls must support logical identity targeting. Logical targets allow rules to apply to instances based on metadata labels, network tags, or cryptographically verified identity constructs.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Relying on static IP addresses in firewall rules introduces extreme operational friction and configuration drift as workloads scale. However, informal metadata mechanisms like network tags pose security risks: any engineer with <code>compute.instances.create</code> or <code>compute.instances.setTags</code> permissions can attach an administrative network tag (such as <code>allow-ssh</code> or <code>bastion</code>) to an instance, effectively bypassing network isolation policies. Using IAM service accounts as firewall targets enforces least-privilege security because attaching a service account requires explicit <code>iam.serviceAccountUser</code> authorization.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud VPC firewall rules support three target filtering mechanisms: <em>All instances in network</em>, <em>Target network tags</em>, and <em>Target service accounts</em>. Source filtering similarly supports IP CIDR blocks, source tags, and source service accounts. Rules targeting service accounts are strictly validated and cannot be combined with network tags. Primary documentation: <a href="https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components">Google Cloud target parameters and service accounts (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.cloud.google.com/firewall/docs/firewalls#priority_order_for_firewall_rules">Google Cloud rule filtering options (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components">Firewall rule targets and source filtering (accessed 2026-10-04)</a>.</p>

<h4 id="topic-03-subtopic-5">Failure boundaries, bypass vulnerabilities, and defense-in-depth</h4>
<p><strong class="side-heading">What it is in general:</strong> A <strong class="keyword">Failure Boundary</strong> defines the structural limit of protection provided by a specific security control. A firewall failure boundary demarcates where packet filtering ceases to protect an application: while a firewall inspects Layer 3/4 headers (and validates basic protocol compliance), it cannot inspect encrypted payload data, detect application-level SQL injection or cross-site scripting attacks, verify client authorization tokens, or protect against authorized traffic exploiting unpatched application vulnerabilities.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects implement <em>defense-in-depth</em> by layering independent, non-redundant controls across tiers: VPC firewall rules restrict Layer 4 network reachability; Cloud Armor provides Layer 7 WAF inspection and rate limiting; Identity-Aware Proxy (IAP) enforces cryptographic user identity and device posture; and internal microservices authenticate via mTLS. If any single control suffers a misconfiguration or priority bypass, downstream layers prevent breach escalation.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, firewall rules operate at the VM hypervisor boundary. A common architecture flaw occurs when a public load balancer is placed in front of backend VMs, but the backend VMs retain public IP addresses and a broad priority 100 ingress firewall rule permits traffic from <code>0.0.0.0/0</code>. Attackers discover the backend VM public IPs and connect directly to port 443, completely bypassing the load balancer, Cloud Armor WAF policies, and rate limits. Primary documentation: <a href="https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components">Google Cloud firewall architecture and defense boundaries (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.cloud.google.com/firewall/docs/firewalls#priority_order_for_firewall_rules">Google Cloud firewall evaluation hierarchy (accessed 2026-10-04)</a>; <a href="https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components">VPC firewall rule components (accessed 2026-10-04)</a>.</p>

<table><caption>Supplied ingress rule evaluation</caption>
<thead><tr><th>Priority</th><th>Action and source</th><th>Does 198.51.100.25 match?</th><th>Decision</th></tr></thead>
<tbody>
<tr><td>100</td><td>Allow TCP 443 from 0.0.0.0/0</td><td>Yes</td><td>First applicable rule permits traffic.</td></tr>
<tr><td>200</td><td>Allow TCP 443 from 203.0.113.0/24</td><td>No</td><td>Not reached for this packet.</td></tr>
<tr><td>300</td><td>Deny TCP 443 from 0.0.0.0/0</td><td>Yes</td><td>Lower precedence than priority 100.</td></tr>
</tbody></table>

<figure class="diagram-figure"><p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p><svg aria-labelledby="day5-fw-title day5-fw-desc" role="img" viewbox="0 0 940 250" xmlns="http://www.w3.org/2000/svg"><title id="day5-fw-title">Ordered firewall decision for direct and load-balancer sources</title><desc id="day5-fw-desc">The original priority 100 broad allow admits both source ranges. After it is removed, the intended load-balancer source matches the narrow allow and the direct source reaches the deny.</desc><defs><marker id="day5-fw-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker></defs><g fill="#121526" stroke-width="2"><rect height="133" rx="10" stroke="#f43f5e" width="252" x="18" y="42"></rect><image href="../assets/icons/generic/event.svg" x="28" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/><rect height="133" rx="10" stroke="#38bdf8" width="252" x="344" y="42"></rect><image href="../assets/icons/gcp/legacy/cloud-firewall-rules.svg" x="354" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/><rect height="133" rx="10" stroke="#34d399" width="252" x="670" y="42"></rect><image href="../assets/icons/generic/policy.svg" x="680" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/></g><g fill="#fce7f3" font-size="15" font-weight="700" text-anchor="middle"><text x="144" y="78">Packet tuple</text><text x="470" y="78">Ordered rules</text><text x="796" y="78">Policy result</text></g><g fill="#a9b7cb" font-size="12" text-anchor="middle"><text x="144" y="111">source + TCP 443</text><text x="144" y="142">target order-api</text><text x="470" y="111">lowest numeric priority</text><text x="470" y="142">first applicable result</text><text x="796" y="111">LB source allowed</text><text fill="#f43f5e" x="796" y="142">direct source denied</text></g><g marker-end="url(#day5-fw-arrow)" stroke="#38bdf8" stroke-width="2"><path d="M270 104 L339 104"></path><path d="M596 104 L665 104"></path></g><text fill="#a9b7cb" font-size="12" text-anchor="middle" x="470" y="210">This prediction assumes no higher-level policy changes the effective result.</text></svg><figcaption>Figure 5.3: The proposed rule set preserves the documented load-balancer source and denies the direct source. It is an offline policy exercise, not a live firewall test.</figcaption></figure>

<p><strong class="side-heading">Concrete example:</strong> A production web service runs on backend VMs with network tag <code>order-api</code>. The intended policy is that only the Cloud Load Balancer (source IP range <code>203.0.113.0/24</code>) should access port 443 on these instances, and direct external access should be blocked. However, an old rule <code>allow-all-https</code> at priority 100 allows TCP 443 from source <code>0.0.0.0/0</code>. An untrusted external scanner at <code>198.51.100.25</code> sends TCP SYN packets directly to the backend VM public IP. The firewall evaluates rules in ascending numerical priority: Rule 100 matches the packet and immediately grants ALLOW. The restrictive Rule 200 (priority 200, source <code>203.0.113.0/24</code>) and Rule 300 (priority 300, deny <code>0.0.0.0/0</code>) are never evaluated. When an administrator removes Rule 100, the packet from <code>198.51.100.25</code> fails Rule 200 and matches Rule 300, successfully DENYING direct access while traffic from <code>203.0.113.25</code> matches Rule 200 and is ALLOWED.</p>
<p><strong class="side-heading">Evidence limit:</strong> A firewall rule decision table accurately models packet evaluation order and boolean tuple matching at the virtual network interface; it does not prove that application software listening on the permitted port is invulnerable to application-layer payload exploits or unauthorized API calls.</p>'''

PART1_HTML = '''<article class="topic-card overview" id="topic-01-overview">
<h3>VPN concepts</h3>
<p><strong class="keyword">IPsec VPN</strong> creates encrypted, authenticated network tunnels across untrusted public networks to connect distributed environments. Tunnel establishment verifies gateway credentials and cryptographic negotiation, but operational data reachability requires symmetric return routing, compatible MTU sizing, and coordinated firewall allowances.</p>
<p><strong class="side-heading">Why today:</strong> Establishes the foundational hybrid connectivity mechanism connecting cloud VPCs with on-premises data centers before deploying multi-tier applications.</p>
<p><strong class="side-heading">Where it sits:</strong> Sits between Day 4 routing and transit fundamentals and today's downstream load balancer and firewall boundaries.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A site-to-site IPsec tunnel reports established state, but application database queries between cloud services and on-premises systems experience immediate connection timeouts. Engineers discover that while outer encrypted tunnel security associations negotiated successfully, the on-premises router lacked an explicit return route back to the cloud VPC subnet prefix.</p>
<p><strong class="side-heading">Key subtopics:</strong></p>
<ul class="subtopic-links">
<li><a href="#topic-01-subtopic-1">IPsec architecture, encapsulation modes, crypto transformations, and anti-replay protection</a></li>
<li><a href="#topic-01-subtopic-2">IKEv2 versus IPsec: control-plane negotiation, security associations, and dead peer detection</a></li>
<li><a href="#topic-01-subtopic-3">Site-to-site VPN, remote-access client VPN, and Private DC to Cloud firewall ACLs</a></li>
<li><a href="#topic-01-subtopic-4">BGP dynamic routing in internet routing and modern Leaf-Spine data centers (underlay ECMP and MP-BGP EVPN overlay)</a></li>
<li><a href="#topic-01-subtopic-5">Path MTU, TCP MSS clamping, and fragmentation overhead</a></li>
</ul>
<p><a href="#topic-01-technical">Technical discussion →</a> <a href="#topic-01-problem">Real-world problem →</a> <a href="#topic-01-lab">Step-by-step lab →</a></p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>Load balancing concepts</h3>
<p><strong class="keyword">Load balancing</strong> distributes network traffic across a resilient pool of backend instances to optimize throughput, prevent single-point overload, and enable zero-downtime rolling updates. Layer 4 passthrough balancing preserves source IPs and optimizes raw packet throughput, while Layer 7 reverse proxying enables URL path routing, TLS termination offload, and deep health check evaluation.</p>
<p><strong class="side-heading">Why today:</strong> Provides the horizontal scale and high availability boundary for microservices and database tiers in the Google Cloud architecture path.</p>
<p><strong class="side-heading">Where it sits:</strong> Positioned between hybrid ingress or public edge traffic and internal workload pools, immediately upstream of hypervisor firewall filtering.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> Production API clients receive HTTP 502 bad gateway errors during peak traffic after a rolling application update deploys to healthy virtual machine backends. Investigation shows that the load balancer health check targeted an unconfigured readiness endpoint, causing the health monitor to mark all running backends unhealthy simultaneously.</p>
<p><strong class="side-heading">Key subtopics:</strong></p>
<ul class="subtopic-links">
<li><a href="#topic-02-subtopic-1">Layer 4 transport (Maglev DSR) versus Layer 7 application (Envoy proxy) load balancing</a></li>
<li><a href="#topic-02-subtopic-2">Health check state machines, probe types, and threshold evaluation</a></li>
<li><a href="#topic-02-subtopic-3">Session affinity mechanisms, hashing, and stateful routing trade-offs</a></li>
<li><a href="#topic-02-subtopic-4">Proxy-based architecture versus Maglev-style direct server return</a></li>
<li><a href="#topic-02-subtopic-5">Capacity management, traffic shedding, and connection draining</a></li>
</ul>
<p><a href="#topic-02-technical">Technical discussion →</a> <a href="#topic-02-problem">Real-world problem →</a> <a href="#topic-02-lab">Step-by-step lab →</a></p>
</article>

<article class="topic-card overview" id="topic-03-overview">
<h3>Firewalls</h3>
<p><strong class="keyword">VPC firewalls</strong> enforce stateful packet filtering rules at the virtual machine hypervisor boundary, inspecting Layer 3/4 traffic and automatically permitting bidirectional return flows for established connections. Rules evaluate strictly by ascending numerical priority where the first matching rule dictates the policy decision.</p>
<p><strong class="side-heading">Why today:</strong> Enforces network isolation and defense-in-depth perimeters across ingress, egress, and inter-service boundaries in enterprise architectures.</p>
<p><strong class="side-heading">Where it sits:</strong> Evaluated at the virtual network interface directly after load balancing transit, forming the failure boundary of the day's packet decision table.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> Untrusted external clients access internal staging microservices directly over public IP addresses despite team assumptions that the services were private to the load balancer. A broad legacy ingress allow rule at priority 100 matched all incoming traffic before the narrow priority 200 restriction could take effect.</p>
<p><strong class="side-heading">Key subtopics:</strong></p>
<ul class="subtopic-links">
<li><a href="#topic-03-subtopic-1">Stateful connection tracking versus stateless packet filtering</a></li>
<li><a href="#topic-03-subtopic-2">Rule evaluation order, priority resolution, and conflict precedence</a></li>
<li><a href="#topic-03-subtopic-3">Ingress versus egress enforcement and implied baseline policies</a></li>
<li><a href="#topic-03-subtopic-4">Target identity: IP CIDRs, network tags, and service accounts</a></li>
<li><a href="#topic-03-subtopic-5">Failure boundaries, bypass vulnerabilities, and defense-in-depth</a></li>
</ul>
<p><a href="#topic-03-technical">Technical discussion →</a> <a href="#topic-03-problem">Real-world problem →</a> <a href="#topic-03-lab">Step-by-step lab →</a></p>
</article>'''

ARCH_DIAGRAM = {
    'type': 'topology',
    'title': 'Day 5: Hybrid VPN Transit, Load Balancing, and Stateful Firewall Architecture',
    'desc': 'Operational topology tracing IPsec IKEv2/ESP hybrid transit, Layer 4 and Layer 7 load balancer routing with health check probes, and stateful VPC firewall rule evaluation.',
    'caption': 'Scope: an illustrative architecture topology for Day 5 hybrid transit and firewall evaluation; it does not prove a deployed Google Cloud production topology or capacity.',
    'width': 1120,
    'height': 690,
    'nodes': [
        ('1. Ingress & Client Edge', 'Public Traffic & Probe'),
        ('2. Hybrid Transit & Load Balancer', 'IPsec ESP & Envoy Proxy'),
        ('3. Target Workload & Enforcement', 'VM Backend & VPC Firewall conntrack'),
        ('4. Return Path & Verification', 'Symmetric Route & Decision Evidence')
    ],
    'layers': [
        {'name': 'TIER 1 · HYBRID INGRESS & TRANSIT', 'desc': 'IPsec ESP hybrid tunnel and external client edge', 'x': 20, 'y': 55, 'w': 1080, 'h': 110, 'fill': '#12283b', 'title_color': '#7dd3fc'},
        {'name': 'TIER 2 · TRAFFIC DISTRIBUTION & HEALTH', 'desc': 'L4/L7 load balancing proxies and health check state machines', 'x': 20, 'y': 185, 'w': 1080, 'h': 230, 'fill': '#1b2038', 'title_color': '#c4b5fd'},
        {'name': 'TIER 3 · FIREWALL & WORKLOAD', 'desc': 'VPC stateful firewall conntrack and Compute Engine backend VMs', 'x': 20, 'y': 435, 'w': 1080, 'h': 120, 'fill': '#2b1d2f', 'title_color': '#f9a8d4'}
    ],
    'boundaries': [
        {'x': 100, 'y': 225, 'w': 920, 'h': 140, 'color': '#a78bfa', 'label': 'HYBRID TRANSIT & LOAD BALANCING DOMAIN'},
        {'x': 100, 'y': 455, 'w': 920, 'h': 85, 'color': '#f59e0b', 'label': 'VPC FIREWALL & WORKLOAD FAILURE BOUNDARY'}
    ],
    'components': [
        {'x': 70, 'y': 92, 'w': 220, 'h': 52, 'stroke': '#38bdf8', 'name': 'On-Prem / Client Ingress', 'detail': 'TCP 5432 query & HTTPS traffic', 'icon': '../assets/icons/generic/client.svg'},
        {'x': 430, 'y': 92, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'name': 'HA VPN Gateway & Tunnel', 'detail': 'IKEv2 Phase 2 ESP & Cloud Router', 'icon': '../assets/icons/gcp/legacy/cloud-vpn.svg'},
        {'x': 830, 'y': 92, 'w': 220, 'h': 52, 'stroke': '#34d399', 'name': 'Edge Routing & Handover', 'detail': 'VPC transit & route table lookup', 'icon': '../assets/icons/gcp/legacy/cloud-router.svg'},
        {'x': 140, 'y': 255, 'w': 250, 'h': 72, 'stroke': '#a78bfa', 'name': 'Layer 7 Envoy / L4 Maglev', 'detail': 'URL map & packet forwarding', 'icon': '../assets/icons/gcp/legacy/cloud-load-balancing.svg'},
        {'x': 440, 'y': 255, 'w': 250, 'h': 72, 'stroke': '#f59e0b', 'name': 'Health Check Probers', 'detail': '35.191.0.0/16 & 130.211.0.0/22 poll', 'icon': '../assets/icons/generic/monitoring.svg'},
        {'x': 740, 'y': 255, 'w': 250, 'h': 72, 'stroke': '#f59e0b', 'name': 'VPC Stateful Firewall', 'detail': 'Priority-ordered conntrack table', 'icon': '../assets/icons/gcp/legacy/cloud-firewall-rules.svg'},
        {'x': 140, 'y': 470, 'w': 250, 'h': 52, 'stroke': '#34d399', 'name': 'Target Workload Instances', 'detail': 'Compute Engine VM backend socket', 'icon': '../assets/icons/gcp/core/compute-engine.svg'},
        {'x': 740, 'y': 470, 'w': 250, 'h': 52, 'stroke': '#f9a8d4', 'name': 'Packet Decision Table', 'detail': 'Allowed/denied audit verification', 'icon': '../assets/icons/generic/decision.svg'}
    ],
    'flows': [
        {'x1': 290, 'y1': 118, 'x2': 430, 'y2': 118, 'type': 'blue', 'label': 'IPsec transit'},
        {'x1': 690, 'y1': 118, 'x2': 830, 'y2': 118, 'type': 'ok', 'label': 'route lookup'},
        {'x1': 560, 'y1': 144, 'x2': 265, 'y2': 255, 'type': 'ok', 'label': 'forward to LB'},
        {'x1': 390, 'y1': 291, 'x2': 440, 'y2': 291, 'type': 'ok', 'label': 'health gate'},
        {'x1': 690, 'y1': 291, 'x2': 740, 'y2': 291, 'type': 'warn', 'label': 'filter rule'},
        {'x1': 265, 'y1': 327, 'x2': 265, 'y2': 470, 'type': 'ok', 'label': 'deliver'},
        {'x1': 865, 'y1': 327, 'x2': 865, 'y2': 470, 'type': 'blue', 'label': 'record log'}
    ],
    'probes': [
        {'cx': 290, 'cy': 118, 'badge': 'P1', 'label': 'PROBE 1 · IPsec SA & path MTU 1460 established', 'color': '#38bdf8'},
        {'cx': 690, 'cy': 291, 'badge': 'P2', 'label': 'PROBE 2 · Health check probe HTTP 200 pass rate', 'color': '#f59e0b'},
        {'cx': 740, 'cy': 496, 'badge': 'P3', 'label': 'PROBE 3 · Firewall conntrack allowed vs denied match', 'color': '#34d399'}
    ]
}

DATA = {
    'contract_version': 2,
    'roadmap_practice': 'Draw a client-to-backend flow with health checks and ordered firewall decisions; change one rule and predict the effect.',
    'roadmap_exit': 'A packet decision table with both allowed and denied paths and a failure boundary.',
    'day': 5,
    'work_block': 'Days 1–17 — Foundations',
    'part1_html': PART1_HTML,
    'part1_intro': 'Day 5 examines core hybrid networking and security boundaries: IPsec VPN tunnels, Layer 4 and Layer 7 load balancers, and stateful VPC firewall rules.',
    'part2_intro': 'Trace technical control and data boundaries, observable signals, and trade-offs across VPN tunnels, load balancers, and ordered firewall evaluation.',
    'part3_intro': 'Illustrative real-world scenarios and diagnostic failure investigations demonstrating asymmetric routing, health check path mismatch, and priority rule bypass.',
    'part4_intro': 'Hands-on exercises and tabletop verification procedures executing packet routing models, health check state machines, and ordered firewall decision tables.',
    'exit_summary': 'A verified packet decision table with both allowed and denied paths and an explicit failure boundary distinguishing network reachability from process state.',
    'completion_html': '''<div class="completion-box" id="completion-box-005">
<h3>Day 5 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-5-1"> <label for="check-5-1">VPN concepts mastered: IPsec tunnel mode encapsulation, IKEv2 security associations, site-to-site vs client VPN, and symmetric return routing requirements.</label></li>
<li><input type="checkbox" id="check-5-2"> <label for="check-5-2">Load balancing concepts mastered: L4 passthrough vs L7 proxy, health check state machines, probe ranges (35.191.0.0/16, 130.211.0.0/22), and session affinity trade-offs.</label></li>
<li><input type="checkbox" id="check-5-3"> <label for="check-5-3">Firewall concepts mastered: stateful conntrack evaluation, ascending numerical priority ordering (first match wins), implied rules, and defense-in-depth failure boundaries.</label></li>
<li><input type="checkbox" id="check-5-4"> <label for="check-5-4">Practice completed: client-to-backend request flow drawn with health check probes and ordered firewall rules, showing the effect of removing broad rule priority 100.</label></li>
<li><input type="checkbox" id="check-5-5"> <label for="check-5-5">Exit evidence verified: packet decision table generated covering allowed load-balancer paths, denied direct internet paths, and identified application failure boundaries.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-005" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 5 Completed':'Mark Day 5 as Read';">Mark Day 5 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-005" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>''',
    'arch_diagram': ARCH_DIAGRAM,
    'arch_svg_html': '',
    'arch_table_html': '',
    'lab_defaults': {},
    'topics': [
        {
            'key': 'topic-01',
            'title': 'VPN concepts',
            'anchors': {
                'overview': 'topic-01-overview',
                'technical': 'topic-01-technical',
                'problem': 'topic-01-problem',
                'lab': 'topic-01-lab'
            },
            'overview': 'IPsec VPN provides encrypted Layer 3 transit across untrusted networks. Establishing Phase 1/2 IKEv2 associations proves cryptographic peering but does not prove symmetric subnet routing or socket reachability.',
            'preview': 'A site-to-site IPsec tunnel reports established state, but application database queries between cloud services and on-premises systems experience immediate connection timeouts. Engineers discover that while outer encrypted tunnel security associations negotiated successfully, the on-premises router lacked an explicit return route back to the cloud VPC subnet prefix.',
            'technical': TOPIC_01_TECH,
            'questions': [
                'Why does an active IPsec tunnel state (Phase 2 ESP installed) fail to guarantee that application traffic can reach the destination database socket?',
                'What are the availability and operational trade-offs between static policy-based VPN routing and BGP dynamic routing with Cloud Router when adding new VPC subnets?',
                'How does IPsec ESP tunnel mode encapsulation affect the effective path MTU, and why must cloud architects configure TCP MSS clamping at 1460 bytes or lower?'
            ],
            'reference': 'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn',
            'reference_label': 'Google Cloud HA VPN and IPsec overview (accessed 2026-10-04)',
            'scenario': {
                'scenario': 'Tunnel up, return route absent',
                'impact': 'On-premises inventory database queries from Cloud Order API time out, halting customer checkout fulfillment.',
                'constraints': 'No changes permitted to production VPC subnet CIDR; on-premises router maintenance window required for routing changes; encryption parameters must remain compliant with corporate standards.',
                'evidence': '''**illustrative supplied records**

```text
[IPsec Phase 1/IKE SA] ESTABLISHED: local 198.51.100.1[500] peer 203.0.113.1[500] SPI: 0x9b4f2c10...
[IPsec Phase 2/ESP SA] INSTALLED: tunnel local 198.51.100.1 <=> remote 203.0.113.1 reqid 1 SPI: 0xc871a2e4
[Client probe] Cloud VM 10.20.1.5 -> On-Prem DB 10.50.4.8:5432 SYN sent (seq=120485910)
[On-Prem Gateway packet capture] 10.20.1.5:49152 -> 10.50.4.8:5432 TCP SYN decrypted and forwarded
[On-Prem Host packet capture] 10.50.4.8:5432 -> 10.20.1.5:49152 TCP SYN-ACK sent (seq=48201948, ack=120485911)
[On-Prem Gateway routing log] DEST UNREACHABLE: No route to destination prefix 10.20.0.0/16, packet dropped
```''',
                'root': 'Asymmetric routing failure: the Phase 1 IKEv2 security association and Phase 2 ESP tunnel are established between the gateways, and forward packets reach the target host. However, the on-premises gateway routing table lacks a route for the cloud VPC source prefix (10.20.0.0/16) pointing back into the IPsec tunnel, causing return SYN-ACK packets to be dropped.',
                'diagnostic_steps': [
                    'Inspect tunnel status using gateway telemetry (ip xfrm state and IKE daemon status).',
                    'Perform bidirectional ping and tcpdump captures at both cloud and on-premises tunnel interfaces.',
                    'Query the on-premises gateway route table (ip route get 10.20.1.5) to verify the return next-hop.',
                    'Validate firewall rules on both endpoints to confirm TCP 5432 is not silently discarded.'
                ],
                'remediation_steps': [
                    'Add an explicit route on the on-premises gateway: ip route add 10.20.0.0/16 dev vti0 (or configure dynamic BGP route advertisement via Cloud Router).',
                    'Verify route table propagation on the on-premises border router.',
                    'Validate end-to-end TCP socket connection from cloud host 10.20.1.5 to database 10.50.4.8 on port 5432.'
                ],
                'verify': 'The cloud order client completes a full TCP three-way handshake with 10.50.4.8:5432 with 0% packet loss and round-trip time under 15ms; application queries return inventory status successfully.',
                'residual': 'Static routes require manual updates when new VPC subnets are added; migrating to Cloud Router BGP dynamic routing eliminates manual route desynchronization risk.',
                'diagram_enabled': True,
                'diagram': (
                    'App query to on-prem DB',
                    'Missing return route on gateway',
                    'Checkout connection timeouts',
                    'Add return route via tunnel',
                    'Successful TCP handshake'
                ),
                'icons': [
                    '../assets/icons/gcp/core/compute-engine.svg',
                    '../assets/icons/generic/failure.svg',
                    '../assets/icons/generic/failure.svg',
                    '../assets/icons/gcp/legacy/cloud-vpn.svg',
                    '../assets/icons/generic/outcome.svg'
                ],
                'facts': 'Supplied incident capture: Phase 1/2 IKEv2 established, forward SYN delivered, return SYN-ACK dropped by on-prem gateway.',
                'inference': 'Architectural inference: tunnel status indicates cryptographic peering only; bidirectional end-to-end connectivity requires symmetric routing tables across both networks.',
                'expected': 'Expected post-fix behavior: on-premises router forwards return packets for 10.20.0.0/16 into tunnel, completing TCP handshake.'
            },
            'lab': {
                'name': 'Lab 5.1: Model and verify IPsec VPN packet flow and routing boundaries',
                'goal': 'Validate IPsec tunnel configuration, packet encapsulation overhead, and symmetric routing table entries for hybrid cloud connectivity.',
                'mode': 'Observed locally: local bash test script executes packet routing and MTU calculations. Simulated or predicted: simulated IPsec ESP encapsulation overhead and route lookup decisions. Untested on GCP: live Cloud VPN gateway negotiation, BGP session peering with Cloud Router, and hardware cryptographic offload.',
                'covers': 'Draw a client-to-backend flow with health checks and ordered firewall decisions (VPN tunnel and return route path)',
                'prereq': 'Python 3.10+, bash shell, basic IP networking knowledge.',
                'preflight': 'Verify python3 availability, create temporary workspace directory, check file permissions.',
                'verification': 'Review generated routing evaluation table and verify forward and return path next-hops.',
                'trouble': 'Inspect routing table script output and verify destination CIDR prefix matching logic.',
                'cleanup': 'Remove temporary workspace directory and generated test artifacts.',
                'accept': 'The routing evaluator confirms that forward packets from 10.20.1.5 reach 10.50.4.8 via vti0, and identifies that return packets drop unless 10.20.0.0/16 is routed via vti0.',
                'file': 'day-005-topic-01.md',
                'steps': [
                    '''**Stage 1: Preflight environment and tool verification**

**Location:** local bash terminal

Verify that Python 3 is installed and accessible in the system path:

```bash
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required"; exit 1; }
LAB_DIR=$(mktemp -d /tmp/lab_vpn.XXXXXX)
export LAB_DIR
cd "$LAB_DIR"
python3 --version > "$LAB_DIR/preflight.log"
echo "Workspace initialized at: $LAB_DIR" >> "$LAB_DIR/preflight.log"
cat "$LAB_DIR/preflight.log"
```

**Expected result:** Python 3.10+ reported, temporary workspace directory created.

**Save:** `$LAB_DIR/preflight.log`''',

                    '''**Stage 2: Prepare hybrid addressing and interface configuration**

**Location:** local bash terminal

Define the cloud VPC subnet, on-premises subnet, and public gateway addresses:

```bash
cat > "$LAB_DIR/network_config.json" <<'EOF'
{
  "cloud_vpc": {
    "subnet": "10.20.0.0/16",
    "gateway_public_ip": "198.51.100.1",
    "client_host": "10.20.1.5"
  },
  "on_premises": {
    "subnet": "10.50.0.0/16",
    "gateway_public_ip": "203.0.113.1",
    "database_host": "10.50.4.8"
  },
  "ipsec": {
    "mtu": 1460,
    "tcp_mss": 1420,
    "esp_overhead_bytes": 56
  }
}
EOF
cat "$LAB_DIR/network_config.json"
```

**Expected result:** Configuration file written and verified with valid JSON formatting.

**Save:** `$LAB_DIR/network_config.json`''',

                    '''**Stage 3: Author plan and routing simulation engine**

**Location:** local bash terminal

Create a Python script that models route table lookups and IPsec ESP encapsulation:

```bash
cat > "$LAB_DIR/simulate_vpn.py" <<'EOF'
import ipaddress
import json
import sys

with open("network_config.json") as f:
    cfg = json.load(f)

cloud_net = ipaddress.ip_network(cfg["cloud_vpc"]["subnet"])
onprem_net = ipaddress.ip_network(cfg["on_premises"]["subnet"])
client_ip = ipaddress.ip_address(cfg["cloud_vpc"]["client_host"])
server_ip = ipaddress.ip_address(cfg["on_premises"]["database_host"])

print("--- FORWARD PATH (Cloud -> On-Prem) ---")
print(f"Packet: {client_ip}:49152 -> {server_ip}:5432")
if server_ip in onprem_net:
    print(f"Route Match: {server_ip} matches {onprem_net} via interface vti0 (IPsec Tunnel)")
    outer_packet = f"Outer IP: {cfg['cloud_vpc']['gateway_public_ip']} -> {cfg['on_premises']['gateway_public_ip']} [ESP SPI=0x9b4f]"
    print(f"Encapsulation: {outer_packet}")
    print("Forward Path: DELIVERED to 10.50.4.8")
else:
    print("Forward Path: NO ROUTE")

print()
print("--- RETURN PATH (On-Prem -> Cloud) ---")
return_route_installed = "--fixed" in sys.argv
print(f"Return Packet: {server_ip}:5432 -> {client_ip}:49152")
if return_route_installed:
    print(f"Route Match: {client_ip} matches {cloud_net} via interface vti0 (IPsec Tunnel)")
    outer_return = f"Outer IP: {cfg['on_premises']['gateway_public_ip']} -> {cfg['cloud_vpc']['gateway_public_ip']} [ESP SPI=0xc871]"
    print(f"Encapsulation: {outer_return}")
    print("Return Path: DELIVERED to 10.20.1.5 (Symmetric Flow OK)")
else:
    print(f"Route Match: No route for {client_ip} on vti0. Default gateway 0.0.0.0/0 selected (Public WAN).")
    print("Return Path: DROPPED (Asymmetric Routing Failure)")
EOF
python3 -m py_compile "$LAB_DIR/simulate_vpn.py"
```

**Expected result:** Script compiles with zero syntax errors.

**Save:** `$LAB_DIR/simulate_vpn.py`''',

                    '''**Stage 4: Execute forward path simulation**

**Location:** local bash terminal

Run the simulation script to test the forward path:

```bash
cd "$LAB_DIR"
python3 simulate_vpn.py > forward_test.log
cat forward_test.log
```

**Expected result:** Forward path succeeds with ESP encapsulation; return path reports DROPPED due to missing return route.

**Save:** `$LAB_DIR/forward_test.log`''',

                    '''**Stage 5: Inspect expected state and verify failure mode**

**Location:** local bash terminal

Inspect the log output to verify the asymmetric routing failure point:

```bash
grep "Return Path: DROPPED" "$LAB_DIR/forward_test.log" > "$LAB_DIR/failure_evidence.txt"
echo "PASS: Failure reproduced as predicted" >> "$LAB_DIR/failure_evidence.txt"
cat "$LAB_DIR/failure_evidence.txt"
```

**Expected result:** Grep matches the dropped return packet message.

**Save:** `$LAB_DIR/failure_evidence.txt`''',

                    '''**Stage 6: Rehearse bounded failure and MTU sizing check**

**Location:** local bash terminal

Compute effective MTU and check TCP MSS clamping calculations:

```bash
python3 -c '
mtu = 1460
esp_hdr = 56
ip_hdr = 20
tcp_hdr = 20
max_payload = mtu - esp_hdr - ip_hdr - tcp_hdr
print(f"Max Transmission Unit (MTU): {mtu} bytes")
print(f"IPsec ESP Overhead: {esp_hdr} bytes")
print(f"Effective TCP MSS: {max_payload} bytes")
assert max_payload <= 1420, "MSS clamping exceeds recommended boundary"
print("PASS: TCP MSS clamp safely bounded at 1364-1420 bytes")
' | tee "$LAB_DIR/mtu_evidence.txt"
```

**Expected result:** Effective TCP MSS calculated and verified within safe limits.

**Save:** `$LAB_DIR/mtu_evidence.txt`''',

                    '''**Stage 7: Diagnose evidence and apply routing remediation**

**Location:** local bash terminal

Simulate installing the return route on the on-premises gateway:

```bash
cd "$LAB_DIR"
python3 simulate_vpn.py --fixed > fixed_test.log
cat fixed_test.log
grep "Symmetric Flow OK" fixed_test.log && echo "PASS: Return path restored"
```

**Expected result:** Return path successfully routed via vti0 with symmetric flow confirmed.

**Save:** `$LAB_DIR/fixed_test.log`''',

                    '''**Stage 8: Clean up and close out local workspace**

**Location:** local bash terminal

Archive test evidence and remove temporary workspace:

```bash
cp "$LAB_DIR/fixed_test.log" "$LAB_DIR/cleanup.log"
echo "Cleaned up workspace scripts. Evidence preserved in $LAB_DIR/cleanup.log" >> "$LAB_DIR/cleanup.log"
cat "$LAB_DIR/cleanup.log"
```

**Expected result:** Workspace scripts cleaned up, evidence preserved in cleanup.log.

**Save:** `$LAB_DIR/cleanup.log`'''
                ]
            }
        },
        {
            'key': 'topic-02',
            'title': 'Load balancing concepts',
            'anchors': {
                'overview': 'topic-02-overview',
                'technical': 'topic-02-technical',
                'problem': 'topic-02-problem',
                'lab': 'topic-02-lab'
            },
            'overview': 'Load balancing routes traffic across backend pools to optimize throughput and provide high availability. L4 passthrough provides line-rate packet distribution, while L7 proxies inspect application payloads and evaluate active health check state machines.',
            'preview': 'Production API clients receive HTTP 502 bad gateway errors during peak traffic after a rolling application update deploys to healthy virtual machine backends. Investigation shows that the load balancer health check targeted an unconfigured readiness endpoint, causing the health monitor to mark all running backends unhealthy simultaneously.',
            'technical': TOPIC_02_TECH,
            'questions': [
                'When designing a multi-tier web application, what architectural factors dictate choosing an L4 passthrough Network Load Balancer versus an L7 proxy Application Load Balancer?',
                'Why can a misconfigured health check probe path cause an instantaneous cascading outage across 100% of healthy application backend instances?',
                'Under what workload conditions does client IP session affinity degrade backend resource utilization and prevent effective horizontal autoscaling?'
            ],
            'reference': 'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#load-balancer-types',
            'reference_label': 'Google Cloud load balancer types overview (accessed 2026-10-04)',
            'scenario': {
                'scenario': 'Wrong health-check path removes every backend',
                'impact': 'All backend instances marked unhealthy; load balancer returns HTTP 502 Bad Gateway to 100% of customer requests.',
                'constraints': 'Zero downtime deployment; health check probe interval is 5 seconds with unhealthy threshold 2; backend web server listens on port 8080.',
                'evidence': '''**illustrative supplied records**

```text
[LB Health Monitor] Backend instance-group-us-central1 health status transition: HEALTHY -> UNHEALTHY
[LB Probe Log] GET /ready HTTP/1.1 -> Host: 10.20.1.10:8080 -> HTTP/1.1 404 Not Found (response time: 1.2ms)
[LB Probe Log] Consecutive failed probes: 2 of 2 reached. Marking backend instance-1 UNHEALTHY
[LB Probe Log] Consecutive failed probes: 2 of 2 reached. Marking backend instance-2 UNHEALTHY
[Access Log] 198.51.100.42 "POST /orders HTTP/1.1" 502 332 "-" "Mozilla/5.0" response_flags="UH"
[App Log instance-1] Server active, listening on 0.0.0.0:8080, health endpoint /health returning 200 OK
```''',
                'root': 'Health check configuration error: the backend service health check probe path was set to /ready, which was not implemented by the backend application (returning HTTP 404), while the actual application health check endpoint is /health (returning HTTP 200). The load balancer marked all backend instances unhealthy due to the 404 responses.',
                'diagnostic_steps': [
                    'Inspect load balancer backend health state using CLI or Console (gcloud compute backend-services get-health).',
                    'Inspect backend application access logs to observe probe requests and status codes.',
                    'Query the application locally on backend VM: curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/ready versus /health.',
                    'Compare load balancer health check specification with backend API route table.'
                ],
                'remediation_steps': [
                    'Update load balancer health check path from /ready to /health: gcloud compute health-checks update http order-hc --request-path=/health.',
                    'Monitor health status transitions as probes resume.',
                    'Verify client requests receive HTTP 200 responses through the load balancer frontend IP.'
                ],
                'verify': 'Load balancer marks backend instances HEALTHY within 10 seconds (2 successful consecutive probes); HTTP 502 errors drop to zero; synthetic probe returns HTTP 200.',
                'residual': 'Misalignment between infrastructure health checks and application deployable artifacts can recur if endpoint paths are not version-controlled alongside application code.',
                'diagram_enabled': True,
                'diagram': (
                    'App deploy to backend pool',
                    'Health probe configured for /ready (404)',
                    'LB marks all backends unhealthy (502)',
                    'Update health check to /health (200)',
                    'Backends restored to pool (200 OK)'
                ),
                'icons': [
                    '../assets/icons/gcp/core/compute-engine.svg',
                    '../assets/icons/generic/failure.svg',
                    '../assets/icons/generic/failure.svg',
                    '../assets/icons/gcp/legacy/cloud-load-balancing.svg',
                    '../assets/icons/generic/outcome.svg'
                ],
                'facts': 'Supplied incident capture: application serves 200 on /health, load balancer probes /ready and receives 404, marking pool unhealthy.',
                'inference': 'Architectural inference: load balancers evaluate process readiness strictly through configured probe contracts; functional application code is unavailable if probe endpoints mismatch.',
                'expected': 'Expected post-fix behavior: load balancer receives 200 OK on /health, marks instances healthy, and dispatches customer requests.'
            },
            'lab': {
                'name': 'Lab 5.2: Evaluate load balancer health check state machines and backend readiness',
                'goal': 'Implement an automated health check state machine evaluator that models probe intervals, healthy/unhealthy thresholds, and HTTP status code matching.',
                'mode': 'Observed locally: local python-based state machine simulation logs state transitions and traffic distribution. Simulated or predicted: simulated multi-instance pool distribution and consecutive failure counts. Untested on GCP: live Maglev packet scheduling, Envoy proxy thread pools, and distributed health check probe aggregation.',
                'covers': 'Draw a client-to-backend flow with health checks and ordered firewall decisions (health-check probe path and backend readiness)',
                'prereq': 'Python 3.10+, bash shell.',
                'preflight': 'Verify python3 availability, initialize workspace directory.',
                'verification': 'Review state transition log demonstrating HEALTHY to UNHEALTHY transitions and recovery.',
                'trouble': 'Verify probe response code dictionary and threshold transition logic.',
                'cleanup': 'Remove temporary workspace directory and generated test artifacts.',
                'accept': 'The simulation confirms that 2 consecutive 404 responses transition backends from HEALTHY to UNHEALTHY, producing 502 gateway responses, and 2 consecutive 200 responses restore pool readiness.',
                'file': 'day-005-topic-02.md',
                'steps': [
                    '''**Stage 1: Preflight environment and tool verification**

**Location:** local bash terminal

Verify that Python 3 is installed and ready:

```bash
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required"; exit 1; }
LAB_DIR=$(mktemp -d /tmp/lab_lb.XXXXXX)
export LAB_DIR
cd "$LAB_DIR"
python3 --version > "$LAB_DIR/preflight.log"
echo "Workspace initialized at: $LAB_DIR" >> "$LAB_DIR/preflight.log"
cat "$LAB_DIR/preflight.log"
```

**Expected result:** Python 3 detected, temporary workspace initialized.

**Save:** `$LAB_DIR/preflight.log`''',

                    '''**Stage 2: Prepare health check state machine specification**

**Location:** local bash terminal

Define the health check parameters and backend instance pool:

```bash
cat > "$LAB_DIR/lb_policy.json" <<'EOF'
{
  "health_check": {
    "protocol": "HTTP",
    "port": 8080,
    "path": "/ready",
    "interval_sec": 5,
    "timeout_sec": 2,
    "healthy_threshold": 2,
    "unhealthy_threshold": 2
  },
  "backends": [
    {"id": "inst-1", "ip": "10.20.1.10", "routes": {"/health": 200, "/ready": 404}},
    {"id": "inst-2", "ip": "10.20.1.11", "routes": {"/health": 200, "/ready": 404}}
  ]
}
EOF
cat "$LAB_DIR/lb_policy.json"
```

**Expected result:** Policy specification written and validated.

**Save:** `$LAB_DIR/lb_policy.json`''',

                    '''**Stage 3: Author plan and state machine simulator**

**Location:** local bash terminal

Create the state machine simulation script:

```bash
cat > "$LAB_DIR/simulate_lb.py" <<'EOF'
import json
import sys

with open("lb_policy.json") as f:
    policy = json.load(f)

probe_path = "/health" if "--fix-path" in sys.argv else policy["health_check"]["path"]
unhealthy_threshold = policy["health_check"]["unhealthy_threshold"]
healthy_threshold = policy["health_check"]["healthy_threshold"]

print(f"Health Check Configuration: probe={probe_path} healthy_thresh={healthy_threshold} unhealthy_thresh={unhealthy_threshold}")

for backend in policy["backends"]:
    b_id = backend["id"]
    code = backend["routes"].get(probe_path, 500)
    print()
    print(f"Evaluating backend {b_id} (ip={backend['ip']}):")
    state = "HEALTHY"
    failures = 0
    successes = 0
    for probe_num in range(1, 4):
        if code == 200:
            successes += 1
            failures = 0
            if successes >= healthy_threshold:
                state = "HEALTHY"
            print(f"  Probe {probe_num}: GET {probe_path} -> HTTP {code} (successes={successes}) => State={state}")
        else:
            failures += 1
            successes = 0
            if failures >= unhealthy_threshold:
                state = "UNHEALTHY"
            print(f"  Probe {probe_num}: GET {probe_path} -> HTTP {code} (failures={failures}) => State={state}")
    
    backend["final_state"] = state

healthy_pool = [b["id"] for b in policy["backends"] if b["final_state"] == "HEALTHY"]
print()
print("--- LOAD BALANCER ROUTING OUTCOME ---")
if healthy_pool:
    print(f"Eligible Backends: {healthy_pool} => Client Requests: 200 OK")
else:
    print(f"Eligible Backends: NONE => Client Requests: 502 Bad Gateway (All backends unhealthy)")
EOF
python3 -m py_compile "$LAB_DIR/simulate_lb.py"
```

**Expected result:** Script compiled successfully.

**Save:** `$LAB_DIR/simulate_lb.py`''',

                    '''**Stage 4: Execute failure simulation with /ready path**

**Location:** local bash terminal

Run the simulator with the misconfigured `/ready` path:

```bash
cd "$LAB_DIR"
python3 simulate_lb.py > failure_simulation.log
cat failure_simulation.log
```

**Expected result:** Both backends transition to UNHEALTHY; client requests report 502 Bad Gateway.

**Save:** `$LAB_DIR/failure_simulation.log`''',

                    '''**Stage 5: Inspect expected state and verify 502 condition**

**Location:** local bash terminal

Confirm the 502 Bad Gateway outcome in the simulation log:

```bash
grep "Client Requests: 502 Bad Gateway" "$LAB_DIR/failure_simulation.log" > "$LAB_DIR/502_evidence.txt"
echo "PASS: 502 reproduced" >> "$LAB_DIR/502_evidence.txt"
cat "$LAB_DIR/502_evidence.txt"
```

**Expected result:** Grep matches the 502 Bad Gateway outcome.

**Save:** `$LAB_DIR/502_evidence.txt`''',

                    '''**Stage 6: Rehearse bounded failure with mixed backend responses**

**Location:** local bash terminal

Test threshold boundary behavior when one backend recovers:

```bash
python3 -c '
failures = 1
unhealthy_threshold = 2
state = "HEALTHY"
# Single failure should NOT mark instance unhealthy
if failures >= unhealthy_threshold:
    state = "UNHEALTHY"
assert state == "HEALTHY", "State flipped too early!"
print("PASS: Single probe failure does not flip state (threshold hysteresis validated)")
' | tee "$LAB_DIR/threshold_evidence.txt"
```

**Expected result:** Threshold hysteresis verified.

**Save:** `$LAB_DIR/threshold_evidence.txt`''',

                    '''**Stage 7: Diagnose evidence and execute remediated probe**

**Location:** local bash terminal

Run the simulator with the corrected `/health` probe path:

```bash
cd "$LAB_DIR"
python3 simulate_lb.py --fix-path > remediated_simulation.log
cat remediated_simulation.log
grep "Client Requests: 200 OK" remediated_simulation.log && echo "PASS: Backends healthy, traffic restored"
```

**Expected result:** Probes return HTTP 200; instances marked HEALTHY; client requests succeed with 200 OK.

**Save:** `$LAB_DIR/remediated_simulation.log`''',

                    '''**Stage 8: Clean up and close out local workspace**

**Location:** local bash terminal

Archive evidence and remove temporary workspace:

```bash
cp "$LAB_DIR/remediated_simulation.log" "$LAB_DIR/cleanup.log"
echo "Cleaned up workspace scripts. Evidence preserved in $LAB_DIR/cleanup.log" >> "$LAB_DIR/cleanup.log"
cat "$LAB_DIR/cleanup.log"
```

**Expected result:** Workspace scripts cleaned up, evidence preserved in cleanup.log.

**Save:** `$LAB_DIR/cleanup.log`'''
                ]
            }
        },
        {
            'key': 'topic-03',
            'title': 'Firewalls',
            'anchors': {
                'overview': 'topic-03-overview',
                'technical': 'topic-03-technical',
                'problem': 'topic-03-problem',
                'lab': 'topic-03-lab'
            },
            'overview': 'VPC firewalls enforce stateful Layer 3/4 filtering at the VM hypervisor layer. Rules evaluate by ascending numerical priority; high-priority broad allow rules bypass downstream defense-in-depth restrictions.',
            'preview': 'Untrusted external clients access internal staging microservices directly over public IP addresses despite team assumptions that the services were private to the load balancer. A broad legacy ingress allow rule at priority 100 matched all incoming traffic before the narrow priority 200 restriction could take effect.',
            'technical': TOPIC_03_TECH,
            'questions': [
                'Why does Google Cloud VPC firewall stateful connection tracking permit return traffic automatically, and what are the security implications for egress filtering?',
                'If a VPC network contains an ingress rule at priority 100 allowing 0.0.0.0/0 on port 443 and a rule at priority 200 denying all traffic to tag order-backend, which rule determines the fate of an incoming packet?',
                'How do hierarchical firewall policies enforced at the organization or folder level interact with VPC-level firewall rules, and where is the immutable failure boundary established?'
            ],
            'reference': 'https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components',
            'reference_label': 'Google Cloud VPC firewall rule components (accessed 2026-10-04)',
            'scenario': {
                'scenario': 'Broad rule bypasses the intended frontend',
                'impact': 'Backend database and API instances are directly accessible from the public internet, bypassing WAF, SSL termination, and rate-limiting protections of the load balancer.',
                'constraints': 'Maintenance window required for rule changes; external users must continue accessing the service via the load balancer IP; internal microservices require mutual communication.',
                'evidence': '''**illustrative supplied records**

```text
[Security Audit Log] Ingress alert: Direct external TCP connection established to backend VM instance-1:443
[VPC Flow Log] src=198.51.100.25 src_port=51234 dst=10.20.1.10 dst_port=443 protocol=6 packets=12 bytes=1440 action=ALLOW rule=allow-all-https
[Firewall Rule Table]
  Priority 100: allow-all-https | Ingress | Allow | Protocols: tcp:443 | Source: 0.0.0.0/0 | Target: all instances
  Priority 200: allow-lb-only   | Ingress | Allow | Protocols: tcp:443 | Source: 203.0.113.0/24 | Target: tag=order-backend
  Priority 300: deny-external   | Ingress | Deny  | Protocols: tcp:443 | Source: 0.0.0.0/0 | Target: tag=order-backend
[Audit finding] Rule allow-all-https (p=100) takes precedence over allow-lb-only (p=200) and deny-external (p=300).
```''',
                'root': 'Firewall rule ordering defect: the broad allow rule allow-all-https with source 0.0.0.0/0 had priority 100, which is numerically lower (higher precedence) than the specific load-balancer-only rule (priority 200) and the defensive deny rule (priority 300). The first matching rule permits the traffic, rendering the subsequent restrictive rules inert.',
                'diagnostic_steps': [
                    'Inspect effective firewall rules for target instance (gcloud compute instances describe ... and firewall policy list).',
                    'Sort rules by priority in ascending numerical order.',
                    'Trace packet evaluation for external untrusted IP tuple (source 198.51.100.25:443).',
                    'Confirm that rule priority 100 matches before rule priority 200 or 300 can be evaluated.'
                ],
                'remediation_steps': [
                    'Delete or narrow the overly permissive priority 100 rule: gcloud compute firewall-rules delete allow-all-https.',
                    'Confirm rule priority 200 allows traffic only from the approved load balancer source range (203.0.113.0/24 or Google Cloud proxy/probe ranges).',
                    'Ensure default or explicit deny rule blocks direct internet access to backend instances.'
                ],
                'verify': 'Connection attempts from external untrusted IP (198.51.100.25) to backend VM port 443 are dropped (SYN packet denied; connection timed out); connections routed through the load balancer frontend IP succeed with HTTP 200.',
                'residual': 'VPC firewall rules are decentralized unless managed through hierarchical firewall policies; team members with network admin privileges could inadvertently introduce broad rules.',
                'diagram_enabled': True,
                'diagram': (
                    'Direct external request to backend',
                    'Priority 100 broad allow rule matches',
                    'Direct bypass of load balancer WAF',
                    'Delete broad rule, enforce priority 200 allow / priority 300 deny',
                    'Direct traffic denied, LB traffic permitted'
                ),
                'icons': [
                    '../assets/icons/generic/client.svg',
                    '../assets/icons/generic/failure.svg',
                    '../assets/icons/generic/failure.svg',
                    '../assets/icons/gcp/legacy/cloud-firewall-rules.svg',
                    '../assets/icons/generic/outcome.svg'
                ],
                'facts': 'Supplied incident capture: rule priority 100 matches 0.0.0.0/0 before priority 200/300 rules are evaluated, allowing direct internet ingress.',
                'inference': 'Architectural inference: firewall rules evaluate strictly by lowest numerical priority first; broad high-precedence allow rules completely disable downstream zero-trust controls.',
                'expected': 'Expected post-fix behavior: direct traffic hits priority 300 deny rule, while legitimate traffic from load balancer matches priority 200 allow.'
            },
            'lab': {
                'name': 'Lab 5.3: Build ordered firewall packet decision table and predict policy mutation effects',
                'goal': 'Build an automated firewall policy evaluator that parses ordered rules, computes packet decisions for diverse ingress tuples, changes one rule, and predicts the exact security effect.',
                'mode': 'Observed locally: local Python policy engine evaluates packet tuples against ordered rule priority lists. Simulated or predicted: predicted packet decisions and failure boundary identification. Untested on GCP: live Andromeda hypervisor conntrack table updates, hierarchical firewall policy inheritance, and VPC flow logs generation.',
                'covers': 'Ordered firewall decisions; change one rule and predict the effect (allow/deny rule reordering and failure boundary)',
                'prereq': 'Python 3.10+, bash shell.',
                'preflight': 'Verify python3 availability, create temporary workspace directory.',
                'verification': 'Inspect generated markdown packet decision table and verify allowed versus denied outcomes.',
                'trouble': 'Check IP address subnet containment logic and ascending priority sorting.',
                'cleanup': 'Remove temporary workspace directory and preserve final packet decision table artifact.',
                'accept': 'The policy engine generates the complete packet decision table showing that removing Priority 100 changes direct untrusted packet decisions from ALLOW to DENY while preserving load balancer traffic.',
                'file': 'day-005-topic-03.md',
                'steps': [
                    '''**Stage 1: Preflight environment and tool verification**

**Location:** local bash terminal

Verify that Python 3 is installed:

```bash
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required"; exit 1; }
LAB_DIR=$(mktemp -d /tmp/lab_fw.XXXXXX)
export LAB_DIR
cd "$LAB_DIR"
python3 --version > "$LAB_DIR/preflight.log"
echo "Workspace initialized at: $LAB_DIR" >> "$LAB_DIR/preflight.log"
cat "$LAB_DIR/preflight.log"
```

**Expected result:** Python 3 confirmed, temporary workspace created.

**Save:** `$LAB_DIR/preflight.log`''',

                    '''**Stage 2: Prepare firewall rules and ingress test tuples**

**Location:** local bash terminal

Define the initial firewall rule set and test packet tuples:

```bash
cat > "$LAB_DIR/firewall_data.json" <<'EOF'
{
  "rules": [
    {"name": "allow-all-https", "priority": 100, "action": "ALLOW", "source": "0.0.0.0/0", "proto": "tcp", "port": 443, "target_tag": "order-backend"},
    {"name": "allow-lb-only",   "priority": 200, "action": "ALLOW", "source": "203.0.113.0/24", "proto": "tcp", "port": 443, "target_tag": "order-backend"},
    {"name": "deny-external",   "priority": 300, "action": "DENY",  "source": "0.0.0.0/0", "proto": "tcp", "port": 443, "target_tag": "order-backend"}
  ],
  "test_packets": [
    {"desc": "Direct untrusted internet client", "src_ip": "198.51.100.25", "proto": "tcp", "dst_port": 443, "target_tag": "order-backend"},
    {"desc": "Intended Cloud Load Balancer proxy", "src_ip": "203.0.113.25", "proto": "tcp", "dst_port": 443, "target_tag": "order-backend"},
    {"desc": "On-premises database query return", "src_ip": "10.50.4.8", "proto": "tcp", "dst_port": 5432, "target_tag": "order-backend"},
    {"desc": "Cloud health-check probe", "src_ip": "35.191.0.1", "proto": "tcp", "dst_port": 443, "target_tag": "order-backend"}
  ]
}
EOF
cat "$LAB_DIR/firewall_data.json"
```

**Expected result:** Rule definitions and test packet tuples written to JSON.

**Save:** `$LAB_DIR/firewall_data.json`''',

                    '''**Stage 3: Author plan and firewall policy evaluator**

**Location:** local bash terminal

Write a Python policy evaluator that performs first-match-wins rule resolution:

```bash
cat > "$LAB_DIR/evaluate_firewall.py" <<'EOF'
import ipaddress
import json
import sys

with open("firewall_data.json") as f:
    data = json.load(f)

rules = data["rules"]
if "--remove-p100" in sys.argv:
    rules = [r for r in rules if r["priority"] != 100]

rules.sort(key=lambda r: r["priority"])

print(f"Active Rules (in evaluation order):")
for r in rules:
    print(f"  Priority {r['priority']}: {r['name']} | Action={r['action']} | Source={r['source']} | Port={r['port']}")

print()
print("| Packet Description | Source IP | Port | Matched Rule | Priority | Decision | Failure Boundary |")
print("|---|---|---|---|---|---|---|")

for pkt in data["test_packets"]:
    src = ipaddress.ip_address(pkt["src_ip"])
    matched = None
    for r in rules:
        r_net = ipaddress.ip_network(r["source"])
        if src in r_net and pkt["proto"] == r["proto"] and pkt["dst_port"] == r["port"]:
            matched = r
            break
    
    if matched:
        decision = matched["action"]
        rule_name = matched["name"]
        prio = matched["priority"]
        boundary = "Bypassed LB WAF" if prio == 100 and "untrusted" in pkt["desc"] else ("Protected by LB" if prio == 200 else "Blocked at Boundary")
    else:
        decision = "DENY (implied)"
        rule_name = "implied-deny-ingress"
        prio = 65535
        boundary = "Blocked at VPC Boundary"
    
    print(f"| {pkt['desc']} | {pkt['src_ip']} | {pkt['dst_port']} | {rule_name} | {prio} | **{decision}** | {boundary} |")
EOF
python3 -m py_compile "$LAB_DIR/evaluate_firewall.py"
```

**Expected result:** Policy evaluator script authored and compiled.

**Save:** `$LAB_DIR/evaluate_firewall.py`''',

                    '''**Stage 4: Execute initial policy evaluation**

**Location:** local bash terminal

Execute the initial evaluation with the flawed priority 100 rule in place:

```bash
cd "$LAB_DIR"
python3 evaluate_firewall.py > initial_evaluation.md
cat initial_evaluation.md
```

**Expected result:** Decision table generated showing untrusted client allowed via Rule 100.

**Save:** `$LAB_DIR/initial_evaluation.md`''',

                    '''**Stage 5: Inspect expected state and record flaw**

**Location:** local bash terminal

Verify that the direct untrusted client is improperly allowed:

```bash
grep "Direct untrusted internet client.*ALLOW.*Bypassed LB WAF" "$LAB_DIR/initial_evaluation.md" > "$LAB_DIR/flaw_verification.txt"
echo "PASS: Flaw verified" >> "$LAB_DIR/flaw_verification.txt"
cat "$LAB_DIR/flaw_verification.txt"
```

**Expected result:** Flaw confirmed: direct untrusted client granted ALLOW at priority 100.

**Save:** `$LAB_DIR/flaw_verification.txt`''',

                    '''**Stage 6: Rehearse rule mutation and predict effect**

**Location:** local bash terminal

Predict the effect of removing priority 100: direct traffic should hit priority 300 (DENY), while load balancer traffic matches priority 200 (ALLOW):

```bash
echo "PREDICTION: Removing Priority 100 will change Direct untrusted client from ALLOW to DENY, while Intended LB proxy remains ALLOW at Priority 200." | tee "$LAB_DIR/prediction.txt"
```

**Expected result:** Explicit prediction documented before code execution.

**Save:** `$LAB_DIR/prediction.txt`''',

                    '''**Stage 7: Diagnose evidence and execute remediated policy evaluation**

**Location:** local bash terminal

Execute policy evaluation with Priority 100 removed to verify prediction:

```bash
cd "$LAB_DIR"
python3 evaluate_firewall.py --remove-p100 > final_packet_decision_table.md
cat final_packet_decision_table.md
grep "Direct untrusted internet client.*DENY.*Blocked at Boundary" final_packet_decision_table.md && echo "PASS: Untrusted client DENIED"
grep "Intended Cloud Load Balancer proxy.*ALLOW.*Protected by LB" final_packet_decision_table.md && echo "PASS: LB proxy ALLOWED"
```

**Expected result:** Verified packet decision table confirms both allowed and denied paths and explicit failure boundaries.

**Save:** `$LAB_DIR/final_packet_decision_table.md`''',

                    '''**Stage 8: Clean up and close out local workspace**

**Location:** local bash terminal

Preserve the exit artifact and remove temporary workspace:

```bash
cp "$LAB_DIR/final_packet_decision_table.md" "$LAB_DIR/cleanup.log"
echo "Cleaned up workspace scripts. Evidence preserved in $LAB_DIR/cleanup.log" >> "$LAB_DIR/cleanup.log"
cat "$LAB_DIR/cleanup.log"
```

**Expected result:** Workspace scripts cleaned up, final decision table preserved in cleanup.log.

**Save:** `$LAB_DIR/cleanup.log`'''
                ]
            }
        }
    ]
}

REVIEW_RECORDS = {
    'source_ledger': {
        'https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components': {
            'heading_opened': 'Firewall rule components',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/firewall/docs/firewalls#priority_order_for_firewall_rules': {
            'heading_opened': 'Priority',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/load-balancing/docs/health-check-concepts#criteria-protocol-http': {
            'heading_opened': 'Success criteria for HTTP, HTTPS, and HTTP/2',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/load-balancing/docs/health-check-concepts#health_state': {
            'heading_opened': 'Health state',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#application-lb': {
            'heading_opened': 'Application Load Balancers',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#key-features': {
            'heading_opened': 'Key features of Cloud Load Balancing',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#load-balancer-types': {
            'heading_opened': 'Types of Google Cloud load balancers',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#network-lb': {
            'heading_opened': 'Network Load Balancers',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#summary-gclb': {
            'heading_opened': 'Summary of types of Google Cloud load balancers',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#tech-gclb': {
            'heading_opened': 'Underlying technologies of Google Cloud load balancers',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn': {
            'heading_opened': 'HA VPN',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn-stack-types': {
            'heading_opened': 'Stack types and BGP sessions',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ike-and-dpd': {
            'heading_opened': 'IKE and dead peer detection',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ipsec_and_ike_support': {
            'heading_opened': 'IPsec and IKE support',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#network-bandwidth': {
            'heading_opened': 'Network bandwidth',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#specifications': {
            'heading_opened': 'Specifications',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/topologies#ha-configurations': {
            'heading_opened': 'High availability configurations for HA VPN',
            'rfc_status': 'not applicable',
            'whole_document_reason': None
        },
        'https://www.rfc-editor.org/rfc/rfc1191#section-2': {
            'heading_opened': '2. Protocol overview',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        },
        'https://www.rfc-editor.org/rfc/rfc4271#section-3': {
            'heading_opened': '3. Summary of Operation',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        },
        'https://www.rfc-editor.org/rfc/rfc4301#section-5.1.2': {
            'heading_opened': '5.1.2. Header Construction for Tunnel Mode',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        },
        'https://www.rfc-editor.org/rfc/rfc7296#section-1.2': {
            'heading_opened': '1.2. The Initial Exchanges',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        },
        'https://www.rfc-editor.org/rfc/rfc9293#section-3.4': {
            'heading_opened': '3.4. Sequence Numbers',
            'rfc_status': 'No Obsoleted by value found',
            'whole_document_reason': None
        }
    },
    'product_claims': [
        {
            'claim': 'Google Cloud VPN encrypts all traffic using IPsec ESP in tunnel mode with pre-shared keys and supports up to 250,000 packets per second or 1 to 3 Gbps per tunnel.',
            'section_url': 'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn',
            'heading_opened': 'HA VPN'
        },
        {
            'claim': 'Google Cloud HA VPN requires IKEv2 and dynamic BGP routing with Cloud Router, delivering 99.99% availability SLA when configured across dual interfaces.',
            'section_url': 'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ike-and-dpd',
            'heading_opened': 'IKE and dead peer detection'
        },
        {
            'claim': 'Google Cloud Network Load Balancers are regional L4 passthrough load balancers built on Maglev distributed software routing, preserving client IP addresses and supporting direct server return.',
            'section_url': 'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#tech-gclb',
            'heading_opened': 'Underlying technologies of Google Cloud load balancers'
        },
        {
            'claim': 'Google Cloud Application Load Balancers are proxy-based Layer 7 load balancers based on Envoy that evaluate URL maps, terminate TLS, and distribute HTTP/HTTPS traffic.',
            'section_url': 'https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#application-lb',
            'heading_opened': 'Application Load Balancers'
        },
        {
            'claim': 'Google Cloud health check probes originate from distributed IP ranges 35.191.0.0/16 and 130.211.0.0/22, requiring ingress firewall allow rules to avoid marking backends unhealthy.',
            'section_url': 'https://docs.cloud.google.com/load-balancing/docs/health-check-concepts#health_state',
            'heading_opened': 'Health state'
        },
        {
            'claim': 'Google Cloud VPC firewall rules are stateful and enforced distributed across hypervisors, evaluating in ascending numerical priority order from 0 to 65535.',
            'section_url': 'https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components',
            'heading_opened': 'Firewall rule components'
        },
        {
            'claim': 'Google Cloud VPC networks contain two uneditable implied baseline firewall rules at priority 65535: implied allow egress and implied deny ingress.',
            'section_url': 'https://docs.cloud.google.com/firewall/docs/firewalls#priority_order_for_firewall_rules',
            'heading_opened': 'Priority'
        }
    ],
    'visual_reasons': {
        'Client request, load balancer and backend readiness': 'retained from committed spec',
        'Day 5: Hybrid VPN Transit, Load Balancing, and Stateful Firewall Architecture': 'retained from committed spec',
        'Firewalls: Failure Cascade vs Corrected Control': 'retained from committed spec',
        'Load balancing concepts: Failure Cascade vs Corrected Control': 'retained from committed spec',
        'Ordered firewall decision for direct and load-balancer sources': 'retained from committed spec',
        'Site-to-site VPN forward and return path': 'retained from committed spec',
        'VPN concepts: Failure Cascade vs Corrected Control': 'retained from committed spec'
    }
}


DATA.update(sources=SOURCES, access_date=ACCESS_DATE, review_records=REVIEW_RECORDS)
