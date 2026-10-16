# Day 19 inputs

## Roadmap entry

### Day 19 — CLI configuration and identity checks

**Time:** 2–3 hours. **Entry prerequisites:** [Day 18](#day-18); bring their exit artifacts.  
**Topic references:** [1.1 / Topic 007](gcp-architect-roadmap-100-days.md#topic-007-references).

- **Study:** Cloud Shell (persistent 5 GB home directory, preinstalled tools); Install and configure `gcloud` locally (`gcloud init`, `gcloud config`, named configurations for multiple projects); Other CLIs: `gsutil`/`gcloud storage`, `bq`, `kubectl`
- **Practice:** Create named CLI configurations and verify project, identity and region before a read-only API call.
- **Exit evidence:** Commands that reliably identify the target environment and prevent an accidental project switch.

<a id="day-20"></a>

## Compact brief

## Day 19 — CLI configuration and identity checks

~~~text
Work only on Day 19 in `gcp-180day-architect-site` (the site directory in this repository). First read `AGENTS.md` and `PAGE_AUTHORING_CONTRACT.md`, then inspect this day’s roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the shared CSS/JS details needed to preserve its components. The roadmap entry below is the curriculum source of truth.

Work block: Days 18–35 — Cloud environment and identity

<a id="day-19"></a>

### Day 19 — CLI configuration and identity checks

**Time:** 2–3 hours. **Entry prerequisites:** [Day 18](#day-18); bring their exit artifacts.  
**Topic references:** [1.1 / Topic 007](gcp-architect-roadmap-100-days.md#topic-007-references).

- **Study:** Cloud Shell (persistent 5 GB home directory, preinstalled tools); Install and configure `gcloud` locally (`gcloud init`, `gcloud config`, named configurations for multiple projects); Other CLIs: `gsutil`/`gcloud storage`, `bq`, `kubectl`
- **Practice:** Create named CLI configurations and verify project, identity and region before a read-only API call.
- **Exit evidence:** Commands that reliably identify the target environment and prevent an accidental project switch.

Coverage keys and required anchors:
- `topic-01` — Cloud Shell (persistent 5 GB home directory, preinstalled tools) — anchors: `#topic-01-overview`, `#topic-01-technical`, `#topic-01-problem`, `#topic-01-lab`
- `topic-02` — Install and configure `gcloud` locally (`gcloud init`, `gcloud config`, named… — anchors: `#topic-02-overview`, `#topic-02-technical`, `#topic-02-problem`, `#topic-02-lab`
- `topic-03` — Other CLIs — anchors: `#topic-03-overview`, `#topic-03-technical`, `#topic-03-problem`, `#topic-03-lab`

Update `scratch/day_data_019.py` as the durable specification. Generate the override with `python3 scripts/author_engine.py --day 19`, build only this day with `python3 scripts/build.py --day 19`, then run `python3 scripts/validate.py`. Fix issues introduced by this day. Do not print the HTML; report the data specification, generated override, rendered page, checks actually run, and source/lab limitations. Choose an offline, emulator, cloud, or tabletop lab mode that matches the Practice; deploy only what the roadmap requires.
~~~

## Coverage rows

```csv
day,topic_key,topic,scope,source_topic_ids,overview_anchor,technical_anchor,problem_anchor,lab_anchor,expected_artifact,further_study_section,publisher_url,publisher_section_verified
19,topic-01,"Cloud Shell (persistent 5 GB home directory, preinstalled tools)","Cloud Shell (persistent 5 GB home directory, preinstalled tools)",7,topic-01-overview,topic-01-technical,topic-01-problem,topic-01-lab,Commands that reliably identify the target environment and prevent an accidental project switch.,sources.html#topic-007,https://cloud.google.com/shell/docs/how-cloud-shell-works#persistent_disk_storage,yes
19,topic-02,"Install and configure <kbd>gcloud</kbd> locally (<kbd>gcloud init</kbd>, <kbd>gcloud config</kbd>, named…","Install and configure `gcloud` locally (`gcloud init`, `gcloud config`, named configurations for multiple projects)",7,topic-02-overview,topic-02-technical,topic-02-problem,topic-02-lab,Commands that reliably identify the target environment and prevent an accidental project switch.,sources.html#topic-007,https://cloud.google.com/sdk/docs/configurations#multiple_configurations,yes
19,topic-03,Other CLIs,"Other CLIs: `gsutil`/`gcloud storage`, `bq`, `kubectl`",7,topic-03-overview,topic-03-technical,topic-03-problem,topic-03-lab,Commands that reliably identify the target environment and prevent an accidental project switch.,sources.html#topic-007,https://cloud.google.com/sdk/docs/components#default_components,yes
```
