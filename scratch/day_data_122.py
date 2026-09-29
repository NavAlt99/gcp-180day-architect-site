"""Day 122 data specification: unit economics and sensitivity."""

DATA = {
    "day": 122,
    "part1_intro": "Convert the Day 121 cost baseline into cost per fulfilled order. Hold output and service constraints constant, then vary demand, retention, and reliability assumptions. All numeric values in this page are synthetic practice inputs, not Google Cloud prices or a forecast.",
    "exit_summary": "A low/base/high monthly model for 100,000, 500,000, and 2,000,000 fulfilled orders, with line-item assumptions, cost per order, retention and availability sensitivity, an SLO constraint, and a ranked optimization with owner, evidence, and residual risk.",
    "part2_intro": "Normalize each design to the same business output and time window. Calculator line items are estimates based on inputs; reconcile them with measured usage and billing exports. A unit cost is meaningful only when numerator scope, denominator, and service level are explicit.",
    "arch_table_html": """<div class="table-container"><table><thead><tr><th>Path / quantity</th><th>Model</th><th>Owner and decision</th><th>Limit and verification</th></tr></thead><tbody>
<tr><td>Estimate design cost</td><td>Service quantity × dated rate assumption, across serving, database, messaging, storage, observability, network and operations</td><td>Architect owns complete scope; finance validates currency, billing context and discounts</td><td>Calculator output depends on entered assumptions and can differ from the bill. Include shared and fixed costs; disclose omissions.</td></tr>
<tr><td>Normalize unit economics</td><td>Attributable cost during period T ÷ successful unique fulfilled orders during T</td><td>Product and operations define a valid outcome; platform supplies usage and billing evidence</td><td>Requests, retries, failed calls and orders are different denominators. State the allocation method for shared services.</td></tr>
<tr><td>Stress assumptions</td><td>Recompute low/base/high demand and vary one driver, such as retention or warm capacity</td><td>Service owner sets SLO, recovery needs and failure headroom</td><td>Averages hide bursts and fixed capacity. Check peak demand, restore objectives and operating effort.</td></tr>
<tr><td>Choose and verify</td><td>Modeled delta = baseline − candidate; compare with observed delta after a controlled change</td><td>Change owner records baseline, guardrail, rollback trigger and review date</td><td>A forecast is not a saving until bill and service evidence confirm it without correctness or SLO regression.</td></tr>
</tbody></table></div>""",
    "arch_diagram": {
        "type": "topology",
        "title": "Day 122 unit-cost model from demand to decision",
        "desc": "Conceptual flow from order demand and service assumptions to resource estimates and billing evidence, then cost per fulfilled order, sensitivity and a reliability-bounded decision.",
        "caption": "Conceptual estimation path for Day 122. It does not establish current prices, workload behavior, billing attribution, or that an optimization preserves an SLO.",
        "width": 1120, "height": 660,
        "layers": [
            {"name": "BUSINESS OUTPUT AND LOAD", "x": 20, "y": 40, "w": 1080, "h": 100, "fill": "#1e3a5f", "title_color": "#7dd3fc", "desc": "same period · fulfilled orders"},
            {"name": "ESTIMATE AND MEASURED USAGE", "x": 20, "y": 180, "w": 1080, "h": 170, "fill": "#064e3b", "title_color": "#6ee7b7", "desc": "assumptions separate from observations"},
            {"name": "NORMALIZE, SENSITIZE AND DECIDE", "x": 20, "y": 405, "w": 1080, "h": 115, "fill": "#422006", "title_color": "#fdba74", "desc": "cost per valid business outcome"},
        ],
        "components": [
            {"x": 45, "y": 76, "w": 200, "h": 48, "name": "Order demand", "detail": "100k / 500k / 2m", "stroke": "#38bdf8"},
            {"x": 305, "y": 76, "w": 200, "h": 48, "name": "Workload profile", "detail": "peak · retries · region", "stroke": "#38bdf8"},
            {"x": 585, "y": 76, "w": 205, "h": 48, "name": "Service objective", "detail": "availability · latency", "stroke": "#38bdf8"},
            {"x": 860, "y": 76, "w": 205, "h": 48, "name": "Business denominator", "detail": "unique fulfillment", "stroke": "#38bdf8"},
            {"x": 50, "y": 225, "w": 205, "h": 64, "name": "Calculator estimate", "detail": "dated quantity × rate", "stroke": "#22c55e"},
            {"x": 310, "y": 225, "w": 205, "h": 64, "name": "Serving + database", "detail": "requests · capacity · HA", "stroke": "#22c55e"},
            {"x": 570, "y": 225, "w": 205, "h": 64, "name": "Data + operations", "detail": "retention · logs · egress", "stroke": "#22c55e"},
            {"x": 830, "y": 225, "w": 205, "h": 64, "name": "Billing + metrics", "detail": "labels · window · totals", "stroke": "#22c55e"},
            {"x": 175, "y": 435, "w": 250, "h": 58, "name": "Low / base / high", "detail": "unit cost + sensitivity", "stroke": "#fdba74"},
            {"x": 680, "y": 435, "w": 250, "h": 58, "name": "Ranked action", "detail": "SLO · guardrail · rollback", "stroke": "#fdba74"},
        ],
        "flows": [
            {"x1": 245, "y1": 100, "x2": 305, "y2": 100, "label": "profile", "type": "ok"},
            {"x1": 505, "y1": 100, "x2": 585, "y2": 100, "label": "constrain", "type": "ok"},
            {"x1": 790, "y1": 100, "x2": 860, "y2": 100, "label": "define outcome", "type": "ok"},
            {"x1": 145, "y1": 124, "x2": 145, "y2": 225, "label": "quantity", "type": "ok"},
            {"x1": 410, "y1": 124, "x2": 410, "y2": 225, "label": "shape demand", "type": "ok"},
            {"x1": 685, "y1": 124, "x2": 685, "y2": 225, "label": "set headroom", "type": "warn"},
            {"x1": 930, "y1": 124, "x2": 930, "y2": 225, "label": "count success", "type": "ok"},
            {"x1": 255, "y1": 257, "x2": 310, "y2": 257, "label": "estimate", "type": "ok"},
            {"x1": 515, "y1": 257, "x2": 570, "y2": 257, "label": "include", "type": "ok"},
            {"x1": 775, "y1": 257, "x2": 830, "y2": 257, "label": "reconcile", "type": "ok"},
            {"x1": 930, "y1": 289, "x2": 800, "y2": 435, "label": "actual cost + output", "type": "warn"},
            {"x1": 425, "y1": 464, "x2": 680, "y2": 464, "label": "review value and risk", "type": "ok"},
        ],
        "boundaries": [{"x": 35, "y": 390, "w": 1045, "h": 145, "label": "VERIFY BOUNDARY · ESTIMATE ≠ INVOICE ≠ PRODUCTION-SAFE SAVING"}],
        "probes": [
            {"cx": 277, "cy": 92, "label": "P1: Fix period and fulfilled-order definition", "color": "#38bdf8"},
            {"cx": 800, "cy": 244, "label": "P2: Reconcile estimate with usage and billing scope", "color": "#22c55e"},
            {"cx": 1040, "cy": 356, "label": "P3: Check SLO and cost delta after a change", "color": "#f59e0b"},
        ],
    },
    "part3_intro": "These are synthetic Brightloaf planning cases, not observed production incidents. Scenario details below are supplied facts; root-cause explanations are architectural inferences to test with calculator assumptions, billing exports, service metrics and the order ledger.",
    "part4_intro": "Complete the integrated local exercise with Day 121 cost-driver notes and the Day 63 data decision if available. Use the same synthetic workload in all checkpoints. No cloud project, credentials or chargeable resources are needed; any calculator interaction remains an estimate.",
    "topics": []
}


def stages(titles):
    return [f"**Stage {i}: {title}**\n\n{detail}" for i, (title, detail) in enumerate(titles, 1)]


base_lab = {
    "mode": "offline/tabletop; calculator website optional for estimate inputs only",
    "preflight": "Use a local file and mark all figures synthetic, not a quote. Do not sign in, enter credentials, create resources, or use a production project.",
    "prereq": "Day 121 workload/cost notes; local editor or spreadsheet; synthetic Brightloaf workload",
    "trouble": "If an input is unknown, record its owner and a bounded assumption; never silently use zero. A predicted result must be labeled as a prediction.",
    "cleanup": "No cloud resource or billing configuration is touched. Save the worksheet as exit evidence and remove only disposable copies.",
    "file": "day-122-unit-cost-model.md",
}


DATA["topics"] = [
    {
        "key": "topic-01",
        "title": "Pricing Calculator: build a full estimate for every design",
        "overview": "The Pricing Calculator turns proposed resources and consumption into estimates teams can compare before deployment. A complete design includes serving, database, queues, storage and retention, observability, network transfer, backups and required availability capacity. Compare alternatives over the same traffic period, regions and business output; date rate assumptions and call out billing-account discounts. It belongs today because unit economics are only as credible as the scope behind the numerator. The calculator warns that estimates depend on supplied assumptions and can differ from the final bill.",
        "preview": "A Brightloaf estimate counts request compute but leaves database HA, backups, logs and inter-region transfer blank. The design appears cheaper than it is, so a funding decision can understate operating cost and recovery capacity.",
        "technical": """For each design, record product, region, billing unit, quantity, utilization pattern, period and assumption source. Separate fixed floor from traffic-driven quantity: a database replica or minimum instance can remain billable in quiet periods, while request processing, data operations and transfer can scale with load. Include retained backups, log/metric volume and shared resources. Record credits, negotiated rates and commitments as separate cases rather than universal prices.

The calculator is a planning interface, not a meter or quote. Billing-account context, negotiated terms, taxes, credits, real utilization, rounding and product-price changes can make invoice results differ. The architect owns scope and workload quantities; finance validates financial assumptions; service owners confirm capacity and redundancy. Preserve an assumptions register and a copy of each candidate estimate.

Compare estimated line items with SKU-level billing export and product telemetry over an equivalent period. Billing exports can lag, and shared services require an allocation policy. A lower estimate is not defensible if it omits resilience, security controls, operations or business output.""",
        "questions": ["Which costs are fixed, demand-driven, or driven by retention and redundancy?", "Do designs use the same region, time window, workload and service objective?", "Which assumptions depend on billing-account discounts?", "How will estimates be reconciled to billing exports and telemetry?"],
        "reference": "https://cloud.google.com/products/calculator",
        "reference_label": "Google Cloud Pricing Calculator (accessed 2026-09-29; estimate assumptions)",
        "scenario": {
            "scenario": "Synthetic Brightloaf review compares two 500,000-order monthly designs. Design A lists serving and database compute only; backups, retained data, logs, messaging and transfer are blank assumptions.",
            "impact": "The draft model claims a 22% saving. This is not comparable until missing items, time period and fulfillment definition are reconciled.",
            "constraints": "Preserve recovery objectives and order idempotency; planning envelope is fixed. No live billing account is supplied.",
            "evidence": "Supplied synthetic facts: 500,000 successful unique orders; five cost categories omitted; 22% is a worksheet claim, not a bill. Evidence to collect: quantities and dated rates for both designs, SKU-level export, storage/backup inventory, and matching business and telemetry counts.",
            "root": "Architectural inference: asymmetric scope explains the apparent saving more plausibly than proven efficiency. Equal-scope recalculation and later billing are needed to test that inference.",
            "diagnostic_steps": ["Freeze both designs to the same month, region, order profile, availability target and fulfilled-order definition.", "Classify rows as included, excluded, shared allocation or unknown; do not treat blanks as zero.", "Check serving, database HA, storage growth, backups, logs, egress and rate dates with their owners.", "Compare complete estimates and label unverified rates or discounts as uncertainty."],
            "remediation_steps": ["Rebuild both estimates from one inventory and constraint set; retain assumptions and an export.", "Prioritize a measured cost driver only after confirming its share and safe service guardrail.", "Compare same-period billing and service evidence after an approved change; roll back on SLO, recovery or correctness regression."],
            "verify": "All material categories are priced or explicitly excluded with rationale, assumptions match, and a plan reconciles estimates with billing. Do not report the worksheet's 22% as achieved savings.",
            "residual": "Prices, discounts, usage and billing attribution change. Shared costs and delayed data limit precision.",
            "facts": "Synthetic case: five categories are omitted and a 22% saving is claimed; no measured saving exists.",
            "inference": "Incomplete scope may explain the gap; complete estimation and billing reconciliation are required.",
            "expected": "Both alternatives have comparable, dated assumptions and a reconciliation owner.",
            "diagram": ("Estimate leaves categories blank", "Asymmetric scope", "False apparent saving", "Normalize inputs and inventory", "Compare complete estimate; reconcile bill")
        },
        "lab": {
            **base_lab,
            "name": "Build a complete comparable estimate",
            "goal": "Compare two designs on the same scope and expose unknown inputs.",
            "expected": "A cost inventory with units, quantity ranges, dated rate sources, confidence and reconciliation plan.",
            "steps": stages([
                ("Set the comparison", "Create the artifact. Fix one-month period, common region assumptions, fulfilled-order denominator, SLO and recovery constraints."),
                ("Inventory design A", "List serving, database and HA, messaging, storage/backup, observability, network and shared operations rows."),
                ("Inventory design B", "Use the identical categories and units. Mark an unknown quantity as unknown, never as zero."),
                ("Bound quantities", "Enter synthetic low/base/high usage quantities for each candidate and name the owner/source that could validate each value."),
                ("Record price basis", "Add a rate date/source and currency placeholder. Keep discounts, credits, taxes and commitments separate and unverified."),
                ("Compare sensitivity", "Change one retention or availability assumption while holding workload and service constraints fixed; describe ranking change, if any."),
                ("Plan reconciliation", "Specify the later calculator export, same-window SKU billing export, telemetry and order-ledger evidence required."),
                ("Verify and clean up", "Confirm same scope, visible unknowns, one-variable sensitivity and explicit limitations. Save the local worksheet; no cloud resources were created.")
            ]),
            "verification": "Both candidates share a period, business output, workload assumptions and constraints; all material categories are priced or marked unknown; and a one-variable sensitivity is recorded.",
            "accept": "Retain the estimate inventory and reconciliation plan in day-122-unit-cost-model.md; blank rows must not silently become zero-cost claims."
        }
    },
    {
        "key": "topic-02",
        "title": "Unit economics: cost per user, transaction and request",
        "overview": "Unit economics divides attributable cost by an outcome that matters to the business. Cost per request, active user, transaction and fulfilled order answer different questions; retries, failures, background work and shared infrastructure make denominators diverge. Define cost allocation, business event, period and whether cost is marginal or fully allocated. This follows the cost inventory because a correct ratio can still mislead when its cost scope or denominator is incomplete.",
        "preview": "Brightloaf request volume doubles in a retry storm while unique fulfilled orders stay flat. Cost per request looks stable as useful throughput stalls and customers wait.",
        "technical": """A unit metric is attributable cost for period T divided by valid business outcomes in T. Document allocation: direct costs can be assigned by project, label or SKU; shared costs may use a driver such as CPU time, storage or request share. Keep currency, billing period, timezone and event boundary consistent. Report total and variable cost when fixed baseline matters. Average unit cost can fall as fixed capacity spreads over more output even when total spend grows.

For the synthetic worksheet, model 100,000, 500,000 and 2,000,000 fulfilled orders. A fixed-plus-variable model is useful for arithmetic, but actual costs can be nonlinear at saturation, tier transitions, minimum capacity or retention thresholds. Vary demand and one other driver independently, then include a combined stress case. Count successful unique fulfillment records, not API calls, and reconcile retries and cancellations.

Billing exports and application metrics have different delays and scopes. Pair cost per unit with volume, latency, error and fulfillment quality. Cost per active user also needs an explicit active-user rule and can hide unequal workload mix; cost per request includes calls that may create no business value.""",
        "questions": ["What event is one valid unit, and how do retries, cancellations and duplicates affect it?", "Which costs are directly attributable, and how are shared costs assigned?", "Do numerator and denominator share the same window and workload scope?", "Does unit cost change under burst load, retention or capacity thresholds?"],
        "reference": "https://docs.cloud.google.com/architecture/framework/cost-optimization/optimize-resource-usage?hl=en",
        "reference_label": "Well-Architected Framework: optimize resource usage (accessed 2026-09-29; workload patterns and cost models)",
        "scenario": {
            "scenario": "Synthetic dashboard divides serving cost by API requests. A load test increases retries while the deduplicated order ledger shows no increase in unique fulfilled orders.",
            "impact": "The dashboard can show a favorable cost/request trend while useful throughput and customer wait time worsen.",
            "constraints": "Ledger reconciliation is delayed, request logs contain retries and database costs are shared. One order must produce at most one fulfillment.",
            "evidence": "Supplied synthetic facts: requests rise, unique fulfilled orders stay flat, and database cost is shared. No dollar amount or production event is asserted. Collect matching windows, retry/status labels, order keys, billing scope, p95 latency and queue metrics.",
            "root": "Architectural inference: attempted traffic is being treated as business value. Check event keys and terminal order states to establish whether output changed.",
            "diagnostic_steps": ["Align billing, metrics and ledger to the same period and timezone.", "Separate first attempts, retries, failures and cancellations; count one successful fulfillment per stable order key.", "Document direct/shared cost allocation and check whether database, queue, storage and telemetry are included.", "Plot total cost, cost per unique order, request volume, p95 latency and retry/error rate together."],
            "remediation_steps": ["Use reconciled unique fulfillments as the value denominator; retain cost/request as a diagnostic.", "Enforce idempotency at the durable order-state boundary and bound retry handling.", "Repeat a bounded replay/load scenario and compare cost, output correctness and SLO."],
            "verify": "Replay may increase request count, but successful fulfillment for the same order key remains one. Recompute ratios over a common window.",
            "residual": "Billing delay, shared-cost allocation and changing order mix remain sources of uncertainty.",
            "facts": "Synthetic case: retry count rises while unique fulfillments stay flat; no production incident is claimed.",
            "inference": "Request count is a poor value denominator during retries.",
            "expected": "Dashboard pairs cost per unique fulfillment with service-quality signals and replay preserves one fulfillment per order.",
            "diagram": ("Retry load rises", "Requests used as value denominator", "False unit-cost improvement", "Count unique successful orders", "Reconcile ledger, cost and SLO")
        },
        "lab": {
            **base_lab,
            "name": "Calculate cost per valid business outcome",
            "goal": "Calculate three traffic levels and compare request and fulfillment denominators.",
            "expected": "A low/base/high table with formulas, synthetic labels, output definition and sensitivity.",
            "prereq": "Day 121 workload notes. Synthetic monthly model: fixed $420 + $0.00212 per fulfilled order; exercise inputs only.",
            "steps": stages([
                ("Define the denominator", "Create the artifact. One unit is one successfully fulfilled unique order in the month; requests remain a separate measure."),
                ("Enter low demand", "Use 100,000 orders and calculate fixed cost, variable cost, total monthly cost and cost/order from the supplied formula."),
                ("Enter base demand", "Repeat the calculation for 500,000 fulfilled orders and show the arithmetic."),
                ("Enter high demand", "Repeat for 2,000,000 fulfilled orders. State that the linear relationship is a synthetic exercise assumption."),
                ("Inject retry load", "Increase request count by 40% while holding successful orders and stipulated cost fixed. Compute both ratios and explain which reflects output."),
                ("Vary retention", "Add a synthetic $300 monthly retention/availability cost to the base case; recalculate unit cost and identify evidence needed to decide."),
                ("Rank one action", "Score one optimization by estimated impact, confidence, effort and SLO risk; name owner, before/after measures and rollback condition."),
                ("Verify and save", "Check arithmetic and denominator. Label all values synthetic and modeled. Save in the shared Day 122 model; no resource cleanup is needed.")
            ]),
            "verification": "Arithmetic checks: $632 / 100,000 = $0.00632; $1,480 / 500,000 = $0.00296; $4,660 / 2,000,000 = $0.00233. Adding $300 to base yields $1,780 / 500,000 = $0.00356. Synthetic values, not prices.",
            "accept": "Retain the calculations, numerator scope, denominator rule, sensitivity, optimization, guardrail and evidence owner in day-122-unit-cost-model.md."
        }
    },
    {
        "key": "topic-03",
        "title": "Cost versus reliability trade-off decisions",
        "overview": "Reliability features consume capacity or create additional copies and operating paths, while protecting customer and business outcomes. Cost decisions compare the price of a reliability level with risks such as service loss, recovery delay, data loss or incorrect fulfillment. Make availability, latency, RPO, RTO, correctness and peak/failure headroom explicit. Cheaper may be appropriate when interruption is acceptable; it is not equivalent when the service promise differs. This topic turns sensitivity into a defensible optimization priority.",
        "preview": "A monthly estimate drops after removing a database standby and lowering capacity, with no recovery or peak test. A fault or burst could delay orders or recovery beyond the customer promise.",
        "technical": """Translate service objectives into controls such as redundancy, health-based failover, spare capacity, backups, replica-lag tolerance and tested recovery. Model their costs in the complete inventory, then vary the relevant driver. Reliability cost includes duplicated steady-state resources, headroom, testing and operational effort. Keep uncertain incident consequences separate rather than presenting a precise monthly loss.

Define feasible candidates first: each must preserve data correctness, security and agreed SLO/RPO/RTO. Then rank by measurable savings, evidence confidence, effort, reversibility and failure impact. Reducing noncritical idle capacity or changing retention after audit/restore review can be lower risk than removing production redundancy. Average utilization does not prove safe headroom; correlate peak demand, failover capacity, queues and latency.

A defensible change has a baseline, hypothesis, owner, observation window, thresholds and rollback trigger. Compare cost and service quality under normal and bounded failure/load conditions. Google Cloud architecture guidance aligns resource decisions with workload requirements and consumption patterns; cost should be optimized within the service promise.""",
        "questions": ["What SLO, RPO, RTO, peak and correctness requirements bound a cheaper option?", "Which costs are recurring, test-only or uncertain consequence estimates?", "What normal and failure-mode evidence shows that capacity is safe?", "Who accepts residual risk, and what signal triggers rollback?"],
        "reference": "https://docs.cloud.google.com/architecture/framework/cost-optimization/align-cloud-spending-business-value",
        "reference_label": "Well-Architected Framework: align spending with business value (accessed 2026-09-29; TCO and workload decisions)",
        "scenario": {
            "scenario": "Synthetic review proposes removing a database standby and lowering serving headroom to meet a monthly target. There is no failover rehearsal or peak measurement; the recovery objective remains in force.",
            "impact": "The modeled bill may fall, but a failure or burst could exceed recovery and latency promises and transfer unmeasured risk to order fulfillment.",
            "constraints": "Preserve the stated recovery objective and one fulfillment per order. This is a bounded tabletop exercise with no production change.",
            "evidence": "Supplied facts: standby removal and capacity reduction are proposed; recovery and peak tests are missing; recovery target remains binding. Collect SLO/RPO/RTO, failover/restore, peak utilization, backlog/latency and full cost evidence.",
            "root": "Architectural inference: the estimate optimizes cost before proving the design remains feasible under failure and peak demand. Missing evidence blocks a defensible risk claim but does not prove failure.",
            "diagnostic_steps": ["Write availability, latency, recovery, peak and correctness constraints beside the estimate.", "Identify affected cost lines and include recovery capacity and operational effort.", "Compare available normal/failure capacity, failover time, queue growth and recovery evidence against constraints.", "Separate certain recurring savings from uncertain incident consequences and assign risk ownership."],
            "remediation_steps": ["Do not advance a candidate that cannot show required recovery and peak behavior; average utilization is insufficient.", "Prioritize a lower-risk measured action such as nonproduction idle scheduling or retention after audit/restore review.", "Before a production reliability change, rehearse restore/failover and peak behavior in a bounded environment with rollback thresholds."],
            "verify": "Decision record includes constraints, line-item cost delta, failure evidence or gap, risk owner and rollback signal. Replay must preserve one fulfillment per order.",
            "residual": "Tabletop work cannot establish production recovery time, bill savings or rare-event likelihood. Representative testing and post-change observation remain necessary.",
            "facts": "Synthetic proposal removes standby and headroom without failover/peak evidence while recovery objective remains required.",
            "inference": "Cost reductions might violate service constraints; missing tests leave the claim uncertain.",
            "expected": "Only candidates meeting reliability and correctness requirements proceed to measured optimization.",
            "diagram": ("Budget target removes standby", "SLO constraints not tested", "Potential recovery or peak breach", "Retain controls; test boundedly", "Optimize within verified guardrails")
        },
        "lab": {
            **base_lab,
            "name": "Rank an optimization under a reliability guardrail",
            "goal": "Choose a cost action whose evidence and risk fit explicit service constraints.",
            "expected": "Decision record with ranked options, priority, guardrails, owner, evidence and rollback.",
            "prereq": "Completed unit-cost worksheet; Day 94 observability concepts; stated synthetic recovery and latency constraints",
            "steps": stages([
                ("Copy the cost baseline", "Create the decision section. Include low/base/high unit costs and retention sensitivity; identify modeled values."),
                ("Write service constraints", "Record the required SLO, RPO, RTO, peak capacity, latency and one-fulfillment invariant; mark unknowns as unknown."),
                ("List candidate actions", "Compare nonproduction idle scheduling, log-retention reduction after audit review, and production standby removal."),
                ("Estimate cost impact", "For each candidate identify changed line items, expected direction and confidence; use qualitative estimates where measured values are absent."),
                ("Test feasibility", "Eliminate any action that violates or cannot demonstrate the stated objectives. Explain why missing failover evidence blocks standby removal."),
                ("Rank the feasible set", "Score impact, evidence confidence, effort, reversibility and failure consequence; select one priority and name its owner."),
                ("Set verification and rollback", "Define baseline, observation window, success threshold, bounded load/failure checks, billing comparison and rollback trigger."),
                ("Verify and save", "Check that modeled savings are not called achieved and the service promise remains explicit. Save the decision; no cloud changes were made.")
            ]),
            "verification": "The selected action is feasible against stated constraints; cost opportunity and confidence are separate; measures and rollback are observable; savings remain modeled until measured.",
            "accept": "Add the decision to day-122-unit-cost-model.md. Acceptance is a defensible priority, not a guaranteed saving."
        }
    }
]
