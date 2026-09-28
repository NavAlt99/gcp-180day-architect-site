"""day_data_083.py — Exhaustive architecture data specification for Day 83.

Covers Availability Math and Dependency Risk:
1. Availability math (99.9% vs 99.95% vs 99.99% downtime calculations, formulas, error budget allocation).
2. Series vs parallel availability (composite SLA calculation, multiplication rule, independence assumptions, correlated failures).
3. Single points of failure (layer-by-layer SPOF identification and elimination across DNS, Network, Compute, Data, and IAM).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 83

DATA = {
    "day": 83,
    "part1_intro": (
        "Day 83 initiates Block 4 (Reliability and Security) by establishing the quantitative mathematical foundations "
        "of enterprise cloud availability. Architects cannot design resilient systems through intuition alone; they must "
        "calculate exact downtime budgets across 99.9%, 99.95%, and 99.99% targets, model compound availability across series "
        "and parallel dependencies, and rigorously challenge the naive assumption of component failure independence. A system "
        "composed of ten 99.9% reliable microservices in series yields an abysmal composite availability of only 99.0%, consuming "
        "over 430 minutes of downtime per month. Today's curriculum deconstructs the mathematical reality of composite SLAs, "
        "uncovers hidden correlated failure modes such as shared control planes and DNS resolution, and audits infrastructure "
        "layer-by-layer to systematically eliminate single points of failure (SPOFs) across the Brightloaf enterprise stack."
    ),
    "exit_summary": (
        "Calculated exact allowed downtime budgets across 99.9%, 99.95%, and 99.99% tiers; modeled series and parallel composite "
        "SLAs across Brightloaf's order-processing topology demonstrating a drop from 99.9% to 99.75% composite availability; "
        "identified five critical correlated failure domains (shared IAM, regional DNS, Cloud NAT port exhaustion, zonal power, "
        "and centralized database lock contention) that invalidate naive multiplication; eliminated four critical SPOFs across "
        "network, compute, and database tiers with verified multi-zone and HA configurations."
    ),
    "part2_intro": (
        "Availability is an engineering discipline governed by probability theory and discrete mathematics. The sections below "
        "detail availability calculations, compound dependency equations, failure correlation risks, and systematic SPOF "
        "elimination techniques across Google Cloud infrastructure."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Availability Tier</th>
      <th>Downtime / Month (30d)</th>
      <th>Downtime / Year (365d)</th>
      <th>Permitted Continuous Outage</th>
      <th>Architectural Requirements &amp; Google Cloud Pattern</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>99.0% ("Two 9s")</strong></td>
      <td>7 hours, 12 minutes</td>
      <td>3.65 days (87.6 hours)</td>
      <td>Hours (manual intervention acceptable)</td>
      <td>Single VM instance, standard persistent disk, daily snapshots, cold restore.</td>
    </tr>
    <tr>
      <td><strong>99.9% ("Three 9s")</strong></td>
      <td>43 minutes, 12 seconds</td>
      <td>8 hours, 45 minutes, 57 seconds</td>
      <td>Tens of minutes (automated restart)</td>
      <td>Regional Managed Instance Group (MIG), autohealing health checks, Cloud SQL single-zone with automated failover replication.</td>
    </tr>
    <tr>
      <td><strong>99.95% ("Three and a half 9s")</strong></td>
      <td>21 minutes, 36 seconds</td>
      <td>4 hours, 22 minutes, 58 seconds</td>
      <td>Minutes (sub-minute automated failover)</td>
      <td>Multi-zone Regional MIG across 3 AZs, Cloud SQL HA with Regional PD synchronous replication, Anycast External HTTP(S) Load Balancer.</td>
    </tr>
    <tr>
      <td><strong>99.99% ("Four 9s")</strong></td>
      <td>4 minutes, 19 seconds</td>
      <td>52 minutes, 36 seconds</td>
      <td>Seconds (instantaneous routing shift)</td>
      <td>Multi-region Cloud Spanner, multi-region Cloud Storage, dual-region active/active Cloud Run, Anycast global load balancing with backend health checks.</td>
    </tr>
    <tr>
      <td><strong>99.999% ("Five 9s")</strong></td>
      <td>25.9 seconds</td>
      <td>5 minutes, 15 seconds</td>
      <td>Sub-second (zero perceptible human downtime)</td>
      <td>Distributed active-active multi-region Spanner, multi-region routing with Anycast BGP, zero-downtime canary pipelines, positive fencing.</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 83: Enterprise Availability and Dependency Topology Flow",
        "desc": "Flow tracing request traversal through edge Anycast, compute tiers, data persistence, and dependency evaluation.",
        "caption": "Figure 83.1: Composite availability flow showing series multiplication risks and parallel redundancy mitigation.",
        "nodes": [
            ("1. Global Edge (99.99%)", "Anycast GCLB + Cloud Armor\\nParallel Multi-Region Entry"),
            ("2. App Tiers (99.95%)", "Regional MIG / GKE Multi-Zone\\nAutoscaled Stateless Workers"),
            ("3. Persistence (99.95%)", "Cloud SQL HA / Spanner\\nSync Regional Replication"),
            ("4. Composite Risk", "Series Product: 99.89%\\nCorrelated Dependency Audit"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Availability math: downtime budgets and error allocation",
            "preview": (
                "An e-commerce team commits to a 99.99% SLA without calculating that it permits only 4 minutes and 19 seconds of downtime per month. "
                "When a routine database restart takes 12 minutes, the entire quarterly SLA penalty is triggered, costing thousands in customer service credits."
            ),
            "overview": (
                "Availability math defines the exact quantitative limits of permitted service degradation over standardized time windows. "
                "Formally, availability is the ratio of operational uptime to total scheduled time: A = Uptime / (Uptime + Downtime). "
                "In modern SRE practice, availability is measured via request-based Service Level Indicators (SLIs): the percentage of valid requests "
                "served successfully within latency thresholds. Each target tier dictates a strict, non-negotiable downtime budget: 99.9% permits 43.2 minutes/month, "
                "99.95% permits 21.6 minutes/month, and 99.99% permits a razor-thin 4.32 minutes/month. Understanding this math prevents engineering teams "
                "from signing contractual SLAs that are mathematically impossible to maintain given the underlying infrastructure building blocks."
            ),
            "technical": (
                "Availability calculations must adhere to strict probabilistic and operational formulas:\n\n"
                "### 1. Fundamental Formulas and Downtime Conversion\n"
                "- **Allowed Downtime ($D$):** For time window $T$ (where $T_{\\text{month}} = 30 \\times 24 \\times 3600 = 2,592,000$ seconds, and $T_{\\text{year}} = 31,536,000$ seconds):\n"
                "  $$D = T \\times (1 - A)$$\n"
                "- **Request-Based Availability ($A_{\\text{req}}$):**\n"
                "  $$A_{\\text{req}} = \\frac{\\sum \\text{Successful Requests}}{\\sum \\text{Total Valid Requests}} \\ge \\text{SLO}$$\n\n"
                "### 2. Time-Based vs. Event-Based Discrepancies\n"
                "Time-based availability measures whether the system socket is listening. Event-based availability measures whether user transactions "
                "complete successfully. A service can be 100% available by time-based ping probes while failing 100% of user checkouts due to database lock exhaustion. "
                "Architects must always align contractual SLAs and internal SLOs with user-visible transaction success.\n\n"
                "### 3. The Exponential Cost Curve\n"
                "Moving from 99.9% to 99.99% does not require a 10% increase in engineering effort; it requires a 10x reduction in failure tolerance. "
                "At 99.9%, human incident response (15-minute MTTA + 15-minute MTTR) can preserve the SLA. At 99.99%, any human intervention guarantees SLA breach; "
                "all failure detection, isolation, draining, and failover must be 100% automated within seconds."
            ),
            "questions": [
                "How does the allowed downtime budget change between a 30-day calendar month and a rolling 28-day window?",
                "Why does human Mean Time to Acknowledge (MTTA) make a 99.99% SLA impossible without fully automated control loops?",
                "What specific transaction exclusions (e.g., client 4xx errors, scheduled maintenance) must be codified in contract terms?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/availability",
            "reference_label": "Google Cloud Architecture Framework: Availability and downtime calculations",
            "scenario": {
                "symptom": (
                    "Brightloaf committed to a contractual 99.99% availability SLA for its B2B Wholesale Ordering API. During a monthly release, "
                    "a database schema migration lock blocked HTTP POST /orders for 8 minutes and 42 seconds. Although the service was available for 99.98% "
                    "of the month, the 4.32-minute allowed downtime was doubled, triggering a mandatory 25% billing refund to enterprise customers."
                ),
                "constraints": (
                    "Must preserve data integrity (zero duplicate orders), honor third-party ERP payment timeouts (max 5s), and avoid manual failovers "
                    "that exceed the 4.32-minute monthly budget."
                ),
                "evidence": (
                    "Cloud Monitoring shows 502/504 spikes between 02:14:10 UTC and 02:22:52 UTC (522 seconds total). Total monthly orders: 1,420,000; "
                    "failed orders: 18,400. Measured request availability: 98.70% during the incident window, dragging monthly availability to 99.980%."
                ),
                "diagnostic_steps": [
                    "Inspect Cloud Load Balancing request logs filtered by `statusDetails='backend_timeout'`.",
                    "Correlate Cloud SQL `query_exec_time` and table lock waits on `orders` during the DDL migration.",
                    "Review Cloud Monitoring SLO error budget burn rate graph to determine the exact moment the monthly budget was depleted.",
                ],
                "root": (
                    "Schema migration executed an exclusive `ALTER TABLE` lock on the transactional database, exceeding the entire 99.99% monthly "
                    "downtime budget in a single operation without an automated zero-downtime schema rollout pattern."
                ),
                "fix": (
                    "Adopt an online schema migration pattern with Ghost/Liquibase (expand/contract), deploy Cloud Spanner with non-blocking schema updates, "
                    "and recalibrate public SLA terms to 99.95% while keeping internal 99.9% SLO with automated rollback within 60 seconds."
                ),
                "verify": (
                    "Execute non-blocking DDL rehearsal in staging; verify Cloud Monitoring records zero HTTP 5xx errors and query latency remains below 45ms."
                ),
                "residual": (
                    "Spanner online schema changes take longer to propagate across regions (up to several minutes) during which write throughput may be throttled."
                ),
                "diagram": (
                    "DDL lock triggered",
                    "Table exclusive lock",
                    "522s downtime breach",
                    "Expand/contract schema",
                    "Zero-downtime deploy"
                ),
                "facts": "Measured outage: 522 seconds. 99.99% monthly limit: 259.2 seconds. Public SLA breached by 262.8 seconds.",
                "inference": "Human-driven migrations cannot support four-nines SLAs without architectural isolation.",
                "expected": "Future schema updates execute concurrently with active transactions without taking exclusive table locks."
            },
            "lab": {
                "name": "Downtime Budget and Error Allocation Engine",
                "file": "day-083-topic-01-downtime.py",
                "goal": "Write and execute an automated downtime budget calculation tool in Python that computes exact SLA windows and error budgets.",
                "expected": "Accurate, formatted table output showing monthly and yearly allowed downtime across multiple tiers, with budget burn simulations.",
                "mode": "local script execution",
                "prereq": "Python 3.10+ installed locally.",
                "preflight": "Verify Python runtime and create exercise file.",
                "steps": [
                    "Open terminal and initialize workspace script:\n\n```sh\ncat <<'EOF' > day-083-topic-01-downtime.py\n#!/usr/bin/env python3\n\"\"\"Automated Availability and Downtime Calculator.\"\"\"\ndef calculate_downtime(sla_percent):\n    month_sec = 30 * 24 * 3600\n    year_sec = 365 * 24 * 3600\n    unavail = (100.0 - sla_percent) / 100.0\n    \n    m_down = month_sec * unavail\n    y_down = year_sec * unavail\n    \n    def fmt(sec):\n        d = int(sec // 86400)\n        sec %= 86400\n        h = int(sec // 3600)\n        sec %= 3600\n        m = int(sec // 60)\n        s = sec % 60\n        parts = []\n        if d > 0: parts.append(f\"{d}d\")\n        if h > 0: parts.append(f\"{h}h\")\n        if m > 0: parts.append(f\"{m}m\")\n        parts.append(f\"{s:.1f}s\")\n        return \" \".join(parts)\n    \n    return fmt(m_down), fmt(y_down)\n\nprint(f\"{'SLA Tier':<10} | {'Monthly Allowed Downtime':<25} | {'Yearly Allowed Downtime':<25}\")\nprint(\"-\" * 66)\nfor sla in [99.0, 99.5, 99.9, 99.95, 99.99, 99.999]:\n    m, y = calculate_downtime(sla)\n    print(f\"{sla:<10.3f}% | {m:<25} | {y:<25}\")\nEOF\npython3 day-083-topic-01-downtime.py\n```",
                    "Verify the generated output matches expected theoretical values: 99.9% is ~43m 12s/month; 99.99% is ~4m 19.2s/month.",
                    "Extend the script to simulate a 5-minute outage and report percentage of monthly error budget consumed for each tier.",
                    "Record the output in your learning log and note why four-nines requires sub-minute automated detection."
                ],
                "verification": (
                    "Confirm script output reports exactly 43m 12.0s for 99.9% monthly, and 4m 19.2s for 99.99% monthly downtime."
                ),
                "trouble": "Ensure floating point precision errors are minimized by formatting seconds to 1 decimal place.",
                "cleanup": "Retain `day-083-topic-01-downtime.py` as an exit evidence artifact.",
                "accept": "Script runs cleanly and displays complete downtime matrix with error budget calculations."
            }
        },
        {
            "key": "topic-02",
            "title": "Series vs parallel availability and compound dependency risk",
            "preview": (
                "An architect chains a 99.99% load balancer, a 99.9% API gateway, three 99.9% microservices, and a 99.95% database in a synchronous call path. "
                "Instead of four nines, the resulting composite availability plummets to 99.65%, resulting in over 150 minutes of monthly downtime."
            ),
            "overview": (
                "Composite availability models how individual component reliability interacts across complex enterprise topologies. "
                "When components operate in series (where each component is strictly necessary for transaction completion), total availability is "
                "the mathematical product of their individual availabilities: A_series = A_1 * A_2 * ... * A_n. In contrast, parallel components "
                "(where redundant components provide active-active or active-passive backup) fail only when all instances fail simultaneously: "
                "A_parallel = 1 - ((1 - A_1) * (1 - A_2) * ... * (1 - A_n)). However, the foundational flaw in classical composite modeling is the "
                "assumption of independence. In cloud environments, components routinely share common failure domains—including regional VPC peering, "
                "IAM policy propagation, Cloud DNS resolution, and shared database locks—causing correlated catastrophic failures."
            ),
            "technical": (
                "Architects must master the mechanics of compound availability modeling and correlated risk:\n\n"
                "### 1. Mathematical Mechanics: Series Chaining\n"
                "For a synchronous call chain traversing $n$ components where each component must succeed:\n"
                "$$A_{\\text{series}} = \\prod_{i=1}^{n} A_i$$\n"
                "Example: A request traversing Cloud Armor (99.99%), GCLB (99.99%), Cloud Run (99.95%), GKE Service (99.9%), and Cloud SQL (99.95%):\n"
                "$$A_{\\text{composite}} = 0.9999 \\times 0.9999 \\times 0.9995 \\times 0.9990 \\times 0.9995 = 0.997805 \\ (99.78\\%$$\n"
                "Monthly allowed downtime explodes from 4.3 minutes to **56.9 minutes**!\n\n"
                "### 2. Parallel Redundancy Mechanics\n"
                "For $m$ identical components running in parallel:\n"
                "$$A_{\\text{parallel}} = 1 - \\prod_{j=1}^{m} (1 - A_j)$$\n"
                "Two independent 99.9% application instances yield $1 - (0.001 \\times 0.001) = 0.999999$ (six 9s) on paper.\n\n"
                "### 3. The Fallacy of Independence & Correlated Failures\n"
                "Parallel components are almost never truly independent in Google Cloud:\n"
                "- **Shared Control Plane:** A misconfigured IAM role or org policy propagates to all instances simultaneously.\n"
                "- **Shared Routing:** Cloud Router BGP session flaps tear down routes to redundant backends.\n"
                "- **Shared Software Defect:** A poison pill payload causes all redundant instances to crash in parallel upon receipt.\n"
                "- **Database Concurrency:** Two parallel microservices serialize on the same primary database row locks, negating compute redundancy."
            ),
            "questions": [
                "Why does adding a synchronous third-party payment gateway with a 99.5% SLA cap your system's theoretical maximum availability at 99.5%?",
                "How does introducing an asynchronous message queue (e.g., Cloud Pub/Sub) decouple series dependencies into parallel availability paths?",
                "What are three specific examples of correlated failure modes that can take down multi-zone redundant deployments?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/design-for-reliability",
            "reference_label": "Google Cloud Reliability Framework: Designing for Redundancy and Decoupling",
            "scenario": {
                "symptom": (
                    "Brightloaf implemented a dual-zone frontend deployment across us-central1-a and us-central1-b expecting 99.999% availability. "
                    "During peak order traffic, an unexpected inventory database dead-lock caused both frontend pools to exhaust their connection pools "
                    "within 30 seconds, crashing all instances in both zones simultaneously."
                ),
                "constraints": (
                    "Must maintain single-fulfillment guarantee, enforce max 3-second user response time, and avoid unbudgeted multi-region database licensing costs."
                ),
                "evidence": (
                    "Cloud Monitoring shows connection pool saturation (100/100 active connections) across all 16 GKE pods in both zones. "
                    "CPU utilization on GKE nodes remained under 18%, while database transaction lock wait time spiked from 2ms to 45,000ms."
                ),
                "diagnostic_steps": [
                    "Query Cloud Monitoring for `kubernetes.io/container/cpu/utilization` vs `cloudsql.googleapis.com/database/postgresql/transaction_lock_wait_time`.",
                    "Examine application connection pool logs to verify thread starvation across both availability zones.",
                    "Audit the application call graph to identify synchronous blocking calls in the critical checkout path.",
                ],
                "root": (
                    "Naive parallel compute topology relied on a single shared transactional database locking mechanism, introducing an unhedged "
                    "series dependency that triggered correlated thread exhaustion across all compute instances."
                ),
                "fix": (
                    "Decouple the checkout path: acknowledge order receipt into Cloud Pub/Sub with local idempotency key, move inventory reconciliation "
                    "to an asynchronous worker queue, and enforce strict circuit breakers on synchronous database calls."
                ),
                "verify": (
                    "Simulate 5,000ms database lock in staging; verify frontend immediately shifts to asynchronous queuing mode, returns HTTP 202 Accepted, "
                    "and checkout availability remains 99.99% without container crashes."
                ),
                "residual": (
                    "Order confirmation becomes eventually consistent, requiring client-side polling or WebSocket push for final fulfillment status."
                ),
                "diagram": (
                    "Traffic surge arrives",
                    "Database lock wait",
                    "Dual-zone thread death",
                    "Asynchronous Pub/Sub outbox",
                    "Decoupled 202 Accepted"
                ),
                "facts": "Two zones of compute crashed concurrently despite 99.999% theoretical parallel availability math.",
                "inference": "Compute redundancy without state decoupling provides zero protection against downstream backend starvation.",
                "expected": "Compute instances survive database slowness by isolating critical user paths from synchronous write locks."
            },
            "lab": {
                "name": "Composite Topology SLA Modeler",
                "file": "day-083-topic-02-composite-sla.py",
                "goal": "Build an analytical tool that calculates composite SLAs for arbitrary series-parallel graphs and highlights correlated failure risks.",
                "expected": "A runnable Python model that outputs composite availability, total monthly downtime, and identified shared dependency choke points.",
                "mode": "local script execution",
                "prereq": "Completion of Exercise 1.",
                "preflight": "Verify Python runtime and initialize script template.",
                "steps": [
                    "Create the composite SLA modeling script:\n\n```sh\ncat <<'EOF' > day-083-topic-02-composite-sla.py\n#!/usr/bin/env python3\n\"\"\"Composite Topology SLA and Correlated Risk Analyzer.\"\"\"\n\ndef series_sla(*components):\n    prod = 1.0\n    for c in components:\n        prod *= (c / 100.0)\n    return prod * 100.0\n\ndef parallel_sla(*components):\n    unavail = 1.0\n    for c in components:\n        unavail *= (1.0 - (c / 100.0))\n    return (1.0 - unavail) * 100.0\n\n# Brightloaf Architecture Models\n# Path A: Naive Synchronous Series Chain\nedge_gclb = 99.99\napp_mesh = 99.90\nauth_svc = 99.95\norder_svc = 99.90\ndatabase = 99.95\n\ncomposite_a = series_sla(edge_gclb, app_mesh, auth_svc, order_svc, database)\nmonth_down_a = (30 * 24 * 60) * (1.0 - (composite_a / 100.0))\n\n# Path B: Resilient Decoupled Architecture with Parallel Redundancy\nredundant_app = parallel_sla(99.90, 99.90)\nasync_buffer = 99.95  # Pub/Sub buffer decoupling database\ncomposite_b = series_sla(edge_gclb, redundant_app, async_buffer)\nmonth_down_b = (30 * 24 * 60) * (1.0 - (composite_b / 100.0))\n\nprint(f\"Path A (Synchronous Series Chain):   {composite_a:.4f}% SLA | Monthly Downtime: {month_down_a:.2f} mins\")\nprint(f\"Path B (Decoupled Parallel Buffers): {composite_b:.4f}% SLA | Monthly Downtime: {month_down_b:.2f} mins\")\nprint(f\"Downtime Reduction Factor:           {month_down_a / month_down_b:.2f}x\")\nEOF\npython3 day-083-topic-02-composite-sla.py\n```",
                    "Run the script and verify that Path A yields ~99.69% (~133 min downtime/month) while Path B yields ~99.93% (~26 min downtime/month).",
                    "Document in your notes the five correlated failure modes that would cause Path B's redundant app tier to fail simultaneously.",
                    "Save the script and model outputs as day exit evidence."
                ],
                "verification": (
                    "Script executes successfully without syntax errors and prints comparative composite availability metrics showing >4x downtime reduction."
                ),
                "trouble": "Ensure percentage values are properly divided by 100 before performing floating point multiplication.",
                "cleanup": "Retain `day-083-topic-02-composite-sla.py` as an exit evidence artifact.",
                "accept": "Demonstrated mastery of compound availability math and identification of correlated failure mechanisms."
            }
        },
        {
            "key": "topic-03",
            "title": "Single points of failure: identification and layer-by-layer elimination",
            "preview": (
                "Brightloaf routes all ingress traffic through a single Cloud NAT gateway IP with default port allocation settings. "
                "During a Black Friday marketing push, SNAT port exhaustion drops 65% of outbound payment gateway connections, shutting down checkout across all regions."
            ),
            "overview": (
                "A Single Point of Failure (SPOF) is any individual component, configuration, or operational boundary whose failure directly induces total system collapse. "
                "SPOFs exist at every tier of the enterprise technology stack: physical infrastructure (single power supply, single rack, single AZ), network topology "
                "(single Cloud NAT, single HA VPN tunnel, unhedged interconnect), compute (standalone VM, zonal GKE master), data persistence (single-instance DB, unversioned bucket), "
                "and administrative control (single service account key, single project billing cap). True architectural resilience demands a disciplined, layer-by-layer audit "
                "methodology that uncovers hidden single points of failure and eliminates them through structural redundancy, automated health checking, and self-healing controls."
            ),
            "technical": (
                "Eliminating SPOFs requires systematic architectural hardening across five distinct infrastructure layers:\n\n"
                "### 1. Network Layer SPOFs & Remediation\n"
                "- **Cloud NAT Exhaustion:** A single NAT gateway allocating fixed 64 ports per VM will drop outbound connections under load. **Remediation:** Configure Dynamic Port Allocation (`--enable-dynamic-port-allocation`), multiple NAT IP addresses, and allocate minimum 256 ports per VM.\n"
                "- **Hybrid Interconnect:** A single Dedicated Interconnect link has a 99.9% SLA. **Remediation:** Deploy 99.99% topology requiring dual links across dual metropolitan availability zones with redundant Cloud Routers.\n\n"
                "### 2. Compute Layer SPOFs & Remediation\n"
                "- **Zonal VM Failure:** An unmanaged standalone Compute Engine VM dies on host hardware fault. **Remediation:** Regional Managed Instance Group (MIG) distributed across 3 zones with Autohealing (`--health-check`) and proactive instance repair.\n"
                "- **GKE Control Plane:** Single-zone GKE cluster control plane restarts during master upgrades. **Remediation:** Deploy GKE Regional Clusters where the Kubernetes control plane is replicated across three availability zones with a 99.95% SLA.\n\n"
                "### 3. Database & Storage Layer SPOFs & Remediation\n"
                "- **Zonal Cloud SQL:** Standalone Cloud SQL instance fails on zonal hypervisor crash. **Remediation:** Enable High Availability (HA) configuration using synchronous Regional Persistent Disk replication with automatic failover in <60 seconds.\n"
                "- **Object Storage:** A regional bucket in a single region is vulnerable to regional catastrophe. **Remediation:** Dual-Region or Multi-Region Cloud Storage buckets with Object Versioning and Turbo Replication (15-minute RPO guarantee).\n\n"
                "### 4. IAM & Governance SPOFs\n"
                "- **Hardcoded Long-Lived Keys:** A compromised or deleted Service Account JSON key invalidates all API traffic. **Remediation:** Workload Identity Federation, short-lived OAuth2 access tokens, and automated key rotation."
            ),
            "questions": [
                "What is the difference in SLA between a single-zone GKE cluster and a regional GKE cluster?",
                "How does Cloud SQL High Availability (HA) achieve failover without data loss compared to read replica promotion?",
                "Why does a Global External Application Load Balancer with Anycast IP eliminate external DNS routing SPOFs?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/eliminate-single-points-of-failure",
            "reference_label": "Google Cloud Architecture Framework: Identifying and eliminating single points of failure",
            "scenario": {
                "symptom": (
                    "During a high-volume promotion, Brightloaf's backend checkout workers began logging `Connection refused: connect` and `ETIMEDOUT` "
                    "when contacting the third-party credit card gateway. Compute Engine instances were healthy, but 70% of outbound transactions failed."
                ),
                "constraints": (
                    "Cannot bypass PCI-DSS compliance, must keep outbound traffic pinned to known static IP addresses for external firewall whitelisting."
                ),
                "evidence": (
                    "Cloud NAT metric `nat/dropped_sent_packets_count` spiked to 14,200 drops/min with reason `OUT_OF_RESOURCES`. "
                    "Only one static IP address was allocated, and each VM had exceeded its fixed 64-port ceiling."
                ),
                "diagnostic_steps": [
                    "Query Cloud Monitoring for `compute.googleapis.com/nat/nat_allocation_exhaustion`.",
                    "Inspect Cloud NAT gateway configuration via `gcloud compute routers nats describe`.",
                    "Review VM active TCP connections using `ss -s` on worker instances to confirm port starvation.",
                ],
                "root": (
                    "Cloud NAT gateway was configured with a single IP address and manual fixed port allocation of 64 ports per VM, creating an unmonitored "
                    "single point of failure that collapsed under high-concurrency outbound HTTPS traffic."
                ),
                "fix": (
                    "Assign four additional static IP addresses to the Cloud NAT gateway, enable Dynamic Port Allocation with a maximum of 1,024 ports per VM, "
                    "and establish Cloud Monitoring alerts for `nat/allocated_ports` utilization exceeding 75%."
                ),
                "verify": (
                    "Simulate 2,000 concurrent outbound connections in staging; verify `dropped_sent_packets_count` remains zero and dynamic port scaling allocates additional ports seamlessly."
                ),
                "residual": (
                    "Dynamic port allocation increases the required public IP quota; enterprise network teams must pre-allocate sufficient IP pools."
                ),
                "diagram": (
                    "Outbound burst begins",
                    "64-port SNAT limit hit",
                    "70% checkout drops",
                    "Dynamic port allocation",
                    "Zero dropped packets"
                ),
                "facts": "Cloud NAT dropped 14,200 packets/min due to port starvation on a single public IP.",
                "inference": "Fixed port allocation creates an artificial ceiling on outbound microservice scalability.",
                "expected": "Cloud NAT dynamically scales ports per VM up to configured maximums without dropping packets."
            },
            "lab": {
                "name": "Layer-by-Layer SPOF Audit and Remediation Runbook",
                "file": "day-083-topic-03-spof-audit.md",
                "goal": "Conduct a comprehensive architectural SPOF audit of a reference multi-tier enterprise architecture and author concrete gcloud remediation commands.",
                "expected": "A structured Markdown audit document covering 5 infrastructure layers, rating failure blast radius, and detailing exact commands to enforce high availability.",
                "mode": "tabletop analysis & command synthesis",
                "prereq": "Completion of Exercises 1 and 2.",
                "preflight": "Review Brightloaf architecture diagram from Day 80.",
                "steps": [
                    "Create the SPOF audit markdown document:\n\n```sh\ncat <<'EOF' > day-083-topic-03-spof-audit.md\n# Day 83: Layer-by-Layer SPOF Audit & Remediation Matrix\n\n## 1. Network Layer Audit\n- **Identified SPOF:** Single Cloud NAT IP with static 64-port limit.\n- **Blast Radius:** Total outbound connectivity failure (payments, external APIs).\n- **Remediation Command:**\n```bash\ngcloud compute routers nats update brightloaf-nat \\\n    --router=brightloaf-cr \\\n    --region=us-central1 \\\n    --enable-dynamic-port-allocation \\\n    --min-ports-per-vm=128 \\\n    --max-ports-per-vm=1024\n```\n\n## 2. Compute Layer Audit\n- **Identified SPOF:** Single-zone standalone Compute Engine VM for batch processing.\n- **Blast Radius:** Entire batch pipeline halted if zone `us-central1-a` suffers outage.\n- **Remediation Command:**\n```bash\ngcloud compute instance-groups managed create brightloaf-batch-rmig \\\n    --region=us-central1 \\\n    --template=brightloaf-batch-template \\\n    --size=3 \\\n    --health-check=brightloaf-batch-hc \\\n    --initial-delay=300\n```\n\n## 3. Database Layer Audit\n- **Identified SPOF:** Single-zone Cloud SQL PostgreSQL instance.\n- **Blast Radius:** RTO > 4 hours (manual backup restoration required on host crash).\n- **Remediation Command:**\n```bash\ngcloud sql instances patch brightloaf-db \\\n    --availability-type=REGIONAL\n```\n\n## 4. Summary Matrix\n| Layer | Pre-Remediation SLA | Post-Remediation SLA | Failover Mechanism |\n| :--- | :--- | :--- | :--- |\n| Network (NAT) | 99.0% (port limited) | 99.99% | Dynamic IP pool & port scaling |\n| Compute | 99.5% (zonal) | 99.95% | Regional MIG multi-zone autohealing |\n| Database | 99.9% (zonal) | 99.95% | Regional PD synchronous failover (<60s) |\nEOF\ncat day-083-topic-03-spof-audit.md\n```",
                    "Verify the remediation commands follow modern GCP CLI syntax and target regional high availability.",
                    "Confirm the audit document establishes a clear connection between theoretical availability math and practical infrastructure controls.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, is well-formatted, and contains valid GCP CLI commands for NAT dynamic allocation, Regional MIG, and Regional Cloud SQL."
                ),
                "trouble": "Ensure `--availability-type=REGIONAL` is used rather than read replica promotion for Cloud SQL HA.",
                "cleanup": "Retain `day-083-topic-03-spof-audit.md` as an exit evidence artifact.",
                "accept": "Completed layer-by-layer SPOF matrix with exact, production-ready remediation commands."
            }
        }
    ]
}
