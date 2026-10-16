#!/usr/bin/env python3
"""Assembler script to generate scratch/day_data_011.py."""
import sys
import pprint
from pathlib import Path

# Add scratch to path
sys.path.insert(0, str(Path("scratch").resolve()))

import day_011_part1
import day_011_part2
import day_011_scenarios_labs

from generate_day_011 import (
    ACCESS_DATE, SOURCES, FIG_11_1_HTML, FIG_11_2_HTML, FIG_11_3_HTML,
    FIG_11_4_HTML, PART1_HTML
)

COMPLETION_HTML = '''<div class="completion-box" id="completion-box-011">
<h3>Day 11 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-11-1"> <label for="check-11-1">Cloud service models mapped: distinguished IaaS, PaaS, FaaS, and SaaS operational boundaries across Compute Engine, Cloud Run, Cloud Run functions, and BigQuery.</label></li>
<li><input type="checkbox" id="check-11-2"> <label for="check-11-2">Shared responsibility understood: delineated Security OF the Cloud (physical, silicon, hypervisor) versus Security IN the Cloud (OS, IAM, app code, data).</label></li>
<li><input type="checkbox" id="check-11-3"> <label for="check-11-3">Customer invariants recognized: verified that IAM least privilege, data classification, and disaster recovery validation never transfer to Google Cloud.</label></li>
<li><input type="checkbox" id="check-11-4"> <label for="check-11-4">Shared fate operationalized: leveraged Security Command Center, secure blueprints, and automated posture management.</label></li>
<li><input type="checkbox" id="check-11-5"> <label for="check-11-5">Exit evidence verified: compiled and audited the complete Shared Responsibility Matrix assigning explicit owners for OS patching, app security, and data recovery across VM, managed-container, and SaaS examples.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-011" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 11 Completed':'Mark Day 11 as Read';">Mark Day 11 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-011" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''

t1_tech = day_011_part1.TOPIC_01_TECH.replace('{FIG_11_1_HTML}', FIG_11_1_HTML)
t2_tech = day_011_part2.TOPIC_02_TECH.replace('{FIG_11_2_HTML}', FIG_11_2_HTML)

s1_scenario = {**day_011_scenarios_labs.SCENARIOS_AND_LABS['topic-01']['scenario']}
s1_scenario['evidence'] = s1_scenario['evidence'] + '\n\n' + FIG_11_3_HTML

s2_scenario = {**day_011_scenarios_labs.SCENARIOS_AND_LABS['topic-02']['scenario']}
s2_scenario['evidence'] = s2_scenario['evidence'] + '\n\n' + FIG_11_4_HTML

topics = [
    {
        'key': 'topic-01',
        'title': 'IaaS, PaaS, FaaS, SaaS, and where GCP services fall',
        'anchors': {
            'overview': 'topic-01-overview',
            'technical': 'topic-01-technical',
            'problem': 'topic-01-problem',
            'lab': 'topic-01-lab'
        },
        'overview': (
            'Cloud service models establish the boundary of operational abstraction separating application business logic '
            'from physical infrastructure. Infrastructure as a Service (IaaS) provides raw virtualized compute, storage, '
            'and networking where the customer manages the entire guest operating system and runtime stack. Platform as a Service (PaaS) '
            'and Function as a Service (FaaS) abstract host operating systems and server provisioning into managed container '
            'and event-driven execution runtimes, while Software as a Service (SaaS) delivers turnkey enterprise applications '
            'where the customer governs only user identity and data access.'
        ),
        'preview': (
            'An order ingestion service hosted on a single Compute Engine virtual machine crashes after a manual operating system update breaks local system libraries during peak holiday traffic. '
            'The engineering team re-architects the endpoint onto Google Cloud Run, delegating host operating system patching to Google while eliminating 14 hours of potential downtime.'
        ),
        'technical': t1_tech,
        'questions': [
            'How do the operational maintenance duties of Compute Engine compare directly against Cloud Run and Cloud Run functions?',
            'Under what architectural conditions is an enterprise justified in accepting the higher maintenance toil of IaaS over PaaS?',
            'Why does serverless FaaS/PaaS eliminate host OS patching while leaving container dependency vulnerabilities entirely within the customer domain?'
        ],
        'reference': 'https://cloud.google.com/learn/paas-vs-iaas-vs-saas#what-are-iaas-paas-saas-and-caas',
        'reference_label': f'Google Cloud — PaaS vs. IaaS vs. SaaS (accessed {ACCESS_DATE})',
        'scenario': s1_scenario,
        'lab': day_011_scenarios_labs.SCENARIOS_AND_LABS['topic-01']['lab']
    },
    {
        'key': 'topic-02',
        'title': 'Shared responsibility model (what Google secures vs what you secure)',
        'anchors': {
            'overview': 'topic-02-overview',
            'technical': 'topic-02-technical',
            'problem': 'topic-02-problem',
            'lab': 'topic-02-lab'
        },
        'overview': (
            'Cloud security is governed by the Shared Responsibility Model, which delineates the security duties '
            'enforced by the cloud provider from those that remain strictly tenant obligations. Google Cloud guarantees the physical '
            'security of data centers, custom Titan silicon verification, KVM hypervisor isolation, and global network encryption '
            '(Security OF the Cloud). The customer remains strictly and non-negotiably responsible for IAM role bindings, service account '
            'credentials, application source code vulnerabilities, network firewall perimeters, and data recovery lifecycle governance (Security IN the Cloud).'
        ),
        'preview': (
            'An engineering team deploying a customer account portal to Cloud Run erroneously assumes that Google Cloud automatically blocks unauthorized public internet requests. '
            'Because the team bound allUsers to the run invoker role, unauthenticated internet callers exfiltrate 128,000 sensitive customer records until least privilege OIDC authentication is restored.'
        ),
        'technical': t2_tech,
        'questions': [
            'What exact hardware, hypervisor, and network security guarantees does Google provide under Security OF the Cloud?',
            'Why does the 99.999999999% durability SLA of Cloud Storage fail to protect an enterprise against accidental data deletion or ransomware?',
            'How does Google Cloud Shared Fate transform compliance and security posture management through Security Command Center and curated blueprints?'
        ],
        'reference': 'https://docs.cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate#shared_responsibility',
        'reference_label': f'Google Cloud Architecture Framework — Shared responsibility and shared fate (accessed {ACCESS_DATE})',
        'scenario': s2_scenario,
        'lab': day_011_scenarios_labs.SCENARIOS_AND_LABS['topic-02']['lab']
    }
]

DAY_DATA_011 = {
    'contract_version': 2,
    'day': 11,
    'day_padded': '011',
    'title': 'Cloud service models and responsibility',
    'work_block': 'Days 1–17 — Foundations',
    'time_estimate': '2–3 hours',
    'prerequisites': 'Day 10 (Docker, container orchestration, and Kubernetes core objects); bring their exit artifacts.',
    'roadmap_practice': 'Assign OS patching, application security and data recovery responsibilities for VM, managed-container and SaaS examples.',
    'roadmap_exit': 'A responsibility matrix with an owner for each task.',
    'part1_html': PART1_HTML,
    'part1_intro': (
        'Day 11 establishes the architectural boundaries between Infrastructure as a Service (IaaS), '
        'Platform as a Service (PaaS), Function as a Service (FaaS), and Software as a Service (SaaS), '
        'and details the Google Cloud Shared Responsibility and Shared Fate models.'
    ),
    'part2_intro': (
        'The following subtopic discussions explore the service model abstraction spectrum, Google Cloud service classifications, '
        'the security demarcation between provider and customer, and the non-delegable customer invariants of IAM, encryption, and data recovery.'
    ),
    'part3_intro': (
        'Real-world operational incidents demonstrate the catastrophic business and security consequences of service model mismatches '
        'and shared responsibility misunderstandings, followed by defensible, verified remediations.'
    ),
    'part4_intro': (
        'The executable labs below provide rigorous, step-by-step procedures to construct a cloud service model decision matrix '
        'and author a comprehensive shared responsibility governance matrix assigning explicit task ownership across VM, container, and SaaS examples.'
    ),
    'exit_summary': (
        'Completion of Day 11 yields a verified, production-grade Shared Responsibility Matrix assigning explicit owners '
        'for OS patching, application security, and data recovery across Compute Engine (VM), Cloud Run (managed-container), '
        'and BigQuery / Google Workspace (SaaS) examples.'
    ),
    'completion_html': COMPLETION_HTML,
    'access_date': ACCESS_DATE,
    'sources': SOURCES,
    'topics': topics
}

if __name__ == '__main__':
    out_file = Path('scratch/day_data_011.py')
    with open(out_file, 'w') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('"""Durable specification for Day 11."""\n\n')
        f.write(f'ACCESS_DATE = {repr(ACCESS_DATE)}\n\n')
        f.write(f'SOURCES = {repr(SOURCES)}\n\n')
        f.write('DATA = ')
        f.write(pprint.pformat(DAY_DATA_011, width=120, sort_dicts=False))
        f.write('\n')
    print(f'Successfully wrote {out_file} ({out_file.stat().st_size} bytes)')
