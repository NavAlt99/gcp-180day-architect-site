# Curriculum Page Update Prompt

Use this prompt for one GCP Architect 180-day curriculum page at a time. Replace `NNN` with the three-digit day number and `N` with the numeric day.

```text
Update only Day NNN of the GCP 180-day Architect curriculum site.

Repository root: /home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site

Read and follow these sources in this exact precedence order. Existing HTML is rendered output and must never override a higher-priority source.
1. ../roadmap-180-days.md — authoritative day scope, prerequisites, study, practice, and exit evidence.
2. ../gcp-architect-180-day-page-prompts.md — Day NNN brief, study goals, exercises, and required anchors.
3. data/coverage.csv — Day NNN topic mappings, required overview/technical/problem/lab anchor IDs, exit evidence, source-topic IDs, and publisher links.
4. ../gcp-architect-roadmap-100-days.md — source-topic cross references and official documentation anchors.
5. PAGE_AUTHORING_CONTRACT.md — mandatory page structure, evidence, SVG, lab, and source rules.
6. ONE_DAY_AT_A_TIME.md — serial authoring, validation, and handoff process.
7. AGENTS.md — repository-specific operating instructions.

Before editing, inspect these Day NNN artifacts when they exist:
- scratch/day_data_NNN.py
- content/day-NNN-page.html
- days/day-NNN.html (reference only; do not treat it as curriculum truth)
- scripts/day_data_template.py and scripts/author_engine.py as needed to preserve the data schema.

Work rules:
- Work on exactly one day. Do not make batch changes or change another day.
- Make the durable curriculum update in scratch/day_data_NNN.py. Do not hand-edit the generated HTML override unless the authoring engine expressly requires it.
- Preserve every coverage.csv topic anchor: #topic-XX-overview, #topic-XX-technical, #topic-XX-problem, and #topic-XX-lab.
- Retain all four numbered parts. For every topic, supply topic-specific teaching content, a multi-layer topology SVG, one five-point failure/corrected incident SVG, eight concrete lab stages, troubleshooting, cleanup, artifact acceptance, and an explicit evidence limit.
- Use source-linked technical content and official primary documentation for mutable product, certification, quota, pricing, or exam claims.
- Clearly label supplied facts, local observations, tabletop predictions, design inferences, and open questions. Do not invent production behavior, exam outcomes, eligibility, pricing, quotas, latency, customer acceptance, credentials, payment data, or protected exam content.
- Preserve the shared site shell, navigation, day selector, progress controls, theme controls, and footer.

After editing, run:
1. python3 scripts/author_engine.py --day N
2. python3 scripts/build.py --day N
3. python3 scripts/validate.py

Fix only issues introduced by Day NNN. Then report: the Day NNN data specification changed, generated content/day-NNN-page.html, rendered days/day-NNN.html, source/lab limitations, and the checks actually run. Do not paste the full HTML page into the response.
```
