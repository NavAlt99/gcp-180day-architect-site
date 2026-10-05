# Day 22 inputs

## Roadmap entry

### Day 22 — Inheritance, labels and tags

**Time:** 2–3 hours. **Entry prerequisites:** [Day 21](#day-21); bring their exit artifacts.  
**Topic references:** [1.2 / Topic 008](gcp-architect-roadmap-100-days.md#topic-008-references).

- **Study:** Resources and inheritance (policies flow downward and are additive for IAM); Labels vs tags vs network tags (three different things, often confused)
- **Practice:** Evaluate effective access in a sample parent/child hierarchy and choose labels versus policy tags versus network tags for three uses.
- **Exit evidence:** An inheritance calculation and a tagging convention with concrete examples.

<a id="day-23"></a>

## Compact brief

## Day 22 — Inheritance, labels and tags

~~~text
Work only on Day 22 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 18–35 — Cloud environment and identity

<a id="day-22"></a>

### Day 22 — Inheritance, labels and tags

**Time:** 2–3 hours. **Entry prerequisites:** [Day 21](#day-21); bring their exit artifacts.  
**Topic references:** [1.2 / Topic 008](gcp-architect-roadmap-100-days.md#topic-008-references).

- **Study:** Resources and inheritance (policies flow downward and are additive for IAM); Labels vs tags vs network tags (three different things, often confused)
- **Practice:** Evaluate effective access in a sample parent/child hierarchy and choose labels versus policy tags versus network tags for three uses.
- **Exit evidence:** An inheritance calculation and a tagging convention with concrete examples.

Coverage keys and required anchors:
- `topic-01` — Resources and inheritance (policies flow downward and are additive for IAM) — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Labels vs tags vs network tags (three different things, often confused) — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`

Update `scratch/day_data_022.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 22`, build only this day with `python3 scripts/build.py --day 22`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
22,topic-01,Resources and inheritance (policies flow downward and are additive for IAM),Resources and inheritance (policies flow downward and are additive for IAM),8,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,An inheritance calculation and a tagging convention with concrete examples.,sources.html#topic-008,https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#benefits_of_the_organization_resource,yes
22,topic-02,"Labels vs tags vs network tags (three different things, often confused)","Labels vs tags vs network tags (three different things, often confused)",8,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,An inheritance calculation and a tagging convention with concrete examples.,sources.html#topic-008,https://cloud.google.com/resource-manager/docs/tags/tags-overview#tags_and_labels,yes
```
