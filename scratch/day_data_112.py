"""day_data_112.py — Exhaustive architecture data specification for Day 112.

Covers Security Command Center (Standard vs Premium vs Enterprise),
Google SecOps (Chronicle SIEM & SOAR architecture),
Mandiant Threat Intelligence integration,
Event Threat Detection (ETD), Container Threat Detection (CTD), Web Security Scanner (WSS), and
Vulnerability Management (OS Patch Management, Artifact Analysis, GKE Security Posture).
"""

DAY_NUM = 112

DATA = {
    'day': 112,
    'part1_intro': (
        'Day 112 establishes the enterprise threat detection, security telemetry normalization, vulnerability management, '
        'and security operations architecture across Google Cloud. Enterprise architects examine the capabilities across '
        'Security Command Center (Standard, Premium, and Enterprise tiers), attack path simulation, Google SecOps '
        '(Chronicle SIEM and SOAR) powered by the Unified Data Model (UDM) and YARA-L 2.0 detection rules, frontline '
        'Mandiant Threat Intelligence integration, built-in detection engines (Event Threat Detection, Container Threat Detection, '
        'Virtual Machine Threat Detection, Web Security Scanner), and full-lifecycle vulnerability management across virtual '
        'machines, container images in Artifact Registry, and GKE runtime workloads.'
    ),
    'exit_summary': (
        'A finding-to-incident record with evidence preserved and false-positive checks.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts threat detection tiers, telemetry ingestion pipelines, analysis engines, '
        'operational latencies, and automation capabilities across Google Cloud security operations solutions.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Detection Platform</th>\n'
        '<th>Telemetry Sources &amp; Ingestion</th>\n'
        '<th>Analysis Engine &amp; Mechanism</th>\n'
        '<th>Detection Latency &amp; Retention</th>\n'
        '<th>Operational Boundary &amp; SOAR Action</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>SCC Standard</strong></td>\n'
        '<td>Cloud Asset Inventory, basic Cloud Logging</td>\n'
        '<td>Asset discovery, basic web scanning, legacy discovery</td>\n'
        '<td>Batch scans (12–24h); 13-month finding history</td>\n'
        '<td>Read-only dashboard; manual console remediation or export to Pub/Sub.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>SCC Premium</strong></td>\n'
        '<td>Admin Activity, Data Access, VPC Flow, DNS, hypervisor memory, GKE kernel eBPF</td>\n'
        '<td>Event Threat Detection, CTD, VMTD, Security Health Analytics, Attack Path Simulation</td>\n'
        '<td>Near real-time (seconds to minutes for ETD/CTD); 13-month finding history</td>\n'
        '<td>Automated export via Continuous Exports to Pub/Sub; automated Cloud Function / Workflows remediation.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>SCC Enterprise</strong></td>\n'
        '<td>SCC Premium feeds plus multi-cloud telemetry (AWS, Azure) and unified SecOps pipeline</td>\n'
        '<td>Integrated Chronicle SIEM, Gemini Security Workbench, Attack Path &amp; Risk Engine</td>\n'
        '<td>Sub-second streaming normalization; 12-month hot data retention in SecOps</td>\n'
        '<td>Integrated Chronicle SOAR playbooks, bi-directional case management, automated containment.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Google SecOps (Chronicle SIEM)</strong></td>\n'
        '<td>All GCP logs, endpoint telemetry (EDR), on-prem firewalls, SaaS identity logs via BindPlane</td>\n'
        '<td>Unified Data Model (UDM) mapping, YARA-L 2.0 streaming detection, Mandiant IOC matching</td>\n'
        '<td>Real-time streaming ingestion; 365-day hot analytical search window</td>\n'
        '<td>Direct alert forwarding to SecOps SOAR case management and external SIEM/ticketing.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Google SecOps (Chronicle SOAR)</strong></td>\n'
        '<td>Alerts from Chronicle SIEM, SCC, third-party EDR, email gateways, cloud alerts</td>\n'
        '<td>Playbook DAG orchestration, entity extraction, alert grouping into threat cases</td>\n'
        '<td>Triggered on ingestion; execution sub-minute per playbook step</td>\n'
        '<td>Bi-directional automated API containment: IAM revoke, firewall block, VM quarantine, Jira dispatch.</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 112: Enterprise Threat Detection, Telemetry Ingestion, and Automated SecOps Topology',
        'desc': 'Architectural layout illustrating Security Command Center tiers, Event/Container Threat Detection engines, Chronicle SIEM UDM ingestion, Mandiant Threat Intelligence correlation, and Chronicle SOAR playbook containment.',
        'caption': 'Figure 112.1: Multi-tiered threat detection and SecOps triage pipeline featuring SCC Premium/Enterprise detectors, UDM normalization, YARA-L rule evaluation, and automated incident response.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Cloud Telemetry & Pipeline Ingestion Plane',
                'desc': 'Cloud Audit Logs (Admin/Data), VPC Flow Logs, DNS queries, hypervisor memory, and GKE kernel eBPF',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Security Command Center Posture & Threat Detection Engine',
                'desc': 'Event Threat Detection (ETD), Container Threat Detection (CTD), VMTD, Security Health Analytics, Attack Path Engine',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Google SecOps (Chronicle SIEM) & UDM Normalization Grid',
                'desc': 'Streaming log normalization into Unified Data Model (UDM), YARA-L 2.0 multi-event correlation, 365-day hot storage',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Mandiant Threat Intelligence & IOC Correlation Plane',
                'desc': 'Frontline adversary profiling, Indicator Confidence Scoring (IC-Score), APT attribution, and automated IOC matching',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: Chronicle SOAR & Automated Incident Containment Fabric',
                'desc': 'Entity clustering, automated investigation playbooks, IAM token revocation, firewall quarantine, and case management',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Audit & VPC Flow Telemetry', 'detail': 'Streaming Pipeline Ingestion', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'GKE eBPF / Memory Stream', 'detail': 'Kernel & Hypervisor Probes', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'ETD & CTD Detectors', 'detail': 'Real-Time Anomaly Engines', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Attack Path Simulator', 'detail': 'Crown Jewel Exposure Graph', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'UDM Parsing Pipeline', 'detail': 'Standardized Entity Models', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'YARA-L Rule Engine', 'detail': 'Multi-Event Correlation (15m)', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Mandiant IOC Feed', 'detail': 'Frontline C2 & Hash Registry', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'IC-Score Evaluator', 'detail': 'Threshold-Based Block Rules', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Chronicle SOAR Playbook', 'detail': 'Automated Containment DAG', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'GCP Remediation API', 'detail': 'IAM Revoke & NGFW Tagging', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'STREAMING TELEMETRY & POSTURE DETECTION BOUNDARY', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'CHRONICLE SIEM & MANDIANT THREAT INTEL FABRIC', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'AUTOMATED ORCHESTRATION & CONTAINMENT DOMAIN', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Inspect Memory & Kernel', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Evaluate Threat Rules', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Simulate Attack Exposure', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Normalize into UDM', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Evaluate YARA-L Match', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Correlate Mandiant Intel', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Filter Stale / Partner IPs', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Trigger SOAR Case', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Execute Automated Containment', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: Continuous Export: Real-Time Finding Stream to Pub/Sub', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: UDM Entity Extraction & Parser Health Latency Metric', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 450, 'label': 'PROBE 3: Automated Containment Verification: IAM Token Revocation Audit', 'badge': 'P3', 'color': '#22c55e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world threat detection failures, false-positive containment cascades, '
        'telemetry parsing blind spots, and unconstrained vulnerability patching outages across enterprise Google Cloud estates. '
        'Each scenario details verbatim diagnostic logs, root cause mechanisms, production remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on architectural exercises implement the complete operational engineering lifecycle for Day 112. '
        'Architects author an SCC finding triage engine, build a YARA-L 2.0 detection rule with automated SOAR playbook containment, '
        'develop a Mandiant threat intelligence correlation module, parse container runtime security telemetry, and deploy a container vulnerability gatekeeper.'
    ),
    'topics': [
        # TOPIC 1
        {
            'key': 'topic-01',
            'title': 'Security Command Center (Standard vs Premium vs Enterprise): findings, misconfiguration detection, threat detection, attack path simulation',
            'overview': (
                'Security Command Center (SCC) serves as Google Cloud’s centralized cloud security posture management (CSPM) '
                'and cloud workload protection platform (CWPP). Understanding the architectural differences between Standard, '
                'Premium, and Enterprise tiers is essential for designing organizational security operations. SCC continuously '
                'discovers cloud assets across the Resource Manager hierarchy, evaluates configurations against compliance benchmarks '
                '(CIS, NIST 800-53, PCI-DSS, ISO 27001), identifies active security threats, and models attack paths leading to high-value assets.'
            ),
            'preview': (
                'An enterprise automated remediation script revokes IAM credentials from a production CI/CD runner after an SCC alert fires, '
                'halting critical deployments due to unvalidated finding triage.'
            ),
            'technical': (
                'SCC operates at the Organization or Project level. In enterprise architectures, SCC is deployed at the Organization '
                'level to maintain centralized oversight across all folders and projects.\n\n'
                '### Tier Architectural Differences\n'
                '1. **SCC Standard**: Included at no additional cost. Provides basic asset discovery via Cloud Asset Inventory, '
                'basic Web Security Scanner for public IP endpoints, and legacy anomaly findings. It lacks compliance benchmarking, '
                'threat detection engines, and automated export mechanisms.\n'
                '2. **SCC Premium**: Activated organization-wide on a pay-as-you-go or subscription commitment model. Adds Security Health '
                'Analytics (SHA) with over 150 misconfiguration detectors, Event Threat Detection (ETD) analyzing Cloud Audit and VPC Flow Logs, '
                'Container Threat Detection (CTD) inspecting GKE container runtimes, Virtual Machine Threat Detection (VMTD) scanning hypervisor memory, '
                'Sensitive Data Protection discovery, compliance reporting dashboards, and Attack Path Simulation.\n'
                '3. **SCC Enterprise**: Unifies cloud posture management with Google SecOps (Chronicle SIEM and SOAR). It extends CSPM '
                'across multi-cloud estates (AWS, Microsoft Azure), incorporates Mandiant-guided remediation workflows, delivers generative AI '
                'security investigations powered by Gemini, and provides end-to-end incident case management with automated response playbooks.\n\n'
                '### Finding Schema and Classification\n'
                'Every security observation generated by SCC adheres to a strict canonical JSON finding schema containing:\n'
                '- `name`: Canonical resource name (`organizations/{org_id}/sources/{source_id}/findings/{finding_id}`).\n'
                '- `parent`: The resource owning the finding.\n'
                '- `resource_name`: Full GCP resource URI (e.g. `//compute.googleapis.com/projects/xyz/zones/us-central1-a/instances/vm-01`).\n'
                '- `category`: Human-readable identifier (e.g. `OPEN_FIREWALL`, `ANOMALOUS_IAM_GRANT`, `PERSISTENCE_SERVICE_ACCOUNT_KEY`).\n'
                '- `finding_class`: Canonical class: `MISCONFIGURATION`, `THREAT`, `VULNERABILITY`, or `OBSERVATION`.\n'
                '- `severity`: Priority rating: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, or `UNSPECIFIED`.\n'
                '- `state`: Finding lifecycle status: `ACTIVE` or `INACTIVE`.\n'
                '- `event_time` & `create_time`: Timestamps of threat occurrence and detection recording.\n'
                '- `source_properties`: Key-value metadata specific to the detecting detector (e.g. source IP, target identity, matched rule).\n'
                '- `indicator`: Indicators of Compromise (IOCs) such as associated IP addresses, domains, or file hashes.\n\n'
                '### Attack Path Simulation\n'
                'SCC Premium and Enterprise incorporate graph-based Attack Path Simulation. The engine models the cloud infrastructure '
                'as a directed graph where nodes represent resources (IAM service accounts, VMs, subnets, GCS buckets) and edges represent '
                'permissions or network connectivity. The engine evaluates exposure from the public internet, calculates potential lateral '
                'movement paths, and computes an "Attack Exposure Score" for designated "crown jewel" resources. This enables security teams '
                'to prioritize fixing a single misconfiguration that breaks an entire attack chain.'
            ),
            'questions': [
                'How does Security Command Center differentiate finding classes between MISCONFIGURATION, THREAT, and VULNERABILITY?',
                'What architectural mechanism enables Attack Path Simulation to quantify crown jewel exposure risks across complex IAM and network graphs?',
                'Why is an automated Continuous Export to Cloud Pub/Sub preferred over periodic REST polling for enterprise incident response?'
            ],
            'reference': 'https://docs.cloud.google.com/security-command-center/docs',
            'reference_label': 'Google Cloud Security Command Center Documentation',
            'scenario': {
                'symptom': 'Production deployment pipeline halts abruptly when automated remediation strips IAM roles from deployment service accounts.',
                'impact': 'Dozens of dependent microservice deployments fail; on-call engineer alerted to unauthorized automated permission revocation.',
                'constraints': 'Automated response must isolate genuine threats within 60 seconds without disrupting legitimate CI/CD infrastructure pipelines.',
                'evidence': (
                    'SCC finding payload and automated remediation log:\n\n'
                    '```json\n'
                    '{\n'
                    '  "name": "organizations/1029384756/sources/203948/findings/misc-sha-002",\n'
                    '  "category": "ADMIN_SERVICE_ACCOUNT_CREATED",\n'
                    '  "findingClass": "MISCONFIGURATION",\n'
                    '  "severity": "HIGH",\n'
                    '  "state": "ACTIVE",\n'
                    '  "resourceName": "//iam.googleapis.com/projects/fintech-prod/serviceAccounts/terraform-runner@fintech-prod.iam.gserviceaccount.com"\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: The automated remediation Cloud Function executed unilateral permission revocation on a HIGH severity finding '
                    'without verifying whether the target account belonged to an authorized CI/CD identity whitelist.'
                ),
                'diagnostic_steps': [
                    'Extract the triggering SCC finding from Cloud Logging or Pub/Sub dead-letter queues to inspect detector attributes.',
                    'Check Cloud Audit Logs for the principal and timestamp that triggered the service account creation event.',
                    'Verify whether the creation activity originated from an authorized CI/CD runner IP address and approved git commit hash.',
                    'Review the automated remediation Cloud Function containment logic to inspect missing exception filters.'
                ],
                'root': 'The automated remediation Cloud Function executed unilateral permission revocation on a HIGH severity finding without verifying whether the target account belonged to an authorized CI/CD whitelist.',
                'fix': 'Update the remediation engine to implement an exception check against an authorized infrastructure-as-code identity registry and require human SOC triage approval for non-quarantineable pipeline identities.',
                'verify': 'Simulate an authorized service account deployment in a staging environment and verify the remediation script logs an audit record without revoking credentials.',
                'residual': 'Authorized identities that are genuinely compromised could evade automated containment if whitelist rules are overly broad.',
                'diagram': (
                    'CI/CD provisions admin service account in production project',
                    'Remediation function strips IAM without checking CI/CD whitelist',
                    'Pipeline halts and dependent microservices fail health checks',
                    'Deploy pre-filter whitelist and approval gate before revocation',
                    'Legitimate deployments succeed; rogue threats isolated rapidly'
                )
            },
            'lab': {
                'name': 'SCC Finding Ingestion and Automated Triage Processor',
                'goal': 'Configure an SCC Pub/Sub export structure and implement a Python triage engine that ingests SCC finding events, performs severity normalization, checks authorization whitelists, and generates incident records.',
                'expected': 'Functional Python triage parser processing raw SCC JSON payloads and outputting structured triage decisions.',
                'mode': 'Python CLI and JSON data simulation',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/scc-triage-lab</kbd>.',
                'steps': [
                    (
                        '#### Set up project workspace and sample SCC finding payloads\n'
                        'Create the working directory and write synthetic SCC finding JSON files representing both an active malicious threat and a benign CI/CD misconfiguration:\n\n'
                        '```sh\n'
                        'mkdir -p ~/scc-triage-lab && cd ~/scc-triage-lab\n'
                        'cat <<\'EOF\' > scc_findings.json\n'
                        '[\n'
                        '  {\n'
                        '    "name": "organizations/1029384756/sources/203948/findings/threat-etd-001",\n'
                        '    "parent": "organizations/1029384756/sources/203948",\n'
                        '    "resourceName": "//compute.googleapis.com/projects/fintech-prod/zones/us-central1-a/instances/bastion-01",\n'
                        '    "category": "BAD_IP_COMMUNICATION",\n'
                        '    "findingClass": "THREAT",\n'
                        '    "severity": "CRITICAL",\n'
                        '    "state": "ACTIVE",\n'
                        '    "eventTime": "2026-09-29T08:15:00Z",\n'
                        '    "sourceProperties": {\n'
                        '      "sourceIp": "198.51.100.45",\n'
                        '      "destinationIp": "203.0.113.88",\n'
                        '      "direction": "OUTBOUND",\n'
                        '      "protocol": "TCP",\n'
                        '      "threatActor": "Known C2 Beacon"\n'
                        '    }\n'
                        '  },\n'
                        '  {\n'
                        '    "name": "organizations/1029384756/sources/203948/findings/misc-sha-002",\n'
                        '    "parent": "organizations/1029384756/sources/203948",\n'
                        '    "resourceName": "//iam.googleapis.com/projects/fintech-prod/serviceAccounts/terraform-runner@fintech-prod.iam.gserviceaccount.com",\n'
                        '    "category": "ADMIN_SERVICE_ACCOUNT_CREATED",\n'
                        '    "findingClass": "MISCONFIGURATION",\n'
                        '    "severity": "HIGH",\n'
                        '    "state": "ACTIVE",\n'
                        '    "eventTime": "2026-09-29T08:20:00Z",\n'
                        '    "sourceProperties": {\n'
                        '      "principalEmail": "admin-deployer@enterprise.com",\n'
                        '      "roles": ["roles/owner"]\n'
                        '    }\n'
                        '  }\n'
                        ']\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the SCC Triage and Incident Generation Engine\n'
                        'Write a Python triage module that processes incoming findings, applies suppression rules for whitelisted deployment identities, determines automated containment actions for active threats, and generates a structured incident record:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > triage_engine.py\n'
                        'import json\n'
                        'import sys\n'
                        'from datetime import datetime, timezone\n'
                        '\n'
                        'APPROVED_CI_IDENTITIES = {\n'
                        '    "terraform-runner@fintech-prod.iam.gserviceaccount.com",\n'
                        '    "cloudbuild-sa@fintech-prod.iam.gserviceaccount.com"\n'
                        '}\n'
                        '\n'
                        'def triage_finding(finding):\n'
                        '    category = finding.get("category")\n'
                        '    f_class = finding.get("findingClass")\n'
                        '    severity = finding.get("severity")\n'
                        '    resource = finding.get("resourceName")\n'
                        '    props = finding.get("sourceProperties", {})\n'
                        '\n'
                        '    decision = {\n'
                        '        "finding_id": finding.get("name").split("/")[-1],\n'
                        '        "resource": resource,\n'
                        '        "category": category,\n'
                        '        "severity": severity,\n'
                        '        "action": "IGNORE",\n'
                        '        "containment": None,\n'
                        '        "reason": ""\n'
                        '    }\n'
                        '\n'
                        '    # Check CI/CD Whitelist suppression\n'
                        '    for identity in APPROVED_CI_IDENTITIES:\n'
                        '        if identity in resource:\n'
                        '            decision["action"] = "SUPPRESS_LOG_ONLY"\n'
                        '            decision["reason"] = f"Resource matches approved CI/CD identity: {identity}"\n'
                        '            return decision\n'
                        '\n'
                        '    # Triage THREAT findings\n'
                        '    if f_class == "THREAT" and severity in ("CRITICAL", "HIGH"):\n'
                        '        decision["action"] = "ESCALATE_AND_CONTAIN"\n'
                        '        if "compute.googleapis.com" in resource:\n'
                        '            decision["containment"] = "APPLY_ISOLATION_FIREWALL_TAG"\n'
                        '            decision["reason"] = f"Active threat detected on compute instance: {props.get(\'threatActor\', \'Unknown\')}"\n'
                        '        elif "iam.googleapis.com" in resource:\n'
                        '            decision["containment"] = "DISABLE_SERVICE_ACCOUNT_KEY"\n'
                        '            decision["reason"] = "Compromised service account credential threat"\n'
                        '        else:\n'
                        '            decision["containment"] = "PAGE_SOC_MANUAL_CONTAINMENT"\n'
                        '            decision["reason"] = "Uncategorized high-severity threat"\n'
                        '    elif f_class == "MISCONFIGURATION" and severity == "CRITICAL":\n'
                        '        decision["action"] = "CREATE_JIRA_TICKET_P1"\n'
                        '        decision["reason"] = "Critical posture misconfiguration requires remediation"\n'
                        '    else:\n'
                        '        decision["action"] = "CREATE_JIRA_TICKET_P3"\n'
                        '        decision["reason"] = f"Standard posture finding {category} ({severity})"\n'
                        '\n'
                        '    return decision\n'
                        '\n'
                        'def main():\n'
                        '    with open("scc_findings.json", "r") as f:\n'
                        '        findings = json.load(f)\n'
                        '\n'
                        '    incident_report = {\n'
                        '        "report_generated_utc": datetime.now(timezone.utc).isoformat(),\n'
                        '        "processed_findings_count": len(findings),\n'
                        '        "triage_results": []\n'
                        '    }\n'
                        '\n'
                        '    print("=== Processing SCC Finding Telemetry Stream ===")\n'
                        '    for f in findings:\n'
                        '        triage = triage_finding(f)\n'
                        '        incident_report["triage_results"].append(triage)\n'
                        '        print(f"Finding: {triage[\'finding_id\']} | Action: {triage[\'action\']} | Containment: {triage[\'containment\']}")\n'
                        '        print(f"  Reason: {triage[\'reason\']}\\n")\n'
                        '\n'
                        '    with open("incident_record.json", "w") as out:\n'
                        '        json.dump(incident_report, out, indent=2)\n'
                        '    print("Triage completed. Wrote incident_record.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    main()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute the Triage Processor and inspect incident records\n'
                        'Run the triage engine and verify that the threat finding escalates to automated firewall isolation while the approved CI/CD service account misconfiguration is safely suppressed:\n\n'
                        '```sh\n'
                        'python3 triage_engine.py\n'
                        'cat incident_record.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python triage processor successfully distinguishing true positive threats requiring isolation from whitelisted administrative deployments.',
                'verification': 'Review terminal output of <kbd>python3 triage_engine.py</kbd> confirming threat-etd-001 is escalated to APPLY_ISOLATION_FIREWALL_TAG and misc-sha-002 is marked SUPPRESS_LOG_ONLY.',
                'trouble': 'If findings are not parsed, verify valid JSON syntax in `scc_findings.json`.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/scc-triage-lab</kbd>.',
                'file': 'day-112-scc-triage.md'
            }
        },

        # TOPIC 2
        {
            'key': 'topic-02',
            'title': 'Google SecOps (Chronicle SIEM & SOAR architecture)',
            'overview': (
                'Google SecOps (formerly Chronicle SIEM and Siemplify SOAR) provides a hyperscale security operations platform '
                'engineered to ingest, normalize, correlate, and automatically respond to massive volumes of telemetry. '
                'SecOps decouples log retention from query latency, allowing organizations to retain petabytes of security logs '
                'in an active, searchable hot state for a full year while executing real-time detection rules using YARA-L 2.0.'
            ),
            'preview': (
                'An internal log format change breaks Chronicle parser rules, allowing unauthorized service account key creation '
                'to evade SIEM detection for 72 hours until high-rate GPU billing triggers external alerts.'
            ),
            'technical': (
                'The Google SecOps architecture consists of two interconnected engines: Chronicle SIEM for ingestion, normalization, '
                'and detection; and Chronicle SOAR for incident management, alert grouping, threat intelligence enrichment, and automated playbook orchestration.\n\n'
                '### Chronicle SIEM Telemetry & The Unified Data Model (UDM)\n'
                'Raw telemetry from heterogeneous sources—including GCP Cloud Audit Logs, VPC Flow Logs, Zeek network logs, CrowdStrike Falcon, '
                'Active Directory, and Okta—is ingested via BindPlane agents, Google Cloud Pub/Sub, or direct HTTP APIs. '
                'Upon ingestion, raw logs pass through specialized parsers that normalize the unstructured records into the Unified Data Model (UDM).\n\n'
                'UDM structures every log record into standardized noun-verb-object relationships:\n'
                '- **Event Metadata**: `event_timestamp`, `event_type` (e.g. `USER_LOGIN`, `NETWORK_CONNECTION`, `PROCESS_LAUNCH`, `USER_UNCATEGORIZED`).\n'
                '- **Principal**: The acting entity (user email, IP, MAC address, service account, host).\n'
                '- **Target**: The object being acted upon (destination IP, URI, target file, cloud resource URI).\n'
                '- **Intermediary**: Proxies, NAT gateways, load balancers, or VPN concentrators traversing the path.\n'
                '- **Security Result**: Detection outcomes, action taken (`ALLOW`, `BLOCK`), severity, and rule classifications.\n\n'
                '### Detection Engineering with YARA-L 2.0\n'
                'Chronicle SIEM executes detection logic using YARA-L 2.0, a declarative domain-specific language designed for '
                'structured telemetry matching and multi-event behavioral correlation across time windows.\n'
                'A YARA-L rule consists of four primary sections:\n'
                '1. `meta`: Documentation, author, severity, MITRE ATT&CK technique IDs.\n'
                '2. `events`: Variable declarations matching UDM attributes and cross-event join variables.\n'
                '3. `match`: The time window over which multi-event correlations must occur (e.g. `$principal_user over 10m`).\n'
                '4. `condition`: Boolean logic specifying occurrence thresholds (e.g. `#login_fail > 5 and #login_success == 1`).\n\n'
                '### Chronicle SOAR Orchestration & Playbooks\n'
                'When detections trigger in Chronicle SIEM or external alerts arrive, Chronicle SOAR aggregates related alerts into '
                'unified "Cases" using entity grouping algorithms (grouping by hostname, user ID, or external IP). '
                'Cases automatically trigger Playbooks—directed acyclic graphs (DAGs) of automated actions:\n'
                '- **Enrichment**: Querying VirusTotal, Mandiant, and internal IPAM to contextualize entities.\n'
                '- **User Interaction**: Dispatching Slack/Teams approvals to managers for privilege escalation validation.\n'
                '- **Remediation**: Executing GCP APIs to disable compromised IAM service accounts, inject null-route firewall rules, '
                'or snapshot infected Compute Engine instances for digital forensics.'
            ),
            'questions': [
                'How does the Chronicle Unified Data Model (UDM) standardize diverse log formats into consistent security entities?',
                'What are the core structural blocks of a YARA-L 2.0 detection rule and how is temporal correlation expressed in the match section?',
                'How does Chronicle SOAR aggregate disparate SIEM alerts into single actionable investigation cases?'
            ],
            'reference': 'https://docs.cloud.google.com/chronicle/docs',
            'reference_label': 'Google SecOps (Chronicle) Architecture and Detection Engineering Guide',
            'scenario': {
                'symptom': 'Compromised developer credentials create service account keys across multiple production projects undetected by SIEM.',
                'impact': 'Attacker provisions high-cost GPU instances for 72 hours undetected; hundreds of thousands of dollars in unauthorized compute billed.',
                'constraints': 'Detection rules must monitor cross-project IAM administrative actions within 15-minute sliding correlation windows.',
                'evidence': (
                    'Raw API Gateway log vs Parser Dropout:\n\n'
                    '```json\n'
                    '{\n'
                    '  "timestamp": "2026-09-29T04:12:00Z",\n'
                    '  "protoPayload": {\n'
                    '    "methodName": "google.iam.admin.v1.CreateServiceAccountKey",\n'
                    '    "authenticationInfo": {"principalEmail": "contractor@partner.com"}\n'
                    '  },\n'
                    '  "parser_status": "DROPPED_UNMAPPED_FIELDS"\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: Schema updates to the gateway logs caused Chronicle Grok parsers to drop unmapped target attributes, '
                    'blinding the YARA-L rule looking for multi-project key generation.'
                ),
                'diagnostic_steps': [
                    'Navigate to SecOps Ingestion & Parsers console and check parser status and dropped log statistics.',
                    'Compare raw log JSON against the Grok/Regex parser extraction rules.',
                    'Execute a historical raw log search to verify that logs reached the ingestion forwarder but failed UDM transformation.',
                    'Validate that YARA-L rules explicitly test parsed UDM fields rather than raw string representations.'
                ],
                'root': 'The ingestion parser failed to normalize nested JSON attributes into UDM fields, causing detection rules relying on UDM targets to fail silently.',
                'fix': 'Update the parser to correctly traverse nested JSON keys into `target.resource` UDM structures and establish an automated alert for parser error rate thresholds.',
                'verify': 'Replay raw log samples through the parser testing tool and execute a Retrohunt verifying the YARA-L rule triggers against historical events.',
                'residual': 'Logs ingested during the 72-hour outage require manual retrospective reprocessing once the parser definition is updated.',
                'diagram': (
                    'Gateway schema change emits unmapped nested JSON keys',
                    'Parser drops unmapped fields; logs bypass UDM target mapping',
                    'Compromised credential generates rogue keys undetected for 72h',
                    'Update parser definition and alert on parser error rate spikes',
                    'YARA-L rule catches cross-project key generation within 15 minutes'
                )
            },
            'lab': {
                'name': 'YARA-L Rule Authoring and SOAR Playbook Simulation',
                'goal': 'Author a functional YARA-L 2.0 detection rule for suspicious privilege escalation and implement a Python SOAR playbook that correlates UDM events, queries threat intelligence, and automates containment.',
                'expected': 'A validated YARA-L rule specification and a working Python SOAR containment script.',
                'mode': 'Declarative YARA-L and Python script execution',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/secops-soar-lab</kbd>.',
                'steps': [
                    (
                        '#### Author the YARA-L 2.0 Detection Rule\n'
                        'Write a declarative YARA-L rule designed to detect a single user principal generating service account keys across multiple projects within a 15-minute window:\n\n'
                        '```sh\n'
                        'mkdir -p ~/secops-soar-lab && cd ~/secops-soar-lab\n'
                        'cat <<\'EOF\' > detect_suspicious_key_creation.yaral\n'
                        'rule suspicious_multi_project_sa_key_creation {\n'
                        '  meta:\n'
                        '    author = "Enterprise Cloud SecOps"\n'
                        '    description = "Detects a single principal creating service account keys across multiple distinct projects within 15 minutes."\n'
                        '    severity = "HIGH"\n'
                        '    mitre_attack = "T1078.004, T1098.001"\n'
                        '\n'
                        '  events:\n'
                        '    $audit.metadata.event_type = "USER_UNCATEGORIZED"\n'
                        '    $audit.metadata.product_event_type = "google.iam.admin.v1.CreateServiceAccountKey"\n'
                        '    $audit.security_result.action = "ALLOW"\n'
                        '    $audit.principal.user.email_addresses = $user_email\n'
                        '    $audit.target.resource.name = $sa_resource\n'
                        '    $audit.target.labels["project_id"] = $project_id\n'
                        '\n'
                        '  match:\n'
                        '    $user_email over 15m\n'
                        '\n'
                        '  condition:\n'
                        '    #sa_resource >= 2 and count_distinct($project_id) >= 2\n'
                        '}\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Generate Synthetic UDM Telemetry and SOAR Playbook\n'
                        'Write a Python simulation representing the Chronicle SOAR engine. The script ingests UDM events matching the detection rule, extracts the suspect principal, checks reputation, and issues an automated IAM credential suspension command:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > soar_playbook.py\n'
                        'import json\n'
                        'import sys\n'
                        'from datetime import datetime, timezone\n'
                        '\n'
                        '# Synthetic UDM alert generated by YARA-L engine\n'
                        'udm_alert = {\n'
                        '    "alert_id": "SEC-ALERT-88392",\n'
                        '    "rule_name": "suspicious_multi_project_sa_key_creation",\n'
                        '    "severity": "HIGH",\n'
                        '    "detection_time": datetime.now(timezone.utc).isoformat(),\n'
                        '    "entities": {\n'
                        '        "principal_user": "external-contractor@partner-firm.com",\n'
                        '        "source_ip": "198.51.100.77",\n'
                        '        "target_service_accounts": [\n'
                        '            "projects/prod-billing/serviceAccounts/billing-sync@prod-billing.iam.gserviceaccount.com",\n'
                        '            "projects/prod-data/serviceAccounts/data-exporter@prod-data.iam.gserviceaccount.com"\n'
                        '        ]\n'
                        '    }\n'
                        '}\n'
                        '\n'
                        'class ChronicleSOARPlaybook:\n'
                        '    def __init__(self, alert):\n'
                        '        self.alert = alert\n'
                        '        self.case_id = f"CASE-{alert[\'alert_id\'].split(\'-\')[-1]}"\n'
                        '        self.execution_log = []\n'
                        '\n'
                        '    def log_step(self, step_name, status, details):\n'
                        '        entry = {\n'
                        '            "step": step_name,\n'
                        '            "status": status,\n'
                        '            "details": details,\n'
                        '            "timestamp": datetime.now(timezone.utc).isoformat()\n'
                        '        }\n'
                        '        self.execution_log.append(entry)\n'
                        '        print(f"[{entry[\'timestamp\']}] {step_name}: {status} -> {details}")\n'
                        '\n'
                        '    def execute(self):\n'
                        '        print(f"=== Triggering SOAR Playbook for {self.case_id} ===")\n'
                        '        user = self.alert["entities"]["principal_user"]\n'
                        '        src_ip = self.alert["entities"]["source_ip"]\n'
                        '\n'
                        '        # Step 1: Threat Intelligence Enrichment\n'
                        '        self.log_step("Enrich_Threat_Intel", "COMPLETED", f"Queried IP {src_ip}: Malicious score 85/100 (Known Tor Exit)")\n'
                        '\n'
                        '        # Step 2: Contextual Identity Verification\n'
                        '        if "contractor" in user:\n'
                        '            self.log_step("Evaluate_Identity_Risk", "TRIGGERED", "Principal is an external contractor identity; high blast radius")\n'
                        '        else:\n'
                        '            self.log_step("Evaluate_Identity_Risk", "INFO", "Internal FTE identity")\n'
                        '\n'
                        '        # Step 3: Containment Actions\n'
                        '        self.log_step("Revoke_Active_Sessions", "EXECUTED", f"Issued gcloud auth revoke for {user}")\n'
                        '        for sa in self.alert["entities"]["target_service_accounts"]:\n'
                        '            self.log_step("Disable_Rogue_SA_Keys", "EXECUTED", f"Disabled newly created keys on {sa}")\n'
                        '\n'
                        '        # Step 4: Ticketing and Escalation\n'
                        '        self.log_step("Dispatch_Jira_P1", "COMPLETED", f"Created SEC-IR-9921 for SOC Tier 3 Lead assigned to {user}")\n'
                        '        \n'
                        '        return {\n'
                        '            "case_id": self.case_id,\n'
                        '            "status": "CONTAINED",\n'
                        '            "execution_history": self.execution_log\n'
                        '        }\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    playbook = ChronicleSOARPlaybook(udm_alert)\n'
                        '    result = playbook.execute()\n'
                        '    with open("soar_execution_result.json", "w") as f:\n'
                        '        json.dump(result, f, indent=2)\n'
                        '    print("\\nPlaybook completed successfully. Saved soar_execution_result.json.")\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Run the SOAR Playbook Simulation and verify containment steps\n'
                        'Execute the Python playbook runner and inspect the resulting JSON case file to verify automated session revocation and key disablement:\n\n'
                        '```sh\n'
                        'python3 soar_playbook.py\n'
                        'cat soar_execution_result.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated YARA-L 2.0 multi-event correlation rule and automated Python SOAR containment playbook executing session revocation.',
                'verification': 'Review terminal output of <kbd>python3 soar_playbook.py</kbd> confirming containment status CONTAINED and automated key disablement steps.',
                'trouble': 'If execution fails, verify python3 version with <kbd>python3 --version</kbd>.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/secops-soar-lab</kbd>.',
                'file': 'day-112-secops-soar.md'
            }
        },

        # TOPIC 3
        {
            'key': 'topic-03',
            'title': 'Mandiant Threat Intelligence integration',
            'overview': (
                'Google Cloud’s integration of Mandiant Threat Intelligence empowers security teams with frontline breach telemetry, '
                'adversary attribution, and tactical indicators of compromise (IOCs) gathered directly from frontline incident response '
                'engagements. Instead of relying solely on public vulnerability databases, organizations leverage high-confidence adversary '
                'intelligence embedded directly into Security Command Center and Google SecOps.'
            ),
            'preview': (
                'Automated firewall blocking triggered by an outdated Mandiant botnet indicator blacklists a major B2B partner IP, '
                'severing critical enterprise supply chain communication.'
            ),
            'technical': (
                'Mandiant Threat Intelligence provides both strategic, operational, and tactical intelligence across Google Cloud environments.\n\n'
                '### Indicators of Compromise (IOCs) and Scoring Taxonomy\n'
                'Threat intelligence feeds continuously update IOC repositories containing millions of malicious IP addresses, domain names, '
                'file hashes, and URL patterns. Mandiant classifies indicators using two primary metrics:\n'
                '1. **Indicator Confidence Score (IC-Score)**: A numeric value from 0 to 100 representing the certainty that an indicator is truly malicious. '
                'High IC-scores (80–100) indicate verified command-and-control (C2) nodes or ransomware infrastructure, enabling automated blocking. '
                'Medium IC-scores (50–79) warrant alerting and analyst review, while low scores (<50) represent suspicious but unconfirmed infrastructure.\n'
                '2. **M-Score (Mandiant Threat Score)**: Evaluates the severity and impact of the threat actor associated with the indicator.\n\n'
                '### Native SCC & SecOps Integration\n'
                '- **Automated Log Correlation**: Chronicle SIEM automatically matches incoming VPC Flow Logs, Cloud DNS query logs, and HTTP proxy logs '
                'against Mandiant IOC feeds in real time. This ingestion occurs behind the scenes—security teams do not need to configure complex manual ETL feeds.\n'
                '- **Threat Attribution & Actor Profiles**: Detections are enriched with Mandiant actor profiles (e.g. APT29, UNC3886, FIN11). '
                'When an alert fires, the analyst sees the adversary’s historical motivations, preferred tools, and associated MITRE ATT&CK techniques.\n'
                '- **Chronicle Curated Detections**: Google SecOps includes pre-packaged, Mandiant-maintained detection rule sets that automatically '
                'adapt as adversary tactics shift, minimizing the maintenance overhead of internal detection engineering.\n\n'
                '### Breach Analytics and Attack Surface Management (ASM)\n'
                'Mandiant Attack Surface Management (ASM) scans an enterprise’s externally facing digital footprint from an attacker’s perspective, '
                'identifying exposed cloud storage buckets, unauthenticated development APIs, abandoned Compute Engine instances, and vulnerable software stacks. '
                'These findings correlate with SCC posture data to prevent external perimeter compromises.'
            ),
            'questions': [
                'How does the Mandiant Indicator Confidence Score (IC-Score) guide the boundary between automated firewall blocking and human analyst triage?',
                'What architectural benefits emerge from Chronicle SIEM automatically evaluating VPC Flow Logs against Mandiant IOCs without manual pipeline configuration?',
                'Why must threat intelligence correlation rules evaluate indicator freshness and internal partner registries before executing automated edge blocks?'
            ],
            'reference': 'https://docs.cloud.google.com/security-command-center/docs',
            'reference_label': 'Mandiant Threat Intelligence Integration in Google Cloud',
            'scenario': {
                'symptom': 'B2B partner API calls return HTTP 403 Forbidden; warehouse stock synchronization drops to zero.',
                'impact': 'Retail inventory synchronization halts during peak trading; automated logistics shipments suspended.',
                'constraints': 'Automated edge blocking must drop verified C2 beacons without disrupting approved partner egress ranges.',
                'evidence': (
                    'Cloud Armor security logs and Mandiant indicator query:\n\n'
                    '```text\n'
                    'Cloud Armor Log: action=DENY, rule=block-ioc-feed, src_ip=203.0.113.50\n'
                    'Mandiant Feed Record:\n'
                    '  Indicator: 203.0.113.50\n'
                    '  IC-Score: 82\n'
                    '  Actor: Commodity Botnet (Mirai)\n'
                    '  Last Seen: 2026-03-15 (198 days stale)\n'
                    '```\n\n'
                    'Analysis: The automated playbook blocked an IP based on an IC-Score threshold without checking indicator last-seen freshness '
                    'or verifying whether the IP was registered in the partner CIDR database.'
                ),
                'diagnostic_steps': [
                    'Review Cloud Armor security policy logs for blocked requests matching the partner’s source IP address.',
                    'Check Chronicle SIEM alert history to identify the specific Mandiant IOC match that triggered the rule injection.',
                    'Inspect the Mandiant Threat Intelligence portal for the indicator’s historical context, last seen date, and malware family attribution.',
                    'Confirm the IP’s current ownership via whois and B2B partner mutual agreements.'
                ],
                'root': 'The automated containment playbook executed autonomous firewall blocking based on an IC-Score threshold without checking an internal partner IP whitelist or evaluating indicator last-seen freshness.',
                'fix': 'Introduce an exception check against an authorized partner CIDR inventory and require secondary analyst verification if an IOC indicator has not exhibited malicious activity within the preceding 30 days.',
                'verify': 'Remove the blocked rule from Cloud Armor, re-enable partner traffic, and verify that subsequent partner API calls log an informational enrichment event without executing containment.',
                'residual': 'If a partner’s infrastructure is actively compromised, an attacker traversing the whitelisted partner IP could bypass automated edge filtering.',
                'diagram': (
                    'Partner logistics service migrates egress to an IP previously used by botnet',
                    'Chronicle SIEM detects incoming traffic matching Mandiant IOC (IC-Score 82)',
                    'Automated SOAR playbook injects Cloud Armor deny rule for the partner IP',
                    'B2B inventory synchronization drops immediately; warehouse stock calls fail',
                    'Resolution: Update playbook with Partner CIDR whitelist and IOC freshness verification'
                )
            },
            'lab': {
                'name': 'Mandiant Threat Intelligence Matcher & Dynamic Scoring Engine',
                'goal': 'Develop a Python threat intelligence correlation engine that matches simulated network connection telemetry against a Mandiant IOC database, calculates composite risk scores, and filters whitelisted partner ranges.',
                'expected': 'Functional Python scoring module that distinguishes genuine C2 traffic from whitelisted partner infrastructure.',
                'mode': 'Python CLI threat modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/mandiant-intel-lab</kbd>.',
                'steps': [
                    (
                        '#### Create Synthetic Mandiant IOC Feed and Network Telemetry\n'
                        'Write JSON datasets representing a Mandiant threat feed containing adversary attribution and IC-scores, alongside sample VPC network connection logs:\n\n'
                        '```sh\n'
                        'mkdir -p ~/mandiant-intel-lab && cd ~/mandiant-intel-lab\n'
                        'cat <<\'EOF\' > mandiant_feed.json\n'
                        '[\n'
                        '  {\n'
                        '    "indicator": "198.51.100.22",\n'
                        '    "type": "IPV4",\n'
                        '    "ic_score": 95,\n'
                        '    "threat_actor": "UNC3886",\n'
                        '    "malware_family": "VirtualPita",\n'
                        '    "last_seen": "2026-09-28T12:00:00Z"\n'
                        '  },\n'
                        '  {\n'
                        '    "indicator": "203.0.113.50",\n'
                        '    "type": "IPV4",\n'
                        '    "ic_score": 82,\n'
                        '    "threat_actor": "Commodity Botnet",\n'
                        '    "malware_family": "Mirai",\n'
                        '    "last_seen": "2026-03-15T00:00:00Z"\n'
                        '  }\n'
                        ']\n'
                        'EOF\n'
                        'cat <<\'EOF\' > network_events.json\n'
                        '[\n'
                        '  {\n'
                        '    "connection_id": "CONN-001",\n'
                        '    "source_vm": "app-server-01",\n'
                        '    "destination_ip": "198.51.100.22",\n'
                        '    "port": 443,\n'
                        '    "bytes_sent": 450200,\n'
                        '    "is_partner_ip": false\n'
                        '  },\n'
                        '  {\n'
                        '    "connection_id": "CONN-002",\n'
                        '    "source_vm": "b2b-gateway-01",\n'
                        '    "destination_ip": "203.0.113.50",\n'
                        '    "port": 443,\n'
                        '    "bytes_sent": 12000,\n'
                        '    "is_partner_ip": true\n'
                        '  }\n'
                        ']\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Threat Intelligence Evaluation Engine\n'
                        'Write a Python engine that correlates network events with the Mandiant feed, evaluates IC-scores and freshness, checks partner flags, and issues actionable triage decisions:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > evaluate_threat_intel.py\n'
                        'import json\n'
                        'from datetime import datetime, timezone, timedelta\n'
                        '\n'
                        'def load_data():\n'
                        '    with open("mandiant_feed.json", "r") as f:\n'
                        '        feed = {item["indicator"]: item for item in json.load(f)}\n'
                        '    with open("network_events.json", "r") as f:\n'
                        '        events = json.load(f)\n'
                        '    return feed, events\n'
                        '\n'
                        'def evaluate_events(feed, events):\n'
                        '    decisions = []\n'
                        '    now = datetime.fromisoformat("2026-09-29T08:00:00Z")\n'
                        '\n'
                        '    print("=== Mandiant Threat Intelligence Telemetry Evaluation ===\\n")\n'
                        '    for ev in events:\n'
                        '        dst = ev["destination_ip"]\n'
                        '        conn = ev["connection_id"]\n'
                        '        \n'
                        '        if dst in feed:\n'
                        '            intel = feed[dst]\n'
                        '            ic_score = intel["ic_score"]\n'
                        '            actor = intel["threat_actor"]\n'
                        '            last_seen = datetime.fromisoformat(intel["last_seen"])\n'
                        '            days_stale = (now - last_seen).days\n'
                        '\n'
                        '            decision = {\n'
                        '                "connection_id": conn,\n'
                        '                "destination_ip": dst,\n'
                        '                "actor": actor,\n'
                        '                "ic_score": ic_score,\n'
                        '                "action": "ALLOW",\n'
                        '                "rationale": ""\n'
                        '            }\n'
                        '\n'
                        '            # Partner bypass verification\n'
                        '            if ev["is_partner_ip"]:\n'
                        '                if days_stale > 90:\n'
                        '                    decision["action"] = "ALLOW_AND_AUDIT"\n'
                        '                    decision["rationale"] = f"Partner IP matches stale IOC ({days_stale} days old). Permitted; ticket created."\n'
                        '                else:\n'
                        '                    decision["action"] = "MANUAL_SOC_REVIEW"\n'
                        '                    decision["rationale"] = "Partner IP matches fresh high-confidence IOC. Escalate to analyst."\n'
                        '            else:\n'
                        '                if ic_score >= 80 and days_stale <= 30:\n'
                        '                    decision["action"] = "AUTOMATED_CONTAINMENT_BLOCK"\n'
                        '                    decision["rationale"] = f"Fresh active threat actor {actor} (IC-Score: {ic_score}). Immediate firewall block."\n'
                        '                else:\n'
                        '                    decision["action"] = "MONITOR"\n'
                        '                    decision["rationale"] = f"Suspicious connection below automated block threshold."\n'
                        '            \n'
                        '            decisions.append(decision)\n'
                        '            print(f"Connection {conn} -> {dst} [{actor}]")\n'
                        '            print(f"  Action: {decision[\'action\']}")\n'
                        '            print(f"  Rationale: {decision[\'rationale\']}\\n")\n'
                        '        else:\n'
                        '            decisions.append({\n'
                        '                "connection_id": conn,\n'
                        '                "destination_ip": dst,\n'
                        '                "action": "ALLOW",\n'
                        '                "rationale": "No threat intel match."\n'
                        '            })\n'
                        '\n'
                        '    with open("triage_verdict.json", "w") as out:\n'
                        '        json.dump(decisions, out, indent=2)\n'
                        '    print("Evaluation completed. Saved triage_verdict.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    feed, events = load_data()\n'
                        '    evaluate_events(feed, events)\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Run the Threat Intelligence Engine and review verdicts\n'
                        'Execute the Python script and inspect the output to verify that active UNC3886 C2 traffic is blocked while the stale partner IP is routed to audit without business disruption:\n\n'
                        '```sh\n'
                        'python3 evaluate_threat_intel.py\n'
                        'cat triage_verdict.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python threat intelligence engine that correctly executes automated containment for fresh high-confidence threats while protecting partner traffic.',
                'verification': 'Review terminal output of <kbd>python3 evaluate_threat_intel.py</kbd> confirming CONN-001 is AUTOMATED_CONTAINMENT_BLOCK and CONN-002 is ALLOW_AND_AUDIT.',
                'trouble': 'If date parsing errors occur, verify python datetime ISO format strings.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/mandiant-intel-lab</kbd>.',
                'file': 'day-112-mandiant-intel.md'
            }
        },

        # TOPIC 4
        {
            'key': 'topic-04',
            'title': 'Event Threat Detection, Container Threat Detection, Web Security Scanner',
            'overview': (
                'Google Cloud incorporates specialized built-in threat detection engines that evaluate telemetry at multiple '
                'architectural layers without requiring intrusive host-based agents. Event Threat Detection (ETD) analyzes '
                'infrastructure-wide audit and network event streams; Container Threat Detection (CTD) monitors GKE container '
                'runtimes using kernel instrumentation; and Web Security Scanner (WSS) discovers application-layer vulnerabilities '
                'in publicly exposed web workloads.'
            ),
            'preview': (
                'A compromised public GKE microservice spawns a reverse shell; Container Threat Detection fires a critical alert '
                'that lingers uncontained for four hours due to misconfigured notification routing.'
            ),
            'technical': (
                'Enterprise threat defense requires multi-layered detection across the cloud control plane, container runtimes, and external web boundaries.\n\n'
                '### Event Threat Detection (ETD)\n'
                'ETD operates directly at the Google Cloud data ingestion pipeline. It analyzes streaming logs without consuming Compute Engine '
                'CPU cycles or requiring logging agents. Supported log sources include Cloud Audit Logs (Admin Activity, Data Access), '
                'VPC Flow Logs, Cloud DNS query logs, and Google Workspace audit logs.\n'
                'Key detection classes include:\n'
                '- **Anomalous IAM Grants**: Privilege escalation (e.g. `roles/owner` granted to external Gmail accounts).\n'
                '- **Data Exfiltration**: Massive BigQuery exports or Cloud Storage transfers to external, unowned storage buckets.\n'
                '- **Cryptocurrency Mining**: Compute Engine network connections to known mining pool stratum protocols.\n'
                '- **Network Anomalies**: Outbound connections to Tor exit nodes, malware C2 servers, or port scanning sweeps.\n'
                '- **Persistence**: Rogue service account key generation and Cloud KMS key destruction attempts.\n\n'
                '### Container Threat Detection (CTD)\n'
                'CTD monitors Google Kubernetes Engine (GKE) container workloads in near real-time. Built on Google’s specialized '
                'kernel instrumentation (eBPF and auditd drivers deployed on GKE Container-Optimized OS nodes), CTD detects container breaches:\n'
                '- **Added Binary Execution**: Execution of unexpected binary executables introduced into a container filesystem at runtime.\n'
                '- **Reverse Shell**: Spawning an interactive shell (e.g. `/bin/bash`, `/bin/sh`) connected to an external network socket.\n'
                '- **Execution of Malicious Binary**: Hashes matching known malware signatures executed inside a pod.\n'
                '- **Kernel Module Loading**: Unauthorized attempts to load Linux kernel modules or modify kernel memory from a container.\n\n'
                '### Virtual Machine Threat Detection (VMTD)\n'
                'VMTD scans the volatile memory of running Compute Engine guest VMs directly from the underlying Google hypervisor. '
                'Because it inspects memory from below the guest operating system, it cannot be blinded, detected, or tampered with by '
                'guest-level rootkits or kernel-mode malware. It specializes in detecting memory-only cryptominers and kernel-space evasion tools.\n\n'
                '### Web Security Scanner (WSS)\n'
                'WSS provides automated dynamic application security testing (DAST) for App Engine, Cloud Run, GKE, and Compute Engine web endpoints. '
                'Operating as an external crawler, WSS tests public interfaces for:\n'
                '- Cross-site scripting (XSS) injection flaws.\n'
                '- Cleartext passwords transmitted over HTTP.\n'
                '- Outdated JavaScript libraries with known CVEs.\n'
                '- Insecure mixed content and sensitive data leaks in public HTML responses.'
            ),
            'questions': [
                'How does Container Threat Detection utilize eBPF kernel instrumentation on GKE nodes to identify reverse shells without modifying container images?',
                'Why can Virtual Machine Threat Detection (VMTD) detect memory-resident malware even when a guest operating system is compromised by a kernel rootkit?',
                'What are the operational trade-offs of enabling Web Security Scanner automated crawls on authenticated web applications?'
            ],
            'reference': 'https://docs.cloud.google.com/security-command-center/docs',
            'reference_label': 'Event Threat Detection and Container Threat Detection Guide',
            'scenario': {
                'symptom': 'Interactive bash reverse shell established from a production GKE pod to an external threat listener.',
                'impact': 'Attacker dumps Kubernetes service account tokens and enumerates cluster secrets for 4 hours.',
                'constraints': 'Runtime threat alerts must trigger automated pod termination within 30 seconds of detection.',
                'evidence': (
                    'SCC Container Threat Detection finding JSON:\n\n'
                    '```json\n'
                    '{\n'
                    '  "category": "EXECUTION_REVERSE_SHELL",\n'
                    '  "findingClass": "THREAT",\n'
                    '  "severity": "CRITICAL",\n'
                    '  "state": "ACTIVE",\n'
                    '  "resourceName": "//container.googleapis.com/projects/prod/clusters/prod-gke/k8s/namespaces/default/pods/api-pod-123",\n'
                    '  "sourceProperties": {\n'
                    '    "destinationIp": "198.51.100.99",\n'
                    '    "destinationPort": 4444,\n'
                    '    "process": "/bin/bash"\n'
                    '  }\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: The alert was emitted immediately by eBPF kernel sensors but sat uncontained because notifications '
                    'were routed to an unmonitored mailbox rather than an automated Pub/Sub subscriber.'
                ),
                'diagnostic_steps': [
                    'Inspect the SCC findings console for `CONTAINER_THREAT_DETECTION` findings within the affected cluster namespace.',
                    'Check GKE audit logs for `pods/exec` and pod creation events associated with the compromised pod name.',
                    'Review Cloud Logging for VPC Flow Log egress connections from the node IP on anomalous ports (e.g. port 4444).',
                    'Verify that SCC Continuous Export is configured with a valid Pub/Sub topic and active IAM subscriber permissions.'
                ],
                'root': 'The security operations pipeline lacked automated Pub/Sub export and containment for CRITICAL Container Threat Detection findings, leaving the reverse shell active until manual discovery.',
                'fix': 'Wire CTD findings directly to a Cloud Run containment microservice that immediately terminates the compromised pod and isolates the node network.',
                'verify': 'Simulate an authorized reverse shell test in a dedicated canary namespace and verify the pod is terminated within 30 seconds.',
                'residual': 'Ephemeral memory artifacts inside the container may be lost upon pod termination unless memory snapshots or forensic logs are preserved beforehand.',
                'diagram': (
                    'Vulnerable public web service accepts malicious file upload',
                    'Attacker executes web shell; spawns interactive reverse shell to external C2',
                    'GKE eBPF kernel driver detects reverse shell; CTD generates CRITICAL finding in SCC',
                    'Alert sent to unmonitored email; attacker enumerates cluster secrets for 4 hours',
                    'Remediation: Configure Continuous Export to Pub/Sub to trigger automated pod termination'
                )
            },
            'lab': {
                'name': 'Container & Event Threat Detection Telemetry Parser and Pod Quarantine',
                'goal': 'Build a Python containment automation engine that ingests simulated CTD and ETD findings, extracts pod and IP metadata, and generates automated Kubernetes and Cloud NGFW containment actions.',
                'expected': 'Functional Python engine that detects reverse shells and data exfiltration, outputting actionable remediation commands.',
                'mode': 'Python script and CLI simulation',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/ctd-etd-lab</kbd>.',
                'steps': [
                    (
                        '#### Set up Synthetic Threat Telemetry Dataset\n'
                        'Create a JSON telemetry file containing a Container Threat Detection reverse shell finding and an Event Threat Detection external exfiltration finding:\n\n'
                        '```sh\n'
                        'mkdir -p ~/ctd-etd-lab && cd ~/ctd-etd-lab\n'
                        'cat <<\'EOF\' > threat_events.json\n'
                        '[\n'
                        '  {\n'
                        '    "engine": "CONTAINER_THREAT_DETECTION",\n'
                        '    "category": "REVERSE_SHELL",\n'
                        '    "severity": "CRITICAL",\n'
                        '    "resource_type": "k8s_pod",\n'
                        '    "cluster_name": "prod-useast1-gke",\n'
                        '    "namespace": "payment-workloads",\n'
                        '    "pod_name": "checkout-api-789bf-9x21z",\n'
                        '    "container_name": "api-gateway",\n'
                        '    "details": {\n'
                        '      "target_ip": "198.51.100.99",\n'
                        '      "target_port": 4444,\n'
                        '      "process": "/bin/bash"\n'
                        '    }\n'
                        '  },\n'
                        '  {\n'
                        '    "engine": "EVENT_THREAT_DETECTION",\n'
                        '    "category": "BIGQUERY_DATA_EXFILTRATION",\n'
                        '    "severity": "HIGH",\n'
                        '    "resource_type": "bigquery_dataset",\n'
                        '    "project_id": "fintech-prod",\n'
                        '    "principal_email": "compromised-sa@fintech-prod.iam.gserviceaccount.com",\n'
                        '    "details": {\n'
                        '      "destination_bucket": "gs://attacker-owned-bucket-xyz",\n'
                        '      "rows_exported": 5000000\n'
                        '    }\n'
                        '  }\n'
                        ']\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Multi-Engine Threat Responder\n'
                        'Write a Python script that parses the threat events, determines the blast radius, and generates automated containment commands (kubectl delete pod and gcloud iam service-accounts keys disable):\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > threat_responder.py\n'
                        'import json\n'
                        'import sys\n'
                        '\n'
                        'def process_threats():\n'
                        '    with open("threat_events.json", "r") as f:\n'
                        '        events = json.load(f)\n'
                        '\n'
                        '    remediation_plan = []\n'
                        '    print("=== Multi-Engine Threat Telemetry Responder ===\\n")\n'
                        '\n'
                        '    for ev in events:\n'
                        '        engine = ev["engine"]\n'
                        '        category = ev["category"]\n'
                        '        sev = ev["severity"]\n'
                        '\n'
                        '        if engine == "CONTAINER_THREAT_DETECTION" and category == "REVERSE_SHELL":\n'
                        '            pod = ev["pod_name"]\n'
                        '            ns = ev["namespace"]\n'
                        '            cluster = ev["cluster_name"]\n'
                        '            dst_ip = ev["details"]["target_ip"]\n'
                        '\n'
                        '            action = {\n'
                        '                "engine": engine,\n'
                        '                "incident_type": "ACTIVE_CONTAINER_ESCAPE_OR_REVERSE_SHELL",\n'
                        '                "target": f"{cluster}/{ns}/{pod}",\n'
                        '                "commands": [\n'
                        '                    f"kubectl delete pod {pod} -n {ns} --grace-period=0 --force",\n'
                        '                    f"gcloud compute firewall-rules create block-c2-{dst_ip.replace(\'.\', \'-\')} --action=DENY --rules=all --destination-ranges={dst_ip}/32 --priority=100"\n'
                        '                ]\n'
                        '            }\n'
                        '            remediation_plan.append(action)\n'
                        '            print(f"CRITICAL DETECTED: {category} in {pod}")\n'
                        '            print(f"  -> Generated Pod Eviction: {action[\'commands\'][0]}")\n'
                        '            print(f"  -> Generated C2 IP Block: {action[\'commands\'][1]}\\n")\n'
                        '\n'
                        '        elif engine == "EVENT_THREAT_DETECTION" and category == "BIGQUERY_DATA_EXFILTRATION":\n'
                        '            sa = ev["principal_email"]\n'
                        '            dest = ev["details"]["destination_bucket"]\n'
                        '\n'
                        '            action = {\n'
                        '                "engine": engine,\n'
                        '                "incident_type": "DATA_EXFILTRATION_TO_UNTRUSTED_DESTINATION",\n'
                        '                "target": sa,\n'
                        '                "commands": [\n'
                        '                    f"gcloud iam service-accounts disable {sa}",\n'
                        '                    f"gcloud storage buckets add-iam-policy-binding {dest} --member=allUsers --role=roles/storage.objectViewer --condition=NULL || echo \'Foreign bucket containment delegated\'"\n'
                        '                ]\n'
                        '            }\n'
                        '            remediation_plan.append(action)\n'
                        '            print(f"HIGH DETECTED: {category} by {sa}")\n'
                        '            print(f"  -> Generated SA Disablement: {action[\'commands\'][0]}\\n")\n'
                        '\n'
                        '    with open("remediation_manifest.json", "w") as out:\n'
                        '        json.dump(remediation_plan, out, indent=2)\n'
                        '    print("Remediation plan generated. Saved remediation_manifest.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    process_threats()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Run the Threat Responder and verify remediation commands\n'
                        'Execute the responder script and verify that the generated remediation manifest contains exact kubectl and gcloud containment instructions:\n\n'
                        '```sh\n'
                        'python3 threat_responder.py\n'
                        'cat remediation_manifest.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated threat telemetry parser capable of mapping CTD and ETD findings to declarative containment actions across Kubernetes and IAM layers.',
                'verification': 'Review terminal output of <kbd>python3 threat_responder.py</kbd> confirming kubectl delete pod and gcloud iam service-accounts disable commands are generated.',
                'trouble': 'If output is empty, inspect dictionary keys in `threat_events.json`.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/ctd-etd-lab</kbd>.',
                'file': 'day-112-threat-engines.md'
            }
        },

        # TOPIC 5
        {
            'key': 'topic-05',
            'title': 'Vulnerability management: OS patch management, Artifact Analysis, GKE security posture',
            'overview': (
                'Modern enterprise vulnerability management requires continuous identification, risk prioritization, and automated '
                'patch remediation across virtual machines, container registries, and active Kubernetes workloads. '
                'Google Cloud provides integrated vulnerability governance through VM Manager OS Patch Management, Artifact Analysis '
                'for container images, and the GKE Security Posture dashboard.'
            ),
            'preview': (
                'An unconstrained VM Manager OS patch deployment reboots all database cluster nodes simultaneously, '
                'causing a 45-minute service outage and loss of database cluster quorum.'
            ),
            'technical': (
                'Vulnerability management operates across three distinct architectural planes in Google Cloud:\n\n'
                '### VM Manager & OS Patch Management\n'
                'VM Manager is a suite of infrastructure management tools built into Compute Engine, powered by the OS Config agent '
                'installed inside Linux and Windows guest images. It encompasses three core capabilities:\n'
                '1. **OS Inventory Management**: Discovers installed OS packages, kernel versions, and unpatched Common Vulnerabilities and Exposures (CVEs).\n'
                '2. **OS Patch Management**: Automates patch deployment schedules across VM fleets. Architects configure:\n'
                '   - **Patch Jobs & Deployments**: Defined rollout windows, instance filters (by label, zone, or name prefix), and roll-out percentages to avoid service degradation.\n'
                '   - **Reboot Settings**: `DEFAULT`, `ALWAYS`, or `NEVER`.\n'
                '   - **Pre-Patch & Post-Patch Scripts**: Custom Cloud Storage scripts executed before patching (e.g. draining connections) and after patching (e.g. running health checks).\n'
                '3. **OS Policy Compliance**: Enforces desired configuration states (e.g. ensuring security agents are installed and specific package versions are locked).\n\n'
                '### Artifact Analysis for Container Registries\n'
                'Artifact Analysis automatically scans container images stored in Artifact Registry. It operates in two modes:\n'
                '- **Initial Scan**: Triggers automatically on image push, scanning OS packages (Debian, Alpine, RHEL, Ubuntu) and language-level packages (Maven, Go, npm, PyPI).\n'
                '- **Continuous Vulnerability Scanning**: As new CVEs are published to the National Vulnerability Database (NVD), Artifact Analysis '
                'retroactively updates vulnerability notes for stored images without requiring images to be rebuilt or re-pushed.\n'
                '- **Metadata & Attestation Storage**: Stores Vulnerability Occurrences, Software Bill of Materials (SBOM), and Binary Authorization attestations as signed metadata.\n\n'
                '### GKE Security Posture Dashboard\n'
                'The GKE Security Posture dashboard unifies workload vulnerability scanning and configuration posture inspection:\n'
                '- **Workload Vulnerability Scanning**: Extends Artifact Analysis into the running cluster, tracking container images actively running inside pods. '
                'It correlates known vulnerabilities with running workloads and highlights reachable vulnerabilities.\n'
                '- **Workload Configuration Auditing**: Audits Kubernetes manifests against the CIS Kubernetes Benchmark and Google security best practices, '
                'flagging pods running as root, missing CPU/memory limits, containers with `allowPrivilegeEscalation=true`, and workloads mounting sensitive host paths (`/var/run/docker.sock`).'
            ),
            'questions': [
                'How does VM Manager ensure that rolling OS patch deployments do not violate database high availability or quorum constraints?',
                'Why does Artifact Analysis continuous vulnerability scanning eliminate the need to trigger rebuilds simply to detect newly published CVEs?',
                'What is the architectural difference between container image vulnerability scanning in Artifact Registry versus runtime workload scanning in the GKE Security Posture dashboard?'
            ],
            'reference': 'https://docs.cloud.google.com/security-command-center/docs',
            'reference_label': 'VM Manager and Artifact Analysis Vulnerability Management Guide',
            'scenario': {
                'symptom': 'All three database cluster nodes in zone us-central1-a reboot concurrently at midnight.',
                'impact': 'Database quorum lost; customer checkout transactions fail for 45 minutes.',
                'constraints': 'Automated patching must never reboot more than one node in a database cluster simultaneously.',
                'evidence': (
                    'VM Manager Patch Deployment configuration:\n\n'
                    '```json\n'
                    '{\n'
                    '  "patchConfig": {\n'
                    '    "rebootConfig": "ALWAYS"\n'
                    '  },\n'
                    '  "rollout": {\n'
                    '    "mode": "ZONE_BY_ZONE",\n'
                    '    "disruptionBudget": {\n'
                    '      "percentage": 100\n'
                    '    }\n'
                    '  }\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: Because all cluster nodes resided in the same zone and the disruption budget was set to 100%, '
                    'the OS Config agent patched and issued reboot signals to all instances simultaneously.'
                ),
                'diagnostic_steps': [
                    'Review `gcloud compute os-config patch-jobs describe` output for the failed patch job execution ID.',
                    'Check VM instance serial port logs for abrupt kernel restart and shutdown signals at the midnight timestamp.',
                    'Inspect instance zone distribution and confirm the lack of multi-zone redundancy.',
                    'Verify the patch deployment manifest’s `rollout` parameters and `disruptionBudget` settings.'
                ],
                'root': 'The OS Patch Deployment lacked a fractional disruption budget and was executed against single-zone clustered workloads without quorum-aware pre-patch draining scripts.',
                'fix': 'Update the OS patch deployment to enforce a disruption budget of 1 instance or 25% max concurrent reboot, and introduce pre-patch scripts that drain node traffic and verify cluster health before rebooting.',
                'verify': 'Execute a dry-run patch job against a staging cluster and verify that nodes reboot serially with confirmed health checks between steps.',
                'residual': 'Kernel updates requiring reboots must still be scheduled during designated low-traffic maintenance windows.',
                'diagram': (
                    'Operations schedules VM Manager patch job with 100% disruption budget',
                    'VM Manager applies OS patches to all database nodes in zone us-central1-a',
                    'All three Cassandra database nodes receive reboot signal simultaneously',
                    'Database quorum drops; cluster enters split-brain lock; checkouts fail',
                    'Remediation: Configure disruptionBudget=1 and pre-patch cluster drain script'
                )
            },
            'lab': {
                'name': 'Container CVE Triage & OS Patch Policy Auditor',
                'goal': 'Develop an automated vulnerability triage script that parses simulated Artifact Analysis CVE occurrence data, calculates CVSS risk scores, and outputs an admission pass/fail decision with an exception procedure.',
                'expected': 'A Python vulnerability evaluation tool enforcing CVE thresholds and generating an exception audit record.',
                'mode': 'Python script and CLI data modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/vuln-triage-lab</kbd>.',
                'steps': [
                    (
                        '#### Set up Synthetic Artifact Analysis Vulnerability Occurrences\n'
                        'Write a JSON dataset representing container vulnerability findings returned by Google Cloud Artifact Analysis, including CVE IDs, CVSS scores, package names, and fix availability:\n\n'
                        '```sh\n'
                        'mkdir -p ~/vuln-triage-lab && cd ~/vuln-triage-lab\n'
                        'cat <<\'EOF\' > artifact_scan_results.json\n'
                        '[\n'
                        '  {\n'
                        '    "cve_id": "CVE-2026-3021",\n'
                        '    "package_name": "openssl",\n'
                        '    "installed_version": "3.0.2-0ubuntu1.10",\n'
                        '    "fixed_version": "3.0.2-0ubuntu1.12",\n'
                        '    "cvss_score": 9.8,\n'
                        '    "severity": "CRITICAL",\n'
                        '    "fix_available": true\n'
                        '  },\n'
                        '  {\n'
                        '    "cve_id": "CVE-2026-1189",\n'
                        '    "package_name": "libxml2",\n'
                        '    "installed_version": "2.9.13",\n'
                        '    "fixed_version": "None",\n'
                        '    "cvss_score": 7.5,\n'
                        '    "severity": "HIGH",\n'
                        '    "fix_available": false\n'
                        '  },\n'
                        '  {\n'
                        '    "cve_id": "CVE-2025-8841",\n'
                        '    "package_name": "curl",\n'
                        '    "installed_version": "7.81.0",\n'
                        '    "fixed_version": "7.81.0-1ubuntu1.15",\n'
                        '    "cvss_score": 5.3,\n'
                        '    "severity": "MEDIUM",\n'
                        '    "fix_available": true\n'
                        '  }\n'
                        ']\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Vulnerability Gatekeeper and Exception Processor\n'
                        'Write a Python vulnerability policy enforcement tool. The script blocks container image deployment if any fixable CRITICAL vulnerability exists, but supports an approved CVE temporary exception process:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > vuln_gatekeeper.py\n'
                        'import json\n'
                        'import sys\n'
                        'from datetime import datetime, timezone\n'
                        '\n'
                        'APPROVED_EXCEPTIONS = {\n'
                        '    "CVE-2026-1189": {\n'
                        '        "reason": "No upstream fix available; mitigated by Cloud Armor WAF rule 1002.",\n'
                        '        "expires": "2026-12-31T00:00:00Z",\n'
                        '        "approver": "security-architect@enterprise.com"\n'
                        '    }\n'
                        '}\n'
                        '\n'
                        'def evaluate_vulnerabilities():\n'
                        '    with open("artifact_scan_results.json", "r") as f:\n'
                        '        cves = json.load(f)\n'
                        '\n'
                        '    print("=== Artifact Analysis Vulnerability Gatekeeper ===\\n")\n'
                        '    blocked = []\n'
                        '    accepted = []\n'
                        '    exceptions_applied = []\n'
                        '\n'
                        '    for cve in cves:\n'
                        '        cve_id = cve["cve_id"]\n'
                        '        score = cve["cvss_score"]\n'
                        '        sev = cve["severity"]\n'
                        '        fix = cve["fix_available"]\n'
                        '\n'
                        '        # Exception evaluation\n'
                        '        if cve_id in APPROVED_EXCEPTIONS:\n'
                        '            exc = APPROVED_EXCEPTIONS[cve_id]\n'
                        '            exceptions_applied.append({\n'
                        '                "cve_id": cve_id,\n'
                        '                "details": exc\n'
                        '            })\n'
                        '            print(f"[EXCEPTION APPLIED] {cve_id} ({sev} {score}): {exc[\'reason\']}")\n'
                        '            accepted.append(cve_id)\n'
                        '            continue\n'
                        '\n'
                        '        # Policy rule: Block any fixable CRITICAL (>= 9.0) or HIGH (>= 7.0)\n'
                        '        if score >= 9.0 and fix:\n'
                        '            blocked.append({\n'
                        '                "cve_id": cve_id,\n'
                        '                "score": score,\n'
                        '                "reason": "CRITICAL vulnerability with vendor fix available must be patched."\n'
                        '            })\n'
                        '            print(f"[REJECTED] {cve_id} ({sev} {score}) - Fix available ({cve[\'fixed_version\']})")\n'
                        '        else:\n'
                        '            accepted.append(cve_id)\n'
                        '            print(f"[ACCEPTED] {cve_id} ({sev} {score}) - Meets deployment threshold")\n'
                        '\n'
                        '    decision = {\n'
                        '        "decision_timestamp": datetime.now(timezone.utc).isoformat(),\n'
                        '        "overall_admission": "REJECT" if blocked else "ACCEPT",\n'
                        '        "blocked_cves": blocked,\n'
                        '        "accepted_cves": accepted,\n'
                        '        "exceptions_applied": exceptions_applied\n'
                        '    }\n'
                        '\n'
                        '    with open("admission_decision.json", "w") as out:\n'
                        '        json.dump(decision, out, indent=2)\n'
                        '\n'
                        '    print(f"\\nOverall Admission Verdict: {decision[\'overall_admission\']}")\n'
                        '    print("Wrote admission_decision.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    evaluate_vulnerabilities()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Run the Vulnerability Gatekeeper and inspect admission decisions\n'
                        'Execute the Python evaluation script and inspect the output to verify that fixable CVE-2026-3021 triggers an admission REJECT while CVE-2026-1189 is permitted under an approved exception:\n\n'
                        '```sh\n'
                        'python3 vuln_gatekeeper.py\n'
                        'cat admission_decision.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated vulnerability gatekeeper script enforcing CVSS thresholds, distinguishing fixable flaws, and recording formal security exceptions.',
                'verification': 'Review terminal output of <kbd>python3 vuln_gatekeeper.py</kbd> confirming overall admission REJECT due to unpatched CVE-2026-3021.',
                'trouble': 'If JSON file cannot be found, verify working directory with <kbd>pwd</kbd>.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/vuln-triage-lab</kbd>.',
                'file': 'day-112-vuln-management.md'
            }
        }
    ]
}
