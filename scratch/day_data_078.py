"""day_data_078.py — Exhaustive architecture data specification for Day 78.

Covers Decision Matrices Grounded in Experiments: Build vs Buy vs Managed Services,
Weighted Criteria Trade-off Matrices, Sensitivity Analysis, and Empirical Grounding.
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 78

DATA = {
    "day": 78,
    "part1_intro": (
        "Day 78 establishes the quantitative discipline of architectural decision-making: replacing intuition, subjective bias, "
        "and vendor hype with rigorous, experiment-grounded trade-off matrices. Architects routinely face the fundamental trilemma: "
        "build custom software, buy commercial off-the-shelf software (COTS/SaaS), or leverage cloud-managed services. Evaluating "
        "these options requires modeling complete Total Cost of Ownership (TCO)—including infrastructure, software licenses, operational "
        "toil, maintenance headcount, and outage blast radius. Furthermore, scoring models must be grounded in empirical benchmarks "
        "(such as measured latency, observed throughput, and failover duration) rather than qualitative impressions. This session "
        "provides the mathematical frameworks, sensitivity analysis methodologies, and verifiable decision templates required to "
        "defend critical architectural selections under stakeholder scrutiny."
    ),
    "exit_summary": (
        "Constructed a multi-criteria decision analysis (MCDA) matrix with mathematically derived Analytic Hierarchy Process (AHP) "
        "weights; executed an empirical sensitivity sweep identifying critical inflection thresholds between Cloud Spanner, Cloud SQL, "
        "and self-managed PostgreSQL; authored an automated Python sensitivity simulator modeling TCO variance across 3-year production horizons."
    ),
    "part2_intro": (
        "Architectural decisions are irreversible commitments that dictate capital expenditure, staffing models, and systemic resilience. "
        "The sections below provide deep technical analyses of the build-versus-buy spectrum, mathematical TCO formulations, "
        "multi-attribute utility theory, and empirical sensitivity analysis."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Architecture Dimension</th>
      <th>Build (Custom In-House)</th>
      <th>Buy (COTS / Third-Party SaaS)</th>
      <th>Managed Service (GCP PaaS/Serverless)</th>
      <th>Empirical Grounding Metric</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>CapEx &amp; Upfront Engineering</strong></td>
      <td>Extremely High (6–18 months dev cycle, custom architecture)</td>
      <td>Moderate (Vendor procurement, integration adapters, onboarding)</td>
      <td>Minimal (Immediate API availability, Terraform provisioning)</td>
      <td>Initial commits to production lead time (days)</td>
    </tr>
    <tr>
      <td><strong>OpEx &amp; Maintenance Toil</strong></td>
      <td>High (24/7 dedicated SRE on-call, manual patching, OS upgrades)</td>
      <td>Moderate (Subscription fees, vendor support tiers, version deprecations)</td>
      <td>Low (Automated backups, SLA-backed maintenance, zero OS patching)</td>
      <td>Quarterly engineering hours spent on operational toil</td>
    </tr>
    <tr>
      <td><strong>Scalability &amp; Blast Radius</strong></td>
      <td>Constrained by custom sharding, manual replication, etcd limits</td>
      <td>Constrained by vendor multi-tenant quotas and rate limits</td>
      <td>Elastic (Multi-zone/multi-region automated autoscaling)</td>
      <td>p99 Latency at 10x baseline peak traffic load</td>
    </tr>
    <tr>
      <td><strong>Portability &amp; Lock-in</strong></td>
      <td>High portability (Self-contained code, container runtime)</td>
      <td>High lock-in (Proprietary data models, vendor API dependencies)</td>
      <td>Moderate lock-in (Managed APIs; mitigated via open standards like SQL)</td>
      <td>Egress data volume transfer cost and migration duration</td>
    </tr>
    <tr>
      <td><strong>Failure Domain &amp; MTTR</strong></td>
      <td>Entirely internal (Kernel bugs, quorum failure, storage corruption)</td>
      <td>External dependency (Vendor status page, black-box troubleshooting)</td>
      <td>Shared responsibility (Google Cloud SLA, automated failover)</td>
      <td>Measured Mean Time to Recovery (MTTR) during zone outage</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 78: Empirical Architecture Decision and Sensitivity Pipeline",
        "desc": "A continuous architectural pipeline converting empirical telemetry into weighted utility scores and sensitivity thresholds.",
        "nodes": [
            ("Empirical Telemetry", "Latency & Throughput Benchmarks\\n+ Pricing APIs & Quotas"),
            ("Utility Normalization", "Linear/Logarithmic Scoring\\n+ Constraint Boundaries"),
            ("AHP Weighting", "Analytic Hierarchy Process\\n+ Consistency Ratio Verification"),
            ("Sensitivity Boundary", "Monte Carlo TCO Modeling\\n+ Tipping Point Analysis"),
            ("Defensible ADR", "Architecture Decision Record\\n+ Traceable Evidence"),
        ],
        "caption": "Figure 78.1: Architectural decision pipeline translating empirical measurements through mathematical weighting to defensible decision records."
    },
    "part3_intro": (
        "The following field cases analyze severe operational and financial disasters caused by flawed architecture decisions. "
        "Each case details the real-world operational context, quantifiable failure metrics, diagnostic sequences, "
        "defensible remediations, and dual-lane failed/corrected architectural diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises provide production-grade, executable configurations and verification scripts for "
        "implementing Analytic Hierarchy Process (AHP) decision models, running Monte Carlo TCO simulations, and executing "
        "sensitivity analysis across multi-year architectural options."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Build vs buy vs managed service",
            "overview": (
                "The decision to build custom software, purchase commercial off-the-shelf software (COTS/SaaS), or adopt "
                "cloud-managed services is the single most consequential choice an enterprise architect makes. Every architectural "
                "component incurs costs across two distinct horizons: Day 1 acquisition/implementation and Day 2 operational lifecycle. "
                "Organizations frequently succumb to the 'build trap', where engineering teams severely underestimate the ongoing toil "
                "of operating self-hosted open-source software—such as Kafka, Elasticsearch, or PostgreSQL—on raw virtual machines. "
                "Conversely, blindly selecting managed cloud services without understanding pricing tiers, egress penalties, or quota "
                "ceilings can lead to catastrophic budget escalation. Grounding this decision requires a comprehensive Total Cost of "
                "Ownership (TCO) equation that accounts for capital expenditure, infrastructure consumption, specialized staffing requirements, "
                "recurring operational toil, and the financial blast radius of availability downtime."
            ),
            "preview": (
                "Selecting a self-managed open-source database cluster to avoid cloud PaaS fees creates hidden operational toil in disk resizing, failover management, and security patch automation. "
                "This operational friction diverts core engineering velocity, degrades mean time to recovery (MTTR), and increases total annual enterprise expenditure."
            ),
            "technical": (
                "Architectural selection across build, buy, and managed services requires quantitative modeling across five key dimensions.\n\n"
                "#### Mathematical TCO Formulation and Operational Toil Modeling\n\n"
                "A naive comparison considers only infrastructure compute and disk charges. A rigorous architectural TCO "
                "model incorporates engineering labor, operational toil, and risk probability over an amortization window of 36 months:\n\n"
                "$$\\text{TCO} = \\sum_{t=1}^{T} \\left( C_{\\text{infra}}(t) + C_{\\text{license}}(t) + C_{\\text{eng}}(t) + C_{\\text{toil}}(t) + C_{\\text{outage}}(t) \\right) + C_{\\text{migration}}$$\n\n"
                "Where direct engineering labor and operational toil are quantified explicitly:\n\n"
                "- Direct engineering labor represents feature maintenance: $\\text{FTE}_{\\text{dev}} \\times \\text{Rate}_{\\text{hourly}} \\times 160$.\n\n"
                "- Operational toil represents repetitive tactical overhead (patching, manual resizing, backup validation): $\\text{FTE}_{\\text{SRE}} \\times \\text{Rate}_{\\text{hourly}} \\times \\text{Hours}_{\\text{toil}}$. Google SRE principles mandate keeping operational toil strictly below 50% of engineering bandwidth.\n\n"
                "- Outage financial risk models expected unmitigated downtime: $(1 - \\text{SLA}) \\times \\text{Minutes}_{\\text{period}} \\times \\text{Cost}_{\\text{downtime/min}}$. At an e-commerce revenue impact of $15,000/minute, a 99.9% available self-hosted system incurs 43.8 minutes of monthly downtime, adding $657,000 in monthly enterprise risk exposure.\n\n"
                "```python\n"
                "# tco_formulation.py\n"
                "def calculate_annual_tco(infra_monthly, sre_toil_hours, sre_rate=185, downtime_mins=43.8, downtime_cost=15000):\n"
                "    c_infra = infra_monthly * 12\n"
                "    c_toil = sre_toil_hours * sre_rate\n"
                "    c_outage = downtime_mins * downtime_cost\n"
                "    total = c_infra + c_toil + c_outage\n"
                "    return {'c_infra': c_infra, 'c_toil': c_toil, 'c_outage': c_outage, 'total': total}\n"
                "```\n\n"
                "#### The Shared Responsibility Boundary Across Architectural Tiers\n\n"
                "The boundary of operational control shifts dramatically across architectural archetypes:\n\n"
                "- **Build on IaaS (e.g., Self-hosted Kafka on GCE):** The customer owns application code, runtime libraries, kernel tuning (`sysctl.conf`), OS security patches, disk volume extension, distributed consensus management (KRaft/ZooKeeper quorum), cross-zone replication topologies, and disaster recovery procedures. Google manages only physical data centers, host hardware, and hypervisors.\n\n"
                "- **Managed Cloud PaaS (e.g., Cloud SQL, Cloud Spanner, Pub/Sub):** Google manages the underlying OS, storage provisioning, point-in-time recovery, high-availability failover, binary patching, and distributed consensus. The customer owns data schema, index design, query optimization, IAM access policies, and application connection pooling.\n\n"
                "- **Buy (COTS/SaaS, e.g., Datadog, Confluent Cloud, Snowflake):** The SaaS vendor manages end-to-end service availability, global feature delivery, and infrastructure scaling. The customer owns data ingestion integration, configuration, user access, and contractual SLA enforcement.\n\n"
                "#### Vendor Lock-In Dynamics, Portability Costs, and Data Gravity\n\n"
                "Architects frequently overpay for 'architectural portability'—spending months designing custom abstraction layers to prevent "
                "lock-in to cloud services like BigQuery or Cloud Spanner. In practice, portability carries substantial negative compound interest:\n\n"
                "- **Lowest Common Denominator Anti-Pattern:** Abstraction layers prevent teams from utilizing cloud-native capabilities (e.g., Spanner TrueTime distributed transactions or BigQuery partition pruning), degrading overall system performance.\n\n"
                "- **Portability Maintenance Tax:** Maintaining multi-cloud compatibility requires continuous regression testing across heterogeneous providers, consuming 15–30% of engineering bandwidth.\n\n"
                "- **Data Gravity Dominance:** When a dataset exceeds 50 Terabytes, network egress costs ($0.08–$0.12 per GB) and transfer duration dominate migration feasibility. Storing 100 TB and transferring it across clouds incurs $8,000–$12,000 in raw egress charges alone, rendering theoretical runtime portability economically unviable.\n\n"
                "#### Day-2 Operational Degradation in Self-Hosted Distributed Clusters\n\n"
                "Self-hosted distributed systems inevitably experience entropy. Consider self-managed PostgreSQL with Patroni and Consul on GCE:\n\n"
                "- **Consensus Heartbeat Starvation:** Under high VM CPU utilization or transient network jitter between zones, Consul agents can miss election heartbeats, triggering false-positive leader failovers and split-brain write corruption.\n\n"
                "- **WAL Storage Saturation:** An unmonitored replication slot or lagging standby causes the primary database to retain PostgreSQL Write-Ahead Logs (`pg_wal`) until the underlying persistent disk reaches 100% capacity, abruptly crashing the database engine into a read-only or kernel emergency state.\n\n"
                "- **Managed Service Mitigation:** Cloud SQL automates automatic storage increases, uses regional persistent disks with synchronous replication, and leverages dedicated health-check daemons independent of userland CPU contention, completely eliminating these failure modes."
            ),
            "questions": [
                "What is the fully burdened cost of SRE labor allocated to manual database patching and backup verification?",
                "Does the proposed architecture introduce custom abstraction layers that sacrifice platform-native capabilities for hypothetical portability?",
                "What is the mathematical blast radius of a single-zone network partition on the self-hosted consensus quorum?"
            ],
            "reference": "https://cloud.google.com/architecture/framework/system-design",
            "reference_label": "Google Cloud Architecture Framework: System Design and Service Selection",
            "scenario": {
                "scenario": (
                    "A fintech payment processing platform handling 8,500 transactions per second chose to self-host an Apache Kafka cluster "
                    "on Compute Engine VMs across three zones (us-central1-a, b, c) rather than adopting managed Google Cloud Pub/Sub or Confluent Cloud. "
                    "The engineering team justified the decision based on raw VM compute pricing ($1,800/month for nine n2-standard-16 VMs with SSD persistent disks) "
                    "versus estimated Pub/Sub message ingestion charges ($4,200/month). During a seasonal 4x traffic surge, disk I/O saturated due to "
                    "unoptimized Kafka segment compaction and synchronous persistent disk flushing. Two broker nodes were marked dead by the ZooKeeper quorum "
                    "due to missed heartbeat pings during prolonged JVM garbage collection pauses. The remaining brokers entered an infinite partition "
                    "rebalancing loop, halting message ingestion for 38 minutes and causing payment authorization timeouts across all merchant endpoints."
                ),
                "impact": (
                    "194,000 credit card authorization requests failed; merchant SLA penalties incurred $280,000 in contractual liquidated damages; "
                    "four senior SREs spent 28 continuous hours manually repairing corrupted partition indices; unbudgeted emergency engineering overtime "
                    "cost $44,000. Total incident cost exceeded $324,000—eradicating 7.5 years of projected infrastructure savings in a single afternoon."
                ),
                "constraints": (
                    "Must sustain 35,000 peak messages/second with p99 latency < 25 ms; must guarantee strict at-least-once delivery; "
                    "operational toil budget must not exceed 4 engineering hours per month; recovery from zone failure must be fully automated without human intervention."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect Compute Engine persistent disk metrics; observe write queue depth exceeding 64, saturating the 15,000 IOPS ceiling of 500GB SSD PD.",
                    "Step 2: Analyze JVM garbage collection logs; identify stop-the-world pause times spiking to 12.8 seconds due to excessive message buffer allocations.",
                    "Step 3: Review ZooKeeper session telemetry; confirm heartbeat timeout expiration (6,000 ms) triggered cascading broker deregistration.",
                    "Step 4: Audit true TCO accounting; discover that cluster maintenance consumed 480 hours of senior SRE toil over 9 months ($88,800 in unmodeled labor)."
                ],
                "root": (
                    "Flawed Day 1 decision matrix that compared raw VM compute costs against managed service fees while completely ignoring "
                    "JVM garbage collection operational tuning, persistent disk IOPS scaling constraints, and human SRE maintenance toil."
                ),
                "remediation_steps": [
                    "Step 1: Provision Google Cloud Pub/Sub topics with dead-letter subscriptions, migrating client ingestion endpoints via Cloud Run routing facades.",
                    "Step 2: Deprecate self-managed ZooKeeper and Kafka brokers, eliminating dedicated VM operational patching and disk management entirely.",
                    "Step 3: Configure Cloud Pub/Sub BigQuery subscriptions and Cloud Storage export buckets to automate long-term message archival without manual administration.",
                    "Step 4: Amend the corporate Architecture Review Board charter to mandate that all self-hosted proposals include fully burdened SRE labor costs ($185/hr) in TCO calculations."
                ],
                "verify": (
                    "Execute synthetic load testing at 45,000 messages/second on Cloud Pub/Sub: observe 0 lost messages, p99 publish latency of 18 ms, "
                    "and zero administrative pages during simulated single-zone failure drill."
                ),
                "residual": (
                    "Cloud Pub/Sub provides at-least-once delivery; downstream payment consumer microservices must enforce idempotency keys "
                    "(deduplication cache in Memorystore Redis) to prevent duplicate transaction charges."
                ),
                "diagram": (
                    "35k msg/s surge saturates self-managed Kafka SSD IOPS",
                    "JVM GC pause 12s causes ZooKeeper quorum heartbeat timeout",
                    "Infinite partition rebalance; 38-minute payment outage",
                    "Replace with managed Cloud Pub/Sub and Cloud Run ingress",
                    "Autonomous elastic scaling, 0 toil, 18 ms p99 verified"
                ),
                "facts": "Self-hosted Kafka on 9 GCE VMs saved $2.4k/mo in sticker price; 35k msg/s surge crashed cluster for 38 min; $324,000 total disaster cost.",
                "inference": "Underestimating Day 2 SRE toil and storage I/O limits in self-hosted clusters leads to catastrophic business outages that dwarf cloud managed service fees.",
                "expected": "Managed Cloud Pub/Sub eliminates server patching and disk sizing toil while automatically scaling across multi-zone infrastructure."
            },
            "lab": {
                "name": "Burdened TCO and Operational Toil Sensitivity Calculator",
                "file": "day-078-tco-calculator.md",
                "goal": "Build an executable Python model that calculates fully burdened 3-year TCO including infrastructure, SRE toil, and downtime financial risk.",
                "expected": "An executable Python financial script modeling TCO variance and demonstrating when managed services break even against self-hosted infrastructure.",
                "mode": "local Python 3 analysis and tabletop modeling; zero cloud billing",
                "prereq": "Day 77 licensing financial model and basic Python scripting",
                "preflight": "Verify Python 3 is installed in your local shell environment.",
                "steps": [
                    "Document the financial parameters and decision criteria in `day-078-tco-calculator.md`.",
                    "Develop the executable Python burdened TCO calculation script (`tco_engine.py`):\n\n```python\n# tco_engine.py\nimport sys\n\ndef model_tco(label, monthly_infra, fte_toil, hourly_rate=185, sla=0.999, cost_per_outage_min=10000):\n    months = 36\n    infra_total = monthly_infra * months\n    # 1 FTE = 160 hours/month = 1,920 hours/year\n    toil_hours_total = fte_toil * 160 * months\n    toil_labor_total = toil_hours_total * hourly_rate\n    # Downtime minutes per year based on SLA\n    # 99.9% = 525.6 min/yr; 99.95% = 262.8 min/yr; 99.999% = 5.26 min/yr\n    downtime_mins_3yr = (1.0 - sla) * 525600 * 3\n    outage_risk_total = downtime_mins_3yr * cost_per_outage_min\n    total_tco = infra_total + toil_labor_total + outage_risk_total\n    return {\n        'label': label,\n        'infra': infra_total,\n        'toil': toil_labor_total,\n        'risk': outage_risk_total,\n        'total': total_tco\n    }\n\n# Evaluate 3 Options\noptions = [\n    model_tco('Self-Hosted Kafka (9x GCE)', monthly_infra=1800, fte_toil=0.60, sla=0.999),\n    model_tco('Managed Cloud Pub/Sub',      monthly_infra=4200, fte_toil=0.04, sla=0.9995),\n    model_tco('Enterprise SaaS Kafka',       monthly_infra=6500, fte_toil=0.08, sla=0.9999)\n]\n\nprint(f\"{'Option':<28} | {'Infra 3-Yr':<12} | {'SRE Toil':<12} | {'Outage Risk':<12} | {'TOTAL BURDENED TCO':<18}\")\nprint(\"-\" * 90)\nfor opt in options:\n    print(f\"{opt['label']:<28} | ${opt['infra']:>10,d} | ${opt['toil']:>10,d} | ${opt['risk']:>10,d} | ${opt['total']:>16,d}\")\n\n# Assert that managed Cloud Pub/Sub has lower total burdened TCO than self-hosted\nassert options[1]['total'] < options[0]['total'], 'Managed Pub/Sub TCO should be lower when toil and risk are factored!'\nprint('\\n>> TCO Sensitivity Verification PASSED: Cloud Pub/Sub saves over $500k in burdened 3-year TCO.')\n```",
                    "Execute the Python TCO analysis engine:\n\n```sh\npython3 tco_engine.py\n```"
                ],
                "verification": (
                    "Run the automated TCO verification suite:\n\n```sh\npython3 -c \"import tco_engine; print('TCO Engine Execution Verified')\"\n```\n\nConfirm that the output demonstrates managed services achieve superior economic return over a 36-month operational horizon."
                ),
                "trouble": (
                    "If the assertion fails, check that hourly_rate is set to $185 and the SLA downtime parameters match expected 3-year outage minutes."
                ),
                "cleanup": (
                    "Remove temporary Python scripts:\n\n```sh\nrm -f tco_engine.py\n```"
                ),
                "accept": "Burdened TCO model documented with dated pricing parameters and SRE toil allocations.",
                "file": "day-078-tco-calculator.md"
            }
        },
        {
            "key": "topic-02",
            "title": "Trade-off matrices with weighted criteria",
            "overview": (
                "Architectural decisions often collapse into ideological debates between engineering factions advocating for their preferred "
                "technologies. Multi-Criteria Decision Analysis (MCDA) replaces subjective arguments with a structured, quantitative "
                "scoring framework. By defining explicit criteria (e.g., latency, cost, regulatory compliance, engineering velocity), "
                "establishing mathematical weighting coefficients, and grounding every evaluation score in verified telemetry or contractual "
                "guarantees, architects build transparent decision records that withstand executive audit. Furthermore, robust decision "
                "matrices include sensitivity analysis to identify the exact tipping points where an architectural preference shifts."
            ),
            "preview": (
                "Assigning subjective weighting coefficients without linking scores to measured latency, throughput, or unit financial models allows architect bias to dictate critical platform decisions. "
                "The resulting architecture suffers from performance bottlenecks or catastrophic cost overruns when production traffic patterns deviate from intuitive assumptions."
            ),
            "technical": (
                "Constructing an empirically grounded trade-off matrix requires rigorous mathematical formulation, pairwise weight calibration, "
                "and systematic sensitivity sweeps.\n\n"
                "#### Analytic Hierarchy Process (AHP) for Weight Derivation\n\n"
                "Arbitrarily assigning weights (e.g., 'Performance = 30%, Cost = 40%') introduces subconscious cognitive bias. The Analytic "
                "Hierarchy Process (AHP), developed by Thomas Saaty, derives objective weightings via pairwise comparison matrices:\n\n"
                "1. Construct an $n \\times n$ comparison matrix $A$ where element $a_{ij}$ represents the relative importance of criterion $i$ over criterion $j$ on a standard scale from 1 (equal) to 9 (extreme importance), with $a_{ji} = 1 / a_{ij}$.\n\n"
                "2. Compute the principal eigenvector $w$ corresponding to the maximum eigenvalue $\\lambda_{\\max}$:\n\n"
                "$$A w = \\lambda_{\\max} w$$\n\n"
                "3. Normalize the eigenvector such that $\\sum_{i=1}^{n} w_i = 1.0$. The resulting vector components $w_i$ represent the mathematically consistent weights.\n\n"
                "4. Calculate the Consistency Index ($CI$) and Consistency Ratio ($CR$):\n\n"
                "$$CI = \\frac{\\lambda_{\\max} - n}{n - 1}, \\quad CR = \\frac{CI}{RI}$$\n\n"
                "Where $RI$ is the Random Index for an $n$-dimensional matrix. If $CR < 0.10$, the pairwise comparisons are internally consistent. If $CR \\ge 0.10$, the architect must re-evaluate contradictory comparisons.\n\n"
                "```python\n"
                "# ahp_weights.py\n"
                "def calculate_ahp_weights(matrix):\n"
                "    n = len(matrix)\n"
                "    geo_means = [math.prod(row) ** (1.0 / n) for row in matrix]\n"
                "    total = sum(geo_means)\n"
                "    weights = [gm / total for gm in geo_means]\n"
                "    return weights\n"
                "```\n\n"
                "#### Grounding Scoring in Empirical Telemetry via Utility Functions\n\n"
                "Every candidate score $s_{ij} \\in [1, 10]$ for option $j$ under criterion $i$ must map directly to an observable measurement via a defined utility function $U_i(x)$:\n\n"
                "- **Performance (p99 Latency):** Inverse linear normalization between best observed latency ($x_{\\min}$) and unacceptable latency ($x_{\\max}$):\n\n"
                "$$U_{\\text{perf}}(x) = 1 + 9 \\times \\frac{x_{\\max} - x}{x_{\\max} - x_{\\min}}$$\n\n"
                "If $x_{\\min} = 5\\text{ ms}$ (score 10) and $x_{\\max} = 100\\text{ ms}$ (score 1), a measured p99 latency of $25\\text{ ms}$ yields an objective score of $1 + 9 \\times \\frac{75}{95} = 8.1$.\n\n"
                "- **Financial TCO:** Negative linear utility mapping annual projected expenditure between lowest cost budget and upper constraint limit.\n\n"
                "- **Compliance & Invariant Safety:** Step-function utility: if a system cannot guarantee ACID serializability for the Day 64 single-fulfillment invariant, its score is automatically clamped to 0, disqualifying the option regardless of low infrastructure cost.\n\n"
                "#### Sensitivity Analysis and Inflection Point Derivation\n\n"
                "The total composite utility score for architectural alternative $j$ is:\n\n"
                "$$S_j = \\sum_{i=1}^{n} w_i s_{ij}$$\n\n"
                "Sensitivity analysis evaluates how variations in criterion weights or underlying empirical variables alter the ranking between Option A and Option B. The tipping point occurs when the utility delta equals zero:\n\n"
                "$$\\Delta S(w_k) = S_A(w_k) - S_B(w_k) = 0$$\n\n"
                "By plotting $S_j$ as a function of weight $w_k \\in [0, 1]$ (while normalizing remaining weights $\\sum_{i \\ne k} w_i = 1 - w_k$), the architect identifies the exact tipping point. For example, if Cloud Spanner is preferred when Availability Weight exceeds 0.22, but Cloud SQL is preferred below 0.22, the architectural decision hinges entirely on the organization's tolerance for scheduled maintenance downtime.\n\n"
                "#### Risk-Weighted Scenario Testing\n\n"
                "A robust architecture must perform across volatile business scenarios. Architects test candidate options across three operational regimes:\n\n"
                "- **Baseline Regime:** Projected normal transaction growth (15% YoY).\n\n"
                "- **Stress/Black Swan Regime:** 10x burst traffic (e.g., flash sales, viral events), network partition across cloud zones, and 50% SRE staffing reduction.\n\n"
                "- **Economic Compression Regime:** 40% infrastructure budget reduction mandate."
            ),
            "questions": [
                "Has every score in the trade-off matrix been mapped to an empirical benchmark log, published SLA, or dated pricing API export?",
                "Does the Consistency Ratio (CR) of the pairwise comparison matrix strictly satisfy the Saaty threshold of CR < 0.10?",
                "What is the mathematical inflection threshold at which an alternative architecture becomes the preferred choice?"
            ],
            "reference": "https://standards.ieee.org/ieee/42010/5836/",
            "reference_label": "IEEE 42010: Systems and Software Engineering — Architecture Description",
            "scenario": {
                "scenario": (
                    "An omnichannel retail enterprise was evaluating databases for its global inventory reservation system. The lead database "
                    "architect created a decision matrix comparing an open-source NoSQL document database (self-hosted Cassandra on GCE) against "
                    "Cloud Spanner. The architect assigned a 45% weight to 'Annual Software License and VM Cost' and only a 5% weight to 'Strict Serializable "
                    "ACID Consistency across Zones'. The matrix scored Cassandra at 8.8 and Cloud Spanner at 6.2, leading to the selection of Cassandra. "
                    "During a Black Friday flash sale with 12,000 concurrent checkout threads across us-central1 and us-east4, Cassandra's eventual consistency "
                    "model suffered from network replication lag. Multiple inventory decrement mutations succeeded concurrently for the same warehouse SKUs, "
                    "violating the core Day 64 single-fulfillment business invariant and resulting in 4,120 duplicate item reservations and oversold merchandise."
                ),
                "impact": (
                    "4,120 orders could not be fulfilled due to negative warehouse inventory; $610,000 in order cancellations and customer goodwill gift cards; "
                    "enterprise brand reputation severely damaged on social media; executive audit revealed the architectural decision matrix had been deliberately "
                    "weighted to favor the architect's familiar open-source toolset."
                ),
                "constraints": (
                    "Must guarantee strict serializable isolation across multi-region write nodes; must prevent double-fulfillment under concurrent race conditions; "
                    "must support sub-50 ms read/write latency at 20,000 QPS."
                ),
                "diagnostic_steps": [
                    "Step 1: Query warehouse fulfillment logs; identify 4,120 distinct checkout transactions referencing identical physical SKU inventory allocations.",
                    "Step 2: Review Cassandra mutation timestamps; confirm that concurrent read-before-write operations executed simultaneously across different replica nodes before gossip synchronization.",
                    "Step 3: Audit original decision matrix; discover that 'Strict Serializable ACID' was weighted at 5%, while 'Direct Monthly Infra Spend' was weighted at 45% without modeling business losses from overselling.",
                    "Step 4: Conduct AHP pairwise re-evaluation with executive stakeholders; recalibrate weights to assign 35% to Data Invariant Integrity and 15% to Infrastructure Cost."
                ],
                "root": (
                    "Subjective weighting manipulation in the architectural decision matrix that penalized Cloud Spanner for higher baseline infrastructure cost while treating transactional consistency as a low-priority optional feature rather than an inviolable business invariant."
                ),
                "remediation_steps": [
                    "Step 1: Migrate the inventory reservation ledger to Google Cloud Spanner utilizing TrueTime-backed distributed transactions.",
                    "Step 2: Implement strict mutation transactions with row-level locks on warehouse SKU balance records, enforcing the Day 64 single-fulfillment invariant.",
                    "Step 3: Establish an automated Sensitivity Analysis gate in the Architecture Decision Record (ADR) template, requiring proof that invariant safety criteria have veto power (step-function utility).",
                    "Step 4: Create an automated reconciliation pipeline to audit reservation balances against physical warehouse scans every 15 minutes."
                ],
                "verify": (
                    "Execute synthetic concurrency stress test executing 25,000 parallel checkout requests against single-item SKUs in Cloud Spanner: "
                    "exactly one transaction succeeds per physical item; 24,999 return clean inventory exhausted exceptions; zero duplicate fulfillments."
                ),
                "residual": (
                    "Cloud Spanner read-write transactions on highly contended single rows (hotspotting) can experience lock wait timeouts; "
                    "high-velocity items must use distributed counter sharding or queuing for queue-based inventory reservation."
                ),
                "diagram": (
                    "12k checkout threads execute concurrent inventory decrements",
                    "Cassandra gossip replication lag allows parallel writes",
                    "4,120 duplicate fulfillments violate Day 64 invariant",
                    "Migrate to Cloud Spanner TrueTime distributed transactions",
                    "Strict serializability guarantees exactly one fulfillment per SKU"
                ),
                "facts": "Cassandra selected over Spanner via 45% cost weight; Black Friday surge caused 4,120 oversold orders; $610k business loss; Spanner TrueTime eliminated overselling.",
                "inference": "Decision matrices that treat core business invariants as negotiable trade-offs produce fragile architectures vulnerable to catastrophic operational failure.",
                "expected": "Cloud Spanner enforces serializable distributed ACID transactions, preventing double-fulfillment under high-concurrency race conditions."
            },
            "lab": {
                "name": "AHP Decision Matrix and Sensitivity Sweep Simulator",
                "file": "day-078-decision-matrix.md",
                "goal": "Author a complete Python decision analysis engine implementing Saaty AHP weight derivation, consistency ratio validation, and sensitivity sweeps across competing architectures.",
                "expected": "An executable Python script that verifies pairwise consistency, calculates normalized criteria weights, and outputs sensitivity tipping point curves.",
                "mode": "local Python 3 algorithm implementation and markdown ADR authoring; zero cloud spend",
                "prereq": "Prior day discovery and migration rehearsal artifacts",
                "preflight": "Ensure Python 3 is installed with standard math libraries.",
                "steps": [
                    "Document the evaluation criteria, stakeholder priorities, and candidate options in `day-078-decision-matrix.md`.",
                    "Create the complete Analytic Hierarchy Process (AHP) and sensitivity simulation script (`ahp_engine.py`):\n\n```python\n# ahp_engine.py\nimport math\n\ndef calculate_ahp(matrix):\n    n = len(matrix)\n    # Compute geometric mean of each row\n    geo_means = []\n    for row in matrix:\n        prod = 1.0\n        for val in row:\n            prod *= val\n        geo_means.append(prod ** (1.0 / n))\n    total = sum(geo_means)\n    weights = [gm / total for gm in geo_means]\n    \n    # Calculate lambda_max and Consistency Ratio\n    weighted_sums = [sum(matrix[i][j] * weights[j] for j in range(n)) for i in range(n)]\n    lambda_max = sum(weighted_sums[i] / weights[i] for i in range(n)) / n\n    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0\n    ri_table = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24}\n    ri = ri_table.get(n, 1.32)\n    cr = ci / ri if ri > 0 else 0.0\n    return weights, cr\n\ndef run_simulation():\n    criteria = [\"Availability & SLA\", \"SRE Operational Toil\", \"ACID Invariant Safety\", \"3-Yr Burdened TCO\"]\n    # Pairwise comparison matrix (Saaty 1-9 scale)\n    # Row comparisons: [Avail, Toil, ACID, TCO]\n    pairwise = [\n        [1.0,  1.5,  1.0,  2.0],\n        [0.67, 1.0,  0.67, 1.5],\n        [1.0,  1.5,  1.0,  2.0],\n        [0.5,  0.67, 0.5,  1.0],\n    ]\n    weights, cr = calculate_ahp(pairwise)\n    print(\"=\" * 75)\n    print(f\"AHP CRITERIA WEIGHT DERIVATION (Consistency Ratio: {cr:.4f})\")\n    print(\"=\" * 75)\n    for c, w in zip(criteria, weights):\n        print(f\"  - {c:<25}: {w*100:5.2f}%\")\n    assert cr < 0.10, \"Inconsistent pairwise comparisons (CR >= 0.10)!\"\n    print(\"  >> Consistency Check: PASSED (CR < 0.10)\")\n\n    # Alternatives: [Self-Hosted PG, Cloud SQL Regional, Cloud Spanner Multi-Region]\n    options = [\"Self-Hosted PG (GCE)\", \"Cloud SQL (Regional)\", \"Cloud Spanner (Multi-Region)\"]\n    raw_scores = [\n        [6.0, 3.0, 8.0, 5.0],\n        [8.5, 8.5, 8.5, 9.0],\n        [10.0, 9.5, 10.0, 7.0],\n    ]\n    \n    print(\"\\nBASELINE COMPOSITE UTILITY SCORES:\")\n    baseline_scores = []\n    for opt, scores in zip(options, raw_scores):\n        composite = sum(w * s for w, s in zip(weights, scores))\n        baseline_scores.append(composite)\n        print(f\"  - {opt:<30}: Composite Score = {composite:5.2f} / 10.00\")\n    \n    # Sensitivity sweep across Availability weight\n    print(\"\\nSENSITIVITY SWEEP: AVAILABILITY WEIGHT VARIATION [0.10 to 0.60]:\")\n    print(f\"  {'Weight(Avail)':<14} | {'Self-Hosted':<14} | {'Cloud SQL':<14} | {'Cloud Spanner':<14} | {'Preferred Option'}\")\n    print(\"  \" + \"-\" * 80)\n    \n    tipping_point_found = False\n    for ha_w in [i * 0.05 for i in range(2, 13)]:\n        scale = (1.0 - ha_w) / (1.0 - weights[0])\n        sim_weights = [ha_w] + [w * scale for w in weights[1:]]\n        sim_scores = [sum(sw * s for sw, s in zip(sim_weights, opt_s)) for opt_s in raw_scores]\n        preferred = options[sim_scores.index(max(sim_scores))]\n        print(f\"  {ha_w:12.2f}   | {sim_scores[0]:12.2f} | {sim_scores[1]:12.2f} | {sim_scores[2]:12.2f} | {preferred}\")\n        if preferred == \"Cloud Spanner (Multi-Region)\" and not tipping_point_found:\n            print(f\"  >>> SENSITIVITY TIPPING POINT: At Availability Weight >= {ha_w:.2f}, Cloud Spanner overtakes Cloud SQL!\")\n            tipping_point_found = True\n            \n    print(\"=\" * 75)\n\nif __name__ == '__main__':\n    run_simulation()\n```",
                    "Execute the AHP decision engine and sensitivity sweep:\n\n```sh\npython3 ahp_engine.py\n```"
                ],
                "verification": (
                    "Run automated assertion testing on the decision engine:\n\n```sh\npython3 -c \"import ahp_engine; print('AHP Sensitivity Engine Test Passed')\"\n```\n\nConfirm output demonstrates that Cloud Spanner is preferred when availability and invariant safety criteria exceed 25% weight."
                ),
                "trouble": (
                    "If the script reports assertion error on consistency ratio, verify that pairwise comparisons satisfy reciprocal symmetry (matrix[i][j] == 1.0 / matrix[j][i])."
                ),
                "cleanup": (
                    "Clean up temporary simulation files:\n\n```sh\nrm -f ahp_engine.py\n```"
                ),
                "accept": "A decision matrix and sensitivity check showing when the preferred option changes, linked to dated pricing and benchmark evidence.",
                "file": "day-078-decision-matrix.md"
            }
        }
    ]
}
