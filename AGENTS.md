# GCP 180-day curriculum site

`PAGE_AUTHORING_CONTRACT.md` is the single canonical rule file. Read its static
rules once before day-specific inputs. Its Source precedence and Read budget
apply to every curriculum task; do not infer requirements from existing HTML.

Use `ONE_DAY_AT_A_TIME.md` to select/run one day serially and
`PAGE_UPDATE_PROMPT.md` for commands and concise handoff without reducing depth. Apply the contract to
every future update; all teaching, evidence, structure, typography, SVG/icon,
exercise, source and rendering requirements remain mandatory.

Author only the durable specification. Preserve the shared site shell and mapped
curriculum scope. Repair target-introduced errors before proceeding. Never edit
multiple day pages concurrently or use batch page generation.

For workflow maintenance, follow the user's named phases and stop boundary.
Do not reauthor day content while reducing instruction overhead. Any ambiguity
or requirement with no canonical home must be resolved explicitly, not silently
substituted. The traceability/report files are audit evidence, not routine
per-page reading material.

Run `scripts/extract_day_inputs.py --day N` before day-specific reading; use its
compact output. New specs use contract version 2; follow the update prompt
command order and fidelity/source/product/visual/spec-diff handoff records.

## Standing page rules

These rules apply to every day update. `scripts/check_page_rules.py` remains the
deterministic built-page verifier; do not weaken or bypass it.

- **R1 — linked subtopics:** every overview card links to every technical
  subtopic, and every listed technical subtopic links to its unique heading ID.
- **R2 — semantic bullets:** labelled subtopic points use real list markup, not
  side-heading paragraphs that merely look like bullets.
- **R3 — first-use discovery links:** selected terms and every
  `strong.keyword` use the exact first-occurrence Google discovery-link form
  required by the checker; a day terms file adds mandatory terms.
- **R4 — diagram geometry:** no SVG label may collide with a node, icon, badge,
  arrow, or viewBox boundary. This is gated when `DIAGRAMS=allow`.
- **R5 — full width:** the technical discussion must use the shared wide page
  container without a per-day width override. The per-day rule treats this as
  required, while the current checker reports it but never gates it; preserve
  that unresolved conflict in handoffs rather than claiming a pass.
- **R6 — evidence limits:** every scenario distinguishes supplied facts,
  inference, expected behavior, and an explicit `Evidence limit:`; never turn a
  tabletop or expected result into observed evidence.
- **R7 — no leaked markup:** convert visible Markdown/HTML markers to semantic
  HTML without changing their normalized text.
- **R8 — readable diagram text:** SVG labels are at least 9px and remain
  readable without clipping. This is gated when `DIAGRAMS=allow`.
- **R9 — verify the built page:** run `check_page_rules.py` against the actual
  rendered day with the selected diagram mode and day terms file. A passing
  source spec is not a substitute for this result.

R1, R2, R3, and R7 are always gated. R4 and R8 are gated only when diagrams may
change. R5 remains the documented checker/prompt decision conflict.

## Day prompt switches

`PROMPT_DAY.md` contains only these inputs; resolve them before authoring:

- `DAY`: required integer 1–180; work on this day only.
- `SCOPE`: `plan`, `update`, or `fix`; `update` permits additive authoring and
  the contract-approved R2/R7 conversions, while `fix` is limited to named
  defects and `plan` makes no day-content changes.
- `DIAGRAMS`: `keep` preserves eligible diagrams; `allow` permits contract-
  compliant additions or repairs and gates R4/R8.
- `TOPICS`: `keep` preserves mapped topic/subtopic scope; `expand` may add only
  same-day Study clauses and may not import later-day content.
- `EXTRA_TOPICS`: empty unless the user names same-day roadmap topics; never a
  license to invent or reorder curriculum scope.
- `IMPROVEMENTS`: optional named fixes; empty means apply the standing rules and
  contract without speculative extras.

Run `scripts/day_run.py` in the order `resolve`, `preflight`, `check`, `gate`,
then `commit`. Stop at the first failure. `--skip-labs` is allowed only when a
lab needs unavailable cloud access or tooling, and the exact skipped labs and
reason must be reported. The script masks credential-shaped subprocess output;
never print remote URLs or secret-bearing environment values yourself.
