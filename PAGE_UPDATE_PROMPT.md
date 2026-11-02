# Curriculum page update prompt

Use for one day. Read `PAGE_AUTHORING_CONTRACT.md`, `AGENTS.md`, and
`ONE_DAY_AT_A_TIME.md`, then fill only the six switches in `PROMPT_DAY.md`.
Standing R1–R9 and switch semantics live in `AGENTS.md`.

Run from the site root, replacing N with `DAY`:

```sh
python3 scripts/day_run.py resolve --day N
python3 scripts/day_run.py preflight --day N
# Author only scratch/day_data_NNN.py from the extracted same-day inputs.
python3 scripts/day_run.py check --day N --diagrams allow
python3 scripts/day_run.py gate --day N
python3 scripts/day_run.py commit --day N
```

Use `--diagrams keep` when the prompt switch says `DIAGRAMS=keep`. Use
`--skip-labs` only for unavailable cloud access or tooling and list every skipped
lab and reason. Stop on the first failure. Never commit when the user prohibits
commits, and never push from this workflow.

The generated handoff is `scratch/handoffs/day-NNN.md`. It must include clickable
spec/override/page paths; layout/navigation status; anchors, depth, exercises and
diagram review; Exit-evidence status; checks actually run; source and lab limits;
Practice-to-lab mapping; source ledger; product-claim list; visuals list; spec
diff stat; and confirmation that explanatory prose was not removed. `UNRECORDED`
review entries and inaccessible sources remain unresolved, not passes.

Finish the gate and local commit before advancing an authorized batch. Start a
fresh isolated context for each day and retain only its number, gate result, and
commit ID.
