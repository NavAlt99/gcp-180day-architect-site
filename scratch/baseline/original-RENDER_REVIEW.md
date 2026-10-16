# Permanent rendering acceptance rules

These rules preserve the fixes discovered during the Day 002 browser review.
They apply to every future page update. Do not rely on copying Day 002 HTML.

## Shared fixes

- Use `assets/site.css` for themes. Do not add per-day `<style>` fixes for panel,
  heading, keyword, or caption colors. Foundation cards, TOC, tables, and rail
  tiles must use light panels in light mode; preserve the active rail indicator.
- Diagrams intentionally retain dark canvases. Their captions must stay light
  in both themes, rather than inheriting light-mode dark muted text.
- All subtopic headings and teaching side labels must be blue and bold. Selected
  prose keywords use the shared theme-aware pink highlight.
- Place wide SVGs inside a contained horizontal scroll wrapper. Do not hide
  inaccessible diagram content or shrink labels until unreadable. Do not mask
  document overflow with `body { overflow-x: hidden }`.
- Every SVG must have a viewBox, role=img, unique referenced title/description
  IDs, local icons, and an evidence caption. Shorten or wrap long labels; inspect
  text inside individual nodes as well as the overall canvas.
- Copyable blocks use `<pre><code>…</code></pre>`, with the shared JS attached.

## Required browser review

1. Build only the requested day, then run `python3 scripts/validate.py --day N`.
   The authoring engine also runs these target-day markup guards automatically.
2. Open the rendered page using an approved browser preview. If file URLs are
   blocked, use an authorized local HTTP preview; do not bypass security.
3. At desktop and 390×844, inspect both light and dark themes. Check cards, TOC,
   tables, rail, selected keywords, teaching headings, and diagram captions.
4. Read `scripts/browser_render_audit.js` into `auditSource` and invoke its
   expression with `tab.playwright.evaluate('(' + auditSource + '\n)()')` using
   the supported browser API. Save all four results. Fix each
   error; this checks document overflow, heading style, caption contrast, SVG
   canvas clipping, scroll containment, and copy-button count.
5. Visually inspect EVERY qualifying diagram: text must fit its nodes; labels,
   arrows, and evidence boundaries must be readable without overlapping. On
   mobile, scroll each wide diagram to its far edge and verify it is reachable.
6. Click one exercise copy button; confirm it reports `Copied`. Verify all
   progress keys and the 180-day selector remain present. Do not mark the user's
   actual progress as completed during review.
7. Recheck exact study-link fragments after the final build; HTTP success is
   insufficient for fragment existence or semantic relevance. Do not assume an
   RFC has `#section-X`: older publications may use page anchors. Repair against
   the live primary source and record the access date, never guessed fragments.
8. Save screenshots and audit results. Restore the theme and temporary viewport
   settings. Record manual checks and anything unverified accurately.

A successful structural check does not prove visual quality. The browser audit
also cannot prove diagram eligibility, technical accuracy, all text/node overlaps,
or source relevance. Those remain mandatory authoring and rendered review tasks.
