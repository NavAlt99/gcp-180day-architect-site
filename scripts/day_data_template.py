"""day_data_template.py — Specification Template for Day Authoring.

Copy this template to scratch/day_data_{DAY:03d}.py and fill in the fields
based on the Day brief in `gcp-architect-180-day-page-prompts.md`.
Then run:
    python3 scripts/author_engine.py --day {DAY}
"""

DAY = 0  # Replace with Day number (e.g. 73)
WORK_BLOCK = ""  # e.g. "Requirements, migration and architecture"

PART1_INTRO = (
    "Overview of today's learning objectives, architecture themes, and focus areas."
)

EXIT_SUMMARY = (
    "Summary of the day's exit artifact as defined in the roadmap."
)

# Optional comparison/architecture table in Part 2
ARCH_TABLE_HTML = """
<table>
<caption>Topic comparison and trade-offs</caption>
<thead>
<tr>
  <th scope="col">Component / Option</th>
  <th scope="col">Google Cloud Implementation</th>
  <th scope="col">Primary Advantage</th>
  <th scope="col">Trade-off / Operational Boundary</th>
</tr>
</thead>
<tbody>
<tr>
  <th scope="row">Option A</th>
  <td>Service A</td>
  <td>High throughput, low latency</td>
  <td>Increased operational overhead</td>
</tr>
</tbody>
</table>
"""

# Overall Architecture Flow SVG in Part 2 (4 boxes recommended)
ARCH_DIAGRAM = {
    "title": "Architecture Workflow",
    "desc": "Flow from requirements to verification.",
    "caption": "Architecture workflow and boundary verification.",
    "nodes": [
        ("1. Input Scope", "Requirements & Constraints"),
        ("2. Architecture", "Design & Topology"),
        ("3. Decision Matrix", "Trade-offs & Rationale"),
        ("4. Verification", "Observable Proof"),
    ]
}

TOPICS = [
    {
        "key": "topic-01",
        "title": "Topic Title Here",
        "preview": (
            "Sentence 1 describing a concrete technical symptom or decision. "
            "Sentence 2 describing its direct user or business impact."
        ),
        "overview": (
            "Define the mechanism, ownership boundary, service model, and fundamental behavior. "
            "Keep teaching prose concise and non-repetitive."
        ),
        "technical": (
            "Explain control and data plane mechanics, limits, failure boundaries, and trade-offs.\n\n"
            "- **Boundary A:** Specific technical detail.\n"
            "- **Boundary B:** Specific technical detail."
        ),
        "questions": [
            "Discovery or review question 1?",
            "Discovery or review question 2?",
            "Discovery or review question 3?",
        ],
        "reference": "https://docs.cloud.google.com/...",
        "reference_label": "Official GCP Documentation Section",
        "scenario": {
            "symptom": "Concrete operational symptom or failure observed in Brightloaf.",
            "constraints": "Preserve business invariant (single fulfillment per order), budget limits, reversibility.",
            "evidence": "Supplied case facts versus unverified assumptions.",
            "diagnostic_steps": [
                "Step 1: Inspect metrics or logs.",
                "Step 2: Correlate error signals with dependencies.",
                "Step 3: Isolate the failing boundary."
            ],
            "root": "Causal root-cause hypothesis.",
            "fix": "Defensible architectural or configuration fix.",
            "verify": "Verification step and observable signals confirming recovery.",
            "residual": "Residual risk or limitation that remains unproven until production testing.",
            # 5-node flow for Incident SVG:
            "diagram": (
                "Initiating event",
                "Root cause failure",
                "Affected outcome",
                "Corrected control",
                "Expected outcome"
            ),
            "facts": "Supplied case facts.",
            "inference": "Architectural inferences.",
            "expected": "Expected behavior post-fix once verified."
        },
        "lab": {
            "name": "Exercise Name",
            "file": "day-000-topic-01.md",
            "level": "Progressive: Beginner → Intermediate → Advanced",
            "goal": "Clear operational objective of the exercise.",
            "expected": "Measurable, verifiable result.",
            "mode": "offline design / emulator / local shell / tabletop",
            "prereq": "Prior day artifacts required.",
            "preflight": "Editor and preflight verification steps.",
            "steps": [
                "**Stage 1: Beginner (Baseline Discovery & Configuration Inspection)**\n- Inspect current project settings, baseline quotas, and target resource configuration:\n\n```sh\ncat <<'EOF' > stage1-discovery.sh\n# Read-only configuration inspection commands...\nEOF\n```",
                "**Stage 2: Intermediate (Implementation, Deployment & Policy Enforcement)**\n- Provision resources, configure policies, and verify the normal happy-path operation:\n\n```sh\ncat <<'EOF' > stage2-deploy.sh\n# Provisioning and configuration commands...\nEOF\n```",
                "**Stage 3: Advanced (Chaos Injection, Failure Rehearsal & Resilience Verification)**\n- Simulate real-world failure mode, brownout surge, or data corruption and verify automated recovery:\n\n```sh\ncat <<'EOF' > stage3-chaos.sh\n# Fault injection, stress testing, and reconciliation verification...\nEOF\n```",
                "Review the generated output artifacts and verify compliance against acceptance criteria."
            ],
            "verification": "Specific commands or observations that verify success across all 3 stages.",
            "trouble": "Common failure mode and troubleshooting advice for each progressive stage.",
            "cleanup": "Cleanup steps in reverse dependency order.",
            "accept": "Artifact acceptance criteria tied to the roadmap Exit evidence."
        }
    }
]
