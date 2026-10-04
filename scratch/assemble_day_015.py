"""Assemble Day 15 data spec into scratch/day_data_015.py."""

import pprint
from scratch.generate_day_015 import ACCESS_DATE, SOURCES, PART1_HTML, FIG_15_1_HTML, FIG_15_2_HTML
from scratch.day_015_part1 import TOPIC_01_TECH
from scratch.day_015_part2 import TOPIC_02_TECH
from scratch.day_015_scenarios_labs import SCENARIOS, LABS

COMPLETION_HTML = '''<div class="completion-box" id="completion-box-015">
<h3>Day 15 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-15-1"> <label for="check-15-1">Scripting primitives mastered: enforced shebang semantics, standard I/O streams (stdin, stdout, stderr), and defensive exit code handling (set -euo pipefail).</label></li>
<li><input type="checkbox" id="check-15-2"> <label for="check-15-2">Architectural styles contrasted: mapped monolith, microservice, and serverless topologies against failure domains, blast radius, and scaling units.</label></li>
<li><input type="checkbox" id="check-15-3"> <label for="check-15-3">Twelve-Factor contracts applied: externalized config to environment (Factor III), enforced stateless execution (Factor VI), and emitted unbuffered logs to stdout (Factor XI).</label></li>
<li><input type="checkbox" id="check-15-4"> <label for="check-15-4">Defensive perimeter secured: executed fast-fail JSON schema validation rejecting malformed requests with HTTP 400 before backend execution.</label></li>
<li><input type="checkbox" id="check-15-5"> <label for="check-15-5">Distributed correlation established: propagated unique Request IDs across request-response lifecycles and structured RFC 8259 JSON log streams.</label></li>
<li><input type="checkbox" id="check-15-6"> <label for="check-15-6">Exit evidence verified: executed local requests, captured validation failures, and authored authoritative Monolith vs Service Boundaries Artifact.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-015" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 15 Completed':'Mark Day 15 as Read';">Mark Day 15 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-015" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''

topic_01_tech_rendered = TOPIC_01_TECH.replace('{FIG_15_1_HTML}', FIG_15_1_HTML)
topic_02_tech_rendered = TOPIC_02_TECH.replace('{FIG_15_2_HTML}', FIG_15_2_HTML)

DATA = {
    'contract_version': 2,
    'day': 15,
    'day_padded': '015',
    'title': 'Day 15 — Small application and architecture styles',
    'time_estimate': '2–3 hours',
    'prerequisites': 'Day 14; bring their exit artifacts.',
    'roadmap_practice': 'Adapt a worked Python or Bash example into a small order endpoint with request IDs and structured logs; handle invalid input.',
    'roadmap_exit': 'A reproducible local request, validation failure and a diagram comparing monolith and service boundaries.',
    'exit_summary': 'Completion of Day 15 delivers an authoritative Monolith vs Service Boundaries Artifact, documenting reproducible local requests, structured validation fast-fail rejections, Twelve-Factor structured JSON logging traces, and a rigorous comparison of monolithic, microservice, and serverless architectures.',
    'work_block': 'Days 1–17 — Foundations',
    'access_date': ACCESS_DATE,
    'sources': SOURCES,
    'part1_intro': 'Day 15 establishes the foundational software delivery and runtime architecture patterns required for cloud systems engineering, examining scripting mechanics (Bash and Python), structural architectural styles (monolith, microservices, serverless), and Twelve-Factor application design principles.',
    'part2_intro': 'The technical analyses below detail process execution models, stream descriptors, POSIX exit code propagation, blast radius isolation, defensive JSON schema validation, Twelve-Factor logging event streams, and Request ID propagation across distributed microservices.',
    'part3_intro': 'Production failure incidents analyze the devastating blast radius of monolithic processes where an un-isolated PDF memory leak halts core checkout operations, and the critical observability blindspots caused by unstructured plain-text logging during high-concurrency database connection exhaustion.',
    'part4_intro': 'The hands-on exercises construct a modular Python order processing endpoint with defensive exit codes, implement Twelve-Factor structured JSON logging, execute fast-fail schema validation, simulate log correlation queries by Request ID, and synthesize the authoritative architectural boundary comparison artifact.',
    'part1_html': PART1_HTML,
    'completion_html': COMPLETION_HTML,
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Basic Python or Bash from an annotated example',
            'anchors': {
                'overview': 'topic-01-overview',
                'technical': 'topic-01-technical',
                'problem': 'topic-01-problem',
                'lab': 'topic-01-lab'
            },
            'reference': SOURCES['topic-01'][1],
            'reference_label': SOURCES['topic-01'][0],
            'overview': 'Modular application architecture begins with disciplined execution primitives across scripting runtimes and service boundaries. Whether implementing infrastructure automation in Bash or designing microservices in Python, cloud architects enforce predictable exit codes, pipeline flow control, and strict separation between stateless compute logic and external persistence. Contrasting monolithic architectures against containerized microservices and event-driven serverless platforms establishes how failure domains, deployment velocity, and scaling boundaries govern production reliability.',
            'preview': 'Problem preview: An e-commerce platform bundles order checkout and PDF invoice rendering into a single monolithic Python process. When a surge of complex invoice requests leaks memory and triggers an operating system Out-Of-Memory (OOM) kill, the entire order checkout pipeline crashes for 35 minutes, blocking $240,000 in customer transactions.',
            'technical': topic_01_tech_rendered,
            'questions': [
                'Why does the Bash strict mode preamble (set -euo pipefail) prevent silent failures in automated cloud deployment pipelines?',
                'How do Linux container cgroup memory limits prevent an Out-Of-Memory leak in one microservice from terminating neighboring services on the same host?',
                'What are the organizational and operational trade-offs when decomposing a monolithic application into independently deployable microservices on GKE?'
            ],
            'scenario': SCENARIOS['topic-01'],
            'lab': LABS['topic-01']
        },
        {
            'key': 'topic-02',
            'title': 'Request validation, REST/JSON, request IDs and structured logs',
            'anchors': {
                'overview': 'topic-02-overview',
                'technical': 'topic-02-technical',
                'problem': 'topic-02-problem',
                'lab': 'topic-02-lab'
            },
            'reference': SOURCES['topic-02'][1],
            'reference_label': SOURCES['topic-02'][0],
            'overview': 'Distributed observability and rigorous request validation form the defensive perimeter of cloud-native microservices. Governed by Twelve-Factor methodology, production services reject malformed client payloads immediately at the network edge before engaging expensive database queries. Furthermore, modern microservices emit structured JSON logs directly to standard output as unbuffered event streams, decorating every log record with a globally unique Request ID (or W3C trace context) to enable sub-minute troubleshooting across distributed Google Cloud services.',
            'preview': 'Problem preview: A high-concurrency checkout failure inundates backend services with database lock timeouts, but applications emit unformatted free-form text strings without correlation IDs. On-call engineers spend 75 minutes manually grepping disjointed server logs across 40 container instances before isolating a downstream connection pool exhaustion bug.',
            'technical': topic_02_tech_rendered,
            'questions': [
                'Why does Twelve-Factor Factor XI mandate that applications emit logs as unbuffered event streams to stdout rather than writing directly to local disk log files?',
                'How does propagating an X-Request-Id header across microservice boundaries reduce Mean Time To Resolution (MTTR) during distributed system outages?',
                'Under what circumstances can unstructured plain-text logging create operational blindspots and exponential cloud ingestion billing costs in Google Cloud Logging?'
            ],
            'scenario': SCENARIOS['topic-02'],
            'lab': LABS['topic-02']
        }
    ]
}

if __name__ == '__main__':
    with open('scratch/day_data_015.py', 'w', encoding='utf-8') as f:
        f.write('"""Day 15 Durable Specification."""\n\n')
        f.write(f'ACCESS_DATE = {repr(ACCESS_DATE)}\n\n')
        f.write(f'SOURCES = {repr(SOURCES)}\n\n')
        f.write('DATA = ')
        pprint.pprint(DATA, stream=f, indent=2, width=120)
    print("Successfully assembled scratch/day_data_015.py")
