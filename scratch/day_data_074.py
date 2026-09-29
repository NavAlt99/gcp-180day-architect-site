"""day_data_074.py — Exhaustive architecture data specification for Day 74.

Covers Regional and Tenant Boundaries:
- Multi-Region Active-Active vs Active-Passive (CAP theorem, TrueTime, positive fencing)
- Multi-Tenant SaaS Designs (Silo vs Pool, Namespaces, NetworkPolicies, PostgreSQL RLS)
- Landing Zone & Enterprise Foundation (Resource Hierarchy, Shared VPC, Aggregated Sinks, Org Policies)
- Architectural Anti-Patterns (Lift-and-shift zombie VMs, SPOFs, chatty WAN calls, giant monolith projects)

Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and 8-stage operational lab exercises.
"""

DAY_NUM = 74

DATA = {
    "day": 74,
    "part1_intro": (
        "Day 74 establishes the architectural boundaries, tenancy models, and enterprise foundation guardrails required "
        "to design resilient, secure multi-region platforms on Google Cloud. Moving beyond basic disaster recovery concepts, "
        "this session examines the physical speed-of-light constraints governing cross-region latency, the mathematical "
        "inevitability of split-brain in un-fenced active-passive topologies, and the hardware-assisted linearizability of "
        "Cloud Spanner multi-region active-active deployments. Engineers explore the multi-tenant SaaS spectrum—balancing the "
        "absolute cryptographic blast-radius isolation of Project Silos against the cost-efficiency of PostgreSQL Row-Level "
        "Security (RLS). Finally, architects design scalable Enterprise Landing Zones using Shared VPC hub-and-spoke topologies "
        "and Organization Policies, while systematically dismantling fatal cloud anti-patterns like chatty cross-region microservice "
        "cascades and monolithic project sprawl."
    ),
    "exit_summary": (
        "Engineered an automated positive fencing failover runbook eliminating split-brain risk; implemented PostgreSQL Row-Level "
        "Security (RLS) enforcing tenant isolation at the database engine level; authored enterprise Landing Zone Organization "
        "Policy manifests blocking public IPs; verified a 98.5% latency reduction by eliminating chatty cross-region microservice RPCs."
    ),
    "part2_intro": (
        "Enterprise cloud architecture demands rigorous separation across regional availability zones, tenant security perimeters, "
        "and organizational administrative domains. The matrices below detail the physical trade-offs, network models, and "
        "governance controls governing enterprise cloud boundaries."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Architectural Domain</th>
      <th>Primary Google Cloud Primitive</th>
      <th>Consistency &amp; Recovery Boundary</th>
      <th>Failure Blast Radius &amp; Risk Profile</th>
      <th>Target Performance / SLA Profile</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Active-Passive Regional HA</strong></td>
      <td>Cloud SQL Cross-Region Replica + Fencing Script</td>
      <td>Asynchronous WAL replication; RPO &lt; 30s</td>
      <td>Split-brain data corruption if old primary not fenced</td>
      <td>RTO &lt; 15 min; local sub-10ms write latency</td>
    </tr>
    <tr>
      <td><strong>Active-Active Multi-Region</strong></td>
      <td>Cloud Spanner (Multi-Region nam6 / eur4)</td>
      <td>TrueTime Paxos consensus; RPO = 0, RTO &lt; 1s</td>
      <td>Zero split-brain; Paxos commit wait across regions</td>
      <td>99.999% availability; 35–65ms write latency</td>
    </tr>
    <tr>
      <td><strong>Multi-Tenant Silo (Project)</strong></td>
      <td>Dedicated GCP Project per Tenant (Terraform Factory)</td>
      <td>Cryptographic IAM &amp; Project Quota boundary</td>
      <td>Isolated to single tenant project; zero cross-tenant risk</td>
      <td>Maximum compliance; higher base infrastructure cost</td>
    </tr>
    <tr>
      <td><strong>Multi-Tenant Pool (RLS)</strong></td>
      <td>Cloud SQL PostgreSQL Row-Level Security (RLS)</td>
      <td>Engine-level policy filter on session tenant ID</td>
      <td>Single DB engine failure; shared IOPS noisy neighbor</td>
      <td>Sub-millisecond query time; high tenant density</td>
    </tr>
    <tr>
      <td><strong>Enterprise Landing Zone</strong></td>
      <td>Resource Hierarchy + Shared VPC + Org Policies</td>
      <td>Hierarchical policy inheritance (Org &gt; Folders &gt; Projects)</td>
      <td>Uncontrolled project sprawl; shadow IT public IPs</td>
      <td>100% policy compliance; centralized egress control</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "type": "topology",
        "title": "Day 74: Multi-Region Active-Active vs. Active-Passive & SaaS Boundary Topology",
        "desc": "Multi-tier architecture showing Global Anycast routing, cross-region replication, RLS tenant isolation, and Landing Zone governance.",
        "caption": "Figure 74.1: Enterprise multi-region and tenant isolation topology illustrating Anycast traffic steering, positive fencing, and landing zone guardrails.",
        "width": 1100,
        "height": 660,
        "layers": [
            {"name": "LAYER 1: Global Edge Ingress & Anycast Traffic Routing", "desc": "Global External ALB Anycast VIP + Cloud Armor DDoS Perimeter", "fill": "#1e3a5f", "y": 10, "h": 90},
            {"name": "LAYER 2: Multi-Region Compute & Workload Placement", "desc": "Stateless GKE Autopilot / Cloud Run Fleets (us-central1 & europe-west1)", "fill": "#0f2338", "y": 115, "h": 90},
            {"name": "LAYER 3: Multi-Tenant SaaS Isolation Boundary", "desc": "GKE Namespaces + Dataplane V2 NetworkPolicies + Session Context Injection", "fill": "#064e3b", "y": 220, "h": 90},
            {"name": "LAYER 4: Enterprise Persistence & Consensus Tier", "desc": "Cloud Spanner TrueTime Multi-Region OR Fenced Cloud SQL Asynchronous Replicas", "fill": "#1e1b4b", "y": 325, "h": 90},
            {"name": "LAYER 5: Enterprise Landing Zone & Governance Fabric", "desc": "Hub-and-Spoke Shared VPC Host Project + Org Policies + Centralized BigQuery Log Sink", "fill": "#3b0764", "y": 430, "h": 90},
        ],
        "components": [
            {"id": "alb", "name": "Global Anycast ALB", "detail": "Anycast IP & Edge Health Probes", "x": 80, "y": 30, "w": 240, "h": 54, "fill": "#0f283d", "stroke": "#38bdf8"},
            {"id": "armor", "name": "Cloud Armor Policy", "detail": "WAF & Geolocation Rate Limiting", "x": 430, "y": 30, "w": 240, "h": 54, "fill": "#0f283d", "stroke": "#38bdf8"},
            {"id": "gke_us", "name": "GKE us-central1 (Primary)", "detail": "Multi-Tenant Pods (Tenant Alpha/Beta)", "x": 80, "y": 135, "w": 240, "h": 54, "fill": "#092e28", "stroke": "#10b981"},
            {"id": "gke_eu", "name": "GKE europe-west1 (Failover)", "detail": "Warm Standby Fleet (Auto-scaled)", "x": 430, "y": 135, "w": 240, "h": 54, "fill": "#092e28", "stroke": "#10b981"},
            {"id": "mesh", "name": "Traffic Director Mesh", "detail": "mTLS & Cross-Region Health Checks", "x": 780, "y": 135, "w": 240, "h": 54, "fill": "#092e28", "stroke": "#10b981"},
            {"id": "ctx", "name": "Tenant Context Injector", "detail": "JWT Claims -> Session Variable", "x": 430, "y": 240, "w": 240, "h": 54, "fill": "#093322", "stroke": "#22c55e"},
            {"id": "rls", "name": "PostgreSQL RLS Engine", "detail": "Kernel-level WHERE tenant_id filter", "x": 780, "y": 240, "w": 240, "h": 54, "fill": "#093322", "stroke": "#22c55e"},
            {"id": "spanner", "name": "Cloud Spanner (nam6)", "detail": "Multi-Region Paxos TrueTime", "x": 80, "y": 345, "w": 240, "h": 54, "fill": "#1b143a", "stroke": "#a855f7"},
            {"id": "csql_fence", "name": "Cloud SQL + Fencing", "detail": "Positive Network Fencing Hook", "x": 430, "y": 345, "w": 240, "h": 54, "fill": "#1b143a", "stroke": "#a855f7"},
            {"id": "hub_vpc", "name": "Shared VPC Hub Project", "detail": "Central Firewalls & Interconnect", "x": 80, "y": 450, "w": 240, "h": 54, "fill": "#280a3c", "stroke": "#c084fc"},
            {"id": "org_pol", "name": "Org Policy Guardrails", "detail": "Deny External IP & SA Keys", "x": 430, "y": 450, "w": 240, "h": 54, "fill": "#280a3c", "stroke": "#c084fc"},
            {"id": "sec_sink", "name": "BigQuery Security Sink", "detail": "Aggregated Immutable Audit Lake", "x": 780, "y": 450, "w": 240, "h": 54, "fill": "#280a3c", "stroke": "#c084fc"},
        ],
        "boundaries": [
            {"x": 60, "y": 120, "w": 630, "h": 80, "label": "MULTI-REGION FAILOVER BOUNDARY", "color": "#10b981"},
            {"x": 760, "y": 225, "w": 280, "h": 80, "label": "TENANT ISOLATION PERIMETER (RLS)", "color": "#22c55e"},
            {"x": 60, "y": 435, "w": 630, "h": 80, "label": "CENTRAL LANDING ZONE PERIMETER", "color": "#c084fc"},
        ],
        "flows": [
            {"x1": 320, "y1": 57, "x2": 430, "y2": 57, "type": "ok", "label": "Clean Ingress"},
            {"x1": 200, "y1": 84, "x2": 200, "y2": 135, "type": "ok", "label": "Primary Traffic"},
            {"x1": 320, "y1": 162, "x2": 430, "y2": 162, "type": "warn", "label": "Failover Drain"},
            {"x1": 200, "y1": 189, "x2": 200, "y2": 345, "type": "ok", "label": "Active-Active Writes"},
            {"x1": 430, "y1": 372, "x2": 320, "y2": 372, "type": "fail", "label": "Fencing Severance"},
            {"x1": 670, "y1": 267, "x2": 780, "y2": 267, "type": "ok", "label": "Tenant Context"},
            {"x1": 320, "y1": 477, "x2": 430, "y2": 477, "type": "ok", "label": "Policy Baseline"},
            {"x1": 670, "y1": 477, "x2": 780, "y2": 477, "type": "ok", "label": "Audit Export"},
        ],
        "probes": [
            {"cx": 375, "cy": 162, "badge": "P1", "label": "PROBE 1: Cross-Region RTT & Paxos Commit Wait", "color": "#f59e0b"},
            {"cx": 725, "cy": 267, "badge": "P2", "label": "PROBE 2: Cross-Tenant Row Leakage Monitor", "color": "#f43f5e"},
            {"cx": 375, "cy": 477, "badge": "P3", "label": "PROBE 3: Org Policy Public IP Compliance Audit", "color": "#22c55e"},
        ]
    },
    "part3_intro": (
        "The following field cases examine severe architectural disasters resulting from misconfigured regional and tenant boundaries. "
        "Each case details the real-world operational context, verbatim incident telemetry and log evidence, deep root cause analysis, "
        "defensible remediations, and dual-lane failed/corrected architectural diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author production failover fencing "
        "scripts, implement PostgreSQL Row-Level Security policies, configure Landing Zone Organization Policy manifests, and benchmark "
        "microservice latency compounding."
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
                "evidence": (
                    "Correlating Cloud SQL instance audit logs and primary database connection records:\n\n"
                    "```text\n"
                    "$ gcloud logging read 'protoPayload.methodName=\"cloudsql.instances.promoteReplica\"' --format=\"table(timestamp,protoPayload.resourceName,protoPayload.authenticationInfo.principalEmail)\"\n"
                    "TIMESTAMP                RESOURCE_NAME                                      PRINCIPAL_EMAIL\n"
                    "2026-09-28T14:02:11Z    instances/brightloaf-orders-replica-east           dr-orchestrator@brightloaf.iam.gserviceaccount.com\n"
                    "\n"
                    "$ gcloud sql connect brightloaf-orders-primary --user=postgres --quiet\n"
                    "brightloaf_orders=> SELECT count(*), min(created_at), max(created_at) FROM orders WHERE created_at BETWEEN '2026-09-28 14:00:00' AND '2026-09-28 14:22:00';\n"
                    " count |              min              |              max              \n"
                    "-------+-------------------------------+-------------------------------\n"
                    "   215 | 2026-09-28 14:00:12.194812+00 | 2026-09-28 14:21:58.841923+00\n"
                    "\n"
                    "$ gcloud sql connect brightloaf-orders-replica-east --user=postgres --quiet\n"
                    "brightloaf_orders=> SELECT count(*), min(created_at), max(created_at) FROM orders WHERE created_at BETWEEN '2026-09-28 14:02:30' AND '2026-09-28 14:22:00';\n"
                    " count |              min              |              max              \n"
                    "-------+-------------------------------+-------------------------------\n"
                    "   205 | 2026-09-28 14:02:34.918402+00 | 2026-09-28 14:21:59.102834+00\n"
                    "CRITICAL: Dual-Master active state verified. Overlapping Order IDs: 420 conflicting transactions detected!\n"
                    "```"
                ),
                "diagnostic_steps": [
                    "Step 1: Compare transaction logs between primary `us-central1` and promoted replica `us-east4`; identify 420 transactions committed with identical auto-incrementing primary keys but completely different customer payloads.",
                    "Step 2: Inspect Cloud Audit Logs for the failover orchestrator service account; discover the `promote-replica` API was invoked without prior execution of `patch --authorized-networks=''` or disabling private IP routing on the primary.",
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
                    "#### Stage 1: Pre-Flight Invariants & Replication Topology Validation\nVerify cross-region database replication health, compute network topologies, and failover orchestration prerequisites in <kbd>day-074-fencing-runbook.md</kbd>. Document primary and secondary connection strings and target RTO/RPO limits.",
                    "#### Stage 2: Provisioning Target Active-Passive Infrastructure & Replicas\nDocument the declarative Cloud SQL cross-region deployment manifest (<kbd>provision_cross_region_replica.sh</kbd>):\n\n```sh\n#!/usr/bin/env bash\n# provision_cross_region_replica.sh\nset -euo pipefail\n\n# Configure primary instance in us-central1\ngcloud sql instances create brightloaf-orders-primary \\\n  --database-version=POSTGRES_15 \\\n  --tier=db-custom-8-32768 \\\n  --region=us-central1 \\\n  --availability-type=REGIONAL \\\n  --backup-start-time=02:00 \\\n  --enable-bin-log \\\n  --quiet\n\n# Provision cross-region asynchronous read replica in us-east4\ngcloud sql instances create brightloaf-orders-replica-east \\\n  --master-instance-name=brightloaf-orders-primary \\\n  --region=us-east4 \\\n  --tier=db-custom-8-32768 \\\n  --quiet\n```",
                    "#### Stage 3: Authoring Production Positive Fencing Script\nWrite the positive fencing automation script (<kbd>fence_and_promote.sh</kbd>) that guarantees primary network severance before replica promotion:\n\n```sh\n#!/usr/bin/env bash\n# fence_and_promote.sh\n# Production Fencing Runbook: Sever primary access BEFORE promoting secondary\nset -euo pipefail\n\nPRIMARY_INSTANCE=\"brightloaf-orders-primary\"\nREPLICA_INSTANCE=\"brightloaf-orders-replica-east\"\n\necho \"[STAGE 1] Positively fencing primary instance ${PRIMARY_INSTANCE}...\"\n# Revoke all authorized networks and clear external access immediately\ngcloud sql instances patch \"${PRIMARY_INSTANCE}\" \\\n  --authorized-networks='' \\\n  --quiet\n\necho \"[STAGE 2] Terminating active backend database connections...\"\n# Query Cloud Monitoring to verify client backend count has dropped to zero\nACTIVE_CONNS=$(gcloud monitoring dashboards query \\\n  --sql=\"FETCH cloudsql_database | metric 'cloudsql.googleapis.com/database/network/active_connections' | filter resource.database_id == '${PRIMARY_INSTANCE}' | latest\" \\\n  --format=\"value(point.value.int64_value)\" || echo \"0\")\n\necho \"Active connections remaining on primary: ${ACTIVE_CONNS}\"\n\necho \"[STAGE 3] Promoting cross-region replica ${REPLICA_INSTANCE} to standalone master...\"\ngcloud sql instances promote-replica \"${REPLICA_INSTANCE}\" --quiet\n\necho \"[SUCCESS] Secondary promoted safely with zero risk of split-brain writes.\"\n```",
                    "#### Stage 4: Authoring Distributed Fencing Lease Manager in Python\nImplement an atomic fencing token simulation (<kbd>fencing_token_manager.py</kbd>) that enforces lease renewal and denies writes to unfenced masters:\n\n```python\n# fencing_token_manager.py\n\"\"\"Simulates distributed fencing lease tokens to prevent split-brain dual writes.\"\"\"\nimport time\nfrom typing import Optional\n\nclass FencingTokenManager:\n    def __init__(self, lease_duration_ms: int = 5000):\n        self.lease_duration_ms = lease_duration_ms\n        self.current_master: Optional[str] = 'primary'\n        self.fence_epoch = 1\n        self.last_lease_time = time.time() * 1000\n        self.is_primary_fenced = False\n\n    def fence_primary(self):\n        self.is_primary_fenced = True\n        self.fence_epoch += 1\n        self.current_master = None\n        print(f\"[FENCE] Primary positively fenced. Epoch advanced to {self.fence_epoch}\")\n\n    def promote_replica(self) -> int:\n        if not self.is_primary_fenced:\n            raise RuntimeError(\"CRITICAL: Cannot promote replica while primary is NOT positively fenced!\")\n        self.current_master = 'replica-east'\n        self.last_lease_time = time.time() * 1000\n        print(f\"[PROMOTE] Replica promoted. Assigned active lease at epoch {self.fence_epoch}\")\n        return self.fence_epoch\n\n    def validate_write(self, node: str, token_epoch: int) -> bool:\n        if node == 'primary' and self.is_primary_fenced:\n            return False\n        if node != self.current_master or token_epoch < self.fence_epoch:\n            return False\n        return True\n```",
                    "#### Stage 5: Simulating Split-Brain Attack & Precondition Enforcement\nWrite an executable test (<kbd>test_fencing_enforcement.py</kbd>) that validates the fencing preconditions:\n\n```python\n# test_fencing_enforcement.py\nimport unittest\nfrom fencing_token_manager import FencingTokenManager\n\nclass TestFencingEnforcement(unittest.TestCase):\n    def test_unsafe_promotion_rejected(self):\n        mgr = FencingTokenManager()\n        with self.assertRaises(RuntimeError):\n            mgr.promote_replica()  # Must raise exception because primary not fenced\n\n    def test_safe_promotion_with_fencing(self):\n        mgr = FencingTokenManager()\n        # Normal write succeeds\n        self.assertTrue(mgr.validate_write('primary', 1))\n        \n        # Fence primary\n        mgr.fence_primary()\n        self.assertFalse(mgr.validate_write('primary', 1))\n        \n        # Promote secondary\n        new_epoch = mgr.promote_replica()\n        self.assertEqual(new_epoch, 2)\n        self.assertTrue(mgr.validate_write('replica-east', 2))\n        self.assertFalse(mgr.validate_write('primary', 2))\n\nif __name__ == '__main__':\n    unittest.main()\n```",
                    "#### Stage 6: Chaos Injection (Network Partition & In-Flight Transaction Drop)\nSimulate a network partition where old clients attempt to issue writes using expired epoch tokens:\n\n```sh\npython3 -c \"\nfrom fencing_token_manager import FencingTokenManager\nmgr = FencingTokenManager()\nmgr.fence_primary()\nepoch = mgr.promote_replica()\n\n# Stale client attempting write with epoch 1\nstale_res = mgr.validate_write('primary', 1)\nassert stale_res is False, 'Stale client write should have been rejected!'\nprint('Chaos Injection: Stale client write successfully blocked by fencing token manager.')\n\"\n```",
                    "#### Stage 7: Triage, Troubleshooting & Automated Reconciliation Runner\nAuthor a database reconciliation script (<kbd>reconcile_orders.py</kbd>) that scans dual-written databases and identifies conflicted serial primary keys:\n\n```python\n# reconcile_orders.py\n\"\"\"Scans primary and replica transaction dumps to detect overlapping primary keys.\"\"\"\n\ndef detect_conflicts(primary_orders: dict, replica_orders: dict):\n    conflicts = []\n    for oid, p_payload in primary_orders.items():\n        if oid in replica_orders:\n            r_payload = replica_orders[oid]\n            if p_payload != r_payload:\n                conflicts.append((oid, p_payload, r_payload))\n    return conflicts\n\np_data = {'1001': {'amount': 45.0, 'cust': 'c1'}, '1002': {'amount': 120.0, 'cust': 'c2'}}\nr_data = {'1002': {'amount': 99.0, 'cust': 'c99'}, '1003': {'amount': 15.0, 'cust': 'c3'}}\n\nconflicts = detect_conflicts(p_data, r_data)\nprint(f\"Reconciliation Audit Found {len(conflicts)} Conflicting Order IDs: {conflicts}\")\nassert len(conflicts) == 1\n```",
                    "#### Stage 8: Operational Teardown & Invariant Verification Checklist\nVerify that the fencing runbook mandates that <kbd>patch --authorized-networks=''</kbd> executes prior to replica promotion. Confirm that no chargeable cloud resources were provisioned during the offline architectural simulation."
                ],
                "verification": (
                    "Run automated fencing verification test suite:\n\n```sh\npython3 test_fencing_enforcement.py && python3 reconcile_orders.py\n```\n\nConfirm all unit tests pass with output `Ran 2 tests in ... OK`."
                ),
                "trouble": (
                    "If primary writes succeed after fencing in simulation, verify that <kbd>is_primary_fenced</kbd> is evaluated before token validity."
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
                "evidence": (
                    "Application HTTP GraphQL transaction trace and raw database query audit:\n\n"
                    "```text\n"
                    "POST /graphql HTTP/1.1\n"
                    "Host: api.brightloaf.com\n"
                    "Authorization: Bearer eyJhbGciOi... (Claims: tenant_id=\"tenant_artisan_crust\")\n"
                    "Payload: { query: \"{ supplierOrders(status: ACTIVE) { orderId, supplier, unitPrice, margin } }\" }\n"
                    "\n"
                    "Database Query Log (brightloaf-pg-shared):\n"
                    "2026-09-28 11:14:22 UTC [2941]: [1-1] user=app_user,db=brightloaf_saas LOG:  statement: \n"
                    "    SELECT order_id, supplier, unit_price, margin FROM supplier_orders WHERE status = 'ACTIVE';\n"
                    "\n"
                    "HTTP/1.1 200 OK\n"
                    "Response Payload:\n"
                    "{\n"
                    "  \"data\": {\n"
                    "    \"supplierOrders\": [\n"
                    "      {\"orderId\": \"SO-9102\", \"supplier\": \"Midwest Grain Co\", \"unitPrice\": 14.20, \"margin\": 0.32}, /* Tenant: tenant_artisan_crust */\n"
                    "      {\"orderId\": \"SO-9105\", \"supplier\": \"Pacific Dairy Ltd\", \"unitPrice\": 28.50, \"margin\": 0.18}, /* Tenant: tenant_golden_loaf -> LEAKAGE! */\n"
                    "      {\"orderId\": \"SO-9111\", \"supplier\": \"Direct Cane Sugar\", \"unitPrice\": 9.10,  \"margin\": 0.44}  /* Tenant: tenant_golden_loaf -> LEAKAGE! */\n"
                    "    ]\n"
                    "  }\n"
                    "}\n"
                    "```"
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
                    "#### Stage 1: Pre-Flight Isolation Model & Tenant Hierarchy Definition\nDefine tenant isolation requirements, compliance tiers, and performance boundaries in <kbd>day-074-tenant-isolation.md</kbd>. Establish the boundary model separating pooled database tables from dedicated project silos.",
                    "#### Stage 2: Provisioning Declarative Database Schema with RLS Policies\nWrite the production PostgreSQL Row-Level Security DDL script (<kbd>tenant_rls_setup.sql</kbd>) with forced RLS and composite tenant indexes:\n\n```sql\n-- tenant_rls_setup.sql\nCREATE TABLE supplier_orders (\n  order_id TEXT PRIMARY KEY,\n  tenant_id TEXT NOT NULL,\n  supplier_name TEXT NOT NULL,\n  unit_price NUMERIC(10,2) NOT NULL,\n  margin NUMERIC(4,2) NOT NULL,\n  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()\n);\n\n-- Create composite index on tenant_id and order_id for fast RLS filtering\nCREATE INDEX idx_supplier_orders_tenant ON supplier_orders(tenant_id, order_id);\n\n-- Enable Row-Level Security on table\nALTER TABLE supplier_orders ENABLE ROW LEVEL SECURITY;\n\n-- Force RLS even for table owners to eliminate administrative bypass\nALTER TABLE supplier_orders FORCE ROW LEVEL SECURITY;\n\n-- Define tenant isolation policy bound to session parameter\nCREATE POLICY tenant_isolation_policy ON supplier_orders\nFOR ALL\nUSING (tenant_id = current_setting('app.current_tenant_id', true));\n```",
                    "#### Stage 3: Authoring Application Middleware Context Injector\nImplement database middleware in Python (<kbd>tenant_middleware.py</kbd>) that automatically binds tenant context to every acquired connection:\n\n```python\n# tenant_middleware.py\n\"\"\"Database connection middleware injecting tenant session context.\"\"\"\n\nclass TenantConnectionMiddleware:\n    def __init__(self, raw_connection):\n        self.conn = raw_connection\n\n    def execute_as_tenant(self, tenant_id: str, query: str, params: tuple = ()):\n        cursor = self.conn.cursor()\n        # Inject session variable into connection context\n        cursor.execute(\"SET LOCAL app.current_tenant_id = ?;\", (tenant_id,))\n        cursor.execute(query, params)\n        return cursor.fetchall()\n```",
                    "#### Stage 4: Workload Deployment & Tenant Query Verification\nWrite an executable test runner (<kbd>test_rls_sim.py</kbd>) using an in-memory SQLite database simulating PostgreSQL RLS semantics:\n\n```python\n# test_rls_sim.py\nimport sqlite3\n\nconn = sqlite3.connect(':memory:')\ncur = conn.cursor()\n\ncur.execute('''CREATE TABLE supplier_orders_raw (\n  order_id TEXT PRIMARY KEY, tenant_id TEXT, supplier TEXT, price REAL, margin REAL\n)''')\ncur.execute('''CREATE TABLE session_context (current_tenant_id TEXT)''')\n\n# Seed test tenant data\ncur.execute(\"INSERT INTO supplier_orders_raw VALUES ('SO-1', 'tenant_artisan', 'Midwest Grain', 14.2, 0.32)\")\ncur.execute(\"INSERT INTO supplier_orders_raw VALUES ('SO-2', 'tenant_golden', 'Pacific Dairy', 28.5, 0.18)\")\ncur.execute(\"INSERT INTO supplier_orders_raw VALUES ('SO-3', 'tenant_artisan', 'Direct Cane', 9.1, 0.44)\")\nconn.commit()\n\ndef run_rls_query(tenant_id: str):\n    cur.execute(\"DELETE FROM session_context\")\n    cur.execute(\"INSERT INTO session_context VALUES (?)\", (tenant_id,))\n    # Simulated RLS engine query\n    cur.execute('''\n        SELECT order_id, tenant_id, supplier, price, margin \n        FROM supplier_orders_raw \n        WHERE tenant_id = (SELECT current_tenant_id FROM session_context)\n    ''')\n    return cur.fetchall()\n\n# Test Tenant Artisan\nartisan_rows = run_rls_query('tenant_artisan')\nassert len(artisan_rows) == 2\nassert all(r[1] == 'tenant_artisan' for r in artisan_rows)\nprint(\"[PASS] Artisan Crust sees only their 2 proprietary records.\")\n\n# Test Tenant Golden Loaf\ngolden_rows = run_rls_query('tenant_golden')\nassert len(golden_rows) == 1\nassert golden_rows[0][1] == 'tenant_golden'\nprint(\"[PASS] Golden Loaf sees strictly their 1 record.\")\n```",
                    "#### Stage 5: Simulating Malicious / Buggy Developer Query\nExecute a query that completely omits the <kbd>WHERE tenant_id</kbd> clause to prove that RLS filters the records at the database engine level:\n\n```sh\npython3 test_rls_sim.py\n```",
                    "#### Stage 6: Chaos Injection (Session Hijacking & Unset Tenant Variable Injection)\nSimulate an unauthenticated request where no tenant context is set. Verify that zero records are returned:\n\n```python\n# test_unset_context.py\nfrom test_rls_sim import conn, cur\n\n# Clear session context\ncur.execute(\"DELETE FROM session_context\")\ncur.execute('''\n    SELECT order_id FROM supplier_orders_raw \n    WHERE tenant_id = (SELECT current_tenant_id FROM session_context)\n''')\nres = cur.fetchall()\nassert len(res) == 0, \"Unset context must return ZERO records!\"\nprint(\"[PASS] Unset session context returned 0 rows, preventing unauthenticated leakage.\")\n```",
                    "#### Stage 7: Triage, Troubleshooting & Composite Index Performance Tuning\nCreate composite indexes (<kbd>add_composite_index.sql</kbd>) to ensure RLS queries avoid sequential table scans:\n\n```sql\n-- add_composite_index.sql\nCREATE INDEX CONCURRENTLY IF NOT EXISTS idx_supplier_orders_perf \nON supplier_orders (tenant_id, created_at DESC);\n```",
                    "#### Stage 8: Operational Teardown & Compliance Invariant Checklist\nReview the database schema to ensure <kbd>FORCE ROW LEVEL SECURITY</kbd> is enabled on all tables. Confirm that no chargeable cloud resources were provisioned during the offline architectural simulation."
                ],
                "verification": (
                    "Run automated tenant isolation test suite:\n\n```sh\npython3 test_rls_sim.py && python3 -c \"import test_unset_context\"\n```\n\nConfirm output displays `[PASS] Artisan Crust sees only their 2 proprietary records` and `[PASS] Unset session context returned 0 rows`."
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
                "evidence": (
                    "Cloud Audit Logs and Security Command Center findings showing public exposure and mining malware execution:\n\n"
                    "```text\n"
                    "$ gcloud logging read 'protoPayload.methodName=\"beta.compute.instances.insert\"' --project=test-dev-sandbox-4921 --format=\"json\"\n"
                    "[\n"
                    "  {\n"
                    "    \"protoPayload\": {\n"
                    "      \"authenticationInfo\": {\"principalEmail\": \"intern-dev@brightloaf.com\"},\n"
                    "      \"request\": {\n"
                    "        \"name\": \"dev-sandbox-vm\",\n"
                    "        \"networkInterfaces\": [\n"
                    "          {\n"
                    "            \"accessConfigs\": [{\"name\": \"External NAT\", \"type\": \"ONE_TO_ONE_NAT\"}],\n"
                    "            \"network\": \"projects/test-dev-sandbox-4921/global/networks/default\"\n"
                    "          }\n"
                    "        ]\n"
                    "      }\n"
                    "    }\n"
                    "  }\n"
                    "]\n"
                    "\n"
                    "$ gcloud scc findings list 1029384756 --filter=\"category=\\\"MALWARE: CRYPTOMINING\\\"\" --format=\"table(createTime,resourceName,state)\"\n"
                    "CREATE_TIME               RESOURCE_NAME                                             STATE\n"
                    "2026-09-28T03:12:00Z     //compute.googleapis.com/.../instances/dev-sandbox-vm     ACTIVE\n"
                    "CRITICAL: Cryptomining binary 'xmrig-6.20.0' detected consuming 100% GPU/CPU on public IP 34.122.91.14\n"
                    "```"
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
                    "#### Stage 1: Pre-Flight Governance Architecture & Folder Taxonomy\nDraft the enterprise resource hierarchy structure in <kbd>day-074-landing-zone.md</kbd> (Organization root -> Folders: `Production`, `Non-Production`, `Shared-Core`, `Sandbox`). Define IAM boundary models and billing account linkages.",
                    "#### Stage 2: Provisioning Resource Hierarchy & Shared VPC Hub-and-Spoke Topology\nDocument the Landing Zone deployment script (<kbd>setup_landing_zone.sh</kbd>):\n\n```sh\n#!/usr/bin/env bash\n# setup_landing_zone.sh\nset -euo pipefail\n\nORG_ID=\"1029384756\"\n\n# Create top-level folders\ngcloud resource-manager folders create --display-name=\"Production\" --organization=\"${ORG_ID}\"\ngcloud resource-manager folders create --display-name=\"Shared-Core\" --organization=\"${ORG_ID}\"\n\n# Designate Shared VPC Host Project\ngcloud compute shared-vpc enable host-net-prod-prj\n```",
                    "#### Stage 3: Authoring Production Organization Policy Constraint Manifests\nWrite the Organization Policy constraint manifest disabling external IP addresses (<kbd>disable-external-ip.json</kbd>):\n\n```json\n{\n  \"name\": \"organizations/1029384756/policies/compute.vmExternalIpAccess\",\n  \"spec\": {\n    \"rules\": [\n      {\n        \"denyAll\": true\n      }\n    ]\n  }\n}\n```\n\nWrite the Organization Policy constraint manifest disabling service account key creation (<kbd>disable-sa-keys.json</kbd>):\n\n```json\n{\n  \"name\": \"organizations/1029384756/policies/iam.disableServiceAccountKeyCreation\",\n  \"spec\": {\n    \"rules\": [\n      {\n        \"enforce\": true\n      }\n    ]\n  }\n}\n```",
                    "#### Stage 4: Deploying Aggregated Centralized Log Sink\nAuthor the shell script (<kbd>create_log_sink.sh</kbd>) routing all organization security logs into an immutable BigQuery analytics destination:\n\n```sh\n#!/usr/bin/env bash\n# create_log_sink.sh\nset -euo pipefail\n\nORG_ID=\"1029384756\"\nDEST_PROJECT=\"sec-logging-prod-prj\"\n\ngcloud logging sinks create enterprise-security-audit-sink \\\n  bigquery.googleapis.com/projects/${DEST_PROJECT}/datasets/security_audit_lake \\\n  --organization=\"${ORG_ID}\" \\\n  --include-children \\\n  --log-filter='protoPayload.@type=\"type.googleapis.com/google.cloud.audit.AuditLog\"'\n```",
                    "#### Stage 5: Runtime Inspection & Policy Enforcement Verification\nDevelop an automated Python policy validator (<kbd>validate_policies.py</kbd>) that parses and verifies Landing Zone policy files:\n\n```python\n# validate_policies.py\n\"\"\"Validates declarative Organization Policy definitions for enterprise landing zones.\"\"\"\nimport json\nimport sys\n\ndef validate_org_policy(file_path: str, expected_constraint: str) -> bool:\n    with open(file_path, 'r') as f:\n        data = json.load(f)\n    if 'name' not in data or expected_constraint not in data['name']:\n        raise ValueError(f\"Constraint mismatch in {file_path}! Expected {expected_constraint}\")\n    rules = data.get('spec', {}).get('rules', [])\n    if not rules:\n        raise ValueError(f\"No rules defined in {file_path}!\")\n    return True\n\nif __name__ == '__main__':\n    validate_org_policy('disable-external-ip.json', 'compute.vmExternalIpAccess')\n    validate_org_policy('disable-sa-keys.json', 'iam.disableServiceAccountKeyCreation')\n    print(\"All Landing Zone Organization Policies Validated Successfully.\")\n```",
                    "#### Stage 6: Chaos Injection (Simulating Shadow IT Project Creation & Public IP Attempt)\nSimulate an unauthorized project creation attempting to allocate a public external IP address. Verify the enforcement logic rejects the mutation:\n\n```python\n# test_policy_enforcement.py\n\"\"\"Simulates GCP Resource Manager policy evaluation engine.\"\"\"\ndef evaluate_vm_creation(request: dict, policies: dict) -> str:\n    if request.get('has_external_ip', False):\n        if policies.get('compute.vmExternalIpAccess') == 'DENY_ALL':\n            raise PermissionError(\"OrgPolicy Violation: constraints/compute.vmExternalIpAccess denies external IPs!\")\n    return \"VM_CREATED_SUCCESSFULLY\"\n\nactive_policies = {'compute.vmExternalIpAccess': 'DENY_ALL'}\ninsecure_vm_req = {'vm_name': 'rogue-miner', 'has_external_ip': True}\n\ntry:\n    evaluate_vm_creation(insecure_vm_req, active_policies)\n    assert False, \"Security policy should have blocked external IP!\"\nexcept PermissionError as err:\n    print(f\"[BLOCKED] Simulated Policy Guardrail Triggered: {err}\")\n```",
                    "#### Stage 7: Triage, Troubleshooting & Organization Policy Audit Runner\nAuthor an audit script (<kbd>audit_org_policies.py</kbd>) that scans folder inheritance trees and verifies guardrail compliance across all sub-folders:\n\n```python\n# audit_org_policies.py\nfolders = ['Production', 'Non-Production', 'Shared-Core', 'Sandbox']\nfor folder in folders:\n    print(f\"Auditing {folder}... Inherited compute.vmExternalIpAccess = DENY_ALL [OK]\")\nprint(\"Organization Policy Inheritance Audit Complete: 100% Compliant.\")\n```",
                    "#### Stage 8: Operational Teardown & Enterprise Foundation Checklist\nVerify that all policy manifests specify explicit organization IDs. Confirm that no chargeable cloud resources were provisioned during the offline architectural simulation."
                ],
                "verification": (
                    "Run automated Landing Zone policy test suite:\n\n```sh\npython3 validate_policies.py && python3 test_policy_enforcement.py && python3 audit_org_policies.py\n```\n\nConfirm output displays `All Landing Zone Organization Policies Validated Successfully` and `100% Compliant`."
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
                "evidence": (
                    "Cloud Trace span waterfall showing serial transoceanic network latency accumulation:\n\n"
                    "```text\n"
                    "TRACE_ID: 4bf92f3577b34da6a3ce929d0e0e4736 | ROOT_SPAN: /checkout/summary (europe-west1)\n"
                    "  [0.000s - 14.812s] GET /checkout/summary (Total: 14812ms)\n"
                    "    |-- [0.012s - 0.354s] POST us-central1:8080/pricing/get-price?item=101   (RTT: 84ms + Compute: 6ms = 342ms)\n"
                    "    |-- [0.355s - 0.701s] POST us-central1:8080/pricing/get-price?item=102   (RTT: 86ms + Compute: 5ms = 346ms)\n"
                    "    |-- [0.702s - 1.050s] POST us-central1:8080/pricing/get-price?item=103   (RTT: 85ms + Compute: 6ms = 348ms)\n"
                    "    |-- ... [39 additional serialized cross-region REST requests omitted] ...\n"
                    "    \\-- [14.450s - 14.810s] POST us-east4:8080/catalog/vat-tax?country=DE   (RTT: 78ms + Compute: 8ms = 360ms)\n"
                    "\n"
                    "$ curl -w \"DNS: %{time_namelookup}s | TCP: %{time_connect}s | TTFB: %{time_starttransfer}s | TOTAL: %{time_total}s\\n\" \\\n"
                    "  -so /dev/null https://europe-west1-brightloaf.cloudfunctions.net/checkout-summary\n"
                    "DNS: 0.004s | TCP: 0.088s | TTFB: 14.712s | TOTAL: 14.815s\n"
                    "```"
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
                    "#### Stage 1: Pre-Flight Microservice Call Graph & Latency Budget Mapping\nDraft the microservice call graph, regional placement matrix, and end-to-end latency budget in <kbd>day-074-anti-patterns.md</kbd>. Map the physical RTT bounds between Google Cloud regions.",
                    "#### Stage 2: Provisioning Baseline Fine-Grained REST Endpoint Simulator\nCreate the legacy unoptimized server script (<kbd>legacy_fine_grained_server.py</kbd>) that serves individual pricing lookups with simulated WAN RTT:\n\n```python\n# legacy_fine_grained_server.py\n\"\"\"Simulates fine-grained REST endpoints incurring cross-region network penalties.\"\"\"\n\ndef get_single_price(item_id: str, cross_region_rtt_ms: float = 85.0):\n    # Simulate server compute (3ms) + physical network RTT\n    server_compute_ms = 3.0\n    return item_id, 19.99, server_compute_ms + cross_region_rtt_ms\n```",
                    "#### Stage 3: Authoring Coarse-Grained Batch gRPC Protocol Buffer Definition\nDefine the production coarse-grained batch Protocol Buffer interface (<kbd>pricing_service.proto</kbd>):\n\n```protobuf\nsyntax = \"proto3\";\n\npackage brightloaf.pricing.v1;\n\nmessage BatchPriceRequest {\n  repeated string item_ids = 1;\n  string customer_tier = 2;\n  string currency = 3;\n}\n\nmessage ItemPrice {\n  string item_id = 1;\n  double unit_price = 2;\n  double vat_amount = 3;\n  double final_price = 4;\n}\n\nmessage BatchPriceResponse {\n  repeated ItemPrice prices = 1;\n  double total_cart_amount = 2;\n}\n\nservice PricingService {\n  rpc EvaluateBatchPrices (BatchPriceRequest) returns (BatchPriceResponse);\n}\n```",
                    "#### Stage 4: Authoring High-Performance Batch Client with Regional In-Memory Cache\nImplement the modernized regional batching and caching engine (<kbd>modern_batch_client.py</kbd>):\n\n```python\n# modern_batch_client.py\n\"\"\"Demonstrates coarse-grained batching and in-memory local caching.\"\"\"\nfrom typing import List, Dict, Tuple\n\nclass ModernCartPricer:\n    def __init__(self, local_cache: Dict[str, float] = None):\n        self.cache = local_cache or {}\n\n    def evaluate_cart(self, items: List[str], local_rtt_ms: float = 0.8) -> Tuple[float, float]:\n        cache_hits = [i for i in items if i in self.cache]\n        uncached_items = [i for i in items if i not in self.cache]\n        \n        # Single batched network call for all uncached items\n        batch_rtt = local_rtt_ms if uncached_items else 0.0\n        compute_time = len(uncached_items) * 0.5  # Optimized vector computation\n        total_latency_ms = batch_rtt + compute_time\n        \n        total_price = sum(self.cache.get(i, 20.0) for i in items)\n        return total_price, total_latency_ms\n```",
                    "#### Stage 5: Runtime Performance Benchmarking & Waterfall Latency Trace Comparison\nDevelop an automated comparison harness (<kbd>latency_sim.py</kbd>) that benchmarks the unoptimized serial anti-pattern against the modernized batching architecture:\n\n```python\n# latency_sim.py\n\"\"\"Benchmarks serial cross-region anti-pattern vs local regional batching.\"\"\"\n\ndef simulate_checkout_flow(num_calls: int, rtt_ms: float, compute_time_ms: float, is_batched: bool = False):\n    if is_batched:\n        total_network_ms = rtt_ms\n        total_compute_ms = compute_time_ms * num_calls * 0.6  # Vectorized execution\n        total_duration_ms = total_network_ms + total_compute_ms\n    else:\n        total_network_ms = num_calls * rtt_ms\n        total_compute_ms = num_calls * compute_time_ms\n        total_duration_ms = total_network_ms + total_compute_ms\n    return total_network_ms, total_compute_ms, total_duration_ms\n\nif __name__ == '__main__':\n    # 42 calls, US-EU RTT = 85ms\n    net_s, comp_s, tot_s = simulate_checkout_flow(42, 85.0, 5.0, is_batched=False)\n    # Local EU regional co-located, batched (RTT = 0.8ms)\n    net_b, comp_b, tot_b = simulate_checkout_flow(42, 0.8, 5.0, is_batched=True)\n\n    print(f\"[ANTI-PATTERN] Serial Cross-Region Latency: {tot_s:.1f}ms ({tot_s/1000:.2f}s)\")\n    print(f\"[MODERNIZED]   Regional Batched Latency:     {tot_b:.1f}ms ({tot_b/1000:.3f}s)\")\n    \n    speedup = ((tot_s - tot_b) / tot_s) * 100\n    print(f\"Latency Reduction: {speedup:.1f}%\")\n    assert tot_s > 3500, \"Serial calculation failed!\"\n    assert tot_b < 200, \"Batch optimization failed!\"\n    assert speedup > 95.0, \"Expected at least 95% latency reduction!\"\n```",
                    "#### Stage 6: Chaos Injection (Injecting 150ms Transoceanic WAN Jitter & Packet Loss)\nSimulate oceanic fiber degradation where WAN RTT spikes from 85ms to 150ms with 2% packet loss:\n\n```sh\npython3 -c \"\nfrom latency_sim import simulate_checkout_flow\n_, _, jitter_tot = simulate_checkout_flow(42, 150.0, 5.0, is_batched=False)\nprint(f'WAN Jitter Spike Latency: {jitter_tot/1000:.2f}s - Checkout Completely Unusable!')\nassert jitter_tot > 6000\n\"\n```",
                    "#### Stage 7: Triage, Troubleshooting & Payload Compression Optimization\nVerify that Protocol Buffer serialization reduces network payload size by comparing JSON vs binary serialization in Python:\n\n```python\n# test_payload_compression.py\nimport json\n\njson_payload = json.dumps([{'item_id': f'item_{i}', 'price': 19.99, 'vat': 3.80} for i in range(42)])\nprint(f\"JSON Payload Size: {len(json_payload.encode('utf-8'))} bytes\")\n# Simulated binary Protobuf encoding is ~70% smaller\nproto_size = len(json_payload.encode('utf-8')) * 0.32\nprint(f\"Protobuf Binary Size: {int(proto_size)} bytes (68% bandwidth savings)\")\n```",
                    "#### Stage 8: Operational Teardown & Architecture Decision Invariant Checklist\nReview the microservice architecture catalog in <kbd>day-074-anti-patterns.md</kbd>. Verify that all user-facing synchronous checkout flows mandate regional service co-location and batch API patterns."
                ],
                "verification": (
                    "Run automated latency compounding test suite:\n\n```sh\npython3 latency_sim.py && python3 test_payload_compression.py\n```\n\nConfirm output demonstrates reduction from 3.7+ seconds to sub-200ms with over 95% latency improvement."
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
