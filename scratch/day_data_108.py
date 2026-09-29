"""day_data_108.py — Exhaustive architecture data specification for Day 108.

Covers Confidential Computing, Resource Location Constraints, Assured Workloads & Sovereignty Boundaries,
and Fine-Grained Data Access (Column-level & Row-level Policy Design).
"""

DAY_NUM = 108

DATA = {
    'day': 108,
    'part1_intro': (
        'Day 108 addresses data residency, in-memory cryptographic isolation, and granular data access governance across '
        'Google Cloud. Architects examine Confidential Computing (AMD SEV / Intel TDX hardware-encrypted memory), Organization '
        'Policy resource location guardrails (`constraints/gcp.resourceLocations`), Assured Workloads compliance boundaries '
        'for jurisdictional sovereignty (EU Sovereign Cloud, US FedRAMP), object retention lifecycle holds, and fine-grained '
        'column-level policy tags and row-level access policies governing analytical datasets.'
    ),
    'exit_summary': (
        'Engineers design and verify an enterprise data residency and sovereignty matrix, an Assured Workloads jurisdictional '
        'boundary specification, a Confidential VM memory encryption verification trace, and a row/column-level access control '
        'architecture fulfilling all Day 108 Exit evidence criteria.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts data state protection boundaries, hardware memory encryption guarantees, '
        'geographic residency enforcement, and granular access filtering across Google Cloud governance architectures.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Residency &amp; Access Control Tier</th>\n'
        '<th>Protection Mechanism</th>\n'
        '<th>Cryptographic &amp; Logical Boundary</th>\n'
        '<th>Enforcement Layer</th>\n'
        '<th>Failure Signal &amp; Trade-off</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>Confidential Computing (CVM)</strong></td>\n'
        '<td>Hardware memory encryption (AMD SEV / Intel TDX)</td>\n'
        '<td>Guest physical RAM encrypted with CPU-generated ephemeral keys</td>\n'
        '<td>Hypervisor / Processor Silicon boundary</td>\n'
        '<td>Negligible CPU overhead (2–6%); hypervisor cannot inspect guest memory dumps or VM cold state.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Resource Location Constraints</strong></td>\n'
        '<td>Organization Policy (`constraints/gcp.resourceLocations`)</td>\n'
        '<td>Restricts resource creation to approved Google Cloud regions/zones</td>\n'
        '<td>Google Cloud Resource Manager &amp; API Control Plane</td>\n'
        '<td>API request blocked immediately with HTTP 412 / OrgPolicy violation if unapproved region is targeted.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Assured Workloads</strong></td>\n'
        '<td>Sovereignty &amp; compliance regime envelope</td>\n'
        '<td>Enforces location, personnel access controls (CAC/FedRAMP), and EKM</td>\n'
        '<td>Managed Folder / Project hierarchy guardrails</td>\n'
        '<td>Restricts available services to certified catalog; limits multi-region deployment flexibility.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Column-Level Access (Policy Tags)</strong></td>\n'
        '<td>Dataplex taxonomies &amp; BigQuery fine-grained reader IAM</td>\n'
        '<td>Restricts SELECT queries on sensitive columns (e.g. SSN, salary)</td>\n'
        '<td>BigQuery SQL Query Engine &amp; IAM policy evaluator</td>\n'
        '<td>User without `roles/datacatalog.categoryFineGrainedReader` gets Access Denied or hashed masking.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Row-Level Access Policies</strong></td>\n'
        '<td>Dynamic SQL row-filter predicates (`SESSION_USER()`)</td>\n'
        '<td>Filters returned dataset rows based on query caller identity</td>\n'
        '<td>BigQuery Storage API execution engine</td>\n'
        '<td>Complex predicates increase query processing overhead; partition pruning must align with filter keys.</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 108: Confidential Computing, Sovereign Cloud Boundaries, and Granular Data Access Topology',
        'desc': 'Architectural layout illustrating Confidential VM memory encryption, Org Policy regional constraints, Assured Workloads sovereignty boundaries, and BigQuery column/row access filters.',
        'caption': 'Figure 108.1: Enterprise data sovereignty and access isolation architecture featuring AMD SEV memory encryption, Org Policy geographic barriers, and fine-grained analytical dataset filtering.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Enterprise Organization Policy & Sovereignty Envelope',
                'desc': 'Resource location constraints (gcp.resourceLocations) and Assured Workloads jurisdictional boundaries',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Confidential Computing & Hardware Memory Encryption Plane',
                'desc': 'Compute Engine Confidential VMs and Confidential GKE nodes running on AMD SEV / Intel TDX silicon',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Storage Retention, Immutable Lock & Deletion Safeguards',
                'desc': 'Cloud Storage Bucket Lock, object retention policies, and legal holds preventing unauthorized destruction',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Granular Data Access Control (Dataplex Policy Tags & Row Filters)',
                'desc': 'Dataplex policy tag taxonomies masking sensitive columns and row-level security evaluating caller identity',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: Analytical Consumer & Forensic Audit Verification Boundary',
                'desc': 'Business intelligence dashboards, analytical consumers, and Cloud Audit logging recording all data queries',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Org Policy: EU Regions Only', 'detail': 'in:europe-west1,europe-west4', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Assured Workloads EU', 'detail': 'Sovereign Controls & Access', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Confidential VM Instance', 'detail': 'AMD SEV Encrypted RAM', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Secure Enclave Memory', 'detail': 'Zero Hypervisor Visibility', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'GCS Retention Policy', 'detail': '365-Day Retention Period', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Bucket Lock / Legal Hold', 'detail': 'Immutable SEC 17a-4 Vault', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Dataplex Policy Tag', 'detail': 'Masking Rule: SHA256 Hash', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Row-Level Access Policy', 'detail': 'region = SESSION_REGION()', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Authorized Analyst', 'detail': 'Queries Filtered Rows Only', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'Audit Activity Log', 'detail': 'Captures Evaluated Policies', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'SOVEREIGNTY & GEOGRAPHIC GOVERNANCE ENVELOPE', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'HARDWARE ENCRYPTION & DATA RETENTION VAULT', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'GRANULAR ANALYTICAL ACCESS FILTERING PLANE', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Enforce Sovereign Boundary', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Provision In Sovereign Zone', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Encrypt Guest RAM (SEV)', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Persist to Locked Storage', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Enforce Retention Period', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Route to BigQuery Table', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Evaluate Dynamic Row Filter', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Mask Tagged PII Columns', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Audit Filtered Access', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: Confidential VM SEV Status & dmesg Attestation', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: GCS Retention Lock & Object Deletion Block', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 345, 'label': 'PROBE 3: BigQuery Policy Tag Masking & Row Filter Evaluation', 'badge': 'P3', 'color': '#f43f5e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world data sovereignty violations, accidental data deletion under retention, '
        'and unauthorized data exposure through misconfigured row-level security. Each scenario details verbatim diagnostic logs, '
        'root cause mechanics, production remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on exercises execute the complete 8-stage operational engineering lifecycle for Day 108. '
        'Architects model Confidential VM deployment parameters, author Organization Policy resource location manifests, '
        'and implement local Python simulations of fine-grained row-level filtering and column-level policy tag masking.'
    ),
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Confidential computing, resource location constraints, Assured Workloads and data…',
            'overview': (
                'Enterprise workloads processing highly sensitive financial or healthcare data require protection across all three '
                'data states: at rest, in transit, and in use. Google Cloud Confidential Computing encrypts data in-use in main memory '
                'using hardware-level AMD Secure Encrypted Virtualization (SEV) and Intel Trust Domain Extensions (TDX), preventing '
                'hypervisor inspection. Concurrently, Organization Policy resource location constraints (`gcp.resourceLocations`) '
                'and Assured Workloads enforce rigid geographical data sovereignty, guaranteeing that data, compute, and encryption keys '
                'never leave designated sovereign jurisdictions.'
            ),
            'preview': (
                'A developer attempts to spin up a compute instance in an unapproved offshore region; Organization Policy immediately '
                'terminates the API request with an authoritative location violation error.'
            ),
            'technical': (
                '### 1. Confidential Computing Mechanics (Data In-Use)\n'
                '- **Hardware-Isolated Memory:** AMD SEV generates an ephemeral cryptographic key inside the AMD Secure Processor. '
                'Memory reads/writes between the CPU and DRAM are encrypted with AES-128/256 at wire speed. The Google host hypervisor, '
                'other VMs, and Google administrators cannot read guest memory plaintext.\n'
                '- **Confidential Space:** A specialized secure enclave environment enabling multi-party confidential data collaboration '
                'without either party disclosing raw proprietary datasets.\n'
                '\n'
                '### 2. Resource Location Constraints & Assured Workloads\n'
                '- **Resource Location Constraint:** Org Policy `constraints/gcp.resourceLocations` defines an allowlist of permitted '
                'regions (e.g. `in:eu-locations`). Any attempt to create buckets, VMs, or BigQuery datasets outside this boundary is rejected.\n'
                '- **Assured Workloads:** Provisions sovereign cloud landing zones enforcing compliance regimes (e.g. EU Sovereign Controls, '
                'US FedRAMP High, CJIS, IL4). Restricts support personnel access, enforces Cloud EKM key sovereignty, and automates '
                'compliance monitoring.'
            ),
            'questions': [
                'How does AMD SEV protect sensitive data in memory against hypervisor compromises and physical memory bus sniffing?',
                'What is the operational impact on multi-region backups when `constraints/gcp.resourceLocations` is strictly enforced?',
                'Under what compliance mandates is Assured Workloads mandatory compared to standard Organization Policies?'
            ],
            'reference': 'https://cloud.google.com/confidential-computing/confidential-vm/docs/confidential-vm-overview',
            'reference_label': 'Google Cloud Confidential Computing: AMD SEV architecture and hardware memory encryption',
            'scenario': {
                'symptom': 'Continuous deployment pipeline fails with HTTP 412 Precondition Failed during infrastructure provisioning: `Location us-west1 is violated by Org Policy`.',
                'constraints': 'European GDPR banking data must reside exclusively within EU physical borders; zero resources permitted in North America.',
                'evidence': (
                    'Cloud Resource Manager audit log showing Org Policy denial:\n\n'
                    '```json\n'
                    '{\n'
                    '  "protoPayload": {\n'
                    '    "serviceName": "compute.googleapis.com",\n'
                    '    "methodName": "compute.instances.insert",\n'
                    '    "status": {\n'
                    '      "code": 9,\n'
                    '      "message": "Constraint constraints/gcp.resourceLocations violated for projects/eu-banking-prod. Location us-west1 is not allowed by policy."\n'
                    '    }\n'
                    '  }\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: A Terraform configuration defaulted to `us-west1` for a secondary backup disk snapshot, '
                    'triggering the organizational boundary guardrail.'
                ),
                'diagnostic_steps': [
                    'Extract the violated constraint name from the Cloud Audit log.',
                    'Inspect active Organization Policy bindings: <kbd>gcloud org-policies describe constraints/gcp.resourceLocations</kbd>.',
                    'Verify the allowlist of permitted locations (`europe-west1`, `europe-west4`).',
                    'Audit Terraform variable declarations for hardcoded non-EU region references.'
                ],
                'root': 'Terraform manifest declared a backup snapshot in an unapproved region, violating organizational sovereignty constraints.',
                'fix': 'Update Terraform region parameters to target `europe-west1` and implement CI linting to validate resource locations before deployment.',
                'verify': 'Re-run Terraform apply; confirm compute instance and disk snapshots provision successfully within EU borders.',
                'residual': 'Global services (e.g. Cloud IAM, Global External ALBs) have global control planes and require documentation of management metadata paths.',
                'diagram': (
                    'Terraform deployment targets us-west1 for secondary backup snapshot',
                    'Org Policy evaluator checks constraints/gcp.resourceLocations',
                    'Location not in EU allowlist; API call rejected with HTTP 412',
                    'Update Terraform region parameter to europe-west1; re-apply manifest',
                    'Resource provisions successfully within verified sovereign EU boundary'
                )
            },
            'lab': {
                'name': 'Resource Location Governance & Confidential VM Modeling',
                'goal': 'Author declarative Terraform configurations for Confidential VMs with AMD SEV and test a Python simulator evaluating geographic resource location policies.',
                'expected': 'Validated Terraform Confidential VM manifest and working Python script evaluating resource location compliance.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Python 3 and Terraform installed.',
                'preflight': 'Establish working directory `~/sovereignty-lab`.',
                'steps': [
                    (
                        '#### Declarative Confidential VM Terraform Architecture\n'
                        'Author a Compute Engine instance manifest enforcing Confidential Computing memory encryption:\n\n'
                        '```sh\n'
                        'mkdir -p ~/sovereignty-lab && cd ~/sovereignty-lab\n'
                        'cat <<\'EOF\' > confidential_vm.tf\n'
                        'resource "google_compute_instance" "confidential_workload" {\n'
                        '  name         = "prod-confidential-worker"\n'
                        '  machine_type = "n2d-standard-4" # N2D / C2D supports AMD SEV\n'
                        '  zone         = "europe-west1-b"\n'
                        '\n'
                        '  boot_disk {\n'
                        '    initialize_params {\n'
                        '      image = "ubuntu-os-cloud/ubuntu-2204-lts"\n'
                        '    }\n'
                        '  }\n'
                        '\n'
                        '  network_interface {\n'
                        '    network = "projects/sovereign-core/global/networks/eu-vpc"\n'
                        '  }\n'
                        '\n'
                        '  confidential_instance_config {\n'
                        '    enable_confidential_compute = true\n'
                        '  }\n'
                        '\n'
                        '  shielded_instance_config {\n'
                        '    enable_secure_boot          = true\n'
                        '    enable_vtpm                 = true\n'
                        '    enable_integrity_monitoring = true\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored confidential_vm.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### Resource Location Policy Evaluator\n'
                        'Author and run Python script simulating Organization Policy regional guardrail enforcement:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > test_location_policy.py\n'
                        'ALLOWED_LOCATIONS = {"europe-west1", "europe-west3", "europe-west4"}\n'
                        '\n'
                        'candidate_resources = [\n'
                        '    {"name": "eu-core-db", "type": "Cloud SQL", "location": "europe-west1"},\n'
                        '    {"name": "eu-analytics-warehouse", "type": "BigQuery", "location": "europe-west4"},\n'
                        '    {"name": "us-log-sink", "type": "Cloud Storage", "location": "us-central1"}, # VIOLATION\n'
                        '    {"name": "asia-read-replica", "type": "Compute VM", "location": "asia-northeast1"} # VIOLATION\n'
                        ']\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("ORGANIZATION POLICY: RESOURCE LOCATION ENFORCEMENT")\n'
                        'print("================================================================")\n'
                        'print(f"Authoritative Allowed Boundary: {ALLOWED_LOCATIONS}\\n")\n'
                        '\n'
                        'for res in candidate_resources:\n'
                        '    is_allowed = res["location"] in ALLOWED_LOCATIONS\n'
                        '    status = "APPROVED (Sovereign Compliant)" if is_allowed else "DENIED (OrgPolicy Violation)"\n'
                        '    print(f"[{status:28s}] {res[\'name\']:24s} Location: {res[\'location\']:16s} ({res[\'type\']})")\n'
                        '\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 test_location_policy.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform Confidential VM configuration with AMD SEV enabled and Python script proving deterministic rejection of non-EU locations.',
                'verification': 'Review terminal output of <kbd>python3 test_location_policy.py</kbd> verifying non-EU resources are blocked.',
                'trouble': 'If Confidential VM fails validation, ensure machine type is N2D, C2D, or C3D (Confidential Computing is unsupported on E2/N1).',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/sovereignty-lab</kbd>.',
                'file': 'day-108-confidential-sovereignty.md'
            }
        },
        {
            'key': 'topic-02',
            'title': 'BigQuery enforcement is exercised in the data block on Day 135',
            'overview': (
                'Enterprise data platforms require granular, multi-layered data access security beyond coarse dataset-level IAM. '
                'Column-level security utilizes Dataplex Policy Tags and Taxonomies to restrict or mask specific attributes '
                '(e.g. tax IDs, credit cards, salaries) so that only authorized principals can view plaintext. Concurrently, '
                'Row-Level Access Policies evaluate dynamic boolean SQL filter predicates (e.g. `SESSION_USER()`) to restrict '
                'visible rows based on organizational division or geographic territory. Full warehouse operationalization '
                'is explored on Day 135; today establishes the foundational access architecture.'
            ),
            'preview': (
                'A regional branch manager queries the global customer database; row-level access policies automatically filter '
                'the returned dataset so only customers residing in their designated territory are returned.'
            ),
            'technical': (
                '### 1. Column-Level Security via Dataplex Policy Tags\n'
                '- **Taxonomies & Policy Tags:** Architects define a hierarchy of security tags (e.g. `Taxonomy: PII -> Tag: High-Confidentiality`).\n'
                '- **Data Catalog Integration:** Policy tags are attached directly to schema fields in BigQuery tables.\n'
                '- **Fine-Grained Reader IAM:** Users require `roles/datacatalog.categoryFineGrainedReader` on the specific tag to query '
                'the column in plaintext. Users without the role either receive a permission error or see dynamic masked values '
                '(null, default, or crypto-hash).\n'
                '\n'
                '### 2. Row-Level Access Policies (RLS)\n'
                '- **Filter Predicates:** Written in GoogleSQL: `CREATE ROW ACCESS POLICY region_filter ON table GRANT TO ("group:eu-managers@brightloaf.com") FILTER USING (region = "EU")`.\n'
                '- **Session Identity Binding:** Evaluates `SESSION_USER()` dynamically at query execution time. The underlying data '
                'is not modified, and administrators do not need to maintain fragmented partitioned copies.'
            ),
            'questions': [
                'How do Dataplex policy tags enable centralized column masking across thousands of BigQuery tables without modifying schema definitions?',
                'What happens when a query executes against a table with Row-Level Access Policies if the caller matches multiple policies?',
                'Why should row-level security predicates be aligned with table partitioning and clustering columns?'
            ],
            'reference': 'https://cloud.google.com/bigquery/docs/column-level-security-intro',
            'reference_label': 'Google Cloud BigQuery: Column-level security and Dataplex policy tag management',
            'scenario': {
                'symptom': 'Regional sales director in EMEA runs a quarterly revenue report and inadvertently views APAC and US confidential customer deals.',
                'constraints': 'All global revenue data resides in a unified BigQuery table; regional directors must only see records for their assigned territory.',
                'evidence': (
                    'Audit log snippet showing broad row access:\n\n'
                    '```text\n'
                    'Caller: emea-director@brightloaf.com\n'
                    'Query: SELECT customer_name, deal_size, territory FROM enterprise_sales.deals;\n'
                    'Returned Row Count: 142,000 (Included territories: US-EAST, US-WEST, APAC, EMEA)\n'
                    'Policy State: No active Row-Level Access Policy on enterprise_sales.deals\n'
                    '```\n\n'
                    'Analysis: Table-level IAM grant (`roles/bigquery.dataViewer`) granted read visibility across all rows '
                    'in the dataset due to absence of row-level security predicates.'
                ),
                'diagnostic_steps': [
                    'Inspect existing Row-Level Access Policies using `INFORMATION_SCHEMA.ROW_ACCESS_POLICIES`.',
                    'Review dataset IAM bindings for overly permissive reader grants.',
                    'Verify the territory column structure and verify compatibility with `SESSION_USER()` mapping tables.',
                    'Check query execution plans for partition pruning efficiency under row filtering.'
                ],
                'root': 'Unified sales table relied exclusively on table-level IAM, lacking dynamic Row-Level Access Policies to segment data by territory.',
                'fix': 'Deploy a BigQuery Row-Level Access Policy binding territory visibility to user group membership using dynamic SQL filter predicates.',
                'verify': 'Execute query as EMEA director; confirm returned row count drops to 28,000 and contains exclusively `territory = "EMEA"`.',
                'residual': 'Table queries that omit partition filters in combination with row policies may scan full tables, increasing slot usage.',
                'diagram': (
                    'EMEA sales director queries global deals table with dataViewer role',
                    'Table lacks Row-Level Access Policies; returns global deals data',
                    'Confidential US and APAC customer deal sizes exposed in report',
                    'Author Row Access Policy: FILTER USING (territory = "EMEA")',
                    'Query re-executed; engine returns only authorized regional records'
                )
            },
            'lab': {
                'name': 'Fine-Grained Column Masking & Row-Level Security Simulator',
                'goal': 'Implement a local Python data engine modeling BigQuery column-level policy tag masking and dynamic row-level access policy evaluation.',
                'expected': 'Functional Python simulation evaluating user identity against column tags and row predicates, returning masked and filtered datasets.',
                'mode': 'Python data engine simulation',
                'prereq': 'Python 3.9+ installed.',
                'preflight': 'Establish working directory `~/row-col-access-lab`.',
                'steps': [
                    (
                        '#### Analytical Access Engine Implementation\n'
                        'Author and run Python script simulating BigQuery column masking and row-level access policies:\n\n'
                        '```sh\n'
                        'mkdir -p ~/row-col-access-lab && cd ~/row-col-access-lab\n'
                        'cat <<\'EOF\' > test_access_policies.py\n'
                        'import hashlib\n'
                        '\n'
                        '# Raw Underlying Warehouse Table\n'
                        'raw_deals_table = [\n'
                        '    {"deal_id": "D-101", "client": "Acme Corp", "amount": 250000, "territory": "EMEA", "ssn": "000-11-2222"},\n'
                        '    {"deal_id": "D-102", "client": "Beta Corp", "amount": 840000, "territory": "US",   "ssn": "111-22-3333"},\n'
                        '    {"deal_id": "D-103", "client": "Gamma LLC", "amount": 120000, "territory": "EMEA", "ssn": "222-33-4444"},\n'
                        '    {"deal_id": "D-104", "client": "Delta Ltd", "amount": 490000, "territory": "APAC", "ssn": "333-44-5555"}\n'
                        ']\n'
                        '\n'
                        'def query_table(user_email: str, user_roles: set) -> list[dict]:\n'
                        '    # 1. Determine Row-Level Access Policy Predicate\n'
                        '    if "role:global_exec" in user_roles:\n'
                        '        row_filter = lambda row: True\n'
                        '    elif "role:emea_director" in user_roles:\n'
                        '        row_filter = lambda row: row["territory"] == "EMEA"\n'
                        '    else:\n'
                        '        row_filter = lambda row: False\n'
                        '\n'
                        '    # 2. Determine Column-Level Policy Tag Masking\n'
                        '    can_view_pii = "role:pii_fine_grained_reader" in user_roles\n'
                        '\n'
                        '    results = []\n'
                        '    for row in raw_deals_table:\n'
                        '        if row_filter(row):\n'
                        '            filtered_row = dict(row)\n'
                        '            if not can_view_pii:\n'
                        '                # Dynamic masking: SHA256 hash or redact\n'
                        '                filtered_row["ssn"] = "XXX-XX-" + filtered_row["ssn"][-4:]\n'
                        '            results.append(filtered_row)\n'
                        '    return results\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("BIGQUERY FINE-GRAINED COLUMN & ROW ACCESS EVALUATOR")\n'
                        'print("================================================================")\n'
                        '\n'
                        '# Case 1: EMEA Director (Without PII reader role)\n'
                        'emea_user = "director-emea@brightloaf.com"\n'
                        'emea_roles = {"role:emea_director"}\n'
                        'emea_results = query_table(emea_user, emea_roles)\n'
                        'print(f"Results for {emea_user} (Territory: EMEA, No PII Grant):")\n'
                        'for r in emea_results:\n'
                        '    print(f"  • Deal: {r[\'deal_id\']} | Client: {r[\'client\']:10s} | Region: {r[\'territory\']} | SSN: {r[\'ssn\']}")\n'
                        '\n'
                        'assert len(emea_results) == 2\n'
                        'assert all(r["territory"] == "EMEA" for r in emea_results)\n'
                        'assert all(r["ssn"].startswith("XXX-XX-") for r in emea_results)\n'
                        'print("\\n[PASS] Row-level filtering enforced: Only EMEA records returned.")\n'
                        'print("[PASS] Column-level masking enforced: SSN masked for unauthorized user.")\n'
                        '\n'
                        '# Case 2: Global Executive (With PII reader role)\n'
                        'exec_user = "cfo@brightloaf.com"\n'
                        'exec_roles = {"role:global_exec", "role:pii_fine_grained_reader"}\n'
                        'exec_results = query_table(exec_user, exec_roles)\n'
                        'print(f"\\nResults for {exec_user} (Global Exec + PII Grant):")\n'
                        'for r in exec_results:\n'
                        '    print(f"  • Deal: {r[\'deal_id\']} | Client: {r[\'client\']:10s} | Region: {r[\'territory\']} | SSN: {r[\'ssn\']}")\n'
                        'assert len(exec_results) == 4\n'
                        'assert exec_results[0]["ssn"] == "000-11-2222"\n'
                        'print("\\n[PASS] Full dataset and plaintext PII returned for authorized executive.")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 test_access_policies.py\n'
                        '```'
                    )
                ],
                'accept': 'Functional Python data policy engine demonstrating accurate row-level filtering and column-level masking across differing user roles.',
                'verification': 'Review terminal output of <kbd>python3 test_access_policies.py</kbd> confirming expected record counts and SSN redactions.',
                'trouble': 'If EMEA results contain non-EMEA records, verify row_filter lambda predicate condition.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/row-col-access-lab</kbd>.',
                'file': 'day-108-data-access-policies.md'
            }
        }
    ]
}
