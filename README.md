# GCP Architect · 180-day static site

This site is generated from `../roadmap-180-days.md` and the 83-topic reading index in `../gcp-architect-roadmap-100-days.md`. It contains 180 day pages with four-part navigation. **The content is an incomplete draft, not a validated 180-day course.** [CONTENT_AUDIT.md](CONTENT_AUDIT.md) inventories the topic-level gaps across all 180 pages. Days 1–12 and 18 have hand-written content; the other topics largely use generated templates. The design follows the neighboring `gcp-architect-site` color and navigation patterns while keeping its files independent.

From the parent `RoadMap` directory:

```sh
python3 gcp-180day-architect-site/scripts/build.py --all
python3 gcp-180day-architect-site/scripts/validate.py
python3 -m http.server 8000 --directory gcp-180day-architect-site
```

For a page-by-page editing session, use [ONE_DAY_AT_A_TIME.md](ONE_DAY_AT_A_TIME.md). Initialize a day once, edit its override, and then build only that day:

```sh
python3 gcp-180day-architect-site/scripts/build.py --init-day 3
# Edit gcp-180day-architect-site/content/day-003-page.html before building.
python3 gcp-180day-architect-site/scripts/build.py --day 3
python3 gcp-180day-architect-site/scripts/validate.py
```

Complete HTML page overrides live in `content/day-NNN-page.html`. `--init-day` copies the existing page only when an override does not yet exist. Edit that override before running `--day`, which validates and writes only `days/day-NNN.html`. The explicit `--all` rebuild retains overrides but still generates draft fallback content for days without one. Days 1 and 2 already have overrides.

Open `http://localhost:8000/`. The build needs the Python `markdown` package; validation needs `beautifulsoup4`. The generated site itself needs no runtime package, service, login or network access. External further-study links need internet access when opened.

`data/coverage.csv` records each day's topic key, four anchors, exit artifact and reading mapping. `data/content-audit.csv` records the generated-content flags for every topic. After regenerating the pages, refresh the audit:

```sh
python3 gcp-180day-architect-site/scripts/audit_content.py
```

Progress is stored only in the browser under `gcp-180day-architect-progress-v1`; export and import controls appear on the index. A checked reading box is separate from each lab and saved artifact. Rendered code blocks have a Copy button; runnable commands in authored labs are fenced blocks with expected output and cleanup notes.

## Current content limits

The exercises are mostly repeated tabletop worksheets. Days 1–4, 6–10 and 12 include authored command-based checks, Day 5 includes specific offline fixtures, and Day 18 includes a Console walkthrough. A tabletop result is never evidence that a live cloud configuration, IAM policy, failover path or SLO works. Cloud-facing days need subject-specific instruction, commands or concrete worksheets, supplied fixtures and observed verification before they can serve as lessons. Many "Topics of the day" headings are clauses copied from the roadmap rather than curated learning topics.

The source index preserves publisher URLs from the 100-day roadmap. Each day links to its source-topic section in this site, but the publisher URL is **not** claimed to land on the exact relevant section; `coverage.csv` marks `publisher_section_verified=no` for every mapped item. Topic-level deep publisher links and timestamped videos still require a separate source audit. These are known gaps against the full build prompt, not validated citations.
