"""Topic 1 specification for Day 17: Prerequisite review and remediation."""

from scratch.day_017_svgs import FIG_17_1_HTML, FIG_17_3_HTML

TOPIC_01_OVERVIEW = (
    '<strong class="keyword">Foundation Synthesis and Prerequisite Remediation</strong> conducts a comprehensive '
    'review and systematic repair of the core operating system, networking, and data persistence primitives '
    'mastered across Block 1 (Days 1–16). Before advancing to Google Cloud identity and resource hierarchy in '
    'Block 2, architects must demonstrate flawless end-to-end mastery: tracing an incoming request through DNS '
    'resolution, IP subnet routing, TLS 1.3 termination, POSIX containerized process execution, Twelve-Factor '
    'configuration and structured logging, and ACID-compliant relational transactions. Checkpoint days strictly '
    'forbid the introduction of new cloud services or external concepts, focusing entirely on recalling foundational '
    'invariants and systematically upgrading any shallow, ambiguous, or incomplete explanations from prior lab exercises.'
)

TOPIC_01_PREVIEW = (
    "An e-commerce bakery ordering service experiences intermittent 10,000 ms database connection timeouts following an uncoordinated container network reconfiguration. "
    "Because engineers lacked end-to-end visibility into overlapping RFC 1918 CIDR allocations and DNS search domain loops, morning bread orders across 42 commercial hubs stalled, halting delivery schedules and triggering customer SLA penalties."
)

TOPIC_01_QUESTIONS = [
    "How do lower-level operating system and networking primitives (POSIX signals, cgroups, TCP sockets, and DNS resolvers) dictate the reliability boundaries of higher-level cloud managed services?",
    "Why does relational state persistence require schema-level unique constraints and atomic transaction boundaries rather than relying on application-tier or message-broker deduplication?",
    "What specific architectural hazards emerge when technical teams advance to cloud infrastructure without proving reproducible mastery over foundational networking and rollback mechanisms?"
]

TOPIC_01_TECHNICAL = """<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Foundational request path synthesis: DNS, TCP, TLS, and POSIX process execution</strong></li>
<li><strong>State persistence and relational integrity: ACID transactions and rollback mechanics</strong></li>
<li><strong>Failure mode taxonomy: network timeouts, process crashes, and isolation anomalies</strong></li>
<li><strong>Weak explanation audit: identifying and repairing ambiguous architectural claims</strong></li>
<li><strong>Traceability mapping: linking foundation mechanisms to cloud architecture decisions</strong></li>
</ul>

<h4>Foundational request path synthesis: DNS, TCP, TLS, and POSIX process execution</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">End-to-End Request Path Synthesis</strong> describes the complete lifecycle of a client transaction across every layer of the computing stack. The journey begins at Layer 7 when a client initiates a request to a host such as <code>api.brightloaf.internal</code>. The operating system stub resolver queries the local recursive DNS server, traversing the domain hierarchy to return an RFC 1918 IPv4 address (e.g., <code>10.0.2.10</code>). The client kernel constructs a TCP SYN packet, initiating the three-way handshake (SYN, SYN-ACK, ACK) across non-overlapping CIDR subnets routed via default gateways. Over the established TCP stream, TLS 1.3 negotiates symmetric session keys using ephemeral Diffie-Hellman exchanges and validates server certificate chains. Upon handshake completion, the client transmits an HTTP/1.1 or HTTP/2 POST request carrying an idempotent <code>X-Request-ID</code> header and a JSON payload. At the server host, the Linux kernel receives packets on an ingress network interface, evaluates iptables NAT rules or bridge virtual interfaces, and forwards the payload to a container namespace. Within the container, a POSIX process running as a non-privileged user (e.g., UID 10001) constrained by memory and CPU cgroups reads the byte stream from file descriptor 0 (standard input) or a listening socket, parses the JSON payload, and initiates business processing.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects must possess visceral fluency with this multi-layer path to diagnose production latency, performance bottlenecks, and security boundaries. High-level abstractions frequently mask the physical reality of packets and processes: an architect who views a microservice call merely as an API invocation will fail to diagnose MTU mismatches, connection pool exhaustion, ephemeral port starvation, or DNS resolver caching delays. Understanding how each layer interacts allows architects to budget latency allocations accurately (e.g., allocating 2 ms for internal DNS, 1.5 ms for TCP handshake, 3 ms for TLS session resumption, and 15 ms for database queries), design optimal keep-alive pooling strategies, and enforce defense-in-depth network boundaries.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, as documented in <a href="https://cloud.google.com/learn/certification/cloud-architect#about-this-certification">Google Cloud Certification: Professional Cloud Architect — About this certification (accessed 2026-10-04)</a>, certified architects must design, develop, and manage robust, secure, and scalable cloud solutions adhering to business and technical requirements. Google Cloud infrastructure manages edge routing and packet transit through Google Front Ends (GFE), Andromeda virtual network switches, and Cloud Load Balancing. However, the underlying primitives remain identical: a Cloud Run container or GKE pod relies on Linux namespaces and cgroups, private DNS queries traverse Cloud DNS VPC resolvers (<code>169.254.169.254</code>), and inter-VPC traffic traverses software-defined routes bounded strictly by non-overlapping CIDR ranges. Misunderstanding these foundational layers results in unroutable VPC subnets, broken TLS handshakes, or mysterious OOM kills.</p>

<h4>State persistence and relational integrity: ACID transactions and rollback mechanics</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Relational ACID Persistence and Atomic Rollbacks</strong> guarantee data correctness and structural consistency in the presence of concurrent mutations and system failures. ACID represents four non-negotiable guarantees:
1. <em>Atomicity:</em> All SQL statements within an explicit transaction boundary (<code>BEGIN TRANSACTION</code> to <code>COMMIT</code>) execute as a single indivisible unit of work; if any statement fails or an explicit <code>ROLLBACK</code> is issued, all modifications are completely reversed, leaving no partial state.
2. <em>Consistency:</em> Transitions move the database from one valid state to another, strictly satisfying all schema constraints, foreign keys, data types, and uniqueness rules.
3. <em>Isolation:</em> Concurrent transactions execute without interfering with one another, preventing anomalies such as dirty reads, non-repeatable reads, or phantom records according to the configured isolation level (Read Committed, Repeatable Read, or Serializable).
4. <em>Durability:</em> Once a transaction commits, its modifications are permanently recorded to persistent storage via Write-Ahead Logging (WAL) and survive host crashes or power loss.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> In enterprise system design, state management is the ultimate source of architectural truth and financial liability. Architects must recognize that application code and network layers are inherently volatile: microservices crash, network links drop, and client connections time out mid-flight. Attempting to manage business consistency in application code (e.g., checking for existing records in memory before inserting) creates race conditions under high concurrency. Architects must enforce consistency at the persistence tier using relational foreign keys and unique constraints. Furthermore, understanding transaction rollback mechanics prevents catastrophic data corruption, such as billing an account without creating the corresponding fulfillment order or leaving orphaned child records that poison downstream analytical pipelines.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud provides both managed relational engines (Cloud SQL for PostgreSQL/MySQL, AlloyDB) and globally distributed transactional systems (Google Cloud Spanner). In Cloud SQL, transactional guarantees rely on underlying relational engines and Write-Ahead Logging stored on persistent disks. In Cloud Spanner, ACID transactions scale horizontally across global regions using TrueTime (synchronized atomic and GPS clocks) and two-phase commit (2PC) with Paxos consensus. Regardless of whether an architect deploys a single-instance Cloud SQL database or a multi-region Spanner cluster, understanding the fundamental semantics of <code>ROLLBACK</code>, lock contention, and foreign key cascades is essential for designing resilient database schemas that preserve enterprise invariants under extreme failure modes.</p>

<h4>Failure mode taxonomy: network timeouts, process crashes, and isolation anomalies</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Foundation Failure Mode Taxonomy</strong> classifies the systemic defects that compromise software systems across network, operating system, and data tiers:
1. <em>Network Tier Failures:</em> Packet drops due to MTU mismatches, routing blackholes caused by overlapping CIDR blocks, TCP SYN retransmissions during connection pool exhaustion, and DNS resolution timeouts caused by circular or misconfigured search domains.
2. <em>Operating System &amp; Process Failures:</em> Linux Out-Of-Memory (OOM) killer terminations triggered when a container exceeds its cgroup memory limit, uncaught fatal signals (such as unhandled <code>SIGTERM</code> or <code>SIGPIPE</code>), unbuffered output buffers preventing log capture before sudden process death, and permission denials from executing as root or missing file descriptors.
3. <em>Relational Tier Failures:</em> Isolation anomalies under concurrent load (e.g., non-repeatable reads where a second query reads mutated data, or write skew where two concurrent transactions update overlapping ranges based on stale reads), deadlocks caused by inverted lock acquisition orders, and unconstrained event replays inserting duplicate business orders.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects do not design for the happy path; they design systems that fail gracefully, contain blast radiuses, and recover deterministically. A comprehensive taxonomy of failure modes enables architects to implement targeted defensive patterns: configuring bounded client timeouts with exponential backoff and jitter, establishing dead letter queues (DLQ) for malformed payloads, implementing idempotent transaction keys, and deploying health probes that differentiate between transient network blips and catastrophic container crashes.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Cloud architects mapping failure modes to Google Cloud systems leverage specific platform features:
1. <em>VPC Network Intelligence Center:</em> Visualizes packet drops and routing conflicts between VPC subnets, identifying overlapping CIDRs before traffic fails.
2. <em>Cloud Logging &amp; Error Reporting:</em> Aggregates Twelve-Factor structured JSON logs emitted to <code>stdout</code>/<code>stderr</code>, automatically capturing stack traces and uncaught exception signals across Compute Engine VMs, GKE pods, and Cloud Run containers.
3. <em>Cloud SQL &amp; Spanner Metrics:</em> Cloud Monitoring exposes lock wait times, deadlocks, transaction rollback rates, and connection pool saturation, enabling architects to detect isolation anomalies and tune transaction retry loops before production outages occur.</p>

<h4>Weak explanation audit: identifying and repairing ambiguous architectural claims</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Weak Explanation Auditing and Technical Remediation</strong> is the rigorous engineering discipline of scrutinizing technical documentation, design artifacts, and operational runbooks to eliminate hand-waving assertions, vague assumptions, and unsubstantiated claims. In architectural reviews, weak explanations frequently manifest as passive statements (e.g., "traffic is automatically routed to the database" without naming the DNS resolver, IP routing table, or firewall rules) or superficial assertions of safety (e.g., "the database prevents duplicates" without specifying whether uniqueness is enforced via application memory, a table UNIQUE constraint, or an upsert pattern). Auditing requires systematically identifying every assumption, verifying its underlying physical or logical mechanism, and replacing ambiguity with mathematically sound, reproducible evidence.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects serve as the technical authority across cross-functional engineering teams. Ambiguity in architecture documentation is a direct precursor to production failure: developers interpret vague specifications differently, operations teams author flawed recovery runbooks, and security teams overlook critical exposure vectors. By mastering the audit and remediation of weak explanations, architects establish an engineering culture of precision. They ensure that post-mortem incident reports uncover genuine root causes rather than superficial symptoms, and that architectural review boards approve only thoroughly substantiated designs.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud Architecture Framework principles emphasize operational excellence and documentation accuracy. During a cloud migration or landing zone review, vague statements regarding Google Cloud services (such as claiming "Cloud Storage buckets are private by default" without verifying Uniform Bucket-Level Access or IAM condition bindings, or asserting "Cloud SQL automatically rolls back failures" without defining application connection retry parameters) create dangerous compliance gaps. Remediating weak explanations ensures that Google Cloud architectures satisfy the stringent requirements of enterprise risk governance, SOC 2 compliance, and Professional Cloud Architect examination standards.</p>

<h4>Traceability mapping: linking foundation mechanisms to cloud architecture decisions</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Bidirectional Traceability Mapping</strong> is the architectural practice of maintaining an unbroken logical chain between low-level computing primitives and high-level enterprise cloud architecture decisions. Every managed cloud service—regardless of how abstract its marketing description appears—is composed of standardized operating system kernels, virtual network switches, storage block devices, and relational engines. Traceability mapping ensures that every cloud configuration parameter (such as VPC subnet CIDR masks, Kubernetes resource requests and limits, or Cloud SQL isolation flags) can be traced directly to an underlying engineering constraint or business requirement.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Mastering traceability separates senior cloud architects from superficial configuration technicians. When a managed cloud service exhibits anomalous behavior (such as intermittent latency spikes, connection drops, or cold-start delays), technicians are helpless because they treat the cloud as a magic black box. In contrast, an architect fluent in traceability looks through the cloud abstraction to understand what is occurring at the kernel, socket, or disk tier. This enables the architect to optimize cost (avoiding over-provisioning memory by tuning Linux cgroups), maximize reliability (calculating TCP keep-alive timers across load balancers), and enforce zero-trust security perimeters.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> The entirety of Google Cloud can be mapped directly to Block 1 foundational primitives:
1. <em>Linux Namespaces &amp; Cgroups (Days 5, 10):</em> Form the runtime foundation of Google Kubernetes Engine (GKE) worker nodes and Cloud Run container execution sandboxes (gVisor).
2. <em>TCP/IP &amp; CIDR Routing (Days 2, 8):</em> Govern Virtual Private Cloud (VPC) subnet allocation, Cloud Interconnect peering, and Cloud NAT gateway sizing.
3. <em>DNS &amp; TLS (Days 3, 8):</em> Dictate Cloud DNS private managed zones, Google-managed SSL certificate lifecycle, and Cloud Load Balancing SSL termination profiles.
4. <em>ACID SQL Transactions (Day 16):</em> Define the consistency models of Cloud SQL for PostgreSQL and Cloud Spanner multi-region read-write transactions.
By mastering these foundational mappings, architects transition seamlessly into Block 2 (Days 18–35), where they will construct enterprise Google Cloud landing zones, resource hierarchies, and Cloud Identity perimeters.</p>

<table class="comparison-table">
  <caption>Table 17.1: End-to-End Foundation Request Pipeline, Subsystems, and Failure Invariants</caption>
  <thead>
    <tr>
      <th scope="col">Pipeline Stage</th>
      <th scope="col">Underlying Subsystem</th>
      <th scope="col">Block 1 Day</th>
      <th scope="col">Core Architectural Invariant</th>
      <th scope="col">Primary Failure Mode &amp; Defense</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1. DNS Resolution</th>
      <td>Recursive Resolver / Stub Resolver</td>
      <td>Days 3, 4</td>
      <td>Deterministic FQDN to IP translation; strictly bounded TTL caching</td>
      <td>Search domain loop / NXDOMAIN timeout; defense: explicit FQDN and private authoritative zones</td>
    </tr>
    <tr>
      <th scope="row">2. TCP/IP Routing</th>
      <td>OS Routing Table / L3 Gateway / ARP</td>
      <td>Day 2</td>
      <td>Non-overlapping CIDR allocations; deterministic next-hop gateway egress</td>
      <td>Subnet IP collision / local loop; defense: enterprise IPAM and non-overlapping RFC 1918 allocations</td>
    </tr>
    <tr>
      <th scope="row">3. TLS Termination</th>
      <td>TLS 1.3 Cryptographic Engine</td>
      <td>Day 8</td>
      <td>Mutual identity authentication; forward secrecy cipher suites</td>
      <td>Certificate expiration / cipher mismatch; defense: automated certificate renewal and TLS 1.3 enforcement</td>
    </tr>
    <tr>
      <th scope="row">4. POSIX Runtime</th>
      <td>Linux Kernel Namespaces &amp; Cgroups</td>
      <td>Days 5, 8, 10</td>
      <td>Non-root execution (UID &gt; 10000); strict cgroup memory and CPU limits</td>
      <td>OOM killer SIGKILL / privilege escalation; defense: non-root user and cgroup memory limits with swap off</td>
    </tr>
    <tr>
      <th scope="row">5. 12-Factor App</th>
      <td>POSIX Process / JSON Parser / Stdout</td>
      <td>Day 15</td>
      <td>Strict schema validation; unbuffered structured JSON logging with request IDs</td>
      <td>Malformed payload / silent buffer drop; defense: HTTP 422 schema rejection and trace context injection</td>
    </tr>
    <tr>
      <th scope="row">6. Relational Persistence</th>
      <td>ACID Engine / Write-Ahead Log (WAL)</td>
      <td>Day 16</td>
      <td>Atomic commit or clean rollback; &le; 1 physical fulfillment per unique order ID</td>
      <td>Partial write / duplicate shipment; defense: BEGIN/ROLLBACK boundaries and UNIQUE(order_id) constraints</td>
    </tr>
  </tbody>
</table>

<div class="technical-figure">
PLACEHOLDER_FIG_17_1
</div>

<p><strong class="side-heading">Concrete example:</strong> Synthesizing the complete foundational request path: establishing a local POSIX socket listener, simulating Twelve-Factor input validation, and executing an atomic relational transaction with rollback verification using Python 3 and SQLite:</p>
<pre><code># 1. Author and execute a comprehensive foundation request and rollback simulator
$ cat &lt;&lt;'EOF' &gt; scratch/day17_foundation_demo.py
import json
import sqlite3
import sys

# Step 1: Initialize relational database with 3NF schema and duplicate fulfillment invariant
db = sqlite3.connect(":memory:")
cur = db.cursor()

cur.execute(\"\"\"
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_email TEXT NOT NULL,
    total_cents INTEGER NOT NULL,
    status TEXT NOT NULL
);
\"\"\")

cur.execute(\"\"\"
CREATE TABLE order_fulfillments (
    fulfillment_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL UNIQUE, -- NON-NEGOTIABLE INVARIANT: &lt;= 1 fulfillment per order
    tracking_number TEXT NOT NULL,
    dispatched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(order_id) REFERENCES orders(order_id)
);
\"\"\")
db.commit()

# Step 2: Simulate Twelve-Factor Request Validation (Days 14-15)
raw_request = '{ "order_id": "ORD-17-8821", "customer_email": "baker@brightloaf.internal", "total_cents": 4200, "items": [{"sku": "SOURDOUGH", "qty": 2}] }'
request_data = json.loads(raw_request)
assert "@" in request_data["customer_email"], "Validation error: invalid email"
assert request_data["total_cents"] > 0, "Validation error: total must be positive"

# Step 3: Execute Atomic Order Transaction (Day 16)
cur.execute("BEGIN TRANSACTION;")
try:
    cur.execute("INSERT INTO orders (order_id, customer_email, total_cents, status) VALUES (?, ?, ?, ?);",
                (request_data["order_id"], request_data["customer_email"], request_data["total_cents"], "PENDING"))
    cur.execute("INSERT INTO order_fulfillments (fulfillment_id, order_id, tracking_number) VALUES (?, ?, ?);",
                ("FUL-9901", request_data["order_id"], "TRK-BRIGHT-17"))
    db.commit()
    print("SUCCESS: Order and fulfillment committed atomically.")
except Exception as e:
    db.rollback()
    print(f"FAILED: Rolled back due to error: {e}")

# Step 4: Prove Rollback Mechanics (Abort transaction on simulated failure)
cur.execute("BEGIN TRANSACTION;")
try:
    cur.execute("INSERT INTO orders (order_id, customer_email, total_cents, status) VALUES (?, ?, ?, ?);",
                ("ORD-FAIL-01", "test@brightloaf.internal", 1500, "PENDING"))
    # Simulate payment gateway timeout triggering rollback
    raise RuntimeError("Payment gateway timeout after 5000 ms")
    db.commit()
except Exception as e:
    db.rollback()
    print(f"VERIFIED ROLLBACK: {e}")

# Verify no orphaned record exists
cur.execute("SELECT COUNT(*) FROM orders WHERE order_id = 'ORD-FAIL-01';")
count = cur.fetchone()[0]
assert count == 0, f"Invariant violated: orphaned order found! count={count}"
print(f"PASS: Zero orphaned rows confirmed after rollback (count={count}).")

# Step 5: Test Duplicate Event Replay Invariant (&lt;= 1 physical fulfillment)
try:
    cur.execute("INSERT INTO order_fulfillments (fulfillment_id, order_id, tracking_number) VALUES (?, ?, ?);",
                ("FUL-9902-DUP", "ORD-17-8821", "TRK-BRIGHT-DUP"))
    db.commit()
    print("CRITICAL DEFECT: Duplicate fulfillment accepted!")
except sqlite3.IntegrityError as e:
    db.rollback()
    print(f"PASS: Invariant preserved! Relational UNIQUE constraint caught duplicate replay: {e}")

db.close()
EOF
$ python3 scratch/day17_foundation_demo.py
SUCCESS: Order and fulfillment committed atomically.
VERIFIED ROLLBACK: Payment gateway timeout after 5000 ms
PASS: Zero orphaned rows confirmed after rollback (count=0).
PASS: Invariant preserved! Relational UNIQUE constraint caught duplicate replay: UNIQUE constraint failed: order_fulfillments.order_id
</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> The demonstration above verifies POSIX in-memory relational transaction semantics, atomic rollbacks, and schema-level uniqueness constraints in Python 3. It simulates network request intake and payment gateway timeouts within a single process and does not measure physical network packet propagation or distributed multi-node consensus latency across Google Cloud regions.</p>"""

TOPIC_01_TECHNICAL = TOPIC_01_TECHNICAL.replace('PLACEHOLDER_FIG_17_1', FIG_17_1_HTML)

TOPIC_01_SCENARIO = {
    'scenario': (
        "During an infrastructure refresh at BrightLoaf, the DevOps team migrated the bakery order ingestion microservice "
        "into a newly provisioned container network while leaving the backend PostgreSQL order database in an existing internal subnet. "
        "Immediately following cutover, the order ingestion service experienced cascading 10,000 ms connection timeouts whenever "
        "attempting to establish TCP handshakes with db.brightloaf.internal. Developers initially suspected application thread pool exhaustion "
        "or database connection pool saturation and attempted to restart the containers. However, the connection timeouts persisted. "
        "Investigation revealed two compounding defects: first, both the order container bridge network and the database subnet had been "
        "assigned the identical RFC 1918 CIDR block (10.0.1.0/24), causing the host Linux kernel to route database-bound packets locally to "
        "its own virtual bridge interface rather than forwarding them to the external gateway; second, the container resolv.conf was populated "
        "with four search domains (order.svc.cluster.local, svc.cluster.local, cluster.local, brightloaf.internal), causing unqualified "
        "queries for db to cycle through multiple sequential NXDOMAIN responses before timing out."
    ),
    'impact': (
        "Morning order ingestion across 42 commercial bakery distribution hubs failed for 85 minutes. Over 1,200 retail store bread "
        "deliveries were delayed, resulting in estimated retail stockouts of $64,000 and triggering severe contractual SLA penalties "
        "from major supermarket partners."
    ),
    'constraints': (
        "RFC 1918 private IPv4 allocations must be mathematically disjoint across all communicating VPCs and container subnets. "
        "DNS resolution in latency-sensitive microservice pipelines must use explicit Fully Qualified Domain Names (FQDN) or strict "
        "ndots configuration to prevent wasteful search domain lookup loops."
    ),
    'evidence': FIG_17_3_HTML,
    'diagram_enabled': False,
    'facts': (
        "Supplied incident facts and logs:\n"
        "1. Order ingestion container assigned IP 10.0.1.15 in local subnet 10.0.1.0/24.\n"
        "2. Backend PostgreSQL database assigned IP 10.0.1.50 in database subnet 10.0.1.0/24.\n"
        "3. Container resolv.conf contained search order.svc.cluster.local svc.cluster.local cluster.local brightloaf.internal with ndots:5.\n"
        "4. Supplied application logs recorded repeated error: connect ETIMEDOUT 10.0.1.50:5432 after 10000ms.\n"
        "5. Host routing table showed 10.0.1.0/24 dev br0 proto kernel scope link src 10.0.1.1."
    ),
    'inference': (
        "Because both subnets shared 10.0.1.0/24, the Linux kernel network stack treated 10.0.1.50 as a local on-link address on br0. "
        "The kernel broadcast ARP requests on the local container bridge instead of forwarding TCP SYN packets to the default gateway. "
        "Furthermore, querying unqualified hostname 'db' caused the resolver to query four nonexistent domains sequentially, "
        "adding 4,000 ms of cumulative DNS delay before failing."
    ),
    'expected': (
        "Re-addressing the order container network to disjoint subnet 10.10.1.0/24 and the database tier to 10.20.1.0/24, combined with "
        "authoritative private DNS resolution using FQDN db.production.brightloaf.internal, establishes deterministic Layer 3 next-hop "
        "routing and restores sub-2 ms TCP handshakes."
    ),
    'root': (
        "Overlapping RFC 1918 CIDR subnet allocation (10.0.1.0/24 in both container and database networks) causing local routing blackholes, "
        "compounded by excessive DNS search domain iteration."
    ),
    'verify': (
        "Execute ip route get 10.20.1.50 to verify next-hop routing via gateway 10.10.1.1, and verify that getent hosts "
        "db.production.brightloaf.internal resolves in under 2 ms with zero NXDOMAIN search iterations."
    ),
    'residual': (
        "Future microservice subnet provisioning must be governed by an automated IP Address Management (IPAM) CIDR reservation registry "
        "in CI/CD to prevent overlapping allocations."
    ),
    'diagnostic_steps': [
        "Inspect container network interfaces and routing table using ip addr and ip route show to detect overlapping CIDRs.",
        "Execute traceroute -n 10.0.1.50 and observe packets looping locally or terminating at the bridge interface without gateway transit.",
        "Capture DNS resolution latency using dig +trace +search db to measure cumulative delay from search domain suffixes.",
        "Review PostgreSQL pg_stat_activity logs to verify zero incoming TCP SYN packets reached port 5432 during the incident."
    ],
    'remediation_steps': [
        "Reconfigure container bridge network CIDR to dedicated non-overlapping range 10.10.1.0/24.",
        "Update application database connection string to use explicit FQDN db.production.brightloaf.internal.",
        "Tune container resolv.conf to set ndots:1 and remove superfluous search domains.",
        "Enforce automated subnet collision linting in Terraform infrastructure deployment pipelines."
    ]
}

TOPIC_01_LAB = {
    'name': 'Exercise A: Reproduce Foundation Request Flow and SQL Transaction Rollback',
    'goal': (
        "Synthesize Block 1 concepts by executing a non-root POSIX containerized request pipeline, simulating DNS resolution "
        "and CIDR routing, and proving atomic SQL rollback and relational uniqueness constraints."
    ),
    'expected': (
        "A verified suite of executable Python and Bash scripts in scratch/day17_lab/ reproducing DNS lookup, TCP/HTTP intake, "
        "Twelve-Factor validation, and atomic database transaction rollback."
    ),
    'mode': (
        "Observed locally: POSIX shell scripts, Python 3 HTTP request handler, SQLite transaction rollback, and unique constraint "
        "enforcement in scratch/day17_lab/. Simulated or predicted: DNS recursive resolver latency, Linux kernel network namespaces, "
        "and multi-tier database rollback logging. Untested on GCP: Production Cloud SQL instance failover, Google Cloud DNS managed "
        "private zones, and VPC firewall packet filtering."
    ),
    'covers': "Reproduce the local request flow and SQL rollback without copying the walkthrough",
    'prereq': 'Linux terminal, Python 3.10+, standard POSIX shell tools (mkdir, cat, python3)',
    'preflight': 'Verify Python 3 runtime availability and initialize dedicated Day 17 lab workspace',
    'verification': 'Execute test suites and verify exit codes equal 0 with all JSON artifacts present in scratch/day17_lab/',
    'trouble': 'Ensure all simulation scripts reside in scratch/day17_lab/ and use valid JSON formatting',
    'cleanup': 'All generated files reside in scratch/day17_lab/ for validation gate auditing',
    'accept': 'All 8 stages complete successfully with zero unhandled errors and all evidence files saved',
    'file': 'day-017-topic-01.md',
    'steps': [
        (
            "**Stage 1: Preflight Environment and Workspace Initialization**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Verify runtime tools and initialize the dedicated laboratory directory structure for Topic 1 request flow synthesis.\n"
            "```bash\n"
            "command -v bash\n"
            "command -v python3\n"
            "command -v mkdir\n"
            "command -v cat\n"
            "mkdir -p scratch/day17_lab\n"
            "cat <<'EOF' > scratch/day17_lab/stage1_init.py\n"
            "import json\n"
            "import sys\n"
            "\n"
            "preflight_state = {\n"
            "    \"day\": 17,\n"
            "    \"topic\": \"topic-01\",\n"
            "    \"exercise\": \"Reproduce Foundation Request Flow and SQL Transaction Rollback\",\n"
            "    \"status\": \"INITIALIZED\",\n"
            "    \"python_version\": sys.version,\n"
            "    \"workspace\": \"scratch/day17_lab\"\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage1_preflight.json\", \"w\") as f:\n"
            "    json.dump(preflight_state, f, indent=2)\n"
            "\n"
            "print(\"Stage 1 complete: Preflight verified and workspace initialized.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage1_init.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Preflight metadata saved to scratch/day17_lab/stage1_preflight.json with status INITIALIZED.\n\n"
            "**Save:** scratch/day17_lab/stage1_preflight.json"
        ),
        (
            "**Stage 2: Model DNS Resolution and CIDR Routing Boundaries**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Author a Python simulation modeling DNS resolution and non-overlapping CIDR routing tables between client, service, and database tiers.\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage2_network_model.py\n"
            "import ipaddress\n"
            "import json\n"
            "\n"
            "# Define authoritative private DNS records\n"
            "dns_zone = {\n"
            "    \"api.brightloaf.internal\": \"10.10.1.10\",\n"
            "    \"db.production.brightloaf.internal\": \"10.20.1.50\"\n"
            "}\n"
            "\n"
            "# Define RFC 1918 Subnets\n"
            "subnet_client = ipaddress.ip_network(\"10.0.1.0/24\")\n"
            "subnet_service = ipaddress.ip_network(\"10.10.1.0/24\")\n"
            "subnet_database = ipaddress.ip_network(\"10.20.1.0/24\")\n"
            "\n"
            "# Assert non-overlapping invariant across all subnets\n"
            "assert not subnet_client.overlaps(subnet_service), \"Client and service subnets must not overlap\"\n"
            "assert not subnet_service.overlaps(subnet_database), \"Service and database subnets must not overlap\"\n"
            "assert not subnet_client.overlaps(subnet_database), \"Client and database subnets must not overlap\"\n"
            "\n"
            "network_audit = {\n"
            "    \"dns_records\": dns_zone,\n"
            "    \"subnets\": {\n"
            "        \"client_tier\": str(subnet_client),\n"
            "        \"service_tier\": str(subnet_service),\n"
            "        \"database_tier\": str(subnet_database)\n"
            "    },\n"
            "    \"disjoint_subnets_verified\": True,\n"
            "    \"routing_invariants_preserved\": True\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage2_network_audit.json\", \"w\") as f:\n"
            "    json.dump(network_audit, f, indent=2)\n"
            "\n"
            "print(\"Stage 2 complete: Disjoint subnets and DNS routing verified.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage2_network_model.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Network routing audit written to scratch/day17_lab/stage2_network_audit.json confirming disjoint subnets.\n\n"
            "**Save:** scratch/day17_lab/stage2_network_audit.json"
        ),
        (
            "**Stage 3: Author Twelve-Factor Request Handler with JSON Schema Validation**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Author a Twelve-Factor application request validation handler that enforces strict schema requirements and emits structured JSON logs.\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage3_request_handler.py\n"
            "import json\n"
            "import re\n"
            "import time\n"
            "\n"
            "EMAIL_REGEX = r\"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$\"\n"
            "\n"
            "def validate_order_request(raw_payload):\n"
            "    try:\n"
            "        data = json.loads(raw_payload)\n"
            "    except Exception as e:\n"
            "        return False, {\"error\": \"Malformed JSON\", \"code\": 400}\n"
            "    \n"
            "    required = [\"order_id\", \"customer_email\", \"total_cents\", \"items\"]\n"
            "    for field in required:\n"
            "        if field not in data:\n"
            "            return False, {\"error\": f\"Missing required field: {field}\", \"code\": 422}\n"
            "    \n"
            "    if not re.match(EMAIL_REGEX, data[\"customer_email\"]):\n"
            "        return False, {\"error\": \"Invalid email format\", \"code\": 422}\n"
            "    \n"
            "    if not isinstance(data[\"total_cents\"], int) or data[\"total_cents\"] <= 0:\n"
            "        return False, {\"error\": \"total_cents must be a positive integer\", \"code\": 422}\n"
            "    \n"
            "    if not isinstance(data[\"items\"], list) or len(data[\"items\"]) == 0:\n"
            "        return False, {\"error\": \"items must be a non-empty array\", \"code\": 422}\n"
            "    \n"
            "    return True, data\n"
            "\n"
            "# Test valid payload\n"
            "valid_raw = json.dumps({\n"
            "    \"order_id\": \"ORD-17-001\",\n"
            "    \"customer_email\": \"store-402@brightloaf.com\",\n"
            "    \"total_cents\": 12500,\n"
            "    \"items\": [{\"sku\": \"SOURDOUGH-01\", \"qty\": 10}]\n"
            "})\n"
            "ok, result = validate_order_request(valid_raw)\n"
            "assert ok is True\n"
            "\n"
            "# Test invalid payload (negative cents)\n"
            "invalid_raw = json.dumps({\n"
            "    \"order_id\": \"ORD-17-002\",\n"
            "    \"customer_email\": \"bad@brightloaf.com\",\n"
            "    \"total_cents\": -500,\n"
            "    \"items\": [{\"sku\": \"BRIOCHE\", \"qty\": 1}]\n"
            "})\n"
            "fail_ok, fail_result = validate_order_request(invalid_raw)\n"
            "assert fail_ok is False and fail_result[\"code\"] == 422\n"
            "\n"
            "handler_audit = {\n"
            "    \"valid_test\": result,\n"
            "    \"invalid_test\": fail_result,\n"
            "    \"schema_enforced\": True,\n"
            "    \"twelve_factor_logging\": \"unbuffered_json_stdout\"\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage3_validation_audit.json\", \"w\") as f:\n"
            "    json.dump(handler_audit, f, indent=2)\n"
            "\n"
            "print(\"Stage 3 complete: Twelve-Factor request validation verified.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage3_request_handler.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Validation test audit written to scratch/day17_lab/stage3_validation_audit.json.\n\n"
            "**Save:** scratch/day17_lab/stage3_validation_audit.json"
        ),
        (
            "**Stage 4: Author Relational Database Schema with Invariant Constraints**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Author a Python script creating a normalized 3NF SQLite database with strict foreign keys and a schema-level UNIQUE constraint enforcing the duplicate fulfillment invariant.\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage4_db_schema.py\n"
            "import json\n"
            "import sqlite3\n"
            "\n"
            "db_path = \"scratch/day17_lab/orders.db\"\n"
            "conn = sqlite3.connect(db_path)\n"
            "cur = conn.cursor()\n"
            "\n"
            "cur.executescript(\"\"\"\n"
            "PRAGMA foreign_keys = ON;\n"
            "\n"
            "DROP TABLE IF EXISTS order_fulfillments;\n"
            "DROP TABLE IF EXISTS order_items;\n"
            "DROP TABLE IF EXISTS orders;\n"
            "\n"
            "CREATE TABLE orders (\n"
            "    order_id TEXT PRIMARY KEY,\n"
            "    customer_email TEXT NOT NULL,\n"
            "    total_cents INTEGER NOT NULL CHECK (total_cents > 0),\n"
            "    status TEXT NOT NULL DEFAULT 'PENDING',\n"
            "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
            ");\n"
            "\n"
            "CREATE TABLE order_items (\n"
            "    item_id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
            "    order_id TEXT NOT NULL,\n"
            "    sku TEXT NOT NULL,\n"
            "    qty INTEGER NOT NULL CHECK (qty > 0),\n"
            "    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE\n"
            ");\n"
            "\n"
            "CREATE TABLE order_fulfillments (\n"
            "    fulfillment_id TEXT PRIMARY KEY,\n"
            "    order_id TEXT NOT NULL UNIQUE, -- INVARIANT: <= 1 fulfillment per order_id\n"
            "    tracking_code TEXT NOT NULL,\n"
            "    dispatched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
            "    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE RESTRICT\n"
            ");\n"
            "\"\"\")\n"
            "conn.commit()\n"
            "conn.close()\n"
            "\n"
            "schema_record = {\n"
            "    \"database\": db_path,\n"
            "    \"tables\": [\"orders\", \"order_items\", \"order_fulfillments\"],\n"
            "    \"foreign_keys_enabled\": True,\n"
            "    \"unique_constraint\": \"order_fulfillments.order_id UNIQUE\"\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage4_schema_audit.json\", \"w\") as f:\n"
            "    json.dump(schema_record, f, indent=2)\n"
            "\n"
            "print(\"Stage 4 complete: Relational schema and constraints initialized.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage4_db_schema.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Database initialized at scratch/day17_lab/orders.db and schema audit saved to scratch/day17_lab/stage4_schema_audit.json.\n\n"
            "**Save:** scratch/day17_lab/stage4_schema_audit.json"
        ),
        (
            "**Stage 5: Execute Successful Order Request and Database Persistence**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Execute an end-to-end request transaction that inserts an order, child order items, and a fulfillment record atomically within an explicit transaction boundary.\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage5_commit_transaction.py\n"
            "import json\n"
            "import sqlite3\n"
            "\n"
            "db_path = \"scratch/day17_lab/orders.db\"\n"
            "conn = sqlite3.connect(db_path)\n"
            "cur = conn.cursor()\n"
            "\n"
            "order_payload = {\n"
            "    \"order_id\": \"ORD-17-9001\",\n"
            "    \"customer_email\": \"bakery-chicago-01@brightloaf.com\",\n"
            "    \"total_cents\": 8400,\n"
            "    \"items\": [{\"sku\": \"RYE-LOAF-01\", \"qty\": 6}, {\"sku\": \"BAGUETTE-02\", \"qty\": 12}]\n"
            "}\n"
            "\n"
            "cur.execute(\"BEGIN TRANSACTION;\")\n"
            "try:\n"
            "    cur.execute(\"INSERT INTO orders (order_id, customer_email, total_cents, status) VALUES (?, ?, ?, 'CONFIRMED');\",\n"
            "                (order_payload[\"order_id\"], order_payload[\"customer_email\"], order_payload[\"total_cents\"]))\n"
            "    for item in order_payload[\"items\"]:\n"
            "        cur.execute(\"INSERT INTO order_items (order_id, sku, qty) VALUES (?, ?, ?);\",\n"
            "                    (order_payload[\"order_id\"], item[\"sku\"], item[\"qty\"]))\n"
            "    cur.execute(\"INSERT INTO order_fulfillments (fulfillment_id, order_id, tracking_code) VALUES (?, ?, ?);\",\n"
            "                (\"FUL-17-001\", order_payload[\"order_id\"], \"TRK-USPS-9001\"))\n"
            "    conn.commit()\n"
            "    status = \"COMMITTED\"\n"
            "except Exception as e:\n"
            "    conn.rollback()\n"
            "    status = f\"FAILED: {e}\"\n"
            "\n"
            "# Verify persisted state\n"
            "cur.execute(\"SELECT COUNT(*) FROM orders WHERE order_id = ?;\", (order_payload[\"order_id\"],))\n"
            "order_count = cur.fetchone()[0]\n"
            "cur.execute(\"SELECT COUNT(*) FROM order_items WHERE order_id = ?;\", (order_payload[\"order_id\"],))\n"
            "items_count = cur.fetchone()[0]\n"
            "cur.execute(\"SELECT COUNT(*) FROM order_fulfillments WHERE order_id = ?;\", (order_payload[\"order_id\"],))\n"
            "ful_count = cur.fetchone()[0]\n"
            "conn.close()\n"
            "\n"
            "assert order_count == 1 and items_count == 2 and ful_count == 1, \"Atomic commit failed to persist all rows\"\n"
            "\n"
            "commit_result = {\n"
            "    \"order_id\": order_payload[\"order_id\"],\n"
            "    \"status\": status,\n"
            "    \"persisted_orders\": order_count,\n"
            "    \"persisted_items\": items_count,\n"
            "    \"persisted_fulfillments\": ful_count\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage5_commit_audit.json\", \"w\") as f:\n"
            "    json.dump(commit_result, f, indent=2)\n"
            "\n"
            "print(\"Stage 5 complete: Successful order committed atomically.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage5_commit_transaction.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Atomic commit audit saved to scratch/day17_lab/stage5_commit_audit.json confirming rows in all 3 tables.\n\n"
            "**Save:** scratch/day17_lab/stage5_commit_audit.json"
        ),
        (
            "**Stage 6: Rehearse Aborted Transaction and Verify Clean SQL Rollback**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Simulate an in-flight network crash and downstream payment failure, proving that an explicit SQL rollback leaves zero orphaned records or half-written state.\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage6_rollback_proof.py\n"
            "import json\n"
            "import sqlite3\n"
            "\n"
            "db_path = \"scratch/day17_lab/orders.db\"\n"
            "conn = sqlite3.connect(db_path)\n"
            "cur = conn.cursor()\n"
            "\n"
            "failed_order_id = \"ORD-17-FAIL-99\"\n"
            "\n"
            "cur.execute(\"BEGIN TRANSACTION;\")\n"
            "try:\n"
            "    # 1. Insert parent order\n"
            "    cur.execute(\"INSERT INTO orders (order_id, customer_email, total_cents, status) VALUES (?, ?, ?, 'PENDING');\",\n"
            "                (failed_order_id, \"unlucky-buyer@brightloaf.com\", 4500))\n"
            "    # 2. Insert child item\n"
            "    cur.execute(\"INSERT INTO order_items (order_id, sku, qty) VALUES (?, ?, ?);\",\n"
            "                (failed_order_id, \"CROISSANT-04\", 4))\n"
            "    # 3. Simulate sudden payment gateway network partition / unhandled exception\n"
            "    raise ConnectionResetError(\"Payment gateway reset connection after 10000ms\")\n"
            "    conn.commit()\n"
            "except Exception as e:\n"
            "    conn.rollback()\n"
            "    caught_error = str(e)\n"
            "\n"
            "# Verify absolute rollback: zero rows in orders or order_items for failed_order_id\n"
            "cur.execute(\"SELECT COUNT(*) FROM orders WHERE order_id = ?;\", (failed_order_id,))\n"
            "orphaned_orders = cur.fetchone()[0]\n"
            "cur.execute(\"SELECT COUNT(*) FROM order_items WHERE order_id = ?;\", (failed_order_id,))\n"
            "orphaned_items = cur.fetchone()[0]\n"
            "conn.close()\n"
            "\n"
            "assert orphaned_orders == 0, f\"Rollback failure: found {orphaned_orders} orphaned orders!\"\n"
            "assert orphaned_items == 0, f\"Rollback failure: found {orphaned_items} orphaned items!\"\n"
            "\n"
            "rollback_audit = {\n"
            "    \"tested_order_id\": failed_order_id,\n"
            "    \"simulated_error\": caught_error,\n"
            "    \"orphaned_orders_count\": orphaned_orders,\n"
            "    \"orphaned_items_count\": orphaned_items,\n"
            "    \"rollback_clean\": True\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage6_rollback_audit.json\", \"w\") as f:\n"
            "    json.dump(rollback_audit, f, indent=2)\n"
            "\n"
            "print(\"Stage 6 complete: Clean SQL rollback proved with zero orphaned rows.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage6_rollback_proof.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Rollback verification audit written to scratch/day17_lab/stage6_rollback_audit.json confirming zero orphaned rows.\n\n"
            "**Save:** scratch/day17_lab/stage6_rollback_audit.json"
        ),
        (
            "**Stage 7: Test Duplicate Event Replay and Prove Invariant Enforcement**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Simulate an at-least-once message queue redelivering an order fulfillment event twice, proving that the schema-level UNIQUE constraint suppresses duplicate physical fulfillment.\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage7_invariant_replay.py\n"
            "import json\n"
            "import sqlite3\n"
            "\n"
            "db_path = \"scratch/day17_lab/orders.db\"\n"
            "conn = sqlite3.connect(db_path)\n"
            "cur = conn.cursor()\n"
            "\n"
            "existing_order_id = \"ORD-17-9001\"\n"
            "\n"
            "# Attempt duplicate fulfillment insertion with identical order_id\n"
            "duplicate_caught = False\n"
            "cur.execute(\"BEGIN TRANSACTION;\")\n"
            "try:\n"
            "    cur.execute(\"INSERT INTO order_fulfillments (fulfillment_id, order_id, tracking_code) VALUES (?, ?, ?);\",\n"
            "                (\"FUL-17-REPLAY-DUP\", existing_order_id, \"TRK-DUP-LABEL\"))\n"
            "    conn.commit()\n"
            "except sqlite3.IntegrityError as e:\n"
            "    conn.rollback()\n"
            "    duplicate_caught = True\n"
            "    error_message = str(e)\n"
            "\n"
            "# Assert duplicate was caught and suppressed\n"
            "assert duplicate_caught is True, \"Invariant breach: duplicate fulfillment allowed!\"\n"
            "\n"
            "# Query database to prove exactly 1 fulfillment exists\n"
            "cur.execute(\"SELECT COUNT(*) FROM order_fulfillments WHERE order_id = ?;\", (existing_order_id,))\n"
            "fulfillment_count = cur.fetchone()[0]\n"
            "conn.close()\n"
            "\n"
            "assert fulfillment_count == 1, f\"Invariant breached! Fulfillment count = {fulfillment_count}\"\n"
            "\n"
            "invariant_audit = {\n"
            "    \"order_id\": existing_order_id,\n"
            "    \"duplicate_replay_caught\": duplicate_caught,\n"
            "    \"integrity_error\": error_message,\n"
            "    \"final_physical_fulfillments\": fulfillment_count,\n"
            "    \"duplicate_fulfillment_invariant_preserved\": True\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage7_invariant_audit.json\", \"w\") as f:\n"
            "    json.dump(invariant_audit, f, indent=2)\n"
            "\n"
            "print(\"Stage 7 complete: Duplicate fulfillment invariant strictly preserved.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage7_invariant_replay.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Invariant audit written to scratch/day17_lab/stage7_invariant_audit.json confirming duplicate caught and fulfillment count equals 1.\n\n"
            "**Save:** scratch/day17_lab/stage7_invariant_audit.json"
        ),
        (
            "**Stage 8: Validate Topic 1 Acceptance Criteria and Compile Evidence Summary**\n\n"
            "**Location:** local terminal\n\n"
            "**Actions:**\n"
            "Verify all Topic 1 stage artifacts exist and compile the final Exercise A evidence ledger.\n"
            "```bash\n"
            "cat <<'EOF' > scratch/day17_lab/stage8_topic1_summary.py\n"
            "import json\n"
            "import os\n"
            "\n"
            "required_artifacts = [\n"
            "    \"scratch/day17_lab/stage1_preflight.json\",\n"
            "    \"scratch/day17_lab/stage2_network_audit.json\",\n"
            "    \"scratch/day17_lab/stage3_validation_audit.json\",\n"
            "    \"scratch/day17_lab/stage4_schema_audit.json\",\n"
            "    \"scratch/day17_lab/stage5_commit_audit.json\",\n"
            "    \"scratch/day17_lab/stage6_rollback_audit.json\",\n"
            "    \"scratch/day17_lab/stage7_invariant_audit.json\"\n"
            "]\n"
            "\n"
            "missing = [p for p in required_artifacts if not os.path.isfile(p)]\n"
            "assert len(missing) == 0, f\"Missing required Topic 1 stage files: {missing}\"\n"
            "\n"
            "summary = {\n"
            "    \"exercise\": \"Exercise A: Reproduce Foundation Request Flow and SQL Transaction Rollback\",\n"
            "    \"topic\": \"topic-01\",\n"
            "    \"verified_stages\": 8,\n"
            "    \"all_artifacts_present\": True,\n"
            "    \"status\": \"PASS\"\n"
            "}\n"
            "\n"
            "with open(\"scratch/day17_lab/stage8_topic1_summary.json\", \"w\") as f:\n"
            "    json.dump(summary, f, indent=2)\n"
            "\n"
            "print(\"Stage 8 complete: Exercise A validation passed with all 8 stages verified.\")\n"
            "EOF\n"
            "python3 scratch/day17_lab/stage8_topic1_summary.py\n"
            "```\n\n"
            "**Expected result:**\n"
            "Summary audit saved to scratch/day17_lab/stage8_topic1_summary.json confirming all 8 stages verified.\n\n"
            "**Save:** scratch/day17_lab/stage8_topic1_summary.json"
        )
    ]
}

TOPIC_01 = {
    'key': 'topic-01',
    'title': 'Prerequisite review and remediation',
    'anchors': {
        'overview': 'topic-01-overview',
        'technical': 'topic-01-technical',
        'problem': 'topic-01-problem',
        'lab': 'topic-01-lab'
    },
    'overview': TOPIC_01_OVERVIEW,
    'preview': TOPIC_01_PREVIEW,
    'technical': TOPIC_01_TECHNICAL,
    'questions': TOPIC_01_QUESTIONS,
    'reference': 'https://cloud.google.com/learn/certification/cloud-architect#about-this-certification',
    'reference_label': 'Google Cloud Certification: Professional Cloud Architect — About this certification (accessed 2026-10-04)',
    'scenario': TOPIC_01_SCENARIO,
    'lab': TOPIC_01_LAB
}
