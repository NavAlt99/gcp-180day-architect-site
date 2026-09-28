"""day_data_089.py — Exhaustive architecture data specification for Day 89.

Covers Messaging, DNS, and Application Health:
1. Messaging (Pub/Sub resource scope, regional endpoints, message storage policies, failure behavior, DLQs, idempotency).
2. DNS (Cloud DNS 100% SLA, routing policies: geolocation, weighted, failover, TTL propagation mechanics).
3. Application (Health check design: shallow vs deep, liveness vs readiness probes, graceful shutdown and SIGTERM draining).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 89

DATA = {
    "day": 89,
    "part1_intro": (
        "Day 89 analyzes the dynamic control plane and communication fabric connecting distributed microservices: asynchronous messaging, "
        "global name resolution, and workload health verification. Even the most robust regional infrastructure fails if asynchronous message "
        "pipelines drop events during regional partitions, if DNS caching traps client traffic at a failed datacenter, or if misconfigured "
        "health probes trigger cascading restarts across healthy compute nodes. Today's curriculum constructs defensible architectures for "
        "Google Cloud Pub/Sub (enforcing regional storage governance, dead-letter queuing, and exactly-once processing pipelines), evaluates "
        "Cloud DNS routing policies (geolocation, weighted, and health-checked failover) against recursive resolver TTL caching realities, "
        "and details application-tier resiliency mechanisms (shallow versus deep probes, readiness versus liveness isolation, and SIGTERM connection draining)."
    ),
    "exit_summary": (
        "Engineered an enterprise messaging and routing resiliency architecture: established Pub/Sub message storage constraints with automated "
        "dead-letter topic dead-lettering and client idempotency controls; designed Cloud DNS health-checked failover policies accounting for resolver TTL lag; "
        "authored an authoritative shallow-versus-deep health probe design document and verified Kubernetes/Cloud Run graceful termination lifecycles."
    ),
    "part2_intro": (
        "Distributed application survivability depends upon predictable decoupled interfaces and rapid, safe failure isolation. "
        "The architectural patterns below dissect Pub/Sub message retention mechanics, Cloud DNS Anycast routing behaviors, "
        "and probe design principles required to prevent self-inflicted systemic brownouts."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Layer</th>
      <th>Primary GCP Mechanism</th>
      <th>Resilience Guarantee &amp; Scope</th>
      <th>Key Failure Mode / Risk</th>
      <th>Architectural Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Messaging</strong></td>
      <td>Cloud Pub/Sub (Regional Endpoints + DLQ)</td>
      <td>At-least-once delivery, horizontal scale, regional persistence boundary</td>
      <td>Poison message crash loop; cross-border data residency violation</td>
      <td>Enforce <code>allowedPersistenceRegions</code>; configure Dead-Letter Topics (5 retries max) + exponential backoff</td>
    </tr>
    <tr>
      <td><strong>Resolution</strong></td>
      <td>Cloud DNS (Anycast Authoritative DNS)</td>
      <td>100% availability SLA; Geolocation, Weighted, and Failover routing</td>
      <td>Recursive resolver TTL caching ignores DNS failover during outages</td>
      <td>Configure 30s-60s TTL; integrate Cloud Monitoring health checks; deploy multi-region Anycast VIPs</td>
    </tr>
    <tr>
      <td><strong>Liveness Probe</strong></td>
      <td>Kubernetes / Compute Engine Liveness HTTP Probe</td>
      <td>Restarts deadlocked or crashed container runtimes automatically</td>
      <td>Cascading restart loop if probe depends on overloaded external DB</td>
      <td>Keep liveness probes shallow (local memory/event-loop check only, zero external network calls)</td>
    </tr>
    <tr>
      <td><strong>Readiness Probe</strong></td>
      <td>Kubernetes Readiness / Cloud Load Balancing Health Check</td>
      <td>Removes degraded instances from service endpoints without killing them</td>
      <td>Thundering herd if slow backends are prematurely saturated with traffic</td>
      <td>Combine shallow readiness with warm-up periods; apply client-side circuit breakers and load shedding</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 89: Resilient Service Health, Resolution, and Messaging Lifecycle",
        "desc": "End-to-end traffic flow showing DNS routing, load balancer probe separation, and asynchronous Pub/Sub decoupling.",
        "caption": "Figure 89.1: Tri-tier resilience model separating external DNS steering, local application probe lifecycles, and asynchronous decoupled messaging.",
        "nodes": [
            ("1. Cloud DNS Anycast", "Health-Checked Failover\\nShort TTL (30s) Steering"),
            ("2. Load Balancer Probes", "Shallow Health Checks\\nReadiness Endpoint Isolation"),
            ("3. Application Runtime", "SIGTERM Connection Drain\\nSeparate Liveness & Readiness"),
            ("4. Pub/Sub Messaging", "Regional Persistence Policy\\nDead-Letter Queue Isolation"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "**Messaging",
            "preview": (
                "A regional network degradation causes an unhandled payload exception in a payment ingestion service, resulting in "
                "continuous subscriber container crash loops that exhaust compute cluster memory and halt 45,000 pending customer orders."
            ),
            "overview": (
                "Google Cloud Pub/Sub provides horizontally scalable, globally available asynchronous messaging with at-least-once "
                "delivery guarantees. Understanding Pub/Sub's architectural boundaries is critical for enterprise reliability. By default, "
                "Pub/Sub topics have a global resource scope, automatically routing message publication and subscription across all Google Cloud "
                "regions. However, highly regulated workloads subject to data sovereignty mandates (e.g. GDPR, HIPAA) require strict message "
                "storage policies to restrict persisted data to explicitly allowed Google Cloud regions. Furthermore, subscriber resilience "
                "requires proactive handling of poison pills (malformed payloads that repeatedly trigger subscriber crashes) through Dead-Letter "
                "Topics (DLQs) and configurable retry delays, coupled with client-side deduplication logic to ensure idempotency."
            ),
            "technical": (
                "### 1. Pub/Sub Architectural Scope and Regional Endpoints\n"
                "- **Global Scope vs Regional Ingress:** Pub/Sub topic and subscription resource IDs exist globally within a project "
                "(`projects/{project}/topics/{topic}`). In standard mode, publishers send traffic to `pubsub.googleapis.com`, which uses Google's "
                "global Anycast network to terminate TLS at the nearest point of presence (PoP). For strict network isolation and compliance, "
                "clients can target regional service endpoints (e.g., `us-central1-pubsub.googleapis.com`), ensuring that network transit remains "
                "strictly within the designated geographic boundary.\n"
                "- **Message Storage Policies (`allowedPersistenceRegions`):** When publishers deliver messages, Pub/Sub persists data in at "
                "least two zones within an approved region. Organizations can enforce an organization policy constraint (`constraints/gcp.resourceLocations`) "
                "or define custom message storage policies on topics. If a publisher sends data while all allowed persistence regions are experiencing "
                "disruptions, Pub/Sub rejects the write with an error rather than violating data residency constraints.\n\n"
                "### 2. Failure Handling, Dead-Letter Topics, and Exponential Backoff\n"
                "- **Acknowledgment Deadlines:** When a subscriber pulls a message, it has a default 10-second ack deadline (configurable up to "
                "600 seconds). If the subscriber crashes or fails to call `acknowledge()` before the deadline expires, the message is redelivered. "
                "High-throughput consumers must use automatic deadline extension libraries or manually send `modifyAckDeadline` requests for long-running jobs.\n"
                "- **Dead-Letter Topics (DLQs):** A poison message (e.g., JSON syntax error, unhandled schema variation) will crash the subscriber, "
                "fail acknowledgment, get redelivered, and crash the subscriber indefinitely. By configuring a Dead-Letter Topic and setting "
                "`maxDeliveryAttempts` (typically 5), Pub/Sub automatically diverts persistently failing messages away from the primary subscription, "
                "allowing normal traffic to proceed without head-of-line blocking.\n"
                "- **Retry Policies:** Configure exponential backoff (e.g., minimum backoff 10s, maximum backoff 600s) on subscriptions to prevent "
                "overwhelming downstream microservices during service recovery.\n\n"
                "### 3. Idempotency and Ordering Guarantees\n"
                "- **At-Least-Once Delivery:** Pub/Sub guarantees that every published message is delivered at least once. Duplicate deliveries occur "
                "when network acknowledgments are dropped, during broker rebalancing, or when ack deadlines expire prematurely. Subscribers *must* "
                "be engineered for idempotency using a deduplication key (e.g., inserting message IDs into Redis with a TTL or leveraging relational "
                "unique constraints).\n"
                "- **Message Ordering:** When ordering keys are enabled, Pub/Sub delivers messages with the same ordering key strictly in the order "
                "they were published. However, if a message with an ordering key fails or redelivery is pending, all subsequent messages for that key "
                "are halted until the head message is acknowledged or routed to a DLQ."
            ),
            "questions": [
                "What happens when all regions listed in a Pub/Sub topic's message storage policy become unavailable?",
                "Why does ordering key enablement increase latency and head-of-line blocking risk during subscriber processing errors?",
                "How does dead-lettering prevent consumer starvation in high-volume asynchronous transaction pipelines?",
            ],
            "reference": "https://docs.cloud.google.com/pubsub/docs/overview",
            "reference_label": "Google Cloud Pub/Sub: Service architecture, message storage policies, and reliability semantics",
            "scenario": {
                "symptom": (
                    "Brightloaf's asynchronous checkout processing subscription experienced an unhandled null pointer exception caused by a corrupted "
                    "shopping cart payload. The subscriber worker crashed immediately upon reading the message, failed to acknowledge it, and "
                    "re-read the same message upon pod restart. Within 20 minutes, 120 worker pods entered CrashLoopBackOff, causing 45,000 valid "
                    "checkout messages to accumulate in the backlog and delaying order confirmations by 90 minutes."
                ),
                "constraints": (
                    "Must maintain 99.95% message processing SLA without dropping unprocessable messages, and prevent bad payloads from crashing subscriber pools."
                ),
                "evidence": (
                    "Cloud Monitoring showed subscription backlog `pubsub.googleapis.com/subscription/num_undelivered_messages` spiked from 12 to 45,820. "
                    "`pubsub.googleapis.com/subscription/dead_letter_message_count` was zero because no Dead-Letter Topic had been configured. "
                    "Kubernetes pod restarts exceeded 800 in 15 minutes."
                ),
                "diagnostic_steps": [
                    "Inspect subscriber application logs to capture the stack trace and offending message payload.",
                    "Verify subscription configuration to check if dead-lettering and retry policies are enabled.",
                    "Inspect Pub/Sub backlog metrics to identify processing throughput degradation and redelivery spikes.",
                ],
                "root": (
                    "The checkout subscription lacked a Dead-Letter Topic and retry policy, causing a single poisoned message to be redelivered "
                    "indefinitely, starving worker threads and crashing compute nodes in a fatal positive feedback loop."
                ),
                "fix": (
                    "Configure a Dead-Letter Topic (`checkout-poison-dlq`) with `maxDeliveryAttempts = 5` and a minimum retry backoff of 10s. "
                    "Implement a defensive JSON schema validator in the subscriber code that traps parsing errors, logs payload telemetry, and "
                    "sends negative acknowledgments or moves invalid payloads to quarantine."
                ),
                "verify": (
                    "Publish a synthetic malformed payload to the staging checkout topic; confirm the subscriber attempts processing 5 times with "
                    "exponential backoff, diverts the message to the DLQ, and continues processing downstream valid messages without pod restarts."
                ),
                "residual": (
                    "Messages in the Dead-Letter Topic expire after the topic retention period (default 7 days) if an operations alert is not triaged."
                ),
                "diagram": (
                    "Malformed message published",
                    "Infinite subscriber crash loop",
                    "45k messages stuck in backlog",
                    "Dead-Letter Topic configured",
                    "DLQ diversion after 5 retries"
                ),
                "facts": "A single corrupted payload crashed 120 subscriber pods repeatedly because no Dead-Letter Topic was configured.",
                "inference": "Without DLQ circuit breaking, poison messages convert localized data bugs into total pipeline outages.",
                "expected": "Poison messages divert to DLQ after 5 attempts; subscriber pods maintain 100% uptime for healthy backlog processing."
            },
            "lab": {
                "name": "Pub/Sub Dead-Letter Queue and Storage Policy Verification",
                "file": "day-089-topic-01-pubsub-resilience.md",
                "goal": "Author and verify a resilient Pub/Sub architecture defining regional message storage policies, DLQ dead-lettering, and subscriber idempotency.",
                "expected": "A comprehensive configuration document and runnable shell script simulating poison message diversion to a dead-letter topic.",
                "mode": "tabletop analysis & command synthesis",
                "prereq": "Understanding of asynchronous event-driven architectures.",
                "preflight": "Review Pub/Sub dead-letter documentation and schema validation patterns.",
                "steps": [
                    "Author the Pub/Sub resilience specification and execution runbook:\n\n```sh\ncat <<'EOF' > day-089-topic-01-pubsub-resilience.md\n# Day 89: Cloud Pub/Sub High Availability & Dead-Letter Architecture\n\n## 1. Storage & Ingress Boundary Specification\n- Topic Name: `projects/brightloaf-prod/topics/orders-v1`\n- Endpoint: `us-central1-pubsub.googleapis.com`\n- Message Storage Policy: `allowedPersistenceRegions: ['us-central1', 'us-east1']`\n- Encryption: Customer-Managed Encryption Keys (CMEK) dual-region ring\n\n## 2. Dead-Letter Topic (DLQ) Configuration Runbook\n\n### Step 1: Create Primary Topic and Dead-Letter Topic\n```bash\n# Create DLQ topic for quarantine\ngcloud pubsub topics create orders-dlq \\\n    --message-retention-duration=14d\n\n# Create DLQ subscription for ops audit\ngcloud pubsub subscriptions create orders-dlq-sub \\\n    --topic=orders-dlq \\\n    --ack-deadline=60\n\n# Create primary production topic with regional storage constraint\ngcloud pubsub topics create orders-v1 \\\n    --message-storage-policy-allowed-regions=us-central1,us-east1\n```\n\n### Step 2: Grant Pub/Sub Service Agent Forwarding Permissions\n```bash\n# Obtain project number\nPROJECT_NUMBER=$(gcloud projects describe $(gcloud config get-value project) --format='value(projectNumber)')\nPUBSUB_SERVICE_ACCOUNT=\"service-${PROJECT_NUMBER}@gcp-sa-pubsub.iam.gserviceaccount.com\"\n\n# Grant publisher role on DLQ to Pub/Sub system agent\ngcloud pubsub topics add-iam-policy-binding orders-dlq \\\n    --member=\"serviceAccount:${PUBSUB_SERVICE_ACCOUNT}\" \\\n    --role=\"roles/pubsub.publisher\"\n\n# Grant subscriber role on primary subscription to allow acking forwarded messages\ngcloud pubsub subscriptions add-iam-policy-binding orders-v1-sub \\\n    --member=\"serviceAccount:${PUBSUB_SERVICE_ACCOUNT}\" \\\n    --role=\"roles/pubsub.subscriber\"\n```\n\n### Step 3: Create Resilient Primary Subscription\n```bash\n# Bind subscription with DLQ and 5 max delivery attempts\ngcloud pubsub subscriptions create orders-v1-sub \\\n    --topic=orders-v1 \\\n    --ack-deadline=30 \\\n    --dead-letter-topic=orders-dlq \\\n    --max-delivery-attempts=5 \\\n    --min-retry-delay=10s \\\n    --max-retry-delay=300s\n```\n\n## 3. Client Idempotency Specification\nSubscribers implement a Redis-backed transactional deduplication gate:\n1. Extract message UUID and ordering key.\n2. Execute atomic Redis command: `SET order:{uuid}:processed 1 NX EX 86400`.\n3. If command returns null (key exists), log duplicate event and send immediate `ack()`.\n4. If command returns OK, execute database transaction and commit order.\nEOF\ncat day-089-topic-01-pubsub-resilience.md\n```",
                    "Verify the configuration explicitly defines `allowedPersistenceRegions` and dead-letter permissions.",
                    "Verify the subscriber idempotency pattern prevents duplicate database writes on redelivery.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains valid gcloud commands for DLQ creation with IAM bindings, and specifies idempotency controls."
                ),
                "trouble": "Ensure Pub/Sub Service Agent IAM permissions are assigned before binding the dead-letter topic to the subscription.",
                "cleanup": "Retain `day-089-topic-01-pubsub-resilience.md` as an exit evidence artifact.",
                "accept": "Completed Pub/Sub architecture document with verified DLQ and idempotency patterns."
            }
        },
        {
            "key": "topic-02",
            "title": "**DNS",
            "preview": (
                "A regional database outage forces network engineers to manually update Cloud DNS records, but branch offices continue sending "
                "requests to the failed region for 45 minutes because local corporate resolvers ignore standard TTL expirations."
            ),
            "overview": (
                "Google Cloud DNS provides authoritative domain name resolution backed by Google's global Anycast infrastructure, delivering "
                "a 100% availability service level agreement (SLA) for external public queries. While Cloud DNS authoritative servers never go down, "
                "the applications relying on DNS for multi-region steering and disaster recovery face major operational constraints. "
                "Traditional DNS failover relies on Time-To-Live (TTL) values; however, recursive DNS resolvers across public ISPs and corporate "
                "intranets frequently cache responses far longer than the configured TTL, creating unpredictable failover latency. To address this, "
                "Cloud DNS offers intelligent routing policies—including Geolocation routing, Weighted round-robin routing, and Health-Checked "
                "Failover routing—which automatically alter response records based on backend health without requiring manual operator intervention."
            ),
            "technical": (
                "### 1. Cloud DNS 100% Availability SLA Conditions\n"
                "- **Authoritative Architecture:** Cloud DNS is hosted across hundreds of Anycast edge locations globally. When a client queries "
                "`ns-cloud-*.googledomains.com`, BGP routes the query to the nearest healthy Google edge node, ensuring instant multi-path redundancy "
                "and an authoritative uptime SLA of 100%.\n"
                "- **SLA Scope and Exclusions:** The 100% SLA applies exclusively to the availability of the authoritative name server responding "
                "to valid DNS queries. It does *not* cover misconfigured DNS records, propagation latency caused by third-party recursive resolvers, "
                "or failures of the underlying target backend services.\n\n"
                "### 2. Cloud DNS Advanced Routing Policies\n"
                "- **Geolocation Routing:** Directs DNS queries to specific IP endpoints based on the geographic origin of the client's query "
                "(determined via EDNS Client Subnet - ECS). For example, European users resolve to `europe-west1` VIPs while North American users "
                "resolve to `us-central1` VIPs, reducing round-trip latency.\n"
                "- **Weighted Round-Robin (WRR):** Enables percentage-based traffic distribution across multiple IP targets. This is standard "
                "for blue/green environment transitions, regional capacity rebalancing, and canary releases (e.g., 95% traffic to `v1`, 5% to `v2`).\n"
                "- **Failover Routing with Health Checks:** Cloud DNS pairs with Cloud Monitoring regional health checks. Architects define a "
                "primary target (e.g. `us-central1` ALB VIP) and a backup target (e.g. `us-east1` ALB VIP). Cloud Monitoring probes the primary endpoint "
                "every 5–10 seconds. When health probes fail across consecutive intervals, Cloud DNS automatically ceases returning the primary IP "
                "and answers subsequent queries exclusively with the backup IP.\n\n"
                "### 3. DNS TTL Mechanics and Resolver Realities\n"
                "- **TTL Trade-Offs:** A low TTL (e.g., 30s or 60s) accelerates failover propagation across internet resolvers during disaster recovery. "
                "However, low TTL dramatically increases the total query volume against Cloud DNS and increases client lookup latency by bypassing "
                "local resolver caches.\n"
                "- **Recursive Resolver Non-Compliance:** Even with a 30s TTL, roughly 10%–25% of enterprise recursive resolvers enforce a minimum "
                "caching floor (often 5 to 15 minutes). Therefore, DNS failover alone cannot guarantee sub-minute RTO. For true sub-second failover, "
                "architects must deploy an Anycast Global External Application Load Balancer (single global VIP with multi-region backend services) "
                "rather than relying on DNS-based steering."
            ),
            "questions": [
                "Why does Cloud DNS's 100% availability SLA fail to protect clients from prolonged downtime during an unmitigated regional service failure?",
                "What is the difference in operational failover speed between DNS-based failover and Global Anycast Load Balancer failover?",
                "How does EDNS Client Subnet (ECS) influence Cloud DNS geolocation routing accuracy?",
            ],
            "reference": "https://docs.cloud.google.com/dns/docs/policies-overview",
            "reference_label": "Google Cloud DNS: Routing policies, health checks, and failover architecture",
            "scenario": {
                "symptom": (
                    "During a scheduled data center maintenance event, Brightloaf changed their primary web portal DNS A-record to point to the backup "
                    "datacenter. While internal engineers observed immediate redirection, 32% of retail store point-of-sale terminals continued "
                    "attempting to connect to the deactivated primary IP for over 40 minutes, causing point-of-sale checkout stalls."
                ),
                "constraints": (
                    "Must automate regional failover steering without requiring manual DNS zone edits during unannounced catastrophic outages."
                ),
                "evidence": (
                    "DNS zone inspection revealed the A-record had a TTL of 86400 (24 hours). Although engineers reduced the TTL to 60 seconds "
                    "immediately before changing the IP, external resolvers that had cached the record hours earlier retained the old IP until their "
                    "original 24-hour cache counter expired."
                ),
                "diagnostic_steps": [
                    "Query authoritative name servers directly using dig with target @ns-cloud-a1.googledomains.com api.brightloaf.com to verify authoritative answer.",
                    "Query public recursive resolvers (Google 8.8.8.8, Cloudflare 1.1.1.1) to compare TTL countdowns.",
                    "Audit past DNS record modifications and historical TTL settings in Cloud DNS change logs.",
                ],
                "root": (
                    "The DNS record TTL was maintained at 86,400 seconds until the moment of failover; DNS TTLs must be lowered days in advance of "
                    "planned changes, or maintained permanently at 60s with automated health-checked routing policies."
                ),
                "fix": (
                    "Transition the DNS zone to a Cloud DNS Failover Routing Policy with a permanent 30-second TTL, tied to an automated Cloud Monitoring "
                    "health check probing the primary load balancer VIP. Deploy Global External Application Load Balancing across regions as the primary "
                    "steering mechanism, reserving DNS failover for catastrophic global control-plane events."
                ),
                "verify": (
                    "Simulate primary VIP failure in staging by blocking health-check probe ports; verify Cloud DNS automatically switches answer "
                    "records to the backup VIP within 60 seconds across all public recursive test resolvers."
                ),
                "residual": (
                    "A 30-second TTL increases external DNS query billing volume and slightly increases first-hit client lookup latency."
                ),
                "diagram": (
                    "24h TTL record cached globally",
                    "Manual DNS IP change applied",
                    "Retail terminals cached on old IP",
                    "Cloud DNS health-checked policy",
                    "Automated switch in 30s TTL window"
                ),
                "facts": "Point-of-sale terminals failed for 40 minutes because the DNS A-record TTL was 86,400 seconds at the time of change.",
                "inference": "DNS cannot serve as an emergency failover mechanism unless TTLs are consistently short and steering is automated.",
                "expected": "Cloud DNS Failover Policy automatically pivots client traffic within 60 seconds of health-check failure."
            },
            "lab": {
                "name": "Cloud DNS Health-Checked Failover Routing Policy Synthesis",
                "file": "day-089-topic-02-dns-routing.md",
                "goal": "Author and verify an automated Cloud DNS Failover Routing Policy with health checks and short TTL steering.",
                "expected": "A comprehensive configuration guide with exact gcloud commands establishing health checks and failover record sets.",
                "mode": "tabletop analysis & command synthesis",
                "prereq": "Understanding of DNS hierarchy and Anycast networking.",
                "preflight": "Review Cloud DNS routing policies documentation.",
                "steps": [
                    "Author the DNS failover routing architecture and configuration runbook:\n\n```sh\ncat <<'EOF' > day-089-topic-02-dns-routing.md\n# Day 89: Cloud DNS Health-Checked Failover Policy Architecture\n\n## 1. Architectural Strategy\nTo minimize failover latency while maintaining resilience against ISP caching defects:\n1. Maintain a standard TTL of **60 seconds** on all user-facing apex and sub-domain routing records.\n2. Configure a Cloud Monitoring HTTP health check targeting `/healthz/shallow` on the primary regional load balancer.\n3. Configure Cloud DNS **Failover Routing Policy** binding Primary VIP (`us-central1`) and Backup VIP (`us-east1`).\n\n## 2. Configuration & Execution Commands\n\n### Step 1: Create Regional Cloud Monitoring Health Check\n```bash\n# Authorize health-check probe against primary regional load balancer\ngcloud compute health-checks create http primary-regional-hc \\\n    --region=us-central1 \\\n    --port=80 \\\n    --request-path=\"/healthz/shallow\" \\\n    --check-interval=5s \\\n    --timeout=3s \\\n    --unhealthy-threshold=2 \\\n    --healthy-threshold=1\n```\n\n### Step 2: Create Managed DNS Zone (if absent)\n```bash\n# Verify or create production public DNS zone\ngcloud dns managed-zones create brightloaf-zone \\\n    --dns-name=\"brightloaf.com.\" \\\n    --description=\"Brightloaf Production Anycast Zone\" \\\n    --dnssec-state=on\n```\n\n### Step 3: Deploy Health-Checked Failover Record Set\n```bash\n# Configure Cloud DNS failover routing policy\ngcloud dns record-sets create api.brightloaf.com. \\\n    --zone=brightloaf-zone \\\n    --type=A \\\n    --ttl=60 \\\n    --routing-policy-type=FAILOVER \\\n    --routing-policy-data=\"primary=34.102.10.1,backup=34.107.20.2\" \\\n    --health-check=primary-regional-hc\n```\n\n## 3. Resolver TTL Recovery Timeline Analysis\n| Elapsed Time | Authoritative State | ISP Recursive Resolver State | Client Traffic Distribution |\n| :--- | :--- | :--- | :--- |\n| **T+00s** | Primary VIP fails | Returning Primary VIP (cached) | 100% Primary (Errors occur) |\n| **T+10s** | Health check marks Primary DOWN | Returning Primary VIP (cached) | 100% Primary |\n| **T+15s** | Cloud DNS switches answer to Backup | Returning Primary VIP (cached) | 100% Primary |\n| **T+45s** | Cloud DNS serving Backup VIP | Compliant resolvers expire TTL | 60% Backup / 40% Primary |\n| **T+75s** | Cloud DNS serving Backup VIP | 95% resolvers updated to Backup | 95% Backup / 5% Primary |\n| **T+300s** | Cloud DNS serving Backup VIP | Non-compliant resolvers expire | 100% Backup |\nEOF\ncat day-089-topic-02-dns-routing.md\n```",
                    "Verify the configuration specifies exact gcloud commands for failover routing policies and health checks.",
                    "Verify the resolver TTL recovery timeline models realistic caching decay across ISP resolvers.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, includes valid gcloud DNS routing commands, and details an end-to-end DNS failover recovery timeline."
                ),
                "trouble": "Ensure Cloud Monitoring health check is created in the same project and region as the primary compute backend.",
                "cleanup": "Retain `day-089-topic-02-dns-routing.md` as an exit evidence artifact.",
                "accept": "Completed Cloud DNS health-checked routing specification and resolver latency analysis."
            }
        },
        {
            "key": "topic-03",
            "title": "**Application",
            "preview": (
                "A transient 5-second database lock causes an application's deep health check endpoint to fail, triggering Google Cloud Load Balancing "
                "to mark all 80 backend instances unhealthy simultaneously and plunging the entire site into a total 502 Bad Gateway outage."
            ),
            "overview": (
                "Application health check design dictates how cloud orchestrators and load balancers detect, isolate, and recover from software "
                "faults. A fundamental architectural trap in microservice design is confounding shallow health checks with deep health checks. "
                "A **shallow health check** verifies only the immediate process's responsiveness (e.g., HTTP listener alive, event loop running, "
                "free local memory). A **deep health check** verifies the availability of upstream and downstream dependencies (e.g., database connection "
                "pools, Redis caches, third-party payment gateways). In load balancing and orchestrator restart loops, deep health checks introduce "
                "catastrophic failure cascades. Furthermore, resilient applications must clearly separate **readiness probes** (which control whether "
                "an instance receives user traffic) from **liveness probes** (which trigger process termination and restart), and must implement "
                "strict **graceful shutdown** routines to drain in-flight connections when SIGTERM signals are issued."
            ),
            "technical": (
                "### 1. Shallow vs Deep Health Checks: Mechanics and Blast Radius\n"
                "- **The Cascading Outage Anti-Pattern:** Consider a service with 100 instances behind a load balancer. If the health check "
                "probes `/healthz/deep` which runs `SELECT 1 FROM database;`, what happens if the database encounters connection pool exhaustion? "
                "All 100 instances fail their health check at the exact same moment. The load balancer concludes that zero instances are healthy and "
                "drops all backend routes, converting a minor database slowdown into a complete total application outage.\n"
                "- **Architectural Rule of Thumb:**\n"
                "  1. **Load Balancer Health Checks:** Must *always* be shallow. They answer: *'Can this specific compute instance parse HTTP requests "
                "and accept new socket connections?'*\n"
                "  2. **Internal Dependency Health Checks:** Deep health checks should be reserved for synthetic monitoring, operational dashboards, "
                "and administrative triage tools (`/healthz/deep`), protected by authentication and decoupled from automatic traffic routing.\n\n"
                "### 2. Kubernetes and Container Probe Taxonomy\n"
                "- **Startup Probe:** Protects slow-starting legacy applications during container initialization. Disables liveness and readiness checks "
                "until the startup probe succeeds, preventing premature process termination.\n"
                "- **Liveness Probe:** Answers: *'Is the process deadlocked or fatally corrupted?'* If a liveness probe fails consecutively, kubelet "
                "kills the container and restarts it according to its restart policy. Liveness probes must be extremely lightweight and should "
                "*never* check external network resources.\n"
                "- **Readiness Probe:** Answers: *'Is the application currently ready to accept user requests?'* If a readiness probe fails (e.g., during "
                "local cache warming or temporary CPU spikes), kubelet removes the Pod IP from the Kubernetes Service endpoints. The container is *not* "
                "killed, preserving its state while traffic is diverted to other healthy pods.\n\n"
                "### 3. Graceful Shutdown and Connection Draining Mechanics\n"
                "- **The Termination Sequence:**\n"
                "  1. Orchestrator (Kubernetes/MIG) sends `SIGTERM` to the container process.\n"
                "  2. Endpoint controller updates IP tables and Load Balancer begins backend draining.\n"
                "  3. Application traps `SIGTERM`: stops accepting *new* connections, marks readiness endpoint as unhealthy (`503 Service Unavailable`), "
                "and allows existing in-flight HTTP requests to complete.\n"
                "  4. After in-flight requests finish or the drain timeout elapses (e.g., 30s), the application closes database pools and exits cleanly (exit code 0).\n"
                "  5. If the application fails to terminate within `terminationGracePeriodSeconds` (e.g., 45s), the kernel sends `SIGKILL`."
            ),
            "questions": [
                "Why does configuring a deep health check on a Cloud Load Balancer backend service violate fault-isolation boundaries?",
                "What is the difference in operational outcome when a liveness probe fails versus when a readiness probe fails?",
                "Why must the application's graceful shutdown timeout be coordinated with the load balancer's backend connection drain timeout?",
            ],
            "reference": "https://docs.cloud.google.com/load-balancing/docs/health-check-concepts",
            "reference_label": "Google Cloud Load Balancing: Health check architecture, probe types, and draining behavior",
            "scenario": {
                "symptom": (
                    "During a midday traffic surge, Brightloaf's catalog service experienced a transient 10-second database connection pool saturation. "
                    "Within 15 seconds, the Cloud Load Balancer marked 100% of catalog instances unhealthy, returning HTTP 502 Bad Gateway to all "
                    "shoppers across Europe and North America for 22 minutes."
                ),
                "constraints": (
                    "Must maintain service availability during partial dependency degradations and isolate backend container restarts from transient external latency."
                ),
                "evidence": (
                    "Load balancer logs revealed all 60 instances failed health checks concurrently at 14:02:10. The health check was configured to probe "
                    "`/healthz`, which executed a complex SQL query across three tables. Application CPU and memory on the VM instances remained under 35%."
                ),
                "diagnostic_steps": [
                    "Inspect Cloud Load Balancer backend service health metrics (`loadbalancing.googleapis.com/backend_status`).",
                    "Review application health check handler source code to identify external network and database dependencies.",
                    "Correlate database slow-query logs and connection pool telemetry with the exact timestamp of load balancer health check failures.",
                ],
                "root": (
                    "Architectural anti-pattern: the load balancer health check was coupled to a deep database query rather than a shallow local "
                    "process probe. When the database slowed down, healthy compute instances were prematurely evicted from the load balancer pool."
                ),
                "fix": (
                    "Split health check endpoints into `/healthz/shallow` (validates HTTP listener and local memory; zero DB calls) and `/healthz/deep` "
                    "(reports dependency status for monitoring only). Reconfigure Cloud Load Balancing to probe `/healthz/shallow`. Configure Kubernetes "
                    "readiness probes to handle soft load shedding and liveness probes to monitor process runloops."
                ),
                "verify": (
                    "Simulate database connection pool exhaustion in staging; confirm that `/healthz/deep` returns 503 while `/healthz/shallow` returns "
                    "200 OK. Confirm Cloud Load Balancing continues routing traffic without dropping instances from the backend pool."
                ),
                "residual": (
                    "Shallow health checks do not detect if a container has lost database connectivity; application code must return clean HTTP 503 "
                    "or degraded responses for requests requiring unavailable dependencies."
                ),
                "diagram": (
                    "Database pool saturated",
                    "Deep probe fails on all 60 VMs",
                    "Load balancer drops 100% backends",
                    "Shallow probe deployed (/shallow)",
                    "Load balancer maintains healthy pool"
                ),
                "facts": "All 60 catalog VMs were declared dead by the load balancer because `/healthz` queried the database during a transient lock.",
                "inference": "Deep health checks on load balancers transform transient downstream blips into catastrophic total compute evictions.",
                "expected": "Load balancer probes `/healthz/shallow`, keeping VMs in service while application circuit-breakers shed load gracefully."
            },
            "lab": {
                "name": "Application Health Check Architecture & Graceful Shutdown Rehearsal",
                "file": "day-089-topic-03-app-health.md",
                "goal": "Design an enterprise health check decision matrix and write a production-ready Node.js/Go graceful shutdown implementation with probe separation.",
                "expected": "A comprehensive Markdown document containing the shallow-vs-deep decision matrix and executable code demonstrating SIGTERM handling.",
                "mode": "tabletop analysis & code synthesis",
                "prereq": "Understanding of HTTP semantics and container lifecycles.",
                "preflight": "Review Kubernetes probe concepts and load balancer draining parameters.",
                "steps": [
                    "Author the health check architecture document and implementation script:\n\n```sh\ncat <<'EOF' > day-089-topic-03-app-health.md\n# Day 89: Application Health Check Architecture & Graceful Termination\n\n## 1. Health Probe Architectural Decision Matrix\n\n| Probe Type | Endpoint | Target Consumer | Trigger Action on Failure | Permitted Dependencies |\n| :--- | :--- | :--- | :--- | :--- |\n| **LB Health Check** | `/healthz/shallow` | Cloud Load Balancer | Evict instance from LB routing | **None** (Process local loopback only) |\n| **K8s Startup** | `/healthz/startup` | Kubelet Orchestrator | Pause other probes; kill after timeout | Local disk/cache warm-up |\n| **K8s Liveness** | `/healthz/liveness` | Kubelet Orchestrator | **Restart container** (SIGKILL) | Internal thread loop / memory sanity |\n| **K8s Readiness** | `/healthz/readiness`| Kubelet Orchestrator | Remove Pod from Service endpoints | Local circuit-breaker state |\n| **Synthetic Deep** | `/healthz/deep` | SRE Dashboard / Monitoring | Alert on-call pager; zero auto-kill | Cloud SQL, Redis, Pub/Sub |\n\n## 2. Production Graceful Shutdown Implementation (Node.js/Express)\n```javascript\nconst express = require('express');\nconst http = require('http');\n\nconst app = express();\nlet isShuttingDown = false;\n\n// Shallow Health Check: For Cloud Load Balancer\napp.get('/healthz/shallow', (req, res) => {\n  if (isShuttingDown) {\n    return res.status(503).send('Server is shutting down');\n  }\n  res.status(200).send('OK');\n});\n\n// Readiness Probe: For Kubernetes Endpoint Controller\napp.get('/healthz/readiness', (req, res) => {\n  if (isShuttingDown) {\n    return res.status(503).send('Not Ready: Draining');\n  }\n  res.status(200).send('READY');\n});\n\n// Liveness Probe: For Kubelet Container Restart\napp.get('/healthz/liveness', (req, res) => {\n  // Must NEVER check external DB or cache\n  res.status(200).send('ALIVE');\n});\n\nconst server = http.createServer(app);\nserver.listen(8080, () => console.log('Service listening on :8080'));\n\n// Graceful Shutdown Handler\nfunction handleSignal(signal) {\n  console.log(`Received ${signal}. Initiating graceful connection drain...`);\n  isShuttingDown = true; // Flips shallow & readiness to 503\n\n  // Wait 5 seconds for Cloud Load Balancer to remove IP from endpoint table\n  setTimeout(() => {\n    server.close(() => {\n      console.log('All in-flight HTTP connections drained. Closing database pools...');\n      // Close DB connections here...\n      process.exit(0);\n    });\n  }, 5000);\n\n  // Hard kill if graceful shutdown hangs\n  setTimeout(() => {\n    console.error('Graceful drain exceeded timeout! Forcing shutdown.');\n    process.exit(1);\n  }, 25000);\n}\n\nprocess.on('SIGTERM', () => handleSignal('SIGTERM'));\nprocess.on('SIGINT', () => handleSignal('SIGINT'));\n```\n\n## 3. Kubernetes Pod Lifecycle Alignment\n```yaml\nspec:\n  terminationGracePeriodSeconds: 30\n  containers:\n  - name: api-server\n    image: gcr.io/brightloaf-prod/api:v1\n    lifecycle:\n      preStop:\n        exec:\n          command: [\"/bin/sh\", \"-c\", \"sleep 5\"]\n    livenessProbe:\n      httpGet:\n        path: /healthz/liveness\n        port: 8080\n      initialDelaySeconds: 5\n      periodSeconds: 10\n    readinessProbe:\n      httpGet:\n        path: /healthz/readiness\n        port: 8080\n      initialDelaySeconds: 2\n      periodSeconds: 5\n```\nEOF\ncat day-089-topic-03-app-health.md\n```",
                    "Verify the decision matrix clearly separates load balancer health checks from internal deep monitoring.",
                    "Verify the graceful shutdown code handles SIGTERM with a 5-second drain window before closing database connections.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains a comprehensive health check decision matrix, and provides working graceful shutdown code."
                ),
                "trouble": "Ensure `terminationGracePeriodSeconds` in Kubernetes exceeds the sum of `sleep 5` preStop hook and the application drain timeout.",
                "cleanup": "Retain `day-089-topic-03-app-health.md` as an exit evidence artifact.",
                "accept": "Completed health check architectural matrix and validated graceful shutdown lifecycle implementation."
            }
        }
    ]
}
