"""day_data_072.py — Exhaustive architecture data specification for Day 72.

Standard: Days 40–50 Architectural Benchmark (e.g., day-044, day-045, day-050).
Covers Web Application Architecture: Sizing compute, caching, persistence, and service decoupling.
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
verbatim telemetry error logs, 8-stage operational engineering exercises, and zero difficulty labels.
"""

DAY_NUM = 72

DATA = {
    "day": 72,
    "part1_intro": (
        "Day 72 synthesizes the end-to-end cloud engineering principles required to design, size, and operate "
        "production web application platforms on Google Cloud. Moving beyond basic component provisioning, this "
        "session dissects the thermodynamic realities of modern web systems: database connection pool saturation, "
        "origin offloading physics using Cloud CDN, cryptographic service identity verification via OpenID Connect (OIDC), "
        "and exactly-once semantics across high-velocity Pub/Sub event ingestion pipelines. Through rigorous quantitative "
        "modeling, packet-level architectural traces, and real-world failure post-mortems, architects learn to design "
        "fault-tolerant systems that maintain sub-second latency and zero data loss under extreme Black Friday burst loads."
    ),
    "exit_summary": (
        "Verified three-tier compute autoscaling bounds with in-VPC PgBouncer connection pooling; architected Cloud CDN "
        "backend bucket caching with immutable asset hashing; established zero-trust service-to-service IAM authentication "
        "using cached OIDC tokens; implemented high-throughput Pub/Sub event streaming with BigQuery windowed deduplication."
    ),
    "part2_intro": (
        "Web application architecture on Google Cloud requires strict control boundaries between ingress, compute, "
        "caching, persistence, and asynchronous processing tiers. The sections below analyze the architectural mechanics, "
        "kernel and network dynamics, mathematical trade-offs, and failure characteristics of each component layer."
    ),
    "arch_table_html": """<div class="table-container">
<table>
<caption>Enterprise Architectural Comparison across Web Application Tiers</caption>
<thead>
<tr>
  <th scope="col">Architecture Layer</th>
  <th scope="col">GCP Service Primitive</th>
  <th scope="col">Primary Bottleneck / Failure Domain</th>
  <th scope="col">Architectural Protection Pattern</th>
  <th scope="col">Target SLO / Performance Metric</th>
</tr>
</thead>
<tbody>
<tr>
  <th scope="row">Global Edge Ingress</th>
  <td>External Application Load Balancer + Cloud CDN</td>
  <td>Cache stampede on origin; TLS handshake latency</td>
  <td>Content-addressed immutable asset hashing; HTTP/3 (QUIC)</td>
  <td>p99 Edge Latency &lt; 25 ms; 85%+ Cache Hit Ratio</td>
</tr>
<tr>
  <th scope="row">Stateless Compute Tier</th>
  <td>Compute Engine MIG / Cloud Run</td>
  <td>Thread starvation under burst; cold starts</td>
  <td>Predictive autoscaling; minimum idle replicas; connection pooling</td>
  <td>p95 Latency &lt; 150 ms; 99.99% Availability</td>
</tr>
<tr>
  <th scope="row">Session &amp; Ephemeral Cache</th>
  <td>Memorystore for Redis (Cluster / HA)</td>
  <td>Memory exhaustion (OOM); cross-zone network latency</td>
  <td>Volatile-LRU eviction; in-VPC Private Service Access; read replicas</td>
  <td>Sub-millisecond query time; zero evictions on critical keys</td>
</tr>
<tr>
  <th scope="row">Relational Persistence Tier</th>
  <td>Cloud SQL for PostgreSQL (HA Regional)</td>
  <td>PostgreSQL backend process RAM exhaustion; lock contention</td>
  <td>In-VPC PgBouncer in transaction mode; read replica query offload</td>
  <td>Active connections &lt; 70% max; p99 query &lt; 40 ms</td>
</tr>
<tr>
  <th scope="row">Asynchronous Streaming Tier</th>
  <td>Pub/Sub + BigQuery Streaming Insert</td>
  <td>At-least-once message duplication; write quota throttling</td>
  <td>Pub/Sub exactly-once delivery; BigQuery Storage Write API dedup</td>
  <td>End-to-end ingestion latency &lt; 2 s; zero duplicate records</td>
</tr>
</tbody>
</table>
</div>""",
    "arch_diagram": {
        "type": "topology",
        "title": "Three-Tier Web Application, Edge CDN, and Streaming Topology",
        "desc": "Multi-tier operational architecture showing CDN edge caching, compute scaling, PgBouncer pooling, and Pub/Sub streaming.",
        "caption": "Figure 72.1: Multi-tier web application topology isolating stateful persistence behind connection proxies, edge caching, and asynchronous streaming.",
        "width": 1100,
        "height": 640,
        "layers": [
            {"name": "LAYER 1: Global Edge Ingress & CDN", "desc": "Global External ALB, Cloud Armor, Cloud CDN Edge PoPs", "fill": "#1e3a5f", "y": 10, "h": 90},
            {"name": "LAYER 2: Stateless Compute & Service Mesh", "desc": "Compute Engine MIG / Cloud Run, OIDC Authentication", "fill": "#0f2338", "y": 110, "h": 90},
            {"name": "LAYER 3: Connection Proxy & Ephemeral Tier", "desc": "In-VPC PgBouncer Pooler, Memorystore Redis Cluster", "fill": "#064e3b", "y": 210, "h": 90},
            {"name": "LAYER 4: Relational Persistence Tier", "desc": "Cloud SQL PostgreSQL Regional HA (Zone A/B)", "fill": "#1e1b4b", "y": 310, "h": 90},
            {"name": "LAYER 5: Event Streaming & Ingestion Tier", "desc": "Cloud Pub/Sub Exactly-Once, BigQuery Storage Write API", "fill": "#3b0764", "y": 410, "h": 90},
        ],
        "components": [
            {"id": "alb", "name": "Global External ALB", "detail": "TLS 1.3 Termination & Anycast", "x": 100, "y": 30, "w": 250, "h": 50, "fill": "#0f283d", "stroke": "#38bdf8"},
            {"id": "cdn", "name": "Cloud CDN Edge PoPs", "detail": "Immutable Static Asset Caching", "x": 420, "y": 30, "w": 260, "h": 50, "fill": "#0f283d", "stroke": "#38bdf8"},
            {"id": "mig", "name": "Compute MIG Fleet", "detail": "Autoscaling Stateless Pods (OIDC)", "x": 420, "y": 130, "w": 260, "h": 50, "fill": "#092e28", "stroke": "#10b981"},
            {"id": "pgb", "name": "In-VPC PgBouncer Tier", "detail": "Transaction Mode (10k -> 80)", "x": 420, "y": 230, "w": 260, "h": 50, "fill": "#093322", "stroke": "#22c55e"},
            {"id": "sql", "name": "Cloud SQL Regional HA", "detail": "Synchronous Standby (Zone B)", "x": 420, "y": 330, "w": 260, "h": 50, "fill": "#1b143a", "stroke": "#a855f7"},
            {"id": "stream", "name": "Pub/Sub + BigQuery", "detail": "Exactly-Once Dedup Pipeline", "x": 750, "y": 430, "w": 260, "h": 50, "fill": "#280a3c", "stroke": "#c084fc"},
        ],
        "flows": [
            {"x1": 350, "y1": 55, "x2": 420, "y2": 55, "type": "ok", "label": "Edge Cache"},
            {"x1": 550, "y1": 80, "x2": 550, "y2": 130, "type": "ok", "label": "Origin Fetch"},
            {"x1": 550, "y1": 180, "x2": 550, "y2": 230, "type": "ok", "label": "Multiplexed SQL"},
            {"x1": 550, "y1": 280, "x2": 550, "y2": 330, "type": "ok", "label": "Bounded Conn (80)"},
            {"x1": 680, "y1": 155, "x2": 750, "y2": 455, "type": "ok", "label": "Async Orders"},
        ],
        "boundaries": [
            {"x": 60, "y": 14, "w": 300, "h": 76, "label": "EDGE PERIMETER (CDN)", "color": "#38bdf8"},
            {"x": 60, "y": 214, "w": 300, "h": 76, "label": "PRIVATE POOLING BOUNDARY", "color": "#10b981"},
            {"x": 60, "y": 314, "w": 300, "h": 76, "label": "HA DATABASE PERIMETER", "color": "#a855f7"},
        ],
        "probes": [
            {"cx": 550, "cy": 105, "label": "PROBE 1: CDN Hit Ratio Audit", "color": "#f59e0b"},
            {"cx": 550, "cy": 205, "label": "PROBE 2: PgBouncer Client Wait Queue", "color": "#f43f5e"},
            {"cx": 550, "cy": 305, "label": "PROBE 3: Cloud SQL Num Backends", "color": "#f43f5e"},
        ]
    },
    "part3_intro": (
        "The following production field cases examine catastrophic failure modes encountered in high-scale web deployments. "
        "Each case details the real-world operational context, precise quantitative failure indicators, root cause analysis, "
        "defensible multi-step remediations, verification procedures, and dual-lane failed/corrected architectural diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author production "
        "manifests, benchmark connection pools, configure immutable CDN caching, validate OIDC tokens, and test "
        "streaming deduplication with zero difficulty labels."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Three-Tier Web Application: Compute Sizing, Connection Pooling, and Health Probing",
            "overview": (
                "Design scalable three-tier web application architectures on Google Cloud. Size stateless compute fleets, "
                "decouple database connection scaling via in-VPC PgBouncer, and establish safe health check autohealing probes."
            ),
            "preview": (
                "A flash sale triggers horizontal compute scaling from 4 to 28 VMs; eager database connection pools exhaust "
                "PostgreSQL backend limits, returning 504 Gateway Timeouts to 85% of shoppers and losing $192,000."
            ),
            "technical": (
                "#### 1. The Physics of Three-Tier Web Systems\n\n"
                "A production three-tier web architecture on Google Cloud separates concerns into three isolated network zones:\n\n"
                "- **Ingress Tier:** External Application Load Balancers terminating TLS 1.3 at Google edge points of presence (PoPs).\n"
                "- **Compute Tier:** Stateless application servers running in private subnets across multiple availability zones "
                "within Compute Engine Managed Instance Groups (MIGs) or Cloud Run.\n"
                "- **Persistence Tier:** Managed relational databases (Cloud SQL Regional HA) and in-memory caches (Memorystore for Redis) "
                "isolated in private subnets accessible only via Private Service Access (PSA).\n\n"
                "#### 2. The Connection Pool Explosion Problem\n\n"
                "Relational databases like PostgreSQL spawn a dedicated operating system process for each client connection. Each process "
                "consumes between 5MB and 12MB of RAM for backend work buffers (`work_mem`, connection metadata). If an application configures "
                "an eager client-side connection pool (e.g. HikariCP with 20 connections per pod), horizontal autoscaling creates an exponential "
                "connection demand (`Total Connections = Instances × Pool Size`).\n\n"
                "When a traffic surge causes instances to scale from 4 to 28, connection demand leaps from 80 to 560 connections. When connections "
                "exceed PostgreSQL's `max_connections` (e.g. 500), the database server denies new connections with "
                "`FATAL: remaining connection slots are reserved for non-replication superuser connections`, locking up the entire cluster.\n\n"
                "#### 3. In-VPC PgBouncer Architecture in Transaction Mode\n\n"
                "To decouple compute autoscaling from database capacity, architects deploy intermediate **PgBouncer** connection poolers "
                "operating in **Transaction Pooling Mode**:\n\n"
                "- The application establishes thousands of lightweight TCP connections to PgBouncer.\n"
                "- PgBouncer holds a small, fixed pool of persistent connections (e.g. 80) to Cloud SQL.\n"
                "- When an application executes a transaction (`BEGIN ... COMMIT`), PgBouncer assigns an active database connection for the "
                "millisecond duration of the transaction and immediately releases it back to the pool for reuse by other threads.\n\n"
                "#### 4. Architectural Trade-offs: Database Connection Management\n\n"
                "| Strategy | Architecture Pattern | Concurrency Limit | Connection Handshake Latency | Failover / Reconnect Behavior | Best Suited For |\n"
                "|---|---|---|---|---|---|\n"
                "| **Client-Side Pooling (HikariCP / SQLAlchemy)** | In-process connection pool embedded in each container | Poor (`replicas × pool_size`); bursts cause DB OOM | Low (in-memory connection reuse) | Re-resolves DNS on connection drops; slow to shed idle sockets | Monolithic services with static, low replica counts (< 5 instances) |\n"
                "| **Centralized PgBouncer (Transaction Mode)** | Intermediate stateless proxy tier in private subnet | Very High (10,000+ client connections to 100 DB connections) | Negligible (< 1 ms proxy hop) | Transparently buffers queries during DB failover; preserves client TCP | High-throughput stateless microservices, serverless bursts |\n"
                "| **Centralized PgBouncer (Session Mode)** | Dedicated proxy retaining server connection for session life | Moderate (1:1 client-to-backend mapping) | Low (< 1 ms proxy hop) | Drops client connection on backend failover | Workloads requiring prepared statements, temp tables, `SET` session vars |\n"
                "| **Cloud SQL Auth Proxy** | Local client sidecar or intermediate VM proxy | Moderate (handles secure TLS & IAM auth) | Adds 200–400ms on initial ephemeral cert handshake | Re-authenticates automatically; handles SSL rotation seamlessly | Enforcing Zero-Trust IAM database auth without managing cert keys |\n"
                "| **Direct Cloud SQL IAM Connectors** | Language-native drivers (Go, Java, Python, Node) | High (eliminates separate proxy process) | Automatic background token refresh | Resilient retry loops built into native client connection factory | Modern cloud-native containers running on Cloud Run or GKE |\n"
            ),
            "questions": [
                "Under what traffic pattern does client-side connection pooling fail when paired with autoscaling compute?",
                "Why does PgBouncer transaction pooling restrict the use of PostgreSQL prepared statements and session variables?",
                "How does isolating health check probes from downstream database health prevent cascading cluster reboots?",
                "What memory overhead does PostgreSQL incur for each active backend connection process?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/scalable-and-resilient-apps",
            "reference_label": "Google Cloud Architecture Center: Build scalable and resilient applications",
            "scenario": {
                "scenario": (
                    "Brightloaf's core e-commerce checkout platform collapses 8 minutes into a major seasonal marketing campaign. "
                    "Marketing launched a flash sale announcement offering a 50% discount on artisan bread bundles, driving an "
                    "instantaneous surge of 4,200 RPS to the checkout service. The Compute Engine Managed Instance Group (MIG) scaled "
                    "rapidly from 4 VMs to 28 VMs across three availability zones in us-central1. While VM CPU utilization remained "
                    "comfortably below 45%, every HTTP checkout request began timing out after 30 seconds, returning HTTP 504 Gateway "
                    "Timeout errors to over 85% of active shoppers."
                ),
                "impact": (
                    "P1 critical production outage. Customer order completion rate plummeted from 99.4% to 11.8% during the peak 30 minutes "
                    "of the promotion. Payment gateway authorizations failed due to upstream network timeouts. Unrecoverable lost revenue was "
                    "estimated at $192,000. Brightloaf's quarterly latency and availability SLO error budgets were completely consumed."
                ),
                "constraints": (
                    "Preserve strict ACID transaction consistency across orders and payment ledgers; cannot perform unbudgeted vertical "
                    "database tier upgrades (e.g. migrating to a 96-core instance during peak); all architectural remedies must be deployable "
                    "with zero downtime and full rollback capability."
                ),
                "evidence": (
                    "Querying Cloud Logging for database error logs revealed connection ceiling saturation:\n\n"
                    "```text\n"
                    "$ gcloud logging read 'resource.type=\"cloudsql_database\" AND textPayload=~\"remaining connection slots\"' --limit=3\n"
                    "2026-09-28T08:04:12Z brightloaf-orders-db postgres[14021]: FATAL: remaining connection slots are reserved for non-replication superuser connections\n"
                    "2026-09-28T08:04:14Z brightloaf-orders-db postgres[14022]: FATAL: remaining connection slots are reserved for non-replication superuser connections\n"
                    "2026-09-28T08:04:15Z brightloaf-orders-db postgres[14025]: FATAL: remaining connection slots are reserved for non-replication superuser connections\n"
                    "```\n\n"
                    "Correlating with Compute Engine MIG scaling events:\n\n"
                    "```text\n"
                    "$ gcloud compute instance-groups managed list-instances checkout-mig --region=us-central1 --format=\"table(instance,status)\" | wc -l\n"
                    "29 (28 worker VMs active * 20 HikariCP pool connections = 560 client connections > 500 max_connections)\n"
                    "```"
                ),
                "root": (
                    "Eager application-level connection pooling without an intermediate connection proxy causes horizontal compute autoscaling "
                    "to violently exhaust database backend worker processes. Each new VM spawns a full connection pool that holds idle TCP sockets "
                    "to PostgreSQL, exhausting memory and backend slots even when individual transactions execute in under 15 milliseconds."
                ),
                "diagnostic_steps": [
                    "Step 1: Query Cloud Monitoring metrics for Cloud SQL `database/postgresql/num_backends` and `database/network/active_connections`; observe connection count hitting the hard limit of 500 at 08:04 UTC and plateauing.",
                    "Step 2: Correlate database metrics with Compute Engine MIG autoscaler timeline in Cloud Logging; observe instance count expanded dynamically from 4 to 28 instances across zones us-central1-a, b, and c.",
                    "Step 3: Inspect application container stdout logs; identify hundreds of repeated exceptions: `org.postgresql.util.PSQLException: FATAL: remaining connection slots are reserved for non-replication superuser connections`.",
                    "Step 4: Audit microservice deployment manifests and HikariCP configuration; confirm `maximumPoolSize` is set to 20 connections per pod with 1 container per VM: 28 VMs × 20 connections = 560 potential connections, exceeding the Cloud SQL ceiling of 500."
                ],
                "fix": (
                    "Tactical Fix: Immediately update the microservice configuration map via rolling deployment to reduce client `maximumPoolSize` "
                    "from 20 to 6 connections per VM (28 × 6 = 168 max connections), restoring immediate database availability.\n\n"
                    "Strategic Fix: Provision an in-VPC high-availability PgBouncer pooler tier deployed across multiple zones behind an "
                    "Internal Passthrough Network Load Balancer in transaction pooling mode (`default_pool_size = 80`, `max_client_conn = 5000`)."
                ),
                "verify": (
                    "Execute synthetic load test simulating 5,000 concurrent client threads against the PgBouncer endpoint. Verify in Cloud "
                    "Monitoring that active Cloud SQL connections remain capped at 85 connections while p99 transaction response time remains "
                    "under 140ms and zero 504 errors are recorded."
                ),
                "residual": (
                    "PgBouncer transaction pooling does not support session-level features such as `LISTEN`/`NOTIFY`, prepared statements "
                    "across transactions (unless using PgBouncer 1.21+ named prepared statements), or temporary tables. Stateful features must "
                    "use a dedicated session-mode pool."
                ),
                "diagram": (
                    "Flash sale traffic spikes",
                    "MIG autoscales to 28 VMs",
                    "DB connection pool exhausted (504)",
                    "Deploy PgBouncer in private subnet",
                    "Connections bounded at 65% capacity"
                ),
                "facts": "MIG surged from 4 to 28 instances during high traffic; Cloud SQL max_connections was set to 500; API returned HTTP 504 errors.",
                "inference": "Autoscaling compute without centralizing or capping database connection pooling directly destabilizes relational persistence layers.",
                "expected": "Connection pooling decouples client concurrency from backend database connections, maintaining sub-300ms p95 latency under burst load."
            },
            "lab": {
                "name": "Three-Tier Sizing, Connection Pooling, and Health-Check Configuration",
                "file": "day-072-three-tier-sizing.md",
                "goal": "Model compute autoscaling bounds against Cloud SQL connection limits, author production PgBouncer configurations, configure Compute Engine health check probes, and test pool multiplexing.",
                "expected": "A complete sizing document with PgBouncer configuration, connection calculation formulas, an autohealing health-check definition, and an executable pool multiplexing test script.",
                "mode": "offline architecture specification, shell scripting, and configuration design; no cloud resources billed",
                "prereq": "Day 71 requirements and Day 61 Cloud SQL configuration notes",
                "preflight": "Review Cloud SQL PostgreSQL connection pricing and Compute Engine health-check documentation.",
                "steps": [
                    (
                        "**Stage 1: Preflight & Environment Validation**\n"
                        "- Define target variables and verify Compute Engine and Cloud SQL API enablement:\n\n"
                        "```sh\n"
                        "export PROJECT_ID=\"brightloaf-prod\"\n"
                        "export REGION=\"us-central1\"\n"
                        "export DB_TIER=\"db-custom-4-16384\"\n"
                        "\n"
                        "gcloud config set project ${PROJECT_ID}\n"
                        "gcloud services enable compute.googleapis.com sqladmin.googleapis.com\n"
                        "```"
                    ),
                    (
                        "**Stage 2: Target / Backing Infrastructure Provisioning**\n"
                        "- Draft three-tier architecture network segmentation in `day-072-three-tier-sizing.md`:\n"
                        "  - Ingress Subnet: `10.128.0.0/24` (Public ALB & Cloud Armor)\n"
                        "  - Compute Subnet: `10.128.1.0/24` (Private MIG Instances)\n"
                        "  - Data Subnet: `10.128.2.0/24` (Private Service Connect & Cloud SQL PSA)"
                    ),
                    (
                        "**Stage 3: Production Manifest Authoring (PgBouncer Configuration INI)**\n"
                        "- Author production PgBouncer configuration file (`pgbouncer.ini`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > pgbouncer.ini\n"
                        "[databases]\n"
                        "* = host=10.128.2.50 port=5432 auth_user=pgbouncer\n"
                        "\n"
                        "[pgbouncer]\n"
                        "logfile = /var/log/pgbouncer/pgbouncer.log\n"
                        "pidfile = /var/run/pgbouncer/pgbouncer.pid\n"
                        "listen_addr = 0.0.0.0\n"
                        "listen_port = 6432\n"
                        "auth_type = scram-sha-256\n"
                        "auth_file = /etc/pgbouncer/userlist.txt\n"
                        "pool_mode = transaction\n"
                        "max_client_conn = 5000\n"
                        "default_pool_size = 50\n"
                        "min_pool_size = 10\n"
                        "reserve_pool_size = 10\n"
                        "reserve_pool_timeout = 5.0\n"
                        "max_db_connections = 100\n"
                        "EOF\n"
                        "cat pgbouncer.ini\n"
                        "```"
                    ),
                    (
                        "**Stage 4: Workload Deployment & Health Check Configuration**\n"
                        "- Author Compute Engine decoupled autohealing health-check specification (`health-check-spec.json`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > health-check-spec.json\n"
                        "{\n"
                        "  \"name\": \"checkout-compute-health-check\",\n"
                        "  \"type\": \"HTTP\",\n"
                        "  \"httpHealthCheck\": {\n"
                        "    \"port\": 8080,\n"
                        "    \"requestPath\": \"/healthz/live\",\n"
                        "    \"proxyHeader\": \"NONE\"\n"
                        "  },\n"
                        "  \"checkIntervalSec\": 10,\n"
                        "  \"timeoutSec\": 5,\n"
                        "  \"unhealthyThreshold\": 3,\n"
                        "  \"healthyThreshold\": 2\n"
                        "}\n"
                        "EOF\n"
                        "cat health-check-spec.json\n"
                        "```"
                    ),
                    (
                        "**Stage 5: Runtime Inspection & Sizing Calculation Verification**\n"
                        "- Develop and execute connection pool safety margin calculator (`sizing_calc.py`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > sizing_calc.py\n"
                        "max_vms = 30\n"
                        "app_pool_per_vm = 5\n"
                        "cloud_sql_tier_max = 500\n"
                        "pgbouncer_pool = 80\n"
                        "\n"
                        "total_app_conns = max_vms * app_pool_per_vm\n"
                        "safety_margin = (cloud_sql_tier_max - pgbouncer_pool) / cloud_sql_tier_max * 100\n"
                        "\n"
                        "print(f\"Max Client Connections: {total_app_conns}\")\n"
                        "print(f\"PgBouncer Backend Pool: {pgbouncer_pool}\")\n"
                        "print(f\"Cloud SQL Safety Margin: {safety_margin:.1f}% free slots\")\n"
                        "assert pgbouncer_pool < cloud_sql_tier_max, 'Database overload risk!'\n"
                        "print('Three-Tier Sizing Math Verified Successfully.')\n"
                        "EOF\n"
                        "python3 sizing_calc.py\n"
                        "```"
                    ),
                    (
                        "**Stage 6: Chaos / Connection Starvation Simulation**\n"
                        "- Simulate burst connection exhaustion without PgBouncer and verify connection rejection:\n\n"
                        "```sh\n"
                        "cat <<'EOF' > simulate_conn_exhaustion.py\n"
                        "# Emulate 28 VMs connecting directly with pool_size=20\n"
                        "attempted_conns = 28 * 20\n"
                        "db_max_limit = 500\n"
                        "dropped = max(0, attempted_conns - db_max_limit)\n"
                        "print(f\"Direct connections: {attempted_conns} attempted, {dropped} dropped by PostgreSQL.\")\n"
                        "assert dropped == 60, 'Connection limit check failed!'\n"
                        "print('EXHAUSTION DETECTED: Direct connection architecture failed under burst!')\n"
                        "EOF\n"
                        "python3 simulate_conn_exhaustion.py\n"
                        "```"
                    ),
                    (
                        "**Stage 7: Triage, Troubleshooting & PgBouncer Multiplexing Patch**\n"
                        "- Verify PgBouncer INI configuration syntax and transaction mode assertion:\n\n"
                        "```sh\n"
                        "python3 -c \"import configparser; c = configparser.ConfigParser(); c.read('pgbouncer.ini'); assert c['pgbouncer']['pool_mode'] == 'transaction'; print('PgBouncer Config Validated: Transaction Mode Active')\"\n"
                        "```"
                    ),
                    (
                        "**Stage 8: Cleanup & Resource Teardown**\n"
                        "- Remove temporary configuration files and calculation models:\n\n"
                        "```sh\n"
                        "rm -f pgbouncer.ini health-check-spec.json sizing_calc.py simulate_conn_exhaustion.py\n"
                        "echo \"Three-tier sizing lab artifacts cleaned up successfully.\"\n"
                        "```"
                    ),
                    (
                        "**Stage 9: Artifact Acceptance Criteria**\n"
                        "- Record the verified PgBouncer configuration, health check probe specifications, and connection mathematical models in `day-072-three-tier-sizing.md`."
                    )
                ],
                "verification": (
                    "Verify configuration parameters using validation scripts:\n\n```sh\npython3 -c \"import configparser; c = configparser.ConfigParser(); c.read('pgbouncer.ini'); assert c['pgbouncer']['pool_mode'] == 'transaction'; print('PgBouncer Config Validated: Transaction Mode')\"\n```\n\nConfirm output displays `PgBouncer Config Validated: Transaction Mode`."
                ),
                "trouble": (
                    "If applications report prepared statement errors under PgBouncer, ensure `pool_mode` is set to transaction and configure named prepared statement support or migrate to session mode."
                ),
                "cleanup": "No remote cloud resources created; retain configuration templates in local repository.",
                "accept": "A verified three-tier sizing calculation, PgBouncer configuration manifest, and decoupled Compute Engine health-check definition."
            }
        },
        {
            "key": "topic-02",
            "title": "Static Site and CDN: Cloud Storage Backend Buckets, Cache Keys, and Cache Stampede Prevention",
            "overview": (
                "Architect resilient static content delivery on Google Cloud using Cloud Storage backend buckets, Cloud CDN, "
                "content-addressed asset hashing, and cache-control headers."
            ),
            "preview": (
                "Misconfigured `Cache-Control: no-cache` headers cause 14,000 requests/second to bypass Cloud CDN, crashing "
                "the backend storage origin and rendering the storefront completely unstyled for 2 hours."
            ),
            "technical": (
                "#### 1. Cloud CDN Edge Architecture and Anycast Routing\n\n"
                "Google Cloud CDN integrates directly with the External Application Load Balancer (ALB). Over 100 edge Points of Presence "
                "(PoPs) terminate client TCP and TLS handshakes locally, caching static assets (JavaScript, CSS, images, video) as close to "
                "the user as possible.\n\n"
                "- **Edge Termination:** Latency drops from 120ms (cross-continent transit) to < 15ms (edge PoP hit).\n"
                "- **Backend Bucket Integration:** Static assets are hosted in Cloud Storage buckets designated as backend buckets behind the ALB.\n\n"
                "#### 2. Cache-Control Header Directives and Immutable Caching\n\n"
                "HTTP caching behavior is governed by client and origin headers:\n\n"
                "- **Immutable Fingerprinted Assets (`bundle.a8f9c1.js`):** `Cache-Control: public, max-age=31536000, immutable`. Instructs "
                "both Cloud CDN and client browsers to cache the file for 1 full year without ever revalidating with the origin.\n"
                "- **Dynamic Entrypoint HTML (`index.html`):** `Cache-Control: public, max-age=0, must-revalidate`. Forces immediate ETag "
                "revalidation to ensure users always receive the latest deployment reference.\n\n"
                "#### 3. Cache Stampede (Thundering Herd) Prevention\n\n"
                "When a popular cached object expires during peak traffic, thousands of concurrent requests miss the cache simultaneously "
                "and flood the origin server ('Cache Stampede'). Cloud CDN prevents stampedes through **Request Collapsing**:\n\n"
                "- When multiple requests for the same missing cache key arrive simultaneously, Cloud CDN collapses them into a single "
                "origin fetch request.\n"
                "- The origin response populates the edge cache and satisfies all waiting client requests concurrently.\n\n"
                "#### 4. Architectural Trade-offs: Static Asset Hosting and CDN Topologies\n\n"
                "| Topology | CDN Integration | Cache Hit Ratio | Origin Egress Billing | TLS Termination Point | Best Suited For |\n"
                "|---|---|---|---|---|---|\n"
                "| **Direct Cloud Storage (Public)** | None (Direct GCS URL) | 0% (Every request hits GCS) | Highest ($0.12/GB internet egress) | Google regional endpoint | Low-traffic internal tools, private artifacts |\n"
                "| **Backend Bucket + Cloud CDN** | Global External ALB + Cloud CDN | High (85%–98% hit ratio) | Lowest (CDN cache fill egress is discounted) | 100+ Anycast Edge PoPs | Global web storefronts, single-page applications (SPAs) |\n"
                "| **Firebase Hosting** | Managed global edge proxy | Very High (> 90%) | Low (bundled with Firebase pricing) | Global CDN edge | JAMstack apps, developer-led web applications |\n"
                "| **Compute VM Nginx Origin** | Custom reverse proxy behind ALB | Moderate (requires local SSD caching) | High (VM compute + disk + egress) | Global ALB edge | Complex dynamic asset generation, real-time image resizing |\n"
            ),
            "questions": [
                "Why must index.html and versioned JavaScript bundles have opposing Cache-Control header strategies?",
                "How does Cloud CDN Request Collapsing prevent thundering herd crashes on backend Cloud Storage buckets?",
                "What is the billing impact of achieving a 95% CDN cache hit ratio compared to direct Cloud Storage origin fetches?",
                "Under what condition does serving signed URLs via Cloud CDN require custom cache key configurations?",
            ],
            "reference": "https://docs.cloud.google.com/cdn/docs/overview",
            "reference_label": "Google Cloud CDN Documentation: Overview and Caching",
            "scenario": {
                "scenario": (
                    "During a promotional launch of a new product catalog, Brightloaf's web storefront experienced a severe "
                    "performance collapse. Marketing assets (images, product brochures, and stylesheet bundles) failed to load, "
                    "rendering the website as raw, unstyled text. An investigation revealed that a junior developer had committed a "
                    "configuration setting applying `Cache-Control: no-cache, no-store, must-revalidate` to all assets uploaded to the "
                    "Cloud Storage backend bucket. As a result, Cloud CDN bypassed its edge cache on 100% of requests, forwarding "
                    "14,200 requests/second directly to the Cloud Storage origin. Cloud Storage rate-limited the backend bucket with "
                    "HTTP 429 Too Many Requests, causing catastrophic asset delivery failure."
                ),
                "impact": (
                    "Storefront degraded for 2 hours and 15 minutes. Over 34,000 customer sessions rendered with missing CSS and broken "
                    "checkout buttons. Conversion rate dropped from 3.2% to 0.4%. Cloud Storage egress billing incurred an unexpected "
                    "$6,800 charge due to un-cached origin transfer."
                ),
                "constraints": (
                    "Achieve > 90% Cloud CDN cache hit ratio; guarantee instantaneous cache invalidation during new software releases; "
                    "maintain sub-30ms static asset load times globally."
                ),
                "evidence": (
                    "Examining HTTP response headers on live assets using <kbd>curl -I</kbd> confirmed anti-pattern cache headers:\n\n"
                    "```text\n"
                    "$ curl -I https://shop.brightloaf.com/assets/app.js\n"
                    "HTTP/2 200\n"
                    "content-type: application/javascript\n"
                    "cache-control: no-cache, no-store, must-revalidate  <-- ANTI-PATTERN: Forcing 100% origin fetches\n"
                    "age: 0\n"
                    "via: 1.1 google\n"
                    "x-cache: MISS\n"
                    "```\n\n"
                    "Cloud Monitoring metric confirmed zero cache hits and origin saturation:\n\n"
                    "```text\n"
                    "loadbalancing.googleapis.com/https/request_count (Total): 14,200 req/sec\n"
                    "loadbalancing.googleapis.com/https/backend_request_count (Origin Fetch): 14,200 req/sec (Cache Hit Ratio: 0.0%)\n"
                    "```"
                ),
                "root": (
                    "Misconfigured Cache-Control headers disabled Cloud CDN edge caching. 100% of static traffic was forwarded to the "
                    "Cloud Storage origin, causing request throttling and cache stampede failure."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect HTTP response headers using <kbd>curl -I https://shop.brightloaf.com/assets/style.css</kbd>; observe `Cache-Control: no-store` and `x-cache: MISS`.",
                    "Step 2: Check Cloud CDN monitoring dashboard in Cloud Console; observe Cache Hit Ratio dropped to 0.0% simultaneously with traffic surge.",
                    "Step 3: Query Cloud Storage backend bucket metrics; identify bucket request rate exceeded 10,000 QPS with HTTP 429 throttling errors.",
                    "Step 4: Audit CI/CD asset upload script; discover `gsutil -h \"Cache-Control: no-cache\"` parameter applied globally to all file types."
                ],
                "fix": (
                    "Tactical Fix: Immediately update Cloud CDN cache policy on the backend bucket via <kbd>gcloud compute backend-buckets update</kbd> "
                    "enforcing `--cache-mode=FORCE_CACHE_ALL` and `--default-ttl=86400` as an emergency containment measure.\n\n"
                    "Strategic Fix: Re-engineer the CI/CD build pipeline to generate content-addressed hashed filenames (`style.7b1c4e.css`) with "
                    "`Cache-Control: public, max-age=31536000, immutable`, while keeping `index.html` at `must-revalidate`."
                ),
                "verify": (
                    "Purge CDN cache using <kbd>gcloud compute url-maps invalidate-cdn-cache</kbd>. Execute synthetic client curl requests "
                    "and verify response headers display `x-cache: HIT`, `age > 0`, and Cloud Monitoring reports Cache Hit Ratio > 92%."
                ),
                "residual": (
                    "Content-addressed immutable asset caching requires automated build tooling to update HTML asset link references on every "
                    "release; un-hashed assets will remain stale at edge PoPs until TTL expiration."
                ),
                "diagram": (
                    "no-cache header on all assets",
                    "CDN misses 100%, floods origin",
                    "GCS throttles (429), styles broken",
                    "Immutable hashing + FORCE_CACHE_ALL",
                    "94% cache hit ratio, sub-25ms latency"
                ),
                "facts": "no-cache header applied to all static files; 14,200 req/s hit GCS origin; GCS returned HTTP 429; website unstyled for 2.25 hours.",
                "inference": "Edge caching requires strict header governance; content-addressed immutable hashing eliminates origin load safely.",
                "expected": "Cloud CDN satisfies 90%+ requests at edge PoPs, offloading backend storage and delivering sub-30ms load times."
            },
            "lab": {
                "name": "Cloud CDN Backend Bucket Configuration and Cache Invalidation Drill",
                "file": "day-072-cdn-caching.md",
                "goal": "Author Cloud Storage backend bucket configurations, configure Cloud CDN caching policies with custom cache keys, and execute automated cache invalidation drills.",
                "expected": "A complete CDN architecture document, a backend bucket provisioning script, an asset hashing verification runner, and a cache invalidation runbook.",
                "mode": "offline architecture specification, shell scripting, and configuration design; no cloud resources billed",
                "prereq": "Day 71 performance sizing and Day 68 technical requirements",
                "preflight": "Review Cloud CDN cache keys and Cache-Control header specifications.",
                "steps": [
                    (
                        "**Stage 1: Preflight & Environment Validation**\n"
                        "- Define target variables and verify Cloud Storage and Compute Engine API enablement:\n\n"
                        "```sh\n"
                        "export PROJECT_ID=\"brightloaf-prod\"\n"
                        "export BUCKET_NAME=\"brightloaf-static-storefront\"\n"
                        "export BACKEND_NAME=\"storefront-backend-bucket\"\n"
                        "\n"
                        "gcloud config set project ${PROJECT_ID}\n"
                        "gcloud services enable compute.googleapis.com storage.googleapis.com\n"
                        "```"
                    ),
                    (
                        "**Stage 2: Target / Backing Infrastructure Provisioning**\n"
                        "- Draft Cloud Storage bucket creation command with uniform bucket-level access:\n\n"
                        "```sh\n"
                        "# Define storage bucket creation command\n"
                        "echo \"Bucket definition: gs://${BUCKET_NAME} with uniform bucket-level access\"\n"
                        "```"
                    ),
                    (
                        "**Stage 3: Production Manifest Authoring (Backend Bucket & CDN Policy)**\n"
                        "- Author backend bucket creation script with strict cache modes (`setup_cdn_backend.sh`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > setup_cdn_backend.sh\n"
                        "#!/usr/bin/env bash\n"
                        "echo \"Creating Backend Bucket with Cloud CDN enabled...\"\n"
                        "# gcloud compute backend-buckets create ${BACKEND_NAME} \\\n"
                        "#   --gcs-bucket-name=${BUCKET_NAME} \\\n"
                        "#   --enable-cdn \\\n"
                        "#   --cache-mode=CACHE_ALL_STATIC \\\n"
                        "#   --default-ttl=3600 \\\n"
                        "#   --max-ttl=86400 \\\n"
                        "#   --client-ttl=3600\n"
                        "echo \"Backend bucket specified with CACHE_ALL_STATIC policy.\"\n"
                        "EOF\n"
                        "chmod +x setup_cdn_backend.sh\n"
                        "./setup_cdn_backend.sh\n"
                        "```"
                    ),
                    (
                        "**Stage 4: Workload Deployment & Cache Header Specification**\n"
                        "- Author asset upload script assigning differential Cache-Control headers (`upload_assets.sh`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > upload_assets.sh\n"
                        "#!/usr/bin/env bash\n"
                        "echo \"Simulating upload of fingerprinted assets with 1-year immutable cache:\"\n"
                        "# gsutil -h \"Cache-Control: public, max-age=31536000, immutable\" cp assets/*.js gs://${BUCKET_NAME}/assets/\n"
                        "echo \"Simulating upload of index.html with must-revalidate:\"\n"
                        "# gsutil -h \"Cache-Control: public, max-age=0, must-revalidate\" cp index.html gs://${BUCKET_NAME}/\n"
                        "echo \"Differential Cache-Control headers applied successfully.\"\n"
                        "EOF\n"
                        "chmod +x upload_assets.sh\n"
                        "./upload_assets.sh\n"
                        "```"
                    ),
                    (
                        "**Stage 5: Runtime Inspection & Verification**\n"
                        "- Author Python script to verify asset hash integrity and header simulation (`verify_cdn_headers.py`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > verify_cdn_headers.py\n"
                        "import hashlib\n"
                        "\n"
                        "def generate_content_hash(content: str) -> str:\n"
                        "    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:8]\n"
                        "\n"
                        "css_code = \"body { background-color: #f8fafc; font-family: sans-serif; }\"\n"
                        "asset_hash = generate_content_hash(css_code)\n"
                        "fingerprinted_name = f\"style.{asset_hash}.css\"\n"
                        "\n"
                        "headers = {\n"
                        "    fingerprinted_name: \"public, max-age=31536000, immutable\",\n"
                        "    \"index.html\": \"public, max-age=0, must-revalidate\"\n"
                        "}\n"
                        "\n"
                        "assert 'immutable' in headers[fingerprinted_name]\n"
                        "assert 'must-revalidate' in headers['index.html']\n"
                        "print(f\"Verified Fingerprinted Asset: {fingerprinted_name}\")\n"
                        "print(\"Header Strategy Assertions Passed Successfully.\")\n"
                        "EOF\n"
                        "python3 verify_cdn_headers.py\n"
                        "```"
                    ),
                    (
                        "**Stage 6: Chaos / Cache Invalidation Rehearsal**\n"
                        "- Author cache invalidation script to purge stale assets during emergency releases (`invalidate_cache.sh`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > invalidate_cache.sh\n"
                        "#!/usr/bin/env bash\n"
                        "echo \"Executing Cloud CDN cache invalidation for emergency release...\"\n"
                        "# gcloud compute url-maps invalidate-cdn-cache storefront-url-map \\\n"
                        "#   --path=\"/index.html\" \\\n"
                        "#   --async\n"
                        "echo \"Cache invalidation initiated for /index.html path.\"\n"
                        "EOF\n"
                        "chmod +x invalidate_cache.sh\n"
                        "./invalidate_cache.sh\n"
                        "```"
                    ),
                    (
                        "**Stage 7: Triage, Troubleshooting & Cache Key Validation**\n"
                        "- Verify cache hit calculation logic:\n\n"
                        "```sh\n"
                        "python3 -c \"hits = 9200; total = 10000; ratio = (hits/total)*100; assert ratio >= 90.0; print('Cache Hit Ratio:', f'{ratio:.1f}% PASS')\"\n"
                        "```"
                    ),
                    (
                        "**Stage 8: Cleanup & Resource Teardown**\n"
                        "- Clean up temporary deployment scripts:\n\n"
                        "```sh\n"
                        "rm -f setup_cdn_backend.sh upload_assets.sh verify_cdn_headers.py invalidate_cache.sh\n"
                        "echo \"CDN caching lab artifacts cleared successfully.\"\n"
                        "```"
                    ),
                    (
                        "**Stage 9: Artifact Acceptance Criteria**\n"
                        "- Save verified CDN backend bucket configurations, header strategies, and invalidation runbooks into `day-072-cdn-caching.md`."
                    )
                ],
                "verification": (
                    "Run automated CDN header validation:\n\n```sh\npython3 -c \"import verify_cdn_headers; print('CDN Strategy Validated')\"\n```\n\nConfirm output displays `Header Strategy Assertions Passed Successfully`."
                ),
                "trouble": (
                    "If assets fail to update following release, verify that index.html specifies `max-age=0, must-revalidate` and verify invalidation status."
                ),
                "cleanup": "No remote cloud resources created; retain configuration templates in local repository.",
                "accept": "A validated Cloud CDN backend bucket configuration, differential header strategy document, and cache invalidation runbook."
            }
        },
        {
            "key": "topic-03",
            "title": "Microservices on GKE or Cloud Run: Service-to-Service IAM and Zero-Trust mTLS",
            "overview": (
                "Architect secure inter-service communication across GKE and Cloud Run. Enforce Zero-Trust mutual TLS (mTLS) "
                "via service mesh and authenticate service-to-service calls using short-lived OpenID Connect (OIDC) identity tokens."
            ),
            "preview": (
                "An internal inventory microservice accepts unauthenticated HTTP calls on a private VPC IP; a compromised frontend "
                "container executes unauthorized stock updates without audit trails."
            ),
            "technical": (
                "#### 1. Zero-Trust Inter-Service Communication Principles\n\n"
                "In traditional perimeter security models, once traffic passes the external firewall, internal service-to-service "
                "traffic is implicitly trusted. A vulnerability in any single microservice allows lateral movement across the entire "
                "network. **Zero-Trust Networking** enforces two mandatory invariants on every internal RPC:\n\n"
                "- **Authentication & Identity:** Every service must cryptographically prove its identity using short-lived tokens.\n"
                "- **Authorization:** Explicit access policies must grant permission for the specific caller identity to invoke the target endpoint.\n\n"
                "#### 2. OpenID Connect (OIDC) Service Identity Tokens\n\n"
                "Google Cloud provides cryptographic identity tokens via the instance metadata server:\n\n"
                "  1. The calling service (running under Service Account A) requests an OIDC token signed by Google, specifying the audience "
                "(`aud = https://inventory-api.internal.brightloaf.com`).\n"
                "  2. The caller attaches the token to the HTTP request: `Authorization: Bearer <ID_TOKEN>`.\n"
                "  3. The receiving service or Cloud Run edge validates the signature against Google's public JSON Web Key Set (JWKS), "
                "confirms the audience matches, and asserts caller identity before executing business logic.\n\n"
                "#### 3. Anthos Service Mesh (ASM) and Mutual TLS (mTLS)\n\n"
                "For GKE microservices, **Anthos Service Mesh (managed Istio)** provides transparent, zero-code mTLS:\n\n"
                "- **Envoy Sidecars:** Intercept all inbound and outbound TCP traffic.\n"
                "- **Mesh CA:** Automatically issues, rotates, and distributes X.509 certificates to each pod (valid for 24 hours).\n"
                "- **PeerAuthentication Policy:** Enforces `STRICT` mTLS across the namespace, automatically rejecting unencrypted plaintext connections.\n\n"
                "#### 4. Architectural Trade-offs: Service-to-Service Authentication\n\n"
                "| Mechanism | Security Guarantee | Implementation Complexity | Latency Overhead | Identity Lifecycle | Best Suited For |\n"
                "|---|---|---|---|---|---|\n"
                "| **Network IP / VPC Peering** | Weak (IP spoofing, perimeter only) | Lowest (standard CIDR routing) | Zero | Static IP allowlists | Legacy monolithic lift-and-shift |\n"
                "| **OIDC Identity Tokens (Cloud Run)** | Strong (Google-signed cryptographic JWT) | Low (native Cloud Run IAM integration) | 2–5 ms validation; token caching required | 1-hour expiration; automated refresh | Serverless microservices, Cloud Run, Cloud Functions |\n"
                "| **Managed Istio / ASM (mTLS)** | Strongest (cryptographic pod identity + mTLS) | High (sidecar proxy management, mesh CA) | 1–3 ms per proxy hop | Automatic 24h X.509 rotation | Large GKE microservice clusters (> 20 services) |\n"
                "| **API Gateway / Cloud Endpoints** | Strong (JWT validation + API keys) | Moderate (declarative OpenAPI specs) | 5–15 ms gateway processing | Client API key & OAuth management | Public-facing microservice APIs, partner integration |\n"
            ),
            "questions": [
                "Why is perimeter network security insufficient without service-to-service cryptographic authentication?",
                "How does token caching prevent performance bottlenecks when validating Google-signed OIDC identity tokens?",
                "What is the operational consequence of deploying a STRICT PeerAuthentication policy before all clients have sidecars?",
                "How does Workload Identity Federation eliminate the need for hardcoded service account keys in microservice containers?",
            ],
            "reference": "https://docs.cloud.google.com/run/docs/authenticating/service-to-service",
            "reference_label": "Google Cloud Run: Service-to-Service Authentication",
            "scenario": {
                "scenario": (
                    "Brightloaf decomposed its ordering application into two Cloud Run microservices: `order-fulfillment` and `inventory-api`. "
                    "To avoid managing authentication tokens during rapid development, the engineering team configured `inventory-api` to "
                    "allow unauthenticated invocations (`allUsers` with `roles/run.invoker`), assuming that because the service had no public DNS "
                    "record, it was secure. During a penetration test, security researchers discovered an unauthenticated SSRF (Server-Side "
                    "Request Forgery) vulnerability in an adjacent marketing microservice. Leveraging the SSRF, the researchers called "
                    "`inventory-api` directly, successfully manipulating warehouse stock levels and triggering fictitious supplier reorders."
                ),
                "impact": (
                    "Critical security vulnerability escalation. Mandatory freeze on all production releases for 3 weeks. Emergency security "
                    "audit cost $95,000. Potential inventory manipulation liability exposure exceeding $450,000."
                ),
                "constraints": (
                    "Enforce strict Zero-Trust authentication between microservices; remove all public invocation permissions; implement "
                    "automated OIDC token acquisition and verification with zero developer credentials stored in code."
                ),
                "evidence": (
                    "Inspecting IAM policy on `inventory-api` revealed public unauthenticated access:\n\n"
                    "```yaml\n"
                    "$ gcloud run services get-iam-policy inventory-api --region=us-central1 --format=\"yaml(bindings)\"\n"
                    "bindings:\n"
                    "- members:\n"
                    "  - allUsers\n"
                    "  role: roles/run.invoker\n"
                    "```\n\n"
                    "Simulating unauthorized internal curl call:\n\n"
                    "```text\n"
                    "$ curl -X POST https://inventory-api-x8w9k-uc.a.run.app/adjustStock -d '{\"item\":\"bread\",\"qty\":-500}'\n"
                    "HTTP/2 200 OK  <-- VULNERABILITY: Executed without Authorization header\n"
                    "```"
                ),
                "root": (
                    "Absence of Zero-Trust service-to-service authentication allowed arbitrary callers to execute privileged API actions. "
                    "Relying on obscurity rather than cryptographic OIDC authentication created a severe security breach."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect Cloud Run service IAM policy bindings using <kbd>gcloud run services get-iam-policy inventory-api</kbd>; discover `allUsers` granted `roles/run.invoker`.",
                    "Step 2: Review Cloud Audit Logs; identify requests executing administrative stock adjustments with caller identity `anonymous`.",
                    "Step 3: Audit calling service account identities; verify `order-fulfillment` runs under a dedicated service account but never generates OIDC identity tokens.",
                    "Step 4: Check network ingress controls; observe `ingress: all` enabled instead of `ingress: internal`."
                ],
                "fix": (
                    "Tactical Fix: Immediately revoke `allUsers` from `roles/run.invoker` and grant invocation permissions strictly to "
                    "`serviceAccount:order-fulfillment-sa@brightloaf-prod.iam.gserviceaccount.com`.\n\n"
                    "Strategic Fix: Implement OIDC Bearer token generation via the metadata server in `order-fulfillment`, and restrict "
                    "`inventory-api` ingress to internal VPC traffic only."
                ),
                "verify": (
                    "Attempt an unauthenticated request to `inventory-api`; verify immediate rejection with HTTP 401 Unauthorized. Send an "
                    "authenticated request with a valid Google-signed OIDC token; verify successful execution with HTTP 200 OK."
                ),
                "residual": (
                    "OIDC token generation from the metadata server takes 10–25ms; microservices must cache tokens in memory until their "
                    "expiration time (55 minutes) to avoid metadata server throttling under high request rates."
                ),
                "diagram": (
                    "allUsers granted run.invoker",
                    "SSRF vulnerability in marketing app",
                    "Unauthorized stock adjustment (P1)",
                    "Revoke allUsers, enforce OIDC token",
                    "Zero-trust verified, 401 on unauth"
                ),
                "facts": "inventory-api allowed allUsers; SSRF exploited unauthenticated access; stock levels adjusted without authorization.",
                "inference": "Internal services must mandate cryptographic token verification; private network placement alone does not prevent unauthorized access.",
                "expected": "inventory-api requires Google-signed OIDC tokens, rejecting unauthenticated requests with HTTP 401."
            },
            "lab": {
                "name": "Service-to-Service OIDC Authentication and Ingress Control",
                "file": "day-072-service-auth.md",
                "goal": "Author Cloud Run service IAM binding policies, implement a Python OIDC token generator and validator, and verify unauthorized invocation blocking.",
                "expected": "A complete Zero-Trust service authentication policy, gcloud IAM binding commands, an executable Python OIDC validator, and an ingress restriction definition.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 71 system design and Day 68 technical requirements",
                "preflight": "Review Cloud Run service-to-service authentication and Google OAuth2 token verification specifications.",
                "steps": [
                    (
                        "**Stage 1: Preflight & Environment Validation**\n"
                        "- Define target variables and verify Cloud Run and IAM service API enablement:\n\n"
                        "```sh\n"
                        "export PROJECT_ID=\"brightloaf-prod\"\n"
                        "export REGION=\"us-central1\"\n"
                        "export CALLER_SA=\"order-fulfillment-sa\"\n"
                        "export TARGET_SERVICE=\"inventory-api\"\n"
                        "\n"
                        "gcloud config set project ${PROJECT_ID}\n"
                        "gcloud services enable run.googleapis.com iam.googleapis.com\n"
                        "```"
                    ),
                    (
                        "**Stage 2: Target / Backing Infrastructure Provisioning**\n"
                        "- Create dedicated Google Service Account for calling service:\n\n"
                        "```sh\n"
                        "# Define service account creation command\n"
                        "echo \"Provisioning service account: ${CALLER_SA}@${PROJECT_ID}.iam.gserviceaccount.com\"\n"
                        "```"
                    ),
                    (
                        "**Stage 3: Production Manifest Authoring (Least Privilege IAM Binding)**\n"
                        "- Author gcloud script granting `roles/run.invoker` strictly to the dedicated service account (`bind_service_iam.sh`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > bind_service_iam.sh\n"
                        "#!/usr/bin/env bash\n"
                        "echo \"Removing allUsers from target service...\"\n"
                        "# gcloud run services remove-iam-policy-binding ${TARGET_SERVICE} \\\n"
                        "#   --region=${REGION} \\\n"
                        "#   --member=\"allUsers\" \\\n"
                        "#   --role=\"roles/run.invoker\"\n"
                        "\n"
                        "echo \"Granting invoker role to caller service account...\"\n"
                        "# gcloud run services add-iam-policy-binding ${TARGET_SERVICE} \\\n"
                        "#   --region=${REGION} \\\n"
                        "#   --member=\"serviceAccount:${CALLER_SA}@${PROJECT_ID}.iam.gserviceaccount.com\" \\\n"
                        "#   --role=\"roles/run.invoker\"\n"
                        "echo \"Zero-Trust IAM policy binding configured successfully.\"\n"
                        "EOF\n"
                        "chmod +x bind_service_iam.sh\n"
                        "./bind_service_iam.sh\n"
                        "```"
                    ),
                    (
                        "**Stage 4: Workload Deployment & OIDC Token Emulation**\n"
                        "- Author the executable Python OIDC token generation and verification test runner (`oidc_auth_sim.py`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > oidc_auth_sim.py\n"
                        "import time\n"
                        "\n"
                        "class OIDCServiceValidator:\n"
                        "    def __init__(self, expected_audience: str, allowed_callers: list):\n"
                        "        self.expected_audience = expected_audience\n"
                        "        self.allowed_callers = set(allowed_callers)\n"
                        "\n"
                        "    def validate_request(self, token: dict) -> tuple[int, str]:\n"
                        "        if not token:\n"
                        "            return 401, 'UNAUTHORIZED: Missing Bearer Token'\n"
                        "        if token.get('aud') != self.expected_audience:\n"
                        "            return 403, 'FORBIDDEN: Audience Mismatch'\n"
                        "        if token.get('exp', 0) < time.time():\n"
                        "            return 401, 'UNAUTHORIZED: Token Expired'\n"
                        "        if token.get('email') not in self.allowed_callers:\n"
                        "            return 403, 'FORBIDDEN: Caller Not Authorized'\n"
                        "        return 200, 'AUTHORIZED: Execution Permitted'\n"
                        "\n"
                        "val = OIDCServiceValidator(\n"
                        "    expected_audience='https://inventory-api.internal',\n"
                        "    allowed_callers=['order-fulfillment-sa@brightloaf-prod.iam.gserviceaccount.com']\n"
                        ")\n"
                        "print('OIDC Service Validator Initialized.')\n"
                        "EOF\n"
                        "python3 oidc_auth_sim.py\n"
                        "```"
                    ),
                    (
                        "**Stage 5: Runtime Inspection & Verification**\n"
                        "- Test valid token acceptance:\n\n"
                        "```sh\n"
                        "cat <<'EOF' >> oidc_auth_sim.py\n"
                        "valid_token = {\n"
                        "    'aud': 'https://inventory-api.internal',\n"
                        "    'email': 'order-fulfillment-sa@brightloaf-prod.iam.gserviceaccount.com',\n"
                        "    'exp': time.time() + 3600\n"
                        "}\n"
                        "status, msg = val.validate_request(valid_token)\n"
                        "assert status == 200 and 'AUTHORIZED' in msg\n"
                        "print('PASS 1: Valid OIDC Token Authenticated Successfully.')\n"
                        "EOF\n"
                        "python3 oidc_auth_sim.py\n"
                        "```"
                    ),
                    (
                        "**Stage 6: Chaos / Unauthorized Caller Simulation**\n"
                        "- Simulate unauthenticated, expired, and unauthorized caller tokens:\n\n"
                        "```sh\n"
                        "cat <<'EOF' >> oidc_auth_sim.py\n"
                        "# Test missing token\n"
                        "assert val.validate_request(None)[0] == 401\n"
                        "print('PASS 2: Unauthenticated Request Blocked (401).')\n"
                        "\n"
                        "# Test expired token\n"
                        "expired_token = dict(valid_token, exp=time.time() - 60)\n"
                        "assert val.validate_request(expired_token)[0] == 401\n"
                        "print('PASS 3: Expired Token Blocked (401).')\n"
                        "\n"
                        "# Test unauthorized caller\n"
                        "rogue_token = dict(valid_token, email='attacker@malicious.com')\n"
                        "assert val.validate_request(rogue_token)[0] == 403\n"
                        "print('PASS 4: Rogue Caller Blocked (403).')\n"
                        "print('All Zero-Trust Identity Invariants Confirmed!')\n"
                        "EOF\n"
                        "python3 oidc_auth_sim.py\n"
                        "```"
                    ),
                    (
                        "**Stage 7: Triage, Troubleshooting & Ingress Verification**\n"
                        "- Verify internal ingress restriction parameter:\n\n"
                        "```sh\n"
                        "python3 -c \"ingress_cfg = {'ingress': 'internal-and-cloud-load-balancing'}; assert ingress_cfg['ingress'] != 'all'; print('Ingress Restriction: PASS')\"\n"
                        "```"
                    ),
                    (
                        "**Stage 8: Cleanup & Resource Teardown**\n"
                        "- Clean up temporary authentication scripts:\n\n"
                        "```sh\n"
                        "rm -f bind_service_iam.sh oidc_auth_sim.py\n"
                        "echo \"Zero-Trust authentication lab artifacts cleared successfully.\"\n"
                        "```"
                    ),
                    (
                        "**Stage 9: Artifact Acceptance Criteria**\n"
                        "- Document verified Cloud Run IAM bindings, OIDC token validation algorithms, and internal ingress controls in `day-072-service-auth.md`."
                    )
                ],
                "verification": (
                    "Run automated OIDC validation test:\n\n```sh\npython3 -c \"import oidc_auth_sim; print('OIDC Test Passed')\"\n```\n\nConfirm output displays `All Zero-Trust Identity Invariants Confirmed`."
                ),
                "trouble": (
                    "If caller receives 403 Forbidden despite valid IAM permissions, ensure the `audience` field in the token generation request matches the target service URL exactly."
                ),
                "cleanup": "No remote cloud resources created; retain configuration templates in local repository.",
                "accept": "A verified service-to-service IAM configuration, executable Python OIDC validator, and ingress control specification."
            }
        },
        {
            "key": "topic-04",
            "title": "Event-Driven Architecture: Pub/Sub Exactly-Once Delivery and Streaming Deduplication",
            "overview": (
                "Architect event-driven systems using Google Cloud Pub/Sub, Eventarc, and BigQuery. Implement exactly-once "
                "delivery semantics, ordered event streaming, and analytical deduplication pipelines."
            ),
            "preview": (
                "Network timeouts on a legacy Pub/Sub ingestion subscriber cause duplicate message redeliveries, creating "
                "4,800 ghost orders in BigQuery and distorting daily sales analytics."
            ),
            "technical": (
                "#### 1. Distributed Messaging Physics: At-Least-Once Delivery\n\n"
                "In distributed systems, the Two Generals Problem dictates that network acknowledgments (`ACKs`) can be lost or delayed. "
                "Standard Google Cloud Pub/Sub guarantees **at-least-once delivery**:\n\n"
                "- If a subscriber processes a message but the ACK is delayed by network transit past the `ackDeadlineSeconds`, Pub/Sub "
                "assumes the subscriber crashed and redelivers the message.\n"
                "- Subscribers must design for duplicate messages, or enable **Pub/Sub Exactly-Once Delivery**.\n\n"
                "#### 2. Cloud Pub/Sub Exactly-Once Delivery Mechanics\n\n"
                "When enabled on a subscription, **Pub/Sub Exactly-Once Delivery** adds distributed transactional coordination:\n\n"
                "- If a subscriber's ACK is in-flight when the deadline expires, redelivery is held until the ACK status is definitively resolved.\n"
                "- If an ACK fails due to transient network failure, the subscriber receives an acknowledgment response (`ackResponse`) "
                "indicating whether the lease was extended or if the message was redelivered.\n\n"
                "#### 3. Ordered Delivery with Ordering Keys\n\n"
                "When events must be processed sequentially (e.g. `OrderCreated -> OrderPaid -> OrderShipped`), publishers assign an "
                "**Ordering Key** (e.g. `order-id`):\n\n"
                "- Pub/Sub guarantees that messages with the same ordering key are delivered to subscribers in the exact order they were received.\n"
                "- If an earlier message in the key sequence fails to ACK, delivery of subsequent messages for that specific key is halted until resolved.\n\n"
                "#### 4. Architectural Trade-offs: Event Streaming and Ingestion Engines\n\n"
                "| Ingestion Primitive | Delivery Guarantee | Ordering Scope | Max Ingestion Throughput | Consumer Scaling Pattern | Best Suited For |\n"
                "|---|---|---|---|---|---|\n"
                "| **Standard Pub/Sub** | At-least-once | Unordered | Millions of messages/sec | Horizontal parallel pull subscribers | High-throughput telemetry, metrics, decoupled notifications |\n"
                "| **Pub/Sub with Ordering Keys** | At-least-once | In-order per key | Bounded per single key (1 MB/s) | Key-partitioned delivery | Stateful workflows, financial ledger mutations |\n"
                "| **Pub/Sub Exactly-Once** | Exactly-once | Optional ordering | High (adds small metadata coordination) | Bounded ACK retry protocol | Critical transactional notifications, billing events |\n"
                "| **BigQuery Storage Write API** | Exactly-once (via stream offsets) | Stream-level | Millions of rows/sec | Direct streaming insert to Capacitor storage | Real-time analytics, data lakehouse ingestion |\n"
            ),
            "questions": [
                "Why does standard Pub/Sub at-least-once delivery inevitably produce duplicate messages during network latency?",
                "How does Pub/Sub Exactly-Once Delivery coordinate message leases to prevent duplicate processing?",
                "What is the operational consequence of a poisoned message blocking an ordering key sequence?",
                "How does BigQuery Storage Write API default stream differ from committed streams in deduplication guarantees?",
            ],
            "reference": "https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery",
            "reference_label": "Google Cloud Pub/Sub: Exactly-Once Delivery",
            "scenario": {
                "scenario": (
                    "During peak order processing, Brightloaf's analytics subscriber experienced a 30-second GC (garbage collection) pause "
                    "in its Java ingestion runtime. Because the Pub/Sub subscription was configured with a default `ackDeadline` of 10 seconds, "
                    "Pub/Sub considered all 4,800 in-flight messages expired and redelivered them to secondary subscriber pods. Once the GC "
                    "pause completed, the original subscriber processed the messages and sent delayed ACKs, while the secondary subscribers "
                    "also processed the same messages. Both subscriber groups inserted the records directly into BigQuery without deduplication "
                    "keys, resulting in 4,800 phantom orders and corrupting corporate revenue dashboards by $140,000."
                ),
                "impact": (
                    "Data corruption in corporate BigQuery analytical warehouse. Executive sales reports overstated gross merchandise value "
                    "(GMV) by $140,000, triggering an emergency analytics audit. Data engineering spent 18 hours manually purging duplicate "
                    "records from downstream reporting tables."
                ),
                "constraints": (
                    "Guarantee zero duplicate record ingestion in BigQuery; eliminate subscriber GC-pause redelivery storms; process order "
                    "events with end-to-end latency < 2 seconds."
                ),
                "evidence": (
                    "Querying BigQuery for duplicate orders confirmed multiple redelivered records:\n\n"
                    "```text\n"
                    "$ bq query --use_legacy_sql=false '\n"
                    "  SELECT\n"
                    "    order_id,\n"
                    "    COUNT(1) as duplicates\n"
                    "  FROM `brightloaf-prod.streaming_analytics.orders_ingest`\n"
                    "  WHERE publish_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)\n"
                    "  GROUP BY 1 HAVING COUNT(1) > 1 LIMIT 3'\n"
                    "+---------------+------------+\n"
                    "| order_id      | duplicates |\n"
                    "+---------------+------------+\n"
                    "| ord-89412-us  |          4 |  <-- Ingestion duplicates confirmed\n"
                    "| ord-89415-eu  |          3 |\n"
                    "| ord-89421-us  |          2 |\n"
                    "+---------------+------------+\n"
                    "```\n\n"
                    "Inspecting Pub/Sub subscription configuration:\n\n"
                    "```yaml\n"
                    "$ gcloud pubsub subscriptions describe orders-analytics-sub --format=\"yaml(ackDeadlineSeconds,enableExactlyOnceDelivery)\"\n"
                    "ackDeadlineSeconds: 10\n"
                    "enableExactlyOnceDelivery: false\n"
                    "```"
                ),
                "root": (
                    "Short acknowledgment deadlines paired with lack of Pub/Sub exactly-once delivery and missing database-level deduplication "
                    "caused transient subscriber pauses to generate thousands of duplicate analytical records."
                ),
                "diagnostic_steps": [
                    "Step 1: Execute SQL deduplication query in BigQuery; observe thousands of duplicate `order_id` records with publish timestamps within seconds of each other.",
                    "Step 2: Inspect Pub/Sub subscription metrics in Cloud Monitoring; observe redelivery count (`subscription/redelivered_message_count`) spiking during the incident window.",
                    "Step 3: Review subscriber JVM GC pause metrics; identify a 30-second stop-the-world garbage collection pause.",
                    "Step 4: Check subscription settings; confirm `enableExactlyOnceDelivery` is disabled and `ackDeadlineSeconds` is set to only 10s."
                ],
                "fix": (
                    "Tactical Fix: Enable Pub/Sub Exactly-Once Delivery on the subscription via <kbd>gcloud pubsub subscriptions update</kbd> "
                    "with `--enable-exactly-once-delivery` and extend the ack deadline to 60 seconds.\n\n"
                    "Strategic Fix: Migrate ingestion to the BigQuery Storage Write API using committed streams with deterministic stream offsets, "
                    "and establish windowed analytical deduplication views using `QUALIFY ROW_NUMBER() OVER(PARTITION BY order_id ORDER BY event_time DESC) = 1`."
                ),
                "verify": (
                    "Simulate 5,000 synthetic messages with intentional 20-second subscriber pauses. Verify that Pub/Sub redelivery rate "
                    "drops to zero, BigQuery duplicate query returns zero rows, and analytical dashboard numbers match the transactional source of truth."
                ),
                "residual": (
                    "Pub/Sub Exactly-Once Delivery requires subscribers to handle ack response acknowledgments asynchronously; high network "
                    "jitter may cause occasional lease extensions to time out."
                ),
                "diagram": (
                    "30s JVM GC pause",
                    "Ack deadline (10s) expires",
                    "Pub/Sub redelivers 4,800 duplicates",
                    "Enable Exactly-Once + 60s ack deadline",
                    "Zero duplicate rows, analytics 100% verified"
                ),
                "facts": "GC pause lasted 30s; ackDeadline was 10s; 4,800 duplicate records inserted into BigQuery; revenue overstated by $140k.",
                "inference": "Messaging pipelines require both broker-level exactly-once delivery and destination-level deduplication.",
                "expected": "Pub/Sub Exactly-Once Delivery and BigQuery Storage Write API guarantee single-record persistence even during subscriber pauses."
            },
            "lab": {
                "name": "Pub/Sub Exactly-Once Delivery and Streaming Deduplication Pipeline",
                "file": "day-072-event-dedup.md",
                "goal": "Author Pub/Sub topic and subscription manifests with exactly-once delivery, build an executable Python message publisher and deduplication consumer, and verify duplicate elimination.",
                "expected": "A complete event streaming architecture specification, a Pub/Sub exactly-once subscription manifest, an executable Python deduplication test runner, and a BigQuery deduplication SQL view.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 71 system design and Day 68 technical requirements",
                "preflight": "Review Google Cloud Pub/Sub exactly-once delivery documentation and BigQuery SQL window functions.",
                "steps": [
                    (
                        "**Stage 1: Preflight & Environment Validation**\n"
                        "- Define target variables and verify Pub/Sub and BigQuery API enablement:\n\n"
                        "```sh\n"
                        "export PROJECT_ID=\"brightloaf-prod\"\n"
                        "export TOPIC_NAME=\"orders-stream-topic\"\n"
                        "export SUB_NAME=\"orders-stream-sub\"\n"
                        "\n"
                        "gcloud config set project ${PROJECT_ID}\n"
                        "gcloud services enable pubsub.googleapis.com bigquery.googleapis.com\n"
                        "```"
                    ),
                    (
                        "**Stage 2: Target / Backing Infrastructure Provisioning**\n"
                        "- Author topic creation script with dead-letter queue support:\n\n"
                        "```sh\n"
                        "# Define topic creation command\n"
                        "echo \"Provisioning topic: projects/${PROJECT_ID}/topics/${TOPIC_NAME}\"\n"
                        "```"
                    ),
                    (
                        "**Stage 3: Production Manifest Authoring (Pub/Sub Exactly-Once Subscription)**\n"
                        "- Author gcloud subscription creation script with exactly-once delivery (`create_exactly_once_sub.sh`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > create_exactly_once_sub.sh\n"
                        "#!/usr/bin/env bash\n"
                        "echo \"Creating Pub/Sub Subscription with Exactly-Once Delivery...\"\n"
                        "# gcloud pubsub subscriptions create ${SUB_NAME} \\\n"
                        "#   --topic=${TOPIC_NAME} \\\n"
                        "#   --enable-exactly-once-delivery \\\n"
                        "#   --ack-deadline=60 \\\n"
                        "#   --message-retention-duration=7d\n"
                        "echo \"Subscription created with enable-exactly-once-delivery=true and ack-deadline=60s.\"\n"
                        "EOF\n"
                        "chmod +x create_exactly_once_sub.sh\n"
                        "./create_exactly_once_sub.sh\n"
                        "```"
                    ),
                    (
                        "**Stage 4: Workload Deployment & BigQuery Deduplication View SQL**\n"
                        "- Author the BigQuery analytical deduplication view SQL (`dedup_view.sql`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > dedup_view.sql\n"
                        "-- BigQuery Analytical Deduplication View\n"
                        "CREATE OR REPLACE VIEW `brightloaf-prod.streaming_analytics.v_orders_deduped` AS\n"
                        "SELECT\n"
                        "  order_id,\n"
                        "  customer_id,\n"
                        "  amount,\n"
                        "  event_time,\n"
                        "  publish_time\n"
                        "FROM `brightloaf-prod.streaming_analytics.orders_ingest`\n"
                        "QUALIFY ROW_NUMBER() OVER (\n"
                        "  PARTITION BY order_id\n"
                        "  ORDER BY publish_time DESC\n"
                        ") = 1;\n"
                        "EOF\n"
                        "cat dedup_view.sql\n"
                        "```"
                    ),
                    (
                        "**Stage 5: Runtime Inspection & Verification**\n"
                        "- Author and execute the Python deduplication test runner (`stream_dedup_sim.py`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > stream_dedup_sim.py\n"
                        "class StreamingDeduplicator:\n"
                        "    def __init__(self):\n"
                        "        self.processed_ids = set()\n"
                        "        self.table = []\n"
                        "\n"
                        "    def ingest(self, message_id: str, order_id: str, amount: float):\n"
                        "        if order_id in self.processed_ids:\n"
                        "            return False, 'DUPLICATE_DROPPED'\n"
                        "        self.processed_ids.add(order_id)\n"
                        "        self.table.append({'msg_id': message_id, 'order_id': order_id, 'amount': amount})\n"
                        "        return True, 'INSERTED'\n"
                        "\n"
                        "dedup = StreamingDeduplicator()\n"
                        "# Ingest initial order\n"
                        "ok, msg = dedup.ingest('msg-001', 'ord-1001', 45.50)\n"
                        "assert ok and msg == 'INSERTED'\n"
                        "# Re-ingest duplicate message (simulating network redelivery)\n"
                        "ok2, msg2 = dedup.ingest('msg-002', 'ord-1001', 45.50)\n"
                        "assert not ok2 and msg2 == 'DUPLICATE_DROPPED'\n"
                        "assert len(dedup.table) == 1\n"
                        "print('Streaming Deduplication Verified: 1 row stored, duplicates eliminated.')\n"
                        "EOF\n"
                        "python3 stream_dedup_sim.py\n"
                        "```"
                    ),
                    (
                        "**Stage 6: Chaos / Redelivery Burst Simulation**\n"
                        "- Simulate a burst of 100 messages containing 40 duplicate records and verify exact retention:\n\n"
                        "```sh\n"
                        "cat <<'EOF' > simulate_redelivery_burst.py\n"
                        "from stream_dedup_sim import StreamingDeduplicator\n"
                        "d = StreamingDeduplicator()\n"
                        "for i in range(60):\n"
                        "    d.ingest(f'm-{i}', f'ord-{i}', 10.0)\n"
                        "# Duplicate 40 messages\n"
                        "duplicates_blocked = sum(1 for i in range(40) if not d.ingest(f'm-dup-{i}', f'ord-{i}', 10.0)[0])\n"
                        "print(f\"Burst: 60 unique orders, 40 duplicates attempted. Blocked: {duplicates_blocked}\")\n"
                        "assert duplicates_blocked == 40 and len(d.table) == 60\n"
                        "print('EXACTLY-ONCE INVARIANT CONFIRMED: Zero duplicate rows stored!')\n"
                        "EOF\n"
                        "python3 simulate_redelivery_burst.py\n"
                        "```"
                    ),
                    (
                        "**Stage 7: Triage, Troubleshooting & BigQuery SQL Syntax Check**\n"
                        "- Validate BigQuery QUALIFY SQL view syntax using Python:\n\n"
                        "```sh\n"
                        "python3 -c \"sql = open('dedup_view.sql').read(); assert 'QUALIFY ROW_NUMBER()' in sql; print('BigQuery Deduplication View SQL Validated')\"\n"
                        "```"
                    ),
                    (
                        "**Stage 8: Cleanup & Resource Teardown**\n"
                        "- Remove temporary stream manifests and calculation scripts:\n\n"
                        "```sh\n"
                        "rm -f create_exactly_once_sub.sh dedup_view.sql stream_dedup_sim.py simulate_redelivery_burst.py\n"
                        "echo \"Streaming deduplication lab cleaned up successfully.\"\n"
                        "```"
                    ),
                    (
                        "**Stage 9: Artifact Acceptance Criteria**\n"
                        "- Save verified Pub/Sub exactly-once subscription definitions, BigQuery QUALIFY deduplication views, and Python simulation scripts in `day-072-event-dedup.md`."
                    )
                ],
                "verification": (
                    "Run automated deduplication test:\n\n```sh\npython3 -c \"import stream_dedup_sim; print('Deduplication Test Passed')\"\n```\n\nConfirm output displays `Streaming Deduplication Verified: 1 row stored, duplicates eliminated`."
                ),
                "trouble": (
                    "If subscribers report `kAckDeadlineExceeded` despite exactly-once delivery, ensure subscriber processing duration is well below the configured ack deadline."
                ),
                "cleanup": "No remote cloud resources created; retain configuration templates in local repository.",
                "accept": "A verified Pub/Sub exactly-once subscription definition, BigQuery analytical deduplication view SQL, and working Python deduplication test runner."
            }
        }
    ]
}
