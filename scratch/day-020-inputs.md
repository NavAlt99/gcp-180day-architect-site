# Day 20 inputs

## Roadmap entry

### Day 20 — APIs, client libraries and emulators

**Time:** 2–3 hours. **Entry prerequisites:** [Day 15](#day-15), [Day 19](#day-19); bring their exit artifacts.  
**Topic references:** [1.1 / Topic 007](gcp-architect-roadmap-100-days.md#topic-007-references) · [2.9 / Topic 021](gcp-architect-roadmap-100-days.md#topic-021-references).

- **Study:** API enablement, client libraries, local versus cloud endpoints, Cloud Shell Editor/Cloud Code and asynchronous operation polling. Run one emulator; learn the purpose and documented limitations of Pub/Sub, Firestore, Spanner and Bigtable emulators without installing all four.
- **Practice:** Run one Pub/Sub emulator example; configure its client endpoint and document how Firestore, Spanner and Bigtable emulators differ from production.
- **Exit evidence:** One reproducible emulator run and a four-service limitations matrix; no requirement to deploy all four.

<a id="day-21"></a>

## Compact brief

## Day 20 — APIs, client libraries and emulators

~~~text
Work only on Day 20 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 18–35 — Cloud environment and identity

<a id="day-20"></a>

### Day 20 — APIs, client libraries and emulators

**Time:** 2–3 hours. **Entry prerequisites:** [Day 15](#day-15), [Day 19](#day-19); bring their exit artifacts.  
**Topic references:** [1.1 / Topic 007](gcp-architect-roadmap-100-days.md#topic-007-references) · [2.9 / Topic 021](gcp-architect-roadmap-100-days.md#topic-021-references).

- **Study:** API enablement, client libraries, local versus cloud endpoints, Cloud Shell Editor/Cloud Code and asynchronous operation polling. Run one emulator; learn the purpose and documented limitations of Pub/Sub, Firestore, Spanner and Bigtable emulators without installing all four.
- **Practice:** Run one Pub/Sub emulator example; configure its client endpoint and document how Firestore, Spanner and Bigtable emulators differ from production.
- **Exit evidence:** One reproducible emulator run and a four-service limitations matrix; no requirement to deploy all four.

Coverage keys and required anchors:
- `topic-01` — API enablement, client libraries, local versus cloud endpoints, Cloud Shell Editor/Cloud… — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Learn the purpose and documented limitations of Pub/Sub, Firestore, Spanner and Bigtable… — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`

Update `scratch/day_data_020.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 20`, build only this day with `python3 scripts/build.py --day 20`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
20,topic-01,"API enablement, client libraries, local versus cloud endpoints, Cloud Shell Editor/Cloud…","API enablement, client libraries, local versus cloud endpoints, Cloud Shell Editor/Cloud Code and asynchronous operation polling. Run one emulator","7,21",topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,One reproducible emulator run and a four-service limitations matrix; no requirement to deploy all four.,sources.html#topic-007,https://cloud.google.com/apis/docs/client-libraries-explained#cloud-client-libraries,yes
20,topic-02,"Learn the purpose and documented limitations of Pub/Sub, Firestore, Spanner and Bigtable…","learn the purpose and documented limitations of Pub/Sub, Firestore, Spanner and Bigtable emulators without installing all four.","7,21",topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,One reproducible emulator run and a four-service limitations matrix; no requirement to deploy all four.,sources.html#topic-007,https://cloud.google.com/pubsub/docs/emulator#known_limitations,yes
```
