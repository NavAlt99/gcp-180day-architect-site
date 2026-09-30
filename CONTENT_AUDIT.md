# Content audit — 180-day site

This audit reads all 180 rendered day pages and all 504 topic sections. It checks template provenance and obvious mismatches, not the technical accuracy of a matched template. The site passes structural navigation checks but **does not pass a topic-level teaching review**.

- 469 / 504 technical discussions outside the authored lessons come from shared domain templates; 14 contain the generic 'input, actor, control boundary' fallback.
- 469 / 504 scenarios outside the authored lessons come from shared templates; 36 use the same inserted-title Brightloaf problem.
- 43 / 504 labs use the same three-column worksheet; 194 topic labs include shell command blocks and 353 include any copyable code or fixture block.
- 43 labs say no cloud resources or credentials are needed, including cloud-setup and managed-service days.
- 0 / 504 publisher links have a verified topic-level section or video timestamp in the coverage manifest.
- 1 headings look like roadmap instructions or caveats rather than a subject to teach. This is a heuristic lower bound.

The common cause is the generator: it splits each Study line at semicolons, treats every resulting clause as a topic, matches keywords to broad explanation templates, and falls back to architecture boilerplate when there is no match. Its ordinary-day case and worksheet are then reused with the title inserted. Matching a keyword does **not** establish that the discussion fits the exact topic or stage.

Examples observed in rendered pages:

- Day 18 previously paired trial-credit material with generic architecture text and a no-cloud worksheet. Its three topics now have authored definitions, failure cases and Console walkthroughs; the remaining days still require the same treatment.
- Day 42 names Kubernetes architecture and cluster choices, but all three labs are the same worksheet, with no cluster-specific exercise or observable check.
- Day 68's business requirements get generic request-path language instead of a stakeholder discovery method and worked requirement trace.
- The roadmap's Day 175–179 caveat about review versus implementation was previously made into a topic; it is now excluded from the topic list.
- Day 180 uses the request-path fallback for a final review and rest day.

## Per-day inventory

| Day | Topics | Fallback discussions | Reused scenarios | Worksheet labs | Command labs | Directive-like headings |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| 2 | 3 | 0 | 0 | 0 | 3 | 0 |
| 3 | 3 | 0 | 0 | 0 | 3 | 0 |
| 4 | 5 | 0 | 0 | 0 | 2 | 0 |
| 5 | 3 | 0 | 0 | 0 | 0 | 0 |
| 6 | 2 | 0 | 0 | 0 | 2 | 0 |
| 7 | 4 | 0 | 0 | 0 | 4 | 0 |
| 8 | 2 | 0 | 0 | 0 | 2 | 0 |
| 9 | 2 | 0 | 0 | 0 | 1 | 0 |
| 10 | 3 | 0 | 0 | 0 | 3 | 0 |
| 11 | 2 | 0 | 0 | 0 | 2 | 0 |
| 12 | 3 | 0 | 3 | 0 | 0 | 0 |
| 13 | 2 | 0 | 2 | 0 | 0 | 0 |
| 14 | 2 | 0 | 2 | 0 | 0 | 0 |
| 15 | 2 | 0 | 2 | 0 | 0 | 0 |
| 16 | 2 | 0 | 2 | 0 | 0 | 0 |
| 17 | 2 | 0 | 2 | 0 | 0 | 0 |
| 18 | 3 | 0 | 0 | 0 | 0 | 0 |
| 19 | 3 | 0 | 3 | 0 | 0 | 0 |
| 20 | 2 | 0 | 2 | 0 | 0 | 0 |
| 21 | 3 | 0 | 3 | 0 | 0 | 0 |
| 22 | 2 | 0 | 2 | 0 | 0 | 0 |
| 23 | 3 | 0 | 3 | 0 | 0 | 0 |
| 24 | 3 | 0 | 3 | 0 | 0 | 0 |
| 31 | 3 | 0 | 3 | 0 | 0 | 0 |
| 32 | 1 | 0 | 1 | 0 | 0 | 0 |
| 33 | 2 | 0 | 2 | 0 | 0 | 0 |
| 34 | 2 | 0 | 2 | 0 | 0 | 0 |
| 35 | 2 | 0 | 2 | 0 | 0 | 0 |
| 36 | 4 | 0 | 4 | 0 | 0 | 0 |
| 37 | 3 | 0 | 3 | 0 | 0 | 0 |
| 38 | 3 | 0 | 3 | 0 | 0 | 0 |
| 39 | 4 | 0 | 4 | 0 | 0 | 0 |
| 40 | 4 | 0 | 4 | 0 | 0 | 0 |
| 41 | 3 | 0 | 3 | 0 | 0 | 0 |
| 42 | 3 | 0 | 3 | 0 | 0 | 0 |
| 43 | 3 | 0 | 3 | 0 | 0 | 0 |
| 44 | 3 | 0 | 3 | 0 | 0 | 0 |
| 45 | 6 | 0 | 6 | 0 | 0 | 0 |
| 46 | 2 | 0 | 2 | 0 | 0 | 0 |
| 47 | 2 | 0 | 2 | 0 | 0 | 0 |
| 48 | 3 | 0 | 3 | 0 | 0 | 0 |
| 49 | 5 | 0 | 5 | 0 | 0 | 0 |
| 50 | 6 | 0 | 6 | 0 | 0 | 0 |
| 51 | 4 | 0 | 4 | 0 | 0 | 0 |
| 52 | 4 | 0 | 4 | 0 | 0 | 0 |
| 53 | 4 | 0 | 4 | 0 | 0 | 0 |
| 54 | 4 | 0 | 4 | 0 | 0 | 0 |
| 55 | 4 | 0 | 4 | 0 | 0 | 0 |
| 56 | 6 | 0 | 6 | 0 | 0 | 0 |
| 57 | 3 | 0 | 3 | 0 | 0 | 0 |
| 58 | 2 | 0 | 2 | 0 | 0 | 0 |
| 59 | 2 | 0 | 2 | 0 | 0 | 0 |
| 60 | 2 | 0 | 2 | 0 | 0 | 0 |
| 61 | 2 | 0 | 2 | 0 | 0 | 0 |
| 62 | 4 | 0 | 4 | 0 | 0 | 0 |
| 63 | 3 | 0 | 3 | 0 | 0 | 0 |
| 64 | 2 | 0 | 2 | 0 | 0 | 0 |
| 65 | 2 | 0 | 2 | 0 | 0 | 0 |
| 66 | 1 | 0 | 1 | 0 | 0 | 0 |
| 67 | 2 | 0 | 2 | 0 | 0 | 0 |
| 68 | 4 | 0 | 4 | 0 | 0 | 0 |
| 69 | 4 | 0 | 4 | 0 | 0 | 0 |
| 70 | 4 | 0 | 4 | 0 | 4 | 0 |
| 71 | 4 | 0 | 4 | 0 | 4 | 0 |
| 72 | 4 | 0 | 4 | 0 | 4 | 0 |
| 73 | 2 | 0 | 2 | 0 | 2 | 0 |
| 74 | 4 | 0 | 4 | 0 | 4 | 0 |
| 75 | 4 | 0 | 4 | 0 | 4 | 0 |
| 76 | 2 | 0 | 2 | 0 | 2 | 0 |
| 77 | 4 | 0 | 4 | 0 | 4 | 0 |
| 78 | 2 | 0 | 2 | 0 | 2 | 0 |
| 79 | 3 | 0 | 3 | 0 | 3 | 0 |
| 80 | 4 | 0 | 4 | 0 | 4 | 0 |
| 81 | 2 | 0 | 2 | 0 | 2 | 0 |
| 82 | 2 | 0 | 2 | 0 | 2 | 0 |
| 83 | 3 | 0 | 3 | 0 | 3 | 0 |
| 84 | 3 | 0 | 3 | 0 | 3 | 0 |
| 85 | 2 | 0 | 2 | 0 | 2 | 0 |
| 86 | 4 | 0 | 4 | 0 | 4 | 0 |
| 87 | 3 | 0 | 3 | 0 | 3 | 0 |
| 88 | 4 | 0 | 4 | 0 | 4 | 0 |
| 89 | 3 | 0 | 3 | 0 | 3 | 0 |
| 90 | 3 | 0 | 3 | 0 | 3 | 0 |
| 91 | 4 | 0 | 4 | 0 | 4 | 0 |
| 92 | 5 | 0 | 5 | 0 | 5 | 0 |
| 93 | 3 | 0 | 3 | 0 | 3 | 0 |
| 94 | 3 | 0 | 3 | 0 | 3 | 0 |
| 95 | 3 | 0 | 3 | 0 | 3 | 0 |
| 96 | 4 | 0 | 4 | 0 | 4 | 0 |
| 97 | 3 | 0 | 3 | 0 | 3 | 0 |
| 98 | 3 | 0 | 3 | 0 | 3 | 0 |
| 99 | 5 | 0 | 5 | 0 | 5 | 0 |
| 100 | 3 | 0 | 3 | 0 | 3 | 0 |
| 101 | 3 | 0 | 3 | 0 | 3 | 0 |
| 102 | 4 | 0 | 4 | 0 | 4 | 0 |
| 103 | 4 | 0 | 4 | 0 | 4 | 0 |
| 104 | 3 | 0 | 3 | 0 | 3 | 0 |
| 105 | 4 | 0 | 4 | 0 | 4 | 0 |
| 106 | 4 | 0 | 4 | 0 | 4 | 0 |
| 107 | 3 | 0 | 3 | 0 | 3 | 0 |
| 108 | 2 | 0 | 2 | 0 | 2 | 0 |
| 109 | 3 | 0 | 3 | 0 | 3 | 1 |
| 110 | 4 | 0 | 4 | 0 | 4 | 0 |
| 111 | 3 | 0 | 3 | 0 | 3 | 0 |
| 112 | 5 | 0 | 5 | 0 | 5 | 0 |
| 113 | 4 | 0 | 4 | 0 | 4 | 0 |
| 114 | 3 | 0 | 3 | 0 | 3 | 0 |
| 115 | 3 | 0 | 3 | 0 | 3 | 0 |
| 116 | 1 | 0 | 1 | 0 | 1 | 0 |
| 117 | 1 | 0 | 1 | 0 | 1 | 0 |
| 118 | 2 | 0 | 2 | 0 | 2 | 0 |
| 119 | 4 | 0 | 4 | 0 | 4 | 0 |
| 120 | 3 | 0 | 3 | 0 | 3 | 0 |
| 121 | 2 | 0 | 2 | 0 | 0 | 0 |
| 122 | 3 | 0 | 3 | 0 | 0 | 0 |
| 123 | 2 | 0 | 2 | 0 | 1 | 0 |
| 124 | 4 | 0 | 4 | 0 | 0 | 0 |
| 125 | 3 | 0 | 3 | 0 | 0 | 0 |
| 126 | 3 | 0 | 3 | 0 | 1 | 0 |
| 127 | 1 | 0 | 1 | 0 | 1 | 0 |
| 128 | 4 | 0 | 4 | 0 | 0 | 0 |
| 129 | 2 | 0 | 2 | 0 | 2 | 0 |
| 130 | 5 | 0 | 5 | 0 | 0 | 0 |
| 131 | 2 | 0 | 2 | 0 | 2 | 0 |
| 132 | 1 | 0 | 1 | 0 | 0 | 0 |
| 133 | 2 | 0 | 2 | 0 | 0 | 0 |
| 134 | 2 | 0 | 2 | 0 | 0 | 0 |
| 135 | 4 | 0 | 4 | 0 | 0 | 0 |
| 136 | 3 | 0 | 3 | 0 | 0 | 0 |
| 137 | 4 | 0 | 4 | 0 | 0 | 0 |
| 138 | 4 | 0 | 4 | 0 | 0 | 0 |
| 139 | 5 | 0 | 5 | 0 | 0 | 0 |
| 140 | 2 | 0 | 2 | 0 | 0 | 0 |
| 141 | 2 | 0 | 2 | 0 | 0 | 0 |
| 142 | 2 | 0 | 2 | 0 | 0 | 0 |
| 143 | 2 | 0 | 2 | 0 | 0 | 0 |
| 144 | 1 | 0 | 1 | 0 | 0 | 0 |
| 145 | 1 | 0 | 1 | 0 | 0 | 0 |
| 146 | 2 | 0 | 2 | 0 | 0 | 0 |
| 147 | 3 | 0 | 3 | 0 | 0 | 0 |
| 148 | 3 | 0 | 3 | 0 | 0 | 0 |
| 149 | 3 | 0 | 3 | 0 | 0 | 0 |
| 150 | 4 | 0 | 4 | 0 | 0 | 0 |
| 151 | 3 | 0 | 3 | 0 | 0 | 0 |
| 152 | 2 | 0 | 2 | 0 | 0 | 0 |
| 153 | 1 | 0 | 1 | 0 | 0 | 0 |
| 154 | 2 | 0 | 2 | 0 | 0 | 0 |
| 155 | 2 | 0 | 2 | 0 | 0 | 0 |
| 156 | 2 | 0 | 2 | 0 | 0 | 0 |
| 157 | 2 | 0 | 2 | 0 | 0 | 0 |
| 158 | 2 | 0 | 2 | 0 | 0 | 0 |
| 159 | 2 | 0 | 2 | 0 | 0 | 0 |
| 160 | 1 | 0 | 1 | 0 | 0 | 0 |
| 161 | 1 | 0 | 1 | 0 | 0 | 0 |
| 162 | 2 | 0 | 2 | 0 | 0 | 0 |
| 163 | 4 | 0 | 4 | 0 | 0 | 0 |
| 164 | 2 | 0 | 2 | 0 | 0 | 0 |
| 165 | 6 | 3 | 6 | 6 | 0 | 0 |
| 166 | 4 | 1 | 4 | 4 | 0 | 0 |
| 167 | 4 | 0 | 4 | 4 | 0 | 0 |
| 168 | 4 | 3 | 4 | 4 | 0 | 0 |
| 169 | 5 | 3 | 5 | 5 | 0 | 0 |
| 170 | 3 | 0 | 3 | 3 | 0 | 0 |
| 171 | 3 | 0 | 3 | 3 | 0 | 0 |
| 172 | 1 | 0 | 1 | 1 | 0 | 0 |
| 173 | 5 | 3 | 5 | 5 | 0 | 0 |
| 174 | 2 | 0 | 2 | 2 | 0 | 0 |
| 175 | 1 | 0 | 1 | 1 | 0 | 0 |
| 176 | 1 | 0 | 1 | 1 | 0 | 0 |
| 177 | 1 | 0 | 1 | 1 | 0 | 0 |
| 178 | 1 | 0 | 1 | 1 | 0 | 0 |
| 179 | 1 | 0 | 1 | 1 | 0 | 0 |
| 180 | 1 | 1 | 1 | 1 | 0 | 0 |

The detailed topic-level flags are in [data/content-audit.csv](data/content-audit.csv). Days 1–12 and 18 are hand-written and materially better aligned, though publisher-section links still need verification across the site. The remaining topics need editorial review against their roadmap Study, Practice and Exit evidence before they can be treated as completed lessons. Rewriting requires topic-specific mechanisms, worked examples, realistic problems, exercises with observable acceptance checks and exact further-study links; adding more generic paragraphs will not repair the mismatch.
