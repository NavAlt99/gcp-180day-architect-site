"""Day 20 generation module: Sources, access dates, overviews, questions, and visual imports."""

from scratch.day_020_svgs import (
    FIG_20_1_HTML,
    FIG_20_2_HTML,
    FIG_20_3_HTML,
    FIG_20_4_HTML
)

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'Google Cloud APIs Documentation: Cloud Client Libraries (accessed 2026-10-04)',
        'https://cloud.google.com/apis/docs/client-libraries-explained#cloud-client-libraries'
    ),
    'topic-02': (
        'Google Cloud Pub/Sub Documentation: Known limitations (accessed 2026-10-04)',
        'https://cloud.google.com/pubsub/docs/emulator#known_limitations'
    )
}

PART1_HTML_DATA = {
    'topic-01': {
        'title': 'API enablement, client libraries, local versus cloud endpoints, Cloud Shell Editor/Cloud…',
        'keyword': 'Google Cloud API Architecture and Client Libraries',
        'overview': (
            '<strong class="keyword">Google Cloud API Architecture and Client Libraries</strong> establish the '
            'programmatic control plane for all GCP services, governed centrally through the Service Usage API. '
            'Client applications interact with cloud services using idiomatic Google Cloud Client Libraries that '
            'manage authentication, gRPC and REST transport layers, connection pooling, and automated retries. '
            'Asynchronous resource mutations return Long-Running Operations (LROs) that require deterministic polling '
            'with exponential backoff and jitter before dependent infrastructure can be configured.'
        ),
        'preview': (
            'A platform engineer triggered an automated database rollout script that executed schema migrations immediately '
            'after receiving an initial API response. Because the script did not poll the asynchronous long-running operation '
            'to completion, the database was still in a pending creation state and rejected all connection attempts, halting the deployment pipeline.'
        ),
        'questions': [
            'Why does receiving an HTTP 200 response from an asynchronous resource creation API not indicate that the target resource is ready for operational traffic?',
            'How do idiomatic Google Cloud Client Libraries differ from legacy Google API Discovery Client Libraries in transport performance and connection lifecycle management?',
            'What specific failure modes emerge when an automated infrastructure pipeline omits exponential backoff and jitter while polling Long-Running Operations?'
        ]
    },
    'topic-02': {
        'title': 'Learn the purpose and documented limitations of Pub/Sub, Firestore, Spanner and Bigtable…',
        'keyword': 'Local Software Emulators and Service Boundaries',
        'overview': (
            '<strong class="keyword">Local Software Emulators and Service Boundaries</strong> enable developers to test '
            'cloud applications locally without provisioning live cloud resources or incurring financial spend. '
            'Official Google Cloud emulators for Pub/Sub, Firestore, Spanner, and Bigtable mirror cloud API contracts '
            'on local loopback ports, redirecting client library RPCs via standard environment variables. '
            'However, emulators run as single-node in-memory processes that diverge significantly from cloud production '
            'in distributed timing, TrueTime consistency, partition durability, and message delivery guarantees.'
        ),
        'preview': (
            'An engineering team verified their order processing microservice against a local Pub/Sub emulator and observed zero message duplicates during functional testing. '
            'When deployed to cloud production, multi-zone network jitter triggered ack deadline timeouts and message redeliveries, resulting in duplicate order fulfillments because the consumer lacked idempotency controls.'
        ),
        'questions': [
            'Which specific production guarantees—such as TrueTime external consistency, multi-region replication, and at-least-once message replay—are omitted by local software emulators?',
            'How do client libraries detect and route traffic to local emulators, and why must authentication credentials be disabled when connecting to emulator endpoints?',
            'What architectural safeguards must be enforced in application code to ensure that systems verified against local emulators remain resilient when deployed to distributed cloud production?'
        ]
    }
}

def render_part1_html():
    cards = []
    for key in ['topic-01', 'topic-02']:
        d = PART1_HTML_DATA[key]
        q_items = ''.join(f'<li>{q}</li>' for q in d['questions'])
        cards.append(f'''<article class="topic-card" id="{key}-overview">
<h3>{d['title']}</h3>
<p><strong class="side-heading">What it is:</strong> {d['overview']}</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> {d['preview']}</p>
<div class="study-prompts">
<p><strong class="side-heading">Architectural questions for study:</strong></p>
<ul>
{q_items}
</ul>
</div>
</article>''')
    return '\n'.join(cards)

def render_completion_html():
    return '''<div class="completion-card">
<h3>Day 20 Completion Checklist &amp; Verification Evidence</h3>
<p>To satisfy the Day 20 exit criteria, verify the following operational and architectural evidence artifacts:</p>
<ul class="checklist">
<li><input type="checkbox" id="check-20-1"> <label for="check-20-1">Service Usage API enablement audited: inspected project service enablement states and handled propagation delays.</label></li>
<li><input type="checkbox" id="check-20-2"> <label for="check-20-2">Client library transport validated: compared gRPC binary protobuf serialization against REST JSON overhead.</label></li>
<li><input type="checkbox" id="check-20-3"> <label for="check-20-3">Asynchronous LRO polling implemented: developed exponential backoff with randomized jitter, asserting <code>done: true</code> before downstream actions.</label></li>
<li><input type="checkbox" id="check-20-4"> <label for="check-20-4">Pub/Sub emulator executed: redirected client library traffic via <code>PUBSUB_EMULATOR_HOST</code> and verified message publish/subscribe flows.</label></li>
<li><input type="checkbox" id="check-20-5"> <label for="check-20-5">Four-service limitations matrix compiled: documented functional divergences and production risks across Pub/Sub, Firestore, Spanner, and Bigtable.</label></li>
<li><input type="checkbox" id="check-20-6"> <label for="check-20-6">Exit evidence artifact generated: authored authoritative report at <code>scratch/day-020-emulator-run-and-limitations.md</code>.</label></li>
</ul>
</div>'''
