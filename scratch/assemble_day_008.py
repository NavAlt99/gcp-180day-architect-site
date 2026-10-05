#!/usr/bin/env python3
"""Assembler script to generate scratch/day_data_008.py."""
import sys
import pprint
from pathlib import Path

# Add scratch to path
sys.path.insert(0, str(Path("scratch").resolve()))

import day_008_part1
import day_008_part2
import day_008_scenarios_labs

# Import base module variables
from generate_day_008 import (
    ACCESS_DATE, SOURCES, FIG_8_1_HTML, FIG_8_2_HTML, FIG_8_3_HTML, FIG_8_4_HTML,
    PART1_HTML, ARCH_DIAGRAM
)

COMPLETION_HTML = '''<div class="completion-box" id="completion-box-008">
<h3>Day 8 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-8-1"> <label for="check-8-1">CPU scheduling mastered: Completely Fair Scheduler run queues, voluntary vs involuntary context switching, and CPU quota throttling.</label></li>
<li><input type="checkbox" id="check-8-2"> <label for="check-8-2">Virtual memory &amp; page cache understood: minor vs major page faults, MemAvailable vs MemFree, dirty writeback, and swap mechanics.</label></li>
<li><input type="checkbox" id="check-8-3"> <label for="check-8-3">OOM &amp; PSI telemetry evaluated: oom_score heuristics, container cgroup memory.max boundaries, and Pressure Stall Information (some vs full).</label></li>
<li><input type="checkbox" id="check-8-4"> <label for="check-8-4">Diagnostic toolchain applied: structured JSON evaluation (jq/python) replacing brittle text grep, socket inspection via ss, and boundary isolation.</label></li>
<li><input type="checkbox" id="check-8-5"> <label for="check-8-5">Practice completed: recorded bounded local CPU task, inspected /proc/meminfo metrics, and classified supplied OOM/PSI incidents into an architectural baseline report.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-008" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 8 Completed':'Mark Day 8 as Read';">Mark Day 8 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-008" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''

t1_tech = day_008_part1.TOPIC_01_TECH.replace('{FIG_8_1_HTML}', FIG_8_1_HTML)
t2_tech = day_008_part2.TOPIC_02_TECH.replace('{FIG_8_2_HTML}', FIG_8_2_HTML)

s1_scenario = {**day_008_scenarios_labs.SCENARIOS_AND_LABS['topic-01']['scenario']}
s1_scenario['evidence'] = s1_scenario['evidence'] + '\n\n' + FIG_8_3_HTML

s2_scenario = {**day_008_scenarios_labs.SCENARIOS_AND_LABS['topic-02']['scenario']}
s2_scenario['evidence'] = s2_scenario['evidence'] + '\n\n' + FIG_8_4_HTML

topics = [
    {
        'key': 'topic-01',
        'title': 'CPU scheduling and waiting, context switching, virtual memory, page faults, RAM/page…',
        'anchors': {
            'overview': 'topic-01-overview',
            'technical': 'topic-01-technical',
            'problem': 'topic-01-problem',
            'lab': 'topic-01-lab'
        },
        'overview': 'Operating system resource telemetry reveals the fundamental hardware bottlenecks governing compute workloads: CPU scheduling queues, context switches, virtual memory translation, page cache dynamics, and kernel OOM invocations. Pressure Stall Information (PSI) introduces kernel-level accounting that quantifies exact microsecond starvation across CPU, memory, and storage subsystems independently of naive utilization metrics.',
        'preview': 'A production batch worker exhibits sudden latency spikes and intermittent crashes, prompting operators to double the host VM instance memory based on low free RAM graphs. The service restarts persist because the application exceeded a strict container cgroup memory quota rather than host-wide physical memory capacity.',
        'technical': t1_tech,
        'questions': [
            'Why does low raw free RAM (MemFree) in Linux frequently represent healthy page cache utilization rather than an imminent Out-Of-Memory failure?',
            'How do Pressure Stall Information (PSI) metrics distinguish between CPU execution saturation and scheduling wait time?',
            'Under what conditions will a containerized process be terminated by the kernel OOM killer despite the underlying virtual machine host having ample available memory?'
        ],
        'reference': 'https://man7.org/linux/man-pages/man7/sched.7.html#DESCRIPTION',
        'reference_label': 'sched(7) Linux CPU scheduling overview description (accessed 2026-10-04)',
        'scenario': s1_scenario,
        'lab': day_008_scenarios_labs.SCENARIOS_AND_LABS['topic-01']['lab']
    },
    {
        'key': 'topic-02',
        'title': 'Grep/sed/awk/jq and curl/dig/ss/tcpdump as diagnostic tools',
        'anchors': {
            'overview': 'topic-02-overview',
            'technical': 'topic-02-technical',
            'problem': 'topic-02-problem',
            'lab': 'topic-02-lab'
        },
        'overview': 'Diagnostic command-line utilities form the primary triage toolchain for inspecting system logs, structured data payloads, network transport states, and raw interface traffic. Combining text filters (grep, sed, awk) and JSON engines (jq) with network diagnostic tools (curl, dig, ss, tcpdump) allows operators to methodically test boundaries one hypothesis at a time.',
        'preview': 'An on-call engineer running unstructured text searches for error strings across production JSON logs reports zero customer impact during an active outage. Downstream payment processing requests were actively failing with HTTP 503 status codes that contained no textual error keywords in their structured payload fields.',
        'technical': t2_tech,
        'questions': [
            'Why does evaluating structured JSON log streams with flat text search tools like grep introduce severe false-negative conclusions during production incident triage?',
            'How does the ss utility differentiate between an external network routing failure and a local process-level socket backlog queue blockage?',
            'What diagnostic advantages does inspecting HTTP status codes and response headers via curl provide over raw TCP socket testing or ICMP ping probes?'
        ],
        'reference': 'https://man7.org/linux/man-pages/man1/grep.1.html#DESCRIPTION',
        'reference_label': 'grep(1) pattern search utility description (accessed 2026-10-04)',
        'scenario': s2_scenario,
        'lab': day_008_scenarios_labs.SCENARIOS_AND_LABS['topic-02']['lab']
    }
]

DATA = {
    'contract_version': 2,
    'roadmap_practice': 'Observe a bounded local CPU task and inspect memory/page-cache metrics; explain supplied OOM and PSI examples without exhausting the host.',
    'roadmap_exit': 'A resource baseline and predicted CPU-throttling versus memory-pressure symptoms.',
    'day': 8,
    'work_block': 'Days 1–17 — Foundations',
    'part1_html': PART1_HTML,
    'part1_intro': 'Day 8 examines core operating system resource signals and diagnostic utilities: CPU scheduling and context switching, virtual memory and page cache dynamics, OOM and PSI telemetry, and disciplined command-line diagnostic tools.',
    'part2_intro': 'Analyze the kernel mechanics governing process scheduling, memory allocation, starvation metrics, text stream filtering, and network transport observation.',
    'part3_intro': 'Real-world architectural failure cases demonstrating container cgroup OOM quota mismatches and silent false-negative monitoring failures from unstructured log grepping.',
    'part4_intro': 'Hands-on operational exercises to benchmark CPU execution, inspect Linux virtual memory distributions, classify OOM and PSI signals, and implement schema-validated log filtering.',
    'exit_summary': 'A verified resource baseline and predicted CPU-throttling versus memory-pressure symptom matrix, backed by empirical CPU benchmarks, memory telemetry calculations, and schema-aware log filtering.',
    'completion_html': COMPLETION_HTML,
    'arch_diagram': ARCH_DIAGRAM,
    'arch_svg_html': '',
    'arch_table_html': '',
    'lab_defaults': {},
    'topics': topics
}

# Write out to scratch/day_data_008.py
out_path = Path("scratch/day_data_008.py")
with open(out_path, "w", encoding="utf-8") as f:
    f.write('"""Durable data specification for Day 8: CPU, memory and diagnostic signals."""\n\n')
    f.write(f'ACCESS_DATE = {repr(ACCESS_DATE)}\n\n')
    f.write(f'SOURCES = {repr(SOURCES)}\n\n')
    f.write(f'DATA = ')
    f.write(pprint.pformat(DATA, width=120, sort_dicts=False))
    f.write('\n')

print(f"Successfully assembled {out_path} ({out_path.stat().st_size} bytes)")
