"""day_data_085.py — Exhaustive architecture data specification for Day 85.

Covers Retries, Timeouts, and Overload Vocabulary:
1. Timeout/deadline budgets, bounded retry with jitter, idempotency keys, circuit breakers, bulkheads, queuing dynamics.
2. Distinguishing measured from forecast throughput, Little's Law, retry amplification budgets.
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 85

DATA = {
    "day": 85,
    "part1_intro": (
        "Day 85 masters the operational mechanics of distributed communication under stress: timeouts, deadline budgets, "
        "exponential backoff with decorrelated jitter, idempotency keys, circuit breakers, bulkheads, and queuing dynamics. "
        "In a distributed cloud system, naive retry policies are the primary cause of catastrophic self-inflicted denial-of-service "
        "(DoS) attacks. When a downstream database experiences a temporary 200ms latency blip, aggressive client retries multiply "
        "incoming traffic by 300% to 500%, transforming a minor transient hiccup into a prolonged, cascading system collapse. "
        "Architects must master Little's Law (L = λW) to understand how queuing delays explode non-linearly near saturation, strictly "
        "distinguish empirical measured throughput from speculative forecast models, and enforce end-to-end deadline propagation "
        "and strict retry budgets to eliminate duplicate fulfillment and retry storms."
    ),
    "exit_summary": (
        "Engineered end-to-end deadline propagation and exponential backoff with full jitter algorithms; implemented distributed "
        "idempotency keys guaranteeing the Day 64 single-fulfillment invariant under repeated retries; constructed an empirical "
        "versus forecast capacity model applying Little's Law (L = λW) demonstrating non-linear queue explosion above 80% saturation; "
        "deployed a runnable Python retry storm simulator enforcing a 10% global retry budget that caps traffic amplification."
    ),
    "part2_intro": (
        "Distributed resilience requires precise control over concurrency, latency percentiles, and retry amplification. "
        "The sections below provide deep engineering specifications for deadline budgets, jitter math, circuit breakers, "
        "idempotent outbox design, and queuing theory."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Resilience Pattern</th>
      <th>Primary Failure Mitigated</th>
      <th>Key Configuration Parameters</th>
      <th>Trade-off / Operational Boundary</th>
      <th>Google Cloud Implementation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Deadline Propagation</strong></td>
      <td>Orphan computation and zombie processing when client has already disconnected.</td>
      <td><code>grpc-timeout</code> header, <code>context.WithTimeout</code>, propagation across hops.</td>
      <td>Downstream calls fail early if upstream hops consume too much budget.</td>
      <td>Cloud Run Request Timeout, gRPC deadline headers, Cloud Tasks dispatch deadlines.</td>
    </tr>
    <tr>
      <td><strong>Exponential Backoff + Full Jitter</strong></td>
      <td>Thundering herd and retry resonance spikes synchronizing against recovering services.</td>
      <td><code>base_delay = 100ms</code>, <code>max_delay = 10s</code>, <code>sleep = random(0, min(max, base * 2^attempt))</code>.</td>
      <td>Increases p99 latency for failing requests while protecting downstream servers.</td>
      <td>Google Cloud Client Libraries default retry policy, Cloud Pub/Sub subscriber backoff.</td>
    </tr>
    <tr>
      <td><strong>Circuit Breaker</strong></td>
      <td>Cascading thread starvation and resource exhaustion from repeatedly calling a dead service.</td>
      <td>Consecutive errors (5), failure rate threshold (50%), ejection duration (30s).</td>
      <td>Rejects requests immediately during outage; requires fallback or caching.</td>
      <td>Cloud Service Mesh (Envoy Outlier Detection), Cloud Armor rate limiting, App Gateway.</td>
    </tr>
    <tr>
      <td><strong>Bulkhead Isolation</strong></td>
      <td>One degraded microservice exhausting global shared thread or connection pools.</td>
      <td>Max concurrent calls per service, separate connection pools, memory limits.</td>
      <td>Unused capacity in Pool A cannot be borrowed by surging Pool B.</td>
      <td>GKE Pod Disruption Budgets &amp; Resource Quotas, Cloud Run Concurrency per instance.</td>
    </tr>
    <tr>
      <td><strong>Idempotency Key</strong></td>
      <td>Duplicate state mutations, repeated credit card charges, or multiple order fulfillments.</td>
      <td><code>Idempotency-Key</code> UUID v4, atomic Redis SETNX or Spanner conditional commit.</td>
      <td>Requires stateful fast cache lookup and strict TTL retention management.</td>
      <td>Memorystore for Redis atomic locking, Cloud Spanner transaction keys, Cloud Tasks de-duplication.</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 85: Distributed Deadline Budget and Circuit Breaker State Transition",
        "desc": "Flow tracing deadline budget depletion across hops and the three-state circuit breaker cycle (Closed, Open, Half-Open).",
        "caption": "Figure 85.1: Request lifecycle showing hop-by-hop deadline propagation and circuit breaker fault isolation.",
        "nodes": [
            ("1. Client Ingress", "Total Budget: 2,500ms\\nIdempotency Key Header"),
            ("2. Gateway Hop", "Hop Latency: 150ms\\nRemaining Budget: 2,350ms"),
            ("3. Circuit Breaker", "Closed -> Open on 50% 5xx\\nImmediate Fast Rejection"),
            ("4. Backend Service", "Exceeds Remaining Budget?\\nAbort Work If Deadline Passed"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Timeout budgets, bounded retries with jitter, idempotency, and circuit breakers",
            "preview": (
                "A transient 500ms database hiccup causes thousands of mobile apps to retry simultaneously without backoff. "
                "The retry storm multiplies traffic by 450%, overwhelming the database connection pool and turning a 5-second glitch into a 45-minute outage."
            ),
            "overview": (
                "Modern cloud resilience relies on defensive communication protocols between distributed microservices. "
                "A **deadline budget** assigns an immutable maximum duration to an end-to-end user transaction; each downstream hop decrements "
                "its local processing time and passes the remaining budget forward, aborting immediately if insufficient time remains. "
                "**Bounded retries with exponential backoff and decorrelated jitter** prevent 'thundering herd' synchronization by spreading retry "
                "attempts across randomized time distributions. To ensure retries never cause duplicate side effects (such as charging a customer twice "
                "or dispatching two delivery trucks for one purchase), systems enforce strict **idempotency keys** using atomic distributed locks. "
                "Finally, **circuit breakers** and **bulkheads** detect downstream degradation and fast-fail subsequent requests, preventing thread starvation "
                "from spreading upstream."
            ),
            "technical": (
                "Resilience mechanics must follow rigorous algorithmic implementations:\n\n"
                "### 1. Bounded Exponential Backoff with Full Jitter\n"
                "Without jitter, all clients that fail simultaneously at $t_0$ retry simultaneously at $t_0 + 2^k$, creating periodic resonance spikes. "
                "The **Full Jitter** algorithm completely randomizes sleep time between zero and the exponential ceiling:\n"
                "$$t_{\\text{temp}} = \\min(T_{\\text{max}}, T_{\\text{base}} \\times 2^{\\text{attempt}})$$\n"
                "$$t_{\\text{sleep}} = \\text{UniformRandom}(0, t_{\\text{temp}})$$\n"
                "This guarantees that retries are uniformly distributed across the timeline, flattening traffic spikes.\n\n"
                "### 2. End-to-End Deadline Propagation\n"
                "In a synchronous chain $A \\to B \\to C$, if Client $A$ sets a deadline of 2,000ms and Gateway $B$ consumes 1,200ms processing business rules, "
                "the call to Service $C$ must carry a deadline of at most 800ms. If Service $C$ estimates its database query will take 1,000ms, it must "
                "abort immediately without issuing the query. Proceeding with the query creates **zombie work** that consumes database CPU while the client "
                "has already timed out and disconnected.\n\n"
                "### 3. Distributed Idempotency and Single-Fulfillment\n"
                "To uphold the inviolable Day 64 single-fulfillment invariant, mutative endpoints (`POST /orders`) require an `Idempotency-Key` header:\n"
                "1. Check distributed cache (Memorystore Redis) using atomic `SET key status NX EX 86400`.\n"
                "2. If key exists and status is `COMPLETED`, return the cached response immediately without re-executing logic.\n"
                "3. If key exists and status is `PROCESSING`, return HTTP 409 Conflict or block until completion.\n"
                "4. If key is new, execute transaction, store result in cache, and commit."
            ),
            "questions": [
                "Why is 'Full Jitter' mathematically superior to 'Equal Jitter' in reducing downstream server queue depth during a retry storm?",
                "How does gRPC deadline propagation automatically cancel in-flight database queries when a client drops its connection?",
                "What failure scenario occurs if an idempotency key cache has a shorter TTL than the maximum client retry window?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/control-plane-data-plane",
            "reference_label": "Google Cloud Architecture Framework: Managing retries, timeouts, and cascading failures",
            "scenario": {
                "symptom": (
                    "During morning rush, Brightloaf's payment authorization service experienced a minor 1.2-second network latency spike. "
                    "Within 15 seconds, the entire order API collapsed with 100% CPU utilization, and 12,000 customers were charged twice "
                    "for single bread orders."
                ),
                "constraints": (
                    "Must strictly preserve the single-fulfillment invariant, limit total payment retry attempts to at most 1, and ensure end-to-end checkout completes within 3.0 seconds."
                ),
                "evidence": (
                    "Application logs show mobile clients retrying failed `POST /orders` calls every 200ms without backoff or jitter. "
                    "Backend logs show identical order payloads being processed concurrently by multiple worker threads due to missing idempotency checks."
                ),
                "diagnostic_steps": [
                    "Inspect Cloud Monitoring metric `loadbalancing.googleapis.com/https/request_count` grouped by response code (spike in 504 Gateway Timeout).",
                    "Analyze database transaction query logs for duplicate `INSERT INTO order_payments` with identical customer and cart IDs.",
                    "Verify client retry headers to confirm lack of backoff delays and missing idempotency tokens.",
                ],
                "root": (
                    "Clients executed aggressive fixed-interval retries without exponential backoff, jitter, or idempotency keys, converting a transient 1.2s delay "
                    "into a massive retry storm that caused duplicate financial charges and database connection exhaustion."
                ),
                "fix": (
                    "Implement server-enforced idempotency keys stored in Memorystore Redis with atomic locking, enforce a maximum of 1 retry with Full Jitter, "
                    "and inject gRPC deadline propagation across all microservice hops."
                ),
                "verify": (
                    "Simulate 500 duplicate concurrent `POST /orders` requests with identical idempotency keys; verify exactly one charge succeeds, "
                    "499 requests receive the cached successful confirmation, and zero duplicate fulfillments occur."
                ),
                "residual": (
                    "Redis cache failure could temporarily disable idempotency validation; requires fallback to relational database unique constraint indexes."
                ),
                "diagram": (
                    "1.2s payment delay",
                    "Unjittered client retries",
                    "Duplicate charges executed",
                    "Redis atomic idempotency",
                    "Single charge preserved"
                ),
                "facts": "12,000 customers charged twice due to unjittered client retries hitting non-idempotent payment handlers.",
                "inference": "Any mutative endpoint without an idempotency key guarantees data corruption during network latency events.",
                "expected": "Idempotency layer filters duplicate retries, returning cached success without re-executing payment mutations."
            },
            "lab": {
                "name": "Exponential Backoff, Full Jitter, and Idempotency Simulator",
                "file": "day-085-topic-01-retry-jitter.py",
                "goal": "Author and execute a Python simulation demonstrating exponential backoff with full jitter and atomic idempotency key validation.",
                "expected": "Runnable script demonstrating uniformly distributed retry timing and 100% prevention of duplicate order fulfillments under high concurrency.",
                "mode": "local script execution",
                "prereq": "Python 3.10+ installed.",
                "preflight": "Verify Python runtime and initialize simulation workspace.",
                "steps": [
                    "Author the retry jitter and idempotency engine:\n\n```sh\ncat <<'EOF' > day-085-topic-01-retry-jitter.py\n#!/usr/bin/env python3\n\"\"\"Exponential Backoff with Full Jitter & Idempotency Key Simulator.\"\"\"\nimport random\nimport time\n\ndef full_jitter_backoff(attempt, base=0.1, cap=5.0):\n    # Full Jitter: Sleep = UniformRandom(0, min(cap, base * 2^attempt))\n    temp = min(cap, base * (2 ** attempt))\n    return random.uniform(0, temp)\n\nprint(\"1. Full Jitter Timing Distribution (5 Attempts, 5 Simulated Clients):\")\nprint(\"-\" * 70)\nprint(f\"{'Client':<10} | {'Attempt 1':<10} | {'Attempt 2':<10} | {'Attempt 3':<10} | {'Attempt 4':<10}\")\nprint(\"-\" * 70)\nfor c in range(1, 6):\n    delays = [f\"{full_jitter_backoff(a):.3f}s\" for a in range(1, 5)]\n    print(f\"Client {c:<3} | {delays[0]:<10} | {delays[1]:<10} | {delays[2]:<10} | {delays[3]:<10}\")\n\nprint(\"\\n2. Idempotency Key Processing Simulation:\")\nprint(\"-\" * 70)\n\n# Simulated distributed cache (Redis SETNX mock)\nidempotency_cache = {}\n\ndef process_order(idempotency_key, order_id, amount):\n    if idempotency_key in idempotency_cache:\n        cached_entry = idempotency_cache[idempotency_key]\n        return f\"CACHED HIT: Order {cached_entry['order_id']} already processed! Amount: ${cached_entry['amount']:.2f}\", False\n    \n    # Atomic write (SETNX)\n    idempotency_cache[idempotency_key] = {'order_id': order_id, 'amount': amount, 'time': time.time()}\n    return f\"MUTATION EXECUTED: Order {order_id} charged ${amount:.2f}\", True\n\n# Simulate 4 identical retries from Client 1\nkey = \"uuid-8f92-order-9941\"\nexecutions = 0\nfor i in range(1, 5):\n    result, mutated = process_order(key, \"ORD-9941\", 42.50)\n    if mutated: executions += 1\n    print(f\"Retry {i}: {result}\")\n\nprint(\"-\" * 70)\nprint(f\"Total Executions Mutated: {executions} (Invariant: MUST BE EXACTLY 1)\")\nassert executions == 1, \"VIOLATION: Single-fulfillment invariant broken!\"\nprint(\"VERIFIED: Single-fulfillment invariant preserved successfully.\")\nEOF\npython3 day-085-topic-01-retry-jitter.py\n```",
                    "Run the script and verify that retries across different clients do not synchronize into identical timestamps.",
                    "Verify that the idempotency check guarantees exactly 1 mutation despite 4 aggressive retry attempts.",
                    "Save the simulation script and output in your evidence repository."
                ],
                "verification": (
                    "Script executes without error, demonstrates non-synchronized jitter delays, and passes the single-fulfillment assertion."
                ),
                "trouble": "Ensure `random.uniform` covers the full range from 0 to the calculated exponential ceiling.",
                "cleanup": "Retain `day-085-topic-01-retry-jitter.py` as an exit evidence artifact.",
                "accept": "Validated implementation of Full Jitter retry backoff and atomic idempotency key filtering."
            }
        },
        {
            "key": "topic-02",
            "title": "Distinguishing measured from forecast throughput and Little's Law",
            "preview": (
                "An engineering team sizes their cluster based on a vendor benchmark claiming '10,000 transactions/second on 8 vCPUs.' "
                "In production, under actual database row-locking contention, the system chokes at 850 QPS, with p99 latency exploding from 15ms to 12,000ms."
            ),
            "overview": (
                "A foundational duty of cloud architecture is strictly distinguishing between **measured throughput** and **forecast throughput**. "
                "Forecast throughput is a theoretical mathematical model, marketing benchmark, or business projection representing how much load "
                "the business hopes or expects to receive. In contrast, measured throughput is empirical telemetry gathered under realistic production "
                "conditions with real network latency, serialization overhead, lock contention, and downstream dependencies. "
                "Applying **Little's Law** ($L = \\lambda W$) reveals why systems cannot scale linearly up to 100% capacity: as utilization exceeds 80%, "
                "queuing delay explodes asymptotically towards infinity. Architects must establish strict **retry budgets** (capping retries at "
                "no more than 10% of total incoming traffic) to prevent forecast models from collapsing under actual operational dynamics."
            ),
            "technical": (
                "Queuing dynamics and capacity modeling must be grounded in mathematical queuing theory:\n\n"
                "### 1. Little's Law and System Concurrency\n"
                "In any stable queuing system, the average number of concurrent requests ($L$) equals the arrival rate ($\\lambda$) multiplied by the average time spent in the system ($W$):\n"
                "$$L = \\lambda \\times W$$\n"
                "- If arrival rate $\\lambda = 1,000$ req/sec and service latency $W = 0.050$ seconds (50ms), average concurrency $L = 50$ requests.\n"
                "- If downstream database contention increases $W$ to 2.0 seconds, concurrency $L$ explodes to **2,000 concurrent requests**!\n"
                "- Unless the web server has 2,000 worker threads pre-allocated, request queues overflow and the server crashes from thread starvation.\n\n"
                "### 2. Kingman's Formula and The 80% Utilization Cliff\n"
                "The wait time in queue ($W_q$) for an M/M/1 queue is governed by utilization ($\\rho = \\lambda / \\mu$):\n"
                "$$W_q = \\frac{\\rho}{1 - \\rho} \\times \\frac{1}{\\mu}$$\n"
                "As utilization $\\rho$ approaches 1.0 (100%), the term $(1 - \\rho)$ approaches zero, driving queue wait times to infinity. "
                "At 50% utilization, queue factor is $0.5 / 0.5 = 1$. At 90% utilization, queue factor explodes to $0.9 / 0.1 = 9$ (9x latency increase)! "
                "Architects must size systems so sustained traffic never exceeds 70-80% of measured maximum throughput.\n\n"
                "### 3. The 10% Global Retry Budget\n"
                "To prevent retry storms from exacerbating queuing delays, Google Cloud SRE enforces a strict **Retry Budget**: clients may only retry "
                "if the ratio of retries to total requests over a rolling 1-minute window remains below 10%. If retries exceed 10%, the client library "
                "fast-fails the request immediately without hitting the network."
            ),
            "questions": [
                "How does Little's Law demonstrate that a 10x increase in backend latency causes an identical 10x explosion in web server concurrency?",
                "Why does operating a database at 95% CPU utilization cause non-linear latency spikes compared to operating at 70% CPU?",
                "What is the mathematical rationale behind capping client retry budgets at 10% of total requests?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/capacity-planning",
            "reference_label": "Google Cloud Architecture Framework: Capacity planning, queuing, and overload control",
            "scenario": {
                "symptom": (
                    "Brightloaf planned for a 5,000 QPS flash sale based on a load test run against mock in-memory stubs. "
                    "In production, when traffic reached 2,200 QPS, backend latency surged from 25ms to 8,400ms, and the GKE ingress "
                    "load balancer began shedding 60% of connections."
                ),
                "constraints": (
                    "Must maintain p95 latency below 200ms for active checkouts; cannot exceed existing Cloud SQL vCPU quotas during the sale."
                ),
                "evidence": (
                    "Cloud SQL CPU utilization crossed 88% at 2,100 QPS. At 88% utilization, PostgreSQL lock contention on the central `inventory` table "
                    "caused average query duration to spike 28x, confirming Kingman's formula queue explosion."
                ),
                "diagnostic_steps": [
                    "Compare staging load test methodology (mock stubs) against production architecture (relational transactional database).",
                    "Plot Cloud SQL CPU utilization against p99 latency to identify the empirical inflection point (the 80% saturation cliff).",
                    "Calculate observed concurrency using Little's Law ($L = \\lambda W$) during normal vs degraded periods.",
                ],
                "root": (
                    "Capacity planning relied on synthetic forecast throughput from mock stubs that ignored database locking overhead; "
                    "operating the relational database past 80% utilization triggered exponential queuing latency."
                ),
                "fix": (
                    "Re-benchmark system using realistic production transactional data to establish measured capacity (safe limit: 1,800 QPS), "
                    "enforce ingress rate limiting at 1,750 QPS, and partition hot inventory rows across 16 shards to eliminate lock serialization."
                ),
                "verify": (
                    "Run dark traffic replay at 2,500 QPS against partitioned database in staging; verify CPU remains below 72% and p95 latency stays under 85ms."
                ),
                "residual": (
                    "Inventory sharding introduces eventual consistency across regional bakery outlets, requiring reconciliation batch jobs."
                ),
                "diagram": (
                    "Forecast: 5k QPS mock",
                    "Prod 88% DB lock hit",
                    "Latency surges to 8.4s",
                    "Sharded inventory rows",
                    "Sub-85ms at 2.5k QPS"
                ),
                "facts": "System collapsed at 2,200 QPS despite forecast model predicting 5,000 QPS capacity.",
                "inference": "Synthetic benchmarks without persistent state locking are completely useless for capacity planning.",
                "expected": "Measured throughput establishes hard operational ceilings enforced by edge rate limiters."
            },
            "lab": {
                "name": "Little's Law and Retry Amplification Budget Simulator",
                "file": "day-085-topic-02-littles-law.py",
                "goal": "Write and execute a Python simulation demonstrating Little's Law, queue explosion under high utilization, and retry budget enforcement.",
                "expected": "A runnable script demonstrating non-linear latency curves as utilization passes 80% and verifying that a 10% retry budget halts cascading overload.",
                "mode": "local script execution",
                "prereq": "Completion of Exercise 1.",
                "preflight": "Verify Python runtime and initialize script file.",
                "steps": [
                    "Author the Little's Law and retry budget script:\n\n```sh\ncat <<'EOF' > day-085-topic-02-littles-law.py\n#!/usr/bin/env python3\n\"\"\"Little's Law and Retry Budget Amplification Simulator.\"\"\"\n\n# 1. Little's Law Demonstration: Concurrency = Arrival Rate * Latency\nprint(\"1. Little's Law Concurrency Analysis (L = λ * W):\")\nprint(\"-\" * 70)\narrival_rate = 1000  # 1,000 requests/sec\nlatencies = [0.020, 0.050, 0.100, 0.500, 1.000, 2.500]  # Latency from 20ms to 2.5s\n\nprint(f\"{'Arrival Rate (λ)':<18} | {'Latency (W)':<15} | {'Required Concurrency (L)':<25}\")\nprint(\"-\" * 70)\nfor w in latencies:\n    l = arrival_rate * w\n    print(f\"{arrival_rate:<18} req/s | {w*1000:<10.0f} ms | {l:<25.1f} active threads\")\n\n# 2. Kingman's Queuing Cliff: Wait Time factor = rho / (1 - rho)\nprint(\"\\n2. Queuing Delay Explosion as Utilization (ρ) Approaches 100%:\")\nprint(\"-\" * 70)\nprint(f\"{'Utilization (ρ)':<18} | {'Queue Wait Factor (ρ / (1-ρ))':<30} | {'Status':<15}\")\nprint(\"-\" * 70)\nfor rho in [0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95, 0.98]:\n    factor = rho / (1.0 - rho)\n    status = \"SAFE\" if rho <= 0.75 else (\"WARNING\" if rho <= 0.85 else \"COLLAPSE\")\n    print(f\"{rho*100:<17.0f}% | {factor:<30.2f}x | {status:<15}\")\n\n# 3. 10% Global Retry Budget Enforcement\nprint(\"\\n3. Global Retry Budget Enforcement (Max 10% Retries):\")\nprint(\"-\" * 70)\ntotal_requests = 10000\nfailed_requests = 1500  # 15% backend failure rate\n\n# Without Retry Budget: All 1,500 fail and retry -> Amplification!\nretries_without_budget = failed_requests\n\n# With SRE 10% Retry Budget: Max permitted retries = 10% of total requests\nmax_permitted_retries = int(total_requests * 0.10)\nallowed_retries = min(failed_requests, max_permitted_retries)\nshed_retries = failed_requests - allowed_retries\n\nprint(f\"Total Initial Requests:     {total_requests}\")\nprint(f\"Initial Backend Failures:   {failed_requests}\")\nprint(f\"Retries Without Budget:     {retries_without_budget} (Full 15% amplification)\")\nprint(f\"Retries Allowed by Budget:  {allowed_retries} (Capped at exactly 10%)\")\nprint(f\"Retries Shed at Client:     {shed_retries} (Prevented retry storm)\")\nEOF\npython3 day-085-topic-02-littles-law.py\n```",
                    "Execute the script and verify that latency wait times explode by 9x at 90% utilization and 19x at 95% utilization.",
                    "Verify that the 10% retry budget caps downstream traffic amplification, protecting the backend from runaway collapse.",
                    "Save the script and analysis as exit evidence."
                ],
                "verification": (
                    "Script runs cleanly, displays accurate concurrency scaling according to Little's Law, and demonstrates retry budget shedding."
                ),
                "trouble": "Ensure utilization `rho` remains strictly less than 1.0 to avoid division by zero.",
                "cleanup": "Retain `day-085-topic-02-littles-law.py` as an exit evidence artifact.",
                "accept": "Mastery of Little's Law, queuing saturation cliffs, and client-side retry budget controls."
            }
        }
    ]
}
