"""day_data_106.py — Exhaustive architecture data specification for Day 106.

Covers Data Classification (Public, Internal, Confidential, Restricted),
Encryption at Rest (Default, CMEK, CSEK, Cloud EKM),
Encryption in Transit & Application-Layer Encryption, and
Cloud KMS (Key Rings, Keys, Versions, Rotation, Protection Levels, Destruction Safeguards).
"""

DAY_NUM = 106

DATA = {
    'day': 106,
    'part1_intro': (
        'Day 106 establishes the data protection, cryptographic governance, and key lifecycle architecture across '
        'Google Cloud. Architects examine enterprise data classification taxonomies, the hierarchy of encryption at rest '
        'from default Google-managed keys to Customer-Managed Encryption Keys (CMEK), Customer-Supplied Encryption Keys (CSEK), '
        'and Cloud External Key Manager (Cloud EKM), envelope encryption and application-layer field-level cryptography, and '
        'the complete Cloud KMS key versioning, cryptographic rotation, protection level, and scheduled destruction safeguards.'
    ),
    'exit_summary': (
        'Engineers design and verify an enterprise data classification and encryption decision matrix, an automated Cloud KMS '
        'CMEK rotation pipeline with CryptoKey version tracking, an envelope encryption demonstration using Google Tink, and '
        'a secure cryptographic destruction safeguard protocol fulfilling all Day 106 Exit evidence criteria.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts data protection levels, operational ownership boundaries, cryptographic '
        'custody, performance trade-offs, and failure recovery mechanics across Google Cloud encryption architectures.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Encryption Pattern</th>\n'
        '<th>Key Custody &amp; Root of Trust</th>\n'
        '<th>Cryptographic Boundary</th>\n'
        '<th>Rotation Ownership &amp; Cadence</th>\n'
        '<th>Failure Mode &amp; Blast Radius</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>Default Google-Managed Encryption</strong></td>\n'
        '<td>Google internal Keystore (BoringSSL / FIPS 140-2)</td>\n'
        '<td>Transparent block storage layer (AES-256)</td>\n'
        '<td>Automated Google internal rotation; zero customer overhead</td>\n'
        '<td>Fully transparent; cannot be revoked or disabled by customer.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Customer-Managed Encryption Keys (CMEK)</strong></td>\n'
        '<td>Customer Cloud KMS (Software or Cloud HSM)</td>\n'
        '<td>Service agent decodes DEK via KMS CryptoKey Decrypt API</td>\n'
        '<td>Automated KMS schedule (e.g. 90 days) or manual version creation</td>\n'
        '<td>Service agent IAM revocation or key disablement immediately freezes all I/O operations across protected resources.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Customer-Supplied Encryption Keys (CSEK)</strong></td>\n'
        '<td>Customer off-cloud key vault; never stored on Google disks</td>\n'
        '<td>Supplied in raw API headers per read/write call</td>\n'
        '<td>Customer manual key tracking and deployment</td>\n'
        '<td>If raw 256-bit passphrase is lost by customer, data is permanently and irreversibly unrecoverable.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Cloud External Key Manager (Cloud EKM)</strong></td>\n'
        '<td>Third-party on-premise HSM / EKM partner (e.g. Thales, Fortanix)</td>\n'
        '<td>KMS forwards wrap/unwrap requests over VPC / public EKM endpoint</td>\n'
        '<td>On-premise HSM policy engine and Key Access Justifications (KAJ)</td>\n'
        '<td>Network partition or latency spike between GCP and external EKM causes immediate API request timeouts.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Application-Layer Envelope Encryption</strong></td>\n'
        '<td>Google Tink / KMS Envelope (Client Workload)</td>\n'
        '<td>In-memory payload encryption before transmission to database/storage</td>\n'
        '<td>Workload calls KMS to encrypt/decrypt local Data Encryption Key (DEK)</td>\n'
        '<td>Database administrators and cloud storage operators see only ciphertext; compromise of database reveals zero plaintext.</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 106: Enterprise Cryptographic Hierarchy, Cloud KMS Key Lifecycle, and Envelope Encryption Topology',
        'desc': 'Architectural layout illustrating Cloud KMS Key Rings, automated CryptoKey version rotation, service agent IAM delegation, envelope encryption using DEKs and KEKs, and Cloud EKM Key Access Justifications.',
        'caption': 'Figure 106.1: Enterprise key lifecycle and encryption topology featuring Cloud KMS Key Rings, CryptoKey version rotation, service agent CMEK binding, application envelope encryption, and destruction protection safeguards.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Enterprise Key Custody & Cloud KMS Management Plane',
                'desc': 'Cloud KMS Key Rings, Software / HSM protection levels, automated rotation schedules, and IAM grant boundaries',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Cryptographic Service Agent Delegation & Token Exchange',
                'desc': 'Google Service Agents (Storage, BigQuery, Compute Engine) using roles/cloudkms.cryptoKeyEncrypterDecrypter',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Storage & Compute Resource CMEK Enforcement Plane',
                'desc': 'Encrypted Cloud Storage buckets, Persistent Disks, BigQuery datasets, and Cloud SQL instances',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Application-Layer Envelope Encryption & Client-Side Vault',
                'desc': 'Workload pods generating ephemeral local DEKs and wrapping with KMS KEKs via Google Tink library',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: External Key Manager (Cloud EKM) & Key Access Justifications (KAJ)',
                'desc': 'On-premise hardware security module validating policy justification headers for data sovereignty',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Cloud KMS Key Ring', 'detail': 'us-central1 / multi-region', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'CryptoKey v1 / v2', 'detail': 'Auto-Rotate (90 Days)', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'GCS Service Agent', 'detail': 'service-108@gs-project.iam', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Compute Service Agent', 'detail': 'CMEK Disk Decryption', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'CMEK Storage Bucket', 'detail': 'AES-256 Wrapped by KMS', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'CMEK Persistent Disk', 'detail': 'Encrypted VM Root Filesystem', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Tink Envelope Minter', 'detail': 'Ephemeral DEK Generator', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Field-Encrypted DB', 'detail': 'PAN / SSN Ciphertext Stored', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Cloud EKM Endpoint', 'detail': 'VPC Interconnect Route', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'KAJ Policy Evaluator', 'detail': 'Automated Reason Attestation', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'CLOUD KMS CRYPTOGRAPHIC CONTROL PLANE', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'MANAGED INFRASTRUCTURE CMEK ENCRYPTION BOUNDARY', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'APPLICATION ENVELOPE & SOVEREIGN EKM DOMAIN', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Promote Primary Version', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Grant EncrypterDecrypter', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Delegate Disk Key Wrap', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Enforce CMEK Policy', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Wrap Persistent Disk DEK', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Call KMS Encrypt (Tink)', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Persist Ciphertext to DB', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Forward Wrap via EKM', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Validate Justification', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: KMS Audit Log: Caller Identity & CryptoKey Version', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: GCS CMEK Binding Validation & Access Denied Catch', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 450, 'label': 'PROBE 3: Cloud EKM Justification Audit & Latency Telemetry', 'badge': 'P3', 'color': '#22c55e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world production data exposure incidents, key version mismanagement, '
        'unintended cryptographic shredding, and cross-boundary encryption failures. Each scenario details verbatim diagnostic '
        'logs, root cause mechanics, production remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on exercises implement the complete 8-stage operational engineering lifecycle for Day 106. '
        'Architects construct declarative Cloud KMS Key Rings and CryptoKeys with automated rotation, author CMEK storage '
        'policies, implement application-layer envelope encryption using Google Tink, and rehearse safe CryptoKey version management.'
    ),
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Data classification (public, internal, confidential, restricted)',
            'overview': (
                'Enterprise data governance begins with a formal, rigorous data classification taxonomy. Organizations '
                'categorize datasets into four standard sensitivity tiers: Public (freely disclosable), Internal (default business '
                'operations), Confidential (intellectual property, commercial contracts, customer telemetry), and Restricted '
                '(personally identifiable information, payment cards, healthcare records, cryptographic credentials). '
                'Classification dictates mandatory architectural controls, including encryption boundaries, access auditing, '
                'and geographic retention policies.'
            ),
            'preview': (
                'A development team stores unmasked credit card numbers in an Internal-tier cloud bucket; data classification '
                'policies enforce immediate migration to Restricted CMEK-encrypted vaults with strict DLP redaction.'
            ),
            'technical': (
                '### 1. Enterprise Four-Tier Data Classification Taxonomy\n'
                '- **Public Tier:** Marketing collateral, public documentation, API specifications. No confidentiality impact if '
                'disclosed; integrity protected by standard Google-managed encryption.\n'
                '- **Internal Tier:** Internal communication, operational logs, non-sensitive telemetry. Handled via standard IAM '
                'and organization-wide access boundaries.\n'
                '- **Confidential Tier:** Source code, strategic planning, business contracts. Requires dedicated IAM project '
                'isolation, audit logging enabled for all Data Access calls, and CMEK encryption.\n'
                '- **Restricted Tier:** Regulatory data (PCI-DSS, HIPAA, GDPR, PII, financial secrets). Requires CMEK backed by '
                'Cloud HSM or Cloud EKM, zero developer direct access, VPC Service Controls perimeter isolation, and automated '
                'Sensitive Data Protection (Cloud DLP) masking.\n'
                '\n'
                '### 2. Operational Invariants & Resource Tagging\n'
                '- Workloads apply Google Cloud Resource Manager Tags (e.g. `data-classification: restricted`) across projects, '
                'folders, and storage buckets.\n'
                '- Organization Policy constraints evaluate tags to enforce CMEK encryption automatically on all newly created '
                'Restricted storage buckets.'
            ),
            'questions': [
                'How does resource tagging bridge business data classification with automated Google Cloud technical enforcement?',
                'What are the mandatory architectural controls that must be applied to the Restricted data tier?',
                'Why is default Google-managed encryption insufficient for data classified under the Restricted tier?'
            ],
            'reference': 'https://cloud.google.com/architecture/framework/security/data-security#data-classification',
            'reference_label': 'Google Cloud Architecture Framework: Data classification and sensitivity management',
            'scenario': {
                'symptom': 'Security audit discovers unencrypted customer tax identifiers stored in an open BigQuery analytics dataset.',
                'constraints': 'Analytics team requires query access to statistical summaries, but plaintext government IDs must never be exposed.',
                'evidence': (
                    'Audit scan result from automated data discovery crawler:\n\n'
                    '```json\n'
                    '{\n'
                    '  "resource_name": "//bigquery.googleapis.com/projects/analytics-core/datasets/customer_telemetry",\n'
                    '  "findings": [\n'
                    '    {\n'
                    '      "info_type": "US_SOCIAL_SECURITY_NUMBER",\n'
                    '      "likelihood": "VERY_LIKELY",\n'
                    '      "record_count": 84210,\n'
                    '      "current_classification_tag": "internal",\n'
                    '      "required_classification_tag": "restricted"\n'
                    '    }\n'
                    '  ]\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: Developers classified the dataset as Internal because it was in an internal project, ignoring the '
                    'presence of Restricted PII within nested JSON columns.'
                ),
                'diagnostic_steps': [
                    'Execute Cloud DLP discovery scan across analytical tables to identify undetected infoTypes.',
                    'Review active Resource Manager Tags on the hosting BigQuery dataset and parent project.',
                    'Identify downstream query users and service accounts reading the raw unmasked columns.',
                    'Evaluate existing IAM bindings against the principle of least privilege.'
                ],
                'root': 'Data classification was assigned at the project level rather than verified against the underlying payload content.',
                'fix': 'Re-tag dataset as Restricted, isolate into a dedicated VPC-SC perimeter, deploy Cloud DLP de-identification, and enforce CMEK encryption.',
                'verify': 'Re-scan table with DLP to verify zero plaintext SSNs; verify analytical queries function via pseudonymized tokens.',
                'residual': 'Historical database backups taken prior to remediation must be scheduled for expedited purge.',
                'diagram': (
                    'Raw customer tax IDs stored in dataset tagged as Internal',
                    'Lack of DLP inspection allows Restricted data in broad project',
                    'Compliance audit flags critical violation and data leak risk',
                    'Enforce Restricted tag; tokenize PII and wrap dataset with CMEK',
                    'Sensitive data pseudonymized; dataset compliant with strict governance'
                )
            },
            'lab': {
                'name': 'Data Classification Matrix & Policy Enforcer',
                'goal': 'Map an enterprise dataset across the four-tier classification model and author a Python script that validates resource configurations against mandatory classification controls.',
                'expected': 'Classification policy specification file and functional Python compliance auditor validating storage encryption and perimeter tags.',
                'mode': 'Python CLI policy evaluation',
                'prereq': 'Python 3.9+ installed.',
                'preflight': 'Create clean working directory `~/data-class-lab`.',
                'steps': [
                    (
                        '#### Classification Matrix Authoring\n'
                        'Define declarative data classification policy assigning mandatory controls per tier:\n\n'
                        '```sh\n'
                        'mkdir -p ~/data-class-lab && cd ~/data-class-lab\n'
                        'cat <<\'EOF\' > classification_policy.json\n'
                        '{\n'
                        '  "public": {\n'
                        '    "min_encryption": "GOOGLE_MANAGED",\n'
                        '    "require_vpc_sc": false,\n'
                        '    "audit_data_access": false\n'
                        '  },\n'
                        '  "internal": {\n'
                        '    "min_encryption": "GOOGLE_MANAGED",\n'
                        '    "require_vpc_sc": false,\n'
                        '    "audit_data_access": true\n'
                        '  },\n'
                        '  "confidential": {\n'
                        '    "min_encryption": "CMEK_SOFTWARE",\n'
                        '    "require_vpc_sc": false,\n'
                        '    "audit_data_access": true\n'
                        '  },\n'
                        '  "restricted": {\n'
                        '    "min_encryption": "CMEK_HSM",\n'
                        '    "require_vpc_sc": true,\n'
                        '    "audit_data_access": true\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        'echo "[POLICY] Authored classification_policy.json"\n'
                        '```'
                    ),
                    (
                        '#### Compliance Auditor Implementation\n'
                        'Author and run an automated Python audit engine verifying resource configurations against data classification rules:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > audit_classification.py\n'
                        'import json\n'
                        '\n'
                        'policy = json.load(open("classification_policy.json"))\n'
                        '\n'
                        'resources = [\n'
                        '    {\n'
                        '        "name": "public-marketing-assets",\n'
                        '        "tag": "public",\n'
                        '        "encryption": "GOOGLE_MANAGED",\n'
                        '        "vpc_sc": false,\n'
                        '        "data_access_audit": false\n'
                        '    },\n'
                        '    {\n'
                        '        "name": "internal-employee-directory",\n'
                        '        "tag": "internal",\n'
                        '        "encryption": "GOOGLE_MANAGED",\n'
                        '        "vpc_sc": false,\n'
                        '        "data_access_audit": true\n'
                        '    },\n'
                        '    {\n'
                        '        "name": "confidential-financial-reports",\n'
                        '        "tag": "confidential",\n'
                        '        "encryption": "GOOGLE_MANAGED",  # VIOLATION: Requires CMEK\n'
                        '        "vpc_sc": false,\n'
                        '        "data_access_audit": true\n'
                        '    },\n'
                        '    {\n'
                        '        "name": "restricted-cardholder-vault",\n'
                        '        "tag": "restricted",\n'
                        '        "encryption": "CMEK_HSM",\n'
                        '        "vpc_sc": true,\n'
                        '        "data_access_audit": true\n'
                        '    }\n'
                        ']\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("DATA CLASSIFICATION TECHNICAL AUDIT ENGINE")\n'
                        'print("================================================================")\n'
                        'for res in resources:\n'
                        '    tier = res["tag"]\n'
                        '    reqs = policy.get(tier, {})\n'
                        '    violations = []\n'
                        '\n'
                        '    # Check encryption requirement\n'
                        '    if reqs.get("min_encryption") == "CMEK_HSM" and res["encryption"] != "CMEK_HSM":\n'
                        '        violations.append(f"Encryption is {res[\'encryption\']}, requires CMEK_HSM")\n'
                        '    elif reqs.get("min_encryption") == "CMEK_SOFTWARE" and res["encryption"] not in ["CMEK_SOFTWARE", "CMEK_HSM"]:\n'
                        '        violations.append(f"Encryption is {res[\'encryption\']}, requires CMEK_SOFTWARE or higher")\n'
                        '\n'
                        '    # Check VPC-SC requirement\n'
                        '    if reqs.get("require_vpc_sc") and not res["vpc_sc"]:\n'
                        '        violations.append("Missing required VPC Service Controls perimeter")\n'
                        '\n'
                        '    # Check Data Access audit\n'
                        '    if reqs.get("audit_data_access") and not res["data_access_audit"]:\n'
                        '        violations.append("Missing required Data Access audit logging")\n'
                        '\n'
                        '    status = "NON-COMPLIANT" if violations else "COMPLIANT"\n'
                        '    print(f"[{status:13s}] {res[\'name\']:30s} (Tier: {tier.upper()})")\n'
                        '    for v in violations:\n'
                        '        print(f"   -> DEFECT: {v}")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 audit_classification.py\n'
                        '```'
                    )
                ],
                'accept': 'Classification policy and Python audit transcript demonstrating deterministic detection of non-compliant storage resources.',
                'verification': 'Review terminal output showing `NON-COMPLIANT` status on `confidential-financial-reports` and `COMPLIANT` on other resources.',
                'trouble': 'If audit script reports syntax errors, verify valid JSON in `classification_policy.json`.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/data-class-lab</kbd>.',
                'file': 'day-106-data-classification.md'
            }
        },
        {
            'key': 'topic-02',
            'title': 'Encryption at rest (default Google-managed), CMEK (Cloud KMS), CSEK, external key manager…',
            'overview': (
                'Google Cloud provides multiple tiers of encryption at rest to satisfy diverse security, operational, and regulatory '
                'mandates. Default Google-managed encryption automatically protects all data at rest using AES-256 without customer '
                'intervention. Customer-Managed Encryption Keys (CMEK) via Cloud KMS allow organizations to control key lifecycle, '
                'rotation, and instant revocation. Customer-Supplied Encryption Keys (CSEK) pass raw keys in API headers per request. '
                'Cloud External Key Manager (Cloud EKM) allows storing keys on third-party HSMs outside Google Cloud, enforcing '
                'Key Access Justifications (KAJ) for cryptographic sovereignty.'
            ),
            'preview': (
                'An enterprise must revoke cloud database access immediately under subpoena; with CMEK, disabling the KMS CryptoKey '
                'renders all persistent storage blocks instantly unreadable without waiting for VM termination.'
            ),
            'technical': (
                '### 1. Cryptographic Mechanics of CMEK\n'
                '- **Two-Tier Envelope Hierarchy:** Workloads encrypt data using a local symmetric Data Encryption Key (DEK). The DEK '
                'is wrapped (encrypted) by a Key Encryption Key (KEK) hosted in Cloud KMS. Only the encrypted DEK is persisted alongside data.\n'
                '- **Service Agent Binding:** Google Cloud services (GCS, BigQuery, Compute Engine) access KMS using their dedicated '
                'service agents (e.g. `service-[PROJECT_NUM]@gs-project-accounts.iam.gserviceaccount.com`), requiring '
                '`roles/cloudkms.cryptoKeyEncrypterDecrypter`.\n'
                '- **Instant Revocation (Cryptographic Erasure):** Disabling a CryptoKey version or revoking the service agent IAM role '
                'immediately halts all data decryption across the resource, providing sub-second containment.\n'
                '\n'
                '### 2. CSEK vs. Cloud EKM\n'
                '- **CSEK Limitations:** CSEK keys are never written to disk or KMS; lost keys mean permanently lost data. Supported '
                'only on Compute Engine disks and Cloud Storage; incompatible with BigQuery, Cloud SQL, and most managed services.\n'
                '- **Cloud EKM with KAJ:** KMS delegates cryptographic wrapping to an external HSM over private interconnect or internet. '
                'Key Access Justifications (KAJ) evaluates automated policy justifications before permitting each external unwrap.'
            ),
            'questions': [
                'What is the operational consequence on active Compute Engine VMs if their backing CMEK disk CryptoKey is disabled?',
                'Why does Customer-Managed Encryption Keys (CMEK) utilize envelope encryption instead of passing the raw data through Cloud KMS APIs?',
                'What architectural guarantees does Cloud EKM provide that cannot be achieved with Cloud KMS HSM protection level?'
            ],
            'reference': 'https://cloud.google.com/kms/docs/envelope-encryption',
            'reference_label': 'Google Cloud KMS: Envelope encryption and customer-managed encryption keys overview',
            'scenario': {
                'symptom': 'Compute Engine instances in a mission-critical database cluster abruptly crash and fail to reboot with error `KMS_KEY_DISABLED`.',
                'constraints': 'Persistent disks are encrypted with CMEK; instances must remain online unless a verifiable breach requires manual shutdown.',
                'evidence': (
                    'Compute Engine system event log showing disk attachment termination:\n\n'
                    '```json\n'
                    '{\n'
                    '  "protoPayload": {\n'
                    '    "serviceName": "compute.googleapis.com",\n'
                    '    "methodName": "compute.instances.start",\n'
                    '    "status": {\n'
                    '      "code": 9,\n'
                    '      "message": "Key projects/brightloaf-sec/locations/us-central1/keyRings/prod-ring/cryptoKeys/disk-key is disabled."\n'
                    '    }\n'
                    '  }\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: A junior administrator mistakenly disabled the primary CryptoKey version in Cloud KMS while attempting '
                    'to rotate keys, instantly revoking disk read/write capability across all attached VMs.'
                ),
                'diagnostic_steps': [
                    'Extract the exact CryptoKey resource URI from the VM instance error details.',
                    'Inspect Cloud KMS key state using <kbd>gcloud kms keys describe</kbd> and <kbd>gcloud kms keys versions list</kbd>.',
                    'Query Cloud Audit logs for `SetCryptoKeyPrimaryVersion` and `UpdateCryptoKeyVersion` actions.',
                    'Check whether service agent permissions on the key ring remain intact.'
                ],
                'root': 'The primary CryptoKey version was manually disabled instead of creating a new version and updating the primary pointer.',
                'fix': 'Re-enable the disabled CryptoKey version immediately; configure automated rotation schedules to eliminate manual version interventions.',
                'verify': 'Verify CryptoKey status returns to `ENABLED`; trigger VM instance boot and verify root filesystem mounts cleanly.',
                'residual': 'Disabling a KMS key clears decrypted DEK caches within minutes, causing sudden crash-consistency states on active filesystems.',
                'diagram': (
                    'Admin disables KMS CryptoKey during erroneous manual rotation',
                    'Compute Engine service agent denied DEK unwrap permission',
                    'VM persistent disk I/O frozen; instance crashes with KMS_KEY_DISABLED',
                    'Re-enable CryptoKey version; automate 90-day rotation schedule',
                    'Service agent unwraps DEK; disk remounts and instances recover'
                )
            },
            'lab': {
                'name': 'CMEK Lifecycle & Service Agent Authorization Modeling',
                'goal': 'Configure declarative Terraform Cloud KMS Key Ring and CryptoKey with automated rotation, and simulate service agent envelope encryption and revocation.',
                'expected': 'Validated Terraform KMS manifest and Python envelope simulation demonstrating cryptographic erasure upon key disabling.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Terraform and Python 3 installed.',
                'preflight': 'Establish working directory `~/cmek-lab`.',
                'steps': [
                    (
                        '#### Declarative Cloud KMS Terraform Manifest\n'
                        'Author production Cloud KMS configuration with 90-day automated rotation and service agent IAM binding:\n\n'
                        '```sh\n'
                        'mkdir -p ~/cmek-lab && cd ~/cmek-lab\n'
                        'cat <<\'EOF\' > kms_cmek.tf\n'
                        'resource "google_kms_key_ring" "storage_keyring" {\n'
                        '  name     = "storage-encryption-keyring"\n'
                        '  location = "us-central1"\n'
                        '}\n'
                        '\n'
                        'resource "google_kms_crypto_key" "gcs_cmek_key" {\n'
                        '  name            = "gcs-bucket-key"\n'
                        '  key_ring        = google_kms_key_ring.storage_keyring.id\n'
                        '  rotation_period = "7776000s" # 90 days\n'
                        '\n'
                        '  version_template {\n'
                        '    algorithm        = "GOOGLE_SYMMETRIC_ENCRYPTION"\n'
                        '    protection_level = "SOFTWARE"\n'
                        '  }\n'
                        '}\n'
                        '\n'
                        '# Grant GCS service agent encrypter/decrypter role\n'
                        'resource "google_kms_crypto_key_iam_binding" "gcs_service_agent_binding" {\n'
                        '  crypto_key_id = google_kms_crypto_key.gcs_cmek_key.id\n'
                        '  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"\n'
                        '  members = [\n'
                        '    "serviceAccount:service-108420918237@gs-project-accounts.iam.gserviceaccount.com"\n'
                        '  ]\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored kms_cmek.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### Envelope Encryption & Cryptographic Erasure Simulation\n'
                        'Author a Python script demonstrating how DEK wrapping protects data and how key disabling achieves instant cryptographic shredding:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > test_cmek_erasure.py\n'
                        'import base64\n'
                        'import hashlib\n'
                        'import os\n'
                        '\n'
                        'class SimulatedCloudKMS:\n'
                        '    def __init__(self):\n'
                        '        self.kek = os.urandom(32)\n'
                        '        self.is_enabled = True\n'
                        '\n'
                        '    def wrap_dek(self, dek: bytes) -> bytes:\n'
                        '        if not self.is_enabled:\n'
                        '            raise PermissionError("CryptoKey is DISABLED: Decryption prohibited.")\n'
                        '        # Simulated XOR wrap with KEK hash\n'
                        '        mask = hashlib.sha256(self.kek).digest()\n'
                        '        return bytes(a ^ b for a, b in zip(dek, mask))\n'
                        '\n'
                        '    def unwrap_dek(self, wrapped_dek: bytes) -> bytes:\n'
                        '        if not self.is_enabled:\n'
                        '            raise PermissionError("CryptoKey is DISABLED: Decryption prohibited.")\n'
                        '        mask = hashlib.sha256(self.kek).digest()\n'
                        '        return bytes(a ^ b for a, b in zip(wrapped_dek, mask))\n'
                        '\n'
                        'kms = SimulatedCloudKMS()\n'
                        'plaintext = b"Brightloaf Confidential Financial Transaction Payload #48102"\n'
                        '\n'
                        '# 1. Generate local DEK and encrypt payload\n'
                        'dek = os.urandom(32)\n'
                        'wrapped_dek = kms.wrap_dek(dek)\n'
                        'ciphertext = bytes(p ^ (dek[i % len(dek)]) for i, p in enumerate(plaintext))\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("CMEK ENVELOPE ENCRYPTION & INSTANT ERASURE DEMO")\n'
                        'print("================================================================")\n'
                        'print(f"Original Plaintext: {plaintext.decode()}")\n'
                        'print(f"Wrapped DEK (Saved with Data): {base64.b64encode(wrapped_dek).decode()[:32]}...")\n'
                        '\n'
                        '# 2. Normal Read: Unwrap DEK and decrypt\n'
                        'recovered_dek = kms.unwrap_dek(wrapped_dek)\n'
                        'decrypted = bytes(c ^ (recovered_dek[i % len(recovered_dek)]) for i, c in enumerate(ciphertext))\n'
                        'print(f"Normal Read Recovery: {decrypted.decode()}")\n'
                        'assert decrypted == plaintext\n'
                        '\n'
                        '# 3. Cryptographic Erasure: Disable KMS Key\n'
                        'kms.is_enabled = False\n'
                        'print("\\n[ACTION] CryptoKey disabled by security team in Cloud KMS!")\n'
                        'try:\n'
                        '    kms.unwrap_dek(wrapped_dek)\n'
                        '    print("[FAIL] Decryption succeeded on disabled key!")\n'
                        'except PermissionError as e:\n'
                        '    print(f"[PASS] Instant Cryptographic Erasure Verified: {e}")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 test_cmek_erasure.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform Cloud KMS configuration with automated rotation and Python envelope encryption test proving instant cryptographic erasure.',
                'verification': 'Review terminal output of <kbd>python3 test_cmek_erasure.py</kbd> confirming permission denial when key is disabled.',
                'trouble': 'If Terraform fails validation, confirm valid service account syntax and 7776000s rotation period.',
                'cleanup': 'Remove test directory: <kbd>rm -rf ~/cmek-lab</kbd>.',
                'file': 'day-106-cmek-lifecycle.md'
            }
        },
        {
            'key': 'topic-03',
            'title': 'Encryption in transit and application-layer encryption',
            'overview': (
                'All network communication inside Google Cloud\'s physical data centers is encrypted by default at Layer 3 using '
                'Application Layer Transport Security (ALTS) and Cloud PSP (Packet Steering Processor). However, high-assurance '
                'compliance standards (e.g. PCI-DSS, HIPAA) require Application-Layer Encryption (ALE). By encrypting sensitive '
                'fields (such as credit card numbers or medical diagnosis codes) directly inside the client application memory using '
                'libraries like Google Tink before storing them in databases or message buses, data remains cryptographically protected '
                'even against compromised database administrators and storage infrastructure.'
            ),
            'preview': (
                'A database snapshot is exfiltrated by a malicious insider; application-layer field encryption ensures the stolen '
                'tables contain only undecryptable ciphertext without the external KMS key.'
            ),
            'technical': (
                '### 1. Google Cloud Encryption in Transit Tiers\n'
                '- **WAN & Inter-Region:** All traffic traversing Google\'s global private backbone between regions and data centers '
                'is encrypted at the hardware level using AES-256.\n'
                '- **Intra-Data Center (Intra-Zone):** Google Cloud encrypts VM-to-VM traffic within the same zone by default using '
                'PSP line-rate hardware encryption or ALTS.\n'
                '\n'
                '### 2. Application-Layer Field Encryption Mechanics\n'
                '- **Google Tink:** An open-source, multi-language cryptographic library built by Google engineers. It abstracts complex '
                'cryptographic primitives (preventing ECB mode and IV reuse vulnerabilities) into simple, robust APIs: AEAD '
                '(Authenticated Encryption with Associated Data) and Deterministic AEAD.\n'
                '- **Associated Data (AAD):** Workloads bind ciphertext cryptographically to metadata (e.g. `order_id` or `user_id`). '
                'If an attacker copies encrypted credit card ciphertext from Order A into Order B, the AEAD decryption algorithm '
                'fails with an integrity validation error.\n'
                '- **Deterministic vs. Non-Deterministic AEAD:** Non-deterministic AEAD generates a unique IV per call (optimal for security); '
                'Deterministic AEAD produces identical ciphertext for identical plaintext, enabling SQL database indexing and exact-match '
                'queries over encrypted columns.'
            ),
            'questions': [
                'Why does application-layer encryption provide stronger security isolation than database-level CMEK encryption?',
                'How does Authenticated Encryption with Associated Data (AEAD) prevent ciphertext transplantation attacks between database records?',
                'What is the security trade-off when using Deterministic AEAD compared to Non-Deterministic AEAD in relational databases?'
            ],
            'reference': 'https://developers.google.com/tink',
            'reference_label': 'Google Tink: Cryptographic library for multi-language application-layer encryption',
            'scenario': {
                'symptom': 'Security team discovers an SQL injection vulnerability in the legacy order history portal that allowed arbitrary SELECT queries.',
                'constraints': 'Cardholder Primary Account Numbers (PANs) must remain uncompromised even if the relational database is dumped.',
                'evidence': (
                    'Database dump extracted during tabletop penetration test:\n\n'
                    '```sql\n'
                    'SELECT order_id, customer_email, card_pan_encrypted, created_at FROM orders WHERE order_id = \'ORD-9912\';\n'
                    '+------------+-------------------+--------------------------------------------------------------+---------------------+\n'
                    '| order_id   | customer_email    | card_pan_encrypted                                           | created_at          |\n'
                    '+------------+-------------------+--------------------------------------------------------------+---------------------+\n'
                    '| ORD-9912   | jane@example.com  | tink:v1:aef810b42918cae7d1...[CIPHERTEXT 128B]...            | 2026-09-29 04:12:00 |\n'
                    '+------------+-------------------+--------------------------------------------------------------+---------------------+\n'
                    '```\n\n'
                    'Analysis: Because the application used Google Tink AEAD with `order_id` bound as Associated Data, the raw '
                    'database dump contained zero usable plaintext PANs, and ciphertexts could not be decrypted outside the payment microservice.'
                ),
                'diagnostic_steps': [
                    'Verify the encryption scheme applied to the `card_pan_encrypted` column.',
                    'Check whether the KMS KEK used to wrap the Tink keyset has public or cross-service IAM exposure.',
                    'Inspect application microservice code to confirm AEAD Associated Data binds to unique immutable row keys.',
                    'Audit Cloud KMS access logs for Decrypt calls matching the payment microservice service account.'
                ],
                'root': 'SQL injection vulnerability existed in web tier, but application-layer envelope encryption prevented data breach.',
                'fix': 'Patch SQL injection vulnerability with parameterized prepared statements; retain Tink application-layer field encryption.',
                'verify': 'Attempt decryption of extracted ciphertext without the payment microservice KMS key (fails with integrity error).',
                'residual': 'Keyset rotation must be scheduled annually, requiring dual-key decryption support in application code.',
                'diagram': (
                    'Attacker exploits SQL injection and dumps orders database table',
                    'Database table stores credit cards protected by Tink AEAD',
                    'Attacker obtains raw ciphertext but lacks KMS KEK access',
                    'Patch SQL injection flaw; maintain field-level envelope encryption',
                    'Zero plaintext leaked; database breach rendered cryptographically benign'
                )
            },
            'lab': {
                'name': 'Application-Layer Envelope Encryption with AEAD Associated Data',
                'goal': 'Implement a Python application-layer envelope encryption engine using AES-256-GCM with Associated Data and demonstrate tampering rejection.',
                'expected': 'Functional Python script encrypting field-level data, validating Associated Data integrity, and proving rejection of transplanted ciphertext.',
                'mode': 'Python cryptographic implementation',
                'prereq': 'Python 3.9+ and standard library.',
                'preflight': 'Establish working directory `~/app-enc-lab`.',
                'steps': [
                    (
                        '#### Application-Layer Cryptographic Engine\n'
                        'Author a pure-Python implementation of AEAD authenticated encryption with associated data binding:\n\n'
                        '```sh\n'
                        'mkdir -p ~/app-enc-lab && cd ~/app-enc-lab\n'
                        'cat <<\'EOF\' > app_encryption.py\n'
                        'import base64\n'
                        'import hashlib\n'
                        'import hmac\n'
                        'import os\n'
                        '\n'
                        'class ApplicationAEAD:\n'
                        '    """Simulated AES-256-GCM AEAD model with Associated Data binding."""\n'
                        '    def __init__(self, key: bytes):\n'
                        '        self.enc_key = hashlib.sha256(key + b":enc").digest()\n'
                        '        self.mac_key = hashlib.sha256(key + b":mac").digest()\n'
                        '\n'
                        '    def encrypt(self, plaintext: str, associated_data: str) -> dict:\n'
                        '        iv = os.urandom(16)\n'
                        '        pt_bytes = plaintext.encode("utf-8")\n'
                        '        # Stream cipher simulation (CTR/XOR with SHA256 keystream)\n'
                        '        keystream = hashlib.sha256(self.enc_key + iv).digest()\n'
                        '        ciphertext = bytes(p ^ (keystream[i % len(keystream)]) for i, p in enumerate(pt_bytes))\n'
                        '        # Authenticate ciphertext + associated data\n'
                        '        tag = hmac.new(self.mac_key, iv + ciphertext + associated_data.encode("utf-8"), hashlib.sha256).digest()\n'
                        '        return {\n'
                        '            "iv": base64.b64encode(iv).decode(),\n'
                        '            "ciphertext": base64.b64encode(ciphertext).decode(),\n'
                        '            "tag": base64.b64encode(tag).decode(),\n'
                        '            "aad": associated_data\n'
                        '        }\n'
                        '\n'
                        '    def decrypt(self, record: dict, associated_data: str) -> str:\n'
                        '        iv = base64.b64decode(record["iv"])\n'
                        '        ciphertext = base64.b64decode(record["ciphertext"])\n'
                        '        expected_tag = base64.b64decode(record["tag"])\n'
                        '\n'
                        '        # Verify HMAC tag including associated data\n'
                        '        actual_tag = hmac.new(self.mac_key, iv + ciphertext + associated_data.encode("utf-8"), hashlib.sha256).digest()\n'
                        '        if not hmac.compare_digest(expected_tag, actual_tag):\n'
                        '            raise ValueError("AEAD Authentication Tag Mismatch! Associated Data altered or ciphertext tampered.")\n'
                        '\n'
                        '        keystream = hashlib.sha256(self.enc_key + iv).digest()\n'
                        '        plaintext = bytes(c ^ (keystream[i % len(keystream)]) for i, c in enumerate(ciphertext))\n'
                        '        return plaintext.decode("utf-8")\n'
                        '\n'
                        '# Test Execution\n'
                        'master_key = os.urandom(32)\n'
                        'aead = ApplicationAEAD(master_key)\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("APPLICATION-LAYER AEAD ASSOCIATED DATA VALIDATION")\n'
                        'print("================================================================")\n'
                        'order_id = "ORD-48192"\n'
                        'pan = "4111-2222-3333-4444"\n'
                        '\n'
                        'record = aead.encrypt(pan, associated_data=f"order:{order_id}")\n'
                        'print(f"Original Card PAN: {pan}")\n'
                        'print(f"Associated Data Binding: order:{order_id}")\n'
                        'print(f"Stored Ciphertext: {record[\'ciphertext\']}")\n'
                        'print(f"Stored Tag:        {record[\'tag\']}")\n'
                        '\n'
                        '# Normal Decryption with valid Associated Data\n'
                        'recovered = aead.decrypt(record, associated_data=f"order:{order_id}")\n'
                        'print(f"\\n[PASS] Decrypted successfully with valid AAD: {recovered}")\n'
                        'assert recovered == pan\n'
                        '\n'
                        '# Negative Test: Transplant Attack (Inject into different order)\n'
                        'print("\\n[TEST] Simulating ciphertext transplantation to Order ORD-99999...")\n'
                        'try:\n'
                        '    aead.decrypt(record, associated_data="order:ORD-99999")\n'
                        '    print("[FAIL] Decryption unexpectedly succeeded with altered AAD!")\n'
                        'except ValueError as e:\n'
                        '    print(f"[PASS] Ciphertext transplant blocked by AEAD tag: {e}")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 app_encryption.py\n'
                        '```'
                    )
                ],
                'accept': 'Functional Python application encryption transcript demonstrating successful decryption with valid Associated Data and rejection upon transplantation.',
                'verification': 'Verify terminal output showing successful decryption and deterministic rejection on altered order binding.',
                'trouble': 'If decryption fails on valid data, check that the associated_data string matches character-for-character.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/app-enc-lab</kbd>.',
                'file': 'day-106-app-encryption.md'
            }
        },
        {
            'key': 'topic-04',
            'title': 'Cloud KMS',
            'overview': (
                'Google Cloud Key Management Service (Cloud KMS) is the unified cryptographic control plane for creating, '
                'managing, and controlling cryptographic keys across Google Cloud services and custom applications. '
                'Architects structure keys within Key Rings, define cryptographic algorithms (Symmetric AES, Asymmetric RSA/ECDSA, '
                'MAC), configure protection levels (Software, FIPS 140-2 Level 3 HSM, External EKM), manage CryptoKey version '
                'rotation, and enforce strict destruction safeguards to prevent irreversible data loss.'
            ),
            'preview': (
                'A scheduled key destruction job triggers on an active database key; Cloud KMS 24-hour destruction delay safeguards '
                'allow administrators to abort destruction and restore key versions before irreversible loss occurs.'
            ),
            'technical': (
                '### 1. Cloud KMS Resource Hierarchy & Key Rings\n'
                '- **Key Rings:** Regional or multi-regional logical containers that group CryptoKeys. Key Rings cannot be deleted or '
                'renamed, ensuring permanent auditability and preventing naming reuse attacks.\n'
                '- **CryptoKeys:** Named cryptographic objects within a Key Ring containing zero or more CryptoKeyVersions. Keys have a '
                'defined purpose (e.g. `ENCRYPT_DECRYPT`, `ASYMMETRIC_SIGN`, `MAC`).\n'
                '- **Protection Levels:**\n'
                '  - `SOFTWARE`: Fast, software-based keys validated against FIPS 140-2 Level 1.\n'
                '  - `HSM`: Hardware-backed keys running inside certified FIPS 140-2 Level 3 Hardware Security Modules.\n'
                '  - `EXTERNAL`: Cloud EKM keys hosted on third-party on-premise hardware.\n'
                '\n'
                '### 2. Key Version Lifecycle & Destruction Safeguards\n'
                '- **Lifecycle States:** `PENDING_GENERATION` -> `ENABLED` -> `DISABLED` -> `DESTROY_SCHEDULED` -> `DESTROYED`.\n'
                '- **Rotation Mechanics:** Rotating a key creates a new CryptoKeyVersion and sets it as the primary version for '
                'subsequent encrypt operations. Existing ciphertext encrypted with older versions remains decryptable as long as '
                'those versions remain `ENABLED`.\n'
                '- **Destruction Safeguards:** Cloud KMS enforces a mandatory minimum **24-hour scheduled destruction delay** '
                '(`destroy_scheduled_duration`). During this window, an administrator can call `RestoreCryptoKeyVersion` to halt '
                'destruction and prevent catastrophic permanent data shredding.'
            ),
            'questions': [
                'Why can Cloud KMS Key Rings and CryptoKeys never be deleted from a Google Cloud project?',
                'How does Cloud KMS ensure that older ciphertext remains decryptable after a key completes an automated rotation?',
                'What is the operational function of the 24-hour destruction delay on a CryptoKeyVersion?'
            ],
            'reference': 'https://cloud.google.com/kms/docs/key-rotation',
            'reference_label': 'Google Cloud KMS: Key rotation, version management, and destruction safeguards',
            'scenario': {
                'symptom': 'Continuous integration pipeline fails during automated database re-indexing with error `CRYPTOKEY_VERSION_DESTROY_SCHEDULED`.',
                'constraints': 'Legacy historical tables encrypted with CryptoKey version 1 must remain readable; destruction was triggered in error.',
                'evidence': (
                    'Cloud KMS Audit log showing destruction scheduling:\n\n'
                    '```json\n'
                    '{\n'
                    '  "protoPayload": {\n'
                    '    "serviceName": "cloudkms.googleapis.com",\n'
                    '    "methodName": "DestroyCryptoKeyVersion",\n'
                    '    "resourceName": "projects/prod-data/locations/us-central1/keyRings/warehouse/cryptoKeys/dw-key/cryptoKeyVersions/1",\n'
                    '    "status": {\n'
                    '      "code": 0,\n'
                    '      "message": "Scheduled for destruction at 2026-09-30T04:15:00Z (24h safety delay active)"\n'
                    '    }\n'
                    '  }\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: A cleanup script scheduled version 1 for destruction assuming version 2 was the primary, failing to '
                    'recognize that historical partition data from 2025 had not yet been re-wrapped with version 2.'
                ),
                'diagnostic_steps': [
                    'List all versions of the target CryptoKey using <kbd>gcloud kms keys versions list</kbd>.',
                    'Identify versions in the `DESTROY_SCHEDULED` state and note their scheduled destruction timestamps.',
                    'Verify whether any active storage objects or database blocks still reference the scheduled version.',
                    'Check IAM caller identity from the audit log to determine which script initiated the destruction.'
                ],
                'root': 'A cleanup automation script erroneously scheduled key version 1 for destruction before verifying all historical data had been re-encrypted.',
                'fix': 'Invoke `RestoreCryptoKeyVersion` within the 24-hour safety window to return version 1 to the `DISABLED` state, then re-enable for decryption.',
                'verify': 'Query historical database partitions; confirm successful decryption without KMS errors; author policy preventing automated destruction calls.',
                'residual': 'Once the 24-hour scheduled destruction delay elapses, the key material is permanently destroyed and data recovery is impossible.',
                'diagram': (
                    'Cleanup script erroneously schedules CryptoKey v1 for destruction',
                    'Historical data still encrypted with v1 fails decryption during re-index',
                    '24-hour destruction delay active; version in DESTROY_SCHEDULED state',
                    'Execute RestoreCryptoKeyVersion before 24-hour deadline expires',
                    'Key version restored to ENABLED; historical data remains decryptable'
                )
            },
            'lab': {
                'name': 'Cloud KMS Key Version Rotation & Safe Restoration Rehearsal',
                'goal': 'Author a declarative Cloud KMS key ring with multi-version rotation and implement a Python simulation of the complete key lifecycle including destruction scheduling and restoration.',
                'expected': 'Validated Terraform KMS manifest and Python script demonstrating version promotion, scheduled destruction, and emergency restore within the 24-hour safety window.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Python 3 and Terraform installed.',
                'preflight': 'Establish working directory `~/kms-lifecycle-lab`.',
                'steps': [
                    (
                        '#### Declarative Cloud KMS Lifecycle Configuration\n'
                        'Author a Terraform configuration specifying key destruction duration and rotation period:\n\n'
                        '```sh\n'
                        'mkdir -p ~/kms-lifecycle-lab && cd ~/kms-lifecycle-lab\n'
                        'cat <<\'EOF\' > kms_lifecycle.tf\n'
                        'resource "google_kms_key_ring" "vault_ring" {\n'
                        '  name     = "enterprise-vault-ring"\n'
                        '  location = "us-central1"\n'
                        '}\n'
                        '\n'
                        'resource "google_kms_crypto_key" "lifecycle_key" {\n'
                        '  name                        = "customer-ledger-key"\n'
                        '  key_ring                    = google_kms_key_ring.vault_ring.id\n'
                        '  rotation_period             = "7776000s" # 90 days\n'
                        '  destroy_scheduled_duration  = "86400s"   # 24 hour safety delay\n'
                        '\n'
                        '  version_template {\n'
                        '    algorithm        = "GOOGLE_SYMMETRIC_ENCRYPTION"\n'
                        '    protection_level = "HSM"\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored kms_lifecycle.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### KMS Version Lifecycle & Restoration Simulator\n'
                        'Author and run Python script modeling key rotation, destruction scheduling, and emergency restore:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > test_kms_lifecycle.py\n'
                        'import time\n'
                        '\n'
                        'class CryptoKeyVersion:\n'
                        '    def __init__(self, version_id: int):\n'
                        '        self.version_id = version_id\n'
                        '        self.state = "ENABLED"\n'
                        '        self.scheduled_destroy_time = None\n'
                        '\n'
                        'class ManagedCryptoKey:\n'
                        '    def __init__(self, name: str):\n'
                        '        self.name = name\n'
                        '        self.versions = [CryptoKeyVersion(1)]\n'
                        '        self.primary_version = 1\n'
                        '\n'
                        '    def rotate(self):\n'
                        '        new_id = len(self.versions) + 1\n'
                        '        new_ver = CryptoKeyVersion(new_id)\n'
                        '        self.versions.append(new_ver)\n'
                        '        self.primary_version = new_id\n'
                        '        print(f"[ROTATE] Generated Version {new_id}; promoted to Primary.")\n'
                        '\n'
                        '    def schedule_destroy(self, version_id: int, delay_seconds: int = 86400):\n'
                        '        ver = self.versions[version_id - 1]\n'
                        '        if ver.version_id == self.primary_version:\n'
                        '            raise ValueError("Cannot destroy primary key version!")\n'
                        '        ver.state = "DESTROY_SCHEDULED"\n'
                        '        ver.scheduled_destroy_time = time.time() + delay_seconds\n'
                        '        print(f"[DESTROY] Version {version_id} scheduled for destruction in {delay_seconds}s (Safety Window Active).")\n'
                        '\n'
                        '    def restore(self, version_id: int):\n'
                        '        ver = self.versions[version_id - 1]\n'
                        '        if ver.state != "DESTROY_SCHEDULED":\n'
                        '            raise ValueError("Only DESTROY_SCHEDULED versions can be restored.")\n'
                        '        ver.state = "DISABLED"\n'
                        '        ver.scheduled_destroy_time = None\n'
                        '        print(f"[RESTORE] Emergency restore succeeded! Version {version_id} recovered to DISABLED state.")\n'
                        '\n'
                        'key = ManagedCryptoKey("customer-ledger-key")\n'
                        'print("================================================================")\n'
                        'print("CLOUD KMS LIFECYCLE, ROTATION & RESTORATION TEST")\n'
                        'print("================================================================")\n'
                        'print(f"Initial State: Primary Version = {key.primary_version}, State = {key.versions[0].state}")\n'
                        '\n'
                        '# 1. Rotate Key\n'
                        'key.rotate()\n'
                        'print(f"After Rotation: Primary Version = {key.primary_version} (v1 remains ENABLED for decrypt)")\n'
                        '\n'
                        '# 2. Schedule v1 for Destruction\n'
                        'key.schedule_destroy(1, delay_seconds=86400)\n'
                        'print(f"Version 1 State: {key.versions[0].state}")\n'
                        '\n'
                        '# 3. Emergency Restore v1 before deadline\n'
                        'key.restore(1)\n'
                        'print(f"Version 1 Final State: {key.versions[0].state}")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 test_kms_lifecycle.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform Cloud KMS configuration with 24h destruction delay and Python simulation proving successful emergency key version restore.',
                'verification': 'Review terminal output of <kbd>python3 test_kms_lifecycle.py</kbd> confirming successful rotation, destroy scheduling, and emergency restore.',
                'trouble': 'If primary key destruction is attempted, script must raise ValueError preventing destruction of active primary key.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/kms-lifecycle-lab</kbd>.',
                'file': 'day-106-kms-lifecycle.md'
            }
        }
    ]
}
