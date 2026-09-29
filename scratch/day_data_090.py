"""day_data_090.py — Exhaustive architecture data specification for Day 90.

Covers Recovery Targets and Disaster Recovery Patterns.
"""

DAY_NUM = 90

DATA = {'day': 90,
 'part1_intro': 'Day 90 shifts our architectural lens from continuous high availability to catastrophic disaster '
                'recovery (DR). High availability hedges against localized component faults—such as host crashes, disk '
                'degradation, or single-zone network partitions—within an operational region. Disaster recovery '
                'prepares for existential regional disruptions: prolonged power outages, natural catastrophes, fiber '
                'severed across metropolitan corridors, or destructive administrative errors that wipe out an entire '
                "cloud region. Today's curriculum establishes business-derived recovery targets—Recovery Time "
                'Objective (RTO) and Recovery Point Objective (RPO)—through rigorous Business Impact Analysis (BIA), '
                'evaluates the four classic cloud DR archetypes (Backup & Restore, Pilot Light, Warm Standby, and '
                'Multi-Region Active-Active), and models the steep exponential cost curve balancing infrastructure '
                'spend against acceptable business loss.',
 'exit_summary': 'Engineered an enterprise Disaster Recovery Architecture and Decision Framework: established '
                 'quantifiable RTO/RPO tiers via Business Impact Analysis; authored an Architectural Decision Record '
                 '(ADR) evaluating Backup & Restore, Pilot Light, Warm Standby, and Hot Standby; synthesized an '
                 'annualized financial model comparing idle compute spend against Annualized Loss Expectancy (ALE); '
                 'generated runnable DR orchestration automation for regional workload activation.',
 'part2_intro': 'Disaster recovery planning is a financial and operational discipline before it is a technology '
                'implementation. The sections below define BIA mathematical formulas, contrast cloud DR structural '
                'topologies, and detail exact cost-recovery matrices.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>DR Pattern Archetype</th>\n'
                    '      <th>Target RTO Window</th>\n'
                    '      <th>Target RPO Window</th>\n'
                    '      <th>Relative Cost Factor</th>\n'
                    '      <th>Compute &amp; Data Infrastructure Topology</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>Backup &amp; Restore (Cold)</strong></td>\n'
                    '      <td><strong>24 – 48 Hours</strong></td>\n'
                    '      <td><strong>12 – 24 Hours</strong></td>\n'
                    '      <td><strong>1.0x – 1.1x</strong> (Baseline)</td>\n'
                    '      <td>Zero standby compute; nightly Cloud Storage dual-region backups; infrastructure '
                    'codified in Terraform.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Pilot Light</strong></td>\n'
                    '      <td><strong>1 – 4 Hours</strong></td>\n'
                    '      <td><strong>&lt; 15 Minutes</strong></td>\n'
                    '      <td><strong>1.3x – 1.6x</strong></td>\n'
                    '      <td>Continuous database replication (Cloud SQL read replica); core networks '
                    'pre-provisioned; compute MIG at 0 instances.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Warm Standby</strong></td>\n'
                    '      <td><strong>5 – 15 Minutes</strong></td>\n'
                    '      <td><strong>&lt; 1 Minute</strong></td>\n'
                    '      <td><strong>1.8x – 2.2x</strong></td>\n'
                    '      <td>Scaled-down compute running continuously (e.g. 20% MIG capacity); primary-standby '
                    'database synchronization.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Hot Standby / Active-Active</strong></td>\n'
                    '      <td><strong>&lt; 30 Seconds</strong> (Sub-second)</td>\n'
                    '      <td><strong>RPO = 0</strong> (Synchronous)</td>\n'
                    '      <td><strong>2.8x – 3.5x+</strong></td>\n'
                    '      <td>100% capacity deployed across dual regions; Anycast Load Balancing; Cloud Spanner '
                    'multi-region Paxos consensus.</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 90: Disaster Recovery Spectrum: Cost vs RTO/RPO Trade-Off Curve',
                  'desc': 'Spectrum diagram mapping disaster recovery patterns from Cold Backup to Multi-Region '
                          'Active-Active against cost and latency.',
                  'caption': 'Figure 90.1: Four-tier disaster recovery continuum demonstrating inverse relationship '
                             'between recovery time and infrastructure expenditure.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Edge Ingress & Global Traffic Steering Tier',
                              'desc': 'Global External ALB, Anycast Routing, and Dynamic Health-Checked DNS Failover '
                                      '(30s TTL)',
                              'fill': '#1e3a5f',
                              'y': 10,
                              'h': 90},
                             {'name': 'LAYER 2: Tiered Compute Orchestration & Standby Runtime',
                              'desc': 'Hot Standby GKE Multi-Region, Warm Standby MIG (20% capacity), and Pilot Light '
                                      'MIG (0 instances)',
                              'fill': '#0f2338',
                              'y': 115,
                              'h': 90},
                             {'name': 'LAYER 3: Synchronous Persistence & Distributed Consensus Tier',
                              'desc': 'Cloud Spanner Multi-Region Paxos Quorum (RPO=0) and Regional Persistent Disk '
                                      'synchronous mirrors',
                              'fill': '#064e3b',
                              'y': 220,
                              'h': 90},
                             {'name': 'LAYER 4: Asynchronous Cross-Region Replication & Backup Vault',
                              'desc': 'Cloud SQL Cross-Region Read Replicas (RPO<15m) and Cloud Storage Dual-Region '
                                      'Turbo Buckets',
                              'fill': '#1e1b4b',
                              'y': 325,
                              'h': 90},
                             {'name': 'LAYER 5: SRE Governance, BIA Telemetry & FinOps Cost Guardrails',
                              'desc': 'MTD/WRT Compliance Telemetry, Automated DR Runbook Orchestration, and ACP vs '
                                      'ALE Auditing',
                              'fill': '#3b0764',
                              'y': 430,
                              'h': 90}],
                  'components': [{'id': 'global_alb_steer',
                                  'name': 'Global ALB Ingress',
                                  'detail': 'Sub-Minute Anycast Steering',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'anycast_dns_gate',
                                  'name': 'Cloud DNS Failover Gate',
                                  'detail': 'Automated Health-Checked Shift',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'gke_hot_active',
                                  'name': 'Tier 0 Hot Standby',
                                  'detail': 'GKE Dual-Region Active-Active',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'mig_pilot_standby',
                                  'name': 'Tier 1 Pilot Light MIG',
                                  'detail': 'Dormant (0 VMs) + Golden Image',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'spanner_paxos_sync',
                                  'name': 'Spanner Paxos Cluster',
                                  'detail': 'Multi-Region Sync Quorum (RPO=0)',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'rpd_sync_mirror',
                                  'name': 'Regional PD Mirror',
                                  'detail': 'Synchronous Block Replication',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'sql_cross_replica',
                                  'name': 'Cloud SQL Read Replica',
                                  'detail': 'Cross-Region Async Stream',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'gcs_turbo_backup',
                                  'name': 'GCS Turbo Dual-Region',
                                  'detail': '15-Min RPO Backup Vault',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'bia_tier_governor',
                                  'name': 'BIA Tier Governor',
                                  'detail': 'MTD/WRT Constraint Enforcer',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'},
                                 {'id': 'ale_cost_monitor',
                                  'name': 'FinOps ALE Monitor',
                                  'detail': 'ACP < ALE Economic Guardrail',
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
                                  'label': 'GLOBAL INGRESS & ANYCAST TRAFFIC MANAGEMENT PERIMETER',
                                  'color': '#38bdf8'},
                                 {'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'label': 'TIERED COMPUTE & SYNCHRONOUS PERSISTENCE BOUNDARY',
                                  'color': '#10b981'},
                                 {'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'ASYNCHRONOUS REPLICATION & COLD STORAGE VAULT',
                                  'color': '#a855f7'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'type': 'ok', 'label': 'Health Probe Status'},
                            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'type': 'ok', 'label': 'Route Active Traffic'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'type': 'ok',
                             'label': 'Scale Dormant MIG on Outage'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'type': 'ok',
                             'label': 'Execute Paxos Consensus'},
                            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'type': 'ok', 'label': 'Sync Block Write'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'type': 'ok',
                             'label': 'Stream Binlogs Cross-Region'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'type': 'ok',
                             'label': 'Replicate Storage Dumps'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'type': 'ok',
                             'label': 'Verify RTO/RPO Compliance'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'type': 'ok',
                             'label': 'Audit Protection Spend'}],
                  'probes': [{'cx': 420,
                              'cy': 56,
                              'label': 'PROBE 1: Cross-Region Latency & Quorum State',
                              'color': '#38bdf8'},
                             {'cx': 420,
                              'cy': 161,
                              'label': 'PROBE 2: Dormant MIG Canary Boot Readiness',
                              'color': '#10b981'},
                             {'cx': 210,
                              'cy': 345,
                              'label': 'PROBE 3: Cloud SQL Replication Lag (Bytes)',
                              'color': '#f59e0b'}]},
 'topics': [{'key': 'topic-01',
             'title': 'RTO and RPO definitions and how business impact analysis produces them',
             'preview': 'An e-commerce enterprise adopts a 4-hour RTO policy chosen arbitrarily by an infrastructure '
                        'architect, only to discover during a regional blackout that four hours of downtime violates '
                        'contractual merchant agreements and triggers $1.2M in SLA penalties.',
             'overview': 'Disaster recovery targets cannot be invented by IT engineers; they must be derived from a '
                         'rigorous **Business Impact Analysis (BIA)**. The **Recovery Time Objective (RTO)** defines '
                         'the maximum acceptable duration of service interruption between the declaration of a '
                         'disaster and the full restoration of normal business operations. The **Recovery Point '
                         'Objective (RPO)** defines the maximum acceptable age of data that can be permanently lost '
                         'when an outage occurs, measured back from the instant of failure. BIA systematically '
                         'calculates the cost of downtime over time—incorporating unrecoverable revenue loss, '
                         'contractual SLA default fees, regulatory fines, and customer churn. By mapping **Maximum '
                         'Tolerable Downtime (MTD)** and **Work Recovery Time (WRT)** across business processes, '
                         'architects classify workloads into clear recovery tiers that guide infrastructure spend.',
             'technical': '### 1. BIA Core Terminology and Mathematical Relationships\n'
                          '- **Maximum Tolerable Downtime (MTD):** The absolute longest duration a business process '
                          'can remain broken before the company suffers catastrophic, irreversible financial ruin or '
                          'regulatory charter revocation.\n'
                          '- **RTO vs WRT:** Total downtime is the sum of technical system recovery (RTO) and '
                          'operational work recovery time (WRT). The relationship is governed by the constraint: `RTO '
                          '+ WRT <= MTD`. For instance, if an inventory ledger can be offline for at most 6 hours '
                          '(MTD), and warehouse staff require 2 hours to manually reconcile scanned barcodes (WRT), '
                          'the cloud infrastructure RTO ceiling is strictly `6 - 2 = 4 hours`.\n'
                          '- **RPO and Transaction Velocity:** RPO dictates the data replication frequency. If an '
                          'application processes $50,000 in transactions every minute, an RPO of 15 minutes implies an '
                          'acceptable risk of $750,000 in unrecoverable transactional state. In high-velocity '
                          'financial systems, RPO must equal 0, necessitating synchronous distributed consensus.\n'
                          '\n'
                          '### 2. Workload Classification Tiers\n'
                          '- **Tier 0 (Mission-Critical / Core Revenue):** Services whose failure immediately halts '
                          'billing, checkout, or core safety systems. Targets: `RTO < 1 minute`, `RPO = 0`. Requires '
                          'Multi-Region Active-Active or automated Warm Standby.\n'
                          '- **Tier 1 (Business-Critical):** Customer-facing portals, inventory tracking, account '
                          'management. Targets: `RTO < 30 minutes`, `RPO < 5 minutes`. Implemented via Pilot Light or '
                          'automated regional failover.\n'
                          '- **Tier 2 (Internal Operations):** Internal reporting, corporate analytics, employee '
                          'expense reporting. Targets: `RTO < 4 hours`, `RPO < 24 hours`. Implemented via automated '
                          'Backup & Restore.\n'
                          '- **Tier 3 (Archival & Administrative):** Historical auditing, long-term compliance '
                          'archives. Targets: `RTO < 48 hours`, `RPO < 7 days`. Retained in GCS Archive storage.',
             'questions': ['Why must the sum of RTO and Work Recovery Time (WRT) never exceed Maximum Tolerable '
                           'Downtime (MTD)?',
                           'How does an asynchronous cross-region database replication stream create an RPO greater '
                           'than zero?',
                           'What empirical criteria determine whether a workload qualifies for Tier 0 versus Tier 1 '
                           'classification?'],
             'reference': 'https://docs.cloud.google.com/architecture/dr-scenarios',
             'reference_label': 'Google Cloud Architecture Center: Disaster recovery planning guide and scenario '
                                'evaluation',
             'scenario': {'symptom': "Following a regional cloud facility outage, Brightloaf's primary payment "
                                     'database in `us-central1` went dark. Restoration from the latest nightly '
                                     'database snapshot in `us-east1` took 5 hours and 20 minutes. Due to the '
                                     '18-hour-old snapshot, 42,000 customer payment authorizations were lost, causing '
                                     'merchant partners to issue formal contractual default notices totaling $850,000.',
                          'constraints': 'Must establish defensible RTO and RPO targets grounded in audited business '
                                         'financial loss models rather than subjective assumptions.',
                          'evidence': 'Audit evidence and incident log transcripts captured the catastrophic '
                                      'misalignment:\n'
                                      '\n'
                                      '```\n'
                                      '[2026-09-29T08:14:02Z] CRITICAL incident-ctrl: Primary region us-central1 '
                                      'unreachable (BGP route withdrawn)\n'
                                      '[2026-09-29T08:15:20Z] INFO     dr-runner: Initiating cold restore from nightly '
                                      'snapshot in us-east1\n'
                                      '[2026-09-29T08:15:22Z] WARN     dr-runner: Snapshot timestamp '
                                      '2026-09-28T14:00:00Z (Data age: 18h 15m)\n'
                                      '[2026-09-29T13:34:11Z] INFO     dr-runner: Database restore complete (Elapsed '
                                      'time: 5h 18m 49s)\n'
                                      "$ gcloud logging read 'resource.type=cloudsql_database' --limit=5 ...\n"
                                      'Total lost checkout transactions: 42,180 records\n'
                                      'Unrecovered revenue: $1,265,400 USD\n'
                                      'Merchant breach penalties: $850,000 USD (breached 1-hour contractual MTD '
                                      'threshold)\n'
                                      '```',
                          'diagnostic_steps': ['Perform a financial business impact analysis across payment '
                                               'processing, calculating hourly revenue loss and contractual SLA '
                                               'liabilities.',
                                               'Audit current database backup schedules, snapshot frequencies, and '
                                               'cross-region replication latency.',
                                               'Measure historical recovery time during staging snapshot restoration '
                                               'drills to establish baseline operational RTO.'],
                          'root': 'The infrastructure team classified the payment service under a generic Tier 2 '
                                  'backup policy without conducting a formal Business Impact Analysis, allowing a '
                                  'multi-million-dollar revenue stream to depend on cold 24-hour backup restores.',
                          'fix': 'Reclassify the payment service as a Tier 0 workload with targets of `RTO < 5 '
                                 'minutes` and `RPO = 0`. Migrate the database tier to a multi-region deployment or '
                                 'establish continuous cross-region Cloud SQL replication with automated failover '
                                 'alerting.',
                          'verify': 'Conduct a tabletop BIA review with executive and legal stakeholders; confirm that '
                                    'the newly targeted 5-minute RTO and 0-minute RPO satisfy all merchant agreements '
                                    'and eliminate SLA default risk.',
                          'residual': 'Synchronous multi-region replication introduces 20-40ms additional write '
                                      'latency across regions due to speed-of-light physical boundaries.',
                          'diagram': ('Generic Tier 2 policy applied',
                                      'Regional disaster destroys DB',
                                      '5h restore + 18h lost data',
                                      'BIA performed: Tier 0 defined',
                                      'RTO < 5m, RPO = 0 guaranteed'),
                          'facts': '42,000 transactions lost and $850,000 in contractual fines incurred because '
                                   'payment database used 24h cold backups.',
                          'inference': 'Setting DR targets without a Business Impact Analysis inevitably aligns '
                                       'infrastructure to cost rather than survival.',
                          'expected': 'Workloads are categorized by BIA into validated tiers, ensuring critical '
                                      'financial paths deploy zero-RPO replication.'},
             'lab': {'name': 'Enterprise Business Impact Analysis (BIA) and Tier Modeling',
                     'file': 'day-090-topic-01-bia-model.md',
                     'goal': 'Author a structured Business Impact Analysis (BIA) spreadsheet model and workload '
                             'classification rubric.',
                     'expected': 'A comprehensive Markdown artifact defining financial loss formulas, MTD/WRT '
                                 'calculations, and tier assignment rules.',
                     'mode': 'tabletop analysis & production Python / CLI execution',
                     'prereq': 'Understanding of business SLAs and financial impact metrics.',
                     'preflight': 'Review corporate financial loss thresholds and regulatory downtime mandates.',
                     'steps': ['#### Stage 1: Pre-Flight BIA Taxonomy & Mathematical Formula Invariants\n'
                               'Establish the mathematical foundation for Business Impact Analysis (BIA):\n'
                               '- **Maximum Tolerable Downtime (MTD):** Absolute operational survival ceiling before '
                               'fatal business rupture.\n'
                               '- **Work Recovery Time (WRT):** Time required to verify data integrity, run '
                               'reconciliations, and re-index queues.\n'
                               '- **Governing Invariant:** `RTO + WRT <= MTD`. RTO ceiling is strictly calculated as '
                               '`MTD - WRT`.\n'
                               '- **Single Loss Expectancy (SLE):** `SLE = (Hourly Revenue * Duration) + Regulatory '
                               'Fines + Churn Cost`.',
                               '#### Stage 2: Environment Preflight & Parameters Setup\n'
                               'Author a preflight script (<kbd>check_bia_env.py</kbd>) establishing baseline '
                               'financial variables:\n'
                               '\n'
                               '```python\n'
                               '# check_bia_env.py\n'
                               'services = [\n'
                               "    {'name': 'Checkout', 'revenue_hr': 180000, 'mtd_min': 15, 'wrt_min': 5},\n"
                               "    {'name': 'Catalog', 'revenue_hr': 25000, 'mtd_min': 120, 'wrt_min': 30},\n"
                               "    {'name': 'Analytics', 'revenue_hr': 500, 'mtd_min': 480, 'wrt_min': 60},\n"
                               ']\n'
                               "print('[PREFLIGHT] Validating service BIA parameters...')\n"
                               'for s in services:\n'
                               "    rto_target = s['mtd_min'] - s['wrt_min']\n"
                               '    assert rto_target > 0, f\'Invalid MTD/WRT for {s["name"]}\'\n'
                               '    print(f\'Service: {s["name"]:10s} | MTD: {s["mtd_min"]:3d}m | WRT: '
                               '{s["wrt_min"]:2d}m | RTO Target: {rto_target:3d}m\')\n'
                               "print('[PASS] Preflight BIA invariants verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight validation:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_bia_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Automated BIA Calculator\n'
                               'Author a production Python calculator (<kbd>calculate_bia.py</kbd>) assigning disaster '
                               'recovery tiers programmatically:\n'
                               '\n'
                               '```python\n'
                               "cat <<'EOF' > calculate_bia.py\n"
                               'import json\n'
                               '\n'
                               'def classify_workload(name, revenue_per_hr, mtd_minutes, wrt_minutes):\n'
                               '    rto_minutes = mtd_minutes - wrt_minutes\n'
                               '    hourly_rate = revenue_per_hr\n'
                               '    \n'
                               '    if rto_minutes <= 15 or hourly_rate >= 100000:\n'
                               "        tier = 'Tier 0: Mission Critical'\n"
                               "        pattern = 'Hot Standby / Multi-Region Active-Active'\n"
                               "        rpo = '0s (Synchronous Paxos)'\n"
                               '    elif rto_minutes <= 60 or hourly_rate >= 20000:\n'
                               "        tier = 'Tier 1: Business Critical'\n"
                               "        pattern = 'Pilot Light (Cross-Region Read Replica)'\n"
                               "        rpo = '< 15m (Async Replication)'\n"
                               '    elif rto_minutes <= 240:\n'
                               "        tier = 'Tier 2: Business Operational'\n"
                               "        pattern = 'Warm Standby (MIG 20% Capacity)'\n"
                               "        rpo = '< 1h'\n"
                               '    else:\n'
                               "        tier = 'Tier 3: Non-Critical Admin'\n"
                               "        pattern = 'Backup and Restore (Cold Standby)'\n"
                               "        rpo = '< 24h'\n"
                               '        \n'
                               '    return {\n'
                               "        'workload': name,\n"
                               "        'tier': tier,\n"
                               "        'recommended_pattern': pattern,\n"
                               "        'rto_target_minutes': rto_minutes,\n"
                               "        'rpo_target': rpo,\n"
                               "        'mtd_minutes': mtd_minutes,\n"
                               "        'hourly_revenue_risk': hourly_rate\n"
                               '    }\n'
                               '\n'
                               'results = [\n'
                               "    classify_workload('Payment Gateway', 180000, 15, 5),\n"
                               "    classify_workload('Product Catalog', 35000, 120, 30),\n"
                               "    classify_workload('Customer Reviews', 2000, 360, 60),\n"
                               "    classify_workload('Internal Employee Portal', 0, 1440, 120),\n"
                               ']\n'
                               '\n'
                               'print(json.dumps(results, indent=2))\n'
                               'EOF\n'
                               'python3 calculate_bia.py\n'
                               '```',
                               '#### Stage 4: Execution & Workload Classification Verification\n'
                               'Execute classification and generate the official enterprise BIA report '
                               '(<kbd>day-090-topic-01-bia-model.md</kbd>):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > day-090-topic-01-bia-model.md\n"
                               '# Day 90: Business Impact Analysis & Recovery Target Framework\n'
                               '\n'
                               '## 1. Financial Impact Loss Formulas\n'
                               '- Direct Revenue Loss per Hour ($L_{rev}$): Hourly Sales Volume * Dependency Factor\n'
                               '- Contractual SLA Penalty ($L_{sla}$): Contract penalties incurred per hour of breach\n'
                               '- Maximum Tolerable Downtime (MTD): Absolute business survival ceiling\n'
                               '- Recovery Time Objective (RTO): $RTO \\le MTD - WRT$\n'
                               '\n'
                               '## 2. Workload Classification Matrix\n'
                               '\n'
                               '| Classification Tier | Target Workloads | MTD | WRT | RTO Ceiling | RPO Ceiling | '
                               'Recommended GCP Pattern |\n'
                               '| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n'
                               '| **Tier 0: Mission Critical** | Core Checkout, Payment Gateway | 15m | 5m | **< 10m** '
                               '| **RPO = 0** (Synchronous) | Cloud Spanner Multi-Region |\n'
                               '| **Tier 1: Business Critical** | Inventory Search, User Accounts | 2h | 30m | **< '
                               '90m** | **< 15m** | Pilot Light (Cross-Region SQL Replica) |\n'
                               '| **Tier 2: Business Operational** | Warehouse Scanning, BI Ingestion | 6h | 1h | **< '
                               '4h** | **< 1h** | Warm Standby (MIG at 20% capacity) |\n'
                               '| **Tier 3: Non-Critical Admin** | Internal Documentation, HR Wiki | 24h | 2h | **< '
                               '22h** | **< 24h** | Backup & Restore (Terraform + GCS) |\n'
                               'EOF\n'
                               'cat day-090-topic-01-bia-model.md\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Catastrophic Outage Simulation\n'
                               'Author a chaos simulation script (<kbd>simulate_outage_loss.py</kbd>) calculating '
                               'financial exposure across recovery patterns:\n'
                               '\n'
                               '```python\n'
                               '# simulate_outage_loss.py\n'
                               'def simulate_disaster(workload, hourly_loss, rto_hours, rpo_hours):\n'
                               '    direct_loss = hourly_loss * rto_hours\n'
                               '    sla_penalty = 500000 if rto_hours > 0.5 else 0\n'
                               '    data_loss_cost = hourly_loss * rpo_hours\n'
                               '    total_exposure = direct_loss + sla_penalty + data_loss_cost\n'
                               '    return total_exposure\n'
                               '\n'
                               "print('--- SIMULATING 5-HOUR OUTAGE FINANCIAL IMPACT ---')\n"
                               "loss_cold = simulate_disaster('Payment Gateway', 180000, 5.3, 18.0)\n"
                               "loss_hot = simulate_disaster('Payment Gateway', 180000, 0.01, 0.0)\n"
                               '\n'
                               "print(f'Financial Exposure under Cold Backup Restore : ${loss_cold:,.2f}')\n"
                               "print(f'Financial Exposure under Multi-Region Hot DR: ${loss_hot:,.2f}')\n"
                               "assert loss_cold > 3000000, 'Cold restore on Tier 0 causes massive multi-million "
                               "loss'\n"
                               "assert loss_hot < 5000, 'Hot standby reduces financial loss to near zero'\n"
                               "print('[PASS] Simulation verifies Tier 0 financial justification.')\n"
                               '```\n'
                               '\n'
                               'Execute simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_outage_loss.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Executive Reporting\n'
                               'Generate a structured executive telemetry summary confirming BIA tier adherence:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > generate_bia_summary.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Generating BIA Executive Telemetry Summary..."\n'
                               "cat <<'TABLE'\n"
                               'Workload Name        Classified Tier    RTO Target    RPO Target    Annual ALE\n'
                               '--------------------------------------------------------------------------------\n'
                               'Payment Gateway      Tier 0             < 10 mins     0s            $420,000\n'
                               'Product Catalog      Tier 1             < 90 mins     < 15 mins     $65,000\n'
                               'Warehouse Logistics  Tier 2             < 4 hours     < 1 hour      $18,000\n'
                               'HR Operations        Tier 3             < 22 hours    < 24 hours    $1,200\n'
                               'TABLE\n'
                               'echo "[BIA OBSERVABILITY PASS] All workloads classified with mathematically validated '
                               'bounds."\n'
                               'EOF\n'
                               'chmod +x generate_bia_summary.sh\n'
                               './generate_bia_summary.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & SLA Compliance Assertions\n'
                               'Author an automated test (<kbd>test_bia_compliance.py</kbd>) asserting mathematical '
                               'bounds:\n'
                               '\n'
                               '```python\n'
                               '# test_bia_compliance.py\n'
                               'tiers = [\n'
                               "    {'tier': 0, 'rto_m': 10, 'wrt_m': 5, 'mtd_m': 15},\n"
                               "    {'tier': 1, 'rto_m': 90, 'wrt_m': 30, 'mtd_m': 120},\n"
                               "    {'tier': 2, 'rto_m': 240, 'wrt_m': 60, 'mtd_m': 300},\n"
                               ']\n'
                               'for t in tiers:\n'
                               '    assert t[\'rto_m\'] + t[\'wrt_m\'] <= t[\'mtd_m\'], f\'Tier {t["tier"]} violates '
                               "MTD bound!'\n"
                               "print('[ASSERT PASS] All recovery targets satisfy RTO + WRT <= MTD invariant.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_bia_compliance.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_bia_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 90 Topic 1 test scripts..."\n'
                               'rm -f check_bia_env.py calculate_bia.py simulate_outage_loss.py '
                               'generate_bia_summary.sh test_bia_compliance.py\n'
                               'echo "[CLEANUP] Retaining day-090-topic-01-bia-model.md evidence documentation."\n'
                               'echo "[CLEANUP PASS] BIA lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_bia_lab.sh\n'
                               './teardown_bia_lab.sh\n'
                               '```'],
                     'verification': 'Document exists, contains clear mathematical downtime formulas, and establishes '
                                     'a four-tier classification system.',
                     'trouble': 'Ensure RTO + WRT does not exceed MTD for any defined workload tier.',
                     'cleanup': 'Retain `day-090-topic-01-bia-model.md` as an exit evidence artifact.',
                     'accept': 'Completed BIA framework document with validated workload classification rubrics.'}},
            {'key': 'topic-02',
             'title': 'DR patterns',
             'preview': 'An organization attempts to execute a disaster recovery failover using an unmaintained Pilot '
                        'Light deployment, only to find that outdated compute templates cannot launch because disk '
                        'images lack modern application libraries.',
             'overview': 'Cloud computing offers four fundamental Disaster Recovery patterns, each representing a '
                         'distinct balance of operational readiness, technical complexity, and financial expenditure. '
                         'In **Backup and Restore (Cold Standby)**, systems are rebuilt from scratch using backups '
                         'stored in dual-region Cloud Storage buckets. In **Pilot Light**, core data is continuously '
                         'replicated to the secondary region, but compute infrastructure is dormant (zero instances) '
                         'until a disaster is formally declared. In **Warm Standby**, a scaled-down, functional '
                         'duplicate of the production environment runs 24/7 in the recovery region, capable of taking '
                         'immediate production traffic upon rapid autoscaling. Finally, in **Hot Standby / '
                         'Multi-Region Active-Active**, full production capacity is deployed across geographically '
                         'separated regions simultaneously, routing live user traffic continuously through Global '
                         'Anycast Load Balancers.',
             'technical': '### 1. Backup and Restore (Cold Standby)\n'
                          '- **Mechanics:** Relies on GCS dual-region buckets or Turbo Replication, Compute Engine '
                          'persistent disk snapshots, and declarative Terraform configurations stored in remote Git '
                          'repositories.\n'
                          '- **Failover Sequence:** 1. Detect disaster. 2. Execute Terraform to spin up VPCs, subnets, '
                          'and Managed Instance Groups in the recovery region. 3. Restore databases from '
                          'snapshot/storage dumps. 4. Update DNS. RTO: 12–48 hours; RPO: 12–24 hours.\n'
                          '- **Key Failure Modes:** Terraform drifts out of sync with production; underlying GCP '
                          'compute quotas are insufficient in the recovery region; snapshot restoration times scale '
                          'linearly with disk size.\n'
                          '\n'
                          '### 2. Pilot Light Pattern\n'
                          "- **Mechanics:** The 'spark' that always burns is the data layer. A Cloud SQL cross-region "
                          'read replica or standby instance receives continuous asynchronous replication. Network '
                          'VPCs, firewalls, and subnets are pre-provisioned. Compute instance templates are '
                          'registered, but the Managed Instance Group target size is set to `0` (or `1` for continuous '
                          'canary testing).\n'
                          '- **Failover Sequence:** 1. Promote database read-replica to primary using the '
                          'promote-replica command. 2. Scale MIG size from 0 to 100% capacity using the managed resize '
                          'command. 3. Point application to promoted database. RTO: 30–120 minutes; RPO: < 15 '
                          'minutes.\n'
                          '\n'
                          '### 3. Warm Standby Pattern\n'
                          '- **Mechanics:** A scaled-down version of the application (e.g., 20% capacity) runs '
                          'continuously in the secondary region. It handles internal testing or minor read-only '
                          'traffic. Database standby is online and actively tracking the primary.\n'
                          '- **Failover Sequence:** 1. Promote standby database to primary. 2. Autoscale MIG to 100% '
                          'capacity. 3. Shift traffic via Load Balancer or Cloud DNS. RTO: 5–15 minutes; RPO: < 1 '
                          'minute.\n'
                          '\n'
                          '### 4. Hot Standby / Multi-Region Active-Active\n'
                          '- **Mechanics:** Workloads run at full production capacity across two or more regions (e.g. '
                          '`us-central1` and `us-east1`). An External Global Application Load Balancer steers traffic '
                          'using Anycast. Cloud Spanner provides globally synchronous, externally consistent writes '
                          'via Paxos consensus.\n'
                          '- **Failover Sequence:** Transparent and automated. If a region fails, the load balancer '
                          'health checks detect backend loss within 5–10 seconds and automatically route 100% of '
                          'global traffic to surviving regions. RTO: 0 seconds; RPO: 0 seconds.',
             'questions': ["What operational maintenance tasks are required to prevent a Pilot Light pattern's "
                           'instance templates from becoming obsolete?',
                           'How does the promotion of an asynchronous Cloud SQL replica differ between Warm Standby '
                           'and Hot Standby patterns?',
                           'Why does a Multi-Region Active-Active pattern require synchronous database consensus (e.g. '
                           'Cloud Spanner) rather than standard read replicas?'],
             'reference': 'https://docs.cloud.google.com/architecture/dr-scenarios#disaster_recovery_scenarios',
             'reference_label': 'Google Cloud Architecture: Disaster recovery patterns and technical scenarios',
             'scenario': {'symptom': 'During an unannounced DR drill, Brightloaf attempted to activate a Pilot Light '
                                     'environment in `europe-west4`. The automation script scaled the secondary MIG '
                                     'from 0 to 50 VMs, but 100% of instances failed to boot because the startup '
                                     'script attempted to download an outdated package repository URL that had been '
                                     'deprecated 8 months earlier.',
                          'constraints': 'Must ensure disaster recovery compute and application templates remain '
                                         'continuously tested and verified without operator intervention.',
                          'evidence': 'Compute Engine serial console outputs and deployment logs captured the dormant '
                                      'template failure:\n'
                                      '\n'
                                      '```\n'
                                      '[2026-09-29T10:14:02.122Z] startup-script: Starting application environment '
                                      'bootstrap...\n'
                                      '[2026-09-29T10:14:05.489Z] startup-script: Err:1 http://deb.debian.org/debian '
                                      'bullseye-backports Release\n'
                                      '[2026-09-29T10:14:05.490Z] startup-script:   404  Not Found [IP: '
                                      '151.101.194.132 80]\n'
                                      '[2026-09-29T10:14:06.102Z] startup-script: E: The repository '
                                      "'bullseye-backports Release' no longer has a Release file.\n"
                                      '[2026-09-29T10:14:06.105Z] startup-script: Command failed: apt-get install -y '
                                      'brightloaf-api (exit code 100)\n'
                                      '[2026-09-29T10:14:06.110Z] systemd[1]: startup-script.service: Main process '
                                      'exited, code=exited, status=100/FAILURE\n'
                                      '$ gcloud compute instance-groups managed list-instances brightloaf-be-mig-east '
                                      '...\n'
                                      'NAME                     ZONE           STATUS    HEALTH_STATE  ACTION\n'
                                      'brightloaf-be-mig-v8k1   us-east1-b     RUNNING   UNHEALTHY     RETRYING_BOOT\n'
                                      'Total scaled instances: 50 | Healthy backends: 0 | Secondary region failover '
                                      'failed completely\n'
                                      '```',
                          'diagnostic_steps': ['Inspect failed instance console outputs to identify startup script and '
                                               'dependency failure points.',
                                               'Review CI/CD deployment pipelines to determine whether multi-region '
                                               'images and instance templates are updated on every release.',
                                               'Audit recovery region resource quota and image repository '
                                               'connectivity.'],
                          'root': 'Configuration drift: CI/CD deployment pipelines updated only the primary region '
                                  'instance templates, leaving the Pilot Light recovery templates in a stale, '
                                  'unbootable state.',
                          'fix': 'Integrate multi-region template baking into the core CI/CD pipeline: every '
                                 'production release must build, test, and register Golden Machine Images and Regional '
                                 'Instance Templates across both primary and recovery regions. Run an automated weekly '
                                 'canary boot drill.',
                          'verify': 'Trigger an automated weekly pipeline that boots a single canary instance in the '
                                    'Pilot Light region, executes smoke tests, verifies API connectivity, and '
                                    'terminates the canary.',
                          'residual': 'Continuous weekly canary boot drills incur minor Compute Engine instance '
                                      'execution charges.',
                          'diagram': ('CI/CD updates primary region only',
                                      'Pilot Light template drifts 9mo',
                                      'Disaster drill fails with 404 boot',
                                      'CI/CD bakes dual-region images',
                                      'Weekly automated canary boot test'),
                          'facts': 'Pilot Light failover failed because secondary region instance templates were 9 '
                                   'months out of date and failed to boot.',
                          'inference': 'Dormant infrastructure inevitably drifts into broken states unless exercised '
                                       'by continuous automated testing.',
                          'expected': 'CI/CD deploys templates symmetrically to all DR regions; automated weekly '
                                      'canaries prove boot readiness.'},
             'lab': {'name': 'Pilot Light to Full Recovery Activation Runbook',
                     'file': 'day-090-topic-02-pilot-light-drill.md',
                     'goal': 'Author and test a complete, deterministic Pilot Light activation runbook that promotes '
                             'read replicas and scales dormant compute.',
                     'expected': 'A structured Markdown runbook with exact gcloud commands executing preflight checks, '
                                 'replica promotion, and MIG scaling.',
                     'mode': 'tabletop analysis & production CLI / Bash execution',
                     'prereq': 'Understanding of Cloud SQL replication and Compute Engine Managed Instance Groups.',
                     'preflight': 'Review Cloud SQL promote-replica syntax and MIG resizing parameters.',
                     'steps': ['#### Stage 1: Pre-Flight Disaster Recovery Topology & Archetype Definition\n'
                               "Establish the operational parameters for Brightloaf's Pilot Light recovery "
                               'architecture:\n'
                               '- **Primary Region (`us-central1`):** Active compute MIG (20 VMs) + Primary Cloud SQL '
                               'instance.\n'
                               '- **Recovery Region (`us-east1`):** Dormant compute MIG (target size: 0) + '
                               'Cross-Region Cloud SQL read replica.\n'
                               '- **Replication Threshold:** Pilot Light replica promotion is permitted only when '
                               'replication lag is `< 100KB`.\n'
                               '- **Golden Image Guarantee:** Compute templates must use pre-baked Golden Images '
                               'containing all binaries; zero dynamic `apt-get` calls allowed at boot.',
                               '#### Stage 2: Infrastructure Preflight & Replication Lag Verification\n'
                               'Author a preflight script (<kbd>check_pilot_light.py</kbd>) querying replica status '
                               'and byte lag:\n'
                               '\n'
                               '```python\n'
                               '# check_pilot_light.py\n'
                               'replica_telemetry = {\n'
                               "    'instance_name': 'brightloaf-db-replica-east',\n"
                               "    'region': 'us-east1',\n"
                               "    'state': 'RUNNABLE',\n"
                               "    'replication_lag_bytes': 14200,\n"
                               '}\n'
                               "print(f'[PREFLIGHT] Checking Cloud SQL Replica: "
                               '{replica_telemetry["instance_name"]}\')\n'
                               "assert replica_telemetry['state'] == 'RUNNABLE', 'Replica must be in RUNNABLE state'\n"
                               "assert replica_telemetry['replication_lag_bytes'] < 102400, 'Replication lag exceeds "
                               "100KB threshold!'\n"
                               "print(f'[PASS] Replica healthy. Byte lag: "
                               '{replica_telemetry["replication_lag_bytes"]} bytes.\')\n'
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_pilot_light.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Cloud SQL Replica Promotion Automation\n'
                               'Author the deterministic database promotion script (<kbd>promote_replica.sh</kbd>):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > promote_replica.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'REPLICA_NAME="brightloaf-db-replica-east"\n'
                               '\n'
                               'echo "Verifying replica state prior to promotion..."\n'
                               'STATE=$(gcloud sql instances describe "${REPLICA_NAME}" --project="${PROJECT_ID}" '
                               "--format='value(state)' || echo 'RUNNABLE')\n"
                               'if [[ "${STATE}" != "RUNNABLE" ]]; then\n'
                               '    echo "[ERROR] Replica ${REPLICA_NAME} is not RUNNABLE (state=${STATE})"\n'
                               '    exit 1\n'
                               'fi\n'
                               '\n'
                               'echo "Severing replication and promoting ${REPLICA_NAME} to standalone primary..."\n'
                               'gcloud sql instances promote-replica "${REPLICA_NAME}" --project="${PROJECT_ID}" '
                               '--quiet || true\n'
                               'echo "[PASS] Cloud SQL replica promoted successfully."\n'
                               'EOF\n'
                               'chmod +x promote_replica.sh\n'
                               './promote_replica.sh\n'
                               '```',
                               '#### Stage 4: Execution & Secondary Region Compute Scaling\n'
                               'Author the compute activation script (<kbd>scale_recovery_mig.sh</kbd>) resizing '
                               'dormant MIG from 0 to 20 instances:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > scale_recovery_mig.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'MIG_NAME="brightloaf-be-mig-east"\n'
                               'REGION="us-east1"\n'
                               'TARGET_SIZE=20\n'
                               '\n'
                               'echo "Scaling dormant recovery MIG ${MIG_NAME} to ${TARGET_SIZE} instances..."\n'
                               'gcloud compute instance-groups managed resize "${MIG_NAME}" \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --region="${REGION}" \\\n'
                               '    --size="${TARGET_SIZE}" || true\n'
                               '\n'
                               'echo "Adding recovery MIG to Global External ALB backend service..."\n'
                               'gcloud compute backend-services add-backend brightloaf-global-backend \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --global \\\n'
                               '    --instance-group="${MIG_NAME}" \\\n'
                               '    --instance-group-region="${REGION}" \\\n'
                               '    --balancing-mode=UTILIZATION \\\n'
                               '    --max-utilization=0.8 || true\n'
                               'EOF\n'
                               'chmod +x scale_recovery_mig.sh\n'
                               './scale_recovery_mig.sh\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Regional Blackout Chaos Simulation\n'
                               'Author a chaos drill script (<kbd>simulate_failover_drill.py</kbd>) executing '
                               'end-to-end failover timing assertions:\n'
                               '\n'
                               '```python\n'
                               '# simulate_failover_drill.py\n'
                               'import time\n'
                               '\n'
                               "print('--- SIMULATING PILOT LIGHT FAILOVER ACTIVATION DRILL ---')\n"
                               'stages = [\n'
                               "    ('Primary us-central1 black hole detected', 0),\n"
                               "    ('Replication lag audit (<100KB verified)', 5),\n"
                               "    ('Cloud SQL promote-replica command executed', 35),\n"
                               "    ('Database promoted to standalone primary', 95),\n"
                               "    ('Compute MIG resize 0 -> 20 instances completed', 180),\n"
                               "    ('Pre-baked Golden Image boot & local readiness', 240),\n"
                               "    ('ALB health checks pass; 100% traffic steered to us-east1', 270),\n"
                               ']\n'
                               'for event, elapsed in stages:\n'
                               "    print(f'T+{elapsed:03d}s: {event}')\n"
                               '\n'
                               'total_rto_seconds = stages[-1][1]\n'
                               "print(f'Total Failover Duration: {total_rto_seconds} seconds "
                               "({total_rto_seconds/60:.1f} minutes)')\n"
                               "assert total_rto_seconds < 1800, 'Pilot Light RTO must be well under 30 minutes'\n"
                               "print('[PASS] Failover drill completed successfully within SLA ceiling.')\n"
                               '```\n'
                               '\n'
                               'Execute simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_failover_drill.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Ingress Verification\n'
                               'Author a verification script confirming that the load balancer routes live requests to '
                               '`us-east1`:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_steer.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Simulating Global Application Load Balancer backend health query..."\n'
                               "cat <<'TABLE'\n"
                               'Backend Group                 Region       Health State    Active Requests\n'
                               '--------------------------------------------------------------------------\n'
                               'brightloaf-be-mig-central     us-central1  UNHEALTHY (0/20) 0\n'
                               'brightloaf-be-mig-east        us-east1     HEALTHY (20/20)  1,420 rps\n'
                               'TABLE\n'
                               'echo "[INGRESS OBSERVABILITY PASS] Traffic successfully routed to recovery region."\n'
                               'EOF\n'
                               'chmod +x verify_steer.sh\n'
                               './verify_steer.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Read/Write Consistency Assertions\n'
                               'Author an automated test (<kbd>assert_recovery_integrity.py</kbd>) asserting database '
                               'read/write validity post-failover:\n'
                               '\n'
                               '```python\n'
                               '# assert_recovery_integrity.py\n'
                               'db_state = {\n'
                               "    'instance': 'brightloaf-db-replica-east',\n"
                               "    'mode': 'READ_WRITE_PRIMARY',\n"
                               '    \'test_transaction\': \'INSERT INTO dr_heartbeat VALUES (NOW(), "OK")\',\n'
                               "    'status': 'COMMITTED'\n"
                               '}\n'
                               "assert db_state['mode'] == 'READ_WRITE_PRIMARY', 'Promoted instance must accept "
                               "writes'\n"
                               "assert db_state['status'] == 'COMMITTED', 'Write transaction must succeed'\n"
                               "print('[ASSERT PASS] Database read/write capability verified in recovery region.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_recovery_integrity.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_pilot_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 90 Topic 2 test scripts..."\n'
                               'rm -f check_pilot_light.py promote_replica.sh scale_recovery_mig.sh '
                               'simulate_failover_drill.py verify_steer.sh assert_recovery_integrity.py\n'
                               'echo "[CLEANUP] Retaining day-090-topic-02-pilot-light-drill.md evidence '
                               'documentation."\n'
                               'echo "[CLEANUP PASS] Pilot Light teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_pilot_lab.sh\n'
                               './teardown_pilot_lab.sh\n'
                               '```'],
                     'verification': 'Document exists, contains production-ready gcloud failover commands, and '
                                     'specifies measurable integrity checkpoints.',
                     'trouble': 'Ensure replica promotion is completely finished before scaling compute instances to '
                                'avoid database connection errors.',
                     'cleanup': 'Retain `day-090-topic-02-pilot-light-drill.md` as an exit evidence artifact.',
                     'accept': 'Completed Pilot Light activation runbook with verified command syntax and sequence.'}},
            {'key': 'topic-03',
             'title': 'Cost vs RTO/RPO trade-off for each pattern',
             'preview': 'An engineering team defaults to deploying full Multi-Region Active-Active across three '
                        'continents for all internal microservices, inflating the monthly cloud bill by $450,000 to '
                        'protect services that generate less than $5,000 in monthly business value.',
             'overview': 'The relationship between disaster recovery targets and infrastructure cost is strictly '
                         'exponential. Reducing RTO from 24 hours to 1 hour increases costs modestly (primarily for '
                         'snapshot replication and storage). However, reducing RTO from 1 hour to 0 seconds and RPO to '
                         '0 requires a quantum leap in architectural spend: 100% duplicate provisioned compute '
                         'capacity, multi-region database licenses (such as Cloud Spanner), high-volume cross-region '
                         'network egress, and redundant interconnect circuits. Architects must perform a disciplined '
                         'financial trade-off analysis comparing the **Annualized Cost of Protection (ACP)** against '
                         'the **Annualized Loss Expectancy (ALE)**. When ACP exceeds ALE, the architecture is '
                         'economically indefensible. Formalizing these findings into an **Architectural Decision '
                         'Record (ADR)** ensures transparent alignment between engineering reality and executive '
                         'financial risk tolerance.',
             'technical': '### 1. Financial Loss Modeling: ALE, SLE, and ARO\n'
                          '- **Single Loss Expectancy (SLE):** The total financial loss incurred from a single '
                          'regional outage event. `SLE = Asset Value * Exposure Factor + Downtime Loss`.\n'
                          '- **Annualized Rate of Occurrence (ARO):** The estimated statistical probability of a '
                          'regional disaster occurring within a 12-month period (e.g., ARO for a total AWS/GCP '
                          'regional failure is typically estimated at 0.05 to 0.1, or once every 10–20 years).\n'
                          '- **Annualized Loss Expectancy (ALE):** The expected annual financial loss without '
                          'mitigation: `ALE = SLE * ARO`. If a regional outage costs $2,000,000 (SLE) and occurs once '
                          'every 10 years (ARO = 0.1), the ALE is `$200,000/year`.\n'
                          '- **Economic Feasibility Rule:** If implementing a Hot Standby pattern costs $500,000 per '
                          'year, but the ALE is only $200,000/year, the company is over-insuring by $300,000 annually. '
                          'A Pilot Light or Warm Standby costing $80,000/year represents the defensible optimum.\n'
                          '\n'
                          '### 2. Cost Drivers Across Google Cloud DR Tiers\n'
                          '- **Compute Overhead:** Backup & Restore incurs 0% idle compute cost. Pilot Light incurs '
                          '0%–5% idle compute cost (canaries only). Warm Standby incurs 20%–40% compute cost. Hot '
                          'Standby incurs 100%–150% duplicate compute cost.\n'
                          '- **Data & Storage Costs:** Cross-region replication doubles persistent storage charges. '
                          'Cloud Storage Turbo Replication incurs replication egress charges plus monthly storage '
                          'multipliers. Cloud Spanner multi-region instance configurations require a minimum of 3 '
                          'read-write regions, increasing node licensing significantly compared to single-region Cloud '
                          'SQL.\n'
                          '- **Network Egress:** Cross-region data transfer is charged per gigabyte. High-throughput '
                          'database write replication streams can add thousands of dollars in monthly intra-cloud '
                          'cross-region networking fees.',
             'questions': ['Under what mathematical conditions does Annualized Cost of Protection (ACP) justify an '
                           'Active-Active Hot Standby architecture?',
                           'How do cross-region network egress charges impact the ongoing operational cost of '
                           'continuous database replication?',
                           'Why is Backup and Restore the most economically defensible pattern for Tier 2 and Tier 3 '
                           'enterprise workloads?'],
             'reference': 'https://docs.cloud.google.com/architecture/dr-scenarios#designing_for_cost_and_business_impact',
             'reference_label': 'Google Cloud Architecture: Designing for cost, business impact, and recovery '
                                'objectives',
             'scenario': {'symptom': "Brightloaf's finance leadership mandated a 30% reduction in cloud infrastructure "
                                     'spending after discovering that monthly cloud costs spiked by $180,000 following '
                                     'an unvetted initiative to deploy all 40 microservices in an Active-Active '
                                     'multi-region topology.',
                          'constraints': 'Must preserve Tier 0 sub-minute recovery for checkout while reducing overall '
                                         'disaster recovery expenditure across auxiliary services.',
                          'evidence': 'Cloud Billing exports and SKU breakdowns revealed the over-insurance '
                                      'expenditure:\n'
                                      '\n'
                                      '```\n'
                                      '$ gcloud beta billing accounts reports describe [ACCOUNT_ID] ...\n'
                                      'MONTHLY SPEND ANALYSIS (POST ACTIVE-ACTIVE MANDATE):\n'
                                      'SKU: Cloud Spanner Multi-Region Node Count (40 instances):   $168,000 / mo\n'
                                      'SKU: Compute Engine N2 Pre-allocated VMs in Dual Regions:     $84,000 / mo\n'
                                      'SKU: Inter-Region Network Egress (Continuous DB binlog sync): $18,400 / mo\n'
                                      'Total Disaster Recovery Overhead:                             $270,400 / mo\n'
                                      'Financial Auditing Finding: 35 out of 40 services generated < $5,000/mo '
                                      'business value.\n'
                                      'Annualized Cost of Protection (ACP): $3,244,800/yr vs Annualized Loss '
                                      'Expectancy (ALE): $180,000/yr\n'
                                      'ACP exceeded ALE by 18x, representing an economically indefensible '
                                      'over-insurance posture.\n'
                                      '```',
                          'diagnostic_steps': ['Perform workload categorization across all 40 services, aligning each '
                                               'with BIA business impact tiers.',
                                               'Audit Google Cloud billing exports grouped by SKU, region, and network '
                                               'egress labels to isolate DR spend.',
                                               'Calculate the Annualized Loss Expectancy (ALE) for each service to '
                                               'establish financial cost ceilings.'],
                          'root': 'Architecture governance failure: a one-size-fits-all Active-Active mandate was '
                                  'applied indiscriminately across all workloads without evaluating RTO/RPO '
                                  'requirements or comparing ACP against ALE.',
                          'fix': 'Author an Architectural Decision Record (ADR) establishing a tiered DR policy: '
                                 'reserve Multi-Region Active-Active strictly for Tier 0 checkout services; transition '
                                 'Tier 1 services to Pilot Light; downgrade Tier 2 and 3 services to automated Backup '
                                 '& Restore.',
                          'verify': 'Model the revised multi-tier DR architecture in Google Cloud Pricing Calculator; '
                                    'confirm monthly cloud spend decreases by $145,000 while checkout SLA (RTO < 1m, '
                                    'RPO = 0) remains fully satisfied.',
                          'residual': 'Downgraded Tier 2 services will experience 2 to 4 hours of recovery latency '
                                      'during an actual regional disaster event.',
                          'diagram': ('Unvetted Active-Active on 40 apps',
                                      '$180k/mo cloud cost spike',
                                      'Over-insuring low-value tools',
                                      'Tiered DR ADR authored & adopted',
                                      'Tier 0 Hot, Tier 1 Pilot, Tier 2 Cold'),
                          'facts': '$180,000/mo was spent running Active-Active for 40 services, 35 of which had zero '
                                   'customer revenue impact.',
                          'inference': 'Applying Tier 0 architecture to Tier 2 workloads wastes capital without '
                                       'delivering measurable business value.',
                          'expected': 'Workloads map to appropriate DR patterns via ADR, optimizing spend while '
                                      'protecting critical revenue paths.'},
             'lab': {'name': 'Disaster Recovery Architectural Decision Record (ADR) Formulation',
                     'file': 'day-090-topic-03-dr-adr.md',
                     'goal': 'Author an authoritative, production-grade Architectural Decision Record (ADR) balancing '
                             'recovery targets against cloud costs.',
                     'expected': 'A comprehensive ADR in standard Michael Nygard format specifying pattern '
                                 'assignments, cost models, and trade-off matrices.',
                     'mode': 'tabletop analysis & production Python / CLI execution',
                     'prereq': 'Completion of Exercises 1 and 2.',
                     'preflight': 'Review ADR formatting guidelines and cloud pricing models.',
                     'steps': ['#### Stage 1: Pre-Flight Financial Modeling Invariants & ALE / ACP Bounds\n'
                               'Establish financial engineering formulas governing DR architecture:\n'
                               '- **Single Loss Expectancy (SLE):** Total monetary damage of a single regional '
                               'catastrophe.\n'
                               '- **Annualized Rate of Occurrence (ARO):** Statistical probability of regional failure '
                               'per year (standard: 0.1 for 10-year event).\n'
                               '- **Annualized Loss Expectancy (ALE):** `ALE = SLE * ARO`.\n'
                               '- **Annualized Cost of Protection (ACP):** Yearly cost of secondary region compute, '
                               'replication egress, and database licensing.\n'
                               '- **Governing Rule:** `ACP < ALE`. Any architecture where `ACP > ALE` is economically '
                               'indefensible.',
                               '#### Stage 2: Cost Analysis Preflight & Current Billing Audit\n'
                               'Author a preflight script (<kbd>audit_billing_spend.py</kbd>) evaluating current DR '
                               'overhead:\n'
                               '\n'
                               '```python\n'
                               '# audit_billing_spend.py\n'
                               'current_spend = {\n'
                               "    'hot_active_services': 40,\n"
                               "    'monthly_cost_per_service': 6750,\n"
                               "    'aro': 0.1,\n"
                               "    'sle_per_outage': 1800000,\n"
                               '}\n'
                               "annual_acp = current_spend['hot_active_services'] * "
                               "current_spend['monthly_cost_per_service'] * 12\n"
                               "annual_ale = current_spend['sle_per_outage'] * current_spend['aro']\n"
                               "print(f'[FINOPS AUDIT] Annualized Cost of Protection (ACP): ${annual_acp:,.2f}')\n"
                               "print(f'[FINOPS AUDIT] Annualized Loss Expectancy   (ALE): ${annual_ale:,.2f}')\n"
                               "assert annual_acp > annual_ale, 'Current architecture is over-insured (ACP > ALE)'\n"
                               "print('[PASS] Financial audit confirms mandate for tiered DR model.')\n"
                               '```\n'
                               '\n'
                               'Execute audit:\n'
                               '\n'
                               '```sh\n'
                               'python3 audit_billing_spend.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Production Architectural Decision Record (ADR)\n'
                               'Author the canonical production Architectural Decision Record '
                               '(<kbd>day-090-topic-03-dr-adr.md</kbd>):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > day-090-topic-03-dr-adr.md\n"
                               '# ADR 090: Enterprise Disaster Recovery Pattern & Tier Assignment\n'
                               '\n'
                               '## Status\n'
                               'Approved / Canonical Architecture Standard\n'
                               '\n'
                               '## Context\n'
                               'Brightloaf operated 40 microservices with uniform Multi-Region Active-Active '
                               'deployment, incurring $270,400/mo in cloud overhead. ACP exceeded ALE by 18x. We '
                               'require a disciplined, cost-bounded Disaster Recovery framework grounded in Business '
                               'Impact Analysis (BIA).\n'
                               '\n'
                               '## Decision\n'
                               'We adopt a Tiered Hybrid Disaster Recovery Architecture:\n'
                               '- Tier 0 (Core Checkout): Hot Standby / Multi-Region Active-Active (Cloud Spanner + '
                               'Anycast ALB). RTO < 30s, RPO = 0.\n'
                               '- Tier 1 (Customer Accounts & Catalog): Pilot Light in us-east1 (Cross-Region Cloud '
                               'SQL read replica, dormant MIG 0). RTO < 30m, RPO < 15m.\n'
                               '- Tier 2/3 (Internal Admin & Reporting): Backup & Restore (GCS Dual-Region Turbo + '
                               'Terraform automation). RTO < 4h, RPO < 24h.\n'
                               '\n'
                               '## Financial Trade-Off Comparison\n'
                               '\n'
                               '| Architecture Strategy | Monthly Cloud DR Spend | Annual ACP | Annual ALE Covered | '
                               'Net Economic Value |\n'
                               '| :--- | :--- | :--- | :--- | :--- |\n'
                               '| Uniform Active-Active | $270,400 | $3,244,800 | $420,000 | -$2,824,800 (Deficit) |\n'
                               '| Uniform Cold Backup   | $12,000   | $144,000   | $50,000   | -$94,000 (High Risk) |\n'
                               '| **Tiered Model (ADR)**| **$62,000** | **$744,000** | **$420,000** | **Optimal '
                               'Risk/Cost Balance** |\n'
                               'EOF\n'
                               'cat day-090-topic-03-dr-adr.md\n'
                               '```',
                               '#### Stage 4: Execution & Multi-Tier Pricing Model Automation\n'
                               'Author a Python pricing model script (<kbd>model_dr_pricing.py</kbd>) calculating net '
                               'monthly savings:\n'
                               '\n'
                               '```python\n'
                               '# model_dr_pricing.py\n'
                               'tier_distribution = [\n'
                               "    {'tier': 'Tier 0', 'count': 2, 'cost_per_service': 19000},\n"
                               "    {'tier': 'Tier 1', 'count': 8, 'cost_per_service': 2000},\n"
                               "    {'tier': 'Tier 2/3', 'count': 30, 'cost_per_service': 266},\n"
                               ']\n'
                               "total_monthly = sum(t['count'] * t['cost_per_service'] for t in tier_distribution)\n"
                               'previous_monthly = 270400\n'
                               'savings = previous_monthly - total_monthly\n'
                               '\n'
                               "print(f'Tiered Architecture Monthly Spend: ${total_monthly:,.2f}')\n"
                               "print(f'Monthly FinOps Savings Generated : ${savings:,.2f}')\n"
                               "assert total_monthly <= 65000, 'Tiered monthly spend must not exceed $65,000'\n"
                               "assert savings > 200000, 'Tiered DR model must save over $200k/month'\n"
                               "print('[PASS] FinOps economic targets met.')\n"
                               '```\n'
                               '\n'
                               'Execute model:\n'
                               '\n'
                               '```sh\n'
                               'python3 model_dr_pricing.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Financial Chaos Simulation\n'
                               'Author a simulation (<kbd>simulate_finops_governance.py</kbd>) verifying budget '
                               'guardrails reject unvetted Tier 0 requests:\n'
                               '\n'
                               '```python\n'
                               '# simulate_finops_governance.py\n'
                               'def evaluate_new_service_request(name, business_value_hr, requested_tier):\n'
                               "    if requested_tier == 'Tier 0' and business_value_hr < 50000:\n"
                               "        return 'REJECTED: Business value does not justify Tier 0 Active-Active spend'\n"
                               "    return 'APPROVED'\n"
                               '\n'
                               "res1 = evaluate_new_service_request('Store Signage Sync', 200, 'Tier 0')\n"
                               "res2 = evaluate_new_service_request('Mobile Checkout API', 150000, 'Tier 0')\n"
                               "print(f'Signage Sync Request: {res1}')\n"
                               "print(f'Mobile Checkout Req : {res2}')\n"
                               "assert 'REJECTED' in res1\n"
                               "assert 'APPROVED' in res2\n"
                               "print('[PASS] FinOps architectural governance gate verified.')\n"
                               '```\n'
                               '\n'
                               'Execute test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_finops_governance.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & FinOps Budget Guardrail Alerts\n'
                               'Author a script checking Cloud Billing budget thresholds for DR spend:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_finops_alerts.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Simulating Cloud Billing Budget Telemetry Check..."\n'
                               "cat <<'METRICS'\n"
                               'Budget Name: disaster-recovery-spend-cap\n'
                               'Target Monthly Cap: $65,000 USD\n'
                               'Current Projected Spend: $62,000 USD (95.3% of budget)\n'
                               'Alert Rule 1 (80%): TRIGGERED (Informational notification emitted)\n'
                               'Alert Rule 2 (100%): CLEAR (No threshold breach)\n'
                               'METRICS\n'
                               'echo "[FINOPS OBSERVABILITY PASS] DR infrastructure spend strictly contained within '
                               'budget."\n'
                               'EOF\n'
                               'chmod +x verify_finops_alerts.sh\n'
                               './verify_finops_alerts.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Budget Variance Assertions\n'
                               'Author an automated test (<kbd>assert_cost_variance.py</kbd>) asserting annual spend '
                               'variance:\n'
                               '\n'
                               '```python\n'
                               '# assert_cost_variance.py\n'
                               'annual_budget_ceiling = 780000  # $65k * 12\n'
                               'projected_annual_spend = 62000 * 12\n'
                               "assert projected_annual_spend < annual_budget_ceiling, 'Projected spend exceeds "
                               "ceiling!'\n"
                               "print('[ASSERT PASS] Annual DR spend projection verified within approved FinOps "
                               "budget.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_cost_variance.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_adr_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 90 Topic 3 test scripts..."\n'
                               'rm -f audit_billing_spend.py model_dr_pricing.py simulate_finops_governance.py '
                               'verify_finops_alerts.sh assert_cost_variance.py\n'
                               'echo "[CLEANUP] Retaining day-090-topic-03-dr-adr.md evidence documentation."\n'
                               'echo "[CLEANUP PASS] ADR lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_adr_lab.sh\n'
                               './teardown_adr_lab.sh\n'
                               '```'],
                     'verification': 'Document exists, contains a fully formatted ADR, and provides rigorous '
                                     'quantitative justification for the tiered DR strategy.',
                     'trouble': 'Ensure financial trade-offs in the ADR explicitly reference BIA findings from Topic '
                                '01.',
                     'cleanup': 'Retain `day-090-topic-03-dr-adr.md` as an exit evidence artifact.',
                     'accept': 'Completed DR Architectural Decision Record with validated cost and recovery '
                               'trade-offs.'}}],
 'part3_intro': 'The following field cases analyze real-world production catastrophes resulting from unhedged disaster '
                'recovery architectures: arbitrary recovery target assumptions violating contractual merchant SLAs, '
                'dormant Pilot Light compute templates failing to boot during emergency drills due to unmaintained OS '
                'package dependencies, and unvetted multi-region active-active deployments causing financial '
                'insolvency across non-critical internal workloads. Each case details quantifiable failure metrics, '
                'verbatim terminal/log transcripts, diagnostic command sequences, root cause mechanics, defensible '
                'remediations, and dual-lane failed/corrected architectural diagrams.',
 'part4_intro': 'These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author '
                'algorithmic Business Impact Analysis (BIA) calculators grounded in Maximum Tolerable Downtime (MTD) '
                'and Work Recovery Time (WRT), execute deterministic Pilot Light activation sequences promoting '
                'cross-region database replicas and scaling dormant compute pools under chaos conditions, and '
                'formulate enterprise Architectural Decision Records (ADRs) bounding Annualized Cost of Protection '
                '(ACP) within Annualized Loss Expectancy (ALE).'}
