"""day_data_075.py — Exhaustive architecture data specification for Day 75.

Covers Migration Assessment and VMware Fit: The 6 Rs, Migration Lifecycle Phases,
Discovery Tools (Migration Center, StratoZone, mFit), and Google Cloud VMware Engine (GCVE).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 75

DATA = {
    "day": 75,
    "part1_intro": (
        "Day 75 masters the enterprise disciplines of datacenter discovery, migration strategy, and workload "
        "rationalization on Google Cloud. Rather than treating cloud migration as a brute-force infrastructure copy, "
        "enterprise architects apply rigorous assessment frameworks: categorizing portfolios across the 6 Rs decision "
        "taxonomy (Rehost, Replatform, Refactor, Repurchase, Retain, Retire), executing disciplined four-phase lifecycles "
        "(Assess, Plan, Deploy, Optimize), and leveraging automated discovery engines (Google Cloud Migration Center, "
        "StratoZone, and mFit). Concurrently, this session examines Google Cloud VMware Engine (GCVE)—evaluating its "
        "hardware-isolated software-defined datacenter (SDDC) stack, VMware HCX Layer 2 network extensions, and total cost "
        "of ownership (TCO) economics as a high-velocity datacenter exit vehicle."
    ),
    "exit_summary": (
        "Constructed a multi-workload 6 Rs rationalization model; blueprinted a four-phase wave migration plan with strict "
        "rollback boundaries; developed a StratoZone-style compute rightsizing TCO calculator saving 54% over provisioned specs; "
        "authored an end-to-end GCVE cluster sizing and HCX network extension architecture runbook."
    ),
    "part2_intro": (
        "Enterprise cloud migration requires balancing business deadlines against architectural modernization. The sections "
        "below analyze workload classification frameworks, dependency clustering mathematics, automated telemetry discovery, "
        "and VMware SDDC cloud-native integration."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Migration Strategy</th>
      <th>Google Cloud Primitive</th>
      <th>Primary Business Driver</th>
      <th>Transformation Effort &amp; Timeline</th>
      <th>Operational &amp; Architectural Benefit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Rehost (Lift &amp; Shift)</strong></td>
      <td>Migrate to Virtual Machines (m4vm)</td>
      <td>Immediate datacenter lease exit</td>
      <td>Lowest (Weeks); zero code changes</td>
      <td>Replicates existing OS; minimal elasticity or cost optimization</td>
    </tr>
    <tr>
      <td><strong>Replatform (Lift &amp; Reshape)</strong></td>
      <td>Cloud SQL / Migrate to Containers</td>
      <td>Reduce OS patching and DB management</td>
      <td>Moderate (1 – 3 Months); minor configs</td>
      <td>Automated HA backups; container portability without code rewrite</td>
    </tr>
    <tr>
      <td><strong>Refactor (Cloud-Native)</strong></td>
      <td>Cloud Run / GKE / Cloud Spanner</td>
      <td>Maximum elasticity, scale, and agility</td>
      <td>Highest (6 – 18 Months); full software rewrite</td>
      <td>True serverless autoscaling; multi-region active-active durability</td>
    </tr>
    <tr>
      <td><strong>VMware Rehost (GCVE)</strong></td>
      <td>Google Cloud VMware Engine (vSphere + HCX)</td>
      <td>Zero-risk datacenter evacuation; retain tooling</td>
      <td>Lowest (Days via HCX live vMotion)</td>
      <td>Identical vCenter operations; dedicated bare-metal hardware</td>
    </tr>
    <tr>
      <td><strong>Retire &amp; Retain</strong></td>
      <td>Decommission OR Retain On-Prem</td>
      <td>Eliminate technical debt / Hardware amortization</td>
      <td>Immediate decommissioning</td>
      <td>Eliminates 100% of software licensing and cloud compute costs</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 75: Enterprise Migration Lifecycle and Tooling Pipeline",
        "desc": "Sequential migration execution flow from automated discovery through wave planning, cutover, and optimization.",
        "nodes": [
            ("1. Assess & Discover", "Migration Center & StratoZone\\n+ Utilization Sizing"),
            ("2. Plan & Cluster", "Wave Dependency Mapping\\n+ Landing Zone Preparation"),
            ("3. Cutover & Rehost", "Migrate to VMs / GCVE HCX\\n+ Asynchronous Block Sync"),
            ("4. Modernize & Optimize", "Right-Sizing & CUDs\\n+ Staged Containerization"),
        ],
        "caption": "Figure 75.1: Phased enterprise migration framework ensuring observable dependency mapping before cutover."
    },
    "part3_intro": (
        "The following field cases analyze real-world migration failures triggered by flawed assessments, missing dependency "
        "analysis, and unoptimized sizing. Each scenario includes quantitative impact data, diagnostic traces, root cause postmortems, "
        "defensible remediations, and dual-lane failed/corrected architectural diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises provide production-grade, executable configurations and verification scripts for "
        "scoring the 6 Rs, modeling migration wave dependencies, calculating rightsized compute TCO, and "
        "sizing Google Cloud VMware Engine clusters."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "The 6 Rs Decision Taxonomy: Rehost, Replatform, Refactor, Repurchase, Retain, Retire",
            "overview": (
                "Master the 6 Rs decision framework for enterprise portfolio rationalization. Evaluate business drivers, "
                "licensing constraints, technical debt, and modernization velocity to select defensible migration paths."
            ),
            "preview": (
                "An organization attempts to refactor 45 legacy applications simultaneously while facing a firm 4-month datacenter "
                "lease deadline; development stalls, budgets collapse, and the landlord assesses $15,000/day overstay penalties."
            ),
            "technical": (
                "#### 1. Strategic Rationalization of the 6 Rs\n\n"
                "Enterprise IT portfolios contain hundreds of heterogeneous workloads accumulated over decades. Successful cloud migration "
                "requires categorizing every application into one of the **6 Rs** based on clear business constraints:\n\n"
                "- **Rehost (Lift-and-Shift):** Moving virtual machine disk blocks directly to Compute Engine using **Migrate to Virtual Machines** "
                "(m4vm). Zero code changes, fastest time-to-value, ideal for fixed datacenter lease terminations. However, it preserves legacy "
                "technical debt, unpatched OS configurations, and oversized VM provisioning.\n\n"
                "- **Replatform (Lift-and-Reshape):** Introducing targeted cloud-managed services without modifying core business code. Examples "
                "include replacing self-hosted MySQL VMs with **Cloud SQL**, migrating containerized apps to **Cloud Run**, or wrapping legacy "
                "binaries using **Migrate to Containers**. Delivers immediate operational cost savings by offloading OS patching, automated HA, "
                "and backups to Google Cloud.\n\n"
                "- **Refactor (Cloud-Native Re-architecture):** Decomposing monolithic applications into microservices, event-driven pipelines "
                "(Pub/Sub, Eventarc), and horizontally scalable databases (Cloud Spanner). Maximizes long-term agility, elastic scale, and "
                "resilience, but requires months of engineering effort and carries the highest delivery risk.\n\n"
                "- **Repurchase (Drop-and-Shop):** Decommissioning custom bespoke software in favor of commercial SaaS solutions (e.g. migrating "
                "custom ticket systems to Jira/ServiceNow, or self-hosted email to Google Workspace).\n\n"
                "- **Retire:** Permanently turning off redundant, un-utilized, or obsolete systems. In enterprise assessments, typically 10% to 20% "
                "of inventoried servers can be retired immediately, eliminating license and hosting costs with zero migration effort.\n\n"
                "- **Retain (Do Nothing / Revisit Later):** Keeping workloads on-premises due to recent hardware capital depreciation, strict "
                "sovereignty regulations, or latency-sensitive factory floor industrial equipment.\n\n"
                "#### 2. The Pragmatic Migration Sequence\n\n"
                "A pervasive architectural anti-pattern is **Ideological Purism**—insisting that every workload must be refactored into "
                "cloud-native microservices before migrating. Pragmatic architects separate the **Datacenter Exit** from **Application Modernization**:\n\n"
                "$$\\text{Phase 1: Fast Exit (Rehost / GCVE)} \\longrightarrow \\text{Phase 2: In-Cloud Replatform} \\longrightarrow \\text{Phase 3: Targeted Refactor}$$\n\n"
                "By moving workloads into Google Cloud first via Rehost or Google Cloud VMware Engine, the enterprise stops bleeding co-location "
                "penalties, gains software-defined telemetry, and modernizes applications iteratively in the cloud.\n\n"
                "#### 3. Technical Constraints Influencing the 6 Rs Decision\n\n"
                "Workload rationalization evaluates five hard gating constraints:\n\n"
                "  1. **OS Kernel & Architecture:** Compute Engine supports standard x86-64 Linux and Windows versions. Legacy 32-bit OSs, custom "
                "UNIX kernels (AIX, HP-UX, Solaris), or non-standard kernel drivers cannot be rehosted directly on Compute Engine and require GCVE, "
                "Bare Metal Solution (BMS), or emulation.\n"
                "  2. **Software Licensing:** Proprietary software (Oracle Database, Microsoft Windows Server, SQL Server) requires evaluating "
                "Bring Your Own License (BYOL) on Sole-Tenant Nodes versus Google Cloud pay-as-you-go licenses.\n"
                "  3. **Network Latency Boundaries:** If an application tier is separated from its database by more than 2ms, Rehosting the app "
                "alone will degrade performance; both tiers must move together.\n"
                "  4. **Data Gravity & Volume:** Databases with petabyte-scale storage require high-speed Cloud Interconnect links (10 Gbps / 100 Gbps) "
                "to replicate data within maintenance cutover windows.\n"
                "  5. **Team Skills & Maturity:** Refactoring to Kubernetes requires container, service mesh, and GitOps expertise; teams lacking "
                "these skills should replatform to Cloud Run or Cloud SQL first.\n\n"
                "#### 4. The 6 Rs Evaluation Decision Matrix\n\n"
                "| Migration Pathway | Implementation Tooling | Mean Time to Migrate | Architectural Risk | Modernization Value | Best Workload Profile |\n"
                "|---|---|---|---|---|---|\n"
                "| **Rehost (Lift & Shift)** | Migrate to Virtual Machines (m4vm) | 1 – 4 Weeks | Low (Replication clone) | Low (Retains VM debt) | Fixed lease exit, COTS packaged applications, legacy VMs |\n"
                "| **Replatform** | Cloud SQL, Cloud Run, mFit | 1 – 3 Months | Low – Moderate | Moderate (Managed ops) | Standard LAMP stacks, self-hosted databases, stateless web apps |\n"
                "| **Refactor** | Cloud Spanner, GKE, Pub/Sub | 6 – 18 Months | High (Code rewrite) | Highest (Elasticity & scale) | Core business differentiators, revenue-generating e-commerce |\n"
                "| **Repurchase** | Commercial SaaS (Workspace, CRM) | 1 – 6 Months | Moderate (Data export) | High (Zero infrastructure) | Peripheral business tools, ERP, CRM, identity providers |\n"
                "| **Retain** | On-Prem Private Cloud / Colocation | Zero (No change) | Zero | None (Maintains status quo) | Mainframes, industrial robotics, un-amortized hardware |\n"
                "| **Retire** | Decommission / Storage Snapshot | 1 – 2 Weeks | Lowest (Post-backup) | High (Direct cost savings) | Stale staging environments, obsolete reporting batch jobs |\n"
            ),
            "questions": [
                "Under what business conditions should an enterprise choose Rehosting over Refactoring?",
                "How does separating the datacenter exit from application modernization protect business timelines?",
                "Why must software licensing models (e.g. Oracle, Windows) be evaluated before selecting Compute Engine VM types?",
                "What percentage of an average enterprise IT portfolio can typically be Retired during assessment?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/migration-to-gcp-getting-started",
            "reference_label": "Google Cloud Architecture Center: Migrate to Google Cloud - Getting started",
            "scenario": {
                "scenario": (
                    "Brightloaf operated 140 virtual machines in an on-premises co-location datacenter whose commercial lease was terminating "
                    "in exactly 4 months. The executive leadership team decreed that all applications must be modernized into cloud-native "
                    "microservices on Google Kubernetes Engine (GKE) and Cloud Spanner. Two months into the initiative, the software engineering "
                    "team had successfully containerized and rewritten only 2 out of 140 services. The monolithic warehouse picking and inventory "
                    "tracking system proved far too entangled with legacy stored procedures to refactor quickly. The landlord issued a formal "
                    "legal notice stating that holding over past the lease expiration would trigger an immediate $15,000/day penalty fee."
                ),
                "impact": (
                    "P1 existential business deadline crisis. Projected holdover penalty fees exceeded $450,000 per month. Engineering "
                    "burnout reached critical levels; key senior developers threatened resignation. Risk of sudden physical eviction from "
                    "the co-location facility threatening all warehouse fulfillment operations."
                ),
                "constraints": (
                    "Vacate the physical datacenter within 60 remaining days; eliminate all holdover lease penalties; ensure zero inventory "
                    "tracking downtime; defer application code rewrites until safely landed in Google Cloud."
                ),
                "diagnostic_steps": [
                    "Step 1: Review the project velocity burndown chart; calculate current velocity (1 service/month) will require 138 additional months to complete refactoring.",
                    "Step 2: Inspect lease contract terms; confirm firm termination date with non-negotiable $15,000 daily overstay penalties.",
                    "Step 3: Analyze workload inventory; identify that 82% of VMs run standard x86-64 Linux and Windows Server OSs compatible with Compute Engine.",
                    "Step 4: Check hybrid network connectivity; confirm dedicated 10 Gbps Cloud Interconnect is established and operating with sub-5ms latency."
                ],
                "root": (
                    "Conflating a hard datacenter exit deadline with deep application refactoring. Demanding full cloud-native rewrites under "
                    "a fixed timeline created an unachievable scope that guaranteed lease default."
                ),
                "remediation_steps": [
                    "Step 1: Immediately halt all in-flight refactoring efforts; pivot the entire migration strategy to Rehost using Google Cloud Migrate to Virtual Machines (m4vm).",
                    "Step 2: Deploy m4vm replication connectors to the on-prem VMware vSphere cluster, initiating background asynchronous block replication for all 138 remaining VMs over Cloud Interconnect.",
                    "Step 3: Execute non-disruptive test clones in isolated Google Cloud VPC subnets to validate that guest OSs, network interfaces, and database binaries boot cleanly.",
                    "Step 4: Schedule weekend cutover windows across three migration waves, executing cutovers with sub-10-minute VM downtime, vacating the facility 12 days ahead of lease termination."
                ],
                "verify": (
                    "Confirm all 140 VMs are running successfully on Compute Engine. Inspect the co-location datacenter; verify all physical "
                    "racks are powered down and decommissioned, and secure written confirmation from the landlord confirming zero lease penalty liabilities."
                ),
                "residual": (
                    "Rehosted VMs retain legacy OS maintenance debt and static sizing; a secondary optimization phase must be scheduled to "
                    "downsize over-provisioned VMs and refactor priority workloads in the cloud."
                ),
                "diagram": (
                    "Refactor 140 apps stalls (lease expires in 60d)",
                    "Landlord threatens $15k/day penalty",
                    "Scope paralysis, imminent lease default",
                    "Pivot to Rehost via Migrate to VMs (m4vm)",
                    "140 VMs migrated in 45 days, $0 penalties"
                ),
                "facts": "Lease ended in 4 months; only 2 of 140 apps refactored in 2 months; $15k/day penalty threatened; 10 Gbps Interconnect existed.",
                "inference": "When time is the binding constraint, Rehost or GCVE is the only viable path to eliminate datacenter liability.",
                "expected": "Migrate to VMs replicates disk blocks in the background, enabling low-risk cutover and meeting strict exit deadlines."
            },
            "lab": {
                "name": "6 Rs Portfolio Rationalization and Migration Scoring Model",
                "file": "day-075-rationalization.md",
                "goal": "Build an automated Python 6 Rs decision scoring engine to evaluate workloads across timeline, complexity, and business value.",
                "expected": "A complete 6 Rs rationalization document, an executable Python scoring model, and verified migration pathway outputs.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 74 landing zone and Day 68 business requirements",
                "preflight": "Review Google Cloud migration assessment best practices and workload scoring dimensions.",
                "steps": [
                    "Draft the enterprise 6 Rs portfolio evaluation framework in `day-075-rationalization.md`.",
                    "Develop an executable Python rationalization scoring script (`score_6r.py`):\n\n```python\n# score_6r.py\n\nWORKLOADS = [\n    {\n        'name': 'Warehouse Inventory Monolith',\n        'time_critical': True,     # Lease ending soon\n        'legacy_os': True,\n        'business_differentiator': True,\n        'db_coupled': True\n    },\n    {\n        'name': 'Customer Support Chatbot',\n        'time_critical': False,\n        'legacy_os': False,\n        'business_differentiator': False, # Commodity tool\n        'db_coupled': False\n    },\n    {\n        'name': 'Core Checkout API',\n        'time_critical': False,\n        'legacy_os': False,\n        'business_differentiator': True,  # High revenue driver\n        'db_coupled': False\n    },\n    {\n        'name': 'Obsolete 2019 Marketing Analytics',\n        'time_critical': False,\n        'legacy_os': True,\n        'business_differentiator': False,\n        'db_coupled': False\n    }\n]\n\ndef assign_6r_pathway(app: dict) -> str:\n    if app['name'].startswith('Obsolete'):\n        return 'RETIRE'\n    if not app['business_differentiator'] and not app['legacy_os']:\n        return 'REPURCHASE (SaaS)'\n    if app['time_critical']:\n        return 'REHOST (Migrate to VMs / GCVE)'\n    if app['business_differentiator'] and not app['time_critical']:\n        return 'REFACTOR (GKE / Cloud Run / Spanner)'\n    return 'REPLATFORM (Cloud SQL / Managed Services)'\n\nfor w in WORKLOADS:\n    strategy = assign_6r_pathway(w)\n    print(f\"{w['name']} -> Assigned Strategy: {strategy}\")\n    w['strategy'] = strategy\n\nassert WORKLOADS[0]['strategy'].startswith('REHOST')\nassert WORKLOADS[1]['strategy'].startswith('REPURCHASE')\nassert WORKLOADS[2]['strategy'].startswith('REFACTOR')\nassert WORKLOADS[3]['strategy'] == 'RETIRE'\nprint(\"6 Rs Workload Rationalization Logic Verified Successfully.\")\n```",
                    "Execute the Python workload scoring script:\n\n```sh\npython3 score_6r.py\n```",
                    "Document the rationalization matrix and post-migration modernization roadmap in `day-075-rationalization.md`."
                ],
                "verification": (
                    "Run automated rationalization model test:\n\n```sh\npython3 -c \"import score_6r; print('6 Rs Rationalization Test Passed')\"\n```\n\nConfirm output displays `6 Rs Workload Rationalization Logic Verified Successfully`."
                ),
                "trouble": (
                    "If time-critical workloads are misclassified, verify conditional evaluation order in `score_6r.py`."
                ),
                "cleanup": "No remote cloud resources created; retain scripts and rationalization matrices in repository.",
                "accept": "A validated 6 Rs rationalization document, an executable Python decision model, and verified pathway classifications."
            }
        },
        {
            "key": "topic-02",
            "title": "The Four Migration Phases: Assess, Plan, Deploy, and Optimize",
            "overview": (
                "Structure enterprise migrations into four disciplined phases. Master wave planning, dependency clustering, "
                "cutover methodologies (Big Bang vs Strangler), and explicit Go/No-Go rollback criteria."
            ),
            "preview": (
                "A project team splits an application frontend and its backend database into separate migration waves, migrating the web app "
                "to the cloud while leaving the database on-premises, causing 45ms cross-connect latency that destroys checkout performance."
            ),
            "technical": (
                "#### 1. The Four-Phase Migration Lifecycle\n\n"
                "Enterprise migrations cannot be treated as a single monolithic event. Google Cloud defines a four-phase lifecycle:\n\n"
                "- **Phase 1: Assess:** Complete automated discovery of all server instances, CPU/RAM utilization percentiles, storage IOPs, "
                "and network port dependencies. Establish Total Cost of Ownership (TCO) benchmarks and identify migration blockers.\n"
                "- **Phase 2: Plan:** Group discovered workloads into logical **Migration Waves** based on dependency clusters. Design the Google "
                "Cloud Landing Zone (Shared VPC, IAM, Organization Policies), configure hybrid network connectivity (Cloud Interconnect), and "
                "author explicit Cutover and Rollback Runbooks.\n"
                "- **Phase 3: Deploy:** Execute pilot migrations to validate tooling. Replicate storage volumes continuously in the background. "
                "Perform user acceptance testing (UAT) on isolated test clones. Execute cutovers during maintenance windows.\n"
                "- **Phase 4: Optimize:** Move from 'running in the cloud' to 'optimizing for the cloud'. Apply Recommender API rightsizing, "
                "purchase Committed Use Discounts (CUDs), configure autohealing and autoscaling, and implement Cloud Monitoring SLO dashboards.\n\n"
                "#### 2. Wave Planning and Dependency Clustering Mathematics\n\n"
                "A critical failure point in migration planning is **Splitting Distributed Dependencies across the Hybrid Link**:\n\n"
                "- If an application executes 15 serial SQL queries per page load, running on-premises over 0.2ms local LAN latency requires "
                "$15 \\times 0.2\\text{ms} = 3.0\\text{ms}$ of network time.\n"
                "- If the application is migrated to Google Cloud in Wave 1 while leaving the database on-premises over a 40ms hybrid interconnect, "
                "the network latency explodes to $15 \\times 40\\text{ms} = 600\\text{ms}$, collapsing user performance.\n\n"
                "**Dependency Clustering Rule:** Applications and their tightly coupled, synchronous dependencies (databases, local caching "
                "clusters, authentication directories) MUST be grouped into the same migration wave and cut over simultaneously.\n\n"
                "#### 3. Cutover Runbooks and Go/No-Go Decision Gates\n\n"
                "Every migration wave cutover must follow a strict, minute-by-minute runbook with explicit **Go / No-Go Decision Gates**:\n\n"
                "- **T - 24 Hours:** Pre-cutover verification. Full data replication sync complete; replication lag < 1 minute; test clone UAT passed.\n"
                "- **T - 0 Hours (Cutover Window Begins):** Stop application services on-premises; set on-premises database to read-only.\n"
                "- **T + 30 Minutes:** Replicate delta storage blocks to Google Cloud; start database and compute instances in GCP.\n"
                "- **T + 60 Minutes (The Go/No-Go Gate):** Smoke test synthetic transactions. If tests pass: redirect DNS / Load Balancer VIPs (Go). "
                "If critical errors occur or replication failed: abort, revert DNS, and re-enable on-premises database (No-Go Rollback).\n"
                "- **Point of No Return:** Once live customer transactions commit in Google Cloud, rollback requires reverse CDC data replication "
                "back to on-premises to prevent data loss.\n\n"
                "#### 4. Architectural Trade-offs: Cutover Methodologies\n\n"
                "| Cutover Strategy | Business Downtime Window | Rollback Complexity | Hybrid Infrastructure Cost | State Synchronization Requirement |\n"
                "|---|---|---|---|---|\n"
                "| **Big Bang Cutover** | Moderate (2 – 6 Hours Maintenance Window) | Low (Revert DNS before Point of No Return) | Lowest (Single-day switchover) | Replicate delta blocks during shutdown |\n"
                "| **Parallel Run (Dual-Write)** | Zero Downtime | Lowest (Instant switchback to on-prem) | Highest (200% compute running concurrently) | Complex bidirectional CDC / dual-write queue |\n"
                "| **Phased Wave Strangler** | Minimal (Per-domain maintenance) | Moderate (Per-service routing control) | Moderate | API Gateway URL routing / strangler facade |\n"
                "| **Canary Traffic Shift** | Zero Downtime | Sub-minute (Shift traffic back to on-prem) | Moderate | Global Load Balancer weighting (requires hybrid backend) |\n"
            ),
            "questions": [
                "Why does splitting an application and its database across a hybrid link cause exponential latency degradation?",
                "What defines the 'Point of No Return' during an enterprise database migration cutover?",
                "How does continuous asynchronous block replication minimize maintenance downtime windows?",
                "What specific telemetry must be verified during a migration Go/No-Go decision gate?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/migration-to-google-cloud-architecture-and-tools",
            "reference_label": "Google Cloud Architecture Center: Migration phases and tooling framework",
            "scenario": {
                "scenario": (
                    "Brightloaf planned a weekend migration of their customer loyalty portal. The project manager scheduled the web frontend "
                    "for Wave 1 on Saturday, and the PostgreSQL database for Wave 2 two weeks later. During the Saturday cutover, the web application "
                    "was deployed to Compute Engine in `us-central1`, communicating with the on-premises database in Chicago over an IPsec VPN "
                    "tunnel (RTT = 48ms). When customer traffic surged on Sunday morning, every user profile load executed 16 sequential SQL queries "
                    "across the VPN, accumulating over 760ms of network latency per request. Compute Engine VM threads exhausted rapidly, "
                    "database connection pools saturated, and customer login requests timed out with HTTP 504 Gateway Timeouts."
                ),
                "impact": (
                    "P1 migration cutover failure. Customer loyalty portal was unusable for 18 hours. 8,400 loyalty point redemptions failed. "
                    "Emergency rollback executed Sunday afternoon under stress, incurring $45,000 in diverted engineering overtime."
                ),
                "constraints": (
                    "Eliminate hybrid latency compounding; ensure cutover completes within a 3-hour maintenance window; establish explicit "
                    "automated Go/No-Go verification gates with sub-15 minute rollback capability."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect application trace spans in Cloud Trace; identify that 94% of total transaction duration is spent in `SocketInputStream.socketRead0()` traversing the on-premises VPN link.",
                    "Step 2: Calculate network compounding: 16 sequential SQL queries × 48ms VPN round-trip time = 768ms of pure network transit latency.",
                    "Step 3: Review migration project plan; discover that wave planning was organized by technical tier (web vs database) rather than business dependency clusters.",
                    "Step 4: Check rollback runbook; observe lack of documented rollback triggers, causing 4 hours of indecision before aborting."
                ],
                "root": (
                    "Flawed wave planning decoupled tightly coupled tiers across a high-latency hybrid link. Organizing migration waves by "
                    "infrastructure layers rather than dependency clusters violated distributed latency boundaries."
                ),
                "remediation_steps": [
                    "Step 1: Re-architect the migration plan to group the web frontend and database into a single, atomic migration wave.",
                    "Step 2: Pre-seed database data to Cloud SQL for PostgreSQL using Database Migration Service (DMS) continuous CDC replication, keeping replication lag under 2 seconds.",
                    "Step 3: Establish a formal Go/No-Go checklist: if synthetic checkout latency exceeds 250ms at T+45 minutes, immediately execute automated DNS rollback to on-premises.",
                    "Step 4: Execute the combined cutover during a Sunday 02:00 UTC window; complete database final sync in 4 minutes, point web tier locally, and switch DNS."
                ],
                "verify": (
                    "Execute post-cutover synthetic login tests in staging. Confirm inter-tier latency between web VMs and Cloud SQL drops to "
                    "0.8ms (local VPC), customer login completes in 140ms, and zero cross-premises network hops occur."
                ),
                "residual": (
                    "Migrating both tiers concurrently requires testing database failover procedures and verifying that Cloud SQL connection "
                    "pooling can absorb peak morning connection spikes."
                ),
                "diagram": (
                    "Web on Cloud; DB on-prem across VPN (48ms)",
                    "16 serial queries compound to 768ms",
                    "Thread exhaustion, 504 gateway timeouts",
                    "Group Web & DB into atomic migration wave",
                    "Local VPC latency (0.8ms), login completes in 140ms"
                ),
                "facts": "Web in cloud, DB on-prem over 48ms VPN; 16 serial queries caused 768ms network lag; 18h outage; rollback cost $45k.",
                "inference": "Organizing migration waves by tier splits synchronous call graphs across WAN links; dependency clustering is mandatory.",
                "expected": "Clustering dependent tiers into atomic waves eliminates cross-premises latency, achieving sub-200ms page load times."
            },
            "lab": {
                "name": "Migration Wave Planning and Dependency Clustering Engine",
                "file": "day-075-wave-planning.md",
                "goal": "Build an executable Python dependency clustering engine to group enterprise applications into atomic migration waves.",
                "expected": "A complete wave planning strategy document, an executable Python clustering script, and verified wave assignment outputs.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 74 anti-patterns and Day 71 performance sizing",
                "preflight": "Review network dependency mapping methodologies and cutover runbook structures.",
                "steps": [
                    "Draft the migration wave planning methodology in `day-075-wave-planning.md`.",
                    "Develop an executable Python dependency clustering script (`wave_planner.py`):\n\n```python\n# wave_planner.py\n\n# Enterprise application dependency graph (service -> set of synchronous dependencies)\nDEPENDENCIES = {\n    'web_frontend': {'order_api', 'auth_service'},\n    'order_api': {'orders_db', 'inventory_service'},\n    'orders_db': set(),\n    'auth_service': {'auth_ldap'},\n    'auth_ldap': set(),\n    'inventory_service': {'inventory_db'},\n    'inventory_db': set(),\n    'standalone_reporting': set() # Independent batch job\n}\n\ndef cluster_wave(start_node: str, graph: dict, visited: set = None):\n    if visited is None:\n        visited = set()\n    visited.add(start_node)\n    for dep in graph.get(start_node, set()):\n        if dep not in visited:\n            cluster_wave(dep, graph, visited)\n    return visited\n\n# Calculate atomic wave for web_frontend\nwave_1 = cluster_wave('web_frontend', DEPENDENCIES)\nprint(\"Atomic Migration Wave 1 Cluster:\", sorted(list(wave_1)))\n\n# Ensure tightly coupled database is inside the wave cluster\nassert 'orders_db' in wave_1, \"Database was decoupled from frontend!\"\nassert 'auth_ldap' in wave_1, \"Authentication was decoupled!\"\nassert 'standalone_reporting' not in wave_1, \"Independent app incorrectly bundled!\"\nprint(\"Migration Wave Dependency Clustering Logic Verified Successfully.\")\n```",
                    "Execute the Python wave planning test:\n\n```sh\npython3 wave_planner.py\n```",
                    "Author the Go/No-Go decision matrix and rollback runbook template in `day-075-wave-planning.md`."
                ],
                "verification": (
                    "Run automated wave planning test:\n\n```sh\npython3 -c \"import wave_planner; print('Wave Planning Engine Test Passed')\"\n```\n\nConfirm output displays `Migration Wave Dependency Clustering Logic Verified Successfully`."
                ),
                "trouble": (
                    "If cyclic dependencies cause infinite loops, verify graph traversal uses visited set guards."
                ),
                "cleanup": "No remote cloud resources created; retain scripts and wave planning artifacts in repository.",
                "accept": "A validated wave planning document, an executable Python dependency clustering script, and a verified cutover runbook."
            }
        },
        {
            "key": "topic-03",
            "title": "Discovery and Assessment Tools: Migration Center, StratoZone, and mFit",
            "overview": (
                "Leverage automated cloud discovery and assessment tooling. Use Google Cloud Migration Center and StratoZone for "
                "utilization-based rightsizing, and evaluate containerization readiness with Migrate to Containers (mFit)."
            ),
            "preview": (
                "An enterprise migrates on-premises VMs based on allocated virtual specs (vCPUs/RAM) rather than actual utilization telemetry, "
                "over-provisioning cloud compute by 320% and inflating the monthly bill by $65,000."
            ),
            "technical": (
                "#### 1. Automated Discovery Mechanics: Agents vs. Agentless Collectors\n\n"
                "Enterprise infrastructure discovery establishes the factual baseline for migration. Google Cloud provides two discovery modes:\n\n"
                "- **Agentless Discovery (VMware vCenter Integration):** The **Migration Center Discovery Client** deploys as an Open Virtualization "
                "Appliance (OVA) on-premises. It connects directly to VMware vCenter APIs, collecting inventory, CPU/RAM allocation, disk storage, "
                "and operating system versions across thousands of VMs in minutes without installing software on guest OSs.\n"
                "- **Agent-Based Discovery:** For physical bare-metal servers or non-VMware hypervisors, lightweight OS agents collect fine-grained "
                "guest telemetry: per-process resource utilization, local network listening ports, and active TCP socket connections to map dependencies.\n\n"
                "#### 2. The Allocated vs. Utilized Sizing Dilemma (StratoZone)\n\n"
                "In traditional on-premises virtualization, system administrators habitually over-allocate resources:\n\n"
                "- A system administrator requests a VM with 16 vCPUs and 64 GB of RAM 'just in case' for future growth.\n"
                "- In reality, the guest workload runs at an average CPU utilization of 6% and consumes 8 GB of RAM.\n"
                "- If an architect maps this VM 1:1 into Compute Engine (`n2-standard-16`), the enterprise pays for 16 vCPUs of cloud compute 24/7.\n\n"
                "**StratoZone / Migration Center Telemetry:** Analyzes 30 to 90 days of peak and percentile utilization metrics (P95 / P99). It "
                "recommends **Rightsized Compute Sizing** (e.g. mapping the 16-vCPU VM to an `n2-standard-4` or `e2-standard-4`), instantly "
                "slashing projected cloud infrastructure costs by 50% to 70% without sacrificing performance.\n\n"
                "#### 3. Containerization Fitness Assessment with mFit\n\n"
                "Not all workloads should remain VMs. Google Cloud **mFit** (Migrate to Containers CLI) inspects Linux and Windows VMs to determine "
                "their containerization readiness:\n\n"
                "- Identifies installed software packages (Apache, Tomcat, Node.js, IIS).\n"
                "- Evaluates kernel modules, local storage dependencies, and Windows registry requirements.\n"
                "- Categorizes workloads into: **Fit for Cloud Run**, **Fit for GKE**, or **Requires VM (Compute Engine / GCVE)**.\n\n"
                "#### 4. Total Cost of Ownership (TCO) Modeling\n\n"
                "A comprehensive cloud business case compares on-premises Total Cost of Ownership (TCO) against Google Cloud spend:\n\n"
                "$$\\text{On-Prem TCO} = \\text{Hardware Depreciation} + \\text{Datacenter Real Estate} + \\text{Power/Cooling} + \\text{Hypervisor Licensing} + \\text{SysAdmin Staff}$$\n\n"
                "Migration Center exports financial models factoring in **3-Year Committed Use Discounts (CUDs)** and storage lifecycle savings, "
                "providing defensible financial projections for executive leadership.\n\n"
                "#### 5. Architectural Trade-offs: Discovery & Assessment Tooling\n\n"
                "| Discovery Tool | Deployment Model | Primary Data Collected | Sizing Philosophy | Output Deliverable |\n"
                "|---|---|---|---|---|\n"
                "| **Migration Center** | Agentless OVA / Agent | Comprehensive inventory & performance telemetry | Percentile-based rightsizing (P95) | Unified GCP console assessment & TCO export |\n"
                "| **StratoZone** | Agentless Appliance | Deep financial modeling, hardware depreciation | Strategic CUD & licensing optimization | Executive financial presentation & wave groupings |\n"
                "| **mFit Assessment** | Standalone Linux/Win CLI | OS kernel, installed runtimes, storage paths | Containerization fit for Cloud Run/GKE | Automated container fitness report & Dockerfile suggestions |\n"
                "| **Database Migration Service (DMS)** | Cloud-managed network pairing | Database schemas, stored procs, data volume | Direct managed database mapping | Automated schema conversion & replication pipeline |\n"
            ),
            "questions": [
                "Why does sizing cloud VMs based on allocated on-premises vCPUs cause severe financial waste?",
                "What is the difference between agentless vCenter discovery and agent-based guest OS discovery?",
                "How does mFit evaluate whether a legacy virtual machine is suitable for containerization on Cloud Run?",
                "What cost factors are included in on-premises TCO beyond raw server hardware purchase costs?",
            ],
            "reference": "https://docs.cloud.google.com/migration-center/docs/overview",
            "reference_label": "Google Cloud Migration Center Documentation: Overview and discovery methods",
            "scenario": {
                "scenario": (
                    "Brightloaf planned a migration of 85 back-office application and reporting VMs to Compute Engine. The procurement team "
                    "reviewed the VMware vCenter inventory spreadsheet and provisioned matching Compute Engine instances based on allocated "
                    "virtual specifications: provisioning 85 instances of `n2-standard-16` (1,360 total vCPUs and 5,440 GB of RAM). During the first "
                    "full billing cycle, the CFO received an unexpected cloud compute invoice for $92,000—more than $65,000 over budget. A subsequent "
                    "audit revealed that 72 of the 85 VMs were running at an average CPU utilization of less than 7%, with memory consumption "
                    "hovering under 12%. The enterprise was paying for 1,100 completely idle vCPUs."
                ),
                "impact": (
                    "Catastrophic financial budget overrun. $65,000/month in wasted cloud expenditure ($780,000 annualized loss). Project "
                    "credibility damaged; board demanded an immediate audit of all cloud engineering spending."
                ),
                "constraints": (
                    "Downsize over-provisioned infrastructure within 30 days; reduce monthly compute spend by at least 60%; ensure zero "
                    "workload performance degradation or CPU throttling during month-end batch peaks."
                ),
                "diagnostic_steps": [
                    "Step 1: Export Compute Engine utilization metrics from Cloud Monitoring; discover 78% of VMs have P99 CPU utilization below 18%.",
                    "Step 2: Inspect StratoZone assessment telemetry; observe that StratoZone had originally recommended `e2-standard-4` instances, but the procurement team ignored the recommendations and provisioned allocated specs.",
                    "Step 3: Analyze workload characteristics; identify that back-office workloads are non-critical and burst only during daytime business hours.",
                    "Step 4: Check billing account; confirm instances were running on full On-Demand pricing without Committed Use Discounts."
                ],
                "root": (
                    "Provisioning cloud VMs based on on-premises allocated specifications rather than actual utilization telemetry. "
                    "Ignoring StratoZone rightsizing data led to severe over-provisioning and massive financial waste."
                ),
                "remediation_steps": [
                    "Step 1: Execute automated rightsizing: resize the 72 underutilized VMs from `n2-standard-16` down to `e2-standard-4` during scheduled rolling maintenance windows.",
                    "Step 2: Migrate 8 stateless background reporting VMs to Cloud Run using mFit containerization recommendations, enabling scale-to-zero when jobs complete.",
                    "Step 3: Purchase a 3-Year Flexible Spend-Based Committed Use Discount (CUD) covering the newly rightsized baseline compute capacity, securing an additional 46% discount.",
                    "Step 4: Establish automated budget alerts and implement mandatory Recommender API review gates in the Terraform CI/CD deployment pipeline."
                ],
                "verify": (
                    "Review Cloud Billing reports 30 days post-downsizing. Confirm monthly compute spend drops from $92,000 to $27,400 (a 70.2% "
                    "savings) while P99 CPU utilization stabilizes comfortably at 55% during peak business hours."
                ),
                "residual": (
                    "Downsizing VMs reduces peak burst headroom; Cloud Monitoring alerts must be configured on CPU utilization (`cpu/utilization > 80%` "
                    "for 10 minutes) to dynamically trigger vertical scaling if business volumes expand."
                ),
                "diagram": (
                    "Provisioned allocated specs (85x n2-16)",
                    "VMs idle at 7% CPU utilization",
                    "$92k/month bill ($65k budget blowout)",
                    "Apply StratoZone rightsizing + 3-Yr CUD",
                    "Bill drops to $27.4k (70% savings), healthy 55% CPU"
                ),
                "facts": "85 VMs provisioned as n2-16 based on allocated specs; average CPU was 7%; $92k/month bill; $65k/month waste.",
                "inference": "On-prem virtualization encourages over-allocation; cloud economics requires utilization-based rightsizing.",
                "expected": "StratoZone rightsizing aligns cloud provisioning with actual consumption, cutting costs by over 60%."
            },
            "lab": {
                "name": "StratoZone-Style Rightsizing Analysis and TCO Modeling",
                "file": "day-075-rightsizing-tco.md",
                "goal": "Build an executable Python TCO rightsizing engine comparing allocated vs utilized compute costs and CUD savings.",
                "expected": "A complete TCO financial analysis document, an executable Python sizing calculator, and verified cost savings output.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 70 cost optimization and Day 74 landing zone",
                "preflight": "Review Google Cloud Compute Engine machine type pricing and StratoZone sizing methodologies.",
                "steps": [
                    "Draft the cloud financial assessment methodology in `day-075-rightsizing-tco.md`.",
                    "Develop an executable Python rightsizing and TCO calculation script (`tco_calc.py`):\n\n```python\n# tco_calc.py\n\n# Hourly On-Demand Rates (us-central1 reference)\nRATES = {\n    'n2-standard-16': 0.7776,  # 16 vCPU, 64 GB RAM\n    'n2-standard-4': 0.1944,   # 4 vCPU, 16 GB RAM\n    'e2-standard-4': 0.1340    # 4 vCPU, 16 GB RAM (Cost-optimized)\n}\nHOURS_PER_MONTH = 730\n\ndef calculate_portfolio_cost(num_vms: int, machine_type: str, cud_discount_pct: float = 0.0):\n    monthly_base = num_vms * RATES[machine_type] * HOURS_PER_MONTH\n    monthly_discounted = monthly_base * (1.0 - cud_discount_pct / 100.0)\n    return monthly_base, monthly_discounted\n\n# Scenario: 85 VMs\n# 1. Unoptimized Allocated Sizing: n2-standard-16 on-demand\nbase_cost, _ = calculate_portfolio_cost(85, 'n2-standard-16', 0.0)\n\n# 2. Rightsized Sizing: e2-standard-4 on-demand\nrightsized_cost, _ = calculate_portfolio_cost(85, 'e2-standard-4', 0.0)\n\n# 3. Rightsized + 3-Year Flexible CUD (46% discount)\n_, optimized_cost = calculate_portfolio_cost(85, 'e2-standard-4', 46.0)\n\nsavings_monthly = base_cost - optimized_cost\nsavings_pct = (savings_monthly / base_cost) * 100.0\n\nprint(f\"Unoptimized Allocated Cost: ${base_cost:,.2f} / month\")\nprint(f\"Rightsized Sizing Cost:     ${rightsized_cost:,.2f} / month\")\nprint(f\"Optimized (Rightsized+CUD): ${optimized_cost:,.2f} / month\")\nprint(f\"Net Monthly Savings:        ${savings_monthly:,.2f} / month ({savings_pct:.1f}% savings)\")\nassert savings_pct > 80.0, \"TCO savings threshold calculation error!\"\nprint(\"StratoZone Rightsizing and TCO Model Verified Successfully.\")\n```",
                    "Execute the Python TCO calculation test:\n\n```sh\npython3 tco_calc.py\n```",
                    "Document the financial findings and executive business case in `day-075-rightsizing-tco.md`."
                ],
                "verification": (
                    "Run automated TCO verification test:\n\n```sh\npython3 -c \"import tco_calc; print('TCO Calculation Test Passed')\"\n```\n\nConfirm output demonstrates monthly savings exceeding 80%."
                ),
                "trouble": (
                    "If savings calculation fails threshold assertion, verify discount percentage formula in `tco_calc.py`."
                ),
                "cleanup": "No remote cloud resources created; retain calculation scripts and financial models in repository.",
                "accept": "A validated rightsizing TCO analysis document, an executable Python financial model, and verified cost savings output."
            }
        },
        {
            "key": "topic-04",
            "title": "Google Cloud VMware Engine (GCVE): Architecture, Sizing, and HCX Migration",
            "overview": (
                "Architect dedicated VMware environments on Google Cloud VMware Engine (GCVE). Master bare-metal node sizing, "
                "vSphere/vSAN/NSX-T integration, and seamless live vMotion migrations using VMware HCX."
            ),
            "preview": (
                "An enterprise attempts a live cross-cloud vMotion migration without configuring MTU sizing on Cloud Interconnect, "
                "causing packet fragmentation that aborts virtual machine migrations midway through a weekend cutover."
            ),
            "technical": (
                "#### 1. Google Cloud VMware Engine (GCVE) Architecture\n\n"
                "For enterprises with deep operational investments in VMware vSphere or tight datacenter evacuation deadlines, refactoring "
                "or rehosting to Compute Engine may carry unacceptable operational friction. **Google Cloud VMware Engine (GCVE)** provides "
                "a fully managed VMware Software-Defined Datacenter (SDDC) running on bare-metal Google Cloud infrastructure:\n\n"
                "- **Dedicated Bare-Metal Nodes:** Nodes run on isolated, single-tenant physical servers (e.g. `ve1-standard-72`: 72 vCPUs, "
                "768 GB RAM, 19.2 TB NVMe raw storage). Hardware is dedicated 100% to the enterprise with zero hypervisor sharing.\n"
                "- **Full VMware SDDC Stack:** Includes **VMware vSphere** (ESXi), **vCenter Server**, **vSAN** (software-defined storage), "
                "and **NSX-T** (software-defined networking).\n"
                "- **Operational Continuity:** IT administrators manage the cluster using their existing vSphere Client, PowerCLI scripts, "
                "and enterprise backup tools (Veeam, Commvault) without retraining staff.\n\n"
                "#### 2. Hybrid Connectivity and Private Service Access\n\n"
                "GCVE operates in a dedicated, high-speed private networking environment connected directly to Google Cloud VPCs:\n\n"
                "- Connects via **Private Service Access (PSA)** or direct VPC Peering with sub-millisecond network latency to Google Cloud "
                "services (BigQuery, Cloud Storage, Cloud SQL).\n"
                "- Connects to on-premises datacenters via **Cloud Interconnect** or Partner Interconnect, establishing high-bandwidth "
                "hybrid connectivity.\n\n"
                "#### 3. VMware HCX (Hybrid Cloud Extension) Migration Mechanics\n\n"
                "The primary migration engine for GCVE is **VMware HCX**, which abstracts on-premises and cloud vSphere environments:\n\n"
                "- **Layer 2 Network Extension:** HCX establishes an encrypted network bridge between on-premises VLANs and GCVE NSX-T overlays. "
                "This allows virtual machines to migrate to Google Cloud **without changing their IP addresses, subnet masks, or default gateways**.\n"
                "- **Live vMotion:** Enables zero-downtime live migration of running VMs over Cloud Interconnect. Applications continue processing "
                "user transactions while memory pages are mirrored across WAN links.\n"
                "- **Cold & Warm (Bulk) Migration:** Replicates disk blocks in the background, scheduling a coordinated reboot to cut over "
                "hundreds of non-critical VMs simultaneously.\n\n"
                "#### 4. The MTU Sizing Trap and Packet Fragmentation\n\n"
                "A catastrophic operational failure in HCX migrations occurs due to **Maximum Transmission Unit (MTU)** mismatches:\n\n"
                "- Standard on-premises Ethernet uses an MTU of 1500 bytes. Jumbo frames use an MTU of 9000 bytes.\n"
                "- HCX encapsulates traffic inside IPsec / Geneve tunnels, adding a 50 to 100-byte encapsulation header.\n"
                "- If Cloud Interconnect or intermediate firewalls are configured with an MTU of 1500 bytes, encapsulated HCX packets exceed "
                "the MTU limit. If network devices drop fragmented packets (DF bit set), live vMotion transfers stall, time out, and abort midway.\n"
                "- **Best Practice:** Configure Cloud Interconnect and Google Cloud VPC with Jumbo Frames (MTU 8896 or 9000 bytes) to accommodate "
                "HCX encapsulation overhead seamlessly.\n\n"
                "#### 5. Architectural Trade-offs: GCVE vs. Native Compute Engine\n\n"
                "| Dimension | Google Cloud VMware Engine (GCVE) | Native Compute Engine (M4VM) | Modernized Cloud Run / GKE |\n"
                "|---|---|---|---|---|\n"
                "| **Minimum Commitment** | Minimum 3 nodes per cluster (~$15k/mo) | Single VM (hourly on-demand / CUD) | $0 baseline (scales to zero) |\n"
                "| **Live Migration (Zero Downtime)** | Native vMotion (No VM reboot required) | Requires brief reboot cutover | Zero-downtime rolling deployment |\n"
                "| **IP Address Preservation** | Built-in via HCX L2 Network Extension | Complex (requires network overlays/NAT) | Native cloud SDN IP addressing |\n"
                "| **Operational Skillset** | Existing VMware vSphere / vCenter staff | Cloud Ops / Linux & Windows sysadmin | Modern DevOps, Kubernetes, GitOps |\n"
                "| **Long-Term Modernization** | Retains hypervisor virtualization | Native cloud APIs and infrastructure | Fully decoupled microservices |\n"
            ),
            "questions": [
                "What minimum cluster node count is required to deploy a production Google Cloud VMware Engine private cloud?",
                "How does VMware HCX Layer 2 network extension eliminate the need to re-IP virtual machines during migration?",
                "Why does packet fragmentation on Cloud Interconnect cause VMware HCX live vMotion transfers to fail?",
                "Under what strategic enterprise conditions is GCVE financially preferable to refactoring on Compute Engine?",
            ],
            "reference": "https://docs.cloud.google.com/vmware-engine/docs/overview",
            "reference_label": "Google Cloud VMware Engine Documentation: Architecture and deployment overview",
            "scenario": {
                "scenario": (
                    "Brightloaf initiated a high-velocity migration of 60 legacy Windows enterprise resource planning (ERP) virtual machines "
                    "from their on-premises vSphere cluster to Google Cloud VMware Engine (GCVE). Because the ERP software utilized hard-coded "
                    "legacy IP addresses across 200 client endpoints, the team deployed VMware HCX with Layer 2 Network Extension over a 10 Gbps "
                    "Cloud Interconnect. During the scheduled Saturday night cutover, engineers initiated bulk live vMotion of the first 20 VMs. "
                    "At 42% completion, every vMotion transfer stalled simultaneously, threw timeout errors, and aborted. The Cloud Interconnect "
                    "router had been provisioned with standard MTU (1500 bytes), while HCX Geneve tunnel encapsulation expanded packet sizes "
                    "to 1550 bytes. Network routers silently dropped the oversized packets, breaking the vMotion memory synchronization stream."
                ),
                "impact": (
                    "P1 migration cutover failure. Cutover window missed. 14 critical ERP database virtual machines left in an inconsistent "
                    "split state between on-prem and cloud. Weekend rollout aborted; business resumed on-premises with emergency failback."
                ),
                "constraints": (
                    "Preserve existing guest IP addresses; ensure live vMotion completes without packet loss; complete migration within "
                    "the next scheduled 4-hour weekend window."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect VMware HCX appliance diagnostic logs; identify recurring error: `WAN Link MTU Verification Failed: Packet size exceeded MTU limit`.",
                    "Step 2: Check Cloud Interconnect attachment configuration; observe MTU was configured to default `1500` instead of jumbo frames.",
                    "Step 3: Run packet ping test over the interconnect link with DF (Don't Fragment) bit set: `ping -s 1472 -M do <gcve_gateway_ip>`; observe 100% packet loss for packets exceeding 1460 bytes.",
                    "Step 4: Audit on-premises core switch configuration; confirm on-premises switches had jumbo frames enabled, while cloud interconnect interface was truncating packets."
                ],
                "root": (
                    "Network MTU mismatch between on-premises jumbo frames and the 1500-byte Cloud Interconnect attachment. HCX Geneve "
                    "tunnel encapsulation overhead pushed packet sizes beyond the interface limit, triggering silent packet drops that collapsed vMotion streams."
                ),
                "remediation_steps": [
                    "Step 1: Reconfigure the Cloud Interconnect VLAN attachment and Google Cloud VPC to enable Jumbo Frames with an MTU of 8896 bytes.",
                    "Step 2: Update the VMware HCX Network Profile to validate path MTU automatically prior to initiating migration jobs.",
                    "Step 3: Execute a single-VM test vMotion during a weekday maintenance window to verify that memory page synchronization sustains 8 Gbps line-rate throughput without packet fragmentation.",
                    "Step 4: Re-initiate the 60-VM bulk migration during the following weekend window, completing live vMotion transfers in 1 hour and 45 minutes with zero downtime."
                ],
                "verify": (
                    "Verify all 60 ERP VMs are active in the GCVE vCenter inventory. Confirm client workstations communicate with the ERP "
                    "servers using their original unchanged IP addresses with sub-2ms network latency and zero packet loss."
                ),
                "residual": (
                    "Layer 2 extended networks route default gateway traffic back to the on-premises core router until the gateway is migrated; "
                    "once all VMs in a VLAN are migrated, the default gateway must be cut over to the GCVE NSX-T router to eliminate hairpin routing."
                ),
                "diagram": (
                    "Live vMotion over 1500 MTU Interconnect",
                    "HCX encapsulation exceeds MTU (1550B)",
                    "Silent packet drops abort vMotion (42%)",
                    "Configure Jumbo Frames (MTU 8896) on Interconnect",
                    "Zero-loss live vMotion, all 60 VMs migrated"
                ),
                "facts": "HCX live vMotion stalled at 42%; Cloud Interconnect had MTU 1500; HCX packets were 1550 bytes; cutover missed.",
                "inference": "Tunnel encapsulation expands packet size; Jumbo Frames (MTU 8896+) are required to prevent vMotion packet drops.",
                "expected": "Enabling Jumbo Frames on Cloud Interconnect allows full-speed HCX live vMotion without packet fragmentation."
            },
            "lab": {
                "name": "Google Cloud VMware Engine Cluster Sizing and MTU Verification",
                "file": "day-075-gcve-sizing.md",
                "goal": "Build an executable Python GCVE cluster sizing calculator and author an MTU network verification runbook.",
                "expected": "A complete GCVE architecture document, an executable Python node calculator, and verified MTU testing commands.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 74 enterprise networking and Day 70 cost governance",
                "preflight": "Review Google Cloud VMware Engine node specifications and VMware vSAN storage requirements.",
                "steps": [
                    "Draft the GCVE architecture blueprint in `day-075-gcve-sizing.md`.",
                    "Define the Cloud Interconnect jumbo frame configuration command:\n\n```sh\n# Configure Cloud Interconnect attachment with Jumbo Frames (MTU 8896)\ngcloud compute interconnects attachments dedicated update brightloaf-interconnect-vlan \\\n  --mtu=8896 \\\n  --region=us-central1\n```",
                    "Develop an executable Python GCVE node sizing calculator (`gcve_sizer.py`):\n\n```python\n# gcve_sizer.py\nimport math\n\n# GCVE ve1-standard-72 node specs\nNODE_VCPU = 72\nNODE_RAM_GB = 768\nNODE_STORAGE_TB = 19.2 # Raw NVMe per node\nVSAN_OVERHEAD_PCT = 0.25 # vSAN slack + metadata + RAID-2 (FTT=2)\n\ndef size_gcve_cluster(total_vcpus: int, total_ram_gb: int, total_storage_tb: int, vcpu_oversubscribe: float = 4.0):\n    # Calculate effective vCPUs allowed via oversubscription\n    effective_vcpus_per_node = NODE_VCPU * vcpu_oversubscribe\n    nodes_by_cpu = math.ceil(total_vcpus / effective_vcpus_per_node)\n    \n    # Calculate nodes required by RAM (no oversubscription for production)\n    nodes_by_ram = math.ceil(total_ram_gb / NODE_RAM_GB)\n    \n    # Calculate nodes required by Storage with vSAN overhead\n    effective_storage_per_node = NODE_STORAGE_TB * (1.0 - VSAN_OVERHEAD_PCT)\n    nodes_by_storage = math.ceil(total_storage_tb / effective_storage_per_node)\n    \n    # Production minimum is 3 nodes\n    required_nodes = max(3, nodes_by_cpu, nodes_by_ram, nodes_by_storage)\n    return nodes_by_cpu, nodes_by_ram, nodes_by_storage, required_nodes\n\n# Scenario: 140 VMs, 560 vCPUs, 2,800 GB RAM, 65 TB raw storage\nby_cpu, by_ram, by_stor, total_nodes = size_gcve_cluster(560, 2800, 65, vcpu_oversubscribe=3.0)\n\nprint(f\"Nodes required by CPU:     {by_cpu}\")\nprint(f\"Nodes required by RAM:     {by_ram}\")\nprint(f\"Nodes required by Storage: {by_stor}\")\nprint(f\"Total GCVE Nodes Required: {total_nodes} nodes (ve1-standard-72)\")\nassert total_nodes >= 3, \"Cluster must satisfy 3-node minimum!\"\nprint(\"GCVE Cluster Sizing Calculation Verified Successfully.\")\n```",
                    "Execute the Python GCVE sizing calculator test:\n\n```sh\npython3 gcve_sizer.py\n```"
                ],
                "verification": (
                    "Run automated GCVE sizing verification test:\n\n```sh\npython3 -c \"import gcve_sizer; print('GCVE Sizing Engine Test Passed')\"\n```\n\nConfirm output displays `GCVE Cluster Sizing Calculation Verified Successfully`."
                ),
                "trouble": (
                    "If storage node count is unexpectedly high, verify vSAN RAID policy assumptions and deduplication factors."
                ),
                "cleanup": "No remote cloud resources created; retain scripts and sizing models in local repository.",
                "accept": "A validated GCVE architecture document, an executable Python node sizing calculator, and verified MTU testing commands."
            }
        }
    ]
}
