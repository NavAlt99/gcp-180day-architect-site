"""day_data_090.py — Exhaustive architecture data specification for Day 90.

Covers Recovery Targets and Disaster Recovery Patterns:
1. RTO and RPO definitions, Business Impact Analysis (BIA), tier classifications, and MTD.
2. Disaster Recovery patterns: Backup and Restore, Pilot Light, Warm Standby, Hot Standby / Active-Active.
3. Cost vs RTO/RPO trade-off matrix, Annualized Loss Expectancy (ALE), and DR Architectural Decision Record (ADR).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 90

DATA = {
    "day": 90,
    "part1_intro": (
        "Day 90 shifts our architectural lens from continuous high availability to catastrophic disaster recovery (DR). "
        "High availability hedges against localized component faults—such as host crashes, disk degradation, or single-zone network "
        "partitions—within an operational region. Disaster recovery prepares for existential regional disruptions: prolonged power outages, "
        "natural catastrophes, fiber severed across metropolitan corridors, or destructive administrative errors that wipe out an entire "
        "cloud region. Today's curriculum establishes business-derived recovery targets—Recovery Time Objective (RTO) and Recovery Point "
        "Objective (RPO)—through rigorous Business Impact Analysis (BIA), evaluates the four classic cloud DR archetypes (Backup & Restore, "
        "Pilot Light, Warm Standby, and Multi-Region Active-Active), and models the steep exponential cost curve balancing infrastructure "
        "spend against acceptable business loss."
    ),
    "exit_summary": (
        "Engineered an enterprise Disaster Recovery Architecture and Decision Framework: established quantifiable RTO/RPO tiers via Business "
        "Impact Analysis; authored an Architectural Decision Record (ADR) evaluating Backup & Restore, Pilot Light, Warm Standby, and Hot Standby; "
        "synthesized an annualized financial model comparing idle compute spend against Annualized Loss Expectancy (ALE); generated runnable "
        "DR orchestration automation for regional workload activation."
    ),
    "part2_intro": (
        "Disaster recovery planning is a financial and operational discipline before it is a technology implementation. "
        "The sections below define BIA mathematical formulas, contrast cloud DR structural topologies, and detail exact cost-recovery matrices."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>DR Pattern Archetype</th>
      <th>Target RTO Window</th>
      <th>Target RPO Window</th>
      <th>Relative Cost Factor</th>
      <th>Compute &amp; Data Infrastructure Topology</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Backup &amp; Restore (Cold)</strong></td>
      <td><strong>24 – 48 Hours</strong></td>
      <td><strong>12 – 24 Hours</strong></td>
      <td><strong>1.0x – 1.1x</strong> (Baseline)</td>
      <td>Zero standby compute; nightly Cloud Storage dual-region backups; infrastructure codified in Terraform.</td>
    </tr>
    <tr>
      <td><strong>Pilot Light</strong></td>
      <td><strong>1 – 4 Hours</strong></td>
      <td><strong>&lt; 15 Minutes</strong></td>
      <td><strong>1.3x – 1.6x</strong></td>
      <td>Continuous database replication (Cloud SQL read replica); core networks pre-provisioned; compute MIG at 0 instances.</td>
    </tr>
    <tr>
      <td><strong>Warm Standby</strong></td>
      <td><strong>5 – 15 Minutes</strong></td>
      <td><strong>&lt; 1 Minute</strong></td>
      <td><strong>1.8x – 2.2x</strong></td>
      <td>Scaled-down compute running continuously (e.g. 20% MIG capacity); primary-standby database synchronization.</td>
    </tr>
    <tr>
      <td><strong>Hot Standby / Active-Active</strong></td>
      <td><strong>&lt; 30 Seconds</strong> (Sub-second)</td>
      <td><strong>RPO = 0</strong> (Synchronous)</td>
      <td><strong>2.8x – 3.5x+</strong></td>
      <td>100% capacity deployed across dual regions; Anycast Load Balancing; Cloud Spanner multi-region Paxos consensus.</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 90: Disaster Recovery Spectrum: Cost vs RTO/RPO Trade-Off Curve",
        "desc": "Spectrum diagram mapping disaster recovery patterns from Cold Backup to Multi-Region Active-Active against cost and latency.",
        "caption": "Figure 90.1: Four-tier disaster recovery continuum demonstrating inverse relationship between recovery time and infrastructure expenditure.",
        "nodes": [
            ("1. Backup & Restore", "Cold Standby\\nRTO: 24h | RPO: 24h | Cost: $"),
            ("2. Pilot Light", "Data Replicated, Compute 0\\nRTO: 2h | RPO: 15m | Cost: $$"),
            ("3. Warm Standby", "Scaled-Down Secondary\\nRTO: 10m | RPO: 1m | Cost: $$$"),
            ("4. Multi-Region Hot", "Active-Active Anycast\\nRTO: 0s | RPO: 0s | Cost: $$$$"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "RTO and RPO definitions and how business impact analysis produces them",
            "preview": (
                "An e-commerce enterprise adopts a 4-hour RTO policy chosen arbitrarily by an infrastructure architect, only to discover "
                "during a regional blackout that four hours of downtime violates contractual merchant agreements and triggers $1.2M in SLA penalties."
            ),
            "overview": (
                "Disaster recovery targets cannot be invented by IT engineers; they must be derived from a rigorous **Business Impact Analysis (BIA)**. "
                "The **Recovery Time Objective (RTO)** defines the maximum acceptable duration of service interruption between the declaration of "
                "a disaster and the full restoration of normal business operations. The **Recovery Point Objective (RPO)** defines the maximum "
                "acceptable age of data that can be permanently lost when an outage occurs, measured back from the instant of failure. "
                "BIA systematically calculates the cost of downtime over time—incorporating unrecoverable revenue loss, contractual SLA default fees, "
                "regulatory fines, and customer churn. By mapping **Maximum Tolerable Downtime (MTD)** and **Work Recovery Time (WRT)** across "
                "business processes, architects classify workloads into clear recovery tiers that guide infrastructure spend."
            ),
            "technical": (
                "### 1. BIA Core Terminology and Mathematical Relationships\n"
                "- **Maximum Tolerable Downtime (MTD):** The absolute longest duration a business process can remain broken before the company "
                "suffers catastrophic, irreversible financial ruin or regulatory charter revocation.\n"
                "- **RTO vs WRT:** Total downtime is the sum of technical system recovery (RTO) and operational work recovery time (WRT). "
                "The relationship is governed by the constraint: `RTO + WRT <= MTD`. For instance, if an inventory ledger can be offline for "
                "at most 6 hours (MTD), and warehouse staff require 2 hours to manually reconcile scanned barcodes (WRT), the cloud infrastructure "
                "RTO ceiling is strictly `6 - 2 = 4 hours`.\n"
                "- **RPO and Transaction Velocity:** RPO dictates the data replication frequency. If an application processes $50,000 in transactions "
                "every minute, an RPO of 15 minutes implies an acceptable risk of $750,000 in unrecoverable transactional state. In high-velocity "
                "financial systems, RPO must equal 0, necessitating synchronous distributed consensus.\n\n"
                "### 2. Workload Classification Tiers\n"
                "- **Tier 0 (Mission-Critical / Core Revenue):** Services whose failure immediately halts billing, checkout, or core safety systems. "
                "Targets: `RTO < 1 minute`, `RPO = 0`. Requires Multi-Region Active-Active or automated Warm Standby.\n"
                "- **Tier 1 (Business-Critical):** Customer-facing portals, inventory tracking, account management. Targets: `RTO < 30 minutes`, "
                "`RPO < 5 minutes`. Implemented via Pilot Light or automated regional failover.\n"
                "- **Tier 2 (Internal Operations):** Internal reporting, corporate analytics, employee expense reporting. Targets: `RTO < 4 hours`, "
                "`RPO < 24 hours`. Implemented via automated Backup & Restore.\n"
                "- **Tier 3 (Archival & Administrative):** Historical auditing, long-term compliance archives. Targets: `RTO < 48 hours`, "
                "`RPO < 7 days`. Retained in GCS Archive storage."
            ),
            "questions": [
                "Why must the sum of RTO and Work Recovery Time (WRT) never exceed Maximum Tolerable Downtime (MTD)?",
                "How does an asynchronous cross-region database replication stream create an RPO greater than zero?",
                "What empirical criteria determine whether a workload qualifies for Tier 0 versus Tier 1 classification?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/dr-scenarios",
            "reference_label": "Google Cloud Architecture Center: Disaster recovery planning guide and scenario evaluation",
            "scenario": {
                "symptom": (
                    "Following a regional cloud facility outage, Brightloaf's primary payment database in `us-central1` went dark. "
                    "Restoration from the latest nightly database snapshot in `us-east1` took 5 hours and 20 minutes. Due to the 18-hour-old "
                    "snapshot, 42,000 customer payment authorizations were lost, causing merchant partners to issue formal contractual default "
                    "notices totaling $850,000."
                ),
                "constraints": (
                    "Must establish defensible RTO and RPO targets grounded in audited business financial loss models rather than subjective assumptions."
                ),
                "evidence": (
                    "BIA audit revealed that payment processing revenue loss was $180,000 per hour, plus a $500,000 penalty if transactions were lost "
                    "beyond 5 minutes. The existing infrastructure configuration relied on nightly cold backups (RPO = 24h, RTO = 6h), completely "
                    "misaligned with the business MTD of 1 hour."
                ),
                "diagnostic_steps": [
                    "Perform a financial business impact analysis across payment processing, calculating hourly revenue loss and contractual SLA liabilities.",
                    "Audit current database backup schedules, snapshot frequencies, and cross-region replication latency.",
                    "Measure historical recovery time during staging snapshot restoration drills to establish baseline operational RTO.",
                ],
                "root": (
                    "The infrastructure team classified the payment service under a generic Tier 2 backup policy without conducting a formal "
                    "Business Impact Analysis, allowing a multi-million-dollar revenue stream to depend on cold 24-hour backup restores."
                ),
                "fix": (
                    "Reclassify the payment service as a Tier 0 workload with targets of `RTO < 5 minutes` and `RPO = 0`. Migrate the database tier "
                    "to a multi-region deployment or establish continuous cross-region Cloud SQL replication with automated failover alerting."
                ),
                "verify": (
                    "Conduct a tabletop BIA review with executive and legal stakeholders; confirm that the newly targeted 5-minute RTO and 0-minute RPO "
                    "satisfy all merchant agreements and eliminate SLA default risk."
                ),
                "residual": (
                    "Synchronous multi-region replication introduces 20-40ms additional write latency across regions due to speed-of-light physical boundaries."
                ),
                "diagram": (
                    "Generic Tier 2 policy applied",
                    "Regional disaster destroys DB",
                    "5h restore + 18h lost data",
                    "BIA performed: Tier 0 defined",
                    "RTO < 5m, RPO = 0 guaranteed"
                ),
                "facts": "42,000 transactions lost and $850,000 in contractual fines incurred because payment database used 24h cold backups.",
                "inference": "Setting DR targets without a Business Impact Analysis inevitably aligns infrastructure to cost rather than survival.",
                "expected": "Workloads are categorized by BIA into validated tiers, ensuring critical financial paths deploy zero-RPO replication."
            },
            "lab": {
                "name": "Enterprise Business Impact Analysis (BIA) and Tier Modeling",
                "file": "day-090-topic-01-bia-model.md",
                "goal": "Author a structured Business Impact Analysis (BIA) spreadsheet model and workload classification rubric.",
                "expected": "A comprehensive Markdown artifact defining financial loss formulas, MTD/WRT calculations, and tier assignment rules.",
                "mode": "tabletop analysis & model synthesis",
                "prereq": "Understanding of business SLAs and financial impact metrics.",
                "preflight": "Review corporate financial loss thresholds and regulatory downtime mandates.",
                "steps": [
                    "Author the Business Impact Analysis specification and tiering framework:\n\n```sh\ncat <<'EOF' > day-090-topic-01-bia-model.md\n# Day 90: Business Impact Analysis & Recovery Target Framework\n\n## 1. Financial Impact Loss Formulas\n- **Direct Revenue Loss per Hour ($L_{rev}$):** Average Hourly Sales Volume * Service Dependency Factor\n- **Labor Idle Cost ($L_{labor}$):** Number of Affected Employees * Average Hourly Fully-Loaded Cost\n- **Contractual SLA Penalty ($L_{sla}$):** Direct contract penalties incurred per hour of breach\n- **Total Cost of Downtime ($TCD$):** $TCD(t) = (L_{rev} + L_{labor}) \times t + L_{sla}(t)$\n\n## 2. Workload Classification Matrix\n\n| Classification Tier | Target Workloads | Max Tolerable Downtime (MTD) | Work Recovery Time (WRT) | Target RTO Ceiling | Target RPO Ceiling | Recommended GCP Pattern |\n| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n| **Tier 0: Mission Critical** | Core Checkout, Payment Gateway | 15 Minutes | 10 Minutes | **< 5 Minutes** | **RPO = 0** (Synchronous) | Multi-Region Active-Active / Spanner |\n| **Tier 1: Business Critical** | Inventory Search, User Accounts | 2 Hours | 30 Minutes | **< 60 Minutes** | **< 15 Minutes** | Pilot Light (Cross-region Cloud SQL replica) |\n| **Tier 2: Business Operational** | Warehouse Scanning, BI Ingestion | 8 Hours | 2 Hours | **< 4 Hours** | **< 4 Hours** | Warm Standby (MIG at 10% capacity) |\n| **Tier 3: Non-Critical Admin** | Internal Documentation, HR Wiki | 72 Hours | 8 Hours | **< 24 Hours** | **< 24 Hours** | Backup & Restore (Terraform + GCS dual-region) |\n\n## 3. Brightloaf Retail BIA Case Assessment\n- **Workload:** Retail Payment Gateway\n- **Hourly Revenue at Risk:** $180,000/hr\n- **Regulatory / Merchant Penalty:** $500,000 at $t > 15\\text{ min}$\n- **Calculated MTD:** 15 minutes\n- **Assigned Tier:** Tier 0 (Mandatory active cross-region data replication, automated failover)\nEOF\ncat day-090-topic-01-bia-model.md\n```",
                    "Verify the BIA artifact explicitly derives RTO from MTD and WRT formulas.",
                    "Verify the four workload tiers have distinct, non-overlapping operational targets.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains clear mathematical downtime formulas, and establishes a four-tier classification system."
                ),
                "trouble": "Ensure RTO + WRT does not exceed MTD for any defined workload tier.",
                "cleanup": "Retain `day-090-topic-01-bia-model.md` as an exit evidence artifact.",
                "accept": "Completed BIA framework document with validated workload classification rubrics."
            }
        },
        {
            "key": "topic-02",
            "title": "DR patterns",
            "preview": (
                "An organization attempts to execute a disaster recovery failover using an unmaintained Pilot Light deployment, "
                "only to find that outdated compute templates cannot launch because disk images lack modern application libraries."
            ),
            "overview": (
                "Cloud computing offers four fundamental Disaster Recovery patterns, each representing a distinct balance of operational "
                "readiness, technical complexity, and financial expenditure. In **Backup and Restore (Cold Standby)**, systems are rebuilt "
                "from scratch using backups stored in dual-region Cloud Storage buckets. In **Pilot Light**, core data is continuously replicated "
                "to the secondary region, but compute infrastructure is dormant (zero instances) until a disaster is formally declared. "
                "In **Warm Standby**, a scaled-down, functional duplicate of the production environment runs 24/7 in the recovery region, capable "
                "of taking immediate production traffic upon rapid autoscaling. Finally, in **Hot Standby / Multi-Region Active-Active**, full "
                "production capacity is deployed across geographically separated regions simultaneously, routing live user traffic continuously "
                "through Global Anycast Load Balancers."
            ),
            "technical": (
                "### 1. Backup and Restore (Cold Standby)\n"
                "- **Mechanics:** Relies on GCS dual-region buckets or Turbo Replication, Compute Engine persistent disk snapshots, and declarative "
                "Terraform configurations stored in remote Git repositories.\n"
                "- **Failover Sequence:** 1. Detect disaster. 2. Execute Terraform to spin up VPCs, subnets, and Managed Instance Groups in the recovery "
                "region. 3. Restore databases from snapshot/storage dumps. 4. Update DNS. RTO: 12–48 hours; RPO: 12–24 hours.\n"
                "- **Key Failure Modes:** Terraform drifts out of sync with production; underlying GCP compute quotas are insufficient in the recovery "
                "region; snapshot restoration times scale linearly with disk size.\n\n"
                "### 2. Pilot Light Pattern\n"
                "- **Mechanics:** The 'spark' that always burns is the data layer. A Cloud SQL cross-region read replica or standby instance receives "
                "continuous asynchronous replication. Network VPCs, firewalls, and subnets are pre-provisioned. Compute instance templates are registered, "
                "but the Managed Instance Group target size is set to `0` (or `1` for continuous canary testing).\n"
                "- **Failover Sequence:** 1. Promote database read-replica to primary using the promote-replica command. 2. Scale MIG size "
                "from 0 to 100% capacity using the managed resize command. 3. Point application to promoted database. RTO: 30–120 minutes; "
                "RPO: < 15 minutes.\n\n"
                "### 3. Warm Standby Pattern\n"
                "- **Mechanics:** A scaled-down version of the application (e.g., 20% capacity) runs continuously in the secondary region. It handles "
                "internal testing or minor read-only traffic. Database standby is online and actively tracking the primary.\n"
                "- **Failover Sequence:** 1. Promote standby database to primary. 2. Autoscale MIG to 100% capacity. 3. Shift traffic via Load Balancer "
                "or Cloud DNS. RTO: 5–15 minutes; RPO: < 1 minute.\n\n"
                "### 4. Hot Standby / Multi-Region Active-Active\n"
                "- **Mechanics:** Workloads run at full production capacity across two or more regions (e.g. `us-central1` and `us-east1`). An External "
                "Global Application Load Balancer steers traffic using Anycast. Cloud Spanner provides globally synchronous, externally consistent writes "
                "via Paxos consensus.\n"
                "- **Failover Sequence:** Transparent and automated. If a region fails, the load balancer health checks detect backend loss within "
                "5–10 seconds and automatically route 100% of global traffic to surviving regions. RTO: 0 seconds; RPO: 0 seconds."
            ),
            "questions": [
                "What operational maintenance tasks are required to prevent a Pilot Light pattern's instance templates from becoming obsolete?",
                "How does the promotion of an asynchronous Cloud SQL replica differ between Warm Standby and Hot Standby patterns?",
                "Why does a Multi-Region Active-Active pattern require synchronous database consensus (e.g. Cloud Spanner) rather than standard read replicas?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/dr-scenarios#disaster_recovery_scenarios",
            "reference_label": "Google Cloud Architecture: Disaster recovery patterns and technical scenarios",
            "scenario": {
                "symptom": (
                    "During an unannounced DR drill, Brightloaf attempted to activate a Pilot Light environment in `europe-west4`. "
                    "The automation script scaled the secondary MIG from 0 to 50 VMs, but 100% of instances failed to boot because the startup script "
                    "attempted to download an outdated package repository URL that had been deprecated 8 months earlier."
                ),
                "constraints": (
                    "Must ensure disaster recovery compute and application templates remain continuously tested and verified without operator intervention."
                ),
                "evidence": (
                    "Instance serial console logs showed `apt-get update failed with HTTP 404 Not Found`. The compute template had not been updated "
                    "since the initial Pilot Light setup 9 months prior, while production CI/CD pipelines had deployed 140 software versions."
                ),
                "diagnostic_steps": [
                    "Inspect failed instance console outputs to identify startup script and dependency failure points.",
                    "Review CI/CD deployment pipelines to determine whether multi-region images and instance templates are updated on every release.",
                    "Audit recovery region resource quota and image repository connectivity.",
                ],
                "root": (
                    "Configuration drift: CI/CD deployment pipelines updated only the primary region instance templates, leaving the Pilot Light "
                    "recovery templates in a stale, unbootable state."
                ),
                "fix": (
                    "Integrate multi-region template baking into the core CI/CD pipeline: every production release must build, test, and register "
                    "Golden Machine Images and Regional Instance Templates across both primary and recovery regions. Run an automated weekly canary boot drill."
                ),
                "verify": (
                    "Trigger an automated weekly pipeline that boots a single canary instance in the Pilot Light region, executes smoke tests, "
                    "verifies API connectivity, and terminates the canary."
                ),
                "residual": (
                    "Continuous weekly canary boot drills incur minor Compute Engine instance execution charges."
                ),
                "diagram": (
                    "CI/CD updates primary region only",
                    "Pilot Light template drifts 9mo",
                    "Disaster drill fails with 404 boot",
                    "CI/CD bakes dual-region images",
                    "Weekly automated canary boot test"
                ),
                "facts": "Pilot Light failover failed because secondary region instance templates were 9 months out of date and failed to boot.",
                "inference": "Dormant infrastructure inevitably drifts into broken states unless exercised by continuous automated testing.",
                "expected": "CI/CD deploys templates symmetrically to all DR regions; automated weekly canaries prove boot readiness."
            },
            "lab": {
                "name": "Pilot Light to Full Recovery Activation Runbook",
                "file": "day-090-topic-02-pilot-light-drill.md",
                "goal": "Author and test a complete, deterministic Pilot Light activation runbook that promotes read replicas and scales dormant compute.",
                "expected": "A structured Markdown runbook with exact gcloud commands executing preflight checks, replica promotion, and MIG scaling.",
                "mode": "tabletop analysis & command synthesis",
                "prereq": "Understanding of Cloud SQL replication and Compute Engine Managed Instance Groups.",
                "preflight": "Review Cloud SQL promote-replica syntax and MIG resizing parameters.",
                "steps": [
                    "Author the Pilot Light failover activation runbook:\n\n```sh\ncat <<'EOF' > day-090-topic-02-pilot-light-drill.md\n# Day 90: Pilot Light Activation & Recovery Orchestration Runbook\n\n## 1. Architecture Topology\n- **Primary Region:** `us-central1` (Production live compute + Primary Cloud SQL)\n- **Recovery Region:** `us-east1` (Dormant MIG target size = 0, Cross-region Cloud SQL read replica)\n\n## 2. Controlled Activation Runbook\n\n### Step 1: Verify Replication Lag Before Promotion\n```bash\n# Check byte lag and replication status on recovery replica\ngcloud sql instances describe brightloaf-db-replica-east \\\n    --format='value(state, replicationLag)'\n# Acceptable threshold: byte lag < 100KB\n```\n\n### Step 2: Sever Replication & Promote Replica to Standalone Primary\n```bash\n# Promote read replica to independent read-write primary\ngcloud sql instances promote-replica brightloaf-db-replica-east\n\n# Confirm instance state transitions to RUNNABLE\ngcloud sql instances describe brightloaf-db-replica-east \\\n    --format='value(state)'\n```\n\n### Step 3: Scale Dormant Compute MIG to Target Capacity\n```bash\n# Resize recovery MIG from 0 to production capacity (e.g. 20 instances)\ngcloud compute instance-groups managed resize brightloaf-be-mig-east \\\n    --region=us-east1 \\\n    --size=20\n\n# Wait for instances to reach RUNNING state\ngcloud compute instance-groups managed list-instances brightloaf-be-mig-east \\\n    --region=us-east1\n```\n\n### Step 4: Update Backend Service and Steer Ingress\n```bash\n# Add recovery MIG to Global External Application Load Balancer backend service\ngcloud compute backend-services add-backend brightloaf-global-backend \\\n    --global \\\n    --instance-group=brightloaf-be-mig-east \\\n    --instance-group-region=us-east1 \\\n    --balancing-mode=UTILIZATION \\\n    --max-utilization=0.8\n```\n\n## 3. Post-Activation Integrity Verification\n- Run smoke test against shallow health endpoint: GET /healthz/shallow\n- Verify write transaction: Execute test order checkout via administrative token\nEOF\ncat day-090-topic-02-pilot-light-drill.md\n```",
                    "Verify the runbook commands follow the exact sequence: replica lag verification -> promotion -> MIG scaling -> LB binding.",
                    "Verify the script includes post-activation integrity verification steps.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains production-ready gcloud failover commands, and specifies measurable integrity checkpoints."
                ),
                "trouble": "Ensure replica promotion is completely finished before scaling compute instances to avoid database connection errors.",
                "cleanup": "Retain `day-090-topic-02-pilot-light-drill.md` as an exit evidence artifact.",
                "accept": "Completed Pilot Light activation runbook with verified command syntax and sequence."
            }
        },
        {
            "key": "topic-03",
            "title": "Cost vs RTO/RPO trade-off for each pattern",
            "preview": (
                "An engineering team defaults to deploying full Multi-Region Active-Active across three continents for all internal microservices, "
                "inflating the monthly cloud bill by $450,000 to protect services that generate less than $5,000 in monthly business value."
            ),
            "overview": (
                "The relationship between disaster recovery targets and infrastructure cost is strictly exponential. Reducing RTO from 24 hours "
                "to 1 hour increases costs modestly (primarily for snapshot replication and storage). However, reducing RTO from 1 hour to 0 seconds "
                "and RPO to 0 requires a quantum leap in architectural spend: 100% duplicate provisioned compute capacity, multi-region database licenses "
                "(such as Cloud Spanner), high-volume cross-region network egress, and redundant interconnect circuits. Architects must perform a "
                "disciplined financial trade-off analysis comparing the **Annualized Cost of Protection (ACP)** against the **Annualized Loss Expectancy (ALE)**. "
                "When ACP exceeds ALE, the architecture is economically indefensible. Formalizing these findings into an **Architectural Decision Record (ADR)** "
                "ensures transparent alignment between engineering reality and executive financial risk tolerance."
            ),
            "technical": (
                "### 1. Financial Loss Modeling: ALE, SLE, and ARO\n"
                "- **Single Loss Expectancy (SLE):** The total financial loss incurred from a single regional outage event. `SLE = Asset Value * Exposure Factor + Downtime Loss`.\n"
                "- **Annualized Rate of Occurrence (ARO):** The estimated statistical probability of a regional disaster occurring within a 12-month period "
                "(e.g., ARO for a total AWS/GCP regional failure is typically estimated at 0.05 to 0.1, or once every 10–20 years).\n"
                "- **Annualized Loss Expectancy (ALE):** The expected annual financial loss without mitigation: `ALE = SLE * ARO`. If a regional outage "
                "costs $2,000,000 (SLE) and occurs once every 10 years (ARO = 0.1), the ALE is `$200,000/year`.\n"
                "- **Economic Feasibility Rule:** If implementing a Hot Standby pattern costs $500,000 per year, but the ALE is only $200,000/year, "
                "the company is over-insuring by $300,000 annually. A Pilot Light or Warm Standby costing $80,000/year represents the defensible optimum.\n\n"
                "### 2. Cost Drivers Across Google Cloud DR Tiers\n"
                "- **Compute Overhead:** Backup & Restore incurs 0% idle compute cost. Pilot Light incurs 0%–5% idle compute cost (canaries only). "
                "Warm Standby incurs 20%–40% compute cost. Hot Standby incurs 100%–150% duplicate compute cost.\n"
                "- **Data & Storage Costs:** Cross-region replication doubles persistent storage charges. Cloud Storage Turbo Replication incurs "
                "replication egress charges plus monthly storage multipliers. Cloud Spanner multi-region instance configurations require a minimum "
                "of 3 read-write regions, increasing node licensing significantly compared to single-region Cloud SQL.\n"
                "- **Network Egress:** Cross-region data transfer is charged per gigabyte. High-throughput database write replication streams "
                "can add thousands of dollars in monthly intra-cloud cross-region networking fees."
            ),
            "questions": [
                "Under what mathematical conditions does Annualized Cost of Protection (ACP) justify an Active-Active Hot Standby architecture?",
                "How do cross-region network egress charges impact the ongoing operational cost of continuous database replication?",
                "Why is Backup and Restore the most economically defensible pattern for Tier 2 and Tier 3 enterprise workloads?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/dr-scenarios#designing_for_cost_and_business_impact",
            "reference_label": "Google Cloud Architecture: Designing for cost, business impact, and recovery objectives",
            "scenario": {
                "symptom": (
                    "Brightloaf's finance leadership mandated a 30% reduction in cloud infrastructure spending after discovering that monthly cloud "
                    "costs spiked by $180,000 following an unvetted initiative to deploy all 40 microservices in an Active-Active multi-region topology."
                ),
                "constraints": (
                    "Must preserve Tier 0 sub-minute recovery for checkout while reducing overall disaster recovery expenditure across auxiliary services."
                ),
                "evidence": (
                    "Cost analysis showed that 35 out of 40 microservices were low-velocity back-office tools (e.g. employee cafeteria menu, store signage "
                    "sync, batch inventory reporting). Running duplicate GKE clusters and Cloud Spanner nodes for these services accounted for 82% "
                    "of the disaster recovery cost increase."
                ),
                "diagnostic_steps": [
                    "Perform workload categorization across all 40 services, aligning each with BIA business impact tiers.",
                    "Audit Google Cloud billing exports grouped by SKU, region, and network egress labels to isolate DR spend.",
                    "Calculate the Annualized Loss Expectancy (ALE) for each service to establish financial cost ceilings.",
                ],
                "root": (
                    "Architecture governance failure: a one-size-fits-all Active-Active mandate was applied indiscriminately across all workloads "
                    "without evaluating RTO/RPO requirements or comparing ACP against ALE."
                ),
                "fix": (
                    "Author an Architectural Decision Record (ADR) establishing a tiered DR policy: reserve Multi-Region Active-Active strictly for "
                    "Tier 0 checkout services; transition Tier 1 services to Pilot Light; downgrade Tier 2 and 3 services to automated Backup & Restore."
                ),
                "verify": (
                    "Model the revised multi-tier DR architecture in Google Cloud Pricing Calculator; confirm monthly cloud spend decreases by $145,000 "
                    "while checkout SLA (RTO < 1m, RPO = 0) remains fully satisfied."
                ),
                "residual": (
                    "Downgraded Tier 2 services will experience 2 to 4 hours of recovery latency during an actual regional disaster event."
                ),
                "diagram": (
                    "Unvetted Active-Active on 40 apps",
                    "$180k/mo cloud cost spike",
                    "Over-insuring low-value tools",
                    "Tiered DR ADR authored & adopted",
                    "Tier 0 Hot, Tier 1 Pilot, Tier 2 Cold"
                ),
                "facts": "$180,000/mo was spent running Active-Active for 40 services, 35 of which had zero customer revenue impact.",
                "inference": "Applying Tier 0 architecture to Tier 2 workloads wastes capital without delivering measurable business value.",
                "expected": "Workloads map to appropriate DR patterns via ADR, optimizing spend while protecting critical revenue paths."
            },
            "lab": {
                "name": "Disaster Recovery Architectural Decision Record (ADR) Formulation",
                "file": "day-090-topic-03-dr-adr.md",
                "goal": "Author an authoritative, production-grade Architectural Decision Record (ADR) balancing recovery targets against cloud costs.",
                "expected": "A comprehensive ADR in standard Michael Nygard format specifying pattern assignments, cost models, and trade-off matrices.",
                "mode": "tabletop analysis & ADR synthesis",
                "prereq": "Completion of Exercises 1 and 2.",
                "preflight": "Review ADR formatting guidelines and cloud pricing models.",
                "steps": [
                    "Author the Disaster Recovery Architectural Decision Record (ADR):\n\n```sh\ncat <<'EOF' > day-090-topic-03-dr-adr.md\n# ADR 090: Enterprise Disaster Recovery Pattern & Tier Assignment\n\n## Status\nApproved / Canonical Architecture Standard\n\n## Context\nBrightloaf operates 40 microservices across retail, e-commerce, and enterprise operations. Recent cloud billing reviews revealed an unsustainable $180,000/month cost increase due to uniform Multi-Region Active-Active deployment across all workloads. Furthermore, previous DR drills demonstrated that unmaintained standby templates drifted out of sync. We require a disciplined, cost-bounded Disaster Recovery framework grounded in Business Impact Analysis (BIA).\n\n## Decision Drivers\n1. **Business Criticality:** Protect Tier 0 revenue checkout ($180k/hr at risk, $500k SLA breach penalty).\n2. **Financial Pragmatism:** Annualized Cost of Protection (ACP) must not exceed Annualized Loss Expectancy (ALE).\n3. **Operational Maintainability:** Standby infrastructure must be continuously exercised to prevent drift.\n\n## Considered Options\n1. Uniform Multi-Region Active-Active for all services ($240,000/mo)\n2. Uniform Backup and Restore for all services ($15,000/mo)\n3. Tiered Hybrid Architecture: Hot Standby (Tier 0), Pilot Light (Tier 1), Backup & Restore (Tier 2/3) ($62,000/mo)\n\n## Decision\nWe adopt **Option 3: Tiered Hybrid Architecture**.\n- **Tier 0 (Core Checkout & Auth):** Hot Standby / Multi-Region Active-Active using Cloud Spanner and Global Anycast ALB. RTO < 30s, RPO = 0.\n- **Tier 1 (Customer Account & Catalog):** Pilot Light in `us-east1` with continuous Cloud SQL read replica and dormant MIG (size 0). RTO < 30m, RPO < 15m.\n- **Tier 2/3 (Internal Admin & Reporting):** Backup & Restore using GCS Dual-Region buckets with Turbo Replication and automated Terraform pipelines. RTO < 4h, RPO < 24h.\n\n## Cost & Trade-Off Matrix\n\n| Tier | Assigned Pattern | Monthly Spend | Target RTO | Target RPO | Justification |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n| **Tier 0** | Hot Standby | $38,000 | < 30s | RPO = 0 | Revenue loss ($180k/hr) justifies Spanner and duplicate compute. |\n| **Tier 1** | Pilot Light | $16,000 | < 30m | < 15m | Cross-region read replica provides low RPO; dormant compute saves $45k/mo. |\n| **Tier 2/3**| Backup & Restore | $8,000 | < 4h | < 24h | Non-critical batch reporting; 4-hour delay causes negligible business loss. |\n| **Total** | **Tiered Model** | **$62,000** | -- | -- | **Saves $178,000/month** compared to uniform Active-Active. |\n\n## Consequences & Compliance\n- Positive: Reduces annual cloud expenditure by $2.13M while providing ironclad RPO = 0 protection for revenue checkout.\n- Negative: Tier 1 failover requires a manual or semi-automated execution of the Pilot Light runbook (estimated 20-minute operational procedure).\n- Verification: CI/CD pipelines will execute automated weekly canary boot drills against the Pilot Light templates to ensure continuous operational readiness.\nEOF\ncat day-090-topic-03-dr-adr.md\n```",
                    "Verify the ADR adheres to standard architectural decision record conventions with context, decision, consequences, and cost trade-offs.",
                    "Verify the cost model demonstrates clear financial justification comparing Hot Standby, Pilot Light, and Backup & Restore.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains a fully formatted ADR, and provides rigorous quantitative justification for the tiered DR strategy."
                ),
                "trouble": "Ensure financial trade-offs in the ADR explicitly reference BIA findings from Topic 01.",
                "cleanup": "Retain `day-090-topic-03-dr-adr.md` as an exit evidence artifact.",
                "accept": "Completed DR Architectural Decision Record with validated cost and recovery trade-offs."
            }
        }
    ]
}
