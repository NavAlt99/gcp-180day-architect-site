#!/usr/bin/env python3
"""Assembler script to generate scratch/day_data_009.py."""
import sys
import pprint
from pathlib import Path

# Add scratch to path
sys.path.insert(0, str(Path("scratch").resolve()))

import day_009_part1
import day_009_part2
import day_009_scenarios_labs

# Import base module variables
from generate_day_009 import (
    ACCESS_DATE, SOURCES, FIG_9_1_HTML, FIG_9_2_HTML, FIG_9_3_HTML, FIG_9_4_HTML,
    PART1_HTML, ARCH_DIAGRAM
)

COMPLETION_HTML = '''<div class="completion-box" id="completion-box-009">
<h3>Day 9 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-9-1"> <label for="check-9-1">Hypervisors mastered: Type 1 bare-metal vs Type 2 hosted, hardware-assisted virtualization (VT-x/AMD-V, EPT), and KVM/QEMU architecture.</label></li>
<li><input type="checkbox" id="check-9-2"> <label for="check-9-2">Guest kernel autonomy understood: sovereign guest OS kernel space, custom module loading (<kbd>insmod</kbd>), and hypervisor memory overhead.</label></li>
<li><input type="checkbox" id="check-9-3"> <label for="check-9-3">Container isolation mechanisms mapped: namespaces (visibility), cgroups v2 (resource quota), seccomp (system call filter), and POSIX capabilities.</label></li>
<li><input type="checkbox" id="check-9-4"> <label for="check-9-4">Resource enforcement distinguished from security: why cgroup memory/CPU limits and private namespaces do not prevent kernel privilege escalation exploits.</label></li>
<li><input type="checkbox" id="check-9-5"> <label for="check-9-5">Exit evidence verified: compiled the isolation worksheet distinguishing resource enforcement from security isolation.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-009" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 9 Completed':'Mark Day 9 as Read';">Mark Day 9 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-009" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''

t1_tech = day_009_part1.TOPIC_01_TECH.replace('{FIG_9_1_HTML}', FIG_9_1_HTML)
t2_tech = day_009_part2.TOPIC_02_TECH.replace('{FIG_9_2_HTML}', FIG_9_2_HTML)

s1_scenario = {**day_009_scenarios_labs.SCENARIOS_AND_LABS['topic-01']['scenario']}
s1_scenario['evidence'] = s1_scenario['evidence'] + '\n\n' + FIG_9_3_HTML

s2_scenario = {**day_009_scenarios_labs.SCENARIOS_AND_LABS['topic-02']['scenario']}
s2_scenario['evidence'] = s2_scenario['evidence'] + '\n\n' + FIG_9_4_HTML

topics = [
    {
        'key': 'topic-01',
        'title': 'Hypervisors and virtual machines',
        'anchors': {
            'overview': 'topic-01-overview',
            'technical': 'topic-01-technical',
            'problem': 'topic-01-problem',
            'lab': 'topic-01-lab'
        },
        'overview': (
            'Virtual machine isolation relies on hardware-assisted virtualization extensions where a hypervisor '
            'intercepts privileged CPU operations and virtualizes physical memory through Extended Page Tables (EPT), '
            'granting each guest operating system a completely sovereign kernel space. In contrast to containers that '
            'multiplex a single shared kernel, a virtual machine provides an impenetrable cryptographic and architectural '
            'isolation boundary backed by independent virtual hardware registers, device emulators, and guest drivers.'
        ),
        'preview': (
            'A third-party enterprise tax calculator requires a proprietary kernel module that fails to load on a '
            'shared container cluster due to dropped module insertion privileges. The team migrates the workload to '
            'a dedicated Compute Engine virtual machine running a vendor-certified guest kernel, restoring transaction '
            'processing without compromising host node security.'
        ),
        'technical': t1_tech,
        'questions': [
            'How does hardware-assisted virtualization (Intel VT-x / AMD-V) eliminate Popek-Goldberg virtualization anomalies without binary translation?',
            'Under what circumstances does guest kernel autonomy dictate choosing a Compute Engine VM over a Kubernetes container runtime?',
            'What architectural threat vectors exist when userspace device emulation (QEMU/VMM) mediates I/O between guest kernels and physical host hardware?'
        ],
        'reference': 'https://docs.kernel.org/virt/kvm/api.html#general-description',
        'reference_label': f'Linux Kernel KVM API General Description (accessed {ACCESS_DATE})',
        'scenario': s1_scenario,
        'lab': day_009_scenarios_labs.SCENARIOS_AND_LABS['topic-01']['lab']
    },
    {
        'key': 'topic-02',
        'title': 'Container isolation',
        'anchors': {
            'overview': 'topic-02-overview',
            'technical': 'topic-02-technical',
            'problem': 'topic-02-problem',
            'lab': 'topic-02-lab'
        },
        'overview': (
            'Linux container isolation is not a physical or hardware boundary, but an orchestration of four discrete '
            'Linux kernel subsystems: namespaces that restrict visibility, control groups (cgroups v2) that govern '
            'resource consumption, seccomp-BPF filters that restrict allowable system calls, and POSIX capabilities '
            'that fragment root privileges. Because containerized processes execute system calls directly on the shared '
            'host Linux kernel, misconfigurations in any single layer can expose the entire host node to compromise '
            'or resource starvation.'
        ),
        'preview': (
            'A fulfillment worker service intermittently crashes with exit code 137 during batch invoicing despite '
            'monitoring dashboards displaying abundant free physical memory on the host server. Inspecting the container '
            'runtime reveals that the application breached its isolated cgroup memory limit during memory-intensive '
            'PDF generation, triggering a local kernel Out-Of-Memory termination.'
        ),
        'technical': t2_tech,
        'questions': [
            'Why do Linux kernel namespaces provide visibility partitioning rather than security boundary containment?',
            'How does cgroups v2 memory.max enforcement trigger process termination independently of host-level physical RAM availability?',
            'In what ways do seccomp-BPF filters and dropped POSIX capabilities reduce kernel attack surfaces for containerized root processes?'
        ],
        'reference': 'https://man7.org/linux/man-pages/man7/namespaces.7.html#DESCRIPTION',
        'reference_label': f'namespaces(7) Linux namespaces overview description (accessed {ACCESS_DATE})',
        'scenario': s2_scenario,
        'lab': day_009_scenarios_labs.SCENARIOS_AND_LABS['topic-02']['lab']
    }
]

DATA = {
    'contract_version': 2,
    'roadmap_practice': "Inspect a local container's namespaces, cgroup limits and user identity; compare its isolation boundary with a VM diagram.",
    'roadmap_exit': "An isolation worksheet distinguishing resource enforcement from security isolation.",
    'day': 9,
    'work_block': 'Days 1–17 — Foundations',
    'part1_html': PART1_HTML,
    'part1_intro': (
        'Day 9 explores the fundamental isolation boundaries dividing compute workloads in cloud architectures: '
        'hardware-assisted hypervisors and virtual machines versus Linux kernel container isolation subsystems '
        '(namespaces, cgroups v2, seccomp, and POSIX capabilities).'
    ),
    'part2_intro': (
        'Analyze the kernel mechanics governing hardware-assisted CPU virtualization (VT-x/EPT), KVM hypervisors, '
        'Linux namespace visibility partitioning, cgroups v2 resource accounting, seccomp BPF filtering, and sandboxing.'
    ),
    'part3_intro': (
        'Real-world architectural failure cases demonstrating container module insertion denial on immutable nodes '
        'and silent container OOM terminations occurring despite ample host physical memory headroom.'
    ),
    'part4_intro': (
        'Hands-on operational exercises to evaluate workload kernel dependencies, inspect live Linux process namespaces '
        'and cgroup controllers, and compile a comprehensive isolation worksheet distinguishing resource enforcement '
        'from security isolation.'
    ),
    'exit_summary': (
        'A comprehensive isolation comparison worksheet distinguishing resource enforcement from security isolation, '
        'validating that namespaces control visibility, cgroups v2 enforce quotas, and seccomp/capabilities restrict '
        'kernel attack surfaces.'
    ),
    'completion_html': COMPLETION_HTML,
    'arch_diagram': ARCH_DIAGRAM,
    'access_date': ACCESS_DATE,
    'sources': SOURCES,
    'topics': topics
}

with open("scratch/day_data_009.py", "w") as f:
    f.write(f'"""Durable data specification for Day 9: VM and container isolation."""\n\n')
    f.write(f'ACCESS_DATE = {repr(ACCESS_DATE)}\n\n')
    f.write(f'SOURCES = {repr(SOURCES)}\n\n')
    f.write(f'DATA = ')
    pprint.pprint(DATA, stream=f, indent=2, width=120)
    f.write('\n')

print("Successfully generated scratch/day_data_009.py")

