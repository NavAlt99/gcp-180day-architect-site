"""day_data_110.py — Exhaustive architecture data specification for Day 110.

Covers Assured Workloads (Compliance Regimes as Guardrails), Audit Logging Design (Admin Activity,
Data Access, Sinks to Locked Buckets), Policy as Code (Org Policy, Config Controller, Policy Controller / OPA Gatekeeper),
and Data Protection Regulations (Right to Erasure, Data Minimization, Breach Notification, DPA, SCCs).
"""

DAY_NUM = 110

DATA = {
    'day': 110,
    'part1_intro': (
        'Day 110 focuses on automated architectural governance, immutable audit logging, policy-as-code guardrails, '
        'and global data protection regulatory enforcement across Google Cloud. Architects evaluate Assured Workloads '
        'for programmatic compliance baseline provisioning, Cloud Audit Logging tiering (mandatory Admin Activity vs. '
        'selective Data Access), log sinks targeting locked, write-once-read-many (WORM) Cloud Storage buckets, '
        'declarative policy-as-code enforcement via Policy Controller (OPA/Gatekeeper) and Terraform static validation, '
        'and technical implementations of GDPR/CCPA mandates including the cryptographic right to erasure, data minimization, '
        'and 72-hour breach notification pipelines.'
    ),
    'exit_summary': (
        'Engineers design, execute, and verify a versioned policy-as-code OPA Gatekeeper constraint suite, an immutable '
        'Cloud Storage Bucket Lock audit retention sink with legal hold capabilities, an automated Data Access log cost optimizer, '
        'and a GDPR cryptographic erasure pipeline fulfilling all Day 110 Exit evidence criteria.'
    ),
    'part2_intro': (
        'The technical comparison below analyzes the operational characteristics, enforcement boundaries, audit durability, '
        'and compliance trade-offs across Google Cloud policy-as-code and audit governance architectures.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Governance Layer</th>\n'
        '<th>Enforcement Engine &amp; Standard</th>\n'
        '<th>Logical &amp; Physical Boundary</th>\n'
        '<th>Audit &amp; Retention Guarantee</th>\n'
        '<th>Failure Signal &amp; Operational Overhead</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>Assured Workloads</strong></td>\n'
        '<td>Automated Compliance Folders (FedRAMP, IL4, EU Sovereign)</td>\n'
        '<td>Folder hierarchy envelope with preconfigured Org Policies</td>\n'
        '<td>Continuous compliance monitoring; access transparency logs</td>\n'
        '<td>Restricts resource provisioning to compliant regions; non-compliant APIs disabled.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Cloud Audit Logging (Admin &amp; Data)</strong></td>\n'
        '<td>Cloud Logging Router (`cloudaudit.googleapis.com`)</td>\n'
        '<td>Project, folder, and organization-wide log sinks</td>\n'
        '<td>Admin Activity (400 days free, immutable); Data Access (30 days default)</td>\n'
        '<td>Unfiltered Data Access logs generate massive log volume and substantial storage charges.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Locked Bucket Sinks (WORM)</strong></td>\n'
        '<td>Cloud Storage Bucket Lock (SEC 17a-4 / FINRA 4511)</td>\n'
        '<td>Object retention policy locked permanently against deletion</td>\n'
        '<td>Mathematically immutable retention period; cannot be overridden even by Org Owner</td>\n'
        '<td>If retention period is set incorrectly, locked buckets cannot be deleted until period expires.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Policy Controller (OPA / Gatekeeper)</strong></td>\n'
        '<td>Kubernetes Admission Webhook &amp; Constraint Templates</td>\n'
        '<td>GKE admission control plane evaluating declarative Rego rules</td>\n'
        '<td>Admission audit logs and continuous background drift scans</td>\n'
        '<td>Non-compliant <kbd>kubectl apply</kbd> commands rejected pre-admission with descriptive Rego violation text.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Cryptographic Erasure (GDPR)</strong></td>\n'
        '<td>Per-User Envelope Encryption (DEK Shredding)</td>\n'
        '<td>User-specific Data Encryption Key stored in KMS or Secret Manager</td>\n'
        '<td>Instant irrecoverable shredding of DEK without rewriting petabyte-scale storage</td>\n'
        '<td>Destroying user DEK renders all user ciphertext permanently unrecoverable across backups.</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 110: Policy as Code, Immutable Audit Logging, and Data Protection Lifecycle Topology',
        'desc': 'Architectural layout illustrating Assured Workloads compliance envelopes, Cloud Audit Logging sinks to locked GCS buckets, Policy Controller admission webhooks, and cryptographic erasure pipelines.',
        'caption': 'Figure 110.1: Enterprise policy-as-code and compliance audit architecture featuring OPA Gatekeeper admission enforcement, immutable WORM log sinks, and GDPR cryptographic erasure.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Enterprise Organization & Assured Workloads Governance Envelope',
                'desc': 'Resource hierarchy folders, Assured Workloads compliance guardrails, and access transparency logs',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Policy as Code Admission & Static Validation Plane',
                'desc': 'Policy Controller (OPA Gatekeeper), Terraform Sentinel/Checkov static analysis, and admission webhooks',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Cloud Logging Router & Aggregated Audit Sink Plane',
                'desc': 'Cloud Audit logs filtering Admin Activity and Data Access, routing to central security logging project',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Immutable WORM Audit Vault (SEC 17a-4 Compliant Bucket Lock)',
                'desc': 'Cloud Storage bucket with locked retention policy and legal hold capabilities preserving tamper-proof evidence',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: Privacy Engineering & Cryptographic Right-to-Erasure Vault',
                'desc': 'Per-user DEK management, automated token shredding, and regulatory breach notification eventarc triggers',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Assured Workloads FedRAMP', 'detail': 'Sovereign Folder Boundary', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Access Transparency', 'detail': 'Google Admin Access Auditing', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'OPA Gatekeeper Controller', 'detail': 'K8s Admission Webhook', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Terraform Static Linter', 'detail': 'Pre-Apply Policy Validation', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Cloud Logging Router', 'detail': 'Aggregated Organization Sink', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Data Access Log Filter', 'detail': 'Cost-Optimized Inclusion', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Locked Storage Bucket', 'detail': 'SEC 17a-4 7-Year Retention', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Bucket Legal Hold Engine', 'detail': 'Litigation Freeze Capability', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Per-User DEK Vault', 'detail': 'Key Shredding on Erasure', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'Breach Eventarc Pipeline', 'detail': '72h Notification Automation', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'SOVEREIGNTY & POLICY-AS-CODE CONTROL PLANE', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'AUDIT TELEMETRY & IMMUTABLE RETENTION VAULT', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'DATA PRIVACY & REGULATORY ERASURE LIFECYCLE', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Audit Support Actions', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Enforce Rego Constraint', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Intercept Non-Compliant IaC', 'type': 'fail'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Stream Audit Events', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Filter High-Volume Reads', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Persist to WORM Storage', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Enforce Immutable Hold', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Trigger GDPR Deletion', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Notify Privacy Regulator', 'type': 'warn'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: OPA Gatekeeper Admission Intercept & Rego Error', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 345, 'label': 'PROBE 2: GCS Retention Policy Immutability & Overwrite Block', 'badge': 'P2', 'color': '#f43f5e'},
            {'cx': 80, 'cy': 450, 'label': 'PROBE 3: Cryptographic Key Shredding & Ciphertext Unrecoverability', 'badge': 'P3', 'color': '#22c55e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world policy enforcement bypasses, audit logging cost explosions, '
        'premature log purge incidents under legal discovery, and incomplete GDPR data erasure penalties. Each scenario details '
        'verbatim terminal output, root cause mechanisms, production remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on exercises execute the complete 8-stage operational engineering lifecycle for Day 110. '
        'Architects author OPA Gatekeeper constraint templates and constraints, construct declarative Cloud Storage Bucket Lock '
        'retention manifests, build an audit log cost filter, and implement a Python cryptographic erasure pipeline.'
    ),
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Assured Workloads (compliance regimes as guardrails)',
            'overview': (
                'Assured Workloads enables enterprise organizations to automatically apply and maintain security and compliance '
                'controls on Google Cloud without compromising developer agility. By selecting a target compliance regime '
                '(e.g. FedRAMP Moderate/High, CJIS, IL4, EU Regions and Support, FreeTrial), Assured Workloads provisions '
                'a dedicated folder hierarchy preconfigured with authoritative Organization Policy guardrails, restrictive '
                'personnel access controls, and Key Access Justifications, continuously monitoring the environment for drift.'
            ),
            'preview': (
                'A developer attempts to attach an unapproved third-party service to a regulated defense project; Assured Workloads '
                'guardrails immediately terminate API calls with a compliance violation notification.'
            ),
            'technical': (
                '### 1. Assured Workloads Architectural Mechanics\n'
                '- **Folder-Level Boundary:** Compliance regimes are instantiated at the Folder level in the Google Cloud resource '
                'hierarchy. All projects provisioned within this folder inherit the compliance constraints automatically.\n'
                '- **Core Guardrail Policies Enforced:**\n'
                '  - `constraints/gcp.resourceLocations`: Restricts resources strictly to certified sovereign geographical regions.\n'
                '  - `constraints/gcp.restrictServiceUsage`: Disables Google Cloud services that have not achieved the required compliance accreditation.\n'
                '  - `constraints/gcp.restrictCmekCryptoKeyProjects`: Mandates that all data encryption keys reside in certified customer-managed KMS projects.\n'
                '\n'
                '### 2. Personnel Controls & Access Transparency\n'
                '- Enforces that Google Support engineers accessing underlying infrastructure possess required security clearances '
                '(e.g. US Persons for FedRAMP/ITAR, EU citizenship for EU Sovereign Cloud).\n'
                '- **Access Transparency:** Logs every single Google administrator access event to customer infrastructure, including '
                'justification, employee ID, and accessed resource.'
            ),
            'questions': [
                'How does Assured Workloads enforce compliance regimes programmatically through Google Cloud Organization Policies?',
                'What is the operational function of Access Transparency in an Assured Workloads environment?',
                'Why can certain standard Google Cloud services not be provisioned inside an Assured Workloads FedRAMP High folder?'
            ],
            'reference': 'https://cloud.google.com/assured-workloads/docs/overview',
            'reference_label': 'Google Cloud Assured Workloads: Compliance regimes, folder boundaries, and sovereign controls',
            'scenario': {
                'symptom': 'Infrastructure team attempts to enable Vertex AI in a defense analytics project and receives `FAILED_PRECONDITION: Service is restricted by Assured Workloads policy`.',
                'constraints': 'Project operates under FedRAMP High compliance; uncertified machine learning APIs must be prevented from accessing sensitive defense telemetry.',
                'evidence': (
                    'Service Usage API error payload:\n\n'
                    '```json\n'
                    '{\n'
                    '  "error": {\n'
                    '    "code": 400,\n'
                    '    "message": "Operation denied by Assured Workloads guardrail constraint constraints/gcp.restrictServiceUsage.",\n'
                    '    "details": [\n'
                    '      {\n'
                    '        "@type": "type.googleapis.com/google.rpc.PreconditionFailure",\n'
                    '        "violations": [\n'
                    '          {\n'
                    '            "type": "gcp.restrictServiceUsage",\n'
                    '            "subject": "aiplatform.googleapis.com",\n'
                    '            "description": "Service aiplatform.googleapis.com is not compliant with regime FEDRAMP_HIGH."\n'
                    '          }\n'
                    '        ]\n'
                    '      }\n'
                    '    ]\n'
                    '  }\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: Assured Workloads enforces a strict allowlist of accredited APIs, blocking uncertified services at the control plane.'
                ),
                'diagnostic_steps': [
                    'Review active Assured Workloads compliance dashboard in Google Cloud Console.',
                    'Check the official Google Cloud FedRAMP High compliant services catalog.',
                    'Inspect Organization Policy constraint <kbd>gcloud org-policies describe constraints/gcp.restrictServiceUsage</kbd>.',
                    'Evaluate compliant alternative architectures (e.g. self-hosted models on certified GCE instances).'
                ],
                'root': 'The requested service was not accredited under the FedRAMP High compliance regime, triggering control-plane rejection.',
                'fix': 'Deploy the machine learning workload on certified Compute Engine instances using hardened, approved container images.',
                'verify': 'Confirm project remains 100% compliant in Assured Workloads compliance dashboard with zero policy violations.',
                'residual': 'Regime service updates occur quarterly; newly accredited services require updating Organization Policy allowlists.',
                'diagram': (
                    'DevOps attempts to enable unaccredited AI API in FedRAMP folder',
                    'Assured Workloads evaluates constraints/gcp.restrictServiceUsage',
                    'Service not on FedRAMP High allowlist; API call denied with 400 error',
                    'Refactor architecture to use accredited GCE instances with hardened OS',
                    'Workload executes compliantly; zero FedRAMP High boundary violations'
                )
            },
            'lab': {
                'name': 'Assured Workloads Compliance Guardrail Modeling',
                'goal': 'Author declarative Organization Policy constraints simulating Assured Workloads service restrictions and test a Python compliance validator.',
                'expected': 'Terraform Org Policy manifest and Python compliance engine verifying service usage allowlists.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Python 3 and Terraform installed.',
                'preflight': 'Establish working directory `~/assured-workloads-lab`.',
                'steps': [
                    (
                        '#### Declarative Service Restriction Org Policy\n'
                        'Author a Terraform configuration declaring an Assured Workloads service usage allowlist:\n\n'
                        '```sh\n'
                        'mkdir -p ~/assured-workloads-lab && cd ~/assured-workloads-lab\n'
                        'cat <<\'EOF\' > service_guardrail.tf\n'
                        'resource "google_folder" "fedramp_folder" {\n'
                        '  display_name = "FedRAMP-High-Regulated-Folder"\n'
                        '  parent       = "organizations/108420918237"\n'
                        '}\n'
                        '\n'
                        'resource "google_folder_organization_policy" "restrict_services" {\n'
                        '  folder     = google_folder.fedramp_folder.name\n'
                        '  constraint = "constraints/gcp.restrictServiceUsage"\n'
                        '\n'
                        '  list_policy {\n'
                        '    allow {\n'
                        '      values = [\n'
                        '        "compute.googleapis.com",\n'
                        '        "storage.googleapis.com",\n'
                        '        "bigquery.googleapis.com",\n'
                        '        "cloudkms.googleapis.com"\n'
                        '      ]\n'
                        '    }\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored service_guardrail.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### Assured Workloads Service Validator\n'
                        'Author and run Python script evaluating API enablement requests against FedRAMP allowlists:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > validate_regime_services.py\n'
                        'FEDRAMP_ALLOWLIST = {\n'
                        '    "compute.googleapis.com",\n'
                        '    "storage.googleapis.com",\n'
                        '    "bigquery.googleapis.com",\n'
                        '    "cloudkms.googleapis.com",\n'
                        '    "logging.googleapis.com"\n'
                        '}\n'
                        '\n'
                        'requested_apis = [\n'
                        '    {"service": "compute.googleapis.com", "caller": "ci-deployer", "env": "FedRAMP-High"},\n'
                        '    {"service": "bigquery.googleapis.com", "caller": "analyst-lead", "env": "FedRAMP-High"},\n'
                        '    {"service": "translate.googleapis.com", "caller": "app-dev", "env": "FedRAMP-High"}, # VIOLATION\n'
                        '    {"service": "aiplatform.googleapis.com", "caller": "ml-engineer", "env": "FedRAMP-High"} # VIOLATION\n'
                        ']\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("ASSURED WORKLOADS: PROGRAMMATIC API GUARDRAIL VALIDATOR")\n'
                        'print("================================================================")\n'
                        'for req in requested_apis:\n'
                        '    svc = req["service"]\n'
                        '    is_compliant = svc in FEDRAMP_ALLOWLIST\n'
                        '    status = "ALLOWED (Compliant Service)" if is_compliant else "BLOCKED (Guardrail Violation)"\n'
                        '    print(f"[{status:28s}] Service: {svc:26s} | Caller: {req[\'caller\']}")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 validate_regime_services.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform Org Policy configuration and Python script verifying deterministic blocking of unaccredited APIs.',
                'verification': 'Review terminal output of <kbd>python3 validate_regime_services.py</kbd> confirming translate and aiplatform APIs are blocked.',
                'trouble': 'If approved APIs are blocked, verify service name exact matches in FEDRAMP_ALLOWLIST set.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/assured-workloads-lab</kbd>.',
                'file': 'day-110-assured-workloads.md'
            }
        },
        {
            'key': 'topic-02',
            'title': 'Audit logging design',
            'overview': (
                'Enterprise security architecture relies on immutable, high-fidelity audit logging to satisfy regulatory mandates '
                'and forensic investigation needs. Google Cloud Audit Logging provides four distinct categories: Admin Activity '
                '(always on, free, immutable for 400 days), Data Access (logs read/write calls to customer data; disabled by default '
                'due to volume), System Event (automated Google administrative actions), and Policy Denied (security policy violations). '
                'Architects must structure aggregated organization log sinks targeting locked, tamper-proof Cloud Storage buckets '
                'to meet SEC 17a-4 and FINRA compliance requirements.'
            ),
            'preview': (
                'A malicious cloud administrator deletes an analytical database table; Admin Activity audit logs capture their '
                'caller identity, source IP, and timestamp in an immutable write-once sink.'
            ),
            'technical': (
                '### 1. Cloud Audit Log Categories & Cost Engineering\n'
                '- **Admin Activity Logs:** Captures all configuration changes, resource creations, updates, and deletions. Always enabled, '
                'stored for 400 days at zero cost; cannot be disabled by any user or organization policy.\n'
                '- **Data Access Logs:** Divided into `ADMIN_READ` (reading resource metadata), `DATA_READ` (reading customer data, '
                'e.g. `storage.objects.get`, `BigQuery SELECT`), and `DATA_WRITE` (writing data). Incurs standard Cloud Logging ingestion '
                'charges ($0.50/GiB beyond free allocation). Must be enabled selectively to prevent budget depletion.\n'
                '\n'
                '### 2. Immutable Log Sinks & Bucket Lock (WORM)\n'
                '- **Aggregated Sinks:** Configured at the Organization or Folder level with `include_children = true` to capture all '
                'events across all current and future projects.\n'
                '- **Bucket Lock (SEC Rule 17a-4):** Sinks export logs to a dedicated Cloud Storage bucket configured with an immutable '
                'retention policy (e.g. 7 years). Once the Bucket Lock is locked, no identity—including project owners or Google support—can '
                'delete or overwrite log files until the retention duration expires.'
            ),
            'questions': [
                'Why are Admin Activity audit logs enabled by default across all Google Cloud projects without incurring storage charges?',
                'What is the architectural risk of enabling Data Access DATA_READ logs globally across an entire organization?',
                'How does Cloud Storage Bucket Lock provide write-once-read-many (WORM) regulatory compliance for financial audit trails?'
            ],
            'reference': 'https://cloud.google.com/logging/docs/audit',
            'reference_label': 'Google Cloud Logging: Cloud Audit Logs architecture and best practices',
            'scenario': {
                'symptom': 'Monthly Google Cloud billing invoice reveals a $38,000 unexpected charge for Cloud Logging ingestion.',
                'constraints': 'Compliance team requires audit trails for sensitive customer tables, but telemetry costs must remain within budget.',
                'evidence': (
                    'Billing breakdown analysis by log name:\n\n'
                    '```text\n'
                    'Log Name: cloudaudit.googleapis.com/data_access\n'
                    'Service: storage.googleapis.com (Method: storage.objects.get)\n'
                    'Ingested Volume: 76,000 GiB in 14 days\n'
                    'Cost: 76,000 GiB * $0.50/GiB = $38,000.00\n'
                    'Root Cause: Data Access DATA_READ was enabled globally on a high-throughput image asset bucket serving 50M requests/day.\n'
                    '```\n\n'
                    'Analysis: Administrators applied a broad organization-level IAM audit configuration enabling `DATA_READ` on Cloud Storage, '
                    'logging every static CDN asset read.'
                ),
                'diagnostic_steps': [
                    'Query Cloud Monitoring metric `logging.googleapis.com/byte_count` grouped by `service_name` and `method_name`.',
                    'Inspect organization-level audit log configuration using <kbd>gcloud organizations get-iam-policy</kbd>.',
                    'Identify buckets with high read volume that do not contain regulated Restricted data.',
                    'Author an audit exclusion filter to drop public asset bucket read logs before ingestion.'
                ],
                'root': 'Data Access DATA_READ logs were enabled globally across all Cloud Storage buckets instead of targeting sensitive data repositories.',
                'fix': 'Disable global Cloud Storage DATA_READ logging; scope Data Access logging explicitly to sensitive datasets, and configure log sink exclusion filters.',
                'verify': 'Verify daily Cloud Logging byte count drops by 98%; confirm Admin Activity and sensitive BigQuery audit logs continue recording.',
                'residual': 'Audit log exclusions prevent ingestion into Logging, so excluded events cannot be queried in Logs Explorer.',
                'diagram': (
                    'Global DATA_READ logging enabled on high-throughput asset bucket',
                    '50M static object reads generate 76TB of logs, driving $38k bill',
                    'Billing anomaly alert fires; security team investigates root cause',
                    'Scope Data Access logging strictly to sensitive buckets; apply exclusions',
                    'Logging bill normalized; sensitive audit requirements fully satisfied'
                )
            },
            'lab': {
                'name': 'Immutable Audit Log Sink & WORM Bucket Lock Architecture',
                'goal': 'Author declarative Terraform manifests establishing an aggregated audit log sink targeting an immutable Cloud Storage bucket with Bucket Lock, and test a Python WORM enforcement simulator.',
                'expected': 'Validated Terraform audit architecture and Python script demonstrating mathematical rejection of premature log deletion.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Python 3 and Terraform installed.',
                'preflight': 'Establish working directory `~/audit-sink-lab`.',
                'steps': [
                    (
                        '#### Declarative WORM Audit Storage Terraform Architecture\n'
                        'Author a Terraform configuration declaring an immutable Cloud Storage retention bucket and log sink:\n\n'
                        '```sh\n'
                        'mkdir -p ~/audit-sink-lab && cd ~/audit-sink-lab\n'
                        'cat <<\'EOF\' > audit_vault.tf\n'
                        'resource "google_storage_bucket" "audit_vault" {\n'
                        '  name                        = "brightloaf-immutable-audit-vault-prod"\n'
                        '  location                    = "US"\n'
                        '  uniform_bucket_level_access = true\n'
                        '\n'
                        '  # SEC 17a-4 / FINRA WORM Retention Policy (7 Years)\n'
                        '  retention_policy {\n'
                        '    is_locked        = true\n'
                        '    retention_period = 220752000 # 7 years in seconds\n'
                        '  }\n'
                        '}\n'
                        '\n'
                        'resource "google_logging_organization_sink" "sec_audit_sink" {\n'
                        '  name        = "org-compliance-audit-sink"\n'
                        '  org_id      = "108420918237"\n'
                        '  destination = "storage.googleapis.com/${google_storage_bucket.audit_vault.name}"\n'
                        '  filter      = "logName:\"logs/cloudaudit.googleapis.com%2Factivity\" OR (logName:\"logs/cloudaudit.googleapis.com%2Fdata_access\" AND protoPayload.serviceName=\"bigquery.googleapis.com\")"\n'
                        '\n'
                        '  include_children = true\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored audit_vault.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### WORM Bucket Lock Enforcement Simulator\n'
                        'Author and run Python script verifying immutable retention enforcement and deletion blocking:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > test_worm_retention.py\n'
                        'import time\n'
                        '\n'
                        'class LockedAuditVault:\n'
                        '    def __init__(self, retention_duration: int):\n'
                        '        self.retention_duration = retention_duration\n'
                        '        self.objects = {}\n'
                        '        self.legal_holds = {}\n'
                        '\n'
                        '    def put_audit_log(self, filename: str, payload: str):\n'
                        '        self.objects[filename] = {\n'
                        '            "payload": payload,\n'
                        '            "created_at": time.time(),\n'
                        '            "expires_at": time.time() + self.retention_duration\n'
                        '        }\n'
                        '        print(f"[STORE] Written: {filename} (Locked for {self.retention_duration}s)")\n'
                        '\n'
                        '    def delete_audit_log(self, filename: str, caller: str):\n'
                        '        if filename not in self.objects:\n'
                        '            raise FileNotFoundError(f"{filename} not found.")\n'
                        '        obj = self.objects[filename]\n'
                        '        current_time = time.time()\n'
                        '        if current_time < obj["expires_at"]:\n'
                        '            remaining = int(obj["expires_at"] - current_time)\n'
                        '            raise PermissionError(f"HTTP 403: Object retention policy active. Deletion prohibited for {remaining} more seconds.")\n'
                        '        if self.legal_holds.get(filename, False):\n'
                        '            raise PermissionError("HTTP 403: Legal Hold active. Deletion blocked.")\n'
                        '        del self.objects[filename]\n'
                        '        print(f"[DELETE] Log purged after retention expiration.")\n'
                        '\n'
                        'vault = LockedAuditVault(retention_duration=86400) # 24h retention simulation\n'
                        'print("================================================================")\n'
                        'print("CLOUD STORAGE BUCKET LOCK WORM RETENTION TEST")\n'
                        'print("================================================================")\n'
                        '\n'
                        'vault.put_audit_log("audit-2026-09-29.json", "Admin Activity Log Payload")\n'
                        '\n'
                        '# Simulate Malicious / Erroneous Deletion Attempt by Admin\n'
                        'print("\\n[ACTION] Rogue admin attempts to delete audit log...")\n'
                        'try:\n'
                        '    vault.delete_audit_log("audit-2026-09-29.json", caller="org-owner@brightloaf.com")\n'
                        '    print("[FAIL] Deletion unexpectedly succeeded on locked object!")\n'
                        'except PermissionError as e:\n'
                        '    print(f"[PASS] Immutable WORM Enforcement Verified: {e}")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 test_worm_retention.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform WORM audit sink configuration and Python simulation proving deterministic rejection of premature object deletion.',
                'verification': 'Review terminal output of <kbd>python3 test_worm_retention.py</kbd> confirming HTTP 403 permission error on deletion attempts.',
                'trouble': 'If deletion succeeds, verify `is_locked = true` and retention period calculations.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/audit-sink-lab</kbd>.',
                'file': 'day-110-audit-logging.md'
            }
        },
        {
            'key': 'topic-03',
            'title': 'Policy as code',
            'overview': (
                'Enterprise governance at scale requires shifting security controls from manual reviews to automated, declarative '
                'Policy as Code. Across Google Cloud, policy as code is implemented across three primary operational control points: '
                'Organization Policy service (hierarchical resource constraints), Policy Controller / Anthos Config Management '
                '(Kubernetes admission control powered by Open Policy Agent Gatekeeper and declarative Rego rules), and Shift-Left '
                'IaC static analysis (Terraform Sentinel, Checkov, and Google Cloud CLI <kbd>gcloud beta terraform vet</kbd>).'
            ),
            'preview': (
                'A developer commits a Kubernetes deployment requesting privileged container root access; Policy Controller admission '
                'webhook intercepts the manifest and rejects the deployment with a descriptive policy violation.'
            ),
            'technical': (
                '### 1. Policy Controller (OPA / Gatekeeper) Architecture\n'
                '- **Constraint Templates:** Define the reusable logic written in Rego (e.g. `K8sRequiredLabels`, `K8sNoPrivilegedContainers`).\n'
                '- **Constraints:** Bind constraint templates to specific Kubernetes namespaces, resources, or label selectors with '
                'enforcement actions: `deny` (hard block) or `dryrun` (audit only).\n'
                '- **Admission Webhook Intercept:** When <kbd>kubectl apply</kbd> is executed, the API server calls the Gatekeeper webhook before '
                'persisting the object to etcd. If Rego evaluates to true for a violation, the request is rejected immediately.\n'
                '\n'
                '### 2. Shift-Left IaC Validation (<kbd>terraform vet</kbd>)\n'
                '- Evaluates Terraform plan JSON against Google Cloud Organization Policy constraints before executing <kbd>terraform apply</kbd>.\n'
                '- Catches unapproved public IPs, missing CMEK keys, and non-compliant firewall rules directly in CI/CD pull request pipelines.'
            ),
            'questions': [
                'How does Policy Controller (OPA Gatekeeper) differ from standard Kubernetes Role-Based Access Control (RBAC)?',
                'What is the operational function of the `dryrun` enforcement action in Gatekeeper constraints?',
                'How does <kbd>gcloud beta terraform vet</kbd> prevent non-compliant infrastructure from ever reaching the Google Cloud API plane?'
            ],
            'reference': 'https://cloud.google.com/anthos-config-management/docs/concepts/policy-controller',
            'reference_label': 'Google Cloud Policy Controller: OPA Gatekeeper concepts and admission enforcement',
            'scenario': {
                'symptom': 'Security team discovers that a production GKE deployment was running containers with `securityContext.privileged: true`, bypassing node isolation.',
                'constraints': 'GKE clusters must enforce CIS Kubernetes Benchmark; privileged containers are strictly prohibited outside system daemonsets.',
                'evidence': (
                    'Pod specification extracted during security audit:\n\n'
                    '```yaml\n'
                    'apiVersion: v1\n'
                    'kind: Pod\n'
                    'metadata:\n'
                    '  name: backend-worker\n'
                    '  namespace: production\n'
                    'spec:\n'
                    '  containers:\n'
                    '  - name: worker\n'
                    '    image: gcr.io/brightloaf/worker:v2\n'
                    '    securityContext:\n'
                    '      privileged: true # CRITICAL DEFECT: Host root escape vulnerability\n'
                    '```\n\n'
                    'Analysis: The cluster lacked admission policy enforcement, permitting developers to bypass security guidelines via direct kubectl applies.'
                ),
                'diagnostic_steps': [
                    'Query GKE cluster for active admission webhooks using <kbd>kubectl get validatingwebhookconfigurations</kbd>.',
                    'Check whether Policy Controller is installed and synchronized.',
                    'Audit all running pods across namespaces for `privileged: true` flags.',
                    'Review CI/CD deployment pipeline for pre-deployment manifest validation checks.'
                ],
                'root': 'Policy Controller was not configured with a strict deny constraint on privileged container contexts.',
                'fix': 'Deploy Policy Controller constraint template `K8sPSPNoPrivilegedContainer` with `enforcementAction: deny` across all non-system namespaces.',
                'verify': 'Attempt <kbd>kubectl apply</kbd> with privileged container specification; verify admission webhook rejects with descriptive policy violation.',
                'residual': 'Essential system daemonsets (e.g. CNI plugins) must be explicitly whitelisted using namespace exclusions.',
                'diagram': (
                    'Developer executes kubectl apply with privileged: true container',
                    'K8s API server forwards manifest to Policy Controller webhook',
                    'Gatekeeper evaluates Rego constraint K8sPSPNoPrivilegedContainer',
                    'Violation detected; Gatekeeper denies admission with HTTP 403',
                    'Host escape vulnerability prevented; deployment blocked at admission'
                )
            },
            'lab': {
                'name': 'OPA Gatekeeper Policy as Code Admission Engine',
                'goal': 'Author a declarative Rego constraint template and constraint rejecting privileged containers and test a Python admission webhook simulator.',
                'expected': 'Valid Rego policy definition and Python admission simulator proving deterministic rejection of non-compliant pod manifests.',
                'mode': 'Python and Rego policy simulation',
                'prereq': 'Python 3.9+ installed.',
                'preflight': 'Establish working directory `~/policy-code-lab`.',
                'steps': [
                    (
                        '#### Declarative OPA Gatekeeper Constraint Manifest\n'
                        'Author a Kubernetes constraint enforcing no privileged containers:\n\n'
                        '```sh\n'
                        'mkdir -p ~/policy-code-lab && cd ~/policy-code-lab\n'
                        'cat <<\'EOF\' > k8s_no_privileged.yaml\n'
                        'apiVersion: constraints.gatekeeper.sh/v1beta1\n'
                        'kind: K8sPSPNoPrivilegedContainer\n'
                        'metadata:\n'
                        '  name: no-privileged-containers-prod\n'
                        'spec:\n'
                        '  enforcementAction: deny\n'
                        '  match:\n'
                        '    kinds:\n'
                        '      - apiGroups: [""]\n'
                        '        kinds: ["Pod"]\n'
                        '    excludedNamespaces: ["kube-system", "gatekeeper-system"]\n'
                        'EOF\n'
                        'echo "[MANIFEST] Authored k8s_no_privileged.yaml successfully."\n'
                        '```'
                    ),
                    (
                        '#### Admission Webhook Policy Evaluator\n'
                        'Author and run Python script simulating OPA Gatekeeper admission control logic:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > test_admission_policy.py\n'
                        'class GatekeeperAdmissionController:\n'
                        '    def evaluate_pod(self, manifest: dict) -> tuple[bool, str]:\n'
                        '        ns = manifest.get("metadata", {}).get("namespace", "default")\n'
                        '        if ns in ["kube-system", "gatekeeper-system"]:\n'
                        '            return True, "EXEMPT (System Namespace)"\n'
                        '\n'
                        '        containers = manifest.get("spec", {}).get("containers", [])\n'
                        '        for c in containers:\n'
                        '            sec_ctx = c.get("securityContext", {})\n'
                        '            if sec_ctx.get("privileged", False) is True:\n'
                        '                return False, f"DENIED: Container \'{c.get(\'name\')}\' requests privileged execution (violates K8sPSPNoPrivilegedContainer)."\n'
                        '        return True, "ALLOWED (Compliant Security Context)"\n'
                        '\n'
                        'test_pods = [\n'
                        '    {\n'
                        '        "metadata": {"name": "secure-api", "namespace": "production"},\n'
                        '        "spec": {"containers": [{"name": "web", "securityContext": {"privileged": False}}]}\n'
                        '    },\n'
                        '    {\n'
                        '        "metadata": {"name": "malicious-pod", "namespace": "production"},\n'
                        '        "spec": {"containers": [{"name": "exploit", "securityContext": {"privileged": True}}]}\n'
                        '    },\n'
                        '    {\n'
                        '        "metadata": {"name": "calico-node", "namespace": "kube-system"},\n'
                        '        "spec": {"containers": [{"name": "cni", "securityContext": {"privileged": True}}]}\n'
                        '    }\n'
                        ']\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("POLICY CONTROLLER / OPA GATEKEEPER ADMISSION VALIDATOR")\n'
                        'print("================================================================")\n'
                        'controller = GatekeeperAdmissionController()\n'
                        'for pod in test_pods:\n'
                        '    name = pod["metadata"]["name"]\n'
                        '    ns = pod["metadata"]["namespace"]\n'
                        '    allowed, msg = controller.evaluate_pod(pod)\n'
                        '    status = "ADMITTED" if allowed else "REJECTED"\n'
                        '    print(f"[{status:8s}] Pod: {name:15s} (Namespace: {ns:12s}) -> {msg}")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 test_admission_policy.py\n'
                        '```'
                    )
                ],
                'accept': 'Functional Python admission policy validator demonstrating deterministic rejection of privileged pods in production namespaces.',
                'verification': 'Review terminal output of <kbd>python3 test_admission_policy.py</kbd> verifying malicious-pod is rejected while calico-node in kube-system is exempted.',
                'trouble': 'If secure-api is rejected, verify default privileged flag is False.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/policy-code-lab</kbd>.',
                'file': 'day-110-policy-as-code.md'
            }
        },
        {
            'key': 'topic-04',
            'title': 'Data protection regulations',
            'overview': (
                'Global data protection frameworks (such as GDPR, CCPA/CPRA, and LGPD) impose mandatory technical and legal '
                'obligations on enterprise cloud architectures. Core technical requirements include the Right to Erasure '
                '(Article 17, "right to be forgotten"), Data Minimization (Article 5), Data Protection Agreements (DPAs), '
                'Standard Contractual Clauses (SCCs) for cross-border transfers, and automated 72-hour regulatory breach '
                'notification pipelines.'
            ),
            'preview': (
                'A user invokes their GDPR Article 17 right to erasure across a petabyte-scale data warehouse; per-user cryptographic '
                'key shredding renders all historical analytical records instantly unrecoverable without rewriting storage blocks.'
            ),
            'technical': (
                '### 1. Cryptographic Erasure Architecture (Right to be Forgotten)\n'
                '- **The Big Data Deletion Challenge:** In immutable append-only systems (BigQuery, Cloud Storage archives, Parquet/ORC '
                'data lakes), deleting individual customer rows requires rewriting terabytes or petabytes of files, costing enormous compute and risking data corruption.\n'
                '- **Cryptographic Key Shredding (Crypto-Shredding):** Every user\'s PII is encrypted with a unique, dedicated User '
                'Data Encryption Key (UDEK). When an Article 17 deletion request is processed, the system permanently destroys the UDEK '
                'in Secret Manager/KMS. The ciphertext remains in analytical storage, but is mathematically impossible to decrypt, '
                'satisfying legal erasure requirements.\n'
                '\n'
                '### 2. Breach Notification & Legal Transfer Governance\n'
                '- **72-Hour Breach Notification:** Mandates automated integration between Security Command Center finding alerts, '
                'Eventarc, and incident response teams to meet GDPR Article 33 reporting timelines.\n'
                '- **DPA & SCCs:** Google Cloud\'s Data Processing Addendum (DPA) incorporates EU Standard Contractual Clauses (SCCs), '
                'legally governing data transfers outside the European Economic Area.'
            ),
            'questions': [
                'How does cryptographic key shredding fulfill GDPR Article 17 erasure requirements on immutable append-only data lakes?',
                'What automated pipeline architecture ensures an enterprise can detect and report a data breach within 72 hours?',
                'Why are Standard Contractual Clauses (SCCs) essential when processing European customer data in global cloud environments?'
            ],
            'reference': 'https://cloud.google.com/security/compliance/gdpr',
            'reference_label': 'Google Cloud GDPR Compliance: Technical controls, privacy whitepapers, and DPA frameworks',
            'scenario': {
                'symptom': 'European privacy regulator serves formal inquiry regarding unfulfilled GDPR Article 17 deletion requests dating back 60 days.',
                'constraints': 'Enterprise must execute verified user erasure requests within 30 days without corrupting historical billing analytics.',
                'evidence': (
                    'Customer deletion ticket audit log snippet:\n\n'
                    '```text\n'
                    'User ID: EU-USER-89102\n'
                    'Request: Article 17 Right to Erasure\n'
                    'Status: PENDING (Exceeded 30-day statutory window)\n'
                    'Engineering Blocker: "User data is embedded in 4,200 compressed BigQuery partition tables; rewriting warehouse exceeds daily slot quota."\n'
                    'Regulatory Consequence: Potential Article 83 fine up to €20M or 4% of global annual turnover.\n'
                    '```\n\n'
                    'Analysis: Data engineering designed the warehouse with monolithic encryption, making individual row deletions '
                    'operationally intractable.'
                ),
                'diagnostic_steps': [
                    'Review analytical schema to identify where customer PII is replicated across tables.',
                    'Evaluate computational cost of running daily partition rewrites versus cryptographic erasure.',
                    'Check current User Data Encryption Key (UDEK) management infrastructure.',
                    'Verify statutory tracking timestamps across all open privacy requests.'
                ],
                'root': 'Analytical architecture lacked per-user key management, requiring costly full-table rewrites to fulfill single-user deletion requests.',
                'fix': 'Implement per-user cryptographic envelope encryption; process Article 17 requests by permanently destroying the target user\'s UDEK.',
                'verify': 'Attempt decryption of user telemetry following UDEK shredding; confirm ciphertext cannot be decrypted; provide cryptographic audit certificate to regulator.',
                'residual': 'Aggregate, anonymized statistical metrics that contain zero personal identifiers can be retained legally for business reporting.',
                'diagram': (
                    'User requests Article 17 erasure; warehouse rewrite blocked by cost',
                    'Failure to erase exceeds 30-day statutory limit; regulator opens inquiry',
                    'Transition architecture to per-user cryptographic key shredding',
                    'Execute deletion request by permanently destroying user UDEK',
                    'User ciphertext rendered mathematically unrecoverable; compliance certified'
                )
            },
            'lab': {
                'name': 'GDPR Cryptographic Key Shredding Engine',
                'goal': 'Implement a Python cryptographic erasure engine demonstrating per-user key shredding and proving permanent ciphertext unrecoverability.',
                'expected': 'Functional Python script encrypting user records with per-user keys, executing cryptographic deletion, and proving failure on post-deletion read attempts.',
                'mode': 'Python cryptographic implementation',
                'prereq': 'Python 3.9+ installed.',
                'preflight': 'Establish working directory `~/gdpr-shred-lab`.',
                'steps': [
                    (
                        '#### Cryptographic Erasure Implementation\n'
                        'Author and run a Python script modeling per-user UDEK lifecycle and cryptographic shredding:\n\n'
                        '```sh\n'
                        'mkdir -p ~/gdpr-shred-lab && cd ~/gdpr-shred-lab\n'
                        'cat <<\'EOF\' > test_crypto_shredding.py\n'
                        'import hashlib\n'
                        'import os\n'
                        '\n'
                        'class UserKeyVault:\n'
                        '    def __init__(self):\n'
                        '        self.user_keys = {}\n'
                        '\n'
                        '    def create_user_key(self, user_id: str) -> bytes:\n'
                        '        key = os.urandom(32)\n'
                        '        self.user_keys[user_id] = key\n'
                        '        return key\n'
                        '\n'
                        '    def get_user_key(self, user_id: str) -> bytes:\n'
                        '        if user_id not in self.user_keys:\n'
                        '            raise KeyError(f"Key for {user_id} does not exist (DESTROYED or UNREGISTERED).")\n'
                        '        return self.user_keys[user_id]\n'
                        '\n'
                        '    def shred_user_key(self, user_id: str):\n'
                        '        if user_id in self.user_keys:\n'
                        '            del self.user_keys[user_id]\n'
                        '            print(f"[SHRED] UDEK for {user_id} permanently erased from Key Vault.")\n'
                        '\n'
                        'vault = UserKeyVault()\n'
                        'user_id = "EU-USER-89102"\n'
                        'ude_key = vault.create_user_key(user_id)\n'
                        '\n'
                        '# Encrypt user PII with UDEK\n'
                        'plaintext_pii = b"Name: Eva Hansen | IBAN: DE89370400440532013000 | Email: eva@example.de"\n'
                        'mask = hashlib.sha256(ude_key).digest()\n'
                        'ciphertext = bytes(p ^ mask[i % len(mask)] for i, p in enumerate(plaintext_pii))\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("GDPR ARTICLE 17 CRYPTOGRAPHIC KEY SHREDDING ENGINE")\n'
                        'print("================================================================")\n'
                        'print(f"User: {user_id}")\n'
                        'print(f"Encrypted Warehouse Payload: {ciphertext.hex()[:48]}... ({len(ciphertext)} bytes)")\n'
                        '\n'
                        '# Normal Operation: Read PII\n'
                        'active_key = vault.get_user_key(user_id)\n'
                        'active_mask = hashlib.sha256(active_key).digest()\n'
                        'decrypted = bytes(c ^ active_mask[i % len(active_mask)] for i, c in enumerate(ciphertext))\n'
                        'print(f"Normal Read Decryption: {decrypted.decode()}")\n'
                        'assert decrypted == plaintext_pii\n'
                        '\n'
                        '# User Invokes GDPR Article 17 Right to Erasure\n'
                        'print("\\n[ACTION] Processing GDPR Article 17 Right to Erasure request...")\n'
                        'vault.shred_user_key(user_id)\n'
                        '\n'
                        '# Post-Erasure Read Attempt\n'
                        'print("[TEST] Attempting to decrypt user record after key shredding...")\n'
                        'try:\n'
                        '    vault.get_user_key(user_id)\n'
                        '    print("[FAIL] Key still accessible!")\n'
                        'except KeyError as e:\n'
                        '    print(f"[PASS] Cryptographic Erasure Verified: {e}")\n'
                        '    print("       Plaintext cannot be recovered; Article 17 legally satisfied.")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 test_crypto_shredding.py\n'
                        '```'
                    )
                ],
                'accept': 'Functional Python cryptographic erasure engine demonstrating irreversible data recovery failure following per-user key shredding.',
                'verification': 'Review terminal output of <kbd>python3 test_crypto_shredding.py</kbd> verifying successful shredding and KeyError exception.',
                'trouble': 'If key is still retrieved, verify dictionary deletion in UserKeyVault.',
                'cleanup': 'Remove test directory: <kbd>rm -rf ~/gdpr-shred-lab</kbd>.',
                'file': 'day-110-data-protection.md'
            }
        }
    ]
}
