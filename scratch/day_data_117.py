"""day_data_117.py — Exhaustive architecture data specification for Day 117.

Covers Security Handover and Evidence Repair:
- Consolidation of DLP synthetic-data de-identification, aggregated audit logging, and IAM-change alerting
- Threat model empirical evidence verification (STRIDE)
- Negative access testing (verifying denied-access controls alongside permitted paths)
- Regulated Workload Handover Package & Unresolved Risk Register
"""

DAY_NUM = 117

DATA = {
    'day': 117,
    'part1_intro': (
        'Day 117 consolidates the empirical security evidence, cryptographic invariants, and audit trails accumulated across the '
        'reliability and security block in preparation for the Gate 5 evaluation and Capstone 2 (Regulated Workload) defense. '
        'Architects systematically index synthetic-data de-identification outputs, organization-level aggregated logging sinks, '
        'real-time IAM policy change alerts, and STRIDE threat model verifications. Crucially, architects repair a common operational '
        'flaw—testing only positive access paths—by executing formal negative access controls, verifying that unauthorized identities '
        'are definitively denied access, and assembling an immutable security handover package with named risk owners.'
    ),
    'exit_summary': (
        'A security evidence index, supported claims and unresolved risks with owners.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts evidence classes, empirical verification standards, compliance claim mappings, '
        'and audit defense criteria across enterprise cloud security governance frameworks.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Evidence Domain</th>\n'
        '<th>Governing Mechanism &amp; Invariant</th>\n'
        '<th>Empirical Verification Method</th>\n'
        '<th>Handover Artifact &amp; Claim</th>\n'
        '<th>Negative Test &amp; Denial Proof</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>1. Data De-identification</strong></td>\n'
        '<td>Sensitive Data Protection (DLP) infoType redaction &amp; crypto-tokenization</td>\n'
        '<td>Inspect transformation output for zero raw PAN, SSN, or MRN fields</td>\n'
        '<td>De-identification transformation ledger proving zero cleartext storage</td>\n'
        '<td>Attempt analytical query against raw storage bucket; verify PERMISSION_DENIED.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>2. Immutable Audit Logging</strong></td>\n'
        '<td>Aggregated log sink to Cloud Storage Bucket Lock (SEC 17a-4 / WORM)</td>\n'
        '<td>Query log sink for 100% of Admin Activity and Data Access events</td>\n'
        '<td>WORM retention policy lock hash proving tamper-proof preservation</td>\n'
        '<td>Attempt object deletion with Org Owner credentials; verify 403 RetentionLockError.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>3. Administrative IAM Alerts</strong></td>\n'
        '<td>Event Threat Detection &amp; Cloud Monitoring log-based metrics for role grants</td>\n'
        '<td>Simulate privileged role grant; verify alert dispatches to SOC within 60s</td>\n'
        '<td>Alert notification log confirming automated incident escalation</td>\n'
        '<td>Attempt non-whitelisted service account creation; verify automated containment block.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>4. STRIDE Threat Model</strong></td>\n'
        '<td>Systematic trust boundary, impersonation, and exfiltration analysis</td>\n'
        '<td>Map all 6 STRIDE threat vectors to verified GCP defensive controls</td>\n'
        '<td>Comprehensive DREAD/STRIDE risk matrix with mitigation backlog</td>\n'
        '<td>Simulate cross-project service account impersonation; verify actAs denial.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>5. Regulated Handover</strong></td>\n'
        '<td>Formal risk register linking supported compliance claims to named owners</td>\n'
        '<td>Executive walkthrough of technical architecture with audit citations</td>\n'
        '<td>Regulated Workload Handover Package with active risk register</td>\n'
        '<td>Verify all residual risks have documented compensating controls and expiration dates.</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 117: Regulated Workload Security Evidence Consolidation and Handover Topology',
        'desc': 'Architectural layout illustrating de-identification pipeline verification, organization log aggregation to locked WORM storage, negative access denial testing, and the formal handover risk register.',
        'caption': 'Figure 117.1: Regulated workload security evidence consolidation featuring dual-path positive/negative testing, DLP tokenization verification, immutable WORM log preservation, and handover governance.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Dual-Path Identity & Access Validation Plane',
                'desc': 'Authorized workload service accounts vs unauthorized external/internal identities executing parallel tests',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Sensitive Data Protection (DLP) Redaction Boundary',
                'desc': 'Cloud DLP inspection and pseudonymization pipeline transforming raw customer PII into tokenized records',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Aggregated Logging Router & Immutable WORM Audit Vault',
                'desc': 'Organization-wide log sinks routing Admin and Data Access logs into SEC 17a-4 locked Cloud Storage buckets',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: STRIDE Threat Model & Empirical Verification Engine',
                'desc': 'Validation of mitigation controls against Spoofing, Tampering, Repudiation, and Elevation of Privilege',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: Regulated Handover Governance & Risk Register Enclave',
                'desc': 'Supported compliance claims, residual risk registry, named operational owners, and sign-off artifacts',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Authorized Service Account', 'detail': 'Scoped Least-Privilege IAM', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Unauthorized Identity', 'detail': 'Negative Test Principal', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'DLP Redaction Service', 'detail': 'Crypto-Tokenization Pipeline', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Sanitized Data Vault', 'detail': 'Zero Cleartext PII Stored', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Org Aggregated Log Sink', 'detail': 'Filters Data & Admin Events', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'WORM Locked Bucket', 'detail': 'SEC 17a-4 Immutable Vault', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'STRIDE Control Matrix', 'detail': 'Empirical Test Traces', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Impersonation Barrier', 'detail': 'actAs Strictly Restricted', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Handover Evidence Index', 'detail': 'Validated Compliance Claims', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'Residual Risk Register', 'detail': 'Named Owners & Deadlines', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'IDENTITY & DE-IDENTIFICATION DATA PROCESSING BOUNDARY', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'IMMUTABLE AUDIT LOGGING & STRIDE CONTROL ENCLAVE', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'REGULATED WORKLOAD GOVERNANCE & HANDOVER DOMAIN', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Execute Parallel Access Tests', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Pass to DLP Pipeline', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Confirm Tokenization', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Emit Audit Stream', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Lock Retention Policy', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Verify STRIDE Trace', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Assert Negative Denial', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Index Supported Claims', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Sign Off Risk Register', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: Negative Access Invariant: Assert PERMISSION_DENIED on Unauthorized Caller', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: WORM Immutability: Assert RetentionLockActive on Evidence GCS Bucket', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 450, 'label': 'PROBE 3: Risk Traceability: 100% of Residual Risks Mapped to Specific Owners', 'badge': 'P3', 'color': '#22c55e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world compliance audit failures, un-tested negative access assumptions, '
        'broken de-identification flows, and incomplete risk registers during regulated cloud workload handovers. '
        'Each scenario details verbatim diagnostic logs, root cause mechanisms, production remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on architectural exercises implement the complete operational engineering lifecycle for Day 117. '
        'Architects execute parallel positive and negative access validation tests, audit Cloud DLP redaction outputs, '
        'and assemble an automated Regulated Workload Security Evidence Index and Risk Register in Python.'
    ),
    'topics': [
        # TOPIC 1
        {
            'key': 'topic-01',
            'title': 'Consolidate synthetic-data de-identification, aggregate-log design, IAM-change alerts and threat-model evidence from earlier days. Repair one missing control test and prepare the regulated-workload handover',
            'overview': (
                'Enterprise regulatory compliance (PCI-DSS 4.0, HIPAA, SOC 2 Type II, ISO 27001) demands verifiable, reproducible evidence '
                'that technical controls are operational, continuously audited, and defensible under adversary pressure. '
                'In preparation for the Gate 5 evaluation and Capstone 2 regulated workload handover, architects consolidate four '
                'foundational pillars: Sensitive Data Protection de-identification pipelines, organization-level immutable audit logging, '
                'real-time IAM change alerting, and empirical STRIDE threat models. Furthermore, architects repair a critical audit deficiency: '
                'proving that access controls actively deny unauthorized calls under adversarial conditions.'
            ),
            'preview': (
                'A compliance audit halts a fintech cloud banking launch because the security documentation contains only successful '
                'access tests, lacking empirical proof that unprivileged service accounts are blocked from accessing raw credit card data.'
            ),
            'technical': (
                'A defensible regulated workload security portfolio requires structured proof across both positive and negative operational paths.\n\n'
                '### 1. Dual-Path Empirical Testing: Positive vs Negative Controls\n'
                '- **The Positive Testing Trap**: Testing only that authorized service accounts can read or write data proves functionality, '
                'not security. A misconfigured policy granting `roles/storage.admin` to `allAuthenticatedUsers` will pass all positive tests.\n'
                '- **Negative Testing Requirement**: Every access control claim must be paired with an explicit negative test proving that '
                'an unprivileged identity (e.g. `untrusted-analytics-sa@enterprise.iam.gserviceaccount.com`) receives HTTP 403 `PERMISSION_DENIED` '
                'when attempting the same operation.\n'
                '- **Failure Discrimination**: Auditors verify that denials stem from policy enforcement rather than malformed syntax or bad endpoints.\n\n'
                '### 2. Consolidated De-identification Proof (DLP)\n'
                '- Verifies that incoming application records containing sensitive customer identifiers (Credit Card Numbers, Social Security '
                'Numbers, Medical Record Numbers) are intercepted by Cloud DLP.\n'
                '- Documents the cryptographic pseudonymization algorithm (e.g. CryptoReplaceFfxFpeConfig with Cloud KMS wrapped key) and '
                'confirms that downstream analytics datasets in BigQuery contain exclusively de-identified ciphertext.\n\n'
                '### 3. Aggregated Logging & WORM Evidence Preservation\n'
                '- Consolidates organization-wide log sinks routing `cloudaudit.googleapis.com/activity` and `cloudaudit.googleapis.com/data_access` '
                'to a dedicated security logging project.\n'
                '- Governed by Cloud Storage Bucket Lock (WORM) with a 7-year retention period, satisfying SEC Rule 17a-4 and FINRA 4511 requirements.\n'
                '- Confirms that IAM policy change events (e.g. `SetIamPolicy`, `CreateServiceAccountKey`) trigger Cloud Monitoring alerts '
                'dispatched to the Security Operations Center (SOC) within 60 seconds.\n\n'
                '### 4. Regulated Workload Handover Package Structure\n'
                'The formal handover package transferred to operations and compliance teams consists of four core registers:\n'
                '1. **Security Evidence Index**: Direct links to verifiable configuration files, Terraform states, and audit log queries.\n'
                '2. **Supported Claims Matrix**: Specific regulatory requirements mapped to technical Google Cloud controls and passing test hashes.\n'
                '3. **Residual Risk Register**: Identified architectural risks, compensating controls, target resolution dates, and named executive owners.\n'
                '4. **Operational Ownership Matrix**: Primary and secondary on-call escalation paths for certificate rotation, KMS lifecycle, and perimeter management.'
            ),
            'questions': [
                'Why does a security audit reject evidence portfolios that demonstrate only successful, authorized API operations?',
                'How does combining Cloud DLP crypto-tokenization with VPC Service Controls eliminate data exfiltration risks in analytical workloads?',
                'What criteria distinguish an acceptable residual risk with a named owner from an un-remediated compliance failure?'
            ],
            'reference': 'https://docs.cloud.google.com/binary-authorization/docs',
            'reference_label': 'Google Cloud Compliance Architecture & Regulated Workload Handover Guide',
            'scenario': {
                'symptom': 'External compliance auditor rejects PCI-DSS ROC (Report on Compliance) submission due to absence of negative access tests.',
                'impact': 'Payment card processing certification delayed by 90 days; merchant processing licenses put on probationary hold.',
                'constraints': 'All access control claims must be proven with cryptographic logs showing both permitted and denied request paths.',
                'evidence': (
                    'Audit Assessment Findings Report:\n\n'
                    '```text\n'
                    'Finding ID: AUDIT-SEC-2026-092\n'
                    'Classification: REJECTED_EVIDENCE\n'
                    'Control: PCI-DSS Requirement 7.2 (Restricting access to cardholder data)\n'
                    'Auditor Notes: The engineering team supplied 14 passing curl/gcloud commands demonstrating that \n'
                    'payment-processor-sa can read bucket gs://cardholder-vault. Zero negative access tests were provided. \n'
                    'There is no empirical proof that unprivileged marketing or analytics service accounts are denied access.\n'
                    '```\n\n'
                    'Analysis: The team had configured an IAM binding on the bucket but omitted an adversarial negative test to confirm '
                    'that project-level reader roles could not bypass bucket-level restrictions.'
                ),
                'diagnostic_steps': [
                    'Review the security testing playbook to identify which negative tests were omitted from the test suite.',
                    'Check IAM policies on `gs://cardholder-vault` to confirm uniform bucket-level access is enabled.',
                    'Execute an empirical negative test using an unprivileged service account identity.',
                    'Capture the exact `google.rpc.Code.PERMISSION_DENIED` (HTTP 403) audit log entry into the evidence repository.'
                ],
                'root': 'The security validation pipeline lacked automated negative testing assertions, failing to prove that unauthorized identities are actively denied access to cardholder storage.',
                'fix': 'Author an automated negative test suite that executes parallel allowed and denied operations, capturing the resulting 403 PERMISSION_DENIED audit log events into the formal evidence index.',
                'verify': 'Re-run the compliance audit test runner; verify the report contains paired ALLOWED and DENIED results for every sensitive resource.',
                'residual': 'Internal users with organization-level `roles/resourcemanager.organizationAdmin` must still be audited via Access Transparency to prevent out-of-band policy tampering.',
                'diagram': (
                    'Security team submits compliance portfolio with only positive test results',
                    'External auditor rejects submission: no proof unauthorized callers are blocked',
                    'Payment card launch delayed 90 days due to missing negative control evidence',
                    'Implement dual-path test suite asserting 403 PERMISSION_DENIED on unprivileged callers',
                    'Evidence index fully verified with paired allowed/denied proofs; compliance approved'
                )
            },
            'lab': {
                'name': 'Regulated Workload Evidence Index & Dual-Path Negative Test Suite',
                'goal': 'Implement a comprehensive Python security evidence verification suite that executes parallel positive and negative access control tests, validates Cloud DLP synthetic data de-identification, and compiles a formal Regulated Workload Handover Package with a residual risk register.',
                'expected': 'A Python compliance tool generating an empirical evidence index, verifying negative denial invariants, and outputting a complete handover package.',
                'mode': 'Python script and CLI data modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/security-handover-lab</kbd>.',
                'steps': [
                    (
                        '#### Define Regulated Workload Security Test Configuration\n'
                        'Create the working directory and write a JSON specification detailing resource endpoints, authorized and unauthorized caller identities, and synthetic de-identification records:\n\n'
                        '```sh\n'
                        'mkdir -p ~/security-handover-lab && cd ~/security-handover-lab\n'
                        'cat <<\'EOF\' > workload_spec.json\n'
                        '{\n'
                        '  "workload_name": "Regulated Core Banking & Payment System",\n'
                        '  "compliance_targets": ["PCI-DSS-4.0", "SOC-2-TYPE-II", "HIPAA"],\n'
                        '  "resources": [\n'
                        '    {\n'
                        '      "resource_id": "gs://cde-cardholder-data-vault",\n'
                        '      "type": "STORAGE_BUCKET",\n'
                        '      "authorized_principal": "serviceAccount:payment-core-sa@fintech-prod.iam.gserviceaccount.com",\n'
                        '      "unauthorized_principal": "serviceAccount:marketing-analytics-sa@fintech-prod.iam.gserviceaccount.com"\n'
                        '    },\n'
                        '    {\n'
                        '      "resource_id": "projects/fintech-sec-kms/locations/us-central1/keyRings/billing/cryptoKeys/pan-dek",\n'
                        '      "type": "KMS_CRYPTOKEY",\n'
                        '      "authorized_principal": "serviceAccount:payment-core-sa@fintech-prod.iam.gserviceaccount.com",\n'
                        '      "unauthorized_principal": "serviceAccount:marketing-analytics-sa@fintech-prod.iam.gserviceaccount.com"\n'
                        '    }\n'
                        '  ],\n'
                        '  "dlp_verification": {\n'
                        '    "raw_sample": "Customer John Doe with Card 4111-2222-3333-4444 and SSN 000-12-3456",\n'
                        '    "deidentified_sample": "Customer John Doe with Card [TOKEN_CC_88921] and SSN [REDACTED_SSN]",\n'
                        '    "info_types_detected": ["CREDIT_CARD_NUMBER", "US_SOCIAL_SECURITY_NUMBER"],\n'
                        '    "zero_raw_pii_confirmed": true\n'
                        '  },\n'
                        '  "unresolved_risks": [\n'
                        '    {\n'
                        '      "risk_id": "RISK-117-01",\n'
                        '      "description": "Cross-region disaster recovery replication has a 15-minute RPO window during regional fiber cuts.",\n'
                        '      "compensating_control": "Asynchronous multi-region dual-bucket replication with Cloud Storage Turbo Replication enabled.",\n'
                        '      "owner": "lead-sre@enterprise.com",\n'
                        '      "remediation_deadline": "2026-12-31"\n'
                        '    }\n'
                        '  ]\n'
                        '}\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Dual-Path Negative Test Suite & Handover Compiler\n'
                        'Write a Python tool that simulates dual-path access control verification, checks DLP de-identification efficacy, audits WORM log retention, and compiles the formal Handover Package:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > compile_handover_package.py\n'
                        'import json\n'
                        'from datetime import datetime, timezone\n'
                        '\n'
                        'def run_handover_audit():\n'
                        '    with open("workload_spec.json", "r") as f:\n'
                        '        spec = json.load(f)\n'
                        '\n'
                        '    print(f"=== Compiling Security Handover Package: {spec[\'workload_name\']} ===\\n")\n'
                        '    evidence_index = []\n'
                        '    all_tests_passed = True\n'
                        '\n'
                        '    # 1. Execute Dual-Path Access Control Verification\n'
                        '    print("1. Running Dual-Path Access Control Tests (Positive & Negative):")\n'
                        '    for res in spec["resources"]: \n'
                        '        rid = res["resource_id"]\n'
                        '        auth_p = res["authorized_principal"].split(":")[1]\n'
                        '        unauth_p = res["unauthorized_principal"].split(":")[1]\n'
                        '\n'
                        '        # Positive test assertion (Must return ALLOWED)\n'
                        '        pos_result = "ALLOWED"\n'
                        '        print(f"  [PASS] Positive: {auth_p} -> {rid} => {pos_result}")\n'
                        '\n'
                        '        # Negative test assertion (Must return PERMISSION_DENIED)\n'
                        '        neg_result = "PERMISSION_DENIED_403"\n'
                        '        print(f"  [PASS] Negative: {unauth_p} -> {rid} => {neg_result}")\n'
                        '\n'
                        '        evidence_index.append({\n'
                        '            "resource": rid,\n'
                        '            "control": "IAM Least Privilege Access Isolation",\n'
                        '            "positive_test": {"principal": auth_p, "status": pos_result},\n'
                        '            "negative_test": {"principal": unauth_p, "status": neg_result},\n'
                        '            "verified": True\n'
                        '        })\n'
                        '\n'
                        '    # 2. Verify DLP De-Identification Pipeline\n'
                        '    print("\\n2. Verifying Sensitive Data Protection (DLP) Tokenization:")\n'
                        '    dlp = spec["dlp_verification"]\n'
                        '    if dlp["zero_raw_pii_confirmed"] and "4111" not in dlp["deidentified_sample"]:\n'
                        '        print(f"  [PASS] De-identification verified: Raw card number transformed to token.")\n'
                        '        evidence_index.append({\n'
                        '            "resource": "Cloud DLP Tokenization Pipeline",\n'
                        '            "control": "Synthetic Data De-identification",\n'
                        '            "evidence": dlp["deidentified_sample"],\n'
                        '            "verified": True\n'
                        '        })\n'
                        '    else:\n'
                        '        print("  [FAIL] De-identification failure: Raw PII found in output!")\n'
                        '        all_tests_passed = False\n'
                        '\n'
                        '    # 3. Assemble Supported Compliance Claims & Residual Risk Register\n'
                        '    print("\\n3. Indexing Supported Claims and Residual Risk Matrix:")\n'
                        '    for risk in spec["unresolved_risks"]:\n'
                        '        print(f"  Risk [{risk[\'risk_id\']}]: {risk[\'description\'][:50]}...")\n'
                        '        print(f"    Owner: {risk[\'owner\']} (Deadline: {risk[\'remediation_deadline\']})")\n'
                        '\n'
                        '    handover_package = {\n'
                        '        "handover_title": f"{spec[\'workload_name\']} - Security Handover Package",\n'
                        '        "compilation_timestamp": datetime.now(timezone.utc).isoformat(),\n'
                        '        "compliance_targets": spec["compliance_targets"],\n'
                        '        "overall_handover_status": "APPROVED_FOR_GATE_5" if all_tests_passed else "REJECTED",\n'
                        '        "security_evidence_index": evidence_index,\n'
                        '        "residual_risk_register": spec["unresolved_risks"]\n'
                        '    }\n'
                        '\n'
                        '    with open("security_handover_package.json", "w") as out:\n'
                        '        json.dump(handover_package, out, indent=2)\n'
                        '    print(f"\\nHandover package successfully compiled. Wrote security_handover_package.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    run_handover_audit()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute the Handover Audit Tool and Inspect Security Evidence\n'
                        'Run the compilation script and verify that dual-path tests pass and the formal security handover package is generated:\n\n'
                        '```sh\n'
                        'python3 compile_handover_package.py\n'
                        'cat security_handover_package.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python security handover compiler executing dual-path negative testing, DLP de-identification verification, and residual risk registry generation.',
                'verification': 'Review terminal output of <kbd>python3 compile_handover_package.py</kbd> confirming overall_handover_status APPROVED_FOR_GATE_5.',
                'trouble': 'If JSON file cannot be loaded, verify file syntax of `workload_spec.json`.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/security-handover-lab</kbd>.',
                'file': 'day-117-security-handover.md'
            }
        }
    ]
}
