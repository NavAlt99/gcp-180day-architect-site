# Day 67 inputs

## Roadmap entry

### Day 67 — Gate 3 — Operate the core application

**Time:** 3–4 hours. **Entry prerequisites:** [Day 66](#day-66); bring their exit artifacts.  
**Topic references:** [tracker / Topic 069](gcp-architect-roadmap-100-days.md#topic-069-references).

- **Study:** Review and remediate prior material only; use the matching gate criteria in the Gates section. Do not introduce new services or concepts on a checkpoint day.
- **Practice:** Without the walkthrough, trace a request, diagnose one fault, recover the service and prove duplicate-event safety and access denial.
- **Exit evidence:** A scored G3 decision and indexed operational evidence for later architecture choices.

## Days 68–82 — Requirements, migration and architecture

<a id="day-68"></a>

## Compact brief

## Day 67 — Gate 3 — Operate the core application

~~~text
Work only on Day 67 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 36–67 — Core services and integrated practice

<a id="day-67"></a>

### Day 67 — Gate 3 — Operate the core application

**Time:** 3–4 hours. **Entry prerequisites:** [Day 66](#day-66); bring their exit artifacts.  
**Topic references:** [tracker / Topic 069](gcp-architect-roadmap-100-days.md#topic-069-references).

- **Study:** Review and remediate prior material only; use the matching gate criteria in the Gates section. Do not introduce new services or concepts on a checkpoint day.
- **Practice:** Without the walkthrough, trace a request, diagnose one fault, recover the service and prove duplicate-event safety and access denial.
- **Exit evidence:** A scored G3 decision and indexed operational evidence for later architecture choices.

Coverage keys and required anchors:
- `topic-01` — Prerequisite review and remediation — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Use the matching gate criteria in the Gates section — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`

Update `scratch/day_data_067.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 67`, build only this day with `python3 scripts/build.py --day 67`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Gate review: reuse evidence; score criteria, record remediation, and decide pass or repeat. No new service.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
67,topic-01,Prerequisite review and remediation,Prerequisite review and remediation,69,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,A scored G3 decision and indexed operational evidence for later architecture choices.,sources.html#topic-069,https://services.google.com/fh/files/misc/professional_cloud_architect_exam_guide_english.pdf,no
67,topic-02,Use the matching gate criteria in the Gates section,use the matching gate criteria in the Gates section. Do not introduce new services or concepts on a checkpoint day.,69,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,A scored G3 decision and indexed operational evidence for later architecture choices.,sources.html#topic-069,https://services.google.com/fh/files/misc/professional_cloud_architect_exam_guide_english.pdf,no
```
