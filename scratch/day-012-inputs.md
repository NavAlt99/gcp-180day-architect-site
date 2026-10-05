# Day 12 inputs

## Roadmap entry

### Day 12 — Regions, scaling and economics

**Time:** 2–3 hours. **Entry prerequisites:** [Day 5](#day-5), [Day 11](#day-11); bring their exit artifacts.  
**Topic references:** [0.4 / Topic 004](gcp-architect-roadmap-100-days.md#topic-004-references).

- **Study:** Regions, zones, multi-region and edge locations; Elasticity vs scalability, vertical vs horizontal scaling; CapEx vs OpEx, pay-as-you-go economics
- **Practice:** Estimate two deployment locations and compare vertical versus horizontal scaling for the retailer's hypothetical workload.
- **Exit evidence:** A location decision with latency, residency, cost and failure-domain assumptions.

<a id="day-13"></a>

## Compact brief

## Day 12 — Regions, scaling and economics

~~~text
Work only on Day 12 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-12"></a>

### Day 12 — Regions, scaling and economics

**Time:** 2–3 hours. **Entry prerequisites:** [Day 5](#day-5), [Day 11](#day-11); bring their exit artifacts.  
**Topic references:** [0.4 / Topic 004](gcp-architect-roadmap-100-days.md#topic-004-references).

- **Study:** Regions, zones, multi-region and edge locations; Elasticity vs scalability, vertical vs horizontal scaling; CapEx vs OpEx, pay-as-you-go economics
- **Practice:** Estimate two deployment locations and compare vertical versus horizontal scaling for the retailer's hypothetical workload.
- **Exit evidence:** A location decision with latency, residency, cost and failure-domain assumptions.

Coverage keys and required anchors:
- `topic-01` — Regions, zones, multi-region and edge locations — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Elasticity vs scalability, vertical vs horizontal scaling — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — CapEx vs OpEx, pay-as-you-go economics — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`

Update `scratch/day_data_012.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 12`, build only this day with `python3 scripts/build.py --day 12`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
12,topic-01,"Regions, zones, multi-region and edge locations","Regions, zones, multi-region and edge locations",4,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"A location decision with latency, residency, cost and failure-domain assumptions.",sources.html#topic-004,https://docs.cloud.google.com/compute/docs/regions-zones#choose,yes
12,topic-02,"Elasticity vs scalability, vertical vs horizontal scaling","Elasticity vs scalability, vertical vs horizontal scaling",4,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"A location decision with latency, residency, cost and failure-domain assumptions.",sources.html#topic-004,https://docs.cloud.google.com/compute/docs/autoscaler#autoscaling_policy,yes
12,topic-03,"CapEx vs OpEx, pay-as-you-go economics","CapEx vs OpEx, pay-as-you-go economics",4,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,"A location decision with latency, residency, cost and failure-domain assumptions.",sources.html#topic-004,https://docs.cloud.google.com/billing/docs/how-to/estimate-costs#access-pricing-calculator,yes
```
