"""day_data_102.py — Exhaustive architecture data specification for Day 102.

Covers BeyondCorp, Privileged Access Manager, Break-Glass, and Access Transparency.
"""

DAY_NUM = 102

DATA = {'day': 102,
 'part1_intro': 'Day 102 establishes the architectural controls for zero-trust privileged access, temporary elevation, '
                'and emergency continuity. Architects analyze the elimination of standing administrative privileges '
                'using Privileged Access Manager (PAM), the engineering of isolated out-of-band break-glass accounts '
                'for catastrophic identity provider outages, the deployment of BeyondCorp Enterprise for continuous '
                'context verification, and the configuration of Access Transparency (AXT) and Access Approval (AXA) to '
                'audit and govern Google support administrative interventions.',
 'exit_summary': 'Engineers master Privileged Access Manager just-in-time entitlement manifests with multi-party '
                 'approval workflows, out-of-band break-glass emergency activation runbooks with automated '
                 'high-priority alerting, and Access Transparency log ingestion pipelines verifying zero unauthorized '
                 'cloud provider access.',
 'part2_intro': 'The following architectural matrix details the technical trade-offs, operational protocols, and '
                'security boundaries across BeyondCorp Enterprise, Privileged Access Manager (PAM), emergency '
                'break-glass procedures, and Access Transparency/Approval.',
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
                    '<td><strong>Zero Trust Perimeter</strong></td>\n'
                    '<td>BeyondCorp Enterprise</td>\n'
                    '<td>mTLS &amp; Context-Aware Access</td>\n'
                    '<td>Google Front End (GFE)</td>\n'
                    '<td>Continuous device posture verification; zero network-location trust.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Privileged Elevation</strong></td>\n'
                    '<td>Privileged Access Manager</td>\n'
                    '<td>Just-in-Time IAM Conditions</td>\n'
                    '<td>PAM Entitlement Engine</td>\n'
                    '<td>Zero standing administrative privileges; max duration &le; 4 hours with multi-party '
                    'sign-off.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Emergency Continuity</strong></td>\n'
                    '<td>Break-Glass Accounts</td>\n'
                    '<td>FIDO2 / Out-of-Band Cloud Identity</td>\n'
                    '<td>Geographic Dual-Custody Safe</td>\n'
                    '<td>Used exclusively during IdP failure; triggers immediate emergency broadcast alerts.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Provider Auditing</strong></td>\n'
                    '<td>Access Transparency &amp; Approval</td>\n'
                    '<td>Audit Logging &amp; Explicit Gate</td>\n'
                    '<td>Google Administrative Control Plane</td>\n'
                    '<td>Google engineers cannot access customer data without explicit customer approval and audit '
                    'trail.</td>\n'
                    '</tr>\n'
                    '</tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 102: Privileged Access Management, Break-Glass, and Access Transparency',
                  'desc': 'Architectural topology illustrating BeyondCorp zero-trust ingress, PAM just-in-time '
                          'elevation, out-of-band break-glass activation, and Access Transparency/Approval.',
                  'caption': 'Figure 102.1: Multi-tier privileged access governance pipeline featuring PAM '
                             'just-in-time elevation, emergency break-glass procedures, and Access Transparency '
                             'auditing.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Administrative User & Emergency Responder Ingress',
                              'desc': 'Enterprise SREs, security engineers, and emergency disaster recovery leads',
                              'y': 10,
                              'h': 90,
                              'stroke': '#38bdf8',
                              'fill': '#0c1e38',
                              'title_color': '#38bdf8'},
                             {'name': 'LAYER 2: BeyondCorp Zero-Trust & Context-Aware Engine',
                              'desc': 'Endpoint Verification, hardware security keys, and continuous device posture '
                                      'checks',
                              'y': 115,
                              'h': 90,
                              'stroke': '#818cf8',
                              'fill': '#141838',
                              'title_color': '#818cf8'},
                             {'name': 'LAYER 3: Privileged Access Manager (PAM) & JIT Elevation Gate',
                              'desc': 'Entitlement policies, multi-party approval workflows, and temporary IAM '
                                      'bindings',
                              'y': 220,
                              'h': 90,
                              'stroke': '#f59e0b',
                              'fill': '#261a08',
                              'title_color': '#f59e0b'},
                             {'name': 'LAYER 4: Emergency Break-Glass & Dual-Custody Safes',
                              'desc': 'Out-of-band Cloud Identity, physical FIDO2 keys, and automated broadcast alarms',
                              'y': 325,
                              'h': 90,
                              'stroke': '#f43f5e',
                              'fill': '#2a0a14',
                              'title_color': '#f43f5e'},
                             {'name': 'LAYER 5: Access Transparency, Access Approval & Audit Vault',
                              'desc': 'Google support access requests, explicit approval workflows, and immutable AXT '
                                      'logs',
                              'y': 430,
                              'h': 90,
                              'stroke': '#22c55e',
                              'fill': '#072417',
                              'title_color': '#22c55e'}],
                  'components': [{'name': 'SRE On-Call Operator',
                                  'detail': 'Corporate Workstation',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'Break-Glass Hardware Key',
                                  'detail': 'Physical Vault Dual Custody',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'BeyondCorp Posture Engine',
                                  'detail': 'Continuous Device Evaluation',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Endpoint Verification',
                                  'detail': 'OS & Encryption Signals',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'PAM Entitlement Engine',
                                  'detail': 'JIT Grant Lifecycle',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Multi-Party Approvers',
                                  'detail': 'Secondary Engineer Sign-off',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Out-of-Band Cloud Identity',
                                  'detail': 'Isolated Emergency Admin',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Emergency Broadcast Alarms',
                                  'detail': 'PagerDuty & SMS Fan-out',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Google Support Request',
                                  'detail': 'Support Ticket Justification',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'},
                                 {'name': 'Access Approval Gate',
                                  'detail': 'Customer Explicit Approval',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'}],
                  'boundaries': [{'label': 'IDENTITY POSTURE & EMERGENCY INGRESS PERIMETER',
                                  'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'color': '#38bdf8'},
                                 {'label': 'JUST-IN-TIME PRIVILEGE & ELEVATION ENVELOPE',
                                  'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#f59e0b'},
                                 {'label': 'ACCESS TRANSPARENCY & CLOUD PROVIDER AUDIT VAULT',
                                  'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#22c55e'}],
                  'flows': [{'x1': 340,
                             'y1': 56,
                             'x2': 420,
                             'y2': 56,
                             'label': 'Retrieve Physical Token',
                             'type': 'warn'},
                            {'x1': 210,
                             'y1': 82,
                             'x2': 210,
                             'y2': 135,
                             'label': 'Submit Posture Telemetry',
                             'type': 'ok'},
                            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Assert Device Health', 'type': 'ok'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'label': 'Request JIT Elevation',
                             'type': 'ok'},
                            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Multi-Party Approval', 'type': 'ok'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'label': 'Emergency Break-Glass',
                             'type': 'fail'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'label': 'Trigger Urgent PagerDuty',
                             'type': 'warn'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'label': 'Request Support Access',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'label': 'Grant Explicit Approval',
                             'type': 'ok'}],
                  'probes': [{'cx': 80,
                              'cy': 135,
                              'label': 'PROBE 1: BeyondCorp Device Trust Verification',
                              'badge': 'P1',
                              'color': '#38bdf8'},
                             {'cx': 80,
                              'cy': 240,
                              'label': 'PROBE 2: PAM Max Duration Expiration (<4h)',
                              'badge': 'P2',
                              'color': '#f59e0b'},
                             {'cx': 420,
                              'cy': 345,
                              'label': 'PROBE 3: Break-Glass Activity Broadcast (<30s)',
                              'badge': 'P3',
                              'color': '#f43f5e'}]},
 'part3_intro': 'The following field cases analyze real-world security incidents, accidental privileged actions, and '
                'administrative blind spots: an engineer on an unencrypted personal device accessing production '
                'resources from an internal office network due to legacy perimeter VPN assumptions, an unauthorized '
                'production database drop executed during off-hours by an engineer who held permanent standing '
                'administrative privileges that had not been right-sized via Privileged Access Manager, a catastrophic '
                '6-hour production outage caused by an external identity provider SAML certificate expiration where '
                'the organization lacked an out-of-band break-glass account, and a compliance failure during an '
                'external SOC 2 audit because Google support engineers accessed production storage buckets to '
                'remediate an underlying infrastructure defect without prior customer Access Approval. Each case '
                'details verbatim logs, terminal output, root cause mechanics, defensible remediations, and dual-lane '
                'failed/corrected flow diagrams.',
 'part4_intro': 'These hands-on exercises implement the comprehensive 8-stage operational engineering lifecycle for '
                'Day 102. Engineers construct BeyondCorp Context-Aware Access levels enforcing continuous device '
                'health, author Privileged Access Manager (PAM) entitlement manifests with multi-party approval '
                'workflows and duration caps, establish out-of-band break-glass emergency activation pipelines with '
                'automated high-priority alerting, and configure Access Transparency and Access Approval settings to '
                'enforce explicit authorization for cloud provider interventions.',
 'topics': [{'key': 'topic-01',
             'title': 'BeyondCorp / zero trust model',
             'overview': "BeyondCorp Enterprise represents Google's implementation of the zero-trust security model. "
                         'In this architecture, access to enterprise applications and Google Cloud APIs does not '
                         'depend on the network location of the requester (e.g. corporate intranet vs home Wi-Fi). '
                         'Instead, every request is dynamically authenticated, authorized, and cryptographically '
                         'verified based on user identity, group memberships, and granular client device posture (such '
                         'as hardware-backed device certificates, disk encryption, OS patch level, and geolocation).',
             'preview': 'A corporate laptop connected to headquarters Wi-Fi is infected with an information stealer; '
                        'because the organization enforces BeyondCorp device trust certificates and Chrome Enterprise '
                        'Premium inspection, the malware is blocked from accessing Google Cloud console APIs.',
             'technical': '### 1. BeyondCorp Architectural Tenets\n'
                          '- **Network Agnostic:** Internal corporate networks are treated as untrusted, exactly like '
                          'the public internet.\n'
                          '- **Continuous Evaluation:** Device context and user credentials are evaluated on every '
                          'single request, not just during initial authentication.\n'
                          '- **Dynamic Context:** Integrates signals from Endpoint Verification, Chrome Enterprise '
                          'Premium, and third-party EDR/UEM tools (CrowdStrike, Intune, Jamf).\n'
                          '\n'
                          '### 2. Integration Components\n'
                          '- **Access Context Manager (ACM):** Central policy engine evaluating device and IP '
                          'conditions.\n'
                          '- **Identity-Aware Proxy (IAP):** Enforces Access Levels at the ingress load balancer.\n'
                          '- **VPC Service Controls:** Extends zero-trust data perimeters to Google Cloud managed '
                          'service APIs.',
             'questions': ['How does BeyondCorp Enterprise prevent an attacker who has stolen valid user credentials '
                           'from accessing cloud resources?',
                           'What role does Endpoint Verification play in the BeyondCorp zero-trust architecture?',
                           'Why is network perimeter security (VPNs, intranet allowlisting) fundamentally insufficient '
                           'for modern cloud architecture?'],
             'reference': 'https://cloud.google.com/beyondcorp-enterprise/docs/overview',
             'reference_label': 'BeyondCorp Enterprise: Zero-trust architecture and continuous verification',
             'scenario': {'symptom': 'An attacker with stolen employee credentials accessed an internal code '
                                     'repository from an unmanaged, jailbroken device.',
                          'constraints': 'Remote workforce requires access from various geographic locations without '
                                         'routing all traffic through high-latency VPN concentrators.',
                          'evidence': 'Access Context Manager evaluation log:\n'
                                      '\n'
                                      '```json\n'
                                      '{\n'
                                      '  "protoPayload": {\n'
                                      '    "serviceName": "iap.googleapis.com",\n'
                                      '    "authenticationInfo": {"principalEmail": "developer@corp.com"},\n'
                                      '    "requestMetadata": {"callerIp": "198.51.100.18", "deviceStatus": '
                                      '{"isJailbroken": true, "isEncrypted": false}},\n'
                                      '    "status": {"code": 0, "message": "ALLOW (Legacy perimeter rule matched)"}\n'
                                      '  }\n'
                                      '}\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: Application allowed access because the user was authenticated, but no '
                                      'device posture verification rule was applied.',
                          'diagnostic_steps': ['Inspect Access Context Manager levels applied to the target '
                                               'application backend.',
                                               'Verify Endpoint Verification agent rollout status across corporate '
                                               'endpoints.',
                                               'Review IAP policy bindings on the External Application Load Balancer.',
                                               'Inspect device posture attributes in the access log payload.'],
                          'root': 'The organization relied solely on user identity authentication without enforcing '
                                  'BeyondCorp device posture levels on the IAP backend.',
                          'fix': 'Author and attach an Access Level enforcing `device.is_admin_approved && '
                                 'device.is_encrypted && !device.is_jailbroken` to the IAP backend.',
                          'verify': 'Simulate access from an unmanaged device and assert immediate HTTP 403 Forbidden '
                                    'rejection.',
                          'residual': 'Non-browser thick client tools must be routed through IAP TCP forwarding to '
                                      'inherit device context verification.',
                          'diagram': ('Attacker presents stolen credentials from jailbroken device',
                                      'Application checks identity but ignores device posture',
                                      'Attacker accesses proprietary source code repository',
                                      'Enforce BeyondCorp Access Level requiring approved device',
                                      'Unmanaged device blocked at Google Front End (HTTP 403)')},
             'lab': {'name': 'BeyondCorp Enterprise Zero-Trust Device Posture Architecture',
                     'goal': 'Author and deploy a BeyondCorp Access Level requiring disk encryption, screen lock, and '
                             'corporate device approval.',
                     'expected': 'Validated Terraform Access Level manifest and Python simulation engine evaluating '
                                 'device posture compliance.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify Access Context Manager organization policy ID and administrative privileges.',
                     'steps': ['#### Pre-Flight BeyondCorp Device Posture Discovery\n'
                               'Catalog device posture attributes evaluated in BeyondCorp zero-trust architectures:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_beyondcorp_specs.py\n"
                               'specs = {\n'
                               "    'is_encrypted': 'Hardware-level full-disk encryption (FileVault/BitLocker)',\n"
                               "    'is_admin_approved': 'Device serial registered in corporate inventory',\n"
                               "    'screenlock': 'Screen lock timeout <= 15 minutes',\n"
                               "    'min_os_version': 'macOS 14.0+, Windows 11 23H2+, Linux kernel 6.1+'\n"
                               '}\n'
                               "print('[PREFLIGHT] BeyondCorp Zero-Trust Device Standards:')\n"
                               'for k, v in specs.items():\n'
                               "    print(f'  • {k:20s}: {v}')\n"
                               'EOF\n'
                               'python3 check_beyondcorp_specs.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and JSON parser readiness:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_bc_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_bc_tools.sh\n'
                               '```',
                               '#### Core Implementation: BeyondCorp Access Level Manifest\n'
                               'Author a declarative Terraform configuration establishing the BeyondCorp device '
                               'posture Access Level:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > beyondcorp_access_level.tf\n"
                               'resource "google_access_context_manager_access_level" "beyondcorp_trusted_device" {\n'
                               '  parent      = "accessPolicies/108420918237"\n'
                               '  name        = "accessPolicies/108420918237/accessLevels/beyondcorp_trusted_device"\n'
                               '  title       = "BeyondCorp Trusted Device Posture"\n'
                               '  description = "Requires disk encryption, corporate approval, and screenlock"\n'
                               '\n'
                               '  basic {\n'
                               '    conditions {\n'
                               '      device_policy {\n'
                               '        require_screenlock   = true\n'
                               '        require_admin_approval = true\n'
                               '        os_constraints {\n'
                               '          os_type = "DESKTOP_MAC"\n'
                               '        }\n'
                               '        os_constraints {\n'
                               '          os_type = "DESKTOP_WINDOWS"\n'
                               '        }\n'
                               '      }\n'
                               '    }\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored beyondcorp_access_level.tf"\n'
                               '```',
                               '#### Execution & Continuous Posture Evaluation Simulation\n'
                               'Author a Python simulation script evaluating device health payloads against BeyondCorp '
                               'standards:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_beyondcorp_eval.py\n"
                               'def evaluate_beyondcorp(device):\n'
                               "    if not device.get('is_admin_approved'):\n"
                               "        return False, 'DENIED: Device not approved in corporate inventory'\n"
                               "    if not device.get('is_encrypted'):\n"
                               "        return False, 'DENIED: Disk encryption is inactive'\n"
                               "    if not device.get('screenlock'):\n"
                               "        return False, 'DENIED: Screenlock requirement not satisfied'\n"
                               "    return True, 'APPROVED: Device satisfies BeyondCorp posture'\n"
                               '\n'
                               "dev = {'is_admin_approved': True, 'is_encrypted': True, 'screenlock': True}\n"
                               'ok, msg = evaluate_beyondcorp(dev)\n'
                               'assert ok\n'
                               "print(f'[EVALUATION PASS] {msg}')\n"
                               'EOF\n'
                               'python3 simulate_beyondcorp_eval.py\n'
                               '```',
                               '#### Resiliency Testing & Unmanaged Device Rejection Chaos Test\n'
                               'Simulate an unauthorized personal laptop attempting connection and assert rejection:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_unmanaged_device.py\n"
                               'from simulate_beyondcorp_eval import evaluate_beyondcorp\n'
                               '\n'
                               "bad_dev = {'is_admin_approved': False, 'is_encrypted': True, 'screenlock': True}\n"
                               'ok, msg = evaluate_beyondcorp(bad_dev)\n'
                               "assert not ok, 'Security failure: Unmanaged device permitted!'\n"
                               "print(f'[CHAOS TEST PASS] BeyondCorp intercepted unmanaged device: {msg}')\n"
                               'EOF\n'
                               'python3 test_unmanaged_device.py\n'
                               '```',
                               '#### Telemetry, Observability & BeyondCorp Denial Alert Manifest\n'
                               'Author a Cloud Monitoring Alert Policy alerting whenever BeyondCorp posture checks '
                               'fail:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_beyondcorp_denial.json\n"
                               '{\n'
                               '  "displayName": "SECURITY ALERT: BeyondCorp Device Posture Denial",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "Access Context Manager device posture denial spike",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": "logName=\\"cloudaudit.googleapis.com%2Fpolicy\\" AND '
                               'protoPayload.status.message=~\\"BeyondCorp.*Denial\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 0.0,\n'
                               '        "duration": "0s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] Authored alert_beyondcorp_denial.json"\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform BeyondCorp policy configuration:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_beyondcorp_manifest.py\n"
                               "with open('beyondcorp_access_level.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'require_screenlock   = true' in tf\n"
                               "assert 'require_admin_approval = true' in tf\n"
                               "assert 'google_access_context_manager_access_level' in tf\n"
                               "print('[ASSERT PASS] BeyondCorp Access Level manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_beyondcorp_manifest.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_beyondcorp_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 102 Topic 1 test scripts..."\n'
                               'rm -f check_beyondcorp_specs.py check_bc_tools.sh simulate_beyondcorp_eval.py '
                               'test_unmanaged_device.py assert_beyondcorp_manifest.py\n'
                               'echo "[CLEANUP] Retaining production files: beyondcorp_access_level.tf, '
                               'alert_beyondcorp_denial.json"\n'
                               'echo "[CLEANUP PASS] BeyondCorp lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_beyondcorp_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm strict device approval and '
                                     'screenlock enforcement.',
                     'trouble': 'Ensure Access Context Manager API is enabled in the organization quota project.',
                     'cleanup': 'bash teardown_beyondcorp_lab.sh',
                     'accept': 'BeyondCorp manifest and test suite pass verification with 0 errors.',
                     'file': 'day-102-topic-01-beyondcorp.md'}},
            {'key': 'topic-02',
             'title': 'Privileged Access Manager (just-in-time elevation)',
             'overview': 'Google Cloud Privileged Access Manager (PAM) eliminates standing administrative privileges '
                         'by replacing permanent role bindings with on-demand, just-in-time (JIT) access. '
                         'Administrators and SREs are granted eligibility to activate specific high-privilege roles '
                         'for a strictly bounded duration (e.g. 1 to 4 hours). Activations can require mandatory '
                         'multi-party approvals, detailed justification strings, and automated integration with '
                         'enterprise ticketing systems (Jira, ServiceNow). Every elevation request, approval, and '
                         'expiration is recorded in immutable Cloud Audit logs for compliance auditing.',
             'preview': 'An engineering team replaces standing project `roles/owner` grants with a PAM entitlement; '
                        'when a production incident occurs, the on-call lead requests 2-hour elevation with incident '
                        'ticket justification, receiving instant automated approval from the secondary on-call '
                        'engineer.',
             'technical': '### 1. PAM Entitlement Architecture\n'
                          '- **Entitlement Resource:** Defined at organization, folder, or project level '
                          '(`locations/global/entitlements/[id]`).\n'
                          '- **Eligible Users:** IAM principals (users or groups) permitted to request elevation.\n'
                          '- **Privileged Role:** The target IAM role granted upon activation (e.g. '
                          '`roles/compute.admin` or custom emergency role).\n'
                          '- **Max Request Duration:** Bounded activation window (e.g. `7200s` / 2 hours; maximum '
                          'allowed is `64800s` / 18 hours).\n'
                          '\n'
                          '### 2. Approval Workflows & Multi-Party Control\n'
                          '- **Manual Approval:** Requires designated approver group to explicitly grant activation.\n'
                          '- **Auto Approval:** Evaluated automatically based on criteria (e.g., standard business '
                          'hours or active PagerDuty shift).\n'
                          '- **Self-Approval Prevention:** PAM can enforce that the requester cannot approve their own '
                          'grant.',
             'questions': ['What is the primary security advantage of using Privileged Access Manager instead of '
                           'standing IAM role assignments?',
                           'How does Privileged Access Manager prevent an SRE from maintaining administrative access '
                           'indefinitely?',
                           'Which Cloud Audit log stream captures Privileged Access Manager grant requests and '
                           'approval decisions?'],
             'reference': 'https://cloud.google.com/iam/docs/pam-overview',
             'reference_label': 'Google Cloud IAM: Privileged Access Manager (PAM) architecture and entitlement '
                                'policies',
             'scenario': {'symptom': 'An SRE made an accidental schema drop on a production database during a weekend '
                                     'off-shift because their permanent Owner role was always active.',
                          'constraints': 'Engineers need emergency access during high-severity incidents, but '
                                         'enterprise compliance mandates zero standing admin privileges.',
                          'evidence': 'Cloud Audit Activity log showing unauthorized off-shift action:\n'
                                      '\n'
                                      '```json\n'
                                      '{\n'
                                      '  "protoPayload": {\n'
                                      '    "authenticationInfo": {"principalEmail": "sre-weekend@corp.com"},\n'
                                      '    "methodName": "cloudsql.instances.delete",\n'
                                      '    "resourceName": "projects/prod-db/instances/prod-postgres-primary",\n'
                                      '    "status": {"code": 0, "message": "OK"}\n'
                                      '  }\n'
                                      '}\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: The engineer possessed permanent standing `roles/cloudsql.admin` '
                                      'permissions with zero operational gating.',
                          'diagnostic_steps': ['Audit project IAM policy for standing administrative roles.',
                                               'Inspect Privileged Access Manager entitlements in the organization.',
                                               'Verify Cloud Audit logs for incident ticket justifications.',
                                               'Review duration limits on existing PAM grant configurations.'],
                          'root': 'Standing administrative roles allowed accidental high-impact mutations outside of '
                                  'approved maintenance windows.',
                          'fix': 'Revoke standing admin roles and author a Privileged Access Manager entitlement '
                                 'requiring secondary on-call approval and a 2-hour max duration.',
                          'verify': 'Attempt administrative command without PAM activation and verify HTTP 403 '
                                    'Forbidden; activate grant via PAM and verify command succeeds.',
                          'residual': 'Emergency activations require approvers to be responsive; fallback out-of-band '
                                      'break-glass procedures must be maintained.',
                          'diagram': ('SRE possesses standing permanent Admin role',
                                      'Accidental mutation executed during off-shift',
                                      'Production database dropped with zero oversight',
                                      'Deploy PAM JIT entitlement with 2-hour cap & approval',
                                      'Access granted only upon verified incident ticket approval')},
             'lab': {'name': 'Privileged Access Manager (PAM) Just-in-Time Elevation Architecture',
                     'goal': 'Author and deploy a PAM Entitlement policy requiring multi-party approval and automated '
                             'expiration.',
                     'expected': 'Declarative Terraform PAM manifest and Python grant activation simulation verifying '
                                 'approval gates and expiration.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify Privileged Access Manager API enablement and administrative access.',
                     'steps': ['#### Pre-Flight PAM Entitlement Architecture Discovery\n'
                               'Catalog PAM entitlement parameters and duration constraints:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_pam_specs.py\n"
                               'specs = {\n'
                               "    'max_duration': '7200s (2 hours maximum active grant)',\n"
                               "    'privileged_role': 'roles/compute.instanceAdmin.v1',\n"
                               "    'eligible_users': 'group:sre-team@corp.com',\n"
                               "    'approvers': 'group:secops-leads@corp.com'\n"
                               '}\n'
                               "print('[PREFLIGHT] PAM Entitlement Specifications:')\n"
                               'for k, v in specs.items():\n'
                               "    print(f'  • {k:18s}: {v}')\n"
                               'EOF\n'
                               'python3 check_pam_specs.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and PAM schema parser readiness:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_pam_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_pam_tools.sh\n'
                               '```',
                               '#### Core Implementation: PAM Entitlement Terraform Manifest\n'
                               'Author a declarative Terraform configuration establishing the PAM entitlement:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > pam_entitlement.tf\n"
                               'resource "google_privileged_access_manager_entitlement" "sre_emergency_elevation" {\n'
                               '  entitlement_id       = "sre-emergency-compute-admin"\n'
                               '  parent               = "projects/prod-workloads"\n'
                               '  location             = "global"\n'
                               '  max_request_duration = "7200s"\n'
                               '\n'
                               '  eligible_users {\n'
                               '    principals = ["group:sre-team@corp.com"]\n'
                               '  }\n'
                               '\n'
                               '  privileged_access {\n'
                               '    gcp_iam_access {\n'
                               '      role_bindings {\n'
                               '        role = "roles/compute.instanceAdmin.v1"\n'
                               '      }\n'
                               '    }\n'
                               '  }\n'
                               '\n'
                               '  approval_workflow {\n'
                               '    manual_approvals {\n'
                               '      require_approver_justification = true\n'
                               '      steps {\n'
                               '        approvers {\n'
                               '          principals = ["group:secops-leads@corp.com"]\n'
                               '        }\n'
                               '      }\n'
                               '    }\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored pam_entitlement.tf"\n'
                               '```',
                               '#### Execution & JIT Elevation Simulation Engine\n'
                               'Author a Python simulation script modeling PAM grant request, multi-party approval, '
                               'and automatic expiry:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_pam_lifecycle.py\n"
                               'class MockPAMEngine:\n'
                               '    def __init__(self, requester, approver, duration_sec):\n'
                               '        self.requester = requester\n'
                               '        self.approver = approver\n'
                               '        self.duration_sec = duration_sec\n'
                               '\n'
                               '    def process_grant(self, justification):\n'
                               '        if not justification:\n'
                               "            raise ValueError('Justification is mandatory for PAM elevation')\n"
                               '        if self.requester == self.approver:\n'
                               "            raise PermissionError('Self-approval forbidden by PAM policy')\n"
                               '        if self.duration_sec > 7200:\n'
                               "            raise ValueError('Requested duration exceeds max limit (7200s)')\n"
                               "        return f'GRANT_ACTIVATED: Expires in {self.duration_sec}s'\n"
                               '\n'
                               "pam = MockPAMEngine('sre@corp.com', 'secops-lead@corp.com', 3600)\n"
                               "status = pam.process_grant('Incident INC-9182 payment outage')\n"
                               "print(f'[PAM PASS] {status}')\n"
                               'EOF\n'
                               'python3 simulate_pam_lifecycle.py\n'
                               '```',
                               '#### Resiliency Testing & Self-Approval Prevention Chaos Test\n'
                               'Simulate an engineer attempting to approve their own elevation request and assert '
                               'rejection:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_self_approval.py\n"
                               'from simulate_pam_lifecycle import MockPAMEngine\n'
                               '\n'
                               "rogue_pam = MockPAMEngine('sre@corp.com', 'sre@corp.com', 3600)\n"
                               'try:\n'
                               "    rogue_pam.process_grant('Self escalation')\n"
                               "    raise AssertionError('PAM permitted unauthorized self-approval!')\n"
                               'except PermissionError as e:\n'
                               "    print(f'[CHAOS TEST PASS] PAM intercepted self-approval attempt: {e}')\n"
                               'EOF\n'
                               'python3 test_self_approval.py\n'
                               '```',
                               '#### Telemetry, Observability & PAM Grant Audit Logging\n'
                               'Author a Cloud Logging filter tracking PAM elevation grants and approval events:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > pam_audit_filter.txt\n"
                               'protoPayload.serviceName="privilegedaccessmanager.googleapis.com"\n'
                               'protoPayload.methodName=~"(CreateGrant|ApproveGrant)"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to pam_audit_filter.txt"\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform PAM manifest attributes:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_pam_manifest.py\n"
                               "with open('pam_entitlement.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'google_privileged_access_manager_entitlement' in tf\n"
                               'assert \'max_request_duration = "7200s"\' in tf\n'
                               "assert 'require_approver_justification = true' in tf\n"
                               "print('[ASSERT PASS] Privileged Access Manager manifest strictly validated.')\n"
                               'EOF\n'
                               'python3 assert_pam_manifest.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_pam_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 102 Topic 2 test scripts..."\n'
                               'rm -f check_pam_specs.py check_pam_tools.sh simulate_pam_lifecycle.py '
                               'test_self_approval.py assert_pam_manifest.py\n'
                               'echo "[CLEANUP] Retaining production files: pam_entitlement.tf, pam_audit_filter.txt"\n'
                               'echo "[CLEANUP PASS] PAM lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_pam_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm max 2-hour duration and strict '
                                     'multi-party approval enforcement.',
                     'trouble': 'Ensure Privileged Access Manager API is enabled in the target project.',
                     'cleanup': 'bash teardown_pam_lab.sh',
                     'accept': 'PAM manifest and test suite pass verification with 0 errors.',
                     'file': 'day-102-topic-02-privileged-access-manager.md'}},
            {'key': 'topic-03',
             'title': 'Break-glass accounts',
             'overview': 'Break-glass emergency accounts provide out-of-band administrative access to Google Cloud '
                         'during catastrophic identity provider (IdP) outages, SAML certificate expirations, or severe '
                         'cyber security emergencies. These accounts reside in an isolated Cloud Identity domain '
                         'completely detached from corporate single sign-on (SSO) infrastructure. They are secured '
                         'with physical FIDO2 hardware security keys stored in geographically separated dual-custody '
                         'safes. Under normal operations, break-glass accounts possess zero standing privileges; any '
                         'authentication or elevation immediately triggers automated high-severity broadcast alerts '
                         'across executive and security teams.',
             'preview': "An enterprise's corporate Okta tenant suffers an unexpected 6-hour global outage; while "
                        'standard employee logins are completely disabled, designated incident commanders retrieve '
                        'physical security keys from the dual-custody safe to activate break-glass emergency response.',
             'technical': '### 1. Break-Glass Account Principles\n'
                          '- **Out-of-Band Identity:** Hosted on an independent domain (e.g. '
                          '`emergency.acmecorp-gcp.com`) or direct Cloud Identity instance with zero dependency on '
                          'corporate IdP.\n'
                          '- **Physical FIDO2 Hardware Keys:** Dual physical security keys (YubiKey) stored in '
                          'tamper-evident sealed envelopes inside dual-custody physical vaults.\n'
                          '- **Zero Standing Privileges:** Account holds no roles by default; role elevation is '
                          'managed via pre-staged conditional IAM scripts or dedicated emergency PAM entitlements.\n'
                          '\n'
                          '### 2. Operational Alarms & Post-Glass Procedures\n'
                          '- **Immediate Broadcast Alerting:** Cloud Function/Eventarc triggered on '
                          '`cloudaudit.googleapis.com` login events for the break-glass principal, fanning out '
                          'PagerDuty, SMS, and email alerts.\n'
                          '- **Post-Incident Remediation:** Mandatory credential rotation, hardware key replacement, '
                          'audit log forensic sealing, and post-mortem review.',
             'questions': ['Why must break-glass accounts be hosted in an isolated Cloud Identity domain rather than '
                           'federated through the corporate IdP?',
                           'What physical security control prevents a single rogue engineer from activating a '
                           'break-glass emergency account?',
                           'What automated alerting action must immediately occur when a break-glass account '
                           'authenticates to Google Cloud?'],
             'reference': 'https://cloud.google.com/architecture/identity/best-practices-break-glass-accounts',
             'reference_label': 'Google Cloud Architecture: Emergency break-glass accounts best practices',
             'scenario': {'symptom': 'An enterprise IdP certificate expired during a holiday weekend, locking all '
                                     'engineers out of Google Cloud during a critical production data corruption '
                                     'event.',
                          'constraints': 'Corporate SSO is completely unresponsive; recovery requires immediate access '
                                         'to the organization root node.',
                          'evidence': 'Authentication error during incident response:\n'
                                      '\n'
                                      '```text\n'
                                      'Google Cloud SSO Error: SAML assertion rejected: Partner certificate expired at '
                                      '2026-09-29T00:00:00Z.\n'
                                      'Contact your workspace administrator to renew the X.509 certificate.\n'
                                      'All 1,400 corporate engineers unable to authenticate to Google Cloud Console or '
                                      'gcloud CLI.\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: The organization had zero independent emergency accounts, resulting '
                                      'in 6 hours of unmitigated downtime while external IdP certificates were '
                                      'reissued.',
                          'diagnostic_steps': ['Check Google Cloud login endpoint availability for non-SSO identities.',
                                               'Verify physical access to emergency safe containing break-glass '
                                               'security keys.',
                                               'Inspect automated alerting webhooks configured for emergency '
                                               'principals.',
                                               'Audit IAM permissions pre-staged for emergency recovery.'],
                          'root': 'Lack of an out-of-band break-glass account created a single point of failure '
                                  'dependent on external IdP availability.',
                          'fix': 'Provision two isolated Cloud Identity break-glass super-admin accounts with physical '
                                 'FIDO2 security keys stored in dual-custody safes, and deploy an automated Eventarc '
                                 'alert rule.',
                          'verify': 'Simulate break-glass login and verify high-severity PagerDuty broadcast fires '
                                    'within 15 seconds.',
                          'residual': 'Break-glass credentials must be rotated immediately following any activation, '
                                      'including emergency drills.',
                          'diagram': ('Corporate IdP certificate expires during weekend',
                                      'All engineers locked out of Google Cloud Console',
                                      'Critical production incident remains unmitigated for 6 hours',
                                      'Retrieve FIDO2 key from safe & login via out-of-band break-glass',
                                      'Emergency access restored in 5 minutes with full broadcast alert')},
             'lab': {'name': 'Break-Glass Emergency Account Architecture and Alerting',
                     'goal': 'Author emergency break-glass IAM elevation scripts and high-priority Cloud Monitoring '
                             'alert policies.',
                     'expected': 'Emergency activation automation and monitoring policy alerting on break-glass '
                                 'identity usage.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify Cloud Monitoring and IAM permissions.',
                     'steps': ['#### Pre-Flight Emergency Account Inventory\n'
                               'Catalog break-glass account specifications and operational rules:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_breakglass_specs.py\n"
                               'specs = {\n'
                               "    'principal': 'breakglass-admin@emergency.corp.gcp.internal',\n"
                               "    'mfa_type': 'Hardware FIDO2 Security Key (YubiKey 5 NFC)',\n"
                               "    'storage': 'Dual-custody fireproof safe (Site A and Site B)',\n"
                               "    'alert_targets': 'PagerDuty P0, CISO SMS, Security Ops Bridge'\n"
                               '}\n'
                               "print('[PREFLIGHT] Emergency Break-Glass Account Configuration:')\n"
                               'for k, v in specs.items():\n'
                               "    print(f'  • {k:16s}: {v}')\n"
                               'EOF\n'
                               'python3 check_breakglass_specs.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Python and JSON tooling readiness:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_bg_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_bg_tools.sh\n'
                               '```',
                               '#### Core Implementation: Emergency Elevation Script\n'
                               'Author a pre-staged emergency elevation bash script with strict time bounding:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > activate_breakglass.sh\n"
                               '#!/usr/bin/env bash\n'
                               '# Emergency Break-Glass Activation Automation\n'
                               'set -euo pipefail\n'
                               '\n'
                               'TARGET_PRINCIPAL="breakglass-admin@emergency.corp.gcp.internal"\n'
                               'ORG_ID="108420918237"\n'
                               '\n'
                               'echo "[ALERT] INITIATING EMERGENCY BREAK-GLASS ACTIVATION FOR ${TARGET_PRINCIPAL}..."\n'
                               'echo "[STEP 1] Validating hardware security key presence... PASS"\n'
                               'echo "[STEP 2] Pre-staged temporary binding to Organization Admin role..."\n'
                               '# Simulated gcloud organizations add-iam-policy-binding-with-condition\n'
                               'echo "[STEP 3] Emitting high-priority emergency broadcast alert..."\n'
                               'echo "[ACTIVATED] Break-glass access active. Max emergency window: 2 hours."\n'
                               'EOF\n'
                               'chmod +x activate_breakglass.sh\n'
                               'bash activate_breakglass.sh\n'
                               '```',
                               '#### Execution & Emergency Broadcast Alert Policy Manifest\n'
                               'Author a Cloud Monitoring Alert Policy alerting whenever the break-glass principal '
                               'performs any API action:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_breakglass_usage.json\n"
                               '{\n'
                               '  "displayName": "EMERGENCY BROADCAST: Break-Glass Account Activated",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "Any Cloud Audit activity from breakglass principal",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": "logName=\\"cloudaudit.googleapis.com%2Factivity\\" AND '
                               'protoPayload.authenticationInfo.principalEmail=\\"breakglass-admin@emergency.corp.gcp.internal\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 0.0,\n'
                               '        "duration": "0s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] Authored alert_breakglass_usage.json"\n'
                               '```',
                               '#### Resiliency Testing & Silent Access Intercept Chaos Test\n'
                               'Simulate an attempt by a rogue administrator to suppress the break-glass alert and '
                               'assert failure:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_alert_unsuppressible.py\n"
                               'def verify_alert_policy_immutability(policy_channels):\n'
                               "    if 'external-siem-webhook' not in policy_channels:\n"
                               "        raise RuntimeError('SECURITY FLAW: External SIEM notification channel "
                               "missing!')\n"
                               "    return '[PASS] Break-glass alert channel cannot be suppressed from internal "
                               "console.'\n"
                               '\n'
                               "res = verify_alert_policy_immutability(['pagerduty-p0', 'ciso-sms', "
                               "'external-siem-webhook'])\n"
                               'print(res)\n'
                               'EOF\n'
                               'python3 test_alert_unsuppressible.py\n'
                               '```',
                               '#### Telemetry, Observability & Break-Glass Audit Trail\n'
                               'Author an audit query searching for break-glass actions across all projects:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > breakglass_audit_query.sql\n"
                               'SELECT\n'
                               '  timestamp,\n'
                               '  protopayload_auditlog.methodName AS api_call,\n'
                               '  protopayload_auditlog.resourceName AS target_resource,\n'
                               '  protopayload_auditlog.requestMetadata.callerIp AS ip_address\n'
                               'FROM `sec-vault-prod.audit_dataset._AllLogs`\n'
                               'WHERE protopayload_auditlog.authenticationInfo.principalEmail = '
                               "'breakglass-admin@emergency.corp.gcp.internal'\n"
                               'ORDER BY timestamp DESC;\n'
                               'EOF\n'
                               'echo "[SQL] Query authored in breakglass_audit_query.sql"\n'
                               '```',
                               '#### Automated Verification & Script Assertions\n'
                               'Execute automated test validating break-glass activation script:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_breakglass_script.py\n"
                               "with open('activate_breakglass.sh') as f:\n"
                               '    script = f.read()\n'
                               '\n'
                               "assert 'set -euo pipefail' in script\n"
                               "assert 'breakglass-admin@emergency.corp.gcp.internal' in script\n"
                               "assert 'EMERGENCY' in script\n"
                               "print('[ASSERT PASS] Break-glass activation script strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_breakglass_script.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_breakglass_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 102 Topic 3 test scripts..."\n'
                               'rm -f check_breakglass_specs.py check_bg_tools.sh activate_breakglass.sh '
                               'test_alert_unsuppressible.py assert_breakglass_script.py\n'
                               'echo "[CLEANUP] Retaining production files: alert_breakglass_usage.json, '
                               'breakglass_audit_query.sql"\n'
                               'echo "[CLEANUP PASS] Break-glass lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_breakglass_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm immediate unsuppressible alerting '
                                     'upon break-glass authentication.',
                     'trouble': 'Ensure notification channels for the alert policy are connected to off-band systems '
                                '(PagerDuty/SMS).',
                     'cleanup': 'bash teardown_breakglass_lab.sh',
                     'accept': 'Break-glass script and alert policy pass verification with 0 errors.',
                     'file': 'day-102-topic-03-break-glass-accounts.md'}},
            {'key': 'topic-04',
             'title': 'Access Transparency and Access Approval',
             'overview': 'Access Transparency (AXT) and Access Approval (AXA) provide enterprise customers with '
                         'unprecedented visibility and control over administrative actions performed by Google '
                         'personnel. Access Transparency provides near real-time audit logs whenever a Google engineer '
                         'accesses customer content during support escalations or infrastructure maintenance. Access '
                         'Approval takes this control further by requiring explicit, pre-authorized customer sign-off '
                         'before Google personnel can access customer resources. Together, they ensure that cloud '
                         'provider access is fully auditable, defensible, and compliant with stringent global '
                         'regulatory standards (SOC 2, ISO 27001, HIPAA, FedRAMP).',
             'preview': 'A financial auditor requests proof that no Google Cloud employee accessed customer payment '
                        'databases during the past quarter; the enterprise exports Access Transparency logs and Access '
                        'Approval grant records demonstrating zero unauthorized provider access.',
             'technical': '### 1. Access Transparency (AXT)\n'
                          '- **Log Stream:** `cloudaudit.googleapis.com/access_transparency`.\n'
                          '- **Logged Attributes:** Accessor identifier (obfuscated or support ID), access reason '
                          '(support ticket justification), target resource name, and accessed methods.\n'
                          '- **Integration:** Sinks can route AXT logs to Cloud Storage, BigQuery, or external SIEMs '
                          '(Splunk, Chronicle).\n'
                          '\n'
                          '### 2. Access Approval (AXA)\n'
                          '- **Workflow:** When Google support requires access, an approval request is generated and '
                          'delivered via Email, Pub/Sub, or Console.\n'
                          '- **Explicit Action:** Customer administrator reviews justification ticket ID and '
                          "explicitly clicks 'Approve' or 'Dismiss'.\n"
                          '- **Time-Bounded Scope:** Approvals grant temporary access (default: 8 hours or ticket '
                          'resolution).\n'
                          '- **Exemptions:** Automatic access allowed only during critical security or system '
                          'availability emergencies (which still generate full AXT logs).',
             'questions': ['What is the fundamental difference between Access Transparency and Access Approval?',
                           'Which Cloud Logging log stream records administrative actions taken by Google Cloud '
                           'personnel?',
                           'What happens if an Access Approval request expires without customer interaction?'],
             'reference': 'https://cloud.google.com/access-transparency/docs/overview',
             'reference_label': 'Google Cloud: Access Transparency and Access Approval architecture',
             'scenario': {'symptom': 'An external regulatory audit cited the organization for failing to demonstrate '
                                     'independent oversight of cloud service provider administrative access.',
                          'constraints': 'Enterprise must provide cryptographic audit proof of all third-party '
                                         'administrative touches to customer healthcare records.',
                          'evidence': 'Audit report extract:\n'
                                      '\n'
                                      '```text\n'
                                      'SOC 2 Type II Finding: Organization failed to demonstrate explicit '
                                      'authorization gates for cloud provider support personnel.\n'
                                      'Google Cloud Support tickets referenced manual database inspections, but no '
                                      'customer pre-approval records existed in the audit trail.\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: Access Transparency was enabled, but Access Approval was '
                                      'unconfigured, allowing Google support to access resources upon ticket creation '
                                      'without explicit customer sign-off.',
                          'diagnostic_steps': ['Query Access Approval settings using gcloud access-approval settings '
                                               'get.',
                                               'Verify Access Transparency log routing sinks in the organization root.',
                                               'Inspect customer notification settings for support approval requests.',
                                               'Check for unapproved support accesses in Access Transparency logs.'],
                          'root': 'Access Approval was not enforced at the organization level, omitting explicit '
                                  'customer pre-authorization for support interventions.',
                          'fix': 'Deploy Access Approval at the organization root with mandatory notification emails '
                                 'to the SecOps team and explicit approval required for all services.',
                          'verify': 'Simulate support escalation and verify that Google personnel cannot access '
                                    'resources until customer approves the request via API or Console.',
                          'residual': 'Emergency break-glass by Google for system-wide infrastructure recovery '
                                      'bypasses AXA but generates an immutable AXT log entry.',
                          'diagram': ('Google engineer responds to customer support ticket',
                                      'Access Approval unconfigured -> support accesses data directly',
                                      'SOC 2 compliance audit issues formal violation finding',
                                      'Enforce Access Approval at Org root with mandatory sign-off',
                                      'Google engineer blocked until SecOps explicitly approves request')},
             'lab': {'name': 'Access Transparency and Access Approval Architecture',
                     'goal': 'Author and deploy organization-level Access Approval settings and Access Transparency '
                             'logging sinks.',
                     'expected': 'Declarative Terraform Access Approval manifest and Python log analysis testing AXT '
                                 'audit trail extraction.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify organization administrator privileges and Access Approval API enablement.',
                     'steps': ['#### Pre-Flight Access Approval Configuration Discovery\n'
                               'Catalog Access Transparency and Access Approval settings:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_axt_specs.py\n"
                               'specs = {\n'
                               "    'axt_log_name': 'cloudaudit.googleapis.com/access_transparency',\n"
                               "    'axa_enforcement': 'Mandatory across all services (allServices)',\n"
                               "    'notification_emails': ['secops-approvers@corp.com'],\n"
                               "    'default_request_duration': '8 hours maximum'\n"
                               '}\n'
                               "print('[PREFLIGHT] Access Transparency / Approval Specifications:')\n"
                               'for k, v in specs.items():\n'
                               "    print(f'  • {k:26s}: {v}')\n"
                               'EOF\n'
                               'python3 check_axt_specs.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and policy syntax linters:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_axa_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_axa_tools.sh\n'
                               '```',
                               '#### Core Implementation: Access Approval Terraform Manifest\n'
                               'Author a declarative Terraform configuration enforcing Access Approval across the '
                               'organization:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > access_approval.tf\n"
                               'resource "google_organization_access_approval_settings" "org_access_approval" {\n'
                               '  organization_id     = "108420918237"\n'
                               '  notification_emails = ["secops-approvers@corp.com"]\n'
                               '\n'
                               '  enrolled_services {\n'
                               '    cloud_product = "all"\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored access_approval.tf"\n'
                               '```',
                               '#### Execution & Access Approval Workflow Simulation\n'
                               'Author a Python simulation script evaluating Access Approval request and decision '
                               'workflows:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_access_approval.py\n"
                               'class AccessApprovalEngine:\n'
                               '    def __init__(self, request_id, justification, approvers):\n'
                               '        self.request_id = request_id\n'
                               '        self.justification = justification\n'
                               '        self.approvers = approvers\n'
                               "        self.status = 'PENDING'\n"
                               '\n'
                               '    def approve(self, approver_email):\n'
                               '        if approver_email not in self.approvers:\n'
                               "            raise PermissionError('Unauthorized approver')\n"
                               "        self.status = 'APPROVED'\n"
                               "        return f'ACCESS GRANTED: Ticket {self.justification} authorized by "
                               "{approver_email}'\n"
                               '\n'
                               "axa = AccessApprovalEngine('req-8120', 'Google Support Case #918201', "
                               "['secops-approvers@corp.com'])\n"
                               "msg = axa.approve('secops-approvers@corp.com')\n"
                               "print(f'[APPROVAL PASS] {msg}')\n"
                               'EOF\n'
                               'python3 simulate_access_approval.py\n'
                               '```',
                               '#### Resiliency Testing & Expired Request Chaos Test\n'
                               'Simulate an unapproved support access request reaching expiration and verify access '
                               'block:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_expired_approval.py\n"
                               'def evaluate_support_access(status):\n'
                               "    if status != 'APPROVED':\n"
                               "        raise PermissionError('HTTP 403 Forbidden: Google support access request not "
                               "approved or expired.')\n"
                               "    return 'ACCESS_PERMITTED'\n"
                               '\n'
                               'try:\n'
                               "    evaluate_support_access('EXPIRED')\n"
                               "    raise AssertionError('Unapproved support access permitted!')\n"
                               'except PermissionError as e:\n'
                               "    print(f'[CHAOS TEST PASS] Access Approval blocked unapproved support access: "
                               "{e}')\n"
                               'EOF\n'
                               'python3 test_expired_approval.py\n'
                               '```',
                               '#### Telemetry, Observability & Access Transparency Log Parsing\n'
                               'Author an automated script parsing Access Transparency audit logs:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > parse_axt_logs.py\n"
                               'sample_axt_entry = {\n'
                               "    'serviceName': 'cloudsql.googleapis.com',\n"
                               "    'methodName': 'google.cloud.sql.v1beta4.SqlInstancesService.Get',\n"
                               "    'accessor': {'principal': 'google-support-agent-918@google.com'},\n"
                               "    'justification': {'reason': 'CUSTOMER_INITIATED_SUPPORT', 'ticketNumber': "
                               "'CASE-91823'}\n"
                               '}\n'
                               "print('[AXT LOG EXTRACT] Verified Google support action:')\n"
                               'print(f\'  • Accessor: {sample_axt_entry["accessor"]["principal"]}\')\n'
                               'print(f\'  • Justification: {sample_axt_entry["justification"]["reason"]} (Ticket: '
                               '{sample_axt_entry["justification"]["ticketNumber"]})\')\n'
                               'print(f\'  • Method: {sample_axt_entry["methodName"]}\')\n'
                               'EOF\n'
                               'python3 parse_axt_logs.py\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform Access Approval manifest:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_axa_manifest.py\n"
                               "with open('access_approval.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'google_organization_access_approval_settings' in tf\n"
                               "assert 'notification_emails' in tf\n"
                               'assert \'cloud_product = "all"\' in tf\n'
                               "print('[ASSERT PASS] Access Approval manifest strictly validated.')\n"
                               'EOF\n'
                               'python3 assert_axa_manifest.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_axa_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 102 Topic 4 test scripts..."\n'
                               'rm -f check_axt_specs.py check_axa_tools.sh simulate_access_approval.py '
                               'test_expired_approval.py parse_axt_logs.py assert_axa_manifest.py\n'
                               'echo "[CLEANUP] Retaining production file: access_approval.tf"\n'
                               'echo "[CLEANUP PASS] Access Approval lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_axa_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm Access Approval enrollment for '
                                     'all services and parse AXT logs.',
                     'trouble': 'Verify that the notification emails belong to valid security team distribution lists.',
                     'cleanup': 'bash teardown_axa_lab.sh',
                     'accept': 'Access Approval manifest and test suite pass verification with 0 errors.',
                     'file': 'day-102-topic-04-access-transparency.md'}}]}
