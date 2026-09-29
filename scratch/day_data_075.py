"""day_data_075.py — Exhaustive architecture data specification for Day 75.

Covers Migration Assessment and VMware Fit:
- The 6 Rs Decision Taxonomy (Rehost, Replatform, Refactor, Repurchase, Retain, Retire)
- Migration Lifecycle Phases (Assess, Plan, Deploy, Optimize)
- Discovery & Assessment Tools (Migration Center, StratoZone-style rightsizing)
- Google Cloud VMware Engine (GCVE, vSAN storage physics, HCX L2 network extensions, TCO)

Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and 8-stage operational lab exercises.
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
        "type": "topology",
        "title": "Day 75: Enterprise Migration Lifecycle and Hybrid GCVE Topology",
        "desc": "End-to-end migration pipeline showing discovery, wave clustering, Dedicated Interconnect, HCX L2 extension, and target compute.",
        "caption": "Figure 75.1: Enterprise migration architecture illustrating on-premises discovery, HCX network extension, GCVE bare metal, and Google Cloud target compute.",
        "width": 1100,
        "height": 640,
        "layers": [
            {"name": "LAYER 1: Source Enterprise Datacenter (On-Premises)", "desc": "VMware vSphere Clusters, SAN/NAS Storage, On-Prem Core Routing", "fill": "#1e3a5f", "y": 10, "h": 90},
            {"name": "LAYER 2: Dedicated Hybrid Connectivity & Migration Fabric", "desc": "10Gbps Dedicated Cloud Interconnect + VMware HCX Layer 2 Network Extension", "fill": "#0f2338", "y": 115, "h": 90},
            {"name": "LAYER 3: Discovery, Assessment & Sizing Control Plane", "desc": "Google Cloud Migration Center, StratoZone Discovery Agents, mFit Sizing", "fill": "#064e3b", "y": 220, "h": 90},
            {"name": "LAYER 4: Target Infrastructure: GCVE & Compute Engine", "desc": "Google Cloud VMware Engine (ve1-standard-72) & Compute Engine Workload Fleet", "fill": "#1e1b4b", "y": 325, "h": 90},
            {"name": "LAYER 5: Modernized Cloud Services & Optimization Fabric", "desc": "Cloud SQL Managed Databases, GKE Enterprise, BigQuery Analytics, FinOps CUDs", "fill": "#3b0764", "y": 430, "h": 90},
        ],
        "components": [
            {"id": "onprem_vc", "name": "On-Prem vCenter", "detail": "350 Virtual Machines (vSphere 7)", "x": 80, "y": 30, "w": 260, "h": 52, "fill": "#0f283d", "stroke": "#38bdf8"},
            {"id": "onprem_san", "name": "Enterprise SAN / NAS", "detail": "Raw Storage (Over-allocated 4x)", "x": 420, "y": 30, "w": 260, "h": 52, "fill": "#0f283d", "stroke": "#38bdf8"},
            {"id": "interconnect", "name": "Dedicated Interconnect", "detail": "10 Gbps Cloud Interconnect Pair", "x": 80, "y": 135, "w": 260, "h": 52, "fill": "#092e28", "stroke": "#10b981"},
            {"id": "hcx_mesh", "name": "VMware HCX L2 Mesh", "detail": "Warm & Live vMotion Transport", "x": 420, "y": 135, "w": 260, "h": 52, "fill": "#092e28", "stroke": "#10b981"},
            {"id": "mig_center", "name": "Migration Center", "detail": "StratoZone Telemetry & Rightsizing", "x": 760, "y": 240, "w": 260, "h": 52, "fill": "#093322", "stroke": "#22c55e"},
            {"id": "gcve_sddc", "name": "GCVE Private Cloud", "detail": "Bare-Metal ESXi + vSAN Datastore", "x": 80, "y": 345, "w": 260, "h": 52, "fill": "#1b143a", "stroke": "#a855f7"},
            {"id": "gce_vms", "name": "Compute Engine Fleet", "detail": "Rightsized VMs (p95 CPU/RAM)", "x": 420, "y": 345, "w": 260, "h": 52, "fill": "#1b143a", "stroke": "#a855f7"},
            {"id": "csql_target", "name": "Cloud SQL Database", "detail": "Replatformed Relational Data", "x": 80, "y": 450, "w": 260, "h": 52, "fill": "#280a3c", "stroke": "#c084fc"},
            {"id": "finops_opt", "name": "FinOps Optimizer", "detail": "3-Year Flexible CUD Coverage", "x": 420, "y": 450, "w": 260, "h": 52, "fill": "#280a3c", "stroke": "#c084fc"},
        ],
        "boundaries": [
            {"x": 60, "y": 14, "w": 640, "h": 80, "label": "ON-PREMISES DATACENTER PERIMETER", "color": "#38bdf8"},
            {"x": 380, "y": 120, "w": 660, "h": 80, "label": "L2 EXTENDED HYBRID MIGRATION FABRIC", "color": "#10b981"},
            {"x": 60, "y": 330, "w": 640, "h": 80, "label": "TARGET GOOGLE CLOUD SDDC & IaaS PERIMETER", "color": "#a855f7"},
        ],
        "flows": [
            {"x1": 210, "y1": 82, "x2": 210, "y2": 135, "type": "ok", "label": "Interconnect Pipe"},
            {"x1": 420, "y1": 161, "x2": 340, "y2": 161, "type": "ok", "label": "HCX Encapsulation"},
            {"x1": 550, "y1": 187, "x2": 760, "y2": 240, "type": "ok", "label": "Inventory Telemetry"},
            {"x1": 210, "y1": 187, "x2": 210, "y2": 345, "type": "ok", "label": "HCX Live vMotion"},
            {"x1": 550, "y1": 187, "x2": 550, "y2": 345, "type": "ok", "label": "Migrate for Compute"},
            {"x1": 210, "y1": 397, "x2": 210, "y2": 450, "type": "ok", "label": "DB Replatforming"},
            {"x1": 550, "y1": 397, "x2": 550, "y2": 450, "type": "ok", "label": "Rightsized Billing"},
        ],
        "probes": [
            {"cx": 210, "cy": 161, "label": "PROBE 1: Interconnect Throughput & HCX Sync Lag", "color": "#f59e0b"},
            {"cx": 760, "cy": 240, "label": "PROBE 2: VM Rightsizing Utilization Drift (p95)", "color": "#22c55e"},
            {"cx": 210, "cy": 371, "label": "PROBE 3: GCVE vSAN Storage Watermark (> 75%)", "color": "#f43f5e"},
        ]
    },
    "part3_intro": (
        "The following field cases analyze real-world migration failures triggered by flawed assessments, missing dependency "
        "analysis, and unoptimized sizing. Each scenario includes quantitative impact data, diagnostic traces, root cause postmortems, "
        "defensible remediations, and dual-lane failed/corrected architectural diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author multi-attribute 6 Rs "
        "scoring engines, graph-based migration wave clustering scripts, StratoZone-style compute rightsizing algorithms, and "
        "GCVE vSAN storage physics calculators."
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
                "#### 1. The 6 Rs Decision Framework Taxonomy\n\n"
                "Enterprise application portfolio rationalization categorizes every workload into one of six canonical paths:\n\n"
                "- **Rehost (Lift & Shift):** Moving virtual machines directly to Google Compute Engine (or GCVE) without architectural or "
                "code modifications. Best when driven by fixed datacenter lease expirations, hardware end-of-life, or rapid datacenter evacuation.\n"
                "- **Replatform (Lift & Reshape):** Making targeted infrastructure-level optimizations without changing core business logic "
                "(e.g. migrating self-hosted PostgreSQL to Cloud SQL, or running containerized workloads on GKE via Migrate to Containers). "
                "Reduces operational management overhead while preserving codebase stability.\n"
                "- **Refactor (Cloud-Native Re-architecting):** Deconstructing monolithic applications into microservices, serverless Cloud Run "
                "functions, and globally distributed databases (Cloud Spanner). Yields maximum elasticity, high agility, and global scale, but "
                "requires extensive engineering investment, long delivery timelines (6–18 months), and rigorous integration testing.\n"
                "- **Repurchase (Drop & Shop):** Retiring a legacy custom-built or licensed application in favor of an off-the-shelf Software-as-a-Service "
                "(SaaS) product (e.g. replacing a legacy CRM VM with Salesforce, or self-hosted email with Google Workspace).\n"
                "- **Retain (Revisit / Do Nothing):** Keeping workloads in on-premises datacenters due to un-amortized hardware depreciation, "
                "extreme low-latency factory robotics requirements, or sovereign data residency constraints.\n"
                "- **Retire (Decommission):** Identifying and shutting down zombie workloads. Up to 15–20% of enterprise server estates run legacy "
                "reporting or test environments that serve zero active users and can be powered off immediately.\n\n"
                "#### 2. The Trap of Premature Refactoring\n\n"
                "The most catastrophic migration error is attempting to refactor complex applications while simultaneously racing against a "
                "hard datacenter lease deadline. Refactoring introduces code regressions, architectural unknowns, and prolonged QA cycles. "
                "When deadlines approach, partially refactored workloads cannot be deployed, trapping the organization in the datacenter.\n\n"
                "**The Two-Phase Modernization Mandate:** First, achieve datacenter exit velocity via **Rehost** or **GCVE** to eliminate "
                "lease liabilities. Once workloads run stably in Google Cloud, execute iterative **Refactoring** projects prioritized by business ROI.\n\n"
                "#### 3. Architectural Trade-offs: The 6 Rs Strategic Spectrum\n\n"
                "| 6 Rs Strategy | Velocity to Cloud | Engineering Effort | Upfront Cost | Post-Migration Operating Cost | Architectural Agility |\n"
                "|---|---|---|---|---|---|\n"
                "| **Rehost** | Highest (Days to Weeks) | Minimal (Ops only) | Lowest ($) | Moderate (Unoptimized VMs) | Baseline (Same as on-prem) |\n"
                "| **Replatform** | Moderate (1 – 3 Months) | Low to Medium | Low ($$) | Optimized (Managed services) | Moderate (PaaS benefits) |\n"
                "| **Refactor** | Lowest (6 – 18 Months) | Extreme (Full Dev rewrite) | Highest ($$$$) | Lowest per unit (True serverless) | Maximum (Elastic cloud-native) |\n"
                "| **Repurchase** | Fast (Vendor dependent) | Data migration only | Variable (SaaS licensing) | Predictable per-seat | High (Vendor roadmap) |\n"
                "| **Retire** | Immediate (Hours) | Zero (Shutdown script) | Negative (Instant savings) | $0.00 | N/A (Eliminated debt) |\n"
            ),
            "questions": [
                "Under what operational conditions should an architect mandate Rehost over Refactor?",
                "What architectural risks emerge from attempting portfolio-wide refactoring during a lease exit?",
                "How does Replatforming (e.g., Cloud SQL) bridge the gap between Rehost speed and Refactor agility?",
                "What discovery techniques uncover zombie workloads eligible for immediate Retirement?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/migration-to-google-cloud",
            "reference_label": "Google Cloud Architecture Center: Migration to Google Cloud: Choosing your migration path",
            "scenario": {
                "scenario": (
                    "Faced with an immovable 4-month datacenter lease expiration, the Chief Technology Officer of a retail logistics company "
                    "mandated that all 45 internal logistics applications must be fully refactored into microservices running on GKE and Cloud Spanner "
                    "prior to cloud deployment. Three months into the migration schedule, 38 of the 45 development teams were bogged down in "
                    "unresolved distributed transaction bugs, broken ORM mappings, and database schema migrations. With 18 days remaining on the "
                    "datacenter lease, only 3 services had passed staging integration tests. The commercial landlord issued an official notice that "
                    "failure to vacate on schedule would trigger a holdover penalty of $15,000 per day plus mandatory 12-month lease renewal."
                ),
                "impact": (
                    "P1 existential operational crisis. 42 critical logistics applications remained stuck on on-premises hardware. Commercial "
                    "lease holdover penalties accrued to $315,000 over 21 days of overstay. The emergency migration bridge consumed 100% of "
                    "engineering capacity, halting all customer-facing product development for an entire quarter."
                ),
                "constraints": (
                    "Vacate on-premises datacenter within 30 days; achieve zero downtime for warehouse scanning APIs; preserve existing database "
                    "transactional consistency; minimize throwaway engineering effort."
                ),
                "evidence": (
                    "Project milestone burn-down telemetry and landlord penalty notice:\n\n"
                    "```text\n"
                    "MIGRATION PROGRAM STATUS DASHBOARD - DAY T-18 BEFORE LEASE EXPIRATION\n"
                    "========================================================================\n"
                    "Target Workloads: 45 Enterprise Applications\n"
                    "Workloads in Production on GKE / Spanner:  3 ( 6.7% - Refactor Stalled)\n"
                    "Workloads Blocked in Distributed QA:       38 (84.4% - ORM/2PC Regressions)\n"
                    "Workloads Unstarted:                        4 ( 8.9%)\n"
                    "Burn-down Velocity: 0.8 apps/month (Required: 15.0 apps/month to hit deadline)\n"
                    "\n"
                    "COMMERCIAL LEASE OVERSTAY INVOICE (Datacenter Facility Metro-West):\n"
                    "Invoice #: INV-2026-0928-OVERSTAY\n"
                    "Daily Holdover Penalty Rate: $15,000.00 / day\n"
                    "Days Accrued Post-Expiration: 21 Days\n"
                    "Total Penalty Assessed: $315,000.00 USD\n"
                    "Mandatory 12-Month Lease Renewal Penalty Pending Trigger at Day 30!\n"
                    "```"
                ),
                "diagnostic_steps": [
                    "Step 1: Audit project velocity metrics; confirm refactoring velocity of 0.8 applications per month makes meeting the datacenter exit deadline mathematically impossible.",
                    "Step 2: Inspect code repositories and pull requests; observe hundreds of stalled PRs wrestling with distributed transaction sagas and cross-service joins.",
                    "Step 3: Review on-premises hypervisor telemetry; confirm the remaining 42 applications run on standard VMware ESXi virtual machines with compatible Linux/Windows OS kernels.",
                    "Step 4: Check network interconnect; verify a 10 Gbps Dedicated Cloud Interconnect is already provisioned and operational between the datacenter and Google Cloud `us-central1`."
                ],
                "root": (
                    "Conflating a fixed timeline datacenter lease exit with architectural application refactoring. The enterprise attempted "
                    "high-friction software re-engineering while under a severe time constraint, causing milestone collapse and catastrophic financial penalties."
                ),
                "remediation_steps": [
                    "Step 1: Immediately halt all active refactoring development; freeze application source code branches to stabilize binaries.",
                    "Step 2: Pivot the migration program to a two-phase strategy: execute an immediate **Rehost** of all 42 remaining VMs to Google Compute Engine using Migrate to Virtual Machines (m4vm).",
                    "Step 3: Replicate VM block storage continuously over the 10 Gbps Interconnect; conduct cutover waves over two successive weekends.",
                    "Step 4: Once all workloads are running in Google Cloud and the on-premises datacenter is decommissioned, resume iterative refactoring on high-ROI services using cloud-native managed services."
                ],
                "verify": (
                    "Execute test cutover wave of 10 VMs using Migrate to Virtual Machines. Verify block replication completes in under 4 hours, "
                    "cutover downtime is under 12 minutes per VM, and logistics scanning services resume normal operations in Compute Engine."
                ),
                "residual": (
                    "Rehosting applications directly to Compute Engine preserves existing software technical debt and operating inefficiencies; "
                    "teams must enforce FinOps governance and committed use discounts until workloads can be replatformed."
                ),
                "diagram": (
                    "Enforce 100% Refactor under 4-month lease",
                    "38/45 apps blocked; velocity collapses",
                    "Lease expires, $315k overstay penalty",
                    "Pivot to m4vm Rehost; migrate in 14 days",
                    "Datacenter exited; refactor staged in cloud"
                ),
                "facts": "Refactor attempted for 45 apps in 4 months; only 3 finished; lease expired; $315k holdover penalties accrued.",
                "inference": "Fixed datacenter deadlines demand low-friction Rehost; architectural Refactoring must occur post-migration.",
                "expected": "Migrate to VMs completes lift-and-shift in 14 days, exiting the datacenter and eliminating overstay liabilities."
            },
            "lab": {
                "name": "6 Rs Portfolio Scoring Engine & Rationalization Matrix",
                "file": "day-075-6r-matrix.md",
                "goal": "Author a quantitative 6 Rs decision matrix and build an executable Python scoring engine to classify enterprise workloads.",
                "expected": "A complete 6 Rs decision rubric, an executable Python rationalization script, and classified workload portfolio output.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 74 architecture boundaries and Day 71 performance sizing",
                "preflight": "Review Google Cloud Migration Center workload classification guidelines.",
                "steps": [
                    "#### Stage 1: Pre-Flight Application Portfolio & Constraint Invariants\nDraft the enterprise application inventory in <kbd>day-075-6r-matrix.md</kbd>. Define quantitative criteria: business criticality, remaining hardware lifespan, software licensing constraints, and developer capacity.",
                    "#### Stage 2: Authoring the Multi-Attribute 6 Rs Decision Schema\nDefine the scoring criteria and weighting parameters for evaluating migration pathways:\n\n```text\nEVALUATION DIMENSIONS:\n1. Timeline Urgency (1 = No deadline, 10 = Immediate lease exit)\n2. Architectural Fit (1 = Tightly coupled legacy, 10 = 12-factor cloud-ready)\n3. Business Value / ROI (1 = Commoditized utility, 10 = Core competitive differentiator)\n4. Licensing Portability (1 = Locked to proprietary hardware, 10 = Open source / BYOL)\n```",
                    "#### Stage 3: Developing the Automated Python 6 Rs Rationalization Engine\nImplement the decision classifier in Python (<kbd>score_portfolio_6r.py</kbd>):\n\n```python\n# score_portfolio_6r.py\n\"\"\"Automated 6 Rs migration decision engine evaluating enterprise workloads.\"\"\"\nfrom typing import Dict, List, Tuple\n\nclass PortfolioScorer:\n    def classify_workload(self, name: str, timeline_urgency: int, cloud_readiness: int, business_roi: int, is_active: bool) -> str:\n        if not is_active:\n            return 'RETIRE'\n        if timeline_urgency >= 8:\n            if cloud_readiness <= 4:\n                return 'REHOST'  # Urgency forces lift & shift\n            else:\n                return 'REPLATFORM'  # Quick containerization or managed DB\n        if business_roi >= 8 and cloud_readiness >= 6:\n            return 'REFACTOR'  # High-value candidate for cloud-native rewrite\n        if cloud_readiness <= 3 and business_roi <= 4:\n            return 'RETAIN'  # Keep on-prem until hardware amortized\n        return 'REPLATFORM'\n\nif __name__ == '__main__':\n    scorer = PortfolioScorer()\n    portfolio = [\n        (\"warehouse_scanner_api\", 9, 3, 9, True),   # High urgency, low readiness -> REHOST\n        (\"customer_loyalty_svc\", 4, 8, 9, True),    # Low urgency, high readiness -> REFACTOR\n        (\"legacy_crystal_reports\", 2, 1, 2, False), # Unused -> RETIRE\n        (\"inventory_relational_db\", 8, 5, 8, True), # High urgency, moderate -> REPLATFORM\n    ]\n    for app, urg, fit, roi, active in portfolio:\n        decision = scorer.classify_workload(app, urg, fit, roi, active)\n        print(f\"{app:<25} -> DECISION: {decision}\")\n```",
                    "#### Stage 4: Workload Assessment Execution & Candidate Classification\nRun the scoring engine to evaluate the candidate workloads:\n\n```sh\npython3 score_portfolio_6r.py\n```",
                    "#### Stage 5: Simulating Tight Datacenter Lease Deadline Constraint Override\nVerify that the engine properly overrides Refactor decisions when timeline urgency hits maximum:\n\n```python\n# test_urgency_override.py\nfrom score_portfolio_6r import PortfolioScorer\n\nscorer = PortfolioScorer()\n# Even high ROI apps must be Rehosted if deadline is immediate (urgency = 10, readiness = 3)\ndecision = scorer.classify_workload('core_billing', timeline_urgency=10, cloud_readiness=3, business_roi=10, is_active=True)\nassert decision == 'REHOST', f\"Urgency override failed! Got {decision}\"\nprint(\"[PASS] Urgency override successfully redirected core_billing to REHOST to prevent deadline breach.\")\n```",
                    "#### Stage 6: Chaos Injection (Simulating Refactor Timeline Slippage & Cost Spillover)\nSimulate financial cost modeling comparing immediate Rehost vs stalled Refactor with holdover penalties:\n\n```sh\npython3 -c \"\nrehost_cost = 14 * 2500 # 14 days migration\nrefactor_cost = (90 * 2500) + (21 * 15000) # 90 days dev + 21 days penalty\nprint(f'Rehost Total: ${rehost_cost:,} vs Refactor Total: ${refactor_cost:,}')\nassert refactor_cost > rehost_cost * 10\nprint('Financial Stress Test Confirmed: Refactor under lease deadline is 15x more expensive!')\n\"\n```",
                    "#### Stage 7: Triage, Troubleshooting & Portfolio Rebalancing Runner\nAuthor an inventory export script (<kbd>export_decisions.py</kbd>) that formats migration waves based on the classified decisions:\n\n```python\n# export_decisions.py\n\"\"\"Groups classified applications into phased execution waves.\"\"\"\nwaves = {'Wave 1 (Rehost)': ['warehouse_scanner_api'], 'Wave 2 (Replatform)': ['inventory_relational_db'], 'Decommission': ['legacy_crystal_reports']}\nfor wave, apps in waves.items():\n    print(f\"{wave}: {', '.join(apps)}\")\n```",
                    "#### Stage 8: Operational Teardown & Migration Governance Checklist\nVerify that all workloads classified as Rehost include a post-migration optimization milestone in the project roadmap. Confirm that no chargeable cloud resources were provisioned during the offline architectural simulation."
                ],
                "verification": (
                    "Run automated portfolio classification test suite:\n\n```sh\npython3 score_portfolio_6r.py && python3 -c \"import test_urgency_override\" && python3 export_decisions.py\n```\n\nConfirm output displays `[PASS] Urgency override successfully redirected` and correct wave groupings."
                ),
                "trouble": (
                    "If active workloads are classified as RETIRE, verify that <kbd>is_active</kbd> boolean properly reflects production traffic."
                ),
                "cleanup": "No remote cloud resources created; retain scoring scripts and classification rubrics in local repository.",
                "accept": "A validated 6 Rs decision rubric, an executable Python rationalization script, and classified workload portfolio output."
            }
        },
        {
            "key": "topic-02",
            "title": "Migration Lifecycle Phases: Assess, Plan, Deploy, and Optimize",
            "overview": (
                "Architect enterprise migration programs across four disciplined phases: Assess (discovery & TCO), "
                "Plan (wave grouping & landing zones), Deploy (replication & cutover), and Optimize (rightsizing & modernizing)."
            ),
            "preview": (
                "Wave 2 cutover migrates an ERP database VM without discovering an undocumented SMB file share dependency on-prem; "
                "Monday morning warehouse shipping labels fail to print, halting physical distribution for 8 hours."
            ),
            "technical": (
                "#### 1. The Four-Phase Migration Lifecycle\n\n"
                "Successful enterprise cloud migrations execute across four structured, sequential phases:\n\n"
                "- **Phase 1: Assess (Discovery & Feasibility):** Deploy agentless discovery tooling across the infrastructure estate. "
                "Catalog all physical hosts, virtual machines, database instances, OS versions, installed software packages, and network traffic flows. "
                "Compute rightsized total cost of ownership (TCO) baselines.\n\n"
                "- **Phase 2: Plan (Wave Grouping & Landing Zone Foundation):** Deconstruct the portfolio into migration waves based on "
                "network affinity clustering. Applications with tight, low-latency inter-service dependencies must migrate in the same cutover "
                "wave. Concurrently, build and validate the enterprise Landing Zone (Resource Hierarchy, Shared VPC, Cloud Interconnect, IAM baselines).\n\n"
                "- **Phase 3: Deploy (Replication, Rehearsal, & Cutover):** Establish continuous data replication pipelines (Migrate to VMs block "
                "replication, Datastream CDC, or VMware HCX). Conduct non-disruptive cutover rehearsals in isolated VPC test environments. "
                "Execute the production cutover during scheduled maintenance windows with explicit rollback triggers.\n\n"
                "- **Phase 4: Optimize (FinOps Rightsizing & Modernization):** Analyze post-migration telemetry using Cloud Monitoring and Cost "
                "Optimization recommendations. Downsize idle CPU/RAM allocations, purchase 1-year and 3-year Committed Use Discounts (CUDs), "
                "and begin replatforming workloads into managed databases and containers.\n\n"
                "#### 2. Network Affinity Clustering and Wave Planning\n\n"
                "Migrating enterprise applications individually almost always results in failure due to hidden cross-server network dependencies. "
                "If Server A is migrated to Google Cloud while its tightly coupled database Server B remains on-premises, inter-service calls "
                "suddenly traverse the hybrid WAN link, incurring a 20x latency penalty.\n\n"
                "Architects utilize **Affinity Grouping** based on NetFlow and VPC Flow Logs: any pair of servers communicating with high bandwidth "
                "or sub-5ms sensitivity are bound into an **Atomic Migration Wave**. They migrate together, or they do not migrate at all.\n\n"
                "#### 3. Architectural Trade-offs: Migration Phase Gates\n\n"
                "| Phase Gate | Mandatory Entry Deliverables | Success Criteria & Exit Sign-off | Common Risk / Failure Mode |\n"
                "|---|---|---|---|\n"
                "| **Phase 1: Assess** | Complete CMDB export, NetFlow telemetry | Validated TCO model, 6 Rs categorization | Incomplete asset discovery; missing zombie VMs |\n"
                "| **Phase 2: Plan** | Landing Zone deployed, Shared VPC active | Affinity-mapped migration waves, DR runbook | Splitting tightly coupled apps across waves |\n"
                "| **Phase 3: Deploy** | Block replication in sync (< 5 min lag) | Cutover rehearsal passed; business sign-off | Overrunning maintenance window; broken rollback |\n"
                "| **Phase 4: Optimize** | 30 days of Cloud Monitoring telemetry | Rightsized VM shapes; CUDs purchased | Leaving over-provisioned VMs running indefinitely |\n"
            ),
            "questions": [
                "Why must network dependency affinity mapping occur prior to wave grouping in Phase 2?",
                "What exact deliverables are required to pass the Phase 3 Deploy gate into production cutover?",
                "How does Phase 4 Optimize systematically reduce cloud infrastructure spend post-cutover?",
                "What operational criteria dictate an immediate cutover rollback during Phase 3?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/migration-to-google-cloud/planning",
            "reference_label": "Google Cloud Architecture Center: Migration planning and execution guide",
            "scenario": {
                "scenario": (
                    "During Wave 2 of Brightloaf's datacenter migration, engineers migrated the core ERP billing engine virtual machine to "
                    "Google Compute Engine using Migrate to Virtual Machines. The VM cutover succeeded, database connectivity was established, "
                    "and the VM passed internal health checks. However, when the automated morning shipping batch ran at 06:00, 14 warehouse "
                    "thermal label printers threw unhandled I/O exceptions. The billing engine had a hardcoded UNC path dependency "
                    "(`\\\\192.168.10.45\\shipping_labels`) to an un-migrated Windows legacy file share on-premises. Because the on-premises subnet "
                    "lacked a return route to the new Google Cloud VPC subnet, SMB file writes timed out after 120 seconds. Pallet staging "
                    "halted across 4 major distribution centers, backing up 8,500 customer shipments."
                ),
                "impact": (
                    "P1 logistics shutdown. 8,500 customer delivery shipments stalled for 8 hours. Warehouse workers idled across 4 distribution "
                    "centers. Estimated supply chain delay penalty: $185,000. Executive emergency bridge convened to evaluate rollback."
                ),
                "constraints": (
                    "Restore shipping label generation within 60 minutes; identify all cross-premises network dependencies; establish an automated "
                    "pre-cutover dependency verification checklist."
                ),
                "evidence": (
                    "ERP application exception stack trace and TCP network routing failure dump:\n\n"
                    "```text\n"
                    "2026-09-28 06:02:14 UTC [Thread-14] ERROR com.brightloaf.erp.LabelDispatcher - Failed to dispatch batch 98124\n"
                    "java.io.IOException: The network name cannot be found\n"
                    "    at jcifs.smb.SmbTransport.send(SmbTransport.java:622)\n"
                    "    at jcifs.smb.SmbSession.send(SmbSession.java:238)\n"
                    "    at jcifs.smb.SmbFile.createNewFile(SmbFile.java:1381)\n"
                    "    at com.brightloaf.erp.LabelDispatcher.writeLabel(LabelDispatcher.java:88)\n"
                    "Caused by: java.net.ConnectException: Connection timed out: //192.168.10.45/shipping_labels\n"
                    "\n"
                    "$ gcloud compute ssh erp-billing-vm --zone=us-central1-a --command=\"traceroute 192.168.10.45\"\n"
                    "traceroute to 192.168.10.45 (192.168.10.45), 30 hops max, 60 byte packets\n"
                    " 1  10.142.0.1 (10.142.0.1)  0.312 ms  0.285 ms  0.270 ms\n"
                    " 2  * * * (Request Timed Out - No Return Route in On-Prem Firewall)\n"
                    " 3  * * * (Destination Net Unreachable)\n"
                    "```"
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect application error logs on the newly migrated `erp-billing-vm`; locate repeated `ConnectException` to on-premises IP `192.168.10.45`.",
                    "Step 2: Check on-premises firewall logs; observe TCP port 445 (SMB) traffic arriving from Google Cloud VPC subnet `10.142.0.0/20` dropped due to missing routing rules.",
                    "Step 3: Review Phase 1 and 2 migration assessment documentation; discover `192.168.10.45` was omitted from the dependency discovery inventory because it was configured via NetBIOS name rather than DNS.",
                    "Step 4: Audit active network connections; confirm 14 warehouse label dispatchers rely on synchronous SMB writes before marking orders as dispatched."
                ],
                "root": (
                    "Flawed Phase 1 discovery and Phase 2 wave planning failed to detect a legacy hardcoded SMB file share dependency. Migrating "
                    "the ERP compute node without migrating its dependent file server or configuring bidirectional hybrid routing caused catastrophic I/O timeouts."
                ),
                "remediation_steps": [
                    "Step 1: Tactical Fix: Immediately establish a temporary static route on the on-premises core router directing return traffic for `10.142.0.0/20` through the Dedicated Interconnect, unblocking SMB writes.",
                    "Step 2: Strategic Fix: Migrate the legacy on-premises file share into Google Cloud Filestore or Cloud Storage using Cloud Storage FUSE.",
                    "Step 3: Mandate automated NetFlow / VPC Flow Logs dependency discovery for all future migration waves, enforcing atomic cutover of all coupled nodes.",
                    "Step 4: Implement a mandatory 24-hour pre-cutover rehearsal in an isolated VPC test subnet to validate all external service integrations."
                ],
                "verify": (
                    "Trigger synthetic label generation test from `erp-billing-vm` to `\\\\192.168.10.45\\shipping_labels`. Confirm SMB file write "
                    "completes in 18ms and warehouse printers resume processing at full line-rate."
                ),
                "residual": (
                    "Cross-premises SMB writes over Dedicated Interconnect incur a 12ms RTT latency penalty; the file share must be migrated to "
                    "Google Cloud Filestore to restore sub-millisecond local performance."
                ),
                "diagram": (
                    "Migrate ERP billing VM in Wave 2",
                    "Hardcoded on-prem SMB share unreachable",
                    "Label printers stall; 8,500 orders backed up",
                    "Add hybrid route; plan Filestore migration",
                    "Shipping resumes; mandate flow log analysis"
                ),
                "facts": "ERP VM migrated without SMB file share; warehouse label printers timed out; 8,500 shipments stalled for 8 hours; $185k penalty.",
                "inference": "Isolated VM migrations without network flow dependency mapping trigger critical runtime disconnections.",
                "expected": "Dependency discovery binds coupled services into atomic migration waves, preventing hybrid connection breaks."
            },
            "lab": {
                "name": "Migration Wave Planning & Dependency Clustering Engine",
                "file": "day-075-wave-planner.md",
                "goal": "Build a network dependency clustering engine in Python that maps communication telemetry into atomic migration waves.",
                "expected": "A complete wave planning specification, an executable Python graph clustering script, and verified wave assignment output.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 74 enterprise foundation and Day 72 networking",
                "preflight": "Review Google Cloud Migration Center group planning concepts and graph clustering algorithms.",
                "steps": [
                    "#### Stage 1: Pre-Flight Dependency Graph & Network Flow Invariants\nDraft the enterprise network flow criteria in <kbd>day-075-wave-planner.md</kbd>. Establish the boundary thresholds: any pair of servers exchanging > 10,000 packets/day or requiring < 5ms RTT must belong to the same atomic wave.",
                    "#### Stage 2: Defining the Application Network Flow Specification\nCreate the synthetic network communication dataset (<kbd>network_flows.json</kbd>) modeling server inter-connections:\n\n```json\n[\n  {\"source\": \"web_frontend_01\", \"target\": \"app_server_01\", \"packet_rate_per_sec\": 450, \"latency_sensitive\": true},\n  {\"source\": \"app_server_01\", \"target\": \"erp_billing_db\", \"packet_rate_per_sec\": 1200, \"latency_sensitive\": true},\n  {\"source\": \"app_server_01\", \"target\": \"smb_label_share\", \"packet_rate_per_sec\": 85, \"latency_sensitive\": true},\n  {\"source\": \"analytics_worker\", \"target\": \"erp_billing_db\", \"packet_rate_per_sec\": 12, \"latency_sensitive\": false},\n  {\"source\": \"inventory_api\", \"target\": \"inventory_db\", \"packet_rate_per_sec\": 600, \"latency_sensitive\": true}\n]\n```",
                    "#### Stage 3: Developing the Graph-Based Wave Clustering Script in Python\nImplement the graph traversal clustering algorithm (<kbd>cluster_migration_waves.py</kbd>):\n\n```python\n# cluster_migration_waves.py\n\"\"\"Clusters interconnected enterprise servers into atomic migration waves.\"\"\"\nimport json\nfrom collections import defaultdict\nfrom typing import Dict, Set, List\n\nclass MigrationWaveClusterer:\n    def __init__(self):\n        self.adj = defaultdict(set)\n\n    def add_flow(self, src: str, dst: str, is_atomic: bool):\n        if is_atomic:\n            self.adj[src].add(dst)\n            self.adj[dst].add(src)\n\n    def compute_atomic_waves(self) -> List[Set[str]]:\n        visited = set()\n        waves = []\n        for node in list(self.adj.keys()):\n            if node not in visited:\n                wave = set()\n                queue = [node]\n                visited.add(node)\n                while queue:\n                    curr = queue.pop(0)\n                    wave.add(curr)\n                    for neighbor in self.adj[curr]:\n                        if neighbor not in visited:\n                            visited.add(neighbor)\n                            queue.append(neighbor)\n                waves.append(wave)\n        return waves\n\nif __name__ == '__main__':\n    with open('network_flows.json', 'r') as f:\n        flows = json.load(f)\n    clusterer = MigrationWaveClusterer()\n    for f in flows:\n        clusterer.add_flow(f['source'], f['target'], f['latency_sensitive'])\n    waves = clusterer.compute_atomic_waves()\n    for i, w in enumerate(waves, 1):\n        print(f\"ATOMIC MIGRATION WAVE {i}: {sorted(list(w))}\")\n```",
                    "#### Stage 4: Executing Wave Segmentation & Dependency Boundary Validation\nRun the dependency clustering engine to identify atomic migration waves:\n\n```sh\npython3 cluster_migration_waves.py\n```",
                    "#### Stage 5: Simulating Hidden Inter-Service Dependency Insertion\nAdd an unmapped legacy dependency to the flow definition and verify that the clustering algorithm automatically binds it into Wave 1:\n\n```python\n# test_dependency_injection.py\nfrom cluster_migration_waves import MigrationWaveClusterer\n\nclusterer = MigrationWaveClusterer()\nclusterer.add_flow('app_server_01', 'erp_billing_db', True)\nclusterer.add_flow('app_server_01', 'smb_label_share', True)\n\nwaves = clusterer.compute_atomic_waves()\nassert len(waves) == 1\nassert 'smb_label_share' in waves[0]\nprint(\"[PASS] Dependency clustering bound smb_label_share into the same atomic wave as app_server_01.\")\n```",
                    "#### Stage 6: Chaos Injection (Network Latency Spike on Cutover Rollback)\nSimulate what happens if an atomic wave is split across regions by calculating added round-trip network transit latency:\n\n```sh\npython3 -c \"\npacket_rate = 1200 # packets per sec\nwan_latency_penalty_ms = 18.0\nadded_delay_sec = (packet_rate * wan_latency_penalty_ms) / 1000.0\nprint(f'Cumulative WAN delay if split: {added_delay_sec:.1f} seconds per second of execution!')\nassert added_delay_sec > 10.0\nprint('Chaos Validation Passed: Splitting atomic wave collapses throughput!')\n\"\n```",
                    "#### Stage 7: Triage, Troubleshooting & Wave Decoupling Runbook\nDocument the wave cutover runbook in <kbd>day-075-wave-planner.md</kbd>. Specify that any wave execution that exceeds its cutover maintenance window by more than 25% triggers an immediate, automated rollback.",
                    "#### Stage 8: Operational Teardown & Cutover Readiness Invariant Checklist\nVerify that all migration wave manifests declare explicit rollback validation commands. Confirm that no chargeable cloud resources were provisioned during the offline architectural simulation."
                ],
                "verification": (
                    "Run automated wave planning test suite:\n\n```sh\npython3 cluster_migration_waves.py && python3 -c \"import test_dependency_injection\"\n```\n\nConfirm output displays `ATOMIC MIGRATION WAVE 1: ['app_server_01', 'erp_billing_db', 'smb_label_share', 'web_frontend_01']`."
                ),
                "trouble": (
                    "If servers are incorrectly split across waves, verify that <kbd>latency_sensitive</kbd> flag is set to True in the flow configuration."
                ),
                "cleanup": "No remote cloud resources created; retain flow specifications and clustering scripts in local repository.",
                "accept": "A validated wave planning specification, an executable Python graph clustering script, and verified wave assignment output."
            }
        },
        {
            "key": "topic-03",
            "title": "Discovery and Assessment Tools: Migration Center, StratoZone-Style Rightsizing",
            "overview": (
                "Deploy automated enterprise discovery tools. Master Google Cloud Migration Center, StratoZone inventory collectors, "
                "mFit assessment heuristics, and empirical utilization-based compute rightsizing."
            ),
            "preview": (
                "Direct 1:1 lift-and-shift of 350 on-prem VMs using provisioned hardware specs (e.g. 16 vCPU, 64 GB RAM) runs up a "
                "$145,000 monthly cloud bill; actual p95 CPU load across the fleet was under 4%."
            ),
            "technical": (
                "#### 1. Automated Discovery Tooling: Migration Center and StratoZone\n\n"
                "Manual discovery using spreadsheets fails in enterprise environments due to un-updated CMDB records, shadow IT VMs, and hidden "
                "network dependencies. Google Cloud provides unified discovery and assessment platforms:\n\n"
                "- **Google Cloud Migration Center:** The unified migration hub in Cloud Console. Integrates asset discovery (importing from VMware vCenter, "
                "AWS, Azure, or CSV), performance data collection, automated grouping, and TCO financial estimations.\n"
                "- **StratoZone Discovery Engine:** Deploys an agentless collector appliance (OVA / Hyper-V) into on-premises subnets. Queries vCenter "
                "APIs and WMI/SSH to sample real-time CPU, RAM, disk I/O, and network telemetry every 15 minutes for 30 days.\n"
                "- **mFit (Migrate to Containers Assessment):** Evaluates Linux and Windows virtual machines to determine containerization suitability, "
                "flagging kernel dependencies, filesystem locks, and service daemons.\n\n"
                "#### 2. The Provisioned vs. Observed Rightsizing Math\n\n"
                "In traditional on-premises datacenters, system administrators over-allocate hardware to avoid procurement friction. A typical "
                "VM is allocated 16 vCPUs and 64 GB RAM, but operates at an average CPU utilization of 3.2% with peak p95 utilization of 7.5%.\n\n"
                "If an enterprise lifts-and-shifts 1:1 to Google Compute Engine based on **allocated** specs, they provision expensive `n2-standard-16` "
                "instances ($388/month each). By analyzing **observed** telemetry (p95 CPU and memory working set), Migration Center rightsizes "
                "the workload to `e2-standard-4` ($97/month) or `e2-custom` shapes, achieving an immediate **60% to 75% baseline cost reduction**.\n\n"
                "#### 3. Financial Modeling: As-Is vs. Optimized TCO\n\n"
                "A defensible cloud business case models four cost dimensions:\n\n"
                "  1. **Compute Rightsizing:** Downsizing VM shapes to p95 utilization + 20% safety headroom.\n"
                "  2. **Committed Use Discounts (CUDs):** Purchasing 1-year or 3-year Flexible or Resource-Based CUDs (saving 37% to 57%).\n"
                "  3. **Storage Tiering:** Moving unattached or cold VMDK volumes to balanced persistent disk and Cloud Storage coldline archive.\n"
                "  4. **Software Licensing (BYOL vs License-Included):** Migrating Windows/SQL Server licenses under Microsoft Azure Hybrid Benefit "
                "or Sole-Tenant Nodes to avoid dual-licensing penalties.\n\n"
                "#### 4. Architectural Trade-offs: Discovery Paradigms\n\n"
                "| Discovery Mechanism | Deployment Effort | Telemetry Granularity | Network Dependency Mapping | Best Suited For |\n"
                "|---|---|---|---|---|\n"
                "| **Static CMDB Export** | Lowest (CSV upload) | Static (Allocated CPU/RAM only) | None (Blind to network) | High-level feasibility & ballpark budgeting |\n"
                "| **StratoZone Agentless OVA** | Moderate (Appliance on vCenter) | High (15-min sampling of CPU/RAM/IOPS) | High (NetFlow / TCP connection tables) | Comprehensive datacenter assessment & TCO |\n"
                "| **OS-Level Discovery Agents** | Highest (Agent on every VM) | Deepest (Process tables, config files) | Deepest (Full packet-level payload) | High-risk legacy applications & security audits |\n"
            ),
            "questions": [
                "Why does sizing cloud virtual machines based on allocated on-premises hardware cause severe budget overruns?",
                "What is the mathematical definition of p95 utilization in StratoZone rightsizing algorithms?",
                "How does Google Cloud Migration Center unify discovery across VMware, physical servers, and multicloud?",
                "Under what operational conditions are Sole-Tenant Nodes required for BYOL licensing optimization?",
            ],
            "reference": "https://docs.cloud.google.com/migration-center/docs",
            "reference_label": "Google Cloud Migration Center Documentation: Discovery and assessment guide",
            "scenario": {
                "scenario": (
                    "Brightloaf engaged a third-party systems integrator to execute an accelerated lift-and-shift of 350 enterprise virtual machines "
                    "from an on-premises VMware cluster to Google Compute Engine. The integrator mapped every VM 1:1 based on provisioned vCenter "
                    "specs: 350 VMs allocated an average of 16 vCPUs and 64 GB RAM were provisioned as `n2-standard-16` instances with 500 GB "
                    "Extreme Persistent Disks. When the first monthly Google Cloud invoice arrived, the compute and storage bill totaled $148,200 "
                    "(compared to a projected budget of $45,000). Upon auditing Cloud Monitoring metrics, the internal infrastructure team "
                    "discovered that 310 of the 350 instances were running at less than 3% average CPU utilization, with p95 peak utilization "
                    "never exceeding 8%."
                ),
                "impact": (
                    "Severe financial budget overrun. Monthly cloud infrastructure costs ran $103,200 over budget (a 230% cost overrun). CFO "
                    "placed an immediate freeze on all cloud migration initiatives. Cloud ROI business case was discredited at the board level."
                ),
                "constraints": (
                    "Reduce monthly compute spend to under $45,000 within 30 days; ensure zero application performance degradation; maintain "
                    "a minimum 25% CPU/memory buffer for peak traffic surges."
                ),
                "evidence": (
                    "Cloud Monitoring fleet utilization audit and billing SKU report:\n\n"
                    "```text\n"
                    "$ gcloud monitoring dashboards query --sql=\"FETCH gce_instance | metric 'compute.googleapis.com/instance/cpu/utilization' | group_by 30d, [mean: mean(value.utilization), p95: percentile(value.utilization, 95)] | top_hosts 10\"\n"
                    "INSTANCE_NAME          MEAN_CPU    P95_CPU     PROVISIONED_SHAPE    RECOMMENDED_SHAPE\n"
                    "prod-billing-worker-01   0.024       0.052      n2-standard-16       e2-standard-4\n"
                    "prod-catalog-app-04      0.018       0.041      n2-standard-16       e2-standard-2\n"
                    "prod-auth-node-12        0.031       0.068      n2-standard-16       e2-standard-4\n"
                    "FLEET SUMMARY: 350 VMs | Mean Fleet CPU: 2.8% | Mean Fleet p95: 6.4% | OVER-PROVISION FACTOR: 4.8x\n"
                    "\n"
                    "$ gcloud beta billing accounts get-spending-report 01A2B3-C4D5E6-F7G8H9 --month=2026-09\n"
                    "SKU: Compute Engine N2 Custom / Standard Instances -> Cost: $118,450.00\n"
                    "SKU: Extreme Persistent Disk (Provisioned IOPS)   -> Cost:  $29,750.00\n"
                    "TOTAL INVOICE AMOUNT: $148,200.00 (BUDGET: $45,000.00 | VARIANCE: +$103,200.00)\n"
                    "```"
                ),
                "diagnostic_steps": [
                    "Step 1: Export Cloud Monitoring utilization telemetry across all 350 Compute Engine instances for the preceding 30 days.",
                    "Step 2: Calculate p95 CPU and memory utilization percentiles; confirm 88% of instances require fewer than 4 vCPUs and 16 GB RAM.",
                    "Step 3: Review Persistent Disk provisioning; discover 350 instances were provisioned with Extreme Persistent Disk (PD-Extreme) with 10,000 provisioned IOPS each, despite actual disk I/O averaging under 80 IOPS.",
                    "Step 4: Check Committed Use Discount (CUD) coverage; observe 0% CUD coverage (100% of fleet running on on-demand hourly pricing)."
                ],
                "root": (
                    "Sizing cloud virtual machines and storage based on statically allocated on-premises hardware limits rather than empirical, "
                    "observed p95 telemetry. Over-provisioning compute and storage by nearly 5x, combined with zero Committed Use Discounts, "
                    "created massive budget inflation."
                ),
                "remediation_steps": [
                    "Step 1: Execute automated rightsizing script: downsize 310 instances from `n2-standard-16` to `e2-standard-4` or `e2-standard-2` based on p95 metrics + 25% safety headroom.",
                    "Step 2: Convert all non-database storage volumes from PD-Extreme to Balanced Persistent Disk (PD-Balanced), reducing disk cost by 72%.",
                    "Step 3: Purchase 3-Year Flexible Committed Use Discounts (CUDs) covering the baseline rightsized compute footprint (55% discount).",
                    "Step 4: Implement Google Cloud Active Assist Recommender API monitoring in CI/CD to continuously flag idle or oversized VMs."
                ],
                "verify": (
                    "Execute rightsizing across a pilot batch of 50 instances. Verify application p99 response times remain completely unchanged, "
                    "CPU utilization stabilizes in the optimal 35–50% range, and monthly projected spend drops from $148,200 to $39,400."
                ),
                "residual": (
                    "Downsized E2 machine types utilize dynamic shared host resource scheduling; ultra-latency-sensitive workloads must remain "
                    "on dedicated N2 or C2 machine types with pinned vCPUs."
                ),
                "diagram": (
                    "1:1 Lift & Shift based on allocated specs",
                    "Fleet operates at 3% CPU; $148k/mo bill",
                    "Budget overrun (+230%); CFO freezes migration",
                    "Rightsize to p95 (e2-std-4) + PD-Balanced + CUDs",
                    "Bill drops to $39.4k/mo (73% savings); SLA intact"
                ),
                "facts": "350 VMs migrated 1:1 on allocated specs; mean CPU was 2.8%; bill reached $148.2k (budget $45k); 0% CUD coverage.",
                "inference": "On-prem allocated hardware is massively bloated; rightsizing to observed p95 metrics is required to achieve cloud TCO.",
                "expected": "Rightsizing to observed utilization and applying 3-year CUDs reduces monthly spend to $39.4k while preserving performance."
            },
            "lab": {
                "name": "Migration Center / StratoZone Rightsizing & TCO Modeling Engine",
                "file": "day-075-rightsizing-tco.md",
                "goal": "Build an empirical compute rightsizing and TCO calculation algorithm in Python based on observed p95 telemetry.",
                "expected": "A complete rightsizing methodology document, an executable Python TCO calculator, and verified rightsizing output.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 71 performance optimization and Day 70 reliability",
                "preflight": "Review Google Cloud Compute Engine machine types and Committed Use Discount pricing models.",
                "steps": [
                    "#### Stage 1: Pre-Flight Telemetry Invariants & Collection Scope\nDraft the rightsizing methodology in <kbd>day-075-rightsizing-tco.md</kbd>. Establish the mathematical boundaries: rightsized target vCPU must equal ceil(observed_p95_vcpu * 1.25) to provide a 25% traffic surge buffer.",
                    "#### Stage 2: Creating Synthetic On-Premises Inventory Dump\nAuthor the raw telemetry inventory file (<kbd>onprem_inventory.json</kbd>) containing allocated and observed metrics for 5 representative virtual machines:\n\n```json\n[\n  {\"vm_name\": \"billing_app_01\", \"allocated_vcpu\": 16, \"allocated_ram_gb\": 64, \"p95_cpu_util\": 0.06, \"p95_ram_util\": 0.18},\n  {\"vm_name\": \"catalog_api_02\", \"allocated_vcpu\": 8,  \"allocated_ram_gb\": 32, \"p95_cpu_util\": 0.04, \"p95_ram_util\": 0.22},\n  {\"vm_name\": \"auth_service_01\", \"allocated_vcpu\": 16, \"allocated_ram_gb\": 64, \"p95_cpu_util\": 0.08, \"p95_ram_util\": 0.15},\n  {\"vm_name\": \"batch_worker_04\", \"allocated_vcpu\": 32, \"allocated_ram_gb\": 128, \"p95_cpu_util\": 0.03, \"p95_ram_util\": 0.10},\n  {\"vm_name\": \"core_database_01\", \"allocated_vcpu\": 32, \"allocated_ram_gb\": 128, \"p95_cpu_util\": 0.65, \"p95_ram_util\": 0.75}\n]\n```",
                    "#### Stage 3: Developing the Rightsizing Optimization Algorithm in Python\nImplement the rightsizing and financial TCO calculator (<kbd>rightsizing_optimizer.py</kbd>):\n\n```python\n# rightsizing_optimizer.py\n\"\"\"Calculates empirical rightsized shapes and cloud TCO savings.\"\"\"\nimport json\nimport math\n\ndef calculate_rightsized_cost(inventory_file: str):\n    with open(inventory_file, 'r') as f:\n        vms = json.load(f)\n    \n    n2_vcpu_month = 24.25\n    n2_ram_month = 3.25\n    e2_vcpu_month = 16.50\n    e2_ram_month = 2.20\n    cud_discount = 0.45  # 55% discount on 3-year Flexible CUD\n    \n    as_is_cost = 0.0\n    optimized_cost = 0.0\n    \n    print(f\"{'VM NAME':<20} {'AS-IS SHAPE':<15} {'RIGHTSIZED':<15} {'MONTHLY SAVINGS'}\")\n    print(\"-\" * 65)\n    \n    for vm in vms:\n        # As-is cost on allocated specs (N2)\n        v_alloc = vm['allocated_vcpu']\n        r_alloc = vm['allocated_ram_gb']\n        vm_as_is = (v_alloc * n2_vcpu_month) + (r_alloc * n2_ram_month)\n        as_is_cost += vm_as_is\n        \n        # Rightsized specs based on p95 + 25% buffer\n        v_needed = max(2, math.ceil(v_alloc * vm['p95_cpu_util'] * 1.25))\n        r_needed = max(4, math.ceil(r_alloc * vm['p95_ram_util'] * 1.25))\n        # Use E2 machine type with CUD\n        vm_opt = ((v_needed * e2_vcpu_month) + (r_needed * e2_ram_month)) * (1.0 - cud_discount)\n        optimized_cost += vm_opt\n        \n        savings = vm_as_is - vm_opt\n        print(f\"{vm['vm_name']:<20} {f'{v_alloc}v/{r_alloc}G':<15} {f'{v_needed}v/{r_needed}G':<15} ${savings:.2f}\")\n        \n    print(\"-\" * 65)\n    print(f\"TOTAL AS-IS MONTHLY SPEND:    ${as_is_cost:.2f}\")\n    print(f\"TOTAL OPTIMIZED MONTHLY SPEND: ${optimized_cost:.2f}\")\n    pct_savings = ((as_is_cost - optimized_cost) / as_is_cost) * 100\n    print(f\"NET FINANCIAL SAVINGS:        {pct_savings:.1f}%\")\n    return as_is_cost, optimized_cost, pct_savings\n\nif __name__ == '__main__':\n    calculate_rightsized_cost('onprem_inventory.json')\n```",
                    "#### Stage 4: Running Utilization-Based Sizing & TCO Comparison\nExecute the rightsizing optimization calculator to determine portfolio savings:\n\n```sh\npython3 rightsizing_optimizer.py\n```",
                    "#### Stage 5: Evaluating Committed Use Discount (CUD) Multipliers\nVerify that the calculator correctly asserts over 60% savings across the sample portfolio:\n\n```python\n# test_tco_assertions.py\nfrom rightsizing_optimizer import calculate_rightsized_cost\n\nas_is, opt, pct = calculate_rightsized_cost('onprem_inventory.json')\nassert pct > 60.0, f\"Expected >60% savings, got {pct:.1f}%\"\nprint(f\"[PASS] Rightsizing optimization verified: {pct:.1f}% reduction achieved.\")\n```",
                    "#### Stage 6: Chaos Injection (Simulating Sudden p99 Compute Spike)\nSimulate what happens if an under-sized VM encounters a sudden 5x traffic surge. Verify that the 25% safety headroom prevents saturation:\n\n```sh\npython3 -c \"\nbase_load = 0.08\nsurge_load = base_load * 5 # 40% CPU\nallocated_capacity = 0.50 # e2-standard-4 capacity equivalent\nassert surge_load < allocated_capacity\nprint('Safety Headroom Test Passed: 25% buffer absorbed 5x traffic surge without throttling.')\n\"\n```",
                    "#### Stage 7: Triage, Troubleshooting & Custom Machine Type Tuning\nDocument in <kbd>day-075-rightsizing-tco.md</kbd> when custom machine types (`e2-custom-6-20480`) should be preferred over standard shapes to prevent paying for unused RAM.",
                    "#### Stage 8: Operational Teardown & FinOps Invariant Checklist\nVerify that the rightsizing runbook enforces monthly Active Assist audits. Confirm that no chargeable cloud resources were provisioned during the offline architectural simulation."
                ],
                "verification": (
                    "Run automated rightsizing test suite:\n\n```sh\npython3 rightsizing_optimizer.py && python3 -c \"import test_tco_assertions\"\n```\n\nConfirm output displays `NET FINANCIAL SAVINGS:` greater than 60% and all unit assertions pass."
                ),
                "trouble": (
                    "If savings are below 50%, verify that CUD discount factor and E2 unit pricing are correctly applied."
                ),
                "cleanup": "No remote cloud resources created; retain inventory files and calculator scripts in local repository.",
                "accept": "A validated rightsizing methodology document, an executable Python TCO calculator, and verified rightsizing output."
            }
        },
        {
            "key": "topic-04",
            "title": "Google Cloud VMware Engine (GCVE): Architecture, HCX Networking, and Trade-offs",
            "overview": (
                "Design Google Cloud VMware Engine (GCVE) private clouds. Architect bare-metal ESXi clusters, vSAN storage "
                "capacity physics, VMware HCX Layer 2 network extensions, and total cost of ownership (TCO) trade-offs."
            ),
            "preview": (
                "An enterprise deploys GCVE to meet a 30-day datacenter exit, but fails to model vSAN FTT-1 storage mirroring and slack space; "
                "the datastore hits 84% capacity on day 3, triggering emergency node additions costing $9,000/month."
            ),
            "technical": (
                "#### 1. Google Cloud VMware Engine (GCVE) Architecture\n\n"
                "Google Cloud VMware Engine provides a fully managed, hardware-isolated VMware Software-Defined Datacenter (SDDC) running directly "
                "on Google Cloud's bare-metal infrastructure:\n\n"
                "- **Dedicated Bare-Metal Nodes:** Nodes (e.g. `ve1-standard-72`) feature 72 hyperthreaded vCPUs, 768 GB RAM, and local NVMe storage, "
                "with zero hypervisor virtualization layer beneath ESXi (no nested virtualization).\n"
                "- **Software Stack:** Fully licensed VMware vSphere, vCenter Server, vSAN Enterprise, NSX-T Software-Defined Networking, and VMware HCX.\n"
                "- **VPC Interconnect:** GCVE connects directly to the customer's Google Cloud VPC via an ultra-low-latency (< 2ms) private peering link, "
                "allowing VMware virtual machines to access Cloud SQL, BigQuery, and Google Cloud APIs at line-rate line speeds without egress transit fees.\n\n"
                "#### 2. Hybrid Migration Fabric: VMware HCX and Layer 2 Network Extension\n\n"
                "VMware **HCX (Hybrid Cloud Extension)** provides the transport layer that enables seamless workload migration from on-premises vSphere:\n\n"
                "- **Layer 2 Network Extension:** HCX establishes an encrypted IPsec or Direct Connect tunnel that extends on-premises VLAN subnets "
                "(e.g. `192.168.20.0/24`) directly into GCVE NSX-T overlay segments.\n"
                "- **Zero IP Changes:** Virtual machines migrate from on-premises ESXi hosts to GCVE without changing their IP addresses, MAC addresses, "
                "or DNS records.\n"
                "- **Live vMotion & Warm Replication:** HCX supports live vMotion across the hybrid link with zero application downtime, as well as "
                "bulk replication (asynchronously syncing disk blocks and scheduling cutover during off-peak hours).\n\n"
                "#### 3. vSAN Storage Thermodynamics: FTT and Slack Space Physics\n\n"
                "The most critical architectural pitfall in GCVE design is failing to understand **vSAN storage physics**:\n\n"
                "- **Failures to Tolerate (FTT):** vSAN distributes data across bare-metal nodes. Under `FTT=1 (RAID-1 Mirroring)`, every gigabyte of "
                "provisioned VMDK requires **2.0 GB of raw physical NVMe storage**. Under `FTT=1 (RAID-5 Erasure Coding)` (requires 4+ nodes), "
                "storage overhead is reduced to 1.33 GB per 1 GB of data.\n"
                "- **Mandatory Slack Space:** vSAN requires a minimum of **20% to 25% unallocated slack space** to perform internal object rebalancing, "
                "garbage collection, snapshot consolidation, and host rebuild operations if a physical node fails.\n"
                "- **Effective Usable Capacity Formula:**\n\n"
                "$$\\text{Usable Storage} = \\frac{\\text{Raw NVMe Storage} \\times (1 - \\text{Slack Fraction})}{\\text{FTT Overhead Multiplier}}$$\n\n"
                "In a 3-node cluster with 57.6 TB raw NVMe storage and FTT=1 (Mirroring), usable capacity is only $\\frac{57.6 \\times 0.75}{2.0} = 21.6\\text{ TB}$. "
                "Attempting to write 30 TB of virtual machines will violently exhaust the cluster.\n\n"
                "#### 4. Architectural Trade-offs: GCVE vs. Native Compute Engine\n\n"
                "| Dimension | Google Cloud VMware Engine (GCVE) | Native Google Compute Engine (GCE) |\n"
                "|---|---|---|\n"
                "| **Minimum Infrastructure Commitment** | 3 Dedicated Bare-Metal Nodes (~$13,500/mo) | 1 Virtual Machine ($15/mo) |\n"
                "| **Migration Speed & Friction** | Highest (Live vMotion; zero IP/VM changes) | Moderate (Requires block conversion via m4vm) |\n"
                "| **Operational Model** | Identical to on-premises vCenter / vSphere tooling | Google Cloud native (Cloud Console, gcloud, APIs) |\n"
                "| **Storage Elasticity** | Coarse-grained (Must add 72-vCPU node to get storage) | Highly granular (Expand Persistent Disk by 1 GB online) |\n"
                "| **Cloud-Native Integration** | High (Sub-2ms VPC peering to BigQuery/Cloud SQL) | Native (Internal SDN fabric) |\n"
            ),
            "questions": [
                "How does VMware HCX Layer 2 network extension eliminate IP re-addressing during cloud migrations?",
                "What is the mathematical impact of vSAN FTT=1 RAID-1 mirroring on effective usable storage capacity?",
                "Why must a GCVE cluster maintain a minimum of 20–25% vSAN slack space at all times?",
                "Under what enterprise constraints is GCVE a superior architectural choice to native Compute Engine?",
            ],
            "reference": "https://docs.cloud.google.com/vmware-engine/docs/overview",
            "reference_label": "Google Cloud VMware Engine Documentation: Architecture and private cloud guide",
            "scenario": {
                "scenario": (
                    "To execute an urgent 30-day datacenter evacuation, Brightloaf procured a baseline 3-node Google Cloud VMware Engine (GCVE) "
                    "cluster using `ve1-standard-72` nodes (57.6 TB raw NVMe storage total). The infrastructure manager calculated that their "
                    "280 on-premises VMs occupied 28 TB of raw disk space in vCenter, concluding that 28 TB would fit comfortably inside the "
                    "57.6 TB cluster with plenty of room to spare. On Day 3 of bulk HCX migration, with 190 VMs migrated, the vCenter web client "
                    "flashed severe red alerts: the vSAN datastore reached 84.6% capacity. vSAN deduplication and compression background tasks "
                    "pegged cluster CPU, I/O latency spiked to 350ms, and automated host alerts triggered an emergency addition of two extra "
                    "`ve1-standard-72` bare-metal nodes, inflating monthly cloud spend by an unplanned $9,000/month."
                ),
                "impact": (
                    "P1 storage capacity emergency and budget shock. vSAN I/O throttling degraded performance across 190 migrated virtual machines. "
                    "Unbudgeted infrastructure expense of $9,000/month ($108,000 annualized). Migration waves were frozen for 5 days while "
                    "architects reassessed storage physics."
                ),
                "constraints": (
                    "Maintain vSAN datastore utilization strictly below 75%; optimize storage policies across the VM estate; avoid adding "
                    "unnecessary bare-metal compute nodes purely to satisfy raw storage demand."
                ),
                "evidence": (
                    "vCenter vSAN datastore capacity alarm and ESXi host kernel error logs:\n\n"
                    "```text\n"
                    "ALERT [vsan-cluster-01] [Event ID: 94812] - vSAN Datastore Disk Space Exhaustion Warning\n"
                    "Total Physical Capacity:   57.60 TB\n"
                    "Used Physical Space:       48.72 TB (84.58% Utilization - CRITICAL THRESHOLD EXCEEDED)\n"
                    "Free Physical Space:        8.88 TB\n"
                    "Mandatory Slack Space Req: 14.40 TB (25.00% Required for Resynchronization / Rebuild)\n"
                    "SLACK SPACE DEFICIT: -5.52 TB - vSAN Object Resynchronization Throttled!\n"
                    "\n"
                    "2026-09-28T09:14:22.184Z esx-node-01.gcve.internal vmkernel: [Storage][vSAN] WARNING: \n"
                    "    Storage policy 'vSAN Default Storage Policy' (FTT=1, Mirroring) enforced on 190 VMDKs. \n"
                    "    Capacity multiplier is 2.0x. Actual logical footprint: 24.36 TB * 2.0 = 48.72 TB physical consumed.\n"
                    "```"
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect vCenter vSAN Capacity Overview; identify that 190 migrated VMs were assigned the default storage policy `FTT=1 (RAID-1 Mirroring)`, doubling physical disk consumption to 48.72 TB.",
                    "Step 2: Review vSAN slack space requirements; confirm that vSAN requires 25% (14.4 TB) of unallocated capacity for object rebalancing and host rebuild operations, leaving usable capacity deeply negative.",
                    "Step 3: Analyze VM storage contents; discover 8.5 TB of historical database log backups and uncompressed tarballs sitting on high-performance vSAN NVMe datastores.",
                    "Step 4: Audit cluster node count; confirm a 3-node cluster cannot enable RAID-5 Erasure Coding (which requires a minimum of 4 nodes)."
                ],
                "root": (
                    "Architectural failure to model vSAN storage physics. The sizing team evaluated raw VMDK size without accounting for the "
                    "2.0x multiplier of FTT=1 RAID-1 mirroring and the mandatory 25% slack space reservation, leading to datastore exhaustion."
                ),
                "remediation_steps": [
                    "Step 1: Expand the cluster to 4 nodes (adding 1 node instead of 2), enabling the transition from RAID-1 Mirroring (2.0x) to RAID-5 Erasure Coding (1.33x multiplier).",
                    "Step 2: Reconfigure the vSAN Default Storage Policy to `FTT=1 (RAID-5 Erasure Coding)` across all non-critical workloads, recovering 16.2 TB of physical NVMe storage.",
                    "Step 3: Offload 8.5 TB of cold database backups and archive tarballs from high-performance vSAN to Google Cloud Storage buckets via Cloud Storage FUSE.",
                    "Step 4: Establish automated Cloud Monitoring alerts triggering at 70% vSAN datastore utilization to prevent cluster throttling."
                ],
                "verify": (
                    "Apply RAID-5 storage policy across migrated VMDKs. Confirm in vCenter that physical used storage drops from 48.72 TB to "
                    "32.4 TB (56.2% capacity utilization), restoring the 25% slack space buffer and eliminating I/O latency spikes."
                ),
                "residual": (
                    "RAID-5 erasure coding incurs a slight write amplification penalty compared to RAID-1 mirroring; high-transaction "
                    "database log volumes (WAL) should retain dedicated RAID-1 mirrored storage policies."
                ),
                "diagram": (
                    "Deploy 3-node GCVE sized on raw VMDKs",
                    "FTT-1 Mirror (2x) + 25% slack exhausts vSAN",
                    "Datastore hits 84.6%; emergency nodes added ($9k/mo)",
                    "Scale to 4 nodes; convert to RAID-5 (1.33x) + GCS tiering",
                    "Datastore drops to 56%; slack restored; costs saved"
                ),
                "facts": "3-node GCVE deployed; raw VMDKs filled 48.7 TB under FTT=1; vSAN hit 84.6% (slack deficit); $9k/mo node expansion triggered.",
                "inference": "vSAN storage physics (FTT multipliers and 25% slack) dictate usable capacity; RAID-5 requires 4 nodes but saves 33% storage.",
                "expected": "4-node cluster with RAID-5 erasure coding reduces footprint to 56% capacity, maintaining healthy slack space."
            },
            "lab": {
                "name": "Google Cloud VMware Engine (GCVE) Cluster Sizing & vSAN Physics Calculator",
                "file": "day-075-gcve-sizing.md",
                "goal": "Author a comprehensive GCVE cluster sizing runbook and build an executable Python vSAN storage physics calculator.",
                "expected": "A complete GCVE architectural sizing document, an executable Python vSAN calculator, and verified node sizing output.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 74 regional boundaries and Day 71 performance sizing",
                "preflight": "Review Google Cloud VMware Engine node specifications and VMware vSAN design guides.",
                "steps": [
                    "#### Stage 1: Pre-Flight SDDC Scope & Performance Invariants\nDraft the GCVE private cloud requirements in <kbd>day-075-gcve-sizing.md</kbd>. Define CPU overcommit ratios (typically 3:1 for general workloads), RAM reservation (100% committed), and vSAN slack space policies (25% reserved).",
                    "#### Stage 2: Defining Bare-Metal Node Specifications\nDocument the physical hardware specifications of the `ve1-standard-72` node architecture (<kbd>gcve_node_specs.json</kbd>):\n\n```json\n{\n  \"node_type\": \"ve1-standard-72\",\n  \"physical_cpu_cores\": 72,\n  \"hyperthreads\": 144,\n  \"ram_gb\": 768,\n  \"raw_nvme_storage_tb\": 19.2,\n  \"cluster_minimum_nodes\": 3,\n  \"cluster_maximum_nodes\": 16\n}\n```",
                    "#### Stage 3: Developing the vSAN Storage Physics & FTT Sizing Calculator in Python\nImplement the vSAN storage thermodynamics calculator (<kbd>gcve_vsan_calculator.py</kbd>):\n\n```python\n# gcve_vsan_calculator.py\n\"\"\"Calculates usable vSAN storage and minimum GCVE node requirements.\"\"\"\nimport math\n\ndef calculate_gcve_cluster(total_vm_storage_tb: float, num_nodes: int, ftt_policy: str = 'RAID1'):\n    node_raw_storage = 19.2  # TB raw NVMe per ve1 node\n    total_raw_storage = num_nodes * node_raw_storage\n    \n    # Storage multipliers\n    multiplier = 2.0 if ftt_policy == 'RAID1' else 1.333  # RAID5 requires 4+ nodes\n    slack_factor = 0.25  # 25% slack space reserved for rebuilds\n    \n    physical_needed = total_vm_storage_tb * multiplier\n    max_safe_physical = total_raw_storage * (1.0 - slack_factor)\n    \n    is_safe = physical_needed <= max_safe_physical\n    utilization_pct = (physical_needed / total_raw_storage) * 100\n    \n    print(f\"CLUSTER SIZING: {num_nodes} Nodes | Policy: {ftt_policy}\")\n    print(f\"Total Raw Storage:       {total_raw_storage:.2f} TB\")\n    print(f\"Physical Space Needed:   {physical_needed:.2f} TB (Multiplier: {multiplier}x)\")\n    print(f\"Max Safe Usable Space:   {max_safe_physical:.2f} TB (75% Limit)\")\n    print(f\"Datastore Utilization:   {utilization_pct:.1f}%\")\n    print(f\"Safe Operational Status: {'HEALTHY [OK]' if is_safe else 'CAPACITY VIOLATION [CRITICAL]'}\")\n    print(\"-\" * 55)\n    return is_safe, utilization_pct\n\nif __name__ == '__main__':\n    # Test 1: 3 Nodes with 28 TB VMDKs on RAID-1 Mirroring (Flawed initial sizing)\n    calculate_gcve_cluster(total_vm_storage_tb=28.0, num_nodes=3, ftt_policy='RAID1')\n    # Test 2: 4 Nodes with 28 TB VMDKs on RAID-5 Erasure Coding (Remediated sizing)\n    calculate_gcve_cluster(total_vm_storage_tb=28.0, num_nodes=4, ftt_policy='RAID5')\n```",
                    "#### Stage 4: Executing Cluster Node Sizing for Enterprise VM Fleet\nRun the vSAN storage physics calculator to observe the capacity violation on 3 nodes and resolution on 4 nodes:\n\n```sh\npython3 gcve_vsan_calculator.py\n```",
                    "#### Stage 5: Simulating Storage Capacity Watermark & RAID-5 Policy Transition\nDevelop automated unit tests (<kbd>test_gcve_physics.py</kbd>) verifying that RAID-1 is rejected and RAID-5 is accepted:\n\n```python\n# test_gcve_physics.py\nfrom gcve_vsan_calculator import calculate_gcve_cluster\n\n# 3 nodes with RAID1 must fail\nis_safe_3, util_3 = calculate_gcve_cluster(28.0, 3, 'RAID1')\nassert is_safe_3 is False\nassert util_3 > 80.0\n\n# 4 nodes with RAID5 must succeed\nis_safe_4, util_4 = calculate_gcve_cluster(28.0, 4, 'RAID5')\nassert is_safe_4 is True\nassert util_4 < 60.0\nprint(\"[PASS] vSAN Storage Physics verified: 4 nodes with RAID-5 restores healthy capacity.\")\n```",
                    "#### Stage 6: Chaos Injection (Simulating Host Hardware Failure & vSAN Rebuild Slack Exhaustion)\nSimulate what happens if 1 node dies in a 3-node cluster that has insufficient slack space:\n\n```sh\npython3 -c \"\nraw_3 = 3 * 19.2\nraw_surviving = 2 * 19.2 # 1 node dead\nused_data = 48.7 # TB\nassert used_data > raw_surviving\nprint('Host Failure Chaos: 2 surviving nodes have 38.4 TB raw space; cannot hold 48.7 TB data!')\nprint('PROVEN: Without 25% slack, a single node hardware glitch causes permanent data unrecoverability!')\n\"\n```",
                    "#### Stage 7: Triage, Troubleshooting & HCX L2 Network Extension Runbook\nDocument the VMware HCX Layer 2 network extension runbook in <kbd>day-075-gcve-sizing.md</kbd>. Specify gateway IP cutover procedures when migrating the default gateway from on-premises core switches to GCVE NSX-T Tier-1 routers.",
                    "#### Stage 8: Operational Teardown & Dedicated Cloud Invariant Checklist\nVerify that all GCVE architectural blueprints enforce a minimum 4-node deployment when RAID-5 erasure coding is selected. Confirm that no chargeable cloud resources were provisioned during the offline architectural simulation."
                ],
                "verification": (
                    "Run automated GCVE sizing verification test suite:\n\n```sh\npython3 gcve_vsan_calculator.py && python3 test_gcve_physics.py\n```\n\nConfirm output displays `Safe Operational Status: HEALTHY [OK]` for 4 nodes with RAID-5 and all unit assertions pass."
                ),
                "trouble": (
                    "If RAID-5 is selected with fewer than 4 nodes in simulation, verify that node count validation enforces the vSAN minimum requirement."
                ),
                "cleanup": "No remote cloud resources created; retain sizing calculations and runbooks in local repository.",
                "accept": "A validated GCVE architectural sizing document, an executable Python vSAN calculator, and verified node sizing output."
            }
        }
    ]
}
