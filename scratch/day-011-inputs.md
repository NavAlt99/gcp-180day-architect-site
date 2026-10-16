# Day 11 inputs

## Roadmap entry

### Day 11 — Cloud service models and responsibility

**Time:** 2–3 hours. **Entry prerequisites:** [Day 10](#day-10); bring their exit artifacts.  
**Topic references:** [0.4 / Topic 004](gcp-architect-roadmap-100-days.md#topic-004-references).

- **Study:** IaaS, PaaS, FaaS, SaaS, and where GCP services fall; Shared responsibility model (what Google secures vs what you secure)
- **Practice:** Assign OS patching, application security and data recovery responsibilities for VM, managed-container and SaaS examples.
- **Exit evidence:** A responsibility matrix with an owner for each task.

<a id="day-12"></a>

## Compact brief

## Day 11 — Cloud service models and responsibility

~~~text
Work only on Day 11 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-11"></a>

### Day 11 — Cloud service models and responsibility

**Time:** 2–3 hours. **Entry prerequisites:** [Day 10](#day-10); bring their exit artifacts.  
**Topic references:** [0.4 / Topic 004](gcp-architect-roadmap-100-days.md#topic-004-references).

- **Study:** IaaS, PaaS, FaaS, SaaS, and where GCP services fall; Shared responsibility model (what Google secures vs what you secure)
- **Practice:** Assign OS patching, application security and data recovery responsibilities for VM, managed-container and SaaS examples.
- **Exit evidence:** A responsibility matrix with an owner for each task.

Coverage keys and required anchors:
- `topic-01` — IaaS, PaaS, FaaS, SaaS, and where GCP services fall — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Shared responsibility model (what Google secures vs what you secure) — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`

Update `scratch/day_data_011.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 11`, build only this day with `python3 scripts/build.py --day 11`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
11,topic-01,"IaaS, PaaS, FaaS, SaaS, and where GCP services fall","IaaS, PaaS, FaaS, SaaS, and where GCP services fall",4,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,A responsibility matrix with an owner for each task.,sources.html#topic-004,https://cloud.google.com/learn/paas-vs-iaas-vs-saas#what-are-iaas-paas-saas-and-caas,yes
11,topic-02,Shared responsibility model (what Google secures vs what you secure),Shared responsibility model (what Google secures vs what you secure),4,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,A responsibility matrix with an owner for each task.,sources.html#topic-004,https://docs.cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate#shared_responsibility,yes
```
