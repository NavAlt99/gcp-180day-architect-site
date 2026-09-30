"""day_data_119.py — Specification for Day 119: Cost baseline and commitments."""

DAY = 119
WORK_BLOCK = "Performance, delivery and operations"

PART1_INTRO = (
    "Day 119 introduces FinOps practices for establishing a cost baseline, "
    "understanding showback vs chargeback, implementing cost visibility, and "
    "identifying compute savings opportunities. The day builds a dated cost model "
    "that captures fixed and variable costs, utilization uncertainty, and commitment risk."
)

EXIT_SUMMARY = (
    "A dated cost model with fixed/variable costs, utilization uncertainty and commitment risk."
)

ARCH_TABLE_HTML = ""

ARCH_DIAGRAM = {}

TOPICS = [
    {
        "key": "topic-01",
        "title": "FinOps principles",
        "preview": (
            "FinOps brings financial accountability to cloud spending through "
            "collaboration between engineering, finance, and business teams."
        ),
        "overview": (
            "FinOps principles: inform, optimise, operate. Establish visibility "
            "into cloud spending, optimize resource usage and costs, and operate "
            "with continuous improvement. Showback allocates costs to business "
            "units; chargeback bills them directly."
        ),
        "technical": (
            "Explain how to implement FinOps in Google Cloud using native tools. "
            "- Inform: Use labels, billing export to BigQuery, Looker Studio dashboards, "
            "budgets and alerts, anomaly detection. "
            "- Optimise: Apply rightsizing recommendations, idle resource recommender, "
            "Spot VMs for fault‑tolerant workloads, committed use discounts, "
            "sustained use discounts, scheduling start/stop for non‑production. "
            "- Operate: Establish governance, automation, and continuous monitoring.\n\n"
            "Diagram: FinOps lifecycle loop → Inform → Optimise → Operate → (back to Inform)"
        ),
        "questions": [
            "How do you choose between showback and chargeback models?",
            "What are the key steps to implement a FinOps culture in an organization?",
            "How do you measure the success of a FinOps program?"
        ],
        "reference": "https://www.finops.org/framework/",
        "reference_label": "FinOps Foundation Framework",
        "scenario": {
            "scenario": (
                "A rapidly growing startup noticed that its cloud bill doubled "
                "quarter‑over‑quarter, but no one could explain which services or "
                "teams drove the increase."
            ),
            "symptom": (
                "Finance reported rising costs, engineering lacked visibility into "
                "per‑service spend, and product teams were unaware of budget impact."
            ),
            "impact": (
                "Without cost attribution, the company risked overspending, missed "
                "optimization opportunities, and misaligned incentives."
            ),
            "constraints": (
                "Must preserve engineering velocity while introducing cost governance; "
                "no manual tagging of existing resources."
            ),
            "evidence": (
                "Billing export snippet showing missing labels:\n\n"
                "```csv\n"
                "service,description,cost,labels\n"
                "Compute Engine,VM1234,$1200,\"\n"
                "Cloud Storage,standard_storage,$300,\"\n"
                "```"
            ),
            "root": (
                "Resources were created without labeling, so cost allocation could not "
                "be performed. The team had not enforced labeling via organization "
                "policy or CI/CD checks."
            ),
            "diagnostic_steps": [
                "Step 1: Enable billing export to BigQuery if not already done.",
                "Step 2: Query for resources lacking required labels (e.g., env, owner).",
                "Step 3: Review organization policy to see if label enforcement is active.",
                "Step 4: Check CI/CD pipelines for label injection steps."
            ],
            "fix": (
                "Tactical Fix: Immediately enforce required labels via Organization Policy "
                "and retroactively tag existing resources using a one‑off script.\n\n"
                "Strategic Fix: Implement a label‑as‑code framework that validates labels "
                "in pull requests and applies default labels via terraform or deployment templates."
            ),
            "verify": (
                "Confirm that 100% of compute storage resources carry the required labels "
                "and that cost allocation reports show accurate per‑team spend."
            ),
            "residual": (
                "Labeling policies must be maintained as new services are added; periodic "
                "audits are needed to catch drift."
            ),
            "diagram": [
                "Resources created without labels",
                "Finance sees rising unexplained costs",
                "Labeling policy missing or not enforced",
                "Enforce labeling and tag existing resources",
                "Cost allocation shows accurate per‑team spend"
            ]
        },
        "lab": {
            "name": "FinOps Labeling and Cost Visibility Exercise",
            "file": "day-119-topic-01.md",
            "goal": (
                "Apply required labels to cloud resources, verify billing export, and "
                "build a simple cost allocation dashboard."
            ),
            "expected": (
                "A set of labeled resources, a billing export table showing label‑based "
                "aggregation, and a Looker Studio dashboard visualizing cost by label."
            ),
            "mode": "Tabletop analysis using a spreadsheet or local BigQuery sandbox.",
            "prereq": "Prior day exit artifacts, access to a Google Cloud project with billing enabled.",
            "preflight": (
                "Ensure billing export to BigQuery is configured and you can query the "
                "billing table."
            ),
            "steps": [
                "**Stage 1: Preflight & Environment Validation** - Confirm billing export dataset and table.",
                "**Stage 2: Prepare Target, Inputs, or Backing Resources** - List required labels (e.g., env, owner, cost_center).",
                "**Stage 3: Author the Plan, Configuration, or Analysis** - Decide on label values for existing resources.",
                "**Stage 4: Execute or Simulate the Planned Work** - Apply labels via gcloud resource update commands or terraform.",
                "**Stage 5: Inspect Expected State & Verify Outcomes** - Query billing table to verify labels appear.",
                "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge** - What if a label is misspelled? How would you correct it?",
                "**Stage 7: Diagnose Evidence & Record Remediation / Decision** - Identify missing labels and apply a remediation script.",
                "**Stage 8: Cleanup or Exercise Closeout** - Remove any temporary scripts; retain the labeling policy as evidence."
            ],
            "verification": "All resources have the required labels and billing export reflects them.",
            "trouble": "If labels are missing after applying, check IAM permissions to modify resources.",
            "cleanup": "Delete any temporary label‑update scripts; keep the finalized labeling policy.",
            "accept": "Save the labeling policy (e.g., organization policy yaml), a sample of labeled resources, and a screenshot of the cost allocation dashboard as evidence for this topic."
        }
    },
    {
        "key": "topic-02",
        "title": "Showback vs chargeback",
        "preview": (
            "Showback reports costs to business units without financial transfer; "
            "chargeback actually bills them, influencing behavior directly."
        ),
        "overview": (
            "Showback makes costs visible, encouraging optimization without "
            "direct budget impact. Chargeback transfers financial responsibility, "
            "creating stronger incentives to reduce spend. Choose based on "
            "organizational maturity and governance goals."
        ),
        "technical": (
            "Explain how to implement showback and chargeback using Google Cloud billing data. "
            "- Export billing to BigQuery and join with label data to aggregate costs per business unit. "
            "- For showback, distribute reports and dashboards; for chargeback, integrate with "
            "finance systems to generate internal invoices.\n\n"
            "Diagram: Showback (reporting only) → Awareness → Limited action\n"
            "Diagram: Chargeback (billing) → Financial impact → Behavior change → Cost reduction"
        ),
        "questions": [
            "What are the advantages and disadvantages of showback versus chargeback?",
            "How do you handle disputes when chargeback amounts are questioned?",
            "How frequently should cost reports be generated for showback/chargeback?"
        ],
        "reference": "https://docs.cloud.google.com/architecture/framework/cost-optimization",
        "reference_label": "Google Cloud Architecture Framework: Cost Optimization",
        "scenario": {
            "scenario": (
                "A mid‑sized company used showback for six months, but product teams "
                "continued to over‑provision resources because there was no financial impact."
            ),
            "symptom": (
                "Cost reports showed rising spend, but no corrective action was taken by teams."
            ),
            "impact": (
                "The company missed savings opportunities and eventually needed a costly "
                "right‑sizing effort after budget overruns."
            ),
            "constraints": (
                "Must implement a chargeback model that is accepted by finance and engineering "
                "without introducing excessive overhead."
            ),
            "evidence": (
                "Showback dashboard snippet:\n\n"
                "```\n"
                "Business Unit | Monthly Cost\n"
                "--------------------|-------------\n"
                "Marketing       | $12,000\n"
                "Sales         | $8,500\n"
                "Engineering   | $45,000\n"
                "```"
            ),
            "root": (
                "Showback alone did not create sufficient financial incentive; teams viewed "
                "cloud spend as an operational expense they could not control."
            ),
            "diagnostic_steps": [
                "Step 1: Review current showback reports and usage trends.",
                "Step 2: Survey teams on perceived control over cloud costs.",
                "Step 3: Design a simple chargeback model (e.g., allocate compute cost per vCPU‑hour).",
                "Step 4: Pilot chargeback with one willing team and measure behavior change."
            ],
            "fix": (
                "Tactical Fix: Immediately run a pilot chargeback for the engineering team using "
                "actual compute usage from billing export.\n\n"
                "Strategic Fix: Build an automated chargeback pipeline that generates monthly "
                "internal invoices and integrates with the finance system."
            ),
            "verify": (
                "Confirm that the pilot team reduced compute usage by at least 15% after "
                "chargeback implementation and that finance received accurate invoices."
            ),
            "residual": (
                "Chargeback requires accurate data and timely processing; any drift in billing "
                "export or labeling will affect invoice accuracy."
            ),
            "diagram": [
                "Showback reports only, no financial impact",
                "Teams see rising costs but feel no pressure",
                "Usage continues to increase unchecked",
                "Implement pilot chargeback for engineering team",
                "Engineering reduces usage after seeing internal invoice"
            ]
        },
        "lab": {
            "name": "Showback and Chargeback Modeling Exercise",
            "file": "day-119-topic-02.md",
            "goal": (
                "Create a showback report and a simple chargeback model using billing export data."
            ),
            "expected": (
                "A showback dashboard (e.g., Looker Studio) and a chargeback calculation "
                "spreadsheet that outputs internal invoice amounts per business unit."
            ),
            "mode": "Tabletop analysis using billing export data in BigQuery or a CSV snapshot.",
            "prereq": "Prior day exit artifacts, access to billing export table or CSV.",
            "preflight": (
                "Export the last month of billing data to a CSV or ensure BigQuery access."
            ),
            "steps": [
                "**Stage 1: Preflight & Environment Validation** - Confirm billing data schema and required labels.",
                "**Stage 2: Prepare Target, Inputs, or Backing Resources** - Define business unit mapping from labels.",
                "**Stage 3: Author the Plan, Configuration, or Analysis** - Write SQL to aggregate cost per unit for showback.",
                "**Stage 4: Execute or Simulate the Planned Work** - Run the query and export results.",
                "**Stage 5: Inspect Expected State & Verify Outcomes** - Verify that totals match the billing export total.",
                "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge** - What if a label is missing? How does that affect allocation?",
                "**Stage 7: Diagnose Evidence & Record Remediation / Decision** - Identify missing‑label costs and decide on a default allocation.",
                "**Stage 8: Cleanup or Exercise Closeout** - Save the showback and chargeback artifacts; remove temporary query files."
            ],
            "verification": "Showback totals equal total billing export; chargeback invoices sum to same total.",
            "trouble": "If totals do not match, check for missing or mis‑aggregated label dimensions.",
            "cleanup": "Delete any temporary SQL query files; retain the final showback and chargeback models.",
            "accept": "Save the showback dashboard URL or image, the chargeback spreadsheet, and a brief note on the allocation method as evidence for this topic."
        }
    },
    {
        "key": "topic-03",
        "title": "Cost visibility",
        "preview": (
            "Cost visibility combines labels, billing export, dashboards, budgets, alerts, "
            "and anomaly detection to provide real‑time insight into cloud spend."
        ),
        "overview": (
            "Implement cost visibility by enabling billing export to BigQuery, applying "
            "consistent labels, building Looker Studio dashboards, setting budgets and "
            "alerts, and configuring anomaly detection to notify of unexpected spend."
        ),
        "technical": (
            "Explain the technical setup for cost visibility in Google Cloud. "
            "- Enable Cloud Billing export to BigQuery (daily schedule). "
            "- Apply resource labels via organization policy or terraform. "
            "- Create Looker Studio dashboards connected to the billing export table. "
            "- Set up budgets and alerts at project, billing account, or label level. "
            "- Use Cloud Monitoring or BigQuery ML for anomaly detection on spend trends.\n\n"
            "Diagram: Billing export → BigQuery → Labels → Dashboards → Budgets/Alerts → Anomaly detection → Action"
        ),
        "questions": [
            "How do you ensure labels are applied consistently across all resources?",
            "What are the best practices for setting budget alerts to avoid fatigue?",
            "How can you differentiate between expected growth and anomalous spend?"
        ],
        "reference": "https://docs.cloud.google.com/architecture/framework/cost-optimization",
        "reference_label": "Google Cloud Architecture Framework: Cost Optimization",
        "scenario": {
            "scenario": (
                "A company noticed a sudden 40% spike in its monthly cloud bill, but "
                "the increase was not detected until the billing invoice arrived."
            ),
            "symptom": (
                "Finance received the invoice and saw the jump; engineering had no "
                "real‑time indication of the anomaly."
            ),
            "impact": (
                "The delayed detection caused unnecessary spend for an entire billing "
                "cycle before investigation could begin."
            ),
            "constraints": (
                "Must detect anomalies within 24‑48 hours and notify the appropriate owners "
                "without generating excessive false positives."
            ),
            "evidence": (
                "Billing export showing a spike in Cloud Storage costs:\n\n"
                "```csv\n"
                "service,description,cost,timestamp\n"
                "Cloud Storage,standard_storage,$5000,2024-09-01\n"
                "Cloud Storage,standard_storage,$7000,2024-09-02\n"
                "```"
            ),
            "root": (
                "No real‑time monitoring or anomaly detection was configured; the team relied "
                "solely on monthly invoices for cost insight."
            ),
            "diagnostic_steps": [
                "Step 1: Verify billing export to BigQuery is active and streaming.",
                "Step 2: Check for existing budgets and alerts in the Cloud Billing console.",
                "Step 3: Look for anomaly detection configurations (e.g., Cloud Monitoring alert on spend metric).",
                "Step 4: Review label coverage to ensure spend can be segmented."
            ],
            "fix": (
                "Tactical Fix: Immediately create a budget alert at 80% of forecast and an anomaly "
                "detection alert on daily spend using Cloud Monitoring.\n\n"
                "Strategic Fix: Build a Looker Studio dashboard that refreshes daily and includes "
                "spend variance versus forecast and anomaly markers."
            ),
            "verify": (
                "Confirm that a simulated spend spike triggers an alert within one hour and that "
                "the dashboard reflects the anomaly."
            ),
            "residual": (
                "Anomaly detection thresholds require tuning; periodic review is needed to adapt "
                "to changing usage patterns."
            ),
            "diagram": [
                "Spend spike occurs but is unseen",
                "Invoice arrives showing 40% increase",
                "Finance investigates after delay",
                "Set up real‑time budget and anomaly alerts",
                "Next spike triggers immediate alert"
            ]
        },
        "lab": {
            "name": "Cost Visibility Dashboard and Alerts Setup",
            "file": "day-119-topic-03.md",
            "goal": (
                "Enable billing export, apply labels, create a Looker Studio dashboard, "
                "and configure budget and anomaly alerts."
            ),
            "expected": (
                "An active billing export to BigQuery, a labeled resource set, a Looker Studio "
                "dashboard showing cost trends, and a budget alert configured at 80% of forecast."
            ),
            "mode": "Tabletop using a sandbox project or local CSV export of billing data.",
            "prereq": "Prior day exit artifacts, access to a Google Cloud project with billing enabled.",
            "preflight": (
                "Ensure you have permission to modify billing settings and create Looker Studio reports."
            ),
            "steps": [
                "**Stage 1: Preflight & Environment Validation** - Confirm billing account and project ID.",
                "**Stage 2: Prepare Target, Inputs, or Backing Resources** - Decide on label schema (env, team, cost_center).",
                "**Stage 3: Author the Plan, Configuration, or Analysis** - Enable billing export to BigQuery.",
                "**Stage 4: Execute or Simulate the Planned Work** - Run the enable command and wait for first export.",
                "**Stage 5: Inspect Expected State & Verify Outcomes** - Check that data appears in the BigQuery dataset.",
                "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge** - What if the export fails? How would you troubleshoot?",
                "**Stage 7: Diagnose Evidence & Record Remediation / Decision** - Verify export logs and re‑enable if needed.",
                "**Stage 8: Cleanup or Exercise Closeout** - Retain the export configuration as evidence; delete any test scripts."
            ],
            "verification": "Billing export table receives new rows daily and labels are present.",
            "trouble": "If no data appears, check IAM permissions for the billing export service account.",
            "cleanup": "Delete any temporary export test files; keep the final export configuration.",
            "accept": "Save the billing export configuration (e.g., command output), a sample of labeled resources, and a screenshot of the Looker Studio dashboard as evidence for this topic."
        }
    },
    {
        "key": "topic-04",
        "title": "Compute savings",
        "preview": (
            "Compute savings come from rightsizing, idle resource recommendations, Spot VMs, "
            "committed use discounts, sustained use discounts, and scheduling start/stop."
        ),
        "overview": (
            "Identify and apply compute savings opportunities: use rightsizing recommendations "
            "to match machine types to workload, idle resource recommender to find unused VMs, "
            "Spot VMs for fault‑tolerant batches, committed use discounts (resource‑ or spend‑based), "
            "sustained use discounts for steady workloads, and schedule start/stop for non‑production."
        ),
        "technical": (
            "Explain how to identify and apply each compute saving technique in Google Cloud. "
            "- Rightsizing: Use Recommender to get machine type suggestions. "
            "- Idle resources: Run the idle VM recommender. "
            "- Spot VMs: Create instance templates with preemptible option and use in managed instance groups. "
            "- Committed use: Purchase resource‑based or spend‑based commitments via the Commitments API. "
            "- Sustained use: Automatically applied when instances run a significant portion of the month. "
            "- Scheduling: Use Cloud Scheduler to start/stop instances via Cloud Functions.\n\n"
            "Diagram: Workload → Rightsizing/Idle/Spot/Committed/Sustained/Schedule → Cost reduction"
        ),
        "questions": [
            "How do you choose between resource‑based and spend‑based committed use discounts?",
            "What safeguards should you put in place when using Spot VMs for fault‑tolerant workloads?",
            "How do you measure the realized savings from each optimization?"
        ],
        "reference": "https://docs.cloud.google.com/architecture/framework/cost-optimization",
        "reference_label": "Google Cloud Architecture Framework: Cost Optimization",
        "scenario": {
            "scenario": (
                "A team ran a batch processing workload on a fixed‑size n1‑standard‑8 instance group, "
                "but the workload was only active 20% of the time, leaving expensive idle resources."
            ),
            "symptom": (
                "Utilization reports showed low CPU usage, yet the instances ran continuously, "
                "driving up cost."
            ),
            "impact": (
                "The team paid for 80% idle capacity, wasting budget that could be used elsewhere."
            ),
            "constraints": (
                "Must maintain batch processing SLAs while reducing cost; cannot increase job latency."
            ),
            "evidence": (
                "Recommender idle resource output:\n\n"
                "```\n"
                "NAME                                 TYPE      IDLE  RECOMMENDATION\n"
                "batch-workers-00001                  VM        yes   Stop or downsize\n"
                "```"
            ),
            "root": (
                "The team provisioned a fixed capacity pool without using autoscaling or "
                "schedule‑based start/stop, leading to persistent idle resources."
            ),
            "diagnostic_steps": [
                "Step 1: Run the idle VM recommender to identify under‑utilized instances.",
                "Step 2: Review workload patterns to determine start/stop windows.",
                "Step 3: Evaluate Spot VM suitability for fault‑tolerant batch steps.",
                "Step 4: Check rightsizing recommendations for better machine type fit."
            ],
            "fix": (
                "Tactical Fix: Immediately stop the identified idle instances and implement a "
                "Cloud Scheduler‑based start/stop schedule for non‑production hours.\n\n"
                "Strategic Fix: Deploy a managed instance group with autoscaling based on queue depth "
                "and use Spot VMs for the worker pool, falling back to on‑demand when needed."
            ),
            "verify": (
                "Confirm that idle resources are eliminated, the schedule starts/stops instances as "
                "expected, and batch job completion times remain within SLA."
            ),
            "residual": (
                "Savings from Spot VMs and commitments require monitoring; market price changes "
                "or commitment utilization gaps can affect realized savings."
            ),
            "diagram": [
                "Fixed‑size instance group runs idle 80% of time",
                "Idle VM recommender flags resources as idle",
                "Team stops idle instances and sets start/stop schedule",
                "Autoscaling Spot VM pool adjusts to workload",
                "Cost reduces while meeting batch SLAs"
            ]
        },
        "lab": {
            "name": "Compute Savings Identification and Application Exercise",
            "file": "day-119-topic-04.md",
            "goal": (
                "Run the idle VM recommender, apply rightsizing suggestions, and model "
                "Spot VM and committed use savings for a workload."
            ),
            "expected": (
                "A list of idle resources to stop, a set of rightsizing recommendations, "
                "a Spot VM instance template, and a commitment purchase recommendation "
                "with estimated savings."
            ),
            "mode": "Tabletop using recommender outputs or a local CSV of usage data.",
            "prereq": "Prior day exit artifacts, access to Recommender API or CSV export of recommendations.",
            "preflight": (
                "Ensure you can query the Recommender for idle VM rightsizing and compute commitments."
            ),
            "steps": [
                "**Stage 1: Preflight & Environment Validation** - Confirm access to Compute Engine Recommender.",
                "**Stage 2: Prepare Target, Inputs, or Backing Resources** - Export current VM inventory and usage metrics.",
                "**Stage 3: Author the Plan, Configuration, or Analysis** - Run idle VM recommender and rightsizing recommender.",
                "**Stage 4: Execute or Simulate the Planned Work** - Record recommendations and calculate potential savings.",
                "**Stage 5: Inspect Expected State & Verify Outcomes** - Verify that stopping idle instances reduces cost as estimated.",
                "**Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge** - What if a recommended machine type is unavailable in the zone?",
                "**Stage 7: Diagnose Evidence & Record Remediation / Decision** - Identify alternative zones or machine types and adjust plan.",
                "**Stage 8: Cleanup or Exercise Closeout** - Save the recommendations and savings model; delete temporary export files."
            ],
            "verification": "Implementing the recommendations yields the projected cost reduction.",
            "trouble": "If savings are lower than expected, re‑check utilization assumptions and commitment terms.",
            "cleanup": "Delete any temporary recommendation export files; keep the final savings plan.",
            "accept": "Save the idle VM list, rightsizing recommendations, Spot VM instance template, and commitment purchase recommendation as evidence for this topic."
        }
    }
]