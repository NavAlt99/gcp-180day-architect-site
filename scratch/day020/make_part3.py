with open('scratch/day020/fig3.html') as f:
    fig3 = f.read()
with open('scratch/day020/fig4.html') as f:
    fig4 = f.read()

part3 = f'''    <section class="part" id="part-3" aria-labelledby="part-3-title">
      <h2 id="part-3-title">3 · Real-world field problems and incident handling</h2>

      <article class="topic-card" id="topic-01-problem">
        <h3>Incident exercise · Premature database initialization fails on unpolled asynchronous LRO</h3>
        
        <p><strong>Symptom:</strong> During an automated release rollout at 08:30 UTC, Brightloaf\\'s deployment automation provisioned a new regional Cloud SQL PostgreSQL instance to support an expanded bakery franchise cluster. The deployment script issued an API creation call, received an immediate HTTP 200 response, and instantly dispatched database schema migration scripts. Within five seconds, the pipeline crashed: connection attempts to port 5432 were refused, the pipeline halted, and subsequent container deployments booted against an unmigrated, unreachable database, halting order dispatch for two business days.</p>

        <p><strong>Operational and business constraints:</strong> Brightloaf maintains a strict 99.95% availability SLO for regional franchise dispatch centers. An aborted migration leaves automated bakery fulfillment in a degraded state, incurring contract SLA penalty fees of $15,000 per hour. Crucially, any emergency database recovery must guarantee that order transaction journals remain consistent and that in-flight or replayed orders cannot create duplicate physical fulfillment records.</p>

        <p><strong>Evidence:</strong> Inspecting the Cloud SQL instance state via API queries immediately after the crash showed that the instance was still in the middle of initialization:</p>
        <pre><code class="language-bash">$ gcloud sql instances describe brightloaf-orders-db --format="yaml(state,ipAddresses)"
state: PENDING_CREATE
ipAddresses:
- ipAddress: 10.0.1.5
  type: PRIVATE

$ python3 scripts/migrate_schema.py
psycopg2.OperationalError: could not connect to server: Connection refused
	Is the server running on host "10.0.1.5" and accepting
	TCP/IP connections on port 5432?</code></pre>

        <p><strong>Root cause:</strong> The deployment pipeline author assumed that receiving an HTTP 200 response from the instance creation endpoint indicated that the database was fully provisioned and ready for connections. In reality, the Cloud SQL Admin API operates asynchronously: the HTTP 200 response merely returns a Long-Running Operation (LRO) resource with <code>done: false</code>. The instance remained in <code>PENDING_CREATE</code> for approximately 90 seconds while Compute Engine provisioned the underlying virtual machine, attached persistent disks, and initialized the PostgreSQL daemon.</p>

        <p><strong>Diagnostic sequence (5 steps):</strong></p>
        <ol>
          <li><strong>Extract and inspect operation handle:</strong> Capture the LRO resource name returned by the initial API response (e.g. <code>operations/sql-instance-create-op-8812</code>).</li>
          <li><strong>Query operational status:</strong> Issue an API call to inspect the operation\\'s current state, checking whether <code>done</code> evaluates to <code>true</code> or <code>false</code>.</li>
          <li><strong>Identify connection readiness:</strong> Verify the database instance state property, confirming that it transitions from <code>PENDING_CREATE</code> to <code>RUNNABLE</code> before dispatching connection strings.</li>
          <li><strong>Implement exponential backoff polling:</strong> Author an automated polling script with exponential backoff and jitter that waits for <code>done: true</code> and asserts that the <code>error</code> block is null.</li>
          <li><strong>Validate schema idempotency and duplicate fulfillment defense:</strong> Verify that the schema migration script applies a table constraint enforcing <code>UNIQUE(order_id)</code> on the fulfillment table, guaranteeing that order retries or replays during failover never produce duplicate physical bakery dispatches.</li>
        </ol>

        <p><strong>Defensible solution:</strong> Refactor the deployment pipeline to incorporate an automated LRO polling gate. The pipeline captures the operation identifier, initiates a polling loop with an initial delay of 2 seconds, backoff multiplier of 1.5, and maximum interval of 30 seconds. Schema migrations and microservice deployments are strictly gated until the operation returns <code>done: true</code> and the instance reports <code>RUNNABLE</code>.</p>

        <p><strong>Verification:</strong> Re-run the automated deployment script with the polling gate integrated, verifying that the operation is polled to completion before migrations execute:</p>
        <pre><code class="language-bash">$ python3 scripts/deploy_with_lro_gate.py --instance brightloaf-orders-db
[INIT] Dispatched instance creation request.
[LRO] Received operation: operations/sql-instance-create-op-8812
[POLL] Operation status: RUNNING (elapsed: 2s)
[POLL] Operation status: RUNNING (elapsed: 5s)
[POLL] Operation status: RUNNING (elapsed: 12s)
[POLL] Operation status: DONE (elapsed: 48s)
[LRO] Operation completed successfully. Zero errors reported.
[DB] Instance state: RUNNABLE. Commencing schema migrations...
[MIGRATE] Applying V1__initial_order_tables.sql...
[MIGRATE] Verified constraint: UNIQUE(order_id) on table order_fulfillments.
[SUCCESS] Pipeline completed with exit status 0.</code></pre>

        <p><strong>Residual risk:</strong> Under severe Google Cloud regional control plane congestion, an LRO may stall or exceed standard provisioning windows. Pipelines must specify an upper timeout ceiling (e.g. 15 minutes) and implement alerting to avoid blocking CI runner queues indefinitely.</p>

{fig3}

      </article>

      <article class="topic-card" id="topic-02-problem">
        <h3>Incident exercise · Emulator in-memory deduplication masks production message replay loop</h3>
        
        <p><strong>Symptom:</strong> A Brightloaf engineering team developed a new order fulfillment microservice and tested its message consumption against the local Cloud Pub/Sub emulator. In all local test runs, orders were processed smoothly with zero duplicate executions. However, within two hours of deploying the service to production Google Kubernetes Engine clusters, regional bakery monitors reported duplicate production batches: automated ovens had baked 1,200 redundant artisan bread orders, double-charging franchisee inventory quotas.</p>

        <p><strong>Operational and business constraints:</strong> Brightloaf\\'s core architectural contract mandates that no customer order can ever be physically fulfilled more than once ($\le 1$ physical fulfillment dispatches per order ID). Over-baking wastes perishable raw ingredients, causes warehouse queue contention, and invalidates inventory accounting records across franchise territories.</p>

        <p><strong>Evidence:</strong> Inspecting production GKE consumer pod logs revealed identical order messages being processed simultaneously by two independent consumer replicas:</p>
        <pre><code class="language-bash">[POD-A] Received Pub/Sub message: ID=msg-77182 OrderID=ORD-49281 AckDeadline=10s
[POD-A] Processing baking recipe calculation (duration: 11.2s)...
[CLOUD-PUBSUB] Message msg-77182 ack deadline expired! Redelivering to subscriber pool.
[POD-B] Received redelivered Pub/Sub message: ID=msg-77182 OrderID=ORD-49281
[POD-B] Dispatching baking ticket to Regional Bakery 04... (TICKET-9912)
[POD-A] Finished recipe. Dispatching baking ticket to Regional Bakery 04... (TICKET-9913)
[ALERT] DUPLICATE PHYSICAL FULFILLMENT: Order ORD-49281 has 2 active tickets!</code></pre>

        <p><strong>Root cause:</strong> The engineering team evaluated the service solely against the local Cloud Pub/Sub emulator. The emulator executes inside a single local JVM process with zero network jitter and near-instantaneous loopback execution, where processing times never exceeded the default 10-second acknowledgment deadline. Consequently, messages were never redelivered in local tests, and the developers omitted consumer-side idempotency filters.</p>
        <p>In production, Cloud Pub/Sub guarantees <strong>at-least-once delivery</strong> across distributed multi-zone clusters. When complex recipe calculations pushed Pod A\\'s processing time past the 10-second deadline, Pub/Sub correctly redelivered the unacknowledged message to Pod B. Lacking a deduplication lock, both pods committed fulfillment actions.</p>

        <p><strong>Diagnostic sequence (5 steps):</strong></p>
        <ol>
          <li><strong>Audit message acknowledgment durations:</strong> Inspect Cloud Monitoring metrics for <code>pubsub.googleapis.com/subscription/ack_latencies</code> to determine if consumer processing times exceed subscription acknowledgment deadlines.</li>
          <li><strong>Identify emulator vs production architectural divergence:</strong> Document that the emulator\\'s single-thread in-memory architecture does not simulate distributed lease expirations or multi-subscriber competition.</li>
          <li><strong>Inspect database fulfillment constraints:</strong> Verify whether the fulfillment database table enforces atomic unique constraints or permits duplicate order ID insertions.</li>
          <li><strong>Implement atomic consumer deduplication:</strong> Refactor the message consumer to acquire a distributed Redis lock (e.g. <code>SETNX order_lock:&lt;order_id&gt;</code>) or execute an atomic SQL conditional insert before dispatching physical inventory tickets.</li>
          <li><strong>Test synthetic message redelivery invariant:</strong> Replay duplicate synthetic order payloads against the consumer, verifying that replayed messages catch duplicate key conflicts, acknowledge the duplicate message, and maintain exactly one physical fulfillment.</li>
        </ol>

        <p><strong>Defensible solution:</strong> Extend the Pub/Sub subscription\\'s acknowledgment deadline from 10 seconds to 60 seconds to provide headroom for heavy compute tasks. Crucially, enforce idempotency at the consumer boundary: wrap fulfillment creation in an atomic database transaction using <code>INSERT ... ON CONFLICT (order_id) DO NOTHING</code> and verify that a database row lock (<code>SELECT ... FOR UPDATE</code>) halts concurrent consumer race conditions. If an order has already been fulfilled, the consumer logs a duplicate detection notice and immediately acknowledges the message without issuing a second baking ticket.</p>

        <p><strong>Verification:</strong> Re-run a synthetic redelivery simulation injecting duplicate order events, verifying that duplicate processing attempts are rejected while maintaining single fulfillment:</p>
        <pre><code class="language-bash">$ python3 tests/test_pubsub_idempotency.py --order-id ORD-49281 --replays 3
[SIMULATION] Publishing initial event: ORD-49281
[CONSUMER-1] Received ORD-49281. Executing fulfillment...
[DB] Inserted fulfillment record for ORD-49281. Ticket issued.
[SIMULATION] Injecting unacknowledged replay 1: ORD-49281
[CONSUMER-2] Received ORD-49281. Checking idempotency guard...
[DB] Duplicate order_id detected (UNIQUE constraint triggered).
[CONSUMER-2] Suppressed duplicate fulfillment ticket. Message ACKed.
[SIMULATION] Injecting unacknowledged replay 2: ORD-49281
[CONSUMER-1] Duplicate detected in Redis lock. Suppressed ticket. Message ACKed.
[ASSERTION] Invariant Verified: Total Physical Fulfillments == 1. Status: PASS.</code></pre>

        <p><strong>Residual risk:</strong> In the event of a total Redis cache flush or temporary memory eviction, deduplication falls back entirely to the relational database. Database connection pooling must be sized appropriately to absorb concurrent constraint checks during storm replays.</p>

{fig4}

      </article>
    </section>
'''

with open('scratch/day020/part3.html', 'w') as f:
    f.write(part3)

print('Part 3 written, length:', len(part3))
