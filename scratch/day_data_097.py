"""day_data_097.py — Exhaustive architecture data specification for Day 97.

Covers Recovery and Overload Experiments:
1. Performance baselines and statistical regression analysis: establishing confidence intervals, P50/P95/P99 latency distribution comparisons, automated regression gates.
2. Bounded service failure execution: Compute Engine Managed Instance Group (MIG) autohealing, application-level health checks, initial delay, unhealthy thresholds, and instance recreation mechanics.
3. Zonal failure tabletop and trace-based modeling: multi-zone cross-partition analysis, MTTR calculations, identifying capacity deficit risks, and labeling tabletop simulation boundaries.
Follows PAGE_AUTHORING_CONTRACT.md with hands-on, verifiable exercises.
"""

DAY_NUM = 97

DATA = {
    "day": 97,
    "part1_intro": (
        "Day 97 moves from experiment design to empirical execution: applying bounded service failure and overload conditions against "
        "a target workload, recording before/during/after telemetry, and revising architectural capacity and recovery models. Resilience is not "
        "a binary state; it is a measurable curve of degradation and recovery. Today's curriculum evaluates performance baselines using "
        "statistical regression analysis, executes automated MIG autohealing fault injection to test instance recreation and traffic draining, "
        "and synthesizes distributed trace data to model multi-zonal failure boundaries and document explicit tabletop simulation limits."
    ),
    "exit_summary": (
        "Executed an empirical Recovery and Overload Experiment: captured before/during/after statistical performance baselines across P50/P95/P99 "
        "latency percentiles; executed a bounded Compute Engine MIG autohealing drill proving zero-downtime instance recreation; authored a "
        "zonal outage trace simulation model with a revised capacity recovery plan and explicit simulation limitation boundaries."
    ),
    "part2_intro": (
        "Empirical resilience validation requires establishing a pristine pre-test baseline, introducing an isolated failure state, "
        "measuring degradation metrics, and recording the time-to-recovery (TTR) curve. The sections below analyze performance baseline math, "
        "MIG autohealing mechanics, and trace-based zonal partition modeling."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Experiment Phase / Component</th>
      <th>GCP Mechanism / Metric</th>
      <th>Observed Telemetry Signal</th>
      <th>Acceptance Criteria &amp; Target</th>
      <th>Simulation Boundary / Limitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Phase 1: Baseline Steady State</strong></td>
      <td>Cloud Monitoring `https/request_latencies`</td>
      <td>P50: 38ms, P95: 110ms, P99: 185ms; Error rate: 0.00%</td>
      <td>P99 latency &lt; 250ms under 5,000 req/sec steady load</td>
      <td>Does not reflect extreme holiday traffic concurrency spikes</td>
    </tr>
    <tr>
      <td><strong>Phase 2: Fault Injection (Autohealing)</strong></td>
      <td>Compute Engine MIG Autohealing Policy</td>
      <td>Health check fails; instance state changes to `RECREATING`</td>
      <td>In-flight TCP drain: 30s; Replacement VM active &lt; 90s</td>
      <td>Single-instance fault; does not test simultaneous multi-node rolling crash</td>
    </tr>
    <tr>
      <td><strong>Phase 3: Zonal Failure Modeling</strong></td>
      <td>Cloud Trace &amp; Cross-Zone VPC Flow Logs</td>
      <td>Cross-zone round-trip time jumps from 0.8ms to timeout (drop)</td>
      <td>Traffic rerouted to remaining 2 zones within 15 seconds</td>
      <td>Simulated via synthetic trace data; cloud provider-level fiber cut cannot be physically enacted</td>
    </tr>
    <tr>
      <td><strong>Phase 4: Post-Recovery State</strong></td>
      <td>Cloud Monitoring &amp; Log Analytics</td>
      <td>MIG target size restored (3/3 instances healthy); Latency P99: 190ms</td>
      <td>100% capacity restored; 0 persistent error log artifacts</td>
      <td>Warm-up cache effects: initial requests post-reboot incur slight JVM/JIT compilation latency</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Before / During / After Experiment Telemetry & Recovery Timeline",
        "desc": "Timeline graph showing steady-state baseline, fault injection impact, MIG autohealing recreation, and post-experiment recovery verification.",
        "caption": "Figure 97.1: Telemetry degradation and autohealing recovery curve across the 4 experiment phases.",
        "nodes": [
            ("1. Baseline Phase", "P99: 185ms, 0% error"),
            ("2. Fault Injected", "Instance health check fails"),
            ("3. Autohealing Drain", "MIG recreates dead VM in 75s"),
            ("4. Restored Baseline", "P99: 190ms, capacity 100%"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Performance Baselines and Statistical Regression Analysis",
            "overview": (
                "Before conducting a resilience or load experiment, engineers must establish a mathematically rigorous performance baseline. "
                "A baseline is not a single average latency number; it is a probability distribution of response times, throughput rates, and resource "
                "utilizations captured over a statistically significant steady-state window. Automated regression analysis compares post-change or "
                "under-stress distributions against this baseline using non-parametric percentile gates (P95, P99), detecting performance degradation "
                "before it breaches user-facing Service Level Objectives."
            ),
            "preview": (
                "An engineering team reviews average response times and concludes an experiment caused no impact, missing that P99 latency doubled for 500 shoppers. "
                "Percentile distribution baselines isolate tail latency regressions that averages completely disguise."
            ),
            "technical": (
                "### 1. Statistical Baseline Methodology\n"
                "- **Sampling Duration:** Baseline capture requires a minimum 30-minute steady-state run at typical production operating concurrency "
                "to allow JVM JIT compilation, database buffer pool warming, and autoscaler stabilization.\n"
                "- **Why Arithmetic Averages Deceive:** In a sample of 10,000 requests, 9,900 requests completing in 10ms with 100 requests taking 5,000ms "
                "yields an average latency of only 59.9ms (which appears acceptable). However, the P99 is 5,000ms—meaning 1 out of every 100 users "
                "experiences an unacceptable 5-second freeze.\n\n"
                "### 2. Quantifying Regression Margins\n"
                "- **Acceptable Variance vs Regressions:** Normal network jitter and CPU scheduling variance introduce +/- 5% fluctuation. "
                "A **Performance Regression** is formally declared when:\n"
                "  1. $P95_{\\text{observed}} > 1.15 \\times P95_{\\text{baseline}}$ (15% degradation).\n"
                "  2. $P99_{\\text{observed}} > 1.25 \\times P99_{\\text{baseline}}$ (25% degradation).\n"
                "  3. Error rate exceeds baseline by $>0.1\\%$.\n\n"
                "### 3. Automated Metric Extraction with MQL\n"
                "- Using Google Cloud Monitoring Query Language (MQL), baseline extraction is automated across percentiles:\n"
                "  `fetch https_lb_rule | metric 'loadbalancing.googleapis.com/https/backend_latencies'`\n"
                "  `| group_by [resource.backend_target_name], 1m, percentile(99)`\n"
                "  `| every 1m`."
            ),
            "questions": [
                "Why must performance baselines be evaluated using percentile distributions (P50, P95, P99) rather than arithmetic averages?",
                "What minimum duration and conditions are required to establish an uncorrupted steady-state baseline in cloud environments?",
                "How does MQL percentile aggregation simplify automated regression detection in continuous deployment pipelines?",
            ],
            "reference": "https://docs.cloud.google.com/monitoring/mql/reference",
            "reference_label": "Google Cloud Monitoring: MQL percentile aggregations and statistical evaluation",
            "scenario": {
                "symptom": (
                    "Following a minor database library upgrade, customer support tickets regarding slow cart checkouts increased by 40%, "
                    "yet the CI/CD pipeline automated test suite reported 'Average Response Time = 62ms (PASSED)'."
                ),
                "constraints": (
                    "Must establish an automated statistical regression gate in the experiment pipeline that detects tail latency regressions."
                ),
                "evidence": (
                    "Cloud Monitoring latency histograms showed that while P50 remained at 35ms, P99 had spiked from 180ms to 2,800ms due to "
                    "un-pooled connection handshakes on 1% of transactions."
                ),
                "diagnostic_steps": [
                    "Compare Cloud Monitoring latency distribution heatmaps before and after the release.",
                    "Calculate P50, P90, P95, and P99 percentiles across both sample windows.",
                    "Audit CI/CD performance testing gates to verify metric evaluation formulas.",
                ],
                "root": (
                    "Flawed metric evaluation: relying on average response time hid a 15x tail latency degradation affecting 1% of all checkout customers."
                ),
                "fix": (
                    "Replace average response time assertions with strict percentile regression formulas (assert $P95 \\le 1.15 \\times \\text{baseline}$ "
                    "and $P99 \\le 1.25 \\times \\text{baseline}$). Deploy automated regression analysis scripts in staging."
                ),
                "verify": (
                    "Run automated regression script against the bad release; verify the script flags a P99 regression failure and halts promotion."
                ),
                "residual": (
                    "Percentile metrics require sufficient sample volume; evaluating P99 on fewer than 100 requests produces statistical noise."
                ),
                "diagram": (
                    "Library upgrade released",
                    "Average latency: 62ms (Pass)",
                    "P99 latency: 2,800ms (Unseen)",
                    "Percentile regression gate deployed",
                    "P99 spike flagged & release blocked"
                )
            },
            "lab": {
                "name": "Statistical Performance Baseline and Regression Analysis Engine",
                "goal": "Author an automated Python statistical analysis engine comparing baseline distributions with experimental degradation runs.",
                "expected": "An executable Python script calculating P50, P95, and P99 percentiles, detecting statistical regressions, and printing an evaluation report.",
                "mode": "local script execution",
                "prereq": "Understanding of percentiles and statistical distributions.",
                "preflight": "Ensure Python 3 standard library is present; no external packages needed.",
                "steps": [
                    "Author the automated statistical baseline and regression evaluation engine (`evaluate_regression.py`):\n\n```sh\ncat <<'EOF' > evaluate_regression.py\n# Statistical Performance Baseline & Regression Analysis Engine\nimport numpy as np\nimport json\n\ndef calculate_distribution_stats(samples):\n    return {\n        \"count\": len(samples),\n        \"mean_ms\": round(float(np.mean(samples)), 2),\n        \"p50_ms\": round(float(np.percentile(samples, 50)), 2),\n        \"p95_ms\": round(float(np.percentile(samples, 95)), 2),\n        \"p99_ms\": round(float(np.percentile(samples, 99)), 2),\n        \"max_ms\": round(float(np.max(samples)), 2)\n    }\n\ndef evaluate_performance_regression(baseline_samples, candidate_samples):\n    base_stats = calculate_distribution_stats(baseline_samples)\n    cand_stats = calculate_distribution_stats(candidate_samples)\n    \n    regressions = []\n    \n    # Regression Gate 1: P95 must not degrade by >15%\n    p95_threshold = base_stats[\"p95_ms\"] * 1.15\n    if cand_stats[\"p95_ms\"] > p95_threshold:\n        regressions.append(f\"P95 REGRESSION: Observed {cand_stats['p95_ms']}ms exceeds threshold {p95_threshold:.1f}ms\")\n        \n    # Regression Gate 2: P99 must not degrade by >25%\n    p99_threshold = base_stats[\"p99_ms\"] * 1.25\n    if cand_stats[\"p99_ms\"] > p99_threshold:\n        regressions.append(f\"P99 REGRESSION: Observed {cand_stats['p99_ms']}ms exceeds threshold {p99_threshold:.1f}ms\")\n        \n    passed = (len(regressions) == 0)\n    return passed, base_stats, cand_stats, regressions\n\n# Generate Synthetic Telemetry Samples (1000 requests each)\nnp.random.seed(42)\n# Baseline: Normal distribution centered around 40ms, tail up to 180ms\nbaseline = np.random.normal(loc=40.0, scale=12.0, size=990).tolist()\nbaseline.extend([140.0, 155.0, 162.0, 175.0, 180.0, 185.0, 190.0, 195.0, 205.0, 210.0])\n\n# Candidate A: Healthy run (minor variance)\ncandidate_healthy = np.random.normal(loc=41.0, scale=12.5, size=990).tolist()\ncandidate_healthy.extend([142.0, 158.0, 160.0, 172.0, 182.0, 188.0, 192.0, 198.0, 202.0, 212.0])\n\n# Candidate B: Regressed run (P99 tail explosion, mean barely moves)\ncandidate_regressed = np.random.normal(loc=42.0, scale=12.0, size=980).tolist()\ncandidate_regressed.extend([150.0] * 10)\ncandidate_regressed.extend([1800.0, 2100.0, 2400.0, 2800.0, 3100.0, 3400.0, 3600.0, 3900.0, 4200.0, 4500.0])\n\nprint(\"=== TEST CASE 1: HEALTHY CANDIDATE ===\")\npass_a, base_s, cand_a_s, reg_a = evaluate_performance_regression(baseline, candidate_healthy)\nprint(f\"Result: {'PASSED' if pass_a else 'FAILED'}\")\nprint(\"Stats:\", json.dumps(cand_a_s, indent=2))\nassert pass_a, \"Candidate A should have passed regression evaluation!\"\n\nprint(\"\n=== TEST CASE 2: REGRESSED CANDIDATE (Tail Spike) ===\")\npass_b, _, cand_b_s, reg_b = evaluate_performance_regression(baseline, candidate_regressed)\nprint(f\"Result: {'PASSED' if pass_b else 'FAILED'}\")\nprint(\"Detected Regressions:\", reg_b)\nprint(f\"Mean moved from {base_s['mean_ms']}ms to {cand_b_s['mean_ms']}ms (only slight change)\")\nprint(f\"P99 moved from {base_s['p99_ms']}ms to {cand_b_s['p99_ms']}ms (CATASTROPHIC!)\")\nassert not pass_b, \"Candidate B failed to detect catastrophic P99 regression!\"\n\nprint(\"\nPASS: Statistical baseline and regression engine mathematically verified!\")\nEOF\npython3 evaluate_regression.py\n```",
                    "Review all output artifacts and confirm that the Python statistical engine runs cleanly and correctly rejects the regressed distribution."
                ],
                "verification": "The Python regression engine accurately calculates percentiles and rejects candidate runs exceeding the 25% P99 tolerance threshold.",
                "trouble": "Ensure `numpy` is installed or fallback to pure Python standard library `statistics` module if numpy is unavailable.",
                "cleanup": "Retain `evaluate_regression.py` as an exit evidence artifact.",
                "accept": "Completed statistical baseline script and verified regression engine. File: `day-097-topic-01-baseline-regression.md`.",
                "file": "day-097-topic-01-baseline-regression.md"
            }
        },
        {
            "key": "topic-02",
            "title": "Bounded Service Failure: MIG Autohealing and Controlled Degradation",
            "overview": (
                "A Managed Instance Group (MIG) with an autohealing policy automatically monitors instance health using application-level health checks "
                "and recreates failing or dead virtual machines without manual intervention. However, misconfigured autohealing policies can cause "
                "'autohealing storms'—where healthy instances experiencing transient load spikes are prematurely declared unhealthy and rebooted "
                "simultaneously, wiping out remaining cluster capacity. Properly tuning initial delay, check interval, and unhealthy thresholds "
                "guarantees that autohealing heals genuine crashes while absorbing temporary overload."
            ),
            "preview": (
                "A database connection hiccup causes an app health check to fail once, prompting the MIG to terminate and recreate all 10 frontend VMs at once. "
                "Configuring autohealing initial delays and consecutive failure thresholds ensures resilience without destructive mass reboots."
            ),
            "technical": (
                "### 1. MIG Autohealing Architecture and Health Checks\n"
                "- **Application Health Check:** Distinct from Load Balancing health checks. While Load Balancing health checks decide whether to route "
                "traffic to an instance, the **Autohealing Health Check** decides whether to **delete and recreate** the instance.\n"
                "- **Initial Delay (Grace Period):** Defines how long the MIG must wait after an instance boots before checking its health check "
                "(e.g. `initialDelaySec: 120`). If the initial delay is shorter than the application bootstrap and JIT warmup time, the MIG enters an "
                "infinite crash-recreate loop.\n\n"
                "### 2. Autohealing Timing Parameters\n"
                "- `checkIntervalSec`: Frequency of probes (e.g. 5 seconds).\n"
                "- `timeoutSec`: Max wait time for response before counting as failure (e.g. 3 seconds).\n"
                "- `unhealthyThreshold`: Number of consecutive failures required before recreation is triggered (e.g. 3 consecutive failures = 15s).\n"
                "- `healthyThreshold`: Number of consecutive successes required to return to healthy status (e.g. 2 consecutive successes).\n\n"
                "### 3. Graceful Draining and Recreation Mechanics\n"
                "- When an instance is marked unhealthy, the MIG notifies the backend service to initiate **Connection Draining** (e.g. 30 seconds).\n"
                "- Existing TCP connections are allowed to terminate gracefully while new requests are routed exclusively to healthy instances.\n"
                "- After the draining timeout elapses, the MIG sends ACPI shutdown, deletes the ephemeral root disk, and provisions a fresh VM from the instance template."
            ),
            "questions": [
                "What is the critical architectural difference between a Load Balancer health check and a MIG Autohealing health check?",
                "What failure mode occurs if the autohealing `initialDelaySec` is configured shorter than application startup time?",
                "How does connection draining protect in-flight transactions when an unhealthy instance is scheduled for autohealing recreation?",
            ],
            "reference": "https://docs.cloud.google.com/compute/docs/instance-groups/autohealing-instances-in-migs",
            "reference_label": "Google Compute Engine: Setting up and configuring autohealing in Managed Instance Groups",
            "scenario": {
                "symptom": (
                    "During a minor traffic surge, all 8 instances in Brightloaf's regional MIG were rebooted simultaneously by the autohealing system, "
                    "causing a complete 4-minute service outage that dropped all live customer shopping carts."
                ),
                "constraints": (
                    "Must configure autohealing so that localized instance crashes are repaired within 90 seconds while transient overload never triggers mass reboots."
                ),
                "evidence": (
                    "Cloud Audit Logs showed `compute.instances.recreate` called on all 8 instances within 10 seconds of each other. The autohealing health check "
                    "was configured with `unhealthyThreshold = 1` and `checkIntervalSec = 2s` probing the heavy database-query endpoint `/healthz/deep`."
                ),
                "diagnostic_steps": [
                    "Inspect MIG autohealing policy via `gcloud compute instance-groups managed describe`.",
                    "Review health check configuration parameters and probe path.",
                    "Examine Compute Engine system event logs to trace recreation timestamps.",
                ],
                "root": (
                    "Overly aggressive autohealing thresholds: querying a deep database endpoint with an unhealthy threshold of 1 meant a momentary "
                    "database queue delay caused all healthy instances to fail their probe simultaneously and get destroyed."
                ),
                "fix": (
                    "Separate health check concerns: point autohealing to a lightweight shallow endpoint (`/healthz/shallow`) that verifies only local "
                    "process liveness. Increase `unhealthyThreshold` to 3 and configure an `initialDelaySec` of 120 seconds."
                ),
                "verify": (
                    "Simulate localized process failure by terminating the application process on one VM; verify that only that single VM is recreated "
                    "after 15 seconds while the other 7 instances continue serving traffic without interruption."
                ),
                "residual": (
                    "A shallow health check does not detect backend database disconnections; database dependency failures must be handled via circuit breakers, not VM recreation."
                ),
                "diagram": (
                    "Transient DB spike delays probe",
                    "Aggressive threshold (1 fail) trips",
                    "MIG destroys all 8 VMs simultaneously",
                    "Shallow /healthz & 3-failure threshold applied",
                    "Only genuine dead VMs recreated; 0 false reboots"
                )
            },
            "lab": {
                "name": "Compute Engine MIG Autohealing Fault Injection and Recreation Drill",
                "goal": "Author a production MIG autohealing policy specification and simulate controlled instance failure and automated recreation.",
                "expected": "A validated gcloud autohealing deployment script, an executable Python state-machine simulator, and a recovery log artifact.",
                "mode": "tabletop analysis & shell synthesis",
                "prereq": "Understanding of Compute Engine Managed Instance Groups and health checks.",
                "preflight": "Review gcloud compute health-checks and instance-groups CLI commands.",
                "steps": [
                    "Author the production shell script deploying a resilient MIG autohealing policy (`setup_mig_autohealing.sh`):\n\n```sh\ncat <<'EOF' > setup_mig_autohealing.sh\n#!/usr/bin/env bash\nset -euo pipefail\n\n# Enterprise Resilient MIG Autohealing Configuration\nREGION=\"us-central1\"\nHEALTH_CHECK_NAME=\"hc-orders-autoheal-shallow\"\nMIG_NAME=\"mig-orders-api-prod\"\n\necho \"=== 1. Creating Lightweight Shallow Autohealing Health Check ===\"\ncat <<COMMAND\ngcloud compute health-checks create http \"$HEALTH_CHECK_NAME\" \\\n    --region=\"$REGION\" \\\n    --port=8080 \\\n    --request-path=\"/healthz/shallow\" \\\n    --check-interval=5s \\\n    --timeout=3s \\\n    --unhealthy-threshold=3 \\\n    --healthy-threshold=2 \\\n    --description=\"Lightweight shallow process liveness check for MIG autohealing\"\nCOMMAND\n\necho \"=== 2. Attaching Autohealing Policy to Regional MIG ===\"\ncat <<COMMAND\ngcloud compute instance-groups managed set-autohealing \"$MIG_NAME\" \\\n    --region=\"$REGION\" \\\n    --http-health-check=\"$HEALTH_CHECK_NAME\" \\\n    --initial-delay=120s\nCOMMAND\n\necho \"=== 3. Fault Injection Command (Simulate Dead Process on Target VM) ===\"\ncat <<COMMAND\n# Kill process inside target VM to trigger bounded recreation\ngcloud compute ssh vm-orders-prod-01 --zone=\"${REGION}-a\" --command=\"sudo pkill -9 -f app_server\"\nCOMMAND\nEOF\nchmod +x setup_mig_autohealing.sh\n./setup_mig_autohealing.sh\n```",
                    "Author an automated Python state machine simulating MIG autohealing probe evaluation, connection draining, and VM recreation:\n\n```sh\ncat <<'EOF' > simulate_autohealing_lifecycle.py\n# State Machine Simulation of MIG Autohealing Lifecycle\n\nclass VMInstance:\n    def __init__(self, name):\n        self.name = name\n        self.state = \"RUNNING\"\n        self.process_alive = True\n        self.consecutive_failures = 0\n        self.draining_timer = 0\n\ninstances = [VMInstance(f\"instance-{i}\") for i in range(1, 4)]\n\n# Fault Injection: Kill process on instance-2\ninstances[1].process_alive = False\nprint(\"FAULT INJECTED: Process terminated on instance-2.\n\")\n\nprint(\"Time (s) | Instance 1 | Instance 2 | Instance 3 | Event Notes\")\nprint(\"------------------------------------------------------------------\")\n\nrecreated = False\nfor t in range(5, 75, 5):\n    notes = []\n    for vm in instances:\n        if vm.state == \"RUNNING\":\n            if not vm.process_alive:\n                vm.consecutive_failures += 1\n                if vm.consecutive_failures >= 3:\n                    vm.state = \"DRAINING\"\n                    vm.draining_timer = 15 # 15s draining\n                    notes.append(f\"{vm.name} marked UNHEALTHY -> DRAINING\")\n            else:\n                vm.consecutive_failures = 0\n        elif vm.state == \"DRAINING\":\n            vm.draining_timer -= 5\n            if vm.draining_timer <= 0:\n                vm.state = \"RECREATING\"\n                notes.append(f\"{vm.name} drained -> RECREATING\")\n        elif vm.state == \"RECREATING\":\n            # Recreate completes: process restored\n            vm.state = \"RUNNING\"\n            vm.process_alive = True\n            vm.consecutive_failures = 0\n            recreated = True\n            notes.append(f\"{vm.name} fresh boot -> HEALTHY\")\n            \n    note_str = \"; \".join(notes) if notes else \"Serving steady-state traffic\"\n    print(f\"{t:8d} | {instances[0].state:10s} | {instances[1].state:10s} | {instances[2].state:10s} | {note_str}\")\n\nassert recreated, \"Autohealing simulation failed: Instance was not recreated!\"\nassert instances[1].state == \"RUNNING\" and instances[1].process_alive, \"Instance 2 not restored!\"\nprint(\"\nPASS: MIG autohealing state machine and bounded recreation verified successfully.\")\nEOF\npython3 simulate_autohealing_lifecycle.py\n```",
                    "Review all output artifacts and confirm that the shell script and Python autohealing state-machine simulation pass execution assertions."
                ],
                "verification": "The shell script includes initial delay and shallow check paths, and the Python simulation verifies that only the dead instance transitions to DRAINING and RECREATING.",
                "trouble": "Ensure `initialDelaySec` is set to at least 2x the time it takes for an instance to execute its startup script and open its listening port.",
                "cleanup": "Retain `setup_mig_autohealing.sh` as an exit evidence artifact.",
                "accept": "Completed MIG autohealing policy script and verified lifecycle simulation. File: `day-097-topic-02-mig-autohealing.md`.",
                "file": "day-097-topic-02-mig-autohealing.md"
            }
        },
        {
            "key": "topic-03",
            "title": "Zonal Failure Tabletop Modeling, Distributed Traces, and Simulation Boundaries",
            "overview": (
                "While single-instance crashes are readily tested in pre-production, physically taking down an entire Google Cloud availability zone "
                "(which houses tens of thousands of customer workloads across dedicated power substations and fiber backbones) cannot be enacted "
                "on live cloud infrastructure. To rigorously evaluate multi-zone resilience without violating cloud provider constraints, architects "
                "combine **tabletop partition analysis** with **synthetic distributed trace modeling**. By analyzing cross-zone latency traces, "
                "capacity headrooms, and stateful failover dependencies, engineers calculate precise Mean Time to Recovery (MTTR) while explicitly "
                "documenting simulation boundaries."
            ),
            "preview": (
                "An architect assumes that losing Zone B will seamlessly shift traffic to Zones A and C, but fails to calculate that remaining zones lack sufficient CPU quota. "
                "Trace modeling and tabletop capacity analysis uncover quota deficits before real disasters strike."
            ),
            "technical": (
                "### 1. Zonal Partition Modeling Methodology\n"
                "- **The Zonal Independence Model:** Google Cloud zones within a region possess independent physical infrastructure (chilled water plants, "
                "backup generators, network core switches) interconnected via ultra-low-latency redundant fiber (<1ms RTT).\n"
                "- **Tabletop Failure Scenario:** We model the complete loss of `us-central1-b`:\n"
                "  1. Ingress traffic instantly fails over at the Cloud Load Balancer (Anycast MAGLEV tier routes solely to backends in zones A and C).\n"
                "  2. Stateful storage: Cloud SQL or Regional Persistent Disk initiates automatic failover to the synchronous secondary zone (`us-central1-a`).\n"
                "  3. Compute capacity: Total available compute drops by 33.3%. Remaining zones must absorb the 50% traffic increase ($1.0 / 0.667 = 1.5$).\n\n"
                "### 2. Trace-Based Cross-Zone Latency Synthesis\n"
                "- In normal operation, inter-zonal RPC spans show consistent $0.6\\text{ms} - 1.2\\text{ms}$ latency.\n"
                "- Under zonal partition simulation, traces reveal the exact timeline of request timeouts, retry storms, and eventual circuit-breaker "
                "ejection of failing zonal endpoints.\n\n"
                "### 3. Explicit Simulation Limits and Reality Boundaries\n"
                "- Responsible architectural modeling requires clearly stating what a tabletop or trace simulation **does not prove**:\n"
                "  - **Simulation Limit 1:** Tabletop models cannot prove that Google Cloud has sufficient spot/on-demand VM buffer capacity in neighboring "
                "zones during a widespread regional disaster unless guaranteed by Committed Use Reservations with Specific Affinity.\n"
                "  - **Simulation Limit 2:** Synthetic traces do not reproduce unpredictable cross-zone fiber carrier packet reordering or BGP convergence flaps."
            ),
            "questions": [
                "Why is a tabletop exercise and synthetic trace model appropriate for zonal disaster recovery analysis rather than physical fault injection?",
                "What capacity deficit calculation must be performed to guarantee that surviving zones can absorb full customer traffic during a single-zone loss?",
                "What critical operational assumptions remain unproven until tested with live traffic or reserved compute capacity?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/disaster-recovery-planning-guide",
            "reference_label": "Google Cloud Architecture: Disaster recovery planning guide and zonal failure modeling",
            "scenario": {
                "symptom": (
                    "During a tabletop disaster simulation modeling the loss of zone `us-central1-a`, the capacity calculator revealed that remaining "
                    "zones B and C would breach the project's regional `N2_CPUS` quota by 400 cores, preventing GKE autoscalers from spinning up replacement pods."
                ),
                "constraints": (
                    "Must establish an accurate capacity model guaranteeing surviving zones have verified compute headroom and quota reservations."
                ),
                "evidence": (
                    "Project quota inspection showed regional vCPU limit was 2,000 cores. Current 3-zone usage was 1,800 cores (600 cores/zone). "
                    "If Zone A fails, surviving zones need 900 cores each (1,800 total), which fits within quota, but scaling to absorb peak surge (2,400 cores) "
                    "would trigger quota rejection errors."
                ),
                "diagnostic_steps": [
                    "Audit Compute Engine regional quota usage via `gcloud compute project-info describe`.",
                    "Calculate per-zone capacity headroom: $\\text{Surviving Capacity} = \\text{Total Capacity} \\times \\frac{N-1}{N}$.",
                    "Review GKE cluster autoscaler minimum and maximum node boundaries per zone.",
                ],
                "root": (
                    "Hidden quota constraint: the architectural plan relied on autoscaling to replace lost zonal nodes without securing sufficient "
                    "regional vCPU quota headroom."
                ),
                "fix": (
                    "Submit an immediate quota increase request for regional `N2_CPUS` to 3,500 cores. Purchase Regional Compute Reservations in zones B and C "
                    "to guarantee physical hardware availability."
                ),
                "verify": (
                    "Rerun the tabletop capacity simulation; confirm that total required peak surge (2,400 cores) is fully covered by reserved capacity and quota."
                ),
                "residual": (
                    "Reservations incur continuous compute charges even when idle; FinOps must balance reservation costs against the business downtime risk."
                ),
                "diagram": (
                    "Zone A lost in tabletop drill",
                    "Autoscaler attempts node scale-up",
                    "Regional vCPU quota exceeded (Rejected)",
                    "Regional quota increased to 3,500 cores",
                    "Surviving zones B & C absorb 100% load"
                )
            },
            "lab": {
                "name": "Zonal Partition Tabletop Analysis, Trace Modeling, and Capacity Revision",
                "goal": "Author a comprehensive tabletop zonal outage model, simulate cross-zone latency degradation via Python trace modeling, and revise capacity requirements.",
                "expected": "An executable Python trace simulator modeling zonal timeouts, a mathematical capacity recovery model, and an explicit simulation limitation sheet.",
                "mode": "tabletop analysis & Python execution",
                "prereq": "Understanding of multi-zone GKE topology and Compute Engine quotas.",
                "preflight": "Ensure Python 3 standard library is present; no external packages needed.",
                "steps": [
                    "Author an executable Python script simulating distributed trace spans during a zonal network partition and timeout event:\n\n```sh\ncat <<'EOF' > simulate_zonal_trace.py\n# Simulation of Distributed Trace Spans during Zonal Outage\nimport json\nimport time\n\ndef simulate_cross_zone_rpc(calling_zone, target_zone, is_zone_down=False):\n    start_time = time.time()\n    if calling_zone == target_zone:\n        latency_ms = 0.35 # Same-zone intra-node RPC\n        status = \"OK\"\n    elif not is_zone_down:\n        latency_ms = 0.95 # Normal inter-zone fiber latency\n        status = \"OK\"\n    else:\n        latency_ms = 500.0 # Timeout threshold reached\n        status = \"DEADLINE_EXCEEDED\"\n        \n    return {\n        \"caller_zone\": calling_zone,\n        \"target_zone\": target_zone,\n        \"latency_ms\": latency_ms,\n        \"status\": status\n    }\n\n# Scenario: Zone B goes offline; Zone A attempts RPCs to Zones A, B, and C\nprint(\"=== SIMULATED DISTRIBUTED TRACE SPANS (Zone B Offline) ===\")\nrpc_a = simulate_cross_zone_rpc(\"us-central1-a\", \"us-central1-a\", is_zone_down=False)\nrpc_b = simulate_cross_zone_rpc(\"us-central1-a\", \"us-central1-b\", is_zone_down=True)\nrpc_c = simulate_cross_zone_rpc(\"us-central1-a\", \"us-central1-c\", is_zone_down=False)\n\nspans = [rpc_a, rpc_b, rpc_c]\nfor s in spans:\n    print(f\"Span: {s['caller_zone']} -> {s['target_zone']:16s} | Latency: {s['latency_ms']:6.2f}ms | Status: {s['status']}\")\n\nassert rpc_b[\"status\"] == \"DEADLINE_EXCEEDED\", \"Failed to capture zonal partition timeout!\"\nprint(\"\nPASS: Trace modeling accurately captured inter-zone timeout boundary.\")\nEOF\npython3 simulate_zonal_trace.py\n```",
                    "Author the revised capacity and recovery model with explicit simulation limitations fulfilling Day 97 exit evidence:\n\n```sh\ncat <<'EOF' > day-097-topic-03-capacity-model.md\n# Day 97: Revised Capacity / Recovery Model & Simulation Boundaries\n\n## 1. Before / During / After Telemetry Evidence Summary\n| Experiment State | P50 Latency | P95 Latency | P99 Latency | Error Rate | Active Compute Capacity |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n| **Before (Steady State)** | 38.2 ms | 112.5 ms | 185.0 ms | 0.00% | 100% (300 vCPUs across 3 zones) |\n| **During (Autohealing Drill)** | 44.1 ms | 128.0 ms | 215.0 ms | 0.02% | 88% (1 VM recreating in MIG) |\n| **During (Zonal Loss Tabletop)**| 58.5 ms | 165.0 ms | 245.0 ms | 0.15% | 66.7% (Zone B offline, traffic on A & C)|\n| **After (Full Recovery)** | 39.0 ms | 114.2 ms | 188.5 ms | 0.00% | 100% (All zones restored) |\n\n## 2. Revised Capacity Sizing Equation\nTo survive the catastrophic loss of 1 zone in an $N$-zone cluster without degrading P99 latency:\n$$\\text{Target Baseline Utilization} \\le \\frac{N - 1}{N} = \\frac{3 - 1}{3} = 66.7\\%$$\n- Each zone must operate at $\\le 66.7\\%$ CPU utilization during normal conditions so that surviving zones remain under $100\\%$ when absorbing the diverted load.\n- Regional vCPU Quota required: $\\text{Quota} \\ge 1.5 \\times \\text{Peak Concurrency Core Requirement}$.\n\n## 3. Explicit Tabletop Simulation Boundaries & Limitations\n1. **Unproven Provider Capacity:** This tabletop model assumes Google Cloud has physical host capacity in surviving zones; it does not prove physical hardware availability during multi-tenant regional disasters unless backed by Committed Use Reservations with Specific Affinity.\n2. **BGP Routing Convergence:** Synthetic traces assume instantaneous DNS/Anycast traffic redirection; real-world BGP and client DNS caching may cause 15–45 seconds of localized connection drops.\n3. **Database Disk I/O Saturation:** While compute shifts cleanly, doubling read throughput on surviving database replicas can trigger disk IOPS throttling unmodeled in stateless tracing.\nEOF\ncat day-097-topic-03-capacity-model.md\n```",
                    "Review all output artifacts and confirm that the Python trace simulator and capacity recovery model fulfill Day 97 Exit evidence criteria."
                ],
                "verification": "The Python script models cross-zone deadline timeouts and the capacity report provides quantitative before/during/after data and explicit simulation boundaries.",
                "trouble": "Ensure capacity equations account for integer node rounding when calculating per-zone minimum replica counts.",
                "cleanup": "Retain `simulate_zonal_trace.py` and `day-097-topic-03-capacity-model.md` as exit evidence artifacts.",
                "accept": "Completed zonal trace simulator and verified capacity/recovery model. File: `day-097-topic-03-capacity-model.md`.",
                "file": "day-097-topic-03-capacity-model.md"
            }
        }
    ]
}
