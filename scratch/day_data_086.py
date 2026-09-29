"""day_data_086.py — Exhaustive architecture data specification for Day 86.

Covers SLIs, SLOs, and Error Budgets:
1. SLIs, SLOs, SLAs and how they differ (definitions, mathematical formulations, contractual safety margins).
2. Error budgets and release velocity governance (burn rates, multi-window alerting, feature freeze policies).
3. Toil and automation (Google SRE 50% rule, toil taxonomy, programmatic remediation).
4. The Four Golden Signals (Latency percentiles, Traffic, Errors, Saturation metrics).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable 8-stage operational engineering exercises.
"""

DAY_NUM = 86

DATA = {'day': 86,
 'part1_intro': 'Day 86 anchors the operational governance of cloud reliability by mastering Service Level Indicators '
                '(SLIs), Service Level Objectives (SLOs), Service Level Agreements (SLAs), and error budget policies. '
                'Reliability is not an abstract virtue; it is an economic trade-off governed by empirical data. SRE '
                'principles mandate that 100% reliability is the wrong target for almost every software system: '
                'striving for perfection stifles innovation, delays feature delivery, and incurs exponential '
                'infrastructure costs with diminishing user returns. Instead, teams define quantifiable SLIs based on '
                'the Four Golden Signals (Latency, Traffic, Errors, and Saturation), set defensible SLOs, and use the '
                'remaining error budget as a shared currency that dynamically regulates deployment velocity. When the '
                'error budget is healthy, teams ship fast; when it burns rapidly, releases freeze and engineering '
                'effort pivots strictly to stability and toil automation.',
 'exit_summary': 'Drafted an authoritative, production-grade Service Level Objective (SLO) specification document for '
                 "Brightloaf's checkout and catalog APIs; established mathematical SLI definitions across latency "
                 'percentiles and error rates; codified a rolling 28-day error budget policy with multi-window burn '
                 'rate alert thresholds (14.4x for 1h, 6x for 6h); implemented an operational toil taxonomy enforcing '
                 "Google's 50% engineering cap; authored and executed a Python error budget burn rate calculator "
                 'simulating catastrophic budget exhaustion.',
 'part2_intro': 'Reliability engineering transforms subjective user satisfaction into precise, enforceable '
                'mathematical thresholds. The sections below provide detailed engineering specifications for SLI '
                'calculation formulas, multi-window burn rate alerting algorithms, toil classification, and Cloud '
                'Monitoring golden signal instrumentation.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Reliability Construct</th>\n'
                    '      <th>Governing Definition</th>\n'
                    '      <th>Primary Audience &amp; Purpose</th>\n'
                    '      <th>Example Target / Metric</th>\n'
                    '      <th>Consequence of Breach</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>Service Level Indicator (SLI)</strong></td>\n'
                    '      <td>A quantifiable, empirical ratio of good events to total valid events over a specified '
                    'window.</td>\n'
                    '      <td>Engineering / SRE: Real-time telemetry measurement.</td>\n'
                    '      <td><code>good_requests (HTTP &lt; 500, &lt; 250ms) / total_requests</code></td>\n'
                    '      <td>Observable signal degradation; feeds SLO error budget consumption.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Service Level Objective (SLO)</strong></td>\n'
                    '      <td>An internal target reliability level agreed upon between Product and SRE teams.</td>\n'
                    '      <td>Product &amp; Engineering: Balancing release velocity against stability.</td>\n'
                    '      <td><strong>99.9%</strong> over rolling 28 days (~40.3 minutes budget).</td>\n'
                    '      <td>Error budget depletion; triggers release freeze and automated rollback.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Service Level Agreement (SLA)</strong></td>\n'
                    '      <td>A legally or commercially binding commitment made to external customers.</td>\n'
                    '      <td>Customers, Legal, Finance: Contractual trust and liability.</td>\n'
                    '      <td><strong>99.5%</strong> over calendar month (provides 4x safety buffer).</td>\n'
                    '      <td>Financial penalties, customer billing credits, contract renegotiation.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Error Budget</strong></td>\n'
                    '      <td>The allowance of permitted unreliability: <code>100% - SLO Target</code>.</td>\n'
                    '      <td>Product &amp; Release Managers: Currency for risk-taking and innovation.</td>\n'
                    '      <td><strong>0.1%</strong> of total transactions (10,000 bad requests per 10M).</td>\n'
                    '      <td>Feature freeze: 100% engineering effort redirected to reliability bugs and toil '
                    'reduction.</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 86: Closed-Loop SLO Governance and Error Budget Release Topology',
                  'desc': 'Multi-tier infrastructure topology illustrating telemetry collection across the Four Golden '
                          'Signals, SLI evaluation, multi-window burn rate calculation, and CI/CD release gating.',
                  'caption': 'Figure 86.1: Multi-tier architectural topology illustrating request flows through edge '
                             'Anycast, decoupled compute tiers, HA persistence, and shared control plane boundaries.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Edge & Client Ingress Tier',
                              'desc': 'Global External ALB, Cloud Armor WAF, Edge Latency Telemetry (Total Traffic '
                                      'Ingress)',
                              'fill': '#1e3a5f',
                              'y': 10,
                              'h': 90},
                             {'name': 'LAYER 2: Application Microservices & Golden Signals',
                              'desc': 'GKE Autopilot Workload Pods exporting Latency, Traffic, Errors, and Saturation',
                              'fill': '#0f2338',
                              'y': 115,
                              'h': 90},
                             {'name': 'LAYER 3: Real-Time SLI Evaluation & Telemetry Fabric',
                              'desc': 'Google Cloud Managed Service for Prometheus (GMP) & Cloud Monitoring MQL '
                                      'Evaluators',
                              'fill': '#064e3b',
                              'y': 220,
                              'h': 90},
                             {'name': 'LAYER 4: Multi-Window Multi-Burn-Rate SRE Engine',
                              'desc': 'Fast Burn 14.4x (1h / 2% budget), Medium Burn 6.0x (6h / 5% budget), Rolling '
                                      '28-Day Window',
                              'fill': '#1e1b4b',
                              'y': 325,
                              'h': 90},
                             {'name': 'LAYER 5: SRE Governance & CI/CD Deployment Gate',
                              'desc': 'Google Cloud Deploy Automated Gate, Feature Freeze Circuit Breaker, and Toil '
                                      'Automation Bot',
                              'fill': '#3b0764',
                              'y': 430,
                              'h': 90}],
                  'components': [{'id': 'alb_ingress',
                                  'name': 'Global External ALB',
                                  'detail': 'Edge Request SLI Source',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'cloud_armor',
                                  'name': 'Cloud Armor DDoS',
                                  'detail': 'Traffic Signal Filter',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'gke_workloads',
                                  'name': 'GKE Microservices',
                                  'detail': 'Golden Signals Instrumentation',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'cloud_sql_ha',
                                  'name': 'Cloud SQL Database',
                                  'detail': 'Saturation Telemetry Source',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'gmp_engine',
                                  'name': 'Managed Prometheus',
                                  'detail': 'PodMonitoring Metrics Scope',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'mql_calculator',
                                  'name': 'MQL SLO Engine',
                                  'detail': 'Rolling 28-Day Compliance',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'burn_fast',
                                  'name': 'Fast Burn 14.4x Alert',
                                  'detail': 'P1 Emergency Pager Trigger',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'burn_medium',
                                  'name': 'Medium Burn 6.0x Alert',
                                  'detail': 'P2 Ticket Generation',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'cd_release_gate',
                                  'name': 'Cloud Deploy Gate',
                                  'detail': 'Error Budget Release Freeze',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'},
                                 {'id': 'toil_remediator',
                                  'name': 'SRE Toil Automator',
                                  'detail': '<50% Toil Cap Enforcement',
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
                                  'label': 'GOLDEN SIGNALS METRICS INGESTION PERIMETER',
                                  'color': '#38bdf8'},
                                 {'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'REAL-TIME SLI & MULTI-WINDOW BURN RATE BOUNDARY',
                                  'color': '#10b981'},
                                 {'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'ERROR BUDGET ENFORCEMENT & RELEASE FREEZE PERIMETER',
                                  'color': '#a855f7'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'type': 'ok', 'label': 'Ingress Rate (Traffic)'},
                            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'type': 'ok', 'label': 'Forward to Workload'},
                            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'type': 'ok', 'label': 'DB Connection Query'},
                            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'type': 'ok', 'label': 'Prometheus Scraping'},
                            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'type': 'ok', 'label': 'MQL Ratio Evaluation'},
                            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'type': 'fail', 'label': 'Fast Burn > 14.4x'},
                            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'type': 'warn', 'label': 'Medium Burn > 6.0x'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'type': 'fail',
                             'label': 'Freeze Release Pipeline'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'type': 'ok',
                             'label': 'Auto-Remediation Toil'}],
                  'probes': [{'cx': 420,
                              'cy': 56,
                              'label': 'PROBE 1: Availability SLI Threshold (>99.9%)',
                              'color': '#38bdf8'},
                             {'cx': 420, 'cy': 266, 'label': 'PROBE 2: p99 Latency SLI (<250ms)', 'color': '#22c55e'},
                             {'cx': 420,
                              'cy': 371,
                              'label': 'PROBE 3: Error Budget Exhaustion Tripwire',
                              'color': '#f43f5e'}]},
 'topics': [{'key': 'topic-01',
             'title': 'SLIs, SLOs, SLAs and how they differ',
             'preview': 'A product manager promises enterprise customers a 99.99% contractual SLA because the staging '
                        'environment had 100% uptime last month. Two weeks after launch, a 15-minute network glitch '
                        'triggers $45,000 in customer refunds because the SLA had no safety margin below the internal '
                        'SLO.',
             'overview': 'The foundation of Site Reliability Engineering is the clear mathematical separation between '
                         'SLIs, SLOs, and SLAs. A **Service Level Indicator (SLI)** is a precisely measured ratio: '
                         'good events divided by valid events over a specified duration. A **Service Level Objective '
                         '(SLO)** is the target percentage for that SLI agreed upon internally between product and '
                         'engineering stakeholders. A **Service Level Agreement (SLA)** is the public or commercial '
                         'contract specifying what happens (usually billing credits or refunds) if the service fails '
                         'to meet a relaxed reliability threshold. In mature cloud organizations, the SLA is always '
                         'significantly looser than the SLO (e.g., an internal SLO of 99.9% paired with an external '
                         'SLA of 99.5%). This gap provides an essential operational buffer, allowing SREs to absorb '
                         'transient infrastructure hiccups, investigate root causes, and remediate problems before '
                         'financial penalties occur.',
             'technical': 'Architects must enforce rigorous mathematical precision in defining SLIs and boundaries:\n'
                          '\n'
                          '### 1. The Canonical SLI Formulation\n'
                          'All SLIs must follow the standardized event-ratio format:\n'
                          '$$\\text{SLI} = \\frac{\\sum \\text{Good Events}}{\\sum \\text{Valid Events}} \\times '
                          '100\\%$$\n'
                          '- **Availability SLI:** Ratio of HTTP responses with status codes `< 500` to total requests '
                          'with status codes `< 600` (excluding invalid client 4xx requests).\n'
                          '- **Latency SLI:** Ratio of requests where `request_latency <= 250ms` measured at the edge '
                          'load balancer to total valid requests.\n'
                          '\n'
                          '### 2. Rolling Compliance Windows vs. Calendar Months\n'
                          "Calendar-month SLOs suffer from the 'reset anomaly': a service can burn 100% of its budget "
                          'on the 1st of the month, yet suffer zero consequences for reckless deployments on the 30th '
                          'because the counter resets the next day. Enterprise SRE mandates **Rolling 28-Day Windows** '
                          '(exactly 4 weeks), ensuring that reliability accountability is smooth, continuous, and '
                          'unaffected by calendar boundaries.\n'
                          '\n'
                          '### 3. Contractual SLA Safety Margin\n'
                          'Never publish an SLA identical to your internal SLO:\n'
                          '- If Internal SLO = 99.9% (allows ~40.3 minutes downtime / 28 days).\n'
                          '- Public SLA = 99.5% (allows ~201.6 minutes downtime / 28 days).\n'
                          '- The 161.3-minute difference is the **Engineering Safety Margin** that protects the '
                          'company from contract penalties.',
             'questions': ['Why should client-generated HTTP 4xx errors (e.g., 404 Not Found, 401 Unauthorized) be '
                           'excluded from the valid requests denominator of an availability SLI?',
                           'How does a rolling 28-day window prevent engineering teams from gaming release schedules '
                           'compared to a monthly calendar window?',
                           'What is the mathematical relationship between the internal SLO target and the external SLA '
                           'penalty threshold?'],
             'reference': 'https://docs.cloud.google.com/architecture/framework/reliability/define-slos',
             'reference_label': 'Google Cloud Architecture Framework: Defining SLIs and SLOs',
             'scenario': {'symptom': 'Brightloaf committed to a customer-facing 99.9% availability SLA. During an '
                                     'unexpected regional fiber cut, the checkout API was unavailable for 52 minutes, '
                                     'resulting in an availability score of 99.87%. The enterprise client demanded a '
                                     'full monthly refund because Brightloaf set its external SLA equal to its '
                                     'internal 99.9% SLO with zero margin for error.',
                          'constraints': 'Must maintain customer enterprise trust while insulating the company from '
                                         'catastrophic financial liability during cloud provider network events.',
                          'evidence': 'Contract review revealed that SLA penalties triggered at `< 99.90%`. Cloud '
                                      'Monitoring records showed the service operated at 99.96% for the preceding six '
                                      'months, but the single 52-minute incident triggered a 100% service credit '
                                      'refund of $18,500.',
                          'diagnostic_steps': ['Audit the contractual SLA documentation against Google Cloud '
                                               'Monitoring SLO records for the past 12 months.',
                                               'Calculate the historical frequency of infrastructure outages exceeding '
                                               '30 minutes in duration.',
                                               'Model financial exposure under an SLO of 99.9% paired with a tiered '
                                               'SLA (99.5% for 10% credit, 99.0% for 25% credit).'],
                          'root': 'Commercial contracts conflated internal aspirational SLOs with external legal SLAs, '
                                  'establishing an unhedged 99.9% contractual guarantee that left zero buffer for '
                                  'uncontrollable third-party upstream infrastructure failures.',
                          'fix': 'Renegotiate customer contract terms: set public SLA to 99.5% with tiered service '
                                 'credits, while maintaining an internal 99.9% engineering SLO on a rolling 28-day '
                                 'window to catch regressions before they breach the contract.',
                          'verify': 'Simulate historical outages against the revised tiered SLA model; verify zero '
                                    'financial refunds would have been owed while preserving strong operational '
                                    'discipline.',
                          'residual': 'Some prospective enterprise clients may initially push back during procurement; '
                                      'requires sales engineering enablement to explain the difference between '
                                      'realistic SLAs and deceptive marketing.',
                          'diagram': ('52m fiber cut outage',
                                      'Internal SLO breached (99.87%)',
                                      '$18.5k SLA refund triggered',
                                      'Tiered SLA policy (99.5%)',
                                      'Zero refund liability'),
                          'facts': '52-minute outage caused 99.87% monthly availability, triggering an $18,500 penalty '
                                   'under an unhedged 99.9% SLA.',
                          'inference': 'Setting SLA equal to SLO guarantees commercial failure when third-party cloud '
                                       'infrastructure suffers an outage.',
                          'expected': 'Internal SLO drives rapid engineering fixes, while a relaxed SLA protects '
                                      'commercial margins.'},
             'lab': {'name': 'SLI Calculation and Safety Margin Modeling Tool',
                     'file': 'day-086-topic-01-sli-calc.py',
                     'goal': 'Write and execute a Python tool that parses transaction logs, computes availability and '
                             'latency SLIs, and models SLA margin buffers.',
                     'expected': 'A runnable script that outputs precise SLI percentages, computes error budget '
                                 'consumption, and validates whether contractual SLA thresholds are breached.',
                     'mode': 'local script execution & verification',
                     'prereq': 'Python 3.10+ installed.',
                     'preflight': 'Verify Python runtime and initialize exercise workspace.',
                     'steps': ['#### Stage 1: Pre-Flight SLI Specification & Safety Margin Invariants\n'
                               'Define the mathematical SLI ratio: $\\text{SLI} = \\frac{\\sum \\text{Good '
                               'Events}}{\\sum \\text{Valid Events}} \\times 100\\%$. Establish the distinction '
                               'between internal SLO (99.9% over rolling 28 days = 40.32 minutes budget) and external '
                               'SLA (99.5% over calendar month = 201.6 minutes threshold), codifying the 161.28-minute '
                               'safety buffer.',
                               '#### Stage 2: Environment Preflight & Invariant Verification\n'
                               'Author a test script (<kbd>test_sli_constants.py</kbd>) verifying that rolling 28-day '
                               'window calculations use exact seconds:\n'
                               '\n'
                               '```python\n'
                               '# test_sli_constants.py\n'
                               'window_days = 28\n'
                               'total_sec = window_days * 24 * 3600\n'
                               "assert total_sec == 2419200, '28 days must equal exactly 2,419,200 seconds'\n"
                               'budget_999 = total_sec * 0.001\n'
                               "print(f'28-Day Window: {total_sec:,}s | 99.9% Budget: {budget_999:.1f}s "
                               "({budget_999/60:.2f} mins)')\n"
                               'assert abs(budget_999 - 2419.2) < 1e-4\n'
                               "print('[PASS] SLI window constants verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight validation:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_sli_constants.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: SLI & SLA Margin Calculator\n'
                               'Author the calculation script (<kbd>sli_margin_calculator.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '#!/usr/bin/env python3\n'
                               '"""sli_margin_calculator.py — Evaluates SLIs, SLO compliance, and SLA buffer '
                               'margins."""\n'
                               'from typing import Dict\n'
                               '\n'
                               'def evaluate_service_health(good_requests: int, total_requests: int, internal_slo: '
                               'float = 99.9, external_sla: float = 99.5) -> Dict:\n'
                               '    sli = (good_requests / total_requests) * 100.0\n'
                               '    slo_passed = sli >= internal_slo\n'
                               '    sla_breached = sli < external_sla\n'
                               '    return {\n'
                               "        'sli': sli,\n"
                               "        'slo_passed': slo_passed,\n"
                               "        'sla_breached': sla_breached,\n"
                               "        'safety_margin_headroom_pct': sli - external_sla\n"
                               '    }\n'
                               '\n'
                               "if __name__ == '__main__':\n"
                               '    # Scenario: 52-minute outage on 10,000,000 requests\n'
                               '    res = evaluate_service_health(good_requests=9987000, total_requests=10000000)\n'
                               '    print(f"Measured SLI: {res[\'sli\']:.4f}%")\n'
                               '    print(f"Internal SLO (99.9%) Met: {res[\'slo_passed\']}")\n'
                               '    print(f"External SLA (99.5%) Breached: {res[\'sla_breached\']}")\n'
                               "    assert not res['slo_passed'] and not res['sla_breached'], 'SLO should fail while "
                               "SLA remains safe'\n"
                               "    print('[PASS] Safety margin protected company from customer SLA billing refund.')\n"
                               '```',
                               '#### Stage 4: Execution & Safety Margin Simulation Telemetry\n'
                               'Execute the SLI margin calculator:\n'
                               '\n'
                               '```sh\n'
                               'python3 sli_margin_calculator.py\n'
                               '```\n'
                               '\n'
                               'Confirm that 99.87% availability triggers internal SLO remediation while leaving the '
                               '99.5% external SLA intact.',
                               '#### Stage 5: Live Verification & SLA Penalty Avoidance Assertions\n'
                               'Author an assertion test (<kbd>test_sla_cushion.py</kbd>) stress-testing outage '
                               'durations against financial liability:\n'
                               '\n'
                               '```python\n'
                               '# test_sla_cushion.py\n'
                               'from sli_margin_calculator import evaluate_service_health\n'
                               '\n'
                               '# Simulate 100-minute outage (99.75% availability)\n'
                               'res = evaluate_service_health(9975000, 10000000)\n'
                               "assert not res['sla_breached'], 'External SLA must not trigger on 100m outage'\n"
                               "assert res['safety_margin_headroom_pct'] > 0.20, 'Safety headroom should exceed "
                               "0.20%'\n"
                               "print(f'[PASS] SLA cushion verified: Headroom is "
                               '{res["safety_margin_headroom_pct"]:.2f}%.\')\n'
                               '```\n'
                               '\n'
                               'Run the verification assertions:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_sla_cushion.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Unhedged 1:1 SLO/SLA Coupling Drill\n'
                               'Author a chaos simulation (<kbd>chaos_slo_coupling.py</kbd>) demonstrating the '
                               'financial penalty of setting SLA equal to SLO:\n'
                               '\n'
                               '```python\n'
                               '# chaos_slo_coupling.py\n'
                               'def calculate_penalty(sli: float, sla_target: float, monthly_billing: float = '
                               '100000.0) -> float:\n'
                               '    if sli < sla_target:\n'
                               '        return monthly_billing * 0.25  # 25% credit\n'
                               '    return 0.0\n'
                               '\n'
                               'flawed_penalty = calculate_penalty(99.87, 99.90)\n'
                               'correct_penalty = calculate_penalty(99.87, 99.50)\n'
                               "print(f'Financial Refund under Coupled SLA (99.9%): ${flawed_penalty:,.2f}')\n"
                               "print(f'Financial Refund under Tiered SLA (99.5%):  ${correct_penalty:,.2f}')\n"
                               'assert flawed_penalty == 25000.0 and correct_penalty == 0.0\n'
                               "print('[PASS] Chaos test proves economic necessity of safety margin.')\n"
                               '```\n'
                               '\n'
                               'Execute the chaos simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_slo_coupling.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Enterprise SLO and SLA Specification\n'
                               'Author the enterprise SLO specification document (<kbd>day-086-slo-spec.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# Day 86: Brightloaf Service Level Objective Specification\n'
                               '\n'
                               '## 1. Core Tier 1 Services\n'
                               '- **Availability SLI:** HTTP 2xx/3xx/4xx responses / Total HTTP responses.\n'
                               '- **Internal SLO Target:** 99.9% over rolling 28-day window.\n'
                               '- **External SLA Commitment:** 99.5% over calendar month.\n'
                               '- **Latency SLI:** 99% of requests < 250ms at Anycast GCLB.\n'
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up intermediate test scripts and retain core artifacts:\n'
                               '\n'
                               '```sh\n'
                               'rm -f test_sli_constants.py test_sla_cushion.py chaos_slo_coupling.py\n'
                               'ls -lh sli_margin_calculator.py day-086-slo-spec.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>sli_margin_calculator.py</kbd> and <kbd>day-086-slo-spec.md</kbd> '
                               'are preserved as verifiable day evidence.'],
                     'verification': 'Script runs cleanly and displays precise SLI calculations and error budget '
                                     'consumption figures.',
                     'trouble': 'Ensure client 4xx errors are subtracted from the total requests before calculating '
                                'the ratio.',
                     'cleanup': 'Retain `day-086-topic-01-sli-calc.py` as an exit evidence artifact.',
                     'accept': 'Validated calculation of request-based SLIs, SLO targets, and contractual SLA '
                               'buffers.'}},
            {'key': 'topic-02',
             'title': 'Error budgets and how they govern release velocity',
             'preview': 'A product team pushes an untested payment feature on Friday afternoon that depletes 90% of '
                        'the quarterly error budget in 2 hours. Because the company has no formal error budget policy, '
                        'the team ships another high-risk update on Monday, triggering a full customer outage.',
             'overview': 'An **error budget** is the exact mathematical headroom of allowed failure: Error Budget = '
                         '100% - SLO Target. Rather than viewing unreliability as a moral failing, Site Reliability '
                         'Engineering treats the error budget as a shared currency allocated to development and '
                         'product teams to encourage rapid innovation and risk-taking. If a service operates with 100% '
                         'uptime, the system is over-engineered and shipping too slowly; the unused budget should be '
                         'spent pushing larger updates and experiments. However, the error budget is only meaningful '
                         'if it is backed by an enforceable **release governance policy**: when the error budget is '
                         'depleted, automated CI/CD guardrails halt all feature deployments, and 100% of engineering '
                         'bandwidth is redirected to fixing reliability, automating toil, and hardening tests until '
                         'the budget recovers.',
             'technical': 'Error budget governance requires formal mathematical burn rates and policy enforcement:\n'
                          '\n'
                          '### 1. Burn Rate Mathematical Mechanics\n'
                          'Burn rate ($B$) is the speed at which a service is consuming its error budget relative to '
                          'the normal rate that would deplete it over the compliance window ($T = 28$ days):\n'
                          '$$B = \\frac{\\text{Observed Error Rate}}{1 - \\text{SLO Target}}$$\n'
                          '- $B = 1.0$: Consumes exactly 100% of the budget over 28 days (nominal consumption).\n'
                          '- $B = 14.4$: Consumes **100% of the entire 28-day budget in only 46.7 hours (2% of budget '
                          'in 1 hour)**!\n'
                          '- $B = 36.0$: Consumes 100% of the 28-day budget in only 18.7 hours (5% of budget in 1 '
                          'hour)!\n'
                          '\n'
                          '### 2. Google SRE Multi-Window Multi-Burn-Rate Alerting\n'
                          'Traditional alerts fire on raw error rate thresholds, generating false alarms on low '
                          'traffic or lagging behind acute catastrophes. Google SRE uses **multi-window '
                          'multi-burn-rate alerts**:\n'
                          '- **Page On-Call Immediately (Critical Severity):** Burn rate $\\ge 14.4$ over 1-hour '
                          'window AND $\\ge 14.4$ over 5-minute window (detects rapid budget destruction within 2 '
                          'minutes).\n'
                          '- **File Ticket (Low Severity):** Burn rate $\\ge 3.0$ over 6-hour window AND $\\ge 3.0$ '
                          'over 30-minute window.\n'
                          '\n'
                          '### 3. Release Freeze Policy Matrix\n'
                          '- **Budget > 20%:** Green Status. Standard continuous delivery, feature flags, A/B canary '
                          'experiments authorized.\n'
                          '- **Budget 0% to 20%:** Yellow Status. Elevated canary bake times (minimum 4 hours); '
                          'high-risk database migrations blocked.\n'
                          '- **Budget < 0% (Exhausted):** Red Status. **Automatic CI/CD deployment block**. Zero '
                          'feature code merges permitted. 100% of sprint capacity allocated to SRE tickets, regression '
                          'testing, and architectural remediation until a 7-day rolling recovery occurs.',
             'questions': ['Why is a 1-hour burn rate alert paired with a 5-minute short window before paging the '
                           'on-call engineer?',
                           'What organizational incentive problem arises if the development team does not suffer a '
                           'feature freeze when the error budget is exhausted?',
                           'How does an error budget eliminate subjective arguments between Product Managers and SREs '
                           'regarding release timing?'],
             'reference': 'https://docs.cloud.google.com/architecture/framework/reliability/error-budgets',
             'reference_label': 'Google Cloud Architecture Framework: Managing release velocity with error budgets',
             'scenario': {'symptom': 'Brightloaf experienced three consecutive production outages in two weeks '
                                     'following rapid feature releases by the mobile engineering team. The rolling '
                                     '28-day error budget was completely exhausted (-140%), yet developers continued '
                                     'pushing new releases, leading to a fourth outage during a peak holiday ordering '
                                     'weekend.',
                          'constraints': 'Must establish objective, non-negotiable governance that halts dangerous '
                                         'releases without requiring executive intervention every sprint.',
                          'evidence': 'Git commit logs showed 14 feature releases deployed in the 7 days following the '
                                      'initial budget depletion. Cloud Monitoring showed the rolling availability SLI '
                                      'fell to 98.40% against a 99.9% SLO.',
                          'diagnostic_steps': ['Correlate Cloud Build release trigger timestamps with Cloud Monitoring '
                                               'error budget exhaustion graphs.',
                                               'Audit CI/CD pipeline configuration to verify whether release gates '
                                               'checked error budget status.',
                                               'Review retrospective meeting notes showing conflicting priorities '
                                               'between Product velocity KPIs and SRE stability alerts.'],
                          'root': 'Absence of an enforceable Error Budget Policy: the organization treated SLO burn '
                                  'alerts as informational telemetry rather than an automated deployment blocker, '
                                  'allowing product velocity to override system stability.',
                          'fix': 'Enact an executive-backed Error Budget Policy and integrate Cloud Build with the '
                                 'Cloud Monitoring SLO API: if remaining budget `< 0%`, the CI/CD pipeline '
                                 'automatically rejects non-hotfix deployments and requires VP Engineering approval to '
                                 'bypass.',
                          'verify': 'Trigger a simulated budget breach in staging; verify CI/CD pipeline halts '
                                    'production deployment and routes work to reliability backlog.',
                          'residual': 'Emergency security patches (CVE remediation) must retain an explicit '
                                      'break-glass override mechanism with audited sign-off.',
                          'diagram': ('Feature deploy causes 5xx',
                                      'Error budget hits -140%',
                                      'Release freeze ignored',
                                      'Automated CI/CD policy gate',
                                      '100% stability focus'),
                          'facts': 'Four consecutive outages occurred because developers pushed releases after error '
                                   'budget was -140% exhausted.',
                          'inference': 'An error budget without automated CI/CD gating is merely an ignored dashboard.',
                          'expected': 'CI/CD deployment gates automatically freeze non-emergency feature releases when '
                                      'error budget is exhausted.'},
             'lab': {'name': 'Multi-Window Burn Rate and CI/CD Release Policy Engine',
                     'file': 'day-086-topic-02-burn-rate.py',
                     'goal': 'Build an automated burn rate calculation and release gating tool in Python implementing '
                             'Google SRE alerting logic.',
                     'expected': 'A runnable script demonstrating multi-window burn rate detection (14.4x / 6x) and '
                                 'simulating automated CI/CD deployment gating.',
                     'mode': 'local script execution & verification',
                     'prereq': 'Completion of Exercise 1.',
                     'preflight': 'Verify Python runtime and initialize script template.',
                     'steps': ['#### Stage 1: Pre-Flight Multi-Window Multi-Burn-Rate Invariants\n'
                               'Establish the multi-window burn rate alert definitions from the Google SRE handbook:\n'
                               '- **Burn Rate 1.0:** Consumes 100% of error budget in exactly 28 days (normal '
                               'operational burn).\n'
                               '- **Burn Rate 14.4 (Fast Burn):** Consumes 2% of budget in 1 hour (100% in 50 hours). '
                               'Alerts on-call via paging (triggers in 2 minutes).\n'
                               '- **Burn Rate 6.0 (Medium Burn):** Consumes 5% of budget in 6 hours. Generates '
                               'high-priority ticket.\n'
                               '- **Budget Freeze Gate:** When error budget is exhausted (<0%), CI/CD deployment '
                               'pipelines automatically block feature rollouts.',
                               '#### Stage 2: Environment Preflight & Burn Rate Math Verification\n'
                               'Author a test script (<kbd>test_burn_rate_math.py</kbd>) calculating required error '
                               'rate for a 14.4x burn rate:\n'
                               '\n'
                               '```python\n'
                               '# test_burn_rate_math.py\n'
                               'slo = 0.999\n'
                               'error_budget = 1.0 - slo  # 0.001 (0.1%)\n'
                               'burn_14_4_error_rate = error_budget * 14.4\n'
                               "print(f'For 99.9% SLO, a 14.4x burn rate corresponds to a {burn_14_4_error_rate * "
                               "100:.2f}% error rate.')\n"
                               'assert abs(burn_14_4_error_rate - 0.0144) < 1e-6\n'
                               "print('[PASS] Multi-window burn rate mathematics verified.')\n"
                               '```\n'
                               '\n'
                               'Run the preflight test:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_burn_rate_math.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Multi-Window Burn Rate Engine\n'
                               'Author the burn rate calculation and release gating script '
                               '(<kbd>burn_rate_engine.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '#!/usr/bin/env python3\n'
                               '"""burn_rate_engine.py — Simulates error budget burn rates and release policy '
                               'gating."""\n'
                               'from typing import Dict, Tuple\n'
                               '\n'
                               'class ErrorBudgetManager:\n'
                               '    def __init__(self, slo_target: float = 99.9, window_days: int = 28):\n'
                               '        self.slo_target = slo_target\n'
                               '        self.total_budget_minutes = (window_days * 24 * 60) * (1.0 - (slo_target / '
                               '100.0))\n'
                               '        self.consumed_minutes = 0.0\n'
                               '\n'
                               '    def record_outage(self, outage_minutes: float):\n'
                               '        self.consumed_minutes += outage_minutes\n'
                               '\n'
                               '    def get_remaining_budget_pct(self) -> float:\n'
                               '        return max(0.0, 100.0 * (1.0 - (self.consumed_minutes / '
                               'self.total_budget_minutes)))\n'
                               '\n'
                               '    def evaluate_release_gate(self) -> Tuple[bool, str]:\n'
                               '        rem = self.get_remaining_budget_pct()\n'
                               '        if rem <= 0.0:\n'
                               "            return False, 'BLOCKED: Error budget 100% exhausted. Feature freeze "
                               "active.'\n"
                               '        elif rem < 20.0:\n'
                               "            return True, 'WARNING: Error budget < 20%. Director approval required.'\n"
                               "        return True, 'APPROVED: Error budget healthy. Releases permitted.'\n"
                               '\n'
                               "if __name__ == '__main__':\n"
                               '    mgr = ErrorBudgetManager(slo_target=99.9)\n'
                               "    print(f'Total Monthly Error Budget: {mgr.total_budget_minutes:.2f} minutes')\n"
                               '    mgr.record_outage(42.0)  # 42 minute outage exceeds 40.32m budget\n'
                               '    allowed, msg = mgr.evaluate_release_gate()\n'
                               "    print(f'Gate Status: {msg}')\n"
                               "    assert not allowed, 'Release gate should block deployment on budget exhaustion'\n"
                               "    print('[PASS] Release gate correctly blocked deployment.')\n"
                               '```',
                               '#### Stage 4: Execution & CI/CD Gate Simulation\n'
                               'Execute the burn rate engine and observe the release gate enforcement:\n'
                               '\n'
                               '```sh\n'
                               'python3 burn_rate_engine.py\n'
                               '```\n'
                               '\n'
                               'Confirm that an outage consuming more than 40.32 minutes immediately triggers a '
                               'release freeze.',
                               '#### Stage 5: Live Verification & Automated Rollback Assertions\n'
                               'Author an assertion test (<kbd>test_release_gate_assertions.py</kbd>) testing multiple '
                               'release stages:\n'
                               '\n'
                               '```python\n'
                               '# test_release_gate_assertions.py\n'
                               'from burn_rate_engine import ErrorBudgetManager\n'
                               '\n'
                               'm = ErrorBudgetManager()\n'
                               'm.record_outage(10.0)\n'
                               'ok, _ = m.evaluate_release_gate()\n'
                               "assert ok, 'Releases should be approved with 75% budget remaining'\n"
                               '\n'
                               'm.record_outage(25.0)  # 35m total consumed (>85%)\n'
                               'ok_warn, msg_warn = m.evaluate_release_gate()\n'
                               "assert 'WARNING' in msg_warn\n"
                               "print('[PASS] Release gate transition states verified successfully.')\n"
                               '```\n'
                               '\n'
                               'Run the verification test:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_release_gate_assertions.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Unchecked Deployment into Exhausted Budget\n'
                               'Author a chaos script (<kbd>chaos_unauthorized_deploy.py</kbd>) proving that feature '
                               'releases into an exhausted budget cause secondary outages:\n'
                               '\n'
                               '```python\n'
                               '# chaos_unauthorized_deploy.py\n'
                               'def simulate_rogue_deploy(budget_exhausted: bool) -> str:\n'
                               '    if budget_exhausted:\n'
                               "        return 'OUTAGE_AMPLIFICATION: Pushed unvetted code into depleted budget; "
                               "customer SLA breached!'\n"
                               "    return 'SAFE_DEPLOY'\n"
                               '\n'
                               'res = simulate_rogue_deploy(budget_exhausted=True)\n'
                               "assert 'OUTAGE_AMPLIFICATION' in res\n"
                               "print('[PASS] Chaos test demonstrates danger of bypassing error budget release "
                               "gates.')\n"
                               '```\n'
                               '\n'
                               'Execute the chaos simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_unauthorized_deploy.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Multi-Window Alerting and Feature Freeze Runbook\n'
                               'Author the operational release governance runbook '
                               '(<kbd>day-086-release-governance.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# Day 86: Error Budget Policy and Deployment Freeze Protocol\n'
                               '\n'
                               '## 1. Burn Rate Alert Escalation Matrix\n'
                               '- **14.4x (2% budget in 1h):** PagerDuty P1 page to Primary On-Call.\n'
                               '- **6.0x (5% budget in 6h):** P2 ticket to Service Team Lead.\n'
                               '- **100% Budget Depletion:** Immediate CI/CD deployment pipeline lock.\n'
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up temporary test scripts and retain core policy artifacts:\n'
                               '\n'
                               '```sh\n'
                               'rm -f test_burn_rate_math.py test_release_gate_assertions.py '
                               'chaos_unauthorized_deploy.py\n'
                               'ls -lh burn_rate_engine.py day-086-release-governance.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>burn_rate_engine.py</kbd> and '
                               '<kbd>day-086-release-governance.md</kbd> are preserved as verifiable day evidence.'],
                     'verification': 'Script executes without error, accurately computes SRE burn rates, and '
                                     'demonstrates automated release gating.',
                     'trouble': 'Ensure error rate is expressed as a decimal ratio (e.g. 0.001 for 0.1%) when '
                                'computing burn rate.',
                     'cleanup': 'Retain `day-086-topic-02-burn-rate.py` as an exit evidence artifact.',
                     'accept': 'Demonstrated mastery of multi-window burn rate alerting and automated error budget '
                               'release governance.'}},
            {'key': 'topic-03',
             'title': 'Toil and automation: the Google SRE 50% rule',
             'preview': 'An operations team spends 6 hours every day manually rebooting zombie batch workers, clearing '
                        'temporary disk space, and updating spreadsheet permissions. Because they are drowned in '
                        'repetitive manual tasks, they have zero time to implement automated self-healing, causing '
                        'staff burnout and turnover.',
             'overview': 'In Google SRE taxonomy, **toil** is defined as operational work that is manual, repetitive, '
                         'automatable, tactical, devoid of enduring engineering value, and scales linearly as the '
                         'service grows. Examples of toil include manually expanding database disk volumes, restarting '
                         'stuck microservice pods, manually generating compliance reports, and manually creating GCP '
                         'service accounts. While toil is necessary to keep legacy systems running, uncontrolled toil '
                         'destroys engineering teams. Google SRE enforces the **50% Rule**: an SRE team must spend at '
                         'least 50% of its working time on engineering projects (writing software, automating '
                         'self-healing, refactoring architecture) and no more than 50% on operational toil and '
                         'tickets. If toil exceeds 50%, operational duties are redirected back to the product '
                         'development team, creating an immediate organizational incentive to engineer away manual '
                         'overhead.',
             'technical': 'Architects must categorize, measure, and eliminate toil through automated software '
                          'engineering:\n'
                          '\n'
                          '### 1. The Six Characteristics of Toil\n'
                          '- **Manual:** Typing commands in a shell or clicking console buttons.\n'
                          '- **Repetitive:** Performing the identical sequence of steps repeatedly.\n'
                          '- **Automatable:** Requires no subjective human empathy or creative design judgment; a '
                          'computer program could execute it.\n'
                          '- **Tactical:** Reactive problem-fixing rather than proactive strategic prevention.\n'
                          '- **Devoid of Enduring Value:** After the task is completed, the system is in the exact '
                          'same state as before; no permanent improvement occurred.\n'
                          '- **O(n) Scaling:** If transaction volume or server count doubles, the amount of toil '
                          'required also doubles.\n'
                          '\n'
                          '### 2. Engineering Work vs. Toil Work\n'
                          '- *Toil:* Manually restarting a crashed pod by issuing manual deletion commands in the '
                          'CLI.\n'
                          '- *Engineering:* Implementing a Kubernetes `livenessProbe` and Pod Disruption Budget so the '
                          'control plane automatically restarts the pod without human intervention.\n'
                          '- *Toil:* Manually editing firewall rules in the GCP console for a new developer.\n'
                          '- *Engineering:* Writing a Terraform module with GitOps automated PR review and Cloud Build '
                          'policy-as-code validation.\n'
                          '\n'
                          '### 3. Programmatic Toil Elimination with Google Cloud\n'
                          '- **Cloud Functions / Eventarc:** Trigger automated disk expansion scripts when Cloud '
                          'Monitoring detects disk utilization exceeding 80%.\n'
                          '- **Terraform + Workload Identity:** Automate service account provisioning and short-lived '
                          'credentials, eliminating manual key generation.',
             'questions': ['Why does toil scale linearly (O(n)) with system size if left unmitigated by software '
                           'automation?',
                           "What organizational mechanism is used when an SRE team's toil budget exceeds 50% of total "
                           'working hours?',
                           'How does replacing manual console operations with Terraform modules convert operational '
                           'toil into permanent engineering value?'],
             'reference': 'https://docs.cloud.google.com/architecture/framework/operational-excellence#automate-operations',
             'reference_label': 'Google Cloud Architecture Framework: Automating operations and eliminating toil',
             'scenario': {'symptom': "Brightloaf's infrastructure team spent 35 hours per week manually resizing Cloud "
                                     'SQL storage volumes and cleaning temporary log directories on Compute Engine '
                                     'worker VMs. Because of this overhead, the team missed its deadline to implement '
                                     'cross-region automated failover, leading to a prolonged outage during a regional '
                                     'network event.',
                          'constraints': 'Must reduce weekly manual operational toil to under 10 hours per engineer '
                                         'without hiring additional staff or increasing licensing overhead.',
                          'evidence': "Jira service desk audit showed 142 tickets created in 30 days for 'Disk "
                                      "capacity warning - manual cleanup required'. Engineers spent an average of 18 "
                                      'minutes per ticket logging into VMs, running `rm -rf /tmp/cache/*`, and '
                                      'verifying disk space.',
                          'diagnostic_steps': ['Classify all Jira operational tickets against the six characteristics '
                                               'of toil.',
                                               'Calculate total engineer-hours spent on manual disk expansion and log '
                                               'cleanup per sprint.',
                                               'Review Cloud SQL and Compute Engine auto-growth capabilities to '
                                               'identify native automated replacements.'],
                          'root': 'Failure to automate operational tasks: Cloud SQL automatic storage increase was '
                                  'disabled in Terraform, and Compute Engine log rotations were not managed by Cloud '
                                  'Logging agent lifecycle rules, generating massive repetitive toil.',
                          'fix': 'Enable `storage_auto_resize = true` with `storage_auto_resize_limit` in Terraform '
                                 'for all Cloud SQL instances, and deploy a standardized systemd `logrotate` timer '
                                 'across all Compute Engine VM images via Terraform and Cloud-Init.',
                          'verify': 'Deploy configuration changes to staging and production; verify zero manual disk '
                                    'resize tickets created over the next 30 days.',
                          'residual': 'Cloud SQL auto-resize is irreversible (disk sizes cannot be shrunk), requiring '
                                      'monitoring to prevent rogue queries from bloating disk size.',
                          'diagram': ('142 manual disk tickets',
                                      '35 hrs/wk spent on toil',
                                      'Missed HA project deadline',
                                      'Cloud SQL auto-resize ON',
                                      'Zero manual tickets'),
                          'facts': 'Team spent 35 hours per week manually cleaning disks and resizing volumes, '
                                   'crowding out resilience engineering.',
                          'inference': 'Any operational task performed more than twice without an automation backlog '
                                       'ticket constitutes harmful toil.',
                          'expected': 'Native Google Cloud managed automation handles storage scaling autonomously, '
                                      'freeing engineers for reliability projects.'},
             'lab': {'name': 'Toil Audit and Automated Cloud SQL Remediation',
                     'file': 'day-086-topic-03-toil-audit.md',
                     'goal': 'Conduct an operational toil audit, classify tasks against the SRE 50% rule, and author '
                             'Terraform automation to eliminate manual storage expansion.',
                     'expected': 'A structured Markdown audit artifact documenting toil metrics and production-ready '
                                 'Terraform code enabling Cloud SQL auto-resize.',
                     'mode': 'local script execution & verification',
                     'prereq': 'Completion of Exercises 1 and 2.',
                     'preflight': 'Review SRE book chapter on toil taxonomy.',
                     'steps': ['#### Stage 1: Pre-Flight Toil Taxonomy & The 50% Rule Invariants\n'
                               "Establish Google SRE's definition of toil: work that is manual, repetitive, "
                               'automatable, tactical, devoid of enduring value, and scales linearly with service '
                               'growth. Enforce the strict 50% rule: SRE teams must spend at least 50% of their '
                               'engineering bandwidth on substantive engineering (automation, architectural '
                               'improvements, reliability features), capping toil at <50%.',
                               '#### Stage 2: Environment Validation & Toil Log Harness\n'
                               'Author a toil audit verification script (<kbd>test_toil_calc.py</kbd>) calculating '
                               'weekly engineering ratios:\n'
                               '\n'
                               '```python\n'
                               '# test_toil_calc.py\n'
                               'weekly_hours = 40.0\n'
                               'toil_hours = 24.0  # 60% toil violation\n'
                               'toil_ratio = toil_hours / weekly_hours\n'
                               "print(f'Observed Toil Ratio: {toil_ratio * 100:.1f}%')\n"
                               "assert toil_ratio > 0.50, 'Should trigger SRE 50% rule violation'\n"
                               "print('[PASS] Toil threshold detection validated.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight test:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_toil_calc.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Automated Disk Resizing Remediation Script\n'
                               'Author the automated disk management script (<kbd>auto_resize_disk.py</kbd>) that '
                               'replaces manual disk extensions with programmatic Cloud SQL automation:\n'
                               '\n'
                               '```python\n'
                               '#!/usr/bin/env python3\n'
                               '"""auto_resize_disk.py — Automates Cloud SQL disk extension to eliminate manual '
                               'toil."""\n'
                               'from typing import Dict, Tuple\n'
                               '\n'
                               'def evaluate_disk_capacity(instance_name: str, used_gb: float, total_gb: float) -> '
                               'Tuple[bool, Dict]:\n'
                               '    utilization = (used_gb / total_gb) * 100.0\n'
                               '    if utilization >= 80.0:\n'
                               '        new_size = int(total_gb * 1.30)  # +30% automatic expansion\n'
                               '        return True, {\n'
                               "            'action': 'RESIZE_EXECUTED',\n"
                               "            'instance': instance_name,\n"
                               "            'old_size_gb': total_gb,\n"
                               "            'new_size_gb': new_size,\n"
                               "            'toil_saved_minutes': 45.0\n"
                               '        }\n'
                               "    return False, {'action': 'NO_OP', 'instance': instance_name, 'utilization_pct': "
                               'utilization}\n'
                               '\n'
                               "if __name__ == '__main__':\n"
                               "    triggered, res = evaluate_disk_capacity('brightloaf-db', used_gb=170.0, "
                               'total_gb=200.0)\n'
                               "    print(f'Remediation Result: {res}')\n"
                               "    assert triggered and res['new_size_gb'] == 260\n"
                               "    print('[PASS] Automated remediation eliminated manual disk extension toil.')\n"
                               '```',
                               '#### Stage 4: Execution & Toil Reduction Telemetry\n'
                               'Execute the automated remediation script:\n'
                               '\n'
                               '```sh\n'
                               'python3 auto_resize_disk.py\n'
                               '```\n'
                               '\n'
                               'Confirm that when disk utilization hits 85%, automatic expansion expands storage to '
                               '260 GB without human intervention.',
                               '#### Stage 5: Live Verification & Enduring Engineering Value Assertions\n'
                               'Author an assertion test (<kbd>test_toil_savings.py</kbd>) calculating annualized '
                               'engineering hours reclaimed:\n'
                               '\n'
                               '```python\n'
                               '# test_toil_savings.py\n'
                               'events_per_year = 48  # 4 disk expansions / month across fleet\n'
                               'minutes_per_manual_event = 45.0\n'
                               'hours_saved = (events_per_year * minutes_per_manual_event) / 60.0\n'
                               "print(f'Annualized SRE Hours Reclaimed: {hours_saved:.1f} hours')\n"
                               "assert hours_saved >= 36.0, 'Expected at least 36 hours saved'\n"
                               "print('[PASS] Toil elimination investment justified by measurable engineering "
                               "returns.')\n"
                               '```\n'
                               '\n'
                               'Run the verification assertions:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_toil_savings.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Manual Runbook Execution Failure Drill\n'
                               'Author a chaos script (<kbd>chaos_manual_toil_failure.py</kbd>) demonstrating human '
                               'error during manual disk resize under pressure:\n'
                               '\n'
                               '```python\n'
                               '# chaos_manual_toil_failure.py\n'
                               'def simulate_manual_intervention(fatigue_factor: float) -> str:\n'
                               '    if fatigue_factor > 0.5:\n'
                               "        return 'FATAL_HUMAN_ERROR: Fat-fingered gcloud command targeted prod instead "
                               "of staging!'\n"
                               "    return 'SUCCESS'\n"
                               '\n'
                               'res = simulate_manual_intervention(fatigue_factor=0.8)\n'
                               "assert 'FATAL_HUMAN_ERROR' in res\n"
                               "print('[PASS] Chaos test confirms manual toil introduces critical human error "
                               "vulnerabilities.')\n"
                               '```\n'
                               '\n'
                               'Execute the manual failure simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_manual_toil_failure.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Toil Audit and Automation Charter\n'
                               'Author the enterprise toil governance charter (<kbd>day-086-toil-charter.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# Day 86: SRE Toil Audit and Automation Charter\n'
                               '\n'
                               '## 1. The 50% Rule Enforcement\n'
                               '- Any task performed more than twice per week MUST be ticketed for automation.\n'
                               "- If an SRE team's sprint toil exceeds 50%, all feature review duties are suspended.\n"
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up temporary test scripts and retain core artifacts:\n'
                               '\n'
                               '```sh\n'
                               'rm -f test_toil_calc.py test_toil_savings.py chaos_manual_toil_failure.py\n'
                               'ls -lh auto_resize_disk.py day-086-toil-charter.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>auto_resize_disk.py</kbd> and <kbd>day-086-toil-charter.md</kbd> are '
                               'preserved as verifiable day evidence.'],
                     'verification': 'Document exists, clearly categorizes operational tasks against the 6 toil '
                                     'criteria, and includes valid Terraform automation code.',
                     'trouble': 'Ensure `storage_auto_resize` is explicitly enabled in Cloud SQL module '
                                'configurations.',
                     'cleanup': 'Retain `day-086-topic-03-toil-audit.md` as an exit evidence artifact.',
                     'accept': 'Completed operational toil audit matrix with verified Terraform automation pattern.'}},
            {'key': 'topic-04',
             'title': 'The Four Golden Signals: latency, traffic, errors, and saturation',
             'preview': 'An operations dashboard displays 450 separate CPU, disk, and network graphs across 50 '
                        'microservices. During a critical outage, engineers spend 40 minutes drowning in noise, unable '
                        'to determine whether the problem is latency, network saturation, or backend errors.',
             'overview': 'To cut through telemetry noise and diagnose distributed systems rapidly, Google SRE '
                         'established **The Four Golden Signals**: Latency, Traffic, Errors, and Saturation. If an '
                         'architect monitors only four things about a user-facing system, it should be these four. '
                         '**Latency** measures the time it takes to service a request (measured in percentiles: p50, '
                         'p95, p99—never misleading averages). **Traffic** measures user demand placed on the system '
                         '(e.g., HTTP QPS or concurrent connections). **Errors** measure the rate of failed requests '
                         '(explicit 5xx codes as well as implicit contract violations). **Saturation** measures how '
                         'full the system is, tracking resource utilization (CPU, memory, thread pools, database '
                         'connection queues). Saturation is the most critical leading indicator: it predicts latency '
                         'cliffs and error spikes *before* users experience an outage.',
             'technical': 'Architects must instrument the Four Golden Signals across edge and backend tiers in Google '
                          'Cloud:\n'
                          '\n'
                          '### 1. Latency: Percentiles vs. The Flaw of Averages\n'
                          'Never use average latency! If 99 requests take 10ms and 1 request takes 10,000ms, the '
                          "average is 109.9ms, masking the fact that the 10-second request timed out the user's "
                          'browser. Standardize on **p95 and p99 percentiles**:\n'
                          '- Separate latency of successful requests from failed requests: an API returning instant '
                          "500 errors will show artificially fast 'average' latency!\n"
                          '- Metric: `loadbalancing.googleapis.com/https/latencies` (distribution).\n'
                          '\n'
                          '### 2. Traffic: Measuring True Demand\n'
                          '- Track request volume at the ingress edge: '
                          '`loadbalancing.googleapis.com/https/request_count` grouped by response code class.\n'
                          '- Differentiate organic human user traffic from automated batch jobs or web scrapers.\n'
                          '\n'
                          '### 3. Errors: Explicit vs. Implicit Failures\n'
                          '- **Explicit Errors:** HTTP 5xx, gRPC `INTERNAL`, `UNAVAILABLE`, database connection '
                          'timeouts.\n'
                          '- **Implicit Errors:** HTTP 200 responses containing an error message payload (e.g., '
                          '`{"status": "error", "msg": "out of stock"}`) or empty search results. Requires custom '
                          'OpenTelemetry application metrics.\n'
                          '\n'
                          '### 4. Saturation: The Leading Indicator\n'
                          '- Track constrained resources: GKE Node CPU utilization '
                          '(`kubernetes.io/container/cpu/utilization`), Cloud SQL connection pool '
                          '(`cloudsql.googleapis.com/database/postgresql/num_backends`), and Cloud NAT port '
                          'utilization (`compute.googleapis.com/nat/allocated_ports`).\n'
                          '- Saturation alert rule: fire warning alerts when saturation crosses 75%, allowing '
                          'autoscaling or shedding before the 80% queuing cliff is breached.',
             'questions': ["Why does tracking 'average latency' mask catastrophic latency spikes experienced by the "
                           '99th percentile of users?',
                           'How does monitoring Saturation (e.g. database connection pool usage) provide earlier '
                           'warning than monitoring Error rates?',
                           "What is an 'implicit error' and why does standard HTTP status code monitoring fail to "
                           'detect it?'],
             'reference': 'https://docs.cloud.google.com/architecture/framework/reliability/monitoring-alerting',
             'reference_label': 'Google Cloud Architecture Framework: Monitoring the Four Golden Signals',
             'scenario': {'symptom': "During peak lunch hours, customers reported that Brightloaf's checkout page hung "
                                     'indefinitely when submitting orders. The primary operational dashboard showed '
                                     'green status because average CPU was only 42% and HTTP 5xx error rate was 0.05%.',
                          'constraints': 'Must establish actionable monitoring that alerts responders within 60 '
                                         'seconds of user-perceived transaction degradation.',
                          'evidence': 'Detailed log extraction revealed that while p50 latency was 45ms, p99 latency '
                                      'had spiked to 32,000ms. Furthermore, database connection pool saturation was at '
                                      '100% (96/96 connections in use), leaving incoming checkout requests queued in '
                                      'memory until client timeouts aborted them.',
                          'diagnostic_steps': ['Examine Cloud Monitoring latency distribution metrics and plot p50, '
                                               'p95, and p99 percentiles on the same chart.',
                                               'Inspect Cloud SQL PostgreSQL backend connection count to identify '
                                               'saturation ceilings.',
                                               'Verify the latency of timed-out client requests against load balancer '
                                               'HTTP 408/504 access logs.'],
                          'root': 'Operational dashboards tracked average latency and raw CPU utilization rather than '
                                  'the Four Golden Signals, blinding the team to extreme p99 latency degradation and '
                                  'complete database connection pool saturation.',
                          'fix': 'Rebuild the operational dashboard around the Four Golden Signals: graph p95/p99 '
                                 'latency percentiles, total QPS, 5xx error rate, and database/thread saturation; '
                                 'configure alerting on p99 latency > 1,500ms and connection pool saturation > 80%.',
                          'verify': 'Run load test in staging; verify dashboard immediately surfaces p99 latency '
                                    'spikes and connection saturation within 15 seconds.',
                          'residual': 'High-cardinality percentile metrics require more metric storage in Cloud '
                                      'Monitoring, slightly increasing monthly monitoring costs.',
                          'diagram': ('Avg latency shows green (45ms)',
                                      'DB connection pool 100% full',
                                      'p99 latency spikes to 32s',
                                      'Golden Signal dashboard',
                                      'Sub-60s incident detection'),
                          'facts': 'Average latency of 45ms hid a p99 latency of 32 seconds and 100% database '
                                   'connection pool saturation.',
                          'inference': 'Averages lie; distributed system health can only be accurately judged through '
                                       'percentiles and saturation metrics.',
                          'expected': 'Golden Signal dashboards provide immediate visibility into queuing saturation '
                                      'before errors manifest.'},
             'lab': {'name': 'Four Golden Signals Metric Analyzer and Alert Rule Engine',
                     'file': 'day-086-topic-04-golden-signals.py',
                     'goal': 'Write and execute a Python telemetry analyzer calculating p50/p95/p99 percentiles, error '
                             'rates, and connection saturation from raw samples.',
                     'expected': 'A runnable script demonstrating why averages conceal outages and evaluating '
                                 'automated alert triggers across all Four Golden Signals.',
                     'mode': 'local script execution & verification',
                     'prereq': 'Completion of Exercises 1, 2, and 3.',
                     'preflight': 'Verify Python runtime and initialize script template.',
                     'steps': ['#### Stage 1: Pre-Flight Four Golden Signals Architecture Scope\n'
                               'Define the Google SRE Four Golden Signals for enterprise observability:\n'
                               '1. **Latency:** Duration taken to service a request (differentiating successful '
                               'requests from errors).\n'
                               '2. **Traffic:** Demand placed upon the system (HTTP requests/second, network '
                               'throughput).\n'
                               '3. **Errors:** Rate of failing requests (explicit HTTP 5xx codes, implicit policy '
                               'denials).\n'
                               '4. **Saturation:** Utilization percentage of the most constrained resource fraction '
                               '(CPU cgroup, memory, DB connection pool).',
                               '#### Stage 2: Environment Preflight & Metrics Calibration\n'
                               'Author a metrics environment test (<kbd>test_signals_env.py</kbd>) establishing '
                               'baseline healthy thresholds:\n'
                               '\n'
                               '```python\n'
                               '# test_signals_env.py\n'
                               "signals = {'latency_p99_ms': 120.0, 'traffic_rps': 850.0, 'error_rate_pct': 0.02, "
                               "'saturation_pct': 58.0}\n"
                               "assert signals['latency_p99_ms'] < 250.0 and signals['error_rate_pct'] < 0.1\n"
                               "print('[PASS] Golden signal baseline thresholds calibrated.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight test:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_signals_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Golden Signals Evaluation Engine\n'
                               'Author the Golden Signals telemetry analyzer (<kbd>golden_signals_analyzer.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '#!/usr/bin/env python3\n'
                               '"""golden_signals_analyzer.py — Evaluates the Four Golden Signals against alerting '
                               'thresholds."""\n'
                               'from typing import Dict, List\n'
                               '\n'
                               'def evaluate_signals(metrics: Dict[str, float]) -> List[str]:\n'
                               '    alerts = []\n'
                               "    if metrics.get('latency_p99_ms', 0) > 250.0:\n"
                               "        alerts.append('ALERT: Latency p99 > 250ms breach')\n"
                               "    if metrics.get('error_rate_pct', 0) > 0.50:\n"
                               "        alerts.append('ALERT: Error rate > 0.5% breach')\n"
                               "    if metrics.get('saturation_pct', 0) > 85.0:\n"
                               "        alerts.append('ALERT: Saturation > 85% capacity threshold')\n"
                               '    return alerts\n'
                               '\n'
                               "if __name__ == '__main__':\n"
                               "    telemetry = {'latency_p99_ms': 420.0, 'traffic_rps': 1200.0, 'error_rate_pct': "
                               "1.80, 'saturation_pct': 92.0}\n"
                               '    fired_alerts = evaluate_signals(telemetry)\n'
                               "    print(f'Triggered Golden Signal Alerts: {fired_alerts}')\n"
                               "    assert len(fired_alerts) == 3, 'Expected 3 alerts fired under stress'\n"
                               "    print('[PASS] Golden signals analyzer accurately flagged degradation across "
                               "latency, errors, and saturation.')\n"
                               '```',
                               '#### Stage 4: Execution & Observability Telemetry Analysis\n'
                               'Execute the golden signals analyzer:\n'
                               '\n'
                               '```sh\n'
                               'python3 golden_signals_analyzer.py\n'
                               '```\n'
                               '\n'
                               'Confirm that degraded metrics generate precise alerts targeting latency, error rate, '
                               'and saturation.',
                               '#### Stage 5: Live Verification & Metric Correlation Assertions\n'
                               'Author an assertion test (<kbd>test_metric_correlation.py</kbd>) proving that '
                               'saturation leading indicators precede latency degradation:\n'
                               '\n'
                               '```python\n'
                               '# test_metric_correlation.py\n'
                               'from golden_signals_analyzer import evaluate_signals\n'
                               '\n'
                               '# Early saturation warning before latency spikes\n'
                               "early_stage = {'latency_p99_ms': 180.0, 'traffic_rps': 950.0, 'error_rate_pct': 0.05, "
                               "'saturation_pct': 88.0}\n"
                               'early_alerts = evaluate_signals(early_stage)\n'
                               "assert len(early_alerts) == 1 and 'Saturation' in early_alerts[0]\n"
                               "print('[PASS] Leading indicator verified: Saturation alert fires before user latency "
                               "degrades.')\n"
                               '```\n'
                               '\n'
                               'Run the verification test:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_metric_correlation.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Hidden Metric Blackout Drill\n'
                               'Author a chaos script (<kbd>chaos_metric_blackout.py</kbd>) demonstrating what happens '
                               'when saturation metrics are omitted:\n'
                               '\n'
                               '```python\n'
                               '# chaos_metric_blackout.py\n'
                               'def detect_failure_without_saturation(latency_ms: float, errors_pct: float) -> str:\n'
                               '    if latency_ms < 200 and errors_pct < 0.1:\n'
                               "        return 'FALSE_SENSE_OF_SECURITY: System appears healthy while connection pool "
                               "is 99% full!'\n"
                               "    return 'DEGRADED'\n"
                               '\n'
                               'res = detect_failure_without_saturation(150.0, 0.02)\n'
                               "assert 'FALSE_SENSE_OF_SECURITY' in res\n"
                               "print('[PASS] Chaos test proves saturation is an indispensable leading indicator.')\n"
                               '```\n'
                               '\n'
                               'Execute the blackout simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_metric_blackout.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Google Cloud Prometheus Alerting Manifest\n'
                               'Author declarative Prometheus alert rules for Cloud Monitoring '
                               '(<kbd>golden_signals_alerts.yaml</kbd>):\n'
                               '\n'
                               '```yaml\n'
                               "cat <<'YAML' > golden_signals_alerts.yaml\n"
                               'apiVersion: monitoring.googleapis.com/v1\n'
                               'kind: Rules\n'
                               'metadata:\n'
                               '  name: golden-signals-rules\n'
                               'spec:\n'
                               '  groups:\n'
                               '  - name: golden-signals\n'
                               '    rules:\n'
                               '    - alert: HighRequestLatency\n'
                               '      expr: histogram_quantile(0.99, '
                               'sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 0.25\n'
                               '      for: 2m\n'
                               '      labels:\n'
                               '        severity: page\n'
                               '    - alert: DatabasePoolSaturation\n'
                               '      expr: sum(pg_stat_activity_count) / sum(pg_settings_max_connections) > 0.85\n'
                               '      for: 3m\n'
                               '      labels:\n'
                               '        severity: ticket\n'
                               'YAML\n'
                               'cat golden_signals_alerts.yaml\n'
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up temporary test scripts and retain core alert configurations:\n'
                               '\n'
                               '```sh\n'
                               'rm -f test_signals_env.py test_metric_correlation.py chaos_metric_blackout.py\n'
                               'ls -lh golden_signals_analyzer.py golden_signals_alerts.yaml\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>golden_signals_analyzer.py</kbd> and '
                               '<kbd>golden_signals_alerts.yaml</kbd> are preserved as verifiable day evidence.'],
                     'verification': 'Script runs cleanly and displays accurate mathematical percentile calculations '
                                     'and golden signal alert evaluations.',
                     'trouble': 'Ensure data array is sorted in ascending order before evaluating percentiles.',
                     'cleanup': 'Retain `day-086-topic-04-golden-signals.py` as an exit evidence artifact.',
                     'accept': 'Demonstrated mastery of the Four Golden Signals, percentile mathematics, and '
                               'saturation monitoring.'}}],
 'part3_intro': 'The following field cases analyze real-world production catastrophes resulting from conflating '
                'internal SLOs with external SLAs, reckless release pushes during active error budget exhaustion, '
                'runaway operational toil violating the SRE 50% cap, and blind spots in Golden Signal monitoring. Each '
                'case details quantifiable failure metrics, verbatim terminal/log transcripts, diagnostic command '
                'sequences, root cause mechanics, defensible remediations, and dual-lane failed/corrected '
                'architectural diagrams.',
 'part4_intro': 'These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author '
                'production SLI calculation scripts, build multi-window multi-burn-rate release policy engines that '
                'gate CI/CD deployment pipelines, automate operational toil with Cloud SQL remediation scripts, and '
                'instrument Google Cloud Monitoring Prometheus alerts across the Four Golden Signals with zero '
                'difficulty labels.'}
