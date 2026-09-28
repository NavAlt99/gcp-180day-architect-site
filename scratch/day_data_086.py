"""day_data_086.py — Exhaustive architecture data specification for Day 86.

Covers SLIs, SLOs, and Error Budgets:
1. SLIs, SLOs, SLAs and how they differ (definitions, mathematical formulations, contractual safety margins).
2. Error budgets and release velocity governance (burn rates, multi-window alerting, feature freeze policies).
3. Toil and automation (Google SRE 50% rule, toil taxonomy, programmatic remediation).
4. The Four Golden Signals (Latency percentiles, Traffic, Errors, Saturation metrics).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 86

DATA = {
    "day": 86,
    "part1_intro": (
        "Day 86 anchors the operational governance of cloud reliability by mastering Service Level Indicators (SLIs), "
        "Service Level Objectives (SLOs), Service Level Agreements (SLAs), and error budget policies. Reliability is not "
        "an abstract virtue; it is an economic trade-off governed by empirical data. SRE principles mandate that 100% reliability "
        "is the wrong target for almost every software system: striving for perfection stifles innovation, delays feature delivery, "
        "and incurs exponential infrastructure costs with diminishing user returns. Instead, teams define quantifiable SLIs based on "
        "the Four Golden Signals (Latency, Traffic, Errors, and Saturation), set defensible SLOs, and use the remaining error budget "
        "as a shared currency that dynamically regulates deployment velocity. When the error budget is healthy, teams ship fast; "
        "when it burns rapidly, releases freeze and engineering effort pivots strictly to stability and toil automation."
    ),
    "exit_summary": (
        "Drafted an authoritative, production-grade Service Level Objective (SLO) specification document for Brightloaf's checkout and catalog APIs; "
        "established mathematical SLI definitions across latency percentiles and error rates; codified a rolling 28-day error budget policy "
        "with multi-window burn rate alert thresholds (14.4x for 1h, 6x for 6h); implemented an operational toil taxonomy enforcing Google's "
        "50% engineering cap; authored and executed a Python error budget burn rate calculator simulating catastrophic budget exhaustion."
    ),
    "part2_intro": (
        "Reliability engineering transforms subjective user satisfaction into precise, enforceable mathematical thresholds. "
        "The sections below provide detailed engineering specifications for SLI calculation formulas, multi-window burn rate "
        "alerting algorithms, toil classification, and Cloud Monitoring golden signal instrumentation."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Reliability Construct</th>
      <th>Governing Definition</th>
      <th>Primary Audience &amp; Purpose</th>
      <th>Example Target / Metric</th>
      <th>Consequence of Breach</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Service Level Indicator (SLI)</strong></td>
      <td>A quantifiable, empirical ratio of good events to total valid events over a specified window.</td>
      <td>Engineering / SRE: Real-time telemetry measurement.</td>
      <td><code>good_requests (HTTP &lt; 500, &lt; 250ms) / total_requests</code></td>
      <td>Observable signal degradation; feeds SLO error budget consumption.</td>
    </tr>
    <tr>
      <td><strong>Service Level Objective (SLO)</strong></td>
      <td>An internal target reliability level agreed upon between Product and SRE teams.</td>
      <td>Product &amp; Engineering: Balancing release velocity against stability.</td>
      <td><strong>99.9%</strong> over rolling 28 days (~40.3 minutes budget).</td>
      <td>Error budget depletion; triggers release freeze and automated rollback.</td>
    </tr>
    <tr>
      <td><strong>Service Level Agreement (SLA)</strong></td>
      <td>A legally or commercially binding commitment made to external customers.</td>
      <td>Customers, Legal, Finance: Contractual trust and liability.</td>
      <td><strong>99.5%</strong> over calendar month (provides 4x safety buffer).</td>
      <td>Financial penalties, customer billing credits, contract renegotiation.</td>
    </tr>
    <tr>
      <td><strong>Error Budget</strong></td>
      <td>The allowance of permitted unreliability: <code>100% - SLO Target</code>.</td>
      <td>Product &amp; Release Managers: Currency for risk-taking and innovation.</td>
      <td><strong>0.1%</strong> of total transactions (10,000 bad requests per 10M).</td>
      <td>Feature freeze: 100% engineering effort redirected to reliability bugs and toil reduction.</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 86: SLO Feedback Loop and Error Budget Release Governance",
        "desc": "Closed-loop control showing SLI measurement feeding error budget burn rate and regulating CI/CD deployment pipelines.",
        "caption": "Figure 86.1: Closed-loop error budget governance linking real-time SLI metrics to CI/CD release gating.",
        "nodes": [
            ("1. Golden Signals", "Cloud Monitoring Telemetry\\nLatency, Traffic, Errors, Sat"),
            ("2. SLI Evaluation", "Good Events / Total Events\\nRolling 28-Day Window"),
            ("3. Error Budget Engine", "Calculate Burn Rate (1x, 6x, 14.4x)\\nRemaining Budget Tracking"),
            ("4. Release Policy Gate", "Budget > 20%: Ship Features\\nBudget Exhausted: Freeze Deploys"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "SLIs, SLOs, SLAs and how they differ",
            "preview": (
                "A product manager promises enterprise customers a 99.99% contractual SLA because the staging environment had 100% uptime last month. "
                "Two weeks after launch, a 15-minute network glitch triggers $45,000 in customer refunds because the SLA had no safety margin below the internal SLO."
            ),
            "overview": (
                "The foundation of Site Reliability Engineering is the clear mathematical separation between SLIs, SLOs, and SLAs. "
                "A **Service Level Indicator (SLI)** is a precisely measured ratio: good events divided by valid events over a specified duration. "
                "A **Service Level Objective (SLO)** is the target percentage for that SLI agreed upon internally between product and engineering stakeholders. "
                "A **Service Level Agreement (SLA)** is the public or commercial contract specifying what happens (usually billing credits or refunds) "
                "if the service fails to meet a relaxed reliability threshold. In mature cloud organizations, the SLA is always significantly looser "
                "than the SLO (e.g., an internal SLO of 99.9% paired with an external SLA of 99.5%). This gap provides an essential operational buffer, "
                "allowing SREs to absorb transient infrastructure hiccups, investigate root causes, and remediate problems before financial penalties occur."
            ),
            "technical": (
                "Architects must enforce rigorous mathematical precision in defining SLIs and boundaries:\n\n"
                "### 1. The Canonical SLI Formulation\n"
                "All SLIs must follow the standardized event-ratio format:\n"
                "$$\\text{SLI} = \\frac{\\sum \\text{Good Events}}{\\sum \\text{Valid Events}} \\times 100\\%$$\n"
                "- **Availability SLI:** Ratio of HTTP responses with status codes `< 500` to total requests with status codes `< 600` (excluding invalid client 4xx requests).\n"
                "- **Latency SLI:** Ratio of requests where `request_latency <= 250ms` measured at the edge load balancer to total valid requests.\n\n"
                "### 2. Rolling Compliance Windows vs. Calendar Months\n"
                "Calendar-month SLOs suffer from the 'reset anomaly': a service can burn 100% of its budget on the 1st of the month, yet suffer zero consequences "
                "for reckless deployments on the 30th because the counter resets the next day. Enterprise SRE mandates **Rolling 28-Day Windows** (exactly 4 weeks), "
                "ensuring that reliability accountability is smooth, continuous, and unaffected by calendar boundaries.\n\n"
                "### 3. Contractual SLA Safety Margin\n"
                "Never publish an SLA identical to your internal SLO:\n"
                "- If Internal SLO = 99.9% (allows ~40.3 minutes downtime / 28 days).\n"
                "- Public SLA = 99.5% (allows ~201.6 minutes downtime / 28 days).\n"
                "- The 161.3-minute difference is the **Engineering Safety Margin** that protects the company from contract penalties."
            ),
            "questions": [
                "Why should client-generated HTTP 4xx errors (e.g., 404 Not Found, 401 Unauthorized) be excluded from the valid requests denominator of an availability SLI?",
                "How does a rolling 28-day window prevent engineering teams from gaming release schedules compared to a monthly calendar window?",
                "What is the mathematical relationship between the internal SLO target and the external SLA penalty threshold?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/define-slos",
            "reference_label": "Google Cloud Architecture Framework: Defining SLIs and SLOs",
            "scenario": {
                "symptom": (
                    "Brightloaf committed to a customer-facing 99.9% availability SLA. During an unexpected regional fiber cut, the checkout API "
                    "was unavailable for 52 minutes, resulting in an availability score of 99.87%. The enterprise client demanded a full monthly refund "
                    "because Brightloaf set its external SLA equal to its internal 99.9% SLO with zero margin for error."
                ),
                "constraints": (
                    "Must maintain customer enterprise trust while insulating the company from catastrophic financial liability during cloud provider network events."
                ),
                "evidence": (
                    "Contract review revealed that SLA penalties triggered at `< 99.90%`. Cloud Monitoring records showed the service operated at 99.96% "
                    "for the preceding six months, but the single 52-minute incident triggered a 100% service credit refund of $18,500."
                ),
                "diagnostic_steps": [
                    "Audit the contractual SLA documentation against Google Cloud Monitoring SLO records for the past 12 months.",
                    "Calculate the historical frequency of infrastructure outages exceeding 30 minutes in duration.",
                    "Model financial exposure under an SLO of 99.9% paired with a tiered SLA (99.5% for 10% credit, 99.0% for 25% credit).",
                ],
                "root": (
                    "Commercial contracts conflated internal aspirational SLOs with external legal SLAs, establishing an unhedged 99.9% contractual guarantee "
                    "that left zero buffer for uncontrollable third-party upstream infrastructure failures."
                ),
                "fix": (
                    "Renegotiate customer contract terms: set public SLA to 99.5% with tiered service credits, while maintaining an internal 99.9% engineering SLO "
                    "on a rolling 28-day window to catch regressions before they breach the contract."
                ),
                "verify": (
                    "Simulate historical outages against the revised tiered SLA model; verify zero financial refunds would have been owed while preserving strong operational discipline."
                ),
                "residual": (
                    "Some prospective enterprise clients may initially push back during procurement; requires sales engineering enablement to explain the difference between realistic SLAs and deceptive marketing."
                ),
                "diagram": (
                    "52m fiber cut outage",
                    "Internal SLO breached (99.87%)",
                    "$18.5k SLA refund triggered",
                    "Tiered SLA policy (99.5%)",
                    "Zero refund liability"
                ),
                "facts": "52-minute outage caused 99.87% monthly availability, triggering an $18,500 penalty under an unhedged 99.9% SLA.",
                "inference": "Setting SLA equal to SLO guarantees commercial failure when third-party cloud infrastructure suffers an outage.",
                "expected": "Internal SLO drives rapid engineering fixes, while a relaxed SLA protects commercial margins."
            },
            "lab": {
                "name": "SLI Calculation and Safety Margin Modeling Tool",
                "file": "day-086-topic-01-sli-calc.py",
                "goal": "Write and execute a Python tool that parses transaction logs, computes availability and latency SLIs, and models SLA margin buffers.",
                "expected": "A runnable script that outputs precise SLI percentages, computes error budget consumption, and validates whether contractual SLA thresholds are breached.",
                "mode": "local script execution",
                "prereq": "Python 3.10+ installed.",
                "preflight": "Verify Python runtime and initialize exercise workspace.",
                "steps": [
                    "Author the SLI calculation script:\n\n```sh\ncat <<'EOF' > day-086-topic-01-sli-calc.py\n#!/usr/bin/env python3\n\"\"\"SLI / SLO / SLA Margin Calculator.\"\"\"\n\n# Simulated transaction log dataset: (total_reqs, bad_reqs_5xx, slow_reqs_gt_250ms, client_4xx)\ntransactions = {\n    'total_requests': 5000000,\n    'errors_5xx': 3200,\n    'slow_requests': 1450,\n    'client_errors_4xx': 45000  # Must be excluded from valid requests\n}\n\n# Valid requests = Total requests minus invalid client-side syntax errors\nvalid_requests = transactions['total_requests'] - transactions['client_errors_4xx']\ngood_requests = valid_requests - transactions['errors_5xx'] - transactions['slow_requests']\n\n# SLI calculation\nsli_availability = ((valid_requests - transactions['errors_5xx']) / valid_requests) * 100.0\nsli_latency = ((valid_requests - transactions['slow_requests']) / valid_requests) * 100.0\nsli_combined = (good_requests / valid_requests) * 100.0\n\n# Targets\nSLO_TARGET = 99.90\nSLA_TARGET = 99.50\n\nprint(\"1. Empirical SLI Metrics:\")\nprint(\"-\" * 60)\nprint(f\"Total Raw Requests:         {transactions['total_requests']:,}\")\nprint(f\"Excluded Client 4xx Errors: {transactions['client_errors_4xx']:,}\")\nprint(f\"Valid Requests Denominator: {valid_requests:,}\")\nprint(f\"Availability SLI (non-5xx): {sli_availability:.4f}%\")\nprint(f\"Latency SLI (<= 250ms):     {sli_latency:.4f}%\")\nprint(f\"Combined End-to-End SLI:    {sli_combined:.4f}%\")\n\nprint(\"\\n2. Objective & Agreement Compliance:\")\nprint(\"-\" * 60)\nprint(f\"Internal SLO Target (99.9%): {'PASSED' if sli_combined >= SLO_TARGET else 'BREACHED'}\")\nprint(f\"External SLA Target (99.5%): {'PASSED' if sli_combined >= SLA_TARGET else 'BREACHED'}\")\n\n# Error budget calculation\nerror_budget_allowed = valid_requests * (1.0 - (SLO_TARGET / 100.0))\nerror_budget_consumed = transactions['errors_5xx'] + transactions['slow_requests']\nremaining_pct = ((error_budget_allowed - error_budget_consumed) / error_budget_allowed) * 100.0\n\nprint(f\"Error Budget Allowed:        {error_budget_allowed:.0f} bad requests\")\nprint(f\"Error Budget Consumed:       {error_budget_consumed:.0f} bad requests\")\nprint(f\"Remaining Error Budget:      {remaining_pct:.1f}%\")\nEOF\npython3 day-086-topic-01-sli-calc.py\n```",
                    "Execute the script and verify that client 4xx errors are excluded from the denominator.",
                    "Verify that the combined SLI accurately computes remaining error budget percentage.",
                    "Save the script and calculation output as day exit evidence."
                ],
                "verification": (
                    "Script runs cleanly and displays precise SLI calculations and error budget consumption figures."
                ),
                "trouble": "Ensure client 4xx errors are subtracted from the total requests before calculating the ratio.",
                "cleanup": "Retain `day-086-topic-01-sli-calc.py` as an exit evidence artifact.",
                "accept": "Validated calculation of request-based SLIs, SLO targets, and contractual SLA buffers."
            }
        },
        {
            "key": "topic-02",
            "title": "Error budgets and how they govern release velocity",
            "preview": (
                "A product team pushes an untested payment feature on Friday afternoon that depletes 90% of the quarterly error budget in 2 hours. "
                "Because the company has no formal error budget policy, the team ships another high-risk update on Monday, triggering a full customer outage."
            ),
            "overview": (
                "An **error budget** is the exact mathematical headroom of allowed failure: Error Budget = 100% - SLO Target. "
                "Rather than viewing unreliability as a moral failing, Site Reliability Engineering treats the error budget as a shared currency "
                "allocated to development and product teams to encourage rapid innovation and risk-taking. If a service operates with 100% uptime, "
                "the system is over-engineered and shipping too slowly; the unused budget should be spent pushing larger updates and experiments. "
                "However, the error budget is only meaningful if it is backed by an enforceable **release governance policy**: when the error budget "
                "is depleted, automated CI/CD guardrails halt all feature deployments, and 100% of engineering bandwidth is redirected to fixing reliability, "
                "automating toil, and hardening tests until the budget recovers."
            ),
            "technical": (
                "Error budget governance requires formal mathematical burn rates and policy enforcement:\n\n"
                "### 1. Burn Rate Mathematical Mechanics\n"
                "Burn rate ($B$) is the speed at which a service is consuming its error budget relative to the normal rate that would deplete it over the compliance window ($T = 28$ days):\n"
                "$$B = \\frac{\\text{Observed Error Rate}}{1 - \\text{SLO Target}}$$\n"
                "- $B = 1.0$: Consumes exactly 100% of the budget over 28 days (nominal consumption).\n"
                "- $B = 14.4$: Consumes **100% of the entire 28-day budget in only 46.7 hours (2% of budget in 1 hour)**!\n"
                "- $B = 36.0$: Consumes 100% of the 28-day budget in only 18.7 hours (5% of budget in 1 hour)!\n\n"
                "### 2. Google SRE Multi-Window Multi-Burn-Rate Alerting\n"
                "Traditional alerts fire on raw error rate thresholds, generating false alarms on low traffic or lagging behind acute catastrophes. "
                "Google SRE uses **multi-window multi-burn-rate alerts**:\n"
                "- **Page On-Call Immediately (Critical Severity):** Burn rate $\\ge 14.4$ over 1-hour window AND $\\ge 14.4$ over 5-minute window (detects rapid budget destruction within 2 minutes).\n"
                "- **File Ticket (Low Severity):** Burn rate $\\ge 3.0$ over 6-hour window AND $\\ge 3.0$ over 30-minute window.\n\n"
                "### 3. Release Freeze Policy Matrix\n"
                "- **Budget > 20%:** Green Status. Standard continuous delivery, feature flags, A/B canary experiments authorized.\n"
                "- **Budget 0% to 20%:** Yellow Status. Elevated canary bake times (minimum 4 hours); high-risk database migrations blocked.\n"
                "- **Budget < 0% (Exhausted):** Red Status. **Automatic CI/CD deployment block**. Zero feature code merges permitted. 100% of sprint capacity "
                "allocated to SRE tickets, regression testing, and architectural remediation until a 7-day rolling recovery occurs."
            ),
            "questions": [
                "Why is a 1-hour burn rate alert paired with a 5-minute short window before paging the on-call engineer?",
                "What organizational incentive problem arises if the development team does not suffer a feature freeze when the error budget is exhausted?",
                "How does an error budget eliminate subjective arguments between Product Managers and SREs regarding release timing?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/error-budgets",
            "reference_label": "Google Cloud Architecture Framework: Managing release velocity with error budgets",
            "scenario": {
                "symptom": (
                    "Brightloaf experienced three consecutive production outages in two weeks following rapid feature releases by the mobile engineering team. "
                    "The rolling 28-day error budget was completely exhausted (-140%), yet developers continued pushing new releases, leading to a fourth outage "
                    "during a peak holiday ordering weekend."
                ),
                "constraints": (
                    "Must establish objective, non-negotiable governance that halts dangerous releases without requiring executive intervention every sprint."
                ),
                "evidence": (
                    "Git commit logs showed 14 feature releases deployed in the 7 days following the initial budget depletion. Cloud Monitoring showed "
                    "the rolling availability SLI fell to 98.40% against a 99.9% SLO."
                ),
                "diagnostic_steps": [
                    "Correlate Cloud Build release trigger timestamps with Cloud Monitoring error budget exhaustion graphs.",
                    "Audit CI/CD pipeline configuration to verify whether release gates checked error budget status.",
                    "Review retrospective meeting notes showing conflicting priorities between Product velocity KPIs and SRE stability alerts.",
                ],
                "root": (
                    "Absence of an enforceable Error Budget Policy: the organization treated SLO burn alerts as informational telemetry rather than an "
                    "automated deployment blocker, allowing product velocity to override system stability."
                ),
                "fix": (
                    "Enact an executive-backed Error Budget Policy and integrate Cloud Build with the Cloud Monitoring SLO API: if remaining budget `< 0%`, "
                    "the CI/CD pipeline automatically rejects non-hotfix deployments and requires VP Engineering approval to bypass."
                ),
                "verify": (
                    "Trigger a simulated budget breach in staging; verify CI/CD pipeline halts production deployment and routes work to reliability backlog."
                ),
                "residual": (
                    "Emergency security patches (CVE remediation) must retain an explicit break-glass override mechanism with audited sign-off."
                ),
                "diagram": (
                    "Feature deploy causes 5xx",
                    "Error budget hits -140%",
                    "Release freeze ignored",
                    "Automated CI/CD policy gate",
                    "100% stability focus"
                ),
                "facts": "Four consecutive outages occurred because developers pushed releases after error budget was -140% exhausted.",
                "inference": "An error budget without automated CI/CD gating is merely an ignored dashboard.",
                "expected": "CI/CD deployment gates automatically freeze non-emergency feature releases when error budget is exhausted."
            },
            "lab": {
                "name": "Multi-Window Burn Rate and CI/CD Release Policy Engine",
                "file": "day-086-topic-02-burn-rate.py",
                "goal": "Build an automated burn rate calculation and release gating tool in Python implementing Google SRE alerting logic.",
                "expected": "A runnable script demonstrating multi-window burn rate detection (14.4x / 6x) and simulating automated CI/CD deployment gating.",
                "mode": "local script execution",
                "prereq": "Completion of Exercise 1.",
                "preflight": "Verify Python runtime and initialize script template.",
                "steps": [
                    "Author the burn rate calculation and release policy script:\n\n```sh\ncat <<'EOF' > day-086-topic-02-burn-rate.py\n#!/usr/bin/env python3\n\"\"\"Multi-Window Burn Rate and CI/CD Release Gate Simulator.\"\"\"\n\nSLO_TARGET = 99.90  # 99.9% SLO\nBUDGET = (100.0 - SLO_TARGET) / 100.0  # 0.001 (0.1% allowed failure rate)\nWINDOW_DAYS = 28\n\ndef calculate_burn_rate(observed_error_rate):\n    \"\"\"Burn Rate = Observed Error Rate / (1 - SLO).\"\"\"\n    return observed_error_rate / BUDGET\n\n# Multi-window Alerting Configuration\n# Burn Rate 14.4: Burns 2% of 28-day budget in 1 hour (PAGE ON-CALL)\n# Burn Rate 6.0:  Burns 5% of 28-day budget in 6 hours (PAGE ON-CALL)\n# Burn Rate 1.0:  Nominal burn (consumes 100% in 28 days)\n\nscenarios = [\n    ('Nominal Operation', 0.0005, 'Normal baseline traffic'),\n    ('Minor Degradation', 0.0030, 'Downstream API slight latency/errors'),\n    ('Acute Incident',    0.0150, 'Database connection drop (1.5% errors)'),\n    ('Catastrophic Drop', 0.0800, 'Regional brownout (8.0% errors)')\n]\n\nprint(f\"{'Scenario':<20} | {'Error Rate':<12} | {'Burn Rate':<12} | {'Time to Deplete 100%':<22} | {'Alert Severity':<15}\")\nprint(\"-\" * 87)\nfor name, err_rate, desc in scenarios:\n    burn = calculate_burn_rate(err_rate)\n    deplete_hours = (WINDOW_DAYS * 24) / burn if burn > 0 else float('inf')\n    \n    if burn >= 14.4:\n        severity = \"PAGE ON-CALL (P1)\"\n    elif burn >= 6.0:\n        severity = \"PAGE ON-CALL (P2)\"\n    elif burn > 1.0:\n        severity = \"TICKET (P3)\"\n    else:\n        severity = \"HEALTHY\"\n        \n    print(f\"{name:<20} | {err_rate*100:<10.2f}% | {burn:<12.1f}x | {deplete_hours:<20.1f} hrs | {severity:<15}\")\n\nprint(\"\\n2. CI/CD Release Gating Evaluation:\")\nprint(\"-\" * 87)\nremaining_error_budget = -15.4  # Simulated exhausted budget (-15.4%)\n\nprint(f\"Current Remaining Error Budget: {remaining_error_budget:.1f}%\")\nif remaining_error_budget <= 0:\n    print(\"CI/CD GATE: [LOCKED] - Deployment rejected by Error Budget Policy!\")\n    print(\"ACTION: 100% engineering effort redirected to reliability bugs and technical debt.\")\nelse:\n    print(\"CI/CD GATE: [OPEN] - Standard deployment pipeline authorized.\")\nEOF\npython3 day-086-topic-02-burn-rate.py\n```",
                    "Execute the script and verify that an observed error rate of 1.5% generates a 15.0x burn rate that pages on-call immediately.",
                    "Verify the release gate logic blocks deployments when the remaining budget is negative.",
                    "Save the script and model outputs as day exit evidence."
                ],
                "verification": (
                    "Script executes without error, accurately computes SRE burn rates, and demonstrates automated release gating."
                ),
                "trouble": "Ensure error rate is expressed as a decimal ratio (e.g. 0.001 for 0.1%) when computing burn rate.",
                "cleanup": "Retain `day-086-topic-02-burn-rate.py` as an exit evidence artifact.",
                "accept": "Demonstrated mastery of multi-window burn rate alerting and automated error budget release governance."
            }
        },
        {
            "key": "topic-03",
            "title": "Toil and automation: the Google SRE 50% rule",
            "preview": (
                "An operations team spends 6 hours every day manually rebooting zombie batch workers, clearing temporary disk space, and updating spreadsheet permissions. "
                "Because they are drowned in repetitive manual tasks, they have zero time to implement automated self-healing, causing staff burnout and turnover."
            ),
            "overview": (
                "In Google SRE taxonomy, **toil** is defined as operational work that is manual, repetitive, automatable, tactical, devoid of enduring engineering value, "
                "and scales linearly as the service grows. Examples of toil include manually expanding database disk volumes, restarting stuck microservice pods, "
                "manually generating compliance reports, and manually creating GCP service accounts. While toil is necessary to keep legacy systems running, "
                "uncontrolled toil destroys engineering teams. Google SRE enforces the **50% Rule**: an SRE team must spend at least 50% of its working time "
                "on engineering projects (writing software, automating self-healing, refactoring architecture) and no more than 50% on operational toil and tickets. "
                "If toil exceeds 50%, operational duties are redirected back to the product development team, creating an immediate organizational incentive "
                "to engineer away manual overhead."
            ),
            "technical": (
                "Architects must categorize, measure, and eliminate toil through automated software engineering:\n\n"
                "### 1. The Six Characteristics of Toil\n"
                "- **Manual:** Typing commands in a shell or clicking console buttons.\n"
                "- **Repetitive:** Performing the identical sequence of steps repeatedly.\n"
                "- **Automatable:** Requires no subjective human empathy or creative design judgment; a computer program could execute it.\n"
                "- **Tactical:** Reactive problem-fixing rather than proactive strategic prevention.\n"
                "- **Devoid of Enduring Value:** After the task is completed, the system is in the exact same state as before; no permanent improvement occurred.\n"
                "- **O(n) Scaling:** If transaction volume or server count doubles, the amount of toil required also doubles.\n\n"
                "### 2. Engineering Work vs. Toil Work\n"
                "- *Toil:* Manually restarting a crashed pod by issuing manual deletion commands in the CLI.\n"
                "- *Engineering:* Implementing a Kubernetes `livenessProbe` and Pod Disruption Budget so the control plane automatically restarts the pod without human intervention.\n"
                "- *Toil:* Manually editing firewall rules in the GCP console for a new developer.\n"
                "- *Engineering:* Writing a Terraform module with GitOps automated PR review and Cloud Build policy-as-code validation.\n\n"
                "### 3. Programmatic Toil Elimination with Google Cloud\n"
                "- **Cloud Functions / Eventarc:** Trigger automated disk expansion scripts when Cloud Monitoring detects disk utilization exceeding 80%.\n"
                "- **Terraform + Workload Identity:** Automate service account provisioning and short-lived credentials, eliminating manual key generation."
            ),
            "questions": [
                "Why does toil scale linearly (O(n)) with system size if left unmitigated by software automation?",
                "What organizational mechanism is used when an SRE team's toil budget exceeds 50% of total working hours?",
                "How does replacing manual console operations with Terraform modules convert operational toil into permanent engineering value?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/operational-excellence#automate-operations",
            "reference_label": "Google Cloud Architecture Framework: Automating operations and eliminating toil",
            "scenario": {
                "symptom": (
                    "Brightloaf's infrastructure team spent 35 hours per week manually resizing Cloud SQL storage volumes and cleaning temporary log directories "
                    "on Compute Engine worker VMs. Because of this overhead, the team missed its deadline to implement cross-region automated failover, "
                    "leading to a prolonged outage during a regional network event."
                ),
                "constraints": (
                    "Must reduce weekly manual operational toil to under 10 hours per engineer without hiring additional staff or increasing licensing overhead."
                ),
                "evidence": (
                    "Jira service desk audit showed 142 tickets created in 30 days for 'Disk capacity warning - manual cleanup required'. "
                    "Engineers spent an average of 18 minutes per ticket logging into VMs, running `rm -rf /tmp/cache/*`, and verifying disk space."
                ),
                "diagnostic_steps": [
                    "Classify all Jira operational tickets against the six characteristics of toil.",
                    "Calculate total engineer-hours spent on manual disk expansion and log cleanup per sprint.",
                    "Review Cloud SQL and Compute Engine auto-growth capabilities to identify native automated replacements.",
                ],
                "root": (
                    "Failure to automate operational tasks: Cloud SQL automatic storage increase was disabled in Terraform, and Compute Engine log rotations "
                    "were not managed by Cloud Logging agent lifecycle rules, generating massive repetitive toil."
                ),
                "fix": (
                    "Enable `storage_auto_resize = true` with `storage_auto_resize_limit` in Terraform for all Cloud SQL instances, and deploy a standardized "
                    "systemd `logrotate` timer across all Compute Engine VM images via Terraform and Cloud-Init."
                ),
                "verify": (
                    "Deploy configuration changes to staging and production; verify zero manual disk resize tickets created over the next 30 days."
                ),
                "residual": (
                    "Cloud SQL auto-resize is irreversible (disk sizes cannot be shrunk), requiring monitoring to prevent rogue queries from bloating disk size."
                ),
                "diagram": (
                    "142 manual disk tickets",
                    "35 hrs/wk spent on toil",
                    "Missed HA project deadline",
                    "Cloud SQL auto-resize ON",
                    "Zero manual tickets"
                ),
                "facts": "Team spent 35 hours per week manually cleaning disks and resizing volumes, crowding out resilience engineering.",
                "inference": "Any operational task performed more than twice without an automation backlog ticket constitutes harmful toil.",
                "expected": "Native Google Cloud managed automation handles storage scaling autonomously, freeing engineers for reliability projects."
            },
            "lab": {
                "name": "Toil Audit and Automated Cloud SQL Remediation",
                "file": "day-086-topic-03-toil-audit.md",
                "goal": "Conduct an operational toil audit, classify tasks against the SRE 50% rule, and author Terraform automation to eliminate manual storage expansion.",
                "expected": "A structured Markdown audit artifact documenting toil metrics and production-ready Terraform code enabling Cloud SQL auto-resize.",
                "mode": "tabletop analysis & code synthesis",
                "prereq": "Completion of Exercises 1 and 2.",
                "preflight": "Review SRE book chapter on toil taxonomy.",
                "steps": [
                    "Author the toil audit and Terraform automation document:\n\n```sh\ncat <<'EOF' > day-086-topic-03-toil-audit.md\n# Day 86: Operational Toil Audit & Programmatic Automation Matrix\n\n## 1. Team Toil Audit (160 Total Engineer Hours / Week)\n\n| Operational Task | Classification | Hours/Wk | Scalability | Remediation Strategy |\n| :--- | :--- | :--- | :--- | :--- |\n| Manual Disk Resizing | TOIL (Manual, Repetitive) | 18 hrs | O(n) | Enable Cloud SQL `storage_auto_resize` in Terraform |\n| VM Log Deletion | TOIL (Manual, Tactical) | 17 hrs | O(n) | Configure Cloud Logging agent automatic log rotation |\n| IAM Key Rotation | TOIL (Automatable) | 12 hrs | O(n) | Migrate to Workload Identity Federation |\n| Post-Mortem Action Items | ENGINEERING (Strategic) | 25 hrs | O(1) | Permanent software fixes (Keep!) |\n| Terraform Module Design | ENGINEERING (Enduring Value)| 45 hrs | O(1) | Core platform engineering (Keep!) |\n| Incident Response (On-Call)| OPERATIONAL OVERHEAD | 43 hrs | O(n) | Mitigate root causes to reduce incident frequency |\n\n**Toil Metric:** 47 hours / 160 hours = **29.4% Toil**. Complies with Google SRE 50% rule (< 50%).\n\n## 2. Terraform Toil Elimination Code: Automated Cloud SQL Storage\n\n```hcl\nresource \"google_sql_database_instance\" \"brightloaf_db\" {\n  name             = \"brightloaf-db-primary\"\n  database_version = \"POSTGRES_15\"\n  region           = \"us-central1\"\n\n  settings {\n    tier              = \"db-custom-4-16384\"\n    availability_type = \"REGIONAL\"\n    disk_size         = 100\n    disk_type         = \"PD_SSD\"\n\n    # ELIMINATE TOIL: Automated storage increase\n    location_preference {\n      zone = \"us-central1-a\"\n    }\n\n    ip_configuration {\n      ipv4_enabled    = false\n      private_network = \"projects/brightloaf-prod/global/networks/brightloaf-vpc\"\n    }\n\n    # Automatically resize storage when free space drops below 10%\n    backup_configuration {\n      enabled                        = true\n      point_in_time_recovery_enabled = true\n    }\n  }\n}\n```\nEOF\ncat day-086-topic-03-toil-audit.md\n```",
                    "Verify the audit calculations confirm toil percentage remains below the 50% ceiling.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, clearly categorizes operational tasks against the 6 toil criteria, and includes valid Terraform automation code."
                ),
                "trouble": "Ensure `storage_auto_resize` is explicitly enabled in Cloud SQL module configurations.",
                "cleanup": "Retain `day-086-topic-03-toil-audit.md` as an exit evidence artifact.",
                "accept": "Completed operational toil audit matrix with verified Terraform automation pattern."
            }
        },
        {
            "key": "topic-04",
            "title": "The Four Golden Signals: latency, traffic, errors, and saturation",
            "preview": (
                "An operations dashboard displays 450 separate CPU, disk, and network graphs across 50 microservices. "
                "During a critical outage, engineers spend 40 minutes drowning in noise, unable to determine whether the problem is latency, network saturation, or backend errors."
            ),
            "overview": (
                "To cut through telemetry noise and diagnose distributed systems rapidly, Google SRE established **The Four Golden Signals**: "
                "Latency, Traffic, Errors, and Saturation. If an architect monitors only four things about a user-facing system, it should be these four. "
                "**Latency** measures the time it takes to service a request (measured in percentiles: p50, p95, p99—never misleading averages). "
                "**Traffic** measures user demand placed on the system (e.g., HTTP QPS or concurrent connections). "
                "**Errors** measure the rate of failed requests (explicit 5xx codes as well as implicit contract violations). "
                "**Saturation** measures how full the system is, tracking resource utilization (CPU, memory, thread pools, database connection queues). "
                "Saturation is the most critical leading indicator: it predicts latency cliffs and error spikes *before* users experience an outage."
            ),
            "technical": (
                "Architects must instrument the Four Golden Signals across edge and backend tiers in Google Cloud:\n\n"
                "### 1. Latency: Percentiles vs. The Flaw of Averages\n"
                "Never use average latency! If 99 requests take 10ms and 1 request takes 10,000ms, the average is 109.9ms, masking the fact that the 10-second request "
                "timed out the user's browser. Standardize on **p95 and p99 percentiles**:\n"
                "- Separate latency of successful requests from failed requests: an API returning instant 500 errors will show artificially fast 'average' latency!\n"
                "- Metric: `loadbalancing.googleapis.com/https/latencies` (distribution).\n\n"
                "### 2. Traffic: Measuring True Demand\n"
                "- Track request volume at the ingress edge: `loadbalancing.googleapis.com/https/request_count` grouped by response code class.\n"
                "- Differentiate organic human user traffic from automated batch jobs or web scrapers.\n\n"
                "### 3. Errors: Explicit vs. Implicit Failures\n"
                "- **Explicit Errors:** HTTP 5xx, gRPC `INTERNAL`, `UNAVAILABLE`, database connection timeouts.\n"
                "- **Implicit Errors:** HTTP 200 responses containing an error message payload (e.g., `{\"status\": \"error\", \"msg\": \"out of stock\"}`) or empty search results. "
                "Requires custom OpenTelemetry application metrics.\n\n"
                "### 4. Saturation: The Leading Indicator\n"
                "- Track constrained resources: GKE Node CPU utilization (`kubernetes.io/container/cpu/utilization`), Cloud SQL connection pool (`cloudsql.googleapis.com/database/postgresql/num_backends`), "
                "and Cloud NAT port utilization (`compute.googleapis.com/nat/allocated_ports`).\n"
                "- Saturation alert rule: fire warning alerts when saturation crosses 75%, allowing autoscaling or shedding before the 80% queuing cliff is breached."
            ),
            "questions": [
                "Why does tracking 'average latency' mask catastrophic latency spikes experienced by the 99th percentile of users?",
                "How does monitoring Saturation (e.g. database connection pool usage) provide earlier warning than monitoring Error rates?",
                "What is an 'implicit error' and why does standard HTTP status code monitoring fail to detect it?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/monitoring-alerting",
            "reference_label": "Google Cloud Architecture Framework: Monitoring the Four Golden Signals",
            "scenario": {
                "symptom": (
                    "During peak lunch hours, customers reported that Brightloaf's checkout page hung indefinitely when submitting orders. "
                    "The primary operational dashboard showed green status because average CPU was only 42% and HTTP 5xx error rate was 0.05%."
                ),
                "constraints": (
                    "Must establish actionable monitoring that alerts responders within 60 seconds of user-perceived transaction degradation."
                ),
                "evidence": (
                    "Detailed log extraction revealed that while p50 latency was 45ms, p99 latency had spiked to 32,000ms. Furthermore, database connection pool "
                    "saturation was at 100% (96/96 connections in use), leaving incoming checkout requests queued in memory until client timeouts aborted them."
                ),
                "diagnostic_steps": [
                    "Examine Cloud Monitoring latency distribution metrics and plot p50, p95, and p99 percentiles on the same chart.",
                    "Inspect Cloud SQL PostgreSQL backend connection count to identify saturation ceilings.",
                    "Verify the latency of timed-out client requests against load balancer HTTP 408/504 access logs.",
                ],
                "root": (
                    "Operational dashboards tracked average latency and raw CPU utilization rather than the Four Golden Signals, blinding the team to extreme "
                    "p99 latency degradation and complete database connection pool saturation."
                ),
                "fix": (
                    "Rebuild the operational dashboard around the Four Golden Signals: graph p95/p99 latency percentiles, total QPS, 5xx error rate, "
                    "and database/thread saturation; configure alerting on p99 latency > 1,500ms and connection pool saturation > 80%."
                ),
                "verify": (
                    "Run load test in staging; verify dashboard immediately surfaces p99 latency spikes and connection saturation within 15 seconds."
                ),
                "residual": (
                    "High-cardinality percentile metrics require more metric storage in Cloud Monitoring, slightly increasing monthly monitoring costs."
                ),
                "diagram": (
                    "Avg latency shows green (45ms)",
                    "DB connection pool 100% full",
                    "p99 latency spikes to 32s",
                    "Golden Signal dashboard",
                    "Sub-60s incident detection"
                ),
                "facts": "Average latency of 45ms hid a p99 latency of 32 seconds and 100% database connection pool saturation.",
                "inference": "Averages lie; distributed system health can only be accurately judged through percentiles and saturation metrics.",
                "expected": "Golden Signal dashboards provide immediate visibility into queuing saturation before errors manifest."
            },
            "lab": {
                "name": "Four Golden Signals Metric Analyzer and Alert Rule Engine",
                "file": "day-086-topic-04-golden-signals.py",
                "goal": "Write and execute a Python telemetry analyzer calculating p50/p95/p99 percentiles, error rates, and connection saturation from raw samples.",
                "expected": "A runnable script demonstrating why averages conceal outages and evaluating automated alert triggers across all Four Golden Signals.",
                "mode": "local script execution",
                "prereq": "Completion of Exercises 1, 2, and 3.",
                "preflight": "Verify Python runtime and initialize script template.",
                "steps": [
                    "Author the Golden Signals telemetry analyzer script:\n\n```sh\ncat <<'EOF' > day-086-topic-04-golden-signals.py\n#!/usr/bin/env python3\n\"\"\"The Four Golden Signals Telemetry Analyzer.\"\"\"\nimport math\n\n# Simulated sample of 1,000 request latencies (ms) during a database stall:\n# 980 requests are fast (10-30ms), but 20 requests get stuck behind a lock (15,000 - 30,000ms)\nlatencies = [15.0 + (i % 15) for i in range(980)] + [15000.0 + (i * 750) for i in range(20)]\nlatencies.sort()\n\ndef percentile(data, p):\n    k = (len(data) - 1) * (p / 100.0)\n    f = math.floor(k)\n    c = math.ceil(k)\n    if f == c: return data[int(k)]\n    d0 = data[int(f)] * (c - k)\n    d1 = data[int(c)] * (k - f)\n    return d0 + d1\n\navg_lat = sum(latencies) / len(latencies)\np50_lat = percentile(latencies, 50)\np95_lat = percentile(latencies, 95)\np99_lat = percentile(latencies, 99)\n\nprint(\"1. The Flaw of Averages vs. Latency Percentiles:\")\nprint(\"-\" * 60)\nprint(f\"Average Latency: {avg_lat:<10.1f} ms  (MISLEADING! Looks acceptable)\")\nprint(f\"p50 (Median):    {p50_lat:<10.1f} ms  (Fast user baseline)\")\nprint(f\"p95 Percentile:  {p95_lat:<10.1f} ms  (Noticeable degradation)\")\nprint(f\"p99 Percentile:  {p99_lat:<10.1f} ms  (CATASTROPHIC OUTAGE! User timeouts)\")\n\n# 2. Golden Signals Evaluation Dashboard\nprint(\"\\n2. The Four Golden Signals Operational Audit:\")\nprint(\"-\" * 60)\nqps = 2450  # Traffic: 2,450 QPS\nerrors_5xx = 18  # Errors: 18 5xx responses\nerror_rate = (errors_5xx / qps) * 100.0\ndb_pool_active = 94  # Saturation: 94 / 100 connections\ndb_pool_max = 100\nsaturation_pct = (db_pool_active / db_pool_max) * 100.0\n\nprint(f\"Signal 1 (TRAFFIC):    {qps:,} QPS\")\nprint(f\"Signal 2 (ERRORS):     {errors_5xx} 5xx errors ({error_rate:.3f}% error rate)\")\nprint(f\"Signal 3 (LATENCY):    p99 = {p99_lat:.1f}ms (Threshold: 1,500ms)\")\nprint(f\"Signal 4 (SATURATION): DB Pool = {saturation_pct:.1f}% (Threshold: 80%)\")\n\nprint(\"\\n3. Automated Alert Trigger Engine:\")\nprint(\"-\" * 60)\nalerts = []\nif p99_lat > 1500.0: alerts.append(\"ALERT: p99 Latency exceeds 1,500ms ceiling!\")\nif saturation_pct > 80.0: alerts.append(\"ALERT: Database connection pool saturation > 80%!\")\nif error_rate > 1.0: alerts.append(\"ALERT: HTTP 5xx error rate > 1.0%!\")\n\nfor a in alerts:\n    print(f\"[TRIGGERED] {a}\")\nEOF\npython3 day-086-topic-04-golden-signals.py\n```",
                    "Execute the script and verify that average latency (445ms) completely obscures the 29,250ms p99 catastrophe.",
                    "Verify that the alert engine triggers on both p99 latency and saturation before overall error rates spike.",
                    "Save the script and analysis as exit evidence."
                ],
                "verification": (
                    "Script runs cleanly and displays accurate mathematical percentile calculations and golden signal alert evaluations."
                ),
                "trouble": "Ensure data array is sorted in ascending order before evaluating percentiles.",
                "cleanup": "Retain `day-086-topic-04-golden-signals.py` as an exit evidence artifact.",
                "accept": "Demonstrated mastery of the Four Golden Signals, percentile mathematics, and saturation monitoring."
            }
        }
    ]
}
