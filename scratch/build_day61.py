#!/usr/bin/env python3
"""Assemble and validate content/day-061-page.html."""
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

SITE_ROOT = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site")
ORIG_PAGE = SITE_ROOT / "content" / "day-061-page.html"

# Import parts
sys.path.insert(0, str(SITE_ROOT / "scratch"))
from part2_content import get_part2_html
from part3_content import get_part3_html
from part4_content import get_part4_html

# Extract header from original day-061-page.html to preserve all 180 navigation options
orig_content = ORIG_PAGE.read_text(encoding="utf-8")
header_start = orig_content.find('<header class="site-nav">')
header_end = orig_content.find('</header>') + len('</header>')
site_header = orig_content[header_start:header_end]

html_parts = []

# DOCTYPE and HEAD
html_parts.append("""<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark light"><title>Day 61: Relational databases and transactions · GCP 180 days</title><link rel="stylesheet" href="../assets/site.css"><script defer src="../assets/site.js"></script></head><body><a class="skip" href="#main">Skip to content</a>""")

# SITE HEADER
html_parts.append(site_header)

# AUDIT BANNER & MAIN OPENING & HERO
html_parts.append("""<div class="audit-banner"><strong>Draft content:</strong> Most lessons use generated templates and have not passed topic-level review. <a href="../CONTENT_AUDIT.md">Read the content audit</a>.</div><main id="main" class="container day" data-day="61" data-prev="day-060.html" data-next="day-062.html" data-index="../index.html"><div class="crumb"><a href="../index.html">Roadmap index</a> / <a href="../index.html#block-core-services-and-integrated-practice">Core services and integrated practice</a> / Day 61 of 180</div><section class="hero"><div class="pills"><span class="pill">DAY 61</span><span class="pill">3–4 hours</span><span class="pill">production practice</span><span class="pill">Topics 020</span></div><h1>Day 61 — Relational databases and transactions</h1><p class="lead"><strong>Outcome:</strong> Evaluate Cloud SQL and AlloyDB relational architectures, connection topologies, regional HA failover, and connection pooling; deep-dive transaction isolation levels, concurrency anomalies, deadlock prevention, WAL durability, and idempotent retry loops.</p><div><strong>Entry prerequisites:</strong> <p><a href="day-016.html">Day 16</a>, <a href="day-060.html">Day 60</a>, <a href="day-026.html">Day 26</a>; bring their exit artifacts.</p></div><div class="callout success"><strong>Exit artifact</strong><p>SQL execution results, concurrency isolation traces, connection and HA failover topology diagrams, and a production Cloud SQL versus AlloyDB architectural decision record saved to <code>day-061-sql-results-adr.md</code>.</p></div><p class="small">Source curriculum checked 2026-09-26; external documentation links are selected reading and may change. A tabletop result is a design exercise, not a production test.</p></section>""")

# TOC ASIDE
html_parts.append("""<aside class="toc" aria-label="On this page"><strong>On this page</strong><a href="#part-1">1 · Topics</a><a href="#part-2">2 · Technical discussion</a><a href="#part-3">3 · Problems and solutions</a><a href="#part-4">4 · Labs</a><div class="toc-topic"><span>Cloud SQL connection paths, pooling/limits, maintenance, backup/PITR, regional HA and…</span><a href="#topic-01-overview">overview</a> · <a href="#topic-01-technical">discussion</a> · <a href="#topic-01-problem">problem</a> · <a href="#topic-01-lab">lab</a></div><div class="toc-topic"><span>Compare AlloyDB compatibility/read pools at selection depth</span><a href="#topic-02-overview">overview</a> · <a href="#topic-02-technical">discussion</a> · <a href="#topic-02-problem">problem</a> · <a href="#topic-02-lab">lab</a></div></aside>""")

# PART 1: TOPICS OF THE DAY
html_parts.append("""<section id="part-1" class="part"><h2>1 · Topics of the day</h2><article id="topic-01-overview" class="topic-card"><h3>Cloud SQL connection paths, pooling/limits, maintenance, backup/PITR, regional HA and…</h3><p>Enterprise relational database architecture on Google Cloud begins with selecting the correct connectivity, connection pooling, and reliability topology for Cloud SQL. Cloud SQL supports three distinct networking paths for client access: Cloud SQL Auth Proxy, Private Services Access (PSA), and Private Service Connect (PSC). Cloud SQL Auth Proxy establishes a local tunnel using Google Cloud Identity and Access Management (IAM) authentication and ephemeral, automatically rotated 1-hour client-side mTLS certificates signed by Google's internal Certificate Authority, eliminating the administrative overhead of self-managed certificate rotation and keeping database endpoints completely off the public Internet. Private Services Access (PSA) connects consumer Virtual Private Clouds (VPCs) to Google-managed Service Networking VPCs via VPC Network Peering across a pre-allocated internal CIDR range (typically <code>/24</code> or <code>/16</code>). However, PSA introduces architectural constraints: it consumes VPC peering quotas (bounded by Google Cloud's 25-peering limit per VPC), introduces severe IP address collision risks across complex corporate multi-VPC landing zones, and lacks transitive routing to on-premises environments without custom route advertisements or proxy gateways. Private Service Connect (PSC) represents the modern, recommended standard: it exposes the Cloud SQL instance as a single <code>/32</code> internal IP forwarding rule directly inside a consumer VPC subnet, requiring zero VPC peering, eliminating CIDR collision risks, enabling native multi-VPC/multi-tenant consumption, and integrating seamlessly with private Cloud DNS zones.</p><p>Relational databases enforce strict client connection limits dictated by memory and operating system concurrency models. In PostgreSQL, each client connection spawns a dedicated operating system process (<code>postgres: user db host</code>) requiring 5 MB to 10 MB of private resident memory in addition to socket buffers, shared memory handles, and query workspace allocations (<code>work_mem</code>). When elastic microservices scale up under sudden traffic surges, hundreds or thousands of unpooled client connections rapidly saturate database memory, induce severe CPU context-switching overhead, and exhaust the database <code>max_connections</code> ceiling. Connection poolers such as PgBouncer (operating in transaction pooling mode) and HikariCP resolve this bottleneck by multiplexing thousands of transient client connections into a compact, CPU-aligned pool of backend database connections sized according to hardware capacity: <code>(vCPU * 2) + effective_spindle_count</code>. For high availability, Cloud SQL Regional HA utilizes synchronous block-level replication via Regional Persistent Disk (Regional PD) across two zones (Zone A primary, Zone B standby) over Google's low-latency Andromeda virtual network, guaranteeing a Recovery Point Objective of zero (RPO = 0). Automated health probes detect primary instance failure, executing failover and IP/DNS redirection within 60 to 120 seconds (RTO). Scheduled maintenance windows provide 7-day advance rollout notifications with flexible reschedule and deferral rules, while automated daily disk snapshots and continuous Write-Ahead Log (WAL) archiving empower down-to-the-second Point-in-Time Recovery (PITR) to reverse accidental data corruption.</p><p>During a seasonal flash-sale spike, 120 unpooled GKE storefront microservices spawn 4,200 direct database connections over Private Services Access, exhausting PostgreSQL connection limits and inducing an unexpected regional HA failover that resets all TCP sockets. Client connection retry storms overwhelm database memory buffers, driving API p99 latency to 38 seconds and abandoning $380,000 in customer checkouts within the first 25 minutes.</p><p><a href="#topic-01-technical">Technical discussion →</a> <a href="#topic-01-problem">Real-world problem →</a> <a href="#topic-01-lab">Step-by-step lab →</a></p></article><article id="topic-02-overview" class="topic-card"><h3>Compare AlloyDB compatibility/read pools at selection depth</h3><p>While Cloud SQL provides managed instances of standard open-source engines on coupled compute and storage, AlloyDB for PostgreSQL introduces a next-generation disaggregated architecture engineered specifically for demanding enterprise transactional and analytical workloads. AlloyDB completely decouples database compute instances from a distributed, multi-zone, log-structured storage engine built upon Google's Colossus distributed storage filesystem and Andromeda software-defined networking. In standard PostgreSQL and Cloud SQL, the database engine must flush both Write-Ahead Log (WAL) records and dirty 8 KB data pages from shared memory to disk, causing significant write amplification, random I/O thrashing, and periodic checkpoint stalls. In contrast, AlloyDB compute instances write ONLY WAL records directly to the distributed storage fleet over Andromeda; compute instances never flush dirty pages to storage. The distributed storage nodes process WAL streams and materialize database pages asynchronously in the background. This fundamental architectural shift delivers more than 4x the transactional write throughput and more than 2x the read throughput of standard PostgreSQL, while enabling instant crash recovery in under 10 seconds because the compute instance requires zero redo log playback upon startup. Read workloads scale horizontally through auto-scaling Read Pools (1 to 20 instances) fronted by an Internal Load Balancer endpoint, while the built-in AlloyDB Columnar Engine automatically accelerates complex analytical queries by up to 100x using an in-memory vectorized columnar store (HTAP).</p><p>Mastering transactional correctness in relational databases requires an uncompromising understanding of SQL transaction isolation levels, concurrency anomalies, lock hierarchies, and resilient retry semantics. The ANSI SQL standard defines four isolation levels, which PostgreSQL implements through Multi-Version Concurrency Control (MVCC): <code>READ COMMITTED</code> (default, where each query sees a new snapshot of committed data), <code>REPEATABLE READ</code> (Snapshot Isolation, where all queries within a transaction share a single snapshot taken at transaction start), and <code>SERIALIZABLE</code> (Serializable Snapshot Isolation - SSI, which guarantees serial execution equivalence by tracking read-write conflict dependencies in memory). In <code>READ COMMITTED</code>, concurrent transactions are vulnerable to non-repeatable reads, phantom reads, and check-then-act race conditions that cause inventory overselling. In <code>REPEATABLE READ</code>, transactions eliminate dirty, non-repeatable, and phantom reads, but remain vulnerable to write skew anomalies across disjoint rows; concurrent updates to the same row abort with serialization failures (<code>SQLSTATE 40001</code>). In <code>SERIALIZABLE</code>, non-serializable interleavings are proactively terminated by the engine. Uncoordinated row-level locking (<code>SELECT ... FOR UPDATE</code>) across multiple records introduces cyclic wait dependencies, causing PostgreSQL's deadlock detector to abort transactions with <code>SQLSTATE 40P01</code> after <code>deadlock_timeout</code> expires. Enterprise applications must guarantee durability (<code>synchronous_commit = on</code>) and implement application-level idempotency tokens coupled with exponential backoff and randomized jitter to handle <code>40001</code> and <code>40P01</code> transactional retries cleanly.</p><p>High-frequency concurrent inventory checkout transactions executing under default Read Committed isolation produce negative stock allocations, while subsequent uncoordinated row-locking updates trigger cascading deadlock aborts and serialization failures across background order workers. Unhandled transaction rollback exceptions crash the order intake pipeline, generating 14,000 failed fulfillment events and an estimated $510,000 in unrecoverable revenue loss and inventory reconciliation liabilities.</p><p><a href="#topic-02-technical">Technical discussion →</a> <a href="#topic-02-problem">Real-world problem →</a> <a href="#topic-02-lab">Step-by-step lab →</a></p></article></section>""")

# PART 2: TECHNICAL DISCUSSION
html_parts.append("""<section id="part-2" class="part"><h2>2 · Technical discussion of each topic</h2>""" + get_part2_html() + """</section>""")

# PART 3: REAL-WORLD PROBLEMS
html_parts.append(get_part3_html())

# PART 4: STEP-BY-STEP LABS
html_parts.append(get_part4_html())

# COMPLETION SECTION
html_parts.append("""<section class="completion"><h2>Daily evidence</h2><p>Assemble your relational database architecture decision record (ADR), PostgreSQL concurrency evaluation, Cloud SQL vs AlloyDB selection criteria, and high-availability failover verification into <code>day-061-sql-results-adr.md</code>. Document your connection path decisions (Cloud SQL Auth Proxy vs PSA vs PSC), PgBouncer transaction-mode pooling parameters (bounding backend connections to <code>(vCPU * 2)</code> while servicing 5,000 client sockets), Regional Persistent Disk synchronous replication RPO/RTO guarantees, AlloyDB continuous WAL streaming and in-memory Columnar Engine HTAP acceleration, and application-level retry wrappers implementing exponential backoff with full jitter to handle <code>SQLSTATE 40001</code> (Serialization Failure) and <code>SQLSTATE 40P01</code> (Deadlock Detected) with guaranteed idempotency.</p><label class="check"><input type="checkbox" data-progress="read-61"> I read and reviewed the day</label><label class="check"><input type="checkbox" data-progress="artifact-61"> I saved the exit artifact</label></section>""")

# PAGER & FOOTER
html_parts.append("""<nav class="pager" aria-label="Day pagination"><a href="day-060.html">&larr; Day 60<small>File systems and backup design</small></a><a href="../index.html">All 180 days<small>Browse the roadmap</small></a><a href="day-062.html">Day 62 &rarr;<small>Distributed and nonrelational database choices</small></a></nav><p class="shortcut">Keyboard: P or [ previous &middot; N or ] next &middot; I index</p></main><footer class="site-footer">GCP Architect &middot; 180-day independent study &middot; Roadmap dated 2026-09-26. Local progress remains in this browser.</footer></body></html>""")

full_html = "".join(html_parts)

# Write to file
ORIG_PAGE.write_text(full_html, encoding="utf-8")
print(f"Successfully wrote {len(full_html)} bytes to {ORIG_PAGE}")

# Run internal audit on the generated HTML
soup = BeautifulSoup(full_html, "html.parser")
ids = [x.get("id") for x in soup.select("[id]")]
duplicates = [x for x in ids if ids.count(x) > 1]
print("Unique IDs count:", len(set(ids)), "Total IDs:", len(ids))
if duplicates:
    print("WARNING: Duplicate IDs found:", set(duplicates))

required_ids = [
    "main", "day-jump", "part-1", "part-2", "part-3", "part-4",
    "topic-01-overview", "topic-01-technical", "topic-01-problem", "topic-01-lab",
    "topic-02-overview", "topic-02-technical", "topic-02-problem", "topic-02-lab"
]
missing_ids = [rid for rid in required_ids if rid not in ids]
if missing_ids:
    print("WARNING: Missing required IDs:", missing_ids)
else:
    print("All required IDs present!")

for phrase in ("Outcome:", "Entry prerequisites:", "Exit artifact", "Daily evidence"):
    if phrase not in soup.get_text(" "):
        print(f"WARNING: Missing phrase: '{phrase}'")

for code in soup.select("code"):
    value = code.get_text(" ", strip=True)
    if code.parent.name != "pre" and re.match(r"^(?:sudo |git |gcloud |terraform |kubectl |docker |python3? |curl |ssh |cat |printf |mkdir |cd |pwd$|ls(?: |$)|command |ip |dig |nslookup |systemctl |journalctl )", value):
        print(f"WARNING: Runnable command outside a code block: {value[:60]}")

for pre in soup.select("pre"):
    if not pre.select_one("code"):
        print(f"WARNING: <pre> element missing child <code> element: {pre}")
    if pre.select_one("kbd"):
        print(f"WARNING: <pre> contains <kbd>: {pre}")

print("Internal audit completed.")
