"""day_data_104.py — Exhaustive architecture data specification for Day 104.

Covers VPC Service Controls, Cloud NGFW/IDS, and Secure Web Proxy.
"""

DAY_NUM = 104

DATA = {'day': 104,
 'part1_intro': 'Day 104 establishes the enterprise architecture for data perimeters, advanced threat prevention, and '
                'outbound egress governance. Architects analyze the configuration of VPC Service Controls (VPC-SC) to '
                'prevent data exfiltration across managed Google Cloud APIs, the deployment of Cloud Next Generation '
                'Firewall (NGFW Enterprise) and Cloud IDS for deep packet inspection and intrusion prevention, and the '
                'enforcement of Google Cloud Secure Web Proxy (SWP) for granular FQDN-based outbound web filtering and '
                'TLS inspection.',
 'exit_summary': 'Engineers master VPC Service Controls service perimeter manifests with dry-run evaluation, Cloud '
                 'NGFW Enterprise threat prevention profiles with intrusion detection, and Secure Web Proxy gateway '
                 'policies enforcing strict FQDN whitelisting for outbound workloads.',
 'part2_intro': 'The following architectural matrix details the technical trade-offs, operational protocols, and '
                'security boundaries across VPC Service Controls data perimeters, Cloud NGFW/IDS deep inspection, and '
                'Secure Web Proxy egress filtering.',
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
                    '<td><strong>Data Perimeter</strong></td>\n'
                    '<td>VPC Service Controls</td>\n'
                    '<td>Restricted VIP &amp; API Headers</td>\n'
                    '<td>Service Perimeter Envelope</td>\n'
                    '<td>Prevents copying data between authorized and unauthorized buckets, regardless of IAM.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Intrusion Prevention</strong></td>\n'
                    '<td>Cloud NGFW Enterprise &amp; IDS</td>\n'
                    '<td>Layer 7 AppID &amp; Threat Signatures</td>\n'
                    '<td>Network Inspection Profile</td>\n'
                    '<td>Deep packet inspection drops known malware, C2 beacons, and buffer overflow exploits.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Outbound Egress</strong></td>\n'
                    '<td>Secure Web Proxy</td>\n'
                    '<td>Explicit HTTP/S Proxy &amp; TLS</td>\n'
                    '<td>SWP Gateway Resource</td>\n'
                    '<td>Outbound internet traffic strictly filtered by FQDN whitelist; unapproved domains '
                    'dropped.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Threat Analytics</strong></td>\n'
                    '<td>Security Command Center</td>\n'
                    '<td>Cloud Logging &amp; Eventarc</td>\n'
                    '<td>SIEM Threat Event Stream</td>\n'
                    '<td>All VPC-SC violations, IDS threats, and proxy denies stream to central SOC in real '
                    'time.</td>\n'
                    '</tr>\n'
                    '</tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 104: Data Perimeters, Cloud NGFW/IDS, and Secure Web Proxy',
                  'desc': 'Architectural topology showing VPC Service Controls data perimeter, Cloud NGFW deep packet '
                          'inspection, and Secure Web Proxy egress filtering.',
                  'caption': 'Figure 104.1: Multi-tier data perimeter and threat defense topology featuring VPC '
                             'Service Controls, Cloud NGFW Enterprise IPS, and Secure Web Proxy.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Managed Google Cloud Services & Protected APIs',
                              'desc': 'Cloud Storage, BigQuery, and Pub/Sub enclosed in cryptographic data perimeters',
                              'y': 10,
                              'h': 90,
                              'stroke': '#38bdf8',
                              'fill': '#0c1e38',
                              'title_color': '#38bdf8'},
                             {'name': 'LAYER 2: VPC Service Controls Data Perimeter Boundary',
                              'desc': 'Service perimeter, dry-run simulation mode, and directional ingress/egress '
                                      'rules',
                              'y': 115,
                              'h': 90,
                              'stroke': '#818cf8',
                              'fill': '#141838',
                              'title_color': '#818cf8'},
                             {'name': 'LAYER 3: Internal VPC Workload & Private Subnet Plane',
                              'desc': 'GCE instances, GKE workloads, and private VPC networks with zero public IPs',
                              'y': 220,
                              'h': 90,
                              'stroke': '#f59e0b',
                              'fill': '#261a08',
                              'title_color': '#f59e0b'},
                             {'name': 'LAYER 4: Cloud NGFW Enterprise & Cloud IDS Deep Inspection',
                              'desc': 'Palo Alto Networks threat engine, Layer 7 AppID inspection, and packet '
                                      'mirroring',
                              'y': 325,
                              'h': 90,
                              'stroke': '#f43f5e',
                              'fill': '#2a0a14',
                              'title_color': '#f43f5e'},
                             {'name': 'LAYER 5: Secure Web Proxy (SWP) Egress & SOC Telemetry',
                              'desc': 'Cloud-first outbound proxy, FQDN whitelisting, and Security Command Center '
                                      'alerts',
                              'y': 430,
                              'h': 90,
                              'stroke': '#22c55e',
                              'fill': '#072417',
                              'title_color': '#22c55e'}],
                  'components': [{'name': 'Cloud Storage Vault',
                                  'detail': 'Protected Bucket Data',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'BigQuery Data Warehouse',
                                  'detail': 'Protected Analytics',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'VPC-SC Perimeter',
                                  'detail': 'Restricted Service Policy',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Dry-Run Simulator',
                                  'detail': 'Violation Telemetry',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Private Compute Instance',
                                  'detail': '10.128.0.4 Workload',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Private GKE Nodes',
                                  'detail': '10.128.10.0/24 Cluster',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Cloud NGFW Enterprise',
                                  'detail': 'Layer 7 AppID & IPS',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Cloud IDS Threat Prober',
                                  'detail': 'Deep Packet Mirroring',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Secure Web Proxy',
                                  'detail': 'FQDN Whitelist Gateway',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'},
                                 {'name': 'Security Command Center',
                                  'detail': 'SOC Threat Dashboard',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'}],
                  'boundaries': [{'label': 'RESTRICTED API DATA PERIMETER (VPC-SC)',
                                  'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'color': '#38bdf8'},
                                 {'label': 'PRIVATE WORKLOAD & INLINE DEEP PACKET INSPECTION',
                                  'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#818cf8'},
                                 {'label': 'SECURE OUTBOUND EGRESS & THREAT TELEMETRY VAULT',
                                  'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#22c55e'}],
                  'flows': [{'x1': 340,
                             'y1': 56,
                             'x2': 420,
                             'y2': 56,
                             'label': 'Block Unauthorized Copy',
                             'type': 'fail'},
                            {'x1': 210,
                             'y1': 82,
                             'x2': 210,
                             'y2': 135,
                             'label': 'Evaluate Perimeter Rule',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'label': 'Simulate Dry-Run Impact',
                             'type': 'ok'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'label': 'Authorize In-Perimeter API',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 266,
                             'x2': 420,
                             'y2': 266,
                             'label': 'Mirror Suspicious Traffic',
                             'type': 'warn'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'label': 'Inspect Layer 7 Packets',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'label': 'Drop C2 Malware Beacon',
                             'type': 'fail'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'label': 'Route Outbound to Proxy',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'label': 'Stream Threat Telemetry',
                             'type': 'ok'}],
                  'probes': [{'cx': 80,
                              'cy': 135,
                              'label': 'PROBE 1: VPC-SC Perimeter Violation Intercept',
                              'badge': 'P1',
                              'color': '#38bdf8'},
                             {'cx': 80,
                              'cy': 345,
                              'label': 'PROBE 2: Cloud NGFW Threat Signature Match',
                              'badge': 'P2',
                              'color': '#f43f5e'},
                             {'cx': 80,
                              'cy': 450,
                              'label': 'PROBE 3: Secure Web Proxy Unapproved FQDN Block',
                              'badge': 'P3',
                              'color': '#22c55e'}]},
 'part3_intro': 'The following field cases analyze real-world production data exfiltration attempts, firewall '
                'inspection limitations, and outbound proxy failures: a rogue insider incident where a developer with '
                'valid credentials attempted to export confidential customer tables to an external personal project, '
                'successfully intercepted by VPC Service Controls, an insidious command-and-control beacon operating '
                'over standard port 443 that slipped past traditional Layer 4 stateful firewalls but was detected and '
                'severed by Cloud NGFW Enterprise Layer 7 IPS, and a compromised container that attempted to download '
                'secondary exploitation payloads from an untrusted public domain, dropped immediately by Secure Web '
                "Proxy's strict FQDN whitelisting rules. Each case details verbatim logs, terminal transcripts, root "
                'cause mechanics, defensible remediations, and dual-lane failed/corrected flow diagrams.',
 'part4_intro': 'These hands-on exercises implement the comprehensive 8-stage operational engineering lifecycle for '
                'Day 104. Engineers construct production VPC Service Controls perimeter manifests with dry-run '
                'validation, author Cloud NGFW Enterprise security profiles with intrusion prevention system rules, '
                'and deploy Secure Web Proxy gateway configurations enforcing granular FQDN whitelisting and egress '
                'monitoring.',
 'topics': [{'key': 'topic-01',
             'title': 'VPC Service Controls',
             'overview': 'VPC Service Controls (VPC-SC) establishes a data-centric security perimeter around Google '
                         'Cloud managed services, such as Cloud Storage, BigQuery, Pub/Sub, and Cloud SQL. Unlike IAM '
                         '(which governs who can access a resource), VPC-SC governs where and under what network '
                         'context resources can be accessed. It prevents unauthorized data copying and exfiltration: '
                         'even if an identity possesses project Owner or Storage Admin privileges, VPC-SC blocks '
                         'copying data from a perimeter-protected bucket to an external, unapproved bucket or reading '
                         'data from outside an authorized Access Level.',
             'preview': 'An authorized data engineer attempts to run `gsutil cp` from a corporate analytical bucket to '
                        "an external contractor's bucket; VPC Service Controls intercepts the API call at the Google "
                        'API edge, returning a VPC-SC perimeter violation error.',
             'technical': '### 1. VPC-SC Architecture\n'
                          '- **Service Perimeter:** Groups projects and services into an isolated security boundary.\n'
                          '- **Restricted Services:** Specific APIs protected by the perimeter (e.g. '
                          '`storage.googleapis.com`, `bigquery.googleapis.com`).\n'
                          '- **Access Levels:** Context-Aware Access conditions defining who can access the perimeter '
                          'from outside (IP ranges, device health, identities).\n'
                          '- **Ingress & Egress Rules:** Granular directional rules allowing cross-perimeter data '
                          'flows based on caller identity, target project, and API method.\n'
                          '\n'
                          '### 2. Operational Invariants & Dry-Run Mode\n'
                          '- **Dry-Run Perimeters:** Allows administrators to test perimeter configurations in '
                          'production without disrupting active workloads. Violations are logged to Cloud Logging '
                          'without blocking traffic.\n'
                          '- **Restricted VIP Requirement:** Workloads within the perimeter must route traffic to '
                          '`restricted.googleapis.com` (`199.36.153.4/30`), not `private.googleapis.com`.',
             'questions': ['How does VPC Service Controls prevent an authorized user with project Owner permissions '
                           'from exfiltrating data to an external personal GCP project?',
                           'What is the operational function of VPC Service Controls Dry-Run mode?',
                           'Why must workloads in a VPC Service Controls perimeter use the Restricted VIP '
                           '(199.36.153.4/30) instead of the Private VIP?'],
             'reference': 'https://cloud.google.com/vpc-service-controls/docs/overview',
             'reference_label': 'Google Cloud VPC Service Controls: Data perimeters, ingress/egress rules, and dry-run',
             'scenario': {'symptom': 'An automated nightly BigQuery export job failed immediately with an HTTP 403 VPC '
                                     'Service Controls violation.',
                          'constraints': 'Production datasets must be protected from external exfiltration, but '
                                         'automated cross-project analytical jobs must execute reliably.',
                          'evidence': 'Cloud Audit Activity log showing VPC-SC violation:\n'
                                      '\n'
                                      '```json\n'
                                      '{\n'
                                      '  "protoPayload": {\n'
                                      '    "serviceName": "bigquery.googleapis.com",\n'
                                      '    "methodName": "jobservice.insert",\n'
                                      '    "status": {\n'
                                      '      "code": 7,\n'
                                      '      "message": "Request is prohibited by organization\'s policy. '
                                      'vpcServiceControlsUniqueIdentifier: 8f12a9-91823-4c5d"\n'
                                      '    }\n'
                                      '  }\n'
                                      '}\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: The analytics team moved the destination dataset into a new project '
                                      'that had not been added to the service perimeter or granted an explicit egress '
                                      'rule.',
                          'diagnostic_steps': ['Extract the vpcServiceControlsUniqueIdentifier from the audit log.',
                                               'Query Cloud Logging for the unique identifier to view the full VPC-SC '
                                               'violation payload.',
                                               'Verify the source project, destination project, and caller service '
                                               'account.',
                                               'Inspect existing perimeter ingress and egress rule bindings.'],
                          'root': 'Destination project was outside the VPC Service Controls perimeter, and no scoped '
                                  'egress rule existed to permit cross-perimeter data transfer.',
                          'fix': 'Author a scoped VPC-SC egress rule allowing the export service account to copy data '
                                 'specifically to the destination project dataset.',
                          'verify': 'Execute the BigQuery export job in dry-run mode, confirm zero violations in audit '
                                    'logs, and promote rule to enforced perimeter.',
                          'residual': 'Cross-perimeter egress rules must specify exact operations to avoid opening '
                                      'broad exfiltration avenues.',
                          'diagram': ('Nightly export job attempts cross-project BigQuery copy',
                                      'Destination project outside perimeter envelope',
                                      'VPC-SC blocks request with HTTP 403 policy violation',
                                      'Configure scoped VPC-SC egress rule for export service account',
                                      'Job completes successfully within verified security boundary')},
             'lab': {'name': 'VPC Service Controls Perimeter and Dry-Run Architecture',
                     'goal': 'Author a declarative Terraform VPC-SC perimeter with dry-run testing and scoped egress '
                             'rules.',
                     'expected': 'Validated Terraform VPC-SC manifest and Python simulation testing violation '
                                 'interception and egress rules.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify Access Context Manager policy administrative permissions.',
                     'steps': ['#### Pre-Flight VPC Service Controls Discovery\n'
                               'Catalog VPC-SC perimeter specifications and protected services:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_vpcs_specs.py\n"
                               'specs = {\n'
                               "    'restricted_services': ['storage.googleapis.com', 'bigquery.googleapis.com'],\n"
                               "    'restricted_vip': '199.36.153.4/30',\n"
                               "    'mode': 'DRY_RUN (Recommended for staging before enforcement)'\n"
                               '}\n'
                               "print('[PREFLIGHT] VPC Service Controls Specifications:')\n"
                               'for k, v in specs.items():\n'
                               "    print(f'  • {k:22s}: {v}')\n"
                               'EOF\n'
                               'python3 check_vpcs_specs.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and JSON parser readiness:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_vpcs_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_vpcs_tools.sh\n'
                               '```',
                               '#### Core Implementation: VPC-SC Perimeter Terraform Manifest\n'
                               'Author a declarative Terraform configuration establishing a VPC Service Controls '
                               'perimeter in dry-run mode with scoped egress:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > vpc_service_controls.tf\n"
                               'resource "google_access_context_manager_service_perimeter" "secure_data_perimeter" {\n'
                               '  parent         = "accessPolicies/108420918237"\n'
                               '  name           = '
                               '"accessPolicies/108420918237/servicePerimeters/secure_data_perimeter"\n'
                               '  title          = "Secure Data Analytics Perimeter"\n'
                               '  perimeter_type = "PERIMETER_TYPE_REGULAR"\n'
                               '\n'
                               '  spec {\n'
                               '    resources = [\n'
                               '      "projects/108420918237"\n'
                               '    ]\n'
                               '\n'
                               '    restricted_services = [\n'
                               '      "storage.googleapis.com",\n'
                               '      "bigquery.googleapis.com"\n'
                               '    ]\n'
                               '\n'
                               '    egress_policies {\n'
                               '      egress_from {\n'
                               '        identity_type = "ANY_IDENTITY"\n'
                               '      }\n'
                               '      egress_to {\n'
                               '        resources = ["projects/918209384712"]\n'
                               '        operations {\n'
                               '          service_name = "bigquery.googleapis.com"\n'
                               '          method_selectors {\n'
                               '            method = "*"\n'
                               '          }\n'
                               '        }\n'
                               '      }\n'
                               '    }\n'
                               '  }\n'
                               '\n'
                               '  use_explicit_dry_run_spec = true\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored vpc_service_controls.tf"\n'
                               '```',
                               '#### Execution & Exfiltration Interception Simulation\n'
                               'Author a Python simulation script evaluating VPC-SC perimeter policy logic:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_vpcs_eval.py\n"
                               'def evaluate_vpcs(source_project, target_project, service):\n'
                               "    in_perimeter = (source_project == 'projects/108420918237')\n"
                               "    target_in_perimeter = (target_project == 'projects/108420918237')\n"
                               "    allowed_egress_target = (target_project == 'projects/918209384712')\n"
                               '    \n'
                               '    if in_perimeter and not target_in_perimeter:\n'
                               '        if not allowed_egress_target:\n'
                               "            return 403, 'DENIED: Prohibited by VPC Service Controls (Exfiltration "
                               "Block)'\n"
                               "        return 200, 'ALLOWED: Permitted by Scoped Egress Rule'\n"
                               "    return 200, 'ALLOWED: Internal Perimeter Operation'\n"
                               '\n'
                               '# Test unauthorized exfiltration attempt\n'
                               "status, msg = evaluate_vpcs('projects/108420918237', "
                               "'projects/attacker-personal-project', 'storage.googleapis.com')\n"
                               'assert status == 403\n'
                               "print(f'[VPC-SC PASS] Exfiltration Intercepted: {msg}')\n"
                               '\n'
                               '# Test authorized cross-perimeter copy\n'
                               "status, msg = evaluate_vpcs('projects/108420918237', 'projects/918209384712', "
                               "'bigquery.googleapis.com')\n"
                               'assert status == 200\n'
                               "print(f'[VPC-SC PASS] Scoped Egress Rule Matched: {msg}')\n"
                               'EOF\n'
                               'python3 simulate_vpcs_eval.py\n'
                               '```',
                               '#### Resiliency Testing & Unauthorized Copy Chaos Test\n'
                               'Simulate an attacker attempting to copy a sensitive dataset to an unapproved bucket '
                               'and assert block:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_unauthorized_copy.py\n"
                               'from simulate_vpcs_eval import evaluate_vpcs\n'
                               '\n'
                               "status, msg = evaluate_vpcs('projects/108420918237', 'projects/rogue-cloud-bucket', "
                               "'storage.googleapis.com')\n"
                               "assert status == 403, 'Security failure: Unauthorized bucket copy permitted!'\n"
                               "print(f'[CHAOS TEST PASS] VPC-SC strictly prevented data exfiltration: {msg}')\n"
                               'EOF\n'
                               'python3 test_unauthorized_copy.py\n'
                               '```',
                               '#### Telemetry, Observability & VPC-SC Violation Filter\n'
                               'Author a Cloud Logging filter tracking VPC Service Controls violations:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > vpc_sc_violation_filter.txt\n"
                               'protoPayload.metadata.vpcServiceControlsUniqueIdentifier:*\n'
                               'protoPayload.status.code=7\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to vpc_sc_violation_filter.txt"\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform VPC-SC manifest:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_vpcs_manifest.py\n"
                               "with open('vpc_service_controls.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'google_access_context_manager_service_perimeter' in tf\n"
                               "assert 'storage.googleapis.com' in tf\n"
                               "assert 'bigquery.googleapis.com' in tf\n"
                               "assert 'egress_policies' in tf\n"
                               "print('[ASSERT PASS] VPC Service Controls manifest strictly validated.')\n"
                               'EOF\n'
                               'python3 assert_vpcs_manifest.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_vpcs_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 104 Topic 1 test scripts..."\n'
                               'rm -f check_vpcs_specs.py check_vpcs_tools.sh simulate_vpcs_eval.py '
                               'test_unauthorized_copy.py assert_vpcs_manifest.py\n'
                               'echo "[CLEANUP] Retaining production files: vpc_service_controls.tf, '
                               'vpc_sc_violation_filter.txt"\n'
                               'echo "[CLEANUP PASS] VPC Service Controls lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_vpcs_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm exfiltration blocking and scoped '
                                     'cross-perimeter egress rules.',
                     'trouble': 'Ensure Access Context Manager API is enabled in the organization.',
                     'cleanup': 'bash teardown_vpcs_lab.sh',
                     'accept': 'VPC-SC manifest and test suite pass verification with 0 errors.',
                     'file': 'day-104-topic-01-vpc-service-controls.md'}},
            {'key': 'topic-02',
             'title': 'Cloud NGFW and Cloud IDS (intrusion detection)',
             'overview': 'Google Cloud Next Generation Firewall (Cloud NGFW Enterprise) and Cloud IDS (Intrusion '
                         'Detection System) deliver deep packet inspection, Layer 7 Application Control (AppID), and '
                         "advanced threat prevention across Google's distributed software-defined network. Cloud NGFW "
                         'Enterprise incorporates Palo Alto Networks threat intelligence directly into the hypervisor '
                         'fabric, dropping malicious traffic inline before it reaches workloads. Cloud IDS operates '
                         'alongside NGFW by mirroring network traffic to dedicated intrusion detection engines, '
                         'detecting complex threats including malware, spyware, command-and-control (C2) callbacks, '
                         'and zero-day exploits.',
             'preview': 'An attacker establishes a covert command-and-control channel over port 443 disguised as '
                        'HTTPS; Cloud NGFW Enterprise inspects the Layer 7 protocol and drops the connection because '
                        'the protocol signature does not match legitimate TLS.',
             'technical': '### 1. Cloud NGFW Enterprise Architecture\n'
                          '- **Layer 7 AppID:** Identifies applications and protocols regardless of port (e.g. '
                          'detecting SSH running over port 80).\n'
                          '- **Intrusion Prevention Service (IPS):** Deep packet inspection against thousands of Palo '
                          'Alto Networks threat signatures.\n'
                          '- **Security Profile Groups:** Reusable policy containers defining threat prevention rules '
                          'attached to firewall policies.\n'
                          '\n'
                          '### 2. Cloud IDS Architecture\n'
                          '- **Packet Mirroring:** Google Cloud hypervisors mirror packets transparently with zero '
                          'agent overhead and zero latency impact on production traffic.\n'
                          '- **Threat Engine:** Inspects mirrored traffic for malware, spyware, and vulnerability '
                          'exploits.\n'
                          '- **Security Command Center:** Threat findings stream directly to SCC for automated triage '
                          'and incident response.',
             'questions': ['What is the key difference between Cloud NGFW Enterprise IPS and Cloud IDS?',
                           'How does Layer 7 AppID prevent an attacker from bypassing firewall rules by running '
                           'non-standard protocols on port 443?',
                           'Does Cloud IDS packet mirroring introduce latency or throughput degradation to production '
                           'workloads?'],
             'reference': 'https://cloud.google.com/firewall/docs/about-firewall-enterprise',
             'reference_label': 'Google Cloud: Cloud NGFW Enterprise and Cloud IDS threat prevention',
             'scenario': {'symptom': 'An internal compute instance was infected with trojan malware that established '
                                     'persistent command-and-control beacons to an external IP.',
                          'constraints': 'Standard Layer 4 firewall rules permitted outbound port 443; inspection must '
                                         'detect malicious protocol behavior without breaking internal HTTPS.',
                          'evidence': 'Security Command Center finding extract:\n'
                                      '\n'
                                      '```text\n'
                                      'Threat Category: MALWARE_COMMAND_AND_CONTROL\n'
                                      'Source: Cloud IDS\n'
                                      'Evidence: Outbound connection from 10.128.0.8:49182 to 198.51.100.44:443\n'
                                      'Signature: PaloAlto Threat ID 14210 (Cobalt Strike Beacon Traffic Profile)\n'
                                      'Status: DETECTED (Traffic permitted by traditional L4 firewall)\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: Standard L4 firewalls evaluated only IP and port, blindly allowing '
                                      'the malicious beacon because it operated on port 443.',
                          'diagnostic_steps': ['Inspect Cloud IDS threat finding details in Security Command Center.',
                                               'Verify Cloud NGFW Enterprise security profile attachment.',
                                               'Review Packet Mirroring configuration in the target VPC.',
                                               'Inspect Layer 7 protocol inspection settings on the egress firewall '
                                               'rule.'],
                          'root': 'Traditional Layer 4 stateful firewalls lacked deep packet inspection capabilities, '
                                  'permitting malware masquerading as HTTPS.',
                          'fix': 'Deploy Cloud NGFW Enterprise with an Intrusion Prevention Security Profile '
                                 'configured to block known command-and-control signatures inline.',
                          'verify': 'Simulate Cobalt Strike beacon traffic and assert immediate connection termination '
                                    'by Cloud NGFW IPS.',
                          'residual': 'TLS-encrypted traffic requires TLS Decryption (Certificate Manager integration) '
                                      'for full payload inspection.',
                          'diagram': ('Malware initiates outbound C2 beacon on port 443',
                                      'Traditional L4 firewall permits traffic as HTTPS',
                                      'Adversary establishes persistent remote control',
                                      'Deploy Cloud NGFW Enterprise with Layer 7 IPS profile',
                                      'Cobalt Strike signature detected; connection severed inline')},
             'lab': {'name': 'Cloud NGFW Enterprise and Cloud IDS Threat Prevention Architecture',
                     'goal': 'Author a declarative Terraform configuration establishing Cloud NGFW Enterprise Security '
                             'Profiles and IPS rules.',
                     'expected': 'Validated Terraform manifest and Python simulation testing Layer 7 AppID detection '
                                 'and threat signature blocking.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify Network Security API enablement and firewall administrative permissions.',
                     'steps': ['#### Pre-Flight Cloud NGFW & IDS Discovery\n'
                               'Catalog Cloud NGFW Enterprise threat inspection features:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_ngfw_specs.py\n"
                               'specs = {\n'
                               "    'threat_prevention': 'Inline deep packet inspection (Palo Alto IPS signatures)',\n"
                               "    'app_id': 'Layer 7 application identification independent of port',\n"
                               "    'packet_mirroring': 'Transparent zero-latency packet mirroring for Cloud IDS',\n"
                               "    'scc_integration': 'Automated threat finding ingestion into Security Command "
                               "Center'\n"
                               '}\n'
                               "print('[PREFLIGHT] Cloud NGFW Enterprise Technical Specifications:')\n"
                               'for k, v in specs.items():\n'
                               "    print(f'  • {k:20s}: {v}')\n"
                               'EOF\n'
                               'python3 check_ngfw_specs.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and syntax linters:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_ngfw_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_ngfw_tools.sh\n'
                               '```',
                               '#### Core Implementation: Cloud NGFW Security Profile Manifest\n'
                               'Author a declarative Terraform configuration establishing an IPS Security Profile and '
                               'Group:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > cloud_ngfw_enterprise.tf\n"
                               'resource "google_network_security_security_profile" "ips_profile" {\n'
                               '  name        = "enterprise-threat-ips-profile"\n'
                               '  parent      = "organizations/108420918237"\n'
                               '  location    = "global"\n'
                               '  type        = "THREAT_PREVENTION"\n'
                               '  description = "Inline intrusion prevention dropping malware and C2 traffic"\n'
                               '\n'
                               '  threat_prevention_profile {\n'
                               '    severity_overrides {\n'
                               '      action   = "ALERT"\n'
                               '      severity = "LOW"\n'
                               '    }\n'
                               '    severity_overrides {\n'
                               '      action   = "DENY"\n'
                               '      severity = "CRITICAL"\n'
                               '    }\n'
                               '    severity_overrides {\n'
                               '      action   = "DENY"\n'
                               '      severity = "HIGH"\n'
                               '    }\n'
                               '  }\n'
                               '}\n'
                               '\n'
                               'resource "google_network_security_security_profile_group" "sec_group" {\n'
                               '  name                      = "enterprise-sec-group"\n'
                               '  parent                    = "organizations/108420918237"\n'
                               '  location                  = "global"\n'
                               '  threat_prevention_profile = google_network_security_security_profile.ips_profile.id\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored cloud_ngfw_enterprise.tf"\n'
                               '```',
                               '#### Execution & Layer 7 Threat Simulation Engine\n'
                               'Author a Python simulation script evaluating Layer 7 AppID and threat signature '
                               'detection:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_ngfw_ips.py\n"
                               'def inspect_packet(port, app_protocol, threat_signature_id=None):\n'
                               '    # Layer 7 AppID verification\n'
                               "    if port == 443 and app_protocol != 'TLS':\n"
                               "        return 'DROPPED_BY_APP_ID (Protocol Mismatch on Port 443)'\n"
                               '    # Threat prevention IPS check\n'
                               '    if threat_signature_id in [14210, 91823]:\n'
                               "        return 'DROPPED_BY_IPS (Critical Threat Signature Matched)'\n"
                               "    return 'ALLOWED (Clean Protocol & Payload)'\n"
                               '\n'
                               '# Test protocol masquerading\n'
                               "res1 = inspect_packet(443, 'NON_TLS_CUSTOM_SHELL')\n"
                               "assert 'DROPPED_BY_APP_ID' in res1\n"
                               "print(f'[NGFW PASS] AppID Blocked Protocol Masquerading: {res1}')\n"
                               '\n'
                               '# Test C2 beacon signature\n'
                               "res2 = inspect_packet(443, 'TLS', threat_signature_id=14210)\n"
                               "assert 'DROPPED_BY_IPS' in res2\n"
                               "print(f'[NGFW PASS] IPS Blocked Cobalt Strike Signature: {res2}')\n"
                               'EOF\n'
                               'python3 simulate_ngfw_ips.py\n'
                               '```',
                               '#### Resiliency Testing & Evasive Protocol Chaos Test\n'
                               'Simulate an evasive tool attempting to tunnel SSH through port 443 and assert block:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_evasive_protocol.py\n"
                               'from simulate_ngfw_ips import inspect_packet\n'
                               '\n'
                               "res = inspect_packet(443, 'SSH')\n"
                               "assert 'DROPPED_BY_APP_ID' in res, 'Security failure: SSH on port 443 permitted!'\n"
                               "print(f'[CHAOS TEST PASS] Layer 7 AppID intercepted evasive protocol tunnel: {res}')\n"
                               'EOF\n'
                               'python3 test_evasive_protocol.py\n'
                               '```',
                               '#### Telemetry, Observability & Cloud IDS Threat Filter\n'
                               'Author a Cloud Logging filter tracking Cloud IDS threat findings:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > ids_threat_filter.txt\n"
                               'resource.type="ids.googleapis.com/Endpoint"\n'
                               'jsonPayload.alert_severity=~"(CRITICAL|HIGH)"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to ids_threat_filter.txt"\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform Cloud NGFW manifest:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_ngfw_manifest.py\n"
                               "with open('cloud_ngfw_enterprise.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'google_network_security_security_profile' in tf\n"
                               "assert 'google_network_security_security_profile_group' in tf\n"
                               "assert 'THREAT_PREVENTION' in tf\n"
                               'assert \'action   = "DENY"\' in tf\n'
                               "print('[ASSERT PASS] Cloud NGFW Enterprise manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_ngfw_manifest.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_ngfw_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 104 Topic 2 test scripts..."\n'
                               'rm -f check_ngfw_specs.py check_ngfw_tools.sh simulate_ngfw_ips.py '
                               'test_evasive_protocol.py assert_ngfw_manifest.py\n'
                               'echo "[CLEANUP] Retaining production files: cloud_ngfw_enterprise.tf, '
                               'ids_threat_filter.txt"\n'
                               'echo "[CLEANUP PASS] Cloud NGFW lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_ngfw_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm Layer 7 AppID protocol '
                                     'enforcement and critical threat signature blocking.',
                     'trouble': 'Ensure organization permissions are available for security profile creation under '
                                'organizations/[ORG_ID].',
                     'cleanup': 'bash teardown_ngfw_lab.sh',
                     'accept': 'Cloud NGFW manifest and test suite pass verification with 0 errors.',
                     'file': 'day-104-topic-02-cloud-ngfw-ids.md'}},
            {'key': 'topic-03',
             'title': 'Secure Web Proxy',
             'overview': 'Google Cloud Secure Web Proxy (SWP) provides scalable, cloud-first outbound web (HTTP/HTTPS) '
                         "inspection and filtering for private VPC workloads. Built directly on Google's global "
                         'infrastructure without requiring third-party proxy virtual appliances or complex routing '
                         'meshes, SWP enforces granular egress security policies based on fully qualified domain names '
                         '(FQDNs), URL paths, HTTP methods, and source identities (Service Accounts and Secure Tags). '
                         'Operating as an explicit or transparent forward proxy, it integrates with Certificate '
                         'Manager to perform TLS inspection and SNI filtering, guaranteeing that workloads can only '
                         'reach pre-approved external domains.',
             'preview': 'An application container compromised by an attacker attempts to download an exploitation '
                        'script from an unauthorized external domain; Secure Web Proxy intercepts the outbound HTTP '
                        'request and drops it because the destination FQDN is not in the approved whitelist.',
             'technical': '### 1. Secure Web Proxy Architecture\n'
                          '- **Gateway Resource:** Managed proxy gateway deployed in a target VPC subnet with an '
                          'allocated internal IP.\n'
                          '- **Security Policy:** Collection of rules evaluated by priority matching source identities '
                          'and destination URL lists.\n'
                          '- **URL Lists:** Declarative lists of allowed FQDNs and paths with wildcard support (e.g. '
                          '`*.debian.org`, `packages.cloud.google.com`).\n'
                          '\n'
                          '### 2. TLS Inspection & Identity Scoping\n'
                          '- **TLS Inspection Policy:** Integrates with Cloud Certificate Authority Service (CAS) to '
                          'perform full SSL decryption and deep URL path inspection.\n'
                          '- **Identity Scoping:** Rules can restrict access by source Service Account '
                          '(`source_service_accounts`) or Resource Manager Secure Tags.',
             'questions': ['How does Secure Web Proxy simplify outbound egress security compared to legacy forward '
                           'proxy appliances?',
                           'What is the difference between SNI-based domain filtering and full TLS inspection in '
                           'Secure Web Proxy?',
                           'How can Secure Web Proxy rules be scoped to allow outbound access exclusively to specific '
                           'internal service accounts?'],
             'reference': 'https://cloud.google.com/secure-web-proxy/docs/overview',
             'reference_label': 'Google Cloud Secure Web Proxy: Outbound egress filtering and TLS inspection',
             'scenario': {'symptom': 'A compromised GKE workload attempted to download an external cryptomining binary '
                                     'from an unauthorized paste site.',
                          'constraints': 'Workloads require outbound access to approved package repositories (e.g. '
                                         'debian.org, github.com), but arbitrary internet access must be blocked.',
                          'evidence': 'Secure Web Proxy access audit log:\n'
                                      '\n'
                                      '```json\n'
                                      '{\n'
                                      '  "protoPayload": {\n'
                                      '    "serviceName": "networksecurity.googleapis.com",\n'
                                      '    "methodName": "ProxyAccessLog",\n'
                                      '    "requestMetadata": {"callerIp": "10.128.10.14", "destinationUrl": '
                                      '"http://pastebin.com/raw/exploit918"},\n'
                                      '    "status": {"code": 7, "message": "DENIED_BY_POLICY (FQDN not in '
                                      'allowed_url_list)"}\n'
                                      '  }\n'
                                      '}\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: Secure Web Proxy intercepted the request, verified the FQDN against '
                                      'the URL whitelist, and terminated the connection.',
                          'diagnostic_steps': ['Inspect Secure Web Proxy policy rules using gcloud network-security '
                                               'gateway-security-policies describe.',
                                               'Review URL lists associated with the gateway policy.',
                                               'Verify proxy configuration settings inside the GKE pod environment '
                                               'variables (http_proxy, https_proxy).',
                                               'Check Cloud Logging for proxy deny events.'],
                          'root': 'Workload attempted to access an unapproved external destination not included in the '
                                  'corporate egress whitelist.',
                          'fix': 'Maintain a strict FQDN URL list allowing only necessary package repositories and '
                                 'configure all private workloads to route egress through Secure Web Proxy.',
                          'verify': 'Send test HTTP request to allowed domain (e.g. debian.org) and verify success; '
                                    'send request to arbitrary domain and assert HTTP 403 Forbidden.',
                          'residual': 'Non-HTTP/HTTPS protocols (e.g. raw TCP, UDP) cannot be inspected by Secure Web '
                                      'Proxy and must be restricted via firewall egress rules.',
                          'diagram': ('Compromised pod attempts to download exploit from paste site',
                                      'Outbound request routed through Secure Web Proxy',
                                      'SWP checks destination FQDN against approved URL list',
                                      'Destination paste site rejected; connection severed with HTTP 403',
                                      'Approved repositories remain accessible; exfiltration prevented')},
             'lab': {'name': 'Secure Web Proxy (SWP) Outbound Egress Architecture',
                     'goal': 'Author a declarative Terraform configuration establishing a Secure Web Proxy gateway, '
                             'URL list, and security policy.',
                     'expected': 'Validated Terraform manifest and Python simulation testing FQDN whitelisting and '
                                 'unauthorized URL rejection.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify Network Security and Network Services API readiness.',
                     'steps': ['#### Pre-Flight Secure Web Proxy Discovery\n'
                               'Catalog Secure Web Proxy components and FQDN whitelist requirements:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_swp_specs.py\n"
                               'specs = {\n'
                               "    'gateway_type': 'SECURE_WEB_GATEWAY (Explicit Forward Proxy)',\n"
                               "    'ports': '[443, 80]',\n"
                               "    'approved_fqdns': ['deb.debian.org', '*.googleapis.com', 'github.com'],\n"
                               "    'default_action': 'DENY (Drop all unapproved FQDNs)'\n"
                               '}\n'
                               "print('[PREFLIGHT] Secure Web Proxy Technical Specifications:')\n"
                               'for k, v in specs.items():\n'
                               "    print(f'  • {k:18s}: {v}')\n"
                               'EOF\n'
                               'python3 check_swp_specs.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and syntax linters:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_swp_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_swp_tools.sh\n'
                               '```',
                               '#### Core Implementation: Secure Web Proxy Terraform Manifest\n'
                               'Author a declarative Terraform configuration establishing the URL list, policy, and '
                               'gateway:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > secure_web_proxy.tf\n"
                               'resource "google_network_security_url_list" "approved_repos" {\n'
                               '  name        = "approved-package-repos"\n'
                               '  project     = "prod-egress-sec"\n'
                               '  location    = "us-central1"\n'
                               '  values      = [\n'
                               '    "deb.debian.org/*",\n'
                               '    "*.googleapis.com/*",\n'
                               '    "github.com/*"\n'
                               '  ]\n'
                               '}\n'
                               '\n'
                               'resource "google_network_security_gateway_security_policy" "swp_policy" {\n'
                               '  name        = "egress-gateway-policy"\n'
                               '  project     = "prod-egress-sec"\n'
                               '  location    = "us-central1"\n'
                               '  description = "Egress policy allowing strictly approved package repositories"\n'
                               '}\n'
                               '\n'
                               'resource "google_network_security_gateway_security_policy_rule" "allow_approved_rule" '
                               '{\n'
                               '  name                    = "allow-approved-repos-rule"\n'
                               '  project                 = "prod-egress-sec"\n'
                               '  location                = "us-central1"\n'
                               '  gateway_security_policy = '
                               'google_network_security_gateway_security_policy.swp_policy.name\n'
                               '  priority                = 1000\n'
                               '  enabled                 = true\n'
                               '  basic_profile           = "ALLOW"\n'
                               '  application_matcher     = "inUrlList(host(), '
                               '\'${google_network_security_url_list.approved_repos.id}\')"\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored secure_web_proxy.tf"\n'
                               '```',
                               '#### Execution & FQDN Filtering Simulation Engine\n'
                               'Author a Python simulation script evaluating FQDN matching against the proxy URL '
                               'list:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_swp_filter.py\n"
                               'import fnmatch\n'
                               '\n'
                               'def evaluate_proxy_egress(destination_url):\n'
                               "    whitelist = ['deb.debian.org/*', '*.googleapis.com/*', 'github.com/*']\n"
                               '    for pattern in whitelist:\n'
                               '        if fnmatch.fnmatch(destination_url, pattern):\n'
                               "            return 200, 'ALLOWED: Matched approved URL list'\n"
                               "    return 403, 'DENIED_BY_POLICY: Unapproved FQDN'\n"
                               '\n'
                               '# Test approved repo\n'
                               "status, msg = evaluate_proxy_egress('deb.debian.org/debian/pool/main')\n"
                               'assert status == 200\n'
                               "print(f'[SWP PASS] Approved Repository: {msg}')\n"
                               '\n'
                               '# Test unapproved pastebin\n'
                               "status, msg = evaluate_proxy_egress('pastebin.com/raw/exploit')\n"
                               'assert status == 403\n'
                               "print(f'[SWP PASS] Unapproved Destination Dropped: {msg}')\n"
                               'EOF\n'
                               'python3 simulate_swp_filter.py\n'
                               '```',
                               '#### Resiliency Testing & Wildcard Bypass Chaos Test\n'
                               'Simulate an attacker attempting to access an unauthorized subdomain and assert '
                               'rejection:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_wildcard_bypass.py\n"
                               'from simulate_swp_filter import evaluate_proxy_egress\n'
                               '\n'
                               "status, msg = evaluate_proxy_egress('evil-debian.org/malware')\n"
                               "assert status == 403, 'Security failure: Rogue domain matched wildcard!'\n"
                               "print(f'[CHAOS TEST PASS] SWP strictly rejected rogue domain: {msg}')\n"
                               'EOF\n'
                               'python3 test_wildcard_bypass.py\n'
                               '```',
                               '#### Telemetry, Observability & Proxy Audit Filter\n'
                               'Author a Cloud Logging filter tracking Secure Web Proxy access and block events:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > swp_log_filter.txt\n"
                               'resource.type="networkservices.googleapis.com/Gateway"\n'
                               'jsonPayload.action="DENIED"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to swp_log_filter.txt"\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform Secure Web Proxy manifest:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_swp_manifest.py\n"
                               "with open('secure_web_proxy.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'google_network_security_url_list' in tf\n"
                               "assert 'google_network_security_gateway_security_policy' in tf\n"
                               "assert 'deb.debian.org/*' in tf\n"
                               "assert 'inUrlList' in tf\n"
                               "print('[ASSERT PASS] Secure Web Proxy manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_swp_manifest.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_swp_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 104 Topic 3 test scripts..."\n'
                               'rm -f check_swp_specs.py check_swp_tools.sh simulate_swp_filter.py '
                               'test_wildcard_bypass.py assert_swp_manifest.py\n'
                               'echo "[CLEANUP] Retaining production files: secure_web_proxy.tf, swp_log_filter.txt"\n'
                               'echo "[CLEANUP PASS] Secure Web Proxy lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_swp_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm FQDN whitelisting and rejection '
                                     'of unapproved external destinations.',
                     'trouble': 'Ensure that the gateway security policy is in the same region as the gateway and URL '
                                'list.',
                     'cleanup': 'bash teardown_swp_lab.sh',
                     'accept': 'Secure Web Proxy manifest and test suite pass verification with 0 errors.',
                     'file': 'day-104-topic-03-secure-web-proxy.md'}}]}
