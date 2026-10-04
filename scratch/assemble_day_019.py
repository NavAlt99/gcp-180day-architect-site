"""Assembler for Day 19 specification (scratch/day_data_019.py)."""

from scratch.generate_day_019 import ACCESS_DATE, SOURCES, PART1_HTML_DATA, render_part1_html, render_completion_html
from scratch.day_019_part1 import TOPIC_01_TECH
from scratch.day_019_part2 import TOPIC_02_TECH
from scratch.day_019_part3 import TOPIC_03_TECH
from scratch.day_019_scenarios_labs import SCENARIOS, LABS

def build_day_data():
    topics = [
        {
            'key': 'topic-01',
            'title': 'Cloud Shell (persistent 5 GB home directory, preinstalled tools)',
            'anchors': {
                'overview': 'topic-01-overview',
                'technical': 'topic-01-technical',
                'problem': 'topic-01-problem',
                'lab': 'topic-01-lab'
            },
            'overview': PART1_HTML_DATA['topic-01']['overview'],
            'preview': PART1_HTML_DATA['topic-01']['preview'],
            'technical': TOPIC_01_TECH.strip(),
            'questions': PART1_HTML_DATA['topic-01']['questions'],
            'reference': SOURCES['topic-01'][1],
            'reference_label': SOURCES['topic-01'][0],
            'scenario': SCENARIOS['topic-01'],
            'lab': LABS['topic-01']
        },
        {
            'key': 'topic-02',
            'title': 'Install and configure <kbd>gcloud</kbd> locally (<kbd>gcloud init</kbd>, <kbd>gcloud config</kbd>, named…',
            'anchors': {
                'overview': 'topic-02-overview',
                'technical': 'topic-02-technical',
                'problem': 'topic-02-problem',
                'lab': 'topic-02-lab'
            },
            'overview': PART1_HTML_DATA['topic-02']['overview'],
            'preview': PART1_HTML_DATA['topic-02']['preview'],
            'technical': TOPIC_02_TECH.strip(),
            'questions': PART1_HTML_DATA['topic-02']['questions'],
            'reference': SOURCES['topic-02'][1],
            'reference_label': SOURCES['topic-02'][0],
            'scenario': SCENARIOS['topic-02'],
            'lab': LABS['topic-02']
        },
        {
            'key': 'topic-03',
            'title': 'Other CLIs',
            'anchors': {
                'overview': 'topic-03-overview',
                'technical': 'topic-03-technical',
                'problem': 'topic-03-problem',
                'lab': 'topic-03-lab'
            },
            'overview': PART1_HTML_DATA['topic-03']['overview'],
            'preview': PART1_HTML_DATA['topic-03']['preview'],
            'technical': TOPIC_03_TECH.strip(),
            'questions': PART1_HTML_DATA['topic-03']['questions'],
            'reference': SOURCES['topic-03'][1],
            'reference_label': SOURCES['topic-03'][0],
            'scenario': SCENARIOS['topic-03'],
            'lab': LABS['topic-03']
        }
    ]

    data = {
        'contract_version': 2,
        'day': 19,
        'day_padded': '019',
        'title': 'Day 19 — CLI configuration and identity checks',
        'time_estimate': '2–3 hours',
        'prerequisites': '[Day 18](#day-18); bring their exit artifacts.',
        'work_block': 'Days 18–35 — Cloud environment and identity',
        'roadmap_practice': 'Create named CLI configurations and verify project, identity and region before a read-only API call.',
        'roadmap_exit': 'Commands that reliably identify the target environment and prevent an accidental project switch.',
        'access_date': ACCESS_DATE,
        'sources': SOURCES,
        'part1_intro': (
            'Mastering Google Cloud administration requires establishing secure workstation configuration baselines, '
            'understanding Cloud Shell storage and virtualization boundaries, and enforcing multi-project context isolation '
            'across gcloud and specialized CLIs.'
        ),
        'part2_intro': (
            'A deep architectural examination of Cloud Shell persistent disk mounts, local gcloud configuration hierarchies, '
            'parameter precedence resolution tiers, and cross-CLI synchronization between storage, data, and container '
            'management utilities.'
        ),
        'part3_intro': (
            'Real-world operational incident case studies demonstrating production service outages and data loss caused by '
            'ephemeral storage misconceptions, ambient environment variable masking, and decoupled Kubernetes contexts.'
        ),
        'part4_intro': (
            'Hands-on guided laboratory exercises modeling Cloud Shell filesystem boundaries, authoring isolated named gcloud '
            'configurations, proving parameter precedence hierarchies, and generating unified multi-CLI preflight verification runbooks.'
        ),
        'exit_summary': (
            'Completion of Day 19 delivers an authoritative CLI Configuration, Identity Verification, and Target Environment '
            'Controls Artifact, documenting verified environment inspection commands, a multi-CLI alignment matrix, an '
            'accidental switch prevention runbook, and a unified context synchronization script.'
        ),
        'part1_html': render_part1_html(),
        'completion_html': render_completion_html(),
        'topics': topics
    }
    return data

if __name__ == '__main__':
    data = build_day_data()
    out_path = 'scratch/day_data_019.py'
    with open(out_path, 'w') as f:
        f.write('"""Durable specification for Day 19: CLI configuration and identity checks."""\n\n')
        f.write(f"ACCESS_DATE = '{ACCESS_DATE}'\n\n")
        f.write(f"SOURCES = {repr(SOURCES)}\n\n")
        f.write(f"DATA = {repr(data)}\n")
    print(f"Generated {out_path} successfully.")
