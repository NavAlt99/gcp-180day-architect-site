"""Day 20 Topic 2 technical content: Local software emulators and four-service behavioral boundaries."""

from scratch.generate_day_020 import FIG_20_2_HTML

TOPIC_02_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Local software emulator ecosystem and architectural purpose</strong></li>
<li><strong>Pub/Sub emulator capabilities and documented limitations</strong></li>
<li><strong>Cloud Firestore emulator behavior and production divergence</strong></li>
<li><strong>Cloud Spanner emulator in-memory schema engine and TrueTime limits</strong></li>
<li><strong>Cloud Bigtable emulator single-node limitations and key-range behavior</strong></li>
</ul>

<h4>Local software emulator ecosystem and architectural purpose</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Local Software Emulators</strong> are developer tooling components provided by cloud vendors that emulate distributed cloud managed services on a local development machine or within a CI/CD container. Emulators listen on standard TCP ports on the loopback interface (<code>127.0.0.1</code>) and implement the exact wire protocol (HTTP/REST or gRPC) and protobuf schemas used by production cloud services, allowing integration test suites to execute without cloud infrastructure costs, network latency, or internet access.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects balance developer velocity against architectural fidelity. While emulators provide indispensable local validation of API contracts and schema structures, architects must ensure engineering teams do not mistake emulator pass marks for production readiness. Architectural designs must treat emulators as functional unit testing aids while maintaining dedicated cloud integration environments for distributed performance, timing, and failure injection testing.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud architecture, emulators are officially provided for Cloud Pub/Sub, Cloud Firestore, Cloud Spanner, and Cloud Bigtable. Official Google Cloud Client Libraries contain native redirection hooks: when an environment variable such as <code>PUBSUB_EMULATOR_HOST=localhost:8085</code> is detected, the client library automatically redirects all calls to the local emulator and configures an insecure gRPC or HTTP transport channel, bypassing Google OAuth 2.0 authentication. While emulators provide high fidelity for functional API contracts, they run as single-process in-memory applications that completely omit production cloud infrastructure semantics, including distributed replication, high-availability failovers, partition latency, and scale-out performance characteristics.</p>

<h4>Pub/Sub emulator capabilities and documented limitations</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Cloud Pub/Sub Emulator</strong> is a Java-based local service that emulates the Google Cloud Pub/Sub messaging service. It provides full support for creating topics, creating subscriptions (pull and push), publishing messages, and acknowledging messages through standard gRPC and REST APIs.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects designing event-driven microservices must enforce consumer-side idempotency safeguards across all message handlers. Because the local Pub/Sub emulator delivers messages synchronously and with zero jitter, it masks at-least-once message replay bugs. Architects require that database unique constraints, deduplication tables, or distributed locks be implemented to ensure that real-world cloud redeliveries do not cause duplicate processing or financial errors.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> As documented in Google Cloud Pub/Sub Documentation: Known limitations (accessed 2026-10-04), the local Pub/Sub emulator exhibits critical architectural differences from production Cloud Pub/Sub:
1. Push subscriptions are not natively supported in standard local environments unless an explicit local HTTP endpoint is routable by the emulator process.
2. In-order message delivery via ordering keys is supported in the emulator, but because the emulator runs in a single in-memory thread, message arrival is virtually deterministic and instantaneous.
3. Production Pub/Sub provides at-least-once delivery guarantees where messages can be redelivered due to network jitter, subscriber ack timeouts, or cluster partition events. The emulator rarely triggers redeliveries unless explicitly forced by omitting acknowledgments. Applications tested solely against the emulator without consumer-side idempotency safeguards (such as database unique constraints) frequently suffer duplicate processing and double-fulfillment bugs in production.</p>

<h4>Cloud Firestore emulator behavior and production divergence</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Cloud Firestore Emulator</strong> is a component of the Firebase Local Emulator Suite that emulates both Firestore in Datastore mode and Firestore in Native mode. It provides comprehensive support for document CRUD operations, real-time snapshot listeners, security rule evaluation, and complex compound queries with in-memory collection indexing.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects utilize the Firestore emulator to validate document schemas and test complex Firestore Security Rules in local pull-request workflows. However, architects must mandate strict index declaration policies: because the emulator auto-creates composite indexes in memory, pipelines must explicitly validate that required composite indexes are declared in configuration files, preventing unindexed query failures when deployed to production.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud architectures, the Firestore emulator allows developers to validate complex Firestore Security Rules and compound query filters locally before deployment. However, the emulator departs from cloud production in several vital operational areas:
1. Indexing: Production Firestore requires composite indexes to be defined and built in advance for compound queries; the emulator automatically builds ad-hoc indexes in memory on the fly, allowing unindexed queries to succeed locally that will fail with an <code>FAILED_PRECONDITION</code> error in production.
2. Transaction Contention: Production Firestore enforces strict document lock contention limits (e.g., max 1 write per second per document under sustained load); the local emulator executes in a single JVM with near-zero write latency, completely masking lock timeouts and hot-spotting bottlenecks.
3. Limits: Production limits on document size (1 MB), batch write operations (max 500 writes per batch), and transaction duration are enforced, but storage durability is ephemeral unless explicitly exported to disk upon shutdown.</p>

<h4>Cloud Spanner emulator in-memory schema engine and TrueTime limits</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Cloud Spanner Emulator</strong> is a lightweight, hermetic implementation of Google Cloud Spanner designed for offline integration testing. Packaged as a native binary and Docker container, it supports both GoogleSQL and PostgreSQL dialects, schema DDL execution, ACID transactions, and standard read/write operations through official Spanner client libraries.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects designing globally distributed transactional databases must recognize the boundary between functional SQL validation and TrueTime distributed consensus. The Spanner emulator allows developers to test relational schemas, foreign keys, and query logic locally, but architects must mandate multi-region staging environments to validate commit wait latency, cross-region replication lag, and distributed lock contention under heavy concurrency.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Cloud Spanner's defining architectural achievement is external consistency at global scale enabled by Google TrueTime API (synchronized atomic clocks and GPS receivers). The local Spanner emulator cannot emulate TrueTime:
1. TrueTime &amp; Commit Wait: The emulator uses local system wall-clock time and implements simulated commit timestamps without the mandatory TrueTime uncertainty window (commit wait). Consequently, distributed race conditions that occur across globally separated Spanner instances cannot be reproduced on the emulator.
2. Scale &amp; Partitioning: Production Spanner dynamically splits tables into splits and distributes them across multiple Paxos groups; the emulator stores all data in a single SQLite in-memory database, masking hotspotting, split distribution latency, and query optimization differences.
3. Concurrent Transactions: High transaction concurrency on the emulator will encounter lock serializability constraints that differ significantly from multi-node Spanner Paxos leader coordination.</p>

<h4>Cloud Bigtable emulator single-node limitations and key-range behavior</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Cloud Bigtable Emulator</strong> provides a local standalone server that implements the Cloud Bigtable data and admin gRPC APIs. It allows developers to create instances, tables, and column families, and perform row-level mutations, scans, and filters using standard Bigtable client libraries.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Bigtable schema design is notoriously sensitive to row-key selection: poorly chosen sequential keys create catastrophic tablet hotspotting in production. Architects must educate developers that because the emulator holds all rows in a single in-memory table without tablet splitting, sequential key patterns appear to perform with microsecond latency locally. Architects must enforce row-key review standards and staging load tests before production cluster deployment.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Production Cloud Bigtable is a massively scalable NoSQL database designed for sub-10ms latency across petabytes of data, relying on dynamic tablet splitting, key-range tablet rebalancing across Compute Engine nodes, and distributed Colossus storage. The local Bigtable emulator diverges fundamentally from this architecture:
1. Single In-Memory Process: The emulator runs as a single Go-based process that stores table data entirely in memory. It does not write to durable storage, and all data is lost when the emulator process terminates.
2. Row Key Distribution &amp; Hotspotting: Production Bigtable performance is entirely dependent on row key design to avoid tablet hotspotting; because the emulator stores all data in memory without tablet partitioning, poorly designed row keys (such as sequential timestamps) will appear to perform with sub-millisecond latency on the emulator, only to suffer massive throughput degradation and CPU throttling on a production cluster.
3. Replication: Cross-region replication, failover policies, and replication latency are completely unsupported by the emulator.</p>

<table class="comparison-table">
  <caption>Table 20.2: Four-Service Software Emulator Architecture, Persistence, and Production Divergence</caption>
  <thead>
    <tr>
      <th scope="col">Service Emulator</th>
      <th scope="col">Default Port &amp; Protocol</th>
      <th scope="col">Storage &amp; Persistence Model</th>
      <th scope="col">Key Production Divergence / Unsupported Features</th>
      <th scope="col">High-Risk Architectural Assumption</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Cloud Pub/Sub</th>
      <td><code>8085</code> (gRPC / HTTP REST)</td>
      <td>In-memory JVM state (ephemeral; wiped on restart)</td>
      <td>No push endpoints; synchronous in-order delivery masks multi-zone at-least-once replay</td>
      <td>Assuming messages are delivered exactly once without consumer idempotency deduplication</td>
    </tr>
    <tr>
      <th scope="row">Cloud Firestore</th>
      <td><code>8080</code> (HTTP REST / WebSockets)</td>
      <td>In-memory with optional import/export flags (<code>--export-on-exit</code>)</td>
      <td>Auto-generates missing composite indexes; document lock contention not throttled</td>
      <td>Assuming compound queries will succeed in production without deploying composite indexes</td>
    </tr>
    <tr>
      <th scope="row">Cloud Spanner</th>
      <td><code>9010</code> (gRPC) / <code>9020</code> (REST)</td>
      <td>Single-process in-memory SQLite database</td>
      <td>No TrueTime commit wait; no Paxos group replication; no dynamic tablet splitting</td>
      <td>Assuming global external consistency timing without testing cross-region latency</td>
    </tr>
    <tr>
      <th scope="row">Cloud Bigtable</th>
      <td><code>8086</code> (gRPC)</td>
      <td>In-memory Go runtime state (ephemeral; zero disk durability)</td>
      <td>No tablet splitting or rebalancing; no replication or failover; hotspotting masked</td>
      <td>Assuming sequential row key schema performs well without production tablet distribution</td>
    </tr>
  </tbody>
</table>

<div class="technical-figure">
''' + FIG_20_2_HTML + '''
</div>

<p><strong class="side-heading">Concrete example:</strong> Configuring client library redirection to the local Pub/Sub emulator and validating topic creation via environment variables:</p>
<pre><code># 1. Start the local Pub/Sub emulator on port 8085
$ gcloud beta emulators pubsub start --host-port=127.0.0.1:8085 &amp;

# 2. Export standard client library redirection environment variable
$ export PUBSUB_EMULATOR_HOST=127.0.0.1:8085
$ export PUBSUB_PROJECT_ID=brightloaf-sandbox-20

# 3. Execute Python client script (automatically redirects to 127.0.0.1:8085 with insecure transport)
$ python3 -c "
import os
from google.cloud import pubsub_v1

project_id = os.environ.get('PUBSUB_PROJECT_ID', 'brightloaf-sandbox-20')
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, 'orders-stream')

try:
    topic = publisher.create_topic(request={'name': topic_path})
    print(f'Successfully created topic on emulator: {topic.name}')
except Exception as e:
    print(f'Topic creation result: {e}')
"
</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> The commands and matrix above demonstrate local software emulator redirection and documented service boundaries in local development environments. They do not simulate production multi-region network partitions, TrueTime clock skew injection, or petabyte-scale Bigtable tablet rebalancing dynamics.</p>
'''
