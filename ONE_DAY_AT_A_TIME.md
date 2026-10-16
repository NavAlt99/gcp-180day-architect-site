# One day at a time

Apply `PAGE_AUTHORING_CONTRACT.md` once as the static rule prefix, then select
the compact day inputs using its Read budget. Use `PAGE_UPDATE_PROMPT.md` for
the command sequence and handoff; do not duplicate the contract into each task.

## Serial run selection

- Set CURRENT_DAY to the requested numeric day; for a single page,
  TARGET_DAY = CURRENT_DAY. An explicit day starts there; a later `next`
  advances one. Stop after Day 180.
- An explicitly authorized multi-day run has a start/end. Use one fresh,
  isolated page agent/context per day, strictly serially: finish the commands,
  acceptance checks and handoff for N before N+1. Never generate pages in a
  batch or edit two concurrently; do not pause between authorized days.
- Give each page agent only its compact brief and the canonical static rules.
  For ten days use ten isolated contexts; the coordinator retains only current
  day, agent result, build/validation status, not ten catalogs or long contexts.

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
