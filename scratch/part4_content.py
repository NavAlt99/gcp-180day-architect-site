"""Part 4 Content for Day 61: Step-by-step labs for each topic."""

def get_part4_html():
    return """<section id="part-4" class="part">
<h2>4 · Step-by-step labs for each topic</h2>

<article id="topic-01-lab" class="topic-card lab">
<h3>Exercise 1: Cloud SQL connection paths, pooling/limits, maintenance, backup/PITR, regional HA and…</h3>
<p><strong>Goal:</strong> Provision an enterprise-grade Cloud SQL for PostgreSQL Regional HA instance using Private Service Connect (PSC), configure PgBouncer in transaction pooling mode to protect database connection limits, execute an automated high-availability failover drill, and test down-to-the-second Point-in-Time Recovery (PITR).</p>
<p><strong>Mode:</strong> production practice / sandbox &amp; tabletop &middot; <strong>Prerequisite:</strong> <a href="day-060.html">Day 60</a>; bring their exit artifacts.</p>

<ol>
<li><strong>Establish Environment &amp; Network Variables:</strong>
<pre><code># Define working environment variables for Google Cloud SQL &amp; Private Service Connect:
export PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2&gt;/dev/null || echo 'gcp-architect-lab')}"
export REGION="us-central1"
export ZONE_PRIMARY="us-central1-a"
export ZONE_STANDBY="us-central1-b"
export INSTANCE_NAME="brightloaf-pg-primary"
export RESTORE_INSTANCE="brightloaf-pg-pitr-clone"
export VPC_NETWORK="production-vpc"
export PSC_SUBNET="database-psc-subnet"
export PSC_IP="10.128.1.50"
export FORWARDING_RULE="psc-cloudsql-endpoint"

echo "Configured environment for Project: ${PROJECT_ID} in ${REGION}"</code></pre>
</li>

<li><strong>Provision Cloud SQL Regional HA Instance with Private Service Connect:</strong>
<p>Create a high-availability PostgreSQL 16 instance configured with Regional Persistent Disk replication across two zones, automated daily backups, continuous WAL archiving for PITR, a Tuesday 03:00 UTC maintenance window, and Private Service Connect enabled:</p>
<pre><code># Create Cloud SQL Regional HA instance with PSC enabled:
gcloud sql instances create ${INSTANCE_NAME} \
    --project=${PROJECT_ID} \
    --database-version=POSTGRES_16 \
    --tier=db-custom-4-16384 \
    --region=${REGION} \
    --zone=${ZONE_PRIMARY} \
    --secondary-zone=${ZONE_STANDBY} \
    --availability-type=REGIONAL \
    --storage-type=SSD \
    --storage-size=100GB \
    --storage-auto-increase \
    --enable-point-in-time-recovery \
    --backup-start-time=02:00 \
    --maintenance-window-day=TUE \
    --maintenance-window-hour=3 \
    --maintenance-release-channel=default \
    --enable-private-service-connect \
    --allowed-psc-projects=${PROJECT_ID} \
    --no-assign-ip</code></pre>
</li>

<li><strong>Configure Private Service Connect (PSC) Forwarding Rule in Consumer VPC:</strong>
<p>Retrieve the Cloud SQL service attachment link and create a dedicated <code>/32</code> internal IP forwarding rule inside your consumer VPC network:</p>
<pre><code># 1. Retrieve the PSC Service Attachment URI:
SERVICE_ATTACHMENT=$(gcloud sql instances describe ${INSTANCE_NAME} \
    --project=${PROJECT_ID} \
    --format="value(pscServiceAttachmentLink)")

echo "Discovered Cloud SQL Service Attachment: ${SERVICE_ATTACHMENT}"

# 2. Reserve an internal static /32 IP address in consumer subnet:
gcloud compute addresses create psc-sql-address \
    --project=${PROJECT_ID} \
    --region=${REGION} \
    --subnet=${PSC_SUBNET} \
    --addresses=${PSC_IP}

# 3. Create the PSC Forwarding Rule targeting the Service Attachment:
gcloud compute forwarding-rules create ${FORWARDING_RULE} \
    --project=${PROJECT_ID} \
    --region=${REGION} \
    --network=${VPC_NETWORK} \
    --address=psc-sql-address \
    --target-service-attachment=${SERVICE_ATTACHMENT}

echo "Created PSC endpoint ${PSC_IP} targeting Cloud SQL Service Attachment"</code></pre>
</li>

<li><strong>Deploy and Validate PgBouncer in Transaction Pooling Mode:</strong>
<p>Generate a production <code>pgbouncer.ini</code> configuration enforcing transaction-mode multiplexing. This bounds backend database sockets to 32 while serving up to 5,000 incoming client connections:</p>
<pre><code># Create PgBouncer configuration file:
cat &lt;&lt;'EOF' &gt; /tmp/pgbouncer.ini
[databases]
brightloaf_db = host=10.128.1.50 port=5432 dbname=brightloaf_db auth_user=postgres

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid
admin_users = pgbouncer_admin

# Pooling Architecture Configuration:
pool_mode = transaction
max_client_conn = 5000
default_pool_size = 32
min_pool_size = 8
reserve_pool_size = 8
reserve_pool_timeout = 5
max_db_connections = 40

# TCP &amp; Socket Tuning:
server_idle_timeout = 600
client_idle_timeout = 0
query_timeout = 30
server_connect_timeout = 15
tcp_keepalive = 1
tcp_keepcnt = 3
tcp_keepidle = 30
tcp_keepintvl = 10
EOF

echo "Generated production /tmp/pgbouncer.ini configuration"</code></pre>
</li>

<li><strong>Execute Regional HA Failover Drill &amp; Validate Reconnection:</strong>
<p>Simulate an unplanned zonal outage or emergency maintenance failover using the gcloud CLI. Measure the exact failover duration and verify that the standby VM in Zone B assumes the primary read-write role:</p>
<pre><code># Record current primary zone:
echo "=== PRE-FAILOVER STATUS ==="
gcloud sql instances describe ${INSTANCE_NAME} \
    --project=${PROJECT_ID} \
    --format="table(name, gceZone, secondaryGceZone, state)"

# Trigger manual failover switchover drill:
echo "Triggering Cloud SQL Regional HA failover drill..."
gcloud sql instances failover ${INSTANCE_NAME} \
    --project=${PROJECT_ID} \
    --quiet

# Monitor failover completion and verify active zone swap:
echo "=== POST-FAILOVER STATUS ==="
gcloud sql instances describe ${INSTANCE_NAME} \
    --project=${PROJECT_ID} \
    --format="table(name, gceZone, secondaryGceZone, state)"</code></pre>
</li>

<li><strong>Test Automated Point-in-Time Recovery (PITR) WAL Rollback:</strong>
<p>Demonstrate down-to-the-second disaster recovery. Record a timestamp, simulate an accidental data corruption event (such as dropping an inventory table), and clone the database instance to the exact second prior to the corruption:</p>
<pre><code># 1. Record the baseline timestamp before corruption:
TARGET_RESTORE_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")
echo "Captured baseline PITR target timestamp: ${TARGET_RESTORE_TIME}"

# 2. Simulate accidental data loss or corruption event in application database:
echo "Simulating table drop event occurring 10 seconds later..."

# 3. Clone instance to exact microsecond before the corruption:
gcloud sql instances clone ${INSTANCE_NAME} ${RESTORE_INSTANCE} \
    --project=${PROJECT_ID} \
    --point-in-time="${TARGET_RESTORE_TIME}"

# 4. Verify cloned instance operational readiness:
gcloud sql instances describe ${RESTORE_INSTANCE} \
    --project=${PROJECT_ID} \
    --format="table(name, gceZone, databaseVersion, state)"</code></pre>
</li>
</ol>

<div class="callout success">
<strong>Expected result / acceptance</strong>
<p>The Cloud SQL Regional HA instance is provisioned with Private Service Connect, exposing a private <code>/32</code> endpoint inside the consumer VPC without VPC peering quotas. PgBouncer multiplexes client traffic into 32 backend sockets. A manual failover drill swaps the primary zone from Zone A to Zone B within 60 to 120 seconds with RPO = 0, and PITR cloning restores data to the exact target timestamp prior to corruption.</p>
</div>

<div class="callout caution">
<strong>Troubleshooting</strong>
<p>If the PSC Forwarding Rule remains in <code>PENDING</code> status, verify that the consumer project ID is explicitly listed in <code>--allowed-psc-projects</code> on the Cloud SQL instance. If PgBouncer returns <code>ERROR: prepared statement does not exist</code>, confirm whether your client ORM is emitting unnamed prepared statements; in PgBouncer 1.21+, configure <code>max_prepared_statements = 100</code> to support server-side statement preparation under transaction pooling.</p>
</div>

<div class="callout">
<strong>Cleanup and cost</strong>
<p>Cloud SQL Regional HA instances incur hourly compute and Regional PD storage charges. To prevent unexpected costs after completing the exercise, terminate the restored clone and primary instance:</p>
<pre><code>gcloud sql instances delete ${RESTORE_INSTANCE} --project=${PROJECT_ID} --quiet
gcloud sql instances delete ${INSTANCE_NAME} --project=${PROJECT_ID} --quiet
gcloud compute forwarding-rules delete ${FORWARDING_RULE} --region=${REGION} --project=${PROJECT_ID} --quiet
gcloud compute addresses delete psc-sql-address --region=${REGION} --project=${PROJECT_ID} --quiet</code></pre>
</div>
<label class="check"><input type="checkbox" data-progress="lab-61-topic-01"> I completed and checked this topic exercise</label>
</article>

<article id="topic-02-lab" class="topic-card lab">
<h3>Exercise 2: Compare AlloyDB compatibility/read pools at selection depth</h3>
<p><strong>Goal:</strong> Deep-dive transactional concurrency, demonstrate isolation anomalies (Non-Repeatable Reads and Write Skew), induce deterministic multi-row deadlocks (<code>SQLSTATE 40P01</code>), and implement a production-grade idempotent retry loop with exponential backoff and full randomized jitter in Python.</p>
<p><strong>Mode:</strong> local exercise &amp; production sandbox &middot; <strong>Prerequisite:</strong> <a href="day-060.html">Day 60</a>, <a href="day-016.html">Day 16</a>; bring their exit artifacts.</p>

<ol>
<li><strong>Initialize Local Multi-Worker Concurrency Test Fixture:</strong>
<p>Execute a standalone Python test script that models transactional concurrency, row-level locks, and state machines without requiring an external cloud database cluster:</p>
<pre><code>python3 -c '
import sqlite3
import os

DB_FILE = "/tmp/brightloaf_inventory.db"
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Create transactional inventory table with non-negative balance check:
cur.execute('''
CREATE TABLE inventory (
    sku TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0),
    version_id INTEGER NOT NULL DEFAULT 1
);
''')

# Create idempotency ledger table:
cur.execute('''
CREATE TABLE idempotency_records (
    idempotency_key TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

# Populate test inventory:
cur.execute("INSERT INTO inventory (sku, description, stock_quantity) VALUES (\x27SOURDOUGH-01\x27, \x27Artisan Sourdough Loaf\x27, 10);")
cur.execute("INSERT INTO inventory (sku, description, stock_quantity) VALUES (\x27BRIOCHE-02\x27, \x27Golden Brioche Buns (4pk)\x27, 10);")
cur.execute("INSERT INTO inventory (sku, description, stock_quantity) VALUES (\x27CROISSANT-03\x27, \x27Butter Croissants (2pk)\x27, 10);")

conn.commit()
conn.close()
print("Initialized transactional inventory database at", DB_FILE)
'</code></pre>
</li>

<li><strong>Simulate Concurrency Isolation Anomalies: Non-Repeatable Read &amp; Write Skew:</strong>
<p>Run a Python script demonstrating how concurrent uncommitted and committed modifications produce Non-Repeatable Reads under standard Read Committed isolation, and contrast with Repeatable Read snapshot isolation:</p>
<pre><code>python3 -c '
import sqlite3
import time
import threading

DB_FILE = "/tmp/brightloaf_inventory.db"

def worker_reader():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    cur = conn.cursor()
    # Read Committed behavior: Query 1
    cur.execute("SELECT stock_quantity FROM inventory WHERE sku = \x27SOURDOUGH-01\x27")
    q1 = cur.fetchone()[0]
    print(f"[Reader Thread] Query 1 observed stock: {q1}")
    time.sleep(0.5)
    # Query 2 after concurrent update
    cur.execute("SELECT stock_quantity FROM inventory WHERE sku = \x27SOURDOUGH-01\x27")
    q2 = cur.fetchone()[0]
    print(f"[Reader Thread] Query 2 observed stock: {q2}")
    if q1 != q2:
        print("[ANOMALY CONFIRMED] Non-Repeatable Read detected: Stock changed within session!")
    conn.close()

def worker_writer():
    time.sleep(0.2)
    conn = sqlite3.connect(DB_FILE, timeout=10)
    cur = conn.cursor()
    cur.execute("UPDATE inventory SET stock_quantity = stock_quantity - 3 WHERE sku = \x27SOURDOUGH-01\x27")
    conn.commit()
    print("[Writer Thread] Committed stock decrement (-3)")
    conn.close()

t1 = threading.Thread(target=worker_reader)
t2 = threading.Thread(target=worker_writer)
t1.start()
t2.start()
t1.join()
t2.join()
'</code></pre>
</li>

<li><strong>Induce and Detect Deterministic Multi-Transaction Deadlocks:</strong>
<p>Run two concurrent transactional threads locking items in opposing sequences (Thread 1: Sourdough &rarr; Brioche; Thread 2: Brioche &rarr; Sourdough) to demonstrate circular wait-for deadlock induction:</p>
<pre><code>python3 -c '
import sqlite3
import time
import threading

DB_FILE = "/tmp/brightloaf_inventory.db"
deadlocks_caught = 0

def transaction_alpha():
    global deadlocks_caught
    conn = sqlite3.connect(DB_FILE, timeout=0.5, isolation_level="EXCLUSIVE")
    try:
        cur = conn.cursor()
        print("[Tx Alpha] Acquired exclusive database lock. Processing SOURDOUGH...")
        cur.execute("UPDATE inventory SET stock_quantity = stock_quantity - 1 WHERE sku = \x27SOURDOUGH-01\x27")
        time.sleep(0.4)
        print("[Tx Alpha] Attempting to update BRIOCHE...")
        cur.execute("UPDATE inventory SET stock_quantity = stock_quantity - 1 WHERE sku = \x27BRIOCHE-02\x27")
        conn.commit()
        print("[Tx Alpha] Success!")
    except sqlite3.OperationalError as e:
        print(f"[Tx Alpha BLOCKED / DEADLOCK]: {e}")
        deadlocks_caught += 1
    finally:
        conn.close()

def transaction_beta():
    global deadlocks_caught
    time.sleep(0.1)
    conn = sqlite3.connect(DB_FILE, timeout=0.5, isolation_level="EXCLUSIVE")
    try:
        cur = conn.cursor()
        print("[Tx Beta] Attempting exclusive database lock...")
        cur.execute("UPDATE inventory SET stock_quantity = stock_quantity - 1 WHERE sku = \x27BRIOCHE-02\x27")
        conn.commit()
        print("[Tx Beta] Success!")
    except sqlite3.OperationalError as e:
        print(f"[Tx Beta BLOCKED / DEADLOCK]: {e}")
        deadlocks_caught += 1
    finally:
        conn.close()

t_a = threading.Thread(target=transaction_alpha)
t_b = threading.Thread(target=transaction_beta)
t_a.start()
t_b.start()
t_a.join()
t_b.join()
print(f"Total concurrent lock conflict / deadlock aborts intercepted: {deadlocks_caught}")
'</code></pre>
</li>

<li><strong>Implement Production Idempotent Retry Wrapper with Exponential Jitter:</strong>
<p>Author a production Python retry wrapper that intercepts concurrency collisions (<code>40001</code> / <code>40P01</code>), enforces client request idempotency, and retries with full randomized jitter:</p>
<pre><code>python3 -c '
import random
import time
import uuid

class SerializationFailure(Exception):
    # Corresponds to PostgreSQL SQLSTATE 40001
    pass

class DeadlockDetected(Exception):
    # Corresponds to PostgreSQL SQLSTATE 40P01
    pass

def execute_idempotent_transaction(idempotency_key, operation_func, max_retries=5, base_backoff=0.05, max_backoff=1.0):
    processed_keys = set()
    attempt = 0
    
    while attempt &lt; max_retries:
        attempt += 1
        try:
            print(f"[Attempt {attempt}] Validating idempotency key: {idempotency_key}...")
            if idempotency_key in processed_keys:
                print(f"[IDEMPOTENT HIT] Transaction {idempotency_key} was already committed. Returning cached receipt.")
                return {"status": "SUCCESS", "cached": True, "attempts": attempt}
            
            # Execute business operation (simulating rare transient concurrency collisions):
            if attempt &lt; 3:
                # Simulate transient 40001 serialization collision
                raise SerializationFailure("could not serialize access due to concurrent update (SQLSTATE 40001)")
            
            # Commit operation:
            processed_keys.add(idempotency_key)
            print(f"[SUCCESS] Transaction {idempotency_key} committed on attempt {attempt}.")
            return {"status": "SUCCESS", "cached": False, "attempts": attempt}
            
        except (SerializationFailure, DeadlockDetected) as ex:
            if attempt &gt;= max_retries:
                print(f"[FATAL] Exhausted {max_retries} attempts. Raising error.")
                raise ex
            
            # Full Jitter backoff formula: t = random.uniform(0, min(max_backoff, base * 2^attempt))
            sleep_duration = random.uniform(0, min(max_backoff, base_backoff * (2 ** attempt)))
            print(f"[RETRYABLE CONFLICT]: {ex}")
            print(f"Applying full jitter sleep: {sleep_duration*1000:.1f}ms before attempt {attempt+1}")
            time.sleep(sleep_duration)

# Execute test with synthetic client idempotency key:
test_key = str(uuid.uuid4())
result = execute_idempotent_transaction(test_key, lambda: None)
print("Final Execution Result:", result)
'</code></pre>
</li>

<li><strong>Verify Deterministic Resource Ordering Invariant:</strong>
<p>Validate that sorting multi-item SKU arrays in ascending alphabetical order before requesting row locks eliminates circular wait graphs:</p>
<pre><code>python3 -c '
# Test deterministic resource sorting logic for multi-item cart:
incoming_cart_items = ["SOURDOUGH-01", "BRIOCHE-02", "CROISSANT-03", "BAGUETTE-04"]

# Step 1: Ensure deterministic ascending sort order:
sorted_items = sorted(incoming_cart_items)
print("Incoming cart order:   ", incoming_cart_items)
print("Deterministic lock order:", sorted_items)

# Verify invariant:
assert sorted_items == ["BAGUETTE-04", "BRIOCHE-02", "CROISSANT-03", "SOURDOUGH-01"]
print("INVARIANT VERIFIED: All transactions acquire row locks in strict alphabetical sequence.")
'</code></pre>
</li>
</ol>

<div class="callout success">
<strong>Expected result / acceptance</strong>
<p>The Python concurrency scripts demonstrate Non-Repeatable Reads under default Read Committed isolation, reproduce circular wait deadlocks when locks are acquired without consistent ordering, and prove that deterministic sorting (<code>ORDER BY sku ASC</code>) combined with an idempotent retry wrapper (handling <code>40001</code> and <code>40P01</code>) achieves 100% transaction completion without deadlocks or duplicate order fulfillment.</p>
</div>

<div class="callout caution">
<strong>Troubleshooting</strong>
<p>If transactions repeatedly exhaust their retry ceiling under high concurrency, inspect the base backoff and jitter configuration. A fixed delay causes retrying threads to collide repeatedly in lock-step resonance; verify that your backoff formula utilizes <code>random.uniform(0, ...)</code> to introduce complete phase decorrelation.</p>
</div>

<div class="callout">
<strong>Cleanup and cost</strong>
<p>The local test database was created in temporary storage. Remove the temporary test files:</p>
<pre><code>rm -f /tmp/brightloaf_inventory.db /tmp/pgbouncer.ini</code></pre>
</div>
<label class="check"><input type="checkbox" data-progress="lab-61-topic-02"> I completed and checked this topic exercise</label>
</article>
</section>"""
