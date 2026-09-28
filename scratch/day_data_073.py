"""day_data_073.py — Exhaustive architecture data specification for Day 73.

Covers Data and Hybrid Architecture Vocabulary: OLTP vs OLAP, Lakes vs Lakehouses,
Batch vs Streaming, Watermarks, Data Mesh, and Dataplex Governance.
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 73

DATA = {
    "day": 73,
    "part1_intro": (
        "Day 73 establishes the architectural vocabulary, storage physics, and organizational boundaries required to "
        "engineer enterprise data platforms on Google Cloud. Moving beyond marketing taxonomy, this session explores "
        "the mechanical differences between row-oriented transactional persistence (Cloud SQL OLTP) and columnar "
        "analytical engines (BigQuery OLAP). Architects examine the mathematical boundaries of streaming systems—unbounded "
        "event streams, processing time vs event time, watermarks, and allowed lateness—alongside the organizational shift "
        "to Data Mesh, domain data contracts, and automated governance with Google Cloud Dataplex. Through rigorous trade-off "
        "matrices and real-world failure postmortems, engineers learn to prevent analytical queries from destabilizing core "
        "transactional systems and eliminate unannounced upstream schema breakages."
    ),
    "exit_summary": (
        "Constructed an end-to-end data flow topology separating OLTP transactions from an analytical lakehouse via "
        "Datastream CDC; established event-time watermarking policies for late-arriving events; published formal JSON Schema "
        "data contracts with Dataplex data quality rules; verified pipeline resiliency with automated Python test runners."
    ),
    "part2_intro": (
        "Modern cloud data systems require strict segregation of operational workloads from analytical compute. The sections "
        "below analyze the storage thermodynamics, distributed stream processing mechanics, orchestration architectures, "
        "and governance contracts that ensure data reliability at scale."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Architectural Paradigm</th>
      <th>Primary Google Cloud Primitive</th>
      <th>Underlying Storage &amp; Compute Format</th>
      <th>Consistency &amp; Latency Profile</th>
      <th>Primary Anti-Pattern / Failure Mode</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Operational Database (OLTP)</strong></td>
      <td>Cloud SQL for PostgreSQL / AlloyDB</td>
      <td>Row-oriented, B-Tree indexed on Persistent Disk</td>
      <td>Strict ACID; sub-10ms transactional writes</td>
      <td>Running unindexed analytical JOINs locking tables</td>
    </tr>
    <tr>
      <td><strong>Data Lake Storage</strong></td>
      <td>Cloud Storage (Multi-zone / Regional)</td>
      <td>Unstructured objects; raw JSON, Parquet, Avro, CSV</td>
      <td>Strong consistency; high-throughput streaming/batch</td>
      <td>Uncurated 'data swamp'; unversioned raw files</td>
    </tr>
    <tr>
      <td><strong>Analytical Warehouse (OLAP)</strong></td>
      <td>BigQuery (Dremel Engine)</td>
      <td>Capacitor columnar storage; partitioned &amp; clustered</td>
      <td>Strong read consistency; sub-second to minutes queries</td>
      <td>Unpartitioned full table scans scanning terabytes</td>
    </tr>
    <tr>
      <td><strong>Governed Lakehouse</strong></td>
      <td>BigLake + Dataplex</td>
      <td>Open formats (Parquet, Iceberg, Delta) + metadata catalog</td>
      <td>Unified fine-grained access control across GCS &amp; BQ</td>
      <td>Bypassing central governance via direct GCS reads</td>
    </tr>
    <tr>
      <td><strong>Streaming Processing</strong></td>
      <td>Cloud Pub/Sub + Cloud Dataflow (Apache Beam)</td>
      <td>Unbounded memory windows; persistent state watermarks</td>
      <td>At-least-once / exactly-once; sub-second freshness</td>
      <td>Unbounded state growth from missing watermarks</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 73: End-to-End Enterprise Data Flow Topology",
        "desc": "Separation of transactional operations from analytical lakehouse consumption via CDC and event streaming.",
        "nodes": [
            ("OLTP Operations", "Cloud SQL Transactions\\n+ PostgreSQL WAL Engine"),
            ("CDC Ingestion", "Serverless Datastream\\n+ Pub/Sub Event Ingestion"),
            ("Stream / Batch Engine", "Cloud Dataflow Pipeline\\n+ Watermark Windowing"),
            ("Governed Lakehouse", "BigQuery & BigLake\\n+ Dataplex Data Contracts"),
        ],
        "caption": "Figure 73.1: Data lifecycle decoupling operational transactions from analytical lakehouse consumption."
    },
    "part3_intro": (
        "The following field cases analyze real-world production outages caused by data architecture misconfigurations. "
        "Each scenario includes quantitative failure metrics, diagnostic sequences, root cause postmortems, "
        "defensible remediations, and dual-lane failed/corrected architectural diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises provide production-grade, executable configurations and verification scripts for "
        "provisioning partitioned BigQuery tables, defining Datastream CDC architectures, modeling Apache Beam watermarks, "
        "and implementing JSON Schema data contracts with automated test runners."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Batch vs. Streaming, OLTP vs. OLAP, Data Lakehouse, and Event Time Physics",
            "overview": (
                "Decouple operational databases from analytical warehouses. Master the mechanics of Capacitor columnar storage, "
                "event-time watermarks, allowed lateness windows, and serverless Change Data Capture (CDC) with Datastream."
            ),
            "preview": (
                "An automated midnight inventory valuation report runs a multi-table JOIN directly against the production Cloud SQL "
                "primary database, saturating CPU and disk IOPS, and causing online customer checkouts to fail with HTTP 504 timeouts."
            ),
            "technical": (
                "#### 1. The Storage Thermodynamics of OLTP vs. OLAP Engines\n\n"
                "Operational (OLTP) and analytical (OLAP) databases serve diametrically opposed access profiles and hardware constraints:\n\n"
                "- **OLTP (Row-Oriented B-Tree Storage):** Relational engines like PostgreSQL on Cloud SQL store complete table rows "
                "contiguously in 8KB disk pages. This architecture optimizes for random point lookups and atomic multi-row updates "
                "(`UPDATE orders SET status = 'shipped' WHERE order_id = 91823`). However, when a query aggregates a single column across "
                "10 million rows (`SELECT sum(total_amount) FROM orders`), the engine must read every entire row into memory, loading "
                "gigabytes of irrelevant column data (addresses, text comments, metadata), exhausting I/O and CPU cache.\n\n"
                "- **OLAP (Columnar Capacitor Storage):** Google BigQuery stores data in a proprietary columnar format called **Capacitor**. "
                "Each column is stored, compressed, and encoded separately in Google's distributed Colossus file system. An aggregation "
                "query touches strictly the requested column bytes, achieving 100x compression ratios and scanning fractions of the data "
                "at multi-terabyte-per-second throughput via Dremel's massively parallel execution trees.\n\n"
                "#### 2. Event Time vs. Processing Time and Watermark Mechanics\n\n"
                "In distributed streaming architectures (Cloud Pub/Sub to Cloud Dataflow), understanding time semantics is critical:\n\n"
                "- **Event Time:** The exact moment when the business event occurred at the edge client or origin source (e.g. mobile checkout timestamp).\n"
                "- **Processing Time:** The local clock time of the cloud server or container that happens to execute the data processing step.\n\n"
                "Because network latency, mobile offline queues, and regional routing delays vary unpredictably, events arrive out of order. "
                "Apache Beam (Cloud Dataflow) introduces **Watermarks**—a monotonically increasing timestamp that represents the system's "
                "confidence that all data with an event timestamp earlier than the watermark has been observed. When computing 1-hour tumbling "
                "windows, the window cannot close until the watermark advances past the window boundary.\n\n"
                "- **Allowed Lateness:** What happens when an in-flight mobile event arrives after the watermark has passed? Streaming pipelines "
                "must define an **Allowed Lateness** window (e.g. 2 hours). Late data arriving within this window triggers an updated window "
                "emission; data arriving past the allowed lateness is dropped or redirected to a dead-letter queue (DLQ).\n\n"
                "#### 3. Change Data Capture (CDC) Mechanics with Datastream\n\n"
                "To move operational data from Cloud SQL into BigQuery without running heavy extraction queries, architects employ **Change Data "
                "Capture (CDC)**. Google Cloud **Datastream** reads the PostgreSQL Write-Ahead Log (WAL) or MySQL binary log asynchronously:\n\n"
                "  1. Datastream operates as an external replication subscriber using logical decoding plugins (`pgoutput` or `wal2json`).\n"
                "  2. Every committed `INSERT`, `UPDATE`, or `DELETE` transaction is streamed as a lightweight event payload to Cloud Storage or BigQuery.\n"
                "  3. Zero query load is placed on the primary database compute engine; transactional operations remain 100% unaffected.\n\n"
                "#### 4. The Modern Lakehouse: Cloud Storage, BigLake, and Open Table Formats\n\n"
                "A traditional data lake (Cloud Storage) offers low-cost, multi-petabyte object retention for raw JSON, CSV, and Parquet files, "
                "but lacks table-level access control, ACID transactions, and metadata consistency. The **Data Lakehouse** architecture "
                "combines the cheap scalability of object storage with the governance and ACID guarantees of a data warehouse:\n\n"
                "- **Google BigLake:** Extends BigQuery's storage engine and access governance directly over open table formats (Apache Iceberg, "
                "Delta Lake, Apache Hudi, Parquet) stored in Cloud Storage, AWS S3, and Azure ADLS without copying physical data.\n"
                "- **Fine-Grained Governance:** BigLake enforces column-level security, row-level filtering, and dynamic data masking via "
                "Google Cloud Dataplex, regardless of whether analysts query data through BigQuery SQL, Dataproc Spark, or external tools.\n\n"
                "#### 5. Architectural Trade-offs: Storage & Freshness Paradigms\n\n"
                "| Storage & Processing Paradigm | Primary GCP Primitive | Typical Data Freshness | Query / Processing Cost | Concurrency Limit | Optimal Business Use Case |\n"
                "|---|---|---|---|---|---|\n"
                "| **Operational OLTP Database** | Cloud SQL for PostgreSQL | Real-time (0 ms latency) | High compute/IOPS per query | 500 – 5,000 active connections | E-commerce shopping cart, user authentication, inventory state |\n"
                "| **Real-Time Event Stream** | Pub/Sub + Dataflow | Sub-second (< 2 seconds) | Continuous compute (hourly worker cost) | Millions of msgs/sec | Real-time fraud detection, live telemetry monitoring, dynamic pricing |\n"
                "| **Serverless CDC Ingestion** | Datastream to BigQuery | Near real-time (15 – 60 seconds) | Pay-per-GB processed (low) | Fully serverless managed | Operational database replication to warehouse for live reporting |\n"
                "| **Scheduled Batch Data Warehouse** | BigQuery (Scheduled Queries) | Hourly to Daily (1 – 24 hours) | Pay-per-TB scanned or slot-hours | 300 concurrent queries per project | Financial reconciliation, executive BI dashboards, ML model training |\n"
                "| **Governed Open Lakehouse** | BigLake on Cloud Storage | Minutes to Hours | Low storage + pay-per-query compute | Scales with query engine | Multi-engine analytics (Spark + SQL), multi-cloud data federation |\n"
            ),
            "questions": [
                "Why does running an analytical aggregation on a row-oriented database cause severe CPU and disk I/O exhaustion?",
                "What is the mathematical purpose of a streaming watermark in Apache Beam / Cloud Dataflow?",
                "How does Datastream Change Data Capture (CDC) extract database mutations without executing SQL SELECT queries?",
                "What architectural capabilities distinguish a modern BigLake lakehouse from a traditional Cloud Storage data lake?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/data-analytics",
            "reference_label": "Google Cloud Architecture Center: Smart analytics reference architecture",
            "scenario": {
                "scenario": (
                    "Every midnight at 00:00 UTC, Brightloaf's automated finance reconciliation and inventory valuation pipeline executes. "
                    "The business intelligence reporting service connects directly to the production Cloud SQL primary database using an "
                    "administrative connection pool. The report issues complex multi-table queries joining the `orders`, `order_items`, `customers`, "
                    "and `inventory_ledger` tables across 3 years of historical records without date partition boundaries. For 28 minutes, "
                    "the database CPU is pinned at 100%, disk read IOPS hit maximum throughput limits, and active database locks freeze the "
                    "transaction commit queue. Night-shift online shoppers attempting to checkout encounter HTTP 504 Gateway Timeout errors."
                ),
                "impact": (
                    "P1 recurring production outage occurring every midnight. 2,400 checkout transactions dropped nightly during the 30-minute "
                    "batch window. Estimated lost revenue: $165,000 over a two-week period. Customer complaints escalated to the executive team. "
                    "Cloud SQL replication to read replicas desynchronized by over 400 seconds, threatening regional disaster recovery."
                ),
                "constraints": (
                    "Eliminate all analytical query load from the production transactional database; ensure inventory reconciliation reports "
                    "complete in under 15 minutes; maintain near real-time data freshness (< 60 seconds) in analytics datasets."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect Cloud SQL Query Insights in Cloud Console; identify slow analytical query `SELECT ... FROM orders JOIN order_items ...` responsible for 88% of total database CPU consumption between 00:00 and 00:28 UTC.",
                    "Step 2: Check database lock contention using `pg_stat_activity`; observe 140 transactional `INSERT INTO orders` statements blocked in `waiting` state behind shared read table locks held by the BI reporting user.",
                    "Step 3: Review the BI tool connection configuration; discover JDBC string points directly to the Cloud SQL primary instance private IP rather than an analytical warehouse.",
                    "Step 4: Audit table partitioning; confirm Cloud SQL tables contain 18 million rows in single monolithic tables without partitioning or archive separation."
                ],
                "root": (
                    "Executing complex OLAP analytical queries directly against an OLTP production database couples analytical compute "
                    "demands to transactional order processing. The row-oriented database engine was forced to execute massive full table scans, "
                    "exhausting CPU and memory buffers and blocking transactional writes."
                ),
                "remediation_steps": [
                    "Step 1: Immediately deploy Google Cloud Datastream for serverless Change Data Capture (CDC), replicating the PostgreSQL WAL directly into BigQuery without query overhead.",
                    "Step 2: Create a curated BigQuery dataset (`brightloaf_analytics`) with date-partitioned and customer-clustered tables (`PARTITION BY DATE(order_timestamp) CLUSTER BY status, customer_id`).",
                    "Step 3: Repoint the midnight inventory valuation report to execute in BigQuery, leveraging Dremel's columnar query execution.",
                    "Step 4: Revoke read access permissions on the Cloud SQL primary instance from the BI reporting service account, enforcing strict workload separation."
                ],
                "verify": (
                    "Execute the midnight inventory reconciliation report against BigQuery. Confirm query completes in 18 seconds (down from "
                    "28 minutes), scans only 420 MB of data due to partition pruning, and primary Cloud SQL CPU remains below 20% throughout midnight."
                ),
                "residual": (
                    "Datastream CDC introduces an asynchronous replication lag of 15 to 45 seconds between transactional commits and warehouse "
                    "visibility; operational alerts requiring sub-second transaction validation must not query BigQuery."
                ),
                "diagram": (
                    "Midnight BI report queries Cloud SQL",
                    "Full table scan pins CPU at 100%",
                    "Checkout freezes, 504 timeouts ($165k lost)",
                    "Deploy Datastream CDC to BigQuery",
                    "Query runs in BigQuery (18s), OLTP untouched"
                ),
                "facts": "Midnight BI query ran against Cloud SQL primary; CPU hit 100% for 28 min; 2,400 checkouts timed out; $165k lost revenue.",
                "inference": "OLTP database engines are structurally unsuited for OLAP workloads; decoupling via CDC guarantees operational stability.",
                "expected": "Datastream streams WAL mutations to BigQuery; analytical queries complete in seconds without touching OLTP compute."
            },
            "lab": {
                "name": "Partitioned BigQuery Lakehouse Design and Watermark Simulation",
                "file": "day-073-lakehouse-design.md",
                "goal": "Design a BigQuery partitioned analytics table, model streaming event-time watermarks in Python, and verify query pruning.",
                "expected": "A complete BigQuery DDL schema, an executable Python watermark simulation script, and verified late-data routing output.",
                "mode": "offline architecture specification, SQL scripting, and Python development; no cloud resources billed",
                "prereq": "Day 72 event streaming fundamentals and Day 29 BigQuery DDL notes",
                "preflight": "Review BigQuery table partitioning documentation and Apache Beam streaming window semantics.",
                "steps": [
                    "Draft the end-to-end data pipeline architecture in `day-073-lakehouse-design.md`.",
                    "Write the production BigQuery DDL table specification with date-partitioning and clustering (`create_orders_fact.sql`):\n\n```sql\n-- create_orders_fact.sql\nCREATE TABLE `brightloaf_analytics.fact_orders` (\n  order_id STRING OPTIONS(description=\"Unique order UUID\"),\n  customer_id STRING OPTIONS(description=\"Customer UUID\"),\n  order_total NUMERIC OPTIONS(description=\"Total order price in USD\"),\n  status STRING OPTIONS(description=\"Order lifecycle state\"),\n  payment_method STRING OPTIONS(description=\"Payment token provider\"),\n  event_timestamp TIMESTAMP OPTIONS(description=\"Client event time\"),\n  ingestion_timestamp TIMESTAMP OPTIONS(description=\"Streaming ingestion time\")\n)\nPARTITION BY DATE(event_timestamp)\nCLUSTER BY status, customer_id\nOPTIONS(\n  partition_expiration_days=730,\n  description=\"Curated order analytics fact table partitioned by event date\"\n);\n```",
                    "Write an executable Python simulation modeling Apache Beam event-time watermarking and late-data handling (`watermark_sim.py`):\n\n```python\n# watermark_sim.py\n\nclass StreamingWindowProcessor:\n    def __init__(self, window_size_sec: int, allowed_lateness_sec: int):\n        self.window_size = window_size_sec\n        self.allowed_lateness = allowed_lateness_sec\n        self.windows = {}\n        self.late_dlq = []\n\n    def process_event(self, event_id: str, event_time: int, current_watermark: int):\n        # Check if event is too late to be incorporated\n        if event_time < (current_watermark - self.allowed_lateness):\n            self.late_dlq.append((event_id, event_time, 'EXCEEDED_ALLOWED_LATENESS'))\n            return 'DROPPED_TO_DLQ'\n        \n        # Assign to 10-second tumbling window\n        window_start = (event_time // self.window_size) * self.window_size\n        window_end = window_start + self.window_size\n        window_key = f\"[{window_start}-{window_end}]\"\n        \n        if window_key not in self.windows:\n            self.windows[window_key] = []\n        self.windows[window_key].append(event_id)\n        \n        if event_time < current_watermark:\n            return f'ACCEPTED_LATE_UPDATE_{window_key}'\n        return f'ACCEPTED_ON_TIME_{window_key}'\n\n# Configure processor: 10s windows, 5s allowed lateness\nprocessor = StreamingWindowProcessor(window_size_sec=10, allowed_lateness_sec=5)\n\n# Event 1: Event time 12, watermark 10 -> On-time for window [10-20]\nassert processor.process_event('evt_1', event_time=12, current_watermark=10) == 'ACCEPTED_ON_TIME_[10-20]'\n\n# Event 2: Watermark advances to 22. Event arrives with event time 18 -> Late for window [10-20], but within allowed lateness (22 - 5 = 17 <= 18)\nassert processor.process_event('evt_2', event_time=18, current_watermark=22) == 'ACCEPTED_LATE_UPDATE_[10-20]'\n\n# Event 3: Event arrives with event time 14, watermark is 22 -> Late and outside allowed lateness (14 < 17) -> Dropped to DLQ\nassert processor.process_event('evt_3', event_time=14, current_watermark=22) == 'DROPPED_TO_DLQ'\nassert len(processor.late_dlq) == 1\nprint('Streaming Watermark and Allowed Lateness Simulation Verified Successfully.')\n```",
                    "Execute the Python watermark verification test:\n\n```sh\npython3 watermark_sim.py\n```"
                ],
                "verification": (
                    "Run automated watermark verification:\n\n```sh\npython3 -c \"import watermark_sim; print('Watermark Simulation Test Passed')\"\n```\n\nConfirm output displays `Streaming Watermark and Allowed Lateness Simulation Verified Successfully`."
                ),
                "trouble": (
                    "If events are dropped unexpectedly, verify that allowed lateness window accommodates expected network jitter."
                ),
                "cleanup": "No remote cloud resources created; retain SQL schemas and simulation scripts in repository.",
                "accept": "A validated BigQuery DDL schema with partitioning and clustering, and a verified Python streaming watermark simulation."
            }
        },
        {
            "key": "topic-02",
            "title": "Pipeline Orchestration, Data Mesh, and Dataplex Governance",
            "overview": (
                "Architect scalable data orchestration and cross-team data mesh governance. Compare Cloud Composer with Cloud Workflows, "
                "implement formal Data Contracts, and automate schema verification and data lineage with Google Cloud Dataplex."
            ),
            "preview": (
                "An upstream checkout developer renames a database column from `customer_zip` to `postal_code` on Friday afternoon; "
                "the overnight Airflow pipeline crashes silently, blinding Monday morning executive revenue dashboards."
            ),
            "technical": (
                "#### 1. The Data Mesh Paradigm: Moving from Monolith to Domains\n\n"
                "In traditional enterprise architectures, a centralized data engineering team is responsible for building and maintaining "
                "all ETL pipelines. As the organization grows, this central team becomes an acute bottleneck: they lack deep domain knowledge "
                "of application schemas, and upstream software developers modify databases without understanding downstream analytics impacts. "
                "**Data Mesh** decentralizes data ownership across four core sociotechnical principles:\n\n"
                "  1. **Domain-Oriented Ownership:** Decentralized domain teams (e.g. Checkout, Catalog, Logistics) own their analytical data "
                "assets as first-class software deliverables.\n"
                "  2. **Data as a Product:** Domain teams treat internal data consumers as customers, providing clean, curated, well-documented, "
                "and SLA-backed data products.\n"
                "  3. **Self-Serve Data Platform:** A centralized platform team provides shared cloud infrastructure (Cloud Composer, BigLake, "
                "Dataplex, CI/CD templates) so domain teams can publish data products autonomously.\n"
                "  4. **Federated Computational Governance:** Universal standards for data quality, encryption, security classification, and "
                "schema evolution are enforced programmatically across all domains.\n\n"
                "#### 2. Data Contracts: The Immutable API Boundary\n\n"
                "A **Data Contract** is a formally negotiated, version-controlled agreement between a data producer (e.g. the Checkout team) "
                "and data consumers (e.g. Financial Analytics, Machine Learning). A data contract defines:\n\n"
                "- **Schema Specification:** Explicit field names, data types, required constraints, and nullability (defined via JSON Schema, "
                "Protobuf, or Avro).\n"
                "- **Semantic Definitions:** Exact business meaning (e.g. 'order_total is net of discounts and exclusive of sales tax').\n"
                "- **Quality SLAs:** Freshness guarantees (e.g. updated within 15 minutes of hour end), volume thresholds, and completeness limits.\n"
                "- **Versioning & Evolution Policy:** Backward compatibility requirements and a mandatory 60-day deprecation notice for breaking changes.\n\n"
                "#### 3. Orchestration Architecture: Cloud Composer vs. Cloud Workflows\n\n"
                "Google Cloud provides two distinct workflow orchestration engines:\n\n"
                "- **Cloud Composer (Managed Apache Airflow):** Provisions a dedicated GKE cluster running Airflow webserver, schedulers, and Celery "
                "workers. Ideal for complex, multi-system Directed Acyclic Graphs (DAGs) requiring cross-database dependencies (e.g. Dataproc Spark "
                "jobs, BigQuery stored procedures, SFTP file extracts, and data quality assertions). High capability, but incurs a continuous baseline GKE cost.\n"
                "- **Cloud Workflows:** Fully managed, serverless, pay-per-step orchestration engine written in YAML. Scales to zero with sub-millisecond "
                "startup latency. Ideal for microservice coordination, event-driven pipelines (triggered by Eventarc), and transactional sagas. "
                "Zero operational infrastructure management.\n\n"
                "#### 4. Automated Governance and Lineage with Google Cloud Dataplex\n\n"
                "Google Cloud **Dataplex** unifies distributed data lakes and warehouses without moving physical bytes:\n\n"
                "- **Lakes and Zones:** Organizes Cloud Storage buckets and BigQuery datasets into logical business 'Lakes' (e.g. `ecommerce-lake`) "
                "divided into **Raw Zones** (landing uncurated files) and **Curated Zones** (cleaned, validated Parquet/BigQuery tables).\n"
                "- **Dataplex Auto Data Quality:** Executes automated serverless data quality rules (e.g. checking null percentage, regex patterns, "
                "uniqueness, and range bounds) on schedule, emitting Cloud Monitoring alerts when data drift violates contracts.\n"
                "- **Automated Data Lineage:** Tracks column-level transformations across BigQuery jobs, Cloud Dataflow pipelines, and Dataproc clusters, "
                "allowing architects to perform automated upstream/downstream impact analysis before modifying any table schema.\n\n"
                "#### 5. Architectural Trade-offs: Orchestration & Governance Primitives\n\n"
                "| Technology Primitive | Execution Model | Minimum Cost Footprint | Supported Dependency Complexity | Data Governance Integration | Best Suited For |\n"
                "|---|---|---|---|---|---|\n"
                "| **Cloud Composer (Airflow)** | Dedicated GKE Cluster | ~$350/month (small environment) | Complex multi-step DAGs with conditional branches | Native Dataplex & BigQuery operators | Enterprise batch ETL, multi-system data pipeline scheduling |\n"
                "| **Cloud Workflows** | Serverless Pay-per-Step | $0 baseline (scales to zero) | Linear / branching microservice steps | Integrates via REST APIs & Eventarc | Event-driven data ingestion, serverless microservice sagas |\n"
                "| **Cloud Tasks Queues** | Serverless Push Queue | Pay per operation (negligible) | Single task execution with retry policies | Built-in token-bucket rate limiting | Rate-limited worker dispatching, buffering third-party APIs |\n"
                "| **Dataplex Data Fabric** | Managed Metadata Plane | Pay per asset & scan | Declarative quality and discovery rules | Central IAM, metadata, and automated lineage | Cross-project data cataloging, automated quality enforcement |\n"
            ),
            "questions": [
                "What four sociotechnical principles define the Data Mesh architectural paradigm?",
                "How does an explicit Data Contract prevent upstream schema refactors from breaking downstream analytics?",
                "Under what operational conditions should an architect choose Cloud Workflows over Cloud Composer?",
                "How does Google Cloud Dataplex enforce uniform security and quality policies across Cloud Storage and BigQuery?",
            ],
            "reference": "https://docs.cloud.google.com/dataplex/docs/introduction",
            "reference_label": "Google Cloud Dataplex Documentation: Data fabric architecture and governance",
            "scenario": {
                "scenario": (
                    "During a Friday afternoon sprint cleanup, a frontend engineer on Brightloaf's checkout service refactored the order "
                    "submission JSON payload, renaming the field `customer_zip` to `postal_code` to align with a new international address "
                    "library. The change passed standard unit tests and was merged directly to production. The overnight Apache Airflow ETL "
                    "pipeline on Cloud Composer attempted to extract Sunday order records into the central BigQuery revenue dataset. The Airflow "
                    "Python task threw an unhandled `KeyError: 'customer_zip'`, failing silently without triggering a pager alert. On Monday "
                    "morning at 08:30, executive management opened the weekly revenue dashboard and observed zero reported revenue for the entire "
                    "weekend, causing emergency crisis meetings and accusations between engineering teams."
                ),
                "impact": (
                    "P1 operational blindness and reporting failure. Executive leadership lacked business visibility for 14 hours. Automated "
                    "marketing ad spend algorithms paused automatically due to presumed zero conversion, resulting in an estimated $95,000 "
                    "in missed sales. Cross-team trust between product development and analytics was severely fractured."
                ),
                "constraints": (
                    "Prevent unannounced breaking schema changes from ever reaching production; enforce automated schema validation in "
                    "CI/CD; alert data engineers within 10 minutes of any pipeline failure."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect Cloud Composer task execution logs; identify task failure with traceback `KeyError: 'customer_zip'` in `load_orders_to_warehouse`.",
                    "Step 2: Compare GitHub commit history for the checkout repository; locate Friday 16:15 commit renaming `customer_zip` to `postal_code` without notification to the data team.",
                    "Step 3: Review Airflow alerting configuration; discover DAG was configured with `email_on_failure: true` pointing to a decommissioned distribution list, with zero PagerDuty or Slack integration.",
                    "Step 4: Check schema governance tools; confirm zero schema registries, data contracts, or Dataplex data quality assertions were configured on the raw ingestion tables."
                ],
                "root": (
                    "Lack of formalized data contracts and cross-team schema governance allowed upstream producers to modify database interfaces "
                    "without validating downstream consumer compatibility. Missing operational alerting allowed a critical pipeline failure to "
                    "remain undetected for 14 hours."
                ),
                "remediation_steps": [
                    "Step 1: Publish a formal JSON Schema Data Contract (`order-placed-contract.json`) governing the order event interface, versioned in a centralized repository.",
                    "Step 2: Implement a pre-merge CI/CD pipeline check in the checkout repository using contract validation to fail builds if changes break existing schema contracts without a major version bump.",
                    "Step 3: Reconfigure Cloud Composer DAGs with SLA miss callbacks and PagerDuty notification webhooks, alerting on-call engineers within 5 minutes of task failure.",
                    "Step 4: Deploy Google Cloud Dataplex Auto Data Quality rules on the BigQuery raw orders dataset to validate column existence and nullability automatically on ingestion."
                ],
                "verify": (
                    "Simulate a breaking schema change in a staging branch by renaming a contract field. Verify that the CI/CD test runner "
                    "detects the contract violation, blocks the pull request merge, and outputs a clear deprecation guidance message."
                ),
                "residual": (
                    "Data contract versioning requires producer teams to support dual-version emission (both `customer_zip` and `postal_code`) "
                    "during a 60-day migration window, adding temporary maintenance overhead to the checkout codebase."
                ),
                "diagram": (
                    "Producer renames column on Friday",
                    "Downstream Airflow DAG fails (KeyError)",
                    "Dashboard shows $0 revenue for weekend",
                    "Enforce JSON Schema contract in CI/CD",
                    "Breaking schema blocked at pull request"
                ),
                "facts": "Column renamed from customer_zip to postal_code; Airflow DAG failed silently; dashboard showed $0 revenue for 14 hours; $95k missed sales.",
                "inference": "Directly coupling analytical extraction to raw internal schemas creates extreme fragility; data products must have published contracts.",
                "expected": "CI/CD contract validation blocks breaking schema changes before merge, preserving pipeline execution integrity."
            },
            "lab": {
                "name": "Data Contract Definition and Orchestration DAG Validation",
                "file": "day-073-data-contracts.md",
                "goal": "Write a formal Data Contract specification, author an Apache Airflow DAG with SLA alerting, and build a Python schema validator.",
                "expected": "A complete JSON Schema data contract, an Airflow DAG file with task dependencies, and an executable Python schema test runner.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 72 microservices and Day 14 Git/JSON practices",
                "preflight": "Review JSON Schema Draft 7 specifications and Apache Airflow DAG authoring best practices.",
                "steps": [
                    "Draft the Data Contract specification in `day-073-data-contracts.md` defining ownership, SLA, and schema requirements.",
                    "Create the production JSON Schema Data Contract (`order_placed_contract.json`):\n\n```json\n{\n  \"$schema\": \"http://json-schema.org/draft-07/schema#\",\n  \"title\": \"OrderPlacedContract\",\n  \"type\": \"object\",\n  \"properties\": {\n    \"order_id\": {\"type\": \"string\", \"pattern\": \"^[a-f0-9\\\\-]{36}$\"},\n    \"customer_id\": {\"type\": \"string\"},\n    \"order_total\": {\"type\": \"number\", \"minimum\": 0.01},\n    \"currency\": {\"type\": \"string\", \"enum\": [\"USD\", \"EUR\", \"GBP\"]},\n    \"customer_zip\": {\"type\": \"string\", \"minLength\": 3},\n    \"timestamp\": {\"type\": \"string\", \"format\": \"date-time\"}\n  },\n  \"required\": [\"order_id\", \"customer_id\", \"order_total\", \"currency\", \"customer_zip\", \"timestamp\"],\n  \"additionalProperties\": true\n}\n```",
                    "Write an Apache Airflow DAG specification with task dependencies and SLA callbacks (`order_pipeline_dag.py`):\n\n```python\n# order_pipeline_dag.py\nfrom datetime import datetime, timedelta\n\n# Emulated Airflow DAG specification for architectural validation\nclass DummyDAG:\n    def __init__(self, dag_id, schedule_interval, default_args):\n        self.dag_id = dag_id\n        self.schedule_interval = schedule_interval\n        self.default_args = default_args\n        self.tasks = []\n\n    def add_task(self, name, downstream=None):\n        self.tasks.append(name)\n\ndef on_sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_slas):\n    print(f\"[P1 ALERT] SLA Missed on DAG {dag}! Route to PagerDuty.\")\n\ndefault_args = {\n    'owner': 'data_platform_team',\n    'depends_on_past': False,\n    'retries': 3,\n    'retry_delay': timedelta(minutes=5),\n    'sla': timedelta(minutes=30)\n}\n\ndag = DummyDAG('brightloaf_order_reconciliation', '@daily', default_args)\nprint(f\"Airflow DAG {dag.dag_id} Initialized with 30-Minute SLA Guarantee.\")\n```",
                    "Write an automated Python schema contract verification script (`contract_validator.py`):\n\n```python\n# contract_validator.py\nimport json\n\ndef validate_order_payload(payload: dict, required_fields: list):\n    missing = [f for f in required_fields if f not in payload]\n    if missing:\n        raise ValueError(f\"Contract Violation! Missing required fields: {missing}\")\n    return True\n\nrequired = [\"order_id\", \"customer_id\", \"order_total\", \"currency\", \"customer_zip\", \"timestamp\"]\n\n# Test 1: Valid payload\nvalid_order = {\n    \"order_id\": \"d3b07384-d113-4632-a52d-8924194883ef\",\n    \"customer_id\": \"cust_9812\",\n    \"order_total\": 48.50,\n    \"currency\": \"USD\",\n    \"customer_zip\": \"94105\",\n    \"timestamp\": \"2026-09-28T12:00:00Z\"\n}\nassert validate_order_payload(valid_order, required) is True\n\n# Test 2: Breaking payload missing customer_zip\ninvalid_order = {\n    \"order_id\": \"d3b07384-d113-4632-a52d-8924194883ef\",\n    \"customer_id\": \"cust_9812\",\n    \"order_total\": 48.50,\n    \"currency\": \"USD\",\n    \"postal_code\": \"94105\", # Renamed field violates contract!\n    \"timestamp\": \"2026-09-28T12:00:00Z\"\n}\n\ntry:\n    validate_order_payload(invalid_order, required)\n    assert False, \"Validator should have rejected breaking change!\"\nexcept ValueError as e:\n    print(f\"Expected Contract Rejection: {e}\")\n\nprint(\"Data Contract Validation Logic Verified Successfully.\")\n```",
                    "Execute the Python contract validation test:\n\n```sh\npython3 contract_validator.py\n```"
                ],
                "verification": (
                    "Run automated contract validation test:\n\n```sh\npython3 -c \"import contract_validator; print('Contract Test Runner Passed')\"\n```\n\nConfirm output displays `Data Contract Validation Logic Verified Successfully`."
                ),
                "trouble": (
                    "If schema validation fails on valid payloads, verify that datetime strings follow ISO 8601 UTC format."
                ),
                "cleanup": "No remote cloud resources created; retain contract JSON files and validation scripts in repository.",
                "accept": "A validated JSON Schema Data Contract, Airflow DAG definition with SLA callbacks, and working Python contract validator."
            }
        }
    ]
}
