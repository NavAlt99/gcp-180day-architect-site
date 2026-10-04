# Token-efficiency report — Phases 0, A, B, C and D

Latest status: Phase E (option 6) complete; Phase F and later remain deferred.
The Phase 0/A sections below retain historical measurements and scope statements.

## Original Phase 0/A scope and commits

Branch: `token-efficiency`, starting at e729d87 from `prompt-fix`.
Phase 0 commit: e33bcfb (baseline). Phase A is the commit containing this report.
Only Phase 0 and Phase A executed. No Phase B or later work has started.

## Phase 0: baseline

Built only Days 002 and 003; validated Day 002. Day 003 is an existing legacy
single-file spec using uppercase PART*_HTML/TOPICS variables, not a DATA/DAY_DATA
dictionary. Its spec and all engine behavior remain untouched. Saved rendered
HTML, SHA-256, sizes and exact original four instructions from `git show HEAD` in
`scratch/baseline/`. Rebuilt both days and compared bytes: identical. Purpose:
a reproducible no-render-change regression and honest before/after measurement.
Saving originals adds repository bytes, but they are audit evidence excluded from
routine authoring context, not a per-page token cost.

## Phase A: changes, justification, measured effect

1. Moved repeated precedence, teaching, typography, diagram, lab, source, evidence,
   and rendering rules into `PAGE_AUTHORING_CONTRACT.md`. Replaced the three
   wrappers with entry-point, serial-selection, command and handoff instructions.
   Why: one canonical rule copy avoids repeated reads/conflicting wording while
   retaining every requirement. Exact numeric topology and incident standards,
   all stage acceptance details and icon provenance rules remain. Contract is
   11,636 bytes (~11.4 KiB), near the approximate 10 KB target; kept the additional
   detail to preserve complete traceability rather than silently remove rules.
2. Static rules precede day-specific invocation; references replace copies.
   Why: stable prompt prefix is suitable for caching. No actual tokenizer or
   provider-cache savings are claimed; only requested bytes/4 estimates measured.
3. Added bounded Read budget, replacing unconditional generated-page/engine/template
   reads in all four instructions and `RENDER_REVIEW.md`. Routine reads: day's
   roadmap entry, extracted brief, coverage rows, durable spec. Necessary primary
   source/icon sections and flagged CSS/JS are bounded exceptions preserving source
   accuracy and assets. Browser audits still run without full rendered context;
   inspect ONLY flagged regions. Why: reduce context input without weakening
   technical depth or validation. Per-run read savings depend on day/flags and
   are not measured in this documentation-only run.
4. Resolved anchors, labeled logs, inline command tags and preview sentence location
   globally. Exactly two preview sentences are Part 1 only; narrowly checked engine
   Part 1/2 confirms preview is emitted in Part 1, not Part 2. Engine never enforced
   sentence count; no new automatic enforcement is claimed. Unknown root causes
   stay unknown. Why: remove contradiction-driven retries without changing pages.
5. Found existing `RENDER_REVIEW.md`; retained its unique audit procedure and moved
   duplicated shared rules to the contract. Applied read policy everywhere, including
   screenshot/visual inspection of flagged regions only. Original review text
   archived in baseline and superseded policy noted explicitly. Not reconstructed.
   Why: prevent this fifth instruction file from reintroducing full-page reads.
6. Created `scratch/instruction-traceability.md`: all 109 original requirement lines
   map to canonical sections or unique workflow/prompt destinations. Long original
   lines contain multiple clauses; their destination list covers those clauses.
   Full originals are archived. Zero unmapped requirements; no files deleted.
   Why: make consolidation reviewable and show every superseded policy explicitly.
7. Updated every live instruction file together before regression/commit, not
   separate partially inconsistent phases. Workflow maintenance boundary in AGENTS
   records the user's phase/stop requirement. No new curriculum requirement added.

## Byte measurements

Bytes/4 is an estimate, not model-token measurement. Savings below count each live
instruction once; baseline archives/traceability are not read by day agents.

| File | Before bytes | After bytes | Before tokens est. | After tokens est. | Saved bytes |
|---|---:|---:|---:|---:|---:|
| AGENTS.md | 3,819 | 1,111 | 954.75 | 277.75 | 2,708 |
| ONE_DAY_AT_A_TIME.md | 3,044 | 1,469 | 761.00 | 367.25 | 1,575 |
| PAGE_UPDATE_PROMPT.md | 7,823 | 1,721 | 1,955.75 | 430.25 | 6,102 |
| PAGE_AUTHORING_CONTRACT.md | 15,335 | 11,636 | 3,833.75 | 2,909.00 | 3,699 |
| scratch/day_data_002.py | 67,330 | 67,330 | 16,832.50 | 16,832.50 | 0 |
| **Four instructions total** | **30,021** | **15,937** | **7,505.25** | **3,984.25** | **14,084** |

Instruction reduction: **46.91%**, or **3,521.00 estimated tokens** per all-four-file read. Day 002 spec is unchanged.

Additional audit procedure: RENDER_REVIEW.md 3,266 → 2,745 bytes (816.50 → 686.25 estimated tokens).

## Options 1–10: scoped accounting

The original Phase A request associates consolidation with options 8, 9, 1 and 2.
The table below records Phase A status; the user subsequently supplied labels
for deferred options. Current Phase C status appears in the follow-up below.
Shared file savings are not double-counted across overlapping options.

| Option | What changed / why | Files | Measured effect |
|---|---|---|---|
| 1 | Bounded day-input Read budget; avoid full catalogs/unrelated pages | Contract, three wrappers, render procedure | Read volume not benchmarked; contributes to aggregate bytes reduction |
| 2 | Static rules first; avoid routine generated-page/engine/template reads; forward schema reference | Same instruction files | Stable prefix established; provider cache benefit unmeasured |
| 3 | Phase C helpers/defaults: not executed during Phase A | None | 0 in Phase A; follow-up status below |
| 4 | Phase D compact diagrams: not executed during Phase A | None | 0 in Phase A; follow-up status below |
| 5 | Phase D directory specs: not executed during Phase A | None | 0 in Phase A; follow-up status below |
| 6 | Phase E spec linter: not executed during Phase A | None | 0 in Phase A; follow-up status below |
| 7 | Phase F study-link checker: not executed during Phase A | None | 0 in Phase A; follow-up status below |
| 8 | One canonical contract; short unique wrappers; duplicate rules moved | Four instructions, render procedure | Per-file table and aggregate above |
| 9 | Resolve four contradictions, record superseded policies, map requirements | Contract, wrappers, render procedure, traceability | 109 original lines mapped; 0 unmapped; rendered diffs empty |
| 10 | Phase G audit output: not executed during Phase A | None | 0 in Phase A; follow-up status below |

## Regression and checks actually run

Phase 0: `python3 scripts/build.py --day 2`; `python3 scripts/validate.py --day 2`;
`python3 scripts/build.py --day 3`; repeat BOTH builds, compare to saved HTML/hash.
Phase A: rebuild BOTH named days, `diff -u` both baseline/current pairs, SHA-256
assertions, `python3 scripts/validate.py --day 2`, requirement-map coverage and
`git diff --check`. Repeated final checks use the same two target builds only.

- day-002.html: byte-identical; 122760 bytes; sha256 86323aef6497c2ec31cf87f9b239f52b04f276532d9294b62610aa5f9c1f584a
- day-003.html: byte-identical; 153299 bytes; sha256 37660836009b5ae726c3a3879cf9ce74962f7b2e0372fb6c6422f94932f8f8b6

Results: byte-identical pages (not even whitespace/order changes), zero validator
errors, zero unmapped original requirements. No regression-triggered stop/revert.
Full-site validation reads existing pages; no full-site build was run.

## Original Phase 0/A unchanged scope and limitations

- All day specs, overrides, rendered pages, CSS, JS, engine, build/validator/checker
  code, coverage.csv, roadmap/catalog content and local icons unchanged. No Day 003
  migration, reauthoring or lab execution. Four parts/anchors/eight-stage labs/
  subtopic depth/diagram eligibility/typography/source rules preserved.
- No schema/skeleton, helper/default extraction, scenario deduplication, compact
  diagram conversion, directory specs, spec linter, link-cache/excerpt changes,
  audit-output code changes or new tests: all B–G work deferred until `continue`.
- `SPEC_SCHEMA.md` is intentionally not created yet; the forward dependency is
  stated, not treated as available. `validate_spec.py` also does not exist yet;
  it was not run or added to current executable commands prematurely.
- No fresh browser/source-link checks this phase: no rendered content or runtime
  changed; requested regression/structural validation checks were executed instead.
- Existing audit limitations remain: not every overlap, arrow ambiguity or
  technical/source error is machine-detectable. New read policy permits flagged
  visual regions only, per user's explicit direction; this is documented globally.
- Baselines preserve output; build-only legacy regression is not proof that a
  legacy spec meets newly clarified authoring requirements or regenerates identically
  through author_engine. That engine regression belongs to later phases.
- Repo files, not the full prompt stream, were measured. Runtime/caching savings,
  actual model tokenization and future per-day outcomes remain unmeasured.

Stop after Phase A commit. Do not begin Phase B until the user replies `continue`.


## User-approved depth floor — instruction-only follow-up

Depth floor (user decision): conceptual depth may increase but must never decrease. Scheduled study time never caps or shortens an explanation. If a topic needs more worked mechanism, examples, or lab detail than the schedule suggests, write it and note the time overrun in the handoff; do not trim it. Token savings come only from structure (shared helpers, defaults, compact diagram specs, read budget), never from shorter prose, fewer subtopics, fewer examples, or thinner labs. Existing page content may be revised only to add or correct depth, not to condense it.

This supersedes both the earlier current-user-allowance decision and the original proportional-to-scheduled-study-time rule. Non-repetitive remains; every live concise directive now explicitly says without reducing depth. Diagram labels use wrap/reflow or larger nodes instead of shortening. Handoff now reports increased topic depth and study-time overruns and confirms no existing explanation was shortened. All five instruction files were searched and treated together; exact before/after wording is in scratch/depth-floor-decision.md.

Phase A measurements remain: four files 30,021 → 15,937 bytes; 7,505.25 → 3,984.25 bytes/4 estimated tokens; 46.91% reduction. These are historical Phase A values, not silently replaced by this follow-up. Day 002 spec remains 67,330 bytes (16,832.50 estimated tokens). Part 2 preview decision remains: exactly two preview sentences are Part 1 only (topics[].preview or part1_html); Part 2 technical explanations have no such sentence limit. Existing engine does not enforce preview sentence count.

Follow-up current sizes (not a remeasurement of Phase A):

| File | Bytes | Estimated tokens (bytes/4) |
|---|---:|---:|
| AGENTS.md | 1,134 | 283.50 |
| ONE_DAY_AT_A_TIME.md | 1,469 | 367.25 |
| PAGE_UPDATE_PROMPT.md | 1,847 | 461.75 |
| PAGE_AUTHORING_CONTRACT.md | 12,304 | 3,076.00 |
| scratch/day_data_002.py | 67,330 | 16,832.50 |

Follow-up verification: rebuild only Days 002 and 003, compare bytes and SHA-256 with Phase 0 baseline; run target Day 002 structural validation and git diff --check. Results recorded in scratch/baseline/depth-floor-checks.txt. No spec, rendered content, engine, helper, diagram, lab, CSS/JS, or source changes. Stop after commit; Phase B not started.


## Phase B — schema and coverage skeleton (authorized follow-up)

Inspected author_engine/build contracts once for this maintenance run, then supplied SPEC_SCHEMA.md and machine-readable SPEC_DEFAULTS.json so day authors need not reread implementation. The schema documents recognized fields, rich/escaped branches, exact fallback appendix, ignored author metadata, legacy loader precedence and limitations (including PART1_HTML not collected by legacy fallback). Only structure may be defaulted, never depth. New_day_skeleton.py reads only target coverage rows, copies keys/titles/exact anchor metadata, supplies eight location/actions/expected/save TODO stages, refuses overwrite, and supports a separate scratch fixture output. Empty diagram fields do not imply diagram eligibility; authored boolean decision is mandatory. No content was inferred or shortened.

Instruction fixes: contract handoff now reads the exact requested concise-report wording; prompt item 5 requires git diff on the durable spec and an explicit no-prose-removal statement. Read budget now identifies schema/skeleton as available. Traceability forward dependency resolved. No read-budget or acceptance rule weakened.

Measurements: SPEC_SCHEMA.md 2996 bytes (749.00 estimated tokens); SPEC_DEFAULTS.json 5278 bytes; new_day_skeleton.py 4832 bytes. Day 002 spec unchanged: 67,330 bytes (16,832.50 estimated tokens). Schema is a stable prefix; actual provider token/cache effects not benchmarked. Skeleton boilerplate is generated without author tokens, but per-page savings vary.

Checks: Day 003 scratch fixture covers all three mapped topics and eight complete stage-label/sentinel slots; DATA loader equality passes; Day 002 overwrite attempt correctly refused (exit 2). Builds Day 002/003 only: byte-identical baseline, hashes unchanged. Day 002 structural validation: 0 errors. No generic content accepted. Legacy spec files and all rendered pages unchanged. Phase B commit contains these results; no Phase C changes mixed into it.


## Phase C — shared helpers and safe lab slots (option 3)

What and why: moved the Day 002 escape/dedent imports and source, keyword,
subtopic, discussion, flow_svg, stage, workspace, write_file, lab and case helpers
into scratch/day_helpers.py. Explicit partial-bound Day 002 context retains every
original sentence, lab prerequisite, provenance label and diagram caption.
Shared helpers contain assembly logic, not substitute teaching explanations.
No other day was migrated. The existing flow_svg geometry remains unchanged;
compact flow data is Phase D and was not introduced.

The engine supplies seven structural lab slots (mode, prereq, preflight,
verification, trouble, cleanup, accept), each with TODO:. Explicit authored fields
win. New skeletons and Day 002 opt in with empty lab_defaults metadata. The
compiler rejects unresolved TODOs anywhere in labs and blank default slots before
writing overrides. Helpers leave missing lab/context/location slots unfinished.
Legacy specs without lab_defaults retain historical omission rendering for backward
compatibility; this is not permission for generic new labs. The future Phase E
linter remains deferred, so legacy generic fallback prose is not newly classified
by this run. Only structure may be defaulted; the depth floor is unchanged.

Day 002 CASES already held the sole literal scenario content. Removed that extra
container and constructed TOPICS scenario entries directly, deriving the completed
topic dictionaries from them. No duplicate scenario prose was deleted because
none existed. This reduces structural indirection, not teaching depth.

Files touched: scratch/day_helpers.py, scratch/day_data_002.py,
scripts/author_engine.py, scripts/new_day_skeleton.py, SPEC_SCHEMA.md,
SPEC_DEFAULTS.json, scratch/instruction-traceability.md, this report,
scratch/baseline/phase-c-input-hashes.txt, scratch/baseline/phase-c-checks.txt,
and scratch/spec-fixtures/phase-c-day-003-skeleton.py (a separate unfinished
fixture, not the durable Day 003 spec). Phase B changed the contract/prompt
handoff and Read budget, added the schema/default appendix/skeleton, and retained
its separate fixture/check evidence; commit 203ba0b records that phase.

### Phase B/C measurements

Bytes/4 estimates measure repository text, not actual tokenizer or provider cache
usage. Phase B values precede helper extraction; instruction increases document
explicit user requirements and available tools, rather than claiming savings.

| File | Before B bytes | After B bytes | After C bytes | Before tokens | After B tokens | After C tokens |
|---|---:|---:|---:|---:|---:|---:|
| AGENTS.md | 1134 | 1134 | 1134 | 283.50 | 283.50 | 283.50 |
| ONE_DAY_AT_A_TIME.md | 1469 | 1469 | 1469 | 367.25 | 367.25 | 367.25 |
| PAGE_UPDATE_PROMPT.md | 1847 | 1924 | 1924 | 461.75 | 481.00 | 481.00 |
| PAGE_AUTHORING_CONTRACT.md | 12304 | 12336 | 12336 | 3076.00 | 3084.00 | 3084.00 |
| scratch/day_data_002.py | 67330 | 67330 | 63292 | 16832.50 | 16832.50 | 15823.00 |

Day 002 per-page specification reduction: 4038 bytes / 1009.50 estimated tokens
(6.00%). Shared helpers add 5526 bytes once (1381.50 estimated tokens); spec plus
helpers totals 68818 bytes, 1488 more than the original single file. This is a
per-page context reduction when shared helpers are reused without rereading them,
not a claim of net repository shrinkage. Schema after C: 2996 bytes; exact-default
appendix 5801 bytes; skeleton script 4864 bytes. Defaults chiefly save generation
of scaffolding; their standalone token benefit has not been benchmarked.

### Checks, depth and deferred options

Both phases rebuilt only Days 002 and 003 and compared baseline bytes/hashes:
PASS, no whitespace differences. Phase C also regenerated Day 002 through the
engine: identical override/rendered output, validator 0 errors. Entire loaded Day
002 and legacy Day 003 content equals pre-C data after JSON normalization and
excluding only new structural lab_defaults metadata. Reviewed git diff on
scratch/day_data_002.py: it removes no explanatory prose, only structure; no facts
were corrected. No topic depth decreased or increased, no study-time overrun.
All 14 subtopics and 32 lab stages remain intact. The initial direct Python data
comparison distinguished tuples from JSON lists; normalization resolved that
comparison issue, with no content or rendered-page change.

Skeleton coverage/eight-stage/TODO/overwrite checks PASS in Phase B. Phase C
checks confirm unresolved/blank defaults, helper omissions, and missing stage
location reject; unfinished skeletons reject before modifying the override;
legacy omitted-field dictionaries remain unchanged. git diff --check passes.
Evidence: scratch/baseline/phase-b-checks.txt and phase-c-checks.txt. No new unit
test suite was introduced (Phase E remains deferred); no full-site build, fresh
browser review, remote link check or cloud lab execution was needed for unchanged
pages. The engine CLI invokes existing whole-site validation, not a whole-site
build. Part 2 preview decision remains unchanged: two sentences apply only to
Part 1; Part 2 explanations have no two-sentence limit.

Current option status: 3 (Phase C helpers/defaults) implemented above; 4 and 5
(Phase D diagrams/directory specs), 6 (Phase E linter), 7 (Phase F links) and
10 (Phase G audit output) remain deferred. Options 1, 2, 8, 9 retain Phase A
measurements above. Raw SVGs, generated HTML, day structure/anchors, typography,
icons, sources, CSS/JS, lab detail and every other durable day spec remain
unchanged. Stop after the Phase C commit; do not begin Phase D.


## Phase B/C follow-up — whole-spec unfinished-content enforcement

What/why: author_engine.py now shares a recursive TODO path scanner between lab
resolution and whole-spec validation. Before any compiler write it checks every
loaded topic/day field, nested list/tuple/dict value and dict key, including
technical prose, preview, scenario evidence/provenance, references, completion
and source metadata. Errors identify the topic key and field path, or explicitly
identify day-level fields. Generated lab-default TODO errors also identify the
topic. No text fallback or rendering behavior changed for finished specs.

Skeleton references now retain coverage publisher URLs behind TODO: verify;
SOURCES uses the Day 002 key -> (label, URL) shape with TODO labels/verified URLs,
and ACCESS_DATE is TODO. DATA includes that metadata so the whole-spec scan
covers it. Only lab.file is prefilled to the engine's day-NNN-key.md default;
all teaching slots remain unfinished. Existing historical fixtures are retained
as Phase B/C evidence rather than overwritten or deleted. Tests generate fresh
fixtures in a temporary directory and verify refusal to overwrite them.

SPEC_SCHEMA.md documents source emission and whole-spec checks and lists
non-empty generic prose fallbacks from SPEC_DEFAULTS.json as future Phase E
rules. Legacy fallbacks remain unchanged; Phase E was not implemented. Exact
fallback appendix note updated. Files touched: scripts/author_engine.py,
scripts/new_day_skeleton.py, SPEC_SCHEMA.md, SPEC_DEFAULTS.json,
tests/test_authoring_followup.py, this report, and
scratch/baseline/phase-bc-followup-checks.txt. No other instructions prescribe the
old skeleton shape or lab-only guard; canonical instructions remain applicable.

Checks actually run:
- PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p
  'test_authoring_followup.py' -v: PASS, 9 tests with topic/scenario/day subtests.
  Includes lab TODO, default case evidence label, technical/reference_label TODO,
  source metadata, missing lab default topic naming, skeleton overwrite/registry,
  exact Day 002 coverage anchors/eight slots and complete Day 002 acceptance.
  Rejection tests assert no Path.write_text call; pre-write guard runs first.
- Compile Day 002 durable spec to override: PASS; generated output unchanged.
- python3 scripts/build.py --day 2 and --day 3: PASS; both byte-identical to
  Phase 0 baselines (no whitespace changes). No full-site or other-day build.
- python3 scripts/validate.py --day 2: PASS, 0 errors.
- Loaded-spec semantic hashes: PASS, exactly Phase C values, using its JSON
  normalization and exclusion of structural lab_defaults metadata:
  Day 002 d5540233f36df205a9d26d56c8b6ccb25c33d33c257dc9c62231f26e8a570cd0;
  Day 003 78a0d0fd7d91c94ead64998e9095a262fa37acd6e34e8d99c6a773b92b768079.
- git diff --check: PASS.

Measured effect: durable Day 002 spec stays 63292 bytes (15823.00 estimated
tokens), and all four instruction sizes stay at Phase C values. This safety fix
adds validation/schema text rather than claiming token savings. Schema expansion
for the requested future-linter rule list is recorded below (bytes/4 estimates).
No explanatory prose, subtopics, examples, labs or other day spec was edited;
no depth change or study-time overrun. Raw SVGs and legacy format remain intact.
No Phase D or later implementation started. Stop after this follow-up commit.

| Follow-up file | Before bytes | After bytes | Estimated token change |
|---|---:|---:|---:|
| scripts/author_engine.py | 61240 | 62503 | 315.75 |
| scripts/new_day_skeleton.py | 4864 | 5212 | 87.00 |
| SPEC_SCHEMA.md | 2996 | 3803 | 201.75 |
| SPEC_DEFAULTS.json | 5801 | 5828 | 6.75 |


## Phase D close-out — tooling only (options 4 and 5)

Approved tooling retained: scripts/compact_flow.py, engine compact-flow routing,
directory-spec loading with the contiguous topic-file check,
new_day_skeleton.py --directory, and tests/test_phase_d.py. No durable day spec
was converted or reauthored. Day 002 keeps its flow_svg helper calls; all other
durable specs, overrides, rendered pages and shared shell remain unchanged.
The canonical diagram quality floor remains in the contract. SPEC_SCHEMA.md now
documents diagram choices and the directory loader/skeleton interface.

| Option | Actual value | Source-size result / limit |
|---|---|---|
| 4 — compact flows | Non-truncating label/detail wrapping, ordered chains of 2–12 nodes, and a numbered transition list | Day 2 helper-based experiment comparator: **63,369 bytes**; compact conversion: **66,024 bytes**, **+2,655 bytes**. NEXT_HOP_FLOW: **2,258 bytes**; NIC_FLOW: **2,415 bytes**. No Day 2 token saving from compact flows. |
| 5 — directory specs | meta.py plus contiguous topic_01.py..topic_0K.py, equivalent loaded data, and --directory skeleton generation | Enables topic-specific source organization/reads; no durable migration and no measured token saving claimed. |

Correction: the earlier compact-flow saving estimate counted rendered output
rather than source. Rendered SVG bytes are not the per-page authoring source cost.
The supplied experiment comparison above is a source increase, not a saving
(+663.75 bytes/4 estimated tokens; actual tokenizer effects unmeasured).
The unchanged on-disk scratch/day_data_002.py is **63,292 bytes**, as recorded in
Phase C; the 63,369-byte experiment comparator is a separate measurement and does
not replace that durable-source baseline. The compact scratch fixture is 66,024
bytes. These experimental fixtures are audit evidence, not adopted day specs.
Compact flows enforce min-width 1120px and horizontal scrolling on mobile.

Visual evidence requiring user review (no visual approval claimed):
- scratch/baseline/diagram-compare/next_hop-before-dark.html
- scratch/baseline/diagram-compare/next_hop-after-dark.html
- scratch/baseline/diagram-compare/next_hop-before-light.html
- scratch/baseline/diagram-compare/next_hop-after-light.html
- scratch/baseline/diagram-compare/nic-before-dark.html
- scratch/baseline/diagram-compare/nic-after-dark.html
- scratch/baseline/diagram-compare/nic-before-light.html
- scratch/baseline/diagram-compare/nic-after-light.html

scratch/phase-d-fixtures.py reproduces the scratch-only compact conversion and
comparison HTML; it was not used to overwrite durable specs or pages. Automated
accessibility/icon/label checks do not prove visual clarity or user approval.

Close-out verification: rebuild Day 002, then Day 003 only; compare both rendered
files byte-for-byte and by SHA-256 with Phase 0 baselines; run validate.py --day 2,
all discovered unit tests including test_phase_d.py, and git diff --check.
Results: both pages byte-identical with unchanged Phase 0 hashes; Day 2 validation
0 errors; all 25 tests PASS (including 7 Phase D tests); git diff --check PASS.
Evidence is recorded in scratch/baseline/phase-d-checks.txt.
No explanatory prose removed, no depth change or study-time overrun, no cloud lab
execution or fresh source-link review. STOP after the Phase D commit; do not start
Phase E.


## Phase E — read-only authored-spec validator (option 6)

Added scripts/validate_spec.py --day N with optional --spec PATH. It uses the
engine's single-file/directory loader and recursive TODO scanner. It never calls
the compiler/build/whole-site validator or parses rendered day pages; Markdown
and SVG fragments from loaded source are inspected in memory only. It prints at
most 30 ERROR lines, one per line as ERROR topic_key field: reason, one summary,
and exit 1 on any error. WARN signals and legacy INFO are separate from errors.

Checks: unfinished values/keys and source metadata; exact coverage topic set,
titles and explicit or engine-derived anchors; exactly eight lab steps, Location/
Expected result/Save markers, recognised environment and code/file-content or
numbered manual body; incident boolean; reachable generic-prose fallback presence;
initial subtopic list and ordered headings with all three relevance labels,
Concrete example and Evidence limit; strong.keyword/strong.side-heading, keywords
outside pre/code and the identical validate.py inline-command pattern; exactly
two Part 1 preview sentences (including part1_html); HTTPS references/source
registry and access date; SVG viewBox/role/title/desc, resolving aria-labelledby,
figcaption, local icon references, compact structure and empty diagram placeholders.
Literal module ACCESS_DATE/SOURCES metadata supplements engine-loaded fields;
unreachable fallback branches do not require unused authored fields.

Rule 10 resolved explicitly by the user: scenario.diagram_enabled is incident-only.
False rejects any incident flow, raw SVG, diagram or icons fields; True requires
incident diagram data. Technical diagrams receive structural checks and a manual
eligibility WARN per topic carrying one (or day-level architecture WARN). Day 2
technical flows with disabled incident flags therefore pass. SPEC_SCHEMA.md records
this decision. PAGE_UPDATE_PROMPT.md runs the validator before author_engine.py;
the contract Read budget has a one-line description. Depth floor wording unchanged.

Depth signals compare each topic's technical text length, subtopic count, lab step
count and total step text length with half the minimum Day 2 range. These WARNs
never fail validation and are not quality thresholds or proof of non-regression.
The validator deliberately cannot establish source relevance, technical accuracy,
complete mapped teaching scope, causal reasoning, actual explanatory depth,
diagram semantic eligibility/visual clarity, icon product correctness, working
lab instructions, or measured cloud behavior. Sentence splitting/command patterns
and marker/heading checks are structural heuristics. Source relevance remains a
manual item in every summary; no new link fetch, visual approval or lab execution
is claimed. Existing compiler/build behavior and legacy compatibility unchanged.

Checks actually run:

- validate_spec.py --day 2: exit 0; **0 errors, 2 technical-diagram eligibility
  WARNs**, on topic-02 and topic-03. No depth WARNs.
- validate_spec.py --day 3: exit 1; **81 existing authored-spec errors, 2 WARNs**.
  Legacy uppercase format explicitly skips generic-fallback-presence checks only;
  all other checks apply. Existing gaps: 3 missing incident booleans, 24 missing
  Location markers, 24 missing Expected result markers, 24 missing Save markers,
  3 missing Concrete example labels, 1 missing source access date, and missing
  strong.keyword/strong.side-heading (1 each). WARNs: topic-02 total stage text
  below the Day 2 reference range and day-level technical diagram eligibility.
  Errors are reported, not silently grandfathered; Day 3 still builds. Its durable
  source is unchanged under the user's explicit scope.
- python3 scripts/build.py --day 2, then --day 3: both **byte-identical to Phase 0**
  (122760 and 153299 bytes, original SHA-256 hashes unchanged).
- python3 scripts/validate.py --day 2: **0 errors**.
- PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v:
  **43 tests PASS**, including 18 new validator tests. In-memory failure fixtures
  cover all ten error classes, scope decision, legacy exemption, depth warnings,
  output cap and no-write guard. Directory loader fixture uses only a temporary
  directory; no tests write days/ or content/.
- git diff --check: PASS. Durable day specs, overrides, rendered pages and shared
  shell unchanged. No explanatory prose removed; no depth change or time overrun.

Evidence: scratch/baseline/phase-e-checks.txt, phase-e-day-002-spec-checks.txt and
phase-e-day-003-spec-checks.txt. Validation/schema/test additions claim no token
saving; they catch structural omissions before expensive compilation/review.
No full-site build or other-day regression build. STOP after the Phase E commit;
Phase F and later not started.

## Two-part Day 4 defect prevention and repair — 2026-10-04

Part A and Part B executed serially. No commit or push. Only the Day 4 durable spec and its generated content/page were authored. The following is appended audit evidence; earlier report prose remains intact.

### Protected snapshot and final comparison

Snapshot taken before instruction/day edits; Day 2 equals the Phase 0 hash. All four final SHA-256 comparisons pass.

```text
86323aef6497c2ec31cf87f9b239f52b04f276532d9294b62610aa5f9c1f584a  days/day-002.html
4579e0ef1f8c07511acbf239c5de8cf7c3a527b94317b0c645102451cf4abaa0  content/day-003-page.html
4579e0ef1f8c07511acbf239c5de8cf7c3a527b94317b0c645102451cf4abaa0  days/day-003.html
77b0aabf62b71bf713f06b295a338e80e0d40b6547388450f9da830b7e894774  scratch/day_data_003.py
```

### Rule/check justification

| Added rule or check | Day 4 defect it prevents |
| --- | --- |
| Practice/Exit verbatim fields; per-lab covers; Practice-to-lab handoff | Day 4 replaced supplied certificate traces and capture annotations with generated exercises; explicit clauses prevent that substitution and retain the worksheet Exit. |
| Three labelled mode parts; version-2 skeleton TODOs; missing-field errors / legacy WARNs | Day 4 claimed multi-version HTTP and TLS-handshake observations although the server speaks HTTP/1.0 and the certificate exercise checks chains and SAN membership. Labels separate those mechanisms without modifying Days 2/3. |
| Stages 1–7 reject || true; external-tool command -v WARNs and Stage 1 checks | Day 4 masked both ping failures and server shutdown failures, and ping had no tool check. Explicit expected-failure branches preserve unexpected failure exit codes. |
| Environment-dependent outputs marked illustrative | Day 4 loopback ping expectations depended on local MTU/kernel behavior; the supplied 1400-byte tunnel is not the local loopback path. |
| Observation-word WARNs in facts/evidence/captions, including embedded figcaption; provenance rule | Day 4 illustrative incident captions said logs were recorded and a packet capture proved the cause, despite no locally produced capture. |
| Address-range WARNs with literal/field; comment-only exception allowlist; reserved-name rule | Day 4 used real public 35.200.10.5, 34.100.1.10 and 34.102.15.20 in examples and non-reserved .local names. Documentation addresses and .test names avoid contacting or attributing evidence to real endpoints. |
| Section URL/fragment rule; whole-document WARNs and reasons | Day 4 broad RFC/product links concealed the specific status-code, header, handshake, MTU, NAT and BGP rules being used. |
| One (accessed YYYY-MM-DD) label pattern; v2 label errors / legacy WARNs | Day 4 mixed undated source labels with separate access sentences; inline, reference and registry label checks keep the access evidence attached to each source. |
| RFC Obsoleted by review; checker status metadata output | Day 4 relied on RFC 6125 without checking its replacement RFC 9525. Review also found RFC 8446 obsoleted by RFC 9846. |
| Status parser uses metadata pairs, not embedded RFC prose; offline regression | During Day 4 live checking, RFC 9293 embedded text falsely looked like an Obsoleted by value for RFC 6298. The corrected parser prevents attributing another RFC’s status to the cited RFC. |
| At-most-300-character heading/first-paragraph excerpts in stdout/JSON; modern, nested, legacy-anchor and h1 tests | Day 4 link success previously showed no opened section text. Excerpts make the actual section auditable, including legacy RFC span headings; they still cannot establish semantic relevance. |
| Source ledger headings and no unsupported verified claims; retained checker limitation/exit codes; no caching | Day 4 had broad links and misleading confidence about logs/product behavior. The ledger distinguishes the checker’s URL/fragment evidence from manual section review; fetch failures remain unverified. |
| Product claims require supporting sections; product-claim handoff | Day 4 invented the Andromeda reason for MTU 1460, hypervisor switch programming, zero-latency/unlimited NAT behavior and timed routing recovery. Section-scoped claims and explicit limits prevent those extrapolations. |
| Coverage publisher hint rule; publisher mismatch WARN; topic-specific completion URLs | Day 4 coverage rows all pointed to RFC 9110 rather than each topic’s primary protocol source. Only its five rows now use confirmed sections and publisher_section_verified=yes. |
| Never silently remove a diagram; preserve/convert/ask rule; Visuals handoff | Day 4 had lost the HTTP versions comparison. A numbered setup/request sequence restores explanatory visual depth without inventing a static qualifying flow. |
| Committed diagram-count comparison and missing-title WARN; unavailable-git skip note | The omitted HTTP comparison could escape normal structural validation. Comparing to HEAD makes future figure losses reviewable without reading current output as curriculum truth. |
| Targeted str_replace/per-topic edit discipline; spec diff stat and no-prose-removal handoff | Day 4’s omitted visual and substituted exercises need visible additions or corrected fragments; a whole-file replacement would obscure depth regressions. |
| Over-100-KB directory-revision WARN | The Day 4 single-file spec already exceeded 100 KB before repair, making large rewrites difficult to review. It stays a single file for this expressly targeted-edit task; the warning directs future revisions. |
| Fail-before-write one-day extractor, robust ## brief / ### roadmap headings and missing/empty tests | Day 4’s brief embeds a nested roadmap heading, while omitted supplied Practice inputs led to incomplete labs. Extraction separates the real heading levels and refuses incomplete canonical inputs. |
| Wrapper command order and version-2 schema/entry-point pointers | Day 4 was authored without explicit verbatim Practice fields or supplied fixtures. Extraction before skeleton/validation makes the canonical input available before generation. |
| Passing/failing in-memory strict-check fixtures; legacy compatibility tests; missing-path reporting fix | Day 4 needs new strict gates while Days 2/3 remain unchanged. Tests exercise all nine requested checks and preserve existing error reporting; the Day 3 test now uses a mutated in-memory marker rather than assuming its intentional update is invalid. |
| Local rerun checks every stage Save path and protocol/model acceptance before cleanup | Day 4 Stage 1 promised preflight.log but wrote preflight.txt; Lab 2 promised openssl_configs.log without creating it. The local wrapper and Stage 2 now create those artifacts. Ping evidence is retained instead of deleted. |
| Matching service icons and explicit control/data-plane diagram captions | Day 4 NAT/routing service nodes used generic firewall/router icons and implied a NAT appliance next hop or undocumented FIB programming. Existing local official Cloud NAT/Router/Interconnect and core Compute Engine icons make those boundaries explicit. |

### Size, depth and edit discipline

Contract: **12,988 → 15,205 bytes**, growth **2,217 bytes**, below about 2.5 KB. Existing contract wording, depth floor and diagram quality floor remain; only the requested manual-grep Read budget passage was replaced.

Day 4 git diff numstat: `290	156	scratch/day_data_004.py` (added / replaced-old lines / path). Spec bytes: **146,200 → 171,845**. Targeted string replacements/additions only; no file recreation, topic removal, lab removal or diagram removal. No explanatory prose was removed or condensed: old lines in the diff are replaced source metadata, corrected unsupported facts, provenance/limits, example addresses, command fixes or additive lab integration.

| Topic | Technical text before → after | Subtopic headings before → after | Lab stages | Stage text before → after |
| --- | --- | --- | --- | --- |
| topic-01 | 10597 → 13061 | 4 → 4 | 8 → 8 | 7309 → 7758 |
| topic-02 | 10863 → 11828 | 4 → 4 | 8 → 8 | 7719 → 9854 |
| topic-03 | 10314 → 11220 | 4 → 4 | 8 → 8 | 6210 → 7739 |
| topic-04 | 10055 → 11219 | 4 → 4 | 8 → 8 | 7379 → 7711 |
| topic-05 | 10778 → 12323 | 4 → 4 | 8 → 8 | 10994 → 13420 |

All scoped subtopics and eight stages per lab remain. Depth increases: supplied trace comparison, supplied MTU/route annotations, HTTP setup sequence, and product ownership/evidence boundaries. No measured learner duration is available; added work may exceed the 2–3-hour estimate and was not trimmed.

### Practice-to-lab map

Practice (verbatim): Compare a valid and a hostname-mismatched certificate trace; annotate an MTU failure and forward/return routes on supplied captures.

Exit (verbatim): A failure worksheet that separates TLS trust, packet size, routing and HTTP errors.

| Lab | Practice/Exit clause and actual artifact |
| --- | --- |
| 1 | Exit HTTP errors: local HTTP/1.0 status artifacts and http_evidence_summary.md; HTTP/2 casing rejection and HTTP/3 are simulations. |
| 2 | Compare valid/hostname-mismatched trace: supplied-valid-trace.txt requests/presents orders.example.test; supplied-mismatch-trace.txt requests orders.example.test/presents admin.example.test; certificate-trace-comparison.md. Generated CA validation is additional local work. |
| 3 | Annotate MTU failure on supplied capture: supplied-mtu-capture.txt names DF=1, length=1500, path MTU=1400 and filtered ICMP; calculations predict base-header MSS 1360. Loopback ping is separate locally produced evidence. |
| 4 | Exit NAT context: local translation/state/capacity model and nat_evidence_summary.md; configured illustrative 64-port allocation, not a universal provider connection limit. |
| 5 | Annotate supplied forward/return capture: 10.20.1.5 → 10.50.4.8 selects 10.50.4.0/24; remote side lacks a covering return route to 10.20.0.0/16. route_engine.py locally simulates this supplied input; day-004-failure-worksheet.md includes TLS, packet-size, route and HTTP distinctions plus NAT context. |

All five labs executed in temporary directories, each with eight non-empty stage Save artifacts checked before cleanup, plus specific status/chain/MTU/NAT/route acceptance checks. No GCP lab deployment was executed. Evidence paths and stdout/stderr are in scratch/day-004-lab-rerun.json; artifacts in /tmp are temporary.

- Lab 1: exit 0; 8 stage checks; acceptance passed; `/tmp/http_lab.3sldZP`.
- Lab 2: exit 0; 8 stage checks; acceptance passed; `/tmp/pki_lab.snAQFp`.
- Lab 3: exit 0; 8 stage checks; acceptance passed; `/tmp/mtu_lab.qQjCBf`.
- Lab 4: exit 0; 8 stage checks; acceptance passed; `/tmp/nat_lab.RQqYfd`.
- Lab 5: exit 0; 8 stage checks; acceptance passed; `/tmp/routing_lab.QdYpNc`.

### Visuals list

- Added/restored: **HTTP Versions: Connection Setup and First Request Sequences**. Three independent 1→2→3→4 rows compare TCP+TLS setup for HTTP/1.1/2 against QUIC+integrated TLS for HTTP/3, then request/response; scope excludes packet timing/early data. Raw 1440×690 SVG, complete labels, local generic icons, title/desc IDs, numbered arrows and horizontal scrolling.

- Retained: **TLS 1.3 1-RTT Handshake: Key Exchange and Certificate Validation** and **Path MTU Discovery and TCP MSS Clamping Packet Traversal**; no explanation or sequence removed.

- Retained/corrected: **VPC Private Outbound: SNAT and Return DNAT Packet Lifecycle**: official Cloud NAT icon, internet-gateway next hop, functional translation caption; prevents an appliance-hop interpretation.

- Retained/corrected: **BGP Route Advertisement, Evaluation, and Packet Forwarding**: official Cloud Router/Interconnect/Compute Engine icons, route-creation transition and control/data-plane limit; removes undocumented internals/latency guarantees.

- Retained/corrected incident figures for topics 01 (HTTP), 02 (TLS), 03 (MTU), 04 (NAT), 05 (routing): fixture provenance captions; routing latency is an illustrative target requiring measurement. All five dual-lane incident diagrams remain.

- Removed: **none**. Whole-figure replacements: **none**. Durable-spec technical figures: 4→5; incident figures: 5→5.

Visual limits: source SVG accessibility attributes and local icons pass spec/structure checks. No browser was exposed by cua.getState (browsers=[]); attempting createBrowserTab(iab) returned “Browser is not available: iab”. Desktop/mobile both-theme rendered audits, overlap/arrow review, copy-button interaction and far-edge reachability therefore remain **unverified**. No browser-audit success is claimed.

### Source ledger

Final checker: **36 passing HTML links, 0 unverified links**; every excerpt ≤300 characters. All Further study links are fragment-level; no whole-document study link needs an exception reason. Access label: `(accessed 2026-10-04)`. Headings below were opened/confirmed from live sections; HTTP/fragment pass alone is not semantic verification.

| URL | Scope | Section heading actually opened |
| --- | --- | --- |
| https://www.rfc-editor.org/rfc/rfc9110.html#section-15 | fragment-level | 15. Status Codes |
| https://docs.cloud.google.com/load-balancing/docs/https#http2-over-tls | fragment-level | HTTP/2 over TLS |
| https://docs.cloud.google.com/load-balancing/docs/https/request-distribution#timeouts_and_retries | fragment-level | Timeouts and retries |
| https://www.rfc-editor.org/rfc/rfc9113.html#section-8.2.1 | fragment-level | 8.2.1. Field Validity |
| https://docs.cloud.google.com/load-balancing/docs/https#backend-service | fragment-level | Backend services |
| https://www.rfc-editor.org/rfc/rfc9114.html#section-3 | fragment-level | 3. Connection Setup and Management |
| https://www.rfc-editor.org/rfc/rfc9114.html#section-4 | fragment-level | 4. Expressing HTTP Semantics in HTTP/3 |
| https://www.rfc-editor.org/rfc/rfc9113.html#section-3.2 | fragment-level | 3.2. Starting HTTP/2 for " https " URIs |
| https://www.rfc-editor.org/rfc/rfc9110.html#section-4.2.2 | fragment-level | 4.2.2. https URI Scheme |
| https://docs.cloud.google.com/load-balancing/docs/https#http3-negotiation | fragment-level | How HTTP/3 is negotiated |
| https://www.rfc-editor.org/rfc/rfc8446.html#section-4 | fragment-level | 4 .  Handshake Protocol |
| https://docs.cloud.google.com/certificate-manager/docs/overview#supported-certificates | fragment-level | Supported TLS certificates |
| https://docs.cloud.google.com/certificate-manager/docs/overview#benefits | fragment-level | Benefits |
| https://www.rfc-editor.org/rfc/rfc5280.html#section-6 | fragment-level | 6 .  Certification Path Validation |
| https://www.rfc-editor.org/rfc/rfc9525.html#section-6 | fragment-level | 6. Verifying Service Identity |
| https://www.rfc-editor.org/rfc/rfc1191.html#section-2 | fragment-level | 2 . Protocol overview |
| https://docs.cloud.google.com/vpc/docs/mtu#valid_mtus | fragment-level | Valid VPC network MTU sizes |
| https://docs.cloud.google.com/vpc/docs/mtu#to-cloudpath | fragment-level | Communication to Google APIs and services |
| https://www.rfc-editor.org/rfc/rfc9293.html#section-3.7.1 | fragment-level | 3.7.1. Maximum Segment Size Option |
| https://docs.cloud.google.com/vpc/docs/mtu#through-cloud-vpn | fragment-level | Communication through Cloud VPN tunnels |
| https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/mtu-considerations#cloud-vpn-payload-mtu-values | fragment-level | Cloud VPN payload MTU values |
| https://www.rfc-editor.org/rfc/rfc3022.html#section-2 | fragment-level | 2 . Overview of traditional NAT |
| https://docs.cloud.google.com/nat/docs/overview#architecture | fragment-level | Architecture |
| https://docs.cloud.google.com/nat/docs/ports-and-addresses#ports | fragment-level | Ports |
| https://docs.cloud.google.com/nat/docs/ports-and-addresses#dynamic-port | fragment-level | Dynamic port allocation |
| https://docs.cloud.google.com/nat/docs/overview#benefits | fragment-level | Benefits |
| https://docs.cloud.google.com/nat/docs/ports-and-addresses#ports-reuse-endpoints | fragment-level | Simultaneous port reuse and endpoint-independent mapping |
| https://docs.cloud.google.com/nat/docs/monitoring#logging | fragment-level | Logging |
| https://www.rfc-editor.org/rfc/rfc1918.html#section-3 | fragment-level | 3 . Private Address Space |
| https://docs.cloud.google.com/nat/docs/monitoring#vm-metrics | fragment-level | VM instance metrics |
| https://docs.cloud.google.com/nat/docs/monitoring#gateway-metrics | fragment-level | NAT gateway metrics |
| https://www.rfc-editor.org/rfc/rfc4271.html#section-3 | fragment-level | 3 .  Summary of Operation |
| https://docs.cloud.google.com/vpc/docs/routes#routeselection | fragment-level | Routing order |
| https://docs.cloud.google.com/vpc/docs/routes#types_of_routes | fragment-level | Route types |
| https://docs.cloud.google.com/network-connectivity/docs/router/concepts/overview#key | fragment-level | Key features |
| https://docs.cloud.google.com/network-connectivity/docs/router/concepts/learned-routes#dynamic-routing-mode | fragment-level | Dynamic routing mode |

RFC 6125 info metadata explicitly says Obsoleted by RFC 9525: hostname matching now cites RFC 9525 §6; RFC 6125 is removed from teaching references. RFC 8446 info metadata says Obsoleted by RFC 9846: the requested roadmap/coverage primary remains historical RFC 8446 §4, with that status in its source label; no claim of current-standard status is made. RFC 9293 has no Obsoleted by metadata value (the corrected parser avoids incidental prose).

Whole-document **status-only** links: rfc-editor.org/info/rfcN, recorded in scratch/day-004-rfc-status-ledger.json; reason: authoritative RFC status metadata is document-wide, not the teaching section. All 22 named RFC/status entries were opened; only 6125→9525 and 8446→9846 have Obsoleted by values. Remaining checked numbers: 1191, 1918, 3022, 4271, 5280, 5880, 6066, 6960, 6996, 7301, 7323, 7541, 9000, 9110, 9112, 9113, 9114, 9293, 9525, 9846.

### Product-claim list and supporting sections

| Product claim / correction | Supporting opened section(s) |
| --- | --- |
| External Application Load Balancer terminates client HTTP/2 with TLS ALPN; HTTP/2 backends need TLS/protocol configuration | [Google Cloud HTTP(S) Load Balancing — HTTP/2 over TLS (accessed 2026-10-04)](https://docs.cloud.google.com/load-balancing/docs/https#http2-over-tls) |
| Client and backend protocol selections can differ; HTTP2 backend protocol uses TLS; no backend protocol fallback promised | [Application Load Balancer — Backend services (accessed 2026-10-04)](https://docs.cloud.google.com/load-balancing/docs/https#backend-service) |
| Backend-service keepalive 600 seconds; backend software must exceed it; Apache/nginx example 620 seconds; backend buckets differ | [External Application Load Balancers — Timeouts and retries (accessed 2026-10-04)](https://docs.cloud.google.com/load-balancing/docs/https/request-distribution#timeouts_and_retries) |
| HTTP/3 is advertised using Alt-Svc and clients can fall back when QUIC/UDP is unavailable; no universal QUIC negotiation promised | [Application Load Balancer — How HTTP/3 is negotiated (accessed 2026-10-04)](https://docs.cloud.google.com/load-balancing/docs/https#http3-negotiation) |
| Certificate Manager manages Google-managed/self-managed certificates; managed issuance/renewal and CA Service pool issuers; no universal 90-day lifetime or chain-completeness promise | [Google Cloud Certificate Manager Overview — Supported TLS certificates (accessed 2026-10-04)](https://docs.cloud.google.com/certificate-manager/docs/overview#supported-certificates) |
| Domain-based certificate selection and DNS/load-balancer authorization; supports lifecycle design, not arbitrary sidecar/mTLS or split-horizon eligibility | [Certificate Manager — Benefits (accessed 2026-10-04)](https://docs.cloud.google.com/certificate-manager/docs/overview#benefits) |
| OCSP stapling/zero-client-lookup is not established by the Certificate Manager cited sections; inspect a real handshake before claiming it | [Google Cloud Certificate Manager Overview — Supported TLS certificates (accessed 2026-10-04)](https://docs.cloud.google.com/certificate-manager/docs/overview#supported-certificates) |
| VPC default MTU 1460, selectable range 1300–8896; base-header IPv4 MSS 1420 is a calculation, not a documented rationale for that default | [Google Cloud VPC Maximum Transmission Unit (MTU) Settings — Valid VPC network MTU sizes (accessed 2026-10-04)](https://docs.cloud.google.com/vpc/docs/mtu#valid_mtus) |
| Google APIs/services have separate path MTU/MSS behavior; no same-VPC Cloud Storage jumbo-throughput guarantee | [VPC MTU — Communication to Google APIs and services (accessed 2026-10-04)](https://docs.cloud.google.com/vpc/docs/mtu#to-cloudpath) |
| Cloud VPN gateway and payload MTUs differ | [VPC MTU — Communication through Cloud VPN tunnels (accessed 2026-10-04)](https://docs.cloud.google.com/vpc/docs/mtu#through-cloud-vpn) |
| VPN payload values depend on cipher, gateway IP version, NAT-T and Interconnect; example 1360 MSS is supplied/configured, not a universal service default | [Cloud VPN — Cloud VPN payload MTU values (accessed 2026-10-04)](https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/mtu-considerations#cloud-vpn-payload-mtu-values) |
| Cloud NAT is distributed managed Andromeda software providing SNAT and response DNAT, not a proxy VM/appliance or NAT route next hop | [Google Cloud NAT Overview — Architecture (accessed 2026-10-04)](https://docs.cloud.google.com/nat/docs/overview#architecture) |
| Cloud Router is the NAT control plane holding configuration; VM external IP reduction is subject to egress rules; no zero-hop latency or infinite-capacity guarantee | [Cloud NAT — Benefits (accessed 2026-10-04)](https://docs.cloud.google.com/nat/docs/overview#benefits) |
| NAT IP offers 64,512 TCP and UDP source ports each; local 64,000 capacity is conservative toy rounding, not a universal connection limit | [Cloud NAT — Ports (accessed 2026-10-04)](https://docs.cloud.google.com/nat/docs/ports-and-addresses#ports) |
| Dynamic allocation has configured minimum/maximum and usage-based growth; Public NAT static vs Private NAT dynamic defaults differ; EIM is incompatible with dynamic allocation | [Cloud NAT — Dynamic port allocation (accessed 2026-10-04)](https://docs.cloud.google.com/nat/docs/ports-and-addresses#dynamic-port) |
| Public NAT EIM reuses mappings across differing destination tuples, subject to its documented conflicts/conditions | [Cloud NAT — Simultaneous port reuse and endpoint-independent mapping (accessed 2026-10-04)](https://docs.cloud.google.com/nat/docs/ports-and-addresses#ports-reuse-endpoints) |
| Configurable NAT connection/error logs go to Cloud Logging; no guarantee of every connection being logged | [Cloud NAT — Logging (accessed 2026-10-04)](https://docs.cloud.google.com/nat/docs/monitoring#logging) |
| compute.googleapis.com/nat/open_connections and dropped_sent_packets_count are VM metrics; OUT_OF_RESOURCES is a drop reason, not observed production data here | [Cloud NAT — VM instance metrics (accessed 2026-10-04)](https://docs.cloud.google.com/nat/docs/monitoring#vm-metrics) |
| router.googleapis.com/nat/nat_allocation_failed is a boolean allocation-failure gauge, not a packet-drop counter | [Cloud NAT — NAT gateway metrics (accessed 2026-10-04)](https://docs.cloud.google.com/nat/docs/monitoring#gateway-metrics) |
| VPC routing is staged; policy/special/subnet/custom rules precede applicable specificity/priority/ECMP decisions; generic LPM model is not full GCP selection | [Google Cloud VPC Routes Overview — Routing order (accessed 2026-10-04)](https://docs.cloud.google.com/vpc/docs/routes#routeselection) |
| Subnet/system/static/dynamic routes have distinct creation, next-hop and applicability rules; no universal production dynamic-routing mandate | [VPC — Route types (accessed 2026-10-04)](https://docs.cloud.google.com/vpc/docs/routes#types_of_routes) |
| Cloud Router manages BGP, learned/advertised routes and BFD support; no documented hypervisor FIB hook, 300-ms detection or fixed restoration guarantee | [Google Cloud Cloud Router Overview — Key features (accessed 2026-10-04)](https://docs.cloud.google.com/network-connectivity/docs/router/concepts/overview#key) |
| Regional/global dynamic mode governs regional learned-route processing and allowable next-hop regions; failover and symmetric return reachability must be checked | [Cloud Router — Dynamic routing mode (accessed 2026-10-04)](https://docs.cloud.google.com/network-connectivity/docs/router/concepts/learned-routes#dynamic-routing-mode) |

Case values (64 ports, 1024 maximum, 4ms/70ms latency, MED/AS-path choices) are supplied illustrative inputs or proposed settings, not defaults, locally measured GCP values or automatic recovery guarantees. 198.51.100.25 is retained because it is in the allowed TEST-NET-2 documentation range. All three real public example literals are replaced; the allowlist contains only its header.

### Final checks and stop boundary

- extract_day_inputs --day 4: passed; final input output includes corrected five coverage rows.

- validate_spec --day 4: 0 errors, 9 WARNs (five diagram manual-review notices, three 0.0.0.0/0 notation notices, one >100-KB revision notice). 0.0.0.0/0 denotes a default route, not a real destination; the requested literal-range checker intentionally reports it.

- validate_spec --day 2: 0 errors, 62 WARNs; original two diagram-review warnings unchanged, additions are new advisory checks. validate_spec --day 3: 0 errors, 49 WARNs; original one diagram-review warning and legacy INFO unchanged, additions are new advisory checks only. No legacy findings were suppressed and no protected spec changed.

- author_engine --day 4, build --day 4, validate --day 4: passed; 0 local link/structure errors. No other day build was requested or run.

- Final uncached check_study_links --day 4: 36 passes, 0 unverified; RFC status values and excerpts in JSON/stdout. Link set unchanged by subsequent caption-only factual corrections; source URLs/labels are the final ones checked.

- All unit tests: 64 pass. Required checker-only unittest discovery: 14 pass. Final labs: five exit 0, all 40 stage artifact checks and specified acceptance checks pass. The temporary runner’s initial NAT assertion expected a reason string that the simulator does not print; corrected to its actual 64 successes / 10 drops / first drop at attempt 65 and dynamic Drops=0.

- Protected SHA-256 comparisons: all four pass. git diff --check passes with core.whitespace including cr-at-eol, preserving coverage.csv’s existing CRLF endings; exactly five CSV rows changed.

- Shared shell/CSS/JS and other day content remain unchanged. Browser rendering checks are unavailable/unverified as disclosed above; structural success is not a visual audit.

Artifacts: scratch/day-004-final-checks.txt, day-004-legacy-validation.txt, day-004-unit-tests.txt, day-004-checker-unit-tests.txt, day-004-study-links.json, day-004-study-links-output.txt, day-004-rfc-status-ledger.json, day-004-lab-rerun.json and protected snapshot/final-check files.

**STOP: no commit or push; no next-day work.**
