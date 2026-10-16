# Day 13 inputs

## Roadmap entry

### Day 13 — State, availability and recovery vocabulary

**Time:** 2–3 hours. **Entry prerequisites:** [Day 12](#day-12); bring their exit artifacts.  
**Topic references:** [0.4 / Topic 004](gcp-architect-roadmap-100-days.md#topic-004-references).

- **Study:** High availability vs fault tolerance vs disaster recovery (three different things); Stateless vs stateful applications (this decides almost every HA design)
- **Practice:** Restart the local service with and without external state; distinguish an available replica from a recoverable backup.
- **Exit evidence:** A state ownership diagram and definitions of HA, fault tolerance, RTO and RPO with examples.

<a id="day-14"></a>

## Compact brief

## Day 13 — State, availability and recovery vocabulary

~~~text
Work only on Day 13 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-13"></a>

### Day 13 — State, availability and recovery vocabulary

**Time:** 2–3 hours. **Entry prerequisites:** [Day 12](#day-12); bring their exit artifacts.  
**Topic references:** [0.4 / Topic 004](gcp-architect-roadmap-100-days.md#topic-004-references).

- **Study:** High availability vs fault tolerance vs disaster recovery (three different things); Stateless vs stateful applications (this decides almost every HA design)
- **Practice:** Restart the local service with and without external state; distinguish an available replica from a recoverable backup.
- **Exit evidence:** A state ownership diagram and definitions of HA, fault tolerance, RTO and RPO with examples.

Coverage keys and required anchors:
- `topic-01` — High availability vs fault tolerance vs disaster recovery (three different things) — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Stateless vs stateful applications (this decides almost every HA design) — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`

Update `scratch/day_data_013.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 13`, build only this day with `python3 scripts/build.py --day 13`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
13,topic-01,High availability vs fault tolerance vs disaster recovery (three different things),High availability vs fault tolerance vs disaster recovery (three different things),4,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"A state ownership diagram and definitions of HA, fault tolerance, RTO and RPO with examples.",sources.html#topic-004,https://docs.cloud.google.com/architecture/disaster-recovery#how_rto_limits_product_choices,yes
13,topic-02,Stateless vs stateful applications (this decides almost every HA design),Stateless vs stateful applications (this decides almost every HA design),4,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"A state ownership diagram and definitions of HA, fault tolerance, RTO and RPO with examples.",sources.html#topic-004,https://docs.cloud.google.com/compute/docs/instance-groups#support_for_stateful_workloads,yes
```
