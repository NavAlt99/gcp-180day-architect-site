# Day 2 rewrite brief (SCOPE=rewrite)

Read `scratch/quality/QUALITY_STANDARD.md` once before auditing. Read
`scratch/quality/day-002-exemplar-arp.md` ONLY at Stage 3 (topic 02).

## Preconditions (stop and report; do not repair)
- PAGE_AUTHORING_CONTRACT.md contains the "Quality floor" rule, `day_run.py resolve`
  accepts SCOPE=rewrite, and check_page_rules.py has R10-R13 with --snapshot/--baseline.
- If the ONLY preflight failure is that branch day-002 already exists, create
  `day-002-rewrite` from updated main per the normal preflight steps, report the
  deviation, continue. Do not edit scripts. If day_run.py refuses the branch name
  later, stop and report.

## Decisions already made by the user
1. Keep every worked dossier. Counts now: topic 01=15, 02=21, 03=8, 04=11. Never
   delete or merge a dossier to reduce count. Counts are protected (R13).
2. Do not move dossiers or change anchors, subtopic structure, diagrams, labs or
   source lists. Rewrite text inside existing items only.
3. Removal is allowed only for (a) verbatim repeats, (b) non-specific boilerplate,
   (c) heading restatements. Weak text is replaced (entry type `rewrite`) and
   factual errors are fixed (type `correction`); nothing is silently dropped.
   Every `rewrite` entry lists ideas_retained.
4. Shared dossier text: "Architect's reasoning chain" is identical in all 55
   dossiers and "Scope guard" repeats per dossier in four variants. Fix in the
   spec helper `worked_mechanisms()` (scratch/day_data_002.py): write the reasoning
   chain once at the top of Part 2 under the plain-language heading "How to read a
   worked dossier" (define its terms), and one scope guard per topic after that
   topic's dossiers. Each text must then appear exactly once on the page.
5. Verification: check GCP and RFC statements against primary documentation, open
   the cited heading, record it with the access date. If a statement cannot be
   verified, rewrite it to what a verified source supports, or mark the ledger
   entry `unresolved` and leave the text for the user's decision. Never add an
   unverified claim.
6. Dossier placement under the subtopics they teach is a recommendation only: list
   it in the handoff; do not implement it.
7. These statements were reported by a reviewer and are NOT yet verified. Check
   each against primary sources, then correct, soften or mark unresolved:
   - ARP subtopic GCP row: Andromeda, Geneve, Jupiter, virtio-net and gVNIC claims;
     "broadcast storms inherent to IPv4 ARP"; capitalized or exclamation emphasis
     ("NOT ARPed!", "NEW L2 header").
   - Next-hop GCP row: virtual default gateway described as an Andromeda endpoint
     distributed across Google datacenter hosts.
   - RFC 1918 subtopic: "Internet routers drop all RFC 1918 traffic... never
     advertised over BGP" (stated as absolute); the RFC 6598 paragraph attributing
     Private Google Access and 169.254.169.254 to 100.64.0.0/10 (169.254.0.0/16 is
     link-local); "private subnets cannot reach the Internet directly; outbound
     requires Cloud NAT".
   - CIDR table: /27 "Cloud SQL private services peering block" versus the text
     saying /24 or /16; "maximum VPC network size" at /8; the claim that AWS and
     Azure each reserve five addresses per subnet.

## Stages (STOP where marked; wait for `go`, `go W1,W3`, or edits)

**Stage 0, read-only inventory.** Run `day_run.py resolve --day 2`, `preflight
--day 2`, `extract_day_inputs.py --day 2`. Before any edit, snapshot the BUILT page:
`python3 scripts/check_page_rules.py --day 2 --diagrams keep --snapshot
scratch/day-002-protected-baseline.json`. Report R10-R13 results and per-topic
dossier counts. Do not load the rendered page. Read the spec in regions, one topic
at a time.

**Stage 1, mechanical.** Decision 4 plus every other verbatim repeat R10 lists. Write
ledger `scratch/audits/day-002-rewrite.json`. Print a compact table only (ID,
location, type, reason class, one line); keep full old_str/new_str in the JSON.
STOP. After `go`: apply, build, run `day_run.py check --day 2 --diagrams keep`,
compare R13. R10 should reach 0 for Day 2 or list each remaining repeat with a
reason. Refresh the Day 2 entry in `scratch/baseline/r10-existing-repeats.json`
(shrink-only).

**Stages 2-5, one per topic in order 01, 02, 03, 04** (Part 1 overview plus Part 2
subtopics and dossiers of that topic only). Audit against the quality standard,
these decisions and the suspect list. Topic 02 is Stage 3: subtopic 3 (ARP and NDP)
and dossiers 15-17 start from the exemplar file. Topics 03 and 04 have not been
reviewed by anyone yet, so read them fresh. Ledger entries per type; `rewrite` and
`correction` entries show words before/after and ideas_retained; `correction`
entries add source URL, heading opened and access date. Print a compact table.
STOP. After `go`: apply, build, `check`, compare R13. Dossier counts must be
unchanged (15, 21, 8, 11). Then continue.

**Stage 6, Parts 3 and 4, audit-only.** Check the incident scenario and lab of each
topic against the standard and R10. Add findings as `proposed`. Apply nothing
except the mechanical R10 fixes approved in Stage 1. STOP.

**Finish.** Run `day_run.py gate --day 2` (R13 against the snapshot), then
`day_run.py commit --day 2` if it passes. Never push. If the gate fails, repair what
these edits caused and rerun, or stop and report.

## Files that may change
scratch/day_data_002.py (or its directory form; report which), the regenerated
override and days/day-002.html, scratch/audits/day-002-*, scratch/day-002-*,
scratch/handoffs/day-002.md, scratch/baseline/r10-existing-repeats.json
(shrink-only), and the study-link and lab reports. Nothing else: no other day,
script, contract, prompt file or asset.

## Token rules
Never print page HTML or full new text in chat; keep topic text in the ledger JSON;
hold one topic in context at a time; no full-site build; no re-reading unchanged
files; do not use the graphify skill and ignore graphify-out/ in cleanliness checks.

## Final report
R10-R13 before and after; dossier counts before and after (must be equal); words
before and after per topic (informational); corrections with sources and access
dates; unresolved items; proposals (dossier placement, Parts 3 and 4 findings);
completed stages; commit hash.
