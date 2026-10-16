"""Assembler for Day 20 specification (scratch/day_data_020.py)."""

from scratch.generate_day_020 import ACCESS_DATE, SOURCES, PART1_HTML_DATA, render_part1_html, render_completion_html
from scratch.day_020_part1 import TOPIC_01_TECH
from scratch.day_020_part2 import TOPIC_02_TECH
from scratch.day_020_scenarios_labs import SCENARIOS, LABS

def build_day_data():
    topics = [
        {
            'key': 'topic-01',
            'title': 'API enablement, client libraries, local versus cloud endpoints, Cloud Shell Editor/Cloud…',
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
            'title': 'Learn the purpose and documented limitations of Pub/Sub, Firestore, Spanner and Bigtable…',
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
        'day': 20,
        'day_padded': '020',
        'title': 'Day 20 — APIs, client libraries and emulators',
        'time_estimate': '2–3 hours',
        'prerequisites': '[Day 15](#day-15), [Day 19](#day-19); bring their exit artifacts.',
        'work_block': 'Days 18–35 — Cloud environment and identity',
        'roadmap_practice': 'Run one Pub/Sub emulator example; configure its client endpoint and document how Firestore, Spanner and Bigtable emulators differ from production.',
        'roadmap_exit': 'One reproducible emulator run and a four-service limitations matrix; no requirement to deploy all four.',
        'access_date': ACCESS_DATE,
        'sources': SOURCES,
        'part1_intro': (
            'A conceptual foundation covering Google Cloud API architecture, Service Usage enablement, client library transports, '
            'loopback endpoint redirection, and asynchronous Long-Running Operation (LRO) polling.'
        ),
        'part2_intro': (
            'An in-depth architectural analysis of API control planes, gRPC versus REST protocols, local software emulators, '
            'and the documented operational limitations across Pub/Sub, Firestore, Spanner, and Bigtable.'
        ),
        'part3_intro': (
            'Real-world production incident case studies analyzing downtime and duplicate order fulfillments caused by '
            'unpolled asynchronous LROs and emulator-induced delivery assumptions.'
        ),
        'part4_intro': (
            'Hands-on guided laboratory exercises modeling Service Usage enablement, benchmarking transport protocols, '
            'executing local Pub/Sub emulator workflows, and compiling the four-service limitations matrix.'
        ),
        'exit_summary': (
            'Completion of Day 20 produces verified exit evidence consisting of a reproducible local Pub/Sub emulator execution '
            'trace and a comprehensive four-service limitations matrix contrasting emulator capabilities with Google Cloud production.'
        ),
        'part1_html': render_part1_html(),
        'completion_html': render_completion_html(),
        'topics': topics
    }
    return data

if __name__ == '__main__':
    data = build_day_data()
    out_path = 'scratch/day_data_020.py'
    with open(out_path, 'w') as f:
        f.write('"""Durable specification for Day 20: APIs, client libraries and emulators."""\n\n')
        f.write(f"ACCESS_DATE = '{ACCESS_DATE}'\n\n")
        f.write(f"SOURCES = {repr(SOURCES)}\n\n")
        f.write(f"DATA = {repr(data)}\n")
    print(f"Generated {out_path} successfully.")
