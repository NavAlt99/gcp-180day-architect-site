"""Durable data specification for Day 9: VM and container isolation."""

ACCESS_DATE = '2026-11-04'

SOURCES = {'topic-01': ('Linux Kernel KVM API General Description (accessed 2026-11-04)', 'https://docs.kernel.org/virt/kvm/api.html#general-description'), 'topic-02': ('Linux Kernel Control Group v2 — Introduction (accessed 2026-11-04)', 'https://docs.kernel.org/admin-guide/cgroup-v2.html#introduction')}

DATA = { 'access_date': '2026-11-04',
  'arch_diagram': {
      'type': 'topology',
      'title': 'Day 9: Hardware-Assisted Hypervisor and Kernel Namespace Isolation Architecture',
      'desc': 'Operational topology contrasting KVM hardware-assisted virtual machine hypervisors with shared-kernel container namespaces, cgroups v2 resource throttles, and seccomp filters.',
      'caption': 'Scope: an illustrative architecture topology for Day 9 VM and container isolation; it does not prove a deployed Google Cloud production topology or capacity.',
      'width': 1120,
      'height': 690,
      'nodes': [
          ('1. Workload Ingress & Demarcation', 'Client Ingress & Packaging Boundary'),
          ('2. Virtual Machine Sovereign Stacks', 'Type 1/KVM Hypervisor & Independent Guest Kernels'),
          ('3. Kernel Container Isolation Gates', 'Namespaces, cgroups v2, Seccomp & Capabilities'),
          ('4. Governance & Isolation Verification', 'Resource Enforcement vs Security Boundary Worksheet')
      ],
      'layers': [
          {'name': 'TIER 1 · WORKLOAD DEMAND & DEMARCATION', 'desc': 'Workload input, placement criteria, and tenant separation boundaries', 'x': 20, 'y': 55, 'w': 1080, 'h': 110, 'fill': '#12283b', 'title_color': '#7dd3fc'},
          {'name': 'TIER 2 · RUNTIME ISOLATION & KERNEL PRIVILEGE', 'desc': 'KVM hypervisor rings, sovereign guest kernels, namespaces, and cgroups v2', 'x': 20, 'y': 185, 'w': 1080, 'h': 230, 'fill': '#1b2038', 'title_color': '#c4b5fd'},
          {'name': 'TIER 3 · GOVERNANCE & SECURITY VERIFICATION', 'desc': 'Policy enforcement, seccomp syscall filters, and isolation worksheet exit evidence', 'x': 20, 'y': 435, 'w': 1080, 'h': 120, 'fill': '#2b1d2f', 'title_color': '#f9a8d4'}
      ],
      'boundaries': [
          {'label': 'LIMIT / FAILURE BOUNDARY', 'x': 430, 'y': 230, 'w': 530, 'h': 140, 'color': '#f59e0b'}
      ],
      'components': [
          {'name': 'Client / Probe Ingress', 'detail': 'Workload input & isolation criteria', 'icon': '../assets/icons/generic/client.svg', 'stroke': '#38bdf8', 'w': 190, 'h': 52, 'x': 70, 'y': 92},
          {'name': 'Hypervisor vs Container Gate', 'detail': 'KVM hardware traps & cgroups v2 quotas', 'icon': '../assets/icons/gcp/core/compute-engine.svg', 'stroke': '#f59e0b', 'w': 250, 'h': 52, 'x': 465, 'y': 92},
          {'name': 'Compute Engine VM Stack', 'detail': 'KVM hypervisor · Sovereign guest kernel', 'icon': '../assets/icons/generic/server.svg', 'stroke': '#38bdf8', 'w': 270, 'h': 64, 'x': 70, 'y': 222},
          {'name': 'Shared Host Container Stack', 'detail': 'GKE / Cloud Run · Shared host kernel', 'icon': '../assets/icons/gcp/core/gke.svg', 'stroke': '#38bdf8', 'w': 270, 'h': 64, 'x': 70, 'y': 312},
          {'name': 'Resource vs Security Gate', 'detail': 'cgroups v2 limit vs seccomp sandbox', 'icon': '../assets/icons/generic/policy.svg', 'stroke': '#f43f5e', 'w': 235, 'h': 62, 'x': 455, 'y': 252},
          {'name': 'Isolated Execution State', 'detail': 'vCPU / Namespaces verified', 'icon': '../assets/icons/generic/endpoint.svg', 'stroke': '#34d399', 'w': 220, 'h': 62, 'x': 715, 'y': 252},
          {'name': 'Architectural Isolation Policy', 'detail': 'Workload placement rules & criteria', 'icon': '../assets/icons/generic/decision.svg', 'stroke': '#38bdf8', 'w': 280, 'h': 52, 'x': 70, 'y': 472},
          {'name': 'Isolation Worksheet Exit Artifact', 'detail': 'Resource limits vs Security isolation', 'icon': '../assets/icons/generic/artifact.svg', 'stroke': '#34d399', 'w': 310, 'h': 52, 'x': 465, 'y': 472}
      ],
      'flows': [
          {'label': 'SPECIFY', 'type': 'ok', 'x1': 260, 'x2': 465, 'y1': 118, 'y2': 118},
          {'label': 'VM PATH', 'type': 'ok', 'x1': 340, 'x2': 455, 'y1': 254, 'y2': 270},
          {'label': 'CONTAINER', 'type': 'warn', 'x1': 340, 'x2': 455, 'y1': 344, 'y2': 295},
          {'label': 'ISOLATE', 'type': 'ok', 'x1': 690, 'x2': 715, 'y1': 283, 'y2': 283},
          {'label': 'VERIFY', 'type': 'ok', 'x1': 350, 'x2': 465, 'y1': 498, 'y2': 498}
      ],
      'probes': [
          {'color': '#38bdf8', 'cx': 300, 'cy': 118, 'label': 'P1: Isolation Contract Criteria'},
          {'color': '#f59e0b', 'cx': 570, 'cy': 252, 'label': 'P2: Kernel vs User Space Boundary'},
          {'color': '#34d399', 'cx': 620, 'cy': 472, 'label': 'P3: Resource Throttling vs Security Trap'}
      ]
  },
  'completion_html': '<div class="completion-box" id="completion-box-009">\n'
                     '<h3>Day 9 Acceptance Checklist</h3>\n'
                     '<ul class="checklist">\n'
                     '<li><input type="checkbox" id="check-9-1"> <label for="check-9-1">Hypervisors mastered: Type 1 '
                     'bare-metal vs Type 2 hosted, hardware-assisted virtualization (VT-x/AMD-V, EPT), and KVM/QEMU '
                     'architecture.</label></li>\n'
                     '<li><input type="checkbox" id="check-9-2"> <label for="check-9-2">Guest kernel autonomy '
                     'understood: sovereign guest OS kernel space, custom module loading (<kbd>insmod</kbd>), and '
                     'hypervisor memory overhead.</label></li>\n'
                     '<li><input type="checkbox" id="check-9-3"> <label for="check-9-3">Container isolation mechanisms '
                     'mapped: namespaces (visibility), cgroups v2 (resource quota), seccomp (system call filter), and '
                     'POSIX capabilities.</label></li>\n'
                     '<li><input type="checkbox" id="check-9-4"> <label for="check-9-4">Resource enforcement '
                     'distinguished from security: why cgroup memory/CPU limits and private namespaces do not prevent '
                     'kernel privilege escalation exploits.</label></li>\n'
                     '<li><input type="checkbox" id="check-9-5"> <label for="check-9-5">Exit evidence verified: '
                     'compiled the isolation worksheet distinguishing resource enforcement from security '
                     'isolation.</label></li>\n'
                     '</ul>\n'
                     '<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">\n'
                     '<button class="btn btn-primary" id="btn-read-009" '
                     'onclick="this.classList.toggle(\'completed\');this.textContent=this.classList.contains(\'completed\')?\'✓ '
                     'Read Day 9 Completed\':\'Mark Day 9 as Read\';">Mark Day 9 as Read</button>\n'
                     '<button class="btn btn-secondary" id="btn-artifact-009" '
                     'onclick="this.classList.toggle(\'verified\');this.textContent=this.classList.contains(\'verified\')?\'✓ '
                     'Exit Artifact Verified\':\'Verify Exit Artifact\';">Verify Exit Artifact</button>\n'
                     '</div>\n'
                     '</div>',
  'contract_version': 2,
  'day': 9,
  'exit_summary': 'A comprehensive isolation comparison worksheet distinguishing resource enforcement from security '
                  'isolation, validating that namespaces control visibility, cgroups v2 enforce quotas, and '
                  'seccomp/capabilities restrict kernel attack surfaces.',
  'part1_html': '<article class="topic-card overview" id="topic-01-overview">\n'
                '<h3>Hypervisors and virtual machines</h3>\n'
                '<p><strong class="keyword">Virtual machine isolation</strong> relies on hardware-assisted '
                'virtualization extensions where a hypervisor intercepts privileged CPU operations and virtualizes '
                'physical memory through Extended Page Tables (EPT), granting each guest operating system a completely '
                'sovereign kernel space. In contrast to containers that multiplex a single shared kernel, a virtual '
                'machine provides a hardware-enforced isolation boundary backed by '
                'independent virtual hardware registers, device emulators, and guest drivers.</p>\n'
                '<p><strong class="side-heading">Why today:</strong> Cloud architects must rigorously determine when '
                'legacy enterprise software, custom kernel drivers, or regulatory compliance mandates require the '
                'sovereign kernel boundary of a Compute Engine virtual machine rather than lightweight '
                'containerization.</p>\n'
                '<p><strong class="side-heading">Where it sits:</strong> Represents the hardware virtualization '
                'boundary in infrastructure architecture, contrasting with the OS-level container isolation analyzed '
                'in topic 2.</p>\n'
                '<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A third-party enterprise tax calculator requires a proprietary kernel '
                'module that fails to load on a shared container cluster due to dropped module insertion privileges. '
                'The team migrates the workload to a dedicated Compute Engine virtual machine running a '
                'vendor-certified guest kernel, restoring transaction processing without compromising host node '
                'security.</p>\n'
                '</article>\n'
                '\n'
                '<article class="topic-card overview" id="topic-02-overview">\n'
                '<h3>Container isolation: namespaces, cgroups, seccomp and capabilities</h3>\n'
                '<p><strong class="keyword">Linux container isolation</strong> is not a physical or hardware boundary, '
                'but an orchestration of four discrete Linux kernel subsystems: namespaces that restrict visibility, '
                'control groups (cgroups v2) that govern resource consumption, seccomp-BPF filters that restrict '
                'allowable system calls, and POSIX capabilities that fragment root privileges. Because containerized '
                'processes execute system calls directly on the shared host Linux kernel, misconfigurations in any '
                'single layer can expose the entire host node to compromise or resource starvation.</p>\n'
                '<p><strong class="side-heading">Why today:</strong> Understanding the precise mechanics of '
                'namespaces, cgroup throttling, and seccomp system call restrictions allows architects to design '
                'resilient Kubernetes workloads and diagnose silent container kills without making false assumptions '
                'about host health.</p>\n'
                '<p><strong class="side-heading">Where it sits:</strong> Follows hypervisor virtualization and '
                'directly applies Day 8 resource controls to complete the day\'s comparative isolation worksheet.</p>\n'
                '<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A fulfillment worker service intermittently crashes with exit code 137 '
                'during batch invoicing despite monitoring dashboards displaying abundant free physical memory on the '
                'host server. Inspecting the container runtime reveals that the application breached its isolated '
                'cgroup memory limit during memory-intensive PDF generation, triggering a local kernel Out-Of-Memory '
                'termination.</p>\n'
                '</article>',
  'part1_intro': 'Day 9 explores the fundamental isolation boundaries dividing compute workloads in cloud '
                 'architectures: hardware-assisted hypervisors and virtual machines versus Linux kernel container '
                 'isolation subsystems (namespaces, cgroups v2, seccomp, and POSIX capabilities).',
  'part2_intro': 'Analyze the kernel mechanics governing hardware-assisted CPU virtualization (VT-x/EPT), KVM '
                 'hypervisors, Linux namespace visibility partitioning, cgroups v2 resource accounting, seccomp BPF '
                 'filtering, and sandboxing.',
  'part3_intro': 'Real-world architectural failure cases demonstrating container module insertion denial on immutable '
                 'nodes and silent container OOM terminations occurring despite ample host physical memory headroom.',
  'part4_intro': 'Hands-on operational exercises to evaluate workload kernel dependencies, inspect live Linux process '
                 'namespaces and cgroup controllers, and compile a comprehensive isolation worksheet distinguishing '
                 'resource enforcement from security isolation.',
  'roadmap_exit': 'An isolation worksheet distinguishing resource enforcement from security isolation.',
  'roadmap_practice': "Inspect a local container's namespaces, cgroup limits and user identity; compare its isolation "
                      'boundary with a VM diagram.',
  'sources': { 'topic-01': ( 'Linux Kernel KVM API General Description (accessed 2026-11-04)',
                             'https://docs.kernel.org/virt/kvm/api.html#general-description'),
               'topic-02': ( 'Linux Kernel Control Group v2 — Introduction (accessed 2026-11-04)',
                             'https://docs.kernel.org/admin-guide/cgroup-v2.html#introduction')},
  'topics': [ { 'anchors': { 'lab': 'topic-01-lab',
                             'overview': 'topic-01-overview',
                             'problem': 'topic-01-problem',
                             'technical': 'topic-01-technical'},
                'key': 'topic-01',
                'lab': { 'accept': 'The placement evaluation log correctly categorizes kernel module dependencies as '
                                   'requiring VM guest kernel isolation.',
                         'cleanup': 'Remove temporary simulation scripts and test artifacts generated in scratch/.',
                         'covers': "Inspect a local container's namespaces, cgroup limits and user identity; compare "
                                   'its isolation boundary with a VM diagram.',
                         'expected': 'An executable placement verification demonstrating that custom kernel '
                                     'dependencies require guest kernel sovereignty, recorded in the isolation '
                                     'comparison worksheet.',
                         'file': 'day-009-exercise-a.md',
                         'goal': 'Map the architectural boundary between guest kernel autonomy in virtual machines and '
                                 'shared kernel execution in containers by testing kernel module placement and '
                                 'verifying isolation failure.',
                         'mode': 'Observed locally: local bash simulation of kernel dependency checking and placement '
                                 'verification. Simulated or predicted: Compute Engine KVM hypervisor guest kernel '
                                 'boot and module loading. Untested on GCP: live physical host hypervisor hardware '
                                 'register traps (VM-Exit) and Andromeda SDN virtio packet offloading.',
                         'name': 'Exercise A · Draw and challenge the kernel boundary',
                         'preflight': 'Verify that bash, python3, and standard POSIX shell utilities are available in '
                                      'the local environment.',
                         'prereq': 'Linux terminal environment with bash and standard core utilities.',
                         'steps': [ '**Stage 1: Preflight and Environment Baseline**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Verify that the execution environment contains the necessary CLI tools and create '
                                    'the isolated scratch workspace.\n'
                                    '```bash\n'
                                    'command -v bash\n'
                                    'command -v python3\n'
                                    'command -v cat\n'
                                    'command -v mkdir\n'
                                    'mkdir -p scratch/day09_lab_a\n'
                                    'echo "Stage 1 preflight initialized at $(date -u +%Y-%m-%dT%H:%M:%SZ)" > '
                                    'scratch/day09_lab_a/stage1.log\n'
                                    'cat scratch/day09_lab_a/stage1.log\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** Tool paths are verified and `stage1.log` contains an ISO '
                                    'timestamp.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_a/stage1.log`',
                                    '**Stage 2: Establish the Workload Fixture and Kernel Dependency**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Create a workload definition file describing two candidate services: a standard '
                                    'stateless REST API and a specialized cryptographic tax adapter requiring a '
                                    'proprietary kernel module.\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_a/workloads.json\n"
                                    '{\n'
                                    '  "workloads": [\n'
                                    '    {\n'
                                    '      "id": "order-api",\n'
                                    '      "name": "Order Management API",\n'
                                    '      "runtime": "python-fastapi",\n'
                                    '      "requires_kernel_module": false,\n'
                                    '      "requires_raw_sockets": false,\n'
                                    '      "memory_mb": 256\n'
                                    '    },\n'
                                    '    {\n'
                                    '      "id": "tax-adapter",\n'
                                    '      "name": "Cryptographic Tax Engine",\n'
                                    '      "runtime": "c-native",\n'
                                    '      "requires_kernel_module": true,\n'
                                    '      "module_name": "tax_crypto.ko",\n'
                                    '      "memory_mb": 512\n'
                                    '    }\n'
                                    '  ]\n'
                                    '}\n'
                                    'EOF\n'
                                    'python3 -m json.tool scratch/day09_lab_a/workloads.json > /dev/null && echo '
                                    '"Fixture validated" > scratch/day09_lab_a/stage2.log\n'
                                    'cat scratch/day09_lab_a/stage2.log\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** `workloads.json` is formatted properly and `stage2.log` '
                                    'confirms fixture validation.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_a/stage2.log`',
                                    '**Stage 3: Test Container Kernel Placement and Observe the Isolation Boundary**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Execute a placement evaluation engine that simulates deploying both workloads to '
                                    'a shared-kernel container runtime (e.g., standard GKE / Container-Optimized OS).\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_a/evaluate_container.py\n"
                                    'import json, sys\n'
                                    '\n'
                                    'with open("scratch/day09_lab_a/workloads.json") as f:\n'
                                    '    data = json.load(f)\n'
                                    '\n'
                                    'results = []\n'
                                    'for w in data["workloads"]:\n'
                                    '    if w["requires_kernel_module"]:\n'
                                    '        results.append({\n'
                                    '            "id": w["id"],\n'
                                    '            "target": "shared-container",\n'
                                    '            "status": "REJECTED",\n'
                                    '            "error": "EPERM: CAP_SYS_MODULE dropped by container runtime",\n'
                                    '            "reason": "Containers share host kernel; custom .ko modules cannot be '
                                    'loaded without compromising host integrity."\n'
                                    '        })\n'
                                    '    else:\n'
                                    '        results.append({\n'
                                    '            "id": w["id"],\n'
                                    '            "target": "shared-container",\n'
                                    '            "status": "ACCEPTED",\n'
                                    '            "reason": "Standard userspace runtime executes cleanly within Linux '
                                    'namespaces and cgroups."\n'
                                    '        })\n'
                                    '\n'
                                    'with open("scratch/day09_lab_a/container_placement.json", "w") as f:\n'
                                    '    json.dump(results, f, indent=2)\n'
                                    'print("Container evaluation complete")\n'
                                    'EOF\n'
                                    'python3 scratch/day09_lab_a/evaluate_container.py > '
                                    'scratch/day09_lab_a/stage3.log\n'
                                    'cat scratch/day09_lab_a/container_placement.json\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** `tax-adapter` is REJECTED with EPERM, while `order-api` is '
                                    'ACCEPTED.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_a/stage3.log`',
                                    '**Stage 4: Emulate Sovereign Virtual Machine Guest Kernel Placement**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Evaluate the placement of the rejected tax adapter into a dedicated Compute '
                                    'Engine virtual machine with a sovereign guest kernel.\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_a/evaluate_vm.py\n"
                                    'import json\n'
                                    '\n'
                                    'with open("scratch/day09_lab_a/workloads.json") as f:\n'
                                    '    data = json.load(f)\n'
                                    '\n'
                                    'vm_results = []\n'
                                    'for w in data["workloads"]:\n'
                                    '    vm_results.append({\n'
                                    '        "id": w["id"],\n'
                                    '        "target": "compute-engine-vm",\n'
                                    '        "status": "ACCEPTED",\n'
                                    '        "isolation_boundary": "Type 1 KVM / Sovereign Guest Kernel",\n'
                                    '        "module_support": "Supported: guest kernel loads module into private '
                                    'virtual Ring 0 space without host impact.",\n'
                                    '        "overhead_mb": 768\n'
                                    '    })\n'
                                    '\n'
                                    'with open("scratch/day09_lab_a/vm_placement.json", "w") as f:\n'
                                    '    json.dump(vm_results, f, indent=2)\n'
                                    'print("VM placement evaluation complete")\n'
                                    'EOF\n'
                                    'python3 scratch/day09_lab_a/evaluate_vm.py > scratch/day09_lab_a/stage4.log\n'
                                    'cat scratch/day09_lab_a/vm_placement.json\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** `tax-adapter` is ACCEPTED on the VM with sovereign guest '
                                    'kernel module support.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_a/stage4.log`',
                                    '**Stage 5: Compare Resource Overhead vs Isolation Guarantees**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Generate a quantitative comparison of memory overhead and boot latency between '
                                    'virtual machine isolation and container execution.\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_a/compare_overhead.py\n"
                                    'import json\n'
                                    '\n'
                                    'with open("scratch/day09_lab_a/workloads.json") as f:\n'
                                    '    workloads = json.load(f)["workloads"]\n'
                                    '\n'
                                    'print(f"{\'WORKLOAD\':<16} | {\'CONTAINER RAM\':<14} | {\'VM RAM (GUEST)\':<16} | '
                                    '{\'OVERHEAD FACTOR\'}")\n'
                                    'print("-" * 65)\n'
                                    'for w in workloads:\n'
                                    '    c_ram = w["memory_mb"]\n'
                                    '    vm_ram = c_ram + 768  # worksheet assumption, not a measured platform value\n'
                                    '    ratio = vm_ram / c_ram\n'
                                    '    print(f"{w[\'id\']:<16} | {c_ram:>4} MB        | {vm_ram:>4} MB          | '
                                    '{ratio:>4.1f}x")\n'
                                    'EOF\n'
                                    'python3 scratch/day09_lab_a/compare_overhead.py > scratch/day09_lab_a/stage5.log\n'
                                    'cat scratch/day09_lab_a/stage5.log\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** Output displays a side-by-side worksheet calculation using '
                                    'the explicit 768 MB guest-overhead assumption; it is not a measured platform value.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_a/stage5.log`',
                                    '**Stage 6: Challenge the Boundary with a Privileged Container Antipattern**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Simulate an insecure proposal to run the tax adapter in a privileged container '
                                    '(`--privileged` or `CAP_SYS_MODULE` added) and produce a security risk '
                                    'assessment.\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_a/security_assessment.py\n"
                                    'assessment = {\n'
                                    '    "antipattern": "Running privileged container with CAP_SYS_MODULE on shared '
                                    'GKE node",\n'
                                    '    "risks": [\n'
                                    '        "Shared Kernel Compromise: Module crashes trigger host-wide kernel panic '
                                    '(oops), taking down all collocated pods.",\n'
                                    '        "Privilege Escalation: An inserted module runs at Ring 0 with '
                                    'unrestricted access to physical memory and neighboring tenant secrets.",\n'
                                    '        "Cluster Policy Violation: Violates GKE Autopilot and standard CIS '
                                    'Kubernetes Benchmarks."\n'
                                    '    ],\n'
                                    '    "recommendation": "Maintain strict security policy: Reject privileged '
                                    'container; deploy to dedicated Compute Engine VM."\n'
                                    '}\n'
                                    'import json\n'
                                    'with open("scratch/day09_lab_a/security_risks.json", "w") as f:\n'
                                    '    json.dump(assessment, f, indent=2)\n'
                                    'print("Security risk assessment documented")\n'
                                    'EOF\n'
                                    'python3 scratch/day09_lab_a/security_assessment.py > '
                                    'scratch/day09_lab_a/stage6.log\n'
                                    'cat scratch/day09_lab_a/security_risks.json\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** Security risks of privileged containers on shared kernels '
                                    'are systematically itemized.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_a/stage6.log`',
                                    '**Stage 7: Formulate Workload Placement Policy Rules**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Codify the architectural placement rules into a deterministic decision matrix '
                                    'function.\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_a/placement_rules.py\n"
                                    'def decide_placement(workload):\n'
                                    '    if workload.get("requires_kernel_module"):\n'
                                    '        return "Compute Engine VM (Sovereign Guest Kernel Required)"\n'
                                    '    if workload.get("requires_custom_drivers"):\n'
                                    '        return "Compute Engine VM (Custom Hardware Driver Required)"\n'
                                    '    if workload.get("untrusted_multitenant_code"):\n'
                                    '        return "Cloud Run / GKE Sandbox with gVisor (Sandboxed Userspace '
                                    'Kernel)"\n'
                                    '    return "Standard GKE / Cloud Run Container (Shared Linux Kernel)"\n'
                                    '\n'
                                    'print("Decision engine rules compiled successfully")\n'
                                    'EOF\n'
                                    'python3 scratch/day09_lab_a/placement_rules.py > scratch/day09_lab_a/stage7.log\n'
                                    'cat scratch/day09_lab_a/stage7.log\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** `stage7.log` confirms that the architectural placement rules '
                                    'compiled successfully.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_a/stage7.log`',
                                    '**Stage 8: Validate the Placement Decision Evidence**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Execute the decision rules across all workload fixtures and record the final '
                                    'verification report.\n'
                                    '```bash\n'
                                    "python3 -c '\n"
                                    'import json\n'
                                    'from scratch.day09_lab_a.placement_rules import decide_placement\n'
                                    '\n'
                                    'with open("scratch/day09_lab_a/workloads.json") as f:\n'
                                    '    workloads = json.load(f)["workloads"]\n'
                                    '\n'
                                    'print("=== FINAL ARCHITECTURAL WORKLOAD PLACEMENT REPORT ===")\n'
                                    'for w in workloads:\n'
                                    '    decision = decide_placement(w)\n'
                                    '    print("Workload: {} ({}) -> Recommendation: {}".format(w["name"], w["id"], decision))\n'
                                    "' > scratch/day09_lab_a/final_report.txt\n"
                                    'cat scratch/day09_lab_a/final_report.txt\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** The final report displays accurate placement recommendations '
                                    'for both workloads.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_a/final_report.txt`'],
                         'trouble': 'If directory permissions prevent creating test fixtures, ensure commands are '
                                    'executed within the scratch/ workspace directory.',
                         'verification': 'Run the validation script to verify that the placement decision logic '
                                         'accurately flags kernel module incompatibilities on container runtimes.'},
                'overview': 'Virtual machine isolation relies on hardware-assisted virtualization extensions where a '
                            'hypervisor intercepts privileged CPU operations and virtualizes physical memory through '
                            'Extended Page Tables (EPT), granting each guest operating system a completely sovereign '
                            'kernel space. In contrast to containers that multiplex a single shared kernel, a virtual '
                            'machine provides a hardware-enforced isolation boundary '
                            'backed by independent virtual hardware registers, device emulators, and guest drivers.',
                'preview': 'A third-party enterprise tax calculator requires a proprietary kernel module that fails to '
                           'load on a shared container cluster due to dropped module insertion privileges. The team '
                           'migrates the workload to a dedicated Compute Engine virtual machine running a '
                           'vendor-certified guest kernel, restoring transaction processing without compromising host '
                           'node security.',
                'questions': [ 'How does hardware-assisted virtualization (Intel VT-x / AMD-V) eliminate '
                               'Popek-Goldberg virtualization anomalies without binary translation?',
                               'Under what circumstances does guest kernel autonomy dictate choosing a Compute Engine '
                               'VM over a Kubernetes container runtime?',
                               'What architectural threat vectors exist when userspace device emulation (QEMU/VMM) '
                               'mediates I/O between guest kernels and physical host hardware?'],
                'reference': 'https://docs.kernel.org/virt/kvm/api.html#general-description',
                'reference_label': 'Linux Kernel KVM API General Description (accessed 2026-11-04)',
                'scenario': { 'constraints': 'GKE worker nodes run an immutable, locked-down Linux kernel where '
                                             'arbitrary module loading is disabled; granting containers privileged '
                                             'security contexts violates company-wide security guardrails; the vendor '
                                             'contract mandates execution of the binary kernel module.',
                              'diagnostic_steps': [ 'Inspect container failure logs: kubectl logs '
                                                    'deployment/tax-calculator --tail=50',
                                                    'Verify dropped capabilities: grep CapEff /proc/[pid]/status and '
                                                    'decode via capsh --decode',
                                                    'Examine node kernel immutability: mount | grep /lib/modules and '
                                                    'verify ro mount flag',
                                                    'Test module loading in an isolated test environment: insmod '
                                                    'tax_crypto.ko to observe EPERM'],
                              'diagram': ( 'Tax calculation service receives synthetic checkout requests',
                                           'Shared container kernel drops CAP_SYS_MODULE blocking insmod',
                                           'Module insertion fails with EPERM causing container crashloop',
                                           'Place adapter on dedicated Compute Engine VM with sovereign guest kernel',
                                           'Vendor kernel module loads in guest; synthetic tax requests succeed'),
                              'diagram_enabled': True,
                              'evidence': 'Reviewing container startup logs reveals "insmod: ERROR: could not insert '
                                          'module tax_crypto.ko: Operation not permitted". Inspecting the process '
                                          'capabilities confirms that CAP_SYS_MODULE was dropped by the container '
                                          'runtime. The host container node kernel (/lib/modules) is mounted read-only '
                                          'and lacks matching kernel headers.\n'
                                          '\n'
                                          '<figure class="diagram-figure">\n'
                                          '<p class="diagram-scroll-hint">Swipe horizontally to view the full '
                                          'diagram.</p>\n'
                                          '<svg aria-labelledby="day9-vm-incident-title day9-vm-incident-desc" '
                                          'role="img" viewbox="0 0 940 300">\n'
                                          '<title id="day9-vm-incident-title">Tax adapter placement failure and '
                                          'corrected VM path</title>\n'
                                          '<desc id="day9-vm-incident-desc">The failed dashed path attempts to run a '
                                          'kernel module inside a shared-kernel container, failing at module '
                                          'insertion. The corrected solid path runs the adapter inside a dedicated VM '
                                          'with its own guest kernel, verified by synthetic requests and an unchanged '
                                          'host.</desc>\n'
                                          '<defs>\n'
                                          '<marker id="day9-vm-arrow" markerheight="8" markerwidth="10" orient="auto" '
                                          'refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" '
                                          'fill="#38bdf8"></path></marker>\n'
                                          '<marker id="day9-vm-fail-arrow" markerheight="8" markerwidth="10" '
                                          'orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" '
                                          'fill="#f43f5e"></path></marker>\n'
                                          '</defs>\n'
                                          '<g fill="#121526" stroke-width="2">\n'
                                          '<rect height="85" rx="8" stroke="#38bdf8" width="150" x="20" '
                                          'y="105"></rect>\n'
                                          '<image href="../assets/icons/generic/client.svg" x="28" y="113" width="22" '
                                          'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '<rect height="85" rx="8" stroke="#f43f5e" width="230" x="225" '
                                          'y="30"></rect>\n'
                                          '<image href="../assets/icons/generic/failure.svg" x="233" y="38" width="22" '
                                          'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '<rect height="85" rx="8" stroke="#34d399" width="230" x="225" '
                                          'y="180"></rect>\n'
                                          '<image href="../assets/icons/gcp/core/compute-engine.svg" x="233" y="188" '
                                          'width="22" height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '<rect height="85" rx="8" stroke="#f43f5e" width="210" x="510" '
                                          'y="30"></rect>\n'
                                          '<image href="../assets/icons/generic/failure.svg" x="518" y="38" width="22" '
                                          'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '<rect height="85" rx="8" stroke="#34d399" width="210" x="510" '
                                          'y="180"></rect>\n'
                                          '<image href="../assets/icons/generic/decision.svg" x="518" y="188" '
                                          'width="22" height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '<rect height="85" rx="8" stroke="#38bdf8" width="150" x="770" '
                                          'y="105"></rect>\n'
                                          '<image href="../assets/icons/generic/outcome.svg" x="763" y="113" '
                                          'width="22" height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '</g>\n'
                                          '<g fill="#fce7f3" font-size="12" font-weight="600" text-anchor="middle">\n'
                                          '<text x="102" y="138">Tax Request</text>\n'
                                          '<text fill="#a9b7cb" x="102" y="158">Synthetic Checkout</text>\n'
                                          '<text x="348" y="58">[FAILED PATH: Container]</text>\n'
                                          '<text fill="#f43f5e" x="348" y="78">Shares immutable host kernel</text>\n'
                                          '<text fill="#a9b7cb" x="348" y="98">No guest kernel layer</text>\n'
                                          '<text x="348" y="208">[CORRECTED: Dedicated VM]</text>\n'
                                          '<text fill="#34d399" x="348" y="228">Independent guest kernel</text>\n'
                                          '<text fill="#a9b7cb" x="348" y="248">Vendor-supported image</text>\n'
                                          '<text x="625" y="58">EXACT FAILURE POINT</text>\n'
                                          '<text fill="#f43f5e" x="625" y="78">insmod: EPERM (Denied)</text>\n'
                                          '<text fill="#a9b7cb" x="622" y="98">CAP_SYS_MODULE dropped</text>\n'
                                          '<text x="625" y="208">CORRECTED CONTROL</text>\n'
                                          '<text fill="#34d399" x="625" y="228">Module loads in guest kernel</text>\n'
                                          '<text fill="#a9b7cb" x="625" y="248">Tax calculation succeeds</text>\n'
                                          '<text x="845" y="135">VERIFICATION</text>\n'
                                          '<text fill="#34d399" font-size="11" x="845" y="155">HTTP 200 Tax Response</text>\n'
                                          '<text fill="#a9b7cb" font-size="11" x="845" y="175">Host nodes unchanged</text>\n'
                                          '</g>\n'
                                          '<g fill="none" stroke-width="2">\n'
                                          '<path d="M170 130 L220 85" marker-end="url(#day9-vm-fail-arrow)" '
                                          'stroke="#f43f5e" stroke-dasharray="7 5"></path>\n'
                                          '<path d="M455 72 L506 72" marker-end="url(#day9-vm-fail-arrow)" '
                                          'stroke="#f43f5e" stroke-dasharray="7 5"></path>\n'
                                          '<path d="M170 165 L220 210" marker-end="url(#day9-vm-arrow)" '
                                          'stroke="#38bdf8"></path>\n'
                                          '<path d="M455 222 L506 222" marker-end="url(#day9-vm-arrow)" '
                                          'stroke="#38bdf8"></path>\n'
                                          '<path d="M740 222 L751 165" marker-end="url(#day9-vm-arrow)" '
                                          'stroke="#38bdf8"></path>\n'
                                          '</g>\n'
                                          '<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" '
                                          'y="285">Dashed line (--&gt;) = failed container placement · Solid line '
                                          '(—&gt;) = corrected VM path and verification</text>\n'
                                          '</svg>\n'
                                          '<figcaption>Figure 9.3: Supplied facts: The tax calculation adapter '
                                          'requires a specialized kernel module, and container nodes run an immutable '
                                          'locked kernel. Architectural inference: Placing the workload into a '
                                          'dedicated VM with its own guest kernel resolves kernel-space dependencies '
                                          'without compromising shared container node security. Expected post-fix '
                                          'behavior: Synthetic tax requests return HTTP 200 while host nodes remain '
                                          'unmodified; this is an architectural scenario, not production '
                                          'telemetry.</figcaption>\n'
                                          '</figure>',
                              'expected': 'Expected post-fix behavior: Synthetic tax requests return HTTP 200 while '
                                          'host nodes remain unmodified; this is an architectural scenario, not '
                                          'production telemetry.',
                              'facts': 'Supplied facts: The tax calculation adapter requires a specialized kernel '
                                       'module, and container nodes run an immutable locked kernel.',
                              'icons': ( '../assets/icons/generic/client.svg',
                                         '../assets/icons/generic/failure.svg',
                                         '../assets/icons/generic/failure.svg',
                                         '../assets/icons/gcp/core/compute-engine.svg',
                                         '../assets/icons/generic/outcome.svg'),
                              'impact': 'Synthetic tax calculation calls and e-commerce checkout integration tests '
                                        'fail with HTTP 500 errors; the deployment pipeline is halted; customer order '
                                        'checkout cannot proceed without tax calculation certification.',
                              'inference': 'Architectural inference: Placing the workload into a dedicated VM with its '
                                           'own guest kernel resolves kernel-space dependencies without compromising '
                                           'shared container node security.',
                              'remediation_steps': [ 'Provision a dedicated Compute Engine instance (e2-standard-2) '
                                                     'with Debian 12 using Terraform',
                                                     'Install vendor kernel headers and build/insert tax_crypto.ko '
                                                     'into the VM guest kernel',
                                                     'Deploy the tax calculation service application onto the VM '
                                                     'systemd service manager',
                                                     'Configure internal Cloud Load Balancing to route synthetic tax '
                                                     'requests to the VM endpoint',
                                                     'Validate that synthetic tax calculation requests return HTTP 200 '
                                                     'with verified cryptographic signatures'],
                              'residual': 'The dedicated VM incurs a dedicated operating system memory overhead '
                                          'baseline (~1 GB RAM) and requires automated guest OS patching via Compute '
                                          'Engine VM Manager / OS Config.',
                              'root': 'The container architecture multiplexes a single shared host Linux kernel. '
                                      'Inserting a kernel module into a container requires modifying the shared host '
                                      'kernel space, which is blocked by dropped capabilities (CAP_SYS_MODULE) and '
                                      'node immutability. Containers do not possess an independent guest kernel.',
                              'scenario': 'A legacy enterprise tax calculation service requires a proprietary '
                                          'third-party Linux kernel module to execute hardware-accelerated '
                                          'cryptographic valuation routines. When deployed onto an existing Kubernetes '
                                          'container cluster running Container-Optimized OS, the application container '
                                          'crashloops immediately upon startup, reporting permission denied during '
                                          'module insertion.',
                              'verify': 'The tax calculation adapter is relocated to a dedicated Compute Engine '
                                        'virtual machine running Debian with a sovereign guest kernel. The vendor '
                                        'kernel module loads successfully into the guest kernel; synthetic checkout '
                                        'requests return HTTP 200 with accurate tax calculations; the shared '
                                        'Kubernetes container nodes remain completely uncompromised and unmodified.'},
                'technical': '<p><strong class="side-heading">Subtopics in this discussion:</strong></p>\n'
                             '<ol>\n'
                             '<li>Type 1 (Bare-Metal) vs Type 2 (Hosted) Hypervisors</li>\n'
                             '<li>Hardware-Assisted Virtualization (Intel VT-x / AMD-V, EPT, and vCPUs)</li>\n'
                             '<li>The Linux KVM Subsystem and QEMU Userspace Model</li>\n'
                             '<li>Compute Engine Hypervisor Architecture and Shielded VM Security</li>\n'
                             '<li>Guest Kernel Autonomy vs Hypervisor Management Overhead</li>\n'
                             '</ol>\n'
                             '\n'
                             '<h4>Type 1 (Bare-Metal) vs Type 2 (Hosted) Hypervisors</h4>\n'
                             '<p><strong class="side-heading">What it is in general:</strong> A <strong '
                             'class="keyword">hypervisor</strong> (or Virtual Machine Monitor, VMM) is the software, '
                             'firmware, or hardware virtualization layer that manages the execution of multiple '
                             'independent virtual machines on a single physical host. Hypervisors fall into two '
                             'fundamental architectural categories: Type 1 (bare-metal) hypervisors run directly on '
                             'the underlying server hardware with no intermediate host operating system, providing '
                             'high throughput, predictable latency, and minimal virtualization overhead. In contrast, '
                             'Type 2 (hosted) hypervisors run as an application process inside a host operating system '
                             '(such as VirtualBox or VMware Workstation), relying on the host OS kernel for hardware '
                             'management, device drivers, and CPU scheduling. The Linux Kernel-based Virtual Machine '
                             '(KVM) blurs this traditional boundary by turning the Linux kernel itself into a '
                             'bare-metal Type 1 hypervisor via a loadable kernel module (<kbd>kvm.ko</kbd>), combining '
                             'native hardware scheduling with complete operating system capabilities.</p>\n'
                             '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Enterprise '
                             'cloud infrastructure is built entirely upon Type 1 bare-metal virtualization '
                             'architectures. Type 1 hypervisors eliminate host operating system context switching '
                             'overhead, provide direct memory management without double page caching, and ensure '
                             'strict noisy-neighbor isolation across multi-tenant physical hardware. Choosing '
                             'virtualized architectures allows architects to run heterogeneous guest operating systems '
                             '(Linux, Windows Server, BSD), enforce strict CPU pinning, and guarantee '
                             'hardware-enforced cryptographic separation between hostile tenants sharing the same '
                             'physical chassis.</p>\n'
                             '<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud Compute Engine '
                             'utilizes a heavily hardened, optimized version of the open-source KVM hypervisor '
                             'deployed directly onto bare-metal fleet servers. In GCP, every Compute Engine instance '
                             'is an isolated KVM guest whose virtual hardware devices (virtio network interfaces, '
                             "persistent disk controllers) are emulated with near-zero latency by Google's custom "
                             'userspace management layer. By relying on KVM as a Type 1 hypervisor, GCP provides live '
                             'migration capabilities, allowing Google to perform host kernel updates and hardware '
                             'maintenance without terminating or restarting customer virtual machines.</p>\n'
                             '\n'
                             '<h4>Hardware-Assisted Virtualization (Intel VT-x / AMD-V, EPT, and vCPUs)</h4>\n'
                             '<p><strong class="side-heading">What it is in general:</strong> Early x86 virtualization '
                             'required complex, slow binary translation because 17 sensitive x86 instructions (the '
                             'famous Popek-Goldberg virtualization requirements) failed silently when executed in '
                             'unprivileged CPU rings. Modern servers solve this through <strong '
                             'class="keyword">hardware-assisted virtualization</strong> (Intel VT-x / AMD-V), which '
                             'introduces a dedicated CPU operating mode: VMX Root Operation (where the hypervisor '
                             'executes) and VMX Non-Root Operation (where the guest operating system and its '
                             'applications execute). Hardware registers known as the Virtual Machine Control Structure '
                             '(VMCS on Intel) or Virtual Machine Control Block (VMCB on AMD) record guest and host CPU '
                             'states. When the guest attempts a privileged operation (such as modifying control '
                             'registers or executing I/O instructions), the CPU hardware triggers a <strong '
                             'class="keyword">VM-Exit</strong>, suspending guest execution and transferring control '
                             'back to the hypervisor in Root mode. Memory virtualization is accelerated by hardware '
                             'page table translation: Intel Extended Page Tables (EPT) or AMD Nested Page Tables (NPT) '
                             'maintain two-dimensional translation tables, mapping Guest Virtual Addresses (GVA) to '
                             'Guest Physical Addresses (GPA), and GPA to Host Physical Addresses (HPA) directly in the '
                             'hardware Memory Management Unit (MMU) TLB cache.</p>\n'
                             '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Virtual CPUs '
                             '(<strong class="keyword">vCPUs</strong>) are not physical processor chips; they are '
                             'standard operating system execution threads scheduled by the hypervisor onto physical '
                             'CPU cores or hardware hyperthreads (Simultaneous Multithreading, SMT). Because every '
                             'VM-Exit incurs hundreds of CPU clock cycles in register state saving, architects must '
                             'optimize guest workloads to minimize unnecessary VM-Exits. Understanding EPT two-tier '
                             'translation explains why memory access latency is marginally higher in VMs than bare '
                             'metal, and why huge pages (Transparent Huge Pages / 2 MB pages) provide substantial '
                             'performance gains for memory-intensive databases by reducing EPT translation table '
                             'walks.</p>\n'
                             '<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine instance '
                             'machine types expose vCPUs that map directly to physical hardware hyperthreads on Intel '
                             'Xeon, AMD EPYC, or ARM Ampere Altra processors. For example, a <kbd>c2-standard-4</kbd> '
                             'instance provides 4 vCPUs, which correspond to 2 physical CPU cores with 2 hyperthreads '
                             "each on Intel Cascade Lake. GCP's virtualization infrastructure supports nested "
                             'virtualization, allowing architects to enable VMX flags inside a Compute Engine VM to '
                             'run KVM or Android emulators inside the cloud instance for dev/test workflows.</p>\n'
                             '\n'
                             '<h4>The Linux KVM Subsystem and QEMU Userspace Model</h4>\n'
                             '<p><strong class="side-heading">What it is in general:</strong> The <strong '
                             'class="keyword">Linux Kernel-based Virtual Machine (KVM)</strong> subsystem exposes the '
                             'hardware virtualization extensions of the host CPU to userspace via the character device '
                             'node <kbd>/dev/kvm</kbd>. KVM provides the core kernel module (<kbd>kvm.ko</kbd>) and '
                             'CPU-specific architecture modules (<kbd>kvm-intel.ko</kbd> or <kbd>kvm-amd.ko</kbd>). '
                             'However, KVM alone does not emulate peripheral hardware devices such as PCI buses, disk '
                             'controllers, serial ports, or network adapters. That device emulation is supplied by a '
                             'userspace program, historically <strong class="keyword">QEMU</strong> (Quick Emulator). '
                             'In the KVM/QEMU architecture, each virtual machine is simply a standard Linux userspace '
                             'process on the host. Each vCPU inside the guest is an ordinary POSIX thread within that '
                             'process. The userspace process calls the <kbd>ioctl()</kbd> system call on the '
                             '<kbd>/dev/kvm</kbd> file descriptor using commands like <kbd>KVM_CREATE_VM</kbd>, '
                             '<kbd>KVM_CREATE_VCPU</kbd>, and enters guest execution via <kbd>KVM_RUN</kbd>. When a '
                             'guest performs I/O, the hardware triggers a VM-Exit, KVM pauses the thread, returns from '
                             'the <kbd>KVM_RUN</kbd> ioctl into userspace QEMU, QEMU emulates the device transfer, and '
                             're-executes <kbd>KVM_RUN</kbd>.</p>\n'
                             '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Because a VM in '
                             'a KVM architecture is an ordinary Linux process on the host, host-level security '
                             'controls, resource policies, and monitoring mechanisms apply directly to the VM process. '
                             'If the userspace emulator has a vulnerability in its virtual device emulation code, an '
                             'attacker inside the guest VM could theoretically escape into the host userspace emulator '
                             'process. Recognizing this distinction empowers architects to enforce defense-in-depth: '
                             'virtual machines provide strong isolation at the CPU execution level, but emulator '
                             'hardening and paravirtualized drivers (<kbd>virtio</kbd>) are essential to minimize '
                             'emulator attack surfaces and maximize I/O throughput.</p>\n'
                             '<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud\'s hypervisor '
                             'architecture replaces traditional open-source QEMU with a bespoke, memory-safe, heavily '
                             'restricted virtual machine monitor written by Google. This custom userspace VMM '
                             'communicates with the Linux KVM kernel driver via <kbd>/dev/kvm</kbd> but strips out '
                             'thousands of obsolete legacy emulated hardware devices (such as IDE floppy drives and '
                             'Sound Blaster cards), eliminating broad classes of hypervisor escape vulnerabilities. '
                             'Furthermore, GCP uses paravirtualized virtio-net and virtio-scsi device drivers to '
                             "provide near-native network and disk throughput directly through Google's Andromeda SDN "
                             'and Colossus storage backends.</p>\n'
                             '\n'
                             '<h4>Compute Engine Hypervisor Architecture and Shielded VM Security</h4>\n'
                             '<p><strong class="side-heading">What it is in general:</strong> Cloud hypervisors must '
                             'defend against both horizontal tenant-to-tenant attacks and vertical guest-to-host '
                             'hypervisor escapes. <strong class="keyword">Shielded VMs</strong> in Google Cloud '
                             'augment KVM virtualization with verifiable cryptographic hardware primitives, '
                             'specifically Unified Extensible Firmware Interface (UEFI) Secure Boot, Virtual Trusted '
                             'Platform Module (vTPM 2.0), and Integrity Monitoring. UEFI Secure Boot cryptographically '
                             'validates the digital signatures of the bootloader, guest kernel, and kernel modules '
                             'before execution begins, preventing rootkits or unauthorized boot code from loading. The '
                             'vTPM maintains an immutable cryptographic audit log of the entire boot sequence '
                             '(measured boot), storing cryptographic hashes in Platform Configuration Registers '
                             '(PCRs). Integrity Monitoring compares these measured boot values against an established '
                             'baseline, alerting administrators via Cloud Logging and Security Command Center if '
                             'unauthorized kernel tampering occurs.</p>\n'
                             '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Shielded VM '
                             'capabilities ensure that an enterprise workload boots only verified, authentic operating '
                             'system binaries. For regulated industries (financial services, healthcare, defense), '
                             'Shielded VM provides cryptographically provable evidence that guest operating system '
                             'kernels have not been tampered with or replaced. Architects can bind sensitive '
                             'encryption keys (such as disk decryption keys or TLS private keys) to vTPM PCRs, '
                             'ensuring that secrets are unsealed only when the virtual machine boots in an authentic, '
                             'untampered kernel state.</p>\n'
                             '<p><strong class="side-heading">Relevance to GCP:</strong> Shielded VM is enabled by '
                             'default on all modern Compute Engine instances in GCP. GCP also provides Confidential '
                             'VMs, which leverage AMD Secure Encrypted Virtualization (SEV) or Intel Trust Domain '
                             "Extensions (TDX) to encrypt the virtual machine's RAM in hardware using ephemeral "
                             "cryptographic keys generated and held entirely by the processor's secure enclave. Even a "
                             'rogue administrator or compromised hypervisor host operating system cannot inspect the '
                             "plaintext contents of a Confidential VM's memory.</p>\n"
                             '\n'
                             '<h4>Guest Kernel Autonomy vs Hypervisor Management Overhead</h4>\n'
                             '<p><strong class="side-heading">What it is in general:</strong> The defining '
                             'architectural property of a virtual machine is <strong class="keyword">guest kernel '
                             'autonomy</strong>: the VM boots its own dedicated, sovereign operating system kernel. '
                             'The guest kernel maintains its own virtual memory page tables, process scheduler, '
                             'network stack, filesystem drivers, and security subsystem. Because the guest kernel has '
                             'full sovereignty inside its virtual hardware partition, it can load specialized vendor '
                             'kernel modules (<kbd>.ko</kbd> files), modify internal kernel parameters via '
                             '<kbd>/proc/sys/</kbd> (sysctl), and configure custom networking protocols (such as SCTP '
                             'or raw packet sockets) without needing permission from or affecting any other tenant on '
                             'the physical host. However, this sovereignty comes at the cost of <strong '
                             'class="keyword">hypervisor overhead</strong>: each VM requires memory allocation for its '
                             'full operating system kernel (typically 300 MB to 1 GB of RAM just for the OS baseline), '
                             'takes seconds to minutes to boot, and incurs CPU cycles for two-level page table walking '
                             '(EPT) and VM-Exit trap handling.</p>\n'
                             '<p><strong class="side-heading">Relevance to a cloud architect:</strong> When evaluating '
                             'workload placement, architects must balance the overhead of guest kernel autonomy '
                             'against the isolation guarantees it provides. Applications requiring legacy commercial '
                             'software with proprietary kernel-space licensing daemons, custom network drivers, or '
                             'specialized filesystem drivers cannot run on container platforms like Cloud Run or '
                             'standard GKE. Conversely, running hundreds of microservices as separate full VMs '
                             'introduces massive memory wastage and operational management overhead, making '
                             'containerization or container sandboxing (gVisor) the superior architectural choice for '
                             'horizontally scalable web services.</p>\n'
                             '<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine provides '
                             'complete guest kernel autonomy across custom operating system images, Debian, Ubuntu, '
                             'Red Hat Enterprise Linux, SUSE, and Windows Server. If an enterprise requires custom '
                             'kernel patches (e.g., real-time kernel extensions or proprietary ERP database patches), '
                             'Compute Engine VMs provide the exact execution venue. Conversely, for container '
                             'workloads that require near-VM isolation without the boot latency of full VMs, Google '
                             'Cloud provides Cloud Run and GKE Sandbox powered by gVisor, which implements a userspace '
                             'kernel to intercept system calls.</p>\n'
                             '\n'
                             '<figure class="diagram-figure">\n'
                             '<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>\n'
                             '<svg aria-labelledby="day9-boundary-title day9-boundary-desc" role="img" viewbox="0 0 '
                             '940 390">\n'
                             '<title id="day9-boundary-title">Virtual machine and container isolation '
                             'boundaries</title>\n'
                             '<desc id="day9-boundary-desc">Two parallel stacks compare a virtual machine with its own '
                             'guest kernel against two containers that share one host kernel. Outlines mark isolation '
                             'scopes.</desc>\n'
                             '<defs>\n'
                             '<marker id="day9-boundary-arrow" markerheight="8" markerwidth="10" orient="auto" '
                             'refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>\n'
                             '</defs>\n'
                             '<g fill="#121526" stroke-width="2">\n'
                             '<rect height="315" rx="12" stroke="#f43f5e" stroke-dasharray="8 5" width="430" x="20" '
                             'y="35"></rect>\n'
                             '<rect height="315" rx="12" stroke="#38bdf8" stroke-dasharray="8 5" width="430" x="490" '
                             'y="35"></rect>\n'
                             '<rect height="60" rx="8" stroke="#38bdf8" width="360" x="55" y="70"></rect>\n'
                             '<image href="../assets/icons/generic/client.svg" x="65" y="86" width="28" height="28" '
                             'preserveAspectRatio="xMidYMid meet"/>\n'
                             '<rect height="60" rx="8" stroke="#f97316" width="360" x="55" y="155"></rect>\n'
                             '<image href="../assets/icons/generic/server.svg" x="65" y="171" width="28" height="28" '
                             'preserveAspectRatio="xMidYMid meet"/>\n'
                             '<rect height="60" rx="8" stroke="#34d399" width="360" x="55" y="240"></rect>\n'
                             '<image href="../assets/icons/gcp/core/compute-engine.svg" x="65" y="256" width="28" '
                             'height="28" preserveAspectRatio="xMidYMid meet"/>\n'
                             '<rect height="60" rx="8" stroke="#38bdf8" width="165" x="525" y="70"></rect>\n'
                             '<image href="../assets/icons/generic/client.svg" x="535" y="86" width="28" height="28" '
                             'preserveAspectRatio="xMidYMid meet"/>\n'
                             '<rect height="60" rx="8" stroke="#38bdf8" width="165" x="720" y="70"></rect>\n'
                             '<image href="../assets/icons/generic/endpoint.svg" x="730" y="86" width="28" height="28" '
                             'preserveAspectRatio="xMidYMid meet"/>\n'
                             '<rect height="60" rx="8" stroke="#f97316" width="360" x="525" y="155"></rect>\n'
                             '<image href="../assets/icons/generic/server.svg" x="535" y="171" width="28" height="28" '
                             'preserveAspectRatio="xMidYMid meet"/>\n'
                             '<rect height="60" rx="8" stroke="#34d399" width="360" x="525" y="240"></rect>\n'
                             '<image href="../assets/icons/generic/storage.svg" x="535" y="256" width="28" height="28" '
                             'preserveAspectRatio="xMidYMid meet"/>\n'
                             '</g>\n'
                             '<g fill="#fce7f3" font-size="13" font-weight="600" text-anchor="middle">\n'
                             '<text x="245" y="58">VIRTUAL MACHINE BOUNDARY</text>\n'
                             '<text x="245" y="97">Order API process + userspace</text>\n'
                             '<text x="245" y="182">Independent Guest Kernel</text>\n'
                             '<text fill="#a9b7cb" font-size="11" x="245" y="199">guest loads own kernel modules &amp; '
                             'drivers</text>\n'
                             '<text x="245" y="267">Virtual Hardware &amp; Hypervisor</text>\n'
                             '<text fill="#a9b7cb" font-size="11" x="245" y="284">EPT memory translation &amp; vCPU '
                             'scheduling</text>\n'
                             '<text x="705" y="58">CONTAINER PROCESS BOUNDARIES</text>\n'
                             '<text x="617" y="97">Order API</text>\n'
                             '<text x="812" y="97">Worker</text>\n'
                             '<text x="705" y="182">Shared Host Linux Kernel</text>\n'
                             '<text fill="#a9b7cb" font-size="11" x="705" y="199">namespaces · cgroups v2 · seccomp · '
                             'capabilities</text>\n'
                             '<text x="705" y="267">Physical Server Hardware</text>\n'
                             '<text fill="#a9b7cb" font-size="11" x="705" y="284">bare metal CPU, RAM, storage, '
                             'network</text>\n'
                             '</g>\n'
                             '<g fill="none" marker-end="url(#day9-boundary-arrow)" stroke="#38bdf8" '
                             'stroke-width="2">\n'
                             '<path d="M235 130 L235 151"></path>\n'
                             '<path d="M235 215 L235 236"></path>\n'
                             '<path d="M607 130 L650 151"></path>\n'
                             '<path d="M802 130 L760 151"></path>\n'
                             '<path d="M705 215 L705 236"></path>\n'
                             '</g>\n'
                             '</svg>\n'
                             '<figcaption>Figure 9.1: Architectural comparison of virtualization versus '
                             'containerization boundaries. A VM encapsulates an independent guest operating system '
                             'kernel over hypervisor-managed virtual hardware, whereas containers partition host '
                             'kernel visibility and resources across processes executing directly on the shared host '
                             'kernel.</figcaption>\n'
                             '</figure>\n'
                             '\n'
                             '<div class="topic-card">\n'
                             '<table>\n'
                             '<caption>Table 9.1: Architectural Isolation Comparison: Virtual Machines vs Linux '
                             'Containers</caption>\n'
                             '<thead>\n'
                             '<tr>\n'
                             '<th>Architectural Property</th>\n'
                             '<th>Virtual Machine (Type 1 KVM)</th>\n'
                             '<th>Linux Container (Docker / Containerd)</th>\n'
                             '</tr>\n'
                             '</thead>\n'
                             '<tbody>\n'
                             '<tr>\n'
                             '<td><strong>Kernel Isolation</strong></td>\n'
                             '<td>Independent, sovereign guest kernel per VM</td>\n'
                             '<td>Shared host Linux kernel across all containers</td>\n'
                             '</tr>\n'
                             '<tr>\n'
                             '<td><strong>Hardware Emulation</strong></td>\n'
                             '<td>Hardware-assisted vCPUs, EPT MMU, emulated PCI/virtio devices</td>\n'
                             '<td>No hardware emulation; processes execute directly on host CPU</td>\n'
                             '</tr>\n'
                             '<tr>\n'
                             '<td><strong>Security Boundary</strong></td>\n'
                             '<td>Hardware-enforced CPU Ring 0 separation via VMX/SVM &amp; hypervisor</td>\n'
                             '<td>Kernel-space software enforcement (namespaces, cgroups, seccomp)</td>\n'
                             '</tr>\n'
                             '<tr>\n'
                             '<td><strong>Boot Latency &amp; Memory</strong></td>\n'
                             '<td>Seconds to minutes boot time; 500 MB–1 GB baseline memory overhead</td>\n'
                             '<td>Milliseconds boot time; negligible baseline overhead (megabytes)</td>\n'
                             '</tr>\n'
                             '<tr>\n'
                             '<td><strong>Kernel Module Capability</strong></td>\n'
                             '<td>Full support: guest can insert custom kernel modules (<kbd>insmod</kbd>)</td>\n'
                             '<td>Blocked: shared kernel rejects container module insertions (<kbd>EPERM</kbd>)</td>\n'
                             '</tr>\n'
                             '<tr>\n'
                             '<td><strong>GCP Implementation</strong></td>\n'
                             '<td>Compute Engine, Bare Metal Solution, Confidential VMs</td>\n'
                             '<td>Google Kubernetes Engine (GKE), Cloud Run, Artifact Registry</td>\n'
                             '</tr>\n'
                             '</tbody>\n'
                             '</table>\n'
                             '</div>\n'
                             '\n'
                             '<p><strong class="side-heading">Concrete example:</strong> Consider an enterprise '
                             'payment gateway that integrates a legacy hardware security module (HSM) vendor library '
                             'requiring a proprietary Linux character device kernel module named '
                             '<kbd>hsm_crypto.ko</kbd>. When deployed inside a standard Docker container on a shared '
                             'Kubernetes node, the container initialization script executes <kbd>insmod '
                             'hsm_crypto.ko</kbd> and immediately aborts with <kbd>Operation not permitted</kbd> '
                             'because the container runtime drops <kbd>CAP_SYS_MODULE</kbd> to protect the shared host '
                             'kernel. Granting the container <kbd>--privileged</kbd> would permit the module to load '
                             'directly into the shared host kernel, compromising every other tenant on the node and '
                             'violating enterprise security policies. The architect correctly migrates the payment '
                             'gateway to a dedicated Compute Engine VM running Debian with a sovereign guest kernel. '
                             'The guest kernel loads <kbd>hsm_crypto.ko</kbd> into its own virtualized Ring 0 space '
                             'without requiring modification of the shared host kernel, satisfying the fixture requirements while '
                             'preserving strict cryptographic boundary separation.</p>\n'
                             '\n'
                             '<p><strong class="side-heading">Evidence limit:</strong> Observing successful execution '
                             'of a custom kernel module inside a virtual machine proves guest kernel sovereignty '
                             'within that specific virtual hardware boundary; it does not prove that the underlying '
                             'physical hypervisor or neighboring virtual machines are immune to side-channel CPU '
                             'timing attacks (such as Spectre or Meltdown) without hypervisor-level microcode '
                             'mitigations, L1TF cache flushes, and core scheduling enabled by the cloud '
                             'provider.</p>\n',
                'title': 'Hypervisors and virtual machines'},
              { 'anchors': { 'lab': 'topic-02-lab',
                             'overview': 'topic-02-overview',
                             'problem': 'topic-02-problem',
                             'technical': 'topic-02-technical'},
                'key': 'topic-02',
                'lab': { 'accept': 'An isolation worksheet distinguishing resource enforcement from security isolation '
                                   'is compiled into scratch/day-009-isolation-worksheet.md.',
                         'cleanup': 'Remove temporary diagnostic scripts and test outputs generated in scratch/.',
                         'covers': "Inspect a local container's namespaces, cgroup limits and user identity; compare "
                                   'its isolation boundary with a VM diagram.',
                         'expected': 'An isolation worksheet distinguishing resource enforcement from security '
                                     'isolation, verifying that namespaces control visibility, cgroups control '
                                     'resource limits, and seccomp/capabilities control kernel privilege.',
                         'file': 'day-009-exercise-b.md',
                         'goal': 'Empirically inspect the active Linux kernel container isolation subsystems directly: '
                                 'inspect namespace inodes under /proc/[pid]/ns/, examine cgroups v2 controller '
                                 'hierarchy and memory accounting, decode POSIX capabilities, and verify seccomp '
                                 'filtering status.',
                         'mode': 'Observed locally: empirical inspection of /proc/$$/ns, /sys/fs/cgroup, '
                                 '/proc/$$/status capabilities, and seccomp filters. Simulated or predicted: GKE '
                                 'Container-Optimized OS cgroup slice hierarchy and Cloud Run gVisor sandbox system '
                                 'call interception. Untested on GCP: hardware-enforced AMD SEV-ES memory encryption '
                                 'registers and GKE Autopilot host path admission webhook rejections.',
                         'name': 'Exercise B · Read your process isolation facts',
                         'preflight': 'Verify that bash, python3, and standard filesystem utilities are operational in '
                                      'the local environment.',
                         'prereq': 'Linux terminal with access to /proc and /sys filesystems.',
                         'steps': [ '**Stage 1: Preflight and Environment Baseline**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Verify core CLI utilities and establish the isolation inspection working '
                                    'directory.\n'
                                    '```bash\n'
                                    'command -v bash\n'
                                    'command -v python3\n'
                                    'command -v cat\n'
                                    'command -v mkdir\n'
                                    'mkdir -p scratch/day09_lab_b\n'
                                    'echo "Stage 1 isolation preflight initialized at $(date -u +%Y-%m-%dT%H:%M:%SZ)" '
                                    '> scratch/day09_lab_b/stage1.log\n'
                                    'cat scratch/day09_lab_b/stage1.log\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** Core tools verified and initial stage log created.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_b/stage1.log`',
                                    '**Stage 2: Capture Process Identity and Namespace Inode Links**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Inspect the active shell process ID ($$), effective UID/GID, and read all '
                                    'namespace symbolic link inodes from `/proc/$$/ns/`.\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_b/inspect_namespaces.py\n"
                                    'import os, sys\n'
                                    '\n'
                                    'pid = os.getpid()\n'
                                    'ns_dir = f"/proc/{pid}/ns"\n'
                                    '\n'
                                    'print(f"Process PID: {pid} | UID: {os.getuid()} | GID: {os.getgid()}")\n'
                                    'print("-" * 50)\n'
                                    'if os.path.exists(ns_dir):\n'
                                    '    for entry in sorted(os.listdir(ns_dir)):\n'
                                    '        link_path = os.path.join(ns_dir, entry)\n'
                                    '        try:\n'
                                    '            target = os.readlink(link_path)\n'
                                    '            print(f"Namespace: {entry:<10} -> Inode: {target}")\n'
                                    '        except OSError as e:\n'
                                    '            print(f"Namespace: {entry:<10} -> Error: {e}")\n'
                                    'else:\n'
                                    '    print("/proc/[pid]/ns not available")\n'
                                    'EOF\n'
                                    'python3 scratch/day09_lab_b/inspect_namespaces.py > '
                                    'scratch/day09_lab_b/namespaces.txt\n'
                                    'cat scratch/day09_lab_b/namespaces.txt\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** Output enumerates namespace entries (cgroup, ipc, mnt, net, '
                                    'pid, user, uts) with their respective inode identifiers.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_b/namespaces.txt`',
                                    '**Stage 3: Inspect cgroups v2 Unified Controller Hierarchy**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Inspect the process cgroup membership via `/proc/$$/cgroup` and examine available '
                                    'controllers in `/sys/fs/cgroup`.\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_b/inspect_cgroups.py\n"
                                    'import os\n'
                                    '\n'
                                    'with open("/proc/self/cgroup") as f:\n'
                                    '    cgroup_info = f.read().strip()\n'
                                    '\n'
                                    'print("Current Process Cgroup Membership:")\n'
                                    'print(cgroup_info)\n'
                                    'print("-" * 50)\n'
                                    '\n'
                                    'cgroup_v2_path = "/sys/fs/cgroup"\n'
                                    'controllers_file = os.path.join(cgroup_v2_path, "cgroup.controllers")\n'
                                    'if os.path.exists(controllers_file):\n'
                                    '    with open(controllers_file) as f:\n'
                                    '        controllers = f.read().strip()\n'
                                    '    print(f"cgroups v2 unified root detected.")\n'
                                    '    print(f"Enabled controllers: {controllers}")\n'
                                    'else:\n'
                                    '    print("cgroups v1 or non-standard cgroup mount detected.")\n'
                                    'EOF\n'
                                    'python3 scratch/day09_lab_b/inspect_cgroups.py > '
                                    'scratch/day09_lab_b/cgroup_hierarchy.txt\n'
                                    'cat scratch/day09_lab_b/cgroup_hierarchy.txt\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** Output displays process cgroup slice and enabled controllers '
                                    '(cpu, memory, io, pids).\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_b/cgroup_hierarchy.txt`',
                                    '**Stage 4: Inspect Memory Limits and OOM Event Telemetry**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Inspect memory accounting files, memory.max (or memory.limit_in_bytes), and '
                                    'memory.events to observe how the kernel tracks limit breaches.\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_b/inspect_memory_events.py\n"
                                    'import os\n'
                                    '\n'
                                    'cgroup_path = "/sys/fs/cgroup"\n'
                                    'memory_max = os.path.join(cgroup_path, "memory.max")\n'
                                    'memory_events = os.path.join(cgroup_path, "memory.events")\n'
                                    '\n'
                                    'if os.path.exists(memory_max):\n'
                                    '    with open(memory_max) as f:\n'
                                    '        print(f"cgroup memory.max: {f.read().strip()}")\n'
                                    'if os.path.exists(memory_events):\n'
                                    '    with open(memory_events) as f:\n'
                                    '        print("cgroup memory.events:")\n'
                                    '        print(f.read().strip())\n'
                                    'else:\n'
                                    '    print("Default host cgroup root: unconstrained memory or simulated cgroup '
                                    'layer.")\n'
                                    'EOF\n'
                                    'python3 scratch/day09_lab_b/inspect_memory_events.py > '
                                    'scratch/day09_lab_b/memory_limits.txt\n'
                                    'cat scratch/day09_lab_b/memory_limits.txt\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** Memory constraints and event counters are recorded in '
                                    '`memory_limits.txt`.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_b/memory_limits.txt`',
                                    '**Stage 5: Inspect Process Capabilities and Decode Effective Bits**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Read process capabilities from `/proc/$$/status` and analyze the effective '
                                    'capability bitmask.\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_b/inspect_capabilities.py\n"
                                    'import re\n'
                                    '\n'
                                    'with open("/proc/self/status") as f:\n'
                                    '    status = f.read()\n'
                                    '\n'
                                    'cap_lines = [line for line in status.splitlines() if line.startswith("Cap")]\n'
                                    'print("Process Capability Bitmasks:")\n'
                                    'for line in cap_lines:\n'
                                    '    print(f"  {line}")\n'
                                    '\n'
                                    'print("-" * 50)\n'
                                    'print("Architectural Analysis:")\n'
                                    'print("  CapEff = 0000000000000000: Completely unprivileged process (zero root '
                                    'capabilities).")\n'
                                    'print("  CapEff != 0: Process retains specific POSIX capabilities (e.g. '
                                    'CAP_NET_BIND_SERVICE).")\n'
                                    'print("  In standard containers, CAP_SYS_ADMIN and CAP_SYS_MODULE are dropped by '
                                    'default.")\n'
                                    'EOF\n'
                                    'python3 scratch/day09_lab_b/inspect_capabilities.py > '
                                    'scratch/day09_lab_b/capabilities.txt\n'
                                    'cat scratch/day09_lab_b/capabilities.txt\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** Capability masks (CapInh, CapPrm, CapEff, CapBnd) are parsed '
                                    'and explained.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_b/capabilities.txt`',
                                    '**Stage 6: Inspect Seccomp System Call Filtering Mode**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Examine the Seccomp status line in `/proc/$$/status` to determine the active '
                                    'system call filtering mode.\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_b/inspect_seccomp.py\n"
                                    'with open("/proc/self/status") as f:\n'
                                    '    for line in f:\n'
                                    '        if line.startswith("Seccomp"):\n'
                                    '            print(f"Observed: {line.strip()}")\n'
                                    '            mode = line.split()[1].strip()\n'
                                    '            if mode == "0":\n'
                                    '                print("Interpretation: Seccomp disabled (SECCOMP_MODE_DISABLED). '
                                    'Full syscall table accessible.")\n'
                                    '            elif mode == "1":\n'
                                    '                print("Interpretation: Strict mode (read, write, _exit, sigreturn '
                                    'only).")\n'
                                    '            elif mode == "2":\n'
                                    '                print("Interpretation: Filter mode (SECCOMP_MODE_FILTER). BPF '
                                    'filter active, gating system calls.")\n'
                                    'EOF\n'
                                    'python3 scratch/day09_lab_b/inspect_seccomp.py > '
                                    'scratch/day09_lab_b/seccomp_mode.txt\n'
                                    'cat scratch/day09_lab_b/seccomp_mode.txt\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** Seccomp mode is identified and interpreted.\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_b/seccomp_mode.txt`',
                                    '**Stage 7: Synthesize the Isolation Worksheet Exit Artifact**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Synthesize all empirical findings into the required curriculum exit artifact: an '
                                    'isolation worksheet distinguishing resource enforcement from security isolation.\n'
                                    '```bash\n'
                                    "cat <<'EOF' > scratch/day09_lab_b/build_worksheet.py\n"
                                    'import datetime\n'
                                    '\n'
                                    'now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d '
                                    '%H:%M:%SZ")\n'
                                    '\n'
                                    'worksheet = f"""# Day 9 Exit Artifact: Isolation Comparison Worksheet\n'
                                    '**Generated:** {now}\n'
                                    '**Scope:** Distinguishing Resource Enforcement from Security Isolation in Virtual '
                                    'Machines and Containers.\n'
                                    '\n'
                                    '## 1. Subsystem Classification Matrix\n'
                                    '\n'
                                    '| Subsystem | Mechanism | Primary Function | Failure Mode / Boundary Breach | '
                                    'Security Boundary? |\n'
                                    '|---|---|---|---|---|\n'
                                    '| **Namespaces** | Kernel isolation tags (`/proc/$$/ns/`) | Visibility '
                                    'partitioning (PID, NET, MNT, IPC, UTS, USER) | Information disclosure / '
                                    'cross-namespace leak | No (Visibility only) |\n'
                                    '| **cgroups v2** | Resource accounting (`/sys/fs/cgroup`) | Resource quota '
                                    'enforcement (CPU, Memory, I/O, PIDs) | Throttling or OOM kill (exit 137) | No '
                                    '(Resource quota only) |\n'
                                    '| **Seccomp** | BPF system call filter (`/proc/$$/status`) | Gating allowable '
                                    'kernel system calls | Syscall rejected (EPERM / SIGSYS) | Yes (Restricts kernel '
                                    'attack surface) |\n'
                                    '| **Capabilities** | POSIX privilege bits (`CapEff`) | Deconstructing root '
                                    'privileges | Operation not permitted (EPERM) | Yes (Restricts privileged '
                                    'operations) |\n'
                                    '| **Virtual Machine (KVM)** | Hardware VMX/SVM & EPT MMU | Sovereign guest kernel '
                                    '& hardware emulation | Hypervisor escape (extremely rare) | Yes (Cryptographic & '
                                    'hardware enforced) |\n'
                                    '\n'
                                    '## 2. Resource Enforcement vs Security Isolation Analysis\n'
                                    '\n'
                                    '1. **Why Resource Enforcement is Not Security Isolation:**\n'
                                    '   - A container with strict cgroups v2 limits (`cpu.max`, `memory.max`) cannot '
                                    'exhaust host memory or starve neighbor CPUs.\n'
                                    '   - However, if the container exploits a vulnerability in the shared Linux '
                                    'kernel (e.g. a Dirty Pipe or io_uring privilege escalation), it gains Ring 0 '
                                    'execution on the host regardless of cgroup limits.\n'
                                    '   - Therefore, cgroups enforce *resource availability*, not *security '
                                    'isolation*.\n'
                                    '\n'
                                    '2. **Why Namespaces are Not Security Isolation:**\n'
                                    '   - Namespaces restrict what a process can see (private PID numbering, private '
                                    'network interfaces).\n'
                                    '   - However, system calls issued inside a namespace enter the same shared kernel '
                                    'space as system calls issued by the host root user.\n'
                                    '   - Therefore, namespaces enforce *visibility boundaries*, not *privilege '
                                    'containment*.\n'
                                    '\n'
                                    '3. **When to Choose Virtual Machines over Containers:**\n'
                                    '   - Workloads requiring custom Linux kernel modules or proprietary device '
                                    'drivers.\n'
                                    '   - Untrusted multi-tenant execution where hostile code could execute arbitrary '
                                    'system calls.\n'
                                    '   - Compliance mandates requiring hardware-isolated cryptographic boundaries '
                                    '(e.g. Confidential Computing / AMD SEV).\n'
                                    '\n'
                                    '4. **Defense-in-Depth Container Sandboxing:**\n'
                                    '   - For container workloads requiring near-VM isolation without VM boot '
                                    'overhead, utilize gVisor (Cloud Run / GKE Sandbox).\n'
                                    '   - gVisor runs an independent application kernel in userspace, preventing '
                                    'untrusted system calls from reaching the host Linux kernel.\n'
                                    '"""\n'
                                    '\n'
                                    'with open("scratch/day-009-isolation-worksheet.md", "w") as f:\n'
                                    '    f.write(worksheet)\n'
                                    '\n'
                                    'print("Worksheet compiled to scratch/day-009-isolation-worksheet.md")\n'
                                    'EOF\n'
                                    'python3 scratch/day09_lab_b/build_worksheet.py > scratch/day09_lab_b/stage7.log\n'
                                    'cat scratch/day09_lab_b/stage7.log\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** `scratch/day-009-isolation-worksheet.md` is compiled '
                                    'successfully.\n'
                                    '\n'
                                    '**Save:** `scratch/day-009-isolation-worksheet.md`',
                                    '**Stage 8: Validate and Verify the Exit Artifact**\n'
                                    '\n'
                                    '**Location:** local terminal\n'
                                    '\n'
                                    '**Actions:**\n'
                                    'Verify that the generated exit artifact contains all required sections, '
                                    'comparison matrices, and architectural justifications.\n'
                                    '```bash\n'
                                    "python3 -c '\n"
                                    'with open("scratch/day-009-isolation-worksheet.md") as f:\n'
                                    '    content = f.read()\n'
                                    '\n'
                                    'required = [\n'
                                    '    "Subsystem Classification Matrix",\n'
                                    '    "Resource Enforcement vs Security Isolation Analysis",\n'
                                    '    "Namespaces",\n'
                                    '    "cgroups v2",\n'
                                    '    "Seccomp",\n'
                                    '    "Capabilities",\n'
                                    '    "Virtual Machine (KVM)"\n'
                                    ']\n'
                                    '\n'
                                    'missing = [req for req in required if req not in content]\n'
                                    'if missing:\n'
                                    '    raise ValueError(f"Missing required sections: {missing}")\n'
                                    '\n'
                                    'print("✓ Day 9 Exit Artifact verified: all matrices and analysis criteria '
                                    'satisfied.")\n'
                                    "' > scratch/day09_lab_b/stage8.log\n"
                                    'cat scratch/day09_lab_b/stage8.log\n'
                                    '```\n'
                                    '\n'
                                    '**Expected result:** Output displays `✓ Day 9 Exit Artifact verified: all '
                                    'matrices and analysis criteria satisfied.`\n'
                                    '\n'
                                    '**Save:** `scratch/day09_lab_b/stage8.log`'],
                         'trouble': 'If /sys/fs/cgroup is mounted as cgroups v1, the lab commands inspect the v1 '
                                    'controllers or fall back to /proc/self/cgroup hierarchy inspection.',
                         'verification': 'Verify that the isolation worksheet exit artifact accurately records all '
                                         'inspected namespace links, cgroup limits, and capability masks.'},
                'overview': 'Linux container isolation is not a physical or hardware boundary, but an orchestration of '
                            'four discrete Linux kernel subsystems: namespaces that restrict visibility, control '
                            'groups (cgroups v2) that govern resource consumption, seccomp-BPF filters that restrict '
                            'allowable system calls, and POSIX capabilities that fragment root privileges. Because '
                            'containerized processes execute system calls directly on the shared host Linux kernel, '
                            'misconfigurations in any single layer can expose the entire host node to compromise or '
                            'resource starvation.',
                'preview': 'A fulfillment worker service intermittently crashes with exit code 137 during batch '
                           'invoicing despite monitoring dashboards displaying abundant free physical memory on the '
                           'host server. Inspecting the container runtime reveals that the application breached its '
                           'isolated cgroup memory limit during memory-intensive PDF generation, triggering a local '
                           'kernel Out-Of-Memory termination.',
                'questions': [ 'Why do Linux kernel namespaces provide visibility partitioning rather than security '
                               'boundary containment?',
                               'How does cgroups v2 memory.max enforcement trigger process termination independently '
                               'of host-level physical RAM availability?',
                               'In what ways do seccomp-BPF filters and dropped POSIX capabilities reduce kernel '
                               'attack surfaces for containerized root processes?'],
                'reference': 'https://docs.kernel.org/admin-guide/cgroup-v2.html#introduction',
                'reference_label': 'Linux Kernel Control Group v2 — Introduction (accessed 2026-11-04)',
                'scenario': { 'constraints': 'The Kubernetes pod deployment specifies a memory limit of 512 MiB '
                                             '(resources.limits.memory: "512Mi"); the node host operating system has '
                                             'ample unallocated memory; application invoicing logic generates '
                                             'uncompressed raster PDF invoices in memory before streaming.',
                              'diagnostic_steps': [ 'Inspect pod termination reason: kubectl describe pod '
                                                    'fulfillment-worker-[id] | grep -A 5 "Last State:"',
                                                    'Inspect cgroups v2 memory events: cat '
                                                    '/sys/fs/cgroup/memory.events inside or at node slice level',
                                                    'Correlate host memory graphs against container memory working set '
                                                    'in Cloud Monitoring',
                                                    'Profile application heap allocation during PDF generation using '
                                                    'memory profilers'],
                              'diagram': ( 'Batch fulfillment worker receives order packaging events',
                                           'In-memory PDF rasterization buffers 640 MB in heap',
                                           'cgroup memory.max breached triggering SIGKILL 137 OOM termination',
                                           'Refactor to chunked stream I/O and calibrate cgroup limit to 1024 MB',
                                           'Peak working set capped at 280 MB; zero OOM kills expected in bounded replay'),
                              'diagram_enabled': True,
                              'evidence': 'Reviewing Kubernetes pod status reveals "OOMKilled: true, ExitCode: 137". '
                                          'Checking the container cgroups v2 telemetry under /sys/fs/cgroup reveals '
                                          'that memory.events recorded oom_kill increments matching the exact pod '
                                          'restart timestamps.\n'
                                          '\n'
                                          '<figure class="diagram-figure">\n'
                                          '<p class="diagram-scroll-hint">Swipe horizontally to view the full '
                                          'diagram.</p>\n'
                                          '<svg aria-labelledby="day9-memory-incident-title day9-memory-incident-desc" '
                                          'role="img" viewbox="0 0 940 310">\n'
                                          '<title id="day9-memory-incident-title">Fulfillment worker cgroup memory '
                                          'failure and streaming control fix</title>\n'
                                          '<desc id="day9-memory-incident-desc">The failed dashed path buffers PDF '
                                          'packing slips in worker heap until breaching cgroup memory.max, triggering '
                                          'OOM kill. The corrected solid path streams generation to storage and '
                                          'right-sizes cgroup memory.max, verified by zero OOM kills and deduplicated '
                                          'fulfillment.</desc>\n'
                                          '<defs>\n'
                                          '<marker id="day9-memory-arrow" markerheight="8" markerwidth="10" '
                                          'orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" '
                                          'fill="#38bdf8"></path></marker>\n'
                                          '<marker id="day9-memory-fail-arrow" markerheight="8" markerwidth="10" '
                                          'orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" '
                                          'fill="#f43f5e"></path></marker>\n'
                                          '</defs>\n'
                                          '<g fill="#121526" stroke-width="2">\n'
                                          '<rect height="85" rx="8" stroke="#38bdf8" width="150" x="20" '
                                          'y="110"></rect>\n'
                                          '<image href="../assets/icons/generic/queue.svg" x="28" y="118" width="22" '
                                          'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '<rect height="85" rx="8" stroke="#f43f5e" width="220" x="225" '
                                          'y="30"></rect>\n'
                                          '<image href="../assets/icons/generic/failure.svg" x="233" y="38" width="22" '
                                          'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '<rect height="85" rx="8" stroke="#34d399" width="220" x="225" '
                                          'y="185"></rect>\n'
                                          '<image href="../assets/icons/generic/decision.svg" x="233" y="193" '
                                          'width="22" height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '<rect height="85" rx="8" stroke="#f43f5e" width="220" x="495" '
                                          'y="30"></rect>\n'
                                          '<image href="../assets/icons/generic/failure.svg" x="503" y="38" width="22" '
                                          'height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '<rect height="85" rx="8" stroke="#34d399" width="220" x="495" '
                                          'y="185"></rect>\n'
                                          '<image href="../assets/icons/generic/monitoring.svg" x="503" y="193" '
                                          'width="22" height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '<rect height="85" rx="8" stroke="#38bdf8" width="155" x="765" '
                                          'y="110"></rect>\n'
                                          '<image href="../assets/icons/generic/outcome.svg" x="768" y="118" '
                                          'width="22" height="22" preserveAspectRatio="xMidYMid meet"/>\n'
                                          '</g>\n'
                                          '<g fill="#fce7f3" font-size="12" font-weight="600" text-anchor="middle">\n'
                                          '<text x="102" y="142">Order Queue</text>\n'
                                          '<text fill="#a9b7cb" x="102" y="162">Batch packing events</text>\n'
                                          '<text x="342" y="58">[FAILED: In-Memory Heap]</text>\n'
                                          '<text fill="#f43f5e" x="342" y="78">Buffers 640M in RAM heap</text>\n'
                                          '<text fill="#a9b7cb" x="342" y="98">Host shows 12G available</text>\n'
                                          '<text x="342" y="213">[CORRECTED: Streamed]</text>\n'
                                          '<text fill="#34d399" x="342" y="233">Stream I/O + 1024M max</text>\n'
                                          '<text fill="#a9b7cb" x="342" y="253">Working set capped at 280M</text>\n'
                                          '<text x="612" y="58">EXACT FAILURE POINT</text>\n'
                                          '<text fill="#f43f5e" x="612" y="78">cgroup memory.max breached</text>\n'
                                          '<text fill="#f43f5e" x="612" y="98">SIGKILL 137 · oom_kill +1</text>\n'
                                          '<text x="612" y="213">CORRECTED CONTROL</text>\n'
                                          '<text fill="#34d399" x="612" y="233">Heap &lt; 50% of cgroup limit</text>\n'
                                          '<text fill="#a9b7cb" x="612" y="253">Zero kernel OOM kills</text>\n'
                                          '<text x="842" y="138">VERIFICATION</text>\n'
                                          '<text fill="#34d399" x="842" y="158">oom_kill == 0</text>\n'
                                          '<text fill="#a9b7cb" x="842" y="178">≤1 per order</text>\n'
                                          '</g>\n'
                                          '<g fill="none" stroke-width="2">\n'
                                          '<path d="M170 135 L220 85" marker-end="url(#day9-memory-fail-arrow)" '
                                          'stroke="#f43f5e" stroke-dasharray="7 5"></path>\n'
                                          '<path d="M445 72 L490 72" marker-end="url(#day9-memory-fail-arrow)" '
                                          'stroke="#f43f5e" stroke-dasharray="7 5"></path>\n'
                                          '<path d="M170 170 L220 215" marker-end="url(#day9-memory-arrow)" '
                                          'stroke="#38bdf8"></path>\n'
                                          '<path d="M445 227 L490 227" marker-end="url(#day9-memory-arrow)" '
                                          'stroke="#38bdf8"></path>\n'
                                          '<path d="M715 227 L756 170" marker-end="url(#day9-memory-arrow)" '
                                          'stroke="#38bdf8"></path>\n'
                                          '</g>\n'
                                          '<text fill="#a9b7cb" font-size="11" text-anchor="middle" x="470" '
                                          'y="295">Dashed line (--&gt;) = cgroup memory failure · Solid line (—&gt;) = '
                                          'streaming fix and idempotent fulfillment</text>\n'
                                          '</svg>\n'
                                          '<figcaption>Figure 9.4: Supplied facts: Worker terminates with exit code '
                                          '137 despite 70% host free memory headroom. Architectural inference: The '
                                          'worker exceeded its isolated cgroup v2 memory.max boundary during in-memory '
                                          'buffering. Expected post-fix behavior: Streamed invoice generation and '
                                          'calibrated memory limits prevent OOM termination while queue deduplication '
                                          'preserves at-most-once fulfillment semantics.</figcaption>\n'
                                          '</figure>',
                              'expected': 'Expected post-fix behavior: Streamed invoice generation and calibrated '
                                          'memory limits prevent OOM termination while queue deduplication preserves '
                                          'at-most-once fulfillment semantics.',
                              'facts': 'Supplied facts: Worker terminates with exit code 137 despite 70% host free '
                                       'memory headroom.',
                              'icons': ( '../assets/icons/generic/queue.svg',
                                         '../assets/icons/generic/failure.svg',
                                         '../assets/icons/generic/failure.svg',
                                         '../assets/icons/generic/monitoring.svg',
                                         '../assets/icons/generic/outcome.svg'),
                              'impact': 'Customer invoice processing and packing slip printing stall; queue messages '
                                        'are retried repeatedly, causing duplicate shipment notices; operational '
                                        'on-call engineers spend hours investigating the wrong architectural layer.',
                              'inference': 'Architectural inference: The worker exceeded its isolated cgroup v2 '
                                           'memory.max boundary during in-memory buffering.',
                              'remediation_steps': [ 'Refactor PDF generation logic to stream output to temporary '
                                                     'storage or Cloud Storage in 8 MB chunks',
                                                     'Update Kubernetes deployment resource limits to '
                                                     'resources.limits.memory: "1024Mi"',
                                                     'Configure Kubernetes Horizontal Pod Autoscaler based on '
                                                     'container memory utilization',
                                                     'Deploy Prometheus / Cloud Monitoring alerting rules on '
                                                     'container_memory_working_set_bytes vs limit',
                                                     'Verify that batch fulfillment completes with zero OOM events and '
                                                     'stable process PIDs'],
                              'residual': 'Allocating 1024 MiB per worker pod increases node reservation requirements, '
                                          'necessitating cluster autoscaler capacity planning to handle peak batch '
                                          'scaling events.',
                              'root': 'The application working set exceeded the isolated container cgroup v2 '
                                      'memory.max boundary (512 MiB) during batch PDF rendering. The Linux kernel '
                                      'cgroup OOM killer terminated the worker process with SIGKILL (exit code 137) to '
                                      'enforce the container limit, entirely independently of host-level physical RAM '
                                      'availability.',
                              'scenario': 'A fulfillment worker service running in a Kubernetes pod crashes repeatedly '
                                          'with exit code 137 during end-of-month batch invoicing. The operations team '
                                          'checks Cloud Monitoring host metrics and observes that the underlying '
                                          'virtual machine node has 12 GB of free physical RAM out of 16 GB total, '
                                          'leading them to erroneously suspect a network timeout or application bug.',
                              'verify': 'The application code is refactored to stream PDF generation in chunked byte '
                                        'streams rather than buffering entire document sets in heap memory. The pod '
                                        'memory limit is right-sized to 1024 MiB with a matching request. Verification '
                                        'confirms zero OOM kills over 24 hours of batch processing while host memory '
                                        'utilization remains stable.'},
                'technical': '<p><strong class="side-heading">Subtopics in this discussion:</strong></p>\n'
                             '<ol>\n'
                             '<li>Linux Kernel Namespaces (PID, NET, MNT, IPC, UTS, and USER)</li>\n'
                             '<li>Control Groups v2 (cgroups v2) Resource Accounting and Quota Limits</li>\n'
                             '<li>Seccomp (Secure Computing Mode) System Call Filtering and BPF Profiles</li>\n'
                             '<li>POSIX Capabilities and Least-Privilege Process Execution</li>\n'
                             '<li>Defense-in-Depth Container Sandboxing: gVisor, Cloud Run, and GKE Node '
                             'Isolation</li>\n'
                             '</ol>\n'
                             '\n'
                             '<h4>Linux Kernel Namespaces (PID, NET, MNT, IPC, UTS, and USER)</h4>\n'
                             '<p><strong class="side-heading">What it is in general:</strong> A Linux <strong '
                             'class="keyword">namespace</strong> is a kernel feature that wraps a global system '
                             'resource in an abstraction such that processes within the namespace see only their own '
                             'isolated instance of that resource. The Linux kernel provides eight distinct namespaces '
                             '(documented in <kbd>namespaces(7)</kbd>):\n'
                             '<strong>PID</strong> (Process ID) namespaces isolate process ID numbering, allowing a '
                             'containerized process to be PID 1 while appearing as an ordinary unprivileged PID on the '
                             'host;\n'
                             '<strong>NET</strong> (Network) namespaces isolate network devices, IP routing tables, '
                             'port bindings, and firewall rules via virtual ethernet pairs (<kbd>veth</kbd>);\n'
                             '<strong>MNT</strong> (Mount) namespaces provide isolated filesystem mount points, '
                             'typically configured via <kbd>pivot_root</kbd> to provide an independent root '
                             'filesystem;\n'
                             '<strong>IPC</strong> (Inter-Process Communication) namespaces isolate System V IPC '
                             'objects and POSIX message queues;\n'
                             '<strong>UTS</strong> (UNIX Timesharing) namespaces isolate system hostnames and NIS '
                             'domain names;\n'
                             '<strong>USER</strong> namespaces map user and group IDs (e.g., UID 0 inside the '
                             'container maps to an unprivileged UID 100000 on the host);\n'
                             '<strong>CGROUP</strong> namespaces isolate the cgroup hierarchy view; and\n'
                             '<strong>TIME</strong> namespaces isolate clock offsets.\n'
                             'Processes transition or join namespaces via the <kbd>clone()</kbd>, '
                             '<kbd>unshare()</kbd>, and <kbd>setns()</kbd> system calls, and their active namespaces '
                             'are reflected as symbolic links under <kbd>/proc/[pid]/ns/</kbd>.</p>\n'
                             '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Namespaces '
                             'establish the illusion of an independent computer for containerized applications, but '
                             'they do NOT enforce security boundaries or resource quotas. A process in a private PID '
                             'namespace cannot see neighboring processes, but if an application inside a container '
                             'exploits a kernel vulnerability (e.g., a buffer overflow in the network stack or '
                             'filesystem driver), it compromises the shared host kernel directly. Architects must '
                             'understand that namespaces control visibility, not privilege or resource '
                             'consumption.</p>\n'
                             '<p><strong class="side-heading">Relevance to GCP:</strong> In Google Kubernetes Engine '
                             '(GKE), Pods are groups of containers that share common namespaces: containers in the '
                             'same Pod share the same Network namespace (allowing them to communicate over '
                             '<kbd>localhost</kbd>) and IPC namespace, while maintaining independent Mount namespaces. '
                             'Cloud Run automatically wraps serverless container instances in dedicated namespaces to '
                             'ensure customer requests execute in isolated runtime environments on Google-managed '
                             'infrastructure.</p>\n'
                             '\n'
                             '<h4>Control Groups v2 (cgroups v2) Resource Accounting and Quota Limits</h4>\n'
                             '<p><strong class="side-heading">What it is in general:</strong> <strong '
                             'class="keyword">Control Groups v2 (cgroups v2)</strong> is the unified Linux kernel '
                             'mechanism that partitions, prioritizes, and limits the hardware resource consumption '
                             '(CPU, memory, I/O, PIDs) of process hierarchies. While cgroups v1 suffered from multiple '
                             'disjoint hierarchies and broken memory-I/O coordination, cgroups v2 enforces a single '
                             'unified hierarchy mounted at <kbd>/sys/fs/cgroup</kbd> with strict top-down resource '
                             'distribution. Resource allocation is governed by controller interface files:\n'
                             '<kbd>cpu.max</kbd> configures CPU bandwidth using Completely Fair Scheduler (CFS) quotas '
                             '(e.g., <kbd>50000 100000</kbd> restricts a cgroup to 0.5 CPU cores per 100 ms period);\n'
                             '<kbd>memory.max</kbd> establishes a hard memory consumption ceiling;\n'
                             '<kbd>memory.high</kbd> serves as a soft limit triggering proactive memory reclaim;\n'
                             '<kbd>memory.current</kbd> reports active memory usage;\n'
                             '<kbd>memory.events</kbd> tracks allocation failures, high-water mark breaches, and '
                             'kernel Out-Of-Memory (<strong class="keyword">OOM</strong>) kills; and\n'
                             '<kbd>pids.max</kbd> caps the number of active tasks to prevent fork bombs.\n'
                             'When a cgroup breaches its hard <kbd>memory.max</kbd> limit and the kernel cannot '
                             'reclaim sufficient anonymous memory or page cache, the kernel invokes the cgroup-aware '
                             'OOM killer to terminate processes inside that specific cgroup with exit code 137 '
                             '(<kbd>SIGKILL</kbd>), leaving the rest of the host operating system completely '
                             'unaffected.</p>\n'
                             '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cgroup limits '
                             'are the exact technical mechanism underlying Kubernetes resource requests and limits '
                             '(<kbd>resources.requests</kbd> and <kbd>resources.limits</kbd>). Misunderstanding '
                             'cgroups v2 leads to common operational blunders: when an application crashes with exit '
                             'code 137, operators frequently inspect host memory metrics and observe 80% free RAM, '
                             'erroneously concluding that memory pressure did not occur. Architects must monitor '
                             'cgroup-specific metrics (<kbd>memory.events</kbd> and container metrics in Cloud '
                             'Monitoring) rather than host-wide metrics to diagnose throttling and OOM terminations '
                             'accurately.</p>\n'
                             '<p><strong class="side-heading">Relevance to GCP:</strong> Modern GKE clusters running '
                             'Container-Optimized OS (COS) nodes enforce Pod CPU and memory controls through the Linux '
                             'cgroup mechanism selected by the node image and Kubernetes version. Architects must '
                             'inspect the actual node hierarchy rather than assume a fixed cgroup mode or filesystem '
                             'path; Google Cloud Monitoring exposes container resource metrics for comparison with '
                             'declared requests and limits.</p>\n'
                             '\n'
                             '<h4>Seccomp (Secure Computing Mode) System Call Filtering and BPF Profiles</h4>\n'
                             '<p><strong class="side-heading">What it is in general:</strong> <strong '
                             'class="keyword">Seccomp</strong> (Secure Computing Mode) is a Linux kernel security '
                             'facility that restricts the system calls a process can issue. The Linux kernel exposes '
                             'over 450 distinct system calls; an ordinary containerized web application requires fewer '
                             'than 70. Seccomp-BPF uses Berkeley Packet Filter (BPF) bytecode programs attached to the '
                             'process via <kbd>prctl(PR_SET_SECCOMP)</kbd> or the <kbd>seccomp()</kbd> system call to '
                             'inspect system call numbers and argument registers before the kernel executes them. If a '
                             'process attempts an unauthorized system call (such as <kbd>reboot</kbd>, '
                             '<kbd>kexec_load</kbd>, or <kbd>ptrace</kbd>), the seccomp filter instantly takes action: '
                             'returning an error code (such as <kbd>EPERM</kbd>), killing the thread with '
                             '<kbd>SIGSYS</kbd>, or killing the entire process with '
                             '<kbd>SECCOMP_RET_KILL_PROCESS</kbd>. Seccomp filters are inherited across '
                             '<kbd>fork()</kbd> and cannot be disabled once installed.</p>\n'
                             '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Seccomp serves '
                             'as the primary line of defense against Linux kernel privilege escalation exploits. '
                             'Nearly all kernel privilege escalation CVEs involve obscure, legacy, or poorly tested '
                             'system calls (e.g., <kbd>bpf()</kbd>, <kbd>userfaultfd()</kbd>, <kbd>keyctl()</kbd>). By '
                             'applying a strict seccomp profile that blocks non-essential system calls, architects '
                             'reduce the reachable kernel attack surface, so arbitrary code execution inside a '
                             'attacker achieves arbitrary code execution inside a container, they cannot trigger '
                             'vulnerabilities in dormant kernel code paths.</p>\n'
                             '<p><strong class="side-heading">Relevance to GCP:</strong> GKE deploys with the default '
                             'Kubernetes supports selecting runtime-default or local seccomp profiles through a Pod '
                             'security context. Architects must inspect the effective profile on the target GKE node '
                             'pool and test required system calls rather than assume a universal blocked-call count.</p>\n'
                             '\n'
                             '<h4>POSIX Capabilities and Least-Privilege Process Execution</h4>\n'
                             '<p><strong class="side-heading">What it is in general:</strong> Traditional UNIX '
                             'partitioned process privileges into a coarse binary model: unprivileged processes (UID '
                             '&gt; 0) with restricted access, and superuser root (UID 0) with absolute, omnipotent '
                             'system power. Linux <strong class="keyword">POSIX capabilities</strong> break down root '
                             'privilege into approximately 40 distinct, fine-grained permission bits (documented in '
                             '<kbd>capabilities(7)</kbd>). For example:\n'
                             '<kbd>CAP_NET_BIND_SERVICE</kbd> allows binding to privileged ports below 1024;\n'
                             '<kbd>CAP_NET_ADMIN</kbd> allows configuring network interfaces and firewall routing '
                             'tables;\n'
                             '<kbd>CAP_SYS_ADMIN</kbd> grants a broad range of administrative operations (often called '
                             '"the new root");\n'
                             '<kbd>CAP_SYS_MODULE</kbd> allows inserting and removing kernel modules; and\n'
                             '<kbd>CAP_CHOWN</kbd> allows modifying file ownership.\n'
                             'Each Linux process maintains four capability sets: Effective (<kbd>CapEff</kbd>), '
                             'Permitted (<kbd>CapPrm</kbd>), Inheritable (<kbd>CapInh</kbd>), and Bounding '
                             '(<kbd>CapBnd</kbd>), inspectable in <kbd>/proc/[pid]/status</kbd>. Container runtimes '
                             'strip the vast majority of capabilities from container processes, retaining only a '
                             'minimal set (such as <kbd>CAP_CHOWN</kbd>, <kbd>CAP_NET_BIND_SERVICE</kbd>, '
                             '<kbd>CAP_SETUID</kbd>) and dropping dangerous bits like <kbd>CAP_SYS_ADMIN</kbd> and '
                             '<kbd>CAP_SYS_MODULE</kbd>.</p>\n'
                             '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Even if a '
                             'container runs as UID 0 (root), dropping capabilities prevents the process from '
                             'compromising the host. A containerized process running as root without '
                             '<kbd>CAP_SYS_MODULE</kbd> cannot load rootkits; without <kbd>CAP_NET_ADMIN</kbd> it '
                             'cannot reconfigure host routing; without <kbd>CAP_SYS_RAWIO</kbd> it cannot write to '
                             'physical storage devices. Architects should enforce the security principle of least '
                             'privilege by dropping all capabilities by default (<kbd>capabilities: drop: '
                             '["ALL"]</kbd>) in Kubernetes security contexts and adding back only the specific bits '
                             'strictly necessary for the application.</p>\n'
                             '<p><strong class="side-heading">Relevance to GCP:</strong> GKE Autopilot enforces strict '
                             'capability guardrails by default, rejecting Pods that attempt to request '
                             '<kbd>CAP_SYS_ADMIN</kbd>, <kbd>CAP_SYS_MODULE</kbd>, or host path volume mounts. In '
                             'standard GKE, Google Cloud Security Command Center (SCC) continuously audits running '
                             'container workloads and raises high-severity findings if containers run with privileged '
                             'flags or excessive capability sets.</p>\n'
                             '\n'
                             '<h4>Defense-in-Depth Container Sandboxing: gVisor, Cloud Run, and GKE Node '
                             'Isolation</h4>\n'
                             '<p><strong class="side-heading">What it is in general:</strong> Because standard '
                             'containers share the host Linux kernel, defense-in-depth requires isolating container '
                             'execution boundaries beyond standard namespaces and cgroups. <strong '
                             'class="keyword">Container sandboxing</strong> introduces an intermediary virtualization '
                             "or emulation boundary between the application and the host kernel. Google's open-source "
                             '<strong class="keyword">gVisor</strong> is a user-space application kernel (written in '
                             'Go) that implements the Linux system call interface. When an application runs inside a '
                             "gVisor sandbox, its system calls are not executed by the host kernel; instead, gVisor's "
                             'userspace kernel (<kbd>Sentry</kbd>) intercepts and implements over 300 Linux system '
                             'calls in safe userspace memory. Storage and network operations are mediated through a '
                             'separate process (<kbd>Gofer</kbd>). Even if an attacker executes malicious shellcode or '
                             "exploits an unpatched Linux kernel zero-day vulnerability, the exploit strikes gVisor's "
                             'memory-safe Go runtime rather than the host Linux kernel.</p>\n'
                             '<p><strong class="side-heading">Relevance to a cloud architect:</strong> Multi-tenant '
                             'SaaS architectures, customer-supplied code execution platforms (such as code evaluation '
                             'runners or CI/CD pipelines), and AI agent execution environments present extreme '
                             'security risks. Running untrusted third-party code in standard containers on a shared '
                             'Kubernetes node is an architectural hazard because a single kernel vulnerability leads '
                             'to cluster-wide compromise. Architects must mandate sandboxed runtimes (such as gVisor '
                             'or microVMs like Firecracker) or dedicated virtual machine node pools to isolate '
                             'untrusted customer workloads securely.</p>\n'
                             '<p><strong class="side-heading">Relevance to GCP:</strong> Cloud Run executes all '
                             'container instances inside gVisor sandboxes by default, providing enterprise-grade '
                             "multi-tenant workload isolation on Google's serverless infrastructure. In GKE, "
                             'architects can enable GKE Sandbox on any node pool with a single configuration flag '
                             '(<kbd>--sandbox type=gvisor</kbd>), allowing Pods with the runtime class '
                             '<kbd>runtimeClassName: gvisor</kbd> to run alongside standard containers while enjoying '
                             'hardware-like isolation without the boot latency of full virtual machines.</p>\n'
                             '\n'
                             '<figure class="diagram-figure">\n'
                             '<p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p>\n'
                             '<svg aria-labelledby="day9-layers-title day9-layers-desc" role="img" viewbox="0 0 940 '
                             '330">\n'
                             '<title id="day9-layers-title">Linux kernel container isolation layers and syscall '
                             'evaluation</title>\n'
                             '<desc id="day9-layers-desc">A containerized process request flows sequentially through '
                             'Linux namespaces, cgroups v2 resource accounting, seccomp system call filtering, and '
                             'POSIX capability checks before executing in the shared host kernel.</desc>\n'
                             '<defs>\n'
                             '<marker id="day9-layers-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" '
                             'refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker>\n'
                             '</defs>\n'
                             '<g fill="#121526" stroke-width="2">\n'
                             '<rect height="230" rx="10" stroke="#38bdf8" width="160" x="20" y="30"></rect>\n'
                             '<image href="../assets/icons/generic/client.svg" x="32" y="42" width="24" height="24" '
                             'preserveAspectRatio="xMidYMid meet"/>\n'
                             '<rect height="230" rx="10" stroke="#f97316" width="160" x="210" y="30"></rect>\n'
                             '<image href="../assets/icons/generic/endpoint.svg" x="222" y="42" width="24" height="24" '
                             'preserveAspectRatio="xMidYMid meet"/>\n'
                             '<rect height="230" rx="10" stroke="#f43f5e" width="160" x="400" y="30"></rect>\n'
                             '<image href="../assets/icons/generic/monitoring.svg" x="412" y="42" width="24" '
                             'height="24" preserveAspectRatio="xMidYMid meet"/>\n'
                             '<rect height="230" rx="10" stroke="#eab308" width="160" x="590" y="30"></rect>\n'
                             '<image href="../assets/icons/generic/policy.svg" x="602" y="42" width="24" height="24" '
                             'preserveAspectRatio="xMidYMid meet"/>\n'
                             '<rect height="230" rx="10" stroke="#34d399" width="140" x="780" y="30"></rect>\n'
                             '<image href="../assets/icons/generic/server.svg" x="792" y="42" width="24" height="24" '
                             'preserveAspectRatio="xMidYMid meet"/>\n'
                             '</g>\n'
                             '<g fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">\n'
                             '<text x="100" y="76">Container Process</text>\n'
                             '<text x="290" y="76">1. Namespaces</text>\n'
                             '<text x="480" y="76">2. cgroups v2</text>\n'
                             '<text x="670" y="76">3. Seccomp &amp; Caps</text>\n'
                             '<text x="850" y="76">Host Kernel</text>\n'
                             '</g>\n'
                             '<g fill="#a9b7cb" font-size="11" text-anchor="middle">\n'
                             '<text x="100" y="98">Order API / Worker</text>\n'
                             '<text fill="#fce7f3" x="100" y="120">Userspace Process</text>\n'
                             '<text x="100" y="142">UID 0 (Container Root)</text>\n'
                             '<text x="100" y="164">or unprivileged UID</text>\n'
                             '<text fill="#38bdf8" x="100" y="195">Issues System Call</text>\n'
                             '<text x="100" y="218">(open, clone, socket)</text>\n'
                             '<text fill="#fce7f3" x="290" y="98">Visibility Filter</text>\n'
                             '<text x="290" y="120">PID: Virtual process tree</text>\n'
                             '<text x="290" y="142">NET: veth &amp; private routes</text>\n'
                             '<text x="290" y="164">MNT: pivot_root tree</text>\n'
                             '<text x="290" y="186">IPC · UTS · USER</text>\n'
                             '<text fill="#34d399" x="290" y="218">✓ Scoped View</text>\n'
                             '<text fill="#fce7f3" x="480" y="98">Resource Limits</text>\n'
                             '<text x="480" y="120">cpu.max (CFS quota)</text>\n'
                             '<text x="480" y="142">memory.max (limit)</text>\n'
                             '<text x="480" y="164">io.max · PSI accounting</text>\n'
                             '<text fill="#f43f5e" x="480" y="195">Breach: OOM Kill</text>\n'
                             '<text fill="#34d399" x="480" y="218">✓ Within Budget</text>\n'
                             '<text fill="#fce7f3" x="670" y="98">Privilege Gating</text>\n'
                             '<text x="670" y="120">Seccomp: BPF filter</text>\n'
                             '<text x="670" y="142">Blocks dangerous calls</text>\n'
                             '<text x="670" y="164">CapEff: Bound bits</text>\n'
                             '<text fill="#f43f5e" x="670" y="195">Denied: EPERM / SIGSYS</text>\n'
                             '<text fill="#34d399" x="670" y="218">✓ Authorized</text>\n'
                             '<text fill="#fce7f3" x="850" y="98">Execution</text>\n'
                             '<text x="850" y="125">Shared Kernel Space</text>\n'
                             '<text x="850" y="155">Ring 0 Privilege</text>\n'
                             '<text x="850" y="185">Hardware I/O</text>\n'
                             '<text fill="#34d399" x="850" y="218">CPU / RAM / Disk</text>\n'
                             '</g>\n'
                             '<g fill="none" marker-end="url(#day9-layers-arrow)" stroke="#38bdf8" stroke-width="2">\n'
                             '<path d="M180 145 L206 145"></path>\n'
                             '<path d="M370 145 L396 145"></path>\n'
                             '<path d="M560 145 L586 145"></path>\n'
                             '<path d="M750 145 L776 145"></path>\n'
                             '</g>\n'
                             '<text fill="#a9b7cb" font-size="12" text-anchor="middle" x="470" y="295">Every container '
                             'action traverses all four kernel control gates; none provides a separate kernel.</text>\n'
                             '</svg>\n'
                             '<figcaption>Figure 9.2: Conceptual system call flow through the four Linux kernel '
                             'container isolation layers. Namespaces partition what the process sees; cgroups v2 '
                             'throttle and cap what it consumes; seccomp filters which system calls may enter kernel '
                             'space; and capabilities restrict privileged kernel operations.</figcaption>\n'
                             '</figure>\n'
                             '\n'
                             '<div class="topic-card">\n'
                             '<table>\n'
                             '<caption>Table 9.2: The Four Pillars of Linux Container Isolation</caption>\n'
                             '<thead>\n'
                             '<tr>\n'
                             '<th>Subsystem</th>\n'
                             '<th>Primary Function</th>\n'
                             '<th>Kernel Inspection Mechanism</th>\n'
                             '<th>Failure or Violation Symptom</th>\n'
                             '</tr>\n'
                             '</thead>\n'
                             '<tbody>\n'
                             '<tr>\n'
                             '<td><strong>Namespaces</strong></td>\n'
                             '<td>Visibility filtering (PID, NET, MNT, IPC, UTS, USER)</td>\n'
                             '<td><kbd>readlink /proc/$$/ns/*</kbd></td>\n'
                             '<td>Process cannot see or address foreign processes or network interfaces</td>\n'
                             '</tr>\n'
                             '<tr>\n'
                             '<td><strong>cgroups v2</strong></td>\n'
                             '<td>Resource quota enforcement (CPU, Memory, I/O, PIDs)</td>\n'
                             '<td><kbd>/sys/fs/cgroup/memory.max</kbd>, <kbd>memory.events</kbd></td>\n'
                             '<td>OOM kill (exit 137, <kbd>oom_kill +1</kbd>) or CPU throttling '
                             '(<kbd>cpu.stat</kbd>)</td>\n'
                             '</tr>\n'
                             '<tr>\n'
                             '<td><strong>Seccomp</strong></td>\n'
                             '<td>System call filtering via BPF bytecode programs</td>\n'
                             '<td><kbd>grep Seccomp /proc/$$/status</kbd></td>\n'
                             '<td>Immediate process abort (<kbd>SIGSYS</kbd>) or permission error '
                             '(<kbd>EPERM</kbd>)</td>\n'
                             '</tr>\n'
                             '<tr>\n'
                             '<td><strong>Capabilities</strong></td>\n'
                             '<td>Deconstruction of root privileges into ~40 discrete bits</td>\n'
                             '<td><kbd>grep CapEff /proc/$$/status</kbd> (<kbd>capsh --decode</kbd>)</td>\n'
                             '<td>Privileged operation rejected (<kbd>Operation not permitted</kbd>)</td>\n'
                             '</tr>\n'
                             '</tbody>\n'
                             '</table>\n'
                             '</div>\n'
                             '\n'
                             '<p><strong class="side-heading">Concrete example:</strong> Consider a production '
                             'document processing container running on GKE that generates PDF reports. The container '
                             'is configured in this worked example with a cgroups v2 memory limit of 512 MB (<kbd>memory.max = '
                             '536870912</kbd>). When an unexpected batch of 50 complex architectural diagrams is '
                             'queued, the application attempts to buffer uncompressed raster images in memory, driving '
                             'memory usage up to 513 MB. The host server possesses 64 GB of physical RAM with 48 GB '
                             'completely unallocated. However, because cgroups v2 enforces local limits independently '
                             'of host headroom, the kernel invokes the cgroup OOM killer, dispatches '
                             '<kbd>SIGKILL</kbd> to the worker process, increments <kbd>oom_kill</kbd> in '
                             '<kbd>/sys/fs/cgroup/memory.events</kbd>, and records exit code 137 in Kubernetes. The '
                             'architect refactors the application to stream document generation directly to Cloud '
                             'Storage via chunked byte buffers, capping active working set memory at 180 MB and '
                             'with the expected result of avoiding cgroup OOM kills without resizing the host VM.</p>\n'
                             '\n'
                             '<p><strong class="side-heading">Evidence limit:</strong> Inspecting namespace links in '
                             '<kbd>/proc/$$/ns/</kbd> and recording capability masks in '
                             '<kbd>/proc/$$/status</kbd> documents the process context visible to this local inspection; '
                             'it does not prove complete security '
                             'against side-channel microarchitectural attacks (such as cache timing or branch '
                             'prediction leaks) on shared CPU cores without hardware-enforced CPU core pinning and '
                             'hypervisor or sandboxed kernel boundaries.</p>\n',
                'title': 'Container isolation'}],
  'work_block': 'Days 1–17 — Foundations'}



# --- POST-PROCESSING ENHANCEMENTS FOR DAY 9 ---
import os, re, urllib.parse
from bs4 import BeautifulSoup, NavigableString

# Load terms from scratch/audits/day-009-terms.txt
_terms_file = 'scratch/audits/day-009-terms.txt'
if os.path.exists(_terms_file):
    TERMS = [l.strip() for l in open(_terms_file, encoding='utf-8') if l.strip() and not l.startswith('#')]
else:
    TERMS = []
TERMS = sorted(TERMS, key=len, reverse=True)

# 1. Expand Topic 1 with worked mechanisms (R2 bullet form)
_t0 = DATA['topics'][0]
_t0['technical'] = _t0['technical'].replace(
    '<h4>The Linux KVM Subsystem and QEMU Userspace Model</h4>',
    '<ul>\n'
    '<li><strong class="side-heading">Core hardware virtualization architectural mechanisms:</strong>\n'
    '<ul>\n'
    '<li><strong class="keyword">Intel VT-x / AMD-V (CPU Virtualization)</strong>: Adds specialized CPU modes—such as Intel VMX Root and Non-Root modes or AMD SVM (Secure Virtual Machine)—allowing guest operating systems to execute privileged instructions directly on the physical processor.</li>\n'
    '<li><strong class="keyword">EPT / RVI (Memory Virtualization)</strong>: Intel Extended Page Tables (EPT) and AMD Rapid Virtualization Indexing (RVI, or Nested Page Tables) handle two-stage memory address translation directly in hardware. This eliminates the heavy overhead of maintaining software shadow page tables.</li>\n'
    '<li><strong class="keyword">vCPUs (Virtual CPUs)</strong>: Logical processing units assigned by the hypervisor to a virtual machine, scheduled directly onto physical CPU cores via hardware virtualization extensions.</li>\n'
    '<li><strong class="keyword">IOMMU (Intel VT-d / AMD-Vi)</strong>: Hardware-level Input/Output Memory Management Units that allow virtual machines to directly access physical hardware like GPUs and network cards (device passthrough).</li>\n'
    '</ul>\n'
    '</li>\n'
    '<li><strong class="side-heading">How hardware-assisted virtualization operates:</strong>\n'
    '<ul>\n'
    '<li><strong class="keyword">Privilege Separation</strong>: The hypervisor runs in a high-privilege root mode, while the guest operating system runs in non-root mode.</li>\n'
    '<li><strong class="keyword">VM Exits and Entries</strong>: When a guest OS attempts a sensitive hardware-level action, a VM exit safely transfers control to the hypervisor, which processes the request and hands control back via a VM entry.</li>\n'
    '<li><strong class="keyword">Performance Gain</strong>: Older methods relied on slow software instruction interception or kernel modification (paravirtualization). Hardware extensions execute code directly, making multi-tenant cloud servers and local hypervisors like VMware Workstation or KVM practical.</li>\n'
    '</ul>\n'
    '</li>\n'
    '</ul>\n\n'
    '<h4>The Linux KVM Subsystem and QEMU Userspace Model</h4>',
    1
)

_t0['technical'] = _t0['technical'].replace(
    '<h4>Compute Engine Hypervisor Architecture and Shielded VM Security</h4>',
    '<ul>\n'
    '<li><strong class="side-heading">The Linux KVM Subsystem (Kernel Space):</strong>\n'
    '<ul>\n'
    '<li><strong class="keyword">Hypervisor Role</strong>: KVM converts the Linux kernel into a Type-1 (bare-metal) hypervisor by loading kernel modules (<kbd>kvm.ko</kbd>, plus hardware-specific modules like <kbd>kvm-intel.ko</kbd> or <kbd>kvm-amd.ko</kbd>).</li>\n'
    '<li><strong class="keyword">Hardware Acceleration</strong>: It leverages hardware virtualization extensions (such as Intel VT-x or AMD-V) to run guest CPU instructions directly on the physical processor at near-native speed.</li>\n'
    '<li><strong class="keyword">Process Representation</strong>: Each virtual machine runs as a standard Linux process managed by the kernel scheduler and memory manager.</li>\n'
    '<li><strong class="keyword">The /dev/kvm Interface</strong>: Userspace programs interact with KVM via the <kbd>/dev/kvm</kbd> character device node using ioctl system calls to create VMs, allocate guest memory, and inject interrupts.</li>\n'
    '</ul>\n'
    '</li>\n'
    '<li><strong class="side-heading">The QEMU Userspace Model:</strong>\n'
    '<ul>\n'
    '<li><strong class="keyword">Device Emulation</strong>: KVM alone only handles CPU and memory virtualization; it relies on QEMU in userspace to emulate complete system hardware—including disk controllers, network cards, graphic adapters, and BIOS/UEFI firmware.</li>\n'
    '<li><strong class="keyword">VM Exits and Hand-offs</strong>: When a guest operating system tries to access a virtualized device or trigger a privileged event that KVM cannot handle directly, a VM exit occurs. Execution transfers from KVM to the QEMU userspace process to handle the device emulation in software before returning control back to the guest.</li>\n'
    '<li><strong class="keyword">Paravirtualization (Virtio)</strong>: To bypass slow device emulation overhead for high-throughput disk and network I/O, QEMU and KVM utilize virtio paravirtualized drivers, allowing the guest and host to communicate efficiently through shared memory rings.</li>\n'
    '<li><strong class="keyword">Management &amp; Control</strong>: QEMU acts as the Virtual Machine Monitor (VMM), often orchestrated via higher-level management APIs and tools like <kbd>libvirt</kbd> and <kbd>virt-manager</kbd>.</li>\n'
    '</ul>\n'
    '</li>\n'
    '</ul>\n\n'
    '<h4>Compute Engine Hypervisor Architecture and Shielded VM Security</h4>',
    1
)

_t0['technical'] = _t0['technical'].replace(
    '<h4>Guest Kernel Autonomy vs Hypervisor Management Overhead</h4>',
    '<ul>\n'
    '<li><strong class="side-heading">Compute Engine Hypervisor Architecture:</strong>\n'
    '<ul>\n'
    '<li><strong class="keyword">Direct Hardware Access</strong>: The hypervisor operates as a bare-metal abstraction layer, scheduling vCPUs and managing physical memory without a general-purpose host operating system in the data path.</li>\n'
    '<li><strong class="keyword">Verified Boot Stack</strong>: Physical servers execute a cryptographically verified boot chain where every layer—from the physical host firmware up to the hypervisor—must pass digital signature validation before loading.</li>\n'
    '<li><strong class="keyword">Tenant Isolation</strong>: Hardware-assisted virtualization extensions (Intel VT-x / AMD-V) and memory management unit (IOMMU) controls isolate guest memory spaces and network traffic per project and instance.</li>\n'
    '</ul>\n'
    '</li>\n'
    '<li><strong class="side-heading">Shielded VM Security Components:</strong> Google Cloud Shielded VMs extend protection from the hypervisor layer into the guest operating system using three primary capabilities:\n'
    '<ul>\n'
    '<li><strong class="keyword">Secure Boot</strong>: Uses Unified Extensible Firmware Interface (UEFI) firmware to verify the digital signatures of all early-boot components, kernels, and kernel modules before they execute, blocking unsigned bootloaders or rootkits. (Enabled via explicit opt-in due to compatibility requirements like ARM64 or out-of-tree drivers).</li>\n'
    '<li><strong class="keyword">Virtual Trusted Platform Module (vTPM)</strong>: Provides a hardware-grade, virtualized TPM 2.0 chip dedicated to the instance. It performs Measured Boot by recording cryptographic hashes of boot components into Platform Configuration Registers (PCRs) and securely stores encryption keys. (Enabled by default).</li>\n'
    '<li><strong class="keyword">Integrity Monitoring</strong>: Continuously tracks boot measurements against a baseline policy through Cloud Monitoring/Operations suites to flag unexpected kernel or boot modifications. (Enabled by default alongside the vTPM).</li>\n'
    '</ul>\n'
    '</li>\n'
    '</ul>\n\n'
    '<h4>Guest Kernel Autonomy vs Hypervisor Management Overhead</h4>',
    1
)

# 2. Expand Topic 2 with worked mechanism (User Namespaces / Rootless Containers)
_t1 = DATA['topics'][1]
_t1['technical'] = _t1['technical'].replace(
    '<h4>Control Groups v2 (cgroups v2) Resource Accounting and Quota Limits</h4>',
    '<ul>\n'
    '<li><strong class="side-heading">User namespace UID mapping and rootless container isolation:</strong> Rootless containers decouple container administration from physical host root by executing the container runtime in an unprivileged user namespace. The Linux kernel can map container UID 0 to a subordinate host UID range defined in <kbd>/etc/subuid</kbd>, with the active translation recorded in <kbd>/proc/[pid]/uid_map</kbd>. The mapping reduces the host privileges attached to container UID 0, but it does not by itself prevent kernel vulnerabilities or unsafe host-resource exposure; architects must combine it with namespaces, capabilities, seccomp, and workload-specific sandboxing.</li>\n'
    '</ul>\n\n'
    '<h4>Control Groups v2 (cgroups v2) Resource Accounting and Quota Limits</h4>',
    1
)

# 2a. Same-day Study expansions: worked VM and container mechanism traces.
def _worked_subtopic(title, general, architect, gcp, trace_rows, example, evidence):
    rows = ''.join(
        '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(*row)
        for row in trace_rows
    )
    return (
        '<h4>' + title + '</h4>\n'
        '<p><strong class="side-heading">What it is in general:</strong> ' + general + '</p>\n'
        '<p><strong class="side-heading">Relevance to a cloud architect:</strong> ' + architect + '</p>\n'
        '<p><strong class="side-heading">Relevance to GCP:</strong> ' + gcp + '</p>\n'
        '<div class="topic-card"><table><caption>' + title + ' — mechanism trace</caption>'
        '<thead><tr><th>Step or state</th><th>Owner</th><th>Observable evidence</th><th>Decision or failure signal</th></tr></thead>'
        '<tbody>' + rows + '</tbody></table></div>\n'
        '<p><strong class="side-heading">Concrete example:</strong> ' + example + '</p>\n'
        '<p><strong class="side-heading">Evidence limit:</strong> ' + evidence + '</p>\n'
    )

_vm_expansions = ''.join([
    _worked_subtopic(
        'From /dev/kvm to a running virtual CPU',
        'A KVM virtual machine begins as a userspace process that opens <kbd>/dev/kvm</kbd>, checks the API version, creates a virtual-machine file descriptor, registers guest memory, creates one or more virtual CPU file descriptors, initializes register state, and repeatedly enters the <kbd>KVM_RUN</kbd> ioctl. The guest does not become a second host kernel process merely because it executes privileged instructions: CPU virtualization keeps guest state in a hardware control structure and returns control to the host on configured exits. Device emulation, interrupt injection, timers, and lifecycle coordination remain responsibilities of the userspace virtual machine monitor. This sequence explains what a VM actually is operationally: host-owned process and memory objects plus hardware-managed guest execution state, not a miniature physical server hidden from the host.',
        'The lifecycle identifies ownership boundaries. Platform teams own host scheduling, memory backing, virtual devices, and stop/start operations; guest teams own the guest kernel, services, filesystems, and application configuration. An architect should ask which failure domain produced the evidence before changing capacity: a guest panic, a virtual device timeout, a host scheduling delay, and a management-plane stop can all present as an unavailable instance but require different remediation. The sequence also clarifies why guest root is powerful inside the VM yet does not automatically control the host.',
        'Compute Engine exposes the instance as a managed VM while keeping the physical host and hypervisor outside the customer administration boundary. Inside the instance, guest-visible evidence includes CPU topology, kernel logs, device identifiers, and service state. Outside the guest, instance state, serial-port output, monitoring, and platform operation records provide a separate view. The learner must correlate these views without claiming access to Google-managed host internals or treating a guest observation as proof of physical-host behavior.',
        [
            ('Open KVM subsystem', 'Host VMM process', '<kbd>open("/dev/kvm")</kbd> result', 'Failure means KVM is unavailable or access is denied'),
            ('Create VM descriptor', 'KVM kernel API', '<kbd>KVM_CREATE_VM</kbd> return value', 'Descriptor scopes later VM-specific ioctls'),
            ('Register guest memory', 'VMM plus host memory manager', 'Userspace address and guest-physical slot', 'Invalid mapping prevents guest memory access'),
            ('Create vCPU', 'KVM and host scheduler', 'vCPU file descriptor and thread', 'Thread placement affects scheduling latency'),
            ('Initialize registers', 'VMM', 'General, control, and special-register state', 'Incorrect boot state stops before guest kernel entry'),
            ('Enter guest', 'CPU virtualization hardware', '<kbd>KVM_RUN</kbd> and guest instruction progress', 'Configured event causes VM exit'),
            ('Handle exit', 'KVM or userspace VMM', 'Exit reason and emulated action', 'Unexpected exit rate indicates workload or device pressure'),
            ('Resume or stop', 'VMM lifecycle controller', 'Next run-loop entry or clean shutdown', 'Preserve guest and platform evidence separately')
        ],
        'A local teaching VMM creates one vCPU and maps a small guest-physical region. A failed <kbd>KVM_CREATE_VM</kbd> call is host-side evidence; a guest boot message after <kbd>KVM_RUN</kbd> is guest-side evidence. The worksheet records both and refuses to infer Compute Engine host implementation details from either observation.',
        'The KVM API trace explains a general Linux virtualization mechanism and can be observed only on a host that exposes KVM. It does not demonstrate Google Cloud host code, physical CPU allocation, tenant placement, or a production Compute Engine failure.'
    ),
    _worked_subtopic(
        'Two-stage address translation and guest memory ownership',
        'A process inside a guest produces a guest virtual address. The guest kernel page tables translate that address to a guest physical address, and the hypervisor-managed second stage translates the guest physical address to host physical memory. Intel Extended Page Tables and AMD nested page tables allow hardware to cache the combined translation in the translation lookaside buffer. A miss can therefore require walks through both page-table structures. The guest owns its first-stage mappings and permissions; the host owns the backing memory, second-stage mappings, reclamation policy, and isolation between virtual machines. A guest page marked writable cannot bypass a read-only or absent second-stage mapping.',
        'This ownership split matters when diagnosing memory symptoms. A guest out-of-memory event is not the same as a host capacity event, and guest free-memory output cannot prove that host backing is immediately available. Architects should separate allocation promises, guest working set, page-cache behavior, ballooning or reclamation, and second-stage translation overhead. Huge pages can reduce translation pressure but introduce allocation, fragmentation, and operational trade-offs. Memory encryption or confidential-computing features add another boundary and must not be inferred from ordinary page-table observations.',
        'Compute Engine customers size guest memory through machine types and observe the guest operating system plus Cloud Monitoring metrics available to them. They do not administer the host page tables. A sound design records guest memory pressure, application allocation behavior, and instance-level metrics, then treats host backing and physical placement as provider-owned. Claims about Confidential VM encryption, live migration, or physical NUMA placement require their own product documentation and cannot be derived from the generic KVM memory path.',
        [
            ('Application load/store', 'Guest process', 'Guest virtual address and application profile', 'Page fault if guest mapping is absent'),
            ('First-stage lookup', 'Guest kernel and MMU', 'Guest page tables', 'Guest permissions may deny access'),
            ('Guest physical address', 'Guest kernel abstraction', 'GPA visible to guest kernel tooling', 'Not a host physical address'),
            ('Second-stage lookup', 'Hypervisor and MMU', 'EPT or nested-page-table entry', 'Missing mapping exits or faults to host'),
            ('Host backing page', 'Host memory manager', 'Provider-owned mapping', 'Guest cannot directly identify physical placement'),
            ('Combined TLB entry', 'Processor', 'Performance counters where exposed', 'Miss increases translation work'),
            ('Dirty/accessed state', 'Guest and host memory subsystems', 'Layer-specific counters', 'Do not merge layer meanings'),
            ('Reclaim or termination', 'Owning memory layer', 'Guest OOM, balloon action, or platform event', 'Diagnose the layer before resizing')
        ],
        'A database reports a guest page fault spike while instance-level memory remains within its configured size. The architect first checks guest working-set growth and page-table activity, then storage latency and application allocation. The team does not label the symptom a physical-host shortage because no host evidence was supplied.',
        'Guest metrics and a conceptual EPT trace establish how translations are expected to compose. They do not reveal the provider host page tables, physical DIMM location, cache residency, or another tenant’s memory behavior.'
    ),
    _worked_subtopic(
        'Virtual CPU scheduling, exits, and overcommit signals',
        'A vCPU is execution state scheduled by the host, commonly represented by a host thread. While the thread is running in guest mode, ordinary guest instructions can execute directly. Configured privileged operations, interrupts, I/O events, or unsupported conditions cause a VM exit so KVM or the userspace VMM can handle the event. The host scheduler can deschedule the vCPU thread just like other runnable work. Guest CPU utilization measures work from the guest perspective, whereas steal time or platform scheduling metrics describe time the guest expected to run but did not. A high exit rate, lock contention, and host scheduling delay are distinct mechanisms even when application latency rises.',
        'Architects need this model for latency-sensitive placement and capacity decisions. Adding vCPUs can reduce queueing when work is parallel, but it can also increase lock contention, cross-NUMA traffic, or licensing cost. CPU pinning and dedicated placement trade flexibility for predictability. Nested virtualization inserts another scheduling and exit boundary: an L2 guest’s privileged event may traverse L1 and L0 controls, so performance results must name the layer under test. A capacity recommendation should use measured runnable queues and service latency rather than assuming every busy vCPU requires a larger machine.',
        'Compute Engine machine series expose documented vCPU counts and performance characteristics, but guest observations do not prove a fixed mapping to physical cores. The design should use product-specific documentation for sustained-use behavior, nested-virtualization support, and sole-tenancy or placement options. In this lesson, the GCP relevance is the diagnostic separation between guest CPU evidence, instance monitoring, and provider-owned host scheduling—not an assertion about a particular fleet scheduler.',
        [
            ('Guest thread becomes runnable', 'Guest scheduler', 'Guest run queue and process state', 'Application may be CPU-bound or blocked'),
            ('vCPU thread runnable', 'Host scheduler', 'Host-side state when locally observable', 'Guest cannot normally see full host queue'),
            ('Guest entry', 'KVM and processor', 'Run-loop transition', 'Direct execution begins'),
            ('Timer or interrupt', 'Virtual interrupt controller', 'Guest interrupt counters', 'Delivery latency affects tail response'),
            ('Privileged operation', 'Guest kernel and CPU', 'VM-exit reason', 'Frequent exits can add overhead'),
            ('Exit handling', 'KVM or VMM', 'Handler duration', 'Device or emulation path may dominate'),
            ('Host deschedule', 'Host scheduler', 'Steal or scheduling evidence where exposed', 'Do not confuse with guest idle time'),
            ('Service completion', 'Guest application', 'Request latency and throughput', 'Correlate rather than infer causality')
        ],
        'A synthetic service shows 90% guest CPU and rising request latency. The worksheet compares guest run queues, application lock profiles, and any exposed scheduling indicators. It recommends a scale test and identifies which measurements would distinguish useful parallelism from host scheduling delay or VM-exit overhead.',
        'A guest benchmark can measure application throughput and guest-visible counters. Without host or platform evidence it cannot prove overcommit, physical-core sharing, scheduler policy, or the cause of a transient latency spike.'
    ),
    _worked_subtopic(
        'Virtual devices, virtio queues, and the IOMMU boundary',
        'A virtual machine needs storage, networking, console, clock, and interrupt devices. Full emulation reproduces a hardware interface in the VMM, while paravirtualized virtio devices present an interface designed for efficient guest-host cooperation. The guest driver places descriptors in shared virtqueues, notifies the device backend, and later consumes completions. Memory used for direct device access must be constrained so a device or guest cannot DMA into unrelated host or tenant memory; an input/output memory management unit supplies that translation and protection boundary for passthrough designs. Device reset, queue ownership, interrupt routing, and completion ordering are therefore part of isolation as well as performance.',
        'The path explains why a VM can be CPU-healthy yet I/O-stalled. Architects should identify the guest driver, queue depth, backend, storage or network service, and completion signal before blaming the hypervisor. Passthrough reduces emulation overhead but narrows mobility and management options; emulation improves compatibility but increases code and exit paths; virtio balances performance with a stable paravirtual contract. Security review must include malformed descriptors, backend privilege, DMA mapping, and reset behavior rather than treating the CPU boundary as the whole VM security story.',
        'Compute Engine exposes supported virtual device interfaces through guest operating system drivers and documented machine or disk capabilities. Customers can inspect guest driver state and service metrics but cannot observe provider backend processes directly. The appropriate GCP decision is to select supported images and drivers, use documented device features, and preserve guest plus service evidence. This lesson does not assign a particular Google backend implementation to every device path.',
        [
            ('Application issues I/O', 'Guest process', 'System call and application trace', 'Request may block or queue'),
            ('Guest kernel builds request', 'Guest driver', 'Block or network queue state', 'Driver errors remain guest-side evidence'),
            ('Descriptor published', 'Guest virtio driver', 'Virtqueue indices', 'Malformed or full ring prevents progress'),
            ('Backend notified', 'Virtual device transport', 'Kick or exit where observable', 'Notification batching changes latency'),
            ('Backend performs work', 'VMM or provider service', 'Service metric or local backend trace', 'Backend is outside guest ownership'),
            ('DMA mapping enforced', 'IOMMU and host', 'Mapping policy when locally observable', 'Prevents access outside assigned memory'),
            ('Completion posted', 'Backend and interrupt path', 'Used-ring entry and interrupt', 'Lost completion appears as guest timeout'),
            ('Guest wakes caller', 'Guest kernel', 'Completed system call', 'End-to-end latency spans every owner')
        ],
        'A VM sees storage latency with low guest CPU. The investigation records application I/O latency, guest block queue depth, driver messages, and disk-service metrics. It does not claim a hypervisor defect merely because the guest waits; the worksheet marks the backend and physical path as unknown until supported evidence exists.',
        'Guest queue and driver observations locate delay within the guest-visible portion of the path. They do not expose provider backend code, physical device firmware, IOMMU configuration, or another tenant’s traffic.'
    ),
    _worked_subtopic(
        'Type 1 and Type 2 failure ownership in a placement decision',
        'The Type 1 and Type 2 labels describe where the virtualization layer sits relative to hardware and a general-purpose host operating system, but they do not replace a failure-domain analysis. A hosted development hypervisor depends on the host desktop kernel, drivers, power policy, and user session. A bare-metal cloud hypervisor removes that desktop ownership model, yet still has firmware, management, virtual-device, and provider-control layers. In both cases the guest retains its own kernel and userspace. The useful comparison is therefore not “secure versus insecure” but which owner configures, observes, patches, and recovers each layer.',
        'Architects should match workload requirements to the boundary: kernel modules, operating-system choice, boot controls, licensing, recovery objectives, and untrusted-code exposure. A VM can satisfy guest-kernel autonomy while still requiring image patching and application hardening. A local Type 2 VM can reproduce guest behavior but is not performance or availability evidence for a cloud Type 1 platform. The worksheet should identify portability assumptions and name every untested provider behavior.',
        'For Compute Engine, Google owns the physical host and virtualization platform while the customer owns the guest according to the service responsibility model. Product features such as Shielded VM, Confidential VM, live migration, sole tenancy, and nested virtualization must be evaluated from their current documentation. This subtopic uses the generic boundary model only to frame those later product decisions.',
        [
            ('Physical firmware', 'Device or cloud provider', 'Attestation or provider evidence if offered', 'Guest logs do not prove firmware state'),
            ('Host or hypervisor', 'Desktop owner or cloud provider', 'Local host logs or provider operation status', 'Ownership differs by deployment model'),
            ('Virtual hardware', 'Hypervisor/VMM owner', 'Guest device enumeration', 'Enumeration proves interface, not backend design'),
            ('Guest boot chain', 'Guest image owner', 'Boot and integrity records', 'Unsigned or incompatible module can fail'),
            ('Guest kernel', 'Customer or image publisher', 'Kernel logs and package state', 'Patch responsibility remains explicit'),
            ('Guest services', 'Application team', 'Service health and configuration', 'A healthy VM is not a healthy application'),
            ('Recovery operation', 'Layer owner', 'Snapshot, restart, rebuild, or provider event', 'Choose action at the failed layer'),
            ('Acceptance evidence', 'Architecture team', 'Layered worksheet', 'Unknown layers remain unknown')
        ],
        'A vendor driver requires a specific guest kernel. The placement record selects a VM because guest-kernel control is necessary, then separately records image patching, boot validation, availability design, and the fact that the local hosted-hypervisor test did not validate Compute Engine performance.',
        'The ownership table is an architectural model. It does not prove the security, availability, or implementation of a named hypervisor product without product-specific evidence.'
    ),
    _worked_subtopic(
        'Guest boot, kernel autonomy, and boundary evidence',
        'A virtual machine boot crosses several contracts: virtual firmware selects boot media, a bootloader loads a guest kernel and initial filesystem, the guest kernel initializes its own scheduler and drivers, and the service manager starts userspace. Kernel autonomy means the guest controls those guest-layer choices within the virtual hardware interface. It does not mean the guest controls the hypervisor, physical firmware, host scheduler, or provider management plane. A boot record must therefore name the layer that emitted it. Virtual firmware messages, bootloader output, kernel messages, system-service status, and platform operation state are complementary evidence rather than interchangeable proof.',
        'This trace helps architects choose images, recovery methods, and patch ownership. A kernel module failure may require a compatible guest kernel, signed module, or boot-policy change; it does not justify weakening the host boundary. A service start failure belongs above the kernel even when the VM is running. Image rollback, serial-console capture, immutable image replacement, and in-place repair have different recovery and audit properties. The design should define which team owns each artifact and when a failed VM is repaired versus rebuilt.',
        'Compute Engine exposes guest startup and serial evidence plus instance lifecycle information, while Google retains the physical host. Shielded VM and Confidential VM add documented controls, but their presence cannot be inferred from a generic KVM trace. This lesson uses guest boot evidence to demonstrate autonomy and responsibility; product eligibility, defaults, and attestation procedures remain subject to current Google Cloud documentation.',
        [
            ('Virtual firmware starts', 'Virtual platform', 'Firmware or serial output', 'Failure precedes guest kernel'),
            ('Boot target selected', 'Firmware and boot policy', 'Selected disk or network target', 'Wrong target can mimic missing OS'),
            ('Bootloader runs', 'Guest image owner', 'Bootloader output and configuration', 'Signature or configuration failure stops kernel load'),
            ('Guest kernel loads', 'Guest OS owner', 'Kernel version and command line', 'Module and driver compatibility begin here'),
            ('Root filesystem mounted', 'Guest kernel', 'Mount and storage-driver evidence', 'Missing device or filesystem blocks userspace'),
            ('Service manager starts', 'Guest userspace owner', 'Unit state and dependency logs', 'VM can be healthy while service fails'),
            ('Application accepts work', 'Application team', 'Bound port and synthetic response', 'Application success is above VM boot'),
            ('Evidence classified', 'Architecture team', 'Layer, source, timestamp, and confidence', 'Do not infer host state from guest logs')
        ],
        'A VM reaches the guest login prompt but the tax-adapter service fails because its module was built for a different guest kernel. The worksheet records successful virtual firmware, bootloader, and kernel stages, then isolates the module compatibility failure. The correction installs a matching test fixture and preserves the original failure log; it does not claim a hypervisor or physical-host defect.',
        'Guest boot and service logs demonstrate only the guest-visible sequence and bounded test outcome. They do not attest physical firmware, Google-managed hypervisor state, neighboring tenants, or production availability.'
    )
])

_container_expansions = ''.join([
    _worked_subtopic(
        'PID namespace initialization, signal, and reaping semantics',
        'A PID namespace gives processes a namespace-relative process identifier and process tree. The first process created in a new PID namespace becomes PID 1 for that namespace and has special responsibilities: it becomes the ancestor for orphaned descendants and must reap terminated children. Processes in an ancestor PID namespace can see descendants with different PID values, while a process cannot see into an ancestor namespace. Signal rules for namespace PID 1 are also special, so a container entrypoint that ignores or fails to forward termination signals can delay shutdown even when the application child is healthy.',
        'This mechanism connects runtime configuration to reliability. An architect should distinguish visibility from security: hiding host PIDs does not prevent a kernel exploit, while correct PID 1 behavior prevents zombie accumulation and supports graceful termination. Container images should use an entrypoint that execs the application or a minimal init that forwards signals and reaps children. Shutdown budgets, queue acknowledgement, and load-balancer draining must be coordinated with the application rather than inferred from the namespace boundary.',
        'In GKE or Cloud Run, the workload still needs correct process and signal handling inside its container execution environment. Platform termination signals and grace periods reach the container boundary, but the entrypoint determines whether application children receive them. Product-specific timeout and lifecycle values require current documentation; the general Linux rule is that namespace-relative PID 1 behavior remains part of the application image design.',
        [
            ('Create PID namespace', 'Runtime with required privilege', '<kbd>clone</kbd> or <kbd>unshare</kbd> result', 'Creation alone is not a security boundary'),
            ('Start namespace init', 'Container entrypoint', 'PID 1 inside namespace', 'Must handle signals and children'),
            ('Fork application child', 'Namespace PID 1', 'Child PID in namespace', 'Host may show a different PID'),
            ('Child exits', 'Guest process lifecycle', 'Zombie until reaped', 'Unreaped children consume PID table entries'),
            ('Termination requested', 'Orchestrator and runtime', 'Signal delivered to container process', 'Entrypoint may fail to forward it'),
            ('Application drains', 'Application', 'In-flight work and exit code', 'Timeout can force termination'),
            ('Namespace disappears', 'Kernel', 'Last process exits', 'Visibility scope ends'),
            ('Evidence saved', 'Operator', '<kbd>/proc/[pid]/status</kbd> and logs', 'PID mapping must name the observer namespace')
        ],
        'A worker shell remains PID 1 and launches the real service as a child. During shutdown the shell does not forward SIGTERM, so the service cannot checkpoint its queue offset before the grace period ends. Replacing the shell form with an exec-form entrypoint makes the service PID 1 and produces a clean bounded shutdown in the local replay.',
        'PID listings prove only the view from the observer’s namespace at that moment. They do not establish host compromise resistance, signal delivery outside the captured interval, or behavior on an untested GCP runtime.'
    ),
    _worked_subtopic(
        'Mount namespace propagation and filesystem boundary composition',
        'A mount namespace gives a process a private view of the mount table. Container runtimes assemble a root filesystem from image layers and writable storage, create bind mounts for declared inputs, and use pivot-root or an equivalent switch before executing the workload. Mount propagation controls whether later mount and unmount events cross a shared, slave, private, or unbindable relationship. The namespace changes path visibility; it does not automatically make a host path safe. A writable bind mount deliberately connects the container to an external filesystem object and can bypass assumptions made from the image alone.',
        'Architects must review every mount as a data and privilege boundary. Read-only flags reduce mutation but do not prevent disclosure. Host paths couple workloads to node layout and can expose sockets, device files, credentials, or runtime control interfaces. Persistent volumes add an external lifecycle and access-control plane. Image immutability, writable temporary space, secret projection, and backup ownership should be recorded separately. A mount error can arise from namespace assembly, permissions, storage attachment, or application paths, so diagnostics need evidence from each owner.',
        'GKE volumes and Cloud Run filesystem behavior are product contracts layered over Linux mount semantics. The design should use supported volume types and documented access modes rather than assuming arbitrary host mounts. The local namespace exercise can show path visibility and read-only behavior, but it cannot validate Google-managed node layout, storage attachment behavior, or multi-zone recovery.',
        [
            ('Resolve image layers', 'Image runtime', 'Image digest and layer metadata', 'Digest identifies content, not mounted state'),
            ('Create mount namespace', 'Container runtime', 'Namespace inode', 'New view may inherit propagation settings'),
            ('Assemble root filesystem', 'Runtime and storage driver', 'Mount table inside namespace', 'Layer or driver failure blocks start'),
            ('Attach declared volume', 'Runtime or CSI path', 'Mount source, target, and flags', 'Access mode and ownership can conflict'),
            ('Switch root', 'Runtime', 'Process root and current directory', 'Stale file descriptor may retain access'),
            ('Application opens path', 'Container process', 'File descriptor and errno', 'ENOENT, EACCES, and EROFS mean different failures'),
            ('Propagation event', 'Kernel mount subsystem', 'Change visible in related namespace', 'Unexpected shared propagation expands impact'),
            ('Unmount and cleanup', 'Runtime/storage owner', 'Released mount and attachment', 'Busy references delay cleanup')
        ],
        'A batch worker expects <kbd>/work</kbd> to be writable but the runtime mounts its input volume read-only. The application fails with EROFS. The fix creates a separate writable scratch mount and leaves the source data read-only; the worksheet records this as a mount-policy correction, not a cgroup or seccomp failure.',
        'A local mount table shows namespace-visible paths and flags. It does not prove storage durability, backend encryption, snapshot correctness, or the filesystem view of another container or GCP node.'
    ),
    _worked_subtopic(
        'Network namespace packet path and port ownership',
        'A network namespace owns interfaces, addresses, routing tables, neighbor tables, socket bindings, and firewall state. A runtime commonly creates a virtual Ethernet pair, leaves one endpoint in the workload namespace, attaches the peer to a host bridge or datapath, assigns routes, and configures forwarding or translation. A listening port belongs to the namespace in which the socket was created; publishing that port requires a separate host or platform routing decision. Loopback is also namespace-local, so two containers do not share localhost merely because they share a node.',
        'The packet path prevents common diagnostic mistakes. An application can listen correctly inside its namespace while the peer interface, route, firewall, service selector, or external load balancer remains wrong. Architects should trace source address, destination, route lookup, policy decision, translation, return path, and ownership at every hop. Network namespace isolation limits visibility and binding conflicts but still relies on the shared host kernel network stack unless an additional sandbox or VM boundary exists.',
        'GKE Pods intentionally share a network namespace among their containers, so sidecars communicate over localhost while different Pods receive distinct network identities. Services, policies, and Google Cloud load-balancing features add control planes outside the Linux namespace. The local veth trace teaches the kernel mechanism; it does not reproduce VPC, GKE dataplane, Cloud NAT, or load-balancer implementation details.',
        [
            ('Create network namespace', 'Runtime', 'Network namespace inode', 'Empty namespace has only local state'),
            ('Create veth pair', 'Runtime or CNI', 'Two linked interfaces', 'Missing peer prevents external path'),
            ('Move endpoint', 'Kernel namespace operation', 'Interface visible inside workload', 'Observer location changes interface names'),
            ('Assign address and route', 'CNI or network owner', 'Address and route tables', 'Wrong prefix or gateway breaks reachability'),
            ('Bind application socket', 'Workload process', 'Listening address and port', 'Binding loopback limits ingress scope'),
            ('Apply policy/forwarding', 'Host or platform datapath', 'Rule counters and decision', 'Drop is outside application listener'),
            ('Traverse external network', 'Cloud or physical network', 'Flow logs where available', 'Absence of logs is not proof of application failure'),
            ('Return packet', 'All path owners', 'Bidirectional trace', 'Asymmetric route can fail only response path')
        ],
        'A service listens on 127.0.0.1 inside its network namespace and passes an in-container curl test, but traffic from the namespace peer fails. Binding the service to the intended namespace interface fixes the local fixture. The worksheet distinguishes that listener scope from Kubernetes Service selection or cloud firewall behavior, which remain untested.',
        'Namespace interface and socket inspection establish the local packet path only. They do not prove VPC routing, external policy, load-balancer health, encryption, or connectivity on an untested GCP deployment.'
    ),
    _worked_subtopic(
        'IPC, UTS, and user namespace relationships',
        'IPC namespaces isolate System V IPC objects and POSIX message queues; UTS namespaces isolate hostname and domain-name values; user namespaces map user and group identifiers and scope many capability checks. These mechanisms solve different problems and can be combined independently. A process may appear as UID 0 inside a user namespace while mapping to an unprivileged identifier outside it. Capabilities gained in that namespace apply only where the kernel checks privilege relative to that namespace. The mapping therefore narrows host authority but does not convert every kernel interface or mounted object into a safe resource.',
        'Architects should treat namespace composition as a set of explicit contracts. Sharing an IPC namespace enables fast local coordination but expands interference and disclosure between the participants. A private UTS hostname aids identity but is not service discovery or authentication. User-ID mapping reduces the consequence of container root yet still requires safe mounts, device exposure, seccomp, and capability policy. Rootless operation changes the threat model and operational constraints; it does not guarantee that every workload feature remains available.',
        'Managed container products choose namespace and privilege configurations according to their service contracts. A local rootless-container observation can demonstrate UID mapping, but it cannot be generalized to Cloud Run or every GKE mode without product documentation. On GKE, Kubernetes security context fields express requested user and capability behavior while admission and runtime controls determine the effective result.',
        [
            ('Create user namespace', 'Runtime or unprivileged process', 'User namespace inode', 'Mapping files start constrained'),
            ('Write UID/GID maps', 'Authorized parent process', '<kbd>uid_map</kbd> and <kbd>gid_map</kbd>', 'Invalid range or permission fails setup'),
            ('Set namespaced identity', 'Kernel credentials', 'UID inside and outside namespace', 'Same numeric UID can mean different principals'),
            ('Create IPC namespace', 'Runtime', 'IPC namespace inode', 'Objects become visibility-scoped'),
            ('Create UTS namespace', 'Runtime', 'Namespace-local hostname', 'Hostname is not an authenticated identity'),
            ('Perform privileged operation', 'Kernel capability check', 'Effective capability and owning namespace', 'Capability may not apply to initial namespace'),
            ('Access mounted object', 'VFS and mount policy', 'Mapped ownership and mount permissions', 'Namespace mapping does not override all object policy'),
            ('Record effective boundary', 'Operator', 'Maps, capabilities, mounts, and runtime policy', 'One artifact alone is insufficient')
        ],
        'A rootless fixture reports UID 0 inside the user namespace and a subordinate host UID outside it. A write to an owned mapped directory succeeds, while a protected host path remains denied. The result demonstrates scoped identity mapping but is recorded alongside mount and capability evidence rather than labeled complete container security.',
        'UID maps and namespace inodes document identity translation and visibility. They do not prove absence of kernel vulnerabilities, safe host mounts, correct service authorization, or the namespace policy of an untested managed runtime.'
    ),
    _worked_subtopic(
        'cgroup v2 hierarchy, delegation, and CPU control',
        'cgroup v2 organizes processes in one hierarchy and enables controllers from parent to child. A child cannot escape a restriction imposed by an ancestor. Controllers are activated through <kbd>cgroup.subtree_control</kbd>, and process membership appears in <kbd>cgroup.procs</kbd>. CPU bandwidth control uses <kbd>cpu.max</kbd> as quota and period, while <kbd>cpu.weight</kbd> expresses proportional preference when siblings compete. A quota can throttle a busy workload even while another host CPU is idle if the cgroup has consumed its allowed bandwidth; weight matters only under contention and is not a guaranteed reservation.',
        'This distinction is central to resource architecture. Requests, limits, reservations, weights, and quotas are not interchangeable. Architects should inspect the effective hierarchy because parent policy, runtime-created slices, and workload-level settings compose. CPU throttling can increase request latency without producing an application exception. Raising a quota may hide inefficient concurrency, while removing it can harm neighbors. The decision requires service-level latency, runnable demand, throttling counters, and cost evidence.',
        'Kubernetes runtimes translate Pod and container resource settings into Linux controls according to the node operating system, cgroup mode, and runtime. GKE monitoring supplies container metrics, but the exact hierarchy and node configuration should be inspected or taken from current product documentation. This lesson avoids assuming one permanent path under <kbd>/sys/fs/cgroup</kbd> for every cluster version.',
        [
            ('Place process in leaf cgroup', 'Runtime or system manager', '<kbd>cgroup.procs</kbd>', 'Wrong membership invalidates later interpretation'),
            ('Enable controller in parent', 'Hierarchy owner', '<kbd>cgroup.subtree_control</kbd>', 'Child interface absent if controller unavailable'),
            ('Set CPU quota', 'Resource-policy owner', '<kbd>cpu.max</kbd>', 'Quota/period defines bounded bandwidth'),
            ('Set CPU weight', 'Resource-policy owner', '<kbd>cpu.weight</kbd>', 'Relative share acts only during competition'),
            ('Workload consumes quota', 'Kernel CPU controller', '<kbd>cpu.stat</kbd> usage counters', 'Execution remains normal until budget exhausted'),
            ('Throttle interval', 'Kernel scheduler/controller', 'Throttled periods and time', 'Latency rises without OOM or permission error'),
            ('Parent restriction applies', 'Ancestor cgroup owner', 'Effective ceiling from hierarchy', 'Child cannot override parent limit'),
            ('Tune and verify', 'Architect/application owner', 'Latency, throughput, throttling, and cost', 'Change one control and preserve baseline')
        ],
        'A worker uses one runnable CPU thread but <kbd>cpu.max</kbd> permits only half a CPU. Host dashboards show spare cores while <kbd>cpu.stat</kbd> records throttling. The worksheet classifies this as cgroup resource enforcement, tests a bounded quota change, and retains application-efficiency analysis as a separate decision.',
        'Cgroup files and a local load test show enforcement in that hierarchy. They do not prove Kubernetes translation, GKE node configuration, production traffic demand, or that CPU quota is the sole cause of an observed service incident.'
    ),
    _worked_subtopic(
        'cgroup memory control, reclaim, pressure, and OOM evidence',
        'The memory controller accounts charged memory to a cgroup and exposes current usage, events, pressure, and configured boundaries. <kbd>memory.high</kbd> is a throttling and reclaim boundary intended to apply pressure before a hard failure, while <kbd>memory.max</kbd> is a hard ceiling. When reclaim cannot satisfy an allocation under the hard boundary, the kernel can invoke cgroup-scoped out-of-memory handling and record events. Page cache, anonymous memory, kernel memory, child cgroups, and workload allocation patterns all influence the result; host free memory does not cancel a lower cgroup ceiling.',
        'Architects need more than a single exit code. Exit 137 can result from SIGKILL for several reasons, so the diagnosis should correlate termination reason, <kbd>memory.events</kbd>, working set, allocation profile, and timestamps. Raising the limit may restore availability but increases reservation and cost; streaming, batching, backpressure, and concurrency limits can reduce working set. Pressure-stall information can reveal degradation before an OOM kill. The exit artifact must label supplied counters separately from locally observed values.',
        'Kubernetes memory requests and limits are enforced through the node’s Linux runtime and cgroup configuration. GKE metrics can support workload-level analysis, but node paths and counter availability vary with the runtime and version. The local lab therefore discovers its cgroup membership instead of assuming the root <kbd>/sys/fs/cgroup</kbd> files always describe the current process.',
        [
            ('Charge allocation', 'Kernel memory controller', '<kbd>memory.current</kbd> and workload profile', 'Charge follows effective cgroup membership'),
            ('Cross high boundary', 'Kernel reclaim path', '<kbd>memory.events</kbd> high counter', 'Workload may slow before hard failure'),
            ('Attempt reclaim', 'Kernel VM subsystem', 'Pressure and reclaim activity', 'Reclaimable cache differs from anonymous memory'),
            ('Cross hard boundary', 'Memory controller', '<kbd>memory.max</kbd> context', 'Allocation cannot exceed effective ceiling'),
            ('Select victim', 'Cgroup OOM handling', 'OOM and oom_kill counters', 'Victim choice and group policy matter'),
            ('Process exits', 'Kernel and runtime', 'SIGKILL/exit status plus termination reason', 'Exit code alone is ambiguous'),
            ('Runtime restarts', 'Orchestrator policy', 'Restart count and new PID', 'Restart can hide recurring pressure'),
            ('Remediate and replay', 'Application/resource owner', 'Working set, events, latency, and cost', 'Verify bounded workload, not an invented production result')
        ],
        'The lab locates the current process cgroup, records <kbd>memory.max</kbd> and <kbd>memory.events</kbd>, and compares them with a supplied 512 MiB failure fixture. It marks local counters as observed and the fixture’s OOM increment as supplied. The worksheet evaluates streaming and a larger limit without claiming that either was deployed to GCP.',
        'A counter snapshot can associate an event with a cgroup only when membership and timestamps are preserved. It does not prove the application allocation site, production recurrence, host memory condition, or managed-platform configuration.'
    ),
    _worked_subtopic(
        'Seccomp and capability checks in the syscall path',
        'A container process enters the kernel through a system call. Seccomp can evaluate the syscall number, architecture, and selected arguments, then allow, reject, trap, log, or terminate according to its filter action. If the call continues, the target kernel subsystem performs ordinary credential, capability, namespace, object-permission, and Linux security module checks. Capabilities split portions of traditional root authority into bits evaluated relative to the governing user namespace and operation. Passing seccomp therefore does not grant permission, and holding a capability does not bypass a seccomp denial.',
        'This ordered model improves both policy design and diagnosis. An EPERM may come from a seccomp action, a missing capability, an object permission, an admission rule, or a read-only mount. A SIGSYS strongly suggests a trap or kill policy but still needs profile and audit evidence. Architects should start with runtime-default profiles, drop unnecessary capabilities, run as a non-root identity, and add only narrowly justified exceptions. Broad privileges such as privileged mode or CAP_SYS_ADMIN enlarge the consequence of a compromise and must not be used merely to silence an unexplained failure.',
        'GKE Autopilot and Standard modes have documented differences in how runtime-default seccomp profiles are applied, and GKE Sandbox changes the isolation boundary. Those product behaviors must be taken from the current GKE seccomp and security documentation. The Linux mechanism remains the same diagnostic sequence: identify the effective profile, capability sets, user namespace, target object, and returned errno or signal.',
        [
            ('Issue syscall', 'Container process', 'Syscall trace in a bounded test', 'Name architecture and arguments where relevant'),
            ('Evaluate seccomp filter', 'Kernel seccomp subsystem', 'Effective mode/profile and audit event', 'Deny can return errno, trap, or kill'),
            ('Resolve credentials', 'Kernel credential model', 'UID/GID and user namespace', 'Namespace-relative root is scoped'),
            ('Check capability', 'Target kernel subsystem', 'Effective and bounding capability sets', 'Missing bit yields permission failure'),
            ('Check object policy', 'VFS/network/device subsystem', 'Mode, ACL, mount, or device policy', 'Capability is not universal bypass'),
            ('Apply security module', 'LSM policy owner', 'Audit record where available', 'Separate policy layer may deny'),
            ('Execute operation', 'Kernel subsystem', 'Return value and side effect', 'Success proves only this invocation'),
            ('Record decision', 'Security/architecture owner', 'Profile, capabilities, identity, errno, and scope', 'Avoid granting broad privilege without cause')
        ],
        'A fixture attempts a mount syscall. The runtime profile denies it and the process also lacks CAP_SYS_ADMIN. The worksheet records both controls, then tests an unrelated permitted syscall. It does not recommend privileged mode, because removing both controls would expand host impact without satisfying a justified workload requirement.',
        'A local syscall result and process status show the effective controls for that process and invocation. They do not prove the absence of kernel vulnerabilities, the profile of another workload, or the policy applied by an untested GKE or Cloud Run environment.'
    ),
    _worked_subtopic(
        'Composing a container isolation claim from independent controls',
        'A defensible container-isolation statement is assembled from independent facts, not from the word container. Namespace evidence describes visibility and identity scopes. Cgroup evidence describes resource accounting and enforcement. Seccomp evidence describes the system-call policy. Capability and credential evidence describe privileged operations available to the process. Mount and network evidence describe intentionally exposed resources. A sandbox or virtual machine can add a separate kernel boundary. Each mechanism has a different owner, failure signal, and bypass consequence, so the final worksheet must state exactly which controls were inspected and which remain assumptions.',
        'Architects use this composition to avoid two opposite mistakes: treating resource limits as complete security, or rejecting containers because they are not virtual machines. A trusted stateless service may be appropriately protected by a shared-kernel runtime with least privilege and strong policy. Hostile customer code may require a sandbox, dedicated node, or VM. The decision depends on attacker capability, data sensitivity, kernel exposure, operational recovery, cost, density, and product support. A single successful probe cannot replace threat modeling or acceptance criteria.',
        'On GCP the available boundary can include standard GKE containers, GKE Sandbox, Cloud Run execution environments, or Compute Engine VMs. The architecture record must use current product documentation for the selected mode and must distinguish requested Kubernetes security context from effective runtime policy. The local lab supplies process-level observations only; it leaves managed-host controls and production behavior explicitly untested.',
        [
            ('Record process identity', 'Workload/runtime', 'UID, GID, user namespace, capability sets', 'Identity is scoped, not universal authority'),
            ('Record namespace set', 'Kernel/runtime', 'Namespace inodes and membership', 'Visibility does not equal resource control'),
            ('Record cgroup membership', 'Runtime/resource owner', 'Effective path, controllers, limits, events', 'Limits do not block kernel exploits'),
            ('Record syscall policy', 'Runtime/security owner', 'Seccomp mode and profile evidence', 'Allowed call still faces other checks'),
            ('Record exposed resources', 'Platform/application owner', 'Mounts, devices, sockets, and network routes', 'Exposure can bypass an assumed boundary'),
            ('Identify kernel boundary', 'Architecture owner', 'Shared kernel, sandbox kernel, or guest kernel', 'Name the actual selected runtime'),
            ('Test bounded failure', 'Lab operator', 'Expected denial, throttle, or termination evidence', 'Failure type identifies the enforcing control'),
            ('State residual risk', 'Security and service owners', 'Unknowns, untested GCP behavior, and recovery plan', 'Acceptance requires explicit limits')
        ],
        'The completed worksheet records a private PID namespace, a finite memory limit, seccomp filter mode 2, and a capability mask that omits CAP_SYS_MODULE. It classifies the memory ceiling as resource enforcement and the syscall/capability controls as attack-surface reduction, while noting that all observed calls still enter the same local host kernel. The placement decision can now justify a VM or sandbox for untrusted code without overstating the local evidence.',
        'The composed claim is only as strong as its captured inputs and scope. It does not prove the absence of kernel defects, the configuration of an unobserved runtime, the GCP host boundary, or production acceptance.'
    )
])

_t0['technical'] = _t0['technical'].replace(
    '<p><strong class="side-heading">Evidence limit:</strong>',
    _vm_expansions + '<p><strong class="side-heading">Evidence limit:</strong>',
    1
)
_t1['technical'] = _t1['technical'].replace(
    '<p><strong class="side-heading">Evidence limit:</strong>',
    _container_expansions + '<p><strong class="side-heading">Evidence limit:</strong>',
    1
)

# 3. R2 Bullets Conversion Function (preserves structural headings like Evidence limit and Subtopics)
def _convert_to_r2_bullets(tech_html):
    def repl_p(m):
        label = m.group(1)
        rest = m.group(2)
        if label.strip() in ('Evidence limit:', 'Subtopics in this discussion:', 'Linked subtopics:'):
            return m.group(0)
        return f'<li><strong class="side-heading">{label}</strong>{rest}</li>'
    s = re.sub(r'<p><strong class="side-heading">(.*?)</strong>(.*?)</p>', repl_p, tech_html, flags=re.DOTALL)
    
    parts = re.split(r'(<h4[^>]*>.*?</h4>|<figure.*?</figure>|<div.*?</div>|<p.*?</p>|<ul>.*?</ul>)', s, flags=re.DOTALL)
    out = []
    for part in parts:
        if not part:
            continue
        if part.startswith(('<h4', '<figure', '<div', '<p', '<ul')):
            out.append(part)
        else:
            trimmed = part.strip()
            if trimmed.startswith('<li>'):
                out.append('<ul>\n' + trimmed + '\n</ul>')
            else:
                out.append(part)
    return '\n\n'.join(out)

for _topic in DATA['topics']:
    _topic['technical'] = _convert_to_r2_bullets(_topic['technical'])

# 4. Link all <strong class="keyword"> spans (put <a> inside <strong>)
def _link_keywords(html_text):
    def _repl(m):
        inner = m.group(1)
        if '<a ' in inner:
            return m.group(0)
        clean_text = re.sub(r'<[^>]+>', '', inner).strip()
        search_url = 'http://www.google.com/search?q=' + urllib.parse.quote_plus(clean_text)
        return '<strong class="keyword"><a href="' + search_url + '" rel="noopener" target="_blank">' + inner + '</a></strong>'
    return re.sub(r'<strong class="keyword">(.*?)</strong>', _repl, html_text)

for _topic in DATA['topics']:
    _topic['technical'] = _link_keywords(_topic['technical'])
DATA['part1_html'] = _link_keywords(DATA['part1_html'])

# 5. Link Listed Terms (first occurrence per subtopic/card)
def _link_terms_in_section(text, terms_list=TERMS):
    soup = BeautifulSoup(f'<root>{text}</root>', 'html.parser')
    for term in terms_list:
        pat = re.compile(r'(?<!\w)(' + re.escape(term) + r')(?!\w)', re.IGNORECASE)
        url = f'http://www.google.com/search?q={urllib.parse.quote_plus(term)}'
        matched = False
        for text_node in list(soup.find_all(string=True)):
            if matched:
                break
            parent = text_node.parent
            in_forbidden = False
            while parent and parent.name != '[document]':
                if parent.name in ('a', 'code', 'kbd', 'samp', 'figcaption', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title', 'script', 'style'):
                    in_forbidden = True
                    break
                if parent.name == 'strong' and 'side-heading' in parent.get('class', []):
                    in_forbidden = True
                    break
                if parent.name == 'strong' and 'keyword' in parent.get('class', []):
                    if parent.find('a'):
                        in_forbidden = True
                        break
                parent = parent.parent
            if in_forbidden:
                continue
            m = pat.search(text_node)
            if m:
                before = text_node[:m.start()]
                matched_text = m.group(1)
                after = text_node[m.end():]
                a_tag = soup.new_tag('a', href=url, rel='noopener', target='_blank')
                a_tag.string = matched_text
                new_nodes = []
                if before:
                    new_nodes.append(NavigableString(before))
                new_nodes.append(a_tag)
                if after:
                    new_nodes.append(NavigableString(after))
                text_node.replace_with(*new_nodes)
                matched = True
    return soup.root.decode_contents()

# Link terms in part1_html overview cards
_cards = re.split(r'(</article>)', DATA['part1_html'])
_new_part1 = []
for _part in _cards:
    if '<article' in _part:
        _new_part1.append(_link_terms_in_section(_part))
    else:
        _new_part1.append(_part)
DATA['part1_html'] = ''.join(_new_part1)

# 6. Assign Subtopic IDs and Link Subtopics
for _topic in DATA['topics']:
    _technical = _topic['technical']
    _headings = re.findall(r'<h4>(.*?)</h4>', _technical, re.S)
    _links = []
    for _number, _heading in enumerate(_headings, 1):
        _anchor = f"{_topic['key']}-subtopic-{_number:02d}"
        _technical = _technical.replace(
            '<h4>' + _heading + '</h4>',
            f'<h4 id="{_anchor}">' + _heading + '</h4>', 1
        )
        _links.append(f'<li><a href="#{_anchor}">{_heading}</a></li>')
    _linked_list = '<ul>' + ''.join(_links) + '</ul>'
    _technical = re.sub(
        r'(<p><strong class="side-heading">Subtopics in this discussion:</strong></p>)\s*<ol>.*?</ol>',
        lambda match: match.group(1) + _linked_list,
        _technical, count=1, flags=re.S
    )
    
    # Link terms in technical subtopics
    _parts = re.split(r'(<h4[^>]*>.*?</h4>)', _technical)
    _new_tech = []
    for _p in _parts:
        if '<h4' in _p:
            _new_tech.append(_p)
        else:
            _new_tech.append(_link_terms_in_section(_p))
    _technical = ''.join(_new_tech)

    # Append Keyword searches discovery aid list at end of technical discussion
    if 'Keyword searches' not in _technical:
        _disc_links = ''.join(f'<li><a href="http://www.google.com/search?q={urllib.parse.quote_plus(t)}" rel="noopener" target="_blank">{t}</a> — discovery aid</li>' for t in TERMS)
        _technical += f'<div><strong>Keyword searches</strong></div><ul>{_disc_links}</ul>'

    _topic['technical'] = _technical

    _topic_key = _topic['key']
    _nav_links = f'<p><a href="#{_topic_key}-technical">Technical discussion →</a> <a href="#{_topic_key}-problem">Real-world problem →</a> <a href="#{_topic_key}-lab">Step-by-step lab →</a></p>'
    _card_pat = r'(<article class="topic-card overview" id="' + _topic_key + r'-overview">.*?)(</article>)'
    DATA['part1_html'] = re.sub(
        _card_pat,
        lambda m: m.group(1) + '<p><strong class="side-heading">Linked subtopics:</strong></p>' + _linked_list + '\n' + _nav_links + '\n' + m.group(2),
        DATA['part1_html'], count=1, flags=re.S
    )

DATA['review_records'] = {
    'source_ledger': {
        'https://docs.kernel.org/virt/kvm/api.html#general-description': {
            'heading_opened': '1. General description',
            'rfc_status': 'not applicable'
        },
        'https://docs.kernel.org/admin-guide/cgroup-v2.html#introduction': {
            'heading_opened': 'Introduction',
            'rfc_status': 'not applicable'
        }
    },
    'product_claims': [
        {
            'claim': 'The KVM API is centered on file descriptors and ioctls, beginning with an open of /dev/kvm.',
            'section_url': 'https://docs.kernel.org/virt/kvm/api.html#general-description',
            'heading_opened': '1. General description'
        },
        {
            'claim': 'KVM_CREATE_VM returns a virtual-machine file descriptor used for VM-specific ioctls.',
            'section_url': 'https://docs.kernel.org/virt/kvm/api.html#general-description',
            'heading_opened': '1. General description'
        },
        {
            'claim': 'cgroup organizes processes hierarchically and distributes system resources through controllers whose restrictions apply down the hierarchy.',
            'section_url': 'https://docs.kernel.org/admin-guide/cgroup-v2.html#introduction',
            'heading_opened': 'Introduction'
        }
    ],
    'visual_reasons': {
        'Day 9: Hardware-Assisted Hypervisor and Kernel Namespace Isolation Architecture': 'Repositioned probe element P1 and cleared node border margins to satisfy R4 clearance requirements.',
        'Virtual machine and container isolation boundaries': 'Adjusted text element baseline coordinates and verified 9px minimum font threshold under R4 and R8.',
        'Linux kernel container isolation layers and syscall evaluation': 'Centered subsystem icons at y=36 and text labels at y=76 across all five columns to eliminate text collisions under R4.',
        'Tax adapter placement failure and corrected VM path': 'Widened node boxes, updated return label to insmod: EPERM (Denied), and adjusted connector arrows to eliminate box/text collisions under R4.',
        'Fulfillment worker cgroup memory failure and streaming control fix': 'Shortened badge label to [CORRECTED: Streamed], widened verification node, and adjusted text coordinates to clear text overlaps under R4.'
    }
}
