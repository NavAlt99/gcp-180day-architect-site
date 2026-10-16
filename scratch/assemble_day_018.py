"""Assemble Day 18 data spec into scratch/day_data_018.py."""

import pprint
from scratch.generate_day_018 import (
    ACCESS_DATE, SOURCES, PART1_HTML,
    FIG_18_1_HTML, FIG_18_2_HTML
)
from scratch.day_018_part1 import TOPIC_01_TECH
from scratch.day_018_part2 import TOPIC_02_TECH
from scratch.day_018_part3 import TOPIC_03_TECH
from scratch.day_018_scenarios_labs import SCENARIOS, LABS

COMPLETION_HTML = '''<div class="completion-box" id="completion-box-018">
<h3>Day 18 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-18-1"> <label for="check-18-1">Account boundaries established: decoupled identity, resource management, and commercial billing roots with 1:N project-to-billing association.</label></li>
<li><input type="checkbox" id="check-18-2"> <label for="check-18-2">Always Free limits verified: validated monthly quotas across Compute Engine (e2-micro), Cloud Storage, and BigQuery strictly in qualifying US regions.</label></li>
<li><input type="checkbox" id="check-18-3"> <label for="check-18-3">Cost control mechanics mastered: proved that Cloud Billing budget alerts are advisory notifications and designed programmatic Pub/Sub kill-switches.</label></li>
<li><input type="checkbox" id="check-18-4"> <label for="check-18-4">Project identifiers distinguished: mapped mutable Project Names, globally unique immutable Project IDs, and system-assigned numeric Project Numbers.</label></li>
<li><input type="checkbox" id="check-18-5"> <label for="check-18-5">Ambient context drift eliminated: implemented context-aware shell prompts (PS1) and mandated explicit --project flags in operational runbooks.</label></li>
<li><input type="checkbox" id="check-18-6"> <label for="check-18-6">Exit evidence verified: authored authoritative Day 18 Redacted Project/Billing Preflight and Cleanup Plan Artifact.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-018" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 18 Completed':'Mark Day 18 as Read';">Mark Day 18 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-018" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''

topic_01_tech_rendered = TOPIC_01_TECH.replace('{FIG_18_1_HTML}', FIG_18_1_HTML)
topic_02_tech_rendered = TOPIC_02_TECH.replace('{FIG_18_2_HTML}', FIG_18_2_HTML)
topic_03_tech_rendered = TOPIC_03_TECH

DATA = {
    'contract_version': 2,
    'day': 18,
    'day_padded': '018',
    'title': 'Day 18 — Cloud sandbox and cost controls',
    'time_estimate': '2–3 hours',
    'prerequisites': 'Day 17; bring their exit artifacts.',
    'roadmap_practice': 'Select a training sandbox or disposable project, inspect billing access and configure budget notifications if authorized.',
    'roadmap_exit': 'A redacted project/billing preflight and cleanup plan; explain why an alert is not a hard spend cap.',
    'exit_summary': 'Completion of Day 18 delivers an authoritative Redacted Project/Billing Preflight and Cleanup Plan Artifact, documenting verified project-to-billing linkages, an Always Free quota comparison matrix, an architectural analysis proving why budget alerts are not hard spend caps, a programmatic Pub/Sub kill-switch design, and an automated disposable sandbox cleanup plan.',
    'work_block': 'Days 18–35 — Cloud environment and identity',
    'access_date': ACCESS_DATE,
    'sources': SOURCES,
    'part1_intro': 'Day 18 inaugurates Block 2 (Cloud Environment and Identity), establishing foundational commercial boundaries, billing account structures, the $300 Free Trial lifecycle, Always Free tier limits, and Google Cloud Console project navigation paradigms.',
    'part2_intro': 'The technical analyses below detail the decoupling of identity and billing, project-to-billing 1:N cardinality, regional Always Free SKU constraints, the critical distinction between advisory budget alerts and programmatic spend caps, and Cloud Shell execution safety.',
    'part3_intro': 'Production incident retrospectives examine service outages caused by severed billing accounts following expired payment cards, massive financial overruns from runaway GPU benchmarks under passive budget alerts, and production service destruction caused by ambient Cloud Shell project context drift.',
    'part4_intro': 'Hands-on engineering exercises implement a Python billing preflight validator, audit Always Free limits across regional SKUs, parse Cloud Billing budget Pub/Sub schemas, configure context-aware shell prompt guards, author an automated cleanup plan, and synthesize the authoritative Day 18 exit artifact.',
    'part1_html': PART1_HTML,
    'completion_html': COMPLETION_HTML,
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Google Cloud accounts and the Free Trial',
            'anchors': {
                'overview': 'topic-01-overview',
                'technical': 'topic-01-technical',
                'problem': 'topic-01-problem',
                'lab': 'topic-01-lab'
            },
            'reference': SOURCES['topic-01'][1],
            'reference_label': SOURCES['topic-01'][0],
            'overview': 'Google Cloud Accounts bind corporate or individual identities to Google Cloud resources through linked Cloud Billing Accounts. The 90-day Free Trial provides $300 in promotional credit for proof-of-concept evaluations across Compute Engine, Cloud Storage, BigQuery, and managed services without incurring automatic charges upon expiration unless explicitly upgraded. Establishing isolated billing boundaries and verifying billing health before provisioning infrastructure protects sandbox environments from unexpected operational suspensions.',
            'preview': 'Problem preview: An expired corporate payment method on an unmonitored billing account triggers automated suspension across training sandbox projects, instantly terminating running compute instances. Without redundant payment routing and billing preflight verification, sudden cloud account lockouts disrupt engineering onboarding and delay critical project timelines.',
            'technical': topic_01_tech_rendered,
            'questions': [
                'Why does Google Cloud enforce a strict separation between user identity, resource hierarchy folders, and Cloud Billing Accounts?',
                'What operational and fraud-prevention constraints are enforced on Google Cloud Free Trial accounts, and how does upgrading to a paid account alter these boundaries?',
                'How does payment method failure in a self-serve billing account impact running compute resources across linked projects, and how is redundancy architected?'
            ],
            'scenario': SCENARIOS['topic-01'],
            'lab': LABS['topic-01']
        },
        {
            'key': 'topic-02',
            'title': 'Google Cloud Free Tier and monthly limits',
            'anchors': {
                'overview': 'topic-02-overview',
                'technical': 'topic-02-technical',
                'problem': 'topic-02-problem',
                'lab': 'topic-02-lab'
            },
            'reference': SOURCES['topic-02'][1],
            'reference_label': SOURCES['topic-02'][0],
            'overview': 'Always Free Tier allowances provide non-expiring monthly usage quotas across core services, including one e2-micro instance in qualifying US regions, 5 GB-months of regional Cloud Storage, and 1 TB of BigQuery query analysis. Crucially, Google Cloud budget alerts are passive notifications that do not halt running instances or block API calls when thresholds are crossed. Implementing programmatic financial controls requires event-driven kill-switches rather than relying on advisory email warnings.',
            'preview': 'Problem preview: A training pipeline exceeds its monthly Always Free Compute Engine quota by running an oversized VM in a non-qualifying region, incurring unexpected daily billing charges. Misinterpreting passive budget alert emails as automated hard spend caps leads to budget exhaustion and unexpected corporate credit card overages.',
            'technical': topic_02_tech_rendered,
            'questions': [
                'Why are Google Cloud Always Free Compute Engine and Cloud Storage allowances restricted strictly to specific United States regions (us-central1, us-east1, us-west1)?',
                'Why does Google Cloud decouple budget alerts from automated workload disruption, and why is an advisory alert email not a hard spend cap?',
                'How can an enterprise architect construct an automated, programmatic hard spend cap using Cloud Billing Budgets, Pub/Sub, and serverless Cloud Functions?'
            ],
            'scenario': SCENARIOS['topic-02'],
            'lab': LABS['topic-02']
        },
        {
            'key': 'topic-03',
            'title': 'Google Cloud Console navigation and project selection',
            'anchors': {
                'overview': 'topic-03-overview',
                'technical': 'topic-03-technical',
                'problem': 'topic-03-problem',
                'lab': 'topic-03-lab'
            },
            'reference': SOURCES['topic-03'][1],
            'reference_label': SOURCES['topic-03'][0],
            'overview': 'Project Context Management governs all operator and automation interactions across the Google Cloud Console, gcloud CLI, and Terraform. Projects provide complete administrative, networking, and IAM isolation, identified by mutable Project Names, globally unique immutable Project IDs, and system-assigned numeric Project Numbers. Guarding against ambient project context drift ensures administrative commands target intended training sandboxes rather than production systems.',
            'preview': 'Problem preview: An engineer executing a resource cleanup command from Cloud Shell targets the production project instead of the training sandbox due to ambient project context drift. Conflating project display names with immutable project IDs risks accidental deletion of production microservice endpoints, creating immediate customer checkout outages.',
            'technical': topic_03_tech_rendered,
            'questions': [
                'What are the technical and operational distinctions between a Project Name, a Project ID, and a Project Number in Google Cloud?',
                'How does Cloud Shell maintain state across browser disconnects, and why must operators beware of ambient project drift in ~/.config/gcloud?',
                'What architectural policies and tooling guards should an SRE team implement to prevent accidental resource deletion in production environments?'
            ],
            'scenario': SCENARIOS['topic-03'],
            'lab': LABS['topic-03']
        }
    ]
}

if __name__ == '__main__':
    with open('scratch/day_data_018.py', 'w', encoding='utf-8') as f:
        f.write('"""Day 18 Durable Specification."""\n\n')
        f.write(f'ACCESS_DATE = {repr(ACCESS_DATE)}\n\n')
        f.write(f'SOURCES = {repr(SOURCES)}\n\n')
        f.write('DATA = ')
        pprint.pprint(DATA, stream=f, indent=4, width=120)
        f.write('\n')
    print('Generated scratch/day_data_018.py successfully.')
