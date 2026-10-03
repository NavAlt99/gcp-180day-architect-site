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
- Typography: Highlight selected key terms in paragraphs with `<strong class="keyword">term</strong>` (pink text, subtle tinted background, like the Kubernetes topic example). Highlight the first meaningful use; do not mark whole sentences or commands. Make side headings/labels such as "Why today", "Where it sits", and "Why today and where it sits" blue and bold using `<strong class="side-heading">...</strong>`. Use the shared theme-aware styles in assets/site.css. Use Markdown or HTML in supported rich-text fields; plain string fields are escaped, so use part1_html for rich overview markup.
- Part 1: Overview with exactly two preview sentences per topic (symptom + business impact).
- Part 2: Subtopic-first discussion. A heading or list entry is not an explanation. Define every subtopic in plain language, expand unfamiliar acronyms on first use, describe how it works with a small concrete example, and explain the architect decision/trade-off and GCP application. Do not substitute generic relevance text for the mechanism. List all subtopics at the start; explain each under its own heading covering "What it is in general", "Relevance to a cloud architect", and "Relevance to GCP" (with primary source links). End each topic with a concrete example and an explicit "Evidence limit:".
- Diagram assets: Check `assets/icons/` first. When a needed GCP or networking icon is missing, obtain an authentic service logo from Google's official Cloud architecture icon assets and add it to the local library with source/provenance recorded. For generic network components without an official asset, create a simple original SVG symbol (for example router, firewall, DNS, switch, client, or endpoint) and label it clearly; do not fabricate Google Cloud or product logos. Keep all assets local to the page and preserve accessible text labels.
- Diagram Generation Rule: ONLY generate a diagram when the actual topic/subtopic specifically describes a multi-step sequence, a data packet traversal flow (for example NIC → kernel queues → application socket), or a request/response lifecycle. Do NOT generate diagrams for conceptual definitions, static features, or configuration topics. For a nonqualifying topic omit the diagram section entirely, including headings, wrappers, captions, and placeholder diagrams. Do not manufacture a sequence merely to justify a diagram. This rule applies to Part 2 topology and Part 3 incident diagrams. Set scenario["diagram_enabled"] = False for every nonqualifying topic; leave ARCH_DIAGRAM/ARCH_SVG_HTML empty when no Part 2 flow qualifies. For a qualifying incident set diagram_enabled = True.
- Qualifying diagrams: Explain the numbered flow in nearby prose; use arrows with meaningful transitions and readable accessible labels. Use the topology standard (1120x690 canvas, non-overlapping tiers, exact vertical drops, bottom probe panel) only where that layout fits the actual flow; a simple linear packet/lifecycle SVG is valid. Reuse appropriate local icons.
- Part 3: Field case per topic with symptoms, verbatim logs, root cause, diagnostic sequence, defensible fix, verification, residual risk, and, only when eligible under the Diagram Generation Rule, a 5-node dual-lane incident SVG (with appropriate icons on every node, verification boundary enclosing nodes 2 & 3, FI badge, and 3-field figcaption).
- Part 4: Step-by-step lab per topic with exactly eight labeled execution stages under "Exact execution", standardized callouts, artifact acceptance, and roadmap exit evidence.
- Exercise completeness: Each of the eight stages must state where to run it (local terminal, Cloud Shell, GCP VM terminal, Console, or tabletop), exact ordered actions, explicit inputs/file contents, expected observable result, and evidence to save. Provide copyable commands or complete Terraform configuration with init/plan/apply/inspect/destroy where appropriate. Define all variables, prerequisites, tools, file paths, and dependencies before use. When commands/Terraform cannot perform the task, give numbered Console navigation or local worksheet/editor instructions with exact fields, values, expected result, and a relevant official procedure link; a link alone is insufficient. Explain local-machine preparation and GCP steps where both environments are involved. For local-only work, state what GCP behavior remains untested rather than inventing deployment. Include bounded failure recovery and cleanup of only lab-owned resources.
- Study links: Run the target-day link check below after building. It tests reachability, redirects, and exact fragments, not semantic correctness. Open each Further study source and confirm it explains the stated topic/subtopic and matches the link label. Prefer the specific official documentation section. Repair broken, irrelevant, and misleading redirect targets; record access date and unresolved access restrictions accurately.
- Inline commands outside code blocks must use <kbd>...</kbd> rather than <code>...</code> to ensure clean validator pass.


Permanent rendering rules: follow `RENDER_REVIEW.md` on every page update. Use shared styles rather than day-specific color patches, run target-day markup guards, and save `scripts/browser_render_audit.js` results for desktop/mobile in both themes plus visual diagram and copy-control checks. Fix all introduced errors before handoff.

Pipeline execution:
Run in order:
python3 scripts/author_engine.py --day N
python3 scripts/build.py --day N
python3 scripts/validate.py --day N
python3 scripts/check_study_links.py --day N --report scratch/day-NNN-study-links.json
For changes to the link checker, also run: python3 -m unittest discover -s tests -p "test_check_study_links.py"
Review subtopic coverage, all eight exercise stages, highlighting/blue bold labels in both themes, and diagram eligibility on the rendered target page. Do not treat HTTP success as proof of topic relevance.
Do not poll or loop on task status; wait for background completion notification. Fix only issues introduced by Day NNN.

Handoff report requirements (token-optimized):
Do not re-summarize or paste full page HTML in chat. Provide only:
1. Data specification, generated override, and rendered page (with clickable local file links).
2. Coverage anchors, described subtopics, diagram eligibility, and exercise completeness reviewed.
3. Roadmap exit artifact/acceptance requirements; distinguish authored instructions from artifacts actually produced by running labs.
4. Checks actually run, structural errors, study-link report, semantic source review, and source/lab limitations. Claim 0 errors only if confirmed; blocked/unverified links are not passes.
```
