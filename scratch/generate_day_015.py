"""Day 15 Overview and SVG Diagram Definitions."""

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'The Missing Semester of Your CS Education — Lecture 2: Shell Tools and Scripting § Shell Scripting (accessed 2026-10-04)',
        'https://missing.csail.mit.edu/2020/shell-tools/#shell-scripting'
    ),
    'topic-02': (
        'The Twelve-Factor App — Section XI: Logs - Treat logs as event streams (accessed 2026-10-04)',
        'https://12factor.net/logs#treat_logs_as_event_streams'
    )
}

PART1_HTML = '''<article class="topic-card overview" id="topic-01-overview">
<h3>Basic Python or Bash from an annotated example</h3>
<p><strong class="keyword">Modular application architecture</strong> begins with disciplined execution primitives across scripting runtimes and service boundaries. Whether implementing infrastructure automation in Bash or designing microservices in Python, cloud architects enforce predictable exit codes, pipeline flow control, and strict separation between stateless compute logic and external persistence. Contrasting monolithic architectures against containerized microservices and event-driven serverless platforms establishes how failure domains, deployment velocity, and scaling boundaries govern production reliability.</p>
<p><strong class="side-heading">Why today:</strong> Engineers frequently deploy tightly coupled monolithic services where a memory leak or unhandled exception in an ancillary module halts the entire core transactional processing engine.</p>
<p><strong class="side-heading">Where it sits:</strong> Sits between infrastructure scripting and distributed application design, bridging local runtime mechanics with Google Cloud deployment targets like Cloud Run and GKE.</p>
<p class="problem-preview">Problem preview: An e-commerce platform bundles order checkout and PDF invoice rendering into a single monolithic Python process. When a surge of complex invoice requests leaks memory and triggers an operating system Out-Of-Memory (OOM) kill, the entire order checkout pipeline crashes for 35 minutes, blocking $240,000 in customer transactions.</p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>Request validation, REST/JSON, request IDs and structured logs</h3>
<p><strong class="keyword">Distributed observability</strong> and rigorous request validation form the defensive perimeter of cloud-native microservices. Governed by Twelve-Factor methodology, production services reject malformed client payloads immediately at the network edge before engaging expensive database queries. Furthermore, modern microservices emit structured JSON logs directly to standard output as unbuffered event streams, decorating every log record with a globally unique Request ID (or W3C trace context) to enable sub-minute troubleshooting across distributed Google Cloud services.</p>
<p><strong class="side-heading">Why today:</strong> Unstructured plain-text logs scattered across distributed microservices create critical diagnostic blindspots during production outages, turning minor database timeouts into multi-hour customer-facing P1 incidents.</p>
<p><strong class="side-heading">Where it sits:</strong> Integrates API edge routing with Google Cloud Logging and Cloud Trace, anchoring runtime validation, error modeling, and distributed observability.</p>
<p class="problem-preview">Problem preview: A high-concurrency checkout failure inundates backend services with database lock timeouts, but applications emit unformatted free-form text strings without correlation IDs. On-call engineers spend 75 minutes manually grepping disjointed server logs across 40 container instances before isolating a downstream connection pool exhaustion bug.</p>
</article>'''

# Figure 15.1: Monolith vs Microservices vs Serverless
FIG_15_1_HTML = '''<figure id="fig-15-1" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day15-arch-patterns-title day15-arch-patterns-desc" viewBox="0 0 940 330" width="940" height="330" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day15-arch-patterns-title">Comparison of Monolith, Microservices, and Serverless Architecture Models</title>
<desc id="day15-arch-patterns-desc">Architectural comparison contrasting a tightly coupled monolithic process with independent containerized microservices and event-driven serverless Cloud Run functions, highlighting deployment boundaries and blast radius isolation.</desc>

<!-- Column 1: Monolithic Architecture -->
<rect x="20" y="25" width="280" height="280" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/server.svg" x="35" y="38" width="22" height="22"/>
<text x="65" y="54" fill="#f43f5e" font-size="12" font-weight="700">MONOLITHIC PATTERN</text>
<text x="65" y="70" fill="#94a3b8" font-size="9.5">Single Shared OS Process</text>

<rect x="35" y="85" width="250" height="150" rx="6" fill="#21262d" stroke="#f43f5e" stroke-width="1.2" stroke-dasharray="3 3"/>
<text x="45" y="104" fill="#fce7f3" font-size="10" font-weight="600">Single Shared Runtime Process (VM)</text>

<rect x="45" y="115" width="230" height="30" rx="4" fill="#161b22" stroke="#475569" stroke-width="1"/>
<text x="55" y="134" fill="#cbd5e1" font-size="9">Module A: Order Checkout Engine</text>

<rect x="45" y="150" width="230" height="30" rx="4" fill="#161b22" stroke="#475569" stroke-width="1"/>
<text x="55" y="169" fill="#cbd5e1" font-size="9">Module B: Inventory &amp; Catalog</text>

<rect x="45" y="185" width="230" height="30" rx="4" fill="#2d161d" stroke="#f43f5e" stroke-width="1.2"/>
<text x="55" y="204" fill="#f43f5e" font-size="9" font-weight="600">Module C: PDF Invoicing (OOM Leak!)</text>

<rect x="35" y="245" width="250" height="48" rx="4" fill="#1c2128" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="263" fill="#f43f5e" font-size="9" font-weight="700">Shared Failure Domain:</text>
<text x="45" y="278" fill="#94a3b8" font-size="8.5">OOM in PDF module kills entire VM &amp; checkout</text>

<!-- Column 2: Microservices Architecture -->
<rect x="330" y="25" width="280" height="280" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/gcp/legacy/google-kubernetes-engine.svg" x="345" y="38" width="22" height="22"/>
<text x="375" y="54" fill="#38bdf8" font-size="12" font-weight="700">MICROSERVICES PATTERN</text>
<text x="375" y="70" fill="#94a3b8" font-size="9.5">Isolated Container Boundaries (GKE)</text>

<rect x="345" y="85" width="250" height="45" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<text x="355" y="104" fill="#38bdf8" font-size="9.5" font-weight="600">Container 1: Order Service Pod</text>
<text x="355" y="119" fill="#94a3b8" font-size="8.5">Autoscales on CPU / Queue depth</text>

<rect x="345" y="138" width="250" height="45" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<text x="355" y="157" fill="#38bdf8" font-size="9.5" font-weight="600">Container 2: Inventory Service Pod</text>
<text x="355" y="172" fill="#94a3b8" font-size="8.5">Independent schema &amp; lifecycle</text>

<rect x="345" y="191" width="250" height="45" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<text x="355" y="210" fill="#34d399" font-size="9.5" font-weight="600">Container 3: PDF Worker Pod</text>
<text x="355" y="225" fill="#94a3b8" font-size="8.5">Isolated memory cgroup limits (OOM localized)</text>

<rect x="345" y="245" width="250" height="48" rx="4" fill="#1c2128" stroke="#38bdf8" stroke-width="1"/>
<text x="355" y="263" fill="#38bdf8" font-size="9" font-weight="700">Isolated Failure Domains:</text>
<text x="355" y="278" fill="#94a3b8" font-size="8.5">PDF restart never interrupts Order Pods</text>

<!-- Column 3: Serverless Architecture -->
<rect x="640" y="25" width="280" height="280" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-run.svg" x="655" y="38" width="22" height="22"/>
<text x="685" y="54" fill="#34d399" font-size="12" font-weight="700">SERVERLESS PATTERN</text>
<text x="685" y="70" fill="#94a3b8" font-size="9.5">Event-Driven Managed Scale (Cloud Run)</text>

<rect x="655" y="85" width="250" height="45" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/generic/endpoint.svg" x="665" y="97" width="18" height="18"/>
<text x="690" y="104" fill="#34d399" font-size="9.5" font-weight="600">Cloud Run: Order API</text>
<text x="690" y="119" fill="#94a3b8" font-size="8.5">Scales 0 to N; pay strictly per request</text>

<rect x="655" y="138" width="250" height="45" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/gcp/legacy/eventarc.svg" x="665" y="150" width="18" height="18"/>
<text x="690" y="157" fill="#34d399" font-size="9.5" font-weight="600">Eventarc / Pub/Sub Broker</text>
<text x="690" y="172" fill="#94a3b8" font-size="8.5">Asynchronous event buffering</text>

<rect x="655" y="191" width="250" height="45" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/cloud-run.svg" x="665" y="203" width="18" height="18"/>
<text x="690" y="210" fill="#34d399" font-size="9.5" font-weight="600">Cloud Run Job: Invoicing Worker</text>
<text x="690" y="225" fill="#94a3b8" font-size="8.5">Ephemeral execution; zero idle cost</text>

<rect x="655" y="245" width="250" height="48" rx="4" fill="#1c2128" stroke="#34d399" stroke-width="1"/>
<text x="665" y="263" fill="#34d399" font-size="9" font-weight="700">Zero Server Management:</text>
<text x="665" y="278" fill="#94a3b8" font-size="8.5">Full per-request isolation and instant scale</text>
</svg>
</div>
<figcaption>Figure 15.1: Comparison of Monolith, Microservices, and Serverless architecture models illustrating deployment units, shared versus isolated runtime processes, blast radius boundaries, and cloud scaling primitives.</figcaption>
</figure>'''

# Figure 15.2: Tracing & Structured Logging Flow
FIG_15_2_HTML = '''<figure id="fig-15-2" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day15-tracing-logs-title day15-tracing-logs-desc" viewBox="0 0 940 330" width="940" height="330" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day15-tracing-logs-title">End-to-End Request Tracing, Structured Logging, and Twelve-Factor Application Flow</title>
<desc id="day15-tracing-logs-desc">Architecture diagram illustrating the propagation of unique request identifiers through microservice tiers, formatted JSON logging emitted to standard output, and ingestion by Google Cloud Logging.</desc>
<defs>
<marker id="day15-trace-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day15-log-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#34d399"/></marker>
</defs>

<!-- Column 1: Client & Ingress Gateway -->
<rect x="20" y="25" width="210" height="275" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/client.svg" x="35" y="38" width="22" height="22"/>
<text x="65" y="54" fill="#38bdf8" font-size="12" font-weight="700">CLIENT &amp; INGRESS</text>
<text x="65" y="70" fill="#94a3b8" font-size="9.5">Cloud Load Balancer</text>

<rect x="35" y="85" width="180" height="60" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<text x="45" y="104" fill="#fce7f3" font-size="10" font-weight="600">Generates Request ID</text>
<text x="45" y="120" fill="#94a3b8" font-size="8.5">X-Request-Id: req-88f1a</text>
<text x="45" y="134" fill="#38bdf8" font-size="8.5">W3C: traceparent header</text>

<rect x="35" y="155" width="180" height="65" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<text x="45" y="174" fill="#fce7f3" font-size="10" font-weight="600">Perimeter Validation</text>
<text x="45" y="190" fill="#34d399" font-size="8.5">Fast-fail schema check</text>
<text x="45" y="204" fill="#34d399" font-size="8.5">Rejects malformed JSON (400)</text>

<rect x="35" y="230" width="180" height="55" rx="4" fill="#1c2128" stroke="#475569" stroke-width="1"/>
<text x="45" y="249" fill="#cbd5e1" font-size="9.5">Trace Context</text>
<text x="45" y="266" fill="#94a3b8" font-size="8.5">Propagates downstream</text>

<!-- Flow Arrow: Ingress to Microservice -->
<path d="M230 115 L260 115" stroke="#38bdf8" stroke-width="2" marker-end="url(#day15-trace-arr)"/>

<!-- Column 2: Order Microservice -->
<rect x="260" y="25" width="240" height="275" rx="8" fill="#161b22" stroke="#eab308" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-run.svg" x="275" y="38" width="22" height="22"/>
<text x="305" y="54" fill="#eab308" font-size="12" font-weight="700">ORDER SERVICE (12-FACTOR)</text>
<text x="305" y="70" fill="#94a3b8" font-size="9.5">Stateless Process Container</text>

<rect x="275" y="85" width="210" height="60" rx="4" fill="#21262d" stroke="#eab308" stroke-width="1.2"/>
<text x="285" y="104" fill="#fce7f3" font-size="10" font-weight="600">Context Extraction</text>
<text x="285" y="120" fill="#94a3b8" font-size="8.5">Binds req_id to async thread</text>
<text x="285" y="134" fill="#cbd5e1" font-size="8.5">Attaches customer_id context</text>

<rect x="275" y="155" width="210" height="60" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<text x="285" y="174" fill="#34d399" font-size="10" font-weight="600">Twelve-Factor Factor XI</text>
<text x="285" y="190" fill="#34d399" font-size="8.5">Logs as unbuffered event stream</text>
<text x="285" y="204" fill="#34d399" font-size="8.5">Emits structured JSON to stdout</text>

<rect x="275" y="225" width="210" height="60" rx="4" fill="#1c2128" stroke="#475569" stroke-width="1"/>
<text x="285" y="244" fill="#cbd5e1" font-size="9.5">Zero Local Disk Logs</text>
<text x="285" y="260" fill="#94a3b8" font-size="8.5">No file rotation /dev/null risks</text>
<text x="285" y="274" fill="#34d399" font-size="8.5">Pure container stdout stream</text>

<!-- Flow Arrow: Service to Logging -->
<path d="M500 185 L530 185" stroke="#34d399" stroke-width="2" marker-end="url(#day15-log-arr)"/>

<!-- Column 3: Structured Log Payload -->
<rect x="530" y="25" width="210" height="275" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<text x="545" y="52" fill="#34d399" font-size="12" font-weight="700">STRUCTURED JSON LOG</text>
<text x="545" y="68" fill="#94a3b8" font-size="9.5">RFC 8259 Standard Payload</text>

<rect x="540" y="80" width="190" height="205" rx="4" fill="#0b0e14" stroke="#334155" stroke-width="1"/>
<text x="550" y="98" fill="#94a3b8" font-size="8.5">{</text>
<text x="555" y="114" fill="#38bdf8" font-size="8.5">"timestamp": "2026-10-04...",</text>
<text x="555" y="130" fill="#fbbf24" font-size="8.5">"severity": "INFO",</text>
<text x="555" y="146" fill="#34d399" font-size="8.5">"message": "Order accepted",</text>
<text x="555" y="162" fill="#f43f5e" font-size="8.5">"request_id": "req-88f1a",</text>
<text x="555" y="178" fill="#cbd5e1" font-size="8.5">"trace": "projects/p/traces/..",</text>
<text x="555" y="194" fill="#cbd5e1" font-size="8.5">"service": "order-service",</text>
<text x="555" y="210" fill="#cbd5e1" font-size="8.5">"customer_id": "CUST-8802",</text>
<text x="555" y="226" fill="#cbd5e1" font-size="8.5">"total_cents": 1620,</text>
<text x="555" y="242" fill="#34d399" font-size="8.5">"latency_ms": 28.4</text>
<text x="550" y="258" fill="#94a3b8" font-size="8.5">}</text>

<!-- Flow Arrow: JSON to Cloud Logging -->
<path d="M740 185 L760 185" stroke="#38bdf8" stroke-width="2" marker-end="url(#day15-trace-arr)"/>

<!-- Column 4: Google Cloud Observability -->
<rect x="760" y="25" width="160" height="275" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/monitoring.svg" x="775" y="38" width="22" height="22"/>
<text x="805" y="52" fill="#38bdf8" font-size="12" font-weight="700">CLOUD SUITE</text>
<text x="805" y="68" fill="#94a3b8" font-size="9.5">Google Cloud Logging</text>

<rect x="775" y="85" width="130" height="55" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="785" y="104" fill="#38bdf8" font-size="9.5" font-weight="700">Instant Queries</text>
<text x="785" y="120" fill="#94a3b8" font-size="8">jsonPayload.request_id</text>
<text x="785" y="132" fill="#94a3b8" font-size="8">="req-88f1a"</text>

<rect x="775" y="150" width="130" height="55" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1"/>
<image href="../assets/icons/gcp/legacy/trace.svg" x="785" y="160" width="16" height="16"/>
<text x="805" y="170" fill="#34d399" font-size="9.5" font-weight="700">Cloud Trace</text>
<text x="785" y="186" fill="#94a3b8" font-size="8">Correlates spans</text>
<text x="785" y="198" fill="#cbd5e1" font-size="8">End-to-end latency</text>

<rect x="775" y="215" width="130" height="70" rx="4" fill="#1c2128" stroke="#f43f5e" stroke-width="1"/>
<image href="../assets/icons/gcp/legacy/error-reporting.svg" x="785" y="225" width="16" height="16"/>
<text x="805" y="235" fill="#f43f5e" font-size="9.5" font-weight="700">Error Grouping</text>
<text x="785" y="252" fill="#94a3b8" font-size="8">Auto-groups stack</text>
<text x="785" y="266" fill="#cbd5e1" font-size="8">Alerts on spike</text>
</svg>
</div>
<figcaption>Figure 15.2: End-to-end request tracing and structured logging architecture showing request ID propagation from edge ingress, Twelve-Factor unbuffered event streaming to stdout, and ingestion into Google Cloud Logging and Cloud Trace.</figcaption>
</figure>'''

# Figure 15.3: Monolithic Blast Radius Incident
FIG_15_3_HTML = '''<figure id="fig-15-3" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day15-blast-incident-title day15-blast-incident-desc" viewBox="0 0 940 280" width="940" height="280" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day15-blast-incident-title">Monolithic Blast Radius Failure and Decoupled Microservice Remediation</title>
<desc id="day15-blast-incident-desc">Incident diagram showing how a memory leak in an un-isolated PDF invoice module crashed an entire monolithic checkout process, and the corrected decoupled microservice architecture.</desc>

<!-- Fragile Monolith Flow (Red) -->
<rect x="20" y="25" width="430" height="230" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<text x="35" y="50" fill="#f43f5e" font-size="12" font-weight="700">MONOLITH BLAST RADIUS (Failure Path)</text>

<rect x="35" y="65" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">1. Client requests heavy batch PDF invoice generation</text>
<text x="45" y="98" fill="#f43f5e" font-size="8.5">Runs in same process memory space as core checkout engine</text>

<rect x="35" y="115" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">2. C-extension memory leak consumes 3.8 GB heap</text>
<text x="45" y="148" fill="#f43f5e" font-size="8.5">Linux kernel invokes Out-Of-Memory (OOM) killer; SIGKILL sent to PID 1</text>

<rect x="35" y="165" width="400" height="75" rx="4" fill="#1c2128" stroke="#f43f5e" stroke-width="1.2"/>
<text x="45" y="185" fill="#f43f5e" font-size="10" font-weight="700">Production Outage: Total System Halts</text>
<text x="45" y="202" fill="#cbd5e1" font-size="9">• Entire VM process terminates; drops 4,200 active TCP checkout sockets</text>
<text x="45" y="218" fill="#cbd5e1" font-size="9">• Zero orders processed for 35 minutes; $240,000 revenue blocked</text>
<text x="45" y="232" fill="#ef4444" font-size="8.5">Blast radius: 100% of e-commerce capabilities halted</text>

<!-- Decoupled Flow (Green) -->
<rect x="480" y="25" width="440" height="230" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<text x="495" y="50" fill="#34d399" font-size="12" font-weight="700">DECOUPLED SERVICE ISOLATION (Remediation)</text>

<rect x="495" y="65" width="410" height="42" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="505" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">1. Core checkout decoupled into stateless Cloud Run container</text>
<text x="505" y="98" fill="#38bdf8" font-size="8.5">Processes order, records payment, and emits Pub/Sub event</text>

<rect x="495" y="115" width="410" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1"/>
<text x="505" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">2. Invoicing isolated in asynchronous Cloud Run Job</text>
<text x="505" y="148" fill="#34d399" font-size="8.5">Runs in independent container cgroup; bounded to 1 GB limit</text>

<rect x="495" y="165" width="410" height="75" rx="4" fill="#1c2128" stroke="#34d399" stroke-width="1.2"/>
<text x="505" y="185" fill="#34d399" font-size="10" font-weight="700">Fault Domain Isolated: Zero Checkout Impact</text>
<text x="505" y="202" fill="#cbd5e1" font-size="9">• PDF worker OOM restarts independently without socket drops</text>
<text x="505" y="218" fill="#cbd5e1" font-size="9">• Core checkout maintains 100.0% availability throughout event</text>
<text x="505" y="232" fill="#34d399" font-size="8.5">Business outcome: Zero revenue lost; automatic job retry succeeds</text>
</svg>
</div>
<figcaption>Figure 15.3: Incident retrospective contrasting an un-isolated monolithic process where an ancillary PDF memory leak halts core checkout operations versus decoupled microservice boundaries isolating fault domains.</figcaption>
</figure>'''

# Figure 15.4: Unstructured Text vs Correlated JSON Logs Incident
FIG_15_4_HTML = '''<figure id="fig-15-4" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day15-logs-incident-title day15-logs-incident-desc" viewBox="0 0 940 280" width="940" height="280" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day15-logs-incident-title">Unstructured Text Logging Blindspot and Correlated JSON Trace Remediation</title>
<desc id="day15-logs-incident-desc">Incident diagram contrasting unsearchable plain-text logs during a high-concurrency checkout failure with structured JSON logs and request ID correlation enabling rapid sub-minute diagnosis.</desc>

<!-- Fragile Plain-Text Logs (Red) -->
<rect x="20" y="25" width="430" height="230" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<text x="35" y="50" fill="#f43f5e" font-size="12" font-weight="700">UNSTRUCTURED LOG BLINDSPOT (Failure)</text>

<rect x="35" y="65" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">1. Concurrent orders hit database connection pool limit</text>
<text x="45" y="98" fill="#f43f5e" font-size="8.5">Services write plain text strings: "Error: connection timeout"</text>

<rect x="35" y="115" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">2. Interleaved plain text logs across 40 container nodes</text>
<text x="45" y="148" fill="#f43f5e" font-size="8.5">Missing Request ID, missing customer ID, missing timestamp tz</text>

<rect x="35" y="165" width="400" height="75" rx="4" fill="#1c2128" stroke="#f43f5e" stroke-width="1.2"/>
<text x="45" y="185" fill="#f43f5e" font-size="10" font-weight="700">Diagnostic Impairment: 75-Minute MTTR</text>
<text x="45" y="202" fill="#cbd5e1" font-size="9">• Engineers execute manual regex greps across disparate text files</text>
<text x="45" y="218" fill="#cbd5e1" font-size="9">• Cannot correlate which specific customer requests failed</text>
<text x="45" y="232" fill="#ef4444" font-size="8.5">Mean Time To Resolution: 75 minutes of customer degradation</text>

<!-- Structured JSON Logs (Green) -->
<rect x="480" y="25" width="440" height="230" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<text x="495" y="50" fill="#34d399" font-size="12" font-weight="700">STRUCTURED JSON &amp; REQUEST IDS (Remediation)</text>

<rect x="495" y="65" width="410" height="42" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="505" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">1. Middleware attaches X-Request-Id &amp; W3C traceparent</text>
<text x="505" y="98" fill="#38bdf8" font-size="8.5">Injected into all outbound RPCs and context loggers</text>

<rect x="495" y="115" width="410" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1"/>
<text x="505" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">2. Emits RFC 8259 structured JSON to stdout stream</text>
<text x="505" y="148" fill="#34d399" font-size="8.5">Google Cloud Logging indexes request_id, severity, latency automatically</text>

<rect x="495" y="165" width="410" height="75" rx="4" fill="#1c2128" stroke="#34d399" stroke-width="1.2"/>
<text x="505" y="185" fill="#34d399" font-size="10" font-weight="700">Rapid Diagnosis: Sub-Minute MTTR</text>
<text x="505" y="202" fill="#cbd5e1" font-size="9">• Query: jsonPayload.request_id="req-9102" returns complete trace</text>
<text x="505" y="218" fill="#cbd5e1" font-size="9">• Root cause connection pool saturation isolated in 90 seconds</text>
<text x="505" y="232" fill="#34d399" font-size="8.5">Pool size increased; service restored with minimal customer impact</text>
</svg>
</div>
<figcaption>Figure 15.4: Incident analysis showing how unsearchable unstructured plain-text logs delay root cause analysis during production outages, contrasted with structured JSON logs and Request ID propagation enabling sub-minute query resolution.</figcaption>
</figure>'''
