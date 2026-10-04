# Day 7 inputs

## Roadmap entry

### Day 7 — SSH, scripts and process inspection

**Time:** 2–3 hours. **Entry prerequisites:** [Day 6](#day-6); bring their exit artifacts.  
**Topic references:** [0.2 / Topic 002](gcp-architect-roadmap-100-days.md#topic-002-references).

- **Study:** SSH: keys, config files, port forwarding, bastion (jump) hosts; Package managers (apt, yum/dnf); Shell scripting: variables, loops, conditionals, exit codes; /proc virtual filesystem and process trees
- **Practice:** Use a local test VM to inspect SSH configuration; write a small script that parses synthetic JSON and fails explicitly on invalid input.
- **Exit evidence:** A script with successful and failed runs, quoting explained, and no stored credentials.

<a id="day-8"></a>

## Compact brief

## Day 7 — SSH, scripts and process inspection

~~~text
Work only on Day 7 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-7"></a>

### Day 7 — SSH, scripts and process inspection

**Time:** 2–3 hours. **Entry prerequisites:** [Day 6](#day-6); bring their exit artifacts.  
**Topic references:** [0.2 / Topic 002](gcp-architect-roadmap-100-days.md#topic-002-references).

- **Study:** SSH: keys, config files, port forwarding, bastion (jump) hosts; Package managers (apt, yum/dnf); Shell scripting: variables, loops, conditionals, exit codes; /proc virtual filesystem and process trees
- **Practice:** Use a local test VM to inspect SSH configuration; write a small script that parses synthetic JSON and fails explicitly on invalid input.
- **Exit evidence:** A script with successful and failed runs, quoting explained, and no stored credentials.

Coverage keys and required anchors:
- `topic-01` — SSH — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Package managers (apt, yum/dnf) — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — Shell scripting — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`
- `topic-04` — /proc virtual filesystem and process trees — anchors: `#topic-04-overview`, `#topic-04-technical`, `#topic-04-problem`, `#topic-04-lab`

Update `scratch/day_data_007.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 7`, build only this day with `python3 scripts/build.py --day 7`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
7,topic-01,SSH,"SSH: keys, config files, port forwarding, bastion (jump) hosts",2,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"A script with successful and failed runs, quoting explained, and no stored credentials.",sources.html#topic-002,https://man7.org/linux/man-pages/man5/ssh_config.5.html#DESCRIPTION,yes
7,topic-02,"Package managers (apt, yum/dnf)","Package managers (apt, yum/dnf)",2,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"A script with successful and failed runs, quoting explained, and no stored credentials.",sources.html#topic-002,https://man7.org/linux/man-pages/man8/rpm.8.html#DESCRIPTION,yes
7,topic-03,Shell scripting,"Shell scripting: variables, loops, conditionals, exit codes",2,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,"A script with successful and failed runs, quoting explained, and no stored credentials.",sources.html#topic-002,https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION,yes
7,topic-04,/proc virtual filesystem and process trees,/proc virtual filesystem and process trees,2,topic-04-overview,topic-04-technical,topic-04-problem,topic-04-lab,"A script with successful and failed runs, quoting explained, and no stored credentials.",sources.html#topic-002,https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION,yes
```
