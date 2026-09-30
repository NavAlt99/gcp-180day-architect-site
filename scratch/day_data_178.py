"""day_data_178.py — Specification for Day 178: Capstone 4 — Migration defense.

Generated from template; fields filled for day 178.
"""

DAY = 178
WORK_BLOCK = "Final gate and capstone defenses"

PART1_INTRO = (
    "Today we synthesize the capstone package developed across previous days and address review findings "
    "to ensure the migration architecture is sound, with clear ownership, acceptance criteria, and decommissioning plans. "
    "We examine existing models, incorporate reviewer feedback, and produce defensible artifacts for the migration capstone."
)

EXIT_SUMMARY = (
    "Final migration package with measurable acceptance, source/target invariants, owners and decommissioning criteria."
)

# Optional comparison/architecture table in Part 2
ARCH_TABLE_HTML = """
<table>
<caption>Enterprise Architectural Comparison and Trade-offs</caption>
<thead>
<tr>
  <th scope="col">Design Option / Strategy</th>
  <th scope="col">Google Cloud Implementation</th>
  <th scope="col">Data Plane & Control Plane Boundary</th>
  <th scope="col">Primary Advantage</th>
  <th scope="col">Trade-off & Failure Blast Radius</th>
</tr>
</thead>
<tbody>
<tr>
  <th scope="row">Pattern A</th>
  <td>Cloud Armor + Managed Protection Plus + Global External ALB</td>
  <td>Edge Envoy proxy layer with anycast routing</td>
  <td>Sub-second DDoS mitigation before traffic reaches backend VPC</td>
  <td>Increased ingress egress billing; false-positive rate tuning overhead</td>
</tr>
<tr>
  <th scope="row">Pattern B</th>
  <td>PSC Service Attachments + Regional Internal ALBs</td>
  <td>Direct SDN encapsulation across VPC boundaries</td>
  <td>Zero public IP exposure, strict IAM consumer accept policies</td>
  <td>Transitive routing limitations; requires dedicated NAT subnet planning</td>
</tr>
</tbody>
</table>
"""

# Architecture Diagram for Part 2 (Day 121 topology standard)
ARCH_DIAGRAM = {
    "type": "topology",
    "title": "Brightloaf Migration Architecture & Boundary Enforcement Topology",
    "desc": "Multi-tier operational architecture showing infrastructure layers, security perimeters, and request flows for the Brightloaf migration scenario.",
    "caption": "Figure: Infrastructure layers, request flows, and boundary verification for the migration architecture.",
    "width": 1120,
    "height": 690,
    "layers": [
        {"name": "INGRESS / DEMAND & INPUTS", "desc": "requests · identities · workloads · policies", "x": 20, "y": 55, "w": 1080, "h": 92, "fill": "#1e3a5f", "title_color": "#7dd3fc"},
        {"name": "MANAGED RUNTIME & DATA PLANE", "desc": "sandboxed compute · service mesh · persistence tier", "x": 20, "y": 185, "w": 1080, "h": 210, "fill": "#064e3b", "title_color": "#6ee7b7"},
        {"name": "GOVERNANCE, AUDIT & POLICY DECISION", "desc": "immutable audit vault · telemetry · admission control", "x": 20, "y": 435, "w": 1080, "h": 115, "fill": "#422006", "title_color": "#fdba74"},
    ],
    "components": [
        # Tier 1 Components (Ingress & Demand)
        {"x": 55, "y": 88, "w": 180, "h": 45, "name": "Client Ingress", "detail": "TLS 1.3 · Anycast ALB", "stroke": "#38bdf8"},
        {"x": 320, "y": 88, "w": 180, "h": 45, "name": "Identity Boundary", "detail": "OIDC · Workload Identity", "stroke": "#38bdf8"},
        {"x": 585, "y": 88, "w": 205, "h": 45, "name": "Workload Dispatch", "detail": "Rate limiting · Concurrency", "stroke": "#38bdf8"},
        {"x": 855, "y": 88, "w": 205, "h": 45, "name": "Regional Context", "detail": "Residency · Quotas", "stroke": "#38bdf8"},
        # Tier 2 Components - Row 1 (Core Services & Platform)
        {"x": 55, "y": 220, "w": 215, "h": 65, "name": "Cloud Run Services", "detail": "Scale-to-zero · Sandboxed", "stroke": "#22c55e"},
        {"x": 330, "y": 220, "w": 215, "h": 65, "name": "GKE Microservices", "detail": "Autopilot · Pod Packing", "stroke": "#22c55e"},
        {"x": 610, "y": 220, "w": 205, "h": 65, "name": "Database Tier", "detail": "Cloud SQL / Spanner HA", "stroke": "#22c55e"},
        {"x": 860, "y": 220, "w": 200, "h": 65, "name": "Analytics Engine", "detail": "BigQuery · Partitioned", "stroke": "#22c55e"},
        # Tier 2 Components - Row 2 (Telemetry & Security State)
        {"x": 170, "y": 320, "w": 250, "h": 52, "name": "Telemetry & Observability", "detail": "Cloud Logging · Trace · Metrics", "stroke": "#f59e0b"},
        {"x": 590, "y": 320, "w": 290, "h": 52, "name": "Security & Cost Accounting", "detail": "KMS · Cloud Armor · FinOps Scope", "stroke": "#f59e0b"},
        # Tier 3 Components (Policy & Decision Guardrails)
        {"x": 220, "y": 468, "w": 280, "h": 58, "name": "Policy & Decision Matrix", "detail": "Org Policies · IAM Invariants", "stroke": "#fdba74"},
        {"x": 620, "y": 468, "w": 280, "h": 58, "name": "Enforced Verification Gate", "detail": "SLO · Automated Rollback", "stroke": "#fdba74"},
    ],
    "flows": [
        # Tier 1 Horizontal Transitions
        {"x1": 235, "y1": 110, "x2": 320, "y2": 110, "label": "auth", "type": "ok"},
        {"x1": 500, "y1": 110, "x2": 585, "y2": 110, "label": "dispatch", "type": "ok"},
        {"x1": 790, "y1": 110, "x2": 855, "y2": 110, "label": "scope", "type": "ok"},
        # Tier 1 to Tier 2 Exact Vertical Drops (x1 == x2)
        {"x1": 145, "y1": 133, "x2": 145, "y2": 220, "label": "HTTP traffic", "type": "ok"},
        {"x1": 415, "y1": 133, "x2": 415, "y2": 220, "label": "gRPC / mTLS", "type": "ok"},
        {"x1": 710, "y1": 133, "x2": 710, "y2": 220, "label": "SQL queries", "type": "ok"},
        {"x1": 960, "y1": 133, "x2": 960, "y2": 220, "label": "sync stream", "type": "warn"},
        # Tier 2 Internal Routing
        {"x1": 270, "y1": 252, "x2": 330, "y2": 252, "label": "egress", "type": "ok"},
        {"x1": 545, "y1": 252, "x2": 610, "y2": 252, "label": "persist", "type": "ok"},
        {"x1": 415, "y1": 285, "x2": 295, "y2": 320, "label": "traces", "type": "warn"},
        {"x1": 710, "y1": 285, "x2": 735, "y2": 320, "label": "audit log", "type": "ok"},
        {"x1": 420, "y1": 346, "x2": 590, "y2": 346, "label": "reconcile", "type": "ok"},
        # Tier 2 to Tier 3 Flow
        {"x1": 735, "y1": 372, "x2": 735, "y2": 468, "label": "verified audit", "type": "ok"},
        {"x1": 500, "y1": 497, "x2": 620, "y2": 497, "label": "enforce gate", "type": "ok"},
    ],
    "boundaries": [
        {"x": 35, "y": 425, "w": 1045, "h": 135, "label": "VERIFICATION BOUNDARY · INVARIANTS & POLICY GATES ENFORCED", "color": "#f59e0b"},
    ],
    "probes": [
        {"cx": 258, "cy": 233, "label": "P1: Ingress Rate & Concurrency Gate", "color": "#38bdf8"},
        {"cx": 858, "cy": 263, "label": "P2: Audit Log & Telemetry Verification", "color": "#22c55e"},
        {"cx": 1040, "cy": 133, "label": "P3: Organization Policy / Residency Check", "color": "#f59e0b"},
    ],
}

# Standard 1:1 Topics Definition
TOPICS = [
    {
        "key": "topic-01",
        "title": "Synthesize the existing capstone package and address review findings",
        "preview": (
            "During the migration capstone review, reviewers noted that the decommissioning criteria were vague, creating uncertainty about when to shut down legacy systems. "
            "This ambiguity risks unnecessary costs and potential security gaps from orphaned resources."
        ),
        "overview": (
            "Define the process of synthesizing the capstone package: collecting design documents, migration wave plans, cutover procedures, and review comments into a coherent package. "
            "Explain ownership boundaries (migration team), the service model (internal review), and the fundamental goal of delivering a defensible migration package with clear acceptance criteria."
        ),
        "technical": (
            "Explain control and data plane mechanics, limits, failure boundaries, and trade-offs.\n\n"
            "- **Control Plane Boundary:** Deep explanation of migration governance, versioning of runbooks, and feedback incorporation.\n"
            "- **Data Plane Path:** Packet or token evaluation path, kernel/driver behavior, latency.\n"
            "- **Failure & Recovery Dynamics:** Behavior during network splits or quota exhaustion."
        ),
        "questions": [
            "How do measurable acceptance criteria reduce uncertainty in migration cutover decisions?",
            "What is the impact of vague decommissioning criteria on operational costs and security posture?",
            "Which trade‑offs arise when increasing model fidelity versus review turnaround time?",
        ],
        "reference": "https://docs.cloud.google.com/architecture/framework",
        "reference_label": "Google Cloud Architecture Framework Overview",

        # PART 3: Realistic Operational Incident (Day 178 specific)
        "scenario": {
            "scenario": (
                "During the capstone review, a stakeholder identified that the decommissioning criteria in the migration package were based on arbitrary time intervals rather than measurable business or technical signals, "
                "leading to potential premature or delayed shutdown of legacy systems."
            ),
            "symptom": (
                "The migration package stated \"Decommission legacy systems 30 days after cutover\" without linking to measurable outcomes like transaction volume, error rates, or cost savings. "
                "This could result in shutting down systems still handling 5% of traffic or keeping idle systems running unnecessarily."
            ),
            "impact": (
                "Premature decommissioning could cause transaction failures and revenue loss, while delayed decommissioning incurs unnecessary infrastructure costs and security risks from unpatched legacy systems. "
                "Financial impact could range from thousands to hundreds of thousands of dollars depending on the scale."
            ),
            "constraints": (
                "Must use only observable, measurable signals from the system (e.g., transaction counts, error rates, latency) for decommissioning decisions; "
                "cannot rely on arbitrary time intervals; must keep the criteria understandable to business stakeholders."
            ),
            # MANDATORY: Verbatim error logs, terminal transcripts, or JSON payloads
            "evidence": (
                "Reviewer comment captured in the capstone review document:\n\n"
                "> \"The decommissioning criteria should be based on measurable business outcomes, not fixed time periods. "
                "Please define clear, quantifiable metrics for when it is safe to shut down each legacy system.\"\n\n"
                "Excerpt from the original migration_package.txt showing the vague criteria:\n\n"
                "```\n"
                "Decommissioning Criteria:\n"
                "- Wait 30 days after cutover to each wave\n"
                "- Then shut down the corresponding legacy system\n"
                "```"
            ),
            "root": (
                "The decommissioning criteria used arbitrary time intervals instead of observable system behavior, "
                "leading to a disconnect between the migration timeline and actual system readiness for decommissioning."
            ),
            "diagnostic_steps": [
                "Step 1: Review the migration package to identify all legacy systems and their associated cutover waves.\n"
                "Step 2: For each legacy system, determine the key business and technical signals that indicate it is no longer needed (e.g., zero transactions, error rates below threshold, cost savings realized).\n"
                "Step 3: Define measurable decommissioning criteria for each system based on those signals.\n"
                "Step 4: Update the migration package with the new criteria and create an Architecture Decision Record (ADR) documenting the change.\n"
                "Step 5: Verify that the criteria are observable and measurable in the production environment."
            ],
            "fix": (
                "Tactical Fix: Immediately update the migration package to replace time-based decommissioning criteria with measurable signals (e.g., \"Decommission when daily transaction count falls below 10 for 7 consecutive days\").\n\n"
                "Strategic Fix: Author an ADR that documents the assumption change, the source of the measurable signals, and the impact on the decommissioning timeline. "
                "Ensure all future migration analyses use this outcomes-based approach."
            ),
            "verify": (
                "Run the updated decommissioning criteria against historical data (if available) or simulate with expected traffic patterns to confirm they produce reasonable timelines. "
                "Confirm that the ADR is correctly linked in the migration package and that the change is version‑controlled. "
                "Check that the criteria are specific, measurable, achievable, relevant, and time-bound (SMART)."
            ),
            "residual": (
                "Even with measurable criteria, external factors (e.g., sudden regulatory changes) could necessitate earlier or later decommissioning. "
                "Such events should be handled via exception processes documented in the migration runbook."
            ),
            # 5-node flow for Incident SVG
            "diagram": (
                "Reviewer examines decommissioning criteria",
                "Criteria based on fixed 30-day interval",
                "Risk of premature or delayed decommissioning",
                "Replace with measurable signals (transaction count, error rate)",
                "Decommissioning triggered by observable system state"
            )
        },

        # PART 4: Exactly 8 topic-adapted execution stages; acceptance follows the stage list.
        "lab": {
            "name": "Define Measurable Decommissioning Criteria for Legacy Systems",
            "file": "day-178-topic-01.md",
            "goal": (
                "Ensure the migration package includes observable, measurable decommissioning criteria for each legacy system based on business and technical signals, "
                "and produce an updated ADR documenting the change."
            ),
            "expected": (
                "An updated migration package text file with specific decommissioning criteria for each legacy system, "
                "accompanied by a signed‑off ADR. All changes are verified and the migration package passes internal review."
            ),
            "mode": "Local/tabletop analysis using text files or simple spreadsheets.",
            "prereq": "Prior day exit artifacts (migration package), text editor or spreadsheet software, access to Google Cloud public documentation.",
            "preflight": (
                "Verify that the migration package directory contains the file `migration_package.txt`. "
                "Confirm you have read/write access to this file."
            ),
            "steps": [
                (
                    "**Stage 1: Preflight & Environment Validation**\n"
                    "- List the files in the migration package directory to confirm presence of required artifacts.\n"
                    "- Check that the text file is not locked or corrupted.\n\n"
                    "```sh\n"
                    "ls -la migration-package/\n"
                    "```"
                ),
                (
                    "**Stage 2: Prepare Target, Inputs, or Backing Resources**\n"
                    "- Copy the migration package to a working directory to avoid altering the original until verification.\n"
                    "- Identify the legacy systems mentioned in the package and the signals that could indicate readiness for decommissioning.\n\n"
                    "```sh\n"
                    "mkdir -p migration-package/working\n"
                    "cp migration-package/migration_package.txt migration-package/working/\n"
                    "```"
                ),
                (
                    "**Stage 3: Author the Plan, Configuration, or Analysis**\n"
                    "- Open the migration package and locate the decommissioning criteria section.\n"
                    "- For each legacy system, determine the appropriate measurable signal (e.g., transaction count, error rate, latency, cost).\n"
                    "- Define a threshold for each signal that indicates it is safe to decommission.\n\n"
                    "```sh\n"
                    "# No commands needed; this stage is analytical.\n"
                    "echo 'Plan: For Order Management System, decommission when daily transaction count < 10 for 7 days.'\n"
                    "echo 'Plan: For Inventory System, decommission when error rate < 0.1% for 14 days.'\n"
                    "```"
                ),
                (
                    "**Stage 4: Execute or Simulate the Planned Work**\n"
                    "- Edit the migration package to replace the time-based criteria with signal-based criteria for each legacy system.\n\n"
                    "```sh\n"
                    "# Example: edit migration package (for tabletop, we will just note the change)\n"
                    "echo 'Updated migration_package.txt:'\n"
                    "echo '  Order Management System: Decommission when daily transaction count < 10 for 7 consecutive days'\n"
                    "echo '  Inventory System: Decommission when error rate < 0.1% for 14 consecutive days'\n"
                    "echo '  Customer Database: Decommission when storage cost savings realized > 90% of projected'\n"
                    "```"
                ),
                (
                    "**Stage 5: Inspect Expected State & Verify Outcomes**\n"
                    "- Verify that the edited migration package contains the new criteria and that they are specific and measurable.\n"
                    "- Check that the criteria are linked to observable system metrics.\n\n"
                    "```sh\n"
                    "# Tabletop verification\n"
                    "echo 'Verified: Order Management System criteria based on transaction count'\n"
                    "echo 'Verified: Inventory System criteria based on error rate'\n"
                    "echo 'Verified: Criteria are specific and measurable'\n"
                    "```"
                ),
                (
                    "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge**\n"
                    "- Introduce a deliberate error: use a signal that is not observable (e.g., \"employee satisfaction\") and verify that the team questions its validity.\n"
                    "- Or test an extreme threshold (e.g., decommission when transaction count < 1000000) to see if it is obviously wrong.\n\n"
                    "```sh\n"
                    "# Simulate using non-observable signal\n"
                    "echo 'If we use \"employee happiness\" as a signal, we cannot measure it objectively, so the criterion is invalid.'\n"
                    "# Test extreme threshold\n"
                    "echo 'If we set decommissioning at < 1000000 transactions/day, we might never decommission if traffic is high.'\n"
                    "```"
                ),
                (
                    "**Stage 7: Diagnose Evidence & Record Remediation/Decision**\n"
                    "- Verify that the edited files contain the expected changes.\n"
                    "- Update the ADR to document the change in assumptions, the source of the measurable signals, and the impact on the decommissioning timeline.\n"
                    "- Sign off the ADR.\n\n"
                    "```sh\n"
                    "# Check the updated migration package\n"
                    "grep -n 'transaction count' migration-package/working/migration_package.txt\n"
                    "# Update ADR (example)\n"
                    "echo 'ADR-002: Updated decommissioning criteria to be based on measurable signals' >> migration-package/ADR-002.md\n"
                    "```"
                ),
                (
                    "**Stage 8: Cleanup or Exercise Closeout**\n"
                    "- Replace the original file in the migration package with the verified updated version.\n"
                    "- Remove any temporary working files.\n"
                    "- Ensure no credentials or sensitive data remain in the working directory.\n\n"
                    "```sh\n"
                    "cp migration-package/working/migration_package.txt migration-package/\n"
                    "rm -rf migration-package/working\n"
                    "echo 'Cleanup complete. Migration package now reflects updated decommissioning criteria.'\n"
                    "```"
                ),
            ],
            "verification": (
                "The migration package shows specific, measurable decommissioning criteria for each legacy system based on observable signals, "
                "and the updated ADR is present and signed off."
            ),
            "trouble": (
                "If the criteria are still time-based, verify that the edit was saved and that the file being read is the updated one. "
                "If a criterion is not measurable, revisit the signal selection and ensure it can be observed from system metrics."
            ),
            "cleanup": (
                "Removing the working directory eliminates temporary files and reduces the risk of accidentally using outdated criteria. "
                "The migration package remains the single source of truth for the final review."
            ),
            "accept": (
                "Save the verified execution record for the topic exit artifact, including the updated migration package file, the signed‑off ADR, "
                "and a note that the changes have been verified and are ready for the capstone defense."
            )
        }
    }
]

