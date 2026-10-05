# Spec schema

Contract: only structure defaults, never teaching/case/lab depth.
`scripts/new_day_skeleton.py --day N`: coverage TODO spec, no overwrite;
`--output`: fixture; `--directory`: create a new directory spec without overwrite. Handoff: depth/overruns separate; git diff spec, no explanatory prose removed
(only structure/corrected facts).

E=escaped; R=Markdown/HTML; H=raw HTML; ?=engine optional, contract still required.
Fallbacks/geometry: SPEC_DEFAULTS.json.
Loader: DAY_DATA, DATA, then legacy uppercase DAY/TOPICS/PART1_INTRO..PART4_INTRO/
ARCH_DIAGRAM/ARCH_SVG_HTML (alias ARCH_DIAGRAM_HTML)/ARCH_TABLE_HTML/EXIT_SUMMARY/
COMPLETION_HTML. PART1_HTML is not collected. Directory specs use meta.py (DATA without topics) and contiguous topic_01.py..topic_0K.py
(each exporting TOPIC); the default loader prefers scratch/day_data_NNN/ when present.
Build reads override, not spec; existing shell needs four parts/completion.

## DATA

- day/work_block: metadata; CLI N controls build. topics: list, default [].
- part1_html H? replaces Part 1; otherwise part1_intro E and overview/preview.
- part2_intro/part3_intro/part4_intro E?: legacy prose fallbacks.
- exit_summary E?: legacy prose fallback, appended to completion.
- completion_html H?: replaces completion; retain read-N/artifact-N controls.
- arch_diagram dict/SVG? {}; arch_svg_html H? overrides it; arch_diagram_html
  alias, empty. arch_table_html H? empty.
- lab_defaults dict?: TODO slots, explicit lab fields win; absent preserves
  legacy omissions. Every spec TODO rejected before writes; errors name topic/field.
- sources/access_date and per-topic anchors: author metadata, scanned for TODOs.

## topics[]

key/title E required; anchors key-overview/technical/problem/lab MUST match
coverage. overview/preview E required unless part1_html; preview is two Part 1
sentences ONLY. technical R? empty; questions list[E]? []; reference URL E?
empty; reference_label E? generic. scenario/lab dict? {}; no exercise alias.

## scenario

scenario E? (symptom alias), impact/constraints E?: empty. evidence R/H? empty
(leading < raw). root/verify/residual E unless multiline/fenced, then R, empty.
diagnostic_steps/remediation_steps list[E]? []; fix E/R? empty when no remediation
steps. diagram_enabled: required bool, absent legacy still renders. diagram:
five strings, generic legacy fallback. icons: five local paths? None.
facts/inference/expected E?: legacy captions. incident_svg_html H? or svg_html H?
override; author accessibility/caption.

## lab

name E? title; goal/expected E? empty; steps list[R]? []: eight strings with
location/actions/expected/save. mode/prereq/preflight E;
verification/trouble/cleanup/accept R: new TODO defaults, explicit topic content
required; legacy omissions unchanged. file: Markdown filename? day-NNN-key.md.
All lab TODOs, including stages, rejected. No stage-dict API.


## Diagrams

- `scratch.day_helpers.flow_svg`: fixed six nodes, no label wrapping; source-compact.
- Compact flow: any ordered chain of 2–12 nodes, non-truncating label/detail wrapping
  and a numbered transition list; larger source. Use when labels or details are long
  or the chain is not six nodes. Enforces `min-width:1120px`, with horizontal scroll
  on mobile; bounded layouts reject content that cannot fit rather than truncate.
- Raw SVG: branches or layouts neither helper supports; retain contract accessibility,
  icons, complete labels, transition explanations and evidence captions.

Compact flow fields: title/caption, optional desc, nodes[] with unique id/label/local
icon and optional detail (string or list), and steps[] with from/to/label matching
adjacent nodes. Route via topic.flow, scenario.flow (subject to diagram_enabled and
raw SVG precedence), or arch_diagram.flow/direct nodes+steps. Eligibility and diagram
quality rules still apply; tooling availability does not approve a conversion.

## sources/helpers

Skeleton emits SOURCES={key: (label,URL)} and ACCESS_DATE, also included in DATA
as sources/access_date for scanning. Reference is TODO: verify + publisher URL;
lab.file is prefilled day-NNN-key.md. Verify links/dates; teaching stays TODO. Geometry unchanged, raw SVG allowed.
scratch.day_helpers assembles explicit context via partial; missing context TODO,
not teaching. Legacy files unchanged. Empty lab_defaults opts in to engine slots;
Whole loaded spec, including metadata, must be TODO-free.


## Fallbacks that count as generic prose

Phase E rule list from SPEC_DEFAULTS.json (legacy behavior unchanged):

- data.part1_intro, part2_intro, part3_intro, part4_intro, exit_summary.
- topic.title (Topic/this topic), t.reference_label.
- scenario.diagram, facts, inference, expected.
- lab.mode, prereq, preflight, trouble, cleanup.
- arch_diagram.title, desc, caption, nodes (both diagram renderers).

These non-empty prose/label fallbacks require authored context; lab TODO slots
are unfinished placeholders, not acceptable prose. Structural lab.file defaults
and colors/dimensions are not teaching prose.


## Read-only spec validation (Phase E)

`python3 scripts/validate_spec.py --day N [--spec PATH]` uses the engine file/directory
loader, checks authored structure before compilation, and never builds or traverses
rendered pages. It emits at most 30 ERROR lines and one summary; any error exits 1.
It checks TODOs, coverage keys/titles/explicit or engine-derived anchors, eight lab
steps with environment/markers and code or numbered manual bodies, incident diagram
booleans, reachable generic-prose fallback slots, subtopic lists/headings/labels,
examples/evidence limits, keyword/side-heading markup and inline commands, Part 1
previews (including part1_html), HTTPS source metadata/access date, SVG attributes
and compact icon existence. ACCESS_DATE/SOURCES literal module metadata supplements
engine-loaded fields when the loader omits it. Legacy uppercase modules skip only
fallback-presence checks, with an INFO line; other errors remain errors, and the
existing compiler remains compatible. Unreachable fallback branches (raw/compact
SVG overrides, disabled incidents, replaced Part 1/completion) require no unused
fallback fields.

scenario.diagram_enabled controls incident diagrams per the contract; False
rejects any incident flow/SVG/diagram/icons fields; True requires incident diagram
data. Technical SVGs are separately eligible and emit a manual eligibility WARN.
Their structural checks cover resolvable title/desc IDs, figcaptions, local icon
references and empty wrappers/headings/placeholders, as well as viewBox and role.
This interpretation preserves the required passing Day 2 case, whose technical
flows occur on topics with disabled incident diagrams.
Depth WARNs use per-topic min/max ranges derived at runtime from the canonical
`scratch/day_data_004.py` (five topics, read-only; no rendered HTML baseline).
Metrics are technical plain-text character length, subtopic heading count, lab
stage count, and total stage plain-text character length per topic. The initial
Day 4 ranges are 11,219–13,061 characters, 4–4 headings, 8–8 stages, and
7,711–13,420 stage characters. Values below half the corresponding minimum
warn; values above the maximum are allowed. This stays warn-only and never fails
on length. `depth_ranges()` recomputes the ranges if the canonical spec changes. These are
signals, not quality thresholds or proof of depth non-regression. Source relevance,
technical accuracy, semantic diagram eligibility, visual clarity, lab executability
and actual depth require manual review; syntax markers cannot establish them.

## Contract version 2 checks

DATA.contract_version = 2 opts into errors for missing non-empty verbatim
roadmap_practice/roadmap_exit, per-lab covers (Practice clause), each mode label
(Observed locally:, Simulated or predicted:, Untested on GCP:), Stage 1–7 code
failure masking, and source labels without `(accessed YYYY-MM-DD)`.
Older specs receive WARNs for these new requirements and keep legacy validation.
External-tool preflight, observation provenance, example address ranges,
whole-document URLs, coverage publisher hints, committed diagram count and files
over 100 KB are review WARNs. Git comparison unavailable emits a skip note.
Use directory form for large revisions. Checks never establish semantic relevance.

## Generated handoff review metadata

Optional `DATA.review_records` is the canonical home for review evidence consumed
by `scripts/write_handoff.py --day N`. It emits `scratch/handoffs/day-NNN.md`
from the loaded spec and git HEAD, with Practice clauses/lab covers, source URLs
and fragments, product-claim candidates, visual additions/removals/replacements
and their reasons, and the actual spec diff stat. Missing evidence is marked
UNRECORDED; labels and HTTP success never establish that a heading was opened.

- `source_ledger`: dictionary keyed by exact URL; each value has
  `heading_opened`, `rfc_status` (for RFCs), `whole_document_reason` (when no fragment).
- `product_claims`: list of reviewed records, each with `claim`, `section_url`
  and `heading_opened`; GCP relevance paragraphs are additionally extracted as
  candidates, with their inline links and GCP section citations from the enclosing
  subtopic, without claiming that support was reviewed.
- `visual_reasons`: dictionary keyed by SVG title, explaining each change.

The generator reports removed source lines without asserting that removed prose
was non-explanatory. Untracked specs and unavailable git baselines stay explicit.

## Batch execution gates

`run_labs.py --day N [--spec PATH] [--timeout SECONDS]` loads the durable spec
and extracts every stage's shell code blocks using the same Markdown renderer
as the compiler. Each lab has an isolated temp workspace, persistent Bash state,
a per-lab timeout and process-group cleanup. Absolute /tmp mktemp templates are
redirected under that workspace. Save files are checked immediately after each
stage, before later authored cleanup can delete them, and hashes are recorded in
`scratch/day-NNN-lab-rerun.json`. Missing tools (including optional command -v
checks) identify their stage and produce SKIPPED, never PASS. Manual/cloud stages
and non-shell code blocks are SKIPPED rather than inferred or deployed. Save
records need explicit filenames; absent/unresolvable paths fail. Authored shell
commands execute with the current user's privileges; the temp workspace is not
a security sandbox.

`batch_gate.py --day N [--contract-hash]` runs extract_day_inputs, validate_spec,
validate, check_study_links and run_labs in that exact order, stopping at the
first failure. It rejects missing/stale reports, unverified links/RFC status,
SKIPPED tools/stages and diagram-count WARNs; depth remains warn-only.
`--contract-hash` creates `scratch/batch-contract.sha256` exclusively on first
run and rejects subsequent contract changes without overwriting the pin.
