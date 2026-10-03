# Graph Report - gcp-180day-architect-site  (2026-10-03)

## Corpus Check
- 217 files · ~4,284,769 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: .csv 2, (none) 1, .css 1)

## Summary
- 765 nodes · 842 edges · 175 communities (39 shown, 136 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2228fb35`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- inspect-adc-and-tokens.py
- build.py
- author_engine.py
- redo_days_153_163_deep.py
- verify_recovery_runbook.py
- create_icon_library.py
- analyze-cost-attribution.py
- audit-day030.py
- consume-budget-notifications.py
- compare-regional-tradeoffs.py
- redo_days_155_163.py
- site.js
- day_data_124.py
- assemble.py
- day_data_130.py
- day-004.md
- One day at a time
- Brightloaf Enterprise Cloud: Inheritance and Tagging Taxonomy Guide
- Brightloaf Enterprise Cloud: Organization Policy & Lifecycle Report
- 2. Three Different Capacity-Failure Explanations
- day-007.md
- day-010.md
- day-002.md
- day-006.md
- datetime
- day-005.md
- day-008.md
- Day-page authoring contract
- Brightloaf Enterprise Cloud: Workforce Identity Matrix
- Day 25 Exit Artifact: Redacted Authorization Evidence
- query-cost-export.py
- Day 30 Exit Artifact: Google Cloud Location & Resource-Scope Matrix
- GCP 180-day curriculum site
- day-003-topic-01-lab.md
- day-009.md
- Day 26 Exit Artifact: Authentication & Token Flow Architecture
- Day 27 Exit Artifact: Billing Responsibility Matrix & Budget Thresholds
- simulate-project-billing.py
- Day 28 Exit Artifact: Cost Attribution Worksheet & Duplicate Event Handling Behavior
- Reusable diagram icons
- day-001-topic-01-lab.md
- day-001-topic-03-lab.md
- day-003.md
- day-018-topic-03-lab.md
- generate-authorization-evidence.py
- calculate-budget-thresholds.py
- day-018-topic-01-lab.md
- day-018-topic-02-lab.md
- simulate-iam-conditions.py
- analyze-capacity-failures.py
- reconcile-cost-table.py
- PAGE_UPDATE_PROMPT.md

## God Nodes (most connected - your core abstractions)
1. `render_day()` - 14 edges
2. `parse_day()` - 11 edges
3. `topic_from_html()` - 10 edges
4. `main()` - 10 edges
5. `esc()` - 9 edges
6. `compile_day_page()` - 8 edges
7. `AuditParser` - 7 edges
8. `clean()` - 7 edges
9. `deep_data()` - 7 edges
10. `article_shell()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `deep_data()` --calls--> `table_for()`  [EXTRACTED]
  scratch/redo_days_153_163_deep.py → scratch/upgrade_days_153_163_rich.py
- `deep_data()` --calls--> `topology()`  [EXTRACTED]
  scratch/redo_days_153_163_deep.py → scratch/upgrade_days_153_163_rich.py

## Import Cycles
- None detected.

## Communities (175 total, 136 thin omitted)

### Community 0 - "inspect-adc-and-tokens.py"
Cohesion: 0.36
Nodes (4): compile_exit_artifact(), generate_mock_tokens(), main(), simulate_adc_resolution()

### Community 1 - "build.py"
Cohesion: 0.08
Nodes (25): article_shell(), authored_card(), day_content(), deep_dive(), esc(), executable_extension(), lesson(), main() (+17 more)

### Community 2 - "author_engine.py"
Cohesion: 0.07
Nodes (13): build_and_validate(), compile_day_page(), load_day_module(), main(), parse_range(), process_single_day(), render_architecture_svg(), render_case_depth() (+5 more)

### Community 3 - "redo_days_153_163_deep.py"
Cohesion: 0.12
Nodes (28): clean(), deep_data(), eight_steps(), extract_labs(), hero(), load(), main(), old_html_topics() (+20 more)

### Community 4 - "verify_recovery_runbook.py"
Cohesion: 0.13
Nodes (8): log_step(), MockPubSubEngine, MockServiceInstance, test_baseline_reproduction(), test_failure_injection_datastore(), test_failure_injection_identity(), test_failure_injection_pubsub_poison_pill(), test_reverse_teardown_lifecycle()

### Community 6 - "create_icon_library.py"
Cohesion: 0.12
Nodes (3): incident_svg(), wrap_svg(), svg_diagram()

### Community 8 - "analyze-cost-attribution.py"
Cohesion: 0.36
Nodes (4): analyze_attribution(), compile_exit_artifact(), generate_synthetic_billing_records(), main()

### Community 16 - "redo_days_155_163.py"
Cohesion: 0.53
Nodes (4): make_day(), run(), topic_toc(), write_page()

### Community 127 - "day-004.md"
Cohesion: 0.18
Nodes (10): Step 1 — Calculate the simple payload bounds, Step 1 — Compare the identities, Step 1 — Read the mapping, Step 1 — Read three observations, Step 1 — Select the most specific route, Step 2 — Check the reverse direction, Step 2 — Diagnose the fixture, Step 2 — Explain the version boundary (+2 more)

### Community 128 - "One day at a time"
Cohesion: 0.20
Nodes (7): Content audit — 180-day site, Per-day inventory, One day at a time, Per-day steps, Run mode, Current content limits, GCP Architect · 180-day static site

### Community 129 - "Brightloaf Enterprise Cloud: Inheritance and Tagging Taxonomy Guide"
Cohesion: 0.20
Nodes (9): 1. Executive Summary and Core Architectural Invariants, 2. Mathematical Inheritance Calculation Matrix, 3. The Three-Plane Metadata Taxonomy, 4. Concrete Terraform Implementation Template, Brightloaf Enterprise Cloud: Inheritance and Tagging Taxonomy Guide, Core Business Invariant:, Plane 1: Resource Labels (Operations and Cloud Billing), Plane 2: Resource Manager Tags (Governance and Conditional IAM) (+1 more)

### Community 130 - "Brightloaf Enterprise Cloud: Organization Policy & Lifecycle Report"
Cohesion: 0.20
Nodes (9): 1. Executive Summary & Core Architectural Invariant, 2. Project Lifecycle State Machine Specification, 3. Organization Policy Test Plan & Admission Evaluation Matrix, 4. Policy Rollback Simulation & Recovery Plan, Brightloaf Enterprise Cloud: Organization Policy & Lifecycle Report, Core Business Invariant:, Enforced Constraints:, Evaluation Results (Predictions vs. Observations): (+1 more)

### Community 131 - "2. Three Different Capacity-Failure Explanations"
Cohesion: 0.20
Nodes (9): 1. BigQuery Billing Export Cost Query & Reconciliation Spreadsheet, 2. Three Different Capacity-Failure Explanations, 3. Duplicate Fulfillment Invariant Attestation, Day 29 Exit Artifact: Cost Query Analysis & Three Capacity-Failure Explanations, Failure Explanation 1: Rate Quota Throttling (API Velocity Boundary), Failure Explanation 2: Allocation Quota Exhaustion (Inventory Ceiling Boundary), Failure Explanation 3: Physical Datacenter Capacity Exhaustion (Hardware Inventory Boundary), Invariant Guarantee: &le; 1 Physical Fulfillment per Unique Order ID (+1 more)

### Community 132 - "day-007.md"
Cohesion: 0.22
Nodes (8): Step 1 — Create a synthetic config, Step 1 — Create fixtures and the script, Step 1 — Identify the distribution, Step 1 — Start and inspect a child, Step 2 — Expand the settings locally, Step 2 — Inspect one installed package, Step 2 — Run a success and failure case, Step 2 — Stop and verify cleanup

### Community 133 - "day-010.md"
Cohesion: 0.22
Nodes (8): Step 1 — Create the image source, Step 1 — Evaluate desired versus actual, Step 1 — Read the manifest fixture, Step 2 — Build and test the disposable layer, Step 2 — Repair and extend the ownership diagram, Step 2 — Repair the constraint, Step 3 — Repeat with a named volume, Step 4 — Verify cleanup

### Community 134 - "day-002.md"
Cohesion: 0.25
Nodes (7): Step 1 — Calculate the ranges, Step 1 — Record your machine's local view, Step 1 — Run a local request and response, Step 2 — Label the layers, Step 2 — Trace a supplied route, Step 2 — Trace the fixture, Step 3 — Inject a failure

### Community 135 - "day-006.md"
Cohesion: 0.25
Nodes (7): Step 1 — Create a disposable worker, Step 1 — Identify the current user, Step 2 — Create a private sample, Step 2 — Start and gracefully stop it, Step 3 — Compare a forced stop, Step 3 — Compare read and write permission, Step 4 — Inspect the journal when available

### Community 137 - "day-005.md"
Cohesion: 0.29
Nodes (6): Step 1 — Classify the traffic, Step 1 — Draw the protected path, Step 1 — Evaluate rules in priority order, Step 2 — Diagnose the probe, Step 2 — Repair and test the policy, Step 2 — Repair and verify

### Community 138 - "day-008.md"
Cohesion: 0.29
Nodes (6): Step 1 — Create a small fixture, Step 1 — Run a bounded CPU task, Step 2 — Parse the status field, Step 2 — Read memory and pressure indicators, Step 3 — Classify a supplied incident, Step 3 — Map the remaining tools to boundaries

### Community 140 - "Day-page authoring contract"
Cohesion: 0.29
Nodes (6): Day-page authoring contract, Diagram node logos and icons, Efficient context and edits, Required content, Sources and completion, Subtopic-first discussion

### Community 141 - "Brightloaf Enterprise Cloud: Workforce Identity Matrix"
Cohesion: 0.29
Nodes (6): 1. Executive Summary & Core Architectural Invariants, 2. Workforce Identity Matrix: People, Workloads, Groups, and Externals, 3. Direct User to Group Consolidation Audit, 4. Domain Restricted Sharing & Public Access Prevention, Brightloaf Enterprise Cloud: Workforce Identity Matrix, Core Business Invariant:

### Community 142 - "Day 25 Exit Artifact: Redacted Authorization Evidence"
Cohesion: 0.29
Nodes (6): 1. Effective Policy Graph Resolution, 2. Redacted Authorization Decision Evidence, 3. Invariant Verification & Compliance Attestation, Day 25 Exit Artifact: Redacted Authorization Evidence, Principal: `group:all-devs@brightloaf.internal`, Principal: `serviceAccount:order-ingest@brightloaf-prod.iam.gserviceaccount.com`

### Community 143 - "query-cost-export.py"
Cohesion: 0.38
Nodes (3): execute_cost_query(), load_detailed_billing_records(), main()

### Community 144 - "Day 30 Exit Artifact: Google Cloud Location & Resource-Scope Matrix"
Cohesion: 0.29
Nodes (6): 1. Executive Summary & Architectural Scope, 2. Resource Classification Matrix by Availability Scope, 3. Multi-Criteria Regional Comparison: Candidate Regions, 4. Organization Policy Guardrails: `constraints/gcp.resourceLocations`, 5. Duplicate Fulfillment Invariant Protection Protocol, Day 30 Exit Artifact: Google Cloud Location & Resource-Scope Matrix

### Community 145 - "GCP 180-day curriculum site"
Cohesion: 0.33
Nodes (5): GCP 180-day curriculum site, Handoff, Instruction sources and precedence, Page acceptance rules, Required curriculum-page workflow

### Community 146 - "day-003-topic-01-lab.md"
Cohesion: 0.33
Nodes (5): Step 1 — Confirm Python, Step 2 — Parse addresses and a prefix, Step 3 — Trace supplied resolver answers, Step 4 — Inject and diagnose one failure, Step 5 — Verify and keep the artifact

### Community 147 - "day-009.md"
Cohesion: 0.33
Nodes (5): Step 1 — Observe the current process, Step 1 — Read the placement fixture, Step 2 — Compare with a local container if available, Step 2 — Inject a boundary failure, Step 3 — Explain two boundaries

### Community 148 - "Day 26 Exit Artifact: Authentication & Token Flow Architecture"
Cohesion: 0.33
Nodes (5): 1. Application Default Credentials (ADC) Search Chain, 2. Separation of Authentication vs. Authorization, 3. Dissected OIDC ID Token Claims, Critical Security Assertions:, Day 26 Exit Artifact: Authentication & Token Flow Architecture

### Community 149 - "Day 27 Exit Artifact: Billing Responsibility Matrix & Budget Thresholds"
Cohesion: 0.33
Nodes (5): 1. Cloud Billing Responsibility Matrix (RACI), 2. Calculated Monthly Budget Alert Thresholds, 3. Programmatic Pub/Sub Alert Event Schema, Day 27 Exit Artifact: Billing Responsibility Matrix & Budget Thresholds, Invariant & Safety Compliance Attestation:

### Community 151 - "Day 28 Exit Artifact: Cost Attribution Worksheet & Duplicate Event Handling Behavior"
Cohesion: 0.33
Nodes (5): 1. Departmental Cost Attribution Worksheet, 2. Notification Handling Behavior for Duplicate Pub/Sub Events, Day 28 Exit Artifact: Cost Attribution Worksheet & Duplicate Event Handling Behavior, Granular Resource Line Items:, Safety & Invariant Attestation:

### Community 152 - "Reusable diagram icons"
Cohesion: 0.40
Nodes (4): Regenerate, Reusable diagram icons, Reuse in a day page, Sources and rights

### Community 153 - "day-001-topic-01-lab.md"
Cohesion: 0.40
Nodes (4): Step 1 — Check your tools, Step 2 — Create the evidence repository, Step 3 — Record a command and its exit code, Step 4 — Write and commit the baseline

### Community 154 - "day-001-topic-03-lab.md"
Cohesion: 0.40
Nodes (4): Step 1 — Confirm the workspace, Step 2 — Create synthetic order data, Step 3 — Record the safety boundary, Step 4 — Commit and verify

### Community 155 - "day-003.md"
Cohesion: 0.40
Nodes (4): Step 1 — Read the fixture, Step 1 — Read the trace, Step 2 — Check the state boundary, Step 2 — Check the typed answers

### Community 156 - "day-018-topic-03-lab.md"
Cohesion: 0.40
Nodes (4): Step 1 — Tour the project context, Step 2 — Try a pinned product, Step 3 — Configure an alert if allowed, Step 4 — Verify and clean up

### Community 157 - "generate-authorization-evidence.py"
Cohesion: 0.60
Nodes (3): evaluate_permission(), main(), resolve_effective_policy()

### Community 158 - "calculate-budget-thresholds.py"
Cohesion: 0.60
Nodes (3): calculate_thresholds(), compile_exit_artifact(), main()

### Community 159 - "day-018-topic-01-lab.md"
Cohesion: 0.50
Nodes (3): Step 1 — Identify the environment, Step 2 — Check billing ownership, Step 3 — Check the trial state

### Community 160 - "day-018-topic-02-lab.md"
Cohesion: 0.50
Nodes (3): Step 1 — Read current limits, Step 2 — Trace the complete workload, Step 3 — Inspect budget protection

## Knowledge Gaps
- **138 isolated node(s):** `Instruction sources and precedence`, `Required curriculum-page workflow`, `Page acceptance rules`, `Handoff`, `Per-day inventory` (+133 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 496 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **136 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Instruction sources and precedence`, `Required curriculum-page workflow`, `Page acceptance rules` to the rest of the system?**
  _138 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `build.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07801418439716312 - nodes in this community are weakly interconnected._
- **Should `author_engine.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07396870554765292 - nodes in this community are weakly interconnected._
- **Should `redo_days_153_163_deep.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12380952380952381 - nodes in this community are weakly interconnected._
- **Should `verify_recovery_runbook.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12857142857142856 - nodes in this community are weakly interconnected._
- **Should `sys` be split into smaller, more focused modules?**
  _Cohesion score 0.11695906432748537 - nodes in this community are weakly interconnected._
- **Should `create_icon_library.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._