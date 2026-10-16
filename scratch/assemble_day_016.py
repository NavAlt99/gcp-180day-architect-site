"""Assemble Day 16 data spec into scratch/day_data_016.py."""

import pprint
from scratch.generate_day_016 import ACCESS_DATE, SOURCES, PART1_HTML, FIG_16_1_HTML, FIG_16_2_HTML
from scratch.day_016_part1 import TOPIC_01_TECH
from scratch.day_016_part2 import TOPIC_02_TECH
from scratch.day_016_scenarios_labs import SCENARIOS, LABS

COMPLETION_HTML = '''<div class="completion-box" id="completion-box-016">
<h3>Day 16 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-16-1"> <label for="check-16-1">Relational foundations mastered: designed 3NF normalized schemas eliminating partial and transitive functional dependencies.</label></li>
<li><input type="checkbox" id="check-16-2"> <label for="check-16-2">Relational algebra applied: executed multi-table INNER and LEFT JOINs with enforced foreign key referential integrity constraints.</label></li>
<li><input type="checkbox" id="check-16-3"> <label for="check-16-3">Analytical aggregation executed: transformed transactional records into business metrics using GROUP BY, SUM, COUNT, and HAVING filters.</label></li>
<li><input type="checkbox" id="check-16-4"> <label for="check-16-4">ACID transaction lifecycle proven: demonstrated atomic commit persistence and complete rollback on simulated payment errors.</label></li>
<li><input type="checkbox" id="check-16-5"> <label for="check-16-5">Concurrency anomalies diagnosed and resolved: contrasted Read Committed overselling races with atomic conditional updates (WHERE stock &gt;= 1).</label></li>
<li><input type="checkbox" id="check-16-6"> <label for="check-16-6">Exit evidence verified: authored authoritative Day 16 SQL Business Outcomes Artifact with schema, queries, rollback logs, and executive value statement.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-016" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 16 Completed':'Mark Day 16 as Read';">Mark Day 16 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-016" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''

topic_01_tech_rendered = TOPIC_01_TECH.replace('{FIG_16_1_HTML}', FIG_16_1_HTML)
topic_02_tech_rendered = TOPIC_02_TECH.replace('{FIG_16_2_HTML}', FIG_16_2_HTML)

DATA = {
    'contract_version': 2,
    'day': 16,
    'day_padded': '016',
    'title': 'Day 16 — SQL foundations and business outcomes',
    'time_estimate': '2–3 hours',
    'prerequisites': 'Day 13, Day 15; bring their exit artifacts.',
    'roadmap_practice': 'Create local orders and customers tables with keys; run a join and aggregate; commit and roll back a transaction. Write the business outcome this application serves.',
    'roadmap_exit': 'Schema, query results, rollback evidence and a one-paragraph value statement; explain normalization and an isolation anomaly from a worked example.',
    'exit_summary': 'Completion of Day 16 delivers an authoritative SQL Schema, Query Results, Rollback Evidence, and Business Value Statement Artifact, documenting Third Normal Form relational schemas, multi-table joins, GROUP BY aggregations, atomic transaction rollback verification, concurrency anomaly remediation, and an executive business value statement.',
    'work_block': 'Days 1–17 — Foundations',
    'access_date': ACCESS_DATE,
    'sources': SOURCES,
    'part1_intro': 'Day 16 explores relational database theory and transaction management, examining normalization mechanics (1NF through 3NF), relational joins and analytical aggregations, ACID transaction guarantees, and ANSI SQL isolation levels.',
    'part2_intro': 'The technical analyses below detail relational algebra operations, foreign key constraints, B-tree indexing considerations, Write-Ahead Logging (WAL) mechanics, Multi-Version Concurrency Control (MVCC) in PostgreSQL and Cloud SQL, and isolation anomaly mitigation strategies.',
    'part3_intro': 'Production incident retrospectives analyze an autocommit failure that left 850 orphaned order records when line item inserts aborted without rollback, and a high-concurrency flash sale overselling disaster under Read Committed isolation resolved via atomic conditional updates.',
    'part4_intro': 'Hands-on engineering exercises establish normalized customers and orders tables in SQLite, execute relational joins and aggregations, verify atomic transaction commits and rollbacks, simulate concurrency anomalies and conditional update fixes, and author the authoritative business outcome exit artifact.',
    'part1_html': PART1_HTML,
    'completion_html': COMPLETION_HTML,
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Relational tables, primary/foreign keys, normalization, SELECT/JOIN/GROUP BY and…',
            'anchors': {
                'overview': 'topic-01-overview',
                'technical': 'topic-01-technical',
                'problem': 'topic-01-problem',
                'lab': 'topic-01-lab'
            },
            'reference': SOURCES['topic-01'][1],
            'reference_label': SOURCES['topic-01'][0],
            'overview': 'Relational database systems organize structured data into mathematical relations with strict typing, foreign key constraints, and mathematical set semantics. Relational normalization decomposes redundant entities from First through Third Normal Form, permanently eliminating update, insertion, and deletion anomalies while foreign keys preserve referential integrity across customer and order lifecycles. Composing multi-table relational joins and analytical aggregations transforms normalized transactional records into authoritative business metrics.',
            'preview': 'Problem preview: An un-normalized order database stores customer billing addresses as redundant strings directly in the orders table, resulting in data desynchronization when customers update profile details. Downstream warehouse fulfillment dispatches 1,200 orders to obsolete addresses, generating $145,000 in return logistics costs and customer delivery disputes.',
            'technical': topic_01_tech_rendered,
            'questions': [
                'Why does Third Normal Form (3NF) mandate the decomposition of transitive dependencies, and how does this prevent data desynchronization in customer address updates?',
                'How do foreign key constraints (such as ON DELETE RESTRICT vs CASCADE) protect relational databases against orphaned line-item records?',
                'Under what circumstances would a cloud architect deliberately introduce denormalization or materialized views in Cloud SQL or AlloyDB?'
            ],
            'scenario': SCENARIOS['topic-01'],
            'lab': LABS['topic-01']
        },
        {
            'key': 'topic-02',
            'title': 'Locking/deadlocks are practised on Day 61',
            'anchors': {
                'overview': 'topic-02-overview',
                'technical': 'topic-02-technical',
                'problem': 'topic-02-problem',
                'lab': 'topic-02-lab'
            },
            'reference': SOURCES['topic-02'][1],
            'reference_label': SOURCES['topic-02'][0],
            'overview': 'ACID transaction semantics and isolation levels protect enterprise state against partial failures and concurrent access race conditions. By wrapping multiple database mutations into an atomic unit of work (BEGIN, COMMIT, ROLLBACK), the database engine guarantees that either all operations succeed completely or the system reverts cleanly to its previous consistent state. Selecting appropriate transaction isolation levels balances transactional safety against throughput, preventing fatal concurrency anomalies such as dirty reads, non-repeatable reads, and inventory overselling.',
            'preview': 'Problem preview: An order-processing service running under default Read Committed isolation executes non-atomic read-then-write stock checks during a flash sale. Because concurrent transactions read identical inventory counts before committing deductions, 450 customer orders are confirmed for an inventory of only 50 physical items, causing immediate inventory overselling and emergency cancellations.',
            'technical': topic_02_tech_rendered,
            'questions': [
                'How does Write-Ahead Logging (WAL) enable database engines to guarantee ACID durability across sudden host power failures?',
                'Why does the default Read Committed isolation level permit lost updates during concurrent read-then-write stock checks, and how does an atomic conditional update eliminate the anomaly?',
                'How does Google Cloud Spanner achieve distributed multi-region external consistency without traditional two-phase locking bottlenecks?'
            ],
            'scenario': SCENARIOS['topic-02'],
            'lab': LABS['topic-02']
        }
    ]
}

if __name__ == '__main__':
    with open('scratch/day_data_016.py', 'w', encoding='utf-8') as f:
        f.write('"""Day 16 Durable Specification."""\n\n')
        f.write(f'ACCESS_DATE = {repr(ACCESS_DATE)}\n\n')
        f.write(f'SOURCES = {repr(SOURCES)}\n\n')
        f.write('DATA = ')
        pprint.pprint(DATA, stream=f, indent=4, width=120)
        f.write('\n')
    print('Generated scratch/day_data_016.py successfully.')
