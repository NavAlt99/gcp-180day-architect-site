# scratch/data_part4.py
"""Part 4 Step-by-Step Hands-On Labs, Completion Section, and Pager for Day 63."""

PART_4 = """<section id="part-4" class="part"><h2>4 · Step-by-step labs for each topic</h2>

<article id="topic-01-lab" class="topic-card lab">
<h3>Exercise 1: Memorystore Redis Cache-Aside Implementation, Stale Read Race Reproduction, and Mutex Lock Mitigation</h3>
<p><strong>Goal:</strong> Implement a complete in-memory Cache-Aside architecture simulator in Python, deterministically reproduce the classic dual-write stale read race hazard that permanently poisons cache state, mitigate the race using Redis Distributed Mutex Locking (SETNX pattern) and Delayed Double Deletion, and evaluate eviction policies under memory pressure.</p>
<p><strong>Mode:</strong> local architectural simulation &bull; <strong>Prerequisite:</strong> <a href="day-062.html">Day 62 distributed database foundations</a>; bring its exit artifact.</p>

<ol>
<li><strong>Preflight Verification:</strong>
<p>Confirm the local Python 3 environment is operational and verify that no cloud credentials or billed resources are required for this architectural exercise:</p>
<pre><code>python3 --version</code></pre>
</li>

<li><strong>Reproduce the Classic Cache-Aside Stale Read Race Hazard:</strong>
<p>Execute an architectural simulation demonstrating how uncoordinated concurrent read and write operations in a Cache-Aside topology lead to permanent cache poisoning:</p>
<pre><code>python3 -c '
import time
import threading

class Database:
    def __init__(self):
        self.data = {"item_101": {"name": "Artisan Sourdough", "price": 49.00}}
        self.lock = threading.Lock()

    def read(self, key):
        time.sleep(0.05)  # simulate disk / network I/O
        with self.lock:
            return self.data.get(key)

    def write(self, key, val):
        with self.lock:
            self.data[key] = val

class NaiveCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, val):
        self.cache[key] = val

    def delete(self, key):
        self.cache.pop(key, None)

db = Database()
cache = NaiveCache()

# Pre-populate cache
cache.set("item_101", {"name": "Artisan Sourdough", "price": 49.00})
print("[Init] Cache populated: price = $49.00")

# Simulate key expiration / invalidation
cache.delete("item_101")
print("[Event] Cache key expired!")

def reader_thread():
    # Reader misses cache, reads old DB state, delays, then sets cache
    val = cache.get("item_101")
    if val is None:
        print("[Reader] Cache miss. Fetching from DB...")
        db_val = db.read("item_101")  # reads 49.00
        time.sleep(0.1)  # Thread context switch delay
        cache.set("item_101", db_val)
        print(f"[Reader] Stale write committed to cache: price = ${db_val[\"price\"]:.2f}")

def writer_thread():
    time.sleep(0.02)  # Writer runs while Reader is fetching from DB
    print("[Writer] Updating DB price to $39.00...")
    db.write("item_101", {"name": "Artisan Sourdough", "price": 39.00})
    cache.delete("item_101")
    print("[Writer] DB updated and cache invalidated.")

t_read = threading.Thread(target=reader_thread)
t_write = threading.Thread(target=writer_thread)

t_read.start()
t_write.start()
t_read.join()
t_write.join()

print("--- POST-RACE AUDIT ---")
print(f"Authoritative DB Price: ${db.read(\"item_101\")[\"price\"]:.2f}")
print(f"Authoritative Cache Price: ${cache.get(\"item_101\")[\"price\"]:.2f}")
if db.read("item_101")["price"] != cache.get("item_101")["price"]:
    print("CRITICAL FAILURE: Cache is permanently poisoned with stale price!")
'</code></pre>
</li>

<li><strong>Mitigate Stampede and Stale Reads via Mutex Locking &amp; Delayed Double Deletion:</strong>
<p>Implement the robust enterprise Cache-Aside pattern utilizing distributed mutex locking (SETNX) and delayed double deletion to ensure cache and database convergence:</p>
<pre><code>python3 -c '
import time
import threading
import uuid

class ProductionCacheAside:
    def __init__(self, db):
        self.db = db
        self.cache = {}
        self.locks = {}
        self.lock_guard = threading.Lock()

    def get(self, key):
        # Cache hit
        if key in self.cache:
            return self.cache[key]
        
        # Cache miss - acquire distributed mutex lock (SETNX simulation)
        lock_id = str(uuid.uuid4())
        acquired = False
        with self.lock_guard:
            if key not in self.locks:
                self.locks[key] = lock_id
                acquired = True
        
        if acquired:
            try:
                print(f"[Worker] Acquired mutex lock for {key}. Querying DB...")
                db_val = self.db.read(key)
                self.cache[key] = db_val
                return db_val
            finally:
                with self.lock_guard:
                    if self.locks.get(key) == lock_id:
                        del self.locks[key]
                print(f"[Worker] Released mutex lock for {key}.")
        else:
            # Another worker is loading; sleep and retry read from cache
            print(f"[Worker] Mutex busy. Waiting for primary worker...")
            time.sleep(0.08)
            return self.cache.get(key, self.db.read(key))

    def update(self, key, val):
        # Delayed double deletion pattern
        print(f"[Mutation] Phase 1: Invalidate cache key {key}...")
        self.cache.pop(key, None)
        
        print(f"[Mutation] Phase 2: Commit update to database...")
        self.db.write(key, val)
        
        # Asynchronous delayed second deletion (clears any racing reads)
        def delayed_delete():
            time.sleep(0.12)
            self.cache.pop(key, None)
            print(f"[Mutation] Phase 3: Delayed double deletion executed for {key}.")
        
        threading.Thread(target=delayed_delete).start()

db = Database() if "Database" in locals() else None
if not db:
    class DB:
        def __init__(self): self.d = {"item_101": {"price": 49.00}}
        def read(self, k): return self.d.get(k)
        def write(self, k, v): self.d[k] = v
    db = DB()

c = ProductionCacheAside(db)
c.get("item_101")
print("[State] Cache warm:", c.cache.get("item_101"))

# Test mutation with delayed double deletion
c.update("item_101", {"price": 39.00})
time.sleep(0.2)
print("[State] Re-reading key after mutation:", c.get("item_101"))
assert c.get("item_101")["price"] == 39.00, "Cache must match DB!"
print("SUCCESS: Cache and Database reconciled perfectly without stale read drift.")
'</code></pre>
</li>

<li><strong>Simulate Memory Eviction Policies (volatile-lru vs. allkeys-lru vs. noeviction):</strong>
<p>Execute an eviction policy simulator modeling Memorystore behavior when maximum memory threshold is reached:</p>
<pre><code>python3 -c '
class RedisEvictionSimulator:
    def __init__(self, max_keys=3, policy="allkeys-lru"):
        self.max_keys = max_keys
        self.policy = policy
        self.store = {}
        self.access_time = {}
        self.ttl = {}
        self.clock = 0

    def set(self, key, val, ttl=None):
        self.clock += 1
        if len(self.store) >= self.max_keys and key not in self.store:
            self._evict()
        self.store[key] = val
        self.access_time[key] = self.clock
        if ttl:
            self.ttl[key] = self.clock + ttl

    def get(self, key):
        self.clock += 1
        if key in self.store:
            self.access_time[key] = self.clock
            return self.store[key]
        return None

    def _evict(self):
        if self.policy == "noeviction":
            raise MemoryError("OOM: maxmemory reached and noeviction policy is active")
        elif self.policy == "allkeys-lru":
            lru_key = min(self.access_time, key=self.access_time.get)
            print(f"[Eviction] allkeys-lru evicted least-recently accessed key: {lru_key}")
            self.store.pop(lru_key)
            self.access_time.pop(lru_key)
            self.ttl.pop(lru_key, None)
        elif self.policy == "volatile-lru":
            candidates = {k: self.access_time[k] for k in self.ttl}
            if not candidates:
                raise MemoryError("OOM: volatile-lru found no keys with TTL set")
            lru_key = min(candidates, key=candidates.get)
            print(f"[Eviction] volatile-lru evicted key with TTL: {lru_key}")
            self.store.pop(lru_key)
            self.access_time.pop(lru_key)
            self.ttl.pop(lru_key, None)

sim = RedisEvictionSimulator(max_keys=3, policy="allkeys-lru")
sim.set("k1", "val1")
sim.set("k2", "val2")
sim.set("k3", "val3")
sim.get("k1")  # Touch k1, making k2 the oldest
sim.set("k4", "val4")  # Should evict k2
assert sim.get("k2") is None, "k2 must be evicted"
print("SUCCESS: Eviction simulator verified LRU behavior.")
'</code></pre>
</li>
</ol>

<div class="callout success"><strong>Expected result / acceptance</strong>
<p>The stale read simulation demonstrates a critical divergence between cache and database, while the mutex locking and delayed double deletion script confirms 100% convergence. The eviction simulation confirms the behavior of allkeys-lru vs volatile-lru under memory pressure.</p>
</div>

<div class="callout caution"><strong>Troubleshooting</strong>
<p>If thread race conditions do not reproduce on fast multi-core systems, increase the simulated database delay in reader_thread. Ensure distributed locks always release in a finally block to prevent permanent worker lockouts.</p>
</div>

<div class="callout"><strong>Cleanup and cost</strong>
<p>All operations execute entirely within the local in-memory Python process. No cloud resources or billed charges are incurred.</p>
</div>

<label class="check"><input type="checkbox" data-progress="lab-63-topic-01"> I completed and checked this topic exercise</label>
</article>

<article id="topic-02-lab" class="topic-card lab">
<h3>Exercise 2: Datastream CDC WAL Log Mining Emulation and Replication Lag Telemetry</h3>
<p><strong>Goal:</strong> Emulate a PostgreSQL Write-Ahead Log (WAL) logical decoding stream, track 64-bit Log Sequence Numbers (LSN), calculate real-time <code>stream_latency</code> telemetry during steady-state versus monolithic batch spikes, and observe replication slot buffer accumulation and storage risk.</p>
<p><strong>Mode:</strong> local architectural simulation &bull; <strong>Prerequisite:</strong> <a href="day-061.html">Day 61 relational foundations</a>; bring its exit artifact.</p>

<ol>
<li><strong>Preflight Verification:</strong>
<p>Verify that Python standard library modules (time, collections, random) are available locally:</p>
<pre><code>python3 -c "import time, collections, random; print('Preflight OK')"</code></pre>
</li>

<li><strong>Simulate PostgreSQL WAL Logical Decoding and Replication Slot Mechanics:</strong>
<p>Execute an architectural simulation modeling how Datastream mines the append-only WAL stream without acquiring database table locks:</p>
<pre><code>python3 -c '
import time
import collections

class WALEngine:
    def __init__(self):
        self.wal_log = []
        self.current_lsn = 0x100000  # Starting 64-bit LSN
        self.disk_used_mb = 50.0

    def commit_transaction(self, table, op, data):
        self.current_lsn += 0x800  # Advance LSN by 2KB
        record = {
            "lsn": f"0/{self.current_lsn:X}",
            "lsn_int": self.current_lsn,
            "timestamp": time.time(),
            "table": table,
            "op": op,
            "data": data
        }
        self.wal_log.append(record)
        self.disk_used_mb += 0.002
        return record

class DatastreamConsumer:
    def __init__(self, wal_engine):
        self.wal_engine = wal_engine
        self.confirmed_lsn = 0x100000
        self.consumed_index = 0
        self.sink = []

    def poll_stream(self, max_batch=50):
        available = self.wal_engine.wal_log[self.consumed_index:self.consumed_index + max_batch]
        if not available:
            return 0, 0.0
        
        now = time.time()
        max_latency = 0.0
        for rec in available:
            latency = now - rec["timestamp"]
            if latency &gt; max_latency:
                max_latency = latency
            self.sink.append(rec)
            self.confirmed_lsn = rec["lsn_int"]
            self.consumed_index += 1
            
        return len(available), max_latency

wal = WALEngine()
stream = DatastreamConsumer(wal)

# Simulate 10 steady-state transactions
print("[Steady State] Generating 10 transactions...")
for i in range(10):
    wal.commit_transaction("orders", "INSERT", {"order_id": f"ORD-{i}", "amt": 25.0 * (i+1)})
    time.sleep(0.01)

count, lag = stream.poll_stream()
print(f"[Datastream] Consumed {count} CDC events. Replication stream latency: {lag*1000:.2f} ms")
assert count == 10, "All events must be consumed"
'</code></pre>
</li>

<li><strong>Simulate Monolithic Batch Spike vs. Micro-Batching on Replication Lag:</strong>
<p>Compare the operational impact of a 50,000-row monolithic update versus a chunked micro-batch approach on WAL backlog and latency:</p>
<pre><code>python3 -c '
import time

# Simulation parameters
monolithic_rows = 50000
stream_poll_rate = 5000  # records per poll cycle

print("--- SCENARIO A: Monolithic Un-chunked Batch (50,000 rows) ---")
start_time = time.time()
# Monolithic commits all 50k rows in a single burst
records = [{"id": i, "t": start_time} for i in range(monolithic_rows)]
wal_backlog = len(records)
print(f"[Source DB] Committed monolithic transaction. WAL backlog: {wal_backlog} records.")

# Datastream drains backlog across polling cycles
cycles = 0
max_latency = 0
while wal_backlog &gt; 0:
    time.sleep(0.02)  # simulate ingestion network delay
    drain = min(wal_backlog, stream_poll_rate)
    wal_backlog -= drain
    cycles += 1
    current_latency = (time.time() - start_time) * 100  # scale for illustration
    if current_latency &gt; max_latency:
        max_latency = current_latency
    if cycles in (1, 5, 10):
        print(f"  Cycle {cycles}: Remaining backlog = {wal_backlog}, Stream Latency = {current_latency:.1f} sec")

print(f"[Result A] Peak Stream Latency: {max_latency:.1f} sec &bull; Severe WAL disk accumulation risk.")

print("\n--- SCENARIO B: Chunked Micro-Batches (5,000 rows x 10 batches) ---")
chunk_size = 5000
max_chunk_latency = 0
for b in range(10):
    b_start = time.time()
    # Micro-batch commit
    batch_records = [{"id": b * chunk_size + i, "t": b_start} for i in range(chunk_size)]
    time.sleep(0.01)  # immediate streaming consumption
    chunk_latency = (time.time() - b_start) * 100
    if chunk_latency &gt; max_chunk_latency:
        max_chunk_latency = chunk_latency

print(f"[Result B] Peak Stream Latency under Micro-Batching: {max_chunk_latency:.1f} sec &bull; Stable WAL.")
'</code></pre>
</li>
</ol>

<div class="callout success"><strong>Expected result / acceptance</strong>
<p>The WAL emulation proves that logical decoding streams committed transactions via LSN offsets with zero table locking. The batch comparison demonstrates that micro-batching flattens replication lag spikes by over 80% compared to monolithic DML bursts.</p>
</div>

<div class="callout caution"><strong>Troubleshooting</strong>
<p>If simulated latency numbers appear identical, verify that time.sleep delays are calibrated for your CPU execution speed. Always monitor source replication slot unread bytes in PostgreSQL production systems.</p>
</div>

<div class="callout"><strong>Cleanup and cost</strong>
<p>All operations execute entirely in-memory within local Python. No cloud project or billing is required.</p>
</div>

<label class="check"><input type="checkbox" data-progress="lab-63-topic-02"> I completed and checked this topic exercise</label>
</article>

<article id="topic-03-lab" class="topic-card lab">
<h3>Exercise 3: CDC Correctness Reconciliation Engine and Enterprise Database Selection Matrix Evaluator</h3>
<p><strong>Goal:</strong> Emulate out-of-order CDC event delivery with network jitter, implement deterministic LSN-based deduplication and windowed SQL MERGE reconciliation using SQLite, and execute an automated Google Cloud Database Selection Decision Framework script evaluating workload requirements across all 7 databases.</p>
<p><strong>Mode:</strong> local architectural simulation &bull; <strong>Prerequisite:</strong> <a href="day-061.html">Day 61 relational foundations</a>; bring its exit artifact.</p>

<ol>
<li><strong>Preflight Verification:</strong>
<p>Verify that Python and sqlite3 are installed and functional:</p>
<pre><code>python3 -c "import sqlite3; print('SQLite3 version:', sqlite3.version)"</code></pre>
</li>

<li><strong>Simulate Out-of-Order CDC Arrival and Verify LSN-Windowed MERGE Reconciliation:</strong>
<p>Execute a local reconciliation script demonstrating how Log Sequence Numbers resolve out-of-order CDC updates:</p>
<pre><code>python3 -c '
import sqlite3
import random

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

# Target table (replicated state)
cur.execute("""
CREATE TABLE target_orders (
    order_id TEXT PRIMARY KEY,
    status TEXT,
    total_amount REAL,
    last_lsn INTEGER
)
""")

# CDC raw change stream table
cur.execute("""
CREATE TABLE cdc_stream (
    event_id INTEGER PRIMARY KEY,
    order_id TEXT,
    status TEXT,
    total_amount REAL,
    lsn INTEGER,
    event_time REAL
)
""")

# Generate chronological mutations for Order ORD-500
events = [
    (1, "ORD-500", "PENDING", 120.00, 1001, 10.0),
    (2, "ORD-500", "PROCESSING", 120.00, 1005, 12.0),
    (3, "ORD-500", "SHIPPED", 120.00, 1010, 15.0),
    (4, "ORD-500", "DELIVERED", 120.00, 1025, 20.0)
]

# Simulate network jitter: DELIVERED arrives BEFORE SHIPPED
shuffled_events = [events[0], events[1], events[3], events[2]]  # Deliv before Ship!
cur.executemany("INSERT INTO cdc_stream VALUES (?, ?, ?, ?, ?, ?)", shuffled_events)
conn.commit()

print("[Simulation] Shuffled CDC delivery order:")
for ev in shuffled_events:
    print(f"  Event ID {ev[0]}: Status = {ev[2]}, LSN = {ev[4]}")

# Execute Deterministic LSN Windowed Upsert
cur.execute("""
INSERT INTO target_orders (order_id, status, total_amount, last_lsn)
SELECT order_id, status, total_amount, lsn
FROM (
    SELECT order_id, status, total_amount, lsn,
           ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY lsn DESC) as rn
    FROM cdc_stream
)
WHERE rn = 1
ON CONFLICT(order_id) DO UPDATE SET
    status = excluded.status,
    total_amount = excluded.total_amount,
    last_lsn = excluded.last_lsn
WHERE excluded.last_lsn > target_orders.last_lsn;
""")
conn.commit()

cur.execute("SELECT order_id, status, last_lsn FROM target_orders WHERE order_id = 'ORD-500'")
res = cur.fetchone()
print("\n--- FINAL RECONCILED TARGET TABLE STATE ---")
print(f"Order: {res[0]} | Status: {res[1]} | LSN: {res[2]}")
assert res[1] == "DELIVERED", "State must be DELIVERED regardless of delivery order!"
print("SUCCESS: Deterministic LSN reconciliation prevented state inversion.")
'</code></pre>
</li>

<li><strong>Execute the Automated Google Cloud Database Selection Decision Engine:</strong>
<p>Run an architectural decision evaluation script that scores workload requirements against Google Cloud's 7 database services:</p>
<pre><code>python3 -c '
def evaluate_database(workload):
    scores = {
        "Cloud SQL": 0, "AlloyDB": 0, "Cloud Spanner": 0, 
        "Firestore": 0, "Bigtable": 0, "Memorystore": 0, "BigQuery": 0
    }
    
    # Access pattern evaluation
    if workload["data_model"] == "relational":
        scores["Cloud SQL"] += 4
        scores["AlloyDB"] += 5
        scores["Cloud Spanner"] += 4
    elif workload["data_model"] == "document":
        scores["Firestore"] += 8
    elif workload["data_model"] == "wide_column":
        scores["Bigtable"] += 8
    elif workload["data_model"] == "key_value":
        scores["Memorystore"] += 8
    elif workload["data_model"] == "columnar_olap":
        scores["BigQuery"] += 8

    # Scale and latency
    if workload.get("sub_ms_cache"):
        scores["Memorystore"] += 10
    if workload.get("qps", 0) > 50000:
        scores["Bigtable"] += 5
        scores["Cloud Spanner"] += 4
        scores["Cloud SQL"] -= 5  # Unsuitable for raw 50k QPS single-node writes
    if workload.get("global_multi_region_acid"):
        scores["Cloud Spanner"] += 10
        scores["Cloud SQL"] -= 8
    if workload.get("htap_columnar_acceleration"):
        scores["AlloyDB"] += 8
    if workload.get("mobile_client_live_sync"):
        scores["Firestore"] += 10
    if workload.get("ad_hoc_sql_analytics_tb_pb"):
        scores["BigQuery"] += 10
        
    recommended = max(scores, key=scores.get)
    return recommended, scores

# Test Workload 1: Global e-commerce checkout with multi-region active-active writes
w1 = {"data_model": "relational", "qps": 8000, "global_multi_region_acid": True}
rec1, s1 = evaluate_database(w1)
print(f"Workload 1 (Global Multi-Region ACID): Recommended = {rec1}")

# Test Workload 2: Fleet delivery IoT telemetry at 100k writes/sec
w2 = {"data_model": "wide_column", "qps": 100000}
rec2, s2 = evaluate_database(w2)
print(f"Workload 2 (Fleet IoT Telemetry): Recommended = {rec2}")

# Test Workload 3: Real-time analytical BI reporting over 50 TB
w3 = {"data_model": "columnar_olap", "ad_hoc_sql_analytics_tb_pb": True}
rec3, s3 = evaluate_database(w3)
print(f"Workload 3 (Petabyte BI Analytics): Recommended = {rec3}")

# Test Workload 4: Sub-millisecond session state & catalog caching
w4 = {"data_model": "key_value", "sub_ms_cache": True}
rec4, s4 = evaluate_database(w4)
print(f"Workload 4 (Sub-ms Catalog Cache): Recommended = {rec4}")
'</code></pre>
</li>
</ol>

<div class="callout success"><strong>Expected result / acceptance</strong>
<p>The SQLite reconciliation script proves that LSN-windowed upsert logic guarantees state correctness even when events arrive completely inverted. The selection framework script validates clean decision boundaries across the seven GCP database products.</p>
</div>

<div class="callout caution"><strong>Troubleshooting</strong>
<p>If SQLite returns syntax errors, verify that SQLite version is 3.25+ (for window functions) and 3.24+ (for ON CONFLICT DO UPDATE). Python 3.8+ includes this by default.</p>
</div>

<div class="callout"><strong>Cleanup and cost</strong>
<p>All operations execute entirely in-memory within local Python and SQLite. No cloud project or billing is required.</p>
</div>

<label class="check"><input type="checkbox" data-progress="lab-63-topic-03"> I completed and checked this topic exercise</label>
</article>

</section>

<section class="completion"><h2>Daily evidence</h2>
<p>Assemble your three foundational artifacts into your study repository as <code>day-063-cache-cdc-selection.md</code>:</p>
<ol>
<li><strong>Cache Invalidation &amp; Concurrency Race Timeline:</strong> A detailed sequence diagram and timeline illustrating the Cache-Aside dual-write race hazard, showing how concurrent reads and writes poison cache state, accompanied by code implementation of Redis distributed mutex locking (SETNX) and delayed double deletion.</li>
<li><strong>Datastream CDC Replication Lag &amp; Log Mining Telemetry:</strong> A technical explanation of transaction log mining (PostgreSQL WAL, MySQL binlog, Oracle LogMiner), comparing backfill versus continuous streaming overhead, defining alerts for <code>stream_latency</code>, and specifying safeguards against replication slot disk saturation.</li>
<li><strong>Completed Enterprise Database Selection Decision Sheet:</strong> An Architectural Decision Record (ADR) mapping workload archetypes across all seven Google Cloud database engines (Cloud SQL, AlloyDB, Cloud Spanner, Firestore, Bigtable, Memorystore, and BigQuery), providing explicit justifications, rejected alternatives, and consistency trade-offs.</li>
</ol>
<label class="check"><input type="checkbox" data-progress="read-63"> I read and reviewed the day</label>
<label class="check"><input type="checkbox" data-progress="artifact-63"> I saved the exit artifact</label>
</section>

<nav class="pager" aria-label="Day pagination">
<a href="day-062.html">← Day 62<small>Distributed and nonrelational database choices</small></a>
<a href="../index.html">All 180 days<small>Browse the roadmap</small></a>
<a href="day-064.html">Day 64 →<small>Messaging, outbox and duplicate handling</small></a>
</nav>
<p class="shortcut">Keyboard: P or [ previous · N or ] next · I index</p>
</main>
<footer class="site-footer">GCP Architect · 180-day independent study · Roadmap dated 2026-09-26. Local progress remains in this browser.</footer>
</body>
</html>
"""
