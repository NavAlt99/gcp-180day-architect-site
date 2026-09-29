"""day_data_109.py — Exhaustive architecture data specification for Day 109.

Covers Shared Responsibility for Compliance, Standards at a Conceptual Level
(ISO 27001, SOC 1/2/3, PCI-DSS, HIPAA, GDPR, FedRAMP, NIST, CIS, HITRUST),
and Compliance Resource Center & Compliance Reports Manager.
"""

DAY_NUM = 109

DATA = {
    'day': 109,
    'part1_intro': (
        'Day 109 establishes the enterprise regulatory compliance architecture, audit evidence governance, and the shared '
        'responsibility model for certified workloads across Google Cloud. Architects examine the critical distinction '
        'between Google Cloud\'s underlying infrastructure certifications and customer application-level compliance obligations, '
        'the technical control mappings across major standards (ISO/IEC 27001, SOC 1/2/3, PCI-DSS v4.0, HIPAA, GDPR, FedRAMP High, '
        'NIST SP 800-53, CIS Benchmarks, HITRUST CSF), and the operational workflows for retrieving authoritative third-party '
        'attestations via the Google Cloud Compliance Reports Manager.'
    ),
    'exit_summary': (
        'Engineers construct and verify an enterprise regulatory control and evidence register distinguishing provider certifications '
        'from customer obligations, an automated CIS Google Cloud Foundations benchmark auditor, and an audit evidence collection '
        'pipeline fulfilling all Day 109 Exit evidence criteria.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts major regulatory frameworks, their core security requirements, Google Cloud\'s '
        'inherited control boundaries, and the mandatory customer-managed technical controls.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Compliance Framework</th>\n'
        '<th>Primary Regulatory Focus</th>\n'
        '<th>Google Cloud Inherited Controls</th>\n'
        '<th>Customer Workload Responsibilities</th>\n'
        '<th>Primary Audit Artifact / Evidence</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>SOC 2 Type II</strong></td>\n'
        '<td>Security, Availability, Confidentiality, Processing Integrity</td>\n'
        '<td>Physical data center security, hypervisor isolation, background checks</td>\n'
        '<td>IAM least privilege, VPC network firewalls, change management, backup drills</td>\n'
        '<td>Independent CPA Service Auditor\'s Report via Compliance Reports Manager</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>PCI-DSS v4.0</strong></td>\n'
        '<td>Cardholder Data Environment (CDE) protection</td>\n'
        '<td>Physical hardware security, underlying network segmentation</td>\n'
        '<td>CDE network perimeter, application-layer tokenization, annual penetration tests</td>\n'
        '<td>Google Cloud Attestation of Compliance (AoC) &amp; Customer Responsibility Matrix (CRM)</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>HIPAA / HITECH</strong></td>\n'
        '<td>Protected Health Information (PHI) safeguards</td>\n'
        '<td>Google Business Associate Agreement (BAA), physical &amp; platform encryption</td>\n'
        '<td>Execute BAA before ingestion, enable Cloud Audit Data Access logs, restrict IAM access</td>\n'
        '<td>Executed Google Cloud BAA agreement &amp; immutable audit log retention sinks</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>FedRAMP High</strong></td>\n'
        '<td>US Federal civilian security standards (NIST SP 800-53)</td>\n'
        '<td>Federal boundary physical security, personnel screening, supply chain</td>\n'
        '<td>Assured Workloads deployment, FIPS 140-2 Level 3 HSM encryption, CAC/PVI access</td>\n'
        '<td>FedRAMP Joint Authorization Board (JAB) Provisional Authorization to Operate (P-ATO)</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>ISO/IEC 27001:2022</strong></td>\n'
        '<td>Information Security Management System (ISMS)</td>\n'
        '<td>Comprehensive organizational security program, data center physical controls</td>\n'
        '<td>Workload risk assessments, security incident response runbooks, CI/CD code scanning</td>\n'
        '<td>ISO/IEC 27001 Certificate of Registration issued by accredited registrar</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 109: Shared Responsibility for Compliance & Audit Evidence Pipeline Topology',
        'desc': 'Architectural layout illustrating Google Cloud inherited physical certifications, customer workload security controls, Compliance Reports Manager, and immutable audit evidence collection.',
        'caption': 'Figure 109.1: Enterprise compliance governance architecture detailing inherited physical and infrastructure certifications, customer workload responsibilities, and automated audit evidence harvesting.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Google Cloud Infrastructure & Certified Physical Foundation',
                'desc': 'Physical data centers, server hardware, fiber backbones, hypervisor isolation, and SOC/ISO audits',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Compliance Resource Center & Third-Party Audit Reports Plane',
                'desc': 'Compliance Reports Manager delivering independent SOC 1/2/3, ISO 27001, and PCI AoC attestations',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Customer Managed Infrastructure & Policy Guardrail Boundary',
                'desc': 'VPC firewall configurations, IAM least-privilege roles, Organization Policies, and CMEK key rings',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Application Workload, Identity & Data Protection Boundary',
                'desc': 'Customer application code, user authentication, data classification, and Cloud DLP de-identification',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: Immutable Audit Evidence Vault & Compliance Auditor Interface',
                'desc': 'Locked Cloud Storage sinks, Cloud Logging exports, Security Command Center posture, and auditor reviews',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Physical Data Centers', 'detail': 'FIPS / Biometric Perimeter', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Google Infrastructure SOC', 'detail': 'SOC 2 Type II Certified', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Compliance Reports Manager', 'detail': 'Self-Service NDA Portal', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Customer Responsibility Matrix', 'detail': 'Shared Fate Guidance', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'VPC Service Controls', 'detail': 'Customer Data Perimeter', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'CMEK Key Management', 'detail': 'Customer Key Custody', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Application Code & Auth', 'detail': 'Customer User Lifecycle', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'DLP Tokenization Pipe', 'detail': 'Format-Preserving Masking', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Locked Audit Log Sink', 'detail': 'SEC 17a-4 Compliant Bucket', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'External Auditor Portal', 'detail': 'Verifies Control Evidence', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'GOOGLE CLOUD INHERITED CERTIFICATION ENVELOPE', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'CUSTOMER WORKLOAD & PLATFORM RESPONSIBILITY DOMAIN', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'COMPLIANCE AUDIT EVIDENCE & ATTESTATION VAULT', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Attest Physical Security', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Publish Audit Reports', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Define Shared Controls', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Enforce Customer Guardrails', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Wrap with Customer Keys', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Deploy Workload Logic', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'De-Identify Customer PII', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Export Immutable Logs', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Deliver Audit Evidence', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: Google SOC 2 Type II Attestation Validity Check', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: CIS Benchmark Automated Configuration Audit', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 450, 'label': 'PROBE 3: Audit Log Retention Lock & Tamper-Proof Assertion', 'badge': 'P3', 'color': '#22c55e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world compliance audit failures, the dangerous fallacy of inherited '
        'compliance assumptions, and missing audit evidence during external regulator inspections. Each scenario details verbatim '
        'findings, root causes, remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on exercises execute the complete 8-stage operational engineering lifecycle for Day 109. '
        'Architects construct an automated CIS Google Cloud Foundations benchmark checker, build an enterprise compliance '
        'control-and-evidence register, and simulate audit evidence harvesting from Cloud Audit logs.'
    ),
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Shared responsibility for compliance (Google\'s certifications do not make your workload…',
            'overview': (
                'A dangerous and recurring enterprise architectural anti-pattern is assuming that deploying a workload into '
                'Google Cloud automatically inherits Google\'s compliance certifications. While Google Cloud is certified under '
                'ISO 27001, SOC 2, PCI-DSS, and FedRAMP, this certification covers only the underlying physical data centers, '
                'hardware, and managed hypervisors. The customer remains 100% accountable for application configuration, IAM '
                'least privilege, firewall rule authoring, encryption key governance, vulnerability management, and audit logging.'
            ),
            'preview': (
                'An enterprise fintech startup assumes its app is PCI-compliant because it runs on GCP; the external Qualified '
                'Security Assessor (QSA) fails the audit due to unencrypted public storage buckets and broad IAM permissions.'
            ),
            'technical': (
                '### 1. Shared Responsibility vs. Shared Fate\n'
                '- **Infrastructure Layer (Google):** Physical data center security, environmental controls, hardware lifecycle '
                'destruction, hypervisor kernel isolation, and underlying network encryption.\n'
                '- **Platform & Configuration Layer (Shared):** Service agents, managed platform patch cycles (e.g. Cloud Run, GKE), '
                'and baseline API security features.\n'
                '- **Workload & Data Layer (Customer):** Identity lifecycle, IAM role bindings, VPC routing, data classification, '
                'CMEK rotation, application vulnerability remediation, and audit log monitoring.\n'
                '\n'
                '### 2. The Customer Responsibility Matrix (CRM)\n'
                '- For frameworks like PCI-DSS and FedRAMP, Google publishes a Customer Responsibility Matrix (CRM) mapping every '
                'individual requirement (e.g. PCI Requirement 10: Log and Monitor All Access) to specific customer actions.'
            ),
            'questions': [
                'Why does hosting an application on a PCI-DSS certified cloud provider like Google Cloud not make the application automatically PCI compliant?',
                'What is the operational function of the Google Cloud Customer Responsibility Matrix (CRM)?',
                'Which compliance controls remain strictly customer responsibilities regardless of whether IaaS, PaaS, or SaaS is chosen?'
            ],
            'reference': 'https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate',
            'reference_label': 'Google Cloud Architecture Framework: Shared responsibility and shared fate models',
            'scenario': {
                'symptom': 'External PCI Qualified Security Assessor (QSA) halts an annual compliance audit, issuing an immediate Failure notice for Requirement 1 (Network Security Controls).',
                'constraints': 'Cardholder Data Environment (CDE) must pass annual PCI-DSS Level 1 assessment to maintain credit card processing authorization.',
                'evidence': (
                    'QSA Assessment Deficiency Notice excerpt:\n\n'
                    '```text\n'
                    'PCI-DSS v4.0 Non-Compliance Finding: Req 1.2.1 / 1.3.1\n'
                    'Finding: Customer CDE VPC network contains default ingress firewall rule "default-allow-ssh" permitting 0.0.0.0/0 on port 22.\n'
                    'Customer Defense: "GCP is PCI-certified; infrastructure firewalls are Google\'s responsibility."\n'
                    'QSA Finding: REJECTED. Ingress firewall configuration is explicitly designated as Customer Responsibility in the Google Cloud PCI CRM.\n'
                    '```\n\n'
                    'Analysis: The cloud engineering team left default VPC networks and open ingress firewall rules active, '
                    'operating under the mistaken belief that Google managed firewall ingress policies.'
                ),
                'diagnostic_steps': [
                    'Review the Google Cloud PCI-DSS Customer Responsibility Matrix for Requirement 1.',
                    'Audit all VPC networks in the CDE project using <kbd>gcloud compute firewall-rules list</kbd>.',
                    'Identify and isolate instances with public external IP addresses.',
                    'Inspect Cloud Audit logs for unauthorized SSH access attempts from the internet.'
                ],
                'root': 'Engineering team confused cloud provider physical network certification with customer VPC firewall configuration duties.',
                'fix': 'Deprovision default VPC networks, delete all `0.0.0.0/0` administrative ingress rules, enforce IAP TCP forwarding, and apply deny-by-default firewall policies.',
                'verify': 'Re-scan VPC with automated security posture scanner; confirm 100% compliance with PCI-DSS network segmentation rules.',
                'residual': 'Third-party vendor SaaS integrations crossing the CDE boundary require continuous reciprocal firewall auditing.',
                'diagram': (
                    'Customer deploys CDE workload onto GCP with open default firewall',
                    'Engineering team assumes Google PCI certification covers VPC rules',
                    'External QSA auditor flags open port 22 and halts PCI certification',
                    'Delete default rules; enforce deny-by-default and IAP tunneling',
                    'VPC network secured; QSA verifies compliance with PCI CRM'
                )
            },
            'lab': {
                'name': 'Shared Responsibility Compliance Auditor & Firewall Sanitizer',
                'goal': 'Author a Python audit tool that evaluates Google Cloud VPC firewall configurations against CIS and PCI-DSS shared responsibility mandates.',
                'expected': 'Functional Python compliance checker identifying open administrative ingress rules and generating an actionable remediation plan.',
                'mode': 'Python CLI audit implementation',
                'prereq': 'Python 3.9+ installed.',
                'preflight': 'Establish working directory `~/compliance-audit-lab`.',
                'steps': [
                    (
                        '#### Compliance Firewall Auditor Implementation\n'
                        'Author and run a Python script evaluating firewall rule definitions against PCI-DSS Requirement 1:\n\n'
                        '```sh\n'
                        'mkdir -p ~/compliance-audit-lab && cd ~/compliance-audit-lab\n'
                        'cat <<\'EOF\' > audit_firewall_compliance.py\n'
                        'firewall_rules = [\n'
                        '    {\n'
                        '        "name": "default-allow-ssh",\n'
                        '        "source": "0.0.0.0/0",\n'
                        '        "port": 22,\n'
                        '        "action": "ALLOW",\n'
                        '        "network": "default"\n'
                        '    },\n'
                        '    {\n'
                        '        "name": "default-allow-rdp",\n'
                        '        "source": "0.0.0.0/0",\n'
                        '        "port": 3389,\n'
                        '        "action": "ALLOW",\n'
                        '        "network": "default"\n'
                        '    },\n'
                        '    {\n'
                        '        "name": "allow-iap-admin-ssh",\n'
                        '        "source": "35.235.240.0/20",\n'
                        '        "port": 22,\n'
                        '        "action": "ALLOW",\n'
                        '        "network": "cde-vpc"\n'
                        '    },\n'
                        '    {\n'
                        '        "name": "allow-internal-mesh",\n'
                        '        "source": "10.128.0.0/16",\n'
                        '        "port": 8443,\n'
                        '        "action": "ALLOW",\n'
                        '        "network": "cde-vpc"\n'
                        '    }\n'
                        ']\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("PCI-DSS / CIS BENCHMARK FIREWALL COMPLIANCE AUDITOR")\n'
                        'print("================================================================")\n'
                        '\n'
                        'def evaluate_rule(rule: dict) -> tuple[bool, str]:\n'
                        '    if rule["source"] == "0.0.0.0/0" and rule["port"] in [22, 3389] and rule["action"] == "ALLOW":\n'
                        '        return False, f"CRITICAL DEFICIENCY: Port {rule[\'port\']} exposed to public internet (0.0.0.0/0)"\n'
                        '    if rule["network"] == "default":\n'
                        '        return False, "HIGH DEFICIENCY: Use of legacy default VPC network in CDE"\n'
                        '    return True, "COMPLIANT (Scoped source and authorized network)"\n'
                        '\n'
                        'for r in firewall_rules:\n'
                        '    passed, reason = evaluate_rule(r)\n'
                        '    status = "PASS" if passed else "FAIL"\n'
                        '    print(f"[{status:4s}] Rule: {r[\'name\']:24s} | Network: {r[\'network\']:8s} | Result: {reason}")\n'
                        '\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 audit_firewall_compliance.py\n'
                        '```'
                    )
                ],
                'accept': 'Functional Python firewall compliance auditor demonstrating deterministic identification of non-compliant public rules.',
                'verification': 'Review terminal output of <kbd>python3 audit_firewall_compliance.py</kbd> verifying failures flagged on default rules.',
                'trouble': 'If compliant rules are flagged, verify CIDR parsing logic.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/compliance-audit-lab</kbd>.',
                'file': 'day-109-shared-responsibility.md'
            }
        },
        {
            'key': 'topic-02',
            'title': 'Standards to know at a conceptual level',
            'overview': (
                'Enterprise cloud architects must master the conceptual landscape of global compliance standards and technical '
                'control frameworks. Key regimes include ISO/IEC 27001 (information security management systems), SOC 1/2/3 '
                '(internal controls and trust services criteria), PCI-DSS v4.0 (cardholder data environment segmentation and encryption), '
                'HIPAA (health information privacy and security), GDPR (European data protection, data residency, and right to erasure), '
                'FedRAMP (federal civilian security baselines), NIST SP 800-53 (security and privacy controls), CIS Benchmarks '
                '(prescriptive configuration hardening), and HITRUST CSF (unified health and financial assurance).'
            ),
            'preview': (
                'A healthcare client requires immediate verification of HIPAA compliance; architects map required technical safeguards '
                'directly to executed Google Cloud BAAs, CMEK encryption, and immutable audit log exports.'
            ),
            'technical': (
                '### 1. Framework Taxonomy & Cross-Mapping\n'
                '- **Broad Governance & Management:** ISO/IEC 27001 (Plan-Do-Check-Act ISMS lifecycle), SOC 2 Type II (attestation '
                'evaluating operational effectiveness over a minimum 6-month period across Security, Availability, and Confidentiality).\n'
                '- **Prescriptive Technical Hardening:** CIS Google Cloud Foundations Benchmark (actionable configuration rules for IAM, '
                'Logging, Networking, and Storage), NIST SP 800-53 Rev 5 (comprehensive catalog of federal security controls).\n'
                '- **Domain-Specific Regimes:** PCI-DSS v4.0 (Payment cards, CDE scope reduction via tokenization), HIPAA / HITECH '
                '(PHI protection via Business Associate Agreements), GDPR (EU data subject rights, right to erasure, data transfer SCCs).\n'
                '\n'
                '### 2. CIS Google Cloud Foundations Benchmark Pillars\n'
                '- **Section 1 (Identity & Access Management):** Enforce MFA on all human accounts; disable service account key creation.\n'
                '- **Section 2 (Logging & Monitoring):** Ensure log sinks capture all administrative and IAM policy modifications.\n'
                '- **Section 3 (Networking):** Eliminate default VPC networks; restrict SSH/RDP ingress to IAP range `35.235.240.0/20`.\n'
                '- **Section 4 (Storage):** Ensure storage buckets enforce uniform bucket-level access and CMEK encryption.'
            ),
            'questions': [
                'What is the operational difference between a SOC 2 Type I report and a SOC 2 Type II report?',
                'How does implementing the CIS Google Cloud Foundations Benchmark assist in achieving compliance across ISO 27001 and PCI-DSS?',
                'What legal instrument must be executed with Google Cloud before any Protected Health Information (PHI) can be ingested under HIPAA?'
            ],
            'reference': 'https://cloud.google.com/security/compliance/compliance-reports-manager',
            'reference_label': 'Google Cloud Compliance: Framework mappings and certified offerings catalog',
            'scenario': {
                'symptom': 'Healthcare application onboarding is halted by chief legal counsel: database contains patient medical records without executed BAA.',
                'constraints': 'Workload must comply with HIPAA Privacy and Security Rules; civil monetary penalties apply for uncertified PHI ingestion.',
                'evidence': (
                    'Internal compliance officer audit memorandum:\n\n'
                    '```text\n'
                    'HIPAA Compliance Defect Report - Project: patient-telemetry-prod\n'
                    'Status: NON-COMPLIANT (CRITICAL RISK)\n'
                    'Finding: Project is processing electronic Protected Health Information (ePHI) across Cloud SQL and Cloud Storage.\n'
                    'Defect 1: Google Cloud Business Associate Agreement (BAA) has not been digitally executed in the Cloud Console.\n'
                    'Defect 2: Cloud Audit Data Access logs for BigQuery and Cloud Storage are disabled, violating 45 CFR § 164.312(b).\n'
                    '```\n\n'
                    'Analysis: Developers deployed clinical workloads into a standard GCP project without executing the mandatory BAA '
                    'or enabling required Data Access audit log categories.'
                ),
                'diagnostic_steps': [
                    'Check Google Cloud Console compliance settings to verify BAA execution state.',
                    'Inspect project-level audit logging configuration for `DATA_READ` and `DATA_WRITE` enablement.',
                    'Verify that all services storing ePHI are listed on Google Cloud\'s HIPAA-included services list.',
                    'Check encryption at rest configurations on target Cloud SQL and Cloud Storage resources.'
                ],
                'root': 'The organization ingested ePHI prior to executing the Google Cloud BAA and failed to enable mandatory HIPAA Data Access audit logs.',
                'fix': 'Execute Google Cloud BAA via the Google Workspace/Cloud Console, enable Data Access audit logging for all HIPAA-included services, and lock log sinks.',
                'verify': 'Confirm BAA execution status is Active; verify Cloud Logging captures all patient record queries in tamper-proof sinks.',
                'residual': 'Non-included Google Cloud services must never be used to process or store ePHI.',
                'diagram': (
                    'Developers ingest patient medical records into unconfigured GCP project',
                    'No Google BAA executed; Data Access audit logging disabled',
                    'Legal counsel flags HIPAA violation and suspends platform launch',
                    'Execute Google Cloud BAA; enable Data Access audit logging',
                    'Workload validated; HIPAA technical safeguards fully operational'
                )
            },
            'lab': {
                'name': 'CIS Benchmark Compliance Scanner & Governance Register',
                'goal': 'Author a comprehensive regulatory control-and-evidence register and implement a Python CIS Benchmark posture scanner validating IAM and logging controls.',
                'expected': 'Markdown compliance matrix and functional Python CIS scanner auditing project security configurations.',
                'mode': 'Python CLI audit implementation',
                'prereq': 'Python 3.9+ installed.',
                'preflight': 'Establish working directory `~/cis-scanner-lab`.',
                'steps': [
                    (
                        '#### CIS Google Cloud Benchmark Posture Scanner\n'
                        'Author and run a Python script auditing essential CIS Benchmark controls:\n\n'
                        '```sh\n'
                        'mkdir -p ~/cis-scanner-lab && cd ~/cis-scanner-lab\n'
                        'cat <<\'EOF\' > cis_posture_scanner.py\n'
                        'class CISBenchmarkAuditor:\n'
                        '    def __init__(self, project_config: dict):\n'
                        '        self.cfg = project_config\n'
                        '\n'
                        '    def audit_section_1_iam(self) -> list[dict]:\n'
                        '        findings = []\n'
                        '        # 1.1 Service account keys\n'
                        '        if self.cfg.get("sa_keys_count", 0) > 0:\n'
                        '            findings.append({"id": "CIS-1.1", "status": "FAIL", "msg": "Service accounts have downloadable private keys."})\n'
                        '        else:\n'
                        '            findings.append({"id": "CIS-1.1", "status": "PASS", "msg": "Zero downloadable service account keys present."})\n'
                        '        # 1.2 Separation of duties\n'
                        '        if "roles/owner" in self.cfg.get("service_account_roles", []):\n'
                        '            findings.append({"id": "CIS-1.2", "status": "FAIL", "msg": "Service account possesses project Owner role."})\n'
                        '        else:\n'
                        '            findings.append({"id": "CIS-1.2", "status": "PASS", "msg": "Least-privilege service account roles enforced."})\n'
                        '        return findings\n'
                        '\n'
                        '    def audit_section_2_logging(self) -> list[dict]:\n'
                        '        findings = []\n'
                        '        if not self.cfg.get("audit_sink_configured", False):\n'
                        '            findings.append({"id": "CIS-2.1", "status": "FAIL", "msg": "No centralized log sink exported to secure storage."})\n'
                        '        else:\n'
                        '            findings.append({"id": "CIS-2.1", "status": "PASS", "msg": "Centralized audit log export sink active."})\n'
                        '        return findings\n'
                        '\n'
                        'mock_gcp_project = {\n'
                        '    "project_id": "brightloaf-enterprise-core",\n'
                        '    "sa_keys_count": 0,\n'
                        '    "service_account_roles": ["roles/storage.objectViewer", "roles/logging.logWriter"],\n'
                        '    "audit_sink_configured": True\n'
                        '}\n'
                        '\n'
                        'auditor = CISBenchmarkAuditor(mock_gcp_project)\n'
                        'print("================================================================")\n'
                        'print(f"CIS BENCHMARK SECURITY SCAN: {mock_gcp_project[\'project_id\']}")\n'
                        'print("================================================================")\n'
                        'all_findings = auditor.audit_section_1_iam() + auditor.audit_section_2_logging()\n'
                        'for f in all_findings:\n'
                        '    print(f"[{f[\'status\']:4s}] {f[\'id\']:8s}: {f[\'msg\']}")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 cis_posture_scanner.py\n'
                        '```'
                    )
                ],
                'accept': 'Functional Python CIS benchmark scanner confirming successful passing evaluations across IAM and logging standards.',
                'verification': 'Review terminal output of <kbd>python3 cis_posture_scanner.py</kbd> confirming 100% PASS on hardened configuration.',
                'trouble': 'If findings fail, inspect project configuration dictionary values.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/cis-scanner-lab</kbd>.',
                'file': 'day-109-compliance-standards.md'
            }
        },
        {
            'key': 'topic-03',
            'title': 'Compliance resource centre and compliance reports manager',
            'overview': (
                'Demonstrating compliance to enterprise customers and independent auditors requires authoritative, verified '
                'attestation documentation. Google Cloud provides the Compliance Reports Manager, a centralized, self-service '
                'portal where enterprise security teams and auditors under NDA can access Google\'s latest third-party audit reports, '
                'SOC 1/2/3 reports, ISO certificates, PCI Attestations of Compliance (AoC), FedRAMP security packages, and '
                'detailed penetration test executive summaries.'
            ),
            'preview': (
                'An enterprise client demands proof of physical data center access controls before signing a contract; the compliance '
                'team downloads Google\'s latest SOC 2 Type II report via Compliance Reports Manager within minutes.'
            ),
            'technical': (
                '### 1. Compliance Reports Manager Architecture\n'
                '- **Self-Service Access:** Accessible directly from Google Cloud Console or the public Compliance Resource Center.\n'
                '- **Non-Disclosure Agreement (NDA) Gating:** Public reports (SOC 3, ISO certificates) are downloadable instantly; '
                'confidential reports (SOC 1/2 Type II, FedRAMP packages) require electronic agreement to an NDA.\n'
                '- **Report Types Available:**\n'
                '  - **SOC 1 Type II (SSAE 18 / ISAE 3402):** Focuses on controls relevant to user organizations\' financial reporting.\n'
                '  - **SOC 2 Type II:** Comprehensive assessment of Security, Availability, and Confidentiality.\n'
                '  - **PCI-DSS AoC:** Formal sign-off by a Qualified Security Assessor for Level 1 Service Provider compliance.\n'
                '  - **ISO Certificates:** ISO 27001, ISO 27017 (Cloud Security), ISO 27018 (Cloud Privacy), ISO 27701 (Privacy Info).\n'
                '\n'
                '### 2. Operational Evidence Harvesting & Audit Package Preparation\n'
                '- Architects combine Google Cloud\'s external audit reports with the organization\'s internal Cloud Audit logs '
                'and Terraform IaC manifests to produce a complete, unified audit evidence package for regulatory examiners.'
            ),
            'questions': [
                'What is the operational difference between public compliance reports (e.g. SOC 3) and confidential reports (e.g. SOC 2 Type II) in Compliance Reports Manager?',
                'How does an enterprise architect utilize the Google Cloud PCI Attestation of Compliance (AoC) in their own PCI QSA audit?',
                'Why should compliance teams establish an automated annual schedule for harvesting newly published SOC and ISO reports?'
            ],
            'reference': 'https://cloud.google.com/security/compliance/compliance-reports-manager',
            'reference_label': 'Google Cloud Compliance Reports Manager: Access to SOC reports, ISO certificates, and attestations',
            'scenario': {
                'symptom': 'Enterprise SaaS procurement deal stalls because the prospect\'s security team requires an independent third-party audit report verifying data center physical controls.',
                'constraints': 'The prospect will not accept vendor self-attestations; requires an accredited CPA firm\'s SOC 2 Type II examination report.',
                'evidence': (
                    'Enterprise procurement security questionnaire item 4.12:\n\n'
                    '```text\n'
                    'Questionnaire Item 4.12: Physical & Environmental Security Controls\n'
                    'Requirement: Provide independent third-party auditor report verifying physical access restrictions, biometric controls, and environmental safeguards for all cloud hosting facilities.\n'
                    'SaaS Vendor Initial Response: "We host on GCP and Google is secure." (REJECTED by customer risk committee).\n'
                    '```\n\n'
                    'Analysis: Vendor sales engineers failed to utilize the Compliance Reports Manager to deliver the authoritative '
                    'Google Cloud SOC 2 Type II report and Customer Responsibility Matrix.'
                ),
                'diagnostic_steps': [
                    'Access Google Cloud Compliance Reports Manager via Cloud Console.',
                    'Search for the latest SOC 2 Type II Google Cloud Services examination report.',
                    'Accept the electronic NDA terms and download the verified PDF report package.',
                    'Cross-reference Customer Responsibility Matrix sections addressing customer physical custody boundaries.'
                ],
                'root': 'The team provided informal vendor assurances rather than downloading authoritative independent auditor attestations from Compliance Reports Manager.',
                'fix': 'Retrieve the formal Google Cloud SOC 2 Type II and SOC 3 reports from Compliance Reports Manager and provide them alongside internal security policies.',
                'verify': 'Customer risk committee approves vendor security review based on accredited CPA SOC 2 Type II attestation.',
                'residual': 'Auditors require updated SOC 2 reports annually upon expiration of the current evaluation period.',
                'diagram': (
                    'Enterprise customer demands independent proof of physical controls',
                    'Vendor provides informal self-attestation; customer procurement rejects',
                    'Deal blocked; security committee requests formal CPA audit opinion',
                    'Download authoritative SOC 2 Type II via Compliance Reports Manager',
                    'Customer accepts accredited CPA report; procurement security approved'
                )
            },
            'lab': {
                'name': 'Compliance Evidence Harvesting & Audit Package Assembler',
                'goal': 'Implement a Python automation script that catalogs regulatory audit artifacts, maps inherited controls, and builds an audit readiness evidence manifest.',
                'expected': 'Functional Python script assembling a comprehensive audit artifact register with verification status and expiration tracking.',
                'mode': 'Python CLI audit automation',
                'prereq': 'Python 3.9+ installed.',
                'preflight': 'Establish working directory `~/evidence-vault-lab`.',
                'steps': [
                    (
                        '#### Compliance Evidence Manifest Assembler\n'
                        'Author and run a Python script aggregating compliance reports and customer evidence into an audit package:\n\n'
                        '```sh\n'
                        'mkdir -p ~/evidence-vault-lab && cd ~/evidence-vault-lab\n'
                        'cat <<\'EOF\' > build_audit_package.py\n'
                        'import datetime\n'
                        'import json\n'
                        '\n'
                        'audit_evidence_registry = [\n'
                        '    {\n'
                        '        "control_domain": "Physical Data Center Security",\n'
                        '        "inherited_from": "Google Cloud",\n'
                        '        "artifact_type": "SOC 2 Type II Report",\n'
                        '        "source": "Compliance Reports Manager",\n'
                        '        "report_period": "2025-11-01 to 2026-04-30",\n'
                        '        "status": "CURRENT"\n'
                        '    },\n'
                        '    {\n'
                        '        "control_domain": "Cardholder Data Physical Boundary",\n'
                        '        "inherited_from": "Google Cloud",\n'
                        '        "artifact_type": "PCI-DSS v4.0 AoC",\n'
                        '        "source": "Compliance Reports Manager",\n'
                        '        "report_period": "Annual 2026",\n'
                        '        "status": "CURRENT"\n'
                        '    },\n'
                        '    {\n'
                        '        "control_domain": "Customer IAM Least Privilege",\n'
                        '        "inherited_from": "Customer Responsibility",\n'
                        '        "artifact_type": "Terraform IAM Policy As Code",\n'
                        '        "source": "Git Repository / GitOps Release 4.12",\n'
                        '        "report_period": "Continuous Enforcement",\n'
                        '        "status": "VERIFIED"\n'
                        '    },\n'
                        '    {\n'
                        '        "control_domain": "Audit Log Immutability & Retention",\n'
                        '        "inherited_from": "Customer Responsibility",\n'
                        '        "artifact_type": "GCS Bucket Lock Configuration",\n'
                        '        "source": "Cloud Storage Retention Policy API",\n'
                        '        "report_period": "365-Day Retention Active",\n'
                        '        "status": "VERIFIED"\n'
                        '    }\n'
                        ']\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("ENTERPRISE AUDIT READINESS EVIDENCE PACKAGE")\n'
                        'print("================================================================")\n'
                        'for item in audit_evidence_registry:\n'
                        '    print(f"Domain:    {item[\'control_domain\']}")\n'
                        '    print(f"Ownership: {item[\'inherited_from\']:25s} | Status: {item[\'status\']}")\n'
                        '    print(f"Evidence:  {item[\'artifact_type\']:25s} | Source: {item[\'source\']}")\n'
                        '    print("----------------------------------------------------------------")\n'
                        '\n'
                        'with open("audit_package_manifest.json", "w") as f:\n'
                        '    json.dump(audit_evidence_registry, f, indent=2)\n'
                        'print("[SUCCESS] Exported audit_package_manifest.json for external examiners.")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 build_audit_package.py\n'
                        '```'
                    )
                ],
                'accept': 'Functional Python audit packaging tool that assembles compliance evidence and exports a structured JSON audit package manifest.',
                'verification': 'Review terminal output of <kbd>python3 build_audit_package.py</kbd> and inspect generated `audit_package_manifest.json`.',
                'trouble': 'If JSON export fails, verify directory write permissions.',
                'cleanup': 'Remove test directory: <kbd>rm -rf ~/evidence-vault-lab</kbd>.',
                'file': 'day-109-compliance-reports.md'
            }
        }
    ]
}
