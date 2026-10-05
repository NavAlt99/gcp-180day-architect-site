"""Day 20 SVGs wrapped in figure containers with non-empty figcaptions."""

FIG_20_1_HTML = '''<figure class="diagram-container">
<svg aria-labelledby="fig20-1-title fig20-1-desc" height="520" role="img" viewbox="0 0 960 520" width="960" xmlns="http://www.w3.org/2000/svg">
<title id="fig20-1-title">Google Cloud Client Library Invocation Flow &amp; Asynchronous LRO Polling Lifecycle</title>
<desc id="fig20-1-desc">Sequence diagram illustrating the client library interaction, Service Usage authorization, synchronous return of an Operation resource, and exponential backoff polling until operation completion.</desc>
<defs>
<lineargradient id="p20-f1-bg" x1="0%" x2="100%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#090d16"></stop>
<stop offset="100%" stop-color="#121526"></stop>
</lineargradient>
<lineargradient id="p20-f1-panel" x1="0%" x2="0%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#1e293b" stop-opacity="0.8"></stop>
<stop offset="100%" stop-color="#0f172a" stop-opacity="0.9"></stop>
</lineargradient>
<marker id="p20-f1-arrow" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"></path>
</marker>
<marker id="p20-f1-arrow-poll" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#f59e0b"></path>
</marker>
<marker id="p20-f1-arrow-ok" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"></path>
</marker>
</defs>
<rect fill="url(#p20-f1-bg)" height="520" rx="12" stroke="#1e293b" stroke-width="1" width="960"></rect>
<!-- Header -->
<text fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" x="480" y="32">Figure 20.1: Client Library Invocation &amp; Asynchronous LRO Polling Lifecycle</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" x="480" y="50">Service Usage Check · Immediate Operation Handle · Exponential Backoff Polling with Jitter · Final Result</text>
<!-- Actors Header -->
<g transform="translate(50, 75)">
<!-- Client Runtime -->
<rect fill="#1e293b" height="40" rx="6" stroke="#38bdf8" stroke-width="1.5" width="180" x="0" y="0"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" x="90" y="24">Client Application</text>
<line stroke="#334155" stroke-dasharray="4 4" stroke-width="1.5" x1="90" x2="90" y1="40" y2="380"></line>
<!-- API Gateway / Service Usage -->
<rect fill="#1e293b" height="40" rx="6" stroke="#818cf8" stroke-width="1.5" width="180" x="260" y="0"></rect>
<text fill="#818cf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" x="350" y="24">Google API Gateway</text>
<line stroke="#334155" stroke-dasharray="4 4" stroke-width="1.5" x1="350" x2="350" y1="40" y2="380"></line>
<!-- Managed Service Backend -->
<rect fill="#1e293b" height="40" rx="6" stroke="#22c55e" stroke-width="1.5" width="180" x="520" y="0"></rect>
<text fill="#22c55e" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" x="610" y="24">Cloud Service Backend</text>
<line stroke="#334155" stroke-dasharray="4 4" stroke-width="1.5" x1="610" x2="610" y1="40" y2="380"></line>
<!-- Messages Flow -->
<!-- Step 1: Create request -->
<path d="M 90 70 L 345 70" fill="none" marker-end="url(#p20-f1-arrow)" stroke="#38bdf8" stroke-width="1.5"></path>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle" x="215" y="64">1. POST /v1/instances (Cloud SQL Create)</text>
<!-- Gateway check -->
<rect fill="#090d16" height="24" rx="4" stroke="#6366f1" stroke-width="1" width="100" x="300" y="80"></rect>
<text fill="#818cf8" font-family="system-ui, sans-serif" font-size="9" text-anchor="middle" x="350" y="96">Auth &amp; Service Check</text>
<path d="M 350 115 L 605 115" fill="none" marker-end="url(#p20-f1-arrow)" stroke="#38bdf8" stroke-width="1.5"></path>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle" x="480" y="110">Forward request to provisioner</text>
<!-- Step 2: Immediate LRO response -->
<path d="M 605 140 L 95 140" fill="none" marker-end="url(#p20-f1-arrow-poll)" stroke="#f59e0b" stroke-dasharray="5 3" stroke-width="1.5"></path>
<text fill="#fbbf24" font-family="monospace" font-size="10" text-anchor="middle" x="350" y="134">2. Return Operation { id: "op-9182", done: false }</text>
<!-- Step 3: Polling Loop 1 -->
<path d="M 90 180 L 345 180" fill="none" marker-end="url(#p20-f1-arrow-poll)" stroke="#f59e0b" stroke-width="1.5"></path>
<text fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle" x="215" y="174">3a. Poll: GET /operations/op-9182 (t = 1s)</text>
<path d="M 345 200 L 95 200" fill="none" marker-end="url(#p20-f1-arrow-poll)" stroke="#f59e0b" stroke-dasharray="5 3" stroke-width="1.5"></path>
<text fill="#f59e0b" font-family="monospace" font-size="10" text-anchor="middle" x="215" y="194">{ done: false, status: "PENDING" }</text>
<!-- Sleep / Backoff box -->
<rect fill="#1e1810" height="22" rx="4" stroke="#f59e0b" stroke-width="1" width="110" x="35" y="215"></rect>
<text fill="#fbbf24" font-family="system-ui, sans-serif" font-size="9" text-anchor="middle" x="90" y="230">Backoff: sleep(2.5s)</text>
<!-- Step 4: Polling Loop 2 -->
<path d="M 90 255 L 345 255" fill="none" marker-end="url(#p20-f1-arrow-poll)" stroke="#f59e0b" stroke-width="1.5"></path>
<text fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle" x="215" y="249">3b. Poll: GET /operations/op-9182 (t = 3.5s)</text>
<path d="M 345 275 L 95 275" fill="none" marker-end="url(#p20-f1-arrow-poll)" stroke="#f59e0b" stroke-dasharray="5 3" stroke-width="1.5"></path>
<text fill="#f59e0b" font-family="monospace" font-size="10" text-anchor="middle" x="215" y="269">{ done: false, status: "RUNNING" }</text>
<!-- Sleep / Backoff box -->
<rect fill="#1e1810" height="22" rx="4" stroke="#f59e0b" stroke-width="1" width="110" x="35" y="290"></rect>
<text fill="#fbbf24" font-family="system-ui, sans-serif" font-size="9" text-anchor="middle" x="90" y="305">Backoff: sleep(5.0s)</text>
<!-- Step 5: Final Poll OK -->
<path d="M 90 330 L 605 330" fill="none" marker-end="url(#p20-f1-arrow-ok)" stroke="#22c55e" stroke-width="1.5"></path>
<text fill="#86efac" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle" x="350" y="324">3c. Poll: GET /operations/op-9182 (t = 8.5s)</text>
<path d="M 605 350 L 95 350" fill="none" marker-end="url(#p20-f1-arrow-ok)" stroke="#22c55e" stroke-dasharray="4 2" stroke-width="2"></path>
<text fill="#4ade80" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="350" y="344">{ done: true, response: { instance: "brightloaf-db", ip: "10.0.1.5" } }</text>
</g>
<!-- Right Side Callout: Architectural Rules -->
<g transform="translate(740, 85)">
<rect fill="#0d1527" height="350" rx="8" stroke="#38bdf8" stroke-width="1.5" width="190" x="0" y="0"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">LRO Polling Rules</text>
<rect fill="#1e1418" height="95" rx="6" stroke="#ef4444" stroke-width="1" width="166" x="12" y="40"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="20" y="58">The Synchronous Trap:</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="20" y="74">Assuming HTTP 200 means</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="20" y="88">resource is ready causes</text>
<text fill="#ef4444" font-family="system-ui, sans-serif" font-size="9" x="20" y="102">connection refusal errors</text>
<text fill="#fca5a5" font-family="system-ui, sans-serif" font-size="9" x="20" y="116">in downstream steps.</text>
<rect fill="#09261a" height="105" rx="6" stroke="#22c55e" stroke-width="1" width="166" x="12" y="145"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="20" y="163">Correct Backoff Rule:</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="20" y="180">1. Initial delay: 1.0s</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="20" y="194">2. Multiplier: 1.5x</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="20" y="208">3. Random jitter: ±20%</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="20" y="222">4. Max delay cap: 30s</text>
<text fill="#86efac" font-family="system-ui, sans-serif" font-size="9" x="20" y="236">5. Total timeout: 15m</text>
<rect fill="#1e293b" height="75" rx="6" stroke="#64748b" stroke-width="1" width="166" x="12" y="260"></rect>
<text fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="20" y="280">Error Checking:</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9" x="20" y="296">Always check error field in</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9" x="20" y="310">operation when done: true</text>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="9" x="20" y="324">before accessing result.</text>
</g>
<!-- Bottom Banner -->
<rect fill="#111827" height="45" rx="6" stroke="#334155" stroke-width="1" width="900" x="30" y="460"></rect>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" x="45" y="480">Architectural Rule: Service mutations in Google Cloud return asynchronous LRO handles by contract.</text>
<text fill="#64748b" font-family="system-ui, sans-serif" font-size="10" x="45" y="495">Automated deployment pipelines must poll operations with exponential backoff and jitter, validating completion before initiating application traffic.</text>
</svg>
<figcaption>
<strong>Figure 20.1: Google Cloud Client Library Invocation Flow &amp; Asynchronous LRO Polling Lifecycle.</strong>
    Visualizes the transition from initial client request through Service Usage validation, the return of an uncompleted Operation resource, and programmatic exponential backoff polling until final resource readiness.
    <br/><strong>Supplied facts:</strong> Long-running infrastructure mutations return an Operation resource with <code>done: false</code>; final status must be polled via <code>operations.get</code> until <code>done: true</code>.
    <br/><strong>Architectural inference:</strong> Treating an initial HTTP 200 response as resource completion causes immediate connection failures in downstream deployment stages.
    <br/><strong>Expected post-fix behavior:</strong> Pipelines implement structured exponential backoff with randomized jitter and operation error inspection, ensuring resources are 100% operational before service traffic is routed.
  </figcaption>
</figure>'''

FIG_20_2_HTML = '''<figure class="diagram-container">
<svg aria-labelledby="fig20-2-title fig20-2-desc" height="520" role="img" viewbox="0 0 960 520" width="960" xmlns="http://www.w3.org/2000/svg">
<title id="fig20-2-title">Local Emulator Redirection Architecture &amp; Four-Service Behavioral Boundaries</title>
<desc id="fig20-2-desc">Architecture diagram showing how client libraries redirect traffic to local Pub/Sub, Firestore, Spanner, and Bigtable emulators via environment variables, detailing the specific divergence points from production.</desc>
<defs>
<lineargradient id="p20-f2-bg" x1="0%" x2="100%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#090d16"></stop>
<stop offset="100%" stop-color="#121526"></stop>
</lineargradient>
<lineargradient id="p20-f2-panel" x1="0%" x2="0%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#1e293b" stop-opacity="0.8"></stop>
<stop offset="100%" stop-color="#0f172a" stop-opacity="0.9"></stop>
</lineargradient>
<marker id="p20-f2-arrow" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"></path>
</marker>
<marker id="p20-f2-arrow-err" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"></path>
</marker>
<marker id="p20-f2-arrow-ok" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"></path>
</marker>
</defs>
<rect fill="url(#p20-f2-bg)" height="520" rx="12" stroke="#1e293b" stroke-width="1" width="960"></rect>
<!-- Header -->
<text fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" x="480" y="32">Figure 20.2: Local Emulator Redirection &amp; Four-Service Divergence Matrix</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" x="480" y="50">Environment Redirection Hooks · In-Memory Simulation Limits · Production System Contrasts</text>
<!-- Client Application Box (Left) -->
<rect fill="url(#p20-f2-panel)" height="350" rx="8" stroke="#38bdf8" stroke-width="1.5" width="210" x="30" y="80"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" x="42" y="104">Client Application Runtime</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="42" y="128">Google Cloud Client Library</text>
<!-- Env Redirection Hooks -->
<rect fill="#090d16" height="200" rx="6" stroke="#334155" stroke-width="1" width="190" x="40" y="145"></rect>
<text fill="#f8fafc" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" x="50" y="165">Redirection Variables:</text>
<text fill="#38bdf8" font-family="monospace" font-size="9" x="50" y="190">PUBSUB_EMULATOR_HOST</text>
<text fill="#94a3b8" font-family="monospace" font-size="9" x="50" y="204">=localhost:8085</text>
<text fill="#f59e0b" font-family="monospace" font-size="9" x="50" y="230">FIRESTORE_EMULATOR_HOST</text>
<text fill="#94a3b8" font-family="monospace" font-size="9" x="50" y="244">=localhost:8080</text>
<text fill="#22c55e" font-family="monospace" font-size="9" x="50" y="270">SPANNER_EMULATOR_HOST</text>
<text fill="#94a3b8" font-family="monospace" font-size="9" x="50" y="284">=localhost:9010</text>
<text fill="#818cf8" font-family="monospace" font-size="9" x="50" y="310">BIGTABLE_EMULATOR_HOST</text>
<text fill="#94a3b8" font-family="monospace" font-size="9" x="50" y="324">=localhost:8086</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" x="42" y="370">Auth Check: Bypassed</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="42" y="388">Transport: HTTP/2 plaintext</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="42" y="406">Zero cloud cost incurred</text>
<!-- Four Service Emulator Boxes in Center-Right -->
<g transform="translate(270, 80)">
<!-- 1. Pub/Sub -->
<rect fill="#0d1626" height="80" rx="6" stroke="#38bdf8" stroke-width="1.5" width="660" x="0" y="0"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="20">1. Cloud Pub/Sub Emulator (Port 8085 · Java Runtime)</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="40">Storage: In-memory only (ephemeral) · Ordering: Trivial single-thread FIFO without partition loss simulation</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="58">Divergence: Masks at-least-once message delivery replays and network ack timeouts seen in production.</text>
<!-- 2. Firestore -->
<rect fill="#1e1810" height="80" rx="6" stroke="#f59e0b" stroke-width="1.5" width="660" x="0" y="90"></rect>
<text fill="#fbbf24" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="110">2. Cloud Firestore Emulator (Port 8080 · Java Runtime)</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="130">Storage: Ephemeral memory (requires export/import flags) · Rules: Local engine tests rule syntax</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="148">Divergence: Relaxed index enforcement; does not simulate regional multi-master quorum latency or hot contention.</text>
<!-- 3. Spanner -->
<rect fill="#09261a" height="80" rx="6" stroke="#22c55e" stroke-width="1.5" width="660" x="0" y="180"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="200">3. Cloud Spanner Emulator (Port 9010 gRPC / 9020 REST · C++ Binary)</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="220">Storage: In-memory / single-process · Engine: SQLite backing core relational SQL parsing</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="238">Divergence: NO TrueTime uncertainty wait (ε); no distributed Paxos consensus, failover, or query cost modeling.</text>
<!-- 4. Bigtable -->
<rect fill="#161226" height="80" rx="6" stroke="#818cf8" stroke-width="1.5" width="660" x="0" y="270"></rect>
<text fill="#a5b4fc" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="290">4. Cloud Bigtable Emulator (Port 8086 · Go Binary)</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="310">Storage: In-memory hash table · API: gRPC Bigtable data and admin API contracts</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="328">Divergence: No tablet splitting, no SSD performance simulation, no hotspotting detection, and zero IAM check.</text>
</g>
<!-- Connecting Arrow from Client to Grid -->
<path d="M 240 255 L 268 255" fill="none" marker-end="url(#p20-f2-arrow)" stroke="#38bdf8" stroke-width="2"></path>
<!-- Bottom Banner -->
<rect fill="#111827" height="45" rx="6" stroke="#334155" stroke-width="1" width="900" x="30" y="460"></rect>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" x="45" y="480">Architectural Rule: An emulator validates API contract syntax, not distributed system semantics.</text>
<text fill="#64748b" font-family="system-ui, sans-serif" font-size="10" x="45" y="495">Always implement application-layer deduplication and idempotency keys to survive real-world at-least-once cloud delivery.</text>
</svg>
<figcaption>
<strong>Figure 20.2: Local Emulator Redirection Architecture &amp; Four-Service Behavioral Boundaries.</strong>
    Illustrates how Google Cloud Client Libraries intercept endpoint configuration to target local emulator processes and highlights key divergences from cloud production environments.
    <br/><strong>Supplied facts:</strong> Setting environment variables (such as <code>PUBSUB_EMULATOR_HOST</code>) transparently redirects client library RPCs to local loopback ports without authentication.
    <br/><strong>Architectural inference:</strong> Local emulators execute single-node in-memory implementations that mask distributed timing, TrueTime commit waits, and message replay loops inherent in production systems.
    <br/><strong>Expected post-fix behavior:</strong> Architecture teams utilize emulators for functional interface tests while enforcing consumer idempotency invariants to protect against production distributed failures.
  </figcaption>
</figure>'''

FIG_20_3_HTML = '''<figure class="diagram-container">
<svg aria-labelledby="fig20-3-title fig20-3-desc" height="520" role="img" viewbox="0 0 960 520" width="960" xmlns="http://www.w3.org/2000/svg">
<title id="fig20-3-title">Incident 20.1: Premature Execution on Unpolled LRO vs Exponential Backoff Polling</title>
<desc id="fig20-3-desc">Incident flow contrasting an automated deployment that failed by executing schema migrations against an unpolled PENDING_CREATE database versus an exponential backoff polling loop verifying done: true.</desc>
<defs>
<lineargradient id="p20-f3-bg" x1="0%" x2="100%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#090d16"></stop>
<stop offset="100%" stop-color="#121526"></stop>
</lineargradient>
<marker id="p20-f3-arrow-err" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"></path>
</marker>
<marker id="p20-f3-arrow-ok" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"></path>
</marker>
</defs>
<rect fill="url(#p20-f3-bg)" height="520" rx="12" stroke="#1e293b" stroke-width="1" width="960"></rect>
<!-- Title Header -->
<text fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" x="480" y="32">Figure 20.3: Incident Flow · Premature Execution on Unpolled Asynchronous LRO</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" x="480" y="50">Pipeline Synchronous Assumption · Connection Refusal Crash · LRO Polling Engine Defense</text>
<!-- Event Trigger (Left) -->
<rect fill="#1e293b" height="160" rx="8" stroke="#38bdf8" stroke-width="1.5" width="210" x="30" y="80"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="42" y="104">Trigger: DB Deployment</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="42" y="128">08:30 UTC Launch</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="42" y="146">CI pipeline provisions</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="42" y="164">Cloud SQL PostgreSQL</text>
<text fill="#38bdf8" font-family="monospace" font-size="9" x="42" y="186">POST /instances</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="42" y="204">Returns HTTP 200 (LRO)</text>
<!-- FAILED PATH (Top Branch) -->
<g transform="translate(270, 80)">
<rect fill="#1a0f12" height="160" rx="8" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="1.5" width="380" x="0" y="0"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">[FAILED PATH: Premature Migration on Unfinished LRO]</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="46">1. Pipeline treats HTTP 200 as instance ready</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="64">2. Immediately executes flyway schema migration</text>
<text fill="#fca5a5" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="84">3. Cloud SQL is in PENDING_CREATE state!</text>
<text fill="#ef4444" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="102">FAIL POINT: Connection refused on port 5432; migration aborts!</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" x="15" y="122">4. Container pods boot against half-migrated database</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" x="15" y="140">Launch halted; order dispatch stalled for 2 business days.</text>
</g>
<!-- CORRECTED PATH (Bottom Branch) -->
<g transform="translate(270, 270)">
<rect fill="#09261a" height="160" rx="8" stroke="#22c55e" stroke-width="1.5" width="380" x="0" y="0"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">[CORRECTED PATH: Exponential Backoff LRO Polling Gate]</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="46">1. Pipeline captures operation handle: operations/op-sql-99</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="64">2. Polls GET /operations/op-sql-99 with exponential backoff</text>
<text fill="#86efac" font-family="system-ui, sans-serif" font-size="10" x="15" y="84">3. Polling asserts: done == True &amp;&amp; error == None</text>
<text fill="#22c55e" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="102">CONTROL: Migration dispatches only after instance is RUNNABLE</text>
<text fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="10" x="15" y="122">4. UNIQUE(order_id) constraint verified in schema</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" x="15" y="140">100% deterministic deployment with zero crash downtime.</text>
</g>
<!-- Arrows from Trigger to Paths -->
<path d="M 240 140 L 268 140" fill="none" marker-end="url(#p20-f3-arrow-err)" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="2"></path>
<path d="M 135 240 L 135 350 L 268 350" fill="none" marker-end="url(#p20-f3-arrow-ok)" stroke="#22c55e" stroke-width="2"></path>
<!-- Verification Boundary on Right -->
<g transform="translate(690, 80)">
<rect fill="#0d1527" height="350" rx="8" stroke="#38bdf8" stroke-width="1.5" width="240" x="0" y="0"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" x="15" y="24">Verification Boundary</text>
<rect fill="#1e1418" height="85" rx="6" stroke="#ef4444" stroke-width="1" width="210" x="15" y="40"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="58">Failed Pipeline State:</text>
<text fill="#fca5a5" font-family="monospace" font-size="9" x="25" y="75">$ flyway migrate</text>
<text fill="#fca5a5" font-family="monospace" font-size="9" x="25" y="90">FATAL: Connection refused</text>
<text fill="#ef4444" font-family="system-ui, sans-serif" font-size="9" x="25" y="106">LRO state: PENDING_CREATE</text>
<rect fill="#09261a" height="120" rx="6" stroke="#22c55e" stroke-width="1" width="210" x="15" y="140"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="158">Corrected Pipeline State:</text>
<text fill="#86efac" font-family="monospace" font-size="9" x="25" y="175">$ python3 poll_lro.py</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="25" y="190">[POLL] done: false (t=5s)</text>
<text fill="#86efac" font-family="system-ui, sans-serif" font-size="9" x="25" y="206">[POLL] done: true (t=45s)</text>
<text fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="9" x="25" y="222">[PASS] State: RUNNABLE</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="9" x="25" y="238">Migrations executed 100%</text>
<rect fill="#1e293b" height="60" rx="6" stroke="#64748b" stroke-width="1" width="210" x="15" y="275"></rect>
<text fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="295">Invariant Preserved:</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9" x="25" y="312">Zero partial transactions</text>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="9" x="25" y="326">Single fulfillment invariant held</text>
</g>
<!-- Connectors to Verification -->
<path d="M 650 160 L 688 160" fill="none" marker-end="url(#p20-f3-arrow-err)" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="1.5"></path>
<path d="M 650 350 L 688 350" fill="none" marker-end="url(#p20-f3-arrow-ok)" stroke="#22c55e" stroke-width="2"></path>
<!-- Bottom Banner -->
<rect fill="#111827" height="45" rx="6" stroke="#334155" stroke-width="1" width="900" x="30" y="460"></rect>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" x="45" y="480">Architectural Rule: Never execute downstream mutations on pending LROs. Poll with exponential backoff.</text>
<text fill="#64748b" font-family="system-ui, sans-serif" font-size="10" x="45" y="495">Ensure database schema migrations commit unique order constraints before client traffic is enabled.</text>
</svg>
<figcaption>
<strong>Figure 20.3: Incident Flow · Premature Execution on Unpolled Asynchronous LRO.</strong>
    Contrasts a pipeline crash caused by executing migrations against a pending Cloud SQL instance with an automated exponential backoff polling gate.
    <br/><strong>Supplied facts:</strong> Infrastructure creation APIs return an Operation handle immediately; database instances remain in <code>PENDING_CREATE</code> until background provisioning completes.
    <br/><strong>Architectural inference:</strong> Pipelines that bypass LRO polling trigger immediate connection refused errors, leaving environments in an unrecoverable half-configured state.
    <br/><strong>Expected post-fix behavior:</strong> Automation workflows poll operations using exponential backoff with jitter, asserting <code>done: true</code> and verifying zero errors before executing schema migrations.
  </figcaption>
</figure>'''

FIG_20_4_HTML = '''<figure class="diagram-container">
<svg aria-labelledby="fig20-4-title fig20-4-desc" height="520" role="img" viewbox="0 0 960 520" width="960" xmlns="http://www.w3.org/2000/svg">
<title id="fig20-4-title">Incident 20.2: Single-Node Emulator Delivery Illusion vs Distributed At-Least-Once Production Replay</title>
<desc id="fig20-4-desc">Incident flow depicting how the Pub/Sub emulator single-thread in-memory behavior masked an at-least-once message replay loop, and how consumer-side database uniqueness constraints preserved single fulfillment.</desc>
<defs>
<lineargradient id="p20-f4-bg" x1="0%" x2="100%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#090d16"></stop>
<stop offset="100%" stop-color="#121526"></stop>
</lineargradient>
<marker id="p20-f4-arrow-err" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"></path>
</marker>
<marker id="p20-f4-arrow-ok" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"></path>
</marker>
</defs>
<rect fill="url(#p20-f4-bg)" height="520" rx="12" stroke="#1e293b" stroke-width="1" width="960"></rect>
<!-- Title Header -->
<text fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" x="480" y="32">Figure 20.4: Incident Flow · Emulator Illusion vs. At-Least-Once Production Replay</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" x="480" y="50">In-Memory Emulator Zero-Jitter Assumption · Ack Deadline Timeout · Idempotent Fulfillment Invariant Defense</text>
<!-- Event Trigger (Left) -->
<rect fill="#1e293b" height="160" rx="8" stroke="#38bdf8" stroke-width="1.5" width="210" x="30" y="80"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="42" y="104">Trigger: Production Surge</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="42" y="128">11:00 UTC Peak Baking</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="42" y="146">Tested only on emulator</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="42" y="164">Network jitter delays</text>
<text fill="#f59e0b" font-family="monospace" font-size="9" x="42" y="186">ack() &gt; 10s deadline</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="42" y="204">Pub/Sub redelivers message</text>
<!-- FAILED PATH (Top Branch) -->
<g transform="translate(270, 80)">
<rect fill="#1a0f12" height="160" rx="8" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="1.5" width="380" x="0" y="0"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">[FAILED PATH: Naive Consumer Assumes Exactly-Once]</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="46">1. Emulator never redelivered messages in tests</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="64">2. Devs omitted consumer deduplication filter</text>
<text fill="#fca5a5" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="84">3. Redelivered message reaches consumer pod B</text>
<text fill="#ef4444" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="102">FAIL POINT: Dispatches second baking ticket for same order!</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" x="15" y="122">4. 1,200 ingredient batches double-ordered</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" x="15" y="140">Emergency circuit breaker tripped to halt dispatch.</text>
</g>
<!-- CORRECTED PATH (Bottom Branch) -->
<g transform="translate(270, 270)">
<rect fill="#09261a" height="160" rx="8" stroke="#22c55e" stroke-width="1.5" width="380" x="0" y="0"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">[CORRECTED PATH: Idempotent Key &amp; Atomic DB Constraint]</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="46">1. Consumer checks Redis lease: SETNX order_id:lock</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="64">2. Replayed message rejected in cache or DB row-lock</text>
<text fill="#86efac" font-family="system-ui, sans-serif" font-size="10" x="15" y="84">3. Database enforces: UNIQUE(order_id) on fulfillments</text>
<text fill="#22c55e" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="102">CONTROL: Second insert catches 409 Conflict &amp; ACKs message</text>
<text fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="10" x="15" y="122">4. Exactly 1 physical bakery fulfillment generated</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" x="15" y="140">Invariant strictly maintained despite cloud message replays.</text>
</g>
<!-- Arrows from Trigger to Paths -->
<path d="M 240 140 L 268 140" fill="none" marker-end="url(#p20-f4-arrow-err)" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="2"></path>
<path d="M 135 240 L 135 350 L 268 350" fill="none" marker-end="url(#p20-f4-arrow-ok)" stroke="#22c55e" stroke-width="2"></path>
<!-- Verification Boundary on Right -->
<g transform="translate(690, 80)">
<rect fill="#0d1527" height="350" rx="8" stroke="#38bdf8" stroke-width="1.5" width="240" x="0" y="0"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" x="15" y="24">Verification Boundary</text>
<rect fill="#1e1418" height="85" rx="6" stroke="#ef4444" stroke-width="1" width="210" x="15" y="40"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="58">Failed Production Log:</text>
<text fill="#fca5a5" font-family="monospace" font-size="9" x="25" y="75">[DISPATCH] ORD-49281 (Pod A)</text>
<text fill="#fca5a5" font-family="monospace" font-size="9" x="25" y="90">[DISPATCH] ORD-49281 (Pod B)</text>
<text fill="#ef4444" font-family="system-ui, sans-serif" font-size="9" x="25" y="106">Duplicate batch produced!</text>
<rect fill="#09261a" height="120" rx="6" stroke="#22c55e" stroke-width="1" width="210" x="15" y="140"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="158">Corrected Consumer Log:</text>
<text fill="#86efac" font-family="monospace" font-size="9" x="25" y="175">[DISPATCH] ORD-49281 (Success)</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="25" y="190">[REPLAY] ORD-49281 caught</text>
<text fill="#86efac" font-family="system-ui, sans-serif" font-size="9" x="25" y="206">[DB 409] Duplicate rejected</text>
<text fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="9" x="25" y="222">[ACK] Redelivered msg acked</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="9" x="25" y="238">Total physical dispatches: 1</text>
<rect fill="#1e293b" height="60" rx="6" stroke="#64748b" stroke-width="1" width="210" x="15" y="275"></rect>
<text fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="295">Invariant Preserved:</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9" x="25" y="312">Order fulfillment count ≤ 1</text>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="9" x="25" y="326">Zero over-baking under replays</text>
</g>
<!-- Connectors to Verification -->
<path d="M 650 160 L 688 160" fill="none" marker-end="url(#p20-f4-arrow-err)" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="1.5"></path>
<path d="M 650 350 L 688 350" fill="none" marker-end="url(#p20-f4-arrow-ok)" stroke="#22c55e" stroke-width="2"></path>
<!-- Bottom Banner -->
<rect fill="#111827" height="45" rx="6" stroke="#334155" stroke-width="1" width="900" x="30" y="460"></rect>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" x="45" y="480">Architectural Rule: Cloud Pub/Sub guarantees at-least-once delivery; the emulator masks this by operating synchronously.</text>
<text fill="#64748b" font-family="system-ui, sans-serif" font-size="10" x="45" y="495">Production microservices must enforce consumer-side idempotency with database uniqueness constraints to prevent duplicate operations.</text>
</svg>
<figcaption>
<strong>Figure 20.4: Incident Flow · Emulator Illusion vs. At-Least-Once Production Replay.</strong>
    Demonstrates how the synchronous zero-jitter behavior of the local Pub/Sub emulator concealed a message replay bug, and how database uniqueness constraints preserved Brightloaf's single-fulfillment invariant in production.
    <br/><strong>Supplied facts:</strong> The Pub/Sub emulator executes in a single JVM with near-zero latency; production Pub/Sub operates across multi-zone clusters where network jitter can trigger ack deadline expiries and message redeliveries.
    <br/><strong>Architectural inference:</strong> Testing solely against an emulator without consumer idempotency checks leads to catastrophic double-fulfillment when deployed to cloud environments.
    <br/><strong>Expected post-fix behavior:</strong> Message handlers implement distributed locking and database-tier unique constraints, safely acknowledging redelivered messages while ensuring physical order fulfillment occurs exactly once.
  </figcaption>
</figure>'''

