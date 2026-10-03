# Spec schema

Contract: only structure defaults, never teaching/case/lab depth.
`scripts/new_day_skeleton.py --day N`: coverage TODO spec, no overwrite;
`--output`: fixture. Handoff: depth/overruns separate; git diff spec, no explanatory prose removed
(only structure/corrected facts).

E=escaped; R=Markdown/HTML; H=raw HTML; ?=engine optional, contract still required.
Fallbacks/geometry: SPEC_DEFAULTS.json.
Loader: DAY_DATA, DATA, then legacy uppercase DAY/TOPICS/PART1_INTRO..PART4_INTRO/
ARCH_DIAGRAM/ARCH_SVG_HTML (alias ARCH_DIAGRAM_HTML)/ARCH_TABLE_HTML/EXIT_SUMMARY/
COMPLETION_HTML. PART1_HTML is not collected. No directories yet. Build reads
override, not spec; existing shell needs four parts/completion.

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
