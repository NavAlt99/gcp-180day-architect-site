# Day 5 inputs

## Roadmap entry

### Day 5 — VPN, load balancers and firewalls

**Time:** 2–3 hours. **Entry prerequisites:** [Day 4](#day-4); bring their exit artifacts.  
**Topic references:** [0.1 / Topic 001](gcp-architect-roadmap-100-days.md#topic-001-references).

- **Study:** VPN concepts: IPsec, IKEv2 tunnels, site-to-site vs client VPN; Load balancing concepts: L4 vs L7, health checks, session affinity; Firewalls: stateful vs stateless, allow/deny rule ordering, failure boundaries
- **Practice:** Draw a client-to-backend flow with health checks and ordered firewall decisions; change one rule and predict the effect.
- **Exit evidence:** A packet decision table with both allowed and denied paths and a failure boundary.

<a id="day-6"></a>

## Compact brief

## Day 5 — VPN, load balancers and firewalls

~~~text
Work only on Day 5 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-5"></a>

### Day 5 — VPN, load balancers and firewalls

**Time:** 2–3 hours. **Entry prerequisites:** [Day 4](#day-4); bring their exit artifacts.  
**Topic references:** [0.1 / Topic 001](gcp-architect-roadmap-100-days.md#topic-001-references).

- **Study:** VPN concepts: IPsec, IKEv2 tunnels, site-to-site vs client VPN; Load balancing concepts: L4 vs L7, health checks, session affinity; Firewalls: stateful vs stateless, allow/deny rule ordering, failure boundaries
- **Practice:** Draw a client-to-backend flow with health checks and ordered firewall decisions; change one rule and predict the effect.
- **Exit evidence:** A packet decision table with both allowed and denied paths and a failure boundary.

Coverage keys and required anchors:
- `topic-01` — VPN concepts — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Load balancing concepts — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — Firewalls — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`

Update `scratch/day_data_005.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 5`, build only this day with `python3 scripts/build.py --day 5`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
5,topic-01,VPN concepts,"VPN concepts: IPsec, IKEv2 tunnels, site-to-site vs client VPN",1,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,A packet decision table with both allowed and denied paths and a failure boundary.,sources.html#topic-001,https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn,yes
5,topic-02,Load balancing concepts,"Load balancing concepts: L4 vs L7, health checks, session affinity",1,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,A packet decision table with both allowed and denied paths and a failure boundary.,sources.html#topic-001,https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview#load-balancer-types,yes
5,topic-03,Firewalls,"Firewalls: stateful vs stateless, allow/deny rule ordering, failure boundaries",1,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,A packet decision table with both allowed and denied paths and a failure boundary.,sources.html#topic-001,https://docs.cloud.google.com/firewall/docs/firewalls#firewall_rule_components,yes
```
