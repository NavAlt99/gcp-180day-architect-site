"""day_data_179.py — Specification for Day 179: Capstone 5 — Cost and reliability rescue.

Generated from template; fields filled for day 179.
"""

DAY = 179
WORK_BLOCK = "Final gate and capstone defenses"

PART1_INTRO = (
    "Today we synthesize the capstone package developed across previous days and address review findings "
    "to ensure the architecture meets cost, reliability, and correctness goals under constrained budgets. "
    "We examine existing models, incorporate reviewer feedback, and produce defensible artifacts."
)

EXIT_SUMMARY = (
    "Final before/after cost/reliability model, trade-off ADRs, adoption plan and scored review with honest uncertainty."
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
    "title": "Brightloaf Capstone Architecture & Boundary Enforcement Topology",
    "desc": "Multi-tier operational architecture showing infrastructure layers, security perimeters, and request flows for the Brightloaf retail scenario.",
    "caption": "Figure: Infrastructure layers, request flows, and boundary verification for the capstone architecture.",
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
            "During capstone review, reviewers noted that the cost model omitted sustained‑use discounts, leading to inflated projections. "
            "This gap risks budget overrun and undermines confidence in the proposed architecture."
        ),
        "overview": (
            "Define the process of synthesizing the capstone package: collecting design documents, cost models, reliability evidence, "
            "and review comments into a coherent package. Explain ownership boundaries (architecture team), the service model (internal review), "
            "and the fundamental goal of delivering a defensible, budget‑aware architecture."
        ),
        "technical": (
            "Explain control and data plane mechanics, limits, failure boundaries, and trade-offs.\n\n"
            "- **Control Plane Boundary:** Deep explanation of review process governance, document versioning, and feedback incorporation.\n"
            "- **Data Plane Path:** Packet or token evaluation path, kernel/driver behavior, latency.\n"
            "- **Failure & Recovery Dynamics:** Behavior during network splits or quota exhaustion."
        ),
        "questions": [
            "How does incorporating sustained‑use discounts affect the total cost of ownership over a three‑year horizon?",
            "What is the impact of assuming independent regional failures versus correlated outages on the calculated availability?",
            "Which trade‑offs arise when increasing model fidelity versus review turnaround time?",
        ],
        "reference": "https://docs.cloud.google.com/architecture/framework",
        "reference_label": "Google Cloud Architecture Framework Overview",

        # PART 3: Realistic Operational Incident (Day 179 specific)
        "scenario": {
            "scenario": (
                "During the capstone review, a stakeholder identified that the reliability model did not include the impact of regional outages "
                "on the multi‑region failover path, potentially overstating availability. The model assumed independent regional failures."
            ),
            "symptom": (
                "The reliability score showed 99.99% annual availability, but the model ignored regional failure correlation, "
                "leading to an overstated availability metric."
            ),
            "impact": (
                "If a regional outage occurs, the actual availability could drop to 99.9%, violating the SLO and causing potential breach of customer commitments. "
                "Financial penalties and loss of trust could result."
            ),
            "constraints": (
                "Must use only publicly available SLO values from Google Cloud documentation; cannot assume unpublished internal metrics; "
                "must keep the model understandable to non‑technical stakeholders."
            ),
            # MANDATORY: Verbatim error logs, terminal transcripts, or JSON payloads
            "evidence": (
                "Reviewer comment captured in the capstone review document:\n\n"
                "> \"The reliability model treats regional failures as independent, which is unrealistic given shared infrastructure risks. "
                "Please update the model to reflect correlated failure probabilities using Google's published outage data.\"\n\n"
                "Excerpt from the original reliability_model.txt showing the assumption:\n\n"
                "```\n"
                "availability = 1 - ( (1 - regional_a) * (1 - regional_b) * (1 - regional_c) )\n"
                "# where regional_a, b, c are the availability of three regions\n"
                "```"
            ),
            "root": (
                "The reliability model assumed independent regional failures, whereas regional outages can be correlated due to shared underlying infrastructure "
                "(e.g., fiber cuts, power events). This assumption led to an inflated availability estimate."
            ),
            "diagnostic_steps": [
                "Step 1: Review Google's published regional outage statistics (e.g., from the Architecture Framework) to understand correlation factors.\n"
                "Step 2: Extract the current reliability model from the capstone package.\n"
                "Step 3: Calculate the joint probability of simultaneous regional outages using the published correlation coefficient.\n"
                "Step 4: Update the availability formula to include the correlation term.\n"
                "Step 5: Document the change in an Architecture Decision Record (ADR)."
            ],
            "fix": (
                "Tactical Fix: Immediately update the reliability model to include a correlation factor derived from Google's published regional outage statistics.\n\n"
                "Strategic Fix: Author an ADR that documents the assumption change, the source of the correlation data, and the impact on the availability calculation. "
                "Ensure all future reliability analyses use this updated model."
            ),
            "verify": (
                "Run the updated model with the correlation factor and compare the result to the baseline. "
                "Confirm that the revised availability aligns with documented regional SLOs when correlation is considered. "
                "Check that the ADR is correctly linked in the capstone package and that the change is version‑controlled."
            ),
            "residual": (
                "Even with correlation, the model cannot predict black‑swan events that affect multiple regions simultaneously (e.g., global software bugs). "
                "Such events remain outside the statistical baseline and should be addressed via operational readiness reviews."
            ),
            # 5-node flow for Incident SVG
            "diagram": (
                "Reviewer examines reliability model",
                "Assumes independent regional failures",
                "Overstated availability metric",
                "Consults GCP outage docs, adds correlation factor",
                "Revised reliability model with realistic availability"
            )
        },

        # PART 4: Exactly 8 topic-adapted execution stages; acceptance follows the stage list.
        "lab": {
            "name": "Validate and Update the Capstone Cost/Reliability Model",
            "file": "day-179-topic-01.md",
            "goal": (
                "Ensure the capstone package includes a defensible cost/reliability model that accounts for regional outage correlation "
                "and sustained‑use discounts, and produce an updated ADR documenting the change."
            ),
            "expected": (
                "An updated cost model spreadsheet and reliability model text file that incorporate sustained‑use discounts and regional correlation, "
                "accompanied by a signed‑off ADR. All changes are verified and the capstone package passes internal review."
            ),
            "mode": "Local/tabletop analysis using spreadsheet software or text files.",
            "prereq": "Prior day exit artifacts (capstone package), spreadsheet software or text editor, access to Google Cloud public documentation.",
            "preflight": (
                "Verify that the capstone package directory contains the files `cost_model.xlsx`, `reliability_model.txt`, and `ADR-001.md`. "
                "Confirm you have read/write access to these files."
            ),
            "steps": [
                (
                    "**Stage 1: Preflight & Environment Validation**\n"
                    "- List the files in the capstone package directory to confirm presence of required artifacts.\n"
                    "- Check that the spreadsheet and text files are not locked or corrupted.\n\n"
                    "```sh\n"
                    "ls -la capstone-package/\n"
                    "```"
                ),
                (
                    "**Stage 2: Prepare Target, Inputs, or Backing Resources**\n"
                    "- Copy the cost and reliability models to a working directory to avoid altering the originals until verification.\n"
                    "- Retrieve the latest Google Cloud SLO and outage documentation from the public docs.\n\n"
                    "```sh\n"
                    "mkdir -p capstone-package/working\n"
                    "cp capstone-package/cost_model.xlsx capstone-package/working/\n"
                    "cp capstone-package/reliability_model.txt capstone-package/working/\n"
                    "```"
                ),
                (
                    "**Stage 3: Author the Plan, Configuration, or Analysis**\n"
                    "- Open the cost model and identify where sustained‑use discounts should be applied (typically a multiplier on compute hours).\n"
                    "- Open the reliability model and locate the availability formula; note the assumption of independent regional failures.\n"
                    "- Determine the correlation factor to use from Google's published outage statistics (e.g., 0.3 for correlated failures).\n\n"
                    "```sh\n"
                    "# No commands needed; this stage is analytical.\n"
                    "echo 'Plan: Update cost model with sustained‑use discount factor of 0.85 for committed use.'\n"
                    "echo 'Plan: Update reliability model with regional correlation factor of 0.3.'\n"
                    "```"
                ),
                (
                    "**Stage 4: Execute or Simulate the Planned Work**\n"
                    "- Edit the cost model to apply the sustained‑use discount factor to the relevant line items.\n"
                    "- Edit the reliability model to replace the independent failure formula with a correlated version.\n\n"
                    "```sh\n"
                    "# Example: edit cost model (assuming you have a tool like ssconvert or use LibreOffice in headless mode; for tabletop, edit manually)\n"
                    "# For tabletop, we will just note the change.\n"
                    "echo 'Updated cost_model.xlsx: applied sustained‑use discount factor 0.85 to compute lines.'\n"
                    "echo 'Updated reliability_model.txt: new formula:'\n"
                    "echo 'availability = 1 - ( (1 - regional_a) * (1 - regional_b) * (1 - regional_c) * (1 - correlation) )'\n"
                    "```"
                ),
                (
                    "**Stage 5: Inspect Expected State & Verify Outcomes**\n"
                    "- Re‑calculate the total cost using the updated cost model; verify that the cost decreases by the expected discount.\n"
                    "- Re‑calculate availability using the updated reliability model; verify that the number is lower than the previous over‑estimate but still meets the SLO when correlation is considered.\n"
                    "- Document the new values.\n\n"
                    "```sh\n"
                    "# Tabletop calculation example\n"
                    "echo 'Old cost: $100,000/year'\n"
                    "echo 'New cost (with 0.85 factor): $85,000/year'\n"
                    "echo 'Old availability (independent): 99.99%'\n"
                    "echo 'New availability (correlated 0.3): 99.9%'\n"
                    "```"
                ),
                (
                    "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge**\n"
                    "- Introduce a deliberate error: forget to save the edited reliability model and verify that version control detects the change.\n"
                    "- Or test an extreme correlation factor (e.g., 0.9) to see the impact on availability and discuss whether it is realistic.\n\n"
                    "```sh\n"
                    "# Simulate forgetting to save\n"
                    "echo 'If we do not save the edited file, the model retains the old assumption, leading to over‑optimistic availability.'\n"
                    "# Test extreme correlation\n"
                    "echo 'With correlation factor 0.9, availability drops to 99.0%, prompting review of whether such correlation is plausible.'\n"
                    "```"
                ),
                (
                    "**Stage 7: Diagnose Evidence & Record Remediation/Decision**\n"
                    "- Verify that the edited files contain the expected changes.\n"
                    "- Update the ADR to document the change in assumptions, the source of the correlation data, and the impact on the model.\n"
                    "- Sign off the ADR.\n\n"
                    "```sh\n"
                    "# Check the updated reliability model\n"
                    "grep -n 'correlation' capstone-package/working/reliability_model.txt\n"
                    "# Update ADR (example)\n"
                    "echo 'ADR-002: Updated reliability model to include regional correlation factor' >> capstone-package/ADR-002.md\n"
                    "```"
                ),
                (
                    "**Stage 8: Cleanup or Exercise Closeout**\n"
                    "- Replace the original files in the capstone package with the verified updated versions.\n"
                    "- Remove any temporary working files.\n"
                    "- Ensure no credentials or sensitive data remain in the working directory.\n\n"
                    "```sh\n"
                    "cp capstone-package/working/cost_model.xlsx capstone-package/\n"
                    "cp capstone-package/working/reliability_model.txt capstone-package/\n"
                    "rm -rf capstone-package/working\n"
                    "echo 'Cleanup complete. Capstone package now reflects updated cost and reliability models.'\n"
                    "```"
                ),
            ],
            "verification": (
                "The cost model shows a reduced total cost reflecting sustained‑use discounts, and the reliability model yields a realistic availability "
                "that accounts for regional correlation. The updated ADR is present and signed off."
            ),
            "trouble": (
                "If the cost model does not reflect the discount, verify that the factor was applied to the correct rows and that the spreadsheet formulas are correct. "
                "If the reliability model still shows the independent failure formula, check that the edit was saved and that the file being read is the updated one."
            ),
            "cleanup": (
                "Removing the working directory eliminates temporary files and reduces the risk of accidentally using outdated models. "
                "The capstone package remains the single source of truth for the final review."
            ),
            "accept": (
                "Save the verified execution record for the topic exit artifact, including the updated cost and reliability model files, the signed‑off ADR, "
                "and a note that the changes have been verified and are ready for the capstone defense."
            )
        }
    }
]

