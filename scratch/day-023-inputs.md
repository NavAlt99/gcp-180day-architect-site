# Day 23 inputs

## Roadmap entry

### Day 23 — Organization policies and lifecycle

**Time:** 2–3 hours. **Entry prerequisites:** [Day 22](#day-22); bring their exit artifacts.  
**Topic references:** [1.2 / Topic 008](gcp-architect-roadmap-100-days.md#topic-008-references).

- **Study:** Project lifecycle: creation, shutdown, 30-day recovery window; Designing a hierarchy for prod/staging/dev and for multi-team companies; Organization Policy Service (constraints that restrict what can be done, regardless of IAM)
- **Practice:** Review a supplied policy plan that restricts location or external addresses; predict accepted and rejected resources before applying a sandbox example.
- **Exit evidence:** An expected/observed or simulated policy test with rollback and a project lifecycle diagram.

<a id="day-24"></a>

## Compact brief

## Day 23 — Organization policies and lifecycle

~~~text
Work only on Day 23 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 18–35 — Cloud environment and identity

<a id="day-23"></a>

### Day 23 — Organization policies and lifecycle

**Time:** 2–3 hours. **Entry prerequisites:** [Day 22](#day-22); bring their exit artifacts.  
**Topic references:** [1.2 / Topic 008](gcp-architect-roadmap-100-days.md#topic-008-references).

- **Study:** Project lifecycle: creation, shutdown, 30-day recovery window; Designing a hierarchy for prod/staging/dev and for multi-team companies; Organization Policy Service (constraints that restrict what can be done, regardless of IAM)
- **Practice:** Review a supplied policy plan that restricts location or external addresses; predict accepted and rejected resources before applying a sandbox example.
- **Exit evidence:** An expected/observed or simulated policy test with rollback and a project lifecycle diagram.

Coverage keys and required anchors:
- `topic-01` — Project lifecycle — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Designing a hierarchy for prod/staging/dev and for multi-team companies — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — Organization Policy Service (constraints that restrict what can be done, regardless of IAM) — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`

Update `scratch/day_data_023.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 23`, build only this day with `python3 scripts/build.py --day 23`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
23,topic-01,Project lifecycle,"Project lifecycle: creation, shutdown, 30-day recovery window",8,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,An expected/observed or simulated policy test with rollback and a project lifecycle diagram.,sources.html#topic-008,https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#projects,yes
23,topic-02,Designing a hierarchy for prod/staging/dev and for multi-team companies,Designing a hierarchy for prod/staging/dev and for multi-team companies,8,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,An expected/observed or simulated policy test with rollback and a project lifecycle diagram.,sources.html#topic-008,https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#folders,yes
23,topic-03,"Organization Policy Service (constraints that restrict what can be done, regardless of IAM)","Organization Policy Service (constraints that restrict what can be done, regardless of IAM)",8,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,An expected/observed or simulated policy test with rollback and a project lifecycle diagram.,sources.html#topic-008,https://cloud.google.com/resource-manager/docs/organization-policy/overview#constraints,yes
```
