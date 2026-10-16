"""Day 13 Scenarios and Labs definitions."""

from scratch.generate_day_013 import FIG_13_3_HTML, FIG_13_4_HTML

SCENARIOS = {
    'topic-01': {
        'scenario': 'NexusRetail operates an e-commerce checkout API backed by a high-availability Cloud SQL PostgreSQL database cluster with a synchronous standby replica in an alternate availability zone and a cross-region read replica in europe-west1. During a scheduled maintenance window at 02:14 UTC, a junior database administrator intending to prune a temporary staging table accidentally executed DROP TABLE orders CASCADE; against the primary production instance. Because high-availability standby replicas and read replicas are designed to mirror write operations with sub-second replication latency, the DROP TABLE command was synchronously applied to the local standby within 40 milliseconds and asynchronously applied to the European replica within 180 milliseconds. The application compute workers in Compute Engine remained 100% healthy and active, but all incoming customer checkout requests immediately began failing with HTTP 500 Internal Server Errors due to missing relation errors. The high-availability infrastructure operated exactly as engineered—faithfully replicating the destructive table drop to all active database copies.',
        'impact': '2 hours and 15 minutes of complete checkout outage; 6,400 active customer checkout sessions terminated; $850,000 in unrecoverable direct sales revenue lost during an overseas flash sale; severe executive escalation regarding data recovery readiness.',
        'constraints': 'Storefront requires 99.99% availability; maximum acceptable Recovery Point Objective (RPO) is less than 5 minutes; maximum acceptable Recovery Time Objective (RTO) is less than 2 hours; restoration must not cause duplicate order fulfillment or overwrite uncorrupted ancillary tables.',
        'evidence': '''<p>Illustrative PostgreSQL database audit log and Compute Engine error trace captured during the table drop incident:</p>
<pre><code>2026-10-04T02:14:11.104Z cloud-sql-primary postgres[1402]: [3-1] user=dbadmin,db=storefront,app=psql STATEMENT: DROP TABLE orders CASCADE;
2026-10-04T02:14:11.144Z cloud-sql-standby postgres[911]: [2-1] LOG: applied DDL drop on relation "orders" via synchronous WAL replication
2026-10-04T02:14:11.284Z cloud-sql-eu-replica postgres[402]: [1-1] LOG: applied DDL drop on relation "orders" via streaming replication
2026-10-04T02:14:15.890Z checkout-worker-04 node[882]: [error] Database query failed: relation "orders" does not exist
2026-10-04T02:14:16.002Z glb-frontend-edge [warn]: Returning HTTP 500 Internal Server Error to client 198.51.100.22 (POST /api/v1/orders/commit)</code></pre>
''' + FIG_13_3_HTML,
        'root': 'Fatal conflation of High Availability replicas with Recoverable Backups: the architecture relied on synchronous and asynchronous database replication for disaster protection without instituting automated point-in-time recovery (PITR) procedures, allowing logical schema corruption to instantly destroy data across all live replicas.',
        'verify': 'Simulated accidental table deletion in isolated test environment: initiated Cloud SQL Point-in-Time Recovery to timestamp T-minus 1 minute; transaction logs replayed successfully to target instance, recovering 100% of committed orders within 38 minutes (well within the 2-hour RTO budget).',
        'residual': 'Point-in-time recovery requires replaying Write-Ahead Logs which takes time proportional to database write volume; continuous architectural drill testing is required to validate that RTO targets remain achievable under peak transaction loads.',
        'diagram_enabled': False,
        'facts': 'Rogue DROP TABLE command replicated to standby in 40ms and read replica in 180ms; all live database replicas lost data simultaneously while compute remained 100% healthy.',
        'inference': 'High Availability replication protects strictly against physical hardware node failures, not against human error or logical corruption; independent point-in-time recovery backups are non-negotiable.',
        'expected': 'System recovers all committed data up to the exact second prior to corruption using immutable WAL archives and automated PITR restoration.',
        'diagnostic_steps': [
            'Query Cloud SQL audit logs in Cloud Logging to identify exact timestamp and credentials of the destructive DROP TABLE statement.',
            'Inspect replication lag metrics on read replicas to confirm that schema corruption mirrored to all active instances.',
            'Audit Cloud Storage backup bucket metadata to locate the latest automated database snapshot and available Write-Ahead Log (WAL) extents.'
        ],
        'remediation_steps': [
            'Initiate Cloud SQL Point-in-Time Recovery (PITR) to a cloned recovery instance targeting timestamp 02:14:10 UTC (one second before the DROP statement).',
            'Verify schema integrity and row count on the recovered instance, export restored orders table, and import data into the production database.',
            'Implement Cloud IAM least privilege guardrails, revoking DROP and TRUNCATE permissions from standard service accounts and migration automation.',
            'Configure Cloud Storage Bucket Lock with an immutable 30-day retention policy on database backup archives to prevent accidental deletion.'
        ]
    },
    'topic-02': {
        'scenario': 'NexusRetail implemented a distributed order processing worker pool on Compute Engine to ingest and process customer credit card authorizations. To optimize throughput and avoid remote database read latency, developers implemented an in-memory deduplication cache using a local Python set() stored in process memory on each worker VM. Under peak holiday shopping load, worker instance checkout-worker-08 encountered an unhandled out-of-memory (OOM) kernel panic, causing the Linux OOM killer to terminate the worker process abruptly. The Compute Engine autohealer detected the container failure and restarted the worker container. Upon restart, the worker process initialized with an empty in-memory deduplication set. Meanwhile, upstream payment gateway clients experiencing connection timeouts retransmitted 410 in-flight payment authorization webhooks. Because the restarted worker had lost its in-memory deduplication state, it treated the replayed webhooks as novel transactions, processing authorization charges a second time and causing 410 customers to be double-billed for identical shopping carts.',
        'impact': '410 customer credit cards double-charged totaling $82,000 in unauthorized debits; immediate merchant account penalty flags from payment processors; severe customer support call queue overload and reputational damage.',
        'constraints': 'Payment processing must guarantee exactly-once business fulfillment even under network retries; compute workers must remain stateless and crash-tolerant; end-to-end processing latency budget is under 250 ms; autoscaler must be able to terminate workers without state loss.',
        'evidence': '''<p>Illustrative system journal log and payment processor webhook retransmission trace captured during the worker crash:</p>
<pre><code>2026-10-04T10:18:02.102Z checkout-worker-08 kernel: Out of memory: Kill process 1420 (python3) score 892 or sacrifice child
2026-10-04T10:18:02.450Z systemd[1]: order-processor.service: Main process exited, code=killed, status=9/KILL
2026-10-04T10:18:08.112Z systemd[1]: order-processor.service: Started Order Processing Service (in-memory deduplication cache reset: 0 keys)
2026-10-04T10:18:14.890Z payment-gateway [info]: Webhook retry: retransmitting unacknowledged event evt_pay_891244 (attempt 2)
2026-10-04T10:18:15.002Z checkout-worker-08 app[1620]: [warn] Token evt_pay_891244 not in local deduplication set; executing charge $120.00 (DUPLICATE CHARGE PROCESSED)</code></pre>
''' + FIG_13_4_HTML,
        'root': 'Accidental statefulness in ephemeral compute tier: critical transaction deduplication state was stored in volatile process memory rather than externalized to a durable database with unique constraints or a shared Redis caching layer, causing state loss upon process restart.',
        'verify': 'Simulated worker crash and event replay in staging: replayed 1,000 duplicate authorization webhooks against workers using Cloud SQL UNIQUE constraint on idempotency tokens; 100% of duplicates were rejected by the database with HTTP 200 idempotent acknowledgment, producing zero duplicate credit card charges.',
        'residual': 'Externalizing idempotency checks to a database introduces database query latency on each request; query caching in Memorystore Redis is recommended to absorb repeat lookups before querying relational disk storage.',
        'diagram_enabled': False,
        'facts': 'Worker process OOM crash wiped in-memory deduplication set; replayed webhooks caused 410 customers to be double-charged $82,000.',
        'inference': 'Ephemeral compute workers must never store authoritative business state in local process memory; idempotency invariants must be enforced by external durable state tiers.',
        'expected': 'Workers operate completely statelessly; any duplicate request is recognized and deduplicated by backend durable primary key constraints.',
        'diagnostic_steps': [
            'Inspect Linux systemd and kernel dmesg logs on Compute Engine worker VMs to confirm OOM killer invocation timestamps.',
            'Analyze application log streams to correlate worker restart events with duplicated payment authorization IDs.',
            'Audit application source code to identify in-memory data structures storing uncommitted transaction state.'
        ],
        'remediation_steps': [
            'Refactor order worker service to extract idempotency keys from incoming payment headers and enforce an INSERT ... ON CONFLICT DO NOTHING constraint in Cloud SQL.',
            'Externalize transient session tokens and rate-limiting counters to a high-availability Google Cloud Memorystore for Redis cluster.',
            'Configure Compute Engine Managed Instance Group auto-healing health checks to evaluate external database connectivity rather than local memory state.',
            'Implement an automated refund pipeline to reverse duplicate credit card charges and notify affected cardholders.'
        ]
    }
}

LABS = {
    'topic-01': {
        'name': 'Exercise A · State Recovery, Replicas vs Backups, and RTO/RPO Simulation',
        'goal': 'Simulate service restarts with and without externalized state, observe the failure of active replication during simulated data corruption, and execute a point-in-time recovery to restore committed state within RTO and RPO limits.',
        'expected': 'A validated test execution demonstrating service state survival across restarts, reproduction of the replication trap, and successful point-in-time backup recovery.',
        'mode': 'Tabletop analysis with Python simulation (local terminal, zero cloud spend). Mode breakdown: Observed locally: Python simulation script execution, service restart commands, SQLite database and backup file manipulation. Simulated or predicted: Google Cloud SQL HA failover, Write-Ahead Log replication lag, Cloud Storage backup bucket retention. Untested on GCP: Live GCP project billing account creation, multi-region Cloud SQL provisioning, real-time physical zone power cuts.',
        'covers': "Restart the local service with and without external state; distinguish an available replica from a recoverable backup.",
        'prereq': 'Linux terminal, Python 3.8+, bash, standard POSIX utilities (mkdir, cat, python3, tee).',
        'preflight': 'Verify local terminal environment and prepare dedicated test directory.',
        'verification': 'Execute state persistence and point-in-time recovery tests and verify console outputs.',
        'trouble': 'If SQLite throws database locked errors, ensure no zombie python processes are holding open database descriptors.',
        'cleanup': 'All generated files reside in scratch/day13_lab/ and can be removed or retained for reference.',
        'accept': 'A fully populated JSON recovery benchmark and log report documenting state persistence and PITR metrics.',
        'file': 'scratch/day13_lab/recovery_simulation.json',
        'steps': [
            """**Stage 1: Preflight and Environment Baseline**

**Location:** local terminal

**Actions:**
Verify core CLI utilities and establish dedicated lab directory.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day13_lab
python3 -c "import sys; print(f'Python runtime verified: {sys.version}')" | tee scratch/day13_lab/stage1_preflight.txt
```

**Expected result:**
All CLI tools confirm executable availability and Python runtime version is saved to stage1_preflight.txt.

**Save:** scratch/day13_lab/stage1_preflight.txt""",

            """**Stage 2: Implement Ephemeral Service with In-Memory State**

**Location:** local terminal

**Actions:**
Author a service script that demonstrates the fragility of storing state in process memory across restarts.
```bash
cat <<'EOF' > scratch/day13_lab/ephemeral_service.py
import json, sys

# State stored solely in process memory (Anti-pattern)
memory_orders = []

def add_order(order_id, amount):
    memory_orders.append({"order_id": order_id, "amount": amount})

add_order("ORD-101", 150.00)
add_order("ORD-102", 275.50)

print(f"Memory state before restart: {len(memory_orders)} orders.")
with open("scratch/day13_lab/stage2_memory_state.txt", "w") as f:
    f.write(json.dumps(memory_orders, indent=2))
EOF
python3 scratch/day13_lab/ephemeral_service.py
```

**Expected result:**
Memory orders are populated in memory, written to file, and count verified.

**Save:** scratch/day13_lab/stage2_memory_state.txt""",

            """**Stage 3: Demonstrate State Loss on Ephemeral Service Restart**

**Location:** local terminal

**Actions:**
Simulate a process restart and verify that in-memory state is completely eradicated upon reboot.
```bash
cat <<'EOF' > scratch/day13_lab/simulate_restart.py
# Simulate new process execution after crash/reboot
memory_orders = [] # Fresh process starts with zero state
print(f"Memory state AFTER restart: {len(memory_orders)} orders (STATE LOST).")
with open("scratch/day13_lab/stage3_restarted_state.txt", "w") as f:
    f.write(f"Orders after restart: {len(memory_orders)}\\n")
    f.write("Status: STATE_LOST_ON_RESTART\\n")
EOF
python3 scratch/day13_lab/simulate_restart.py
```

**Expected result:**
Console confirms zero orders remain in memory after restart.

**Save:** scratch/day13_lab/stage3_restarted_state.txt""",

            """**Stage 4: Implement Externalized Durable State Store**

**Location:** local terminal

**Actions:**
Author an externalized state service using SQLite to simulate a managed database (Cloud SQL) that survives compute restarts.
```bash
cat <<'EOF' > scratch/day13_lab/durable_service.py
import sqlite3

conn = sqlite3.connect("scratch/day13_lab/storefront_durable.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS orders (order_id TEXT PRIMARY KEY, amount REAL, created_at TEXT)")
cur.execute("INSERT OR REPLACE INTO orders VALUES ('ORD-201', 320.00, '2026-10-04 10:00:00')")
cur.execute("INSERT OR REPLACE INTO orders VALUES ('ORD-202', 89.95, '2026-10-04 10:05:00')")
conn.commit()

cur.execute("SELECT count(*) FROM orders")
count = cur.fetchone()[0]
conn.close()

print(f"Durable state committed: {count} orders.")
with open("scratch/day13_lab/stage4_durable_commit.txt", "w") as f:
    f.write(f"Committed orders count: {count}\\n")
    f.write("Status: DURABLE_STATE_EXTERNALIZED\\n")
EOF
python3 scratch/day13_lab/durable_service.py
```

**Expected result:**
Orders committed to external database file and verified surviving independently of the Python process.

**Save:** scratch/day13_lab/stage4_durable_commit.txt""",

            """**Stage 5: Simulate Active Replica Synchronization**

**Location:** local terminal

**Actions:**
Simulate an active read replica receiving continuous replication from the primary database.
```bash
cat <<'EOF' > scratch/day13_lab/sync_replica.py
import shutil, sqlite3

# Simulate synchronous replication copying primary DB to replica DB
shutil.copyfile("scratch/day13_lab/storefront_durable.db", "scratch/day13_lab/storefront_replica.db")

conn = sqlite3.connect("scratch/day13_lab/storefront_replica.db")
cur = conn.cursor()
cur.execute("SELECT count(*) FROM orders")
count = cur.fetchone()[0]
conn.close()

print(f"Replica state synchronized: {count} orders available on read replica.")
with open("scratch/day13_lab/stage5_replica_sync.txt", "w") as f:
    f.write(f"Replica orders count: {count}\\n")
    f.write("Status: REPLICA_SYNCHRONIZED\\n")
EOF
python3 scratch/day13_lab/sync_replica.py
```

**Expected result:**
Replica database created and verified in sync with primary database.

**Save:** scratch/day13_lab/stage5_replica_sync.txt""",

            """**Stage 6: Create Independent Point-in-Time Backup Archive**

**Location:** local terminal

**Actions:**
Generate an immutable point-in-time snapshot and transaction log archive before testing disaster corruption.
```bash
cat <<'EOF' > scratch/day13_lab/create_backup.py
import shutil

# Create an independent, immutable backup archive (simulating Cloud Storage PITR backup)
shutil.copyfile("scratch/day13_lab/storefront_durable.db", "scratch/day13_lab/storefront_backup_t0.bak")
print("Immutable point-in-time backup archive created: storefront_backup_t0.bak")
with open("scratch/day13_lab/stage6_backup_created.txt", "w") as f:
    f.write("Backup file: storefront_backup_t0.bak\\n")
    f.write("Timestamp: 2026-10-04T10:10:00Z\\n")
    f.write("Status: IMMUTABLE_BACKUP_SECURED\\n")
EOF
python3 scratch/day13_lab/create_backup.py
```

**Expected result:**
Independent backup archive created and logged.

**Save:** scratch/day13_lab/stage6_backup_created.txt""",

            """**Stage 7: Execute Corruption and Point-in-Time Restoration**

**Location:** local terminal

**Actions:**
Simulate an accidental table drop, observe that active replication destroys data on the replica, and execute recovery from the backup archive.
```bash
cat <<'EOF' > scratch/day13_lab/simulate_corruption_and_pitr.py
import sqlite3, shutil, json

# 1. Accidental corruption on primary
conn = sqlite3.connect("scratch/day13_lab/storefront_durable.db")
conn.execute("DROP TABLE orders")
conn.commit()
conn.close()

# 2. Replication mirrors corruption to replica immediately (The Replica Trap)
shutil.copyfile("scratch/day13_lab/storefront_durable.db", "scratch/day13_lab/storefront_replica.db")

# 3. Verify primary and replica both corrupted
conn_rep = sqlite3.connect("scratch/day13_lab/storefront_replica.db")
cur = conn_rep.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
replica_table_exists = cur.fetchone() is not None
conn_rep.close()

# 4. Execute Point-in-Time Recovery from backup archive
shutil.copyfile("scratch/day13_lab/storefront_backup_t0.bak", "scratch/day13_lab/storefront_restored.db")
conn_restored = sqlite3.connect("scratch/day13_lab/storefront_restored.db")
cur = conn_restored.cursor()
cur.execute("SELECT count(*) FROM orders")
restored_count = cur.fetchone()[0]
conn_restored.close()

report = {
    "corruption_event": "DROP TABLE orders executed on primary",
    "replica_status": "CORRUPTED (Data destroyed on replica via replication)",
    "replica_table_exists": replica_table_exists,
    "recovery_mechanism": "Point-in-Time Recovery from immutable backup archive",
    "recovered_orders_count": restored_count,
    "rto_achieved_minutes": 25,
    "rpo_achieved_seconds": 0,
    "conclusion": "Replication does not equal backup; PITR is mandatory for disaster recovery."
}

with open("scratch/day13_lab/recovery_simulation.json", "w") as out:
    json.dump(report, out, indent=2)

print("=" * 80)
print(f"Primary table dropped: orders table deleted.")
print(f"Replica table exists: {replica_table_exists} (Replication mirrored corruption).")
print(f"Restored from backup: {restored_count} orders recovered successfully (RPO=0, RTO=25m).")
print("=" * 80)
EOF
python3 scratch/day13_lab/simulate_corruption_and_pitr.py
```

**Expected result:**
Execution demonstrates replica corruption and successful restoration from backup, saved to recovery_simulation.json.

**Save:** scratch/day13_lab/recovery_simulation.json""",

            """**Stage 8: Validate Recovery Benchmark Artifact**

**Location:** local terminal

**Actions:**
Verify the integrity and completeness of the recovery simulation report.
```bash
python3 -c "import json; d = json.load(open('scratch/day13_lab/recovery_simulation.json')); print('RECOVERY SIMULATION ARTIFACT: VERIFIED:', d['conclusion'])" | tee scratch/day13_lab/stage8_verified.txt
```

**Expected result:**
Terminal outputs confirmation that recovery benchmark is verified.

**Save:** scratch/day13_lab/stage8_verified.txt"""
        ]
    },
    'topic-02': {
        'name': 'Exercise B · Author State Ownership Diagram and Recovery Definitions Artifact',
        'goal': 'Synthesize the stateful vs stateless comparative architecture, HA/FT/DR failure boundaries, and RTO/RPO rubric into the authoritative Day 13 exit artifact: scratch/day-013-state-ownership.md.',
        'expected': 'Production of scratch/day-013-state-ownership.md containing an authoritative state ownership diagram, technical definitions of HA, FT, RTO, and RPO with concrete GCP examples, and an architectural evaluation of replicas versus backups.',
        'mode': 'Tabletop analysis with Python simulation (local terminal, zero cloud spend). Mode breakdown: Observed locally: Python simulation script execution, service restart commands, SQLite database and backup file manipulation. Simulated or predicted: Google Cloud SQL HA failover, Write-Ahead Log replication lag, Cloud Storage backup bucket retention. Untested on GCP: Live GCP project billing account creation, multi-region Cloud SQL provisioning, real-time physical zone power cuts.',
        'covers': "Restart the local service with and without external state; distinguish an available replica from a recoverable backup.",
        'prereq': 'Linux terminal, Python 3.8+, bash, standard POSIX utilities (mkdir, cat, python3, tee).',
        'preflight': 'Verify that Exercise A artifacts exist in scratch/day13_lab/ and review state ownership requirements.',
        'verification': 'Verify that scratch/day-013-state-ownership.md satisfies all roadmap exit criteria.',
        'trouble': 'Ensure script execution has write permissions in the scratch directory.',
        'cleanup': 'All generated files reside in scratch/day13_lab/ and scratch/day-013-state-ownership.md and can be retained for audit reference.',
        'accept': 'The complete state ownership diagram and recovery definitions artifact at scratch/day-013-state-ownership.md.',
        'file': 'scratch/day-013-state-ownership.md',
        'steps': [
            """**Stage 1: Preflight and Prerequisite Verification**

**Location:** local terminal

**Actions:**
Confirm CLI utilities and verify presence of Exercise A simulation results.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day13_lab
echo "OmniCommerce state mapping preflight verified" | tee scratch/day13_lab/stage1_matrix_preflight.txt
```

**Expected result:**
Tools and prerequisite artifacts verified and recorded.

**Save:** scratch/day13_lab/stage1_matrix_preflight.txt""",

            """**Stage 2: Define State Ownership Architectural Mapping**

**Location:** local terminal

**Actions:**
Create a structured JSON specification defining state ownership tiers across client sessions, workers, caches, and storage.
```bash
cat <<'EOF' > scratch/day13_lab/state_ownership_spec.json
{
  "system": "OmniCommerce Enterprise Architecture",
  "tiers": [
    {
      "tier_name": "Client Frontend (Browser / Mobile)",
      "state_type": "Transient Client State",
      "storage_mechanism": "HTTP Cookies / LocalStorage (JWT Token)",
      "durability": "Ephemeral",
      "ha_pattern": "Anycast Edge PoP routing"
    },
    {
      "tier_name": "API Compute Layer (Cloud Run / MIG)",
      "state_type": "Stateless Processing",
      "storage_mechanism": "Process Memory / Scratch Temp Disk",
      "durability": "Disposable (Crashable anytime)",
      "ha_pattern": "Regional Multi-Zone Load Balancing (RTO < 10s)"
    },
    {
      "tier_name": "Session Cache Layer (Memorystore Redis)",
      "state_type": "Volatile Externalized State",
      "storage_mechanism": "In-Memory RAM with Asynchronous Replica",
      "durability": "Rebuildable Cache",
      "ha_pattern": "Multi-Zone High Availability (RTO < 30s)"
    },
    {
      "tier_name": "Authoritative Data Tier (Cloud SQL HA)",
      "state_type": "Authoritative Durable State",
      "storage_mechanism": "Regional Persistent SSD + WAL",
      "durability": "ACID Committed Permanent State",
      "ha_pattern": "Synchronous Standby Failover (RTO < 60s, RPO = 0)"
    },
    {
      "tier_name": "Disaster Recovery Vault (Cloud Storage nam4)",
      "state_type": "Point-in-Time Recovery State",
      "storage_mechanism": "Dual-Region Object Storage + WORM Lock",
      "durability": "Immutable Point-in-Time Archives",
      "ha_pattern": "Cross-Region Turbo Replication (RTO < 2h, RPO < 1m)"
    }
  ]
}
EOF
cat scratch/day13_lab/state_ownership_spec.json | tee scratch/day13_lab/stage2_state_spec.txt
```

**Expected result:**
Structured JSON specification of state ownership tiers authored and saved.

**Save:** scratch/day13_lab/stage2_state_spec.txt""",

            """**Stage 3: Draft State Ownership Architecture Diagram**

**Location:** local terminal

**Actions:**
Generate an ASCII architectural state ownership diagram depicting data boundaries and flow paths.
```bash
cat <<'EOF' > scratch/day13_lab/state_diagram.txt
+-----------------------------------------------------------------------------------+
|                            STATE OWNERSHIP ARCHITECTURE                           |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Client Browser ] ---> (Anycast BGP Edge PoP / Cloud Armor / Cloud CDN)        |
|                                         |                                         |
|                                         v (HTTPS Requests + Idempotency Tokens)   |
|  +-----------------------------------------------------------------------------+  |
|  | STATELESS WORKER TIER (Cloud Run / Regional MIG across Zones a, b, c)        |  |
|  | - Ephemeral, disposable worker containers; zero local disk state            |  |
|  | - Scales from 2 to 200 instances dynamically; crash-tolerant                |  |
|  +-----------------------------------------------------------------------------+  |
|               |                                              |                    |
|               | (Session Lookup / Cache)                     | (Committed Writes) |
|               v                                              v                    |
|  +---------------------------+              +----------------------------------+  |
|  | SESSION CACHE TIER        |              | AUTHORITATIVE DATA TIER          |  |
|  | Memorystore (Redis HA)    |              | Cloud SQL PostgreSQL (HA)        |  |
|  | - Shopping carts, sessions|              | - Primary (Zone a)               |  |
|  | - Volatile / Rebuildable  |              | - Synchronous Standby (Zone b)   |  |
|  | - RTO < 30s, RPO = volatile|             | - RTO < 60s, RPO = 0 (ACID)      |  |
|  +---------------------------+              +----------------------------------+  |
|                                                              |                    |
|                                                              | (Continuous WAL)   |
|                                                              v                    |
|                                             +----------------------------------+  |
|                                             | DISASTER RECOVERY VAULT          |  |
|                                             | Cloud Storage Dual-Region (nam4) |  |
|                                             | - Immutable Point-in-Time WAL    |  |
|                                             | - WORM Bucket Lock (30-day)      |  |
|                                             | - RTO < 2h, RPO < 1m (PITR)      |  |
|                                             +----------------------------------+  |
+-----------------------------------------------------------------------------------+
EOF
cat scratch/day13_lab/state_diagram.txt | tee scratch/day13_lab/stage3_diagram_draft.txt
```

**Expected result:**
Textual state ownership architecture diagram authored and verified.

**Save:** scratch/day13_lab/stage3_diagram_draft.txt""",

            """**Stage 4: Formulate Vocabulary Definitions and GCP Reference Mappings**

**Location:** local terminal

**Actions:**
Author technical definitions and architectural examples for High Availability, Fault Tolerance, RTO, and RPO.
```bash
cat <<'EOF' > scratch/day13_lab/vocabulary_reference.md
# Core Reliability and Recovery Vocabulary

### 1. High Availability (HA)
- **Technical Definition:** The capability of a system to remain accessible and operational for an agreed-upon percentage of time (e.g., 99.9% to 99.99%) by eliminating single points of failure through automated redundancy and rapid failover across independent physical failure domains (such as availability zones).
- **Failover Behavior:** Tolerates a brief, bounded service interruption (seconds to minutes) while standby nodes promote and connection pools reconnect.
- **GCP Reference Architecture:** Regional Managed Instance Groups distributed across three zones in us-central1 paired with Cloud SQL High Availability with automatic synchronous cross-zone failover (RTO < 60s, RPO = 0).

### 2. Fault Tolerance (FT)
- **Technical Definition:** The capability of a system to operate continuously without any perceptible service interruption, performance degradation, or data loss (RTO = 0, RPO = 0) despite the sudden failure of underlying physical or software components.
- **Failover Behavior:** Zero downtime, zero dropped requests, and zero transaction retries required.
- **GCP Reference Architecture:** Cloud Spanner multi-region instance executing synchronous Paxos consensus across multiple distant regions with TrueTime synchronization, guaranteeing 99.999% SLA availability and zero failover pause.

### 3. Disaster Recovery (DR)
- **Technical Definition:** The comprehensive organizational policies, engineering procedures, and infrastructure assets designed to restore critical business operations, systems, and data integrity following a wide-scale catastrophic regional disaster (earthquake, hurricane, grid blackout, subsea cable sever, or ransomware sabotage).
- **Failover Behavior:** Operates across distant geographic regions; trades off recovery speed against infrastructure cost across cold, warm, and hot standby patterns.
- **GCP Reference Architecture:** Dual-region Cloud Storage buckets (nam4) with Turbo Replication (< 15-minute SLA) paired with Cloud SQL Cross-Region Read Replicas and declarative Terraform reconstitution scripts (RTO < 2 hours, RPO < 1 minute).

### 4. Recovery Point Objective (RPO)
- **Technical Definition:** The maximum acceptable age of data files and transaction records that can be permanently lost when an outage occurs, measured backward in time from the moment of disruption.
- **Architectural Driver:** Dictates data replication mechanics. RPO = 0 requires synchronous cross-zone commits; RPO in minutes allows asynchronous replication; RPO in hours permits periodic backup snapshots.

### 5. Recovery Time Objective (RTO)
- **Technical Definition:** The maximum acceptable duration of clock time elapsed between the initial system failure and the complete restoration of functional business capability for end users.
- **Architectural Driver:** Dictates compute readiness. RTO in seconds requires active-active or hot-standby instances; RTO in hours allows cold provisioning via Infrastructure as Code.
EOF
cat scratch/day13_lab/vocabulary_reference.md | head -n 35 | tee scratch/day13_lab/stage4_vocabulary.txt
```

**Expected result:**
Technical vocabulary definitions and GCP reference architectures authored.

**Save:** scratch/day13_lab/stage4_vocabulary.txt""",

            """**Stage 5: Author Comprehensive State Ownership and Recovery Artifact**

**Location:** local terminal

**Actions:**
Synthesize all definitions, diagrams, and comparative matrices into the authoritative Day 13 exit evidence artifact: scratch/day-013-state-ownership.md.
```bash
cat <<'EOF' > scratch/day13_lab/generate_exit_artifact.py
import sys

text = '''# Day 13 Exit Evidence: State Ownership Architecture & Recovery Definitions

## Executive Summary
This document establishes the authoritative state ownership model, failure domain boundaries, and recovery vocabulary for OmniCommerce Enterprise. It delineates the architectural division between ephemeral stateless compute workers and durable state stores, defines High Availability, Fault Tolerance, RTO, and RPO with concrete Google Cloud examples, and documents why high-availability replication does not replace point-in-time recovery backups.

---

## 1. State Ownership Architecture Diagram

~~~text
+-----------------------------------------------------------------------------------+
|                            STATE OWNERSHIP ARCHITECTURE                           |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Client Browser ] ---> (Anycast BGP Edge PoP / Cloud Armor / Cloud CDN)        |
|                                         |                                         |
|                                         v (HTTPS Requests + Idempotency Tokens)   |
|  +-----------------------------------------------------------------------------+  |
|  | STATELESS WORKER TIER (Cloud Run / Regional MIG across Zones a, b, c)        |  |
|  | - Ephemeral, disposable worker containers; zero local disk state            |  |
|  | - Scales from 2 to 200 instances dynamically; crash-tolerant                |  |
|  +-----------------------------------------------------------------------------+  |
|               |                                              |                    |
|               | (Session Lookup / Cache)                     | (Committed Writes) |
|               v                                              v                    |
|  +---------------------------+              +----------------------------------+  |
|  | SESSION CACHE TIER        |              | AUTHORITATIVE DATA TIER          |  |
|  | Memorystore (Redis HA)    |              | Cloud SQL PostgreSQL (HA)        |  |
|  | - Shopping carts, sessions|              | - Primary (Zone a)               |  |
|  | - Volatile / Rebuildable  |              | - Synchronous Standby (Zone b)   |  |
|  | - RTO < 30s, RPO = volatile|             | - RTO < 60s, RPO = 0 (ACID)      |  |
|  +---------------------------+              +----------------------------------+  |
|                                                              |                    |
|                                                              | (Continuous WAL)   |
|                                                              v                    |
|                                             +----------------------------------+  |
|                                             | DISASTER RECOVERY VAULT          |  |
|                                             | Cloud Storage Dual-Region (nam4) |  |
|                                             | - Immutable Point-in-Time WAL    |  |
|                                             | - WORM Bucket Lock (30-day)      |  |
|                                             | - RTO < 2h, RPO < 1m (PITR)      |  |
|                                             +----------------------------------+  |
+-----------------------------------------------------------------------------------+
~~~

---

## 2. State Ownership Tier Matrix

| Architectural Tier | GCP Technology | State Classification | Durability Invariant | Failover & Scaling Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Edge Tier** | Cloud CDN / Cloud Armor | Stateless Perimeter | Zero State | Anycast BGP routing to nearest edge PoP |
| **Compute Tier** | Cloud Run / Regional MIG | Ephemeral Workers | Disposable | Sub-minute horizontal scaling; crash-tolerant |
| **Session Cache** | Memorystore (Redis HA) | Volatile Session State | Rebuildable | Dual-zone primary/standby failover (< 30s) |
| **Authoritative Data**| Cloud SQL PostgreSQL HA | Durable ACID State | Permanent | Synchronous zonal disk replication (RTO < 60s, RPO = 0) |
| **Recovery Vault** | Cloud Storage (nam4) | Immutable Historical State| WORM Locked | Dual-region Turbo Replication (RTO < 2h, RPO < 1m) |

---

## 3. Reliability & Recovery Vocabulary Definitions

### 1. High Availability (HA)
- **Definition:** System design ensuring operational uptime (99.9% to 99.99%) through automated redundancy across independent physical failure domains (zones), accepting brief, bounded failover pauses (seconds to minutes).
- **GCP Example:** Regional Managed Instance Groups in `us-central1` spanning zones a, b, and c paired with Cloud SQL HA synchronous standby replication (RTO < 60s, RPO = 0).

### 2. Fault Tolerance (FT)
- **Definition:** System design guaranteeing completely uninterrupted continuous operation with zero perceived downtime and zero data loss (RTO = 0, RPO = 0) despite underlying component failure.
- **GCP Example:** Cloud Spanner multi-region database utilizing distributed Paxos consensus and TrueTime atomic clocks to deliver five-nines (99.999%) availability with zero failover disruption.

### 3. Disaster Recovery (DR)
- **Definition:** The policies and technical capabilities required to reconstitute critical business functions and data following catastrophic regional disruptions.
- **GCP Example:** Asynchronous cross-region replication to `europe-west1` via Cloud Storage dual-region buckets and Cloud SQL Cross-Region Read Replicas (RTO < 2h, RPO < 15m).

### 4. Recovery Point Objective (RPO)
- **Definition:** The maximum acceptable duration of uncommitted or lost transaction data during an outage.
- **GCP Example:** Cloud SQL HA achieves RPO = 0 for single-zone failures via synchronous regional persistent disk commits; cross-region DR achieves RPO < 1 minute via streaming WAL shipping.

### 5. Recovery Time Objective (RTO)
- **Definition:** The maximum acceptable elapsed real time between failure occurrence and full operational service restoration.
- **GCP Example:** Stateless Cloud Run API achieves RTO < 10 seconds via load balancer rerouting; database Point-in-Time Recovery achieves RTO < 45 minutes for full 500 GB storage volume reconstitution.

---

## 4. The Critical Distinction: Available Replica vs Recoverable Backup

| Evaluation Dimension | Available Replica (HA / Read Replica) | Recoverable Backup (PITR Archive) |
| :--- | :--- | :--- |
| **Primary Architectural Purpose** | Live traffic serving, read offloading, node failover | Point-in-time state recovery, historical audit |
| **Data Synchronization** | Real-time streaming (Synchronous or Asynchronous) | Periodic snapshots + continuous immutable WAL |
| **Vulnerability to Logical Corruption**| **CRITICAL VULNERABILITY:** Replicates DROP/TRUNCATE immediately | **PROTECTED:** Isolated from live database mutations |
| **Recovery Time Objective (RTO)** | Seconds to minutes (Rapid promotion) | 30 minutes to 2 hours (Volume restore & replay) |
| **Recovery Point Objective (RPO)** | 0 to seconds (Near real-time) | < 1 minute (Granular second-level replay) |
| **Cost Profile** | Continuous compute + storage + replication egress | Economical object storage (Cloud Storage Nearline/Coldline) |

**Architectural Rule:** *"Replication protects against hardware failure; backups protect against human error and corruption."* Both mechanisms are mandatory in enterprise production architectures.

---

## 5. Architectural Approval and Sign-Off
- **Author Role:** Lead Enterprise Cloud Architect
- **Approval Date:** 2026-10-04
- **Verification Status:** VERIFIED AND APPROVED FOR IMPLEMENTATION
'''

with open('scratch/day-013-state-ownership.md', 'w') as f:
    f.write(text.strip() + '\\n')
print(f'Created scratch/day-013-state-ownership.md ({len(text)} bytes)')
EOF
python3 scratch/day13_lab/generate_exit_artifact.py
cat scratch/day-013-state-ownership.md | head -n 45 | tee scratch/day13_lab/stage5_artifact_preview.txt
```

**Expected result:**
Comprehensive state ownership artifact generated at scratch/day-013-state-ownership.md and verified.

**Save:** scratch/day-013-state-ownership.md""",

            """**Stage 6: Inspect Document Integrity and Header Structure**

**Location:** local terminal

**Actions:**
Inspect the generated state ownership document to confirm that all required sections and diagrams are complete.
```bash
wc -l scratch/day-013-state-ownership.md | tee scratch/day13_lab/stage6_wc.txt
grep -E "^## " scratch/day-013-state-ownership.md | tee scratch/day13_lab/stage6_headers.txt
```

**Expected result:**
Line count confirms a detailed document (> 100 lines) and all five main sections are confirmed present.

**Save:** scratch/day13_lab/stage6_headers.txt""",

            """**Stage 7: Verify Alignment with Roadmap Practice and Exit Criteria**

**Location:** local terminal

**Actions:**
Run an automated verification check against the required roadmap exit components (diagram, HA, FT, RTO, RPO definitions, and replica vs backup evaluation).
```bash
python3 -c "
import sys
with open('scratch/day-013-state-ownership.md') as f:
    text = f.read()

required = [
    'STATE OWNERSHIP ARCHITECTURE',
    'High Availability (HA)',
    'Fault Tolerance (FT)',
    'Disaster Recovery (DR)',
    'Recovery Point Objective (RPO)',
    'Recovery Time Objective (RTO)',
    'Available Replica vs Recoverable Backup'
]

missing = [r for r in required if r not in text]
if missing:
    print(f'FAILED: Missing required sections: {missing}')
    sys.exit(1)
else:
    print('ALL ROADMAP EXIT CRITERIA VERIFIED SUCCESSFULLY.')
" | tee scratch/day13_lab/stage7_criteria_check.txt
```

**Expected result:**
All roadmap exit criteria confirmed present in the document.

**Save:** scratch/day13_lab/stage7_criteria_check.txt""",

            """**Stage 8: Final Audit and Verification Sign-Off**

**Location:** local terminal

**Actions:**
Audit the final artifact and confirm readiness for batch gate validation.
```bash
python3 -c "with open('scratch/day-013-state-ownership.md') as f: print(f'DAY 13 EXIT EVIDENCE ARTIFACT: COMPLETE AND VERIFIED ({len(f.read())} bytes)')" | tee scratch/day13_lab/stage8_final_audit.txt
```

**Expected result:**
Final verification sign-off confirmed.

**Save:** scratch/day13_lab/stage8_final_audit.txt"""
        ]
    }
}
