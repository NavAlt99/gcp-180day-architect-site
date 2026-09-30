DAY_DATA = {
    "day": 164,
    "part1_intro": (
        "Day 164 is a decision checkpoint, not permission to stop studying. "
        "Use the Day 162 domain map, Day 163 error log and the artifacts already built to identify one repair that would materially improve evidence quality; keep the booking decision separate from confidence or a single practice score."
    ),
    "part2_intro": (
        "Readiness is a traceable state: a current exam scope, domain evidence, unresolved risks, a dated repair plan and a deliberate booking decision. "
        "The page below separates documented certification information from the learner's local evidence and from the decision still owned by the learner."
    ),
    "part3_intro": (
        "The field cases are synthetic decision drills. They show how an architect can be overconfident or prematurely book without presenting either situation as an observed learner result."
    ),
    "part4_intro": (
        "Complete both exercises with the existing portfolio. Use synthetic rows and local notes; do not paste protected exam questions, credentials, payment details or an unverified readiness claim."
    ),
    "exit_summary": (
        "A dated readiness decision, six-domain evidence matrix, highest-value repair plan, current preparation/booking checklist and explicit reason to book now or defer."
    ),
    "arch_table_html": """
<table><caption>Readiness evidence path</caption><thead><tr><th>Boundary</th><th>Decision question</th><th>Evidence to attach</th><th>Limit</th></tr></thead><tbody>
<tr><td>Scope</td><td>Which current exam path applies: standard or renewal?</td><td>Official certification page and current guide, with access date.</td><td>Eligibility and exam details can change; the learner must recheck them before registration.</td></tr>
<tr><td>Capability</td><td>Which domain is weakest by missing or non-repeatable evidence?</td><td>Day 162 domain map, Day 163 error log and linked artifacts.</td><td>A practice score is a local signal, not proof of readiness.</td></tr>
<tr><td>Repair</td><td>What one exercise will close the highest-risk evidence gap?</td><td>Artifact, acceptance test, owner and due date.</td><td>Unverified product behavior or price remains an open question.</td></tr>
<tr><td>Booking gate</td><td>Is the learner choosing to book now, defer, or re-evaluate?</td><td>Decision record with assumptions, remaining work and trigger to revisit.</td><td>Booking is a learner decision; this curriculum does not schedule or pay for an exam.</td></tr>
</tbody></table>
""",
    "arch_diagram": {
        "type": "topology",
        "title": "Day 164 readiness evidence and decision gate",
        "desc": "Three-tier readiness architecture showing current source scope, learner evidence, repair decisions and the final booking decision with observable probes.",
        "caption": "Scope: a local readiness-planning model for Day 164. It shows evidence ownership and decision flow; it does not prove a learner's score, eligibility, booking availability or exam performance.",
        "width": 1120,
        "height": 690,
        "layers": [
            {"name": "TIER 1 · INPUTS / DEMAND", "desc": "current sources and learner need", "x": 10, "y": 55, "w": 1100, "h": 92, "fill": "#0c2033", "title_color": "#38bdf8", "opacity": 0.72},
            {"name": "TIER 2 · EVIDENCE / REPAIR", "desc": "artifacts, scoring and remediation", "x": 10, "y": 185, "w": 1100, "h": 210, "fill": "#241808", "title_color": "#f59e0b", "opacity": 0.64},
            {"name": "TIER 3 · GOVERNANCE / DECISION", "desc": "owner, revisit trigger and choice", "x": 10, "y": 435, "w": 1100, "h": 115, "fill": "#062316", "title_color": "#22c55e", "opacity": 0.68}
        ],
        "components": [
            {"name": "Official scope", "detail": "page + guide + date", "x": 60, "y": 78, "w": 250, "h": 56, "stroke": "#38bdf8", "fill": "#102a42"},
            {"name": "Portfolio inputs", "detail": "domain map + error log", "x": 435, "y": 78, "w": 250, "h": 56, "stroke": "#38bdf8", "fill": "#102a42"},
            {"name": "Booking question", "detail": "book, defer or revisit", "x": 810, "y": 78, "w": 250, "h": 56, "stroke": "#38bdf8", "fill": "#102a42"},
            {"name": "Scope register", "detail": "standard / renewal", "x": 60, "y": 220, "w": 250, "h": 105, "stroke": "#f59e0b", "fill": "#3b2508"},
            {"name": "Evidence matrix", "detail": "six domains · 0–3", "x": 435, "y": 220, "w": 250, "h": 105, "stroke": "#f59e0b", "fill": "#3b2508"},
            {"name": "Repair queue", "detail": "artifact · owner · date", "x": 810, "y": 220, "w": 250, "h": 105, "stroke": "#f59e0b", "fill": "#3b2508"},
            {"name": "Recheck trigger", "detail": "missing evidence or source change", "x": 245, "y": 455, "w": 250, "h": 70, "stroke": "#22c55e", "fill": "#064e3b"},
            {"name": "Learner decision", "detail": "book now / defer", "x": 625, "y": 455, "w": 250, "h": 70, "stroke": "#22c55e", "fill": "#064e3b"}
        ],
        "flows": [
            {"x1": 185, "y1": 134, "x2": 185, "y2": 220, "type": "ok", "label": "verify scope"},
            {"x1": 560, "y1": 134, "x2": 560, "y2": 220, "type": "ok", "label": "score evidence"},
            {"x1": 935, "y1": 134, "x2": 935, "y2": 220, "type": "warn", "label": "do not assume"},
            {"x1": 310, "y1": 272, "x2": 435, "y2": 272, "type": "ok", "label": "scope"},
            {"x1": 685, "y1": 272, "x2": 810, "y2": 272, "type": "ok", "label": "prioritize"},
            {"x1": 935, "y1": 325, "x2": 750, "y2": 455, "type": "ok", "label": "gate"},
            {"x1": 560, "y1": 325, "x2": 370, "y2": 455, "type": "warn", "label": "repair trigger"},
            {"x1": 495, "y1": 490, "x2": 625, "y2": 490, "type": "ok", "label": "recheck"}
        ],
        "boundaries": [
            {"x": 42, "y": 205, "w": 1036, "h": 140, "color": "#f59e0b", "label": "EVIDENCE CHECK"},
            {"x": 220, "y": 442, "w": 680, "h": 94, "color": "#22c55e", "label": "DECISION OWNER"}
        ],
        "probes": [
            {"cx": 0, "cy": 0, "label": "PROBE 1 · source date", "badge": "P1", "color": "#38bdf8"},
            {"cx": 0, "cy": 0, "label": "PROBE 2 · evidence score", "badge": "P2", "color": "#f59e0b"},
            {"cx": 0, "cy": 0, "label": "PROBE 3 · repair exit", "badge": "P3", "color": "#22c55e"}
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Remediate the weakest domain and verify exam scope",
            "overview": (
                "Use the Day 162 six-domain map and Day 163 error log to choose the weakest domain by missing, stale or non-repeatable evidence. "
                "Then confirm the current standard-versus-renewal path from the official certification page and guide, recording the access date and the learner's own eligibility question. "
                "A repair is complete only when a prior artifact, a changed-constraint check and a visible acceptance result are attached."
            ),
            "preview": (
                "Symptom: a learner can name services but cannot defend one domain decision or identify which current exam path applies. "
                "Effect: study time and a possible booking decision may be spent against the wrong scope."
            ),
            "technical": (
                "The readiness loop has four distinct inputs: the current official scope, the learner's evidence portfolio, the error taxonomy and the repair plan. "
                "Score evidence rather than confidence: correctness asks whether the decision fits the requirements, traceability asks whether the source and artifact are findable, and failure reasoning asks whether a changed constraint produces a changed answer. "
                "A missing score is not a zero-quality product claim; it is an evidence gap to repair. Keep the exam page's current standard and renewal descriptions as documentation, and keep the learner's domain rating as local evidence. "
                "Do not copy live exam questions or infer readiness from a single practice set."
            ),
            "questions": [
                "Which current source establishes the exam path, and when was it checked?",
                "What saved artifact demonstrates the weakest domain rather than merely naming it?",
                "What changed constraint would reverse the chosen architecture answer?",
                "What observable acceptance result closes the repair?"
            ],
            "reference": "https://cloud.google.com/learn/certification/cloud-architect",
            "reference_label": "Google Cloud Professional Cloud Architect certification page (checked 2026-09-30)",
            "scenario": {
                "scenario": "A learner's portfolio has complete pages for all six domains, but the security/compliance domain has no reproducible authorization test and the exam path was never recorded.",
                "impact": "The learner may over-rate broad reading, choose a repair that cannot be verified, or schedule against the wrong current scope. The business effect is lost study time and an avoidable decision made without evidence.",
                "constraints": "Use only the learner's existing artifacts and current official preparation material; do not copy protected exam content, submit a booking, or present a practice score as an observed readiness measure.",
                "facts": "Synthetic portfolio review: the security/compliance artifact is missing a denied-action result and the current exam path is unrecorded.",
                "inference": "The first failing boundary is evidence ownership and scope selection, not necessarily IAM knowledge. The learner needs a source-dated scope register and one bounded authorization repair.",
                "root": "The review treated page completion as capability and did not require a reproducible artifact, changed-constraint check or current scope citation.",
                "diagnostic_steps": [
                    "Compare the six domain rows with the Day 163 error taxonomy and mark missing, stale, supplied or observed evidence.",
                    "Open the official certification page and guide; record the path checked, access date and any eligibility question without guessing.",
                    "Select the weakest row and write the smallest repair that produces both an allowed and a denied result or an equivalent decision trace.",
                    "Re-score the row only after the artifact and changed-constraint result are saved."
                ],
                "remediation_steps": [
                    "Create a dated scope register with standard-versus-renewal choice, source links and a recheck date.",
                    "Re-run the selected domain exercise using synthetic identities or a tabletop policy matrix, labeling predictions as predictions.",
                    "Attach the failed case, corrected decision, acceptance signal, owner and residual uncertainty to the readiness packet."
                ],
                "verify": "The row has a source-dated scope decision, a linked repair artifact, a negative case and a reviewer or self-review note explaining what would change the decision.",
                "residual": "Current exam rules, documentation and eligibility can change; a local evidence packet cannot establish a passing score or guarantee production skill."
            },
            "lab": {
                "name": "Weakest-domain repair packet",
                "goal": "Turn one weak domain into a source-dated, reviewable repair decision.",
                "expected": "A readiness packet contains the current scope, six-domain evidence matrix, selected repair, negative case, acceptance result and remaining uncertainty.",
                "mode": "local/tabletop with synthetic data; no exam booking or cloud mutation",
                "prereq": "Day 162 domain map, Day 163 error log and one linked prior artifact",
                "preflight": "Use a local note named `day-164-readiness-repair.md`; record access date, sources checked, lab mode and the fact that all examples are synthetic.",
                "steps": [
                    "**Stage 1 — Preflight and validate assumptions/environment.** Open the Day 162 domain map and Day 163 error log. Confirm that the note has a source-date field, six domain rows, an evidence classification column, and no copied protected exam content.",
                    "**Stage 2 — Prepare the target, inputs, or backing resources.** Copy one artifact link and one error-log entry into the selected domain row. Add the official certification page and exam-guide links, the access date, and the unresolved standard-versus-renewal question.",
                    "**Stage 3 — Author the plan, configuration, or analysis.** Fill a repair table with `requirement | decision rule | existing evidence | missing evidence | acceptance signal | owner | due/recheck date`. Select the smallest repair that can produce a visible result.",
                    "**Stage 4 — Execute or simulate the planned change.** Re-run the selected prior exercise with synthetic inputs. Record one allowed case, one denied or rejected case, and the exact decision rule; mark every result as observed, supplied or predicted.",
                    "**Stage 5 — Inspect expected state and verify outcomes.** Score the row from 0 to 3 for correctness, traceability, evidence, failure reasoning and communication. Accept only when the artifact link, negative case, source date and acceptance result are present.",
                    "**Stage 6 — Rehearse a bounded failure, edge case, or decision challenge.** Change one material constraint—residency, recovery target, cost ceiling, identity boundary or team skill. Write which decision changes first and which evidence would reveal the change.",
                    "**Stage 7 — Diagnose evidence and record remediation/decision.** Write the root cause of the evidence gap, the chosen repair, rejected alternative, owner, next review date and the reason the result does or does not support a booking decision.",
                    "**Stage 8 — Clean up or close out the exercise.** Save `day-164-readiness-repair.md`, link it from the exit packet, remove only disposable copies, and record that no exam booking, payment or cloud resource was created."
                ],
                "verification": "The selected domain row is re-scored with evidence, the scope path is cited, and the readiness packet states the next repair or booking decision.",
                "accept": "The artifact is accepted only when it names the weak domain, source date, linked evidence, negative case, changed-constraint result, owner, recheck date and unresolved risk.",
                "trouble": "If a score is based on memory or page completion, downgrade it to an evidence gap. If the official page and guide disagree with an old note, keep the current source as the input and record the old claim for repair.",
                "cleanup": "No chargeable resource is created. Keep the readiness packet and delete only disposable working copies; never store credentials, payment data or protected exam content.",
                "file": "day-164-readiness-repair.md"
            }
        },
        {
            "key": "topic-02",
            "title": "Plan the remaining Days 165–179 before deciding whether to book",
            "overview": (
                "Day 164 does not replace the multi-team architecture, synthesis, gate and capstone work scheduled for Days 165–179. "
                "Convert the remaining curriculum into a short dependency-aware plan: preserve the next platform boundary, assign an artifact owner, set a completion signal, and use Day 180 only for light review and logistics. "
                "Booking can be recorded as defer, re-evaluate or learner-chosen now, but the reason must be explicit and reversible."
            ),
            "preview": (
                "Symptom: a learner books because the current score feels comfortable while required platform and capstone evidence is still unreviewed. "
                "Effect: remaining work is compressed, decision quality drops, and Day 180 is incorrectly treated as a catch-up day."
            ),
            "technical": (
                "Model the remaining work as a small dependency graph, not a motivational checklist. Days 165–173 produce multi-team architecture and synthesis artifacts, Day 174 is the integrated gate, Days 175–179 are capstone defenses, and Day 180 is reserved for light review, logistics and rest. "
                "For each remaining day record prerequisite, artifact, acceptance signal, owner and stop/revisit trigger. A booking decision depends on the learner's own constraints and current official process; the curriculum can expose missing evidence but cannot authorize registration. "
                "Use a recheck date for sources and a bounded repair queue so a new documentation change or failed capstone does not silently invalidate the readiness packet."
            ),
            "questions": [
                "Which remaining artifact is a prerequisite for the next gate or capstone?",
                "What is the acceptance signal, and what would make the plan stop or change?",
                "Which task belongs on Day 180, and which must be completed before it?",
                "What learner-owned condition would justify booking or deferral?"
            ],
            "reference": "https://services.google.com/fh/files/misc/professional_cloud_architect_exam_guide_english.pdf",
            "reference_label": "Google Cloud Professional Cloud Architect exam guide (checked 2026-09-30)",
            "scenario": {
                "scenario": "A learner plans to use Day 180 for all remaining preparation, although the landing-zone, identity, API, sustainability, capacity and capstone artifacts are still incomplete.",
                "impact": "The plan hides prerequisite work and turns a light-review day into a compressed implementation sprint. A booking choice made from that plan cannot be explained or revisited cleanly.",
                "constraints": "Respect the curriculum order, keep the schedule learner-owned, avoid promises about exam availability or scores, and preserve time for recovery and review rather than adding unbounded tasks.",
                "facts": "Synthetic planning case: several later-day artifacts are marked not started, while Day 180 is labeled light review/rest in the roadmap.",
                "inference": "The planning defect is a missing dependency and acceptance model. The repair is to sequence the remaining work and make booking conditional on evidence rather than calendar pressure.",
                "root": "The plan treated all study days as interchangeable and collapsed implementation, gate review, capstone defense and rest into one final bucket.",
                "diagnostic_steps": [
                    "List Days 165–180 and copy each exit artifact into a dependency table; mark source, owner, state and acceptance signal.",
                    "Draw arrows from prerequisites to the next gate or defense and identify the first incomplete upstream artifact.",
                    "Compare the plan with the current official exam guide and certification preparation page; record only documented facts and learner decisions separately.",
                    "Run a stop test: mark one required capstone artifact late and record the booking decision, communication and revised date."
                ],
                "remediation_steps": [
                    "Create a dated repair queue for Days 165–179 with one evidence-producing task per day and a named completion signal.",
                    "Reserve Day 180 for light review, logistics and rest; move any missing platform or capstone work earlier.",
                    "Record book, defer or re-evaluate with a trigger, not a vague confidence statement, and review it after the integrated gate."
                ],
                "verify": "The plan shows dependencies, owners, acceptance signals, a stop/revisit trigger and a booking choice that can change after later evidence.",
                "residual": "A well-ordered plan still cannot predict exam performance, preserve future documentation or guarantee a preferred test appointment."
            },
            "lab": {
                "name": "Remaining-work dependency and booking gate",
                "goal": "Build a bounded plan for Days 165–180 and make a reversible booking decision from evidence.",
                "expected": "A dependency map and decision record protect Days 165–179 as required work and reserve Day 180 for light review, logistics and rest.",
                "mode": "local/tabletop planning with synthetic schedule data; no booking or payment",
                "prereq": "Day 164 topic 1 repair packet and the roadmap exit evidence for Days 165–180",
                "preflight": "Use a separate local note named `day-164-remaining-plan.md`; record today's date, available study hours as an assumption, and that the booking decision is learner-owned.",
                "steps": [
                    "**Stage 1 — Preflight and validate assumptions/environment.** Open the roadmap entries for Days 165–180 and the Day 164 repair packet. Confirm that each row has an artifact field, acceptance field, owner field, dependency field and state field; label unknown availability or timing as an assumption.",
                    "**Stage 2 — Prepare the target, inputs, or backing resources.** Enter one row per day with its exit evidence. Mark Days 165–173 as platform/synthesis work, Day 174 as the integrated gate, Days 175–179 as capstone defenses, and Day 180 as light review/rest.",
                    "**Stage 3 — Author the plan, configuration, or analysis.** Add prerequisite arrows, a one-sentence acceptance test, a source or artifact link, an owner, a planned review date and a stop/revisit trigger for every row. Keep the plan small enough to inspect daily.",
                    "**Stage 4 — Execute or simulate the planned change.** Complete a planning slice for the next three days: write the first artifact, acceptance signal and fallback for each. Do not claim that a future artifact or exam booking already exists.",
                    "**Stage 5 — Inspect expected state and verify outcomes.** Check that every Day 165–179 row has a predecessor or an explicit start condition, and that no implementation or capstone task is assigned to Day 180. Save the resulting dependency order.",
                    "**Stage 6 — Rehearse a bounded failure, edge case, or decision challenge.** Mark one upstream artifact late or one official source changed. Propagate the impact to the gate/capstone and write the new booking choice: book, defer or re-evaluate, with a concrete trigger.",
                    "**Stage 7 — Diagnose evidence and record remediation/decision.** Record the critical path, the first missing evidence, the responsible owner, the revised plan and the reason for the current booking choice. Separate documented exam facts, local observations, tabletop predictions and learner decisions.",
                    "**Stage 8 — Clean up or close out the exercise.** Save `day-164-remaining-plan.md`, link it from the readiness packet, remove disposable copies, and leave Day 180 labeled for light review, logistics and rest. Do not open a registration flow or enter payment details."
                ],
                "verification": "The plan has a dependency chain for Days 165–179, a protected Day 180, and a booking choice with a trigger to revisit.",
                "accept": "The artifact is accepted only when every remaining day has an exit artifact and acceptance signal, the critical path is visible, the stop test is recorded and the learner decision is reversible.",
                "trouble": "If all rows appear independent, inspect the gate and capstone prerequisites again. If the plan needs Day 180 for implementation, move that work earlier and keep the conflict visible rather than redefining the rest day.",
                "cleanup": "No chargeable resource or booking is created. Keep the dependency note as evidence and remove only disposable copies; do not store payment data or protected exam material.",
                "file": "day-164-remaining-plan.md"
            }
        }
    ]
}
