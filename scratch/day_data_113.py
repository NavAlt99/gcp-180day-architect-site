"""day_data_113.py — Exhaustive architecture data specification for Day 113.

Covers Incident Response Process (Detect, Contain, Eradicate, Recover, Learn),
Forensics Basics (Snapshots, Log Preservation, Evidence Handling, Chain of Custody),
Threat Modelling (STRIDE on Cloud-Native GCP Architectures), and
Penetration Testing Rules and Guidelines on Google Cloud.
"""

DAY_NUM = 113

DATA = {
    'day': 113,
    'part1_intro': (
        'Day 113 establishes the enterprise incident response lifecycle, digital forensics preservation protocols, '
        'systematic threat modeling methodologies, and penetration testing governance across Google Cloud. '
        'Architects examine the end-to-end incident handling process (Detect, Contain, Eradicate, Recover, Learn), '
        'forensic evidence acquisition procedures across persistent disks and volatile memory without compromising integrity, '
        'STRIDE threat modeling adapted to cloud trust boundaries and IAM impersonation vectors, and the formal rules '
        'of engagement governing penetration testing and vulnerability assessments on Google Cloud infrastructure.'
    ),
    'exit_summary': (
        'A threat model, incident timeline and owners for the highest residual risks.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts incident response phases, forensic preservation mechanics, '
        'threat modeling vectors, and security assessment boundaries across cloud-native environments.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Operational Phase</th>\n'
        '<th>Core Technical Action</th>\n'
        '<th>Primary GCP Mechanisms</th>\n'
        '<th>Data Artifact &amp; Evidence Output</th>\n'
        '<th>Critical Anti-Pattern &amp; Risk</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>1. Incident Detection &amp; Triage</strong></td>\n'
        '<td>Telemetry correlation, blast radius evaluation, severity assignment</td>\n'
        '<td>Security Command Center, Chronicle SIEM, Cloud Logging, Pub/Sub</td>\n'
        '<td>Unified incident ticket, initial IOC inventory, timeline log</td>\n'
        '<td>Premature termination of compromised instances destroying volatile memory.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>2. Containment &amp; Isolation</strong></td>\n'
        '<td>Network quarantine, identity invalidation, credential revocation</td>\n'
        '<td>Cloud NGFW quarantine tags, IAM key disablement, OAuth session revocation</td>\n'
        '<td>Quarantined resource IDs, active network session drop confirmations</td>\n'
        '<td>Broad network cut isolating critical shared database or telemetry collectors.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>3. Forensic Acquisition</strong></td>\n'
        '<td>Non-destructive disk imaging, memory dump, immutable log lock</td>\n'
        '<td>Archive disk snapshots, KMS CMEK export, GCS Bucket Lock (WORM)</td>\n'
        '<td>SHA-256 disk hash manifest, chain-of-custody ledger, raw audit exports</td>\n'
        '<td>Rebooting or attaching writable forensic tooling directly to evidence disks.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>4. Threat Modeling (STRIDE)</strong></td>\n'
        '<td>Decomposing architectures into trust boundaries, flows, and mitigations</td>\n'
        '<td>Data Flow Diagrams (DFD), IAM Recommender, VPC Service Controls</td>\n'
        '<td>STRIDE risk register, DREAD score matrix, mitigation backlog</td>\n'
        '<td>Ignoring service account impersonation chains (`actAs`) across project boundaries.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>5. Pen Testing Governance</strong></td>\n'
        '<td>Controlled adversarial simulation adhering to Google Cloud policies</td>\n'
        '<td>Customer-managed VMs, Cloud Armor rate controls, red-team scopes</td>\n'
        '<td>Authorized Rules of Engagement (RoE), testing window log, finding report</td>\n'
        '<td>Launching volumetric DoS/DDoS tests violating Google Acceptable Use Policy.</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 113: Incident Response Lifecycle, Forensic Isolation, and STRIDE Threat Model Topology',
        'desc': 'Architectural layout illustrating incident triage pipelines, forensic snapshot isolation into dedicated projects, immutable WORM log preservation, STRIDE trust boundaries, and penetration testing controls.',
        'caption': 'Figure 113.1: Enterprise cloud incident response and forensic topology featuring automated containment, quarantined evidence projects, immutable log retention, and threat modeling boundaries.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Compromised Production Workload Plane',
                'desc': 'Active GKE pods, Compute Engine VMs, and IAM identities exhibiting anomalous threat behaviors',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Dynamic Containment & Network Isolation Boundary',
                'desc': 'Cloud NGFW quarantine tag injection, IAM token revocation, and egress route nullification',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Forensic Snapshot & Evidence Acquisition Pipeline',
                'desc': 'Archive disk snapshots, cryptographic SHA-256 hash minters, and memory image collectors',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Quarantined Forensic Analysis & WORM Storage Vault',
                'desc': 'Isolated forensics project, read-only disk mounts, SEC 17a-4 locked Cloud Storage buckets',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: STRIDE Threat Modeling & Governance Control Plane',
                'desc': 'Trust boundary enforcement, impersonation prevention, and penetration testing rules of engagement',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Compromised Workload VM', 'detail': 'Active Rootkit / C2 Egress', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Compromised SA Identity', 'detail': 'Rogue Key Downloaded', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Isolation Tag Injector', 'detail': 'NGFW Deny-All Rule 0', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'IAM Credential Revoker', 'detail': 'Token Invalidation API', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Archive Disk Snapshot', 'detail': 'Read-Only Bitstream Copy', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Evidence Hash Minter', 'detail': 'SHA-256 Chain of Custody', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Forensics Workstation', 'detail': 'Isolated Analysis Project', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'WORM Evidence Bucket', 'detail': 'Locked Retention Policy', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'STRIDE Threat Register', 'detail': 'Boundary & Flow Matrix', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'Pen Test RoE Validator', 'detail': 'AUP Scope Compliance', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'ACTIVE PRODUCTION THREAT & ISOLATION BOUNDARY', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'CRYPTOGRAPHIC FORENSIC PRESERVATION VAULT', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'ARCHITECTURE THREAT MODEL & GOVERNANCE PLANE', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Detect Privilege Abuse', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Apply Isolation Tag', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Revoke OAuth Sessions', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Snapshot Persistent Disk', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Generate Hash Ledger', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Attach RO Disk to Forensics', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Lock Logs in WORM GCS', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Evaluate STRIDE Vectors', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Enforce Pen Test RoE', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: Containment Verification: Zero Outbound Egress Packets', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: Bitstream Integrity: SHA-256 Snapshot Checksum Match', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 450, 'label': 'PROBE 3: Threat Modeling Review: Zero Unauthenticated Trust Edges', 'badge': 'P3', 'color': '#22c55e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world incident handling failures, evidence destruction blunders, '
        'unmodeled IAM privilege escalation chains, and unauthorized penetration testing disruptions across Google Cloud estates. '
        'Each scenario details verbatim diagnostic logs, root cause mechanisms, production remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on architectural exercises implement the complete operational engineering lifecycle for Day 113. '
        'Architects author an incident response orchestration runner, build an automated forensic disk snapshot and evidence hashing tool, '
        'develop a programmatic STRIDE threat modeling engine, and enforce a penetration testing rules-of-engagement validator.'
    ),
    'topics': [
        # TOPIC 1
        {
            'key': 'topic-01',
            'title': 'Incident response process: detect, contain, eradicate, recover, learn',
            'overview': (
                'An effective cloud incident response process translates traditional operational playbooks (NIST SP 800-61 / ISO 27035) '
                'into API-driven, cloud-native operational reality. Google Cloud incident response requires rapid orchestration across '
                'five discrete phases: Detect (telemetry correlation and blast radius assessment), Contain (short-term isolation versus '
                'long-term boundary lockdown), Eradicate (purging persistence vectors and revoking compromised credentials), '
                'Recover (controlled restoration from trusted baselines), and Learn (blameless postmortem and prevention automation).'
            ),
            'preview': (
                'An on-call engineer deletes a compromised VM during an active breach, inadvertently destroying the volatile RAM '
                'and command history needed to identify persistent backdoor accounts planted across the organization.'
            ),
            'technical': (
                'Cloud incident response requires structured coordination across technical, operational, and organizational domains.\n\n'
                '### 1. Detect & Triage\n'
                '- **Signal Correlation**: Ingesting high-fidelity alerts from Security Command Center, Chronicle SIEM, and Cloud Logging.\n'
                '- **Severity Categorization**: Classifying incidents into formal tiers:\n'
                '  - **SEV-0 (Catastrophic)**: Organization-wide breach, root credential compromise, active mass data exfiltration.\n'
                '  - **SEV-1 (Critical)**: Production service compromise, customer PII exposure, active lateral movement.\n'
                '  - **SEV-2 (Major)**: Isolated workload breach, single service account compromise without privilege escalation.\n'
                '  - **SEV-3 (Minor)**: Localized policy violation or contained malware without business disruption.\n'
                '- **Incident Command System (ICS)**: Establishing roles: Incident Commander (leads response), Technical Lead (coordinates forensics), '
                'and Communications Lead (manages regulatory disclosures and customer updates).\n\n'
                '### 2. Containment Strategy\n'
                '- **Short-Term Containment**: Stop immediate damage without destroying forensic evidence.\n'
                '  - Network Isolation: Applying a Cloud NGFW isolation network tag (`quarantine-isolate`) with a priority 0 deny-all egress rule.\n'
                '  - Identity Revocation: Disabling compromised service account keys (<kbd>gcloud iam service-accounts keys disable</kbd>), revoking user OAuth tokens, and stripping role bindings.\n'
                '  - Workload Freeze: Pausing GKE pods or disabling autoscaling to prevent malware propagation to newly minted nodes.\n'
                '- **Long-Term Containment**: Isolating affected VPC subnets, revoking shared VPC peering routes, and rotating Cloud KMS CryptoKeys.\n\n'
                '### 3. Eradication & Remediation\n'
                '- Identifying and eliminating all persistence mechanisms: rogue service account keys, modified IAM policies, unauthorized Cloud Scheduler jobs, '
                'backdoor Docker images in Artifact Registry, and rogue Cloud Functions.\n'
                '- Rebuilding infrastructure from verified, immutable Infrastructure-as-Code (Terraform) manifests and clean base images rather than patching compromised systems.\n\n'
                '### 4. Recovery & Verification\n'
                '- Restoring systems from pre-incident, validated immutable backups or re-deploying clean containers via CI/CD.\n'
                '- Operating in heightened surveillance mode: enabling verbose Cloud Audit Data Access logs, strict VPC Flow Logging, and dedicated Chronicle SIEM detection rules for 30 days.\n\n'
                '### 5. Lessons Learned & Postmortem\n'
                '- Conducting a blameless post-incident review within 72 hours of incident closure.\n'
                '- Documenting the exact timeline, root causes (5 Whys), detection latency, containment duration, and corrective action items assigned with deadlines.'
            ),
            'questions': [
                'Why must containment actions precede instance destruction or reboot during an active cloud security incident?',
                'How does applying a high-priority Cloud NGFW isolation tag halt lateral movement without destroying volatile host memory?',
                'What are the critical components of a blameless postmortem following a cloud data breach?'
            ],
            'reference': 'https://docs.cloud.google.com/security-command-center/docs',
            'reference_label': 'Google Cloud Incident Response and Security Operations Best Practices',
            'scenario': {
                'symptom': 'Cryptomining alert triggers panic; engineer terminates Compute Engine VM; lateral persistence goes undiscovered.',
                'impact': 'Attacker retains secondary foothold via rogue service account key; launches ransomware across cloud storage buckets 48 hours later.',
                'constraints': 'Incident response procedures must mandate evidence preservation prior to destructive eradication.',
                'evidence': (
                    'Audit Log showing premature VM deletion:\n\n'
                    '```json\n'
                    '{\n'
                    '  "protoPayload": {\n'
                    '    "methodName": "v1.compute.instances.delete",\n'
                    '    "principalEmail": "junior-oncall@enterprise.com",\n'
                    '    "resourceName": "projects/prod/zones/us-central1-a/instances/api-gw-01"\n'
                    '  }\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: Deleting the instance destroyed volatile memory containing bash history and injected environment variables, '
                    'hiding the fact that the attacker had already executed <kbd>gcloud iam service-accounts keys create</kbd> on a backend billing identity.'
                ),
                'diagnostic_steps': [
                    'Inspect Cloud Audit Logs for administrative actions performed by the compromised instance’s attached service account.',
                    'Check for service account key creation events (`CreateServiceAccountKey`) across all projects within 24 hours of the alert.',
                    'Review Cloud Logging for VPC Flow Log egress traffic from adjacent instances to identify lateral movement attempts.',
                    'Review incident response documentation to verify why non-destructive isolation was bypassed.'
                ],
                'root': 'The on-call operational runbook lacked a mandatory containment stage, allowing engineers to delete compromised resources before forensic snapshots and identity audits were performed.',
                'fix': 'Enforce an automated incident response workflow where compromised VMs are tagged for network quarantine and snapshotted automatically, removing manual delete permissions from incident responders.',
                'verify': 'Simulate an incident in a sandbox project; verify the containment script applies isolation firewall tags and triggers snapshots without terminating instances.',
                'residual': 'Encrypted malware command-and-control communication traversing permitted outbound DNS tunnels could evade basic IP-based network isolation.',
                'diagram': (
                    'SCC detects active cryptocurrency mining on production API gateway instance',
                    'Panicked on-call engineer deletes VM immediately instead of isolating it',
                    'Instance RAM and process history erased; rogue SA key remains undetected',
                    'Implement mandatory automated quarantine tagging and forensic disk snapshotting',
                    'Attacker persistence fully cataloged and eradicated; zero evidence destroyed'
                )
            },
            'lab': {
                'name': 'Cloud Incident Response Workflow Runner & Timeline Tracker',
                'goal': 'Implement a Python incident response orchestration engine that ingests security alerts, assigns severity tiers, executes non-destructive network isolation, and generates an auditable incident timeline.',
                'expected': 'A functional Python IR orchestrator that evaluates alert severity and generates declarative quarantine and recovery plans.',
                'mode': 'Python script and CLI data modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/cloud-ir-lab</kbd>.',
                'steps': [
                    (
                        '#### Set up Sample Security Incident Payload\n'
                        'Create the lab directory and write a JSON file representing a multi-stage security incident involving compromised credentials and unauthorized compute provisioning:\n\n'
                        '```sh\n'
                        'mkdir -p ~/cloud-ir-lab && cd ~/cloud-ir-lab\n'
                        'cat <<\'EOF\' > active_incident.json\n'
                        '{\n'
                        '  "incident_id": "INC-2026-0929",\n'
                        '  "title": "Unauthorized Persistence and Anomalous Compute Provisioning",\n'
                        '  "initial_detector": "CHRONICLE_ETD",\n'
                        '  "detected_time": "2026-09-29T09:00:00Z",\n'
                        '  "affected_resources": [\n'
                        '    {\n'
                        '      "type": "compute_instance",\n'
                        '      "resource_id": "projects/fintech-prod/zones/us-central1-a/instances/crypto-worker-01",\n'
                        '      "zone": "us-central1-a",\n'
                        '      "ip_address": "10.0.1.45"\n'
                        '    },\n'
                        '    {\n'
                        '      "type": "service_account",\n'
                        '      "resource_id": "projects/fintech-prod/serviceAccounts/data-exporter@fintech-prod.iam.gserviceaccount.com",\n'
                        '      "email": "data-exporter@fintech-prod.iam.gserviceaccount.com"\n'
                        '    }\n'
                        '  ],\n'
                        '  "indicators": {\n'
                        '    "c2_ip": "198.51.100.99",\n'
                        '    "rogue_key_id": "key-883920194"\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Incident Response Orchestration Engine\n'
                        'Write a Python incident management script that executes the PICERL lifecycle: calculates severity, generates non-destructive containment commands, creates forensic tasks, and outputs an incident timeline log:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > ir_orchestrator.py\n'
                        'import json\n'
                        'from datetime import datetime, timezone\n'
                        '\n'
                        'def run_incident_response():\n'
                        '    with open("active_incident.json", "r") as f:\n'
                        '        inc = json.load(f)\n'
                        '\n'
                        '    timeline = []\n'
                        '    def log_event(phase, action, detail):\n'
                        '        entry = {\n'
                        '            "timestamp": datetime.now(timezone.utc).isoformat(),\n'
                        '            "phase": phase,\n'
                        '            "action": action,\n'
                        '            "detail": detail\n'
                        '        }\n'
                        '        timeline.append(entry)\n'
                        '        print(f"[{entry[\'phase\']}] {action}: {detail}")\n'
                        '\n'
                        '    print(f"=== Activating Incident Response Protocol: {inc[\'incident_id\']} ===\\n")\n'
                        '\n'
                        '    # Phase 1: Detect & Triage\n'
                        '    log_event("DETECT", "TRIAGE_ALERT", f"Ingested {inc[\'initial_detector\']} alert: {inc[\'title\']}")\n'
                        '    sev = "SEV-1"\n'
                        '    log_event("DETECT", "ASSIGN_SEVERITY", f"Assigned {sev} based on multi-resource compromise")\n'
                        '\n'
                        '    # Phase 2: Containment (Non-Destructive Isolation)\n'
                        '    containment_commands = []\n'
                        '    for res in inc["affected_resources"]:\n'
                        '        if res["type"] == "compute_instance":\n'
                        '            vm = res["resource_id"].split("/")[-1]\n'
                        '            zone = res["zone"]\n'
                        '            cmd1 = f"gcloud compute instances add-tags {vm} --tags=quarantine-isolate --zone={zone}"\n'
                        '            containment_commands.append(cmd1)\n'
                        '            log_event("CONTAIN", "NETWORK_ISOLATION", f"Tagging VM {vm} with quarantine-isolate")\n'
                        '        elif res["type"] == "service_account":\n'
                        '            sa = res["email"]\n'
                        '            key_id = inc["indicators"]["rogue_key_id"]\n'
                        '            cmd2 = f"gcloud iam service-accounts keys disable {key_id} --iam-account={sa}"\n'
                        '            containment_commands.append(cmd2)\n'
                        '            log_event("CONTAIN", "CREDENTIAL_REVOCATION", f"Disabling rogue key {key_id} on {sa}")\n'
                        '\n'
                        '    # Phase 3: Eradication\n'
                        '    log_event("ERADICATE", "PERSISTENCE_AUDIT", "Scanning all projects for unauthorized serviceAccountKeys and IAM role bindings")\n'
                        '    \n'
                        '    # Phase 4: Recovery\n'
                        '    log_event("RECOVER", "CANARY_RESTORATION", "Re-deploying clean immutable containers via validated CI/CD commit hash")\n'
                        '\n'
                        '    # Phase 5: Lessons Learned\n'
                        '    log_event("LEARN", "SCHEDULE_POSTMORTEM", "Scheduling blameless postmortem within 48 hours; assigning PIR owner")\n'
                        '\n'
                        '    record = {\n'
                        '        "incident_id": inc["incident_id"],\n'
                        '        "severity": sev,\n'
                        '        "containment_execution_plan": containment_commands,\n'
                        '        "incident_timeline": timeline\n'
                        '    }\n'
                        '\n'
                        '    with open("incident_response_record.json", "w") as out:\n'
                        '        json.dump(record, out, indent=2)\n'
                        '    print("\\nIR Workflow completed. Wrote incident_response_record.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    run_incident_response()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute the IR Orchestrator and Inspect Generated Record\n'
                        'Run the orchestration tool and verify that containment commands isolate the VM and revoke rogue service account keys without terminating infrastructure:\n\n'
                        '```sh\n'
                        'python3 ir_orchestrator.py\n'
                        'cat incident_response_record.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python incident response orchestrator demonstrating non-destructive containment sequencing and complete PICERL timeline logging.',
                'verification': 'Review terminal output of <kbd>python3 ir_orchestrator.py</kbd> confirming containment execution commands and complete phase progression.',
                'trouble': 'If JSON file cannot be found, verify file creation with <kbd>ls -la</kbd>.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/cloud-ir-lab</kbd>.',
                'file': 'day-113-incident-response.md'
            }
        },

        # TOPIC 2
        {
            'key': 'topic-02',
            'title': 'Forensics basics: snapshots, log preservation, evidence handling',
            'overview': (
                'Digital forensics in Google Cloud requires acquiring and preserving legally defensible digital evidence from cloud '
                'infrastructure without altering original media states or breaking chain of custody. Forensics specialists must understand '
                'the distinction between volatile evidence (RAM, running processes, open network sockets) and non-volatile evidence '
                '(persistent disks, object storage, and audit logs), mastering non-destructive disk snapshotting, cryptographic hashing, '
                'and immutable WORM log retention.'
            ),
            'preview': (
                'An investigator executes a standard reboot on a suspected compromised VM to attach an analysis tool, wiping volatile '
                'memory and resetting inode access times needed for criminal prosecution.'
            ),
            'technical': (
                'Forensic evidence handling in Google Cloud adheres to strict legal standards of admissibility and chain of custody.\n\n'
                '### Volatile vs Non-Volatile Telemetry\n'
                '1. **Volatile Evidence**: Vanishes immediately upon instance reboot, shutdown, or migration. Includes CPU registers, '
                'kernel memory structures, running process tables, active TCP/UDP connections, and decrypted TLS session keys. '
                'In Compute Engine, volatile memory cannot be snapshotted directly from the API unless Virtual Machine Threat Detection (VMTD) '
                'is active or in-guest memory dumping tools (e.g. LiME, AVML) are deployed prior to stopping the instance.\n'
                '2. **Non-Volatile Evidence**: Preserved persistently across reboots. Includes persistent disks, Cloud Storage objects, '
                'and immutable Cloud Audit Logs.\n\n'
                '### Non-Destructive Persistent Disk Forensics Pipeline\n'
                'To inspect a compromised Compute Engine disk without altering evidentiary integrity:\n'
                '- **Step 1: Take Archive Snapshot**: Execute an archive snapshot of the persistent disk while the instance is quarantined:\n'
                '  <kbd>gcloud compute disks snapshot [DISK_NAME] --snapshot-type=ARCHIVE --zone=[ZONE]</kbd>.\n'
                '- **Step 2: Generate Cryptographic Hash**: Compute a cryptographic SHA-256 hash manifest of the snapshot or disk image.\n'
                '- **Step 3: Transfer to Quarantined Forensics Project**: Share the snapshot with a dedicated, isolated forensics GCP project '
                'with restricted IAM access and zero production network routing.\n'
                '- **Step 4: Mount Read-Only on Forensics Analysis Workstation**: Create a new persistent disk from the snapshot and attach it '
                'to a sanitized analysis VM strictly in read-only mode (`mode=READ_ONLY`). Never boot directly from the compromised disk.\n\n'
                '### Immutable Audit Log Preservation (WORM)\n'
                'Attackers frequently attempt to cover their tracks by deleting Cloud Logging buckets or modifying log sinks.\n'
                '- **Aggregated Log Sinks**: Configure organization-level log sinks routing all Admin Activity, Data Access, and VPC Flow Logs '
                'to a centralized security vault project.\n'
                '- **Bucket Lock (WORM - Write Once, Read Many)**: Store logs in a Cloud Storage bucket governed by a locked object retention policy. '
                'Once locked, objects cannot be overwritten, modified, or deleted by any user—including Organization Administrators—until the retention '
                'period expires (fulfilling SEC Rule 17a-4 and FINRA requirements).\n'
                '- **Legal Holds**: Place indefinite legal holds on specific evidence objects during ongoing litigation or criminal investigations.'
            ),
            'questions': [
                'Why must a persistent disk snapshot created for forensics be attached to an analysis VM exclusively in read-only mode?',
                'How does a Cloud Storage locked retention policy (Bucket Lock) prevent attackers with stolen administrative credentials from deleting audit logs?',
                'What is the evidentiary purpose of computing and recording a SHA-256 hash immediately upon disk image acquisition?'
            ],
            'reference': 'https://docs.cloud.google.com/security-command-center/docs',
            'reference_label': 'Google Cloud Digital Forensics and Evidence Preservation Guide',
            'scenario': {
                'symptom': 'Security team stops and reboots a compromised web server VM to attach analysis tools; prosecution collapses due to broken evidence custody.',
                'impact': 'Criminal case dismissed by judicial authorities because memory artifacts were purged and disk access timestamps were modified during reboot.',
                'constraints': 'Evidence acquisition procedures must preserve bitstream disk integrity and document complete cryptographic chain of custody.',
                'evidence': (
                    'Audit Log showing writable disk attachment and inode modification:\n\n'
                    '```json\n'
                    '{\n'
                    '  "protoPayload": {\n'
                    '    "methodName": "v1.compute.instances.attachDisk",\n'
                    '    "request": {\n'
                    '      "mode": "READ_WRITE",\n'
                    '      "source": "projects/prod/zones/us-central1-a/disks/compromised-root"\n'
                    '    }\n'
                    '  }\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: Attaching the compromised disk in `READ_WRITE` mode caused the analysis operating system to write journal entries '
                    'and update filesystem access timestamps, destroying evidence admissibility in court.'
                ),
                'diagnostic_steps': [
                    'Review Cloud Audit Logs to inspect how the evidentiary disk was attached to analysis instances.',
                    'Check whether an initial archive snapshot was executed prior to mounting the disk.',
                    'Verify the existence of a signed SHA-256 hash manifest recorded at the exact moment of disk acquisition.',
                    'Confirm whether volatile memory capture was attempted before instance shutdown.'
                ],
                'root': 'Investigators mounted the original evidence disk in READ_WRITE mode rather than snapshotting it and attaching a cloned disk in READ_ONLY mode.',
                'fix': 'Mandate that evidence disks are snapshotted immediately, cloned into an isolated forensics project, and mounted strictly with mode=READ_ONLY.',
                'residual': 'Encrypted ephemeral scratch disks (local-ssd) cannot be snapshotted via the Compute Engine API and require in-guest bitstream copying.',
                'diagram': (
                    'Investigators stop compromised VM and attach disk in READ_WRITE mode',
                    'Operating system updates filesystem journal and overwrites access times',
                    'Cryptographic integrity violated; court rejects evidence chain of custody',
                    'Enforce procedure: Archive snapshot, SHA-256 hash, and attach as READ_ONLY',
                    'Forensic evidence preserved verifiably; legal admissibility guaranteed'
                )
            },
            'lab': {
                'name': 'Forensic Disk Imaging and Chain-of-Custody Manifest Generator',
                'goal': 'Implement a Python forensics automation script that simulates creating a forensic disk snapshot, calculates cryptographic SHA-256 checksums, mounts in read-only mode, and generates an immutable chain-of-custody ledger.',
                'expected': 'A verified Python forensic tool creating cryptographic evidence manifests and chain-of-custody logs.',
                'mode': 'Python script and CLI data modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/forensics-lab</kbd>.',
                'steps': [
                    (
                        '#### Generate Synthetic Evidence File and Disk Image\n'
                        'Create a simulated disk image containing evidence files, logs, and suspicious bash history:\n\n'
                        '```sh\n'
                        'mkdir -p ~/forensics-lab && cd ~/forensics-lab\n'
                        'cat <<\'EOF\' > evidence_disk.raw\n'
                        '[ROOT_FS_HEADER_BLOCK_001]\n'
                        'TIMESTAMP=2026-09-29T08:30:00Z\n'
                        'INODE_TABLE_START\n'
                        '/bin/bash: modified=false\n'
                        '/tmp/.hidden_miner: md5=e99a18c428cb38d5f260853678922e03, user=root\n'
                        '/etc/shadow: accessed=true\n'
                        'INODE_TABLE_END\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Forensic Evidence Acquisition Tool\n'
                        'Write a Python tool that computes cryptographic SHA-256 hashes, generates an immutable acquisition record, and validates read-only analysis parameters:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > acquire_evidence.py\n'
                        'import hashlib\n'
                        'import json\n'
                        'import sys\n'
                        'from datetime import datetime, timezone\n'
                        '\n'
                        'def hash_file(filepath):\n'
                        '    hasher = hashlib.sha256()\n'
                        '    with open(filepath, "rb") as f:\n'
                        '        while chunk := f.read(65536):\n'
                        '            hasher.update(chunk)\n'
                        '    return hasher.hexdigest()\n'
                        '\n'
                        'def acquire_disk(disk_path, investigator, case_id):\n'
                        '    print(f"=== Starting Evidence Acquisition for {case_id} ===\\n")\n'
                        '    sha256_hash = hash_file(disk_path)\n'
                        '    print(f"Original Disk SHA-256: {sha256_hash}")\n'
                        '\n'
                        '    # Generate Forensic Chain of Custody Record\n'
                        '    manifest = {\n'
                        '        "case_id": case_id,\n'
                        '        "acquisition_timestamp": datetime.now(timezone.utc).isoformat(),\n'
                        '        "investigator": investigator,\n'
                        '        "source_disk": disk_path,\n'
                        '        "evidence_sha256": sha256_hash,\n'
                        '        "storage_location": "gs://forensic-vault-sec17a4-immutable/cases/INC-2026-0929/disk.raw",\n'
                        '        "mount_policy": {\n'
                        '            "mode": "READ_ONLY",\n'
                        '            "allow_write": False,\n'
                        '            "quarantine_project": "proj-sec-forensics-isolated"\n'
                        '        },\n'
                        '        "integrity_verified": True\n'
                        '    }\n'
                        '\n'
                        '    with open("chain_of_custody_manifest.json", "w") as out:\n'
                        '        json.dump(manifest, out, indent=2)\n'
                        '    print("Chain of Custody Manifest generated successfully.")\n'
                        '    \n'
                        '    # Verification check: Ensure read-only invariant\n'
                        '    assert manifest["mount_policy"]["mode"] == "READ_ONLY", "VIOLATION: Disk must be read-only!"\n'
                        '    print("Invariant Verified: Mount mode is strictly READ_ONLY.\\n")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    acquire_disk("evidence_disk.raw", "lead-forensic-examiner@enterprise.com", "CASE-2026-0929")\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute Acquisition Script and Verify Chain-of-Custody Manifest\n'
                        'Run the forensic tool, compute the hash, and inspect the resulting JSON chain-of-custody ledger:\n\n'
                        '```sh\n'
                        'python3 acquire_evidence.py\n'
                        'cat chain_of_custody_manifest.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python forensic acquisition tool generating SHA-256 checksum manifests and verifying read-only mount parameters.',
                'verification': 'Review terminal output of <kbd>python3 acquire_evidence.py</kbd> confirming SHA-256 hash generation and invariant verification.',
                'trouble': 'If hashing fails, ensure `evidence_disk.raw` exists in current directory.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/forensics-lab</kbd>.',
                'file': 'day-113-forensics-acquisition.md'
            }
        },

        # TOPIC 3
        {
            'key': 'topic-03',
            'title': 'Threat modelling (STRIDE) on your own architecture',
            'overview': (
                'Threat modeling provides a proactive, structured framework for identifying security flaws, trust boundary crossings, '
                'and threat actor incentives early in the architectural lifecycle. The STRIDE methodology decomposes cloud architectures '
                'into six threat categories: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of '
                'Privilege. In Google Cloud architectures, STRIDE specifically exposes risks associated with service account impersonation chains, '
                'unsegmented VPC topologies, and missing IAM resource boundaries.'
            ),
            'preview': (
                'An enterprise analytics architecture allows a low-privilege ETL worker pod to impersonate a privileged data-warehouse '
                'service account via missing `iam.serviceAccounts.actAs` restrictions, enabling tenant database takeover.'
            ),
            'technical': (
                'Applying STRIDE to cloud architectures requires mapping Data Flow Diagrams (DFDs) across cloud trust boundaries.\n\n'
                '### STRIDE Taxonomy Applied to Google Cloud\n'
                '1. **Spoofing (Identity Compromise)**:\n'
                '   - *Cloud Threat*: Stealing or forging service account keys, abusing user OAuth tokens, or impersonating identities across projects.\n'
                '   - *GCP Mitigations*: Disabling service account key creation (`constraints/iam.disableServiceAccountKeyCreation`), adopting Workload Identity Federation, and requiring mTLS with Certificate Authority Service.\n'
                '2. **Tampering (Data & Configuration Integrity)**:\n'
                '   - *Cloud Threat*: Modifying container images in Artifact Registry, altering BigQuery transaction logs, or tampering with Terraform state files.\n'
                '   - *GCP Mitigations*: Binary Authorization attestations, Cloud KMS CMEK encryption, GCS Object Versioning, and Bucket Lock (WORM).\n'
                '3. **Repudiation (Audit Evasion)**:\n'
                '   - *Cloud Threat*: An attacker executing administrative actions and denying involvement, or disabling audit logging.\n'
                '   - *GCP Mitigations*: Cloud Audit Logs (Admin Activity + Data Access), Access Transparency, aggregated log sinks routing to locked storage vaults.\n'
                '4. **Information Disclosure (Data Exfiltration)**:\n'
                '   - *Cloud Threat*: Exfiltrating sensitive customer PII from Cloud Storage or BigQuery to external unowned buckets.\n'
                '   - *GCP Mitigations*: VPC Service Controls security perimeters, Cloud DLP (Sensitive Data Protection) inspection and masking, Private Service Connect.\n'
                '5. **Denial of Service (Resource & Quota Exhaustion)**:\n'
                '   - *Cloud Threat*: Exhausting Cloud Run instance concurrency, launching volumetric HTTP floods against public APIs, or draining API rate quotas.\n'
                '   - *GCP Mitigations*: Cloud Armor rate limiting and adaptive DDoS protection, max instance scaling limits, and quota alert monitoring.\n'
                '6. **Elevation of Privilege (Privilege Escalation)**:\n'
                '   - *Cloud Threat*: A compromised low-privilege workload leveraging `iam.serviceAccounts.actAs` or `resourcemanager.projects.setIamPolicy` to grant itself Organization Administrator.\n'
                '   - *GCP Mitigations*: Least privilege IAM, IAM Recommender removal of excessive permissions, Policy Controller admission webhooks, and restricting `iam.serviceAccountTokenCreator`.'
            ),
            'questions': [
                'How does the STRIDE model systematically uncover service account impersonation chains across Google Cloud projects?',
                'Why are VPC Service Controls perimeters considered the definitive mitigation against Information Disclosure (Data Exfiltration)?',
                'What architectural control prevents Elevation of Privilege when a workload pod requires access to an external Google API?'
            ],
            'reference': 'https://docs.cloud.google.com/security-command-center/docs',
            'reference_label': 'Google Cloud Threat Modeling and Security Architecture Framework',
            'scenario': {
                'symptom': 'Low-privilege marketing analytics pod queries and dumps the primary production payment credit card database.',
                'impact': 'Catastrophic regulatory breach under PCI-DSS; 1.2 million cardholder records exfiltrated to an external bucket.',
                'constraints': 'Workloads must never be able to mint tokens for identities outside their explicit microservice boundary.',
                'evidence': (
                    'Audit Log showing service account token generation:\n\n'
                    '```json\n'
                    '{\n'
                    '  "protoPayload": {\n'
                    '    "methodName": "GenerateAccessToken",\n'
                    '    "authenticationInfo": {\n'
                    '      "principalEmail": "marketing-analytics-sa@prod.iam.gserviceaccount.com"\n'
                    '    },\n'
                    '    "request": {\n'
                    '      "name": "projects/-/serviceAccounts/payment-master-sa@prod.iam.gserviceaccount.com"\n'
                    '    }\n'
                    '  }\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: The marketing service account had been granted `roles/iam.serviceAccountTokenCreator` on the parent project, '
                    'allowing it to impersonate ANY service account in the project, including the database master administrator.'
                ),
                'diagnostic_steps': [
                    'Review IAM policy bindings on the project to inspect grants of `roles/iam.serviceAccountTokenCreator`.',
                    'Check Cloud Audit Logs for `GenerateAccessToken` and `SignBlob` API invocations across all service accounts.',
                    'Inspect the data flow diagram to trace why a marketing analytics service was co-located in the same project as payment databases.',
                    'Evaluate GKE Workload Identity bindings for the marketing analytics Kubernetes service account.'
                ],
                'root': 'A broad grant of `roles/iam.serviceAccountTokenCreator` at the project level enabled an Elevation of Privilege threat vector via service account impersonation.',
                'fix': 'Revoke the project-level token creator role, segregate workloads into dedicated projects, and restrict Workload Identity bindings strictly to designated least-privilege identities.',
                'verify': 'Attempt token generation from the marketing analytics pod using <kbd>gcloud auth print-access-token --impersonate-service-account</kbd>; verify permission denied error.',
                'residual': 'Authorized analytical queries must be sanitized via tokenization pipelines to prevent direct exposure to cardholder telemetry.',
                'diagram': (
                    'Marketing worker pod compromised via unpatched dependency flaw',
                    'Attacker leverages project-level serviceAccountTokenCreator role',
                    'Worker impersonates payment-master-sa and extracts database encryption keys',
                    'Enforce STRIDE mitigation: Segregate projects and eliminate token creator role',
                    'Workloads restricted strictly to least-privilege; impersonation blocked'
                )
            },
            'lab': {
                'name': 'STRIDE Threat Modeling Engine & Risk Matrix Evaluator',
                'goal': 'Develop a Python STRIDE threat modeling tool that ingests an architecture component graph, identifies trust boundary crossings, maps threat vectors, and computes composite DREAD risk scores.',
                'expected': 'A functioning Python STRIDE evaluation engine that parses architecture models and produces a prioritized mitigation register.',
                'mode': 'Python script and CLI modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/stride-lab</kbd>.',
                'steps': [
                    (
                        '#### Define Architectural Topology and Trust Boundaries\n'
                        'Create a JSON model representing a cloud microservice architecture with public ingress, analytical processing, and storage components:\n\n'
                        '```sh\n'
                        'mkdir -p ~/stride-lab && cd ~/stride-lab\n'
                        'cat <<\'EOF\' > architecture_graph.json\n'
                        '{\n'
                        '  "system_name": "Cloud Payment Processing Pipeline",\n'
                        '  "components": [\n'
                        '    {\n'
                        '      "id": "COMP-01",\n'
                        '      "name": "Public API Gateway",\n'
                        '      "type": "process",\n'
                        '      "trust_zone": "INTERNET_FACING",\n'
                        '      "auth": "API_KEY"\n'
                        '    },\n'
                        '    {\n'
                        '      "id": "COMP-02",\n'
                        '      "name": "Transaction Processor Pod",\n'
                        '      "type": "process",\n'
                        '      "trust_zone": "RESTRICTED_CDE",\n'
                        '      "auth": "WORKLOAD_IDENTITY"\n'
                        '    },\n'
                        '    {\n'
                        '      "id": "COMP-03",\n'
                        '      "name": "Cardholder Data Vault",\n'
                        '      "type": "data_store",\n'
                        '      "trust_zone": "RESTRICTED_CDE",\n'
                        '      "auth": "IAM_CMEK"\n'
                        '    }\n'
                        '  ],\n'
                        '  "flows": [\n'
                        '    {\n'
                        '      "source": "COMP-01",\n'
                        '      "target": "COMP-02",\n'
                        '      "protocol": "HTTP",\n'
                        '      "crosses_trust_boundary": true\n'
                        '    },\n'
                        '    {\n'
                        '      "source": "COMP-02",\n'
                        '      "target": "COMP-03",\n'
                        '      "protocol": "GRPC_TLS",\n'
                        '      "crosses_trust_boundary": false\n'
                        '    }\n'
                        '  ]\n'
                        '}\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Automated STRIDE Evaluation Tool\n'
                        'Write a Python engine that parses the architecture, identifies vulnerabilities (unencrypted trust boundary traversal, weak auth), and maps STRIDE mitigations:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > stride_evaluator.py\n'
                        'import json\n'
                        'import sys\n'
                        '\n'
                        'def evaluate_stride():\n'
                        '    with open("architecture_graph.json", "r") as f:\n'
                        '        arch = json.load(f)\n'
                        '\n'
                        '    print(f"=== Running STRIDE Threat Model: {arch[\'system_name\']} ===\\n")\n'
                        '    threats = []\n'
                        '\n'
                        '    # Evaluate components\n'
                        '    for comp in arch["components"]:\n'
                        '        cid = comp["id"]\n'
                        '        cname = comp["name"]\n'
                        '        auth = comp["auth"]\n'
                        '        zone = comp["trust_zone"]\n'
                        '\n'
                        '        if zone == "INTERNET_FACING" and auth == "API_KEY":\n'
                        '            threats.append({\n'
                        '                "component": cname,\n'
                        '                "category": "SPOOFING",\n'
                        '                "threat": "Static API Key is susceptible to interception and token replay.",\n'
                        '                "severity": "HIGH",\n'
                        '                "mitigation": "Enforce OAuth 2.0 with PKCE and Google Cloud Armor rate limiting."\n'
                        '            })\n'
                        '\n'
                        '    # Evaluate flows\n'
                        '    for flow in arch["flows"]:\n'
                        '        src = flow["source"]\n'
                        '        dst = flow["target"]\n'
                        '        proto = flow["protocol"]\n'
                        '        cross = flow["crosses_trust_boundary"]\n'
                        '\n'
                        '        if cross and proto == "HTTP":\n'
                        '            threats.append({\n'
                        '                "flow": f"{src} -> {dst}",\n'
                        '                "category": "TAMPERING / INFO_DISCLOSURE",\n'
                        '                "threat": "Unencrypted HTTP traversing trust boundary allows cleartext eavesdropping and payload tampering.",\n'
                        '                "severity": "CRITICAL",\n'
                        '                "mitigation": "Mandate mutual TLS (mTLS) with Certificate Authority Service."\n'
                        '            })\n'
                        '\n'
                        '    print(f"Discovered {len(threats)} STRIDE Threat Vectors:\\n")\n'
                        '    for t in threats:\n'
                        '        print(f"[{t[\'category\']}] Severity: {t[\'severity\']}")\n'
                        '        print(f"  Threat: {t[\'threat\']}")\n'
                        '        print(f"  Mitigation: {t[\'mitigation\']}\\n")\n'
                        '\n'
                        '    report = {\n'
                        '        "system_name": arch["system_name"],\n'
                        '        "threat_count": len(threats),\n'
                        '        "threat_register": threats\n'
                        '    }\n'
                        '\n'
                        '    with open("stride_threat_register.json", "w") as out:\n'
                        '        json.dump(report, out, indent=2)\n'
                        '    print("STRIDE evaluation completed. Saved stride_threat_register.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    evaluate_stride()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Run the STRIDE Evaluator and Inspect Threat Register\n'
                        'Execute the Python evaluation script and inspect the output to verify that spoofing and unencrypted trust boundary traversal threats are accurately cataloged:\n\n'
                        '```sh\n'
                        'python3 stride_evaluator.py\n'
                        'cat stride_threat_register.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python STRIDE evaluation engine that systematically parses cloud trust boundaries and maps actionable mitigations.',
                'verification': 'Review terminal output of <kbd>python3 stride_evaluator.py</kbd> confirming discovery of SPOOFING and TAMPERING threat vectors.',
                'trouble': 'If JSON parsing error occurs, verify syntax in `architecture_graph.json`.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/stride-lab</kbd>.',
                'file': 'day-113-stride-modeling.md'
            }
        },

        # TOPIC 4
        {
            'key': 'topic-04',
            'title': 'Penetration testing rules on GCP',
            'overview': (
                'Conducting penetration testing, red teaming, and adversary emulation exercises on Google Cloud requires strict '
                'adherence to Google’s Acceptable Use Policy and testing rules of engagement. While Google permits organizations to perform '
                'security assessments against their own cloud resources without prior notification, strict technical and operational '
                'boundaries govern what targets and techniques are legally and architecturally permissible.'
            ),
            'preview': (
                'A third-party red team executes an unthrottled volumetric stress test against a public Cloud Load Balancer, triggering '
                'network infrastructure rate limits and causing collateral outage for adjacent enterprise services.'
            ),
            'technical': (
                'Penetration testing governance on Google Cloud balances adversarial assessment with cloud infrastructure stability.\n\n'
                '### Permitted vs Prohibited Activities\n'
                'Google Cloud’s policy does **not** require pre-approval or advance notice to Google for performing security assessments '
                'against customer-owned resources, provided the testing adheres to the following rules:\n'
                '1. **Permitted Scope**:\n'
                '   - User-provisioned Compute Engine virtual machine instances.\n'
                '   - Customer application endpoints running on Google Kubernetes Engine (GKE), Cloud Run, and App Engine.\n'
                '   - Customer Cloud Functions and Cloud Storage buckets.\n'
                '   - Application-layer vulnerability scanning, SQL injection testing, XSS testing, and API authentication fuzzing.\n'
                '2. **Strictly Prohibited Scope**:\n'
                '   - **Denial of Service (DoS / DDoS)**: Launching volumetric attacks, SYN floods, UDP amplification, or stress tests designed to exhaust cloud network bandwidth or underlying Google edge infrastructure.\n'
                '   - **Physical Facilities**: Attempting physical security intrusion against Google data centers or offices.\n'
                '   - **Google Personnel**: Social engineering, phishing, or vishing attacks directed at Google employees or contractors.\n'
                '   - **Shared Multi-Tenant Infrastructure**: Attempting to breach or exploit underlying Google control plane components (Borg, underlying Spanner infrastructure, Andromeda SDN, or hypervisors).\n'
                '   - **Collateral Disruption**: Generating testing traffic that degrades service quality for other Google Cloud customers.\n\n'
                '### Rules of Engagement (RoE) Architectural Framework\n'
                'Prior to commencing any penetration test, enterprise security teams must establish a formal RoE document specifying:\n'
                '- **Source IP Whitelisting**: Designating the exact public IP ranges used by the penetration testing firm.\n'
                '- **Emergency Stop Procedure ("Kill Switch")**: Establishing a rapid out-of-band communication channel (e.g. dedicated bridge line) capable of halting testing within 60 seconds if unexpected production instability occurs.\n'
                '- **Testing Windows**: Restricting testing to designated maintenance or low-traffic hours.\n'
                '- **SOC De-confliction Protocol**: Notifying the SOC management team in advance to distinguish simulated attacks from real-world nation-state intrusions, or deliberately running a "purple team" exercise to measure detection latencies.'
            ),
            'questions': [
                'Does Google Cloud require prior notification or formal permission before conducting a penetration test against customer-owned Compute Engine instances?',
                'Why are volumetric Denial of Service (DoS) tests strictly prohibited even when targeted exclusively at customer-owned IP addresses?',
                'What operational safeguards must be defined in a formal Rules of Engagement (RoE) artifact before initiating a red-team engagement?'
            ],
            'reference': 'https://docs.cloud.google.com/security-command-center/docs',
            'reference_label': 'Google Cloud Penetration Testing Policies and Guidelines',
            'scenario': {
                'symptom': 'External pen testing firm launches automated stress tool; regional network egress limits saturated; legitimate customer traffic dropped.',
                'impact': 'Production e-commerce storefront inaccessible for 35 minutes; Cloud Armor triggers automated threshold rate limiting.',
                'constraints': 'Penetration testing must never employ volumetric exhaustion techniques or exceed agreed bandwidth caps.',
                'evidence': (
                    'Cloud Monitoring network bandwidth spike and RoE violation:\n\n'
                    '```text\n'
                    'Egress Bandwidth: 48.5 Gbps (Threshold: 5.0 Gbps)\n'
                    'Dropped Packets: 82% on regional load balancer\n'
                    'Tool Fingerprint: Low Orbit Ion Cannon / High-Thread HTTP Flooder\n'
                    '```\n\n'
                    'Analysis: The external security vendor exceeded the agreed scope by launching volumetric denial-of-service testing '
                    'without rate throttling, violating both the signed RoE and the Google Cloud Acceptable Use Policy.'
                ),
                'diagnostic_steps': [
                    'Review Cloud Armor and Cloud Monitoring bandwidth metrics to identify the source IP addresses of the volumetric flood.',
                    'Check the signed Rules of Engagement (RoE) contract to confirm whether load testing or DoS was explicitly excluded.',
                    'Execute the emergency kill switch protocol to immediately revoke access for the testing firm’s source IPs.',
                    'Confirm that no adjacent tenant infrastructure or shared Google Cloud edge routers experienced degradation.'
                ],
                'root': 'The penetration testing firm deployed unthrottled volumetric stress testing tools in violation of Google Cloud policies and signed RoE constraints.',
                'fix': 'Immediately block testing IPs at Cloud Armor, enforce strict request rate caps in the RoE, and mandate technical pre-flight reviews of testing tools.',
                'verify': 'Resume testing using throttled, application-layer vulnerability scanners and verify bandwidth remains well within baseline operational limits.',
                'residual': 'High-volume web application vulnerability scanners can still trigger application-level database locks if concurrency is unconstrained.',
                'diagram': (
                    'Penetration tester executes unthrottled stress test against load balancer',
                    'Network traffic surges to 48 Gbps, violating Google Acceptable Use Policy',
                    'Cloud Armor rate limiters activate; legitimate customer traffic dropped',
                    'Activate RoE emergency kill switch and block tester source IPs at edge',
                    'Enforce application-layer rate limits; resume testing compliantly'
                )
            },
            'lab': {
                'name': 'Penetration Testing Scope & RoE Compliance Auditor',
                'goal': 'Implement a Python Rules of Engagement (RoE) auditor that validates proposed penetration testing scopes against Google Cloud acceptable use policies, detecting prohibited DoS techniques and unowned infrastructure.',
                'expected': 'A verified Python RoE validator that identifies policy violations and outputs formal authorization manifests.',
                'mode': 'Python script and CLI data modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/pentest-roe-lab</kbd>.',
                'steps': [
                    (
                        '#### Define Proposed Penetration Testing Plan\n'
                        'Create a JSON file specifying a proposed security testing engagement, including target assets, planned tools, and test methods:\n\n'
                        '```sh\n'
                        'mkdir -p ~/pentest-roe-lab && cd ~/pentest-roe-lab\n'
                        'cat <<\'EOF\' > proposed_pentest_plan.json\n'
                        '{\n'
                        '  "assessment_name": "Q4 Enterprise Security Assessment",\n'
                        '  "vendor": "RedTeam Specialists LLC",\n'
                        '  "testing_window": "2026-10-05 to 2026-10-12",\n'
                        '  "targets": [\n'
                        '    {\n'
                        '      "target_type": "CUSTOMER_COMPUTE_VM",\n'
                        '      "target_ip": "34.102.15.88",\n'
                        '      "owned_by_customer": true\n'
                        '    },\n'
                        '    {\n'
                        '      "target_type": "GOOGLE_MANAGED_SPANNER_BACKEND",\n'
                        '      "target_ip": "172.217.16.206",\n'
                        '      "owned_by_customer": false\n'
                        '    }\n'
                        '  ],\n'
                        '  "testing_methods": [\n'
                        '    "OWASP_TOP_10_WEB_SCAN",\n'
                        '    "IAM_PRIVILEGE_ESCALATION_TEST",\n'
                        '    "DISTRIBUTED_DENIAL_OF_SERVICE_STRESS_TEST"\n'
                        '  ]\n'
                        '}\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the RoE Compliance Validator\n'
                        'Write a Python script that evaluates the testing plan against Google Cloud policies, flagging prohibited DoS tests and unowned infrastructure targets:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > validate_pentest_roe.py\n'
                        'import json\n'
                        'import sys\n'
                        '\n'
                        'PROHIBITED_METHODS = {\n'
                        '    "DISTRIBUTED_DENIAL_OF_SERVICE_STRESS_TEST",\n'
                        '    "VOLUMETRIC_SYN_FLOOD",\n'
                        '    "PHYSICAL_DATACENTER_INTRUSION",\n'
                        '    "SOCIAL_ENGINEERING_GOOGLE_STAFF"\n'
                        '}\n'
                        '\n'
                        'def audit_roe():\n'
                        '    with open("proposed_pentest_plan.json", "r") as f:\n'
                        '        plan = json.load(f)\n'
                        '\n'
                        '    print(f"=== Auditing Pen Test RoE: {plan[\'assessment_name\']} ===\\n")\n'
                        '    violations = []\n'
                        '    approved_targets = []\n'
                        '\n'
                        '    # Audit Targets\n'
                        '    for target in plan["targets"]:\n'
                        '        tip = target["target_ip"]\n'
                        '        ttype = target["target_type"]\n'
                        '        owned = target["owned_by_customer"]\n'
                        '        \n'
                        '        if not owned:\n'
                        '            violations.append(f"ILLEGAL TARGET: {tip} ({ttype}) is Google-managed/unowned infrastructure.")\n'
                        '        else:\n'
                        '            approved_targets.append(tip)\n'
                        '\n'
                        '    # Audit Testing Methods\n'
                        '    for method in plan["testing_methods"]:\n'
                        '        if method in PROHIBITED_METHODS:\n'
                        '            violations.append(f"PROHIBITED METHOD: {method} violates Google Cloud Acceptable Use Policy.")\n'
                        '\n'
                        '    print("Audit Results:")\n'
                        '    if violations:\n'
                        '        print("STATUS: REJECTED - Policy Violations Detected:\\n")\n'
                        '        for v in violations:\n'
                        '            print(f"  [!] {v}")\n'
                        '        verdict = "REJECTED"\n'
                        '    else:\n'
                        '        print("STATUS: APPROVED - All scopes adhere to Google Cloud Pen Testing Policy.\\n")\n'
                        '        verdict = "APPROVED"\n'
                        '\n'
                        '    audit_result = {\n'
                        '        "assessment_name": plan["assessment_name"],\n'
                        '        "verdict": verdict,\n'
                        '        "violations_found": violations,\n'
                        '        "approved_targets": approved_targets\n'
                        '    }\n'
                        '\n'
                        '    with open("roe_audit_report.json", "w") as out:\n'
                        '        json.dump(audit_result, out, indent=2)\n'
                        '    print(f"\\nWrote roe_audit_report.json with verdict: {verdict}")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    audit_roe()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute the RoE Compliance Validator and Review Audit Output\n'
                        'Run the validator tool and inspect the resulting JSON audit report to confirm that DoS testing and unowned target scopes are intercepted:\n\n'
                        '```sh\n'
                        'python3 validate_pentest_roe.py\n'
                        'cat roe_audit_report.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python penetration testing auditor successfully detecting prohibited DoS methodologies and unowned cloud infrastructure targets.',
                'verification': 'Review terminal output of <kbd>python3 validate_pentest_roe.py</kbd> confirming verdict REJECTED due to prohibited DDoS and unowned Spanner target.',
                'trouble': 'If JSON file cannot be loaded, verify syntax of `proposed_pentest_plan.json`.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/pentest-roe-lab</kbd>.',
                'file': 'day-113-pentest-rules.md'
            }
        }
    ]
}
