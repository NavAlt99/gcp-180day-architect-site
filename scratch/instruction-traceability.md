# Instruction requirement traceability — Phase A

Originals obtained with `git show HEAD:<file>` after Phase 0 (unchanged from starting commit e729d87). Exact original text is retained under `scratch/baseline/original-*`; it is audit evidence, excluded from routine day-agent reads. Every nonempty requirement line, including all clauses in long bullet/paragraph lines, has a home below. Headings/code fences/blank lines are not requirements.

Mappings name canonical contract sections unless a destination filename is explicit. “Supersedes” records a user-requested policy correction, not a silently omitted requirement. All original content is retained in baseline files.

## Explicit decisions

- Coverage rows supply exact anchors; generic key wording removed from live instructions.
- Literal logs retain verbatim records, labeled supplied/illustrative/local-observed; no invented production observations.
- Copyable commands use pre/code; inline commands use kbd; non-command filenames/terms use code.
- Exactly two preview sentences occur in Part 1 only, in topics[].preview or rich part1_html. Part 2 has no such length restriction. Confirmed by narrow read of author_engine.py Part 1/2: preview emitted only in Part 1; sentence count is not automatically enforced by existing engine. Engine unchanged.
- New Read budget replaces unconditional generated-HTML/template-page reads everywhere, including RENDER_REVIEW.md. Audits still run; full rendered context is excluded and only flagged regions are inspected. Durable-spec, icon, source, and audit acceptance checks remain mandatory.
- Explicit user-approved depth floor: conceptual depth may increase but must never decrease; scheduled time never caps or shortens explanations. Add required mechanisms/examples/lab detail and report time overruns. Token savings are structural only, never shorter prose/fewer subtopics/fewer examples/thinner labs; existing explanations may only gain or correct depth, never be condensed. The original "proportional to scheduled study time" rule is intentionally superseded. This replaces the earlier current-user-allowance decision.
- Serial multi-day subagent instruction applies only to an explicitly authorized multi-day page run, not this maintenance task.
- Phase B delivered SPEC_SCHEMA.md, SPEC_DEFAULTS.json and the non-overwriting coverage skeleton. Read budget uses these instead of engine internals; legacy single-file loading remains. The prior forward reference is now resolved.
- RENDER_REVIEW.md existed; no reconstruction. Its unique audit procedure remains, with global read-policy correction.
- Evidence sequence diagrams inside Part 3 are allowed with diagram_enabled False when they qualify under the Diagram Generation Rule and carry a scope caption; they never replace the five-node incident diagram when the case qualifies.

## Requirement map

| Original file:line | Original requirement locator (full text in baseline) | New home / disposition |
|---|---|---|
| AGENTS.md:5 | For any curriculum-page task, treat these files as the authoritative source of truth, in this order: | Source precedence |
| AGENTS.md:7 | 1. ../roadmap-180-days.md — day scope, prerequisites, study, practice, and exit evidence. | Source precedence |
| AGENTS.md:8 | 2. ../gcp-architect-180-day-page-prompts.md — the compact day-specific brief and required anchors. | Source precedence |
| AGENTS.md:9 | 3. data/coverage.csv — the topic-to-anchor mapping, exit evidence, source-topic IDs, and publisher links. | Source precedence |
| AGENTS.md:10 | 4. ../gcp-architect-roadmap-100-days.md — source-topic cross references and official documentation links. | Source precedence |
| AGENTS.md:11 | 5. PAGE_AUTHORING_CONTRACT.md — required teaching structure, evidence rules, SVG requirements, lab standards, and source rules. | Source precedence |
| AGENTS.md:12 | 6. ONE_DAY_AT_A_TIME.md — serial authoring, build, validation, and handoff workflow. | Source precedence |
| AGENTS.md:14 | Existing HTML is rendered output, not curriculum truth. Do not infer requirements from a prior page when an authoritative input above differs. | Source precedence |
| AGENTS.md:18 | - Work on exactly one day at a time, in serial order. Do not use batch generation or edit multiple day pages concurrently. | ONE_DAY_AT_A_TIME.md: Serial run selection |
| AGENTS.md:19 | - Before editing Day N, read its roadmap entry, generated brief, coverage rows, current scratch/day_data_NNN.py if present, current content/… | Read budget [explicitly supersedes unconditional HTML reads] |
| AGENTS.md:20 | - Author the durable input in scratch/day_data_NNN.py. Keep page content topic-specific; do not use generic fallback prose, generic root causes… | Content invariants |
| AGENTS.md:21 | - Generate the override with python3 scripts/author_engine.py --day N, then run python3 scripts/build.py --day N and python3 scripts/validat… | PAGE_UPDATE_PROMPT.md: command sequence |
| AGENTS.md:22 | - Fix only issues introduced by the target day before proceeding. Preserve the shared site shell, navigation, day selector, progress controls, th… | Content invariants |
| AGENTS.md:26 | - Preserve every overview, technical, problem, and lab anchor listed in data/coverage.csv. | Content invariants |
| AGENTS.md:27 | - Retain the four numbered parts. Apply the conditional Diagram Generation Rule in PAGE_AUTHORING_CONTRACT.md to topology and incident SVGs; om… | Content invariants; Part 4; Diagram eligibility and standards; Sources and evidence |
| AGENTS.md:28 | - Apply PAGE_UPDATE_PROMPT.md and the contract to every future page update: selected keyword highlights, blue bold side headings, fully explain… | Typography and inline code; Part 2; Part 4 |
| AGENTS.md:29 | - After building the target day, run python3 scripts/check_study_links.py --day N --report scratch/day-NNN-study-links.json and manually confir… | Sources and evidence; PAGE_UPDATE_PROMPT.md: command sequence |
| AGENTS.md:30 | - Use official primary documentation for time-sensitive product, certification, quota, price, and exam claims. Clearly distinguish supplied facts… | Sources and evidence |
| AGENTS.md:31 | - Do not invent production behavior, exam results, eligibility, pricing, quotas, latency, or customer acceptance. Never expose credentials, prote… | Sources and evidence |
| AGENTS.md:35 | Report the data specification, generated override, rendered page, source/lab limitations, and checks actually run. Do not paste full page HTML in… | PAGE_UPDATE_PROMPT.md: Handoff |
| AGENTS.md:37 | Permanent rendering rules: follow RENDER_REVIEW.md on every page update. Use shared styles rather than day-specific color patches, run target-d… | Permanent rendering rules; RENDER_REVIEW.md: procedure; Read budget |
| ONE_DAY_AT_A_TIME.md:3 | Use this workflow to build the 180-day site without carrying one page's assumptions into another. | Day-specific execution and handoff |
| ONE_DAY_AT_A_TIME.md:7 | - Set CURRENT_DAY to the requested day. For a single page, TARGET_DAY = CURRENT_DAY. A later next advances by one; an explicit day starts t… | ONE_DAY_AT_A_TIME.md: Serial run selection |
| ONE_DAY_AT_A_TIME.md:8 | - For a batch, set a start and end day. The coordinator assigns one fresh, isolated subagent per day and runs them strictly serially: finish, bui… | ONE_DAY_AT_A_TIME.md: Serial run selection [authorized multi-day run remains serial] |
| ONE_DAY_AT_A_TIME.md:9 | - Each page agent receives only the compact Day N brief from gcp-architect-180-day-page-prompts.md; it reads the shared PAGE_AUTHORING_CONTRAC… | Read budget; ONE_DAY_AT_A_TIME.md: Serial run selection |
| ONE_DAY_AT_A_TIME.md:13 | 1. Find the Day N brief in ../gcp-architect-180-day-page-prompts.md. It contains the source roadmap entry and the required coverage IDs. If the… | ONE_DAY_AT_A_TIME.md: Per-day preparation |
| ONE_DAY_AT_A_TIME.md:14 | 2. In the site directory, inspect the day's scratch/day_data_NNN.py if present, content/day-NNN-page.html if present, days/day-NNN.html, d… | Read budget; Content invariants [unconditional rendered/spec-engine reads superseded] |
| ONE_DAY_AT_A_TIME.md:15 | 3. Update scratch/day_data_NNN.py as the durable source. Generate or refresh the override with python3 scripts/author_engine.py --day N; do n… | Content invariants; PAGE_UPDATE_PROMPT.md: command sequence |
| ONE_DAY_AT_A_TIME.md:16 | 4. Build and validate only the target day: python3 scripts/build.py --day N, then python3 scripts/validate.py --day N. Repair issues introduc… | Content invariants; PAGE_UPDATE_PROMPT.md: command sequence |
| ONE_DAY_AT_A_TIME.md:17 | 5. Report the data specification, generated override, rendered page, changes, checks actually run, and any unverified source or lab limitation. D… | PAGE_UPDATE_PROMPT.md: Handoff |
| ONE_DAY_AT_A_TIME.md:19 | Apply PAGE_UPDATE_PROMPT.md on every page update. After the target-day build, run python3 scripts/check_study_links.py --day N --report scratc… | Sources and evidence; PAGE_UPDATE_PROMPT.md: command sequence |
| ONE_DAY_AT_A_TIME.md:21 | Use PAGE_AUTHORING_CONTRACT.md for page content, source checks, diagrams, labs, and acceptance criteria. The current roadmap is authoritative w… | Source precedence |
| ONE_DAY_AT_A_TIME.md:23 | For a ten-page run, this means ten isolated page contexts in sequence, not ten full copies of the authoring instructions and not ten pages in one… | ONE_DAY_AT_A_TIME.md: Serial run selection |
| ONE_DAY_AT_A_TIME.md:25 | Permanent rendering rules: follow RENDER_REVIEW.md on every page update. Use shared styles rather than day-specific color patches, run target-d… | Permanent rendering rules; RENDER_REVIEW.md: procedure; Read budget |
| PAGE_UPDATE_PROMPT.md:3 | Use this prompt for one GCP Architect 180-day curriculum page at a time. Replace NNN with the three-digit day number and N with the numeric d… | PAGE_UPDATE_PROMPT.md: invocation |
| PAGE_UPDATE_PROMPT.md:6 | Update Day NNN of the GCP 180-day Architect site in the repository's gcp-180day-architect-site/ directory. Run commands from that directory unl… | PAGE_UPDATE_PROMPT.md: invocation |
| PAGE_UPDATE_PROMPT.md:8 | Precedence: | Source precedence |
| PAGE_UPDATE_PROMPT.md:9 | 1. ../roadmap-180-days.md (scope, prereqs, study, practice, exit evidence) | Source precedence |
| PAGE_UPDATE_PROMPT.md:10 | 2. ../gcp-architect-180-day-page-prompts.md (Day NNN brief, required anchors) | Source precedence |
| PAGE_UPDATE_PROMPT.md:11 | 3. data/coverage.csv (topic-to-anchor mappings, source IDs, publisher links) | Source precedence |
| PAGE_UPDATE_PROMPT.md:12 | 4. ../gcp-architect-roadmap-100-days.md (source topic refs, official doc links) | Source precedence |
| PAGE_UPDATE_PROMPT.md:13 | 5. PAGE_AUTHORING_CONTRACT.md (subtopic-first schema, SVG/icon standards, 8-stage lab progression) | Source precedence |
| PAGE_UPDATE_PROMPT.md:14 | 6. AGENTS.md & ONE_DAY_AT_A_TIME.md (serial authoring-engine workflow and handoff) | Source precedence |
| PAGE_UPDATE_PROMPT.md:16 | Requirements: | Content invariants |
| PAGE_UPDATE_PROMPT.md:17 | - Target only Day NNN. Durable specification belongs in scratch/day_data_NNN.py. | Content invariants |
| PAGE_UPDATE_PROMPT.md:18 | - Retain all four numbered parts and preserve every coverage anchor (#topic-XX-overview, #topic-XX-technical, #topic-XX-problem, #topic-XX-lab). | Content invariants |
| PAGE_UPDATE_PROMPT.md:19 | - Typography: Highlight selected key terms in paragraphs with <strong class="keyword">term</strong> (pink text, subtle tinted background, like … | Typography and inline code |
| PAGE_UPDATE_PROMPT.md:20 | - Part 1: Overview with exactly two preview sentences per topic (symptom + business impact). | Part 1; Part 2 [two-sentence location clarified] |
| PAGE_UPDATE_PROMPT.md:21 | - Part 2: Subtopic-first discussion. A heading or list entry is not an explanation. Define every subtopic in plain language, expand unfamiliar ac… | Part 2 |
| PAGE_UPDATE_PROMPT.md:22 | - Diagram assets: Check assets/icons/ first. When a needed GCP or networking icon is missing, obtain an authentic service logo from Google's of… | Diagram icons |
| PAGE_UPDATE_PROMPT.md:23 | - Diagram Generation Rule: ONLY generate a diagram when the actual topic/subtopic specifically describes a multi-step sequence, a data packet tra… | Diagram eligibility and standards |
| PAGE_UPDATE_PROMPT.md:24 | - Qualifying diagrams: Explain the numbered flow in nearby prose; use arrows with meaningful transitions and readable accessible labels. Use the … | Diagram eligibility and standards |
| PAGE_UPDATE_PROMPT.md:25 | - Part 3: Field case per topic with symptoms, verbatim logs, root cause, diagnostic sequence, defensible fix, verification, residual risk, and, o… | Part 3; Diagram eligibility and standards [labeled literal logs] |
| PAGE_UPDATE_PROMPT.md:26 | - Part 4: Step-by-step lab per topic with exactly eight labeled execution stages under "Exact execution", standardized callouts, artifact accepta… | Part 4 |
| PAGE_UPDATE_PROMPT.md:27 | - Exercise completeness: Each of the eight stages must state where to run it (local terminal, Cloud Shell, GCP VM terminal, Console, or tabletop)… | Part 4 |
| PAGE_UPDATE_PROMPT.md:28 | - Study links: Run the target-day link check below after building. It tests reachability, redirects, and exact fragments, not semantic correctnes… | Sources and evidence |
| PAGE_UPDATE_PROMPT.md:29 | - Inline commands outside code blocks must use <kbd>...</kbd> rather than <code>...</code> to ensure clean validator pass. | Typography and inline code |
| PAGE_UPDATE_PROMPT.md:32 | Permanent rendering rules: follow RENDER_REVIEW.md on every page update. Use shared styles rather than day-specific color patches, run target-d… | Permanent rendering rules; RENDER_REVIEW.md: procedure; Read budget |
| PAGE_UPDATE_PROMPT.md:34 | Pipeline execution: | PAGE_UPDATE_PROMPT.md: command sequence |
| PAGE_UPDATE_PROMPT.md:35 | Run in order: | PAGE_UPDATE_PROMPT.md: command sequence |
| PAGE_UPDATE_PROMPT.md:36 | python3 scripts/author_engine.py --day N | PAGE_UPDATE_PROMPT.md: command sequence |
| PAGE_UPDATE_PROMPT.md:37 | python3 scripts/build.py --day N | PAGE_UPDATE_PROMPT.md: command sequence |
| PAGE_UPDATE_PROMPT.md:38 | python3 scripts/validate.py --day N | PAGE_UPDATE_PROMPT.md: command sequence |
| PAGE_UPDATE_PROMPT.md:39 | python3 scripts/check_study_links.py --day N --report scratch/day-NNN-study-links.json | PAGE_UPDATE_PROMPT.md: command sequence |
| PAGE_UPDATE_PROMPT.md:40 | For changes to the link checker, also run: python3 -m unittest discover -s tests -p "test_check_study_links.py" | PAGE_UPDATE_PROMPT.md: checker tests; Sources and evidence |
| PAGE_UPDATE_PROMPT.md:41 | Review subtopic coverage, all eight exercise stages, highlighting/blue bold labels in both themes, and diagram eligibility on the rendered target… | Part 2; Part 4; Typography and inline code; Diagram eligibility and standards; Permanent rendering rules; Read budget; Sources and evidence |
| PAGE_UPDATE_PROMPT.md:42 | Do not poll or loop on task status; wait for background completion notification. Fix only issues introduced by Day NNN. | Day-specific execution and handoff; Content invariants |
| PAGE_UPDATE_PROMPT.md:44 | Handoff report requirements (token-optimized): | PAGE_UPDATE_PROMPT.md: Handoff |
| PAGE_UPDATE_PROMPT.md:45 | Do not re-summarize or paste full page HTML in chat. Provide only: | PAGE_UPDATE_PROMPT.md: Handoff |
| PAGE_UPDATE_PROMPT.md:46 | 1. Data specification, generated override, and rendered page (with clickable local file links). | PAGE_UPDATE_PROMPT.md: Handoff item 1 |
| PAGE_UPDATE_PROMPT.md:47 | 2. Coverage anchors, described subtopics, diagram eligibility, and exercise completeness reviewed. | PAGE_UPDATE_PROMPT.md: Handoff item 2 |
| PAGE_UPDATE_PROMPT.md:48 | 3. Roadmap exit artifact/acceptance requirements; distinguish authored instructions from artifacts actually produced by running labs. | PAGE_UPDATE_PROMPT.md: Handoff item 3 |
| PAGE_UPDATE_PROMPT.md:49 | 4. Checks actually run, structural errors, study-link report, semantic source review, and source/lab limitations. Claim 0 errors only if confirme… | PAGE_UPDATE_PROMPT.md: Handoff item 4 |
| PAGE_AUTHORING_CONTRACT.md:3 | Use this contract with one generated day brief from gcp-architect-180-day-page-prompts.md. The roadmap entry in that brief is the curriculum so… | Source precedence; Day-specific execution and handoff |
| PAGE_AUTHORING_CONTRACT.md:7 | - Read the day's roadmap entry, generated brief, coverage rows, durable data specification if present, rendered page if present, and only the CSS… | Read budget [explicitly supersedes unconditional rendered reads] |
| PAGE_AUTHORING_CONTRACT.md:8 | - Preserve the existing HTML shell, selector, theme controls, navigation, progress controls, footer, and useful visuals. Author the durable speci… | Content invariants; PAGE_UPDATE_PROMPT.md: command sequence |
| PAGE_AUTHORING_CONTRACT.md:9 | - Keep the page focused on the day's Study, Practice, and Exit evidence. Do not add products or deploy alternatives merely because they are named… | Source precedence |
| PAGE_AUTHORING_CONTRACT.md:10 | - Write concise, non-repetitive teaching prose. Define the mechanism, ownership/boundary, a meaningful limit or trade-off, and the observable evi… | Content invariants [explicit user-approved depth floor intentionally supersedes original proportional-to-scheduled-time rule; non-repetitive remains without reducing depth] |
| PAGE_AUTHORING_CONTRACT.md:14 | Retain the site's four numbered parts and every topic ID/anchor listed in the coverage rows: #key-overview, #key-technical, #key-problem, a… | Content invariants [exact coverage anchors replace generic key wording] |
| PAGE_AUTHORING_CONTRACT.md:16 | 1. **Topics of the day:** For each mapped topic, explain what it is, why it belongs today, and where it sits. End that topic with exactly two pre… | Part 1 |
| PAGE_AUTHORING_CONTRACT.md:17 | 2. **Technical discussion:** Explain the relevant control/data flow, ownership, boundary, limit, failure signal, and trade-off. Include an access… | Part 2; Diagram eligibility and standards; Sources and evidence |
| PAGE_AUTHORING_CONTRACT.md:18 | 3. **Problem and solution:** Give one clearly labeled example per topic. Include symptoms/evidence, business and operational constraints, causal … | Part 3; Diagram eligibility and standards |
| PAGE_AUTHORING_CONTRACT.md:19 | 4. **Step-by-step lab:** Provide a named exercise for each topic or an integrated exercise with an explicit checkpoint for each. Every exercise m… | Part 4 |
| PAGE_AUTHORING_CONTRACT.md:21 | All commands and multi-line file contents belong in <pre><code> blocks with the site's working copy control. Keep non-command filenames and sho… | Typography and inline code; Sources and evidence |
| PAGE_AUTHORING_CONTRACT.md:25 | - Highlight selected key terms at their first meaningful use in paragraphs with <strong class="keyword">...</strong>. Use the shared pink text … | Typography and inline code |
| PAGE_AUTHORING_CONTRACT.md:26 | - Side headings and labels such as “Why today”, “Where it sits”, and “Why today and where it sits” must be blue and bold: <strong class="side-he… | Typography and inline code |
| PAGE_AUTHORING_CONTRACT.md:27 | - Every subtopic needs a beginner-readable definition, expanded unfamiliar acronyms, a mechanism explanation, and a concrete example before its a… | Part 2 |
| PAGE_AUTHORING_CONTRACT.md:31 | Follow RENDER_REVIEW.md for shared theme fixes and mandatory browser acceptance. Do not put reusable panel/heading/caption fixes in individual … | Permanent rendering rules; RENDER_REVIEW.md: procedure; Read budget |
| PAGE_AUTHORING_CONTRACT.md:35 | ONLY generate a diagram if the actual topic/subtopic specifically describes a multi-step sequence, a data packet traversal flow (for example NIC … | Diagram eligibility and standards |
| PAGE_AUTHORING_CONTRACT.md:37 | This rule governs both Part 2 and Part 3 and supersedes earlier blanket topology/incident requirements. For each topic explicitly set scenario["… | Diagram eligibility and standards |
| PAGE_AUTHORING_CONTRACT.md:41 | Each of the eight stages must provide: | Part 4 |
| PAGE_AUTHORING_CONTRACT.md:43 | 1. Execution location: local terminal, Cloud Shell, terminal inside a GCP VM, Console, or local/tabletop worksheet; name the shell/OS and tools w… | Part 4 |
| PAGE_AUTHORING_CONTRACT.md:44 | 2. Ordered actions with copyable commands and full required file contents, or numbered manual instructions with exact navigation, fields, and val… | Part 4 |
| PAGE_AUTHORING_CONTRACT.md:45 | 3. Expected observable result and a concrete artifact/output to save, with a stop condition or recovery instruction where needed. Environment-dep… | Part 4; Typography and inline code |
| PAGE_AUTHORING_CONTRACT.md:47 | For tasks unavailable through commands or Terraform, provide a relevant official procedure link AND complete step-by-step Console/editor/workshee… | Part 4 |
| PAGE_AUTHORING_CONTRACT.md:51 | - At the start of each topic's Technical discussion, list all subtopics covered by that topic before explaining any of them. Derive this complete… | Part 2 |
| PAGE_AUTHORING_CONTRACT.md:52 | - Discuss every listed subtopic in the same order, under its own descriptive heading. For each subtopic, explicitly cover **What it is in general… | Part 2 |
| PAGE_AUTHORING_CONTRACT.md:53 | - Use a concrete topic-specific example to connect the general concept to the architect's decision and its GCP application. Explain prerequisites… | Part 2 |
| PAGE_AUTHORING_CONTRACT.md:54 | - Preserve the topic's existing coverage anchors and the four numbered parts. Subtopic headings supplement the mapped topic structure. A subtopic… | Content invariants; Part 2 |
| PAGE_AUTHORING_CONTRACT.md:58 | - Reuse the local library in assets/icons/; consult assets/icons/manifest.json for mappings and provenance, assets/icons/index.html for pre… | Diagram icons |
| PAGE_AUTHORING_CONTRACT.md:59 | - Every diagram, including topology and incident SVGs, must include an appropriate logo or icon on every node alongside its readable text label. … | Diagram icons |
| PAGE_AUTHORING_CONTRACT.md:60 | - Use an appropriate concept icon for non-component nodes such as an event, decision, policy, artifact, or outcome. Label these explicitly so the… | Diagram icons |
| PAGE_AUTHORING_CONTRACT.md:61 | - Use official Google Cloud architecture icon assets for GCP logos, preserve their proportions and colors, and record their source. Prefer local … | Diagram icons |
| PAGE_AUTHORING_CONTRACT.md:62 | - If a required official GCP icon is missing from the local library, obtain the authentic asset from Google's official Cloud architecture icon re… | Diagram icons |
| PAGE_AUTHORING_CONTRACT.md:63 | - Keep icons inside their nodes with enough space for readable labels, arrows, and badges. Retain the required topology/incident layout, unique S… | Diagram icons; Diagram eligibility and standards |
| PAGE_AUTHORING_CONTRACT.md:64 | - Before completing a page, check every diagram for node icon coverage, correct service-to-icon mapping, resolved asset references, and absence o… | Diagram icons; Diagram eligibility and standards; Permanent rendering rules; Read budget |
| PAGE_AUTHORING_CONTRACT.md:68 | Use primary documentation for product behavior that can change. Open each cited section and confirm the fragment resolves before describing it as… | Sources and evidence |
| PAGE_AUTHORING_CONTRACT.md:70 | After building the target day, run python3 scripts/check_study_links.py --day N --report scratch/day-NNN-study-links.json. The check covers Fur… | Sources and evidence; PAGE_UPDATE_PROMPT.md: command sequence/checker tests |
| PAGE_AUTHORING_CONTRACT.md:72 | Build only the target day with python3 scripts/build.py --day N, then run python3 scripts/validate.py. Review the final page for the four par… | Content invariants; Permanent rendering rules; PAGE_UPDATE_PROMPT.md: command sequence/Handoff; Read budget |

Coverage check: 109 original requirement lines mapped; 0 unmapped. Long lines map to multiple sections when their clauses span topics. No requirement source was deleted. All superseded read policies remain archived and explicitly explained above.

User-approved Phase B handoff clarification: concise reporting stays separate from depth; item 5 requires git diff on the durable spec and an explicit no-explanatory-prose-removal statement. The depth floor itself is unchanged.

Phase C implementation homes: shared assembly is scratch/day_helpers.py; explicit Day 002 context remains scratch/day_data_002.py. SPEC_SCHEMA.md documents all new lab_defaults fields and structural-only defaulting. Engine TODO lab slots reject before writes; new specs opt in, while legacy single-file omissions remain compatible. No original acceptance requirement was replaced; no explanatory prose was removed. Option 3 implemented; 4/5/6/7/10 deferred per the user.
