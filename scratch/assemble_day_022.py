"""Assembler for Day 22 specification (scratch/day_data_022.py)."""

from scratch.generate_day_022 import ACCESS_DATE, SOURCES, PART1_HTML_DATA, render_part1_html, render_completion_html
from scratch.day_022_part1 import TOPIC_01_TECH
from scratch.day_022_part2 import TOPIC_02_TECH
from scratch.day_022_scenarios_labs import SCENARIOS, LABS

def build_day_data():
    topics = [
        {
            'key': 'topic-01',
            'title': 'Resources and inheritance (policies flow downward and are additive for IAM)',
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
            'title': 'Labels vs tags vs network tags (three different things, often confused)',
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
        }
    ]

    data = {
        'contract_version': 2,
        'day': 22,
        'day_padded': '022',
        'title': 'Day 22 — Inheritance, labels and tags',
        'time_estimate': '2–3 hours',
        'prerequisites': '[Day 21](#day-21); bring their exit artifacts.',
        'work_block': 'Days 18–35 — Cloud environment and identity',
        'roadmap_practice': 'Evaluate effective access in a sample parent/child hierarchy and choose labels versus policy tags versus network tags for three uses.',
        'roadmap_exit': 'An inheritance calculation and a tagging convention with concrete examples.',
        'access_date': ACCESS_DATE,
        'sources': SOURCES,
        'part1_intro': (
            'A conceptual foundation covering hierarchical IAM policy inheritance, the additive union principle, '
            'and the three distinct architectural metadata planes: Resource Labels, Resource Manager Tags, and Network Tags.'
        ),
        'part2_intro': (
            'An in-depth technical analysis detailing mathematical effective access calculations, IAM Deny policy precedence, '
            'control plane limits, FinOps billing export queries, CEL conditional IAM tags, and VPC firewall packet filtering.'
        ),
        'part3_intro': (
            'Real-world operational incident case studies examining production database drops caused by inherited folder-level '
            'editor roles and security perimeter exposures caused by confusing resource labels with network tags.'
        ),
        'part4_intro': (
            'Hands-on guided laboratory exercises modeling container hierarchy bindings, calculating additive IAM unions, '
            'enforcing IAM Deny rules, benchmarking the three-plane metadata matrix, and authoring the enterprise taxonomy guide.'
        ),
        'exit_summary': (
            'Completion of Day 22 produces verified exit evidence consisting of a mathematically proved IAM inheritance calculation '
            'matrix and a comprehensive enterprise tagging guide with concrete Terraform configurations.'
        ),
        'part1_html': render_part1_html(),
        'completion_html': render_completion_html(),
        'topics': topics
    }
    return data

if __name__ == '__main__':
    data = build_day_data()
    out_path = 'scratch/day_data_022.py'
    with open(out_path, 'w') as f:
        f.write('"""Durable specification for Day 22: Inheritance, labels and tags."""\n\n')
        f.write(f"ACCESS_DATE = '{ACCESS_DATE}'\n\n")
        f.write(f"SOURCES = {repr(SOURCES)}\n\n")
        f.write(f"DATA = {repr(data)}\n")
    print(f"Generated {out_path} successfully.")
