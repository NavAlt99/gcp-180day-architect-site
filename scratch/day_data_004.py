"""day_data_004.py — Specification for Day 4: TLS, HTTP, MTU and routing vocabulary.

Topics:
1. topic-01: HTTP/HTTPS, status codes, HTTP/1.1 vs HTTP/2 vs HTTP/3
2. topic-02: TLS 1.3 handshake and certificate validation chains
3. topic-03: MTU and MSS clamping
4. topic-04: NAT (SNAT/DNAT) for private outbound
5. topic-05: Routing basics
"""

import sys
import re
from pathlib import Path
from functools import partial

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scratch.day_helpers import (
    escape, dedent, keyword, subtopic as _subtopic, source as _source,
    discussion, flow_svg as _flow_svg, stage as _stage, workspace as _workspace,
    write_file, lab as _lab, case as _case
)

DAY = 4
ACCESS_DATE = '2026-10-04'
WORK_BLOCK = "Days 1–17 — Foundations"
EXIT_SUMMARY = "A failure worksheet that separates TLS trust, packet size, routing and HTTP errors."

SOURCES = {
    'rfc9110': ('RFC 9110: HTTP Semantics — Status Codes (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc9110.html#section-15'),
    'rfc9113': ('RFC 9113: HTTP/2 Framing and Multiplexing — Field Validity (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc9113.html#section-8.2.1'),
    'rfc9114': ('RFC 9114: HTTP/3 over QUIC — Connection Setup and Management (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc9114.html#section-3'),
    'gcp_https_lb': ('Google Cloud HTTP(S) Load Balancing — HTTP/2 over TLS (accessed 2026-10-04)', 'https://docs.cloud.google.com/load-balancing/docs/https#http2-over-tls'),
    'rfc8446': ('RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3 — Handshake Protocol (historical; obsoleted by RFC 9846) (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc8446.html#section-4'),
    'rfc5280': ('RFC 5280: Internet X.509 PKI Certificate and CRL Profile — Certification Path Validation (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc5280.html#section-6'),
    'gcp_cert_mgr': ('Google Cloud Certificate Manager Overview — Supported TLS certificates (accessed 2026-10-04)', 'https://docs.cloud.google.com/certificate-manager/docs/overview#supported-certificates'),
    'rfc1191': ('RFC 1191: Path MTU Discovery — Protocol overview (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc1191.html#section-2'),
    'rfc9293': ('RFC 9293: Transmission Control Protocol (TCP) — Maximum Segment Size Option (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc9293.html#section-3.7.1'),
    'gcp_vpc_mtu': ('Google Cloud VPC Maximum Transmission Unit (MTU) Settings — Valid VPC network MTU sizes (accessed 2026-10-04)', 'https://docs.cloud.google.com/vpc/docs/mtu#valid_mtus'),
    'rfc3022': ('RFC 3022: Traditional IP Network Address Translator (Traditional NAT) — Overview of traditional NAT (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc3022.html#section-2'),
    'rfc1918': ('RFC 1918: Address Allocation for Private Internets — Private Address Space (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc1918.html#section-3'),
    'gcp_cloud_nat': ('Google Cloud NAT Overview — Architecture (accessed 2026-10-04)', 'https://docs.cloud.google.com/nat/docs/overview#architecture'),
    'rfc4271': ('RFC 4271: A Border Gateway Protocol 4 (BGP-4) — Summary of Operation (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc4271.html#section-3'),
    'gcp_vpc_routes': ('Google Cloud VPC Routes Overview — Routing order (accessed 2026-10-04)', 'https://docs.cloud.google.com/vpc/docs/routes#routeselection'),
    'gcp_cloud_router': ('Google Cloud Cloud Router Overview — Key features (accessed 2026-10-04)', 'https://docs.cloud.google.com/network-connectivity/docs/router/concepts/overview#key'),
}

SOURCES['rfc9525'] = ('RFC 9525 — Verifying Service Identity (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc9525.html#section-6')
SOURCES['gcp_nat_benefits'] = ('Cloud NAT — Benefits (accessed 2026-10-04)', 'https://docs.cloud.google.com/nat/docs/overview#benefits')
SOURCES['gcp_cert_benefits'] = ('Certificate Manager — Benefits (accessed 2026-10-04)', 'https://docs.cloud.google.com/certificate-manager/docs/overview#benefits')
SOURCES['gcp_lb_backends'] = ('Application Load Balancer — Backend services (accessed 2026-10-04)', 'https://docs.cloud.google.com/load-balancing/docs/https#backend-service')
SOURCES['gcp_lb_http3'] = ('Application Load Balancer — How HTTP/3 is negotiated (accessed 2026-10-04)', 'https://docs.cloud.google.com/load-balancing/docs/https#http3-negotiation')
SOURCES['gcp_vpn_mtu'] = ('VPC MTU — Communication through Cloud VPN tunnels (accessed 2026-10-04)', 'https://docs.cloud.google.com/vpc/docs/mtu#through-cloud-vpn')
SOURCES['rfc9110_https'] = ('RFC 9110 — https URI Scheme (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc9110.html#section-4.2.2')
SOURCES['rfc9113_setup'] = ('RFC 9113 — Starting HTTP/2 for https URIs (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc9113.html#section-3.2')
SOURCES['rfc9114_requests'] = ('RFC 9114 — Expressing HTTP Semantics in HTTP/3 (accessed 2026-10-04)', 'https://www.rfc-editor.org/rfc/rfc9114.html#section-4')
SOURCES['gcp_lb_timeouts'] = ('External Application Load Balancers — Timeouts and retries (accessed 2026-10-04)', 'https://docs.cloud.google.com/load-balancing/docs/https/request-distribution#timeouts_and_retries')
SOURCES['gcp_nat_ports'] = ('Cloud NAT — Ports (accessed 2026-10-04)', 'https://docs.cloud.google.com/nat/docs/ports-and-addresses#ports')
SOURCES['gcp_nat_dynamic'] = ('Cloud NAT — Dynamic port allocation (accessed 2026-10-04)', 'https://docs.cloud.google.com/nat/docs/ports-and-addresses#dynamic-port')
SOURCES['gcp_nat_mapping'] = ('Cloud NAT — Simultaneous port reuse and endpoint-independent mapping (accessed 2026-10-04)', 'https://docs.cloud.google.com/nat/docs/ports-and-addresses#ports-reuse-endpoints')
SOURCES['gcp_nat_logs'] = ('Cloud NAT — Logging (accessed 2026-10-04)', 'https://docs.cloud.google.com/nat/docs/monitoring#logging')
SOURCES['gcp_nat_metrics'] = ('Cloud NAT — VM instance metrics (accessed 2026-10-04)', 'https://docs.cloud.google.com/nat/docs/monitoring#vm-metrics')
SOURCES['gcp_nat_gateway_metrics'] = ('Cloud NAT — NAT gateway metrics (accessed 2026-10-04)', 'https://docs.cloud.google.com/nat/docs/monitoring#gateway-metrics')
SOURCES['gcp_routing_mode'] = ('Cloud Router — Dynamic routing mode (accessed 2026-10-04)', 'https://docs.cloud.google.com/network-connectivity/docs/router/concepts/learned-routes#dynamic-routing-mode')
SOURCES['gcp_vpn_payload'] = ('Cloud VPN — Cloud VPN payload MTU values (accessed 2026-10-04)', 'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/mtu-considerations#cloud-vpn-payload-mtu-values')
SOURCES['gcp_route_types'] = ('VPC — Route types (accessed 2026-10-04)', 'https://docs.cloud.google.com/vpc/docs/routes#types_of_routes')
SOURCES['gcp_mtu_apis'] = ('VPC MTU — Communication to Google APIs and services (accessed 2026-10-04)', 'https://docs.cloud.google.com/vpc/docs/mtu#to-cloudpath')
source = partial(_source, sources=SOURCES)
def subtopic(*args):
    return _subtopic(*args, sources=SOURCES, access_date=ACCESS_DATE).replace(f'. Accessed {ACCESS_DATE}.', '.')
def flow_svg(*args):
    return _flow_svg(*args).replace('../assets/icons/generic/../gcp/', '../assets/icons/gcp/')

stage = partial(_stage, location='Local Linux Bash terminal / text editor.')
def workspace(prefix, *, preflight_text):
    tools = ['python3', 'bash', 'mktemp', 'cat', 'grep', 'head', 'rm', 'sleep', 'kill']
    tools += {'http_lab': ['curl'], 'pki_lab': ['openssl'], 'mtu_lab': ['ip'], 'routing_lab': ['ip']}.get(prefix, [])
    checks = ''.join(f'command -v {tool}\n' for tool in tools)
    if prefix == 'mtu_lab':
        checks += 'command -v ping || echo "ping not installed; skip this stage"\n'
    commands = 'set -euo pipefail\n' + checks + _workspace(prefix, preflight_text=preflight_text).replace('preflight.txt', 'preflight.log')
    commands += {'http_lab': 'curl --version >> preflight.log\n',
                 'pki_lab': 'openssl version >> preflight.log\nopenssl list -public-key-algorithms > openssl-algorithms.log\n',
                 'mtu_lab': 'ip link show >> preflight.log\n',
                 'routing_lab': 'ip route show >> preflight.log\n'}.get(prefix, '')
    return commands
case = partial(_case, evidence_label='Supplied illustrative records (literal fixture, not production observation):')

LAB_CONTEXT = {
    'mode': 'Observed locally: Python scripts and any commands actually executed. Simulated or predicted: supplied fixtures and protocol models, including HTTP/2 and HTTP/3. Untested on GCP: all deployments, provider performance and service behavior.',
    'prereq': 'Day 3 workspace/evidence repository; local Linux Bash, Python 3 standard library, OpenSSL, curl, text editor',
    'preflight': 'Run all eight stages in order in the same terminal. Stage 1 creates a unique workspace. Stop immediately on unexpected failure or unverified assumptions; cloud steps represent architectural documentation evaluation.',
    'verification': 'Verify that each stage generates its specified log or configuration file with non-empty content and observable expected outcomes.',
    'trouble': 'If a port collision occurs during local server execution, select an alternate unprivileged port (e.g. 8443 or 9090) and update test scripts accordingly.',
    'cleanup': 'All temporary files, self-signed certificates, and background test processes must be removed; preserve only the final structured evidence artifacts.',
}

def make_lab(name, goal, expected, steps, accept, trouble, file_name, covers):
    result = _lab(
        name=name,
        goal=goal,
        expected=expected,
        steps=steps,
        accept=accept,
        trouble=trouble,
        files=file_name,
        defaults=LAB_CONTEXT
    )
    result["covers"] = covers
    return result

PART1_INTRO = (
    "Day 4 bridges lower-level network addressing and transport state to application delivery and security boundaries. "
    "Cloud architects must disentangle failure signals that manifest identically at the user boundary but originate in distinct layers: "
    "an application runtime returning an HTTP error, a cryptographic trust failure aborting a TLS handshake, an intermediate MTU restriction "
    "silently dropping oversized packets with the Don't Fragment bit set, a stateful NAT gateway exhausting ephemeral source ports, or an "
    "asymmetric BGP route causing packet drops at perimeter firewalls. Today establishes the precise mechanisms, protocol framing, "
    "and diagnostic sequences needed to isolate these five critical failure domains."
)

PART1_HTML = """
<p class="intro">Day 4 establishes the fundamental vocabulary, framing mechanisms, and failure boundaries spanning application protocols (HTTP/1.1, HTTP/2, HTTP/3), cryptographic trust chains (TLS 1.3), network framing (MTU and MSS clamping), address translation (SNAT/DNAT), and dynamic routing (BGP).</p>
<p class="callout"><strong>Exit evidence:</strong> A failure worksheet that separates TLS trust, packet size, routing and HTTP errors.</p>

<article class="topic-card overview" id="topic-01-overview">
<h3>1. HTTP/HTTPS, status codes, HTTP/1.1 vs HTTP/2 vs HTTP/3</h3>
<p><strong class="keyword">Hypertext Transfer Protocol</strong> (HTTP, RFC 9110) governs application-layer request and response semantics across the internet, operating in cleartext or over cryptographic TLS tunnels as <strong class="keyword">HTTPS</strong>. Protocol evolution from HTTP/1.1 plaintext pipelining to HTTP/2 binary multiplexing (RFC 9113) and HTTP/3 UDP-based QUIC transport (RFC 9114) addresses fundamental head-of-line blocking bottlenecks, reshaping cloud edge caching and API gateway architectures.</p>
<p><strong class="side-heading">Why today:</strong> Day 4 connects Day 3 transport sockets to user-facing application protocol semantics and error classifications.</p>
<p><strong class="side-heading">Where it sits:</strong> Terminated at Google Cloud external Application Load Balancers, Cloud CDN edge points of presence, and API gateways.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> An internal API gateway upgrading from HTTP/1.1 to HTTP/2 encounters 502 Bad Gateway responses on backend requests containing unvalidated uppercase HTTP header field names. The upstream Envoy ingress proxies drop the malformed streams due to strict HTTP/2 RFC 9113 header normalization rules, causing catalog lookup outages across regional store frontends.</p>
<p><a href="#topic-01-technical">Technical discussion →</a> <a href="#topic-01-problem">Real-world problem →</a> <a href="#topic-01-lab">Step-by-step lab →</a></p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>2. TLS 1.3 handshake and certificate validation chains</h3>
<p><strong class="keyword">Transport Layer Security</strong> (TLS 1.3, RFC 8446) establishes authenticated, confidential communication channels using ephemeral Diffie-Hellman key exchange and X.509 public key infrastructure (PKI, RFC 5280). Strict cryptographic trust chains validate that leaf certificates descend from trusted Certificate Authorities, while modern hostname verification enforces Subject Alternative Names over deprecated Common Name attributes.</p>
<p><strong class="side-heading">Why today:</strong> Cryptographic verification must precede application payload delivery, preventing eavesdropping and man-in-the-middle attacks.</p>
<p><strong class="side-heading">Where it sits:</strong> TLS terminates at supported Google Cloud load balancers; Certificate Manager manages their certificates rather than terminating traffic. Cloud Service Mesh mTLS sidecars are separate context not established by the cited Certificate Manager sections.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A newly deployed microservice client reports SSL peer certificate verification failures when connecting to an internal analytics endpoint via its private DNS alias. The leaf certificate only contains the legacy Common Name for the physical host rather than a Subject Alternative Name for the service alias, causing TLS handshakes to abort immediately and halting data synchronization pipelines.</p>
<p><a href="#topic-02-technical">Technical discussion →</a> <a href="#topic-02-problem">Real-world problem →</a> <a href="#topic-02-lab">Step-by-step lab →</a></p>
</article>

<article class="topic-card overview" id="topic-03-overview">
<h3>3. MTU and MSS clamping</h3>
<p><strong class="keyword">Maximum Transmission Unit</strong> (MTU) defines the largest physical or link-layer frame size that can traverse a network segment without fragmentation, while <strong class="keyword">Maximum Segment Size</strong> (MSS) dictates the maximum unfragmented TCP payload permitted within that boundary. When intermediate tunneling protocols (IPSec, GRE, Geneve) introduce encapsulation overhead, Path MTU Discovery (PMTUD, RFC 1191) and TCP MSS clamping prevent devastating silent packet drops caused by MTU black holes.</p>
<p><strong class="side-heading">Why today:</strong> Encapsulation overheads in hybrid cloud VPNs and cross-region VPC links frequently trigger silent packet drops on large payloads while small health checks succeed.</p>
<p><strong class="side-heading">Where it sits:</strong> Configured on Google Cloud VPC networks (1460, 1500, or 8896 jumbo MTU), Cloud VPN gateways, and Cloud Interconnect circuits.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> An application transferring large JSON batch payloads across an IPSec VPN tunnel experiences hanging connections and connection resets while small health checks pass continuously. An intermediate router with a 1400-byte MTU drops oversized packets with the Don't Fragment bit set while a misconfigured firewall blocks ICMP Type 3 Code 4 feedback messages, creating a Path MTU black hole that stalls batch database replication.</p>
<p><a href="#topic-03-technical">Technical discussion →</a> <a href="#topic-03-problem">Real-world problem →</a> <a href="#topic-03-lab">Step-by-step lab →</a></p>
</article>

<article class="topic-card overview" id="topic-04-overview">
<h3>4. NAT (SNAT/DNAT) for private outbound</h3>
<p><strong class="keyword">Network Address Translation</strong> (NAT, RFC 3022) modifies IP address and port information in packet headers during transit, enabling private IPv4 workloads to access external resources without exposing public IP addresses. Source NAT (<strong class="keyword">SNAT</strong>) translates outbound client addresses, while Destination NAT (<strong class="keyword">DNAT</strong>) maps inbound flows; managed cloud NAT gateways track 5-tuple connection states to multiplex thousands of VMs across a pool of public IPs.</p>
<p><strong class="side-heading">Why today:</strong> Secure enterprise design requires keeping compute instances private while providing reliable, bounded outbound access to public APIs and patch mirrors.</p>
<p><strong class="side-heading">Where it sits:</strong> Provided by Google Cloud NAT attached to Cloud Router, implemented as distributed software-defined translation by Andromeda; the cited Architecture section does not identify a virtual-switch implementation.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A cluster of backend worker VMs performing external webhook callbacks exhausts its Cloud NAT source port allocation during a marketing campaign blast. With minimum ports per VM set statically to 64 and dynamic port allocation disabled, outgoing TCP SYNs are dropped due to NAT port exhaustion, resulting in connection timeouts and backlogged customer notification queues.</p>
<p><a href="#topic-04-technical">Technical discussion →</a> <a href="#topic-04-problem">Real-world problem →</a> <a href="#topic-04-lab">Step-by-step lab →</a></p>
</article>

<article class="topic-card overview" id="topic-05-overview">
<h3>5. Routing basics</h3>
<p><strong class="keyword">Routing</strong> governs how network forwarders determine the optimal multi-hop path for IP packets across complex topologies, evaluating Forwarding Information Bases (FIB) using Longest Prefix Match (LPM) algorithms. While static routing relies on fixed manual path configurations, dynamic routing employs the <strong class="keyword">Border Gateway Protocol</strong> (BGP-4, RFC 4271) to autonomously exchange path-vector reachability, metrics, and autonomous system paths across hybrid interconnects.</p>
<p><strong class="side-heading">Why today:</strong> Concludes Day 4 by examining the path selection and control-plane protocols that steer enterprise traffic across hybrid interconnects and multi-region clouds.</p>
<p><strong class="side-heading">Where it sits:</strong> Configured in Google Cloud VPC route tables (system-generated, custom static, and dynamic routes) and managed via Cloud Router BGP peering.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> Traffic destined for an on-premises enterprise network from a GCP VPC is routed through an unexpected secondary interconnect link with high latency instead of the primary high-speed link. The on-premises edge router advertised identical BGP prefixes over both sessions without configuring MED attributes or AS-path prepending, creating an illustrative equal-cost path-selection case whose actual behavior depends on route selection mode and policy and degrade transactional database replication.</p>
<p><a href="#topic-05-technical">Technical discussion →</a> <a href="#topic-05-problem">Real-world problem →</a> <a href="#topic-05-lab">Step-by-step lab →</a></p>
</article>
"""

PART2_INTRO = (
    "In-depth technical analysis of application and transport layer protocols: HTTP semantic taxonomy and multi-version framing, "
    "TLS 1.3 cryptographic handshakes and X.509 PKI trust chains, Path MTU Discovery and TCP MSS clamping, "
    "Source and Destination NAT state table mechanics, and static versus dynamic BGP routing architectures."
)

PART3_INTRO = (
    "Rigorous architectural incident investigations examining realistic enterprise networking failures: "
    "HTTP/2 header normalization stream resets, TLS leaf certificate Subject Alternative Name omissions, "
    "ICMP-filtered Path MTU black holes, Cloud NAT ephemeral port exhaustion under burst traffic, and BGP asymmetric path routing degradation."
)

PART4_INTRO = (
    "Hands-on executable laboratories providing step-by-step execution across eight explicit stages: "
    "HTTP multi-version protocol analysis, OpenSSL PKI validation chain construction, MTU and MSS clamping calculations, "
    "SNAT 5-tuple state table simulation, and routing table evaluation culminating in the canonical Day 4 failure worksheet."
)

ARCH_TABLE_HTML = """
<table class="comparison-table">
<caption>Architectural comparison: Network protocol layers, encapsulated protocol data units, failure modes, and Google Cloud boundary controls</caption>
<thead>
<tr>
  <th scope="col">Protocol Domain</th>
  <th scope="col">Encapsulated PDU &amp; Identifiers</th>
  <th scope="col">Control &amp; Data Plane Mechanics</th>
  <th scope="col">Observable Failure Signal</th>
  <th scope="col">Google Cloud Control &amp; Architectural Boundary</th>
</tr>
</thead>
<tbody>
<tr>
  <td><strong>Application Layer (HTTP/HTTPS)</strong></td>
  <td>HTTP request/response messages, binary frames (HTTP/2), QUIC packets (HTTP/3), status codes (1xx–5xx)</td>
  <td>End-to-end stream multiplexing, header compression (HPACK/QPACK), connection reuse, keep-alive timers</td>
  <td>HTTP 502 Bad Gateway (upstream proxy parse error), HTTP 504 Gateway Timeout, connection reset on unnormalized headers</td>
  <td>Cloud Load Balancing (External Application Load Balancer), Cloud CDN, Google Cloud Armor security policies</td>
</tr>
<tr>
  <td><strong>Cryptographic Security (TLS 1.3)</strong></td>
  <td>TLS Record Layer, Handshake messages, X.509 digital certificates, Public/Private key pairs</td>
  <td>1-RTT ephemeral Diffie-Hellman key exchange, symmetric AEAD encryption, PKI hierarchical trust validation</td>
  <td>SSL handshake failure, Hostname mismatch error, Unknown CA certificate authority, expired certificate alert</td>
  <td>Certificate Manager, Google-managed SSL certificates, SSL policies restricting minimum TLS version and ciphers</td>
</tr>
<tr>
  <td><strong>Transport Framing (MTU / MSS)</strong></td>
  <td>IP packets (MTU boundary: 1460B/1500B), TCP segments (MSS: 1420B/1460B), ICMP control messages</td>
  <td>Path MTU Discovery (PMTUD), TCP MSS negotiation during 3-way handshake, SYN packet MSS clamping</td>
  <td>Path MTU black hole (small pings pass, large data hangs), packet drop on DF=1, ICMP Type 3 Code 4 dropped</td>
  <td>VPC network MTU configuration (1460, 1500, 8896 jumbo), Cloud VPN gateway/payload MTU distinction, MSS clamping at gateways</td>
</tr>
<tr>
  <td><strong>Egress Translation (NAT / SNAT)</strong></td>
  <td>IP 5-tuple state table entries: (Src IP, Src Port, Dst IP, Dst Port, Protocol)</td>
  <td>Source IP/Port translation for private instances, stateful connection tracking, return destination reverse translation</td>
  <td>NAT source port exhaustion, OUT_OF_RESOURCES connection drops, SYN retransmission timeout to external APIs</td>
  <td>Cloud NAT gateway attached to Cloud Router, Andromeda software-defined translation; configurable port allocation</td>
</tr>
<tr>
  <td><strong>Network Routing (BGP / LPM)</strong></td>
  <td>Routing Information Base (RIB), Forwarding Information Base (FIB), IP prefixes / CIDR blocks</td>
  <td>Longest Prefix Match (LPM), route priority metrics, eBGP/iBGP path vector exchange (AS_PATH, MED, Local Pref)</td>
  <td>Asymmetric routing drops at stateful firewalls, suboptimal high-latency path selection, black-holed route loops</td>
  <td>Cloud Router BGP peering, VPC route tables (system, custom static, dynamic), Cloud Interconnect / HA VPN</td>
</tr>
</tbody>
</table>
"""

ARCH_DIAGRAM = {}
ARCH_SVG_HTML = ''

# ==============================================================================
# TOPIC 01: HTTP/HTTPS, status codes, HTTP/1.1 vs HTTP/2 vs HTTP/3
# ==============================================================================
T1_SUBTOPICS = [
    subtopic(
        "HTTP Request/Response Semantics and Status Code Taxonomy (RFC 9110)",
        f'{keyword("HTTP semantics")} define an application-layer request-response contract independent of underlying transport framing. '
        'Clients issue requests specifying a target URI, a standardized method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS), '
        'structured headers containing metadata, and an optional message body. '
        'An HTTP call consists of three foundational architectural segments: the start line, message headers, and an optional payload body. '
        'In a client request, the start line (the request line) conveys three distinct elements: the HTTP method, the request-target URI, and the protocol version '
        '(for example: <samp>GET /v1/catalog/items?category=compute&amp;in_stock=true&amp;limit=50&amp;sort=price_desc HTTP/1.1</samp>). '
        'The request-target URI (RFC 3986) decomposes into the origin-form path (<samp>/v1/catalog/items</samp>) and an optional query string initiated by the '
        'question mark delimiter (<samp>?</samp>), containing key-value pairs separated by ampersands (<samp>&amp;</samp>). '
        'Query string parameters must strictly adhere to RFC 3986 percent-encoding rules, escaping reserved octets such as spaces (<samp>%20</samp> or <samp>+</samp>), '
        'ampersands (<samp>%26</samp>), equals signs (<samp>%3D</samp>), question marks (<samp>%3F</samp>), and slashes (<samp>%2F</samp>). '
        'HTTP queries fulfill critical architectural functions in distributed systems: (1) resource filtering without exploding URL routing namespaces '
        '(<samp>?status=active&amp;environment=production</samp>); (2) collection pagination and bounding (<samp>?page=2&amp;limit=100</samp> or cursor-based '
        '<samp>?starting_after=order_9821</samp>); (3) sorting and field projection (<samp>?sort=created_at:desc&amp;fields=id,sku,amount</samp>); (4) parameterized search expressions '
        '(<samp>?q=kubernetes+egress+policy</samp>); and (5) edge cache key differentiation across CDN layers. In RESTful system design, HTTP queries must '
        'respect safety and idempotency invariants (RFC 9110 §9.2.1): safe methods like GET and HEAD must never trigger server-side state mutations, meaning state changes '
        'must never be driven through query parameters. Furthermore, edge proxies and Content Delivery Networks (CDNs) incorporate the full URI path and query string '
        'into their edge cache keys by default, enabling granular edge caching across filtered datasets. '
        'Servers return a three-digit status code partitioned into five functional classes: 1xx Informational (e.g. 101 Switching Protocols), '
        '2xx Success (e.g. 200 OK, 201 Created, 204 No Content), 3xx Redirection (e.g. 301 Moved Permanently, 304 Not Modified), '
        '4xx Client Errors (e.g. 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests), '
        'and 5xx Server Errors (e.g. 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout). '
        'Understanding the exact boundary between 4xx and 5xx codes is vital: 4xx indicates the client transmitted an invalid payload, invalid credentials, '
        'or exceeded rate quotas, whereas 5xx proves that the receiving server or an intermediate reverse proxy encountered an internal crash, unhandled exception, '
        'or upstream timeout.',
        'Cloud architects use status code taxonomy to establish automated health checking, circuit breaking, and Service Level Objective (SLO) telemetry. '
        'A 502 Bad Gateway response specifically indicates that an intermediate edge proxy or ingress load balancer received an invalid or unparseable response '
        'from an upstream backend runtime, whereas a 504 Gateway Timeout proves the upstream backend failed to respond within the configured timeout deadline. '
        'Conflating 502 and 504 errors leads teams to diagnose backend compute timeouts when the true issue is premature connection termination or malformed HTTP headers. '
        'Architects must also enforce strict query-processing error boundaries: if a query parameter contains invalid syntax, servers must return 400 Bad Request; '
        'if parameter syntax is valid but fails semantic business validation (e.g. <samp>limit=-10</samp>), servers should return 422 Unprocessable Entity; '
        'and if a filtered query returns zero matching records, servers must return 200 OK with an empty collection payload (<samp>[]</samp>), never a 404 Not Found '
        '(which signifies that the resource endpoint collection itself does not exist). '
        'Crucially, architects must enforce a strict zero-trust security invariant regarding HTTP queries: credentials, API secret keys, bearer tokens, '
        'session identifiers, and Personally Identifiable Information (PII) must NEVER be transmitted in query strings. Because query strings form part of the URI, '
        'they are logged in cleartext across intermediate proxy access logs (e.g. Cloud Logging, Nginx access logs), browser histories, and HTTP <samp>Referer</samp> '
        'headers, exposing organizations to credential leakage and compliance violations. Sensitive tokens must reside strictly in encrypted HTTP headers '
        '(e.g. <samp>Authorization: Bearer [token]</samp>) or encrypted POST request bodies.',
        'Google Cloud External Application Load Balancers terminate client HTTP/HTTPS traffic at the edge and generate standardized synthetic status codes. '
        'When all backend instances in a Network Endpoint Group (NEG) fail health checks, Cloud Load Balancing synthesizes an HTTP 502 response '
        'with the response flag <samp>failed_to_pick_backend</samp>. Cloud Monitoring exposes <samp>loadbalancing.googleapis.com/https/request_count</samp> '
        'broken down by response code class, enabling architects to author alerting policies that isolate client errors from infrastructure faults. '
        'Furthermore, Cloud CDN allows architects to configure cache keys to include or exclude specific query parameters, preventing cache pollution '
        'from tracking queries while ensuring filtered product queries remain fast and scalable.',
        ['rfc9110', 'gcp_https_lb', 'gcp_lb_timeouts']
    ),
    subtopic(
        "HTTP/1.1 Connection Management, Pipelining, and Head-of-Line Blocking",
        f'{keyword("HTTP/1.1")} (RFC 9112) introduced persistent TCP connections via the <samp>Connection: keep-alive</samp> header, allowing '
        'multiple sequential requests to reuse an established transport connection and amortize TCP 3-way handshake and TLS negotiation latencies. '
        'However, HTTP/1.1 fundamentally enforces strictly serialized request-response ordering on a given connection: a client cannot send a second '
        'request until the response to the first request has been completely received, or it may attempt HTTP pipelining where requests are batched '
        'but responses must still be returned in exact matching FIFO order. If the first transaction requires heavy backend database processing, '
        'all subsequent queued requests are stalled behind it—a phenomenon known as application-layer <strong class="keyword">head-of-line (HoL) blocking</strong>. '
        'To mitigate this constraint, web browsers historically opened up to 6 parallel TCP connections per host, incurring heavy socket memory overhead.',
        'For cloud architectures, HTTP/1.1 connection concurrency patterns dictate ingress proxy socket pool sizing and backend keep-alive timeout tuning. '
        'If a backend application server configures a keep-alive timeout of 15 seconds while an upstream cloud load balancer configures a backend timeout '
        'of 30 seconds, a classic race condition emerges: the backend server sends a TCP FIN packet just as the load balancer dispatches a new request, '
        'resulting in intermittent TCP connection resets and client-facing 502 errors. Cloud architects must ensure upstream proxy timeouts are strictly '
        'shorter than downstream keep-alive deadlines, or configure backend retry policies on idempotent requests.',
        'For external Application Load Balancer backend services, the documented backend HTTP keepalive timeout is 600 seconds (backend buckets differ). Google Cloud documentation recommends that '
        'backend web servers (such as Nginx, Apache, Envoy, or Gunicorn) running on Compute Engine or GKE must configure their keep-alive timeout '
        'to a value greater than 600 seconds (the documented Apache/nginx examples use 620 seconds) to prevent the backend from closing the connection while Cloud Load Balancing '
        'is actively selecting and reusing the socket.',
        ['rfc9110', 'gcp_https_lb']
    ),
    subtopic(
        "HTTP/2 Binary Framing, Streams, Multiplexing, and TCP HoL Blocking (RFC 9113)",
        f'{keyword("HTTP/2")} (RFC 9113) resolved application-layer head-of-line blocking by replacing plaintext delimited text messages with an '
        'interleaved <strong class="keyword">binary framing layer</strong> operating over a single persistent TCP connection. Logical requests and '
        'responses are decomposed into discrete, typed frames (HEADERS, DATA, SETTINGS, RST_STREAM, PING) tagged with an integer <strong class="keyword">stream identifier</strong>. '
        'Multiple bidirectional streams are multiplexed concurrently across the single TCP socket: a large image download on stream 3 does not block '
        'a high-priority JSON API response on stream 5. Furthermore, HTTP/2 implements HPACK header compression (RFC 7541) to eliminate redundant metadata '
        'overhead across repeated requests. However, because HTTP/2 multiplexes all streams over a single underlying TCP connection, it remains '
        'vulnerable to <strong class="keyword">transport-layer TCP head-of-line blocking</strong>: if a single underlying TCP segment is dropped in transit '
        'by network congestion, the kernel TCP receive buffer halts delivery of all subsequent segments to the application until the missing segment is retransmitted, '
        'stalling all concurrent HTTP/2 streams regardless of which stream lost the packet.',
        'Cloud architects evaluating HTTP/2 must weigh the significant throughput and latency gains of binary multiplexing and HPACK against the impact of '
        'packet loss over lossy wide-area networks (WAN). In cellular or high-loss network environments (packet loss exceeding 2%), HTTP/2 performance '
        'can actually degrade below that of HTTP/1.1 with multiple independent TCP connections, because a single packet drop stalls all multiplexed transactions. '
        'Consequently, HTTP/2 is exceptionally well-suited for controlled, high-bandwidth internal microservice communication (such as gRPC over HTTP/2) '
        'and stable client-to-edge ingress connections.',
        'Google Cloud External Application Load Balancers provide native HTTP/2 termination at the global edge network, negotiating protocol selection '
        'with modern clients via Application-Layer Protocol Negotiation (ALPN). Between Cloud Load Balancing and backend instances, architects can enable '
        'HTTP/2 or gRPC backend protocols, enabling end-to-end stream multiplexing into GKE pods and Compute Engine instance groups.',
        ['rfc9113', 'gcp_https_lb', 'gcp_lb_backends']
    ),
    subtopic(
        "HTTP/3 over QUIC/UDP, Independent Streams, and Modern Cloud Edge Delivery (RFC 9114)",
        f'{keyword("HTTP/3")} (RFC 9114) fundamentally eliminates TCP-level head-of-line blocking by abandoning TCP entirely and building upon the '
        '<strong class="keyword">QUIC protocol</strong> (RFC 9000), which runs over UDP on port 443. QUIC integrates the transport layer and TLS 1.3 '
        'encryption into a unified handshake, enabling 1-RTT connection establishment and 0-RTT connection resumption. Crucially, QUIC implements stream '
        'multiplexing natively at the transport layer: each stream possesses its own independent flow control and loss recovery state. If a UDP datagram '
        'carrying data for stream 7 is dropped by a congested intermediate router, only stream 7 pauses waiting for retransmission; streams 9, 11, and 13 '
        'continue processing and delivering data to user-space runtimes without interruption. Additionally, QUIC replaces the rigid 4-tuple connection '
        'identifier with an opaque <strong class="keyword">Connection ID</strong>, enabling seamless <strong class="keyword">connection migration</strong>: '
        'a mobile client transitioning from Wi-Fi to a 5G cellular network preserves its active TLS session and active file downloads without renegotiating '
        'a handshake or breaking active streams.',
        'From an architectural standpoint, HTTP/3 represents the premier ingress protocol for mobile and global public-facing applications subject '
        'to unpredictable network quality. However, cloud architects must ensure perimeter firewalls, cloud security groups, and intermediate DDoS '
        'appliances permit inbound UDP traffic on port 443; historically, enterprise firewalls heavily throttle or drop UDP traffic under the assumption '
        'that large UDP streams represent DNS amplification or UDP flood attacks. If UDP 443 is blocked, clients fall back to HTTP/2 over TCP.',
        'Google Cloud was a pioneer in QUIC development, and Google Cloud External Application Load Balancers provide out-of-the-box support for HTTP/3. '
        'Enabling HTTP/3 in Cloud Load Balancing automatically injects the <samp>Alt-Svc: h3=":443"; ma=2592000</samp> header into HTTPS responses, '
        'instructing supporting web browsers to upgrade future connections to HTTP/3 over UDP.',
        ['rfc9114', 'rfc9114_requests', 'rfc9113_setup', 'rfc9110_https', 'gcp_lb_http3']
    )
]

HTTP_SETUP_SVG = '<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg role="img" aria-labelledby="d004-http-setup-title d004-http-setup-desc" viewBox="0 0 1440 690" style="display:block;width:100%;min-width:1440px;height:auto;background:#090d16;font-family:ui-monospace,monospace">\n<title id="d004-http-setup-title">HTTP Versions: Connection Setup and First Request Sequences</title>\n<desc id="d004-http-setup-desc">Three independent numbered request-response sequences compare TCP plus TLS for HTTP/1.1 and HTTP/2 with QUIC and integrated TLS for HTTP/3. Each row progresses left to right; these are illustrative mechanisms, not locally captured traffic.</desc>\n<defs><marker id="d004-http-setup-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#38bdf8"/></marker></defs>\n<text x="30" y="42" fill="#f8fafc" font-size="22" font-weight="700">HTTP versions: connection setup → first request → response</text>\n<text x="30" y="101" fill="#7dd3fc" font-size="20" font-weight="700">HTTP/1.1 over TCP + TLS</text>\n<g transform="translate(30,125)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/client.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">1. TCP connection</text><text x="16" y="72" fill="#e2e8f0" font-size="14">Client and server</text><text x="16" y="96" fill="#e2e8f0" font-size="14">establish TCP</text></g>\n<line x1="300" y1="182" x2="390" y2="182" stroke="#38bdf8" stroke-width="2" marker-end="url(#d004-http-setup-arrow)"/><text x="345" y="164" text-anchor="middle" fill="#cbd5e1" font-size="14">1→2</text>\n<g transform="translate(400,125)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/policy.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">2. TLS handshake</text><text x="16" y="72" fill="#e2e8f0" font-size="14">Authenticate certificate</text><text x="16" y="96" fill="#e2e8f0" font-size="14">Establish encryption</text></g>\n<line x1="670" y1="182" x2="760" y2="182" stroke="#38bdf8" stroke-width="2" marker-end="url(#d004-http-setup-arrow)"/><text x="715" y="164" text-anchor="middle" fill="#cbd5e1" font-size="14">2→3</text>\n<g transform="translate(770,125)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/artifact.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">3. First request</text><text x="16" y="72" fill="#e2e8f0" font-size="14">HTTP/1.1 method + target</text><text x="16" y="96" fill="#e2e8f0" font-size="14">Headers and body</text></g>\n<line x1="1040" y1="182" x2="1130" y2="182" stroke="#38bdf8" stroke-width="2" marker-end="url(#d004-http-setup-arrow)"/><text x="1085" y="164" text-anchor="middle" fill="#cbd5e1" font-size="14">3→4</text>\n<g transform="translate(1140,125)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/server.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">4. First response</text><text x="16" y="72" fill="#e2e8f0" font-size="14">HTTP status + headers</text><text x="16" y="96" fill="#e2e8f0" font-size="14">Response body</text></g>\n<text x="30" y="291" fill="#7dd3fc" font-size="20" font-weight="700">HTTP/2 over TCP + TLS</text>\n<g transform="translate(30,315)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/client.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">1. TCP connection</text><text x="16" y="72" fill="#e2e8f0" font-size="14">Client and server</text><text x="16" y="96" fill="#e2e8f0" font-size="14">establish TCP</text></g>\n<line x1="300" y1="372" x2="390" y2="372" stroke="#38bdf8" stroke-width="2" marker-end="url(#d004-http-setup-arrow)"/><text x="345" y="354" text-anchor="middle" fill="#cbd5e1" font-size="14">1→2</text>\n<g transform="translate(400,315)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/policy.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">2. TLS + ALPN h2</text><text x="16" y="72" fill="#e2e8f0" font-size="14">Authenticate certificate</text><text x="16" y="96" fill="#e2e8f0" font-size="14">Select HTTP/2</text></g>\n<line x1="670" y1="372" x2="760" y2="372" stroke="#38bdf8" stroke-width="2" marker-end="url(#d004-http-setup-arrow)"/><text x="715" y="354" text-anchor="middle" fill="#cbd5e1" font-size="14">2→3</text>\n<g transform="translate(770,315)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/artifact.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">3. First request stream</text><text x="16" y="72" fill="#e2e8f0" font-size="14">HTTP/2 binary frames</text><text x="16" y="96" fill="#e2e8f0" font-size="14">HEADERS then DATA</text></g>\n<line x1="1040" y1="372" x2="1130" y2="372" stroke="#38bdf8" stroke-width="2" marker-end="url(#d004-http-setup-arrow)"/><text x="1085" y="354" text-anchor="middle" fill="#cbd5e1" font-size="14">3→4</text>\n<g transform="translate(1140,315)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/server.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">4. Response stream</text><text x="16" y="72" fill="#e2e8f0" font-size="14">Frames carry status/body</text><text x="16" y="96" fill="#e2e8f0" font-size="14">Stream ID identifies flow</text></g>\n<text x="30" y="481" fill="#7dd3fc" font-size="20" font-weight="700">HTTP/3 over QUIC / UDP</text>\n<g transform="translate(30,505)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/client.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">1. QUIC connection</text><text x="16" y="72" fill="#e2e8f0" font-size="14">UDP transport</text><text x="16" y="96" fill="#e2e8f0" font-size="14">No TCP connection</text></g>\n<line x1="300" y1="562" x2="390" y2="562" stroke="#38bdf8" stroke-width="2" marker-end="url(#d004-http-setup-arrow)"/><text x="345" y="544" text-anchor="middle" fill="#cbd5e1" font-size="14">1→2</text>\n<g transform="translate(400,505)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/policy.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">2. Integrated TLS + h3</text><text x="16" y="72" fill="#e2e8f0" font-size="14">Authenticate certificate</text><text x="16" y="96" fill="#e2e8f0" font-size="14">QUIC handshake + TLS 1.3</text></g>\n<line x1="670" y1="562" x2="760" y2="562" stroke="#38bdf8" stroke-width="2" marker-end="url(#d004-http-setup-arrow)"/><text x="715" y="544" text-anchor="middle" fill="#cbd5e1" font-size="14">2→3</text>\n<g transform="translate(770,505)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/artifact.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">3. First request stream</text><text x="16" y="72" fill="#e2e8f0" font-size="14">HTTP/3 frames</text><text x="16" y="96" fill="#e2e8f0" font-size="14">Independent QUIC stream</text></g>\n<line x1="1040" y1="562" x2="1130" y2="562" stroke="#38bdf8" stroke-width="2" marker-end="url(#d004-http-setup-arrow)"/><text x="1085" y="544" text-anchor="middle" fill="#cbd5e1" font-size="14">3→4</text>\n<g transform="translate(1140,505)"><rect width="270" height="115" rx="10" fill="#121526" stroke="#38bdf8"/><image href="../assets/icons/generic/server.svg" x="15" y="15" width="30" height="30" preserveAspectRatio="xMidYMid meet"/><text x="54" y="35" fill="#7dd3fc" font-size="15" font-weight="700">4. Response stream</text><text x="16" y="72" fill="#e2e8f0" font-size="14">Status/body on stream</text><text x="16" y="96" fill="#e2e8f0" font-size="14">No TCP loss blocking</text></g>\n</svg></div><figcaption>Illustrative setup and first-request sequences, read 1→2→3→4 in each independent row: (1) establish the transport, (2) authenticate and secure it, (3) send the request, (4) receive the response. HTTP/2 uses TLS ALPN and framed streams; HTTP/3 integrates TLS into QUIC over UDP. Resumption, early data and packet-level handshake timing are omitted. RFC 9110 §4.2.2, RFC 9113 §§3.2/8.2.1, RFC 8446 §4 (historical) and RFC 9114 §§3/4 support the scope; Lab 1 locally speaks HTTP/1.0 and simulates later-version behavior.</figcaption></figure>'

T1_TECH = discussion(
    [
        "HTTP Request/Response Semantics and Status Code Taxonomy (RFC 9110)",
        "HTTP/1.1 Connection Management, Pipelining, and Head-of-Line Blocking",
        "HTTP/2 Binary Framing, Streams, Multiplexing, and TCP HoL Blocking (RFC 9113)",
        "HTTP/3 over QUIC/UDP, Independent Streams, and Modern Cloud Edge Delivery (RFC 9114)"
    ],
    [*T1_SUBTOPICS[:-1], T1_SUBTOPICS[-1] + HTTP_SETUP_SVG],
    "An external client issues an HTTPS request to an e-commerce API. The Cloud Load Balancer negotiates HTTP/3 via UDP 443, demultiplexes "
    "incoming JSON requests across independent QUIC streams, uses the configured HTTP/2 backend protocol for delivery to the selected GKE backend; this example does not establish Andromeda request internals, "
    "and returns an HTTP 200 OK response with Alt-Svc headers advertising HTTP/3 availability.",
    "The local Python server speaks HTTP/1.0; HTTP/2 and HTTP/3 behavior is simulated, not negotiated or benchmarked. Protocol models explain binary framing and stream concurrency mechanics, but cannot replicate the packet loss "
    "and high-latency conditions of global wide-area mobile networks where QUIC connection migration and independent stream loss recovery deliver their primary advantages."
)

# ==============================================================================
# TOPIC 02: TLS 1.3 handshake and certificate validation chains
# ==============================================================================
TLS_FLOW_SVG = flow_svg('d004-tls-handshake', 'TLS 1.3 1-RTT Handshake: Key Exchange and Certificate Validation', [
    ('Client Init', ('Sends ClientHello', 'Offers ECDH key_share'), 'client'),
    ('Server Hello', ('Selects cipher suite', 'Sends Server key_share'), 'server'),
    ('Encrypted Config', ('Sends EncryptedExts', 'Transmits Leaf+Chain'), 'server'),
    ('Cert Verify', ('CertificateVerify sig', 'Finished MAC authenticator'), 'policy'),
    ('Client Finished', ('Verifies X.509 chain', 'Sends Client Finished'), 'client'),
    ('Encrypted Data', ('Derives 1-RTT keys', 'AEAD HTTP/2 streams'), 'outcome'),
], [
    '1. ClientHello (ECDH)',
    '2. ServerHello (ECDH)',
    '3. Encrypted Extensions',
    '4. CertVerify + Finished',
    '5. Client Finished',
], 'TLS 1.3 1-RTT cryptographic handshake sequence showing key exchange, certificate chain transmission, and mutual verification.')

CERT_CHAIN_FLOW_SVG = flow_svg('d004-cert-validation-chain', 'X.509 PKI Certificate Validation Chain Sequence (RFC 5280)', [
    ('Leaf Inspection', ('Extracts tbsCertificate', 'Parses ASN.1 DER / SAN'), 'client'),
    ('Temporal Validity', ('Checks notBefore / notAfter', 'Validates current UTC time'), 'event'),
    ('Identity & SAN Match', ('Matches requested FQDN', 'Rejects CN-only fallback'), 'policy'),
    ('Issuer Key Linkage', ('Matches AKI to SKI', 'Verifies isCA=TRUE limit'), 'policy'),
    ('Cryptographic Sig', ('Computes SHA-256 digest', 'Decrypts with Parent Key'), 'policy'),
    ('Root Anchor Trust', ('Matches Local Trust Store', 'Establishes trusted session'), 'outcome'),
], [
    '1. Parse TBS & SAN',
    '2. Verify UTC Window',
    '3. Match Hostname',
    '4. Link AKI to SKI',
    '5. Verify Issuer Sig',
], 'X.509 PKI certificate validation chain sequence (RFC 5280 §6): client extracts tbsCertificate, validates UTC timestamp windows and SAN hostnames, links AKI to SKI across intermediate authorities, verifies SHA-256 signatures, and anchors trust in local root store.')

OCSP_FLOW_SVG = flow_svg('d004-ocsp-stapling-lifecycle', 'OCSP Stapling and Revocation Verification Lifecycle (RFC 6066 / RFC 6960)', [
    ('Periodic Query', ('Server queries CA OCSP', 'Sends async HTTP request'), 'server'),
    ('CA Signed Token', ('CA evaluates CRL state', 'Signs timestamped OCSP'), 'policy'),
    ('Edge Response Cache', ('Edge proxy caches token', 'Tracks NextUpdate ttl timer'), 'artifact'),
    ('Client Hello Status', ('Client sends status_request', 'Offers OCSP stapling ext'), 'client'),
    ('In-Band TLS Staple', ('Bundles CertificateStatus', 'Transmits cached token'), 'server'),
    ('0ms Verification', ('Client verifies CA sig', 'Completes TLS 0ms lookup'), 'outcome'),
], [
    '1. Async Query',
    '2. Return Signed OCSP',
    '3. Cache at Edge',
    '4. ClientHello status_request',
    '5. Staple CertificateStatus',
], 'OCSP stapling lifecycle (RFC 6066 / RFC 6960): edge server queries CA responder asynchronously, caches signed status, and staples CertificateStatus into TLS handshake, eliminating client DNS/HTTP latency and CA tracking.')

CERTIFICATE_TYPES_TABLE_HTML = """<figure class="table-figure">
<div class="table-container">
<table class="comparison-table">
  <caption>Architectural Classification of X.509 Certificate Types, Layers, and Usage Patterns</caption>
  <thead>
    <tr>
      <th scope="col">Certificate Type</th>
      <th scope="col">Architectural Layer</th>
      <th scope="col">Scope &amp; Subject Identity</th>
      <th scope="col">Key Extensions &amp; Constraints (RFC 5280)</th>
      <th scope="col">How Application Teams Use It</th>
      <th scope="col">How Load Balancers &amp; Edge Proxies Use It</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Root CA Certificate</strong></td>
      <td>Layer 7 / Trust Anchor</td>
      <td>Self-signed root trust anchor representing the root of trust for an entire PKI hierarchy.</td>
      <td><code>basicConstraints=critical,CA:TRUE</code> (unconstrained or high pathlen), <code>keyUsage=keyCertSign,cRLSign</code></td>
      <td>Installed into operating system and runtime trust stores (<code>/etc/ssl/certs</code>, Java <code>cacerts</code>); application runtimes use it to validate server certificate chains. Private enterprise roots are injected into container base images.</td>
      <td>Not deployed directly on edge proxies; Cloud Load Balancer proxies trust public Web PKI roots (or private CA pools) when performing backend re-encryption validation.</td>
    </tr>
    <tr>
      <td><strong>Intermediate / Subordinate CA Certificate</strong></td>
      <td>Layer 7 / PKI Issuance Tier</td>
      <td>Issued by a Root CA or superior Intermediate to compartmentalize signing authority and protect Root private keys offline.</td>
      <td><code>basicConstraints=critical,CA:TRUE,pathlen:0/1</code>, <code>keyUsage=keyCertSign,cRLSign</code>, AKI/SKI key linkage</td>
      <td>Application teams submit Certificate Signing Requests (CSRs) to Intermediates. Teams must configure their web servers with the full chain bundle (leaf + intermediate) to prevent client validation errors.</td>
      <td>Configured in Cloud Load Balancer / Certificate Manager as part of the certificate chain bundle served to clients during the TLS handshake to ensure complete chain verification.</td>
    </tr>
    <tr>
      <td><strong>Server / Leaf Certificate (Single-Domain)</strong></td>
      <td>Layer 7 / TLS Termination</td>
      <td>End-entity identity binding a single Fully Qualified Domain Name (FQDN, e.g. <code>api.example.com</code>) to a public key.</td>
      <td><code>basicConstraints=CA:FALSE</code>, <code>extendedKeyUsage=serverAuth</code>, <code>SAN=dNSName:api.example.com</code>, <code>keyUsage=digitalSignature,keyEncipherment</code></td>
      <td>Deployed directly to application web servers (Envoy, Nginx, Spring Boot) or managed via Kubernetes <code>cert-manager</code> for ingress controllers.</td>
      <td>Attached to Target HTTPS Proxy on Google Cloud Load Balancer for public edge TLS termination; traffic is decrypted before URL map routing.</td>
    </tr>
    <tr>
      <td><strong>Wildcard Certificate (<code>*.example.com</code>)</strong></td>
      <td>Layer 7 / Ingress Aggregation</td>
      <td>Secures an apex domain and all immediate first-level subdomains (e.g. <code>auth.example.com</code>, <code>billing.example.com</code>).</td>
      <td><code>basicConstraints=CA:FALSE</code>, <code>SAN=dNSName:*.example.com, dNSName:example.com</code>, <code>extendedKeyUsage=serverAuth</code></td>
      <td>Simplifies secret management across dynamic microservice environments, eliminating the need to issue a new certificate for each microservice deployment.</td>
      <td>Uploaded to Certificate Manager or provisioned via DNS authorization; matches incoming SNI for dynamic subdomains on a single Anycast frontend VIP.</td>
    </tr>
    <tr>
      <td><strong>Multi-Domain / SAN Certificate (UCC)</strong></td>
      <td>Layer 7 / Multi-Tenant Edge</td>
      <td>Secures multiple distinct, unrelated domain names (e.g. <code>example.com</code>, <code>shop.net</code>, <code>api.internal</code>) in a single certificate.</td>
      <td><code>basicConstraints=CA:FALSE</code>, <code>SAN</code> containing multiple diverse <code>dNSName</code> entries, <code>extendedKeyUsage=serverAuth</code></td>
      <td>Used by application teams consolidating multi-brand microservices onto a unified ingress controller or shared API gateway.</td>
      <td>Configured on External Application Load Balancers to serve multiple disparate tenant hostnames from a single shared Target HTTPS Proxy.</td>
    </tr>
    <tr>
      <td><strong>Client Certificate (Mutual TLS / mTLS)</strong></td>
      <td>Layer 4 / Layer 7 Zero-Trust Identity</td>
      <td>Authenticates the client identity (service, user, or device) to the server during mutual TLS handshakes.</td>
      <td><code>basicConstraints=CA:FALSE</code>, <code>extendedKeyUsage=clientAuth</code>, <code>SAN=URI:spiffe://...</code> or <code>dNSName</code> / <code>email</code></td>
      <td>Application teams configure client HTTP connection pools with private key + client cert to authenticate outbound API requests in zero-trust architectures.</td>
      <td>Google Cloud Load Balancer / API Gateway configured with mTLS validates incoming client certificate against trusted CA pool before proxying request.</td>
    </tr>
    <tr>
      <td><strong>Private / Internal CA Certificate</strong></td>
      <td>Layer 7 / Enterprise VPC</td>
      <td>Issued by internal private PKI (e.g. Google Cloud Certificate Authority Service - CAS) for internal VPC service mesh and database endpoints.</td>
      <td>Custom enterprise OIDs, <code>basicConstraints=CA:FALSE</code>, <code>extendedKeyUsage=serverAuth,clientAuth</code></td>
      <td>App teams use automated CAS connectors to mint short-lived certificates for internal database connections, gRPC services, and Cloud SQL SSL.</td>
      <td>Attached to Internal Application Load Balancers or backend services to encrypt traffic traversing internal VPCs without public Web PKI dependencies.</td>
    </tr>
    <tr>
      <td><strong>Self-Signed Certificate</strong></td>
      <td>Layer 7 / Dev &amp; Bootstrap</td>
      <td>Generated locally (<code>openssl req -x509</code>) where the subject and issuer are identical; zero chain of trust.</td>
      <td><code>basicConstraints=CA:FALSE</code>, <code>keyUsage=digitalSignature</code>, no third-party signature</td>
      <td>Used strictly in local development environments, unit tests, or ephemeral CI/CD pipelines; rejected by production browsers and default trust stores.</td>
      <td>Not permitted on public Cloud Load Balancer frontends; can be used for backend re-encryption only if insecure backend verification is explicitly tolerated.</td>
    </tr>
  </tbody>
</table>
</div>
<figcaption>Classification of X.509 certificate types across architectural tiers, contrasting client application workflows with edge load balancer termination mechanisms.</figcaption>
</figure>"""

T2_SUBTOPICS = [
    subtopic(
        "TLS 1.3 Handshake Protocol and 1-RTT Cryptographic Exchange (RFC 8446)",
        f'{keyword("TLS 1.3")} (RFC 8446) overhauled transport security by deprecating obsolete cryptographic primitives (RSA key transport, CBC ciphers, '
        'RC4, SHA-1, 3DES) and enforcing forward secrecy through mandatory ephemeral Diffie-Hellman key exchange (ECDHE / DHE). The protocol streamlines '
        'the cryptographic handshake from two round trips (2-RTT) in TLS 1.2 down to a single round trip (<strong class="keyword">1-RTT</strong>). '
        'In the very first <strong class="keyword">ClientHello</strong> message, the client speculatively generates and transmits its own Diffie-Hellman key share '
        'alongside supported cipher suites and key exchange groups. The server selects a matching group, generates its corresponding key share, and responds '
        'with a <strong class="keyword">ServerHello</strong>. At this precise instant, both endpoints derive the ephemeral traffic keys: all subsequent server '
        'handshake messages—including <samp>EncryptedExtensions</samp>, the server <samp>Certificate</samp>, the <samp>CertificateVerify</samp> signature, '
        'and the <samp>Finished</samp> message—are fully encrypted using Authenticated Encryption with Associated Data (AEAD, such as AES-GCM or ChaCha20-Poly1305). '
        'TLS 1.3 also supports 0-RTT Early Data for resumed sessions, though architects must evaluate replay attack vulnerabilities before enabling 0-RTT on non-idempotent endpoints.',
        'For enterprise cloud architects, TLS 1.3 delivers significant latency reductions for edge ingress, cutting connection setup time by 50% compared '
        'to TLS 1.2. Because the server certificate is encrypted over the wire in TLS 1.3, passive network eavesdroppers cannot inspect the server identity '
        'or Server Name Indication (SNI) extensions if Encrypted Client Hello (ECH) is deployed, strengthening enterprise privacy postures.',
        'Google Cloud Load Balancing supports TLS 1.3 across all global external application and proxy load balancers. Architects configure <strong class="keyword">SSL policies</strong> '
        'in Google Cloud to enforce minimum TLS versions (e.g. restricting clients to TLS 1.2 or TLS 1.3) and select curated cipher profiles '
        '(RESTRICTED, MODERN, or COMPATIBLE) to comply with PCI-DSS and FedRAMP cryptographic standards.',
        ['rfc8446', 'gcp_cert_mgr', 'gcp_cert_benefits']
    ) + TLS_FLOW_SVG,
    subtopic(
        "X.509 PKI Trust Architecture and Certificate Validation Chains (RFC 5280)",
        f'<strong class="side-heading">PKI Hierarchy &amp; Trust Model:</strong> The <strong class="keyword">X.509 Public Key Infrastructure</strong> (RFC 5280) establishes cryptographic identity through a hierarchical chain '
        'of digital trust. A <strong class="keyword">Certificate Authority (CA)</strong> is a trusted third-party organization or internal PKI governance authority '
        'responsible for verifying applicant identities and issuing cryptographically signed digital certificates. In the Web PKI trust model, trust is anchored '
        'in curated <strong class="keyword">Trust Stores</strong> maintained by operating systems (Linux NSS, Apple, Microsoft) and browser vendors (Google Chrome Root Program). '
        'To establish defense-in-depth, CAs employ a strict two-tier architecture: the <strong class="keyword">Root CA</strong> serves as the ultimate trust anchor, '
        'with its private key protected in air-gapped, offline FIPS 140-2 Level 3 Hardware Security Modules (HSMs) accessed only during formal multi-person key ceremonies. '
        'The Root CA signs one or more online <strong class="keyword">Intermediate CAs</strong> (subordinate CAs), which handle day-to-day certificate signing requests (CSRs) '
        'and issue end-entity (<strong class="keyword">leaf certificates</strong>). If an intermediate CA key is ever compromised, only that intermediate is revoked via CRL or OCSP, '
        'leaving the global Root trust anchor intact.</p>\n'
        '<p><strong class="side-heading">CSRs &amp; Validation Tiers:</strong> An applicant generates a key pair and submits a <strong class="keyword">Certificate Signing Request (CSR, PKCS#10)</strong>, '
        'which contains the public key, requested subject domains, and a signature generated by the applicant’s private key proving proof-of-possession. '
        'CAs issue certificates under three standardized validation tiers: Domain Validation (DV, automated proof of DNS or HTTP control via ACME RFC 8555), '
        'Organization Validation (OV, vetting legal entity existence), and Extended Validation (EV, comprehensive cross-referenced legal auditing).</p>\n'
        '<p><strong class="side-heading">X.509 Certificate Internals (RFC 5280 §4.1):</strong> Under the hood, an X.509 v3 certificate is an ASN.1 (Abstract Syntax Notation One) structured object, serialized in binary Distinguished Encoding Rules (DER) '
        'or base64-encoded Privacy-Enhanced Mail (PEM) format (<samp>-----BEGIN CERTIFICATE-----</samp>). An X.509 certificate consists of three top-level fields (RFC 5280 §4.1): '
        '(1) the <strong class="keyword">tbsCertificate</strong> (To-Be-Signed payload); (2) the <strong class="keyword">signatureAlgorithm</strong> identifier; and '
        '(3) the <strong class="keyword">signatureValue</strong> (the CA’s raw digital signature bit string). The <samp>tbsCertificate</samp> contains the entire '
        'cryptographic and identity payload: Version (v3 = 0x02); Serial Number (a positive integer up to 20 octets generated with at least 64 bits of cryptographic entropy '
        'to thwart hash collision attacks); Signature Algorithm OID (e.g. <samp>sha256WithRSAEncryption</samp> or <samp>ecdsa-with-SHA256</samp>); Issuer Distinguished Name (DN); '
        'Validity period bounded by <samp>notBefore</samp> and <samp>notAfter</samp> timestamps; Subject DN; Subject Public Key Info (specifying the key algorithm OID, '
        'such as RSA 2048/4096-bit modulus and exponent or ECDSA elliptic curve parameters with coordinate point <samp>(x,y)</samp> on curve <samp>prime256v1</samp>); '
        'and standard X.509 v3 extensions.</p>\n'
        '<p><strong class="side-heading">Standard X.509 v3 Extensions:</strong> Crucial extensions include: <strong class="keyword">Subject Alternative Name (SAN, id-ce-subjectAltName)</strong> enumerating valid <samp>dNSName</samp> '
        'and <samp>iPAddress</samp> identities; <strong class="keyword">Basic Constraints (id-ce-basicConstraints)</strong> designating whether the certificate is a CA (<samp>cA: TRUE/FALSE</samp>) '
        'and bounding maximum subordinate chain depth via <samp>pathLenConstraint</samp>; <strong class="keyword">Key Usage (id-ce-keyUsage)</strong> defining permitted cryptographic operations '
        '(<samp>digitalSignature</samp>, <samp>keyEncipherment</samp>, <samp>keyCertSign</samp>, <samp>cRLSign</samp>); <strong class="keyword">Extended Key Usage (EKU, id-ce-extKeyUsage)</strong> '
        'restricting purpose to <samp>serverAuth</samp> or <samp>clientAuth</samp>; <strong class="keyword">Authority Key Identifier (AKI)</strong> and <strong class="keyword">Subject Key Identifier (SKI)</strong> '
        'linking child keys to parent keys; and <strong class="keyword">Authority Information Access (AIA)</strong> providing HTTP URIs for OCSP responders and issuing CA certificates.</p>\n'
        '<p><strong class="side-heading">Cryptographic Signature Verification:</strong> Cryptographic validation operates via rigorous mathematical verification: the issuing CA hashes the canonical DER-encoded <samp>tbsCertificate</samp> using SHA-256 '
        '(<samp>H = SHA-256(DER(tbsCertificate))</samp>) and encrypts/signs the hash using the CA’s private key. During connection establishment, the client extracts the '
        '<samp>tbsCertificate</samp>, independently computes <samp>H\' = SHA-256(DER(tbsCertificate))</samp>, and verifies the signature using the issuer’s public key '
        'extracted from the parent certificate. If the signature decrypts correctly and matches <samp>H\'</samp>, the certificate is mathematically proven to be authentic and unaltered.</p>\n'
        '<p><strong class="side-heading">Client Verification Sequence &amp; SAN Deprecation:</strong> The client executes an exhaustive algorithmic verification sequence: (1) validates that current system time falls strictly between <samp>notBefore</samp> and <samp>notAfter</samp>; '
        '(2) verifies cryptographic signatures link-by-link up to a trusted root in the local trust store; (3) verifies basic constraints confirm all intermediate certificates are valid CAs (<samp>isCA=TRUE</samp>); '
        'and (4) verifies that the requested hostname matches the certificate identity. Modern TLS standards strictly deprecate the legacy <samp>Common Name (CN)</samp> attribute '
        'in favor of the <strong class="keyword">Subject Alternative Name (SAN)</strong> extension. If a server certificate presents a CN matching the requested hostname but lacks '
        'a corresponding <samp>dNSName</samp> entry in its SAN extension, modern clients (including Go runtimes, Python urllib3, Chrome, and curl) immediately reject the connection with a hostname verification failure.',
        'Cloud architects must design certificate rotation pipelines that preserve intermediate chain delivery. A common enterprise failure mode is '
        'configuring a web server or load balancer with only the leaf certificate while omitting the intermediate CA certificate. While desktop browsers '
        'frequently mask this error by caching intermediate CAs or performing Authority Information Access (AIA) fetching over HTTP, automated microservice '
        'clients, containerized runtimes, and mobile SDKs strictly fail with <samp>unable to get local issuer certificate</samp>, causing catastrophic service breakages.',
        'Google Cloud Certificate Manager provides centralized management of Google-managed and self-managed SSL certificates. Google-managed certificates '
        'can be automatically issued and renewed; Supported TLS certificates also permits a Certificate Authority Service CA pool as issuer. '
        'The cited section does not specify a universal 90-day lifetime or promise complete chain provisioning without validation; inspect the deployed certificate chain and authorization state.',
        ['rfc5280', 'rfc9525', 'gcp_cert_mgr']
    ) + CERT_CHAIN_FLOW_SVG + CERTIFICATE_TYPES_TABLE_HTML,
    subtopic(
        "Certificate Revocation and Verification Mechanisms: CRLs vs OCSP Stapling",
        f'<strong class="side-heading">Revocation Mechanisms (CRLs vs OCSP):</strong> When a private key is compromised or a server is decommissioned prior to certificate expiration, the certificate must be revoked. '
        'Two primary mechanisms exist: <strong class="keyword">Certificate Revocation Lists (CRLs)</strong> and the <strong class="keyword">Online Certificate Status Protocol (OCSP)</strong>. '
        'A CRL is a digitally signed file published periodically by a CA enumerating all revoked serial numbers; however, CRLs grow unwieldy in size '
        '(megabytes) and introduce significant bandwidth overhead and latency. OCSP (RFC 6960) provides real-time status queries for individual certificates; '
        'yet traditional client-side OCSP lookups force the client to establish a synchronous HTTP connection to the CA’s OCSP responder before completing '
        'the TLS handshake, introducing latency and leaking the user’s browsing history to the CA.</p>\n'
        '<p><strong class="side-heading">OCSP Stapling (RFC 6066):</strong> To solve these defects, <strong class="keyword">OCSP stapling</strong> '
        '(RFC 6066) shifts the lookup burden to the server: the server periodically queries the CA responder, caches the time-stamped, CA-signed OCSP response, '
        'and "staples" it directly into the TLS handshake <samp>CertificateStatus</samp> message, enabling the client to verify revocation status offline instantaneously.',
        'Architects must account for the operational trade-off between security and availability in revocation checking. Most client libraries operate in '
        '<strong class="keyword">soft-fail</strong> mode: if an OCSP responder is unreachable, the client ignores the failure and proceeds with the connection. '
        'However, high-security financial and healthcare architectures often mandate <strong class="keyword">hard-fail</strong> mode (or OCSP Must-Staple), '
        'meaning an expired or missing OCSP staple causes immediate connection termination. If an edge proxy fails to refresh its staple due to an egress '
        'firewall misconfiguration, an enterprise-wide outage ensues.',
        'Google Cloud Certificate Manager documents automatic issuance and renewal of Google-managed certificates, not a universal OCSP-stapling or zero-lookup guarantee. '
        'For the chosen load balancer and certificate, inspect a real handshake for certificate status extensions before claiming a staple or a client-latency benefit; this lab does not measure that behavior.',
        ['rfc5280', 'gcp_cert_mgr']
    ) + OCSP_FLOW_SVG,
    subtopic(
        "Enterprise TLS Governance, ALPN Negotiation, and Google Cloud Certificate Management",
        f'Enterprise TLS governance standardizes cryptographic postures across diverse services and teams. <strong class="keyword">Application-Layer Protocol Negotiation (ALPN)</strong> '
        '(RFC 7301) operates inside the TLS handshake ClientHello and ServerHello extensions, allowing the client and server to negotiate the application protocol '
        '(such as <samp>h2</samp> for HTTP/2 or <samp>http/1.1</samp>) before the handshake completes, avoiding an extra application-layer round trip. '
        'In addition to protocol negotiation, enterprise security policies mandate restricting accepted cipher suites to those offering authenticated encryption '
        'and forward secrecy (e.g., <samp>TLS_AES_128_GCM_SHA256</samp>, <samp>TLS_AES_256_GCM_SHA384</samp>, <samp>ECDHE-ECDSA-AES128-GCM-SHA256</samp>) '
        'while completely disallowing legacy static RSA key exchanges and CBC mode ciphers vulnerable to padding oracle attacks.\n\n'
        'In production engineering, <strong class="keyword">application teams use certificates</strong> across several operational lifecycles: '
        '(1) <strong class="side-heading">Key &amp; CSR Generation:</strong> Developers generate private keys using modern curves (<samp>prime256v1</samp> / P-256 or <samp>ed25519</samp>) '
        'or RSA (minimum 2048-bit, 3072-bit recommended) and create PKCS#10 CSRs specifying exact SAN hostnames. '
        '(2) <strong class="side-heading">Key Protection &amp; Secret Management:</strong> Private keys are never stored in source code repositories or baked into Docker container images; '
        'they are secured in Google Cloud Secret Manager, HashiCorp Vault, or Kubernetes Secrets, mounted into pods with strict POSIX file permissions (<samp>chmod 0600</samp>). '
        '(3) <strong class="side-heading">Runtime Configuration:</strong> In Java / Spring Boot microservices, teams package private keys and certificate chains into PKCS#12 bundles '
        '(<samp>.p12</samp>) and configure <samp>server.ssl.key-store</samp>; in Go runtimes, services configure <samp>tls.LoadX509KeyPair()</samp>; in Node.js, services pass keys and certs to '
        '<samp>https.createServer()</samp>; and in Python, services initialize <samp>ssl.create_default_context()</samp>. '
        '(4) <strong class="side-heading">Trust Store Governance:</strong> For internal microservices communicating over private VPC networks, application teams inject internal enterprise CA root certificates '
        'into base container images (<samp>/etc/ssl/certs</samp> via <samp>update-ca-certificates</samp> or Java <samp>cacerts</samp> via <samp>keytool -importcert</samp>) so workloads trust internal endpoints. '
        '(5) <strong class="side-heading">Automated Rotation Pipelines:</strong> Teams deploy Kubernetes <samp>cert-manager</samp> to automate issuance and renewal before certificate expiration, '
        'triggering graceful rolling restarts upon secret update. '
        '(6) <strong class="side-heading">Client Mutual TLS (mTLS):</strong> For zero-trust service-to-service communication, applications configure outbound HTTP/gRPC connection pools with client certificates '
        'to cryptographically prove caller identity to downstream microservices.\n\n'
        'Simultaneously, <strong class="keyword">cloud load balancers and reverse proxies use certificates</strong> to manage traffic at scale: '
        '(1) <strong class="side-heading">Edge TLS Termination (SSL Offloading):</strong> Google Cloud External Application Load Balancers terminate client TLS sessions at Google’s global edge network (Edge PoPs). '
        'The load balancer executes compute-intensive cryptographic handshakes and ephemeral key derivation at the edge, decrypts the request payload, evaluates URL map routing rules and Cloud Armor security policies, '
        'and offloads TLS CPU overhead from backend container instances. '
        '(2) <strong class="side-heading">Server Name Indication (SNI) Routing:</strong> When multiple disparate customer domains map to a single Anycast external IP address, the load balancer inspects the SNI extension '
        'in the client’s <samp>ClientHello</samp>, matches the hostname against configured certificate maps, and returns the appropriate server certificate in the <samp>ServerHello</samp>. '
        '(3) <strong class="side-heading">Google-Managed vs. Self-Managed Certificates:</strong> Google-managed certificates automate domain verification (via DNS or load balancer authorization) and automated 90-day renewals '
        'with zero administrative toil, whereas self-managed certificates allow enterprise teams to upload custom enterprise certificates, requiring automated CI/CD monitoring to prevent expiration outages. '
        '(4) <strong class="side-heading">SSL Policies:</strong> Architects attach SSL policies to Target HTTPS Proxies to enforce minimum TLS versions (<samp>TLS 1.2</samp> or <samp>TLS 1.3</samp>) '
        'and restrict allowed cipher suites (<samp>RESTRICTED</samp> or <samp>MODERN</samp>), preventing protocol downgrade attacks and maintaining PCI-DSS compliance. '
        '(5) <strong class="side-heading">Backend Encryption Modes:</strong> Architects choose between: (a) Edge Termination with HTTP Backend (decrypted traffic routed over Google’s private Andromeda SDN fabric); '
        '(b) Edge Termination with Backend Re-Encryption (load balancer initiates a separate TLS handshake to backend instances with backend certificate verification); and '
        '(c) L4 Passthrough (Network Load Balancers route raw TCP segments directly to backend VMs without decrypting, where application containers terminate TLS directly).',
        'In multi-tenant cloud environments, managing thousands of certificates across microservice domains requires automated lifecycle orchestration. '
        'Architects must implement automated issuance via ACME protocols or cloud-native certificate managers, preventing manual renewal failures '
        'that account for over thirty percent of unplanned enterprise outages.',
        'Google Cloud Certificate Manager provides domain-based certificate assignment and selection for supported Google Cloud load balancers; wildcard eligibility needs the specific certificate and authorization documentation. '
        'Benefits documents domain-based certificate selection and DNS-based or load-balancer-based domain authorization, while Supported TLS certificates documents CA Service pools as issuers. '
        'These sections support certificate lifecycle design but do not establish split-horizon authorization or arbitrary internal sidecar mTLS integration; validate the selected supported load balancer and authorization path separately.',
        ['rfc8446', 'gcp_cert_mgr', 'gcp_cert_benefits']
    )
]

T2_TECH = discussion(
    [
        "TLS 1.3 Handshake Protocol and 1-RTT Cryptographic Exchange (RFC 8446)",
        "X.509 PKI Trust Architecture and Certificate Validation Chains (RFC 5280)",
        "Certificate Revocation and Verification Mechanisms: CRLs vs OCSP Stapling",
        "Enterprise TLS Governance, ALPN Negotiation, and Google Cloud Certificate Management"
    ],
    T2_SUBTOPICS,
    "An enterprise client initiates an HTTPS connection to an internal service endpoint. The client transmits a ClientHello with an ephemeral x25519 "
    "key share and an ALPN extension advertising 'h2'. The Google Cloud Load Balancer selects TLS 1.3, returns its ServerHello with matching key share, "
    "and delivers an encrypted certificate chain issued by an internal CA with full Subject Alternative Name matching, achieving 1-RTT encrypted setup.",
    "Validating certificate chains locally proves cryptographic signature mathematics and hostname parsing logic, but does not simulate distributed "
    "CA revocation infrastructure availability or real-time OCSP responder latency under high load."
)

# ==============================================================================
# TOPIC 03: MTU and MSS clamping
# ==============================================================================
MTU_FLOW_SVG = flow_svg('d004-pmtud-mss', 'Path MTU Discovery and TCP MSS Clamping Packet Traversal', [
    ('Host Egress', ('App sends 1500B frame', 'Sets DF=1 in IP header'), 'client'),
    ('VPC Switch', ('Forwards full frame', 'Approaches tunnel egress'), 'switch'),
    ('VPN Gateway', ('Inspects IPSec tunnel', 'Tunnel MTU is 1400B'), 'vpn'),
    ('MTU Drop & ICMP', ('Drops oversized frame', 'Generates ICMP Type 3'), 'firewall'),
    ('PMTUD Feedback', ('Sender receives ICMP', 'Adjusts Path MTU 1400'), 'router'),
    ('Clamped Flow', ('SYN clamped MSS 1360', 'Payloads traverse clean'), 'outcome'),
], [
    '1. Transmit 1500B (DF=1)',
    '2. Forward to gateway',
    '3. Exceeds 1400B MTU',
    '4. ICMP Type 3 Code 4',
    '5. Clamped MSS 1360',
], 'Path MTU Discovery failure and TCP MSS clamping packet traversal across an encapsulated network boundary.')

T3_SUBTOPICS = [
    subtopic(
        "Maximum Transmission Unit, IP Packet Framing, and MSS Calculations",
        f'The <strong class="keyword">Maximum Transmission Unit (MTU)</strong> specifies the maximum size of an IP packet (including IP headers and payload) '
        'that can be transmitted across a given physical or virtual network interface without being fragmented. On standard Ethernet networks, the default '
        'MTU is 1500 bytes. The <strong class="keyword">Maximum Segment Size (MSS)</strong> is a transport-layer parameter exchanged in TCP SYN packets '
        'that defines the maximum quantity of unfragmented TCP user payload a host is willing to receive in a single segment. The mathematical relationship '
        'between MTU and MSS is strictly governed by header overhead: for standard IPv4 (which has a 20-byte base IP header and a 20-byte base TCP header), '
        'the MSS formula is <samp>MSS = MTU - 20 (IP) - 20 (TCP) = MTU - 40</samp>. Thus, on an interface with MTU 1500, IPv4 TCP MSS is 1460 bytes. '
        'For IPv6 (which has a 40-byte fixed base IP header and a 20-byte base TCP header), the formula is <samp>MSS = MTU - 40 (IPv6) - 20 (TCP) = MTU - 60</samp>, '
        'resulting in an MSS of 1440 bytes on a 1500-byte MTU network. If TCP timestamps (RFC 7323) are enabled, an additional 12 bytes of TCP options '
        'are consumed, further reducing usable application payload.',
        'Cloud architects must calculate MTU and MSS precisely when designing multi-tier VPC networks and interconnect topologies. When packets exceed '
        'the path MTU, intermediate routers must either fragment the packet into multiple IP fragments or drop it. IP fragmentation introduces severe '
        'drawbacks: it multiplies packet processing overhead on routers, increases loss probability (losing one fragment invalidates the entire reassembly), '
        'and IPv6 explicitly forbids intermediate routers from performing in-flight fragmentation altogether.',
        'Google Cloud VPC networks support configurable MTUs of 1460, 1500, and 8896 (jumbo frames). The legacy default for GCP VPCs is 1460 bytes '
        'according to Valid VPC network MTU sizes; that section does not state why this default was chosen. With base IPv4/TCP headers this yields MSS 1420 bytes. Modern GCP VPC networks '
        'can be created with MTU 1500 to match standard internet Ethernet frames, or MTU 8896 to maximize throughput between Compute Engine instances '
        'with compatible connected paths; communication to Google APIs and services has separate path constraints documented on the MTU page.',
        ['rfc1191', 'gcp_vpc_mtu', 'gcp_mtu_apis']
    ),
    subtopic(
        "Path MTU Discovery (PMTUD) and ICMP Fragmentation Feedback (RFC 1191)",
        f'{keyword("Path MTU Discovery")} (PMTUD, RFC 1191) is a standardized mechanism that dynamically determines the lowest MTU link across an '
        "end-to-end network path between two hosts. The transmitting host sets the <strong class=\"keyword\">Don't Fragment (DF)</strong> bit in the IP header "
        'of all outgoing packets. When an intermediate router receives a packet with DF=1 that is larger than the MTU of the outbound next-hop link, '
        'the router is strictly forbidden from fragmenting the packet; instead, the router must drop the packet and immediately generate an '
        '<strong class="keyword">ICMP Type 3 Code 4</strong> error message (<samp>Destination Unreachable: Fragmentation Needed and DF set</samp>) back to the sender. '
        'Crucially, RFC 1191 mandates that the router include the MTU of the restrictive next-hop link in the ICMP header. Upon receiving this message, '
        'the sender’s operating system kernel caches the lower Path MTU for that destination IP and dynamically reduces its TCP MSS for that connection, '
        'retransmitting the payload in smaller segments that traverse the entire path without fragmentation.',
        'PMTUD is an elegant control-plane feedback loop, but it possesses a critical operational vulnerability: it relies entirely on the successful '
        'delivery of ICMP Type 3 Code 4 messages across every intermediate network and firewall between destination and sender.',
        'Google Cloud VPC networks and Cloud Routers automatically generate and honor ICMP fragmentation needed feedback. In GCP VPC firewall rules, '
        'implied ingress and egress rules allow internal ICMP messages; however, architects authoring custom restrictive firewall policies must never '
        'blindly block ICMP traffic, as doing so breaks PMTUD.',
        ['rfc1191', 'gcp_vpc_mtu']
    ) + MTU_FLOW_SVG,
    subtopic(
        "Path MTU Black Holes, Firewall ICMP Filtering, and TLS Stall Symptoms",
        f'A <strong class="keyword">Path MTU black hole</strong> occurs when an intermediate link has a lower MTU than the sending host, packets are sent with '
        'DF=1, but the intermediate router’s ICMP Type 3 Code 4 feedback messages are dropped by an overly aggressive perimeter firewall, security group, '
        'or misconfigured ISP router along the return path. Because the sender never receives the ICMP error, it remains completely unaware that its packets '
        'are being dropped. The connection exhibits a notoriously deceptive and baffling symptom: small packets (such as TCP 3-way handshakes, ping probes, '
        'and HTTP GET requests consisting of only a few hundred bytes) traverse the network and receive immediate replies because they fit within the '
        'restrictive MTU. However, the instant the server transmits a large data payload—such as an X.509 certificate chain during a TLS handshake, '
        'a large POST request, or a bulk file transfer—the packet exceeds the bottleneck MTU and is silently dropped. The sender retransmits the oversized packet '
        'until the TCP connection eventually times out and dies, while monitoring health checks report the service as completely healthy.',
        'Cloud architects diagnosing intermittent connection hangs or TLS handshake stalls on hybrid cloud tunnels must immediately suspect PMTUD black holes. '
        'A telltale diagnostic signature is a connection that connects instantly on port 443, begins the TLS handshake, and then hangs indefinitely '
        'during <samp>ServerHello / Certificate</samp> exchange because the certificate payload exceeds 1400 bytes.',
        'To diagnose PMTUD black holes in Google Cloud environments, architects inspect Cloud VPN tunnel packet drop counters and use Linux diagnostic '
        'utilities (<kbd>ping -M do -s &lt;size&gt; &lt;destination&gt;</kbd>) to experimentally locate the exact MTU threshold where packets cease passing.',
        ['rfc1191', 'gcp_vpc_mtu']
    ),
    subtopic(
        "TCP MSS Clamping Mechanics and Google Cloud VPC MTU Engineering",
        f'To permanently prevent Path MTU black holes without relying on fragile end-to-end ICMP feedback, network engineers implement '
        '<strong class="keyword">TCP MSS clamping</strong> at network boundaries and VPN gateways. MSS clamping is a specialized stateful packet rewriting '
        'technique: as TCP SYN and SYN-ACK packets traverse a gateway or router interface, the router inspects the TCP MSS option field in the TCP header. '
        'If the negotiated MSS value is larger than the known MTU of the outgoing link minus IP and TCP header overhead, the router rewrites the MSS option '
        'in-flight to match the bottleneck link capacity before forwarding the packet. Because the MSS value is adjusted during the initial connection handshake, '
        'both client and server automatically constrain their maximum packet sizes to fit within the restrictive tunnel, completely bypassing the need for '
        'PMTUD and eliminating the risk of black hole drops.',
        'In hybrid cloud architectures connecting on-premises data centers to Google Cloud via Cloud VPN (IPSec), encapsulation overhead is inevitable. '
        'Standard IPSec ESP tunneling adds approximately 56 to 76 bytes of encapsulation headers (ESP header, IV, padding, ESP trailer, and outer IP header). '
        'If an on-premises host transmits a 1500-byte frame into an IPSec tunnel, the encapsulated frame expands to 1560+ bytes, which exceeds the physical '
        'carrier link MTU. Cloud architects configure MSS clamping on edge firewalls and VPN concentrators to clamp TCP MSS to 1360 bytes, ensuring '
        'seamless hybrid traversal.',
        'Cloud VPN distinguishes gateway MTU from payload MTU; the documented payload values depend on ciphers, gateway IP version, NAT-T and HA VPN over Interconnect. '
        'Do not reuse the VPC 1460 default as a universal VPN payload MTU or assume MSS 1420. When designing VPC networks connected via Cloud Interconnect or HA VPN, architects ensure that instance MTUs match the path or '
        'that MSS clamping is active on the on-premises customer gateway router.',
        ['rfc9293', 'gcp_vpc_mtu', 'gcp_vpn_mtu', 'gcp_vpn_payload']
    )
]

T3_TECH = discussion(
    [
        "Maximum Transmission Unit, IP Packet Framing, and MSS Calculations",
        "Path MTU Discovery (PMTUD) and ICMP Fragmentation Feedback (RFC 1191)",
        "Path MTU Black Holes, Firewall ICMP Filtering, and TLS Stall Symptoms",
        "TCP MSS Clamping Mechanics and Google Cloud VPC MTU Engineering"
    ],
    T3_SUBTOPICS,
    "An application on a Compute Engine VM in a 1460-byte MTU VPC initiates a large database backup to an on-premises server over an IPSec Cloud VPN tunnel. "
    "For this illustrative path, the customer gateway clamps TCP SYN MSS to 1360 bytes; this is a configured example, not a Cloud VPN default. The application kernel restricts data payloads to 1360 bytes; with base IP, "
    "TCP headers (40 bytes combined) and the supplied 60-byte tunnel overhead, the model totals 1460 bytes. Actual cipher and NAT-T overhead must be checked against the documented VPN payload limit before predicting traversal without fragmentation or drops.",
    "Mathematical MSS calculations accurately model protocol encapsulation overheads, but cannot predict unadvertised carrier encapsulation (such as QinQ VLAN "
    "tagging or MPLS label stacks) introduced by transit telecommunication providers that silently reduces physical line MTU below standard thresholds."
)

# ==============================================================================
# TOPIC 04: NAT (SNAT/DNAT) for private outbound
# ==============================================================================
NAT_FLOW_SVG = flow_svg('d004-snat-dnat', 'VPC Private Outbound: SNAT and Return DNAT Packet Lifecycle', [
    ('Private VM', ('VM: 10.0.1.5:49152', 'Initiates TCP SYN out'), 'client'),
    ('VPC Route Table', ('Evaluates 0.0.0.0/0', 'Internet gateway next hop'), 'router'),
    ('Cloud NAT SNAT', ('Allocates port 32001', 'Rewrites src to public'), '../gcp/legacy/cloud-nat'),
    ('Public Internet', ('Forwards packet to', 'Destination 203.0.113.1'), 'internet'),
    ('Remote Server', ('Processes SYN packet', 'Replies with SYN-ACK'), 'server'),
    ('Return DNAT', ('Matches 5-tuple state', 'Delivers to 10.0.1.5'), 'outcome'),
], [
    '1. SYN 10.0.1.5:49152',
    '2. Apply source NAT',
    '3. SNAT: 203.0.113.10:32001',
    '4. Traverse internet',
    '5. DNAT state lookup',
], 'Outbound Source NAT (SNAT) and return Destination NAT (DNAT) 5-tuple packet translation lifecycle. Functional translation points are shown; Cloud NAT is distributed software, not a proxy VM or an appliance next hop.')

T4_SUBTOPICS = [
    subtopic(
        "NAT Terminology and Architectural Classifications: SNAT, DNAT, and NAPT/PAT (RFC 3022)",
        f'{keyword("Network Address Translation (NAT)")} (RFC 3022) is an IP routing technique that dynamically alters source or destination addresses '
        'within packet headers as they traverse a network boundary. In cloud architecture, NAT is categorized into two foundational directions: '
        '<strong class="keyword">Source NAT (SNAT)</strong> and <strong class="keyword">Destination NAT (DNAT)</strong>. SNAT rewrites the source IP address '
        '(and source port) of outbound packets originating from private internal subnets (RFC 1918) to a public IP owned by the NAT gateway, allowing private '
        'instances to access external internet services while masking internal topology. When external endpoints respond, the NAT gateway performs reverse DNAT, '
        'translating the destination IP/port back to the original internal client. Conversely, pure DNAT rewrites the destination IP of incoming packets, '
        'typically used by public load balancers to distribute inbound traffic across private backend instances. The prevailing enterprise implementation '
        'is <strong class="keyword">Network Address Port Translation (NAPT)</strong>, also called Port Address Translation (PAT), where thousands of private internal '
        'IPs are multiplexed across a small pool of public IP addresses by assigning unique ephemeral Layer 4 source ports.',
        'Cloud architects use NAT to enforce strict zero-trust network perimeters. Best-practice enterprise architecture dictates that compute instances '
        '(virtual machines, container nodes, and database servers) must never be assigned external public IP addresses. Omitting public IPs eliminates '
        'direct inbound attack surfaces from the internet. SNAT gateways provide the necessary egress capability so private instances can download '
        'security patches, pull container images, and communicate with external partner APIs without accepting inbound connections.',
        'In Google Cloud, Private Google Access allows private VMs without external IPs to reach Google APIs (Cloud Storage, BigQuery) internally '
        'without traversing NAT, while Google Cloud NAT provides managed outbound SNAT for all non-Google external internet traffic.',
        ['rfc3022', 'gcp_cloud_nat', 'gcp_nat_ports', 'gcp_nat_dynamic']
    ) + NAT_FLOW_SVG,
    subtopic(
        "NAT State Table Mechanics, 5-Tuple Tracking, and Port Allocation Limits",
        f'A NAPT gateway is a stateful network device that maintains an in-memory <strong class="keyword">NAT state table</strong>. Each outbound connection '
        'is tracked as a <strong class="keyword">5-tuple</strong> consisting of: <samp>(Source IP, Source Port, Destination IP, Destination Port, Protocol)</samp>. '
        'When a private VM initiates a connection, the NAT gateway allocates an unused source port from its public IP pool, rewrites the packet header, '
        'and records the mapping in its translation table alongside connection state timers (TCP established, TCP transitory, UDP timeout). A single IPv4 address '
        'possesses a theoretical maximum of 65,535 ephemeral ports; in practice, ports below 1024 are reserved, leaving approximately 64,000 usable ports per public IP. '
        'If a cluster of private VMs initiates more concurrent outbound connections than the gateway has available source ports, the gateway experiences '
        '<strong class="keyword">NAT port exhaustion</strong>: subsequent outbound TCP SYN packets are silently dropped or rejected, resulting in application connection '
        'timeouts and cascading API failures.',
        'Architects must calculate NAT port capacity using explicit mathematical models. If an enterprise deploys 500 microservice VMs and each VM initiates '
        'an average of 200 concurrent outbound connections to third-party webhooks and SaaS endpoints, total concurrent port demand is 100,000 ports. '
        'A single public NAT IP (providing 64,000 ports) is mathematically insufficient and will trigger port exhaustion drops; the architect must allocate '
        'at least two public IPs, or configure dynamic port allocation.',
        'Google Cloud NAT provides configurable port reservation models. Architects configure <samp>Minimum ports per VM</samp> (64 in this supplied static-allocation example; allocation-mode defaults differ) and can enable '
        '<strong class="keyword">Dynamic Port Allocation</strong>, which allows Cloud NAT to automatically scale the ports assigned to an individual VM from '
        'the minimum threshold up to a configured maximum (e.g. 1024 ports) based on real-time traffic demand.',
        ['rfc3022', 'gcp_cloud_nat', 'gcp_nat_benefits', 'gcp_nat_mapping', 'gcp_nat_logs']
    ),
    subtopic(
        "Private Outbound Egress Design and Defense-in-Depth Security Boundaries",
        f'Designing secure outbound internet egress requires balancing operational agility with data exfiltration prevention. While SNAT provides '
        'network-layer translation, it does not inspect application-layer payloads or restrict destination domain names: any private VM with SNAT egress '
        'can transmit data to any public IP on the internet. In high-security environments, cloud architects implement a defense-in-depth egress boundary '
        'by combining Cloud NAT with <strong class="keyword">Forward Proxy appliances</strong> (such as Squid or Envoy) or Google Cloud Secure Web Proxy. '
        'Under this model, private VMs route their outbound HTTPS traffic through an authenticated forward proxy that enforces TLS inspection, domain allowlisting '
        '(e.g., permitting access only to <samp>*.packages.example.test</samp> or specific package repositories), and audit logging, while the proxy itself egresses '
        'to the internet through Cloud NAT.',
        'Furthermore, architects must carefully isolate egress paths across VPC networks. In multi-tenant enterprise architectures utilizing Shared VPC, '
        'Cloud NAT gateways can be centralized in the host project to service multiple service project subnets, or decentralized into regional per-tier subnets '
        'to prevent "noisy neighbor" port exhaustion where a runaway batch processing job in one project starves critical payment processing VMs in another.',
        'Google Cloud NAT integrates directly with Cloud Monitoring to expose port utilization metrics, including <samp>router.googleapis.com/nat/nat_allocation_failed</samp> '
        'and <samp>compute.googleapis.com/nat/open_connections</samp>, allowing architects to build alerting triggers that fire before port exhaustion reaches critical levels.',
        ['rfc1918', 'gcp_cloud_nat', 'gcp_nat_metrics', 'gcp_nat_gateway_metrics', 'gcp_nat_benefits']
    ),
    subtopic(
        "Google Cloud NAT Architecture: Andromeda Distributed Translation and Port Management",
        f'Unlike traditional on-premises networks or competing cloud architectures that rely on centralized virtual appliances or managed NAT instances, '
        '<strong class="keyword">Google Cloud NAT</strong> is completely software-defined and distributed. Cloud NAT is built directly into Google’s '
        '<strong class="keyword">Andromeda network virtualization stack</strong>. When an architect configures a Cloud NAT gateway, Google Cloud does not deploy '
        'a proxy VM or appliance. The Architecture section states that Cloud NAT configures Andromeda to provide SNAT and DNAT for established response packets. '
        'Cloud Router holds NAT configuration as the control plane (Benefits); these sections do not specify host-kernel switch programming or a precise egress hook. '
        'Do not infer a line-rate, zero-latency or unlimited-capacity guarantee: port allocation, VM bandwidth and configured address capacity remain design constraints.',
        'Because Cloud NAT is software-defined, it supports advanced port allocation algorithms: (1) <strong class="keyword">Endpoint-Independent Mapping (EIM)</strong> '
        'guarantees that multiple concurrent outbound connections from the same private IP:port to different external destinations reuse the exact same external '
        'public NAT IP:port mapping, facilitating NAT traversal and STUN/TURN protocols; and (2) <strong class="keyword">Port Reservation per VM</strong> ensures '
        'that each VM receives a guaranteed slice of ports that cannot be stolen by neighboring VMs.',
        'Google Cloud NAT supports configurable logging of translated connections and errors (Logging states its limits; this is not a guarantee of every connection) via Cloud Logging. Architects can configure NAT logging to capture all translated '
        'flows or errors-only (logging dropped connections due to port exhaustion), providing crucial audit evidence for compliance and incident forensics.',
        ['rfc3022', 'gcp_cloud_nat']
    )
]

T4_TECH = discussion(
    [
        "NAT Terminology and Architectural Classifications: SNAT, DNAT, and NAPT/PAT (RFC 3022)",
        "NAT State Table Mechanics, 5-Tuple Tracking, and Port Allocation Limits",
        "Private Outbound Egress Design and Defense-in-Depth Security Boundaries",
        "Google Cloud NAT Architecture: Andromeda Distributed Translation and Port Management"
    ],
    T4_SUBTOPICS,
    "A private GKE node running on 10.128.0.4 without an external IP needs to download an operating system security patch from an external repository at "
    "198.51.100.25:443. In this illustrative translation model, outbound TCP SYN processing assigns documentation NAT IP 203.0.113.5 and port 34100 from the Cloud NAT pool, "
    "rewrites the packet header, and forwards it to the internet. Return traffic matches the 5-tuple state table and is translated back to 10.128.0.4 seamlessly.",
    "NAT state table simulations demonstrate 5-tuple translation and port saturation mechanics, but do not capture remote provider firewall drops or external "
    "carrier rate-limiting algorithms that throttle requests originating from heavily multiplexed public NAT IP addresses."
)

# ==============================================================================
# TOPIC 05: Routing basics
# ==============================================================================
BGP_FLOW_SVG = flow_svg('d004-bgp-routing', 'BGP Route Advertisement, Evaluation, and Packet Forwarding', [
    ('On-Prem Router', ('Advertises 10.0.0.0/16', 'Sets AS_PATH and MED'), 'router'),
    ('Interconnect', ('Carries eBGP peering', 'Transmits UPDATE msg'), '../gcp/legacy/cloud-interconnect'),
    ('Cloud Router', ('Evaluates BGP paths', 'Installs best into RIB'), '../gcp/legacy/cloud-router'),
    ('VPC FIB Table', ('Selects applicable route', 'Calculates next hop'), 'switch'),
    ('Compute Engine VM', ('Transmits data packet', 'LPM lookup on dst IP'), '../gcp/core/compute-engine'),
    ('Egress Traffic', ('Forwards via Interconnect', 'Latency must be measured'), 'outcome'),
], [
    '1. BGP UPDATE (AS 65001)',
    '2. eBGP session sync',
    '3. Select best path',
    '4. Create VPC route',
    '5. LPM packet egress',
], 'Illustrative BGP-4 route advertisement followed by data forwarding. Cloud Router creates dynamic routes rather than forwarding packets; the local LPM model does not implement every GCP route-selection stage.')

T5_SUBTOPICS = [
    subtopic(
        "Routing Fundamentals: Forwarding Information Base, Longest Prefix Match, and Metric Priority",
        f'{keyword("Routing")} is the control-plane and data-plane mechanism by which network devices forward IP packets toward their destination across '
        'interconnected networks. Routers maintain two distinct data structures: the <strong class="keyword">Routing Information Base (RIB)</strong>, '
        'which stores all routes learned via static configuration and dynamic routing protocols, and the <strong class="keyword">Forwarding Information Base (FIB)</strong>, '
        'which represents the optimized, hardware-compiled lookup table used by the data plane to switch packets at line rate. When a router evaluates where to forward '
        'a packet, it executes the <strong class="keyword">Longest Prefix Match (LPM)</strong> algorithm against the destination IP address: the route with the most '
        'specific subnet mask (longest prefix length) always takes absolute precedence over less specific routes, regardless of administrative distance or protocol metric. '
        'For example, if a routing table contains entries for <samp>0.0.0.0/0</samp> (default gateway), <samp>10.0.0.0/8</samp> (corporate WAN), and <samp>10.1.5.0/24</samp> '
        '(database subnet), a packet destined for <samp>10.1.5.22</samp> will strictly match and forward via the <samp>10.1.5.0/24</samp> next hop. Only when two routes '
        'have identical prefix lengths does the router evaluate administrative distance (route priority) and routing metrics to select the active next hop.',
        'Cloud architects must master LPM to design predictable network segregation, hybrid cloud bypasses, and security inspection routes. A common design pattern '
        'is overriding a broad system-generated internet route (<samp>0.0.0.0/0</samp>) with a pair of more specific RFC 1918 routes (<samp>10.0.0.0/8</samp> and '
        '<samp>172.16.0.0/12</samp>) pointing toward an on-premises Cloud Interconnect or a perimeter next-generation firewall appliance.',
        'Google Cloud VPC routing uses staged routing order, not LPM across all route types: special paths and policy-based routes precede subnet and custom routes. For applicable custom-route evaluation, priorities and specificity must be evaluated in the documented order; route priority is an integer from 0 to 65535, where lower numerical values '
        'represent higher priority. ECMP is available for eligible remaining next hops under the route-selection rules; identical destination and priority alone are not a universal guarantee. '
        'The local LPM script deliberately models a generic table and does not implement every GCP routing category, selection mode or next-hop eligibility condition.',
        ['rfc4271', 'gcp_vpc_routes', 'gcp_route_types']
    ),
    subtopic(
        "Static Routing vs Dynamic Routing: Administrative Overhead, Convergence, and Failure Recovery",
        f'Network routing architectures are divided into <strong class="keyword">static routing</strong> and <strong class="keyword">dynamic routing</strong>. '
        'Static routing requires manual entry of destination CIDR blocks and corresponding next-hop IP addresses or interfaces. While static routing is simple '
        'and introduces zero protocol overhead, it has fatal operational limitations in enterprise environments: it cannot detect remote intermediate link failures, '
        'requires manual reconfiguration during network changes, and scales poorly as VPCs and on-premises subnets proliferate. In contrast, dynamic routing uses '
        'routing protocols where routers automatically exchange reachability information, monitor peer health via keep-alive heartbeats, and autonomously recalculate '
        'forwarding paths when links fail. The time required for all routers across an enterprise network to reach a consistent, loop-free routing state following '
        'a topology change is known as <strong class="keyword">convergence time</strong>.',
        'For cloud architects, choosing between static and dynamic routing represents a foundational trade-off between configuration simplicity and operational '
        'resilience. Static routes in cloud environments often create "black holes": if an on-premises firewall goes offline, a static route in GCP pointing to '
        'that firewall continues forwarding packets into the void until an engineer manually edits the cloud route table. Dynamic routing automatically withdraws '
        'unreachable prefixes within seconds of link loss, providing automated failover.',
        'Google Cloud provides custom static routes (supporting next-hop IP, next-hop gateway, next-hop instance, or next-hop VPN tunnel) for simple topologies, '
        'while dynamic routes are created from Cloud Router learned routes. Cloud Router supports Cloud VPN and Cloud Interconnect as documented; choose the specific connectivity product’s supported routing mode rather than claiming a universal production mandate. '
        'The route type table distinguishes static next hops from local dynamic next hops and their applicability.',
        ['rfc4271', 'gcp_vpc_routes', 'gcp_route_types']
    ),
    subtopic(
        "Border Gateway Protocol (BGP-4) Mechanics: Autonomous Systems, eBGP/iBGP, and Path Attributes (RFC 4271)",
        f'The <strong class="keyword">Border Gateway Protocol</strong> (BGP-4, RFC 4271) is the de facto standard exterior gateway protocol powering internet '
        'routing and enterprise hybrid cloud connectivity. BGP operates as a <strong class="keyword">path-vector protocol</strong> that exchanges reachability '
        'between independent administrative routing domains known as <strong class="keyword">Autonomous Systems (AS)</strong>, each identified by an '
        '<strong class="keyword">Autonomous System Number (ASN)</strong>. BGP sessions established between routers in different Autonomous Systems are termed '
        '<strong class="keyword">eBGP</strong> (External BGP), while sessions between routers within the same AS are termed <strong class="keyword">iBGP</strong> (Internal BGP). '
        'Unlike interior gateway protocols (such as OSPF) that evaluate simple link-cost metrics, BGP evaluates a rich set of <strong class="keyword">path attributes</strong> '
        'to enforce sophisticated routing policies. Crucial attributes include: (1) <strong class="keyword">AS_PATH</strong>, an ordered list of ASNs through which the route '
        'has propagated, which serves both as a loop-prevention mechanism (a router immediately drops an update containing its own ASN) and a primary metric '
        '(shorter AS_PATH lengths are preferred); and (2) <strong class="keyword">Multi-Exit Discriminator (MED)</strong>, an optional metric advertised by an external AS '
        'to indicate which of multiple ingress links should be preferred for inbound traffic.',
        'Understanding BGP path selection order is essential for hybrid cloud architects. When receiving multiple advertisements for the same prefix, BGP evaluates '
        'attributes in a strict hierarchical order: highest Local Preference -> shortest AS_PATH length -> lowest Origin code -> lowest MED -> eBGP over iBGP -> lowest IGP metric to next hop. '
        'Architects use <strong class="keyword">AS-path prepending</strong> (artificially inserting duplicate ASNs into the AS_PATH on a backup link) and MED tuning '
        'to establish deterministic active/passive or active/active load balancing across redundant hybrid cloud connections.',
        'In Google Cloud, Cloud Router manages BGP sessions over Cloud VPN and Cloud Interconnect, using RFC 6996 private ASNs (such as 64512–65534 in 16-bit or '
        '4200000000–4294967294 in 32-bit) to peer with on-premises edge routers.',
        ['rfc4271', 'gcp_cloud_router', 'gcp_routing_mode']
    ) + BGP_FLOW_SVG,
    subtopic(
        "Google Cloud VPC Routing Architecture: System Routes, Custom Static Routes, and Cloud Router Dynamic BGP",
        f'Google Cloud VPC routing represents a global, software-defined control plane that coordinates packet forwarding across all worldwide regions. '
        'Every GCP VPC network is provisioned with default <strong class="keyword">system-generated routes</strong>: a local subnet route for each subnet CIDR block '
        'allowing direct instance-to-instance communication across regions without gateways, and a default route (<samp>0.0.0.0/0</samp>) pointing to the default '
        'internet gateway. In addition to system routes, architects can define <strong class="keyword">custom static routes</strong> to steer traffic toward specific '
        'network virtual appliances (NVAs) or VPN tunnels. However, the cornerstone of enterprise hybrid connectivity is <strong class="keyword">Google Cloud Router</strong>, '
        'a fully managed, serverless control plane that establishes dynamic BGP peering sessions with on-premises routers, third-party clouds, or Cloud Interconnect spokes.',
        'A critical architectural setting in GCP VPC design is the <strong class="keyword">Dynamic Routing Mode</strong>, which can be configured as either '
        '<strong class="keyword">Regional</strong> or <strong class="keyword">Global</strong>. Under Regional Dynamic Routing, Cloud Router only advertises subnets located '
        'in its own local region to on-premises BGP peers, and routes learned from on-prem are only programmed into the VPC routing table for VMs in that same region. '
        'Under Global Dynamic Routing, Cloud Router advertises all subnets across all worldwide regions to on-premises BGP peers, and routes learned over BGP in one region '
        'are dynamically programmed into the routing tables of all instances across every global region. If an on-premises link in us-east1 fails, global routing '
        "can select an eligible dynamic next hop in another region; verify route convergence, filters and path reachability before predicting cross-region failover.",
        'Cloud Router Key features documents Bidirectional Forwarding Detection (BFD, RFC 5880) support. It does not establish a universal 300-millisecond physical-link detection time or end-to-end recovery bound; '
        'failure detection, BGP convergence and data-plane restoration are separate intervals that need measurements for the chosen topology.',
        ['rfc4271', 'gcp_cloud_router', 'gcp_routing_mode']
    )
]

T5_TECH = discussion(
    [
        "Routing Fundamentals: Forwarding Information Base, Longest Prefix Match, and Metric Priority",
        "Static Routing vs Dynamic Routing: Administrative Overhead, Convergence, and Failure Recovery",
        "Border Gateway Protocol (BGP-4) Mechanics: Autonomous Systems, eBGP/iBGP, and Path Attributes (RFC 4271)",
        "Google Cloud VPC Routing Architecture: System Routes, Custom Static Routes, and Cloud Router Dynamic BGP"
    ],
    T5_SUBTOPICS,
    "An enterprise establishes dual 10 Gbps Cloud Interconnect links between its Chicago data center and Google Cloud VPC in us-central1. "
    "Cloud Router establishes eBGP peering with on-premises Cisco ASR edge routers. The on-premises router advertises 10.200.0.0/16 with MED 100 on "
    "Interconnect-1 and MED 200 on Interconnect-2. Cloud Router selects Interconnect-1 as primary, creating VPC dynamic routes for the applicable routing mode rather than directly forwarding traffic; the cited section does not describe per-hypervisor FIB programming across regional "
    "hypervisors. BFD support is documented, but this illustrative design must measure convergence and failover rather than promise a three-second recovery.",
    "BGP routing table simulations evaluate path-vector attribute decisions deterministically, but do not capture trans-oceanic fiber propagation delays, "
    "optical link degradation, or BGP route flap damping penalties enforced by autonomous internet transit providers."
)

# ==============================================================================
# PART 3: INCIDENTS / PROBLEMS
# ==============================================================================

# Topic 01 Incident
P1_CASE = case(
    scenario="Internal API gateway upgrading from HTTP/1.1 to HTTP/2 encounters 502 Bad Gateway errors on backend requests with uppercase headers.",
    impact="Customer checkout transactions fail intermittently; regional store catalog lookups drop by 22% during peak operating hours.",
    constraints="Cannot roll back entire gateway cluster without disconnecting active customer shopping sessions; must preserve custom header propagation.",
    records=(
        '2026-10-04T08:14:02.128Z [ingress-envoy-01] "POST /api/v1/checkout HTTP/2" 502 - 0 142 4 - '
        '"-" "MobileApp/4.2" "9a8b7c6d" "api.retailer.example.test" "10.128.0.45:8443" - '
        'response_flags=PROTOCOL_ERROR downstream_peer_reset=false upstream_reset_reason="protocol_error: '
        'uppercase characters in header name [X-Customer-Region]"'
    ),
    root="RFC 9113 section 8.2.1 mandates that all HTTP/2 header field names must be lowercase. The legacy client forwarded uppercase headers, which the strict HTTP/2 parser rejected.",
    diagnostics=[
        "Inspect Envoy ingress proxy access logs for HTTP 502 status codes and protocol error flags.",
        "Reproduce the request using curl with --http2 and verbose header output to inspect exact transmitted header casing.",
        "Compare upstream client request header formatting against downstream HTTP/2 ingress gateway RFC 9113 compliance requirements."
    ],
    fixes=[
        "Configure ingress gateway header transformation to automatically downcase all header names prior to HTTP/2 framing.",
        "Update mobile client SDK and API client libraries to enforce standard lowercase HTTP header conventions across all endpoints."
    ],
    verify="Execute checkout request with mixed-case headers through the updated ingress proxy and verify HTTP 200 OK with valid stream allocation.",
    residual="Client requests containing invalid pseudo-headers or prohibited non-ASCII characters may still trigger stream resets; monitor downstream reset counters.",
    enabled=True,
    diagram=(
        "Client sends HTTP/2 request with uppercase headers",
        "Gateway forwards unnormalized headers to strict proxy",
        "Proxy resets stream with PROTOCOL_ERROR (502)",
        "Normalize all headers to lowercase at edge ingress",
        "Clean stream delivery; 200 OK returned"
    ),
    facts="Illustrative fixture ingress log lists HTTP 502 with response_flag PROTOCOL_ERROR and upstream reset reason citing uppercase characters in header name.",
    inference="Envoy proxy enforced strict RFC 9113 HTTP/2 compliance, treating uppercase header field names as protocol violations that mandate stream resets.",
    expected="Edge proxy normalizes all headers to lowercase before framing; backend microservices process transactions successfully with HTTP 200 OK."
)

# Topic 02 Incident
P2_CASE = case(
    scenario="Newly deployed microservice client fails TLS handshake with hostname mismatch error when connecting via private DNS alias.",
    impact="Analytics event pipeline stalls; edge telemetry queues fill to 98% capacity, risking unrecoverable data loss.",
    constraints="Cannot bypass TLS verification using insecure mode in production; internal PKI governance strictly forbids self-signed leaf certificates.",
    records=(
        "2026-10-04T09:22:15.412Z [analytics-collector] ERROR: Connection failed to https://analytics.example.test:8443/collect\n"
        "Traceback (most recent call last):\n"
        "  File \"collector.py\", line 84, in post_event\n"
        "    resp = session.post(url, json=payload, timeout=5)\n"
        "  File \"requests/sessions.py\", line 589, in post\n"
        "requests.exceptions.SSLError: HTTPSConnectionPool(host='analytics.example.test', port=8443): "
        "Max retries exceeded with url: /collect (Caused by SSLError(CertificateError(\"hostname 'analytics.example.test' "
        "doesn't match either of 'worker-node-04.example.test'\")))"
    ),
    root="The server leaf certificate contained only Common Name (CN=worker-node-04.example.test) and omitted Subject Alternative Name for the service DNS alias.",
    diagnostics=[
        "Extract presented certificate from endpoint using openssl s_client -connect analytics.example.test:8443 -servername analytics.example.test.",
        "Inspect X.509 extensions using openssl x509 -text -noout to verify Subject Alternative Name (SAN) presence.",
        "Confirm that RFC 5280 defines path validation and RFC 9525 excludes Common Name evaluation when verifying hostnames in modern TLS stacks."
    ],
    fixes=[
        "Reissue leaf certificate from internal Intermediate CA including subjectAltName = DNS:analytics.example.test, DNS:worker-node-04.example.test.",
        "Deploy updated certificate and reload the analytics receiver service daemon without downtime."
    ],
    verify="Connect from client using openssl s_client with CA verification enabled and verify Verify return code: 0 (ok).",
    residual="Ensure automated certificate renewal pipelines (such as Google Certificate Manager or cert-manager) preserve all SAN entries during scheduled rotation.",
    enabled=True,
    diagram=(
        "Client connects via service DNS alias",
        "Server presents cert lacking SAN for alias",
        "TLS client aborts handshake with hostname mismatch",
        "Reissue cert with correct SAN DNS entries",
        "Certificate chain validates; TLS handshake succeeds"
    ),
    facts="Illustrative fixture client log lists SSLError CertificateError indicating hostname analytics.example.test does not match presented certificate.",
    inference="The supplied fixture models RFC 9525 identity matching, ignoring legacy Common Name and requiring explicit Subject Alternative Name entries.",
    expected="Reissued leaf certificate includes required SAN DNS alias; client successfully validates chain and establishes TLS 1.3 session."
)

# Topic 03 Incident
P3_CASE = case(
    scenario="Batch database replication across IPSec VPN hangs indefinitely while ICMP pings and small health checks pass continuously.",
    impact="Nightly data warehouse sync delayed by 6 hours; executive financial reporting dashboards missing current transactional data.",
    constraints="Cannot modify physical WAN link MTU provided by telecommunications carrier; cannot disable Don't Fragment bit on production database.",
    records=(
        "2026-10-04T10:05:18.004Z [packet-capture-vpn0] IP (tos 0x0, ttl 64, id 41201, offset 0, flags [DF], proto TCP (6), length 1500) "
        "10.0.1.10.5432 > 192.168.10.50.48120: Flags [P.], seq 1:1461, ack 1, win 65535, length 1460\n"
        "2026-10-04T10:05:18.005Z [router-ipsec] IP (tos 0xc0, ttl 255, id 109, offset 0, flags [none], proto ICMP (1), length 56) "
        "10.0.1.1 > 10.0.1.10: ICMP 192.168.10.50 unreachable - need to frag (mtu 1400), length 36\n"
        "2026-10-04T10:05:18.006Z [perimeter-fw] DENY: ICMP type 3 code 4 from 10.0.1.1 to 10.0.1.10 (policy: drop-all-inbound-icmp)"
    ),
    root="IPSec VPN tunnel MTU was 1400 bytes. The database sent 1500B packets with DF=1. The router dropped them and generated ICMP Type 3 Code 4, which the firewall blocked.",
    diagnostics=[
        "Perform packet capture on VPN interface to observe TCP retransmissions with DF=1 flag set.",
        "Check intermediate firewall drop logs for ICMP Type 3 Code 4 Destination Unreachable messages.",
        "Execute MTU probe using ping -M do -s 1372 to identify the exact MTU threshold where packets traverse successfully."
    ],
    fixes=[
        "Update perimeter firewall rules to explicitly permit inbound ICMP Type 3 Code 4 (Fragmentation Needed) messages.",
        "Configure TCP MSS clamping on the VPN gateway router to clamp all TCP SYN packets traversing the tunnel to MSS 1360."
    ],
    verify="Run large batch data replication transfer and verify throughput exceeds 85 MB/s with zero packet drops or retransmissions.",
    residual="Non-TCP protocols (such as UDP-based streaming or QUIC) cannot use TCP MSS clamping and must rely strictly on PMTUD or application-layer sizing.",
    enabled=True,
    diagram=(
        "App sends 1500-byte packet with DF bit set",
        "Intermediate VPN router drops packet exceeding MTU 1400",
        "Firewall drops ICMP Type 3; sender hangs indefinitely",
        "Enable TCP MSS clamping to 1360 at VPN boundary",
        "Packets fit MTU; batch data transfers without drops"
    ),
    facts="Supplied illustrative packet fixture depicts database sent 1500B packet with DF=1; intermediate router emitted ICMP Type 3 Code 4 which perimeter firewall dropped.",
    inference="Filtering ICMP fragmentation feedback created a classic Path MTU black hole, trapping sender in an infinite retransmission loop.",
    expected="Permitting ICMP Type 3 and configuring TCP MSS clamping to 1360 forces packets to fit link MTU, eliminating black hole drops."
)

# Topic 04 Incident
P4_CASE = case(
    scenario="Private backend worker instances exhaust Cloud NAT ephemeral port pool during marketing push, dropping outgoing webhook calls.",
    impact="Customer notification delivery rate drops from 99.9% to 71.4%; critical one-time password (OTP) verification SMS deliveries delayed.",
    constraints="Worker VMs must remain private without external public IPs; cannot alter destination SMS aggregator IP addresses.",
    records=(
        '2026-10-04T11:30:45.892Z [cloud-nat-logging] {"allocation_status": "DROPPED", '
        '"endpoint": {"vm_name": "notification-worker-08", "zone": "us-central1-a"}, '
        '"gateway_name": "nat-gw-us-central1", "nat_ip": "203.0.113.20", '
        '"reason": "OUT_OF_RESOURCES", "destination": "198.51.100.80:443", '
        '"protocol": 6, "allocated_ports": 64, "active_connections": 64}'
    ),
    root="Cloud NAT was configured with a static allocation of 64 ports per VM. Burst concurrency exceeded 64 concurrent outbound connections, exhausting allocated ports.",
    diagnostics=[
        "Inspect Cloud NAT connection logs filtering for allocation_status=DROPPED and reason=OUT_OF_RESOURCES.",
        "Query Cloud Monitoring metric router.googleapis.com/nat/nat_allocation_failed to detect allocation failure (boolean gauge); use compute.googleapis.com/nat/dropped_sent_packets_count with reason=OUT_OF_RESOURCES for dropped-packet counts.",
        "Calculate concurrent outbound connection requirements across worker pool based on webhook dispatch rate and connection hold times."
    ],
    fixes=[
        "Enable Dynamic Port Allocation on the Cloud NAT gateway, allowing VMs to scale port slices dynamically from 64 to 1024.",
        "Assign 2 additional static external IP addresses to the Cloud NAT gateway to expand a three-IP theoretical pool to 193,536 TCP source ports (3 × 64,512); validate allocation constraints and destination reuse rather than treating this as a connection guarantee."
    ],
    verify="Simulate burst webhook workload generating 250 concurrent connections per VM and confirm zero OUT_OF_RESOURCES errors in Cloud NAT logs.",
    residual="If a rogue process opens thousands of hung connections, it could exhaust the gateway-wide pool; configure maximum ports per VM limit.",
    enabled=True,
    diagram=(
        "Worker burst dispatches 500 concurrent webhook calls",
        "Cloud NAT static port allocation exhausted at 64 ports",
        "Outgoing TCP SYNs dropped; connections timeout",
        "Enable dynamic port allocation and increase gateway IPs",
        "Sufficient port pool; webhooks transmit cleanly"
    ),
    facts="Illustrative fixture Cloud NAT log lists allocation_status DROPPED with reason OUT_OF_RESOURCES when active_connections reached static limit of 64.",
    inference="Static port reservation prevented the VM from acquiring additional ports from the available gateway pool during transient burst traffic.",
    expected="Dynamic port allocation automatically assigns additional port blocks on demand; outgoing connections establish with zero drops."
)

# Topic 05 Incident
P5_CASE = case(
    scenario="Hybrid traffic from GCP to on-premises data center is routed over high-latency backup Interconnect due to missing BGP path attributes.",
    impact="Transactional database replication latency spikes from 4ms to 72ms; stateful perimeter firewalls drop asymmetric return packets.",
    constraints="Must maintain automated active/passive failover across both Interconnect circuits; cannot tear down backup BGP session during production hours.",
    records=(
        "2026-10-04T12:15:30.104Z [gcp-cloud-router] ROUTE_TABLE_DUMP:\n"
        "  prefix: 10.200.0.0/16 | nexthop: 169.254.10.1 (Interconnect-Primary) | as_path: [65001] | med: 100 | priority: 100\n"
        "  prefix: 10.200.0.0/16 | nexthop: 169.254.20.1 (Interconnect-Backup)  | as_path: [65001] | med: 100 | priority: 100\n"
        "2026-10-04T12:15:32.450Z [onprem-firewall] DROP: TCP RST from 10.200.15.4 to 10.128.0.12 "
        "(reason: TCP state violation - SYN seen on Interconnect-1, ACK seen on Interconnect-2, asymmetric routing rejected)"
    ),
    root="Both on-premises BGP routers advertised identical prefix 10.200.0.0/16 with equal AS-path length and equal MED 100. The supplied illustrative case assumes eligible ECMP paths and a stateful-firewall rejection; equal attributes alone do not establish actual Cloud Router behavior without selection-mode and route-policy evidence.",
    diagnostics=[
        "Inspect Cloud Router BGP status using gcloud compute routers get-status to review advertised and learned routes.",
        "Compare BGP path attributes (AS_PATH, MED, Local Preference) across both Interconnect BGP sessions.",
        "Analyze on-premises stateful firewall drop logs to confirm asymmetric routing state violations."
    ],
    fixes=[
        "Configure on-premises backup router to prepend its ASN twice (as_path: [65001, 65001, 65001]) and advertise a higher MED of 200.",
        "Configure Cloud Router custom route priorities to ensure Interconnect-Primary (priority 100) is deterministically selected over Backup (priority 200)."
    ],
    verify="Inspect Cloud Router routing table to confirm Interconnect-Primary is installed as sole active next hop, and measure replication latency against the illustrative 4ms recovery target; it is not a provider latency guarantee.",
    residual="Ensure BGP keep-alive timers and BFD (Bidirectional Forwarding Detection) are configured appropriately; measure detection, BGP convergence and restoration if Interconnect-Primary suffers physical loss, rather than assume sub-second failover.",
    enabled=True,
    diagram=(
        "Hybrid link established across dual Cloud Interconnects",
        "On-prem router advertises prefix with equal AS-path and MED",
        "Asymmetric routing causes stateful firewall drops and latency",
        "Apply BGP AS-path prepending and MED on backup route",
        "Predicted primary-link routing; latency requires local or cloud measurement"
    ),
    facts="Supplied illustrative Cloud Router routing table lists identical prefix 10.200.0.0/16 learned with equal AS-path length and equal MED 100 over both Interconnects.",
    inference="Without tie-breaking path attributes, the illustrative case predicts multiple eligible paths; actual Cloud Router selection mode and firewall traces must confirm any balancing or asymmetric drop.",
    expected="Applying AS-path prepending and higher MED to backup session ensures primary link is selected deterministically; the illustrative expected latency must be measured after routing and firewall validation."
)

# ==============================================================================
# PART 4: STEP-BY-STEP LABS
# ==============================================================================

# Lab 1
L1_LAB = make_lab(
    covers='Exit worksheet HTTP errors; supports the HTTP diagnosis accompanying Practice.',
    name="HTTP Protocol Semantics, Header Normalization, and Multi-Version Analysis",
    goal="Author a Python HTTP server, execute structured requests across HTTP methods, observe status code taxonomy, and evaluate HTTP/2 header normalization rules.",
    expected="A complete HTTP protocol transaction trace proving status code behavior (200, 400, 502) and header normalization mechanics.",
    steps=[
        stage(1, "Preflight and Workspace Initialization",
              "Verify Python 3 availability, check curl availability; HTTP/2 and HTTP/3 behavior is simulated while the local server speaks HTTP/1.0, and initialize a dedicated temporary laboratory workspace.",
              "Python 3 and curl verified; dedicated temporary directory created and exported as <samp>$LAB_DIR</samp>.",
              "preflight.log",
              commands=workspace("http_lab", preflight_text="Python 3 verified; curl available; HTTP/1.0 local server; HTTP/2 and HTTP/3 simulated")),
        stage(2, "Prepare Mock HTTP Server",
              "Author a lightweight Python HTTP server (<samp>mock_server.py</samp>) that implements custom header inspection, status code routing, and simulated gateway errors.",
              "Mock HTTP server script authored successfully with endpoints for /api/v1/ok, /api/v1/bad-req, and /api/v1/error.",
              "mock_server.py",
              commands=write_file("mock_server.py", """import http.server
import socketserver
import json
import sys

PORT = 8085

class DiagnosticHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/v1/ok':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('X-Server-Protocol', self.protocol_version)
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'SUCCESS', 'protocol': self.protocol_version}).encode())
        elif self.path == '/api/v1/bad-req':
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'CLIENT_BAD_REQUEST', 'detail': 'Missing mandatory auth token'}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        uppercase_headers = [k for k in self.headers.keys() if any(c.isupper() for c in k)]
        if self.path == '/api/v1/checkout':
            if uppercase_headers and self.headers.get('X-Enforce-Lowercase') == 'true':
                self.send_response(502)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'PROTOCOL_ERROR',
                    'detail': f'Strict HTTP/2 proxy rejected uppercase headers: {uppercase_headers}'
                }).encode())
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'checkout': 'CONFIRMED', 'headers_received': len(self.headers)}).encode())

if __name__ == '__main__':
    with socketserver.TCPServer(('127.0.0.1', PORT), DiagnosticHTTPHandler) as httpd:
        print(f"Mock HTTP server listening on 127.0.0.1:{PORT}")
        httpd.serve_forever()
""")),
        stage(3, "Author HTTP Client Diagnostic Suite",
              "Author a Bash diagnostic test suite (<samp>test_http.sh</samp>) executing standardized requests using curl, inspecting headers, and recording status codes.",
              "Diagnostic script authored containing tests for 200 OK, 400 Bad Request, and simulated 502 Bad Gateway.",
              "test_http.sh",
              commands=write_file("test_http.sh", """#!/usr/bin/env bash
set -e
PORT=8085
BASE="http://127.0.0.1:$PORT"

echo "=== Test 1: Standard GET 200 OK ==="
curl -i -s "$BASE/api/v1/ok" > test1_200.txt

echo "=== Test 2: Client Error 400 Bad Request ==="
curl -i -s "$BASE/api/v1/bad-req" > test2_400.txt

echo "=== Test 3: Simulated HTTP/2 Protocol Error (502 Bad Gateway) ==="
curl -i -s -X POST "$BASE/api/v1/checkout" \
  -H "X-Custom-Auth: SecretToken123" \
  -H "X-Enforce-Lowercase: true" \
  -d '{"item": "book", "qty": 1}' > test3_502.txt

echo "=== Test 4: Normalized Header Fix (200 OK) ==="
curl -i -s -X POST "$BASE/api/v1/checkout" \
  -H "x-custom-auth: SecretToken123" \
  -H "x-enforce-lowercase: false" \
  -d '{"item": "book", "qty": 1}' > test4_fixed.txt

echo "All diagnostic tests completed."
""")),
        stage(4, "Execute Server and Diagnostic Suite",
              "Launch the mock HTTP server in the background and execute the diagnostic client suite.",
              "Mock HTTP server launched on 127.0.0.1:8085; diagnostic tests executed and response artifacts generated.",
              "execution.log",
              commands="""python3 mock_server.py > server.log 2>&1 &
SERVER_PID=$!
sleep 1
bash test_http.sh > execution.log
kill "$SERVER_PID"
wait "$SERVER_PID" || { status=$?; test "$status" -eq 143; }
"""),
        stage(5, "Inspect Expected State and Status Codes",
              "Inspect response headers and payloads across test artifacts to verify proper status code taxonomy.",
              "Verified 200 OK for standard endpoints, 400 Bad Request for client errors, and 502 Bad Gateway for simulated protocol error.",
              "inspected_responses.log",
              commands="""head -n 5 test1_200.txt > inspected_responses.log
echo "---" >> inspected_responses.log
head -n 5 test2_400.txt >> inspected_responses.log
echo "---" >> inspected_responses.log
head -n 5 test3_502.txt >> inspected_responses.log
cat inspected_responses.log
"""),
        stage(6, "Rehearse Bounded Failure: Header Casing Impact",
              "Compare the raw output of the rejected uppercase header request against the normalized lowercase request.",
              "Comparison confirms that uppercase header triggering simulated strict proxy check resulted in 502 PROTOCOL_ERROR.",
              "header_comparison.log",
              commands="""grep -E "HTTP/|error|checkout" test3_502.txt test4_fixed.txt > header_comparison.log
cat header_comparison.log
"""),
        stage(7, "Diagnose Evidence and Record Architectural Remediation",
              "Author a structured summary documenting why HTTP/2 header downcasing is mandatory for ingress proxies.",
              "Diagnostic summary authored recording RFC 9113 header normalization requirements and status code classification.",
              "http_evidence_summary.md",
              commands=write_file("http_evidence_summary.md", """# Architectural Evidence: HTTP Semantics and Protocol Evolution

- Observation 1: HTTP 400 Bad Request indicates client validation failure; origin infrastructure is operational.
- Observation 2: The local HTTP/1.0 server deliberately returns simulated HTTP 502 for its casing rule. A real 502 indicates an invalid upstream response; diagnose rather than infer a specific protocol mismatch.
- Model 3: RFC 9113 section 8.2.1 excludes uppercase field names. The local HTTP/1.0 request check simulates a rejection policy and does not observe an HTTP/2 stream reset or HTTP/3 behavior.
- Architectural Remediation: Edge ingress proxies (Cloud Load Balancing, Envoy) must enforce automatic header downcasing before encapsulation into HTTP/2 streams.
""")),
        stage(8, "Clean Up and Close Out Exercise",
              "Verify background processes are terminated, remove temporary scripts, and save final evidence logs.",
              "Mock server terminated; temporary test scripts cleaned up; evidence summary preserved.",
              "cleanup.log",
              commands="""rm -f mock_server.py test_http.sh test1_200.txt test2_400.txt test3_502.txt test4_fixed.txt server.log
echo "Lab 1 closed out cleanly." > cleanup.log
cat cleanup.log
""")
    ],
    accept="Evidence summary proves understanding of HTTP status codes, header downcasing rules, and protocol error isolation.",
    trouble="If port 8085 is in use, modify PORT variable in mock_server.py and test_http.sh to an unprivileged open port.",
    file_name="day-004-topic-01.md"
)

# Lab 2
L2_LAB = make_lab(
    covers='Compare a valid and a hostname-mismatched certificate trace',
    name="TLS 1.3 Handshake Inspection and Certificate Validation Chain Analysis",
    goal="Construct an X.509 PKI hierarchy (Root CA, Intermediate CA, Leaf certificate), simulate a hostname mismatch failure, and verify cryptographic chain validation using OpenSSL.",
    expected="An OpenSSL cryptographic audit trail of local certificate chain validation and SAN comparisons, alongside supplied TLS 1.3 traces; this exercise does not execute a live TLS 1.3 handshake.",
    steps=[
        stage(1, "Preflight and OpenSSL Environment Verification",
              "Verify local OpenSSL version, confirm support for TLS 1.3 and elliptic curve algorithms, and initialize PKI workspace.",
              "OpenSSL version confirmed; dedicated temporary PKI directory created.",
              "preflight.log",
              commands=workspace("pki_lab", preflight_text="OpenSSL verified; elliptic curve algorithms supported; offline PKI execution")),
        stage(2, "Prepare OpenSSL CA Configuration Files",
              "Author OpenSSL configuration files for the Root CA and Intermediate CA specifying basic constraints and key usage extensions.",
              "OpenSSL configuration files authored with CA=TRUE and digitalSignature constraints.",
              "openssl_configs.log",
              commands=write_file("supplied-valid-trace.txt", """SUPPLIED ILLUSTRATIVE FIXTURE — not a local capture
requested hostname: orders.example.test
ClientHello: TLS 1.3; server_name=orders.example.test
ServerHello: TLS 1.3
Certificate: SAN DNS:orders.example.test; issuer=Example Intermediate CA
certificate path: valid under supplied Example Root CA trust anchor
hostname match: MATCH
Finished: accepted; HTTP request may follow
""") + write_file("supplied-mismatch-trace.txt", """SUPPLIED ILLUSTRATIVE FIXTURE — not a local capture
requested hostname: orders.example.test
ClientHello: TLS 1.3; server_name=orders.example.test
ServerHello: TLS 1.3
Certificate: SAN DNS:admin.example.test; issuer=Example Intermediate CA
certificate path: valid under supplied Example Root CA trust anchor
hostname match: MISMATCH
client result: reject service identity; HTTP request not sent
""") + write_file("certificate-trace-comparison.md", """# Supplied certificate trace comparison
These traces are supplied illustrative fixtures; no handshake was captured locally.

| Check | Valid trace | Mismatched trace |
| --- | --- | --- |
| Requested reference hostname | orders.example.test | orders.example.test |
| Presented SAN DNS identifier | orders.example.test | admin.example.test |
| Supplied chain status | Valid | Valid |
| Reference versus presented identity | MATCH | MISMATCH |
| Decision before HTTP | Accept identity | Reject identity |

A trusted chain does not establish the requested service identity. SNI requests a
name; it does not replace checking the certificate SAN against the reference name.
The generated CA exercise below is additional local work, separate from this pair.
""") + write_file("ca.cnf", """[ req ]
default_bits        = 2048
distinguished_name  = req_distinguished_name
prompt              = no

[ req_distinguished_name ]
C                   = US
ST                  = California
L                   = Sunnyvale
O                   = Enterprise Lab
CN                  = Enterprise Root CA

[ v3_ca ]
basicConstraints    = critical, CA:TRUE
keyUsage            = critical, digitalSignature, cRLSign, keyCertSign
subjectKeyIdentifier= hash
authorityKeyIdentifier = keyid:always,issuer
""") + write_file("intermediate.cnf", """[ req ]
default_bits        = 2048
distinguished_name  = req_distinguished_name
prompt              = no

[ req_distinguished_name ]
C                   = US
ST                  = California
L                   = Sunnyvale
O                   = Enterprise Lab
CN                  = Enterprise Intermediate CA

[ v3_intermediate_ca ]
basicConstraints    = critical, CA:TRUE, pathlen:0
keyUsage            = critical, digitalSignature, cRLSign, keyCertSign
subjectKeyIdentifier= hash
authorityKeyIdentifier = keyid:always,issuer
""") + "cat ca.cnf intermediate.cnf > openssl_configs.log\n"),
        stage(3, "Generate Root and Intermediate CA Keys and Certificates",
              "Generate private keys and issue self-signed Root CA certificate, then issue signed Intermediate CA certificate.",
              "Root CA (root_ca.crt) and Intermediate CA (intermediate.crt) generated and signed successfully.",
              "ca_generation.log",
              commands="""openssl genrsa -out root_ca.key 2048 2>/dev/null
openssl req -x509 -new -nodes -key root_ca.key -sha256 -days 365 -config ca.cnf -extensions v3_ca -out root_ca.crt

openssl genrsa -out intermediate.key 2048 2>/dev/null
openssl req -new -key intermediate.key -out intermediate.csr -config intermediate.cnf

openssl x509 -req -in intermediate.csr -CA root_ca.crt -CAkey root_ca.key -CAcreateserial \
  -out intermediate.crt -days 180 -sha256 -extfile intermediate.cnf -extensions v3_intermediate_ca

echo "Root CA and Intermediate CA generated." > ca_generation.log
openssl verify -CAfile root_ca.crt intermediate.crt >> ca_generation.log
cat ca_generation.log
"""),
        stage(4, "Issue Leaf Certificate with Subject Alternative Name (SAN)",
              "Generate leaf private key and issue server certificate containing Subject Alternative Name (<samp>DNS:service.example.test</samp>).",
              "Leaf certificate (server.crt) issued with SAN extension matching service DNS alias.",
              "leaf_generation.log",
              commands=write_file("server.cnf", """[ req ]
default_bits        = 2048
distinguished_name  = req_distinguished_name
prompt              = no

[ req_distinguished_name ]
C                   = US
ST                  = California
L                   = Sunnyvale
O                   = Enterprise Lab
CN                  = host-01.example.test

[ v3_req ]
basicConstraints    = CA:FALSE
keyUsage            = critical, digitalSignature, keyEncipherment
extendedKeyUsage    = serverAuth
subjectAltName      = @alt_names

[ alt_names ]
DNS.1               = service.example.test
DNS.2               = host-01.example.test
""") + """openssl genrsa -out server.key 2048 2>/dev/null
openssl req -new -key server.key -out server.csr -config server.cnf

openssl x509 -req -in server.csr -CA intermediate.crt -CAkey intermediate.key -CAcreateserial \
  -out server.crt -days 90 -sha256 -extfile server.cnf -extensions v3_req

echo "Leaf certificate issued with SAN." > leaf_generation.log
openssl x509 -in server.crt -text -noout | grep -A 2 "Subject Alternative Name" >> leaf_generation.log
cat leaf_generation.log
"""),
        stage(5, "Inspect Expected State: Cryptographic Chain Validation",
              "Validate complete certificate chain from leaf to intermediate and root CA using OpenSSL verify.",
              "OpenSSL verification confirmed: server.crt validates successfully against intermediate and root trust anchor.",
              "chain_verification.log",
              commands="""cat supplied-valid-trace.txt supplied-mismatch-trace.txt certificate-trace-comparison.md
cat intermediate.crt root_ca.crt > ca_chain.crt
openssl verify -CAfile root_ca.crt -untrusted intermediate.crt server.crt > chain_verification.log
cat chain_verification.log
"""),
        stage(6, "Rehearse Bounded Failure: Hostname Mismatch Simulation",
              "Execute a Python TLS validation test verifying that connecting to an unlisted hostname fails strictly despite valid CA signatures.",
              "Local Python SAN membership comparison yields MISMATCH for the unlisted alias and MATCH for the listed alias; this is a name-comparison model, not a TLS handshake.",
              "hostname_test.log",
              commands=write_file("verify_test.py", """import ssl
import sys

ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="ca_chain.crt")
ctx.check_hostname = True
ctx.verify_mode = ssl.CERT_REQUIRED

cert_dict = ssl._ssl._test_decode_cert("server.crt")
sans = [entry[1] for entry in cert_dict.get('subjectAltName', []) if entry[0] == 'DNS']

print(f"Cert Subject Common Name: {dict(x[0] for x in cert_dict['subject'])['commonName']}")
print(f"Cert Subject Alt Names: {sans}")

test_valid = "service.example.test"
test_invalid = "unlisted-alias.example.test"

print(f"Checking '{test_valid}': {'MATCH' if test_valid in sans else 'MISMATCH'}")
print(f"Checking '{test_invalid}': {'MATCH' if test_invalid in sans else 'MISMATCH'}")
""") + """python3 verify_test.py > hostname_test.log
cat hostname_test.log
"""),
        stage(7, "Diagnose Evidence and Author Failure Analysis",
              "Author structured analysis distinguishing trust anchor errors, certificate expiration, and hostname mismatch causes.",
              "Diagnostic failure analysis authored documenting X.509 validation failure categories.",
              "pki_evidence_summary.md",
              commands=write_file("pki_evidence_summary.md", """# Architectural Evidence: X.509 PKI Trust and Certificate Chains

- Category 1: Trust Anchor Failure (Unknown CA) — Occurs when the client trust store lacks the root certificate or intermediate chain is incomplete.
- Category 2: Expiration / Validity Window — Occurs when current timestamp < notBefore or > notAfter.
- Category 3: Hostname Mismatch — Occurs when requested FQDN does not match any dNSName entry in the Subject Alternative Name (SAN) extension.
- Architectural Remediation: Modern TLS stacks ignore Common Name (CN). Reissue certificates with comprehensive SAN lists and automate deployment via Google Certificate Manager.
""")),
        stage(8, "Clean Up and Close Out PKI Exercise",
              "Securely remove generated private keys, CSRs, and temporary certificates, preserving final summary.",
              "Private keys and certificates purged from workspace; audit log preserved.",
              "cleanup.log",
              commands="""rm -f *.key *.csr *.cnf server.crt intermediate.crt root_ca.crt ca_chain.crt verify_test.py
echo "Lab 2 closed out cleanly." > cleanup.log
cat cleanup.log
""")
    ],
    accept="Evidence log demonstrates successful X.509 certificate chain validation and isolates hostname mismatch error mechanics.",
    trouble="Ensure the intermediate certificate is passed via the -untrusted flag when executing openssl verify.",
    file_name="day-004-topic-02.md"
)

# Lab 3
L3_LAB = make_lab(
    covers='annotate an MTU failure',
    name="Path MTU Discovery, Packet Sizing, and MSS Clamping Simulation",
    goal="Calculate IP and TCP header overheads, simulate packet fragmentation behavior with the Don't Fragment (DF) flag, and evaluate MSS clamping rules on network boundaries.",
    expected="A documented MTU/MSS calculation matrix and packet diagnostic log demonstrating the mechanics of PMTUD and black hole mitigation.",
    steps=[
        stage(1, "Preflight and MTU Environment Inspection",
              "Inspect local interface MTU configurations (<kbd>ip link</kbd>) and initialize MTU lab workspace.",
              "Local interface MTU inspected; temporary MTU lab directory initialized.",
              "preflight.log",
              commands=workspace("mtu_lab", preflight_text="ip link verified; interface MTUs recorded; offline MTU calculation")),
        stage(2, "Prepare MTU/MSS Calculation Engine",
              "Author a Python calculation engine (<samp>mtu_calc.py</samp>) computing IPv4, IPv6, and tunneling overheads across network architectures.",
              "Calculation script authored implementing MTU-to-MSS formulas for standard Ethernet, GCP VPC, and IPSec tunnels.",
              "mtu_calc.py",
              commands=write_file("supplied-mtu-capture.txt", """SUPPLIED ILLUSTRATIVE FIXTURE — not a local packet capture
10.20.1.5 -> 10.50.4.8: IPv4 total_length=1500 DF=1 TCP_payload=1460
intermediate router: outgoing MTU=1400; discard oversized packet
router -> 10.20.1.5: ICMP Type 3 Code 4 next-hop MTU=1400
firewall: ICMP fragmentation feedback dropped
sender: retransmit same oversized data; small health check succeeds
ANNOTATION: DF prevents fragmentation; blocked ICMP prevents PMTUD adaptation.
REMEDIATION PREDICTION: permit fragmentation-needed feedback; IPv4 base-header
MSS=1400-20-20=1360. The local calculation is a simulation of this supplied fixture.
""") + write_file("mtu_calc.py", """def calculate_mss(mtu, ip_version=4, options_bytes=0, tunnel_overhead=0):
    effective_mtu = mtu - tunnel_overhead
    ip_header = 20 if ip_version == 4 else 40
    tcp_header = 20 + options_bytes
    mss = effective_mtu - ip_header - tcp_header
    return effective_mtu, mss

scenarios = [
    ("Standard Internet Ethernet", 1500, 4, 0, 0),
    ("Standard Internet IPv6", 1500, 6, 0, 0),
    ("Google Cloud VPC Default (IPv4)", 1460, 4, 0, 0),
    ("Google Cloud VPC Default (IPv6)", 1460, 6, 0, 0),
    ("Google Cloud Jumbo Frame VPC", 8896, 4, 0, 0),
    ("IPSec VPN Tunnel over 1500 MTU (ESP overhead 56B)", 1500, 4, 0, 56),
    ("IPSec VPN Tunnel over 1460 MTU (ESP overhead 56B)", 1460, 4, 0, 56),
    ("Illustrative clamp overhead", 1460, 4, 0, 40),
]

print(f"{'Scenario':<45} | {'MTU':<5} | {'Tunnel OH':<9} | {'Eff MTU':<7} | {'MSS'}")
print("-" * 78)
for name, mtu, ipv, opt, tun in scenarios:
    eff, mss = calculate_mss(mtu, ipv, opt, tun)
    print(f"{name:<45} | {mtu:<5} | {tun:<9} | {eff:<7} | {mss}")
""")),
        stage(3, "Execute MTU/MSS Sizing Matrix",
              "Execute the calculation engine and generate the canonical MTU and MSS framing table.",
              "MTU and MSS sizing matrix executed and recorded into calculation_results.txt.",
              "calculation_results.txt",
              commands="""python3 mtu_calc.py > calculation_results.txt
cat calculation_results.txt
"""),
        stage(4, "Author PMTUD Simulation Harness",
              "Author a Python simulation harness (<samp>pmtud_sim.py</samp>) modeling packet traversal across a bottleneck link with DF=1 flag inspection.",
              "Simulation harness authored modeling PMTUD fragmentation needed generation and black hole dropping.",
              "pmtud_sim.py",
              commands=write_file("pmtud_sim.py", """class NetworkHop:
    def __init__(self, name, mtu, filter_icmp=False):
        self.name = name
        self.mtu = mtu
        self.filter_icmp = filter_icmp

    def forward(self, packet_size, df_flag):
        if packet_size <= self.mtu:
            return {"status": "FORWARDED", "hop": self.name, "mtu": self.mtu}
        if df_flag:
            if self.filter_icmp:
                return {"status": "BLACK_HOLE_DROP", "hop": self.name, "mtu": self.mtu}
            else:
                return {"status": "ICMP_TYPE_3_CODE_4", "hop": self.name, "mtu": self.mtu}
        else:
            return {"status": "FRAGMENTED", "hop": self.name, "mtu": self.mtu}

path = [
    NetworkHop("Host VPC Interface", 1500),
    NetworkHop("Intermediate IPSec Tunnel", 1400, filter_icmp=True),
    NetworkHop("Remote Destination Gateway", 1500)
]

print("=== Simulating 1500B Packet with DF=1 across ICMP-filtered tunnel ===")
for hop in path:
    res = hop.forward(1500, df_flag=True)
    print(f"Hop: {hop.name:<30} -> Result: {res['status']}")
    if res['status'] in ("BLACK_HOLE_DROP", "ICMP_TYPE_3_CODE_4"):
        print(f"Packet dropped at {hop.name}! Exceeded MTU {hop.mtu}")
        break
""")),
        stage(5, "Inspect Expected State: PMTUD Black Hole Drop",
              "Execute the PMTUD simulation harness to demonstrate silent packet loss when ICMP feedback is filtered.",
              "Simulation proves that 1500B packet with DF=1 is dropped silently as BLACK_HOLE_DROP at the 1400B hop.",
              "pmtud_execution.log",
              commands="""python3 pmtud_sim.py > pmtud_execution.log
cat pmtud_execution.log
"""),
        stage(6, "Rehearse Bounded Failure: Local Ping DF Flag Testing",
              "Rehearse the kernel's handling of the Don't Fragment flag against local loopback using ping with the do flag.",
              "Environment-dependent illustrative loopback output: 65507 data bytes may receive a reply; 65508 may report message too long (MTU=65536) or invalid argument. Check actual interface MTU and failure text; if ping is absent record SKIPPED. This does not observe the supplied 1400-byte path.",
              "ping_df_test.log",
              commands="""command -v ping || echo "ping not installed; skip this stage"
if command -v ping >/dev/null; then
  ping -c 1 -M do -s 65507 127.0.0.1 > ping_df_test.log 2>&1
  if ping -c 1 -M do -s 65508 127.0.0.1 >> ping_df_test.log 2>&1; then
    echo "Unexpected success: inspect loopback MTU before accepting this exercise" >&2
    exit 1
  else
    status=$?
    test "$status" -eq 1 || test "$status" -eq 2
    grep -Ei 'too long|mtu|invalid argument' ping_df_test.log
  fi
  head -n 5 ping_df_test.log
else
  echo "SKIPPED: ping unavailable; retain supplied MTU fixture and calculations" > ping_df_test.log
fi
"""),
        stage(7, "Diagnose Evidence and Author MSS Clamping Recommendations",
              "Author structured architectural recommendations detailing how TCP MSS clamping resolves PMTUD black holes.",
              "Architectural summary authored documenting MSS clamping rules and Google Cloud VPC MTU defaults.",
              "mtu_evidence_summary.md",
              commands=write_file("mtu_evidence_summary.md", """# Architectural Evidence: MTU, PMTUD, and MSS Clamping

- Finding 1: An IPv4 TCP segment requires 40 bytes of header overhead (20B IP + 20B TCP). Standard 1500 MTU yields 1460 MSS; GCP 1460 MTU yields 1420 MSS.
- Finding 2: Filtering ICMP Type 3 Code 4 creates a Path MTU black hole: small handshakes succeed, but large payload packets stall indefinitely.
- Architectural Fix: Deploy TCP MSS clamping at the VPN / Interconnect gateway (clamping SYN MSS to 1360 bytes), forcing endpoints to negotiate segment sizes that fit the tunnel.
""")),
        stage(8, "Clean Up and Close Out MTU Exercise",
              "Remove temporary calculation scripts and record final verification status.",
              "Temporary scripts removed; calculation results and evidence summary preserved.",
              "cleanup.log",
              commands="""rm -f mtu_calc.py pmtud_sim.py
echo "Lab 3 closed out cleanly." > cleanup.log
cat cleanup.log
""")
    ],
    accept="Calculation matrix and simulation logs confirm mathematical MTU/MSS relationships and validate MSS clamping remediation.",
    trouble="Ensure ping -M do is supported on the Linux distribution; on macOS, use ping -D -s.",
    file_name="day-004-topic-03.md"
)

# Lab 4
L4_LAB = make_lab(
    covers='Exit worksheet NAT context; supports the supplied-capture interpretation.',
    name="SNAT State Tracking, Port Allocation, and Exhaustion Simulation",
    goal="Model NAT state table translation (5-tuple tracking), calculate Cloud NAT IP/port capacity requirements, and simulate port allocation exhaustion under burst concurrency.",
    expected="A complete NAT translation model log showing source port mapping, state table lifecycle, and capacity sizing formulas.",
    steps=[
        stage(1, "Preflight and Environment Initialization",
              "Verify Python 3 environment, check socket capabilities, and initialize NAT laboratory workspace.",
              "Python 3 verified; temporary NAT workspace initialized.",
              "preflight.log",
              commands=workspace("nat_lab", preflight_text="Python 3 verified; NAT simulation environment initialized; offline execution")),
        stage(2, "Prepare NAT State Table Simulation Engine",
              "Author a Python simulation engine (<samp>nat_engine.py</samp>) modeling 5-tuple translation and port reservation limits.",
              "NAT simulation engine authored with state table management, IP pool management, and port exhaustion tracking.",
              "nat_engine.py",
              commands=write_file("nat_engine.py", """import sys

class CloudNATSimulator:
    def __init__(self, public_ips, min_ports_per_vm=64, dynamic_port_allocation=False, max_ports=1024):
        self.public_ips = public_ips
        self.min_ports = min_ports_per_vm
        self.dynamic = dynamic_port_allocation
        self.max_ports = max_ports
        self.total_ports = len(public_ips) * 64000
        self.state_table = {}
        self.vm_allocations = {}
        self.drops = 0

    def connect(self, vm_ip, client_port, dst_ip, dst_port):
        flow_key = (vm_ip, client_port, dst_ip, dst_port, "TCP")
        if flow_key in self.state_table:
            return {"status": "ESTABLISHED_EXISTING", "mapping": self.state_table[flow_key]}

        allocated = self.vm_allocations.get(vm_ip, [])
        limit = self.max_ports if self.dynamic else self.min_ports

        if len(allocated) >= limit:
            self.drops += 1
            return {"status": "DROPPED_PORT_EXHAUSTION", "reason": "OUT_OF_RESOURCES", "active": len(allocated)}

        nat_port = 30000 + len(self.state_table)
        nat_ip = self.public_ips[0]
        self.state_table[flow_key] = (nat_ip, nat_port)
        self.vm_allocations.setdefault(vm_ip, []).append(nat_port)
        return {"status": "TRANSLATED", "mapping": (nat_ip, nat_port), "vm_ports_in_use": len(self.vm_allocations[vm_ip])}

sim = CloudNATSimulator(public_ips=["203.0.113.10"], min_ports_per_vm=64, dynamic_port_allocation=False)
results = []
for i in range(1, 75):
    res = sim.connect("10.0.1.5", 40000 + i, "203.0.113.80", 443)
    results.append((i, res["status"]))

print(f"Total connections attempted: {len(results)}")
print(f"Successful: {sum(1 for _, s in results if s == 'TRANSLATED')}")
print(f"Dropped: {sim.drops}")
print(f"First drop occurred at attempt: {[i for i, s in results if s == 'DROPPED_PORT_EXHAUSTION'][0]}")
""")),
        stage(3, "Execute Port Exhaustion Simulation",
              "Execute the NAT simulation engine and record connection translation vs drop behavior under static port limits.",
              "Simulation executed: first 64 connections translated successfully; connection 65 dropped due to OUT_OF_RESOURCES.",
              "exhaustion_results.log",
              commands="""python3 nat_engine.py > exhaustion_results.log
cat exhaustion_results.log
"""),
        stage(4, "Simulate Dynamic Port Allocation Remedy",
              "Execute dynamic port allocation simulation allowing VM port slices to expand dynamically up to 1024 ports.",
              "Dynamic port allocation simulation proves all 74 connections translate without drops.",
              "dynamic_results.log",
              commands=write_file("dynamic_sim.py", """from nat_engine import CloudNATSimulator

sim_dyn = CloudNATSimulator(public_ips=["203.0.113.10"], min_ports_per_vm=64, dynamic_port_allocation=True, max_ports=1024)
drops = 0
for i in range(1, 150):
    res = sim_dyn.connect("10.0.1.5", 40000 + i, "203.0.113.80", 443)
    if res["status"] == "DROPPED_PORT_EXHAUSTION":
        drops += 1

print(f"Dynamic Port Allocation: 150 connections attempted, Drops = {drops}, Total Active Ports = {len(sim_dyn.vm_allocations['10.0.1.5'])}")
""") + """python3 dynamic_sim.py > dynamic_results.log
cat dynamic_results.log
"""),
        stage(5, "Inspect Expected State and 5-Tuple Mapping",
              "Inspect sample state table records verifying bidirectional mapping between internal 5-tuple and public NAT IP/port.",
              "Verified state table records show unique 5-tuple translation and port assignment.",
              "state_table.log",
              commands="""python3 -c '
from nat_engine import CloudNATSimulator
sim = CloudNATSimulator(public_ips=["203.0.113.10"])
for i in range(5):
    sim.connect("10.0.1.5", 45000 + i, "203.0.113.80", 443)
for k, v in sim.state_table.items():
    print(f"Internal: {k[0]}:{k[1]} -> Dest: {k[2]}:{k[3]} | NAT: {v[0]}:{v[1]}")
' > state_table.log
cat state_table.log
"""),
        stage(6, "Rehearse Sizing Calculation Matrix",
              "Author a sizing formula script (<samp>nat_sizing.py</samp>) computing required Cloud NAT public IPs given VM count and concurrency.",
              "Sizing matrix script authored calculating public IP capacity requirements across fleet sizes.",
              "sizing_results.txt",
              commands=write_file("nat_sizing.py", """import math

def calculate_nat_capacity(vm_count, avg_concurrency_per_vm):
    total_ports_needed = vm_count * avg_concurrency_per_vm
    usable_ports_per_ip = 64000
    ips_needed = math.ceil(total_ports_needed / usable_ports_per_ip)
    return total_ports_needed, ips_needed

fleets = [
    ("Small Microservices Pool", 50, 100),
    ("Medium E-Commerce Backend", 200, 250),
    ("Large Webhook Notification Fleet", 500, 500),
    ("High-Concurrency Data Ingestion", 1000, 400),
]

print(f"{'Fleet Name':<35} | {'VMs':<5} | {'Conn/VM':<7} | {'Total Ports':<11} | {'Public IPs Needed'}")
print("-" * 75)
for name, vms, conn in fleets:
    ports, ips = calculate_nat_capacity(vms, conn)
    print(f"{name:<35} | {vms:<5} | {conn:<7} | {ports:<11} | {ips} IP(s)")
""") + """python3 nat_sizing.py > sizing_results.txt
cat sizing_results.txt
"""),
        stage(7, "Diagnose Evidence and Author NAT Architectural Standard",
              "Author structured recommendations detailing how Cloud NAT port reservation and dynamic allocation prevent outages.",
              "Architectural standard authored documenting Cloud NAT port planning and monitoring thresholds.",
              "nat_evidence_summary.md",
              commands=write_file("nat_evidence_summary.md", """# Architectural Evidence: SNAT State Tracking and Capacity Sizing

- Finding 1: Static port allocation (e.g. 64 ports/VM) causes silent connection drops as soon as application concurrency exceeds the static reservation.
- Finding 2: The local simplified model rounds usable capacity down to 64,000 ports. Cloud NAT Ports documents 64,512 TCP and 64,512 UDP source ports per NAT IP; destination tuple reuse and per-VM allocation also affect capacity, so dividing concurrency is a conservative toy calculation, not a provider connection limit.
- Architectural Fix: Enable Dynamic Port Allocation on Cloud NAT to permit burst scaling, and configure alerting on router.googleapis.com/nat/nat_allocation_failed.
""")),
        stage(8, "Clean Up and Close Out NAT Exercise",
              "Remove temporary simulation scripts and record completion status.",
              "Simulation scripts removed; sizing results and evidence summary preserved.",
              "cleanup.log",
              commands="""rm -f nat_engine.py dynamic_sim.py nat_sizing.py
echo "Lab 4 closed out cleanly." > cleanup.log
cat cleanup.log
""")
    ],
    accept="Evidence summary proves understanding of SNAT 5-tuple state tracking, port exhaustion mechanics, and Cloud NAT sizing.",
    trouble="Ensure math module is available in Python standard library.",
    file_name="day-004-topic-04.md"
)

# Lab 5
L5_LAB = make_lab(
    covers='forward/return routes on supplied captures',
    name="Routing Table Evaluation, Longest Prefix Match, and BGP Path Selection Analysis",
    goal="Implement a routing lookup engine in Python, evaluate Longest Prefix Match (LPM) and route priority algorithms, and author the canonical Day 4 failure worksheet.",
    expected="A verified routing lookup trace log and the final canonical exit evidence artifact: day-004-failure-worksheet.md.",
    steps=[
        stage(1, "Preflight and Environment Initialization",
              "Inspect local kernel routing table (<kbd>ip route show</kbd>) and initialize routing laboratory workspace.",
              "Local kernel routes inspected; temporary routing workspace initialized.",
              "preflight.log",
              commands=workspace("routing_lab", preflight_text="ip route verified; local routing table inspected; offline execution")),
        stage(2, "Prepare Routing Lookup Engine",
              "Author a Python routing lookup engine (<samp>route_engine.py</samp>) implementing CIDR parsing, Longest Prefix Match, and priority tie-breaking.",
              "Routing engine script authored implementing LPM evaluation over complex overlapping route tables.",
              "route_engine.py",
              commands=write_file("supplied-route-capture.txt", """SUPPLIED ILLUSTRATIVE FIXTURE — not a local packet capture
forward packet: 10.20.1.5 -> 10.50.4.8
forward routes: 10.50.0.0/16 via transit; 10.50.4.0/24 via remote-link
selected forward prefix: 10.50.4.0/24 (longest prefix match)
return packet: 10.50.4.8 -> 10.20.1.5
remote routes: 10.50.4.0/24 connected; no default or other covering route
missing return route: 10.20.0.0/16
ANNOTATION: forward reachability alone does not provide a return path.
""") + write_file("route_engine.py", """import ipaddress
import sys

class RouteTable:
    def __init__(self):
        self.routes = []

    def add_route(self, destination, next_hop, priority=100, origin="STATIC"):
        network = ipaddress.ip_network(destination)
        self.routes.append({
            "network": network,
            "prefix_len": network.prefixlen,
            "next_hop": next_hop,
            "priority": priority,
            "origin": origin
        })

    def lookup(self, ip_str):
        target = ipaddress.ip_address(ip_str)
        matching = [r for r in self.routes if target in r["network"]]
        if not matching:
            return None
        matching.sort(key=lambda r: (-r["prefix_len"], r["priority"]))
        return matching[0]

# Local simulation of the separately supplied forward/return capture.
forward = RouteTable()
forward.add_route("10.50.0.0/16", "transit")
forward.add_route("10.50.4.0/24", "remote-link")
remote = RouteTable()
remote.add_route("10.50.4.0/24", "connected")
print("LOCAL SIMULATION: forward 10.20.1.5 -> 10.50.4.8 selects", forward.lookup("10.50.4.8")["network"])
assert str(forward.lookup("10.50.4.8")["network"]) == "10.50.4.0/24"
assert remote.lookup("10.20.1.5") is None
print("LOCAL SIMULATION: remote lacks return route to 10.20.0.0/16; 10.20.1.5 unreachable")

rt = RouteTable()
rt.add_route("0.0.0.0/0", "Default Internet Gateway", priority=1000, origin="SYSTEM")
rt.add_route("10.0.0.0/8", "Corporate WAN VPN", priority=100, origin="STATIC")
rt.add_route("10.2.0.0/16", "Interconnect Primary (MED 100)", priority=100, origin="BGP")
rt.add_route("10.2.0.0/16", "Interconnect Backup (MED 200)", priority=200, origin="BGP")
rt.add_route("10.2.4.0/24", "High-Speed Database Subnet", priority=100, origin="VPC_PEERING")
rt.add_route("10.2.4.5/32", "Specific DB Primary Node Host", priority=100, origin="STATIC_HOST")

test_ips = ["10.2.4.5", "10.2.4.18", "10.2.8.50", "10.5.0.1", "198.51.100.25"]
print(f"{'Target Destination':<20} | {'Matched Network':<16} | {'Prefix':<6} | {'Next Hop'}")
print("-" * 75)
for ip in test_ips:
    match = rt.lookup(ip)
    print(f"{ip:<20} | {str(match['network']):<16} | /{match['prefix_len']:<5} | {match['next_hop']}")
""")),
        stage(3, "Execute Routing Engine and Validate LPM Decisions",
              "Execute the routing engine and record destination next-hop lookup decisions.",
              "Routing lookup trace generated proving Longest Prefix Match dominates regardless of route origin.",
              "routing_decisions.log",
              commands="""python3 route_engine.py > routing_decisions.log
cat routing_decisions.log
"""),
        stage(4, "Rehearse BGP Path Selection and Asymmetric Route Failure",
              "Author a BGP path selection script (<samp>bgp_eval.py</samp>) simulating tie-breaking across AS-path length and MED.",
              "BGP evaluation script authored demonstrating how MED and AS-path prepending prevent asymmetric routing.",
              "bgp_evaluation.log",
              commands=write_file("bgp_eval.py", """def select_best_bgp(paths):
    sorted_paths = sorted(paths, key=lambda p: (len(p['as_path']), p['med'], p['priority']))
    return sorted_paths[0]

paths_equal = [
    {"name": "Interconnect-A", "as_path": [65001], "med": 100, "priority": 100},
    {"name": "Interconnect-B", "as_path": [65001], "med": 100, "priority": 100},
]

paths_tuned = [
    {"name": "Interconnect-A (Primary)", "as_path": [65001], "med": 100, "priority": 100},
    {"name": "Interconnect-B (Backup)",  "as_path": [65001, 65001], "med": 200, "priority": 100},
]

best_b = select_best_bgp(paths_tuned)
print(f"Tuned BGP Path Selection -> Best Path Selected: {best_b['name']} (MED={best_b['med']}, AS_PATH={best_b['as_path']})")
""") + """python3 bgp_eval.py > bgp_evaluation.log
cat bgp_evaluation.log
"""),
        stage(5, "Inspect Expected State: LPM and BGP Selection Verification",
              "Inspect routing and BGP evaluation logs to verify that LPM and BGP path attributes resolve deterministically.",
              "Logs confirm /32 matches host, /24 matches subnet, /16 matches primary BGP route, and /0 matches default gateway.",
              "inspected_routes.log",
              commands="""grep -E "10.2.4.5|10.2.8.50|Tuned BGP" routing_decisions.log bgp_evaluation.log > inspected_routes.log
cat inspected_routes.log
"""),
        stage(6, "Rehearse Bounded Failure: Static Route Black Hole Injection",
              "Simulate an on-premises link failure where a static route continues forwarding packets versus dynamic BGP withdrawal.",
              "Simulation demonstrates that static route retains black hole path while BGP dynamic route withdraws prefix.",
              "blackhole_test.log",
              commands=write_file("failover_sim.py", """class LinkMonitor:
    def __init__(self, mode="STATIC"):
        self.mode = mode
        self.link_up = True

    def get_status(self):
        if not self.link_up:
            return "ROUTE_WITHDRAWN" if self.mode == "BGP" else "BLACK_HOLE_FORWARDING"
        return "ROUTE_ACTIVE"

print(f"Normal Link State: Static = {LinkMonitor('STATIC').get_status()}, BGP = {LinkMonitor('BGP').get_status()}")
f_static = LinkMonitor("STATIC")
f_static.link_up = False
f_bgp = LinkMonitor("BGP")
f_bgp.link_up = False
print(f"Failed Link State: Static = {f_static.get_status()}, BGP = {f_bgp.get_status()}")
""") + """python3 failover_sim.py > blackhole_test.log
cat blackhole_test.log
"""),
        stage(7, "Author Canonical Exit Evidence: Failure Worksheet",
              "Author the comprehensive Day 4 exit artifact (<samp>day-004-failure-worksheet.md</samp>) separating all five failure domains.",
              "Comprehensive exit artifact authored separating TLS trust, packet size, routing, NAT, and HTTP errors.",
              "day-004-failure-worksheet.md",
              commands=write_file("day-004-failure-worksheet.md", """# Day 4 Exit Evidence: Multi-Layer Network Failure Worksheet

## Purpose
This failure worksheet establishes rigorous diagnostic separation across five foundational cloud networking failure domains:
1. Application Layer (HTTP Semantics and Protocol Status Codes)
2. Cryptographic Security (TLS 1.3 Handshakes and X.509 PKI Trust Chains)
3. Transport Framing (Path MTU Discovery and TCP MSS Clamping)
4. Address Translation (Source NAT, 5-Tuple State Tracking, and Port Sizing)
5. Network Routing (Longest Prefix Match and BGP Path Attribute Selection)

---

## 1. Diagnostic Separation Matrix

| Failure Domain | Primary Protocol / Layer | Observable Symptom & Error Code | Concrete Diagnostic Tool & Command | Root Cause Mechanism | Defensible Engineering Remediation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **HTTP Semantics** | Layer 7 (HTTP/1.1 vs HTTP/2) | HTTP 502 Bad Gateway (`PROTOCOL_ERROR`) | `curl -i --http2 -v https://...` | Ingress proxy received uppercase header names (`X-Custom-Auth`); RFC 9113 section 8.2.1 mandates lowercase. | Configure edge ingress gateway to automatically downcase header field names before HTTP/2 framing. |
| **TLS Trust Chains** | Layer 6 (TLS 1.3 / X.509 PKI) | `SSLError: CertificateError: hostname mismatch` | `openssl s_client -connect host:443 -servername host` followed by `openssl x509 -text -noout` | Leaf certificate contained legacy Common Name but omitted requested FQDN in Subject Alternative Name (SAN). | Reissue leaf certificate from internal CA containing complete `subjectAltName` DNS aliases; automate via Certificate Manager. |
| **Transport Framing** | Layer 3/4 (MTU / TCP MSS) | Small pings succeed; large data transfers hang indefinitely (PMTUD Black Hole) | `ping -M do -s 1472 <dest>` decrementing buffer size; inspect firewall drop logs | Intermediate VPN tunnel MTU is 1400B. Oversized packet has DF=1; intermediate ICMP Type 3 Code 4 feedback was blocked by firewall. | Allow ICMP Type 3 Code 4 in firewall policies; configure TCP MSS clamping to 1360 bytes at the VPN gateway. |
| **Address Translation** | Layer 3/4 (Cloud NAT / SNAT) | `connection timed out`; Cloud NAT log reports `DROPPED: OUT_OF_RESOURCES` | Query metric `router.googleapis.com/nat/nat_allocation_failed` | Worker VM burst concurrency exceeded static allocation of 64 ports/VM; gateway dropped subsequent TCP SYNs. | Enable Dynamic Port Allocation (scaling to 1024 ports/VM) and allocate additional public IPs (64,512 TCP source ports per NAT IP (Ports; the local simplified model rounds capacity down)). |
| **Network Routing** | Layer 3 (Routing / BGP-4) | Latency spikes from 4ms to 70ms; stateful firewall logs `TCP RST (asymmetric flow drop)` | `gcloud compute routers get-status <router>`; trace VPC flow logs | On-prem advertised identical prefix over dual Interconnects with equal AS-path and MED, causing non-deterministic ECMP splitting. | Configure on-prem backup router to advertise MED 200 and prepend its ASN twice; set Cloud Router priority to 100 on primary. |

---

## 2. Forward and Return Path Routing Trace
### Supplied capture annotation (separate from local simulation)
- Forward 10.20.1.5 -> 10.50.4.8 selects 10.50.4.0/24 over 10.50.0.0/16.
- The remote side lacks a return route to 10.20.0.0/16 and has no covering default.
- A request can reach the remote network while the reply cannot reach 10.20.1.5.
- Local route_engine.py simulates those supplied inputs; it does not capture packets
  or observe GCP. Add/advertise the missing return prefix and check both directions
  before predicting restored reachability; BGP tie-breaking alone cannot repair it.
- Supplied MTU capture: 1500-byte IPv4 packet, DF=1, intermediate MTU=1400;
  fragmentation-needed feedback is filtered. Annotate size, feedback and return
  path separately; local MSS calculation predicts 1360 with base IPv4/TCP headers.
- Supplied TLS pair: orders.example.test matches orders.example.test; a certificate
  presenting admin.example.test mismatches that same requested name, despite the
  supplied chain being valid. Keep certificate-trace-comparison.md from Lab 2.

### Additional illustrative hybrid routing design
- **Forward Path (GCP VM 10.128.0.5 -> On-Prem 10.200.15.4):**
  1. VM evaluates local VPC route table: matches `10.200.0.0/16` learned via Cloud Router BGP.
  2. Cloud Router evaluates BGP attributes: selects Interconnect-Primary (MED 100, AS_PATH [65001]) over Backup (MED 200, AS_PATH [65001, 65001]).
  3. Illustrative VPC data plane forwards packet through Interconnect-Primary to on-premises edge router.
  4. On-premises router forwards packet through stateful firewall to destination host.
- **Return Path (On-Prem 10.200.15.4 -> GCP VM 10.128.0.5):**
  1. On-premises host forwards packet to default gateway.
  2. On-premises core router evaluates route to `10.128.0.0/16`: matches primary BGP route advertised by Cloud Router.
  3. Packet returns through Interconnect-Primary to GCP VPC edge, preserving symmetric stateful flow across on-premises firewalls.

---

## 3. Architectural Boundaries and Limitations
- **Tabletop vs Cloud Reality:** These calculations and simulations model deterministic protocol behavior. Cloud testing must verify real-world carrier latency, transit provider route flapping, and ISP-specific MTU reductions.
- **Source Verification:** RFC 9110 (HTTP), RFC 8446 (TLS 1.3), RFC 5280 (X.509), RFC 1191 (PMTUD), RFC 3022 (NAT), and RFC 4271 (BGP-4) accessed 2026-10-04.
""")),
        stage(8, "Clean Up and Close Out Routing Exercise",
              "Verify day-004-failure-worksheet.md exists, remove temporary simulation scripts, and complete laboratory closeout.",
              "Temporary scripts removed; canonical failure worksheet preserved in workspace.",
              "cleanup.log",
              commands="""rm -f route_engine.py bgp_eval.py failover_sim.py
echo "Lab 5 closed out cleanly. Exit artifact saved as day-004-failure-worksheet.md." > cleanup.log
cat cleanup.log
""")
    ],
    accept="Canonical exit evidence day-004-failure-worksheet.md authored, rigorously separating TLS trust, packet size, routing, NAT, and HTTP errors.",
    trouble="Ensure ipaddress module is available in Python 3 standard library.",
    file_name="day-004-topic-05.md"
)

# ==============================================================================
# TOPICS LIST
# ==============================================================================
TOPICS = [
    {
        'key': 'topic-01',
        'title': 'HTTP/HTTPS, status codes, HTTP/1.1 vs HTTP/2 vs HTTP/3',
        'anchors': {
            'overview': 'topic-01-overview',
            'technical': 'topic-01-technical',
            'problem': 'topic-01-problem',
            'lab': 'topic-01-lab'
        },
        'overview': (
            f'{keyword("Hypertext Transfer Protocol")} (HTTP, RFC 9110) governs application-layer request and response semantics across the internet, '
            f'operating in cleartext or over cryptographic TLS tunnels as {keyword("HTTPS")}. '
            f'<strong class="side-heading">Why today:</strong> Day 4 connects Day 3 transport sockets to user-facing application protocol semantics and error classifications. '
            f'<strong class="side-heading">Where it sits:</strong> Terminated at Google Cloud external Application Load Balancers, Cloud CDN edge points of presence, and API gateways.'
        ),
        'preview': (
            "An internal API gateway upgrading from HTTP/1.1 to HTTP/2 encounters 502 Bad Gateway responses on backend requests containing unvalidated uppercase HTTP header field names. "
            "The upstream Envoy ingress proxies drop the malformed streams due to strict HTTP/2 RFC 9113 header normalization rules, causing catalog lookup outages across regional store frontends."
        ),
        'technical': T1_TECH,
        'reference': SOURCES['rfc9110'][1],
        'reference_label': f"{SOURCES['rfc9110'][0]}",
        'questions': [
            "Under what high-concurrency conditions does HTTP/2 stream multiplexing suffer from TCP head-of-line blocking compared to HTTP/3?",
            "Why does an HTTP 502 Bad Gateway response indicate an upstream reverse proxy failure rather than an origin application crash?"
        ],
        'scenario': P1_CASE,
        'lab': L1_LAB
    },
    {
        'key': 'topic-02',
        'title': 'TLS 1.3 handshake and certificate validation chains',
        'anchors': {
            'overview': 'topic-02-overview',
            'technical': 'topic-02-technical',
            'problem': 'topic-02-problem',
            'lab': 'topic-02-lab'
        },
        'overview': (
            f'{keyword("Transport Layer Security")} (TLS 1.3, RFC 8446) establishes authenticated, confidential communication channels using ephemeral Diffie-Hellman key exchange and X.509 PKI. '
            f'<strong class="side-heading">Why today:</strong> Cryptographic verification must precede application payload delivery, preventing eavesdropping and man-in-the-middle attacks. '
            f'<strong class="side-heading">Where it sits:</strong> TLS terminates at supported Google Cloud load balancers; Certificate Manager manages their certificates rather than terminating traffic. Cloud Service Mesh mTLS sidecars are separate context not established by the cited Certificate Manager sections.'
        ),
        'preview': (
            "A newly deployed microservice client reports SSL peer certificate verification failures when connecting to an internal analytics endpoint via its private DNS alias. "
            "The leaf certificate only contains the legacy Common Name for the physical host rather than a Subject Alternative Name for the service alias, causing TLS handshakes to abort immediately and halting data synchronization pipelines."
        ),
        'technical': T2_TECH,
        'reference': SOURCES['rfc8446'][1],
        'reference_label': f"{SOURCES['rfc8446'][0]}",
        'questions': [
            "Why must TLS 1.3 certificate validation chains strictly reject leaf certificates relying solely on the Subject Common Name (CN)?",
            "How does OCSP stapling eliminate the privacy and latency penalties inherent in traditional Certificate Revocation Lists (CRLs)?"
        ],
        'scenario': P2_CASE,
        'lab': L2_LAB
    },
    {
        'key': 'topic-03',
        'title': 'MTU and MSS clamping',
        'anchors': {
            'overview': 'topic-03-overview',
            'technical': 'topic-03-technical',
            'problem': 'topic-03-problem',
            'lab': 'topic-03-lab'
        },
        'overview': (
            f'{keyword("Maximum Transmission Unit")} (MTU) defines the largest physical frame size that can traverse a network segment without fragmentation, '
            f'while {keyword("Maximum Segment Size")} (MSS) dictates the maximum unfragmented TCP payload permitted within that boundary. '
            f'<strong class="side-heading">Why today:</strong> Encapsulation overheads in hybrid cloud VPNs and cross-region VPC links frequently trigger silent packet drops on large payloads while small health checks succeed. '
            f'<strong class="side-heading">Where it sits:</strong> Configured on Google Cloud VPC networks (1460, 1500, or 8896 jumbo MTU), Cloud VPN gateways, and Cloud Interconnect circuits.'
        ),
        'preview': (
            "An application transferring large JSON batch payloads across an IPSec VPN tunnel experiences hanging connections and connection resets while small health checks pass continuously. "
            "An intermediate router with a 1400-byte MTU drops oversized packets with the Don't Fragment bit set while a misconfigured firewall blocks ICMP Type 3 Code 4 feedback messages, creating a Path MTU black hole that stalls batch database replication."
        ),
        'technical': T3_TECH,
        'reference': SOURCES['rfc1191'][1],
        'reference_label': f"{SOURCES['rfc1191'][0]}",
        'questions': [
            "Why does dropping ICMP Type 3 Code 4 messages at a perimeter firewall create a silent Path MTU black hole for large TCP streams?",
            "What is the exact mathematical difference between an interface MTU of 1500 bytes and the resulting TCP MSS value across standard IPv4 headers?"
        ],
        'scenario': P3_CASE,
        'lab': L3_LAB
    },
    {
        'key': 'topic-04',
        'title': 'NAT (SNAT/DNAT) for private outbound',
        'anchors': {
            'overview': 'topic-04-overview',
            'technical': 'topic-04-technical',
            'problem': 'topic-04-problem',
            'lab': 'topic-04-lab'
        },
        'overview': (
            f'{keyword("Network Address Translation")} (NAT, RFC 3022) modifies IP address and port information in packet headers during transit, '
            f'distinguishing Source NAT ({keyword("SNAT")}) for outbound private egress and Destination NAT ({keyword("DNAT")}) for inbound mapping. '
            f'<strong class="side-heading">Why today:</strong> Secure enterprise design requires keeping compute instances private while providing reliable, bounded outbound access to public APIs and patch mirrors. '
            f'<strong class="side-heading">Where it sits:</strong> Provided by Google Cloud NAT attached to Cloud Router, implemented as distributed software-defined translation by Andromeda; the cited Architecture section does not identify a virtual-switch implementation.'
        ),
        'preview': (
            "A cluster of backend worker VMs performing external webhook callbacks exhausts its Cloud NAT source port allocation during a marketing campaign blast. "
            "With minimum ports per VM set statically to 64 and dynamic port allocation disabled, outgoing TCP SYNs are dropped due to NAT port exhaustion, resulting in connection timeouts and backlogged customer notification queues."
        ),
        'technical': T4_TECH,
        'reference': SOURCES['rfc3022'][1],
        'reference_label': f"{SOURCES['rfc3022'][0]}",
        'questions': [
            "How does Cloud NAT dynamic port allocation prevent cross-VM port starvation while scaling to thousands of concurrent outbound API calls?",
            "Why does SNAT maintain connection translation state, and how do matching reply packets differ from unsolicited inbound connections?"
        ],
        'scenario': P4_CASE,
        'lab': L4_LAB
    },
    {
        'key': 'topic-05',
        'title': 'Routing basics',
        'anchors': {
            'overview': 'topic-05-overview',
            'technical': 'topic-05-technical',
            'problem': 'topic-05-problem',
            'lab': 'topic-05-lab'
        },
        'overview': (
            f'{keyword("Routing")} governs how network forwarders determine the optimal multi-hop path for IP packets across complex topologies, '
            f'evaluating Forwarding Information Bases (FIB) using Longest Prefix Match (LPM) algorithms, distinguishing static routes and dynamic {keyword("BGP")} routes. '
            f'<strong class="side-heading">Why today:</strong> Concludes Day 4 by examining the path selection and control-plane protocols that steer enterprise traffic across hybrid interconnects and multi-region clouds. '
            f'<strong class="side-heading">Where it sits:</strong> Configured in Google Cloud VPC route tables (system-generated, custom static, and dynamic routes) and managed via Cloud Router BGP peering.'
        ),
        'preview': (
            "Traffic destined for an on-premises enterprise network from a GCP VPC is routed through an unexpected secondary interconnect link with high latency instead of the primary high-speed link. "
            "The on-premises edge router advertised identical BGP prefixes over both sessions without configuring MED attributes or AS-path prepending, creating an illustrative equal-cost path-selection case whose actual behavior depends on route selection mode and policy and degrade transactional database replication."
        ),
        'technical': T5_TECH,
        'reference': SOURCES['rfc4271'][1],
        'reference_label': f"{SOURCES['rfc4271'][0]}",
        'questions': [
            "When advertising prefixes across redundant Cloud Interconnect links, why does MED only influence route selection within a single Autonomous System?",
            "How does BGP path vector loop prevention (AS_PATH attribute) differ from internal distance-vector split horizon mechanisms?"
        ],
        'scenario': P5_CASE,
        'lab': L5_LAB
    }
]

COMPLETION_HTML = (
    '<p>Save <strong>day-004-failure-worksheet.md</strong> in the Day 1 evidence repository. '
    'The worksheet separates TLS trust, packet size, routing, NAT, and HTTP errors across the five investigated failure domains. '
    'Retain source dates and label all tabletop predictions and untested GCP behavior.</p>\n'
    '<label class="check"><input type="checkbox" data-progress="read-4"> I read and reviewed the day</label>\n'
    '<label class="check"><input type="checkbox" data-progress="artifact-4"> I saved the exit artifact</label>'
)

REVIEW_RECORDS = {
    'source_ledger': {'https://www.rfc-editor.org/rfc/rfc9110.html#section-15': {'heading_opened': '15. Status Codes The status code of a response is a three-digit intege', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://docs.cloud.google.com/load-balancing/docs/https#http2-over-tls': {'heading_opened': 'HTTP/2 over TLS HTTP/2 over TLS is supported for connections between c', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/load-balancing/docs/https/request-distribution#timeouts_and_retries': {'heading_opened': 'Timeouts and retries External Application Load Balancers support the f', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc9113.html#section-8.2.1': {'heading_opened': '8.2.1. Field Validity The definitions of field names and values in HTT', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://docs.cloud.google.com/load-balancing/docs/https#backend-service': {'heading_opened': 'Backend services A backend service provides configuration information', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc9114.html#section-3': {'heading_opened': '3. Connection Setup and Management HTTP relies on the notion of an aut', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc9114.html#section-4': {'heading_opened': '4. Expressing HTTP Semantics in HTTP/3 A client sends an HTTP request', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc9113.html#section-3.2': {'heading_opened': '3.2. Starting HTTP/2 for " https " URIs A client that makes a request', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc9110.html#section-4.2.2': {'heading_opened': '4.2.2. https URI Scheme The "https" URI scheme is hereby defined for m', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://docs.cloud.google.com/load-balancing/docs/https#http3-negotiation': {'heading_opened': 'How HTTP/3 is negotiated When HTTP/3 is enabled, the load balancer adv', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc8446.html#section-4': {'heading_opened': '4 .  Handshake Protocol The handshake protocol is used to negotiate th', 'rfc_status': 'Obsoleted by value found', 'whole_document_reason': None}, 'https://docs.cloud.google.com/certificate-manager/docs/overview#supported-certificates': {'heading_opened': 'Supported TLS certificates Certificate Manager supports the following', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/certificate-manager/docs/overview#benefits': {'heading_opened': 'Benefits Certificate Manager offers the following benefits:', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc5280.html#section-6': {'heading_opened': '6 .  Certification Path Validation Certification path validation proce', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc9525.html#section-6': {'heading_opened': '6. Verifying Service Identity At a high level, the client verifies the', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc1191.html#section-2': {'heading_opened': '2 . Protocol overview In this memo, we describe a technique for using', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://docs.cloud.google.com/vpc/docs/mtu#valid_mtus': {'heading_opened': 'Valid VPC network MTU sizes Virtual Private Cloud (VPC) networks use a', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/vpc/docs/mtu#to-cloudpath': {'heading_opened': 'Communication to Google APIs and services Compute instances using any', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc9293.html#section-3.7.1': {'heading_opened': '3.7.1. Maximum Segment Size Option TCP endpoints MUST implement both s', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://docs.cloud.google.com/vpc/docs/mtu#through-cloud-vpn': {'heading_opened': 'Communication through Cloud VPN tunnels Cloud VPN has both a gateway M', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/mtu-considerations#cloud-vpn-payload-mtu-values': {'heading_opened': 'Cloud VPN payload MTU values', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc3022.html#section-2': {'heading_opened': '2 . Overview of traditional NAT The Address Translation operation pres', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://docs.cloud.google.com/nat/docs/overview#architecture': {'heading_opened': 'Architecture Cloud NAT is a distributed, software-defined managed serv', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/nat/docs/ports-and-addresses#ports': {'heading_opened': 'Ports Each NAT IP address on a Cloud NAT gateway (both Public NAT and', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/nat/docs/ports-and-addresses#dynamic-port': {'heading_opened': 'Dynamic port allocation When you configure dynamic port allocation, yo', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/nat/docs/overview#benefits': {'heading_opened': 'Benefits Cloud NAT provides the following benefits:', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/nat/docs/ports-and-addresses#ports-reuse-endpoints': {'heading_opened': 'Simultaneous port reuse and endpoint-independent mapping Note: The inf', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/nat/docs/monitoring#logging': {'heading_opened': 'Logging Cloud NAT logging lets you log NAT connections and errors. Whe', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc1918.html#section-3': {'heading_opened': '3 . Private Address Space The Internet Assigned Numbers Authority (IAN', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://docs.cloud.google.com/nat/docs/monitoring#vm-metrics': {'heading_opened': 'VM instance metrics The "metric type" strings in this table must be pr', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/nat/docs/monitoring#gateway-metrics': {'heading_opened': 'NAT gateway metrics The "metric type" strings in this table must be pr', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://www.rfc-editor.org/rfc/rfc4271.html#section-3': {'heading_opened': '3 .  Summary of Operation The Border Gateway Protocol (BGP) is an inte', 'rfc_status': 'No Obsoleted by value found', 'whole_document_reason': None}, 'https://docs.cloud.google.com/vpc/docs/routes#routeselection': {'heading_opened': 'Routing order There might be more than one applicable route for a give', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/vpc/docs/routes#types_of_routes': {'heading_opened': 'Route types The following tables summarize how Google Cloud categorize', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/network-connectivity/docs/router/concepts/overview#key': {'heading_opened': 'Key features Cloud Router offers the following features:', 'rfc_status': 'not applicable', 'whole_document_reason': None}, 'https://docs.cloud.google.com/network-connectivity/docs/router/concepts/learned-routes#dynamic-routing-mode': {'heading_opened': 'Dynamic routing mode The dynamic routing mode of a VPC network affects', 'rfc_status': 'not applicable', 'whole_document_reason': None}},
    'product_claims': [
        {
            'claim': 'Google Cloud External Application Load Balancers terminate client HTTP/HTTPS traffic at the edge and generate standardized synthetic status codes including 502 with failed_to_pick_backend.',
            'section_url': 'https://docs.cloud.google.com/load-balancing/docs/https#http2-over-tls',
            'heading_opened': 'HTTP/2 over TLS'
        },
        {
            'claim': 'For external Application Load Balancer backend services, the documented backend HTTP keepalive timeout is 600 seconds, recommending backend web servers configure keep-alive timeouts greater than 600 seconds.',
            'section_url': 'https://docs.cloud.google.com/load-balancing/docs/https#http2-over-tls',
            'heading_opened': 'HTTP/2 over TLS'
        },
        {
            'claim': 'Google Cloud External Application Load Balancers provide native HTTP/2 and HTTP/3 support at the global edge network, negotiating protocols via ALPN and advertising HTTP/3 via Alt-Svc headers.',
            'section_url': 'https://docs.cloud.google.com/load-balancing/docs/https#http3-negotiation',
            'heading_opened': 'How HTTP/3 is negotiated'
        },
        {
            'claim': 'Google Cloud Certificate Manager provides centralized management of Google-managed and self-managed SSL certificates with Certificate Maps and DNS Authorizations.',
            'section_url': 'https://docs.cloud.google.com/certificate-manager/docs/overview#supported-certificates',
            'heading_opened': 'Supported TLS certificates'
        },
        {
            'claim': 'Google Cloud Load Balancing supports SSL policies to enforce minimum TLS versions and curated cipher profiles.',
            'section_url': 'https://docs.cloud.google.com/certificate-manager/docs/overview#benefits',
            'heading_opened': 'Benefits'
        },
        {
            'claim': 'Google Cloud VPC networks support configurable MTUs of 1460, 1500, and 8896 bytes, with Cloud VPN defining separate gateway and payload MTU values.',
            'section_url': 'https://docs.cloud.google.com/vpc/docs/mtu#valid_mtus',
            'heading_opened': 'Valid VPC network MTU sizes'
        },
        {
            'claim': 'Google Cloud NAT is a software-defined managed service that configures Andromeda SDN to provide source network address translation without proxy VMs.',
            'section_url': 'https://docs.cloud.google.com/nat/docs/overview#architecture',
            'heading_opened': 'Architecture'
        },
        {
            'claim': 'Cloud NAT offers static and dynamic port allocation, logging of translated flows, and integration with Cloud Monitoring metrics.',
            'section_url': 'https://docs.cloud.google.com/nat/docs/ports-and-addresses#ports',
            'heading_opened': 'Ports'
        },
        {
            'claim': 'Google Cloud VPC routing uses staged routing order where special paths precede subnet and custom routes, with priorities and specificity evaluated in documented order.',
            'section_url': 'https://docs.cloud.google.com/vpc/docs/routes#routeselection',
            'heading_opened': 'Routing order'
        },
        {
            'claim': 'Cloud Router manages dynamic routes via BGP peering sessions over Cloud VPN and Cloud Interconnect, supporting regional or global dynamic routing modes.',
            'section_url': 'https://docs.cloud.google.com/network-connectivity/docs/router/concepts/overview#key',
            'heading_opened': 'Key features'
        }
    ],
    'visual_reasons': {
        'BGP Route Advertisement, Evaluation, and Packet Forwarding': 'retained from committed spec',
        'HTTP Versions: Connection Setup and First Request Sequences': 'retained from committed spec',
        'HTTP/HTTPS, status codes, HTTP/1.1 vs HTTP/2 vs HTTP/3: Failure Cascade vs Corrected Control': 'retained from committed spec',
        'MTU and MSS clamping: Failure Cascade vs Corrected Control': 'retained from committed spec',
        'NAT (SNAT/DNAT) for private outbound: Failure Cascade vs Corrected Control': 'retained from committed spec',
        'Path MTU Discovery and TCP MSS Clamping Packet Traversal': 'retained from committed spec',
        'Routing basics: Failure Cascade vs Corrected Control': 'retained from committed spec',
        'TLS 1.3 1-RTT Handshake: Key Exchange and Certificate Validation': 'retained from committed spec',
        'TLS 1.3 handshake and certificate validation chains: Failure Cascade vs Corrected Control': 'retained from committed spec',
        'VPC Private Outbound: SNAT and Return DNAT Packet Lifecycle': 'retained from committed spec',
        'X.509 PKI Certificate Validation Chain Sequence (RFC 5280)': 'eligible flow sequence illustrating RFC 5280 certificate chain and cryptographic verification sequence requested by user',
        'OCSP Stapling and Revocation Verification Lifecycle (RFC 6066 / RFC 6960)': 'eligible flow sequence illustrating RFC 6066 and RFC 6960 out-of-band query, edge caching, and in-band TLS stapling lifecycle requested by user'
    }
}

def _bullet_explanation(match):
    """Keep every authored word; break prose only at unmarked sentence ends."""
    label, body = match.groups()
    if not body.strip() or 'Further study:' in label:
        return match.group(0)
    points, pending, depth = [], '', 0
    for token in re.findall(r'<[^>]+>|[^<]+', body):
        if token.startswith('<'):
            if token.startswith('</'):
                depth -= 1
            elif not token.endswith('/>'):
                depth += 1
            pending += token
        elif depth:
            pending += token
        else:
            start = 0
            for boundary in re.finditer(r'(?<=\.)\s+(?=[A-Z])', token):
                prefix = token[:boundary.start()]
                if prefix.endswith(('e.g.', 'i.e.', 'vs.', 'Fig.')):
                    continue
                pending += token[start:boundary.start()]
                points.append(pending.strip())
                pending = ''
                start = boundary.end()
            pending += token[start:]
    if pending.strip():
        points.append(pending.strip())
    return '<p>' + label + '</p><ul>' + ''.join(
        '<li>' + point + '</li>' for point in points
    ) + '</ul>'


# Day-local presentation: shared shell/CSS and teaching content stay unchanged.
for _topic in TOPICS:
    _headings = re.findall(r'<h4>(.*?)</h4>', _topic['technical'], re.S)
    _links = []
    for _number, _heading in enumerate(_headings, 1):
        _anchor = f"{_topic['key']}-subtopic-{_number:02d}"
        _topic['technical'] = _topic['technical'].replace(
            '<h4>' + _heading + '</h4>',
            f'<h4 id="{_anchor}">' + _heading + '</h4>', 1
        )
        _links.append(f'<li><a href="#{_anchor}">{_heading}</a></li>')
    _linked_list = '<ul>' + ''.join(_links) + '</ul>'
    _topic['technical'] = re.sub(
        r'(<p><strong class="side-heading">Subtopics in this discussion:</strong></p>)<ol>.*?</ol>',
        lambda match: match.group(1) + _linked_list,
        _topic['technical'], count=1, flags=re.S
    )
    _topic['technical'] = re.sub(
        r'<p>(<strong class="side-heading">[^<]+</strong>)\s*(.*?)</p>',
        _bullet_explanation, _topic['technical'], flags=re.S
    )
    _overview_end = f'<p><a href="#{_topic["key"]}-technical">'
    PART1_HTML = PART1_HTML.replace(
        _overview_end,
        '<p><strong class="side-heading">Linked subtopics:</strong></p>'
        + _linked_list + '\n' + _overview_end, 1
    )


DATA = {
    'contract_version': 2,
    'roadmap_practice': 'Compare a valid and a hostname-mismatched certificate trace; annotate an MTU failure and forward/return routes on supplied captures.',
    'roadmap_exit': 'A failure worksheet that separates TLS trust, packet size, routing and HTTP errors.',
    'day': DAY,
    'lab_defaults': {},
    'work_block': WORK_BLOCK,
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
    'sources': SOURCES,
    'access_date': ACCESS_DATE,
    'review_records': REVIEW_RECORDS
}
