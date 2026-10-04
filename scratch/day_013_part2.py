"""Day 13 Topic 2 technical discussion."""

TOPIC_02_TECH = '''
<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Stateless Architecture Foundations: Ephemeral Compute, Shared-Nothing Design, and Externalized State</strong></li>
<li><strong>Stateful Architecture Realities: Data Locality, Persistent Storage Bindings, and Ordered Lifecycle Dependencies</strong></li>
<li><strong>How State Placement Dictates High Availability, Autoscaling, and Failover Topologies</strong></li>
<li><strong>Session State, Caching, and Ephemeral Volatility: Redis, Memorystore, and Distributed State Stores</strong></li>
<li><strong>Stateful Managed Instance Groups and Stateful Kubernetes Workloads on GCP: Stateful MIGs and StatefulSets</strong></li>
</ul>

<p>The single most decisive architectural decision in cloud systems design is the classification and placement of application state. The choice between stateless and stateful architectures dictates how systems scale horizontally, how high availability is engineered across failure domains, and how automated failover behaves during infrastructure disruptions (<a href="https://docs.cloud.google.com/compute/docs/instance-groups#support_for_stateful_workloads" rel="noopener noreferrer">Google Cloud Compute Engine — Managed instance groups: Support for stateful workloads (accessed 2026-10-04)</a>). Architects must master the mechanisms of stateless decomposition, understand the constraints of persistent data locality, and leverage Google Cloud managed primitives to decouple ephemeral compute from durable state.</p>

<h3>Stateless Architecture Foundations: Ephemeral Compute, Shared-Nothing Design, and Externalized State</h3>

<p><strong class="side-heading">What it is in general:</strong>
A <strong class="keyword">Stateless Architecture</strong> adheres to a pure <em>Shared-Nothing Architecture (SN)</em> where individual compute worker nodes (virtual machines, containers, or serverless functions) retain zero persistent client state, session context, or local disk records between successive requests. In a stateless application, every incoming HTTP request or gRPC call contains all the authentication credentials, transaction payload, and context required to execute the operation—or the compute worker fetches that state dynamically from an externalized, centralized data tier.</p>

<p><strong class="side-heading">Relevance to a cloud architect:</strong>
Stateless compute instances are completely ephemeral, interchangeable, and disposable ("cattle, not pets"). An individual instance can experience a kernel panic, be evicted by a cloud hypervisor update, or be abruptly terminated by an autoscaler scale-in policy without causing any user-visible data loss or transaction corruption. Load balancers distribute requests across stateless instances using simple round-robin or least-request algorithms without requiring complex session stickiness. This property unlocks frictionless horizontal elasticity, rapid blue-green deployments, canary testing, and effortless multi-zone load balancing.</p>

<p><strong class="side-heading">Relevance to GCP:</strong>
In Google Cloud, stateless architecture is the native execution model for <strong class="keyword">Cloud Run</strong> and standard <strong class="keyword">Stateless Managed Instance Groups (MIGs)</strong>. Cloud Run scales container instances from zero to hundreds of concurrent workers in sub-seconds in response to incoming HTTP traffic. Because containers maintain zero local disk state, Google Cloud routes incoming traffic to whichever container instance has available concurrency headroom across the entire region.</p>

<h3>Stateful Architecture Realities: Data Locality, Persistent Storage Bindings, and Ordered Lifecycle Dependencies</h3>

<p><strong class="side-heading">What it is in general:</strong>
A <strong class="keyword">Stateful Architecture</strong> involves workloads that maintain authoritative data, transactional write-ahead logs, or persistent client state directly bound to specific physical nodes or attached persistent storage volumes. Subsequent requests depend directly on data mutations executed during preceding requests. Examples include relational database management systems (RDBMS), distributed message brokers (Kafka, RabbitMQ), distributed search clusters (Elasticsearch), and legacy monolithic enterprise software.</p>

<p><strong class="side-heading">Relevance to a cloud architect:</strong>
Stateful workloads cannot be scaled out or terminated arbitrarily. If an autoscaler terminates a stateful database instance without a graceful shutdown, in-flight transactions are aborted, uncommitted database write-ahead log buffers in memory are lost, and database indexes risk corruption. Furthermore, stateful nodes possess persistent identities (such as fixed hostnames, static internal IP addresses, and specific persistent disk attachments) that must be preserved across reboots. Scaling stateful systems horizontally requires complex distributed coordination: data partitioning (sharding), quorum consensus algorithms (Paxos, Raft), leader election, and distributed lock managers.</p>

<p><strong class="side-heading">Relevance to GCP:</strong>
Google Cloud provides managed stateful storage services that encapsulate this distributed complexity, such as <strong class="keyword">Cloud SQL</strong>, <strong class="keyword">AlloyDB</strong>, <strong class="keyword">Cloud Spanner</strong>, and <strong class="keyword">Cloud Bigtable</strong>. When architects must run self-managed stateful software (such as custom Cassandra or Kafka clusters) directly on Compute Engine, they utilize <strong class="keyword">Stateful Managed Instance Groups</strong> with stateful disk configurations to guarantee that attached Persistent Disks and IP addresses persist across VM repair and update cycles.</p>

<h3>How State Placement Dictates High Availability, Autoscaling, and Failover Topologies</h3>

<p><strong class="side-heading">What it is in general:</strong>
The placement of state determines the operational topology and failure boundaries of every cloud tier:
(1) <em>Stateless Tier:</em> High Availability is trivial. Identical compute instances are distributed across three availability zones behind a Cloud Load Balancer. If Zone A suffers an electrical failure, the load balancer detects failed health checks within 5 to 15 seconds and automatically redirects 100% of user traffic to healthy instances in Zone B and Zone C with zero downtime;
(2) <em>Stateful Tier:</em> High Availability is difficult and bound by physical latency. Multiple stateful nodes must replicate data across zones. To guarantee zero data loss (RPO = 0), replication must be synchronous, requiring every write transaction to complete a round-trip network acknowledgment across zones (adding 1.0 to 1.5 ms of latency per commit). During a zonal failure, automated failover requires promoting a standby replica to primary and repointing application connection pools, causing a 30 to 60-second operational pause.</p>

<p><strong class="side-heading">Relevance to a cloud architect:</strong>
The central tenet of resilient cloud design is: <em>Maximize the stateless compute surface and concentrate state into dedicated, managed storage engines</em>. A catastrophic anti-pattern is "accidental statefulness"—where developers store shopping cart data, in-flight transaction deduplication tokens, or uploaded user files in local VM process memory or temporary scratch disks. When traffic surges and the autoscaler replaces or scales down those VMs, customer data vanishes, causing severe application bugs that cannot be traced in testing environments.</p>

<p><strong class="side-heading">Relevance to GCP:</strong>
In GCP architectures, architects isolate the presentation and business logic layers into stateless Regional MIGs or Cloud Run services. All transient user sessions are externalized to <strong class="keyword">Memorystore for Redis</strong>, and all durable business transactions are committed to <strong class="keyword">Cloud SQL</strong> or <strong class="keyword">Cloud Spanner</strong>. This decoupling ensures that the compute tier can autoscale from 2 to 200 instances without touching database schemas or risking session loss.</p>

<h3>Session State, Caching, and Ephemeral Volatility: Redis, Memorystore, and Distributed State Stores</h3>

<p><strong class="side-heading">What it is in general:</strong>
To enable stateless application tiers while maintaining high performance, architects externalize ephemeral session state and transient data into high-speed in-memory data stores. An in-memory cache provides sub-millisecond read and write latency for user session tokens, shopping cart contents, and API rate-limiting buckets.</p>

<p><strong class="side-heading">Relevance to a cloud architect:</strong>
An architect must rigorously distinguish between <em>rebuildable volatile state</em> and <em>authoritative durable state</em>:
(1) <em>Volatile State:</em> Data that can be lost without compromising business integrity. For example, a cached product catalog or session lookup table. If the Redis cache crashes, user sessions may be invalidated (prompting users to log in again), or the database absorbs temporary cache-miss query spikes, but no financial ledgers are corrupted;
(2) <em>Durable State:</em> Irreplaceable business records—such as completed financial payments, order confirmations, and inventory allocations. <em>Authoritative durable state must never reside exclusively in a volatile in-memory cache</em>. Transactions must be written to an ACID-compliant durable database before acknowledging success to the client.</p>

<p><strong class="side-heading">Relevance to GCP:</strong>
Google Cloud provides <strong class="keyword">Memorystore for Redis</strong> as a fully managed, in-memory caching service with High Availability support. In an HA Memorystore configuration, Google Cloud automatically provisions a primary node and a replica node across two separate zones, replicating data via asynchronous replication and executing automatic failover within 30 seconds if the primary node degrades.</p>

<h3>Stateful Managed Instance Groups and Stateful Kubernetes Workloads on GCP: Stateful MIGs and StatefulSets</h3>

<p><strong class="side-heading">What it is in general:</strong>
When enterprise workloads cannot be decomposed into stateless microservices—such as legacy monolithic ERP systems, ZooKeeper ensembles, or stateful database appliances—architects must implement infrastructure automation that accommodates stateful constraints without sacrificing automated health checks and rolling upgrades.</p>

<p><strong class="side-heading">Relevance to a cloud architect:</strong>
Google Cloud addresses this requirement through specialized compute abstractions that bind persistent resources to specific instance identities:
(1) <em>Stateful Managed Instance Groups (Stateful MIGs):</em> Unlike standard stateless MIGs that treat VMs as disposable, a Stateful MIG allows architects to declare <em>Stateful Policy</em> and <em>Per-Instance Configs (PIC)</em>. When a VM in a Stateful MIG is updated, restarted, or auto-healed, GCP preserves the instance name, its internal and external IP addresses, and its attached Persistent Disks. The disk is detached from the failing VM and reattached to the replacement VM in the same zone;
(2) <em>GKE StatefulSets:</em> In Kubernetes, <strong class="keyword">StatefulSets</strong> manage the deployment and scaling of a set of Pods, providing guarantees about the ordering and uniqueness of these Pods (e.g., <kbd>web-0</kbd>, <kbd>web-1</kbd>). Each Pod receives a dedicated PersistentVolumeClaim (PVC) backed by a Compute Engine Persistent Disk that follows the Pod across rescheduling events.</p>

<p><strong class="side-heading">Relevance to GCP:</strong>
Architects configure Stateful MIGs via <kbd>gcloud compute instance-groups managed set-stateful-policy</kbd>, defining specific device names (such as <kbd>--stateful-disk=device-name=data-disk,auto-delete=never</kbd>) and static IP reservation. This capability allows organizations to modernize legacy stateful workloads with automated health-check auto-healing while guaranteeing zero data loss on attached persistent block storage.</p>

{FIG_13_2_HTML}

<div class="table-wrapper">
<table>
<thead>
<tr>
<th>Dimension</th>
<th>Stateless Architecture</th>
<th>Stateful Architecture</th>
<th>Externalized Session Cache</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Instance Lifecycle</strong></td>
<td>Ephemeral, disposable, immediately replaceable</td>
<td>Persistent identity, ordered lifecycle, non-interchangeable</td>
<td>Managed service lifecycle; volatile in-memory storage</td>
</tr>
<tr>
<td><strong>Local Disk State</strong></td>
<td>Zero persistent state; local storage is scratch-only</td>
<td>Authoritative write-ahead logs, database files, indexes</td>
<td>Ephemeral append-only snapshot files (RDB/AOF)</td>
</tr>
<tr>
<td><strong>Horizontal Elasticity</strong></td>
<td>Instantaneous (sub-minute scaling from 0 to 1,000+ instances)</td>
<td>Manual or coordinated (requires data rebalancing/sharding)</td>
<td>Vertical scaling or cluster sharding (Redis Cluster)</td>
</tr>
<tr>
<td><strong>HA Failover Mechanism</strong></td>
<td>Automated round-robin load balancer traffic diversion (&lt; 15s)</td>
<td>Replica promotion, VIP remount, or quorum election (30–60s)</td>
<td>Automatic primary-to-replica zonal failover (&lt; 30s)</td>
</tr>
<tr>
<td><strong>GCP Compute Primitive</strong></td>
<td>Cloud Run, Stateless Regional MIGs, GKE Deployments</td>
<td>Stateful MIGs, GKE StatefulSets, Bare Metal Solution</td>
<td>Cloud Memorystore for Redis / Memcached</td>
</tr>
</tbody>
</table>
</div>

<p><strong class="side-heading">Concrete example:</strong>
An international travel reservation portal refactors its architecture to survive unexpected regional traffic surges. The booking web API is containerized and deployed on a stateless Regional MIG across <kbd>us-central1-a</kbd>, <kbd>b</kbd>, and <kbd>c</kbd>, scaling from 4 to 80 instances based on CPU utilization. User session tokens, search history, and room lock reservations are externalized to an HA Memorystore Redis instance. All confirmed flight reservations and payment ledger records are durably committed to Cloud SQL PostgreSQL HA with synchronous standby replication. For a legacy flight reservation ticketing gateway that requires a fixed internal IP and local licensing disk bindings, the team provisions a Stateful MIG with a persistent data disk and static IP policy, achieving automated VM self-healing without invalidating third-party carrier software licenses.</p>

<p><strong class="side-heading">Evidence limit:</strong>
Externalizing state from compute workers to managed databases does not eliminate stateful failure domains; it shifts state complexity to the database tier. High connection counts from hundreds of autoscaling stateless workers can saturate database connection pools and lock tables, making database connection multiplexing (e.g., PgBouncer) and read caching mandatory architectural safeguards.</p>
'''
