# Curriculum Page Update Prompt

Use this prompt for one GCP Architect 180-day curriculum page at a time. Replace `NNN` with the three-digit day number and `N` with the numeric day.

```text
Update Day NNN of the GCP 180-day Architect site in the repository's `gcp-180day-architect-site/` directory. Run commands from that directory unless a command is explicitly run from the repository root.

Precedence:
1. ../roadmap-180-days.md (scope, prereqs, study, practice, exit evidence)
2. ../gcp-architect-180-day-page-prompts.md (Day NNN brief, required anchors)
3. data/coverage.csv (topic-to-anchor mappings, source IDs, publisher links)
4. ../gcp-architect-roadmap-100-days.md (source topic refs, official doc links)
5. PAGE_AUTHORING_CONTRACT.md (subtopic-first schema, SVG/icon standards, 8-stage lab progression)
6. AGENTS.md & ONE_DAY_AT_A_TIME.md (serial authoring-engine workflow and handoff)

Requirements:
- Target only Day NNN. Durable specification belongs in scratch/day_data_NNN.py.
- Retain all four numbered parts and preserve every coverage anchor (#topic-XX-overview, #topic-XX-technical, #topic-XX-problem, #topic-XX-lab).
- Part 1: Overview with exactly two preview sentences per topic (symptom + business impact).
- Part 2: Subtopic-first discussion. List all subtopics at the start; explain each under its own heading covering "What it is in general", "Relevance to a cloud architect", and "Relevance to GCP" (with primary source links). End each topic with a concrete example and an explicit "Evidence limit:".
- Diagram assets: Check `assets/icons/` first. When a needed GCP or networking icon is missing, obtain an authentic service logo from Google's official Cloud architecture icon assets and add it to the local library with source/provenance recorded. For generic network components without an official asset, create a simple original SVG symbol (for example router, firewall, DNS, switch, client, or endpoint) and label it clearly; do not fabricate Google Cloud or product logos. Keep all assets local to the page and preserve accessible text labels.
- Part 2 Visuals: Topology standard SVG (1120x690 canvas, 3 non-overlapping tiers, exact vertical drops, bottom probe panel) with appropriate official GCP or generic network component icons on all nodes.
- Part 3: Field case per topic with symptoms, verbatim logs, root cause, diagnostic sequence, defensible fix, verification, residual risk, and a 5-node dual-lane incident SVG (with appropriate icons on every node, verification boundary enclosing nodes 2 & 3, FI badge, and 3-field figcaption).
- Part 4: Step-by-step lab per topic with exactly eight labeled execution stages under "Exact execution", standardized callouts, artifact acceptance, and roadmap exit evidence.
- Inline commands outside code blocks must use <kbd>...</kbd> rather than <code>...</code> to ensure clean validator pass.

Pipeline execution:
Run: python3 scripts/author_engine.py --day N && python3 scripts/build.py --day N && python3 scripts/validate.py
Do not poll or loop on task status; wait for background completion notification. Fix only issues introduced by Day NNN.

Handoff report requirements (token-optimized):
Do not re-summarize or paste full page HTML in chat. Provide only:
1. Files updated (with markdown file:// links).
2. Coverage anchors verified.
3. Roadmap exit artifact generated.
4. Validation summary (0 errors confirmed).
```
