# GCP 180-day curriculum site

## Instruction sources and precedence

For any curriculum-page task, treat these files as the authoritative source of truth, in this order:

1. `../roadmap-180-days.md` — day scope, prerequisites, study, practice, and exit evidence.
2. `../gcp-architect-180-day-page-prompts.md` — the compact day-specific brief and required anchors.
3. `data/coverage.csv` — the topic-to-anchor mapping, exit evidence, source-topic IDs, and publisher links.
4. `../gcp-architect-roadmap-100-days.md` — source-topic cross references and official documentation links.
5. `PAGE_AUTHORING_CONTRACT.md` — required teaching structure, evidence rules, SVG requirements, lab standards, and source rules.
6. `ONE_DAY_AT_A_TIME.md` — serial authoring, build, validation, and handoff workflow.

Existing HTML is rendered output, not curriculum truth. Do not infer requirements from a prior page when an authoritative input above differs.

## Required curriculum-page workflow

- Work on exactly one day at a time, in serial order. Do not use batch generation or edit multiple day pages concurrently.
- Before editing Day `N`, read its roadmap entry, generated brief, coverage rows, current `scratch/day_data_NNN.py` if present, current `content/day-NNN-page.html` if present, and the required sections of `PAGE_AUTHORING_CONTRACT.md`.
- Author the durable input in `scratch/day_data_NNN.py`. Keep page content topic-specific; do not use generic fallback prose, generic root causes, or generic lab steps in place of the day’s actual case, trade-off, and acceptance evidence.
- Generate the override with `python3 scripts/author_engine.py --day N`, then run `python3 scripts/build.py --day N` and `python3 scripts/validate.py --day N`.
- Fix only issues introduced by the target day before proceeding. Preserve the shared site shell, navigation, day selector, progress controls, theme controls, and footer.

## Page acceptance rules

- Preserve every `overview`, `technical`, `problem`, and `lab` anchor listed in `data/coverage.csv`.
- Retain the four numbered parts. Apply the conditional Diagram Generation Rule in `PAGE_AUTHORING_CONTRACT.md` to topology and incident SVGs; omit nonqualifying diagram sections. Include eight executable lab stages per topic, source-linked technical content, an explicit evidence limit, troubleshooting, cleanup, and artifact acceptance.
- Apply `PAGE_UPDATE_PROMPT.md` and the contract to every future page update: selected keyword highlights, blue bold side headings, fully explained subtopics, and exact commands or manual instructions with execution location, expected results, and evidence for each exercise stage.
- After building the target day, run `python3 scripts/check_study_links.py --day N --report scratch/day-NNN-study-links.json` and manually confirm each Further study source supports its topic. Report blocked/unverified links honestly.
- Use official primary documentation for time-sensitive product, certification, quota, price, and exam claims. Clearly distinguish supplied facts, local observations, tabletop predictions, design inferences, and open questions.
- Do not invent production behavior, exam results, eligibility, pricing, quotas, latency, or customer acceptance. Never expose credentials, protected exam content, or payment data.

## Handoff

Report the data specification, generated override, rendered page, source/lab limitations, and checks actually run. Do not paste full page HTML into chat.

Permanent rendering rules: follow `RENDER_REVIEW.md` on every page update. Use shared styles rather than day-specific color patches, run target-day markup guards, and save `scripts/browser_render_audit.js` results for desktop/mobile in both themes plus visual diagram and copy-control checks. Fix all introduced errors before handoff.
