#!/usr/bin/env python3
"""Assembler script to generate scratch/day_data_010.py."""
import sys
import pprint
from pathlib import Path

# Add scratch to path
sys.path.insert(0, str(Path("scratch").resolve()))

import day_010_part1
import day_010_part2
import day_010_part3
import day_010_scenarios_labs

# Import base module variables
from generate_day_010 import (
    ACCESS_DATE, SOURCES, FIG_10_1_HTML, FIG_10_2_HTML, FIG_10_3_HTML,
    FIG_10_4_HTML, FIG_10_5_HTML, FIG_10_6_HTML, PART1_HTML, ARCH_DIAGRAM
)

COMPLETION_HTML = '''<div class="completion-box" id="completion-box-010">
<h3>Day 10 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-10-1"> <label for="check-10-1">Docker storage mastered: OverlayFS copy-on-write lowerdir/upperdir, inodes, multi-stage builds, and Artifact Registry.</label></li>
<li><input type="checkbox" id="check-10-2"> <label for="check-10-2">Filesystem durability understood: volatile page cache vs POSIX <kbd>fsync()</kbd> flushes to persistent volume storage.</label></li>
<li><input type="checkbox" id="check-10-3"> <label for="check-10-3">Kubernetes control plane mapped: etcd desired state, continuous controller reconciliation, two-phase scheduler bin packing, and self-healing.</label></li>
<li><input type="checkbox" id="check-10-4"> <label for="check-10-4">Core objects &amp; routing connected: Ingress path routing, Service label selectors, dynamic EndpointSlices, Pod replicas, ConfigMaps, and Secrets.</label></li>
<li><input type="checkbox" id="check-10-5"> <label for="check-10-5">Exit evidence verified: compiled the Pod/Deployment/Service ownership diagram and verified volume persistence across container lifecycles.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-010" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 10 Completed':'Mark Day 10 as Read';">Mark Day 10 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-010" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''

t1_tech = day_010_part1.TOPIC_01_TECH.replace('{FIG_10_1_HTML}', FIG_10_1_HTML)
t2_tech = day_010_part2.TOPIC_02_TECH.replace('{FIG_10_2_HTML}', FIG_10_2_HTML)
t3_tech = day_010_part3.TOPIC_03_TECH.replace('{FIG_10_3_HTML}', FIG_10_3_HTML)

s1_scenario = {**day_010_scenarios_labs.SCENARIOS_AND_LABS['topic-01']['scenario']}
s1_scenario['evidence'] = s1_scenario['evidence'] + '\n\n' + FIG_10_4_HTML

s2_scenario = {**day_010_scenarios_labs.SCENARIOS_AND_LABS['topic-02']['scenario']}
s2_scenario['evidence'] = s2_scenario['evidence'] + '\n\n' + FIG_10_5_HTML

s3_scenario = {**day_010_scenarios_labs.SCENARIOS_AND_LABS['topic-03']['scenario']}
s3_scenario['evidence'] = s3_scenario['evidence'] + '\n\n' + FIG_10_6_HTML

topics = [
    {
        'key': 'topic-01',
        'title': 'Docker',
        'anchors': {
            'overview': 'topic-01-overview',
            'technical': 'topic-01-technical',
            'problem': 'topic-01-problem',
            'lab': 'topic-01-lab'
        },
        'overview': (
            'Container image construction and storage architecture combine layered content-addressable tarballs '
            'into a unified root filesystem using copy-on-write union filesystems (OverlayFS). Ephemeral writable container '
            'layers discard state upon process termination, meaning durable application state requires external storage mounts '
            'and explicit operating system persistence semantics: while buffered application writes remain in volatile '
            'kernel page cache, only synchronous flush operations (fsync() / fdatasync()) guarantee write persistence '
            'down to non-volatile physical storage blocks.'
        ),
        'preview': (
            'An order checkout microservice writes transaction recovery markers to its local container directory, '
            'but an automatic pod restart wipes out all active markers and causes duplicate order charges. '
            'The engineering team attaches a persistent volume with explicit filesystem synchronization calls, '
            'ensuring transaction markers survive container replacement and prevent duplicate processing.'
        ),
        'technical': t1_tech,
        'questions': [
            'How does the OverlayFS copy-on-write mechanism impact I/O performance during random write operations?',
            'Why does the standard POSIX write() system call fail to guarantee durability across sudden container terminations?',
            'What architectural criteria dictate choosing between Kubernetes emptyDir, PersistentVolumes, and Cloud Storage FUSE mounts?'
        ],
        'reference': 'https://man7.org/linux/man-pages/man2/fsync.2.html#DESCRIPTION',
        'reference_label': f'fsync(2) Linux file data synchronization description (accessed {ACCESS_DATE})',
        'scenario': s1_scenario,
        'lab': day_010_scenarios_labs.SCENARIOS_AND_LABS['topic-01']['lab']
    },
    {
        'key': 'topic-02',
        'title': 'Container orchestration',
        'anchors': {
            'overview': 'topic-02-overview',
            'technical': 'topic-02-technical',
            'problem': 'topic-02-problem',
            'lab': 'topic-02-lab'
        },
        'overview': (
            'Container orchestration automates the operational lifecycle of distributed containerized applications '
            'across fleets of virtual machine nodes. Managing individual containers imperatively on bare hosts introduces '
            'severe architectural failure modes: unhandled host hardware crashes, manual port allocation conflicts, '
            'lack of automated rollouts and rollbacks, and inability to reconcile desired capacity against node resources. '
            'Kubernetes solves these challenges through a centralized declarative control plane that continuously reconciles '
            'actual runtime telemetry against desired state stored in etcd.'
        ),
        'preview': (
            'A surge in user checkout requests causes a production order service to exhaust host memory on a '
            'standalone virtual machine, crashing all collocated containers and dropping user requests. '
            'Migrating the service to a managed Kubernetes cluster allows the scheduler to distribute replicas '
            'across multiple worker nodes and automatically restart failed instances without operator intervention.'
        ),
        'technical': t2_tech,
        'questions': [
            'How does a declarative reconciliation loop differ from traditional imperative infrastructure automation scripts?',
            'What distinct operational roles do kube-scheduler, kube-controller-manager, and kubelet execute during pod placement?',
            'Under what failure conditions will a Kubernetes Pod become trapped indefinitely in Pending status?'
        ],
        'reference': 'https://kubernetes.io/docs/concepts/overview/#why-you-need-kubernetes-and-what-can-it-do',
        'reference_label': f'Why you need Kubernetes and what it can do (accessed {ACCESS_DATE})',
        'scenario': s2_scenario,
        'lab': day_010_scenarios_labs.SCENARIOS_AND_LABS['topic-02']['lab']
    },
    {
        'key': 'topic-03',
        'title': 'Kubernetes core objects',
        'anchors': {
            'overview': 'topic-03-overview',
            'technical': 'topic-03-technical',
            'problem': 'topic-03-problem',
            'lab': 'topic-03-lab'
        },
        'overview': (
            'Kubernetes core objects represent the foundational declarative primitives used to model cloud-native applications: '
            'Pods represent the atomic unit of collocated container scheduling; Deployments manage declarative replica scaling '
            'and zero-downtime rolling updates; Services provide stable virtual IP addresses and load-balanced endpoint routing '
            'across ephemeral pods; Ingress routes external HTTP/HTTPS traffic into internal cluster services; and ConfigMaps '
            'and Secrets decouple configuration and sensitive credentials from container image binaries.'
        ),
        'preview': (
            'A newly deployed microservice passes all readiness checks but external client requests fail immediately with '
            'HTTP 503 Service Unavailable errors. An inspection reveals that a subtle typo in the Service selector label '
            'prevented the controller from attaching pod IP addresses to the routing endpoint slice.'
        ),
        'technical': t3_tech,
        'questions': [
            'How do Kubernetes Services decouple network routing from ephemeral pod IP churn using EndpointSlices?',
            'Why does a single-character typo in a Service label selector cause silent external HTTP 503 routing failures?',
            'In what ways does mounting ConfigMaps and Secrets as volumes provide superior operational flexibility over environment variables?'
        ],
        'reference': 'https://kubernetes.io/docs/concepts/overview/working-with-objects/#kubernetes-objects',
        'reference_label': f'Understanding Kubernetes objects (accessed {ACCESS_DATE})',
        'scenario': s3_scenario,
        'lab': day_010_scenarios_labs.SCENARIOS_AND_LABS['topic-03']['lab']
    }
]

DATA = {
    'contract_version': 2,
    'roadmap_practice': 'Build a tiny container from an annotated example; compare ephemeral files with a mounted volume and trace buffered write versus durable flush.',
    'roadmap_exit': 'A runnable image, persistence check and Pod/Deployment/Service ownership diagram.',
    'day': 10,
    'work_block': 'Days 1–17 — Foundations',
    'part1_html': PART1_HTML,
    'part1_intro': (
        'Day 10 examines container storage layers, filesystem durability, and container orchestration architectures: '
        'OCI image construction, OverlayFS copy-on-write root filesystems, POSIX fsync() write durability, '
        'declarative reconciliation loops in Kubernetes, and the core object hierarchy (Pods, Deployments, Services, '
        'Ingress, ConfigMaps, and Secrets).'
    ),
    'part2_intro': (
        'Analyze the technical mechanics governing container storage layering, BuildKit layer caching, POSIX page cache '
        'synchronization, declarative control loops, two-phase scheduler bin packing, and service discovery routing.'
    ),
    'part3_intro': (
        'Real-world architectural failure cases demonstrating ephemeral container layer data loss, scale-out scheduling '
        'traps under node memory exhaustion, and silent HTTP 503 routing failures caused by Service selector typos.'
    ),
    'part4_intro': (
        'Hands-on operational exercises to build a container image, test volume persistence against ephemeral teardown, '
        'simulate Kubernetes scheduler bin packing under capacity limits, and diagnose broken Service selectors.'
    ),
    'exit_summary': (
        'A comprehensive Pod/Deployment/Service ownership diagram and storage durability baseline distinguishing '
        'ephemeral OverlayFS storage from persistent volume mounts, backed by runnable container image verification, '
        'scheduler bin packing telemetry, and verified service selector routing.'
    ),
    'completion_html': COMPLETION_HTML,
    'arch_diagram': ARCH_DIAGRAM,
    'access_date': ACCESS_DATE,
    'sources': SOURCES,
    'topics': topics
}

with open("scratch/day_data_010.py", "w") as f:
    f.write(f'"""Durable data specification for Day 10: Images, filesystems and orchestration."""\n\n')
    f.write(f'ACCESS_DATE = {repr(ACCESS_DATE)}\n\n')
    f.write(f'SOURCES = {repr(SOURCES)}\n\n')
    f.write(f'DATA = ')
    pprint.pprint(DATA, stream=f, indent=2, width=120)
    f.write('\n')

print("Successfully generated scratch/day_data_010.py")
