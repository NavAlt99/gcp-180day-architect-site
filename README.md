# GCP Architect · 180-day static site

This site is generated from `../roadmap-180-days.md` and the 83-topic reading index in `../gcp-architect-roadmap-100-days.md`. It contains 180 day pages with four-part navigation. **The content is an incomplete draft, not a validated 180-day course.** [CONTENT_AUDIT.md](CONTENT_AUDIT.md) inventories the topic-level gaps across all 180 pages. Days 1–12 and 18 have hand-written content; the other topics largely use generated templates. The design follows the neighboring `gcp-architect-site` color and navigation patterns while keeping its files independent.

From the parent `RoadMap` directory:

```sh
python3 gcp-180day-architect-site/scripts/build.py --all
python3 gcp-180day-architect-site/scripts/validate.py
python3 -m http.server 8000 --directory gcp-180day-architect-site
```

## Curriculum page updates

Do not edit `content/day-NNN-page.html` or `days/day-NNN.html` as source. Author
the durable specification in `scratch/day_data_NNN.py`, then build and verify
only the selected day.

[PAGE_AUTHORING_CONTRACT.md](PAGE_AUTHORING_CONTRACT.md) is the canonical rule
file. Use [ONE_DAY_AT_A_TIME.md](ONE_DAY_AT_A_TIME.md) for isolated serial
execution, [DAY_WORKFLOW_PROMPT.md](DAY_WORKFLOW_PROMPT.md) for the complete
per-day workflow, [PAGE_UPDATE_PROMPT.md](PAGE_UPDATE_PROMPT.md) for its command
sequence and handoff, and [BATCH_UPDATE_PROMPT.md](BATCH_UPDATE_PROMPT.md) as the
single entry point for a multi-day range.

### Prompt parameters

`PROMPT_DAY.md` accepts exactly these six per-day inputs. Do not add workflow
instructions or new keys to that file.

| Parameter | Allowed value | Meaning |
| --- | --- | --- |
| `DAY` | Integer `1`–`180` | Required. Selects the only day that may be read, audited, or changed. |
| `SCOPE` | `plan`, `update`, `audit-only`, or `fix` | `plan` reports proposed work without changing files; `update` performs additive authoring; `audit-only` writes only the named audit evidence; `fix` applies only confirmed audit-ledger findings after the required `go` selection. |
| `DIAGRAMS` | `keep` or `allow` | `keep` preserves diagrams and reports unresolved visual issues; `allow` permits eligible diagram additions or repairs and gates diagram geometry/readability checks. |
| `TOPICS` | `keep` or `expand` | `keep` preserves mapped topic and subtopic scope; `expand` permits only additions supported by the same day's Study clauses. It never permits later-day material. |
| `EXTRA_TOPICS` | Empty, or user-named same-day roadmap topics | Leave empty normally. This field cannot invent, import, or reorder curriculum scope. |
| `IMPROVEMENTS` | Empty, or a single-line list of named fixes | Use for explicit requested improvements. `keywords:` may list comma-separated discovery-link terms; separate additional fixes with semicolons. Empty means apply only the standing rules and contract, without speculative extras. |

Use this complete shape, including empty fields:

```text
DAY=17
SCOPE=update
DIAGRAMS=allow
TOPICS=keep
EXTRA_TOPICS=
IMPROVEMENTS=keywords: Cloud Logging, log-based metric; fix the named source-ledger gaps
```

Common combinations:

- Audit and create the Day N findings ledger: `SCOPE=audit-only`.
- Apply selected confirmed findings: `SCOPE=fix`, then reply with `go`,
  `go defects`, `go enhancements`, or specific IDs such as `go F1,F3` when the
  workflow asks for the selection.
- Perform full additive authoring: `SCOPE=update`.
- Inspect and propose work without content changes: `SCOPE=plan`.
- Preserve all existing diagrams: `DIAGRAMS=keep`; permit eligible repairs or
  additions: `DIAGRAMS=allow`.

For one day, save those switches in `PROMPT_DAY.md` and ask the agent:

```text
Update Day N in gcp-180day-architect-site. Read PAGE_AUTHORING_CONTRACT.md once,
then follow ONE_DAY_AT_A_TIME.md and instantiate DAY_WORKFLOW_PROMPT.md using
PROMPT_DAY.md. Run scripts/extract_day_inputs.py --day N before day-specific
reading. Execute scripts/day_run.py in the required resolve, preflight, check,
gate, commit order and stop at the first failure.
```

For a range, the coordinator prompt adds these parameters:

| Parameter | Allowed value | Meaning |
| --- | --- | --- |
| `START` | Integer `1`–`180` | First day in the inclusive range, or the first incomplete day when resuming. |
| `END` | Integer `START`–`180` | Final day in the inclusive range. |
| `BATCH_SIZE` | Positive integer; default `10` | Checkpoint window size only. It never permits parallel or combined page authoring. |

The six per-day parameters remain required as shared worker switches. A range
may specify explicit per-day overrides; otherwise every day receives the shared
values. Use this prompt once after replacing `START` and `END`:

```text
Update curriculum pages from Day START through Day END in
gcp-180day-architect-site, with BATCH_SIZE=10 unless I specify another checkpoint
size. Use these shared worker switches unless I provide per-day overrides:
SCOPE=update
DIAGRAMS=allow
TOPICS=keep
EXTRA_TOPICS=
IMPROVEMENTS=

Follow BATCH_UPDATE_PROMPT.md as the canonical batch workflow. Read
PAGE_AUTHORING_CONTRACT.md once as the stable rules prefix, instantiate the full
DAY_WORKFLOW_PROMPT.md separately for every day, and author days strictly
serially in fresh isolated contexts. Advance only after the current day passes
all required gates. Stop at the first failed gate, contract-hash change,
unresolved source/lab/diagram issue, my stated stop boundary, or Day END. Do not
parallelize page authoring, combine page generation, defer per-day gates, or
silently skip a failed day.

Commits are authorized. Commit each passing day separately.

At each checkpoint, record the completed days, PASS/FAIL state, handoff paths,
commit IDs when applicable, and exact resume day. Do not recap page content.
```

If commits are not authorized, replace the commit sentence explicitly. To resume
a stopped batch, set `START` to the first incomplete day; leave completed PASS
days untouched. The default batch window is ten days, but every page remains an
isolated one-day job.

Open `http://localhost:8000/`. The build needs the Python `markdown` package; validation needs `beautifulsoup4`. The generated site itself needs no runtime package, service, login or network access. External further-study links need internet access when opened.

`data/coverage.csv` records each day's topic key, four anchors, exit artifact and reading mapping. `data/content-audit.csv` records the generated-content flags for every topic. After regenerating the pages, refresh the audit:

```sh
python3 gcp-180day-architect-site/scripts/audit_content.py
```

Progress is stored only in the browser under `gcp-180day-architect-progress-v1`; export and import controls appear on the index. A checked reading box is separate from each lab and saved artifact. Rendered code blocks have a Copy button; runnable commands in authored labs are fenced blocks with expected output and cleanup notes.

## Current content limits

The exercises are mostly repeated tabletop worksheets. Days 1–4, 6–10 and 12 include authored command-based checks, Day 5 includes specific offline fixtures, and Day 18 includes a Console walkthrough. A tabletop result is never evidence that a live cloud configuration, IAM policy, failover path or SLO works. Cloud-facing days need subject-specific instruction, commands or concrete worksheets, supplied fixtures and observed verification before they can serve as lessons. Many "Topics of the day" headings are clauses copied from the roadmap rather than curated learning topics.

The source index preserves publisher URLs from the 100-day roadmap. Each day links to its source-topic section in this site, but the publisher URL is **not** claimed to land on the exact relevant section; `coverage.csv` marks `publisher_section_verified=no` for every mapped item. Topic-level deep publisher links and timestamped videos still require a separate source audit. These are known gaps against the full build prompt, not validated citations.
