# Day 24 inputs

## Roadmap entry

### Day 24 — Principals and workforce identity

**Time:** 2–3 hours. **Entry prerequisites:** [Day 23](#day-23); bring their exit artifacts.  
**Topic references:** [1.3 / Topic 009](gcp-architect-roadmap-100-days.md#topic-009-references).

- **Study:** Cloud Identity vs Google Workspace vs consumer Google accounts; Principals: Google account, group, service account, domain, allAuthenticatedUsers, allUsers; Why groups (not individual users) should receive roles
- **Practice:** Build a principal inventory for developers, operators and workloads; replace individual grants with suitable groups in the design.
- **Exit evidence:** An identity matrix distinguishing people, service accounts, groups and external identities.

<a id="day-25"></a>

## Compact brief

## Day 24 — Principals and workforce identity

~~~text
Work only on Day 24 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 18–35 — Cloud environment and identity

<a id="day-24"></a>

### Day 24 — Principals and workforce identity

**Time:** 2–3 hours. **Entry prerequisites:** [Day 23](#day-23); bring their exit artifacts.  
**Topic references:** [1.3 / Topic 009](gcp-architect-roadmap-100-days.md#topic-009-references).

- **Study:** Cloud Identity vs Google Workspace vs consumer Google accounts; Principals: Google account, group, service account, domain, allAuthenticatedUsers, allUsers; Why groups (not individual users) should receive roles
- **Practice:** Build a principal inventory for developers, operators and workloads; replace individual grants with suitable groups in the design.
- **Exit evidence:** An identity matrix distinguishing people, service accounts, groups and external identities.

Coverage keys and required anchors:
- `topic-01` — Cloud Identity vs Google Workspace vs consumer Google accounts — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Principals — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — Why groups (not individual users) should receive roles — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`

Update `scratch/day_data_024.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 24`, build only this day with `python3 scripts/build.py --day 24`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
24,topic-01,Cloud Identity vs Google Workspace vs consumer Google accounts,Cloud Identity vs Google Workspace vs consumer Google accounts,9,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"An identity matrix distinguishing people, service accounts, groups and external identities.",sources.html#topic-009,https://cloud.google.com/iam/docs/principals-overview#domains,yes
24,topic-02,Principals,"Principals: Google account, group, service account, domain, allAuthenticatedUsers, allUsers",9,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"An identity matrix distinguishing people, service accounts, groups and external identities.",sources.html#topic-009,https://cloud.google.com/iam/docs/principals-overview#principal-types,yes
24,topic-03,Why groups (not individual users) should receive roles,Why groups (not individual users) should receive roles,9,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,"An identity matrix distinguishing people, service accounts, groups and external identities.",sources.html#topic-009,https://cloud.google.com/iam/docs/groups-best-practices#job-functions-access,yes
```
