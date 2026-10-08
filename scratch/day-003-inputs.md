# Day 3 inputs

## Roadmap entry

### Day 3 — DNS, sockets and transport

**Time:** 2–3 hours. **Entry prerequisites:** [Day 2](#day-2); bring their exit artifacts.  
**Topic references:** [0.1 / Topic 001](gcp-architect-roadmap-100-days.md#topic-001-references).

- **Study:** IPv6 basics; DNS: record types (A, AAAA, CNAME, MX, TXT, NS, SOA, PTR), TTL, recursive vs authoritative resolvers; TCP vs UDP, three-way handshake, TCP connection states (ESTABLISHED, TIME_WAIT), ports, socket buffers
- **Practice:** Trace an IPv4 and IPv6 lookup from supplied resolver output; label socket endpoints and the TCP handshake.
- **Exit evidence:** A DNS/transport diagram distinguishing name resolution, reachability and established connection.

<a id="day-4"></a>

## Compact brief

## Day 3 — DNS, sockets and transport

~~~text
Work only on Day 3 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-3"></a>

### Day 3 — DNS, sockets and transport

**Time:** 2–3 hours. **Entry prerequisites:** [Day 2](#day-2); bring their exit artifacts.  
**Topic references:** [0.1 / Topic 001](gcp-architect-roadmap-100-days.md#topic-001-references).

- **Study:** IPv6 basics; DNS: record types (A, AAAA, CNAME, MX, TXT, NS, SOA, PTR), TTL, recursive vs authoritative resolvers; TCP vs UDP, three-way handshake, TCP connection states (ESTABLISHED, TIME_WAIT), ports, socket buffers
- **Practice:** Trace an IPv4 and IPv6 lookup from supplied resolver output; label socket endpoints and the TCP handshake.
- **Exit evidence:** A DNS/transport diagram distinguishing name resolution, reachability and established connection.

Coverage keys and required anchors:
- `topic-01` — IPv6 addressing and scope — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — DNS records, TTL and resolver roles — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — TCP and UDP, ports, connection states and buffers — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`

Update `scratch/day_data_003.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 3`, build only this day with `python3 scripts/build.py --day 3`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
3,topic-01,IPv6 addressing and scope,IPv6 addressing and scope,1,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"A DNS/transport diagram distinguishing name resolution, reachability and established connection.",sources.html#topic-001,https://datatracker.ietf.org/doc/html/rfc4291#section-2,yes
3,topic-02,"DNS records, TTL and resolver roles","DNS records, TTL and resolver roles",1,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"A DNS/transport diagram distinguishing name resolution, reachability and established connection.",sources.html#topic-001,https://datatracker.ietf.org/doc/html/rfc1035#section-3.2.1,yes
3,topic-03,"TCP and UDP, ports, connection states and buffers","TCP and UDP, ports, connection states and buffers",1,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,"A DNS/transport diagram distinguishing name resolution, reachability and established connection.",sources.html#topic-001,https://datatracker.ietf.org/doc/html/rfc9293#section-3,yes
```
