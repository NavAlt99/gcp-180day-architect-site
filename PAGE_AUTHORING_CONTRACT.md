# Day-page authoring contract

Use this contract with one generated day brief from `gcp-architect-180-day-page-prompts.md`. The roadmap entry in that brief is the curriculum source of truth. Work on one day only.

## Efficient context and edits

- Read the day's roadmap entry, its coverage rows, its existing override/page, and only the CSS/JavaScript rules needed for components you touch. Do not load the 180-day prompt file, the full roadmap, unrelated day pages, or the whole selector markup into working context.
- Preserve the existing HTML shell, selector, theme controls, navigation, progress controls, footer, and useful visuals. Edit `content/day-NNN-page.html`; initialize it from the current rendered page only if the override is absent. Build only that day.
- Keep the page focused on the day's Study, Practice, and Exit evidence. Do not add products or deploy alternatives merely because they are named for comparison. Use synthetic Brightloaf examples only when useful.
- Write concise, non-repetitive teaching prose. Define the mechanism, ownership/boundary, a meaningful limit or trade-off, and the observable evidence. Keep the depth proportional to the scheduled study time.

## Required content

Retain the site's four numbered parts and every topic ID/anchor listed in the coverage rows: `#key-overview`, `#key-technical`, `#key-problem`, and `#key-lab`.

1. **Topics of the day:** For each mapped topic, explain what it is, why it belongs today, and where it sits. End that topic with exactly two preview sentences: one concrete symptom or decision, then its user/business effect.
2. **Technical discussion:** Explain the relevant control/data flow, ownership, boundary, limit, failure signal, and trade-off. Include an accessible architecture-path table and at least one day-specific SVG diagram. The diagram needs a unique accessible title/description, readable labels, a horizontally scrollable wrapper, and a caption stating scope and what it does not prove. End each topic with a verified authoritative written source linked to a real relevant section. Add videos only when the segment and timestamp have actually been checked; never invent them.
3. **Problem and solution:** Give one clearly labeled example per topic. Include symptoms/evidence, business and operational constraints, causal root-cause reasoning, a defensible fix, verification, and residual risk. Keep supplied facts separate from inference. Include one additional incident SVG per topic, with failed and corrected paths visibly distinguished and an in-diagram verification boundary. Do not portray an example or prediction as an observed production incident. For event replay, preserve one business fulfillment per order.
4. **Step-by-step lab:** Provide a named exercise for each topic or an integrated exercise with an explicit checkpoint for each. Include goal/result, mode/limits, prerequisites, preflight, exact steps, expected state, verification, troubleshooting, cleanup, and artifact acceptance tied to the roadmap's Exit evidence. For cloud changes, verify identity, project, APIs, permissions, location, inventory, billing assumptions, and bounded cost first; clean up in reverse dependency order. Prefer a local/tabletop lab when it satisfies the Practice. Never expose credentials.

All commands and multi-line file contents belong in `<pre><code>` blocks with the site's working copy control. Keep non-command filenames and short technical terms inline. All expected cloud output must be labeled illustrative when environment-dependent. Distinguish documentation, local observation, and tabletop prediction.

## Sources and completion

Use primary documentation for product behavior that can change. Open each cited section and confirm the fragment resolves before describing it as verified; include descriptive link text and access date. A second written source is preferable to an unverified video. Do not invent quotas, prices, outputs, version details, or causal claims.

Build only the target day with `python3 scripts/build.py --day N`, then run `python3 scripts/validate.py`. Review the final page for the four parts, required anchors, valid local links, complete day selector, working copy blocks, unique SVG IDs/ARIA references, responsive figure scrolling, and accurate exit evidence. Fix only issues caused by this edit. Do not run a full-site build. Report what changed, checks actually run, and any source or lab limitation; do not paste the HTML into chat.
