"""day_data_151.py — Specification for Day 151: Discovery: budget, risks and success."""

DAY = 151
WORK_BLOCK = "Discovery, cases and exam preparation"

PART1_INTRO = (
    "Day 151 focuses on the discovery phase of a cloud architecture engagement, "
    "specifically defining budget and timeline constraints, identifying customer-perceived risks, "
    "and establishing measurable success criteria."
)

EXIT_SUMMARY = (
    "A scoped proposal document that includes explicit acceptance criteria and exclusions."
)

ARCH_TABLE_HTML = ""

ARCH_DIAGRAM = {
    "type": "topology",
    "title": "Discovery Process Architecture & Stakeholder Flow",
    "desc": "Illustrates the iterative discovery cycle involving stakeholders, constraints, and outcomes.",
    "caption": "Figure: Discovery process showing budget, risk, and success interactions.",
    "width": 1120,
    "height": 690,
    "layers": [
        {"name": "STAKEHOLDER INPUTS", "desc": "Customer, regulators, sponsors, end‑users", "x": 20, "y": 40, "w": 1080, "h": 90, "fill": "#1e3a5f", "title_color": "#7dd3fc"},
        {"name": "DISCOVERY ANALYSIS", "desc": "Budget, risk, success modeling, trade‑off studies", "x": 20, "y": 170, "w": 1080, "h": 180, "fill": "#064e3b", "title_color": "#6ee7b7"},
        {"name": "GOVERNANCE & DOCUMENTATION", "desc": "Scoped proposal, acceptance criteria, exclusions", "x": 20, "y": 390, "w": 1080, "h": 120, "fill": "#422006", "title_color": "#fdba74"},
    ],
    "components": [
        {"x": 55, "y": 70, "w": 180, "h": 45, "name": "Customer & Sponsors", "detail": "Budget owners, executive sponsors", "stroke": "#38bdf8"},
        {"x": 320, "y": 70, "w": 180, "h": 45, "name": "Regulators & Compliance", "detail": "Legal, audit, data residency", "stroke": "#38bdf8"},
        {"x": 585, "y": 70, "w": 205, "h": 45, "name": "End‑Users & Ops", "detail": "Service users, support teams", "stroke": "#38bdf8"},
        {"x": 855, "y": 70, "w": 205, "h": 45, "name": "Technical Leads", "detail": "Architects, engineers, security", "stroke": "#38bdf8"},
        {"x": 55, "y": 200, "w": 260, "h": 60, "name": "Budget Modeling", "detail": "Cost estimation, timeline phasing, contingency", "stroke": "#22c55e"},
        {"x": 375, "y": 200, "w": 260, "h": 60, "name": "Risk Identification", "detail": "Threat modeling, dependency gaps, failure scenarios", "stroke": "#22c55e"},
        {"x": 695, "y": 200, "w": 260, "h": 60, "name": "Success Metrics", "detail": "KPIs, SLIs, SLOs, business outcomes", "stroke": "#22c55e"},
        {"x": 220, "y": 420, "w": 280, "h": 55, "name": "Draft Proposal", "detail": "Initial scope, assumptions, open questions", "stroke": "#f59e0b"},
        {"x": 620, "y": 420, "w": 280, "h": 55, "name": "Final Proposal", "detail": "Acceptance criteria, exclusions, sign‑off", "stroke": "#fdba74"},
    ],
    "flows": [
        {"x1": 235, "y1": 115, "x2": 320, "y2": 115, "label": "regulatory input", "type": "ok"},
        {"x1": 500, "y1": 115, "x2": 585, "y2": 115, "label": "user feedback", "type": "ok"},
        {"x1": 790, "y1": 115, "x2": 855, "y2": 115, "label": "technical constraints", "type": "ok"},
        {"x1": 145, "y1": 133, "x2": 145, "y2": 200, "label": "stakeholder needs", "type": "ok"},
        {"x1": 415, "y1": 133, "x2": 415, "y2": 200, "label": "budget questions", "type": "ok"},
        {"x1": 710, "y1": 133, "x2": 710, "y2": 200, "label": "risk questions", "type": "ok"},
        {"x1": 960, "y1": 133, "x2": 960, "y2": 200, "label": "success questions", "type": "ok"},
        {"x1": 185, "y1": 260, "x2": 220, "y2": 420, "label": "budget → proposal", "type": "ok"},
        {"x1": 505, "y1": 260, "x2": 620, "y2": 420, "label": "risk/success → proposal", "type": "ok"},
    ],
    "boundaries": [
        {"x": 35, "y": 380, "w": 1045, "h": 150, "label": "GOVERNANCE BOUNDARY · PROPOSAL & EXCLUSIONS", "color": "#f59e0b"},
    ],
    "probes": [
        {"cx": 195, "cy": 230, "label": "P1: Budget Clarity", "color": "#38bdf8"},
        {"cx": 595, "cy": 230, "label": "P2: Risk Coverage", "color": "#22c55e"},
        {"cx": 995, "cy": 230, "label": "P3: Success Measurability", "color": "#f59e0b"},
    ],
}

TOPICS = [
    {
        "key": "topic-01",
        "title": "What is the budget and the timeline?",
        "preview": (
            "Budget and timeline define the financial and scheduling boundaries for the architecture effort. "
            "Misalignment leads to scope creep, inadequate resources, or missed delivery windows."
        ),
        "overview": (
            "The budget encompasses all expected costs: compute, storage, networking, licensing, support, "
            "and contingency. The timeline includes phases: discovery, design, implementation, testing, "
            "and handoff, with milestones and dependencies."
        ),
        "technical": (
            "Explain how budget and timeline influence architectural decisions such as service tiers, "
            "redundancy levels, and feature scope. "
            "- Cost Drivers: Identify consumption‑based pricing versus fixed commitments. "
            "- Time‑Boxing: Show how phased delivery aligns with budget releases. "
            "- Trade‑off Analysis: Demonstrate how reducing scope or selecting lower‑cost services extends timeline or reduces features."
        ),
        "questions": [
            "How does a constrained budget affect the choice between managed services and self‑managed infrastructure?",
            "What timeline risks arise from dependency on external teams or third‑party integrations?",
            "How can contingency reserves be justified without inflating the overall budget?"
        ],
        "reference": "https://cloud.google.com/architecture/framework/cost-optimization",
        "reference_label": "Google Cloud Architecture Framework: Cost Optimization",
        "scenario": {
            "scenario": "During a cloud migration project, monthly cloud spend exceeded the forecast by 45% two months after go‑live.",
            "symptom": "Storage and data transfer costs were trending upward due to unexpected log retention and duplicate data sets.",
            "impact": "The project faced a potential $120,000 overrun for the fiscal year, prompting an emergency review.",
            "constraints": "No disruption to production services allowed; cost corrections must preserve SLAs and data governance policies.",
            "evidence": "Billing export shows anomalous storage and streaming insert costs.",
            "root": "Misconfigured lifecycle policy failed to transition aged logs to cheaper storage, and a streaming pipeline inserted raw events instead of aggregated batches.",
            "diagnostic_steps": [
                "1. Export detailed billing data.",
                "2. Filter services by cost and sort descending.",
                "3. Examine Cloud Storage lifecycle rules.",
                "4. Review streaming pipeline configurations."
            ],
            "fix": "Update lifecycle policy to transition logs older than 30 days to Nearline Storage and enable batching in the streaming pipeline.",
            "verify": "Confirm that next month’s billing shows storage costs within 10% of forecast and streaming insert costs reduced by at least 70%.",
            "residual": "Continuous monitoring and quarterly budget reviews are required.",
            "diagram": [
                "Misconfigured lifecycle & streaming settings",
                "Logs retained in expensive storage, high‑frequency inserts",
                "Cost spikes exceed forecast by 45%",
                "Update lifecycle policy & enable batching",
                "Storage costs drop; streaming insert costs reduce"
            ]
        },
        "lab": {
            "name": "Budget Modeling and Timeline Negotiation Exercise",
            "file": "day-151-topic-01.md",
            "goal": "Construct a simple budget model for a cloud‑based order service, identify cost drivers, and negotiate a realistic timeline with stakeholder constraints.",
            "expected": "A budget spreadsheet showing phased cost estimates, a timeline Gantt chart with milestones, and a documented agreement on acceptable variance thresholds.",
            "mode": "tabletop analysis & spreadsheet modeling",
            "prereq": "Prior day exit artifacts, access to spreadsheet software (e.g., Google Sheets, Excel).",
            "preflight": "Gather baseline pricing for core services (Compute Engine, Cloud Storage, BigQuery) from the public pricing calculator.",
            "steps": [
                "**Stage 1: Preflight & Assumption / Environment Validation** - List required services and collect their on‑demand pricing.",
                "**Stage 2: Prepare Target, Inputs, or Backing Resources** - Define workload assumptions: 2 vCPU instances running 24/7, 5 TB storage, 1 TB monthly query load.",
                "**Stage 3: Author the Plan, Configuration, or Analysis** - Compute monthly cost.",
                "**Stage 4: Execute or Simulate the Planned Work** - Perform the calculation and record the result.",
                "**Stage 5: Inspect Expected State & Verify Outcomes** - Validate that the math matches a spreadsheet SUM formula.",
                "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge** - What if storage grows to 10 TB? Re‑calculate cost and impact on budget.",
                "**Stage 7: Diagnose Evidence & Record Remediation / Decision** - Identify that adding a Nearline Storage tier for older logs reduces storage cost by 40%.",
                "**Stage 8: Cleanup or Exercise Closeout** - Document the final budget model and note any assumptions for future review."
            ],
            "verification": "Budget model totals match independent calculations and reflect realistic service usage.",
            "trouble": "If costs appear too low, verify that all required services (networking, support licenses) are included.",
            "cleanup": "Delete any temporary spreadsheet files; retain the final budget model as part of the exit artifact.",
            "accept": "Save the budget model, timeline worksheet, and a short memo documenting agreed‑upon variance thresholds (e.g., ±10% monthly, ±15% total) as evidence for this topic."
        }
    },
    {
        "key": "topic-02",
        "title": "What are the biggest risks as the customer sees them?",
        "preview": (
            "Customer‑perceived risks often differ from technical risks; they include budget overruns, "
            "missed business outcomes, and compliance surprises."
        ),
        "overview": (
            "Risk discovery involves interviewing stakeholders to capture concerns about financial exposure, "
            "regulatory penalties, operational disruption, and failure to deliver promised capabilities. "
            "These risks are logged, categorized, and prioritized for mitigation planning."
        ),
        "technical": (
            "Explain how perceived risks map to technical controls and architectural mitigations. "
            "- Financial Risk: Mitigated by budget alerts, cost‑tagging, and commitment‑based discounts. "
            "- Compliance Risk: Addressed via data residency controls, audit logging, and automated policy enforcement. "
            "- Operational Risk: Reduced through redundancy, automated failover, and thorough run‑book testing. "
            "- Strategic Risk: Countered by phased delivery, success metrics, and early value demonstration."
        ),
        "questions": [
            "How do you differentiate between a perceived risk and an actual technical vulnerability?",
            "What techniques help surface hidden risks that stakeholders may not initially articulate?",
            "How should risk priority be adjusted when new information emerges during the project?"
        ],
        "reference": "https://cloud.google.com/architecture/framework/risk-management",
        "reference_label": "Google Cloud Architecture Framework: Risk Management",
        "scenario": {
            "scenario": "After deploying a healthcare‑data analytics platform, the compliance team notified the project that patient‑identifying information (PII) was being stored in a regional bucket that did not meet data‑residency requirements.",
            "symptom": "An audit logs export showed that personally identifiable fields were present in raw ingest files that landed in a multi‑region bucket, contrary to the mandated single‑region storage rule.",
            "impact": "The organization faced a potential regulatory fine of up to 4% of global turnover and mandatory breach notification to affected individuals.",
            "constraints": "No patient data may be moved without preserving chain‑of‑custody; remediation must not introduce downtime for downstream analytics pipelines.",
            "evidence": "Audit log entry shows PII in bucket; bucket location output shows multi‑region configuration.",
            "root": "The ingestion pipeline defaulted to the organization’s default multi‑region bucket for all incoming files, without inspecting data classification or applying a residency‑based routing rule.",
            "diagnostic_steps": [
                "1. Run a data classification job on a sample of ingested files to tag PII vs non‑PII.",
                "2. Review the Cloud Function or Dataflow template that selects the destination bucket.",
                "3. Verify that the bucket selection logic includes a residency condition based on data tags.",
                "4. Check IAM permissions to ensure the pipeline cannot write to unauthorized locations."
            ],
            "fix": "Update the ingestion function to route PII‑tagged objects to a dedicated regional bucket and non‑PII to the multi‑region bucket. Implement an automated data‑classification stage using Cloud DLP.",
            "verify": "Confirm that subsequent audit logs show no PII appearing in the multi‑region bucket and that all PII‑tagged objects reside only in the approved regional bucket.",
            "residual": "Even with automated controls, false‑negative classifications are possible; periodic manual sampling and DLP model updates are required.",
            "diagram": [
                "Ingestion pipeline without residency check",
                "PII‑tagged file lands in multi‑region bucket",
                "Compliance audit flags residency violation",
                "Update pipeline to route by data classification",
                "PII stored only in approved regional bucket"
            ]
        },
        "lab": {
            "name": "Risk Identification and Prioritization Workshop",
            "file": "day-151-topic-02.md",
            "goal": "Elicit, categorize, and rank stakeholder‑perceived risks for a cloud migration initiative using a structured risk‑matrix approach.",
            "expected": "A risk register listing at least eight distinct risks, each with likelihood, impact, and a mitigation owner, plus a heat‑map visualization.",
            "mode": "tabletop analysis & risk‑matrix drafting",
            "prereq": "Prior day exit artifacts, sticky notes or a digital collaboration board (e.g., Miro, Jamboard).",
            "preflight": "Review the project charter and any existing risk logs from earlier discovery days.",
            "steps": [
                "**Stage 1: Preflight & Assumption / Environment Validation** - Confirm the list of stakeholders to interview (e.g., CTO, CFO, Head of Compliance, Ops Lead).",
                "**Stage 2: Prepare Target, Inputs, or Backing Resources** - Prepare a risk‑matrix template with axes: Likelihood (Rare‑Almost Certain) and Impact (Insignificant‑Catastrophic).",
                "**Stage 3: Author the Plan, Configuration, or Analysis** - Draft open‑ended questions to uncover risks (e.g., \"What keeps you up at night about this project?\").",
                "**Stage 4: Execute or Simulate the Planned Work** - Conduct the interviews (or role‑play them) and capture each stated risk on a separate note.",
                "**Stage 5: Inspect Expected State & Verify Outcomes** - Group similar risks together and eliminate duplicates.",
                "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge** - For the top‑ranked risk, discuss what early warning signs would look like.",
                "**Stage 7: Diagnose Evidence & Record Remediation / Decision** - Assign a likelihood and impact score to each risk, then plot them on the matrix.",
                "**Stage 8: Cleanup or Exercise Closeout** - Document the final risk register and agree on review cadence (e.g., bi‑weekly)."
            ],
            "verification": "The risk register contains mutually exclusive, collectively exhaustive risks covering budget, compliance, operational, and strategic dimensions.",
            "trouble": "If risks appear vague, ask for concrete examples or past incidents that illustrate the concern.",
            "cleanup": "Return any physical notes to the stakeholder or archive digital notes in the project repository.",
            "accept": "Save the risk register (CSV or markdown), the heat‑map image, and a short meeting summary as evidence for this topic."
        }
    },
    {
        "key": "topic-03",
        "title": "How will success be measured?",
        "preview": (
            "Success measurement translates business goals into observable, quantifiable indicators that "
            "can be tracked throughout the lifecycle of the cloud solution."
        ),
        "overview": (
            "Success metrics (often expressed as SLIs, SLOs, or business KPIs) are agreed upon with stakeholders "
            "to provide objective evidence that the delivered architecture meets its intended outcomes. "
            "They must be specific, measurable, achievable, relevant, and time‑bound (SMART)."
        ),
        "technical": (
            "Explain how to define and validate success metrics in a cloud‑native context. "
            "- Service‑Level Indicators (SLIs): Quantitative measures such as latency, error rate, or throughput. "
            "- Service‑Level Objectives (SLOs): Target values for SLIs (e.g., 99.9% of requests < 200 ms). "
            "- Business KPIs: Higher‑level outcomes like revenue growth, user adoption, or cost savings. "
            "- Measurement Planning: Identify data sources (logs, metrics, tracing), collection frequency, and reporting dashboards. "
            "- Validation: Run synthetic transactions or canary releases to confirm that metrics behave as expected."
        ),
        "questions": [
            "How do you balance technical metrics (e.g., latency) with business outcomes (e.g., customer satisfaction) when defining success?",
            "What precautions prevent metric gaming or misinterpretation of data?",
            "How often should success metrics be reviewed and potentially updated during a long‑running project?"
        ],
        "reference": "https://cloud.google.com/architecture/framework/reliability",
        "reference_label": "Google Cloud Architecture Framework: Reliability",
        "scenario": {
            "scenario": "Three weeks after launching a customer‑facing API, the reliability team observed that the API’s error‑rate SLO (99.9% success) was being violated, with error rates creeping up to 1.2%.",
            "symptom": "Clients reported intermittent HTTP 502 errors; internal dashboards showed elevated 5xx responses from the API gateway, yet backend services reported healthy latency and error rates.",
            "impact": "The SLO breach triggered error‑budget consumption, slowing release velocity and prompting an escalation to senior management.",
            "constraints": "No degradation of user experience permitted; any fix must preserve existing functionality and not introduce new failure modes.",
            "evidence": "API gateway log snippet shows 502 errors; backend service metrics show healthy request duration.",
            "root": "An undocumented dependency on a third‑party payment service that occasionally returned HTTP 502 errors under load. The API gateway propagated these errors as‑is, while the backend metrics only measured success of internal processing, not the external call.",
            "diagnostic_steps": [
                "1. Enable end‑to‑end request tracing (e.g., Cloud Trace) to see where latency or errors occur.",
                "2. Review the API gateway configuration for error propagation and retry policies.",
                "3. Check the third‑party service’s status page or incident history for correlated outages.",
                "4. Verify that timeout and circuit‑breaker settings in the gateway match the external SLA."
            ],
            "fix": "Configure the API gateway to retry failed upstream calls twice with exponential backoff before returning an error to the client. Introduce a dedicated health‑check endpoint for the third‑party service and adjust the API logic to fail fast and return a service‑unavailable error only after the health check fails.",
            "verify": "Confirm that error‑rate metrics drop back below the SLO threshold (0.1%) and that client‑observed errors are eliminated during a synthetic load test.",
            "residual": "Even with retries and health checks, transient external failures may still occur; the error budget should accommodate such expected variability.",
            "diagram": [
                "Third‑party service intermittent 502 errors",
                "API gateway propagates errors as 502 to clients",
                "Observed error‑rate SLO breach (1.2% > 0.1%)",
                "Add gateway retry logic and health‑check dependency",
                "Error‑rate drops below SLO; client errors eliminated"
            ]
        },
        "lab": {
            "name": "Success Metrics Definition and Validation Exercise",
            "file": "day-151-topic-03.md",
            "goal": "Define a set of success metrics (SLIs, SLOs, business KPIs) for a cloud‑based order service and validate them using a simple synthetic test.",
            "expected": "A metric specification document containing at least three SLIs with associated SLOs, two business KPIs, and a validation plan that includes test procedures and expected thresholds.",
            "mode": "tabletop analysis & metric drafting",
            "prereq": "Prior day exit artifacts, access to a monitoring demo (e.g., Prometheus + Grafana) or logs.",
            "preflight": "Review the service architecture and identify key user journeys (e.g., place order, check status).",
            "steps": [
                "**Stage 1: Preflight & Assumption / Environment Validation** - Confirm the list of critical user journeys to measure.",
                "**Stage 2: Prepare Target, Inputs, or Backing Resources** - Prepare a metric‑definition template with columns: Metric, Type (SLI/SLO/KPI), Target, Measurement Method.",
                "**Stage 3: Author the Plan, Configuration, or Analysis** - Draft SLIs: request latency, error rate, throughput. Draft SLOs: 99.9% < 200ms, 99.5% success. Draft KPIs: orders per day, average order value.",
                "**Stage 4: Execute or Simulate the Planned Work** - Instrument a local test service (or use a provided trace) to collect latency and error data.",
                "**Stage 5: Inspect Expected State & Verify Outcomes** - Compare collected metrics against the drafted SLOs and note any deviations.",
                "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge** - What if latency spikes to 500ms for 5% of requests? How does that affect the SLO compliance?",
                "**Stage 7: Diagnose Evidence & Record Remediation / Decision** - Identify that adding a frontend cache reduces latency for repeat requests, bringing the SLO back within target.",
                "**Stage 8: Cleanup or Exercise Closeout** - Finalize the metric specification and store it with the validation results."
            ],
            "verification": "The metric specification is complete, internally consistent, and aligned with the service’s user journeys.",
            "trouble": "If metrics seem unattainable, re‑examine the assumptions about traffic volume and resource limits.",
            "cleanup": "Delete any temporary test scripts or dashboards; retain the final metric specification as evidence.",
            "accept": "Save the metric specification (markdown or CSV), a screenshot of the validation dashboard, and a brief note on the agreed‑upon review frequency (e.g., monthly) as evidence for this topic."
        }
    }
]