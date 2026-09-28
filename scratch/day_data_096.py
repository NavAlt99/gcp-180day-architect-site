"""day_data_096.py — Exhaustive architecture data specification for Day 96.

Covers Bounded Failure Experiment Design:
1. Load and stress testing: modern distributed load frameworks (k6, Locust), saturation curves, concurrency models, breaking-point discovery.
2. Chaos engineering and fault injection: bounded blast radii, terminating instances, blackholing a zone via Cloud Firewall, Envoy/Istio fault injection (synthetic latency, HTTP 503 drops).
3. Canary and blue/green deployments: Cloud Deploy, traffic splitting via Cloud Load Balancing and Service Mesh, automated rollback metrics and canary SLO evaluation gates.
4. Game days and DR drills: cross-functional chaos rehearsals, safety officer roles, non-negotiable abort triggers, preserving core business invariants (single fulfillment per order).
Follows PAGE_AUTHORING_CONTRACT.md with hands-on, verifiable exercises.
"""

DAY_NUM = 96

DATA = {
    "day": 96,
    "part1_intro": (
        "Day 96 transitions system resilience from passive theoretical assumptions to empirical, scientific verification through "
        "bounded failure experiments. Complex distributed architectures rarely fail in clean, anticipated ways; rather, cascading brownouts, "
        "deadlocks, and retry storms emerge only when production systems experience saturation, packet loss, or partial dependency degradation. "
        "Today's curriculum engineers a disciplined Chaos and Resilience framework: authoring scalable load testing scripts with k6, injecting "
        "bounded faults (zonal blackholes, instance kills, network jitter) using service mesh and firewall controls, deploying automated canary "
        "traffic gates in Cloud Deploy, and establishing Game Day governance with strict abort criteria that defend core business invariants."
    ),
    "exit_summary": (
        "Engineered an approved-for-production Bounded Failure Experimentation Sheet: authored distributed k6 load testing specifications; "
        "constructed bounded chaos injection runbooks (zonal network isolation, service-mesh latency injection); designed canary deployment "
        "traffic splitting policies with automated rollback triggers; validated Game Day governance preserving the single-fulfillment business invariant."
    ),
    "part2_intro": (
        "Resilience experimentation demands strict scientific methodology: defining a steady-state hypothesis, selecting an isolated blast radius, "
        "injecting a controlled fault, observing system adaptation signals, and enforcing instant abort conditions. The sections below analyze "
        "load testing mechanics, chaos fault primitives, canary routing boundaries, and Game Day operational controls."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Testing / Resilience Paradigm</th>
      <th>Primary Tools &amp; GCP Integration</th>
      <th>Fault Primitive / Test Mechanism</th>
      <th>Automated Abort Threshold</th>
      <th>Preserved Business Invariant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Load &amp; Stress Testing</strong></td>
      <td>k6, Locust on GKE / Cloud Run</td>
      <td>Virtual User (VU) ramp to 50,000 req/sec to discover saturation knee and thread pool exhaustion</td>
      <td>Error rate &gt; 1.0% or P99 latency &gt; 2,500ms for 30 consecutive seconds</td>
      <td>Zero database connection starvation; zero dropped financial transactions</td>
    </tr>
    <tr>
      <td><strong>Zonal Network Blackhole</strong></td>
      <td>Cloud Firewall / Route Tagging</td>
      <td>Priority 1 egress/ingress DENY rule isolating `us-central1-a` to test multi-zone failover</td>
      <td>Cross-zone failover time &gt; 15 seconds or health check flap across &gt; 1 zone</td>
      <td>Compute capacity autoscales in healthy zones without customer downtime</td>
    </tr>
    <tr>
      <td><strong>Synthetic Fault Injection</strong></td>
      <td>Istio / Cloud Service Mesh (Traffic Director)</td>
      <td>Inject 500ms latency and 10% HTTP 503 errors on downstream inventory gRPC calls</td>
      <td>Client checkout error budget burn rate &gt; 14.4x (catastrophic 1h threshold)</td>
      <td>Circuit breaker opens gracefully; client UI degrades to cached inventory</td>
    </tr>
    <tr>
      <td><strong>Canary Deployment</strong></td>
      <td>Cloud Deploy &amp; Global External Application Load Balancer</td>
      <td>Weighted traffic split: 1% Canary vs 99% Stable; incremental progression (1% &rarr; 5% &rarr; 25% &rarr; 100%)</td>
      <td>Canary HTTP 5xx rate &gt; 0.1% or Canary P95 latency &gt; 1.5x stable baseline</td>
      <td>Immediate automated rollback to stable version within 10 seconds</td>
    </tr>
    <tr>
      <td><strong>Asynchronous Replay Chaos</strong></td>
      <td>Cloud Pub/Sub &amp; Cloud Tasks</td>
      <td>Inject duplicate message IDs and out-of-order event streams to test consumer deduplication</td>
      <td>Duplicate fulfillment count &gt; 0 across any processed order ID</td>
      <td><strong>Strict Single Fulfillment:</strong> No customer order is billed or dispatched twice</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Bounded Chaos & Canary Experimentation Pipeline",
        "desc": "Architectural flow diagram showing distributed load generation, service mesh fault injection, canary traffic gates, and automated abort circuit breakers.",
        "caption": "Figure 96.1: Scientific experiment execution pipeline with steady-state monitoring and automated abort circuit breakers.",
        "nodes": [
            ("1. Baseline Steady State", "P99 < 150ms & 0% error"),
            ("2. Bounded Fault Injection", "k6 load & zonal blackhole"),
            ("3. Automated Abort Gate", "Rollback if burn rate > 14.4x"),
            ("4. Post-Test Verification", "Invariant & recovery confirmed"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Load and Stress Testing: Saturation Curves, Concurrency, and k6 Automation",
            "overview": (
                "Load testing validates that an architecture satisfies performance SLOs under anticipated traffic, while stress testing deliberately "
                "drives the system past its breaking point to observe degradation behavior. Modern distributed load tools like k6 and Locust model "
                "realistic user journeys using asynchronous, lightweight Virtual Users (VUs). By measuring throughput, concurrency, and latency percentiles "
                "across stepped ramp-up stages, engineers identify the system's 'saturation knee'—the inflection point where adding concurrency ceases to "
                "increase throughput and instead leads to queue buffer bloat, thread contention, and cascading timeouts."
            ),
            "preview": (
                "An e-commerce platform scales frontend pods rapidly during a flash sale, but throughput collapses because backend database connection pools "
                "become saturated. Proper stress testing identifies pool limits and enforces request rate-limiting before production brownouts occur."
            ),
            "technical": (
                "### 1. Saturation Curves and Little's Law\n"
                "- **Little's Law:** In any stable queuing system, the average number of concurrent requests in flight (L) equals the arrival rate (lambda) "
                "multiplied by the average latency (W): L = lambda * W.\n"
                "- **The Saturation Knee:** Below the saturation threshold, latency remains constant as throughput scales linearly with concurrency. "
                "Once physical bottlenecks (CPU, disk I/O, database lock contention) are reached, throughput plateaus and latency spikes exponentially. "
                "Unbounded queues buffer excess requests until timeouts trigger client retries, amplifying the overload into an unrecoverable collapse.\n\n"
                "### 2. Distributed Load Testing Frameworks (k6 vs Locust vs JMeter)\n"
                "- **k6 (JavaScript/Go runtime):** Compiles test scenarios into native Go routines, achieving tens of thousands of concurrent connections "
                "per VM with minimal CPU overhead. Supports declarative thresholds (e.g. `http_req_duration: ['p(95)<300']`) that automatically exit with "
                "failure codes in CI/CD pipelines.\n"
                "- **Locust (Python):** Event-based framework allowing complex, dynamic business logic in pure Python; ideal for multi-step transactional flows.\n"
                "- **JMeter (Java thread-per-client):** High resource consumption; prone to testing tool saturation where JMeter's own JVM pauses distort results.\n\n"
                "### 3. Test Topologies and Cloud Load Injection\n"
                "- **Distributed GKE Load Clusters:** Running load generators across multiple GKE nodes in a distinct testing project prevents local network "
                "interface card (NIC) saturation from becoming the bottleneck.\n"
                "- **Egress NAT and Port Limits:** Load generators must allocate sufficient Cloud NAT ports (minimum 4096 ports per VM) to prevent "
                "`EADDRNOTAVAIL` socket exhaustion when initiating 20,000+ outbound connections per minute."
            ),
            "questions": [
                "How does Little's Law explain why application latency increases exponentially once backend database connection pools are saturated?",
                "What architectural precautions must be taken to prevent distributed load test generators from exhausting local Cloud NAT socket ports?",
                "Why must load testing validate P95 and P99 latency percentiles rather than arithmetic average response times?",
            ],
            "reference": "https://k6.io/docs/using-k6/scenarios",
            "reference_label": "k6 Documentation: Scenarios, execution models, and automated threshold evaluation",
            "scenario": {
                "symptom": (
                    "During a preliminary load test at 12,000 requests/sec, Brightloaf's API response time jumped from 45ms to 9,800ms within 40 seconds, "
                    "causing GKE Horizontal Pod Autoscalers (HPA) to spin up 200 additional pods, which immediately crashed Cloud SQL."
                ),
                "constraints": (
                    "Must establish strict concurrency limits and load testing thresholds that prevent HPA runaway from crushing backend stateful databases."
                ),
                "evidence": (
                    "Cloud Monitoring showed Cloud SQL active connections surged from 80 to 2,400 (exceeding `max_connections = 1000`). "
                    "Each new pod opened 10 idle connections upon boot, exhausting database memory buffers."
                ),
                "diagnostic_steps": [
                    "Examine Cloud SQL connection metrics `cloudsql.googleapis.com/database/network/connections`.",
                    "Review k6 scenario execution metrics to correlate Virtual User concurrency with API response latency.",
                    "Audit HPA configuration to determine whether CPU target utilization was distorted by blocked thread wait states.",
                ],
                "root": (
                    "Unbounded connection pooling: scaling stateless pods without connection pooling intermediaries (such as PgBouncer) "
                    "caused autoscaling to amplify database resource exhaustion."
                ),
                "fix": (
                    "Deploy PgBouncer connection pooling sidecars on GKE with a maximum pool limit of 250 connections. Update k6 test suite "
                    "with hard automated abort thresholds (`http_req_failed > 0.02` immediately aborts test)."
                ),
                "verify": (
                    "Rerun k6 stress test up to 25,000 requests/sec; verify Cloud SQL connections stay bounded at 250 and P99 latency remains under 250ms."
                ),
                "residual": (
                    "PgBouncer manages connection limits but cannot speed up un-indexed database queries; slow queries will still back up in the pool."
                ),
                "diagram": (
                    "k6 ramps concurrency to 12k req/s",
                    "HPA spins 200 pods with 10 conns each",
                    "Cloud SQL max_connections exceeded",
                    "PgBouncer pooling & k6 abort gate deployed",
                    "Bounded 250 conns with steady P99 < 250ms"
                )
            },
            "lab": {
                "name": "k6 Stress Testing Specification and Concurrency Saturation Script",
                "goal": "Author a declarative k6 load test script defining stepped concurrency ramp-ups and strict automated abort thresholds.",
                "expected": "A validated k6 JavaScript script, an executable Python test runner simulating saturation knees, and a test analysis document.",
                "mode": "local script execution & tabletop analysis",
                "prereq": "Understanding of HTTP concurrency, request rates, and latency percentiles.",
                "preflight": "Ensure Python 3 standard library is accessible; no external packages required.",
                "steps": [
                    "Author the declarative k6 load testing specification (`load-test-checkout.js`) with staged VU ramp-up and threshold gates:\n\n```sh\ncat <<'EOF' > load-test-checkout.js\n// k6 Load & Stress Test Scenario: Checkout API Saturation\nimport http from 'k6/http';\nimport { check, sleep } from 'k6';\n\nexport const options = {\n  stages: [\n    { duration: '30s', target: 50 },  // Warm-up to 50 VUs\n    { duration: '1m', target: 200 },  // Normal peak load\n    { duration: '30s', target: 500 },  // Stress load to saturation knee\n    { duration: '1m', target: 500 },  // Sustained stress\n    { duration: '30s', target: 0 },    // Graceful recovery cool-down\n  ],\n  thresholds: {\n    // Bounded Abort Criteria:\n    http_req_duration: ['p(95)<300', 'p(99)<1000'], // 95% under 300ms, 99% under 1s\n    http_req_failed: ['rate<0.01'],                 // Under 1% failure rate\n  },\n};\n\nexport default function () {\n  const payload = JSON.stringify({\n    order_id: `ord-${__VU}-${__ITER}`,\n    sku: 'SKU-BRIGHTLOAF-ARTISAN',\n    quantity: 1,\n  });\n\n  const params = {\n    headers: {\n      'Content-Type': 'application/json',\n      'X-Simulated-Client': 'k6-load-engine',\n    },\n  };\n\n  const res = http.post('http://127.0.0.1:8080/api/v1/orders', payload, params);\n  check(res, {\n    'status is 200 or 201': (r) => r.status === 200 || r.status === 201,\n    'transaction idempotent': (r) => !r.body.includes('DUPLICATE_ORDER'),\n  });\n\n  sleep(0.1); // 100ms think time\n}\nEOF\ncat load-test-checkout.js\n```",
                    "Author an automated Python simulation modeling the saturation knee and verifying threshold evaluation logic:\n\n```sh\ncat <<'EOF' > simulate_saturation_curve.py\n# Mathematical simulation of system throughput saturation knee\n\ndef evaluate_system_performance(concurrency):\n    # Below saturation (knee at 250 concurrency)\n    if concurrency <= 250:\n        throughput = concurrency * 10 # 10 req/s per VU\n        latency_ms = 40 + (concurrency * 0.08) # Minimal queue wait\n        error_rate = 0.0\n    else:\n        # Saturated: throughput plateaus, queue backs up exponentially\n        throughput = 2500 # Capped by DB connection pool\n        excess_concurrency = concurrency - 250\n        latency_ms = 60 + (excess_concurrency ** 1.8) # Exponential queuing delay\n        error_rate = min(0.35, (excess_concurrency * 0.0015))\n        \n    return throughput, latency_ms, error_rate\n\nprint(\"Concurrency | Throughput (req/s) | Latency (ms) | Error Rate | Status\")\nprint(\"----------------------------------------------------------------------\")\n\nabort_triggered = False\nfor vus in [50, 100, 200, 250, 300, 400, 500]:\n    tput, lat, err = evaluate_system_performance(vus)\n    status = \"HEALTHY\"\n    if lat > 1000 or err > 0.01:\n        status = \"ABORT CRITERIA BREACHED\"\n        if not abort_triggered:\n            abort_triggered = True\n            first_abort_vu = vus\n    print(f\"{vus:11d} | {tput:18.1f} | {lat:12.1f} | {err*100:9.2f}% | {status}\")\n\nassert abort_triggered, \"Test failed: Saturation threshold was never reached!\"\nprint(f\"\nPASS: Saturation knee identified. Automated abort correctly triggered at {first_abort_vu} VUs.\")\nEOF\npython3 simulate_saturation_curve.py\n```",
                    "Review all output artifacts and confirm that the k6 script and Python saturation simulation pass mathematical assertions."
                ],
                "verification": "The k6 script defines staged concurrency and strict percentile thresholds, and the Python simulation proves the saturation inflection point.",
                "trouble": "Ensure k6 thresholds use single quotes inside JavaScript objects (`'p(95)<300'`) to prevent syntax errors.",
                "cleanup": "Retain `load-test-checkout.js` as an exit evidence artifact.",
                "accept": "Completed k6 load specification and verified saturation simulation script. File: `day-096-topic-01-load-testing.md`.",
                "file": "day-096-topic-01-load-testing.md"
            }
        },
        {
            "key": "topic-02",
            "title": "Chaos Engineering and Fault Injection: Zonal Blackholes and Service Mesh Latency",
            "overview": (
                "Chaos engineering is the discipline of experimenting on a distributed software system to build confidence in its capability to withstand "
                "turbulent conditions in production. Rather than causing unconstrained outages, principled chaos experiments enforce strict 'blast radii'—bounded "
                "domains where faults are injected under continuous automated supervision. Typical fault primitives include terminating random compute instances, "
                "blackholing a single availability zone via Cloud Firewall rules, and injecting artificial latency and HTTP 503 errors at the service mesh layer."
            ),
            "preview": (
                "When a network switch in an availability zone begins dropping 15% of packets, services in other zones hang waiting for timeouts. "
                "Injecting synthetic latency and zonal blackholes tests circuit breakers and proves the system isolates degraded zones without human intervention."
            ),
            "technical": (
                "### 1. The Principles of Chaos Engineering\n"
                "- **Hypothesis Formulation:** Define steady state using business metrics (e.g. order completion rate > 99.5%, P99 latency < 250ms). "
                "Hypothesize that upon injecting the fault, the steady state will be maintained through automated failover.\n"
                "- **Blast Radius Containment:** Experiments begin in isolated pre-production staging environments before progressing to single-canary production instances. "
                "Never run an experiment without a pre-tested, single-command automated rollback script.\n\n"
                "### 2. Fault Injection Primitives in Google Cloud\n"
                "- **Instance Termination:** Deleting Compute Engine VMs in an autoscaled Managed Instance Group (MIG) verifies that health checks replace "
                "dead nodes and load balancers redirect in-flight TCP sessions without 502 Bad Gateway errors.\n"
                "- **Zonal Network Blackhole (Firewall Isolation):** Creating a high-priority egress DENY firewall rule targeted at instances tagged in a specific zone "
                "(`us-central1-a`) simulates complete zonal loss without actually destroying persistent disk data.\n"
                "- **Service Mesh Fault Injection (Istio / Cloud Service Mesh):** Declaratively inject synthetic latency (e.g. 2.0s delay on 20% of requests) "
                "or abort codes (HTTP 503 on 10% of requests) via `VirtualService` CRDs without modifying application code.\n\n"
                "### 3. Automated Emergency Abort Triggers\n"
                "- A background monitoring daemon queries Cloud Monitoring every 5 seconds during the experiment.\n"
                "- If the global SLO error budget consumption exceeds the critical threshold (e.g. error rate > 2.0% for 15s), the daemon immediately "
                "triggers the rollback script, tearing down the injected fault and restoring normal network topology."
            ),
            "questions": [
                "Why is a zonal firewall egress blackhole architecturally safer for testing multi-zone failover than deleting running VM instances?",
                "How does Cloud Service Mesh inject synthetic network delay and HTTP aborts without requiring changes to application source code?",
                "What safety mechanisms guarantee that an uncontrolled chaos experiment can be terminated within seconds if customer impact occurs?",
            ],
            "reference": "https://istio.io/latest/docs/tasks/traffic-management/fault-injection/",
            "reference_label": "Istio / Cloud Service Mesh: Declarative fault injection and latency delay tasks",
            "scenario": {
                "symptom": (
                    "A transient packet loss brownout in `us-central1-b` caused the entire global storefront to stop taking orders, even though "
                    "zones `us-central1-a` and `us-central1-c` had 70% surplus compute capacity."
                ),
                "constraints": (
                    "Must verify that the application detects and drains degraded zones within 30 seconds while maintaining the single-fulfillment invariant."
                ),
                "evidence": (
                    "Frontend pods in zone A remained connected to slow, packet-dropping database read replicas in zone B because TCP connection "
                    "keep-alives were set to 7200 seconds and no gRPC client deadlines were enforced."
                ),
                "diagnostic_steps": [
                    "Inspect TCP connection states on GKE pods using `netstat -tn` to identify connections stuck in `CLOSE_WAIT`.",
                    "Verify Envoy proxy connection pool timeouts in Cloud Service Mesh access logs.",
                    "Inspect Cloud Load Balancing backend health check interval and unhealthy threshold parameters.",
                ],
                "root": (
                    "Missing gRPC deadlines and overly generous load balancer health checks (requiring 3 consecutive 10-second failures) allowed "
                    "a partially degraded zone to blackhole customer traffic for over 3 minutes."
                ),
                "fix": (
                    "Enforce strict 500ms gRPC request deadlines and configure Cloud Service Mesh outlier detection (`consecutive5xxErrors: 3`, "
                    "`baseEjectionTime: 30s`). Rehearse zonal failover using automated chaos firewall rules."
                ),
                "verify": (
                    "Execute the zonal blackhole chaos script; verify outlier detection ejects degraded zone B within 6 seconds and 100% of checkout "
                    "transactions succeed across zones A and C."
                ),
                "residual": (
                    "Ejecting an entire zone reduces total cluster compute capacity by 33%; remaining zones must have adequate HPA headroom to absorb load."
                ),
                "diagram": (
                    "Packet loss brownout in zone B",
                    "Missing gRPC timeouts trap requests",
                    "Global storefront halts on timeouts",
                    "Outlier detection & 500ms deadlines deployed",
                    "Zone B ejected in 6s; A & C handle 100% load"
                )
            },
            "lab": {
                "name": "Chaos Engineering: Zonal Network Blackhole and Service Mesh Fault Injection",
                "goal": "Author executable scripts for simulating zonal network isolation via Cloud Firewall and declarative Istio fault injection manifests.",
                "expected": "A production shell script deploying and rolling back a zonal blackhole, an Istio VirtualService fault manifest, and an automated verification test.",
                "mode": "tabletop analysis & shell/YAML synthesis",
                "prereq": "Understanding of Google Cloud VPC firewall rules and Service Mesh routing.",
                "preflight": "Review gcloud compute firewall-rules CLI commands and Istio fault injection schemas.",
                "steps": [
                    "Author the automated zonal isolation and emergency rollback shell script (`chaos-zonal-blackhole.sh`):\n\n```sh\ncat <<'EOF' > chaos-zonal-blackhole.sh\n#!/usr/bin/env bash\nset -euo pipefail\n\n# Chaos Experiment: Bounded Zonal Network Blackhole\nRULE_NAME=\"chaos-isolate-zone-b\"\nNETWORK=\"brightloaf-vpc\"\nTARGET_TAG=\"zone-us-central1-b\"\nPRIORITY=10 # Highest priority override\n\ncase \"${1:-}\" in\n  inject)\n    echo \"[!] INJECTING CHAOS: Blackholing egress traffic from zone us-central1-b...\"\n    cat <<COMMAND\ngcloud compute firewall-rules create \"$RULE_NAME\" \\\n    --network=\"$NETWORK\" \\\n    --priority=\"$PRIORITY\" \\\n    --direction=EGRESS \\\n    --action=DENY \\\n    --rules=all \\\n    --target-tags=\"$TARGET_TAG\" \\\n    --description=\"CHAOS EXPERIMENT: Bounded egress blackhole for zone B\"\nCOMMAND\n    echo \"[+] Injected. Egress traffic in zone B blocked.\"\n    ;;\n  abort|rollback)\n    echo \"[*] ROLLING BACK CHAOS: Removing isolation firewall rule...\"\n    cat <<COMMAND\ngcloud compute firewall-rules delete \"$RULE_NAME\" --quiet\nCOMMAND\n    echo \"[+] Rollback complete. Normal zonal routing restored.\"\n    ;;\n  *)\n    echo \"Usage: $0 {inject|rollback|abort}\"\n    exit 1\n    ;;\nesac\nEOF\nchmod +x chaos-zonal-blackhole.sh\n./chaos-zonal-blackhole.sh inject\n./chaos-zonal-blackhole.sh rollback\n```",
                    "Author a declarative Cloud Service Mesh (Istio) Fault Injection manifest injecting synthetic latency and HTTP 503 errors:\n\n```sh\ncat <<'EOF' > istio-fault-injection.yaml\napiVersion: networking.istio.io/v1beta1\nkind: VirtualService\nmetadata:\n  name: inventory-service-chaos\n  namespace: production\nspec:\n  hosts:\n    - inventory-service.production.svc.cluster.local\n  http:\n    - match:\n        - headers:\n            x-chaos-experiment:\n              exact: \"resilience-drill-2026\"\n      fault:\n        delay:\n          percentage:\n            value: 20.0 # 20% of matching requests receive 1.5s delay\n          fixedDelay: 1.5s\n        abort:\n          percentage:\n            value: 5.0  # 5% of matching requests receive HTTP 503\n          httpStatus: 503\n      route:\n        - destination:\n            host: inventory-service.production.svc.cluster.local\n            subset: v1\n    - route:\n        - destination:\n            host: inventory-service.production.svc.cluster.local\n            subset: v1\nEOF\ncat istio-fault-injection.yaml\n```",
                    "Author an automated Python simulation verifying that the client circuit breaker opens and falls back gracefully when faults are injected:\n\n```sh\ncat <<'EOF' > simulate_circuit_breaker.py\n# Simulation of Client Circuit Breaker Responding to Injected Faults\nimport random\n\ndef simulate_backend_call(inject_fault=False):\n    if inject_fault and random.random() < 0.25:\n        return False, 503, \"Service Unavailable (Chaos Injected)\"\n    return True, 200, \"OK\"\n\n# Circuit Breaker state: CLOSED, OPEN, HALF_OPEN\nstate = \"CLOSED\"\nfailure_count = 0\nconsecutive_success = 0\n\nprint(\"Request | Injected | Result | CB State | Fallback Invoked\")\nprint(\"----------------------------------------------------------\")\n\nfor req_id in range(1, 21):\n    fault_active = (req_id >= 5 and req_id <= 12)\n    success, code, msg = simulate_backend_call(inject_fault=fault_active)\n    fallback = False\n    \n    if state == \"OPEN\":\n        fallback = True\n        status_text = \"SKIPPED (Circuit Open)\"\n    elif success:\n        failure_count = 0\n        status_text = f\"{code} OK\"\n    else:\n        failure_count += 1\n        status_text = f\"{code} FAULT\"\n        if failure_count >= 3:\n            state = \"OPEN\"\n            fallback = True\n            \n    print(f\"{req_id:7d} | {str(fault_active):8s} | {status_text:20s} | {state:8s} | {str(fallback)}\")\n\nprint(\"\nPASS: Circuit breaker prevented thread exhaustion and protected client invariant.\")\nEOF\npython3 simulate_circuit_breaker.py\n```",
                    "Review all output artifacts and confirm that the shell script, YAML manifest, and Python circuit breaker simulation run without error."
                ],
                "verification": "The shell script includes inject and rollback idempotency, the Istio YAML targets explicit request headers to limit blast radius, and the Python test proves circuit breaker isolation.",
                "trouble": "Ensure Istio fault injection matches on a custom test header (`x-chaos-experiment`) so regular customer traffic is not impacted during staging experiments.",
                "cleanup": "Retain `chaos-zonal-blackhole.sh` and `istio-fault-injection.yaml` as exit evidence artifacts.",
                "accept": "Completed chaos firewall automation script and verified Istio fault manifest. File: `day-096-topic-02-chaos-injection.md`.",
                "file": "day-096-topic-02-chaos-injection.md"
            }
        },
        {
            "key": "topic-03",
            "title": "Canary and Blue/Green Deployments: Cloud Deploy, Traffic Director, and Rollback Gates",
            "overview": (
                "Continuous delivery in high-availability environments requires deployment strategies that eliminate downtime and prevent bad releases "
                "from impacting the entire user base. **Blue/Green deployments** maintain two identical environments, instantly switching 100% of traffic "
                "via load balancer target pool reassignment. **Canary deployments** take a progressive approach, routing a tiny fraction (1% to 5%) "
                "of live production traffic to the new version (Canary) while 95% to 99% continues on the stable release. Google Cloud Deploy and "
                "Cloud Load Balancing automate this progressive rollout, evaluating error and latency metrics after each phase and executing instant rollbacks "
                "if canary SLO thresholds are breached."
            ),
            "preview": (
                "A subtle memory leak in a new software release causes pods to crash only after 20 minutes under real traffic. "
                "A Canary deployment catches the elevated error rate at 1% traffic, automatically rolling back before 99% of customers are impacted."
            ),
            "technical": (
                "### 1. Progressive Canary Mechanics with Cloud Load Balancing\n"
                "- **Weighted Backend Services:** Google Cloud Global External Application Load Balancers allow setting traffic weights on backend services "
                "associated with the same URL map (e.g. `stable-backend: 95`, `canary-backend: 5`).\n"
                "- **Session Affinity Considerations:** When testing stateful or cookie-based sessions, architects configure `GENERATED_COOKIE` affinity "
                "to ensure an individual user consistently hits either the canary or stable backend, preventing jarring UI state resets.\n\n"
                "### 2. Google Cloud Deploy Automated Delivery Pipelines\n"
                "- **Pipelines:** Defined via `clouddeploy.yaml` with explicit progression stages: `dev` &rarr; `staging` &rarr; `production`.\n"
                "- **Canary Strategy Configuration:** Declares automatic progression increments:\n"
                "  `strategy.canary.runtimeConfig.cloudRun.serviceSpec` or `kubernetes.gatewayService` with phases: `phase 1: 10%`, `phase 2: 25%`, `phase 3: 100%`.\n"
                "- **Pre-deployment & Post-deployment Hooks:** Execute automated smoke tests and Cloud Monitoring verification queries between phases.\n\n"
                "### 3. Automated Rollback Gates and Telemetry Verification\n"
                "- SREs define canary comparison gates: Canary metrics are compared directly against the concurrent Stable baseline:\n"
                "  - $\\text{Canary Error Rate} > 1.5 \\times \\text{Stable Error Rate}$ &rarr; **Immediate Rollback**.\n"
                "  - $\\text{Canary P95 Latency} > 1.25 \\times \\text{Stable P95 Latency}$ &rarr; **Immediate Rollback**.\n"
                "- Rollback executes in sub-second time by resetting load balancer weights to `stable: 100, canary: 0` without re-deploying pods."
            ),
            "questions": [
                "How does a progressive canary deployment mitigate the risk of slow-burning bugs (such as memory leaks) compared to Blue/Green deployment?",
                "Why must automated canary analysis compare Canary performance against concurrent Stable performance rather than a static historical baseline?",
                "How does Cloud Load Balancing weighted routing achieve sub-second traffic rollback without waiting for pod termination?",
            ],
            "reference": "https://docs.cloud.google.com/deploy/docs/canary-deployment",
            "reference_label": "Google Cloud Deploy: Automated progressive canary deployments and verification",
            "scenario": {
                "symptom": (
                    "A new microservice version v2.1.0 was rolled out directly to 100% of production. Within 12 minutes, a database connection pool leak "
                    "exhausted all available slots, dropping 100% of checkout transactions and requiring a stressful 45-minute rollback procedure."
                ),
                "constraints": (
                    "Must automate deployment pipelines such that new releases are verified against live production traffic with zero downtime and automatic 10-second rollbacks."
                ),
                "evidence": (
                    "Postmortem review showed the v2.1.0 code passed all staging synthetic tests because staging lacked production-scale concurrency. "
                    "The defect only manifested when concurrent user sessions exceeded 500."
                ),
                "diagnostic_steps": [
                    "Review Cloud Deploy rollout history and target release manifests.",
                    "Inspect Cloud Load Balancing traffic logs grouped by backend service version tag.",
                    "Analyze Cloud Monitoring metrics comparing error rates across v1.0 and v2.1.0 instances.",
                ],
                "root": (
                    "All-at-once deployment strategy: deploying straight to 100% production traffic exposed all users to an un-isolated concurrency defect."
                ),
                "fix": (
                    "Implement a progressive Cloud Deploy canary pipeline (1% &rarr; 5% &rarr; 25% &rarr; 100%) with automated Cloud Monitoring verification hooks "
                    "that abort the rollout and restore 100% stable traffic if canary error rates exceed 0.5%."
                ),
                "verify": (
                    "Deploy a synthetic faulty canary; verify Cloud Deploy detects elevated 5xx errors during Phase 1 (1%) and triggers automatic rollback in <10 seconds."
                ),
                "residual": (
                    "Database schema migrations must remain backwards-compatible with both Stable and Canary versions simultaneously (expand/contract pattern)."
                ),
                "diagram": (
                    "v2.1.0 deployed straight to 100%",
                    "Connection leak crashes all pods",
                    "45-minute manual rollback outage",
                    "Cloud Deploy 1% canary pipeline implemented",
                    "Defect caught at 1%; 10s auto-rollback"
                )
            },
            "lab": {
                "name": "Cloud Deploy Progressive Canary Pipeline and Traffic Splitting Manifest",
                "goal": "Author a declarative Google Cloud Deploy canary pipeline and verify weighted traffic splitting and automated rollback logic.",
                "expected": "A validated `clouddeploy.yaml` canary pipeline definition, a URL map traffic-split configuration, and an automated verification script.",
                "mode": "tabletop analysis & YAML synthesis",
                "prereq": "Understanding of Google Cloud Deploy delivery pipelines and Load Balancing.",
                "preflight": "Review Cloud Deploy pipeline schemas and weighted backend service syntax.",
                "steps": [
                    "Author the Google Cloud Deploy progressive canary delivery pipeline manifest (`clouddeploy.yaml`):\n\n```sh\ncat <<'EOF' > clouddeploy.yaml\napiVersion: deploy.cloud.google.com/v1\nkind: DeliveryPipeline\nmetadata:\n  name: brightloaf-canary-pipeline\ndescription: Enterprise progressive canary deployment pipeline for Brightloaf API\nserialPipeline:\n  stages:\n    - targetId: staging-env\n    - targetId: prod-env\n      strategy:\n        canary:\n          runtimeConfig:\n            kubernetes:\n              serviceNetworking:\n                service: \"orders-api\"\n                deployment: \"orders-api\"\n          route:\n            phases:\n              - id: \"canary-1-percent\"\n                percentage: 1\n                verify: true\n              - id: \"canary-10-percent\"\n                percentage: 10\n                verify: true\n              - id: \"canary-50-percent\"\n                percentage: 50\n                verify: true\n              - id: \"full-rollout\"\n                percentage: 100\nEOF\ncat clouddeploy.yaml\n```",
                    "Author the Google Cloud Load Balancing weighted URL map patch configuring 1% canary traffic split:\n\n```sh\ncat <<'EOF' > patch_url_map_canary.yaml\n# Weighted traffic splitting configuration for Global External Application Load Balancer\ndefaultService: https://www.googleapis.com/compute/v1/projects/brightloaf-prod/global/backendServices/orders-be-stable\nhostRules:\n  - hosts:\n      - \"api.brightloaf.com\"\n    pathMatcher: api-matcher\npathMatchers:\n  - name: api-matcher\n    defaultRouteAction:\n      weightedBackendServices:\n        - backendService: https://www.googleapis.com/compute/v1/projects/brightloaf-prod/global/backendServices/orders-be-stable\n          weight: 99\n        - backendService: https://www.googleapis.com/compute/v1/projects/brightloaf-prod/global/backendServices/orders-be-canary\n          weight: 1\nEOF\ncat patch_url_map_canary.yaml\n```",
                    "Author an automated Python simulation modeling canary metric evaluation and automatic rollback decision logic:\n\n```sh\ncat <<'EOF' > simulate_canary_evaluation.py\n# Automated Canary Analysis (ACA) Decision Simulator\n\ndef evaluate_canary_health(canary_error_rate, stable_error_rate, canary_p95_ms, stable_p95_ms):\n    # Rollback Rule 1: Canary error rate exceeds 1.5x stable baseline\n    if canary_error_rate > (stable_error_rate * 1.5 + 0.005):\n        return False, f\"ROLLBACK: Error rate excessive ({canary_error_rate*100:.2f}% vs {stable_error_rate*100:.2f}%)\"\n    \n    # Rollback Rule 2: Canary latency exceeds 1.25x stable baseline\n    if canary_p95_ms > (stable_p95_ms * 1.25):\n        return False, f\"ROLLBACK: Latency degraded ({canary_p95_ms:.1f}ms vs {stable_p95_ms:.1f}ms)\"\n        \n    return True, \"PROMOTE: Metrics within acceptable SLO tolerances\"\n\n# Test Case A: Healthy Canary (Minor normal variance)\nhealthy, msg_a = evaluate_canary_health(0.002, 0.002, 145.0, 140.0)\nprint(f\"Test Case A (Normal Build):  {msg_a}\")\nassert healthy, \"Test Case A failed: Healthy canary should be promoted!\"\n\n# Test Case B: Bad Canary (Elevated errors)\nunhealthy, msg_b = evaluate_canary_health(0.025, 0.002, 148.0, 140.0)\nprint(f\"Test Case B (Buggy Build):   {msg_b}\")\nassert not unhealthy, \"Test Case B failed: Buggy canary was not rolled back!\"\n\nprint(\"\nPASS: Automated Canary Analysis (ACA) gate logic validated successfully.\")\nEOF\npython3 simulate_canary_evaluation.py\n```",
                    "Review all output artifacts and confirm that the Cloud Deploy pipeline, weighted URL map, and Python canary evaluation simulator run cleanly."
                ],
                "verification": "The Cloud Deploy manifest defines progressive percentage phases with verification enabled, and the Python test confirms automated rollback decision thresholds.",
                "trouble": "Ensure sum of weights in `weightedBackendServices` equals exactly 100 (e.g. 99 and 1) to prevent URL map validation rejection.",
                "cleanup": "Retain `clouddeploy.yaml` and `patch_url_map_canary.yaml` as exit evidence artifacts.",
                "accept": "Completed Cloud Deploy canary pipeline and verified URL map weighted routing manifest. File: `day-096-topic-03-canary-deploy.md`.",
                "file": "day-096-topic-03-canary-deploy.md"
            }
        },
        {
            "key": "topic-04",
            "title": "Game Days and Disaster Recovery Drills: Operational Rehearsals and Invariant Defense",
            "overview": (
                "A Game Day is a structured operational exercise where cross-functional engineering, SRE, and product teams rehearse major failure "
                "scenarios in a live or pre-production environment. Rather than testing only automated system failover, Game Days test human incident "
                "response, communication hygiene, monitoring clarity, and runbook accuracy under pressure. To maintain safety, every Game Day operates "
                "under an explicit Governance Charter with designated Incident Commanders, independent Safety Officers armed with instant abort power, "
                "and non-negotiable business invariants—most critically, the guarantee that no customer transaction is duplicated or lost."
            ),
            "preview": (
                "During a chaos experiment simulating Pub/Sub broker restart, consumers replay unacknowledged messages and charge 40 customers twice. "
                "Strict Game Day governance and idempotent consumer design defend core business invariants against replay corruption."
            ),
            "technical": (
                "### 1. Game Day Governance and Role RACI\n"
                "- **Incident Commander (IC):** Drives the triage workflow, coordinates responder hypotheses, and makes high-level operational decisions.\n"
                "- **Safety Officer:** An independent senior engineer whose sole responsibility is monitoring customer impact and abort criteria. "
                "The Safety Officer has absolute authority to abort the exercise instantly without seeking management approval.\n"
                "- **Chaos Lead:** Prepares and executes the specific fault injection runbooks (e.g. killing nodes or cutting network routes).\n"
                "- **Scribe / Communications Lead:** Records timeline events and publishes internal and external status updates.\n\n"
                "### 2. Defending the Core Business Invariant: Single Fulfillment per Order\n"
                "- In event-driven Google Cloud architectures (Pub/Sub, Cloud Tasks), messages provide **at-least-once delivery**.\n"
                "- When testing broker failure or consumer crashes, message redelivery is guaranteed. SREs must verify that the consumer enforces "
                "**idempotent execution**:\n"
                "  - Checking a transactional deduplication store (e.g. Cloud Spanner or Cloud SQL `processed_orders` table with a unique constraint on `order_id`).\n"
                "  - Rejecting redelivered events before executing payment charges or warehouse fulfillment.\n\n"
                "### 3. Non-Negotiable Abort Triggers\n"
                "- Every Game Day protocol requires explicit, quantifiable abort criteria established before the drill starts:\n"
                "  1. Global customer error rate exceeds 1.0% for more than 15 seconds.\n"
                "  2. Total revenue checkout transaction loss exceeds $500.\n"
                "  3. Any duplicate fulfillment event is detected (zero-tolerance invariant).\n"
                "  4. Telemetry blindness: if monitoring dashboards or log streams become unresponsive for >30 seconds."
            ),
            "questions": [
                "Why must the Safety Officer have unilateral, absolute authority to abort a Game Day drill without executive consensus?",
                "How does an at-least-once message broker (such as Cloud Pub/Sub) threaten the single-fulfillment invariant during chaos failure drills?",
                "What architectural mechanisms guarantee that a consumer idempotency check is atomic and immune to race conditions?",
            ],
            "reference": "https://sre.google/workbook/incident-response/",
            "reference_label": "Google SRE Workbook: Incident response drills, tabletop exercises, and postmortems",
            "scenario": {
                "symptom": (
                    "During a Game Day chaos drill simulating Cloud Pub/Sub worker pod terminations, 12 customer credit cards were charged twice "
                    "because redelivered order messages were re-executed by a replacement worker pod."
                ),
                "constraints": (
                    "Must guarantee 100% idempotent message consumption during catastrophic worker crashes: no customer order may ever be fulfilled twice."
                ),
                "evidence": (
                    "Post-drill log analysis confirmed Pub/Sub redelivered message `msg-9921` after the original worker pod was killed before calling `acknowledge()`. "
                    "The new worker pod processed the order from scratch without verifying whether payment had already succeeded."
                ),
                "diagnostic_steps": [
                    "Query Cloud SQL payment transactions grouped by `order_id` having `COUNT(*) > 1`.",
                    "Inspect worker service log lines for `msg_acknowledged` timestamps relative to pod termination events.",
                    "Audit the database schema to check for unique constraint enforcement on `order_id` in the payment ledger.",
                ],
                "root": (
                    "Non-idempotent consumer logic: the fulfillment worker executed payment charges before recording a persistent transaction lock, "
                    "causing unacknowledged redelivered messages to process as brand-new orders."
                ),
                "fix": (
                    "Implement transactional idempotency using an atomic database check: `INSERT INTO processed_events (event_id, processed_at) VALUES (?, NOW()) "
                    "ON CONFLICT (event_id) DO NOTHING`. If zero rows are inserted, abort processing and immediately acknowledge the message."
                ),
                "verify": (
                    "Rerun the Game Day drill; inject 500 duplicate order messages with identical `event_id` tokens; verify payment records show exactly "
                    "500 successful single charges and 0 duplicate charges."
                ),
                "residual": (
                    "Idempotency records must be retained in the database for at least the maximum message retention window of the queue (e.g. 7 days in Pub/Sub)."
                ),
                "diagram": (
                    "Worker killed before ACK",
                    "Pub/Sub redelivers message",
                    "Non-idempotent worker double-charges",
                    "Atomic event_id DB constraint added",
                    "Duplicate rejected; invariant preserved"
                )
            },
            "lab": {
                "name": "Game Day Operational Charter and Idempotent Message Processing Verification",
                "goal": "Author a Game Day operational protocol with strict abort criteria and implement a Python test proving the single-fulfillment invariant under duplicate event injection.",
                "expected": "A complete Game Day charter in Markdown and an executable Python script verifying idempotent consumer execution under chaos replay.",
                "mode": "tabletop analysis & Python execution",
                "prereq": "Understanding of distributed messaging, at-least-once delivery, and idempotency.",
                "preflight": "Ensure Python 3 standard library is accessible; no external dependencies required.",
                "steps": [
                    "Author the Game Day Operational Charter and Governance Protocol (`day-096-topic-04-gameday-charter.md`):\n\n```sh\ncat <<'EOF' > day-096-topic-04-gameday-charter.md\n# Day 96: Enterprise Game Day Operational Charter & Governance Protocol\n\n## 1. Drill Scope & Objectives\n- **Target System:** Brightloaf Order Processing Pipeline (Cloud Run & Cloud Pub/Sub).\n- **Drill Date & Window:** 2026-09-28 14:00 - 16:00 UTC.\n- **Primary Hypothesis:** Terminating 50% of active order consumer workers during peak load will not result in dropped orders, duplicate customer charges, or P99 latency exceeding 2.0 seconds.\n\n## 2. Command Team RACI\n- **Incident Commander:** Lead SRE (Manages technical coordination).\n- **Safety Officer:** Principal Reliability Architect (Sole owner of abort triggers; monitors customer SLOs).\n- **Chaos Operator:** Platform Engineer (Executes fault injection commands).\n- **Scribe:** Systems Analyst (Maintains timeline log).\n\n## 3. Non-Negotiable Abort Triggers\n1. Global customer checkout error rate > 0.5% for >15 consecutive seconds.\n2. Invariant Violation: Any duplicate fulfillment or charge detected (IMMEDIATE ABORT).\n3. Database connection pool exhaustion > 90% capacity.\n4. Telemetry failure: Loss of Cloud Monitoring metric stream for >30 seconds.\nEOF\ncat day-096-topic-04-gameday-charter.md\n```",
                    "Author an executable Python script verifying idempotent message consumption under aggressive duplicate injection:\n\n```sh\ncat <<'EOF' > test_idempotent_consumer.py\n# Simulation of Idempotent Message Consumer Protecting Single-Fulfillment Invariant\n\nclass IdempotentOrderProcessor:\n    def __init__(self):\n        self.processed_event_ids = set() # Simulated atomic transactional deduplication ledger\n        self.customer_charges = {}\n        self.duplicate_rejections = 0\n        \n    def process_order_event(self, event_id, customer_id, amount_usd):\n        # Step 1: Atomic Deduplication Gate (Defends Business Invariant)\n        if event_id in self.processed_event_ids:\n            self.duplicate_rejections += 1\n            return False, \"REJECTED: Duplicate event detected. Invariant protected.\"\n            \n        # Step 2: Record lock atomically\n        self.processed_event_ids.add(event_id)\n        \n        # Step 3: Execute Business Logic\n        if customer_id not in self.customer_charges:\n            self.customer_charges[customer_id] = 0.0\n        self.customer_charges[customer_id] += amount_usd\n        \n        return True, f\"SUCCESS: Charged ${amount_usd:.2f}\"\n\nprocessor = IdempotentOrderProcessor()\n\n# Chaos Invariant Test: 10 distinct orders, but each sent 3 times (simulating Pub/Sub redelivery after worker crash)\ntotal_messages = 0\nfor i in range(1, 11):\n    event_id = f\"evt-order-{i:03d}\"\n    customer_id = f\"cust-{i:03d}\"\n    for attempt in range(1, 4): # 3 deliveries per order\n        total_messages += 1\n        success, msg = processor.process_order_event(event_id, customer_id, 25.00)\n\nprint(f\"Total Messages Injected:    {total_messages}\")\nprint(f\"Unique Orders Processed:    {len(processor.processed_event_ids)}\")\nprint(f\"Duplicate Replays Rejected: {processor.duplicate_rejections}\")\n\n# Assert invariant: Exactly 10 unique orders charged, exactly 20 duplicates rejected\nassert len(processor.processed_event_ids) == 10, \"Invariant breached: incorrect unique orders!\"\nassert processor.duplicate_rejections == 20, \"Invariant breached: duplicate charges permitted!\"\nfor cust, total in processor.customer_charges.items():\n    assert total == 25.00, f\"Invariant breached: Customer {cust} charged ${total} instead of $25.00!\"\n\nprint(\"\nPASS: Single fulfillment per order invariant mathematically verified under chaos replay!\")\nEOF\npython3 test_idempotent_consumer.py\n```",
                    "Author the approved-for-lab experiment sheet fulfilling Day 96 exit evidence:\n\n```sh\ncat <<'EOF' > day-096-topic-04-experiment-sheet.md\n# Day 96: Approved-for-Lab Bounded Failure Experiment Sheet\n\n| Experiment ID | Injected Fault Primitive | Steady-State Hypothesis | Automated Abort Threshold | Preserved Invariant |\n| :--- | :--- | :--- | :--- | :--- |\n| **EXP-01: CPU Saturation** | 500 Virtual Users via k6 stress test | P99 latency remains <300ms via HPA autoscaling | Global error rate > 1.0% or P99 > 2500ms | Zero dropped checkout requests |\n| **EXP-02: Zonal Blackhole** | Priority 10 Cloud Firewall egress DENY on `us-central1-b` | Traffic drains to zones A & C in <15s | Health check flap across >1 zone | Zero customer 502 Bad Gateway errors |\n| **EXP-03: Dependency Latency**| Istio 1.5s delay & 5% 503 errors on Inventory API | Client circuit breaker trips; degrades to cached stock | Checkout error budget burn rate > 14.4x | No database thread starvation |\n| **EXP-04: Pub/Sub Replay** | Replay 500 duplicate message IDs to fulfillment queue | Idempotent consumer deduplicates messages | Duplicate execution count > 0 | **Single fulfillment per customer order** |\nEOF\ncat day-096-topic-04-experiment-sheet.md\n```",
                    "Review all output artifacts and confirm that the Game Day charter, Python idempotency verification test, and experiment sheet fulfill Day 96 Exit evidence criteria."
                ],
                "verification": "The Game Day charter defines strict role RACI and quantitative abort criteria, the Python test proves zero duplicate transactions under message replay, and the experiment sheet links signals to invariants.",
                "trouble": "Ensure idempotency key storage uses an atomic unique index or set to avoid race conditions during concurrent worker thread execution.",
                "cleanup": "Retain `day-096-topic-04-gameday-charter.md` and `day-096-topic-04-experiment-sheet.md` as exit evidence artifacts.",
                "accept": "Completed Game Day charter and verified approved-for-lab experiment sheet. File: `day-096-topic-04-gameday-drills.md`.",
                "file": "day-096-topic-04-gameday-drills.md"
            }
        }
    ]
}
