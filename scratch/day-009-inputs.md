# Day 9 inputs

## Roadmap entry

### Day 9 — VM and container isolation

**Time:** 2–3 hours. **Entry prerequisites:** [Day 8](#day-8); bring their exit artifacts.  
**Topic references:** [0.3 / Topic 003](gcp-architect-roadmap-100-days.md#topic-003-references).

- **Study:** Virtualization and Containers: Hypervisors (Type 1 vs Type 2), what a VM actually is; Containers vs VMs (Linux kernel namespaces: PID, net, mnt, IPC, UTS, user; cgroups v2 resource limits for CPU/memory; seccomp profiles and capabilities)
- **Practice:** Inspect a local container's namespaces, cgroup limits and user identity; compare its isolation boundary with a VM diagram.
- **Exit evidence:** An isolation worksheet distinguishing resource enforcement from security isolation.

<a id="day-10"></a>

## Compact brief

## Day 9 — VM and container isolation

~~~text
Work only on Day 9 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-9"></a>

### Day 9 — VM and container isolation

**Time:** 2–3 hours. **Entry prerequisites:** [Day 8](#day-8); bring their exit artifacts.  
**Topic references:** [0.3 / Topic 003](gcp-architect-roadmap-100-days.md#topic-003-references).

- **Study:** Virtualization and Containers: Hypervisors (Type 1 vs Type 2), what a VM actually is; Containers vs VMs (Linux kernel namespaces: PID, net, mnt, IPC, UTS, user; cgroups v2 resource limits for CPU/memory; seccomp profiles and capabilities)
- **Practice:** Inspect a local container's namespaces, cgroup limits and user identity; compare its isolation boundary with a VM diagram.
- **Exit evidence:** An isolation worksheet distinguishing resource enforcement from security isolation.

Coverage keys and required anchors:
- `topic-01` — Hypervisors and virtual machines — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Container isolation — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`

Update `scratch/day_data_009.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 9`, build only this day with `python3 scripts/build.py --day 9`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
9,topic-01,Hypervisors and virtual machines,Hypervisors and virtual machines,3,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,An isolation worksheet distinguishing resource enforcement from security isolation.,sources.html#topic-003,https://docs.kernel.org/virt/kvm/api.html#general-description,yes
9,topic-02,Container isolation,"Container isolation: namespaces, cgroups, seccomp and capabilities",3,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,An isolation worksheet distinguishing resource enforcement from security isolation.,sources.html#topic-003,https://man7.org/linux/man-pages/man7/namespaces.7.html#DESCRIPTION,yes
```
