# Permanent rendering acceptance rules

These rules preserve the fixes discovered during the Day 002 browser review.
They apply to every future page update. Do not rely on copying Day 002 HTML.

The canonical rules are in `PAGE_AUTHORING_CONTRACT.md`, sections Permanent
rendering rules, Typography and inline code, and Diagram eligibility and standards.
Use this file only for audit procedure; apply the contract's Read budget globally.

## Required browser review

1. Build only the requested day, then run `python3 scripts/validate.py --day N`.
   The authoring engine also runs these target-day markup guards automatically.
2. Run the browser audit through an approved preview without importing full
   page text or screenshots into author context. If file URLs are blocked, use
   an authorized local HTTP preview; do not bypass security. Inspect rendered
   regions only for a specific validator/audit flag, per the canonical Read budget.
3. Audit desktop and 390×844 in both themes. Review durable-spec markup and
   shared styling; on a flag, inspect the affected cards, TOC, tables, rail,
   keywords, headings or captions only.
4. Read `scripts/browser_render_audit.js` into `auditSource` and invoke its
   expression with `tab.playwright.evaluate('(' + auditSource + '\n)()')` using
   the supported browser API. Save all four results. Fix each
   error; this checks document overflow, heading style, caption contrast, SVG
   canvas clipping, scroll containment, and copy-button count.
5. Check EVERY qualifying diagram for node/icon coverage, readable text, arrows
   and evidence boundaries without overlaps. Use durable-spec review and audit
   bounds/scroll results; inspect only flagged rendered diagrams. Verify mobile
   far-edge reachability through the audit/browser control, saving compact results.
6. Click one exercise copy button; confirm it reports `Copied`. Verify all
   progress keys and the 180-day selector remain present. Do not mark the user's
   actual progress as completed during review.
7. Recheck exact study-link fragments after the final build; HTTP success is
   insufficient for fragment existence or semantic relevance. Do not assume an
   RFC has `#section-X`: older publications may use page anchors. Repair against
   the live primary source and record the access date, never guessed fragments.
8. Save audit results and screenshots of flagged regions only. Restore theme and viewport
   settings. Record manual checks and anything unverified accurately.

A successful structural check does not prove visual quality. The browser audit
also cannot prove diagram eligibility, technical accuracy, all text/node overlaps,
or source relevance. Those remain mandatory authoring and rendered review tasks.
