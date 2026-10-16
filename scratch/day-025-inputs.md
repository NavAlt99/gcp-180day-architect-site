# Day 25 inputs

## Roadmap entry

### Day 25 — Roles and authorization decisions

**Time:** 2–3 hours. **Entry prerequisites:** [Day 24](#day-24); bring their exit artifacts.  
**Topic references:** [1.3 / Topic 009](gcp-architect-roadmap-100-days.md#topic-009-references).

- **Study:** Roles: basic (Owner/Editor/Viewer, avoid in production), predefined, custom; IAM policy structure: bindings, members, roles, conditions; Policy inheritance and the effective policy
- **Practice:** Evaluate predefined versus custom roles and test one narrow allowed operation and one denied operation using a sandbox or policy fixture.
- **Exit evidence:** Redacted authorization evidence tied to principal, resource, role and condition.

<a id="day-26"></a>

## Compact brief

## Day 25 — Roles and authorization decisions

~~~text
Work only on Day 25 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 18–35 — Cloud environment and identity

<a id="day-25"></a>

### Day 25 — Roles and authorization decisions

**Time:** 2–3 hours. **Entry prerequisites:** [Day 24](#day-24); bring their exit artifacts.  
**Topic references:** [1.3 / Topic 009](gcp-architect-roadmap-100-days.md#topic-009-references).

- **Study:** Roles: basic (Owner/Editor/Viewer, avoid in production), predefined, custom; IAM policy structure: bindings, members, roles, conditions; Policy inheritance and the effective policy
- **Practice:** Evaluate predefined versus custom roles and test one narrow allowed operation and one denied operation using a sandbox or policy fixture.
- **Exit evidence:** Redacted authorization evidence tied to principal, resource, role and condition.

Coverage keys and required anchors:
- `topic-01` — Roles — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — IAM policy structure — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — Policy inheritance and the effective policy — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`

Update `scratch/day_data_025.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 25`, build only this day with `python3 scripts/build.py --day 25`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
25,topic-01,Roles,"Roles: basic (Owner/Editor/Viewer, avoid in production), predefined, custom",9,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"Redacted authorization evidence tied to principal, resource, role and condition.",sources.html#topic-009,https://cloud.google.com/iam/docs/roles-overview#role-types,yes
25,topic-02,IAM policy structure,"IAM policy structure: bindings, members, roles, conditions",9,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"Redacted authorization evidence tied to principal, resource, role and condition.",sources.html#topic-009,https://cloud.google.com/iam/docs/policies#structure,yes
25,topic-03,Policy inheritance and the effective policy,Policy inheritance and the effective policy,9,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,"Redacted authorization evidence tied to principal, resource, role and condition.",sources.html#topic-009,https://cloud.google.com/iam/docs/overview#policy-inheritance,yes
```
