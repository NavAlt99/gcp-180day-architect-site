# Day-page authoring contract

Canonical rules for every page update: read once as a static prefix before day
inputs. Wrappers reference these rules; token savings must not reduce page
structure, technical depth, or acceptance evidence.

## Source precedence

1. `../roadmap-180-days.md`: scope/prerequisites/Study/Practice/Exit evidence.
2. `../gcp-architect-180-day-page-prompts.md`: compact day brief/anchors.
3. `data/coverage.csv`: topic/anchor/source-ID/publisher/exit mappings.
4. `../gcp-architect-roadmap-100-days.md`: source-topic references/official docs.
5. This contract: teaching/evidence/SVG/lab/source/rendering rules.
6. `ONE_DAY_AT_A_TIME.md`: serial run; `PAGE_UPDATE_PROMPT.md`: commands/handoff;
   `AGENTS.md`: entry point.

HTML is output, not curriculum truth. Current roadmap overrides older prompts;
alternate Day 13 is noncanonical. Stay within Study/Practice/Exit evidence;
comparisons do not justify extra products/deployments. Brightloaf synthetic
examples are optional when useful.

## Content invariants

Preserve shell, navigation, 180-day selector, progress/theme controls, footer,
and useful eligible visuals. Keep four numbered parts and exact coverage-row
overview/technical/problem/lab anchors (e.g. `#topic-01-overview`); subtopics
supplement them. Durable source: `scratch/day_data_NNN.py`; never hand-edit
`content/day-NNN-page.html` or `days/day-NNN.html` as source. Build one named day,
never the full site. Fix only introduced issues and rerun checks before advancing.
No generic fallback prose/root causes/lab steps or unfilled placeholders.

Write concise non-repetitive prose without reducing depth, retaining mechanisms,
ownership/boundaries, limits, trade-offs and evidence.

Depth floor (user decision): conceptual depth may increase but must never decrease. Scheduled study time never caps or shortens an explanation. If a topic needs more worked mechanism, examples, or lab detail than the schedule suggests, write it and note the time overrun in the handoff; do not trim it. Token savings come only from structure (shared helpers, defaults, compact diagram specs, read budget), never from shorter prose, fewer subtopics, fewer examples, or thinner labs. Existing page content may be revised only to add or correct depth, not to condense it.

### Part 1: Topics of the day

Each mapped topic: what it is, why today, where it sits. Closing problem-preview:
exactly two sentences (symptom/decision, then user/business effect); links may follow.

### Part 2: Subtopic-first technical discussion

Preview sentence count applies ONLY to Part 1 (`topics[].preview` or `part1_html`),
not Part 2 technical content; existing engine does not enforce sentence count.

List ALL scoped subtopics first, derived from Study/brief/coverage, not later days.
Explain each in order under a descriptive heading with these explicit labels:
- **What it is in general:** plain definition, first-use acronym expansions,
  mechanism, concrete topic example.
- **Relevance to a cloud architect:** design/ownership/reliability/security/cost/
  operational trade-off across providers.
- **Relevance to GCP:** documented service/feature/configuration/architecture use
  and primary source; if no direct equivalent, say so and explain applicability.
  Never invent mappings or deployments.

Cover control/data flow, ownership, boundaries, limits, failure signals,
trade-offs and prerequisites; add an accessible architecture-path table where
useful. End with a concrete example, **Evidence limit:** and verified authoritative
written section. Headings/lists/links/repeated or generic relevance are not
explanations. Video segments/timestamps must be actually checked.

### Part 3: Problem and solution

One labeled case/topic: symptoms, literal logs, business/operational constraints,
causal root reasoning, diagnostic sequence, defensible fix, verification, residual
risk. Logs labeled **supplied**, **illustrative** or **local-observed**; supplied
text verbatim, measured distinct from expected, never production observation.
Facts/inferences/predictions/questions stay distinct; unknown causes stay unknown.
Event replay: one business fulfillment per order.

### Part 4: Executable labs

Named exercise per topic, or integrated exercise with explicit topic checkpoints:
exactly eight stages under **Exact execution**, with topic-specific names/actions:
1. Preflight: validate assumptions/environment.
2. Prepare target, inputs, or backing resources.
3. Author plan, configuration, or analysis.
4. Execute or simulate the planned change.
5. Inspect expected state and verify outcomes.
6. Rehearse bounded failure, edge case, or decision challenge.
7. Diagnose evidence and record remediation/decision.
8. Clean up or close out.

Every stage: location (local terminal, Cloud Shell, GCP VM terminal, Console,
or local/tabletop worksheet), OS/shell/tools, ordered exact actions/inputs/file
contents, observable expected result, evidence/path to save, stop/recovery where
needed. Define variables/prerequisites/dependencies/tools/paths before use and
how environment values are obtained. Headings or generic review/analyze/verify
alone are insufficient.

Use copyable commands or complete Terraform including prerequisites and
init/plan/apply/inspect/destroy. Otherwise give numbered Console/editor/worksheet
navigation, exact fields/values/result AND official procedure link, not link alone.
Local/tabletop tasks need exact calculation/decision inputs and visible outcomes,
not invented provisioning/fault injection. Explain BOTH local/GCP preparation,
execution and handoff when involved. Prefer local/tabletop when Practice permits;
state untested GCP behavior, never deploy merely to add a cloud variant.

Include goal/result, mode/limits, prerequisites, preflight, execution, expected
state, verification, troubleshooting, cleanup/cost, acceptance after eight stages,
and roadmap Exit evidence mapping. Cloud preflight verifies identity/project/APIs/
permissions/location/inventory/billing/bounded cost. Stage 8 removes only lab-owned
resources in reverse dependency order or explicitly closes the local artifact.

## Typography and inline code

Selected first-use prose terms: `<strong class="keyword">term</strong>` with
shared pink/tinted highlight (Kubernetes example); no whole sentences or commands.
Labels Why today/Where it sits/combined use `<strong class="side-heading">`;
labels and subtopic headings are blue/bold in both themes via `assets/site.css`,
not per-day patches. Rich fields accept Markdown/HTML, plain fields are escaped;
use `part1_html` for rich overview. Copyable commands/multiline contents use
`<pre><code>` and working copy controls. Inline commands use `<kbd>`; non-command
filenames/short terms use `<code>`. Expected environment-dependent cloud output
is illustrative.

## Diagram eligibility and standards

Diagram quality floor (user decision): compact diagram data may replace hand-written SVG markup only when the rendered result is at least as clear as before: every node has its correct icon, labels are complete (wrapped or enlarged, never truncated), arrows and numbered transitions are unambiguous, nothing clips or overlaps, and accessibility and caption requirements still hold. When the renderer cannot meet this, author raw SVG instead. Token savings must never reduce diagram clarity, icon coverage, or label completeness.

ONLY diagram actual multi-step sequences, packet traversal or request/response
lifecycles. No conceptual/static/configuration diagrams, invented qualifying flows,
or empty headings/wrappers/captions/placeholders. Applies to Part 2 topology and
Part 3 incidents, overriding blanket requirements. Explicit boolean
`scenario["diagram_enabled"]`: False when nonqualifying, True for eligible incidents;
legacy missing-key behavior remains. Empty `ARCH_DIAGRAM`/`ARCH_SVG_HTML` if no
Part 2 flow qualifies. Place subtopic SVGs beside their explanation, not unrelated
infrastructure. Number transitions with meaningful arrows and matching nearby
prose; linear flows are valid.

Applicable multi-tier topology standard: minimum 1120x690; non-overlapping tiers
Ingress/Demand y=55..147, Runtime/Data y=185..395, Governance/Decision y=435..550;
vertical drops x1=x2 into centers; boundary boxes end before y=560; bottom probe
panel. Eligible incident standard: five-node dual-lane progression Initiating
Event -> Root Cause Defect/FI -> Impact & Degradation versus Same Trigger ->
Defensive Control -> Verified Outcome; boundary encloses nodes 2/3; FI badge;
figcaption **Supplied facts**, **Architectural inference**, **Expected post-fix
behavior**. Standards are in the engine; no Day 96/121 page-template reads.

Every SVG: viewBox, role=img, unique title/desc IDs, aria-labelledby, readable
labels, icon/node, horizontal scroll wrapper, scope/evidence-limit caption.
Check text/icons/badges/arrows for clipping/overlap; labels/path explain without
color/icon recognition. Wrap/reflow labels or enlarge nodes without reducing depth or removing meaning;
never shrink illegibly or mask body overflow with overflow-x:hidden.

## Diagram icons

Reuse `assets/icons/`; targeted `manifest.json` mappings/provenance, `index.html`
previews, `README.md` embedding. Prefer `gcp/core/` to `gcp/legacy/`. Every GCP
service node uses its matching official product icon, not a generic provider logo;
preserve colors/proportions. Label provider boundaries separately, provider logo
where appropriate. Generic client/router/switch/firewall/load-balancer/DNS/endpoint
nodes use recognizable icons; events/decisions/policies/artifacts/outcomes use
labeled concept icons, not implied services.

Missing official icons: obtain authentic Google Cloud architecture assets,
add locally with manifest provenance; no redrawn/generated logos or emoji. Missing
generic icons: original labeled SVG, not a Google mark. Local assets/symbols must
work offline; verify every node mapping and asset reference.

## Sources and evidence

Official primary written docs for changeable product behavior, certification/
exam, quotas, prices, versions, eligibility. Open cited sections; verify actual
fragment/title/subject supports descriptive labels; date access. Prefer second
written source to unverified video; never invent segments/timestamps. Separate
supplied facts, local observations, tabletop predictions, design inferences and
open questions. No invented production behavior/exam results/outputs/quotas/prices/
latency/causality/customer acceptance. No credentials/protected exam/payment data.

Study-link checks cover HTTP/redirects, local targets, exact fragments, NOT
relevance. Manually verify every Further study subject/label. Fix broken,
irrelevant or misleading targets; missing fragments/non-success/access restrictions
remain unresolved, not passes. Record dates/report/limits. Checker changes require
its documented unit tests.

## Permanent rendering rules

Follow `RENDER_REVIEW.md`: shared fixes/target markup guards, saved desktop/mobile
both-theme audits, focused diagram/copy checks. Light cards/TOC/tables/rail retain
active indicator; dark-canvas captions readable; scrolling contained, selector/
progress keys/copies intact. Fix introduced errors. Audits cannot prove every
text overlap/arrow/source/eligibility decision; rendered reads follow Read budget.

## Read budget

After static rules read ONLY the day's roadmap entry, compact brief, coverage.csv
rows, and durable `scratch/day_data_NNN.py` if present. Extract brief/entry using
bounded grep/rg and sed, never full 180-day catalog/roadmap, unrelated days or
selector markup. Give each context only its compact brief. Precedence item 4,
icon metadata/source sections or flagged CSS/JS are targeted exceptions only when
needed, not full-file reads.

Do NOT routinely read `content/day-NNN-page.html`, `days/day-NNN.html`, rendered
pages, `author_engine.py`, `build.py`, Day 96/121 pages. Use available `SPEC_SCHEMA.md` instead
of engine internals; its `SPEC_DEFAULTS.json` appendix lists fallback expressions.
`scripts/validate_spec.py --day N` checks authored source before compilation, without building or reading rendered pages.
For missing specs, available `scripts/new_day_skeleton.py --day N` creates a
coverage-based TODO skeleton without overwriting authored input. Run validators/browser audit
without full rendered text/screenshots in author context. Open/read rendered pages
ONLY for a specific validate.py/browser-audit problem, ONLY the flagged region.
Review depth/coverage/eligibility in durable spec; retain source/audit checks.
This overrides unconditional rendered reading, not teaching or acceptance checks.

## Day-specific execution and handoff

After static rules select CURRENT_DAY N (NNN zero-padded); use serial workflow
and update prompt commands/handoff. No cross-day assumptions. Wait for background
completion, no status polling/loops. Handoff stays concise; report depth changes as a separate item, not as content recap.
