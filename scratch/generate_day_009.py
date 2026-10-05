"""Base definitions, figures, and architecture topology for Day 9: VM and container isolation."""

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        f'Linux Kernel KVM API General Description (accessed {ACCESS_DATE})',
        'https://docs.kernel.org/virt/kvm/api.html#general-description'
    ),
    'topic-02': (
        f'namespaces(7) Linux namespaces overview description (accessed {ACCESS_DATE})',
        'https://man7.org/linux/man-pages/man7/namespaces.7.html#DESCRIPTION'
    )
}

FIG_9_1_HTML = '''<figure class="diagram-figure">
<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>
<svg aria-labelledby="day9-boundary-title day9-boundary-desc" role="img" viewbox="0 0 940 390">
<title id="day9-boundary-title">Virtual machine and container isolation boundaries</title>
<desc id="day9-boundary-desc">Two parallel stacks compare a virtual machine with its own guest kernel against two containers that share one host kernel. Outlines mark isolation scopes.</desc>
<defs>
<marker id="day9-boundary-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>
</defs>
<g fill="#121526" stroke-width="2">
<rect height="315" rx="12" stroke="#f43f5e" stroke-dasharray="8 5" width="430" x="20" y="35"></rect>
<rect height="315" rx="12" stroke="#38bdf8" stroke-dasharray="8 5" width="430" x="490" y="35"></rect>
<rect height="60" rx="8" stroke="#38bdf8" width="360" x="55" y="70"></rect>
<image href="../assets/icons/generic/client.svg" x="65" y="86" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="60" rx="8" stroke="#f97316" width="360" x="55" y="155"></rect>
<image href="../assets/icons/generic/server.svg" x="65" y="171" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="60" rx="8" stroke="#34d399" width="360" x="55" y="240"></rect>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="65" y="256" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="60" rx="8" stroke="#38bdf8" width="165" x="525" y="70"></rect>
<image href="../assets/icons/generic/client.svg" x="535" y="86" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="60" rx="8" stroke="#38bdf8" width="165" x="720" y="70"></rect>
<image href="../assets/icons/generic/endpoint.svg" x="730" y="86" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="60" rx="8" stroke="#f97316" width="360" x="525" y="155"></rect>
<image href="../assets/icons/generic/server.svg" x="535" y="171" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
<rect height="60" rx="8" stroke="#34d399" width="360" x="525" y="240"></rect>
<image href="../assets/icons/generic/storage.svg" x="535" y="256" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>
</g>
<g fill="#fce7f3" font-size="13" font-weight="600" text-anchor="middle">
<text x="245" y="58">VIRTUAL MACHINE BOUNDARY</text>
<text x="245" y="97">Order API process + userspace</text>
<text x="245" y="182">Independent Guest Kernel</text>
<text fill="#a9b7cb" font-size="11" x="245" y="199">guest loads own kernel modules &amp; drivers</text>
<text x="245" y="267">Virtual Hardware &amp; Hypervisor</text>
<text fill="#a9b7cb" font-size="11" x="245" y="284">EPT memory translation &amp; vCPU scheduling</text>
<text x="705" y="58">CONTAINER PROCESS BOUNDARIES</text>
<text x="617" y="97">Order API</text>
<text x="812" y="97">Worker</text>
<text x="705" y="182">Shared Host Linux Kernel</text>
<text fill="#a9b7cb" font-size="11" x="705" y="199">namespaces · cgroups v2 · seccomp · capabilities</text>
<text x="705" y="267">Physical Server Hardware</text>
<text fill="#a9b7cb" font-size="11" x="705" y="284">bare metal CPU, RAM, storage, network</text>
</g>
<g fill="none" marker-end="url(#day9-boundary-arrow)" stroke="#38bdf8" stroke-width="2">
<path d="M235 130 L235 151"></path>
<path d="M235 215 L235 236"></path>
<path d="M607 130 L650 151"></path>
<path d="M802 130 L760 151"></path>
<path d="M705 215 L705 236"></path>
</g>
</svg>
<figcaption>Figure 9.1: Architectural comparison of virtualization versus containerization boundaries. A VM encapsulates an independent guest operating system kernel over hypervisor-managed virtual hardware, whereas containers partition host kernel visibility and resources across processes executing directly on the shared host kernel.</figcaption>
</figure>'''

FIG_9_2_HTML = '''<figure class="diagram-figure">
<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>
<svg aria-labelledby="day9-layers-title day9-layers-desc" role="img" viewbox="0 0 940 330">
<title id="day9-layers-title">Linux kernel container isolation layers and syscall evaluation</title>
<desc id="day9-layers-desc">A containerized process request flows sequentially through Linux namespaces, cgroups v2 resource accounting, seccomp system call filtering, and POSIX capability checks before executing in the shared host kernel.</desc>
<defs>
<marker id="day9-layers-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>
</defs>
<g fill="#121526" stroke-width="2">
<rect height="230" rx="10" stroke="#38bdf8" width="160" x="20" y="30"></rect>
<image href="../assets/icons/generic/client.svg" x="32" y="42" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
<rect height="230" rx="10" stroke="#f97316" width="160" x="210" y="30"></rect>
<image href="../assets/icons/generic/endpoint.svg" x="222" y="42" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
<rect height="230" rx="10" stroke="#f43f5e" width="160" x="400" y="30"></rect>
<image href="../assets/icons/generic/monitoring.svg" x="412" y="42" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
<rect height="230" rx="10" stroke="#eab308" width="160" x="590" y="30"></rect>
<image href="../assets/icons/generic/policy.svg" x="602" y="42" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
<rect height="230" rx="10" stroke="#34d399" width="140" x="780" y="30"></rect>
<image href="../assets/icons/generic/server.svg" x="792" y="42" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
</g>
<g fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">
<text x="110" y="60">Container Process</text>
<text x="300" y="60">1. Namespaces</text>
<text x="490" y="60">2. cgroups v2</text>
<text x="680" y="60">3. Seccomp &amp; Caps</text>
<text x="860" y="60">Host Kernel</text>
</g>
<g fill="#a9b7cb" font-size="11" text-anchor="middle">
<text x="100" y="90">Order API / Worker</text>
<text fill="#fce7f3" x="100" y="115">Userspace Process</text>
<text x="100" y="140">UID 0 (Container Root)</text>
<text x="100" y="165">or unprivileged UID</text>
<text fill="#38bdf8" x="100" y="200">Issues System Call</text>
<text x="100" y="225">(open, clone, socket)</text>
<text fill="#fce7f3" x="290" y="90">Visibility Filter</text>
<text x="290" y="115">PID: Virtual process tree</text>
<text x="290" y="140">NET: veth &amp; private routes</text>
<text x="290" y="165">MNT: pivot_root tree</text>
<text x="290" y="190">IPC · UTS · USER</text>
<text fill="#34d399" x="290" y="225">✓ Scoped View</text>
<text fill="#fce7f3" x="480" y="90">Resource Limits</text>
<text x="480" y="115">cpu.max (CFS quota)</text>
<text x="480" y="140">memory.max (limit)</text>
<text x="480" y="165">io.max · PSI accounting</text>
<text fill="#f43f5e" x="480" y="200">Breach: OOM Kill</text>
<text fill="#34d399" x="480" y="225">✓ Within Budget</text>
<text fill="#fce7f3" x="670" y="90">Privilege Gating</text>
<text x="670" y="115">Seccomp: BPF filter</text>
<text x="670" y="140">Blocks dangerous calls</text>
<text x="670" y="165">CapEff: Bound bits</text>
<text fill="#f43f5e" x="670" y="200">Denied: EPERM / SIGSYS</text>
<text fill="#34d399" x="670" y="225">✓ Authorized</text>
<text fill="#fce7f3" x="850" y="90">Execution</text>
<text x="850" y="120">Shared Kernel Space</text>
<text x="850" y="150">Ring 0 Privilege</text>
<text x="850" y="180">Hardware I/O</text>
<text fill="#34d399" x="850" y="225">CPU / RAM / Disk</text>
</g>
<g fill="none" marker-end="url(#day9-layers-arrow)" stroke="#38bdf8" stroke-width="2">
<path d="M180 145 L206 145"></path>
<path d="M370 145 L396 145"></path>
<path d="M560 145 L586 145"></path>
<path d="M750 145 L776 145"></path>
</g>
<text fill="#a9b7cb" font-size="12" text-anchor="middle" x="470" y="295">Every container action traverses all four kernel control gates; none provides a separate kernel.</text>
</svg>
<figcaption>Figure 9.2: Conceptual system call flow through the four Linux kernel container isolation layers. Namespaces partition what the process sees; cgroups v2 throttle and cap what it consumes; seccomp filters which system calls may enter kernel space; and capabilities restrict privileged kernel operations.</figcaption>
</figure>'''

FIG_9_3_HTML = '''<figure class="diagram-figure">
<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>
<svg aria-labelledby="day9-vm-incident-title day9-vm-incident-desc" role="img" viewbox="0 0 940 300">
<title id="day9-vm-incident-title">Tax adapter placement failure and corrected VM path</title>
<desc id="day9-vm-incident-desc">The failed dashed path attempts to run a kernel module inside a shared-kernel container, failing at module insertion. The corrected solid path runs the adapter inside a dedicated VM with its own guest kernel, verified by synthetic requests and an unchanged host.</desc>
<defs>
<marker id="day9-vm-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>
<marker id="day9-vm-fail-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"></path></marker>
</defs>
<g fill="#121526" stroke-width="2">
<rect height="85" rx="8" stroke="#38bdf8" width="150" x="20" y="105"></rect>
<image href="../assets/icons/generic/client.svg" x="28" y="113" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#f43f5e" width="230" x="225" y="30"></rect>
<image href="../assets/icons/generic/failure.svg" x="233" y="38" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#34d399" width="230" x="225" y="180"></rect>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="233" y="188" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#f43f5e" width="210" x="510" y="30"></rect>
<image href="../assets/icons/generic/failure.svg" x="518" y="38" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#34d399" width="210" x="510" y="180"></rect>
<image href="../assets/icons/generic/decision.svg" x="518" y="188" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#38bdf8" width="150" x="770" y="105"></rect>
<image href="../assets/icons/generic/outcome.svg" x="778" y="113" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
</g>
<g fill="#fce7f3" font-size="12" font-weight="600" text-anchor="middle">
<text x="102" y="138">Tax Request</text>
<text fill="#a9b7cb" x="102" y="158">Synthetic Checkout</text>
<text x="348" y="58">[FAILED PATH: Container]</text>
<text fill="#f43f5e" x="348" y="78">Shares immutable host kernel</text>
<text fill="#a9b7cb" x="348" y="98">No guest kernel layer</text>
<text x="348" y="208">[CORRECTED: Dedicated VM]</text>
<text fill="#34d399" x="348" y="228">Independent guest kernel</text>
<text fill="#a9b7cb" x="348" y="248">Vendor-supported image</text>
<text x="622" y="58">EXACT FAILURE POINT</text>
<text fill="#f43f5e" x="622" y="78">insmod: Operation not permitted</text>
<text fill="#a9b7cb" x="622" y="98">CAP_SYS_MODULE dropped</text>
<text x="622" y="208">CORRECTED CONTROL</text>
<text fill="#34d399" x="622" y="228">Module loads in guest kernel</text>
<text fill="#a9b7cb" x="622" y="248">Tax calculation succeeds</text>
<text x="852" y="135">VERIFICATION</text>
<text fill="#34d399" x="852" y="155">HTTP 200 Tax Response</text>
<text fill="#a9b7cb" x="852" y="175">Host nodes unchanged</text>
</g>
<g fill="none" stroke-width="2">
<path d="M170 130 L220 85" marker-end="url(#day9-vm-fail-arrow)" stroke="#f43f5e" stroke-dasharray="7 5"></path>
<path d="M455 72 L506 72" marker-end="url(#day9-vm-fail-arrow)" stroke="#f43f5e" stroke-dasharray="7 5"></path>
<path d="M170 165 L220 210" marker-end="url(#day9-vm-arrow)" stroke="#38bdf8"></path>
<path d="M455 222 L506 222" marker-end="url(#day9-vm-arrow)" stroke="#38bdf8"></path>
<path d="M720 222 L766 165" marker-end="url(#day9-vm-arrow)" stroke="#38bdf8"></path>
</g>
<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="285">Dashed line (--&gt;) = failed container placement · Solid line (—&gt;) = corrected VM path and verification</text>
</svg>
<figcaption>Figure 9.3: Supplied facts: The tax calculation adapter requires a specialized kernel module, and container nodes run an immutable locked kernel. Architectural inference: Placing the workload into a dedicated VM with its own guest kernel resolves kernel-space dependencies without compromising shared container node security. Expected post-fix behavior: Synthetic tax requests return HTTP 200 while host nodes remain unmodified; this is an architectural scenario, not production telemetry.</figcaption>
</figure>'''

FIG_9_4_HTML = '''<figure class="diagram-figure">
<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>
<svg aria-labelledby="day9-memory-incident-title day9-memory-incident-desc" role="img" viewbox="0 0 940 310">
<title id="day9-memory-incident-title">Fulfillment worker cgroup memory failure and streaming control fix</title>
<desc id="day9-memory-incident-desc">The failed dashed path buffers PDF packing slips in worker heap until breaching cgroup memory.max, triggering OOM kill. The corrected solid path streams generation to storage and right-sizes cgroup memory.max, verified by zero OOM kills and deduplicated fulfillment.</desc>
<defs>
<marker id="day9-memory-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>
<marker id="day9-memory-fail-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"></path></marker>
</defs>
<g fill="#121526" stroke-width="2">
<rect height="85" rx="8" stroke="#38bdf8" width="150" x="20" y="110"></rect>
<image href="../assets/icons/generic/queue.svg" x="28" y="118" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#f43f5e" width="220" x="225" y="30"></rect>
<image href="../assets/icons/generic/failure.svg" x="233" y="38" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#34d399" width="220" x="225" y="185"></rect>
<image href="../assets/icons/generic/decision.svg" x="233" y="193" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#f43f5e" width="220" x="495" y="30"></rect>
<image href="../assets/icons/generic/failure.svg" x="503" y="38" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#34d399" width="220" x="495" y="185"></rect>
<image href="../assets/icons/generic/monitoring.svg" x="503" y="193" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
<rect height="85" rx="8" stroke="#38bdf8" width="155" x="765" y="110"></rect>
<image href="../assets/icons/generic/outcome.svg" x="773" y="118" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
</g>
<g fill="#fce7f3" font-size="12" font-weight="600" text-anchor="middle">
<text x="102" y="142">Order Queue</text>
<text fill="#a9b7cb" x="102" y="162">Batch packing events</text>
<text x="342" y="58">[FAILED: In-Memory Heap]</text>
<text fill="#f43f5e" x="342" y="78">Buffers 640M in RAM heap</text>
<text fill="#a9b7cb" x="342" y="98">Host shows 12G available</text>
<text x="342" y="213">[CORRECTED: Stream + Limit]</text>
<text fill="#34d399" x="342" y="233">Stream I/O + 1024M max</text>
<text fill="#a9b7cb" x="342" y="253">Working set capped at 280M</text>
<text x="612" y="58">EXACT FAILURE POINT</text>
<text fill="#f43f5e" x="612" y="78">cgroup memory.max breached</text>
<text fill="#f43f5e" x="612" y="98">SIGKILL 137 · oom_kill +1</text>
<text x="612" y="213">CORRECTED CONTROL</text>
<text fill="#34d399" x="612" y="233">Heap &lt; 50% of cgroup limit</text>
<text fill="#a9b7cb" x="612" y="253">Zero kernel OOM kills</text>
<text x="849" y="138">VERIFICATION</text>
<text fill="#34d399" x="849" y="158">oom_kill == 0</text>
<text fill="#a9b7cb" x="849" y="178">≤1 fulfillment per order</text>
</g>
<g fill="none" stroke-width="2">
<path d="M170 135 L220 85" marker-end="url(#day9-memory-fail-arrow)" stroke="#f43f5e" stroke-dasharray="7 5"></path>
<path d="M445 72 L490 72" marker-end="url(#day9-memory-fail-arrow)" stroke="#f43f5e" stroke-dasharray="7 5"></path>
<path d="M170 170 L220 215" marker-end="url(#day9-memory-arrow)" stroke="#38bdf8"></path>
<path d="M445 227 L490 227" marker-end="url(#day9-memory-arrow)" stroke="#38bdf8"></path>
<path d="M715 227 L760 170" marker-end="url(#day9-memory-arrow)" stroke="#38bdf8"></path>
</g>
<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="295">Dashed line (--&gt;) = cgroup memory failure · Solid line (—&gt;) = streaming fix and idempotent fulfillment</text>
</svg>
<figcaption>Figure 9.4: Supplied facts: Worker terminates with exit code 137 despite 70% host free memory headroom. Architectural inference: The worker exceeded its isolated cgroup v2 memory.max boundary during in-memory buffering. Expected post-fix behavior: Streamed invoice generation and calibrated memory limits prevent OOM termination while queue deduplication preserves at-most-once fulfillment semantics.</figcaption>
</figure>'''

PART1_HTML = '''<article class="topic-card overview" id="topic-01-overview">
<h3>Hypervisors and virtual machines</h3>
<p><strong class="keyword">Virtual machine isolation</strong> relies on hardware-assisted virtualization extensions where a hypervisor intercepts privileged CPU operations and virtualizes physical memory through Extended Page Tables (EPT), granting each guest operating system a completely sovereign kernel space. In contrast to containers that multiplex a single shared kernel, a virtual machine provides an impenetrable cryptographic and architectural isolation boundary backed by independent virtual hardware registers, device emulators, and guest drivers.</p>
<p><strong class="side-heading">Why today:</strong> Cloud architects must rigorously determine when legacy enterprise software, custom kernel drivers, or regulatory compliance mandates require the sovereign kernel boundary of a Compute Engine virtual machine rather than lightweight containerization.</p>
<p class="problem-preview">A third-party enterprise tax calculator requires a proprietary kernel module that fails to load on a shared container cluster due to dropped module insertion privileges. The team migrates the workload to a dedicated Compute Engine virtual machine running a vendor-certified guest kernel, restoring transaction processing without compromising host node security.</p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>Container isolation: namespaces, cgroups, seccomp and capabilities</h3>
<p><strong class="keyword">Linux container isolation</strong> is not a physical or hardware boundary, but an orchestration of four discrete Linux kernel subsystems: namespaces that restrict visibility, control groups (cgroups v2) that govern resource consumption, seccomp-BPF filters that restrict allowable system calls, and POSIX capabilities that fragment root privileges. Because containerized processes execute system calls directly on the shared host Linux kernel, misconfigurations in any single layer can expose the entire host node to compromise or resource starvation.</p>
<p><strong class="side-heading">Why today:</strong> Understanding the precise mechanics of namespaces, cgroup throttling, and seccomp system call restrictions allows architects to design resilient Kubernetes workloads and diagnose silent container kills without making false assumptions about host health.</p>
<p class="problem-preview">A fulfillment worker service intermittently crashes with exit code 137 during batch invoicing despite monitoring dashboards displaying abundant free physical memory on the host server. Inspecting the container runtime reveals that the application breached its isolated cgroup memory limit during memory-intensive PDF generation, triggering a local kernel Out-Of-Memory termination.</p>
</article>'''

ARCH_DIAGRAM = {
    'type': 'topology',
    'title': 'Day 9 foundation path — Day 9 — VM and container isolation',
    'desc': 'Three-tier foundation topology for Day 9 — VM and container isolation. It separates ingress and demand, runtime and data, and governance and decision evidence, with probes at each ownership boundary.',
    'caption': 'Scope: a teaching topology for Day 9\'s day 9 — vm and container isolation path. It shows ownership boundaries and evidence flow; it does not prove a deployed Google Cloud topology, capacity, or production behavior.',
    'width': 1120,
    'height': 690,
    'nodes': [
        ('1. Workload Ingress & Demarcation', 'Client Ingress & Packaging Boundary'),
        ('2. Virtual Machine Sovereign Stacks', 'Type 1/KVM Hypervisor & Independent Guest Kernels'),
        ('3. Kernel Container Isolation Gates', 'Namespaces, cgroups v2, Seccomp & Capabilities'),
        ('4. Governance & Isolation Verification', 'Resource Enforcement vs Security Boundary Worksheet')
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
        {'x': 70, 'y': 92, 'w': 190, 'h': 52, 'stroke': '#38bdf8', 'name': 'Client / probe', 'detail': 'workload input & criteria', 'icon': '../assets/icons/generic/client.svg'},
        {'x': 465, 'y': 92, 'w': 250, 'h': 52, 'stroke': '#f59e0b', 'name': 'Boundary under study', 'detail': 'Day 9 — VM and container isolation', 'icon': '../assets/icons/gcp/core/compute-engine.svg'},
        {'x': 70, 'y': 222, 'w': 270, 'h': 64, 'stroke': '#38bdf8', 'name': 'Compute Engine VM Stack', 'detail': 'KVM hypervisor · Sovereign guest kernel', 'icon': '../assets/icons/generic/server.svg'},
        {'x': 70, 'y': 312, 'w': 270, 'h': 64, 'stroke': '#38bdf8', 'name': 'Shared Host Container Stack', 'detail': 'GKE / Cloud Run · Shared host kernel', 'icon': '../assets/icons/gcp/core/gke.svg'},
        {'x': 455, 'y': 252, 'w': 235, 'h': 62, 'stroke': '#f43f5e', 'name': 'Resource vs Security Gate', 'detail': 'cgroups v2 limit vs seccomp sandbox', 'icon': '../assets/icons/generic/policy.svg'},
        {'x': 715, 'y': 252, 'w': 220, 'h': 62, 'stroke': '#34d399', 'name': 'Isolated Execution State', 'detail': 'vCPU / Namespaces verified', 'icon': '../assets/icons/generic/endpoint.svg'},
        {'x': 70, 'y': 472, 'w': 280, 'h': 52, 'stroke': '#38bdf8', 'name': 'Architectural Isolation Policy', 'detail': 'Workload placement rules & criteria', 'icon': '../assets/icons/generic/decision.svg'},
        {'x': 465, 'y': 472, 'w': 310, 'h': 52, 'stroke': '#34d399', 'name': 'Isolation Worksheet Exit Artifact', 'detail': 'Resource limits vs Security isolation', 'icon': '../assets/icons/generic/artifact.svg'}
    ],
    'flows': [
        {'x1': 260, 'y1': 118, 'x2': 465, 'y2': 118, 'type': 'ok', 'label': 'SPECIFY'},
        {'x1': 340, 'y1': 254, 'x2': 455, 'y2': 270, 'type': 'ok', 'label': 'VM PATH'},
        {'x1': 340, 'y1': 344, 'x2': 455, 'y2': 295, 'type': 'warn', 'label': 'CONTAINER'},
        {'x1': 690, 'y1': 283, 'x2': 715, 'y2': 283, 'type': 'ok', 'label': 'ISOLATE'},
        {'x1': 350, 'y1': 498, 'x2': 465, 'y2': 498, 'type': 'ok', 'label': 'VERIFY'}
    ],
    'probes': [
        {'cx': 250, 'cy': 118, 'label': 'P1: Isolation Contract Criteria', 'desc': 'Workload requirements check', 'color': '#38bdf8'},
        {'cx': 570, 'cy': 252, 'label': 'P2: Kernel vs User Space Boundary', 'desc': 'Kernel privilege and module check', 'color': '#f59e0b'},
        {'cx': 620, 'cy': 472, 'label': 'P3: Resource Throttling vs Security Trap', 'desc': 'Distinguish resource vs security', 'color': '#34d399'}
    ]
}
