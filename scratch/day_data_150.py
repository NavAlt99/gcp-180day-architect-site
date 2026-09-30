"""day_data_150.py — Specification for Day 150: Discovery: data, regulation and skills.

Generated from template; fields filled for day 150.
"""

DAY = 150
WORK_BLOCK = "Discovery, cases and exam preparation"

PART1_INTRO = (
    "Today we focus on discovery activities for architecture planning: understanding user locations, "
    "data residency requirements, applicable regulations and audits, existing system integrations, "
    "and team skills assessment. These inputs constrain and shape the eventual architecture."
)

EXIT_SUMMARY = (
    "A constraint/skills matrix and a mitigation or simpler alternative for each gap."
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
    "title": "Brightloaf Discovery Architecture & Boundary Enforcement Topology",
    "desc": "Multi-tier operational architecture showing infrastructure layers, security perimeters, and request flows for the Brightloaf discovery scenario.",
    "caption": "Figure: Infrastructure layers, request flows, and boundary verification for the discovery architecture.",
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
        "title": "Where are users, and where must data legally reside?",
        "preview": (
            "Users are concentrated in urban areas across North America and Europe, but data residency laws require "
            "personal data to remain within national borders in countries like Germany and Canada. "
            "This creates a tension between serving users locally and complying with data localization requirements."
        ),
        "overview": (
            "Define the challenge of user distribution versus data residency requirements. "
            "Explain how user location affects latency and experience, while data sovereignty laws (like GDPR, "
            "data localization laws) restrict where personal data can be stored and processed. "
            "Describe the ownership boundary (typically legal/compliance team) and the service model "
            "(mapping user locations to compliant data regions)."
        ),
        "technical": (
            "Explain control and data plane mechanics, limits, failure boundaries, and trade-offs.\n\n"
            "- **Control Plane Boundary:** Deep explanation of how data residency policies are configured in cloud "
            "services (e.g., resource location constraints, organization policies) and how they propagate to "
            "data storage and processing services.\n"
            "- **Data Plane Path:** How user requests are routed to appropriate regions based on residency "
            "requirements, including any latency implications from detours to compliant regions.\n"
            "- **Failure & Recovery Dynamics:** How data residency constraints affect disaster recovery options "
            "and backup/restore procedures when compliant regions experience outages."
        ),
        "questions": [
            "How does requiring data to reside in the same country as users affect cross-border user experiences?",
            "What techniques exist to minimize latency when data must be stored in specific geographic locations?",
            "How do you handle situations where a user travels between jurisdictions with different data laws?",
        ],
        "reference": "https://docs.cloud.google.com/architecture/framework",
        "reference_label": "Google Cloud Architecture Framework Overview",

        # PART 3: Realistic Operational Incident (Day 150 specific)
        "scenario": {
            "scenario": (
                "During discovery for a European expansion, the architecture team proposed a single central "
                "database in us-central1 to serve all global users for simplicity, not realizing that EU GDPR "
                "requires personal data of EU residents to remain within the EU unless adequate protections exist."
            ),
            "symptom": (
                "Legal team flagged the architecture during review, noting that storing EU customer data in "
                "US regions without appropriate safeguards (like Standard Contractual Clauses) violates GDPR "
                "Chapter V on data transfers, potentially resulting in fines up to 4% of global revenue."
            ),
            "impact": (
                "Non-compliance could lead to significant financial penalties, mandatory data deletion, "
                "and reputational damage. Fixing the issue after deployment would require costly data migration "
                "and potential service downtime during the move to EU-based storage."
            ),
            "constraints": (
                "Must comply with GDPR and other applicable data protection laws; cannot process EU personal "
                "data outside approved jurisdictions without adequate safeguards; solution must maintain "
                "acceptable latency for users in all served regions."
            ),
            # MANDATORY: Verbatim error logs, terminal transcripts, or JSON payloads
            "evidence": (
                "Legal review comment captured in the discovery document:\n\n"
                "> \"Storing EU personal data in US regions without GDPR-compliant transfer mechanisms "
                "violates Article 44-49 of GDPR. Either move data to EU regions or implement appropriate "
                "safeguards like Standard Contractual Clauses or Binding Corporate Rules.\"\n\n"
                "Screenshot of the initial architecture diagram showing single region deployment:\n\n"
                "```\n"
                "[Users Worldwide] --> [Central DB: us-central1]\n"
                "```\n\n"
                "And the corrected version showing regional separation:\n\n"
                "```\n"
                "[EU Users] --> [DB: europe-west1/2/3]\n"
                "[US Users] --> [DB: us-central1/us-east1/us-east4]\n"
                "[Asia Users] --> [DB: asia-east1/asia-southeast1]\n"
                "```"
            ),
            "root": (
                "The team overlooked data residency requirements during initial architecture brainstorming, "
                "focusing only on technical simplicity and performance without considering legal constraints "
                "on where data can physically reside."
            ),
            "diagnostic_steps": [
                "Step 1: Identify all user geographies and corresponding data residency requirements.\n"
                "Step 2: Map data types to their respective legal restrictions (PII, financial data, health data, etc.).\n"
                "Step 3: For each user geography, determine compliant Google Cloud regions where data can be stored.\n"
                "Step 4: Design a regionalized architecture that places data in compliant locations closest to users.\n"
                "Step 5: Evaluate latency and consistency trade-offs of the distributed approach."
            ],
            "fix": (
                "Tactical Fix: Immediately update the architecture to deploy separate database instances in "
                "GDPR-compliant European regions (europe-west1-3) for EU user data, while maintaining US "
                "instances for non-EU data.\n\n"
                "Strategic Fix: Implement a data residency policy as code using Organization Policy Service "
                "to restrict resource locations based on data classification tags, preventing future violations."
            ),
            "verify": (
                "Confirm that all EU user data is now stored only in europe-west* regions via resource "
                "location audits. Verify that the Organization Policy is correctly enforced by attempting to "
                "create a non-compliant resource and observing the rejection. Check latency measurements "
                "for EU users to ensure they remain within acceptable bounds."
            ),
            "residual": (
                "Even with regional data storage, cross-border data transfers may still occur for analytics "
                "or backup purposes, requiring ongoing legal review. Additionally, emerging regulations "
                "like data localization laws in countries such as Russia and China may impose stricter "
                "requirements over time."
            ),
            # 5-node flow for Incident SVG
            "diagram": (
                "Team proposes single-region database for simplicity",
                "Legal review identifies GDPR violation for EU data",
                "Risk of fines and forced data deletion",
                "Redesign with regional data storage in compliant locations",
                "Architecture adheres to data residency requirements"
            )
        },

        # PART 4: Exactly 8 topic-adapted execution stages; acceptance follows the stage list.
        "lab": {
            "name": "Map User Locations to Data Residency Requirements",
            "file": "day-150-topic-01.md",
            "goal": (
                "Create a mapping of user locations to compliant data storage regions based on applicable "
                "data residency laws and regulations, identifying any gaps where user experience may suffer "
                "due to compliance requirements."
            ),
            "expected": (
                "A documented matrix showing user regions, data types, applicable regulations, compliant "
                "Google Cloud regions, and any identified gaps requiring mitigation strategies."
            ),
            "mode": "Local/tabletop analysis using spreadsheet software or text files.",
            "prereq": "Prior day exit artifacts, spreadsheet software or text editor, access to Google Cloud "
                      "region documentation and data residency requirement references.",
            "preflight": (
                "Verify access to Google Cloud region documentation (https://cloud.google.com/about/locations) "
                "and data residency requirement sources (e.g., GDPR text, local data protection laws)."
            ),
            "steps": [
                (
                    "**Stage 1: Preflight & Environment Validation**\n"
                    "- Gather reference materials on user locations, data types, and applicable regulations.\n"
                    "- Identify the Google Cloud regions available for data storage and processing.\n\n"
                    "```sh\n"
                    "# No commands needed; this stage is preparatory.\n"
                    "echo 'Gathering user location data, data type classifications, and regulation references'\n"
                    "echo 'Checking available Google Cloud regions for deployment'\n"
                    "```"
                ),
                (
                    "**Stage 2: Prepare Target, Inputs, or Backing Resources**\n"
                    "- Create a working spreadsheet or text file to map user locations to compliant regions.\n"
                    "- List all significant user geographies and the types of data they generate.\n\n"
                    "```sh\n"
                    "mkdir -p discovery-work/working\n"
                    "echo 'User_Region,Data_Type,Applicable_Regulations,Compliant_GCP_Regions,Notes' > discovery-work/working/matrix.csv\n"
                    "```"
                ),
                (
                    "**Stage 3: Author the Plan, Configuration, or Analysis**\n"
                    "- For each user region and data type combination, research applicable data residency laws.\n"
                    "- Determine which Google Cloud regions satisfy those requirements.\n"
                    "- Document any gaps where no compliant region offers low latency to users.\n\n"
                    "```sh\n"
                    "# No commands needed; this stage is analytical.\n"
                    "echo 'Analyzing: EU users + Personal Data -> GDPR -> Compliant: europe-west1-3'\n"
                    "echo 'Analyzing: CA users + Personal Data -> CCPA/CPRA -> Compliant: us-west1-4, etc.'\n"
                    "echo 'Analyzing: BR users + Personal Data -> LGPD -> Compliant: southamerica-east1'\n"
                    "```"
                ),
                (
                    "**Stage 4: Execute or Simulate the Planned Work**\n"
                    "- Populate the working matrix with user regions, data types, regulations, and compliant regions.\n"
                    "- Calculate approximate latencies from user regions to compliant GCP regions.\n"
                    "- Identify any combinations where latency exceeds acceptable thresholds.\n\n"
                    "```sh\n"
                    "# Example matrix entries (for tabletop, we'll just document the additions)\n"
                    "echo 'Adding: Germany,Personal Data,GDPR,europe-west1-3 (Frankfurt),Low latency'\n"
                    "echo 'Adding: Brazil,Personal Data,LGPD,southamerica-east1 (São Paulo),Low latency'\n"
                    "echo 'Adding: India,Personal Data,PDPB,asia-south1 (Mumbai),Low latency'\n"
                    "echo 'Identifying Gap: Australia,Health Data,My Health Records->No local region,Higher latency to asia-southeast1'\n"
                    "```"
                ),
                (
                    "**Stage 5: Inspect Expected State & Verify Outcomes**\n"
                    "- Review the completed matrix for accuracy and completeness.\n"
                    "- Verify that all identified gaps are documented with potential mitigations (e.g., "
                    "edge caching, consent exceptions, or architectural alternatives).\n"
                    "- Check that the matrix aligns with the Practice activity of mapping users, data locations, integrations and operator skills.\n\n"
                    "```sh\n"
                    "# Tabletop verification\n"
                    "echo 'Verified: Matrix includes all major user regions'\n"
                    "echo 'Verified: Each entry cites specific regulation'\n"
                    "echo 'Verified: Gaps are documented with mitigation strategies'\n"
                    "```"
                ),
                (
                    "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge**\n"
                    "- Introduce a deliberate error: omit a major regulation (e.g., forget HIPAA for US health data) "
                    "and verify the impact on the compliance mapping.\n"
                    "- Or test an extreme scenario: what if all countries required data localization?\n\n"
                    "```sh\n"
                    "# Simulate missing regulation\n"
                    "echo 'If we omit HIPAA, we might incorrectly allow US health data in non-compliant regions.'\n"
                    "# Test data localization extreme\n"
                    "echo 'If every country required in-country storage, we would need many more regions or face high latency.'\n"
                    "```"
                ),
                (
                    "**Stage 7: Diagnose Evidence & Record Remediation/Decision**\n"
                    "- Verify that the matrix correctly reflects all applicable regulations for each data type.\n"
                    "- Update any incorrect entries based on further research.\n"
                    "- Document the final matrix as part of the discovery evidence.\n\n"
                    "```sh\n"
                    "# Check the matrix for completeness\n"
                    "grep -i 'hipaa' discovery-work/working/matrix.csv || echo 'HIPAA entry missing - needs addition'\n"
                    "# Finalize the matrix\n"
                    "cp discovery-work/working/matrix.csv discovery-work/final-constraint-skills-matrix.csv\n"
                    "```"
                ),
                (
                    "**Stage 8: Cleanup or Exercise Closeout**\n"
                    "- Move the final matrix to the appropriate location in the discovery evidence.\n"
                    "- Remove any temporary working files.\n"
                    "- Ensure no sensitive data remains in the working directory.\n\n"
                    "```sh\n"
                    "mkdir -p discovery-work/evidence\n"
                    "cp discovery-work/final-constraint-skills-matrix.csv discovery-work/evidence/\n"
                    "rm -rf discovery-work/working\n"
                    "echo 'Cleanup complete. Constraint/skills matrix is ready as exit evidence.'\n"
                    "```"
                ),
            ],
            "verification": (
                "The constraint/skills matrix accurately maps user locations and data types to compliant "
                "Google Cloud regions based on applicable regulations, with gaps clearly identified and "
                "mitigation strategies documented."
            ),
            "trouble": (
                "If the matrix shows non compliant regions as compliant, double-check the regulation research "
                "for that data type and region combination. If gaps are missing, re-examine the latency "
                "requirements and user experience thresholds."
            ),
            "cleanup": (
                "Removing the working directory eliminates temporary files and reduces the risk of "
                "accidentally using outdated or incomplete matrices. "
                "The final evidence remains the single source of truth for the discovery activity."
            ),
            "accept": (
                "Save the verified execution record for the topic exit artifact, including the final "
                "constraint/skills matrix in the discovery evidence folder, and a note that the matrix "
                "has been verified and is ready for inclusion in the day's exit evidence."
            )
        }
    },
    {
        "key": "topic-02",
        "title": "What regulations and audits apply?",
        "preview": (
            "Identifying applicable regulations (e.g., GDPR, HIPAA, PCI‑DSS) and audit requirements early "
            "prevents costly redesign and ensures the architecture meets legal obligations from the outset."
        ),
        "overview": (
            "This topic covers the process of discovering which laws, regulations, and audit frameworks "
            "apply to the workload based on data type, industry, and geography. It includes mapping those "
            "requirements to specific technical controls in Google Cloud."
        ),
        "technical": (
            "Explain how regulatory requirements translate into cloud configuration and controls.\n\n"
            "- **Control Plane:** Using Organization Policy, IAM conditions, and Cloud Audit Logs to enforce "
            "regulatory rules.\n"
            "- **Data Plane:** Ensuring data residency, encryption, and access controls meet specific mandates.\n"
            "- **Audit & Reporting:** Configuring Cloud Audit Logs export to meet retention and format requirements."
        ),
        "questions": [
            "How do you determine which regulatory frameworks apply to a given workload?",
            "What Google Cloud services help automate compliance evidence collection?",
            "How do you handle conflicting requirements from multiple jurisdictions?"
        ],
        "reference": "https://cloud.google.com/security/compliance",
        "reference_label": "Google Cloud Compliance",

        # PART 3: Realistic Operational Incident
        "scenario": {
            "scenario": (
                "A fintech startup assumed its payment processing workload only needed PCI‑DSS compliance, "
                "but during discovery the legal team identified that the EU‑based customers also subjected "
                "the service to GDPR and local electronic money regulations."
            ),
            "symptom": (
                "The architecture lacked data subject consent logs and could not demonstrate the right to be "
                "forgotten, triggering a compliance gap finding."
            ),
            "impact": (
                "Non‑compliance could result in fines, mandatory remediation, and loss of ability to process "
                "EU card payments."
            ),
            "constraints": (
                "Must satisfy both PCI‑DSS and GDPR without degrading transaction latency or availability."
            ),
            "evidence": (
                "Compliance checklist showing missing GDPR artifacts:\n\n"
                "```\n"
                "☑ PCI‑DSS: Encryption of cardholder data\n"
                "☐ GDPR: Data subject request handling\n"
                "☐ GDPR: Records of processing activities\n"
                "```"
            ),
            "root": (
                "The team focused on the most familiar regulation (PCI‑DSS) and omitted a systematic "
                "regional regulation scan during discovery."
            ),
            "diagnostic_steps": [
                "Step 1: Create a regulation matrix linking data types, user geography, and applicable laws.\n"
                "Step 2: Consult legal or compliance officers for each identified law.\n"
                "Step 3: Map each law to specific Google Cloud controls (e.g., Cloud KMS for encryption, "
                "Audit Logging for retention).\n"
                "Step 4: Validate the mapping with a compliance audit tool or third‑party assessor."
            ],
            "fix": (
                "Tactical Fix: Immediately add Cloud Audit Logs retention configuration and a Data Subject "
                "Request (DSR) workflow using Cloud Functions.\n\n"
                "Strategic Fix: Implement a compliance‑as‑code pipeline that runs automated checks (e.g., Forseti) "
                "against the Terraform plan before deployment."
            ),
            "verify": (
                "Confirm that audit logs are retained for the required period and that DSR requests can be "
                "fulfilled within the mandated timeframe using a test request."
            ),
            "residual": (
                "Regulations evolve; a quarterly review of the regulation matrix is necessary to stay current."
            ),
            "diagram": [
                "Team assumed only PCI‑DSS applied",
                "Discovery reveals GDPR and local e‑money rules",
                "Compliance gap flagged during legal review",
                "Add audit logs and DSR workflow",
                "Architecture satisfies both PCI‑DSS and GDPR"
            ]
        },

        # PART 4: Exactly 8 topic-adapted execution stages
        "lab": {
            "name": "Regulation and Audit Requirements Workshop",
            "file": "day-150-topic-02.md",
            "goal": (
                "Produce a regulation‑to‑control mapping matrix for the workload and identify any missing "
                "evidence artifacts needed for audit."
            ),
            "expected": (
                "A matrix listing each applicable regulation, its key requirements, the corresponding Google "
                "Cloud service or configuration, and the evidence that will be collected (logs, reports, etc.)."
            ),
            "mode": "Local/tabletop analysis using a spreadsheet or text file.",
            "prereq": "Prior day exit artifacts, access to regulation summaries (e.g., GDPR Articles, PCI‑DSS reqs).",
            "preflight": (
                "Gather official summaries or trusted third‑party guides for the regulations in scope."
            ),
            "steps": [
                "**Stage 1: Preflight & Environment Validation** - Confirm list of regulations to evaluate.",
                "**Stage 2: Prepare Target, Inputs, or Backing Resources** - Create a two‑column worksheet: Regulation | Requirement.",
                "**Stage 3: Author the Plan, Configuration, or Analysis** - For each requirement, research the Google Cloud service or setting that satisfies it.",
                "**Stage 4: Execute or Simulate the Planned Work** - Fill in the worksheet with mappings (e.g., GDPR Art. 32 → Cloud KMS + CMEK).",
                "**Stage 5: Inspect Expected State & Verify Outcomes** - Verify that each requirement has at least one mapping and note any gaps.",
                "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge** - What if a new regulation emerges mid‑project? How would you update the matrix?",
                "**Stage 7: Diagnose Evidence & Record Remediation / Decision** - Update any incorrect or incomplete mappings based on team feedback.",
                "**Stage 8: Cleanup or Exercise Closeout** - Save the final matrix as evidence and discard temporary worksheets."
            ],
            "verification": "The matrix is complete, with every regulation requirement linked to a concrete Google Cloud control or evidence artifact.",
            "trouble": "If a requirement appears unmappable, re‑examine whether it is truly a legal mandate or a sector‑specific best practice.",
            "cleanup": "Delete any temporary spreadsheets or notes; retain the final regulation‑to‑control matrix as evidence.",
            "accept": "Save the regulation matrix, a brief note on the review cadence (e.g., quarterly), and any identified gaps with mitigation plans as evidence for this topic."
        }
    },
    {
        "key": "topic-03",
        "title": "What existing systems must we integrate with?",
        "preview": (
            "Understanding current system interfaces (APIs, data formats, protocols) is essential to design "
            "a cloud architecture that connects smoothly without requiring costly custom adapters."
        ),
        "overview": (
            "This topic involves inventorying existing systems that the new architecture must interact with, "
            "documenting their APIs, data models, authentication methods, and availability constraints."
        ),
        "technical": (
            "Explain how to model integration points and choose appropriate connectivity patterns.\n\n"
            "- **Synchronous vs. Asynchronous:** Decide between REST/gRPC (sync) and Pub/Sub (async) based on latency needs.\n"
            "- **Protocol Translation:** Use Cloud API Gateway or Apigee to mediate between protocols (e.g., SOAP to REST).\n"
            "- **Data Format Mapping:** Apply Cloud Dataflow or Apigee policy to transform XML/JSON as needed.\n"
            "- **Security:** Map existing auth (e.g., LDAP, SAML) to Google Cloud IAM or Identity‑Aware Proxy."
        ),
        "questions": [
            "How do you document the interface contract of a legacy system lacking formal specifications?",
            "What factors influence the choice between a direct connection and a mediated integration layer?",
            "How do you handle systems that cannot be modified to support cloud‑native auth?"
        ],
        "reference": "https://cloud.google.com/apigateway",
        "reference_label": "Cloud API Gateway Documentation",

        # PART 3: Realistic Operational Incident
        "scenario": {
            "scenario": (
                "During discovery for a retail analytics platform, the team overlooked that the legacy "
                "inventory management system only exposes a SOAP‑based endpoint with WS‑Security authentication."
            ),
            "symptom": (
                "Initial designs assumed a REST JSON API, leading to missing integration components in the architecture."
            ),
            "impact": (
                "The gap would have required custom middleware development, increasing cost and delaying delivery."
            ),
            "constraints": (
                "Must integrate without altering the legacy system; latency for inventory queries must stay under 2 seconds."
            ),
            "evidence": (
                "Interface inventory snippet:\n\n"
                "```\n"
                "System: Legacy Inventory (on‑prem)\n"
                "Endpoint: https://inventory.example.com/ws/InventoryService\n"
                "Protocol: SOAP 1.2 over HTTPS\n"
                "Auth: WS‑Security UsernameToken\n"
                "Data Format: XML (XSD schema attached)\n"
                "```"
            ),
            "root": (
                "The team relied on a high‑level diagram from the system owner and did not perform a detailed "
                "interface discovery (e.g., WSDL retrieval, authentication handshake)."
            ),
            "diagnostic_steps": [
                "Step 1: Obtain the WSDL or equivalent interface definition from the system owner.\n"
                "Step 2: List all operations, data types, and security requirements.\n"
                "Step 3: Evaluate translation options (e.g., Apigee SOAP‑REST transformation).\n"
                "Step 4: Sketch a proof‑of‑concept mapping using Cloud API Gateway or Apigee."
            ],
            "fix": (
                "Tactical Fix: Immediately create an Apigee proxy that converts SOAP calls to REST JSON internally "
                "and maps WS‑Security tokens to Google Cloud IAM via OIDC.\n\n"
                "Strategic Fix: Implement an integration‑as‑code repository that stores API specifications (OpenAPI, AsyncAPI) "
                "and generates deployment artifacts (Apigee proxies, Cloud Functions) automatically."
            ),
            "verify": (
                "Confirm that a test inventory query returns the expected JSON payload and that latency is under 2 seconds "
                "using a load‑testing tool."
            ),
            "residual": (
                "Legacy systems may evolve; version the captured interface and schedule periodic re‑validation."
            ),
            "diagram": [
                "Team assumed REST JSON endpoint",
                "Discovery reveals legacy SOAP/WS‑Security interface",
                "Integration gap identified during technical review",
                "Add Apigee SOAP‑REST proxy with auth mapping",
                "Legacy system integrates with latency under 2 s"
            ]
        },

        # PART 4: Exactly 8 topic-adapted execution stages
        "lab": {
            "name": "Existing Systems Integration Workshop",
            "file": "day-150-topic-03.md",
            "goal": (
                "Produce an integration catalog that lists each external system, its interface details, and the "
                "chosen Google Cloud connectivity pattern."
            ),
            "expected": (
                "A catalog (markdown or spreadsheet) containing for each system: name, endpoint, protocol, auth, "
                "data format, and the recommended Google Cloud service or configuration for connection."
            ),
            "mode": "Local/tabletop analysis using a text file or spreadsheet.",
            "prereq": "Prior day exit artifacts, access to existing system documentation or contacts.",
            "preflight": (
                "Reach out to system owners to collect the latest interface documents (WSDL, OpenAPI, etc.)."
            ),
            "steps": [
                "**Stage 1: Preflight & Environment Validation** - Verify list of systems to integrate.",
                "**Stage 2: Prepare Target, Inputs, or Backing Resources** - Create a worksheet with columns: System, Endpoint, Protocol, Auth, Format, Google Cloud Solution.",
                "**Stage 3: Author the Plan, Configuration, or Analysis** - For each system, research the appropriate Google Cloud service (e.g., API Gateway, Pub/Sub, Cloud VPN).",
                "**Stage 4: Execute or Simulate the Planned Work** - Fill in the worksheet with the chosen connectivity pattern.",
                "**Stage 5: Inspect Expected State & Verify Outcomes** - Verify that each system has a feasible mapping and note any constraints (e.g., latency, throughput).",
                "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge** - What if a system goes offline during cutover? How would you handle fallback?",
                "**Stage 7: Diagnose Evidence & Record Remediation / Decision** - Update any incomplete or inaccurate entries based on feedback from system owners.",
                "**Stage 8: Cleanup or Exercise Closeout** - Save the final catalog as evidence and discard temporary worksheets."
            ],
            "verification": "The catalog is complete and each entry includes a concrete Google Cloud integration method.",
            "trouble": "If a system’s interface is undocumented, treat it as a black box and plan for a sniffing or monitoring approach to infer the contract.",
            "cleanup": "Delete any temporary spreadsheets or notes; retain the final integration catalog as evidence.",
            "accept": "Save the integration catalog, a brief note on the validation date, and any outstanding questions with owners as evidence for this topic."
        }
    },
    {
        "key": "topic-04",
        "title": "What skills does the team have?",
        "preview": (
            "Assessing team skills early prevents over‑commitment to unfamiliar technologies and highlights "
            "where training or hiring is needed."
        ),
        "overview": (
            "This topic covers a structured evaluation of the team’s existing competencies (e.g., Kubernetes, "
            "data engineering, security) relative to the skills required to operate the proposed architecture."
        ),
        "technical": (
            "Explain how to map team skills to architecture responsibilities and identify gaps.\n\n"
            "- **Skill Inventory:** Use a questionnaire or interview to capture proficiency levels (e.g., none, beginner, intermediate, advanced).\n"
            "- **Role Mapping:** Assign architecture components (e.g., cluster admin, data pipeline engineer) to required skill sets.\n"
            "- **Gap Analysis:** Compare required vs. available skills and plan mitigations (training, consulting, hiring).\n"
            "- **Evidence:** Retain the skill matrix and the gap‑mitigation plan as part of the discovery artifacts."
        ),
        "questions": [
            "How do you evaluate proficiency levels without relying solely on self‑assessment?",
            "What threshold of skill gap triggers a decision to hire versus upskill?",
            "How do you keep the skill matrix up to date as the team evolves?"
        ],
        "reference": "https://cloud.google.com/architecture/framework",
        "reference_label": "Google Cloud Architecture Framework Overview",

        # PART 3: Realistic Operational Incident
        "scenario": {
            "scenario": (
                "During discovery for a machine learning platform, the architecture proposed a Kubeflow‑based "
                "solution, but the team’s skill assessment revealed no prior experience with Kubernetes operators."
            ),
            "symptom": (
                "The team underestimated the operational overhead, leading to missed milestones during the prototype phase."
            ),
            "impact": (
                "The project would have required either extensive consulting or a redesign to a more managed service (e.g., Vertex AI)."
            ),
            "constraints": (
                "The solution must be operable by the existing team within three months of training; no external managed "
                "ML service may be used due to data residency constraints."
            ),
            "evidence": (
                "Skill assessment table (excerpt):\n\n"
                "```\n"
                "Skill                | Team Avg. Proficiency (0‑5)\n"
                "---------------------|---------------------------\n"
                "Kubernetes administration | 1\n"
                "Kubeflow pipelines        | 0\n"
                "Python ML libraries       | 4\n"
                "```"
            ),
            "root": (
                "The team relied on anecdotal statements (‘we’ve used containers’) without a formal proficiency evaluation."
            ),
            "diagnostic_steps": [
                "Step 1: Define the skill domains required for the architecture (e.g., cluster ops, ML framework, monitoring).\n"
                "Step 2: Conduct a confidential self‑assessment or peer‑review questionnaire.\n"
                "Step 3: Aggregate results and identify domains where the average proficiency is below a threshold (e.g., 3).\n"
                "Step 4: For each gap, define a mitigation plan (e.g., Coursera course, paired programming with a consultant).\n"
                "Step 5: Schedule checkpoints to re‑evaluate proficiency after the mitigation."
            ],
            "fix": (
                "Tactical Fix: Immediately enroll the team in a Kubernetes fundamentals course and schedule hands‑on labs.\n\n"
                "Strategic Fix: Implement a skills‑tracking dashboard that updates after each completed training module or certification."
            ),
            "verify": (
                "Confirm that after the training period, the team’s average proficiency in Kubernetes administration reaches at least 3 "
                "and that they can successfully deploy a sample application to a test cluster."
            ),
            "residual": (
                "Skills decay; plan for refresher training every six months and maintain a competency‑budget in the project plan."
            ),
            "diagram": [
                "Team proposes Kubeflow on Kubernetes",
                "Skill assessment shows low Kubernetes proficiency",
                "Operational gap identified during planning review",
                "Enroll in Kubernetes training and schedule labs",
                "Team achieves sufficient proficiency to operate the platform"
            ]
        },

        # PART 4: Exactly 8 topic-adapted execution stages
        "lab": {
            "name": "Team Skills Assessment Workshop",
            "file": "day-150-topic-04.md",
            "goal": (
                "Produce a skills matrix that captures proficiency levels for each relevant domain and a gap‑mitigation plan."
            ),
            "expected": (
                "A matrix (spreadsheet or markdown) listing skill domains, proficiency levels (e.g., 0‑5), and for any gaps "
                "a defined mitigation plan with owner and target date."
            ),
            "mode": "Local/tabletop analysis using a questionnaire and a spreadsheet.",
            "prereq": "Prior day exit artifacts, access to a skill‑assessment questionnaire (e.g., Likert scale).",
            "preflight": (
                "Finalize the list of skill domains based on the architecture components discovered so far."
            ),
            "steps": [
                "**Stage 1: Preflight & Environment Validation** - Confirm list of skill domains to evaluate.",
                "**Stage 2: Prepare Target, Inputs, or Backing Resources** - Create a questionnaire with a column for self‑rating (0‑5).",
                "**Stage 3: Author the Plan, Configuration, or Analysis** - Distribute the questionnaire and collect responses anonymously if preferred.",
                "**Stage 4: Execute or Simulate the Planned Work** - Aggregate the results into a matrix and calculate average proficiency per domain.",
                "**Stage 5: Inspect Expected State & Verify Outcomes** - Identify domains where the average is below the agreed‑upon threshold (e.g., 3).",
                "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge** - What if a key team member leaves after the assessment? How would you mitigate the knowledge loss?",
                "**Stage 7: Diagnose Evidence & Record Remediation / Decision** - For each gap, write a mitigation plan (training, hiring, consulting) with an owner and target completion date.",
                "**Stage 8: Cleanup or Exercise Closeout** - Save the final skills matrix and gap‑mitigation plan as evidence and discard temporary questionnaires."
            ],
            "verification": "The matrix is complete and each domain with a gap has an associated mitigation plan.",
            "trouble": "If proficiency scores seem inflated, consider incorporating a practical exercise or peer review to validate self‑ratings.",
            "cleanup": "Delete any temporary questionnaires or notes; retain the final skills matrix and mitigation plan as evidence.",
            "accept": "Save the skills matrix, the gap‑mitigation plan, and a note on the reassessment schedule (e.g., every 2 months) as evidence for this topic."
        }
    }
]