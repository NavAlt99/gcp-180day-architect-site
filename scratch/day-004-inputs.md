# Day 4 inputs

## Roadmap entry

### Day 4 — TLS, HTTP, MTU and routing vocabulary

**Time:** 2–3 hours. **Entry prerequisites:** [Day 3](#day-3); bring their exit artifacts.  
**Topic references:** [0.1 / Topic 001](gcp-architect-roadmap-100-days.md#topic-001-references).

- **Study:** HTTP/HTTPS, TLS 1.3 handshake, certificate validation chains, status codes, HTTP/1.1 vs HTTP/2 vs HTTP/3; MTU and MSS clamping; NAT (SNAT/DNAT) for private outbound; Routing basics: static vs dynamic routing, BGP at conceptual level
- **Practice:** Compare a valid and a hostname-mismatched certificate trace; annotate an MTU failure and forward/return routes on supplied captures.
- **Exit evidence:** A failure worksheet that separates TLS trust, packet size, routing and HTTP errors.

<a id="day-5"></a>

## Compact brief

## Day 4 — TLS, HTTP, MTU and routing vocabulary

~~~text
Work only on Day 4 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-4"></a>

### Day 4 — TLS, HTTP, MTU and routing vocabulary

**Time:** 2–3 hours. **Entry prerequisites:** [Day 3](#day-3); bring their exit artifacts.  
**Topic references:** [0.1 / Topic 001](gcp-architect-roadmap-100-days.md#topic-001-references).

- **Study:** HTTP/HTTPS, TLS 1.3 handshake, certificate validation chains, status codes, HTTP/1.1 vs HTTP/2 vs HTTP/3; MTU and MSS clamping; NAT (SNAT/DNAT) for private outbound; Routing basics: static vs dynamic routing, BGP at conceptual level
- **Practice:** Compare a valid and a hostname-mismatched certificate trace; annotate an MTU failure and forward/return routes on supplied captures.
- **Exit evidence:** A failure worksheet that separates TLS trust, packet size, routing and HTTP errors.

Coverage keys and required anchors:
- `topic-01` — HTTP/HTTPS, status codes, HTTP/1.1 vs HTTP/2 vs HTTP/3 — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — TLS 1.3 handshake and certificate validation chains — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — MTU and MSS clamping — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`
- `topic-04` — NAT (SNAT/DNAT) for private outbound — anchors: `#topic-04-overview`, `#topic-04-technical`, `#topic-04-problem`, `#topic-04-lab`
- `topic-05` — Routing basics — anchors: `#topic-05-overview`, `#topic-05-technical`, `#topic-05-problem`, `#topic-05-lab`

Update `scratch/day_data_004.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 4`, build only this day with `python3 scripts/build.py --day 4`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
4,topic-01,"HTTP/HTTPS, status codes, HTTP/1.1 vs HTTP/2 vs HTTP/3","HTTP/HTTPS, status codes, HTTP/1.1 vs HTTP/2 vs HTTP/3",1,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"A failure worksheet that separates TLS trust, packet size, routing and HTTP errors.",sources.html#topic-001,https://www.rfc-editor.org/rfc/rfc9110.html#section-15,yes
4,topic-02,TLS 1.3 handshake and certificate validation chains,TLS 1.3 handshake and certificate validation chains,1,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"A failure worksheet that separates TLS trust, packet size, routing and HTTP errors.",sources.html#topic-001,https://www.rfc-editor.org/rfc/rfc8446.html#section-4,yes
4,topic-03,MTU and MSS clamping,MTU and MSS clamping,1,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,"A failure worksheet that separates TLS trust, packet size, routing and HTTP errors.",sources.html#topic-001,https://www.rfc-editor.org/rfc/rfc1191.html#section-2,yes
4,topic-04,NAT (SNAT/DNAT) for private outbound,NAT (SNAT/DNAT) for private outbound,1,topic-04-overview,topic-04-technical,topic-04-problem,topic-04-lab,"A failure worksheet that separates TLS trust, packet size, routing and HTTP errors.",sources.html#topic-001,https://www.rfc-editor.org/rfc/rfc3022.html#section-2,yes
4,topic-05,Routing basics,"Routing basics: static vs dynamic routing, BGP at conceptual level",1,topic-05-overview,topic-05-technical,topic-05-problem,topic-05-lab,"A failure worksheet that separates TLS trust, packet size, routing and HTTP errors.",sources.html#topic-001,https://www.rfc-editor.org/rfc/rfc4271.html#section-3,yes
```
