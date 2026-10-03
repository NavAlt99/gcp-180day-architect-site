# Token-efficiency report — Phases 0, A, B, C and D

Latest status: Phase D closed out as tooling only; Phase E and later remain deferred.
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
