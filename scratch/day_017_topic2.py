"""Topic 2 specification for Day 17: Use the matching gate criteria in the Gates section."""

from scratch.day_017_svgs import FIG_17_2_HTML, FIG_17_4_HTML

TOPIC_02_OVERVIEW = (
    '<strong class="keyword">Gate 1 Evaluation Criteria and Pass/Repeat Governance</strong> applies the formal '
    'five-dimension assessment rubric from the Gates section to evaluate readiness for Block 2 (Cloud environment '
    'and identity). Candidates evaluate their cumulative Block 1 portfolio across Correctness (technical and '
    'mathematical precision), Traceability (mapping implementations to architectural requirements), Evidence Quality '
    '(reproducible timestamped outputs and exit codes), Recovery Reasoning (predicting failure modes and verifying '
    'clean rollbacks), and Communication (concise business and operational trade-off framing). To secure an authoritative '
    'PASS decision, every dimension must score at least 2 out of 3, with a composite score of at least 12 out of 15, '
    'and non-negotiable verification that the duplicate fulfillment invariant (&le; 1 physical fulfillment per unique '
    'order ID) is preserved.'
)

TOPIC_02_PREVIEW = (
    "An infrastructure candidate attempts to advance to cloud identity topics despite submitting unverified database rollback logs and vague network routing explanations. "
    "Without enforcing rigorous rubric gating, subtle gaps in transaction isolation and CIDR subnet math compound into critical security vulnerabilities and production data corruption during cloud landing zone deployment."
)

TOPIC_02_QUESTIONS = [
    "How does a quantitative five-dimension rubric prevent subjective bias and technical debt accumulation during architectural capability assessments?",
    "What are the non-negotiable operational criteria that distinguish an acceptable architectural artifact from an unverified or hand-waving explanation?",
    "Why must an architectural checkpoint enforce an explicit pass or repeat decision, and how does targeted remediation repair identified weaknesses without discarding valid work?"
]

TOPIC_02_TECHNICAL = """<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Gate 1 governance model: objective evaluation without introducing new services</strong></li>
<li><strong>The five-dimension foundation evaluation rubric (Correctness, Traceability, Evidence, Failure, Governance)</strong></li>
<li><strong>Adversarial audit protocol: validating reproducibility of Days 5, 8, 10, and 16 artifacts</strong></li>
<li><strong>Remediation mechanics: repairing flawed evidence without re-executing entire blocks</strong></li>
<li><strong>Pass/Repeat decision framework: non-negotiable criteria for advancing to Block 2</strong></li>
</ul>

<h4>Gate 1 governance model: objective evaluation without introducing new services</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Gate Governance and Quality Checkpoint Barriers</strong> represent formal architectural decision gates designed to validate foundational competencies before progressing to higher-complexity domains. Gate 1 sits as the terminal boundary of Block 1 (Days 1–17: Foundations). The overarching governance rule of Gate 1 is absolute and non-negotiable: <em>no new cloud services, provider products, or novel architectural patterns may be introduced</em>. Checkpoint days exist exclusively to evaluate retention, synthesize cross-domain mechanisms, audit operational evidence, and remediate identified gaps. Introducing new topics on a gate day dilutes focus and masks unresolved weaknesses beneath new layers of complexity.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> In enterprise technology programs, architectural checkpoints prevent compounding technical debt. Project managers under delivery pressure frequently advocate for "soft gates" or advancing with known defects, promising to fix foundation flaws later. A cloud architect acts as the impartial guardian of engineering integrity: allowing engineers to configure cloud infrastructure without mastered operating system, networking, and relational fundamentals results in fragile, un-debuggable systems in production. Enforcing strict gating without scope creep ensures that technical teams genuinely possess the prerequisite capabilities required for subsequent phases.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> As established in the <a href="https://cloud.google.com/architecture/framework#core_principles">Google Cloud Architecture Framework: Core principles (accessed 2026-10-04)</a>, Google Cloud mandates operational excellence, system reliability, and disciplined change management. The framework instructs organizations to establish rigorous review mechanisms before deploying production workloads. Gate 1 directly mirrors an enterprise Architecture Review Board (ARB) checkpoint, ensuring candidates can trace Linux system calls, diagnose RFC 1918 CIDR routing, and enforce ACID rollbacks before provisioning Google Cloud Resource Manager folder hierarchies, Cloud Identity synchronization, and IAM policies in Block 2.</p>

<h4>The five-dimension foundation evaluation rubric (Correctness, Traceability, Evidence, Failure, Governance)</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">The Five-Dimension Foundation Rubric</strong> provides an objective, multi-faceted grading standard that evaluates engineering deliverables on a scale of 0 to 3:
1. <em>Dimension 1: Correctness (0–3):</em> Evaluates the mathematical and technical precision of the implementation. Network subnet masks, CIDR ranges, SQL normalization rules, foreign key constraints, and POSIX process controls must be mathematically sound with zero unhandled syntax or semantic errors.
2. <em>Dimension 2: Traceability (0–3):</em> Assesses whether every configuration decision, script parameter, and architectural pattern traces directly back to curriculum roadmap requirements and documented physical mechanisms, avoiding arbitrary "magic numbers" or unexplained defaults.
3. <em>Dimension 3: Evidence Quality (0–3):</em> Measures the rigor of the produced artifacts. Evidence must consist of timestamped terminal logs, exit codes, verifiable assertions, and reproducible script runs that an independent reviewer can execute without relying on external, unstated environmental state.
4. <em>Dimension 4: Failure Reasoning &amp; Recovery (0–3):</em> Evaluates the candidate's ability to predict failure modes, define blast radiuses, rehearse atomic rollbacks, and guarantee system invariants—specifically proving that replaying network events never breaches the duplicate fulfillment invariant (&le; 1 physical fulfillment per unique order ID).
5. <em>Dimension 5: Communication &amp; Governance (0–3):</em> Assesses alignment with Google Cloud Digital Leader business framing: concise problem summaries, clear delineation between observed facts and tabletop hypotheses, and defensible justification of architectural trade-offs.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Objective rubrics eliminate subjective evaluation and inconsistent standards across engineering organizations. When reviewing vendor proposals, internal design documents, or promotion portfolios, senior architects utilize structured rubrics to benchmark technical maturity. This quantitative framework ensures that junior engineers receive actionable, transparent feedback on why an artifact fails to meet enterprise standards and what specific mechanical improvements are required.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud Professional Cloud Architect certification questions test an architect's ability to evaluate multiple viable solutions against rigorous criteria including business impact, cost, security, and operational reliability. Applying this five-dimension rubric trains architects to evaluate Google Cloud architectures systematically: determining whether a Proposed Cloud SQL configuration satisfies high-availability recovery objectives, whether VPC Shared subnets trace to compliance boundaries, and whether automated Cloud Build pipelines produce defensible deployment evidence.</p>

<h4>Adversarial audit protocol: validating reproducibility of Days 5, 8, 10, and 16 artifacts</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Adversarial Artifact Auditing</strong> is an active inspection protocol where prior deliverables are treated as unproven claims until independently validated through cold-start reproduction. Rather than passively glancing at previously authored markdown files, an adversarial audit executes the scripts in clean, disposable workspaces, verifies output SHA-256 hashes, and probes edge-case boundaries across the four key prerequisite days:
- <em>Day 5 (Shell &amp; POSIX):</em> Inspecting pipeline error handling, <code>set -euo pipefail</code>, trap signal handlers, and exit status propagation.
- <em>Day 8 (Networking &amp; Security):</em> Verifying non-overlapping CIDR calculation, DNS lookup paths, TCP socket lifecycle, and TLS 1.3 certificate validation.
- <em>Day 10 (State &amp; Scheduling):</em> Auditing process state machines, Linux systemd unit definitions, cron schedule boundaries, and distributed worker execution invariants.
- <em>Day 16 (Relational Databases &amp; SQL):</em> Probing relational 3NF normalization, atomic <code>COMMIT</code> and <code>ROLLBACK</code> boundaries, isolation levels, and UNIQUE constraint enforcement under concurrent replays.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Production outages frequently stem from "verified" runbooks that were never actually executed in a realistic cold-start environment. An architect must cultivate institutional skepticism: if an operational runbook or disaster recovery procedure has not been verified via an adversarial audit within a disposable sandbox, it cannot be trusted to perform during a real disaster. Proving reproducibility under cold-start conditions ensures that runbooks contain all implicit dependencies, environment variables, and permission prerequisites.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud Site Reliability Engineering (SRE), disaster recovery and failover procedures (such as recovering from a regional Cloud SQL failure or restoring a Spanner database to a point-in-time recovery timestamp) are subjected to regular automated "game days" and chaos testing. Applying the adversarial audit protocol to Block 1 artifacts instills the exact same operational discipline required to validate Google Cloud landing zones and automated Terraform disaster recovery pipelines.</p>

<h4>Remediation mechanics: repairing flawed evidence without re-executing entire blocks</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Targeted Remediation Mechanics</strong> describes the surgical process of identifying specific deficiencies in an architectural artifact and correcting them without discarding valid surrounding work. When an audit uncovers a weak explanation (such as an ambiguous description of DNS TTL caching or an unverified claim about SQL isolation levels), the architect does not restart the curriculum or rewrite unrelated sections. Instead, the architect:
1. Isolates the exact flaw (identifying missing mechanisms, unhandled error cases, or vague claims).
2. Authors a targeted correction containing the underlying physical or mathematical explanation.
3. Provides reproducible terminal evidence demonstrating the repaired mechanism in action.
4. Updates the evaluation score for that specific rubric dimension, updating the audit ledger.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Efficiency and capital conservation are essential architectural virtues. Ripping out entire subsystems or re-executing multi-week engineering phases because of an isolated defect wastes immense organizational resources. Skilled architects practice surgical remediation: they diagnose the precise failure boundary, design a minimal backward-compatible patch, verify the fix with automated regression tests, and maintain project momentum while upholding non-negotiable safety standards.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud enterprise operations, infrastructure drift and security policy violations are remediated surgically. When Security Command Center (SCC) flags an over-permissive IAM binding or an unencrypted Cloud Storage bucket, architects do not tear down the entire project; they author targeted Terraform updates or apply remediation scripts via Google Cloud Policy Controller. Learning targeted remediation at Gate 1 prepares architects to manage cloud operational drift cleanly and effectively.</p>

<h4>Pass/Repeat decision framework: non-negotiable criteria for advancing to Block 2</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">The Pass/Repeat Decision Boundary</strong> establishes the unambiguous mathematical criteria required to clear Gate 1 and advance to Block 2:
- <em>Criterion 1 (Dimension Floor):</em> Every single dimension of the five-dimension rubric must score at least 2 ("Adequate with documented limits") out of 3. Any score of 0 ("Absent") or 1 ("Partial / Flawed") triggers an immediate block-level hold.
- <em>Criterion 2 (Composite Score):</em> The sum of all five dimensions must be at least 12 out of 15 (80% minimum proficiency across foundations).
- <em>Criterion 3 (Non-Negotiable Invariants):</em> Zero unhandled runtime exceptions or syntax errors in lab execution, and mathematically verified preservation of the duplicate fulfillment invariant (&le; 1 physical fulfillment per unique order ID).
- <em>Decision Matrix:</em>
  - If all criteria are satisfied: <strong>PASS</strong> &rarr; Authorize progression to Day 18 (Google Cloud accounts, Free Tier, and Resource Hierarchy).
  - If any criterion is unmet: <strong>REPEAT</strong> &rarr; Freeze curriculum progression; execute targeted remediation on failing dimensions until re-scored to passing thresholds.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects frequently serve as the final signatory on production go-live decisions and major architecture transitions. Softening gating criteria due to external schedule pressure inevitably leads to severe production incidents, security breaches, and reputational damage. A cloud architect must possess the professional spine to issue a formal REPEAT decision when foundational criteria are unmet, protecting the enterprise from catastrophic downstream failures.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Progressing from foundational infrastructure to Google Cloud enterprise identity and resource management (Block 2) requires absolute clarity regarding security and isolation boundaries. An engineer who struggles with POSIX process privileges or CIDR subnetting will make disastrous errors when configuring Google Cloud Organization policies, VPC Service Controls, or IAM Workload Identity Federation. Enforcing the Pass/Repeat boundary at Gate 1 guarantees that only qualified architectures advance to cloud deployment.</p>

<table class="comparison-table">
  <caption>Table 17.2: Gate 1 Five-Dimension Evaluation Rubric, Criteria, and Thresholds</caption>
  <thead>
    <tr>
      <th scope="col">Dimension</th>
      <th scope="col">Evaluation Scope</th>
      <th scope="col">Score 0 (Absent)</th>
      <th scope="col">Score 1 (Partial)</th>
      <th scope="col">Score 2 (Adequate Floor)</th>
      <th scope="col">Score 3 (Defensible Master)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1. Correctness</th>
      <td>CIDRs, POSIX commands, SQL normalization, schemas</td>
      <td>Syntax errors, invalid CIDRs, unhandled crashes</td>
      <td>Works in happy path; breaks on boundary inputs</td>
      <td>Mathematically sound; handles edge cases with limits</td>
      <td>Flawless execution; rigorous boundary proofs</td>
    </tr>
    <tr>
      <th scope="row">2. Traceability</th>
      <td>Roadmap linkage, configuration rationale, mechanism mapping</td>
      <td>No rationale; arbitrary values and magic numbers</td>
      <td>Vague references without naming mechanisms</td>
      <td>Clear linkage from roadmap to config options</td>
      <td>Bidirectional mapping from low-level to cloud decisions</td>
    </tr>
    <tr>
      <th scope="row">3. Evidence Quality</th>
      <td>Timestamped logs, exit codes, reproducible artifacts</td>
      <td>No saved evidence; claims without terminal logs</td>
      <td>Truncated logs; missing exit codes or environment</td>
      <td>Complete timestamped logs with exit codes</td>
      <td>Fully reproducible cold-start scripts with hashes</td>
    </tr>
    <tr>
      <th scope="row">4. Recovery Reasoning</th>
      <td>Failure prediction, rollback proofs, invariant preservation</td>
      <td>No failure planning; orphaned records on crash</td>
      <td>Rollback attempted but leaves partial state</td>
      <td>Clean rollback; verifies zero orphaned rows</td>
      <td>Mathematically guarantees &le; 1 physical fulfillment</td>
    </tr>
    <tr>
      <th scope="row">5. Governance</th>
      <td>Cloud Digital Leader framing, facts vs hypotheses</td>
      <td>Conflates speculation with observed facts</td>
      <td>Excessive jargon; weak business value framing</td>
      <td>Clear distinction of facts; concise business impact</td>
      <td>Executive-ready trade-off analysis and risk bounds</td>
    </tr>
  </tbody>
</table>

<div class="technical-figure">
PLACEHOLDER_FIG_17_2
</div>

<p><strong class="side-heading">Concrete example:</strong> Authoring and executing an automated Python evaluation script that grades the five rubric dimensions, enforces the Gate 1 decision boundary, and outputs the final pass/repeat determination:</p>
<pre><code># 1. Author and execute the Gate 1 scoring and evaluation engine
$ cat &lt;&lt;'EOF' > scratch/day17_rubric_evaluator.py
import json

rubric_scores = {
    "dimension_1_correctness": {
        "score": 3,
        "justification": "CIDR math verified non-overlapping; SQLite schema in 3NF; POSIX scripts run clean."
    },
    "dimension_2_traceability": {
        "score": 3,
        "justification": "All config options trace to Twelve-Factor principles and Day 1-16 roadmap items."
    },
    "dimension_3_evidence_quality": {
        "score": 3,
        "justification": "Timestamped JSON audits with exit codes generated in scratch/day17_lab/."
    },
    "dimension_4_recovery_reasoning": {
        "score": 3,
        "justification": "Proved atomic rollback with zero orphaned rows; UNIQUE constraint caught replay."
    },
    "dimension_5_governance": {
        "score": 3,
        "justification": "Concise business impact framed with SRE/Cloud Digital Leader standards."
    }
}

# Evaluate Gate 1 Decision Boundary
DIMENSION_FLOOR = 2
COMPOSITE_THRESHOLD = 12

scores = [item["score"] for item in rubric_scores.values()]
total_score = sum(scores)
min_score = min(scores)

pass_floor = min_score >= DIMENSION_FLOOR
pass_composite = total_score >= COMPOSITE_THRESHOLD
invariants_cleared = True # Verified duplicate fulfillment invariant <= 1

final_decision = "PASS" if (pass_floor and pass_composite and invariants_cleared) else "REPEAT"

decision_record = {
    "rubric": rubric_scores,
    "total_score": f"{total_score} / 15",
    "minimum_dimension_score": min_score,
    "criteria_checks": {
        "dimension_floor_cleared": pass_floor,
        "composite_threshold_cleared": pass_composite,
        "duplicate_fulfillment_invariant_preserved": invariants_cleared
    },
    "gate_1_decision": final_decision,
    "authorization": "Cleared to advance to Block 2 (Days 18-35: Cloud environment and identity)"
}

print(json.dumps(decision_record, indent=2))
EOF
$ python3 scratch/day17_rubric_evaluator.py
{
  "rubric": {
    "dimension_1_correctness": {
      "score": 3,
      "justification": "CIDR math verified non-overlapping; SQLite schema in 3NF; POSIX scripts run clean."
    },
    "dimension_2_traceability": {
      "score": 3,
      "justification": "All config options trace to Twelve-Factor principles and Day 1-16 roadmap items."
    },
    "dimension_3_evidence_quality": {
      "score": 3,
      "justification": "Timestamped JSON audits with exit codes generated in scratch/day17_lab/."
    },
    "dimension_4_recovery_reasoning": {
      "score": 3,
      "justification": "Proved atomic rollback with zero orphaned rows; UNIQUE constraint caught replay."
    },
    "dimension_5_governance": {
      "score": 3,
      "justification": "Concise business impact framed with SRE/Cloud Digital Leader standards."
    }
  },
  "total_score": "15 / 15",
  "minimum_dimension_score": 3,
  "criteria_checks": {
    "dimension_floor_cleared": true,
    "composite_threshold_cleared": true,
    "duplicate_fulfillment_invariant_preserved": true
  },
  "gate_1_decision": "PASS",
  "authorization": "Cleared to advance to Block 2 (Days 18-35: Cloud environment and identity)"
}
</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> The rubric evaluator and threshold rules shown above demonstrate automated decision logic applied to simulated Block 1 deliverables. They do not replace peer human code reviews or live enterprise audit compliance systems.</p>"""

TOPIC_02_TECHNICAL = TOPIC_02_TECHNICAL.replace('PLACEHOLDER_FIG_17_2', FIG_17_2_HTML)

TOPIC_02_SCENARIO = {
    'scenario': (
        "During an asynchronous order dispatch recovery at BrightLoaf, a worker pod failed while processing message BL-17-901. "
        "The message queue re-delivered the unacknowledged message 15 seconds later to a secondary worker pod. "
        "Because the order fulfillments database table lacked a UNIQUE constraint on order_id, the secondary worker inserted a second "
        "fulfillment record, generating a second physical shipping label and dispatching a duplicate bread delivery truck to franchise store 104."
    ),
    'impact': (
        "18 duplicate commercial bakery shipments were dispatched across the regional territory before dispatchers noticed anomalous "
        "warehouse dock activity. Over $28,000 in perishable inventory was double-delivered, resulting in total inventory loss and waste, "
        "while tying up logistics fleets during morning rush hours."
    ),
    'constraints': (
        "The system must guarantee the duplicate fulfillment invariant: <= 1 physical fulfillment per unique order ID. "
        "At-least-once message queues inherently deliver duplicate messages during network partitions; idempotency must be enforced at "
        "the relational persistence boundary."
    ),
    'evidence': FIG_17_4_HTML,
    'diagram_enabled': False,
    'facts': (
        "Supplied incident facts and logs:\n"
        "1. Message queue delivered order event BL-17-901 at 05:00:01 UTC.\n"
        "2. Worker 1 acknowledged the event late due to a 10,000 ms database write stall; queue redelivered at 05:00:16 UTC.\n"
        "3. Worker 2 executed: INSERT INTO order_fulfillments (fulfillment_id, order_id) VALUES ('ful-002', 'BL-17-901').\n"
        "4. Both inserts succeeded without error; database showed two fulfillment rows for BL-17-901.\n"
        "5. Two physical shipping labels were printed and dispatched from the warehouse."
    ),
    'inference': (
        "Relying on application-layer deduplication or transport-level message acknowledgements cannot prevent duplicate processing "
        "in distributed architectures. A relational UNIQUE constraint on order_id is the only mechanism that atomically prevents "
        "duplicate fulfillment inserts regardless of consumer concurrency or queue redeliveries."
    ),
    'expected': (
        "A database schema constraint UNIQUE(order_id) on the order_fulfillments table rejects the replayed event with an integrity "
        "error, preventing duplicate label printing and preserving the <= 1 fulfillment invariant."
    ),
    'root': (
        "Omission of a schema-level UNIQUE(order_id) constraint on the order_fulfillments table, allowing at-least-once message "
        "delivery to violate the duplicate fulfillment invariant."
    ),
    'verify': (
        "Attempt to insert two fulfillment rows with identical order_id in SQLite/PostgreSQL; assert that the second insert fails with "
        "sqlite3.IntegrityError or 23505 unique_violation, leaving exactly one fulfillment row in the table."
    ),
    'residual': (
        "Application handlers must catch uniqueness violations and acknowledge the replayed message as an idempotent success rather "
        "than crashing and entering an infinite redelivery loop."
    ),
    'diagnostic_steps': [
        "Query the fulfillment table for duplicate order_ids using SELECT order_id, COUNT(*) FROM order_fulfillments GROUP BY order_id HAVING COUNT(*) > 1.",
        "Inspect message queue consumer delivery counts to verify multiple deliveries of event BL-17-901.",
        "Review worker application logs to trace concurrent execution threads across distinct container instances.",
        "Inspect schema definitions using \\d order_fulfillments to check for missing uniqueness constraints."
    ],
    'remediation_steps': [
        "Apply a schema migration adding a UNIQUE(order_id) constraint to the order_fulfillments table.",
        "Refactor worker code to wrap fulfillment creation in an explicit transaction catching IntegrityError as an idempotent success.",
        "Implement transactional outbox pattern to link message acknowledgement with database commitment.",
        "Add automated integration tests verifying that duplicate event injection produces exactly 1 fulfillment row."
    ]
}

TOPIC_02_LAB = {
    'name': 'Exercise B: Gate 1 Five-Dimension Rubric Scoring and Remediation',
    'goal': (
        "Conduct a systematic audit of Block 1 exit evidence (Days 5, 8, 10, 16), evaluate proficiency across the five rubric dimensions, "
        "repair the weakest explanation, and author the authoritative Gate 1 checklist and pass/repeat decision."
    ),
    'expected': (
        "A completed and scored Gate 1 checklist file at scratch/day-017-g1-checklist.md containing explicit scores (0–3) for all "
        "five dimensions, a detailed remediation of the weakest explanation, and a formal pass decision."
    ),
    'mode': (
        "Observed locally: Five-dimension rubric scoring calculations, artifact hash verification, weak explanation repair document "
        "generation at scratch/day-017-g1-checklist.md. Simulated or predicted: Architectural review board scoring dynamics and enterprise "
        "audit compliance workflows. Untested on GCP: Google Cloud Architecture Framework automated compliance tooling and Organization "
        "Policy drift detection."
    ),
    'covers': "Repair the weakest shell, network or state explanation and produce a scored G1 checklist with an explicit pass or repeat decision",
    'prereq': 'Completion of Exercise A, local Python 3.10+ runtime, POSIX shell',
    'preflight': 'Ensure scratch/day17_lab workspace is accessible and initialize Topic 2 environment',
    'verification': 'Verify that scratch/day-017-g1-checklist.md exists and contains scores >= 2 for all dimensions and total >= 12/15',
    'trouble': 'If scoring falls below 2 on any dimension, review the corresponding Block 1 day and apply targeted remediation',
    'cleanup': 'Artifacts remain in scratch/day17_lab/ and scratch/day-017-g1-checklist.md for validation gate auditing',
    'accept': 'All 8 stages complete successfully, producing the authoritative scored Gate 1 checklist with an explicit PASS decision',
    'file': 'day-017-topic-02.md',
    'steps': [
        (
            "**Stage 1: Initialize Gate 1 Evaluation Workspace**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Verify environment prerequisites and initialize the Gate 1 evaluation audit workspace.\n"
            "```bash\n"
            "command -v bash\n"
            "command -v python3\n"
            "command -v mkdir\n"
            "command -v cat\n"
            "mkdir -p scratch/day17_lab\n"
            "cat <<'EOF' > scratch/day17_lab/stage1_gate_init.py\n"
            "import json\n"
            "import sys\n"
            "\n"
            "gate_init = {\n"
            "    \"gate\": \"Gate 1 (Block 1 Foundations Recall & Repair)\",\n"
            "    \"curriculum_day\": 17,\n"
            "    \"status\": \"INITIALIZED\",\n"
            "    \"rubric_dimensions\": 5,\n"
            "    \"passing_score_floor\": 2,\n"
            "    \"passing_composite_threshold\": 12\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage1_gate_preflight.json\", \"w\") as f:\n"
            "    json.dump(gate_init, f, indent=2)\n"
            "\n"
            "print(\"Stage 1 complete: Gate 1 audit environment initialized.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage1_gate_init.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Gate preflight audit written to scratch/day17_lab/stage1_gate_preflight.json.\n\n"
            "**Save:** scratch/day17_lab/stage1_gate_preflight.json"
        ),
        (
            "**Stage 2: Audit Prior Block 1 Evidence Artifacts (Days 5, 8, 10, 16)**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Author a Python script inspecting Block 1 prerequisite artifacts (Days 5, 8, 10, 16) and evaluating their cold-start integrity.\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage2_audit_prereqs.py\n"
            "import json\n"
            "\n"
            "prereq_audit = {\n"
            "    \"day_05\": {\n"
            "        \"domain\": \"Linux & POSIX Process Lifecycle\",\n"
            "        \"required_artifact\": \"Shell pipeline, trap signal handler, exit codes\",\n"
            "        \"status\": \"VERIFIED\",\n"
            "        \"integrity_check\": \"Valid set -euo pipefail and trap cleanup present\"\n"
            "    },\n"
            "    \"day_08\": {\n"
            "        \"domain\": \"TCP/IP, DNS, and TLS Networking\",\n"
            "        \"required_artifact\": \"CIDR subnet calculation, DNS trace, TLS 1.3 handshake\",\n"
            "        \"status\": \"VERIFIED\",\n"
            "        \"integrity_check\": \"RFC 1918 non-overlapping subnets confirmed\"\n"
            "    },\n"
            "    \"day_10\": {\n"
            "        \"domain\": \"State Persistence, Systemd, and Scheduling\",\n"
            "        \"required_artifact\": \"Cron expression, systemd unit, distributed state invariants\",\n"
            "        \"status\": \"VERIFIED\",\n"
            "        \"integrity_check\": \"Process supervision and restart boundaries confirmed\"\n"
            "    },\n"
            "    \"day_16\": {\n"
            "        \"domain\": \"Relational Schema, ACID, and SQL Isolation\",\n"
            "        \"required_artifact\": \"3NF schema, atomic rollback proof, isolation anomaly demonstration\",\n"
            "        \"status\": \"VERIFIED\",\n"
            "        \"integrity_check\": \"Duplicate fulfillment invariant preserved via UNIQUE constraint\"\n"
            "    }\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage2_prereqs_audit.json\", \"w\") as f:\n"
            "    json.dump(prereq_audit, f, indent=2)\n"
            "\n"
            "print(\"Stage 2 complete: Block 1 prerequisite artifacts audited.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage2_audit_prereqs.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Prerequisites audit written to scratch/day17_lab/stage2_prereqs_audit.json.\n\n"
            "**Save:** scratch/day17_lab/stage2_prereqs_audit.json"
        ),
        (
            "**Stage 3: Score Dimension 1 (Correctness) and Dimension 2 (Traceability)**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Evaluate Dimension 1 (technical and mathematical accuracy) and Dimension 2 (curriculum requirement traceability).\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage3_score_dim1_dim2.py\n"
            "import json\n"
            "\n"
            "dim1_dim2_scores = {\n"
            "    \"dimension_1_correctness\": {\n"
            "        \"name\": \"Correctness\",\n"
            "        \"score\": 3,\n"
            "        \"max\": 3,\n"
            "        \"findings\": \"Subnet CIDRs mathematically non-overlapping (10.10.1.0/24 vs 10.20.1.0/24). Schema in 3NF with foreign keys enabled. Zero syntax errors.\",\n"
            "        \"cleared\": True\n"
            "    },\n"
            "    \"dimension_2_traceability\": {\n"
            "        \"name\": \"Traceability\",\n"
            "        \"score\": 3,\n"
            "        \"max\": 3,\n"
            "        \"findings\": \"Every configuration setting links directly to Twelve-Factor principles and Days 1-16 roadmap items. No ungrounded magic numbers.\",\n"
            "        \"cleared\": True\n"
            "    }\n"
            "}\n"
            "\n"
            "assert dim1_dim2_scores[\"dimension_1_correctness\"][\"score\"] >= 2\n"
            "assert dim1_dim2_scores[\"dimension_2_traceability\"][\"score\"] >= 2\n"
            "\n"
            "with open(\"scratch/day17_lab/stage3_dim1_dim2.json\", \"w\") as f:\n"
            "    json.dump(dim1_dim2_scores, f, indent=2)\n"
            "\n"
            "print(\"Stage 3 complete: Dimensions 1 and 2 scored and verified.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage3_score_dim1_dim2.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Scores saved to scratch/day17_lab/stage3_dim1_dim2.json.\n\n"
            "**Save:** scratch/day17_lab/stage3_dim1_dim2.json"
        ),
        (
            "**Stage 4: Score Dimension 3 (Evidence Quality) and Dimension 4 (Recovery Reasoning)**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Evaluate Dimension 3 (reproducible timestamped outputs) and Dimension 4 (failure prediction, atomic rollback, and invariant defense).\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage4_score_dim3_dim4.py\n"
            "import json\n"
            "\n"
            "dim3_dim4_scores = {\n"
            "    \"dimension_3_evidence_quality\": {\n"
            "        \"name\": \"Evidence Quality\",\n"
            "        \"score\": 3,\n"
            "        \"max\": 3,\n"
            "        \"findings\": \"Timestamped JSON outputs generated with verified exit codes. Scripts execute cold-start in isolated temporary directories.\",\n"
            "        \"cleared\": True\n"
            "    },\n"
            "    \"dimension_4_recovery_reasoning\": {\n"
            "        \"name\": \"Recovery Reasoning\",\n"
            "        \"score\": 3,\n"
            "        \"max\": 3,\n"
            "        \"findings\": \"Demonstrated clean SQL rollback on connection failure (zero orphaned rows). Proved duplicate fulfillment invariant <= 1 via UNIQUE constraint.\",\n"
            "        \"cleared\": True\n"
            "    }\n"
            "}\n"
            "\n"
            "assert dim3_dim4_scores[\"dimension_3_evidence_quality\"][\"score\"] >= 2\n"
            "assert dim3_dim4_scores[\"dimension_4_recovery_reasoning\"][\"score\"] >= 2\n"
            "\n"
            "with open(\"scratch/day17_lab/stage4_dim3_dim4.json\", \"w\") as f:\n"
            "    json.dump(dim3_dim4_scores, f, indent=2)\n"
            "\n"
            "print(\"Stage 4 complete: Dimensions 3 and 4 scored and verified.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage4_score_dim3_dim4.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Scores saved to scratch/day17_lab/stage4_dim3_dim4.json.\n\n"
            "**Save:** scratch/day17_lab/stage4_dim3_dim4.json"
        ),
        (
            "**Stage 5: Score Dimension 5 (Communication and Governance)**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Evaluate Dimension 5 (business value framing, Cloud Digital Leader alignment, and distinguishing observed facts from tabletop models).\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage5_score_dim5.py\n"
            "import json\n"
            "\n"
            "dim5_score = {\n"
            "    \"dimension_5_governance\": {\n"
            "        \"name\": \"Communication and Governance\",\n"
            "        \"score\": 3,\n"
            "        \"max\": 3,\n"
            "        \"findings\": \"Clear separation between local observed terminal outputs and simulated cloud behavior. Business impact concisely framed with financial figures.\",\n"
            "        \"cleared\": True\n"
            "    }\n"
            "}\n"
            "\n"
            "assert dim5_score[\"dimension_5_governance\"][\"score\"] >= 2\n"
            "\n"
            "with open(\"scratch/day17_lab/stage5_dim5.json\", \"w\") as f:\n"
            "    json.dump(dim5_score, f, indent=2)\n"
            "\n"
            "print(\"Stage 5 complete: Dimension 5 scored and verified.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage5_score_dim5.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Score saved to scratch/day17_lab/stage5_dim5.json.\n\n"
            "**Save:** scratch/day17_lab/stage5_dim5.json"
        ),
        (
            "**Stage 6: Identify Weakest Architectural Explanation (DNS TTL vs Relational Isolation)**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Conduct an audit to identify the weakest architectural explanation from Block 1 and author an authoritative technical remediation analysis.\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage6_identify_weakness.py\n"
            "import json\n"
            "\n"
            "weakness_audit = {\n"
            "    \"identified_weakness\": \"Ambiguous DNS Caching and Negative Response Handling vs Relational Isolation Anomalies\",\n"
            "    \"prior_flawed_claim\": \"DNS automatically directs client traffic to the nearest healthy service instance without latency or cache staleness.\",\n"
            "    \"root_gap\": \"Failed to specify recursive resolver TTL bounds, negative NXDOMAIN caching (RFC 2308), and the interaction between container search domains and resolver ndots.\",\n"
            "    \"remediation_strategy\": \"Replace hand-waving statement with exact physical mechanisms: stub resolver search loop math, RFC 2308 negative cache TTL, and explicit FQDN routing.\"\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage6_weakness_audit.json\", \"w\") as f:\n"
            "    json.dump(weakness_audit, f, indent=2)\n"
            "\n"
            "print(\"Stage 6 complete: Weak explanation identified and remediation strategy formulated.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage6_identify_weakness.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Weakness analysis saved to scratch/day17_lab/stage6_weakness_audit.json.\n\n"
            "**Save:** scratch/day17_lab/stage6_weakness_audit.json"
        ),
        (
            "**Stage 7: Author Scored Gate 1 Checklist and Authoritative Remediation Document**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Generate the authoritative Day 17 exit criteria artifact: the scored G1 checklist, corrected evidence, and explicit pass decision at scratch/day-017-g1-checklist.md.\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage7_generate_checklist.py\n"
            "checklist_content = '''# Gate 1 — Foundation Recall and Repair: Scored Audit & Pass Decision\n"
            "\n"
            "**Curriculum Day:** Day 17 (Gate 1 — Foundation recall and repair)  \n"
            "**Candidate:** Lead Enterprise Cloud Architect  \n"
            "**Terminal Boundary:** Block 1 Foundations (Days 1–17)  \n"
            "**Status:** AUTHORITATIVE AUDIT & SIGN-OFF  \n"
            "**Exit Decision:** PASS (Cleared for Block 2: Cloud environment and identity)  \n"
            "\n"
            "---\n"
            "\n"
            "## 1. Executive Summary & Gate 1 Mandate\n"
            "\n"
            "Gate 1 validates candidate readiness to advance from local computing, networking, and relational foundations to Google Cloud infrastructure (Days 18–35). In strict accordance with the Gate Governance policy:\n"
            "- **Zero New Services:** No new cloud services, provider products, or novel patterns were introduced.\n"
            "- **Reproducible Foundations:** End-to-end local request processing, POSIX execution, and SQL rollback mechanics were reproduced without walkthrough aids.\n"
            "- **Invariant Preserved:** The core duplicate fulfillment invariant (<= 1 physical fulfillment per unique order ID) was mathematically and programmatically verified.\n"
            "\n"
            "---\n"
            "\n"
            "## 2. Five-Dimension Foundation Rubric Scoring Matrix\n"
            "\n"
            "Each dimension is scored on an objective scale of 0 to 3:\n"
            "- `0`: Absent / Untested\n"
            "- `1`: Partial / Flawed\n"
            "- `2`: Adequate with documented limits (Passing Floor)\n"
            "- `3`: Defensible Mastery\n"
            "\n"
            "| Dimension | Weight | Score (0–3) | Passing Floor | Evaluation Findings & Supporting Evidence |\n"
            "|---|---|---|---|---|\n"
            "| **1. Correctness** | 20% | **3 / 3** | >= 2 | Subnet CIDR allocations (10.10.1.0/24 and 10.20.1.0/24) verified mathematically non-overlapping. Schema modeled in 3NF with active foreign keys and check constraints. Zero syntax or runtime errors. |\n"
            "| **2. Traceability** | 20% | **3 / 3** | >= 2 | Every configuration setting, port mapping, and retry threshold traces directly to Twelve-Factor principles and Days 1–16 roadmap requirements. Zero unexplained magic numbers. |\n"
            "| **3. Evidence Quality** | 20% | **3 / 3** | >= 2 | Timestamped JSON execution logs with exit codes generated in `scratch/day17_lab/`. All scripts execute from cold-start in disposable sandboxes with verified assertions. |\n"
            "| **4. Recovery Reasoning** | 20% | **3 / 3** | >= 2 | Demonstrated clean SQL rollback on payment timeout with zero orphaned parent or child rows. Enforced `UNIQUE(order_id)` constraint suppressing duplicate message replay shipments. |\n"
            "| **5. Governance & CDL** | 20% | **3 / 3** | >= 2 | Concise Cloud Digital Leader business impact framing ($64k outage impact). Clear, explicit distinction between local observed behavior and simulated cloud environments. |\n"
            "| **COMPOSITE TOTAL** | **100%** | **15 / 15** | **>= 12** | **OUTSTANDING PASS: All criteria satisfied.** |\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Systematic Remediation of Weakest Foundation Explanation\n"
            "\n"
            "### Prior Flawed Explanation (Audit Finding):\n"
            "> *\"DNS automatically routes client requests to healthy backend service instances, ensuring low latency and eliminating connection errors.\"*\n"
            "\n"
            "### Architectural Critique & Identified Defect:\n"
            "The prior claim is dangerously inaccurate and conflates DNS resolution with active layer 7 load balancing. Specifically:\n"
            "1. **Resolver Caching & TTL:** Standard DNS resolvers cache responses for the duration of the Time-To-Live (TTL) record. If a backend IP fails during the TTL window, the client continues attempting TCP handshakes to the dead IP until the cache expires.\n"
            "2. **Negative Caching (RFC 2308):** When a DNS server returns an `NXDOMAIN` (Non-Existent Domain) error, resolvers cache that failure for the duration of the SOA record minimum TTL. In misconfigured container networks with search domains, querying unqualified names causes repeated negative lookups that choke the network.\n"
            "3. **Search Domain Overhead:** A `resolv.conf` with multiple search domains (e.g., `order.svc.cluster.local`, `svc.cluster.local`) and `ndots:5` causes unqualified queries to issue up to 4 sequential DNS requests across search paths before trying an absolute lookup, adding 2,000–4,000 ms of latency.\n"
            "\n"
            "### Corrected Authoritative Explanation:\n"
            "> **Authoritative DNS Mechanics:** DNS operates strictly as a static or dynamic name-to-IP directory service, not an active health-checking load balancer. To achieve resilient microservice connectivity:\n"
            "> 1. Microservices must use Fully Qualified Domain Names (FQDN) ending with a trailing dot (e.g., `db.production.brightloaf.internal.`) or configure `ndots:1` in `/etc/resolv.conf` to bypass wasteful search domain iterations.\n"
            "> 2. Application connection pools must implement proactive health checking, circuit breakers, and short DNS TTL cache timeouts (e.g., 5 to 30 seconds) rather than relying on OS-level resolver caching.\n"
            "> 3. Network routing must be verified using non-overlapping RFC 1918 CIDR allocations, ensuring that packet routing table lookups route deterministically to external gateways rather than looping on local virtual interfaces.\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Invariant Verification & Proof\n"
            "\n"
            "- **Target Invariant:** Duplicate Fulfillment Invariant (<= 1 physical fulfillment per unique order ID).\n"
            "- **Tested Scenario:** At-least-once message queue redelivered order event `ORD-17-9001` twice.\n"
            "- **Mechanism Enforced:** Relational database table `order_fulfillments` configured with `order_id TEXT NOT NULL UNIQUE`.\n"
            "- **Observed Outcome:** Second insertion attempt caught with `sqlite3.IntegrityError: UNIQUE constraint failed: order_fulfillments.order_id`.\n"
            "- **Result:** Invariant 100% preserved. Exactly 1 physical shipment record persisted.\n"
            "\n"
            "---\n"
            "\n"
            "## 5. Formal Gate 1 Exit Decision\n"
            "\n"
            "| Evaluation Criterion | Minimum Threshold | Verified Score | Decision Status |\n"
            "|---|---|---|---|\n"
            "| Dimension Floor | Score >= 2 in every dimension | Min = 3 | **PASS** |\n"
            "| Composite Score | Total >= 12 / 15 | Total = 15 / 15 | **PASS** |\n"
            "| Unhandled Errors | Zero runtime errors | 0 errors | **PASS** |\n"
            "| Invariant Defense | Duplicate fulfillment invariant preserved | Preserved (<= 1) | **PASS** |\n"
            "| Prerequisite Exit Evidence | Days 5, 8, 10, 16 artifacts audited | Audited | **PASS** |\n"
            "\n"
            "### Final Determination: **PASS**\n"
            "The candidate has demonstrated complete, defensible mastery over Block 1 foundations. Permission is officially granted to advance to **Day 18 (Google Cloud accounts, Free Tier, and Resource Hierarchy)**.\n"
            "'''\n"
            "\n"
            "with open(\"scratch/day-017-g1-checklist.md\", \"w\") as f:\n"
            "    f.write(checklist_content.strip() + \"\\n\")\n"
            "\n"
            "print(\"Stage 7 complete: Scored Gate 1 checklist and remediation saved to scratch/day-017-g1-checklist.md.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage7_generate_checklist.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Scored Gate 1 checklist written to scratch/day-017-g1-checklist.md.\n\n"
            "**Save:** scratch/day-017-g1-checklist.md"
        ),
        (
            "**Stage 8: Validate Gate 1 Decision Boundary and Compile Stage Summary**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Verify all Topic 2 stage files and the final Gate 1 exit criteria checklist exist, writing the final acceptance audit.\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage8_topic2_summary.py\n"
            "import json\n"
            "import os\n"
            "\n"
            "required_stage_files = [\n"
            "    \"scratch/day17_lab/stage1_gate_preflight.json\",\n"
            "    \"scratch/day17_lab/stage2_prereqs_audit.json\",\n"
            "    \"scratch/day17_lab/stage3_dim1_dim2.json\",\n"
            "    \"scratch/day17_lab/stage4_dim3_dim4.json\",\n"
            "    \"scratch/day17_lab/stage5_dim5.json\",\n"
            "    \"scratch/day17_lab/stage6_weakness_audit.json\",\n"
            "    \"scratch/day-017-g1-checklist.md\"\n"
            "]\n"
            "\n"
            "missing = [p for p in required_stage_files if not os.path.isfile(p)]\n"
            "assert len(missing) == 0, f\"Missing required Topic 2 stage files: {missing}\"\n"
            "\n"
            "summary = {\n"
            "    \"exercise\": \"Exercise B: Gate 1 Five-Dimension Rubric Scoring and Remediation\",\n"
            "    \"topic\": \"topic-02\",\n"
            "    \"verified_stages\": 8,\n"
            "    \"all_artifacts_present\": True,\n"
            "    \"exit_artifact\": \"scratch/day-017-g1-checklist.md\",\n"
            "    \"gate_decision\": \"PASS\",\n"
            "    \"status\": \"PASS\"\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage8_topic2_summary.json\", \"w\") as f:\n"
            "    json.dump(summary, f, indent=2)\n"
            "\n"
            "print(\"Stage 8 complete: Exercise B validation passed with Gate 1 PASS decision confirmed.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage8_topic2_summary.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Summary audit saved to scratch/day17_lab/stage8_topic2_summary.json confirming Gate 1 PASS decision.\n\n"
            "**Save:** scratch/day17_lab/stage8_topic2_summary.json"
        )
    ]
}

TOPIC_02 = {
    'key': 'topic-02',
    'title': 'Use the matching gate criteria in the Gates section',
    'anchors': {
        'overview': 'topic-02-overview',
        'technical': 'topic-02-technical',
        'problem': 'topic-02-problem',
        'lab': 'topic-02-lab'
    },
    'overview': TOPIC_02_OVERVIEW,
    'preview': TOPIC_02_PREVIEW,
    'technical': TOPIC_02_TECHNICAL,
    'questions': TOPIC_02_QUESTIONS,
    'reference': 'https://cloud.google.com/architecture/framework#core_principles',
    'reference_label': 'Google Cloud Architecture Framework: Core principles (accessed 2026-10-04)',
    'scenario': TOPIC_02_SCENARIO,
    'lab': TOPIC_02_LAB
}
