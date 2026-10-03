# One day at a time

Use this workflow to build the 180-day site without carrying one page's assumptions into another.

## Run mode

- Set `CURRENT_DAY` to the requested day. For a single page, `TARGET_DAY = CURRENT_DAY`. A later `next` advances by one; an explicit day starts there. Stop after Day 180.
- For a batch, set a start and end day. The coordinator assigns one fresh, isolated subagent per day and runs them strictly serially: finish, build, and validate Day N before starting Day N+1. Never edit two day pages concurrently, and do not pause between days in an authorized batch.
- Each page agent receives only the compact Day N brief from `gcp-architect-180-day-page-prompts.md`; it reads the shared `PAGE_AUTHORING_CONTRACT.md`. Do not paste the full prompt catalog or unrelated roadmap sections into every task.

## Per-day steps

1. Find the Day N brief in `../gcp-architect-180-day-page-prompts.md`. It contains the source roadmap entry and the required coverage IDs. If the brief is stale, regenerate it with `python3 ../generate-day-prompts.py`.
2. In the site directory, inspect the day's `scratch/day_data_NNN.py` if present, `content/day-NNN-page.html` if present, `days/day-NNN.html`, `data/coverage.csv` rows for N, and only the components/styles needed for the change. Preserve the existing page shell and useful visuals.
3. Update `scratch/day_data_NNN.py` as the durable source. Generate or refresh the override with `python3 scripts/author_engine.py --day N`; do not hand-edit generated HTML as the durable source.
4. Build and validate only the target day: `python3 scripts/build.py --day N`, then `python3 scripts/validate.py --day N`. Repair issues introduced by this edit and rerun the required commands. Do not run a full-site build.
5. Report the data specification, generated override, rendered page, changes, checks actually run, and any unverified source or lab limitation. Do not paste page HTML into chat.

Apply `PAGE_UPDATE_PROMPT.md` on every page update. After the target-day build, run `python3 scripts/check_study_links.py --day N --report scratch/day-NNN-study-links.json` and confirm source relevance manually.

Use `PAGE_AUTHORING_CONTRACT.md` for page content, source checks, diagrams, labs, and acceptance criteria. The current roadmap is authoritative when older prompts disagree with it. An alternate Day 13 prompt is explicitly noncanonical and must not silently change the current curriculum.

For a ten-page run, this means ten isolated page contexts in sequence, not ten full copies of the authoring instructions and not ten pages in one long context. Keep the coordinator's context to the current day number, agent result, and build/validation status.

Permanent rendering rules: follow `RENDER_REVIEW.md` on every page update. Use shared styles rather than day-specific color patches, run target-day markup guards, and save `scripts/browser_render_audit.js` results for desktop/mobile in both themes plus visual diagram and copy-control checks. Fix all introduced errors before handoff.
