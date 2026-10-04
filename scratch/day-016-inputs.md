# Day 16 inputs

## Roadmap entry

### Day 16 — SQL foundations and business outcomes

**Time:** 2–3 hours. **Entry prerequisites:** [Day 13](#day-13), [Day 15](#day-15); bring their exit artifacts.  
**Topic references:** [0.6 / Topic 006](gcp-architect-roadmap-100-days.md#topic-006-references) · [2.8 / Topic 020](gcp-architect-roadmap-100-days.md#topic-020-references).

- **Study:** Relational tables, primary/foreign keys, normalization, SELECT/JOIN/GROUP BY and transaction commit/rollback. Introduce ACID and an isolation anomaly through a worked example; locking/deadlocks are practised on Day 61. Use Cloud Digital Leader material for business framing; its exam and full course are optional.
- **Practice:** Create local orders and customers tables with keys; run a join and aggregate; commit and roll back a transaction. Write the business outcome this application serves.
- **Exit evidence:** Schema, query results, rollback evidence and a one-paragraph value statement; explain normalization and an isolation anomaly from a worked example.

<a id="day-17"></a>

## Compact brief

## Day 16 — SQL foundations and business outcomes

~~~text
Work only on Day 16 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-16"></a>

### Day 16 — SQL foundations and business outcomes

**Time:** 2–3 hours. **Entry prerequisites:** [Day 13](#day-13), [Day 15](#day-15); bring their exit artifacts.  
**Topic references:** [0.6 / Topic 006](gcp-architect-roadmap-100-days.md#topic-006-references) · [2.8 / Topic 020](gcp-architect-roadmap-100-days.md#topic-020-references).

- **Study:** Relational tables, primary/foreign keys, normalization, SELECT/JOIN/GROUP BY and transaction commit/rollback. Introduce ACID and an isolation anomaly through a worked example; locking/deadlocks are practised on Day 61. Use Cloud Digital Leader material for business framing; its exam and full course are optional.
- **Practice:** Create local orders and customers tables with keys; run a join and aggregate; commit and roll back a transaction. Write the business outcome this application serves.
- **Exit evidence:** Schema, query results, rollback evidence and a one-paragraph value statement; explain normalization and an isolation anomaly from a worked example.

Coverage keys and required anchors:
- `topic-01` — Relational tables, primary/foreign keys, normalization, SELECT/JOIN/GROUP BY and… — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Locking/deadlocks are practised on Day 61 — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`

Update `scratch/day_data_016.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 16`, build only this day with `python3 scripts/build.py --day 16`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
16,topic-01,"Relational tables, primary/foreign keys, normalization, SELECT/JOIN/GROUP BY and…","Relational tables, primary/foreign keys, normalization, SELECT/JOIN/GROUP BY and transaction commit/rollback. Introduce ACID and an isolation anomaly through a worked example","6,20",topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"Schema, query results, rollback evidence and a one-paragraph value statement; explain normalization and an isolation anomaly from a worked example.",sources.html#topic-006,https://www.postgresql.org/docs/current/tutorial-join.html#TUTORIAL-JOIN,yes
16,topic-02,Locking/deadlocks are practised on Day 61,locking/deadlocks are practised on Day 61. Use Cloud Digital Leader material for business framing,"6,20",topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"Schema, query results, rollback evidence and a one-paragraph value statement; explain normalization and an isolation anomaly from a worked example.",sources.html#topic-006,https://www.postgresql.org/docs/current/transaction-iso.html#TRANSACTION-ISO,yes
```
