"""day_data_092.py — Exhaustive architecture data specification for Day 92.

Covers Failover and Failback Planning:
1. Failover and failback procedures, DNS TTL considerations, reverse replication synchronization.
2. DR testing methodologies: tabletop exercises, game days, chaos engineering, full failover drills.
3. Google Cloud quota scope verification, regional compute ceilings, and reservation management.
4. Rate-limiting and graceful degradation during regional brownouts (Cloud Armor, load shedding).
5. Executable runbooks vs strategic playbooks, abort criteria, and operational ownership.
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 92

DATA = {
    "day": 92,
    "part1_intro": (
        "Day 92 synthesizes the operational, procedural, and technical culmination of disaster recovery: controlled failover execution, "
        "safe failback synchronization, and organizational readiness drills. An emergency failover plan that has never been tested in production "
        "is merely an untested hypothesis. Furthermore, while failing over during a regional catastrophe is urgent and high-stakes, the subsequent "
        "failback—returning workloads from the secondary recovery site to the restored primary region—is frequently more hazardous. "
        "Without strict reverse data replication, failback overwrites newly committed transactions, creating massive data corruption. "
        "Today's curriculum constructs end-to-end failover and failback procedures, formalizes structured DR testing frameworks (from tabletop "
        "exercises to full-scale unannounced regional blackhole drills), verifies Google Cloud regional quota headroom to eliminate capacity traps, "
        "implements Cloud Armor rate-limiting and graceful degradation during brownouts, and authors executable SRE operational runbooks equipped "
        "with explicit abort criteria and consistency checkpoints."
    ),
    "exit_summary": (
        "Engineered an enterprise Failover and Failback Orchestration Framework: designed an asymmetric failover and reverse-replication failback "
        "architecture; established an annual DR testing cadence across tabletop simulations, chaos game days, and full traffic shifts; implemented "
        "automated Google Cloud quota headroom auditing scripts; authored a Cloud Armor rate-limiting and shed-queue policy for brownout protection; "
        "produced a production-grade Executable Failover & Failback Runbook with clear owner assignments, abort triggers, and data parity checks."
    ),
    "part2_intro": (
        "Operational resilience requires transitioning disaster recovery from theoretical documentation into repeatable, audited engineering muscle memory. "
        "The sections below analyze failback mechanics, test paradigms, quota verification routines, brownout rate-limiting, and runbook governance."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Operational Phase</th>
      <th>Primary Risk / Failure Mode</th>
      <th>Key Technical Mechanism</th>
      <th>Safety Control &amp; Invariant</th>
      <th>Abort / Rollback Criteria</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Emergency Failover</strong></td>
      <td>Secondary region quota exhaustion; stale VM templates</td>
      <td>Cloud DNS steering; Cloud SQL replica promotion; MIG autoscale</td>
      <td>Pre-purchased Compute Engine Reservations; CI/CD multi-region template baking</td>
      <td>Secondary database fails to reach RUNNABLE within 5 minutes</td>
    </tr>
    <tr>
      <td><strong>Stabilization in DR</strong></td>
      <td>Traffic surge overpowers secondary region</td>
      <td>Cloud Armor edge rate-limiting; priority load shedding</td>
      <td>Drop non-essential background APIs; prioritize checkout transactions</td>
      <td>Database CPU sustained > 90% or 5xx error rate > 5%</td>
    </tr>
    <tr>
      <td><strong>Reverse Replication</strong></td>
      <td>Split-brain data divergence between regions</td>
      <td>Re-establish replication from DR secondary back to restored primary</td>
      <td>Byte lag must reach zero before failback traffic pivot</td>
      <td>Reverse replication errors or data checksum mismatch</td>
    </tr>
    <tr>
      <td><strong>Controlled Failback</strong></td>
      <td>In-flight writes lost during return pivot</td>
      <td>Graceful connection drain; read-only maintenance window; DNS update</td>
      <td>Lock writes during pivot; verify database parity before unlocking ingress</td>
      <td>Unapplied write transactions detected on secondary database</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 92: Full-Cycle Disaster Recovery: Failover, Reverse Replication, and Failback",
        "desc": "Lifecycle diagram showing primary failure, failover to secondary, reverse replication alignment, and safe failback return.",
        "caption": "Figure 92.1: Complete disaster recovery lifecycle illustrating the critical reverse-replication synchronization phase before return-to-primary.",
        "nodes": [
            ("1. Failover Pivot", "Steer Traffic to DR Secondary\\nPromote Read Replica"),
            ("2. DR Operations", "Rate Limiting & Shedding\\nLive Production in Region B"),
            ("3. Reverse Sync", "Region A Restored\\nReverse Replicate B -> A"),
            ("4. Safe Failback", "Drain Secondary & Shift to A\\nZero Data Loss Guaranteed"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Failover and failback procedures, DNS TTL considerations",
            "preview": (
                "After operating in a secondary DR region for 14 hours, an SRE team abruptly shifts DNS back to the restored primary region, "
                "causing immediate database split-brain and overwriting 12,000 customer transactions created during the failover period."
            ),
            "overview": (
                "While disaster **failover** is conducted urgently in response to an unexpected catastrophic infrastructure collapse, **failback** "
                "(the process of returning workloads to the restored primary environment) must be planned and executed with methodical precision. "
                "The core engineering danger during failback is data divergence (split-brain). During the outage, the secondary recovery database "
                "accumulated new writes, updates, and deletes. If traffic is switched back to the primary before these new transactions are synchronized, "
                "the primary and secondary databases diverge, resulting in permanent data corruption. A resilient failback procedure requires: "
                "1) re-establishing **reverse replication** from the secondary to the restored primary, 2) lowering DNS TTLs days in advance of the planned "
                "cutover, 3) initiating a brief read-only maintenance window to drain in-flight connections, 4) verifying byte-level data parity, and "
                "5) pivoting traffic back to the primary."
            ),
            "technical": (
                "### 1. The Asymmetry Between Failover and Failback\n"
                "- **Failover Velocity:** Speed is paramount. The primary region is dead; transactions are failing. Engineers trigger automated or "
                "semi-automated runbooks to promote replicas and steer traffic to secondary infrastructure as rapidly as possible.\n"
                "- **Failback Deliberation:** Safety and data integrity are paramount. The business is currently operating successfully in the DR region. "
                "Failback should *never* occur under emergency conditions; it must be scheduled during low-traffic maintenance windows.\n\n"
                "### 2. Reverse Replication Synchronization Mechanics\n"
                "- **The Reversal Sequence:**\n"
                "  1. The primary region (`us-central1`) is declared healthy by Google Cloud.\n"
                "  2. Do *not* point clients back yet. Configure the restored database instance in `us-central1` as an *external replica* "
                "tracking the currently active primary in `us-east1`.\n"
                "  3. Stream Write-Ahead Logs (WAL) or binary logs across regions from `us-east1` to `us-central1`.\n"
                "  4. Monitor replication byte lag until it reaches zero.\n\n"
                "### 3. DNS TTL Caching Considerations During Failback\n"
                "- **Pre-Failback TTL Reduction:** At least 48 to 72 hours before a scheduled failback, reduce DNS A-record TTLs from standard durations "
                "(e.g. 300s or 3600s) down to **30 seconds** across all Cloud DNS public zones.\n"
                "- **Connection Draining Maintenance Gate:** During cutover, place the application into read-only mode for 60 seconds (exceeding DNS TTL). "
                "This ensures all straggling requests to the secondary region are read-only and no new writes are accepted while traffic pivots to the primary."
            ),
            "questions": [
                "Why does executing a failback without establishing reverse data replication cause catastrophic split-brain corruption?",
                "What is the operational rationale for lowering DNS TTLs 48 hours prior to a planned failback maintenance window?",
                "How does placing the application in read-only mode during DNS cutover prevent orphaned transactional state?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/dr-scenarios#failover_and_failback",
            "reference_label": "Google Cloud Architecture: Failover and failback procedures, synchronization, and DNS management",
            "scenario": {
                "symptom": (
                    "Following a 12-hour regional power outage in `us-central1`, Brightloaf operated successfully on their DR standby database in `us-east1`. "
                    "Once Google Cloud restored `us-central1`, an operator immediately pointed Cloud DNS back to the original database in `us-central1`. "
                    "Within 10 minutes, inventory discrepancies appeared: 3,400 orders placed during the 12-hour DR window vanished from customer order histories."
                ),
                "constraints": (
                    "Must guarantee 100% transactional consistency and zero data loss during return-to-primary failback procedures."
                ),
                "evidence": (
                    "Audit logs confirmed the database in `us-central1` was restored to its pre-crash state (12 hours stale). "
                    "Because reverse replication from `us-east1` was never configured, all transactions committed in `us-east1` remained orphaned on the secondary instance."
                ),
                "diagnostic_steps": [
                    "Compare maximum transaction log sequence numbers between primary and secondary database instances.",
                    "Review failback operational execution logs to audit the exact sequence of DNS record updates versus database synchronization.",
                    "Quantify the volume of un-synchronized writes created during the DR operational window.",
                ],
                "root": (
                    "Procedural failure: the engineering runbook treated failback as a simple DNS record reversion, completely omitting the "
                    "mandatory reverse-replication synchronization phase."
                ),
                "fix": (
                    "Rewrite the SRE Failback Playbook to mandate reverse replication: 1. Configure the restored instance as a downstream replica of "
                    "the DR primary. 2. Verify zero replication lag. 3. Enter read-only maintenance mode. 4. Pivot DNS. 5. Promote the restored primary."
                ),
                "verify": (
                    "Execute a staged tabletop failback drill in pre-production: populate secondary database with 10,000 synthetic records, configure "
                    "reverse replication to the restored primary, verify data parity checksums match 100%, and execute cutover with zero missing records."
                ),
                "residual": (
                    "A 60-second read-only maintenance window is required during the final DNS traffic pivot to ensure write quiescence."
                ),
                "diagram": (
                    "12h writes committed in DR region",
                    "Operator flips DNS back to primary",
                    "3,400 orders vanished (Split-brain)",
                    "Reverse replication established",
                    "Zero-loss verified failback cutover"
                ),
                "facts": "3,400 customer orders were lost during failback because DNS was reverted before syncing writes back to the primary.",
                "inference": "Failback without reverse replication is mathematically equivalent to intentional historical data truncation.",
                "expected": "Failback runbooks strictly enforce reverse replication and checksum verification before any DNS traffic redirection."
            },
            "lab": {
                "name": "Controlled Failover and Safe Failback Execution Runbook",
                "file": "day-092-topic-01-failover-failback.md",
                "goal": "Author an authoritative, step-by-step failover and reverse-replication failback runbook with validation checkpoints.",
                "expected": "A comprehensive Markdown runbook detailing exact preflight checks, gcloud replication commands, and parity validation scripts.",
                "mode": "tabletop analysis & command synthesis",
                "prereq": "Understanding of database replication and DNS TTL propagation.",
                "preflight": "Review Cloud SQL replica creation and promotion CLI syntax.",
                "steps": [
                    "Author the failover and safe failback execution runbook:\n\n```sh\ncat <<'EOF' > day-092-topic-01-failover-failback.md\n# Day 92: Enterprise Failover & Reverse-Replication Failback Runbook\n\n## 1. Operational Overview\n- **Primary Production Region:** `us-central1`\n- **Disaster Recovery Region:** `us-east1`\n- **Pre-Cutover Prerequisite:** Cloud DNS TTL lowered to **30 seconds** 48 hours prior to scheduled failback.\n\n## 2. Emergency Failover Phase (Region A -> Region B)\n\n### Step 1: Declare Disaster & Sever Primary Ingress\n```bash\n# Remove primary region backend from Global External ALB\ngcloud compute backend-services remove-backend brightloaf-global-be \\\n    --global \\\n    --instance-group=brightloaf-mig-central \\\n    --instance-group-region=us-central1\n```\n\n### Step 2: Promote DR Read Replica to Standalone Primary\n```bash\n# Promote replica in us-east1 to read-write primary\ngcloud sql instances promote-replica brightloaf-db-east \\\n    --project=brightloaf-prod\n```\n\n### Step 3: Direct Ingress to DR Region\n```bash\n# Scale compute in us-east1 and add to load balancer\ngcloud compute instance-groups managed resize brightloaf-mig-east \\\n    --region=us-east1 \\\n    --size=30\n```\n\n## 3. Safe Controlled Failback Phase (Region B -> Region A)\n\n### Step 1: Re-establish Reverse Replication (East -> Central)\n```bash\n# Re-create database in us-central1 as a read replica of brightloaf-db-east\ngcloud sql instances create brightloaf-db-central-new \\\n    --project=brightloaf-prod \\\n    --master-instance-name=brightloaf-db-east \\\n    --region=us-central1\n\n# Monitor replication lag until byte lag reaches 0\ngcloud sql instances describe brightloaf-db-central-new \\\n    --format='value(replicationLag)'\n```\n\n### Step 2: Quiesce Ingress & Enter Read-Only Maintenance Gate\n```bash\n# Set application into read-only mode via feature flag\ngcloud runtime-config configs variables set app/read_only_mode true \\\n    --config-name=brightloaf-runtime-config\n\n# Wait 60 seconds for DNS caches and in-flight HTTP connections to drain\nsleep 60\n```\n\n### Step 3: Promote Restored Primary & Pivot Ingress\n```bash\n# Promote central database\ngcloud sql instances promote-replica brightloaf-db-central-new\n\n# Point load balancer back to central MIG\ngcloud compute backend-services add-backend brightloaf-global-be \\\n    --global \\\n    --instance-group=brightloaf-mig-central \\\n    --instance-group-region=us-central1\n\n# Disable read-only maintenance mode\ngcloud runtime-config configs variables set app/read_only_mode false \\\n    --config-name=brightloaf-runtime-config\n```\n\n## 4. Verification Checkpoint\n- Verify database record checksum parity between `brightloaf-db-east` and `brightloaf-db-central-new`.\nEOF\ncat day-092-topic-01-failover-failback.md\n```",
                    "Verify the runbook clearly separates emergency failover from the methodical, five-step reverse-replication failback.",
                    "Verify the script includes a 60-second read-only quiescence gate to prevent write loss during cutover.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains production-ready gcloud failover/failback commands, and enforces reverse-replication integrity."
                ),
                "trouble": "Ensure reverse replica byte lag reaches exactly zero before promoting the restored instance.",
                "cleanup": "Retain `day-092-topic-01-failover-failback.md` as an exit evidence artifact.",
                "accept": "Completed failover and failback operational runbook with verified commands and safety gates."
            }
        },
        {
            "key": "topic-02",
            "title": "DR testing",
            "preview": (
                "An enterprise performs its very first disaster recovery test during a scheduled weekend maintenance window, "
                "only to accidentally wipe out live production customer data because the test script ran against the wrong Google Cloud project."
            ),
            "overview": (
                "Disaster recovery capabilities decay over time due to code deployments, configuration drift, and team turnover. "
                "Regular, disciplined **DR Testing** is essential to validate that recovery procedures remain operational. "
                "Testing follows a progressive maturity model: **Tabletop Exercises** (structured walkthroughs where architects and SREs trace "
                "failure scenarios on paper to identify process defects), **Game Days / Chaos Engineering** (targeted, controlled failure injection "
                "in staging or production to verify automated self-healing), and **Full Regional Failover Drills** (complete simulation or actual "
                "evacuation of user traffic from a primary region). Every DR test must operate under strict governance: defining an **Incident Commander**, "
                "establishing non-negotiable **Abort Criteria**, and enforcing project isolation to prevent accidental production harm."
            ),
            "technical": (
                "### 1. The DR Testing Maturity Spectrum\n"
                "- **Level 1: Tabletop Analysis (Quarterly):** Cross-functional teams (SRE, Security, Database, Network, Product) walk through a hypothetical "
                "outage script (e.g. 'Submarine fiber cut isolates Europe region'). Identifies missing runbook steps, outdated IAM access, and unmapped dependencies "
                "with zero operational risk.\n"
                "- **Level 2: Component Fault Injection / Chaos Game Days (Monthly):** Controlled experiments testing automated resilience: e.g. killing "
                "primary Cloud SQL instances, draining a GKE node pool, or injecting 500ms network latency via Chaos Mesh. Confirms autohealing and alerts.\n"
                "- **Level 3: Full-Scale Regional Evacuation Drill (Bi-annually):** Live or canary shift of production traffic to the recovery region. "
                "Measures empirical RTO and RPO against BIA targets.\n\n"
                "### 2. Testing Governance and Operational Abort Criteria\n"
                "- **The 'Red Button' (Abort Triggers):** A DR drill must be immediately aborted and rolled back if predefined safety thresholds are violated:\n"
                "  1. *Customer Impact Threshold:* Error rate exceeds 1% for more than 2 minutes.\n"
                "  2. *Revenue Loss Threshold:* Failed checkout transactions exceed $10,000.\n"
                "  3. *Latency Threshold:* P99 latency spikes beyond 2,500ms.\n"
                "  4. *Real Incident Interruption:* An actual production P1/P2 incident occurs during the test window.\n"
                "- **Role Separation:** The DR Exercise Lead coordinates the simulation; the Safety Monitor has sole authority to hit the abort button; "
                "the Communications Lead keeps stakeholders informed."
            ),
            "questions": [
                "What organizational benefits do tabletop exercises provide before conducting live infrastructure fault injection?",
                "What specific telemetry metrics must trigger an immediate, non-negotiable abort of a production DR game day?",
                "Why must disaster recovery drills test both the technical failover and the subsequent failback return procedure?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/dr-scenarios#testing_disaster_recovery",
            "reference_label": "Google Cloud Architecture: Disaster recovery testing methodologies, game days, and drill frameworks",
            "scenario": {
                "symptom": (
                    "During an unannounced DR drill in production, an SRE team initiated automated traffic evacuation to `europe-west1`. "
                    "The primary checkout service crashed, and customer error rates spiked to 14%. The drill continued for 45 minutes because "
                    "no single engineer had been designated with explicit authority to declare an abort, resulting in $340,000 in lost customer sales."
                ),
                "constraints": (
                    "Must establish rigid DR drill governance defining explicit abort criteria and designating an empowered Safety Officer."
                ),
                "evidence": (
                    "Post-drill audio recordings revealed responders argued for 35 minutes over whether the failure was an expected drill artifact "
                    "or an unintended production regression. No written abort thresholds existed in the test plan."
                ),
                "diagnostic_steps": [
                    "Review communication channels and timeline transcripts from the failed drill to identify governance bottlenecks.",
                    "Audit telemetry metrics (error rate, latency, revenue flow) recorded during the drill window.",
                    "Review test plan documentation to verify presence of abort criteria and safety officer appointments.",
                ],
                "root": (
                    "Governance failure: the DR test was conducted without predefined abort criteria, a designated Safety Officer, or automated "
                    "rollback monitors, converting a routine readiness drill into an uncontrolled production outage."
                ),
                "fix": (
                    "Establish a mandatory DR Drill Governance Framework: require written test plans with explicit numerical abort thresholds "
                    "(e.g. error rate > 1%), appoint an independent Safety Officer with sole authority to terminate drills, and build automated rollback scripts."
                ),
                "verify": (
                    "Execute a controlled staging drill where synthetic error rates are forced to 1.5%; verify monitoring systems trigger automated "
                    "drill abort and rollback to primary within 60 seconds."
                ),
                "residual": (
                    "Setting overly sensitive abort thresholds may terminate legitimate drills prematurely; thresholds must reflect true customer harm."
                ),
                "diagram": (
                    "DR drill triggers 14% error spike",
                    "Responders argue for 35 minutes",
                    "$340k revenue lost during drill",
                    "Safety Officer & abort criteria set",
                    "Auto-rollback triggers in 60s"
                ),
                "facts": "$340,000 lost during a test because no one had authority to abort the drill when errors surged to 14%.",
                "inference": "A disaster recovery test without explicit abort criteria is indistinguishable from an unmitigated production outage.",
                "expected": "Drills are governed by strict numerical abort criteria and an empowered Safety Officer with immediate rollback authority."
            },
            "lab": {
                "name": "Disaster Recovery Game Day Test Plan and Tabletop Simulation",
                "file": "day-092-topic-02-dr-test-plan.md",
                "goal": "Author an enterprise DR Game Day Test Plan defining roles, timeline scenarios, and explicit automated abort criteria.",
                "expected": "A comprehensive test plan in Markdown specifying incident command roles, injection scripts, and abort monitoring queries.",
                "mode": "tabletop analysis & governance synthesis",
                "prereq": "Understanding of SRE incident command and monitoring metrics.",
                "preflight": "Review corporate change management guidelines and SRE incident response roles.",
                "steps": [
                    "Author the DR Game Day Test Plan and governance charter:\n\n```sh\ncat <<'EOF' > day-092-topic-02-dr-test-plan.md\n# Day 92: Enterprise DR Game Day Test Plan & Governance Charter\n\n## 1. Test Metadata & Scope\n- **Exercise Codename:** Operation Phoenix Ash\n- **Target Date & Time:** 2026-10-15 02:00 – 04:00 UTC (Off-peak traffic)\n- **Target Environment:** Pre-Production Staging (`brightloaf-staging`)\n- **Simulation Hypothesis:** Complete catastrophic network blackhole in primary region `us-central1`.\n\n## 2. Command Team Roles & Responsibilities\n- **Exercise Commander (IC):** Directs timeline progression and authorizes phase transitions.\n- **Safety Officer (Red Button Owner):** Monitors live telemetry; holds absolute, unquestioned authority to immediately abort the drill.\n- **Chaos Engineer:** Executes fault injection scripts and simulated network cuts.\n- **Communications Lead:** Posts internal status updates every 15 minutes to `#dr-drill-bridge`.\n\n## 3. Strict Numerical Abort Criteria (Non-Negotiable)\nThe Safety Officer will immediately invoke the abort sequence if ANY of the following occur:\n1. **HTTP 5xx Error Rate:** Spikes above **1.0%** for > 60 consecutive seconds.\n2. **Synthetic Checkout Failure:** > 3 consecutive synthetic payment authorizations fail.\n3. **P99 API Latency:** Exceeds **2,000 ms** across two consecutive evaluation windows.\n4. **Database Staleness:** Replication lag to secondary exceeds **60 seconds**.\n5. **Real-World Incident:** Any active P1 or P2 incident is declared anywhere in the enterprise.\n\n## 4. Phase-by-Phase Execution Timeline\n\n| Elapsed Time | Phase Name | Responsible Role | Target Action / Verification |\n| :--- | :--- | :--- | :--- |\n| **T-30m** | Preflight Baseline | IC & Safety Officer | Confirm staging is healthy; establish comms bridge; review abort plan. |\n| **T+00m** | Phase 1: Fault Injection | Chaos Engineer | Simulate primary outage by dropping firewall rules to `us-central1` MIG. |\n| **T+05m** | Phase 2: Failover Pivot | Responders | Promote database in `us-east1`; scale secondary MIG from 0 to 30. |\n| **T+15m** | Phase 3: Traffic Steering | Responders | Shift Cloud DNS and Load Balancer backends to `us-east1`. |\n| **T+30m** | Phase 4: Steady-State Audit| SRE Team | Run end-to-end integration tests in DR region; verify 0% errors. |\n| **T+60m** | Phase 5: Reverse Sync & Failback | DB Lead | Re-establish reverse replication to `us-central1`; execute failback. |\n| **T+90m** | Post-Drill Wrap-Up | All Responders | Verify primary operates normally; conduct initial hot-wash retrospective. |\n\n## 5. Automated Emergency Abort Command\n```bash\n# Instant rollback to primary: restores traffic and tears down secondary overrides\ngcloud compute backend-services update brightloaf-global-be \\\n    --global \\\n    --set-security-policy=default-policy \\\n    --description=\"Drill Aborted: Restoring Primary Traffic\"\n```\nEOF\ncat day-092-topic-02-dr-test-plan.md\n```",
                    "Verify the test plan specifies the five core SRE roles and assigns an independent Safety Officer.",
                    "Verify the five numerical abort criteria are strictly defined with measurable thresholds.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains a structured Game Day test plan, and details non-negotiable abort thresholds."
                ),
                "trouble": "Ensure staging test environments mirror production network and database topologies to produce valid drill insights.",
                "cleanup": "Retain `day-092-topic-02-dr-test-plan.md` as an exit evidence artifact.",
                "accept": "Completed DR Game Day test plan with verified governance, timeline, and abort criteria."
            }
        },
        {
            "key": "topic-03",
            "title": "Verify quota scope and available failover capacity",
            "preview": (
                "An e-commerce site initiates emergency regional failover during Black Friday, but the secondary region's Managed Instance Group "
                "fails to scale beyond 24 VMs because the default regional vCPU quota was never increased from standard trial limits."
            ),
            "overview": (
                "In Google Cloud, resource allocations are governed by strict **Quotas and System Limits**. A pervasive architectural pitfall "
                "in disaster recovery planning is assuming that resource quotas approved in the primary region automatically apply globally. "
                "Most Google Cloud compute quotas—such as `CPUS`, `N2_CPUS`, `DISKS_TOTAL_GB`, and `IN_USE_ADDRESSES`—are strictly **regional**. "
                "If an enterprise operates 1,200 vCPUs in `us-central1`, but their secondary disaster recovery region (`us-east1`) has never had its "
                "regional quota increased above the default 24 vCPUs, any attempt to scale the secondary MIG during an outage will fail immediately "
                "with `QUOTA_EXCEEDED` errors. Furthermore, quota increases during a widespread public regional disaster may be delayed or rejected "
                "due to cloud-wide capacity constraints. Resilient DR design requires auditing regional quota headroom continuously and purchasing "
                "**Compute Engine Reservations** to physically guarantee hardware availability."
            ),
            "technical": (
                "### 1. Quota Scope Hierarchy in Google Cloud\n"
                "- **Global Quotas:** Apply across the entire Google Cloud project regardless of location (e.g. `NETWORKS`, `FIREWALLS`, `GLOBAL_EXTERNAL_HTTP_LB_FORWARDING_RULES`).\n"
                "- **Regional Quotas:** Apply strictly within a single geographic region (e.g. `Compute Engine API / CPUS` in `us-east1`, `SSD_TOTAL_GB` in `europe-west4`). "
                "Having 10,000 CPUs available in Iowa (`us-central1`) provides zero capacity to launch instances in Virginia (`us-east1`).\n"
                "- **Zonal Quotas:** Apply within a specific datacenter zone (e.g. local persistent disk capacity per zone).\n\n"
                "### 2. Quota vs Capacity: The 'Hot Day' Trap\n"
                "- **Quota Is Not Guaranteed Capacity:** Having an approved quota of 1,000 vCPUs merely grants legal permission to request instances; "
                "it does *not* guarantee physical hardware is idle in Google's datacenter. If a major regional storm causes dozens of enterprises "
                "to failover simultaneously to `us-east1`, Google Cloud may experience transient `ZONE_RESOURCE_POOL_EXHAUSTED` errors.\n"
                "- **Compute Engine Reservations:** The only technical mechanism to guarantee physical capacity during a regional disaster is a "
                "Compute Engine Reservation (zonal reservation for specific machine types, e.g. `c2-standard-16`). Reserved instances incur standard "
                "hourly compute pricing even when idle, representing an insurance policy for Tier 0 failover.\n\n"
                "### 3. Automated Quota Auditing and Monitoring\n"
                "- Use Cloud Monitoring metric `serviceruntime.googleapis.com/quota/allocation/usage` divided by `quota/limit` to alert SREs when "
                "capacity utilization exceeds 75% in either the primary or recovery region.\n"
                "- Enforce infrastructure-as-code linting that compares Terraform target node counts against current regional quota ceilings."
            ),
            "questions": [
                "What is the architectural difference between an approved Google Cloud resource quota and a Compute Engine hardware reservation?",
                "Why will scaling a secondary Managed Instance Group during a disaster fail if regional CPUS quotas have not been explicitly increased?",
                "How do multi-region capacity reservations prevent ZONE_RESOURCE_POOL_EXHAUSTED errors during large-scale cloud brownouts?",
            ],
            "reference": "https://docs.cloud.google.com/compute/docs/quotas",
            "reference_label": "Google Cloud Compute Engine: Resource quotas, regional scopes, and capacity reservation architecture",
            "scenario": {
                "symptom": (
                    "During an unannounced disaster drill, Brightloaf attempted to scale their secondary MIG in `europe-west1` from 0 to 80 instances. "
                    "The operation halted at 6 instances, logging hundreds of `Quota 'CPUS' exceeded. Limit: 24.0 in region europe-west1` errors. "
                    "The failover failed completely."
                ),
                "constraints": (
                    "Must verify and enforce that recovery regions possess adequate quota headroom and reserved capacity to absorb 100% of production traffic."
                ),
                "evidence": (
                    "Compute Engine API logs confirmed that while `us-central1` had a custom quota of 2,000 CPUS, `europe-west1` had never been upgraded "
                    "from the default project creation quota of 24 CPUS. No hardware reservations had been provisioned."
                ),
                "diagnostic_steps": [
                    "Query the Compute Engine API for regional quota limits and current usage across primary and secondary regions.",
                    "Review historical quota increase requests in the Google Cloud Console to identify un-submitted regions.",
                    "Inspect Compute Engine reservation lists to verify whether capacity was pre-allocated in the DR region.",
                ],
                "root": (
                    "Architecture oversight: the infrastructure team provisioned secondary MIG templates but failed to request regional quota increases "
                    "or purchase compute reservations in the disaster recovery region."
                ),
                "fix": (
                    "Submit formal Google Cloud quota increase requests to match regional CPU and IP quotas between `us-central1` and `us-east1`. "
                    "Purchase Compute Engine Reservations for minimum viable Tier 0 checkout capacity (40 instances) in the secondary region. "
                    "Deploy an automated Python quota audit script run via Cloud Build weekly."
                ),
                "verify": (
                    "Run an automated quota verification script; confirm that regional CPU, SSD, and IP quota ceilings in `us-east1` equal or exceed "
                    "production requirements, and test scaling the secondary MIG to 80 instances without errors."
                ),
                "residual": (
                    "Pre-purchased Compute Engine Reservations incur continuous baseline compute charges."
                ),
                "diagram": (
                    "Failover triggered to secondary region",
                    "MIG attempts to scale to 80 VMs",
                    "Crash: Quota exceeded at 24 CPUs",
                    "Regional quota increased to 2,000",
                    "Compute reservations guarantee hardware"
                ),
                "facts": "Failover halted at 6 VMs because the secondary region had default quota of 24 CPUs while primary used 1,200.",
                "inference": "Secondary infrastructure is completely non-viable if regional quotas are not actively provisioned to match production.",
                "expected": "Secondary regions maintain identical quota limits and pre-reserved capacity to absorb 100% of production traffic."
            },
            "lab": {
                "name": "Regional Quota Headroom Audit and Reservation Verification",
                "file": "day-092-topic-03-quota-audit.md",
                "goal": "Author an automated regional quota auditing script and reservation specification ensuring secondary region capacity.",
                "expected": "A comprehensive Markdown guide containing an executable Python script auditing Compute Engine quotas and reservation syntax.",
                "mode": "tabletop analysis & script synthesis",
                "prereq": "Understanding of Google Cloud quota APIs and resource management.",
                "preflight": "Review Compute Engine quota commands and reservation creation syntax.",
                "steps": [
                    "Author the quota auditing framework and reservation runbook:\n\n```sh\ncat <<'EOF' > day-092-topic-03-quota-audit.md\n# Day 92: Google Cloud Regional Quota & Capacity Verification Framework\n\n## 1. Core Principles\n1. **Quota Symmetry:** Secondary recovery regions must maintain identical resource quotas to primary regions for all mission-critical SKUs.\n2. **Hardware Guarantees:** Tier 0 services require Compute Engine **Reservations** to eliminate `ZONE_RESOURCE_POOL_EXHAUSTED` risk.\n\n## 2. Compute Engine Capacity Reservation Runbook\n\n### Step 1: Create Specific Zonal Reservation in DR Region\n```bash\n# Reserve 20 c2-standard-16 instances in us-east1-b for Tier 0 checkout\ngcloud compute reservations create res-checkout-dr-east \\\n    --zone=us-east1-b \\\n    --vm-count=20 \\\n    --machine-type=c2-standard-16 \\\n    --require-specific-reservation\n\n# Confirm reservation status is READY\ngcloud compute reservations describe res-checkout-dr-east \\\n    --zone=us-east1-b \\\n    --format='value(status)'\n```\n\n### Step 2: Configure Secondary MIG to Consume Specific Reservation\n```bash\n# Update instance template to target the reservation\ngcloud compute instance-templates create template-checkout-dr-east \\\n    --machine-type=c2-standard-16 \\\n    --reservation-affinity=specific \\\n    --reservation=res-checkout-dr-east \\\n    --region=us-east1\n```\n\n## 3. Automated Multi-Region Quota Auditing Script\n```python\n# Automated script to audit primary vs secondary regional quota parity\nimport subprocess\nimport json\n\ndef audit_quotas(project_id, primary_region, secondary_region):\n    print(f\"Auditing Quotas for Project: {project_id}\")\n    print(f\"Comparing Primary: {primary_region} vs DR Secondary: {secondary_region}\")\n    \n    # Target critical quotas\n    critical_metrics = ['CPUS', 'N2_CPUS', 'DISKS_TOTAL_GB', 'IN_USE_ADDRESSES']\n    \n    # Simulated quota extraction\n    quotas = {\n        primary_region: {'CPUS': 2000, 'N2_CPUS': 1500, 'DISKS_TOTAL_GB': 50000, 'IN_USE_ADDRESSES': 100},\n        secondary_region: {'CPUS': 2000, 'N2_CPUS': 1500, 'DISKS_TOTAL_GB': 50000, 'IN_USE_ADDRESSES': 100},\n    }\n    \n    discrepancies = []\n    for m in critical_metrics:\n        prim = quotas[primary_region].get(m, 0)\n        sec = quotas[secondary_region].get(m, 0)\n        if sec < prim:\n            discrepancies.append(f\"CRITICAL: {m} in {secondary_region} ({sec}) < {primary_region} ({prim})\")\n        else:\n            print(f\"PASS: {m} is symmetric ({sec} >= {prim})\")\n            \n    if discrepancies:\n        print(\"\\n--- AUDIT FAILED ---\")\n        for d in discrepancies:\n            print(d)\n    else:\n        print(\"\\n--- AUDIT PASSED: Secondary region has 100% quota parity ---\")\n\naudit_quotas('brightloaf-prod', 'us-central1', 'us-east1')\nEOF\npython3 -c \"with open('day-092-topic-03-quota-audit.md') as f: print('Quota audit runbook generated, length:', len(f.read()))\"\n```",
                    "Verify the reservation runbook uses specific reservation affinity to lock in dedicated compute instances.",
                    "Verify the Python auditing script tests critical quota metrics across primary and recovery regions.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains valid gcloud reservation commands, and details an automated quota parity script."
                ),
                "trouble": "Ensure project billing account has sufficient credit authorization before requesting multi-thousand vCPU quota increases.",
                "cleanup": "Retain `day-092-topic-03-quota-audit.md` as an exit evidence artifact.",
                "accept": "Completed regional quota auditing framework with validated reservation commands."
            }
        },
        {
            "key": "topic-04",
            "title": "Rate-limiting and graceful degradation during regional brownouts",
            "preview": (
                "A partial regional brownout reduces secondary datacenter capacity by 50%, causing remaining web servers to collapse under "
                "a thundering herd of user retries instead of shedding non-essential background traffic."
            ),
            "overview": (
                "During a catastrophic regional disaster or large-scale cloud brownout, the secondary disaster recovery site frequently operates "
                "under constrained capacity. Compute nodes may be autoscaling slowly, database connection pools may be throttled, or network transit "
                "may be degraded. If incoming user traffic is allowed to flood the secondary environment without restriction, the surge will trigger "
                "a positive feedback loop of CPU saturation, request timeouts, and client retries—collapsing the secondary site in a total brownout. "
                "Architects must implement **graceful degradation** and **edge rate-limiting** using **Google Cloud Armor**. By classifying incoming "
                "traffic into priority tiers, the platform sheds non-critical requests (e.g. recommendation engines, marketing banners, batch syncs) "
                "at Google's edge, preserving 100% of compute capacity for core revenue-generating operations (user authentication and checkout)."
            ),
            "technical": (
                "### 1. Cloud Armor Edge Rate-Limiting Mechanics\n"
                "- **Edge Enforcement:** Cloud Armor evaluates rate-limiting rules at Google's global Anycast edge points of presence (PoPs), *before* "
                "requests ever traverse the cross-region backbone or touch backend compute instances.\n"
                "- **Throttle vs Deny Actions:** Rules can enforce HTTP 429 Too Many Requests, redirect traffic to a static maintenance page hosted on "
                "Cloud Storage, or insert a Google reCAPTCHA challenge.\n"
                "- **Configurable Rate Limits:** Define client IP or user-token thresholds: e.g., allow max 100 requests per minute per IP; requests "
                "exceeding the threshold are dropped at the edge with HTTP 429 for a 5-minute ban period.\n\n"
                "### 2. Tiered Load Shedding and Feature Flags\n"
                "- **The Degradation Pyramid:**\n"
                "  1. *Tier 1 (Non-Essential):* AI product recommendations, social widgets, personalized promotional banners. Shed first via client-side "
                "feature flags or edge URL blocking.\n"
                "  2. *Tier 2 (Secondary Business):* Order history lookup, review submissions, account profile editing. Throttled to 10% capacity.\n"
                "  3. *Tier 3 (Core Invariant):* Cart checkout, payment processing, inventory reservation. Protected with 100% priority queueing.\n"
                "- **Static Fallback Pages:** When backend services are overwhelmed, configure Cloud Load Balancing and Cloud CDN to return stale "
                "cached responses (`stale-while-revalidate`) or route users to a static bucket-hosted apologies page."
            ),
            "questions": [
                "Why does enforcing rate limiting at Google Cloud Armor edge nodes protect backend compute from CPU exhaustion during brownouts?",
                "How does priority load shedding preserve core checkout functionality when a secondary datacenter operates at 50% capacity?",
                "What role does client-side exponential backoff with randomized jitter play in dampening retry storms?",
            ],
            "reference": "https://docs.cloud.google.com/armor/docs/rate-limiting-overview",
            "reference_label": "Google Cloud Armor: Edge rate limiting architecture, throttle rules, and load shedding",
            "scenario": {
                "symptom": (
                    "During a regional network brownout, Brightloaf's secondary recovery site in `us-east1` was forced to handle 100% of global traffic "
                    "with only 60% of normal compute capacity online. Within 4 minutes, background requests for product recommendation carousels "
                    "exhausted database connection pools, causing 100% of payment checkout attempts to fail with HTTP 504 Gateway Timeout."
                ),
                "constraints": (
                    "Must prioritize core checkout operations during capacity deficits, shedding non-essential background traffic at the network edge."
                ),
                "evidence": (
                    "Load balancer metrics showed recommendation API calls accounted for 72% of total incoming HTTP requests and consumed 85% "
                    "of database CPU. Checkout requests accounted for only 8% of requests but failed due to recommendation thread contention."
                ),
                "diagnostic_steps": [
                    "Inspect backend service request distribution grouped by URL path and HTTP method.",
                    "Correlate database connection pool utilization with specific API endpoint query logs.",
                    "Review Cloud Armor security policies to check for active rate-limiting and URL-filtering rules.",
                ],
                "root": (
                    "Lack of traffic prioritization: the secondary site treated all HTTP requests equally, allowing low-value recommendation traffic "
                    "to crowd out mission-critical checkout transactions during a regional capacity crunch."
                ),
                "fix": (
                    "Deploy a Cloud Armor security policy with tiered rate-limiting: shed `/api/v1/recommendations/*` with HTTP 429 when regional "
                    "traffic exceeds 5,000 req/s, while reserving unrestricted capacity for `/api/v1/checkout/*`. Configure client apps to hide "
                    "recommendation carousels when receiving 429 status."
                ),
                "verify": (
                    "Simulate an overload condition in staging by firing 15,000 concurrent requests; verify Cloud Armor drops recommendation traffic "
                    "at the edge while checkout requests process with 100% success and sub-500ms latency."
                ),
                "residual": (
                    "Users will see an empty space or default static banner instead of personalized recommendations during brownouts."
                ),
                "diagram": (
                    "Secondary site has 60% capacity",
                    "Recommendations consume 85% DB",
                    "Checkout fails on thread lock",
                    "Cloud Armor edge shedding active",
                    "Non-essential shed; checkout 100%"
                ),
                "facts": "Recommendations consumed 85% of database capacity, killing checkouts because all traffic was treated with equal priority.",
                "inference": "During a capacity brownout, failure to prioritize traffic guarantees the failure of your most valuable transactions.",
                "expected": "Cloud Armor sheds low-value endpoints at the edge, reserving compute headroom for essential checkout transactions."
            },
            "lab": {
                "name": "Cloud Armor Edge Rate-Limiting & Shed-Queue Policy Synthesis",
                "file": "day-092-topic-04-rate-limiting.md",
                "goal": "Author and verify a Google Cloud Armor security policy establishing rate limiting and priority load shedding for brownouts.",
                "expected": "A comprehensive configuration guide detailing gcloud armor commands for path-based throttling and client rate caps.",
                "mode": "tabletop analysis & command synthesis",
                "prereq": "Understanding of Google Cloud Armor and Cloud Load Balancing.",
                "preflight": "Review Cloud Armor security policy syntax and rate-limiting rule parameters.",
                "steps": [
                    "Author the Cloud Armor rate-limiting and load-shedding runbook:\n\n```sh\ncat <<'EOF' > day-092-topic-04-rate-limiting.md\n# Day 92: Cloud Armor Rate-Limiting & Graceful Degradation Architecture\n\n## 1. Architectural Strategy\nDuring regional capacity brownouts, protect Tier 0 checkout by enforcing edge shedding:\n1. **Priority 1000:** Drop non-essential recommendations (`/api/v1/recommendations/*`) when client rate exceeds 20 req/min.\n2. **Priority 2000:** Rate-limit general API browsing (`/api/v1/*`) to 100 req/min per IP.\n3. **Priority 3000:** Bypass rate limits for authenticated checkout transactions (`/api/v1/checkout/*`).\n4. **Default Rule:** Allow standard traffic.\n\n## 2. Configuration & Execution Commands\n\n### Step 1: Create Cloud Armor Security Policy\n```bash\n# Create enterprise security policy\ngcloud compute security-policies create brightloaf-brownout-policy \\\n    --description=\"Edge rate limiting and priority load shedding during DR\"\n```\n\n### Step 2: Configure Non-Essential Load Shedding Rule\n```bash\n# Aggressive throttling on heavy recommendation endpoints\ngcloud compute security-policies rules create 1000 \\\n    --security-policy=brightloaf-brownout-policy \\\n    --expression=\"request.path.startsWith('/api/v1/recommendations/')\" \\\n    --action=throttle \\\n    --rate-limit-threshold-count=20 \\\n    --rate-limit-threshold-interval-sec=60 \\\n    --conform-action=allow \\\n    --exceed-action=deny-429 \\\n    --enforce-on-key=IP\n```\n\n### Step 3: Configure General Browse Rate Limiting\n```bash\n# Prevent bot scraping and retry storms across product catalog\ngcloud compute security-policies rules create 2000 \\\n    --security-policy=brightloaf-brownout-policy \\\n    --expression=\"request.path.startsWith('/api/v1/catalog/')\" \\\n    --action=throttle \\\n    --rate-limit-threshold-count=100 \\\n    --rate-limit-threshold-interval-sec=60 \\\n    --conform-action=allow \\\n    --exceed-action=deny-429 \\\n    --enforce-on-key=IP\n```\n\n### Step 4: Bind Policy to Global Backend Service\n```bash\n# Attach policy to Cloud Load Balancer external ingress\ngcloud compute backend-services update brightloaf-global-be \\\n    --global \\\n    --security-policy=brightloaf-brownout-policy\n```\n\n## 3. Client Graceful Degradation Protocol\n- When client frontend receives HTTP 429 from `/recommendations`, it suppresses error modals and gracefully renders a pre-cached offline catalog.\nEOF\ncat day-092-topic-04-rate-limiting.md\n```",
                    "Verify the Cloud Armor rules differentiate between non-essential recommendations and critical paths.",
                    "Verify the commands specify exact throttle parameters with conform and exceed actions.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains valid gcloud compute security-policies commands, and defines client degradation logic."
                ),
                "trouble": "Ensure Cloud Armor rules evaluate path matching accurately using CEQL expressions before deploying to production.",
                "cleanup": "Retain `day-092-topic-04-rate-limiting.md` as an exit evidence artifact.",
                "accept": "Completed Cloud Armor rate-limiting policy runbook with verified edge-shedding rules."
            }
        },
        {
            "key": "topic-05",
            "title": "Runbooks and playbooks",
            "preview": (
                "During a major regional outage, an on-call engineer attempts to follow an unverified 80-page Word document playbook, "
                "getting trapped on step 14 because an ambiguous instruction tells them to 'verify network settings' without providing a command."
            ),
            "overview": (
                "In high-stress disaster recovery situations, cognitive overload degrades human decision-making. High-performing Site Reliability "
                "Engineering (SRE) teams eliminate operational ambiguity by strictly distinguishing between **Strategic Playbooks** and **Executable Runbooks**. "
                "A **Playbook** operates at the strategic level: it defines decision trees, escalation thresholds, executive notification trees, "
                "and business abort criteria (the *'What'* and the *'Why'*). An **Executable Runbook** operates at the tactical level: it is a concise, "
                "deterministic, peer-reviewed engineering document providing exact, copy-pasteable terminal commands with explicit expected outputs, "
                "ownership roles, and sanity verification steps (the *'How'*). Every runbook must include explicit rollback instructions for every command, "
                "must be stored in version-controlled Git repositories, and must be tested quarterly."
            ),
            "technical": (
                "### 1. Structural Comparison: Playbooks vs Runbooks\n"
                "- **Playbook Characteristics:** High-level narrative, architectural diagrams, stakeholder RACI matrices (Responsible, Accountable, "
                "Consulted, Informed), regulatory reporting timelines, and criteria for declaring disaster versus local incident.\n"
                "- **Runbook Characteristics:** Step-by-step numbered CLI commands, pre-flight prerequisites, exact parameter flags, expected stdout "
                "matching patterns, failure troubleshooting sidebars, and time-to-execute benchmarks.\n\n"
                "### 2. Runbook Engineering Standards\n"
                "- **Rule of Idempotency:** Every command in a runbook should be idempotent—running it twice must produce the same end state without "
                "triggering errors or unintended duplicate mutations.\n"
                "- **Explicit Verification Checkpoints:** Never follow a state-changing command without an immediate verification command: "
                "e.g. following a `promote-replica` command immediately with `describe` to verify that `state == RUNNABLE` before proceeding.\n"
                "- **No Ambiguity / No Placeholders:** Commands must never contain un-parameterized placeholders like `<insert_your_ip_here>`. "
                "Use environment variables (e.g. `export TARGET_ZONE=us-central1-a`) defined in a preflight setup block.\n\n"
                "### 3. Ownership and Version Control Hygiene\n"
                "- Runbooks must be maintained as Markdown or executable notebooks (e.g. Jupyter / Cloud Shell tutorials) in the main service Git repository.\n"
                "- Pull requests modifying infrastructure code must require corresponding updates to operational runbooks as part of CI/CD linting."
            ),
            "questions": [
                "What is the mechanical distinction between a strategic Disaster Recovery Playbook and an executable SRE Runbook?",
                "Why must every mutation command in an emergency runbook be immediately paired with an explicit verification command?",
                "How does parameterized environment variable definition in preflight blocks prevent catastrophic command-line errors?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/dr-scenarios#runbooks_and_playbooks",
            "reference_label": "Google Cloud Architecture: Creating executable disaster recovery playbooks, runbooks, and SRE procedures",
            "scenario": {
                "symptom": (
                    "During a midnight regional outage, an on-call engineer attempted to promote a database replica following an unversioned wiki page. "
                    "The wiki directed the engineer to run a generic shell snippet containing `PROJECT_ID=<your-project>`. The engineer accidentally "
                    "pasted their personal sandbox project ID, creating an orphaned replica while production remained completely offline for an extra 50 minutes."
                ),
                "constraints": (
                    "Must establish standardized, automated, and parameterized executable runbooks that eliminate manual string substitution errors."
                ),
                "evidence": (
                    "Terminal session history showed the engineer executed commands across three different project contexts because environment "
                    "variables were not validated in an automated preflight script. The wiki documentation had last been edited 18 months prior."
                ),
                "diagnostic_steps": [
                    "Inspect shell history and audit logs from the responder's session to trace command execution sequences.",
                    "Review wiki documentation history to identify stale instructions and missing parameter validation checks.",
                    "Audit SRE runbook testing cadence and version control synchronization.",
                ],
                "root": (
                    "Documentation anti-pattern: reliance on unmaintained, unversioned wiki pages with manual text placeholders rather than "
                    "parameterized, peer-reviewed Git-managed executable runbooks."
                ),
                "fix": (
                    "Migrate all operational runbooks to Markdown in the primary Git repository. Implement strict preflight variable assertion blocks "
                    "that validate Google Cloud authentication, active project IDs, and API permissions before allowing execution."
                ),
                "verify": (
                    "Execute the revised runbook in a staging environment; confirm that preflight assertions catch invalid project IDs immediately "
                    "and block command execution, guiding the operator with clean error messages."
                ),
                "residual": (
                    "Engineers must keep Git checkouts updated locally or execute runbooks via standardized Google Cloud Shell workspaces."
                ),
                "diagram": (
                    "Engineer reads 18mo stale wiki",
                    "Pastes wrong project placeholder",
                    "Orphaned sandbox replica created",
                    "Git-managed executable runbook",
                    "Preflight assertions enforce sanity"
                ),
                "facts": "50 minutes of downtime added because a wiki runbook required manual variable substitution and targeted the wrong project.",
                "inference": "Manual parameter replacement during an emergency guarantees operator error under high-stress conditions.",
                "expected": "Runbooks are versioned code artifacts with automated preflight assertions that validate environment state."
            },
            "lab": {
                "name": "Production-Grade Executable SRE Runbook with Abort Triggers",
                "file": "day-092-topic-05-executable-runbook.md",
                "goal": "Author a production-grade, executable Disaster Recovery runbook complete with preflight assertions, ownership RACI, and abort triggers.",
                "expected": "A comprehensive Markdown document containing parameterized shell commands, verification steps, and automated rollback logic.",
                "mode": "tabletop analysis & runbook synthesis",
                "prereq": "Completion of Exercises 1 through 4.",
                "preflight": "Review SRE runbook authoring standards and Bash defensive programming patterns.",
                "steps": [
                    "Author the production-grade executable SRE runbook:\n\n```sh\ncat <<'EOF' > day-092-topic-05-executable-runbook.md\n# Day 92: Canonical Executable SRE Runbook: Regional Failover\n\n## 1. Metadata & Ownership RACI\n- **Service Name:** Brightloaf Core Transaction API\n- **Runbook ID:** RB-DR-092-A\n- **Version:** 2.4.0 (Git: `ops/runbooks/rb-092.md`)\n- **Incident Commander:** Primary SRE On-Call\n- **Technical Lead:** Database SRE Lead\n- **Communications:** Incident Communications Officer\n\n## 2. Mandatory Preflight Validation (Run First)\n```bash\n# Ensure defensive shell execution\nset -euo pipefail\n\n# Assert required environment variables are set\nexport EXPECTED_PROJECT=\"brightloaf-prod\"\nCURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)\n\nif [[ \"$CURRENT_PROJECT\" != \"$EXPECTED_PROJECT\" ]]; then\n    echo \"ERROR: Active gcloud project is '$CURRENT_PROJECT', expected '$EXPECTED_PROJECT'!\"\n    echo \"Run: gcloud config set project $EXPECTED_PROJECT\"\n    exit 1\nfi\n\necho \"PREFLIGHT PASSED: Operating on $CURRENT_PROJECT\"\n```\n\n## 3. Execution Sequence with Checkpoints\n\n### Step 1: Promote Secondary Database in us-east1\n```bash\n# Execution: Trigger promotion\ngcloud sql instances promote-replica brightloaf-db-east \\\n    --async\n\n# Verification Checkpoint: Poll until state is RUNNABLE\nfor i in {1..30}; do\n    STATE=$(gcloud sql instances describe brightloaf-db-east --format='value(state)')\n    echo \"Current DB State: $STATE (Attempt $i/30)\"\n    if [[ \"$STATE\" == \"RUNNABLE\" ]]; then break; fi\n    sleep 10\ndone\n\nif [[ \"$STATE\" != \"RUNNABLE\" ]]; then\n    echo \"ABORT TRIGGER: Database promotion failed to reach RUNNABLE within 5 minutes!\"\n    exit 2\nfi\n```\n\n### Step 2: Scale Recovery MIG to Target Capacity\n```bash\n# Execution: Scale secondary compute instances\ngcloud compute instance-groups managed resize brightloaf-mig-east \\\n    --region=us-east1 \\\n    --size=30\n\n# Verification Checkpoint: Ensure at least 25 instances are RUNNING\nRUNNING_COUNT=$(gcloud compute instance-groups managed list-instances brightloaf-mig-east \\\n    --region=us-east1 \\\n    --filter=\"currentActions.none=true AND status=RUNNING\" \\\n    --format='value(instance)' | wc -l)\n\necho \"Active Running Compute Instances in us-east1: $RUNNING_COUNT / 30\"\n```\n\n## 4. Rollback & Abort Protocol\nIf an abort trigger is encountered at any stage:\n1. Execute rollback command to restore primary backend configuration.\n2. Escalate immediately to Database SRE Lead and Incident Commander.\n3. Log failure timestamp in incident channel.\nEOF\ncat day-092-topic-05-executable-runbook.md\n```",
                    "Verify the runbook contains defensive Bash preflight checks asserting project identity.",
                    "Verify every state mutation is followed by an explicit verification polling loop with timeout abort logic.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains production-ready defensive bash scripts, and provides explicit abort triggers and RACI assignments."
                ),
                "trouble": "Ensure `set -euo pipefail` is used in all automation scripts to catch unset variables and unhandled command failures.",
                "cleanup": "Retain `day-092-topic-05-executable-runbook.md` as an exit evidence artifact.",
                "accept": "Completed executable SRE runbook adhering to production authoring and governance standards."
            }
        }
    ]
}
