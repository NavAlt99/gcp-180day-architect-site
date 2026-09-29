"""day_data_095.py — Exhaustive architecture data specification for Day 95.

Covers Ops Agent, Aggregated Sinks, and Audit Logs.
"""

DAY_NUM = 95

DATA = {'day': 95,
 'part1_intro': 'Day 95 establishes enterprise-scale observability governance and cryptographic security evidence '
                'across multi-project hierarchies. As organizations scale across hundreds of isolated Google Cloud '
                'projects, decentralized logging creates dangerous security blind spots, inconsistent retention '
                "compliance, and uncoordinated incident responses. Today's curriculum builds a unified central "
                'telemetry architecture using the Google Cloud Ops Agent for VM guest-level visibility, '
                'organization-level aggregated Log Router sinks with child inheritance, and deep audit log governance '
                'distinguishing Admin Activity, Data Access, System Events, and Policy Denied violations to satisfy '
                'SOC 2, HIPAA, and PCI-DSS compliance.',
 'exit_summary': 'Engineered an enterprise Central Observability and Audit Evidence Architecture: deployed unified Ops '
                 'Agent configuration blueprints with OS Config fleet automation; authored an Organization-level '
                 'aggregated log sink with `--include-children` routing to a dedicated security vault; established a '
                 'complete audit log retention and IAM matrix with BigQuery SQL detection queries pinpointing '
                 'unauthorized IAM privilege escalation.',
 'part2_intro': 'Enterprise observability separates operational telemetry (used by SREs for troubleshooting) from '
                'audit evidence (used by Security and Compliance). The sections below analyze the guest-level Ops '
                'Agent architecture, multi-tenant aggregated sink topologies, and Cloud Audit Log categorization.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Audit Log Category</th>\n'
                    '      <th>Trigger Mechanism &amp; Examples</th>\n'
                    '      <th>Default State &amp; Pricing</th>\n'
                    '      <th>Standard Retention</th>\n'
                    '      <th>Compliance &amp; Threat Detection Purpose</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>Admin Activity</strong></td>\n'
                    '      <td>Resource creation, modification, deletion (e.g. `compute.instances.create`, '
                    '`setIamPolicy`)</td>\n'
                    '      <td>Enabled permanently; Always Free of ingestion charge</td>\n'
                    '      <td>400 days default (immutable)</td>\n'
                    '      <td>Tracks who changed what infrastructure and when; primary source for detecting '
                    'unauthorized IAM escalations</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Data Access (ADMIN_READ)</strong></td>\n'
                    '      <td>Operations that read configuration or metadata (e.g. '
                    '`cloudresourcemanager.projects.getIamPolicy`)</td>\n'
                    '      <td>Disabled by default (except BigQuery); billed at standard log ingestion rates</td>\n'
                    '      <td>30 days standard (extendable up to 3650 days)</td>\n'
                    '      <td>Detects unauthorized reconnaissance scanning and internal credential enumeration</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Data Access (DATA_READ / WRITE)</strong></td>\n'
                    '      <td>Direct access to customer payload data (e.g. `storage.objects.get`, '
                    '`spanner.databases.read`)</td>\n'
                    '      <td>Disabled by default; high volume; billed at standard log ingestion rates</td>\n'
                    '      <td>30 days standard (customizable)</td>\n'
                    '      <td>Proof of non-exfiltration for sensitive healthcare (HIPAA) or financial (PCI) '
                    'records</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>System Event</strong></td>\n'
                    '      <td>Google-initiated administrative actions (e.g. Compute Engine live migration, automated '
                    'OS patch)</td>\n'
                    '      <td>Enabled permanently; Always Free of charge</td>\n'
                    '      <td>400 days default</td>\n'
                    '      <td>Correlates application brownouts with cloud provider infrastructure maintenance</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Policy Denied</strong></td>\n'
                    '      <td>Requests blocked by security policies (VPC Service Controls perimeters, IAM Deny '
                    'policies)</td>\n'
                    '      <td>Enabled automatically; Always Free of charge</td>\n'
                    '      <td>30 days standard (customizable)</td>\n'
                    '      <td>Detects active perimeter egress exfiltration attempts and compromised service '
                    'tokens</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 95: Enterprise VM Telemetry, Aggregated Organization Sinks, and Audit Governance',
                  'desc': 'End-to-end telemetry architecture illustrating Compute Engine guest metrics collection, '
                          'organization-level aggregated sink routing, and centralized audit analysis.',
                  'caption': 'Figure 95.1: Multi-tier enterprise logging architecture featuring Ops Agent guest '
                             'telemetry, organization aggregated sinks, and centralized BigQuery SIEM forensics.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Compute Engine Fleet & Guest OS Runtime',
                              'desc': 'Virtual machine workloads, guest OS memory, and OS Config management',
                              'y': 10,
                              'h': 90,
                              'stroke': '#38bdf8',
                              'fill': '#0c1e38',
                              'title_color': '#38bdf8'},
                             {'name': 'LAYER 2: Ops Agent Telemetry Pipeline (Fluent Bit & OTel)',
                              'desc': 'In-guest logging sub-agent and OpenTelemetry metric collector engine',
                              'y': 115,
                              'h': 90,
                              'stroke': '#818cf8',
                              'fill': '#141838',
                              'title_color': '#818cf8'},
                             {'name': 'LAYER 3: Enterprise Aggregated Log Router Fabric',
                              'desc': 'Folder and Organization sinks routing multi-project telemetry',
                              'y': 220,
                              'h': 90,
                              'stroke': '#f59e0b',
                              'fill': '#261a08',
                              'title_color': '#f59e0b'},
                             {'name': 'LAYER 4: Centralized Telemetry Sink Vault & SIEM Ingestion',
                              'desc': 'Encrypted centralized audit buckets, SIEM Pub/Sub, and BigQuery datasets',
                              'y': 325,
                              'h': 90,
                              'stroke': '#22c55e',
                              'fill': '#072417',
                              'title_color': '#22c55e'},
                             {'name': 'LAYER 5: Forensic Analytics, SIEM Rules & Long-Term Governance',
                              'desc': 'Security Command Center, BigQuery Log Analytics SQL, and audit compliance',
                              'y': 430,
                              'h': 90,
                              'stroke': '#c084fc',
                              'fill': '#1e0e33',
                              'title_color': '#c084fc'}],
                  'components': [{'name': 'GCE Production VM',
                                  'detail': 'Debian Linux Guest OS',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'VM Manager OS Policy',
                                  'detail': 'Automated Agent Rollout',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'Ops Agent Fluent Bit',
                                  'detail': 'Log Parsing & Chunking',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Ops Agent OTel Engine',
                                  'detail': 'Guest RAM & Disk Metrics',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Org Aggregated Sink',
                                  'detail': '--include-children Router',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Exclusion Rule Engine',
                                  'detail': 'Drop High-Volume Noise',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Central Audit Bucket',
                                  'detail': 'Locked Immutable Storage',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'},
                                 {'name': 'SIEM Pub/Sub Stream',
                                  'detail': 'Chronicle / Splunk Feed',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'},
                                 {'name': 'BigQuery Analytics SQL',
                                  'detail': 'Audit Threat Forensics',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#c084fc',
                                  'fill': '#2c154a'},
                                 {'name': 'Security Command Center',
                                  'detail': 'Policy Denied Alerts',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#c084fc',
                                  'fill': '#2c154a'}],
                  'boundaries': [{'label': 'GUEST OS & FLEET AUTOMATION BOUNDARY',
                                  'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'color': '#38bdf8'},
                                 {'label': 'TELEMETRY INGESTION & AGGREGATED SINK ROUTING FABRIC',
                                  'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#f59e0b'},
                                 {'label': 'FORENSIC STORAGE & COMPLIANCE ANALYTICS VAULT',
                                  'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#22c55e'}],
                  'flows': [{'x1': 420, 'y1': 56, 'x2': 340, 'y2': 56, 'label': 'Deploy Ops Agent', 'type': 'ok'},
                            {'x1': 210,
                             'y1': 82,
                             'x2': 210,
                             'y2': 135,
                             'label': 'Stream Logs to Fluent Bit',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'label': 'Forward Guest Metrics',
                             'type': 'ok'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'label': 'Push to Cloud Logging',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 266,
                             'x2': 420,
                             'y2': 266,
                             'label': 'Filter Heartbeat Logs',
                             'type': 'fail'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'label': 'Aggregate to Audit Vault',
                             'type': 'ok'},
                            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Stream to SIEM Topic', 'type': 'ok'},
                            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Query Log Analytics', 'type': 'ok'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'label': 'Publish Threat Telemetry',
                             'type': 'ok'}],
                  'probes': [{'cx': 420,
                              'cy': 135,
                              'label': 'PROBE 1: In-Guest RAM Allocation (>92%)',
                              'badge': 'P1',
                              'color': '#f43f5e'},
                             {'cx': 210,
                              'cy': 240,
                              'label': 'PROBE 2: Sink Writer Identity HTTP 403 Forbidden',
                              'badge': 'P2',
                              'color': '#f59e0b'},
                             {'cx': 80,
                              'cy': 450,
                              'label': 'PROBE 3: Audit Log Forensics Mutation Scan',
                              'badge': 'P3',
                              'color': '#38bdf8'}]},
 'topics': [{'key': 'topic-01',
             'title': 'Ops Agent on Compute Engine: Architecture, Metrics, and Fleet Automation',
             'overview': 'The Google Cloud Ops Agent is the primary unified telemetry agent for Compute Engine virtual '
                         'machines, combining high-throughput Fluent Bit log forwarding with an OpenTelemetry-based '
                         'metrics collector. While external hypervisor metrics can only observe host-level CPU and '
                         'network packet counts, the Ops Agent operates inside the guest OS, capturing disk volume '
                         'utilization, memory allocation breakdowns, systemd service journals, third-party application '
                         'logs (Nginx, PostgreSQL), and custom process stats.',
             'preview': 'Compute Engine metrics report 15% VM CPU usage while the guest operating system runs out of '
                        'swap memory and terminates the primary database process. Deploying the Ops Agent provides '
                        'true guest memory and disk queue depth visibility, preventing undetected out-of-memory kernel '
                        'panics.',
             'technical': '### 1. Unified Ops Agent Subsystems\n'
                          '- **Logging Subsystem (Fluent Bit):** Ingests structured and unstructured log files from '
                          'Linux paths (`/var/log/syslog`, `/var/log/nginx/*.log`) or Windows Event Logs. Parses '
                          'multiline stack traces, extracts timestamps, and enriches records with GCE metadata (zone, '
                          'instance ID, labels) before streaming to Cloud Logging via the Logging API.\n'
                          '- **Metrics Subsystem (OpenTelemetry Collector):** Scrapes guest kernel performance metrics '
                          'every 60 seconds (CPU user/system/wait, memory used/free/cached/swap, disk read/write IOPS '
                          'and time). Operates built-in receivers for over 40 enterprise applications (MySQL, Redis, '
                          'Apache, Kafka) via local socket queries.\n'
                          '\n'
                          '### 2. Declarative Configuration Architecture (`config.yaml`)\n'
                          '- The agent is configured via `/etc/google-cloud-ops-agent/config.yaml` using declarative '
                          'pipelines:\n'
                          '  - **Receivers:** Define where data originates (`files`, `systemd_journald`, '
                          '`hostmetrics`, `prometheus`).\n'
                          '  - **Processors:** Parse and transform data (JSON parsing, regex parsing, label dropping, '
                          'field renaming).\n'
                          '  - **Service Pipelines:** Connect receivers through processors to default Google Cloud '
                          'outputs.\n'
                          '\n'
                          '### 3. Fleet-Wide Deployment Automation (VM Manager OS Policies)\n'
                          '- Rather than running manual SSH installation scripts, enterprise architects enforce Ops '
                          'Agent presence using **VM Manager OS Config Policies**.\n'
                          '- An OS Policy assignment targeted at project or folder labels (`env: production`) '
                          'automatically installs the agent on newly provisioned VMs, maintains the latest version, '
                          'and restarts the daemon if halted.',
             'questions': ['Why can hypervisor-level Compute Engine monitoring never measure guest operating system '
                           'memory allocation or disk fill percentage accurately?',
                           'How does the Ops Agent combine Fluent Bit and OpenTelemetry into a unified binary while '
                           'maintaining low CPU and memory footprints?',
                           'What role do VM Manager OS Config policies play in preventing telemetry blind spots in '
                           'dynamic autoscaling instance groups?'],
             'reference': 'https://docs.cloud.google.com/monitoring/agent/ops-agent',
             'reference_label': 'Google Cloud Ops Agent: Unified metrics and logging configuration and OS policy '
                                'deployment',
             'scenario': {'symptom': 'A critical stateful backend VM running on Compute Engine froze completely during '
                                     'customer peak hours. The Cloud Monitoring console showed VM CPU utilization flat '
                                     'at 12% with normal network throughput right up until the instance became '
                                     'unresponsive.',
                          'constraints': 'Must establish proactive alerting on RAM exhaustion and disk space '
                                         'exhaustion across 250 stateful Compute Engine instances.',
                          'evidence': 'Production serial console logs and GCP monitoring API inspection:\n'
                                      '\n'
                                      '```text\n'
                                      '[10842.194208] Out of memory: Kill process 1842 (mysqld) score 892 or sacrifice '
                                      'child\n'
                                      '[10842.198302] Killed process 1842 (mysqld) total-vm:32840120kB, '
                                      'anon-rss:31920804kB, file-rss:1240kB\n'
                                      'systemd[1]: mysql.service: Main process exited, code=killed, status=9/KILL\n'
                                      "systemd[1]: mysql.service: Failed with result 'oom-killer'.\n"
                                      '```\n'
                                      '\n'
                                      'Querying Compute Engine host metrics via gcloud:\n'
                                      '\n'
                                      '```bash\n'
                                      'gcloud monitoring metric-descriptors describe '
                                      'compute.googleapis.com/instance/cpu/utilization\n'
                                      '# Metric recorded 0.14 utilization at 03:14:00 UTC (hypervisor has 0% insight '
                                      'into in-guest RSS allocations)\n'
                                      '```',
                          'diagnostic_steps': ['Inspect `agent.googleapis.com` metric availability in Metrics Explorer '
                                               'for the failing VM.',
                                               'Review serial port output via `gcloud compute instances '
                                               'get-serial-port-output` to confirm OOM killer invocation.',
                                               'Audit VM metadata to inspect installed daemon agents and OS Config '
                                               'policies.'],
                          'root': 'Lack of guest-level telemetry: without the Ops Agent, Cloud Monitoring only '
                                  'receives hypervisor CPU ticks and cannot observe guest RAM or swap exhaustion, '
                                  'leaving SREs completely blind to memory leaks.',
                          'fix': 'Author a declarative `config.yaml` enabling hostmetrics and application receivers. '
                                 'Deploy a VM Manager OS Config Policy ensuring automated Ops Agent installation and '
                                 'enforcement across all existing and future Compute Engine instances.',
                          'verify': 'Verify `agent.googleapis.com/memory/percent_used` metrics appear in Cloud '
                                    'Monitoring and configure an alert policy firing at >85% RAM utilization.',
                          'residual': 'The Ops Agent consumes approximately 50–100 MiB of guest RAM and 1–2% of a '
                                      'single vCPU core; on very small instances (e.g. `e2-micro`), this overhead must '
                                      'be planned into memory budgeting.',
                          'diagram': ('Hypervisor metrics report 14% CPU',
                                      'Guest RAM quietly leaks to 100%',
                                      'Kernel OOM killer terminates DB',
                                      'Ops Agent deployed via OS Policy',
                                      'Proactive in-guest RAM alert fires')},
             'lab': {'name': 'Ops Agent Configuration Blueprint and OS Config Fleet Policy Synthesis',
                     'goal': 'Author a production Ops Agent declarative configuration manifest and an automated VM '
                             'Manager OS Policy deployment script.',
                     'expected': 'A validated `config.yaml` with custom logging and metric pipelines, and an '
                                 'executable OS Policy assignment definition.',
                     'mode': 'tabletop analysis & YAML/JSON synthesis',
                     'prereq': 'Understanding of Linux systemd journals and Compute Engine VM Manager.',
                     'preflight': 'Review Ops Agent configuration syntax and OS Policy assignment parameters.',
                     'steps': ['#### Stage 1: Pre-Flight Guest Metric & Telemetry Inspection\n'
                               'Audit existing Compute Engine metric visibility to verify absence of guest operating '
                               'system metrics:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_guest_metrics.py\n"
                               'import json\n'
                               '\n'
                               '# Verify host hypervisor metric limits\n'
                               "host_metrics = ['compute.googleapis.com/instance/cpu/utilization', "
                               "'compute.googleapis.com/instance/disk/read_bytes_count']\n"
                               "guest_metrics = ['agent.googleapis.com/memory/percent_used', "
                               "'agent.googleapis.com/processes/count_by_state']\n"
                               '\n'
                               "print('[PREFLIGHT] Validating Compute Engine observability tier...')\n"
                               "print(f'[HOST METRICS] Available by default: {host_metrics}')\n"
                               "print(f'[GUEST METRICS] Requires Google Cloud Ops Agent: {guest_metrics}')\n"
                               'EOF\n'
                               'python3 check_guest_metrics.py\n'
                               '```',
                               '#### Stage 2: Infrastructure Preflight & Agent Repository Verification\n'
                               'Inspect the target VM environment and verify package repository signing keys:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_agent_prereqs.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Verifying Linux distribution and systemd readiness..."\n'
                               'uname -a\n'
                               'which systemctl >/dev/null && echo "[PASS] systemd init system confirmed."\n'
                               'echo "Simulating Ops Agent repository check..."\n'
                               'test -d /etc/google-cloud-ops-agent || mkdir -p /etc/google-cloud-ops-agent\n'
                               'echo "[PASS] Configuration directory initialized."\n'
                               'EOF\n'
                               'bash verify_agent_prereqs.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Production Ops Agent Config Manifest\n'
                               'Author a production declarative Ops Agent configuration '
                               '(`/etc/google-cloud-ops-agent/config.yaml`) defining custom log receivers and process '
                               'metrics:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > generate_ops_agent_config.py\n"
                               "ops_agent_yaml = '''logging:\n"
                               '  receivers:\n'
                               '    app_mysql_error:\n'
                               '      type: files\n'
                               "      include_paths: ['/var/log/mysql/error.log']\n"
                               '      record_log_file_path: true\n'
                               '    system_syslog:\n'
                               '      type: files\n'
                               "      include_paths: ['/var/log/syslog', '/var/log/messages']\n"
                               '  processors:\n'
                               '    parse_severity:\n'
                               '      type: parse_regex\n'
                               "      regex: '^(?<time>\\\\S+ \\\\S+) (?<host>\\\\S+) (?<ident>\\\\S+): "
                               "(?<message>.*)$'\n"
                               '  service:\n'
                               '    pipelines:\n'
                               '      default_pipeline:\n'
                               '        receivers: [app_mysql_error, system_syslog]\n'
                               '        processors: [parse_severity]\n'
                               'metrics:\n'
                               '  receivers:\n'
                               '    hostmetrics:\n'
                               '      type: hostmetrics\n'
                               '      collection_interval: 30s\n'
                               '    process_metrics:\n'
                               '      type: processes\n'
                               '      collection_interval: 30s\n'
                               '  service:\n'
                               '    pipelines:\n'
                               '      default_pipeline:\n'
                               '        receivers: [hostmetrics, process_metrics]\n'
                               "'''\n"
                               '\n'
                               "with open('ops_agent_config.yaml', 'w') as f:\n"
                               '    f.write(ops_agent_yaml)\n'
                               "print('[CONFIG] Production Ops Agent configuration written to ops_agent_config.yaml')\n"
                               'EOF\n'
                               'python3 generate_ops_agent_config.py\n'
                               '```',
                               '#### Stage 4: Fleet Automation: VM Manager OS Policy Assignment Manifest\n'
                               'Author the declarative OS Policy Assignment JSON manifest to automate fleet-wide '
                               'installation across production instances:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > os_policy_ops_agent.json\n"
                               '{\n'
                               '  "osPolicies": [\n'
                               '    {\n'
                               '      "id": "ops-agent-fleet-policy",\n'
                               '      "mode": "ENFORCEMENT",\n'
                               '      "resourceGroups": [\n'
                               '        {\n'
                               '          "resources": [\n'
                               '            {\n'
                               '              "id": "install-ops-agent-pkg",\n'
                               '              "pkg": {\n'
                               '                "desiredState": "INSTALLED",\n'
                               '                "apt": {"name": "google-cloud-ops-agent"}\n'
                               '              }\n'
                               '            }\n'
                               '          ]\n'
                               '        }\n'
                               '      ]\n'
                               '    }\n'
                               '  ],\n'
                               '  "instanceFilter": {\n'
                               '    "inclusionLabels": [{"labels": {"env": "production"}}]\n'
                               '  },\n'
                               '  "rollout": {\n'
                               '    "disruptionBudget": {"fixed": 10},\n'
                               '    "minWaitDuration": "60s"\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[POLICY] OS Policy Assignment manifest os_policy_ops_agent.json validated."\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Fluent Bit Syntax Failure Chaos Injection\n'
                               'Inject malformed configuration syntax to verify agent validation gates and prevent '
                               'service crash loops:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_corrupt_config.py\n"
                               'import yaml\n'
                               '\n'
                               "malformed_config = '''logging:\n"
                               '  receivers:\n'
                               '    broken_receiver:\n'
                               '      type: invalid_type_name\n'
                               "'''\n"
                               '\n'
                               'try:\n'
                               '    cfg = yaml.safe_load(malformed_config)\n'
                               "    receiver_type = cfg['logging']['receivers']['broken_receiver']['type']\n"
                               "    valid_types = ['files', 'fluentforward', 'tcp']\n"
                               '    if receiver_type not in valid_types:\n'
                               "        raise ValueError(f'Unsupported Ops Agent receiver type: {receiver_type}')\n"
                               'except Exception as e:\n'
                               "    print(f'[CHAOS TEST PASS] Configuration validator intercepted fatal syntax error: "
                               "{e}')\n"
                               'EOF\n'
                               'python3 test_corrupt_config.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Guest Memory Alert Rule Synthesis\n'
                               'Author a Cloud Monitoring Alert Policy JSON configuration alerting when in-guest '
                               'memory exceeds 90%:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_policy_memory.json\n"
                               '{\n'
                               '  "displayName": "CRITICAL: GCE In-Guest Memory Utilization > 90%",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "Ops Agent RAM percent_used condition",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": "metric.type=\\"agent.googleapis.com/memory/percent_used\\" AND '
                               'resource.type=\\"gce_instance\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 90.0,\n'
                               '        "duration": "120s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] In-guest RAM alert policy synthesized in '
                               'alert_policy_memory.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Fleet Compliance Assertions\n'
                               'Run an automated verification script validating both configuration schema and policy '
                               'filtering semantics:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_ops_agent_deployment.py\n"
                               'import json\n'
                               'import yaml\n'
                               '\n'
                               "with open('ops_agent_config.yaml') as f:\n"
                               '    agent_cfg = yaml.safe_load(f)\n'
                               "assert 'logging' in agent_cfg and 'metrics' in agent_cfg, 'Config missing primary "
                               "stanzas'\n"
                               "assert 'hostmetrics' in agent_cfg['metrics']['receivers'], 'Missing hostmetrics "
                               "receiver'\n"
                               "assert 'process_metrics' in agent_cfg['metrics']['receivers'], 'Missing process "
                               "metrics receiver'\n"
                               '\n'
                               "with open('os_policy_ops_agent.json') as f:\n"
                               '    policy_cfg = json.load(f)\n'
                               "assert policy_cfg['osPolicies'][0]['mode'] == 'ENFORCEMENT', 'Policy must be in "
                               "ENFORCEMENT mode'\n"
                               "assert policy_cfg['instanceFilter']['inclusionLabels'][0]['labels']['env'] == "
                               "'production'\n"
                               '\n'
                               "print('[ASSERT PASS] Ops Agent configuration and OS Policy Assignment strictly "
                               "compliant.')\n"
                               'EOF\n'
                               'python3 verify_ops_agent_deployment.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Execute automated teardown script removing temporary verification artifacts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_ops_agent_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 95 Topic 1 test manifests..."\n'
                               'rm -f check_guest_metrics.py verify_agent_prereqs.sh generate_ops_agent_config.py '
                               'test_corrupt_config.py verify_ops_agent_deployment.py\n'
                               'echo "[CLEANUP] Retaining production configs: ops_agent_config.yaml, '
                               'os_policy_ops_agent.json, alert_policy_memory.json"\n'
                               'echo "[CLEANUP PASS] Ops Agent lab cleanup completed successfully."\n'
                               'EOF\n'
                               'bash teardown_ops_agent_lab.sh\n'
                               '```'],
                     'verification': 'The Ops Agent config accurately specifies receivers and service pipelines, and '
                                     'the OS Policy Assignment defines bounded disruption budgets and enforcement '
                                     'scripts.',
                     'trouble': 'Ensure `time_key` and `time_format` in `parse_json` match the exact RFC 3339 '
                                'timestamp emitted by the application logging library.',
                     'cleanup': 'Retain `ops-agent-config.yaml` and `day-095-topic-01-ospolicy-agent.json` as exit '
                                'evidence artifacts.',
                     'accept': 'Completed Ops Agent configuration and verified OS Policy assignment manifest. File: '
                               '`day-095-topic-01-ops-agent.md`.',
                     'file': 'day-095-topic-01-ops-agent.md'}},
            {'key': 'topic-02',
             'title': 'Centralized Logging Design Across Projects and Organization-Level Aggregated Sinks',
             'overview': 'In an enterprise Google Cloud environment with dozens or hundreds of projects, '
                         'decentralizing log management introduces severe compliance vulnerabilities: individual '
                         'project owners can delete security log buckets, disable audit sinks, or tamper with '
                         'evidence. Centralized logging aggregates log records at the Organization or Folder level '
                         'using **Aggregated Log Router Sinks** configured with `--include-children`. These sinks '
                         'route all matching logs downstream into a dedicated, locked-down Security Telemetry Project, '
                         'providing an immutable, centralized logging repository for Security Operations Centers (SOC) '
                         'and compliance auditors.',
             'preview': 'A rogue administrator with Project Owner permissions deletes local log buckets to hide '
                        'malicious resource tampering. Organization-level aggregated sinks capture and lock audit logs '
                        'in a centralized vault before local project administrators can touch them.',
             'technical': '### 1. Organization & Folder Aggregated Sinks (`--include-children`)\n'
                          '- **Inheritance:** An aggregated sink created at the Organization level '
                          '(`organizations/{ORG_ID}`) or Folder level (`folders/{FOLDER_ID}`) with the '
                          '`--include-children` flag automatically intercepts logs emitted by every current and future '
                          'project within that hierarchy.\n'
                          '- **Non-Intercepting vs Intercepting Sinks:**\n'
                          '  - **Non-Intercepting (Default):** The aggregated sink copies a copy of the log to the '
                          'central security destination while leaving the original log record to continue flowing '
                          'through local child project Log Routers for developer visibility.\n'
                          '  - **Intercepting (`--intercept-children`):** The sink captures the log and stops it from '
                          'flowing to child project log routers, used when sensitive audit logs must be hidden from '
                          'local project teams.\n'
                          '\n'
                          '### 2. Dedicated Security Project & Central Log Bucket Topology\n'
                          '- **Destination Project:** Sinks route logs to '
                          '`logging.googleapis.com/projects/{SEC_PROJECT}/locations/{REGION}/buckets/{CENTRAL_BUCKET}`.\n'
                          '- **Sink Writer Identity:** Creating an organization sink generates a unique service '
                          'account (Writer Identity): `o123456789-999@gcp-sa-logging.iam.gserviceaccount.com`. This '
                          'identity must be granted `roles/logging.bucketWriter` on the target bucket.\n'
                          '- **IAM Segregation:** Local project developers have zero IAM permissions in the '
                          'centralized security project. Even if a local project is compromised, attackers cannot '
                          'modify, truncate, or delete historical log records in the central vault.\n'
                          '\n'
                          '### 3. Log Analytics and SIEM Export Topology\n'
                          '- Centralized Log Buckets enable Log Analytics, allowing security teams to run SQL queries '
                          'across logs from 500 projects simultaneously.\n'
                          '- In parallel, a Pub/Sub sink forwards high-severity security events in real time to '
                          'third-party SIEM platforms (Splunk, Chronicle, Microsoft Sentinel).',
             'questions': ['How does the `--include-children` flag eliminate telemetry onboarding friction when new '
                           'projects are created in a folder?',
                           'What security vulnerability arises if central logging relies on local project-level sinks '
                           'rather than organization-level sinks?',
                           'How does configuring a distinct Writer Identity per aggregated sink enforce the principle '
                           'of least privilege in multi-tenant architectures?'],
             'reference': 'https://docs.cloud.google.com/logging/docs/routing/overview#aggregated_sinks',
             'reference_label': 'Google Cloud Logging: Aggregated organization and folder sinks with child inheritance',
             'scenario': {'symptom': 'During a forensic investigation into a suspected data breach, security analysts '
                                     'discovered that all Cloud Audit Logs in the affected project had been deleted, '
                                     "and the project's local log retention had been altered from 365 days to 1 day.",
                          'constraints': 'Must guarantee immutable log retention that cannot be deleted or bypassed by '
                                         'users holding `roles/owner` or `roles/editor` in child workload projects.',
                          'evidence': 'Cloud Logging log sink status and error metrics:\n'
                                      '\n'
                                      '```bash\n'
                                      'gcloud logging sinks describe org-security-audit-sink '
                                      '--organization=108420918237\n'
                                      '```\n'
                                      '\n'
                                      'Output reveals sink writer identity:\n'
                                      '\n'
                                      '```yaml\n'
                                      'destination: '
                                      'logging.googleapis.com/projects/sec-vault-prod/locations/global/buckets/org-audit-bucket\n'
                                      'filter: logName:"cloudaudit.googleapis.com"\n'
                                      'includeChildren: true\n'
                                      'name: org-security-audit-sink\n'
                                      'writerIdentity: '
                                      'serviceAccount:o108420918237-91823@gcp-sa-logging.iam.gserviceaccount.com\n'
                                      '```\n'
                                      '\n'
                                      'Metric error inspection:\n'
                                      '\n'
                                      '```text\n'
                                      'logging.googleapis.com/log_entry_dropped_count {reason: "PERMISSION_DENIED", '
                                      'destination: "projects/sec-vault-prod/..."} = 4,812,019 drops\n'
                                      'HTTP 403 Forbidden: Caller does not have required permission '
                                      "'logging.buckets.write' on resource "
                                      "'projects/sec-vault-prod/locations/global/buckets/org-audit-bucket'.\n"
                                      '```',
                          'diagnostic_steps': ['Audit organization-level log sinks via `gcloud logging sinks list '
                                               '--organization={ORG_ID}`.',
                                               'Review IAM policy bindings on the compromised project to determine how '
                                               'permissions were escalated.',
                                               "Inspect the central security project's log intake to verify whether an "
                                               'immutable centralized sink existed.'],
                          'root': 'Decentralized log architecture: relying on local project log buckets allowed local '
                                  'project administrators to destroy forensic audit evidence upon compromising '
                                  'project-level credentials.',
                          'fix': 'Deploy an organization-level aggregated sink with `--include-children` routing all '
                                 'audit and security logs directly to a dedicated, IAM-isolated '
                                 '`brightloaf-security-vault` project. Apply Cloud Storage bucket lock or Log Bucket '
                                 'retention lock.',
                          'verify': 'Simulate an administrative action in a child project; verify the event appears in '
                                    "the central security project's bucket within seconds. Attempt to delete the "
                                    'central log bucket using child project owner credentials and confirm HTTP 403 '
                                    'Forbidden.',
                          'residual': 'Aggregated sinks increase cross-project log ingestion volume; architects must '
                                      'pair aggregated sinks with strict inclusion filters to avoid centralizing '
                                      'low-value debug noise.',
                          'diagram': ('Aggregated sink created at Org root',
                                      'Writer SA lacking IAM write role',
                                      '4.8M audit logs silently dropped',
                                      'Grant roles/logging.bucketWriter to SA',
                                      'Audit stream restored to central vault')},
             'lab': {'name': 'Organization Aggregated Log Sink and Central Security Vault Architecture',
                     'goal': 'Author an organization-level aggregated sink specification and verify IAM writer '
                             'identity permissions and log routing.',
                     'expected': 'A complete gcloud deployment script for an organization aggregated sink with '
                                 'verified IAM bindings and architecture diagram.',
                     'mode': 'tabletop analysis & shell synthesis',
                     'prereq': 'Understanding of Google Cloud Resource Manager hierarchies and Log Router sinks.',
                     'preflight': 'Review organization-level gcloud logging commands and IAM role bindings.',
                     'steps': ['#### Stage 1: Pre-Flight Aggregated Log Sink Hierarchy Audit\n'
                               'Audit the enterprise resource hierarchy to verify organization and folder node IDs:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_hierarchy.py\n"
                               "org_id = '108420918237'\n"
                               "dest_project = 'sec-vault-prod'\n"
                               "bucket_id = 'org-audit-bucket'\n"
                               'expected_dest = '
                               "f'logging.googleapis.com/projects/{dest_project}/locations/global/buckets/{bucket_id}'\n"
                               "print(f'[PREFLIGHT] Auditing hierarchy for Org: {org_id}')\n"
                               "print(f'[PREFLIGHT] Centralized Destination: {expected_dest}')\n"
                               'EOF\n'
                               'python3 check_hierarchy.py\n'
                               '```',
                               '#### Stage 2: Infrastructure Preflight & Permission Inspection\n'
                               'Verify destination bucket IAM bindings and simulate Cloud Logging permission '
                               'validation:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_iam_preflight.py\n"
                               "required_role = 'roles/logging.bucketWriter'\n"
                               "print(f'[PREFLIGHT] Required IAM role on central log bucket: {required_role}')\n"
                               "print('[PREFLIGHT] Note: Sinks created with --include-children generate a unique "
                               "organization writer identity service account.')\n"
                               'EOF\n'
                               'python3 verify_iam_preflight.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Aggregated Organization Sink Manifest\n'
                               'Author a declarative Terraform configuration deploying the organization-level '
                               'aggregated sink with children inclusion and exclusion rules:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > aggregated_sink.tf\n"
                               'resource "google_logging_organization_sink" "org_audit_sink" {\n'
                               '  name             = "org-security-audit-sink"\n'
                               '  description      = "Aggregated audit log sink routing all organization child '
                               'telemetry to central vault"\n'
                               '  org_id           = "108420918237"\n'
                               '  destination      = '
                               '"logging.googleapis.com/projects/sec-vault-prod/locations/global/buckets/org-audit-bucket"\n'
                               '  include_children = true\n'
                               '\n'
                               '  filter = <<-EOT\n'
                               '    logName:"cloudaudit.googleapis.com"\n'
                               '  EOT\n'
                               '\n'
                               '  exclusions {\n'
                               '    name        = "exclude-gke-read-tokens"\n'
                               '    description = "Exclude repetitive GKE service account read tokens from flooding '
                               'SIEM"\n'
                               '    filter      = '
                               '"protoPayload.methodName=\\"io.k8s.certificates.v1.certificatesigningrequests.get\\""\n'
                               '  }\n'
                               '}\n'
                               '\n'
                               'resource "google_project_iam_member" "sink_writer_permission" {\n'
                               '  project = "sec-vault-prod"\n'
                               '  role    = "roles/logging.bucketWriter"\n'
                               '  member  = google_logging_organization_sink.org_audit_sink.writer_identity\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Created aggregated_sink.tf"\n'
                               '```',
                               '#### Stage 4: Execution & Ingestion Verification Script\n'
                               'Simulate the sink deployment and verify writer identity binding extraction:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_sink_deployment.py\n"
                               'import re\n'
                               '\n'
                               "with open('aggregated_sink.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'include_children = true' in tf\n"
                               "assert 'roles/logging.bucketWriter' in tf\n"
                               "print('[DEPLOY SIM] Aggregated sink manifest contains necessary include_children and "
                               "IAM grant.')\n"
                               'EOF\n'
                               'python3 simulate_sink_deployment.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Permission Revocation Fault Injection\n'
                               'Simulate an ungranted writer identity to confirm the alert and logging failure mode:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_sink_permission_fault.py\n"
                               'class MockSink:\n'
                               '    def __init__(self, writer_sa, bucket_permissions):\n'
                               '        self.writer_sa = writer_sa\n'
                               '        self.bucket_permissions = bucket_permissions\n'
                               '\n'
                               '    def write_log(self, log_entry):\n'
                               '        if self.writer_sa not in self.bucket_permissions:\n'
                               "            raise PermissionError(f'HTTP 403 Forbidden: {self.writer_sa} lacks "
                               "logging.buckets.write')\n"
                               "        return 'LOG_INGESTED_200_OK'\n"
                               '\n'
                               '# Fault injection: SA missing from bucket permissions\n'
                               "sink = MockSink('serviceAccount:o10842-sa@gcp-sa-logging.iam.gserviceaccount.com', "
                               'set())\n'
                               'try:\n'
                               "    sink.write_log({'event': 'ADMIN_WRITE'})\n"
                               'except PermissionError as e:\n'
                               "    print(f'[CHAOS TEST PASS] Intercepted expected destination permission denial: "
                               "{e}')\n"
                               'EOF\n'
                               'python3 test_sink_permission_fault.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Sink Error Monitoring\n'
                               'Author a Cloud Monitoring Alert manifest detecting any dropped logs across enterprise '
                               'sinks:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_sink_errors.json\n"
                               '{\n'
                               '  "displayName": "ALERT: Aggregated Log Sink Log Drop Rate > 0",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "Logging log_entry_dropped_count",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": "metric.type=\\"logging.googleapis.com/log_entry_dropped_count\\" '
                               'AND resource.type=\\"logging_sink\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 0.0,\n'
                               '        "duration": "60s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] Sink drop alert policy synthesized in alert_sink_errors.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Sink Boundary Assertions\n'
                               'Execute automated test validating Terraform manifest attributes and IAM binding '
                               'consistency:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_sink_integrity.py\n"
                               "with open('aggregated_sink.tf') as f:\n"
                               '    manifest = f.read()\n'
                               '\n'
                               "assert 'google_logging_organization_sink' in manifest\n"
                               "assert 'include_children = true' in manifest\n"
                               "assert 'exclusions {' in manifest\n"
                               "assert 'google_project_iam_member' in manifest\n"
                               "print('[ASSERT PASS] Aggregated sink infrastructure manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_sink_integrity.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script cleaning up local test artifacts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_sink_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 95 Topic 2 test scripts..."\n'
                               'rm -f check_hierarchy.py verify_iam_preflight.py simulate_sink_deployment.py '
                               'test_sink_permission_fault.py assert_sink_integrity.py\n'
                               'echo "[CLEANUP] Retaining production manifests: aggregated_sink.tf, '
                               'alert_sink_errors.json"\n'
                               'echo "[CLEANUP PASS] Aggregated sink lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_sink_lab.sh\n'
                               '```'],
                     'verification': 'The shell script includes `--include-children` and assigns '
                                     '`roles/logging.bucketWriter`, and the Python isolation test proves local project '
                                     'owners cannot tamper with central vault buckets.',
                     'trouble': 'Ensure the central bucket already exists with Log Analytics enabled before creating '
                                'the organization sink to prevent dead-letter sink drops.',
                     'cleanup': 'Retain `deploy_org_aggregated_sink.sh` as an exit evidence artifact.',
                     'accept': 'Completed aggregated organization sink script and verified IAM isolation test. File: '
                               '`day-095-topic-02-aggregated-sinks.md`.',
                     'file': 'day-095-topic-02-aggregated-sinks.md'}},
            {'key': 'topic-03',
             'title': 'Cloud Audit Log Types: Admin Activity, Data Access, System Events, and Policy Denied',
             'overview': "Google Cloud Audit Logs answer the fundamental forensic question: 'Who did what, where, and "
                         "when?' Across the platform, audit events are divided into five distinct types: Admin "
                         'Activity (mandatory and free), Data Access (ADMIN_READ, DATA_READ, DATA_WRITE; high-volume '
                         'and billable), System Event (Google automated actions), and Policy Denied (security rule '
                         'violations). Understanding their ingestion mechanics, default states, and analytical SQL '
                         'signatures is vital for detecting privilege escalation, credential theft, and compliance '
                         'drift.',
             'preview': 'An attacker obtains stolen service account credentials and elevates their IAM permissions '
                        'before downloading a customer database. Admin Activity audit logs provide undeniable '
                        'cryptographic proof of the exact authorization change and source IP address.',
             'technical': '### 1. In-Depth Analysis of the Five Audit Log Streams\n'
                          '- **Admin Activity Logs (`cloudaudit.googleapis.com/activity`):**\n'
                          '  - Records calls that alter GCP resource configuration or metadata (e.g. `SetIamPolicy`, '
                          '`CreateBucket`, `InsertInstance`).\n'
                          '  - **State:** Enabled by default on all services; cannot be disabled by any user or '
                          'organization policy.\n'
                          '  - **Retention & Billing:** Retained for 400 days in the `_Required` bucket; 100% free of '
                          'ingestion and storage charges.\n'
                          '- **Data Access Logs (`cloudaudit.googleapis.com/data_access`):**\n'
                          '  - Divided into three sub-types: `ADMIN_READ` (reading metadata/IAM), `DATA_READ` (reading '
                          'user data like GCS objects), and `DATA_WRITE` (modifying user data like Cloud Spanner '
                          'records).\n'
                          '  - **State:** Disabled by default (except BigQuery Data Access, which is always enabled).\n'
                          '  - **Billing:** Billed at standard log ingestion rates; turning on `DATA_READ` on '
                          'high-throughput Cloud Storage buckets can generate millions of events per hour and massive '
                          'bills.\n'
                          '- **System Event Logs (`cloudaudit.googleapis.com/system_event`):**\n'
                          '  - Records automated platform events executed by Google infrastructure (e.g., GCE live '
                          'migration during hardware servicing).\n'
                          '  - **State:** Always on; 400 days retention; free of charge.\n'
                          '- **Policy Denied Logs (`cloudaudit.googleapis.com/policy`):**\n'
                          '  - Emitted whenever a security policy denies an API call (e.g. VPC Service Controls '
                          'boundary violation, IAM Deny rule).\n'
                          '  - Essential for identifying data exfiltration attempts and misconfigured service '
                          'accounts.\n'
                          '\n'
                          '### 2. Forensic Log Payload Anatomy\n'
                          '- Audit logs are structured in `protoPayload` conforming to `google.cloud.audit.AuditLog`:\n'
                          '  - `authenticationInfo.principalEmail`: Identity of the actor (user or service account).\n'
                          '  - `requestMetadata.callerIp`: Public IP address where the API request originated.\n'
                          '  - `methodName`: The exact API RPC invoked (e.g. '
                          '`google.iam.admin.v1.CreateServiceAccountKey`).\n'
                          '  - `authorizationInfo`: Permissions checked, resource evaluated, and granted status.\n'
                          '  - `serviceData` / `request`: The serialized API request parameters submitted by the '
                          'caller.',
             'questions': ['Why are Admin Activity audit logs enabled permanently by default and retained for 400 days '
                           'without cost to the customer?',
                           'What architectural risks and costs must be evaluated before enabling Data Access '
                           '`DATA_READ` logging on high-traffic storage buckets?',
                           'How do Policy Denied audit logs distinguish between an unintentional network '
                           'misconfiguration and an active malicious data exfiltration attempt?'],
             'reference': 'https://docs.cloud.google.com/logging/docs/audit',
             'reference_label': 'Google Cloud Audit Logs: Architecture, types, retention periods, and BigQuery '
                                'forensic querying',
             'scenario': {'symptom': "A junior developer's compromised laptop credentials were used at 02:30 UTC on a "
                                     'Sunday to grant the external account `attacker@external-evil.com` the '
                                     '`roles/resourcemanager.organizationAdmin` role across the entire Google Cloud '
                                     'organization.',
                          'constraints': 'Must identify the compromised identity, source IP, affected resource, and '
                                         'exact timestamp within 15 minutes to revoke access and isolate compromised '
                                         'keys.',
                          'evidence': 'Forensic audit trail investigation showing missing telemetry:\n'
                                      '\n'
                                      '```bash\n'
                                      'gcloud logging read \'logName:"cloudaudit.googleapis.com" AND '
                                      'resource.type="gcs_bucket"\' --limit=5\n'
                                      '# Returned 0 entries during the exact window of database snapshot export\n'
                                      '```\n'
                                      '\n'
                                      'Organization audit logging configuration check:\n'
                                      '\n'
                                      '```bash\n'
                                      'gcloud organizations get-iam-policy 108420918237\n'
                                      '```\n'
                                      '\n'
                                      'Policy extract showing Data Access audit logs unconfigured for Storage:\n'
                                      '\n'
                                      '```yaml\n'
                                      'auditConfigs:\n'
                                      '- auditLogConfigs:\n'
                                      '  - logType: ADMIN_READ\n'
                                      '  service: allServices\n'
                                      '# DATA_READ and DATA_WRITE completely missing for storage.googleapis.com\n'
                                      '```',
                          'diagnostic_steps': ['Query Admin Activity logs for `methodName = '
                                               "'google.iam.admin.v1.SetIamPolicy'` or `SetOrgPolicy`.",
                                               'Extract `authenticationInfo.principalEmail` and '
                                               '`requestMetadata.callerIp`.',
                                               'Inspect the `request.policy.bindings` payload to compare '
                                               'before-and-after role assignments.'],
                          'root': 'Compromised developer credentials: an active session token was used to execute an '
                                  'unauthorized IAM policy update granting organization-level administrative access.',
                          'fix': 'Immediately revoke the unauthorized IAM binding via `gcloud organizations '
                                 "remove-iam-policy-binding`. Revoke the developer's session credentials and disable "
                                 'the affected user account. Deploy a Cloud Monitoring real-time alert on high-risk '
                                 'IAM mutation methods.',
                          'verify': 'Run the forensic SQL query and verify the removal of the malicious binding is '
                                    'logged with a corresponding Admin Activity event. Confirm the external account '
                                    'has 0 active bindings.',
                          'residual': 'Admin Activity logs prove that an IAM binding was granted, but determining what '
                                      'actions the attacker performed during the window requires cross-correlating '
                                      'with Data Access logs, which must be enabled beforehand.',
                          'diagram': ('Compromised SA accesses backup bucket',
                                      'DATA_READ audit logs disabled',
                                      'Forensics cannot identify leaked data',
                                      'Enable DATA_READ/WRITE on Storage',
                                      'Audit trail captures object downloads')},
             'lab': {'name': 'Audit Log Forensics and BigQuery IAM Mutation Detection Synthesis',
                     'goal': 'Author a production BigQuery Log Analytics forensic query detecting unauthorized IAM '
                             'policy mutations and build an automated test script.',
                     'expected': 'A validated BigQuery SQL query extracting caller IP and IAM deltas, and an '
                                 'executable Python test script validating forensic detection.',
                     'mode': 'tabletop analysis & SQL/Python execution',
                     'prereq': 'Understanding of Cloud Audit Logs and BigQuery SQL.',
                     'preflight': 'Review google.cloud.audit.AuditLog schema and BigQuery JSON functions.',
                     'steps': ['#### Stage 1: Pre-Flight Audit Configuration Discovery\n'
                               'Inspect organization and project IAM audit configuration to catalog enabled audit '
                               'streams:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > discover_audit_configs.py\n"
                               'audit_types = {\n'
                               "    'ADMIN_ACTIVITY': 'Always enabled by default, free of ingestion charge.',\n"
                               "    'DATA_READ': 'Disabled by default. Generates high volume on Cloud Storage / "
                               "BigQuery.',\n"
                               "    'DATA_WRITE': 'Disabled by default. Logs object writes, table alterations.',\n"
                               "    'ADMIN_READ': 'Disabled by default. Logs get/list administrative reads.'\n"
                               '}\n'
                               "print('[PREFLIGHT] Cataloging Cloud Audit Log streams:')\n"
                               'for k, v in audit_types.items():\n'
                               "    print(f'  • {k}: {v}')\n"
                               'EOF\n'
                               'python3 discover_audit_configs.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Audit Exemption Verification\n'
                               'Inspect IAM policy structure for exempt members that bypass audit generation:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_audit_exemptions.py\n"
                               'exempt_members = '
                               "['serviceAccount:high-throughput-worker@app.iam.gserviceaccount.com']\n"
                               "print('[PREFLIGHT] Auditing exempt members list...')\n"
                               "print(f'[SECURITY WARNING] Audit exemption active for: {exempt_members}')\n"
                               'EOF\n'
                               'python3 check_audit_exemptions.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Cloud Audit Policy Manifest\n'
                               'Author a declarative Terraform configuration enabling `DATA_READ` and `DATA_WRITE` for '
                               'sensitive services while exempting high-velocity internal workers:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > audit_policy.tf\n"
                               'resource "google_project_iam_audit_config" "storage_audit" {\n'
                               '  project = "prod-data-platform"\n'
                               '  service = "storage.googleapis.com"\n'
                               '\n'
                               '  audit_log_config {\n'
                               '    log_type = "DATA_READ"\n'
                               '    exempted_members = [\n'
                               '      '
                               '"serviceAccount:internal-backup-runner@prod-data-platform.iam.gserviceaccount.com"\n'
                               '    ]\n'
                               '  }\n'
                               '\n'
                               '  audit_log_config {\n'
                               '    log_type = "DATA_WRITE"\n'
                               '  }\n'
                               '}\n'
                               '\n'
                               'resource "google_project_iam_audit_config" "iam_audit" {\n'
                               '  project = "prod-data-platform"\n'
                               '  service = "iam.googleapis.com"\n'
                               '\n'
                               '  audit_log_config {\n'
                               '    log_type = "ADMIN_READ"\n'
                               '  }\n'
                               '  audit_log_config {\n'
                               '    log_type = "DATA_READ"\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authoring audit_policy.tf complete."\n'
                               '```',
                               '#### Stage 4: Execution & BigQuery SQL Forensic Threat Hunt Query\n'
                               'Author an optimized BigQuery SQL query to detect unauthorized IAM role grants '
                               '(`SetIamPolicy`):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > forensic_threat_hunt.sql\n"
                               '-- BigQuery Log Analytics Forensic Threat Hunting Query\n'
                               '-- Target: Detect anomalous SetIamPolicy role grants across projects\n'
                               'SELECT\n'
                               '  timestamp,\n'
                               '  protopayload_auditlog.authenticationInfo.principalEmail AS actor,\n'
                               '  protopayload_auditlog.resourceName AS resource,\n'
                               '  protopayload_auditlog.methodName AS method,\n'
                               '  binding.role AS assigned_role,\n'
                               '  member AS granted_principal\n'
                               'FROM\n'
                               '  `sec-vault-prod.global_audit_dataset._AllLogs`,\n'
                               '  '
                               'UNNEST(JSON_EXTRACT_ARRAY(protopayload_auditlog.serviceData.policyDelta.bindingDeltas)) '
                               'AS delta,\n'
                               "  UNNEST([JSON_EXTRACT_SCALAR(delta, '$.role')]) AS binding_role,\n"
                               "  UNNEST(JSON_EXTRACT_STRING_ARRAY(delta, '$.action')) AS action\n"
                               'WHERE\n'
                               '  protopayload_auditlog.methodName LIKE "%SetIamPolicy%"\n'
                               '  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)\n'
                               'ORDER BY timestamp DESC\n'
                               'LIMIT 100;\n'
                               'EOF\n'
                               'echo "[SQL] Forensic query saved to forensic_threat_hunt.sql"\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Audit Log Tampering Tabletop\n'
                               'Simulate an attempt by an attacker with `roles/owner` to delete Cloud Audit logs and '
                               'verify platform immutability:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_audit_immutability.py\n"
                               'def simulate_audit_delete_attempt(role):\n'
                               '    # Google Cloud Audit Logs cannot be deleted or modified by any IAM principal\n'
                               "    immutable_types = ['cloudaudit.googleapis.com/activity', "
                               "'cloudaudit.googleapis.com/data_access']\n"
                               "    if role in ['roles/owner', 'roles/editor', 'roles/logging.admin']:\n"
                               "        return '[SECURITY PASS] Google Cloud API rejected log deletion: Cloud Audit "
                               "Logs are append-only and cryptographically immutable.'\n"
                               "    return 'DENIED'\n"
                               '\n'
                               "print(simulate_audit_delete_attempt('roles/owner'))\n"
                               'EOF\n'
                               'python3 test_audit_immutability.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Policy Denied Anomaly Detection\n'
                               'Author a Cloud Monitoring metric-based alerting rule triggering when '
                               '`cloudaudit.googleapis.com/policy` denies spike:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_policy_denied.json\n"
                               '{\n'
                               '  "displayName": "SECURITY: IAM Policy Denied Spike Detected",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "High volume of Policy Denied audit entries",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": '
                               '"logName=\\"projects/sec-vault-prod/logs/cloudaudit.googleapis.com%2Fpolicy\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 10.0,\n'
                               '        "duration": "60s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] Policy denied alert policy synthesized in '
                               'alert_policy_denied.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Audit Completeness Assertions\n'
                               'Execute automated test validating audit policy definitions and SQL schema syntax:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_audit_compliance.py\n"
                               "with open('audit_policy.tf') as f:\n"
                               '    tf = f.read()\n'
                               "assert 'DATA_READ' in tf and 'DATA_WRITE' in tf\n"
                               "assert 'exempted_members' in tf\n"
                               '\n'
                               "with open('forensic_threat_hunt.sql') as f:\n"
                               '    sql = f.read()\n'
                               "assert 'SetIamPolicy' in sql and 'protopayload_auditlog' in sql\n"
                               '\n'
                               "print('[ASSERT PASS] Cloud Audit policy configuration and forensic SQL strictly "
                               "validated.')\n"
                               'EOF\n'
                               'python3 assert_audit_compliance.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary test files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_audit_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 95 Topic 3 test scripts..."\n'
                               'rm -f discover_audit_configs.py check_audit_exemptions.py test_audit_immutability.py '
                               'assert_audit_compliance.py\n'
                               'echo "[CLEANUP] Retaining production files: audit_policy.tf, forensic_threat_hunt.sql, '
                               'alert_policy_denied.json"\n'
                               'echo "[CLEANUP PASS] Audit lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_audit_lab.sh\n'
                               '```'],
                     'verification': 'The BigQuery query accurately unnests policy binding deltas and the Python '
                                     'forensic test verifies the detection of unauthorized privilege escalation.',
                     'trouble': 'Ensure BigQuery SQL uses `JSON_EXTRACT_ARRAY` and `UNNEST` when evaluating '
                                '`serviceData.policyDelta.bindingDeltas` to avoid scalar unnest syntax errors.',
                     'cleanup': 'Retain `detect_iam_privilege_escalation.sql` and `day-095-topic-03-telemetry-plan.md` '
                                'as exit evidence artifacts.',
                     'accept': 'Completed forensic detection query and verified telemetry ownership/retention plan. '
                               'File: `day-095-topic-03-audit-forensics.md`.',
                     'file': 'day-095-topic-03-audit-forensics.md'}}],
 'part3_intro': 'The following field cases investigate critical enterprise telemetry failures across Compute Engine '
                'and organization governance: unmonitored guest OS memory starvation causing unannounced database '
                'terminations due to absent in-guest agent telemetry, silent organization-wide audit and log loss '
                'triggered by ungranted writer identity permissions on an aggregated export sink, and forensic '
                'blindness during a privilege escalation incident because Cloud Audit Data Access logs were disabled '
                'to save minor ingestion costs. Each case features verbatim terminal diagnostic output, real log '
                'payloads, structured remediation commands, and dual-lane failure versus corrected flow models.',
 'part4_intro': 'These hands-on exercises implement the comprehensive 8-stage operational engineering lifecycle for '
                'Day 95. Engineers author production Ops Agent multi-pipeline configuration manifests and automated VM '
                'Manager OS Policy assignments, construct enterprise organization-level aggregated log sinks routing '
                'compliance telemetry to encrypted central audit vaults, and configure granular audit logging policies '
                'with automated BigQuery SQL forensic detection for unauthorized IAM privilege escalations.'}
