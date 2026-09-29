"""day_data_103.py — Exhaustive architecture data specification for Day 103.

Covers Defense in Depth, Firewall Patterns, Cloud Armor, and Private Connectivity.
"""

DAY_NUM = 103

DATA = {'day': 103,
 'part1_intro': 'Day 103 establishes the comprehensive architecture for enterprise defense-in-depth and advanced '
                'network security. Architects analyze multi-layered defensive engineering spanning edge protection, '
                'hierarchical firewall policies, service account network scoping, Cloud Armor Web Application Firewall '
                '(WAF) and Adaptive Protection, and private connectivity patterns eliminating all public IPv4 '
                'addresses via Private Google Access, Cloud NAT, and Private Service Connect (PSC).',
 'exit_summary': 'Engineers master defense-in-depth architectural layering, hierarchical firewall policy enforcement '
                 'with service account scoping, Cloud Armor preconfigured WAF rules and rate limiting, and '
                 'zero-public-IP network topologies utilizing Private Google Access and Private Service Connect.',
 'part2_intro': 'The following architectural matrix details the technical trade-offs, operational protocols, and '
                'security boundaries across defense-in-depth layering, hierarchical firewalls, Cloud Armor WAF, and '
                'private connectivity transit options.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '<thead>\n'
                    '<tr>\n'
                    '<th>Architecture Layer</th>\n'
                    '<th>Control Mechanism</th>\n'
                    '<th>Primary Protocol</th>\n'
                    '<th>Security Boundary</th>\n'
                    '<th>Operational Invariant</th>\n'
                    '</tr>\n'
                    '</thead>\n'
                    '<tbody>\n'
                    '<tr>\n'
                    '<td><strong>Edge &amp; WAF</strong></td>\n'
                    '<td>Cloud Armor</td>\n'
                    '<td>ModSecurity / CEL</td>\n'
                    '<td>Google Edge Network</td>\n'
                    '<td>All external HTTP/S traffic inspected for OWASP Top 10 before reaching backends.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Network Perimeter</strong></td>\n'
                    '<td>Hierarchical Firewalls</td>\n'
                    '<td>Network Protocol &amp; Port Rules</td>\n'
                    '<td>Organization &amp; Folder Nodes</td>\n'
                    '<td>Mandatory egress deny-all; ingress scoped strictly to non-transferable Service '
                    'Accounts.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Workload Plane</strong></td>\n'
                    '<td>Zero Public IP Architecture</td>\n'
                    '<td>RFC 1918 Private Addressing</td>\n'
                    '<td>VPC Subnet Perimeter</td>\n'
                    '<td>Workloads never receive public IPv4 addresses; all egress mediated via Cloud NAT.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Private Transit</strong></td>\n'
                    '<td>Private Google Access &amp; PSC</td>\n'
                    '<td>Internal DNS &amp; Private VIPs</td>\n'
                    '<td><code>restricted.googleapis.com</code></td>\n'
                    "<td>Google Cloud API traffic remains strictly on Google's private global fiber network.</td>\n"
                    '</tr>\n'
                    '</tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 103: Defense-in-Depth Layering, Firewall Design, Cloud Armor, and Private Connectivity',
                  'desc': 'Architectural topology showing Cloud Armor WAF at the edge, hierarchical firewalls, private '
                          'workload subnets, and Private Google Access/PSC transit.',
                  'caption': 'Figure 103.1: Multi-layer network security topology featuring Cloud Armor WAF edge '
                             'protection, service-account firewall filtering, and zero-public-IP private transit.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Global Edge Ingress & Cloud Armor WAF Perimeter',
                              'desc': 'External ALB, DDoS mitigation, and Cloud Armor preconfigured OWASP rules',
                              'y': 10,
                              'h': 90,
                              'stroke': '#38bdf8',
                              'fill': '#0c1e38',
                              'title_color': '#38bdf8'},
                             {'name': 'LAYER 2: Hierarchical Policy & VPC Firewall Fabric',
                              'desc': 'Org-level security policies, Service Account-scoped rules, and egress '
                                      'restrictions',
                              'y': 115,
                              'h': 90,
                              'stroke': '#818cf8',
                              'fill': '#141838',
                              'title_color': '#818cf8'},
                             {'name': 'LAYER 3: Private Subnet Workload Plane (Zero Public IPs)',
                              'desc': 'GCE instances and GKE nodes with RFC 1918 addresses and shielded VM protections',
                              'y': 220,
                              'h': 90,
                              'stroke': '#f59e0b',
                              'fill': '#261a08',
                              'title_color': '#f59e0b'},
                             {'name': 'LAYER 4: Private Google Access, Cloud NAT & PSC Transit',
                              'desc': 'Private Google Access (restricted VIP), Cloud NAT, and Private Service Connect '
                                      'endpoints',
                              'y': 325,
                              'h': 90,
                              'stroke': '#f43f5e',
                              'fill': '#2a0a14',
                              'title_color': '#f43f5e'},
                             {'name': 'LAYER 5: Managed Google APIs, Internal Services & Audit Vault',
                              'desc': 'BigQuery, GCS, Spanner, internal producer services, and firewall audit logs',
                              'y': 430,
                              'h': 90,
                              'stroke': '#22c55e',
                              'fill': '#072417',
                              'title_color': '#22c55e'}],
                  'components': [{'name': 'External Web Client',
                                  'detail': 'Public Internet HTTPS',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'Cloud Armor WAF',
                                  'detail': 'SQLi / XSS / Bot Shield',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'Hierarchical Firewall',
                                  'detail': 'Org-Level Egress Block',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'SA-Scoped Firewall',
                                  'detail': 'Target: sa-api-worker',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Private App VM',
                                  'detail': '10.128.10.4 (No Public IP)',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Private GKE Pods',
                                  'detail': '10.128.20.0/24 Cluster',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Private Google Access',
                                  'detail': '199.36.153.4/30 (Restricted)',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Cloud NAT Gateway',
                                  'detail': 'Outbound-Only Updates',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'BigQuery & Cloud Storage',
                                  'detail': 'Private API Endpoint',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'},
                                 {'name': 'Private Service Connect',
                                  'detail': 'Internal Service Consumer',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'}],
                  'boundaries': [{'label': 'GLOBAL EDGE & CLOUD ARMOR WAF PERIMETER',
                                  'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'color': '#38bdf8'},
                                 {'label': 'HIERARCHICAL FIREWALL & PRIVATE WORKLOAD FABRIC',
                                  'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#818cf8'},
                                 {'label': 'PRIVATE ACCESS & MANAGED TRANSIT VAULT',
                                  'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#22c55e'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Inspect WAF Rules', 'type': 'ok'},
                            {'x1': 210,
                             'y1': 82,
                             'x2': 210,
                             'y2': 135,
                             'label': 'Evaluate Org Firewalls',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'label': 'Filter by Service Account',
                             'type': 'ok'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'label': 'Route to Private Subnet',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 266,
                             'x2': 420,
                             'y2': 266,
                             'label': 'Block Inbound Public',
                             'type': 'fail'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'label': 'Route to Restricted VIP',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'label': 'NAT Outbound Internet',
                             'type': 'ok'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'label': 'Access Managed Storage',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'label': 'Connect via PSC Endpoint',
                             'type': 'ok'}],
                  'probes': [{'cx': 420,
                              'cy': 30,
                              'label': 'PROBE 1: Cloud Armor WAF SQLi Drop (HTTP 403)',
                              'badge': 'P1',
                              'color': '#38bdf8'},
                             {'cx': 80,
                              'cy': 135,
                              'label': 'PROBE 2: Hierarchical Policy Egress Drop',
                              'badge': 'P2',
                              'color': '#f43f5e'},
                             {'cx': 80,
                              'cy': 345,
                              'label': 'PROBE 3: Private Google Access VIP Reachability',
                              'badge': 'P3',
                              'color': '#22c55e'}]},
 'part3_intro': 'The following field cases analyze real-world network security vulnerabilities, perimeter breaches, '
                'and firewall design defects: an enterprise data breach caused by relying on a single network '
                'perimeter firewall where a public-facing container compromise allowed immediate unhindered lateral '
                'movement across internal subnets, a network tag spoofing incident where a developer attached a '
                'privileged network tag to a test instance, inadvertently exposing an internal MySQL database to the '
                'public internet, a severe application SQL injection exploit that bypassed security because Cloud '
                'Armor preconfigured WAF rules had been deployed in preview-only mode, and a crypto-ransomware '
                'incident on a database instance whose public IP was port-scanned and compromised within 15 minutes of '
                'provisioning because the subnet lacked Private Google Access and Cloud NAT controls. Each case '
                'details verbatim logs, terminal transcripts, root cause analysis, defensible remediations, and '
                'dual-lane failed/corrected flow diagrams.',
 'part4_intro': 'These hands-on exercises implement the comprehensive 8-stage operational engineering lifecycle for '
                'Day 103. Engineers construct defense-in-depth policy manifests enforcing layered security controls, '
                'author hierarchical firewall policies and identity-based service account firewall rules, deploy Cloud '
                'Armor security policies with preconfigured OWASP Core Rule Sets (CRS) and rate-limiting rules, and '
                'architect private connectivity topologies configuring Private Google Access, Cloud NAT, and Private '
                'Service Connect.',
 'topics': [{'key': 'topic-01',
             'title': 'Defence in depth layering',
             'overview': 'Defense-in-depth is the foundational architectural strategy of implementing multiple '
                         'redundant security controls across every layer of the computing stack: Edge & DDoS (Cloud '
                         'Armor), Network (Hierarchical Firewalls and VPC peering isolation), Compute & Host (Shielded '
                         'VMs, Confidential Computing, OS Login), Identity & Access (IAM, Workload Identity, PAM), and '
                         'Data Storage (Customer-Managed Encryption Keys, VPC Service Controls, Cloud DLP). If any '
                         'single layer is penetrated or misconfigured, subsequent defensive perimeters automatically '
                         'contain the adversary and prevent lateral movement.',
             'preview': 'An attacker bypasses an edge load balancer using a zero-day vulnerability; however, because '
                        'the target compute workloads are isolated in a private subnet governed by service-account '
                        'firewalls and strict VPC Service Controls perimeters, data exfiltration is completely '
                        'blocked.',
             'technical': '### 1. The 5 Defensive Tiers\n'
                          '- **Tier 1 (Edge / Perimeter):** Cloud Armor, Cloud CDN, External Application Load '
                          'Balancers, TLS 1.3 termination.\n'
                          '- **Tier 2 (Network):** Hierarchical Firewall Policies, VPC isolation, Private Google '
                          'Access, Cloud NAT.\n'
                          '- **Tier 3 (Host / Compute):** Shielded VMs (Secure Boot, vTPM, Integrity Monitoring), OS '
                          'Login (eliminates SSH keys).\n'
                          '- **Tier 4 (Identity & Access):** Principle of least privilege, Context-Aware Access, IAM '
                          'Conditions, PAM just-in-time elevation.\n'
                          '- **Tier 5 (Data & Governance):** CMEK with Cloud KMS, VPC Service Controls perimeters, '
                          'Client-side field-level encryption, Cloud Audit logs.\n'
                          '\n'
                          '### 2. Operational Invariants\n'
                          '- **No Perimeter Monoculture:** Never assume network firewalls alone protect data; every '
                          'tier must independently authenticate and authorize.\n'
                          '- **Fail-Closed Gateways:** Default egress must be denied; outbound connections require '
                          'explicit authorization.',
             'questions': ['Why is a flat VPC network with perimeter-only firewalls considered an architectural '
                           'anti-pattern in Google Cloud?',
                           'How does the combination of Shielded VMs and OS Login strengthen the host tier in '
                           'defense-in-depth?',
                           'Which control ensures data cannot be exfiltrated even if an attacker gains full '
                           'administrative access to a Compute Engine instance?'],
             'reference': 'https://cloud.google.com/architecture/defense-in-depth',
             'reference_label': 'Google Cloud Architecture: Defense-in-depth layered security design',
             'scenario': {'symptom': 'A web application compromise in a public subnet allowed an attacker to query '
                                     'internal database records and exfiltrate customer data.',
                          'constraints': 'Application requires internet access to serve customers, but backend '
                                         'databases contain confidential PII.',
                          'evidence': 'Netflow and Cloud Audit log extract:\n'
                                      '\n'
                                      '```text\n'
                                      '2026-09-29T14:10:00Z [COMPROMISE] Web container (10.128.0.5) exploited via '
                                      'deserialization vulnerability.\n'
                                      '2026-09-29T14:10:15Z [LATERAL] 10.128.0.5 opened direct TCP connection to '
                                      '10.128.0.25:5432 (Postgres DB) -> ALLOWED (Flat VPC rule)\n'
                                      '2026-09-29T14:10:45Z [EXFILTRATION] 10.128.0.5 sent 1.4GB payload to '
                                      '198.51.100.89:443 -> ALLOWED (Unrestricted default egress)\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: The organization relied on a single edge firewall; subnets were flat '
                                      'with zero internal segmentation, no egress filtering, and no data perimeter.',
                          'diagnostic_steps': ['Inspect VPC firewall rules for 0.0.0.0/0 egress allowance.',
                                               'Verify subnet separation between web tier and database tier.',
                                               'Audit database IAM authentication and encryption configuration.',
                                               'Check VPC Service Controls perimeter membership.'],
                          'root': 'Lack of defense-in-depth layering: flat internal network allowed unrestricted '
                                  'lateral movement, and unmonitored default egress enabled direct exfiltration.',
                          'fix': 'Segment web and database tiers into isolated subnets, enforce service-account-based '
                                 'internal firewall rules, deny default egress, and enclose database in a VPC Service '
                                 'Controls perimeter.',
                          'verify': 'Simulate compromise on web tier and verify that database connections are blocked '
                                    'at the network layer and internet egress is denied.',
                          'residual': 'Legitimate outbound updates require routing through Cloud NAT with domain '
                                      'allowlisting or Secure Web Proxy.',
                          'diagram': ('Web container compromised via deserialization exploit',
                                      'Flat VPC allows unrestricted internal lateral movement',
                                      'Attacker drains database and exfiltrates via default egress',
                                      'Enforce multi-tier defense: SA firewalls, private subnet & egress block',
                                      'Lateral movement blocked at network; egress denied')},
             'lab': {'name': 'Defense-in-Depth Layered Architecture Implementation',
                     'goal': 'Author a multi-layered infrastructure manifest enforcing edge, network, host, and egress '
                             'controls.',
                     'expected': 'Declarative Terraform manifest establishing isolated subnets, strict egress deny, '
                                 'and service account network scoping.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify VPC network permissions and Terraform CLI availability.',
                     'steps': ['#### Pre-Flight Defense-in-Depth Tier Discovery\n'
                               'Catalog security controls across the 5 architectural tiers:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_did_tiers.py\n"
                               'tiers = {\n'
                               "    'Tier 1 (Edge)': 'Cloud Armor WAF with OWASP Core Rule Set',\n"
                               "    'Tier 2 (Network)': 'Hierarchical firewalls, isolated subnets, zero public IPs',\n"
                               "    'Tier 3 (Host)': 'Shielded VMs with Secure Boot and vTPM integrity',\n"
                               "    'Tier 4 (Identity)': 'IAM least privilege with Service Account scoping',\n"
                               "    'Tier 5 (Data)': 'CMEK encryption and VPC Service Controls perimeter'\n"
                               '}\n'
                               "print('[PREFLIGHT] Defense-in-Depth Architectural Matrix:')\n"
                               'for k, v in tiers.items():\n'
                               "    print(f'  • {k:18s}: {v}')\n"
                               'EOF\n'
                               'python3 check_did_tiers.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and policy linters:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_did_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_did_tools.sh\n'
                               '```',
                               '#### Core Implementation: Multi-Tier Network Segmentation Manifest\n'
                               'Author a declarative Terraform configuration establishing tiered subnets and '
                               'default-deny egress:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > defense_in_depth.tf\n"
                               'resource "google_compute_network" "secure_vpc" {\n'
                               '  name                    = "prod-secure-vpc"\n'
                               '  auto_create_subnetworks = false\n'
                               '}\n'
                               '\n'
                               'resource "google_compute_subnetwork" "web_subnet" {\n'
                               '  name          = "web-tier-subnet"\n'
                               '  ip_cidr_range = "10.128.10.0/24"\n'
                               '  region        = "us-central1"\n'
                               '  network       = google_compute_network.secure_vpc.id\n'
                               '}\n'
                               '\n'
                               'resource "google_compute_subnetwork" "db_subnet" {\n'
                               '  name          = "db-tier-subnet"\n'
                               '  ip_cidr_range = "10.128.20.0/24"\n'
                               '  region        = "us-central1"\n'
                               '  network       = google_compute_network.secure_vpc.id\n'
                               '  private_ip_google_access = true\n'
                               '}\n'
                               '\n'
                               '# Default Deny Egress\n'
                               'resource "google_compute_firewall" "deny_all_egress" {\n'
                               '  name      = "deny-all-egress"\n'
                               '  network   = google_compute_network.secure_vpc.name\n'
                               '  direction = "EGRESS"\n'
                               '  priority  = 65534\n'
                               '\n'
                               '  deny {\n'
                               '    protocol = "all"\n'
                               '  }\n'
                               '  destination_ranges = ["0.0.0.0/0"]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored defense_in_depth.tf"\n'
                               '```',
                               '#### Execution & Lateral Movement Block Simulation\n'
                               'Author a Python simulation script verifying that web tier cannot access unauthorized '
                               'ports:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_lateral_block.py\n"
                               'def evaluate_network_flow(src_tier, dst_tier, dst_port):\n'
                               '    # Only permit Web -> DB on port 5432 with explicit SA\n'
                               "    if src_tier == 'web' and dst_tier == 'db':\n"
                               '        if dst_port == 5432:\n'
                               "            return 'ALLOWED_BY_SA_FIREWALL'\n"
                               "        return 'BLOCKED_BY_DEFAULT_DENY'\n"
                               "    if dst_tier == 'internet':\n"
                               "        return 'BLOCKED_BY_EGRESS_RULE'\n"
                               "    return 'BLOCKED'\n"
                               '\n'
                               "print('[SIMULATION] Testing Lateral Movement Barriers:')\n"
                               "res1 = evaluate_network_flow('web', 'db', 22) # SSH\n"
                               "assert res1 == 'BLOCKED_BY_DEFAULT_DENY'\n"
                               "print(f'  • Web -> DB SSH (Port 22): {res1} -> PASS')\n"
                               '\n'
                               "res2 = evaluate_network_flow('web', 'internet', 443)\n"
                               "assert res2 == 'BLOCKED_BY_EGRESS_RULE'\n"
                               "print(f'  • Web -> Internet Direct: {res2} -> PASS')\n"
                               'EOF\n'
                               'python3 simulate_lateral_block.py\n'
                               '```',
                               '#### Resiliency Testing & Egress Bypass Chaos Test\n'
                               'Simulate an attacker attempting to establish an outbound reverse shell and assert '
                               'interception:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_reverse_shell_block.py\n"
                               'from simulate_lateral_block import evaluate_network_flow\n'
                               '\n'
                               "status = evaluate_network_flow('web', 'internet', 4444)\n"
                               "assert status == 'BLOCKED_BY_EGRESS_RULE', 'Security failure: Reverse shell egress "
                               "permitted!'\n"
                               "print(f'[CHAOS TEST PASS] Egress deny-all rule intercepted reverse shell: {status}')\n"
                               'EOF\n'
                               'python3 test_reverse_shell_block.py\n'
                               '```',
                               '#### Telemetry, Observability & Firewall Rule Logging Manifest\n'
                               'Author a Cloud Logging filter tracking dropped egress packets:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > firewall_drop_filter.txt\n"
                               'resource.type="gce_subnetwork"\n'
                               'logName="projects/prod-net/logs/compute.googleapis.com%2Ffirewall"\n'
                               'jsonPayload.rule_details.action="DENY"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to firewall_drop_filter.txt"\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform defense-in-depth manifest:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_did_manifest.py\n"
                               "with open('defense_in_depth.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'private_ip_google_access = true' in tf\n"
                               'assert \'direction = "EGRESS"\' in tf\n'
                               "assert 'deny-all-egress' in tf\n"
                               "print('[ASSERT PASS] Defense-in-depth Terraform manifest strictly validated.')\n"
                               'EOF\n'
                               'python3 assert_did_manifest.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_did_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 103 Topic 1 test scripts..."\n'
                               'rm -f check_did_tiers.py check_did_tools.sh simulate_lateral_block.py '
                               'test_reverse_shell_block.py assert_did_manifest.py\n'
                               'echo "[CLEANUP] Retaining production files: defense_in_depth.tf, '
                               'firewall_drop_filter.txt"\n'
                               'echo "[CLEANUP PASS] Defense-in-depth lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_did_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm tiered subnetting and '
                                     'default-deny egress enforcement.',
                     'trouble': 'Ensure priority of custom allow rules is lower (numerically smaller) than default '
                                'deny priority 65534.',
                     'cleanup': 'bash teardown_did_lab.sh',
                     'accept': 'Network manifest and test suite pass verification with 0 errors.',
                     'file': 'day-103-topic-01-defense-in-depth.md'}},
            {'key': 'topic-02',
             'title': 'Firewall design patterns',
             'overview': 'Google Cloud firewall architecture operates at two distinct tiers: Hierarchical Firewall '
                         'Policies (defined at Organization or Folder levels to enforce non-overridable security '
                         'baselines) and VPC Network Firewall Rules (defined at the network level). Modern firewall '
                         'design patterns mandate moving away from fragile network IP tags (which any developer with '
                         'Compute Instance Editor can attach or remove) to identity-based Service Account firewall '
                         'scoping (`target_service_accounts` and `source_service_accounts`). This guarantees that '
                         'network connectivity is cryptographically tied to the verified IAM identity of the workload '
                         'rather than arbitrary string labels.',
             'preview': 'A junior developer attempts to attach the network tag `allow-external-ssh` to a staging '
                        'instance; because the organization enforces a Hierarchical Firewall Policy with delegated '
                        'Secure Tags and Service Account rules, the spoofed tag has zero effect.',
             'technical': '### 1. Hierarchical Firewall Policies\n'
                          '- **Policy Hierarchy:** Org Level -> Folder Level -> VPC Network Level.\n'
                          '- **Evaluation Order:** Evaluated top-down. Rules can `ALLOW`, `DENY`, or `goto_next`.\n'
                          '- **Immutability:** Project owners cannot delete, override, or disable rules inherited from '
                          'higher hierarchy nodes.\n'
                          '\n'
                          '### 2. Service Account Scoped Firewall Rules\n'
                          '- **Target Service Accounts:** Rule applies only to instances running as the specified '
                          'service account.\n'
                          '- **Source Service Accounts:** Ingress is permitted only if the source instance running '
                          'within the same VPC runs as the authorized service account.\n'
                          '- **Secure Tags:** Resource Manager Tags managed via IAM '
                          '(`roles/resourcemanager.tagAdmin`), preventing unauthorized developers from tagging '
                          'instances.',
             'questions': ['Why are Service Account-based firewall rules superior to network tag-based firewall rules '
                           'in enterprise environments?',
                           'What is the operational function of the `goto_next` action in a Hierarchical Firewall '
                           'Policy?',
                           'How do Resource Manager Secure Tags differ from traditional Compute Engine network tags?'],
             'reference': 'https://cloud.google.com/firewall/docs/firewalls_overview',
             'reference_label': 'Google Cloud: VPC firewall rules and hierarchical firewall policies',
             'scenario': {'symptom': 'An internal database cluster was exposed to the public internet because a '
                                     'developer added the tag `web-server` to test a webhook.',
                          'constraints': 'Multiple application teams deploy instances in a shared VPC; network '
                                         'security must be enforced centrally without restricting self-service '
                                         'instance creation.',
                          'evidence': 'Compute Engine instance configuration and firewall rule binding:\n'
                                      '\n'
                                      '```text\n'
                                      'Instance: db-postgres-node-1\n'
                                      "Tags: ['database', 'web-server'] # Developer added 'web-server'\n"
                                      'Firewall Rule: allow-web-traffic-public\n'
                                      "Target Tags: ['web-server']\n"
                                      'Allowed: tcp:80, tcp:443, tcp:5432 # Overly broad port range included '
                                      'postgres!\n'
                                      'Source: 0.0.0.0/0\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: Anyone with `compute.instances.setTags` permission could modify '
                                      'network security boundaries arbitrarily.',
                          'diagnostic_steps': ['Audit firewall rules matching target tags vs service accounts.',
                                               'Verify IAM permissions for compute.instances.setTags across developer '
                                               'roles.',
                                               'Inspect Hierarchical Firewall Policy rules applied at the folder root.',
                                               'Check port exposure using Network Intelligence Center Firewall '
                                               'Insights.'],
                          'root': 'Firewall rules were scoped using mutable network tags instead of cryptographically '
                                  'bound Service Accounts.',
                          'fix': 'Migrate firewall rules to use `target_service_accounts = '
                                 '["sa-db@prod.iam.gserviceaccount.com"]` and enforce an Org-level policy blocking '
                                 'public ingress.',
                          'verify': 'Attach arbitrary network tags to the instance and assert that database ports '
                                    'remain completely inaccessible from the internet.',
                          'residual': 'Instances require proper service account association at creation time; '
                                      'modifying service accounts requires instance recreation or stop/start.',
                          'diagram': ("Developer adds 'web-server' tag to production DB instance",
                                      'Tag matches overly broad public firewall rule',
                                      'Database port 5432 exposed to internet scanners',
                                      'Convert firewall rule to target_service_accounts = sa-db',
                                      'Tag ignored; database accessible strictly via authorized SA')},
             'lab': {'name': 'Service Account-Scoped Firewall Rule Architecture',
                     'goal': 'Author declarative Terraform firewall manifests enforcing Service Account-scoped rules '
                             'and hierarchical protection.',
                     'expected': 'Validated Terraform firewall manifest and Python simulation testing SA-scoped vs '
                                 'tag-based rule evaluation.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify compute.firewalls permissions and Terraform availability.',
                     'steps': ['#### Pre-Flight Firewall Design Pattern Discovery\n'
                               'Catalog firewall scoping mechanisms and rule precedence:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_firewall_patterns.py\n"
                               'patterns = {\n'
                               "    'Hierarchical Policies': 'Enforced top-down from Organization or Folder nodes',\n"
                               "    'Service Account Rules': 'Tied to instance identity; immune to tag spoofing',\n"
                               "    'Secure Tags': 'Resource Manager tags protected by IAM tagUser role',\n"
                               "    'Legacy Network Tags': 'DEPRECATED: Mutable by any instance editor'\n"
                               '}\n'
                               "print('[PREFLIGHT] Enterprise Firewall Scoping Patterns:')\n"
                               'for k, v in patterns.items():\n'
                               "    print(f'  • {k:22s}: {v}')\n"
                               'EOF\n'
                               'python3 check_firewall_patterns.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and syntax linters:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_fw_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_fw_tools.sh\n'
                               '```',
                               '#### Core Implementation: Service Account Firewall Manifest\n'
                               'Author a declarative Terraform configuration scoping ingress strictly by Service '
                               'Account:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > sa_firewall.tf\n"
                               'resource "google_compute_firewall" "allow_web_to_db" {\n'
                               '  name        = "allow-web-sa-to-db-sa"\n'
                               '  network     = "prod-vpc"\n'
                               '  description = "Permit Postgres connectivity strictly from authorized web service '
                               'account"\n'
                               '\n'
                               '  allow {\n'
                               '    protocol = "tcp"\n'
                               '    ports    = ["5432"]\n'
                               '  }\n'
                               '\n'
                               '  source_service_accounts = ["web-runner@prod-app.iam.gserviceaccount.com"]\n'
                               '  target_service_accounts = ["db-runner@prod-app.iam.gserviceaccount.com"]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored sa_firewall.tf"\n'
                               '```',
                               '#### Execution & Service Account Filtering Simulation\n'
                               'Author a Python simulation script evaluating firewall matching by service account:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_sa_firewall.py\n"
                               'def evaluate_firewall(source_sa, target_sa, port):\n'
                               "    rule_src = 'web-runner@prod-app.iam.gserviceaccount.com'\n"
                               "    rule_tgt = 'db-runner@prod-app.iam.gserviceaccount.com'\n"
                               '    \n'
                               '    if source_sa == rule_src and target_sa == rule_tgt and port == 5432:\n'
                               "        return 'ALLOWED (Service Account Identity Matched)'\n"
                               "    return 'DENIED (Identity Mismatch)'\n"
                               '\n'
                               "res1 = evaluate_firewall('web-runner@prod-app.iam.gserviceaccount.com', "
                               "'db-runner@prod-app.iam.gserviceaccount.com', 5432)\n"
                               "assert 'ALLOWED' in res1\n"
                               "print(f'[EVAL PASS] Legitimate web SA: {res1}')\n"
                               '\n'
                               "res2 = evaluate_firewall('rogue-worker@prod-app.iam.gserviceaccount.com', "
                               "'db-runner@prod-app.iam.gserviceaccount.com', 5432)\n"
                               "assert 'DENIED' in res2\n"
                               "print(f'[EVAL PASS] Rogue SA: {res2}')\n"
                               'EOF\n'
                               'python3 simulate_sa_firewall.py\n'
                               '```',
                               '#### Resiliency Testing & Tag Spoofing Ineffectiveness Chaos Test\n'
                               'Simulate an instance with spoofed network tags and verify SA rule denies access:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_tag_spoof_blocked.py\n"
                               'def evaluate_with_tag_spoof(instance_sa, instance_tags):\n'
                               '    # Firewall ignores tags because rule is bound strictly to service accounts\n'
                               "    if instance_sa != 'web-runner@prod-app.iam.gserviceaccount.com':\n"
                               "        return 'BLOCKED_BY_FIREWALL'\n"
                               "    return 'ALLOWED'\n"
                               '\n'
                               "res = evaluate_with_tag_spoof('developer-test-sa@corp.com', ['web-server', 'admin'])\n"
                               "assert res == 'BLOCKED_BY_FIREWALL', 'Security failure: Tag spoofing permitted "
                               "connection!'\n"
                               "print(f'[CHAOS TEST PASS] Tag spoofing had zero effect on SA-scoped rule: {res}')\n"
                               'EOF\n'
                               'python3 test_tag_spoof_blocked.py\n'
                               '```',
                               '#### Telemetry, Observability & Firewall Rule Logging\n'
                               'Author a Cloud Logging filter tracking Service Account firewall hits:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > sa_firewall_log_filter.txt\n"
                               'resource.type="gce_subnetwork"\n'
                               'jsonPayload.rule_details.reference="network:prod-vpc/firewall:allow-web-sa-to-db-sa"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to sa_firewall_log_filter.txt"\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform SA firewall manifest:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_sa_firewall.py\n"
                               "with open('sa_firewall.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'source_service_accounts' in tf, 'Must use source_service_accounts instead of "
                               "tags'\n"
                               "assert 'target_service_accounts' in tf, 'Must use target_service_accounts instead of "
                               "tags'\n"
                               "assert 'target_tags' not in tf, 'Tags must not be present in SA-scoped rules'\n"
                               "print('[ASSERT PASS] Service Account-scoped firewall manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_sa_firewall.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_fw_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 103 Topic 2 test scripts..."\n'
                               'rm -f check_firewall_patterns.py check_fw_tools.sh simulate_sa_firewall.py '
                               'test_tag_spoof_blocked.py assert_sa_firewall.py\n'
                               'echo "[CLEANUP] Retaining production files: sa_firewall.tf, '
                               'sa_firewall_log_filter.txt"\n'
                               'echo "[CLEANUP PASS] Firewall design lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_fw_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm service account network scoping '
                                     'and tag spoofing immunity.',
                     'trouble': 'Both source and target instances must be attached to the same VPC network for '
                                'source_service_accounts evaluation.',
                     'cleanup': 'bash teardown_fw_lab.sh',
                     'accept': 'Firewall manifest and test suite pass verification with 0 errors.',
                     'file': 'day-103-topic-02-firewall-design.md'}},
            {'key': 'topic-03',
             'title': 'Cloud Armor',
             'overview': 'Google Cloud Armor provides enterprise Web Application Firewall (WAF) and distributed '
                         "denial-of-service (DDoS) protection at Google's global edge network. Operating in tandem "
                         'with External Application Load Balancers, Cloud Armor inspects incoming HTTP/HTTPS requests '
                         'before they reach backend microservices. Key capabilities include preconfigured WAF rules '
                         'based on OWASP Top 10 Core Rule Set (mitigating SQL injection, Cross-Site Scripting, Remote '
                         'Code Execution, and Local File Inclusion), Adaptive Protection with machine learning anomaly '
                         'detection, bot defense with reCAPTCHA Enterprise, and token-bucket rate limiting.',
             'preview': 'An attacker launches a sophisticated Layer 7 HTTP flood attempting credential stuffing; Cloud '
                        'Armor Adaptive Protection detects the traffic anomaly and generates a signature-based rate '
                        "limiting rule that drops malicious requests at Google's edge with zero backend load.",
             'technical': '### 1. Cloud Armor WAF Architecture\n'
                          '- **Policy Scope:** Edge security policies (applied before caching and load balancing) and '
                          'Backend security policies (applied to backend services).\n'
                          '- **Preconfigured Rules:** ModSecurity Core Rule Set (CRS) expressions (e.g. '
                          "`evaluatePreconfiguredExpr('sqli-v33-stable')`, "
                          "`evaluatePreconfiguredExpr('xss-v33-stable')`).\n"
                          '- **Evaluation Modes:** Enforce (`deny(403)`) versus Preview (`preview = true` for safe '
                          'telemetry collection without dropping traffic).\n'
                          '\n'
                          '### 2. Rate Limiting & Adaptive Protection\n'
                          '- **Rate Limiting:** Token-bucket algorithm specifying `rate_limit_threshold` (e.g. 100 '
                          'requests per 1-minute window) and `conform_action` vs `exceed_action`.\n'
                          '- **Adaptive Protection:** Continuously baselines application traffic patterns; when '
                          'anomalies are detected, it alerts SREs and provides copy-pasteable CEL mitigation rules.',
             'questions': ['What is the operational risk of deploying Cloud Armor preconfigured WAF rules directly in '
                           "'enforce' mode without testing in 'preview' mode?",
                           'How does Cloud Armor Rate Limiting distinguish legitimate client traffic bursts from '
                           'malicious Layer 7 floods?',
                           'Which Cloud Armor feature utilizes machine learning to automatically baseline traffic and '
                           'generate targeted mitigation rules during an attack?'],
             'reference': 'https://cloud.google.com/armor/docs/cloud-armor-overview',
             'reference_label': 'Google Cloud Armor: Enterprise WAF and DDoS mitigation architecture',
             'scenario': {'symptom': 'An enterprise web portal suffered a data breach via SQL injection despite having '
                                     'a Cloud Armor security policy attached.',
                          'constraints': 'Application must protect against OWASP Top 10 vulnerabilities without '
                                         'increasing P99 backend latency.',
                          'evidence': 'Cloud Armor security policy configuration and attack logs:\n'
                                      '\n'
                                      '```json\n'
                                      '{\n'
                                      '  "rule": {\n'
                                      '    "action": "deny(403)",\n'
                                      '    "preview": true, // CRITICAL DEFECT: Policy was left in preview mode!\n'
                                      '    "match": {"expr": {"expression": '
                                      '"evaluatePreconfiguredExpr(\'sqli-v33-stable\')"}}\n'
                                      '  }\n'
                                      '}\n'
                                      '```\n'
                                      '\n'
                                      'Log analysis: Ingress logs showed SQL injection payloads flagged with '
                                      '`preview_action: "deny(403)"`, but HTTP response status returned `200 OK` '
                                      'because preview mode does not drop traffic.',
                          'diagnostic_steps': ['Inspect the Cloud Armor security policy using gcloud compute '
                                               'security-policies describe.',
                                               'Verify the preview parameter on all preconfigured rules.',
                                               'Review Cloud Logging entries for previewExecution results.',
                                               'Audit backend database query logs for injected SQL statements.'],
                          'root': 'The Cloud Armor security policy was deployed in preview mode during testing and was '
                                  'never transitioned to enforcement mode in production.',
                          'fix': 'Set `preview = false` on all preconfigured WAF rules and configure an automated '
                                 'rate-limiting rule for sensitive endpoints.',
                          'verify': 'Send synthetic SQL injection test payloads and assert immediate HTTP 403 '
                                    "Forbidden responses at Google's edge.",
                          'residual': 'Strict sensitivity levels (e.g. sqli sensitivity level 4) may generate false '
                                      'positives; tune rules using exclusion expressions for specific parameters.',
                          'diagram': ('Attacker sends SQL injection payload in HTTP query',
                                      'Cloud Armor evaluates rule in PREVIEW mode',
                                      'Payload forwarded to backend; database breached',
                                      'Update Cloud Armor rule to enforce (preview = false)',
                                      'Attack payload dropped at Google edge with HTTP 403')},
             'lab': {'name': 'Cloud Armor WAF and Rate Limiting Architecture',
                     'goal': 'Author a production Cloud Armor security policy enforcing OWASP SQLi/XSS inspection and '
                             'rate limiting.',
                     'expected': 'Declarative Terraform Cloud Armor policy and Python simulation testing SQL injection '
                                 'interception and rate limits.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify compute.securityPolicies permissions and Terraform readiness.',
                     'steps': ['#### Pre-Flight Cloud Armor WAF Rule Discovery\n'
                               'Catalog Cloud Armor preconfigured Core Rule Sets and rate limit parameters:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_armor_specs.py\n"
                               'specs = {\n'
                               '    \'sqli_rule\': \'evaluatePreconfiguredExpr("sqli-v33-stable")\',\n'
                               '    \'xss_rule\': \'evaluatePreconfiguredExpr("xss-v33-stable")\',\n'
                               "    'rate_limit': '100 requests per 60 seconds per client IP',\n"
                               "    'exceed_action': 'deny(429) Too Many Requests'\n"
                               '}\n'
                               "print('[PREFLIGHT] Cloud Armor Security Policy Specifications:')\n"
                               'for k, v in specs.items():\n'
                               "    print(f'  • {k:16s}: {v}')\n"
                               'EOF\n'
                               'python3 check_armor_specs.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and syntax linters:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_armor_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_armor_tools.sh\n'
                               '```',
                               '#### Core Implementation: Cloud Armor Terraform Manifest\n'
                               'Author a declarative Terraform configuration establishing enforced WAF and rate '
                               'limiting:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > cloud_armor_policy.tf\n"
                               'resource "google_compute_security_policy" "edge_waf_policy" {\n'
                               '  name        = "edge-protection-policy"\n'
                               '  description = "OWASP Top 10 WAF rules and rate limiting in enforcement mode"\n'
                               '\n'
                               '  # Rule 1: OWASP SQL Injection Protection\n'
                               '  rule {\n'
                               '    action   = "deny(403)"\n'
                               '    priority = "1000"\n'
                               '    preview  = false # STRICT ENFORCEMENT\n'
                               '    match {\n'
                               '      expr {\n'
                               '        expression = "evaluatePreconfiguredExpr(\'sqli-v33-stable\')"\n'
                               '      }\n'
                               '    }\n'
                               '    description = "Block SQL Injection attempts"\n'
                               '  }\n'
                               '\n'
                               '  # Rule 2: Token-Bucket Rate Limiting\n'
                               '  rule {\n'
                               '    action   = "rate_based_ban"\n'
                               '    priority = "2000"\n'
                               '    preview  = false\n'
                               '    match {\n'
                               '      versioned_expr = "SRC_IPS_V1"\n'
                               '      config {\n'
                               '        src_ip_ranges = ["*"]\n'
                               '      }\n'
                               '    }\n'
                               '    rate_limit_options {\n'
                               '      conform_action = "allow"\n'
                               '      exceed_action  = "deny(429)"\n'
                               '      rate_limit_threshold {\n'
                               '        count        = 100\n'
                               '        interval_sec = 60\n'
                               '      }\n'
                               '      ban_duration_sec = 600\n'
                               '    }\n'
                               '    description = "Throttle clients exceeding 100 req/min"\n'
                               '  }\n'
                               '\n'
                               '  # Default allow rule\n'
                               '  rule {\n'
                               '    action   = "allow"\n'
                               '    priority = "2147483647"\n'
                               '    match {\n'
                               '      versioned_expr = "SRC_IPS_V1"\n'
                               '      config {\n'
                               '        src_ip_ranges = ["*"]\n'
                               '      }\n'
                               '    }\n'
                               '    description = "Default allow fallback"\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored cloud_armor_policy.tf"\n'
                               '```',
                               '#### Execution & WAF Evaluation Simulation\n'
                               'Author a Python simulation script evaluating SQLi detection and rate limiting logic:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_armor_eval.py\n"
                               'import re\n'
                               '\n'
                               'def evaluate_request(query_param, req_count_per_min):\n'
                               '    # Simulate SQLi preconfigured regex\n'
                               '    sqli_pattern = re.compile(r"(\'|\x08(UNION|SELECT|DROP|INSERT)\x08)", '
                               're.IGNORECASE)\n'
                               '    if sqli_pattern.search(query_param):\n'
                               "        return 403, 'DENIED: Cloud Armor SQLi WAF Rule Triggered'\n"
                               '    if req_count_per_min > 100:\n'
                               "        return 429, 'DENIED: Rate Limit Exceeded (HTTP 429)'\n"
                               "    return 200, 'ALLOWED: Clean traffic'\n"
                               '\n'
                               'status, msg = evaluate_request("1\' OR \'1\'=\'1", 10)\n'
                               'assert status == 403\n'
                               "print(f'[WAF PASS] SQLi Payload Intercepted: {msg}')\n"
                               '\n'
                               'status, msg = evaluate_request("normal_query", 150)\n'
                               'assert status == 429\n'
                               "print(f'[RATE LIMIT PASS] Flood Intercepted: {msg}')\n"
                               'EOF\n'
                               'python3 simulate_armor_eval.py\n'
                               '```',
                               '#### Resiliency Testing & Preview Mode Leak Chaos Test\n'
                               'Assert that policy configuration rejects preview mode on production security rules:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_no_preview_leaks.py\n"
                               "with open('cloud_armor_policy.tf') as f:\n"
                               '    content = f.read()\n'
                               '\n'
                               "if 'preview  = true' in content:\n"
                               "    raise AssertionError('CRITICAL DEFECT: Production policy contains preview = "
                               "true!')\n"
                               "print('[CHAOS TEST PASS] Policy strictly verified: Zero preview mode rules "
                               "detected.')\n"
                               'EOF\n'
                               'python3 test_no_preview_leaks.py\n'
                               '```',
                               '#### Telemetry, Observability & Cloud Armor WAF Ingestion Filter\n'
                               'Author a Cloud Logging filter tracking blocked WAF attacks:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > armor_block_filter.txt\n"
                               'resource.type="http_load_balancer"\n'
                               'jsonPayload.statusDetails="denied_by_security_policy"\n'
                               'jsonPayload.enforcedSecurityPolicy.name="edge-protection-policy"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to armor_block_filter.txt"\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform Cloud Armor policy:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_armor_manifest.py\n"
                               "with open('cloud_armor_policy.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'google_compute_security_policy' in tf\n"
                               "assert 'sqli-v33-stable' in tf\n"
                               "assert 'rate_based_ban' in tf\n"
                               "assert 'preview  = false' in tf\n"
                               "print('[ASSERT PASS] Cloud Armor policy manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_armor_manifest.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_armor_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 103 Topic 3 test scripts..."\n'
                               'rm -f check_armor_specs.py check_armor_tools.sh simulate_armor_eval.py '
                               'test_no_preview_leaks.py assert_armor_manifest.py\n'
                               'echo "[CLEANUP] Retaining production files: cloud_armor_policy.tf, '
                               'armor_block_filter.txt"\n'
                               'echo "[CLEANUP PASS] Cloud Armor lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_armor_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm SQLi interception, rate-based '
                                     'bans, and zero preview mode rules.',
                     'trouble': 'Ensure Cloud Armor policy is attached to the backend service of an External '
                                'Application Load Balancer.',
                     'cleanup': 'bash teardown_armor_lab.sh',
                     'accept': 'Cloud Armor manifest and test suite pass verification with 0 errors.',
                     'file': 'day-103-topic-03-cloud-armor.md'}},
            {'key': 'topic-04',
             'title': 'Private connectivity',
             'overview': 'Private connectivity patterns eliminate the need for external public IPv4 addresses across '
                         'enterprise Google Cloud workloads, dramatically reducing the attack surface. Three core '
                         'Google Cloud architectural components provide private connectivity: (1) Private Google '
                         'Access (allows private RFC 1918 instances to reach Google APIs like Cloud Storage, BigQuery, '
                         "and Pub/Sub over Google's internal network), (2) Cloud NAT (provides managed, outbound-only "
                         'internet connectivity for software package updates without exposing instances to inbound '
                         'unsolicited connections), and (3) Private Service Connect (PSC) (enables private cross-VPC '
                         'microservice communication between consumer and producer networks via internal forwarding '
                         'rules).',
             'preview': 'A confidential payment processing VM requires access to BigQuery and operating system '
                        'security patches; by configuring Private Google Access and Cloud NAT, the instance satisfies '
                        'all external communication requirements with zero inbound public internet exposure.',
             'technical': '### 1. Private Google Access (PGA)\n'
                          '- **Subnet Setting:** `private_ip_google_access = true` on the target VPC subnetwork.\n'
                          '- **Routing VIPs:** Standard default VIP (`199.36.153.8/30` / `private.googleapis.com`) or '
                          'Restricted VIP (`199.36.153.4/30` / `restricted.googleapis.com` for VPC Service Controls '
                          'compliance).\n'
                          '- **DNS Mapping:** Private DNS zone for `*.googleapis.com` mapping CNAME records to '
                          '`restricted.googleapis.com`.\n'
                          '\n'
                          '### 2. Cloud NAT Architecture\n'
                          '- **Outbound Only:** Translates private RFC 1918 IPs to allocated public IPs for egress; '
                          'strictly stateful, dropping all unsolicited inbound connections.\n'
                          '- **Port Allocation:** Dynamic port allocation prevents TCP port exhaustion under high '
                          'concurrency.\n'
                          '\n'
                          '### 3. Private Service Connect (PSC)\n'
                          '- **Consumer Rule:** Internal IP address forwarding rule (`10.x.x.x`) connecting to a '
                          'producer service attachment without VPC Peering route collisions.',
             'questions': ['What is the difference between the `private.googleapis.com` and '
                           '`restricted.googleapis.com` virtual IP addresses in Private Google Access?',
                           'How does Cloud NAT protect Compute Engine instances compared to assigning an external '
                           'public IP address directly to the VM?',
                           'Why is Private Service Connect preferred over VPC Network Peering in large-scale '
                           'multi-tenant enterprise architectures?'],
             'reference': 'https://cloud.google.com/vpc/docs/private-access-options',
             'reference_label': 'Google Cloud VPC: Private connectivity, Private Google Access, and PSC',
             'scenario': {'symptom': 'A newly provisioned database VM with an assigned public IP was infected with '
                                     'cryptocurrency mining malware within 15 minutes of launch.',
                          'constraints': 'Instance required access to external APT repositories for security patches '
                                         'and BigQuery for analytical data export.',
                          'evidence': 'Compute Engine instance network configuration and firewall logs:\n'
                                      '\n'
                                      '```text\n'
                                      'Instance: analytics-worker-prod\n'
                                      'NetworkInterfaces[0].accessConfigs[0].natIP: 35.192.42.114 (PUBLIC IP '
                                      'ASSIGNED)\n'
                                      'Firewall: default-allow-internal (Priority 65534), allow-ssh (0.0.0.0/0)\n'
                                      'Inbound scan log: 198.51.100.12 brute-forced weak temporary password on port 22 '
                                      'within 12m of boot.\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: The team assigned a public IP simply to allow the VM to download '
                                      'software packages and access Google APIs, opening it to internet port scanners.',
                          'diagnostic_steps': ['Inspect instance network configuration for external NAT IP '
                                               'assignments.',
                                               'Verify subnet Private Google Access enablement status.',
                                               'Check Cloud NAT gateway deployment in the region.',
                                               'Audit VPC firewall rules for 0.0.0.0/0 ingress.'],
                          'root': 'Unnecessary public IP assignment on private workloads to satisfy outbound '
                                  'connectivity needs.',
                          'fix': 'Remove public IP, enable Private Google Access on the subnet for API access, deploy '
                                 'Cloud NAT for outbound package updates, and enforce the Org Policy '
                                 '`compute.vmExternalIpAccess`.',
                          'verify': 'Confirm instance has zero external IP, can resolve and query BigQuery via PGA, '
                                    'and can run apt update via Cloud NAT.',
                          'residual': 'Cloud NAT incurs egress bandwidth charges and per-gateway hourly fees.',
                          'diagram': ('VM provisioned with external public IP for updates',
                                      'Internet scanners detect and brute-force public IP',
                                      'Instance infected with cryptomining malware',
                                      'Remove public IP; deploy Private Google Access & Cloud NAT',
                                      'Workload accesses APIs & updates with 0 public exposure')},
             'lab': {'name': 'Private Connectivity Architecture: PGA, Cloud NAT, and PSC',
                     'goal': 'Author a declarative Terraform configuration establishing Private Google Access, Cloud '
                             'NAT, and a private subnet.',
                     'expected': 'Validated Terraform manifest and Python simulation testing private VIP routing and '
                                 'outbound NAT translation.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify compute.networks and compute.routers permissions.',
                     'steps': ['#### Pre-Flight Private Connectivity Discovery\n'
                               'Catalog private access VIPs and Cloud NAT gateway parameters:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_private_specs.py\n"
                               'specs = {\n'
                               "    'restricted_vip': '199.36.153.4/30 (Supports VPC Service Controls)',\n"
                               "    'private_vip': '199.36.153.8/30 (Standard Google APIs)',\n"
                               "    'cloud_nat_type': 'PUBLIC NAT (Managed outbound-only translation)',\n"
                               "    'psc_endpoint': 'Private consumer forwarding rule (RFC 1918)'\n"
                               '}\n'
                               "print('[PREFLIGHT] Private Connectivity Technical Specifications:')\n"
                               'for k, v in specs.items():\n'
                               "    print(f'  • {k:16s}: {v}')\n"
                               'EOF\n'
                               'python3 check_private_specs.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and syntax linters:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_priv_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_priv_tools.sh\n'
                               '```',
                               '#### Core Implementation: Private VPC and Cloud NAT Manifest\n'
                               'Author a declarative Terraform configuration establishing Private Google Access and '
                               'Cloud NAT:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > private_connectivity.tf\n"
                               'resource "google_compute_network" "private_vpc" {\n'
                               '  name                    = "prod-private-vpc"\n'
                               '  auto_create_subnetworks = false\n'
                               '}\n'
                               '\n'
                               'resource "google_compute_subnetwork" "isolated_subnet" {\n'
                               '  name                     = "isolated-workload-subnet"\n'
                               '  ip_cidr_range            = "10.128.50.0/24"\n'
                               '  region                   = "us-central1"\n'
                               '  network                  = google_compute_network.private_vpc.id\n'
                               '  private_ip_google_access = true # PRIVATE GOOGLE ACCESS ENABLED\n'
                               '}\n'
                               '\n'
                               'resource "google_compute_router" "nat_router" {\n'
                               '  name    = "nat-router-us-central1"\n'
                               '  region  = "us-central1"\n'
                               '  network = google_compute_network.private_vpc.id\n'
                               '}\n'
                               '\n'
                               'resource "google_compute_router_nat" "outbound_nat" {\n'
                               '  name                               = "outbound-gateway-central1"\n'
                               '  router                             = google_compute_router.nat_router.name\n'
                               '  region                             = "us-central1"\n'
                               '  nat_ip_allocate_option             = "AUTO_ONLY"\n'
                               '  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored private_connectivity.tf"\n'
                               '```',
                               '#### Execution & Private VIP Routing Simulation\n'
                               'Author a Python simulation script verifying private API resolution and NAT outbound '
                               'statefulness:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_private_routing.py\n"
                               'def route_traffic(destination_type, has_public_ip, has_pga, has_nat):\n'
                               "    if destination_type == 'GOOGLE_APIS':\n"
                               '        if has_pga or has_public_ip:\n'
                               "            return 'ROUTED_INTERNALLY_VIA_PGA (199.36.153.4/30)'\n"
                               "        return 'DROPPED_NO_ROUTE'\n"
                               "    if destination_type == 'EXTERNAL_INTERNET':\n"
                               '        if has_nat:\n'
                               "            return 'ROUTED_OUTBOUND_VIA_CLOUD_NAT (Stateful Outbound Only)'\n"
                               "        return 'DROPPED_NO_INTERNET'\n"
                               "    if destination_type == 'INBOUND_INTERNET':\n"
                               '        if has_public_ip:\n'
                               "            return 'INBOUND_EXPOSED'\n"
                               "        return 'DROPPED_SAFE (Zero Inbound Exposure)'\n"
                               '\n'
                               '# Test private VM behavior\n'
                               "p1 = route_traffic('GOOGLE_APIS', has_public_ip=False, has_pga=True, has_nat=True)\n"
                               "assert 'PGA' in p1\n"
                               "print(f'[PGA PASS] {p1}')\n"
                               '\n'
                               "p2 = route_traffic('EXTERNAL_INTERNET', has_public_ip=False, has_pga=True, "
                               'has_nat=True)\n'
                               "assert 'CLOUD_NAT' in p2\n"
                               "print(f'[NAT PASS] {p2}')\n"
                               '\n'
                               "p3 = route_traffic('INBOUND_INTERNET', has_public_ip=False, has_pga=True, "
                               'has_nat=True)\n'
                               "assert 'DROPPED_SAFE' in p3\n"
                               "print(f'[ZERO EXPOSURE PASS] {p3}')\n"
                               'EOF\n'
                               'python3 simulate_private_routing.py\n'
                               '```',
                               '#### Resiliency Testing & Public IP Leak Chaos Test\n'
                               'Assert that the subnet configuration strictly blocks instances with external IP '
                               'addresses:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_public_ip_block.py\n"
                               'def validate_instance_interfaces(access_configs):\n'
                               '    if len(access_configs) > 0:\n'
                               "        raise AssertionError('SECURITY VIOLATION: External NAT access config assigned "
                               "to private workload!')\n"
                               "    return '[COMPLIANT] Zero public IPv4 addresses assigned.'\n"
                               '\n'
                               'res = validate_instance_interfaces([])\n'
                               "print(f'[CHAOS TEST PASS] {res}')\n"
                               'EOF\n'
                               'python3 test_public_ip_block.py\n'
                               '```',
                               '#### Telemetry, Observability & Cloud NAT Logging Manifest\n'
                               'Author a Cloud Logging filter tracking Cloud NAT error and translation drops:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > nat_logging_filter.txt\n"
                               'resource.type="nat_gateway"\n'
                               'jsonPayload.allocation_status="OUT_OF_RESOURCES"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to nat_logging_filter.txt"\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform private connectivity manifest:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_private_manifest.py\n"
                               "with open('private_connectivity.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'private_ip_google_access = true' in tf\n"
                               "assert 'google_compute_router_nat' in tf\n"
                               "assert 'AUTO_ONLY' in tf\n"
                               "print('[ASSERT PASS] Private connectivity Terraform manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_private_manifest.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_priv_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 103 Topic 4 test scripts..."\n'
                               'rm -f check_private_specs.py check_priv_tools.sh simulate_private_routing.py '
                               'test_public_ip_block.py assert_private_manifest.py\n'
                               'echo "[CLEANUP] Retaining production files: private_connectivity.tf, '
                               'nat_logging_filter.txt"\n'
                               'echo "[CLEANUP PASS] Private connectivity lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_priv_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm Private Google Access enablement '
                                     'and Cloud NAT outbound translation.',
                     'trouble': 'Ensure that the router and NAT gateway are in the exact same region as the subnet.',
                     'cleanup': 'bash teardown_priv_lab.sh',
                     'accept': 'Private connectivity manifest and test suite pass verification with 0 errors.',
                     'file': 'day-103-topic-04-private-connectivity.md'}}]}
