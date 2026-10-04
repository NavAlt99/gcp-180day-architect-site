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
