# scratch/data_part2_tech.py
"""Part 2 Technical Discussion Articles and Comparison Tables for Day 63."""

PART_2_TECH = """<section id="part-2" class="part"><h2>2 · Technical discussion of each topic</h2>
<!-- PART_2_SVG_PLACEHOLDER -->
<article id="topic-01-technical" class="topic-card">
<h3>Memorystore/cache choices, stale reads and invalidation</h3>
<p>In-memory caching is an architectural tier engineered to decouple compute microservices from persistent relational storage I/O, reducing p99 latency from tens of milliseconds to sub-millisecond durations while protecting primary databases from read saturation. Google Cloud delivers fully managed in-memory caching through <strong>Cloud Memorystore</strong>, offering two distinct engines: Memorystore for Redis and Memorystore for Memcached.</p>

<p><strong>Memorystore Engine Architectures: Redis vs. Memcached vs. Redis Cluster:</strong></p>
<ul>
<li><strong>Memorystore for Memcached:</strong> A multi-threaded, pure in-memory key-value cache designed for string-based object caching. Memcached executes across multiple worker threads, scaling vertically with CPU cores and horizontally by adding independent nodes across zones. It provides no native clustering or server-side replication; clients distribute keys across nodes using consistent hashing algorithms (such as libketama). Value sizes are constrained to 1 MB, and memory eviction relies on a strict slab allocator. Memcached provides zero persistence, zero cross-zone replication, and no data structures beyond raw strings, making it optimal for high-throughput, horizontally partitionable read-mostly web session and HTML fragment caches.</li>
<li><strong>Memorystore for Redis (Basic vs. Standard Tier):</strong> Redis operates a single-threaded command execution event loop backed by rich in-memory data structures (strings, hashes, lists, sets, sorted sets, bitmaps, HyperLogLogs, and geospatial indexes) with value sizes up to 512 MB. Google Cloud offers two tiers:
  <ul>
  <li><em>Basic Tier:</em> A standalone, single-node instance residing in a single compute zone without a replica. It provides no high-availability SLA during maintenance events or underlying hardware failures; restarts result in complete cache loss. It is intended strictly for transient, non-critical cache buffers.</li>
  <li><em>Standard Tier:</em> An active-passive high-availability pair spanning two distinct zones within a region. The primary node asynchronously replicates mutations to a cross-zone read replica. When the primary fails or undergoes maintenance, an automated failover promotes the replica in 30 to 60 seconds, backed by a 99.9% availability SLA. Standard Tier also supports up to 5 read replicas to horizontally scale read throughput via dedicated read endpoints.</li>
  </ul>
</li>
<li><strong>Memorystore for Redis Cluster:</strong> An enterprise-scale distributed caching topology that partitions the 16,384 Redis keyspace hash slots across up to 125 primary shards and 125 cross-zone replica shards (up to 250 nodes total). Memory scales up to 10 terabytes, while throughput exceeds 10 million queries per second with sub-millisecond p99 latency. Keys are assigned to slots via <code>CRC16(key) mod 16384</code>; multi-key operations can be constrained to single shards using hash tags (e.g., <code>{user_102}:profile</code> and <code>{user_102}:cart</code>). Memorystore for Redis Cluster supports online cluster resharding and vertical shard scaling with zero application downtime, backed by a 99.99% availability SLA.</li>
</ul>

<p><strong>Caching Topologies and Architectural Design Patterns:</strong></p>
<ol>
<li><strong>Cache-Aside (Lazy Loading):</strong> The application coordinates data retrieval and persistence. On a read, the application inspects the cache; on a cache hit, it returns the cached value. On a cache miss, the application reads the authoritative database, writes the result to the cache with an explicit Time-To-Live (TTL), and returns the value. On a write or mutation, the application updates the database and invalidates (deletes) the cache entry. Cache-Aside ensures that only actively requested keys consume memory, and the application remains operational even if the cache cluster fails completely. However, cache misses incur three network round trips (cache read &rarr; DB read &rarr; cache write), and concurrent operations can introduce stale read race conditions.</li>
<li><strong>Write-Through:</strong> The application writes directly to the cache, and the cache synchronously writes the updated data to the underlying database within the same operational boundary before returning success. This guarantees that cached data is always fresh, eliminating stale reads. However, write latency increases because writes must traverse both tiers sequentially, and infrequently read data clutters the cache unless paired with aggressive TTL eviction.</li>
<li><strong>Write-Behind (Write-Back / Write-Deferred):</strong> The application writes mutations directly to the cache, which acknowledges the write immediately. An asynchronous background worker batches these mutations and flushes them to the backing database. While Write-Behind provides ultra-low write latency and absorbs massive write traffic spikes, it introduces an acute durability hazard: if the cache node crashes before mutations are flushed to disk, unwritten data is permanently lost (Recovery Point Objective &gt; 0).</li>
<li><strong>Refresh-Ahead:</strong> The cache automatically refreshes hot keys from the backing database prior to TTL expiration, governed by predictive access algorithms or background schedulers. This delivers near-zero read latency for high-frequency queries but can generate unnecessary database load if access predictions are inaccurate.</li>
</ol>

<p><strong>Stale Read Hazards, Concurrency Races, and Stampede Protection:</strong></p>
<ul>
<li><strong>The Dual-Write Concurrency Race:</strong> In a standard Cache-Aside topology without distributed synchronization, concurrent reads and writes inevitably create permanent cache poisoning:
  <ol>
  <li><em>Time t1:</em> Client A queries Redis for Key K &rarr; Cache Miss.</li>
  <li><em>Time t2:</em> Client A queries Cloud SQL and retrieves stale Value V1.</li>
  <li><em>Time t3:</em> Client B updates Cloud SQL to Value V2 and commits the transaction.</li>
  <li><em>Time t4:</em> Client B sends a <code>DEL K</code> command to Redis to invalidate the cache.</li>
  <li><em>Time t5:</em> Client A completes its delayed execution and issues <code>SET K V1</code> to Redis.</li>
  </ol>
  <em>Result:</em> Redis now holds stale Value V1 permanently until its TTL expires, despite Cloud SQL holding Value V2. To mitigate this race, systems employ <strong>Delayed Double Deletion</strong> (Client B deletes the cache key, commits the database transaction, sleeps for a calibrated delta e.g., 500ms to allow concurrent reads to resolve, and issues a second <code>DEL K</code>), or utilize monotonic version vectors and conditional writes.
</li>
<li><strong>Cache Stampede (Thundering Herd):</strong> When a hot key accessed by thousands of concurrent clients expires or is invalidated, all incoming requests simultaneously experience a cache miss. Hundreds or thousands of parallel worker threads storm the relational database with identical expensive queries, saturating connection pools, driving CPU to 100%, and causing cascading 503/504 gateway failures. Two proven architectural mitigations resolve this:
  <ul>
  <li><em>Distributed Mutex Locking (Redis SETNX):</em> Only the first worker experiencing a cache miss acquires an exclusive distributed lock (<code>SET resource:lock &lt;uuid&gt; NX EX 5</code>). That single worker queries the database, repopulates the cache, and releases the lock. All other workers poll the cache or wait briefly, preventing database load amplification.</li>
  <li><em>Probabilistic Early Expiration (The XFetch Algorithm):</em> Instead of waiting for a key to strictly expire, reading clients probabilistically recompute and refresh the cached entry in the background prior to expiration. The algorithm evaluates:
  <pre><code>delta * beta * log(random()) &gt; (ttl - now)</code></pre>
  where <code>delta</code> is the compute/query duration, <code>beta &gt; 0</code> is an aggressiveness multiplier, and <code>random()</code> is a uniform float in <code>(0, 1)</code>. As the key approaches expiration, the probability of early background refresh increases asymptotically. Higher-traffic keys are refreshed seamlessly with zero database stampede and zero client-visible latency spikes.
  </li>
  </ul>
</li>
<li><strong>Memory Eviction Policies (maxmemory-policy):</strong> When Memorystore memory reaches its threshold, the eviction policy determines key survival:
  <ul>
  <li><code>volatile-lru</code>: Evicts the least recently used keys among those with an expiration set (TTL). Ideal for mixed caching and persistent metadata.</li>
  <li><code>allkeys-lru</code>: Evicts least recently used keys across the entire keyspace. Recommended for standard Cache-Aside web architectures.</li>
  <li><code>volatile-lfu</code> / <code>allkeys-lfu</code>: Evicts least frequently used keys, preserving frequently accessed hot items even if idle for short intervals.</li>
  <li><code>noeviction</code>: Returns an Out-Of-Memory (OOM) error on write commands. Mandatory for Redis instances used as message brokers (Redis Streams/PubSub) or rate-limiting counters where silent key drops would corrupt application invariants.</li>
  </ul>
</li>
</ul>

<p><strong>Table 63.1: Google Cloud In-Memory Caching Topology Comparison</strong></p>
<table>
<thead>
<tr>
<th>Architectural Dimension</th>
<th>Memorystore for Memcached</th>
<th>Memorystore for Redis (Basic / Standard)</th>
<th>Memorystore for Redis Cluster</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Core Engine &amp; Concurrency</strong></td>
<td>Multi-threaded Memcached; vertical scaling across CPU cores.</td>
<td>Single-threaded Redis event loop per node.</td>
<td>Distributed Redis Cluster; parallel single-threaded shard engines.</td>
</tr>
<tr>
<td><strong>Data Structures &amp; Payloads</strong></td>
<td>Pure key-value (Strings only); 1 MB max value size.</td>
<td>Strings, Hashes, Lists, Sets, Sorted Sets, Streams; 512 MB max value.</td>
<td>Full Redis data structure support; hash tags <code>{tag}</code> for multi-key ops.</td>
</tr>
<tr>
<td><strong>Keyspace Partitioning</strong></td>
<td>Client-side consistent hashing (libketama); no server coordination.</td>
<td>Single keyspace; no sharding. Optional read replicas (up to 5).</td>
<td>16,384 server-side hash slots; automated CRC16 slot routing.</td>
</tr>
<tr>
<td><strong>Max Capacity &amp; Scale</strong></td>
<td>Up to 5 TB memory; up to 32 nodes per instance.</td>
<td>Up to 300 GB memory per instance; single primary node.</td>
<td>Up to 10 TB+ memory; up to 250 nodes (125 primary + 125 replicas).</td>
</tr>
<tr>
<td><strong>Throughput (QPS)</strong></td>
<td>Hundreds of thousands of QPS; linear multi-thread scale.</td>
<td>~50,000 to 100,000 QPS (Basic/Standard primary).</td>
<td>Millions of QPS (&gt;10M QPS with multi-shard linear scaling).</td>
</tr>
<tr>
<td><strong>High Availability &amp; SLA</strong></td>
<td>Zero native replication; node loss evicts keys. No HA SLA.</td>
<td>Basic: 0% SLA. Standard: Cross-zone failover (&lt;30s), 99.9% SLA.</td>
<td>Automated cross-zone shard failover; 99.99% availability SLA.</td>
</tr>
<tr>
<td><strong>Persistence &amp; Snapshots</strong></td>
<td>None (Purely volatile RAM).</td>
<td>RDB snapshots to Cloud Storage (Standard Tier); manual export/import.</td>
<td>Automated RDB snapshot persistence and scheduled backups.</td>
</tr>
<tr>
<td><strong>Ideal Enterprise Workload</strong></td>
<td>Simple, transient HTML/JSON fragment caching; multi-threaded read floods.</td>
<td>Session stores, leaderboards, distributed locks, moderate-scale cache.</td>
<td>High-scale e-commerce catalogs, global session caching, multi-TB datasets.</td>
</tr>
</tbody>
</table>

<div class="callout"><strong>Apply it</strong><p>Input: the Brightloaf order checkout API must maintain sub-millisecond response times for hot product inventory reads while ensuring zero stale pricing writes during catalog promotions. Expected: a defensible Memorystore for Redis Cluster architecture with Cache-Aside pattern, distributed mutex locking (SETNX), XFetch probabilistic early expiration, and delayed double deletion to eliminate stale read race hazards.</p></div>

<div class="callout"><strong>Further study</strong>
<p><a href="../sources.html#topic-020">Topic 020 source section</a> in this site, with original publisher links and the reading context.</p>
<p>Publisher: <a href="https://docs.cloud.google.com/memorystore/docs" rel="noopener noreferrer">Cloud Memorystore Documentation</a>. Comprehensive guide to Memorystore for Redis, Redis Cluster, and Memcached topologies, eviction policies, and replication architectures.</p>
</div>
</article>

<article id="topic-02-technical" class="topic-card">
<h3>Database Migration Service and Datastream/CDC</h3>
<p>Enterprise data architectures must continuously liberate transactional data from operational relational silos without burdening source online transaction processing (OLTP) engines. Google Cloud addresses this through two purpose-built serverless replication technologies: <strong>Database Migration Service (DMS)</strong> for database migrations and <strong>Datastream</strong> for continuous Change Data Capture (CDC).</p>

<p><strong>Database Migration Service (DMS): Serverless Homogeneous Migration:</strong></p>
<ul>
<li><strong>Core Purpose and Scope:</strong> DMS is designed for minimal-downtime, lift-and-shift migrations of production PostgreSQL, MySQL, and SQL Server databases from on-premises datacenters, AWS RDS/EC2, or Compute Engine into Cloud SQL and AlloyDB for PostgreSQL.</li>
<li><strong>Serverless Architecture &amp; Connectivity:</strong> DMS requires no migration servers or agents to manage. It provisions managed, serverless worker pipelines that connect securely to source environments via VPC Peering, Private Service Connect (PSC), or Reverse SSH tunnels over Cloud VPN / Cloud Interconnect.</li>
<li><strong>Replication Lifecycle:</strong>
  <ol>
  <li><em>Pre-Migration Verification:</em> Automated checks validate user permissions, binary log formats, replication slot parameters, table primary keys, and engine version compatibility.</li>
  <li><em>Initial Snapshot Dump:</em> DMS takes a non-locking, point-in-time snapshot dump of source schema and historical data, applying it directly to the target Cloud SQL or AlloyDB replica.</li>
  <li><em>Continuous Change Data Replication:</em> Once the initial dump completes, DMS attaches to the source database's native change stream (PostgreSQL logical replication slots using <code>pgoutput</code>; MySQL binary logs using Global Transaction Identifiers / GTID; SQL Server Change Tracking) to tail all subsequent transactions.</li>
  <li><em>Cutover Phase:</em> The source database is set to read-only; DMS drains the replication backlog until replication lag reaches zero; the administrator promotes the Cloud SQL/AlloyDB instance to a standalone master; and client application connection strings are updated. Total application cutover downtime is restricted to minutes.</li>
  </ol>
</li>
</ul>

<p><strong>Datastream: Serverless Real-Time Change Data Capture (CDC):</strong></p>
<ul>
<li><strong>Core Purpose &amp; Fan-Out:</strong> Datastream is a serverless, real-time CDC service engineered to stream row-level mutations (INSERT, UPDATE, DELETE) and schema modifications continuously from relational databases (Oracle, PostgreSQL, MySQL, SQL Server) directly into Google Cloud analytics and event sinks:
  <ul>
  <li><em>BigQuery:</em> Streaming upsert merge into real-time analytical tables. Datastream leverages BigQuery continuous streaming buffers and automated background MERGE operations, making committed operational changes queryable in BigQuery in seconds to minutes without batch ETL scripts.</li>
  <li><em>Cloud Storage:</em> Persists raw CDC event streams as Apache Avro or JSON newline-delimited files partitioned by date and table, serving as an immutable changelog for lakehouse architectures (BigLake / Dataproc).</li>
  <li><em>Cloud Pub/Sub:</em> Emits CDC mutation events onto a distributed messaging topic, triggering event-driven Cloud Functions, Cloud Run services, or automated distributed cache invalidation pipelines.</li>
  </ul>
</li>
<li><strong>Zero-Impact Transaction Log Mining:</strong> Datastream avoids querying operational database tables via <code>SELECT</code> queries during streaming. Instead, it directly mines low-level transaction logs:
  <ul>
  <li><em>PostgreSQL:</em> Connects to a logical replication slot using the <code>pgoutput</code> plugin. It decodes the append-only Write-Ahead Log (WAL) at the filesystem layer, capturing committed changes without acquiring shared table locks or polluting the database shared buffer cache.</li>
  <li><em>MySQL:</em> Reads the row-based binary log (<code>binlog_format=ROW</code>, <code>binlog_row_image=FULL</code>) using GTIDs.</li>
  <li><em>Oracle:</em> Mines transaction redo logs via Oracle LogMiner or Oracle GoldenGate integrations.</li>
  <li><em>SQL Server:</em> Consumes change tables populated by SQL Server Change Data Capture (CDC) agent jobs.</li>
  </ul>
</li>
<li><strong>Backfill Phase vs. Continuous Streaming Phase:</strong>
  <ul>
  <li><em>Backfill Phase:</em> When a stream is initialized, Datastream extracts the existing historical state of selected tables. It divides large tables into parallel primary-key chunks, executing concurrent read queries against the source database. Architects must carefully tune connection pool limits and schedule backfills during low-traffic windows to prevent exhausting source database CPU and I/O.</li>
  <li><em>Streaming Phase:</em> Once backfill completes, Datastream transitions into continuous log tailing. In this mode, source resource utilization is minimal (typically &lt;2% CPU overhead and negligible disk I/O).</li>
  </ul>
</li>
<li><strong>Operational Telemetry, Lag Metrics, and WAL Disk Exhaustion Risk:</strong>
  <ul>
  <li><em>Stream Latency Telemetry:</em> The primary operational health indicator is <code>datastream.googleapis.com/stream/stream_latency</code>, which measures the elapsed time from transaction commit on the source database to successful delivery and acknowledgment at the destination sink. Alerts should trigger if latency exceeds 60 seconds.</li>
  <li><em>The Replication Slot Disk Exhaustion Hazard:</em> In PostgreSQL, an active replication slot retains WAL files on disk until the downstream consumer (Datastream) acknowledges consumption. If Datastream is paused, network connectivity breaks, or the target BigQuery ingestion experiences backpressure, the source database cannot recycle WAL files. The <code>pg_wal</code> directory grows unbounded until source disk storage reaches 100%, causing the PostgreSQL instance to crash and halt all production OLTP operations. Operational mitigation requires configuring Cloud SQL storage auto-increase, setting alerts on replication slot unread bytes, and establishing maximum WAL size safety thresholds (<code>max_slot_wal_keep_size</code>).</li>
  </ul>
</li>
<li><strong>Schema Drift Handling:</strong> Production databases undergo routine DDL schema alterations. Datastream automatically detects and propagates non-breaking schema modifications (such as <code>ALTER TABLE ADD COLUMN</code>) to BigQuery and Cloud Storage without pausing the stream. For breaking DDL changes (dropping a column, renaming a field, or changing data types), Datastream provides configurable behavior: it can pause the affected table stream, allowing administrators to migrate downstream tables, or forward raw JSON payloads containing schema evolution metadata.</li>
</ul>

<p><strong>Table 63.2: Database Migration Service (DMS) vs. Datastream CDC Comparison</strong></p>
<table>
<thead>
<tr>
<th>Architectural Dimension</th>
<th>Database Migration Service (DMS)</th>
<th>Datastream Serverless CDC</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Primary Architectural Purpose</strong></td>
<td>Permanent database lift-and-shift migration with minimal downtime.</td>
<td>Continuous, real-time change data capture and streaming integration.</td>
</tr>
<tr>
<td><strong>Source Database Support</strong></td>
<td>PostgreSQL, MySQL, SQL Server (On-Prem, AWS RDS, Compute Engine).</td>
<td>Oracle, PostgreSQL, MySQL, SQL Server.</td>
</tr>
<tr>
<td><strong>Destination Sink Targets</strong></td>
<td>Cloud SQL (MySQL/Postgres/SQL Server) and AlloyDB for PostgreSQL.</td>
<td>BigQuery (Streaming Upsert Merge), Cloud Storage (Avro/JSON), Pub/Sub.</td>
</tr>
<tr>
<td><strong>Operational Lifecycle</strong></td>
<td>Transient/Finite: Terminates upon final application cutover.</td>
<td>Permanent: Continuous operational data pipeline running indefinitely.</td>
</tr>
<tr>
<td><strong>Data Transformation Capability</strong></td>
<td>Homogeneous: Replicates exact database schema and data types.</td>
<td>Heterogeneous: Enriches events with CDC metadata (LSN, change type, timestamp).</td>
</tr>
<tr>
<td><strong>BigQuery Integration</strong></td>
<td>None (Requires separate replication/ETL tooling).</td>
<td>Native automated streaming upsert merge into real-time analytical tables.</td>
</tr>
<tr>
<td><strong>Cutover Requirement</strong></td>
<td>Requires planned cutover window to promote replica and redirect traffic.</td>
<td>Zero cutover window; source and destination remain independent systems.</td>
</tr>
<tr>
<td><strong>Failure &amp; Backpressure Risk</strong></td>
<td>Replication lag delays migration cutover milestone.</td>
<td>Unread replication slots can accumulate WAL and exhaust source disk.</td>
</tr>
</tbody>
</table>

<div class="callout"><strong>Apply it</strong><p>Input: the enterprise data engineering team must synchronize 500,000 daily inventory and fulfillment mutations from an on-premises PostgreSQL cluster to BigQuery without impacting production OLTP transaction latency. Expected: a serverless Datastream CDC architecture utilizing non-locking WAL logical decoding via pgoutput, with automated BigQuery continuous merge upsert, stream_latency alerting, and replication slot disk thresholds.</p></div>

<div class="callout"><strong>Further study</strong>
<p><a href="../sources.html#topic-020">Topic 020 source section</a> in this site, with original publisher links and the reading context.</p>
<p>Publisher: <a href="https://docs.cloud.google.com/datastream/docs" rel="noopener noreferrer">Google Cloud Datastream Documentation</a>. Official documentation on serverless change data capture, transaction log mining (PostgreSQL WAL, MySQL binlog, Oracle LogMiner), and BigQuery continuous streaming integration.</p>
</div>
</article>

<article id="topic-03-technical" class="topic-card">
<h3>CDC correctness returns on Days 76 and 137</h3>
<p>Architecting distributed data pipelines requires maintaining strict consistency boundaries between transactional storage and downstream replicas. Systems must explicitly address transport delivery semantics, out-of-order event delivery, and the fundamental criteria governing database selection across Google Cloud's storage portfolio.</p>

<p><strong>CDC Correctness: Transport Delivery vs. Application End-to-End Correctness:</strong></p>
<ul>
<li><strong>At-Least-Once Transport Delivery:</strong> Messaging fabrics and streaming transports—including Cloud Pub/Sub, Datastream, and database replication slots—operate on at-least-once delivery semantics. In the event of transient network drops, consumer rebalancing, or worker crashes prior to message acknowledgment, identical CDC mutation records are retransmitted. Applications that assume "exactly-once delivery" at the transport layer suffer silent data corruption (e.g., executing duplicate financial debits or double-incrementing inventory allocations).</li>
<li><strong>End-to-End Idempotency:</strong> Idempotent processing ensures that applying the same mutation event multiple times produces the exact same system state as applying it once. A CDC pipeline achieves end-to-end correctness only when consumers maintain an idempotent processing layer backed by unique transaction identifiers and version checks.</li>
<li><strong>The Out-of-Order Event Arrival Hazard:</strong> In distributed networks, mutation events generated in strict chronological sequence on the source database can arrive out of order at the consumer due to multi-partition streaming, network jitter, or multi-threaded worker pools. For example:
  <ol>
  <li><em>Time t1 (Source):</em> Order 101 status updated to <code>SHIPPED</code>.</li>
  <li><em>Time t2 (Source):</em> Order 101 status updated to <code>DELIVERED</code>.</li>
  <li><em>Delivery (Network):</em> Due to thread scheduling, the consumer processes the <code>DELIVERED</code> event first, writing <code>status = 'DELIVERED'</code> to the destination table.</li>
  <li><em>Delivery (Delayed):</em> Moments later, the delayed <code>SHIPPED</code> event arrives. If processed naively, it overwrites the record, leaving Order 101 permanently stuck in <code>SHIPPED</code> state.</li>
  </ol>
</li>
<li><strong>Deterministic Ordering Tokens: LSN, SCN, and Timestamp Vectors:</strong>
  To prevent out-of-order state corruption, consumers must enforce deterministic monotonic sequencing using transaction log coordinates provided in Datastream metadata:
  <ul>
  <li><em>PostgreSQL Log Sequence Number (LSN):</em> A 64-bit integer representing the exact byte offset of the transaction record in the source database Write-Ahead Log (WAL). LSN is strictly monotonically increasing for every transaction commit.</li>
  <li><em>Oracle System Change Number (SCN):</em> A monotonically increasing logical timestamp stamping every commit.</li>
  <li><em>MySQL GTID &amp; Binlog Coordinates:</em> Global Transaction Identifiers ensuring deterministic sequence across multi-master and replica topologies.</li>
  <li><em>Datastream Metadata Envelope:</em> Every CDC event emitted by Datastream contains:
    <pre><code>_metadata_source_timestamp: Event commit time on source DB
_metadata_lsn: 64-bit Log Sequence Number (PostgreSQL)
_metadata_scn: System Change Number (Oracle)
_metadata_change_type: INSERT / UPDATE / DELETE
_metadata_is_deleted: Boolean indicating deletion</code></pre>
  </li>
  </ul>
</li>
<li><strong>Deterministic Reconciliation via BigQuery SQL MERGE:</strong>
  When streaming CDC into BigQuery or downstream datastores, the target table must not execute un-versioned updates. Instead, ingestion queries or scheduled merge jobs utilize window functions to isolate the latest record by LSN and timestamp:
  <pre><code>MERGE INTO `project.dataset.orders_current` T
USING (
  SELECT * EXCEPT(row_num)
  FROM (
    SELECT *,
      ROW_NUMBER() OVER (
        PARTITION BY order_id 
        ORDER BY _metadata_source_timestamp DESC, _metadata_lsn DESC
      ) AS row_num
    FROM `project.dataset.orders_cdc_stream`
  )
  WHERE row_num = 1
) S
ON T.order_id = S.order_id
WHEN MATCHED AND S._metadata_change_type = 'DELETE' THEN
  DELETE
WHEN MATCHED AND S._metadata_lsn &gt; T._metadata_lsn THEN
  UPDATE SET status = S.status, total_amount = S.total_amount, _metadata_lsn = S._metadata_lsn
WHEN NOT MATCHED AND S._metadata_change_type != 'DELETE' THEN
  INSERT (order_id, status, total_amount, _metadata_lsn)
  VALUES (S.order_id, S.status, S.total_amount, S._metadata_lsn);</code></pre>
  This deterministic merge guarantees that delayed, out-of-order events with lower LSNs are discarded, preserving system state correctness.
</li>
</ul>

<p><strong>Unified Google Cloud Database Selection Framework:</strong></p>
<p>Enterprise architects frequently face architectural impedance mismatches by choosing the wrong storage engine for their workload access patterns. Google Cloud provides seven core database products, each optimized for distinct operational profiles:</p>
<ol>
<li><strong>Cloud SQL:</strong> Managed MySQL, PostgreSQL, and SQL Server. Best for standard enterprise relational OLTP workloads (&lt;64 TB storage, &lt;96 vCPUs) requiring full SQL dialect compatibility, complex joins, stored procedures, and ACID compliance within a single primary instance backed by cross-zone HA.</li>
<li><strong>AlloyDB for PostgreSQL:</strong> Enterprise-grade PostgreSQL-compatible database featuring a disaggregated compute and storage architecture, an integrated columnar engine for analytical acceleration, automated indexing, fast failover (&lt;10s), and a 99.99% inclusive SLA. Ideal for high-scale hybrid transactional and analytical processing (HTAP) demanding up to 4x faster transactional throughput and 100x faster analytical queries than standard PostgreSQL.</li>
<li><strong>Cloud Spanner:</strong> Globally distributed, horizontally scalable relational database offering external consistency (strict serializability via TrueTime atomic clock synchronization) and multi-region active-active Paxos consensus. Delivers five 9s (99.999%) availability SLA, unlimited horizontal write scaling, transparent sharding, and zero planned downtime. Mandatory for mission-critical global financial ledgers, global inventory, and multi-region e-commerce.</li>
<li><strong>Cloud Firestore:</strong> Serverless document NoSQL database featuring automatic scaling to zero, live snapshot listeners for real-time mobile/web sync, multi-region 99.999% SLA, and offline client persistence. Best for mobile application state, user profiles, and flexible hierarchical JSON catalogs. Subject to a strict 1 write/sec per document throughput limit.</li>
<li><strong>Cloud Bigtable:</strong> Ultra-high-throughput, sparsely populated, wide-column NoSQL database (Apache HBase API). Delivers single-digit millisecond p99 latency at petabyte scale and millions of operations per second. Optimal for high-velocity IoT telemetry, financial ticker feeds, and user clickstream analysis. Constrained by a single primary row key without secondary indexes or multi-row transactions.</li>
<li><strong>Cloud Memorystore:</strong> Sub-millisecond in-memory cache and session store (Redis / Memcached / Redis Cluster). Ideal for absorbing read traffic, caching computed database queries, managing distributed mutex locks, and tracking transient ephemeral state.</li>
<li><strong>BigQuery:</strong> Serverless, petabyte-scale analytical data warehouse (OLAP) with decoupled storage (Capacitor) and compute (Dremel). Engineered for high-throughput batch and continuous streaming analytics, complex aggregation queries across billions of rows, and built-in machine learning. Unsuitable for low-latency row-level point lookups or transactional OLTP.</li>
</ol>

<p><strong>Table 63.3: Unified Google Cloud Database Selection Decision Matrix</strong></p>
<table>
<thead>
<tr>
<th>Database Service</th>
<th>Primary Data Model</th>
<th>p99 Latency</th>
<th>Scaling Boundary</th>
<th>Consistency Model</th>
<th>Availability SLA</th>
<th>Primary Cost Driver</th>
<th>Ideal Workload &amp; Anti-Pattern</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Cloud SQL</strong></td>
<td>Relational (PostgreSQL, MySQL, SQL Server)</td>
<td>5–15 ms</td>
<td>Vertical scale up to 96 vCPU, 64 TB; Read replicas up to 10.</td>
<td>Strict ACID (Single-region instance)</td>
<td>99.95% (Single-zone) / 99.99% (Cross-zone HA)</td>
<td>Provisioned vCPU, RAM, storage (SSD), egress.</td>
<td><strong>Ideal:</strong> Traditional enterprise OLTP, ERP, CRM.<br><strong>Anti-pattern:</strong> Global active-active writes, massive IoT telemetry.</td>
</tr>
<tr>
<td><strong>AlloyDB for PostgreSQL</strong></td>
<td>Relational / Columnar HTAP (PostgreSQL 100%)</td>
<td>2–8 ms</td>
<td>Vertical scale up to 128 vCPU; Disaggregated storage to tens of TBs.</td>
<td>Strict ACID (PostgreSQL MVCC)</td>
<td>99.99% (Inclusive of maintenance)</td>
<td>Provisioned compute nodes, disaggregated storage consumed.</td>
<td><strong>Ideal:</strong> High-throughput transactional OLTP + real-time reporting.<br><strong>Anti-pattern:</strong> Multi-region active-active distributed transactions.</td>
</tr>
<tr>
<td><strong>Cloud Spanner</strong></td>
<td>Relational with Global Schemas</td>
<td>5–15 ms</td>
<td>Unlimited horizontal scale; thousands of Paxos nodes.</td>
<td>External Consistency (Strict Serializability via TrueTime)</td>
<td>99.99% (Regional) / 99.999% (Multi-region)</td>
<td>Provisioned Spanner nodes / processing units (PU), storage.</td>
<td><strong>Ideal:</strong> Global financial ledgers, multi-region commerce, inventory.<br><strong>Anti-pattern:</strong> Transient session caching, sub-millisecond key-value lookups.</td>
</tr>
<tr>
<td><strong>Cloud Firestore</strong></td>
<td>Hierarchical Document NoSQL (JSON)</td>
<td>10–30 ms</td>
<td>Horizontal automatic scaling to millions of clients.</td>
<td>Strong consistency on documents; Eventual on global queries.</td>
<td>99.99% (Regional) / 99.999% (Multi-region)</td>
<td>Document reads, writes, deletes, and storage volume.</td>
<td><strong>Ideal:</strong> Mobile/web backends, user profiles, real-time client sync.<br><strong>Anti-pattern:</strong> Counter updates exceeding 1 write/sec per document.</td>
</tr>
<tr>
<td><strong>Cloud Bigtable</strong></td>
<td>Wide-Column NoSQL (SSTable/HFile)</td>
<td>&lt;6 ms</td>
<td>Linear horizontal scale; petabytes of data, millions of QPS.</td>
<td>Single-row strong consistency; Eventual across clusters.</td>
<td>99.9% (Single cluster) / 99.999% (Multi-cluster routing)</td>
<td>Provisioned cluster nodes, SSD storage consumed.</td>
<td><strong>Ideal:</strong> IoT time-series, clickstream telemetry, high-QPS write floods.<br><strong>Anti-pattern:</strong> Complex multi-table relational joins, low-volume relational data.</td>
</tr>
<tr>
<td><strong>Cloud Memorystore</strong></td>
<td>In-Memory Key-Value &amp; Data Structures (Redis/Memcached)</td>
<td>&lt;1 ms (sub-millisecond)</td>
<td>Vertical scale (Standard) or up to 250 shards / 10 TB (Cluster).</td>
<td>In-memory immediate; Eventual across async read replicas.</td>
<td>Basic: None / Standard: 99.9% / Cluster: 99.99%</td>
<td>Provisioned memory capacity (GB) and cluster node hours.</td>
<td><strong>Ideal:</strong> Sub-millisecond cache-aside, session stores, mutex locks.<br><strong>Anti-pattern:</strong> Durable primary ledger storage (data loss on crash/flush).</td>
</tr>
<tr>
<td><strong>BigQuery</strong></td>
<td>Columnar Analytical Warehouse (Capacitor)</td>
<td>数百ms to seconds</td>
<td>Petabyte / Exabyte scale; thousands of dynamic compute slots.</td>
<td>Read-committed; strong consistency on metadata.</td>
<td>99.99% multi-region SLA</td>
<td>Slot compute hours (or bytes scanned) + active/long-term storage.</td>
<td><strong>Ideal:</strong> Enterprise data warehousing, business intelligence, CDC analytics.<br><strong>Anti-pattern:</strong> Low-latency transactional point queries (OLTP).</td>
</tr>
</tbody>
</table>

<div class="callout"><strong>Apply it</strong><p>Input: an enterprise architect must select the target persistence and caching engines for Brightloaf's omnichannel platform spanning transactional ledgers, IoT fleet tracking, mobile client sync, and analytical reporting. Expected: an architectural decision record applying the unified GCP database selection framework, routing ACID transactions to AlloyDB/Cloud SQL, global catalog to Spanner, mobile carts to Firestore, sensor telemetry to Bigtable, session cache to Memorystore, and analytics to BigQuery, while enforcing deterministic LSN ordering for CDC stream ingestion.</p></div>

<div class="callout"><strong>Further study</strong>
<p><a href="../sources.html#topic-020">Topic 020 source section</a> in this site, with original publisher links and the reading context.</p>
<p>Publisher: <a href="https://cloud.google.com/products/databases" rel="noopener noreferrer">Google Cloud Database Portfolio</a>. Architectural guide and selection framework across Cloud SQL, AlloyDB, Cloud Spanner, Firestore, Bigtable, Memorystore, and BigQuery.</p>
</div>
</article>
</section>
"""
