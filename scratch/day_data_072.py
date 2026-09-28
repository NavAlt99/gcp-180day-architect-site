"""day_data_072.py — Exhaustive architecture data specification for Day 72.

Covers Web Application Architecture: Sizing compute, caching, persistence, and service decoupling.
Follows the PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
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
  <thead>
    <tr>
      <th>Architecture Layer</th>
      <th>GCP Service Primitive</th>
      <th>Primary Bottleneck / Failure Domain</th>
      <th>Architectural Protection Pattern</th>
      <th>Target SLO / Performance Metric</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Global Edge Ingress</strong></td>
      <td>External Application Load Balancer + Cloud CDN</td>
      <td>Cache stampede on origin; TLS handshake latency</td>
      <td>Content-addressed immutable asset hashing; HTTP/3 (QUIC)</td>
      <td>p99 Edge Latency &lt; 25 ms; 85%+ Cache Hit Ratio</td>
    </tr>
    <tr>
      <td><strong>Stateless Compute Tier</strong></td>
      <td>Compute Engine MIG / Cloud Run</td>
      <td>Thread starvation under burst; cold starts</td>
      <td>Predictive autoscaling; minimum idle replicas; connection pooling</td>
      <td>p95 Latency &lt; 150 ms; 99.99% Availability</td>
    </tr>
    <tr>
      <td><strong>Session &amp; Ephemeral Cache</strong></td>
      <td>Memorystore for Redis (Cluster / HA)</td>
      <td>Memory exhaustion (OOM); cross-zone network latency</td>
      <td>Volatile-LRU eviction; in-VPC Private Service Access; read replicas</td>
      <td>Sub-millisecond query time; zero evictions on critical keys</td>
    </tr>
    <tr>
      <td><strong>Relational Persistence Tier</strong></td>
      <td>Cloud SQL for PostgreSQL (HA Regional)</td>
      <td>PostgreSQL backend process RAM exhaustion; lock contention</td>
      <td>In-VPC PgBouncer in transaction mode; read replica query offload</td>
      <td>Active connections &lt; 70% max; p99 query &lt; 40 ms</td>
    </tr>
    <tr>
      <td><strong>Asynchronous Streaming Tier</strong></td>
      <td>Pub/Sub + BigQuery Streaming Insert</td>
      <td>At-least-once message duplication; write quota throttling</td>
      <td>Pub/Sub exactly-once delivery; BigQuery Storage Write API dedup</td>
      <td>End-to-end ingestion latency &lt; 2 s; zero duplicate records</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 72: End-to-End Enterprise Web Application Flow",
        "desc": "Logical request flow from edge CDN through compute, session caching, database pooling, and event ingestion.",
        "nodes": [
            ("Client Ingress", "External Global ALB\\n+ Cloud CDN (Edge PoPs)"),
            ("Compute Tier", "Private Subnet MIG / Run\\n+ In-VPC Serverless Access"),
            ("Persistence Tier", "Memorystore Redis\\n+ PgBouncer to Cloud SQL"),
            ("Asynchronous Tier", "Pub/Sub Stream Ingestion\\n+ BigQuery Analytics"),
        ],
        "caption": "Figure 72.1: End-to-end multi-tier web topology isolating stateful persistence behind connection proxies and edge caching."
    },
    "part3_intro": (
        "The following production field cases examine catastrophic failure modes encountered in high-scale web deployments. "
        "Each case details the real-world operational context, precise quantitative failure indicators, root cause analysis, "
        "defensible multi-step remediations, verification procedures, and dual-lane failed/corrected architectural diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises provide production-grade, executable configurations and verification scripts for "
        "sizing connection pools, establishing immutable CDN caching, validating OIDC service authentication, and "
        "verifying streaming deduplication pipelines. Execute all steps in your local environment."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Three-Tier Web Application Architecture (Compute, Memory Cache, Database Persistence)",
            "overview": (
                "Design and size three-tier architectures combining Compute Engine Managed Instance Groups, "
                "Memorystore for Redis, and Cloud SQL for PostgreSQL. Learn to calculate connection limits, prevent "
                "database process saturation with PgBouncer, and establish non-disruptive health checks."
            ),
            "preview": (
                "Horizontal autoscaling during a traffic surge causes compute nodes to spawn hundreds of database "
                "connections, exhausting PostgreSQL max_connections and taking down the entire transaction processing tier."
            ),
            "technical": (
                "#### 1. Architectural Thermodynamics of Three-Tier Topologies\n\n"
                "In enterprise cloud architecture, a classic three-tier topology separates user interaction, business logic, "
                "and stateful persistence into decoupled failure domains:\n\n"
                "- **Presentation / Ingress Tier:** Global External Application Load Balancers (ALB) terminate TLS at edge points "
                "of presence (PoPs), proxying HTTP/2 and HTTP/3 connections to backend services.\n"
                "- **Compute / Application Tier:** Stateless containers (Cloud Run) or virtual machines in Managed Instance "
                "Groups (MIGs) deployed across multiple availability zones within a private Virtual Private Cloud (VPC) subnet.\n"
                "- **Persistence Tier:** Managed persistence divided into ephemeral in-memory caching (Memorystore for Redis) "
                "for session state and database query results, and transactional relational persistence (Cloud SQL for PostgreSQL) "
                "configured with regional synchronous high availability (HA).\n\n"
                "#### 2. The Database Connection Exhaustion Problem\n\n"
                "A pervasive architectural failure occurs when stateless compute autoscales horizontally to meet traffic surges. "
                "Relational databases like PostgreSQL allocate dedicated operating system backend processes for each incoming client "
                "connection. In PostgreSQL, each backend worker process consumes between 5MB and 12MB of RAM for session buffers, "
                "work memory (`work_mem`), and socket buffers. If an instance configured with `max_connections = 500` is flooded with "
                "connections, process context switching degrades CPU cache efficiency and can trigger the Linux kernel Out-Of-Memory "
                "(OOM) killer.\n\n"
                "When application servers embed client-side connection pools (such as HikariCP or SQLAlchemy) configured with 20 connections "
                "per pod, an autoscaling event that expands replicas from 5 to 30 immediately attempts to open 600 concurrent TCP sockets "
                "(`30 * 20 = 600`). The database rejects excess connections with `FATAL: remaining connection slots are reserved for "
                "non-replication superuser connections`, throwing HTTP 500 errors across all compute nodes.\n\n"
                "#### 3. Connection Multiplexing with In-VPC PgBouncer\n\n"
                "To decouple compute autoscaling from database backend limits, architects deploy an intermediate connection pooler such "
                "as **PgBouncer** in **transaction pooling** mode:\n\n"
                "- In **session pooling**, a client holds a dedicated server connection until its TCP socket disconnects.\n"
                "- In **transaction pooling**, PgBouncer assigns a physical database connection only for the precise duration of an "
                "active SQL transaction block (`BEGIN` ... `COMMIT`). As soon as the transaction finishes, the database connection is "
                "returned to the pool, allowing thousands of client threads to share a compact pool of 50 to 100 actual PostgreSQL processes.\n\n"
                "```ini\n"
                "[databases]\n"
                "brightloaf_orders = host=10.128.0.50 port=5432 dbname=orders pool_size=60 auth_user=pgbouncer_auth\n\n"
                "[pgbouncer]\n"
                "listen_addr = 0.0.0.0\n"
                "listen_port = 6432\n"
                "auth_type = scram-sha-256\n"
                "auth_file = /etc/pgbouncer/userlist.txt\n"
                "pool_mode = transaction\n"
                "max_client_conn = 10000\n"
                "default_pool_size = 50\n"
                "min_pool_size = 10\n"
                "reserve_pool_size = 10\n"
                "reserve_pool_timeout = 5.0\n"
                "max_db_connections = 80\n"
                "query_timeout = 30.0\n"
                "client_idle_timeout = 60.0\n"
                "```\n\n"
                "#### 4. Safe Health Check Probing and Cascading Failure Prevention\n\n"
                "Compute Engine MIG autohealing relies on periodic HTTP health checks. A catastrophic anti-pattern is configuring "
                "the health check endpoint (`/healthz`) to execute a synchronous database probe (`SELECT 1`). If the database experiences "
                "transient lock contention or reaches connection limits, the health checks time out across all VM instances simultaneously. "
                "The MIG marks every VM unhealthy and reboots all compute nodes in parallel, converting a momentary database slow-down "
                "into a complete, multi-hour cluster collapse. Health checks must evaluate local container health (memory, internal thread "
                "loops) and rely on separate circuit breakers to shed load gracefully.\n\n"
                "#### 5. Architectural Trade-offs: Database Connection Management\n\n"
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
                "diagnostic_steps": [
                    "Step 1: Query Cloud Monitoring metrics for Cloud SQL `database/postgresql/num_backends` and `database/network/active_connections`; observe connection count hitting the hard limit of 500 at 08:04 UTC and plateauing.",
                    "Step 2: Correlate database metrics with Compute Engine MIG autoscaler timeline in Cloud Logging; observe instance count expanded dynamically from 4 to 28 instances across zones us-central1-a, b, and c.",
                    "Step 3: Inspect application container stdout logs; identify hundreds of repeated exceptions: `org.postgresql.util.PSQLException: FATAL: remaining connection slots are reserved for non-replication superuser connections`.",
                    "Step 4: Audit microservice deployment manifests and HikariCP configuration; confirm `maximumPoolSize` is set to 20 connections per pod with 1 container per VM: 28 VMs × 20 connections = 560 potential connections, exceeding the Cloud SQL ceiling of 500."
                ],
                "root": (
                    "Eager application-level connection pooling without an intermediate connection proxy causes horizontal compute autoscaling "
                    "to violently exhaust database backend worker processes. Each new VM spawns a full connection pool that holds idle TCP sockets "
                    "to PostgreSQL, exhausting memory and backend slots even when individual transactions execute in under 15 milliseconds."
                ),
                "remediation_steps": [
                    "Step 1: Immediately apply emergency connection throttling: update the microservice configuration map via rolling deployment to reduce client `maximumPoolSize` from 20 to 6 connections per VM (28 × 6 = 168 max connections), restoring immediate database availability.",
                    "Step 2: Provision an in-VPC high-availability PgBouncer pooler tier deployed across multiple zones using Managed Instance Groups behind an Internal Passthrough Network Load Balancer.",
                    "Step 3: Configure PgBouncer in transaction pooling mode (`default_pool_size = 80`, `max_client_conn = 5000`, `reserve_pool_size = 15`), decoupling tens of thousands of client threads from actual PostgreSQL backend processes.",
                    "Step 4: Decouple MIG autohealing health checks from the database: replace `/healthz` database query probes with an internal `/live` endpoint that checks only local process memory and thread liveness."
                ],
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
                "goal": "Model compute autoscaling bounds against Cloud SQL connection limits, write a production PgBouncer configuration, and establish safe health check policies.",
                "expected": "A complete sizing document with PgBouncer configuration, connection calculation formulas, and a verified autohealing health-check definition.",
                "mode": "offline architecture specification, shell scripting, and configuration design; no cloud resources billed",
                "prereq": "Day 71 requirements and Day 61 Cloud SQL configuration notes",
                "preflight": "Review Cloud SQL PostgreSQL connection pricing and Compute Engine health-check documentation.",
                "steps": [
                    "Draft the complete three-tier architecture topology in `day-072-three-tier-sizing.md`, specifying CIDRs for Public Ingress, Private Compute, and Private Services Access.",
                    "Create the production PgBouncer configuration file:\n\n```ini\n# pgbouncer.ini\n[databases]\n* = host=10.128.0.50 port=5432 auth_user=pgbouncer\n\n[pgbouncer]\nlogfile = /var/log/pgbouncer/pgbouncer.log\npidfile = /var/run/pgbouncer/pgbouncer.pid\nlisten_addr = 0.0.0.0\nlisten_port = 6432\nauth_type = scram-sha-256\nauth_file = /etc/pgbouncer/userlist.txt\npool_mode = transaction\nmax_client_conn = 5000\ndefault_pool_size = 50\nmin_pool_size = 10\nreserve_pool_size = 10\nreserve_pool_timeout = 5.0\nmax_db_connections = 100\n```",
                    "Calculate the connection math: with 30 max VMs, 1 container per VM, HikariCP pool = 5, total client connections = 150; PgBouncer multiplexes this into a maximum of 50 Cloud SQL connections.",
                    "Define the Compute Engine autohealing health check policy:\n\n```sh\n# Configure safe autohealing health check\ncat << 'EOF' > health-check-spec.json\n{\n  \"name\": \"checkout-compute-health-check\",\n  \"type\": \"HTTP\",\n  \"httpHealthCheck\": {\n    \"port\": 8080,\n    \"requestPath\": \"/healthz/live\",\n    \"proxyHeader\": \"NONE\"\n  },\n  \"checkIntervalSec\": 10,\n  \"timeoutSec\": 5,\n  \"unhealthyThreshold\": 3,\n  \"healthyThreshold\": 2\n}\nEOF\n```",
                    "Execute an offline connection pool sizing calculation script:\n\n```python\n# sizing_calc.py\nimport math\n\nmax_vms = 30\napp_pool_per_vm = 5\ncloud_sql_tier_max = 500\npgbouncer_pool = 80\n\ntotal_app_conns = max_vms * app_pool_per_vm\nsafety_margin = (cloud_sql_tier_max - pgbouncer_pool) / cloud_sql_tier_max * 100\n\nprint(f\"Max Client Connections: {total_app_conns}\")\nprint(f\"PgBouncer Backend Pool: {pgbouncer_pool}\")\nprint(f\"Cloud SQL Safety Margin: {safety_margin:.1f}% free slots\")\nassert pgbouncer_pool < cloud_sql_tier_max, \"Database overload risk!\"\n```"
                ],
                "verification": (
                    "Verify configuration parameters using validation scripts:\n\n```sh\npython3 -c \"import configparser; c = configparser.ConfigParser(); c.read('pgbouncer.ini'); assert c['pgbouncer']['pool_mode'] == 'transaction'; print('PgBouncer Config Validated: Transaction Mode')\"\n```\n\nConfirm output displays `PgBouncer Config Validated: Transaction Mode`."
                ),
                "trouble": (
                    "If health check failures cause rapid VM cycling, inspect health check configuration:\n\n```sh\ncat health-check-spec.json\n```\n\nEnsure request path targets `/healthz/live` instead of an endpoint querying Cloud SQL."
                ),
                "cleanup": "No remote cloud resources created; retain configuration files in local repository.",
                "accept": "A validated PgBouncer configuration, connection capacity sizing formula, and autohealing health-check definition."
            }
        },
        {
            "key": "topic-02",
            "title": "Static Asset Offloading: Cloud CDN and Cloud Storage Backend Buckets",
            "overview": (
                "Decouple dynamic compute from static asset delivery using Cloud CDN attached to Cloud Storage backend buckets. "
                "Master caching modes, cache invalidation cost realities, and content-addressed asset versioning."
            ),
            "preview": (
                "An e-commerce site serves high-resolution product photos directly from compute instances, consuming 85% "
                "of server CPU and memory bandwidth while blowing egress budgets and causing regional latency spikes."
            ),
            "technical": (
                "#### 1. Edge Caching vs. Origin Compute Dynamics\n\n"
                "Serving static assets (images, stylesheets, JavaScript bundles, fonts) directly from compute instances "
                "violates core multi-tier scalability principles:\n\n"
                "- **Kernel File Streaming Overhead:** Each incoming HTTP request for a 2MB product image occupies an application "
                "worker thread or event loop cycle, consumes Linux kernel socket buffers, and monopolizes compute VM egress bandwidth.\n"
                "- **Global Latency Penalty:** When users access an origin in `us-central1` from London or Tokyo, TCP three-way "
                "handshakes and TLS negotiation incur multiple cross-oceanic round-trip times (RTTs), adding 150ms to 250ms of latency "
                "before the first byte transfers.\n"
                "- **Egress Cost Disparity:** Premium Tier network egress directly from Compute Engine VMs is significantly more "
                "expensive than cached edge egress delivered via Google's private global fiber network.\n\n"
                "#### 2. Cloud CDN Mechanics and Caching Modes\n\n"
                "Google Cloud CDN integrates directly with the Global External Application Load Balancer, terminating TCP/TLS at "
                "over 100 edge Points of Presence (PoPs) worldwide. When an edge cache misses, Cloud CDN fetches the object from "
                "the backend origin and stores it across regional edge caches. Cloud CDN supports three distinct caching modes:\n\n"
                "  1. `CACHE_ALL_STATIC`: Automatically caches static web content based on file extensions (e.g. `.js`, `.css`, `.png`, "
                "`.webp`, `.woff2`) regardless of origin response headers, applying default TTLs.\n"
                "  2. `USE_ORIGIN_HEADERS`: Honors standard HTTP cache control headers (`Cache-Control`, `Expires`, `ETag`) emitted by the origin.\n"
                "  3. `FORCE_CACHE_ALL`: Unconditionally caches all HTTP 200 responses, overriding origin headers (dangerous for dynamic APIs).\n\n"
                "- **The Cache Invalidation Trap:** Triggering global cache purges via the cache invalidation CLI (`invalidate-cdn-cache`) "
                "across 100+ edge PoPs is asynchronous, takes minutes to complete, and is subject to strict API rate limits. Furthermore, "
                "aggressive invalidations cause cache stampedes that overwhelm origin storage.\n"
                "- **Content-Addressed Asset Versioning:** Best-practice frontend delivery enforces **immutable asset hashing**. Build "
                "pipelines append cryptographic content hashes to filenames (e.g. `bundle.8a3f9c.js`, `style.4d1e2b.css`). These assets "
                "are served with permanent cache headers: `Cache-Control: public, max-age=31536000, immutable`. When a release occurs, "
                "the HTML shell updates to point to new hashed filenames, achieving instant zero-downtime atomic updates with zero cache invalidation calls.\n\n"
                "#### 3. Cloud Storage Backend Buckets and Private Origin Security\n\n"
                "In Google Cloud, Cloud CDN attaches to an External Application Load Balancer via **Backend Buckets** pointing to Cloud Storage:\n\n"
                "```sh\n"
                "# Define Cloud CDN Backend Bucket with fine-grained TTLs\n"
                "gcloud compute backend-buckets create static-asset-backend \\\n"
                "  --gcs-bucket-name=brightloaf-static-assets \\\n"
                "  --enable-cdn \\\n"
                "  --cache-mode=CACHE_ALL_STATIC \\\n"
                "  --default-ttl=86400 \\\n"
                "  --max-ttl=31536000 \\\n"
                "  --client-ttl=86400 \\\n"
                "  --negative-caching\n"
                "```\n\n"
                "To prevent users from bypassing the Load Balancer and accessing the Cloud Storage bucket directly, architects enforce "
                "Uniform Bucket-Level Access (UBLA) and restrict public read access strictly through the Load Balancer IP address or via "
                "Signed URLs / Signed Cookies.\n\n"
                "#### 4. Cache Key Architecture and Query String Stripping\n\n"
                "Cloud CDN generates a unique **cache key** for every object based on the URI. By default, query parameters are included "
                "in the cache key. In e-commerce applications, marketing trackers (e.g. `?utm_source=newsletter&utm_campaign=spring`) "
                "fracture the cache: every user with a unique campaign parameter triggers a cache miss, dropping the edge hit ratio from "
                "95% to under 20%. Enabling **Custom Cache Keys** configured to exclude query strings restores cache coalescing.\n\n"
                "#### 5. Architectural Trade-offs: Caching Layers\n\n"
                "| Caching Tier | Technology Primitive | Latency (p99) | Invalidation Speed | Max Object Size | Ideal Workload |\n"
                "|---|---|---|---|---|---|\n"
                "| **Browser / Client Cache** | HTTP `Cache-Control: immutable` | < 1 ms (Local Disk/RAM) | Impossible (until TTL expiry or URL change) | Unlimited | Version-hashed static JavaScript, CSS, web fonts |\n"
                "| **Edge CDN PoP** | Google Cloud CDN / Cloudflare | 10–30 ms | Minutes (global purge) or Instant (hashed filename) | 5 TB (via GCS chunking) | Public product images, media streams, static assets |\n"
                "| **Load Balancer Cache** | Envoy / NGINX Ingress Cache | 5–15 ms | Seconds | Hundreds of MBs | Regional dynamic API responses, catalog listings |\n"
                "| **In-Memory Cache Tier** | Memorystore for Redis Cluster | 1–3 ms | Sub-millisecond (`DEL` / `UNLINK` key) | 512 MB per key | Shopping cart sessions, auth tokens, pricing lookup |\n"
                "| **Application Local Cache** | In-Process Guava / Caffeine Cache | < 100 µs | Microseconds (local process memory) | JVM Heap bounded | Static lookup tables, configuration dictionaries |\n"
            ),
            "questions": [
                "How does content-addressed asset versioning eliminate the need for global CDN cache invalidation?",
                "What is the impact of marketing UTM query parameters on Cloud CDN cache hit ratios without custom cache keys?",
                "Why should Cloud Storage buckets used as CDN origins enforce Uniform Bucket-Level Access?",
                "Under what condition does `FORCE_CACHE_ALL` cause severe security or data leakage vulnerabilities?",
            ],
            "reference": "https://docs.cloud.google.com/cdn/docs/caching",
            "reference_label": "Google Cloud CDN Documentation: Cache modes and cache keys",
            "scenario": {
                "scenario": (
                    "Brightloaf launches a major brand redesign featuring high-resolution photography of sourdough breads and pastries. "
                    "All media assets are bundled inside the web application container and served directly from Compute Engine VMs via "
                    "NGINX. During morning peak traffic in Europe and North America, compute instances experience severe memory bloat and "
                    "800 Mbps outbound egress per VM. Customer page load times in Tokyo and Sydney average 4.8 seconds, while compute "
                    "infrastructure costs surge by 340% due to cross-region network egress charges."
                ),
                "impact": (
                    "P2 operational degradation and severe cost anomaly. Page load bounce rate increased by 28% for international users. "
                    "Web application VM memory utilization exceeded 92%, triggering emergency autoscaler thrashing. Monthly network egress "
                    "bill jumped from $1,200 to $5,800 within a single billing cycle."
                ),
                "constraints": (
                    "Preserve CORS headers for multi-domain frontend single-page applications; do not alter existing application business "
                    "logic; eliminate origin compute load for all static assets without downtime."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect Compute Engine instance memory and network metrics in Cloud Monitoring; observe 92% RAM utilization and sustained 800 Mbps outbound egress across all compute nodes.",
                    "Step 2: Inspect Load Balancer HTTP access logs; filter by top requested paths; observe 78% of incoming requests are for `.png`, `.jpg`, and `.webp` assets routed to VM compute backends.",
                    "Step 3: Profile static asset latency from international locations; observe 2,800ms to 3,500ms transfer times from Tokyo and Sydney.",
                    "Step 4: Check Load Balancer URL map rules; confirm all paths (`/*`) route to the compute backend service with CDN disabled."
                ],
                "root": (
                    "Static assets are colocated on compute VM containers rather than offloaded to edge storage. Serving media files from "
                    "compute origins forces application processes to stream heavy byte payloads across regional boundaries, exhausting "
                    "kernel socket memory and incurring expensive VM egress tariffs."
                ),
                "remediation_steps": [
                    "Step 1: Provision a dedicated Cloud Storage bucket (`gs://brightloaf-static-prod`) configured with Uniform Bucket-Level Access and public read permissions.",
                    "Step 2: Configure CORS policy on the Cloud Storage bucket to allow web fonts and SVG icons across all authorized Brightloaf domains.",
                    "Step 3: Create a Cloud CDN Backend Bucket pointing to the Cloud Storage bucket with `CACHE_ALL_STATIC` mode and custom cache keys stripping UTM query parameters.",
                    "Step 4: Update the Global External Application Load Balancer URL map to route all `/static/*` and `/media/*` path rules directly to the Cloud CDN Backend Bucket."
                ],
                "verify": (
                    "Run international HTTP client probes against static image URLs. Inspect response headers to verify `Via: 1.1 google` "
                    "and `Age: >0` confirm edge cache hits, with latency dropping from 3,200ms to under 25ms in Tokyo and London."
                ),
                "residual": (
                    "Stale files can persist at edge nodes if cache headers do not use asset fingerprinting or explicit TTLs. Continuous "
                    "integration pipelines must enforce unique content hashes on all production asset filenames."
                ),
                "diagram": (
                    "Web tier streams static images",
                    "Compute RAM & egress saturate",
                    "High latency & $5.8k bill",
                    "Attach Cloud CDN to GCS bucket",
                    "94% offload, sub-25ms edge latency"
                ),
                "facts": "Web VMs saturated on egress streaming media files; international latency exceeded 4s; monthly bill increased 340%.",
                "inference": "Serving static assets from application compute wastes CPU and kernel memory while multiplying network egress costs.",
                "expected": "Cloud CDN backend buckets absorb 90%+ of traffic at edge PoPs, reducing origin egress and achieving sub-30ms global delivery."
            },
            "lab": {
                "name": "Cloud CDN Backend Bucket and CORS Configuration",
                "file": "day-072-cdn-backend-bucket.md",
                "goal": "Configure a Cloud Storage backend bucket, establish CORS headers, enable Cloud CDN caching, and verify edge response headers.",
                "expected": "A complete architecture runbook with Cloud Storage CORS specification, CDN backend bucket definitions, and URL map routing rules.",
                "mode": "offline architecture specification, shell scripting, and configuration design; no cloud resources billed",
                "prereq": "Day 71 load balancer routing fundamentals",
                "preflight": "Review Cloud CDN caching documentation and Cloud Storage CORS configuration schemas.",
                "steps": [
                    "Create the CORS configuration file for Cloud Storage:\n\n```json\n[\n  {\n    \"origin\": [\"https://brightloaf.com\", \"https://www.brightloaf.com\"],\n    \"method\": [\"GET\", \"HEAD\", \"OPTIONS\"],\n    \"responseHeader\": [\"Content-Type\", \"Cache-Control\", \"ETag\"],\n    \"maxAgeSeconds\": 3600\n  }\n]\n```",
                    "Apply CORS and Uniform Bucket-Level Access to the origin bucket:\n\n```sh\n# Configure GCS bucket properties\ngcloud storage buckets update gs://brightloaf-static-prod \\\n  --uniform-bucket-level-access \\\n  --cors-file=cors-config.json\n```",
                    "Create the Cloud CDN backend bucket with static caching mode enabled:\n\n```sh\n# Create Cloud CDN backend bucket\ngcloud compute backend-buckets create static-asset-backend \\\n  --gcs-bucket-name=brightloaf-static-prod \\\n  --enable-cdn \\\n  --cache-mode=CACHE_ALL_STATIC \\\n  --default-ttl=86400 \\\n  --max-ttl=31536000 \\\n  --client-ttl=86400\n```",
                    "Attach the backend bucket to the Global External Load Balancer URL map:\n\n```sh\n# Update URL map with path matchers\ngcloud compute url-maps add-path-matcher brightloaf-global-lb \\\n  --default-service=order-api-backend \\\n  --path-matcher-name=main-routing \\\n  --backend-bucket-path-rules='/static/*=static-asset-backend'\n```",
                    "Perform edge cache hit verification:\n\n```sh\ncurl -IL https://brightloaf.com/static/bundle.8a3c.js\n```\nVerify response headers contain `Via: 1.1 google` and `Age: >0`."
                ],
                "verification": (
                    "Validate JSON syntax and routing rule assertions:\n\n```sh\npython3 -c \"import json; d = json.load(open('cors-config.json')); assert len(d) > 0; print('CORS JSON Validated Successfully')\"\n```\n\nConfirm output displays `CORS JSON Validated Successfully`."
                ),
                "trouble": (
                    "If browser requests fail with CORS errors, inspect response headers:\n\n```sh\ncurl -H \"Origin: https://brightloaf.com\" -H \"Access-Control-Request-Method: GET\" -I https://brightloaf.com/static/bundle.8a3c.js\n```\n\nVerify `Access-Control-Allow-Origin` header matches the requesting domain."
                ),
                "cleanup": "No remote cloud resources created; retain configuration files in local repository.",
                "accept": "A validated Cloud CDN backend bucket specification, complete CORS configuration, and routing runbook."
            }
        },
        {
            "key": "topic-03",
            "title": "Decoupled Microservices Communication: Cloud Run, Internal Ingress, and IAM Authentication",
            "overview": (
                "Architect zero-trust service-to-service communication across decoupled microservices. Enforce internal ingress "
                "controls, OpenID Connect (OIDC) identity tokens, and least-privilege IAM service account bindings."
            ),
            "preview": (
                "An internal catalog microservice is accidentally deployed with public ingress and unauthenticated access, "
                "exposing proprietary pricing data and internal database schemas to public scraping."
            ),
            "technical": (
                "#### 1. Zero-Trust Microservice Identity Architecture\n\n"
                "In traditional on-premises architectures, internal network perimeters (e.g. private subnets) were treated as "
                "implicitly trusted zones. Modern cloud-native architectures reject this perimeter-only model in favor of **Zero-Trust**: "
                "every service request must be explicitly authenticated, authorized, and encrypted, regardless of whether the caller "
                "originates from within the same VPC or across project boundaries.\n\n"
                "- **Identity vs. Network Boundaries:** Restricting network paths via VPC firewall rules provides defense-in-depth, "
                "but does not verify the cryptographic identity of the calling workload. An attacker who compromises a single compute "
                "container can pivot across internal subnets if services lack identity authentication.\n"
                "- **The OIDC Token Standard:** Google Cloud implements service identity verification using OpenID Connect (OIDC) "
                "identity tokens. When service A invokes service B, service A fetches a cryptographically signed JSON Web Token (JWT) "
                "from the local Google Cloud metadata server (`http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=TARGET_SERVICE_URL`).\n\n"
                "#### 2. Cloud Run Ingress Controls and IAM Invoker Bindings\n\n"
                "Cloud Run provides two orthogonal layers of security: network ingress controls and IAM authentication:\n\n"
                "  1. **Ingress Controls (`--ingress`):**\n"
                "     - `all`: The service accepts requests directly from the public internet and internal VPCs.\n"
                "     - `internal`: The service accepts traffic strictly from VPC networks within the same project or VPC Service "
                "Controls perimeter, and internal HTTP(S) Load Balancers. Internet traffic is rejected at the Google edge.\n"
                "     - `internal-and-cloud-load-balancing`: Restricts access to internal VPCs and Cloud Load Balancing VIPs.\n"
                "  2. **IAM Authorization (`roles/run.invoker`):**\n"
                "     - By default, Cloud Run rejects unauthenticated requests with HTTP 401 Unauthorized.\n"
                "     - Granting `roles/run.invoker` to `allUsers` enables public access.\n"
                "     - In zero-trust architectures, `roles/run.invoker` is granted strictly to the unique Google Service Account (GSA) "
                "of the calling service.\n\n"
                "```sh\n"
                "# Deploy target service with internal ingress only\n"
                "gcloud run deploy catalog-service \\\n"
                "  --image=gcr.io/brightloaf-prod/catalog:v1.4 \\\n"
                "  --ingress=internal \\\n"
                "  --no-allow-unauthenticated \\\n"
                "  --service-account=catalog-runner@brightloaf-prod.iam.gserviceaccount.com\n\n"
                "# Grant invoker permissions strictly to caller service account\n"
                "gcloud run services add-iam-policy-binding catalog-service \\\n"
                "  --member=serviceAccount:order-api-sa@brightloaf-prod.iam.gserviceaccount.com \\\n"
                "  --role=roles/run.invoker\n"
                "```\n\n"
                "#### 3. Client-Side Token Acquisition and Caching\n\n"
                "A critical operational pitfall is requesting a fresh OIDC token from the instance metadata server for every outgoing "
                "HTTP request. The metadata server throttles aggressive calls, introducing sub-second latency spikes. Production HTTP "
                "clients must cache OIDC tokens in memory and reuse them until 5 minutes before their expiration time (standard Google "
                "ID tokens have a 1-hour lifetime).\n\n"
                "```python\n"
                "# oidc_client.py - Cached Google OIDC Token Client\n"
                "import time\n"
                "import urllib.request\n"
                "import google.auth.transport.requests\n"
                "import google.oauth2.id_token\n\n"
                "class CachedOIDCClient:\n"
                "    def __init__(self, target_audience: str):\n"
                "        self.target_audience = target_audience\n"
                "        self.cached_token = None\n"
                "        self.expiry_time = 0\n"
                "        self.request = google.auth.transport.requests.Request()\n\n"
                "    def get_token(self) -> str:\n"
                "        current_time = time.time()\n"
                "        if not self.cached_token or current_time >= (self.expiry_time - 300):\n"
                "            # Fetch fresh token with target service URL as audience\n"
                "            self.cached_token = google.oauth2.id_token.fetch_id_token(self.request, self.target_audience)\n"
                "            # Google ID tokens expire in 3600 seconds\n"
                "            self.expiry_time = current_time + 3600\n"
                "        return self.cached_token\n"
                "```\n\n"
                "#### 4. Dataplane V2 (eBPF) Network Policies\n\n"
                "When microservices run on Google Kubernetes Engine (GKE), GKE Dataplane V2 (powered by Cilium and eBPF) enforces "
                "kernel-level `NetworkPolicy` primitives. While IAM governs application identity at the HTTP/gRPC layer, Kubernetes "
                "Network Policies enforce layer 3/4 egress and ingress rules, preventing compromised pods from initiating lateral "
                "port scans across cluster namespaces.\n\n"
                "#### 5. Architectural Trade-offs: Service-to-Service Authentication Mechanisms\n\n"
                "| Mechanism | Authentication Protocol | Overhead / Latency | Key Rotation Complexity | Ingress Scope | Best Suited For |\n"
                "|---|---|---|---|---|---|\n"
                "| **Google OIDC ID Tokens** | Cryptographic JWT signed by Google | < 1 ms (cached) | Fully managed by Google Cloud IAM | Cloud Run, App Engine, Cloud Functions | Serverless microservices, cross-project service invocation |\n"
                "| **mTLS (Service Mesh / Istio)** | X.509 Mutual TLS Handshake | ~2–5 ms per connection handshake | Automated via Mesh CA (Citadel / Private CA) | GKE Cluster / Mesh VPC | Complex microservices requiring L7 traffic routing, canary, telemetry |\n"
                "| **Shared API Keys** | Static shared secrets in HTTP headers | Negligible | High (requires redeployment / Secrets Manager update) | Public or Private | Third-party developer APIs; NOT recommended for internal microservices |\n"
                "| **VPC-SC Perimeter Only** | IP / Project boundary enforcement | Zero (no cryptographic check) | Managed via Access Context Manager | GCP API Boundary | Bulk data exfiltration prevention; cannot replace service authentication |\n"
                "| **IAM Database Authentication** | Ephemeral OAuth2 access tokens | 200–400ms handshake | Automated via Cloud SQL Auth Proxy | Database Port (5432/3306) | Zero-trust connection to Cloud SQL without static passwords |\n"
            ),
            "questions": [
                "What is the difference between Cloud Run ingress controls and IAM authentication bindings?",
                "Why must the `audience` claim in an OIDC ID token match the exact URL of the target Cloud Run service?",
                "How does caching OIDC tokens prevent metadata server rate-limit exhaustion during high concurrency?",
                "Why is a private VPC network perimeter insufficient for achieving Zero-Trust architecture?",
            ],
            "reference": "https://docs.cloud.google.com/run/docs/authenticating/service-to-service",
            "reference_label": "Google Cloud Run Documentation: Service-to-service authentication",
            "scenario": {
                "scenario": (
                    "During an emergency operational patch to resolve internal routing errors between the order-processing service and the "
                    "catalog service, a platform engineer redeployed the internal catalog service with `--allow-unauthenticated` and default "
                    "ingress (`all`). Three weeks later, an automated security vulnerability scanner discovered that the proprietary product "
                    "pricing catalog, inventory forecasts, and supplier cost margins were publicly accessible via a direct `.run.app` URL "
                    "over the open internet without any authentication."
                ),
                "impact": (
                    "P1 compliance and data exfiltration incident. Over 45,000 internal wholesale pricing records were harvested by an "
                    "external competitor web scraper. Audit violation cited under ISO 27001 Annex A.9 (Access Control). Emergency executive "
                    "escalation and mandatory engineering review across all serverless workloads."
                ),
                "constraints": (
                    "Enforce zero public internet access to the catalog service; require cryptographically signed service account credentials "
                    "for all internal callers; do not introduce manual certificate management overhead; ensure sub-10ms inter-service latency."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect Cloud Run IAM policy via the service IAM inspection CLI; observe `allUsers` bound to `roles/run.invoker`.",
                    "Step 2: Inspect Cloud Run ingress settings; observe ingress set to `all` (accepting public internet traffic).",
                    "Step 3: Review Cloud Logging audit logs; filter by `resource.type=\"cloud_run_revision\"` and observe requests originating from public external IP blocks.",
                    "Step 4: Check Order API client code; observe missing `Authorization: Bearer` token generation logic in HTTP client calls."
                ],
                "root": (
                    "Bypassing authentication and ingress controls during an incident patch left internal microservice APIs exposed to the "
                    "public internet. Lack of automated CI/CD policy-as-code enforcement allowed an unauthenticated Cloud Run service to "
                    "pass into production."
                ),
                "remediation_steps": [
                    "Step 1: Immediately revoke public access: remove the `allUsers` IAM binding from `roles/run.invoker` on `catalog-service`.",
                    "Step 2: Reconfigure Cloud Run ingress to `--ingress=internal`, restricting traffic strictly to the VPC and internal load balancers.",
                    "Step 3: Bind `roles/run.invoker` exclusively to `serviceAccount:order-api-sa@brightloaf-prod.iam.gserviceaccount.com`.",
                    "Step 4: Update the calling client application to fetch and attach Google OIDC identity tokens with target service audience in all outbound HTTP requests."
                ],
                "verify": (
                    "Execute an unauthenticated curl request to the catalog service and confirm HTTP 403 Forbidden. Execute an authenticated "
                    "request using the Order API service account identity token and confirm HTTP 200 OK."
                ),
                "residual": (
                    "Token acquisition adds a sub-millisecond local metadata server latency overhead; tokens must be cached until expiry to "
                    "avoid metadata rate limits. Workloads calling across VPCs require Shared VPC or Serverless VPC Access connectors."
                ),
                "diagram": (
                    "Emergency patch disables auth",
                    "allUsers granted run.invoker",
                    "Public scraping of pricing data",
                    "Set --ingress=internal & IAM OIDC",
                    "Zero-trust verified, 403 to public"
                ),
                "facts": "Cloud Run service had --allow-unauthenticated and ingress=all; internal pricing data scraped publicly.",
                "inference": "Disabling authentication to bypass networking configuration breaks zero-trust boundaries and violates data compliance.",
                "expected": "Services enforce internal ingress and strictly validate caller OIDC tokens signed by Google Cloud IAM."
            },
            "lab": {
                "name": "Zero-Trust Microservice Authentication and Ingress Enforcement",
                "file": "day-072-zero-trust-auth.md",
                "goal": "Configure internal ingress and least-privilege IAM invoker permissions, then develop a Python client with OIDC token caching.",
                "expected": "A secure Cloud Run deployment script, an IAM policy binding definition, and a verified Python OIDC client script.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 71 service decoupling and IAM fundamentals",
                "preflight": "Review Google Cloud Run IAM authentication docs and OIDC token validation schemas.",
                "steps": [
                    "Define the least-privilege Google Service Accounts:\n\n```sh\n# Create caller and receiver service accounts\ngcloud iam service-accounts create order-service-sa --display-name='Order Processing Service'\ngcloud iam service-accounts create catalog-service-sa --display-name='Catalog Internal Service'\n```",
                    "Grant `roles/run.invoker` strictly to the caller service account on the target service:\n\n```sh\n# Bind invoker role to caller service account only\ngcloud run services add-iam-policy-binding catalog-service \\\n  --region=us-central1 \\\n  --member='serviceAccount:order-service-sa@brightloaf-prod.iam.gserviceaccount.com' \\\n  --role='roles/run.invoker'\n```",
                    "Deploy the target microservice with internal ingress enforced:\n\n```sh\n# Deploy with internal ingress and strict authentication\ngcloud run deploy catalog-service \\\n  --image=gcr.io/brightloaf-prod/catalog:v1.4 \\\n  --ingress=internal \\\n  --no-allow-unauthenticated \\\n  --service-account=catalog-service-sa@brightloaf-prod.iam.gserviceaccount.com\n```",
                    "Write the production Python client script with token caching (`oidc_invoker.py`):\n\n```python\n# oidc_invoker.py\nimport time\n\nclass TokenManager:\n    def __init__(self, audience: str):\n        self.audience = audience\n        self.token = None\n        self.expiry = 0\n\n    def get_token(self) -> str:\n        now = time.time()\n        if not self.token or now >= self.expiry:\n            # Simulate fetching token from metadata server\n            self.token = f\"mock_token_for_{self.audience}_{int(now)}\"\n            self.expiry = now + 300  # 5-minute cache\n            print(f\"[INFO] Fetched fresh OIDC token for {self.audience}\")\n        return self.token\n\nclient = TokenManager(\"https://catalog-service-xyz.a.run.app\")\nt1 = client.get_token()\nt2 = client.get_token()\nassert t1 == t2, \"Token caching failed!\"\nprint(\"OIDC Token Manager Verified: Caching is active.\")\n```",
                    "Execute the client script to verify token caching logic:\n\n```sh\npython3 oidc_invoker.py\n```"
                ],
                "verification": (
                    "Verify token caching and policy specification:\n\n```sh\npython3 -c \"import oidc_invoker; t = oidc_invoker.TokenManager('test'); assert t.get_token() == t.get_token(); print('OIDC Verification Passed')\"\n```\n\nConfirm output displays `OIDC Verification Passed`."
                ),
                "trouble": (
                    "If caller receives HTTP 403 Forbidden, inspect the IAM policy binding:\n\n```sh\ngcloud run services get-iam-policy catalog-service --region=us-central1\n```\n\nVerify the caller service account email is listed under `roles/run.invoker`."
                ),
                "cleanup": "No remote cloud resources created; retain configuration files in local repository.",
                "accept": "A validated Cloud Run IAM configuration, internal ingress deployment script, and working OIDC client implementation."
            }
        },
        {
            "key": "topic-04",
            "title": "High-Throughput Event Ingestion and Deduplication with Pub/Sub and BigQuery",
            "overview": (
                "Design high-velocity event ingestion pipelines using Google Cloud Pub/Sub and BigQuery. Implement exactly-once "
                "delivery, handle network retries, and master database deduplication patterns."
            ),
            "preview": (
                "An e-commerce order analytics pipeline ingests duplicate checkout events due to network retries, causing "
                "BigQuery sales dashboards to double-count $450,000 in Black Friday revenue."
            ),
            "technical": (
                "#### 1. At-Least-Once Delivery Mechanics in Distributed Messaging\n\n"
                "In high-scale distributed systems, achieving zero message loss under network partitions requires acknowledgment-based "
                "protocols. Google Cloud Pub/Sub guarantees **at-least-once delivery** by default. When an application subscriber processes "
                "a message but network congestion delays the acknowledgment (`ACK`) past the configured `ackDeadlineSeconds`, the Pub/Sub "
                "broker assumes delivery failed and automatically redelivers the message to another subscriber instance.\n\n"
                "- **The Duplicate Event Trap:** If an e-commerce order checkout event (`order_id: 98412`, `amount: $350`) is redelivered, "
                "a naive streaming insert pipeline will write two identical rows into the BigQuery `orders_fact` table. Downstream executive "
                "financial dashboards, revenue reporting, and inventory allocation models will double-count revenue and deplete inventory "
                "ghost records.\n\n"
                "#### 2. Cloud Pub/Sub Exactly-Once Delivery (EOD)\n\n"
                "Google Cloud Pub/Sub provides native **Exactly-Once Delivery** on pull and push subscriptions within a single cloud region:\n\n"
                "- When EOD is enabled, Pub/Sub tracks acknowledgment states globally within the region. If an `ACK` is sent before the "
                "deadline, redelivery is guaranteed not to occur.\n"
                "- **Subscription Modifying API:**\n\n"
                "```sh\n"
                "# Create Pub/Sub subscription with Exactly-Once Delivery enabled\n"
                "gcloud pubsub subscriptions create order-events-eod-sub \\\n"
                "  --topic=brightloaf-order-events \\\n"
                "  --enable-exactly-once-delivery \\\n"
                "  --ack-deadline=60 \\\n"
                "  --message-retention-duration=7d\n"
                "```\n\n"
                "- **Limitations of Broker-Level EOD:** Exactly-Once Delivery does NOT protect against **publisher-side duplicates**. If "
                "a mobile client or web checkout microservice publishes an event, experiences a network timeout before receiving the Pub/Sub "
                "publish response, and retries the publish call, Pub/Sub assigns two distinct `message_id` values to the two identical payloads. "
                "Therefore, downstream consumers must implement **business-key deduplication**.\n\n"
                "#### 3. BigQuery Streaming Ingestion and Deduplication Patterns\n\n"
                "BigQuery offers two primary streaming ingestion mechanisms:\n\n"
                "  1. **BigQuery Storage Write API (Recommended):** Supports stream-level exactly-once semantics by specifying an `offset` "
                "within a `COMMITTED` stream. Appending duplicate records with previously committed offsets is rejected by BigQuery.\n"
                "  2. **Legacy `tabledata.insertAll` with `insertId`:** When rows are inserted with a unique `insertId` (e.g. `order_id`), "
                "BigQuery deduplicates rows with the same `insertId` over a best-effort 1-minute window. However, this window is insufficient "
                "for retries occurring after several minutes.\n\n"
                "#### 4. Batch and Windowed Deduplication via SQL MERGE\n\n"
                "For bulletproof idempotent persistence, data engineers stage incoming raw events into a partitioned staging table "
                "(`orders_staging`), and execute periodic atomic `MERGE` statements into the final production fact table:\n\n"
                "```sql\n"
                "-- Atomic Upsert Deduplication via BigQuery MERGE\n"
                "MERGE INTO `brightloaf_dw.orders_fact` AS target\n"
                "USING (\n"
                "  SELECT * EXCEPT(row_num)\n"
                "  FROM (\n"
                "    SELECT *,\n"
                "      ROW_NUMBER() OVER(\n"
                "        PARTITION BY order_id\n"
                "        ORDER BY event_timestamp DESC\n"
                "      ) as row_num\n"
                "    FROM `brightloaf_dw.orders_staging`\n"
                "    WHERE DATE(ingestion_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)\n"
                "  )\n"
                "  WHERE row_num = 1\n"
                ") AS source\n"
                "ON target.order_id = source.order_id\n"
                "WHEN MATCHED AND source.event_timestamp > target.event_timestamp THEN\n"
                "  UPDATE SET\n"
                "    target.status = source.status,\n"
                "    target.total_amount = source.total_amount,\n"
                "    target.last_updated = source.event_timestamp\n"
                "WHEN NOT MATCHED THEN\n"
                "  INSERT (order_id, customer_id, total_amount, status, created_at, last_updated)\n"
                "  VALUES (source.order_id, source.customer_id, source.total_amount, source.status, source.event_timestamp, source.event_timestamp);\n"
                "```\n\n"
                "#### 5. Architectural Trade-offs: Ingestion & Deduplication Patterns\n\n"
                "| Deduplication Strategy | Processing Layer | Latency Window | Compute Cost | Guaranteed Semantics | Ideal Workload |\n"
                "|---|---|---|---|---|---|\n"
                "| **Pub/Sub Exactly-Once (EOD)** | Messaging Broker (Regional) | Real-time (within ACK window) | Standard Pub/Sub pricing | Exactly-once delivery from broker to subscriber | Inter-service microservice triggers, order orchestration |\n"
                "| **Storage Write API Offset** | BigQuery Ingestion Stream | Real-time (< 2 seconds) | Low (per-GB write charge) | Exactly-once stream append | Real-time analytics ingestion pipelines |\n"
                "| **Redis SETNX / Bloom Filter** | In-Memory Ephemeral Cache | Sub-millisecond | Memory capacity allocation | Idempotent key deduplication (TTL bounded) | Payment gateway duplicate submission guard (Day 64 invariant) |\n"
                "| **Scheduled BigQuery MERGE** | BigQuery Data Warehouse | 10–60 minutes (Batch window) | BigQuery Slot / Query compute | 100% deterministic ACID deduplication | Financial reporting, revenue reconciliation, BI dashboards |\n"
                "| **Relational ON CONFLICT DO UPDATE** | PostgreSQL / Spanner Database | Immediate (ACID commit) | Database CPU / IOPS | Absolute transactional guarantee | Core order persistence, customer balance ledger |\n"
            ),
            "questions": [
                "Why does Pub/Sub Exactly-Once Delivery fail to prevent duplicates caused by client-side network retries?",
                "What is the difference between BigQuery Storage Write API offset deduplication and legacy insertId deduplication?",
                "How does the `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` SQL pattern ensure deterministic deduplication in BigQuery?",
                "Under what operational scenario is Redis `SETNX` preferred over database-level SQL deduplication?",
            ],
            "reference": "https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery",
            "reference_label": "Google Cloud Pub/Sub Documentation: Exactly-once delivery",
            "scenario": {
                "scenario": (
                    "During a Black Friday promotional peak, Brightloaf's order analytics ingestion pipeline processed 140,000 checkout "
                    "events through Pub/Sub into a streaming BigQuery dataset. Due to heavy network congestion between the application "
                    "cluster and the Pub/Sub regional endpoint, the checkout microservice experienced transient HTTP 503 errors and "
                    "automatically retried event publication. The BigQuery real-time dashboard reported $980,000 in gross merchandise "
                    "value (GMV), whereas the core transactional PostgreSQL database recorded only $530,000 in settled orders. Executive "
                    "management was presented with conflicting financial metrics, triggering a freeze on marketing ad spend."
                ),
                "impact": (
                    "P1 financial reporting failure and data corruption. Financial dashboards overstated revenue by 84.9% ($450,000 artificial "
                    "revenue phantom). Inventory planning pipelines automatically initiated unneeded replenishment orders with suppliers. "
                    "Data engineering spent 36 hours executing manual database deduplication scripts."
                ),
                "constraints": (
                    "Preserve sub-2-second end-to-end ingestion latency for operational alerts; ensure 100% mathematical accuracy on financial "
                    "metrics; eliminate duplicate rows in BigQuery without incurring massive multi-terabyte query scanning costs."
                ),
                "diagnostic_steps": [
                    "Step 1: Execute verification SQL in BigQuery counting total rows versus distinct `order_id` values: `SELECT count(1), count(distinct order_id) FROM orders_fact`; identify 48,200 duplicate records.",
                    "Step 2: Inspect Pub/Sub subscription metrics in Cloud Monitoring; observe redelivery rate surged to 18% during peak traffic.",
                    "Step 3: Audit client-side publisher configuration; discover aggressive retry policy with exponential backoff missing client-side request idempotency tokens.",
                    "Step 4: Check BigQuery table configuration; observe direct streaming inserts into production fact tables without deduplication staging or MERGE reconciliation."
                ],
                "root": (
                    "Client-side publish retries generated multiple unique Pub/Sub messages for the same checkout event. Downstream BigQuery "
                    "streaming ingestion inserted all incoming messages directly into fact tables without staging or idempotent deduplication logic."
                ),
                "remediation_steps": [
                    "Step 1: Enable Exactly-Once Delivery (EOD) on the Pub/Sub subscription to eliminate broker-side redeliveries.",
                    "Step 2: Introduce an in-memory Redis deduplication guard (`SETNX order:{id} EX 86400`) at the publisher gateway to suppress duplicate publishes within 24 hours.",
                    "Step 3: Redirect BigQuery streaming ingestion to a partitioned staging table (`orders_staging`) with a 3-day partition expiration.",
                    "Step 4: Deploy an hourly scheduled BigQuery `MERGE` query that atomically deduplicates staging records into the final `orders_fact` table using `ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY event_timestamp DESC)`."
                ],
                "verify": (
                    "Execute the reconciliation SQL script comparing row count and distinct `order_id` count across the production fact table. "
                    "Verify `count(1) == count(distinct order_id)` confirms zero duplicate records remain, and financial dashboards match "
                    "settled PostgreSQL transaction totals to the exact cent."
                ),
                "residual": (
                    "Streaming real-time views that query staging before the hourly MERGE runs must query a deduplicated SQL VIEW rather "
                    "than querying the raw staging table directly."
                ),
                "diagram": (
                    "Network retry duplicates events",
                    "Direct stream into BigQuery",
                    "Revenue double-counted (+85%)",
                    "Enable EOD & scheduled MERGE dedup",
                    "Deterministic counts, zero phantom data"
                ),
                "facts": "BigQuery reported $980k while Cloud SQL showed $530k; 48,200 duplicate rows caused by publisher network retries.",
                "inference": "Messaging brokers cannot prevent publisher-side duplicate events; deduplication must be enforced at storage boundaries.",
                "expected": "Staging tables combined with atomic MERGE deduplication guarantee exactly-once persistence in data warehouses."
            },
            "lab": {
                "name": "High-Throughput Ingestion and BigQuery Deduplication Runbook",
                "file": "day-072-ingestion-dedup.md",
                "goal": "Build an end-to-end ingestion runbook with Pub/Sub Exactly-Once Delivery configuration and BigQuery MERGE deduplication scripts.",
                "expected": "A complete data pipeline specification, Pub/Sub CLI commands, and an executable BigQuery SQL deduplication script.",
                "mode": "offline architecture specification, SQL scripting, and Python data simulation; no cloud resources billed",
                "prereq": "Day 71 event-driven concepts and Day 64 single-fulfillment invariants",
                "preflight": "Review Pub/Sub Exactly-Once Delivery constraints and BigQuery partitioned table pricing.",
                "steps": [
                    "Create the Pub/Sub topic and Exactly-Once subscription specification:\n\n```sh\n# Create Pub/Sub topic\ngcloud pubsub topics create brightloaf-orders-stream\n\n# Create subscription with EOD enabled\ngcloud pubsub subscriptions create brightloaf-orders-eod-sub \\\n  --topic=brightloaf-orders-stream \\\n  --enable-exactly-once-delivery \\\n  --ack-deadline=60\n```",
                    "Write the production BigQuery MERGE deduplication script (`dedup_orders.sql`):\n\n```sql\n-- dedup_orders.sql\nMERGE INTO `brightloaf_dw.orders_fact` AS target\nUSING (\n  SELECT * EXCEPT(row_num)\n  FROM (\n    SELECT *,\n      ROW_NUMBER() OVER(\n        PARTITION BY order_id\n        ORDER BY event_timestamp DESC\n      ) as row_num\n    FROM `brightloaf_dw.orders_staging`\n    WHERE ingestion_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)\n  )\n  WHERE row_num = 1\n) AS source\nON target.order_id = source.order_id\nWHEN MATCHED THEN\n  UPDATE SET target.status = source.status, target.amount = source.amount\nWHEN NOT MATCHED THEN\n  INSERT (order_id, customer_id, amount, status, event_timestamp)\n  VALUES (source.order_id, source.customer_id, source.amount, source.status, source.event_timestamp);\n```",
                    "Develop an offline Python simulation script to verify idempotency math (`test_dedup.py`):\n\n```python\n# test_dedup.py\nimport sqlite3\n\nconn = sqlite3.connect(':memory:')\ncur = conn.cursor()\ncur.execute('''CREATE TABLE staging (order_id TEXT, amount REAL, ts INT)''')\ncur.execute('''CREATE TABLE fact (order_id TEXT PRIMARY KEY, amount REAL, ts INT)''')\n\n# Insert simulated duplicate stream (order_1 arrives twice due to retry)\nevents = [('ord_1', 100.0, 10), ('ord_1', 100.0, 11), ('ord_2', 50.0, 12)]\ncur.executemany('INSERT INTO staging VALUES (?,?,?)', events)\n\n# Emulate BigQuery MERGE deduplication\ncur.execute('''\nINSERT INTO fact\nSELECT order_id, amount, ts\nFROM (\n  SELECT order_id, amount, ts,\n    ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY ts DESC) as rn\n  FROM staging\n) WHERE rn = 1\n''')\nconn.commit()\n\ncur.execute('SELECT count(1), count(distinct order_id) FROM fact')\ntotal, distinct_cnt = cur.fetchone()\nassert total == distinct_cnt == 2, 'Deduplication failed!'\nprint(f'Deduplication Verified: Total Rows = {total}, Distinct = {distinct_cnt}')\n```",
                    "Execute the Python deduplication verification test:\n\n```sh\npython3 test_dedup.py\n```"
                ],
                "verification": (
                    "Run verification assertion test:\n\n```sh\npython3 -c \"import test_dedup; print('Deduplication Script Test Passed Successfully')\"\n```\n\nConfirm output displays `Deduplication Script Test Passed Successfully`."
                ),
                "trouble": (
                    "If deduplication queries trigger high slot consumption in BigQuery, inspect query execution plans:\n\n```sh\ncat dedup_orders.sql\n```\n\nVerify the query filters on `ingestion_time` partition boundaries to limit scanned bytes."
                ),
                "cleanup": "No remote cloud resources created; retain SQL scripts and test runners in local repository.",
                "accept": "A validated Pub/Sub EOD subscription runbook, BigQuery MERGE deduplication SQL script, and verified Python test runner."
            }
        }
    ]
}
