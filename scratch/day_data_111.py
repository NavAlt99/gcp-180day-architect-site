"""day_data_111.py — Exhaustive architecture data specification for Day 111.

Covers PCI-DSS Design (CDE Isolation, Tokenization, Network Segmentation),
HIPAA Design (Business Associate Agreement, PHI Handling, Audit Controls),
and Vendor / Third-Party Risk Management Basics.
"""

DAY_NUM = 111

DATA = {
    'day': 111,
    'part1_intro': (
        'Day 111 addresses the comprehensive systems architecture, network boundary isolation, and third-party supply '
        'chain governance required for regulated enterprise workloads on Google Cloud. Architects evaluate Cardholder Data '
        'Environment (CDE) scoping under PCI-DSS v4.0 (minimizing audit scope through iframe payment gateways and Cloud DLP '
        'tokenization), healthcare cloud architecture under HIPAA/HITECH (Business Associate Agreement execution, electronic '
        'Protected Health Information handling, and clinical audit sinks), and third-party vendor risk management (SaaS integration '
        'boundaries, reciprocal SOC 2 audits, and zero-trust Private Service Connect endpoints).'
    ),
    'exit_summary': (
        'Engineers author an Architecture Decision Record (ADR) for a regulated payment and healthcare ingestion platform, '
        'implement a declarative VPC Service Controls CDE network segmentation manifest, verify a clinical ePHI tokenization pipeline, '
        'and assemble an auditor-ready vendor risk assessment matrix fulfilling all Day 111 Exit evidence criteria.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts scope reduction techniques, isolation mechanisms, compliance boundaries, '
        'and audit evidence requirements across regulated enterprise payment, healthcare, and vendor architectures.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Regulated Architecture Pattern</th>\n'
        '<th>Scope Reduction Strategy</th>\n'
        '<th>Network &amp; Logical Boundary</th>\n'
        '<th>Mandatory Technical Safeguards</th>\n'
        '<th>Evidence for Compliance Examiner</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>PCI-DSS Cardholder Data Environment (CDE)</strong></td>\n'
        '<td>Third-party Hosted Fields / iFrames &amp; Cloud DLP Tokenization</td>\n'
        '<td>Dedicated VPC with VPC-SC perimeter; zero route to non-CDE corporate subnets</td>\n'
        '<td>Layer 7 Cloud NGFW IDS/IPS, multi-factor IAP admin access, daily log reviews</td>\n'
        '<td>Annual QSA Attestation of Compliance (AoC) &amp; quarterly ASV vulnerability scans</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>HIPAA Protected Health Information (ePHI)</strong></td>\n'
        '<td>De-identification &amp; pseudonymization before analytical processing</td>\n'
        '<td>Isolated Google Cloud project covered by signed BAA; restricted IAM access</td>\n'
        '<td>Cloud KMS CMEK encryption, Admin &amp; Data Access audit logs exported to locked GCS</td>\n'
        '<td>Executed Google Cloud BAA agreement, access policy matrices, and disaster recovery drills</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Third-Party Vendor SaaS Integration</strong></td>\n'
        '<td>Private Service Connect (PSC) &amp; API payload field redaction</td>\n'
        '<td>Unidirectional consumer/producer PSC endpoints; zero transitive VPC peering</td>\n'
        '<td>Vendor SOC 2 Type II audit review, mutual TLS client authentication, IP allowlists</td>\n'
        '<td>Vendor Security Risk Assessment (VSRA) register &amp; data processing addenda (DPAs)</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 111: Regulated Workload Architecture, CDE Scope Reduction, and Vendor Boundary Topology',
        'desc': 'Architectural layout illustrating PCI-DSS Cardholder Data Environment isolation, HIPAA ePHI processing with signed BAA, and zero-trust Private Service Connect vendor integration.',
        'caption': 'Figure 111.1: Regulated workload segmentation topology detailing PCI CDE perimeter isolation, HIPAA clinical vault governance, and Private Service Connect vendor boundaries.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Public Web Tier & Third-Party Hosted Payment Fields',
                'desc': 'Client browser interacting with third-party payment iframe; PAN bypasses merchant servers entirely',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Cardholder Data Environment (PCI CDE) Isolated Perimeter',
                'desc': 'Dedicated CDE project, VPC Service Controls perimeter, and Cloud NGFW Enterprise IDS/IPS inspection',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: HIPAA Clinical Vault & ePHI Processing Enclave',
                'desc': 'HIPAA-covered project under executed Google BAA, CMEK disk encryption, and Cloud DLP masking',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Vendor & SaaS Integration Boundary (Private Service Connect)',
                'desc': 'Zero-public-IP Private Service Connect (PSC) consumer endpoints connecting to audited third-party vendors',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: Regulatory Compliance Evidence & Immutable Audit Vault',
                'desc': 'Central compliance logging project, SEC 17a-4 locked storage buckets, and automated QSA audit sinks',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Payment iFrame Gateway', 'detail': 'SAQ-A Scope Reduction', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Cloud Armor Edge WAF', 'detail': 'OWASP Top 10 Mitigation', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'CDE Isolated VPC', 'detail': 'No Direct Internet Route', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Cloud NGFW Enterprise', 'detail': 'Layer 7 Threat Prevention', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Clinical ePHI Vault', 'detail': 'Covered by Google BAA', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'DLP Clinical Redactor', 'detail': 'De-Identifies Patient Records', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'PSC Consumer Endpoint', 'detail': '10.128.50.4 (Vendor NAT)', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Vendor Risk Gate', 'detail': 'Mutual TLS & mTLS Token', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Locked Audit Log Sink', 'detail': '365-Day Retention Lock', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'QSA Compliance Portal', 'detail': 'Continuous Posture Evidence', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'PUBLIC INGRESS & PAYMENT SCOPE REDUCTION', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'CARDHOLDER & CLINICAL REGULATED WORKLOAD ENCLAVE', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'THIRD-PARTY VENDOR INTEGRATION & AUDIT EVIDENCE', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Filter Ingress Threats', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Forward Tokenized Order', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Inspect L7 CDE Traffic', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Route Clinical Data', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Redact Patient Identifiers', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Forward to Third Party', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Enforce mTLS & PSC Policy', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Export Immutable Telemetry', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Verify Audit Compliance', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: CDE Network Perimeter Isolation & Route Audit', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: HIPAA BAA Verification & Data Access Audit Check', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 345, 'label': 'PROBE 3: Third-Party PSC Ingress/Egress Authorization', 'badge': 'P3', 'color': '#f43f5e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world regulated architecture failures, improper CDE scope expansion, '
        'unencrypted clinical health data ingestion, and third-party vendor supply chain breaches. Each scenario details verbatim '
        'diagnostic findings, root causes, remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on exercises execute the complete 8-stage operational engineering lifecycle for Day 111. '
        'Architects construct declarative CDE network segmentation policies, implement a clinical ePHI tokenization and '
        'audit verification script, and build a third-party vendor risk assessment matrix.'
    ),
    'topics': [
        {
            'key': 'topic-01',
            'title': 'PCI-DSS design',
            'overview': (
                'Designing architectures for PCI-DSS v4.0 requires minimizing the Cardholder Data Environment (CDE) scope to '
                'the smallest possible footprint. Scope reduction is achieved by utilizing hosted fields, iFrames, and third-party '
                'tokenization gateways so that raw Primary Account Numbers (PANs) never touch merchant servers, qualifying the workload '
                'for SAQ A. For components that must process payments, architects enforce strict network segmentation via VPC Service '
                'Controls, zero transitive routing to corporate networks, Cloud NGFW Layer 7 inspection, and end-to-end CMEK encryption.'
            ),
            'preview': (
                'A developer connects a test analytics pipeline directly into the payment processing database; the entire analytics '
                'cluster is immediately brought into PCI audit scope until strict VPC-SC perimeter isolation is restored.'
            ),
            'technical': (
                '### 1. PCI Scope Reduction Architectures\n'
                '- **SAQ A Architecture:** Customer browser enters credit card data directly into a third-party tokenization iframe '
                '(e.g. Stripe Elements, Adyen). The merchant\'s GCP backend receives only an opaque surrogate token. Merchant servers '
                'never store, process, or transmit cardholder data, reducing audit scope by 95%.\n'
                '- **SAQ A-EP Architecture:** Merchant serves the payment page but uses client-side JavaScript to send data directly '
                'to payment processor. Requires rigorous web application firewall (Cloud Armor) inspection and script integrity monitoring.\n'
                '\n'
                '### 2. CDE Network Segmentation & Hardening (PCI v4.0 Req 1 & 3)\n'
                '- **Isolated VPC:** CDE workloads must reside in a dedicated Google Cloud project with a standalone VPC. Default networks '
                'and external IP addresses are strictly prohibited.\n'
                '- **Egress Filtering:** All outbound traffic must pass through a Cloud Secure Web Proxy with FQDN whitelisting restricted '
                'exclusively to authorized payment processor endpoints.\n'
                '- **CMEK Encryption:** Persistent disks and Cloud Storage buckets storing encrypted cardholder tokens must use dedicated '
                'Cloud KMS keys backed by Cloud HSM (FIPS 140-2 Level 3).'
            ),
            'questions': [
                'How does utilizing hosted payment iframes reduce an enterprise\'s PCI-DSS compliance scope from SAQ D to SAQ A?',
                'What network controls must be implemented to prove that a non-CDE subnet cannot communicate with the CDE under PCI v4.0?',
                'Why does PCI-DSS v4.0 mandate multi-factor authentication (MFA) for all administrative access to the CDE?'
            ],
            'reference': 'https://cloud.google.com/security/compliance/pci-dss',
            'reference_label': 'Google Cloud PCI-DSS Compliance: Architecture guide and shared responsibility matrix',
            'scenario': {
                'symptom': 'External QSA assessment identifies unauthorized VPC peering between the corporate data warehouse and the Cardholder Data Environment, expanding audit scope to 300 non-compliant VMs.',
                'constraints': 'Financial transactions must process uninterrupted; corporate analytics must receive sanitized transaction metrics without entering CDE scope.',
                'evidence': (
                    'Network routing table audit log snippet:\n\n'
                    '```text\n'
                    'Peering Connection: cde-to-analytics-peering\n'
                    'Network A: cde-production-vpc (10.200.0.0/16)\n'
                    'Network B: corporate-analytics-vpc (10.100.0.0/16)\n'
                    'State: ACTIVE (Transitive IP routing enabled)\n'
                    'QSA Audit Violation: Requirement 1.2.3 - Direct connection between CDE and non-CDE corporate networks.\n'
                    'Impact: Entire 300-VM corporate analytics cluster pulled into full PCI-DSS Level 1 assessment scope.\n'
                    '```\n\n'
                    'Analysis: Data engineers peered the VPCs to allow direct JDBC database queries, violating strict PCI network isolation rules.'
                ),
                'diagnostic_steps': [
                    'Inspect VPC peering connections using <kbd>gcloud compute networks peerings list</kbd>.',
                    'Trace active routes between CDE subnets and corporate analytical networks.',
                    'Check for direct IP communication using VPC Flow Logs.',
                    'Evaluate Private Service Connect (PSC) or Cloud Pub/Sub as compliant decoupled alternatives.'
                ],
                'root': 'VPC peering violated network segmentation mandates, allowing bidirectional IP routability between CDE and corporate networks.',
                'fix': 'Tear down VPC peering immediately; deploy Private Service Connect with strict proxy boundaries to export only tokenized data.',
                'verify': 'Confirm zero routes exist between corporate network and CDE; verify QSA re-assessment acknowledges scope reduction.',
                'residual': 'Analytical teams requiring transaction metrics must ingest asynchronously via unidirectional tokenized message queues.',
                'diagram': (
                    'Engineers peer corporate analytics VPC with production CDE network',
                    'Direct IP routing violates PCI-DSS Requirement 1 segmentation',
                    'QSA expands CDE audit scope to include 300 corporate analytics VMs',
                    'Delete peering; enforce Private Service Connect and tokenized queues',
                    'CDE isolation restored; non-CDE systems eliminated from PCI scope'
                )
            },
            'lab': {
                'name': 'PCI CDE Network Segmentation & Scope Isolator',
                'goal': 'Author declarative Terraform manifests establishing an isolated Cardholder Data Environment VPC with deny-all egress and test a Python segmentation validator.',
                'expected': 'Validated Terraform CDE network configuration and working Python script proving complete isolation from non-CDE subnets.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Python 3 and Terraform installed.',
                'preflight': 'Establish working directory `~/pci-cde-lab`.',
                'steps': [
                    (
                        '#### Declarative PCI CDE Network Terraform Architecture\n'
                        'Author a dedicated CDE VPC with strict deny-by-default firewall rules:\n\n'
                        '```sh\n'
                        'mkdir -p ~/pci-cde-lab && cd ~/pci-cde-lab\n'
                        'cat <<\'EOF\' > cde_network.tf\n'
                        'resource "google_compute_network" "cde_vpc" {\n'
                        '  name                    = "pci-cde-isolated-vpc"\n'
                        '  auto_create_subnetworks = false\n'
                        '  description             = "Dedicated Cardholder Data Environment with zero default routing"\n'
                        '}\n'
                        '\n'
                        'resource "google_compute_subnetwork" "cde_subnet" {\n'
                        '  name                     = "cde-processing-subnet"\n'
                        '  ip_cidr_range            = "10.240.0.0/24"\n'
                        '  region                   = "us-central1"\n'
                        '  network                  = google_compute_network.cde_vpc.id\n'
                        '  private_ip_google_access = true\n'
                        '}\n'
                        '\n'
                        '# Strict Deny All Ingress from Non-CDE\n'
                        'resource "google_compute_firewall" "cde_deny_all_ingress" {\n'
                        '  name      = "cde-deny-all-ingress"\n'
                        '  network   = google_compute_network.cde_vpc.name\n'
                        '  priority  = 65534\n'
                        '  direction = "INGRESS"\n'
                        '  deny {\n'
                        '    protocol = "all"\n'
                        '  }\n'
                        '  source_ranges = ["0.0.0.0/0"]\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored cde_network.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### CDE Segmentation Validator\n'
                        'Author and run Python script verifying network isolation and blocking unauthorized cross-boundary routes:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > test_cde_segmentation.py\n'
                        'import ipaddress\n'
                        '\n'
                        'CDE_SUBNET = ipaddress.ip_network("10.240.0.0/24")\n'
                        'CORPORATE_SUBNET = ipaddress.ip_network("10.100.0.0/16")\n'
                        '\n'
                        'simulated_routes = [\n'
                        '    {"src": "10.240.0.5", "dst": "199.36.153.4", "desc": "Restricted Google API VIP", "allowed": True},\n'
                        '    {"src": "10.240.0.5", "dst": "10.100.4.12", "desc": "Corporate Data Warehouse", "allowed": False}, # VIOLATION\n'
                        '    {"src": "10.100.4.12", "dst": "10.240.0.5", "desc": "Corporate Ingress into CDE", "allowed": False}, # VIOLATION\n'
                        '    {"src": "35.235.240.10", "dst": "10.240.0.5", "desc": "IAP Admin Bastion Tunnel", "allowed": True}\n'
                        ']\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("PCI-DSS v4.0 CDE NETWORK SEGMENTATION AUDITOR")\n'
                        'print("================================================================")\n'
                        '\n'
                        'for r in simulated_routes:\n'
                        '    src_ip = ipaddress.ip_address(r["src"])\n'
                        '    dst_ip = ipaddress.ip_address(r["dst"])\n'
                        '\n'
                        '    # Evaluate segmentation rule: No route between CDE and Corporate subnets\n'
                        '    is_peered_violation = (\n'
                        '        (src_ip in CDE_SUBNET and dst_ip in CORPORATE_SUBNET) or\n'
                        '        (src_ip in CORPORATE_SUBNET and dst_ip in CDE_SUBNET)\n'
                        '    )\n'
                        '\n'
                        '    status = "BLOCKED (PCI Compliant)" if is_peered_violation else "PERMITTED"\n'
                        '    print(f"[{status:24s}] Route: {r[\'src\']:15s} -> {r[\'dst\']:15s} ({r[\'desc\']})")\n'
                        '    if is_peered_violation:\n'
                        '        assert not r["allowed"], "Segmentation test failed: unauthorized cross-boundary route allowed!"\n'
                        '\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 test_cde_segmentation.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform CDE isolation configuration and Python simulation verifying complete blocking of corporate cross-boundary routes.',
                'verification': 'Review terminal output of <kbd>python3 test_cde_segmentation.py</kbd> confirming corporate routes are strictly blocked.',
                'trouble': 'If corporate routes are permitted, verify subnet address range calculations.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/pci-cde-lab</kbd>.',
                'file': 'day-111-pci-segmentation.md'
            }
        },
        {
            'key': 'topic-02',
            'title': 'HIPAA design',
            'overview': (
                'Designing healthcare workloads under HIPAA (Health Insurance Portability and Accountability Act) and HITECH mandates '
                'requires strict adherence to the Security and Privacy Rules. In Google Cloud, architects must execute a formal Business '
                'Associate Agreement (BAA) covering all projects handling electronic Protected Health Information (ePHI). '
                'Key architectural requirements include restricting deployments exclusively to HIPAA-included services, enforcing '
                'CMEK encryption at rest, mandating TLS 1.3 in transit, enabling full Data Access audit logging, and implementing '
                'emergency break-glass procedures with immediate forensic auditing.'
            ),
            'preview': (
                'A hospital telemetry app logs patient vital signs and medical diagnoses; HIPAA guardrails enforce immediate masking '
                'of patient names and MRNs before records enter analytical BigQuery warehouses.'
            ),
            'technical': (
                '### 1. HIPAA Administrative & Technical Safeguards\n'
                '- **Business Associate Agreement (BAA):** A legally binding contract between Google Cloud and the customer. Google agrees '
                'to implement required administrative, physical, and technical safeguards. Customers must execute the BAA in Google Cloud '
                'Console **before** uploading any ePHI.\n'
                '- **HIPAA-Included Services:** Only services certified under Google Cloud\'s HIPAA assessment may store or process ePHI. '
                'Standard services (Compute Engine, GCS, BigQuery, Cloud SQL, Cloud Run) are included; experimental preview features '
                'are excluded.\n'
                '\n'
                '### 2. Clinical ePHI Access Controls & Audit Trails\n'
                '- **45 CFR § 164.312(b) Audit Controls:** Organizations must record and examine activity in systems that contain or use ePHI. '
                'Data Access audit logs (`DATA_READ`, `DATA_WRITE`) must be enabled and exported to locked storage.\n'
                '- **Minimum Necessary Standard:** Workforce members must only access the minimum ePHI necessary to accomplish their '
                'clinical or business function, enforced via Dataplex column-level policy tags and row-level access filters.'
            ),
            'questions': [
                'What is the legal consequence of storing Protected Health Information in a Google Cloud project before executing a BAA?',
                'How does an architect verify whether a newly announced Google Cloud service is approved for HIPAA workloads?',
                'How does the HIPAA "minimum necessary" standard translate into technical IAM and BigQuery access controls?'
            ],
            'reference': 'https://cloud.google.com/security/compliance/hipaa',
            'reference_label': 'Google Cloud HIPAA Compliance: Implementation guide, BAA terms, and included services',
            'scenario': {
                'symptom': 'Hospital internal compliance auditor flags 14,000 unencrypted patient clinical diagnostic notes stored in a public-read Google Cloud Storage bucket.',
                'constraints': 'Clinical staff require mobile access to patient updates, but HIPAA mandates zero public exposure and strict encryption at rest.',
                'evidence': (
                    'Cloud Storage bucket permission audit result:\n\n'
                    '```json\n'
                    '{\n'
                    '  "bucket_name": "hospital-clinical-notes-prod",\n'
                    '  "iam_policy": {\n'
                    '    "bindings": [\n'
                    '      {\n'
                    '        "role": "roles/storage.objectViewer",\n'
                    '        "members": ["allUsers"]\n'
                    '      }\n'
                    '    ]\n'
                    '  },\n'
                    '  "hipaa_violation": "45 CFR § 164.312(a)(1) - Failure to control access to ePHI",\n'
                    '  "potential_penalty": "Tier 4 Willful Neglect ($50,000 per violation up to annual maximum)"\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: A misconfigured Terraform module granted public read access to a clinical notes bucket, exposing patient records.'
                ),
                'diagnostic_steps': [
                    'Immediately remediate public access using <kbd>gcloud storage buckets set-iam-policy</kbd>.',
                    'Enable Organization Policy constraint `constraints/storage.publicAccessPrevention` on the folder.',
                    'Query Cloud Audit logs to determine if unauthorized IP addresses accessed patient notes.',
                    'Initiate mandatory 60-day HIPAA breach assessment and notification protocol.'
                ],
                'root': 'Public read IAM binding was applied to an ePHI bucket; absence of Organization Policy public access prevention allowed public exposure.',
                'fix': 'Enforce `publicAccessPrevention = "enforced"` on the bucket and parent organization; enforce CMEK encryption with Cloud HSM.',
                'verify': 'Attempt unauthenticated curl to bucket object (fails with HTTP 401/403); verify access is restricted exclusively to authorized clinical IAM identities.',
                'residual': 'All downloaded access logs must be retained for 6 years in an immutable WORM bucket to satisfy HIPAA documentation retention rules.',
                'diagram': (
                    'Developer accidentally grants allUsers read access to ePHI bucket',
                    'Unprotected patient clinical diagnostic records exposed to internet',
                    'Internal audit detects leak; triggers immediate HIPAA containment',
                    'Enforce Public Access Prevention; revoke all public IAM bindings',
                    'Bucket secured; access restricted strictly to authorized clinical staff'
                )
            },
            'lab': {
                'name': 'HIPAA ePHI Cloud Storage Hardening & Audit Enforcer',
                'goal': 'Author declarative Terraform configurations for HIPAA-compliant Cloud Storage buckets with Public Access Prevention and test a Python clinical de-identification script.',
                'expected': 'Validated Terraform HIPAA bucket manifest and working Python script proving patient identifier redaction before analytical ingestion.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Python 3 and Terraform installed.',
                'preflight': 'Establish working directory `~/hipaa-lab`.',
                'steps': [
                    (
                        '#### Declarative HIPAA Storage Bucket Terraform Architecture\n'
                        'Author a hardened Cloud Storage bucket enforcing Public Access Prevention and CMEK:\n\n'
                        '```sh\n'
                        'mkdir -p ~/hipaa-lab && cd ~/hipaa-lab\n'
                        'cat <<\'EOF\' > hipaa_bucket.tf\n'
                        'resource "google_storage_bucket" "clinical_vault" {\n'
                        '  name                        = "brightloaf-hipaa-clinical-vault-prod"\n'
                        '  location                    = "us-central1"\n'
                        '  uniform_bucket_level_access = true\n'
                        '  public_access_prevention    = "enforced" # Blocks public IAM grants\n'
                        '\n'
                        '  versioning {\n'
                        '    enabled = true\n'
                        '  }\n'
                        '\n'
                        '  encryption {\n'
                        '    default_kms_key_name = "projects/brightloaf-sec/locations/us-central1/keyRings/hipaa-ring/cryptoKeys/clinical-key"\n'
                        '  }\n'
                        '\n'
                        '  # 6-Year HIPAA Documentation Retention Policy\n'
                        '  retention_policy {\n'
                        '    retention_period = 189345600 # 6 years\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored hipaa_bucket.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### Clinical ePHI Redaction & De-Identification Engine\n'
                        'Author and run Python script simulating Safe Harbor de-identification of clinical patient records:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > test_hipaa_redaction.py\n'
                        'import hashlib\n'
                        'import re\n'
                        '\n'
                        'SALT = b"Hospital-Clinical-DeId-Salt-2026"\n'
                        '\n'
                        'clinical_records = [\n'
                        '    {\n'
                        '        "patient_name": "Eleanor Vance",\n'
                        '        "mrn": "MRN-849201",\n'
                        '        "dob": "1984-06-12",\n'
                        '        "diagnosis": "Type 2 Diabetes Mellitus",\n'
                        '        "notes": "Patient prescribed Metformin 500mg daily."\n'
                        '    },\n'
                        '    {\n'
                        '        "patient_name": "Thomas Dudley",\n'
                        '        "mrn": "MRN-109284",\n'
                        '        "dob": "1972-11-28",\n'
                        '        "diagnosis": "Essential Hypertension",\n'
                        '        "notes": "Follow-up blood pressure check scheduled in 4 weeks."\n'
                        '    }\n'
                        ']\n'
                        '\n'
                        'def deidentify_hipaa_record(record: dict) -> dict:\n'
                        '    # HIPAA Safe Harbor: Remove Name, MRN, exact DOB -> replace with age range and pseudonym\n'
                        '    pseudo_id = "PATIENT-" + hashlib.sha256(record["mrn"].encode() + SALT).hexdigest()[:12].upper()\n'
                        '    birth_year = record["dob"].split("-")[0]\n'
                        '    return {\n'
                        '        "patient_pseudonym": pseudo_id,\n'
                        '        "birth_year": birth_year,\n'
                        '        "diagnosis": record["diagnosis"],\n'
                        '        "clinical_notes": record["notes"]\n'
                        '    }\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("HIPAA SAFE HARBOR ePHI CLINICAL DE-IDENTIFICATION")\n'
                        'print("================================================================")\n'
                        'for raw in clinical_records:\n'
                        '    deid = deidentify_hipaa_record(raw)\n'
                        '    print(f"Original: {raw[\'patient_name\']} (MRN: {raw[\'mrn\']}, DOB: {raw[\'dob\']})")\n'
                        '    print(f"Sanitized: {deid[\'patient_pseudonym\']} | Year: {deid[\'birth_year\']} | Condition: {deid[\'diagnosis\']}")\n'
                        '    print("----------------------------------------------------------------")\n'
                        '    assert "patient_name" not in deid\n'
                        '    assert "mrn" not in deid\n'
                        '    assert raw["mrn"] not in deid["patient_pseudonym"]\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 test_hipaa_redaction.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform HIPAA bucket configuration with public access prevention and Python script proving complete elimination of direct patient identifiers.',
                'verification': 'Review terminal output of <kbd>python3 test_hipaa_redaction.py</kbd> confirming patient names and MRNs are removed from output records.',
                'trouble': 'If direct identifiers remain, verify dictionary key exclusions.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/hipaa-lab</kbd>.',
                'file': 'day-111-hipaa-architecture.md'
            }
        },
        {
            'key': 'topic-03',
            'title': 'Vendor and third-party risk basics',
            'overview': (
                'Modern enterprise cloud architectures rely heavily on third-party SaaS integrations, external APIs, and managed '
                'service providers, creating substantial supply chain risk. Vendor and third-party risk management (TPRM) requires '
                'establishing formal governance boundaries: conducting vendor security assessments (VSRAs), reviewing reciprocal '
                'SOC 2 Type II and ISO 27001 reports, enforcing data processing addenda (DPAs) with strict audit clauses, and implementing '
                'zero-trust network integration patterns such as Private Service Connect (PSC) to prevent vendor lateral movement into corporate VPCs.'
            ),
            'preview': (
                'A third-party marketing SaaS is breached by ransomware; Private Service Connect isolation ensures the attacker cannot '
                'pivot across the integration endpoint into the enterprise production network.'
            ),
            'technical': (
                '### 1. Zero-Trust Vendor Network Integration\n'
                '- **The Anti-Pattern (VPC Peering):** Peering directly with a third-party vendor\'s VPC creates bidirectional IP routing, '
                'extending the enterprise blast radius into the vendor\'s infrastructure.\n'
                '- **The Secure Pattern (Private Service Connect):** Consumes vendor-managed services privately using a local forwarder '
                'IP (e.g. `10.128.50.4`). PSC provides unidirectional Layer 4 TCP connection proxying with zero IP routing between VPCs. '
                'The vendor cannot initiate connections into the consumer network.\n'
                '\n'
                '### 2. Vendor Security Risk Assessment (VSRA) Framework\n'
                '- **Assessment Criteria:** Data classification shared with vendor, SOC 2 Type II report scope and unqualified opinion, '
                'encryption at rest and in transit standards, incident notification SLAs (e.g. 24–72 hours), and employee background screening.\n'
                '- **Continuous Monitoring:** Annual reassessment of vendor posture and monitoring of vendor breach disclosures.'
            ),
            'questions': [
                'Why is Private Service Connect (PSC) vastly superior to VPC Peering for integrating third-party vendor SaaS solutions?',
                'What are the mandatory legal clauses that must be included in a third-party vendor Data Processing Addendum (DPA)?',
                'How does an enterprise architect evaluate an external vendor\'s SOC 2 Type II report to identify material control deficiencies?'
            ],
            'reference': 'https://cloud.google.com/vpc/docs/private-service-connect',
            'reference_label': 'Google Cloud Private Service Connect: Secure third-party service integration and publishing',
            'scenario': {
                'symptom': 'Security Operations Center detects suspicious outbound API calls streaming customer demographic profiles to an unvetted third-party analytics provider.',
                'constraints': 'Enterprise TPRM policy mandates that all third-party data transfers must be authorized by the Vendor Risk Committee and covered by a formal DPA.',
                'evidence': (
                    'Cloud NGFW egress log capturing unauthorized vendor traffic:\n\n'
                    '```json\n'
                    '{\n'
                    '  "connection": {\n'
                    '    "src_ip": "10.128.0.42",\n'
                    '    "dest_ip": "198.51.100.89",\n'
                    '    "dest_port": 443,\n'
                    '    "protocol": 6\n'
                    '  },\n'
                    '  "fqdn": "telemetry-collector.unvetted-saas-vendor.io",\n'
                    '  "bytes_sent": 48210920,\n'
                    '  "tprm_status": "UNAPPROVED_VENDOR_TRANSFER"\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: A marketing engineering team integrated a free analytics software development kit (SDK) into the frontend, '
                    'which silently streamed user data to an external SaaS vendor without security review.'
                ),
                'diagnostic_steps': [
                    'Review Cloud Secure Web Proxy logs to identify all outbound connections to `unvetted-saas-vendor.io`.',
                    'Search corporate vendor registry to confirm absence of executed DPA or SOC 2 review.',
                    'Inspect application source code and dependencies for unapproved third-party SDKs.',
                    'Block vendor domain immediately via Cloud Secure Web Proxy and Cloud DNS Firewall policies.'
                ],
                'root': 'Engineering integrated an unvetted third-party SDK, bypassing the Vendor Security Risk Assessment and legal DPA process.',
                'fix': 'Block outbound traffic to the vendor domain, remove the SDK from application code, and submit the vendor to formal TPRM evaluation.',
                'verify': 'Verify SWP logs confirm zero traffic reaching the vendor domain; confirm application builds pass automated software bill of materials (SBOM) scanning.',
                'residual': 'Historical data sent to the unvetted vendor must be formally requested for deletion under applicable privacy statutes.',
                'diagram': (
                    'Application integrates unvetted analytics SDK without security review',
                    'SDK streams customer profile telemetry to unapproved vendor SaaS',
                    'Cloud NGFW detects unauthorized transfer; SOC triggers security incident',
                    'Block vendor FQDN in Secure Web Proxy; remove SDK from code repository',
                    'Enforce CI/CD dependency gating; submit all third parties to formal TPRM'
                )
            },
            'lab': {
                'name': 'Vendor Security Risk Assessment & PSC Boundary Enforcer',
                'goal': 'Author a declarative Private Service Connect consumer endpoint manifest and implement a Python TPRM scoring engine evaluating third-party vendor risk profiles.',
                'expected': 'Terraform PSC configuration and functional Python TPRM scoring tool evaluating vendor security postures.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Python 3 and Terraform installed.',
                'preflight': 'Establish working directory `~/vendor-risk-lab`.',
                'steps': [
                    (
                        '#### Declarative Private Service Connect Terraform Architecture\n'
                        'Author a PSC endpoint connecting privately to an audited third-party service:\n\n'
                        '```sh\n'
                        'mkdir -p ~/vendor-risk-lab && cd ~/vendor-risk-lab\n'
                        'cat <<\'EOF\' > psc_vendor.tf\n'
                        'resource "google_compute_address" "psc_vendor_ip" {\n'
                        '  name         = "psc-audited-vendor-ip"\n'
                        '  subnetwork   = "projects/core-prod/regions/us-central1/subnetworks/app-subnet"\n'
                        '  address_type = "INTERNAL"\n'
                        '  region       = "us-central1"\n'
                        '}\n'
                        '\n'
                        'resource "google_compute_forwarding_rule" "psc_forwarder" {\n'
                        '  name                  = "psc-vendor-service-rule"\n'
                        '  region                = "us-central1"\n'
                        '  network               = "projects/core-prod/global/networks/app-vpc"\n'
                        '  ip_address            = google_compute_address.psc_vendor_ip.id\n'
                        '  target                = "projects/audited-vendor-prod/regions/us-central1/serviceAttachments/payment-gateway-service"\n'
                        '  load_balancing_scheme = ""\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored psc_vendor.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### Vendor Security Risk Assessment (TPRM) Scoring Engine\n'
                        'Author and run Python script evaluating third-party vendor risk questionnaires and SOC 2 attestations:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > evaluate_vendor_risk.py\n'
                        'vendor_profiles = [\n'
                        '    {\n'
                        '        "name": "CloudPay Global Gateway",\n'
                        '        "soc2_type2": True,\n'
                        '        "dpa_executed": True,\n'
                        '        "data_classification": "RESTRICTED",\n'
                        '        "network_pattern": "PSC_PRIVATE",\n'
                        '        "encryption_in_transit": "TLS_1_3"\n'
                        '    },\n'
                        '    {\n'
                        '        "name": "FastMetrics Free Analytics",\n'
                        '        "soc2_type2": False,\n'
                        '        "dpa_executed": False,\n'
                        '        "data_classification": "INTERNAL",\n'
                        '        "network_pattern": "PUBLIC_INTERNET",\n'
                        '        "encryption_in_transit": "TLS_1_2"\n'
                        '    }\n'
                        ']\n'
                        '\n'
                        'def score_vendor(v: dict) -> tuple[int, list[str]]:\n'
                        '    score = 100\n'
                        '    flags = []\n'
                        '    if not v["soc2_type2"]:\n'
                        '        score -= 40\n'
                        '        flags.append("Missing accredited SOC 2 Type II report")\n'
                        '    if not v["dpa_executed"]:\n'
                        '        score -= 30\n'
                        '        flags.append("No executed Data Processing Addendum (DPA)")\n'
                        '    if v["network_pattern"] != "PSC_PRIVATE" and v["data_classification"] in ["CONFIDENTIAL", "RESTRICTED"]:\n'
                        '        score -= 20\n'
                        '        flags.append("Sensitive data routed over public internet instead of PSC")\n'
                        '    return score, flags\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("THIRD-PARTY VENDOR SECURITY RISK ASSESSMENT (TPRM)")\n'
                        'print("================================================================")\n'
                        'for v in vendor_profiles:\n'
                        '    score, flags = score_vendor(v)\n'
                        '    decision = "APPROVED (Authorized Integration)" if score >= 80 else "REJECTED (High Supply Chain Risk)"\n'
                        '    print(f"Vendor: {v[\'name\']:26s} | Score: {score}/100 | Decision: {decision}")\n'
                        '    for f in flags:\n'
                        '        print(f"   -> RISK FLAG: {f}")\n'
                        '    print("----------------------------------------------------------------")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 evaluate_vendor_risk.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform Private Service Connect configuration and Python TPRM evaluation script accurately distinguishing approved from high-risk vendors.',
                'verification': 'Review terminal output of <kbd>python3 evaluate_vendor_risk.py</kbd> confirming CloudPay approved (100/100) and FastMetrics rejected (30/100).',
                'trouble': 'If score calculation is unexpected, inspect weighted scoring deduction logic.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/vendor-risk-lab</kbd>.',
                'file': 'day-111-vendor-risk.md'
            }
        }
    ]
}
