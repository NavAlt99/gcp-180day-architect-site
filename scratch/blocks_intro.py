"""Hero, TOC, and Part 1 overview for Day 58."""

HERO_HTML = """<section class="hero">
<div class="pills"><span class="pill">DAY 58</span><span class="pill">3–4 hours</span><span class="pill">production practice</span><span class="pill">Cloud Storage &amp; Durability</span></div>
<h1>Day 58 — Object storage and local durability</h1>
<p class="lead"><strong>Outcome:</strong> Upload a small synthetic dataset and test a narrow access path; inspect version/retention behavior without applying irreversible production locks.</p>
<div><strong>Entry prerequisites:</strong> <p><a href="day-016.html">Day 16</a>, <a href="day-037.html">Day 37</a>, <a href="day-057.html">Day 57</a>; bring their exit artifacts.</p></div>
<div class="callout success"><strong>Exit artifact</strong><p>An object lifecycle/access worksheet and a durable-write versus cached-write explanation, assembled as <code>day-058-storage-durability.md</code>.</p></div>
<p class="small">Source curriculum checked 2026-09-26; external documentation links are selected reading and may change. A tabletop result is a design exercise, not a production test.</p>
</section>"""

TOC_HTML = """<aside class="toc" aria-label="On this page">
<strong>On this page</strong>
<a href="#part-1">1 · Topics</a>
<a href="#part-2">2 · Technical discussion</a>
<a href="#part-3">3 · Problems and solutions</a>
<a href="#part-4">4 · Labs</a>
<div class="toc-topic"><span>Cloud Storage access and location choices, classes, lifecycle, Autoclass, versioning,…</span><a href="#topic-01-overview">overview</a> · <a href="#topic-01-technical">discussion</a> · <a href="#topic-01-problem">problem</a> · <a href="#topic-01-lab">lab</a></div>
<div class="toc-topic"><span>Irreversible retention locking is a design exercise</span><a href="#topic-02-overview">overview</a> · <a href="#topic-02-technical">discussion</a> · <a href="#topic-02-problem">problem</a> · <a href="#topic-02-lab">lab</a></div>
</aside>"""

PART1_HTML = """<section id="part-1" class="part">
<h2>1 · Topics of the day</h2>

<article id="topic-01-overview" class="topic-card">
<h3>Cloud Storage access and location choices, classes, lifecycle, Autoclass, versioning,…</h3>
<p>Google Cloud Storage is an exabyte-scale, globally distributed object storage platform built directly upon Google's Colossus cluster filesystem and Spanner global metadata management tier. When designing enterprise storage backends, architects must balance location topologies (single-region for lowest latency, dual-region paired active-active with a contractual 15-minute Turbo Replication RPO SLA, or multi-region across continental zones), storage classes (Standard for frequent access, Nearline with 30-day minimum duration, Coldline with 90-day minimum duration, and Archive with 365-day minimum duration alongside strict early deletion and retrieval surcharges), and automated lifecycle policies. Autoclass removes operational manual tiering toil by dynamically transitioning inactive objects to colder tiers and seamlessly auto-promoting accessed objects back to Standard with zero retrieval fees. Concurrently, Object Lifecycle Management (OLM) rules execute asynchronous daily reconciliation based on conditions such as age, creation date, live state, and newer version counts. Object Versioning assigns immutable generation and metageneration numbers to preserve historical state, reinforced by Cloud Storage's default 7-day Soft Delete window for disaster rollback. Access control is hardened through Uniform Bucket-Level Access (UBLA), eliminating legacy ACL ambiguity in favor of pure Cloud IAM, complemented by v4 Signed URLs for time-bounded delegated access. Crucially, Cloud Storage enforces globally strong read-after-write and read-after-delete consistency, contrasting fundamentally with local POSIX filesystem dirty page caching where OS buffer flushes (<code>fsync</code> and <code>fdatasync</code>) are mandatory before data is physically committed to block media.</p>
<p>A misconfigured lifecycle transition rule aggressively archives active invoice data, while an uncoordinated worker write path relies on asynchronous POSIX buffer flushes before final object upload. Querying systems receive stale reads and encounter massive early deletion surcharges, stalling daily billing reconciliations by 18 hours and incurring $62,000 in unbudgeted retrieval penalties.</p>
<p><a href="#topic-01-technical">Technical discussion →</a> <a href="#topic-01-problem">Real-world problem →</a> <a href="#topic-01-lab">Step-by-step lab →</a></p>
</article>

<article id="topic-02-overview" class="topic-card">
<h3>Irreversible retention locking is a design exercise</h3>
<p>Enterprise regulatory compliance mandates strict Write Once, Read Many (WORM) storage guarantees under financial frameworks including SEC Rule 17a-4(f), FINRA Rule 4511(c), and CFTC Regulation 1.31. Cloud Storage enforces WORM compliance through bucket-level retention policies that specify an immutable retention period during which objects cannot be deleted, modified, or overwritten by any identity—including project owners and storage administrators. Operational flexibility is maintained using Retention Holds: Event-Based Holds freeze object deletion indefinitely until an external business trigger occurs (such as customer contract termination or account closure), at which point the hold is cleared and the retention period countdown initiates; Temporary Holds freeze object deletion for legal discovery, regulatory subpoenas, and ongoing litigation. However, an unlocked retention policy can still be removed or shortened by a privileged administrative identity. Bucket Lock irrevocably locks the retention policy: once locked, the policy cannot be deleted, and the retention duration cannot be reduced—it can only be extended. Furthermore, the bucket itself cannot be destroyed until every contained object has satisfied its retention duration and been deleted. Because Bucket Lock is permanent and mathematically irreversible, its implementation carries immense operational blast radius and must be treated as a rigorous design exercise governed by canary testing, soak periods, and multi-party architectural sign-off.</p>
<p>An automated maintenance script with elevated bucket credentials executes an unconstrained deletion against an un-locked regulatory archive, purging 18 months of financial audit ledgers. The irreversible loss of immutable records violates SEC Rule 17a-4 and FINRA 4511 compliance, resulting in immediate federal regulatory subpoenas and $1.4 million in statutory penalties.</p>
<p><a href="#topic-02-technical">Technical discussion →</a> <a href="#topic-02-problem">Real-world problem →</a> <a href="#topic-02-lab">Step-by-step lab →</a></p>
</article>
</section>"""
print("blocks_intro.py written")
