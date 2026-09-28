"""Part 3 Field Case Incidents and SVG Diagrams for Day 62."""

def get_part3_incidents_html():
    return """<section id="part-3" class="part">
<h2>3 · Real-world problems and production mitigations</h2>

<!-- INCIDENT 1 -->
<article id="topic-01-problem" class="topic-card">
<h3>Spanner Sequential Primary Key Hotspotting &amp; Multi-Region Commit Wait Latency Trap · field case</h3>

<p><strong>Context &amp; Situation:</strong> Brightloaf operates a global payment and order checkout service spanning North America, backed by a Cloud Spanner multi-region instance (<code>nam3</code> topology spanning read-write regions in <code>us-east4</code> and <code>us-central1</code>, with a witness replica in <code>us-east1</code>). The database schema stores customer orders using a primary key defined as <code>(order_timestamp TIMESTAMP, order_id STRING(36))</code> to support chronological order querying for customer support dashboards. Order line items are stored in a separate, un-interleaved table <code>order_items (item_id STRING(36), order_id STRING(36), sku STRING(64), quantity INT64)</code>.</p>

<p><strong>Symptoms &amp; Impact:</strong> During a premier holiday flash-sale event, incoming order checkout traffic surged to 12,000 transactions per second. Because <code>order_timestamp</code> was monotonically increasing, 100% of all incoming write transactions targeted the single Colossus split managing the upper boundary of the table. A single Spanner compute node's Paxos leader CPU pegged at 100%, while the remaining 15 nodes in the instance hovered under 8% CPU. While TrueTime commit-wait normally incurs only 7ms (<code>2 * &epsilon;</code>), the transaction lock queue on the single overloaded Paxos leader ballooned transaction commit latency to 8.5 seconds. Concurrently, because <code>order_items</code> was not interleaved, every checkout required a distributed two-phase commit (2PC) coordinating across two independent Paxos groups over the multi-region WAN. Distributed lock timeouts cascaded into front-end HTTP 504 Gateway Timeouts. Over a 40-minute window, 24,000 checkout attempts failed, resulting in $420,000 in abandoned orders and severe brand reputation fallout.</p>

<p><strong>Diagnostic Sequence:</strong></p>
<ol>
<li><strong>Spanner Key Visualizer Inspection:</strong> Opening the Cloud Spanner Key Visualizer in the Cloud Console revealed a stark, vivid red horizontal band across the write heatmap. Over 96% of all write operations were concentrated on a single split key range, confirming an extreme write hotspot.</li>
<li><strong>Node CPU Telemetry:</strong> Cloud Monitoring metrics (<code>spanner.googleapis.com/instance/cpu/utilization_by_priority</code>) showed a single compute node pinned at 100% CPU utilization, while surrounding nodes remained virtually idle. The Paxos leader process was starved of CPU cycles to process incoming lock acquisitions.</li>
<li><strong>Query Statistics and Lock Contention:</strong> Inspecting <code>INFORMATION_SCHEMA.SPANNER_SYS.TOP_QUERIES</code> and <code>LOCK_STATISTICS</code> showed that the <code>INSERT INTO orders</code> statement experienced average lock wait times of 4,800ms. Multiple concurrent transactions were queuing for exclusive locks on the tail split.</li>
<li><strong>Distributed 2PC Overhead:</strong> Transaction statistics confirmed that 100% of checkout transactions were multi-split transactions requiring distributed two-phase commit across the <code>orders</code> and <code>order_items</code> splits, compounding WAN commit-wait round trips between <code>us-east4</code> and <code>us-central1</code>.</li>
</ol>

<p><strong>Root Cause Analysis:</strong></p>
<ol>
<li><strong>Monotonic Sequential Primary Key:</strong> Leading the primary key with a raw, monotonically increasing timestamp (<code>order_timestamp</code>) systematically routed every new row into the highest split range. Spanner's automatic split rebalancer continuously divided the split, but because all new writes had higher timestamps, 100% of new traffic immediately moved to the newly created tail split.</li>
<li><strong>Un-interleaved Child Tables:</strong> Storing <code>order_items</code> as an independent top-level table forced Spanner to execute distributed two-phase commit across distinct Paxos consensus groups for every order checkout, magnifying multi-region WAN latency and lock hold times.</li>
<li><strong>Absence of Storing Secondary Indexes:</strong> The application relied on the primary key sort order for chronological range scans, creating an architectural dependency that prevented hashing the primary key.</li>
</ol>

<p><strong>Defensible Remediation:</strong></p>
<ol>
<li><strong>Decentralize Key Space via Bit-Reversed Sequential Keys:</strong> Refactor the primary key to use a bit-reversed sequential integer or cryptographically random UUIDv4: <code>(order_id STRING(36), ...)</code>. For numerical order sequences, apply bit-reversal to high-order bits: <code>BIT_REVERSE(order_sequence_id)</code>, scattering sequential inserts uniformly across all Paxos splits and utilizing 100% of cluster nodes.</li>
<li><strong>Implement Table Interleaving:</strong> Interleave <code>orders</code> and <code>order_items</code> into the <code>customers</code> root table:
<pre><code>CREATE TABLE orders (
  customer_id STRING(36),
  order_id STRING(36),
  order_timestamp TIMESTAMP,
  order_total NUMERIC
) PRIMARY KEY (customer_id, order_id),
  INTERLEAVE IN PARENT customers ON DELETE CASCADE;

CREATE TABLE order_items (
  customer_id STRING(36),
  order_id STRING(36),
  line_item_id STRING(36),
  sku STRING(64),
  quantity INT64,
  price NUMERIC
) PRIMARY KEY (customer_id, order_id, line_item_id),
  INTERLEAVE IN PARENT orders ON DELETE CASCADE;</code></pre>
This ensures that all data for a customer, their orders, and their line items reside in the exact same physical Colossus split, enabling single-split transactions that bypass distributed 2PC entirely.</li>
<li><strong>Deploy Storing Secondary Index for Chronological Scans:</strong> Create a secondary index for chronological dashboard queries:
<pre><code>CREATE INDEX idx_orders_by_timestamp ON orders (order_timestamp DESC)
STORING (order_total, customer_id);</code></pre>
The <code>STORING</code> clause serves queries directly from the index without requiring expensive cross-split join lookups.</li>
</ol>

<figure class="diagram-figure">
<svg role="img" aria-labelledby="d62-p1-title d62-p1-desc" viewBox="0 0 980 290" width="100%" height="auto" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d62-p1-title">Incident 1: Spanner Monotonic Key Hotspot vs Bit-Reversed Key &amp; Table Interleaving</title>
<desc id="d62-p1-desc">Diagram contrasting the failed path (monotonically increasing timestamp key funneling 12k QPS into a single Paxos leader split with 8.5s commit wait latency and dropped carts) against the corrected path (bit-reversed key and interleaved customer-order tables distributing writes across 20 splits with 24ms p99 write latency).</desc>
<defs>
<marker id="d62-p1-mf" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/>
</marker>
<marker id="d62-p1-mc" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
<marker id="d62-p1-probe" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/>
</marker>
</defs>

<!-- Failed Path Container -->
<rect x="20" y="20" width="940" height="115" rx="6" fill="#1e1b2e" stroke="#f43f5e" stroke-width="1.5"/>
<text x="35" y="42" fill="#f43f5e" font-size="13" font-weight="700">FAILED PATH: Monotonic Timestamp PK &amp; Uninterleaved Multi-Split Distributed 2PC</text>

<rect x="35" y="55" width="220" height="65" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="45" y="75" fill="#f1f5f9" font-size="11" font-weight="600">12,000 Orders / Sec</text>
<text x="45" y="91" fill="#f43f5e" font-size="10">PK: (order_ts, order_id)</text>
<text x="45" y="105" fill="#cbd5e1" font-size="10">Monotonic sequence input</text>

<rect x="300" y="55" width="290" height="65" rx="4" fill="#4c0519" stroke="#f43f5e" stroke-width="1.5"/>
<text x="310" y="75" fill="#fda4af" font-size="11" font-weight="700">Single Paxos Split (Tail Split)</text>
<text x="310" y="91" fill="#fecdd3" font-size="10">100% writes land on 1 leader (100% CPU)</text>
<text x="310" y="105" fill="#f43f5e" font-size="10">TrueTime commit queue: 8.5s latency</text>

<rect x="635" y="55" width="310" height="65" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1"/>
<text x="645" y="75" fill="#fda4af" font-size="11" font-weight="700">Distributed 2PC Stalls</text>
<text x="645" y="91" fill="#f43f5e" font-size="10">Un-interleaved order_items WAN lock</text>
<text x="645" y="105" fill="#f43f5e" font-size="10">HTTP 504 Timeouts ($420k loss)</text>

<path d="M 255 87 L 300 87" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d62-p1-mf)"/>
<path d="M 590 87 L 635 87" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d62-p1-mf)"/>

<!-- Corrected Path Container -->
<rect x="20" y="150" width="940" height="120" rx="6" fill="#0f291e" stroke="#22c55e" stroke-width="1.5"/>
<text x="35" y="172" fill="#4ade80" font-size="13" font-weight="700">CORRECTED PATH: Bit-Reversed Key, Table Interleaving &amp; Storing Secondary Index</text>

<rect x="35" y="185" width="200" height="70" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="45" y="205" fill="#f1f5f9" font-size="11" font-weight="600">12,000 Orders / Sec</text>
<text x="45" y="221" fill="#86efac" font-size="10">Bit-reversed UUID / Hash PK</text>
<text x="45" y="237" fill="#cbd5e1" font-size="10">Uniform hash keyspace</text>

<rect x="260" y="185" width="220" height="70" rx="4" fill="#064e3b" stroke="#22c55e" stroke-width="1.5"/>
<text x="270" y="205" fill="#a7f3d0" font-size="11" font-weight="700">20 Paxos Splits (Balanced)</text>
<text x="270" y="221" fill="#ecfdf5" font-size="10">Traffic dispersed evenly (32% CPU)</text>
<text x="270" y="237" fill="#4ade80" font-size="10">Commit wait: bounded 14ms</text>

<rect x="505" y="185" width="200" height="70" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
<text x="515" y="205" fill="#bae6fd" font-size="11" font-weight="700">Table Interleaving</text>
<text x="515" y="221" fill="#e0f2fe" font-size="10">Orders + Items in Customer Split</text>
<text x="515" y="237" fill="#38bdf8" font-size="10">Atomic single-split commit (No 2PC)</text>

<rect x="730" y="185" width="215" height="70" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="740" y="205" fill="#4ade80" font-size="11" font-weight="700">Production Stability</text>
<text x="740" y="221" fill="#86efac" font-size="10">p99 write latency: 24 ms</text>
<text x="740" y="237" fill="#22c55e" font-size="10">Zero 504s &bull; Storing index active</text>

<path d="M 235 220 L 260 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p1-mc)"/>
<path d="M 480 220 L 505 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p1-mc)"/>
<path d="M 705 220 L 730 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p1-mc)"/>

<!-- Verify Boundary Probe Point -->
<circle cx="260" cy="220" r="7" fill="#f59e0b" stroke="#ffffff" stroke-width="2"/>
<text x="250" y="278" fill="#f59e0b" font-size="10" font-weight="700">VERIFY BOUNDARY</text>
</svg>
<figcaption>Figure 62.2: Incident 1 Root Cause and Remediation. <strong>Supplied facts:</strong> In a multi-region Cloud Spanner deployment (nam3), a flash-sale order surge of 12,000 writes/sec with a monotonically increasing timestamp primary key funneled all traffic into a single Paxos leader split, driving CPU to 100% and commit-wait queueing to 8.5 seconds. Un-interleaved line item tables forced distributed cross-region two-phase commit, triggering cascading HTTP 504 gateway timeouts and $420,000 in abandoned orders. <strong>Architectural inference:</strong> Sequential primary keys defeat distributed split rebalancing and violate Spanner's parallel shared-nothing topology. Refactoring to bit-reversed keys or UUIDs scatters writes uniformly across all nodes, while table interleaving co-locates orders and line items into parent customer splits, converting multi-split distributed transactions into instantaneous single-split commits. <strong>Expected post-fix behavior:</strong> Key Visualizer confirms a uniform green write heatmap across all 20 splits; Paxos leader CPU remains below 35% under 15,000 writes/sec, and p99 write latency drops from 8.5 seconds to 24 milliseconds with zero HTTP 504 timeouts.</figcaption>
</figure>

<p><strong>Verification:</strong> The remediation was validated in a staging environment simulating 15,000 writes/second against the multi-region Spanner instance. Key Visualizer confirmed a uniform light-green heatmap across all 20 splits. Spanner CPU utilization stabilized at 32% across all nodes. Transaction commit latency averaged 14ms with a p99 of 24ms. Chronological queries against the storing index executed in under 8ms without split joins.</p>
<p><strong>Residual Risk:</strong> Using bit-reversed primary keys prevents simple range-based scanning on insertion order; all chronological order reporting must route through secondary indexes. Secondary index writes introduce a small write amplification factor (one additional Paxos write per indexed field).</p>
</article>

<!-- INCIDENT 2 -->
<article id="topic-02-problem" class="topic-card">
<h3>Firestore Single-Document Contention (1 Write/sec Limit) &amp; Missing Composite Index Stalls · field case</h3>

<p><strong>Context &amp; Situation:</strong> Brightloaf's mobile engineering team deployed a promotional flash-sale feature in the customer mobile app, allowing users to claim limited-edition artisanal bakery packages. To display live real-time stock levels, the mobile app updated a single global Firestore document: <code>/counters/black_friday_deal</code> with an integer field <code>available_stock</code>. Concurrently, the mobile app added a dynamic store locator and product search query filtering by store and category: <code>collection('products').where('store_id', '==', selectedStore).where('category', '==', 'artisan_bread').orderBy('price_cents', 'asc')</code>.</p>

<p><strong>Symptoms &amp; Impact:</strong> When the marketing campaign went viral, over 15,000 mobile shoppers launched the app simultaneously, generating 350 purchase attempts per second against the single <code>/counters/black_friday_deal</code> document. Because Firestore documents are subject to a physical Paxos limit of approximately 1 write per second, 98% of incoming transactional writes failed with <code>FAILED_PRECONDITION: Aborted due to concurrent update</code>. Concurrently, every mobile user attempting to search the catalog received an uncaught exception: <code>FAILED_PRECONDITION: The query requires an index</code>. The entire mobile storefront crashed, preventing 8,500 active shoppers from completing checkout and resulting in $215,000 in lost revenue, brand embarrassment on social media, and emergency on-call triage.</p>

<p><strong>Diagnostic Sequence:</strong></p>
<ol>
<li><strong>Firestore Error Metric Spike:</strong> Cloud Monitoring showed a massive spike in Firestore error rates (<code>firestore.googleapis.com/api/request_count</code> with status <code>FAILED_PRECONDITION</code>). Write operation latency spiked vertically from 25ms to over 12,000ms before aborting.</li>
<li><strong>Document Contention Analysis:</strong> Cloud Logging revealed thousands of rollback exceptions concentrated on document path <code>projects/brightloaf/databases/(default)/documents/counters/black_friday_deal</code>. The logs confirmed clients were repeatedly retrying check-and-decrement transactions against the exact same document, inducing extreme Paxos lease thrashing.</li>
<li><strong>Query Index Failure Inspection:</strong> The product catalog query logs contained direct links provided by Firestore's query engine: <code>https://console.cloud.google.com/firestore/databases/-default-/indexes/composite/create?...</code>. The application attempted a multi-field query combining two equality filters with an inequality sort without an existing composite index.</li>
<li><strong>Client Unhandled Exceptions:</strong> Review of the mobile app code revealed that the transaction callback lacked exponential backoff and treated all transaction failures as fatal application errors, causing the mobile checkout view to crash.</li>
</ol>

<p><strong>Root Cause Analysis:</strong></p>
<ol>
<li><strong>Violation of Single-Document Write Rate Limit:</strong> Attempting to funnel 350 writes/second into a single document violated Firestore's fundamental architecture, which enforces ~1 write/sec per document to maintain Paxos consensus.</li>
<li><strong>Missing Declarative Composite Index:</strong> Firestore automatically builds single-field indexes, but queries combining multiple equality filters with an <code>orderBy</code> clause on a different attribute require an explicit composite index. Because <code>firestore.indexes.json</code> was not updated in the CI/CD pipeline, the query failed in production.</li>
<li><strong>Client-Side Brittle Retry Semantics:</strong> The mobile client application executed tight, un-jittered reconnect loops on transaction rollbacks, accelerating contention rather than backing off.</li>
</ol>

<p><strong>Defensible Remediation:</strong></p>
<ol>
<li><strong>Implement Distributed Sharded Counter Pattern:</strong> Refactor the global counter into 50 independent shards in a dedicated subcollection:
<pre><code>/counters/black_friday_deal/shards/0
/counters/black_friday_deal/shards/1
...
/counters/black_friday_deal/shards/49</code></pre>
When a client records a purchase, it picks a random shard index: <code>shard_id = random.randint(0, 49)</code> and executes an atomic increment:
<pre><code>db.collection('counters').document('black_friday_deal')
  .collection('shards').document(str(shard_id))
  .update({'count': firestore.Increment(-1)})</code></pre>
This scatters 350 writes/sec across 50 documents, keeping each document at ~7 writes/sec (well within transient burst thresholds) and eliminating contention aborts.</li>
<li><strong>Server-Side Aggregation Query for Total Stock:</strong> The mobile application queries the aggregate stock using Firestore's server-side aggregation API:
<pre><code>total_stock = db.collection('counters').document('black_friday_deal')
  .collection('shards').aggregate(sum('count')).get()</code></pre>
This returns the exact sum in a single network round-trip, billed as a single document read.</li>
<li><strong>Deploy Composite Index via Configuration as Code:</strong> Add the missing composite index to <code>firestore.indexes.json</code> and deploy via CI/CD:
<pre><code>{
  "indexes": [
    {
      "collectionGroup": "products",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "store_id", "order": "ASCENDING" },
        { "fieldPath": "category", "order": "ASCENDING" },
        { "fieldPath": "price_cents", "order": "ASCENDING" }
      ]
    }
  ],
  "fieldOverrides": [
    {
      "collectionGroup": "products",
      "fieldPath": "raw_specs_json",
      "indexes": []
    }
  ]
}</code></pre>
Exempt <code>raw_specs_json</code> from single-field indexing to eliminate write amplification.</li>
</ol>

<figure class="diagram-figure">
<svg role="img" aria-labelledby="d62-p2-title d62-p2-desc" viewBox="0 0 980 290" width="100%" height="auto" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d62-p2-title">Incident 2: Firestore 1 Write/Sec Contention vs Sharded Counter &amp; Composite Index</title>
<desc id="d62-p2-desc">Diagram contrasting the failed path (350 writes/sec targeting a single document counter causing 412 contention aborts and unindexed query crashes) against the corrected path (50-shard subcollection with randomized routing, server-side sum aggregation, and declarative composite index).</desc>
<defs>
<marker id="d62-p2-mf" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/>
</marker>
<marker id="d62-p2-mc" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
<marker id="d62-p2-probe" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/>
</marker>
</defs>

<!-- Failed Path Container -->
<rect x="20" y="20" width="940" height="115" rx="6" fill="#1e1b2e" stroke="#f43f5e" stroke-width="1.5"/>
<text x="35" y="42" fill="#f43f5e" font-size="13" font-weight="700">FAILED PATH: Single-Document Contention (350 Writes/Sec) &amp; Missing Composite Index</text>

<rect x="35" y="55" width="220" height="65" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="45" y="75" fill="#f1f5f9" font-size="11" font-weight="600">15,000 Mobile Clients</text>
<text x="45" y="91" fill="#f43f5e" font-size="10">350 concurrent writes/sec</text>
<text x="45" y="105" fill="#cbd5e1" font-size="10">Target: /counters/black_friday</text>

<rect x="300" y="55" width="290" height="65" rx="4" fill="#4c0519" stroke="#f43f5e" stroke-width="1.5"/>
<text x="310" y="75" fill="#fda4af" font-size="11" font-weight="700">Single Document Limit Hit</text>
<text x="310" y="91" fill="#fecdd3" font-size="10">Firestore 1 write/sec Paxos ceiling</text>
<text x="310" y="105" fill="#f43f5e" font-size="10">412 Precondition Aborts (98%)</text>

<rect x="635" y="55" width="310" height="65" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1"/>
<text x="645" y="75" fill="#fda4af" font-size="11" font-weight="700">Storefront Crash</text>
<text x="645" y="91" fill="#f43f5e" font-size="10">Unindexed catalog query fails</text>
<text x="645" y="105" fill="#f43f5e" font-size="10">8,500 stranded carts ($215k loss)</text>

<path d="M 255 87 L 300 87" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d62-p2-mf)"/>
<path d="M 590 87 L 635 87" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d62-p2-mf)"/>

<!-- Corrected Path Container -->
<rect x="20" y="150" width="940" height="120" rx="6" fill="#0f291e" stroke="#22c55e" stroke-width="1.5"/>
<text x="35" y="172" fill="#4ade80" font-size="13" font-weight="700">CORRECTED PATH: 50-Shard Counter, Server-Side SUM &amp; Declarative Composite Index</text>

<rect x="35" y="185" width="200" height="70" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="45" y="205" fill="#f1f5f9" font-size="11" font-weight="600">Mobile Clients</text>
<text x="45" y="221" fill="#86efac" font-size="10">Random shard router (0..49)</text>
<text x="45" y="237" fill="#cbd5e1" font-size="10">Atomic increment</text>

<rect x="260" y="185" width="220" height="70" rx="4" fill="#064e3b" stroke="#22c55e" stroke-width="1.5"/>
<text x="270" y="205" fill="#a7f3d0" font-size="11" font-weight="700">50 Shard Subcollection</text>
<text x="270" y="221" fill="#ecfdf5" font-size="10">~7 writes/sec per shard (Safe)</text>
<text x="270" y="237" fill="#4ade80" font-size="10">Zero contention aborts</text>

<rect x="505" y="185" width="200" height="70" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
<text x="515" y="205" fill="#bae6fd" font-size="11" font-weight="700">Server Aggregation</text>
<text x="515" y="221" fill="#e0f2fe" font-size="10">aggregate(sum('count'))</text>
<text x="515" y="237" fill="#38bdf8" font-size="10">Single read cost &bull; 18ms latency</text>

<rect x="730" y="185" width="215" height="70" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="740" y="205" fill="#4ade80" font-size="11" font-weight="700">Composite Index Active</text>
<text x="740" y="221" fill="#86efac" font-size="10">store + category + price ASC</text>
<text x="740" y="237" fill="#22c55e" font-size="10">Catalog query sub-15ms</text>

<path d="M 235 220 L 260 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p2-mc)"/>
<path d="M 480 220 L 505 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p2-mc)"/>
<path d="M 705 220 L 730 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p2-mc)"/>

<!-- Verify Boundary Probe Point -->
<circle cx="260" cy="220" r="7" fill="#f59e0b" stroke="#ffffff" stroke-width="2"/>
<text x="250" y="278" fill="#f59e0b" font-size="10" font-weight="700">VERIFY BOUNDARY</text>
</svg>
<figcaption>Figure 62.3: Incident 2 Root Cause and Remediation. <strong>Supplied facts:</strong> A viral flash promotion generated 350 writes/second against a single Firestore inventory document, violating the 1 write/second/document physical Paxos limit and causing 98% of transactions to abort with <code>412 FAILED_PRECONDITION</code>. Simultaneously, a dynamic catalog search failed with unindexed query errors, crashing the checkout view and abandoning $215,000 in orders across 8,500 mobile shoppers. <strong>Architectural inference:</strong> High-velocity writes must be dispersed across a distributed sharded counter subcollection, where randomized writes distribute contention and server-side aggregation queries retrieve totals efficiently. Multi-field equality and sort queries must be codified declaratively in <code>firestore.indexes.json</code> with single-field exemptions to control write amplification. <strong>Expected post-fix behavior:</strong> 50-shard counter absorbs 500 writes/sec with 0% transaction contention aborts; server-side SUM aggregation executes in 18ms at the cost of a single document read; catalog searches execute in 12ms.</figcaption>
</figure>

<p><strong>Verification:</strong> The remediation was validated using a synthetic Locust load test executing 500 concurrent writes/second against the 50-shard counter. Contention aborts dropped to 0%, write latency averaged 16ms, and server-side aggregation queries returned exact inventory counts in 18ms. The composite index deployment was verified via Cloud Logging and the index state dashboard, and catalog queries returned in 12ms.</p>
<p><strong>Residual Risk:</strong> Operating 50 shards multiplies document write operations and storage billing by 50 for the counter subcollection. For extreme write rates exceeding 5,000 writes/sec, caching counters in Google Cloud Memorystore for Redis with periodic asynchronous batch persistence to Firestore is recommended.</p>
</article>

<!-- INCIDENT 3 -->
<article id="topic-03-problem" class="topic-card">
<h3>Bigtable Lexicographical Timestamp Hotspotting &amp; Multi-Cluster Replication Routing Lag · field case</h3>

<p><strong>Context &amp; Situation:</strong> Brightloaf operates a logistics fleet of 320 temperature-monitored refrigerated delivery vans supplying fresh baked goods to commercial grocery chains. Each vehicle streams GPS coordinates, refrigeration telemetry, and engine health every 500ms (150,000 events/second) into a Cloud Bigtable instance. The instance was configured with two 8-node SSD clusters: Cluster 1 in <code>us-central1-a</code> and Cluster 2 in <code>us-central1-b</code>, using a default multi-cluster routing Application Profile. Row keys were structured as <code>YYYY-MM-DD-HH-MM#VEHICLE_ID</code>.</p>

<p><strong>Symptoms &amp; Impact:</strong> Telemetry ingestion write latency spiked from a normal 4ms to over 850ms, triggering backpressure across ingestion Pub/Sub queues and dropping telemetry packets. Concurrently, regional delivery dispatchers monitoring live vehicle positions observed up to 4 minutes of location lag: delivery vans were displayed at highway junctions when they had already arrived at store loading docks. Dispatchers sent 320 delivery vans to incorrect distribution bays during peak morning deliveries, causing traffic gridlock at depots, spoiling temperature-sensitive sourdough consignments, and generating $165,000 in direct freight write-offs.</p>

<p><strong>Diagnostic Sequence:</strong></p>
<ol>
<li><strong>Bigtable Key Visualizer Analysis:</strong> Inspecting the Bigtable Key Visualizer revealed an intense red diagonal stripe moving across the tablet space. Over 94% of all write operations were concentrated on a single tablet server split—the split holding the latest timestamp prefix. Surrounding tablet servers were virtually idle.</li>
<li><strong>Tablet Server CPU Utilization:</strong> Cloud Monitoring telemetry showed 2 nodes in Cluster 1 pinned at 98% CPU utilization, while the remaining 6 nodes operated at under 10% CPU. The write bottleneck overwhelmed MemTable flushes and WAL logging on the hot tablet.</li>
<li><strong>Replication Lag Telemetry:</strong> The metric <code>bigtable.googleapis.com/cluster/replication/lag_latency</code> showed replication lag between Cluster 1 and Cluster 2 had spiked to 240 seconds. A heavy batch analytics ETL job was running against the default App Profile, saturating read queues in Cluster 2.</li>
<li><strong>Application Profile Routing Audit:</strong> Reviewing the client configuration revealed that both real-time operational dispatchers and the heavy analytics pipeline shared the same Multi-Cluster Routing App Profile. Dispatcher reads were routed round-robin to Cluster 2, reading stale, un-replicated vehicle positions.</li>
</ol>

<p><strong>Root Cause Analysis:</strong></p>
<ol>
<li><strong>Sequential Timestamp Row Key Hotspotting:</strong> Because Bigtable sorts all row keys lexicographically, prepending the key with a monotonic timestamp (<code>YYYY-MM-DD-HH-MM</code>) concentrated all 150k writes/sec onto the single tablet server managing the highest byte range. Automatic tablet splitting could not resolve the bottleneck because new writes continuously advanced into the newest split.</li>
<li><strong>Shared Eventual Consistency Routing Profile:</strong> Real-time delivery dispatchers requiring up-to-the-second vehicle positions were configured with Multi-Cluster Routing, exposing them to asynchronous cross-cluster replication lag.</li>
<li><strong>Resource Contention from Un-isolated Workloads:</strong> Batch analytics scans and high-velocity ingestion competed for the same cluster resources without dedicated routing isolation.</li>
</ol>

<p><strong>Defensible Remediation:</strong></p>
<ol>
<li><strong>Re-engineer Row Key with Salt Hash and Reverse Timestamp:</strong> Redesign the Bigtable row key using field salting and descending time inversion:
<pre><code>row_key = HASH(vehicle_id)[0:4] + "#" + tenant_id + "#" + vehicle_id + "#" + reverse_timestamp
where:
reverse_timestamp = String.format("%019d", Long.MAX_VALUE - epoch_timestamp_ms)</code></pre>
The 4-character MD5/SHA256 salt prefix uniformly distributes incoming writes across 16+ tablet splits and all tablet servers, eliminating write hotspotting. The reverse timestamp ensures that range scans for a vehicle return the most recent telemetry readings first.</li>
<li><strong>Isolate Workloads with Dedicated Application Profiles:</strong>
  <ul>
  <li><strong>Operational Ingestion Profile:</strong> Multi-cluster routing across all clusters for maximum write resilience and 99.999% SLA.</li>
  <li><strong>Dispatcher Operational Profile:</strong> Single-cluster routing directed strictly to <code>us-central1-a</code>, providing strict <strong>Read-Your-Writes consistency</strong> and eliminating replication lag for dispatchers.</li>
  <li><strong>Batch Analytics Profile:</strong> Single-cluster routing directed to <code>us-central1-b</code> with standard priority, isolating batch queries from production ingestion.</li>
  </ul>
</li>
<li><strong>Configure Column-Family Garbage Collection:</strong> Implement a garbage collection policy retaining only the 5 most recent versions or data younger than 14 days:
<pre><code>cbt setgcpolicy delivery_telemetry metrics maxversions=5 maxage=14d</code></pre>
</li>
</ol>

<figure class="diagram-figure">
<svg role="img" aria-labelledby="d62-p3-title d62-p3-desc" viewBox="0 0 980 290" width="100%" height="auto" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d62-p3-title">Incident 3: Bigtable Timestamp Hotspot vs Salted Reverse Key &amp; Isolated App Profiles</title>
<desc id="d62-p3-desc">Diagram contrasting the failed path (sequential timestamp key concentrating 150k writes/sec onto one tablet server with 850ms latency and stale multi-cluster reads) against the corrected path (salted hash prefix with reverse timestamp and isolated Single-Cluster Read-Your-Writes App Profile).</desc>
<defs>
<marker id="d62-p3-mf" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/>
</marker>
<marker id="d62-p3-mc" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
<marker id="d62-p3-probe" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/>
</marker>
</defs>

<!-- Failed Path Container -->
<rect x="20" y="20" width="940" height="115" rx="6" fill="#1e1b2e" stroke="#f43f5e" stroke-width="1.5"/>
<text x="35" y="42" fill="#f43f5e" font-size="13" font-weight="700">FAILED PATH: Monotonic Timestamp Row Key &amp; Un-isolated Eventual Routing</text>

<rect x="35" y="55" width="220" height="65" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="45" y="75" fill="#f1f5f9" font-size="11" font-weight="600">150,000 Events / Sec</text>
<text x="45" y="91" fill="#f43f5e" font-size="10">Key: YYYY-MM-DD-HH#dev</text>
<text x="45" y="105" fill="#cbd5e1" font-size="10">Strict monotonic ordering</text>

<rect x="300" y="55" width="290" height="65" rx="4" fill="#4c0519" stroke="#f43f5e" stroke-width="1.5"/>
<text x="310" y="75" fill="#fda4af" font-size="11" font-weight="700">Tail Tablet Server (Hotspot)</text>
<text x="310" y="91" fill="#fecdd3" font-size="10">94% writes hit 1 node (98% CPU)</text>
<text x="310" y="105" fill="#f43f5e" font-size="10">Write latency: 850 ms &bull; Backpressure</text>

<rect x="635" y="55" width="310" height="65" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1"/>
<text x="645" y="75" fill="#fda4af" font-size="11" font-weight="700">Stale Dispatcher Reads</text>
<text x="645" y="91" fill="#f43f5e" font-size="10">Replication lag: 240s &bull; Analytics contention</text>
<text x="645" y="105" fill="#f43f5e" font-size="10">320 vans stranded ($165k cargo loss)</text>

<path d="M 255 87 L 300 87" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d62-p1-mf)"/>
<path d="M 590 87 L 635 87" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d62-p1-mf)"/>

<!-- Corrected Path Container -->
<rect x="20" y="150" width="940" height="120" rx="6" fill="#0f291e" stroke="#22c55e" stroke-width="1.5"/>
<text x="35" y="172" fill="#4ade80" font-size="13" font-weight="700">CORRECTED PATH: Salted Reverse Row Key &amp; Segregated App Profiles</text>

<rect x="35" y="185" width="200" height="70" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="45" y="205" fill="#f1f5f9" font-size="11" font-weight="600">150,000 Events / Sec</text>
<text x="45" y="221" fill="#86efac" font-size="10">Key: hash[0:4]#dev#~ts</text>
<text x="45" y="237" fill="#cbd5e1" font-size="10">16-way hash distribution</text>

<rect x="260" y="185" width="220" height="70" rx="4" fill="#064e3b" stroke="#22c55e" stroke-width="1.5"/>
<text x="270" y="205" fill="#a7f3d0" font-size="11" font-weight="700">Balanced Tablet Fleet</text>
<text x="270" y="221" fill="#ecfdf5" font-size="10">All 8 nodes active (28% CPU)</text>
<text x="270" y="237" fill="#4ade80" font-size="10">Write latency: 3.8 ms p99</text>

<rect x="505" y="185" width="200" height="70" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
<text x="515" y="205" fill="#bae6fd" font-size="11" font-weight="700">Single-Cluster Profile</text>
<text x="515" y="221" fill="#e0f2fe" font-size="10">Dispatcher &rarr; Cluster 1 only</text>
<text x="515" y="237" fill="#38bdf8" font-size="10">Read-Your-Writes &bull; Zero lag</text>

<rect x="730" y="185" width="215" height="70" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="740" y="205" fill="#4ade80" font-size="11" font-weight="700">Isolated Analytics</text>
<text x="740" y="221" fill="#86efac" font-size="10">Batch ETL &rarr; Cluster 2</text>
<text x="740" y="237" fill="#22c55e" font-size="10">GC: maxversions=5 maxage=14d</text>

<path d="M 235 220 L 260 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p1-mc)"/>
<path d="M 480 220 L 505 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p1-mc)"/>
<path d="M 705 220 L 730 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p1-mc)"/>

<!-- Verify Boundary Probe Point -->
<circle cx="260" cy="220" r="7" fill="#f59e0b" stroke="#ffffff" stroke-width="2"/>
<text x="250" y="278" fill="#f59e0b" font-size="10" font-weight="700">VERIFY BOUNDARY</text>
</svg>
<figcaption>Figure 62.4: Incident 3 Root Cause and Remediation. <strong>Supplied facts:</strong> A refrigerated fleet telemetry stream of 150,000 events/second using a sequential timestamp row key prefix concentrated 94% of writes onto a single Bigtable tablet server, driving write latency to 850ms. Dispatchers sharing a multi-cluster eventual routing profile with heavy analytics jobs observed 4-minute replication lag, stranding 320 delivery vans and causing $165,000 in spoiled consignment write-offs. <strong>Architectural inference:</strong> Sequential timestamp prefixes violate Bigtable's lexicographical range partitioning. Salting row keys with a hash prefix distributes write load across all tablet servers, while reverse timestamps enable instantaneous descending time-series lookups. Workloads must be isolated into dedicated App Profiles: Single-Cluster routing guarantees Read-Your-Writes consistency for dispatchers, while Multi-Cluster routing handles ingestion. <strong>Expected post-fix behavior:</strong> Key Visualizer confirms uniform write distribution across all 8 nodes; p99 write latency stabilizes at 3.8ms under 180,000 writes/sec; dispatcher location queries return zero-lag vehicle positions.</figcaption>
</figure>

<p><strong>Verification:</strong> The remediation was validated using a synthetic telemetry replay test streaming 180,000 writes/second. Key Visualizer confirmed a uniform green write distribution across all tablet splits. Tablet server CPU hovered evenly between 26% and 31%. Write latency dropped to 3.8ms p99. Dispatcher queries directed through the Single-Cluster App Profile returned the latest GPS coordinates in 4.2ms with zero replication lag.</p>
<p><strong>Residual Risk:</strong> Salting row keys prevents simple table-wide range scans across all vehicles simultaneously; fleet-wide queries require scatter-gather queries querying each salt prefix in parallel. In addition, Single-Cluster App Profiles require manual failover procedures or application-level fallbacks if the primary cluster zone experiences an outage.</p>
</article>

<!-- INCIDENT 4 -->
<article id="topic-04-problem" class="topic-card">
<h3>Enterprise Database Selection Failure &amp; Architectural Impedance Mismatch · field case</h3>

<p><strong>Context &amp; Situation:</strong> Brightloaf's platform modernization leadership attempted to mandate a "single database engine" to simplify team training and operational management. Under this directive, the engineering team attempted to route high-frequency delivery van telemetry (150k writes/sec) into Cloud Spanner, while simultaneously migrating the multi-entity financial accounting ledger and inventory reservations into Cloud Firestore documents without transactions or composite indexes.</p>

<p><strong>Symptoms &amp; Impact:</strong> Within six weeks of deployment, Brightloaf's Google Cloud database bill surged by $85,000 per month: Spanner compute capacity had to be scaled to 60 nodes solely to absorb the append-only telemetry stream. Concurrently, the financial ledger in Firestore suffered widespread concurrency write skew, race conditions, and phantom balance adjustments across customer accounts. During a mandatory SOX compliance audit, external auditors discovered $310,000 in unreconciled debit/credit ledger discrepancies, halting a planned corporate capital round and triggering severe regulatory audit penalties.</p>

<p><strong>Diagnostic Sequence:</strong></p>
<ol>
<li><strong>Cost Attribution Analysis:</strong> Cloud Billing reports revealed that Cloud Spanner compute nodes were consuming over 72% of the entire database infrastructure budget, driven by raw write throughput requirements rather than relational or transactional queries.</li>
<li><strong>Ledger Consistency Audit:</strong> Comparing ledger transaction logs against actual customer balances revealed severe write skew: multiple concurrent order services updated account documents outside of ACID transactions, resulting in lost updates and out-of-order ledger writes.</li>
<li><strong>Architecture Review:</strong> Cross-functional architectural review revealed an absence of formal Architectural Decision Records (ADRs). The database selection had been driven by executive consensus rather than a systematic mapping of workload characteristics against data model, consistency, latency, and cost constraints.</li>
</ol>

<p><strong>Root Cause Analysis:</strong></p>
<ol>
<li><strong>Architectural Impedance Mismatch:</strong> Cloud Spanner's expensive, strictly serializable Paxos consensus engine was wasted on transient, append-only time-series telemetry. Conversely, Firestore's document model was misapplied to a complex, multi-entity double-entry financial ledger requiring relational schema constraints and strict serializability.</li>
<li><strong>Absence of Formal ADR Governance:</strong> The organization lacked a rigorous architectural decision process to evaluate candidate stores against explicit workload boundaries, SLA targets, and total cost of ownership.</li>
</ol>

<p><strong>Defensible Remediation:</strong></p>
<ol>
<li><strong>Author and Enforce Enterprise Database Selection ADR (ADR-062):</strong> Formulate an authoritative Architecture Decision Record defining non-negotiable workload assignments:
  <ul>
  <li><strong>Domain 1: Core Financial Ledger &amp; Inventory Reservations &rarr; Cloud Spanner:</strong> Relational schematization, parent-child table interleaving (Customers &rarr; Orders &rarr; LineItems), strict serializability via TrueTime commit wait, and 99.999% multi-region availability (RPO = 0).</li>
  <li><strong>Domain 2: Client State, Mobile Carts &amp; User Profiles &rarr; Cloud Firestore:</strong> Serverless document data model, distributed sharded counters for promotions, real-time push listeners for mobile UI sync, and offline client persistence.</li>
  <li><strong>Domain 3: High-Throughput Fleet &amp; IoT Telemetry &rarr; Cloud Bigtable:</strong> Wide-column sparse store, salted reverse-timestamp row keys, stateless tablet servers on Colossus, and dedicated App Profiles.</li>
  </ul>
</li>
<li><strong>Implement Double-Entry Ledger Schema in Spanner:</strong> Migrate financial accounts to Spanner with relational check constraints, foreign keys, and strict transactional ACID boundaries to guarantee 100% debit/credit reconciliation.</li>
<li><strong>Migrate Telemetry Ingestion to Bigtable:</strong> Provision an 8-node Bigtable cluster, cutting monthly telemetry ingestion infrastructure costs by 78% (saving $71,000/month).</li>
</ol>

<figure class="diagram-figure">
<svg role="img" aria-labelledby="d62-p4-title d62-p4-desc" viewBox="0 0 980 290" width="100%" height="auto" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d62-p4-title">Incident 4: Database Selection Impedance Mismatch vs ADR-Governed Workload Segregation</title>
<desc id="d62-p4-desc">Diagram contrasting the failed path (monolithic attempt routing IoT to Spanner causing $85k cost spike and Ledger to Firestore causing write skew) against the corrected path (ADR-governed workload mapping: Spanner for ACID ledger, Firestore for mobile sync, and Bigtable for IoT telemetry).</desc>
<defs>
<marker id="d62-p4-mf" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/>
</marker>
<marker id="d62-p4-mc" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
<marker id="d62-p4-probe" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/>
</marker>
</defs>

<!-- Failed Path Container -->
<rect x="20" y="20" width="940" height="115" rx="6" fill="#1e1b2e" stroke="#f43f5e" stroke-width="1.5"/>
<text x="35" y="42" fill="#f43f5e" font-size="13" font-weight="700">FAILED PATH: "One Size Fits All" Monolithic Database Anti-Pattern</text>

<rect x="35" y="55" width="220" height="65" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="45" y="75" fill="#f1f5f9" font-size="11" font-weight="600">Disparate Workloads</text>
<text x="45" y="91" fill="#f43f5e" font-size="10">IoT writes (150k QPS)</text>
<text x="45" y="105" fill="#f43f5e" font-size="10">Financial ledger accounting</text>

<rect x="300" y="55" width="290" height="65" rx="4" fill="#4c0519" stroke="#f43f5e" stroke-width="1.5"/>
<text x="310" y="75" fill="#fda4af" font-size="11" font-weight="700">Mismatched Engine Assignment</text>
<text x="310" y="91" fill="#fecdd3" font-size="10">IoT &rarr; Spanner (60 nodes provisioned)</text>
<text x="310" y="105" fill="#f43f5e" font-size="10">Ledger &rarr; Unindexed Firestore</text>

<rect x="635" y="55" width="310" height="65" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1"/>
<text x="645" y="75" fill="#fda4af" font-size="11" font-weight="700">Catastrophic Business Impact</text>
<text x="645" y="91" fill="#f43f5e" font-size="10">$85k/mo Spanner cost explosion</text>
<text x="645" y="105" fill="#f43f5e" font-size="10">$310k audit discrepancy &bull; SOX failure</text>

<path d="M 255 87 L 300 87" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d62-p1-mf)"/>
<path d="M 590 87 L 635 87" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d62-p1-mf)"/>

<!-- Corrected Path Container -->
<rect x="20" y="150" width="940" height="120" rx="6" fill="#0f291e" stroke="#22c55e" stroke-width="1.5"/>
<text x="35" y="172" fill="#4ade80" font-size="13" font-weight="700">CORRECTED PATH: ADR-Governed Workload Segregation &amp; Domain Boundaries</text>

<rect x="35" y="185" width="200" height="70" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="45" y="205" fill="#f1f5f9" font-size="11" font-weight="600">Enterprise Workloads</text>
<text x="45" y="221" fill="#86efac" font-size="10">Rigorous ADR Evaluation</text>
<text x="45" y="237" fill="#cbd5e1" font-size="10">Mapped by data model &amp; SLA</text>

<rect x="260" y="185" width="220" height="70" rx="4" fill="#064e3b" stroke="#22c55e" stroke-width="1.5"/>
<text x="270" y="205" fill="#a7f3d0" font-size="11" font-weight="700">Cloud Spanner (Interleaved)</text>
<text x="270" y="221" fill="#ecfdf5" font-size="10">Core financial ledger &amp; orders</text>
<text x="270" y="237" fill="#4ade80" font-size="10">Strict serializability &bull; Zero skew</text>

<rect x="505" y="185" width="200" height="70" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
<text x="515" y="205" fill="#bae6fd" font-size="11" font-weight="700">Cloud Firestore</text>
<text x="515" y="221" fill="#e0f2fe" font-size="10">Mobile cart &amp; user profiles</text>
<text x="515" y="237" fill="#38bdf8" font-size="10">Sharded counters &bull; Realtime sync</text>

<rect x="730" y="185" width="215" height="70" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="740" y="205" fill="#4ade80" font-size="11" font-weight="700">Cloud Bigtable</text>
<text x="740" y="221" fill="#86efac" font-size="10">150k IoT telemetry &bull; Colossus</text>
<text x="740" y="237" fill="#22c55e" font-size="10">$71k/mo saved &bull; Sub-5ms write</text>

<path d="M 235 220 L 260 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p1-mc)"/>
<path d="M 480 220 L 505 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p1-mc)"/>
<path d="M 705 220 L 730 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d62-p1-mc)"/>

<!-- Verify Boundary Probe Point -->
<circle cx="260" cy="220" r="7" fill="#f59e0b" stroke="#ffffff" stroke-width="2"/>
<text x="250" y="278" fill="#f59e0b" font-size="10" font-weight="700">VERIFY BOUNDARY</text>
</svg>
<figcaption>Figure 62.5: Incident 4 Root Cause and Remediation. <strong>Supplied facts:</strong> An executive mandate for a single database engine routed 150k QPS IoT telemetry into Cloud Spanner, requiring 60 compute nodes and inflating monthly costs by $85,000, while routing financial ledger accounting into Firestore without transactions caused un-serializable write skew and a $310,000 SOX audit discrepancy. <strong>Architectural inference:</strong> Attempting to force disparate access patterns into an ill-fitting database creates explosive cost and catastrophic consistency failures. Formulating an Architectural Decision Record (ADR) maps workloads strictly to architectural strengths: Spanner for ACID relational ledgers, Firestore for mobile real-time state, and Bigtable for high-throughput time-series telemetry. <strong>Expected post-fix behavior:</strong> Ingestion costs drop by $71,000/month on Bigtable; Spanner handles financial ledger transactions with 100% reconciliation accuracy and zero write skew across 500,000 transactions.</figcaption>
</figure>

<p><strong>Verification:</strong> The database migration and ADR enforcement were validated through a 30-day parallel run. The Spanner double-entry ledger processed 500,000 simulated orders with zero reconciliation anomalies and 100% mathematical audit closure. Bigtable absorbed the 150k writes/sec telemetry stream at 3.6ms latency, reducing monthly telemetry storage and compute billing from $92,000 to $18,400.</p>
<p><strong>Residual Risk:</strong> Running a multi-database architecture requires diverse domain expertise across development and SRE teams. Cross-system synchronization (e.g., aggregating Bigtable delivery milestones into customer Spanner invoices) must be orchestrated through reliable, idempotent event messaging pipelines (Pub/Sub and Cloud Dataflow).</p>
</article>
</section>"""
