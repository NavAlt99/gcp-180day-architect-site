"""day_data_097.py — Exhaustive architecture data specification for Day 97.

Covers Performance Baselines, Bounded Service Failures, and Zonal Limits.
"""

DAY_NUM = 97

DATA = {'day': 97,
 'part1_intro': 'Day 97 moves from experiment design to empirical execution: applying bounded service failure and '
                'overload conditions against a target workload, recording before/during/after telemetry, and revising '
                'architectural capacity and recovery models. Resilience is not a binary state; it is a measurable '
                "curve of degradation and recovery. Today's curriculum evaluates performance baselines using "
                'statistical regression analysis, executes automated MIG autohealing fault injection to test instance '
                'recreation and traffic draining, and synthesizes distributed trace data to model multi-zonal failure '
                'boundaries and document explicit tabletop simulation limits.',
 'exit_summary': 'Executed an empirical Recovery and Overload Experiment: captured before/during/after statistical '
                 'performance baselines across P50/P95/P99 latency percentiles; executed a bounded Compute Engine MIG '
                 'autohealing drill proving zero-downtime instance recreation; authored a zonal outage trace '
                 'simulation model with a revised capacity recovery plan and explicit simulation limitation '
                 'boundaries.',
 'part2_intro': 'Empirical resilience validation requires establishing a pristine pre-test baseline, introducing an '
                'isolated failure state, measuring degradation metrics, and recording the time-to-recovery (TTR) '
                'curve. The sections below analyze performance baseline math, MIG autohealing mechanics, and '
                'trace-based zonal partition modeling.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Experiment Phase / Component</th>\n'
                    '      <th>GCP Mechanism / Metric</th>\n'
                    '      <th>Observed Telemetry Signal</th>\n'
                    '      <th>Acceptance Criteria &amp; Target</th>\n'
                    '      <th>Simulation Boundary / Limitation</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>Phase 1: Baseline Steady State</strong></td>\n'
                    '      <td>Cloud Monitoring `https/request_latencies`</td>\n'
                    '      <td>P50: 38ms, P95: 110ms, P99: 185ms; Error rate: 0.00%</td>\n'
                    '      <td>P99 latency &lt; 250ms under 5,000 req/sec steady load</td>\n'
                    '      <td>Does not reflect extreme holiday traffic concurrency spikes</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Phase 2: Fault Injection (Autohealing)</strong></td>\n'
                    '      <td>Compute Engine MIG Autohealing Policy</td>\n'
                    '      <td>Health check fails; instance state changes to `RECREATING`</td>\n'
                    '      <td>In-flight TCP drain: 30s; Replacement VM active &lt; 90s</td>\n'
                    '      <td>Single-instance fault; does not test simultaneous multi-node rolling crash</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Phase 3: Zonal Failure Modeling</strong></td>\n'
                    '      <td>Cloud Trace &amp; Cross-Zone VPC Flow Logs</td>\n'
                    '      <td>Cross-zone round-trip time jumps from 0.8ms to timeout (drop)</td>\n'
                    '      <td>Traffic rerouted to remaining 2 zones within 15 seconds</td>\n'
                    '      <td>Simulated via synthetic trace data; cloud provider-level fiber cut cannot be physically '
                    'enacted</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Phase 4: Post-Recovery State</strong></td>\n'
                    '      <td>Cloud Monitoring &amp; Log Analytics</td>\n'
                    '      <td>MIG target size restored (3/3 instances healthy); Latency P99: 190ms</td>\n'
                    '      <td>100% capacity restored; 0 persistent error log artifacts</td>\n'
                    '      <td>Warm-up cache effects: initial requests post-reboot incur slight JVM/JIT compilation '
                    'latency</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 97: Performance Baseline Analysis, MIG Autohealing, and Zonal Failure Modeling',
                  'desc': 'Architectural topology illustrating synthetic baseline sampling, regional MIG autohealing '
                          'control loops, and distributed trace tabletop failure modeling.',
                  'caption': 'Figure 97.1: Architectural control plane for statistical regression detection, MIG '
                             'autohealing dampening, and zonal tabletop blast radius isolation.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Synthetic Probing & Ingress Baseline Perimeter',
                              'desc': 'Synthetic latency probes, baseline traffic ingestion, and statistical sampling',
                              'y': 10,
                              'h': 90,
                              'stroke': '#38bdf8',
                              'fill': '#0c1e38',
                              'title_color': '#38bdf8'},
                             {'name': 'LAYER 2: Regional Load Balancer & Health Probing Fabric',
                              'desc': 'Regional External ALB, health check probes, and traffic distribution',
                              'y': 115,
                              'h': 90,
                              'stroke': '#818cf8',
                              'fill': '#141838',
                              'title_color': '#818cf8'},
                             {'name': 'LAYER 3: Multi-Zone Managed Instance Group (MIG) Runtime',
                              'desc': 'Compute Engine instances across us-central1-a, b, and c with auto-scaling',
                              'y': 220,
                              'h': 90,
                              'stroke': '#f59e0b',
                              'fill': '#261a08',
                              'title_color': '#f59e0b'},
                             {'name': 'LAYER 4: Autohealing Controller & Load Shedding Gate',
                              'desc': 'MIG autohealing daemon, calibrated initial delay, and graceful degradation '
                                      'intercept',
                              'y': 325,
                              'h': 90,
                              'stroke': '#f43f5e',
                              'fill': '#2a0a14',
                              'title_color': '#f43f5e'},
                             {'name': 'LAYER 5: SRE Observability, Cloud Trace & Regression Engine',
                              'desc': 'Distributed trace waterfall, statistical percentile regression, and tabletop '
                                      'audit',
                              'y': 430,
                              'h': 90,
                              'stroke': '#22c55e',
                              'fill': '#072417',
                              'title_color': '#22c55e'}],
                  'components': [{'name': 'Synthetic Latency Probe',
                                  'detail': '1,000 req/min Continuous',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'Client Ingress Edge',
                                  'detail': 'Global HTTPS VIP',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'Regional ALB',
                                  'detail': 'Backend Service Routing',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Health Check Engine',
                                  'detail': 'Interval 10s, Threshold 3',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'MIG Zone A (Target)',
                                  'detail': 'Failure Simulation Node',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'MIG Zone B (Surviving)',
                                  'detail': 'Active Workload Node',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'MIG Autohealing Daemon',
                                  'detail': '300s Initial Delay Guard',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Load Shedding Gate',
                                  'detail': 'HTTP 429 / Degraded Shed',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Cloud Trace Waterfall',
                                  'detail': 'Cross-Zone Latency Trace',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'},
                                 {'name': 'Statistical Regression Test',
                                  'detail': 'Mann-Whitney U Analysis',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'}],
                  'boundaries': [{'label': 'INGRESS PROBING & TRAFFIC DISTRIBUTION BOUNDARY',
                                  'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'color': '#38bdf8'},
                                 {'label': 'REGIONAL MIG MULTI-ZONE RESILIENCY PERIMETER',
                                  'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#818cf8'},
                                 {'label': 'AUTOHEALING GOVERNANCE & TRACE ANALYSIS VAULT',
                                  'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#22c55e'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Inject Synthetic Trace', 'type': 'ok'},
                            {'x1': 210,
                             'y1': 82,
                             'x2': 210,
                             'y2': 135,
                             'label': 'Forward to Regional ALB',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'label': 'Poll /healthz Endpoint',
                             'type': 'ok'},
                            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Balance Across Zones', 'type': 'ok'},
                            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Zone A Network Cut', 'type': 'fail'},
                            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Dampened Autohealing', 'type': 'ok'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'label': 'Activate Load Shedding',
                             'type': 'warn'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'label': 'Extract Trace Timeline',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'label': 'Assert Regression Free',
                             'type': 'ok'}],
                  'probes': [{'cx': 80,
                              'cy': 30,
                              'label': 'PROBE 1: P99 Latency Regression (>35ms)',
                              'badge': 'P1',
                              'color': '#38bdf8'},
                             {'cx': 80,
                              'cy': 345,
                              'label': 'PROBE 2: Autohealing Boot Flap Trigger',
                              'badge': 'FI',
                              'color': '#f43f5e'},
                             {'cx': 420,
                              'cy': 450,
                              'label': 'PROBE 3: Mann-Whitney U p-value (<0.01)',
                              'badge': 'P3',
                              'color': '#22c55e'}]},
 'topics': [{'key': 'topic-01',
             'title': 'Performance Baselines and Statistical Regression Analysis',
             'overview': 'Before conducting a resilience or load experiment, engineers must establish a mathematically '
                         'rigorous performance baseline. A baseline is not a single average latency number; it is a '
                         'probability distribution of response times, throughput rates, and resource utilizations '
                         'captured over a statistically significant steady-state window. Automated regression analysis '
                         'compares post-change or under-stress distributions against this baseline using '
                         'non-parametric percentile gates (P95, P99), detecting performance degradation before it '
                         'breaches user-facing Service Level Objectives.',
             'preview': 'An engineering team reviews average response times and concludes an experiment caused no '
                        'impact, missing that P99 latency doubled for 500 shoppers. Percentile distribution baselines '
                        'isolate tail latency regressions that averages completely disguise.',
             'technical': '### 1. Statistical Baseline Methodology\n'
                          '- **Sampling Duration:** Baseline capture requires a minimum 30-minute steady-state run at '
                          'typical production operating concurrency to allow JVM JIT compilation, database buffer pool '
                          'warming, and autoscaler stabilization.\n'
                          '- **Why Arithmetic Averages Deceive:** In a sample of 10,000 requests, 9,900 requests '
                          'completing in 10ms with 100 requests taking 5,000ms yields an average latency of only '
                          '59.9ms (which appears acceptable). However, the P99 is 5,000ms—meaning 1 out of every 100 '
                          'users experiences an unacceptable 5-second freeze.\n'
                          '\n'
                          '### 2. Quantifying Regression Margins\n'
                          '- **Acceptable Variance vs Regressions:** Normal network jitter and CPU scheduling variance '
                          'introduce +/- 5% fluctuation. A **Performance Regression** is formally declared when:\n'
                          '  1. $P95_{\\text{observed}} > 1.15 \\times P95_{\\text{baseline}}$ (15% degradation).\n'
                          '  2. $P99_{\\text{observed}} > 1.25 \\times P99_{\\text{baseline}}$ (25% degradation).\n'
                          '  3. Error rate exceeds baseline by $>0.1\\%$.\n'
                          '\n'
                          '### 3. Automated Metric Extraction with MQL\n'
                          '- Using Google Cloud Monitoring Query Language (MQL), baseline extraction is automated '
                          'across percentiles:\n'
                          "  `fetch https_lb_rule | metric 'loadbalancing.googleapis.com/https/backend_latencies'`\n"
                          '  `| group_by [resource.backend_target_name], 1m, percentile(99)`\n'
                          '  `| every 1m`.',
             'questions': ['Why must performance baselines be evaluated using percentile distributions (P50, P95, P99) '
                           'rather than arithmetic averages?',
                           'What minimum duration and conditions are required to establish an uncorrupted steady-state '
                           'baseline in cloud environments?',
                           'How does MQL percentile aggregation simplify automated regression detection in continuous '
                           'deployment pipelines?'],
             'reference': 'https://docs.cloud.google.com/monitoring/mql/reference',
             'reference_label': 'Google Cloud Monitoring: MQL percentile aggregations and statistical evaluation',
             'scenario': {'symptom': 'Following a minor database library upgrade, customer support tickets regarding '
                                     'slow cart checkouts increased by 40%, yet the CI/CD pipeline automated test '
                                     "suite reported 'Average Response Time = 62ms (PASSED)'.",
                          'constraints': 'Must establish an automated statistical regression gate in the experiment '
                                         'pipeline that detects tail latency regressions.',
                          'evidence': 'Production latency percentiles over 14 days:\n'
                                      '\n'
                                      '```text\n'
                                      'Baseline (v2.1.0): Mean: 22ms, P50: 18ms, P90: 38ms, P99: 45ms, P99.9: 82ms\n'
                                      'Current  (v2.2.0): Mean: 24ms, P50: 19ms, P90: 42ms, P99: 148ms, P99.9: 890ms\n'
                                      'Alert status: Mean-latency alert (threshold > 50ms) did NOT trigger (24ms < '
                                      '50ms).\n'
                                      '```\n'
                                      '\n'
                                      'Database lock contention log:\n'
                                      '\n'
                                      '```text\n'
                                      '2026-09-29T08:12:00Z [WARN] PostgreSQL: process 4128 waiting for ExclusiveLock '
                                      'on table user_sessions\n'
                                      'Lock wait duration: 1042ms (caused by unindexed foreign key check introduced in '
                                      'v2.2.0 migration)\n'
                                      '```',
                          'diagnostic_steps': ['Compare Cloud Monitoring latency distribution heatmaps before and '
                                               'after the release.',
                                               'Calculate P50, P90, P95, and P99 percentiles across both sample '
                                               'windows.',
                                               'Audit CI/CD performance testing gates to verify metric evaluation '
                                               'formulas.'],
                          'root': 'Flawed metric evaluation: relying on average response time hid a 15x tail latency '
                                  'degradation affecting 1% of all checkout customers.',
                          'fix': 'Replace average response time assertions with strict percentile regression formulas '
                                 '(assert $P95 \\le 1.15 \\times \\text{baseline}$ and $P99 \\le 1.25 \\times '
                                 '\\text{baseline}$). Deploy automated regression analysis scripts in staging.',
                          'verify': 'Run automated regression script against the bad release; verify the script flags '
                                    'a P99 regression failure and halts promotion.',
                          'residual': 'Percentile metrics require sufficient sample volume; evaluating P99 on fewer '
                                      'than 100 requests produces statistical noise.',
                          'diagram': ('New release deployed with unindexed table',
                                      'Mean latency unchanged at 24ms',
                                      'P99 latency explodes from 45ms to 148ms',
                                      'Enforce automated Mann-Whitney U test on P99',
                                      'CI/CD blocks release before production rollout')},
             'lab': {'name': 'Statistical Performance Baseline and Regression Analysis Engine',
                     'goal': 'Author an automated Python statistical analysis engine comparing baseline distributions '
                             'with experimental degradation runs.',
                     'expected': 'An executable Python script calculating P50, P95, and P99 percentiles, detecting '
                                 'statistical regressions, and printing an evaluation report.',
                     'mode': 'local script execution',
                     'prereq': 'Understanding of percentiles and statistical distributions.',
                     'preflight': 'Ensure Python 3 standard library is present; no external packages needed.',
                     'steps': ['#### Stage 1: Pre-Flight Statistical Distribution Discovery\n'
                               'Inspect sample response time distributions to determine why mean averages obscure '
                               'long-tail regressions:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > analyze_skewness.py\n"
                               'import statistics\n'
                               '\n'
                               'normal_traffic = [18, 19, 20, 21, 22, 23, 24, 25, 45, 82]\n'
                               'regressed_traffic = [18, 19, 20, 21, 22, 23, 24, 25, 148, 890]\n'
                               '\n'
                               "print(f'[PREFLIGHT] Baseline Mean: {statistics.mean(normal_traffic):.1f}ms | P99 "
                               "proxy: {max(normal_traffic)}ms')\n"
                               "print(f'[PREFLIGHT] Regressed Mean: {statistics.mean(regressed_traffic):.1f}ms | P99 "
                               "proxy: {max(regressed_traffic)}ms')\n"
                               "print('[OBSERVATION] Mean shifted by only 80ms while tail latency degraded by "
                               "808ms!')\n"
                               'EOF\n'
                               'python3 analyze_skewness.py\n'
                               '```',
                               '#### Stage 2: Infrastructure Preflight & SciPy Environment Inspection\n'
                               'Verify statistical analysis library availability in local environment:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_stats_env.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Verifying statistical computation engine..."\n'
                               'python3 -c "import math; print(\'[PASS] Standard mathematical runtime verified.\')"\n'
                               'echo "[PASS] Statistical inspection environment ready."\n'
                               'EOF\n'
                               'bash check_stats_env.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Non-Parametric Regression Detector\n'
                               'Author a Python statistical module implementing Mann-Whitney U ranking to detect '
                               'latency shifts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > statistical_regression_detector.py\n"
                               'def compute_mann_whitney_u(baseline, candidate):\n'
                               '    """Compute Mann-Whitney U test statistic for non-parametric distribution '
                               'comparison."""\n'
                               '    n1, n2 = len(baseline), len(candidate)\n'
                               "    combined = [(val, 'A') for val in baseline] + [(val, 'B') for val in candidate]\n"
                               '    combined.sort(key=lambda x: x[0])\n'
                               '    \n'
                               "    rank_b = sum(i + 1 for i, (val, grp) in enumerate(combined) if grp == 'B')\n"
                               '    u2 = rank_b - (n2 * (n2 + 1)) / 2\n'
                               '    u1 = (n1 * n2) - u2\n'
                               '    u_stat = min(u1, u2)\n'
                               '    \n'
                               '    # Check if candidate median/P99 is significantly higher\n'
                               '    p99_base = sorted(baseline)[int(n1 * 0.95)]\n'
                               '    p99_cand = sorted(candidate)[int(n2 * 0.95)]\n'
                               '    regressed = (p99_cand > p99_base * 1.25) and (u_stat < (n1 * n2 * 0.3))\n'
                               '    return regressed, p99_base, p99_cand\n'
                               '\n'
                               "if __name__ == '__main__':\n"
                               '    base = [20, 22, 21, 23, 19, 25, 24, 28, 45, 50] * 10\n'
                               '    bad = [20, 22, 21, 23, 19, 25, 24, 28, 140, 195] * 10\n'
                               '    is_reg, b_p99, c_p99 = compute_mann_whitney_u(base, bad)\n'
                               "    print(f'[ANALYSIS] Baseline P95: {b_p99}ms | Candidate P95: {c_p99}ms | Regressed: "
                               "{is_reg}')\n"
                               "    assert is_reg, 'Failed to detect tail latency regression!'\n"
                               'EOF\n'
                               'python3 statistical_regression_detector.py\n'
                               '```',
                               '#### Stage 4: Execution & CI/CD Pipeline Gate Integration\n'
                               'Author a CI/CD build gate script reading benchmark JSON output and asserting zero tail '
                               'regressions:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > cicd_performance_gate.py\n"
                               'import json\n'
                               'from statistical_regression_detector import compute_mann_whitney_u\n'
                               '\n'
                               'benchmark_data = {\n'
                               "    'baseline_ms': [21, 22, 20, 23, 22, 21, 24, 25, 42, 45] * 5,\n"
                               "    'release_candidate_ms': [21, 22, 20, 23, 22, 21, 24, 25, 44, 48] * 5\n"
                               '}\n'
                               '\n'
                               'regressed, b_p99, c_p99 = compute_mann_whitney_u(\n'
                               "    benchmark_data['baseline_ms'], benchmark_data['release_candidate_ms']\n"
                               ')\n'
                               'if regressed:\n'
                               "    print(f'[CI GATE REJECT] Regression detected! Candidate P99 {c_p99}ms vs Baseline "
                               "{b_p99}ms')\n"
                               '    exit(1)\n'
                               'else:\n'
                               "    print(f'[CI GATE APPROVE] Release approved. Candidate P99 {c_p99}ms within "
                               "tolerance.')\n"
                               'EOF\n'
                               'python3 cicd_performance_gate.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Synthetic Jitter Chaos Injection\n'
                               'Simulate transient network packet drops causing synthetic tail latency spikes and test '
                               'detection sensitivity:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_sensitivity.py\n"
                               'from statistical_regression_detector import compute_mann_whitney_u\n'
                               '\n'
                               'base = [20, 21, 22, 23, 24, 25] * 15\n'
                               '# 5% of requests hit 300ms network timeout\n'
                               'jitter_injected = [20, 21, 22, 23, 24, 25] * 14 + [300] * 6\n'
                               '\n'
                               'regressed, b_p99, c_p99 = compute_mann_whitney_u(base, jitter_injected)\n'
                               "print(f'[CHAOS TEST] Jitter test result: Regressed={regressed} (Baseline P95: "
                               "{b_p99}ms, Injected P95: {c_p99}ms)')\n"
                               "assert regressed, 'Detector insensitive to 5% tail latency spikes!'\n"
                               "print('[PASS] Tail latency detector caught intermittent timeout spikes.')\n"
                               'EOF\n'
                               'python3 test_sensitivity.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Cloud Monitoring SLO Manifest\n'
                               'Author a Cloud Monitoring Latency SLO configuration targeting P99 < 100ms over 28-day '
                               'rolling window:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > slo_p99_latency.json\n"
                               '{\n'
                               '  "displayName": "Core API P99 Latency SLO",\n'
                               '  "goal": 0.99,\n'
                               '  "rollingPeriod": "2419200s",\n'
                               '  "serviceLevelIndicator": {\n'
                               '    "requestBased": {\n'
                               '      "distributionCut": {\n'
                               '        "distributionFilter": '
                               '"metric.type=\\"loadbalancing.googleapis.com/https/backend_latencies\\"",\n'
                               '        "range": {"start": 0.0, "end": 100.0}\n'
                               '      }\n'
                               '    }\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[SLO] Authored slo_p99_latency.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Statistical Precision Assertions\n'
                               'Execute automated test validating mathematical edge cases in regression detection:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_statistical_precision.py\n"
                               'from statistical_regression_detector import compute_mann_whitney_u\n'
                               '\n'
                               '# Identical distributions must return False\n'
                               'd = [10, 20, 30, 40, 50] * 10\n'
                               'reg, _, _ = compute_mann_whitney_u(d, d)\n'
                               "assert not reg, 'Identical distributions incorrectly marked as regressed'\n"
                               "print('[ASSERT PASS] Statistical regression precision mathematically verified.')\n"
                               'EOF\n'
                               'python3 assert_statistical_precision.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary benchmark scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_baseline_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 97 Topic 1 test scripts..."\n'
                               'rm -f analyze_skewness.py check_stats_env.sh statistical_regression_detector.py '
                               'cicd_performance_gate.py test_sensitivity.py assert_statistical_precision.py\n'
                               'echo "[CLEANUP] Retaining SLO configuration: slo_p99_latency.json"\n'
                               'echo "[CLEANUP PASS] Baseline analysis lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_baseline_lab.sh\n'
                               '```'],
                     'verification': 'The Python regression engine accurately calculates percentiles and rejects '
                                     'candidate runs exceeding the 25% P99 tolerance threshold.',
                     'trouble': 'Ensure `numpy` is installed or fallback to pure Python standard library `statistics` '
                                'module if numpy is unavailable.',
                     'cleanup': 'Retain `evaluate_regression.py` as an exit evidence artifact.',
                     'accept': 'Completed statistical baseline script and verified regression engine. File: '
                               '`day-097-topic-01-baseline-regression.md`.',
                     'file': 'day-097-topic-01-baseline-regression.md'}},
            {'key': 'topic-02',
             'title': 'Bounded Service Failure: MIG Autohealing and Controlled Degradation',
             'overview': 'A Managed Instance Group (MIG) with an autohealing policy automatically monitors instance '
                         'health using application-level health checks and recreates failing or dead virtual machines '
                         'without manual intervention. However, misconfigured autohealing policies can cause '
                         "'autohealing storms'—where healthy instances experiencing transient load spikes are "
                         'prematurely declared unhealthy and rebooted simultaneously, wiping out remaining cluster '
                         'capacity. Properly tuning initial delay, check interval, and unhealthy thresholds guarantees '
                         'that autohealing heals genuine crashes while absorbing temporary overload.',
             'preview': 'A database connection hiccup causes an app health check to fail once, prompting the MIG to '
                        'terminate and recreate all 10 frontend VMs at once. Configuring autohealing initial delays '
                        'and consecutive failure thresholds ensures resilience without destructive mass reboots.',
             'technical': '### 1. MIG Autohealing Architecture and Health Checks\n'
                          '- **Application Health Check:** Distinct from Load Balancing health checks. While Load '
                          'Balancing health checks decide whether to route traffic to an instance, the **Autohealing '
                          'Health Check** decides whether to **delete and recreate** the instance.\n'
                          '- **Initial Delay (Grace Period):** Defines how long the MIG must wait after an instance '
                          'boots before checking its health check (e.g. `initialDelaySec: 120`). If the initial delay '
                          'is shorter than the application bootstrap and JIT warmup time, the MIG enters an infinite '
                          'crash-recreate loop.\n'
                          '\n'
                          '### 2. Autohealing Timing Parameters\n'
                          '- `checkIntervalSec`: Frequency of probes (e.g. 5 seconds).\n'
                          '- `timeoutSec`: Max wait time for response before counting as failure (e.g. 3 seconds).\n'
                          '- `unhealthyThreshold`: Number of consecutive failures required before recreation is '
                          'triggered (e.g. 3 consecutive failures = 15s).\n'
                          '- `healthyThreshold`: Number of consecutive successes required to return to healthy status '
                          '(e.g. 2 consecutive successes).\n'
                          '\n'
                          '### 3. Graceful Draining and Recreation Mechanics\n'
                          '- When an instance is marked unhealthy, the MIG notifies the backend service to initiate '
                          '**Connection Draining** (e.g. 30 seconds).\n'
                          '- Existing TCP connections are allowed to terminate gracefully while new requests are '
                          'routed exclusively to healthy instances.\n'
                          '- After the draining timeout elapses, the MIG sends ACPI shutdown, deletes the ephemeral '
                          'root disk, and provisions a fresh VM from the instance template.',
             'questions': ['What is the critical architectural difference between a Load Balancer health check and a '
                           'MIG Autohealing health check?',
                           'What failure mode occurs if the autohealing `initialDelaySec` is configured shorter than '
                           'application startup time?',
                           'How does connection draining protect in-flight transactions when an unhealthy instance is '
                           'scheduled for autohealing recreation?'],
             'reference': 'https://docs.cloud.google.com/compute/docs/instance-groups/autohealing-instances-in-migs',
             'reference_label': 'Google Compute Engine: Setting up and configuring autohealing in Managed Instance '
                                'Groups',
             'scenario': {'symptom': "During a minor traffic surge, all 8 instances in Brightloaf's regional MIG were "
                                     'rebooted simultaneously by the autohealing system, causing a complete 4-minute '
                                     'service outage that dropped all live customer shopping carts.',
                          'constraints': 'Must configure autohealing so that localized instance crashes are repaired '
                                         'within 90 seconds while transient overload never triggers mass reboots.',
                          'evidence': 'Compute Engine MIG autohealing event log:\n'
                                      '\n'
                                      '```text\n'
                                      "2026-09-29T11:00:15Z Instance 'api-mig-8f12' recreating: health check reported "
                                      'UNHEALTHY\n'
                                      "2026-09-29T11:00:45Z Instance 'api-mig-8f12' started, applying startup scripts\n"
                                      '2026-09-29T11:01:05Z Health check prober: GET /healthz -> 503 Service '
                                      'Unavailable (JVM warming up)\n'
                                      "2026-09-29T11:01:10Z Instance 'api-mig-8f12' recreating: health check reported "
                                      'UNHEALTHY\n'
                                      'MIG autohealing thrash count: 184 instance recreations in 15 minutes. Fleet '
                                      'capacity collapsed to 0%.\n'
                                      '```',
                          'diagnostic_steps': ['Inspect MIG autohealing policy via `gcloud compute instance-groups '
                                               'managed describe`.',
                                               'Review health check configuration parameters and probe path.',
                                               'Examine Compute Engine system event logs to trace recreation '
                                               'timestamps.'],
                          'root': 'Overly aggressive autohealing thresholds: querying a deep database endpoint with an '
                                  'unhealthy threshold of 1 meant a momentary database queue delay caused all healthy '
                                  'instances to fail their probe simultaneously and get destroyed.',
                          'fix': 'Separate health check concerns: point autohealing to a lightweight shallow endpoint '
                                 '(`/healthz/shallow`) that verifies only local process liveness. Increase '
                                 '`unhealthyThreshold` to 3 and configure an `initialDelaySec` of 120 seconds.',
                          'verify': 'Simulate localized process failure by terminating the application process on one '
                                    'VM; verify that only that single VM is recreated after 15 seconds while the other '
                                    '7 instances continue serving traffic without interruption.',
                          'residual': 'A shallow health check does not detect backend database disconnections; '
                                      'database dependency failures must be handled via circuit breakers, not VM '
                                      'recreation.',
                          'diagram': ('Application JVM takes 90s to warm up',
                                      'MIG initial delay set to only 30s',
                                      'Autohealing kills VM before it can boot',
                                      'Calibrate initial delay to 300s & separate probers',
                                      'Fleet boots smoothly with zero autohealing flapping')},
             'lab': {'name': 'Compute Engine MIG Autohealing Fault Injection and Recreation Drill',
                     'goal': 'Author a production MIG autohealing policy specification and simulate controlled '
                             'instance failure and automated recreation.',
                     'expected': 'A validated gcloud autohealing deployment script, an executable Python state-machine '
                                 'simulator, and a recovery log artifact.',
                     'mode': 'tabletop analysis & shell synthesis',
                     'prereq': 'Understanding of Compute Engine Managed Instance Groups and health checks.',
                     'preflight': 'Review gcloud compute health-checks and instance-groups CLI commands.',
                     'steps': ['#### Stage 1: Pre-Flight MIG & Health Check Specification Audit\n'
                               'Catalog existing Compute Engine health check parameters and initial delay settings:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > audit_health_checks.py\n"
                               'hc_params = {\n'
                               "    'check_interval_sec': 5,\n"
                               "    'timeout_sec': 5,\n"
                               "    'unhealthy_threshold': 2,\n"
                               "    'healthy_threshold': 2,\n"
                               "    'autohealing_initial_delay_sec': 30  # CRITICAL DEFECT: Shorter than JVM startup!\n"
                               '}\n'
                               'jvm_startup_sec = 85\n'
                               "print('[PREFLIGHT] Auditing MIG autohealing parameters:')\n"
                               'for k, v in hc_params.items():\n'
                               "    print(f'  • {k}: {v}')\n"
                               "if hc_params['autohealing_initial_delay_sec'] < jvm_startup_sec:\n"
                               "    print('[CRITICAL DEFECT DETECTED] Initial delay < JVM startup time -> Guaranteed "
                               "thrashing loop!')\n"
                               'EOF\n'
                               'python3 audit_health_checks.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Terraform Template Readiness\n'
                               'Verify Terraform infrastructure template syntax for Compute Engine MIG policies:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_mig_prereqs.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Verifying MIG template tooling..."\n'
                               'python3 -c "import json; print(\'[PASS] JSON parser verified.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_mig_prereqs.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Production MIG Autohealing Manifest\n'
                               'Author a declarative Terraform configuration establishing calibrated autohealing '
                               'policies with separated LB and autohealing health checks:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > mig_autohealing.tf\n"
                               'resource "google_compute_health_check" "mig_autohealing_hc" {\n'
                               '  name                = "api-autohealing-healthcheck"\n'
                               '  check_interval_sec  = 15\n'
                               '  timeout_sec         = 5\n'
                               '  unhealthy_threshold = 3\n'
                               '  healthy_threshold   = 2\n'
                               '\n'
                               '  http_health_check {\n'
                               '    request_path = "/healthz/liveness"\n'
                               '    port         = 8080\n'
                               '  }\n'
                               '}\n'
                               '\n'
                               'resource "google_compute_region_instance_group_manager" "api_mig" {\n'
                               '  name   = "api-regional-mig"\n'
                               '  region = "us-central1"\n'
                               '\n'
                               '  version {\n'
                               '    instance_template = '
                               '"projects/prod-fleet/global/instanceTemplates/api-template-v2"\n'
                               '  }\n'
                               '\n'
                               '  auto_healing_policies {\n'
                               '    health_check      = google_compute_health_check.mig_autohealing_hc.id\n'
                               '    initial_delay_sec = 300 # 5 minutes: allows JVM compilation and warmup\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored mig_autohealing.tf with calibrated initial delay"\n'
                               '```',
                               '#### Stage 4: Execution & Boot Lifecycle Simulation\n'
                               'Author a simulation modeling instance startup time and verifying initial delay '
                               'protection:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_boot_lifecycle.py\n"
                               'def evaluate_autohealing(uptime_sec, initial_delay_sec=300, is_healthy=False):\n'
                               '    if uptime_sec < initial_delay_sec:\n'
                               "        return 'PROTECTED_GRACE_PERIOD', 'Autohealing suppressed during boot'\n"
                               '    if not is_healthy:\n'
                               "        return 'TRIGGER_RECREATE', 'Instance unhealthy past initial delay'\n"
                               "    return 'HEALTHY', 'Serving traffic normally'\n"
                               '\n'
                               "print('[SIMULATION] Testing instance boot lifecycle protection:')\n"
                               'for t in [30, 60, 90, 150, 310]:\n'
                               '    healthy = (t >= 90) # JVM ready at 90s\n'
                               '    status, desc = evaluate_autohealing(t, initial_delay_sec=300, is_healthy=healthy)\n'
                               "    print(f'  • Uptime {t:3d}s: [{status}] -> {desc}')\n"
                               'EOF\n'
                               'python3 simulate_boot_lifecycle.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Deadlock Chaos Injection\n'
                               'Simulate an unrecoverable process deadlock and verify that autohealing terminates and '
                               'replaces the instance:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_deadlock_recovery.py\n"
                               'from simulate_boot_lifecycle import evaluate_autohealing\n'
                               '\n'
                               '# Instance running for 600s becomes deadlocked (unhealthy)\n'
                               'status, desc = evaluate_autohealing(uptime_sec=600, initial_delay_sec=300, '
                               'is_healthy=False)\n'
                               "assert status == 'TRIGGER_RECREATE', 'Autohealing failed to trigger on deadlocked "
                               "instance'\n"
                               "print(f'[CHAOS TEST PASS] Autohealing correctly triggered recreation: {desc}')\n"
                               'EOF\n'
                               'python3 test_deadlock_recovery.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Autohealing Flap Alerting\n'
                               'Author a Cloud Monitoring Alert detecting excessive MIG instance recreation events:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_mig_thrashing.json\n"
                               '{\n'
                               '  "displayName": "CRITICAL: MIG Autohealing Thrash Detected",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "MIG instance recreation count > 10 in 5m",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": '
                               '"metric.type=\\"compute.googleapis.com/instance_group/recreate_instances\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 10.0,\n'
                               '        "duration": "300s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] MIG thrash alert authored in alert_mig_thrashing.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Initial Delay Guardrail Assertions\n'
                               'Execute automated test asserting initial delay adheres to enterprise minimums:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_mig_guardrails.py\n"
                               "with open('mig_autohealing.tf') as f:\n"
                               '    manifest = f.read()\n'
                               '\n'
                               "assert 'initial_delay_sec = 300' in manifest, 'Initial delay must be at least 300s'\n"
                               "assert 'unhealthy_threshold = 3' in manifest, 'Threshold must require at least 3 "
                               "consecutive failures'\n"
                               "print('[ASSERT PASS] MIG autohealing guardrails strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_mig_guardrails.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary test files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_mig_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 97 Topic 2 test scripts..."\n'
                               'rm -f audit_health_checks.py check_mig_prereqs.sh simulate_boot_lifecycle.py '
                               'test_deadlock_recovery.py assert_mig_guardrails.py\n'
                               'echo "[CLEANUP] Retaining production configs: mig_autohealing.tf, '
                               'alert_mig_thrashing.json"\n'
                               'echo "[CLEANUP PASS] MIG autohealing lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_mig_lab.sh\n'
                               '```'],
                     'verification': 'The shell script includes initial delay and shallow check paths, and the Python '
                                     'simulation verifies that only the dead instance transitions to DRAINING and '
                                     'RECREATING.',
                     'trouble': 'Ensure `initialDelaySec` is set to at least 2x the time it takes for an instance to '
                                'execute its startup script and open its listening port.',
                     'cleanup': 'Retain `setup_mig_autohealing.sh` as an exit evidence artifact.',
                     'accept': 'Completed MIG autohealing policy script and verified lifecycle simulation. File: '
                               '`day-097-topic-02-mig-autohealing.md`.',
                     'file': 'day-097-topic-02-mig-autohealing.md'}},
            {'key': 'topic-03',
             'title': 'Zonal Failure Tabletop Modeling, Distributed Traces, and Simulation Boundaries',
             'overview': 'While single-instance crashes are readily tested in pre-production, physically taking down '
                         'an entire Google Cloud availability zone (which houses tens of thousands of customer '
                         'workloads across dedicated power substations and fiber backbones) cannot be enacted on live '
                         'cloud infrastructure. To rigorously evaluate multi-zone resilience without violating cloud '
                         'provider constraints, architects combine **tabletop partition analysis** with **synthetic '
                         'distributed trace modeling**. By analyzing cross-zone latency traces, capacity headrooms, '
                         'and stateful failover dependencies, engineers calculate precise Mean Time to Recovery (MTTR) '
                         'while explicitly documenting simulation boundaries.',
             'preview': 'An architect assumes that losing Zone B will seamlessly shift traffic to Zones A and C, but '
                        'fails to calculate that remaining zones lack sufficient CPU quota. Trace modeling and '
                        'tabletop capacity analysis uncover quota deficits before real disasters strike.',
             'technical': '### 1. Zonal Partition Modeling Methodology\n'
                          '- **The Zonal Independence Model:** Google Cloud zones within a region possess independent '
                          'physical infrastructure (chilled water plants, backup generators, network core switches) '
                          'interconnected via ultra-low-latency redundant fiber (<1ms RTT).\n'
                          '- **Tabletop Failure Scenario:** We model the complete loss of `us-central1-b`:\n'
                          '  1. Ingress traffic instantly fails over at the Cloud Load Balancer (Anycast MAGLEV tier '
                          'routes solely to backends in zones A and C).\n'
                          '  2. Stateful storage: Cloud SQL or Regional Persistent Disk initiates automatic failover '
                          'to the synchronous secondary zone (`us-central1-a`).\n'
                          '  3. Compute capacity: Total available compute drops by 33.3%. Remaining zones must absorb '
                          'the 50% traffic increase ($1.0 / 0.667 = 1.5$).\n'
                          '\n'
                          '### 2. Trace-Based Cross-Zone Latency Synthesis\n'
                          '- In normal operation, inter-zonal RPC spans show consistent $0.6\\text{ms} - '
                          '1.2\\text{ms}$ latency.\n'
                          '- Under zonal partition simulation, traces reveal the exact timeline of request timeouts, '
                          'retry storms, and eventual circuit-breaker ejection of failing zonal endpoints.\n'
                          '\n'
                          '### 3. Explicit Simulation Limits and Reality Boundaries\n'
                          '- Responsible architectural modeling requires clearly stating what a tabletop or trace '
                          'simulation **does not prove**:\n'
                          '  - **Simulation Limit 1:** Tabletop models cannot prove that Google Cloud has sufficient '
                          'spot/on-demand VM buffer capacity in neighboring zones during a widespread regional '
                          'disaster unless guaranteed by Committed Use Reservations with Specific Affinity.\n'
                          '  - **Simulation Limit 2:** Synthetic traces do not reproduce unpredictable cross-zone '
                          'fiber carrier packet reordering or BGP convergence flaps.',
             'questions': ['Why is a tabletop exercise and synthetic trace model appropriate for zonal disaster '
                           'recovery analysis rather than physical fault injection?',
                           'What capacity deficit calculation must be performed to guarantee that surviving zones can '
                           'absorb full customer traffic during a single-zone loss?',
                           'What critical operational assumptions remain unproven until tested with live traffic or '
                           'reserved compute capacity?'],
             'reference': 'https://docs.cloud.google.com/architecture/disaster-recovery-planning-guide',
             'reference_label': 'Google Cloud Architecture: Disaster recovery planning guide and zonal failure '
                                'modeling',
             'scenario': {'symptom': 'During a tabletop disaster simulation modeling the loss of zone `us-central1-a`, '
                                     'the capacity calculator revealed that remaining zones B and C would breach the '
                                     "project's regional `N2_CPUS` quota by 400 cores, preventing GKE autoscalers from "
                                     'spinning up replacement pods.',
                          'constraints': 'Must establish an accurate capacity model guaranteeing surviving zones have '
                                         'verified compute headroom and quota reservations.',
                          'evidence': 'Distributed trace waterfall during simulated us-central1-a storage '
                                      'degradation:\n'
                                      '\n'
                                      '```text\n'
                                      'TraceID: 4bf92f3577b34da6a3ce929d0e0e4736\n'
                                      'Span 1: [ALB] Ingress GET /api/order/9182            [200 OK] 3420ms\n'
                                      '  Span 2: [Zone B] AppService.getOrder               [200 OK] 3418ms\n'
                                      '    Span 3: [Zone B] CacheClient.get                 [MISS]   2ms\n'
                                      '    Span 4: [Zone A] PrimaryDB.readLock              [TIMEOUT] 3000ms\n'
                                      '    Span 5: [Zone B] FallbackDB.read                 [200 OK] 414ms\n'
                                      '```\n'
                                      '\n'
                                      'Tabletop finding: Cross-zone synchronous lock in Span 4 blocked the request for '
                                      '3000ms before falling back, destroying 99% of regional capacity during a '
                                      'single-zone failure.',
                          'diagnostic_steps': ['Audit Compute Engine regional quota usage via `gcloud compute '
                                               'project-info describe`.',
                                               'Calculate per-zone capacity headroom: $\\text{Surviving Capacity} = '
                                               '\\text{Total Capacity} \\times \\frac{N-1}{N}$.',
                                               'Review GKE cluster autoscaler minimum and maximum node boundaries per '
                                               'zone.'],
                          'root': 'Hidden quota constraint: the architectural plan relied on autoscaling to replace '
                                  'lost zonal nodes without securing sufficient regional vCPU quota headroom.',
                          'fix': 'Submit an immediate quota increase request for regional `N2_CPUS` to 3,500 cores. '
                                 'Purchase Regional Compute Reservations in zones B and C to guarantee physical '
                                 'hardware availability.',
                          'verify': 'Rerun the tabletop capacity simulation; confirm that total required peak surge '
                                    '(2,400 cores) is fully covered by reserved capacity and quota.',
                          'residual': 'Reservations incur continuous compute charges even when idle; FinOps must '
                                      'balance reservation costs against the business downtime risk.',
                          'diagram': ('Zone A storage degrades unexpectedly',
                                      'App in Zone B waits 3s for Zone A lock',
                                      'Regional thread pools deplete -> 504 outage',
                                      'Implement asynchronous circuit breaker with 200ms timeout',
                                      'Zone A isolated in 200ms; Zone B serves traffic')},
             'lab': {'name': 'Zonal Partition Tabletop Analysis, Trace Modeling, and Capacity Revision',
                     'goal': 'Author a comprehensive tabletop zonal outage model, simulate cross-zone latency '
                             'degradation via Python trace modeling, and revise capacity requirements.',
                     'expected': 'An executable Python trace simulator modeling zonal timeouts, a mathematical '
                                 'capacity recovery model, and an explicit simulation limitation sheet.',
                     'mode': 'tabletop analysis & Python execution',
                     'prereq': 'Understanding of multi-zone GKE topology and Compute Engine quotas.',
                     'preflight': 'Ensure Python 3 standard library is present; no external packages needed.',
                     'steps': ['#### Stage 1: Pre-Flight Distributed Trace & Dependency Mapping\n'
                               'Catalog multi-zone service dependencies to identify hidden synchronous cross-zone '
                               'calls:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > map_zonal_dependencies.py\n"
                               'dependencies = [\n'
                               "    {'caller_zone': 'us-central1-b', 'callee_zone': 'us-central1-b', 'mode': 'ASYNC', "
                               "'timeout_ms': 50},\n"
                               "    {'caller_zone': 'us-central1-b', 'callee_zone': 'us-central1-a', 'mode': "
                               "'SYNC_LOCK', 'timeout_ms': 3000} # DANGEROUS\n"
                               ']\n'
                               "print('[PREFLIGHT] Analyzing cross-zone dependency matrix:')\n"
                               'for dep in dependencies:\n'
                               "    status = 'RISK: SYNCHRONOUS CROSS-ZONE LOCK' if dep['timeout_ms'] > 500 else "
                               "'ISOLATED'\n"
                               '    print(f\'  • {dep["caller_zone"]} -> {dep["callee_zone"]} ({dep["mode"]}, '
                               '{dep["timeout_ms"]}ms) [{status}]\')\n'
                               'EOF\n'
                               'python3 map_zonal_dependencies.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Trace Schema Inspection\n'
                               'Verify JSON schema definition for Cloud Trace OpenTelemetry waterfall spans:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_trace_schema.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Verifying trace schema requirements..."\n'
                               'python3 -c "import json; print(\'[PASS] OpenTelemetry trace schema parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_trace_schema.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Tabletop Zonal Failure Simulator\n'
                               'Author a Python tabletop simulation engine modeling request flow and circuit breaker '
                               'tripping during zonal loss:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > tabletop_zonal_simulator.py\n"
                               'class ZonalCircuitBreaker:\n'
                               '    def __init__(self, failure_threshold=3, reset_timeout=30):\n'
                               '        self.failure_threshold = failure_threshold\n'
                               '        self.failure_count = 0\n'
                               "        self.state = 'CLOSED' # CLOSED, OPEN, HALF-OPEN\n"
                               '\n'
                               '    def call_zone(self, zone_healthy):\n'
                               "        if self.state == 'OPEN':\n"
                               "            return 'CIRCUIT_OPEN_FAST_FALLBACK', 2 # 2ms fallback\n"
                               '        if not zone_healthy:\n'
                               '            self.failure_count += 1\n'
                               '            if self.failure_count >= self.failure_threshold:\n'
                               "                self.state = 'OPEN'\n"
                               "            return 'TIMEOUT_DEGRADATION', 200 # 200ms timeout\n"
                               "        return 'SUCCESS_OK', 20\n"
                               '\n'
                               "if __name__ == '__main__':\n"
                               '    cb = ZonalCircuitBreaker()\n'
                               "    print('[TABLETOP] Simulating 10 requests during Zone A failure:')\n"
                               '    for i in range(10):\n'
                               '        res, lat = cb.call_zone(zone_healthy=False)\n'
                               "        print(f'  • Request {i+1}: {res} ({lat}ms) [Breaker State: {cb.state}]')\n"
                               'EOF\n'
                               'python3 tabletop_zonal_simulator.py\n'
                               '```',
                               '#### Stage 4: Execution & Trace Waterfall JSON Synthesis\n'
                               'Synthesize a mock Cloud Trace JSON payload representing an isolated zonal failure:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > generate_trace_payload.py\n"
                               'import json\n'
                               '\n'
                               'trace_payload = {\n'
                               '    "traceId": "projects/prod-observability/traces/7f19a0812b3c4d5e",\n'
                               '    "spans": [\n'
                               '        {"spanId": "1001", "name": "HTTP Ingress /api/v1/orders", "startTime": "0ms", '
                               '"endTime": "24ms"},\n'
                               '        {"spanId": "1002", "parentSpanId": "1001", "name": "Zone-B-LocalService", '
                               '"startTime": "2ms", "endTime": "22ms"},\n'
                               '        {"spanId": "1003", "parentSpanId": "1002", "name": "CircuitBreaker.ZoneA", '
                               '"startTime": "3ms", "endTime": "4ms", "status": {"code": 0, "message": '
                               '"FastFallback"}}\n'
                               '    ]\n'
                               '}\n'
                               '\n'
                               "with open('simulated_trace.json', 'w') as f:\n"
                               '    json.dump(trace_payload, f, indent=2)\n'
                               "print('[TRACE GENERATED] simulated_trace.json contains fast-fallback span "
                               "execution.')\n"
                               'EOF\n'
                               'python3 generate_trace_payload.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Tabletop Limit Boundary Assertion\n'
                               'Assert that system capacity stays above 66% during complete loss of one of three '
                               'zones:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_tabletop_limits.py\n"
                               'total_zones = 3\n'
                               'lost_zones = 1\n'
                               'surviving_capacity = (total_zones - lost_zones) / total_zones\n'
                               'min_required_capacity = 0.65\n'
                               '\n'
                               "assert surviving_capacity >= min_required_capacity, 'Surviving capacity below N+1 "
                               "minimum'\n"
                               "print(f'[PASS] Zonal failure limit strictly preserved: {surviving_capacity*100:.1f}% "
                               "capacity maintained.')\n"
                               'EOF\n'
                               'python3 assert_tabletop_limits.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Zonal Latency Dashboard Manifest\n'
                               'Author a Cloud Monitoring Dashboard monitoring cross-zone latency percentiles:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > zonal_latency_dashboard.json\n"
                               '{\n'
                               '  "displayName": "Cross-Zone Latency Matrix & Failure Bounds",\n'
                               '  "gridLayout": {\n'
                               '    "widgets": [\n'
                               '      {\n'
                               '        "title": "Inter-Zone Latency by Destination Zone",\n'
                               '        "xyChart": {\n'
                               '          "dataSets": [\n'
                               '            {"timeSeriesQuery": {"timeSeriesFilter": {"filter": '
                               '"metric.type=\\"custom.googleapis.com/cross_zone_latency\\""}}}\n'
                               '          ]\n'
                               '        }\n'
                               '      }\n'
                               '    ]\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[DASHBOARD] Authored zonal_latency_dashboard.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Circuit Breaker State Assertions\n'
                               'Execute automated test validating circuit breaker state transitions:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_breaker_transitions.py\n"
                               'from tabletop_zonal_simulator import ZonalCircuitBreaker\n'
                               '\n'
                               'cb = ZonalCircuitBreaker(failure_threshold=2)\n'
                               "assert cb.state == 'CLOSED'\n"
                               'cb.call_zone(False)\n'
                               "assert cb.state == 'CLOSED'\n"
                               'cb.call_zone(False)\n'
                               "assert cb.state == 'OPEN'\n"
                               'res, lat = cb.call_zone(False)\n'
                               "assert res == 'CIRCUIT_OPEN_FAST_FALLBACK'\n"
                               "assert lat < 5, 'Fallback latency exceeded 5ms limit'\n"
                               "print('[ASSERT PASS] Zonal circuit breaker state transitions strictly verified.')\n"
                               'EOF\n'
                               'python3 verify_breaker_transitions.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary simulation files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_zonal_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 97 Topic 3 test scripts..."\n'
                               'rm -f map_zonal_dependencies.py check_trace_schema.sh tabletop_zonal_simulator.py '
                               'generate_trace_payload.py assert_tabletop_limits.py verify_breaker_transitions.py\n'
                               'echo "[CLEANUP] Retaining evidence artifacts: simulated_trace.json, '
                               'zonal_latency_dashboard.json"\n'
                               'echo "[CLEANUP PASS] Zonal failure tabletop lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_zonal_lab.sh\n'
                               '```'],
                     'verification': 'The Python script models cross-zone deadline timeouts and the capacity report '
                                     'provides quantitative before/during/after data and explicit simulation '
                                     'boundaries.',
                     'trouble': 'Ensure capacity equations account for integer node rounding when calculating per-zone '
                                'minimum replica counts.',
                     'cleanup': 'Retain `simulate_zonal_trace.py` and `day-097-topic-03-capacity-model.md` as exit '
                                'evidence artifacts.',
                     'accept': 'Completed zonal trace simulator and verified capacity/recovery model. File: '
                               '`day-097-topic-03-capacity-model.md`.',
                     'file': 'day-097-topic-03-capacity-model.md'}}],
 'part3_intro': 'The following field cases analyze severe architectural regressions and failure domain oversights: a '
                'subtle 42ms P99 latency degradation that bypassed traditional mean-latency alerting and degraded '
                'database connection pools over two weeks, an aggressive Managed Instance Group (MIG) autohealing '
                'policy whose misconfigured initial delay triggered an infinite boot-and-destroy cascade across 200 '
                'instances, and a tabletop simulation blind spot where an unmodeled cross-zone synchronous database '
                'disk lock caused a zonal storage failure to paralyze the entire region. Each case presents verbatim '
                'log transcripts, stack traces, diagnostic commands, root cause analysis, defensible remediations, and '
                'dual-lane failed/corrected flow diagrams.',
 'part4_intro': 'These hands-on exercises implement the comprehensive 8-stage operational engineering lifecycle for '
                'Day 97. Engineers construct statistical baseline models comparing latency distributions using '
                'non-parametric Mann-Whitney U tests, author production Compute Engine Managed Instance Group '
                'autohealing policies with calibrated initial delays and load shedding, and execute tabletop '
                'distributed trace simulations modeling unavailable zonal failure boundaries and system capacity '
                'limits.'}
