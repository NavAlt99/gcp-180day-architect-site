# Day 10 inputs

## Roadmap entry

### Day 10 — Images, filesystems and orchestration

**Time:** 2–3 hours. **Entry prerequisites:** [Day 9](#day-9); bring their exit artifacts.  
**Topic references:** [0.3 / Topic 003](gcp-architect-roadmap-100-days.md#topic-003-references).

- **Study:** Docker: images, layers, Dockerfile, registries, mounts, inodes, volumes, POSIX filesystem sync/fsync semantics; Container orchestration: why Kubernetes exists; Kubernetes core objects: Pod, Deployment, Service, Ingress, ConfigMap, Secret
- **Practice:** Build a tiny container from an annotated example; compare ephemeral files with a mounted volume and trace buffered write versus durable flush.
- **Exit evidence:** A runnable image, persistence check and Pod/Deployment/Service ownership diagram.

<a id="day-11"></a>

## Compact brief

## Day 10 — Images, filesystems and orchestration

~~~text
Work only on Day 10 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 1–17 — Foundations

<a id="day-10"></a>

### Day 10 — Images, filesystems and orchestration

**Time:** 2–3 hours. **Entry prerequisites:** [Day 9](#day-9); bring their exit artifacts.  
**Topic references:** [0.3 / Topic 003](gcp-architect-roadmap-100-days.md#topic-003-references).

- **Study:** Docker: images, layers, Dockerfile, registries, mounts, inodes, volumes, POSIX filesystem sync/fsync semantics; Container orchestration: why Kubernetes exists; Kubernetes core objects: Pod, Deployment, Service, Ingress, ConfigMap, Secret
- **Practice:** Build a tiny container from an annotated example; compare ephemeral files with a mounted volume and trace buffered write versus durable flush.
- **Exit evidence:** A runnable image, persistence check and Pod/Deployment/Service ownership diagram.

Coverage keys and required anchors:
- `topic-01` — Docker — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Container orchestration — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — Kubernetes core objects — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`

Update `scratch/day_data_010.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 10`, build only this day with `python3 scripts/build.py --day 10`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
10,topic-01,Docker,"Docker: images, layers, Dockerfile, registries, mounts, inodes, volumes, POSIX filesystem sync/fsync semantics",3,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,"A runnable image, persistence check and Pod/Deployment/Service ownership diagram.",sources.html#topic-003,https://docs.docker.com/get-started/docker-concepts/,no
10,topic-02,Container orchestration,Container orchestration: why Kubernetes exists,3,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,"A runnable image, persistence check and Pod/Deployment/Service ownership diagram.",sources.html#topic-003,https://kubernetes.io/docs/concepts/,no
10,topic-03,Kubernetes core objects,"Kubernetes core objects: Pod, Deployment, Service, Ingress, ConfigMap, Secret",3,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,"A runnable image, persistence check and Pod/Deployment/Service ownership diagram.",sources.html#topic-003,https://kubernetes.io/docs/concepts/,no
```
