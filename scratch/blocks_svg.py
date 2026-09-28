"""SVG diagrams for Day 58: Architecture and Field Incident cases."""

FIG_58_1_ARCH_SVG = """<figure class="diagram-figure">
<svg role="img" aria-labelledby="d58-arch-title d58-arch-desc" viewBox="0 0 1060 620" width="100%" height="auto" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d58-arch-title">Cloud Storage Durability, Turbo Replication, Autoclass Lifecycle &amp; WORM Compliance Architecture</title>
<desc id="d58-arch-desc">Comprehensive architectural diagram illustrating the POSIX dirty buffer versus Colossus strong commit boundary, Dual-Region Turbo Replication across us-central1 and us-east1, Autoclass cold tiering lifecycle, and WORM Bucket Lock enforcement.</desc>
<defs>
<marker id="d58-m-write" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
<marker id="d58-m-rep" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/>
</marker>
<marker id="d58-m-tier" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#c084fc"/>
</marker>
<marker id="d58-m-lock" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/>
</marker>
<marker id="d58-m-blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#38bdf8"/>
</marker>
</defs>

<!-- Canvas Outer Border -->
<rect x="15" y="15" width="1030" height="590" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
<text x="35" y="42" fill="#f8fafc" font-size="16" font-weight="700">Cloud Storage Durability, Turbo Replication, Autoclass Lifecycle &amp; WORM Compliance Architecture</text>
<text x="35" y="60" fill="#94a3b8" font-size="12">POSIX Dirty Cache vs Colossus Global Commit, 15-Min RPO Turbo Replication, Autoclass Zero-Fee Tiering &amp; WORM Bucket Lock</text>

<!-- Legend -->
<g transform="translate(560, 28)">
<line x1="0" y1="12" x2="25" y2="12" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d58-m-write)"/>
<text x="32" y="16" fill="#86efac" font-size="10">Direct Commit</text>
<line x1="125" y1="12" x2="150" y2="12" stroke="#f59e0b" stroke-width="2.5" marker-end="url(#d58-m-rep)"/>
<text x="157" y="16" fill="#fcd34d" font-size="10">Turbo Replication</text>
<line x1="260" y1="12" x2="285" y2="12" stroke="#c084fc" stroke-width="2" marker-end="url(#d58-m-tier)"/>
<text x="292" y="16" fill="#d8b4fe" font-size="10">Autoclass Tier</text>
<line x1="380" y1="12" x2="405" y2="12" stroke="#f43f5e" stroke-width="2" marker-end="url(#d58-m-lock)"/>
<text x="412" y="16" fill="#fca5a5" font-size="10">WORM Lock</text>
</g>

<!-- Column 1: Client Ingestion & Durability Boundary -->
<rect x="35" y="80" width="235" height="505" rx="6" fill="#090d16" stroke="#475569" stroke-width="1.5"/>
<text x="50" y="105" fill="#f1f5f9" font-size="13" font-weight="700">1 · Ingestion &amp; Durability</text>
<text x="50" y="122" fill="#94a3b8" font-size="11">POSIX Buffer vs Direct Ingestion</text>

<!-- Sub-box: Application Worker -->
<rect x="50" y="135" width="205" height="70" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
<text x="60" y="155" fill="#38bdf8" font-size="11" font-weight="700">Compute Worker / App Node</text>
<text x="60" y="172" fill="#cbd5e1" font-size="10">Generates transaction order payload</text>
<text x="60" y="188" fill="#94a3b8" font-size="10">In-memory buffer (RAM heap)</text>

<!-- Sub-box: POSIX File Flush Boundary -->
<rect x="50" y="215" width="205" height="85" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
<text x="60" y="235" fill="#fcd34d" font-size="11" font-weight="700">POSIX Kernel Buffer Cache</text>
<text x="60" y="251" fill="#cbd5e1" font-size="10">write() writes to dirty pages</text>
<text x="60" y="267" fill="#fb7185" font-size="10">Uncommitted on host crash!</text>
<text x="60" y="283" fill="#86efac" font-size="10">Must call fdatasync() to commit</text>

<!-- Sub-box: Direct GCS Client Upload -->
<rect x="50" y="310" width="205" height="85" rx="4" fill="#132337" stroke="#22c55e" stroke-width="1.5"/>
<text x="60" y="330" fill="#4ade80" font-size="11" font-weight="700">Direct GCS Ingestion Stream</text>
<text x="60" y="346" fill="#cbd5e1" font-size="10">Chunked Resumable Upload</text>
<text x="60" y="362" fill="#38bdf8" font-size="10">CRC32c / MD5 Digest Validation</text>
<text x="60" y="378" fill="#cbd5e1" font-size="10">HTTP 200 = Durable Commit</text>

<!-- Sub-box: Access Control & Preconditions -->
<rect x="50" y="405" width="205" height="85" rx="4" fill="#1e293b" stroke="#3b82f6" stroke-width="1"/>
<text x="60" y="425" fill="#60a5fa" font-size="11" font-weight="700">Access &amp; Atomic Preconditions</text>
<text x="60" y="441" fill="#cbd5e1" font-size="10">Uniform Bucket-Level Access (IAM)</text>
<text x="60" y="457" fill="#38bdf8" font-size="10">Signed URLs v4 (Time-bounded)</text>
<text x="60" y="473" fill="#fcd34d" font-size="10">x-goog-if-generation-match: 0</text>

<!-- Sub-box: Local Durability Summary -->
<rect x="50" y="500" width="205" height="70" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="60" y="520" fill="#94a3b8" font-size="10" font-weight="600">Durability Guarantee</text>
<text x="60" y="536" fill="#cbd5e1" font-size="10">POSIX: Block commit after flush</text>
<text x="60" y="552" fill="#34d399" font-size="10">GCS: Multi-zone Colossus commit</text>


<!-- Column 2: Dual-Region Turbo Replication Engine -->
<rect x="285" y="80" width="240" height="505" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
<text x="300" y="105" fill="#38bdf8" font-size="13" font-weight="700">2 · Dual-Region Engine</text>
<text x="300" y="122" fill="#94a3b8" font-size="11">nam4: us-central1 + us-east1</text>

<!-- Sub-box: Bucket Definition -->
<rect x="295" y="135" width="220" height="75" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
<text x="305" y="155" fill="#38bdf8" font-size="11" font-weight="700">Dual-Region Bucket (nam4)</text>
<text x="305" y="171" fill="#cbd5e1" font-size="10">Location: US-CENTRAL1 &amp; US-EAST1</text>
<text x="305" y="187" fill="#86efac" font-size="10">Active-Active Read / Write Routing</text>
<text x="305" y="201" fill="#94a3b8" font-size="9">Cross-region latency ~18ms</text>

<!-- Sub-box: Spanner Global Metadata -->
<rect x="295" y="220" width="220" height="80" rx="4" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
<text x="305" y="240" fill="#c7d2fe" font-size="11" font-weight="700">Spanner Global Metadata</text>
<text x="305" y="256" fill="#a5b4fc" font-size="10">Atomic Read-After-Write Globally</text>
<text x="305" y="272" fill="#cbd5e1" font-size="10">Strong Read-After-Delete</text>
<text x="305" y="288" fill="#34d399" font-size="10">Generation &amp; Metageneration Index</text>

<!-- Sub-box: Primary Region Colossus -->
<rect x="295" y="310" width="220" height="85" rx="4" fill="#132337" stroke="#22c55e" stroke-width="1.5"/>
<text x="305" y="330" fill="#4ade80" font-size="11" font-weight="700">Primary Colossus Cluster</text>
<text x="305" y="346" fill="#cbd5e1" font-size="10">Reed-Solomon (8+4) Erasure Coding</text>
<text x="305" y="362" fill="#cbd5e1" font-size="10">Distributed across 3 local zones</text>
<text x="305" y="378" fill="#a7f3d0" font-size="10">11 9's Annual Durability (99.999999999%)</text>

<!-- Sub-box: Turbo Replication Channel -->
<rect x="295" y="405" width="220" height="85" rx="4" fill="#2a1d12" stroke="#f59e0b" stroke-width="1.5"/>
<text x="305" y="425" fill="#fcd34d" font-size="11" font-weight="700">Turbo Replication Channel</text>
<text x="305" y="441" fill="#fde68a" font-size="10">Contractual SLA: 15-Minute RPO</text>
<text x="305" y="457" fill="#cbd5e1" font-size="10">100% Target Replicated to us-east1</text>
<text x="305" y="473" fill="#f59e0b" font-size="10">Replication fee applies per GB</text>

<!-- Sub-box: Failover Guarantee -->
<rect x="295" y="500" width="220" height="70" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="305" y="520" fill="#94a3b8" font-size="10" font-weight="600">Disaster Failover Engine</text>
<text x="305" y="536" fill="#cbd5e1" font-size="10">Zero-downtime read/write shift</text>
<text x="305" y="552" fill="#38bdf8" font-size="10">Independent of primary region health</text>


<!-- Column 3: Storage Classes & Autoclass Lifecycle -->
<rect x="540" y="80" width="240" height="505" rx="6" fill="#090d16" stroke="#475569" stroke-width="1.5"/>
<text x="555" y="105" fill="#f1f5f9" font-size="13" font-weight="700">3 · Autoclass &amp; Classes</text>
<text x="555" y="122" fill="#94a3b8" font-size="11">Tiering, Duration &amp; Retrieval</text>

<!-- Sub-box: Autoclass Engine -->
<rect x="550" y="135" width="220" height="70" rx="4" fill="#2e1065" stroke="#c084fc" stroke-width="1.5"/>
<text x="560" y="155" fill="#e9d5ff" font-size="11" font-weight="700">Autoclass Management</text>
<text x="560" y="171" fill="#cbd5e1" font-size="10">Automated access tracking daemon</text>
<text x="560" y="187" fill="#d8b4fe" font-size="10">Eliminates manual lifecycle scripts</text>

<!-- Sub-box: Standard Tier -->
<rect x="550" y="215" width="220" height="55" rx="4" fill="#1e293b" stroke="#3b82f6" stroke-width="1"/>
<text x="560" y="233" fill="#60a5fa" font-size="10" font-weight="700">Standard Tier (Hot Data)</text>
<text x="560" y="247" fill="#cbd5e1" font-size="9">0-day min duration | $0.00 retrieval</text>
<text x="560" y="260" fill="#94a3b8" font-size="9">Frequent daily access &amp; analytics</text>

<!-- Sub-box: Nearline Tier -->
<rect x="550" y="278" width="220" height="55" rx="4" fill="#1e293b" stroke="#06b6d4" stroke-width="1"/>
<text x="560" y="296" fill="#22d3ee" font-size="10" font-weight="700">Nearline Tier (30-Day Min)</text>
<text x="560" y="310" fill="#cbd5e1" font-size="9">30-day inactivity demotion</text>
<text x="560" y="323" fill="#f87171" font-size="9">Early delete fee if removed &lt;30d</text>

<!-- Sub-box: Coldline Tier -->
<rect x="550" y="341" width="220" height="55" rx="4" fill="#1e293b" stroke="#818cf8" stroke-width="1"/>
<text x="560" y="359" fill="#a5b4fc" font-size="10" font-weight="700">Coldline Tier (90-Day Min)</text>
<text x="560" y="373" fill="#cbd5e1" font-size="9">90-day inactivity demotion</text>
<text x="560" y="386" fill="#f87171" font-size="9">Early delete fee if removed &lt;90d</text>

<!-- Sub-box: Archive Tier -->
<rect x="550" y="404" width="220" height="55" rx="4" fill="#1e293b" stroke="#a855f7" stroke-width="1"/>
<text x="560" y="422" fill="#c084fc" font-size="10" font-weight="700">Archive Tier (365-Day Min)</text>
<text x="560" y="436" fill="#cbd5e1" font-size="9">365-day inactivity | Long-term WORM</text>
<text x="560" y="449" fill="#f87171" font-size="9">Early delete fee if removed &lt;365d</text>

<!-- Sub-box: Auto-Promotion on Read -->
<rect x="550" y="468" width="220" height="102" rx="4" fill="#052e16" stroke="#22c55e" stroke-width="1.5"/>
<text x="560" y="488" fill="#4ade80" font-size="10" font-weight="700">Zero-Fee Auto-Promotion on Read</text>
<text x="560" y="504" fill="#a7f3d0" font-size="9">Reading cold object moves to Standard</text>
<text x="560" y="518" fill="#34d399" font-size="9">NO data retrieval surcharges applied!</text>
<text x="560" y="534" fill="#cbd5e1" font-size="9">Soft Delete: 7-day default restore window</text>
<text x="560" y="550" fill="#94a3b8" font-size="9">Protects versioned &amp; live objects</text>


<!-- Column 4: Compliance & Retention Engine -->
<rect x="795" y="80" width="235" height="505" rx="6" fill="#0f172a" stroke="#f43f5e" stroke-width="1.5"/>
<text x="810" y="105" fill="#fb7185" font-size="13" font-weight="700">4 · Compliance &amp; WORM</text>
<text x="810" y="122" fill="#94a3b8" font-size="11">SEC 17a-4, Holds &amp; Bucket Lock</text>

<!-- Sub-box: Retention Policy -->
<rect x="805" y="135" width="215" height="75" rx="4" fill="#1e293b" stroke="#f43f5e" stroke-width="1"/>
<text x="815" y="155" fill="#fb7185" font-size="11" font-weight="700">WORM Retention Policy</text>
<text x="815" y="171" fill="#cbd5e1" font-size="10">Period: 7 Years (220,752,000s)</text>
<text x="815" y="187" fill="#fca5a5" font-size="10">Objects cannot be overwritten</text>
<text x="815" y="201" fill="#94a3b8" font-size="9">SEC 17a-4 / FINRA 4511 certified</text>

<!-- Sub-box: Event-Based Holds -->
<rect x="805" y="220" width="215" height="80" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
<text x="815" y="240" fill="#fcd34d" font-size="11" font-weight="700">Event-Based Holds</text>
<text x="815" y="256" fill="#cbd5e1" font-size="10">Indefinite freeze during contract</text>
<text x="815" y="272" fill="#fde68a" font-size="10">Countdown begins on hold release</text>
<text x="815" y="288" fill="#94a3b8" font-size="9">E.g. Loan payoff / Employee exit</text>

<!-- Sub-box: Temporary Legal Holds -->
<rect x="805" y="310" width="215" height="80" rx="4" fill="#1e293b" stroke="#e11d48" stroke-width="1"/>
<text x="815" y="330" fill="#fda4af" font-size="11" font-weight="700">Temporary Legal Holds</text>
<text x="815" y="346" fill="#cbd5e1" font-size="10">Litigation discovery freeze</text>
<text x="815" y="362" fill="#fb7185" font-size="10">Blocks delete even if period ends</text>
<text x="815" y="378" fill="#94a3b8" font-size="9">Released exclusively by Legal IAM</text>

<!-- Sub-box: Immutable Bucket Lock -->
<rect x="805" y="400" width="215" height="85" rx="4" fill="#4c0519" stroke="#f43f5e" stroke-width="2"/>
<text x="815" y="420" fill="#fecdd3" font-size="11" font-weight="700">Immutable Bucket Lock</text>
<text x="815" y="436" fill="#ffffff" font-size="10" font-weight="700">isLocked: true (IRREVERSIBLE)</text>
<text x="815" y="452" fill="#fda4af" font-size="10">Policy CANNOT be deleted</text>
<text x="815" y="468" fill="#fca5a5" font-size="10">Duration can ONLY be increased</text>

<!-- Sub-box: Blast Radius Safeguards -->
<rect x="805" y="495" width="215" height="75" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="815" y="515" fill="#94a3b8" font-size="10" font-weight="600">Blast Radius Safeguards</text>
<text x="815" y="531" fill="#cbd5e1" font-size="10">Bucket cannot be destroyed</text>
<text x="815" y="547" fill="#f87171" font-size="10">Dual-custody approval required</text>
<text x="815" y="561" fill="#94a3b8" font-size="9">Never lock staging/test buckets</text>


<!-- Connecting Flow Paths -->
<!-- 1. Direct Commit Flow: Ingestion -> Spanner & Colossus -->
<path d="M 255 350 L 295 260" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d58-m-write)"/>
<path d="M 255 350 L 295 350" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d58-m-write)"/>

<!-- 2. Turbo Replication Flow: Colossus Primary -> Turbo Channel -> Destination -->
<path d="M 405 395 L 405 405" fill="none" stroke="#f59e0b" stroke-width="2.5" marker-end="url(#d58-m-rep)"/>
<path d="M 515 447 C 530 447, 530 170, 550 170" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#d58-m-rep)"/>

<!-- 3. Tiering Flow: Standard -> Nearline -> Coldline -> Archive -->
<path d="M 660 270 L 660 278" fill="none" stroke="#c084fc" stroke-width="2" marker-end="url(#d58-m-tier)"/>
<path d="M 660 333 L 660 341" fill="none" stroke="#c084fc" stroke-width="2" marker-end="url(#d58-m-tier)"/>
<path d="M 660 396 L 660 404" fill="none" stroke="#c084fc" stroke-width="2" marker-end="url(#d58-m-tier)"/>

<!-- 4. Auto-Promotion Loopback: Cold Read -> Standard -->
<path d="M 770 490 C 785 490, 785 242, 770 242" fill="none" stroke="#22c55e" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#d58-m-write)"/>

<!-- 5. WORM Enforcement Flow: Archive/Object -> Holds -> Bucket Lock -->
<path d="M 770 430 L 805 170" fill="none" stroke="#f43f5e" stroke-width="2" marker-end="url(#d58-m-lock)"/>
<path d="M 912 210 L 912 220" fill="none" stroke="#f43f5e" stroke-width="2" marker-end="url(#d58-m-lock)"/>
<path d="M 912 300 L 912 310" fill="none" stroke="#f43f5e" stroke-width="2" marker-end="url(#d58-m-lock)"/>
<path d="M 912 390 L 912 400" fill="none" stroke="#f43f5e" stroke-width="2.5" marker-end="url(#d58-m-lock)"/>
</svg>
<figcaption>Figure 58.1: Cloud Storage Durability, Turbo Replication, Autoclass Lifecycle &amp; WORM Compliance Architecture. <strong>Supplied facts:</strong> POSIX dirty cache commits to disk only on <code>fsync()</code>/<code>fdatasync()</code>, while Cloud Storage provides global strong read-after-write consistency upon HTTP 200. Dual-region Turbo Replication guarantees 15-minute cross-region RPO SLA. Autoclass transitions inactive objects and auto-promotes on read with $0 retrieval fees. Bucket Lock irreversibly enforces SEC 17a-4 WORM compliance. <strong>Architectural inference:</strong> Decoupling local compute buffer flushes from Colossus distributed commit prevents partial data ingestion, while Autoclass avoids early deletion penalties. Locking retention policies permanently protects audit ledgers from privileged insider tampering. <strong>Expected post-fix behavior:</strong> Microservices stream orders directly with generation preconditions, achieving 100% atomic idempotency, 15-minute cross-region RPO, zero retrieval penalties, and immutable 7-year audit retention.</figcaption>
</figure>"""


FIG_58_2_INCIDENT_1_SVG = """<figure class="diagram-figure">
<svg role="img" aria-labelledby="d58-i1-title d58-i1-desc" viewBox="0 0 980 280" width="100%" height="auto" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d58-i1-title">Incident 1: POSIX Dirty Buffer Crash &amp; Lifecycle Fee Spiral vs fdatasync and Autoclass Governance</title>
<desc id="d58-i1-desc">Diagram showing failed path where uncommitted POSIX buffer cache and aggressive OLM lifecycle demotion caused data loss and early deletion penalties, followed by corrected path with synchronous fdatasync, dual-region Turbo Replication, and Autoclass.</desc>
<defs>
<marker id="d58-i1-mf" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/>
</marker>
<marker id="d58-i1-mc" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
</defs>

<!-- Failed Path Box -->
<rect x="20" y="20" width="940" height="110" rx="6" fill="#1e1b2e" stroke="#f43f5e" stroke-width="1.5"/>
<text x="35" y="45" fill="#f43f5e" font-size="13" font-weight="700">FAILED PATH: POSIX Dirty Cache Preemption &amp; Aggressive OLM Early Deletion Penalties</text>

<rect x="40" y="60" width="220" height="50" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="50" y="80" fill="#f1f5f9" font-size="11" font-weight="600">App Worker (No fsync)</text>
<text x="50" y="96" fill="#94a3b8" font-size="10">Dirty pages in RAM buffer cache</text>

<rect x="330" y="60" width="240" height="50" rx="4" fill="#4c0519" stroke="#f43f5e" stroke-width="1.5"/>
<text x="340" y="80" fill="#fda4af" font-size="11" font-weight="700">Worker Crash / Truncated Upload</text>
<text x="340" y="96" fill="#fecdd3" font-size="10">No generation precondition (Race overwrite)</text>

<rect x="680" y="60" width="260" height="50" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1"/>
<text x="690" y="80" fill="#f1f5f9" font-size="11" font-weight="600">OLM Day 10 Coldline Demote</text>
<text x="690" y="96" fill="#f43f5e" font-size="10">Early delete penalty + $62K retrieval</text>

<path d="M 260 85 L 330 85" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d58-i1-mf)"/>
<path d="M 570 85 L 680 85" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d58-i1-mf)"/>

<!-- Corrected Path Box -->
<rect x="20" y="145" width="940" height="115" rx="6" fill="#0f291e" stroke="#22c55e" stroke-width="1.5"/>
<text x="35" y="170" fill="#4ade80" font-size="13" font-weight="700">CORRECTED PATH: fdatasync Flush / Direct CRC32c Stream, Turbo Replication &amp; Autoclass</text>

<rect x="40" y="185" width="220" height="55" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="50" y="205" fill="#f1f5f9" font-size="11" font-weight="600">Worker: fdatasync() / CRC32c</text>
<text x="50" y="221" fill="#86efac" font-size="10">Direct Resumable Stream to GCS</text>

<rect x="330" y="185" width="240" height="55" rx="4" fill="#064e3b" stroke="#34d399" stroke-width="1.5"/>
<text x="340" y="205" fill="#a7f3d0" font-size="11" font-weight="700">Dual-Region Turbo (nam4)</text>
<text x="340" y="221" fill="#cbd5e1" font-size="10">15-min RPO SLA &amp; if-generation-match: 0</text>

<rect x="680" y="185" width="260" height="55" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="690" y="205" fill="#f1f5f9" font-size="11" font-weight="600">Autoclass Dynamic Tiering</text>
<text x="690" y="221" fill="#86efac" font-size="10">$0 retrieval fee on read; 0 penalty</text>

<path d="M 260 212 L 330 212" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d58-i1-mc)"/>
<path d="M 570 212 L 680 212" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d58-i1-mc)"/>

<!-- Verify Boundary -->
<rect x="320" y="180" width="260" height="65" rx="6" fill="none" stroke="#f59e0b" stroke-width="1" stroke-dasharray="4,4"/>
<text x="325" y="172" fill="#fbbf24" font-size="10" font-weight="600">VERIFY BOUNDARY: Atomic Precondition &amp; Turbo RPO</text>
</svg>
<figcaption>Figure 58.2: Incident 1 Root Cause and Remediation. <strong>Supplied facts:</strong> POSIX dirty buffer writes without explicit flush caused partial object uploads during worker preemption, while aggressive OLM demotion incurred massive early deletion and retrieval surcharges. <strong>Architectural inference:</strong> Enforcing <code>fdatasync()</code> prior to upload or streaming directly with CRC32c validation guarantees data integrity, while <code>x-goog-if-generation-match: 0</code> prevents race overwrites. Autoclass eliminates early deletion fees and enables zero-fee read promotions. <strong>Expected post-fix behavior:</strong> 100% of order invoices achieve immediate global durability, dual-region replication commits across us-central1 and us-east1 in &lt;15 minutes, and Autoclass eliminates $62,000/month in unexpected data retrieval penalties.</figcaption>
</figure>"""


FIG_58_3_INCIDENT_2_SVG = """<figure class="diagram-figure">
<svg role="img" aria-labelledby="d58-i2-title d58-i2-desc" viewBox="0 0 980 280" width="100%" height="auto" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d58-i2-title">Incident 2: Unlocked Retention Policy Deletion vs Immutable Bucket Lock and Legal Holds</title>
<desc id="d58-i2-desc">Diagram showing failed path where unlocked retention policy was cleared by compromised admin credential destroying compliance logs, followed by corrected path with immutable Bucket Lock and Event-based holds blocking deletion attempts.</desc>
<defs>
<marker id="d58-i2-mf" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/>
</marker>
<marker id="d58-i2-mc" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
</defs>

<!-- Failed Path Box -->
<rect x="20" y="20" width="940" height="110" rx="6" fill="#1e1b2e" stroke="#f43f5e" stroke-width="1.5"/>
<text x="35" y="45" fill="#f43f5e" font-size="13" font-weight="700">FAILED PATH: Unlocked Retention Policy Cleared by Compromised CI/CD Service Account</text>

<rect x="40" y="60" width="220" height="50" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="50" y="80" fill="#f1f5f9" font-size="11" font-weight="600">Unlocked Retention (7yr)</text>
<text x="50" y="96" fill="#94a3b8" font-size="10">isLocked: false (Permits mutation)</text>

<rect x="330" y="60" width="240" height="50" rx="4" fill="#4c0519" stroke="#f43f5e" stroke-width="1.5"/>
<text x="340" y="80" fill="#fda4af" font-size="11" font-weight="700">Compromised Service Account</text>
<text x="340" y="96" fill="#fecdd3" font-size="10">Executes clear-retention-policy</text>

<rect x="680" y="60" width="260" height="50" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1"/>
<text x="690" y="80" fill="#f1f5f9" font-size="11" font-weight="600">Compliance Ledgers Purged</text>
<text x="690" y="96" fill="#f43f5e" font-size="10">SEC 17a-4 breach; $1.4M regulatory fine</text>

<path d="M 260 85 L 330 85" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d58-i2-mf)"/>
<path d="M 570 85 L 680 85" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d58-i2-mf)"/>

<!-- Corrected Path Box -->
<rect x="20" y="145" width="940" height="115" rx="6" fill="#0f291e" stroke="#22c55e" stroke-width="1.5"/>
<text x="35" y="170" fill="#4ade80" font-size="13" font-weight="700">CORRECTED PATH: Immutable Bucket Lock (isLocked: true) &amp; Dual-Custody Legal Holds</text>

<rect x="40" y="185" width="220" height="55" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="50" y="205" fill="#f1f5f9" font-size="11" font-weight="600">Locked Retention Policy</text>
<text x="50" y="221" fill="#86efac" font-size="10">isLocked: true (IRREVERSIBLE)</text>

<rect x="330" y="185" width="240" height="55" rx="4" fill="#064e3b" stroke="#34d399" stroke-width="1.5"/>
<text x="340" y="205" fill="#a7f3d0" font-size="11" font-weight="700">WORM Enforcement Engine</text>
<text x="340" y="221" fill="#cbd5e1" font-size="10">Event-based &amp; Temporary holds active</text>

<rect x="680" y="185" width="260" height="55" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="690" y="205" fill="#f1f5f9" font-size="11" font-weight="600">Deletion Attempt Rejected</text>
<text x="690" y="221" fill="#86efac" font-size="10">HTTP 403 WORM Lock; 100% audit retention</text>

<path d="M 260 212 L 330 212" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d58-i2-mc)"/>
<path d="M 570 212 L 680 212" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d58-i2-mc)"/>

<!-- Verify Boundary -->
<rect x="320" y="180" width="260" height="65" rx="6" fill="none" stroke="#f59e0b" stroke-width="1" stroke-dasharray="4,4"/>
<text x="325" y="172" fill="#fbbf24" font-size="10" font-weight="600">VERIFY BOUNDARY: Irreversible Bucket Lock &amp; WORM</text>
</svg>
<figcaption>Figure 58.3: Incident 2 Root Cause and Remediation. <strong>Supplied facts:</strong> An unlocked retention policy was deleted by a compromised admin credential, purging regulatory compliance ledgers. <strong>Architectural inference:</strong> Bucket Lock permanently prevents deletion or reduction of retention policies, even by Google Cloud project owners. Event-Based and Temporary Holds provide operational and legal flexibility without compromising WORM integrity. <strong>Expected post-fix behavior:</strong> Cloud Storage rejects any object deletion or retention clearance with HTTP 403 Forbidden; audit ledgers remain mathematically immutable for the required 7-year regulatory period.</figcaption>
</figure>"""
print("blocks_svg.py written")
