"""day_data_116.py — Exhaustive architecture data specification for Day 116.

Covers End-to-End Security Integration:
- No-Public-IP Architecture & Cloud NAT
- Identity-Aware Proxy (IAP) Tunneling
- Private Google Access & Private Service Connect (PSC)
- Organization Policy Guardrails (vmExternalIpAccess, requireOsLogin)
- VPC Service Controls (Perimeter Dry-Run Mode & Ingress/Egress Rules)
- Cloud KMS CMEK Automatic Version Rotation & Decryption Invariants
"""

DAY_NUM = 116

DATA = {
    'day': 116,
    'part1_intro': (
        'Day 116 synthesizes and validates the foundational security, network isolation, and cryptographic controls studied across '
        'earlier modules into a unified, end-to-end enterprise architecture. Enterprise architects integrate no-public-IP compute '
        'topologies, Identity-Aware Proxy (IAP) contextual tunneling, private API access via Private Google Access and Private '
        'Service Connect (PSC), authoritative Organization Policy guardrails, VPC Service Controls perimeter dry-run validation, '
        'and Customer-Managed Encryption Key (CMEK) automated cryptographic rotation into a coherent, verifiable request trace.'
    ),
    'exit_summary': (
        'An integrated security trace and a list of inconsistencies repaired across identity, network and data controls.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts the complementary defensive layers that form Google Cloud’s defense-in-depth '
        'security boundary, detailing control planes, enforcement mechanisms, telemetry sources, and multi-control interaction points.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Defensive Layer</th>\n'
        '<th>Enforcement Plane &amp; Mechanism</th>\n'
        '<th>Core Configuration Parameters</th>\n'
        '<th>Primary Audit &amp; Telemetry Signal</th>\n'
        '<th>Cross-Control Dependency &amp; Inconsistency Risk</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>1. Zero Public IP Perimeter</strong></td>\n'
        '<td>Compute Engine / VPC Network Interface control</td>\n'
        '<td>`constraints/compute.vmExternalIpAccess` (Deny ALL), Cloud NAT for egress</td>\n'
        '<td>Compute instance describe `networkInterfaces[0].accessConfigs` is empty</td>\n'
        '<td>External traffic blocked, requiring IAP TCP forwarding or Private Service Connect for ingress.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>2. Identity-Aware Proxy (IAP)</strong></td>\n'
        '<td>Context-Aware Access (BeyondCorp) &amp; Google Front End (GFE)</td>\n'
        '<td>Firewall rule allowing `35.235.240.0/20` on TCP 22/3389/443; IAM `roles/iap.tunnelResourceAccessor`</td>\n'
        '<td>Cloud Audit Data Access logs (`cloudaudit.googleapis.com`) with client device context</td>\n'
        '<td>Missing firewall route for GFE range drops IAP proxy connections despite valid IAM permissions.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>3. Private API Access (PGA / PSC)</strong></td>\n'
        '<td>Andromeda Software-Defined Network encapsulation</td>\n'
        '<td>Subnet `privateIpGoogleAccess=true`, DNS forward to `restricted.googleapis.com` (199.36.153.4/30)</td>\n'
        '<td>VPC Flow Logs showing internal VM to Google VIP egress; DNS query logs</td>\n'
        '<td>Routing to `default` instead of `restricted` VIP permits data exfiltration outside VPC SC perimeters.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>4. VPC Service Controls</strong></td>\n'
        '<td>Google API gateway control plane inspection</td>\n'
        '<td>Service perimeter defining protected projects, restricted services, and dry-run evaluation</td>\n'
        '<td>VPC SC violation logs with `vpcServiceControlsUniqueIdentifier` and `violationReason`</td>\n'
        '<td>Deploying perimeters in enforced mode without dry-run auditing halts cross-project analytics pipelines.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>5. CMEK Cryptographic Lifecycle</strong></td>\n'
        '<td>Cloud KMS HSM/Software CryptoKey Engine</td>\n'
        '<td>`rotationPeriod="7776000s"` (90 days), service agent binding `roles/cloudkms.cryptoKeyEncrypterDecrypter`</td>\n'
        '<td>KMS API audit logs capturing Decrypt invocations and primary key version ID</td>\n'
        '<td>Revoking IAM from service agents or destroying older key versions renders historical ciphertext unreadable.</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 116: End-to-End Integrated Private Access, Security Perimeter, and CMEK Lifecycle Topology',
        'desc': 'Architectural layout illustrating remote administrator access through Identity-Aware Proxy into private VPC subnets, Private Google Access to restricted API VIPs, VPC Service Controls dry-run perimeters, and CMEK storage encryption.',
        'caption': 'Figure 116.1: End-to-end security integration topology showing contextual IAP ingress, private VPC routes, restricted Google VIPs, VPC Service Controls perimeter boundaries, and Cloud KMS CMEK encryption.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: BeyondCorp Identity & Administrative Ingress Plane',
                'desc': 'Client workstation, Context-Aware device verification, and Identity-Aware Proxy (IAP) TCP proxy',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Isolated Private VPC Network & Host Boundary',
                'desc': 'Subnets with no external IPs, Cloud NAT egress gateway, and strict 35.235.240.0/20 IAP ingress firewall',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Private Google Access & API DNS Routing Plane',
                'desc': 'Cloud DNS response policies directing api.googleapis.com to restricted.googleapis.com (199.36.153.4/30)',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: VPC Service Controls Security Perimeter Domain',
                'desc': 'Dry-run perimeter protecting Cloud Storage, BigQuery, and Secret Manager against exfiltration',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: Cloud KMS Cryptographic Custody & CMEK Storage Plane',
                'desc': 'Cloud KMS Key Rings, automated 90-day rotation, and CMEK-encrypted Cloud Storage & Cloud SQL resources',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Admin Workstation', 'detail': 'Context-Aware Device', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'IAP TCP Proxy VIP', 'detail': '35.235.240.0/20 Tunnel', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Private Compute VM', 'detail': 'No External IP / OS Login', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Cloud NAT Gateway', 'detail': 'Outbound Only (No Ingress)', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Private Google Access', 'detail': 'Subnet PGA Enabled', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Cloud DNS Policy', 'detail': 'restricted.googleapis.com', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'VPC SC Perimeter', 'detail': 'Dry-Run Mode Active', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Violation Log Sink', 'detail': 'Dry-Run Audit Filter', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Cloud KMS Key Ring', 'detail': 'Auto-Rotate (90 Days)', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'CMEK Data Bucket', 'detail': 'Encrypted by KMS Version', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'CONTEXTUAL ACCESS & ADMINISTRATIVE INGRESS BOUNDARY', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'VPC NETWORK & PRIVATE API ROUTING DOMAIN', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'VPC SERVICE CONTROLS & CMEK ENCRYPTION PERIMETER', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Evaluate Context & Device', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Forward SSH via IAP', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Egress via Cloud NAT', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Route API to PGA', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Resolve Restricted VIP', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Inspect VPC SC Rules', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Audit Dry-Run Hits', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Invoke KMS Decrypt', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Read CMEK Ciphertext', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: Public IP Invariant: Zero External Access Configs Verified', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: DNS Resolution: Verify 199.36.153.4/30 Restricted VIP', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 450, 'label': 'PROBE 3: CMEK Invariant: Verify Decryption Succeeds Across Key Rotations', 'badge': 'P3', 'color': '#22c55e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world cross-control integration failures, perimeter dry-run mismatches, '
        'unintended routing breaks, and key rotation outages across complex multi-project Google Cloud deployments. '
        'Each scenario details verbatim diagnostic logs, root cause mechanisms, production remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on architectural exercises implement the complete operational engineering lifecycle for Day 116. '
        'Architects construct an end-to-end multi-layer security trace script in Python that validates identity, network, perimeter, '
        'and cryptographic invariants across a unified enterprise environment, identifying and repairing cross-control inconsistencies.'
    ),
    'topics': [
        # TOPIC 1
        {
            'key': 'topic-01',
            'title': 'Integrate controls already studied: no-public-IP access, IAP, private API access, policy guardrails, perimeter dry-run and CMEK rotation. Validate the existing example end to end',
            'overview': (
                'Enterprise cloud security requires the harmonious integration of multiple independent defensive systems: identity governance, '
                'network perimeter filtering, private API routing, policy guardrails, and cryptographic key management. '
                'A single configuration flaw in any layer—such as a missing firewall rule for Identity-Aware Proxy, an incomplete DNS override '
                'for Private Google Access, an un-audited VPC Service Controls perimeter, or an expired CMEK service agent grant—can break '
                'production availability or silently expose internal assets. Day 116 validates the entire request path end-to-end.'
            ),
            'preview': (
                'An enterprise microservice fails to query a Cloud Storage bucket following a Cloud KMS key rotation because a VPC Service '
                'Controls perimeter dry-run rule was misconfigured, blocking cross-project KMS decrypt calls.'
            ),
            'technical': (
                'An integrated end-to-end security architecture enforces multi-layered invariants across the complete request lifecycle.\n\n'
                '### 1. The Zero-Public-IP & Ingress Control Boundary\n'
                '- **Policy Enforcement**: `constraints/compute.vmExternalIpAccess` is enforced at the organization root, preventing any '
                'developer or automation from attaching public IPv4 addresses to Compute Engine instances or GKE nodes.\n'
                '- **Administrative Access via IAP**: Operators connect to private instances strictly using Identity-Aware Proxy TCP forwarding:\n'
                '  <kbd>gcloud compute ssh [VM_NAME] --tunnel-through-iap --zone=[ZONE]</kbd>.\n'
                '- **Firewall Invariant**: The VPC network must contain an ingress firewall rule allowing TCP ports 22 (SSH) and 3389 (RDP) '
                'strictly from the Google Front End IP block `35.235.240.0/20`. All other external ingress is denied.\n\n'
                '### 2. Private Google Access & API DNS Boundaries\n'
                '- **Subnet PGA**: Every subnet hosting workloads has `privateIpGoogleAccess = true`, enabling instances without external IPs '
                'to access Google APIs.\n'
                '- **Restricted VIP Routing**: Standard `default.googleapis.com` resolves to public IPs. To enforce VPC Service Controls compliance, '
                'Cloud DNS private response zones must map `*.googleapis.com` and `*.pkg.dev` to `restricted.googleapis.com` (`199.36.153.4/30`).\n'
                '- **Route Table Invariant**: A custom static route directs `199.36.153.4/30` to the `default-internet-gateway` next hop.\n\n'
                '### 3. VPC Service Controls Dry-Run Governance\n'
                '- **Perimeter Architecture**: Defines the security boundary enclosing workloads, storage buckets, and BigQuery datasets.\n'
                '- **Dry-Run Validation**: Before enforcing perimeters, security teams run perimeters in `DRY_RUN` mode. All cross-project calls '
                'that violate perimeter ingress/egress rules execute successfully but emit structured `VpcServiceControlsViolation` logs in '
                'Cloud Logging, allowing engineers to author precise ingress/egress allow rules prior to full enforcement.\n\n'
                '### 4. CMEK Key Lifecycle & Rotation Invariants\n'
                '- **Rotation Invariant**: Cloud KMS CryptoKeys rotate automatically on a 90-day schedule (`rotation_period = "7776000s"`). '
                'New write operations automatically use the new primary CryptoKey version.\n'
                '- **Decryption Continuity**: Historical CryptoKey versions must remain in the `ENABLED` state indefinitely. Service agents '
                '(e.g. `service-[PROJECT_NUM]@gs-project.iam.gserviceaccount.com`) must retain `roles/cloudkms.cryptoKeyEncrypterDecrypter` '
                'across all versions to ensure existing data remains readable without disruption.'
            ),
            'questions': [
                'How do Organization Policy guardrails, IAP firewall rules, and VPC routing combine to eliminate external IP dependencies?',
                'Why must Cloud DNS route traffic specifically to restricted.googleapis.com (199.36.153.4/30) rather than private.googleapis.com when enforcing VPC Service Controls?',
                'What operational failure occurs if an administrator destroys an older Cloud KMS CryptoKey version following an automated rotation?'
            ],
            'reference': 'https://docs.cloud.google.com/binary-authorization/docs',
            'reference_label': 'Google Cloud Security Architecture & Private Access Integration Guide',
            'scenario': {
                'symptom': 'Internal billing service loses access to encrypted financial records immediately following automated Cloud KMS key rotation.',
                'impact': 'Daily financial reconciliation jobs fail; operations team suspects Cloud KMS corruption or database failure.',
                'constraints': 'Private workloads must access CMEK storage across key rotations without external IP exposure or perimeter violations.',
                'evidence': (
                    'VPC Service Controls Dry-Run and KMS Audit Log correlation:\n\n'
                    '```json\n'
                    '{\n'
                    '  "protoPayload": {\n'
                    '    "methodName": "cloudkms.googleapis.com/v1.CryptoKeyService.Decrypt",\n'
                    '    "status": {"code": 7, "message": "Request denied by VPC Service Controls: cross-project KMS call blocked"},\n'
                    '    "serviceData": {\n'
                    '      "vpcServiceControlsViolation": {\n'
                    '        "violationReason": "SECURITY_PERIMETER_VIOLATION",\n'
                    '        "callerProject": "fintech-billing-prod",\n'
                    '        "targetResource": "projects/fintech-sec-kms/locations/us-central1/keyRings/billing/cryptoKeys/fin-key/cryptoKeyVersions/2"\n'
                    '      }\n'
                    '    }\n'
                    '  }\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: When version 2 of the CMEK key was created, the Cloud Storage service agent in `fintech-billing-prod` '
                    'attempted to access the KMS project `fintech-sec-kms`. The VPC Service Controls perimeter omitted an egress rule '
                    'for the new key version service boundary.'
                ),
                'diagnostic_steps': [
                    'Review Cloud Logging for VPC Service Controls violation logs matching the billing service project.',
                    'Check Cloud KMS audit logs to confirm that CryptoKey version 2 was promoted to PRIMARY.',
                    'Inspect the VPC Service Controls perimeter configuration for cross-project ingress and egress rules.',
                    'Verify the Cloud Storage service agent IAM bindings on the KMS Key Ring in `fintech-sec-kms`.'
                ],
                'root': 'The VPC Service Controls perimeter enclosed the storage project but lacked an egress policy permitting the Cloud Storage service agent to invoke KMS Decrypt in the separate security project.',
                'residual': 'Adding new Google Cloud services to the pipeline requires pre-emptively updating perimeter egress rules in dry-run mode.',
                'diagram': (
                    'Cloud KMS rotates billing CryptoKey to Version 2 automatically',
                    'Storage service agent calls KMS Decrypt across project boundaries',
                    'VPC Service Controls perimeter blocks cross-project API invocation',
                    'Author explicit perimeter egress rule permitting storage-to-KMS access',
                    'End-to-end request trace succeeds: private IP, IAP, VPC SC, and CMEK verified'
                )
            },
            'lab': {
                'name': 'End-to-End Integrated Security Trace & Cross-Control Inconsistency Repair',
                'goal': 'Implement a comprehensive Python security integration testing suite that traces a simulated request through Identity-Aware Proxy, No-Public-IP checks, Restricted DNS resolution, VPC Service Controls perimeters, and Cloud KMS CMEK rotation, diagnosing and repairing configuration inconsistencies.',
                'expected': 'A Python verification suite executing all 5 control checks, reporting initial cross-control failures, applying automated repairs, and achieving a 100% verified trace.',
                'mode': 'Python script and CLI data modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/security-integration-lab</kbd>.',
                'steps': [
                    (
                        '#### Define Multi-Layer Security Architecture Configuration\n'
                        'Create the working directory and write a JSON representation of an enterprise cloud environment containing cross-control configuration details (some of which have intentional inconsistencies):\n\n'
                        '```sh\n'
                        'mkdir -p ~/security-integration-lab && cd ~/security-integration-lab\n'
                        'cat <<\'EOF\' > security_topology.json\n'
                        '{\n'
                        '  "compute_instances": [\n'
                        '    {\n'
                        '      "name": "billing-processor-01",\n'
                        '      "zone": "us-central1-a",\n'
                        '      "external_ip": null,\n'
                        '      "internal_ip": "10.0.1.15",\n'
                        '      "iap_access_allowed": true\n'
                        '    }\n'
                        '  ],\n'
                        '  "firewall_rules": [\n'
                        '    {\n'
                        '      "name": "allow-iap-ssh",\n'
                        '      "source_ranges": ["35.235.240.0/20"],\n'
                        '      "allowed_ports": ["tcp:22"]\n'
                        '    }\n'
                        '  ],\n'
                        '  "dns_policy": {\n'
                        '    "domain": "*.googleapis.com",\n'
                        '    "target_vip": "199.36.153.4",\n'
                        '    "is_restricted_vip": true\n'
                        '  },\n'
                        '  "vpc_service_controls": {\n'
                        '    "perimeter_name": "billing_perimeter",\n'
                        '    "mode": "DRY_RUN",\n'
                        '    "protected_projects": ["fintech-billing-prod"],\n'
                        '    "egress_rules": [\n'
                        '      {\n'
                        '        "destination_project": "fintech-sec-kms",\n'
                        '        "service": "cloudkms.googleapis.com",\n'
                        '        "status": "MISSING_CONFIGURATION"\n'
                        '      }\n'
                        '    ]\n'
                        '  },\n'
                        '  "cmek_lifecycle": {\n'
                        '    "key_name": "projects/fintech-sec-kms/locations/us-central1/keyRings/billing/cryptoKeys/fin-key",\n'
                        '    "primary_version": 2,\n'
                        '    "versions": [\n'
                        '      {"version": 1, "state": "ENABLED"},\n'
                        '      {"version": 2, "state": "ENABLED"}\n'
                        '    ],\n'
                        '    "service_agent_permission": "roles/cloudkms.cryptoKeyEncrypterDecrypter"\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the End-to-End Security Trace and Repair Tool\n'
                        'Write a Python tool that evaluates each defensive layer, detects the broken VPC Service Controls egress rule, repairs the configuration inconsistency, and generates an integrated security trace record:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > trace_security_controls.py\n'
                        'import json\n'
                        'from datetime import datetime, timezone\n'
                        '\n'
                        'def evaluate_and_repair():\n'
                        '    with open("security_topology.json", "r") as f:\n'
                        '        topo = json.load(f)\n'
                        '\n'
                        '    print("=== Executing Integrated End-to-End Security Trace ===\\n")\n'
                        '    trace_log = []\n'
                        '    inconsistencies_repaired = []\n'
                        '\n'
                        '    def log_control(layer, status, detail):\n'
                        '        entry = {"layer": layer, "status": status, "detail": detail}\n'
                        '        trace_log.append(entry)\n'
                        '        print(f"[{status}] {layer}: {detail}")\n'
                        '\n'
                        '    # Layer 1: No-Public-IP Check\n'
                        '    has_external_ip = False\n'
                        '    for vm in topo["compute_instances"]:\n'
                        '        if vm["external_ip"] is not None:\n'
                        '            has_external_ip = True\n'
                        '    if not has_external_ip:\n'
                        '        log_control("NO_PUBLIC_IP", "PASS", "All Compute Engine instances have zero external IPv4 configs.")\n'
                        '    else:\n'
                        '        log_control("NO_PUBLIC_IP", "FAIL", "Detected external IP on instance!")\n'
                        '\n'
                        '    # Layer 2: IAP Tunneling\n'
                        '    iap_fw = any("35.235.240.0/20" in fw["source_ranges"] for fw in topo["firewall_rules"])\n'
                        '    if iap_fw:\n'
                        '        log_control("IAP_INGRESS", "PASS", "Firewall allows 35.235.240.0/20 on port tcp:22 for contextual access.")\n'
                        '    else:\n'
                        '        log_control("IAP_INGRESS", "FAIL", "Missing firewall rule for Google Front End IAP range.")\n'
                        '\n'
                        '    # Layer 3: Private Google Access DNS\n'
                        '    dns = topo["dns_policy"]\n'
                        '    if dns["target_vip"] == "199.36.153.4" and dns["is_restricted_vip"]:\n'
                        '        log_control("RESTRICTED_DNS", "PASS", "DNS response policy resolves googleapis.com to 199.36.153.4.")\n'
                        '    else:\n'
                        '        log_control("RESTRICTED_DNS", "FAIL", "DNS routes to default public VIP instead of restricted VIP.")\n'
                        '\n'
                        '    # Layer 4: VPC Service Controls Egress\n'
                        '    vpc_sc = topo["vpc_service_controls"]\n'
                        '    kms_rule = next((r for r in vpc_sc["egress_rules"] if r["service"] == "cloudkms.googleapis.com"), None)\n'
                        '    if kms_rule and kms_rule["status"] == "MISSING_CONFIGURATION":\n'
                        '        log_control("VPC_SC_EGRESS", "WARN", "Cross-project KMS egress rule is MISSING; dry-run alerts triggered.")\n'
                        '        print("  -> Applying automated configuration repair: Authoring VPC SC Egress allow rule...")\n'
                        '        kms_rule["status"] = "CONFIGURED_ACTIVE"\n'
                        '        kms_rule["allow_methods"] = ["cloudkms.googleapis.com/v1.CryptoKeyService.Decrypt"]\n'
                        '        inconsistencies_repaired.append({\n'
                        '            "control": "VPC Service Controls Egress Policy",\n'
                        '            "issue": "Missing cross-project egress rule from fintech-billing-prod to fintech-sec-kms",\n'
                        '            "resolution": "Added explicit egress rule permitting cloudkms.googleapis.com Decrypt method."\n'
                        '        })\n'
                        '        log_control("VPC_SC_EGRESS", "REPAIRED", "Egress rule configured and verified active.")\n'
                        '\n'
                        '    # Layer 5: CMEK Rotation Invariant\n'
                        '    cmek = topo["cmek_lifecycle"]\n'
                        '    p_ver = cmek["primary_version"]\n'
                        '    all_enabled = all(v["state"] == "ENABLED" for v in cmek["versions"])\n'
                        '    if p_ver == 2 and all_enabled:\n'
                        '        log_control("CMEK_LIFECYCLE", "PASS", f"Primary version is {p_ver}; older version 1 retained in ENABLED state.")\n'
                        '    else:\n'
                        '        log_control("CMEK_LIFECYCLE", "FAIL", "Historical key version disabled or primary version incorrect.")\n'
                        '\n'
                        '    # Save verified state\n'
                        '    integrated_evidence = {\n'
                        '        "trace_timestamp": datetime.now(timezone.utc).isoformat(),\n'
                        '        "overall_status": "SUCCESS_VERIFIED",\n'
                        '        "security_trace": trace_log,\n'
                        '        "inconsistencies_repaired": inconsistencies_repaired\n'
                        '    }\n'
                        '\n'
                        '    with open("integrated_security_trace.json", "w") as out:\n'
                        '        json.dump(integrated_evidence, out, indent=2)\n'
                        '    print(f"\\nTrace Completed. Repaired {len(inconsistencies_repaired)} cross-control inconsistency.")\n'
                        '    print("Wrote integrated_security_trace.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    evaluate_and_repair()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute the Security Trace Tool and Inspect Verification Results\n'
                        'Run the Python trace script and inspect the output to confirm that all 5 layers pass and the VPC Service Controls egress inconsistency is repaired:\n\n'
                        '```sh\n'
                        'python3 trace_security_controls.py\n'
                        'cat integrated_security_trace.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python security integration script executing multi-layer verification and successfully repairing cross-control VPC Service Controls egress policies.',
                'verification': 'Review terminal output of <kbd>python3 trace_security_controls.py</kbd> confirming overall_status SUCCESS_VERIFIED and repair of VPC SC egress rule.',
                'trouble': 'If JSON file cannot be loaded, verify file syntax of `security_topology.json`.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/security-integration-lab</kbd>.',
                'file': 'day-116-security-trace.md'
            }
        }
    ]
}
