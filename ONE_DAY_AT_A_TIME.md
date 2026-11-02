# One day at a time

Apply `PAGE_AUTHORING_CONTRACT.md` once as the static rule prefix, then select
the compact day inputs using its Read budget. Use `DAY_WORKFLOW_PROMPT.md` for
the complete worker workflow and `PAGE_UPDATE_PROMPT.md` for its command sequence
and handoff; do not duplicate the contract into each task.

## Serial run selection

- Set CURRENT_DAY to the requested numeric day; for a single page,
  TARGET_DAY = CURRENT_DAY. An explicit day starts there; a later `next`
  advances one. Stop after Day 180.
- An explicitly authorized multi-day run has a start/end and uses
  `BATCH_UPDATE_PROMPT.md`. One user invocation is enough for the authorized
  range. The coordinator divides it into windows of 10 days by default; this is
  a checkpoint/recovery boundary, not a shared authoring context.
- Use one fresh, isolated page agent/context per day, strictly serially: finish
  the commands, acceptance checks and handoff for N before N+1. Never generate
  several pages in one context or edit two concurrently. Continue across window
  boundaries without asking the user to repeat the prompt unless a stop
  condition is reached.
- Give each page agent only its compact brief and the canonical static rules.
  For ten days use ten isolated contexts; the coordinator retains only the
  authorized range, current window/day, gate result and commit ID, not catalogs,
  durable specs, page prose or long worker summaries.

## Batch window policy

- Default `BATCH_SIZE=10`. A larger authorized range is processed as consecutive
  10-day windows under the same invocation. A smaller final window is normal.
- Batch size controls checkpoint frequency only. It never permits more than one
  active day, reuse of a page context, cross-day copy/paste, deferred gates, or a
  combined commit.
- At each window boundary, record a compact manifest of day, PASS/FAIL, handoff
  path and commit ID when applicable. Continue automatically after a fully
  passing window. Stop on the first failed gate, changed contract hash, unresolved
  source/lab/diagram issue, user stop boundary, or end of the authorized range.
- Resume from the first incomplete day with a fresh context; never rerun a
  completed PASS day unless the user requests it or its inputs changed.

## Per-day preparation

Extract the day entry/brief and coverage rows; read the durable spec if present.
If the brief is stale, regenerate with `python3 ../generate-day-prompts.py` from
the site directory, then extract only the requested brief. Apply the contract's
precedence/read policy to stale or alternate prompts. Author the durable source,
run the update prompt's commands, repair introduced failures, and hand off before
advancing. Do not run a full-site build.

Run `scripts/extract_day_inputs.py --day N` before day-specific reading; use its
compact output. New specs use contract version 2; follow the update prompt
command order and fidelity/source/product/visual/spec-diff handoff records.

## Batch safety boundary

For explicitly authorized batches, run `python3 scripts/batch_gate.py --day N
--contract-hash` after each day's build and acceptance checks. Stop immediately
on the first FAIL; do not advance to N+1. A SKIPPED lab tool, unverified link or
diagram-count WARN fails the gate. Write `scratch/handoffs/day-NNN.md` using
`write_handoff.py`. Commit per day after PASS when commits are authorized; an
explicit no-commit instruction overrides this workflow. Never carry one day's
spec or summary into the next day's context. The coordinator keeps only current
day, gate result and commit ID. The gate checks a completed day; it never authors
or rebuilds any page. A changed pinned contract requires explicit resolution
before resuming; do not silently reset `scratch/batch-contract.sha256`.
