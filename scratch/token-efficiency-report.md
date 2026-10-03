# Token-efficiency report — Phase 0 and Phase A only

## Scope and commits

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

The request associates Phase A with options 8, 9, 1 and 2 but does not supply
separate labels for the other numbers. This table accounts for all ten without
inventing implementation claims or starting deferred phases. Shared file savings
are not double-counted across overlapping options.

| Option | What changed / why | Files | Measured effect |
|---|---|---|---|
| 1 | Bounded day-input Read budget; avoid full catalogs/unrelated pages | Contract, three wrappers, render procedure | Read volume not benchmarked; contributes to aggregate bytes reduction |
| 2 | Static rules first; avoid routine generated-page/engine/template reads; forward schema reference | Same instruction files | Stable prefix established; provider cache benefit unmeasured |
| 3 | Not executed; no independent label supplied in scoped request | None | 0; B–G deferred |
| 4 | Not executed; no independent label supplied in scoped request | None | 0; B–G deferred |
| 5 | Not executed; no independent label supplied in scoped request | None | 0; B–G deferred |
| 6 | Not executed; no independent label supplied in scoped request | None | 0; B–G deferred |
| 7 | Not executed; no independent label supplied in scoped request | None | 0; B–G deferred |
| 8 | One canonical contract; short unique wrappers; duplicate rules moved | Four instructions, render procedure | Per-file table and aggregate above |
| 9 | Resolve four contradictions, record superseded policies, map requirements | Contract, wrappers, render procedure, traceability | 109 original lines mapped; 0 unmapped; rendered diffs empty |
| 10 | Not executed; no independent label supplied in scoped request | None | 0; B–G deferred |

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

## Deliberately unchanged and limitations

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
