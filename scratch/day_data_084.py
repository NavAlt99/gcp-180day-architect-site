"""day_data_084.py — Exhaustive architecture data specification for Day 84.

Covers Failure Domains and Graceful Degradation:
1. Failure domains (instance, zone, region, service, dependency, human error blast radiuses).
2. HA vs Fault Tolerance vs Disaster Recovery vs Backup (the four distinct operational pillars).
3. Graceful degradation and load shedding (priority tiers, circuit breakers, shedding mechanics).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 84

DATA = {
    "day": 84,
    "part1_intro": (
        "Day 84 advances Block 4 by deconstructing cloud failure domains and establishing the architectural boundaries "
        "of resilient system design. Cloud systems do not fail uniformly; failure occurs along discrete, predictable boundaries "
        "spanning individual hardware instances, availability zones, entire geographic regions, upstream cloud provider control planes, "
        "external SaaS dependencies, and human operator misconfigurations. Architects must strictly distinguish between four frequently "
        "conflated concepts: High Availability (minimizing downtime via automated failover), Fault Tolerance (zero perceptible interruption "
        "via lock-step redundancy), Disaster Recovery (restoring operations after catastrophic regional loss), and Backups (inert point-in-time "
        "data preservation). Today's curriculum maps each failure domain to concrete Google Cloud containment controls and implements "
        "graceful degradation and load shedding to ensure core business fulfillment survives severe infrastructure brownouts."
    ),
    "exit_summary": (
        "Constructed an exhaustive failure domain matrix mapping 6 distinct boundaries (instance, zone, region, service, dependency, "
        "human error) to blast radiuses and mitigation controls; formally defined architectural boundaries distinguishing HA, Fault "
        "Tolerance, DR, and Backups across RTO, RPO, and cost vectors; conducted a three-part tabletop stress test simulating zone "
        "evacuation, payment dependency blackout, and administrative credential revocation; deployed a Python load shedding simulator "
        "enforcing request priority tiers (Critical, Standard, Sheddable) under 300% overload."
    ),
    "part2_intro": (
        "Resilient architecture demands understanding the blast radius of every boundary in the system. The sections below provide "
        "deep technical specifications for Google Cloud failure domains, operational continuity pillars, and load-shedding control loops."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Operational Concept</th>
      <th>Primary Objective</th>
      <th>Target RTO / RPO</th>
      <th>Cost &amp; Complexity</th>
      <th>Google Cloud Reference Architecture</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>High Availability (HA)</strong></td>
      <td>Automate failover to redundant healthy nodes within a region during hardware or zonal faults.</td>
      <td>RTO: &lt; 60 seconds<br>RPO: 0 (synchronous)</td>
      <td>Moderate (+100% compute/disk redundancy)</td>
      <td>Regional Managed Instance Groups (MIG) across 3 AZs; Cloud SQL HA with Regional Persistent Disk replication.</td>
    </tr>
    <tr>
      <td><strong>Fault Tolerance (FT)</strong></td>
      <td>Guarantee zero downtime and zero data loss; system masks hardware crashes without connection drops.</td>
      <td>RTO: 0 seconds<br>RPO: 0 seconds</td>
      <td>Extreme (+200–300% multi-region redundancy)</td>
      <td>Cloud Spanner multi-region instance with Paxos distributed consensus across 3 regions; Anycast Global External ALB.</td>
    </tr>
    <tr>
      <td><strong>Disaster Recovery (DR)</strong></td>
      <td>Re-establish system operations in a secondary geographic region following catastrophic primary regional loss.</td>
      <td>RTO: 15m – 4 hours<br>RPO: &lt; 15 minutes</td>
      <td>Low to Moderate (pilot light or warm standby)</td>
      <td>Cross-region asynchronous database replicas; Cloud Storage dual-region/multi-region buckets; Terraform automated infrastructure spin-up.</td>
    </tr>
    <tr>
      <td><strong>Backup &amp; Archive</strong></td>
      <td>Preserve immutable, point-in-time snapshots for regulatory compliance, audit, and ransomware/corruption recovery.</td>
      <td>RTO: Hours to Days<br>RPO: Backup interval (e.g. 24h)</td>
      <td>Lowest (storage cost only)</td>
      <td>Cloud Storage Coldline/Archive with Object Retention Lock (WORM); Cloud SQL Automated Backups &amp; PITR transaction logs.</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 84: Failure Domain Containment and Graceful Degradation Hierarchy",
        "desc": "Hierarchical boundary mapping from edge ingress down to data persistence, showing degradation isolation lines.",
        "caption": "Figure 84.1: Architecture failure containment hierarchy illustrating zone, region, and dependency blast-radius fences.",
        "nodes": [
            ("1. Ingress & Armor", "Anycast Edge + Rate Limiting\\nLoad Shedding (L4/L7)"),
            ("2. Regional App Mesh", "Multi-Zone Regional MIG\\nZonal Blast Radius Fence"),
            ("3. Fallback Circuit", "Cache / Static Responses\\nAsync Outbox Buffer"),
            ("4. Data Persistence", "Regional PD / Spanner Paxos\\nCorrelated Failure Barrier"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Failure domains: instance, zone, region, service, dependency, and human error",
            "preview": (
                "A company deploys its entire microservice architecture across three Compute Engine instances in a single zone (us-central1-a). "
                "When a routine substation transformer failure knocks out power to that zone, all 14 services go dark simultaneously for 4 hours."
            ),
            "overview": (
                "A failure domain is an architectural boundary within which a single fault, event, or configuration error is contained. "
                "In Google Cloud, failure domains form a strict physical and logical hierarchy: instance (local hypervisor or CPU fault), "
                "zone (datacenter power, cooling, or intra-zone network switch failure), region (metropolitan fiber severing, severe weather, "
                "or regional control plane partition), service (outage of a specific managed API like Pub/Sub or Cloud IAM), external dependency "
                "(outage of a third-party payment gateway or logistics ERP), and human error (fat-finger command, unauthorized schema wipe, or malformed "
                "Terraform push). Rigorous architects design systems such that a failure in an inner domain is strictly isolated and automatically "
                "masked by outer domain controls, preventing localized disruptions from escalating into enterprise-wide outages."
            ),
            "technical": (
                "Architects must classify each infrastructure tier against the six canonical cloud failure domains:\n\n"
                "### 1. The Physical Hierarchy: Instance, Zone, and Region\n"
                "- **Instance Domain:** Confined to single host server hardware or kernel crashes. Handled seamlessly by Compute Engine **Live Migration** "
                "(transparently moving running VMs to new hosts during hypervisor maintenance without stopping the guest OS) and Regional MIG **Autohealing**.\n"
                "- **Zone Domain (AZ):** Datacenters within a region have independent power, cooling, and networking feeds. A zonal failure drops all "
                "zonal Persistent Disks and non-HA instances in that zone. Handled by **Regional MIGs** distributing instances evenly across 3 AZs and **Cloud SQL HA**.\n"
                "- **Region Domain:** Geographic areas separated by at least 100 miles. Handled by **Global External Application Load Balancers** "
                "routing traffic across multi-region backend services via Anycast BGP.\n\n"
                "### 2. The Logical Hierarchy: Service, Dependency, and Human\n"
                "- **Managed Service Domain:** Regional control plane degradation (e.g., Compute Engine API cannot accept new `instances.insert` calls). "
                "Handled by pre-provisioning capacity (N+1 over-provisioning) and avoiding runtime reliance on control-plane APIs during auto-scale events.\n"
                "- **External Dependency Domain:** Downstream third-party systems (Stripe, Twilio, Salesforce) fail or throttle. Handled by **Circuit Breakers** "
                "(Envoy/Istio), fallback stale caching, and asynchronous dead-letter queues.\n"
                "- **Human Error Domain:** Accounts for >70% of enterprise outages. Handled by GitOps, automated CI/CD canary validations, Terraform state locking, "
                "IAM Principle of Least Privilege, and immutable Cloud Storage bucket locks."
            ),
            "questions": [
                "How does Compute Engine Live Migration prevent instance-domain hardware failures from affecting running applications?",
                "What is the blast radius difference between a zonal Persistent Disk failure and a regional Persistent Disk failure?",
                "Why must automated autoscaling avoid synchronous calls to the Compute Engine control plane during an active regional disaster?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/failure-domains",
            "reference_label": "Google Cloud Architecture Framework: Defining and isolating failure domains",
            "scenario": {
                "symptom": (
                    "Brightloaf experienced a 90-minute complete outage of its Order Processing API when Google Cloud experienced an electrical "
                    "switchgear fault in `us-central1-f`. Investigation revealed that while web servers were multi-zone, the Redis caching layer "
                    "and internal API gateway were hardcoded to IP addresses located solely in `us-central1-f`."
                ),
                "constraints": (
                    "Must maintain sub-50ms cache response times, ensure zero lost orders, and operate within the existing monthly cloud infrastructure budget."
                ),
                "evidence": (
                    "Cloud Logging showed 100% of API requests failing with `RedisConnectionException: Connection refused to 10.128.1.15:6379`. "
                    "The IP address mapped to a standalone Compute Engine VM in `us-central1-f` that was forcibly terminated by the host power outage."
                ),
                "diagnostic_steps": [
                    "Correlate Google Cloud Service Health Dashboard zonal incidents for `us-central1-f` with Brightloaf API error spikes.",
                    "Audit GCP internal route tables and DNS private zones to trace the physical zone location of the Redis cache host.",
                    "Inspect GKE pod logs to verify that application pods in healthy zones `us-central1-a` and `us-central1-b` crashed solely due to Redis connection timeouts.",
                ],
                "root": (
                    "Architectural failure domain mismatch: multi-zone application workloads were coupled to a single-zone stateful Redis cache, "
                    "collapsing the effective availability boundary of the entire system down to a single zone."
                ),
                "fix": (
                    "Migrate the standalone Redis cache to Memorystore for Redis Standard Tier (with automated cross-zone replica and automatic failover in <30 seconds), "
                    "and configure application connection strings to use the managed VIP rather than a physical zonal IP."
                ),
                "verify": (
                    "Initiate a controlled failover drill via `gcloud memorystore instances failover`; verify zero dropped transactions and cache availability restored within 22 seconds."
                ),
                "residual": (
                    "During the 20-30 second Memorystore failover window, in-flight Redis writes are lost, requiring cache client retry logic."
                ),
                "diagram": (
                    "Zonal power fault",
                    "Redis single-zone crash",
                    "Multi-zone app collapse",
                    "Memorystore HA replica",
                    "Sub-30s auto failover"
                ),
                "facts": "Zonal power cut in us-central1-f brought down entire multi-zone application due to single-zone Redis dependency.",
                "inference": "A system's failure domain is dictated by its least resilient critical-path component.",
                "expected": "Memorystore Standard Tier automatically shifts traffic to healthy replica in us-central1-a without manual intervention."
            },
            "lab": {
                "name": "Failure Domain Mapping and Boundary Audit",
                "file": "day-084-topic-01-failure-domains.md",
                "goal": "Map an enterprise architecture against six cloud failure domains and author verification commands to confirm regional boundaries.",
                "expected": "A comprehensive failure matrix Markdown artifact documenting blast radius, mitigation controls, and boundary verification commands.",
                "mode": "tabletop analysis & architecture synthesis",
                "prereq": "Review Day 83 SPOF audit artifact.",
                "preflight": "Initialize audit document template in workspace.",
                "steps": [
                    "Author the failure domain audit matrix:\n\n```sh\ncat <<'EOF' > day-084-topic-01-failure-domains.md\n# Day 84: Enterprise Failure Domain Boundary Matrix\n\n## 1. Domain Boundary Audit\n\n| Failure Domain | Primary Threat | Blast Radius | Containment Control | Verification Check |\n| :--- | :--- | :--- | :--- | :--- |\n| **Instance** | Host CPU/RAM crash, hypervisor update | 1 VM instance | Regional MIG Autohealing + Live Migration | `gcloud compute instances describe <VM> --format='value(scheduling.onHostMaintenance)'` |\n| **Zone (AZ)** | Data center power, cooling, local fiber | 1 Availability Zone | Multi-Zone Regional MIG (3 AZs) + Cloud SQL HA | `gcloud compute instance-groups managed list-instances <RMIG>` |\n| **Region** | Metropolitan fiber cut, severe storm | Entire GCP Region | Anycast Global External ALB + Multi-Region Spanner | `gcloud compute backend-services describe <SVC> --global` |\n| **Service API** | Cloud Control Plane throttling/outage | Provisioning operations | N+1 capacity headroom; zero runtime control-plane calls | `gcloud monitoring metric-descriptors list --filter='metric.type=\"compute.googleapis.com\"'` |\n| **Dependency** | Payment Gateway / Third-party SaaS | Checkout completion | Asynchronous Pub/Sub Outbox + Circuit Breakers | Tabletop circuit-breaker trip verification |\n| **Human Error** | Accidental table drop or bad config | System-wide corruption | Terraform state locking + IAM Least Privilege + WORM Storage | `gcloud storage buckets describe gs://<BUCKET> --format='value(retentionPolicy)'` |\n\n## 2. Tabletop Verification\n- Confirmed all critical stateful dependencies possess cross-zone replication.\n- Verified Compute Engine Live Migration policy is set to `MIGRATE`, not `TERMINATE`.\nEOF\ncat day-084-topic-01-failure-domains.md\n```",
                    "Verify that the matrix distinguishes between data-plane survival and control-plane provisioning limits.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists and covers all 6 failure domains with concrete GCP commands and architectural containment controls."
                ),
                "trouble": "Ensure Live Migration scheduling is set to `MIGRATE` for production Compute Engine workloads.",
                "cleanup": "Retain `day-084-topic-01-failure-domains.md` as an exit evidence artifact.",
                "accept": "Completed failure domain matrix with verified containment controls across all six architectural tiers."
            }
        },
        {
            "key": "topic-02",
            "title": "HA vs fault tolerance vs disaster recovery vs backup: four distinct operational pillars",
            "preview": (
                "An engineering director cancels the disaster recovery program, arguing that 'our database has High Availability enabled, so we are protected against disasters.' "
                "When a ransomware attack encrypts the primary database, the HA mechanism faithfully replicates the encrypted corrupt blocks to the standby in 40 milliseconds, wiping out all copies."
            ),
            "overview": (
                "Enterprise architects must rigorously distinguish between High Availability (HA), Fault Tolerance (FT), Disaster Recovery (DR), "
                "and Backup. Conflating these four concepts is one of the most dangerous and common anti-patterns in enterprise IT. "
                "HA protects against localized hardware or zonal failures by providing automated, sub-minute failover to a hot standby in the same region. "
                "Fault Tolerance completely masks component failures with zero downtime and zero data loss through continuous lock-step replication (e.g., Paxos consensus). "
                "Disaster Recovery provides structured operational processes and cross-region replication to resurrect an entire business application following "
                "a catastrophic regional loss. Backups provide point-in-time, immutable snapshots to recover from data corruption, accidental deletion, or ransomware. "
                "HA does not protect against regional destruction or logical data corruption; backups do not provide high availability."
            ),
            "technical": (
                "A rigorous engineering comparison of the four continuity pillars:\n\n"
                "### 1. High Availability (HA) Mechanics\n"
                "- **Scope:** Single region, multi-zone. Protects against host, rack, and datacenter hardware failures.\n"
                "- **Mechanism:** Active/standby or active/active instances within the same region. Heartbeat monitors detect failure and trigger automated DNS/VIP failover.\n"
                "- **Metrics:** RTO < 60 seconds; RPO = 0 (using synchronous storage replication like Regional PD).\n"
                "- **Fatal Vulnerability:** Susceptible to regional destruction, network partition, and logical data corruption.\n\n"
                "### 2. Fault Tolerance (FT) Mechanics\n"
                "- **Scope:** Multi-zone or multi-region. Protects against any single component failure with zero user impact.\n"
                "- **Mechanism:** Distributed consensus protocols (e.g., TrueTime + Paxos in Cloud Spanner). Writes require majority quorum across independent voting zones/regions.\n"
                "- **Metrics:** RTO = 0 seconds; RPO = 0 seconds. Transparent to TCP connections and active client requests.\n"
                "- **Fatal Vulnerability:** Extreme financial cost (3x resources minimum) and write latency overhead dictated by speed-of-light inter-region round trips.\n\n"
                "### 3. Disaster Recovery (DR) Mechanics\n"
                "- **Scope:** Multi-region or hybrid cloud. Protects against regional destruction, prolonged cloud provider blackouts, or geopolitical disruption.\n"
                "- **Mechanism:** Cross-region asynchronous replication (Cloud SQL cross-region replica, GCS dual-region bucket) combined with automated Terraform orchestration.\n"
                "- **Metrics:** RTO = 15m to 4h; RPO = 5s to 15m (bounded by asynchronous replication lag).\n\n"
                "### 4. Backup & Archive Mechanics\n"
                "- **Scope:** Immutable out-of-band storage. Protects against human error, malicious deletion, ransomware, and software schema bugs.\n"
                "- **Mechanism:** Point-in-time snapshots, transaction write-ahead logs (WAL) for Point-In-Time Recovery (PITR), and WORM Object Retention Locks.\n"
                "- **Metrics:** RTO = Hours to Days (constrained by disk restore throughput); RPO = Snapshot frequency."
            ),
            "questions": [
                "Why does synchronous HA replication amplify the damage of an accidental `DROP TABLE` command compared to asynchronous backups?",
                "What is the physical network latency trade-off inherent in Spanner's multi-region Fault Tolerance versus Cloud SQL's regional High Availability?",
                "How does Cloud Storage Bucket Lock (WORM) fulfill regulatory compliance requirements that standard HA cannot address?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/ha-dr-backup",
            "reference_label": "Google Cloud Reliability Framework: Comparing HA, Fault Tolerance, DR, and Backup",
            "scenario": {
                "symptom": (
                    "A junior engineer executed an unindexed migration script on Brightloaf's primary production database, corrupting 45,000 order records. "
                    "The on-call operator immediately triggered the Cloud SQL HA failover button, expecting it to restore the uncorrupted state. "
                    "The standby node was activated, but all 45,000 records remained identically corrupted, prolonging the outage by 3 hours."
                ),
                "constraints": (
                    "Must restore order database to the exact state 60 seconds prior to the corrupted script execution, while preserving transactions completed before that timestamp."
                ),
                "evidence": (
                    "Cloud SQL HA logs show successful failover from `brightloaf-db-primary` to `brightloaf-db-standby` in 18.4 seconds. "
                    "However, because Regional Persistent Disk operates at block-level synchronous replication, the corrupt database blocks were replicated in lock-step."
                ),
                "diagnostic_steps": [
                    "Inspect Cloud SQL replication logs to demonstrate that block replication operated perfectly as designed.",
                    "Verify the exact timestamp of the errant `UPDATE` query via Cloud SQL query insights (04:12:30 UTC).",
                    "Query Cloud SQL Automated Backups and Transaction Logs to verify Point-In-Time Recovery (PITR) availability.",
                ],
                "root": (
                    "Conflating High Availability with Backup & Recovery: the operator treated an infrastructure failover mechanism (HA) as a data "
                    "recovery tool, failing to recognize that HA synchronously replicates all logical data corruption instantly."
                ),
                "fix": (
                    "Execute Point-In-Time Recovery (PITR) to restore a clone of the database to 04:11:00 UTC (1 minute prior to corruption), "
                    "reconcile pending orders from Cloud Pub/Sub, and update operational runbooks to prohibit HA failovers for logical data errors."
                ),
                "verify": (
                    "Verify cloned instance contains uncorrupted orders, execute data diff, point application to clone, and confirm zero missing orders."
                ),
                "residual": (
                    "PITR restoration to a new instance requires updating connection secrets or DNS CNAMEs, inducing a 12-minute maintenance window."
                ),
                "diagram": (
                    "Corrupt script runs",
                    "HA syncs corrupt blocks",
                    "Standby identically broken",
                    "Cloud SQL PITR clone",
                    "Data restored to T-60s"
                ),
                "facts": "Cloud SQL HA successfully failed over in 18.4s but preserved 100% of corrupt data blocks.",
                "inference": "High Availability guarantees infrastructure uptime, not data correctness.",
                "expected": "Point-In-Time Recovery restores data state to a known clean transaction log position."
            },
            "lab": {
                "name": "Point-In-Time Recovery and Four-Pillar Architecture Drill",
                "file": "day-084-topic-02-four-pillars.md",
                "goal": "Author an authoritative architecture decision record clarifying the Four Pillars of Resilience and author a Cloud SQL PITR recovery script.",
                "expected": "A structured Markdown document detailing the four pillars, risk boundaries, and runnable gcloud PITR restoration commands.",
                "mode": "tabletop analysis & command synthesis",
                "prereq": "Completion of Exercise 1.",
                "preflight": "Review Cloud SQL PITR documentation.",
                "steps": [
                    "Create the Four Pillars ADR and recovery runbook:\n\n```sh\ncat <<'EOF' > day-084-topic-02-four-pillars.md\n# Day 84: Architecture Decision Record — The Four Pillars of Resilience\n\n## 1. Classification Framework\n- **High Availability (HA):** Protects against zonal hardware failure. Handled via Cloud SQL Regional HA.\n- **Fault Tolerance (FT):** Protects against in-flight transaction loss. Handled via multi-region Spanner.\n- **Disaster Recovery (DR):** Protects against regional destruction. Handled via cross-region read replicas + Terraform.\n- **Backup & Retention:** Protects against corruption/ransomware. Handled via Cloud SQL PITR + GCS Bucket Lock.\n\n## 2. Point-In-Time Recovery (PITR) Runbook\nIn the event of logical data corruption, operators MUST NOT trigger HA failover. Execute PITR clone:\n\n```bash\n# 1. Identify corruption timestamp (e.g. 2026-09-28T04:12:30Z)\nTARGET_TIME=\"2026-09-28T04:11:00Z\"\n\n# 2. Restore database to a new instance at target timestamp\ngcloud sql instances clone brightloaf-db-primary brightloaf-db-recovered \\\n    --point-in-time=\"${TARGET_TIME}\" \\\n    --async\n\n# 3. Monitor clone operation\ngcloud sql operations list --instance=brightloaf-db-recovered\n\n# 4. Update Secret Manager database connection string once restored\ngcloud secrets versions add brightloaf-db-host \\\n    --data-file=<(gcloud sql instances describe brightloaf-db-recovered --format='value(ipAddresses[0].ipAddress)')\n```\nEOF\ncat day-084-topic-02-four-pillars.md\n```",
                    "Verify the PITR script specifies a timestamp prior to the corruption event.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists and contains accurate, production-grade GCP CLI commands for Point-In-Time database cloning and secret updates."
                ),
                "trouble": "Ensure transaction logging (`--enable-bin-log` or WAL archiving) is enabled prior to attempting PITR operations.",
                "cleanup": "Retain `day-084-topic-02-four-pillars.md` as an exit evidence artifact.",
                "accept": "Mastery of the Four Pillars of Resilience with validated PITR recovery runbook."
            }
        },
        {
            "key": "topic-03",
            "title": "Graceful degradation and load shedding under severe stress",
            "preview": (
                "A sudden viral marketing push spikes order volume by 800%. Unable to handle the load, the database queue overflows, "
                "causing web servers to run out of memory and crash; customers attempting to check out receive generic 500 errors instead of clean feedback."
            ),
            "overview": (
                "Graceful degradation and load shedding are defensive engineering patterns that ensure a system preserves its critical core transactions "
                "when total demand exceeds physical processing capacity. Under extreme stress, an unhardened distributed system exhibits catastrophic "
                "cascading failure: thread pools exhaust, database queues fill, latencies skyrocket past client timeouts, retries multiply the load, "
                "and every service collapses. In contrast, a gracefully degrading system categorizes requests into strict priority tiers (e.g., Critical Checkout, "
                "Standard Search, Low-Priority Recommendations). When capacity saturation is detected, the system proactively sheds non-essential load at the edge, "
                "disables resource-heavy UI features (serving cached or static fallbacks), and issues clean HTTP 429 / 503 responses, keeping the critical checkout "
                "pipeline responsive and profitable."
            ),
            "technical": (
                "Implementing graceful degradation requires a coordinated, multi-tier defense architecture:\n\n"
                "### 1. Request Priority Tiers\n"
                "- **Tier 1 (Critical):** Core revenue-generating paths (e.g., `POST /orders`, payment verification). Must NEVER be shed until total infrastructure collapse.\n"
                "- **Tier 2 (Standard):** User browsing and cart operations (e.g., `GET /catalog`, `POST /cart`). Throttled only under severe stress (>85% CPU saturation).\n"
                "- **Tier 3 (Sheddable):** Non-essential or auxiliary operations (e.g., product recommendations, real-time reviews, personalized discounts, telemetry). "
                "Immediately shed or bypassed when system enters overload mode.\n\n"
                "### 2. Edge Load Shedding Mechanics\n"
                "- **Cloud Armor Rate Limiting:** Enforce token-bucket throttling at the edge based on client IP or API key, rejecting excess requests before they consume "
                "expensive backend Compute or Database resources.\n"
                "- **Early HTTP 429/503 with `Retry-After`:** Reject excess requests early with an explicit backoff header, preventing desperate client retry loops from amplifying the storm.\n\n"
                "### 3. Application-Level Degradation Patterns\n"
                "- **Static Fallback:** If recommendation microservice latency exceeds 200ms, circuit breaker trips and returns a pre-cached JSON payload of top-10 global bestsellers.\n"
                "- **Feature Flag Shedding:** Dynamically disable expensive database queries (e.g., complex multi-table analytics aggregations) via centralized runtime flags.\n"
                "- **Asynchronous Queue Buffering:** Shift synchronous processing to Cloud Pub/Sub, returning HTTP 202 Accepted with a job status tracking URL."
            ),
            "questions": [
                "How does shedding load early at Cloud Armor reduce backend database CPU consumption compared to shedding inside application code?",
                "What is the role of the `Retry-After` HTTP header in preventing cascading retry storms from client applications?",
                "Why must the Critical Checkout path be isolated from the shared connection pool used by the Recommendation service?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability/graceful-degradation",
            "reference_label": "Google Cloud Architecture Framework: Handling overload and graceful degradation",
            "scenario": {
                "symptom": (
                    "During a flash sale, Brightloaf's web servers were overwhelmed by 12,000 requests/sec (4x normal peak). Compute Engine VM CPU hit 99%, "
                    "and the application began crashing due to Out-Of-Memory (OOM) errors. 100% of user checkouts failed for 28 minutes."
                ),
                "constraints": (
                    "Must preserve order placement for users already with active carts; cannot provision additional database read replicas in real-time due to 15-minute spin-up latency."
                ),
                "evidence": (
                    "Logs indicate 68% of backend CPU cycles were consumed calculating dynamic personalized recommendations and real-time bread baking status widgets, "
                    "starving the critical order submission threads."
                ),
                "diagnostic_steps": [
                    "Examine Cloud Profiler flame graphs to identify top CPU-consuming methods during the traffic spike.",
                    "Review Cloud Load Balancing backend latency broken down by URL path (`/api/v1/recommendations` vs `/api/v1/orders`).",
                    "Verify memory exhaustion triggers in Kubernetes events (`OOMKilled` on order-api pods).",
                ],
                "root": (
                    "Monolithic request handling lacked priority tiering: CPU-intensive recommendation queries competed for identical compute and thread resources "
                    "as revenue-critical order transactions, causing total system collapse when recommendations choked."
                ),
                "fix": (
                    "Implement a dynamic circuit breaker in Envoy / Cloud Run: under >80% CPU load, immediately return static empty arrays for recommendations, "
                    "and configure Cloud Armor rate limiting to prioritize `/orders` over all browsing traffic."
                ),
                "verify": (
                    "Simulate 15,000 req/sec load in staging; confirm recommendation traffic is shed with HTTP 200 static fallback, while checkout success rate remains >99.8%."
                ),
                "residual": (
                    "Personalized conversion rates temporarily dip by ~4% during active shedding, but 96% of order volume is successfully captured."
                ),
                "diagram": (
                    "12k req/sec surge",
                    "CPU starved by reco",
                    "OOM crash of checkout",
                    "Edge load shedding",
                    "99.8% checkout success"
                ),
                "facts": "68% of CPU was consumed by non-essential recommendation calculations, starving checkout.",
                "inference": "Equal resource allocation across features under load is an existential risk to core business survival.",
                "expected": "System proactively sheds Tier 3 requests to preserve 100% throughput for Tier 1 revenue transactions."
            },
            "lab": {
                "name": "Load Shedding and Request Priority Simulation Engine",
                "file": "day-084-topic-03-load-shedder.py",
                "goal": "Write and run a Python simulation modeling request prioritization and load shedding under 300% system overload.",
                "expected": "A runnable script demonstrating 100% survival of Critical transactions while non-essential traffic is shed with clean HTTP 429/503 responses.",
                "mode": "local script execution",
                "prereq": "Completion of Exercises 1 and 2.",
                "preflight": "Verify Python runtime and initialize simulation script.",
                "steps": [
                    "Create the load shedding simulator script:\n\n```sh\ncat <<'EOF' > day-084-topic-03-load-shedder.py\n#!/usr/bin/env python3\n\"\"\"Load Shedding and Priority Tier Simulation Engine.\"\"\"\nimport random\n\nCAPACITY_LIMIT = 500  # Max requests per second the backend can handle safely\nTOTAL_INCOMING = 1500  # 300% overload surge\n\n# Distribution: 20% Critical (Orders), 50% Standard (Browse), 30% Sheddable (Recommendations)\nrequests = []\nfor _ in range(TOTAL_INCOMING):\n    r_type = random.choices(['CRITICAL', 'STANDARD', 'SHEDDABLE'], weights=[0.2, 0.5, 0.3])[0]\n    requests.append(r_type)\n\nprocessed = {'CRITICAL': 0, 'STANDARD': 0, 'SHEDDABLE': 0}\nshed = {'CRITICAL': 0, 'STANDARD': 0, 'SHEDDABLE': 0}\n\ncurrent_load = 0\n\n# Priority Shedding Algorithm\nfor r in requests:\n    if current_load < CAPACITY_LIMIT:\n        processed[r] += 1\n        current_load += 1\n    else:\n        # System in overload: shed sheddable first, then standard\n        if r == 'SHEDDABLE':\n            shed[r] += 1\n        elif r == 'STANDARD':\n            # If we can drop sheddable to make room, we would, but here we shed standard\n            shed[r] += 1\n        elif r == 'CRITICAL':\n            # Critical requests pre-empt or force survival\n            processed[r] += 1\n            # Shed an already accepted sheddable if possible, or shed standard\n            if processed['SHEDDABLE'] > 0:\n                processed['SHEDDABLE'] -= 1\n                shed['SHEDDABLE'] += 1\n            elif processed['STANDARD'] > 0:\n                processed['STANDARD'] -= 1\n                shed['STANDARD'] += 1\n\nprint(f\"Simulation Results under {TOTAL_INCOMING} req/sec (Capacity: {CAPACITY_LIMIT} req/sec):\")\nprint(\"-\" * 70)\nprint(f\"{'Tier':<12} | {'Processed':<12} | {'Shed (HTTP 429)':<16} | {'Survival Rate':<15}\")\nprint(\"-\" * 70)\nfor tier in ['CRITICAL', 'STANDARD', 'SHEDDABLE']:\n    total = processed[tier] + shed[tier]\n    rate = (processed[tier] / total) * 100.0 if total > 0 else 0\n    print(f\"{tier:<12} | {processed[tier]:<12} | {shed[tier]:<16} | {rate:<15.1f}%\")\nEOF\npython3 day-084-topic-03-load-shedder.py\n```",
                    "Execute the script and verify that `CRITICAL` requests achieve ~100% survival rate while `SHEDDABLE` absorbs the majority of drops.",
                    "Review how this mechanism preserves core business invariants even when overall server capacity is exceeded by 300%.",
                    "Save the simulation script and output in your learning repository."
                ],
                "verification": (
                    "Script runs cleanly, displays formatted results, and demonstrates that Critical order transactions survive 300% traffic spikes."
                ),
                "trouble": "Ensure total processed requests across all tiers never exceeds the specified `CAPACITY_LIMIT`.",
                "cleanup": "Retain `day-084-topic-03-load-shedder.py` as an exit evidence artifact.",
                "accept": "Demonstrated practical mastery of graceful degradation and priority-based load shedding."
            }
        }
    ]
}
