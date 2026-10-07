# Day 1 inputs

## Roadmap entry

### Day 1 — Local workspace and learning baseline

**Time:** 2–3 hours. **Entry prerequisites:** None; begin with the orientation tasks.  
**Topic references:** [0.2 / Topic 002](gcp-architect-roadmap-100-days.md#topic-002-references) · [1.4 / Topic 010](gcp-architect-roadmap-100-days.md#topic-010-references).

- **Study:** Local shell/editor/repository orientation; study-day versus calendar-day planning; synthetic data, cost limits and cleanup. Read a worked example before installing or using unfamiliar tools. Cloud account setup is Day 18; Terraform and Kubernetes are introduced when needed.
- **Practice:** Create a disposable Linux workspace and evidence repository; run one harmless command and record its exit code. Choose a lab budget and a cleanup checklist before enabling paid resources.
- **Exit evidence:** A versioned README with available study hours, environment, baseline skills, budget and cleanup owner.

<a id="day-2"></a>

## Compact brief

## Day 1 — Local workspace and learning baseline

~~~text
Work only on Day 1 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-1"></a>

### Day 1 — Local workspace and learning baseline

**Time:** 2–3 hours. **Entry prerequisites:** None; begin with the orientation tasks.  
**Topic references:** [0.2 / Topic 002](gcp-architect-roadmap-100-days.md#topic-002-references) · [1.4 / Topic 010](gcp-architect-roadmap-100-days.md#topic-010-references).

- **Study:** Local shell/editor/repository orientation; study-day versus calendar-day planning; synthetic data, cost limits and cleanup. Read a worked example before installing or using unfamiliar tools. Cloud account setup is Day 18; Terraform and Kubernetes are introduced when needed.
- **Practice:** Create a disposable Linux workspace and evidence repository; run one harmless command and record its exit code. Choose a lab budget and a cleanup checklist before enabling paid resources.
- **Exit evidence:** A versioned README with available study hours, environment, baseline skills, budget and cleanup owner.

Coverage keys and required anchors:
- `topic-01` — Local workspace and evidence repository — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Study sessions and learning baseline — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — Synthetic data, budget and cleanup ownership — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`

Update `scratch/day_data_001.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 1`, build only this day with `python3 scripts/build.py --day 1`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
1,topic-01,Local workspace and evidence repository,Local workspace and evidence repository,"2,10",topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"A versioned README with available study hours, environment, baseline skills, budget and cleanup owner.",sources.html#topic-002,https://www.gnu.org/software/bash/manual/,no
1,topic-02,Study sessions and learning baseline,Study sessions and learning baseline,"2,10",topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"A versioned README with available study hours, environment, baseline skills, budget and cleanup owner.",sources.html#topic-002,https://www.gnu.org/software/bash/manual/,no
1,topic-03,"Synthetic data, budget and cleanup ownership","Synthetic data, budget and cleanup ownership","2,10",topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,"A versioned README with available study hours, environment, baseline skills, budget and cleanup owner.",sources.html#topic-010,https://docs.cloud.google.com/billing/docs/how-to/budgets,no
```
