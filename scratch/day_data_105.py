"""day_data_105.py — Exhaustive architecture data specification for Day 105.

Covers TLS Everywhere (Managed Certs, mTLS, CAS), Secure Hybrid Connectivity (MACsec, HA VPN),
Bastion Patterns vs IAP TCP Forwarding, and DNS Security (DNSSEC, DNS Logging).
"""

DAY_NUM = 105

DATA = {
    'day': 105,
    'part1_intro': (
        'Day 105 focuses on cryptographic transport security, enterprise identity attestation, and hybrid boundary '
        'isolation across Google Cloud. Architects evaluate TLS termination patterns and bidirectional cryptographic '
        'authentication (mTLS) backed by private Certificate Authority Service (CAS), secure hybrid link-layer and '
        'network-layer encryption via MACsec and HA VPN IPsec, zero-public-IP administrative access using IAP TCP '
        'forwarding over legacy bastion jumphosts, and authoritative DNS integrity using DNSSEC and query audit logging.'
    ),
    'exit_summary': (
        'Engineers design and verify an enterprise certificate rotation trace, mTLS service mesh attestation pipeline, '
        'hybrid link-layer MACsec versus IPsec encapsulation model, IAP tunneling security policy, and DNSSEC chain-of-trust '
        'ownership matrix meeting all Day 105 Exit evidence criteria.'
    ),
    'part2_intro': (
        'The technical comparison below analyzes the trade-offs, OSI layer operational boundaries, cryptographic protocols, '
        'and administrative ownership models across Google Cloud transport security architectures.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Transport Security Pattern</th>\n'
        '<th>OSI Layer &amp; Protocol</th>\n'
        '<th>Cryptographic Boundary</th>\n'
        '<th>Key / Cert Lifecycle Owner</th>\n'
        '<th>Failure Signal &amp; Blast Radius</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>Google-Managed SSL / TLS</strong></td>\n'
        '<td>Layer 7 (TLS 1.3 / ALPN)</td>\n'
        '<td>Edge Google Front End (GFE) / Cloud Load Balancing</td>\n'
        '<td>Automated Google CA / Let\'s Encrypt (90-day rotation)</td>\n'
        '<td>CAA record mismatch or ACME DNS challenge failure; drops all external client ingress.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Mutual TLS (mTLS) with CAS</strong></td>\n'
        '<td>Layer 7 (Client &amp; Server X.509)</td>\n'
        '<td>End-to-end between client and mesh proxy / ALB backend</td>\n'
        '<td>Enterprise Private CA Service (DevOps / Security PKI)</td>\n'
        '<td>Client certificate expiration or revoked root CA; handshake terminates with TLS alert 42 (bad_certificate).</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>MACsec on Cloud Interconnect</strong></td>\n'
        '<td>Layer 2 (IEEE 802.1AE)</td>\n'
        '<td>Point-to-point physical link between on-prem router and Google Colocation edge</td>\n'
        '<td>Shared Pre-Shared Key (CAK/CKN) stored in Cloud Secret Manager</td>\n'
        '<td>Key mismatch disables L2 Ethernet frames; immediate BGP session collapse across 100G interconnect.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Cloud HA VPN (IPsec)</strong></td>\n'
        '<td>Layer 3 (IPsec ESP / IKEv2)</td>\n'
        '<td>Gateway-to-gateway across public internet / transit providers</td>\n'
        '<td>IKE pre-shared secret &amp; automated BGP rekeying</td>\n'
        '<td>Phase 1/2 cryptographic proposal mismatch; tunnels remain DOWN, rerouting to secondary peer.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>IAP TCP Forwarding</strong></td>\n'
        '<td>Layer 7 IAM Encapsulated over TLS WebSocket</td>\n'
        '<td>Client workstation to Google Cloud identity endpoint (35.235.240.0/20)</td>\n'
        '<td>Google OAuth2 token &amp; short-lived tunnel session keys</td>\n'
        '<td>Missing `roles/iap.tunnelResourceAccessor` or Context-Aware Access denial; SSH/RDP session rejected at proxy.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Cloud DNSSEC</strong></td>\n'
        '<td>Application / DNS (RRSIG, DNSKEY, DS)</td>\n'
        '<td>Recursive resolver validation chain to root zone</td>\n'
        '<td>Automated KSK / ZSK rotation via Google Cloud DNS</td>\n'
        '<td>Stale DS record at registrar; entire domain returns SERVFAIL for all validating public resolvers.</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 105: Multi-Tier Transport Cryptography, Hybrid Tunneling, and Identity Proxy Topology',
        'desc': 'Architectural layout illustrating Google Front End TLS termination, mTLS service mesh verification via Private CAS, MACsec and HA VPN hybrid transport, IAP TCP forwarding, and DNSSEC authoritative validation.',
        'caption': 'Figure 105.1: Multi-boundary enterprise encryption architecture detailing Layer 2 MACsec, Layer 3 HA VPN IPsec, Layer 7 mTLS via Certificate Authority Service, IAP TCP access, and DNSSEC cryptographic trust chains.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Edge Cryptography & Authoritative DNS Resolution',
                'desc': 'Cloud DNS with DNSSEC validation, GFE anycast edge, and automated Google-managed TLS termination',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Identity-Aware Proxy & Zero-Public-IP Administrative Access',
                'desc': 'IAP TCP forwarding gateway on 35.235.240.0/20 routing SSH/RDP over authenticated TLS WebSockets',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Internal Microservice Mutual TLS (mTLS) & Private CAS Plane',
                'desc': 'Certificate Authority Service (CAS) root/subordinate pool issuing ephemeral X.509 certs to Envoy sidecars',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Secure Hybrid Connectivity Plane (MACsec & HA VPN)',
                'desc': 'Dedicated Interconnect with line-rate L2 IEEE 802.1AE MACsec and Layer 3 HA VPN IKEv2 IPsec fallback',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: On-Premises Data Center & Corporate Operations Boundary',
                'desc': 'Customer Edge Routers, hardware security modules, enterprise directory, and auditing SIEM collectors',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Cloud DNSSEC Zone', 'detail': 'KSK/ZSK Signed RRSIG', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'External Application LB', 'detail': 'GFE Managed TLS 1.3', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'IAP TCP Tunnel Gateway', 'detail': '35.235.240.0/20 CIDR', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Target Private VM', 'detail': 'SSH via Port 22 (No Pub IP)', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Private CA Service', 'detail': 'Subordinate Issuing Pool', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Service Mesh Envoy Pods', 'detail': 'mTLS SPIFFE / SAN Auth', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Dedicated Interconnect', 'detail': '100G MACsec L2 Encrypted', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Cloud HA VPN Gateway', 'detail': 'Dual IPsec ESP Tunnels', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'On-Prem Border Router', 'detail': 'BGP Peer & CKN/CAK Key', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'Enterprise Audit SIEM', 'detail': 'DNS Query & IAP Logs', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'EDGE INGRESS & ACCESS CONTROL VAULT', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'INTERNAL SERVICE MESH & HYBRID TRANSIT ENCLAVE', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'ENTERPRISE HYBRID EXTENSION & ON-PREM EDGE', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Validate DNSSEC & Route', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Tunnel Admin Access', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Forward SSH Payload', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Issue Workload Certs', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Enforce Bidirectional mTLS', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Cross-Cloud Interconnect', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Failover to HA VPN IPsec', 'type': 'warn'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Encrypt L2 Wire (MACsec)', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Stream Forensics to SIEM', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: IAP Tunnel Authentication & Context Check', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: CAS Certificate Validity & CRL / OCSP Revocation', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 345, 'label': 'PROBE 3: MACsec Line-Rate Framing & CAK Key Rotation', 'badge': 'P3', 'color': '#f43f5e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world transport encryption failures, certificate chain breakdowns, '
        'hybrid connectivity disruptions, and perimeter bypass attempts. Each case details verbatim diagnostic logs, root cause '
        'mechanisms, production remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on exercises execute the complete 8-stage operational engineering lifecycle for Day 105. '
        'Architects configure managed certificate profiles, author private Certificate Authority Service pools, '
        'deploy IAP TCP forwarding firewall rules, and establish cryptographically signed DNSSEC zones with query auditing.'
    ),
    'topics': [
        {
            'key': 'topic-01',
            'title': 'TLS everywhere: managed certificates, mTLS, Certificate Authority Service',
            'overview': (
                'Enterprise workloads require pervasive cryptographic transport security across public ingress, internal '
                'microservices, and third-party integrations. Google Cloud Certificate Manager provides scalable, automated '
                'TLS provisioning with DNS-authorization and wildcard support at the edge. Within the private VPC, Mutual TLS '
                '(mTLS) enforces cryptographic client identity verification using ephemeral X.509 certificates issued by '
                'Google Cloud Certificate Authority Service (CAS), eliminating shared secret anti-patterns.'
            ),
            'preview': (
                'An external payment webhook rejects incoming orders because the application load balancer certificate lacks '
                'an intermediate trust bundle; mTLS ensures both server and client validate cryptographic identity.'
            ),
            'technical': (
                '### 1. Edge TLS vs. Internal Mutual TLS (mTLS)\n'
                '- **Public Ingress TLS:** External Application Load Balancers terminate client TLS sessions at the GFE edge. '
                'Google-managed certificates automate 90-day renewals using ACME DNS or HTTP challenges. Certificate Manager '
                'allows attaching up to 1,000,000 certificates per load balancer via Certificate Maps.\n'
                '- **Mutual TLS (mTLS):** In zero-trust networks, server authentication is insufficient. The server requests '
                'and validates a client X.509 certificate during the TLS handshake. Certificate Authority Service (CAS) '
                'acts as the highly available, managed PKI root/subordinate tier, issuing short-lived workload certificates '
                'integrated with Cloud Service Mesh and SPIFFE IDs.\n'
                '\n'
                '### 2. Certificate Authority Service (CAS) Architecture\n'
                '- **CA Pools:** Group certificate authorities with common IAM policies, issuance modes, and certificate revocation '
                'lists (CRLs).\n'
                '- **Tiers:** DevOps Tier (optimized for high-volume, short-lived container certificates, 30-day CRLs) vs. '
                'Enterprise Tier (FIPS 140-2 Level 3 HSM-backed keys, strict auditing, comprehensive compliance certifications).\n'
                '- **Rotation Mechanics:** Subordinate CAs must be renewed before expiration; workload sidecars utilize Automated '
                'Certificate Management protocols to refresh leaf certs every 24 hours.'
            ),
            'questions': [
                'Why should microservice-to-microservice traffic utilize mTLS with Private CAS rather than public Google-managed certificates?',
                'What is the architectural difference between the DevOps Tier and Enterprise Tier in Google Cloud CAS?',
                'How does Certificate Manager use Certificate Maps to overcome traditional SSL certificate limits on Cloud Load Balancing?'
            ],
            'reference': 'https://cloud.google.com/certificate-authority-service/docs/overview',
            'reference_label': 'Google Cloud Certificate Authority Service: Architecture and CA pool management',
            'scenario': {
                'symptom': 'Internal payment ingestion API fails with HTTP 502 Bad Gateway and upstream TLS alert `unknown_ca` (SSL alert 48).',
                'constraints': 'Zero-trust architecture mandates all internal RPC calls must enforce mutual TLS; no unencrypted plaintext in VPC.',
                'evidence': (
                    'Envoy sidecar proxy log showing certificate verification failure:\n\n'
                    '```json\n'
                    '{\n'
                    '  "response_flags": "UC",\n'
                    '  "upstream_transport_failure_reason": "TLS_error:|268435581:SSL_routines:OPENSSL_internal:CERTIFICATE_VERIFY_FAILED:ssl/tls_record.cc:291",\n'
                    '  "connection_termination_details": "peer_certificate_verification_failed: unable to get local issuer certificate",\n'
                    '  "downstream_remote_address": "10.128.0.45:49182",\n'
                    '  "upstream_host": "10.128.1.12:8443"\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: The calling client sidecar was issued a new leaf certificate from a freshly created CAS subordinate pool, '
                    'but the receiving server sidecar trust bundle had not been updated with the new subordinate CA root.'
                ),
                'diagnostic_steps': [
                    'Inspect Envoy sidecar logs on both caller and receiver pods for SSL handshake termination details.',
                    'Extract the active server trust store bundle using `openssl s_client -connect 10.128.1.12:8443 -showcerts`.',
                    'Query Certificate Authority Service for the issuing subordinate CA certificate chain.',
                    'Confirm whether the server trust anchor includes the full subject key identifier (SKI) of the new issuing CA.'
                ],
                'root': 'The receiving service trust bundle only contained the root CA certificate and omitted the intermediate subordinate CA certificate that signed the client leaf.',
                'fix': 'Update the trust config map across the service mesh to distribute the complete CAS CA pool bundle containing root and intermediate signing certificates.',
                'verify': 'Initiate mutual TLS curl probe passing client certificate and verifying full chain validation without errors.',
                'residual': 'Workloads must reload trust bundles dynamically without requiring full container restart to prevent downtime during CA rotations.',
                'diagram': (
                    'Client attempts mTLS handshake with new subordinate cert',
                    'Server trust store missing intermediate CAS certificate',
                    'TLS handshake terminated with SSL CERTIFICATE_VERIFY_FAILED',
                    'Publish full CA pool intermediate chain to service trust store',
                    'mTLS handshake completes; mutual cryptographic identity verified'
                )
            },
            'lab': {
                'name': 'Mutual TLS Certificate Authority Chain & Rotation',
                'goal': 'Generate a local PKI hierarchy with root CA, intermediate subordinate CA, server, and client certs, and verify mTLS handshake validation and rotation.',
                'expected': 'Functional OpenSSL and Python mTLS verification script demonstrating mutual client/server certificate validation and rejection of untrusted certificates.',
                'mode': 'Local shell and OpenSSL PKI simulation',
                'prereq': 'OpenSSL 1.1.1+ and Python 3.9+ installed.',
                'preflight': 'Verify OpenSSL binary and create a clean isolated working directory `~/mtls-lab`.',
                'steps': [
                    (
                        '#### Environment Preflight & Tooling Check\n'
                        'Confirm OpenSSL availability and establish workspace:\n\n'
                        '```sh\n'
                        'mkdir -p ~/mtls-lab && cd ~/mtls-lab\n'
                        'openssl version\n'
                        'python3 --version\n'
                        'echo "[PASS] Tooling preflight successful."\n'
                        '```'
                    ),
                    (
                        '#### Root Certificate Authority (CA) Generation\n'
                        'Generate an RSA 4096-bit private key and self-signed root certificate simulating Enterprise CAS Root:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > generate_pki.sh\n'
                        '#!/usr/bin/env bash\n'
                        'set -euo pipefail\n'
                        '# 1. Root CA\n'
                        'openssl genrsa -out root_ca.key 4096\n'
                        'openssl req -x509 -new -nodes -key root_ca.key -sha256 -days 365 \\\n'
                        '  -subj "/C=US/ST=California/O=Brightloaf/OU=Security/CN=Brightloaf-Root-CA" \\\n'
                        '  -out root_ca.crt\n'
                        '\n'
                        '# 2. Subordinate Intermediate CA\n'
                        'openssl genrsa -out sub_ca.key 2048\n'
                        'openssl req -new -key sub_ca.key -out sub_ca.csr \\\n'
                        '  -subj "/C=US/ST=California/O=Brightloaf/OU=Mesh/CN=Brightloaf-Sub-CA"\n'
                        '\n'
                        'cat <<\'EXT\' > sub_ca.ext\n'
                        'basicConstraints=critical,CA:TRUE,pathlen:0\n'
                        'keyUsage=critical,digitalSignature,keyCertSign,cRLSign\n'
                        'EXT\n'
                        '\n'
                        'openssl x509 -req -in sub_ca.csr -CA root_ca.crt -CAkey root_ca.key \\\n'
                        '  -CAcreateserial -out sub_ca.crt -days 180 -sha256 -extfile sub_ca.ext\n'
                        '\n'
                        '# 3. Concatenate CA Chain Bundle\n'
                        'cat sub_ca.crt root_ca.crt > ca_chain.crt\n'
                        'echo "[PASS] Root and Subordinate CAs generated successfully."\n'
                        'EOF\n'
                        'bash generate_pki.sh\n'
                        '```'
                    ),
                    (
                        '#### Server and Client Certificate Issuance\n'
                        'Issue server and client leaf certificates signed by the subordinate CA:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > issue_leaf_certs.sh\n'
                        '#!/usr/bin/env bash\n'
                        'set -euo pipefail\n'
                        '# Server Cert with SAN\n'
                        'openssl genrsa -out server.key 2048\n'
                        'openssl req -new -key server.key -out server.csr \\\n'
                        '  -subj "/C=US/ST=California/O=Brightloaf/OU=Payments/CN=payments.internal"\n'
                        '\n'
                        'cat <<\'EXT\' > server.ext\n'
                        'basicConstraints=CA:FALSE\n'
                        'keyUsage=digitalSignature,keyEncipherment\n'
                        'extendedKeyUsage=serverAuth\n'
                        'subjectAltName=DNS:payments.internal,DNS:localhost,IP:127.0.0.1\n'
                        'EXT\n'
                        '\n'
                        'openssl x509 -req -in server.csr -CA sub_ca.crt -CAkey sub_ca.key \\\n'
                        '  -CAcreateserial -out server.crt -days 30 -sha256 -extfile server.ext\n'
                        '\n'
                        '# Client Cert with SAN\n'
                        'openssl genrsa -out client.key 2048\n'
                        'openssl req -new -key client.key -out client.csr \\\n'
                        '  -subj "/C=US/ST=California/O=Brightloaf/OU=Orders/CN=orders-service"\n'
                        '\n'
                        'cat <<\'EXT\' > client.ext\n'
                        'basicConstraints=CA:FALSE\n'
                        'keyUsage=digitalSignature,keyEncipherment\n'
                        'extendedKeyUsage=clientAuth\n'
                        'subjectAltName=DNS:orders.internal\n'
                        'EXT\n'
                        '\n'
                        'openssl x509 -req -in client.csr -CA sub_ca.crt -CAkey sub_ca.key \\\n'
                        '  -CAcreateserial -out client.crt -days 30 -sha256 -extfile client.ext\n'
                        'echo "[PASS] Server and Client certificates issued."\n'
                        'EOF\n'
                        'bash issue_leaf_certs.sh\n'
                        '```'
                    ),
                    (
                        '#### Mutual TLS Validation Engine\n'
                        'Execute Python verification server and client enforcing bidirectional TLS certificate exchange:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > test_mtls.py\n'
                        'import socket\n'
                        'import ssl\n'
                        'import threading\n'
                        'import time\n'
                        '\n'
                        'def run_server():\n'
                        '    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)\n'
                        '    context.verify_mode = ssl.CERT_REQUIRED\n'
                        '    context.load_verify_locations(cafile="ca_chain.crt")\n'
                        '    context.load_cert_chain(certfile="server.crt", keyfile="server.key")\n'
                        '\n'
                        '    bind_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n'
                        '    bind_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n'
                        '    bind_socket.bind(("127.0.0.1", 18443))\n'
                        '    bind_socket.listen(5)\n'
                        '\n'
                        '    conn, addr = bind_socket.accept()\n'
                        '    with context.wrap_socket(conn, server_side=True) as sconn:\n'
                        '        peer_cert = sconn.getpeercert()\n'
                        '        subject = dict(x[0] for x in peer_cert[\'subject\'])\n'
                        '        print(f"[SERVER] Handshake Success! Authenticated Client CN: {subject.get(\'commonName\')}")\n'
                        '        sconn.sendall(b"HTTP/1.1 200 OK\\r\\nContent-Length: 17\\r\\n\\r\\nMTLS-AUTH-SUCCESS")\n'
                        '    bind_socket.close()\n'
                        '\n'
                        'server_thread = threading.Thread(target=run_server)\n'
                        'server_thread.daemon = True\n'
                        'server_thread.start()\n'
                        'time.sleep(1)\n'
                        '\n'
                        'client_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="ca_chain.crt")\n'
                        'client_context.load_cert_chain(certfile="client.crt", keyfile="client.key")\n'
                        '\n'
                        'raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n'
                        'with client_context.wrap_socket(raw_sock, server_hostname="localhost") as csock:\n'
                        '    csock.connect(("127.0.0.1", 18443))\n'
                        '    server_cert = csock.getpeercert()\n'
                        '    srv_sub = dict(x[0] for x in server_cert[\'subject\'])\n'
                        '    print(f"[CLIENT] Handshake Success! Authenticated Server CN: {srv_sub.get(\'commonName\')}")\n'
                        '    csock.sendall(b"GET / HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n")\n'
                        '    data = csock.recv(1024)\n'
                        '    print(f"[CLIENT] Received: {data.decode().splitlines()[0]}")\n'
                        'EOF\n'
                        'python3 test_mtls.py\n'
                        '```'
                    ),
                    (
                        '#### Negative Testing: Rejection of Untrusted Client\n'
                        'Generate a rogue self-signed client certificate and verify that server strictly drops connection:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > test_rogue_client.py\n'
                        'import socket\n'
                        'import ssl\n'
                        'import subprocess\n'
                        '\n'
                        '# Create rogue key/cert signed by unknown authority\n'
                        'subprocess.run("openssl req -x509 -newkey rsa:2048 -keyout rogue.key -out rogue.crt -days 1 -nodes -subj \'/CN=rogue-attacker\'", shell=True, check=True)\n'
                        '\n'
                        'client_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="ca_chain.crt")\n'
                        'client_context.load_cert_chain(certfile="rogue.crt", keyfile="rogue.key")\n'
                        '\n'
                        'try:\n'
                        '    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n'
                        '    with client_context.wrap_socket(raw_sock, server_hostname="localhost") as csock:\n'
                        '        csock.connect(("127.0.0.1", 18443))\n'
                        '    print("[FAIL] Rogue client connection unexpectedly succeeded!")\n'
                        'except ssl.SSLError as e:\n'
                        '    print(f"[PASS] Server deterministically rejected rogue client: {e}")\n'
                        'EOF\n'
                        'python3 test_rogue_client.py\n'
                        '```'
                    )
                ],
                'accept': 'Complete mTLS handshake transcript proving bidirectional identity attestation and successful deterministic rejection of untrusted certificates.',
                'verification': 'Verify `root_ca.crt`, `sub_ca.crt`, `server.crt`, and `client.crt` fingerprints and inspect Python verification output.',
                'trouble': 'If handshake fails with certificate untrusted, ensure `ca_chain.crt` contains both subordinate and root certificates.',
                'cleanup': 'Remove test certificates and keys: `rm -rf ~/mtls-lab`.',
                'file': 'day-105-mtls-pki.md'
            }
        },
        {
            'key': 'topic-02',
            'title': 'Secure hybrid connectivity: MACsec for Interconnect, HA VPN encryption',
            'overview': (
                'Connecting on-premises infrastructure to Google Cloud requires defense-in-depth transport cryptography. '
                'Cloud Interconnect provides dedicated, high-bandwidth private circuits, but physical cables traverse '
                'third-party facilities; MACsec (IEEE 802.1AE) provides line-rate hardware encryption at Layer 2. '
                'For internet-routed connections, Cloud HA VPN provides 99.99% SLA-backed Layer 3 IPsec encapsulation (IKEv2, AES-GCM).'
            ),
            'preview': (
                'An enterprise border router renegotiates an IPsec security association causing a 200ms packet stall; '
                'combining MACsec on Dedicated Interconnect with HA VPN delivers wire-speed encryption with automated cryptographic failover.'
            ),
            'technical': (
                '### 1. MACsec on Cloud Interconnect (Layer 2)\n'
                '- **Standard:** IEEE 802.1AE encrypts all Ethernet frames at the physical link layer between customer on-prem edge routers '
                'and Google Cloud colocation points of presence (PoPs).\n'
                '- **Line-Rate Performance:** Encrypts at 10 Gbps and 100 Gbps speeds with zero CPU overhead or packet fragmentation.\n'
                '- **Key Agreement (MKA):** Uses Connectivity Association Keys (CAKs) and Connectivity Key Names (CKNs) stored securely '
                'in Google Cloud Secret Manager and synchronized with the on-premise hardware.\n'
                '\n'
                '### 2. Cloud HA VPN (Layer 3 IPsec)\n'
                '- **SLA & Architecture:** Cloud HA VPN guarantees 99.99% availability by enforcing two active tunnels per gateway across '
                'independent Google Cloud failure domains.\n'
                '- **Encapsulation:** Uses IPsec Encapsulating Security Payload (ESP) in tunnel mode, paired with IKEv2 and dynamic BGP routing.\n'
                '- **Crypto Suites:** Recommends `AES-GCM-256` with Diffie-Hellman Group 19/20 for Perfect Forward Secrecy (PFS).'
            ),
            'questions': [
                'Why does MACsec provide superior throughput and lower latency compared to IPsec for hybrid interconnects?',
                'Under what circumstances would an architect run HA VPN IPsec over Cloud Interconnect (VPN over Interconnect)?',
                'What is the operational impact on BGP sessions when a MACsec pre-shared key (CAK) expires?'
            ],
            'reference': 'https://cloud.google.com/network-connectivity/docs/interconnect/concepts/macsec-overview',
            'reference_label': 'Google Cloud Interconnect: MACsec encryption architecture and key management',
            'scenario': {
                'symptom': 'Dedicated Interconnect interface drops all traffic during scheduled CKN key rotation, causing multi-region failover.',
                'constraints': 'Financial compliance requires uninterrupted L2 encryption on all physical transoceanic circuits.',
                'evidence': (
                    'Cisco IOS-XE syslog showing MKA key rollover failure:\n\n'
                    '```text\n'
                    '%MKA-3-KEY_MISMATCH: MKA session failed on HundredGigE0/1/0: CKN 0123456789ABCDEF CAK mismatch with peer\n'
                    '%LINK-3-UPDOWN: Interface HundredGigE0/1/0, changed state to down\n'
                    '%BGP-5-ADJCHANGE: neighbor 169.254.0.1 Down Interface down\n'
                    '```\n\n'
                    'Analysis: Google Cloud Interconnect MACsec config was updated with a new primary CKN, but the on-premise router '
                    'had not pre-configured the fallback key chain, triggering link tear-down.'
                ),
                'diagnostic_steps': [
                    'Check Google Cloud Console Interconnect status for MACsec operational state (`OPERATIONAL` vs `NOT_ESTABLISHED`).',
                    'Inspect router MKA session status: `show mka sessions interface HundredGigE0/1/0`.',
                    'Validate active CKN and CAK strings stored in Cloud Secret Manager against on-premise key chain definitions.',
                    'Verify MACsec key rotation was executed using the hitless graceful rollover procedure.'
                ],
                'root': 'The on-premise edge router did not have hitless MKA key rollover configured, causing an immediate link drop when Google activated the new CKN.',
                'fix': 'Configure dual-key MKA key chains on the edge router with overlapping validity windows before initiating MACsec key rotation in Google Cloud.',
                'verify': 'Simulate key rollover in staging; verify `show mka session` transitions keys with zero dropped packets and stable BGP.',
                'residual': 'Hardware vendor MKA implementation differences require standardized lab testing before global production key rotations.',
                'diagram': (
                    'Primary MACsec CKN key expires or rotated on Google edge',
                    'On-prem router missing pre-shared fallback MKA key definition',
                    'MACsec session drops; L2 link goes DOWN and BGP collapses',
                    'Deploy dual-key MKA key chain with overlapping validity window',
                    'MACsec key rotates hitlessly; BGP and line-rate traffic remain stable'
                )
            },
            'lab': {
                'name': 'Hybrid Encryption Architecture & HA VPN Failover Modeling',
                'goal': 'Model and calculate IPsec vs MACsec throughput, MTU/MSS clamping impact, and author declarative Terraform HA VPN gateway with dual encrypted tunnels.',
                'expected': 'Validated Terraform HA VPN configuration with BGP peering and Python MTU clamping calculator verifying packet fragmentation thresholds.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Terraform CLI and Python 3.9+ available.',
                'preflight': 'Ensure clean working directory `~/vpn-macsec-lab`.',
                'steps': [
                    (
                        '#### MTU and MSS Clamping Architectural Calculator\n'
                        'Calculate exact MTU constraints for IPsec ESP vs MACsec encapsulation:\n\n'
                        '```sh\n'
                        'mkdir -p ~/vpn-macsec-lab && cd ~/vpn-macsec-lab\n'
                        'cat <<\'EOF\' > calc_mtu.py\n'
                        'def calculate_transport_overhead():\n'
                        '    standard_eth_mtu = 1500\n'
                        '    jumbo_eth_mtu = 9000\n'
                        '\n'
                        '    # MACsec (802.1AE): 32 bytes overhead (SecTAG 16B + ICV 16B)\n'
                        '    macsec_overhead = 32\n'
                        '    # IPsec ESP Tunnel Mode (AES-GCM): 56 bytes overhead (IP 20B + ESP Header/IV 16B + ICV 16B + Pad 4B)\n'
                        '    ipsec_overhead = 56\n'
                        '\n'
                        '    print("================================================================")\n'
                        '    print("HYBRID TRANSPORT OVERHEAD AND MTU CLAMPING MATRIX")\n'
                        '    print("================================================================")\n'
                        '    print(f"Standard Ethernet MTU: {standard_eth_mtu} bytes")\n'
                        '    print(f"  • MACsec Effective Payload: {standard_eth_mtu - macsec_overhead} bytes (Overhead: {macsec_overhead}B)")\n'
                        '    print(f"  • IPsec Effective Payload:  {standard_eth_mtu - ipsec_overhead} bytes (Overhead: {ipsec_overhead}B)")\n'
                        '    print(f"  • Recommended TCP MSS for IPsec: {standard_eth_mtu - ipsec_overhead - 40} bytes (IP 20B + TCP 20B)")\n'
                        '    print("\\nJumbo Frame Interconnect (9000 bytes):")\n'
                        '    print(f"  • MACsec Effective Payload: {jumbo_eth_mtu - macsec_overhead} bytes")\n'
                        '    print(f"  • IPsec Effective Payload:  {jumbo_eth_mtu - ipsec_overhead} bytes")\n'
                        '    print("================================================================")\n'
                        '\n'
                        'calculate_transport_overhead()\n'
                        'EOF\n'
                        'python3 calc_mtu.py\n'
                        '```'
                    ),
                    (
                        '#### Declarative Cloud HA VPN Terraform Architecture\n'
                        'Author an enterprise Cloud HA VPN configuration with dual 99.99% SLA encrypted IPsec tunnels:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > ha_vpn.tf\n'
                        'resource "google_compute_ha_vpn_gateway" "ha_gateway" {\n'
                        '  name    = "prod-hybrid-ha-vpn"\n'
                        '  network = "projects/brightloaf-prod/global/networks/core-vpc"\n'
                        '  region  = "us-central1"\n'
                        '}\n'
                        '\n'
                        'resource "google_compute_external_vpn_gateway" "onprem_gateway" {\n'
                        '  name            = "onprem-edge-router"\n'
                        '  redundancy_type = "TWO_IPS_REDUNDANCY"\n'
                        '  description     = "Customer On-Premises Border Edge"\n'
                        '  interface {\n'
                        '    id         = 0\n'
                        '    ip_address = "203.0.113.10"\n'
                        '  }\n'
                        '  interface {\n'
                        '    id         = 1\n'
                        '    ip_address = "203.0.113.11"\n'
                        '  }\n'
                        '}\n'
                        '\n'
                        '# Tunnel 0: Interface 0\n'
                        'resource "google_compute_vpn_tunnel" "tunnel_0" {\n'
                        '  name                  = "ha-vpn-tunnel-0"\n'
                        '  region                = "us-central1"\n'
                        '  vpn_gateway           = google_compute_ha_vpn_gateway.ha_gateway.id\n'
                        '  vpn_gateway_interface = 0\n'
                        '  peer_external_gateway = google_compute_external_vpn_gateway.onprem_gateway.id\n'
                        '  peer_external_gateway_interface = 0\n'
                        '  shared_secret         = "d0NotUs3InProd-Crypt0Gr4phicSecr3t-99!"\n'
                        '  router                = "prod-cloud-router"\n'
                        '  ike_version           = 2\n'
                        '}\n'
                        '\n'
                        '# Tunnel 1: Interface 1\n'
                        'resource "google_compute_vpn_tunnel" "tunnel_1" {\n'
                        '  name                  = "ha-vpn-tunnel-1"\n'
                        '  region                = "us-central1"\n'
                        '  vpn_gateway           = google_compute_ha_vpn_gateway.ha_gateway.id\n'
                        '  vpn_gateway_interface = 1\n'
                        '  peer_external_gateway = google_compute_external_vpn_gateway.onprem_gateway.id\n'
                        '  peer_external_gateway_interface = 1\n'
                        '  shared_secret         = "d0NotUs3InProd-Crypt0Gr4phicSecr3t-99!"\n'
                        '  router                = "prod-cloud-router"\n'
                        '  ike_version           = 2\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored ha_vpn.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### Validation and Preflight Syntax Check\n'
                        'Validate the Terraform manifest syntax and parameters:\n\n'
                        '```sh\n'
                        'python3 -c "\n'
                        'import re\n'
                        'content = open(\'ha_vpn.tf\').read()\n'
                        'assert \'google_compute_ha_vpn_gateway\' in content\n'
                        'assert \'vpn_gateway_interface = 0\' in content\n'
                        'assert \'vpn_gateway_interface = 1\' in content\n'
                        'print(\'[PASS] HA VPN Terraform architecture verified with dual redundant interfaces.\')\n'
                        '"\n'
                        '```'
                    )
                ],
                'accept': 'Validated MTU overhead calculation table and validated Terraform HA VPN manifest supporting dual-tunnel failover.',
                'verification': 'Verify outputs of <kbd>python3 calc_mtu.py</kbd> and structural integrity of `ha_vpn.tf`.',
                'trouble': 'If TCP connections stall on VPN, ensure TCP MSS clamping is configured to 1404 bytes on Cloud Router.',
                'cleanup': 'Remove local configuration files: `rm -rf ~/vpn-macsec-lab`.',
                'file': 'day-105-hybrid-encryption.md'
            }
        },
        {
            'key': 'topic-03',
            'title': 'Bastion patterns vs IAP TCP forwarding',
            'overview': (
                'Traditional infrastructure architectures relied on public-facing bastion jump hosts (jumphosts) placed in public '
                'subnets to administer private VMs. This model created significant attack surfaces: persistent public IP scanning, '
                'SSH brute-forcing, bastion patching overhead, and shared SSH key management risks. Identity-Aware Proxy (IAP) '
                'TCP Forwarding eliminates the need for public IPs and jump hosts entirely, encapsulating administrative protocols '
                'within TLS WebSockets authorized dynamically by Google IAM and Context-Aware Access.'
            ),
            'preview': (
                'An internet scanner attempts automated brute-force attacks against SSH port 22; IAP TCP forwarding eliminates '
                'public IP exposure entirely and enforces multi-factor IAM checks before tunneling bytes.'
            ),
            'technical': (
                '### 1. Architectural Comparison: Bastion vs. IAP TCP Forwarding\n'
                '- **Bastion Jump Host Anti-Pattern:** Requires public IP on bastion VM; ingress firewall rule `0.0.0.0/0:22`; '
                'requires maintaining OS patch cycles, SSH keys, bastion user accounts, and monitoring for host compromise. '
                'If the bastion is compromised, the attacker has a pivot point into the entire private VPC.\n'
                '- **IAP TCP Forwarding Architecture:** Private VMs have **zero public IP addresses**. The administrative client '
                'uses <kbd>gcloud compute ssh --tunnel-through-iap</kbd>. The Google Cloud CLI initiates an authenticated TLS WebSocket '
                'connection to the Google IAP proxy endpoint. IAP evaluates IAM permissions (`roles/iap.tunnelResourceAccessor`) '
                'and Context-Aware Access policies (device status, IP, MFA) before forwarding TCP packets directly into the VPC '
                'via Google internal forwarding range `35.235.240.0/20`.\n'
                '\n'
                '### 2. Firewall Invariant for IAP\n'
                '- The VPC firewall only needs a single ingress rule allowing TCP port 22 (SSH) and port 3389 (RDP) '
                'from source IP range `35.235.240.0/20`.\n'
                '- All traffic originating from outside this range is rejected at the network perimeter.'
            ),
            'questions': [
                'Why does IAP TCP forwarding eliminate the operational overhead and security risk of traditional bastion hosts?',
                'What exact Google-owned CIDR block must be whitelisted in VPC firewall rules to allow IAP TCP tunneling?',
                'How can Context-Aware Access policies be layered on top of IAP to prevent administrative access from unmanaged personal devices?'
            ],
            'reference': 'https://cloud.google.com/iap/docs/tcp-forwarding-overview',
            'reference_label': 'Google Cloud IAP: TCP forwarding concepts and administrative access control',
            'scenario': {
                'symptom': 'Security team detects 45,000 failed SSH login attempts per hour on public bastion host `/var/log/auth.log`.',
                'constraints': 'DevOps engineers must maintain 24/7 emergency SSH access to production VMs while eliminating external port scanning.',
                'evidence': (
                    'Audit log snippet from compromised legacy bastion VM:\n\n'
                    '```text\n'
                    'Sep 29 03:14:02 bastion-01 sshd[19842]: Failed password for invalid user admin from 198.51.100.42 port 54122 ssh2\n'
                    'Sep 29 03:14:04 bastion-01 sshd[19845]: Failed password for root from 198.51.100.42 port 54124 ssh2\n'
                    'Sep 29 03:14:06 bastion-01 sshd[19848]: Failed password for invalid user deploy from 198.51.100.42 port 54126 ssh2\n'
                    '```\n\n'
                    'Analysis: Legacy bastion VM had public IP `34.120.45.10` with open port 22 to `0.0.0.0/0`, subjecting it to continuous dictionary attacks.'
                ),
                'diagnostic_steps': [
                    'Review VPC firewall rules to identify ingress rules allowing port 22 from `0.0.0.0/0`.',
                    'Inspect Compute Engine instance inventory to locate all VMs configured with external public IP addresses.',
                    'Check IAM role bindings for `roles/iap.tunnelResourceAccessor` on the target project.',
                    'Verify existence of the required Google IAP forwarding firewall rule for `35.235.240.0/20`.'
                ],
                'root': 'Public bastion host exposed SSH directly to the internet; absence of IAP configuration forced reliance on vulnerable static key authentication.',
                'fix': 'Deprovision the bastion VM, author a VPC firewall rule allowing `35.235.240.0/20` on port 22, and enforce <kbd>gcloud compute ssh --tunnel-through-iap</kbd>.',
                'verify': 'Attempt external direct SSH connection (fails with timeout); initiate IAP tunnel connection with valid IAM identity (succeeds).',
                'residual': 'Local workstation must have Google Cloud SDK installed and user must maintain valid OAuth credentials.',
                'diagram': (
                    'Internet scanner floods public bastion VM on port 22',
                    'VPC firewall exposes public SSH ingress rule 0.0.0.0/0:22',
                    'Bastion auth logs flooded with brute-force dictionary attempts',
                    'Decommission bastion; enforce IAP rule for 35.235.240.0/20 only',
                    'Zero public IPs exposed; admin access authenticated via Google IAM'
                )
            },
            'lab': {
                'name': 'IAP TCP Tunneling Security Policy & Firewall Enforcer',
                'goal': 'Author declarative firewall manifests restricting administrative access to IAP IP range 35.235.240.0/20 and test authorization simulation.',
                'expected': 'Terraform firewall manifest and Python IAP policy verification script demonstrating deterministic blocking of non-IAP sources.',
                'mode': 'Declarative Terraform and CLI validation',
                'prereq': 'Terraform and Python 3 installed.',
                'preflight': 'Establish working directory `~/iap-lab`.',
                'steps': [
                    (
                        '#### Declarative IAP Ingress Firewall Configuration\n'
                        'Author the secure VPC firewall rule allowing administrative access only from Google IAP infrastructure:\n\n'
                        '```sh\n'
                        'mkdir -p ~/iap-lab && cd ~/iap-lab\n'
                        'cat <<\'EOF\' > iap_firewall.tf\n'
                        'resource "google_compute_firewall" "allow_iap_administrative_access" {\n'
                        '  name        = "allow-iap-admin-access"\n'
                        '  network     = "core-vpc"\n'
                        '  description = "Permit SSH and RDP administrative traffic exclusively via Google Cloud IAP"\n'
                        '  direction   = "INGRESS"\n'
                        '  priority    = 1000\n'
                        '\n'
                        '  # Google Cloud IAP IP range\n'
                        '  source_ranges = [\n'
                        '    "35.235.240.0/20"\n'
                        '  ]\n'
                        '\n'
                        '  allow {\n'
                        '    protocol = "tcp"\n'
                        '    ports    = ["22", "3389"]\n'
                        '  }\n'
                        '\n'
                        '  target_tags = ["allow-iap-admin"]\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored iap_firewall.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### IAP Access Validation Simulator\n'
                        'Execute Python verification script evaluating network ingress policies against IAP requirements:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > verify_iap_policy.py\n'
                        'import ipaddress\n'
                        '\n'
                        'IAP_CIDR = ipaddress.ip_network("35.235.240.0/20")\n'
                        '\n'
                        'test_packets = [\n'
                        '    {"source_ip": "35.235.240.5", "port": 22, "desc": "Valid Google IAP Tunnel Proxy"},\n'
                        '    {"source_ip": "35.235.245.100", "port": 3389, "desc": "Valid Google IAP Windows RDP"},\n'
                        '    {"source_ip": "198.51.100.42", "port": 22, "desc": "External Internet Scanner"},\n'
                        '    {"source_ip": "10.128.0.10", "port": 22, "desc": "Internal VPC Peer (Non-IAP)"}\n'
                        ']\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("IAP INGRESS FIREWALL DETERMINISTIC EVALUATION")\n'
                        'print("================================================================")\n'
                        'for pkt in test_packets:\n'
                        '    src = ipaddress.ip_address(pkt["source_ip"])\n'
                        '    allowed = src in IAP_CIDR\n'
                        '    status = "ALLOWED (Forward to VM)" if allowed else "DROPPED (Zero Public Exposure)"\n'
                        '    print(f"[{status}] Source: {pkt[\'source_ip\']:16s} Port: {pkt[\'port\']} -> {pkt[\'desc\']}")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 verify_iap_policy.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform firewall definition enforcing source range 35.235.240.0/20 and Python simulation verifying deterministic packet dropping.',
                'verification': 'Review terminal output of <kbd>python3 verify_iap_policy.py</kbd> verifying external IP ranges are blocked.',
                'trouble': 'If <kbd>gcloud compute ssh --tunnel-through-iap</kbd> fails, verify the caller has `roles/iap.tunnelResourceAccessor` on the project.',
                'cleanup': 'Remove local configuration: `rm -rf ~/iap-lab`.',
                'file': 'day-105-iap-bastion.md'
            }
        },
        {
            'key': 'topic-04',
            'title': 'DNS security (DNSSEC, DNS logging)',
            'overview': (
                'Domain Name System (DNS) is the critical control plane of all network communication, yet plain DNS queries '
                'are unauthenticated and susceptible to cache poisoning, man-in-the-middle spoofing, and covert data exfiltration. '
                'Domain Name System Security Extensions (DNSSEC) provides cryptographic integrity and authenticity using digital '
                'signatures. In parallel, Cloud DNS query logging and Cloud DNS firewall policies provide enterprise visibility '
                'and threat prevention against malicious domain lookups and DNS tunneling.'
            ),
            'preview': (
                'A malicious internal script queries a covert DNS exfiltration endpoint; DNS query logging captures the base64-encoded '
                'tunneling subdomain and triggers automated incident response.'
            ),
            'technical': (
                '### 1. Cloud DNSSEC Cryptographic Trust Chain\n'
                '- **Zone Signing Key (ZSK):** Used by Cloud DNS to sign all Resource Record Sets (RRsets) in the zone, producing '
                '`RRSIG` records. Typically uses elliptic curve algorithms (`ECDSAP256SHA256`) and rotates automatically.\n'
                '- **Key Signing Key (KSK):** Signs the ZSK record set (`DNSKEY`). The hash of the KSK is submitted to the parent registrar '
                'as a Delegation Signer (`DS`) record, establishing an unbroken chain of cryptographic trust to the DNS root.\n'
                '- **Authenticated Denial of Existence:** Uses `NSEC3` records to prevent zone-walking attacks while proving non-existence of subdomains.\n'
                '\n'
                '### 2. Cloud DNS Query Logging & DNS Firewall\n'
                '- **Query Logging:** Captures all DNS queries originating from inside the VPC, logging client IP, requested FQDN, '
                'record type, response code, and latency to Cloud Logging.\n'
                '- **DNS Firewall Policies:** Applies threat intelligence domain blocklists at the VPC resolver level. Blocks known '
                'malware C2 domains and DNS exfiltration endpoints before IP resolution can take place.'
            ),
            'questions': [
                'How does DNSSEC protect client resolvers against DNS cache poisoning and spoofed record injection?',
                'What is the operational consequence if a domain registrar DS record does not match the active Cloud DNS KSK?',
                'How does Cloud DNS query logging enable Security Operations teams to detect DNS data exfiltration?'
            ],
            'reference': 'https://cloud.google.com/dns/docs/dnssec-advanced',
            'reference_label': 'Google Cloud DNS: DNSSEC concepts, algorithm selection, and DS record management',
            'scenario': {
                'symptom': 'All external internet clients experience SERVFAIL when attempting to resolve corporate website following registrar migration.',
                'constraints': 'DNSSEC must remain active to satisfy federal cyber compliance mandates; cannot permanently disable validation.',
                'evidence': (
                    '<kbd>dig +dnssec</kbd> output showing broken chain of trust:\n\n'
                    '```text\n'
                    ';; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 41209\n'
                    ';; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1\n'
                    ';; OPT PSEUDOSECTION:\n'
                    '; EDNS: version: 0, flags: do; udp: 4096\n'
                    ';; QUESTION SECTION:\n'
                    ';api.brightloaf.com. IN A\n'
                    '```\n\n'
                    'Analysis: The registrar retained an obsolete DS record pointing to a decommissioned on-premise BIND KSK, '
                    'while Google Cloud DNS was signing records with a newly generated ECDSAP256SHA256 KSK.'
                ),
                'diagnostic_steps': [
                    'Query authoritative DNSKEY records using <kbd>dig @ns-cloud-a1.googledomains.com api.brightloaf.com DNSKEY +multiline</kbd>.',
                    'Query parent registrar DS records using <kbd>dig DS brightloaf.com +trace</kbd>.',
                    'Compute the cryptographic hash (SHA-256) of the Google Cloud DNS KSK and compare against parent DS record digest.',
                    'Check Google Cloud DNSSEC state via <kbd>gcloud dns managed-zones describe brightloaf-zone</kbd>.'
                ],
                'root': 'Cryptographic trust chain divergence: Registrar DS record did not match the Cloud DNS Key Signing Key (KSK).',
                'fix': 'Extract active KSK DS record details from Cloud DNS and update the parent domain registrar records immediately.',
                'verify': 'Run <kbd>dig +dnssec api.brightloaf.com</kbd> against public validating resolvers (`8.8.8.8`) and verify `NOERROR` with valid `RRSIG`.',
                'residual': 'Registrar DNS propagation and parent zone TTLs (typically 24 hours) may prolong SERVFAIL caching during misconfigurations.',
                'diagram': (
                    'Cloud DNS signs zone records with new ECDSAP256SHA256 KSK',
                    'Domain registrar publishes outdated DS record from legacy provider',
                    'Validating resolver detects digest mismatch and returns SERVFAIL',
                    'Publish updated DS record matching Cloud DNS KSK at registrar',
                    'DNSSEC chain of trust verified to root; queries resolve with NOERROR'
                )
            },
            'lab': {
                'name': 'DNSSEC Zone Validation & Query Log Exfiltration Detector',
                'goal': 'Configure declarative DNSSEC managed zone manifests and author a Python DNS query log analyzer that detects DNS exfiltration heuristics.',
                'expected': 'Validated Terraform Cloud DNS zone manifest with DNSSEC enabled and working Python log detector identifying anomalous subdomain entropy.',
                'mode': 'Terraform and Python analytics simulation',
                'prereq': 'Python 3 and Terraform installed.',
                'preflight': 'Create clean working directory `~/dns-sec-lab`.',
                'steps': [
                    (
                        '#### Declarative Cloud DNSSEC Terraform Configuration\n'
                        'Author an authoritative Cloud DNS zone enforcing DNSSEC with ECDSAP256SHA256 algorithm:\n\n'
                        '```sh\n'
                        'mkdir -p ~/dns-sec-lab && cd ~/dns-sec-lab\n'
                        'cat <<\'EOF\' > dnssec_zone.tf\n'
                        'resource "google_dns_managed_zone" "secure_zone" {\n'
                        '  name        = "brightloaf-secure-zone"\n'
                        '  dns_name    = "brightloaf.internal."\n'
                        '  description = "Production authoritative DNS zone with hardware-grade DNSSEC enabled"\n'
                        '  visibility  = "private"\n'
                        '\n'
                        '  private_visibility_config {\n'
                        '    networks {\n'
                        '      network_url = "projects/brightloaf-prod/global/networks/core-vpc"\n'
                        '    }\n'
                        '  }\n'
                        '\n'
                        '  dnssec_config {\n'
                        '    state         = "on"\n'
                        '    non_existence = "nsec3"\n'
                        '\n'
                        '    default_key_specs {\n'
                        '      algorithm  = "ecdsap256sha256"\n'
                        '      key_type   = "keySigning"\n'
                        '      key_length = 256\n'
                        '    }\n'
                        '\n'
                        '    default_key_specs {\n'
                        '      algorithm  = "ecdsap256sha256"\n'
                        '      key_type   = "zoneSigning"\n'
                        '      key_length = 256\n'
                        '    }\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored dnssec_zone.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### DNS Tunneling & Exfiltration Anomaly Detector\n'
                        'Author a Python log analytics script that inspects Cloud DNS query logs for high-entropy exfiltration subdomains:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > detect_dns_exfil.py\n'
                        'import math\n'
                        'import re\n'
                        '\n'
                        'def calculate_shannon_entropy(data: str) -> float:\n'
                        '    if not data:\n'
                        '        return 0.0\n'
                        '    prob = [float(data.count(c)) / len(data) for c in dict.fromkeys(list(data))]\n'
                        '    return - sum([p * math.log(p) / math.log(2.0) for p in prob])\n'
                        '\n'
                        'sample_dns_logs = [\n'
                        '    {"client_ip": "10.128.0.5", "query": "api.brightloaf.internal", "type": "A"},\n'
                        '    {"client_ip": "10.128.0.5", "query": "database-primary.brightloaf.internal", "type": "A"},\n'
                        '    {"client_ip": "10.128.0.22", "query": "dGhpcyBpcyBhIHNlY3JldCBwYXNzd29yZA==.exfil.attacker-domain.com", "type": "TXT"},\n'
                        '    {"client_ip": "10.128.0.22", "query": "a8f9c1b3e4d89a7f10b2c3d4e5f6a7b8c9d0.c2.malicious-network.org", "type": "A"}\n'
                        ']\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("CLOUD DNS QUERY AUDIT: EXFILTRATION & C2 DETECTION")\n'
                        'print("================================================================")\n'
                        'ENTROPY_THRESHOLD = 3.8\n'
                        'for log in sample_dns_logs:\n'
                        '    subdomain = log["query"].split(".")[0]\n'
                        '    entropy = calculate_shannon_entropy(subdomain)\n'
                        '    length = len(subdomain)\n'
                        '    is_suspicious = entropy > ENTROPY_THRESHOLD or length > 30\n'
                        '    status = "ALERT: SUSPICIOUS TUNNELING" if is_suspicious else "NORMAL QUERY"\n'
                        '    print(f"[{status:26s}] Client: {log[\'client_ip\']:12s} Entropy: {entropy:.2f} Len: {length:2d} -> {log[\'query\']}")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 detect_dns_exfil.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated DNSSEC Terraform configuration and Python Shannon entropy detector identifying high-entropy DNS tunneling queries.',
                'verification': 'Run <kbd>python3 detect_dns_exfil.py</kbd> and verify alert triggering on exfiltration queries.',
                'trouble': 'If DNSSEC validation fails after registrar update, verify DS digest matches active KSK via <kbd>gcloud dns record-sets list</kbd>.',
                'cleanup': 'Remove test files: `rm -rf ~/dns-sec-lab`.',
                'file': 'day-105-dnssec-audit.md'
            }
        }
    ]
}
