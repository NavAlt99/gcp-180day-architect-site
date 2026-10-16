# Day 14 inputs

## Roadmap entry

### Day 14 — Git, APIs and JSON

**Time:** 2–3 hours. **Entry prerequisites:** [Day 7](#day-7), [Day 10](#day-10); bring their exit artifacts.  
**Topic references:** [0.5 / Topic 005](gcp-architect-roadmap-100-days.md#topic-005-references).

- **Study:** Git fundamentals (branch, merge, PR); REST APIs and JSON
- **Practice:** Commit a tiny request/response example; create a branch, review a diff and merge a change; parse an error response.
- **Exit evidence:** A repository history and annotated HTTP/JSON success and failure examples.

<a id="day-15"></a>

## Compact brief

## Day 14 — Git, APIs and JSON

~~~text
Work only on Day 14 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-14"></a>

### Day 14 — Git, APIs and JSON

**Time:** 2–3 hours. **Entry prerequisites:** [Day 7](#day-7), [Day 10](#day-10); bring their exit artifacts.  
**Topic references:** [0.5 / Topic 005](gcp-architect-roadmap-100-days.md#topic-005-references).

- **Study:** Git fundamentals (branch, merge, PR); REST APIs and JSON
- **Practice:** Commit a tiny request/response example; create a branch, review a diff and merge a change; parse an error response.
- **Exit evidence:** A repository history and annotated HTTP/JSON success and failure examples.

Coverage keys and required anchors:
- `topic-01` — Git fundamentals (branch, merge, PR) — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — REST APIs and JSON — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`

Update `scratch/day_data_014.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 14`, build only this day with `python3 scripts/build.py --day 14`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
14,topic-01,"Git fundamentals (branch, merge, PR)","Git fundamentals (branch, merge, PR)",5,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,A repository history and annotated HTTP/JSON success and failure examples.,sources.html#topic-005,https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging#_basic_branching_and_merging,yes
14,topic-02,REST APIs and JSON,REST APIs and JSON,5,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,A repository history and annotated HTTP/JSON success and failure examples.,sources.html#topic-005,https://www.rfc-editor.org/rfc/rfc9110#section-9.3,yes
```
