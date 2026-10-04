"""Base definitions, figures, and architecture topology for Day 10: Images, filesystems and orchestration."""

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        f'fsync(2) Linux file data synchronization description (accessed {ACCESS_DATE})',
        'https://man7.org/linux/man-pages/man2/fsync.2.html#DESCRIPTION'
    ),
    'topic-02': (
        f'Why you need Kubernetes and what it can do (accessed {ACCESS_DATE})',
        'https://kubernetes.io/docs/concepts/overview/#why-you-need-kubernetes-and-what-can-it-do'
    ),
    'topic-03': (
        f'Understanding Kubernetes objects (accessed {ACCESS_DATE})',
        'https://kubernetes.io/docs/concepts/overview/working-with-objects/#kubernetes-objects'
    )
}

FIG_10_1_HTML = '''<figure class="diagram-figure">
<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>
<svg aria-labelledby="day10-storage-title day10-storage-desc" role="img" viewbox="0 0 940 330">
<title id="day10-storage-title">Docker container storage architecture and POSIX write durability path</title>
<desc id="day10-storage-desc">The diagram illustrates container storage layers on the left and the POSIX write durability pipeline from process memory down to non-volatile storage on the right.</desc>
<defs>
<marker id="day10-storage-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>
</defs>
<g fill="#121526" stroke-width="2">
<rect height="45" rx="6" stroke="#f43f5e" width="420" x="20" y="65"></rect>
<image href="../assets/icons/generic/failure.svg" x="28" y="73" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="45" rx="6" stroke="#f97316" width="420" x="20" y="115"></rect>
<image href="../assets/icons/generic/artifact.svg" x="28" y="123" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="45" rx="6" stroke="#38bdf8" width="420" x="20" y="165"></rect>
<image href="../assets/icons/generic/storage.svg" x="28" y="173" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="55" rx="6" stroke="#34d399" width="420" x="20" y="220"></rect>
<image href="../assets/icons/generic/storage.svg" x="28" y="233" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="45" rx="6" stroke="#38bdf8" width="400" x="495" y="65"></rect>
<image href="../assets/icons/generic/endpoint.svg" x="503" y="73" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="45" rx="6" stroke="#f97316" width="400" x="495" y="115"></rect>
<image href="../assets/icons/generic/server.svg" x="503" y="123" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="45" rx="6" stroke="#f43f5e" width="400" x="495" y="165"></rect>
<image href="../assets/icons/generic/storage.svg" x="503" y="173" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="45" rx="6" stroke="#34d399" width="400" x="495" y="225"></rect>
<image href="../assets/icons/generic/storage.svg" x="503" y="233" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
</g>
<g fill="#fce7f3" font-size="12" font-weight="700" text-anchor="middle">
<text x="235" y="52">CONTAINER STORAGE LAYERS</text>
<text fill="#f43f5e" x="245" y="93">Thin Writable Layer (Ephemeral · Deleted on exit)</text>
<text fill="#f97316" x="245" y="143">Application Layer (Read-Only · e.g., app.py)</text>
<text fill="#38bdf8" x="245" y="193">Base Image Layer (Read-Only · e.g., python:3.12-alpine)</text>
<text fill="#34d399" x="245" y="252">Persistent Volume Mount (/data -&gt; durable storage)</text>
<text x="705" y="52">POSIX WRITE &amp; DURABILITY PIPELINE</text>
<text fill="#38bdf8" x="710" y="91">1. Process Heap &amp; Runtime Buffer (Volatile RAM)</text>
<text fill="#f97316" x="710" y="141">2. Linux OS Page Cache (Transferred via flush())</text>
<text fill="#f43f5e" x="710" y="191">3. Disk Controller Cache (Issued via fsync() syscall)</text>
<text fill="#34d399" x="710" y="251">4. Non-Volatile Physical Storage Blocks (Durable Commit)</text>
</g>
<g fill="none" marker-end="url(#day10-storage-arrow)" stroke="#38bdf8" stroke-width="2">
<path d="M695 100 L695 113"></path>
<path d="M695 150 L695 163"></path>
<path d="M695 200 L695 223"></path>
</g>
<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="305">Ephemeral container storage vanishes on pod deletion; only fsync() on mounted volumes guarantees persistence.</text>
</svg>
<figcaption>Figure 10.1: Architecture of container image layers, ephemeral overlay storage, and the operating system write durability path. Only data flushed via fsync() to mounted volumes survives container replacement.</figcaption>
</figure>'''

FIG_10_2_HTML = '''<figure class="diagram-figure">
<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>
<svg aria-labelledby="day10-reconcile-title day10-reconcile-desc" role="img" viewbox="0 0 940 300">
<title id="day10-reconcile-title">Kubernetes declarative control loop and reconciliation architecture</title>
<desc id="day10-reconcile-desc">The diagram illustrates the continuous reconciliation loop between desired state in etcd, the controller manager, the scheduler, and kubelet agents on worker nodes.</desc>
<defs>
<marker id="day10-reconcile-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>
</defs>
<g fill="#121526" stroke-width="2">
<rect height="220" rx="10" stroke="#38bdf8" width="200" x="20" y="35"></rect>
<image href="../assets/icons/generic/server.svg" x="28" y="45" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
<rect height="220" rx="10" stroke="#f97316" width="200" x="250" y="35"></rect>
<image href="../assets/icons/generic/decision.svg" x="258" y="45" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
<rect height="220" rx="10" stroke="#eab308" width="200" x="480" y="35"></rect>
<image href="../assets/icons/generic/monitoring.svg" x="488" y="45" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
<rect height="220" rx="10" stroke="#34d399" width="210" x="710" y="35"></rect>
<image href="../assets/icons/gcp/core/gke.svg" x="718" y="45" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
</g>
<g fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">
<text x="125" y="65">1. Control Plane</text>
<text x="355" y="65">2. Controllers</text>
<text x="585" y="65">3. Scheduler</text>
<text x="820" y="65">4. Worker Nodes</text>
</g>
<g fill="#a9b7cb" font-size="11" text-anchor="middle">
<text fill="#38bdf8" x="120" y="95">kube-apiserver</text>
<text x="120" y="120">etcd Data Store</text>
<text x="120" y="145">Stores Desired State</text>
<text x="120" y="170">(e.g., replicas: 3)</text>
<text fill="#fce7f3" x="120" y="210">Authoritative Spec</text>
<text fill="#f97316" x="350" y="95">controller-manager</text>
<text x="350" y="120">Deployment Loop</text>
<text x="350" y="145">Compares Desired vs Actual</text>
<text x="350" y="170">Creates Missing Pods</text>
<text fill="#fce7f3" x="350" y="210">Reconciliation Engine</text>
<text fill="#eab308" x="580" y="95">kube-scheduler</text>
<text x="580" y="120">Filters Node Capacity</text>
<text x="580" y="145">Evaluates CPU / RAM</text>
<text x="580" y="170">Assigns Pod to Node</text>
<text fill="#fce7f3" x="580" y="210">Placement Decision</text>
<text fill="#34d399" x="815" y="95">kubelet &amp; CRI</text>
<text x="815" y="120">Pulls Image &amp; Starts Pod</text>
<text x="815" y="145">Executes Health Probes</text>
<text x="815" y="170">Reports Status to API</text>
<text fill="#fce7f3" x="815" y="210">Observed Actual State</text>
</g>
<g fill="none" marker-end="url(#day10-reconcile-arrow)" stroke="#38bdf8" stroke-width="2">
<path d="M220 145 L246 145"></path>
<path d="M450 145 L476 145"></path>
<path d="M680 145 L706 145"></path>
<path d="M815 235 L815 270 L120 270 L120 258"></path>
</g>
<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="285">Continuous feedback loop: actual node telemetry reconciles against declared desired state in etcd.</text>
</svg>
<figcaption>Figure 10.2: Declarative reconciliation loop in Kubernetes. The control plane watches declared desired state, detects divergence, calculates placement across worker nodes, and executes autonomous convergence.</figcaption>
</figure>'''

FIG_10_3_HTML = '''<figure class="diagram-figure">
<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>
<svg aria-labelledby="day10-objects-title day10-objects-desc" role="img" viewbox="0 0 940 320">
<title id="day10-objects-title">Kubernetes core object relationships and traffic routing path</title>
<desc id="day10-objects-desc">The diagram traces request traffic from external clients through Ingress and Service selectors down to backend Pods mounting ConfigMaps and Secrets.</desc>
<defs>
<marker id="day10-objects-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>
</defs>
<g fill="#121526" stroke-width="2">
<rect height="240" rx="10" stroke="#38bdf8" width="160" x="20" y="35"></rect>
<image href="../assets/icons/generic/load-balancer.svg" x="28" y="45" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
<rect height="240" rx="10" stroke="#f97316" width="200" x="210" y="35"></rect>
<image href="../assets/icons/generic/router.svg" x="218" y="45" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
<rect height="240" rx="10" stroke="#34d399" width="230" x="440" y="35"></rect>
<image href="../assets/icons/generic/endpoint.svg" x="448" y="45" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
<rect height="240" rx="10" stroke="#eab308" width="220" x="700" y="35"></rect>
<image href="../assets/icons/generic/policy.svg" x="708" y="45" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
</g>
<g fill="#fce7f3" font-size="12" font-weight="700" text-anchor="middle">
<text x="105" y="65">Ingress Layer</text>
<text x="315" y="65">Service Abstraction</text>
<text x="560" y="65">Deployment &amp; Pods</text>
<text x="815" y="65">Config &amp; Secrets</text>
</g>
<g fill="#a9b7cb" font-size="11" text-anchor="middle">
<text fill="#38bdf8" x="100" y="95">Ingress Controller</text>
<text x="100" y="120">HTTP /orders Route</text>
<text x="100" y="145">TLS Termination</text>
<text x="100" y="170">Routes to Service</text>
<text fill="#fce7f3" x="100" y="210">External Ingress</text>
<text fill="#f97316" x="310" y="95">orders-svc (ClusterIP)</text>
<text x="310" y="120">Port: 80 -&gt; Target: 8080</text>
<text x="310" y="145">Selector: app: orders</text>
<text x="310" y="170">EndpointSlice Controller</text>
<text fill="#fce7f3" x="310" y="210">Stable Virtual IP</text>
<text fill="#34d399" x="555" y="95">Deployment: orders</text>
<text x="555" y="120">Labels: app: orders</text>
<text x="555" y="145">Pod 1: 10.244.1.5:8080</text>
<text x="555" y="170">Pod 2: 10.244.2.8:8080</text>
<text fill="#fce7f3" x="555" y="210">Ephemeral Replicas</text>
<text fill="#eab308" x="810" y="95">ConfigMap: app-config</text>
<text x="810" y="120">Feature flags &amp; ports</text>
<text x="810" y="145">Secret: db-credentials</text>
<text x="810" y="170">Encrypted auth tokens</text>
<text fill="#fce7f3" x="810" y="210">Injected Environment</text>
</g>
<g fill="none" marker-end="url(#day10-objects-arrow)" stroke="#38bdf8" stroke-width="2">
<path d="M180 145 L206 145"></path>
<path d="M410 145 L436 145"></path>
<path d="M700 145 L674 145"></path>
</g>
<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="295">Traffic traverses Ingress -&gt; Service -&gt; Pod; Pods mount ConfigMaps and Secrets independently.</text>
</svg>
<figcaption>Figure 10.3: Kubernetes core object relationships and traffic routing hierarchy. External traffic reaches Pods via Ingress and matching Service selectors, while configuration and secrets are injected decoupled from image layers.</figcaption>
</figure>'''

FIG_10_4_HTML = '''<figure class="diagram-figure">
<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>
<svg aria-labelledby="day10-volume-incident-title day10-volume-incident-desc" role="img" viewbox="0 0 940 310">
<title id="day10-volume-incident-title">Ephemeral container layer data loss and persistent volume fix</title>
<desc id="day10-volume-incident-desc">The failed dashed path writes state to an ephemeral container layer that is destroyed during rolling updates. The corrected solid path mounts a persistent volume claim and invokes fsync, guaranteeing data survival across container lifecycles.</desc>
<defs>
<marker id="day10-vol-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>
<marker id="day10-vol-fail-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"></path></marker>
</defs>
<g fill="#121526" stroke-width="2">
<rect height="85" rx="8" stroke="#38bdf8" width="150" x="20" y="110"></rect>
<image href="../assets/icons/generic/client.svg" x="28" y="118" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#f43f5e" width="220" x="225" y="30"></rect>
<image href="../assets/icons/generic/failure.svg" x="233" y="38" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#34d399" width="220" x="225" y="185"></rect>
<image href="../assets/icons/generic/storage.svg" x="233" y="193" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#f43f5e" width="220" x="495" y="30"></rect>
<image href="../assets/icons/generic/failure.svg" x="503" y="38" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#34d399" width="220" x="495" y="185"></rect>
<image href="../assets/icons/generic/decision.svg" x="503" y="193" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#38bdf8" width="155" x="765" y="110"></rect>
<image href="../assets/icons/generic/outcome.svg" x="773" y="118" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
</g>
<g fill="#fce7f3" font-size="12" font-weight="600" text-anchor="middle">
<text x="102" y="142">Order Ingress</text>
<text fill="#a9b7cb" x="102" y="162">Checkout stream</text>
<text x="342" y="58">[FAILED: Ephemeral Layer]</text>
<text fill="#f43f5e" x="342" y="78">Writes to /tmp/orders.log</text>
<text fill="#a9b7cb" x="342" y="98">Thin writable container layer</text>
<text x="342" y="213">[CORRECTED: Persistent Vol]</text>
<text fill="#34d399" x="342" y="233">Mounts PVC /data/orders</text>
<text fill="#a9b7cb" x="342" y="253">GCP Persistent Disk CSI</text>
<text x="612" y="58">EXACT FAILURE POINT</text>
<text fill="#f43f5e" x="612" y="78">Pod redeployed / restarted</text>
<text fill="#f43f5e" x="612" y="98">Writable layer destroyed</text>
<text x="612" y="213">CORRECTED CONTROL</text>
<text fill="#34d399" x="612" y="233">POSIX fsync() commits data</text>
<text fill="#a9b7cb" x="612" y="253">Survives container teardown</text>
<text x="849" y="138">VERIFICATION</text>
<text fill="#34d399" x="849" y="158">Data intact post-restart</text>
<text fill="#a9b7cb" x="849" y="178">Zero duplicate charges</text>
</g>
<g fill="none" stroke-width="2">
<path d="M170 135 L220 85" marker-end="url(#day10-vol-fail-arrow)" stroke="#f43f5e" stroke-dasharray="7 5"></path>
<path d="M445 72 L490 72" marker-end="url(#day10-vol-fail-arrow)" stroke="#f43f5e" stroke-dasharray="7 5"></path>
<path d="M170 170 L220 215" marker-end="url(#day10-vol-arrow)" stroke="#38bdf8"></path>
<path d="M445 227 L490 227" marker-end="url(#day10-vol-arrow)" stroke="#38bdf8"></path>
<path d="M715 227 L760 170" marker-end="url(#day10-vol-arrow)" stroke="#38bdf8"></path>
</g>
<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="295">Dashed line (--&gt;) = ephemeral layer data loss · Solid line (—&gt;) = persistent volume mount and fsync verification</text>
</svg>
<figcaption>Figure 10.4: Supplied facts: Writing state to ephemeral container filesystem results in data loss upon pod recreation. Architectural inference: Decoupling storage lifecycle from container lifecycle via persistent volumes ensures recovery marker survival. Expected post-fix behavior: Replacement containers read existing recovery markers, preserving at-most-once fulfillment semantics.</figcaption>
</figure>'''

FIG_10_5_HTML = '''<figure class="diagram-figure">
<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>
<svg aria-labelledby="day10-sched-incident-title day10-sched-incident-desc" role="img" viewbox="0 0 940 310">
<title id="day10-sched-incident-title">Deployment scale-out failure under node capacity exhaustion</title>
<desc id="day10-sched-incident-desc">The failed dashed path shows three pods trapped in Pending due to insufficient node memory. The corrected solid path right-sizes requests and triggers node autoscaling, resulting in 5 running replicas.</desc>
<defs>
<marker id="day10-sched-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>
<marker id="day10-sched-fail-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"></path></marker>
</defs>
<g fill="#121526" stroke-width="2">
<rect height="85" rx="8" stroke="#38bdf8" width="150" x="20" y="110"></rect>
<image href="../assets/icons/generic/queue.svg" x="28" y="118" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#f43f5e" width="220" x="225" y="30"></rect>
<image href="../assets/icons/generic/failure.svg" x="233" y="38" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#34d399" width="220" x="225" y="185"></rect>
<image href="../assets/icons/generic/server.svg" x="233" y="193" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#f43f5e" width="220" x="495" y="30"></rect>
<image href="../assets/icons/generic/failure.svg" x="503" y="38" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#34d399" width="220" x="495" y="185"></rect>
<image href="../assets/icons/generic/decision.svg" x="503" y="193" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#38bdf8" width="155" x="765" y="110"></rect>
<image href="../assets/icons/generic/outcome.svg" x="773" y="118" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
</g>
<g fill="#fce7f3" font-size="12" font-weight="600" text-anchor="middle">
<text x="102" y="142">Scale Trigger</text>
<text fill="#a9b7cb" x="102" y="162">Replicas: 5</text>
<text x="342" y="58">[FAILED: Fixed Node Pool]</text>
<text fill="#f43f5e" x="342" y="78">3 nodes @ 4G allocatable</text>
<text fill="#a9b7cb" x="342" y="98">Uncalibrated 2G request</text>
<text x="342" y="213">[CORRECTED: Autoscaler]</text>
<text fill="#34d399" x="342" y="233">Calibrated 768M request</text>
<text fill="#a9b7cb" x="342" y="253">Autoscaler adds node</text>
<text x="612" y="58">EXACT FAILURE POINT</text>
<text fill="#f43f5e" x="612" y="78">0/3 nodes available</text>
<text fill="#f43f5e" x="612" y="98">3 Pods trapped in Pending</text>
<text x="612" y="213">CORRECTED CONTROL</text>
<text fill="#34d399" x="612" y="233">Scheduler places all pods</text>
<text fill="#a9b7cb" x="612" y="253">Readiness probes pass</text>
<text x="849" y="138">VERIFICATION</text>
<text fill="#34d399" x="849" y="158">5/5 Replicas Running</text>
<text fill="#a9b7cb" x="849" y="178">Zero dropped checkouts</text>
</g>
<g fill="none" stroke-width="2">
<path d="M170 135 L220 85" marker-end="url(#day10-sched-fail-arrow)" stroke="#f43f5e" stroke-dasharray="7 5"></path>
<path d="M445 72 L490 72" marker-end="url(#day10-sched-fail-arrow)" stroke="#f43f5e" stroke-dasharray="7 5"></path>
<path d="M170 170 L220 215" marker-end="url(#day10-sched-arrow)" stroke="#38bdf8"></path>
<path d="M445 227 L490 227" marker-end="url(#day10-sched-arrow)" stroke="#38bdf8"></path>
<path d="M715 227 L760 170" marker-end="url(#day10-sched-arrow)" stroke="#38bdf8"></path>
</g>
<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="295">Dashed line (--&gt;) = unschedulable capacity failure · Solid line (—&gt;) = autoscaling and right-sized placement</text>
</svg>
<figcaption>Figure 10.5: Supplied facts: Scaled Deployment fails to place three replicas due to node memory exhaustion. Architectural inference: Reconciling desired state requires physical capacity; right-sizing requests and enabling cluster autoscaling restores schedulability. Expected post-fix behavior: All five replicas achieve Running status and pass readiness probes.</figcaption>
</figure>'''

FIG_10_6_HTML = '''<figure class="diagram-figure">
<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>
<svg aria-labelledby="day10-selector-incident-title day10-selector-incident-desc" role="img" viewbox="0 0 940 310">
<title id="day10-selector-incident-title">Service selector label mismatch causing zero backend endpoints</title>
<desc id="day10-selector-incident-desc">The failed dashed path routes requests to a Service whose selector contains a typo, resulting in empty endpoints and HTTP 503. The corrected solid path aligns the selector with Pod labels, restoring traffic flow.</desc>
<defs>
<marker id="day10-sel-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>
<marker id="day10-sel-fail-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"></path></marker>
</defs>
<g fill="#121526" stroke-width="2">
<rect height="85" rx="8" stroke="#38bdf8" width="150" x="20" y="110"></rect>
<image href="../assets/icons/generic/client.svg" x="28" y="118" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#f43f5e" width="220" x="225" y="30"></rect>
<image href="../assets/icons/generic/failure.svg" x="233" y="38" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#34d399" width="220" x="225" y="185"></rect>
<image href="../assets/icons/generic/router.svg" x="233" y="193" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#f43f5e" width="220" x="495" y="30"></rect>
<image href="../assets/icons/generic/failure.svg" x="503" y="38" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#34d399" width="220" x="495" y="185"></rect>
<image href="../assets/icons/generic/decision.svg" x="503" y="193" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#38bdf8" width="155" x="765" y="110"></rect>
<image href="../assets/icons/generic/outcome.svg" x="773" y="118" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
</g>
<g fill="#fce7f3" font-size="12" font-weight="600" text-anchor="middle">
<text x="102" y="142">Client Ingress</text>
<text fill="#a9b7cb" x="102" y="162">GET /checkout</text>
<text x="342" y="58">[FAILED: Selector Typo]</text>
<text fill="#f43f5e" x="342" y="78">Service selector: app: order</text>
<text fill="#a9b7cb" x="342" y="98">Pod labels: app: orders</text>
<text x="342" y="213">[CORRECTED: Matched Label]</text>
<text fill="#34d399" x="342" y="233">Service selector: app: orders</text>
<text fill="#a9b7cb" x="342" y="253">Exact key-value match</text>
<text x="612" y="58">EXACT FAILURE POINT</text>
<text fill="#f43f5e" x="612" y="78">EndpointSlice is empty</text>
<text fill="#f43f5e" x="612" y="98">Ingress returns HTTP 503</text>
<text x="612" y="213">CORRECTED CONTROL</text>
<text fill="#34d399" x="612" y="233">Endpoints populated with IPs</text>
<text fill="#a9b7cb" x="612" y="253">10.244.1.5:8080 active</text>
<text x="849" y="138">VERIFICATION</text>
<text fill="#34d399" x="849" y="158">HTTP 200 OK</text>
<text fill="#a9b7cb" x="849" y="178">Order processed cleanly</text>
</g>
<g fill="none" stroke-width="2">
<path d="M170 135 L220 85" marker-end="url(#day10-sel-fail-arrow)" stroke="#f43f5e" stroke-dasharray="7 5"></path>
<path d="M445 72 L490 72" marker-end="url(#day10-sel-fail-arrow)" stroke="#f43f5e" stroke-dasharray="7 5"></path>
<path d="M170 170 L220 215" marker-end="url(#day10-sel-arrow)" stroke="#38bdf8"></path>
<path d="M445 227 L490 227" marker-end="url(#day10-sel-arrow)" stroke="#38bdf8"></path>
<path d="M715 227 L760 170" marker-end="url(#day10-sel-arrow)" stroke="#38bdf8"></path>
</g>
<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="295">Dashed line (--&gt;) = empty endpoint slice failure · Solid line (—&gt;) = aligned selector and active pod proxying</text>
</svg>
<figcaption>Figure 10.6: Supplied facts: Healthy running Pods receive zero traffic due to a selector typo in the Service specification. Architectural inference: Services decouple IP addressing via label selectors; exact matching is required for EndpointSlice generation. Expected post-fix behavior: Aligned selectors populate endpoints, restoring HTTP 200 responses.</figcaption>
</figure>'''

PART1_HTML = '''<article class="topic-card overview" id="topic-01-overview">
<h3>Docker: images, layers, Dockerfile, registries, mounts, inodes, volumes, POSIX filesystem sync/fsync semantics</h3>
<p><strong class="keyword">Container image construction</strong> and storage architecture combine layered content-addressable tarballs into a unified root filesystem using copy-on-write union filesystems (OverlayFS). Ephemeral writable container layers discard state upon process termination, meaning durable application state requires external storage mounts and explicit operating system persistence semantics: while buffered application writes remain in volatile kernel page cache, only synchronous flush operations (<kbd>fsync()</kbd> / <kbd>fdatasync()</kbd>) guarantee write persistence down to non-volatile physical storage blocks.</p>
<p><strong class="side-heading">Why today:</strong> Cloud architects must recognize the physical boundary between ephemeral container execution and durable enterprise storage to prevent silent data loss during container restarts, rolling updates, and node migrations.</p>
<p class="problem-preview">An order checkout microservice writes transaction recovery markers to its local container directory, but an automatic pod restart wipes out all active markers and causes duplicate order charges. The engineering team attaches a persistent volume with explicit filesystem synchronization calls, ensuring transaction markers survive container replacement and prevent duplicate processing.</p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>Container orchestration: why Kubernetes exists</h3>
<p><strong class="keyword">Container orchestration</strong> automates the operational lifecycle of distributed containerized applications across fleets of virtual machine nodes. Managing individual containers imperatively on bare hosts introduces severe architectural failure modes: unhandled host hardware crashes, manual port allocation conflicts, lack of automated rollouts and rollbacks, and inability to reconcile desired capacity against node resources. Kubernetes solves these challenges through a centralized declarative control plane that continuously reconciles actual runtime telemetry against desired state stored in etcd.</p>
<p><strong class="side-heading">Why today:</strong> Modern cloud-native architectures require automated placement, self-healing, bin packing, and declarative rollouts that manual host-level container tooling cannot deliver at enterprise scale.</p>
<p class="problem-preview">A surge in user checkout requests causes a production order service to exhaust host memory on a standalone virtual machine, crashing all collocated containers and dropping user requests. Migrating the service to a managed Kubernetes cluster allows the scheduler to distribute replicas across multiple worker nodes and automatically restart failed instances without operator intervention.</p>
</article>

<article class="topic-card overview" id="topic-03-overview">
<h3>Kubernetes core objects: Pod, Deployment, Service, Ingress, ConfigMap, Secret</h3>
<p><strong class="keyword">Kubernetes core objects</strong> represent the foundational declarative primitives used to model cloud-native applications: <strong>Pods</strong> represent the atomic unit of collocated container scheduling; <strong>Deployments</strong> manage declarative replica scaling and zero-downtime rolling updates; <strong>Services</strong> provide stable virtual IP addresses and load-balanced endpoint routing across ephemeral pods; <strong>Ingress</strong> routes external HTTP/HTTPS traffic into internal cluster services; and <strong>ConfigMaps</strong> and <strong>Secrets</strong> decouple configuration and sensitive credentials from container image binaries.</p>
<p><strong class="side-heading">Why today:</strong> Mastering the ownership hierarchy and traffic routing pathways linking Ingress, Services, and Pods is required to design reliable multi-tier cloud architectures and rapidly diagnose routing breakdowns.</p>
<p class="problem-preview">A newly deployed microservice passes all readiness checks but external client requests fail immediately with HTTP 503 Service Unavailable errors. An inspection reveals that a subtle typo in the Service selector label prevented the controller from attaching pod IP addresses to the routing endpoint slice.</p>
</article>'''

ARCH_DIAGRAM = {
    'type': 'topology',
    'title': 'Day 10 foundation path — Day 10 — Images, filesystems and orchestration',
    'desc': 'Three-tier foundation topology for Day 10 — Images, filesystems and orchestration. It separates ingress and demand, runtime and data, and governance and decision evidence, with probes at each ownership boundary.',
    'caption': 'Scope: a teaching topology for Day 10\'s day 10 — images, filesystems and orchestration path. It shows ownership boundaries and evidence flow; it does not prove a deployed Google Cloud topology, capacity, or production behavior.',
    'width': 1120,
    'height': 690,
    'nodes': [
        ('1. Workload Ingress & Client Traffic', 'External Client Ingress & Packaging Boundary'),
        ('2. Storage & Filesystem Durability', 'OverlayFS Writable Layers, Mounts & fsync()'),
        ('3. Declarative Control Plane & Scheduling', 'kube-apiserver, etcd, Scheduler & Kubelet CRI'),
        ('4. Core Objects & Routing Hierarchy', 'Ingress, Service Selectors, Pods, ConfigMaps & Secrets')
    ],
    'layers': [
        {'name': 'TIER 1 · INGRESS / DEMAND', 'desc': 'request, client, edge', 'x': 20, 'y': 55, 'w': 1080, 'h': 110, 'fill': '#12283b', 'title_color': '#7dd3fc'},
        {'name': 'TIER 2 · RUNTIME / DATA', 'desc': 'state, process, path', 'x': 20, 'y': 185, 'w': 1080, 'h': 230, 'fill': '#1b2038', 'title_color': '#c4b5fd'},
        {'name': 'TIER 3 · GOVERNANCE / DECISION', 'desc': 'policy, evidence, exit', 'x': 20, 'y': 435, 'w': 1080, 'h': 120, 'fill': '#2b1d2f', 'title_color': '#f9a8d4'}
    ],
    'boundaries': [
        {'x': 430, 'y': 230, 'w': 530, 'h': 140, 'color': '#f59e0b', 'label': 'LIMIT / FAILURE BOUNDARY'}
    ],
    'components': [
        {'x': 70, 'y': 92, 'w': 190, 'h': 52, 'stroke': '#38bdf8', 'name': 'Client / probe', 'detail': 'HTTP checkout & ingress traffic', 'icon': '../assets/icons/generic/client.svg'},
        {'x': 465, 'y': 92, 'w': 250, 'h': 52, 'stroke': '#f59e0b', 'name': 'Boundary under study', 'detail': 'Day 10 — Images, filesystems & orchestration', 'icon': '../assets/icons/gcp/core/gke.svg'},
        {'x': 70, 'y': 222, 'w': 270, 'h': 64, 'stroke': '#38bdf8', 'name': 'Docker Storage Engine', 'detail': 'OverlayFS COW layer · fsync() durability', 'icon': '../assets/icons/generic/storage.svg'},
        {'x': 70, 'y': 312, 'w': 270, 'h': 64, 'stroke': '#38bdf8', 'name': 'Kubernetes Control Plane', 'detail': 'etcd desired state · controller reconciliation', 'icon': '../assets/icons/generic/server.svg'},
        {'x': 455, 'y': 252, 'w': 235, 'h': 62, 'stroke': '#f43f5e', 'name': 'Placement & Capacity Gate', 'detail': 'Scheduler filtering · Allocatable RAM/CPU', 'icon': '../assets/icons/generic/decision.svg'},
        {'x': 715, 'y': 252, 'w': 220, 'h': 62, 'stroke': '#34d399', 'name': 'Active Core Object Stack', 'detail': 'Service VIP -> Pod EndpointSlice', 'icon': '../assets/icons/generic/endpoint.svg'},
        {'x': 70, 'y': 472, 'w': 280, 'h': 52, 'stroke': '#38bdf8', 'name': 'Storage & Routing Policy', 'detail': 'Volume persistence & selector rules', 'icon': '../assets/icons/generic/policy.svg'},
        {'x': 465, 'y': 472, 'w': 310, 'h': 52, 'stroke': '#34d399', 'name': 'Ownership Diagram Exit Artifact', 'detail': 'Pod/Deployment/Service relationship report', 'icon': '../assets/icons/generic/artifact.svg'}
    ],
    'flows': [
        {'x1': 260, 'y1': 118, 'x2': 465, 'y2': 118, 'type': 'ok', 'label': 'INGRESS'},
        {'x1': 340, 'y1': 254, 'x2': 455, 'y2': 270, 'type': 'ok', 'label': 'PERSIST'},
        {'x1': 340, 'y1': 344, 'x2': 455, 'y2': 295, 'type': 'warn', 'label': 'RECONCILE'},
        {'x1': 690, 'y1': 283, 'x2': 715, 'y2': 283, 'type': 'ok', 'label': 'ROUTE'},
        {'x1': 350, 'y1': 498, 'x2': 465, 'y2': 498, 'type': 'ok', 'label': 'AUDIT'}
    ],
    'probes': [
        {'cx': 250, 'cy': 118, 'label': 'P1: Container Packaging & Manifest Check', 'desc': 'Verify image layering and manifest specs', 'color': '#38bdf8'},
        {'cx': 570, 'cy': 252, 'label': 'P2: Node Capacity & Bin Packing Check', 'desc': 'Verify scheduler resource requests', 'color': '#f59e0b'},
        {'cx': 620, 'cy': 472, 'label': 'P3: Service Selector & Endpoint Binding Check', 'desc': 'Verify exact label matching and routing', 'color': '#34d399'}
    ]
}
