"""Assemble Day 13 data spec into scratch/day_data_013.py."""

import pprint
from scratch.generate_day_013 import ACCESS_DATE, SOURCES, PART1_HTML, FIG_13_1_HTML, FIG_13_2_HTML
from scratch.day_013_part1 import TOPIC_01_TECH
from scratch.day_013_part2 import TOPIC_02_TECH
from scratch.day_013_scenarios_labs import SCENARIOS, LABS

COMPLETION_HTML = '''<div class="completion-box" id="completion-box-013">
<h3>Day 13 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-13-1"> <label for="check-13-1">Resilience boundaries mastered: differentiated High Availability multi-zone failover, Fault Tolerance zero-downtime consensus, and Disaster Recovery cross-region reconstitution.</label></li>
<li><input type="checkbox" id="check-13-2"> <label for="check-13-2">Recovery objectives quantified: mapped RTO and RPO trade-offs against exponential cost curves and synchronous vs asynchronous data replication.</label></li>
<li><input type="checkbox" id="check-13-3"> <label for="check-13-3">Replication trap eliminated: established that live replicas mirror logical corruption and verified point-in-time recovery (PITR) procedures.</label></li>
<li><input type="checkbox" id="check-13-4"> <label for="check-13-4">State architecture decoupled: externalized ephemeral worker state to durable database constraints and high-speed in-memory caches.</label></li>
<li><input type="checkbox" id="check-13-5"> <label for="check-13-5">Exit evidence verified: executed local state survival tests and authored authoritative State Ownership and Recovery Architecture Artifact.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-013" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 13 Completed':'Mark Day 13 as Read';">Mark Day 13 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-013" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''

topic_01_tech_rendered = TOPIC_01_TECH.replace('{FIG_13_1_HTML}', FIG_13_1_HTML)
topic_02_tech_rendered = TOPIC_02_TECH.replace('{FIG_13_2_HTML}', FIG_13_2_HTML)

DATA = {
    'contract_version': 2,
    'day': 13,
    'day_padded': '013',
    'title': 'Day 13 — State, availability and recovery vocabulary',
    'time_estimate': '2–3 hours',
    'prerequisites': 'Day 12; bring their exit artifacts.',
    'roadmap_practice': 'Restart the local service with and without external state; distinguish an available replica from a recoverable backup.',
    'roadmap_exit': 'A state ownership diagram and definitions of HA, fault tolerance, RTO and RPO with examples.',
    'exit_summary': 'Completion of Day 13 delivers an authoritative State Ownership and Recovery Architecture Artifact, mapping state persistence boundaries, failure domains, and verified point-in-time recovery workflows across High Availability, Fault Tolerance, and Disaster Recovery topologies.',
    'work_block': 'Days 1–17 — Foundations',
    'access_date': ACCESS_DATE,
    'sources': SOURCES,
    'part1_intro': 'Day 13 establishes the non-negotiable architectural vocabulary and principles governing system resilience, contrasting High Availability, Fault Tolerance, and Disaster Recovery, while analyzing the profound operational consequences of stateless versus stateful application topologies.',
    'part2_intro': 'The technical analyses below detail failure domain boundaries, RTO/RPO trade-off curves, the critical differences between replication and point-in-time recovery, and state isolation mechanics across Compute Engine and managed data tiers.',
    'part3_intro': 'Production failure incidents illustrate the destructive replication trap where high-availability standby replicas mirror logical corruption, and the catastrophic risk of ephemeral worker restart when transaction deduplication state is stored in process memory.',
    'part4_intro': 'The hands-on exercises demonstrate local service state survival across process restarts, reproduce the failure of active replication during logical data deletion, execute point-in-time recovery to restore lost transactions, and author an authoritative state ownership decision document.',
    'part1_html': PART1_HTML,
    'completion_html': COMPLETION_HTML,
    'topics': [
        {
            'key': 'topic-01',
            'title': 'High availability vs fault tolerance vs disaster recovery (three different things)',
            'anchors': {
                'overview': 'topic-01-overview',
                'technical': 'topic-01-technical',
                'problem': 'topic-01-problem',
                'lab': 'topic-01-lab'
            },
            'reference': SOURCES['topic-01'][1],
            'reference_label': SOURCES['topic-01'][0],
            'overview': 'Resilience architectures are governed by three distinct operational disciplines: High Availability (HA), Fault Tolerance (FT), and Disaster Recovery (DR). High availability designs minimize unplanned downtime through redundant components and automated failover, fault tolerance guarantees continuous uninterrupted operation with zero data loss across component failures, and disaster recovery reconstitutes critical systems after catastrophic regional disruptions. Understanding how Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO) dictate product selection separates professional cloud architects from naive builders.',
            'preview': 'Problem preview: A rogue migration script drops an enterprise production table across a high-availability database cluster, propagating the drop command to active read replicas within 200 milliseconds. The engineering team must execute a point-in-time recovery from an immutable backup archive to recover $850,000 in lost transaction records within a 2-hour RTO window.',
            'technical': topic_01_tech_rendered,
            'questions': [
                'Why does synchronous replication across multi-zone standby replicas fail to protect a database against accidental DROP TABLE or ransomware attacks?',
                'What are the engineering and economic trade-offs when shifting an application recovery profile from Cold Standby (backup and restore) to Warm Standby?',
                'How does the Recovery Point Objective (RPO) dictate whether data replication must be synchronous versus asynchronous across failure domains?'
            ],
            'scenario': SCENARIOS['topic-01'],
            'lab': LABS['topic-01']
        },
        {
            'key': 'topic-02',
            'title': 'Stateless vs stateful applications (this decides almost every HA design)',
            'anchors': {
                'overview': 'topic-02-overview',
                'technical': 'topic-02-technical',
                'problem': 'topic-02-problem',
                'lab': 'topic-02-lab'
            },
            'reference': SOURCES['topic-02'][1],
            'reference_label': SOURCES['topic-02'][0],
            'overview': 'Application state architecture dictates every downstream high-availability, autoscaling, and disaster-recovery design decision in cloud systems. Stateless applications treat local runtime instances as ephemeral and interchangeable workers, externalizing all customer sessions and persistence into managed distributed data tiers. Stateful applications maintain authoritative client state, local disk bindings, or ordered lifecycle identities on specific instances, requiring specialized storage attachment and persistent IP reservation.',
            'preview': 'Problem preview: An order-processing service caches pending fulfillment tokens in local worker process memory to avoid remote database latency, but crashes under an unhandled exception. Because pending transaction tokens were not externalized to Memorystore Redis or Cloud SQL, 1,420 uncommitted customer orders vanish permanently upon VM restart.',
            'technical': topic_02_tech_rendered,
            'questions': [
                'Why does storing in-flight transaction deduplication tokens in local process memory violate cloud elasticity and crash-tolerance principles?',
                'How do Stateful Managed Instance Groups (MIGs) preserve persistent data and network identities during VM auto-healing events?',
                'Under what architectural conditions should session state be externalized to an in-memory cache like Memorystore Redis versus a durable relational database like Cloud SQL?'
            ],
            'scenario': SCENARIOS['topic-02'],
            'lab': LABS['topic-02']
        }
    ]
}

if __name__ == '__main__':
    with open('scratch/day_data_013.py', 'w', encoding='utf-8') as f:
        f.write('"""Day 13 Durable Specification."""\n\n')
        f.write(f'ACCESS_DATE = {repr(ACCESS_DATE)}\n\n')
        f.write(f'SOURCES = {repr(SOURCES)}\n\n')
        f.write('DATA = ')
        pprint.pprint(DATA, stream=f, indent=2, width=120)
        f.write('\n')
    print('Successfully assembled scratch/day_data_013.py')
