# Day 8 inputs

## Roadmap entry

### Day 8 — CPU, memory and diagnostic signals

**Time:** 2–3 hours. **Entry prerequisites:** [Day 6](#day-6), [Day 7](#day-7); bring their exit artifacts.  
**Topic references:** [0.2 / Topic 002](gcp-architect-roadmap-100-days.md#topic-002-references).

- **Study:** CPU scheduling and waiting, context switching, virtual memory, page faults, RAM/page cache/swap, OOM and PSI; grep/sed/awk/jq and curl/dig/ss/tcpdump as diagnostic tools. Learn to interpret one signal at a time; advanced scheduler or kernel tuning is optional.
- **Practice:** Observe a bounded local CPU task and inspect memory/page-cache metrics; explain supplied OOM and PSI examples without exhausting the host.
- **Exit evidence:** A resource baseline and predicted CPU-throttling versus memory-pressure symptoms.

<a id="day-9"></a>

## Compact brief

## Day 8 — CPU, memory and diagnostic signals

~~~text
Work only on Day 8 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-8"></a>

### Day 8 — CPU, memory and diagnostic signals

**Time:** 2–3 hours. **Entry prerequisites:** [Day 6](#day-6), [Day 7](#day-7); bring their exit artifacts.  
**Topic references:** [0.2 / Topic 002](gcp-architect-roadmap-100-days.md#topic-002-references).

- **Study:** CPU scheduling and waiting, context switching, virtual memory, page faults, RAM/page cache/swap, OOM and PSI; grep/sed/awk/jq and curl/dig/ss/tcpdump as diagnostic tools. Learn to interpret one signal at a time; advanced scheduler or kernel tuning is optional.
- **Practice:** Observe a bounded local CPU task and inspect memory/page-cache metrics; explain supplied OOM and PSI examples without exhausting the host.
- **Exit evidence:** A resource baseline and predicted CPU-throttling versus memory-pressure symptoms.

Coverage keys and required anchors:
- `topic-01` — CPU scheduling and waiting, context switching, virtual memory, page faults, RAM/page… — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Grep/sed/awk/jq and curl/dig/ss/tcpdump as diagnostic tools — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`

Update `scratch/day_data_008.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 8`, build only this day with `python3 scripts/build.py --day 8`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
8,topic-01,"CPU scheduling and waiting, context switching, virtual memory, page faults, RAM/page…","CPU scheduling and waiting, context switching, virtual memory, page faults, RAM/page cache/swap, OOM and PSI",2,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,A resource baseline and predicted CPU-throttling versus memory-pressure symptoms.,sources.html#topic-002,https://pages.cs.wisc.edu/~remzi/OSTEP/,no
8,topic-02,Grep/sed/awk/jq and curl/dig/ss/tcpdump as diagnostic tools,grep/sed/awk/jq and curl/dig/ss/tcpdump as diagnostic tools. Learn to interpret one signal at a time,2,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,A resource baseline and predicted CPU-throttling versus memory-pressure symptoms.,sources.html#topic-002,https://www.brendangregg.com/linuxperf.html,no
```
