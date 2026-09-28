"""day_data_087.py — Exhaustive architecture data specification for Day 87.

Covers Incidents, Blameless Post-Mortems, and Capacity Planning:
1. Incident management (severity levels P1-P4, Incident Commander ICS roles, escalation paths).
2. Blameless post-mortems (Five Whys, timeline reconstruction, systemic guardrails, SMART action items).
3. Capacity planning and load forecasting (N+1 regional redundancy, Google Cloud quota headroom, seasonal peak modeling).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 87

DATA = {
    "day": 87,
    "part1_intro": (
        "Day 87 masters the operational human and organizational protocols that preserve cloud resilience: structured incident management, "
        "blameless post-mortems, and predictive capacity planning. Technology fails inevitably; the differentiator of high-performing "
        "engineering organizations is the speed, coordination, and psychological safety with which teams respond to outages and extract "
        "systemic learnings. Following the battle-tested Incident Command System (ICS), architects learn to separate command leadership "
        "from technical execution, triage severity levels from P1 to P4, and shield responders from executive interruption. Furthermore, "
        "today's curriculum establishes blameless post-mortem culture—treating human error not as a root cause, but as a symptom of inadequate "
        "systemic guardrails—and formulates rigorous capacity planning models that manage Google Cloud quota ceilings and N+1 redundancy."
    ),
    "exit_summary": (
        "Constructed an enterprise Incident Response Playbook defining ICS roles (Incident Commander, Operations Lead, Communications Lead) "
        "and severity escalation matrices; completed a comprehensive blameless post-mortem analysis with second-by-second timeline "
        "reconstruction and Five Whys causal analysis for a simulated regional database failover incident; authored five SMART preventive "
        "action items; implemented an automated Python capacity planning calculator modeling seasonal load surges and GCP quota headroom."
    ),
    "part2_intro": (
        "Operational resilience transforms chaotic firefighting into a disciplined, repeatable engineering workflow. The sections "
        "below detail ICS role boundaries, severity triage thresholds, post-mortem authoring rubrics, and capacity forecasting mathematics."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Severity Tier</th>
      <th>Business &amp; User Impact Criteria</th>
      <th>Response Target (MTTA)</th>
      <th>Command Cadence &amp; Escalation</th>
      <th>External Communication Policy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>P1 — Critical</strong></td>
      <td>Core revenue path down (e.g. 100% checkout failure); data loss risk; active security breach.</td>
      <td><strong>&lt; 5 minutes</strong> (Immediate 24/7 page)</td>
      <td>Incident Commander dedicated; war room established; VP Eng notified immediately.</td>
      <td>Public status page updated every 15 minutes; executive briefings every 30 minutes.</td>
    </tr>
    <tr>
      <td><strong>P2 — Major</strong></td>
      <td>Significant service degradation (>10% users affected); core feature impaired without workaround.</td>
      <td><strong>&lt; 15 minutes</strong> (Primary + Secondary page)</td>
      <td>Operations Lead directs triage; technical bridge formed; on-call manager engaged.</td>
      <td>Status page updated every 30 minutes; internal stakeholder email sent hourly.</td>
    </tr>
    <tr>
      <td><strong>P3 — Moderate</strong></td>
      <td>Non-critical feature down (e.g. search recommendations); workaround exists; minimal user disruption.</td>
      <td><strong>&lt; 1 hour</strong> (Business hours / on-call ticket)</td>
      <td>On-call engineer investigates during working shift; escalates if blast radius grows.</td>
      <td>No public status update; daily operational summary report.</td>
    </tr>
    <tr>
      <td><strong>P4 — Minor</strong></td>
      <td>Cosmetic UI bug; internal reporting delay; non-impacting telemetry failure.</td>
      <td><strong>&lt; 24 hours</strong> (Next business day)</td>
      <td>Standard engineering backlog grooming; regular sprint ticket triage.</td>
      <td>Internal release notes only.</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 87: Incident Command Lifecycle and Post-Mortem Feedback Loop",
        "desc": "Lifecycle tracing detection through ICS role delegation, mitigation, and blameless post-mortem action item delivery.",
        "caption": "Figure 87.1: Incident management lifecycle showing clear separation between command, operations, and communications.",
        "nodes": [
            ("1. Multi-Burn Alert", "Monitoring Triggers P1 Page\\nMTTA < 5min"),
            ("2. Incident Command", "Appoint IC, Ops, & Comms\\nIsolate Responders from Execs"),
            ("3. Mitigation & Drain", "Prioritize Recovery over Root\\nTraffic Shift / Rollback"),
            ("4. Blameless Post-Mortem", "Five Whys + Timeline Audit\\nSMART Engineering Fixes"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Incident management: severity levels, on-call, and incident command",
            "preview": (
                "During a major payment outage, twenty senior executives join the Slack triage channel demanding instant updates, "
                "distracting the lead database engineer so severely that she accidentally enters a command that deletes the primary database table."
            ),
            "overview": (
                "Modern incident response is modeled after the industrial Incident Command System (ICS), designed to coordinate high-stress, "
                "time-critical emergencies without organizational chaos. The golden rule of incident response is the strict separation of roles: "
                "the **Incident Commander (IC)** owns overall decision authority, assigns investigation streams, and maintains situational awareness, "
                "but *never* touches a terminal or debugs code directly. The **Operations Lead** directs technical troubleshooting and executes runbooks. "
                "The **Communications Lead** handles all stakeholder and customer communication, actively shielding the technical team from executive "
                "distraction. Clearly codified severity tiers (P1 to P4) dictate response timeframes, alerting channels, and escalation paths, "
                "ensuring that high-impact outages receive immediate, structured focus without panic."
            ),
            "technical": (
                "Incident operations must strictly adhere to documented organizational protocols:\n\n"
                "### 1. Incident Command System (ICS) Core Roles\n"
                "- **Incident Commander (IC):** Holds absolute operational authority during the incident. Assesses severity, appoints leads, approves "
                "high-risk mitigations (such as regional traffic drains or database restarts), and maintains a calm, disciplined cadence.\n"
                "- **Operations Lead (Ops Lead):** Directs the technical responders. Formulates diagnostic hypotheses, reviews telemetry, and assigns "
                "specific investigation tasks to domain experts (networking, database, compute).\n"
                "- **Communications Lead (Comms Lead):** The sole liaison to executive leadership, customer support, and public status pages. "
                "Updates the public status page at fixed intervals (e.g. every 15 minutes for P1) and prevents external stakeholders from entering the technical war room.\n\n"
                "### 2. The Mitigation-First Imperative\n"
                "In enterprise SRE, **mitigation always precedes root cause analysis**. The sole objective during an active incident is restoring "
                "user-facing availability as rapidly as possible (e.g., rolling back a release, draining traffic to a secondary region, toggling a feature flag, "
                "or restarting an autoscaling group). Diagnosing *why* the bug occurred must be deferred until after user service is restored.\n\n"
                "### 3. Formal Shift Handoff Protocol\n"
                "For incidents spanning multiple hours, responders suffer cognitive fatigue. Handoffs must be conducted synchronously using a formal "
                "written summary: current operational state, proven facts, ruled-out hypotheses, active mitigation streams, and explicit verbal transfer of IC authority."
            ),
            "questions": [
                "Why must the Incident Commander refrain from typing debugging commands or inspecting logs directly during a P1 incident?",
                "What is the specific role of the Communications Lead in protecting technical responders from executive interference?",
                "Why must teams prioritize rapid mitigation (e.g., traffic drain or rollback) over finding the underlying code defect?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/operational-excellence#manage-incidents",
            "reference_label": "Google Cloud Architecture Framework: Managing and escalating enterprise incidents",
            "scenario": {
                "symptom": (
                    "Brightloaf suffered a 75-minute outage of its checkout API. Early in the outage, the VP of Sales and Director of Support joined "
                    "the engineering incident bridge, repeatedly interrogating the database engineer about customer impact. Disoriented by the pressure, "
                    "the engineer applied a hotfix directly to production without testing, which doubled the volume of 500 errors."
                ),
                "constraints": (
                    "Must establish strict communication air gaps between executives and technical responders while maintaining 15-minute stakeholder updates."
                ),
                "evidence": (
                    "Incident voice bridge recording showed 42 minutes of discussion between executives and engineers debating revenue impact, "
                    "leaving the on-call engineer only 18 minutes to investigate database connection pool deadlocks."
                ),
                "diagnostic_steps": [
                    "Review incident bridge timeline and message logs to measure time spent answering non-technical executive questions.",
                    "Analyze the failed hotfix commit pushed during the incident to identify why standard review controls were bypassed.",
                    "Audit the absence of a designated Communications Lead in the historical incident logs.",
                ],
                "root": (
                    "Failure to implement Incident Command System (ICS) role separation: the absence of an Incident Commander and Communications Lead "
                    "allowed external stakeholders to directly distract and pressure technical responders, causing an error that worsened the outage."
                ),
                "fix": (
                    "Mandate ICS role assignment on all P1/P2 incidents: appoint a dedicated Communications Lead who hosts an executive broadcast channel, "
                    "and enforce a strict policy locking technical debugging bridges to authorized engineering responders only."
                ),
                "verify": (
                    "Execute a tabletop incident simulation with executive observers; verify responders operate without interruption and public status updates occur every 15 minutes."
                ),
                "residual": (
                    "Executives may initially feel excluded; requires leadership alignment meetings to explain that air-gapping responders accelerates MTTR."
                ),
                "diagram": (
                    "Execs enter eng channel",
                    "Database lead distracted",
                    "Unverified hotfix fails",
                    "Appoint Comms Lead air gap",
                    "MTTR reduced by 60%"
                ),
                "facts": "42 minutes of technical troubleshooting were lost to answering executive status inquiries on the primary bridge.",
                "inference": "Responders cannot conduct complex distributed systems triage while simultaneously managing executive anxiety.",
                "expected": "Communications Lead handles external messaging, allowing Operations Lead to execute technical recovery unhindered."
            },
            "lab": {
                "name": "Incident Command Playbook and Severity Triage Matrix",
                "file": "day-087-topic-01-ics-playbook.md",
                "goal": "Author an enterprise Incident Response Playbook specifying ICS roles, paging triggers, and communication cadences.",
                "expected": "A structured Markdown playbook covering P1-P4 triage rules, war room protocols, and executive communication templates.",
                "mode": "tabletop analysis & process synthesis",
                "prereq": "Review Day 86 golden signals and error budget artifacts.",
                "preflight": "Initialize incident playbook template in workspace.",
                "steps": [
                    "Author the Incident Command Playbook:\n\n```sh\ncat <<'EOF' > day-087-topic-01-ics-playbook.md\n# Day 87: Enterprise Incident Management & ICS Playbook\n\n## 1. Incident Command System (ICS) Roles\n\n- **Incident Commander (IC):**\n  - Declares incident severity and leads the response.\n  - Assigns investigation tasks; maintains high-level situational awareness.\n  - Authorizes high-risk mitigations (traffic drain, service shutdown, DB failover).\n  - Does NOT perform technical debugging.\n\n- **Operations Lead (Ops Lead):**\n  - Directs technical responders (Database, Network, Compute).\n  - Coordinates hypothesis testing and executes runbooks.\n\n- **Communications Lead (Comms Lead):**\n  - Sole owner of external status page and internal executive briefings.\n  - Publishes updates every 15 minutes for P1, 30 minutes for P2.\n  - Strictly bars non-technical observers from the technical war room.\n\n## 2. Severity Escalation Matrix\n\n| Severity | Business Impact | MTTA Target | Alerting Channel | Status Update Cadence |\n| :--- | :--- | :--- | :--- | :--- |\n| **P1** | Core revenue path down (Checkout 0%) | < 5 mins | PagerDuty 24/7 (Multi-burn alert) | Every 15 minutes |\n| **P2** | Major service degraded (>10% users) | < 15 mins | PagerDuty On-Call Lead | Every 30 minutes |\n| **P3** | Non-critical feature broken | < 1 hour | Slack #on-call-triage | Daily summary |\n| **P4** | Minor cosmetic defect / telemetry bug | < 24 hours | Jira Backlog Ticket | Sprint grooming |\n\n## 3. Standard P1 Status Update Template\n```markdown\n### Incident Status Update [P1] — Brightloaf Order Checkout\n**Status:** INVESTIGATING | MITIGATING | RESOLVED\n**Impact:** Approximately 15% of checkout requests in us-central1 are receiving HTTP 504 timeouts.\n**Current Action:** Operations team has shifted 100% of ingress traffic to us-east1 via Global Load Balancer.\n**Next Update:** In 15 minutes (14:30 UTC).\n```\nEOF\ncat day-087-topic-01-ics-playbook.md\n```",
                    "Verify that the playbook establishes clear authority boundaries and explicit communications cadences.",
                    "Save the playbook in your artifact repository."
                ],
                "verification": (
                    "Playbook exists, defines all three primary ICS roles, and includes a complete severity escalation matrix with status update templates."
                ),
                "trouble": "Ensure P1 communication templates omit speculative root causes and focus strictly on observed impact and mitigation steps.",
                "cleanup": "Retain `day-087-topic-01-ics-playbook.md` as an exit evidence artifact.",
                "accept": "Completed enterprise incident response playbook with verified role boundaries and communication governance."
            }
        },
        {
            "key": "topic-02",
            "title": "Blameless post-mortems and systemic action item tracking",
            "preview": (
                "After an outage, leadership fires the junior engineer who ran a bad database query. "
                "Three weeks later, terrified of being blamed, another engineer conceals a production bug for four days until it causes a catastrophic customer data loss."
            ),
            "overview": (
                "The core premise of modern Site Reliability Engineering is that **post-mortems must be blameless**. "
                "Humans are inherently fallible; if an engineer can take down production with a single command or misconfigured configuration, "
                "the fundamental fault lies in the architecture, automated guardrails, and access policies—not the individual. "
                "Punishing individuals creates a culture of fear where failures are concealed, near-misses are ignored, and systemic bugs fester. "
                "A blameless post-mortem assumes that every participant acted in good faith with the information they had at the time. "
                "By analyzing the incident through **The Five Whys** and timeline reconstruction, the organization uncovers systemic root causes "
                "and produces actionable, preventive engineering fixes (SMART Action Items) that permanently eliminate entire classes of failure."
            ),
            "technical": (
                "Authoring an authoritative post-mortem requires strict adherence to standardized SRE rubrics:\n\n"
                "### 1. Second-by-Second Timeline Reconstruction\n"
                "The foundation of every post-mortem is an objective, high-precision timeline compiled from machine logs, metrics, and chat transcripts:\n"
                "- $t_0$ (Fault Injected): Exact timestamp the error was introduced (e.g. `2026-09-28T14:02:11Z` commit merged).\n"
                "- $t_1$ (User Impact Starts): First observable spike in SLI degradation.\n"
                "- $t_2$ (Detection / Alert): Monitoring alert fires and on-call engineer paged.\n"
                "- $t_3$ (Incident Declared): Incident Commander assumes control; war room opened.\n"
                "- $t_4$ (Mitigation Applied): Action taken that restores user service (e.g. traffic drained).\n"
                "- $t_5$ (Resolution): Systems fully operational, data reconciled, and incident closed.\n\n"
                "### 2. The Five Whys: Distinguishing Proximate Trigger from Systemic Cause\n"
                "Never stop at the human trigger:\n"
                "- *Why did checkout fail?* The database ran out of disk space.\n"
                "- *Why did it run out of space?* A rogue query generated a massive 500GB temporary table.\n"
                "- *Why did the query run?* An unindexed analytics query was run directly against the production primary.\n"
                "- *Why was it run against the primary?* Analytics credentials had read/write permissions to production instead of read-only replica.\n"
                "- *Why did they have production access?* IAM roles were assigned manually without least-privilege automation. (Systemic Cause!)\n\n"
                "### 3. SMART Action Items\n"
                "Action items must be **Specific, Measurable, Achievable, Relevant, and Time-bound** (e.g., 'Deploy automated disk auto-resize in Terraform by Oct 15; Owner: Jane D.'). "
                "Categorize fixes into: **Prevent** (architectural safeguards), **Mitigate** (faster failover), and **Detect** (earlier alerting)."
            ),
            "questions": [
                "Why does blaming an individual for an outage increase organizational risk rather than decreasing it?",
                "How does 'The Five Whys' technique uncover systemic architectural flaws beneath human operational errors?",
                "What are the mandatory attributes of a SMART action item in an SRE post-mortem?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/operational-excellence#post-mortems",
            "reference_label": "Google Cloud Architecture Framework: Conducting blameless post-mortems",
            "scenario": {
                "symptom": (
                    "During a scheduled maintenance window, an administrator accidentally ran a Terraform script against the production project "
                    "instead of staging, destroying the production VPC network and taking down all services for 4 hours."
                ),
                "constraints": (
                    "Must establish technical safeguards that prevent cross-environment Terraform destruction without slowing down routine deployment pipelines."
                ),
                "evidence": (
                    "Shell history showed the administrator had active Google Cloud credentials with `roles/owner` across both staging and production projects "
                    "in a single terminal session, with state files stored in improperly partitioned buckets."
                ),
                "diagnostic_steps": [
                    "Reconstruct the command execution timeline from Google Cloud Audit Logs (`cloudaudit.googleapis.com/activity`).",
                    "Audit Terraform state bucket permissions and workspace configuration.",
                    "Conduct a Five Whys analysis to determine why the CLI command lacked production environment fencing.",
                ],
                "root": (
                    "Systemic lack of environment isolation: production and staging infrastructure shared administrative credential sessions, "
                    "lacked automated Terraform `-target` plan reviews, and possessed no `prevent_destroy` lifecycle rules on core VPC resources."
                ),
                "fix": (
                    "Enforce strict organizational boundaries: isolate production and staging into separate GCP folders, require separate Service Account "
                    "impersonation with short-lived tokens, enforce `lifecycle { prevent_destroy = true }` in Terraform on all network resources, "
                    "and mandate automated CI/CD execution via Cloud Build with pull request approval gates."
                ),
                "verify": (
                    "Attempt a simulated `terraform destroy` against production in CI/CD; verify the pipeline blocks execution with a policy-as-code error."
                ),
                "residual": (
                    "Authorized resource decommissioning requires an explicit multi-step PR to remove the `prevent_destroy` block before destruction."
                ),
                "diagram": (
                    "Shared credentials active",
                    "Terraform applied to prod",
                    "Production VPC destroyed",
                    "Terrform prevent_destroy",
                    "Zero cross-env destruction"
                ),
                "facts": "Administrator destroyed production VPC because local shell held unhedged credentials for both environments.",
                "inference": "Human error is inevitable; systems that permit total destruction via single unvalidated commands are defective.",
                "expected": "Terraform policy-as-code and GCP project isolation prevent accidental destruction of critical foundation assets."
            },
            "lab": {
                "name": "Blameless Post-Mortem Authoring and Action Item Registry",
                "file": "day-087-topic-02-post-mortem.md",
                "goal": "Author a comprehensive, blameless post-mortem for a simulated production failure, complete with timeline and SMART action items.",
                "expected": "A production-grade Markdown post-mortem document adhering to Google SRE standards with Five Whys causal analysis.",
                "mode": "tabletop analysis & incident synthesis",
                "prereq": "Completion of Exercise 1.",
                "preflight": "Review post-mortem template in workspace.",
                "steps": [
                    "Author the blameless post-mortem document:\n\n```sh\ncat <<'EOF' > day-087-topic-02-post-mortem.md\n# Post-Mortem: Incident INC-20260928 — Order Processing Regional Latency Surge\n\n## 1. Executive Summary\nOn 2026-09-28 from 14:02 UTC to 14:38 UTC (36 minutes total), Brightloaf experienced a P1 degradation \nimpacting the B2B checkout API in `us-central1`. Approximately 18,200 orders received HTTP 504 timeouts. \nService was fully mitigated by draining ingress traffic to `us-east1` via Cloud Load Balancing.\n\n## 2. Incident Metadata\n- **Incident Commander:** Alex M. | **Operations Lead:** Sarah T. | **Communications Lead:** David K.\n- **Time to Detect (MTTD):** 2m 14s | **Time to Mitigate (MTTM):** 36m 12s | **Total Outage:** 36m 12s\n- **SLO Impact:** Consumed 18.4% of rolling 28-day error budget.\n\n## 3. High-Precision Timeline (UTC)\n- **14:02:10:** Downstream payment provider began throttling requests to 50 TPS.\n- **14:04:24:** Cloud Monitoring multi-window burn rate alert fired (Burn Rate = 18.2x). On-call paged.\n- **14:06:00:** Incident Commander declared P1; opened war room bridge.\n- **14:12:30:** Operations Lead identified database connection pool starvation on primary Cloud SQL.\n- **14:25:00:** IC approved regional traffic shift to `us-east1` secondary warm standby.\n- **14:38:22:** Traffic stabilized; p99 latency returned to 45ms; zero 504 errors observed.\n- **14:45:00:** Incident officially resolved; post-mortem initiated.\n\n## 4. Root Cause Analysis: The Five Whys\n1. *Why did orders fail?* Backend web servers ran out of available worker threads.\n2. *Why were threads exhausted?* Each thread was blocked waiting for synchronous payment responses.\n3. *Why did payments block?* Downstream provider experienced severe throttling and failed to return responses within 2s.\n4. *Why didn't the application time out earlier?* The HTTP client timeout was set to 60s instead of 2.5s.\n5. *Why was timeout set to 60s?* Legacy configuration carried over from batch processing without resilience review. (**Systemic Root Cause**)\n\n## 5. SMART Action Items\n\n| Item | Action Description | Category | Owner | Target Date | Verification |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n| **ACT-01** | Enforce 2,500ms timeout on payment client | Prevent | Sarah T. | 2026-10-05 | Chaos test in staging |\n| **ACT-02** | Implement Circuit Breaker in Envoy mesh | Mitigate | Alex M.  | 2026-10-12 | Synthetic fault injection |\n| **ACT-03** | Add connection pool saturation alert at 75%| Detect   | David K. | 2026-10-02 | Metric threshold alert |\n| **ACT-04** | Automate regional traffic drain runbook | Mitigate | Jane R.  | 2026-10-19 | GCLB automated script |\n| **ACT-05** | Audit all external API timeouts across codebase| Prevent| Team     | 2026-10-26 | Code review checklist |\nEOF\ncat day-087-topic-02-post-mortem.md\n```",
                    "Verify the post-mortem focuses entirely on systemic design flaws rather than assigning personal blame.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, includes second-by-second timeline, Five Whys analysis, and five SMART action items with assigned owners."
                ),
                "trouble": "Ensure every action item specifies a measurable verification check and a calendar completion target.",
                "cleanup": "Retain `day-087-topic-02-post-mortem.md` as an exit evidence artifact.",
                "accept": "Mastery of the blameless post-mortem process and actionable engineering remediation tracking."
            }
        },
        {
            "key": "topic-03",
            "title": "Capacity planning, load forecasting, and Google Cloud quota management",
            "preview": (
                "Brightloaf launches a major nationwide promotion expected to generate 5x normal traffic. "
                "Two minutes after launch, autoscaling abruptly stops because the project hit the default regional `CPUS_ALL_REGIONS` quota ceiling, dropping 60% of new customer checkouts."
            ),
            "overview": (
                "Capacity planning is the proactive engineering discipline of ensuring that cloud infrastructure possesses sufficient computing, storage, "
                "and network resources to satisfy anticipated user demand without violating SLOs or incurring wasteful over-provisioning costs. "
                "In Google Cloud, capacity is governed by hard physical and administrative boundaries: **quotas** (enforced ceilings on API requests and resources "
                "like vCPUs or public IPs) and **capacity limits** (physical server availability in specific zones). "
                "Architects must model organic growth alongside seasonal flash surges, enforce **N+1 regional redundancy** (guaranteeing sufficient headroom "
                "to absorb the loss of an entire availability zone), and audit GCP quota allocations at least 4 to 6 weeks prior to major commercial events."
            ),
            "technical": (
                "Capacity planning requires rigorous mathematical modeling and proactive quota governance:\n\n"
                "### 1. The N+1 Multi-Zone Headroom Rule\n"
                "If a system distributes load across $Z$ availability zones in a region, the loss of one zone increases the load on remaining zones to:\n"
                "$$\\text{Load per surviving zone} = \\frac{1}{Z - 1} \\times 100\\%$$\n"
                "- Across 3 zones ($Z=3$): losing 1 zone forces remaining 2 zones to absorb $50\\%$ of total load each (a **50% traffic surge per zone**).\n"
                "- SRE Mandate: Baseline steady-state utilization per zone must never exceed:\n"
                "$$\\text{Max Baseline Utilization} = \\frac{Z - 1}{Z} \\times 80\\%$$\n"
                "- For $Z=3$: $(2/3) \\times 80\\% = \\mathbf{53.3\\%}$. If a 3-zone cluster operates above 53.3% utilization, losing a single zone pushes surviving zones "
                "past the 80% saturation cliff, triggering immediate cascading failure!\n\n"
                "### 2. Google Cloud Quota Architecture\n"
                "- **Resource Quotas:** E.g., `compute.googleapis.com/cpus` (regional), `compute.googleapis.com/in_use_addresses` (regional static IPs), `cloudsql.googleapis.com/instances`.\n"
                "- **Rate Quotas:** API call rates (e.g. 1,000 `instances.insert` calls per 100 seconds).\n"
                "- Quotas prevent runaway billing and protect provider multitenant stability. Quota increases require human review and can take 2 to 5 business days.\n\n"
                "### 3. Proactive Load Forecasting Equations\n"
                "Calculate required vCPUs ($C_{\\text{req}}$) from forecast peak QPS ($Q$), single-core capacity ($Q_{\\text{core}}$), and target maximum utilization ($\\rho = 0.70$):\n"
                "$$C_{\\text{req}} = \\left\\lceil \\frac{Q}{Q_{\\text{core}} \\times \\rho} \\right\\rceil \\times \\frac{Z}{Z - 1}$$"
            ),
            "questions": [
                "Why must a 3-zone regional cluster maintain steady-state CPU utilization below 53.3% to survive the complete loss of one zone?",
                "What is the operational difference between a regional resource quota and a rate-limiting API quota in Google Cloud?",
                "Why must enterprise quota increases be requested weeks in advance of planned commercial marketing promotions?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/capacity-planning",
            "reference_label": "Google Cloud Architecture Framework: Sizing, forecasting, and quota management",
            "scenario": {
                "symptom": (
                    "During a Cyber Monday sale, Brightloaf's GKE cluster attempted to autoscale from 30 nodes to 75 nodes to handle an 8,000 QPS surge. "
                    "The GKE Cluster Autoscaler stalled at 48 nodes, emitting events: `Quota 'CPUS' exceeded in region us-central1`. "
                    "Incoming requests queued up and 45% of user checkouts failed."
                ),
                "constraints": (
                    "Must accommodate flash promotions up to 10,000 QPS while maintaining N+1 multi-zone resilience and staying within approved FinOps annual budgets."
                ),
                "evidence": (
                    "Google Cloud Quota console showed `compute.googleapis.com/cpus` ceiling in `us-central1` was set to the default of 400 vCPUs. "
                    "The 48 running `c2-standard-8` nodes consumed 384 vCPUs, leaving insufficient quota to schedule the remaining 27 requested nodes."
                ),
                "diagnostic_steps": [
                    "Query Cloud Logging for `resource.type=\"k8s_cluster\"` and filter by `scaleUp: failedQuota`.",
                    "Audit Google Cloud Quotas console across all target regions for Compute Engine CPUs and In-Use Public IP addresses.",
                    "Calculate peak vCPU demand using historical single-pod QPS benchmark metrics.",
                ],
                "root": (
                    "Capacity planning failed to audit regional GCP quotas prior to a planned 5x marketing promotion, allowing autoscaling to hit an "
                    "unmonitored administrative quota ceiling during peak traffic."
                ),
                "fix": (
                    "Establish a formal pre-event Capacity Checklist: submit quota increase requests for 1,200 vCPUs 4 weeks in advance, configure Cloud Monitoring "
                    "quota utilization alerts at 75%, and implement multi-region overflow routing via Global Load Balancer to spill excess load into `us-east1`."
                ),
                "verify": (
                    "Verify `gcloud compute regions describe us-central1` shows quota increased to 1,200 vCPUs; simulate synthetic node autoscale in staging to 80 nodes."
                ),
                "residual": (
                    "Unused idle quota costs nothing in GCP, but commitments (CUDs) require careful modeling to avoid paying for excess reserved headroom."
                ),
                "diagram": (
                    "8k QPS surge arrives",
                    "GCP 400 CPU quota hit",
                    "Autoscaling stalls (45% 5xx)",
                    "Pre-event quota increase",
                    "Clean 75-node autoscale"
                ),
                "facts": "Cluster autoscaler choked at 48 nodes because regional CPU quota was capped at 400 vCPUs.",
                "inference": "Autoscaling policies are completely useless if underlying cloud provider quotas are not proactively sized.",
                "expected": "Pre-provisioned quota headroom allows cluster to autoscale seamlessly up to planned peak capacity."
            },
            "lab": {
                "name": "N+1 Multi-Zone Headroom and Quota Sizing Engine",
                "file": "day-087-topic-03-capacity-calc.py",
                "goal": "Write and run a Python capacity planning tool calculating N+1 multi-zone headroom and required Google Cloud regional quotas.",
                "expected": "A runnable script computing maximum steady-state utilization targets and generating GCP quota request specifications.",
                "mode": "local script execution",
                "prereq": "Completion of Exercises 1 and 2.",
                "preflight": "Verify Python runtime and initialize script template.",
                "steps": [
                    "Author the capacity and quota planning calculator:\n\n```sh\ncat <<'EOF' > day-087-topic-03-capacity-calc.py\n#!/usr/bin/env python3\n\"\"\"N+1 Multi-Zone Capacity and GCP Quota Sizing Calculator.\"\"\"\nimport math\n\ndef calculate_capacity(peak_qps, qps_per_core, zones=3, target_util=0.75):\n    \"\"\"\n    Calculate required compute resources ensuring N+1 zone survivability.\n    Target utilization on surviving zones must not exceed target_util (75%).\n    \"\"\"\n    # Safe steady-state ceiling across all zones\n    safe_steady_state_util = ((zones - 1) / zones) * target_util\n    \n    # Raw vCPUs required under normal conditions at 100% capacity\n    raw_vcpus = peak_qps / qps_per_core\n    \n    # Sized vCPUs guaranteeing N+1 survival at target_util\n    required_vcpus = math.ceil(raw_vcpus / safe_steady_state_util)\n    vcpus_per_zone = math.ceil(required_vcpus / zones)\n    total_vcpus = vcpus_per_zone * zones\n    \n    # Recommended GCP Quota (add 25% safety buffer for rolling upgrades)\n    recommended_quota = math.ceil(total_vcpus * 1.25)\n    \n    return safe_steady_state_util, total_vcpus, vcpus_per_zone, recommended_quota\n\n# Brightloaf Holiday Surge Model\nforecast_peak_qps = 8500\nbenchmark_qps_per_core = 35.0  # Measured under production database load\nzones = 3\n\nsafe_util, total_cpus, cpus_per_z, quota_needed = calculate_capacity(\n    forecast_peak_qps, benchmark_qps_per_core, zones\n)\n\nprint(\"1. N+1 Multi-Zone Resilience Planning Matrix (3 Zones):\")\nprint(\"-\" * 70)\nprint(f\"Forecast Peak Load:            {forecast_peak_qps:,} QPS\")\nprint(f\"Single-Core Measured Capacity: {benchmark_qps_per_core:.1f} QPS / vCPU\")\nprint(f\"Max Allowed Steady-State Util: {safe_util * 100.0:.1f}% (Above this, losing 1 zone causes collapse!)\")\nprint(f\"Total Provisioned vCPUs:       {total_cpus} vCPUs ({cpus_per_z} vCPUs / zone)\")\nprint(f\"Surviving Load (1 Zone Lost):  {(1.0 / (zones - 1)) * (forecast_peak_qps / (cpus_per_z * (zones - 1) * benchmark_qps_per_core)) * 100:.1f}% utilization\")\n\nprint(\"\\n2. Google Cloud Regional Quota Recommendation:\")\nprint(\"-\" * 70)\nprint(f\"Minimum Operational vCPUs:     {total_cpus}\")\nprint(f\"Rolling Upgrade Buffer (+25%): {quota_needed - total_cpus}\")\nprint(f\"Recommended GCP Quota Request: {quota_needed} vCPUs (`compute.googleapis.com/cpus`)\")\n\nprint(\"\\n3. Quota Request gcloud Command:\")\nprint(\"-\" * 70)\nprint(f\"# Run 4 weeks prior to holiday launch:\")\nprint(f\"gcloud compute project-info add-metadata \\\")\nprint(f\"    --metadata=quota-request='region=us-central1,metric=CPUS,limit={quota_needed}'\")\nEOF\npython3 day-087-topic-03-capacity-calc.py\n```",
                    "Execute the script and verify that steady-state utilization must not exceed 50.0% in a 3-zone cluster to maintain 75% load during a zone outage.",
                    "Verify the generated quota request includes sufficient headroom for rolling cluster updates.",
                    "Save the script and calculations as exit evidence."
                ],
                "verification": (
                    "Script runs cleanly and displays accurate mathematical sizing for N+1 multi-zone resilience and GCP quota allocation."
                ),
                "trouble": "Ensure steady-state utilization formula multiplies `target_util` by `(zones - 1) / zones`.",
                "cleanup": "Retain `day-087-topic-03-capacity-calc.py` as an exit evidence artifact.",
                "accept": "Demonstrated mastery of N+1 multi-zone capacity planning and Google Cloud quota management."
            }
        }
    ]
}
