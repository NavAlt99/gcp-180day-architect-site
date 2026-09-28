"""day_data_095.py — Exhaustive architecture data specification for Day 95.

Covers Central Observability and Audit Evidence:
1. Ops Agent on Compute Engine: unified Fluent Bit & OpenTelemetry collector architecture, guest-level metrics (RAM, disk IOPS), OS Policy automated fleet rollouts.
2. Centralized logging design: Organization and folder-level aggregated sinks with `--include-children`, centralized SIEM/SOC projects, IAM isolation, non-intercepting vs intercepting router behavior.
3. Cloud Audit Logs: Admin Activity (free, 400d, mandatory), Data Access (ADMIN_READ, DATA_READ, DATA_WRITE), System Event, Policy Denied (VPC Service Controls, IAM deny), tamper-resistant retention.
Follows PAGE_AUTHORING_CONTRACT.md with hands-on, verifiable exercises.
"""

DAY_NUM = 95

DATA = {
    "day": 95,
    "part1_intro": (
        "Day 95 establishes enterprise-scale observability governance and cryptographic security evidence across multi-project "
        "hierarchies. As organizations scale across hundreds of isolated Google Cloud projects, decentralized logging creates dangerous "
        "security blind spots, inconsistent retention compliance, and uncoordinated incident responses. Today's curriculum builds a unified "
        "central telemetry architecture using the Google Cloud Ops Agent for VM guest-level visibility, organization-level aggregated Log Router "
        "sinks with child inheritance, and deep audit log governance distinguishing Admin Activity, Data Access, System Events, and Policy Denied "
        "violations to satisfy SOC 2, HIPAA, and PCI-DSS compliance."
    ),
    "exit_summary": (
        "Engineered an enterprise Central Observability and Audit Evidence Architecture: deployed unified Ops Agent configuration blueprints with "
        "OS Config fleet automation; authored an Organization-level aggregated log sink with `--include-children` routing to a dedicated security vault; "
        "established a complete audit log retention and IAM matrix with BigQuery SQL detection queries pinpointing unauthorized IAM privilege escalation."
    ),
    "part2_intro": (
        "Enterprise observability separates operational telemetry (used by SREs for troubleshooting) from audit evidence (used by Security and Compliance). "
        "The sections below analyze the guest-level Ops Agent architecture, multi-tenant aggregated sink topologies, and Cloud Audit Log categorization."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Audit Log Category</th>
      <th>Trigger Mechanism &amp; Examples</th>
      <th>Default State &amp; Pricing</th>
      <th>Standard Retention</th>
      <th>Compliance &amp; Threat Detection Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Admin Activity</strong></td>
      <td>Resource creation, modification, deletion (e.g. `compute.instances.create`, `setIamPolicy`)</td>
      <td>Enabled permanently; Always Free of ingestion charge</td>
      <td>400 days default (immutable)</td>
      <td>Tracks who changed what infrastructure and when; primary source for detecting unauthorized IAM escalations</td>
    </tr>
    <tr>
      <td><strong>Data Access (ADMIN_READ)</strong></td>
      <td>Operations that read configuration or metadata (e.g. `cloudresourcemanager.projects.getIamPolicy`)</td>
      <td>Disabled by default (except BigQuery); billed at standard log ingestion rates</td>
      <td>30 days standard (extendable up to 3650 days)</td>
      <td>Detects unauthorized reconnaissance scanning and internal credential enumeration</td>
    </tr>
    <tr>
      <td><strong>Data Access (DATA_READ / WRITE)</strong></td>
      <td>Direct access to customer payload data (e.g. `storage.objects.get`, `spanner.databases.read`)</td>
      <td>Disabled by default; high volume; billed at standard log ingestion rates</td>
      <td>30 days standard (customizable)</td>
      <td>Proof of non-exfiltration for sensitive healthcare (HIPAA) or financial (PCI) records</td>
    </tr>
    <tr>
      <td><strong>System Event</strong></td>
      <td>Google-initiated administrative actions (e.g. Compute Engine live migration, automated OS patch)</td>
      <td>Enabled permanently; Always Free of charge</td>
      <td>400 days default</td>
      <td>Correlates application brownouts with cloud provider infrastructure maintenance</td>
    </tr>
    <tr>
      <td><strong>Policy Denied</strong></td>
      <td>Requests blocked by security policies (VPC Service Controls perimeters, IAM Deny policies)</td>
      <td>Enabled automatically; Always Free of charge</td>
      <td>30 days standard (customizable)</td>
      <td>Detects active perimeter egress exfiltration attempts and compromised service tokens</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Enterprise Centralized Logging & Audit Evidence Topology",
        "desc": "Hierarchical diagram showing multi-project application workloads, Ops Agents, organization-level aggregated sinks, and centralized security telemetry vaults.",
        "caption": "Figure 95.1: Multi-project aggregated log routing and centralized SIEM ingestion architecture with child project inheritance.",
        "nodes": [
            ("1. Multi-Project Workloads", "VM Ops Agent & App pods"),
            ("2. Organization Log Router", "Aggregated sink with --include-children"),
            ("3. Central Security Vault", "Restricted IAM project & Log Bucket"),
            ("4. SIEM & Audit Analytics", "BigQuery SQL & Splunk export"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Ops Agent on Compute Engine: Architecture, Metrics, and Fleet Automation",
            "overview": (
                "The Google Cloud Ops Agent is the primary unified telemetry agent for Compute Engine virtual machines, combining high-throughput "
                "Fluent Bit log forwarding with an OpenTelemetry-based metrics collector. While external hypervisor metrics can only observe "
                "host-level CPU and network packet counts, the Ops Agent operates inside the guest OS, capturing disk volume utilization, memory "
                "allocation breakdowns, systemd service journals, third-party application logs (Nginx, PostgreSQL), and custom process stats."
            ),
            "preview": (
                "Compute Engine metrics report 15% VM CPU usage while the guest operating system runs out of swap memory and terminates the primary database process. "
                "Deploying the Ops Agent provides true guest memory and disk queue depth visibility, preventing undetected out-of-memory kernel panics."
            ),
            "technical": (
                "### 1. Unified Ops Agent Subsystems\n"
                "- **Logging Subsystem (Fluent Bit):** Ingests structured and unstructured log files from Linux paths (`/var/log/syslog`, `/var/log/nginx/*.log`) "
                "or Windows Event Logs. Parses multiline stack traces, extracts timestamps, and enriches records with GCE metadata (zone, instance ID, labels) "
                "before streaming to Cloud Logging via the Logging API.\n"
                "- **Metrics Subsystem (OpenTelemetry Collector):** Scrapes guest kernel performance metrics every 60 seconds (CPU user/system/wait, "
                "memory used/free/cached/swap, disk read/write IOPS and time). Operates built-in receivers for over 40 enterprise applications "
                "(MySQL, Redis, Apache, Kafka) via local socket queries.\n\n"
                "### 2. Declarative Configuration Architecture (`config.yaml`)\n"
                "- The agent is configured via `/etc/google-cloud-ops-agent/config.yaml` using declarative pipelines:\n"
                "  - **Receivers:** Define where data originates (`files`, `systemd_journald`, `hostmetrics`, `prometheus`).\n"
                "  - **Processors:** Parse and transform data (JSON parsing, regex parsing, label dropping, field renaming).\n"
                "  - **Service Pipelines:** Connect receivers through processors to default Google Cloud outputs.\n\n"
                "### 3. Fleet-Wide Deployment Automation (VM Manager OS Policies)\n"
                "- Rather than running manual SSH installation scripts, enterprise architects enforce Ops Agent presence using **VM Manager OS Config Policies**.\n"
                "- An OS Policy assignment targeted at project or folder labels (`env: production`) automatically installs the agent on newly provisioned VMs, "
                "maintains the latest version, and restarts the daemon if halted."
            ),
            "questions": [
                "Why can hypervisor-level Compute Engine monitoring never measure guest operating system memory allocation or disk fill percentage accurately?",
                "How does the Ops Agent combine Fluent Bit and OpenTelemetry into a unified binary while maintaining low CPU and memory footprints?",
                "What role do VM Manager OS Config policies play in preventing telemetry blind spots in dynamic autoscaling instance groups?",
            ],
            "reference": "https://docs.cloud.google.com/monitoring/agent/ops-agent",
            "reference_label": "Google Cloud Ops Agent: Unified metrics and logging configuration and OS policy deployment",
            "scenario": {
                "symptom": (
                    "A critical stateful backend VM running on Compute Engine froze completely during customer peak hours. The Cloud Monitoring console "
                    "showed VM CPU utilization flat at 12% with normal network throughput right up until the instance became unresponsive."
                ),
                "constraints": (
                    "Must establish proactive alerting on RAM exhaustion and disk space exhaustion across 250 stateful Compute Engine instances."
                ),
                "evidence": (
                    "Console inspection revealed the VM lacked the Ops Agent. Serial port output logs showed Linux Out-Of-Memory (OOM) killer "
                    "invoked `oom_kill_process` on PostgreSQL because cache and buffer memory consumed 100% of physical RAM."
                ),
                "diagnostic_steps": [
                    "Inspect `agent.googleapis.com` metric availability in Metrics Explorer for the failing VM.",
                    "Review serial port output via `gcloud compute instances get-serial-port-output` to confirm OOM killer invocation.",
                    "Audit VM metadata to inspect installed daemon agents and OS Config policies.",
                ],
                "root": (
                    "Lack of guest-level telemetry: without the Ops Agent, Cloud Monitoring only receives hypervisor CPU ticks and cannot observe "
                    "guest RAM or swap exhaustion, leaving SREs completely blind to memory leaks."
                ),
                "fix": (
                    "Author a declarative `config.yaml` enabling hostmetrics and application receivers. Deploy a VM Manager OS Config Policy "
                    "ensuring automated Ops Agent installation and enforcement across all existing and future Compute Engine instances."
                ),
                "verify": (
                    "Verify `agent.googleapis.com/memory/percent_used` metrics appear in Cloud Monitoring and configure an alert policy firing at >85% RAM utilization."
                ),
                "residual": (
                    "The Ops Agent consumes approximately 50–100 MiB of guest RAM and 1–2% of a single vCPU core; on very small instances (e.g. `e2-micro`), "
                    "this overhead must be planned into memory budgeting."
                ),
                "diagram": (
                    "Hypervisor metrics report 12% CPU",
                    "Guest RAM quietly leaks to 100%",
                    "Kernel OOM killer terminates DB",
                    "Ops Agent deployed via OS Policy",
                    "Proactive guest RAM alert active"
                )
            },
            "lab": {
                "name": "Ops Agent Configuration Blueprint and OS Config Fleet Policy Synthesis",
                "goal": "Author a production Ops Agent declarative configuration manifest and an automated VM Manager OS Policy deployment script.",
                "expected": "A validated `config.yaml` with custom logging and metric pipelines, and an executable OS Policy assignment definition.",
                "mode": "tabletop analysis & YAML/JSON synthesis",
                "prereq": "Understanding of Linux systemd journals and Compute Engine VM Manager.",
                "preflight": "Review Ops Agent configuration syntax and OS Policy assignment parameters.",
                "steps": [
                    "Author the production Ops Agent declarative configuration file (`config.yaml`) with structured JSON parsing and application host metrics:\n\n```sh\ncat <<'EOF' > ops-agent-config.yaml\n# Production Google Cloud Ops Agent Configuration\nlogging:\n  receivers:\n    syslog_systemd:\n      type: systemd_journald\n    brightloaf_app:\n      type: files\n      include_paths:\n        - /var/log/brightloaf/*.log\n      record_log_file_path: true\n  processors:\n    parse_json:\n      type: parse_json\n      time_key: time\n      time_format: \"%Y-%m-%dT%H:%M:%SZ\"\n  service:\n    pipelines:\n      app_pipeline:\n        receivers: [brightloaf_app]\n        processors: [parse_json]\n      syslog_pipeline:\n        receivers: [syslog_systemd]\n\nmetrics:\n  receivers:\n    hostmetrics:\n      type: hostmetrics\n      collection_interval: 30s\n  service:\n    pipelines:\n      default_pipeline:\n        receivers: [hostmetrics]\nEOF\ncat ops-agent-config.yaml\n```",
                    "Author the VM Manager OS Policy Assignment JSON manifest ensuring automated fleet installation across all production VMs:\n\n```sh\ncat <<'EOF' > day-095-topic-01-ospolicy-agent.json\n{\n  \"osPolicyAssignmentId\": \"enforce-ops-agent-prod\",\n  \"description\": \"Enforce Google Cloud Ops Agent installation and running state on all prod VMs\",\n  \"osPolicies\": [\n    {\n      \"id\": \"ops-agent-policy\",\n      \"mode\": \"ENFORCEMENT\",\n      \"resourceGroups\": [\n        {\n          \"resources\": [\n            {\n              \"id\": \"install-package\",\n              \"pkg\": {\n                \"desiredState\": \"INSTALLED\",\n                \"apt\": {\n                  \"name\": \"google-cloud-ops-agent\"\n                }\n              }\n            },\n            {\n              \"id\": \"enable-service\",\n              \"exec\": {\n                \"validate\": {\n                  \"script\": \"systemctl is-active google-cloud-ops-agent\",\n                  \"interpreter\": \"SHELL\"\n                },\n                \"enforce\": {\n                  \"script\": \"systemctl enable --now google-cloud-ops-agent\",\n                  \"interpreter\": \"SHELL\"\n                }\n              }\n            }\n          ]\n        }\n      ]\n    }\n  ],\n  \"instanceFilter\": {\n    \"inclusionLabels\": [\n      {\n        \"labels\": {\n          \"environment\": \"production\"\n        }\n      }\n    ]\n  },\n  \"rollout\": {\n    \"disruptionBudget\": {\n      \"percent\": 20\n    },\n    \"minWaitDuration\": \"300s\"\n  }\n}\nEOF\ncat day-095-topic-01-ospolicy-agent.json\n```",
                    "Author an automated validation script verifying configuration syntax and policy parameters:\n\n```sh\ncat <<'EOF' > validate_ops_agent_config.py\n# Validation test for Ops Agent YAML and OS Policy JSON\nimport json\nimport yaml\n\nwith open(\"ops-agent-config.yaml\") as f:\n    agent_conf = yaml.safe_load(f)\nassert \"logging\" in agent_conf and \"metrics\" in agent_conf, \"Ops agent config missing core sections!\"\nassert \"syslog_systemd\" in agent_conf[\"logging\"][\"receivers\"], \"Missing systemd journal receiver!\"\n\nwith open(\"day-095-topic-01-ospolicy-agent.json\") as f:\n    osp = json.load(f)\nassert osp[\"osPolicies\"][0][\"mode\"] == \"ENFORCEMENT\", \"OS policy must be in ENFORCEMENT mode!\"\nassert osp[\"instanceFilter\"][\"inclusionLabels\"][0][\"labels\"][\"environment\"] == \"production\"\n\nprint(\"PASS: Ops Agent config and OS Policy Assignment mathematically validated.\")\nEOF\npython3 validate_ops_agent_config.py\n```",
                    "Review all output artifacts and confirm that the YAML configuration and OS Policy JSON pass programmatic assertions."
                ],
                "verification": "The Ops Agent config accurately specifies receivers and service pipelines, and the OS Policy Assignment defines bounded disruption budgets and enforcement scripts.",
                "trouble": "Ensure `time_key` and `time_format` in `parse_json` match the exact RFC 3339 timestamp emitted by the application logging library.",
                "cleanup": "Retain `ops-agent-config.yaml` and `day-095-topic-01-ospolicy-agent.json` as exit evidence artifacts.",
                "accept": "Completed Ops Agent configuration and verified OS Policy assignment manifest. File: `day-095-topic-01-ops-agent.md`.",
                "file": "day-095-topic-01-ops-agent.md"
            }
        },
        {
            "key": "topic-02",
            "title": "Centralized Logging Design Across Projects and Organization-Level Aggregated Sinks",
            "overview": (
                "In an enterprise Google Cloud environment with dozens or hundreds of projects, decentralizing log management introduces severe "
                "compliance vulnerabilities: individual project owners can delete security log buckets, disable audit sinks, or tamper with evidence. "
                "Centralized logging aggregates log records at the Organization or Folder level using **Aggregated Log Router Sinks** configured with "
                "`--include-children`. These sinks route all matching logs downstream into a dedicated, locked-down Security Telemetry Project, "
                "providing an immutable, centralized logging repository for Security Operations Centers (SOC) and compliance auditors."
            ),
            "preview": (
                "A rogue administrator with Project Owner permissions deletes local log buckets to hide malicious resource tampering. "
                "Organization-level aggregated sinks capture and lock audit logs in a centralized vault before local project administrators can touch them."
            ),
            "technical": (
                "### 1. Organization & Folder Aggregated Sinks (`--include-children`)\n"
                "- **Inheritance:** An aggregated sink created at the Organization level (`organizations/{ORG_ID}`) or Folder level (`folders/{FOLDER_ID}`) "
                "with the `--include-children` flag automatically intercepts logs emitted by every current and future project within that hierarchy.\n"
                "- **Non-Intercepting vs Intercepting Sinks:**\n"
                "  - **Non-Intercepting (Default):** The aggregated sink copies a copy of the log to the central security destination while leaving "
                "the original log record to continue flowing through local child project Log Routers for developer visibility.\n"
                "  - **Intercepting (`--intercept-children`):** The sink captures the log and stops it from flowing to child project log routers, "
                "used when sensitive audit logs must be hidden from local project teams.\n\n"
                "### 2. Dedicated Security Project & Central Log Bucket Topology\n"
                "- **Destination Project:** Sinks route logs to `logging.googleapis.com/projects/{SEC_PROJECT}/locations/{REGION}/buckets/{CENTRAL_BUCKET}`.\n"
                "- **Sink Writer Identity:** Creating an organization sink generates a unique service account (Writer Identity): "
                "`o123456789-999@gcp-sa-logging.iam.gserviceaccount.com`. This identity must be granted `roles/logging.bucketWriter` on the target bucket.\n"
                "- **IAM Segregation:** Local project developers have zero IAM permissions in the centralized security project. Even if a local project "
                "is compromised, attackers cannot modify, truncate, or delete historical log records in the central vault.\n\n"
                "### 3. Log Analytics and SIEM Export Topology\n"
                "- Centralized Log Buckets enable Log Analytics, allowing security teams to run SQL queries across logs from 500 projects simultaneously.\n"
                "- In parallel, a Pub/Sub sink forwards high-severity security events in real time to third-party SIEM platforms (Splunk, Chronicle, Microsoft Sentinel)."
            ),
            "questions": [
                "How does the `--include-children` flag eliminate telemetry onboarding friction when new projects are created in a folder?",
                "What security vulnerability arises if central logging relies on local project-level sinks rather than organization-level sinks?",
                "How does configuring a distinct Writer Identity per aggregated sink enforce the principle of least privilege in multi-tenant architectures?",
            ],
            "reference": "https://docs.cloud.google.com/logging/docs/routing/overview#aggregated_sinks",
            "reference_label": "Google Cloud Logging: Aggregated organization and folder sinks with child inheritance",
            "scenario": {
                "symptom": (
                    "During a forensic investigation into a suspected data breach, security analysts discovered that all Cloud Audit Logs in the affected "
                    "project had been deleted, and the project's local log retention had been altered from 365 days to 1 day."
                ),
                "constraints": (
                    "Must guarantee immutable log retention that cannot be deleted or bypassed by users holding `roles/owner` or `roles/editor` in child workload projects."
                ),
                "evidence": (
                    "The compromised project was utilizing standalone, project-level log sinks. The malicious actor used compromised Project Owner credentials "
                    "to execute `gcloud logging buckets delete _Default` and purge the local audit history."
                ),
                "diagnostic_steps": [
                    "Audit organization-level log sinks via `gcloud logging sinks list --organization={ORG_ID}`.",
                    "Review IAM policy bindings on the compromised project to determine how permissions were escalated.",
                    "Inspect the central security project's log intake to verify whether an immutable centralized sink existed.",
                ],
                "root": (
                    "Decentralized log architecture: relying on local project log buckets allowed local project administrators to destroy forensic "
                    "audit evidence upon compromising project-level credentials."
                ),
                "fix": (
                    "Deploy an organization-level aggregated sink with `--include-children` routing all audit and security logs directly to a dedicated, "
                    "IAM-isolated `brightloaf-security-vault` project. Apply Cloud Storage bucket lock or Log Bucket retention lock."
                ),
                "verify": (
                    "Simulate an administrative action in a child project; verify the event appears in the central security project's bucket within seconds. "
                    "Attempt to delete the central log bucket using child project owner credentials and confirm HTTP 403 Forbidden."
                ),
                "residual": (
                    "Aggregated sinks increase cross-project log ingestion volume; architects must pair aggregated sinks with strict inclusion filters "
                    "to avoid centralizing low-value debug noise."
                ),
                "diagram": (
                    "Compromised local project owner",
                    "Deletes local log bucket",
                    "Forensic audit trail lost",
                    "Organization aggregated sink deployed",
                    "Immutable audit logs secured in vault"
                )
            },
            "lab": {
                "name": "Organization Aggregated Log Sink and Central Security Vault Architecture",
                "goal": "Author an organization-level aggregated sink specification and verify IAM writer identity permissions and log routing.",
                "expected": "A complete gcloud deployment script for an organization aggregated sink with verified IAM bindings and architecture diagram.",
                "mode": "tabletop analysis & shell synthesis",
                "prereq": "Understanding of Google Cloud Resource Manager hierarchies and Log Router sinks.",
                "preflight": "Review organization-level gcloud logging commands and IAM role bindings.",
                "steps": [
                    "Author the production shell script deploying an organization-level aggregated log sink with child inheritance:\n\n```sh\ncat <<'EOF' > deploy_org_aggregated_sink.sh\n#!/usr/bin/env bash\nset -euo pipefail\n\n# Enterprise Centralized Telemetry Sink Deployment\nORG_ID=\"123456789012\"\nSEC_PROJECT=\"brightloaf-sec-telemetry\"\nCENTRAL_BUCKET=\"org-audit-vault-central\"\nLOCATION=\"us-central1\"\nSINK_NAME=\"sk-org-aggregated-audit-sink\"\n\nFILTER='logName:\"logs/cloudaudit.googleapis.com\" OR severity >= WARNING'\n\necho \"=== 1. Creating Organization Aggregated Log Sink ===\"\n# Note: --include-children ensures all current and future projects inherit this sink\ncat <<COMMAND\ngcloud logging sinks create \"$SINK_NAME\" \\\n    \"logging.googleapis.com/projects/$SEC_PROJECT/locations/$LOCATION/buckets/$CENTRAL_BUCKET\" \\\n    --organization=\"$ORG_ID\" \\\n    --include-children \\\n    --log-filter=\"$FILTER\" \\\n    --description=\"Centralized compliance sink for audit and warning logs across all child projects\"\nCOMMAND\n\necho \"=== 2. Granting Writer Identity IAM Permissions ===\"\n# Extract generated writer identity service account\nWRITER_IDENTITY=\"serviceAccount:o${ORG_ID}-sink-${SINK_NAME}@gcp-sa-logging.iam.gserviceaccount.com\"\n\ncat <<COMMAND\ngcloud logging buckets add-iam-policy-binding \"$CENTRAL_BUCKET\" \\\n    --project=\"$SEC_PROJECT\" \\\n    --location=\"$LOCATION\" \\\n    --member=\"$WRITER_IDENTITY\" \\\n    --role=\"roles/logging.bucketWriter\"\nCOMMAND\n\necho \"=== 3. Verification: Audit Log Query ===\"\ncat <<COMMAND\ngcloud logging read 'logName:\"logs/cloudaudit.googleapis.com%2Factivity\"' \\\n    --project=\"$SEC_PROJECT\" \\\n    --bucket=\"$CENTRAL_BUCKET\" \\\n    --location=\"$LOCATION\" \\\n    --limit=5\nCOMMAND\nEOF\nchmod +x deploy_org_aggregated_sink.sh\n./deploy_org_aggregated_sink.sh\n```",
                    "Author an automated Python simulation verifying that child project events are routed while unauthorized local tampering is blocked:\n\n```sh\ncat <<'EOF' > test_aggregated_sink_isolation.py\n# Simulation of Centralized Log Bucket IAM Isolation\n\nclass IAMAuthorizer:\n    def __init__(self):\n        self.roles = {\n            \"local_project_owner\": [\"projects/child-app/compute.admin\", \"projects/child-app/logging.admin\"],\n            \"security_admin\": [\"projects/sec-vault/logging.admin\", \"projects/sec-vault/logging.viewer\"],\n            \"org_sink_writer\": [\"projects/sec-vault/logging.bucketWriter\"]\n        }\n    \n    def check_permission(self, identity, target_resource, permission):\n        user_perms = self.roles.get(identity, [])\n        required = f\"{target_resource}/{permission}\"\n        return required in user_perms\n\nauth = IAMAuthorizer()\n\n# Scenario 1: Local project owner attempts to delete central security vault log bucket\ncan_delete_central = auth.check_permission(\"local_project_owner\", \"projects/sec-vault\", \"logging.admin\")\nprint(f\"Local Project Owner can modify Central Vault: {can_delete_central}\")\nassert not can_delete_central, \"SECURITY BREACH: Local owner should not have access to central vault!\"\n\n# Scenario 2: Aggregated sink writer identity writes audit log to central vault\ncan_write = auth.check_permission(\"org_sink_writer\", \"projects/sec-vault\", \"logging.bucketWriter\")\nprint(f\"Org Sink Writer can write to Central Vault:      {can_write}\")\nassert can_write, \"FAILURE: Sink writer identity must possess bucketWriter role!\"\n\nprint(\"PASS: Aggregated sink IAM boundary and isolation mathematically verified.\")\nEOF\npython3 test_aggregated_sink_isolation.py\n```",
                    "Review all output artifacts and confirm that the shell deployment script and Python IAM isolation tests run cleanly."
                ],
                "verification": "The shell script includes `--include-children` and assigns `roles/logging.bucketWriter`, and the Python isolation test proves local project owners cannot tamper with central vault buckets.",
                "trouble": "Ensure the central bucket already exists with Log Analytics enabled before creating the organization sink to prevent dead-letter sink drops.",
                "cleanup": "Retain `deploy_org_aggregated_sink.sh` as an exit evidence artifact.",
                "accept": "Completed aggregated organization sink script and verified IAM isolation test. File: `day-095-topic-02-aggregated-sinks.md`.",
                "file": "day-095-topic-02-aggregated-sinks.md"
            }
        },
        {
            "key": "topic-03",
            "title": "Cloud Audit Log Types: Admin Activity, Data Access, System Events, and Policy Denied",
            "overview": (
                "Google Cloud Audit Logs answer the fundamental forensic question: 'Who did what, where, and when?' Across the platform, audit events "
                "are divided into five distinct types: Admin Activity (mandatory and free), Data Access (ADMIN_READ, DATA_READ, DATA_WRITE; high-volume and "
                "billable), System Event (Google automated actions), and Policy Denied (security rule violations). Understanding their ingestion "
                "mechanics, default states, and analytical SQL signatures is vital for detecting privilege escalation, credential theft, and compliance drift."
            ),
            "preview": (
                "An attacker obtains stolen service account credentials and elevates their IAM permissions before downloading a customer database. "
                "Admin Activity audit logs provide undeniable cryptographic proof of the exact authorization change and source IP address."
            ),
            "technical": (
                "### 1. In-Depth Analysis of the Five Audit Log Streams\n"
                "- **Admin Activity Logs (`cloudaudit.googleapis.com/activity`):**\n"
                "  - Records calls that alter GCP resource configuration or metadata (e.g. `SetIamPolicy`, `CreateBucket`, `InsertInstance`).\n"
                "  - **State:** Enabled by default on all services; cannot be disabled by any user or organization policy.\n"
                "  - **Retention & Billing:** Retained for 400 days in the `_Required` bucket; 100% free of ingestion and storage charges.\n"
                "- **Data Access Logs (`cloudaudit.googleapis.com/data_access`):**\n"
                "  - Divided into three sub-types: `ADMIN_READ` (reading metadata/IAM), `DATA_READ` (reading user data like GCS objects), "
                "and `DATA_WRITE` (modifying user data like Cloud Spanner records).\n"
                "  - **State:** Disabled by default (except BigQuery Data Access, which is always enabled).\n"
                "  - **Billing:** Billed at standard log ingestion rates; turning on `DATA_READ` on high-throughput Cloud Storage buckets can generate "
                "millions of events per hour and massive bills.\n"
                "- **System Event Logs (`cloudaudit.googleapis.com/system_event`):**\n"
                "  - Records automated platform events executed by Google infrastructure (e.g., GCE live migration during hardware servicing).\n"
                "  - **State:** Always on; 400 days retention; free of charge.\n"
                "- **Policy Denied Logs (`cloudaudit.googleapis.com/policy`):**\n"
                "  - Emitted whenever a security policy denies an API call (e.g. VPC Service Controls boundary violation, IAM Deny rule).\n"
                "  - Essential for identifying data exfiltration attempts and misconfigured service accounts.\n\n"
                "### 2. Forensic Log Payload Anatomy\n"
                "- Audit logs are structured in `protoPayload` conforming to `google.cloud.audit.AuditLog`:\n"
                "  - `authenticationInfo.principalEmail`: Identity of the actor (user or service account).\n"
                "  - `requestMetadata.callerIp`: Public IP address where the API request originated.\n"
                "  - `methodName`: The exact API RPC invoked (e.g. `google.iam.admin.v1.CreateServiceAccountKey`).\n"
                "  - `authorizationInfo`: Permissions checked, resource evaluated, and granted status.\n"
                "  - `serviceData` / `request`: The serialized API request parameters submitted by the caller."
            ),
            "questions": [
                "Why are Admin Activity audit logs enabled permanently by default and retained for 400 days without cost to the customer?",
                "What architectural risks and costs must be evaluated before enabling Data Access `DATA_READ` logging on high-traffic storage buckets?",
                "How do Policy Denied audit logs distinguish between an unintentional network misconfiguration and an active malicious data exfiltration attempt?",
            ],
            "reference": "https://docs.cloud.google.com/logging/docs/audit",
            "reference_label": "Google Cloud Audit Logs: Architecture, types, retention periods, and BigQuery forensic querying",
            "scenario": {
                "symptom": (
                    "A junior developer's compromised laptop credentials were used at 02:30 UTC on a Sunday to grant the external account "
                    "`attacker@external-evil.com` the `roles/resourcemanager.organizationAdmin` role across the entire Google Cloud organization."
                ),
                "constraints": (
                    "Must identify the compromised identity, source IP, affected resource, and exact timestamp within 15 minutes to revoke access and isolate compromised keys."
                ),
                "evidence": (
                    "Security Operations executed an automated BigQuery Log Analytics query over Admin Activity logs matching `methodName = 'SetIamPolicy'`, "
                    "instantly isolating the change event, caller IP, and full IAM policy delta."
                ),
                "diagnostic_steps": [
                    "Query Admin Activity logs for `methodName = 'google.iam.admin.v1.SetIamPolicy'` or `SetOrgPolicy`.",
                    "Extract `authenticationInfo.principalEmail` and `requestMetadata.callerIp`.",
                    "Inspect the `request.policy.bindings` payload to compare before-and-after role assignments.",
                ],
                "root": (
                    "Compromised developer credentials: an active session token was used to execute an unauthorized IAM policy update granting organization-level administrative access."
                ),
                "fix": (
                    "Immediately revoke the unauthorized IAM binding via `gcloud organizations remove-iam-policy-binding`. Revoke the developer's session credentials "
                    "and disable the affected user account. Deploy a Cloud Monitoring real-time alert on high-risk IAM mutation methods."
                ),
                "verify": (
                    "Run the forensic SQL query and verify the removal of the malicious binding is logged with a corresponding Admin Activity event. "
                    "Confirm the external account has 0 active bindings."
                ),
                "residual": (
                    "Admin Activity logs prove that an IAM binding was granted, but determining what actions the attacker performed during the window "
                    "requires cross-correlating with Data Access logs, which must be enabled beforehand."
                ),
                "diagram": (
                    "Compromised developer session",
                    "Unauthorized SetIamPolicy call",
                    "External attacker granted Org Admin",
                    "Admin Activity log captures caller IP",
                    "Binding revoked & credentials purged"
                )
            },
            "lab": {
                "name": "Audit Log Forensics and BigQuery IAM Mutation Detection Synthesis",
                "goal": "Author a production BigQuery Log Analytics forensic query detecting unauthorized IAM policy mutations and build an automated test script.",
                "expected": "A validated BigQuery SQL query extracting caller IP and IAM deltas, and an executable Python test script validating forensic detection.",
                "mode": "tabletop analysis & SQL/Python execution",
                "prereq": "Understanding of Cloud Audit Logs and BigQuery SQL.",
                "preflight": "Review google.cloud.audit.AuditLog schema and BigQuery JSON functions.",
                "steps": [
                    "Author the production BigQuery forensic detection query (`detect_iam_privilege_escalation.sql`) identifying unauthorized IAM role grants:\n\n```sh\ncat <<'EOF' > detect_iam_privilege_escalation.sql\n-- Forensic detection query: Identifies high-risk IAM privilege escalations and unauthorized SetIamPolicy calls\nSELECT\n  timestamp,\n  protoPayload.authenticationInfo.principalEmail AS actor,\n  protoPayload.requestMetadata.callerIp AS source_ip,\n  protoPayload.serviceName AS target_service,\n  protoPayload.methodName AS api_method,\n  protoPayload.resourceName AS affected_resource,\n  binding.role AS granted_role,\n  member AS granted_principal\nFROM\n  `brightloaf-sec-telemetry.us_central1.org_audit_vault_central._AllLogs`,\n  UNNEST(JSON_EXTRACT_ARRAY(protoPayload.serviceData.policyDelta.bindingDeltas)) AS delta_json,\n  UNNEST([STRUCT(\n    JSON_VALUE(delta_json, '$.role') AS role,\n    JSON_VALUE(delta_json, '$.member') AS member,\n    JSON_VALUE(delta_json, '$.action') AS action\n  )]) AS binding\nWHERE\n  timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)\n  AND logName LIKE '%cloudaudit.googleapis.com%2Factivity'\n  AND protoPayload.methodName LIKE '%.SetIamPolicy%'\n  AND binding.action = 'ADD'\n  AND binding.role IN (\n    'roles/owner',\n    'roles/editor',\n    'roles/resourcemanager.organizationAdmin',\n    'roles/iam.securityAdmin',\n    'roles/resourcemanager.folderAdmin'\n  )\nORDER BY\n  timestamp DESC\nLIMIT 50;\nEOF\ncat detect_iam_privilege_escalation.sql\n```",
                    "Author an executable Python script simulating an audit event stream and validating the forensic detection parser:\n\n```sh\ncat <<'EOF' > test_audit_forensics.py\n# Simulation of Cloud Audit Log Forensic Analysis\nimport json\nimport datetime\n\nsynthetic_audit_event = {\n    \"protoPayload\": {\n        \"@type\": \"type.googleapis.com/google.cloud.audit.AuditLog\",\n        \"serviceName\": \"cloudresourcemanager.googleapis.com\",\n        \"methodName\": \"SetIamPolicy\",\n        \"resourceName\": \"organizations/123456789012\",\n        \"authenticationInfo\": {\n            \"principalEmail\": \"compromised-dev@brightloaf.com\"\n        },\n        \"requestMetadata\": {\n            \"callerIp\": \"203.0.113.88\"\n        },\n        \"serviceData\": {\n            \"policyDelta\": {\n                \"bindingDeltas\": [\n                    {\n                        \"action\": \"ADD\",\n                        \"role\": \"roles/resourcemanager.organizationAdmin\",\n                        \"member\": \"user:attacker@external-evil.com\"\n                    }\n                ]\n            }\n        }\n    },\n    \"timestamp\": datetime.datetime.now(datetime.timezone.utc).isoformat(),\n    \"logName\": \"projects/sec-vault/logs/cloudaudit.googleapis.com%2Factivity\"\n}\n\ndef forensic_detector(event):\n    payload = event.get(\"protoPayload\", {})\n    method = payload.get(\"methodName\", \"\")\n    actor = payload.get(\"authenticationInfo\", {}).get(\"principalEmail\", \"\")\n    caller_ip = payload.get(\"requestMetadata\", {}).get(\"callerIp\", \"\")\n    \n    alerts = []\n    if \"SetIamPolicy\" in method:\n        deltas = payload.get(\"serviceData\", {}).get(\"policyDelta\", {}).get(\"bindingDeltas\", [])\n        for d in deltas:\n            if d.get(\"action\") == \"ADD\" and \"Admin\" in d.get(\"role\", \"\"):\n                alerts.append({\n                    \"severity\": \"CRITICAL\",\n                    \"actor\": actor,\n                    \"source_ip\": caller_ip,\n                    \"granted_role\": d.get(\"role\"),\n                    \"granted_to\": d.get(\"member\")\n                })\n    return alerts\n\ndetected = forensic_detector(synthetic_audit_event)\nprint(\"=== FORENSIC DETECTION RESULT ===\")\nprint(json.dumps(detected, indent=2))\n\nassert len(detected) == 1, \"Failed to detect high-risk IAM privilege escalation!\"\nassert detected[0][\"actor\"] == \"compromised-dev@brightloaf.com\"\nassert detected[0][\"granted_to\"] == \"user:attacker@external-evil.com\"\nprint(\"\nPASS: Audit log forensic detection logic validated successfully!\")\nEOF\npython3 test_audit_forensics.py\n```",
                    "Author the telemetry ownership and retention plan fulfilling Day 95 exit evidence:\n\n```sh\ncat <<'EOF' > day-095-topic-03-telemetry-plan.md\n# Day 95: Enterprise Telemetry Ownership & Retention Governance Plan\n\n## 1. Telemetry Stream Ownership RACI Matrix\n| Telemetry Stream | Responsible Owner | Storage Location | Default Retention | Extended Compliance Hold |\n| :--- | :--- | :--- | :--- | :--- |\n| **Admin Activity Audit** | InfoSec / SOC | Central Security Vault (`_Required`) | 400 Days (Free) | 7 Years (Cloud Storage WORM) |\n| **Data Access Audit** | Compliance / Database SRE | Regional Log Bucket (`data-audit`) | 30 Days | 365 Days (BigQuery Linked) |\n| **Policy Denied Audit** | Security Architecture | Central Security Vault (`policy-denied`)| 90 Days | 365 Days |\n| **Ops Agent VM Logs** | Application Engineering Teams | Local Project Default Bucket | 30 Days | None (Routine debug) |\n| **OpenTelemetry Traces**| Observability Platform Team | Cloud Trace Global Store | 30 Days | None (Tail-sampled errors only) |\n\n## 2. Authorization Change Forensic Query Verification\n- **Target Dataset:** `brightloaf-sec-telemetry.us_central1.org_audit_vault_central._AllLogs`\n- **Query Identifier:** `detect_iam_privilege_escalation.sql`\n- **Trigger Alert:** Cloud Monitoring Alert Policy firing on any `ADD` binding with `roles/*Admin` executed outside corporate VPN CIDR blocks.\nEOF\ncat day-095-topic-03-telemetry-plan.md\n```",
                    "Review all output artifacts and confirm that the BigQuery SQL query, Python forensic parser, and telemetry governance plan fulfill Day 95 Exit evidence."
                ],
                "verification": "The BigQuery query accurately unnests policy binding deltas and the Python forensic test verifies the detection of unauthorized privilege escalation.",
                "trouble": "Ensure BigQuery SQL uses `JSON_EXTRACT_ARRAY` and `UNNEST` when evaluating `serviceData.policyDelta.bindingDeltas` to avoid scalar unnest syntax errors.",
                "cleanup": "Retain `detect_iam_privilege_escalation.sql` and `day-095-topic-03-telemetry-plan.md` as exit evidence artifacts.",
                "accept": "Completed forensic detection query and verified telemetry ownership/retention plan. File: `day-095-topic-03-audit-forensics.md`.",
                "file": "day-095-topic-03-audit-forensics.md"
            }
        }
    ]
}
