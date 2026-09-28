"""Part 2 Architectural SVG Diagram for Day 62."""

def get_part2_svg():
    return """<figure class="diagram-figure">
<svg role="img" aria-labelledby="d62-arch-title d62-arch-desc" viewBox="0 0 1080 780" width="100%" height="auto" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d62-arch-title">Google Cloud Distributed Database Fabric: Spanner, Firestore, and Bigtable Architectures</title>
<desc id="d62-arch-desc">Comprehensive architectural topology detailing Cloud Spanner TrueTime commit-wait and multi-region Paxos quorum consensus, Cloud Firestore sharded counter and composite index pipeline, and Cloud Bigtable stateless tablet server Colossus fabric with lexicographical row key range scanning and multi-cluster replication routing.</desc>
<defs>
<marker id="d62-m-spanner" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#38bdf8"/>
</marker>
<marker id="d62-m-paxos" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#a855f7"/>
</marker>
<marker id="d62-m-fire" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/>
</marker>
<marker id="d62-m-bigtable" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
<marker id="d62-m-colossus" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#ec4899"/>
</marker>
<marker id="d62-m-sync" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#06b6d4"/>
</marker>
</defs>

<!-- SECTION 1: CLOUD SPANNER ARCHITECTURE -->
<rect x="20" y="20" width="1040" height="240" rx="6" fill="#131b2e" stroke="#1e293b" stroke-width="1.5"/>
<text x="35" y="42" fill="#38bdf8" font-size="13" font-weight="700">1. CLOUD SPANNER: TrueTime External Consistency, Multi-Region Paxos Quorum &amp; Interleaving</text>

<!-- TrueTime Engine Box -->
<rect x="35" y="55" width="270" height="190" rx="4" fill="#0f172a" stroke="#0284c7" stroke-width="1"/>
<text x="45" y="75" fill="#38bdf8" font-size="11" font-weight="700">TrueTime API &amp; Master Clocks</text>
<text x="45" y="93" fill="#cbd5e1" font-size="10">GPS Receivers + Rubidium Atomic Clocks</text>
<text x="45" y="109" fill="#94a3b8" font-size="10">Bounded Time Uncertainty Interval:</text>
<rect x="45" y="117" width="250" height="30" rx="3" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
<text x="55" y="136" fill="#7dd3fc" font-family="monospace" font-size="10">now() = [t.earliest, t.latest] (e ~ 1-7ms)</text>
<text x="45" y="163" fill="#f59e0b" font-size="10">&#9733; Commit Wait Rule (External Consistency):</text>
<text x="45" y="179" fill="#fde68a" font-size="10">Hold commit lock until TrueTime &gt; t.latest</text>
<text x="45" y="195" fill="#94a3b8" font-size="10">Guarantees global causal transaction order</text>
<text x="45" y="211" fill="#22c55e" font-size="10">Zero read locks for global snapshot reads</text>
<text x="45" y="227" fill="#94a3b8" font-size="10">Regional (99.99%) vs Multi-Region nam3 (99.999%)</text>

<!-- Multi-Region Paxos Topology Box -->
<rect x="320" y="55" width="410" height="190" rx="4" fill="#0f172a" stroke="#a855f7" stroke-width="1"/>
<text x="330" y="75" fill="#c084fc" font-size="11" font-weight="700">Multi-Region Paxos Consensus Group (e.g., nam3)</text>

<!-- Zone 1: Leader -->
<rect x="330" y="85" width="125" height="145" rx="4" fill="#1e1b4b" stroke="#818cf8" stroke-width="1"/>
<text x="338" y="103" fill="#c7d2fe" font-size="10" font-weight="700">us-east4 (Zone A)</text>
<text x="338" y="119" fill="#38bdf8" font-size="10">&#9679; PAXOS LEADER</text>
<text x="338" y="135" fill="#cbd5e1" font-size="9">Handles R/W Tx</text>
<text x="338" y="151" fill="#cbd5e1" font-size="9">Acquires 2PL locks</text>
<text x="338" y="167" fill="#f59e0b" font-size="9">Assigns TrueTime s</text>
<text x="338" y="183" fill="#ec4899" font-size="9">Waits commit window</text>
<text x="338" y="199" fill="#22c55e" font-size="9">Split Rebalancer</text>
<text x="338" y="215" fill="#94a3b8" font-size="9">Colossus SSTables</text>

<!-- Zone 2: Voting Replica -->
<rect x="465" y="85" width="125" height="145" rx="4" fill="#1e1b4b" stroke="#818cf8" stroke-width="1"/>
<text x="473" y="103" fill="#c7d2fe" font-size="10" font-weight="700">us-central1 (Zone B)</text>
<text x="473" y="119" fill="#a855f7" font-size="10">&#9679; VOTING REPLICA</text>
<text x="473" y="135" fill="#cbd5e1" font-size="9">Participates in Quorum</text>
<text x="473" y="151" fill="#cbd5e1" font-size="9">Votes on Paxos logs</text>
<text x="473" y="167" fill="#22c55e" font-size="9">Serves local snapshot</text>
<text x="473" y="183" fill="#38bdf8" font-size="9">Promotable to Leader</text>
<text x="473" y="199" fill="#94a3b8" font-size="9">Quorum = 2 of 3 votes</text>
<text x="473" y="215" fill="#94a3b8" font-size="9">Colossus SSTables</text>

<!-- Zone 3: Witness Replica -->
<rect x="600" y="85" width="120" height="145" rx="4" fill="#1e1b4b" stroke="#818cf8" stroke-width="1"/>
<text x="608" y="103" fill="#c7d2fe" font-size="10" font-weight="700">us-east1 (Zone C)</text>
<text x="608" y="119" fill="#f59e0b" font-size="10">&#9679; WITNESS REPLICA</text>
<text x="608" y="135" fill="#cbd5e1" font-size="9">Votes in Paxos Quorum</text>
<text x="608" y="151" fill="#cbd5e1" font-size="9">Stores zero data rows</text>
<text x="608" y="167" fill="#cbd5e1" font-size="9">Ties breaker in failover</text>
<text x="608" y="183" fill="#22c55e" font-size="9">Zero storage charge</text>
<text x="608" y="199" fill="#94a3b8" font-size="9">RPO = 0 across regions</text>
<text x="608" y="215" fill="#94a3b8" font-size="9">Tie-breaker node</text>

<!-- Schema Interleaving & Hotspotting Box -->
<rect x="745" y="55" width="300" height="190" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1"/>
<text x="755" y="75" fill="#4ade80" font-size="11" font-weight="700">Table Interleaving &amp; Anti-Hotspotting</text>
<rect x="755" y="85" width="280" height="85" rx="3" fill="#022c22" stroke="#059669" stroke-width="1"/>
<text x="765" y="101" fill="#a7f3d0" font-size="10" font-weight="700">Interleaved Parent-Child Storage:</text>
<text x="765" y="117" fill="#86efac" font-size="9">Customers (CustomerID [PK])</text>
<text x="765" y="131" fill="#cbd5e1" font-size="9">&rarr; Orders (CustomerID, OrderID) [INTERLEAVED]</text>
<text x="765" y="145" fill="#cbd5e1" font-size="9">&rarr; OrderItems (CustID, OrdID, ItemID) [INTERLEAVED]</text>
<text x="765" y="159" fill="#38bdf8" font-size="9">&#9733; Co-located on single split &rarr; Atomic, zero 2PC</text>
<text x="755" y="185" fill="#f43f5e" font-size="10">&#9888; Anti-Pattern: Monotonic Key (Timestamp)</text>
<text x="755" y="199" fill="#fecdd3" font-size="9">Funnels 100% writes to 1 split &rarr; Hotspot saturation</text>
<text x="755" y="215" fill="#22c55e" font-size="10">&#10004; Remedy: Bit-Reversed Key / UUIDv4 / Hash</text>
<text x="755" y="229" fill="#a7f3d0" font-size="9">Uniform write distribution across all Paxos splits</text>

<!-- Connectors in Section 1 -->
<path d="M 305 130 L 330 130" fill="none" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#d62-m-spanner)"/>
<path d="M 455 130 L 465 130" fill="none" stroke="#a855f7" stroke-width="1.5" marker-end="url(#d62-m-paxos)"/>
<path d="M 590 130 L 600 130" fill="none" stroke="#a855f7" stroke-width="1.5" marker-end="url(#d62-m-paxos)"/>

<!-- SECTION 2: CLOUD FIRESTORE ARCHITECTURE -->
<rect x="20" y="275" width="1040" height="235" rx="6" fill="#131b2e" stroke="#1e293b" stroke-width="1.5"/>
<text x="35" y="297" fill="#f59e0b" font-size="13" font-weight="700">2. CLOUD FIRESTORE: Document Model, 1 Write/Sec Limit, Sharded Counter &amp; Index Pipeline</text>

<!-- Client & Realtime Listen Box -->
<rect x="35" y="310" width="270" height="185" rx="4" fill="#0f172a" stroke="#d97706" stroke-width="1"/>
<text x="45" y="330" fill="#fbbf24" font-size="11" font-weight="700">Client Integration &amp; Real-time Sync</text>
<text x="45" y="348" fill="#cbd5e1" font-size="10">Mobile / Web App Clients (SDKs)</text>
<text x="45" y="364" fill="#94a3b8" font-size="10">Bidirectional gRPC / WebSocket listen streams</text>
<text x="45" y="380" fill="#f59e0b" font-size="10">&#9679; Offline Client Cache (SQLite / IndexedDB):</text>
<text x="45" y="396" fill="#cbd5e1" font-size="9">Local mutation queue &amp; zero-latency reads</text>
<text x="45" y="410" fill="#cbd5e1" font-size="9">Automatic delta sync upon reconnection</text>
<text x="45" y="426" fill="#38bdf8" font-size="10">&#9679; Declarative Security Rules (RBAC):</text>
<text x="45" y="442" fill="#cbd5e1" font-size="9">request.auth.uid == resource.data.ownerId</text>
<text x="45" y="456" fill="#22c55e" font-size="9">Enforces document-level authorization</text>
<text x="45" y="472" fill="#94a3b8" font-size="9">Max document size: 1 MB payload</text>

<!-- Sharded Counter Pattern Box -->
<rect x="320" y="310" width="410" height="185" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1"/>
<text x="330" y="330" fill="#fbbf24" font-size="11" font-weight="700">Scalability Limits &amp; Distributed Sharded Counter Pattern</text>

<rect x="330" y="340" width="390" height="40" rx="3" fill="#4c0519" stroke="#f43f5e" stroke-width="1"/>
<text x="340" y="356" fill="#fda4af" font-size="10" font-weight="700">&#9888; Physical Bottleneck: 1 Write / Second / Document</text>
<text x="340" y="370" fill="#fecdd3" font-size="9">Single document updates require Paxos consensus &rarr; High write rate causes aborts</text>

<rect x="330" y="388" width="390" height="98" rx="3" fill="#064e3b" stroke="#22c55e" stroke-width="1"/>
<text x="340" y="404" fill="#86efac" font-size="10" font-weight="700">&#10004; Sharded Counter Architecture (N = 20 to 50 shards):</text>
<text x="340" y="418" fill="#ecfdf5" font-size="9">Path: /counters/flash_sale_promo/shards/{shard_id}</text>
<text x="340" y="432" fill="#cbd5e1" font-size="9">Write: Pick shard_id = random(0, N-1) &rarr; Increment shard atomically</text>
<text x="340" y="446" fill="#38bdf8" font-size="9">Throughput: N * 1 write/sec (50 shards = 50 writes/sec sustained)</text>
<text x="340" y="460" fill="#fde68a" font-size="9">Read: Server-side Aggregation Query: db.collection(...).aggregate(sum('count'))</text>
<text x="340" y="474" fill="#a7f3d0" font-size="9">Zero client-side merge toil &bull; Eliminates contention rollbacks</text>

<!-- Indexing Pipeline Box -->
<rect x="745" y="310" width="300" height="185" rx="4" fill="#0f172a" stroke="#a855f7" stroke-width="1"/>
<text x="755" y="330" fill="#c084fc" font-size="11" font-weight="700">Firestore Query &amp; Index Engine</text>
<rect x="755" y="340" width="280" height="52" rx="3" fill="#1e1b4b" stroke="#6366f1" stroke-width="1"/>
<text x="765" y="356" fill="#c7d2fe" font-size="10" font-weight="700">Single-Field vs Composite Indexes</text>
<text x="765" y="370" fill="#94a3b8" font-size="9">Automatic: Ascending &amp; Descending on all scalar fields</text>
<text x="765" y="384" fill="#cbd5e1" font-size="9">Zigzag Merge Join: In-memory join of single-field indexes</text>

<rect x="755" y="398" width="280" height="90" rx="3" fill="#18181b" stroke="#334155" stroke-width="1"/>
<text x="765" y="414" fill="#38bdf8" font-size="10" font-weight="700">Composite Indexes (firestore.indexes.json)</text>
<text x="765" y="428" fill="#cbd5e1" font-size="9">Required for: Equality + Inequality + OrderBy</text>
<text x="765" y="442" fill="#ec4899" font-size="9">Example: status == 'OPEN' &amp;&amp; created &gt; T ORDER BY created</text>
<text x="765" y="456" fill="#f59e0b" font-size="9">&#9733; Index Exemptions:</text>
<text x="765" y="470" fill="#cbd5e1" font-size="9">Exempt high-cardinality/unqueried fields</text>
<text x="765" y="482" fill="#22c55e" font-size="9">Prevents write amplification &amp; storage bloat</text>

<!-- Connectors in Section 2 -->
<path d="M 305 380 L 330 380" fill="none" stroke="#f59e0b" stroke-width="1.5" marker-end="url(#d62-m-fire)"/>
<path d="M 730 400 L 745 400" fill="none" stroke="#a855f7" stroke-width="1.5" marker-end="url(#d62-m-paxos)"/>

<!-- SECTION 3: CLOUD BIGTABLE ARCHITECTURE -->
<rect x="20" y="525" width="1040" height="235" rx="6" fill="#131b2e" stroke="#1e293b" stroke-width="1.5"/>
<text x="35" y="547" fill="#22c55e" font-size="13" font-weight="700">3. CLOUD BIGTABLE: Disaggregated Storage, Row Key Design &amp; Multi-Cluster Replication</text>

<!-- Row Key Engineering Box -->
<rect x="35" y="560" width="310" height="185" rx="4" fill="#0f172a" stroke="#16a34a" stroke-width="1"/>
<text x="45" y="580" fill="#4ade80" font-size="11" font-weight="700">Row Key Engineering (Single Primary Index)</text>
<text x="45" y="598" fill="#cbd5e1" font-size="10">All rows sorted lexicographically (byte-by-byte)</text>

<rect x="45" y="608" width="290" height="42" rx="3" fill="#4c0519" stroke="#f43f5e" stroke-width="1"/>
<text x="55" y="622" fill="#fda4af" font-size="10" font-weight="700">&#9888; Anti-Pattern: YYYY-MM-DD#DeviceID</text>
<text x="55" y="636" fill="#fecdd3" font-size="9">Monotonic timestamp funnels 100% writes to last tablet</text>

<rect x="45" y="656" width="290" height="78" rx="3" fill="#064e3b" stroke="#22c55e" stroke-width="1"/>
<text x="55" y="670" fill="#86efac" font-size="10" font-weight="700">&#10004; Production Composite Salted Reverse Row Key:</text>
<text x="55" y="684" fill="#a7f3d0" font-family="monospace" font-size="9">HASH(dev)[0:4]#tenant#dev#~timestamp</text>
<text x="55" y="698" fill="#cbd5e1" font-size="9">where ~timestamp = Long.MAX_VALUE - timestamp</text>
<text x="55" y="712" fill="#38bdf8" font-size="9">&#9658; Hash prefix: Distributes writes across all tablets</text>
<text x="55" y="724" fill="#22c55e" font-size="9">&#9658; Reverse TS: Fast descending time-series scans</text>

<!-- Tablet Server & Colossus Fabric Box -->
<rect x="360" y="560" width="370" height="185" rx="4" fill="#0f172a" stroke="#059669" stroke-width="1"/>
<text x="370" y="580" fill="#34d399" font-size="11" font-weight="700">Stateless Tablet Servers &amp; Colossus Storage</text>

<!-- Tablet Server Nodes -->
<rect x="370" y="590" width="165" height="145" rx="3" fill="#022c22" stroke="#10b981" stroke-width="1"/>
<text x="378" y="608" fill="#a7f3d0" font-size="10" font-weight="700">Tablet Servers (Stateless)</text>
<text x="378" y="624" fill="#cbd5e1" font-size="9">Compute Fleet (Nodes)</text>
<text x="378" y="638" fill="#38bdf8" font-size="9">MemTable in RAM</text>
<text x="378" y="652" fill="#38bdf8" font-size="9">Block Cache in RAM</text>
<text x="378" y="666" fill="#f59e0b" font-size="9">Tablet Splits rebalance</text>
<text x="378" y="680" fill="#cbd5e1" font-size="9">in seconds (no data move)</text>
<text x="378" y="694" fill="#22c55e" font-size="9">10k-14k QPS per node</text>
<text x="378" y="708" fill="#94a3b8" font-size="9">Linear compute scaling</text>

<!-- Colossus Storage Filesystem -->
<rect x="550" y="590" width="170" height="145" rx="3" fill="#18181b" stroke="#52525b" stroke-width="1"/>
<text x="558" y="608" fill="#f4f4f5" font-size="10" font-weight="700">Colossus File System</text>
<text x="558" y="624" fill="#ec4899" font-size="9">Shared Distributed Disk</text>
<text x="558" y="638" fill="#cbd5e1" font-size="9">Write-Ahead Log (WAL)</text>
<text x="558" y="652" fill="#cbd5e1" font-size="9">Immutable SSTables</text>
<text x="558" y="666" fill="#818cf8" font-size="9">Minor &amp; Major Compactions</text>
<text x="558" y="680" fill="#f59e0b" font-size="9">Garbage Collection (GC):</text>
<text x="558" y="694" fill="#cbd5e1" font-size="9">Max versions &amp; max age</text>
<text x="558" y="708" fill="#22c55e" font-size="9">Zero checkpoint stalls</text>

<!-- Replication & App Profiles Box -->
<rect x="745" y="560" width="300" height="185" rx="4" fill="#0f172a" stroke="#06b6d4" stroke-width="1"/>
<text x="755" y="580" fill="#22d3ee" font-size="11" font-weight="700">Multi-Cluster Replication &amp; Routing</text>
<rect x="755" y="590" width="280" height="65" rx="3" fill="#164e63" stroke="#0891b2" stroke-width="1"/>
<text x="765" y="606" fill="#a5f3fc" font-size="10" font-weight="700">App Profile: Multi-Cluster Routing</text>
<text x="765" y="620" fill="#cbd5e1" font-size="9">Automated cross-cluster failover &bull; 99.999% SLA</text>
<text x="765" y="634" fill="#f59e0b" font-size="9">Eventual consistency model across regions</text>
<text x="765" y="646" fill="#cbd5e1" font-size="9">Ideal for high-throughput IoT &amp; write feeds</text>

<rect x="755" y="662" width="280" height="72" rx="3" fill="#1e1b4b" stroke="#6366f1" stroke-width="1"/>
<text x="765" y="678" fill="#c7d2fe" font-size="10" font-weight="700">App Profile: Single-Cluster Routing</text>
<text x="765" y="692" fill="#cbd5e1" font-size="9">Routes to fixed cluster (e.g. us-central1-a)</text>
<text x="765" y="706" fill="#22c55e" font-size="9">Strict Read-Your-Writes consistency</text>
<text x="765" y="718" fill="#cbd5e1" font-size="9">Manual failover control &bull; 99.9% SLA</text>

<!-- Connectors in Section 3 -->
<path d="M 345 650 L 360 650" fill="none" stroke="#22c55e" stroke-width="1.5" marker-end="url(#d62-m-bigtable)"/>
<path d="M 535 650 L 550 650" fill="none" stroke="#ec4899" stroke-width="1.5" marker-end="url(#d62-m-colossus)"/>
<path d="M 730 650 L 745 650" fill="none" stroke="#06b6d4" stroke-width="1.5" marker-end="url(#d62-m-sync)"/>
</svg>
<figcaption>Figure 62.1: Google Cloud Distributed Database Fabric: Cloud Spanner, Cloud Firestore, and Cloud Bigtable Architectural Topology. Detailed architecture illustrating: (1) Cloud Spanner's TrueTime atomic clock and GPS timekeeping daemon enforcing the commit wait rule for external consistency, multi-region Paxos consensus groups spanning read-write leaders, voting replicas, and witness nodes, and schema table interleaving; (2) Cloud Firestore's document hierarchy, single-document 1 write/sec constraint, 50-shard distributed counter pattern with server-side sum aggregation, and composite index pipeline; and (3) Cloud Bigtable's decoupled compute-storage topology on Colossus, salted reverse-timestamp row key range scans, and application profile routing policies balancing eventual consistency against read-your-writes guarantees.</figcaption>
</figure>"""
