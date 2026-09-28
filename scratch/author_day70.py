"""Author the Day 70 page from the existing site shell."""
from html import escape
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "content/day-070-page.html"
soup = BeautifulSoup(PAGE.read_text(), "html.parser")


pillars = [
    {
        "key": "topic-01", "title": "Operational excellence",
        "preview": (
            "After a Brightloaf release, checkout errors rise but no one can identify the alert owner or the rollback decision. "
            "Operators spend time reconstructing the change while customers cannot complete orders."
        ),
        "overview": (
            "Operational excellence asks whether the people and processes around a workload can operate it, observe it, "
            "change it safely, and improve it over time. It connects service objectives to dashboards and alerts, incident "
            "roles, runbooks, change controls, and learning actions. An automation tool or runbook is only useful evidence "
            "when the team can show who uses it, under which trigger, and how it knows the action worked."
        ),
        "technical": (
            "Start with the user-facing objective and trace how a symptom becomes an owned action. Check whether a signal "
            "describes user impact, whether an alert reaches a named responder, whether the responder has the permissions "
            "and decision authority needed to act, and whether the runbook ends with an observable recovery check. For "
            "change management, trace a proposed change through review, deployment, rollback criteria, and post-change "
            "observation. A review should distinguish documented procedure from a demonstrated rehearsal."
        ),
        "questions": [
            "Which user objective does each alert protect, and who receives it outside business hours?",
            "What condition triggers rollback, who can authorize it, and what signal confirms recovery?",
            "Where are incident actions and follow-up owners recorded so recurring causes can be removed?",
        ],
        "reference": "https://docs.cloud.google.com/architecture/framework/operational-excellence#core-principles",
        "reference_label": "Operational excellence: core principles",
        "scenario": {
            "symptom": "A release is followed by checkout failures; the incident channel has graphs but no named alert owner or agreed rollback trigger.",
            "constraints": "The team must protect order integrity, keep the incident response reversible, and avoid declaring recovery from a green infrastructure signal alone.",
            "evidence": "The synthetic case provides a release-to-error sequence and missing ownership and rollback evidence. It provides no measured error rate, duration, or confirmed code defect.",
            "diagnosis": "Correlate the change record with the user-facing checkout signal; inspect the alert route and runbook; ask the on-call responder to identify the decision owner; then confirm which check represents successful order submission.",
            "root": "The operating path has no explicit owner and decision rule linking the customer symptom to a reversible response. A code regression is one possibility, not an established fact.",
            "fix": "Assign an accountable incident lead and alert owner, write a rollback trigger tied to the checkout objective, and require a post-rollback functional check before closing the incident.",
            "verify": "In a controlled rehearsal or later incident, confirm the alert reaches the owner, the decision is recorded, rollback completes, and a test order reaches the expected terminal state without duplicate fulfillment.",
            "residual": "A rehearsal cannot prove every future release is safe; retain change-specific monitoring and review any failed or ambiguous recovery check.",
            "diagram": ("Release reaches checkout", "No owned alert or rollback rule", "Checkout failures persist", "Named response owner", "Functional order check passes"),
            "facts": "Synthetic Brightloaf case: checkout failures follow a release, and the incident record lacks an alert owner and rollback trigger. No production measurements or confirmed code defect are supplied.",
            "inference": "Without an owner and decision rule, responders may delay a reversible mitigation while they reconstruct responsibilities. The exact fault remains unknown.",
            "expected": "An owned alert, an explicit rollback condition, and a functional recovery check make the response traceable. A rehearsal or incident record is needed to show that the path works.",
        },
        "lab": {
            "name": "Operational response trace",
            "file": "day-070-operations-review.md",
            "steps": [
                "From the Day 69 requirements, write the user outcome and the observable signal that best represents it. Label any missing threshold as an open requirement instead of inventing one.",
                "Draw the handoff from signal to alert recipient, incident lead, change decision, rollback action, and recovery check. Name the artifact or owner at each handoff.",
                "Use the synthetic case in Part 3. Mark which links are supported by evidence, which are only asserted, and which are missing. Keep the possible code defect separate from the established ownership gap.",
                "Write one remediation with an owner role, a reversible action, a rehearsal condition, a success observation, and a residual risk. Save the diagram and decision record in the named file.",
            ],
            "expected": "A response trace that names the signal, responder, decision authority, rollback condition, recovery observation, owner, and remaining uncertainty.",
            "trouble": "If no objective is defined, carry forward the Day 69 requirement gap. If the responder lacks authority, record the escalation path. Do not label a tabletop walkthrough as a passed rehearsal.",
            "accept": "The artifact contains one evidence-backed operating strength and one owned remediation, with a recovery check that observes customer order behavior.",
        },
    },
    {
        "key": "topic-02", "title": "Security, privacy, and compliance",
        "preview": (
            "A support export gives a recipient more order detail than the support task requires, and the review cannot find an approval or retention decision. "
            "The organization may expose customer information and lack evidence to explain how it was handled."
        ),
        "overview": (
            "This lens follows data and access through the workload: what information is collected, why it is needed, which identities can use it, "
            "how use is recorded, and when it is removed. Security controls, privacy decisions, and compliance obligations overlap but are not interchangeable. "
            "Cloud providers secure parts of the service; the customer still owns workload configuration, identities, data use, and the interpretation of its obligations. "
            "A framework review can identify questions and evidence gaps, but it is not a legal attestation."
        ),
        "technical": (
            "Trace a representative data item from collection through storage, staff access, export, and deletion. At each boundary, record the data owner, "
            "purpose, identity, authorization decision, logging evidence, and retention rule. Compare permissions with the task being performed and check whether "
            "an export has fewer fields or a narrower audience than the source system. Map obligations to the organization's actual jurisdictions and contracts; "
            "do not infer compliance from a product feature or a generic control checklist."
        ),
        "questions": [
            "Which data classes and purposes are in scope, and who approved that classification?",
            "Can a reviewer trace each support role to the minimum data and actions needed for its task?",
            "What audit record, retention rule, and escalation process cover exported data after it leaves the application?",
        ],
        "reference": "https://docs.cloud.google.com/architecture/framework/security/implement-zero-trust#principle-overview",
        "reference_label": "Security: implement zero trust",
        "scenario": {
            "symptom": "A support worker can export full order records even though the stated task only needs delivery status.",
            "constraints": "Preserve support's ability to resolve delivery questions, limit exposure of customer data, retain an auditable decision, and follow the organization's own retention and privacy obligations.",
            "evidence": "The synthetic case states that the export contains broader order details than the task needs and that approval and retention evidence are unavailable. It identifies no real customer, actual access log, or regulatory breach.",
            "diagnosis": "Compare the support task to the export fields; inspect the role grant and approval trail; identify where the export is stored and shared; then ask the data owner to confirm purpose, retention, and incident escalation requirements.",
            "root": "The access and export design does not show a task-specific data boundary or a documented owner decision. Whether the access was used improperly is not established by the scenario.",
            "fix": "Design a status-only support view for this task, grant access through an approved role, log access, and assign a retention and deletion rule to exported records. Route any real exposure concern through the organization's incident process.",
            "verify": "Use a test identity with the support role to confirm it can see delivery status but not unrelated order fields; inspect the approval and access record, and verify the export lifecycle against the approved retention rule.",
            "residual": "A sample role check does not establish that every export path is restricted or that the organization's legal obligations are met; review other interfaces and obtain the appropriate privacy or compliance decision.",
            "diagram": ("Support asks for status", "Role exposes full order record", "Unneeded fields are exportable", "Scoped support view", "Only approved fields are visible"),
            "facts": "Synthetic Brightloaf case: a support task needs delivery status, while its export includes broader order details and no approval or retention evidence is available. No real access event or breach is supplied.",
            "inference": "The mismatch between task and data scope indicates a least-privilege and governance gap; it does not establish that data was misused or that a law was violated.",
            "expected": "A scoped view, approved role, access record, and retention decision make the intended boundary reviewable. Workload-wide access paths and legal obligations still need separate review.",
        },
        "lab": {
            "name": "Support data boundary review",
            "file": "day-070-security-review.md",
            "steps": [
                "Copy the support task and required user outcome from the Day 69 artifact. List the minimum data fields that would let the worker complete that task.",
                "Map the source record, support identity, authorization, view or export, audit record, and deletion point. Mark unknown owners and missing evidence explicitly.",
                "Compare the synthetic export in Part 3 with the minimum field list. Record the excess fields as a risk hypothesis, not as proof of misuse or a confirmed breach.",
                "Propose a narrower view or export, the approving owner, an access check using a test identity, and a retention verification. Save the data-flow sketch and evidence register in the named file.",
            ],
            "expected": "A data-flow sketch that states purpose, minimum fields, role boundary, approval evidence, audit evidence, retention owner, verification method, and unresolved obligations.",
            "trouble": "If a field's purpose is unclear, request a data-owner decision. If policy or law is uncertain, leave the obligation open for the responsible privacy or compliance reviewer rather than guessing.",
            "accept": "The artifact contains one supported security or privacy strength and one owned remediation, with a test-identity check and explicit residual risk.",
        },
    },
    {
        "key": "topic-03", "title": "Reliability",
        "preview": (
            "A fulfillment dependency slows down, and the order service retries without a bound or a tested degraded response. "
            "Orders stall while operators cannot tell whether replay and recovery will preserve one fulfillment per order."
        ),
        "overview": (
            "Reliability is workload-specific: the team first states what users need and under which conditions, then identifies how failures are observed, handled, "
            "and learned from. Review dependency maps, objectives, failure domains, graceful degradation, data recovery, and recovery exercises together. "
            "Redundant components alone do not demonstrate reliability. Business correctness is part of the review: retrying or replaying a message must not create a second fulfillment."
        ),
        "technical": (
            "Use the Day 69 service objectives to define the reliability boundary and the failure conditions that matter to customers. Follow a request and its resulting "
            "event through dependencies and state changes. Check whether signals reveal user impact, retries have limits and backoff, overload is contained, and the system "
            "has an explicit degraded response. For recovery, inspect backup or replay assumptions and the reconciliation step that detects missing or duplicate business outcomes. "
            "A tabletop prediction, a component health check, and a measured recovery rehearsal are different kinds of evidence."
        ),
        "questions": [
            "Which user objective and dependency boundary define acceptable behavior during a slowdown?",
            "Where are retry limits, backoff, load shedding, and the degraded response documented and observed?",
            "How does a recovery test reconcile order state and prove replay cannot create duplicate fulfillment?",
        ],
        "reference": "https://docs.cloud.google.com/architecture/framework/reliability#focus-areas-for-reliability",
        "reference_label": "Reliability: scoping, observation, response, and learning",
        "scenario": {
            "symptom": "When the fulfillment dependency is slow, the order service keeps retrying and customers see orders remain pending.",
            "constraints": "Protect order state, avoid amplifying the dependency, preserve a clear customer response, and do not claim recovery until pending work is reconciled.",
            "evidence": "The synthetic case says retries are unbounded in the described path and no degraded-mode rehearsal is available. It supplies no latency, error rate, outage duration, or confirmed duplicate order.",
            "diagnosis": "Trace one order from request through event and fulfillment state; inspect retry policy and dependency signals; identify whether each attempt uses a stable idempotency key; then compare pending, completed, and replayed business records after a controlled recovery exercise.",
            "root": "The described path lacks a bounded retry response and evidence that recovery is safe at the business-state boundary. The scenario does not prove a duplicate fulfillment occurred.",
            "fix": "Bound retries with backoff and a defined stop condition, return a deliberate pending or degraded response, and make fulfillment creation idempotent on a stable order key. Add reconciliation before replay is considered complete.",
            "verify": "In a controlled test, slow or fail the dependency, observe that retries remain bounded, restore it, replay the event, and reconcile order and fulfillment records to confirm one business fulfillment per order.",
            "residual": "The exercise covers its selected failure mode only. Dependency combinations, data loss, and regional recovery need their own scoped tests and evidence.",
            "diagram": ("Fulfillment slows", "Unbounded retry adds pressure", "Orders remain pending", "Bounded retry + idempotency", "Reconciled single fulfillment"),
            "facts": "Synthetic Brightloaf case: a slow fulfillment dependency is followed by repeated retry behavior and pending orders; no degraded-mode rehearsal is available. No measured duration or duplicate fulfillment is supplied.",
            "inference": "Retries can increase pressure on a slow dependency, and recovery lacks demonstrated business-state safety. The scenario does not show that a duplicate occurred.",
            "expected": "Bounded retries, a deliberate degraded response, idempotent fulfillment, and reconciliation should contain pressure and preserve one fulfillment per order; a controlled test must verify this.",
        },
        "lab": {
            "name": "Failure and recovery evidence map",
            "file": "day-070-reliability-review.md",
            "steps": [
                "Select one Day 69 user objective and draw the order request, state store, fulfillment dependency, and resulting business record. Label owners and trust boundaries.",
                "Add the failure signals, retry limits, degraded response, recovery trigger, replay step, and reconciliation check. If a control is unknown, mark it unknown.",
                "Use the Part 3 case to mark where repeated attempts could add pressure. State the stable idempotency key and the invariant that one order cannot create a second fulfillment.",
                "Write a controlled rehearsal outline: inject a dependency slowdown, observe bounded retries, restore the dependency, replay safely, and reconcile order and fulfillment state. Keep expected outcomes labeled as predictions until run.",
            ],
            "expected": "A failure path and recovery map with an objective, bounded retry rule, degraded response, idempotency invariant, reconciliation evidence, and test boundary.",
            "trouble": "If the business key or state transition is unclear, stop at that boundary and assign an owner to define it. Do not equate a successful health check with completed or correct orders.",
            "accept": "The artifact contains one evidence-backed reliability strength and one remediation, with a recovery check that preserves the single-fulfillment invariant.",
        },
    },
    {
        "key": "topic-04", "title": "Cost optimization",
        "preview": (
            "A capacity proposal uses one peak estimate and omits the workload shape, environment requirements, and owner for its assumptions. "
            "The team may pay for unused capacity or remove capacity that protects a customer objective."
        ),
        "overview": (
            "Cost optimization asks whether the workload's consumption produces business value at an acceptable total operating cost. Review demand patterns, resource "
            "owners, environment-specific requirements, allocation data, and forecast assumptions, then compare options against reliability, performance, security, and operating effort. "
            "Lower spend is not automatically better if it breaks a requirement. Budgets and alerts improve visibility but are notifications, not hard spending caps."
        ),
        "technical": (
            "Start with a cost question tied to a business outcome, such as cost per successfully completed order, and identify which usage and billing data could answer it. "
            "Separate fixed commitments from variable consumption and state the workload, period, region, environment, and demand assumptions used by the estimate. "
            "Compare options under normal and changed demand while holding required service objectives constant. Include operating labor and failure costs where evidence exists; label unknown prices or usage as assumptions. "
            "A forecast supports a decision but does not predict a guaranteed bill."
        ),
        "questions": [
            "What user or business unit of value does the estimate support, and which team owns the inputs?",
            "Do the demand shape and production-versus-development requirements justify each resource assumption?",
            "How will observed usage, allocation, and service objectives be reviewed after a cost change?",
        ],
        "reference": "https://docs.cloud.google.com/architecture/framework/cost-optimization/optimize-resource-usage#principle-overview",
        "reference_label": "Cost optimization: optimize resource usage",
        "scenario": {
            "symptom": "A capacity proposal contains a single peak estimate but no demand history, environment split, or trace to the service objective it should protect.",
            "constraints": "Maintain customer-facing service requirements, distinguish production from nonproduction needs, and make cost assumptions reviewable without inventing usage or prices.",
            "evidence": "The synthetic case supplies only the presence of a peak estimate and the missing demand-to-resource trace. It supplies no billing export, unit price, workload measurement, or budget value.",
            "diagnosis": "Identify the estimate owner and source; ask what workload window and environment it represents; map each proposed resource to its demand driver and reliability or performance constraint; then list which source data would validate the assumptions.",
            "root": "The proposal is not reproducible because workload shape, environment context, and requirement links are absent. The scenario cannot establish that resources are overprovisioned or underprovisioned.",
            "fix": "Create an owned forecast with explicit demand and pricing sources, separate production and nonproduction assumptions, attach service constraints, and define a review trigger for actual usage and business value.",
            "verify": "Before changing production capacity, compare forecast assumptions with authorized billing and usage evidence, review the expected effect on objectives, and after an approved change compare actual use and service outcomes with the stated hypothesis.",
            "residual": "Prices, demand, and product behavior can change; revisit the model on a defined cadence or when the workload or service objective changes. A budget alert does not block spending.",
            "diagram": ("Peak-only estimate", "Demand and owner missing", "Capacity choice is unsupported", "Owned demand model", "Usage and objective reviewed"),
            "facts": "Synthetic Brightloaf case: a capacity proposal has one peak estimate without a demand-to-resource trace. No price, usage measurement, or budget value is supplied.",
            "inference": "The proposal is not reproducible enough to support either a safe reduction or a claim of overprovisioning; the actual cost opportunity remains unknown.",
            "expected": "An owned demand model tied to environment-specific service requirements makes the decision reviewable. Actual usage and service behavior must be checked after an approved change.",
        },
        "lab": {
            "name": "Workload cost assumption review",
            "file": "day-070-cost-review.md",
            "steps": [
                "Choose a business outcome from the Day 69 requirements and name a useful cost unit, such as cost per completed order. Do not enter a numeric result without a supplied data source.",
                "Create an assumption register for demand shape, environment, resource, region, billing or price source, service constraint, and owner. Mark unavailable inputs as unknown.",
                "Use the Part 3 peak-only case. Identify at least one assumption that could make a cost reduction unsafe and one assumption that could hide idle spend; describe what evidence would distinguish them.",
                "Write a review plan that compares actual authorized usage and allocation with the forecast after an approved change, keeps service objectives in scope, and names a revisit trigger. Save the register and decision note in the named file.",
            ],
            "expected": "A reproducible assumption register that connects demand, resource, owner, price or billing source, environment, business value, service constraint, and revisit trigger.",
            "trouble": "If billing or usage data is unavailable, leave the estimate qualitative and assign a data owner. Do not treat a budget notification as a spend limit or use an unverified price.",
            "accept": "The artifact contains one evidence-backed cost-management strength and one owned remediation that protects stated service requirements and has a post-change review method.",
        },
    },
]


def put(section_id, markup):
    section = soup.select_one(f"#{section_id}")
    heading = section.find("h2", recursive=False)
    for child in list(section.contents):
        if child is not heading:
            child.extract()
    section.append(BeautifulSoup(markup, "html.parser"))


def wrap_svg(text, limit=22):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > limit:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines[:2]


def incident_svg(index, pillar):
    event, cause, impact, control, outcome = pillar["scenario"]["diagram"]
    uid = f"d70-case-{index}"
    labels = [
        (25, 61, "Initiating event", event, "#94a3b8"),
        (280, 61, "ROOT CAUSE", cause, "#fb7185"),
        (535, 61, "Affected outcome", impact, "#fb7185"),
        (25, 221, "Same trigger", event, "#94a3b8"),
        (280, 221, "CORRECTED CONTROL", control, "#4ade80"),
        (535, 221, "Expected outcome", outcome, "#4ade80"),
    ]
    box_html = []
    for x, y, label, detail, color in labels:
        lines = wrap_svg(detail)
        detail_html = "".join(
            f'<text x="{x+95}" y="{y+{1:57,2:49}[len(lines)] + j*17}" text-anchor="middle" style="font:12px ui-monospace,monospace;fill:#cbd5e1">{escape(line)}</text>'
            for j, line in enumerate(lines)
        )
        box_html.append(
            f'<g><rect x="{x}" y="{y}" width="190" height="88" rx="12" fill="#121526" stroke="{color}" stroke-width="2"/>'
            f'<text x="{x+95}" y="{y+27}" text-anchor="middle" style="font:700 14px ui-monospace,monospace;fill:#e2e8f0">{escape(label)}</text>'
            f'{detail_html}</g>'
        )
    boxes = "".join(box_html)
    return f'''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg viewBox="0 0 960 365" width="960" height="365" role="img" aria-labelledby="{uid}-title {uid}-desc" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block">
<title id="{uid}-title">{escape(pillar['title'])}: synthetic failed and corrected paths</title><desc id="{uid}-desc">The dashed upper path runs from the initiating event through the labeled root cause to customer impact. The solid lower path shows the proposed control, expected outcome, and verification boundary. This is a synthetic case, not a measured incident.</desc>
<defs><marker id="{uid}-rose-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0 L10 4 L0 8 Z" fill="#fb7185"/></marker><marker id="{uid}-green-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0 L10 4 L0 8 Z" fill="#4ade80"/></marker></defs>
<text x="25" y="35" style="font:700 17px ui-monospace,monospace;fill:#fb7185">FAILED PATH · dashed</text><text x="25" y="195" style="font:700 17px ui-monospace,monospace;fill:#4ade80">CORRECTED PATH · solid</text>
<path d="M215 105 H275 M470 105 H530 M725 105 H785" stroke="#fb7185" stroke-width="3" stroke-dasharray="9 7" fill="none" marker-end="url(#{uid}-rose-arrow)"/><path d="M215 265 H275 M470 265 H530 M725 265 H785" stroke="#4ade80" stroke-width="3" fill="none" marker-end="url(#{uid}-green-arrow)"/>
{boxes}<line x1="800" y1="50" x2="800" y2="320" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5 5"/><text x="820" y="92" transform="rotate(90 820 92)" style="font:700 13px ui-monospace,monospace;fill:#cbd5e1">VERIFICATION BOUNDARY</text>
<text x="25" y="350" style="font:13px ui-monospace,monospace;fill:#94a3b8">Synthetic case; the lower lane is a proposed control pending workload-specific verification.</text></svg></div>
<figcaption><strong>Supplied facts:</strong> {escape(pillar['scenario']['facts'])}<br><strong>Architectural inference:</strong> {escape(pillar['scenario']['inference'])}<br><strong>Expected post-fix behavior:</strong> {escape(pillar['scenario']['expected'])}</figcaption></figure>'''


def technical_svg():
    uid = "d70-review-path"
    nodes = [
        (24, "Day 69 inputs", "goals · owners"),
        (264, "Set boundary", "workload · assumptions"),
        (504, "Inspect evidence", "four review lenses"),
        (744, "Owned follow-up", "check · residual risk"),
    ]
    boxes = "".join(
        f'<g><rect x="{x}" y="88" width="190" height="106" rx="14" fill="#121526" stroke="#334155" stroke-width="2"/>'
        f'<text x="{x+95}" y="130" text-anchor="middle" style="font:700 16px ui-monospace,monospace;fill:#e2e8f0">{escape(title)}</text>'
        f'<text x="{x+95}" y="160" text-anchor="middle" style="font:13px ui-monospace,monospace;fill:#94a3b8">{escape(sub)}</text></g>'
        for x, title, sub in nodes
    )
    return f'''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg viewBox="0 0 960 280" width="960" height="280" role="img" aria-labelledby="{uid}-title {uid}-desc" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block">
<title id="{uid}-title">Day 70 workload review path</title><desc id="{uid}-desc">Use prior goals and owners to define a workload boundary, inspect evidence through four review lenses, then assign follow-up with a check and residual-risk record.</desc><defs><marker id="d70-review-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0 L10 4 L0 8 Z" fill="#38bdf8"/></marker></defs>
{boxes}<path d="M214 141 H257 M454 141 H497 M694 141 H737" stroke="#38bdf8" stroke-width="3" fill="none" marker-end="url(#d70-review-arrow)"/><text x="24" y="245" style="font:13px ui-monospace,monospace;fill:#94a3b8">A review organizes evidence and decisions; it does not certify compliance or prove runtime behavior.</text>
</svg></div><figcaption>Model: move from the Day 69 goals and owners through a bounded evidence review to an owned follow-up. It applies to the workload review process and does not prove a control, service objective, or regulatory obligation is satisfied.</figcaption></figure>'''


# Part 1: orient each lens and preview one concrete problem in exactly two sentences.
part1 = '''<p class="intro">Day 70 turns the requirements and stakeholder priorities from Day 69 into an evidence-backed review. Inspect the same workload through four lenses, then record a strength and a remediation for each one.</p>
<p class="callout"><strong>Exit evidence</strong> Bring the Day 69 requirements and owner map. Leave with one evidence-backed strength and one owned remediation per pillar, each tied to a verification method and residual risk.</p>'''
for i, p in enumerate(pillars, 1):
    part1 += f'''<article id="{p['key']}-overview" class="topic-card overview"><h3>{i}. {escape(p['title'])}</h3><p>{escape(p['overview'])}</p><p class="problem-preview"><strong>Problem preview:</strong> {escape(p['preview'])}</p></article>'''
put("part-1", part1)

# Part 2: shared review procedure, architecture path, and pillar-specific analysis.
part2 = '''<p class="intro">Begin with the workload boundary and the customer outcome from Day 69. For each claim, link the requirement, inspected artifact, accountable owner, evidence date or scope, and the limitation that remains. Keep an assertion distinct from an observation and a tabletop prediction distinct from a measured result.</p>
<table><caption>Review path and evidence record</caption><thead><tr><th scope="col">Review stage</th><th scope="col">Inputs and scope</th><th scope="col">Decision</th><th scope="col">Evidence to retain</th></tr></thead><tbody>
<tr><th scope="row">Bound</th><td>Requirements, stakeholders, system context, data and dependency boundaries</td><td>Choose workload, user outcome, assumptions, and review owners</td><td>Scope statement with requirement and owner references</td></tr>
<tr><th scope="row">Inspect</th><td>Operational, security, reliability, and cost artifacts</td><td>Ask pillar-specific questions; record supported, asserted, missing, or stale evidence</td><td>Artifact name, owner, scope/date, observed fact, and limitation</td></tr>
<tr><th scope="row">Decide</th><td>Strengths, gaps, impact, constraints, dependencies</td><td>Prioritize a remediation without dropping required user outcomes</td><td>Decision rationale, accountable owner, and residual risk</td></tr>
<tr><th scope="row">Verify</th><td>Proposed control and acceptance condition</td><td>Select review, rehearsal, measurement, or policy decision appropriate to the claim</td><td>Expected result before the check; observed result only after it runs</td></tr>
</tbody></table>''' + technical_svg()
for i, p in enumerate(pillars, 1):
    questions = "".join(f"<li>{escape(q)}</li>" for q in p["questions"])
    part2 += f'''<article id="{p['key']}-technical" class="topic-card technical"><h3>{i}. {escape(p['title'])}: what to inspect</h3><p>{escape(p['technical'])}</p><h4>Review questions</h4><ul>{questions}</ul><p><strong>Further study:</strong> <a href="{p['reference']}" target="_blank" rel="noopener">Google Cloud Well-Architected Framework — {escape(p['reference_label'])}</a>.</p></article>'''
put("part-2", part2)

# Part 3: distinct synthetic cases and separate incident diagrams.
part3 = '<p class="intro">These Brightloaf cases are illustrative scenarios, not observed production incidents. Use the case facts as written, make inferences explicit, and treat the lower diagram lane as a proposal until its verification step has been performed.</p>'
for i, p in enumerate(pillars, 1):
    c = p["scenario"]
    part3 += f'''<article id="{p['key']}-problem" class="topic-card problem"><h3>{i}. {escape(p['title'])}: {escape(c['symptom'])}</h3>
<p><strong>Constraints:</strong> {escape(c['constraints'])}</p><p><strong>Case evidence:</strong> {escape(c['evidence'])}</p>
<h4>Diagnostic sequence</h4><ol><li>{escape(c['diagnosis'])}</li><li>Compare the observed workflow to the requirement and responsible owner; write down what is known and what remains uncertain.</li><li>Choose a verification boundary that can establish the relevant user or business outcome, not just component health.</li></ol>
<p><strong>Root cause hypothesis:</strong> {escape(c['root'])}</p>{incident_svg(i, p)}
<h4>Defensible response and verification</h4><p>{escape(c['fix'])} {escape(c['verify'])}</p><p><strong>Residual risk:</strong> {escape(c['residual'])}</p></article>'''
put("part-3", part3)

# Part 4: four different offline exercises with explicit output and acceptance rules.
part4 = '<p class="intro">Each exercise is an offline design review using Day 69 artifacts and the synthetic case above. No cloud account, credentials, CLI, or billable resources are required. Mark expected behavior as a prediction unless a real test or measurement has been performed.</p>'
for i, p in enumerate(pillars, 1):
    lab = p["lab"]
    steps = "".join(f"<li>{escape(step)}</li>" for step in lab["steps"])
    part4 += f'''<article id="{p['key']}-lab" class="topic-card lab"><h3>Exercise {i}: {escape(lab['name'])}</h3>
<p><strong>Goal:</strong> create an evidence-backed review record for {escape(p['title'].lower())}.</p>
<p><strong>Expected Result:</strong> {escape(lab['expected'])}</p>
<p><strong>Mode:</strong> offline tabletop with synthetic Brightloaf facts. <strong>Preflight:</strong> open a local editor, gather the Day 69 requirements and stakeholder owner map, and create <code>{escape(lab['file'])}</code>. Mark the scenario synthetic.</p>
<h4>Exact Execution</h4><ol>{steps}</ol>
<h4>Verification</h4><p>Expected output: {escape(lab['expected'])} Confirm the file separates inspected evidence, assertion, unknown, and prediction, and includes an owner and a specific acceptance check.</p>
<h4>Troubleshooting</h4><p>{escape(lab['trouble'])}</p>
<h4>Cleanup</h4><p>No cloud resources are created. Keep the accepted review note as Day 70 evidence; remove only disposable local drafts.</p>
<h4>Artifact Acceptance</h4><p>{escape(lab['accept'])} File: <code>{escape(lab['file'])}</code>.</p>
<label class="check"><input type="checkbox" data-progress="lab-70-topic-{i}"> I completed and checked this topic exercise</label></article>'''
put("part-4", part4)

# Keep the page's progress controls and add a concise exit-artifact description once.
completion = soup.select_one(".completion")
for old in completion.select(".exit-summary"):
    old.decompose()
completion.append(BeautifulSoup('<p class="exit-summary">Exit artifact: four pillar records, each with one evidence-backed strength, one owned remediation, an acceptance check, and residual risk.</p>', "html.parser"))

PAGE.write_text(str(soup))
