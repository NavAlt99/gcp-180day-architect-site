# Curriculum batch update prompt

Use this once for a multi-day request. The default window is 10 days: large
enough to remove repetitive user prompting while small enough for useful
checkpoints and recovery. Window size never changes the one-day context boundary.

```text
Update curriculum pages from Day START through Day END in
gcp-180day-architect-site, with BATCH_SIZE=10 unless I specify another checkpoint
size. Use these shared worker switches unless I provide per-day overrides:
SCOPE=update
DIAGRAMS=allow
TOPICS=expand
EXTRA_TOPICS=none
IMPROVEMENTS=none

Read PAGE_AUTHORING_CONTRACT.md once as the stable rules prefix. Follow
ONE_DAY_AT_A_TIME.md and instantiate the entire DAY_WORKFLOW_PROMPT.md for each
day; its PAGE_UPDATE_PROMPT.md reference supplies the command/handoff component.
Process the authorized range as consecutive windows, but author days strictly
serially. For every day:

1. Start a fresh isolated page context containing only the canonical static rules
   and that day's output from scripts/extract_day_inputs.py.
2. Author only that day's durable specification. Do not reuse prose, source
   conclusions, examples, lab results or summaries from another day.
3. Apply all standing R1-R9 requirements and the selected scope, diagram and
   topic rules. Run all PAGE_UPDATE_PROMPT.md commands required by that scope,
   repair target-introduced failures, write the handoff, and run
   scripts/batch_gate.py --day N --contract-hash when the workflow requires it.
4. Advance only after PASS. Commit that day separately only when commits are
   authorized.
5. Retain in the coordinator only the authorized range, current window/day,
   PASS/FAIL, handoff path and commit ID. Discard the worker context before the
   next day.

At each 10-day window boundary, write a compact checkpoint manifest and continue
without asking me to repeat this prompt. Stop immediately on the first failed
gate, contract-hash change, unresolved source/lab/diagram issue, my stated stop
boundary, or Day END. Do not parallelize page authoring, combine page generation,
defer per-day gates, or silently skip a failed day.

`SCOPE=plan` and `SCOPE=audit-only` complete their read-only work for every day
in the range. `SCOPE=fix` retains the worker prompt's explicit confirmation
boundary and therefore stops at the first day awaiting approval; resume at that
day after the requested `go` selection. `SCOPE=update` is the unattended batch
authoring mode.

Final response: report completed days, the first incomplete/failed day if any,
handoff paths, commits when applicable, and the exact resume day. Do not recap
page content.
```

Examples:

- `START=21 END=30` is one 10-day window and one user prompt.
- `START=21 END=45` is three internal windows (10, 10, 5) under one user prompt.
- To resume a stopped run, set `START` to the first incomplete day; completed
  PASS days remain untouched.
