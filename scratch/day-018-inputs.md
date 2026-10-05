# Day 18 inputs

## Roadmap entry

### Day 18 — Cloud sandbox and cost controls

**Time:** 2–3 hours. **Entry prerequisites:** [Day 17](#day-17); bring their exit artifacts.  
**Topic references:** [1.1 / Topic 007](gcp-architect-roadmap-100-days.md#topic-007-references).

- **Study:** Create a GCP account, claim the free trial credit; Understand the free tier (Always Free products and their limits); Google Cloud Console tour (navigation, pinned products, project picker)
- **Practice:** Select a training sandbox or disposable project, inspect billing access and configure budget notifications if authorized.
- **Exit evidence:** A redacted project/billing preflight and cleanup plan; explain why an alert is not a hard spend cap.

<a id="day-19"></a>

## Compact brief

## Day 18 — Cloud sandbox and cost controls

~~~text
Work only on Day 18 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 18–35 — Cloud environment and identity

<a id="day-18"></a>

### Day 18 — Cloud sandbox and cost controls

**Time:** 2–3 hours. **Entry prerequisites:** [Day 17](#day-17); bring their exit artifacts.  
**Topic references:** [1.1 / Topic 007](gcp-architect-roadmap-100-days.md#topic-007-references).

- **Study:** Create a GCP account, claim the free trial credit; Understand the free tier (Always Free products and their limits); Google Cloud Console tour (navigation, pinned products, project picker)
- **Practice:** Select a training sandbox or disposable project, inspect billing access and configure budget notifications if authorized.
- **Exit evidence:** A redacted project/billing preflight and cleanup plan; explain why an alert is not a hard spend cap.

Coverage keys and required anchors:
- `topic-01` — Google Cloud accounts and the Free Trial — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Google Cloud Free Tier and monthly limits — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — Google Cloud Console navigation and project selection — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`

Update `scratch/day_data_018.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 18`, build only this day with `python3 scripts/build.py --day 18`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
18,topic-01,Google Cloud accounts and the Free Trial,Google Cloud accounts and the Free Trial,7,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,A redacted project/billing preflight and cleanup plan; explain why an alert is not a hard spend cap.,sources.html#topic-007,https://cloud.google.com/free/docs/free-cloud-features#free-trial,yes
18,topic-02,Google Cloud Free Tier and monthly limits,Google Cloud Free Tier and monthly limits,7,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,A redacted project/billing preflight and cleanup plan; explain why an alert is not a hard spend cap.,sources.html#topic-007,https://cloud.google.com/free/docs/free-cloud-features#free-tier-usage-limits,yes
18,topic-03,Google Cloud Console navigation and project selection,Google Cloud Console navigation and project selection,7,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,A redacted project/billing preflight and cleanup plan; explain why an alert is not a hard spend cap.,sources.html#topic-007,https://cloud.google.com/resource-manager/docs/view-update-projects#identifying_projects,yes
```
