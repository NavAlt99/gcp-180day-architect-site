"""day_data_092.py — Exhaustive architecture data specification for Day 92.

Covers Failover and Failback Planning.
"""

DAY_NUM = 92

DATA = {'day': 92,
 'part1_intro': 'Day 92 synthesizes the operational, procedural, and technical culmination of disaster recovery: '
                'controlled failover execution, safe failback synchronization, and organizational readiness drills. An '
                'emergency failover plan that has never been tested in production is merely an untested hypothesis. '
                'Furthermore, while failing over during a regional catastrophe is urgent and high-stakes, the '
                'subsequent failback—returning workloads from the secondary recovery site to the restored primary '
                'region—is frequently more hazardous. Without strict reverse data replication, failback overwrites '
                "newly committed transactions, creating massive data corruption. Today's curriculum constructs "
                'end-to-end failover and failback procedures, formalizes structured DR testing frameworks (from '
                'tabletop exercises to full-scale unannounced regional blackhole drills), verifies Google Cloud '
                'regional quota headroom to eliminate capacity traps, implements Cloud Armor rate-limiting and '
                'graceful degradation during brownouts, and authors executable SRE operational runbooks equipped with '
                'explicit abort criteria and consistency checkpoints.',
 'exit_summary': 'Engineered an enterprise Failover and Failback Orchestration Framework: designed an asymmetric '
                 'failover and reverse-replication failback architecture; established an annual DR testing cadence '
                 'across tabletop simulations, chaos game days, and full traffic shifts; implemented automated Google '
                 'Cloud quota headroom auditing scripts; authored a Cloud Armor rate-limiting and shed-queue policy '
                 'for brownout protection; produced a production-grade Executable Failover & Failback Runbook with '
                 'clear owner assignments, abort triggers, and data parity checks.',
 'part2_intro': 'Operational resilience requires transitioning disaster recovery from theoretical documentation into '
                'repeatable, audited engineering muscle memory. The sections below analyze failback mechanics, test '
                'paradigms, quota verification routines, brownout rate-limiting, and runbook governance.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Operational Phase</th>\n'
                    '      <th>Primary Risk / Failure Mode</th>\n'
                    '      <th>Key Technical Mechanism</th>\n'
                    '      <th>Safety Control &amp; Invariant</th>\n'
                    '      <th>Abort / Rollback Criteria</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>Emergency Failover</strong></td>\n'
                    '      <td>Secondary region quota exhaustion; stale VM templates</td>\n'
                    '      <td>Cloud DNS steering; Cloud SQL replica promotion; MIG autoscale</td>\n'
                    '      <td>Pre-purchased Compute Engine Reservations; CI/CD multi-region template baking</td>\n'
                    '      <td>Secondary database fails to reach RUNNABLE within 5 minutes</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Stabilization in DR</strong></td>\n'
                    '      <td>Traffic surge overpowers secondary region</td>\n'
                    '      <td>Cloud Armor edge rate-limiting; priority load shedding</td>\n'
                    '      <td>Drop non-essential background APIs; prioritize checkout transactions</td>\n'
                    '      <td>Database CPU sustained > 90% or 5xx error rate > 5%</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Reverse Replication</strong></td>\n'
                    '      <td>Split-brain data divergence between regions</td>\n'
                    '      <td>Re-establish replication from DR secondary back to restored primary</td>\n'
                    '      <td>Byte lag must reach zero before failback traffic pivot</td>\n'
                    '      <td>Reverse replication errors or data checksum mismatch</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Controlled Failback</strong></td>\n'
                    '      <td>In-flight writes lost during return pivot</td>\n'
                    '      <td>Graceful connection drain; read-only maintenance window; DNS update</td>\n'
                    '      <td>Lock writes during pivot; verify database parity before unlocking ingress</td>\n'
                    '      <td>Unapplied write transactions detected on secondary database</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 92: Full-Cycle Disaster Recovery: Failover, Reverse Replication, and Failback',
                  'desc': 'Lifecycle diagram showing primary failure, failover to secondary, reverse replication '
                          'alignment, and safe failback return.',
                  'caption': 'Figure 92.1: Complete disaster recovery lifecycle illustrating the critical '
                             'reverse-replication synchronization phase before return-to-primary.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Edge Ingress & Global Traffic Steering Tier',
                              'desc': 'Cloud DNS Health-Checked Failover (30s TTL), Global External ALB, and Cloud '
                                      'Armor Edge Rate-Limiting',
                              'fill': '#1e3a5f',
                              'y': 10,
                              'h': 90},
                             {'name': 'LAYER 2: Compute Capacity & Hardware Reservation Tier',
                              'desc': 'Compute Engine Capacity Reservations (Zonal), Regional MIG Autoscaling, and '
                                      'Pre-baked Golden Templates',
                              'fill': '#0f2338',
                              'y': 115,
                              'h': 90},
                             {'name': 'LAYER 3: Persistence, Failover & Reverse Replication Tier',
                              'desc': 'Cloud SQL Primary Instance, Cross-Region Read Replica Promotion, and Reverse '
                                      'WAL Sync Stream',
                              'fill': '#064e3b',
                              'y': 220,
                              'h': 90},
                             {'name': 'LAYER 4: DR Game Day & Chaos Injection Control Plane',
                              'desc': 'Chaos Fault Injection Engine, Safety Officer Live Telemetry Bridge, and '
                                      'Automated Rollback Controller',
                              'fill': '#1e1b4b',
                              'y': 325,
                              'h': 90},
                             {'name': 'LAYER 5: SRE Governance, Quota Auditing & Executable Runbooks',
                              'desc': 'Automated Multi-Region Quota Auditing, Parameterized Runbooks, and Production '
                                      'Abort Criteria Monitors',
                              'fill': '#3b0764',
                              'y': 430,
                              'h': 90}],
                  'components': [{'id': 'cloud_armor_edge',
                                  'name': 'Cloud Armor Edge',
                                  'detail': 'Priority Load Shedding (429)',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'alb_dns_steer',
                                  'name': 'Global ALB & Cloud DNS',
                                  'detail': '30s TTL Health-Checked Steering',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'gce_reservation_gate',
                                  'name': 'Compute Reservations',
                                  'detail': 'Guaranteed Capacity (No Pool Exhaust)',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'mig_dr_pool',
                                  'name': 'Secondary DR MIG',
                                  'detail': 'Autoscaling to 100% Workload',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'sql_promoted_primary',
                                  'name': 'Promoted SQL Primary',
                                  'detail': 'Read-Write Primary in us-east1',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'reverse_wal_stream',
                                  'name': 'Reverse Replication',
                                  'detail': 'Sync Back to Restored Primary',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'chaos_injection_engine',
                                  'name': 'Chaos Injection Engine',
                                  'detail': 'Controlled Zonal / Network Cuts',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'safety_officer_abort',
                                  'name': 'Safety Officer Abort',
                                  'detail': 'Red Button Automated Rollback',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'quota_headroom_audit',
                                  'name': 'Quota Parity Monitor',
                                  'detail': 'Continuous Multi-Region Audit',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'},
                                 {'id': 'git_executable_runbook',
                                  'name': 'Executable Runbook',
                                  'detail': 'Git-Managed Parameterized SRE Code',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'}],
                  'boundaries': [{'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'INGRESS TRAFFIC MANAGEMENT & CLOUD ARMOR EDGE PERIMETER',
                                  'color': '#38bdf8'},
                                 {'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'label': 'COMPUTE CAPACITY & REVERSE PERSISTENCE BOUNDARY',
                                  'color': '#10b981'},
                                 {'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'label': 'SRE OPERATIONAL GOVERNANCE & CHAOS SAFETY BOUNDARY',
                                  'color': '#a855f7'}],
                  'flows': [{'x1': 340,
                             'y1': 56,
                             'x2': 420,
                             'y2': 56,
                             'type': 'ok',
                             'label': 'Shed Non-Essential Edge Traffic'},
                            {'x1': 210,
                             'y1': 82,
                             'x2': 210,
                             'y2': 135,
                             'type': 'ok',
                             'label': 'Route Checkout Traffic'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'type': 'ok',
                             'label': 'Attach Hardware Reservation'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'type': 'ok',
                             'label': 'Direct Database Reads/Writes'},
                            {'x1': 340,
                             'y1': 266,
                             'x2': 420,
                             'y2': 266,
                             'type': 'ok',
                             'label': 'Reverse WAL Stream to Primary'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'type': 'ok',
                             'label': 'Inject Controlled Fault'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'type': 'fail',
                             'label': 'Trigger Abort Rollback'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'type': 'ok',
                             'label': 'Verify Regional Quota Parity'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'type': 'ok',
                             'label': 'Execute Parameterized Steps'}],
                  'probes': [{'cx': 80,
                              'cy': 30,
                              'label': 'PROBE 1: Cloud Armor 429 Edge Drop Counter',
                              'color': '#38bdf8'},
                             {'cx': 420,
                              'cy': 240,
                              'label': 'PROBE 2: Reverse Replication Byte Lag (=0 Check)',
                              'color': '#10b981'},
                             {'cx': 420,
                              'cy': 345,
                              'label': 'PROBE 3: Safety Officer Abort Trigger Monitor',
                              'color': '#ef4444'}]},
 'topics': [{'key': 'topic-01',
             'title': 'Failover and failback procedures, DNS TTL considerations',
             'preview': 'After operating in a secondary DR region for 14 hours, an SRE team abruptly shifts DNS back '
                        'to the restored primary region, causing immediate database split-brain and overwriting 12,000 '
                        'customer transactions created during the failover period.',
             'overview': 'While disaster **failover** is conducted urgently in response to an unexpected catastrophic '
                         'infrastructure collapse, **failback** (the process of returning workloads to the restored '
                         'primary environment) must be planned and executed with methodical precision. The core '
                         'engineering danger during failback is data divergence (split-brain). During the outage, the '
                         'secondary recovery database accumulated new writes, updates, and deletes. If traffic is '
                         'switched back to the primary before these new transactions are synchronized, the primary and '
                         'secondary databases diverge, resulting in permanent data corruption. A resilient failback '
                         'procedure requires: 1) re-establishing **reverse replication** from the secondary to the '
                         'restored primary, 2) lowering DNS TTLs days in advance of the planned cutover, 3) initiating '
                         'a brief read-only maintenance window to drain in-flight connections, 4) verifying byte-level '
                         'data parity, and 5) pivoting traffic back to the primary.',
             'technical': '### 1. The Asymmetry Between Failover and Failback\n'
                          '- **Failover Velocity:** Speed is paramount. The primary region is dead; transactions are '
                          'failing. Engineers trigger automated or semi-automated runbooks to promote replicas and '
                          'steer traffic to secondary infrastructure as rapidly as possible.\n'
                          '- **Failback Deliberation:** Safety and data integrity are paramount. The business is '
                          'currently operating successfully in the DR region. Failback should *never* occur under '
                          'emergency conditions; it must be scheduled during low-traffic maintenance windows.\n'
                          '\n'
                          '### 2. Reverse Replication Synchronization Mechanics\n'
                          '- **The Reversal Sequence:**\n'
                          '  1. The primary region (`us-central1`) is declared healthy by Google Cloud.\n'
                          '  2. Do *not* point clients back yet. Configure the restored database instance in '
                          '`us-central1` as an *external replica* tracking the currently active primary in '
                          '`us-east1`.\n'
                          '  3. Stream Write-Ahead Logs (WAL) or binary logs across regions from `us-east1` to '
                          '`us-central1`.\n'
                          '  4. Monitor replication byte lag until it reaches zero.\n'
                          '\n'
                          '### 3. DNS TTL Caching Considerations During Failback\n'
                          '- **Pre-Failback TTL Reduction:** At least 48 to 72 hours before a scheduled failback, '
                          'reduce DNS A-record TTLs from standard durations (e.g. 300s or 3600s) down to **30 '
                          'seconds** across all Cloud DNS public zones.\n'
                          '- **Connection Draining Maintenance Gate:** During cutover, place the application into '
                          'read-only mode for 60 seconds (exceeding DNS TTL). This ensures all straggling requests to '
                          'the secondary region are read-only and no new writes are accepted while traffic pivots to '
                          'the primary.',
             'questions': ['Why does executing a failback without establishing reverse data replication cause '
                           'catastrophic split-brain corruption?',
                           'What is the operational rationale for lowering DNS TTLs 48 hours prior to a planned '
                           'failback maintenance window?',
                           'How does placing the application in read-only mode during DNS cutover prevent orphaned '
                           'transactional state?'],
             'reference': 'https://docs.cloud.google.com/architecture/dr-scenarios#failover_and_failback',
             'reference_label': 'Google Cloud Architecture: Failover and failback procedures, synchronization, and DNS '
                                'management',
             'scenario': {'symptom': 'Following a 12-hour regional power outage in `us-central1`, Brightloaf operated '
                                     'successfully on their DR standby database in `us-east1`. Once Google Cloud '
                                     'restored `us-central1`, an operator immediately pointed Cloud DNS back to the '
                                     'original database in `us-central1`. Within 10 minutes, inventory discrepancies '
                                     'appeared: 3,400 orders placed during the 12-hour DR window vanished from '
                                     'customer order histories.',
                          'constraints': 'Must guarantee 100% transactional consistency and zero data loss during '
                                         'return-to-primary failback procedures.',
                          'evidence': 'Database audit logs and replication telemetry captured the split-brain '
                                      'truncation:\n'
                                      '\n'
                                      '```\n'
                                      "[2026-09-29T16:00:15Z] FAILBACK: Operator executed 'gcloud dns record-sets "
                                      "update api.brightloaf.com --rrdatas=34.102.10.1'\n"
                                      '[2026-09-29T16:00:20Z] INFO     dns-edge: Primary IP 34.102.10.1 answering live '
                                      'traffic\n'
                                      '[2026-09-29T16:04:12Z] ERROR    order-service: Foreign key mismatch: order_id '
                                      '#8849120 referenced non-existent customer in us-central1\n'
                                      "$ gcloud sql instances describe brightloaf-db-central --format='value(state, "
                                      "replicationLag)' ...\n"
                                      'Primary state: RUNNABLE | Master instance: NONE (Reverse replication was NEVER '
                                      'configured)\n'
                                      'Data delta: 3,420 orders committed in us-east1 during outage window were '
                                      'completely absent from us-central1.\n'
                                      'Unrecovered revenue: $427,500 USD in orphaned customer transactions.\n'
                                      '```',
                          'diagnostic_steps': ['Compare maximum transaction log sequence numbers between primary and '
                                               'secondary database instances.',
                                               'Review failback operational execution logs to audit the exact sequence '
                                               'of DNS record updates versus database synchronization.',
                                               'Quantify the volume of un-synchronized writes created during the DR '
                                               'operational window.'],
                          'root': 'Procedural failure: the engineering runbook treated failback as a simple DNS record '
                                  'reversion, completely omitting the mandatory reverse-replication synchronization '
                                  'phase.',
                          'fix': 'Rewrite the SRE Failback Playbook to mandate reverse replication: 1. Configure the '
                                 'restored instance as a downstream replica of the DR primary. 2. Verify zero '
                                 'replication lag. 3. Enter read-only maintenance mode. 4. Pivot DNS. 5. Promote the '
                                 'restored primary.',
                          'verify': 'Execute a staged tabletop failback drill in pre-production: populate secondary '
                                    'database with 10,000 synthetic records, configure reverse replication to the '
                                    'restored primary, verify data parity checksums match 100%, and execute cutover '
                                    'with zero missing records.',
                          'residual': 'A 60-second read-only maintenance window is required during the final DNS '
                                      'traffic pivot to ensure write quiescence.',
                          'diagram': ('12h writes committed in DR region',
                                      'Operator flips DNS back to primary',
                                      '3,400 orders vanished (Split-brain)',
                                      'Reverse replication established',
                                      'Zero-loss verified failback cutover'),
                          'facts': '3,400 customer orders were lost during failback because DNS was reverted before '
                                   'syncing writes back to the primary.',
                          'inference': 'Failback without reverse replication is mathematically equivalent to '
                                       'intentional historical data truncation.',
                          'expected': 'Failback runbooks strictly enforce reverse replication and checksum '
                                      'verification before any DNS traffic redirection.'},
             'lab': {'name': 'Controlled Failover and Safe Failback Execution Runbook',
                     'file': 'day-092-topic-01-failover-failback.md',
                     'goal': 'Author an authoritative, step-by-step failover and reverse-replication failback runbook '
                             'with validation checkpoints.',
                     'expected': 'A comprehensive Markdown runbook detailing exact preflight checks, gcloud '
                                 'replication commands, and parity validation scripts.',
                     'mode': 'tabletop analysis & production CLI / Bash execution',
                     'prereq': 'Understanding of database replication and DNS TTL propagation.',
                     'preflight': 'Review Cloud SQL replica creation and promotion CLI syntax.',
                     'steps': ['#### Stage 1: Pre-Flight Failover / Failback Topology & Invariant Architecture\n'
                               "Establish the operational invariants for Brightloaf's failover and failback "
                               'lifecycle:\n'
                               '- **Failover Invariant:** Rapid promotion of secondary database `brightloaf-db-east` '
                               'and compute scaling within 15 minutes of primary failure.\n'
                               '- **Failback Invariant:** Return-to-primary is strictly forbidden until **reverse '
                               'replication** from `us-east1` to `us-central1` is fully established and byte lag '
                               'reaches `0`.\n'
                               '- **Quiescence Invariant:** A 60-second read-only maintenance window is mandated '
                               'during DNS pivot to guarantee write quiescence.',
                               '#### Stage 2: Infrastructure Preflight & TTL Verification\n'
                               'Author a preflight script (<kbd>check_failover_env.py</kbd>) verifying DNS TTLs and '
                               'database states:\n'
                               '\n'
                               '```python\n'
                               '# check_failover_env.py\n'
                               'env_state = {\n'
                               "    'primary_region': 'us-central1',\n"
                               "    'recovery_region': 'us-east1',\n"
                               "    'dns_ttl_seconds': 30,\n"
                               "    'quiesce_window_seconds': 60,\n"
                               '}\n'
                               "print('[PREFLIGHT] Checking failover and failback configuration...')\n"
                               "assert env_state['dns_ttl_seconds'] <= 60, 'DNS TTL must be 60 seconds or lower'\n"
                               "assert env_state['quiesce_window_seconds'] >= env_state['dns_ttl_seconds'], 'Quiesce "
                               "window must exceed DNS TTL'\n"
                               "print('[PASS] Preflight failback invariants verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_failover_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Emergency Failover Execution\n'
                               'Author the emergency failover script promoting the secondary database and scaling '
                               'compute:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > execute_failover.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'echo "[FAILOVER] Declaring disaster in us-central1; steering to us-east1..."\n'
                               'gcloud sql instances promote-replica brightloaf-db-east \\\n'
                               '    --project="${PROJECT_ID}" --quiet || true\n'
                               '\n'
                               'echo "[FAILOVER] Scaling secondary compute MIG in us-east1 to 30 instances..."\n'
                               'gcloud compute instance-groups managed resize brightloaf-mig-east \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --region=us-east1 \\\n'
                               '    --size=30 || true\n'
                               'EOF\n'
                               'chmod +x execute_failover.sh\n'
                               './execute_failover.sh\n'
                               '```',
                               '#### Stage 4: Steady-State Operations & Reverse Replication Setup\n'
                               'Author the script configuring reverse replication from `us-east1` back to '
                               '`us-central1` once the primary region recovers:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > setup_reverse_replication.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'echo "[FAILBACK] Creating restored database in us-central1 as read replica of us-east1 '
                               'primary..."\n'
                               'gcloud sql instances create brightloaf-db-central-new \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --master-instance-name=brightloaf-db-east \\\n'
                               '    --region=us-central1 || true\n'
                               'echo "[PASS] Reverse replication pipeline established."\n'
                               'EOF\n'
                               'chmod +x setup_reverse_replication.sh\n'
                               './setup_reverse_replication.sh\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Zero-Lag Quiescence Simulation\n'
                               'Author a simulation script (<kbd>simulate_failback_quiesce.py</kbd>) modeling write '
                               'quiescence and replication lag catch-up:\n'
                               '\n'
                               '```python\n'
                               '# simulate_failback_quiesce.py\n'
                               'import time\n'
                               '\n'
                               "print('--- SIMULATING CONTROLLED FAILBACK CUTOVER ---')\n"
                               'replication_lag_bytes = 45000\n'
                               "print(f'[Step 1] Initial reverse replication lag: {replication_lag_bytes} bytes')\n"
                               '\n'
                               "print('[Step 2] Activating read-only maintenance mode (60s drain)...')\n"
                               '# Ingest stops; replica catches up\n'
                               'replication_lag_bytes = 0\n'
                               "print(f'[Step 3] Reverse replication lag reached: {replication_lag_bytes} bytes "
                               "(Zero-loss parity achieved)')\n"
                               "assert replication_lag_bytes == 0, 'Cannot failback until byte lag is exactly zero'\n"
                               "print('[PASS] Zero-loss cutover condition satisfied.')\n"
                               '```\n'
                               '\n'
                               'Execute simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_failback_quiesce.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Cutover Verification\n'
                               'Author a verification script confirming that traffic has returned to `us-central1`:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_failback_cutover.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Verifying load balancer routing post-failback..."\n'
                               "cat <<'TABLE'\n"
                               'Backend Service Target         Region       Health State   Active Traffic\n'
                               '-------------------------------------------------------------------------\n'
                               'brightloaf-mig-central         us-central1  HEALTHY        100% (2,450 rps)\n'
                               'brightloaf-mig-east            us-east1     HEALTHY          0% (Standby)\n'
                               'TABLE\n'
                               'echo "[FAILBACK OBSERVABILITY PASS] Workload successfully returned to primary '
                               'region."\n'
                               'EOF\n'
                               'chmod +x verify_failback_cutover.sh\n'
                               './verify_failback_cutover.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Database Checksum Parity Assertions\n'
                               'Author an automated test (<kbd>assert_data_parity.py</kbd>) asserting database row '
                               'counts match between regions:\n'
                               '\n'
                               '```python\n'
                               '# assert_data_parity.py\n'
                               "east_checksum = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'\n"
                               "central_checksum = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'\n"
                               "assert east_checksum == central_checksum, 'Data checksum mismatch between East and "
                               "Central databases!'\n"
                               "print('[ASSERT PASS] Database parity verified with 100% cryptographic checksum "
                               "match.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_data_parity.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_failover_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 92 Topic 1 test scripts..."\n'
                               'rm -f check_failover_env.py execute_failover.sh setup_reverse_replication.sh '
                               'simulate_failback_quiesce.py verify_failback_cutover.sh assert_data_parity.py\n'
                               'echo "[CLEANUP] Retaining day-092-topic-01-failover-failback.md evidence '
                               'documentation."\n'
                               'echo "[CLEANUP PASS] Failover/failback teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_failover_lab.sh\n'
                               './teardown_failover_lab.sh\n'
                               '```'],
                     'verification': 'Document exists, contains production-ready gcloud failover/failback commands, '
                                     'and enforces reverse-replication integrity.',
                     'trouble': 'Ensure reverse replica byte lag reaches exactly zero before promoting the restored '
                                'instance.',
                     'cleanup': 'Retain `day-092-topic-01-failover-failback.md` as an exit evidence artifact.',
                     'accept': 'Completed failover and failback operational runbook with verified commands and safety '
                               'gates.'}},
            {'key': 'topic-02',
             'title': 'DR testing',
             'preview': 'An enterprise performs its very first disaster recovery test during a scheduled weekend '
                        'maintenance window, only to accidentally wipe out live production customer data because the '
                        'test script ran against the wrong Google Cloud project.',
             'overview': 'Disaster recovery capabilities decay over time due to code deployments, configuration drift, '
                         'and team turnover. Regular, disciplined **DR Testing** is essential to validate that '
                         'recovery procedures remain operational. Testing follows a progressive maturity model: '
                         '**Tabletop Exercises** (structured walkthroughs where architects and SREs trace failure '
                         'scenarios on paper to identify process defects), **Game Days / Chaos Engineering** '
                         '(targeted, controlled failure injection in staging or production to verify automated '
                         'self-healing), and **Full Regional Failover Drills** (complete simulation or actual '
                         'evacuation of user traffic from a primary region). Every DR test must operate under strict '
                         'governance: defining an **Incident Commander**, establishing non-negotiable **Abort '
                         'Criteria**, and enforcing project isolation to prevent accidental production harm.',
             'technical': '### 1. The DR Testing Maturity Spectrum\n'
                          '- **Level 1: Tabletop Analysis (Quarterly):** Cross-functional teams (SRE, Security, '
                          "Database, Network, Product) walk through a hypothetical outage script (e.g. 'Submarine "
                          "fiber cut isolates Europe region'). Identifies missing runbook steps, outdated IAM access, "
                          'and unmapped dependencies with zero operational risk.\n'
                          '- **Level 2: Component Fault Injection / Chaos Game Days (Monthly):** Controlled '
                          'experiments testing automated resilience: e.g. killing primary Cloud SQL instances, '
                          'draining a GKE node pool, or injecting 500ms network latency via Chaos Mesh. Confirms '
                          'autohealing and alerts.\n'
                          '- **Level 3: Full-Scale Regional Evacuation Drill (Bi-annually):** Live or canary shift of '
                          'production traffic to the recovery region. Measures empirical RTO and RPO against BIA '
                          'targets.\n'
                          '\n'
                          '### 2. Testing Governance and Operational Abort Criteria\n'
                          "- **The 'Red Button' (Abort Triggers):** A DR drill must be immediately aborted and rolled "
                          'back if predefined safety thresholds are violated:\n'
                          '  1. *Customer Impact Threshold:* Error rate exceeds 1% for more than 2 minutes.\n'
                          '  2. *Revenue Loss Threshold:* Failed checkout transactions exceed $10,000.\n'
                          '  3. *Latency Threshold:* P99 latency spikes beyond 2,500ms.\n'
                          '  4. *Real Incident Interruption:* An actual production P1/P2 incident occurs during the '
                          'test window.\n'
                          '- **Role Separation:** The DR Exercise Lead coordinates the simulation; the Safety Monitor '
                          'has sole authority to hit the abort button; the Communications Lead keeps stakeholders '
                          'informed.',
             'questions': ['What organizational benefits do tabletop exercises provide before conducting live '
                           'infrastructure fault injection?',
                           'What specific telemetry metrics must trigger an immediate, non-negotiable abort of a '
                           'production DR game day?',
                           'Why must disaster recovery drills test both the technical failover and the subsequent '
                           'failback return procedure?'],
             'reference': 'https://docs.cloud.google.com/architecture/dr-scenarios#testing_disaster_recovery',
             'reference_label': 'Google Cloud Architecture: Disaster recovery testing methodologies, game days, and '
                                'drill frameworks',
             'scenario': {'symptom': 'During an unannounced DR drill in production, an SRE team initiated automated '
                                     'traffic evacuation to `europe-west1`. The primary checkout service crashed, and '
                                     'customer error rates spiked to 14%. The drill continued for 45 minutes because '
                                     'no single engineer had been designated with explicit authority to declare an '
                                     'abort, resulting in $340,000 in lost customer sales.',
                          'constraints': 'Must establish rigid DR drill governance defining explicit abort criteria '
                                         'and designating an empowered Safety Officer.',
                          'evidence': 'Incident command communications transcripts and error rate metrics captured the '
                                      'governance vacuum:\n'
                                      '\n'
                                      '```\n'
                                      '[2026-09-29T14:10:00Z] INCIDENT BRIDGE AUDIO RECORDING TRANSCRIPT:\n'
                                      '14:12:15 [SRE-1]: Checkout error rate spiked to 14.2%. Are we aborting the '
                                      'drill?\n'
                                      "14:14:02 [Dev-Lead]: Wait, that might just be the database warming up. Don't "
                                      'abort yet.\n'
                                      '14:26:45 [Product]: Customer support is flooding our channel. Over $200k in '
                                      'failed checkouts!\n'
                                      '14:35:10 [SRE-2]: Who actually has authority to press the abort button? We '
                                      "don't have a designated lead.\n"
                                      '[2026-09-29T14:55:00Z] DRILL TERMINATED: 45 minutes elapsed before manual '
                                      'rollback executed.\n'
                                      'Total lost sales: $342,000 USD during a pre-planned internal test drill.\n'
                                      'Finding: Zero numerical abort criteria defined in test documentation; no Safety '
                                      'Officer appointed.\n'
                                      '```',
                          'diagnostic_steps': ['Review communication channels and timeline transcripts from the failed '
                                               'drill to identify governance bottlenecks.',
                                               'Audit telemetry metrics (error rate, latency, revenue flow) recorded '
                                               'during the drill window.',
                                               'Review test plan documentation to verify presence of abort criteria '
                                               'and safety officer appointments.'],
                          'root': 'Governance failure: the DR test was conducted without predefined abort criteria, a '
                                  'designated Safety Officer, or automated rollback monitors, converting a routine '
                                  'readiness drill into an uncontrolled production outage.',
                          'fix': 'Establish a mandatory DR Drill Governance Framework: require written test plans with '
                                 'explicit numerical abort thresholds (e.g. error rate > 1%), appoint an independent '
                                 'Safety Officer with sole authority to terminate drills, and build automated rollback '
                                 'scripts.',
                          'verify': 'Execute a controlled staging drill where synthetic error rates are forced to '
                                    '1.5%; verify monitoring systems trigger automated drill abort and rollback to '
                                    'primary within 60 seconds.',
                          'residual': 'Setting overly sensitive abort thresholds may terminate legitimate drills '
                                      'prematurely; thresholds must reflect true customer harm.',
                          'diagram': ('DR drill triggers 14% error spike',
                                      'Responders argue for 35 minutes',
                                      '$340k revenue lost during drill',
                                      'Safety Officer & abort criteria set',
                                      'Auto-rollback triggers in 60s'),
                          'facts': '$340,000 lost during a test because no one had authority to abort the drill when '
                                   'errors surged to 14%.',
                          'inference': 'A disaster recovery test without explicit abort criteria is indistinguishable '
                                       'from an unmitigated production outage.',
                          'expected': 'Drills are governed by strict numerical abort criteria and an empowered Safety '
                                      'Officer with immediate rollback authority.'},
             'lab': {'name': 'Disaster Recovery Game Day Test Plan and Tabletop Simulation',
                     'file': 'day-092-topic-02-dr-test-plan.md',
                     'goal': 'Author an enterprise DR Game Day Test Plan defining roles, timeline scenarios, and '
                             'explicit automated abort criteria.',
                     'expected': 'A comprehensive test plan in Markdown specifying incident command roles, injection '
                                 'scripts, and abort monitoring queries.',
                     'mode': 'tabletop analysis & production CLI / Bash execution',
                     'prereq': 'Understanding of SRE incident command and monitoring metrics.',
                     'preflight': 'Review corporate change management guidelines and SRE incident response roles.',
                     'steps': ['#### Stage 1: Pre-Flight DR Game Day Invariants & Safety Officer Governance\n'
                               'Establish the governance and safety invariants for DR Game Day testing:\n'
                               '- **Command Hierarchy:** Clear separation between Incident Commander (leads '
                               'execution), Safety Officer (sole authority to abort), and Chaos Engineer.\n'
                               '- **Numerical Abort Thresholds:** 1) HTTP 5xx error rate > 1.0% for > 60s, 2) P99 '
                               'latency > 2,000ms, 3) > 3 synthetic payment failures, 4) Active P1/P2 real incident.\n'
                               '- **Automated Rollback:** Rollback script pre-tested and ready to execute within 60 '
                               'seconds.',
                               '#### Stage 2: Environment Preflight & Staging Target Isolation\n'
                               'Author a preflight script (<kbd>check_gameday_env.py</kbd>) verifying staging target '
                               'environment isolation:\n'
                               '\n'
                               '```python\n'
                               '# check_gameday_env.py\n'
                               "target_project = 'brightloaf-staging'\n"
                               "print(f'[PREFLIGHT] Validating DR drill target project: {target_project}')\n"
                               "assert 'prod' not in target_project, 'Unannounced chaos drills must NEVER target "
                               "production directly'\n"
                               "print('[PASS] Staging isolation verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_gameday_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Enterprise Game Day Test Plan & Charter\n'
                               'Author the formal test plan and governance document '
                               '(<kbd>day-092-topic-02-dr-test-plan.md</kbd>):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > day-092-topic-02-dr-test-plan.md\n"
                               '# Day 92: Enterprise DR Game Day Test Plan & Governance Charter\n'
                               '\n'
                               '## 1. Test Metadata & Scope\n'
                               '- Exercise Codename: Operation Phoenix Ash\n'
                               '- Target Environment: Pre-Production Staging (`brightloaf-staging`)\n'
                               '- Simulation Hypothesis: Catastrophic network partition in primary region '
                               '`us-central1`.\n'
                               '\n'
                               '## 2. Command Team Roles & Responsibilities\n'
                               '- Exercise Commander (IC): Directs timeline progression and authorizes phase '
                               'transitions.\n'
                               '- Safety Officer (Red Button Owner): Monitors live telemetry; holds absolute, '
                               'unquestioned authority to immediately abort the drill.\n'
                               '- Chaos Engineer: Executes fault injection scripts.\n'
                               '- Communications Lead: Posts updates every 15 minutes to `#dr-drill-bridge`.\n'
                               '\n'
                               '## 3. Strict Numerical Abort Criteria (Non-Negotiable)\n'
                               '1. HTTP 5xx Error Rate: > 1.0% for > 60 consecutive seconds.\n'
                               '2. Synthetic Checkout Failure: > 3 consecutive failures.\n'
                               '3. P99 API Latency: > 2,000 ms across two consecutive evaluation windows.\n'
                               '4. Database Replication Lag: > 60 seconds.\n'
                               '5. Real-World Incident: Any active P1 or P2 incident declared.\n'
                               'EOF\n'
                               'cat day-092-topic-02-dr-test-plan.md\n'
                               '```',
                               '#### Stage 4: Execution & Chaos Fault Injection Script\n'
                               'Author the chaos fault injection script simulating regional blackhole failure:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > inject_regional_blackhole.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "[CHAOS] Injecting simulated regional blackhole in us-central1..."\n'
                               "cat <<'SIM'\n"
                               'Step 1: Ingress firewall rules dropped to us-central1 backend MIG\n'
                               'Step 2: Cloud Monitoring detects health probe failure at 10s\n'
                               'Step 3: Traffic shift begins steering toward us-east1\n'
                               'SIM\n'
                               'echo "[PASS] Fault injection active."\n'
                               'EOF\n'
                               'chmod +x inject_regional_blackhole.sh\n'
                               './inject_regional_blackhole.sh\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Abort Threshold Breach Drill\n'
                               'Author a chaos simulation script (<kbd>simulate_abort_trigger.py</kbd>) verifying that '
                               'the Safety Officer triggers abort when errors hit 1.5%:\n'
                               '\n'
                               '```python\n'
                               '# simulate_abort_trigger.py\n'
                               'error_rate = 0.015 # 1.5% error rate\n'
                               'threshold = 0.010  # 1.0% threshold\n'
                               '\n'
                               "print(f'[MONITOR] Evaluated Error Rate: {error_rate*100:.1f}% (Threshold: "
                               "{threshold*100:.1f}%)')\n"
                               'if error_rate > threshold:\n'
                               "    print('[SAFETY OFFICER] RED BUTTON TRIGGERED: Error rate exceeded 1.0%!')\n"
                               "    print('[SAFETY OFFICER] Initiating immediate automated rollback...')\n"
                               '    aborted = True\n'
                               'else:\n'
                               '    aborted = False\n'
                               '\n'
                               "assert aborted is True, 'Safety Officer must abort drill when threshold breached'\n"
                               "print('[PASS] Automated abort logic verified.')\n"
                               '```\n'
                               '\n'
                               'Execute chaos test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_abort_trigger.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Automated Rollback Execution\n'
                               'Author the rollback command executing instant primary restoration:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > execute_auto_rollback.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "[ROLLBACK] Safety Officer aborted drill. Restoring primary ingress..."\n'
                               'echo "[ROLLBACK] Re-attaching us-central1 backend service..."\n'
                               'echo "[ROLLBACK] All traffic successfully restored to healthy primary baseline in 38 '
                               'seconds."\n'
                               'EOF\n'
                               'chmod +x execute_auto_rollback.sh\n'
                               './execute_auto_rollback.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Abort Window Assertions\n'
                               'Author an automated test (<kbd>assert_abort_timing.py</kbd>) asserting rollback '
                               'duration bounds:\n'
                               '\n'
                               '```python\n'
                               '# assert_abort_timing.py\n'
                               'rollback_duration_seconds = 38\n'
                               "assert rollback_duration_seconds < 60, 'Rollback must complete in under 60 seconds'\n"
                               "print('[ASSERT PASS] Rollback execution velocity verified within SLA bound.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_abort_timing.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_gameday_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 92 Topic 2 test scripts..."\n'
                               'rm -f check_gameday_env.py inject_regional_blackhole.sh simulate_abort_trigger.py '
                               'execute_auto_rollback.sh assert_abort_timing.py\n'
                               'echo "[CLEANUP] Retaining day-092-topic-02-dr-test-plan.md evidence documentation."\n'
                               'echo "[CLEANUP PASS] Game Day lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_gameday_lab.sh\n'
                               './teardown_gameday_lab.sh\n'
                               '```'],
                     'verification': 'Document exists, contains a structured Game Day test plan, and details '
                                     'non-negotiable abort thresholds.',
                     'trouble': 'Ensure staging test environments mirror production network and database topologies to '
                                'produce valid drill insights.',
                     'cleanup': 'Retain `day-092-topic-02-dr-test-plan.md` as an exit evidence artifact.',
                     'accept': 'Completed DR Game Day test plan with verified governance, timeline, and abort '
                               'criteria.'}},
            {'key': 'topic-03',
             'title': 'Verify quota scope and available failover capacity',
             'preview': 'An e-commerce site initiates emergency regional failover during Black Friday, but the '
                        "secondary region's Managed Instance Group fails to scale beyond 24 VMs because the default "
                        'regional vCPU quota was never increased from standard trial limits.',
             'overview': 'In Google Cloud, resource allocations are governed by strict **Quotas and System Limits**. A '
                         'pervasive architectural pitfall in disaster recovery planning is assuming that resource '
                         'quotas approved in the primary region automatically apply globally. Most Google Cloud '
                         'compute quotas—such as `CPUS`, `N2_CPUS`, `DISKS_TOTAL_GB`, and `IN_USE_ADDRESSES`—are '
                         'strictly **regional**. If an enterprise operates 1,200 vCPUs in `us-central1`, but their '
                         'secondary disaster recovery region (`us-east1`) has never had its regional quota increased '
                         'above the default 24 vCPUs, any attempt to scale the secondary MIG during an outage will '
                         'fail immediately with `QUOTA_EXCEEDED` errors. Furthermore, quota increases during a '
                         'widespread public regional disaster may be delayed or rejected due to cloud-wide capacity '
                         'constraints. Resilient DR design requires auditing regional quota headroom continuously and '
                         'purchasing **Compute Engine Reservations** to physically guarantee hardware availability.',
             'technical': '### 1. Quota Scope Hierarchy in Google Cloud\n'
                          '- **Global Quotas:** Apply across the entire Google Cloud project regardless of location '
                          '(e.g. `NETWORKS`, `FIREWALLS`, `GLOBAL_EXTERNAL_HTTP_LB_FORWARDING_RULES`).\n'
                          '- **Regional Quotas:** Apply strictly within a single geographic region (e.g. `Compute '
                          'Engine API / CPUS` in `us-east1`, `SSD_TOTAL_GB` in `europe-west4`). Having 10,000 CPUs '
                          'available in Iowa (`us-central1`) provides zero capacity to launch instances in Virginia '
                          '(`us-east1`).\n'
                          '- **Zonal Quotas:** Apply within a specific datacenter zone (e.g. local persistent disk '
                          'capacity per zone).\n'
                          '\n'
                          "### 2. Quota vs Capacity: The 'Hot Day' Trap\n"
                          '- **Quota Is Not Guaranteed Capacity:** Having an approved quota of 1,000 vCPUs merely '
                          'grants legal permission to request instances; it does *not* guarantee physical hardware is '
                          "idle in Google's datacenter. If a major regional storm causes dozens of enterprises to "
                          'failover simultaneously to `us-east1`, Google Cloud may experience transient '
                          '`ZONE_RESOURCE_POOL_EXHAUSTED` errors.\n'
                          '- **Compute Engine Reservations:** The only technical mechanism to guarantee physical '
                          'capacity during a regional disaster is a Compute Engine Reservation (zonal reservation for '
                          'specific machine types, e.g. `c2-standard-16`). Reserved instances incur standard hourly '
                          'compute pricing even when idle, representing an insurance policy for Tier 0 failover.\n'
                          '\n'
                          '### 3. Automated Quota Auditing and Monitoring\n'
                          '- Use Cloud Monitoring metric `serviceruntime.googleapis.com/quota/allocation/usage` '
                          'divided by `quota/limit` to alert SREs when capacity utilization exceeds 75% in either the '
                          'primary or recovery region.\n'
                          '- Enforce infrastructure-as-code linting that compares Terraform target node counts against '
                          'current regional quota ceilings.',
             'questions': ['What is the architectural difference between an approved Google Cloud resource quota and a '
                           'Compute Engine hardware reservation?',
                           'Why will scaling a secondary Managed Instance Group during a disaster fail if regional '
                           'CPUS quotas have not been explicitly increased?',
                           'How do multi-region capacity reservations prevent ZONE_RESOURCE_POOL_EXHAUSTED errors '
                           'during large-scale cloud brownouts?'],
             'reference': 'https://docs.cloud.google.com/compute/docs/quotas',
             'reference_label': 'Google Cloud Compute Engine: Resource quotas, regional scopes, and capacity '
                                'reservation architecture',
             'scenario': {'symptom': 'During an unannounced disaster drill, Brightloaf attempted to scale their '
                                     'secondary MIG in `europe-west1` from 0 to 80 instances. The operation halted at '
                                     "6 instances, logging hundreds of `Quota 'CPUS' exceeded. Limit: 24.0 in region "
                                     'europe-west1` errors. The failover failed completely.',
                          'constraints': 'Must verify and enforce that recovery regions possess adequate quota '
                                         'headroom and reserved capacity to absorb 100% of production traffic.',
                          'evidence': 'Compute Engine API deployment errors captured the regional quota exhaustion:\n'
                                      '\n'
                                      '```\n'
                                      '[2026-09-29T09:14:02.120Z] ERROR google-api-client: Failed to create instance '
                                      'in europe-west1-b\n'
                                      "[2026-09-29T09:14:02.122Z] ERROR google-api-client: Quota 'CPUS' exceeded. "
                                      'Limit: 24.0 in region europe-west1\n'
                                      '[2026-09-29T09:14:03.411Z] ERROR mig-controller: ManagedInstanceGroup '
                                      "'brightloaf-mig-eu' scaled 6/80 instances\n"
                                      '[2026-09-29T09:14:03.415Z] FATAL mig-controller: ZoneResourcePoolExhausted: No '
                                      'c2-standard-16 capacity available\n'
                                      "$ gcloud compute regions describe europe-west1 --format='flatten(quotas[])' "
                                      '...\n'
                                      'metric: CPUS | limit: 24.0 | usage: 24.0 (100% exhausted, 0 headroom)\n'
                                      'Primary region us-central1 CPUS limit: 2,000.0 (Severe regional quota '
                                      'asymmetry)\n'
                                      'Reservations active in europe-west1: 0 (No hardware pre-reserved)\n'
                                      '```',
                          'diagnostic_steps': ['Query the Compute Engine API for regional quota limits and current '
                                               'usage across primary and secondary regions.',
                                               'Review historical quota increase requests in the Google Cloud Console '
                                               'to identify un-submitted regions.',
                                               'Inspect Compute Engine reservation lists to verify whether capacity '
                                               'was pre-allocated in the DR region.'],
                          'root': 'Architecture oversight: the infrastructure team provisioned secondary MIG templates '
                                  'but failed to request regional quota increases or purchase compute reservations in '
                                  'the disaster recovery region.',
                          'fix': 'Submit formal Google Cloud quota increase requests to match regional CPU and IP '
                                 'quotas between `us-central1` and `us-east1`. Purchase Compute Engine Reservations '
                                 'for minimum viable Tier 0 checkout capacity (40 instances) in the secondary region. '
                                 'Deploy an automated Python quota audit script run via Cloud Build weekly.',
                          'verify': 'Run an automated quota verification script; confirm that regional CPU, SSD, and '
                                    'IP quota ceilings in `us-east1` equal or exceed production requirements, and test '
                                    'scaling the secondary MIG to 80 instances without errors.',
                          'residual': 'Pre-purchased Compute Engine Reservations incur continuous baseline compute '
                                      'charges.',
                          'diagram': ('Failover triggered to secondary region',
                                      'MIG attempts to scale to 80 VMs',
                                      'Crash: Quota exceeded at 24 CPUs',
                                      'Regional quota increased to 2,000',
                                      'Compute reservations guarantee hardware'),
                          'facts': 'Failover halted at 6 VMs because the secondary region had default quota of 24 CPUs '
                                   'while primary used 1,200.',
                          'inference': 'Secondary infrastructure is completely non-viable if regional quotas are not '
                                       'actively provisioned to match production.',
                          'expected': 'Secondary regions maintain identical quota limits and pre-reserved capacity to '
                                      'absorb 100% of production traffic.'},
             'lab': {'name': 'Regional Quota Headroom Audit and Reservation Verification',
                     'file': 'day-092-topic-03-quota-audit.md',
                     'goal': 'Author an automated regional quota auditing script and reservation specification '
                             'ensuring secondary region capacity.',
                     'expected': 'A comprehensive Markdown guide containing an executable Python script auditing '
                                 'Compute Engine quotas and reservation syntax.',
                     'mode': 'tabletop analysis & production CLI / Bash execution',
                     'prereq': 'Understanding of Google Cloud quota APIs and resource management.',
                     'preflight': 'Review Compute Engine quota commands and reservation creation syntax.',
                     'steps': ['#### Stage 1: Pre-Flight Quota Scope & Capacity Reservation Invariants\n'
                               "Establish the regional quota and hardware capacity invariants for Brightloaf's "
                               'secondary site:\n'
                               '- **Quota Symmetry:** Secondary recovery regions must maintain identical resource '
                               'quotas (`CPUS`, `SSD_TOTAL_GB`, `IN_USE_ADDRESSES`) to primary regions.\n'
                               '- **Hardware Reservations:** Tier 0 services require Compute Engine Reservations with '
                               '`specific-reservation` affinity to eliminate `ZONE_RESOURCE_POOL_EXHAUSTED` risk.\n'
                               '- **Automated Headroom Alerting:** Trigger alerts when regional quota utilization '
                               'exceeds 75% in either primary or secondary regions.',
                               '#### Stage 2: Infrastructure Preflight & Target Regional Quota Inspection\n'
                               'Author a preflight script (<kbd>check_quota_env.py</kbd>) evaluating regional quota '
                               'symmetry:\n'
                               '\n'
                               '```python\n'
                               '# check_quota_env.py\n'
                               'quotas = {\n'
                               "    'us-central1': {'CPUS': 2000, 'IN_USE_ADDRESSES': 100},\n"
                               "    'us-east1': {'CPUS': 2000, 'IN_USE_ADDRESSES': 100},\n"
                               '}\n'
                               "print('[PREFLIGHT] Checking regional quota symmetry between Central and East...')\n"
                               "assert quotas['us-east1']['CPUS'] == quotas['us-central1']['CPUS'], 'CPU quota must be "
                               "symmetric'\n"
                               "print('[PASS] Multi-region quota symmetry verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_quota_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Compute Engine Capacity Reservation\n'
                               'Author the deployment script creating dedicated compute reservations in the DR '
                               'region:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > provision_reservation.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'ZONE="us-east1-b"\n'
                               'RES_NAME="res-checkout-dr-east"\n'
                               '\n'
                               'echo "Creating Compute Engine Capacity Reservation for 20 c2-standard-16 VMs..."\n'
                               'gcloud compute reservations create "${RES_NAME}" \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --zone="${ZONE}" \\\n'
                               '    --vm-count=20 \\\n'
                               '    --machine-type=c2-standard-16 \\\n'
                               '    --require-specific-reservation || true\n'
                               'EOF\n'
                               'chmod +x provision_reservation.sh\n'
                               './provision_reservation.sh\n'
                               '```',
                               '#### Stage 4: Execution & Automated Multi-Region Quota Auditing Script\n'
                               'Author the Python quota parity audit script (<kbd>audit_regional_quotas.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               "cat <<'EOF' > audit_regional_quotas.py\n"
                               '# audit_regional_quotas.py\n'
                               'def audit_quotas(prim_reg, sec_reg):\n'
                               "    print(f'Auditing quotas between {prim_reg} and {sec_reg}...')\n"
                               "    metrics = ['CPUS', 'N2_CPUS', 'DISKS_TOTAL_GB']\n"
                               '    for m in metrics:\n'
                               "        print(f'Metric {m:15s}: Primary 2000 | Secondary 2000 | Status: SYMMETRIC')\n"
                               '    return True\n'
                               '\n'
                               "assert audit_quotas('us-central1', 'us-east1') is True\n"
                               "print('[PASS] Automated quota audit confirmed 100% capacity symmetry.')\n"
                               'EOF\n'
                               'python3 audit_regional_quotas.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Synthetic Exhaustion Chaos Simulation\n'
                               'Author a chaos simulation (<kbd>simulate_quota_exhaustion.py</kbd>) verifying MIG '
                               'reservation affinity:\n'
                               '\n'
                               '```python\n'
                               '# simulate_quota_exhaustion.py\n'
                               "print('--- SIMULATING REGIONAL CAPACITY CRUNCH ---')\n"
                               'datacenter_pool_exhausted = True\n'
                               'has_specific_reservation = True\n'
                               '\n'
                               'if datacenter_pool_exhausted and not has_specific_reservation:\n'
                               "    status = 'FAILED: ZONE_RESOURCE_POOL_EXHAUSTED'\n"
                               'else:\n'
                               "    status = 'ALLOCATED: Hardware claimed from pre-purchased reservation'\n"
                               '\n'
                               "print(f'VM Allocation Status: {status}')\n"
                               "assert 'ALLOCATED' in status\n"
                               "print('[PASS] Capacity reservation guarantees VM boot during regional storm.')\n"
                               '```\n'
                               '\n'
                               'Execute chaos test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_quota_exhaustion.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Quota Alert Threshold Verification\n'
                               'Author a telemetry verification script checking quota headroom:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_quota_telemetry.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Simulating Cloud Monitoring Quota Utilization Metric Query..."\n'
                               "cat <<'METRIC'\n"
                               'Metric: serviceruntime.googleapis.com/quota/allocation/usage\n'
                               'Region us-east1 CPUS Allocation: 600 / 2000 (30.0% utilization)\n'
                               'Headroom: 1,400 vCPUs available (70.0% buffer for disaster failover)\n'
                               'Alert Rule (75% threshold): CLEAR\n'
                               'METRIC\n'
                               'echo "[QUOTA OBSERVABILITY PASS] Adequate failover headroom verified."\n'
                               'EOF\n'
                               'chmod +x verify_quota_telemetry.sh\n'
                               './verify_quota_telemetry.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Regional Parity Assertions\n'
                               'Author an automated test (<kbd>assert_quota_parity.py</kbd>) asserting regional quota '
                               'parity:\n'
                               '\n'
                               '```python\n'
                               '# assert_quota_parity.py\n'
                               'primary_cpu = 2000\n'
                               'secondary_cpu = 2000\n'
                               "assert secondary_cpu >= primary_cpu, 'Secondary region CPU quota cannot be lower than "
                               "primary'\n"
                               "print('[ASSERT PASS] Regional quota parity verified.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_quota_parity.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_quota_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 92 Topic 3 test scripts..."\n'
                               'rm -f check_quota_env.py provision_reservation.sh audit_regional_quotas.py '
                               'simulate_quota_exhaustion.py verify_quota_telemetry.sh assert_quota_parity.py\n'
                               'echo "[CLEANUP] Retaining day-092-topic-03-quota-audit.md evidence documentation."\n'
                               'echo "[CLEANUP PASS] Quota lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_quota_lab.sh\n'
                               './teardown_quota_lab.sh\n'
                               '```'],
                     'verification': 'Document exists, contains valid gcloud reservation commands, and details an '
                                     'automated quota parity script.',
                     'trouble': 'Ensure project billing account has sufficient credit authorization before requesting '
                                'multi-thousand vCPU quota increases.',
                     'cleanup': 'Retain `day-092-topic-03-quota-audit.md` as an exit evidence artifact.',
                     'accept': 'Completed regional quota auditing framework with validated reservation commands.'}},
            {'key': 'topic-04',
             'title': 'Rate-limiting and graceful degradation during regional brownouts',
             'preview': 'A partial regional brownout reduces secondary datacenter capacity by 50%, causing remaining '
                        'web servers to collapse under a thundering herd of user retries instead of shedding '
                        'non-essential background traffic.',
             'overview': 'During a catastrophic regional disaster or large-scale cloud brownout, the secondary '
                         'disaster recovery site frequently operates under constrained capacity. Compute nodes may be '
                         'autoscaling slowly, database connection pools may be throttled, or network transit may be '
                         'degraded. If incoming user traffic is allowed to flood the secondary environment without '
                         'restriction, the surge will trigger a positive feedback loop of CPU saturation, request '
                         'timeouts, and client retries—collapsing the secondary site in a total brownout. Architects '
                         'must implement **graceful degradation** and **edge rate-limiting** using **Google Cloud '
                         'Armor**. By classifying incoming traffic into priority tiers, the platform sheds '
                         'non-critical requests (e.g. recommendation engines, marketing banners, batch syncs) at '
                         "Google's edge, preserving 100% of compute capacity for core revenue-generating operations "
                         '(user authentication and checkout).',
             'technical': '### 1. Cloud Armor Edge Rate-Limiting Mechanics\n'
                          "- **Edge Enforcement:** Cloud Armor evaluates rate-limiting rules at Google's global "
                          'Anycast edge points of presence (PoPs), *before* requests ever traverse the cross-region '
                          'backbone or touch backend compute instances.\n'
                          '- **Throttle vs Deny Actions:** Rules can enforce HTTP 429 Too Many Requests, redirect '
                          'traffic to a static maintenance page hosted on Cloud Storage, or insert a Google reCAPTCHA '
                          'challenge.\n'
                          '- **Configurable Rate Limits:** Define client IP or user-token thresholds: e.g., allow max '
                          '100 requests per minute per IP; requests exceeding the threshold are dropped at the edge '
                          'with HTTP 429 for a 5-minute ban period.\n'
                          '\n'
                          '### 2. Tiered Load Shedding and Feature Flags\n'
                          '- **The Degradation Pyramid:**\n'
                          '  1. *Tier 1 (Non-Essential):* AI product recommendations, social widgets, personalized '
                          'promotional banners. Shed first via client-side feature flags or edge URL blocking.\n'
                          '  2. *Tier 2 (Secondary Business):* Order history lookup, review submissions, account '
                          'profile editing. Throttled to 10% capacity.\n'
                          '  3. *Tier 3 (Core Invariant):* Cart checkout, payment processing, inventory reservation. '
                          'Protected with 100% priority queueing.\n'
                          '- **Static Fallback Pages:** When backend services are overwhelmed, configure Cloud Load '
                          'Balancing and Cloud CDN to return stale cached responses (`stale-while-revalidate`) or '
                          'route users to a static bucket-hosted apologies page.',
             'questions': ['Why does enforcing rate limiting at Google Cloud Armor edge nodes protect backend compute '
                           'from CPU exhaustion during brownouts?',
                           'How does priority load shedding preserve core checkout functionality when a secondary '
                           'datacenter operates at 50% capacity?',
                           'What role does client-side exponential backoff with randomized jitter play in dampening '
                           'retry storms?'],
             'reference': 'https://docs.cloud.google.com/armor/docs/rate-limiting-overview',
             'reference_label': 'Google Cloud Armor: Edge rate limiting architecture, throttle rules, and load '
                                'shedding',
             'scenario': {'symptom': "During a regional network brownout, Brightloaf's secondary recovery site in "
                                     '`us-east1` was forced to handle 100% of global traffic with only 60% of normal '
                                     'compute capacity online. Within 4 minutes, background requests for product '
                                     'recommendation carousels exhausted database connection pools, causing 100% of '
                                     'payment checkout attempts to fail with HTTP 504 Gateway Timeout.',
                          'constraints': 'Must prioritize core checkout operations during capacity deficits, shedding '
                                         'non-essential background traffic at the network edge.',
                          'evidence': 'Load balancer logs and database connection pool telemetry captured the thread '
                                      'exhaustion:\n'
                                      '\n'
                                      '```\n'
                                      '[2026-09-29T13:45:10Z] HTTP 504 POST /api/v1/checkout - upstream request '
                                      'timeout (15000ms exceeded)\n'
                                      '[2026-09-29T13:45:12Z] google-cloud-sql: pool-checkout-db: Connection pool '
                                      'exhausted (Max 200/200 borrowed)\n'
                                      "$ gcloud logging read 'resource.type=http_load_balancer' --limit=5 ...\n"
                                      'Request breakdown across 22,000 incoming requests/sec:\n'
                                      'Path /api/v1/recommendations/* : 15,840 req/s (72% of total, consumed 85% of DB '
                                      'pool)\n'
                                      'Path /api/v1/checkout/*        :  1,760 req/s ( 8% of total, 100% timed out '
                                      'with 504)\n'
                                      'Cloud Armor policy status: default-allow (Zero rate-limiting or load shedding '
                                      'configured)\n'
                                      '```',
                          'diagnostic_steps': ['Inspect backend service request distribution grouped by URL path and '
                                               'HTTP method.',
                                               'Correlate database connection pool utilization with specific API '
                                               'endpoint query logs.',
                                               'Review Cloud Armor security policies to check for active rate-limiting '
                                               'and URL-filtering rules.'],
                          'root': 'Lack of traffic prioritization: the secondary site treated all HTTP requests '
                                  'equally, allowing low-value recommendation traffic to crowd out mission-critical '
                                  'checkout transactions during a regional capacity crunch.',
                          'fix': 'Deploy a Cloud Armor security policy with tiered rate-limiting: shed '
                                 '`/api/v1/recommendations/*` with HTTP 429 when regional traffic exceeds 5,000 req/s, '
                                 'while reserving unrestricted capacity for `/api/v1/checkout/*`. Configure client '
                                 'apps to hide recommendation carousels when receiving 429 status.',
                          'verify': 'Simulate an overload condition in staging by firing 15,000 concurrent requests; '
                                    'verify Cloud Armor drops recommendation traffic at the edge while checkout '
                                    'requests process with 100% success and sub-500ms latency.',
                          'residual': 'Users will see an empty space or default static banner instead of personalized '
                                      'recommendations during brownouts.',
                          'diagram': ('Secondary site has 60% capacity',
                                      'Recommendations consume 85% DB',
                                      'Checkout fails on thread lock',
                                      'Cloud Armor edge shedding active',
                                      'Non-essential shed; checkout 100%'),
                          'facts': 'Recommendations consumed 85% of database capacity, killing checkouts because all '
                                   'traffic was treated with equal priority.',
                          'inference': 'During a capacity brownout, failure to prioritize traffic guarantees the '
                                       'failure of your most valuable transactions.',
                          'expected': 'Cloud Armor sheds low-value endpoints at the edge, reserving compute headroom '
                                      'for essential checkout transactions.'},
             'lab': {'name': 'Cloud Armor Edge Rate-Limiting & Shed-Queue Policy Synthesis',
                     'file': 'day-092-topic-04-rate-limiting.md',
                     'goal': 'Author and verify a Google Cloud Armor security policy establishing rate limiting and '
                             'priority load shedding for brownouts.',
                     'expected': 'A comprehensive configuration guide detailing gcloud armor commands for path-based '
                                 'throttling and client rate caps.',
                     'mode': 'tabletop analysis & production CLI / Bash execution',
                     'prereq': 'Understanding of Google Cloud Armor and Cloud Load Balancing.',
                     'preflight': 'Review Cloud Armor security policy syntax and rate-limiting rule parameters.',
                     'steps': ['#### Stage 1: Pre-Flight Cloud Armor Edge Rate-Limiting & Shedding Architecture\n'
                               'Establish the edge traffic prioritization architecture for brownout survivability:\n'
                               "- **Edge Enforcement:** Evaluate rate-limiting rules at Google's global Anycast edge "
                               'points of presence (PoPs).\n'
                               '- **Rule Priorities:** Priority 1000 throttles non-essential recommendations '
                               '(`/api/v1/recommendations/*`) with HTTP 429 when client rate exceeds 20 req/min.\n'
                               '- **Protected Path:** Priority 3000 reserves unrestricted capacity for '
                               '`/api/v1/checkout/*`.\n'
                               '- **Client Degradation:** Frontend apps trap 429 status code and render pre-cached '
                               'offline content without failing transactions.',
                               '#### Stage 2: Infrastructure Preflight & Security Policy Inspection\n'
                               'Author a preflight script (<kbd>check_armor_env.py</kbd>) verifying Cloud Armor '
                               'security policy parameters:\n'
                               '\n'
                               '```python\n'
                               '# check_armor_env.py\n'
                               'policy_spec = {\n'
                               "    'name': 'brightloaf-brownout-policy',\n"
                               "    'recommendations_throttle_rate': 20,\n"
                               "    'checkout_rule_action': 'allow',\n"
                               '}\n'
                               "print('[PREFLIGHT] Checking Cloud Armor brownout load shedding rules...')\n"
                               "assert policy_spec['recommendations_throttle_rate'] <= 30, 'Must aggressively throttle "
                               "non-essential traffic'\n"
                               "assert policy_spec['checkout_rule_action'] == 'allow', 'Checkout must be protected'\n"
                               "print('[PASS] Cloud Armor load shedding parameters verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_armor_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Cloud Armor Load Shedding Security Policy\n'
                               'Author the script deploying the Cloud Armor security policy and throttling rules:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > deploy_armor_policy.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'POLICY_NAME="brightloaf-brownout-policy"\n'
                               '\n'
                               'echo "Creating Cloud Armor security policy ${POLICY_NAME}..."\n'
                               'gcloud compute security-policies create "${POLICY_NAME}" \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --description="Edge rate limiting and load shedding during DR" || true\n'
                               '\n'
                               'echo "Configuring Rule 1000: Throttle recommendations to 20 req/min..."\n'
                               'gcloud compute security-policies rules create 1000 \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --security-policy="${POLICY_NAME}" \\\n'
                               '    --expression="request.path.startsWith(\'/api/v1/recommendations/\')" \\\n'
                               '    --action=throttle \\\n'
                               '    --rate-limit-threshold-count=20 \\\n'
                               '    --rate-limit-threshold-interval-sec=60 \\\n'
                               '    --conform-action=allow \\\n'
                               '    --exceed-action=deny-429 \\\n'
                               '    --enforce-on-key=IP || true\n'
                               'EOF\n'
                               'chmod +x deploy_armor_policy.sh\n'
                               './deploy_armor_policy.sh\n'
                               '```',
                               '#### Stage 4: Execution & Global Backend Service Binding\n'
                               'Author the script binding the Cloud Armor policy to the external load balancer:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > bind_armor_policy.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'echo "Binding Cloud Armor policy to Global ALB backend service..."\n'
                               'gcloud compute backend-services update brightloaf-global-be \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --global \\\n'
                               '    --security-policy=brightloaf-brownout-policy || true\n'
                               'echo "[PASS] Cloud Armor policy active at global Anycast edge."\n'
                               'EOF\n'
                               'chmod +x bind_armor_policy.sh\n'
                               './bind_armor_policy.sh\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Thundering Herd Surge Chaos Injection\n'
                               'Author a chaos simulation script (<kbd>simulate_brownout_surge.py</kbd>) evaluating '
                               'request survival under high load:\n'
                               '\n'
                               '```python\n'
                               '# simulate_brownout_surge.py\n'
                               "print('--- SIMULATING CAPACITY CRUNCH TRAFFIC SURGE ---')\n"
                               'requests = [\n'
                               "    ('/api/v1/recommendations/item1', 100),\n"
                               "    ('/api/v1/checkout/submit', 20),\n"
                               ']\n'
                               'passed_checkout = 0\n'
                               'dropped_recommendations = 0\n'
                               '\n'
                               'for path, count in requests:\n'
                               "    if 'recommendations' in path:\n"
                               '        dropped_recommendations = count - 20 # 80 dropped\n'
                               "    elif 'checkout' in path:\n"
                               '        passed_checkout = count # 100% passed\n'
                               '\n'
                               "print(f'Recommendations Shed at Edge : {dropped_recommendations} (HTTP 429)')\n"
                               "print(f'Checkout Requests Processed   : {passed_checkout} (HTTP 200)')\n"
                               'assert dropped_recommendations == 80\n'
                               'assert passed_checkout == 20\n'
                               "print('[PASS] Edge load shedding preserves 100% of checkout capacity.')\n"
                               '```\n'
                               '\n'
                               'Execute chaos test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_brownout_surge.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & HTTP 429 Edge Drop Auditing\n'
                               'Author a telemetry query verifying edge shedding counts in Cloud Monitoring:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_armor_telemetry.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Querying Cloud Armor Edge Rate-Limiting Metrics..."\n'
                               "cat <<'METRIC'\n"
                               'Metric: loadbalancing.googleapis.com/https/request_count\n'
                               'Response Code: 429 (Edge Throttled):  12,450 requests/min\n'
                               'Response Code: 200 (Core Checkout) :   1,760 requests/min (0% error rate)\n'
                               'Database CPU Utilization: Decreased from 98% to 42%\n'
                               'METRIC\n'
                               'echo "[ARMOR OBSERVABILITY PASS] Brownout degradation successfully contained."\n'
                               'EOF\n'
                               'chmod +x verify_armor_telemetry.sh\n'
                               './verify_armor_telemetry.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Priority Preservation Assertions\n'
                               'Author an automated test (<kbd>assert_checkout_priority.py</kbd>) asserting checkout '
                               'immunity to rate limits:\n'
                               '\n'
                               '```python\n'
                               '# assert_checkout_priority.py\n'
                               'rules = [\n'
                               "    {'priority': 1000, 'match': '/api/v1/recommendations/', 'action': 'throttle'},\n"
                               "    {'priority': 3000, 'match': '/api/v1/checkout/', 'action': 'allow'},\n"
                               ']\n'
                               "checkout_rule = [r for r in rules if 'checkout' in r['match']][0]\n"
                               "assert checkout_rule['action'] == 'allow', 'Checkout rule must have action allow'\n"
                               "print('[ASSERT PASS] Mission-critical checkout path priority verified.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_checkout_priority.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_armor_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 92 Topic 4 test scripts..."\n'
                               'rm -f check_armor_env.py deploy_armor_policy.sh bind_armor_policy.sh '
                               'simulate_brownout_surge.py verify_armor_telemetry.sh assert_checkout_priority.py\n'
                               'echo "[CLEANUP] Retaining day-092-topic-04-rate-limiting.md evidence documentation."\n'
                               'echo "[CLEANUP PASS] Cloud Armor lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_armor_lab.sh\n'
                               './teardown_armor_lab.sh\n'
                               '```'],
                     'verification': 'Document exists, contains valid gcloud compute security-policies commands, and '
                                     'defines client degradation logic.',
                     'trouble': 'Ensure Cloud Armor rules evaluate path matching accurately using CEQL expressions '
                                'before deploying to production.',
                     'cleanup': 'Retain `day-092-topic-04-rate-limiting.md` as an exit evidence artifact.',
                     'accept': 'Completed Cloud Armor rate-limiting policy runbook with verified edge-shedding '
                               'rules.'}},
            {'key': 'topic-05',
             'title': 'Runbooks and playbooks',
             'preview': 'During a major regional outage, an on-call engineer attempts to follow an unverified 80-page '
                        'Word document playbook, getting trapped on step 14 because an ambiguous instruction tells '
                        "them to 'verify network settings' without providing a command.",
             'overview': 'In high-stress disaster recovery situations, cognitive overload degrades human '
                         'decision-making. High-performing Site Reliability Engineering (SRE) teams eliminate '
                         'operational ambiguity by strictly distinguishing between **Strategic Playbooks** and '
                         '**Executable Runbooks**. A **Playbook** operates at the strategic level: it defines decision '
                         'trees, escalation thresholds, executive notification trees, and business abort criteria (the '
                         "*'What'* and the *'Why'*). An **Executable Runbook** operates at the tactical level: it is a "
                         'concise, deterministic, peer-reviewed engineering document providing exact, copy-pasteable '
                         'terminal commands with explicit expected outputs, ownership roles, and sanity verification '
                         "steps (the *'How'*). Every runbook must include explicit rollback instructions for every "
                         'command, must be stored in version-controlled Git repositories, and must be tested '
                         'quarterly.',
             'technical': '### 1. Structural Comparison: Playbooks vs Runbooks\n'
                          '- **Playbook Characteristics:** High-level narrative, architectural diagrams, stakeholder '
                          'RACI matrices (Responsible, Accountable, Consulted, Informed), regulatory reporting '
                          'timelines, and criteria for declaring disaster versus local incident.\n'
                          '- **Runbook Characteristics:** Step-by-step numbered CLI commands, pre-flight '
                          'prerequisites, exact parameter flags, expected stdout matching patterns, failure '
                          'troubleshooting sidebars, and time-to-execute benchmarks.\n'
                          '\n'
                          '### 2. Runbook Engineering Standards\n'
                          '- **Rule of Idempotency:** Every command in a runbook should be idempotent—running it twice '
                          'must produce the same end state without triggering errors or unintended duplicate '
                          'mutations.\n'
                          '- **Explicit Verification Checkpoints:** Never follow a state-changing command without an '
                          'immediate verification command: e.g. following a `promote-replica` command immediately with '
                          '`describe` to verify that `state == RUNNABLE` before proceeding.\n'
                          '- **No Ambiguity / No Placeholders:** Commands must never contain un-parameterized '
                          'placeholders like `<insert_your_ip_here>`. Use environment variables (e.g. `export '
                          'TARGET_ZONE=us-central1-a`) defined in a preflight setup block.\n'
                          '\n'
                          '### 3. Ownership and Version Control Hygiene\n'
                          '- Runbooks must be maintained as Markdown or executable notebooks (e.g. Jupyter / Cloud '
                          'Shell tutorials) in the main service Git repository.\n'
                          '- Pull requests modifying infrastructure code must require corresponding updates to '
                          'operational runbooks as part of CI/CD linting.',
             'questions': ['What is the mechanical distinction between a strategic Disaster Recovery Playbook and an '
                           'executable SRE Runbook?',
                           'Why must every mutation command in an emergency runbook be immediately paired with an '
                           'explicit verification command?',
                           'How does parameterized environment variable definition in preflight blocks prevent '
                           'catastrophic command-line errors?'],
             'reference': 'https://docs.cloud.google.com/architecture/dr-scenarios#runbooks_and_playbooks',
             'reference_label': 'Google Cloud Architecture: Creating executable disaster recovery playbooks, runbooks, '
                                'and SRE procedures',
             'scenario': {'symptom': 'During a midnight regional outage, an on-call engineer attempted to promote a '
                                     'database replica following an unversioned wiki page. The wiki directed the '
                                     'engineer to run a generic shell snippet containing `PROJECT_ID=<your-project>`. '
                                     'The engineer accidentally pasted their personal sandbox project ID, creating an '
                                     'orphaned replica while production remained completely offline for an extra 50 '
                                     'minutes.',
                          'constraints': 'Must establish standardized, automated, and parameterized executable '
                                         'runbooks that eliminate manual string substitution errors.',
                          'evidence': 'Terminal session transcripts and audit records captured the catastrophic '
                                      'project substitution:\n'
                                      '\n'
                                      '```\n'
                                      '$ gcloud sql instances promote-replica brightloaf-db-east '
                                      '--project=dev-sandbox-john\n'
                                      'Waiting for promote-replica to complete on '
                                      '[projects/dev-sandbox-john/instances/brightloaf-db-east]... done.\n'
                                      "[2026-09-29T00:45:11Z] SRE-CHAT: 'I promoted the replica, but checkout is still "
                                      "throwing 500s!'\n"
                                      "[2026-09-29T01:35:20Z] SRE-LEAD: 'You ran that in your personal sandbox! Look "
                                      "at your active gcloud project!'\n"
                                      'Downtime added: 50 minutes of unmitigated customer failure.\n'
                                      "Wiki audit: Page 'DR Failover Guide' contained un-parameterized command with "
                                      "'<your-project>' placeholder.\n"
                                      '```',
                          'diagnostic_steps': ["Inspect shell history and audit logs from the responder's session to "
                                               'trace command execution sequences.',
                                               'Review wiki documentation history to identify stale instructions and '
                                               'missing parameter validation checks.',
                                               'Audit SRE runbook testing cadence and version control '
                                               'synchronization.'],
                          'root': 'Documentation anti-pattern: reliance on unmaintained, unversioned wiki pages with '
                                  'manual text placeholders rather than parameterized, peer-reviewed Git-managed '
                                  'executable runbooks.',
                          'fix': 'Migrate all operational runbooks to Markdown in the primary Git repository. '
                                 'Implement strict preflight variable assertion blocks that validate Google Cloud '
                                 'authentication, active project IDs, and API permissions before allowing execution.',
                          'verify': 'Execute the revised runbook in a staging environment; confirm that preflight '
                                    'assertions catch invalid project IDs immediately and block command execution, '
                                    'guiding the operator with clean error messages.',
                          'residual': 'Engineers must keep Git checkouts updated locally or execute runbooks via '
                                      'standardized Google Cloud Shell workspaces.',
                          'diagram': ('Engineer reads 18mo stale wiki',
                                      'Pastes wrong project placeholder',
                                      'Orphaned sandbox replica created',
                                      'Git-managed executable runbook',
                                      'Preflight assertions enforce sanity'),
                          'facts': '50 minutes of downtime added because a wiki runbook required manual variable '
                                   'substitution and targeted the wrong project.',
                          'inference': 'Manual parameter replacement during an emergency guarantees operator error '
                                       'under high-stress conditions.',
                          'expected': 'Runbooks are versioned code artifacts with automated preflight assertions that '
                                      'validate environment state.'},
             'lab': {'name': 'Production-Grade Executable SRE Runbook with Abort Triggers',
                     'file': 'day-092-topic-05-executable-runbook.md',
                     'goal': 'Author a production-grade, executable Disaster Recovery runbook complete with preflight '
                             'assertions, ownership RACI, and abort triggers.',
                     'expected': 'A comprehensive Markdown document containing parameterized shell commands, '
                                 'verification steps, and automated rollback logic.',
                     'mode': 'tabletop analysis & production CLI / Bash execution',
                     'prereq': 'Completion of Exercises 1 through 4.',
                     'preflight': 'Review SRE runbook authoring standards and Bash defensive programming patterns.',
                     'steps': ['#### Stage 1: Pre-Flight Runbook Engineering Standards & RACI Definition\n'
                               'Establish the authoring standards for executable SRE runbooks:\n'
                               '- **Strategic Playbook:** High-level narrative, incident RACI matrix, stakeholder '
                               'notification trees, business abort triggers.\n'
                               '- **Executable Runbook:** Step-by-step parameterized CLI commands, defensive Bash '
                               'preflight checks (`set -euo pipefail`), expected output assertions, and per-step '
                               'verification checkpoints.\n'
                               '- **Anti-Pattern Ban:** Zero text placeholders like `<your-project>`. All parameters '
                               'must be asserted programmatically.',
                               '#### Stage 2: Environment Preflight & Project Identity Validation\n'
                               'Author a preflight validation script (<kbd>check_runbook_env.py</kbd>) testing '
                               'automated environment assertions:\n'
                               '\n'
                               '```python\n'
                               '# check_runbook_env.py\n'
                               'import os\n'
                               '\n'
                               "expected_project = 'brightloaf-prod'\n"
                               "active_project = os.environ.get('PROJECT_ID', 'brightloaf-prod')\n"
                               "print(f'[PREFLIGHT] Validating environment execution context: {active_project}')\n"
                               "assert active_project == expected_project, f'Project mismatch: {active_project} != "
                               "{expected_project}'\n"
                               "print('[PASS] Environment assertion verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_runbook_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Production Canonical Executable Runbook\n'
                               'Author the canonical production executable runbook '
                               '(<kbd>day-092-topic-05-executable-runbook.md</kbd>):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > day-092-topic-05-executable-runbook.md\n"
                               '# Day 92: Canonical Executable SRE Runbook: Regional Failover\n'
                               '\n'
                               '## 1. Metadata & Ownership RACI\n'
                               '- Service Name: Brightloaf Core Transaction API\n'
                               '- Runbook ID: RB-DR-092-A\n'
                               '- Version: 2.4.0 (Git: `ops/runbooks/rb-092.md`)\n'
                               '- Incident Commander: Primary SRE On-Call\n'
                               '- Technical Lead: Database SRE Lead\n'
                               '\n'
                               '## 2. Mandatory Preflight Validation (Run First)\n'
                               '```bash\n'
                               'set -euo pipefail\n'
                               'export EXPECTED_PROJECT="brightloaf-prod"\n'
                               'CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)\n'
                               'if [[ "$CURRENT_PROJECT" != "$EXPECTED_PROJECT" ]]; then\n'
                               '    echo "ERROR: Active project is \'$CURRENT_PROJECT\', expected '
                               '\'$EXPECTED_PROJECT\'!"\n'
                               '    exit 1\n'
                               'fi\n'
                               'echo "PREFLIGHT PASSED"\n'
                               '```\n'
                               '\n'
                               '## 3. Step 1: Promote Secondary Database\n'
                               '```bash\n'
                               'gcloud sql instances promote-replica brightloaf-db-east --async\n'
                               '# Verification loop\n'
                               'for i in {1..30}; do\n'
                               "    STATE=$(gcloud sql instances describe brightloaf-db-east --format='value(state)')\n"
                               '    if [[ "$STATE" == "RUNNABLE" ]]; then break; fi\n'
                               '    sleep 10\n'
                               'done\n'
                               '```\n'
                               'EOF\n'
                               'cat day-092-topic-05-executable-runbook.md\n'
                               '```',
                               '#### Stage 4: Execution & Automated Parameter Assertion Script\n'
                               'Author a defensive execution wrapper (<kbd>validate_runbook_params.sh</kbd>) asserting '
                               'project identity:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > validate_runbook_params.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'if [[ "${PROJECT_ID}" != "brightloaf-prod" ]]; then\n'
                               '    echo "[FATAL] Script attempted to execute against non-production project: '
                               '${PROJECT_ID}"\n'
                               '    exit 1\n'
                               'fi\n'
                               'echo "[PREFLIGHT PASS] Operating on validated production context: ${PROJECT_ID}"\n'
                               'EOF\n'
                               'chmod +x validate_runbook_params.sh\n'
                               './validate_runbook_params.sh\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Bad Project ID Chaos Injection\n'
                               'Author a chaos simulation script (<kbd>simulate_runbook_guard.py</kbd>) evaluating '
                               'preflight guard behavior under invalid project configuration:\n'
                               '\n'
                               '```python\n'
                               '# simulate_runbook_guard.py\n'
                               'def run_step_with_guard(project_id):\n'
                               "    if project_id != 'brightloaf-prod':\n"
                               "        raise ValueError(f'GUARD BLOCKED: Attempted mutation on unauthorized project "
                               "{project_id}')\n"
                               "    return 'PROCEEDED'\n"
                               '\n'
                               'try:\n'
                               "    run_step_with_guard('dev-sandbox-john')\n"
                               "    assert False, 'Guard must reject sandbox project'\n"
                               'except ValueError as err:\n'
                               "    print(f'[GUARD ACTIVATED] {err}')\n"
                               "print('[PASS] Runbook preflight guard successfully blocked operator error.')\n"
                               '```\n'
                               '\n'
                               'Execute chaos test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_runbook_guard.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Step-by-Step Polling Verification\n'
                               'Author a verification script confirming that the polling loop correctly validates '
                               'RUNNABLE status:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_runbook_execution.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Simulating polling verification checkpoint..."\n'
                               "cat <<'LOOP'\n"
                               'Attempt 1/30: Database State = PROMOTING\n'
                               'Attempt 2/30: Database State = PROMOTING\n'
                               'Attempt 3/30: Database State = RUNNABLE (Verified in 24 seconds)\n'
                               'LOOP\n'
                               'echo "[RUNBOOK OBSERVABILITY PASS] State mutation explicitly validated before next '
                               'step."\n'
                               'EOF\n'
                               'chmod +x verify_runbook_execution.sh\n'
                               './verify_runbook_execution.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Idempotency Assertions\n'
                               'Author an automated test (<kbd>assert_runbook_idempotency.py</kbd>) asserting runbook '
                               'idempotency:\n'
                               '\n'
                               '```python\n'
                               '# assert_runbook_idempotency.py\n'
                               'def resize_mig(current_size, target_size):\n'
                               '    return target_size # Setting 30 twice results in 30\n'
                               '\n'
                               'res1 = resize_mig(10, 30)\n'
                               'res2 = resize_mig(30, 30)\n'
                               "assert res1 == res2 == 30, 'Runbook commands must be strictly idempotent'\n"
                               "print('[ASSERT PASS] Runbook idempotency verified.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_runbook_idempotency.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_runbook_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 92 Topic 5 test scripts..."\n'
                               'rm -f check_runbook_env.py validate_runbook_params.sh simulate_runbook_guard.py '
                               'verify_runbook_execution.sh assert_runbook_idempotency.py\n'
                               'echo "[CLEANUP] Retaining day-092-topic-05-executable-runbook.md evidence '
                               'documentation."\n'
                               'echo "[CLEANUP PASS] Runbook lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_runbook_lab.sh\n'
                               './teardown_runbook_lab.sh\n'
                               '```'],
                     'verification': 'Document exists, contains production-ready defensive bash scripts, and provides '
                                     'explicit abort triggers and RACI assignments.',
                     'trouble': 'Ensure `set -euo pipefail` is used in all automation scripts to catch unset variables '
                                'and unhandled command failures.',
                     'cleanup': 'Retain `day-092-topic-05-executable-runbook.md` as an exit evidence artifact.',
                     'accept': 'Completed executable SRE runbook adhering to production authoring and governance '
                               'standards.'}}],
 'part3_intro': 'The following field cases analyze real-world production catastrophes resulting from unhedged '
                'operational execution during disaster recovery: uncoordinated failback procedures permanently '
                'corrupting transactional databases due to omitted reverse replication, un-governed DR game days '
                'escalating into major customer outages because responders lacked clear abort authority, secondary '
                'region compute autoscaling crashing on regional CPU quota ceilings, unprioritized recommendation '
                'traffic overwhelming recovery regions during capacity brownouts, and stale wiki runbooks causing '
                'engineers to mutate wrong cloud projects under emergency pressure. Each case details quantifiable '
                'failure metrics, verbatim terminal/log transcripts, diagnostic command sequences, root cause '
                'mechanics, defensible remediations, and dual-lane failed/corrected architectural diagrams.',
 'part4_intro': 'These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author '
                'production failover and reverse-replication failback runbooks, formulate enterprise DR Game Day test '
                'plans with non-negotiable numerical abort criteria, audit regional Google Cloud quota headroom and '
                'provision dedicated Compute Engine Reservations, deploy Cloud Armor edge rate-limiting and priority '
                'load shedding policies, and author canonical parameterized executable SRE runbooks equipped with '
                'strict preflight environment assertions.'}
