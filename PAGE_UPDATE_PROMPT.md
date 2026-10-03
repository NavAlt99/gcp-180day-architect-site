# Curriculum page update prompt

Use for one day. Replace N with its numeric day and NNN with its three-digit form.
Static rules come first: read `PAGE_AUTHORING_CONTRACT.md` once, use its Source
precedence and Read budget, then `ONE_DAY_AT_A_TIME.md` for serial selection.

```text
Update Day NNN in gcp-180day-architect-site/ following the canonical contract
and serial workflow. Run from that directory unless explicitly stated otherwise.
Author scratch/day_data_NNN.py using only the scoped day inputs. Preserve all
contract requirements; finish acceptance checks and fix target-introduced errors.

Run in order:
python3 scripts/author_engine.py --day N
python3 scripts/build.py --day N
python3 scripts/validate.py --day N
python3 scripts/check_study_links.py --day N --report scratch/day-NNN-study-links.json
If changing the checker, also run:
python3 -m unittest discover -s tests -p "test_check_study_links.py"

Review durable-spec coverage, subtopic explanations, exercise stages, sources,
and diagram eligibility. Run the contract's rendering acceptance checks within
its read budget. Do not treat HTTP success as source relevance or an audit pass
as proof of technical accuracy.

Handoff only:
1. Clickable paths to specification, generated override and rendered page.
2. Reviewed anchors, subtopic depth, diagram eligibility and exercise completeness.
3. Roadmap exit artifact/acceptance; distinguish instructions from artifacts
   actually produced by executed labs.
4. Checks actually run/results, structural errors, study-link report, semantic
   source review and source/lab limits. Claim zero errors only when confirmed;
   blocked/unverified links are not passes. No full-page HTML or content recap.
```
