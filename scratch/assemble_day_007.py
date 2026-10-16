#!/usr/bin/env python3
"""Assembler script to generate scratch/day_data_007.py."""
import sys
import pprint
from pathlib import Path

# Add scratch to path
sys.path.insert(0, str(Path("scratch").resolve()))

import day_007_part1
import day_007_part2
import day_007_part3
import day_007_part4
import day_007_scenarios_labs

# Import base module variables
from generate_day_007 import (
    ACCESS_DATE, SOURCES, FIG_7_1_HTML, FIG_7_2_HTML, FIG_7_3_HTML, FIG_7_4_HTML,
    FIG_7_5_HTML, FIG_7_6_HTML, FIG_7_7_HTML, FIG_7_8_HTML,
    PART1_HTML, ARCH_DIAGRAM
)

COMPLETION_HTML = '''<div class="completion-box" id="completion-box-007">
<h3>Day 7 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-7-1"> <label for="check-7-1">SSH configuration mastered: key permissions (0600), ProxyJump stanzas, connection multiplexing, and disabling insecure agent forwarding.</label></li>
<li><input type="checkbox" id="check-7-2"> <label for="check-7-2">Package management verified: deb/rpm metadata verification, GPG signature checking, and golden immutable images over fragile runtime installs.</label></li>
<li><input type="checkbox" id="check-7-3"> <label for="check-7-3">Shell scripting hardened: set -euo pipefail, strict double-quoting preventing word splitting, explicit exit codes (0, 2, 3), and zero stored credentials.</label></li>
<li><input type="checkbox" id="check-7-4"> <label for="check-7-4">/proc inspection demonstrated: VFS zero-block allocation, process status and memory telemetry, process tree parentage, and open/deleted file descriptor diagnostics.</label></li>
<li><input type="checkbox" id="check-7-5"> <label for="check-7-5">Practice completed: inspected SSH configuration; executed hardened JSON parsing script with successful and explicit failure runs, quoting explained, and no stored credentials.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-007" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 7 Completed':'Mark Day 7 as Read';">Mark Day 7 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-007" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''

t1_tech = day_007_part1.TOPIC_01_TECH.replace('{FIG_7_1_HTML}', FIG_7_1_HTML)
t2_tech = day_007_part2.TOPIC_02_TECH.replace('{FIG_7_2_HTML}', FIG_7_2_HTML)
t3_tech = day_007_part3.TOPIC_03_TECH.replace('{FIG_7_3_HTML}', FIG_7_3_HTML)
t4_tech = day_007_part4.TOPIC_04_TECH.replace('{FIG_7_4_HTML}', FIG_7_4_HTML)

s1_scenario = {**day_007_scenarios_labs.SCENARIOS_AND_LABS['topic-01']['scenario']}
s1_scenario['evidence'] = s1_scenario['evidence'] + '\n\n' + FIG_7_5_HTML

s2_scenario = {**day_007_scenarios_labs.SCENARIOS_AND_LABS['topic-02']['scenario']}
s2_scenario['evidence'] = s2_scenario['evidence'] + '\n\n' + FIG_7_6_HTML

s3_scenario = {**day_007_scenarios_labs.SCENARIOS_AND_LABS['topic-03']['scenario']}
s3_scenario['evidence'] = s3_scenario['evidence'] + '\n\n' + FIG_7_7_HTML

s4_scenario = {**day_007_scenarios_labs.SCENARIOS_AND_LABS['topic-04']['scenario']}
s4_scenario['evidence'] = s4_scenario['evidence'] + '\n\n' + FIG_7_8_HTML

topics = [
    {
        'key': 'topic-01',
        'title': 'SSH',
        'anchors': {
            'overview': 'topic-01-overview',
            'technical': 'topic-01-technical',
            'problem': 'topic-01-problem',
            'lab': 'topic-01-lab'
        },
        'overview': 'Secure Shell establishes encrypted, cryptographically authenticated remote transport tunnels. Beyond terminal access, SSH underpins enterprise cloud access architectures through asymmetric key pairs, configuration profiles, dynamic port forwarding, and multi-hop bastion jump proxies.',
        'preview': 'An administrative engineer enabling SSH agent forwarding across a shared staging jump host exposes their decrypted private key credentials to local root users on the bastion. Rogue operators on the compromised jump host hijack the forwarded socket to authenticate to high-security production database instances.',
        'technical': t1_tech,
        'questions': [
            'Why does SSH agent forwarding (-A) represent a critical lateral movement vulnerability on multi-tenant or shared perimeter jump boxes?',
            'How does OpenSSH ProxyJump (-J) maintain end-to-end cryptographic confidentiality between the client and destination compared to interactive bastion logins?',
            'Under what conditions should cloud architects choose Compute Engine OS Login and IAP TCP forwarding over self-managed SSH key metadata?'
        ],
        'reference': 'https://man7.org/linux/man-pages/man5/ssh_config.5.html#DESCRIPTION',
        'reference_label': 'ssh_config(5) OpenSSH client configuration description (accessed 2026-10-04)',
        'scenario': s1_scenario,
        'lab': day_007_scenarios_labs.SCENARIOS_AND_LABS['topic-01']['lab']
    },
    {
        'key': 'topic-02',
        'title': 'Package managers (apt, yum/dnf)',
        'anchors': {
            'overview': 'topic-02-overview',
            'technical': 'topic-02-technical',
            'problem': 'topic-02-problem',
            'lab': 'topic-02-lab'
        },
        'overview': 'Package managers automate software delivery, dependency resolution, and cryptographically verified installation across Linux distributions. Tools query repository metadata, verify detached GPG signatures, and track system state in transactional databases.',
        'preview': 'A production provisioning automation script fails during an auto-scaling event because an upstream third-party repository GPG key expired, halting system updates. The failed package manager transaction blocks VM startup, preventing replacement web server instances from handling incoming peak traffic.',
        'technical': t2_tech,
        'questions': [
            'Why does relying on runtime package installations in VM startup scripts create critical availability and determinism risks during auto-scaling events?',
            'How do package managers verify release metadata integrity using detached GPG signatures, and what is the security impact of setting trusted=yes in repository declarations?',
            'What architectural advantages do immutable pre-baked golden images (HashiCorp Packer) offer over dynamic runtime package management in enterprise cloud environments?'
        ],
        'reference': 'https://man7.org/linux/man-pages/man8/rpm.8.html#DESCRIPTION',
        'reference_label': 'rpm(8) package manager description (accessed 2026-10-04)',
        'scenario': s2_scenario,
        'lab': day_007_scenarios_labs.SCENARIOS_AND_LABS['topic-02']['lab']
    },
    {
        'key': 'topic-03',
        'title': 'Shell scripting',
        'anchors': {
            'overview': 'topic-03-overview',
            'technical': 'topic-03-technical',
            'problem': 'topic-03-problem',
            'lab': 'topic-03-lab'
        },
        'overview': 'Shell scripting orchestrates operating system commands, data streams, and execution control flow into automated administrative tools and deployment pipelines. Mastering variable quoting, control loops, conditionals, signal handling, and exit code propagation prevents silent execution failures.',
        'preview': 'An unquoted variable in an automated backup cleanup script subjects filenames with spaces to shell word splitting, executing recursive file deletion against unintended root directories. The resulting filesystem truncation destroys customer application configuration state across multiple service mount points.',
        'technical': t3_tech,
        'questions': [
            'How does bash word splitting on unquoted variables introduce both catastrophic filesystem destruction defects and security injection vulnerabilities?',
            'Why is set -o pipefail required in automated deployment pipelines, and how does standard pipeline exit status behavior mask upstream compilation or security scanner failures?',
            'What are the failure modes of using regex text manipulation to parse JSON payloads in shell scripts, and why should architects delegate schema validation to dedicated tools like python3 or jq?'
        ],
        'reference': 'https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION',
        'reference_label': 'bash(1) GNU Bourne-Again SHell description (accessed 2026-10-04)',
        'scenario': s3_scenario,
        'lab': day_007_scenarios_labs.SCENARIOS_AND_LABS['topic-03']['lab']
    },
    {
        'key': 'topic-04',
        'title': '/proc virtual filesystem and process trees',
        'anchors': {
            'overview': 'topic-04-overview',
            'technical': 'topic-04-technical',
            'problem': 'topic-04-problem',
            'lab': 'topic-04-lab'
        },
        'overview': 'The /proc filesystem is a pseudo-filesystem generated dynamically by the Linux kernel in virtual memory to expose real-time process metadata, memory allocations, open file descriptors, and hardware telemetry. Process trees maintain parent-child ancestry, enabling operators to trace service lineages and diagnose workloads.',
        'preview': 'An unmonitored batch worker process deleted its primary multi-gigabyte log file from disk while retaining an active file descriptor, causing the VM root disk to reach 100% capacity despite du reporting free space. Application database transactions freeze due to disk exhaustion because the kernel refuses to reclaim unlinked inode blocks until the owning process terminates.',
        'technical': t4_tech,
        'questions': [
            'Why does unlinking a multi-gigabyte file with rm fail to reclaim disk space if an active process maintains an open file descriptor to the inode?',
            'How can system operators diagnose and remediate 100% disk utilization caused by unlinked open file descriptors online without rebooting the VM or killing the process?',
            'What security risks are introduced by passing database credentials or API secrets as process environment variables visible in /proc/[pid]/environ?'
        ],
        'reference': 'https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION',
        'reference_label': 'proc(5) process information pseudo-filesystem description (accessed 2026-10-04)',
        'scenario': s4_scenario,
        'lab': day_007_scenarios_labs.SCENARIOS_AND_LABS['topic-04']['lab']
    }
]

DATA = {
    'contract_version': 2,
    'roadmap_practice': 'Use a local test VM to inspect SSH configuration; write a small script that parses synthetic JSON and fails explicitly on invalid input.',
    'roadmap_exit': 'A script with successful and failed runs, quoting explained, and no stored credentials.',
    'day': 7,
    'work_block': 'Days 1–17 — Foundations',
    'part1_html': PART1_HTML,
    'part1_intro': 'Day 7 explores core Linux systems administration, automation, and diagnostic primitives: SSH cryptographic boundaries, distribution package managers, defensive shell scripting, and the /proc virtual filesystem.',
    'part2_intro': 'Examine the operational mechanisms, cryptographic handshakes, and diagnostic interfaces governing remote access, software packaging, shell execution, and kernel process state.',
    'part3_intro': 'Real-world architectural failure cases demonstrating agent forwarding socket hijacking, expired package signing keys, unquoted variable word splitting, and unlinked open file descriptor leaks.',
    'part4_intro': 'Hands-on operational exercises and verification workflows to configure SSH profiles, inspect package databases, author defensive JSON parsing scripts, and navigate the /proc filesystem.',
    'exit_summary': 'A verified defensive shell script demonstrating successful and failed JSON parsing runs, strict variable quoting, zero stored credentials, and an execution evidence report.',
    'completion_html': COMPLETION_HTML,
    'arch_diagram': ARCH_DIAGRAM,
    'arch_svg_html': '',
    'arch_table_html': '',
    'lab_defaults': {},
    'topics': topics
}

# Write out to scratch/day_data_007.py
out_path = Path("scratch/day_data_007.py")
with open(out_path, "w", encoding="utf-8") as f:
    f.write('"""Durable data specification for Day 7: SSH, scripts and process inspection."""\n\n')
    f.write(f'ACCESS_DATE = {repr(ACCESS_DATE)}\n\n')
    f.write(f'SOURCES = {repr(SOURCES)}\n\n')
    f.write(f'DATA = ')
    f.write(pprint.pformat(DATA, width=120, sort_dicts=False))
    f.write('\n')

print(f"Successfully assembled {out_path} ({out_path.stat().st_size} bytes)")
