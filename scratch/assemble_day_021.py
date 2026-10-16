"""Assembler for Day 21 specification (scratch/day_data_021.py)."""

from scratch.generate_day_021 import ACCESS_DATE, SOURCES, PART1_HTML_DATA, render_part1_html, render_completion_html
from scratch.day_021_part1 import TOPIC_01_TECH
from scratch.day_021_part2 import TOPIC_02_TECH
from scratch.day_021_part3 import TOPIC_03_TECH
from scratch.day_021_scenarios_labs import SCENARIOS, LABS

def build_day_data():
    topics = [
        {
            'key': 'topic-01',
            'title': 'Organization node (tied to Cloud Identity or Google Workspace domain)',
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
            'title': 'Folders (mapping to departments, environments or teams)',
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
            'title': 'Projects',
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
        'day': 21,
        'day_padded': '021',
        'title': 'Day 21 — Resource hierarchy and ownership',
        'time_estimate': '2–3 hours',
        'prerequisites': '[Day 18](#day-18), [Day 19](#day-19), [Day 20](#day-20); bring their exit artifacts.',
        'work_block': 'Days 18–35 — Cloud environment and identity',
        'roadmap_practice': 'Sketch an organization/folder/project hierarchy for development and production and label each owner.',
        'roadmap_exit': 'A landing-zone draft with stable IDs, environment boundaries and operating responsibilities.',
        'access_date': ACCESS_DATE,
        'sources': SOURCES,
        'part1_intro': (
            'A conceptual foundation covering Google Cloud resource hierarchy architecture, Cloud Identity and Google Workspace '
            'apex domain bindings, multi-tier folder structuring models, additive IAM policy inheritance, and the Project Identifiers Triad.'
        ),
        'part2_intro': (
            'An in-depth technical analysis detailing the Organization resource lifecycle, domain verification mechanics, '
            'environment isolation between Production and Non-Production trees, hierarchical Organization Policy enforcement, '
            'Project ID immutability, and Google-managed service agent derivation.'
        ),
        'part3_intro': (
            'Real-world operational incident case studies examining shadow IT risks from orphan projects outside organization nodes, '
            'production database drops caused by flat folder IAM inheritance leakage, and cross-project CMEK decryption outages '
            'triggered by conflating project names with numerical project numbers.'
        ),
        'part4_intro': (
            'Hands-on guided laboratory exercises executing organization root node audits, multi-tier folder tree modeling, '
            'additive IAM policy calculations, project identifier validation, service agent derivations, and authoritative landing zone authoring.'
        ),
        'exit_summary': (
            'Completion of Day 21 produces verified exit evidence consisting of a validated landing-zone draft with stable IDs, '
            'rigorous environment boundaries, additive IAM inheritance proofs, and documented operating responsibilities.'
        ),
        'part1_html': render_part1_html(),
        'completion_html': render_completion_html(),
        'topics': topics
    }
    return data

if __name__ == '__main__':
    data = build_day_data()
    out_path = 'scratch/day_data_021.py'
    with open(out_path, 'w') as f:
        f.write('"""Durable specification for Day 21: Resource hierarchy and ownership."""\n\n')
        f.write(f"ACCESS_DATE = '{ACCESS_DATE}'\n\n")
        f.write(f"SOURCES = {repr(SOURCES)}\n\n")
        f.write(f"DATA = {repr(data)}\n")
    print(f"Generated {out_path} successfully.")
