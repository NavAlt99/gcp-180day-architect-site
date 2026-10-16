# Day 180 inputs

## Roadmap entry

### Day 180 — Final review, logistics and rest

**Time:** 0.5–1 hours. **Entry prerequisites:** [Day 179](#day-179); bring their exit artifacts.  
**Topic references:** [consult-2 / Topic 067](gcp-architect-roadmap-100-days.md#topic-067-references) · [tracker / Topic 069](gcp-architect-roadmap-100-days.md#topic-069-references).

- **Study:** Consolidate existing evidence, logistics and the continuing-learning plan. No new material.
- **Practice:** Read the remaining uncertainty log, confirm exam arrangements if booked and stop adding new scope.
- **Exit evidence:** A continuing-learning list, verified cleanup and realistic next steps; no new lab or timed assessment.

## Choosing between the 180-day and 100-day routes

The [100-day plan](gcp-architect-roadmap-100-days.md) is a different learning structure: five 20-day levels revisit the same domains with increasing depth. Its published planning estimate is 460–560 hours at 3–7 hours per study day. This 180-day route spreads domain-specific practice across more sessions, uses six gates and ends with five capstone defenses. Its own hour estimate is in the workload table above. Neither count represents a guaranteed time to mastery, certification or a Staff-level role.

Choose the phase route for longer stretches on one domain, or the level route for frequent revisiting across domains. To switch, map topic IDs and accepted artifacts; reuse valid evidence and complete missing prerequisites rather than matching day numbers or dropping whole phases. Both now use the same F01–F12 meanings. At a lower daily time budget, extend the calendar while preserving the completion criteria. Optional specialist work can deepen either route without being silently included in its estimate.

## Completion and continuing practice

- Every daily task has accepted evidence or an explicitly recorded limitation; critical gate failures are repaired.
- All 83 source topics are mapped to actual artifacts, with the depth reached recorded honestly.
- Design choices can be traced backward through experiments or documented alternatives to the underlying mechanism.
- The five capstone reviews include costs, failure/recovery, security, ownership, exceptions and measurable adoption.
- Resources are cleaned up, unsupported claims are removed, and remaining experience gaps have a continuing-learning plan.

## Compact brief

## Day 180 — Final review, logistics and rest

~~~text
Work only on Day 180 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Day 180 — Final review and rest

<a id="day-180"></a>

### Day 180 — Final review, logistics and rest

**Time:** 0.5–1 hours. **Entry prerequisites:** [Day 179](#day-179); bring their exit artifacts.  
**Topic references:** [consult-2 / Topic 067](gcp-architect-roadmap-100-days.md#topic-067-references) · [tracker / Topic 069](gcp-architect-roadmap-100-days.md#topic-069-references).

- **Study:** Consolidate existing evidence, logistics and the continuing-learning plan. No new material.
- **Practice:** Read the remaining uncertainty log, confirm exam arrangements if booked and stop adding new scope.
- **Exit evidence:** A continuing-learning list, verified cleanup and realistic next steps; no new lab or timed assessment.

Coverage keys and required anchors:
- `topic-01` — Consolidate existing evidence, logistics and the continuing-learning plan — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`

Update `scratch/day_data_180.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 180`, build only this day with `python3 scripts/build.py --day 180`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Final review/rest: consolidate evidence and cleanup; no new lab or timed assessment.
~~~

## Alternate Day 13 — user-supplied VPC firewall sequence

~~~text
Use the same `PAGE_AUTHORING_CONTRACT.md`, but treat the following user-supplied curriculum as an alternate. Do not change canonical Day 13 or its neighbors.

### Day 13 — VPC Security: Cloud Firewall Policies and Network IAM
- Time Estimate: 3.5 hours
- Entry prerequisites: Day 12 Custom VPC foundation deployed with non-overlapping subnets.
- Study: VPC Firewall components (ingress vs. egress, implied rules, priority values), Network Tags vs. Service Accounts for targeting, Hierarchical Firewall Policies, and Network IAM Roles (Network Admin vs. Security Admin).
- Practice: Design a zero-trust firewall policy mapping for the Brightloaf retail tier isolation (Frontend, Order API, Database).
- Exit evidence: Validated gcloud commands enforcing strict directional traffic rules and an IAM role assignment matrix for network segregation.
- Topic keys: gcp-firewall-rules, gcp-firewall-tags, gcp-iam-network

Extra constraints for this alternate only: clearly label it as user-supplied and noncanonical; align prerequisites before adopting. Explain implied rules, priority, targeting trade-offs, hierarchy, and the Network Admin/Security Admin permissions split. Show the client → frontend → API → database path with direct frontend-to-database access blocked. Correct any technically impossible incident hypothesis before proposing a policy. If using cloud, require project/account, API, permission, rule inventory, region and budget preflight; use exact commands, never expose a database publicly, and clean up in reverse order. This is a firewall design exercise, not a request to silently change canonical Day 13.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
180,topic-01,"Consolidate existing evidence, logistics and the continuing-learning plan","Consolidate existing evidence, logistics and the continuing-learning plan. No new material.","67,69",topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"A continuing-learning list, verified cleanup and realistic next steps; no new lab or timed assessment.",sources.html#topic-067,https://docs.cloud.google.com/architecture/framework,no
```
