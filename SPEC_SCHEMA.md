# Single-file specification schema

Contract first. `scripts/new_day_skeleton.py --day N`: TODO spec from coverage,
no overwrite; `--output`: scratch fixture.
Only structure may be defaulted; all teaching/case/lab text stays topic-specific.
Handoff: separate depth increases/overruns; git diff the spec and state no prose
removed except structure/corrected facts. TODOs are unfinished.

Loader: DAY_DATA, DATA, then legacy variables. Directories unsupported. Legacy DAY/TOPICS/PART1_INTRO…PART4_INTRO/ARCH_DIAGRAM/
ARCH_SVG_HTML (alias ARCH_DIAGRAM_HTML)/ARCH_TABLE_HTML/EXIT_SUMMARY/COMPLETION_HTML
map to lower-case fields. PART1_HTML is NOT collected. Build reads override, not spec; four-part shell needed.

E=escaped; R=Markdown/HTML; H=HTML; ?=engine optional, contract still mandatory.
Exact fallback expressions: SPEC_DEFAULTS.json.

## DATA

day (metadata; CLI N controls build), work_block (unused metadata), topics (list,
default []). part1_html H? replaces Part 1; otherwise part1_intro E and each
topic overview/preview. part2_intro/part3_intro/part4_intro E? have legacy prose
fallbacks. exit_summary E? also appended to completion. completion_html H?
replaces completion body: retain read-N/artifact-N controls. arch_diagram dict
or SVG string? defaults {}; arch_svg_html H? overrides it (arch_diagram_html alias,
default empty); arch_table_html H? defaults empty. sources: ignored author metadata. anchors metadata also ignored.

## topics[]

key/title E required; anchors derive as key-overview/technical/problem/lab and
must exactly match coverage. overview/preview E required unless part1_html;
preview has two Part 1 sentences ONLY. technical R? defaults empty; questions
list[E]? defaults []; reference URL E? empty; reference_label E? generic label.
scenario dict? {}; lab dict? {} (no exercise alias).

## scenario

scenario E? (symptom alias, empty); impact/constraints E? empty; evidence R/H?
empty (leading < is raw); root/verify/residual E unless multiline/fenced, then R,
empty. diagnostic_steps/remediation_steps list[E]? []; fix E/R? empty fallback
when remediation_steps absent. diagram_enabled MUST be bool; absent legacy value
still renders. diagram: five strings, legacy generic fallback. icons: five local
paths? None. facts/inference/expected E? legacy captions. incident_svg_html H?
or svg_html H? override incident; supply accessibility/caption yourself.

## lab

name E? title fallback; goal/expected E? empty; steps list[R]? []: exactly eight,
each with location/actions/expected/save. mode/prereq/preflight E;
verification/trouble/cleanup/accept R; explicit topic text required; new defaults carry TODO. file E via Markdown?
default day-NNN-key.md. No stage dict API: stage helpers return strings.

## sources / diagrams

Sources: author registry key -> (label,URL), access date separate; skeleton
{label,url,accessed} metadata. Embed verified links/dates in text/reference.
Geometry unchanged; raw SVG supported. Geometry defaults: SPEC_DEFAULTS.json.
