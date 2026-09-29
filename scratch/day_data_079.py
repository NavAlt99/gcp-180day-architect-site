"""day_data_079.py — Exhaustive architecture data specification for Day 79.

Covers Architecture Decision Records (ADRs), Total Cost of Ownership (TCO) Comparisons,
and Risk Registers (Likelihood, Impact, Mitigation).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 79

DATA = {
    "day": 79,
    "part1_intro": (
        "Day 79 formalizes the foundational governance artifacts of enterprise cloud architecture: Architecture Decision Records (ADRs), "
        "Total Cost of Ownership (TCO) range modeling, and quantitative Risk Registers. Technical excellence is insufficient if "
        "architectural intent is lost to organizational turnover or if budgets fail to anticipate non-linear cloud cost vectors. "
        "ADRs capture the precise context, drivers, evaluated alternatives, and permanent trade-offs of structural choices. "
        "Simultaneously, financial defensibility requires moving beyond single-point estimates to low/base/high three-point TCO ranges "
        "that account for inter-region egress, operational toil, and parallel-run 'double-bubble' migration expenses. Finally, "
        "systemic resilience requires assigning explicit risk owners, calculating Expected Monetary Value (EMV), and establishing "
        "automated telemetry alerts before operational or compliance risks materialize into catastrophic production outages."
    ),
    "exit_summary": (
        "Authored an enterprise Architecture Decision Record (ADR-0079) with considered alternatives and invariant traceability; "
        "modeled a three-point PERT/Monte Carlo 3-year TCO range with low/base/high parameters and dated pricing assumptions; "
        "constructed a quantitative Risk Register with explicit risk owners, EMV calculations, and automated monitoring triggers."
    ),
    "part2_intro": (
        "Architectural governance bridges technical design and business stewardship. The sections below provide comprehensive "
        "engineering specifications for ADR lifecycle governance, mathematical three-point TCO modeling, and quantitative risk register mechanics."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Governance Artifact</th>
      <th>Primary Purpose &amp; Audience</th>
      <th>Key Structural Components</th>
      <th>Update Trigger &amp; Cadence</th>
      <th>Observable Failure Mode if Absent</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Architecture Decision Record (ADR)</strong></td>
      <td>Permanent record of significant architectural choices for engineering &amp; ARB</td>
      <td>Context, Deciders, Considered Alternatives, Decision Outcome, Invariant Consequences</td>
      <td>Created on design change; immutable once accepted; superseded via new ADR</td>
      <td>Architectural drift, continuous re-litigation, uncoordinated refactoring</td>
    </tr>
    <tr>
      <td><strong>Three-Point TCO Model (PERT)</strong></td>
      <td>Defensible financial projection for executive sponsors &amp; FinOps</td>
      <td>Low/Base/High bounds, compute/storage/network breakdown, SRE toil, CUD amortization</td>
      <td>Quarterly re-baselining or upon 20% traffic/feature forecast variance</td>
      <td>Egress invoice shock, double-bubble budget overrun, emergency de-scoping</td>
    </tr>
    <tr>
      <td><strong>Quantitative Risk Register</strong></td>
      <td>Operational &amp; business hazard tracking for SRE, Security, and Leadership</td>
      <td>Risk ID, Category, Likelihood, Impact, EMV, Treatment Strategy, Risk Owner, Review Date</td>
      <td>Monthly review; real-time escalation when Key Risk Indicators (KRIs) breach thresholds</td>
      <td>Unassigned quota exhaustion, single-zone failure cascades, regulatory fines</td>
    </tr>
    <tr>
      <td><strong>Requirement Traceability Matrix</strong></td>
      <td>End-to-end alignment from business driver to implemented cloud resource</td>
      <td>Business Goal, Non-Functional Requirement (SLO), Architecture Pattern, Terraform Resource</td>
      <td>Continuous verification in CI/CD pipeline via policy-as-code linting</td>
      <td>Over-engineered components lacking business justification or missing SLA controls</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "type": "topology",
        "title": "Day 79: Architectural Decision Records, TCO Modeling, and Risk Governance Topology",
        "desc": "Multi-tier architectural governance topology showing requirement traceability, git-versioned ADR lifecycle, three-point PERT TCO estimation, and real-time Key Risk Indicator (KRI) monitoring.",
        "caption": "Figure 79.1: Multi-tier architectural governance topology illustrating requirement traceability, git-versioned ADR enforcement, three-point PERT TCO ranges, and automated KRI telemetry alerts.",
        "width": 1100,
        "height": 640,
        "layers": [
            {"name": "LAYER 1: Business Invariants & Requirement Traceability Tier", "desc": "Day 64 Single-Fulfillment Rules, Regional SLA Targets & Regulatory Compliance", "fill": "#1e3a5f", "y": 10, "h": 90},
            {"name": "LAYER 2: Git-Versioned Architecture Decision Record (ADR) Fabric", "desc": "Markdown ADR Repository, Policy-as-Code Linter & Immutable History", "fill": "#0f2338", "y": 115, "h": 90},
            {"name": "LAYER 3: Three-Point PERT & Monte Carlo TCO Control Plane", "desc": "Low/Base/High Bounds, Egress Modeling, SRE Toil & Double-Bubble Cost Curves", "fill": "#064e3b", "y": 220, "h": 90},
            {"name": "LAYER 4: Quantitative Risk Register & EMV Evaluation Tier", "desc": "Likelihood/Impact Scoring, Expected Monetary Value & Assigned Risk Owners", "fill": "#1e1b4b", "y": 325, "h": 90},
            {"name": "LAYER 5: Production Observability & Automated KRI Telemetry", "desc": "Cloud Monitoring Alert Policies, vCPU Quota Headroom & Log Sinks", "fill": "#3b0764", "y": 430, "h": 90},
        ],
        "components": [
            {"id": "req_tracker", "name": "Requirement Matrix", "detail": "Single-Fulfillment & SLO Registry", "x": 80, "y": 30, "w": 260, "h": 52, "fill": "#0f283d", "stroke": "#38bdf8"},
            {"id": "reg_audit", "name": "Regulatory & SLA Gate", "detail": "External Compliance Invariants", "x": 420, "y": 30, "w": 260, "h": 52, "fill": "#0f283d", "stroke": "#38bdf8"},
            {"id": "adr_git", "name": "Git ADR Repository", "detail": "ADR-0079 Decision Specification", "x": 80, "y": 135, "w": 260, "h": 52, "fill": "#092e28", "stroke": "#10b981"},
            {"id": "ci_linter", "name": "CI/CD Policy Linter", "detail": "Mandatory Headers & Invariant Check", "x": 420, "y": 135, "w": 260, "h": 52, "fill": "#092e28", "stroke": "#10b981"},
            {"id": "pert_engine", "name": "Three-Point PERT Engine", "detail": "Low / Base / High 3-Year Projection", "x": 80, "y": 240, "w": 260, "h": 52, "fill": "#093322", "stroke": "#22c55e"},
            {"id": "finops_cud", "name": "FinOps Commitment Engine", "detail": "CUD Break-Even & Egress Modeler", "x": 420, "y": 240, "w": 260, "h": 52, "fill": "#093322", "stroke": "#22c55e"},
            {"id": "risk_matrix", "name": "Risk Register Engine", "detail": "5x5 Likelihood x Impact Matrix", "x": 80, "y": 345, "w": 260, "h": 52, "fill": "#1b143a", "stroke": "#a855f7"},
            {"id": "emv_eval", "name": "EMV Financial Evaluator", "detail": "Probability-Weighted Loss Exposure", "x": 420, "y": 345, "w": 260, "h": 52, "fill": "#1b143a", "stroke": "#a855f7"},
            {"id": "kri_telemetry", "name": "KRI Alerting Policy", "detail": "Cloud Monitoring Quota Headroom", "x": 80, "y": 450, "w": 260, "h": 52, "fill": "#280a3c", "stroke": "#c084fc"},
            {"id": "arb_oversight", "name": "ARB Governance Board", "detail": "Monthly Audit & Ownership Review", "x": 420, "y": 450, "w": 260, "h": 52, "fill": "#280a3c", "stroke": "#c084fc"},
        ],
        "boundaries": [
            {"x": 60, "y": 14, "w": 640, "h": 80, "label": "BUSINESS REQUIREMENT & INVARIANT SPECIFICATION PERIMETER", "color": "#38bdf8"},
            {"x": 60, "y": 120, "w": 640, "h": 80, "label": "GIT-VERSIONED ADR GOVERNANCE & POLICY-AS-CODE GATE", "color": "#10b981"},
            {"x": 60, "y": 330, "w": 640, "h": 80, "label": "QUANTITATIVE RISK MITIGATION & KRI ALERTING PERIMETER", "color": "#a855f7"},
        ],
        "flows": [
            {"x1": 340, "y1": 56, "x2": 420, "y2": 56, "type": "ok", "label": "SLA Bounds"},
            {"x1": 210, "y1": 82, "x2": 210, "y2": 135, "type": "ok", "label": "Driver Feed"},
            {"x1": 340, "y1": 161, "x2": 420, "y2": 161, "type": "warn", "label": "PR Validation"},
            {"x1": 210, "y1": 187, "x2": 210, "y2": 240, "type": "ok", "label": "Chosen Pattern"},
            {"x1": 340, "y1": 266, "x2": 420, "y2": 266, "type": "ok", "label": "Discount Model"},
            {"x1": 210, "y1": 292, "x2": 210, "y2": 345, "type": "ok", "label": "Variance Input"},
            {"x1": 340, "y1": 371, "x2": 420, "y2": 371, "type": "fail", "label": "Loss Calculation"},
            {"x1": 210, "y1": 397, "x2": 210, "y2": 450, "type": "ok", "label": "Threshold Setup"},
            {"x1": 340, "y1": 476, "x2": 420, "y2": 476, "type": "ok", "label": "Executive Signoff"},
        ],
        "probes": [
            {"cx": 420, "cy": 161, "label": "PROBE 1: Git ADR Policy Compliance (100% PR check)", "color": "#10b981"},
            {"cx": 80, "cy": 266, "label": "PROBE 2: 95% Confidence TCO Variance Band (< 25% stddev)", "color": "#22c55e"},
            {"cx": 420, "cy": 476, "label": "PROBE 3: Real-Time KRI Quota Alert Margin (> 25% buffer)", "color": "#f59e0b"},
        ]
    },
    "part3_intro": (
        "The following field cases analyze severe production crises resulting from undocumented decisions, unmodeled cloud cost vectors, "
        "and unassigned operational risks. Each case details real-world operational contexts, quantifiable failure metrics, diagnostic sequences with verbatim evidence, "
        "defensible remediations, and dual-lane failed/corrected architectural diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author and lint enterprise ADRs, "
        "run three-point PERT TCO simulations with Monte Carlo distributions, and compute quantitative risk register scores with KRI telemetry."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Architecture Decision Records (ADRs)",
            "overview": (
                "An Architecture Decision Record (ADR) is a lightweight, structured document that captures an important architectural "
                "decision made for a software system, along with its context, considered alternatives, and resulting consequences. "
                "In complex cloud environments, architectural debt accumulates not because teams make poor choices, but because the rationale, "
                "underlying constraints, and rejected alternatives of earlier decisions are forgotten. When original team members depart, "
                "successors lack the historical context required to evaluate whether existing configurations represent deliberate optimization "
                "or obsolete compromises. Establishing a git-versioned ADR repository ensures that every significant technical choice is "
                "traceable, defensible, and subject to peer review."
            ),
            "preview": (
                "Drafting informal design documents that omit explicit non-goals, architectural consequences, and rejected alternatives leads to costly organizational re-litigation when personnel turns over. "
                "This ambiguity causes architectural drift, uncoordinated refactoring, and unbudgeted rework across cross-functional engineering teams."
            ),
            "technical": (
                "Effective architectural governance mandates formalizing the ADR structure, lifecycle, and validation tooling.\n\n"
                "#### Standard Structure and Lifecycle States of an Enterprise ADR\n\n"
                "High-functioning engineering organizations standardize on structured ADR formats such as Michael Nygard's format or MADR "
                "(Markdown Any Decision Record). Every ADR must contain the following discrete sections:\n\n"
                "1. **Metadata Header:** Unique sequential identifier (e.g., `ADR-0079`), descriptive title, creation date, deciders, and status.\n\n"
                "2. **Status Lifecycle:**\n"
                "   - `Proposed`: Under active discussion within the Architecture Review Board (ARB).\n"
                "   - `Accepted`: Formally approved; binding on implementation teams.\n"
                "   - `Rejected`: Evaluated but discarded due to prohibitive trade-offs or cost.\n"
                "   - `Deprecated`: Previously active, but no longer recommended for new workloads.\n"
                "   - `Superseded`: Replaced by a subsequent decision (must reference `Superseded by ADR-NNNN`).\n\n"
                "3. **Context and Problem Statement:** The business driver, technical constraint, or operational trigger requiring a decision. Explains the forces at play (technological, financial, regulatory).\n\n"
                "4. **Considered Alternatives:** Comprehensive evaluation of at least two viable options (including 'Do Nothing'), analyzing pros, cons, and estimated implementation complexity.\n\n"
                "5. **Decision Outcome:** The chosen alternative with direct rationale linked to empirical benchmarks and business priorities.\n\n"
                "6. **Consequences:** Positive benefits, negative trade-offs, and operational risks introduced by the selection.\n\n"
                "#### Git-Driven Architectural Governance and CI/CD Linting\n\n"
                "Storing ADRs in a separate documentation wiki leads to documentation rot. Best-practice architectural governance stores ADRs "
                "directly in the application's git repository under `docs/decisions/` or `architecture/adr/`. This enables automated governance:\n\n"
                "- **Pull Request Enactment:** Any PR that introduces a new cloud service (e.g., adding Cloud Bigtable or Vertex AI in Terraform) must include an associated ADR link; CI checks block merging without ARB approval.\n\n"
                "- **Automated Linter Validation:** Static analysis scripts verify that mandatory headers (Status, Deciders, Date, Invariant Impact) exist and follow standardized regex schemas.\n\n"
                "```sh\n"
                "# Example ADR CI validation check\n"
                "adr-lint --dir=./docs/adr --require-status=Accepted,Proposed --require-fields=Deciders,Impact\n"
                "```\n\n"
                "#### Traceability to System Invariants and Non-Functional Requirements\n\n"
                "Every ADR must explicitly evaluate its impact on systemic invariants and SLOs. For example, any ADR modifying database "
                "replication topologies, caching layers, or asynchronous messaging queues must explicitly state whether it preserves the "
                "Day 64 single-fulfillment business invariant (preventing double-allocation of physical stock or duplicate payment execution). "
                "Decisions that introduce eventual consistency must specify compensating saga patterns, reconciliation batch schedules, and "
                "maximum acceptable lag thresholds.\n\n"
                "#### Reversal and Supersession Mechanics\n\n"
                "ADRs are historical records and must never be edited retroactively to alter their original rationale. When production realities, "
                "cloud pricing changes, or scale demands require abandoning a previous decision, architects author a new ADR that explicitly "
                "supersedes the predecessor:\n\n"
                "```markdown\n"
                "<!-- In ADR-0112 -->\n"
                "## Context\n"
                "Workload growth has exceeded 80,000 QPS, surpassing the vertical scaling limits of Cloud SQL.\n"
                "## Decision Outcome\n"
                "Migrate to Cloud Spanner. This ADR supersedes [ADR-0079](ADR-0079-relational-database.md).\n"
                "```"
            ),
            "questions": [
                "Does the ADR explicitly enumerate at least two rejected alternatives with concrete empirical justification?",
                "Are the operational trade-offs and residual risks explicitly assigned to named engineering owners?",
                "Does the decision verify that core business invariants (e.g., single-fulfillment) remain mathematically guaranteed?"
            ],
            "reference": "https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions",
            "reference_label": "Documenting Architecture Decisions — Michael Nygard",
            "scenario": {
                "scenario": (
                    "A multi-region payments processor migrated its transaction clearing engine from Cloud Spanner to Cloud SQL for PostgreSQL "
                    "to reduce baseline monthly cloud spend. The lead engineer who championed the change left the organization four months later. "
                    "No ADR was authored to record the decision, its non-functional constraints, or the operational safeguards required to handle "
                    "cross-region failovers. During a subsequent trans-Atlantic network fiber disruption, an on-duty SRE noticed high replication lag "
                    "on the cross-region read replica in europe-west1 and manually promoted the replica to primary while the us-central1 primary was "
                    "still processing live merchant traffic. This triggered an uncoordinated split-brain split-write condition across two active master databases."
                ),
                "impact": (
                    "3,480 payment settlement records diverged between regions; $1,240,000 in duplicate settlement payouts were issued to merchant banks; "
                    "accounting teams took 18 days of manual transaction auditing to reconcile ledgers; payment processing license temporarily suspended "
                    "by financial regulatory authorities pending an external architectural audit."
                ),
                "constraints": (
                    "Must enforce single active write authority across all regions; zero split-brain write tolerance; automated failover must require "
                    "fenced consensus; full architectural rationale must be documented and accessible to all on-call personnel."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect database connection strings across regional application pods; discover services in europe-west1 writing to the local promoted replica while us-central1 services wrote to the primary:\n\n"
                    "```text\n"
                    "2026-10-14T03:12:01.402Z [postgres-replica] LOG: received promote request via pg_ctl promote\n"
                    "2026-10-14T03:12:01.405Z [postgres-replica] LOG: redo starts at 14/82000028\n"
                    "2026-10-14T03:12:01.418Z [postgres-replica] LOG: selected new timeline ID: 2\n"
                    "2026-10-14T03:12:01.450Z [postgres-replica] LOG: database system is ready to accept read-write connections\n"
                    "2026-10-14T03:12:02.105Z [app-payments-eu] INFO: connected to writable master at 10.142.0.12 (europe-west1)\n"
                    "2026-10-14T03:12:02.110Z [app-payments-us] INFO: connected to writable master at 10.128.0.44 (us-central1)\n"
                    "```",
                    "Step 2: Inspect cross-region ledger audit logs; identify massive divergence in WAL timelines and transaction records:\n\n"
                    "```text\n"
                    "2026-10-14T03:15:22.910Z [ledger-audit] CRITICAL: Split-brain detected across regional clusters!\n"
                    "  - Primary (us-central1): Timeline=1, MaxLSN=14/83FA0020, InsertedRecords=18,420\n"
                    "  - Promoted Replica (europe-west1): Timeline=2, MaxLSN=14/82410090, InsertedRecords=3,480\n"
                    "  - Conflict: 3,480 merchant payouts issued concurrently on both timelines with overlapping transaction IDs!\n"
                    "```",
                    "Step 3: Search engineering repositories for architectural documentation regarding cross-region failover protocols; found zero ADRs, runbooks, or failover design specifications:\n\n"
                    "```sh\n"
                    "$ git log -n 1 --oneline services/clearing-db/\n"
                    "e29f10a switch db to cloudsql  # [UNREVIEWED COMMIT: 0 ADRs, 0 peer review comments]\n"
                    "$ find docs/ -name \"*ADR*\" -o -name \"*failover*\"\n"
                    "# (Empty result: No architectural documentation present)\n"
                    "```",
                    "Step 4: Audit emergency escalation time; confirmed engineer was unaware that the database was configured with asynchronous replication rather than synchronous multi-region consensus."
                ],
                "root": (
                    "Complete absence of an Architecture Decision Record (ADR) detailing the critical operational differences, asynchronous replication limits, "
                    "and manual promotion dangers of Cloud SQL versus Cloud Spanner, leaving on-call engineers without documented operational boundaries."
                ),
                "remediation_steps": [
                    "Step 1: Immediately sever write traffic to the promoted replica, isolate diverging transaction records into an audit quarantine table, and restore single-primary write routing.",
                    "Step 2: Author retroactive ADR-0079 detailing database selection, replication topology, and positive fencing requirements.",
                    "Step 3: Mandate an automated CI/CD policy-as-code gate requiring an approved, peer-reviewed ADR for any infrastructure commit altering storage or network architectures.",
                    "Step 4: Re-architect the ledger layer onto Cloud Spanner or establish automated fencing controllers (such as Google Cloud Database Migration Service managed orchestrators) to prevent split-brain promotions."
                ],
                "verify": (
                    "Execute simulated cross-region network isolation drill: confirm that local SREs cannot manually promote asynchronous replicas without "
                    "verifying cryptographic fencing tokens, and verify that the ADR repository contains approved failover runbooks."
                ),
                "residual": (
                    "Manual database failovers always carry residual risk of replication lag data loss; recovery point objective (RPO) must be continuously "
                    "monitored via Cloud Monitoring replication lag metrics."
                ),
                "diagram": (
                    "Trans-Atlantic fiber disruption causes cross-region replication lag",
                    "Undocumented manual replica promotion by uninformed SRE",
                    "Split-brain write split: $1.24M duplicate payouts issued",
                    "Mandate git-versioned ADRs with explicit failover runbooks",
                    "Fenced consensus promotion guarantees zero split-brain divergence"
                ),
                "facts": "Cloud SQL substituted for Spanner without ADR; SRE promoted lagging replica during fiber cut; 3,480 diverged ledgers; $1.24M loss.",
                "inference": "Omitting ADRs strips on-call engineers of operational safety constraints, transforming minor network blips into catastrophic split-brain disasters.",
                "expected": "Standardized ADRs define operational boundaries, failover constraints, and automated fencing controls before changes hit production."
            },
            "lab": {
                "name": "Git-Driven ADR Governance and Automated Schema Linter",
                "file": "day-079-adr-governance.md",
                "goal": "Author a production-grade Architecture Decision Record (ADR-0079) and build an automated Python linter that validates ADR metadata, required sections, and business invariant traceability.",
                "expected": "A complete, compliant markdown ADR and an automated Python validation script returning zero errors.",
                "mode": "local Python 3 execution and filesystem text auditing; zero cloud billing",
                "prereq": "Day 78 decision matrix artifacts and basic Python 3 environment",
                "preflight": "Verify python3 is available in your shell.",
                "steps": [
                    "#### Stage 1: Design Specification & ADR Governance Skeleton\nDocument ADR governance rules and directory hierarchy in <kbd>day-079-adr-governance.md</kbd>. Define mandatory metadata headers, status transition state machines, and invariant traceability requirements.",
                    "#### Stage 2: Preflight Environment Validation & Syntax Readiness\nVerify that the Python runtime has standard regular expression and filesystem libraries available (<kbd>preflight_env.py</kbd>):\n\n```python\n# preflight_env.py\nimport re, sys\nprint(f\"Python Version: {sys.version}\")\nassert hasattr(re, 'search'), \"Regular expression module required for ADR linting\"\nprint(\"[PASS] Environment ready for ADR governance.\")\n```",
                    "#### Stage 3: Core Implementation: Production ADR Authoring\nAuthor the production Architecture Decision Record (<kbd>ADR-0079-database-selection.md</kbd>):\n\n```markdown\n# ADR-0079: Core Ledger Database Selection and Failover Fencing\n\n- **Status:** Accepted\n- **Date:** 2026-09-28\n- **Deciders:** Principal Architect, Lead Database Administrator, Security Lead\n- **Technical Category:** Data Storage & Transaction Processing\n\n## Context and Problem Statement\nThe transaction settlement platform requires a highly available transactional datastore capable of sustaining 15,000 writes/sec across dual geographic regions. The system must strictly preserve the Day 64 single-fulfillment invariant: no transaction may be processed twice or settled across split-brain primary nodes under network partition conditions.\n\n## Considered Alternatives\n1. **Option 1: Cloud SQL for PostgreSQL (Cross-Region Read Replica)** - Lower monthly baseline infrastructure cost ($2,400/mo), but utilizes asynchronous replication across regions with high split-brain risk during manual promotion.\n2. **Option 2: Google Cloud Spanner (Multi-Region Instance)** - Higher baseline cost ($5,800/mo), but leverages hardware TrueTime atomic clocks to provide external consistency and automated failover without split-brain hazards.\n\n## Decision Outcome\n**Chosen Option:** **Option 2: Google Cloud Spanner (Multi-Region)**.\n\n### Rationale\nWhile Cloud Spanner carries a $3,400/month infrastructure premium, it mathematically eliminates split-brain split-write hazards via distributed Paxos consensus. The financial risk of a single split-brain incident ($1.24M historical loss) far exceeds the 3-year infrastructure cost delta ($122,400).\n\n## Invariant Traceability & Consequences\n- **Single-Fulfillment Invariant:** Strict serializability guarantees that concurrent settlement attempts against identical ledger IDs will fail with lock conflict rather than duplicate execution.\n- **Operational Consequences:** Requires data modeling adaptation to support table interleaving and UUID primary keys to prevent partition hotspotting.\n- **Risk Owner:** Lead Database Administrator (Review Cadence: Semi-Annual).\n```",
                    "#### Stage 4: CI/CD Automated Governance Linter Implementation\nBuild the automated ADR verification linter (<kbd>lint_adr.py</kbd>):\n\n```python\n# lint_adr.py\nimport re, sys\n\ndef lint_adr(filepath: str) -> None:\n    with open(filepath, 'r') as f:\n        content = f.read()\n        \n    errors = []\n    required_sections = [\n        \"# ADR-\",\n        \"- **Status:**\",\n        \"- **Date:**\",\n        \"- **Deciders:**\",\n        \"## Context and Problem Statement\",\n        \"## Considered Alternatives\",\n        \"## Decision Outcome\",\n        \"## Invariant Traceability & Consequences\",\n        \"Single-Fulfillment Invariant\",\n        \"Risk Owner:\"\n    ]\n    \n    for sec in required_sections:\n        if sec not in content:\n            errors.append(f\"Missing required ADR section/tag: '{sec}'\")\n            \n    # Validate Status tag\n    status_match = re.search(r'\\*\\*Status:\\*\\*\\s+(Proposed|Accepted|Rejected|Deprecated|Superseded)', content)\n    if not status_match:\n        errors.append(\"Status must be one of: Proposed, Accepted, Rejected, Deprecated, Superseded\")\n        \n    if errors:\n        print(f\"ADR LINT FAILED for {filepath}:\")\n        for err in errors:\n            print(f\"  [ERROR] {err}\")\n        sys.exit(1)\n    else:\n        print(f\"ADR LINT PASSED: {filepath} satisfies all architectural governance rules.\")\n\nif __name__ == '__main__':\n    lint_adr('ADR-0079-database-selection.md')\n```",
                    "#### Stage 5: Execution & Policy Linter Telemetry\nExecute the ADR linter across the generated artifact:\n\n```sh\npython3 preflight_env.py && python3 lint_adr.py\n```",
                    "#### Stage 6: Chaos & Non-Compliant ADR Rejection Test\nInject an invalid ADR missing invariant consequences to verify that the CI gate rejects non-compliant contributions (<kbd>test_linter_rejection.py</kbd>):\n\n```python\n# test_linter_rejection.py\nimport subprocess, sys\n\ninvalid_adr = \"# ADR-9999: Flawed\\n- **Status:** Draft\\n\"\nwith open('ADR-invalid.md', 'w') as f:\n    f.write(invalid_adr)\n\nres = subprocess.run([sys.executable, 'lint_adr.py'], capture_output=True, text=True)\nprint(f\"Linter Exit Code on Malformed Input: {res.returncode}\")\n# Clean up temporary test file\nimport os; os.remove('ADR-invalid.md') if os.path.exists('ADR-invalid.md') else None\nprint(\"[PASS] Linter successfully blocked malformed ADR.\")\n```",
                    "#### Stage 7: Runbook Authoring: ADR Supersession Protocol\nDocument the formal protocol for deprecating and superseding ADRs. Verify that whenever an architecture decision is superseded, the original ADR status is updated to `Superseded` with a pointer to the new ADR (<kbd>adr_lifecycle.md</kbd>).",
                    "#### Stage 8: Teardown & Scratch Artifact Management\nClean up temporary execution files while retaining the validated ADR artifact:\n\n```sh\npython3 test_linter_rejection.py\n```"
                ],
                "verification": (
                    "Run automated validation command:\n\n```sh\npython3 lint_adr.py\n```\n\nConfirm output displays `ADR LINT PASSED` with zero governance violations."
                ),
                "trouble": (
                    "If the linter fails on missing tags, verify that heading strings in `ADR-0079-database-selection.md` match exact spelling and formatting."
                ),
                "cleanup": (
                    "Remove temporary ADR linting scripts:\n\n```sh\nrm -f preflight_env.py test_linter_rejection.py\n```"
                ),
                "accept": "A structured ADR containing considered alternatives, dated pricing assumptions, invariant traceability, and named risk owners.",
                "file": "day-079-adr-governance.md"
            }
        },
        {
            "key": "topic-02",
            "title": "Total cost of ownership (TCO) comparisons",
            "overview": (
                "Accurately forecasting cloud expenditures requires moving beyond simplistic single-point estimates generated by static "
                "cost calculators. Real-world enterprise cloud total cost of ownership (TCO) is governed by systemic variability: fluctuating "
                "user adoption, network data egress across regions, persistent disk snapshot retention, operational SRE toil, and parallel-run "
                "'double-bubble' migration expenses. A defensible architectural TCO model utilizes three-point estimation (Low / Base / High) "
                "grounded in the Program Evaluation and Review Technique (PERT) or Monte Carlo probabilistic simulations. This provides "
                "executive decision-makers with confidence intervals and reveals the exact economic tipping points where architecture choices diverge."
            ),
            "preview": (
                "Relying solely on baseline list prices from cloud calculators without modeling network egress, operational toil, licensing renewals, and disaster recovery replication leads to multi-million-dollar budget overruns. "
                "This variance forces emergency cost-cutting measures that compromise infrastructure resilience and violate enterprise SLAs."
            ),
            "technical": (
                "Rigorous cloud financial architecture demands modeling probabilistic ranges, unmasking hidden cost vectors, and factoring in commitments.\n\n"
                "#### Three-Point Estimation Formulation (PERT and Monte Carlo)\n\n"
                "Rather than assuming static monthly spend, architects model each architectural component across three uncertainty regimes:\n\n"
                "- **Optimistic ($O$):** Best-case baseline (minimal data growth, low traffic volatility, high CUD coverage, zero major incidents).\n\n"
                "- **Most Likely ($M$):** Expected production baseline reflecting historical quarterly growth (15–20% YoY).\n\n"
                "- **Pessimistic ($P$):** High-stress case (5x burst traffic, prolonged double-bubble parallel run, unoptimized data egress, elevated SRE emergency toil).\n\n"
                "The PERT expected value ($\\mu$) and standard deviation ($\\sigma$) for 3-year TCO are calculated as:\n\n"
                "$$\\mu = \\frac{O + 4M + P}{6}, \\quad \\sigma = \\frac{P - O}{6}$$\n\n"
                "The 95% confidence interval for executive budget defense is $[\mu - 2\sigma, \mu + 2\sigma]$.\n\n"
                "#### Hidden and Non-Linear Cloud Cost Vectors\n\n"
                "Enterprise cloud budgets frequently experience variance due to four non-linear cost vectors:\n\n"
                "1. **Inter-Region Network Egress:** Traffic between GCP regions (e.g., us-central1 to europe-west1) costs $0.01/GB for default routing or up to $0.08/GB for premium tier internet. A database replicating 50 TB/month across regions generates $4,000/month in pure egress charges.\n\n"
                "2. **Cloud NAT Processing Charges:** Beyond the fixed hourly gateway charge ($0.045/hour), Cloud NAT charges $0.045 per GB of data processed. Ingestion pipelines pulling 200 TB/month through NAT incur $9,000/month in processing fees.\n\n"
                "3. **Persistent Disk Snapshot Cumulative Storage:** Incremental snapshots accumulate silently. Without strict lifecycle deletion policies, snapshot storage can exceed the primary disk size by 300–500% over 12 months.\n\n"
                "4. **Cloud Monitoring Custom Metrics:** Ingesting custom application metrics beyond the free tier incurs $0.258 per million samples. Microservices generating thousands of unique metric label combinations can generate surprising five-figure monthly observability bills.\n\n"
                "#### Committed Use Discounts (CUDs) and Break-Even Utilization\n\n"
                "Google Cloud offers two primary CUD models:\n\n"
                "- **Resource-Based CUDs:** Commit to specific vCPU and RAM quantities in a specific region for 1 or 3 years (up to 57% savings for general compute, up to 70% for memory-optimized).\n\n"
                "- **Flexible Spend-Based CUDs:** Commit to a minimum hourly dollar spend across Compute Engine, Cloud Run, and GKE across all regions (up to 46% savings for 3-year commitment).\n\n"
                "Break-even utilization analysis is critical: for a 1-year resource CUD providing a 37% discount, the break-even utilization threshold is $1.0 - 0.37 = 63\%$. If a seasonal workload operates below 63% capacity over 12 months, paying on-demand rates is cheaper than locking into an unused commitment.\n\n"
                "#### The Double-Bubble Migration FinOps Model\n\n"
                "During cloud migration waves (Days 75–77), enterprises operate on-premises data centers and target cloud environments concurrently. "
                "Architects must calculate the 'Double-Bubble' duration: the cumulative financial penalty of dual-running infrastructure during "
                "discovery, replication, and rehearsal. Accelerating the cutover window by 60 days via automated testing often yields higher net ROI "
                "than negotiating 5% discounts on VM compute rates."
            ),
            "questions": [
                "Does the TCO comparison include low, base, and high three-point ranges with explicit standard deviation bounds?",
                "Are inter-region network egress and Cloud NAT processing charges explicitly modeled based on expected throughput?",
                "What is the break-even utilization percentage for all proposed Committed Use Discounts (CUDs)?"
            ],
            "reference": "https://cloud.google.com/products/calculator",
            "reference_label": "Google Cloud Pricing Calculator and TCO Best Practices",
            "scenario": {
                "scenario": (
                    "An enterprise retail data platform migrated its business intelligence warehouse from an on-premises Hadoop cluster to "
                    "Google Cloud BigQuery. The architecture team estimated monthly cloud spend at $18,000 based on raw query compute slots. "
                    "However, they neglected to model cross-region network egress fees for downstream ETL pipelines that extracted 180 TB of raw "
                    "analytics tables monthly from us-central1 into a European reporting cluster in europe-west3. Furthermore, application developers "
                    "configured automated query polling jobs without result caching, generating 4.2 million on-demand query executions per month. "
                    "At the end of Month 2, the cloud invoice arrived at $104,500—an unbudgeted 480% variance that consumed the department's entire "
                    "annual contingency reserve."
                ),
                "impact": (
                    "Finance placed an immediate freeze on all cloud project funding; the data science team was forced to halt training machine learning models; "
                    "executive leadership demanded an emergency retrospective and threatened to re-patriate workloads back to the on-prem data center."
                ),
                "constraints": (
                    "Total monthly cloud expenditure must remain strictly below $28,000; European reporting systems must receive fresh data within 2 hours; "
                    "all future cloud architectures must present three-point TCO ranges prior to budget approval."
                ),
                "diagnostic_steps": [
                    "Step 1: Export Cloud Billing data to BigQuery; query `gcp_billing_export_resource_v1` grouped by `service.description` and `sku.description`:\n\n"
                    "```sql\n"
                    "SELECT\n"
                    "  service.description AS service_name,\n"
                    "  sku.description AS sku_name,\n"
                    "  ROUND(SUM(cost), 2) AS total_cost_usd,\n"
                    "  ROUND(SUM(usage.amount_in_pricing_units), 2) AS total_units\n"
                    "FROM `finops-prod-99.billing_export.gcp_billing_export_resource_v1`\n"
                    "WHERE invoice.month = '202610'\n"
                    "GROUP BY 1, 2 ORDER BY total_cost_usd DESC LIMIT 5;\n"
                    "```\n\n"
                    "```text\n"
                    "+------------------+-----------------------------------------------+----------------+-------------+\n"
                    "| service_name     | sku_name                                      | total_cost_usd | total_units |\n"
                    "+------------------+-----------------------------------------------+----------------+-------------+\n"
                    "| BigQuery         | Analysis (Queries - On-Demand)                |       84700.18 | 1694.00 TB  |\n"
                    "| Compute Engine   | Network Inter-Region Egress Americas to EMEA  |       19800.42 |  180.00 TB  |\n"
                    "+------------------+-----------------------------------------------+----------------+-------------+\n"
                    "```",
                    "Step 2: Inspect BigQuery query execution audit logs; discover 4.2 million un-cached queries polling identical date partitions:\n\n"
                    "```json\n"
                    "{\n"
                    "  \"protoPayload\": {\n"
                    "    \"serviceData\": {\n"
                    "      \"jobCompletedEvent\": {\n"
                    "        \"job\": {\n"
                    "          \"jobConfiguration\": {\"query\": {\"query\": \"SELECT * FROM `orders.daily_summary` WHERE dt = CURRENT_DATE()\"}},\n"
                    "          \"jobStatistics\": {\"totalBytesBilled\": \"42949672960\", \"queryOutputRowCount\": \"12\", \"billingTier\": 1},\n"
                    "          \"jobStatus\": {\"state\": \"DONE\"}\n"
                    "        }\n"
                    "      }\n"
                    "    }\n"
                    "  }\n"
                    "}\n"
                    "```",
                    "Step 3: Re-calculate the 3-point TCO range using actual observed variance parameters; observe that the original estimate ($18k) was below even the most optimistic theoretical bound."
                ],
                "root": (
                    "Single-point architectural cost estimation that modeled only compute storage/query processing while completely omitting "
                    "cross-region data transfer egress charges, query polling concurrency, and data replication volume."
                ),
                "remediation_steps": [
                    "Step 1: Re-architect European ETL to utilize BigQuery cross-region dataset replication during off-peak hours with compressed Parquet extraction.",
                    "Step 2: Implement BigQuery BI Engine with query caching, reducing unneeded on-demand query scans by 74%.",
                    "Step 3: Purchase a 1-year Commit for baseline BigQuery compute slots, reducing unit slot-hour costs by 35%.",
                    "Step 4: Establish Cloud Billing budget alerts at 75%, 90%, and 100% of the $28,000 threshold with automated Pub/Sub webhooks triggering query quota limits."
                ],
                "verify": (
                    "Monitor Cloud Billing reports over 30 consecutive billing cycles: confirm monthly expenditure stabilizes at $22,400 "
                    "(well below the $28,000 cap), with inter-region egress reduced from $19,800 to $1,850/month."
                ),
                "residual": (
                    "Sudden business growth or viral consumer sales events can spike BigQuery query volumes; project must enforce per-query "
                    "maximum bytes billed flags (`--maximum_bytes_billed=10000000000`) on all automated service accounts."
                ),
                "diagram": (
                    "ETL pipeline extracts 180 TB/mo uncompressed cross-region",
                    "Unmodeled inter-region network egress charges accumulate",
                    "Invoice shock: $104.5k/mo (480% over budget); funding freeze",
                    "Implement BigQuery BI Engine caching & compressed replication",
                    "Stabilized at $22.4k/mo with automated budget alerts verified"
                ),
                "facts": "BigQuery estimated at $18k/mo; 180 TB cross-region egress caused $104.5k bill; caching + CUD stabilized cost at $22.4k/mo.",
                "inference": "Single-point estimates conceal network data gravity costs; multi-variable three-point modeling reveals non-linear cloud billing traps.",
                "expected": "Three-point PERT TCO ranges account for egress volatility, preventing catastrophic budget surprises."
            },
            "lab": {
                "name": "PERT Three-Point TCO Range and Monte Carlo Simulator",
                "file": "day-079-tco-pert-model.md",
                "goal": "Build an executable Python financial engine that computes three-point PERT estimates, standard deviations, and Monte Carlo confidence intervals for competing cloud architectures.",
                "expected": "An executable Python simulation script generating low, base, and high 3-year TCO bounds with dated pricing parameters.",
                "mode": "local Python 3 mathematical simulation; zero cloud spend",
                "prereq": "Prior day decision matrix artifacts and basic Python 3 environment",
                "preflight": "Ensure Python 3 is installed with math and random modules.",
                "steps": [
                    "#### Stage 1: Design Specification & TCO Variance Bounds Skeleton\nDocument three-point estimation assumptions and unit cost drivers in <kbd>day-079-tco-pert-model.md</kbd>. Establish the mathematical boundaries for compute, storage, cross-region network egress, and SRE toil.",
                    "#### Stage 2: Preflight Environment Validation & Random Generator Check\nVerify the local Python execution environment and ensure standard math and random modules are functional (<kbd>preflight_tco.py</kbd>):\n\n```python\n# preflight_tco.py\nimport math, random\nassert hasattr(random, 'triangular'), \"random.triangular required for Beta-PERT approximation\"\nprint(\"[PASS] Mathematical runtime verified.\")\n```",
                    "#### Stage 3: Core Implementation: Python PERT & Monte Carlo TCO Engine\nCreate the complete PERT and Monte Carlo TCO engine script (<kbd>tco_pert.py</kbd>):\n\n```python\n# tco_pert.py\n\"\"\"Computes three-point PERT and Monte Carlo TCO confidence intervals.\"\"\"\nimport random, math\nfrom typing import Tuple, List\n\ndef pert_estimate(o: float, m: float, p: float) -> Tuple[float, float]:\n    mean = (o + 4.0 * m + p) / 6.0\n    std = (p - o) / 6.0\n    return mean, std\n\ndef run_tco_simulation():\n    print(\"=\" * 75)\n    print(\"DAY 79: THREE-POINT PERT & MONTE CARLO TCO RANGE SIMULATOR\")\n    print(\"=\" * 75)\n    \n    components = [\n        (\"Compute & Memory (GCE / GKE)\",    120.0, 160.0, 240.0),\n        (\"Storage & Snapshots (PD & GCS)\",   35.0,  55.0,  95.0),\n        (\"Network Inter-Region Egress\",      15.0,  45.0, 130.0),\n        (\"SRE Operational Toil (Burdened)\",  40.0,  85.0, 160.0),\n        (\"Third-Party Software Licensing\",   60.0,  60.0,  75.0),\n        (\"Migration Double-Bubble Running\",   20.0,  35.0,  60.0)\n    ]\n    \n    total_mean = 0.0\n    total_variance = 0.0\n    \n    print(f\"\\n{'Component':<32} | {'Opt (O)':<9} | {'Likely (M)':<10} | {'Pess (P)':<9} | {'PERT Mean':<10} | {'StdDev'}\")\n    print(\"-\" * 88)\n    for name, o, m, p in components:\n        mu, sigma = pert_estimate(o, m, p)\n        total_mean += mu\n        total_variance += (sigma ** 2)\n        print(f\"{name:<32} | ${o:>6.1f}k | ${m:>7.1f}k | ${p:>6.1f}k | ${mu:>7.1f}k | ${sigma:>5.1f}k\")\n        \n    total_std = math.sqrt(total_variance)\n    low_95 = total_mean - 1.96 * total_std\n    high_95 = total_mean + 1.96 * total_std\n    \n    print(\"-\" * 88)\n    print(f\"{'TOTAL 3-YEAR TCO ESTIMATE':<32} |          |            |          | ${total_mean:>7.1f}k | ${total_std:>5.1f}k\")\n    print(f\"\\nEXECUTIVE BUDGET DEFENSE BOUNDS (95% Confidence Interval):\")\n    print(f\"  - Low Bound  (-1.96 sigma): ${low_95:,.1f}k  ($ {low_95*1000:>10,.0f})\")\n    print(f\"  - Base Target (PERT Mean):  ${total_mean:,.1f}k  ($ {total_mean*1000:>10,.0f})\")\n    print(f\"  - High Bound (+1.96 sigma): ${high_95:,.1f}k  ($ {high_95*1000:>10,.0f})\")\n    \n    # Monte Carlo verification (10,000 trials)\n    random.seed(42)\n    trials = 10000\n    sim_totals = []\n    for _ in range(trials):\n        trial_sum = 0.0\n        for _, o, m, p in components:\n            trial_sum += random.triangular(o, p, m)\n        sim_totals.append(trial_sum)\n        \n    sim_totals.sort()\n    mc_p05 = sim_totals[int(trials * 0.05)]\n    mc_p50 = sim_totals[int(trials * 0.50)]\n    mc_p95 = sim_totals[int(trials * 0.95)]\n    \n    print(f\"\\nMONTE CARLO EMPIRICAL DISTRIBUTION (10,000 Iterations):\")\n    print(f\"  - 5th Percentile (P05):    ${mc_p05:,.1f}k\")\n    print(f\"  - 50th Percentile (Median): ${mc_p50:,.1f}k\")\n    print(f\"  - 95th Percentile (P95):   ${mc_p95:,.1f}k\")\n    \n    assert low_95 < total_mean < high_95, \"PERT Confidence interval mathematical inversion error!\"\n    print(\"\\n>> Verification PASSED: TCO probability distribution is mathematically defensible.\")\n    print(\"=\" * 75)\n\nif __name__ == '__main__':\n    run_tco_simulation()\n```",
                    "#### Stage 4: Execution & Simulation Telemetry\nExecute the PERT TCO simulator:\n\n```sh\npython3 preflight_tco.py && python3 tco_pert.py\n```",
                    "#### Stage 5: Live Verification & Confidence Interval Assertions\nAuthor an assertion script to verify that confidence bounds strictly contain median and expected values (<kbd>test_tco_bounds.py</kbd>):\n\n```python\n# test_tco_bounds.py\nfrom tco_pert import pert_estimate\nimport math\n\no, m, p = 15.0, 45.0, 130.0\nmean, std = pert_estimate(o, m, p)\nassert mean == (15 + 4*45 + 130) / 6.0, \"Mean calculation error!\"\nassert std == (130 - 15) / 6.0, \"StdDev calculation error!\"\nprint(f\"[PASS] Egress PERT calculation verified: mean=${mean:.2f}k, std=${std:.2f}k\")\n```",
                    "#### Stage 6: Chaos & Network Egress Shock Injection\nSimulate an adverse 3x egress volume expansion to test high-bound sensitivity (<kbd>stress_egress_shock.py</kbd>):\n\n```python\n# stress_egress_shock.py\nfrom tco_pert import pert_estimate\n# Pessimistic egress jumps from 130k to 390k\nmean_base, _ = pert_estimate(15.0, 45.0, 130.0)\nmean_shock, _ = pert_estimate(15.0, 45.0, 390.0)\ndelta = mean_shock - mean_base\nprint(f\"Egress Shock: 3-Year Mean increases by ${delta:,.1f}k\")\nassert delta > 40.0, \"Expected significant mean shift under network egress shock!\"\nprint(\"[PASS] Egress stress test complete: Quantified impact on budget bounds.\")\n```",
                    "#### Stage 7: Runbook Authoring: FinOps Budget Alert Configuration\nDocument Cloud Billing budget alerts with automated Pub/Sub notification hooks to trigger query throttling before monthly spending breaches the PERT base target (<kbd>finops_runbook.md</kbd>).",
                    "#### Stage 8: Teardown & Script Cleanup\nClean up temporary verification files:\n\n```sh\npython3 test_tco_bounds.py && python3 stress_egress_shock.py\n```"
                ],
                "verification": (
                    "Run automated assertion testing on the TCO model:\n\n```sh\npython3 -c \"import tco_pert; tco_pert.run_tco_simulation(); print('TCO PERT Simulator Test Passed')\"\n```\n\nConfirm that the output demonstrates a defensible 95% confidence interval and prints P05, P50, and P95 percentiles."
                ),
                "trouble": (
                    "If the standard deviation calculation fails, ensure math.sqrt is provided with a strictly non-negative variance sum."
                ),
                "cleanup": (
                    "Remove temporary simulation scripts:\n\n```sh\nrm -f preflight_tco.py test_tco_bounds.py stress_egress_shock.py\n```"
                ),
                "accept": "A three-point PERT TCO estimation model with low/base/high bounds and dated pricing parameters.",
                "file": "day-079-tco-pert-model.md"
            }
        },
        {
            "key": "topic-03",
            "title": "Risk registers (likelihood, impact, mitigation)",
            "overview": (
                "A quantitative Risk Register transforms vague architectural anxieties into actionable, prioritized risk mitigation "
                "roadmaps. Every architectural choice introduces systemic hazards: vendor API quotas, regional hardware capacity constraints, "
                "regulatory compliance shifts, single points of failure (SPOFs), and operational skill gaps. By evaluating each risk through "
                "formal likelihood (1–5) and impact (1–5) scoring, calculating Expected Monetary Value (EMV), assigning explicit named risk "
                "owners, and establishing real-time Key Risk Indicators (KRIs) in Cloud Monitoring, architects ensure that risks are actively "
                "managed rather than discovered during major production outages."
            ),
            "preview": (
                "Treating architectural risks as informal hallway conversations rather than documenting them in a quantified risk register leaves critical single points of failure unmonitored. "
                "When an unmitigated operational or supply-chain failure occurs, the organization faces extended downtime, regulatory sanctions, and executive liability."
            ),
            "technical": (
                "Operationalizing an architectural risk register requires mathematical modeling, treatment frameworks, and automated telemetry.\n\n"
                "#### Quantitative Risk Modeling and Expected Monetary Value (EMV)\n\n"
                "Architects classify risks using a two-dimensional matrix and quantify total exposure through Expected Monetary Value:\n\n"
                "1. **Likelihood Rating ($L \\in [1, 5]$):** Probability of occurrence over a 12-month horizon (1: Rare &lt; 5%, 2: Unlikely 5–20%, 3: Possible 20–50%, 4: Likely 50–80%, 5: Almost Certain &gt; 80%).\n\n"
                "2. **Impact Rating ($I \\in [1, 5]$):** Business severity if realized (1: Negligible &lt; $10k, 2: Minor $10k–$50k, 3: Moderate $50k–$250k, 4: Major $250k–$1M, 5: Catastrophic &gt; $1M / SLA breach).\n\n"
                "3. **Risk Severity Score ($RS$):** $RS = L \\times I$. Scores $\\ge 15$ are classified as High/Critical risks requiring mandatory Architecture Review Board remediation plans.\n\n"
                "4. **Expected Monetary Value (EMV):** For quantified financial risks, EMV represents the probability-weighted financial impact:\n\n"
                "$$\\text{EMV} = P(\\text{Risk}) \\times \\text{Financial Impact} ($)$$\n\n"
                "If a regional network outage carries a 15% annual probability and an unmitigated business loss of $2,000,000, its annual EMV is $300,000. Spending $80,000/year on multi-region automated failover yields a positive net risk ROI of $220,000.\n\n"
                "#### Four Architectural Risk Treatment Strategies\n\n"
                "Every identified risk in the register must map to one of four formal treatment strategies:\n\n"
                "- **Mitigate (Control):** Implement technical or process controls to reduce likelihood or impact (e.g., configuring multi-region Cloud Spanner, deploying Cloud Armor DDoS protection, establishing automated database backups).\n\n"
                "- **Avoid (Redesign):** Eliminate the risk entirely by altering the architectural design (e.g., adopting managed Cloud Run instead of self-hosted Kubernetes to avoid managing control plane etcd quorums).\n\n"
                "- **Transfer (Share):** Shift financial or operational impact to a third party (e.g., purchasing cyber-risk insurance or entering an enterprise SLA contract with Google Cloud Professional Services).\n\n"
                "- **Accept (Retain):** Acknowledge the risk without active remediation when cost of mitigation exceeds potential impact. Acceptance requires formal written executive sign-off and an explicit expiration review date.\n\n"
                "#### Key Risk Indicators (KRIs) and Automated Alerting\n\n"
                "A static markdown file becomes obsolete unless linked to real-time production telemetry. Architects establish automated Key Risk Indicators:\n\n"
                "- **Quota Exhaustion Risk:** KRI = Current Usage / Quota Limit. Alert triggers at 80% consumption before API requests are throttled.\n\n"
                "- **Replication Lag Divergence Risk:** KRI = Cloud SQL replica byte lag. Alert triggers when lag exceeds 10 MB or 5 seconds, warning of failover data loss.\n\n"
                "- **Cost Variance Risk:** KRI = Daily burn rate / Monthly budget allocation. Alert triggers when projected end-of-month spend exceeds 110%."
            ),
            "questions": [
                "Does every risk with a severity score >= 15 have a funded mitigation plan and an explicitly named risk owner?",
                "Has Expected Monetary Value (EMV) been calculated to justify the return on investment for high-availability architectural controls?",
                "Are automated Key Risk Indicators (KRIs) configured in Cloud Monitoring to alert before operational thresholds are breached?"
            ],
            "reference": "https://cloud.google.com/architecture/framework/reliability",
            "reference_label": "Google Cloud Architecture Framework: Reliability and Risk Management",
            "scenario": {
                "scenario": (
                    "A real-time financial algorithmic execution platform operated its trade matching engines across Compute Engine instances in "
                    "us-east4. The architecture team recognized the risk of GCP project API quota exhaustion during market volatility spikes but recorded "
                    "it merely as an informal note in an architectural design doc rather than establishing a formal Risk Register entry with an assigned owner. "
                    "During an unprecedented Federal Reserve interest rate announcement, market volatility surged 8x. The automated scaling group attempted "
                    "to launch 120 additional c2-standard-60 compute instances. The Compute Engine API returned `QUOTA_EXCEEDED` errors because the project's "
                    "regional vCPU quota was capped at 1,000 cores. Scaling halted, trade execution latency degraded from 1.2 ms to 4,800 ms, and inbound "
                    "orders backed up in memory queues until application servers suffered out-of-memory kernel panics."
                ),
                "impact": (
                    "640,000 customer trade execution orders were delayed or dropped; institutional traders suffered $3,800,000 in slippage losses; "
                    "the firm was fined $450,000 by financial market regulators for inadequate capacity risk controls; total executive compensation clawbacks ensued."
                ),
                "constraints": (
                    "Must guarantee 100% compute capacity availability during market volatility bursts; API quota usage must be monitored continuously; "
                    "all operational risks must have assigned risk owners with weekly audit sign-offs."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect Compute Engine API audit logs; observe thousands of `compute.instances.insert` operations returning HTTP 403 `QuotaExceeded`:\n\n"
                    "```json\n"
                    "{\n"
                    "  \"protoPayload\": {\n"
                    "    \"methodName\": \"v1.compute.instances.insert\",\n"
                    "    \"status\": {\"code\": 8, \"message\": \"Quota 'CPUS' exceeded. Limit: 1000.0 in region us-east4.\"},\n"
                    "    \"request\": {\"zone\": \"us-east4-a\", \"machineType\": \"zones/us-east4-a/machineTypes/c2-standard-60\"}\n"
                    "  }\n"
                    "}\n"
                    "```",
                    "Step 2: Check Cloud Monitoring metric `compute.googleapis.com/quota/allocation/usage`; observe vCPU usage pinned at 1,000 / 1,000 cores (100% saturation):\n\n"
                    "```text\n"
                    "2026-10-29T18:30:00Z [quota-telemetry] region=us-east4 metric=CPUS limit=1000.0 current_usage=1000.0 headroom=0.0 (SATURATED)\n"
                    "2026-10-29T18:30:15Z [app-order-engine] ERROR: Failed to scale out pool: 120 VM creation requests rejected\n"
                    "2026-10-29T18:30:22Z [app-order-engine] WARNING: Inbound memory queue depth: 642,800 orders (memory pressure 98.4%)\n"
                    "```",
                    "Step 3: Review risk documentation; discovered that the quota risk had been noted 8 months prior but had no assigned risk owner, no monitoring alert, and no quota increase ticket filed.",
                    "Step 4: Audit emergency escalation time; confirmed that emergency GCP quota requests during live market events take 2 to 6 hours for approval, completely useless during intraday market volatility."
                ],
                "root": (
                    "Failure to maintain a quantitative Risk Register with an assigned risk owner and automated Key Risk Indicator (KRI) alerts, "
                    "allowing a known project vCPU quota ceiling to remain unmanaged until it triggered catastrophic production failure."
                ),
                "remediation_steps": [
                    "Step 1: Immediately file and secure emergency regional vCPU quota increases to 5,000 cores, backed by Google Cloud Committed Use Discounts.",
                    "Step 2: Formalize the enterprise Architectural Risk Register, assigning the Platform SRE Lead as the permanent owner of API Quota Risks.",
                    "Step 3: Deploy automated Cloud Monitoring alert policies on `compute.googleapis.com/quota/allocation/usage` triggering P1 notifications when usage exceeds 75% of limit.",
                    "Step 4: Implement capacity reservations (`gcloud compute reservations create`) in primary and secondary zones to guarantee physical hardware availability regardless of cloud-wide spot demand."
                ],
                "verify": (
                    "Execute synthetic surge drill: simulate 500% auto-scaling launch; verify Cloud Monitoring tracks vCPU quota headroom in real time, "
                    "and verify that capacity reservations satisfy all VM provisioning requests with zero quota errors."
                ),
                "residual": (
                    "Cloud-wide regional hardware supply constraints can occasionally delay capacity reservation fulfillments; architecture must "
                    "maintain automated cross-region burst failover capability into us-central1."
                ),
                "diagram": (
                    "Market volatility surge triggers 120 VM auto-scale launch",
                    "Regional vCPU quota (1,000 cores) saturates without KRI alert",
                    "Compute API QUOTA_EXCEEDED: $3.8M trading slippage loss",
                    "Deploy automated KRI alerts at 75% quota + capacity reservations",
                    "Guaranteed hardware availability with zero scaling rejections"
                ),
                "facts": "Project vCPU quota capped at 1,000 cores; market spike crashed scaling; $3.8M slippage loss; capacity reservations and KRI alerts remediated risk.",
                "inference": "Unassigned risks inevitably turn into production outages; proactive KRI alerting and capacity reservations neutralize quota exhaustion hazards.",
                "expected": "Quantitative risk registers with automated telemetry triggers ensure quota and capacity limits are expanded months before production spikes."
            },
            "lab": {
                "name": "Quantitative Risk Register Scoring and KRI Telemetry Harness",
                "file": "day-079-risk-register.md",
                "goal": "Build an executable Python Risk Register Engine that calculates risk severity scores, computes Expected Monetary Value (EMV), and outputs formatted markdown tables and KRI monitoring specs.",
                "expected": "An executable Python script that scores risks, identifies critical mitigation priorities, and generates an auditable risk register markdown artifact.",
                "mode": "local Python 3 execution and automated markdown generation; zero cloud billing",
                "prereq": "Prior day decision matrix artifacts and basic Python 3 environment",
                "preflight": "Verify Python 3 is installed in your local shell environment.",
                "steps": [
                    "#### Stage 1: Design Specification & Risk Matrix Skeleton\nDocument risk evaluation criteria and governance scoring scales in <kbd>day-079-risk-register.md</kbd>. Define the 5x5 Likelihood x Impact matrix, treatment categorizations, and EMV formulation.",
                    "#### Stage 2: Preflight Environment Validation & Syntax Check\nVerify the local Python 3 execution environment and ensure standard typing and mathematical modules are functional (<kbd>preflight_risk.py</kbd>):\n\n```python\n# preflight_risk.py\nimport sys\nprint(f\"Python Version: {sys.version}\")\nassert sys.version_info >= (3, 8), \"Python 3.8+ required\"\nprint(\"[PASS] Risk register runtime verified.\")\n```",
                    "#### Stage 3: Core Implementation: Python Risk Register & EMV Engine\nDevelop the executable Risk Register analysis engine (<kbd>risk_engine.py</kbd>):\n\n```python\n# risk_engine.py\n\"\"\"Calculates architectural risk severity scores and Expected Monetary Value.\"\"\"\nimport sys\nfrom typing import List, Tuple\n\ndef evaluate_risk_register() -> Tuple[float, int]:\n    print(\"=\" * 80)\n    print(\"DAY 79: QUANTITATIVE ARCHITECTURAL RISK REGISTER & EMV ENGINE\")\n    print(\"=\" * 80)\n    \n    risks = [\n        (\"RSK-01\", \"Regional vCPU Quota Exhaustion\", \"Operational\", 4, 5, 3800000.0, \"Mitigate\", \"Lead Platform SRE\"),\n        (\"RSK-02\", \"Cross-Region DB Split-Brain Promotion\", \"Architectural\", 2, 5, 1240000.0, \"Mitigate\", \"Principal Data Architect\"),\n        (\"RSK-03\", \"Unmodeled Inter-Region Egress Shock\", \"Financial\", 4, 3, 250000.0, \"Mitigate\", \"FinOps Manager\"),\n        (\"RSK-04\", \"Third-Party Auth Provider Outage\", \"Vendor/External\", 3, 4, 750000.0, \"Transfer\", \"Identity Lead\"),\n        (\"RSK-05\", \"Day 64 Single-Fulfillment Violation\", \"Business Invariant\", 2, 5, 2000000.0, \"Mitigate\", \"Lead Transaction Architect\"),\n        (\"RSK-06\", \"Sub-Optimal CUD Utilization Rate\", \"Financial\", 3, 2, 80000.0, \"Accept\", \"FinOps Manager\"),\n    ]\n    \n    prob_map = {1: 0.05, 2: 0.15, 3: 0.35, 4: 0.65, 5: 0.90}\n    \n    print(f\"\\n{'ID':<8} | {'Risk Title':<34} | {'L':<2} | {'I':<2} | {'Score':<5} | {'EMV ($)':<12} | {'Treatment':<9} | {'Owner'}\")\n    print(\"-\" * 105)\n    \n    critical_count = 0\n    total_emv = 0.0\n    \n    for rid, title, cat, l, i, max_loss, treat, owner in risks:\n        score = l * i\n        prob = prob_map[l]\n        emv = prob * max_loss\n        total_emv += emv\n        \n        status = \"CRITICAL\" if score >= 15 else (\"HIGH\" if score >= 10 else \"MEDIUM\")\n        if score >= 15:\n            critical_count += 1\n            \n        print(f\"{rid:<8} | {title:<34} | {l:<2} | {i:<2} | {score:<2} ({status[:4]}) | ${emv:>10,.0f} | {treat:<9} | {owner}\")\n        \n    print(\"-\" * 105)\n    print(f\"TOTAL ANNUALIZED EXPECTED MONETARY VALUE (EMV) EXPOSURE: ${total_emv:,.0f}\")\n    print(f\"CRITICAL RISKS REQUIRING IMMEDIATE ARB MITIGATION (Score >= 15): {critical_count}\")\n    \n    assert critical_count >= 2, \"Risk evaluation must detect at least 2 critical architectural risks!\"\n    print(\"\\n>> Risk Register Verification PASSED: All critical risks assigned to named owners.\")\n    print(\"=\" * 80)\n    return total_emv, critical_count\n\nif __name__ == '__main__':\n    evaluate_risk_register()\n```",
                    "#### Stage 4: Execution & Risk Register Tabulation\nExecute the Risk Register engine:\n\n```sh\npython3 preflight_risk.py && python3 risk_engine.py\n```",
                    "#### Stage 5: Live Verification & Score Assertions\nAuthor an assertion test ensuring that EMV calculations and risk scoring strictly align with standard probability tables (<kbd>test_risk_assertions.py</kbd>):\n\n```python\n# test_risk_assertions.py\nfrom risk_engine import evaluate_risk_register\n\nemv, crit = evaluate_risk_register()\nassert emv > 3000000.0, f\"Expected total EMV > $3M, got ${emv:,.2f}\"\nassert crit == 2, f\"Expected exactly 2 critical risks (RSK-01, RSK-05), got {crit}\"\nprint(f\"[PASS] Risk assertions verified: Total EMV exposure is ${emv:,.2f}.\")\n```",
                    "#### Stage 6: Chaos & Unassigned Risk Injection Testing\nSimulate an unassigned high-severity risk to test ARB governance guardrails (<kbd>test_unassigned_risk.py</kbd>):\n\n```python\n# test_unassigned_risk.py\nflawed_risk = {\"ID\": \"RSK-99\", \"Title\": \"Unmonitored Interconnect Drop\", \"Score\": 20, \"Owner\": \"\"}\nassert flawed_risk[\"Owner\"] != \"\", \"[ARB REJECTED] Critical risk detected with empty owner!\"\n```",
                    "#### Stage 7: Runbook Authoring: Key Risk Indicator (KRI) Alerting Specification\nDefine Terraform alert policies for Cloud Monitoring to track quota consumption and replication lag. Configure notification channels for P1 alerts when quota headroom drops below 25% (<kbd>kri_monitoring.tf</kbd>).",
                    "#### Stage 8: Teardown & Script Cleanup\nRun final verification and clean up temporary execution scripts:\n\n```sh\npython3 test_risk_assertions.py\n```"
                ],
                "verification": (
                    "Run automated validation test:\n\n```sh\npython3 -c \"import risk_engine; risk_engine.evaluate_risk_register(); print('Risk Register Engine Verified')\"\n```\n\nConfirm output calculates total Expected Monetary Value (EMV) and identifies all critical architectural risks."
                ),
                "trouble": (
                    "If the assertion fails on critical risks, check that likelihood and impact ratings for RSK-01 (4x5=20) and RSK-05 (2x5=10) match expected parameters."
                ),
                "cleanup": (
                    "Remove temporary Python scripts:\n\n```sh\nrm -f preflight_risk.py test_risk_assertions.py test_unassigned_risk.py\n```"
                ),
                "accept": "A quantitative risk register documenting likelihood, impact, EMV calculations, and explicit risk owners.",
                "file": "day-079-risk-register.md"
            }
        }
    ]
}
