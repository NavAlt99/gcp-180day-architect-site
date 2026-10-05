"""Assemble Day 14 data spec into scratch/day_data_014.py."""

import pprint
from scratch.generate_day_014 import ACCESS_DATE, SOURCES, PART1_HTML, FIG_14_1_HTML, FIG_14_2_HTML
from scratch.day_014_part1 import TOPIC_01_TECH
from scratch.day_014_part2 import TOPIC_02_TECH
from scratch.day_014_scenarios_labs import SCENARIOS, LABS

COMPLETION_HTML = '''<div class="completion-box" id="completion-box-014">
<h3>Day 14 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-14-1"> <label for="check-14-1">Git DAG topology mastered: modeled commits as immutable Directed Acyclic Graph nodes and branches as lightweight 41-byte movable reference pointers.</label></li>
<li><input type="checkbox" id="check-14-2"> <label for="check-14-2">Branch governance enforced: implemented branch protection policies on trunk branches, requiring Pull Request peer reviews and automated Cloud Build CI test passes.</label></li>
<li><input type="checkbox" id="check-14-3"> <label for="check-14-3">Merge provenance preserved: differentiated fast-forward vs non-fast-forward (--no-ff) merges, ensuring clean release histories and single-commit revertability.</label></li>
<li><input type="checkbox" id="check-14-4"> <label for="check-14-4">RFC 9110 HTTP semantics applied: designed resource-oriented RESTful endpoints using safe (GET) and idempotent (PUT, DELETE) methods, strictly rejecting 200 OK error payloads.</label></li>
<li><input type="checkbox" id="check-14-5"> <label for="check-14-5">Defensive API client verified: intercepted upstream non-JSON HTML 502/503 proxy errors and enforced Idempotency-Key headers to eliminate duplicate billing.</label></li>
<li><input type="checkbox" id="check-14-6"> <label for="check-14-6">Exit evidence verified: executed local Git/API exercises and authored authoritative Repository History and Annotated HTTP/JSON API Examples Artifact.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-014" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 14 Completed':'Mark Day 14 as Read';">Mark Day 14 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-014" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''

topic_01_tech_rendered = TOPIC_01_TECH.replace('{FIG_14_1_HTML}', FIG_14_1_HTML)
topic_02_tech_rendered = TOPIC_02_TECH.replace('{FIG_14_2_HTML}', FIG_14_2_HTML)

DATA = {
    'contract_version': 2,
    'day': 14,
    'day_padded': '014',
    'title': 'Day 14 — Git, APIs and JSON',
    'time_estimate': '2–3 hours',
    'prerequisites': 'Day 7, Day 10; bring their exit artifacts.',
    'roadmap_practice': 'Commit a tiny request/response example; create a branch, review a diff and merge a change; parse an error response.',
    'roadmap_exit': 'A repository history and annotated HTTP/JSON success and failure examples.',
    'exit_summary': 'Completion of Day 14 delivers an authoritative Repository History and Annotated HTTP/JSON API Examples Artifact, documenting verified Git DAG branching and merging mechanics alongside robust RFC 9110 REST and RFC 8259 JSON request-response models.',
    'work_block': 'Days 1–17 — Foundations',
    'access_date': ACCESS_DATE,
    'sources': SOURCES,
    'part1_intro': 'Day 14 establishes the core engineering disciplines of distributed version control and distributed systems integration, focusing on Git branching topologies, Pull Request governance, and robust RESTful API design using JSON data interchange.',
    'part2_intro': 'The technical analyses below detail Git internal Directed Acyclic Graph (DAG) structures, branching mechanics, non-fast-forward merge provenance, RFC 9110 HTTP method semantics, status code taxonomies, and defensive API client engineering against upstream proxy failures.',
    'part3_intro': 'Production failure incidents analyze the devastating impact of unreviewed direct commits to production trunk branches breaking JSON schema contracts, and the cascading failure of naive JSON clients crashing on upstream HTML 502 Bad Gateway responses.',
    'part4_intro': 'The hands-on exercises initialize a local Git repository, execute an isolated feature branch enhancement with diff review and non-fast-forward merge, implement standard REST method operations, parse structured error envelopes, and synthesize the authoritative repository history and annotated API examples artifact.',
    'part1_html': PART1_HTML,
    'completion_html': COMPLETION_HTML,
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Git fundamentals (branch, merge, PR)',
            'anchors': {
                'overview': 'topic-01-overview',
                'technical': 'topic-01-technical',
                'problem': 'topic-01-problem',
                'lab': 'topic-01-lab'
            },
            'reference': SOURCES['topic-01'][1],
            'reference_label': SOURCES['topic-01'][0],
            'overview': 'Distributed version control systems manage source code and declarative infrastructure as an immutable Directed Acyclic Graph (DAG) of snapshot commits. Git branches serve as lightweight, movable 41-byte pointers to specific commit hashes, allowing engineering teams to isolate feature experiments and bug fixes from stable production baselines. Pull Requests formalize collaborative code review, branch protection policies, and automated Continuous Integration (CI) validation gates, ensuring that unreviewed, breaking changes never contaminate the production trunk branch.',
            'preview': 'Problem preview: A developer pushes an unvalidated direct commit to the production main branch, inadvertently altering the JSON attribute naming convention in an API contract. Because the commit bypassed pull request CI test gates, 1,200 downstream microservice instances crash upon deployment, generating an emergency P1 outage.',
            'technical': topic_01_tech_rendered,
            'questions': [
                'Why does an immutable Directed Acyclic Graph (DAG) commit structure enable cryptographic provenance verification in Google Cloud Binary Authorization?',
                'What are the operational and audit trade-offs between fast-forward merges, non-fast-forward merges (--no-ff), and squash merges on protected trunk branches?',
                'How do automated Cloud Build triggers and Pull Request branch protection rules mitigate the blast radius of breaking schema modifications?'
            ],
            'scenario': SCENARIOS['topic-01'],
            'lab': LABS['topic-01']
        },
        {
            'key': 'topic-02',
            'title': 'REST APIs and JSON',
            'anchors': {
                'overview': 'topic-02-overview',
                'technical': 'topic-02-technical',
                'problem': 'topic-02-problem',
                'lab': 'topic-02-lab'
            },
            'reference': SOURCES['topic-02'][1],
            'reference_label': SOURCES['topic-02'][0],
            'overview': 'Representational State Transfer (REST) and JSON establish the universal protocol language of modern distributed cloud systems. Governed by RFC 9110 HTTP semantics and RFC 8259 data interchange standards, REST APIs decouple clients from servers through standardized HTTP methods (GET, POST, PUT, DELETE), resource-oriented URI hierarchies, and self-describing JSON payloads. Defensive client engineering requires strict status code handling, content-type negotiation, and resilient error recovery when upstream proxies emit unexpected HTML error responses.',
            'preview': 'Problem preview: An upstream cloud load balancer encounters transient backend exhaustion and returns a 502 Bad Gateway response with an HTML error body. An downstream order-processing service assumes every response contains JSON and attempts to parse the HTML, crashing with an unhandled parser exception and triggering an uncontrolled retry storm that double-bills 340 customer accounts.',
            'technical': topic_02_tech_rendered,
            'questions': [
                'Why is returning HTTP 200 OK with an embedded error payload in the JSON body considered a dangerous anti-pattern in cloud microservices?',
                'How does the RFC 9110 distinction between safe and idempotent HTTP methods govern automated retry logic in API clients?',
                'Why must defensive API clients validate the Content-Type header before attempting to parse response bodies with JSON deserializers?'
            ],
            'scenario': SCENARIOS['topic-02'],
            'lab': LABS['topic-02']
        }
    ]
}

if __name__ == '__main__':
    with open('scratch/day_data_014.py', 'w', encoding='utf-8') as f:
        f.write('"""Day 14 Durable Specification."""\n\n')
        f.write(f'ACCESS_DATE = {repr(ACCESS_DATE)}\n\n')
        f.write(f'SOURCES = {repr(SOURCES)}\n\n')
        f.write('DATA = ')
        pprint.pprint(DATA, stream=f, indent=2, width=120)
    print("Successfully assembled scratch/day_data_014.py")
