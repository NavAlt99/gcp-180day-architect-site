"""Scenarios and 8-stage step-by-step labs for Day 9: VM and container isolation."""

SCENARIOS_AND_LABS = {
    'topic-01': {
        'scenario': {
            'scenario': 'A legacy enterprise tax calculation service requires a proprietary third-party Linux kernel module to execute hardware-accelerated cryptographic valuation routines. When deployed onto an existing Kubernetes container cluster running Container-Optimized OS, the application container crashloops immediately upon startup, reporting permission denied during module insertion.',
            'impact': 'Synthetic tax calculation calls and e-commerce checkout integration tests fail with HTTP 500 errors; the deployment pipeline is halted; customer order checkout cannot proceed without tax calculation certification.',
            'constraints': 'GKE worker nodes run an immutable, locked-down Linux kernel where arbitrary module loading is disabled; granting containers privileged security contexts violates company-wide security guardrails; the vendor contract mandates execution of the binary kernel module.',
            'evidence': 'Reviewing container startup logs reveals "insmod: ERROR: could not insert module tax_crypto.ko: Operation not permitted". Inspecting the process capabilities confirms that CAP_SYS_MODULE was dropped by the container runtime. The host container node kernel (/lib/modules) is mounted read-only and lacks matching kernel headers.',
            'root': 'The container architecture multiplexes a single shared host Linux kernel. Inserting a kernel module into a container requires modifying the shared host kernel space, which is blocked by dropped capabilities (CAP_SYS_MODULE) and node immutability. Containers do not possess an independent guest kernel.',
            'verify': 'The tax calculation adapter is relocated to a dedicated Compute Engine virtual machine running Debian with a sovereign guest kernel. The vendor kernel module loads successfully into the guest kernel; synthetic checkout requests return HTTP 200 with accurate tax calculations; the shared Kubernetes container nodes remain completely uncompromised and unmodified.',
            'residual': 'The dedicated VM incurs a dedicated operating system memory overhead baseline (~1 GB RAM) and requires automated guest OS patching via Compute Engine VM Manager / OS Config.',
            'diagram_enabled': True,
            'facts': 'Supplied facts: The tax calculation adapter requires a specialized kernel module, and container nodes run an immutable locked kernel.',
            'inference': 'Architectural inference: Placing the workload into a dedicated VM with its own guest kernel resolves kernel-space dependencies without compromising shared container node security.',
            'expected': 'Expected post-fix behavior: Synthetic tax requests return HTTP 200 while host nodes remain unmodified; this is an architectural scenario, not production telemetry.',
            'diagram': (
                'Tax calculation service receives synthetic checkout requests',
                'Shared container kernel drops CAP_SYS_MODULE blocking insmod',
                'Module insertion fails with EPERM causing container crashloop',
                'Place adapter on dedicated Compute Engine VM with sovereign guest kernel',
                'Vendor kernel module loads in guest; synthetic tax requests succeed'
            ),
            'icons': (
                '../assets/icons/generic/client.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/gcp/core/compute-engine.svg',
                '../assets/icons/generic/outcome.svg'
            ),
            'diagnostic_steps': [
                'Inspect container failure logs: kubectl logs deployment/tax-calculator --tail=50',
                'Verify dropped capabilities: grep CapEff /proc/[pid]/status and decode via capsh --decode',
                'Examine node kernel immutability: mount | grep /lib/modules and verify ro mount flag',
                'Test module loading in an isolated test environment: insmod tax_crypto.ko to observe EPERM'
            ],
            'remediation_steps': [
                'Provision a dedicated Compute Engine instance (e2-standard-2) with Debian 12 using Terraform',
                'Install vendor kernel headers and build/insert tax_crypto.ko into the VM guest kernel',
                'Deploy the tax calculation service application onto the VM systemd service manager',
                'Configure internal Cloud Load Balancing to route synthetic tax requests to the VM endpoint',
                'Validate that synthetic tax calculation requests return HTTP 200 with verified cryptographic signatures'
            ]
        },
        'lab': {
            'name': 'Exercise A · Draw and challenge the kernel boundary',
            'goal': 'Map the architectural boundary between guest kernel autonomy in virtual machines and shared kernel execution in containers by testing kernel module placement and verifying isolation failure.',
            'expected': 'An executable placement verification demonstrating that custom kernel dependencies require guest kernel sovereignty, recorded in the isolation comparison worksheet.',
            'mode': 'Observed locally: local bash simulation of kernel dependency checking and placement verification. Simulated or predicted: Compute Engine KVM hypervisor guest kernel boot and module loading. Untested on GCP: live physical host hypervisor hardware register traps (VM-Exit) and Andromeda SDN virtio packet offloading.',
            'covers': "Inspect a local container's namespaces, cgroup limits and user identity; compare its isolation boundary with a VM diagram.",
            'prereq': 'Linux terminal environment with bash and standard core utilities.',
            'preflight': 'Verify that bash, python3, and standard POSIX shell utilities are available in the local environment.',
            'verification': 'Run the validation script to verify that the placement decision logic accurately flags kernel module incompatibilities on container runtimes.',
            'trouble': 'If directory permissions prevent creating test fixtures, ensure commands are executed within the scratch/ workspace directory.',
            'cleanup': 'Remove temporary simulation scripts and test artifacts generated in scratch/.',
            'accept': 'The placement evaluation log correctly categorizes kernel module dependencies as requiring VM guest kernel isolation.',
            'file': 'day-009-exercise-a.md',
            'steps': [
                '''**Stage 1: Preflight and Environment Baseline**

**Location:** local terminal

**Actions:**
Verify that the execution environment contains the necessary CLI tools and create the isolated scratch workspace.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day09_lab_a
echo "Stage 1 preflight initialized at $(date -u +%Y-%m-%dT%H:%M:%SZ)" > scratch/day09_lab_a/stage1.log
cat scratch/day09_lab_a/stage1.log
```

**Expected result:** Tool paths are verified and `stage1.log` contains an ISO timestamp.

**Save:** `scratch/day09_lab_a/stage1.log`''',

                '''**Stage 2: Establish the Workload Fixture and Kernel Dependency**

**Location:** local terminal

**Actions:**
Create a workload definition file describing two candidate services: a standard stateless REST API and a specialized cryptographic tax adapter requiring a proprietary kernel module.
```bash
cat <<'EOF' > scratch/day09_lab_a/workloads.json
{
  "workloads": [
    {
      "id": "order-api",
      "name": "Order Management API",
      "runtime": "python-fastapi",
      "requires_kernel_module": false,
      "requires_raw_sockets": false,
      "memory_mb": 256
    },
    {
      "id": "tax-adapter",
      "name": "Cryptographic Tax Engine",
      "runtime": "c-native",
      "requires_kernel_module": true,
      "module_name": "tax_crypto.ko",
      "memory_mb": 512
    }
  ]
}
EOF
python3 -m json.tool scratch/day09_lab_a/workloads.json > /dev/null && echo "Fixture validated" > scratch/day09_lab_a/stage2.log
cat scratch/day09_lab_a/stage2.log
```

**Expected result:** `workloads.json` is formatted properly and `stage2.log` confirms fixture validation.

**Save:** `scratch/day09_lab_a/stage2.log`''',

                '''**Stage 3: Test Container Kernel Placement and Observe the Isolation Boundary**

**Location:** local terminal

**Actions:**
Execute a placement evaluation engine that simulates deploying both workloads to a shared-kernel container runtime (e.g., standard GKE / Container-Optimized OS).
```bash
cat <<'EOF' > scratch/day09_lab_a/evaluate_container.py
import json, sys

with open("scratch/day09_lab_a/workloads.json") as f:
    data = json.load(f)

results = []
for w in data["workloads"]:
    if w["requires_kernel_module"]:
        results.append({
            "id": w["id"],
            "target": "shared-container",
            "status": "REJECTED",
            "error": "EPERM: CAP_SYS_MODULE dropped by container runtime",
            "reason": "Containers share host kernel; custom .ko modules cannot be loaded without compromising host integrity."
        })
    else:
        results.append({
            "id": w["id"],
            "target": "shared-container",
            "status": "ACCEPTED",
            "reason": "Standard userspace runtime executes cleanly within Linux namespaces and cgroups."
        })

with open("scratch/day09_lab_a/container_placement.json", "w") as f:
    json.dump(results, f, indent=2)
print("Container evaluation complete")
EOF
python3 scratch/day09_lab_a/evaluate_container.py > scratch/day09_lab_a/stage3.log
cat scratch/day09_lab_a/container_placement.json
```

**Expected result:** `tax-adapter` is REJECTED with EPERM, while `order-api` is ACCEPTED.

**Save:** `scratch/day09_lab_a/stage3.log`''',

                '''**Stage 4: Emulate Sovereign Virtual Machine Guest Kernel Placement**

**Location:** local terminal

**Actions:**
Evaluate the placement of the rejected tax adapter into a dedicated Compute Engine virtual machine with a sovereign guest kernel.
```bash
cat <<'EOF' > scratch/day09_lab_a/evaluate_vm.py
import json

with open("scratch/day09_lab_a/workloads.json") as f:
    data = json.load(f)

vm_results = []
for w in data["workloads"]:
    vm_results.append({
        "id": w["id"],
        "target": "compute-engine-vm",
        "status": "ACCEPTED",
        "isolation_boundary": "Type 1 KVM / Sovereign Guest Kernel",
        "module_support": "Supported: guest kernel loads module into private virtual Ring 0 space without host impact.",
        "overhead_mb": 768
    })

with open("scratch/day09_lab_a/vm_placement.json", "w") as f:
    json.dump(vm_results, f, indent=2)
print("VM placement evaluation complete")
EOF
python3 scratch/day09_lab_a/evaluate_vm.py > scratch/day09_lab_a/stage4.log
cat scratch/day09_lab_a/vm_placement.json
```

**Expected result:** `tax-adapter` is ACCEPTED on the VM with sovereign guest kernel module support.

**Save:** `scratch/day09_lab_a/stage4.log`''',

                '''**Stage 5: Compare Resource Overhead vs Isolation Guarantees**

**Location:** local terminal

**Actions:**
Generate a quantitative comparison of memory overhead and boot latency between virtual machine isolation and container execution.
```bash
cat <<'EOF' > scratch/day09_lab_a/compare_overhead.py
import json

with open("scratch/day09_lab_a/workloads.json") as f:
    workloads = json.load(f)["workloads"]

print(f"{'WORKLOAD':<16} | {'CONTAINER RAM':<14} | {'VM RAM (GUEST)':<16} | {'OVERHEAD FACTOR'}")
print("-" * 65)
for w in workloads:
    c_ram = w["memory_mb"]
    vm_ram = c_ram + 768  # 768 MB guest OS kernel + systemd overhead
    ratio = vm_ram / c_ram
    print(f"{w['id']:<16} | {c_ram:>4} MB        | {vm_ram:>4} MB          | {ratio:>4.1f}x")
EOF
python3 scratch/day09_lab_a/compare_overhead.py > scratch/day09_lab_a/stage5.log
cat scratch/day09_lab_a/stage5.log
```

**Expected result:** Output displays a side-by-side memory footprint comparison highlighting the 2.5x to 4x memory overhead factor of dedicated VMs.

**Save:** `scratch/day09_lab_a/stage5.log`''',

                '''**Stage 6: Challenge the Boundary with a Privileged Container Antipattern**

**Location:** local terminal

**Actions:**
Simulate an insecure proposal to run the tax adapter in a privileged container (`--privileged` or `CAP_SYS_MODULE` added) and produce a security risk assessment.
```bash
cat <<'EOF' > scratch/day09_lab_a/security_assessment.py
assessment = {
    "antipattern": "Running privileged container with CAP_SYS_MODULE on shared GKE node",
    "risks": [
        "Shared Kernel Compromise: Module crashes trigger host-wide kernel panic (oops), taking down all collocated pods.",
        "Privilege Escalation: An inserted module runs at Ring 0 with unrestricted access to physical memory and neighboring tenant secrets.",
        "Cluster Policy Violation: Violates GKE Autopilot and standard CIS Kubernetes Benchmarks."
    ],
    "recommendation": "Maintain strict security policy: Reject privileged container; deploy to dedicated Compute Engine VM."
}
import json
with open("scratch/day09_lab_a/security_risks.json", "w") as f:
    json.dump(assessment, f, indent=2)
print("Security risk assessment documented")
EOF
python3 scratch/day09_lab_a/security_assessment.py > scratch/day09_lab_a/stage6.log
cat scratch/day09_lab_a/security_risks.json
```

**Expected result:** Security risks of privileged containers on shared kernels are systematically itemized.

**Save:** `scratch/day09_lab_a/stage6.log`''',

                '''**Stage 7: Formulate Workload Placement Policy Rules**

**Location:** local terminal

**Actions:**
Codify the architectural placement rules into a deterministic decision matrix function.
```bash
cat <<'EOF' > scratch/day09_lab_a/placement_rules.py
def decide_placement(workload):
    if workload.get("requires_kernel_module"):
        return "Compute Engine VM (Sovereign Guest Kernel Required)"
    if workload.get("requires_custom_drivers"):
        return "Compute Engine VM (Custom Hardware Driver Required)"
    if workload.get("untrusted_multitenant_code"):
        return "Cloud Run / GKE Sandbox with gVisor (Sandboxed Userspace Kernel)"
    return "Standard GKE / Cloud Run Container (Shared Linux Kernel)"

print("Decision engine rules compiled successfully")
EOF
python3 scratch/day09_lab_a/placement_rules.py > scratch/day09_lab_a/stage7.log
cat scratch/day09_lab_a/stage7.log
```

**Expected result:** `stage7.log` confirms that the architectural placement rules compiled successfully.

**Save:** `scratch/day09_lab_a/stage7.log`''',

                '''**Stage 8: Validate the Placement Decision Evidence**

**Location:** local terminal

**Actions:**
Execute the decision rules across all workload fixtures and record the final verification report.
```bash
python3 -c '
import json
from scratch.day09_lab_a.placement_rules import decide_placement

with open("scratch/day09_lab_a/workloads.json") as f:
    workloads = json.load(f)["workloads"]

print("=== FINAL ARCHITECTURAL WORKLOAD PLACEMENT REPORT ===")
for w in workloads:
    decision = decide_placement(w)
    print(f"Workload: {w[\"name\"]} ({w[\"id\"]}) -> Recommendation: {decision}")
' > scratch/day09_lab_a/final_report.txt
cat scratch/day09_lab_a/final_report.txt
```

**Expected result:** The final report displays accurate placement recommendations for both workloads.

**Save:** `scratch/day09_lab_a/final_report.txt`'''
            ]
        }
    },
    'topic-02': {
        'scenario': {
            'scenario': 'A fulfillment worker service running in a Kubernetes pod crashes repeatedly with exit code 137 during end-of-month batch invoicing. The operations team checks Cloud Monitoring host metrics and observes that the underlying virtual machine node has 12 GB of free physical RAM out of 16 GB total, leading them to erroneously suspect a network timeout or application bug.',
            'impact': 'Customer invoice processing and packing slip printing stall; queue messages are retried repeatedly, causing duplicate shipment notices; operational on-call engineers spend hours investigating the wrong architectural layer.',
            'constraints': 'The Kubernetes pod deployment specifies a memory limit of 512 MiB (resources.limits.memory: "512Mi"); the node host operating system has ample unallocated memory; application invoicing logic generates uncompressed raster PDF invoices in memory before streaming.',
            'evidence': 'Reviewing Kubernetes pod status reveals "OOMKilled: true, ExitCode: 137". Checking the container cgroups v2 telemetry under /sys/fs/cgroup reveals that memory.events recorded oom_kill increments matching the exact pod restart timestamps.',
            'root': 'The application working set exceeded the isolated container cgroup v2 memory.max boundary (512 MiB) during batch PDF rendering. The Linux kernel cgroup OOM killer terminated the worker process with SIGKILL (exit code 137) to enforce the container limit, entirely independently of host-level physical RAM availability.',
            'verify': 'The application code is refactored to stream PDF generation in chunked byte streams rather than buffering entire document sets in heap memory. The pod memory limit is right-sized to 1024 MiB with a matching request. Verification confirms zero OOM kills over 24 hours of batch processing while host memory utilization remains stable.',
            'residual': 'Allocating 1024 MiB per worker pod increases node reservation requirements, necessitating cluster autoscaler capacity planning to handle peak batch scaling events.',
            'diagram_enabled': True,
            'facts': 'Supplied facts: Worker terminates with exit code 137 despite 70% host free memory headroom.',
            'inference': 'Architectural inference: The worker exceeded its isolated cgroup v2 memory.max boundary during in-memory buffering.',
            'expected': 'Expected post-fix behavior: Streamed invoice generation and calibrated memory limits prevent OOM termination while queue deduplication preserves at-most-once fulfillment semantics.',
            'diagram': (
                'Batch fulfillment worker receives order packaging events',
                'In-memory PDF rasterization buffers 640 MB in heap',
                'cgroup memory.max breached triggering SIGKILL 137 OOM termination',
                'Refactor to chunked stream I/O and calibrate cgroup limit to 1024 MB',
                'Peak working set capped at 280 MB; zero OOM kills observed'
            ),
            'icons': (
                '../assets/icons/generic/queue.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/monitoring.svg',
                '../assets/icons/generic/outcome.svg'
            ),
            'diagnostic_steps': [
                'Inspect pod termination reason: kubectl describe pod fulfillment-worker-[id] | grep -A 5 "Last State:"',
                'Inspect cgroups v2 memory events: cat /sys/fs/cgroup/memory.events inside or at node slice level',
                'Correlate host memory graphs against container memory working set in Cloud Monitoring',
                'Profile application heap allocation during PDF generation using memory profilers'
            ],
            'remediation_steps': [
                'Refactor PDF generation logic to stream output to temporary storage or Cloud Storage in 8 MB chunks',
                'Update Kubernetes deployment resource limits to resources.limits.memory: "1024Mi"',
                'Configure Kubernetes Horizontal Pod Autoscaler based on container memory utilization',
                'Deploy Prometheus / Cloud Monitoring alerting rules on container_memory_working_set_bytes vs limit',
                'Verify that batch fulfillment completes with zero OOM events and stable process PIDs'
            ]
        },
        'lab': {
            'name': 'Exercise B · Read your process isolation facts',
            'goal': 'Empirically inspect the active Linux kernel container isolation subsystems directly: inspect namespace inodes under /proc/[pid]/ns/, examine cgroups v2 controller hierarchy and memory accounting, decode POSIX capabilities, and verify seccomp filtering status.',
            'expected': 'An isolation worksheet distinguishing resource enforcement from security isolation, verifying that namespaces control visibility, cgroups control resource limits, and seccomp/capabilities control kernel privilege.',
            'mode': 'Observed locally: empirical inspection of /proc/$$/ns, /sys/fs/cgroup, /proc/$$/status capabilities, and seccomp filters. Simulated or predicted: GKE Container-Optimized OS cgroup slice hierarchy and Cloud Run gVisor sandbox system call interception. Untested on GCP: hardware-enforced AMD SEV-ES memory encryption registers and GKE Autopilot host path admission webhook rejections.',
            'covers': "Inspect a local container's namespaces, cgroup limits and user identity; compare its isolation boundary with a VM diagram.",
            'prereq': 'Linux terminal with access to /proc and /sys filesystems.',
            'preflight': 'Verify that bash, python3, and standard filesystem utilities are operational in the local environment.',
            'verification': 'Verify that the isolation worksheet exit artifact accurately records all inspected namespace links, cgroup limits, and capability masks.',
            'trouble': 'If /sys/fs/cgroup is mounted as cgroups v1, the lab commands inspect the v1 controllers or fall back to /proc/self/cgroup hierarchy inspection.',
            'cleanup': 'Remove temporary diagnostic scripts and test outputs generated in scratch/.',
            'accept': 'An isolation worksheet distinguishing resource enforcement from security isolation is compiled into scratch/day-009-isolation-worksheet.md.',
            'file': 'day-009-exercise-b.md',
            'steps': [
                '''**Stage 1: Preflight and Environment Baseline**

**Location:** local terminal

**Actions:**
Verify core CLI utilities and establish the isolation inspection working directory.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day09_lab_b
echo "Stage 1 isolation preflight initialized at $(date -u +%Y-%m-%dT%H:%M:%SZ)" > scratch/day09_lab_b/stage1.log
cat scratch/day09_lab_b/stage1.log
```

**Expected result:** Core tools verified and initial stage log created.

**Save:** `scratch/day09_lab_b/stage1.log`''',

                '''**Stage 2: Capture Process Identity and Namespace Inode Links**

**Location:** local terminal

**Actions:**
Inspect the active shell process ID ($$), effective UID/GID, and read all namespace symbolic link inodes from `/proc/$$/ns/`.
```bash
cat <<'EOF' > scratch/day09_lab_b/inspect_namespaces.py
import os, sys

pid = os.getpid()
ns_dir = f"/proc/{pid}/ns"

print(f"Process PID: {pid} | UID: {os.getuid()} | GID: {os.getgid()}")
print("-" * 50)
if os.path.exists(ns_dir):
    for entry in sorted(os.listdir(ns_dir)):
        link_path = os.path.join(ns_dir, entry)
        try:
            target = os.readlink(link_path)
            print(f"Namespace: {entry:<10} -> Inode: {target}")
        except OSError as e:
            print(f"Namespace: {entry:<10} -> Error: {e}")
else:
    print("/proc/[pid]/ns not available")
EOF
python3 scratch/day09_lab_b/inspect_namespaces.py > scratch/day09_lab_b/namespaces.txt
cat scratch/day09_lab_b/namespaces.txt
```

**Expected result:** Output enumerates namespace entries (cgroup, ipc, mnt, net, pid, user, uts) with their respective inode identifiers.

**Save:** `scratch/day09_lab_b/namespaces.txt`''',

                '''**Stage 3: Inspect cgroups v2 Unified Controller Hierarchy**

**Location:** local terminal

**Actions:**
Inspect the process cgroup membership via `/proc/$$/cgroup` and examine available controllers in `/sys/fs/cgroup`.
```bash
cat <<'EOF' > scratch/day09_lab_b/inspect_cgroups.py
import os

with open("/proc/self/cgroup") as f:
    cgroup_info = f.read().strip()

print("Current Process Cgroup Membership:")
print(cgroup_info)
print("-" * 50)

cgroup_v2_path = "/sys/fs/cgroup"
controllers_file = os.path.join(cgroup_v2_path, "cgroup.controllers")
if os.path.exists(controllers_file):
    with open(controllers_file) as f:
        controllers = f.read().strip()
    print(f"cgroups v2 unified root detected.")
    print(f"Enabled controllers: {controllers}")
else:
    print("cgroups v1 or non-standard cgroup mount detected.")
EOF
python3 scratch/day09_lab_b/inspect_cgroups.py > scratch/day09_lab_b/cgroup_hierarchy.txt
cat scratch/day09_lab_b/cgroup_hierarchy.txt
```

**Expected result:** Output displays process cgroup slice and enabled controllers (cpu, memory, io, pids).

**Save:** `scratch/day09_lab_b/cgroup_hierarchy.txt`''',

                '''**Stage 4: Inspect Memory Limits and OOM Event Telemetry**

**Location:** local terminal

**Actions:**
Inspect memory accounting files, memory.max (or memory.limit_in_bytes), and memory.events to observe how the kernel tracks limit breaches.
```bash
cat <<'EOF' > scratch/day09_lab_b/inspect_memory_events.py
import os

cgroup_path = "/sys/fs/cgroup"
memory_max = os.path.join(cgroup_path, "memory.max")
memory_events = os.path.join(cgroup_path, "memory.events")

if os.path.exists(memory_max):
    with open(memory_max) as f:
        print(f"cgroup memory.max: {f.read().strip()}")
if os.path.exists(memory_events):
    with open(memory_events) as f:
        print("cgroup memory.events:")
        print(f.read().strip())
else:
    print("Default host cgroup root: unconstrained memory or simulated cgroup layer.")
EOF
python3 scratch/day09_lab_b/inspect_memory_events.py > scratch/day09_lab_b/memory_limits.txt
cat scratch/day09_lab_b/memory_limits.txt
```

**Expected result:** Memory constraints and event counters are recorded in `memory_limits.txt`.

**Save:** `scratch/day09_lab_b/memory_limits.txt`''',

                '''**Stage 5: Inspect Process Capabilities and Decode Effective Bits**

**Location:** local terminal

**Actions:**
Read process capabilities from `/proc/$$/status` and analyze the effective capability bitmask.
```bash
cat <<'EOF' > scratch/day09_lab_b/inspect_capabilities.py
import re

with open("/proc/self/status") as f:
    status = f.read()

cap_lines = [line for line in status.splitlines() if line.startswith("Cap")]
print("Process Capability Bitmasks:")
for line in cap_lines:
    print(f"  {line}")

print("-" * 50)
print("Architectural Analysis:")
print("  CapEff = 0000000000000000: Completely unprivileged process (zero root capabilities).")
print("  CapEff != 0: Process retains specific POSIX capabilities (e.g. CAP_NET_BIND_SERVICE).")
print("  In standard containers, CAP_SYS_ADMIN and CAP_SYS_MODULE are dropped by default.")
EOF
python3 scratch/day09_lab_b/inspect_capabilities.py > scratch/day09_lab_b/capabilities.txt
cat scratch/day09_lab_b/capabilities.txt
```

**Expected result:** Capability masks (CapInh, CapPrm, CapEff, CapBnd) are parsed and explained.

**Save:** `scratch/day09_lab_b/capabilities.txt`''',

                '''**Stage 6: Inspect Seccomp System Call Filtering Mode**

**Location:** local terminal

**Actions:**
Examine the Seccomp status line in `/proc/$$/status` to determine the active system call filtering mode.
```bash
cat <<'EOF' > scratch/day09_lab_b/inspect_seccomp.py
with open("/proc/self/status") as f:
    for line in f:
        if line.startswith("Seccomp"):
            print(f"Observed: {line.strip()}")
            mode = line.split()[1].strip()
            if mode == "0":
                print("Interpretation: Seccomp disabled (SECCOMP_MODE_DISABLED). Full syscall table accessible.")
            elif mode == "1":
                print("Interpretation: Strict mode (read, write, _exit, sigreturn only).")
            elif mode == "2":
                print("Interpretation: Filter mode (SECCOMP_MODE_FILTER). BPF filter active, gating system calls.")
EOF
python3 scratch/day09_lab_b/inspect_seccomp.py > scratch/day09_lab_b/seccomp_mode.txt
cat scratch/day09_lab_b/seccomp_mode.txt
```

**Expected result:** Seccomp mode is identified and interpreted.

**Save:** `scratch/day09_lab_b/seccomp_mode.txt`''',

                '''**Stage 7: Synthesize the Isolation Worksheet Exit Artifact**

**Location:** local terminal

**Actions:**
Synthesize all empirical findings into the required curriculum exit artifact: an isolation worksheet distinguishing resource enforcement from security isolation.
```bash
cat <<'EOF' > scratch/day09_lab_b/build_worksheet.py
import datetime

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

worksheet = f"""# Day 9 Exit Artifact: Isolation Comparison Worksheet
**Generated:** {now}
**Scope:** Distinguishing Resource Enforcement from Security Isolation in Virtual Machines and Containers.

## 1. Subsystem Classification Matrix

| Subsystem | Mechanism | Primary Function | Failure Mode / Boundary Breach | Security Boundary? |
|---|---|---|---|---|
| **Namespaces** | Kernel isolation tags (`/proc/$$/ns/`) | Visibility partitioning (PID, NET, MNT, IPC, UTS, USER) | Information disclosure / cross-namespace leak | No (Visibility only) |
| **cgroups v2** | Resource accounting (`/sys/fs/cgroup`) | Resource quota enforcement (CPU, Memory, I/O, PIDs) | Throttling or OOM kill (exit 137) | No (Resource quota only) |
| **Seccomp** | BPF system call filter (`/proc/$$/status`) | Gating allowable kernel system calls | Syscall rejected (EPERM / SIGSYS) | Yes (Restricts kernel attack surface) |
| **Capabilities** | POSIX privilege bits (`CapEff`) | Deconstructing root privileges | Operation not permitted (EPERM) | Yes (Restricts privileged operations) |
| **Virtual Machine (KVM)** | Hardware VMX/SVM & EPT MMU | Sovereign guest kernel & hardware emulation | Hypervisor escape (extremely rare) | Yes (Cryptographic & hardware enforced) |

## 2. Resource Enforcement vs Security Isolation Analysis

1. **Why Resource Enforcement is Not Security Isolation:**
   - A container with strict cgroups v2 limits (`cpu.max`, `memory.max`) cannot exhaust host memory or starve neighbor CPUs.
   - However, if the container exploits a vulnerability in the shared Linux kernel (e.g. a Dirty Pipe or io_uring privilege escalation), it gains Ring 0 execution on the host regardless of cgroup limits.
   - Therefore, cgroups enforce *resource availability*, not *security isolation*.

2. **Why Namespaces are Not Security Isolation:**
   - Namespaces restrict what a process can see (private PID numbering, private network interfaces).
   - However, system calls issued inside a namespace enter the same shared kernel space as system calls issued by the host root user.
   - Therefore, namespaces enforce *visibility boundaries*, not *privilege containment*.

3. **When to Choose Virtual Machines over Containers:**
   - Workloads requiring custom Linux kernel modules or proprietary device drivers.
   - Untrusted multi-tenant execution where hostile code could execute arbitrary system calls.
   - Compliance mandates requiring hardware-isolated cryptographic boundaries (e.g. Confidential Computing / AMD SEV).

4. **Defense-in-Depth Container Sandboxing:**
   - For container workloads requiring near-VM isolation without VM boot overhead, utilize gVisor (Cloud Run / GKE Sandbox).
   - gVisor runs an independent application kernel in userspace, preventing untrusted system calls from reaching the host Linux kernel.
"""

with open("scratch/day-009-isolation-worksheet.md", "w") as f:
    f.write(worksheet)

print("Worksheet compiled to scratch/day-009-isolation-worksheet.md")
EOF
python3 scratch/day09_lab_b/build_worksheet.py > scratch/day09_lab_b/stage7.log
cat scratch/day09_lab_b/stage7.log
```

**Expected result:** `scratch/day-009-isolation-worksheet.md` is compiled successfully.

**Save:** `scratch/day-009-isolation-worksheet.md`''',

                '''**Stage 8: Validate and Verify the Exit Artifact**

**Location:** local terminal

**Actions:**
Verify that the generated exit artifact contains all required sections, comparison matrices, and architectural justifications.
```bash
python3 -c '
with open("scratch/day-009-isolation-worksheet.md") as f:
    content = f.read()

required = [
    "Subsystem Classification Matrix",
    "Resource Enforcement vs Security Isolation Analysis",
    "Namespaces",
    "cgroups v2",
    "Seccomp",
    "Capabilities",
    "Virtual Machine (KVM)"
]

missing = [req for req in required if req not in content]
if missing:
    raise ValueError(f"Missing required sections: {missing}")

print("✓ Day 9 Exit Artifact verified: all matrices and analysis criteria satisfied.")
' > scratch/day09_lab_b/stage8.log
cat scratch/day09_lab_b/stage8.log
```

**Expected result:** Output displays `✓ Day 9 Exit Artifact verified: all matrices and analysis criteria satisfied.`

**Save:** `scratch/day09_lab_b/stage8.log`'''
            ]
        }
    }
}
