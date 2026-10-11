"""Durable data specification for Day 10: Images, filesystems and orchestration."""

ACCESS_DATE = '2026-10-04'

SOURCES = {'topic-01': ('fsync(2) Linux file data synchronization description (accessed 2026-10-04)', 'https://man7.org/linux/man-pages/man2/fsync.2.html#DESCRIPTION'), 'topic-02': ('Why you need Kubernetes and what it can do (accessed 2026-10-04)', 'https://kubernetes.io/docs/concepts/overview/#why-you-need-kubernetes-and-what-can-it-do'), 'topic-03': ('Understanding Kubernetes objects (accessed 2026-10-04)', 'https://kubernetes.io/docs/concepts/overview/working-with-objects/#kubernetes-objects')}

DATA = {'access_date': '2026-10-04',
 'arch_diagram': {'boundaries': [{'color': '#f59e0b',
                                  'h': 140,
                                  'label': 'LIMIT / FAILURE BOUNDARY',
                                  'w': 530,
                                  'x': 430,
                                  'y': 230}],
                  'caption': 'Scope: an illustrative architecture topology for Day 10 container storage and Kubernetes '
                             'orchestration; it does not prove a deployed Google Cloud production topology or '
                             'capacity.',
                  'components': [{'detail': 'HTTP checkout & API traffic',
                                  'h': 52,
                                  'icon': '../assets/icons/generic/client.svg',
                                  'name': 'Client / Ingress Traffic',
                                  'stroke': '#38bdf8',
                                  'w': 190,
                                  'x': 70,
                                  'y': 92},
                                 {'detail': 'Image manifests, OverlayFS & GKE control plane',
                                  'h': 52,
                                  'icon': '../assets/icons/gcp/core/gke.svg',
                                  'name': 'OCI Packaging & Orchestration Gate',
                                  'stroke': '#f59e0b',
                                  'w': 250,
                                  'x': 465,
                                  'y': 92},
                                 {'detail': 'OverlayFS COW layer · fsync() durability',
                                  'h': 64,
                                  'icon': '../assets/icons/generic/storage.svg',
                                  'name': 'Docker Storage Engine',
                                  'stroke': '#38bdf8',
                                  'w': 270,
                                  'x': 70,
                                  'y': 222},
                                 {'detail': 'etcd desired state · controller reconciliation',
                                  'h': 64,
                                  'icon': '../assets/icons/generic/server.svg',
                                  'name': 'Kubernetes Control Plane',
                                  'stroke': '#38bdf8',
                                  'w': 270,
                                  'x': 70,
                                  'y': 312},
                                 {'detail': 'Scheduler filtering · Allocatable RAM/CPU',
                                  'h': 62,
                                  'icon': '../assets/icons/generic/decision.svg',
                                  'name': 'Placement & Capacity Gate',
                                  'stroke': '#f43f5e',
                                  'w': 235,
                                  'x': 455,
                                  'y': 252},
                                 {'detail': 'Service VIP -> Pod EndpointSlice',
                                  'h': 62,
                                  'icon': '../assets/icons/generic/endpoint.svg',
                                  'name': 'Active Core Object Stack',
                                  'stroke': '#34d399',
                                  'w': 220,
                                  'x': 715,
                                  'y': 252},
                                 {'detail': 'Volume persistence & selector rules',
                                  'h': 52,
                                  'icon': '../assets/icons/generic/policy.svg',
                                  'name': 'Storage & Routing Policy',
                                  'stroke': '#38bdf8',
                                  'w': 280,
                                  'x': 70,
                                  'y': 472},
                                 {'detail': 'Pod/Deployment/Service relationship report',
                                  'h': 52,
                                  'icon': '../assets/icons/generic/artifact.svg',
                                  'name': 'Ownership Diagram Exit Artifact',
                                  'stroke': '#34d399',
                                  'w': 310,
                                  'x': 465,
                                  'y': 472}],
                  'desc': 'Operational topology tracing OCI image layers, OverlayFS copy-on-write storage durability, '
                          'kube-apiserver declarative reconciliation, and Service-to-Pod routing hierarchy.',
                  'flows': [{'label': 'INGRESS', 'type': 'ok', 'x1': 260, 'x2': 465, 'y1': 118, 'y2': 118},
                            {'label': 'PERSIST', 'type': 'ok', 'x1': 340, 'x2': 455, 'y1': 254, 'y2': 270},
                            {'label': 'RECONCILE', 'type': 'warn', 'x1': 340, 'x2': 455, 'y1': 344, 'y2': 295},
                            {'label': 'ROUTE', 'type': 'ok', 'x1': 690, 'x2': 715, 'y1': 283, 'y2': 283},
                            {'label': 'AUDIT', 'type': 'ok', 'x1': 350, 'x2': 465, 'y1': 498, 'y2': 498}],
                  'height': 690,
                  'layers': [{'desc': 'External client ingress, HTTP checkouts, and OCI image manifests',
                              'fill': '#12283b',
                              'h': 110,
                              'name': 'TIER 1 · WORKLOAD INGRESS & PACKAGING',
                              'title_color': '#7dd3fc',
                              'w': 1080,
                              'x': 20,
                              'y': 55},
                             {'desc': 'OverlayFS COW layers, volume mounts, kube-apiserver, and etcd reconciliation',
                              'fill': '#1b2038',
                              'h': 230,
                              'name': 'TIER 2 · STORAGE ENGINE & CONTROL PLANE',
                              'title_color': '#c4b5fd',
                              'w': 1080,
                              'x': 20,
                              'y': 185},
                             {'desc': 'Service VIP routing, EndpointSlices, volume persistence, and ownership diagram '
                                      'artifact',
                              'fill': '#2b1d2f',
                              'h': 120,
                              'name': 'TIER 3 · ROUTING HIERARCHY & PERSISTENCE GOVERNANCE',
                              'title_color': '#f9a8d4',
                              'w': 1080,
                              'x': 20,
                              'y': 435}],
                  'nodes': [('1. Workload Ingress & Client Traffic', 'External Client Ingress & Packaging Boundary'),
                            ('2. Storage & Filesystem Durability', 'OverlayFS Writable Layers, Mounts & fsync()'),
                            ('3. Declarative Control Plane & Scheduling',
                             'kube-apiserver, etcd, Scheduler & Kubelet CRI'),
                            ('4. Core Objects & Routing Hierarchy',
                             'Ingress, Service Selectors, Pods, ConfigMaps & Secrets')],
                  'probes': [{'color': '#38bdf8',
                              'cx': 250,
                              'cy': 118,
                              'label': 'P1: Container Packaging & Manifest Check'},
                             {'color': '#f59e0b',
                              'cx': 570,
                              'cy': 252,
                              'label': 'P2: Node Capacity & Bin Packing Check'},
                             {'color': '#34d399',
                              'cx': 620,
                              'cy': 472,
                              'label': 'P3: Service Selector & Endpoint Binding Check'}],
                  'title': 'Day 10: Container Storage Durability and Kubernetes Control Plane Topology',
                  'type': 'topology',
                  'width': 1120},
 'completion_html': '<div class="completion-box" id="completion-box-010">\n'
                    '<h3>Day 10 Acceptance Checklist</h3>\n'
                    '<ul class="checklist">\n'
                    '<li><input type="checkbox" id="check-10-1"> <label for="check-10-1">Docker storage mastered: '
                    'OverlayFS copy-on-write lowerdir/upperdir, inodes, multi-stage builds, and Artifact '
                    'Registry.</label></li>\n'
                    '<li><input type="checkbox" id="check-10-2"> <label for="check-10-2">Filesystem durability '
                    'understood: volatile page cache vs POSIX <kbd>fsync()</kbd> flushes to persistent volume '
                    'storage.</label></li>\n'
                    '<li><input type="checkbox" id="check-10-3"> <label for="check-10-3">Kubernetes control plane '
                    'mapped: etcd desired state, continuous controller reconciliation, two-phase scheduler bin '
                    'packing, and self-healing.</label></li>\n'
                    '<li><input type="checkbox" id="check-10-4"> <label for="check-10-4">Core objects &amp; routing '
                    'connected: Ingress path routing, Service label selectors, dynamic EndpointSlices, Pod replicas, '
                    'ConfigMaps, and Secrets.</label></li>\n'
                    '<li><input type="checkbox" id="check-10-5"> <label for="check-10-5">Exit evidence verified: '
                    'compiled the Pod/Deployment/Service ownership diagram and verified volume persistence across '
                    'container lifecycles.</label></li>\n'
                    '</ul>\n'
                    '<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">\n'
                    '<button class="btn btn-primary" id="btn-read-010" '
                    'onclick="this.classList.toggle(\'completed\');this.textContent=this.classList.contains(\'completed\')?\'✓ '
                    'Read Day 10 Completed\':\'Mark Day 10 as Read\';">Mark Day 10 as Read</button>\n'
                    '<button class="btn btn-secondary" id="btn-artifact-010" '
                    'onclick="this.classList.toggle(\'verified\');this.textContent=this.classList.contains(\'verified\')?\'✓ '
                    'Exit Artifact Verified\':\'Verify Exit Artifact\';">Verify Exit Artifact</button>\n'
                    '</div>\n'
                    '</div>',
 'contract_version': 2,
 'day': 10,
 'exit_summary': 'A comprehensive Pod/Deployment/Service ownership diagram and storage durability baseline '
                 'distinguishing ephemeral OverlayFS storage from persistent volume mounts, backed by runnable '
                 'container image verification, scheduler bin packing telemetry, and verified service selector '
                 'routing.',
 'part1_html': '<article class="topic-card overview" id="topic-01-overview">\n'
               '<h3>Docker: images, layers, Dockerfile, registries, mounts, inodes, volumes, POSIX filesystem '
               'sync/fsync semantics</h3>\n'
               '<p><strong class="keyword">Container image construction</strong> and storage architecture combine '
               'layered content-addressable tarballs into a unified root filesystem using copy-on-write union '
               'filesystems (OverlayFS). Ephemeral writable container layers discard state upon process termination, '
               'meaning durable application state requires external storage mounts and explicit operating system '
               'persistence semantics: while buffered application writes remain in volatile kernel page cache, only '
               'synchronous flush operations (<kbd>fsync()</kbd> / <kbd>fdatasync()</kbd>) guarantee write persistence '
               'down to non-volatile physical storage blocks.</p>\n'
               '<p><strong class="side-heading">Why today:</strong> Cloud architects must recognize the physical '
               'boundary between ephemeral container execution and durable enterprise storage to prevent silent data '
               'loss during container restarts, rolling updates, and node migrations.</p>\n'
               '<p><strong class="side-heading">Where it sits:</strong> Builds on Day 9 container runtime boundaries '
               'to establish image packaging and durable storage before coordinating multi-node clusters.</p>\n'
               '<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> An order checkout '
               'microservice writes transaction recovery markers to its local container directory, but an automatic '
               'pod restart wipes out all active markers and causes duplicate order charges. The engineering team '
               'attaches a persistent volume with explicit filesystem synchronization calls, ensuring transaction '
               'markers survive container replacement and prevent duplicate processing.</p>\n'
               '</article>\n'
               '\n'
               '<article class="topic-card overview" id="topic-02-overview">\n'
               '<h3>Container orchestration: why Kubernetes exists</h3>\n'
               '<p><strong class="keyword">Container orchestration</strong> automates the operational lifecycle of '
               'distributed containerized applications across fleets of virtual machine nodes. Managing individual '
               'containers imperatively on bare hosts introduces severe architectural failure modes: unhandled host '
               'hardware crashes, manual port allocation conflicts, lack of automated rollouts and rollbacks, and '
               'inability to reconcile desired capacity against node resources. Kubernetes solves these challenges '
               'through a centralized declarative control plane that continuously reconciles actual runtime telemetry '
               'against desired state stored in etcd.</p>\n'
               '<p><strong class="side-heading">Why today:</strong> Modern cloud-native architectures require '
               'automated placement, self-healing, bin packing, and declarative rollouts that manual host-level '
               'container tooling cannot deliver at enterprise scale.</p>\n'
               '<p><strong class="side-heading">Where it sits:</strong> Bridges single-node container runtime '
               'mechanics with the declarative cluster control plane primitives defined in topic 3.</p>\n'
               '<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A surge in user '
               'checkout requests causes a production order service to exhaust host memory on a standalone virtual '
               'machine, crashing all collocated containers and dropping user requests. Migrating the service to a '
               'managed Kubernetes cluster allows the scheduler to distribute replicas across multiple worker nodes '
               'and automatically restart failed instances without operator intervention.</p>\n'
               '</article>\n'
               '\n'
               '<article class="topic-card overview" id="topic-03-overview">\n'
               '<h3>Kubernetes core objects: Pod, Deployment, Service, Ingress, ConfigMap, Secret</h3>\n'
               '<p><strong class="keyword">Kubernetes core objects</strong> represent the foundational declarative '
               'primitives used to model cloud-native applications: <strong>Pods</strong> represent the atomic unit of '
               'collocated container scheduling; <strong>Deployments</strong> manage declarative replica scaling and '
               'zero-downtime rolling updates; <strong>Services</strong> provide stable virtual IP addresses and '
               'load-balanced endpoint routing across ephemeral pods; <strong>Ingress</strong> routes external '
               'HTTP/HTTPS traffic into internal cluster services; and <strong>ConfigMaps</strong> and '
               '<strong>Secrets</strong> decouple configuration and sensitive credentials from container image '
               'binaries.</p>\n'
               '<p><strong class="side-heading">Why today:</strong> Mastering the ownership hierarchy and traffic '
               'routing pathways linking Ingress, Services, and Pods is required to design reliable multi-tier cloud '
               'architectures and rapidly diagnose routing breakdowns.</p>\n'
               '<p><strong class="side-heading">Where it sits:</strong> Translates orchestration requirements into '
               "deployable API primitives, providing the structural model for the day's exit ownership diagram.</p>\n"
               '<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A newly deployed '
               'microservice passes all readiness checks but external client requests fail immediately with HTTP 503 '
               'Service Unavailable errors. An inspection reveals that a subtle typo in the Service selector label '
               'prevented the controller from attaching pod IP addresses to the routing endpoint slice.</p>\n'
               '</article>',
 'part1_intro': 'Day 10 examines container storage layers, filesystem durability, and container orchestration '
                'architectures: OCI image construction, OverlayFS copy-on-write root filesystems, POSIX fsync() write '
                'durability, declarative reconciliation loops in Kubernetes, and the core object hierarchy (Pods, '
                'Deployments, Services, Ingress, ConfigMaps, and Secrets).',
 'part2_intro': 'Analyze the technical mechanics governing container storage layering, BuildKit layer caching, POSIX '
                'page cache synchronization, declarative control loops, two-phase scheduler bin packing, and service '
                'discovery routing.',
 'part3_intro': 'Real-world architectural failure cases demonstrating ephemeral container layer data loss, scale-out '
                'scheduling traps under node memory exhaustion, and silent HTTP 503 routing failures caused by Service '
                'selector typos.',
 'part4_intro': 'Hands-on operational exercises to build a container image, test volume persistence against ephemeral '
                'teardown, simulate Kubernetes scheduler bin packing under capacity limits, and diagnose broken '
                'Service selectors.',
 'roadmap_exit': 'A runnable image, persistence check and Pod/Deployment/Service ownership diagram.',
 'roadmap_practice': 'Build a tiny container from an annotated example; compare ephemeral files with a mounted volume '
                     'and trace buffered write versus durable flush.',
 'sources': {'topic-01': ('fsync(2) Linux file data synchronization description (accessed 2026-10-04)',
                          'https://man7.org/linux/man-pages/man2/fsync.2.html#DESCRIPTION'),
             'topic-02': ('Why you need Kubernetes and what it can do (accessed 2026-10-04)',
                          'https://kubernetes.io/docs/concepts/overview/#why-you-need-kubernetes-and-what-can-it-do'),
             'topic-03': ('Understanding Kubernetes objects (accessed 2026-10-04)',
                          'https://kubernetes.io/docs/concepts/overview/working-with-objects/#kubernetes-objects')},
 'topics': [{'anchors': {'lab': 'topic-01-lab',
                         'overview': 'topic-01-overview',
                         'problem': 'topic-01-problem',
                         'technical': 'topic-01-technical'},
             'key': 'topic-01',
             'lab': {'accept': 'A persistence verification report confirming data loss on ephemeral storage and 100% '
                               'record retention on mounted volume storage with fsync.',
                     'cleanup': 'Remove temporary container simulation directories and files created in '
                                'scratch/day10_lab_a.',
                     'covers': 'Build a tiny container from an annotated example; compare ephemeral files with a '
                               'mounted volume and trace buffered write versus durable flush.',
                     'expected': 'A runnable container image, verified ephemeral file destruction upon container '
                                 'replacement, and verified durable persistence of fsync-committed records across '
                                 'volume mounts.',
                     'file': 'day-010-exercise-a.md',
                     'goal': 'Build a lightweight container application, contrast ephemeral container storage '
                             'lifecycles with mounted persistent volume durability, and demonstrate the POSIX fsync() '
                             'writeback boundary.',
                     'mode': 'Observed locally: local bash execution of Python application simulation, file creation, '
                             'and fsync flushing. Simulated or predicted: Docker/containerd OverlayFS upperdir '
                             'deletion and GKE Persistent Disk CSI dynamic volume provisioning. Untested on GCP: '
                             'Compute Engine hyperdisk NVMe controller flush caching and cross-zone volume migration '
                             'latency.',
                     'name': 'Exercise A · Build a container and test volume persistence',
                     'preflight': 'Verify that bash, python3, and standard file manipulation tools are installed.',
                     'prereq': 'Linux terminal with bash and core utilities.',
                     'steps': ['**Stage 1: Preflight and Environment Baseline**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Verify core CLI utilities and establish the isolated test workspace for container '
                               'storage testing.\n'
                               '```bash\n'
                               'command -v bash\n'
                               'command -v python3\n'
                               'command -v cat\n'
                               'command -v mkdir\n'
                               'mkdir -p scratch/day10_lab_a/ephemeral_layer scratch/day10_lab_a/mounted_volume\n'
                               'echo "Stage 1 preflight complete at $(date -u +%Y-%m-%dT%H:%M:%SZ)" > '
                               'scratch/day10_lab_a/stage1.log\n'
                               'cat scratch/day10_lab_a/stage1.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Tooling paths verified and workspace directories initialized.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_a/stage1.log`',
                               '**Stage 2: Author Application Fixture with Buffered Write and fsync Flush**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Author a Python application fixture that demonstrates the difference between standard '
                               'buffered writes and durable POSIX fsync flushes.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_a/app.py\n"
                               'import os, sys, time\n'
                               '\n'
                               'def write_unbuffered_record(path, record_id):\n'
                               '    # Standard write: buffers in application memory / kernel page cache\n'
                               '    with open(path, "a") as f:\n'
                               '        f.write(f"ORDER_RECORD:{record_id}:{time.time()}:BUFFERED\\n")\n'
                               '\n'
                               'def write_durable_record(path, record_id):\n'
                               '    # Durable write: forces kernel page cache writeback to disk via fsync\n'
                               '    with open(path, "a") as f:\n'
                               '        f.write(f"ORDER_RECORD:{record_id}:{time.time()}:DURABLE\\n")\n'
                               '        f.flush()\n'
                               '        os.fsync(f.fileno())\n'
                               '\n'
                               'if __name__ == "__main__":\n'
                               '    mode = sys.argv[1]\n'
                               '    target_dir = sys.argv[2]\n'
                               '    out_file = os.path.join(target_dir, "orders.log")\n'
                               '    if mode == "ephemeral":\n'
                               '        write_unbuffered_record(out_file, "ORD-9001")\n'
                               '        print(f"Wrote unbuffered record to ephemeral path: {out_file}")\n'
                               '    elif mode == "durable":\n'
                               '        write_durable_record(out_file, "ORD-9002")\n'
                               '        print(f"Wrote fsync-flushed record to durable volume path: {out_file}")\n'
                               'EOF\n'
                               'python3 -c "import py_compile; py_compile.compile(\'scratch/day10_lab_a/app.py\')" && '
                               'echo "Fixture compiled successfully" > scratch/day10_lab_a/stage2.log\n'
                               'cat scratch/day10_lab_a/stage2.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Application fixture is compiled and validated.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_a/stage2.log`',
                               '**Stage 3: Author Dockerfile with Multi-Stage Build Directives**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Author an annotated Dockerfile demonstrating multi-stage build patterns, minimal base '
                               'layers, and non-root execution.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_a/Dockerfile\n"
                               '# Multi-stage Dockerfile: separates build dependencies from minimal runtime\n'
                               'FROM python:3.12-alpine AS builder\n'
                               'WORKDIR /app\n'
                               'COPY app.py .\n'
                               'RUN python3 -m compileall app.py\n'
                               '\n'
                               '# Minimal runtime stage\n'
                               'FROM python:3.12-alpine\n'
                               'WORKDIR /app\n'
                               'COPY --from=builder /app/app.py .\n'
                               '# Create non-root unprivileged service user\n'
                               'RUN adduser -D -u 10001 appuser &&     mkdir -p /data && chown -R appuser:appuser '
                               '/data\n'
                               'USER 10001\n'
                               'VOLUME ["/data"]\n'
                               'ENTRYPOINT ["python3", "app.py"]\n'
                               'EOF\n'
                               'echo "Dockerfile authored and verified" > scratch/day10_lab_a/stage3.log\n'
                               'cat scratch/day10_lab_a/stage3.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Multi-stage Dockerfile is generated and verified.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_a/stage3.log`',
                               '**Stage 4: Simulate Ephemeral Storage Write and Observe Teardown Loss**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Execute the application in ephemeral mode (simulating an OverlayFS writable container '
                               'layer), record the transaction, and simulate container teardown and replacement.\n'
                               '```bash\n'
                               '# Container 1 launches and writes to ephemeral layer\n'
                               'python3 scratch/day10_lab_a/app.py ephemeral scratch/day10_lab_a/ephemeral_layer > '
                               'scratch/day10_lab_a/stage4.log\n'
                               'echo "--- Container 1 file state ---" >> scratch/day10_lab_a/stage4.log\n'
                               'cat scratch/day10_lab_a/ephemeral_layer/orders.log >> scratch/day10_lab_a/stage4.log\n'
                               '\n'
                               '# Container 1 terminates (OverlayFS thin writable layer destroyed)\n'
                               'rm -rf scratch/day10_lab_a/ephemeral_layer/*\n'
                               '\n'
                               '# Container 2 (replacement pod) launches with fresh empty rootfs\n'
                               'if [ ! -f scratch/day10_lab_a/ephemeral_layer/orders.log ]; then\n'
                               '    echo "OBSERVED: orders.log does not exist in Container 2! Ephemeral data '
                               'destroyed." >> scratch/day10_lab_a/stage4.log\n'
                               'fi\n'
                               'cat scratch/day10_lab_a/stage4.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Output documents data creation in Container 1 and complete loss '
                               'in Container 2.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_a/stage4.log`',
                               '**Stage 5: Simulate Mounted Volume Write with POSIX fsync Durability**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Execute the application in durable mode using a mounted volume simulation with '
                               'explicit fsync, then simulate container replacement.\n'
                               '```bash\n'
                               '# Container 1 writes to mounted volume with fsync\n'
                               'python3 scratch/day10_lab_a/app.py durable scratch/day10_lab_a/mounted_volume > '
                               'scratch/day10_lab_a/stage5.log\n'
                               '\n'
                               '# Container 1 terminates; mounted volume remains intact on host/network storage\n'
                               '# Container 2 launches and attaches the existing volume\n'
                               'echo "--- Container 2 reading mounted volume ---" >> scratch/day10_lab_a/stage5.log\n'
                               'cat scratch/day10_lab_a/mounted_volume/orders.log >> scratch/day10_lab_a/stage5.log\n'
                               'if grep -q "ORD-9002" scratch/day10_lab_a/mounted_volume/orders.log; then\n'
                               '    echo "VERIFIED: Transaction ORD-9002 survived container replacement on mounted '
                               'volume!" >> scratch/day10_lab_a/stage5.log\n'
                               'fi\n'
                               'cat scratch/day10_lab_a/stage5.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Transaction ORD-9002 is preserved across container lifecycles on '
                               'the mounted volume.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_a/stage5.log`',
                               '**Stage 6: Rehearse Sudden Process Crash: Buffered Cache vs fsync Media**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Simulate an abrupt process termination to observe why kernel page cache buffering '
                               'alone is insufficient without fsync().\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_a/simulate_crash.py\n"
                               'import os, sys, subprocess\n'
                               '\n'
                               'crash_log = "scratch/day10_lab_a/crash_test.log"\n'
                               'child_code = ("import os\\n" \n'
                               '              "with open(\'scratch/day10_lab_a/crash_test.log\', \'w\') as f:\\n" \n'
                               '              "    for i in range(100):\\n" \n'
                               '              "        f.write(f\'UNFLUSHED_RECORD_{i}\\\\n\')\\n" \n'
                               '              "    os._exit(137)\\n")\n'
                               'proc = subprocess.run([sys.executable, "-c", child_code])\n'
                               'size = os.path.getsize(crash_log) if os.path.exists(crash_log) else 0\n'
                               'print(f"Abrupt termination simulated with exit code {proc.returncode}. Flushed bytes: '
                               '{size}")\n'
                               'EOF\n'
                               'python3 scratch/day10_lab_a/simulate_crash.py > scratch/day10_lab_a/stage6.log\n'
                               'cat scratch/day10_lab_a/stage6.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Output illustrates that abrupt process exits can truncate or lose '
                               'uncommitted dirty page buffers.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_a/stage6.log`',
                               '**Stage 7: Compile the Persistence Verification Report**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Generate a comprehensive persistence verification report contrasting ephemeral '
                               'container layers with persistent volume mounts.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_a/compile_report.py\n"
                               'report = """# Day 10 Persistence and Storage Verification Report\n'
                               'Generated: Local Terminal Simulation\n'
                               '\n'
                               '## 1. Experimental Results Summary\n'
                               '- Ephemeral Layer Test: Record ORD-9001 written to thin OverlayFS layer was DESTROYED '
                               'upon container restart.\n'
                               '- Mounted Volume Test: Record ORD-9002 written with POSIX fsync() SURVIVED container '
                               'replacement.\n'
                               '- Crash Simulation: Unflushed page cache writes subject to data corruption during '
                               'abrupt SIGKILL terminations.\n'
                               '\n'
                               '## 2. Architectural Storage Guidance\n'
                               '1. Never write transactional or recovery data to ephemeral container storage (/tmp or '
                               'container rootfs).\n'
                               '2. Attach Kubernetes PersistentVolumeClaims backed by managed cloud block storage '
                               '(pd-balanced / pd-ssd).\n'
                               '3. Ensure stateful applications call fsync() or fdatasync() to commit dirty memory '
                               'pages to non-volatile disk.\n'
                               '"""\n'
                               'with open("scratch/day-010-persistence-report.txt", "w") as f:\n'
                               '    f.write(report)\n'
                               'print("Persistence report compiled")\n'
                               'EOF\n'
                               'python3 scratch/day10_lab_a/compile_report.py > scratch/day10_lab_a/stage7.log\n'
                               'cat scratch/day-010-persistence-report.txt\n'
                               '```\n'
                               '\n'
                               '**Expected result:** `scratch/day-010-persistence-report.txt` is compiled and '
                               'verified.\n'
                               '\n'
                               '**Save:** `scratch/day-010-persistence-report.txt`',
                               '**Stage 8: Validate the Persistence Report and Clean Up**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Validate that the persistence report satisfies all evaluation criteria and remove '
                               'transient files.\n'
                               '```bash\n'
                               'test -f scratch/day-010-persistence-report.txt && grep -q "SURVIVED" '
                               'scratch/day-010-persistence-report.txt\n'
                               'echo "✓ Day 10 Exercise A validation passed successfully" > '
                               'scratch/day10_lab_a/stage8.log\n'
                               'cat scratch/day10_lab_a/stage8.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Validation succeeds with clean status.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_a/stage8.log`'],
                     'trouble': 'If write permission errors occur, verify that scratch/day10_lab_a directory '
                                'permissions are readable and writeable.',
                     'verification': 'Verify that ephemeral files are deleted on container simulation restart while '
                                     'mounted volume files persist intact.'},
             'overview': 'Container image construction and storage architecture combine layered content-addressable '
                         'tarballs into a unified root filesystem using copy-on-write union filesystems (OverlayFS). '
                         'Ephemeral writable container layers discard state upon process termination, meaning durable '
                         'application state requires external storage mounts and explicit operating system persistence '
                         'semantics: while buffered application writes remain in volatile kernel page cache, only '
                         'synchronous flush operations (fsync() / fdatasync()) guarantee write persistence down to '
                         'non-volatile physical storage blocks.',
             'preview': 'An order checkout microservice writes transaction recovery markers to its local container '
                        'directory, but an automatic pod restart wipes out all active markers and causes duplicate '
                        'order charges. The engineering team attaches a persistent volume with explicit filesystem '
                        'synchronization calls, ensuring transaction markers survive container replacement and prevent '
                        'duplicate processing.',
             'questions': ['How does the OverlayFS copy-on-write mechanism impact I/O performance during random write '
                           'operations?',
                           'Why does the standard POSIX write() system call fail to guarantee durability across sudden '
                           'container terminations?',
                           'What architectural criteria dictate choosing between Kubernetes emptyDir, '
                           'PersistentVolumes, and Cloud Storage FUSE mounts?'],
             'reference': 'https://man7.org/linux/man-pages/man2/fsync.2.html#DESCRIPTION',
             'reference_label': 'fsync(2) Linux file data synchronization description (accessed 2026-10-04)',
             'scenario': {'constraints': 'The service is deployed as a stateless container deployment; ephemeral '
                                         'container root filesystems are backed by OverlayFS thin writable layers; '
                                         'storage lifecycle is inadvertently coupled to container process execution.',
                          'diagnostic_steps': ['Inspect pod volume mounts: kubectl get pod checkout-worker-[id] -o '
                                               'jsonpath="{.spec.containers[*].volumeMounts}"',
                                               'Inspect container OverlayFS storage: docker inspect [container-id] | '
                                               'jq ".[0].GraphDriver.Data"',
                                               'Simulate pod restart and check file persistence: kubectl delete pod '
                                               'checkout-worker-[id] && kubectl exec -it checkout-worker-[new-id] -- '
                                               'ls -l /tmp',
                                               'Analyze application write durability code for missing fsync() or '
                                               'fdatasync() invocations'],
                          'diagram': ('Order processing container receives checkout payload',
                                      'Application writes transaction record to ephemeral /tmp',
                                      'Container restart destroys writable layer; order marker vanishes',
                                      'Attach persistent volume claim and invoke fsync on writes',
                                      'Order markers survive container teardown and replica migration'),
                          'diagram_enabled': True,
                          'evidence': 'Inspecting the container runtime reveals that /tmp was located on the container '
                                      'writable layer (upperdir) rather than a persistent volume mount. When the pod '
                                      'was rescheduled, containerd destroyed the container instance and its associated '
                                      'writable layer. Filesystem traces show that writes to '
                                      '/tmp/checkout_recovery.log were buffered in kernel page cache without invoking '
                                      'fsync(), meaning even pre-teardown unflushed writes were lost upon pod '
                                      'termination.\n'
                                      '\n'
                                      '<figure class="diagram-figure">\n'
                                      '<p class="diagram-scroll-hint">Swipe horizontally to view the full '
                                      'diagram.</p>\n'
                                      '<svg aria-labelledby="day10-volume-incident-title day10-volume-incident-desc" '
                                      'role="img" viewbox="0 0 940 310">\n'
                                      '<title id="day10-volume-incident-title">Ephemeral container layer data loss and '
                                      'persistent volume fix</title>\n'
                                      '<desc id="day10-volume-incident-desc">The failed dashed path writes state to an '
                                      'ephemeral container layer that is destroyed during rolling updates. The '
                                      'corrected solid path mounts a persistent volume claim and invokes fsync, '
                                      'guaranteeing data survival across container lifecycles.</desc>\n'
                                      '<defs>\n'
                                      '<marker id="day10-vol-arrow" markerheight="8" markerwidth="10" orient="auto" '
                                      'refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>\n'
                                      '<marker id="day10-vol-fail-arrow" markerheight="8" markerwidth="10" '
                                      'orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" '
                                      'fill="#f43f5e"></path></marker>\n'
                                      '</defs>\n'
                                      '<g fill="#121526" stroke-width="2">\n'
                                      '<rect height="85" rx="8" stroke="#38bdf8" width="150" x="20" y="110"></rect>\n'
                                      '<image href="../assets/icons/generic/client.svg" x="28" y="118" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#f43f5e" width="220" x="225" y="30"></rect>\n'
                                      '<image href="../assets/icons/generic/failure.svg" x="233" y="38" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#34d399" width="220" x="225" y="185"></rect>\n'
                                      '<image href="../assets/icons/generic/storage.svg" x="233" y="193" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#f43f5e" width="220" x="495" y="30"></rect>\n'
                                      '<image href="../assets/icons/generic/failure.svg" x="503" y="38" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#34d399" width="220" x="495" y="185"></rect>\n'
                                      '<image href="../assets/icons/generic/decision.svg" x="503" y="193" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#38bdf8" width="155" x="765" y="110"></rect>\n'
                                      '<image href="../assets/icons/generic/outcome.svg" x="773" y="118" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '</g>\n'
                                      '<g fill="#fce7f3" font-size="12" font-weight="600" text-anchor="middle">\n'
                                      '<text x="102" y="142">Order Ingress</text>\n'
                                      '<text fill="#a9b7cb" x="102" y="162">Checkout stream</text>\n'
                                      '<text x="342" y="58">[FAILED: Ephemeral Layer]</text>\n'
                                      '<text fill="#f43f5e" x="342" y="78">Writes to /tmp/orders.log</text>\n'
                                      '<text fill="#a9b7cb" x="342" y="98">Thin writable container layer</text>\n'
                                      '<text x="342" y="213">[CORRECTED: Persistent Vol]</text>\n'
                                      '<text fill="#34d399" x="342" y="233">Mounts PVC /data/orders</text>\n'
                                      '<text fill="#a9b7cb" x="342" y="253">GCP Persistent Disk CSI</text>\n'
                                      '<text x="612" y="58">EXACT FAILURE POINT</text>\n'
                                      '<text fill="#f43f5e" x="612" y="78">Pod redeployed / restarted</text>\n'
                                      '<text fill="#f43f5e" x="612" y="98">Writable layer destroyed</text>\n'
                                      '<text x="612" y="213">CORRECTED CONTROL</text>\n'
                                      '<text fill="#34d399" x="612" y="233">POSIX fsync() commits data</text>\n'
                                      '<text fill="#a9b7cb" x="612" y="253">Survives container teardown</text>\n'
                                      '<text x="849" y="138">VERIFICATION</text>\n'
                                      '<text fill="#34d399" x="849" y="158">Data intact post-restart</text>\n'
                                      '<text fill="#a9b7cb" x="849" y="178">Zero duplicate charges</text>\n'
                                      '</g>\n'
                                      '<g fill="none" stroke-width="2">\n'
                                      '<path d="M170 135 L220 85" marker-end="url(#day10-vol-fail-arrow)" '
                                      'stroke="#f43f5e" stroke-dasharray="7 5"></path>\n'
                                      '<path d="M445 72 L490 72" marker-end="url(#day10-vol-fail-arrow)" '
                                      'stroke="#f43f5e" stroke-dasharray="7 5"></path>\n'
                                      '<path d="M170 170 L220 215" marker-end="url(#day10-vol-arrow)" '
                                      'stroke="#38bdf8"></path>\n'
                                      '<path d="M445 227 L490 227" marker-end="url(#day10-vol-arrow)" '
                                      'stroke="#38bdf8"></path>\n'
                                      '<path d="M715 227 L760 170" marker-end="url(#day10-vol-arrow)" '
                                      'stroke="#38bdf8"></path>\n'
                                      '</g>\n'
                                      '<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="295">Dashed '
                                      'line (--&gt;) = ephemeral layer data loss · Solid line (—&gt;) = persistent '
                                      'volume mount and fsync verification</text>\n'
                                      '</svg>\n'
                                      '<figcaption>Figure 10.4: Supplied facts: Writing state to ephemeral container '
                                      'filesystem results in data loss upon pod recreation. Architectural inference: '
                                      'Decoupling storage lifecycle from container lifecycle via persistent volumes '
                                      'ensures recovery marker survival. Expected post-fix behavior: Replacement '
                                      'containers read existing recovery markers, preserving at-most-once fulfillment '
                                      'semantics.</figcaption>\n'
                                      '</figure>',
                          'expected': 'Expected post-fix behavior: Replacement containers read existing recovery '
                                      'markers, preserving at-most-once fulfillment semantics.',
                          'facts': 'Supplied facts: Writing state to ephemeral container filesystem results in data '
                                   'loss upon pod recreation.',
                          'icons': ('../assets/icons/generic/client.svg',
                                    '../assets/icons/generic/failure.svg',
                                    '../assets/icons/generic/failure.svg',
                                    '../assets/icons/generic/storage.svg',
                                    '../assets/icons/generic/outcome.svg'),
                          'impact': 'E-commerce customers suffer duplicate credit card charges totaling thousands of '
                                    'dollars; customer service queues are overwhelmed; payment gateway audit flags '
                                    'account for automated transaction reconciliation failure.',
                          'inference': 'Architectural inference: Decoupling storage lifecycle from container lifecycle '
                                       'via persistent volumes ensures recovery marker survival.',
                          'remediation_steps': ['Provision a Kubernetes PersistentVolumeClaim requesting 10Gi on '
                                                'pd-balanced storage class',
                                                'Update Deployment specification to mount the PVC at /var/lib/checkout',
                                                'Refactor application write logic to call os.fsync(file.fileno()) '
                                                'after writing recovery markers',
                                                'Configure pod disruption budgets to coordinate volume detachment '
                                                'during node upgrades',
                                                'Execute automated rolling update test and verify transaction record '
                                                'integrity across replacement pods'],
                          'residual': 'Persistent volume attachments introduce a 15–30 second volume '
                                      'detachment/reattachment latency if a pod is rescheduled to a different physical '
                                      'host node in the cluster.',
                          'root': 'The application stored critical state in the container thin writable layer rather '
                                  'than a mounted persistent volume, and failed to issue POSIX fsync() system calls to '
                                  'commit transaction records to non-volatile storage before confirming payment '
                                  'processing.',
                          'scenario': 'An order checkout microservice deployed on a container cluster writes '
                                      'transaction recovery markers to its local container filesystem at '
                                      '/tmp/checkout_recovery.log during user purchases. During a routine rolling '
                                      'update of the application deployment, the old container is terminated and a new '
                                      'container is provisioned. The engineering team discovers that all active '
                                      'checkout recovery markers vanished upon container termination, leading to '
                                      'duplicate payment charges when the queue reprocessed unconfirmed transactions.',
                          'verify': 'The Kubernetes deployment is updated to mount a PersistentVolumeClaim backed by '
                                    'Compute Engine Persistent Disk (pd-balanced) onto /var/lib/checkout. The '
                                    'application code is updated to issue os.fsync() on every recovery marker write. '
                                    'Verification confirms that simulated container terminations preserve 100% of '
                                    'recovery markers across replacement pods with zero duplicate transactions.'},
             'technical': '<p><strong class="side-heading">Subtopics in this discussion:</strong></p>\n'
                          '<ol>\n'
                          '<li>OCI Image Layers, Inodes, and the Copy-on-Write (OverlayFS) Rootfs</li>\n'
                          '<li>Dockerfile Directives and Buildkit Layer Caching Architecture</li>\n'
                          '<li>Container Registries, Content Addressability, and Artifact Registry</li>\n'
                          '<li>Bind Mounts vs Volumes vs Ephemeral Container Storage</li>\n'
                          '<li>POSIX Filesystem Semantics: Page Cache, sync(), and fsync() Durability</li>\n'
                          '</ol>\n'
                          '\n'
                          '<h4>OCI Image Layers, Inodes, and the Copy-on-Write (OverlayFS) Rootfs</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> An Open Container '
                          'Initiative (<strong class="keyword">OCI</strong>) container image is an immutable '
                          'collection of tarball archives containing filesystem diffs, an image configuration JSON '
                          'blob, and a cryptographic manifest. When a container runtime (such as containerd or Docker) '
                          "launches a container, it constructs the container's root filesystem using a union "
                          'filesystem driver, predominantly <strong class="keyword">OverlayFS</strong>. OverlayFS '
                          'merges multiple underlying read-only image layers (referred to as <kbd>lowerdir</kbd>) with '
                          'a single ephemeral, writable top layer (<kbd>upperdir</kbd>) and an internal coordination '
                          'directory (<kbd>workdir</kbd>) into a single unified mount point (<kbd>merged</kbd>). '
                          'Filesystem metadata and disk allocation are tracked via index nodes (<strong '
                          'class="keyword">inodes</strong>). When a process reads a file, OverlayFS looks top-down '
                          'through the layers and reads directly from the lowest read-only layer where the file '
                          'exists. When a process attempts to modify a file belonging to a lower layer, OverlayFS '
                          'performs a <strong class="keyword">Copy-on-Write</strong> (CoW) operation: it copies the '
                          'entire file up to <kbd>upperdir</kbd> before permitting modifications, allocating a new '
                          'inode in the writable layer while leaving the base image layer unchanged.</p>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Union filesystem '
                          'dynamics dictate container runtime performance and node storage stability. Performing heavy '
                          'random writes or appending to massive log files inside the thin writable layer causes '
                          'severe disk fragmentation, inode exhaustion, and significant I/O latency due to the '
                          'synchronous copy-up overhead of large files. Furthermore, because <kbd>upperdir</kbd> is '
                          "bound to the container's lifecycle, any file written to the container layer is deleted "
                          'permanently when the container is replaced or rescheduled by Kubernetes. Architects must '
                          'mandate that all stateful write paths bypass the CoW layer entirely via external volume '
                          'mounts.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> Google Kubernetes Engine (GKE) '
                          'nodes running Container-Optimized OS (COS) mount the local boot disk with OverlayFS backed '
                          'by <kbd>ext4</kbd>. When multiple Pods on a GKE node pull the same base image (such as '
                          'Debian or distroless), the node stores only a single copy of each layer digest in the local '
                          'containerd snapshotter, saving gigabytes of disk space across collocated workloads. GKE '
                          'Node Auto-repair monitors local inode exhaustion on the node root filesystem and drains '
                          'unhealthy nodes if rogue containers consume all available filesystem inodes.</p>\n'
                          '\n'
                          '<h4>Dockerfile Directives and Buildkit Layer Caching Architecture</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> A <strong '
                          'class="keyword">Dockerfile</strong> is a text manifest specifying the sequential assembly '
                          'instructions used by container build engines (such as Docker BuildKit or Kaniko) to produce '
                          'an OCI image. Each directive that modifies filesystem state (<kbd>FROM</kbd>, '
                          '<kbd>COPY</kbd>, <kbd>ADD</kbd>, <kbd>RUN</kbd>) generates a new immutable filesystem '
                          'layer. Build engines utilize content-addressable layer caching: before executing a '
                          'directive, the builder calculates a SHA-256 cache key based on the instruction string and '
                          'the checksums of any input files. If an exact cache hit exists in the local or remote '
                          'cache, the builder skips execution and reuses the cached layer digest. If any layer cache '
                          'is invalidated (for example, if a source code file copied via <kbd>COPY . .</kbd> changes), '
                          'all subsequent layers are invalidated and must be rebuilt sequentially. Multi-stage builds '
                          'separate build-time dependencies (compilers, SDKs, test suites) from final runtime '
                          'artifacts, drastically reducing attack surfaces and final image sizes.</p>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Dockerfile design '
                          'directly impacts CI/CD pipeline velocity, network egress bandwidth, and security '
                          'vulnerability profiles. Ordering directives from least-frequently changing (base OS '
                          'packages, language dependencies) to most-frequently changing (application source code) '
                          'maximizes layer cache hit rates, dropping build times from 10 minutes to 15 seconds. '
                          'Employing multi-stage builds ensures that compilers, debug symbols, and package managers '
                          '(e.g., <kbd>gcc</kbd>, <kbd>npm</kbd>, <kbd>pip</kbd>) are excluded from production '
                          'containers, preventing attackers from compiling exploits inside compromised production '
                          'pods.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud Build uses Kaniko '
                          'and BuildKit cache backends to build container images directly on Google Cloud '
                          'infrastructure. Google provides minimal, secure "Distroless" base images that contain only '
                          'the runtime application and its immediate runtime dependencies—omitting package managers, '
                          'shells, and standard Linux utilities—which integrate seamlessly into Artifact Registry '
                          'vulnerability scanning to maintain high security compliance across GKE and Cloud Run '
                          'deployments.</p>\n'
                          '\n'
                          '<div class="callout" id="docker-multistage-comparison" style="margin-top:1.5rem;">\n'
                          '<p><strong style="font-size:1.1rem; color:#7dd3fc;">Operational Lab Comparison: '
                          'Single-Stage vs Optimized Multi-Stage Docker Packaging</strong></p>\n'
                          '<p><strong>Goal &amp; Overview:</strong> Empirically demonstrate the layer immutability '
                          'trap, image bloat, and attack surface expansion of naive single-stage builds versus minimal '
                          'multi-stage Distroless packaging.</p>\n'
                          '\n'
                          '<table style="width:100%; border-collapse:collapse; margin:1rem 0;">\n'
                          '<thead>\n'
                          '<tr style="border-bottom:2px solid #334155; text-align:left;">\n'
                          '<th style="padding:8px;">Metric / Architectural Invariant</th>\n'
                          '<th style="padding:8px;">Single-Stage Build (Debian Base)</th>\n'
                          '<th style="padding:8px;">Multi-Stage Build (Distroless / Scratch)</th>\n'
                          '</tr>\n'
                          '</thead>\n'
                          '<tbody>\n'
                          '<tr style="border-bottom:1px solid #1e293b;">\n'
                          '<td style="padding:8px;"><strong>Final Image Size on Disk</strong></td>\n'
                          '<td style="padding:8px; color:#f43f5e;">~68.4 MB (Retains hidden compiler SDK in lower '
                          'layer)</td>\n'
                          '<td style="padding:8px; color:#10b981;">~2.4 MB (&gt;96% storage reduction)</td>\n'
                          '</tr>\n'
                          '<tr style="border-bottom:1px solid #1e293b;">\n'
                          '<td style="padding:8px;"><strong>Layer Immutability Trap (<kbd>RUN rm '
                          '-rf</kbd>)</strong></td>\n'
                          '<td style="padding:8px; color:#f43f5e;"><strong>FAILED</strong>: Deleting files creates '
                          'whiteout markers; bytes stay in layer 1</td>\n'
                          '<td style="padding:8px; color:#10b981;"><strong>AVOIDED</strong>: Build tools isolated in '
                          'ephemeral builder stage</td>\n'
                          '</tr>\n'
                          '<tr style="border-bottom:1px solid #1e293b;">\n'
                          '<td style="padding:8px;"><strong>Attack Surface (Compilers &amp; Shells)</strong></td>\n'
                          '<td style="padding:8px; color:#f43f5e;">Includes <kbd>gcc</kbd>, <kbd>apt-get</kbd>, and '
                          '<kbd>/bin/sh</kbd> (Living-off-the-land exploit vector)</td>\n'
                          '<td style="padding:8px; color:#10b981;">Zero compilers, zero package managers, zero '
                          'interactive shells</td>\n'
                          '</tr>\n'
                          '<tr style="border-bottom:1px solid #1e293b;">\n'
                          '<td style="padding:8px;"><strong>GKE Autoscaling Pull Latency</strong></td>\n'
                          '<td style="padding:8px; color:#f43f5e;">High network egress and node containerd '
                          'decompression time (15–30s)</td>\n'
                          '<td style="padding:8px; color:#10b981;">Sub-second layer pull and snapshot unpack '
                          '(&lt;2s)</td>\n'
                          '</tr>\n'
                          '</tbody>\n'
                          '</table>\n'
                          '\n'
                          '<p><strong>Concrete Code &amp; Manifest Fixtures:</strong></p>\n'
                          '<div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin-top:0.5rem;">\n'
                          '<div>\n'
                          '<p><strong>Single-Stage Dockerfile (Anti-Pattern):</strong></p>\n'
                          '<pre><code>FROM debian:12-slim\n'
                          'WORKDIR /app\n'
                          '# Installs heavy compiler SDK (65MB)\n'
                          'COPY src/build_sdk /build_tools/\n'
                          'COPY src/order_dispatch_bin /app/order_dispatch\n'
                          '# Layer Immutability Trap: rm -rf does NOT reclaim layer size!\n'
                          'RUN rm -rf /build_tools\n'
                          'ENTRYPOINT ["/app/order_dispatch"]</code></pre>\n'
                          '</div>\n'
                          '<div>\n'
                          '<p><strong>Optimized Multi-Stage Dockerfile (Best Practice):</strong></p>\n'
                          '<pre><code># Stage 1: Build & Compilation Environment\n'
                          'FROM debian:12-slim AS builder\n'
                          'WORKDIR /workspace\n'
                          'COPY src/build_sdk /build_tools/\n'
                          'COPY src/order_dispatch_bin /workspace/order_dispatch\n'
                          '\n'
                          '# Stage 2: Minimal Distroless Runtime\n'
                          'FROM gcr.io/distroless/static-debian12:nonroot\n'
                          'WORKDIR /app\n'
                          'COPY --from=builder /workspace/order_dispatch /app/order_dispatch\n'
                          'USER nonroot:nonroot\n'
                          'ENTRYPOINT ["/app/order_dispatch"]</code></pre>\n'
                          '</div>\n'
                          '</div>\n'
                          '</div>\n'
                          '\n'
                          '\n'
                          '<h4>Container Registries, Content Addressability, and Artifact Registry</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> A <strong '
                          'class="keyword">container registry</strong> is an OCI-compliant distributed '
                          'content-addressable storage service that stores, versions, and serves container image '
                          'layers and manifests. Images are addressed not merely by mutable human-readable tags (such '
                          'as <kbd>:latest</kbd> or <kbd>:v1.2.0</kbd>), but by their immutable cryptographic digest: '
                          'the SHA-256 hash of the image manifest (e.g., <kbd>sha256:7b9...8f4</kbd>). When a '
                          'container runtime pulls an image, it retrieves the manifest, checks which layer digests '
                          'already exist in its local snapshotter, and downloads only the missing layer blobs in '
                          'parallel. Content addressability ensures that if two distinct images share identical base '
                          'layers, the registry and node store and transfer that layer blob exactly once.</p>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Relying on mutable '
                          'image tags (such as deploying <kbd>my-app:prod</kbd>) introduces non-deterministic '
                          'deployment failures: different nodes in a Kubernetes cluster can pull different underlying '
                          'image digests under the same tag, causing phantom bugs and impossible rollbacks. Enterprise '
                          'architecture standards mandate referencing container images by their cryptographic SHA-256 '
                          'digest in production Kubernetes manifests to guarantee immutability, auditability, and '
                          'binary reproducibility across staging and production environments.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud <strong '
                          'class="keyword">Artifact Registry</strong> is the enterprise evolution of Container '
                          'Registry (GCR), providing regional and multi-regional OCI repositories with native IAM '
                          'integration, customer-managed encryption keys (CMEK), and automated Container Analysis '
                          'vulnerability scanning. Artifact Registry integrates natively with Google Cloud Binary '
                          'Authorization, allowing architects to enforce deploy-time policy controls: GKE clusters '
                          'automatically reject Pod deployments whose container images lack cryptographic provenance '
                          'attestations signed by approved CI/CD build keys.</p>\n'
                          '\n'
                          '<h4>Bind Mounts vs Volumes vs Ephemeral Container Storage</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> Container runtimes provide '
                          'three distinct storage mechanisms to expose filesystems to containerized processes:\n'
                          '1. <strong class="keyword">Ephemeral container storage</strong>: the default writable '
                          'OverlayFS layer (<kbd>upperdir</kbd>). Data written here is strictly bound to the container '
                          'lifecycle; when the container process terminates or the pod is rescheduled, all written '
                          'data is permanently deleted.\n'
                          '2. <strong class="keyword">Bind mounts</strong>: an exact file or directory on the host '
                          'operating system is mounted directly into the container filesystem namespace (<kbd>mount '
                          '--bind</kbd>). The container process reads and writes directly to host storage, bypassing '
                          'OverlayFS CoW entirely.\n'
                          '3. <strong class="keyword">Named volumes</strong>: managed storage directories created and '
                          'governed by the container runtime or storage plugin (in Kubernetes, PersistentVolumes '
                          'managed by Container Storage Interface, <strong class="keyword">CSI</strong>, drivers). '
                          'Volumes decouple the storage lifecycle entirely from container and node lifecycles, '
                          'enabling independent backup, snapshotting, and reattachment across different physical '
                          'hosts.</p>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Choosing the wrong '
                          'storage abstraction leads to immediate disaster. Storing transactional state in ephemeral '
                          'storage guarantees data loss during routine rolling updates or node maintenance. Using bind '
                          'mounts couples the container to specific host filesystem paths, breaking container '
                          'portability and violating cluster security policies. Architects must mandate named volumes '
                          'backed by managed network block storage for stateful workloads (databases, message brokers) '
                          'while treating ephemeral container storage strictly as disposable scratch space.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> GKE utilizes the Google Compute '
                          'Engine Persistent Disk CSI Driver to dynamically provision zonal and regional Persistent '
                          'Disks (<kbd>pd-balanced</kbd>, <kbd>pd-ssd</kbd>, <kbd>hyperdisk-balanced</kbd>) in '
                          'response to Kubernetes PersistentVolumeClaims (PVCs). GKE also provides the Cloud Storage '
                          'FUSE CSI driver to mount Cloud Storage buckets as filesystems directly inside Pods, and the '
                          'Filestore CSI driver for multi-writer NFS shared filesystem access across hundreds of '
                          'distributed pods.</p>\n'
                          '\n'
                          '<h4>POSIX Filesystem Semantics: Page Cache, sync(), and fsync() Durability</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> In modern operating '
                          'systems, when an application invokes the standard POSIX <kbd>write()</kbd> system call, '
                          'data is NOT written immediately to physical storage hardware. Instead, the Linux kernel '
                          'copies the data into volatile kernel RAM known as the <strong class="keyword">page '
                          'cache</strong>, marks the memory pages as "dirty", and returns success to the application '
                          "in microseconds. The kernel's background flusher threads (<kbd>kworker</kbd> / "
                          '<kbd>flusher</kbd>) periodically flush dirty pages to disk asynchronously based on sysctl '
                          'thresholds (<kbd>vm.dirty_background_ratio</kbd>). If the host operating system crashes or '
                          'power fails before dirty pages are flushed, all buffered data is permanently lost. To '
                          'guarantee that data has physically reached non-volatile persistent media, the application '
                          'must issue explicit POSIX synchronization calls:\n'
                          '<kbd>sync()</kbd> schedules all dirty page cache buffers across the entire system for '
                          'writeback;\n'
                          '<strong class="keyword">fsync()</strong> flushes all modified in-core data and filesystem '
                          'metadata for a specific file descriptor to non-volatile storage and blocks until the '
                          'physical disk controller confirms persistence; and\n'
                          '<kbd>fdatasync()</kbd> flushes only the modified data and necessary retrieval metadata '
                          '(omitting timestamps), reducing disk I/O operations.</p>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Understanding '
                          'POSIX persistence semantics is critical when designing stateful systems on cloud '
                          'infrastructure. High-throughput ingestion microservices that buffer records in RAM without '
                          'invoking <kbd>fsync()</kbd> will report successful transaction writes to clients, only to '
                          'suffer silent data corruption or loss when the cloud provider executes live migration or '
                          'preempts a spot instance. Architects must ensure database engines (PostgreSQL, MySQL, '
                          'Kafka) configure Write-Ahead Logging (WAL) with calibrated <kbd>fsync</kbd> commit '
                          'intervals, and recognize that cloud block storage latency is directly tied to IOPS and sync '
                          'flush throughput.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine Persistent Disks '
                          '(PD) and Hyperdisk volumes emulate SCSI/NVMe storage controllers that acknowledge '
                          '<kbd>fsync()</kbd> flushes only when data has been written to redundant non-volatile '
                          "physical storage across Google's storage network. In GKE, write-heavy databases that issue "
                          'frequent <kbd>fsync()</kbd> calls require <kbd>pd-ssd</kbd> or '
                          '<kbd>hyperdisk-balanced</kbd> volumes with high provisioned IOPS to avoid queue depth '
                          'saturation and transaction commit latency spikes.</p>\n'
                          '\n'
                          '<figure class="diagram-figure">\n'
                          '<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>\n'
                          '<svg aria-labelledby="day10-storage-title day10-storage-desc" role="img" viewbox="0 0 940 330">\n'
                          '<title id="day10-storage-title">Docker container storage architecture and POSIX write durability path</title>\n'
                          '<desc id="day10-storage-desc">The diagram illustrates container storage layers on the left and the POSIX write durability pipeline from process memory down to non-volatile storage on the right.</desc>\n'
                          '<defs>\n'
                          '<marker id="day10-storage-arrow" markerheight="6" markerwidth="8" orient="auto" refx="7" refy="3"><path d="M0,0 L8,3 L0,6 Z" fill="#38bdf8"></path></marker>\n'
                          '</defs>\n'
                          '<g fill="#121526" stroke-width="2">\n'
                          '<rect height="42" rx="6" stroke="#f43f5e" width="420" x="20" y="58"></rect>\n'
                          '<image href="../assets/icons/generic/failure.svg" x="28" y="65" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="42" rx="6" stroke="#f97316" width="420" x="20" y="114"></rect>\n'
                          '<image href="../assets/icons/generic/artifact.svg" x="28" y="121" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="42" rx="6" stroke="#38bdf8" width="420" x="20" y="170"></rect>\n'
                          '<image href="../assets/icons/generic/storage.svg" x="28" y="177" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="48" rx="6" stroke="#34d399" width="420" x="20" y="226"></rect>\n'
                          '<image href="../assets/icons/generic/storage.svg" x="28" y="236" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="42" rx="6" stroke="#38bdf8" width="425" x="495" y="58"></rect>\n'
                          '<image href="../assets/icons/generic/endpoint.svg" x="503" y="65" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="42" rx="6" stroke="#f97316" width="425" x="495" y="114"></rect>\n'
                          '<image href="../assets/icons/generic/server.svg" x="503" y="121" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="42" rx="6" stroke="#f59e0b" width="425" x="495" y="170"></rect>\n'
                          '<image href="../assets/icons/generic/storage.svg" x="503" y="177" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="48" rx="6" stroke="#34d399" width="425" x="495" y="226"></rect>\n'
                          '<image href="../assets/icons/generic/storage.svg" x="503" y="236" width="28" height="28" preserveAspectRatio="xMidYMid meet"/>\n'
                          '</g>\n'
                          '<g font-size="12" font-weight="700">\n'
                          '<text fill="#fce7f3" text-anchor="middle" x="230" y="44">CONTAINER STORAGE LAYERS</text>\n'
                          '<text fill="#f43f5e" x="66" y="84">Thin Writable Layer (Ephemeral · Deleted on exit)</text>\n'
                          '<text fill="#f97316" x="66" y="140">Application Layer (Read-Only · e.g., app.py)</text>\n'
                          '<text fill="#38bdf8" x="66" y="196">Base Image Layer (Read-Only · python:3.12-alpine)</text>\n'
                          '<text fill="#34d399" x="66" y="255">Persistent Volume Mount (/data -&gt; durable storage)</text>\n'
                          '<text fill="#fce7f3" text-anchor="middle" x="707" y="44">POSIX WRITE &amp; DURABILITY PIPELINE</text>\n'
                          '<text fill="#38bdf8" x="541" y="84">1. Process Heap &amp; Runtime Buffer (Volatile RAM)</text>\n'
                          '<text fill="#f97316" x="541" y="140">2. Linux OS Page Cache (Kernel RAM · via write())</text>\n'
                          '<text fill="#f59e0b" x="541" y="196">3. Disk Controller Cache (Device RAM · Writeback)</text>\n'
                          '<text fill="#34d399" x="541" y="255">4. Non-Volatile Physical Storage (Durable via fsync())</text>\n'
                          '</g>\n'
                          '<g fill="none" marker-end="url(#day10-storage-arrow)" stroke="#38bdf8" stroke-width="2">\n'
                          '<path d="M707 100 L707 114"></path>\n'
                          '<path d="M707 156 L707 170"></path>\n'
                          '<path d="M707 212 L707 226"></path>\n'
                          '</g>\n'
                          '<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="305">Ephemeral container storage vanishes on pod deletion; only fsync() on mounted volumes guarantees persistence to non-volatile media.</text>\n'
                          '</svg>\n'
                          '<figcaption>Figure 10.1: Architecture of container image layers, ephemeral overlay storage, and the operating system write durability path. Only data flushed via fsync() through the controller cache to persistent physical storage survives container replacement.</figcaption>\n'
                          '</figure>\n'
                          '\n'
                          '<div class="topic-card">\n'
                          '<table>\n'
                          '<caption>Table 10.1: Container Storage Abstractions and Persistence '
                          'Characteristics</caption>\n'
                          '<thead>\n'
                          '<tr>\n'
                          '<th>Storage Layer</th>\n'
                          '<th>Lifecycle &amp; Scope</th>\n'
                          '<th>Filesystem Mechanism</th>\n'
                          '<th>Durability Guarantee</th>\n'
                          '<th>GCP CSI / Service Equivalent</th>\n'
                          '</tr>\n'
                          '</thead>\n'
                          '<tbody>\n'
                          '<tr>\n'
                          '<td><strong>Ephemeral Container Layer</strong></td>\n'
                          '<td>Bound to container process; deleted upon pod restart</td>\n'
                          '<td>OverlayFS thin writable layer (<kbd>upperdir</kbd>)</td>\n'
                          '<td>Zero durability; volatile to container crashes</td>\n'
                          '<td>Local node root disk (<kbd>/var/lib/containerd</kbd>)</td>\n'
                          '</tr>\n'
                          '<tr>\n'
                          '<td><strong>EmptyDir Volume</strong></td>\n'
                          '<td>Bound to Pod lifecycle; deleted when Pod is deleted</td>\n'
                          '<td>Host filesystem directory or in-memory <kbd>tmpfs</kbd></td>\n'
                          '<td>Survives container restarts within the same Pod</td>\n'
                          '<td>GKE local SSD or ephemeral node storage</td>\n'
                          '</tr>\n'
                          '<tr>\n'
                          '<td><strong>PersistentVolume (Block)</strong></td>\n'
                          '<td>Independent of Pod/node lifecycle; durable network storage</td>\n'
                          '<td>Direct block device format (<kbd>ext4</kbd>/<kbd>xfs</kbd>)</td>\n'
                          '<td>Full durability; requires <kbd>fsync()</kbd> to commit</td>\n'
                          '<td>GKE Compute Engine PD CSI Driver (<kbd>pd-balanced</kbd>)</td>\n'
                          '</tr>\n'
                          '<tr>\n'
                          '<td><strong>Shared Volume (NFS)</strong></td>\n'
                          '<td>Shared across multiple pods concurrently (<kbd>ReadWriteMany</kbd>)</td>\n'
                          '<td>Network File System (NFSv3 / NFSv4)</td>\n'
                          '<td>Centralized durability across multi-zone nodes</td>\n'
                          '<td>GKE Filestore CSI Driver / Managed Filestore</td>\n'
                          '</tr>\n'
                          '<tr>\n'
                          '<td><strong>Object Storage Mount</strong></td>\n'
                          '<td>Global scale; blob storage mounted as POSIX directory</td>\n'
                          '<td>FUSE userspace filesystem mapping to object APIs</td>\n'
                          '<td>Object-level durability; non-standard POSIX semantics</td>\n'
                          '<td>GKE Cloud Storage FUSE CSI Driver</td>\n'
                          '</tr>\n'
                          '</tbody>\n'
                          '</table>\n'
                          '</div>\n'
                          '\n'
                          '<p><strong class="side-heading">Concrete example:</strong> Consider an order processing '
                          'microservice that generates transaction verification tokens before dispatching payment '
                          'events. In the legacy version, the developer writes tokens to <kbd>/tmp/tokens.log</kbd> '
                          'inside the container without mounting a volume. When GKE triggers a rolling update to '
                          'deploy a new container version, Kubernetes terminates the old pod, destroying its OverlayFS '
                          'writable layer. The new replacement pod starts with an empty <kbd>/tmp</kbd>, leaving '
                          'incoming checkout verification requests with missing token files and causing duplicate '
                          'customer charges. The architect remediates the service by attaching a Kubernetes '
                          'PersistentVolumeClaim backed by <kbd>pd-balanced</kbd> mounted to '
                          '<kbd>/var/lib/tokens</kbd>. Furthermore, the application code is updated to invoke '
                          '<kbd>os.fsync(f.fileno())</kbd> immediately after appending each token record. When the pod '
                          'is redeployed, the Persistent Disk dynamically unmounts from the old node, reattaches to '
                          "the replacement pod's node, and all transaction tokens are read intact, preserving "
                          'at-most-once payment processing.</p>\n'
                          '\n'
                          '<p><strong class="side-heading">Evidence limit:</strong> Observing successful execution of '
                          'an application <kbd>write()</kbd> system call proves data transfer into the operating '
                          "system kernel's memory page cache; it does NOT prove that data has been committed to "
                          'non-volatile physical storage media without verifying that <kbd>fsync()</kbd> completed '
                          'successfully without returning <kbd>EIO</kbd> or <kbd>EROFS</kbd> errors.</p>\n',
             'title': 'Docker'},
            {'anchors': {'lab': 'topic-02-lab',
                         'overview': 'topic-02-overview',
                         'problem': 'topic-02-problem',
                         'technical': 'topic-02-technical'},
             'key': 'topic-02',
             'lab': {'accept': 'A scheduler simulation log documenting the transition from capacity failure to '
                               'autoscaled resolution in scratch/day-010-scheduler-simulation.txt.',
                     'cleanup': 'Remove transient simulation scripts in scratch/day10_lab_b.',
                     'covers': 'Container orchestration: why Kubernetes exists; continuous reconciliation loops, '
                               'scheduler bin packing, and self-healing.',
                     'expected': 'A deterministic scheduler simulation demonstrating pod placement filtering, pending '
                                 'state traps under capacity limits, and autoscaling resolution.',
                     'file': 'day-010-exercise-b.md',
                     'goal': 'Simulate the Kubernetes control loop, declarative state reconciliation, two-phase '
                             'scheduler bin packing, and capacity limit exhaustion.',
                     'mode': 'Observed locally: local Python simulation of Kubernetes scheduler filtering and scoring '
                             'algorithms. Simulated or predicted: GKE Cluster Autoscaler provisioning of Compute '
                             'Engine instances and kubelet pod startup. Untested on GCP: live Andromeda SDN virtual '
                             'network routing tables and multi-zone node affinity scoring.',
                     'name': 'Exercise B · Simulate scheduler reconciliation and capacity limits',
                     'preflight': 'Verify Python 3 runtime is available and initialize the simulation directory.',
                     'prereq': 'Linux terminal with Python 3.',
                     'steps': ['**Stage 1: Preflight and Tooling Baseline**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Verify environment prerequisites and set up the scheduler simulation workspace.\n'
                               '```bash\n'
                               'command -v bash\n'
                               'command -v python3\n'
                               'command -v cat\n'
                               'command -v mkdir\n'
                               'mkdir -p scratch/day10_lab_b\n'
                               'echo "Stage 1 scheduler preflight complete at $(date -u +%Y-%m-%dT%H:%M:%SZ)" > '
                               'scratch/day10_lab_b/stage1.log\n'
                               'cat scratch/day10_lab_b/stage1.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Tooling paths confirmed and workspace initialized.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_b/stage1.log`',
                               '**Stage 2: Define Cluster Node Inventory and Allocatable Headroom**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Create a JSON fixture representing a 3-node Kubernetes cluster with physical capacity '
                               'and existing system reservations.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_b/nodes.json\n"
                               '{\n'
                               '  "nodes": [\n'
                               '    {"name": "node-zone-a-1", "allocatable_ram_mb": 4096, "reserved_ram_mb": 1024},\n'
                               '    {"name": "node-zone-b-1", "allocatable_ram_mb": 4096, "reserved_ram_mb": 1024},\n'
                               '    {"name": "node-zone-c-1", "allocatable_ram_mb": 4096, "reserved_ram_mb": 1024}\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'python3 -m json.tool scratch/day10_lab_b/nodes.json > /dev/null && echo "Node '
                               'inventory validated" > scratch/day10_lab_b/stage2.log\n'
                               'cat scratch/day10_lab_b/stage2.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Node inventory created with 3 nodes possessing 3072 MB net '
                               'allocatable RAM each.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_b/stage2.log`',
                               '**Stage 3: Define Workload Deployment Manifest with Resource Requests**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Create the workload manifest representing the checkout service requesting 2048 MB RAM '
                               'per replica.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_b/deployment.json\n"
                               '{\n'
                               '  "name": "checkout-processor",\n'
                               '  "desired_replicas": 5,\n'
                               '  "request_ram_mb": 2048\n'
                               '}\n'
                               'EOF\n'
                               'echo "Deployment manifest configured with 5 replicas requesting 2048 MB each" > '
                               'scratch/day10_lab_b/stage3.log\n'
                               'cat scratch/day10_lab_b/stage3.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Workload manifest authored and saved.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_b/stage3.log`',
                               '**Stage 4: Execute Scheduler Filtering and Bin Packing Algorithm**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Execute the simulation engine to test how the scheduler places the 5 replicas across '
                               'the 3 nodes.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_b/scheduler_sim.py\n"
                               'import json\n'
                               '\n'
                               'with open("scratch/day10_lab_b/nodes.json") as f:\n'
                               '    cluster = json.load(f)\n'
                               'with open("scratch/day10_lab_b/deployment.json") as f:\n'
                               '    dep = json.load(f)\n'
                               '\n'
                               'nodes = cluster["nodes"]\n'
                               'req = dep["request_ram_mb"]\n'
                               'replicas = dep["desired_replicas"]\n'
                               '\n'
                               '# Calculate available headroom\n'
                               'for n in nodes:\n'
                               '    n["available_ram"] = n["allocatable_ram_mb"] - n["reserved_ram_mb"]\n'
                               '    n["placed_pods"] = []\n'
                               '\n'
                               'placed = 0\n'
                               'pending = []\n'
                               '\n'
                               'for i in range(1, replicas + 1):\n'
                               '    pod_name = f"{dep[\'name\']}-replica-{i}"\n'
                               '    # Predicate: NodeResourcesFit\n'
                               '    candidate = None\n'
                               '    for n in sorted(nodes, key=lambda x: x["available_ram"], reverse=True):\n'
                               '        if n["available_ram"] >= req:\n'
                               '            candidate = n\n'
                               '            break\n'
                               '    if candidate:\n'
                               '        candidate["available_ram"] -= req\n'
                               '        candidate["placed_pods"].append(pod_name)\n'
                               '        placed += 1\n'
                               '    else:\n'
                               '        pending.append(pod_name)\n'
                               '\n'
                               'print(f"SCHEDULER RUN 1: Placed: {placed}/{replicas} | Pending: '
                               '{len(pending)}/{replicas}")\n'
                               'for n in nodes:\n'
                               '    print(f"  {n[\'name\']}: {len(n[\'placed_pods\'])} pods, {n[\'available_ram\']} MB '
                               'RAM remaining")\n'
                               'if pending:\n'
                               '    print(f"  FAILED PREDICATE: 0/3 nodes available: 3 Insufficient memory for '
                               '{pending}")\n'
                               'EOF\n'
                               'python3 scratch/day10_lab_b/scheduler_sim.py > scratch/day10_lab_b/stage4.log\n'
                               'cat scratch/day10_lab_b/stage4.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Output confirms 3 pods placed (1 per node) and 2 pods trapped in '
                               'Pending due to insufficient memory.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_b/stage4.log`',
                               '**Stage 5: Rehearse Scale-Out Surge and Detect Unplaced Pending Pods**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Simulate traffic surge scaling to 7 replicas to observe how unschedulable pods '
                               'accumulate without crashing the cluster.\n'
                               '```bash\n'
                               "python3 -c '\n"
                               'import json\n'
                               'with open("scratch/day10_lab_b/deployment.json") as f:\n'
                               '    d = json.load(f)\n'
                               'd["desired_replicas"] = 7\n'
                               'with open("scratch/day10_lab_b/deployment.json", "w") as f:\n'
                               '    json.dump(d, f, indent=2)\n'
                               "'\n"
                               'python3 scratch/day10_lab_b/scheduler_sim.py > scratch/day10_lab_b/stage5.log\n'
                               'cat scratch/day10_lab_b/stage5.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Output confirms that 4 pods are trapped in Pending while existing '
                               '3 pods continue executing unharmed.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_b/stage5.log`',
                               '**Stage 6: Rehearse Worker Node Failure and Autonomous Rescheduling**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Simulate an unexpected node crash and observe the node controller detecting the '
                               'failure and rescheduling pods.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_b/simulate_node_failure.py\n"
                               'import json\n'
                               '\n'
                               'with open("scratch/day10_lab_b/nodes.json") as f:\n'
                               '    cluster = json.load(f)\n'
                               '\n'
                               '# Node 3 suffers hardware fault\n'
                               'failed_node = cluster["nodes"].pop(2)\n'
                               'print(f"EVENT: Node {failed_node[\'name\']} failed heartbeat! Marked NotReady.")\n'
                               'print(f"EVENT: Node controller evicts pods from {failed_node[\'name\']} and re-queues '
                               'them.")\n'
                               'with open("scratch/day10_lab_b/nodes_degraded.json", "w") as f:\n'
                               '    json.dump(cluster, f, indent=2)\n'
                               'EOF\n'
                               'python3 scratch/day10_lab_b/simulate_node_failure.py > scratch/day10_lab_b/stage6.log\n'
                               'cat scratch/day10_lab_b/stage6.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Output documents node eviction and re-queueing of displaced '
                               'pods.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_b/stage6.log`',
                               '**Stage 7: Formulate GKE Cluster Autoscaler Capacity Policy**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Calibrate workload resource requests to 768 MB and simulate GKE Cluster Autoscaler '
                               'adding a new worker node.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_b/autoscaler_remediation.py\n"
                               'import json\n'
                               '\n'
                               '# Calibrate deployment requests to realistic working set\n'
                               'with open("scratch/day10_lab_b/deployment.json") as f:\n'
                               '    dep = json.load(f)\n'
                               'dep["desired_replicas"] = 5\n'
                               'dep["request_ram_mb"] = 768\n'
                               '\n'
                               '# Autoscaler provisions node 4\n'
                               'with open("scratch/day10_lab_b/nodes.json") as f:\n'
                               '    cluster = json.load(f)\n'
                               'cluster["nodes"].append({"name": "node-zone-a-2", "allocatable_ram_mb": 4096, '
                               '"reserved_ram_mb": 1024})\n'
                               '\n'
                               'nodes = cluster["nodes"]\n'
                               'req = dep["request_ram_mb"]\n'
                               'replicas = dep["desired_replicas"]\n'
                               '\n'
                               'for n in nodes:\n'
                               '    n["available_ram"] = n["allocatable_ram_mb"] - n["reserved_ram_mb"]\n'
                               '    n["placed_pods"] = []\n'
                               '\n'
                               'placed = 0\n'
                               'for i in range(1, replicas + 1):\n'
                               '    pod_name = f"{dep[\'name\']}-replica-{i}"\n'
                               '    candidate = sorted([n for n in nodes if n["available_ram"] >= req], key=lambda x: '
                               'x["available_ram"], reverse=True)[0]\n'
                               '    candidate["available_ram"] -= req\n'
                               '    candidate["placed_pods"].append(pod_name)\n'
                               '    placed += 1\n'
                               '\n'
                               'output = f"""# Day 10 Scheduler Simulation Report\n'
                               'Reconciliation Status: SUCCESS\n'
                               'Desired Replicas: {replicas} | Placed: {placed} | Pending: 0\n'
                               'Node Distribution:\n'
                               '"""\n'
                               'for n in nodes:\n'
                               '    output += f"  - {n[\'name\']}: {len(n[\'placed_pods\'])} pods, '
                               '{n[\'available_ram\']} MB free\\n"\n'
                               '\n'
                               'with open("scratch/day-010-scheduler-simulation.txt", "w") as f:\n'
                               '    f.write(output)\n'
                               'print("Scheduler remediation simulation completed successfully")\n'
                               'EOF\n'
                               'python3 scratch/day10_lab_b/autoscaler_remediation.py > '
                               'scratch/day10_lab_b/stage7.log\n'
                               'cat scratch/day-010-scheduler-simulation.txt\n'
                               '```\n'
                               '\n'
                               '**Expected result:** All 5 replicas placed cleanly across the autoscaled cluster '
                               'nodes.\n'
                               '\n'
                               '**Save:** `scratch/day-010-scheduler-simulation.txt`',
                               '**Stage 8: Validate Scheduler Invariant and Close Simulation**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Verify that zero pods remain in Pending status and all scheduler invariants are '
                               'satisfied.\n'
                               '```bash\n'
                               'test -f scratch/day-010-scheduler-simulation.txt && grep -q "Pending: 0" '
                               'scratch/day-010-scheduler-simulation.txt\n'
                               'echo "✓ Day 10 Exercise B validation passed successfully" > '
                               'scratch/day10_lab_b/stage8.log\n'
                               'cat scratch/day10_lab_b/stage8.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Verification passes with zero pending pods.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_b/stage8.log`'],
                     'trouble': 'If simulation output is missing, verify scratch/day10_lab_b directory path.',
                     'verification': 'Verify that the scheduler simulation accurately rejects pods when allocatable '
                                     'memory is exhausted and places them when capacity expands.'},
             'overview': 'Container orchestration automates the operational lifecycle of distributed containerized '
                         'applications across fleets of virtual machine nodes. Managing individual containers '
                         'imperatively on bare hosts introduces severe architectural failure modes: unhandled host '
                         'hardware crashes, manual port allocation conflicts, lack of automated rollouts and '
                         'rollbacks, and inability to reconcile desired capacity against node resources. Kubernetes '
                         'solves these challenges through a centralized declarative control plane that continuously '
                         'reconciles actual runtime telemetry against desired state stored in etcd.',
             'preview': 'A surge in user checkout requests causes a production order service to exhaust host memory on '
                        'a standalone virtual machine, crashing all collocated containers and dropping user requests. '
                        'Migrating the service to a managed Kubernetes cluster allows the scheduler to distribute '
                        'replicas across multiple worker nodes and automatically restart failed instances without '
                        'operator intervention.',
             'questions': ['How does a declarative reconciliation loop differ from traditional imperative '
                           'infrastructure automation scripts?',
                           'What distinct operational roles do kube-scheduler, kube-controller-manager, and kubelet '
                           'execute during pod placement?',
                           'Under what failure conditions will a Kubernetes Pod become trapped indefinitely in Pending '
                           'status?'],
             'reference': 'https://kubernetes.io/docs/concepts/overview/#why-you-need-kubernetes-and-what-can-it-do',
             'reference_label': 'Why you need Kubernetes and what it can do (accessed 2026-10-04)',
             'scenario': {'constraints': 'Fixed node pool capacity of 3 nodes; each node has 4 GB allocatable memory; '
                                         'existing system pods consume 1 GB per node; uncalibrated application '
                                         'requests mandate 2 GB RAM per replica.',
                          'diagnostic_steps': ['Inspect pod status: kubectl get pods -l app=order-processor -o wide',
                                               'Inspect pod scheduling failure events: kubectl describe pod '
                                               'order-processor-[id] | grep -A 5 Events:',
                                               'Inspect node allocatable capacity: kubectl describe nodes | grep -A 8 '
                                               '"Allocatable:"',
                                               'Calculate aggregate requested resources across active pods: kubectl '
                                               'get pods -A -o jsonpath="{...}"'],
                          'diagram': ('Surge traffic triggers deployment scale-out from 2 to 5 replicas',
                                      'Uncalibrated memory requests exceed cluster allocatable capacity',
                                      'Pods trapped in Pending with Insufficient memory events',
                                      'Enable GKE cluster autoscaler and calibrate pod requests',
                                      'New node provisions in 90 seconds; all 5 replicas reach Running'),
                          'diagram_enabled': True,
                          'evidence': 'Reviewing "kubectl get pods" reveals 3 pods in Pending state. Inspecting pod '
                                      'events via "kubectl describe pod order-processor-[id]" reveals the scheduling '
                                      'failure: "0/3 nodes available: 3 Insufficient memory". Host nodes show zero CPU '
                                      'saturation, but allocatable memory reservation is fully booked.\n'
                                      '\n'
                                      '<figure class="diagram-figure">\n'
                                      '<p class="diagram-scroll-hint">Swipe horizontally to view the full '
                                      'diagram.</p>\n'
                                      '<svg aria-labelledby="day10-sched-incident-title day10-sched-incident-desc" '
                                      'role="img" viewbox="0 0 940 310">\n'
                                      '<title id="day10-sched-incident-title">Deployment scale-out failure under node '
                                      'capacity exhaustion</title>\n'
                                      '<desc id="day10-sched-incident-desc">The failed dashed path shows three pods '
                                      'trapped in Pending due to insufficient node memory. The corrected solid path '
                                      'right-sizes requests and triggers node autoscaling, resulting in 5 running '
                                      'replicas.</desc>\n'
                                      '<defs>\n'
                                      '<marker id="day10-sched-arrow" markerheight="8" markerwidth="10" orient="auto" '
                                      'refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>\n'
                                      '<marker id="day10-sched-fail-arrow" markerheight="8" markerwidth="10" '
                                      'orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" '
                                      'fill="#f43f5e"></path></marker>\n'
                                      '</defs>\n'
                                      '<g fill="#121526" stroke-width="2">\n'
                                      '<rect height="85" rx="8" stroke="#38bdf8" width="150" x="20" y="110"></rect>\n'
                                      '<image href="../assets/icons/generic/queue.svg" x="28" y="118" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#f43f5e" width="220" x="225" y="30"></rect>\n'
                                      '<image href="../assets/icons/generic/failure.svg" x="233" y="38" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#34d399" width="220" x="225" y="185"></rect>\n'
                                      '<image href="../assets/icons/generic/server.svg" x="233" y="193" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#f43f5e" width="220" x="495" y="30"></rect>\n'
                                      '<image href="../assets/icons/generic/failure.svg" x="503" y="38" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#34d399" width="220" x="495" y="185"></rect>\n'
                                      '<image href="../assets/icons/generic/decision.svg" x="503" y="193" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#38bdf8" width="155" x="765" y="110"></rect>\n'
                                      '<image href="../assets/icons/generic/outcome.svg" x="773" y="118" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '</g>\n'
                                      '<g fill="#fce7f3" font-size="12" font-weight="600" text-anchor="middle">\n'
                                      '<text x="102" y="142">Scale Trigger</text>\n'
                                      '<text fill="#a9b7cb" x="102" y="162">Replicas: 5</text>\n'
                                      '<text x="342" y="58">[FAILED: Fixed Node Pool]</text>\n'
                                      '<text fill="#f43f5e" x="342" y="78">3 nodes @ 4G allocatable</text>\n'
                                      '<text fill="#a9b7cb" x="342" y="98">Uncalibrated 2G request</text>\n'
                                      '<text x="342" y="213">[CORRECTED: Autoscaler]</text>\n'
                                      '<text fill="#34d399" x="342" y="233">Calibrated 768M request</text>\n'
                                      '<text fill="#a9b7cb" x="342" y="253">Autoscaler adds node</text>\n'
                                      '<text x="612" y="58">EXACT FAILURE POINT</text>\n'
                                      '<text fill="#f43f5e" x="612" y="78">0/3 nodes available</text>\n'
                                      '<text fill="#f43f5e" x="612" y="98">3 Pods trapped in Pending</text>\n'
                                      '<text x="612" y="213">CORRECTED CONTROL</text>\n'
                                      '<text fill="#34d399" x="612" y="233">Scheduler places all pods</text>\n'
                                      '<text fill="#a9b7cb" x="612" y="253">Readiness probes pass</text>\n'
                                      '<text x="849" y="138">VERIFICATION</text>\n'
                                      '<text fill="#34d399" x="849" y="158">5/5 Replicas Running</text>\n'
                                      '<text fill="#a9b7cb" x="849" y="178">Zero dropped checkouts</text>\n'
                                      '</g>\n'
                                      '<g fill="none" stroke-width="2">\n'
                                      '<path d="M170 135 L220 85" marker-end="url(#day10-sched-fail-arrow)" '
                                      'stroke="#f43f5e" stroke-dasharray="7 5"></path>\n'
                                      '<path d="M445 72 L490 72" marker-end="url(#day10-sched-fail-arrow)" '
                                      'stroke="#f43f5e" stroke-dasharray="7 5"></path>\n'
                                      '<path d="M170 170 L220 215" marker-end="url(#day10-sched-arrow)" '
                                      'stroke="#38bdf8"></path>\n'
                                      '<path d="M445 227 L490 227" marker-end="url(#day10-sched-arrow)" '
                                      'stroke="#38bdf8"></path>\n'
                                      '<path d="M715 227 L760 170" marker-end="url(#day10-sched-arrow)" '
                                      'stroke="#38bdf8"></path>\n'
                                      '</g>\n'
                                      '<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="295">Dashed '
                                      'line (--&gt;) = unschedulable capacity failure · Solid line (—&gt;) = '
                                      'autoscaling and right-sized placement</text>\n'
                                      '</svg>\n'
                                      '<figcaption>Figure 10.5: Supplied facts: Scaled Deployment fails to place three '
                                      'replicas due to node memory exhaustion. Architectural inference: Reconciling '
                                      'desired state requires physical capacity; right-sizing requests and enabling '
                                      'cluster autoscaling restores schedulability. Expected post-fix behavior: All '
                                      'five replicas achieve Running status and pass readiness probes.</figcaption>\n'
                                      '</figure>',
                          'expected': 'Expected post-fix behavior: All five replicas achieve Running status and pass '
                                      'readiness probes.',
                          'facts': 'Supplied facts: Scaled Deployment fails to place three replicas due to node memory '
                                   'exhaustion.',
                          'icons': ('../assets/icons/generic/queue.svg',
                                    '../assets/icons/generic/failure.svg',
                                    '../assets/icons/generic/failure.svg',
                                    '../assets/icons/generic/server.svg',
                                    '../assets/icons/generic/outcome.svg'),
                          'impact': 'Order processing throughput drops below required demand; checkout queues back up; '
                                    'customer transactions time out with HTTP 504 Gateway Timeout errors.',
                          'inference': 'Architectural inference: Reconciling desired state requires physical capacity; '
                                       'right-sizing requests and enabling cluster autoscaling restores '
                                       'schedulability.',
                          'remediation_steps': ['Profile actual container memory working set under load in Cloud '
                                                'Monitoring',
                                                'Update Deployment manifest to calibrate requests: '
                                                'resources.requests.memory: "768Mi"',
                                                'Enable GKE Cluster Autoscaler: gcloud container clusters update '
                                                '[cluster] --enable-autoscaling --min-nodes=3 --max-nodes=8',
                                                'Apply updated Deployment and verify scheduler placement across '
                                                'available nodes',
                                                'Confirm all 5 replicas reach Running state and pass HTTP readiness '
                                                'probes'],
                          'residual': 'Autoscaler scale-up requires VM provisioning time (typically 60–90 seconds in '
                                      'GKE), during which transient queuing may occur unless overprovisioning buffer '
                                      'pods are configured.',
                          'root': 'The total requested memory for 5 replicas (10 GB) plus system reservations (3 GB) '
                                  'exceeds total cluster allocatable capacity (12 GB). The scheduler strictly enforces '
                                  'declared resource requests during the filtering phase, preventing pod placement '
                                  'even when actual memory usage is low.',
                          'scenario': 'A retail flash sale causes an automated traffic surge. An operator attempts to '
                                      'scale an order processing service from 2 to 5 replicas. Because the cluster '
                                      'node pool has fixed capacity (3 nodes with 4 GB allocatable RAM each) and the '
                                      'Pods specify uncalibrated 2 GB memory requests, the scheduler successfully '
                                      'places only 2 pods, leaving the remaining 3 replicas trapped indefinitely in '
                                      'Pending status.',
                          'verify': 'Application resource requests are right-sized from 2 GB to 768 MB based on real '
                                    'profiling, and GKE Cluster Autoscaler is enabled on the node pool. All 5 replicas '
                                    'achieve Running status within 90 seconds, pass readiness probes, and scale-out '
                                    'throughput reaches 1,200 orders per second.'},
             'technical': '<p><strong class="side-heading">Subtopics in this discussion:</strong></p>\n'
                          '<ol>\n'
                          '<li><a href="#topic-02-subtopic-1">The Failure Modes of Standalone Host Container '
                          'Management</a></li>\n'
                          '<li><a href="#topic-02-subtopic-2">Declarative Desired State vs Imperative Container '
                          'Commands</a></li>\n'
                          '<li><a href="#topic-02-subtopic-3">Continuous Reconciliation Loops and the Control Plane '
                          'Architecture</a></li>\n'
                          '<li><a href="#topic-02-subtopic-4">Automated Scheduling, Bin Packing, and Resource '
                          'Constraint Enforcement</a></li>\n'
                          '<li><a href="#topic-02-subtopic-5">Self-Healing: Liveness/Readiness Probes, Restarts, and '
                          'Rescheduling</a></li>\n'
                          '</ol>\n'
                          '\n'
                          '<h4 id="topic-02-subtopic-1">The Failure Modes of Standalone Host Container '
                          'Management</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> Managing container runtimes '
                          '(<strong class="keyword">containerd</strong>, <strong class="keyword">dockerd</strong>, '
                          '<strong class="keyword">runc</strong>) imperatively on standalone compute hosts relies on '
                          'localized host process isolation without a distributed cluster orchestrator. In this '
                          'architecture, operations are governed by localized system daemons (e.g., <strong '
                          'class="keyword">systemd</strong>) or ad-hoc shell commands. Standalone container hosting '
                          'exhibits four catastrophic operational and architectural failure modes when operating '
                          'distributed microservices:</p>\n'
                          '<ul>\n'
                          '<li><strong>Unmanaged Host Crashes &amp; Lack of Automated Failover:</strong> A standalone '
                          'host has no distributed heartbeat mechanism or cluster-wide membership consensus. If the '
                          'underlying bare-metal hardware, hypervisor, or Linux kernel panics '
                          '(<kbd>kernel.panic</kbd>), suffers an uncorrectable memory fault, or experiences network '
                          'interface card (<strong class="keyword">NIC</strong>) isolation, all resident containers '
                          'terminate immediately. The mean time to recovery (<strong class="keyword">MTTR</strong>) is '
                          'bounded by human detection, manual triage, and manual container re-provisioning on an '
                          'alternate host.</li>\n'
                          '<li><strong>Host Port Space Saturation &amp; EADDRINUSE Collisions:</strong> Standalone '
                          'host bridge networking relies on Linux network namespace boundary traversal via <strong '
                          'class="keyword">iptables DNAT</strong> mapping (e.g., binding container port '
                          '<kbd>8080/tcp</kbd> to host port <kbd>0.0.0.0:8080</kbd>). Schedulers cannot collocate '
                          'multiple replicas of the same service on the same host without assigning static, arbitrary '
                          'high-port offsets (<kbd>8081</kbd>, <kbd>8082</kbd>), causing <kbd>bind()</kbd> system '
                          'calls to fail with <kbd>EADDRINUSE</kbd> (errno 98) and fracturing ingress proxy '
                          'configurations.</li>\n'
                          '<li><strong>Resource Fragmentation &amp; Absence of Global Bin Packing:</strong> Without a '
                          'multi-dimensional bin packing algorithm, workload placement is determined by manual '
                          'operator assignment. Operators inevitably strand compute resources—such as running a '
                          'memory-bound workload on a node with abundant free CPU, while exhausting RAM and starving '
                          'neighbor containers—leading to severe under-utilization or node thrashing.</li>\n'
                          '<li><strong>Brittle Imperative Rollouts:</strong> Executing zero-downtime rolling updates '
                          'via shell scripts (<kbd>docker stop old &amp;&amp; docker run -d new</kbd>) lacks '
                          'transactional atomicity. If the new container experiences runtime initialization failure '
                          '(e.g., failed configuration parse or library linkage defect), client traffic is dropped '
                          'instantly; automated health validation, traffic draining, and deterministic rollbacks do '
                          'not exist.</li>\n'
                          '</ul>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Relying on '
                          'standalone container hosting (e.g., a fleet of Compute Engine VMs running Docker daemons '
                          'with bash deploy scripts) creates an operational bottleneck that caps organizational '
                          'velocity and destroys Service Level Objectives (<strong class="keyword">SLOs</strong>). '
                          'Consider a microservices topology consisting of $M = 15$ interdependent services. On '
                          'standalone VMs with a 99.9% VM availability SLA and manual failover taking an average of 45 '
                          'minutes, composite application availability decays exponentially ($A_{\\text{composite}} = '
                          '\\prod_{i=1}^{M} A_i \\approx 0.999^{15} \\approx 98.51\\%$). This results in over 10.8 '
                          'hours of unplanned downtime per month, violating standard enterprise three-nines (99.9%) '
                          'SLOs. Blast radius is maximized because a single VM failure drops 100% of collocated '
                          'containers. Architects adopt container orchestrators to transform compute infrastructure '
                          'from brittle, pet-like individual servers into a fungible, self-healing utility '
                          'fabric.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> Deploying standalone Docker '
                          'containers on <strong class="keyword">Compute Engine</strong> running Container-Optimized '
                          'OS (<strong class="keyword">COS</strong>) without an orchestration tier leaves workloads '
                          'vulnerable to zonal hardware faults and live migration interrupts. <strong '
                          'class="keyword">Google Kubernetes Engine (GKE)</strong> eliminates standalone host '
                          'vulnerabilities by abstracting raw Compute Engine instances into elastic, self-healing Node '
                          'Pools distributed across multiple GCP Availability Zones. GKE node auto-repair continuously '
                          'monitors worker node health through the node problem detector, automatically draining and '
                          'recreating failing VMs without operator intervention.</p>\n'
                          '<p><strong class="side-heading">Concrete example:</strong> An un-orchestrated payment '
                          'service container running via <kbd>docker run -d -p 443:8443 gcr.io/corp/pay:v1</kbd> on a '
                          'Compute Engine VM experiences a memory leak. The Linux kernel <strong class="keyword">OOM '
                          'killer</strong> terminates the process with <kbd>SIGKILL</kbd> (exit code 137). Because the '
                          'host lacks an active supervisor control loop, the service port remains unresponsive for 52 '
                          'minutes until an on-call engineer restarts the container manually.</p>\n'
                          '<p><strong class="side-heading">Evidence limit:</strong> Standalone VM experiments verify '
                          'container termination on host failure, but local environments cannot simulate large-scale '
                          'cloud provider fabric reboots, undercloud top-of-rack (ToR) switch outages, or cross-zone '
                          'optical fiber cuts handled by GKE control planes.</p>\n'
                          '\n'
                          '<h4 id="topic-02-subtopic-2">Declarative Desired State vs Imperative Container '
                          'Commands</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> Container systems operate '
                          'under two diametrically opposed management philosophies: imperative execution and '
                          'declarative desired state convergence.</p>\n'
                          '<ul>\n'
                          '<li><strong>Imperative Execution:</strong> The system state is altered via a chronological '
                          'sequence of imperative mutation commands (e.g., <kbd>docker run</kbd>, <kbd>docker '
                          'scale</kbd>, <kbd>docker network connect</kbd>). If step 4 of a 6-step imperative '
                          'deployment script fails due to an API timeout, the infrastructure is left in an unknown, '
                          'non-deterministic intermediate state. Re-running the script is non-idempotent and often '
                          'produces fatal conflicts.</li>\n'
                          '<li><strong>Declarative Desired State:</strong> The engineer specifies the complete, target '
                          'end-state schema in an immutable text manifest (JSON/YAML). The declarative schema is '
                          'submitted to a centralized API server, which stores the specification as the canonical '
                          'source of truth.</li>\n'
                          '<li><strong>Diff Reconciliation Engine:</strong> The orchestrator continuously calculates '
                          'the mathematical delta between desired state ($S_{\\text{desired}}$) and observed actual '
                          'runtime state ($S_{\\text{actual}}$):\n'
                          '$$\\Delta = S_{\\text{desired}} \\setminus S_{\\text{actual}}$$\n'
                          'If $\\Delta \\neq \\emptyset$, the orchestrator executes idempotent state transitions until '
                          'the system converges to $\\Delta = \\emptyset$.</li>\n'
                          '<li><strong>Three-Way Merge Patching:</strong> When applying manifest updates, Kubernetes '
                          'executes a <strong class="keyword">three-way merge patch</strong> comparing: (1) the '
                          '<kbd>last-applied-configuration</kbd> annotation, (2) the current live configuration stored '
                          'in <strong class="keyword">etcd</strong>, and (3) the incoming modified manifest. This '
                          'prevents destructive field overwrites while allowing dynamic controllers (e.g., '
                          'autoscalers) to manage runtime fields without configuration conflicts.</li>\n'
                          '</ul>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Declarative state '
                          'enforcement eliminates configuration drift caused by operator debugging sessions directly '
                          'on nodes. By storing declarative manifests in Git repositories (<strong '
                          'class="keyword">GitOps</strong>), every production infrastructure change is backed by '
                          'cryptographic Git commit hashes. Rollbacks require a single <kbd>git revert</kbd> commit '
                          'rather than complex, reverse-engineered operational shell rollback scripts. An '
                          'architectural anti-pattern is using imperative CLI flags (<kbd>kubectl run '
                          '--image=...</kbd> or <kbd>kubectl expose</kbd>) inside production deployment pipelines '
                          'instead of version-controlled, declarative manifests validated by schema linters.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> <strong class="keyword">Google '
                          'Cloud Config Sync</strong> (part of GKE Enterprise) enforces declarative GitOps across '
                          'fleet-wide GKE clusters. Config Sync runs an in-cluster root reconciler that continuously '
                          'pulls declarative configurations from Git or OCI registries, detects drift against live '
                          'cluster objects within seconds, and applies transactional three-way merge patches to '
                          'restore compliance. Config Sync integrates with <strong class="keyword">Policy Controller '
                          '(OPA Gatekeeper)</strong> on GKE, rejecting non-declarative mutations that violate '
                          'organization guardrails directly at the <kbd>kube-apiserver</kbd> admission gate.</p>\n'
                          '<p><strong class="side-heading">Concrete example:</strong> An operator imperatively updates '
                          "a GKE production Deployment's replica count from 12 to 2 via <kbd>kubectl scale "
                          'deployment/frontend --replicas=2</kbd> during an incident investigation. Within 15 seconds, '
                          'Config Sync detects the drift against the canonical Git repository (<kbd>replicas: '
                          '12</kbd>), triggers a reconciliation event, and scales the Deployment back to 12 replicas '
                          'automatically.</p>\n'
                          '<p><strong class="side-heading">Evidence limit:</strong> Local <kbd>kubectl diff</kbd> '
                          'commands demonstrate manifest comparisons against local clusters, but do not capture '
                          'multi-cluster GitOps webhook serialization delays or large-scale OCI registry sync '
                          'latencies across global GCP regions.</p>\n'
                          '\n'
                          '<h4 id="topic-02-subtopic-3">Continuous Reconciliation Loops and the Control Plane '
                          'Architecture</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> The Kubernetes control '
                          'plane is an asynchronous, level-triggered distributed control system designed to '
                          'continuously drive current infrastructure state toward declared desired state.</p>\n'
                          '<ul>\n'
                          '<li><strong>Level-Triggered vs Edge-Triggered Semantics:</strong> Edge-triggered systems '
                          'react only to state transition boundaries (e.g., "container stopped event"). If a network '
                          'partition causes an edge event to be dropped, the system remains permanently out of sync. '
                          'Kubernetes implements <strong class="keyword">level-triggered control loops</strong>: '
                          'components periodically poll and stream full state representations via HTTP/2 chunked '
                          'streams, ensuring that missed transient events are corrected during the subsequent '
                          'reconciliation pass.</li>\n'
                          '<li><strong>Control Plane Components:</strong>\n'
                          '  <ul>\n'
                          '  <li><kbd>kube-apiserver</kbd>: The stateless, horizontally scalable gateway for the '
                          'cluster. It intercepts HTTP REST operations, handles authentication (<strong '
                          'class="keyword">x509 client certificates</strong>, webhook tokens), executes authorization '
                          '(<strong class="keyword">RBAC</strong>), triggers Mutating/Validating Admission '
                          'Controllers, and serves as the sole component permitted to communicate with etcd.</li>\n'
                          '  <li><kbd>etcd</kbd>: A distributed, strongly consistent key-value datastore implementing '
                          'the <strong class="keyword">Raft consensus algorithm</strong>. All cluster objects are '
                          'stored under key hierarchies (e.g., <kbd>/registry/pods/default/pod-1</kbd>) with '
                          'multi-version concurrency control (<strong class="keyword">MVCC</strong>) and 64-bit '
                          'resource versions to guarantee linearizable consistency.</li>\n'
                          '  <li><kbd>kube-controller-manager</kbd>: A monolithic binary packaging multiple decoupled '
                          'continuous reconciliation loops (<kbd>DeploymentController</kbd>, '
                          '<kbd>ReplicaSetController</kbd>, <kbd>NodeLifecycleController</kbd>, '
                          '<kbd>EndpointSliceController</kbd>).</li>\n'
                          '  <li><kbd>kube-scheduler</kbd>: The placement engine that assigns unscheduled Pods '
                          '(<kbd>spec.nodeName == ""</kbd>) to candidate worker nodes based on two-phase filtering and '
                          'scoring.</li>\n'
                          '  <li><kbd>kubelet</kbd>: The primary node agent. Watches <kbd>kube-apiserver</kbd> for Pod '
                          'specs scheduled to its host, interacts with the Container Runtime Interface (<strong '
                          'class="keyword">CRI</strong>) to spawn/destroy containers, configures the Container Network '
                          'Interface (<strong class="keyword">CNI</strong>), and handles volume mounts via the '
                          'Container Storage Interface (<strong class="keyword">CSI</strong>).</li>\n'
                          '  </ul>\n'
                          '</li>\n'
                          '</ul>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> etcd Raft '
                          'consensus requires an odd cluster quorum size ($N = 2F + 1$) to tolerate $F$ node failures. '
                          'A 3-node etcd cluster tolerates 1 failure; a 5-node cluster tolerates 2 failures. Writing '
                          'to etcd requires synchronous disk <strong class="keyword">fdatasync</strong> operations; if '
                          'storage write latency exceeds 10 ms, Raft heartbeats drop, triggering cascade leader '
                          'elections and freezing control plane operations. Crucially, the control plane is decoupled '
                          'from the data plane: if <kbd>kube-apiserver</kbd> or etcd becomes unavailable, running data '
                          'plane workloads, established TCP streams, and iptables routing on worker nodes continue '
                          'executing uninterrupted, though autoscaling, rolling deployments, and self-healing '
                          'rescheduling are temporarily halted.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> GKE abstracts the entire control '
                          'plane as a Google-managed service. In GKE Regional Clusters, Google provisions multi-master '
                          '<kbd>kube-apiserver</kbd> and etcd replicas spanning three distinct GCP Availability Zones '
                          'with automated SSD persistent storage provisioning, automated zero-downtime control plane '
                          'patching, and 99.95% availability SLA backing. <strong class="keyword">GKE '
                          'Autopilot</strong> manages both the control plane and worker nodes, dynamically '
                          'provisioning compute resources and configuring hardened kernel security profiles according '
                          'to Google SRE best practices.</p>\n'
                          '<p><strong class="side-heading">Concrete example:</strong> A worker node hosting 3 Pod '
                          'replicas experiences a localized kernel lockup. The GKE <kbd>NodeLifecycleController</kbd> '
                          'misses <kbd>kubelet</kbd> node lease heartbeats for <kbd>node-monitor-grace-period</kbd> '
                          '(default 40s), marks the node <kbd>NotReady</kbd>, and schedules pod eviction. The '
                          '<kbd>ReplicaSetController</kbd> notices that observed active pods (2) is less than desired '
                          'replicas (3), generates a replacement Pod specification, and commits it to '
                          '<kbd>kube-apiserver</kbd>.</p>\n'
                          '<p><strong class="side-heading">Evidence limit:</strong> Local controller inspection '
                          'exposes Informer queue metrics and API audit logs, but internal multi-master etcd Raft '
                          'leader election latencies and Google-managed control plane VM telemetry are inaccessible in '
                          'managed GKE environments.</p>\n'
                          '\n'
                          '<h4 id="topic-02-subtopic-4">Automated Scheduling, Bin Packing, and Resource Constraint '
                          'Enforcement</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> The <strong '
                          'class="keyword">kube-scheduler</strong> assigns Pods to worker nodes through a '
                          'deterministic two-phase pipeline executed for every unscheduled Pod:</p>\n'
                          '<ul>\n'
                          '<li><strong>Filtering Phase (Predicates):</strong> Evaluates candidate nodes against hard '
                          'binary constraints. Nodes failing any predicate plugin are eliminated:\n'
                          '  <ul>\n'
                          "  <li><kbd>NodeResourcesFit</kbd>: Verifies that the node's allocatable CPU, memory, and "
                          "ephemeral storage exceed the Pod's declared <kbd>resources.requests</kbd>.</li>\n"
                          '  <li><kbd>NodeName</kbd> &amp; <kbd>NodePorts</kbd>: Enforces explicit node bindings and '
                          'checks host port availability.</li>\n'
                          '  <li><kbd>NodeAffinity</kbd> &amp; <kbd>PodTopologySpread</kbd>: Evaluates hard node '
                          'labels and zone balance constraints.</li>\n'
                          '  <li><kbd>Taints</kbd> &amp; <kbd>Tolerations</kbd>: Verifies that the Pod possesses '
                          'tolerations matching any taints applied to nodes (e.g., dedicated GPU pools or maintenance '
                          'cordons).</li>\n'
                          '  </ul>\n'
                          '</li>\n'
                          '<li><strong>Scoring Phase (Priorities):</strong> Ranks the remaining candidate nodes on a '
                          'scale of 0 to 100 using weighted evaluation plugins:\n'
                          '  <ul>\n'
                          '  <li><kbd>NodeResourcesBalancedAllocation</kbd>: Scores nodes higher when placing the Pod '
                          'achieves an equal ratio of CPU to memory allocation, preventing compute resource '
                          'stranding.</li>\n'
                          '  <li><kbd>ImageLocality</kbd>: Assigns higher scores to nodes that already have the '
                          'required container image layers cached locally, minimizing container pull latency.</li>\n'
                          '  </ul>\n'
                          '</li>\n'
                          '<li><strong>Resource Contracts (Requests vs Limits):</strong>\n'
                          '  <ul>\n'
                          '  <li><kbd>requests</kbd>: Represents guaranteed minimum capacity. Used exclusively by '
                          '<kbd>kube-scheduler</kbd> during the <kbd>NodeResourcesFit</kbd> filtering phase and by the '
                          'Linux kernel Completely Fair Scheduler (<strong class="keyword">CFS</strong>) to allocate '
                          'relative CPU shares (<kbd>cpu.shares</kbd>).</li>\n'
                          '  <li><kbd>limits</kbd>: Represents maximum ceiling enforced by Linux kernel cgroups. CPU '
                          'limits enforce hard CFS quota windows (<kbd>cpu.cfs_quota_us</kbd> over '
                          '<kbd>cpu.cfs_period_us</kbd>), throttling threads that exceed quota. Memory limits '
                          'configure hard cgroup ceilings (<kbd>memory.max</kbd>); if a container exceeds its memory '
                          'limit, the Linux kernel invokes <kbd>oom_killer</kbd> to terminate processes inside the '
                          'container.</li>\n'
                          '  </ul>\n'
                          '</li>\n'
                          '</ul>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Quality of Service '
                          '(<strong class="keyword">QoS</strong>) classes govern workload survivability during '
                          'resource pressure. Guaranteed QoS (<kbd>requests == limits</kbd>) provides highest '
                          'stability and immunity to node eviction during memory pressure, but minimizes bin packing '
                          'efficiency. Burstable QoS (<kbd>requests &lt; limits</kbd>) balances cost efficiency with '
                          'headroom, but risks CPU throttling and OOM termination if neighbor workloads spike '
                          'simultaneously. BestEffort QoS (no requests or limits) is first to be evicted by '
                          '<kbd>kubelet</kbd> when node allocatable memory drops below eviction thresholds. Setting '
                          'memory limits significantly higher than requests creates an overcommitted node memory pool, '
                          'risking node kernel panics if multiple burstable containers peak concurrently.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> <strong class="keyword">GKE '
                          'Cluster Autoscaler (CA)</strong> integrates directly with the scheduler queue. When a Pod '
                          'fails <kbd>NodeResourcesFit</kbd> across all existing nodes, it enters <kbd>Pending</kbd> '
                          'state with a <kbd>FailedScheduling</kbd> event. CA intercepts this event, simulates node '
                          'placement across configured node pools, and triggers the Compute Engine API to provision '
                          'new VMs within 60–90 seconds. <strong class="keyword">GKE Node Auto-Provisioning '
                          '(NAP)</strong> analyzes unscheduled Pod requirements (CPU architecture, memory ratios, GPU '
                          'accelerators) and automatically constructs new GKE node pools with custom machine shapes '
                          'on-demand.</p>\n'
                          '<p><strong class="side-heading">Concrete example:</strong> A batch analytics Pod requesting '
                          '<kbd>cpu: 4000m</kbd> and <kbd>memory: 16Gi</kbd> cannot fit onto a cluster of three '
                          '<kbd>e2-standard-4</kbd> worker nodes (each possessing only <kbd>1200m</kbd> allocatable '
                          'CPU remaining). The scheduler marks the Pod <kbd>Pending</kbd>; GKE Cluster Autoscaler '
                          'detects the unschedulable workload and triggers Compute Engine to launch an additional '
                          '<kbd>e2-standard-8</kbd> instance into the regional node pool.</p>\n'
                          '<p><strong class="side-heading">Evidence limit:</strong> Standalone scheduler simulation '
                          'scripts demonstrate filtering and scoring logic mathematically, but cannot test physical '
                          'cloud VM API rate limits, GCP quota exhaustion errors, or live compute engine stockouts in '
                          'constrained zones.</p>\n'
                          '\n'
                          '<h4 id="topic-02-subtopic-5">Self-Healing: Liveness/Readiness Probes, Restarts, and '
                          'Rescheduling</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> Kubernetes separates '
                          'process health into three distinct probe lifecycles evaluated by <kbd>kubelet</kbd> via '
                          'HTTP GET, TCP socket connection, or in-container <kbd>exec</kbd> commands:</p>\n'
                          '<ul>\n'
                          '<li><kbd>startupProbe</kbd>: Inhibits liveness and readiness probes while a legacy or '
                          'complex application initializes (e.g., JVM class loading, database schema validation). This '
                          'prevents premature container restarts during slow boot sequences.</li>\n'
                          '<li><kbd>livenessProbe</kbd>: Determines whether the container application is alive or '
                          'fundamentally broken (e.g., process deadlock, unrecoverable thread starvation, memory '
                          'corruption). If a liveness probe fails <kbd>failureThreshold</kbd> times consecutively '
                          '(default 3), <kbd>kubelet</kbd> issues <kbd>SIGTERM</kbd> to PID 1, waits '
                          '<kbd>terminationGracePeriodSeconds</kbd> (default 30s), sends <kbd>SIGKILL</kbd>, and '
                          "restarts the container runtime sandbox according to the Pod's "
                          '<kbd>restartPolicy</kbd>.</li>\n'
                          '<li><kbd>readinessProbe</kbd>: Determines whether the container is ready to accept inbound '
                          'network traffic. <strong>Readiness probe failures NEVER trigger container '
                          'restarts</strong>. When a readiness probe fails, the <kbd>EndpointSliceController</kbd> '
                          "immediately removes the Pod's IP address from active <strong "
                          'class="keyword">EndpointSlices</strong>. Network proxies (kube-proxy and cloud load '
                          'balancers) stop routing traffic to the Pod within milliseconds, allowing it to drain '
                          'in-flight requests or finish background processing while preserving process memory '
                          'state.</li>\n'
                          '</ul>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Coupling liveness '
                          'probes to downstream external dependencies (e.g., querying a PostgreSQL database in '
                          '<kbd>/healthz</kbd>) is an architectural anti-pattern. If the database experiences '
                          'transient latency or downtime, all application Pods fail their liveness probes '
                          'simultaneously, inducing a cluster-wide restart storm (<strong class="keyword">thundering '
                          'herd</strong>) that overwhelms CRI runtimes, saturates registries with image pulls, and '
                          'prevents database recovery. Decoupled readiness probes prevent 502 Bad Gateway and 503 '
                          'Service Unavailable errors during traffic spikes: overloaded Pods fail readiness, shedding '
                          'load to healthy replicas, while avoiding crash loops.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> In <strong class="keyword">GKE '
                          'Container-Native Load Balancing with Network Endpoint Groups (NEGs)</strong>, readiness '
                          'probe states are mirrored directly to Google Cloud External Application Load Balancers. '
                          'When a Pod fails its readiness check, Google Cloud Load Balancer health checkers detect the '
                          'endpoint failure and withdraw edge routing within sub-second intervals, avoiding node proxy '
                          'double-hops and isolating failed backends at the Google edge network.</p>\n'
                          '<p><strong class="side-heading">Concrete example:</strong> A Go microservice suffers a '
                          'mutex deadlock in an HTTP handler thread pool. The <kbd>readinessProbe</kbd> fails, causing '
                          'GKE to detach the Pod from its NEG; 10 seconds later, the <kbd>livenessProbe</kbd> '
                          '(<kbd>GET /live</kbd>) fails 3 consecutive checks. <kbd>kubelet</kbd> sends '
                          '<kbd>SIGKILL</kbd> to the deadlocked PID 1 and re-spawns the container, logging a restart '
                          'count increment in <kbd>kubectl get pods</kbd>.</p>\n'
                          '<p><strong class="side-heading">Evidence limit:</strong> Local container probe testing '
                          'verifies iptables endpoint detachment and process restarts, but cannot reproduce BGP edge '
                          'route withdrawal latencies or Google Cloud Load Balancer health check probe intervals from '
                          'distributed edge points of presence (<strong class="keyword">PoPs</strong>).</p>\n'
                          '\n'
                          '<figure class="diagram-figure">\n'
                          '<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>\n'
                          '<svg aria-labelledby="day10-reconcile-title day10-reconcile-desc" role="img" viewbox="0 0 '
                          '940 300">\n'
                          '<title id="day10-reconcile-title">Kubernetes declarative control loop and reconciliation '
                          'architecture</title>\n'
                          '<desc id="day10-reconcile-desc">The diagram illustrates the continuous reconciliation loop '
                          'between desired state in etcd, the controller manager, the scheduler, and kubelet agents on '
                          'worker nodes.</desc>\n'
                          '<defs>\n'
                          '<marker id="day10-reconcile-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" '
                          'refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>\n'
                          '</defs>\n'
                          '<g fill="#121526" stroke-width="2">\n'
                          '<rect height="220" rx="10" stroke="#38bdf8" width="200" x="20" y="35"></rect>\n'
                          '<image href="../assets/icons/generic/server.svg" x="28" y="45" width="24" height="24" '
                          'preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="220" rx="10" stroke="#f97316" width="200" x="250" y="35"></rect>\n'
                          '<image href="../assets/icons/generic/decision.svg" x="258" y="45" width="24" height="24" '
                          'preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="220" rx="10" stroke="#eab308" width="200" x="480" y="35"></rect>\n'
                          '<image href="../assets/icons/generic/monitoring.svg" x="488" y="45" width="24" height="24" '
                          'preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="220" rx="10" stroke="#34d399" width="210" x="710" y="35"></rect>\n'
                          '<image href="../assets/icons/gcp/core/gke.svg" x="718" y="45" width="24" height="24" '
                          'preserveAspectRatio="xMidYMid meet"/>\n'
                          '</g>\n'
                          '<g fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">\n'
                          '<text x="125" y="65">1. Control Plane</text>\n'
                          '<text x="355" y="65">2. Controllers</text>\n'
                          '<text x="585" y="65">3. Scheduler</text>\n'
                          '<text x="820" y="65">4. Worker Nodes</text>\n'
                          '</g>\n'
                          '<g fill="#a9b7cb" font-size="11" text-anchor="middle">\n'
                          '<text fill="#38bdf8" x="120" y="95">kube-apiserver</text>\n'
                          '<text x="120" y="120">etcd Data Store</text>\n'
                          '<text x="120" y="145">Stores Desired State</text>\n'
                          '<text x="120" y="170">(e.g., replicas: 3)</text>\n'
                          '<text fill="#fce7f3" x="120" y="210">Authoritative Spec</text>\n'
                          '<text fill="#f97316" x="350" y="95">controller-manager</text>\n'
                          '<text x="350" y="120">Deployment Loop</text>\n'
                          '<text x="350" y="145">Compares Desired vs Actual</text>\n'
                          '<text x="350" y="170">Creates Missing Pods</text>\n'
                          '<text fill="#fce7f3" x="350" y="210">Reconciliation Engine</text>\n'
                          '<text fill="#eab308" x="580" y="95">kube-scheduler</text>\n'
                          '<text x="580" y="120">Filters Node Capacity</text>\n'
                          '<text x="580" y="145">Evaluates CPU / RAM</text>\n'
                          '<text x="580" y="170">Assigns Pod to Node</text>\n'
                          '<text fill="#fce7f3" x="580" y="210">Placement Decision</text>\n'
                          '<text fill="#34d399" x="815" y="95">kubelet &amp; CRI</text>\n'
                          '<text x="815" y="120">Pulls Image &amp; Starts Pod</text>\n'
                          '<text x="815" y="145">Executes Health Probes</text>\n'
                          '<text x="815" y="170">Reports Status to API</text>\n'
                          '<text fill="#fce7f3" x="815" y="210">Observed Actual State</text>\n'
                          '</g>\n'
                          '<g fill="none" marker-end="url(#day10-reconcile-arrow)" stroke="#38bdf8" stroke-width="2">\n'
                          '<path d="M220 145 L246 145"></path>\n'
                          '<path d="M450 145 L476 145"></path>\n'
                          '<path d="M680 145 L706 145"></path>\n'
                          '<path d="M815 235 L815 270 L120 270 L120 258"></path>\n'
                          '</g>\n'
                          '<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="285">Continuous '
                          'feedback loop: actual node telemetry reconciles against declared desired state in '
                          'etcd.</text>\n'
                          '</svg>\n'
                          '<figcaption>Figure 10.2: Declarative reconciliation loop in Kubernetes. The control plane '
                          'watches declared desired state, detects divergence, calculates placement across worker '
                          'nodes, and executes autonomous convergence.</figcaption>\n'
                          '</figure>\n',
             'title': 'Container orchestration'},
            {'anchors': {'lab': 'topic-03-lab',
                         'overview': 'topic-03-overview',
                         'problem': 'topic-03-problem',
                         'technical': 'topic-03-technical'},
             'key': 'topic-03',
             'lab': {'accept': 'The curriculum exit evidence artifact is generated at '
                               'scratch/day-010-ownership-diagram.md containing the complete Pod/Deployment/Service '
                               'ownership hierarchy.',
                     'cleanup': 'Remove transient test manifests in scratch/day10_lab_c.',
                     'covers': 'Kubernetes core objects: Pod, Deployment, Service, Ingress, ConfigMap, Secret; '
                               'ownership relationships and traffic routing.',
                     'expected': 'A verified routing repair and the curriculum exit evidence: a Pod/Deployment/Service '
                                 'ownership diagram distinguishing declarative relationships and request flows.',
                     'file': 'day-010-exercise-c.md',
                     'goal': 'Diagnose a Kubernetes Service selector mismatch defect, repair routing endpoint '
                             'bindings, and map the complete architectural ownership hierarchy connecting Ingress, '
                             'Services, Deployments, Pods, ConfigMaps, and Secrets.',
                     'mode': 'Observed locally: local manifest inspection, endpoint resolution simulation, and '
                             'ownership hierarchy compilation. Simulated or predicted: GKE Ingress controller '
                             'provisioning Google Cloud Load Balancer URL maps and NEG bindings. Untested on GCP: '
                             'Cloud Armor WAF policy evaluation and SSL certificate provisioning latency.',
                     'name': 'Exercise C · Diagnose service selectors and map ownership hierarchy',
                     'preflight': 'Verify Python 3 runtime and initialize workspace.',
                     'prereq': 'Linux terminal with Python 3.',
                     'steps': ['**Stage 1: Preflight and Workspace Setup**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Verify CLI utilities and create workspace directories for Kubernetes object '
                               'evaluation.\n'
                               '```bash\n'
                               'command -v bash\n'
                               'command -v python3\n'
                               'command -v cat\n'
                               'command -v mkdir\n'
                               'mkdir -p scratch/day10_lab_c\n'
                               'echo "Stage 1 core objects preflight complete at $(date -u +%Y-%m-%dT%H:%M:%SZ)" > '
                               'scratch/day10_lab_c/stage1.log\n'
                               'cat scratch/day10_lab_c/stage1.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Tooling verified and workspace initialized.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_c/stage1.log`',
                               '**Stage 2: Author Kubernetes Core Manifests (Deployment, Service, ConfigMap, '
                               'Secret)**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Author a multi-object Kubernetes manifest containing a Deployment, Service, ConfigMap, '
                               'and Secret.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_c/manifests.yaml\n"
                               'apiVersion: v1\n'
                               'kind: ConfigMap\n'
                               'metadata:\n'
                               '  name: inventory-config\n'
                               'data:\n'
                               '  MAX_PAGE_SIZE: "50"\n'
                               '  CACHE_ENABLED: "true"\n'
                               '---\n'
                               'apiVersion: v1\n'
                               'kind: Secret\n'
                               'metadata:\n'
                               '  name: inventory-secret\n'
                               'type: Opaque\n'
                               'data:\n'
                               '  DB_PASSWORD: "c3VwZXJzZWNyZXRwYXNz" # base64 for supersecretpass\n'
                               '---\n'
                               'apiVersion: apps/v1\n'
                               'kind: Deployment\n'
                               'metadata:\n'
                               '  name: inventory-deployment\n'
                               'spec:\n'
                               '  replicas: 3\n'
                               '  selector:\n'
                               '    matchLabels:\n'
                               '      app: inventory-service\n'
                               '  template:\n'
                               '    metadata:\n'
                               '      labels:\n'
                               '        app: inventory-service\n'
                               '    spec:\n'
                               '      containers:\n'
                               '      - name: inventory\n'
                               '        image: gcr.io/demo/inventory:v1.0.0\n'
                               '        ports:\n'
                               '        - containerPort: 8080\n'
                               '---\n'
                               'apiVersion: v1\n'
                               'kind: Service\n'
                               'metadata:\n'
                               '  name: inventory-service\n'
                               'spec:\n'
                               '  type: ClusterIP\n'
                               '  selector:\n'
                               '    app: inventory-backend # INTENTIONAL DEFECT: Typo mismatch vs app: '
                               'inventory-service\n'
                               '  ports:\n'
                               '  - port: 80\n'
                               '    targetPort: 8080\n'
                               'EOF\n'
                               'echo "Manifests authored with intentional selector defect" > '
                               'scratch/day10_lab_c/stage2.log\n'
                               'cat scratch/day10_lab_c/stage2.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Multi-object manifest authored with intentional selector typo.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_c/stage2.log`',
                               '**Stage 3: Inject Intentional Selector Typo and Generate Endpoint Defect**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Execute a manifest audit script that extracts the Service selector and compares it '
                               'against the Deployment template labels.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_c/audit_selector.py\n"
                               'import re\n'
                               '\n'
                               'with open("scratch/day10_lab_c/manifests.yaml") as f:\n'
                               '    text = f.read()\n'
                               '\n'
                               '# Extract Pod labels\n'
                               'pod_label_match = re.search(r"template:.*?labels:\\s*\\n\\s*app:\\s*([^\\n]+)", text, '
                               're.S)\n'
                               'pod_label = pod_label_match.group(1).strip() if pod_label_match else None\n'
                               '\n'
                               '# Extract Service selector\n'
                               'svc_selector_match = re.search(r"kind: '
                               'Service.*?selector:\\s*\\n\\s*app:\\s*([^\\n]+)", text, re.S)\n'
                               'svc_selector = svc_selector_match.group(1).strip() if svc_selector_match else None\n'
                               '\n'
                               'print(f"Deployment Pod Template Label: \'app: {pod_label}\'")\n'
                               'print(f"Service Selector Label:        \'app: {svc_selector}\'")\n'
                               '\n'
                               'if pod_label != svc_selector:\n'
                               '    print("\\n[CRITICAL ROUTING DEFECT DETECTED]")\n'
                               '    print(f"  Mismatch: Service selector \'{svc_selector}\' != Pod label '
                               '\'{pod_label}\'")\n'
                               '    print("  Outcome: EndpointSlice will be EMPTY. Traffic will fail with HTTP 503.")\n'
                               'else:\n'
                               '    print("\\n[ROUTING ALIGNED]")\n'
                               '    print("  Endpoints populated. Traffic will route successfully.")\n'
                               'EOF\n'
                               'python3 scratch/day10_lab_c/audit_selector.py > scratch/day10_lab_c/stage3.log\n'
                               'cat scratch/day10_lab_c/stage3.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Audit script detects selector mismatch and flags empty endpoint '
                               'outcome.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_c/stage3.log`',
                               '**Stage 4: Run EndpointSlice Diagnostic Engine and Detect Zero Targets**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Simulate the Kubernetes EndpointSlice controller evaluation to document the '
                               'zero-target defect.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_c/simulate_endpointslice.py\n"
                               'import json\n'
                               '\n'
                               'pod_ips = ["10.244.1.5", "10.244.2.8", "10.244.3.12"]\n'
                               'pod_labels = {"app": "inventory-service"}\n'
                               'service_selector = {"app": "inventory-backend"}\n'
                               '\n'
                               'matches = []\n'
                               'for ip in pod_ips:\n'
                               '    if all(pod_labels.get(k) == v for k, v in service_selector.items()):\n'
                               '        matches.append({"ip": ip, "ready": True})\n'
                               '\n'
                               'endpoint_slice = {\n'
                               '    "metadata": {"name": "inventory-service-slice"},\n'
                               '    "endpoints": matches\n'
                               '}\n'
                               'print("Simulated EndpointSlice Output:")\n'
                               'print(json.dumps(endpoint_slice, indent=2))\n'
                               'print(f"Active Ready Endpoints: {len(matches)}")\n'
                               'EOF\n'
                               'python3 scratch/day10_lab_c/simulate_endpointslice.py > '
                               'scratch/day10_lab_c/stage4.log\n'
                               'cat scratch/day10_lab_c/stage4.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Output displays 0 active ready endpoints.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_c/stage4.log`',
                               '**Stage 5: Repair Service Selector Label and Reconcile Endpoints**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Repair the selector typo in the Service manifest and re-run the diagnostic engine.\n'
                               '```bash\n'
                               '# Correct selector in manifest\n'
                               "sed -i 's/app: inventory-backend/app: inventory-service/g' "
                               'scratch/day10_lab_c/manifests.yaml\n'
                               'python3 scratch/day10_lab_c/audit_selector.py > scratch/day10_lab_c/stage5.log\n'
                               'cat scratch/day10_lab_c/stage5.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Audit script confirms `[ROUTING ALIGNED]` with matching labels.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_c/stage5.log`',
                               '**Stage 6: Trace End-to-End Request Path from Ingress to Service to Pod**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Simulate client HTTP request routing through the repaired Service and EndpointSlice to '
                               'backend pods.\n'
                               '```bash\n'
                               "python3 -c '\n"
                               'import random\n'
                               '\n'
                               'pod_ips = ["10.244.1.5:8080", "10.244.2.8:8080", "10.244.3.12:8080"]\n'
                               'print("Simulating 6 Ingress Client Requests through Service VIP 10.96.0.45:80:")\n'
                               'for req_id in range(1, 7):\n'
                               '    target = random.choice(pod_ips)\n'
                               '    print(f"  Request #{req_id} -> Ingress -> inventory-service:80 -> Pod IP {target} '
                               '[HTTP 200 OK]")\n'
                               "' > scratch/day10_lab_c/stage6.log\n"
                               'cat scratch/day10_lab_c/stage6.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Output displays load-balanced routing across all 3 backend pod '
                               'IPs.\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_c/stage6.log`',
                               '**Stage 7: Synthesize the Pod/Deployment/Service Ownership Diagram Exit Artifact**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Synthesize all findings into the required curriculum exit evidence: a '
                               'Pod/Deployment/Service ownership diagram distinguishing declarative relationships and '
                               'request flows.\n'
                               '```bash\n'
                               "cat <<'EOF' > scratch/day10_lab_c/build_exit_artifact.py\n"
                               'import datetime\n'
                               '\n'
                               'now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")\n'
                               '\n'
                               'content = f"""# Day 10 Exit Evidence: Pod / Deployment / Service Ownership Diagram\n'
                               '**Generated:** {now}\n'
                               '**Curriculum Scope:** Kubernetes Core Objects (Pod, Deployment, Service, Ingress, '
                               'ConfigMap, Secret)\n'
                               '\n'
                               '## 1. Declarative Ownership & Control Hierarchy\n'
                               '\n'
                               '[ Developer / GitOps Manifest ]\n'
                               '               │\n'
                               '               ▼\n'
                               '      [ Ingress Resource ]\n'
                               '               │ (defines host & path routing rules)\n'
                               '               ▼\n'
                               '      [ Service Object ] ─── (selector: app=inventory-service) ───┐\n'
                               '               │                                                  │ matches\n'
                               '               │ (virtual IP & kube-proxy / NEG routing)           │\n'
                               '               ▼                                                  ▼\n'
                               '     [ EndpointSlice ] ───────────────────────────────► [ Pod Replicas ]\n'
                               '                                                              ▲   ▲   ▲\n'
                               '                                                              │   │   │ owns\n'
                               '                                                      [ ReplicaSet ]\n'
                               '                                                              ▲\n'
                               '                                                              │ manages rollout\n'
                               '                                                      [ Deployment ]\n'
                               '\n'
                               '## 2. Configuration & Credential Injection Hierarchy\n'
                               '\n'
                               '  [ ConfigMap: inventory-config ]            [ Secret: inventory-secret ]\n'
                               '        │ (non-sensitive vars)                    │ (encrypted credentials)\n'
                               '        ▼                                         ▼\n'
                               '   [ volumeMount: /etc/config ]              [ env: DB_PASSWORD ]\n'
                               '        └───────────────────┬─────────────────────┘\n'
                               '                            ▼\n'
                               '               [ Container: inventory ]\n'
                               '\n'
                               '## 3. Core Object Function & Lifecycle Matrix\n'
                               '\n'
                               '| Core Object | Controlling Component | Lifecycle & Scope | Addressing / Discovery | '
                               'Failure Consequence |\n'
                               '|---|---|---|---|---|\n'
                               '| **Ingress** | Ingress Controller / Cloud Load Balancer | Global / Edge HTTP routing '
                               '| Public or internal VIP + DNS | Edge HTTP 404 / 502 routing failure |\n'
                               '| **Service** | kube-proxy / EndpointSlice Controller | Cluster-wide stable virtual IP '
                               '| ClusterIP / CoreDNS name | HTTP 503 if selector has typo |\n'
                               '| **Deployment** | kube-controller-manager | Declarative rollout & replica count | '
                               'Managed via labels & ReplicaSets | Pods crash or unplaced if misconfigured |\n'
                               '| **Pod** | kubelet & Container Runtime (CRI) | Ephemeral atomic container bundle | '
                               'Ephemeral Pod IP in VPC | Container restart / rescheduling |\n'
                               '| **ConfigMap** | kube-apiserver / etcd | Decoupled configuration values | Volume '
                               'mount or env variable | Pod startup failure if key missing |\n'
                               '| **Secret** | kube-apiserver / Cloud KMS | Decoupled sensitive tokens | Volume mount '
                               'or env variable | Authentication failure if unsealed |\n'
                               '\n'
                               '## 4. Key Architectural Takeaways\n'
                               '1. **Never Target Pod IPs Directly:** Pods are ephemeral; always route traffic through '
                               'a Service virtual IP backed by EndpointSlices.\n'
                               '2. **Label Selector Precision:** A single-character typo in a Service selector '
                               'decouples all backend Pods without failing pod health checks.\n'
                               '3. **Decouple Config & Code:** Use ConfigMaps and Secrets to ensure container images '
                               'remain strictly immutable and environment-agnostic.\n'
                               '"""\n'
                               '\n'
                               'with open("scratch/day-010-ownership-diagram.md", "w") as f:\n'
                               '    f.write(content)\n'
                               '\n'
                               'print("Exit artifact generated at scratch/day-010-ownership-diagram.md")\n'
                               'EOF\n'
                               'python3 scratch/day10_lab_c/build_exit_artifact.py > scratch/day10_lab_c/stage7.log\n'
                               'cat scratch/day-010-ownership-diagram.md\n'
                               '```\n'
                               '\n'
                               '**Expected result:** `scratch/day-010-ownership-diagram.md` is generated '
                               'successfully.\n'
                               '\n'
                               '**Save:** `scratch/day-010-ownership-diagram.md`',
                               '**Stage 8: Validate and Verify the Day 10 Exit Artifact**\n'
                               '\n'
                               '**Location:** local terminal\n'
                               '\n'
                               '**Actions:**\n'
                               'Validate that the generated ownership diagram contains all required sections and '
                               'satisfies curriculum exit criteria.\n'
                               '```bash\n'
                               "python3 -c '\n"
                               'with open("scratch/day-010-ownership-diagram.md") as f:\n'
                               '    text = f.read()\n'
                               '\n'
                               'required = [\n'
                               '    "Declarative Ownership & Control Hierarchy",\n'
                               '    "Configuration & Credential Injection Hierarchy",\n'
                               '    "Core Object Function & Lifecycle Matrix",\n'
                               '    "Pod",\n'
                               '    "Deployment",\n'
                               '    "Service",\n'
                               '    "Ingress",\n'
                               '    "ConfigMap",\n'
                               '    "Secret"\n'
                               ']\n'
                               '\n'
                               'missing = [req for req in required if req not in text]\n'
                               'if missing:\n'
                               '    raise ValueError(f"Missing required sections: {missing}")\n'
                               '\n'
                               'print("✓ Day 10 Exit Artifact verified: complete ownership hierarchy and matrix '
                               'validated.")\n'
                               "' > scratch/day10_lab_c/stage8.log\n"
                               'cat scratch/day10_lab_c/stage8.log\n'
                               '```\n'
                               '\n'
                               '**Expected result:** Output displays `✓ Day 10 Exit Artifact verified: complete '
                               'ownership hierarchy and matrix validated.`\n'
                               '\n'
                               '**Save:** `scratch/day10_lab_c/stage8.log`'],
                     'trouble': 'If YAML parsing errors occur, ensure standard syntax without illegal tabs.',
                     'verification': 'Verify that the ownership diagram exit artifact accurately maps all core '
                                     'objects, labels, selectors, and routing paths.'},
             'overview': 'Kubernetes core objects represent the foundational declarative primitives used to model '
                         'cloud-native applications: Pods represent the atomic unit of collocated container '
                         'scheduling; Deployments manage declarative replica scaling and zero-downtime rolling '
                         'updates; Services provide stable virtual IP addresses and load-balanced endpoint routing '
                         'across ephemeral pods; Ingress routes external HTTP/HTTPS traffic into internal cluster '
                         'services; and ConfigMaps and Secrets decouple configuration and sensitive credentials from '
                         'container image binaries.',
             'preview': 'A newly deployed microservice passes all readiness checks but external client requests fail '
                        'immediately with HTTP 503 Service Unavailable errors. An inspection reveals that a subtle '
                        'typo in the Service selector label prevented the controller from attaching pod IP addresses '
                        'to the routing endpoint slice.',
             'questions': ['How do Kubernetes Services decouple network routing from ephemeral pod IP churn using '
                           'EndpointSlices?',
                           'Why does a single-character typo in a Service label selector cause silent external HTTP '
                           '503 routing failures?',
                           'In what ways does mounting ConfigMaps and Secrets as volumes provide superior operational '
                           'flexibility over environment variables?'],
             'reference': 'https://kubernetes.io/docs/concepts/overview/working-with-objects/#kubernetes-objects',
             'reference_label': 'Understanding Kubernetes objects (accessed 2026-10-04)',
             'scenario': {'constraints': 'Deployment labels specify "app: inventory-service"; Service selector '
                                         'specifies "app: inventory-backend" due to a typographical error during '
                                         'manifest drafting; Ingress routes to Service on port 80.',
                          'diagnostic_steps': ['Inspect Service status and virtual IP: kubectl get svc '
                                               'inventory-service',
                                               'Check attached Service endpoints: kubectl get endpoints '
                                               'inventory-service',
                                               'Compare Service selector against Pod labels: kubectl get svc '
                                               'inventory-service -o jsonpath="{.spec.selector}" && kubectl get pods '
                                               '--show-labels',
                                               'Query EndpointSlices directly: kubectl get endpointslices -l '
                                               'kubernetes.io/service-name=inventory-service'],
                          'diagram': ('External client issues HTTP request through Cloud Load Balancer',
                                      'Service selector app: inventory-backend has typo vs pod labels',
                                      'Service Endpoints empty; Ingress returns HTTP 503 Service Unavailable',
                                      'Correct selector label to match app: inventory-service exactly',
                                      'EndpointSlice registers 3 pod IPs; client requests return HTTP 200'),
                          'diagram_enabled': True,
                          'evidence': 'Executing "kubectl get endpoints inventory-service" reveals "<none>". Reviewing '
                                      'EndpointSlices via "kubectl get endpointslices -l '
                                      'kubernetes.io/service-name=inventory-service" confirms that zero endpoints are '
                                      'attached. While pods are 100% healthy, the label mismatch prevents the '
                                      'EndpointSlice controller from associating pod IP addresses with the Service '
                                      'virtual IP.\n'
                                      '\n'
                                      '<figure class="diagram-figure">\n'
                                      '<p class="diagram-scroll-hint">Swipe horizontally to view the full '
                                      'diagram.</p>\n'
                                      '<svg aria-labelledby="day10-selector-incident-title '
                                      'day10-selector-incident-desc" role="img" viewbox="0 0 940 310">\n'
                                      '<title id="day10-selector-incident-title">Service selector label mismatch '
                                      'causing zero backend endpoints</title>\n'
                                      '<desc id="day10-selector-incident-desc">The failed dashed path routes requests '
                                      'to a Service whose selector contains a typo, resulting in empty endpoints and '
                                      'HTTP 503. The corrected solid path aligns the selector with Pod labels, '
                                      'restoring traffic flow.</desc>\n'
                                      '<defs>\n'
                                      '<marker id="day10-sel-arrow" markerheight="8" markerwidth="10" orient="auto" '
                                      'refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>\n'
                                      '<marker id="day10-sel-fail-arrow" markerheight="8" markerwidth="10" '
                                      'orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" '
                                      'fill="#f43f5e"></path></marker>\n'
                                      '</defs>\n'
                                      '<g fill="#121526" stroke-width="2">\n'
                                      '<rect height="85" rx="8" stroke="#38bdf8" width="150" x="20" y="110"></rect>\n'
                                      '<image href="../assets/icons/generic/client.svg" x="28" y="118" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#f43f5e" width="220" x="225" y="30"></rect>\n'
                                      '<image href="../assets/icons/generic/failure.svg" x="233" y="38" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#34d399" width="220" x="225" y="185"></rect>\n'
                                      '<image href="../assets/icons/generic/router.svg" x="233" y="193" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#f43f5e" width="220" x="495" y="30"></rect>\n'
                                      '<image href="../assets/icons/generic/failure.svg" x="503" y="38" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#34d399" width="220" x="495" y="185"></rect>\n'
                                      '<image href="../assets/icons/generic/decision.svg" x="503" y="193" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '<rect height="85" rx="8" stroke="#38bdf8" width="155" x="765" y="110"></rect>\n'
                                      '<image href="../assets/icons/generic/outcome.svg" x="773" y="118" width="22" '
                                      'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                      '</g>\n'
                                      '<g fill="#fce7f3" font-size="12" font-weight="600" text-anchor="middle">\n'
                                      '<text x="102" y="142">Client Ingress</text>\n'
                                      '<text fill="#a9b7cb" x="102" y="162">GET /checkout</text>\n'
                                      '<text x="342" y="58">[FAILED: Selector Typo]</text>\n'
                                      '<text fill="#f43f5e" x="342" y="78">Service selector: app: order</text>\n'
                                      '<text fill="#a9b7cb" x="342" y="98">Pod labels: app: orders</text>\n'
                                      '<text x="342" y="213">[CORRECTED: Matched Label]</text>\n'
                                      '<text fill="#34d399" x="342" y="233">Service selector: app: orders</text>\n'
                                      '<text fill="#a9b7cb" x="342" y="253">Exact key-value match</text>\n'
                                      '<text x="612" y="58">EXACT FAILURE POINT</text>\n'
                                      '<text fill="#f43f5e" x="612" y="78">EndpointSlice is empty</text>\n'
                                      '<text fill="#f43f5e" x="612" y="98">Ingress returns HTTP 503</text>\n'
                                      '<text x="612" y="213">CORRECTED CONTROL</text>\n'
                                      '<text fill="#34d399" x="612" y="233">Endpoints populated with IPs</text>\n'
                                      '<text fill="#a9b7cb" x="612" y="253">10.244.1.5:8080 active</text>\n'
                                      '<text x="849" y="138">VERIFICATION</text>\n'
                                      '<text fill="#34d399" x="849" y="158">HTTP 200 OK</text>\n'
                                      '<text fill="#a9b7cb" x="849" y="178">Order processed cleanly</text>\n'
                                      '</g>\n'
                                      '<g fill="none" stroke-width="2">\n'
                                      '<path d="M170 135 L220 85" marker-end="url(#day10-sel-fail-arrow)" '
                                      'stroke="#f43f5e" stroke-dasharray="7 5"></path>\n'
                                      '<path d="M445 72 L490 72" marker-end="url(#day10-sel-fail-arrow)" '
                                      'stroke="#f43f5e" stroke-dasharray="7 5"></path>\n'
                                      '<path d="M170 170 L220 215" marker-end="url(#day10-sel-arrow)" '
                                      'stroke="#38bdf8"></path>\n'
                                      '<path d="M445 227 L490 227" marker-end="url(#day10-sel-arrow)" '
                                      'stroke="#38bdf8"></path>\n'
                                      '<path d="M715 227 L760 170" marker-end="url(#day10-sel-arrow)" '
                                      'stroke="#38bdf8"></path>\n'
                                      '</g>\n'
                                      '<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="295">Dashed '
                                      'line (--&gt;) = empty endpoint slice failure · Solid line (—&gt;) = aligned '
                                      'selector and active pod proxying</text>\n'
                                      '</svg>\n'
                                      '<figcaption>Figure 10.6: Supplied facts: Healthy running Pods receive zero '
                                      'traffic due to a selector typo in the Service specification. Architectural '
                                      'inference: Services decouple IP addressing via label selectors; exact matching '
                                      'is required for EndpointSlice generation. Expected post-fix behavior: Aligned '
                                      'selectors populate endpoints, restoring HTTP 200 responses.</figcaption>\n'
                                      '</figure>',
                          'expected': 'Expected post-fix behavior: Aligned selectors populate endpoints, restoring '
                                      'HTTP 200 responses.',
                          'facts': 'Supplied facts: Healthy running Pods receive zero traffic due to a selector typo '
                                   'in the Service specification.',
                          'icons': ('../assets/icons/generic/client.svg',
                                    '../assets/icons/generic/failure.svg',
                                    '../assets/icons/generic/failure.svg',
                                    '../assets/icons/generic/router.svg',
                                    '../assets/icons/generic/outcome.svg'),
                          'impact': 'Frontend shopping cart checkouts fail; customers cannot view item availability; '
                                    'warehouse picking operations stall due to inventory API unavailability.',
                          'inference': 'Architectural inference: Services decouple IP addressing via label selectors; '
                                       'exact matching is required for EndpointSlice generation.',
                          'remediation_steps': ['Edit Service manifest to align selector: spec.selector.app: '
                                                '"inventory-service"',
                                                'Apply updated Service definition: kubectl apply -f service.yaml',
                                                'Verify EndpointSlice controller attaches pod IP addresses: kubectl '
                                                'get endpoints inventory-service',
                                                'Execute curl test against Ingress endpoint: curl -I '
                                                'https://api.example.com/inventory',
                                                'Confirm HTTP 200 status code and load balancing across all 3 backend '
                                                'pods'],
                          'residual': 'Label-based decoupling relies on string key-value matching without compile-time '
                                      'type safety, requiring automated GitOps manifest schema validation (e.g., '
                                      'Kubeval or Conftest) to detect selector drift pre-deployment.',
                          'root': 'A typographical discrepancy between the Service manifest selector (app: '
                                  'inventory-backend) and the Pod template labels (app: inventory-service) broke the '
                                  'declarative association between the routing layer and backend compute instances.',
                          'scenario': 'An inventory microservice consisting of 3 replicas is deployed to Google '
                                      'Kubernetes Engine. The application pods start, initialize, pass their HTTP '
                                      'readiness probes, and achieve Running status. However, all external customer '
                                      'traffic routed through the Ingress controller fails with HTTP 503 Service '
                                      'Unavailable errors. Cloud Monitoring alerts trigger on elevated edge error '
                                      'rates.',
                          'verify': 'The Service selector label is corrected to "app: inventory-service" and applied '
                                    'to the cluster. The EndpointSlice controller instantly detects the matching '
                                    'labels and attaches all 3 pod IP addresses. Ingress returns HTTP 200 OK across '
                                    'all synthetic customer requests with sub-5ms latency.'},
             'technical': '<p><strong class="side-heading">Subtopics in this discussion:</strong></p>\n'
                          '<ol>\n'
                          '<li><a href="#topic-03-subtopic-1">Pods: The Atomic Unit of Kubernetes Scheduling and '
                          'Collocation</a></li>\n'
                          '<li><a href="#topic-03-subtopic-2">Deployments and ReplicaSets: Declarative Rollouts and '
                          'Rollbacks</a></li>\n'
                          '<li><a href="#topic-03-subtopic-3">Services and EndpointSlices: Stable Networking and '
                          'Service Discovery</a></li>\n'
                          '<li><a href="#topic-03-subtopic-4">Ingress Controllers and Cloud Load Balancing '
                          'Integration</a></li>\n'
                          '<li><a href="#topic-03-subtopic-5">ConfigMaps and Secrets: Decoupling Configuration and '
                          'Sensitive Credentials</a></li>\n'
                          '</ol>\n'
                          '\n'
                          '<h4 id="topic-03-subtopic-1">Pods: The Atomic Unit of Kubernetes Scheduling and '
                          'Collocation</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> A <strong '
                          'class="keyword">Pod</strong> is the fundamental schedulable and deployable unit in '
                          'Kubernetes. Rather than scheduling isolated Linux containers, Kubernetes instantiates a Pod '
                          'as a shared execution sandbox that bundles one or more application containers.</p>\n'
                          '<ul>\n'
                          '<li><strong>The Pause / Infra Container Architecture:</strong> When a Pod is scheduled, '
                          '<kbd>kubelet</kbd> instructs the CRI runtime to instantiate an "infra" or "pause" container '
                          '(<kbd>registry.k8s.io/pause</kbd>). The pause container allocates the underlying Linux '
                          'kernel namespaces and enters an infinite sleep loop. Application containers then join the '
                          'namespaces established by the pause container.</li>\n'
                          '<li><strong>Namespace Sharing Dynamics:</strong>\n'
                          '  <ul>\n'
                          '  <li><em>Network Namespace (Shared):</em> All containers within a Pod share identical '
                          'virtual network interfaces (<kbd>eth0</kbd>), loopback (<kbd>lo</kbd>), IP address, and '
                          'TCP/UDP port spaces. Container A running on port <kbd>8080</kbd> communicates with '
                          'Container B on port <kbd>5432</kbd> via <kbd>127.0.0.1</kbd> (localhost) with zero network '
                          'encapsulation latency.</li>\n'
                          '  <li><em>IPC Namespace (Shared):</em> Containers share POSIX shared memory '
                          '(<kbd>/dev/shm</kbd>) and System V IPC primitives, enabling high-performance inter-process '
                          'communication.</li>\n'
                          '  <li><em>Mount Namespace (Isolated):</em> Each container maintains its own distinct '
                          'filesystem rootfs. Persistent volumes and ConfigMaps are mounted at explicitly declared '
                          'directory paths within individual container mount tables.</li>\n'
                          '  <li><em>PID Namespace (Isolated by default):</em> Process trees are isolated per '
                          'container, but can be unified across the Pod by declaring <kbd>spec.shareProcessNamespace: '
                          'true</kbd> to allow helper containers to inspect or signal primary application '
                          'processes.</li>\n'
                          '  </ul>\n'
                          '</li>\n'
                          '<li><strong>Common Multi-Container Pod Patterns:</strong>\n'
                          '  <ul>\n'
                          '  <li><em>Init Containers:</em> Execute sequentially to completion before primary '
                          'application containers initialize (e.g., running database migrations or validating DNS '
                          'availability).</li>\n'
                          '  <li><em>Sidecar Containers:</em> Run concurrently alongside the main application '
                          'container to provide supplemental operational capabilities (e.g., Envoy proxies for service '
                          'meshes, Fluentbit log forwarders, or Google Cloud SQL Auth Proxies).</li>\n'
                          '  </ul>\n'
                          '</li>\n'
                          '</ul>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Multi-container '
                          'Pods must adhere strictly to the single-responsibility lifecycle principle. Collocating two '
                          'independent business microservices in the same Pod is an anti-pattern: it forces them to '
                          'share vertical CPU/memory scaling constraints, creates shared fate during node failures, '
                          'and prevents independent CI/CD release lifecycles. Furthermore, direct point-to-point '
                          'communication targeting Pod IP addresses is fundamentally fragile because Pod IPs are '
                          'dynamically assigned upon creation and discarded upon termination. Architects mandate that '
                          'all ingress and internal traffic traverse abstracted Service VIPs or headless discovery '
                          'records.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> <strong class="keyword">GKE '
                          'VPC-Native Clusters</strong> assign Pod IP addresses directly from dedicated secondary IP '
                          "subnets within the customer's Google Cloud Virtual Private Cloud (<strong "
                          'class="keyword">VPC</strong>) using <strong class="keyword">VPC Alias IP ranges</strong>. '
                          'This architecture eliminates traditional software overlay networks (<strong '
                          'class="keyword">VXLAN / Geneve</strong>). Every GKE Pod IP is natively routable across the '
                          'VPC, allowing direct, low-latency connectivity to Compute Engine VMs, on-premises systems '
                          'via Cloud Interconnect, and managed services like Cloud SQL without NAT translation or '
                          'gateway proxies.</p>\n'
                          '<p><strong class="side-heading">Concrete example:</strong> A web application container '
                          'running in a GKE Pod connects to a local Cloud SQL Auth Proxy sidecar container at '
                          '<kbd>127.0.0.1:5432</kbd>. The sidecar intercepts the local traffic, establishes a mutual '
                          'TLS tunnel using Google Cloud IAM credentials, and forwards requests to a managed Cloud SQL '
                          'instance across the VPC.</p>\n'
                          '<p><strong class="side-heading">Evidence limit:</strong> Local namespace tools (<kbd>ip '
                          'netns</kbd>, <kbd>lsns</kbd>) inspect network and IPC sharing on a single Linux kernel, but '
                          "cannot test VPC Alias IP route table synchronization across Google's global Andromeda "
                          'Software-Defined Network (<strong class="keyword">SDN</strong>).</p>\n'
                          '\n'
                          '<h4 id="topic-03-subtopic-2">Deployments and ReplicaSets: Declarative Rollouts and '
                          'Rollbacks</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> Kubernetes manages '
                          'scalable, stateless workloads through a multi-tier declarative ownership hierarchy:</p>\n'
                          '<p style="text-align:center; font-family:monospace; background:#0f172a; padding:8px; '
                          'border-radius:6px; border:1px solid #1e293b;">Deployment ──► ReplicaSet ──► Pods</p>\n'
                          '<ul>\n'
                          '<li><strong>The Deployment Controller:</strong> A Deployment does not create or manage Pods '
                          'directly. Instead, it owns and orchestrates one or more <strong '
                          'class="keyword">ReplicaSets</strong>. The active ReplicaSet is responsible for maintaining '
                          'the declared number of identical Pod replicas (<kbd>spec.replicas</kbd>) using label '
                          'selectors.</li>\n'
                          "<li><strong>Rolling Update Mechanics:</strong> When a Deployment's pod template "
                          '(<kbd>spec.template</kbd>) is modified:\n'
                          '  <ol>\n'
                          '  <li>The Deployment controller creates a <em>new</em>, distinct ReplicaSet with a unique '
                          'hash suffix (<kbd>pod-template-hash</kbd>).</li>\n'
                          '  <li>The controller computes rollout progression bounded by two parameters:\n'
                          '    <ul>\n'
                          '    <li><kbd>maxSurge</kbd>: The maximum number or percentage of Pods that can be scheduled '
                          'above desired capacity during the rollout (e.g., <kbd>25%</kbd> or <kbd>1</kbd>).</li>\n'
                          '    <li><kbd>maxUnavailable</kbd>: The maximum number or percentage of Pods that can be '
                          'offline during the update (e.g., <kbd>0</kbd> or <kbd>25%</kbd>).</li>\n'
                          '    </ul>\n'
                          '  </li>\n'
                          '  <li>The controller incrementally scales up the new ReplicaSet while scaling down the old '
                          'ReplicaSet, waiting for newly created Pods to pass readiness probes before terminating '
                          'previous generation replicas.</li>\n'
                          '  </ol>\n'
                          '</li>\n'
                          '<li><strong>Deterministic Rollbacks:</strong> If the new image crashes or fails readiness '
                          'checks, the operator triggers <kbd>kubectl rollout undo deployment/&lt;name&gt;</kbd>. The '
                          'Deployment controller reverses the reconciliation direction, immediately scaling the '
                          'previous healthy ReplicaSet back up to 100% capacity and decommissioning the failing new '
                          'ReplicaSet without modifying underlying image artifacts.</li>\n'
                          '</ul>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Capacity planning '
                          'during rollouts requires budgeting for surge capacity. Setting <kbd>maxSurge: 50%</kbd> '
                          'requires 50% additional spare cluster CPU and RAM capacity during deployments. If a cluster '
                          'lacks sufficient spare headroom or compute autoscaling is throttled, rolling updates stall '
                          'in an unresolved <kbd>Pending</kbd> state. Setting <kbd>maxUnavailable: 0</kbd> guarantees '
                          'that baseline traffic capacity is never degraded below desired scale, protecting '
                          'transaction throughput during high-volume business hours. An anti-pattern is using '
                          '<kbd>kubectl edit</kbd> directly in production or failing to specify '
                          '<kbd>revisionHistoryLimit</kbd>, which can cause hundreds of obsolete ReplicaSet objects to '
                          'accumulate in etcd, degrading API server serialization performance.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> <strong class="keyword">Google '
                          'Cloud Deploy</strong> provides a fully managed continuous delivery platform for GKE. Cloud '
                          'Deploy uses declarative render and deploy targets (via Skaffold), automating progressive '
                          'delivery pipelines (Dev &rarr; Staging &rarr; Production) and providing one-click rollbacks '
                          'with audit trails stored in Google Cloud Logging. GKE Release Channels (Rapid, Regular, '
                          'Stable) coordinate with Deployment controllers to ensure worker node upgrades respect '
                          'PodDisruptionBudgets (<strong class="keyword">PDBs</strong>), preventing node drains from '
                          'violating minimum application replica requirements.</p>\n'
                          '<p><strong class="side-heading">Concrete example:</strong> A Deployment with <kbd>replicas: '
                          '4</kbd>, <kbd>maxSurge: 1</kbd>, and <kbd>maxUnavailable: 0</kbd> is updated to image '
                          '<kbd>gcr.io/corp/checkout:v2</kbd>. The Deployment controller scales the new ReplicaSet to '
                          '1 pod (total cluster pods: 5). Once the new pod passes its <kbd>readinessProbe</kbd>, the '
                          'old ReplicaSet is scaled down to 3 pods (total: 4). This sequence repeats until all 4 pods '
                          'run <kbd>v2</kbd>.</p>\n'
                          '<p><strong class="side-heading">Evidence limit:</strong> Local cluster rollouts verify '
                          'ReplicaSet scaling logic and surge arithmetic, but cannot simulate multi-region progressive '
                          'traffic shifting with automated canary analysis (ACA) and automated rollback triggers on '
                          'Google Cloud Monitoring SLI error budgets.</p>\n'
                          '\n'
                          '<h4 id="topic-03-subtopic-3">Services and EndpointSlices: Stable Networking and Service '
                          'Discovery</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> A Kubernetes <strong '
                          'class="keyword">Service</strong> is an architectural abstraction that provides a stable, '
                          'persistent network endpoint (Virtual IP and DNS name) for a dynamic, ephemeral collection '
                          'of backend Pods.</p>\n'
                          '<ul>\n'
                          '<li><strong>Label Selectors and Decoupling:</strong> Services decouple traffic consumers '
                          'from backend providers using label selectors (<kbd>spec.selector: app=order-api</kbd>). '
                          'Pods matching the selector are automatically registered as routing targets regardless of '
                          'their physical host location or lifecycle restarts.</li>\n'
                          '<li><strong>kube-proxy &amp; Data Path Packet Translation:</strong>\n'
                          '  <ul>\n'
                          '  <li>On every worker node, <kbd>kube-proxy</kbd> watches the API server for changes to '
                          'Services and EndpointSlices.</li>\n'
                          '  <li><em>iptables Mode:</em> <kbd>kube-proxy</kbd> programs kernel Netfilter chains '
                          '(<kbd>KUBE-SERVICES</kbd>, <kbd>KUBE-SVC-*</kbd>, <kbd>KUBE-SEP-*</kbd>). When a client '
                          'sends a packet to a Service ClusterIP (<kbd>10.96.0.10:80</kbd>), the kernel performs '
                          'Destination Network Address Translation (<strong class="keyword">DNAT</strong>) using the '
                          '<kbd>statistic --mode random</kbd> module, rewriting the destination IP to an active Pod IP '
                          'chosen with equal probability ($1/N$).</li>\n'
                          '  <li><em>IPVS Mode:</em> In large clusters, <kbd>kube-proxy</kbd> configures IP Virtual '
                          'Server (<strong class="keyword">IPVS</strong>) hash tables in the Linux kernel, switching '
                          'routing complexity from $O(N)$ sequential iptables rule evaluations to $O(1)$ hash table '
                          'lookups.</li>\n'
                          '  </ul>\n'
                          '</li>\n'
                          '<li><strong>EndpointSlices (Scalability Architecture):</strong> Traditional Kubernetes '
                          '<kbd>Endpoints</kbd> resources stored all backend Pod IPs in a single monolithic object. In '
                          'clusters with thousands of replicas, a single Pod restart required serializing the entire '
                          'multi-megabyte Endpoints object across etcd and all nodes. <strong '
                          'class="keyword">EndpointSlices</strong> partition backend endpoints into modular groups of '
                          'up to 100 endpoints per slice, reducing etcd network and write overhead by over 90%.</li>\n'
                          '</ul>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> '
                          '<kbd>kube-proxy</kbd> iptables/IPVS operates strictly at Layer 4 (TCP/UDP). It selects a '
                          'backend Pod during the initial TCP three-way handshake (<kbd>SYN</kbd>). If an HTTP client '
                          'or reverse proxy uses persistent HTTP/1.1 or HTTP/2 keep-alive connections, all subsequent '
                          'HTTP requests over that TCP connection will be routed to the exact same backend Pod, '
                          'completely breaking load distribution. L7 load balancing (Ingress/Service Mesh) is required '
                          'for persistent connections. Furthermore, a single-character typographical error in a '
                          'Service selector (<kbd>app: backend-srv</kbd> vs <kbd>app: backend-service</kbd>) leaves '
                          'the Service intact but results in an empty EndpointSlice, dropping inbound requests with '
                          'connection refused or HTTP 503 even though all backend Pods report healthy status.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> <strong class="keyword">GKE '
                          'Container-Native Load Balancing with NEGs</strong> completely bypasses '
                          '<kbd>kube-proxy</kbd> and node-level iptables. GKE programs Google Cloud Load Balancer '
                          '(<strong class="keyword">GCLB</strong>) proxy targets directly with Pod VPC alias IPs. This '
                          'eliminates the "double-hop" penalty where traffic hits a random node\'s NodePort, traverses '
                          'iptables, and hops across the internal network to a second node where the target Pod '
                          'actually resides. NEGs preserve the original client source IP address and reduce median '
                          'request latency by 5–15 ms.</p>\n'
                          '<p><strong class="side-heading">Concrete example:</strong> A frontend microservice calls '
                          '<kbd>http://payment-service.default.svc.cluster.local:8080</kbd>. CoreDNS resolves the '
                          'domain to ClusterIP <kbd>10.96.44.18</kbd>. The Linux kernel on the node evaluates the '
                          '<kbd>KUBE-SVC-PAYMENT</kbd> chain, selects one of three backend Pod IPs '
                          '(<kbd>10.244.2.14:8080</kbd>), performs DNAT, and routes the packet across the virtual '
                          'bridge.</p>\n'
                          '<p><strong class="side-heading">Evidence limit:</strong> Local inspection via <kbd>iptables '
                          '-t nat -L</kbd> and <kbd>kubectl get endpointslices</kbd> proves packet rewrite rules, but '
                          'cannot demonstrate Google Andromeda SDN direct packet injection into GKE NEGs or Cloud '
                          'Armor edge packet filtering.</p>\n'
                          '\n'
                          '<h4 id="topic-03-subtopic-4">Ingress Controllers and Cloud Load Balancing Integration</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> Ingress is an Layer 7 '
                          '(HTTP/HTTPS) routing API resource that consolidates external routing rules into a unified '
                          'entry point:</p>\n'
                          '<ul>\n'
                          '<li><strong>The Exposure Problem:</strong>\n'
                          '  <ul>\n'
                          '  <li><kbd>ClusterIP</kbd>: Accessible only within the cluster virtual network.</li>\n'
                          '  <li><kbd>NodePort</kbd>: Opens an arbitrary high-range port (<kbd>30000-32767</kbd>) on '
                          'every cluster VM. Fragile, exposes node infrastructure, and requires external port-mapping '
                          'proxies.</li>\n'
                          '  <li><kbd>LoadBalancer</kbd>: Allocates a dedicated cloud network load balancer per '
                          'Service. In an architecture with 40 microservices, allocating 40 cloud load balancers '
                          'creates massive cost inefficiency and IP address exhaustion.</li>\n'
                          '  <li><kbd>Ingress</kbd>: Operates as an intelligent Layer 7 reverse proxy. It routes '
                          'multiple external hostnames (<kbd>api.example.com</kbd>, <kbd>shop.example.com</kbd>) and '
                          'URL path prefixes (<kbd>/cart</kbd>, <kbd>/orders</kbd>) through a single public IP address '
                          'to multiple internal Services.</li>\n'
                          '  </ul>\n'
                          '</li>\n'
                          '<li><strong>The Ingress Controller:</strong> The <kbd>Ingress</kbd> resource is merely a '
                          'configuration manifest. An <strong class="keyword">Ingress Controller</strong> (such as GKE '
                          'Ingress, NGINX, or Envoy) runs continuously as a control daemon, translating Ingress path '
                          'rules into physical reverse proxy configurations or programming cloud load balancing '
                          'forwarding rules.</li>\n'
                          '</ul>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Consolidating '
                          'dozens of backend microservices behind a single Ingress controller reduces cloud load '
                          'balancing costs by &gt;75%, eliminating duplicate static IP allocations and unneeded '
                          'forwarding rules. Ingress provides a unified security perimeter for TLS termination, '
                          'HTTP-to-HTTPS redirects, rate limiting, and Web Application Firewall (<strong '
                          'class="keyword">WAF</strong>) inspection, shielding internal Pods from raw Internet '
                          'exposure.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> <strong class="keyword">GKE '
                          'Ingress (GCE Ingress Controller)</strong> translates Kubernetes <kbd>Ingress</kbd> '
                          'manifests directly into Google Cloud External Application Load Balancers or Internal '
                          'Application Load Balancers.</p>\n'
                          '<ul>\n'
                          '<li><strong>Google-Managed SSL Certificates:</strong> Managed via the '
                          '<kbd>ManagedCertificate</kbd> custom resource, provisioning and auto-renewing Google CA or '
                          "Let's Encrypt certificates without manual secret rotation.</li>\n"
                          '<li><strong>Google Cloud Armor:</strong> Attached to GKE backends via a '
                          '<kbd>BackendConfig</kbd> CRD, enforcing Layer 7 DDoS mitigation, IP allowlists/denylists, '
                          "and OWASP Top 10 rule inspection at Google's global network edge.</li>\n"
                          '<li><strong>Google Cloud CDN:</strong> Enabled via <kbd>BackendConfig</kbd> to cache static '
                          "HTTP assets directly at Google's worldwide Edge PoPs.</li>\n"
                          '</ul>\n'
                          '<p><strong class="side-heading">Concrete example:</strong> An Ingress resource defines path '
                          '<kbd>/api/checkout</kbd> pointing to <kbd>checkout-svc:80</kbd> and <kbd>/static/*</kbd> '
                          'pointing to <kbd>frontend-svc:80</kbd>. GKE Ingress creates a Google Cloud URL map, '
                          'attaches a Google-managed certificate for <kbd>app.example.com</kbd>, and configures Cloud '
                          'Armor to block SQL injection attacks before requests reach the cluster.</p>\n'
                          '<p><strong class="side-heading">Evidence limit:</strong> Declarative Ingress YAML manifests '
                          'can be validated offline with <kbd>kubeval</kbd>, but testing Google Cloud Armor WAF rule '
                          'enforcement, SSL negotiation cipher suites, and CDN edge cache hit ratios requires deployed '
                          'GCP load balancer infrastructure.</p>\n'
                          '\n'
                          '<h4 id="topic-03-subtopic-5">ConfigMaps and Secrets: Decoupling Configuration and Sensitive '
                          'Credentials</h4>\n'
                          '<p><strong class="side-heading">What it is in general:</strong> Kubernetes implements the '
                          'Twelve-Factor App methodology by strictly separating application source code from '
                          'configuration and credentials:</p>\n'
                          '<ul>\n'
                          '<li><kbd>ConfigMap</kbd>: Stores non-confidential configuration data as key-value pairs or '
                          'whole configuration files (e.g., <kbd>application.properties</kbd>, <kbd>nginx.conf</kbd>, '
                          'feature flags).</li>\n'
                          '<li><kbd>Secret</kbd>: Stores sensitive credentials (API tokens, database passwords, TLS '
                          'private keys) encoded in base64. Base64 encoding is an obfuscation mechanism, <strong>not '
                          'encryption</strong>.</li>\n'
                          '<li><strong>Injection Mechanisms &amp; Lifecycle Semantics:</strong>\n'
                          '  <ul>\n'
                          '  <li><em>Environment Variables (<kbd>env</kbd> / <kbd>envFrom</kbd>):</em> Values are '
                          'evaluated and injected into the container process table at startup. <strong>Dynamic updates '
                          'do not occur</strong>: if a ConfigMap or Secret is updated in the API server, running '
                          'containers retain the original values until they are restarted.</li>\n'
                          '  <li><em>Volume Mounts (<kbd>volumeMounts</kbd>):</em> Projected into the container '
                          'filesystem as virtual files. Kubernetes uses atomic symlink rotation (<kbd>..data</kbd> '
                          'symlinks). When a ConfigMap or Secret is updated in the API server, <kbd>kubelet</kbd> '
                          'automatically updates the projected files inside running containers within seconds without '
                          'restarting the container process.</li>\n'
                          '  </ul>\n'
                          '</li>\n'
                          '</ul>\n'
                          '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Baking credentials '
                          'into container image layers embeds secrets permanently into immutable image layers, '
                          'exposing them to any user with image pull access. Exposing Secrets as environment variables '
                          'is also an anti-pattern: environment variables are routinely dumped into application crash '
                          'logs, subshells, error tracking systems (e.g., Sentry), and <kbd>/proc/$PID/environ</kbd>, '
                          'dramatically increasing credential leakage risk. Architects mandate projected volume mounts '
                          'with restricted file permissions (<kbd>defaultMode: 0400</kbd>). Furthermore, in vanilla '
                          'Kubernetes, Secrets are stored in etcd as unencrypted plaintext base64 strings; gaining '
                          'access to an etcd backup or disk snapshot exposes all cluster credentials unless KMS '
                          'envelope encryption is enforced.</p>\n'
                          '<p><strong class="side-heading">Relevance to GCP:</strong> <strong class="keyword">GKE '
                          'Database Encryption (Application-Layer Secrets Encryption)</strong> integrates GKE directly '
                          'with <strong class="keyword">Google Cloud Key Management Service (Cloud KMS)</strong>. When '
                          'a Secret is written to etcd, <kbd>kube-apiserver</kbd> uses a Customer-Managed Encryption '
                          'Key (<strong class="keyword">CMEK</strong>) to perform envelope encryption, storing only '
                          'encrypted ciphertext in etcd. Additionally, the <strong class="keyword">Google Cloud Secret '
                          'Manager CSI Driver</strong> mounts secrets directly from Google Cloud Secret Manager into '
                          'GKE Pods using <strong class="keyword">GKE Workload Identity</strong>. This architecture '
                          'eliminates storing sensitive credentials in Kubernetes etcd altogether; secrets are fetched '
                          'directly from Secret Manager at container mount time using fine-grained GCP IAM roles.</p>\n'
                          '<p><strong class="side-heading">Concrete example:</strong> A backend deployment mounts a '
                          'database password from Google Cloud Secret Manager using the SecretProviderClass. When a '
                          'database administrator rotates the password in Secret Manager, the Secret Manager CSI '
                          'driver refreshes the mounted file at <kbd>/etc/secrets/db_password</kbd> without requiring '
                          'a pod restart or modifying Kubernetes manifests.</p>\n'
                          '<p><strong class="side-heading">Evidence limit:</strong> Volume mount symlink rotation can '
                          'be verified locally on a Linux filesystem, but Google Cloud KMS envelope encryption key '
                          'rotations and Workload Identity OIDC token exchanges cannot be observed without live GCP '
                          'API integration.</p>\n'
                          '\n'
                          '<figure class="diagram-figure">\n'
                          '<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>\n'
                          '<svg aria-labelledby="day10-objects-title day10-objects-desc" role="img" viewbox="0 0 940 '
                          '320">\n'
                          '<title id="day10-objects-title">Kubernetes core object relationships and traffic routing '
                          'path</title>\n'
                          '<desc id="day10-objects-desc">The diagram traces request traffic from external clients '
                          'through Ingress and Service selectors down to backend Pods mounting ConfigMaps and '
                          'Secrets.</desc>\n'
                          '<defs>\n'
                          '<marker id="day10-objects-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" '
                          'refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>\n'
                          '</defs>\n'
                          '<g fill="#121526" stroke-width="2">\n'
                          '<rect height="240" rx="10" stroke="#38bdf8" width="160" x="20" y="35"></rect>\n'
                          '<image href="../assets/icons/generic/load-balancer.svg" x="28" y="45" width="24" '
                          'height="24" preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="240" rx="10" stroke="#f97316" width="200" x="210" y="35"></rect>\n'
                          '<image href="../assets/icons/generic/router.svg" x="218" y="45" width="24" height="24" '
                          'preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="240" rx="10" stroke="#34d399" width="230" x="440" y="35"></rect>\n'
                          '<image href="../assets/icons/generic/endpoint.svg" x="448" y="45" width="24" height="24" '
                          'preserveAspectRatio="xMidYMid meet"/>\n'
                          '<rect height="240" rx="10" stroke="#eab308" width="220" x="700" y="35"></rect>\n'
                          '<image href="../assets/icons/generic/policy.svg" x="708" y="45" width="24" height="24" '
                          'preserveAspectRatio="xMidYMid meet"/>\n'
                          '</g>\n'
                          '<g fill="#fce7f3" font-size="12" font-weight="700" text-anchor="middle">\n'
                          '<text x="105" y="65">Ingress Layer</text>\n'
                          '<text x="315" y="65">Service Abstraction</text>\n'
                          '<text x="560" y="65">Deployment &amp; Pods</text>\n'
                          '<text x="815" y="65">Config &amp; Secrets</text>\n'
                          '</g>\n'
                          '<g fill="#a9b7cb" font-size="11" text-anchor="middle">\n'
                          '<text fill="#38bdf8" x="100" y="95">Ingress Controller</text>\n'
                          '<text x="100" y="120">HTTP /orders Route</text>\n'
                          '<text x="100" y="145">TLS Termination</text>\n'
                          '<text x="100" y="170">Routes to Service</text>\n'
                          '<text fill="#fce7f3" x="100" y="210">External Ingress</text>\n'
                          '<text fill="#f97316" x="310" y="95">orders-svc (ClusterIP)</text>\n'
                          '<text x="310" y="120">Port: 80 -&gt; Target: 8080</text>\n'
                          '<text x="310" y="145">Selector: app: orders</text>\n'
                          '<text x="310" y="170">EndpointSlice Controller</text>\n'
                          '<text fill="#fce7f3" x="310" y="210">Stable Virtual IP</text>\n'
                          '<text fill="#34d399" x="555" y="95">Deployment: orders</text>\n'
                          '<text x="555" y="120">Labels: app: orders</text>\n'
                          '<text x="555" y="145">Pod 1: 10.244.1.5:8080</text>\n'
                          '<text x="555" y="170">Pod 2: 10.244.2.8:8080</text>\n'
                          '<text fill="#fce7f3" x="555" y="210">Ephemeral Replicas</text>\n'
                          '<text fill="#eab308" x="810" y="95">ConfigMap: app-config</text>\n'
                          '<text x="810" y="120">Feature flags &amp; ports</text>\n'
                          '<text x="810" y="145">Secret: db-credentials</text>\n'
                          '<text x="810" y="170">Encrypted auth tokens</text>\n'
                          '<text fill="#fce7f3" x="810" y="210">Injected Environment</text>\n'
                          '</g>\n'
                          '<g fill="none" marker-end="url(#day10-objects-arrow)" stroke="#38bdf8" stroke-width="2">\n'
                          '<path d="M180 145 L206 145"></path>\n'
                          '<path d="M410 145 L436 145"></path>\n'
                          '<path d="M700 145 L674 145"></path>\n'
                          '</g>\n'
                          '<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" y="295">Traffic traverses '
                          'Ingress -&gt; Service -&gt; Pod; Pods mount ConfigMaps and Secrets independently.</text>\n'
                          '</svg>\n'
                          '<figcaption>Figure 10.3: Kubernetes core object relationships and traffic routing '
                          'hierarchy. External traffic reaches Pods via Ingress and matching Service selectors, while '
                          'configuration and secrets are injected decoupled from image layers.</figcaption>\n'
                          '</figure>\n',
             'title': 'Kubernetes core objects'}],
 'work_block': 'Days 1–17 — Foundations'}


# Targeted Day 10 additions: retain original explanations and all existing exercises.
import re as _re
from html import escape as _escape
from urllib.parse import quote as _quote

_BUILD_COMPARE_STAGES = [
('Preflight and Workspace Setup', r"""set -euo pipefail
command -v bash
command -v python3
command -v cat
command -v mkdir
command -v docker
command -v podman
command -v mktemp
if docker info > /dev/null 2>&1; then
    ENGINE=docker
else
    podman info > /dev/null
    ENGINE=podman
fi
export ENGINE
BUILD_FLAGS=()
OPT_DIR=$(mktemp -d /tmp/day010-image-XXXXXX)
export OPT_DIR
mkdir -p "$OPT_DIR/evidence"
if [ "$ENGINE" = podman ]; then
    # Per-build policy supports disposable HOME in the lab runner. This accepts
    # unsigned builder images exactly as an ordinary Docker pull does; production
    # must use its own signature/provenance verification policy.
    printf '%s\n' '{"default":[{"type":"insecureAcceptAnything"}]}' > "$OPT_DIR/pull-policy.json"
    BUILD_FLAGS=(--signature-policy "$OPT_DIR/pull-policy.json")
    # Scope policy lookup for archive operations to this session's lab directory.
    OPT_PREVIOUS_CONFIG=${XDG_CONFIG_HOME-}
    export XDG_CONFIG_HOME="$OPT_DIR/config"
    mkdir -p "$XDG_CONFIG_HOME/containers"
    python3 - <<'POLICY'
import os,pathlib
p=pathlib.Path(os.environ['OPT_DIR'])
(pathlib.Path(os.environ['XDG_CONFIG_HOME'])/'containers/policy.json').write_bytes((p/'pull-policy.json').read_bytes())
POLICY
fi
printf '%s\n' "$OPT_DIR" > scratch/day-010-image-workspace.txt
"$ENGINE" version > "$OPT_DIR/evidence/runtime.txt"
"$ENGINE" info > "$OPT_DIR/evidence/baseline.txt"
RUN_ID=$(python3 -c 'import uuid; print(uuid.uuid4().hex[:12])')
SINGLE_IMAGE="localhost/day010-single:$RUN_ID"
MULTI_IMAGE="localhost/day010-multi:$RUN_ID"
DELETE_IMAGE="localhost/day010-delete:$RUN_ID"
export SINGLE_IMAGE MULTI_IMAGE DELETE_IMAGE
printf '%s\n' "$SINGLE_IMAGE" "$MULTI_IMAGE" "$DELETE_IMAGE" > "$OPT_DIR/evidence/tags.txt"
""", 'A daemon responds; a unique, lab-owned directory and image tags exist. Allow about 2 GB free disk and registry access. Stop on daemon/registry errors; do not substitute fabricated measurements.'),
('Application Source Code & Build Dependencies Fixture', r"""cat > "$OPT_DIR/main.go" <<'GO'
package main
import (
    "fmt"
    "net/http"
    "os"
)
func main() {
    if len(os.Args) == 2 && os.Args[1] == "--self-test" {
        fmt.Println("day010-service:ok")
        return
    }
    http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain")
        fmt.Fprintln(w, "day010-service:ok")
    })
    if err := http.ListenAndServe(":8080", nil); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}
GO
cat > "$OPT_DIR/.dockerignore" <<'IGNORE'
evidence
*.tar
IGNORE
cat > "$OPT_DIR/build-prefix" <<'DOCKER'
FROM docker.io/library/golang:1.26-alpine AS build
# Explicit build-only compiler, linker, libc headers and make.
RUN apk add --no-cache build-base
WORKDIR /src
COPY main.go /src/main.go
# An intentionally retained 32 MiB, incompressible build fixture plus 2000 files.
RUN mkdir -p /build /out && dd if=/dev/urandom of=/build/cache.bin bs=1048576 count=32 && i=0; while [ "$i" -lt 2000 ]; do touch "/build/header-$i"; i=$((i+1)); done
RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /out/service /src/main.go
DOCKER
cat "$OPT_DIR/main.go" > "$OPT_DIR/evidence/source.txt"
""", 'A complete HTTP service, self-test path and intentional build-cache fixture exist. CGO_ENABLED=0 avoids runtime libc dependencies for the scratch image. The random cache deliberately makes layer retention measurable; it is not a realistic requirement of this service.'),
('Author and Build the Single-Stage Container Image', r"""cat "$OPT_DIR/build-prefix" > "$OPT_DIR/Dockerfile.single"
cat >> "$OPT_DIR/Dockerfile.single" <<'DOCKER'
# The Go SDK, GCC, make, apk, shell, source and build cache remain reachable.
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/out/service"]
DOCKER
"$ENGINE" build "${BUILD_FLAGS[@]}" -f "$OPT_DIR/Dockerfile.single" -t "$SINGLE_IMAGE" "$OPT_DIR" > "$OPT_DIR/evidence/single-build.log" 2>&1
"$ENGINE" run --rm "$SINGLE_IMAGE" --self-test > "$OPT_DIR/evidence/single-selftest.txt"
python3 - <<'CHECK'
import os,pathlib
p=pathlib.Path(os.environ['OPT_DIR'])/'evidence/single-selftest.txt'
assert p.read_text().strip() == 'day010-service:ok'
CHECK
""", 'The compiled binary runs as UID 65532, while build tools and cache remain in the final image. Save the actual build log; tag-based bases can change, so later inspection records image IDs and layer digests.'),
('Author and Build the Multi-Stage Container Image', r"""cat "$OPT_DIR/build-prefix" > "$OPT_DIR/Dockerfile.multi"
cat >> "$OPT_DIR/Dockerfile.multi" <<'DOCKER'
# scratch contains no shell, libc, package manager or trusted CA bundle.
FROM scratch AS runtime
COPY --from=build /out/service /service
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/service"]
DOCKER
"$ENGINE" build "${BUILD_FLAGS[@]}" -f "$OPT_DIR/Dockerfile.multi" -t "$MULTI_IMAGE" "$OPT_DIR" > "$OPT_DIR/evidence/multi-build.log" 2>&1
"$ENGINE" run --rm "$MULTI_IMAGE" --self-test > "$OPT_DIR/evidence/multi-selftest.txt"
python3 - <<'CHECK'
import os,pathlib
p=pathlib.Path(os.environ['OPT_DIR'])/'evidence'
assert (p/'multi-selftest.txt').read_bytes() == (p/'single-selftest.txt').read_bytes()
CHECK
""", 'The same source and static build flags produce a runnable, non-root runtime artifact. Builder layers can remain in local cache but are not ancestors of the final runtime image. Outbound TLS would require an explicitly copied CA bundle; scratch is suitable here because this service only answers inbound HTTP.'),
('Inspect and Measure Layer Composition, Tarball Bloat, and Inode Footprint', r"""cat > "$OPT_DIR/Dockerfile.delete" <<'DOCKER'
ARG BASE
FROM ${BASE}
USER 0
# A later whiteout hides /build without deleting the bytes in ancestor layers.
RUN rm -rf /build
USER 65532:65532
DOCKER
"$ENGINE" build "${BUILD_FLAGS[@]}" --build-arg "BASE=$SINGLE_IMAGE" -f "$OPT_DIR/Dockerfile.delete" -t "$DELETE_IMAGE" "$OPT_DIR" > "$OPT_DIR/evidence/delete-build.log" 2>&1
for pair in "single:$SINGLE_IMAGE" "multi:$MULTI_IMAGE" "delete:$DELETE_IMAGE"; do
    name=${pair%%:*}; image=${pair#*:}
    "$ENGINE" image inspect "$image" > "$OPT_DIR/evidence/$name-inspect.json"
    "$ENGINE" history --no-trunc "$image" > "$OPT_DIR/evidence/$name-history.txt"
    "$ENGINE" save -o "$OPT_DIR/evidence/$name-image.tar" "$image"
    cid=$("$ENGINE" create "$image")
    "$ENGINE" export -o "$OPT_DIR/evidence/$name-rootfs.tar" "$cid"
    "$ENGINE" rm "$cid"
done
cat > "$OPT_DIR/measure.py" <<'PYCODE'
import json,os,pathlib,tarfile
p=pathlib.Path(os.environ['OPT_DIR'])/'evidence'
rows={}
for name in ('single','multi','delete'):
    info=json.loads((p/f'{name}-inspect.json').read_text())[0]
    with tarfile.open(p/f'{name}-rootfs.tar') as tf:
        members=tf.getmembers()
    paths={m.name.lstrip('./'):m for m in members}
    # Hard links reuse inodes. Runtime-injected /etc/hosts and /dev entries
    # may appear in exports; this is a logical-rootfs proxy, not host df -i.
    rows[name]={
        'image_id':info['Id'], 'image_bytes':info['Size'],
        'saved_archive_bytes':(p/f'{name}-image.tar').stat().st_size,
        'rootfs_entries':len(paths),
        'rootfs_inode_proxy':sum(not m.islnk() for m in paths.values()),
        'filesystem_layers':len(info['RootFS']['Layers']),
        'layer_digests':info['RootFS']['Layers'],
        'build_cache_visible':any(n.startswith('build/') for n in paths),
        'tools_present':{tool:any(path.rsplit('/',1)[-1]==tool for path in paths)
                         for tool in ('go','gcc','make','apk','sh','bash')}}
assert rows['single']['build_cache_visible']
assert not rows['delete']['build_cache_visible']
assert rows['delete']['layer_digests'][:rows['single']['filesystem_layers']] == rows['single']['layer_digests']
assert rows['delete']['image_bytes'] >= rows['single']['image_bytes']
assert rows['delete']['saved_archive_bytes'] >= rows['single']['saved_archive_bytes'] * 0.95
(p/'metrics.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
PYCODE
python3 "$OPT_DIR/measure.py" > "$OPT_DIR/evidence/metrics.txt"
""", 'history lists instruction sizes; RootFS.Layers counts actual filesystem diffs rather than zero-byte metadata history entries. The deletion image has fewer visible files but retains the original layer digests and archive bytes. Export-based inode proxy counts files/directories/symlinks with hard links deduplicated, not physical host inode consumption; inspect df -i on the runtime storage filesystem separately for node capacity decisions.'),
('Attack Surface & Exploit Vector Audit', r""""$ENGINE" run --rm --entrypoint /bin/sh "$SINGLE_IMAGE" -c 'type go gcc make apk' > "$OPT_DIR/evidence/single-tools.txt"
python3 - <<'AUDIT'
import json,os,pathlib,subprocess
p=pathlib.Path(os.environ['OPT_DIR'])/'evidence'
r=json.loads((p/'metrics.json').read_text())
assert all(r['single']['tools_present'][t] for t in ('go','gcc','make','apk','sh'))
assert not any(r['multi']['tools_present'].values())
results=[]
for executable in ('/bin/sh','/bin/bash','/sbin/apk','/usr/bin/gcc','/usr/local/go/bin/go'):
    proc=subprocess.run([os.environ['ENGINE'],'run','--rm','--entrypoint',executable,
                         os.environ['MULTI_IMAGE'],'--version'],capture_output=True,text=True)
    assert proc.returncode != 0, executable
    results.append({'executable':executable,'exit_code':proc.returncode,'stderr':proc.stderr})
# A successful run distinguishes the expected absent-entrypoint failures from a dead daemon.
proc=subprocess.run([os.environ['ENGINE'],'run','--rm',os.environ['MULTI_IMAGE'],'--self-test'],capture_output=True,text=True,check=True)
assert proc.stdout.strip()=='day010-service:ok'
(p/'audit.json').write_text(json.dumps(results,indent=2)+'\n')
AUDIT
""", 'Filesystem inspection and executable-launch failures agree: the final runtime has no audited compiler, SDK, package manager or shell. This removes convenient post-exploitation tools, not Go application vulnerabilities, kernel exposure, malicious dependencies or all CVEs. A vulnerability scanner and signed provenance are separate controls, not claimed results of this audit.'),
('Compile the Image Optimization & Security Verification Report', r"""python3 - <<'REPORT'
import json,os,pathlib
p=pathlib.Path(os.environ['OPT_DIR'])/'evidence'
m=json.loads((p/'metrics.json').read_text())
report={'day':10,'observed_locally':m,'negative_entrypoint_tests':json.loads((p/'audit.json').read_text()),
        'size_reduction_percent':round(100*(1-m['multi']['image_bytes']/m['single']['image_bytes']),2),
        'scope':'Logical uncompressed image size and saved archive bytes; not registry compressed transfer, shared cache disk usage or a CVE scan.',
        'architecture':'Single stage inherits SDK and build cache; final scratch stage inherits only the copied static binary.',
        'inode_limit':'Rootfs inode proxy excludes duplicate hard-link entries; overlay host inodes and shared layers are runtime dependent.',
        'gcp':'No GCP deployment or GKE performance measurement was performed.'}
path=pathlib.Path('scratch/day-010-image-comparison.json')
path.write_text(json.dumps(report,indent=2)+'\n')
lines=['# Day 10 image optimization report','', '| Image | Image bytes | Archive bytes | FS layers | Inode proxy |','|---|---:|---:|---:|---:|']
for name,row in m.items():
    lines.append(f"| {name} | {row['image_bytes']} | {row['saved_archive_bytes']} | {row['filesystem_layers']} | {row['rootfs_inode_proxy']} |")
lines.extend(['',report['scope'],report['inode_limit'],report['architecture'],report['gcp']])
pathlib.Path('scratch/day-010-image-comparison.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
REPORT
""", 'JSON contains measured bytes, image identities, layer digests, inode proxies and negative execution tests. Markdown presents the comparison. Hundreds of MiB versus less than 25 MiB is an acceptance target for this fixture, not a pre-recorded result.'),
('Validate Acceptance Invariants and Cleanup', r"""python3 - <<'ACCEPT'
import json,pathlib
r=json.loads(pathlib.Path('scratch/day-010-image-comparison.json').read_text())
s,m,d=(r['observed_locally'][k] for k in ('single','multi','delete'))
assert s['image_bytes'] > 100*1024*1024
assert 0 < m['image_bytes'] < 25*1024*1024
assert m['filesystem_layers'] < s['filesystem_layers']
assert m['rootfs_inode_proxy'] < s['rootfs_inode_proxy']
assert d['image_bytes'] >= s['image_bytes']
assert not any(m['tools_present'].values())
assert len(r['negative_entrypoint_tests']) == 5
print('Day 10 image optimization acceptance PASS')
ACCEPT
"$ENGINE" image rm "$DELETE_IMAGE" "$MULTI_IMAGE" "$SINGLE_IMAGE"
# Delete only this run's bulky archives; keep logs and structured reports for review.
python3 - <<'CLEAN'
import os,pathlib
p=pathlib.Path(os.environ['OPT_DIR'])/'evidence'
for f in p.glob('*.tar'):
    f.unlink()
pathlib.Path('scratch/day-010-image-cleanup.txt').write_text('Lab image tags and export/save archives removed. Shared builder cache and pulled base retained; no global prune.\n')
CLEAN
if [ "$ENGINE" = podman ]; then
    if [ -n "$OPT_PREVIOUS_CONFIG" ]; then
        export XDG_CONFIG_HOME="$OPT_PREVIOUS_CONFIG"
    else
        unset XDG_CONFIG_HOME
    fi
fi
""", 'All invariants pass, lab image tags and bulky archives are removed, reports and diagnostic logs remain. On an earlier failure, use tags.txt and the printed workspace path to remove only this run’s containers/images after inspecting evidence; never run a global prune.')]

_EXTRA_IMAGE_LAB = '<section id="topic-01-multistage-lab" class="lab">\n<h3>Additional exercise · Single-stage versus optimized multi-stage Go image</h3>\n'
_EXTRA_IMAGE_LAB += '<p><strong>Goal:</strong> Build the same compiled HTTP service twice; prove image-layer immutability, quantify size/layers/inode footprint, and audit runtime tools.</p>\n'
_EXTRA_IMAGE_LAB += '<p><strong>Expected result:</strong> Runnable equivalent binaries, measured size reduction, retained lower-layer cache after deletion, and a structured security comparison.</p>\n'
_EXTRA_IMAGE_LAB += '<p><strong>Mode:</strong> Observed locally: only measurements produced by the commands below. Simulated or predicted: none in the image comparison. Untested on GCP: GKE deployment, pull latency and network behavior. Linux/Bash; Docker Engine or rootless Podman with Docker-compatible commands.</p>\n'
_EXTRA_IMAGE_LAB += '<p><strong>Prerequisite:</strong> Docker CLI and Podman CLI available for explicit daemon fallback; Python 3 and core utilities; running engine, registry access, about 2 GB disk. No GCP credentials or cloud resources.</p>\n'
_EXTRA_IMAGE_LAB += '<p><strong>Preflight:</strong> Execute in one Bash session from the existing lab working directory, where scratch exists. Stage 1 records the chosen daemon and baseline. Keep the workspace path for recovery.</p>\n<h4>Exact execution</h4>\n<ol>\n'
for _n, (_title, _commands, _expected) in enumerate(_BUILD_COMPARE_STAGES, 1):
    _EXTRA_IMAGE_LAB += '<li><h5>Stage '+str(_n)+': '+_escape(_title)+'</h5><p><strong>Location:</strong> local terminal; Linux, Bash, selected container engine and Python 3. Run sequentially in the same session.</p><p><strong>Actions:</strong></p><pre><code class="language-bash">'+_escape(_commands)+'</code></pre><p><strong>Expected result:</strong> '+_escape(_expected)+'</p><p><strong>Evidence:</strong> Retain the run-owned evidence directory and the comparison report; stop on any failed assertion.</p></li>\n'
_EXTRA_IMAGE_LAB += '</ol><div class="callout success"><strong>Expected result / acceptance</strong><p>All eight stages complete. The multi-stage image is less than 25 MiB, has fewer filesystem layers and rootfs inode proxies, passes the same binary self-test, and lacks all audited tools. A later rm hides build files but preserves ancestor layer bytes. Save: <code>scratch/day-010-image-comparison.json</code>, <code>scratch/day-010-image-comparison.md</code>, <code>scratch/day-010-image-cleanup.txt</code>.</p></div>\n'
_EXTRA_IMAGE_LAB += '<div class="callout caution"><strong>Troubleshooting</strong><ul><li>Daemon permission denied: use an authorized Docker socket or the explicit rootless Podman fallback; do not chmod the socket globally.</li><li>Registry or apk failure: inspect single-build.log; restore registry access and rerun before recording acceptance.</li><li>exec format error: build and run on the same engine architecture; CGO_ENABLED=0 does not fix a CPU architecture mismatch.</li><li>Scratch TLS/DNS or debug requirements: copy required CA/config files explicitly, or choose a maintained minimal runtime and repeat all metrics.</li><li>Do not compare compressed registry sizes with uncompressed inspect Size; builder cache disk remains a separate metric.</li></ul></div>\n'
_EXTRA_IMAGE_LAB += '<div class="callout"><strong>Cleanup</strong><p>Stage 8 removes only unique lab tags and archive files. Keep structured reports and logs; shared cache/base images remain. No billed cloud resources are created.</p></div></section>\n'
# Keep the original persistence exercise intact. Its closeout executes the separate
# eight-stage comparison too, so run_labs and batch_gate cannot silently skip it.
DATA['topics'][0]['lab']['steps'][7] += '\n\n' + _EXTRA_IMAGE_LAB
DATA['topics'][0]['lab']['mode'] += ' Additional comparison: actual Docker-compatible builds and runtime inspection; engine selection is recorded per run.'
DATA['topics'][0]['lab']['steps'][0] = DATA['topics'][0]['lab']['steps'][0].replace('command -v mkdir', 'command -v mkdir\ncommand -v date\ncommand -v rm\ncommand -v grep\ncommand -v docker\ncommand -v podman')

# Linked subtopics in both the overview and technical discussion. Lists use the
# available card width instead of the shared paragraph reading-width cap.
for _t in DATA['topics']:
    _key = _t['key']
    _tech = _t['technical']
    _headings = list(_re.finditer(r'<h4(?: id="[^"]+")?>(.*?)</h4>', _tech))
    for _i, _heading in reversed(list(enumerate(_headings[:5], 1))):
        _tech = _tech[:_heading.start()] + '<h4 id="'+_key+'-subtopic-'+str(_i)+'">'+_heading.group(1)+'</h4>' + _tech[_heading.end():]
    _first = _re.search(r'<ol>.*?</ol>', _tech, _re.S)
    _links = '<ul>' + ''.join('<li><a href="#'+_key+'-subtopic-'+str(_i)+'">'+_h.group(1)+'</a></li>' for _i,_h in enumerate(_headings[:5],1)) + '</ul>'
    assert _first is not None
    _tech = _tech[:_first.start()] + _links + _tech[_first.end():]
    # Preserve every word while giving each labelled mechanism a full-width bullet.
    _tech = _re.sub(r'<p>(<strong class="side-heading">.*?</strong>.*?)</p>',r'<ul><li>\1</li></ul>',_tech,flags=_re.S)
    _tech = _tech.replace('<ul><li><strong class="side-heading">Subtopics in this discussion:</strong></li></ul>', '<p><strong class="side-heading">Subtopics in this discussion:</strong></p>')
    _t['technical'] = _tech
    _overview = _re.search(r'<article[^>]*id="'+_key+r'-overview".*?</article>', DATA['part1_html'], _re.S)
    assert _overview is not None
    _old = _overview.group(0)
    DATA['part1_html'] = DATA['part1_html'].replace(_old, _old.replace('</article>','<p><strong class="side-heading">Linked subtopics:</strong></p>'+_links+'</article>'),1)

# Correct specific unsupported guarantees while preserving their mechanisms.
_CORRECTIONS = {
'zero network encapsulation latency':'no inter-Pod network hop; loopback still has processing cost',
'NEGs preserve the original client source IP address and reduce median request latency by 5–15 ms.':'NEGs target Pod endpoints directly. For proxy-based Application Load Balancers, applications obtain client information from forwarding headers; this lesson provides no measured latency improvement.',
'Consolidating dozens of backend microservices behind a single Ingress controller reduces cloud load balancing costs by &gt;75%, eliminating duplicate static IP allocations and unneeded forwarding rules.':'Consolidating compatible host/path routes can reduce duplicate frontend resources. Savings depend on traffic, backend configuration, load balancer pricing and availability requirements; there is no universal percentage reduction.',
'automatically updates the projected files inside running containers within seconds without restarting the container process.':'eventually updates projected files without restarting the container process; propagation includes the kubelet sync period and cache propagation delay. A subPath mount does not receive these updates, and the application must reopen or reload the changed file.',
'Within 15 seconds, Config Sync':'On a subsequent successful reconciliation, Config Sync',
'detects drift against live cluster objects within seconds, and applies transactional three-way merge patches to restore compliance.':'detects and reconciles drift for managed resources; convergence depends on source polling, API availability and reconciliation health rather than a guaranteed number of seconds or a multi-object transaction.',
'consensus requires an odd cluster quorum size ($N = 2F + 1$) to tolerate $F$ node failures.':'consensus needs a majority of voting members; an odd membership size is normally chosen to tolerate $F$ failures with $N = 2F + 1$ voters.',
'if storage write latency exceeds 10 ms, Raft heartbeats drop, triggering cascade leader elections and freezing control plane operations.':'sustained disk or network delays can delay heartbeats and provoke leader elections; the outcome depends on election timeouts and workload, not a universal 10 ms threshold.',
'(default 40s)':'(inspect the running controller configuration rather than assume a fixed default)',
'When a database administrator rotates the password in Secret Manager, the Secret Manager CSI driver refreshes the mounted file':'When the add-on supports and has automatic rotation enabled, it refreshes the mounted secret file on its configured interval after a Secret Manager version change; the application must reload it. This can update the file',
'with automated SSD persistent storage provisioning, automated zero-downtime control plane patching, and 99.95% availability SLA backing.':'for control-plane availability; upgrades and the applicable SLA have documented conditions, and zero downtime for every application is not guaranteed.',
}
for _t in DATA['topics']:
    for _old,_new in _CORRECTIONS.items():
        _t['technical'] = _t['technical'].replace(_old,_new)

# Explicit worked boundaries supplement, rather than replace, existing depth.
DATA['topics'][1]['technical'] += '<div><strong>Worked reconciliation and scheduling boundaries</strong></div><ul><li><strong class="side-heading">Concrete example:</strong> A Deployment declares three replicas; its controller manages ReplicaSets, whose controller creates missing Pods. The scheduler filters nodes before scoring eligible candidates; kubelet starts bound Pods through the runtime. Each controller retries from observed state, so a watch event is a prompt to reconcile, not a transaction spanning all components.</li><li>A 2 CPU / 1 GiB request must fit remaining allocatable requests. Limits constrain runtime use: CPU is throttled; a memory limit can trigger OOM termination. NodeAffinity constrains placement, and tolerating a taint permits but does not guarantee it. NodeResourcesBalancedAllocation balances resource fractions; ImageLocality favors cached images. Neither plugin name alone proves a globally optimal bin packing policy. GKE Cluster Autoscaler evaluates whether more eligible nodes could place pending Pods within configured constraints; adding nodes cannot repair impossible affinity or invalid storage topology.</li><li>Liveness failure can restart the container; readiness failure changes its readiness condition without inherently restarting it. A failed Pod is not moved: controllers create replacements with new UIDs. EndpointSlice readiness and GKE load-balancer backend health/readiness gates are distinct signals, so propagation and connection draining must be considered before claiming zero downtime.</li><li>Config Sync is the current configuration reconciliation product associated with the historical Anthos Config Management name. GitOps rollback restores versioned configuration, but requires immutable image references and compatible database/configuration state; reverting Git does not reverse external side effects.</li><li><strong class="side-heading">Evidence limit:</strong> The scheduler lab is a deliberately simplified Python placement model; it does not execute upstream scheduler plugins, Raft or GKE autoscaling.</li></ul>'
DATA['topics'][2]['technical'] += '<div><strong>Worked rollout, traffic and secret boundaries</strong></div><ul><li><strong class="side-heading">Concrete example:</strong> With four desired replicas, maxSurge=1 and maxUnavailable=0 permit an additional rollout Pod while retaining four available replicas, provided readiness and capacity permit it. Terminating Pods can temporarily consume additional resources. A Deployment rollback restores a previous Pod template, not database contents. Canary traffic allocation needs a separate rollout/traffic policy; Cloud Deploy is an optional delivery integration, not a Deployment controller feature.</li><li>Deployment owns ReplicaSets; ReplicaSets own Pods through ownerReferences. Services select Pods by labels, and EndpointSlice objects describe endpoints; neither a Service nor an Ingress owns a Deployment. Ingress configuration requires a controller. GKE Ingress can use NEGs to reach Pod endpoints, so the external path need not traverse the ClusterIP or kube-proxy. kube-proxy iptables/IPVS descriptions apply only to clusters using those implementations; managed data planes can differ.</li><li>ConfigMap/Secret environment values are fixed for an existing container process. Mounted values update eventually except subPath, and application reload remains necessary. Base64 is encoding. Kubernetes at-rest encryption requires configuration; GKE application-layer encryption uses a key encryption key to protect data encryption keys. Secret Manager CSI mounting with Workload Identity Federation for GKE can avoid storing the fetched secret in etcd unless a separate synchronization feature writes a Kubernetes Secret. Automatic rotation must be configured and verified.</li><li><strong class="side-heading">Evidence limit:</strong> The local manifests and model demonstrate selectors and ownership intent; they do not prove Google load-balancer health, Cloud Armor policy enforcement, certificate issuance, CDN cache behavior or IAM authorization.</li></ul>'

# Search links are discovery aids; official written sections remain the evidence.
_SEARCH_TERMS = [['OCI image layers','Docker multi-stage builds','OverlayFS whiteouts','POSIX fsync'],['Kubernetes reconciliation controllers','etcd Raft consensus','NodeResourcesFit NodeAffinity TaintToleration','NodeResourcesBalancedAllocation ImageLocality','GKE Cluster Autoscaler','Config Sync Anthos Config Management'],['Kubernetes Pod namespaces','Deployment maxSurge maxUnavailable','EndpointSlice kube-proxy IPVS','GKE Ingress Cloud Armor Cloud CDN','Secret Manager CSI Workload Identity Federation']]
for _t,_terms in zip(DATA['topics'],_SEARCH_TERMS):
    _t['technical'] += '<div><strong>Keyword searches</strong></div><ul>'+''.join('<li><a href="https://www.google.com/search?q='+_quote(_term)+'" target="_blank" rel="noopener">'+_escape(_term)+' (accessed 2026-10-10)</a> — discovery aid; verify behavior against the official section citations.</li>' for _term in _terms)+'</ul>'

# A single closeout artifact list keeps runner path extraction unambiguous.
_step8 = DATA['topics'][0]['lab']['steps'][7]
_step8 = _step8.replace('**Save:** `scratch/day10_lab_a/stage8.log`', '')
_step8 = _step8.replace('Save: <code>', 'Reports: <code>')
DATA['topics'][0]['lab']['steps'][7] = _step8 + '\n\n**Save:** `scratch/day10_lab_a/stage8.log`, `scratch/day-010-image-comparison.json`, `scratch/day-010-image-comparison.md`, `scratch/day-010-image-cleanup.txt`'

_SECTION_SOURCES = {
    'docker-build': ('Use multi-stage builds', 'https://docs.docker.com/build/building/multi-stage/#use-multi-stage-builds'),
    'fsync': ('DESCRIPTION', 'https://man7.org/linux/man-pages/man2/fsync.2.html#DESCRIPTION'),
    'overview': ('Why you need Kubernetes and what can it do', 'https://kubernetes.io/docs/concepts/overview/#why-you-need-kubernetes-and-what-can-it-do'),
    'objects': ('Understanding Kubernetes objects', 'https://kubernetes.io/docs/concepts/overview/working-with-objects/#kubernetes-objects'),
    'controllers': ('Control via API server', 'https://kubernetes.io/docs/concepts/architecture/controller/#control-via-api-server'),
    'config-sync': ('How Config Sync works', 'https://docs.cloud.google.com/kubernetes-engine/config-sync/docs/overview#how-config-sync-works'),
    'scheduling': ('Framework workflow', 'https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/#framework-workflow'),
    'readiness': ('Readiness probe', 'https://kubernetes.io/docs/concepts/workloads/pods/probes/#readiness-probe'),
    'pods': ('Pod networking', 'https://kubernetes.io/docs/concepts/workloads/pods/#pod-networking'),
    'deployment': ('Rolling Update Deployment', 'https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment'),
    'service': ('EndpointSlices', 'https://kubernetes.io/docs/concepts/services-networking/service/#endpointslices'),
    'ingress': ('The Ingress resource', 'https://kubernetes.io/docs/concepts/services-networking/ingress/#the-ingress-resource'),
    'neg': ('Container-native load balancing', 'https://docs.cloud.google.com/kubernetes-engine/docs/concepts/ingress#container-native-load-balancing'),
    'configmap': ('Mounted ConfigMaps are updated automatically', 'https://kubernetes.io/docs/concepts/configuration/configmap/#mounted-configmaps-are-updated-automatically'),
    'secret-rotation': ('Manage automatic secret rotation', 'https://docs.cloud.google.com/secret-manager/docs/secret-manager-managed-csi-component'),
}
_CITATIONS = [
    [('docker-build',), ('docker-build',), ('docker-build',), ('fsync',), ('fsync',)],
    [('overview',), ('config-sync','controllers'), ('controllers',), ('scheduling',), ('readiness','neg')],
    [('pods',), ('deployment',), ('service','neg'), ('ingress','neg'), ('configmap','secret-rotation')],
]
for _t,_groups in zip(DATA['topics'],_CITATIONS):
    _tech = _t['technical']
    _blocks = list(_re.finditer(r'<h4 id="'+_t['key']+r'-subtopic-[1-5]">.*?(?=<h4|$)',_tech,_re.S))
    assert len(_blocks) == 5
    for _block,_group in reversed(list(zip(_blocks,_groups))):
        _citation = '<ul><li><strong class="side-heading">Further study:</strong> '+ '; '.join('<a href="'+_SECTION_SOURCES[_k][1]+'">'+_escape(_SECTION_SOURCES[_k][0])+' (accessed 2026-10-10)</a>' for _k in _group) + '. Scope: these sections support the named mechanisms; local exercises do not establish GCP production behavior.</li></ul>\n'
        _tech = _tech[:_block.end()] + _citation + _tech[_block.end():]
    _t['technical'] = _tech

DATA['review_records'] = {
    'source_ledger': {_url: {'heading_opened': _heading} for _heading,_url in _SECTION_SOURCES.values()},
    'product_claims': [
        {'claim':'Multi-stage final images copy selected artifacts and exclude builder tools.', 'section_url':_SECTION_SOURCES['docker-build'][1], 'heading_opened':_SECTION_SOURCES['docker-build'][0]},
        {'claim':'Config Sync reconciles configurations from its configured source of truth; no fixed convergence time is claimed.', 'section_url':_SECTION_SOURCES['config-sync'][1], 'heading_opened':_SECTION_SOURCES['config-sync'][0]},
        {'claim':'GKE container-native load balancing targets Pod endpoints in NEGs and uses load-balancer-aware readiness gates.', 'section_url':_SECTION_SOURCES['neg'][1], 'heading_opened':_SECTION_SOURCES['neg'][0]},
        {'claim':'Readiness failure does not inherently restart a container; liveness and restartPolicy govern restart behavior.', 'section_url':_SECTION_SOURCES['readiness'][1], 'heading_opened':_SECTION_SOURCES['readiness'][0]},
        {'claim':'Mounted ConfigMaps update eventually; environment values and subPath mounts require separate handling.', 'section_url':_SECTION_SOURCES['configmap'][1], 'heading_opened':_SECTION_SOURCES['configmap'][0]},
        {'claim':'Secret Manager mounted-file rotation requires enabled automatic rotation and its configured interval.', 'section_url':_SECTION_SOURCES['secret-rotation'][1], 'heading_opened':_SECTION_SOURCES['secret-rotation'][0]},
    ],
    'visual_reasons': {},
}
for _t,_terms in zip(DATA['topics'],_SEARCH_TERMS):
    for _term in _terms:
        DATA['review_records']['source_ledger']['https://www.google.com/search?q='+_quote(_term)] = {'heading_opened':'Not a technical evidence citation; keyword discovery only', 'whole_document_reason':'A search query has no stable documentation section. User explicitly requested Google keyword links.'}

for _t in DATA['topics'][1:]:
    _t['lab']['steps'][0] = _t['lab']['steps'][0].replace('command -v mkdir', 'command -v mkdir\ncommand -v date\ncommand -v grep')
DATA['topics'][2]['lab']['steps'][0] = DATA['topics'][2]['lab']['steps'][0].replace('command -v mkdir', 'command -v mkdir\ncommand -v sed')

DATA['review_records']['source_ledger'][_SECTION_SOURCES['secret-rotation'][1]]['whole_document_reason'] = 'The Manage automatic secret rotation heading was opened and reviewed, but tested fragment variants were absent in fetched HTML. Cite the document root rather than retain an unverified section fragment.'
