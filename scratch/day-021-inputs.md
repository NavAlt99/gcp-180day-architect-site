# Day 21 inputs

## Roadmap entry

### Day 21 — Resource hierarchy and ownership

**Time:** 2–3 hours. **Entry prerequisites:** [Day 19](#day-19); bring their exit artifacts.  
**Topic references:** [1.2 / Topic 008](gcp-architect-roadmap-100-days.md#topic-008-references).

- **Study:** Organization node (tied to Cloud Identity or Google Workspace domain); Folders (mapping to departments, environments or teams); Projects: project ID vs project name vs project number (ID is immutable and globally unique)
- **Practice:** Sketch an organization/folder/project hierarchy for development and production and label each owner.
- **Exit evidence:** A landing-zone draft with stable IDs, environment boundaries and operating responsibilities.

<a id="day-22"></a>

## Compact brief

## Day 21 — Resource hierarchy and ownership

~~~text
Work only on Day 21 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 18–35 — Cloud environment and identity

<a id="day-21"></a>

### Day 21 — Resource hierarchy and ownership

**Time:** 2–3 hours. **Entry prerequisites:** [Day 19](#day-19); bring their exit artifacts.  
**Topic references:** [1.2 / Topic 008](gcp-architect-roadmap-100-days.md#topic-008-references).

- **Study:** Organization node (tied to Cloud Identity or Google Workspace domain); Folders (mapping to departments, environments or teams); Projects: project ID vs project name vs project number (ID is immutable and globally unique)
- **Practice:** Sketch an organization/folder/project hierarchy for development and production and label each owner.
- **Exit evidence:** A landing-zone draft with stable IDs, environment boundaries and operating responsibilities.

Coverage keys and required anchors:
- `topic-01` — Organization node (tied to Cloud Identity or Google Workspace domain) — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Folders (mapping to departments, environments or teams) — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — Projects — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`

Update `scratch/day_data_021.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 21`, build only this day with `python3 scripts/build.py --day 21`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
21,topic-01,Organization node (tied to Cloud Identity or Google Workspace domain),Organization node (tied to Cloud Identity or Google Workspace domain),8,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"A landing-zone draft with stable IDs, environment boundaries and operating responsibilities.",sources.html#topic-008,https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#organizations,yes
21,topic-02,"Folders (mapping to departments, environments or teams)","Folders (mapping to departments, environments or teams)",8,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"A landing-zone draft with stable IDs, environment boundaries and operating responsibilities.",sources.html#topic-008,https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#folders,yes
21,topic-03,Projects,Projects: project ID vs project name vs project number (ID is immutable and globally unique),8,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,"A landing-zone draft with stable IDs, environment boundaries and operating responsibilities.",sources.html#topic-008,https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#projects,yes
```
