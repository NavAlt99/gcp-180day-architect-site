with open('scratch/day020/fig1.html') as f:
    fig1 = f.read()
with open('scratch/day020/fig2.html') as f:
    fig2 = f.read()

part2 = f'''    <section class="part" id="part-2" aria-labelledby="part-2-title">
      <h2 id="part-2-title">2 · Architecture, control flow, boundaries, and limits</h2>

      <article class="topic-card" id="topic-01-technical">
        <h3>Google Cloud API architecture, client library transports, and asynchronous LRO polling</h3>
        <p>Google Cloud exposes all infrastructure and managed platform capabilities through structured Application Programming Interfaces (APIs). Understanding the control flow from client invocation through API enablement, authentication parsing, transport selection, and asynchronous operation polling is essential for building robust cloud architectures.</p>

        <h4>Service Enablement &amp; Propagation Boundaries</h4>
        <p>Before any project can consume a Google Cloud service, the service must be explicitly enabled through the Service Usage API (<code>serviceusage.googleapis.com</code>). When an administrator activates an API (such as the Cloud SQL Admin API or Cloud Pub/Sub API), the Service Usage control plane registers the activation across regional API gateways and edge routing proxies.</p>
        <p>Architects must account for <strong>enablement propagation latency</strong>: while API enablement returns a success status almost immediately, the activation state propagates eventually consistently across Google\\'s global frontends. During automated CI/CD provisioning, calls dispatched within 10 to 60 seconds of enablement can fail with <code>PERMISSION_DENIED: Service not enabled</code> errors unless automated retry handlers with exponential backoff are incorporated.</p>

        <h4>The Client Library Spectrum: Idiomatic vs. Discovery vs. REST</h4>
        <p>Google Cloud provides multiple tiers of programmatic access, each with distinct performance, concurrency, and maintenance profiles:</p>
        <ul>
          <li><strong>Google Cloud Client Libraries (Recommended):</strong> Modern, service-specific, idiomatic libraries (e.g. <code>google-cloud-pubsub</code>, <code>google-cloud-storage</code>). They communicate over high-performance <strong>gRPC over HTTP/2</strong> by default, supporting bi-directional streaming, binary protobuf serialization, automated channel pooling, dynamic OAuth 2.0 token refreshes, and built-in retries with exponential backoff and jitter.</li>
          <li><strong>Google API Client Libraries (Legacy):</strong> Generic, discovery-based libraries (e.g. <code>google-api-python-client</code>) dynamically generated from discovery documents. They use HTTP/1.1 REST transports, suffer higher JSON serialization overhead, and lack built-in gRPC streaming capabilities.</li>
          <li><strong>Direct REST / gRPC Endpoints:</strong> Raw HTTP requests directed to <code>*.googleapis.com</code> with manual <code>Authorization: Bearer &lt;token&gt;</code> headers. Useful for lightweight shell scripts or unsupported runtimes, but require developers to manually implement connection pooling, token lifecycle management, and retry algorithms.</li>
        </ul>

        <h4>Asynchronous Long-Running Operations (LRO)</h4>
        <p>Google Cloud APIs distinguish between <em>synchronous operations</em> (which execute within sub-second thresholds and return final results in the initial HTTP response) and <em>asynchronous mutations</em>. Operations that require resource orchestration—such as provisioning a Cloud SQL instance, creating a GKE cluster, or creating a persistent disk snapshot—cannot block the client HTTP connection without risking network gateway timeouts.</p>
        <p>For these operations, Google Cloud implements the <strong>Long-Running Operations (LRO) pattern</strong>. The initial API call synchronously returns an <code>Operation</code> resource handle with <code>done: false</code>, an operation identifier (e.g. <code>operations/operation-169829381-abcd</code>), and target resource metadata. The client application must then enter an asynchronous polling loop:</p>
        <ol>
          <li>Send <code>GET /v1/operations/{{operationId}}</code> to inspect the operation state.</li>
          <li>If <code>done: false</code>, calculate exponential backoff delay with randomized jitter:
            <br><code>delay = min(initial_delay * (multiplier ** attempt) + random_jitter, max_delay)</code>.
          </li>
          <li>Sleep for the computed duration and repeat the query.</li>
          <li>When <code>done: true</code>, check whether an <code>error</code> object is present. If an error is returned, parse the Google RPC error code (such as <code>RESOURCE_EXHAUSTED</code> or <code>DEADLINE_EXCEEDED</code>). If successful, extract the final resource representation from the <code>response</code> payload.</li>
        </ol>

        <div class="callout warning">
          <strong>The Synchronous Creation Fallacy</strong>
          <p>A frequent anti-pattern in cloud automation is treating an HTTP 200 response from a creation endpoint as a guarantee of resource readiness. The HTTP 200 response merely confirms that the API server accepted the request and initiated an asynchronous background operation. Attempting to connect to, configure, or migrate a resource before its LRO reports <code>done: true</code> results in immediate connection refusal and deployment pipeline failure.</p>
        </div>

        <div class="table-wrap">
          <table>
            <caption>Google Cloud API Invocation Models &amp; Asynchronous Operation Contracts</caption>
            <thead>
              <tr>
                <th scope="col">Invocation Model</th>
                <th scope="col">Protocol &amp; Transport</th>
                <th scope="col">Completion &amp; Polling Model</th>
                <th scope="col">Retry &amp; Backoff Mechanics</th>
                <th scope="col">Architectural Risk &amp; Failure Mode</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th scope="row">Google Cloud Client Libraries</th>
                <td>gRPC over HTTP/2 (Protobuf)</td>
                <td>Built-in LRO polling wrappers (<code>operation.result()</code>)</td>
                <td>Automated exponential backoff with randomized jitter</td>
                <td>Blocking calls in event-driven loops freeze worker threads; use async clients.</td>
              </tr>
              <tr>
                <th scope="row">Legacy API Client Libraries</th>
                <td>REST over HTTP/1.1 (JSON)</td>
                <td>Manual polling loop required for LRO resources</td>
                <td>Basic retry policies; no gRPC streaming support</td>
                <td>Higher latency on high-throughput streaming; elevated memory allocation.</td>
              </tr>
              <tr>
                <th scope="row">Direct REST Endpoints</th>
                <td>Raw HTTPS / JSON</td>
                <td>Explicit query against <code>operations.get</code> endpoint</td>
                <td>Must be hand-coded in client application</td>
                <td>Silent failure when scripts omit LRO polling; pipeline races ahead on pending state.</td>
              </tr>
              <tr>
                <th scope="row">Infrastructure as Code (Terraform)</th>
                <td>Underlying Go SDK (gRPC/REST)</td>
                <td>Automated provider polling with timeout boundaries</td>
                <td>Provider-managed retry on transient 429/503 errors</td>
                <td>Exceeding default provider timeout (e.g. 20m) fails state recording.</td>
              </tr>
            </tbody>
          </table>
        </div>

{fig1}

        <div class="further-study">
          <h4>Further Study · Primary Documentation</h4>
          <ul>
            <li><a href="https://cloud.google.com/service-usage/docs/overview" target="_blank" rel="noopener noreferrer">Google Cloud Documentation: Service Usage API Overview</a></li>
            <li><a href="https://cloud.google.com/apis/docs/client-libraries-explained" target="_blank" rel="noopener noreferrer">Google Cloud Documentation: Client Libraries Explained</a></li>
            <li><a href="https://cloud.google.com/apis/design/design_patterns#long_running_operations" target="_blank" rel="noopener noreferrer">Google Cloud Documentation: API Design Patterns — Long-Running Operations</a></li>
          </ul>
        </div>
      </article>

      <article class="topic-card" id="topic-02-technical">
        <h3>Local software emulators and four-service behavioral boundaries</h3>
        <p>Testing microservice architectures against live Google Cloud resources introduces financial costs, latency overhead, and cross-developer test collisions. Google Cloud provides local software emulators that replicate service API contracts on developer workstations. However, because emulators utilize lightweight local runtimes, architects must rigorously document their behavioral divergences from multi-zone cloud production systems.</p>

        <h4>Endpoint Redirection via Environment Variables</h4>
        <p>Official Google Cloud Client Libraries include native endpoint interception hooks. When a developer exports a service-specific emulator environment variable, the client library alters its internal transport configuration: it redirects network sockets to loopback addresses, changes the scheme from TLS to plaintext HTTP/2 or HTTP/1.1, and disables Google OAuth 2.0 credential discovery. No application code changes or conditional branching are required.</p>

        <h4>Four-Service Emulator Limitations &amp; Production Divergences</h4>
        <p>Architects must analyze the documented limitations of the four primary data and messaging emulators:</p>
        
        <ol>
          <li>
            <p><strong>Cloud Pub/Sub Emulator (<code>PUBSUB_EMULATOR_HOST=localhost:8085</code>):</strong></p>
            <ul>
              <li><em>Purpose:</em> Validates message publishing, topic schemas, subscription pulls, and acknowledgment contracts.</li>
              <li><em>Limitations:</em> Operates strictly in-memory within a single Java Virtual Machine process. It does not replicate multi-zone partition recovery, dead-letter topic exponential backoff delays, or high-throughput message reordering. Crucially, because local latency is negligible, messages are rarely redelivered due to acknowledgment timeouts—masking real-world at-least-once message replay bugs that cause duplicate order fulfillments in production.</li>
            </ul>
          </li>
          <li>
            <p><strong>Cloud Firestore Emulator (<code>FIRESTORE_EMULATOR_HOST=localhost:8080</code>):</strong></p>
            <ul>
              <li><em>Purpose:</em> Validates document hierarchy, CRUD operations, transactions, and Firestore Security Rules.</li>
              <li><em>Limitations:</em> By default, data resides in volatile memory and is purged when the process terminates unless <code>--export-on-exit</code> and <code>--import-data</code> flags are supplied. Composite index enforcement is significantly relaxed compared to production; queries that would fail in the cloud due to missing composite indexes often execute successfully in the emulator. Furthermore, the emulator does not simulate multi-region Paxos quorum latency.</li>
            </ul>
          </li>
          <li>
            <p><strong>Cloud Spanner Emulator (<code>SPANNER_EMULATOR_HOST=localhost:9010</code>):</strong></p>
            <ul>
              <li><em>Purpose:</em> Validates relational SQL syntax, DDL schema definitions, foreign key constraints, and client transactions.</li>
              <li><em>Limitations:</em> Implemented as a single-process C++ application backed by an in-memory SQLite storage engine. It completely lacks <strong>TrueTime support</strong>: instead of enforcing commit wait periods ($2\epsilon$) to guarantee external consistency across distributed nodes, it relies on the local system clock. It does not simulate distributed Paxos consensus, split-brain leader elections, automatic query plan optimization, or change streams.</li>
            </ul>
          </li>
          <li>
            <p><strong>Cloud Bigtable Emulator (<code>BIGTABLE_EMULATOR_HOST=localhost:8086</code>):</strong></p>
            <ul>
              <li><em>Purpose:</em> Validates Bigtable schema definitions (column families), mutations, row filtering, and range scans.</li>
              <li><em>Limitations:</em> Operates as a lightweight Go binary maintaining table data in memory. It does not simulate tablet splitting, SSTable LSM compaction cycles, key range hotspotting, or multi-cluster replication. Security and IAM authorization checks are entirely bypassed.</li>
            </ul>
          </li>
        </ol>

        <div class="table-wrap">
          <table>
            <caption>Four-Service Emulator Limitations and Production Divergence Matrix</caption>
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
                <td>Port 8085 · gRPC / REST</td>
                <td>Volatile in-memory Java heap</td>
                <td>No multi-zone partition loss; zero network jitter; push endpoints require manual proxying.</td>
                <td>Assuming single-delivery order processing without idempotent deduplication keys.</td>
              </tr>
              <tr>
                <th scope="row">Cloud Firestore</th>
                <td>Port 8080 · HTTP/REST</td>
                <td>In-memory (exportable to disk)</td>
                <td>Relaxed composite index requirements; no multi-region replication delay.</td>
                <td>Deploying queries without creating composite indexes in cloud configuration.</td>
              </tr>
              <tr>
                <th scope="row">Cloud Spanner</th>
                <td>Port 9010 (gRPC) / 9020 (REST)</td>
                <td>Single-process SQLite backing</td>
                <td><strong>No TrueTime ($2&epsilon; wait)</strong>; no distributed Paxos consensus; no change streams.</td>
                <td>Assuming transaction commit latency and query execution plans reflect cloud scale.</td>
              </tr>
              <tr>
                <th scope="row">Cloud Bigtable</th>
                <td>Port 8086 · gRPC</td>
                <td>In-memory Go hash structures</td>
                <td>No tablet splitting; no SSD performance curve; no hotspotting detection; no IAM.</td>
                <td>Assuming sequential row key designs will perform identically under multi-terabyte production loads.</td>
              </tr>
            </tbody>
          </table>
        </div>

{fig2}

        <div class="further-study">
          <h4>Further Study · Primary Documentation</h4>
          <ul>
            <li><a href="https://cloud.google.com/pubsub/docs/emulator" target="_blank" rel="noopener noreferrer">Google Cloud Documentation: Testing Apps Locally with the Pub/Sub Emulator</a></li>
            <li><a href="https://cloud.google.com/firestore/docs/emulator" target="_blank" rel="noopener noreferrer">Google Cloud Documentation: Test Rules and Queries with the Firestore Emulator</a></li>
            <li><a href="https://cloud.google.com/spanner/docs/emulator" target="_blank" rel="noopener noreferrer">Google Cloud Documentation: Emulating Cloud Spanner Locally</a></li>
            <li><a href="https://cloud.google.com/bigtable/docs/emulator" target="_blank" rel="noopener noreferrer">Google Cloud Documentation: Testing Apps with the Bigtable Emulator</a></li>
          </ul>
        </div>
      </article>
    </section>
'''

with open('scratch/day020/part2.html', 'w') as f:
    f.write(part2)

print('Part 2 written, length:', len(part2))
