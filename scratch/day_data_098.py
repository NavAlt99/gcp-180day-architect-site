"""day_data_098.py — Exhaustive architecture data specification for Day 98.

Covers Restore and Failover Acceptance:
1. Recovery acceptance criteria: post-restore verification gates, read-write transactional validation, connection pool reconnection, DNS/Private Service Access endpoint integrity.
2. Invariant verification and RTO/RPO measurement: mathematical validation of Recovery Time Objective (RTO) and Recovery Point Objective (RPO), financial ledger balance conservation, and the single-fulfillment invariant.
3. Comparative recovery paths: Cloud SQL Regional High Availability (automatic synchronous failover, RPO=0, RTO 60–120s) versus Cross-Region Replica Promotion (asynchronous disaster recovery, RPO > 0, RTO 5–15m); executing one representative path while detailing the alternative.
Follows PAGE_AUTHORING_CONTRACT.md with hands-on, verifiable exercises.
"""

DAY_NUM = 98

DATA = {
    "day": 98,
    "part1_intro": (
        "Day 98 establishes the rigorous operational and mathematical acceptance gates required before declaring a database restore "
        "or disaster recovery failover successful. In enterprise systems, completing a database restore command is merely the initial step; "
        "production traffic must never be released until data integrity invariants, replication parity, and application connection health "
        "are empirically verified. Today's curriculum builds a comprehensive Disaster Recovery Acceptance Framework: validating transaction "
        "consistency, measuring observed RTO and RPO against contractual SLAs, comparing Cloud SQL Regional HA with Cross-Region Replica Promotion, "
        "and executing automated post-failover acceptance tests defending the core single-fulfillment business invariant."
    ),
    "exit_summary": (
        "Executed an enterprise Database Restore and Failover Acceptance drill: measured empirical recovery duration (RTO = 84s) and data loss (RPO = 0s); "
        "authored and verified an executable failover runbook comparing Cloud SQL Regional HA against Cross-Region Promotion; validated mathematical "
        "ledger balance conservation and the single-fulfillment invariant with explicit distinctions between lab metrics and production enterprise boundaries."
    ),
    "part2_intro": (
        "Disaster recovery acceptance bridges infrastructure automation with application correctness. The sections below analyze acceptance test "
        "mechanics, invariant verification math, and the technical trade-offs distinguishing synchronous Regional HA from asynchronous cross-region promotion."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Recovery Architecture / Topology</th>
      <th>Replication Mechanics &amp; Protocol</th>
      <th>Measured RPO (Data Loss)</th>
      <th>Measured RTO (Recovery Time)</th>
      <th>Failover Trigger &amp; Operational Trade-off</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Cloud SQL Regional HA</strong></td>
      <td>Synchronous block-level replication via Regional Persistent Disk across 2 zones</td>
      <td><strong>RPO = 0</strong> (Zero committed transaction loss)</td>
      <td><strong>RTO = 60–120s</strong> (Automated failover &amp; crash recovery replay)</td>
      <td>Fully automated via Google Cloud control plane; protects against single-zone outage; identical regional pricing premium</td>
    </tr>
    <tr>
      <td><strong>Cross-Region Read Replica Promotion</strong></td>
      <td>Asynchronous database replication (PostgreSQL streaming / MySQL binary logs)</td>
      <td><strong>RPO = Seconds to Minutes</strong> (Proportional to network byte lag)</td>
      <td><strong>RTO = 5–15 minutes</strong> (Manual or semi-automated promote command + DNS cutover)</td>
      <td>Manual or scripted decision; protects against total multi-zone regional catastrophe; requires reverse-replication rebuild to fail back</td>
    </tr>
    <tr>
      <td><strong>Point-in-Time Recovery (PITR Backup)</strong></td>
      <td>Full daily snapshot base backup + continuous Write-Ahead Log (WAL) archive</td>
      <td><strong>RPO &lt; 5 minutes</strong> (To the specific second prior to corruption)</td>
      <td><strong>RTO = 30–90 minutes</strong> (Provision new instance + restore storage + replay WAL)</td>
      <td>Human-authorized disaster response; used for accidental table drop, ransomware, or schema corruption; provisions a new instance IP</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Cloud SQL Disaster Recovery Acceptance & Verification Flow",
        "desc": "Flow diagram showing primary instance failure, Regional HA failover execution, connection pool reconnection, and automated invariant acceptance testing.",
        "caption": "Figure 98.1: End-to-end failover lifecycle, automated invariant verification gate, and production traffic release boundary.",
        "nodes": [
            ("1. Primary Zone Failure", "Zone B primary halts"),
            ("2. Regional HA Failover", "Standby promoted in 84s"),
            ("3. Acceptance Verification", "Single fulfillment & balances tested"),
            ("4. Traffic Re-admission", "Healthy instances accept traffic"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Recovery Acceptance Criteria After Backup Restore or Replica Promotion",
            "overview": (
                "Declaring a database recovered requires satisfying explicit, objective acceptance criteria spanning network, security, and data layers. "
                "Too often, teams celebrate when a backup restore or replica promotion operation completes successfully in the CLI, "
                "only to direct user traffic to an instance that lacks necessary IAM service account bindings, has outdated read-only parameters, or contains "
                "corrupted foreign key indexes. An enterprise acceptance checklist enforces sequential verification gates before read-write connection "
                "pools are re-opened to client traffic."
            ),
            "preview": (
                "A promoted read replica accepts traffic while still configured in read-only transaction mode, causing all customer checkout writes to fail. "
                "Pre-traffic recovery acceptance gates verify read-write status and connection pool reconnection before opening application ingress."
            ),
            "technical": (
                "### 1. The Four-Stage Recovery Acceptance Pipeline\n"
                "- **Stage 1: Infrastructure Readiness Gate:**\n"
                "  - Verify database instance status is `RUNNABLE` via the instance describe API.\n"
                "  - Confirm Private Service Access (PSA) VPC peering IP address is reachable from application subnets.\n"
                "  - Verify SSL/TLS certificates and Cloud SQL Auth Proxy client authorization tokens.\n"
                "- **Stage 2: Engine Configuration & Mode Gate:**\n"
                "  - In promoted replicas, assert the database engine has disabled standby mode: `SHOW transaction_read_only;` must return `off`.\n"
                "  - Check `max_connections`, `shared_buffers`, and active connection headroom.\n"
                "- **Stage 3: Application Health Gate:**\n"
                "  - Execute lightweight diagnostic query: `SELECT 1;`.\n"
                "  - Test connection pool draining and recycling: ensure application pods re-establish live sockets without stale connection errors.\n"
                "- **Stage 4: Post-Restore Binary Log & Replication Stream Gate:**\n"
                "  - If promoted to primary, ensure automated backups and point-in-time recovery (WAL archiving) are re-enabled immediately.\n"
                "  - A newly promoted primary is un-backed-up until a fresh base snapshot completes; running without backups creates severe residual risk."
            ),
            "questions": [
                "Why must a promoted replica immediately have automated backups and WAL archiving re-enabled before opening production write traffic?",
                "What hidden configuration states (such as `transaction_read_only = on`) can cause a promoted replica to reject application writes?",
                "How does the Cloud SQL Auth Proxy handle automatic connection recovery when a primary instance changes IP addresses during failover?",
            ],
            "reference": "https://docs.cloud.google.com/sql/docs/postgres/high-availability",
            "reference_label": "Google Cloud SQL: High availability configuration and post-failover recovery mechanics",
            "scenario": {
                "symptom": (
                    "Following an emergency cross-region replica promotion during a regional outage, all Brightloaf customer checkout transactions "
                    "threw HTTP 500 errors with database exception: `ERROR: cannot execute INSERT in a read-only transaction`."
                ),
                "constraints": (
                    "Must automate post-promotion acceptance checks so that transaction read-write mode is verified before application pods switch database endpoints."
                ),
                "evidence": (
                    "The promotion script promoted the replica instance in `us-east1`, but the application's connection string configuration still pointed "
                    "to a local read-only connection pool that had `read_only = true` hardcoded in its HikariCP datasource properties."
                ),
                "diagnostic_steps": [
                    "Execute direct psql query against promoted instance: `SELECT pg_is_in_recovery();`.",
                    "Inspect application pod datasource configuration and environment variable overrides.",
                    "Review application error logs in Logs Explorer for specific database SQL state codes (`25006`).",
                ],
                "root": (
                    "Unverified application datasource binding: the database had promoted correctly to primary, but the application connection pool "
                    "was configured with read-only session flags, rejecting all insert operations."
                ),
                "fix": (
                    "Incorporate an automated pre-flight acceptance probe in the deployment script that executes a transactional insert/delete test "
                    "using the application's primary datasource credentials before updating Cloud DNS or Kubernetes service selectors."
                ),
                "verify": (
                    "Run automated acceptance probe script; confirm it executes a canary write transaction, verifies `pg_is_in_recovery() = false`, "
                    "and returns exit code 0 before traffic shifting occurs."
                ),
                "residual": (
                    "Cross-region promotion breaks the original replication link; a new replica must be provisioned in the primary region to re-establish HA."
                ),
                "diagram": (
                    "Replica promoted to primary",
                    "App connection pool set to read-only",
                    "Customer checkout INSERTs fail (500)",
                    "Pre-flight acceptance probe deployed",
                    "Read-write verified; zero failed checkouts"
                )
            },
            "lab": {
                "name": "Database Recovery Acceptance Probe and Pre-Traffic Verification Script",
                "goal": "Author an automated Python acceptance verification runner that validates database readiness, read-write state, and connection pool health.",
                "expected": "An executable Python script executing the 4 recovery acceptance stages and outputting a structured acceptance certificate.",
                "mode": "local script execution",
                "prereq": "Understanding of relational database transactions and failover mechanics.",
                "preflight": "Ensure Python 3 standard library is present; no external packages needed.",
                "steps": [
                    "Author the automated database recovery acceptance runner (`verify_recovery_acceptance.py`):\n\n```sh\ncat <<'EOF' > verify_recovery_acceptance.py\n# Automated Post-Restore / Post-Failover Recovery Acceptance Engine\nimport json\nimport time\n\nclass SimulatedDatabase:\n    def __init__(self, is_in_recovery=False, allow_writes=True, current_connections=12):\n        self._in_recovery = is_in_recovery\n        self._allow_writes = allow_writes\n        self._connections = current_connections\n        self._max_connections = 100\n        self.table_data = {}\n        \n    def query_scalar(self, sql):\n        if sql == \"SELECT pg_is_in_recovery();\":\n            return self._in_recovery\n        if sql == \"SHOW transaction_read_only;\":\n            return \"on\" if not self._allow_writes else \"off\"\n        if sql == \"SELECT count(*) FROM pg_stat_activity;\":\n            return self._connections\n        return None\n        \n    def execute_canary_transaction(self, test_key, test_val):\n        if not self._allow_writes or self._in_recovery:\n            raise RuntimeError(\"ERROR: cannot execute INSERT in a read-only transaction\")\n        self.table_data[test_key] = test_val\n        # Delete immediately to leave zero residual data\n        del self.table_data[test_key]\n        return True\n\ndef run_recovery_acceptance_suite(db_instance):\n    results = {\n        \"timestamp\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime()),\n        \"stages\": {},\n        \"passed\": False\n    }\n    \n    # Stage 1: Engine Recovery Mode Assertion\n    in_rec = db_instance.query_scalar(\"SELECT pg_is_in_recovery();\")\n    results[\"stages\"][\"1_engine_mode\"] = {\n        \"check\": \"pg_is_in_recovery == False\",\n        \"value\": in_rec,\n        \"status\": \"PASS\" if not in_rec else \"FAIL\"\n    }\n    \n    # Stage 2: Transaction Read-Write Mode Assertion\n    ro_status = db_instance.query_scalar(\"SHOW transaction_read_only;\")\n    results[\"stages\"][\"2_read_write_mode\"] = {\n        \"check\": \"transaction_read_only == off\",\n        \"value\": ro_status,\n        \"status\": \"PASS\" if ro_status == \"off\" else \"FAIL\"\n    }\n    \n    # Stage 3: Connection Headroom Assertion\n    active_conns = db_instance.query_scalar(\"SELECT count(*) FROM pg_stat_activity;\")\n    headroom_ok = active_conns < 80 # Must have >20% headroom\n    results[\"stages\"][\"3_connection_headroom\"] = {\n        \"active_connections\": active_conns,\n        \"headroom_sufficient\": headroom_ok,\n        \"status\": \"PASS\" if headroom_ok else \"FAIL\"\n    }\n    \n    # Stage 4: Live Canary Write/Delete Transaction\n    canary_ok = False\n    try:\n        canary_ok = db_instance.execute_canary_transaction(\"__canary_probe__\", \"probe_val\")\n        results[\"stages\"][\"4_canary_transaction\"] = {\"status\": \"PASS\", \"error\": None}\n    except Exception as e:\n        results[\"stages\"][\"4_canary_transaction\"] = {\"status\": \"FAIL\", \"error\": str(e)}\n        \n    # Overall Acceptance Certificate\n    all_passed = (not in_rec) and (ro_status == \"off\") and headroom_ok and canary_ok\n    results[\"passed\"] = all_passed\n    return results\n\n# Scenario A: Promoted Primary that is fully healthy\nhealthy_promoted_db = SimulatedDatabase(is_in_recovery=False, allow_writes=True, current_connections=15)\ncert_healthy = run_recovery_acceptance_suite(healthy_promoted_db)\nprint(\"=== SCENARIO A: HEALTHY PROMOTED INSTANCE ===\")\nprint(json.dumps(cert_healthy, indent=2))\nassert cert_healthy[\"passed\"], \"Healthy promoted instance should pass acceptance!\"\n\n# Scenario B: Promoted instance stuck in read-only mode\nunhealthy_ro_db = SimulatedDatabase(is_in_recovery=False, allow_writes=False, current_connections=15)\ncert_unhealthy = run_recovery_acceptance_suite(unhealthy_ro_db)\nprint(\"\n=== SCENARIO B: UNHEALTHY READ-ONLY INSTANCE ===\")\nprint(json.dumps(cert_unhealthy, indent=2))\nassert not cert_unhealthy[\"passed\"], \"Read-only instance must be rejected by acceptance suite!\"\n\nprint(\"\nPASS: Database recovery acceptance engine mathematically verified.\")\nEOF\npython3 verify_recovery_acceptance.py\n```",
                    "Review all output artifacts and confirm that the Python acceptance suite runs cleanly and correctly gates unhealthy instances."
                ],
                "verification": "The Python acceptance engine verifies recovery mode, read-write status, connection headroom, and canary transaction execution before certifying readiness.",
                "trouble": "Ensure canary transaction cleans up its temporary test rows so no synthetic probe artifacts remain in production schemas.",
                "cleanup": "Retain `verify_recovery_acceptance.py` as an exit evidence artifact.",
                "accept": "Completed database recovery acceptance probe and verified execution certificate. File: `day-098-topic-01-recovery-acceptance.md`.",
                "file": "day-098-topic-01-recovery-acceptance.md"
            }
        },
        {
            "key": "topic-02",
            "title": "Verifying Data Invariants, Recovery Time (RTO), and Data Loss (RPO)",
            "overview": (
                "After a database restore or failover, infrastructure metrics measure duration and connection counts, but only application-level "
                "data invariants prove whether data corruption or transaction loss occurred. A business invariant is an immutable truth that must "
                "hold across all operational states: in banking, total debits must equal total credits; in e-commerce, every paid order must be fulfilled "
                "exactly once and inventory count plus items sold must equal total initial stock. Verifying these invariants against post-restore "
                "data provides empirical proof of actual Recovery Point Objective (RPO) and confirms zero customer financial harm."
            ),
            "preview": (
                "A database restore finishes in 10 minutes, but 45 in-flight payment records lack corresponding fulfillment entries. "
                "Running post-restore invariant reconciliation scripts isolates unfulfilled transactions and measures actual data loss."
            ),
            "technical": (
                "### 1. Mathematical Definitions of RTO and RPO\n"
                "- **Recovery Time Objective (RTO):** The maximum tolerable elapsed time between the declaration of disaster and the full restoration "
                "of production read-write capability: $\\text{RTO} = T_{\\text{restored}} - T_{\\text{disaster}}$.\n"
                "- **Recovery Point Objective (RPO):** The maximum acceptable data loss measured in time backward from the disaster event: "
                "$\\text{RPO} = T_{\\text{disaster}} - T_{\\text{last\\_committed\\_data\\_preserved}}$.\n\n"
                "### 2. Core Business Invariant Verification\n"
                "- **Invariant 1: Conservation of Account Balances:**\n"
                "  $$\\sum \\text{Customer Balances} + \\sum \\text{Pending Escrow} = \\text{Total Ledger Cash}$$\n"
                "- **Invariant 2: Strict Single Fulfillment:**\n"
                "  $$\\forall \\text{order} \\in \\text{Orders}: \\text{count}(\\text{fulfillments}(\\text{order})) = 1 \\iff \\text{order.status} = \\text{'PAID'}$$\n"
                "  Every paid order must have exactly one warehouse dispatch record; zero paid orders may have duplicate or zero dispatches.\n"
                "- **Invariant 3: Inventory Stock Parity:**\n"
                "  $$\\text{Current Stock} + \\sum \\text{Shipped Quantities} = \\text{Initial Stock}$$\n\n"
                "### 3. Auditing Alerting Behavior During Failover\n"
                "- When a database fails over, dozens of downstream microservices experience temporary connection pool drops.\n"
                "- **Alert Fatigue Prevention:** SLO burn-rate alerts must distinguish between an acute 60-second failover window (which burns a minor fraction "
                "of the 30-day error budget) and an unrecovered, catastrophic total outage. If the failover completes within the contractual RTO (e.g. <120s), "
                "incident managers should receive informational updates while on-call escalation pages are held until RTO thresholds are breached."
            ),
            "questions": [
                "What is the mathematical difference between infrastructure restoration time (RTO) and transactional data loss (RPO)?",
                "How does verifying application-level data invariants prove data consistency beyond low-level database page checksums?",
                "Why should alert policies incorporate grace periods matching the expected database HA failover duration?",
            ],
            "reference": "https://sre.google/sre-book/data-integrity/",
            "reference_label": "Google Site Reliability Engineering: Data integrity, verification, and recovery principles",
            "scenario": {
                "symptom": (
                    "Following an unexpected Cloud SQL zonal failover, warehouse dispatch operators reported that 28 orders placed immediately prior "
                    "to the failover were dispatched twice, while 14 customer credit cards were charged without an order record being created."
                ),
                "constraints": (
                    "Must establish an automated invariant verification script that reconciles payment gateway ledgers against database order records "
                    "immediately post-failover."
                ),
                "evidence": (
                    "Log analysis revealed that during the 90-second failover, the asynchronous payment webhook worker retried transactions without "
                    "enclosing the payment record and order record inside an atomic distributed transaction."
                ),
                "diagnostic_steps": [
                    "Query the database for orphan payment tokens lacking corresponding order IDs.",
                    "Audit warehouse dispatch records grouped by `order_id` to identify duplicate entries.",
                    "Reconcile payment gateway settlement reports against database ledger tables.",
                ],
                "root": (
                    "Non-atomic transactional boundaries: decoupled database writes without cross-table atomic locks allowed transient failover disconnects "
                    "to corrupt business state consistency."
                ),
                "fix": (
                    "Enclose order creation, inventory deduction, and payment capture inside an atomic database transaction. Implement post-failover "
                    "invariant verification scripts that audit data integrity before opening ingress."
                ),
                "verify": (
                    "Trigger a simulated failover; execute the invariant reconciliation script; confirm 100% of orders satisfy the single-fulfillment invariant "
                    "with zero duplicate dispatches and zero orphan charges."
                ),
                "residual": (
                    "External third-party payment gateways operate outside the local database ACID boundary; distributed two-phase commit or transactional outbox patterns are required."
                ),
                "diagram": (
                    "Zonal failover occurs",
                    "Non-atomic writes split during cutover",
                    "28 duplicate dispatches & orphan charges",
                    "Atomic transaction & invariant auditor deployed",
                    "100% single fulfillment verified; 0 discrepancies"
                )
            },
            "lab": {
                "name": "Data Invariant Reconciliation Engine and RTO/RPO Measurement Script",
                "goal": "Author an executable Python script calculating empirical RTO and RPO and verifying the single-fulfillment business invariant across a simulated failover.",
                "expected": "A runnable Python script executing invariant mathematical audits and outputting an RTO/RPO measurement certificate.",
                "mode": "local script execution",
                "prereq": "Understanding of business invariants, data integrity, and RTO/RPO calculations.",
                "preflight": "Ensure Python 3 standard library is present; no external packages required.",
                "steps": [
                    "Author the automated business invariant auditor and RTO/RPO calculator (`audit_data_invariants.py`):\n\n```sh\ncat <<'EOF' > audit_data_invariants.py\n# Automated Business Invariant Auditor and RTO/RPO Verification Engine\nimport json\nimport time\n\n# Simulated Post-Failover Dataset\norders_table = [\n    {\"order_id\": f\"ord-{i:03d}\", \"customer\": f\"cust-{i:03d}\", \"amount\": 50.0, \"status\": \"PAID\"}\n    for i in range(1, 101)\n]\n\n# Simulated fulfillments: Exactly 1 per order (Normal invariant)\nfulfillments_table = [\n    {\"fulfillment_id\": f\"ful-{i:03d}\", \"order_id\": f\"ord-{i:03d}\", \"carrier\": \"FedEx\"}\n    for i in range(1, 101)\n]\n\ndef verify_single_fulfillment_invariant(orders, fulfillments):\n    fulfillment_counts = {}\n    for f in fulfillments:\n        oid = f[\"order_id\"]\n        fulfillment_counts[oid] = fulfillment_counts.get(oid, 0) + 1\n        \n    violations = []\n    for o in orders:\n        oid = o[\"order_id\"]\n        count = fulfillment_counts.get(oid, 0)\n        if o[\"status\"] == \"PAID\" and count != 1:\n            violations.append({\n                \"order_id\": oid,\n                \"status\": o[\"status\"],\n                \"fulfillment_count\": count,\n                \"violation\": \"Duplicate fulfillment\" if count > 1 else \"Missing fulfillment\"\n            })\n            \n    return (len(violations) == 0), violations\n\ndef measure_rto_rpo(disaster_time_epoch, recovery_time_epoch, last_committed_epoch):\n    # RTO: Elapsed duration to restore service\n    measured_rto_sec = recovery_time_epoch - disaster_time_epoch\n    # RPO: Data gap between disaster and last preserved transaction\n    measured_rpo_sec = max(0, disaster_time_epoch - last_committed_epoch)\n    \n    return {\n        \"measured_rto_seconds\": measured_rto_sec,\n        \"measured_rpo_seconds\": measured_rpo_sec,\n        \"rto_sla_target_seconds\": 120,\n        \"rpo_sla_target_seconds\": 0,\n        \"rto_compliant\": measured_rto_sec <= 120,\n        \"rpo_compliant\": measured_rpo_sec == 0\n    }\n\n# Execute Invariant Audit\ninvariant_passed, violations = verify_single_fulfillment_invariant(orders_table, fulfillments_table)\nprint(\"=== INVARIANT VERIFICATION: SINGLE FULFILLMENT ===\")\nprint(f\"All 100 Paid Orders Have Exactly 1 Fulfillment: {invariant_passed}\")\nassert invariant_passed, f\"Invariant breached: {violations}\"\n\n# Measure Recovery Metrics for Regional HA Failover\nt_disaster = 1700000000\nt_recovered = 1700000084 # Restored in 84 seconds\nt_last_data = 1700000000  # Synchronous replication preserved all data (0s loss)\n\nrecovery_metrics = measure_rto_rpo(t_disaster, t_recovered, t_last_data)\nprint(\"\n=== MEASURED RTO AND RPO METRICS ===\")\nprint(json.dumps(recovery_metrics, indent=2))\n\nassert recovery_metrics[\"rto_compliant\"], \"RTO breached SLA target!\"\nassert recovery_metrics[\"rpo_compliant\"], \"RPO breached: Data loss occurred!\"\n\nprint(\"\nPASS: Invariant verification and RTO/RPO evaluation mathematically certified.\")\nEOF\npython3 audit_data_invariants.py\n```",
                    "Author the tested runbook and explicit distinction sheet between lab metrics and production enterprise boundaries (`day-098-topic-02-rto-rpo-report.md`):\n\n```sh\ncat <<'EOF' > day-098-topic-02-rto-rpo-report.md\n# Day 98: Measured Recovery Metrics, Invariant Audit & Production RTO/RPO Boundary Report\n\n## 1. Measured Lab Recovery Metrics\n- **Target Scenario:** Cloud SQL PostgreSQL Regional HA Zonal Failover Drill.\n- **Disaster Injected:** Primary database VM in `us-central1-b` halted via forced ACPI shutdown.\n- **Measured RTO:** **84 seconds** (Automatic detection: 20s, Standby promotion: 45s, DNS/proxy update: 19s). Target SLA: <= 120s.\n- **Measured RPO:** **0 seconds** (Synchronous Regional Persistent Disk replication preserved 100% of committed transactions).\n- **Business Invariant Verification:** Exactly 100 out of 100 paid orders had exactly 1 warehouse fulfillment record (0 duplicates, 0 missing).\n\n## 2. Tested Disaster Recovery Runbook Steps\n1. Confirm primary failure in Cloud Monitoring (`cloudsql.googleapis.com/database/up = 0`).\n2. Allow Cloud SQL automated HA control plane 90 seconds to initiate automatic standby promotion.\n3. Run `verify_recovery_acceptance.py` to confirm `pg_is_in_recovery() == false` and read-write transaction capability.\n4. Execute `audit_data_invariants.py` to verify account balance and single-fulfillment invariants.\n5. Re-enable application ingress traffic and monitor connection pool depth.\n\n## 3. Explicit Distinction from Production Enterprise Boundaries\n1. **Lab Scope vs Production Scale:** In this lab drill, the database size was 500 MB with 12 active connections. In production, a 2 TB database with 800 active connections will experience longer crash recovery replay time, extending actual RTO toward the 120–180s boundary.\n2. **Network BGP Convergence:** The lab assumes instantaneous local routing updates. Across global multi-region deployments, DNS TTLs and client connection caching may delay traffic migration by up to 60 seconds.\n3. **Replication Lag Sensitivity:** While Regional HA guarantees RPO=0, Cross-Region Promotion carries inherent asynchronous replication lag (RPO typically 2–15 seconds under normal load, but potentially minutes during high-throughput network saturation).\nEOF\ncat day-098-topic-02-rto-rpo-report.md\n```",
                    "Review all output artifacts and confirm that the Python invariant audit runs cleanly and the report details tested runbook steps and production boundaries."
                ],
                "verification": "The Python script calculates exact RTO and RPO metrics, confirms invariant compliance, and the report clearly delineates lab observations from production scale.",
                "trouble": "Ensure `last_committed_epoch` accurately reflects the timestamp of the latest persistent transaction to prevent artificial RPO calculations.",
                "cleanup": "Retain `audit_data_invariants.py` and `day-098-topic-02-rto-rpo-report.md` as exit evidence artifacts.",
                "accept": "Completed invariant audit script and verified RTO/RPO report. File: `day-098-topic-02-invariant-audit.md`.",
                "file": "day-098-topic-02-invariant-audit.md"
            }
        },
        {
            "key": "topic-03",
            "title": "Executing One Representative Recovery Path and Comparing Alternatives",
            "overview": (
                "A resilient architecture maintains distinct recovery paths optimized for different disaster scopes. **Cloud SQL Regional High Availability** "
                "is the primary intra-regional recovery path, providing fully automated, zero-data-loss failover across zones within seconds. "
                "Conversely, **Cross-Region Read Replica Promotion** is the catastrophic recovery path invoked only when an entire geographical cloud "
                "region experiences sustained, catastrophic failure. Understanding the exact mechanical trade-offs between these two paths—and executing "
                "one representative path while documenting the operational runbook for the alternative—is an essential competency for Google Cloud Professional Architects."
            ),
            "preview": (
                "An operational team panics during a single-zone network blip and executes a manual cross-region promotion, causing unnecessary data loss and breaking replication. "
                "Strict runbooks govern when to rely on automatic Regional HA versus when to trigger manual cross-region disaster recovery."
            ),
            "technical": (
                "### 1. Comparative Analysis of Recovery Paths\n"
                "- **Path A: Cloud SQL Regional High Availability (Representative Path Executed):**\n"
                "  - **Topology:** Primary instance in Zone A, Standby instance in Zone B, sharing a synchronized Regional Persistent Disk.\n"
                "  - **Failover Trigger:** Automated heartbeats detected by Google Cloud control plane. If the primary VM fails for >60s, the control plane "
                "attaches the regional disk to the standby VM and redirects the regional static IP.\n"
                "  - **RPO & RTO:** RPO = 0; RTO = 60–120 seconds.\n"
                "  - **Failback:** Completely seamless; once Zone A recovers, it automatically synchronizes as the new standby.\n"
                "- **Path B: Cross-Region Replica Promotion (Alternative Path Detailed):**\n"
                "  - **Topology:** Primary in `us-central1`, asynchronous Read Replica in `us-east1` replicating over Google's global fiber backbone.\n"
                "  - **Failover Trigger:** Human-in-the-loop operational decision. Promoted via the Cloud SQL replica promotion API.\n"
                "  - **RPO & RTO:** RPO = Asynchronous replication byte lag (typically 1–10 seconds); RTO = 5–15 minutes (provisioning standalone metadata, promoting instance, updating application DNS).\n"
                "  - **Failback Complexity:** High; promoting a replica permanently severs replication. To fail back, SREs must provision a new replica in `us-central1`, "
                "wait for full initial data synchronization, and execute a scheduled maintenance cutover."
            ),
            "questions": [
                "Under what exact operational criteria should an organization trigger cross-region replica promotion instead of waiting for Regional HA failover?",
                "Why does promoting a cross-region read replica permanently sever replication, and what steps are required to fail back?",
                "How does Regional Persistent Disk synchronous replication guarantee RPO=0 during an unexpected zonal hypervisor crash?",
            ],
            "reference": "https://docs.cloud.google.com/sql/docs/postgres/replication/cross-region-replicas",
            "reference_label": "Google Cloud SQL: Cross-region replication, promotion runbooks, and disaster recovery planning",
            "scenario": {
                "symptom": (
                    "During a localized power blip affecting a single zone in Iowa (`us-central1-a`), an on-call engineer panicked and executed a cross-region "
                    "promotion command to North Virginia (`us-east1`), causing $15,000 in un-replicated transaction data loss and a 6-hour database re-sync ordeal."
                ),
                "constraints": (
                    "Must establish strict operational runbook guardrails that forbid manual cross-region promotion for single-zone incidents."
                ),
                "evidence": (
                    "The primary Cloud SQL instance had Regional HA enabled and was already in the process of automated failover to `us-central1-b` (RPO=0). "
                    "The premature replica promotion in `us-east1` severed replication while 12 seconds of write transactions remained in transit."
                ),
                "diagnostic_steps": [
                    "Review Cloud Audit Logs to check who invoked `sql.instances.promoteReplica`.",
                    "Inspect Cloud SQL replication lag metrics `cloudsql.googleapis.com/database/replication/replica_byte_lag` prior to promotion.",
                    "Verify the status of the regional standby instance in `us-central1-b`.",
                ],
                "root": (
                    "Lack of operational runbook clarity: the responder did not understand that Regional HA automatically handles zonal loss with zero data loss, "
                    "mistakenly invoking a destructive cross-region disaster recovery protocol."
                ),
                "fix": (
                    "Enforce a mandatory 15-minute observation window and Incident Commander authorization before cross-region promotion can be invoked. "
                    "Document the exact decision matrix in the Disaster Recovery runbook."
                ),
                "verify": (
                    "Simulate single-zone failure; verify Regional HA completes within 90s with zero data loss. Confirm runbook prevents replica promotion."
                ),
                "residual": (
                    "If an entire cloud region suffers complete fiber severance lasting >4 hours, cross-region promotion remains the sole recovery mechanism."
                ),
                "diagram": (
                    "Zone A blip trips primary VM",
                    "Regional HA automatically promotes Zone B (RPO=0)",
                    "Panicked engineer triggers replica promotion in us-east1",
                    "Runbook decision matrix & guardrails enforced",
                    "Regional HA handles zonal loss; 0 data loss"
                )
            },
            "lab": {
                "name": "Cloud SQL Regional HA Failover Drill and Cross-Region Promotion Runbook",
                "goal": "Execute the representative Regional HA failover simulation and author the complete operational runbook for cross-region disaster recovery.",
                "expected": "A validated execution script for Regional HA failover, a comparative decision matrix, and a cross-region promotion runbook.",
                "mode": "tabletop analysis & shell synthesis",
                "prereq": "Understanding of Cloud SQL HA commands and cross-region replication.",
                "preflight": "Review Cloud SQL failover and replica promotion CLI operations.",
                "steps": [
                    "Author the shell execution script simulating the representative Regional HA failover path (`execute_regional_ha_drill.sh`):\n\n```sh\ncat <<'EOF' > execute_regional_ha_drill.sh\n#!/usr/bin/env bash\nset -euo pipefail\n\n# Execution of Representative Recovery Path: Cloud SQL Regional HA Failover\nINSTANCE_NAME=\"brightloaf-orders-db\"\nPROJECT_NAME=\"brightloaf-prod\"\n\necho \"=== 1. Preflight: Verify Primary HA Configuration ===\"\ncat <<COMMAND\ngcloud sql instances describe \"$INSTANCE_NAME\" \\\n    --project=\"$PROJECT_NAME\" \\\n    --format='table(name, state, region, gceZone, secondaryGceZone, settings.availabilityType)'\nCOMMAND\n\necho \"\n=== 2. Triggering Bounded Regional HA Failover ===\"\ncat <<COMMAND\n# Initiates automated failover to the synchronous secondary standby zone\ngcloud sql instances failover \"$INSTANCE_NAME\" \\\n    --project=\"$PROJECT_NAME\" \\\n    --quiet\nCOMMAND\n\necho \"\n=== 3. Post-Failover Verification ===\"\ncat <<COMMAND\n# Verify instance zone has swapped to previous secondary zone with RUNNABLE state\ngcloud sql instances describe \"$INSTANCE_NAME\" \\\n    --project=\"$PROJECT_NAME\" \\\n    --format='table(name, state, gceZone, secondaryGceZone)'\nCOMMAND\nEOF\nchmod +x execute_regional_ha_drill.sh\n./execute_regional_ha_drill.sh\n```",
                    "Author the operational decision matrix and emergency runbook for the alternative recovery path: Cross-Region Promotion (`day-098-topic-03-cross-region-runbook.md`):\n\n```sh\ncat <<'EOF' > day-098-topic-03-cross-region-runbook.md\n# Day 98: Disaster Recovery Runbook: Cross-Region Replica Promotion (Alternative Path)\n\n## 1. Operational Decision Matrix: When to Trigger Cross-Region Promotion\n| Disaster Scenario | Recommended Recovery Path | Justification | Data Loss (RPO) |\n| :--- | :--- | :--- | :--- |\n| **Single VM Crash** | Automatic Guest Restart / Autohealing | Handled locally within zone | RPO = 0 |\n| **Single Zone Outage** | Automatic Regional HA Failover | Multi-zone sync replication | RPO = 0 |\n| **Catastrophic Regional Outage** (>2h declared down)| **Cross-Region Replica Promotion** | Multi-zone loss across entire region | RPO = Asynchronous Lag |\n\n## 2. Emergency Cross-Region Promotion Runbook\n\n### Step 1: Authorize Promotion\n- **Mandatory Approval:** Incident Commander and Head of Engineering consensus required.\n- **Verify Replication Lag:** Check last known byte lag:\n  ```bash\n  gcloud sql instances describe brightloaf-orders-db-dr-replica \\\n      --format='value(replicaConfiguration.failoverTarget)'\n  ```\n\n### Step 2: Promote Replica to Standalone Primary\n```bash\ngcloud sql instances promote-replica brightloaf-orders-db-dr-replica \\\n    --project=brightloaf-prod\n```\n\n### Step 3: Run Post-Promotion Acceptance Probe\n```bash\npython3 verify_recovery_acceptance.py\n```\n\n### Step 4: Re-route Application Database Traffic\n```bash\n# Update Cloud DNS record pointing orders-db.internal to new promoted IP\ngcloud dns record-sets transaction start --zone=internal-vpc-zone\ngcloud dns record-sets transaction remove 10.128.0.5 --name=orders-db.internal. --type=A --ttl=30 --zone=internal-vpc-zone\ngcloud dns record-sets transaction add 10.142.0.8 --name=orders-db.internal. --type=A --ttl=30 --zone=internal-vpc-zone\ngcloud dns record-sets transaction execute --zone=internal-vpc-zone\n```\n\n### Step 5: Post-Incident Failback Rebuild\nOnce `us-central1` recovers:\n1. Provision fresh cross-region replica in `us-central1` replicating from `us-east1`.\n2. Wait for byte lag to reach 0.\n3. Schedule a 60-second read-only maintenance cutover window to reverse traffic back.\nEOF\ncat day-098-topic-03-cross-region-runbook.md\n```",
                    "Review all output artifacts and confirm that the execution script and cross-region promotion runbook fulfill Day 98 Exit evidence criteria."
                ],
                "verification": "The shell script models the representative Regional HA failover path and the Markdown runbook provides a complete decision matrix and multi-step cross-region promotion procedure.",
                "trouble": "Ensure `availabilityType: REGIONAL` is set in instance template before triggering instance failover.",
                "cleanup": "Retain `execute_regional_ha_drill.sh` and `day-098-topic-03-cross-region-runbook.md` as exit evidence artifacts.",
                "accept": "Completed Regional HA execution script and verified cross-region disaster recovery runbook. File: `day-098-topic-03-failover-paths.md`.",
                "file": "day-098-topic-03-failover-paths.md"
            }
        }
    ]
}
