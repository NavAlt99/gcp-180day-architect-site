"""day_data_074.py — Exhaustive architecture data specification for Day 74.

Covers Regional and Tenant Boundaries: Multi-Region Active-Active vs Active-Passive,
Multi-Tenant SaaS Isolation Models, Enterprise Landing Zones, and Architectural Anti-Patterns.
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 74

DATA = {
    "day": 74,
    "part1_intro": (
        "Day 74 explores the macroscopic boundaries of cloud architecture: regional survivability, multi-tenant isolation, "
        "and enterprise landing zones. Moving beyond single-region deployments, architects confront the physical realities "
        "of cross-continental speed-of-light network latency, distributed CAP theorem trade-offs, and split-brain fencing "
        "under regional network partitions. Concurrently, this session examines the multi-tenant SaaS spectrum—balancing "
        "the cryptographic blast radius of Project-per-Tenant silos against the cost efficiency of pooled database Row-Level "
        "Security. Finally, architects blueprint Google Cloud Enterprise Foundations (Landing Zones) and diagnose four "
        "fatal architectural anti-patterns that collapse enterprise scalability."
    ),
    "exit_summary": (
        "Formalized multi-region active-passive database fencing procedures preventing split-brain corruption; constructed "
        "a multi-tenant SaaS isolation trade-off matrix; authored a production Landing Zone resource hierarchy with Shared VPC "
        "governance; executed simulation scripts proving the latency compounding of chatty cross-region microservice anti-patterns."
    ),
    "part2_intro": (
        "Architecting enterprise boundaries requires rigid separation of blast domains. The sections below analyze the network "
        "physics of multi-region replication, the software and hardware isolation primitives of multi-tenant SaaS, the "
        "governance hierarchy of landing zones, and prescriptive remedies for four critical anti-patterns."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Boundary Dimension</th>
      <th>Google Cloud Primitive</th>
      <th>Primary Blast Radius / Threat Model</th>
      <th>Architectural Protection Pattern</th>
      <th>Target SLA / Isolation Guarantee</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Multi-Region Active-Passive</strong></td>
      <td>Cloud SQL Regional HA + Cross-Region Replica</td>
      <td>Split-brain dual-master write divergence</td>
      <td>Automated primary fencing prior to replica promotion</td>
      <td>RTO &lt; 15 min; RPO &lt; 60 s; 0 split-brain</td>
    </tr>
    <tr>
      <td><strong>Multi-Region Active-Active</strong></td>
      <td>Cloud Spanner (nam6 / Multi-Region)</td>
      <td>Write conflicts across geographic regions</td>
      <td>TrueTime atomic clock external consistency (Paxos)</td>
      <td>99.999% Availability; RTO = 0; RPO = 0</td>
    </tr>
    <tr>
      <td><strong>SaaS Tenant Isolation (Silo)</strong></td>
      <td>Dedicated GCP Project per Tenant (Terraform)</td>
      <td>Cross-tenant credential or quota contamination</td>
      <td>Hard cryptographic, IAM, and network boundaries</td>
      <td>100% blast radius containment; zero leakage</td>
    </tr>
    <tr>
      <td><strong>SaaS Tenant Isolation (Pool)</strong></td>
      <td>PostgreSQL Row-Level Security (RLS)</td>
      <td>Application bug omitting tenant_id filter</td>
      <td>Database engine kernel-level RLS policies</td>
      <td>Sub-millisecond query time; high tenant density</td>
    </tr>
    <tr>
      <td><strong>Enterprise Landing Zone</strong></td>
      <td>Resource Hierarchy + Shared VPC + Org Policies</td>
      <td>Uncontrolled project sprawl; shadow IT networks</td>
      <td>Hub-and-spoke networking; central security baselines</td>
      <td>100% policy compliance; centralized egress control</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 74: Enterprise Regional and Tenant Isolation Topology",
        "desc": "Logical multi-region traffic routing, multi-tenant isolation boundaries, and centralized landing zone governance.",
        "nodes": [
            ("Client Ingress", "Global Anycast External ALB\\n+ Multi-Region Health Routing"),
            ("Tenant Compute", "GKE Namespaces / Cloud Run\\n+ In-VPC Tenant Context"),
            ("Persistence Tier", "Cloud Spanner Active-Active\\nOR Fenced Cloud SQL Replicas"),
            ("Foundation Governance", "Resource Hierarchy & Shared VPC\\n+ Central Org Policy Guardrails"),
        ],
        "caption": "Figure 74.1: Comprehensive enterprise boundary model combining multi-region survivability with tenant isolation."
    },
    "part3_intro": (
        "The following field cases examine severe architectural disasters resulting from misconfigured regional and tenant boundaries. "
        "Each case details the real-world scenario, quantifiable impact, diagnostic trace, defensible remediation sequence, "
        "and responsive dual-lane SVG diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises provide production-grade, executable configurations and verification scripts for "
        "simulating multi-region failover fencing, configuring PostgreSQL Row-Level Security, drafting Landing Zone "
        "policies, and modeling the latency compounding of chatty cross-region anti-patterns."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Multi-Region Active-Active vs. Active-Passive Architectures",
            "overview": (
                "Design resilient multi-region architectures. Master cross-region replication lag, CAP theorem trade-offs, "
                "split-brain fencing mechanisms, and Cloud Spanner TrueTime multi-region active-active synchronization."
            ),
            "preview": (
                "An automated cross-region database failover promotes a secondary read replica during a network hiccup while the old primary "
                "is still accepting writes, creating two unsynchronized master databases and permanently corrupting 420 customer orders."
            ),
            "technical": (
                "#### 1. Cross-Region Latency and the CAP Theorem Speed-of-Light Constraint\n\n"
                "Designing across multiple cloud regions introduces inescapable physical networking limits. The physical fiber distance "
                "between Google Cloud `us-central1` (Iowa) and `europe-west3` (Frankfurt) is over 7,000 kilometers, incurring a minimum "
                "round-trip time (RTT) of 95 milliseconds. Under the CAP Theorem, a distributed system must choose between **Consistency** "
                "and **Availability** during network partitions:\n\n"
                "- **Synchronous Two-Phase Commit (2PC):** If a transaction requires synchronous acknowledgments across regions before committing, "
                "every database write incurs a 100ms+ latency penalty. A network cut between continents stalls all transactional writes.\n"
                "- **Asynchronous Replication:** The primary region commits transactions locally in sub-5ms, streaming WAL logs asynchronously "
                "to the secondary region. While latency is minimized, there is always an **RPO Replication Lag** (typically 1 to 5 seconds). "
                "If the primary region suffers a sudden catastrophic failure, transactions committed in the primary that have not yet replicated "
                "are permanently lost.\n\n"
                "#### 2. Active-Passive Failover and the Split-Brain Fencing Problem\n\n"
                "In an active-passive topology, Region A serves 100% of write traffic while Region B operates a warm standby or read replica. "
                "The most catastrophic failure mode in active-passive systems is **Split-Brain**:\n\n"
                "- If an interconnect partition occurs, Region B's monitoring agent may conclude Region A is dead because heartbeats fail.\n"
                "- If Region B automatically promotes its read replica to a standalone primary while Region A's compute instances are still "
                "accepting customer writes, the enterprise now has **two independent primary databases** accepting contradictory mutations.\n"
                "- When network connectivity restores, the datasets have irreconcilably diverged. Merging conflicting order IDs, inventory "
                "counts, and financial balances requires weeks of manual forensic accounting.\n\n"
                "**Positive Fencing Mandate:** A secondary replica must NEVER be promoted until the orchestrator positively fences (shuts down "
                "or revokes network access to) the old primary database.\n\n"
                "#### 3. Active-Active Multi-Region Consistency with Cloud Spanner\n\n"
                "True multi-region active-active architectures eliminate passive idle infrastructure by serving writes and reads concurrently "
                "from multiple continents. Google Cloud Spanner achieves this without split-brain using **TrueTime**:\n\n"
                "- Cloud Spanner utilizes atomic clocks and GPS receivers integrated directly into Google's datacenter hardware.\n"
                "- TrueTime represents time not as a discrete tick, but as an interval `[t.earliest, t.latest]` with guaranteed bounded "
                "uncertainty (`epsilon < 7ms`).\n"
                "- Spanner uses Paxos consensus groups across regions. When a transaction commits, the leader waits out the clock uncertainty "
                "before releasing locks (**Commit Wait**), guaranteeing **External Consistency** (linearizability) globally without locks.\n\n"
                "#### 4. Global External Application Load Balancer Anycast Routing\n\n"
                "Client traffic steering across regions is managed via Google's Global External Application Load Balancers using a single Anycast VIP. "
                "BGP routes clients to the nearest Google edge PoP. If a regional backend service fails its health checks, the global load balancer "
                "automatically steers incoming HTTP requests to the secondary region in under 30 seconds with zero DNS propagation delays.\n\n"
                "#### 5. Architectural Trade-offs: Multi-Region Availability Topologies\n\n"
                "| Topology Model | Write Latency | Read Latency | RTO (Recovery Time) | RPO (Data Loss Window) | Operational Cost Multiplier | Failure Risk Profile |\n"
                "|---|---|---|---|---|---|---|\n"
                "| **Active-Passive (Cold Backup)** | Sub-10ms (Local) | Sub-10ms (Local) | 4 – 12 Hours | 1 – 24 Hours | 1.1x (Storage only) | Prolonged downtime during disaster |\n"
                "| **Active-Passive (Warm Standby)** | Sub-10ms (Local) | Sub-10ms (Local) | 5 – 15 Minutes | < 30 Seconds | 1.5x (Idle DB replica) | Split-brain risk if fencing fails |\n"
                "| **Active-Passive (Hot Standby)** | Sub-10ms (Local) | Sub-10ms (Local) | < 60 Seconds | < 5 Seconds | 2.0x (100% idle compute) | High cost; split-brain risk |\n"
                "| **Active-Active (Spanner nam6)** | 30 – 60ms (Paxos) | < 5ms (Local Read) | Near Zero (< 1s) | Absolute Zero (0s) | 3.0x – 4.0x (Distributed nodes) | Zero split-brain; higher base cost |\n"
            ),
            "questions": [
                "Why does synchronous cross-region replication inevitably degrade transactional write performance?",
                "What exact sequence of operations constitutes 'positive fencing' during active-passive database failover?",
                "How does Cloud Spanner's TrueTime technology prevent distributed split-brain write conflicts?",
                "What is the operational advantage of Global Anycast VIP routing over traditional DNS-based failover (GeoDNS)?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/disaster-recovery",
            "reference_label": "Google Cloud Architecture Center: Disaster recovery planning guide",
            "scenario": {
                "scenario": (
                    "During a scheduled quarterly disaster recovery rehearsal, Brightloaf platform engineers simulated a regional failure "
                    "in `us-central1`. The automated orchestration script triggered a promotion of the cross-region Cloud SQL read replica "
                    "in `us-east4`. However, because the primary region's VPC network remained reachable from certain internal subnets, "
                    "the primary database was never fenced or shut down. For 22 minutes during the drill, the frontend web servers in "
                    "`us-central1` continued writing new orders to the old primary, while newly routed traffic in `us-east4` wrote orders "
                    "to the promoted replica. When engineers declared the drill complete and attempted to resume normal operations, they "
                    "discovered 420 conflicting customer orders with overlapping serial IDs and divergent inventory allocations."
                ),
                "impact": (
                    "Severe P1 data corruption incident. 420 customer orders were duplicated or overwritten. Data engineering and finance "
                    "spent 72 hours conducting manual database reconciliation. Production checkout was frozen for 6 hours to prevent further "
                    "divergence. Estimated business cost: $140,000 in lost sales and manual engineering overtime."
                ),
                "constraints": (
                    "Enforce positive fencing before any database promotion can execute; achieve RTO < 15 minutes and RPO < 60 seconds; "
                    "guarantee zero split-brain data corruption under any network partition scenario."
                ),
                "diagnostic_steps": [
                    "Step 1: Compare transaction logs between primary `us-central1` and promoted replica `us-east4`; identify 420 transactions committed with identical auto-incrementing primary keys but different customer payloads.",
                    "Step 2: Inspect Cloud Audit Logs for the failover orchestrator service account; discover the `promote-replica` API was called without prior execution of `patch --authorized-networks=''` on the primary.",
                    "Step 3: Review Load Balancer health check logs; observe that backends in `us-central1` remained marked HEALTHY during the drill because the local compute VMs were never signaled to stop.",
                    "Step 4: Check database configuration; confirm Cloud SQL was running standard PostgreSQL without distributed lock managers or fencing tokens."
                ],
                "root": (
                    "The failover automation script promoted the asynchronous read replica without positively fencing (disabling network access "
                    "to) the old primary database. Both databases accepted concurrent writes, creating dual-master split-brain data divergence."
                ),
                "remediation_steps": [
                    "Step 1: Rewrite the failover orchestration runbook to mandate positive fencing: revoking all authorized networks and disabling private service access on the primary before promoting the secondary replica.",
                    "Step 2: Implement a distributed fencing token mechanism; application servers must acquire an atomic lease in Memorystore Redis before issuing writes to the primary database.",
                    "Step 3: Reconfigure the Global External Application Load Balancer with automated backend draining to gracefully terminate in-flight connections prior to shifting traffic.",
                    "Step 4: Initiate an architectural evaluation to migrate high-volume transactional ordering from Cloud SQL to Cloud Spanner multi-region (`nam6`) to achieve native active-active zero-split-brain durability."
                ],
                "verify": (
                    "Execute a controlled failover simulation in staging. Verify that the fencing script severs all client connections to the "
                    "primary within 5 seconds, confirms zero active database sessions, and only then promotes the secondary replica without data divergence."
                ),
                "residual": (
                    "Positive fencing cuts off active transactions in flight in the failing region; client applications must implement idempotent "
                    "transaction retry loops to handle transient connection drops gracefully."
                ),
                "diagram": (
                    "Simulated outage in us-central1",
                    "Replica promoted, old primary NOT fenced",
                    "Dual-master split brain (420 orders lost)",
                    "Mandate positive fencing before promotion",
                    "Clean single-primary cutover in <60s"
                ),
                "facts": "Failover drill promoted replica without fencing primary; dual writes occurred for 22 min; 420 orders diverged; 6h checkout freeze.",
                "inference": "Automated failover without positive fencing guarantees split-brain data corruption during partial network partitions.",
                "expected": "Positive fencing disables primary write access before replica promotion, ensuring exactly one master at all times."
            },
            "lab": {
                "name": "Multi-Region Failover Fencing and Split-Brain Verification",
                "file": "day-074-fencing-runbook.md",
                "goal": "Write a positive fencing failover runbook and build an executable Python test simulating network partitioning and fencing assertion.",
                "expected": "A complete operational fencing runbook, gcloud CLI sequence, and an executable Python split-brain prevention test runner.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 73 data flow and Day 70 reliability principles",
                "preflight": "Review Cloud SQL replica promotion CLI documentation and distributed fencing lease patterns.",
                "steps": [
                    "Draft the positive fencing failover procedure in `day-074-fencing-runbook.md`.",
                    "Define the exact CLI fencing and promotion command sequence:\n\n```sh\n# Step 1: Positively fence the primary instance by severing network access\ngcloud sql instances patch brightloaf-orders-primary \\\n  --authorized-networks='' \\\n  --quiet\n\n# Step 2: Verify zero active client connections on primary before proceeding\n# Step 3: Promote the cross-region replica to standalone master\ngcloud sql instances promote-replica brightloaf-orders-replica-east \\\n  --quiet\n```",
                    "Write an executable Python simulation modeling split-brain fencing logic (`fencing_sim.py`):\n\n```python\n# fencing_sim.py\n\nclass MultiRegionCluster:\n    def __init__(self):\n        self.primary_active = True\n        self.replica_promoted = False\n        self.primary_fenced = False\n        self.orders = []\n\n    def fence_primary(self):\n        self.primary_fenced = True\n        self.primary_active = False\n        return True\n\n    def promote_replica(self):\n        # Enforce positive fencing precondition\n        if not self.primary_fenced:\n            raise RuntimeError(\"CRITICAL: Cannot promote replica while primary is NOT fenced! Split-brain risk!\")\n        self.replica_promoted = True\n        return True\n\n    def write_order(self, region: str, order_id: str):\n        if region == 'primary' and self.primary_active:\n            self.orders.append(('primary', order_id))\n            return 'WRITE_COMMITTED_PRIMARY'\n        elif region == 'secondary' and self.replica_promoted:\n            self.orders.append(('secondary', order_id))\n            return 'WRITE_COMMITTED_SECONDARY'\n        return 'WRITE_REJECTED_FENCED'\n\ncluster = MultiRegionCluster()\n# Normal write to primary\nassert cluster.write_order('primary', 'ord_1') == 'WRITE_COMMITTED_PRIMARY'\n\n# Attempt unsafe promotion without fencing -> must fail!\ntry:\n    cluster.promote_replica()\n    assert False, \"Unsafe promotion should have thrown an error!\"\nexcept RuntimeError as e:\n    print(f\"Fencing Guard Triggered: {e}\")\n\n# Execute proper fencing\ncluster.fence_primary()\nassert cluster.write_order('primary', 'ord_2') == 'WRITE_REJECTED_FENCED'\n\n# Promote replica safely\ncluster.promote_replica()\nassert cluster.write_order('secondary', 'ord_3') == 'WRITE_COMMITTED_SECONDARY'\nprint(\"Multi-Region Fencing Logic Verified Successfully.\")\n```",
                    "Execute the Python fencing simulation test:\n\n```sh\npython3 fencing_sim.py\n```"
                ],
                "verification": (
                    "Run automated fencing verification test:\n\n```sh\npython3 -c \"import fencing_sim; print('Fencing Test Runner Passed')\"\n```\n\nConfirm output displays `Multi-Region Fencing Logic Verified Successfully`."
                ),
                "trouble": (
                    "If primary writes succeed after fencing in simulation, verify that `primary_active` flag is set to False upon fencing."
                ),
                "cleanup": "No remote cloud resources created; retain runbooks and simulation scripts in local repository.",
                "accept": "A validated failover fencing runbook, gcloud execution sequence, and working Python split-brain prevention test."
            }
        },
        {
            "key": "topic-02",
            "title": "Multi-Tenant SaaS Designs: Project, VPC, Namespace, and Row-Level Isolation",
            "overview": (
                "Evaluate the multi-tenant SaaS architecture spectrum. Balance security blast radius, noisy neighbor risks, "
                "and infrastructure costs across Project Silos, GKE Namespaces, and PostgreSQL Row-Level Security (RLS)."
            ),
            "preview": (
                "An application bug in a shared database query omits the `tenant_id` WHERE clause, allowing an enterprise client to view "
                "a direct competitor's proprietary order records and pricing margins, triggering a multi-million-dollar lawsuit."
            ),
            "technical": (
                "#### 1. The Multi-Tenant Isolation Spectrum: Silo vs. Pool Models\n\n"
                "In Software-as-a-Service (SaaS) architecture, multi-tenancy governs how multiple independent customers (tenants) share "
                "underlying cloud infrastructure. The design space spans from complete physical isolation (Silo Model) to total resource sharing (Pool Model):\n\n"
                "- **Silo Model (Project per Tenant):** Each customer receives a dedicated Google Cloud Project with its own VPC, Cloud SQL "
                "database, and IAM permissions. Maximum security, complete compliance isolation, zero noisy-neighbor interference, and trivial "
                "per-tenant cost attribution. However, provisioning requires automated infrastructure-as-code (Terraform Project Factory), and "
                "operational updates must be rolled out across hundreds of separate projects.\n\n"
                "- **Pool Model (Shared Infrastructure & Pooled Storage):** All tenants share the same compute cluster (GKE / Cloud Run) and the "
                "same relational database tables, distinguished only by a `tenant_id` column. Maximum resource utilization, lowest base cost, "
                "and instant tenant onboarding. However, any software bug in an application query risks cross-tenant data leakage, and a single "
                "heavy customer can exhaust database I/O, degrading performance for all other tenants (Noisy Neighbor problem).\n\n"
                "#### 2. Network and Compute Isolation: GKE Namespaces and Dataplane V2\n\n"
                "For workloads that pool compute on Google Kubernetes Engine (GKE), Kubernetes **Namespaces** provide logical isolation:\n\n"
                "- **RBAC & Quotas:** Resource quotas (`ResourceQuota` and `LimitRange`) cap CPU, memory, and pod counts per tenant namespace, "
                "preventing a rogue container from starving the cluster.\n"
                "- **Dataplane V2 (Cilium eBPF) Network Policies:** By default, Kubernetes pods can communicate with any other pod across namespaces. "
                "Enforcing strict NetworkPolicies drops all cross-namespace traffic unless explicitly whitelisted.\n\n"
                "#### 3. Database Row-Level Security (RLS) Mechanics\n\n"
                "In a pooled database architecture, relying on application developers to remember `WHERE tenant_id = ?` in every SQL query "
                "is an inevitable failure point. Modern relational engines like PostgreSQL provide **Row-Level Security (RLS)**:\n\n"
                "```sql\n"
                "-- Enable Row-Level Security on shared orders table\n"
                "ALTER TABLE orders ENABLE ROW LEVEL SECURITY;\n\n"
                "-- Define RLS policy filtering rows by session tenant variable\n"
                "CREATE POLICY tenant_isolation_policy ON orders\n"
                "FOR ALL\n"
                "USING (tenant_id = current_setting('app.current_tenant_id', true));\n"
                "```\n\n"
                "Before executing any query, the application connection sets the session variable (`SET LOCAL app.current_tenant_id = 'tenant_42';`). "
                "The PostgreSQL query planner automatically injects the tenant filter into the query execution tree. Even if a developer writes "
                "`SELECT * FROM orders`, the database engine physically returns only rows belonging to `tenant_42`.\n\n"
                "#### 4. The Noisy Neighbor Problem and Dynamic Throttling\n\n"
                "In pooled architectures, tenants share hardware limits (CPU, memory, database IOPS). To prevent one tenant from monopolizing "
                "resources, architects enforce token-bucket rate limiting per tenant at the API Gateway or Load Balancer, and implement tenant-aware "
                "priority queues in message brokers.\n\n"
                "#### 5. Architectural Trade-offs: SaaS Tenant Isolation Models\n\n"
                "| Isolation Architecture | Security Blast Radius | Noisy Neighbor Risk | Infrastructure Base Cost | Operational Complexity | Typical Customer Tier |\n"
                "|---|---|---|---|---|---|\n"
                "| **Project Silo (GCP Project per Tenant)** | Absolute (Cryptographic & IAM boundary) | Zero (Dedicated quotas) | Highest ($$$$ per project) | High (Requires automated Terraform fleet) | Enterprise / Regulated Banking / Gov |\n"
                "| **VPC / Cluster per Tenant** | High (Network & Kernel isolation) | Very Low (Independent VMs) | High ($$$ cluster fees) | Moderate (Fleet management) | Large Enterprise / Healthcare |\n"
                "| **GKE Namespace Isolation** | Moderate (Shared OS kernel) | Low (cgroup CPU/RAM limits) | Moderate ($$ optimal bin-packing) | Moderate (Kubernetes RBAC/Policies) | Mid-Market / Standard B2B SaaS |\n"
                "| **Database Row-Level Security (RLS)** | Low (Relies on DB engine policies) | High (Shared DB IOPS) | Lowest ($ single shared database) | Lowest (Standard web app deployment) | Free / Self-Serve / SMB Customers |\n"
            ),
            "questions": [
                "Why is relying on application-level SQL filtering (WHERE tenant_id = ?) dangerous in multi-tenant SaaS?",
                "How does PostgreSQL Row-Level Security (RLS) enforce tenant isolation at the database engine level?",
                "What architectural mechanisms mitigate the 'Noisy Neighbor' problem in pooled compute clusters?",
                "Under what compliance frameworks is a Project-per-Tenant (Silo) model mandatory over a pooled model?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/saas-tenant-isolation",
            "reference_label": "Google Cloud Architecture Center: Multi-tenant SaaS tenant isolation",
            "scenario": {
                "scenario": (
                    "Brightloaf operates a SaaS B2B bakery inventory management platform serving 320 independent commercial bakery chains "
                    "on a shared Cloud SQL PostgreSQL database. During an application refactoring to support GraphQL queries, a software "
                    "engineer introduced a resolver that omitted the `tenant_id` filter when querying the `supplier_orders` table. A corporate "
                    "franchise client ('Artisan Crust') executed a catalog search and noticed that the response returned wholesale flour and butter "
                    "pricing agreements belonging to their direct market competitor ('Golden Loaf'). Artisan Crust captured screenshots, "
                    "retained legal counsel, and issued an immediate formal breach notification demanding a forensic audit."
                ),
                "impact": (
                    "Severe P1 confidentiality breach and contractual violation. Cross-tenant data leakage affected 14 enterprise bakery chains. "
                    "Golden Loaf filed a $2.5 million commercial lawsuit for trade secret disclosure. Artisan Crust terminated their annual enterprise "
                    "contract ($180,000 ARR). Mandatory third-party SOC 2 Type II audit triggered."
                ),
                "constraints": (
                    "Guarantee 100% cryptographic or engine-level tenant isolation; prevent any query from accessing cross-tenant rows even if "
                    "application code contains bugs; maintain high tenant density and low database operating costs."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect application access logs; correlate GraphQL query timestamps with database query logs; identify `SELECT * FROM supplier_orders WHERE status = 'active'` missing tenant qualification.",
                    "Step 2: Review database schema; discover `supplier_orders` table possessed a `tenant_id` column but lacked PostgreSQL Row-Level Security (RLS) enablement.",
                    "Step 3: Audit application ORM configuration; confirm queries rely entirely on developer discipline to append tenant filters in Python/Java code.",
                    "Step 4: Check GKE cluster architecture; observe all tenant microservices execute under a single shared service account with full database table permissions."
                ],
                "root": (
                    "Relying on application-level WHERE clauses in software code without database engine-enforced Row-Level Security (RLS) "
                    "allowed an application code bug to bypass tenant boundaries and expose confidential competitor trade secrets."
                ),
                "remediation_steps": [
                    "Step 1: Immediately enable PostgreSQL Row-Level Security (RLS) on all multi-tenant tables (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`).",
                    "Step 2: Define strict RLS policies bound to session configuration settings (`USING (tenant_id = current_setting('app.current_tenant_id', true))`).",
                    "Step 3: Update database connection pooling middleware to automatically set `app.current_tenant_id` on every acquired database connection before executing business logic.",
                    "Step 4: Offer high-value regulated enterprise clients an isolated Project-per-Tenant (Silo) deployment option automated via Terraform Project Factory."
                ],
                "verify": (
                    "Execute a raw SQL query `SELECT * FROM supplier_orders` as a simulated tenant without a WHERE clause. Verify the database "
                    "engine returns strictly the rows matching the configured `app.current_tenant_id`, returning zero rows for all other tenants."
                ),
                "residual": (
                    "Row-Level Security adds a sub-millisecond query planning overhead to every database query; complex multi-table joins on "
                    "RLS tables require composite indexes on `(tenant_id, primary_key)` to maintain optimal query execution plans."
                ),
                "diagram": (
                    "GraphQL bug omits WHERE tenant_id",
                    "Competitor wholesale prices leaked",
                    "Lawsuit filed, $180k ARR contract lost",
                    "Enable PostgreSQL Row-Level Security (RLS)",
                    "Engine forces tenant filter on all queries"
                ),
                "facts": "GraphQL resolver omitted tenant filter; competitor wholesale prices exposed; $2.5M lawsuit filed; $180k contract cancelled.",
                "inference": "Application-level tenant filtering is vulnerable to developer error; database-enforced RLS eliminates cross-tenant data leakage.",
                "expected": "Database kernel-level RLS policies enforce tenant boundaries regardless of application query syntax."
            },
            "lab": {
                "name": "PostgreSQL Row-Level Security (RLS) Tenant Isolation Simulation",
                "file": "day-074-tenant-isolation.md",
                "goal": "Write a PostgreSQL Row-Level Security (RLS) schema, configure session context injection, and build a Python test verifying cross-tenant isolation.",
                "expected": "A complete SQL RLS script, connection middleware runbook, and an executable Python tenant isolation test runner.",
                "mode": "offline architecture specification, SQL scripting, and Python development; no cloud resources billed",
                "prereq": "Day 73 lakehouse design and Day 70 security principles",
                "preflight": "Review PostgreSQL documentation on Row Security Policies and session configuration parameters.",
                "steps": [
                    "Draft the multi-tenant SaaS isolation strategy in `day-074-tenant-isolation.md`.",
                    "Write the production PostgreSQL Row-Level Security DDL script (`tenant_rls_setup.sql`):\n\n```sql\n-- tenant_rls_setup.sql\nCREATE TABLE tenant_orders (\n  order_id TEXT PRIMARY KEY,\n  tenant_id TEXT NOT NULL,\n  customer_email TEXT NOT NULL,\n  total_amount NUMERIC(10,2) NOT NULL\n);\n\n-- Create index on tenant_id for high-speed RLS evaluation\nCREATE INDEX idx_tenant_orders_tenant ON tenant_orders(tenant_id);\n\n-- Enable Row-Level Security on table\nALTER TABLE tenant_orders ENABLE ROW LEVEL SECURITY;\n\n-- Force RLS even for table owners to prevent administrative bypass\nALTER TABLE tenant_orders FORCE ROW LEVEL SECURITY;\n\n-- Create strict tenant isolation policy\nCREATE POLICY tenant_isolation_policy ON tenant_orders\nFOR ALL\nUSING (tenant_id = current_setting('app.current_tenant_id', true));\n```",
                    "Write an executable Python simulation modeling PostgreSQL RLS mechanics (`test_rls_sim.py`):\n\n```python\n# test_rls_sim.py\nimport sqlite3\n\n# Simulate RLS engine behavior using SQLite in-memory database with custom views\nconn = sqlite3.connect(':memory:')\ncur = conn.cursor()\n\n# Create underlying shared table\ncur.execute('''CREATE TABLE orders_raw (order_id TEXT, tenant_id TEXT, amount REAL)''')\ncur.execute('''CREATE TABLE session_context (current_tenant_id TEXT)''')\n\n# Populate sample multi-tenant data\ncur.execute(\"INSERT INTO orders_raw VALUES ('ord_1', 'tenant_alpha', 150.0)\")\ncur.execute(\"INSERT INTO orders_raw VALUES ('ord_2', 'tenant_beta', 220.0)\")\ncur.execute(\"INSERT INTO orders_raw VALUES ('ord_3', 'tenant_alpha', 85.0)\")\n\n# Function simulating RLS query with session context injection\ndef query_orders_as_tenant(tenant_id: str):\n    # Simulate setting session variable\n    cur.execute(\"DELETE FROM session_context\")\n    cur.execute(\"INSERT INTO session_context VALUES (?)\", (tenant_id,))\n    \n    # RLS simulated view: SELECT * FROM orders WHERE tenant_id = session.tenant_id\n    cur.execute('''\n        SELECT order_id, tenant_id, amount \n        FROM orders_raw \n        WHERE tenant_id = (SELECT current_tenant_id FROM session_context)\n    ''')\n    return cur.fetchall()\n\n# Test Tenant Alpha: should see ord_1 and ord_3 only\nalpha_orders = query_orders_as_tenant('tenant_alpha')\nassert len(alpha_orders) == 2\nassert all(row[1] == 'tenant_alpha' for row in alpha_orders)\n\n# Test Tenant Beta: should see ord_2 only\nbeta_orders = query_orders_as_tenant('tenant_beta')\nassert len(beta_orders) == 1\nassert beta_orders[0][0] == 'ord_2'\n\nprint(\"Row-Level Security Tenant Isolation Verified Successfully.\")\n```",
                    "Execute the Python RLS simulation test:\n\n```sh\npython3 test_rls_sim.py\n```"
                ],
                "verification": (
                    "Run automated tenant isolation test:\n\n```sh\npython3 -c \"import test_rls_sim; print('Tenant RLS Test Passed')\"\n```\n\nConfirm output displays `Row-Level Security Tenant Isolation Verified Successfully`."
                ),
                "trouble": (
                    "If queries return rows from other tenants in simulation, verify that session context injection strictly matches the active tenant ID."
                ),
                "cleanup": "No remote cloud resources created; retain SQL scripts and test runners in repository.",
                "accept": "A validated PostgreSQL RLS schema, session context injection runbook, and working Python tenant isolation test."
            }
        },
        {
            "key": "topic-03",
            "title": "Landing Zone / Enterprise Foundation: Org Structure, Hub-and-Spoke Networking, and Baselines",
            "overview": (
                "Blueprint enterprise Google Cloud foundations. Architect the resource hierarchy (Organizations, Folders, Projects), "
                "hub-and-spoke Shared VPC networking, centralized log sinks, and organization policy guardrails."
            ),
            "preview": (
                "Developers provision ad-hoc cloud projects without central networking or security guardrails; an unmonitored VM with a "
                "public IP and open SSH port is compromised by cryptominers, running up a $35,000 compute bill in 4 days."
            ),
            "technical": (
                "#### 1. The Google Cloud Resource Hierarchy\n\n"
                "Enterprise cloud governance is anchored in Google Cloud's hierarchical resource structure:\n\n"
                "- **Organization:** Root node linked 1:1 to Google Workspace or Cloud Identity domain. The supreme policy enforcement point.\n"
                "- **Folders:** Groupings representing environments (`Production`, `Non-Production`), business units (`Retail`, `Wholesale`), "
                "or compliance domains (`PCI-DSS`, `HIPAA`). IAM roles and Organization Policies inherit hierarchically down the tree.\n"
                "- **Projects:** The core operational container. All cloud resources (VMs, buckets, databases) belong to exactly one project. "
                "Projects define IAM boundaries, API enablement, billing account linkage, and quota allocations.\n\n"
                "#### 2. Hub-and-Spoke Shared VPC Networking Architecture\n\n"
                "Allowing individual projects to manage their own VPC networks leads to network fragmentation, duplicate Cloud NAT gateways, "
                "and unmonitored egress paths. Enterprise foundations implement **Shared VPC** in a Hub-and-Spoke model:\n\n"
                "- **Host Project (The Hub):** Owned exclusively by the central Network Operations team. Contains the Shared VPC network, "
                "regional subnets, Cloud Interconnect / VPN attachments to on-premises datacenters, Cloud NAT, and centralized next-generation firewalls.\n"
                "- **Service Projects (The Spokes):** Owned by domain workload teams (e.g. `checkout-prod-prj`, `catalog-prod-prj`). Workload VMs "
                "and containers attach their virtual network interfaces directly to subnets in the Host Project.\n"
                "- **Separation of Duties:** Workload engineers manage their applications and VMs, but have ZERO permission to modify network routing, "
                "firewalls, or subnet CIDRs.\n\n"
                "#### 3. Centralized Log Sinks and Security Auditing\n\n"
                "Security compliance requires an immutable, centralized audit trail. Organization-level **Aggregated Log Sinks** stream all "
                "Audit Logs, VPC Flow Logs, and Firewall Rules logs across all projects in the entire organization into:\n\n"
                "  1. A locked, retention-compliant Cloud Storage bucket for long-term legal archival (7-year retention).\n"
                "  2. A centralized BigQuery security analytics dataset for real-time threat hunting and SIEM integration.\n\n"
                "#### 4. Organization Policy Service Guardrails\n\n"
                "Organization Policies enforce programmatic security guardrails that override local project IAM permissions:\n\n"
                "- `constraints/compute.vmExternalIpAccess`: Denies external public IP addresses on all Compute Engine VMs, forcing all traffic "
                "through Load Balancers and Cloud NAT.\n"
                "- `constraints/iam.disableServiceAccountKeyCreation`: Blocks developers from generating downloadable JSON service account keys.\n"
                "- `constraints/gcp.resourceLocations`: Restricts resource creation strictly to approved regions (e.g. `us-central1`, `us-west1`).\n\n"
                "#### 5. Architectural Trade-offs: Enterprise Foundation Networking Primitives\n\n"
                "| Foundation Primitive | Network Topology | Central Administration | Cross-Project Bandwidth | Operational Overhead | Best Suited For |\n"
                "|---|---|---|---|---|---|\n"
                "| **Shared VPC (Hub & Spoke)** | Centralized single SDN network | Highest (Central Network Host Project) | Full Google SDN line-rate (0ms hop) | Low (Unified IP space management) | Enterprise standard for internal microservices & workloads |\n"
                "| **VPC Network Peering** | Decentralized mesh between separate VPCs | Moderate (Requires pairwise peering) | Line-rate (No gateway hop) | High (Non-transitive routing; quota limits) | Connecting independent SaaS systems or distinct corporate orgs |\n"
                "| **Network Connectivity Center** | Hub-and-spoke with router appliances | High (Central connectivity hub) | Bounded by SD-WAN / router VM limits | Moderate | Integrating hybrid on-premises SD-WAN and multicloud routers |\n"
                "| **Private Service Connect (PSC)** | Consumer/Producer endpoint via IP | High (Decoupled private endpoint) | Line-rate SDN forwarding | Lowest (No RFC 1918 CIDR overlap conflicts) | Exposing managed services across separate organizations |\n"
            ),
            "questions": [
                "How does the Google Cloud resource hierarchy enforce policy inheritance across folders and projects?",
                "What is the operational division of responsibility between a Shared VPC Host Project and Service Projects?",
                "Why is disabling public external IP addresses via Organization Policy a critical enterprise security baseline?",
                "What is the architectural difference between Shared VPC and non-transitive VPC Network Peering?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/landing-zones",
            "reference_label": "Google Cloud Architecture Center: Google Cloud architecture framework: Landing zones",
            "scenario": {
                "scenario": (
                    "Brightloaf operated without a centralized landing zone or organization policy governance. Developers created "
                    "standalone Google Cloud projects directly using personal corporate logins linked to a central billing account. A junior "
                    "developer working on a test microservice created a public Compute Engine VM in a personal project, assigning it an "
                    "ephemeral external IP address and configuring a firewall rule opening port 22 (SSH) to `0.0.0.0/0` with a weak password. "
                    "Within 72 hours, automated internet port scanners compromised the VM and installed an XMRig cryptomining worm that "
                    "auto-scaled the instance family to 32 high-GPU instances. The attack went undetected for 5 days because the project lacked "
                    "centralized logging, security alerting, or budget thresholds, racking up $38,000 in unauthorized compute costs."
                ),
                "impact": (
                    "P1 security compromise and financial fraud. $38,000 in unbudgeted compute charges. Corporate IP blacklisted on spam "
                    "and malware registries. Security audit cited complete failure of enterprise perimeter governance."
                ),
                "constraints": (
                    "Prevent unauthorized project creation; block external IP addresses on all compute instances by default; centralize all "
                    "audit and security logging into an immutable enterprise security lake."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect billing export anomalies; discover sudden $38,000 spike originating from an unmonitored project `test-dev-sandbox-4921`.",
                    "Step 2: Check project IAM bindings; observe project owned by a single individual without organization-level security admin oversight.",
                    "Step 3: Review Compute Engine configuration; discover 32 `a2-highgpu-1g` instances running cryptomining binaries with public external IPs.",
                    "Step 4: Check Organization Policies; observe zero policies enabled at the root organization node."
                ],
                "root": (
                    "Lack of an enterprise landing zone foundation, absence of Organization Policies restricting public IP access, and "
                    "uncontrolled project provisioning allowed an insecure, unmonitored compute instance to be compromised."
                ),
                "remediation_steps": [
                    "Step 1: Implement an enterprise Google Cloud Landing Zone with a standardized Resource Hierarchy (Folders: `Core`, `Prod`, `Non-Prod`, `Sandbox`).",
                    "Step 2: Deploy Organization Policies at the root node: `compute.vmExternalIpAccess` (DENY ALL) and `iam.disableServiceAccountKeyCreation` (ENFORCE).",
                    "Step 3: Migrate all project networking into a centralized Hub-and-Spoke Shared VPC managed by the central networking team.",
                    "Step 4: Configure an organization-level Aggregated Log Sink exporting all audit and VPC flow logs into a locked BigQuery security dataset."
                ],
                "verify": (
                    "Attempt to create a Compute Engine VM with an external public IP address in any project. Verify the Google Cloud API "
                    "rejects the request immediately with an Organization Policy violation error."
                ),
                "residual": (
                    "Blocking external IPs requires all developers to access internal VMs via Identity-Aware Proxy (IAP) TCP forwarding, "
                    "requiring updated developer workstation tooling and onboarding runbooks."
                ),
                "diagram": (
                    "Ad-hoc project with public IP & weak SSH",
                    "Cryptomining worm infects VM",
                    "$38,000 fraud bill, zero audit trail",
                    "Deploy Landing Zone & Shared VPC",
                    "Org policy blocks public IPs; IAP enforced"
                ),
                "facts": "Ad-hoc project had public VM with open SSH; cryptomining worm installed; $38k compute bill in 5 days; no central logging.",
                "inference": "Unmanaged project sprawl creates indefensible attack surfaces; landing zones enforce immutable security baselines.",
                "expected": "Landing zones enforce Shared VPC and Org Policies, blocking public IP creation and centralizing security telemetry."
            },
            "lab": {
                "name": "Enterprise Landing Zone Resource Hierarchy and Org Policy Definition",
                "file": "day-074-landing-zone.md",
                "goal": "Design a complete enterprise resource hierarchy, write Organization Policy constraint manifests, and build a Python validation test.",
                "expected": "A complete Landing Zone blueprint, JSON organization policy definitions, and an executable Python policy validator.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 70 security compliance and Day 68 governance requirements",
                "preflight": "Review Google Cloud Resource Manager and Organization Policy Service documentation.",
                "steps": [
                    "Draft the enterprise resource hierarchy structure in `day-074-landing-zone.md` (Org -> Folders: `Production`, `Non-Production`, `Shared-Core`).",
                    "Write the Organization Policy constraint manifest disabling external IP addresses (`disable-external-ip.json`):\n\n```json\n{\n  \"name\": \"organizations/1029384756/policies/compute.vmExternalIpAccess\",\n  \"spec\": {\n    \"rules\": [\n      {\n        \"denyAll\": true\n      }\n    ]\n  }\n}\n```",
                    "Write the Organization Policy constraint manifest disabling service account key creation (`disable-sa-keys.json`):\n\n```json\n{\n  \"name\": \"organizations/1029384756/policies/iam.disableServiceAccountKeyCreation\",\n  \"spec\": {\n    \"rules\": [\n      {\n        \"enforce\": true\n      }\n    ]\n  }\n}\n```",
                    "Develop an executable Python script validating Landing Zone policy manifests (`validate_policies.py`):\n\n```python\n# validate_policies.py\nimport json\n\ndef validate_org_policy(file_path: str, expected_constraint: str):\n    with open(file_path, 'r') as f:\n        data = json.load(f)\n    assert 'name' in data and expected_constraint in data['name'], f\"Constraint {expected_constraint} mismatch!\"\n    assert 'spec' in data and len(data['spec']['rules']) > 0, \"Policy rules missing!\"\n    return True\n\nassert validate_org_policy('disable-external-ip.json', 'compute.vmExternalIpAccess') is True\nassert validate_org_policy('disable-sa-keys.json', 'iam.disableServiceAccountKeyCreation') is True\nprint(\"Landing Zone Organization Policies Validated Successfully.\")\n```",
                    "Execute the Python policy validation script:\n\n```sh\npython3 validate_policies.py\n```"
                ],
                "verification": (
                    "Run automated policy verification test:\n\n```sh\npython3 -c \"import validate_policies; print('Landing Zone Test Passed')\"\n```\n\nConfirm output displays `Landing Zone Organization Policies Validated Successfully`."
                ),
                "trouble": (
                    "If policy JSON fails validation, verify that organization numeric ID in the policy name follows Google Cloud naming formats."
                ),
                "cleanup": "No remote cloud resources created; retain JSON policies and validation scripts in local repository.",
                "accept": "A validated Landing Zone architecture blueprint, Organization Policy constraint manifests, and working Python policy validator."
            }
        },
        {
            "key": "topic-04",
            "title": "Architectural Anti-Patterns: Lift-and-Shift, SPOFs, Chatty Cross-Region Calls, and Giant Monoliths",
            "overview": (
                "Identify and remediate four fatal cloud architectural anti-patterns: unoptimized lift-and-shift, single points "
                "of failure (SPOF), chatty cross-region microservice RPC cascades, and giant monolithic multi-team projects."
            ),
            "preview": (
                "A microservice architecture executes 48 sequential remote RPC calls across continents for a single customer shopping "
                "cart page load, ballooning end-to-end latency to 14.8 seconds and destroying conversion rates."
            ),
            "technical": (
                "#### 1. Anti-Pattern 1: Unoptimized Lift-and-Shift (Zombie VM Monolith)\n\n"
                "- **The Symptom:** Migrating on-premises virtual machines directly to Compute Engine without architectural refactoring. "
                "VMs run 24/7 with over-allocated static RAM and disk, monolithic software stacks, local filesystem dependencies, and manual patching.\n"
                "- **The Consequence:** Higher operating costs than on-premises (no hardware depreciation benefit), zero elasticity, and no cloud-native "
                "auto-healing. A host failure crashes the application exactly as it did in the private datacenter.\n"
                "- **Prescriptive Remedy:** Containerize into stateless Cloud Run or GKE workloads; externalize state to managed Redis and Cloud SQL; "
                "enforce autoscaling from zero.\n\n"
                "#### 2. Anti-Pattern 2: The Single Point of Failure (SPOF) Blindspot\n\n"
                "- **The Symptom:** Architecting a high-availability multi-zone web tier that secretly relies on a single un-replicated dependency "
                "(e.g. a single Redis master VM, an un-backed-up SFTP server, or a single NAT gateway IP).\n"
                "- **The Consequence:** A minor zonal hardware glitch in the hidden dependency collapses the entire multi-zone application stack.\n"
                "- **Prescriptive Remedy:** Conduct systematic Failure Mode and Effects Analysis (FMEA); eliminate single points via Cloud NAT (software-defined "
                "regional routing), Memorystore High Availability (automatic failover), and regional Cloud Storage.\n\n"
                "#### 3. Anti-Pattern 3: Chatty Cross-Region Microservice Calls (Latency Compounding)\n\n"
                "- **The Symptom:** Breaking a monolith into microservices without respecting data locality. When a user requests a web page, "
                "Service A in `us-central1` executes 12 serial REST/gRPC calls to Service B in `europe-west3`, which in turn executes serial queries "
                "against a database in `us-east4`.\n\n"
                "$$\\text{Total Latency} = \\sum_{i=1}^{N} (\\text{Computation}_i + \\text{RTT}_i)$$\n\n"
                "If cross-region RTT is 75ms, 40 sequential calls add $40 \\times 75\\text{ms} = 3,000\\text{ms}$ of pure network transit latency, "
                "rendering the application unusable.\n\n"
                "- **Prescriptive Remedy:** Co-locate dependent services in the same regional boundary; batch network calls into composite requests "
                "(GraphQL / gRPC streaming); deploy regional read-replicas and edge caches; adopt event-driven asynchronous choreography.\n\n"
                "#### 4. Anti-Pattern 4: The Giant Monolithic Project\n\n"
                "- **The Symptom:** Deploying development, staging, production, analytics, and infrastructure into a single massive Google Cloud Project.\n"
                "- **The Consequence:** Inevitable catastrophic human error (a developer running a destruction command in dev accidentally wipes production "
                "databases); severe IAM role explosion; hard project-level quota exhaustion (e.g. VPC route limits, API rate limits).\n"
                "- **Prescriptive Remedy:** Segregate workloads into separate projects by environment and domain within a standardized landing zone hierarchy.\n\n"
                "#### 5. Architectural Trade-offs: Anti-Pattern Catalog & Modernization Remedies\n\n"
                "| Anti-Pattern | Root Architectural Flaw | Observability Symptom | Modernization Remedy | Target Architectural Pattern |\n"
                "|---|---|---|---|---|\n"
                "| **Lift-and-Shift Zombie** | Treating Cloud as hosted hardware | Static CPU < 10%; manual VM patching | Containerization + Cloud Run / GKE | Cloud-Native Elastic Serverless |\n"
                "| **Hidden SPOF** | Zonal dependency in multi-zone app | 100% outage from single zone glitch | Regional HA + Managed Services | Redundant Parallel Availability |\n"
                "| **Chatty Cross-Region RPC** | Microservice serialization across WAN | p99 latency > 10s; high network egress bill | Colocate in region + Batching + Caching | Data Locality & Coarse-Grained APIs |\n"
                "| **Giant Monolith Project** | Missing environment boundaries | Accidental prod outages; quota throttling | Multi-project landing zone + Shared VPC | Zero-Trust Project-Level Isolation |\n"
            ),
            "questions": [
                "How does serial cross-region RPC call compounding destroy application latency in microservice architectures?",
                "What is the operational danger of running development and production workloads in a single Google Cloud project?",
                "How does Failure Mode and Effects Analysis (FMEA) uncover hidden Single Points of Failure (SPOFs)?",
                "Why does a direct Lift-and-Shift migration often result in higher monthly costs than on-premises hosting?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/system-design",
            "reference_label": "Google Cloud Architecture Center: System design anti-patterns",
            "scenario": {
                "scenario": (
                    "Brightloaf decomposed its monolithic e-commerce application into 14 distributed microservices. However, during the "
                    "migration, the Order Summary frontend was deployed in `europe-west1` (Belgium) to serve European users, while the Pricing "
                    "Service remained in `us-central1` (Iowa) and the Product Catalog Service resided in `us-east4` (Virginia). When a customer "
                    "loaded the checkout cart, the Order Summary frontend made 42 sequential synchronous REST calls to the Pricing and Catalog "
                    "services to calculate item discounts, local VAT taxes, and currency conversions. Customer page load times averaged 14.8 "
                    "seconds per cart view, resulting in an immediate 68% cart abandonment rate across European shoppers."
                ),
                "impact": (
                    "Severe commercial failure. European conversion rate plummeted from 3.2% to 0.4%. Over $280,000 in monthly sales lost. "
                    "Cross-region network egress bills surged by $14,000/month due to millions of small, uncompressed JSON HTTP payloads "
                    "crossing oceanic fiber links."
                ),
                "constraints": (
                    "Reduce cart page load latency to under 500ms; eliminate cross-region serialization; maintain unified global pricing rules."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect Google Cloud Trace waterfall spans for `/checkout/summary`; observe 42 sequential network hops averaging 85ms each, consuming 13.6 seconds of total request duration in network transit.",
                    "Step 2: Review network telemetry; discover microservices were communicating over public internet IPs rather than private Google Cloud backbone networks.",
                    "Step 3: Analyze service deployment manifests; confirm Pricing Service was deployed exclusively in `us-central1` without regional replicas or caching.",
                    "Step 4: Check API payload sizes; observe uncompressed JSON responses transferring redundant catalog metadata on every single call."
                ],
                "root": (
                    "Chatty cross-region microservice anti-pattern: serializing dozens of synchronous fine-grained HTTP calls across distant "
                    "cloud regions compounded network transit latency, rendering the user-facing checkout page completely unresponsive."
                ),
                "remediation_steps": [
                    "Step 1: Co-locate all customer-facing microservices within the same cloud region (`europe-west1`), reducing inter-service network RTT from 85ms to sub-1ms.",
                    "Step 2: Refactor fine-grained REST APIs into a coarse-grained batch API (`/pricing/batch-evaluate`), replacing 42 individual network round-trips with a single batch request.",
                    "Step 3: Deploy regional in-memory read caches (Memorystore for Redis) in Europe to cache static product catalog data locally.",
                    "Step 4: Adopt gRPC with Protocol Buffers over HTTP/2, compressing payload sizes by 70% and multiplexing requests over persistent TCP connections."
                ],
                "verify": (
                    "Execute a load test against the refactored `/checkout/summary` endpoint from European client probes. Verify that end-to-end "
                    "cart load latency drops from 14.8 seconds to 220 milliseconds (a 98.5% improvement) with zero cross-region network calls."
                ),
                "residual": (
                    "Caching pricing and catalog data regionally introduces potential cache invalidation lag; cache TTLs must be tuned to "
                    "invalidate immediately when global price updates occur."
                ),
                "diagram": (
                    "EU Frontend makes 42 serial calls to US",
                    "Network RTT compounds (42 * 85ms)",
                    "14.8s cart latency, 68% abandonment",
                    "Co-locate in EU + Batch gRPC + Redis",
                    "Latency drops to 220ms (98% faster)"
                ),
                "facts": "42 sequential cross-region calls; cart load took 14.8s; 68% cart abandonment; $280k lost sales; $14k extra egress.",
                "inference": "Serial network calls across distant regions compound latency exponentially; data locality and batching are mandatory.",
                "expected": "Regional service co-location and batch gRPC APIs reduce latency to sub-300ms, restoring customer conversion rates."
            },
            "lab": {
                "name": "Latency Compounding Modeling and Microservice Anti-Pattern Simulation",
                "file": "day-074-anti-patterns.md",
                "goal": "Build an executable Python latency compounding simulation modeling serial cross-region calls vs regional batching.",
                "expected": "A complete anti-pattern diagnostic document, an executable Python latency simulation script, and verified benchmark output.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 71 performance sizing and Day 72 microservices",
                "preflight": "Review Google Cloud network latency matrices and gRPC batching design patterns.",
                "steps": [
                    "Draft the architectural anti-pattern remediation catalog in `day-074-anti-patterns.md`.",
                    "Develop an executable Python simulation modeling cross-region latency compounding (`latency_sim.py`):\n\n```python\n# latency_sim.py\nimport time\n\ndef simulate_checkout_flow(num_calls: int, rtt_ms: float, compute_time_ms: float, is_batched: bool = False):\n    if is_batched:\n        # Single batch round-trip + combined compute\n        total_network_ms = rtt_ms\n        total_compute_ms = compute_time_ms * num_calls * 0.7 # Batch efficiency\n        total_duration_ms = total_network_ms + total_compute_ms\n    else:\n        # Serial sequential round-trips\n        total_network_ms = num_calls * rtt_ms\n        total_compute_ms = num_calls * compute_time_ms\n        total_duration_ms = total_network_ms + total_compute_ms\n    return total_network_ms, total_compute_ms, total_duration_ms\n\n# Scenario: 42 microservice calls, US-EU RTT = 85ms, Compute = 5ms per call\nnet_serial, comp_serial, total_serial = simulate_checkout_flow(42, 85.0, 5.0, is_batched=False)\nnet_batch, comp_batch, total_batch = simulate_checkout_flow(42, 85.0, 5.0, is_batched=True)\n\n# Scenario: Co-located in same region (RTT = 0.8ms), batched\nnet_local, comp_local, total_local = simulate_checkout_flow(42, 0.8, 5.0, is_batched=True)\n\nprint(f\"Serial Cross-Region: Network={net_serial:.0f}ms, Total={total_serial:.0f}ms ({total_serial/1000:.2f}s)\")\nprint(f\"Batched Cross-Region: Network={net_batch:.0f}ms, Total={total_batch:.0f}ms ({total_batch/1000:.2f}s)\")\nprint(f\"Local Regional Batched: Network={net_local:.1f}ms, Total={total_local:.1f}ms ({total_local:.0f}ms)\")\nassert total_serial > 3500, \"Serial latency calculation failed!\"\nassert total_local < 300, \"Local optimization calculation failed!\"\nprint(\"Latency Compounding Simulation Verified Successfully.\")\n```",
                    "Execute the Python latency simulation test:\n\n```sh\npython3 latency_sim.py\n```",
                    "Document the batch gRPC Protocol Buffer interface in `day-074-anti-patterns.md` demonstrating coarse-grained request structures."
                ],
                "verification": (
                    "Run automated latency compounding test:\n\n```sh\npython3 -c \"import latency_sim; print('Latency Compounding Test Passed')\"\n```\n\nConfirm output demonstrates reduction from 3.7+ seconds to sub-300ms."
                ),
                "trouble": (
                    "If batched latency exceeds threshold, verify that batch efficiency factor properly models vector processing."
                ),
                "cleanup": "No remote cloud resources created; retain simulation scripts and diagnostic notes in local repository.",
                "accept": "A validated anti-pattern remediation document, an executable Python latency simulation script, and verified benchmark output."
            }
        }
    ]
}
