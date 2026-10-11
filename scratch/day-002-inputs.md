# Day 2 inputs

## Roadmap entry

### Day 2 — IP addressing and packet paths

**Time:** 2–3 hours. **Entry prerequisites:** [Day 1](#day-1); bring their exit artifacts.  
**Topic references:** [0.1 / Topic 001](gcp-architect-roadmap-100-days.md#topic-001-references).

- **Study:** OSI and TCP/IP models (what lives at each layer; L4 vs L7); IPv4 addressing, private ranges (RFC 1918), ARP/NDP, CIDR notation and subnet math (/24, /20, /16; splitting ranges); Packet lifecycle from physical NIC to application socket
- **Practice:** Split a /24 into four equal networks and trace a packet from a host to a different subnet using a supplied diagram.
- **Exit evidence:** Four correct ranges with network/broadcast addresses and a labeled next-hop path.

<a id="day-3"></a>

## Compact brief

## Day 2 — IP addressing and packet paths

~~~text
Work only on Day 2 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-2"></a>

### Day 2 — IP addressing and packet paths

**Time:** 2–3 hours. **Entry prerequisites:** [Day 1](#day-1); bring their exit artifacts.  
**Topic references:** [0.1 / Topic 001](gcp-architect-roadmap-100-days.md#topic-001-references).

- **Study:** OSI and TCP/IP models (what lives at each layer; L4 vs L7); IPv4 addressing, private ranges (RFC 1918), ARP/NDP, CIDR notation and subnet math (/24, /20, /16; splitting ranges); Packet lifecycle from physical NIC to application socket
- **Practice:** Split a /24 into four equal networks and trace a packet from a host to a different subnet using a supplied diagram.
- **Exit evidence:** Four correct ranges with network/broadcast addresses and a labeled next-hop path.

Coverage keys and required anchors:
- `topic-01` — OSI and TCP/IP layer models — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — IPv4 addressing, private ranges, ARP/NDP and CIDR subnetting — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — Packet path from NIC to application socket — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`
- `topic-04` — Process communication protocols: IPC, Unix domain sockets, and network RPCs — anchors: `#topic-04-overview`, `#topic-04-technical`, `#topic-04-problem`, `#topic-04-lab`

Update `scratch/day_data_002.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 2`, build only this day with `python3 scripts/build.py --day 2`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
2,topic-01,OSI and TCP/IP layer models,OSI and TCP/IP layer models,1,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,Four correct ranges with network/broadcast addresses and a labeled next-hop path.,sources.html#topic-001,https://www.rfc-editor.org/rfc/rfc9293.html#section-2,yes
2,topic-02,"IPv4 addressing, private ranges, ARP/NDP and CIDR subnetting","IPv4 addressing, private ranges, ARP/NDP and CIDR subnetting",1,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,Four correct ranges with network/broadcast addresses and a labeled next-hop path.,sources.html#topic-001,https://www.rfc-editor.org/rfc/rfc1918.html#section-3,yes
2,topic-03,Packet path from NIC to application socket,Packet path from NIC to application socket,1,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,Four correct ranges with network/broadcast addresses and a labeled next-hop path.,sources.html#topic-001,https://docs.kernel.org/networking/napi.html#driver-api,yes
2,topic-04,"Process communication protocols: IPC, Unix domain sockets, and network RPCs","Process communication protocols: IPC, Unix domain sockets, and network RPCs",1,topic-04-overview,topic-04-technical,topic-04-problem,topic-04-lab,Four correct ranges with network/broadcast addresses and a labeled next-hop path.,sources.html#topic-001,https://man7.org/linux/man-pages/man7/unix.7.html#DESCRIPTION,yes
```
