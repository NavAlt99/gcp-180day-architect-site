# Day 15 inputs

## Roadmap entry

### Day 15 — Small application and architecture styles

**Time:** 2–3 hours. **Entry prerequisites:** [Day 14](#day-14); bring their exit artifacts.  
**Topic references:** [0.5 / Topic 005](gcp-architect-roadmap-100-days.md#topic-005-references).

- **Study:** Basic Python or Bash from an annotated example; request validation, REST/JSON, request IDs and structured logs. Compare monolith, microservices and serverless styles and apply relevant 12-factor principles. SQL starts on Day 16 rather than being bundled into this programming session.
- **Practice:** Adapt a worked Python or Bash example into a small order endpoint with request IDs and structured logs; handle invalid input.
- **Exit evidence:** A reproducible local request, validation failure and a diagram comparing monolith and service boundaries.

<a id="day-16"></a>

## Compact brief

## Day 15 — Small application and architecture styles

~~~text
Work only on Day 15 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-15"></a>

### Day 15 — Small application and architecture styles

**Time:** 2–3 hours. **Entry prerequisites:** [Day 14](#day-14); bring their exit artifacts.  
**Topic references:** [0.5 / Topic 005](gcp-architect-roadmap-100-days.md#topic-005-references).

- **Study:** Basic Python or Bash from an annotated example; request validation, REST/JSON, request IDs and structured logs. Compare monolith, microservices and serverless styles and apply relevant 12-factor principles. SQL starts on Day 16 rather than being bundled into this programming session.
- **Practice:** Adapt a worked Python or Bash example into a small order endpoint with request IDs and structured logs; handle invalid input.
- **Exit evidence:** A reproducible local request, validation failure and a diagram comparing monolith and service boundaries.

Coverage keys and required anchors:
- `topic-01` — Basic Python or Bash from an annotated example — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Request validation, REST/JSON, request IDs and structured logs — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`

Update `scratch/day_data_015.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 15`, build only this day with `python3 scripts/build.py --day 15`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
15,topic-01,Basic Python or Bash from an annotated example,Basic Python or Bash from an annotated example,5,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"A reproducible local request, validation failure and a diagram comparing monolith and service boundaries.",sources.html#topic-005,https://missing.csail.mit.edu/2020/shell-tools/#shell-scripting,yes
15,topic-02,"Request validation, REST/JSON, request IDs and structured logs","request validation, REST/JSON, request IDs and structured logs. Compare monolith, microservices and serverless styles and apply relevant 12-factor principles. SQL starts on Day 16 rather than being bundled into this programming session.",5,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"A reproducible local request, validation failure and a diagram comparing monolith and service boundaries.",sources.html#topic-005,https://12factor.net/logs#treat_logs_as_event_streams,yes
```
