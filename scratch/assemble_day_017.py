"""Assemble scratch/day_data_017.py from modular components."""

import pprint
from scratch.day_017_part1 import (
    PART1_HTML, PART1_INTRO, PART2_INTRO, PART3_INTRO, PART4_INTRO,
    EXIT_SUMMARY, COMPLETION_HTML
)
from scratch.day_017_topic1 import TOPIC_01
from scratch.day_017_topic2 import TOPIC_02

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'Google Cloud Certification: Professional Cloud Architect — About this certification (accessed 2026-10-04)',
        'https://cloud.google.com/learn/certification/cloud-architect#about-this-certification'
    ),
    'topic-02': (
        'Google Cloud Architecture Framework: Core principles (accessed 2026-10-04)',
        'https://cloud.google.com/architecture/framework#core_principles'
    )
}

REVIEW_RECORDS = {
    'source_ledger': {
        'https://cloud.google.com/learn/certification/cloud-architect#about-this-certification': {
            'heading_opened': 'About this certification'
        },
        'https://cloud.google.com/architecture/framework#core_principles': {
            'heading_opened': 'Core principles'
        }
    },
    'product_claims': [
        {
            'claim': 'Google Cloud infrastructure manages edge routing and packet transit through Google Front Ends (GFE), Andromeda virtual network switches, and Cloud Load Balancing, with private DNS queries traversing Cloud DNS VPC resolvers at 169.254.169.254.',
            'section_url': 'https://cloud.google.com/learn/certification/cloud-architect#about-this-certification',
            'heading_opened': 'About this certification'
        },
        {
            'claim': 'The Google Cloud Architecture Framework mandates operational excellence, system reliability, and disciplined change management through iterative review mechanisms before deploying production workloads.',
            'section_url': 'https://cloud.google.com/architecture/framework#core_principles',
            'heading_opened': 'Core principles'
        }
    ],
    'visual_reasons': {
        'Gate 1 End-to-End Foundation Request and Execution Trace': 'Preserved comprehensive architectural request flow tracing client checkout through DNS, CIDR routing, TLS termination, containerized execution, 12-Factor app validation, and relational ACID persistence.',
        'Five-Dimension Foundation Rubric and Gate 1 Decision Flow': 'Preserved five-dimension evaluation rubric and Gate 1 decision flow mapping Correctness, Traceability, Evidence Quality, Recovery Reasoning, and Communication.',
        'Incident Diagram: Overlapping CIDR Subnets and DNS Conflict Remediation': 'Preserved diagnostic incident flow showing subnet collision in 10.0.1.0/24 and search domain loop contrasted with disjoint CIDRs and authoritative FQDN resolution.',
        'Incident Diagram: Unchecked Event Replay Breaches Duplicate Fulfillment Invariant': 'Preserved diagnostic incident flow showing message redelivery without uniqueness constraint causing duplicate physical shipments contrasted with relational uniqueness guard.'
    }
}

DATA = {
    'contract_version': 2,
    'day': 17,
    'day_padded': '017',
    'title': 'Day 17 — Gate 1 — Foundation recall and repair',
    'time_estimate': '2–3 hours',
    'prerequisites': '[Day 5](#day-5), [Day 8](#day-8), [Day 10](#day-10), [Day 16](#day-16); bring their exit artifacts.',
    'work_block': 'Days 1–17 — Foundations',
    'roadmap_practice': 'Reproduce the local request flow and SQL rollback without copying the walkthrough; repair the weakest shell, network or state explanation.',
    'roadmap_exit': 'A scored G1 checklist, corrected evidence and an explicit pass or repeat decision.',
    'access_date': ACCESS_DATE,
    'sources': SOURCES,
    'part1_intro': PART1_INTRO,
    'part2_intro': PART2_INTRO,
    'part3_intro': PART3_INTRO,
    'part4_intro': PART4_INTRO,
    'exit_summary': EXIT_SUMMARY,
    'part1_html': PART1_HTML,
    'completion_html': COMPLETION_HTML,
    'topics': [TOPIC_01, TOPIC_02],
    'review_records': REVIEW_RECORDS,
    'lab_defaults': {},
    'arch_diagram': {},
    'arch_svg_html': '',
    'arch_table_html': ''
}


def main():
    target_file = 'scratch/day_data_017.py'
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write('"""Durable specification for Day 17: Gate 1 — Foundation recall and repair."""\n\n')
        f.write(f"ACCESS_DATE = {repr(ACCESS_DATE)}\n\n")
        f.write(f"SOURCES = {pprint.pformat(SOURCES, width=120)}\n\n")
        f.write("DATA = ")
        pprint.pprint(DATA, stream=f, width=120, sort_dicts=False)
        f.write("\n")
    print(f"Generated {target_file} successfully.")


if __name__ == '__main__':
    main()
