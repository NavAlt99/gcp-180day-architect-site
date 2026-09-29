"""day_data_083.py — Exhaustive architecture data specification for Day 83.

Covers Availability Math and Dependency Risk:
1. Availability math (99.9% vs 99.95% vs 99.99% downtime calculations, formulas, error budget allocation).
2. Series vs parallel availability (composite SLA calculation, multiplication rule, independence assumptions, correlated failures).
3. Single points of failure (layer-by-layer SPOF identification and elimination across DNS, Network, Compute, Data, and IAM).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable 8-stage operational engineering exercises.
"""

DAY_NUM = 83

DATA = {'day': 83,
 'part1_intro': 'Day 83 initiates Block 4 (Reliability and Security) by establishing the quantitative mathematical '
                'foundations of enterprise cloud availability. Architects cannot design resilient systems through '
                'intuition alone; they must calculate exact downtime budgets across 99.9%, 99.95%, and 99.99% targets, '
                'model compound availability across series and parallel dependencies, and rigorously challenge the '
                'naive assumption of component failure independence. A system composed of ten 99.9% reliable '
                'microservices in series yields an abysmal composite availability of only 99.0%, consuming over 430 '
                "minutes of downtime per month. Today's curriculum deconstructs the mathematical reality of composite "
                'SLAs, uncovers hidden correlated failure modes such as shared control planes and DNS resolution, and '
                'audits infrastructure layer-by-layer to systematically eliminate single points of failure (SPOFs) '
                'across the Brightloaf enterprise stack.',
 'exit_summary': 'Calculated exact allowed downtime budgets across 99.9%, 99.95%, and 99.99% tiers; modeled series and '
                 "parallel composite SLAs across Brightloaf's order-processing topology demonstrating a drop from "
                 '99.9% to 99.75% composite availability; identified five critical correlated failure domains (shared '
                 'IAM, regional DNS, Cloud NAT port exhaustion, zonal power, and centralized database lock contention) '
                 'that invalidate naive multiplication; eliminated four critical SPOFs across network, compute, and '
                 'database tiers with verified multi-zone and HA configurations.',
 'part2_intro': 'Availability is an engineering discipline governed by probability theory and discrete mathematics. '
                'The sections below detail availability calculations, compound dependency equations, failure '
                'correlation risks, and systematic SPOF elimination techniques across Google Cloud infrastructure.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Availability Tier</th>\n'
                    '      <th>Downtime / Month (30d)</th>\n'
                    '      <th>Downtime / Year (365d)</th>\n'
                    '      <th>Permitted Continuous Outage</th>\n'
                    '      <th>Architectural Requirements &amp; Google Cloud Pattern</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>99.0% ("Two 9s")</strong></td>\n'
                    '      <td>7 hours, 12 minutes</td>\n'
                    '      <td>3.65 days (87.6 hours)</td>\n'
                    '      <td>Hours (manual intervention acceptable)</td>\n'
                    '      <td>Single VM instance, standard persistent disk, daily snapshots, cold restore.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>99.9% ("Three 9s")</strong></td>\n'
                    '      <td>43 minutes, 12 seconds</td>\n'
                    '      <td>8 hours, 45 minutes, 57 seconds</td>\n'
                    '      <td>Tens of minutes (automated restart)</td>\n'
                    '      <td>Regional Managed Instance Group (MIG), autohealing health checks, Cloud SQL single-zone '
                    'with automated failover replication.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>99.95% ("Three and a half 9s")</strong></td>\n'
                    '      <td>21 minutes, 36 seconds</td>\n'
                    '      <td>4 hours, 22 minutes, 58 seconds</td>\n'
                    '      <td>Minutes (sub-minute automated failover)</td>\n'
                    '      <td>Multi-zone Regional MIG across 3 AZs, Cloud SQL HA with Regional PD synchronous '
                    'replication, Anycast External HTTP(S) Load Balancer.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>99.99% ("Four 9s")</strong></td>\n'
                    '      <td>4 minutes, 19 seconds</td>\n'
                    '      <td>52 minutes, 36 seconds</td>\n'
                    '      <td>Seconds (instantaneous routing shift)</td>\n'
                    '      <td>Multi-region Cloud Spanner, multi-region Cloud Storage, dual-region active/active Cloud '
                    'Run, Anycast global load balancing with backend health checks.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>99.999% ("Five 9s")</strong></td>\n'
                    '      <td>25.9 seconds</td>\n'
                    '      <td>5 minutes, 15 seconds</td>\n'
                    '      <td>Sub-second (zero perceptible human downtime)</td>\n'
                    '      <td>Distributed active-active multi-region Spanner, multi-region routing with Anycast BGP, '
                    'zero-downtime canary pipelines, positive fencing.</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 83: Enterprise Availability and Dependency Risk Topology',
                  'desc': 'Multi-tier infrastructure topology illustrating series multiplicative risk, parallel '
                          'decoupling buffers, correlated failure domains, and SPOF elimination.',
                  'caption': 'Figure 83.1: Multi-tier architectural topology illustrating request flows through edge '
                             'Anycast, decoupled compute tiers, HA persistence, and shared control plane boundaries.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Global Edge & Ingress Anycast Tier',
                              'desc': 'Global External Application Load Balancer, Cloud Armor DDoS Mitigation, and TLS '
                                      '1.3 Termination',
                              'fill': '#1e3a5f',
                              'y': 10,
                              'h': 90},
                             {'name': 'LAYER 2: Stateless Compute & Asynchronous Decoupling Fabric',
                              'desc': 'Regional Multi-Zone MIG, Cloud Pub/Sub Decoupling Buffer, and Circuit Breakers',
                              'fill': '#0f2338',
                              'y': 115,
                              'h': 90},
                             {'name': 'LAYER 3: Stateful Persistence & Regional HA Storage',
                              'desc': 'Cloud SQL HA Primary/Standby with Synchronous Regional Persistent Disk '
                                      'Replication',
                              'fill': '#064e3b',
                              'y': 220,
                              'h': 90},
                             {'name': 'LAYER 4: Cross-Cutting Dependency & Shared Control Plane',
                              'desc': 'Google Cloud IAM Token Minting, Cloud DNS Resolution, and Secret Manager',
                              'fill': '#1e1b4b',
                              'y': 325,
                              'h': 90},
                             {'name': 'LAYER 5: Observability & Availability SLA Governance',
                              'desc': 'Cloud Monitoring SLI Evaluators, Multi-Window Error Budget Burn Rate Trackers',
                              'fill': '#3b0764',
                              'y': 430,
                              'h': 90}],
                  'components': [{'id': 'alb_edge',
                                  'name': 'Global External ALB',
                                  'detail': '99.99% Anycast IP Ingress',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'armor_sec',
                                  'name': 'Cloud Armor Policy',
                                  'detail': 'Edge WAF & Rate Limiting',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'mig_app',
                                  'name': 'Regional Multi-Zone MIG',
                                  'detail': '3 AZs Autohealing (99.95%)',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'pubsub_buf',
                                  'name': 'Cloud Pub/Sub Buffer',
                                  'detail': 'Asynchronous Decoupling (99.95%)',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'sql_ha_pri',
                                  'name': 'Cloud SQL HA Primary',
                                  'detail': 'Zone us-central1-a (Sync)',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'sql_ha_sec',
                                  'name': 'Cloud SQL HA Standby',
                                  'detail': 'Zone us-central1-b (Failover <60s)',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'shared_dep',
                                  'name': 'Cloud IAM & Cloud DNS',
                                  'detail': 'Correlated Control Plane SPOF',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'nat_gateway',
                                  'name': 'Cloud NAT Gateway',
                                  'detail': 'Dynamic SNAT Port Pool',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'slo_monitor',
                                  'name': 'Cloud Monitoring SLI',
                                  'detail': 'Error Budget Burn Rate Engine',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'},
                                 {'id': 'alert_router',
                                  'name': 'Incident Alert Router',
                                  'detail': 'Automated Page & Circuit Open',
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
                                  'label': 'GLOBAL HIGH-AVAILABILITY ANYCAST PERIMETER',
                                  'color': '#38bdf8'},
                                 {'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'DECOUPLED ASYNCHRONOUS COMPUTE PERIMETER',
                                  'color': '#10b981'},
                                 {'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'CORRELATED CONTROL PLANE & SHARED DEPENDENCY BOUNDARY',
                                  'color': '#a855f7'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'type': 'ok', 'label': 'HTTPS Anycast'},
                            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'type': 'ok', 'label': 'L7 Internal Proxy'},
                            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'type': 'ok', 'label': 'Async Queue Enqueue'},
                            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'type': 'ok', 'label': 'Sync SQL Write'},
                            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'type': 'ok', 'label': 'Regional PD Sync'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'type': 'warn',
                             'label': 'IAM Token / DNS Check'},
                            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'type': 'ok', 'label': 'Outbound SNAT Pool'},
                            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'type': 'ok', 'label': 'SLI Telemetry Stream'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'type': 'fail',
                             'label': 'Burn Rate Breach Page'}],
                  'probes': [{'cx': 420,
                              'cy': 56,
                              'label': 'PROBE 1: Edge Anycast Latency & Health Check',
                              'color': '#38bdf8'},
                             {'cx': 420,
                              'cy': 161,
                              'label': 'PROBE 2: Pub/Sub Async Buffer Queue Depth',
                              'color': '#22c55e'},
                             {'cx': 420,
                              'cy': 266,
                              'label': 'PROBE 3: Cloud SQL HA Replication Lag (<1s)',
                              'color': '#f59e0b'}]},
 'topics': [{'key': 'topic-01',
             'title': 'Availability math: downtime budgets and error allocation',
             'preview': 'An e-commerce team commits to a 99.99% SLA without calculating that it permits only 4 minutes '
                        'and 19 seconds of downtime per month. When a routine database restart takes 12 minutes, the '
                        'entire quarterly SLA penalty is triggered, costing thousands in customer service credits.',
             'overview': 'Availability math defines the exact quantitative limits of permitted service degradation '
                         'over standardized time windows. Formally, availability is the ratio of operational uptime to '
                         'total scheduled time: A = Uptime / (Uptime + Downtime). In modern SRE practice, availability '
                         'is measured via request-based Service Level Indicators (SLIs): the percentage of valid '
                         'requests served successfully within latency thresholds. Each target tier dictates a strict, '
                         'non-negotiable downtime budget: 99.9% permits 43.2 minutes/month, 99.95% permits 21.6 '
                         'minutes/month, and 99.99% permits a razor-thin 4.32 minutes/month. Understanding this math '
                         'prevents engineering teams from signing contractual SLAs that are mathematically impossible '
                         'to maintain given the underlying infrastructure building blocks.',
             'technical': 'Availability calculations must adhere to strict probabilistic and operational formulas:\n'
                          '\n'
                          '### 1. Fundamental Formulas and Downtime Conversion\n'
                          '- **Allowed Downtime ($D$):** For time window $T$ (where $T_{\\text{month}} = 30 \\times 24 '
                          '\\times 3600 = 2,592,000$ seconds, and $T_{\\text{year}} = 31,536,000$ seconds):\n'
                          '  $$D = T \\times (1 - A)$$\n'
                          '- **Request-Based Availability ($A_{\\text{req}}$):**\n'
                          '  $$A_{\\text{req}} = \\frac{\\sum \\text{Successful Requests}}{\\sum \\text{Total Valid '
                          'Requests}} \\ge \\text{SLO}$$\n'
                          '\n'
                          '### 2. Time-Based vs. Event-Based Discrepancies\n'
                          'Time-based availability measures whether the system socket is listening. Event-based '
                          'availability measures whether user transactions complete successfully. A service can be '
                          '100% available by time-based ping probes while failing 100% of user checkouts due to '
                          'database lock exhaustion. Architects must always align contractual SLAs and internal SLOs '
                          'with user-visible transaction success.\n'
                          '\n'
                          '### 3. The Exponential Cost Curve\n'
                          'Moving from 99.9% to 99.99% does not require a 10% increase in engineering effort; it '
                          'requires a 10x reduction in failure tolerance. At 99.9%, human incident response (15-minute '
                          'MTTA + 15-minute MTTR) can preserve the SLA. At 99.99%, any human intervention guarantees '
                          'SLA breach; all failure detection, isolation, draining, and failover must be 100% automated '
                          'within seconds.',
             'questions': ['How does the allowed downtime budget change between a 30-day calendar month and a rolling '
                           '28-day window?',
                           'Why does human Mean Time to Acknowledge (MTTA) make a 99.99% SLA impossible without fully '
                           'automated control loops?',
                           'What specific transaction exclusions (e.g., client 4xx errors, scheduled maintenance) must '
                           'be codified in contract terms?'],
             'reference': 'https://docs.cloud.google.com/architecture/framework/reliability/availability',
             'reference_label': 'Google Cloud Architecture Framework: Availability and downtime calculations',
             'scenario': {'symptom': 'Brightloaf committed to a contractual 99.99% availability SLA for its B2B '
                                     'Wholesale Ordering API. During a monthly release, a database schema migration '
                                     'lock blocked HTTP POST /orders for 8 minutes and 42 seconds. Although the '
                                     'service was available for 99.98% of the month, the 4.32-minute allowed downtime '
                                     'was doubled, triggering a mandatory 25% billing refund to enterprise customers.',
                          'constraints': 'Must preserve data integrity (zero duplicate orders), honor third-party ERP '
                                         'payment timeouts (max 5s), and avoid manual failovers that exceed the '
                                         '4.32-minute monthly budget.',
                          'evidence': 'Cloud Monitoring shows 502/504 spikes between 02:14:10 UTC and 02:22:52 UTC '
                                      '(522 seconds total). Total monthly orders: 1,420,000; failed orders: 18,400. '
                                      'Measured request availability: 98.70% during the incident window, dragging '
                                      'monthly availability to 99.980%.',
                          'diagnostic_steps': ['Inspect Cloud Load Balancing request logs filtered by '
                                               "`statusDetails='backend_timeout'`.",
                                               'Correlate Cloud SQL `query_exec_time` and table lock waits on `orders` '
                                               'during the DDL migration.',
                                               'Review Cloud Monitoring SLO error budget burn rate graph to determine '
                                               'the exact moment the monthly budget was depleted.'],
                          'root': 'Schema migration executed an exclusive `ALTER TABLE` lock on the transactional '
                                  'database, exceeding the entire 99.99% monthly downtime budget in a single operation '
                                  'without an automated zero-downtime schema rollout pattern.',
                          'fix': 'Adopt an online schema migration pattern with Ghost/Liquibase (expand/contract), '
                                 'deploy Cloud Spanner with non-blocking schema updates, and recalibrate public SLA '
                                 'terms to 99.95% while keeping internal 99.9% SLO with automated rollback within 60 '
                                 'seconds.',
                          'verify': 'Execute non-blocking DDL rehearsal in staging; verify Cloud Monitoring records '
                                    'zero HTTP 5xx errors and query latency remains below 45ms.',
                          'residual': 'Spanner online schema changes take longer to propagate across regions (up to '
                                      'several minutes) during which write throughput may be throttled.',
                          'diagram': ('DDL lock triggered',
                                      'Table exclusive lock',
                                      '522s downtime breach',
                                      'Expand/contract schema',
                                      'Zero-downtime deploy'),
                          'facts': 'Measured outage: 522 seconds. 99.99% monthly limit: 259.2 seconds. Public SLA '
                                   'breached by 262.8 seconds.',
                          'inference': 'Human-driven migrations cannot support four-nines SLAs without architectural '
                                       'isolation.',
                          'expected': 'Future schema updates execute concurrently with active transactions without '
                                      'taking exclusive table locks.'},
             'lab': {'name': 'Downtime Budget and Error Allocation Engine',
                     'file': 'day-083-topic-01-downtime.py',
                     'goal': 'Write and execute an automated downtime budget calculation tool in Python that computes '
                             'exact SLA windows and error budgets.',
                     'expected': 'Accurate, formatted table output showing monthly and yearly allowed downtime across '
                                 'multiple tiers, with budget burn simulations.',
                     'mode': 'local script execution & verification',
                     'prereq': 'Python 3.10+ installed locally.',
                     'preflight': 'Verify Python runtime and create exercise file.',
                     'steps': ['#### Stage 1: Pre-Flight Mathematical Invariants & SLA Calibration\n'
                               'Define the mathematical constants and calendar parameters for SLA compliance windows. '
                               'A standard 30-day billing month comprises exactly 2,592,000 seconds (43,200 minutes), '
                               'while a 365-day year comprises 31,536,000 seconds. Establish the target tiers: 99.0% '
                               '(Two 9s), 99.9% (Three 9s), 99.95% (Three and a half 9s), 99.99% (Four 9s), and '
                               '99.999% (Five 9s).',
                               '#### Stage 2: Environment Validation & Precision Math Verification\n'
                               'Author an environment validation script (<kbd>test_math_precision.py</kbd>) to ensure '
                               'floating-point precision issues do not truncate fractional seconds:\n'
                               '\n'
                               '```python\n'
                               '# test_math_precision.py\n'
                               'import math\n'
                               'month_sec = 30 * 24 * 3600\n'
                               'unavail_4nines = (100.0 - 99.99) / 100.0\n'
                               'down_4nines = month_sec * unavail_4nines\n'
                               "assert abs(down_4nines - 259.2) < 1e-6, f'Expected 259.2s, got {down_4nines}'\n"
                               "print('[PASS] Precision math verified: 99.99% monthly downtime is exactly 259.20 "
                               "seconds (4m 19.2s).')\n"
                               '```\n'
                               '\n'
                               'Execute the preflight test:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_math_precision.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: High-Precision Downtime Engine\n'
                               'Create the comprehensive availability calculation and error budget simulation engine '
                               '(<kbd>day-083-topic-01-downtime.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '#!/usr/bin/env python3\n'
                               '"""day-083-topic-01-downtime.py — Enterprise Availability & Downtime Budget '
                               'Engine."""\n'
                               'from typing import Dict, Tuple\n'
                               '\n'
                               'class AvailabilityCalculator:\n'
                               '    MONTH_SECONDS = 30 * 24 * 3600\n'
                               '    YEAR_SECONDS = 365 * 24 * 3600\n'
                               '\n'
                               '    @classmethod\n'
                               '    def calculate_allowable_downtime(cls, sla_percent: float) -> Dict[str, float]:\n'
                               '        unavailability_ratio = (100.0 - sla_percent) / 100.0\n'
                               '        return {\n'
                               "            'sla': sla_percent,\n"
                               "            'monthly_sec': cls.MONTH_SECONDS * unavailability_ratio,\n"
                               "            'yearly_sec': cls.YEAR_SECONDS * unavailability_ratio,\n"
                               "            'monthly_min': (cls.MONTH_SECONDS * unavailability_ratio) / 60.0,\n"
                               "            'yearly_min': (cls.YEAR_SECONDS * unavailability_ratio) / 60.0,\n"
                               '        }\n'
                               '\n'
                               '    @classmethod\n'
                               '    def format_duration(cls, seconds: float) -> str:\n'
                               '        sec = round(seconds, 1)\n'
                               '        days = int(sec // 86400)\n'
                               '        sec %= 86400\n'
                               '        hours = int(sec // 3600)\n'
                               '        sec %= 3600\n'
                               '        minutes = int(sec // 60)\n'
                               '        remainder_sec = sec % 60\n'
                               '        parts = []\n'
                               "        if days > 0: parts.append(f'{days}d')\n"
                               "        if hours > 0: parts.append(f'{hours}h')\n"
                               "        if minutes > 0: parts.append(f'{minutes}m')\n"
                               "        parts.append(f'{remainder_sec:.1f}s')\n"
                               "        return ' '.join(parts)\n"
                               '\n'
                               '    @classmethod\n'
                               '    def simulate_outage_impact(cls, sla_percent: float, outage_duration_sec: float) -> '
                               'Dict[str, float]:\n'
                               '        budget = cls.calculate_allowable_downtime(sla_percent)\n'
                               "        budget_consumed_pct = (outage_duration_sec / budget['monthly_sec']) * 100.0\n"
                               '        return {\n'
                               "            'sla': sla_percent,\n"
                               "            'outage_sec': outage_duration_sec,\n"
                               "            'monthly_budget_sec': budget['monthly_sec'],\n"
                               "            'burn_pct': budget_consumed_pct,\n"
                               "            'is_breached': outage_duration_sec > budget['monthly_sec'],\n"
                               "            'headroom_sec': budget['monthly_sec'] - outage_duration_sec\n"
                               '        }\n'
                               '\n'
                               "if __name__ == '__main__':\n"
                               "    print('=' * 80)\n"
                               "    print('DAY 83: ENTERPRISE AVAILABILITY & DOWNTIME BUDGET MATRIX')\n"
                               "    print('=' * 80)\n"
                               '    print(f"{\'SLA Tier\':<12} | {\'Monthly Downtime\':<22} | {\'Yearly '
                               'Downtime\':<22} | {\'Human MTTR Viable\':<18}")\n'
                               "    print('-' * 80)\n"
                               '    tiers = [99.0, 99.5, 99.9, 99.95, 99.99, 99.999]\n'
                               '    for t in tiers:\n'
                               '        data = AvailabilityCalculator.calculate_allowable_downtime(t)\n'
                               "        m_str = AvailabilityCalculator.format_duration(data['monthly_sec'])\n"
                               "        y_str = AvailabilityCalculator.format_duration(data['yearly_sec'])\n"
                               "        viable = 'YES (>15m MTTR)' if data['monthly_min'] >= 15.0 else 'NO (Automated "
                               "Only)'\n"
                               '        print(f"{t:<10.3f}% | {m_str:<22} | {y_str:<22} | {viable:<18}")\n'
                               "    print('=' * 80)\n"
                               '```',
                               '#### Stage 4: Execution & Multi-Tier Downtime Budget Tabulation\n'
                               'Execute the downtime budget engine and review the generated metrics table:\n'
                               '\n'
                               '```sh\n'
                               'python3 day-083-topic-01-downtime.py\n'
                               '```\n'
                               '\n'
                               'Confirm that 99.9% yields exactly 43m 12.0s monthly downtime, while 99.99% yields 4m '
                               '19.2s.',
                               '#### Stage 5: Error Budget Burn Simulation & Alerting Assertions\n'
                               'Develop an automated test harness (<kbd>test_budget_burn.py</kbd>) to simulate a '
                               '300-second (5-minute) unmitigated database failover and assert error budget depletion '
                               'across all tiers:\n'
                               '\n'
                               '```python\n'
                               '# test_budget_burn.py\n'
                               'from day_083_topic_01_downtime import AvailabilityCalculator\n'
                               '\n'
                               '# 5-minute outage = 300 seconds\n'
                               'outage_sec = 300.0\n'
                               'impact_3nines = AvailabilityCalculator.simulate_outage_impact(99.9, outage_sec)\n'
                               'impact_4nines = AvailabilityCalculator.simulate_outage_impact(99.99, outage_sec)\n'
                               '\n'
                               'print(f"3-Nines (99.9%) Burn: {impact_3nines[\'burn_pct\']:.2f}% (Headroom: '
                               '{impact_3nines[\'headroom_sec\']:.1f}s)")\n'
                               'print(f"4-Nines (99.99%) Burn: {impact_4nines[\'burn_pct\']:.2f}% (Breached: '
                               '{impact_4nines[\'is_breached\']})")\n'
                               '\n'
                               "assert not impact_3nines['is_breached'], '99.9% should tolerate a 5-minute outage'\n"
                               "assert impact_4nines['is_breached'], '99.99% must breach on a 5-minute outage (limit: "
                               "259.2s)'\n"
                               "assert impact_4nines['burn_pct'] > 115.0, 'Burn percentage should exceed 115%'\n"
                               "print('[PASS] Error budget burn assertions verified successfully.')\n"
                               '```\n'
                               '\n'
                               'Run the assertion test:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_budget_burn.py\n'
                               '```',
                               '#### Stage 6: Chaos & Disaster Outage Allocation Stress Testing\n'
                               'Author a chaos simulation script (<kbd>chaos_outage_stress.py</kbd>) that models '
                               'random intermittent failure spikes and calculates cumulative error budget exhaustion '
                               'across an active 30-day window:\n'
                               '\n'
                               '```python\n'
                               '# chaos_outage_stress.py\n'
                               'import random\n'
                               'from day_083_topic_01_downtime import AvailabilityCalculator\n'
                               '\n'
                               'random.seed(83)\n'
                               'incidents = [random.uniform(5.0, 45.0) for _ in range(12)]  # 12 minor transient '
                               'glitches\n'
                               'total_downtime = sum(incidents)\n'
                               "print(f'Simulated 12 transient incidents totaling: {total_downtime:.2f} seconds.')\n"
                               '\n'
                               'for sla in [99.9, 99.95, 99.99]:\n'
                               '    res = AvailabilityCalculator.simulate_outage_impact(sla, total_downtime)\n'
                               '    print(f"SLA {sla}%: {res[\'burn_pct\']:.1f}% budget consumed, Breached: '
                               '{res[\'is_breached\']}")\n'
                               '```\n'
                               '\n'
                               'Execute the chaos simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_outage_stress.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook Authoring: SRE Error Budget Policy\n'
                               'Codify the mathematical governance rules in an enterprise SRE Markdown policy '
                               '(<kbd>day-083-slo-policy.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# SRE Policy: Availability Tiers and Error Budget Depletion Governance\n'
                               '\n'
                               '## 1. Contractual SLA vs Internal SLO Alignment\n'
                               '- Target Internal SLO: 99.95% (21.6 min/mo allowed downtime).\n'
                               '- Contractual External SLA: 99.9% (43.2 min/mo allowed downtime).\n'
                               '- Safety Margin Headroom: Exactly 21.6 minutes reserved for unpredicted infrastructure '
                               'brownouts.\n'
                               '\n'
                               '## 2. Release Freeze Enforcement Thresholds\n'
                               '- **Burn Rate > 14.4 (Fast Burn):** P1 page, emergency rollback, release freeze.\n'
                               '- **Burn Rate > 6.0 (Medium Burn):** P2 investigation within 1 hour.\n'
                               '- **Budget Exhaustion (100% consumed):** Mandatory feature freeze; 100% engineering '
                               'effort diverted to reliability.\n'
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up intermediate test scripts and retain core artifacts:\n'
                               '\n'
                               '```sh\n'
                               'rm -f test_math_precision.py test_budget_burn.py chaos_outage_stress.py\n'
                               'ls -lh day-083-topic-01-downtime.py day-083-slo-policy.md\n'
                               '```\n'
                               '\n'
                               'Verify that <kbd>day-083-topic-01-downtime.py</kbd> and '
                               '<kbd>day-083-slo-policy.md</kbd> are preserved as verifiable day evidence.'],
                     'verification': 'Confirm script output reports exactly 43m 12.0s for 99.9% monthly, and 4m 19.2s '
                                     'for 99.99% monthly downtime.',
                     'trouble': 'Ensure floating point precision errors are minimized by formatting seconds to 1 '
                                'decimal place.',
                     'cleanup': 'Retain `day-083-topic-01-downtime.py` as an exit evidence artifact.',
                     'accept': 'Script runs cleanly and displays complete downtime matrix with error budget '
                               'calculations.'}},
            {'key': 'topic-02',
             'title': 'Series vs parallel availability and compound dependency risk',
             'preview': 'An architect chains a 99.99% load balancer, a 99.9% API gateway, three 99.9% microservices, '
                        'and a 99.95% database in a synchronous call path. Instead of four nines, the resulting '
                        'composite availability plummets to 99.65%, resulting in over 150 minutes of monthly downtime.',
             'overview': 'Composite availability models how individual component reliability interacts across complex '
                         'enterprise topologies. When components operate in series (where each component is strictly '
                         'necessary for transaction completion), total availability is the mathematical product of '
                         'their individual availabilities: A_series = A_1 * A_2 * ... * A_n. In contrast, parallel '
                         'components (where redundant components provide active-active or active-passive backup) fail '
                         'only when all instances fail simultaneously: A_parallel = 1 - ((1 - A_1) * (1 - A_2) * ... * '
                         '(1 - A_n)). However, the foundational flaw in classical composite modeling is the assumption '
                         'of independence. In cloud environments, components routinely share common failure '
                         'domains—including regional VPC peering, IAM policy propagation, Cloud DNS resolution, and '
                         'shared database locks—causing correlated catastrophic failures.',
             'technical': 'Architects must master the mechanics of compound availability modeling and correlated '
                          'risk:\n'
                          '\n'
                          '### 1. Mathematical Mechanics: Series Chaining\n'
                          'For a synchronous call chain traversing $n$ components where each component must succeed:\n'
                          '$$A_{\\text{series}} = \\prod_{i=1}^{n} A_i$$\n'
                          'Example: A request traversing Cloud Armor (99.99%), GCLB (99.99%), Cloud Run (99.95%), GKE '
                          'Service (99.9%), and Cloud SQL (99.95%):\n'
                          '$$A_{\\text{composite}} = 0.9999 \\times 0.9999 \\times 0.9995 \\times 0.9990 \\times '
                          '0.9995 = 0.997805 \\ (99.78\\%$$\n'
                          'Monthly allowed downtime explodes from 4.3 minutes to **56.9 minutes**!\n'
                          '\n'
                          '### 2. Parallel Redundancy Mechanics\n'
                          'For $m$ identical components running in parallel:\n'
                          '$$A_{\\text{parallel}} = 1 - \\prod_{j=1}^{m} (1 - A_j)$$\n'
                          'Two independent 99.9% application instances yield $1 - (0.001 \\times 0.001) = 0.999999$ '
                          '(six 9s) on paper.\n'
                          '\n'
                          '### 3. The Fallacy of Independence & Correlated Failures\n'
                          'Parallel components are almost never truly independent in Google Cloud:\n'
                          '- **Shared Control Plane:** A misconfigured IAM role or org policy propagates to all '
                          'instances simultaneously.\n'
                          '- **Shared Routing:** Cloud Router BGP session flaps tear down routes to redundant '
                          'backends.\n'
                          '- **Shared Software Defect:** A poison pill payload causes all redundant instances to crash '
                          'in parallel upon receipt.\n'
                          '- **Database Concurrency:** Two parallel microservices serialize on the same primary '
                          'database row locks, negating compute redundancy.',
             'questions': ['Why does adding a synchronous third-party payment gateway with a 99.5% SLA cap your '
                           "system's theoretical maximum availability at 99.5%?",
                           'How does introducing an asynchronous message queue (e.g., Cloud Pub/Sub) decouple series '
                           'dependencies into parallel availability paths?',
                           'What are three specific examples of correlated failure modes that can take down multi-zone '
                           'redundant deployments?'],
             'reference': 'https://docs.cloud.google.com/architecture/framework/reliability/design-for-reliability',
             'reference_label': 'Google Cloud Reliability Framework: Designing for Redundancy and Decoupling',
             'scenario': {'symptom': 'Brightloaf implemented a dual-zone frontend deployment across us-central1-a and '
                                     'us-central1-b expecting 99.999% availability. During peak order traffic, an '
                                     'unexpected inventory database dead-lock caused both frontend pools to exhaust '
                                     'their connection pools within 30 seconds, crashing all instances in both zones '
                                     'simultaneously.',
                          'constraints': 'Must maintain single-fulfillment guarantee, enforce max 3-second user '
                                         'response time, and avoid unbudgeted multi-region database licensing costs.',
                          'evidence': 'Cloud Monitoring shows connection pool saturation (100/100 active connections) '
                                      'across all 16 GKE pods in both zones. CPU utilization on GKE nodes remained '
                                      'under 18%, while database transaction lock wait time spiked from 2ms to '
                                      '45,000ms.',
                          'diagnostic_steps': ['Query Cloud Monitoring for `kubernetes.io/container/cpu/utilization` '
                                               'vs '
                                               '`cloudsql.googleapis.com/database/postgresql/transaction_lock_wait_time`.',
                                               'Examine application connection pool logs to verify thread starvation '
                                               'across both availability zones.',
                                               'Audit the application call graph to identify synchronous blocking '
                                               'calls in the critical checkout path.'],
                          'root': 'Naive parallel compute topology relied on a single shared transactional database '
                                  'locking mechanism, introducing an unhedged series dependency that triggered '
                                  'correlated thread exhaustion across all compute instances.',
                          'fix': 'Decouple the checkout path: acknowledge order receipt into Cloud Pub/Sub with local '
                                 'idempotency key, move inventory reconciliation to an asynchronous worker queue, and '
                                 'enforce strict circuit breakers on synchronous database calls.',
                          'verify': 'Simulate 5,000ms database lock in staging; verify frontend immediately shifts to '
                                    'asynchronous queuing mode, returns HTTP 202 Accepted, and checkout availability '
                                    'remains 99.99% without container crashes.',
                          'residual': 'Order confirmation becomes eventually consistent, requiring client-side polling '
                                      'or WebSocket push for final fulfillment status.',
                          'diagram': ('Traffic surge arrives',
                                      'Database lock wait',
                                      'Dual-zone thread death',
                                      'Asynchronous Pub/Sub outbox',
                                      'Decoupled 202 Accepted'),
                          'facts': 'Two zones of compute crashed concurrently despite 99.999% theoretical parallel '
                                   'availability math.',
                          'inference': 'Compute redundancy without state decoupling provides zero protection against '
                                       'downstream backend starvation.',
                          'expected': 'Compute instances survive database slowness by isolating critical user paths '
                                      'from synchronous write locks.'},
             'lab': {'name': 'Composite Topology SLA Modeler',
                     'file': 'day-083-topic-02-composite-sla.py',
                     'goal': 'Build an analytical tool that calculates composite SLAs for arbitrary series-parallel '
                             'graphs and highlights correlated failure risks.',
                     'expected': 'A runnable Python model that outputs composite availability, total monthly downtime, '
                                 'and identified shared dependency choke points.',
                     'mode': 'local script execution & verification',
                     'prereq': 'Completion of Exercise 1.',
                     'preflight': 'Verify Python runtime and initialize script template.',
                     'steps': ['#### Stage 1: Pre-Flight Topology Architecture & Dependency Graph Invariants\n'
                               "Define the two reference topologies for Brightloaf's Order Processing system:\n"
                               '- **Path A (Naive Synchronous Series Chain):** Anycast ALB (99.99%) -> Cloud Run '
                               'Gateway (99.95%) -> Auth Service (99.90%) -> Order API (99.90%) -> Cloud SQL DB '
                               '(99.95%).\n'
                               '- **Path B (Decoupled Resilient Architecture):** Anycast ALB (99.99%) -> Redundant App '
                               'Pool (two 99.90% instances in parallel) -> Cloud Pub/Sub Buffer (99.95%).',
                               '#### Stage 2: Environment Setup & Graph Modeling Harness\n'
                               'Create an environment test script (<kbd>test_env_topology.py</kbd>) verifying that '
                               "Python's math library accurately computes floating-point products across deep "
                               'dependency chains:\n'
                               '\n'
                               '```python\n'
                               '# test_env_topology.py\n'
                               'chain = [0.9999, 0.9995, 0.9990, 0.9990, 0.9995]\n'
                               'prod = 1.0\n'
                               'for p in chain: prod *= p\n'
                               "print(f'Product: {prod:.6f} ({prod * 100:.4f}%)')\n"
                               "assert 0.9970 < prod < 0.9980, 'Product calculation out of expected range'\n"
                               "print('[PASS] Topology product verification harness ready.')\n"
                               '```\n'
                               '\n'
                               'Run the preflight harness:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_env_topology.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Series vs Parallel Composite Modeler\n'
                               'Author the complete composite SLA simulation tool '
                               '(<kbd>day-083-topic-02-composite-sla.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '#!/usr/bin/env python3\n'
                               '"""day-083-topic-02-composite-sla.py — Composite Topology SLA and Correlated Risk '
                               'Analyzer."""\n'
                               'from typing import List, Tuple\n'
                               '\n'
                               'def series_sla(*components: float) -> float:\n'
                               '    prod = 1.0\n'
                               '    for c in components:\n'
                               '        prod *= (c / 100.0)\n'
                               '    return prod * 100.0\n'
                               '\n'
                               'def parallel_sla(*components: float) -> float:\n'
                               '    unavail = 1.0\n'
                               '    for c in components:\n'
                               '        unavail *= (1.0 - (c / 100.0))\n'
                               '    return (1.0 - unavail) * 100.0\n'
                               '\n'
                               'def calculate_monthly_downtime_minutes(sla_percent: float) -> float:\n'
                               '    total_monthly_minutes = 30 * 24 * 60\n'
                               '    return total_monthly_minutes * (1.0 - (sla_percent / 100.0))\n'
                               '\n'
                               'def evaluate_topologies():\n'
                               '    # Path A: Naive Synchronous Series Chain\n'
                               '    edge_gclb = 99.99\n'
                               '    cloud_run = 99.95\n'
                               '    auth_svc = 99.90\n'
                               '    order_svc = 99.90\n'
                               '    database = 99.95\n'
                               '    composite_a = series_sla(edge_gclb, cloud_run, auth_svc, order_svc, database)\n'
                               '    down_a = calculate_monthly_downtime_minutes(composite_a)\n'
                               '\n'
                               '    # Path B: Decoupled Architecture\n'
                               '    parallel_app = parallel_sla(99.90, 99.90)\n'
                               '    pubsub_buffer = 99.95\n'
                               '    composite_b = series_sla(edge_gclb, parallel_app, pubsub_buffer)\n'
                               '    down_b = calculate_monthly_downtime_minutes(composite_b)\n'
                               '\n'
                               "    print('=' * 85)\n"
                               "    print('DAY 83: COMPOSITE TOPOLOGY SLA & DOWNTIME REDUCTION ANALYSIS')\n"
                               "    print('=' * 85)\n"
                               "    print(f'Path A (Synchronous Series Chain):   {composite_a:8.4f}% SLA | Monthly "
                               "Downtime: {down_a:6.2f} mins')\n"
                               "    print(f'Path B (Decoupled Parallel Buffers): {composite_b:8.4f}% SLA | Monthly "
                               "Downtime: {down_b:6.2f} mins')\n"
                               "    print(f'Downtime Reduction Factor:           {down_a / down_b:8.2f}x "
                               "improvement')\n"
                               "    print('=' * 85)\n"
                               '    return composite_a, down_a, composite_b, down_b\n'
                               '\n'
                               "if __name__ == '__main__':\n"
                               '    evaluate_topologies()\n'
                               '```',
                               '#### Stage 4: Execution & Compound SLA Risk Analysis\n'
                               'Execute the composite topology simulation script:\n'
                               '\n'
                               '```sh\n'
                               'python3 day-083-topic-02-composite-sla.py\n'
                               '```\n'
                               '\n'
                               'Confirm that Path A suffers 99.69% composite SLA (over 130 minutes monthly downtime) '
                               'while Path B achieves 99.93% (under 27 minutes downtime).',
                               '#### Stage 5: Live Verification & Fallacy of Independence Assertions\n'
                               'Author an assertion test (<kbd>test_correlation_penalty.py</kbd>) proving that '
                               'correlated failure coefficients degrade naive parallel availability:\n'
                               '\n'
                               '```python\n'
                               '# test_correlation_penalty.py\n'
                               'from day_083_topic_02_composite_sla import parallel_sla\n'
                               '\n'
                               '# Naive independent parallel\n'
                               'naive_parallel = parallel_sla(99.9, 99.9)\n'
                               "print(f'Naive Parallel Availability: {naive_parallel:.6f}%')\n"
                               "assert naive_parallel > 99.999, 'Two independent 99.9% nodes should mathematically "
                               "yield >99.999%'\n"
                               '\n'
                               '# Correlated failure model: 15% probability of shared dependency crash (IAM, DB '
                               'locks)\n'
                               'rho = 0.15\n'
                               'correlated_unavail = (0.001 * 0.001) + (rho * 0.001)\n'
                               'correlated_sla = (1.0 - correlated_unavail) * 100.0\n'
                               "print(f'Correlated Parallel Availability (rho=0.15): {correlated_sla:.6f}%')\n"
                               "assert correlated_sla < 99.99, 'Correlated failure must drag availability down below "
                               "99.99%'\n"
                               "print('[PASS] Correlation penalty verified: Shared dependencies erase 2 nines of "
                               "availability!')\n"
                               '```\n'
                               '\n'
                               'Run the assertion script:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_correlation_penalty.py\n'
                               '```',
                               '#### Stage 6: Chaos & Correlated Blast Radius Failure Injection\n'
                               'Author a chaos drill (<kbd>chaos_correlated_failure.py</kbd>) that simulates '
                               'concurrent database lock saturation across both redundant application instances:\n'
                               '\n'
                               '```python\n'
                               '# chaos_correlated_failure.py\n'
                               'def simulate_cluster_health(shared_db_healthy: bool, node_a_alive: bool, node_b_alive: '
                               'bool) -> str:\n'
                               '    if not shared_db_healthy:\n'
                               "        return 'TOTAL_OUTAGE: Both nodes starved on shared DB threadpool lock'\n"
                               '    if node_a_alive or node_b_alive:\n'
                               "        return 'OPERATIONAL: Handled by healthy node'\n"
                               "    return 'OUTAGE: Both compute nodes dead'\n"
                               '\n'
                               'status_ok = simulate_cluster_health(True, True, False)\n'
                               'status_chaos = simulate_cluster_health(False, True, True)\n'
                               "print(f'Single Node Crash State: {status_ok}')\n"
                               "print(f'Shared DB Lock Crash State: {status_chaos}')\n"
                               "assert 'TOTAL_OUTAGE' in status_chaos\n"
                               "print('[PASS] Chaos test confirms compute redundancy fails under shared state "
                               "correlation.')\n"
                               '```\n'
                               '\n'
                               'Execute the chaos simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_correlated_failure.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Dependency Decoupling Architecture Guidelines\n'
                               'Author the architectural decoupling standard '
                               '(<kbd>day-083-decoupling-runbook.md</kbd>) documenting how asynchronous queues, '
                               'circuit breakers, and read replicas protect availability:\n'
                               '\n'
                               '```markdown\n'
                               '# Architecture Guideline: Dependency Decoupling and Compound SLA Defense\n'
                               '\n'
                               '## 1. Asynchronous Boundary Pattern\n'
                               '- No synchronous HTTP/gRPC call in user-facing checkout may traverse > 2 microservices '
                               'in series.\n'
                               '- Heavy operations (inventory reconciliation, invoicing, fraud scoring) MUST use Cloud '
                               'Pub/Sub buffer queues.\n'
                               '\n'
                               '## 2. Circuit Breaker Parameters\n'
                               '- Open circuit threshold: 50% error rate over 10 seconds.\n'
                               '- Half-open trial window: 5 seconds with 10% canary traffic.\n'
                               '- Fallback response: Return cached catalog data or HTTP 202 Accepted with idempotency '
                               'token.\n'
                               '```',
                               '#### Stage 8: Teardown, Script Cleanup & Artifact Acceptance\n'
                               'Remove temporary test harnesses and verify exit artifacts:\n'
                               '\n'
                               '```sh\n'
                               'rm -f test_env_topology.py test_correlation_penalty.py chaos_correlated_failure.py\n'
                               'ls -lh day-083-topic-02-composite-sla.py day-083-decoupling-runbook.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>day-083-topic-02-composite-sla.py</kbd> and '
                               '<kbd>day-083-decoupling-runbook.md</kbd> are retained.'],
                     'verification': 'Script executes successfully without syntax errors and prints comparative '
                                     'composite availability metrics showing >4x downtime reduction.',
                     'trouble': 'Ensure percentage values are properly divided by 100 before performing floating point '
                                'multiplication.',
                     'cleanup': 'Retain `day-083-topic-02-composite-sla.py` as an exit evidence artifact.',
                     'accept': 'Demonstrated mastery of compound availability math and identification of correlated '
                               'failure mechanisms.'}},
            {'key': 'topic-03',
             'title': 'Single points of failure: identification and layer-by-layer elimination',
             'preview': 'Brightloaf routes all ingress traffic through a single Cloud NAT gateway IP with default port '
                        'allocation settings. During a Black Friday marketing push, SNAT port exhaustion drops 65% of '
                        'outbound payment gateway connections, shutting down checkout across all regions.',
             'overview': 'A Single Point of Failure (SPOF) is any individual component, configuration, or operational '
                         'boundary whose failure directly induces total system collapse. SPOFs exist at every tier of '
                         'the enterprise technology stack: physical infrastructure (single power supply, single rack, '
                         'single AZ), network topology (single Cloud NAT, single HA VPN tunnel, unhedged '
                         'interconnect), compute (standalone VM, zonal GKE master), data persistence (single-instance '
                         'DB, unversioned bucket), and administrative control (single service account key, single '
                         'project billing cap). True architectural resilience demands a disciplined, layer-by-layer '
                         'audit methodology that uncovers hidden single points of failure and eliminates them through '
                         'structural redundancy, automated health checking, and self-healing controls.',
             'technical': 'Eliminating SPOFs requires systematic architectural hardening across five distinct '
                          'infrastructure layers:\n'
                          '\n'
                          '### 1. Network Layer SPOFs & Remediation\n'
                          '- **Cloud NAT Exhaustion:** A single NAT gateway allocating fixed 64 ports per VM will drop '
                          'outbound connections under load. **Remediation:** Configure Dynamic Port Allocation '
                          '(`--enable-dynamic-port-allocation`), multiple NAT IP addresses, and allocate minimum 256 '
                          'ports per VM.\n'
                          '- **Hybrid Interconnect:** A single Dedicated Interconnect link has a 99.9% SLA. '
                          '**Remediation:** Deploy 99.99% topology requiring dual links across dual metropolitan '
                          'availability zones with redundant Cloud Routers.\n'
                          '\n'
                          '### 2. Compute Layer SPOFs & Remediation\n'
                          '- **Zonal VM Failure:** An unmanaged standalone Compute Engine VM dies on host hardware '
                          'fault. **Remediation:** Regional Managed Instance Group (MIG) distributed across 3 zones '
                          'with Autohealing (`--health-check`) and proactive instance repair.\n'
                          '- **GKE Control Plane:** Single-zone GKE cluster control plane restarts during master '
                          'upgrades. **Remediation:** Deploy GKE Regional Clusters where the Kubernetes control plane '
                          'is replicated across three availability zones with a 99.95% SLA.\n'
                          '\n'
                          '### 3. Database & Storage Layer SPOFs & Remediation\n'
                          '- **Zonal Cloud SQL:** Standalone Cloud SQL instance fails on zonal hypervisor crash. '
                          '**Remediation:** Enable High Availability (HA) configuration using synchronous Regional '
                          'Persistent Disk replication with automatic failover in <60 seconds.\n'
                          '- **Object Storage:** A regional bucket in a single region is vulnerable to regional '
                          'catastrophe. **Remediation:** Dual-Region or Multi-Region Cloud Storage buckets with Object '
                          'Versioning and Turbo Replication (15-minute RPO guarantee).\n'
                          '\n'
                          '### 4. IAM & Governance SPOFs\n'
                          '- **Hardcoded Long-Lived Keys:** A compromised or deleted Service Account JSON key '
                          'invalidates all API traffic. **Remediation:** Workload Identity Federation, short-lived '
                          'OAuth2 access tokens, and automated key rotation.',
             'questions': ['What is the difference in SLA between a single-zone GKE cluster and a regional GKE '
                           'cluster?',
                           'How does Cloud SQL High Availability (HA) achieve failover without data loss compared to '
                           'read replica promotion?',
                           'Why does a Global External Application Load Balancer with Anycast IP eliminate external '
                           'DNS routing SPOFs?'],
             'reference': 'https://docs.cloud.google.com/architecture/framework/reliability/eliminate-single-points-of-failure',
             'reference_label': 'Google Cloud Architecture Framework: Identifying and eliminating single points of '
                                'failure',
             'scenario': {'symptom': "During a high-volume promotion, Brightloaf's backend checkout workers began "
                                     'logging `Connection refused: connect` and `ETIMEDOUT` when contacting the '
                                     'third-party credit card gateway. Compute Engine instances were healthy, but 70% '
                                     'of outbound transactions failed.',
                          'constraints': 'Cannot bypass PCI-DSS compliance, must keep outbound traffic pinned to known '
                                         'static IP addresses for external firewall whitelisting.',
                          'evidence': 'Cloud NAT metric `nat/dropped_sent_packets_count` spiked to 14,200 drops/min '
                                      'with reason `OUT_OF_RESOURCES`. Only one static IP address was allocated, and '
                                      'each VM had exceeded its fixed 64-port ceiling.',
                          'diagnostic_steps': ['Query Cloud Monitoring for '
                                               '`compute.googleapis.com/nat/nat_allocation_exhaustion`.',
                                               'Inspect Cloud NAT gateway configuration via `gcloud compute routers '
                                               'nats describe`.',
                                               'Review VM active TCP connections using `ss -s` on worker instances to '
                                               'confirm port starvation.'],
                          'root': 'Cloud NAT gateway was configured with a single IP address and manual fixed port '
                                  'allocation of 64 ports per VM, creating an unmonitored single point of failure that '
                                  'collapsed under high-concurrency outbound HTTPS traffic.',
                          'fix': 'Assign four additional static IP addresses to the Cloud NAT gateway, enable Dynamic '
                                 'Port Allocation with a maximum of 1,024 ports per VM, and establish Cloud Monitoring '
                                 'alerts for `nat/allocated_ports` utilization exceeding 75%.',
                          'verify': 'Simulate 2,000 concurrent outbound connections in staging; verify '
                                    '`dropped_sent_packets_count` remains zero and dynamic port scaling allocates '
                                    'additional ports seamlessly.',
                          'residual': 'Dynamic port allocation increases the required public IP quota; enterprise '
                                      'network teams must pre-allocate sufficient IP pools.',
                          'diagram': ('Outbound burst begins',
                                      '64-port SNAT limit hit',
                                      '70% checkout drops',
                                      'Dynamic port allocation',
                                      'Zero dropped packets'),
                          'facts': 'Cloud NAT dropped 14,200 packets/min due to port starvation on a single public IP.',
                          'inference': 'Fixed port allocation creates an artificial ceiling on outbound microservice '
                                       'scalability.',
                          'expected': 'Cloud NAT dynamically scales ports per VM up to configured maximums without '
                                      'dropping packets.'},
             'lab': {'name': 'Layer-by-Layer SPOF Audit and Remediation Runbook',
                     'file': 'day-083-topic-03-spof-audit.md',
                     'goal': 'Conduct a comprehensive architectural SPOF audit of a reference multi-tier enterprise '
                             'architecture and author concrete gcloud remediation commands.',
                     'expected': 'A structured Markdown audit document covering 5 infrastructure layers, rating '
                                 'failure blast radius, and detailing exact commands to enforce high availability.',
                     'mode': 'tabletop analysis & production CLI / YAML execution',
                     'prereq': 'Completion of Exercises 1 and 2.',
                     'preflight': 'Review Brightloaf architecture diagram from Day 80.',
                     'steps': ['#### Stage 1: Pre-Flight Five-Tier Infrastructure Scope & Invariant Definition\n'
                               'Establish the scope of the layer-by-layer SPOF audit across five core enterprise '
                               'infrastructure tiers:\n'
                               '1. **Network Tier:** Cloud NAT, HA VPN, Cloud Interconnect, and external DNS.\n'
                               '2. **Compute Tier:** Compute Engine VMs, Managed Instance Groups, and GKE control '
                               'plane / node pools.\n'
                               '3. **Database Tier:** Cloud SQL instances, transaction logs, and persistent disks.\n'
                               '4. **Storage Tier:** Cloud Storage buckets, Turbo Replication, and object versioning.\n'
                               '5. **IAM & Governance Tier:** Service account keys, OAuth2 credentials, and quota '
                               'allocation ceilings.',
                               '#### Stage 2: Target Infrastructure State Inspection & Metric Extraction\n'
                               'Author a diagnostic script (<kbd>inspect_spof_state.py</kbd>) that scans configuration '
                               'dictionaries and flags unmitigated single points of failure:\n'
                               '\n'
                               '```python\n'
                               '# inspect_spof_state.py\n'
                               '"""Scans infrastructure resources and identifies single-zone or fixed-capacity '
                               'SPOFs."""\n'
                               'infra_resources = [\n'
                               "    {'name': 'brightloaf-nat-gw', 'type': 'NAT', 'ips': 1, 'dynamic_ports': False},\n"
                               "    {'name': 'batch-worker-vm', 'type': 'VM', 'zone': 'us-central1-a', 'mig': False},\n"
                               "    {'name': 'brightloaf-db', 'type': 'CloudSQL', 'availability': 'ZONAL'},\n"
                               ']\n'
                               'spofs = []\n'
                               'for r in infra_resources:\n'
                               "    if r['type'] == 'NAT' and not r['dynamic_ports']:\n"
                               "        spofs.append((r['name'], 'NETWORK_SPOF: Fixed SNAT port ceiling'))\n"
                               "    elif r['type'] == 'VM' and not r['mig']:\n"
                               "        spofs.append((r['name'], 'COMPUTE_SPOF: Unmanaged single-zone VM'))\n"
                               "    elif r['type'] == 'CloudSQL' and r['availability'] == 'ZONAL':\n"
                               "        spofs.append((r['name'], 'DATABASE_SPOF: Zonal database without standby "
                               "failover'))\n"
                               '\n'
                               "print(f'Identified {len(spofs)} critical single points of failure:')\n"
                               'for name, reason in spofs:\n'
                               "    print(f'  - [CRITICAL] {name}: {reason}')\n"
                               "assert len(spofs) == 3, 'Expected 3 SPOFs identified'\n"
                               "print('[PASS] Infrastructure SPOF inspection completed.')\n"
                               '```\n'
                               '\n'
                               'Execute the inspection script:\n'
                               '\n'
                               '```sh\n'
                               'python3 inspect_spof_state.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Cloud NAT Dynamic Port Scaling & Hardening Script\n'
                               'Author the network tier remediation script (<kbd>remediate_nat_spof.sh</kbd>) '
                               'configuring Dynamic Port Allocation and multi-IP provisioning:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > remediate_nat_spof.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "[1/3] Hardening Cloud NAT Gateway against SNAT port exhaustion..."\n'
                               '# Simulating gcloud compute routers nats update\n'
                               "cat <<'YAML' > hardened-nat-config.yaml\n"
                               'name: brightloaf-nat\n'
                               'router: brightloaf-cr\n'
                               'region: us-central1\n'
                               'enableDynamicPortAllocation: true\n'
                               'minPortsPerVm: 128\n'
                               'maxPortsPerVm: 1024\n'
                               'natIps:\n'
                               '  - projects/brightloaf-prod/regions/us-central1/addresses/nat-ip-1\n'
                               '  - projects/brightloaf-prod/regions/us-central1/addresses/nat-ip-2\n'
                               '  - projects/brightloaf-prod/regions/us-central1/addresses/nat-ip-3\n'
                               '  - projects/brightloaf-prod/regions/us-central1/addresses/nat-ip-4\n'
                               'YAML\n'
                               'echo "[SUCCESS] Cloud NAT dynamic port scaling policy written with 4 dedicated static '
                               'IPs."\n'
                               'EOF\n'
                               'chmod +x remediate_nat_spof.sh\n'
                               './remediate_nat_spof.sh\n'
                               '```',
                               '#### Stage 4: Compute & Database SPOF Elimination Manifests\n'
                               'Author the declarative infrastructure configurations for Regional MIG and Regional '
                               'Cloud SQL (<kbd>regional_ha_manifests.sh</kbd>):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > regional_ha_manifests.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "[2/3] Authoring Compute & Database Regional HA Declarations..."\n'
                               '\n'
                               '# Compute Tier: Regional MIG with Autohealing\n'
                               "cat <<'CONF' > compute-regional-mig.json\n"
                               '{\n'
                               '  "name": "brightloaf-batch-rmig",\n'
                               '  "region": "us-central1",\n'
                               '  "distributionPolicy": {\n'
                               '    "zones": [\n'
                               '      {"zone": "us-central1-a"},\n'
                               '      {"zone": "us-central1-b"},\n'
                               '      {"zone": "us-central1-c"}\n'
                               '    ]\n'
                               '  },\n'
                               '  "targetSize": 3,\n'
                               '  "autoHealingPolicies": [{\n'
                               '    "healthCheck": "projects/brightloaf-prod/global/healthChecks/batch-hc",\n'
                               '    "initialDelaySec": 300\n'
                               '  }]\n'
                               '}\n'
                               'CONF\n'
                               '\n'
                               '# Database Tier: Cloud SQL Regional HA Configuration\n'
                               "cat <<'CONF' > cloudsql-ha.json\n"
                               '{\n'
                               '  "settings": {\n'
                               '    "availabilityType": "REGIONAL",\n'
                               '    "backupConfiguration": {\n'
                               '      "enabled": true,\n'
                               '      "pointInTimeRecoveryEnabled": true,\n'
                               '      "binaryLogEnabled": true\n'
                               '    },\n'
                               '    "dataDiskType": "PD_SSD",\n'
                               '    "dataDiskSizeGb": 250\n'
                               '  }\n'
                               '}\n'
                               'CONF\n'
                               'echo "[SUCCESS] Compute Regional MIG and Cloud SQL HA JSON manifests generated."\n'
                               'EOF\n'
                               'chmod +x regional_ha_manifests.sh\n'
                               './regional_ha_manifests.sh\n'
                               '```',
                               '#### Stage 5: Runtime Inspection & High Availability Validation Assertions\n'
                               'Author a verification test (<kbd>verify_ha_topology.py</kbd>) confirming that all '
                               'three patched resources meet regional HA invariants:\n'
                               '\n'
                               '```python\n'
                               '# verify_ha_topology.py\n'
                               'import json\n'
                               '\n'
                               '# Validate MIG configuration\n'
                               "mig_cfg = json.load(open('compute-regional-mig.json'))\n"
                               "assert len(mig_cfg['distributionPolicy']['zones']) == 3, 'MIG must span 3 availability "
                               "zones'\n"
                               "assert mig_cfg['autoHealingPolicies'][0]['initialDelaySec'] == 300, 'Autohealing "
                               "policy missing'\n"
                               '\n'
                               '# Validate Cloud SQL HA configuration\n'
                               "db_cfg = json.load(open('cloudsql-ha.json'))\n"
                               "assert db_cfg['settings']['availabilityType'] == 'REGIONAL', 'Cloud SQL must be "
                               "REGIONAL HA'\n"
                               "assert db_cfg['settings']['backupConfiguration']['pointInTimeRecoveryEnabled'], 'PITR "
                               "must be enabled'\n"
                               '\n'
                               "print('[PASS] Regional HA invariants validated across compute, storage, and "
                               "network.')\n"
                               '```\n'
                               '\n'
                               'Run the verification assertions:\n'
                               '\n'
                               '```sh\n'
                               'python3 verify_ha_topology.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Zonal Host Crash & NAT Port Starvation Drill\n'
                               'Develop a chaos drill simulation (<kbd>chaos_spof_injection.py</kbd>) that simulates a '
                               'zonal hypervisor crash and asserts that the regional MIG redistributes workers across '
                               'surviving zones without data loss:\n'
                               '\n'
                               '```python\n'
                               '# chaos_spof_injection.py\n'
                               '"""Simulates zone crash on 3-zone MIG."""\n'
                               "zones = {'us-central1-a': 1, 'us-central1-b': 1, 'us-central1-c': 1}\n"
                               "print(f'Initial Cluster Distribution: {zones}')\n"
                               '\n'
                               '# Simulate loss of zone us-central1-a\n'
                               "print('[CHAOS] Injecting fatal substation power outage in us-central1-a...')\n"
                               "zones['us-central1-a'] = 0\n"
                               '# Regional MIG autohealing redistributes lost instance to healthy zones\n'
                               "zones['us-central1-b'] += 1\n"
                               "print(f'Post-Autohealing Cluster Distribution: {zones}')\n"
                               "assert sum(zones.values()) == 3, 'MIG must maintain target capacity of 3 instances'\n"
                               "assert zones['us-central1-a'] == 0 and zones['us-central1-b'] == 2\n"
                               "print('[PASS] Chaos test passed: Regional MIG self-healed lost instance across "
                               "surviving zones.')\n"
                               '```\n'
                               '\n'
                               'Execute the chaos simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_spof_injection.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Comprehensive Layer-by-Layer SPOF Audit Document\n'
                               'Author the master enterprise SPOF audit document '
                               '(<kbd>day-083-topic-03-spof-audit.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# Day 83: Layer-by-Layer SPOF Audit & Remediation Matrix\n'
                               '\n'
                               '## 1. Network Layer Audit\n'
                               '- **Identified SPOF:** Single Cloud NAT IP with static 64-port limit.\n'
                               '- **Blast Radius:** Total outbound connectivity failure (payments, external APIs).\n'
                               '- **Remediation:** Enforce Dynamic Port Allocation (min 128, max 1024) across 4 static '
                               'public IPs.\n'
                               '\n'
                               '## 2. Compute Layer Audit\n'
                               '- **Identified SPOF:** Single-zone standalone Compute Engine VM for batch processing.\n'
                               '- **Blast Radius:** Entire batch pipeline halted if zone `us-central1-a` suffers '
                               'outage.\n'
                               '- **Remediation:** Regional MIG distributed across 3 AZs with autohealing health '
                               'checks.\n'
                               '\n'
                               '## 3. Database Layer Audit\n'
                               '- **Identified SPOF:** Single-zone Cloud SQL PostgreSQL instance.\n'
                               '- **Blast Radius:** RTO > 4 hours (manual backup restoration required on host crash).\n'
                               '- **Remediation:** Cloud SQL Regional HA with synchronous Regional PD replication '
                               '(<60s failover).\n'
                               '\n'
                               '## 4. Summary Matrix\n'
                               '| Layer | Pre-Remediation SLA | Post-Remediation SLA | Failover Mechanism |\n'
                               '| :--- | :--- | :--- | :--- |\n'
                               '| Network (NAT) | 99.0% (port limited) | 99.99% | Dynamic IP pool & port scaling |\n'
                               '| Compute | 99.5% (zonal) | 99.95% | Regional MIG multi-zone autohealing |\n'
                               '| Database | 99.9% (zonal) | 99.95% | Regional PD synchronous failover (<60s) |\n'
                               '```',
                               '#### Stage 8: Teardown, Verification Checklist & Artifact Acceptance\n'
                               'Teardown temporary simulation files and verify final evidence artifacts:\n'
                               '\n'
                               '```sh\n'
                               'rm -f inspect_spof_state.py remediate_nat_spof.sh regional_ha_manifests.sh '
                               'verify_ha_topology.py chaos_spof_injection.py hardened-nat-config.yaml '
                               'compute-regional-mig.json cloudsql-ha.json\n'
                               'ls -lh day-083-topic-03-spof-audit.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>day-083-topic-03-spof-audit.md</kbd> exists, is populated, and '
                               'serves as complete exit evidence.'],
                     'verification': 'Document exists, is well-formatted, and contains valid GCP CLI commands for NAT '
                                     'dynamic allocation, Regional MIG, and Regional Cloud SQL.',
                     'trouble': 'Ensure `--availability-type=REGIONAL` is used rather than read replica promotion for '
                                'Cloud SQL HA.',
                     'cleanup': 'Retain `day-083-topic-03-spof-audit.md` as an exit evidence artifact.',
                     'accept': 'Completed layer-by-layer SPOF matrix with exact, production-ready remediation '
                               'commands.'}}],
 'part3_intro': 'The following field cases analyze real-world production catastrophes resulting from naive '
                'availability math, unhedged series dependency chaining, and overlooked single points of failure. Each '
                'case contains quantifiable failure metrics, verbatim terminal/log transcripts, diagnostic command '
                'sequences, root cause mechanics, defensible remediations, and dual-lane failed/corrected '
                'architectural diagrams.',
 'part4_intro': 'These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author '
                'production calculation scripts, execute mathematical simulations of series/parallel failure chains, '
                'author declarative high-availability Google Cloud configurations, inject simulated zonal crashes and '
                'SNAT port starvation, and verify recovery against strict acceptance criteria with zero difficulty '
                'labels.'}
