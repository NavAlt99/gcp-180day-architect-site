"""Day 14 Overview and SVG Diagram Definitions."""

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'Pro Git (2nd Edition) — Chapter 3.2: Git Branching - Basic Branching and Merging (accessed 2026-10-04)',
        'https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging#_basic_branching_and_merging'
    ),
    'topic-02': (
        'RFC 9110: HTTP Semantics — Section 9.3: Method Definitions (accessed 2026-10-04)',
        'https://www.rfc-editor.org/rfc/rfc9110#section-9.3'
    )
}

PART1_HTML = '''<article class="topic-card overview" id="topic-01-overview">
<h3>Git fundamentals (branch, merge, PR)</h3>
<p><strong class="keyword">Distributed version control</strong> forms the bedrock of modern infrastructure and software engineering. Git models source history as an immutable Directed Acyclic Graph (DAG) of snapshot commits, where branches operate as lightweight, movable pointers to specific cryptographic hashes. Pull Requests (PRs) enforce collaborative peer review, automated continuous integration (CI) test execution, and compliance policies before code merges into protected trunk branches. Understanding branching topology, fast-forward versus three-way merge semantics, and pull request gating separates reliable enterprise engineering from error-prone ad-hoc deployments.</p>
<p><strong class="side-heading">Why today:</strong> Unreviewed direct commits to trunk branches frequently push broken schema definitions and syntax errors directly to production, bypassing automated validation gates.</p>
<p><strong class="side-heading">Where it sits:</strong> Sits at the inception of the cloud delivery pipeline, anchoring GitOps automation, Terraform infrastructure management, and Cloud Build CI/CD triggers.</p>
<p class="problem-preview">Problem preview: A developer pushes an unvalidated direct commit to the production main branch, inadvertently altering the JSON attribute naming convention in an API contract. Because the commit bypassed pull request CI test gates, 1,200 downstream microservice instances crash upon deployment, generating an emergency P1 outage.</p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>REST APIs and JSON</h3>
<p><strong class="keyword">Representational State Transfer (REST)</strong> and JavaScript Object Notation (JSON) establish the universal protocol language of modern distributed cloud systems. Governed by RFC 9110 HTTP semantics and RFC 8259 data interchange standards, REST APIs decouple clients from servers through standardized HTTP methods (GET, POST, PUT, DELETE), resource-oriented URI hierarchies, and self-describing JSON payloads. Defensive client engineering requires strict status code handling, content-type negotiation, and resilient error recovery when upstream proxies emit unexpected HTML error responses.</p>
<p><strong class="side-heading">Why today:</strong> Cloud architects integrate dozens of disparate microservices, third-party payment gateways, and Google Cloud management APIs using REST/JSON; fragile contract assumptions lead directly to cascading runtime failures.</p>
<p><strong class="side-heading">Where it sits:</strong> Directs service-to-service communication across Cloud Run, GKE, API Gateway, and Cloud Functions, dictating payload contracts, error models, and retry invariants.</p>
<p class="problem-preview">Problem preview: An upstream cloud load balancer encounters transient backend exhaustion and returns a 502 Bad Gateway response with an HTML error body. An downstream order-processing service assumes every response contains JSON and attempts to parse the HTML, crashing with an unhandled parser exception and triggering an uncontrolled retry storm that double-bills 340 customer accounts.</p>
</article>'''

# Figure 14.1: Git Branching & CI Lifecycle
FIG_14_1_HTML = '''<figure id="fig-14-1" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day14-fig1-title day14-fig1-desc" viewBox="0 0 940 330" width="940" height="330" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day14-fig1-title">Git Branching, Pull Request Review Lifecycle, and GitOps CI/CD Integration</title>
<desc id="day14-fig1-desc">Architectural diagram illustrating feature branch divergence from main, automated Cloud Build CI test gates, peer code review, non-fast-forward merge integration, and deployment triggers.</desc>
<defs>
<marker id="day14-git-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day14-merge-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#34d399"/></marker>
<marker id="day14-ci-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#fbbf24"/></marker>
</defs>

<!-- Main Trunk Line -->
<rect x="20" y="25" width="430" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/policy.svg" x="35" y="38" width="22" height="22"/>
<text x="70" y="54" fill="#38bdf8" font-size="12" font-weight="700">MAIN BRANCH (PROTECTED TRUNK)</text>
<text x="70" y="70" fill="#94a3b8" font-size="9.5">Production release artifact source of truth</text>

<!-- Main Commits -->
<circle cx="70" cy="90" r="13" fill="#21262d" stroke="#38bdf8" stroke-width="2"/>
<text x="70" y="94" fill="#38bdf8" font-size="9.5" font-weight="700" text-anchor="middle">C0</text>
<text x="70" y="112" fill="#94a3b8" font-size="8" text-anchor="middle">Init</text>

<circle cx="170" cy="90" r="13" fill="#21262d" stroke="#38bdf8" stroke-width="2"/>
<text x="170" y="94" fill="#38bdf8" font-size="9.5" font-weight="700" text-anchor="middle">C1</text>
<text x="170" y="112" fill="#94a3b8" font-size="8" text-anchor="middle">Base API</text>

<circle cx="370" cy="90" r="15" fill="#21262d" stroke="#34d399" stroke-width="2.5"/>
<text x="370" y="94" fill="#34d399" font-size="9.5" font-weight="700" text-anchor="middle">C4</text>
<text x="370" y="112" fill="#34d399" font-size="8" text-anchor="middle">Merge PR</text>

<path d="M83 90 L157 90" stroke="#38bdf8" stroke-width="2" marker-end="url(#day14-git-arrow)"/>
<path d="M183 90 L355 90" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#day14-git-arrow)"/>

<!-- Feature Branch Line -->
<rect x="20" y="145" width="430" height="155" rx="8" fill="#161b22" stroke="#eab308" stroke-width="2"/>
<text x="35" y="168" fill="#eab308" font-size="12" font-weight="700">FEATURE BRANCH: feature/order-tax</text>
<text x="35" y="184" fill="#94a3b8" font-size="9.5">Isolated developer development &amp; schema iteration</text>

<circle cx="170" cy="225" r="13" fill="#21262d" stroke="#eab308" stroke-width="2"/>
<text x="170" y="229" fill="#eab308" font-size="9.5" font-weight="700" text-anchor="middle">C2</text>
<text x="170" y="248" fill="#94a3b8" font-size="8" text-anchor="middle">+Tax field</text>

<circle cx="280" cy="225" r="13" fill="#21262d" stroke="#eab308" stroke-width="2"/>
<text x="280" y="229" fill="#eab308" font-size="9.5" font-weight="700" text-anchor="middle">C3</text>
<text x="280" y="248" fill="#94a3b8" font-size="8" text-anchor="middle">Unit tests</text>

<!-- Divergence & Convergence -->
<path d="M170 103 L170 212" stroke="#eab308" stroke-width="2" marker-end="url(#day14-git-arrow)"/>
<path d="M183 225 L267 225" stroke="#eab308" stroke-width="2" marker-end="url(#day14-git-arrow)"/>
<path d="M293 225 L370 105" stroke="#34d399" stroke-width="2.5" marker-end="url(#day14-merge-arrow)"/>
<text x="355" y="180" fill="#34d399" font-size="9" font-weight="600">Merge (--no-ff)</text>

<!-- Pull Request & CI Gates -->
<rect x="475" y="25" width="230" height="275" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/decision.svg" x="490" y="38" width="22" height="22"/>
<text x="520" y="54" fill="#34d399" font-size="12" font-weight="700">PULL REQUEST GATES</text>
<text x="520" y="70" fill="#94a3b8" font-size="9.5">Pre-Merge Validation Protocol</text>

<rect x="490" y="85" width="200" height="45" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<text x="500" y="104" fill="#fce7f3" font-size="10" font-weight="600">1. Automated Lint &amp; Test</text>
<text x="500" y="120" fill="#94a3b8" font-size="9">pytest + JSON schema validation</text>

<rect x="490" y="140" width="200" height="45" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<text x="500" y="159" fill="#fce7f3" font-size="10" font-weight="600">2. Peer Code Review</text>
<text x="500" y="175" fill="#94a3b8" font-size="9">Minimum 1 senior architect approval</text>

<rect x="490" y="195" width="200" height="45" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<text x="500" y="214" fill="#fce7f3" font-size="10" font-weight="600">3. Branch Protection</text>
<text x="500" y="230" fill="#94a3b8" font-size="9">Direct push to main disabled</text>

<rect x="490" y="250" width="200" height="38" rx="4" fill="#1c2128" stroke="#34d399" stroke-width="1"/>
<text x="590" y="272" fill="#34d399" font-size="9.5" font-weight="700" text-anchor="middle">✓ Status Check Required</text>

<!-- Cloud Build & Deployment -->
<rect x="730" y="25" width="190" height="275" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/gcp/legacy/cloud-build.svg" x="745" y="38" width="24" height="24"/>
<text x="775" y="54" fill="#38bdf8" font-size="12" font-weight="700">GITOPS CI/CD</text>
<text x="775" y="70" fill="#94a3b8" font-size="9.5">Google Cloud Build</text>

<rect x="745" y="85" width="160" height="50" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="755" y="105" fill="#fce7f3" font-size="10" font-weight="600">Build Trigger</text>
<text x="755" y="122" fill="#94a3b8" font-size="8.5">On push to main branch</text>

<rect x="745" y="145" width="160" height="50" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<image href="../assets/icons/gcp/core/cloud-run.svg" x="755" y="157" width="18" height="18"/>
<text x="780" y="167" fill="#fce7f3" font-size="10" font-weight="600">Artifact Registry</text>
<text x="780" y="182" fill="#94a3b8" font-size="8.5">Container image build</text>

<rect x="745" y="205" width="160" height="50" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1"/>
<text x="755" y="225" fill="#fce7f3" font-size="10" font-weight="600">Cloud Run Deploy</text>
<text x="755" y="242" fill="#34d399" font-size="8.5">Automated release</text>

<path d="M705 90 L725 90" stroke="#38bdf8" stroke-width="2" marker-end="url(#day14-ci-arrow)"/>
</svg>
</div>
<figcaption>Figure 14.1: Git branching and Pull Request lifecycle showing isolated feature branch development, automated CI test gates, peer review approvals, non-fast-forward merge to protected main, and automated Cloud Build deployment.</figcaption>
</figure>'''

# Figure 14.2: REST API & JSON Lifecycle
FIG_14_2_HTML = '''<figure id="fig-14-2" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day14-fig2-title day14-fig2-desc" viewBox="0 0 940 330" width="940" height="330" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day14-fig2-title">RESTful HTTP/JSON Request-Response Lifecycle, Status Codes, and Idempotency Gateway</title>
<desc id="day14-fig2-desc">Architectural diagram illustrating RESTful client-server communication over HTTP/JSON, schema validation, HTTP methods, status code semantics, and defensive error parsing.</desc>
<defs>
<marker id="day14-req-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day14-res-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#34d399"/></marker>
<marker id="day14-err-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"/></marker>
</defs>

<!-- Column 1: Client Layer -->
<rect x="20" y="25" width="220" height="275" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/load-balancer.svg" x="35" y="38" width="22" height="22"/>
<text x="65" y="54" fill="#38bdf8" font-size="12" font-weight="700">REST API CLIENT</text>
<text x="65" y="70" fill="#94a3b8" font-size="9.5">Frontend App / Microservice</text>

<rect x="35" y="85" width="190" height="60" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<text x="45" y="104" fill="#fce7f3" font-size="10" font-weight="600">RFC 9110 Methods</text>
<text x="45" y="120" fill="#94a3b8" font-size="8.5">• GET (Safe, Idempotent)</text>
<text x="45" y="134" fill="#94a3b8" font-size="8.5">• POST / PUT / DELETE</text>

<rect x="35" y="155" width="190" height="65" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<text x="45" y="174" fill="#fce7f3" font-size="10" font-weight="600">Defensive Client Invariant</text>
<text x="45" y="190" fill="#34d399" font-size="8.5">• Check Content-Type header</text>
<text x="45" y="204" fill="#34d399" font-size="8.5">• Supply Idempotency-Key</text>

<rect x="35" y="230" width="190" height="55" rx="4" fill="#1c2128" stroke="#475569" stroke-width="1"/>
<text x="45" y="249" fill="#cbd5e1" font-size="9.5">Payload Serializer</text>
<text x="45" y="266" fill="#94a3b8" font-size="8.5">RFC 8259 JSON encoder/decoder</text>

<!-- Column 2: Gateway Layer -->
<rect x="260" y="25" width="240" height="275" rx="8" fill="#161b22" stroke="#eab308" stroke-width="2"/>
<image href="../assets/icons/gcp/legacy/cloud-api-gateway.svg" x="275" y="38" width="24" height="24"/>
<text x="305" y="54" fill="#eab308" font-size="12" font-weight="700">API GATEWAY</text>
<text x="305" y="70" fill="#94a3b8" font-size="9.5">Perimeter Security &amp; Routing</text>

<rect x="275" y="85" width="210" height="55" rx="4" fill="#21262d" stroke="#eab308" stroke-width="1.2"/>
<text x="285" y="104" fill="#fce7f3" font-size="10" font-weight="600">Schema Validation</text>
<text x="285" y="120" fill="#94a3b8" font-size="8.5">Rejects malformed JSON: 400 Bad Req</text>
<text x="285" y="132" fill="#ef4444" font-size="8.5">Stops invalid payloads at perimeter</text>

<rect x="275" y="150" width="210" height="55" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<text x="285" y="169" fill="#fce7f3" font-size="10" font-weight="600">Authentication &amp; Rate Limit</text>
<text x="285" y="185" fill="#94a3b8" font-size="8.5">JWT token verification (401 / 403)</text>
<text x="285" y="198" fill="#94a3b8" font-size="8.5">Token-bucket quota (429 Too Many Req)</text>

<rect x="275" y="215" width="210" height="70" rx="4" fill="#1c2128" stroke="#34d399" stroke-width="1"/>
<text x="285" y="234" fill="#34d399" font-size="10" font-weight="600">Idempotency Filter</text>
<text x="285" y="250" fill="#cbd5e1" font-size="8.5">Caches POST Idempotency-Key</text>
<text x="285" y="264" fill="#34d399" font-size="8.5">Prevents duplicate transaction processing</text>

<!-- Flow Arrows: Client to Gateway -->
<path d="M240 115 L260 115" stroke="#38bdf8" stroke-width="2" marker-end="url(#day14-req-arr)"/>
<path d="M260 175 L240 175" stroke="#34d399" stroke-width="2" marker-end="url(#day14-res-arr)"/>

<!-- Column 3: Backend Service -->
<rect x="520" y="25" width="210" height="275" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-run.svg" x="535" y="38" width="22" height="22"/>
<text x="565" y="54" fill="#34d399" font-size="12" font-weight="700">BACKEND SERVICE</text>
<text x="565" y="70" fill="#94a3b8" font-size="9.5">Cloud Run / Microservice</text>

<rect x="535" y="85" width="180" height="60" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<text x="545" y="104" fill="#fce7f3" font-size="10" font-weight="600">Business Logic</text>
<text x="545" y="120" fill="#94a3b8" font-size="8.5">Executes ACID transactions</text>
<text x="545" y="134" fill="#34d399" font-size="8.5">Returns 200 OK / 201 Created</text>

<rect x="535" y="155" width="180" height="60" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1.2"/>
<text x="545" y="174" fill="#fce7f3" font-size="10" font-weight="600">Structured Error Model</text>
<text x="545" y="190" fill="#f43f5e" font-size="8.5">Google API Design Standard</text>
<text x="545" y="204" fill="#94a3b8" font-size="8.5">error: {code, message, status}</text>

<rect x="535" y="225" width="180" height="60" rx="4" fill="#1c2128" stroke="#475569" stroke-width="1"/>
<text x="545" y="244" fill="#cbd5e1" font-size="9.5">JSON Serialization</text>
<text x="545" y="260" fill="#94a3b8" font-size="8.5">Sets Content-Type: application/json</text>
<text x="545" y="274" fill="#34d399" font-size="8.5">Includes correlation request_id</text>

<!-- Flow Arrows: Gateway to Backend -->
<path d="M500 115 L520 115" stroke="#38bdf8" stroke-width="2" marker-end="url(#day14-req-arr)"/>
<path d="M520 175 L500 175" stroke="#34d399" stroke-width="2" marker-end="url(#day14-res-arr)"/>

<!-- Column 4: Status Code & Error Taxonomy -->
<rect x="750" y="25" width="170" height="275" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<text x="765" y="52" fill="#38bdf8" font-size="12" font-weight="700">STATUS TAXONOMY</text>
<text x="765" y="68" fill="#94a3b8" font-size="9.5">RFC 9110 Response Classes</text>

<rect x="765" y="85" width="140" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1"/>
<text x="775" y="102" fill="#34d399" font-size="10" font-weight="700">2xx Success</text>
<text x="775" y="118" fill="#94a3b8" font-size="8.5">200 OK, 201 Created, 204</text>

<rect x="765" y="135" width="140" height="42" rx="4" fill="#21262d" stroke="#eab308" stroke-width="1"/>
<text x="775" y="152" fill="#eab308" font-size="10" font-weight="700">4xx Client Error</text>
<text x="775" y="168" fill="#94a3b8" font-size="8.5">400, 401, 403, 404, 429</text>

<rect x="765" y="185" width="140" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="775" y="202" fill="#f43f5e" font-size="10" font-weight="700">5xx Server Error</text>
<text x="775" y="218" fill="#94a3b8" font-size="8.5">500 Internal, 502, 503</text>

<rect x="765" y="235" width="140" height="50" rx="4" fill="#1c2128" stroke="#f43f5e" stroke-width="1"/>
<text x="775" y="252" fill="#f43f5e" font-size="9" font-weight="700">⚠ Non-JSON 502/503</text>
<text x="775" y="266" fill="#94a3b8" font-size="8">HTML body from proxy;</text>
<text x="775" y="278" fill="#34d399" font-size="8">Must check Content-Type!</text>
</svg>
</div>
<figcaption>Figure 14.2: RESTful API and JSON request-response architecture illustrating RFC 9110 HTTP method semantics, API Gateway schema enforcement, status code classes (2xx, 4xx, 5xx), and defensive non-JSON error handling.</figcaption>
</figure>'''

# Figure 14.3: Incident 1 - Direct Commit to Main
FIG_14_3_HTML = '''<figure id="fig-14-3" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day14-fig3-title day14-fig3-desc" viewBox="0 0 940 280" width="940" height="280" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day14-fig3-title">Direct Commit to Main Failure and Protected Branch PR Remediation</title>
<desc id="day14-fig3-desc">Sequence diagram illustrating an unreviewed direct commit to main breaking production JSON schemas, contrasted with protected branch and PR gating remediation.</desc>

<!-- Step 1: Failed Flow (Red) -->
<rect x="20" y="25" width="430" height="230" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<text x="35" y="50" fill="#f43f5e" font-size="12" font-weight="700">UNREVIEWED COMMIT FAILURE (Root Cause)</text>

<rect x="35" y="65" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">1. Developer executes git push origin main directly</text>
<text x="45" y="98" fill="#f43f5e" font-size="8.5">Bypasses code review and CI automated test suite</text>

<rect x="35" y="115" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">2. Breaking schema change: orderId renamed to id</text>
<text x="45" y="148" fill="#f43f5e" font-size="8.5">Silently breaks JSON contract with downstream microservices</text>

<rect x="35" y="165" width="400" height="75" rx="4" fill="#1c2128" stroke="#f43f5e" stroke-width="1.2"/>
<text x="45" y="185" fill="#f43f5e" font-size="10" font-weight="700">Production Impact: P1 Outage</text>
<text x="45" y="202" fill="#cbd5e1" font-size="9">• 1,200 microservice containers throw KeyError: 'orderId'</text>
<text x="45" y="218" fill="#cbd5e1" font-size="9">• HTTP 500 Internal Server Errors; 8,500 checkouts blocked</text>
<text x="45" y="232" fill="#ef4444" font-size="8.5">Downtime duration: 45 minutes; $320,000 lost revenue</text>

<!-- Step 2: Remediated Flow (Green) -->
<rect x="480" y="25" width="440" height="230" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<text x="495" y="50" fill="#34d399" font-size="12" font-weight="700">PROTECTED BRANCH &amp; PR GATES (Architectural Fix)</text>

<rect x="495" y="65" width="410" height="42" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="505" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">1. Feature branch created: git checkout -b feature/order-schema</text>
<text x="505" y="98" fill="#38bdf8" font-size="8.5">Isolated developer development without trunk risk</text>

<rect x="495" y="115" width="410" height="42" rx="4" fill="#21262d" stroke="#eab308" stroke-width="1"/>
<text x="505" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">2. Pull Request submitted; Cloud Build runs pytest</text>
<text x="505" y="148" fill="#eab308" font-size="8.5">CI catches breaking field rename; PR blocked automatically</text>

<rect x="495" y="165" width="410" height="75" rx="4" fill="#1c2128" stroke="#34d399" stroke-width="1.2"/>
<text x="505" y="185" fill="#34d399" font-size="10" font-weight="700">Remediated Outcome: Zero Production Outages</text>
<text x="505" y="202" fill="#cbd5e1" font-size="9">• Contract breaking changes caught before merge</text>
<text x="505" y="218" fill="#cbd5e1" font-size="9">• Branch protection policy legally blocks direct pushes</text>
<text x="505" y="232" fill="#34d399" font-size="8.5">Production availability: 100% maintained; 0 error impact</text>
</svg>
</div>
<figcaption>Figure 14.3: Incident retrospective contrasting an unreviewed direct commit to main causing production API schema breakage versus branch protection policies and automated Cloud Build PR gates catching defects before merge.</figcaption>
</figure>'''

# Figure 14.4: Incident 2 - Malformed JSON Error Handling
FIG_14_4_HTML = '''<figure id="fig-14-4" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day14-fig4-title day14-fig4-desc" viewBox="0 0 940 280" width="940" height="280" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day14-fig4-title">Malformed JSON Error Handling Failure and Idempotent REST Gateway Remediation</title>
<desc id="day14-fig4-desc">Sequence diagram illustrating an upstream non-JSON 502 Bad Gateway response crashing an API client parser and causing duplicate billing, contrasted with defensive Content-Type checking and Idempotency-Key headers.</desc>

<!-- Fragile Path (Red) -->
<rect x="20" y="25" width="430" height="230" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<text x="35" y="50" fill="#f43f5e" font-size="12" font-weight="700">FRAGILE PARSER &amp; RETRY STORM (Failure)</text>

<rect x="35" y="65" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">1. Upstream LB emits HTTP 502 with HTML body</text>
<text x="45" y="98" fill="#f43f5e" font-size="8.5">&lt;html&gt;&lt;body&gt;502 Bad Gateway&lt;/body&gt;&lt;/html&gt;</text>

<rect x="35" y="115" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">2. Client runs json.loads(response.text) unconditionally</text>
<text x="45" y="148" fill="#f43f5e" font-size="8.5">json.decoder.JSONDecodeError crashes worker thread</text>

<rect x="35" y="165" width="400" height="75" rx="4" fill="#1c2128" stroke="#f43f5e" stroke-width="1.2"/>
<text x="45" y="185" fill="#f43f5e" font-size="10" font-weight="700">Double Billing Impact</text>
<text x="45" y="202" fill="#cbd5e1" font-size="9">• Unhandled crash aborts transaction acknowledgement</text>
<text x="45" y="218" fill="#cbd5e1" font-size="9">• Upstream scheduler retries payment without Idempotency-Key</text>
<text x="45" y="232" fill="#ef4444" font-size="8.5">340 customer cards double-charged ($68,000 unauthorized)</text>

<!-- Defensive Path (Green) -->
<rect x="480" y="25" width="440" height="230" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<text x="495" y="50" fill="#34d399" font-size="12" font-weight="700">DEFENSIVE CLIENT &amp; IDEMPOTENCY (Remediation)</text>

<rect x="495" y="65" width="410" height="42" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="505" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">1. Client inspects Content-Type &amp; HTTP status code</text>
<text x="505" y="98" fill="#38bdf8" font-size="8.5">Detects text/html; wraps response in standard GatewayError</text>

<rect x="495" y="115" width="410" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1"/>
<text x="505" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">2. Request supplies Idempotency-Key: &lt;uuid&gt; header</text>
<text x="505" y="148" fill="#34d399" font-size="8.5">Payment gateway enforces exactly-once transaction fulfillment</text>

<rect x="495" y="165" width="410" height="75" rx="4" fill="#1c2128" stroke="#34d399" stroke-width="1.2"/>
<text x="505" y="185" fill="#34d399" font-size="10" font-weight="700">Remediated Invariant: Zero Duplicate Charges</text>
<text x="505" y="202" fill="#cbd5e1" font-size="9">• Non-JSON errors handled gracefully without thread crashes</text>
<text x="505" y="218" fill="#cbd5e1" font-size="9">• Retries recognized by gateway; returns original authorization</text>
<text x="505" y="232" fill="#34d399" font-size="8.5">Fulfillment invariant: Exactly 1 payment captured per order</text>
</svg>
</div>
<figcaption>Figure 14.4: Incident analysis showing how blind JSON deserialization of non-JSON HTML 502 responses causes parser crashes and duplicate payments, remediated by defensive Content-Type checking and Idempotency-Key headers.</figcaption>
</figure>'''
