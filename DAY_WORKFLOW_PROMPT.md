# Complete per-day curriculum workflow prompt

This is the canonical operational prompt for one isolated day. Edit only the
configuration block. In a batch, the coordinator fills `DAY` for each day and
uses the shared switches from `BATCH_UPDATE_PROMPT.md`; every other instruction
below applies unchanged.

```text
DAY=
SCOPE=                 (plan | update | audit-only | fix)
DIAGRAMS=allow         (keep | allow)
TOPICS=expand          (keep | expand | add)
EXTRA_TOPICS=          (only with TOPICS=add; one per line as "title | one-line reason")
IMPROVEMENTS:
- keywords:
```

Every other reference uses `DAY`, `NNN` (DAY zero-padded to three digits),
`BRANCH`, or these switches.

## Step 0: resolve and confirm

- Require integer `DAY` from 1 through 180; derive `NNN` and `BRANCH=day-NNN`.
- Print exactly `Day DAY | NNN | branch BRANCH | SCOPE=<value> DIAGRAMS=<value>
  TOPICS=<value>`, then the `EXTRA_TOPICS` list or `none` and the `IMPROVEMENTS`
  list or `none`. Use only these values. If a file, command or message names a
  different day, stop and report it.
- Stop when `EXTRA_TOPICS` is nonempty without `TOPICS=add`, or `TOPICS=add` has
  no entries. Each entry must be `title | one-line reason`.
- If DAY is a roadmap gate/capstone whose entry does not fit the four-topic
  template, stop and explain why.
- With `DIAGRAMS=allow`, if `scripts/compact_hierarchy.py` is absent, author only
  flow diagrams and list needed hierarchies under `Diagram recommendations`.

## Standing page requirements

These formatting rules apply to every authored, updated or fixed page regardless
of `TOPICS`; every audit checks them.

### R1 — linked subtopics

In each `topic-XX-overview` card, immediately after Problem preview, add one
`<strong class="side-heading">Linked subtopics:</strong>` followed by a `<ul>`
whose items link to every `#topic-XX-subtopic-Y`. The technical discussion's
opening `Subtopics in this discussion:` list links the same anchors. Never copy
another day's markup, duplicate an existing list, or leave a dangling target.
Add missing heading IDs through the durable spec key that generates them.

### R2 — labelled bullets

Each technical subtopic renders its labelled explanations as bullets, one
`<li><strong class="side-heading">Label:</strong> text</li>` per existing label.
Read labels from the spec; never invent them. Paragraph-to-list conversion may
change only markup: normalized wording, links and order remain identical.

### R3 — keyword discovery links

Link the first occurrence per technical subtopic or overview card of every
`strong.keyword` term, every `keywords:` IMPROVEMENTS term, every term in
`scratch/audits/day-NNN-terms.txt`, and every architectural/technical term a
learner would search. Use exactly:

`<a href="http://www.google.com/search?q=TERM" rel="noopener" target="_blank">TERM</a>`

Preserve displayed wording; replace spaces in the query with `+` and percent-
encode other special characters; match case-insensitively. Never link inside a
heading, `kbd`, `code`, `figcaption` or existing link. Put the anchor inside a
`strong.keyword` span when applicable. Keep the end-of-discussion `Keyword
searches` list and label every item `discovery aid`. Discovery links are not
sources: exclude them from the source ledger, product claims and unverified-link
gate.

### R4 — diagram collision clearance

No SVG text overlaps an icon, other text, a node border (4px inner margin), or
the viewBox edge. Report clearances within 6px as `borderline`.

### R5 — shared width

Technical-discussion width comes from `assets/site.css`. Never add an inline
`<style>` override for container width, layout, fonts or palette, a style
attribute that overrides the technical/container width, or a per-day width rule.
Never edit shared scripts/templates for a page. The checker verifies the shared
stylesheet link and width overrides; this rule is gated.

### R6 — built-page verification

After building, run R9 against `days/day-NNN.html`, not only the spec. Each
failure records the generating spec key. A diagram that cannot be measured
because it uses transforms other than `translate` is listed under `Not checked`.

### R7 — no leaked Markdown

Rendered prose contains no literal list markers inside paragraphs or at line
starts, `**`, backticks, or `#` headings. Convert them in the spec to semantic
HTML without changing wording: lists to `<ul><li>`, bold to `<strong>`, and
backticks to the page's matching `<samp>` or `<code>`. A list marker inside an
existing `<li>` is split into separate list items. R7 is critical and gated.

### R8 — diagram text size

No SVG text is below 9 viewBox units. Raise small labels and wrap or resize the
node; never shrink other text to compensate.

### R9 — deterministic checker

Audit, fix gate and update gate run:

`python3 scripts/check_page_rules.py --day DAY --diagrams <DIAGRAMS> --terms-file scratch/audits/day-NNN-terms.txt --json scratch/day-NNN-rules.json`

The checker runs on the built page and checks R1–R5, R7 and R8. Exit 1 is a
gated failure. Paste every per-rule line and the per-diagram measurement table
into the handoff. Do not reimplement it or claim a pass without its counts. If
the script is missing or crashes, stop. Record its measurement method,
not-measured diagrams and advisory terms. Every FAIL becomes a finding: R1, R2,
R3 and R7 are critical; R4, R5 and R8 are major.

## Scope rules

### SCOPE=plan

Change no files; create no branch or commit. Run `extract_day_inputs.py --day
DAY`, then report: existing topics and their subtopics/diagrams (title, flow or
hierarchy, eligibility); proposed expansions with the exact Day DAY Study clause;
EXTRA_TOPICS with their clause or `outside roadmap scope`; proposed hierarchies
with levels, relationship per level and informed decision; learner-time impact;
and R9 output when the built page exists. Stop and wait for `SCOPE=update`.

### SCOPE=audit-only

Create no branch or commit and change no content. The only writable files are:

- `scratch/audits/day-NNN-audit.json`
- `scratch/audits/day-NNN-terms.txt`
- `scratch/day-NNN-rules.json`
- `scratch/day-NNN-lab-rerun.json`

Read the contract once and the spec once via `extract_day_inputs.py`. Do not load
the generated override or rendered page into context; use checker output and open
only a specifically flagged region. Run `validate_spec.py`, `validate.py`,
`check_study_links.py`, `run_labs.py`, and R9 with IMPROVEMENTS keywords. Report
every failure instance. Review advisory terms, write the meaningful improvement,
advisory and lowercase searchable terms one per line to the terms file, and rerun
R9.

Audit four areas:

- content: facts, technical accuracy, roadmap drift, source/product support,
  depth floor, and every validator warning;
- diagrams: R4/R8, technical accuracy, geometry, color, accessibility and
  eligibility; record an ineligible existing diagram as `decision needed`, not a
  replacement defect;
- scenarios: plausibility, consistent timeline, `Evidence limit:`, and no
  invented product claims;
- exercises: exactly eight stages, correct commands/expected output, no skipped
  tool, and roadmap Practice mapping.

Severity is critical for misrendering, R1/R2/R3/R7, factual or lab errors; major
for R4/R5/R8 and contract-floor gaps; otherwise minor. Sort by severity and cover
critical areas first.

Write the audit ledger with the durable-spec hash, summary, R3 term list and
findings. Every finding has ID `F1...`, kind (`defect` or `enhancement`), area,
severity, class/type, location, justifying rule, and status `open`. A defect has
an exact `old_str` matching once and `new_str`. An enhancement has an
`anchor_str` matching once, full drafted insertion, exact Day DAY Study clause,
and learner-time delta. Reject anything without a same-day Study clause as
`outside roadmap scope`.

Print `Planned changes`: every finding table; coverage of every IMPROVEMENTS
line; counts by area/kind; files a fix would touch; findings remaining open;
total learner-time impact; R9 output; and a complete `Not checked` list. Never
imply unchecked work passed. State that browser audits were not run unless used.
Then stop.

### SCOPE=fix

Read only the audit ledger and terms file; do not extract inputs or re-audit. Stop
if no open finding exists, the durable-spec hash differs, or any open finding's
`old_str`/`anchor_str` does not match exactly once. Report only failing findings.
Otherwise print open findings (ID, severity, kind, area, location and one-line
change) plus touched files, then stop for explicit `go`, `go defects`, `go
enhancements`, or `go F1,F3`. Make no changes or branch before approval.

After approval, run branch preflight, apply only selected ledger text with
targeted `str_replace` edits, correcting each selected defect class everywhere
on the page in the same pass. Run Work steps 4–5 and the gate, then mark applied
findings `fixed` and commit/push. Diagram findings remain open unless
`DIAGRAMS=allow`; `topic N` enhancements remain open unless `TOPICS=expand`.

### SCOPE=update

Author or update the page using every standing rule, switch and Work step below.

## Diagram and topic switches

### DIAGRAMS=keep

Do not add, remove, alter or replace diagrams. List R4 collisions, R8 small text,
ineligible diagrams and other recommendations as unresolved in the handoff; R4
and R8 are reported but not gated.

### DIAGRAMS=allow

Add or change only eligible diagrams:

- `flow`: an actual multi-step sequence, packet traversal, or request/response
  lifecycle;
- `hierarchy`: parent-child, containment, inheritance or scope with at least two
  levels, a labelled relationship per level, and adjacent prose explaining every
  level, direction and informed decision.

Flat lists, matrices, definitions and classifications use tables. Never invent a
qualifying flow. Leave an ineligible existing diagram in place and recommend a
decision unless it can truthfully become a qualifying sequence; if eligibility
and depth conflict, keep it and ask. Never use default/filler nodes or silently
remove a visual. Record every addition/removal/replacement and justification in
Visuals. Correct a diagram defect class everywhere on the page in one pass.

Changed diagrams must have technically exact syscalls/protocol/persistence and
network stages; arrows from clean outer edges with uniform box gaps, grid spacing
and alignment; no R4/R8 defects; at most one header icon; node-centered text;
minimum 9px text; non-fault colors for normal stages; accurate legend; meaning
without color alone; viewBox, role=img, unique title/desc, aria-labelledby,
scroll wrapper, and scope-bounded figcaption.

### TOPICS=keep

Add no topic or subtopic. Correct and complete existing scope; standing rules
still apply.

### TOPICS=expand

Add subtopics, worked mechanisms and `topic N` improvements only inside existing
topics and only from Day DAY Study scope, never later days. Record every addition
and clause under Expansions. Use targeted insertions; do not condense/reorder
existing prose except exact-wording R2/R7 markup conversions.

### TOPICS=add

Add only EXTRA_TOPICS after confirming none duplicates the next five roadmap
days; stop and name a duplicate day. Each added topic has the three Part 1 labels
(two-sentence Problem preview), linked subtopics and complete technical discussion
with three labels, concrete example and Evidence limit, one incident, one exact
eight-stage lab, and sources. Add `coverage.csv` rows using the next topic key and
same-day anchor pattern; copy source IDs from the closest same-day topic and never
change the global source-ID set, roadmap Practice or roadmap Exit. Mark the topic
user-added and record that the roadmap lists fewer topics and needs updating.

## Branch preflight

For update/fix only, before any edit:

1. `git fetch --all --prune`; main is `main`.
2. Require a clean `git status --porcelain` except this day's four audit files.
   Otherwise stop and list paths; never repair by force.
3. Require every local branch to have an upstream and not be ahead, using
   `git for-each-ref refs/heads --format='%(refname:short) %(upstream:short)
   %(upstream:track)'`.
4. Require `git branch --no-merged origin/main` and `git branch -r --no-merged
   origin/main` to be empty except origin/HEAD and origin/main. Report possible
   squash/rebase false positives for user confirmation; do not guess.
5. `git switch main`; `git pull --ff-only origin main`; require local main equals
   origin/main. Never push main.
6. Stop if BRANCH exists locally or remotely.
7. `git switch -c BRANCH` from updated main.

Print one result per check and the main commit hash.

## Work

For update, run all steps; fix runs steps 4–5 after approved ledger edits.

1. Read the entire contract once.
2. Follow `PAGE_UPDATE_PROMPT.md` within its read budget. Run
   `extract_day_inputs.py --day DAY`. Targeted-edit an existing spec; otherwise
   create the skeleton and fill every TODO. Set contract version 2 and copy
   roadmap Practice/Exit verbatim. Report legacy migration requirements before
   editing.
3. Apply R1–R5, R7–R8 and all switches to every topic.
4. In PAGE_UPDATE_PROMPT order run `validate_spec.py`, `author_engine.py`,
   `build.py`, `validate.py`, `check_study_links.py`, `run_labs.py`, and
   `batch_gate.py`, all scoped to DAY.
5. Run R9 and capture every rule line plus the per-diagram table.
6. Write `scratch/handoffs/day-NNN.md` with applied finding IDs, R9 output,
   Practice-to-lab map, source ledger with opened headings, product claims and
   supporting sections, Visuals and unresolved collisions, Expansions,
   user-added topics, discovery links, spec diff stat, and learner-time impact.
   Do not paste page HTML.

## Gate before commit

Continue only when preflight passed; validators and batch gate pass; no lab tool
was skipped; every non-discovery link is verified; no TODO remains; every removed
diagram has a handoff reason; R9 passes its gated rules; converted paragraphs
retain normalized text; no other prose was condensed/reordered; no shared script
or template changed; and every Day DAY coverage anchor exists in the built page.
On any failure, do not commit or push; report the first failing check and stop.

## Commit and push

After the gate, run `git add .`, then require every staged path to be one of this
day's spec/directory, generated override/page, study-link/lab/handoff/rule/audit/
term evidence, or `data/coverage.csv` with only Day DAY rows changed. If anything
else is staged, `git reset`, report it and stop. Print the staged stat. Commit
`Day DAY: <roadmap title>`. Re-run pushed/merged checks for branches other than
BRANCH, then `git push -u origin BRANCH`. Never push main or force-push.

## Finish

Print checks/results, preflight and main hash, R1–R5/R7/R8 output, spec size,
depth overruns, expansions, added topics, visual changes, fragment versus whole-
document sources, unresolved items, commit hash and branch. State that browser
audits were not run unless actually used. Then stop.
