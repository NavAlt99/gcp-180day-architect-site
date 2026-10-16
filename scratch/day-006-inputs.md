# Day 6 inputs

## Roadmap entry

### Day 6 — Shell, processes and services

**Time:** 2–3 hours. **Entry prerequisites:** [Day 1](#day-1); bring their exit artifacts.  
**Topic references:** [0.2 / Topic 002](gcp-architect-roadmap-100-days.md#topic-002-references).

- **Study:** Linux kernel vs user space, file system navigation, permissions (chmod, chown), users and groups; Processes, file descriptors (stdin/stdout/stderr), pipes, redirection, boot-to-service sequence and services (systemd unit lifecycle), signals (SIGTERM, SIGKILL), exit statuses, logs (journalctl, /var/log)
- **Practice:** Start and stop a disposable local service, inspect its PID and journal, and compare a graceful stop with a forced termination.
- **Exit evidence:** Commands, exit codes and log timestamps explaining the service lifecycle.

<a id="day-7"></a>

## Compact brief

## Day 6 — Shell, processes and services

~~~text
Work only on Day 6 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-6"></a>

### Day 6 — Shell, processes and services

**Time:** 2–3 hours. **Entry prerequisites:** [Day 1](#day-1); bring their exit artifacts.  
**Topic references:** [0.2 / Topic 002](gcp-architect-roadmap-100-days.md#topic-002-references).

- **Study:** Linux kernel vs user space, file system navigation, permissions (chmod, chown), users and groups; Processes, file descriptors (stdin/stdout/stderr), pipes, redirection, boot-to-service sequence and services (systemd unit lifecycle), signals (SIGTERM, SIGKILL), exit statuses, logs (journalctl, /var/log)
- **Practice:** Start and stop a disposable local service, inspect its PID and journal, and compare a graceful stop with a forced termination.
- **Exit evidence:** Commands, exit codes and log timestamps explaining the service lifecycle.

Coverage keys and required anchors:
- `topic-01` — Linux kernel vs user space, file system navigation, permissions (chmod, chown), users and… — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Processes, file descriptors (stdin/stdout/stderr), pipes, redirection, boot-to-service… — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`

Update `scratch/day_data_006.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 6`, build only this day with `python3 scripts/build.py --day 6`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
6,topic-01,"Linux kernel vs user space, file system navigation, permissions (chmod, chown), users and…","Linux kernel vs user space, file system navigation, permissions (chmod, chown), users and groups",2,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"Commands, exit codes and log timestamps explaining the service lifecycle.",sources.html#topic-002,https://man7.org/linux/man-pages/man2/chmod.2.html#DESCRIPTION,yes
6,topic-02,"Processes, file descriptors (stdin/stdout/stderr), pipes, redirection, boot-to-service…","Processes, file descriptors (stdin/stdout/stderr), pipes, redirection, boot-to-service sequence and services (systemd unit lifecycle), signals (SIGTERM, SIGKILL), exit statuses, logs (journalctl, /var/log)",2,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"Commands, exit codes and log timestamps explaining the service lifecycle.",sources.html#topic-002,https://man7.org/linux/man-pages/man5/systemd.service.5.html#DESCRIPTION,yes
```
