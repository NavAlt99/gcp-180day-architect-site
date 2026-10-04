"""Assembler for Day 12 durable spec scratch/day_data_012.py."""

import pprint
from scratch.generate_day_012 import (
    ACCESS_DATE,
    SOURCES,
    PART1_HTML,
    FIG_12_1_HTML,
    FIG_12_2_HTML,
    FIG_12_3_HTML,
)
from scratch.day_012_part1 import TOPIC_01_TECH
from scratch.day_012_part2 import TOPIC_02_TECH
from scratch.day_012_part3 import TOPIC_03_TECH
from scratch.day_012_scenarios_labs import SCENARIOS, LABS

def build_data():
    tech1 = TOPIC_01_TECH.replace('{FIG_12_1_HTML}', FIG_12_1_HTML)
    tech2 = TOPIC_02_TECH.replace('{FIG_12_2_HTML}', FIG_12_2_HTML)
    tech3 = TOPIC_03_TECH.replace('{FIG_12_3_HTML}', FIG_12_3_HTML)

    completion_html = '''<div class="completion-box" id="completion-box-012">
<h3>Day 12 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-12-1"> <label for="check-12-1">Geographic hierarchy mastered: evaluated Edge PoPs, Regions, Zones, and Multi-Regions against latency, residency, and failure domain boundaries.</label></li>
<li><input type="checkbox" id="check-12-2"> <label for="check-12-2">Scaling mechanics differentiated: compared vertical scaling limits and reboot downtime against horizontal stateless elasticity and connection pooling.</label></li>
<li><input type="checkbox" id="check-12-3"> <label for="check-12-3">Downstream protection designed: incorporated PgBouncer and predictive autoscaling to prevent database saturation death spirals.</label></li>
<li><input type="checkbox" id="check-12-4"> <label for="check-12-4">Cloud economics modeled: structured a 6-part production Bill of Materials across compute, storage, egress, and operational fees.</label></li>
<li><input type="checkbox" id="check-12-5"> <label for="check-12-5">Exit evidence verified: generated authoritative Location Decision Artifact balancing latency, GDPR compliance, cost, and failure-domain assumptions.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-012" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 12 Completed':'Mark Day 12 as Read';">Mark Day 12 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-012" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''

    topics = [
        {
            'key': 'topic-01',
            'title': 'Regions, zones, multi-region and edge locations',
            'anchors': {
                'overview': 'topic-01-overview',
                'technical': 'topic-01-technical',
                'problem': 'topic-01-problem',
                'lab': 'topic-01-lab'
            },
            'overview': 'Google Cloud infrastructure organizes global computing resources across a hierarchy of Edge Points of Presence (PoPs), independent geographic Regions, physically isolated Zones, and Multi-Region collections. Edge locations terminate incoming user connections via Anycast BGP routing, while regions and zones establish physical failure isolation boundaries with sub-millisecond inter-zone connectivity. Mastering these tiers enables architects to satisfy strict user latency budgets and regulatory data residency requirements while eliminating single points of failure.',
            'preview': 'A retail checkout service running in a single availability zone experiences a 4-hour total blackout when a local utility substation trips. Migrating to a Regional Managed Instance Group distributed across three zones guarantees automatic, sub-minute failover with zero customer transaction loss.',
            'technical': tech1,
            'questions': [
                'How do Edge PoPs and Anycast BGP routing reduce end-user latency compared to standard public internet routing?',
                'Under what architectural conditions is a dual-region deployment preferred over a single regional multi-zone architecture?',
                'Why does synchronous cross-region data replication introduce latency trade-offs compared to zonal replication?'
            ],
            'reference': 'https://docs.cloud.google.com/compute/docs/regions-zones#choose',
            'reference_label': 'Google Cloud Compute Engine — Regions and zones (accessed 2026-10-04)',
            'scenario': SCENARIOS['topic-01'],
            'lab': LABS['topic-01']
        },
        {
            'key': 'topic-02',
            'title': 'Elasticity vs scalability, vertical vs horizontal scaling',
            'anchors': {
                'overview': 'topic-02-overview',
                'technical': 'topic-02-technical',
                'problem': 'topic-02-problem',
                'lab': 'topic-02-lab'
            },
            'overview': 'Scalability defines the structural capacity of a system to handle increased throughput by adding resources, whereas elasticity is the autonomous, real-time dynamic adjustment of capacity to match immediate demand. Vertical scaling modifies the compute parameters of a single instance but requires downtime reboots and hits physical hardware ceilings. Horizontal scaling adds independent stateless nodes behind a load balancer, providing virtually limitless headroom when combined with downstream connection multiplexing.',
            'preview': 'An uncoordinated flash-sale autoscaling surge spawns 120 Compute Engine instances that open 3,000 connections to PostgreSQL, crashing the database and triggering an autoscaling death spiral. Introducing PgBouncer connection multiplexing and predictive autoscaling stabilizes the state tier while absorbing 9,500 requests per second.',
            'technical': tech2,
            'questions': [
                'What distinguishes structural system scalability from real-time dynamic elasticity?',
                'Why does vertical scaling inherently require planned downtime for Compute Engine virtual machines?',
                'How does an autoscaling compute tier cause saturation cascades in downstream relational databases, and how does connection pooling mitigate this?'
            ],
            'reference': 'https://docs.cloud.google.com/compute/docs/autoscaler#autoscaling_policy',
            'reference_label': 'Google Cloud Compute Engine — Autoscaling groups of instances (accessed 2026-10-04)',
            'scenario': SCENARIOS['topic-02'],
            'lab': LABS['topic-02']
        },
        {
            'key': 'topic-03',
            'title': 'CapEx vs OpEx, pay-as-you-go economics',
            'anchors': {
                'overview': 'topic-03-overview',
                'technical': 'topic-03-technical',
                'problem': 'topic-03-problem',
                'lab': 'topic-03-lab'
            },
            'overview': 'Cloud computing shifts enterprise financial mechanics from capitalized hardware investments (CapEx) depreciated over years to flexible operational expenses (OpEx) billed by the second. True cloud financial engineering requires evaluating the full six-dimension Bill of Materials (BOM)—encompassing compute, persistent storage, object storage operations, network egress, managed backing services, and observability. Architects balance on-demand pricing with Committed Use Discounts (CUDs) and Spot VMs to achieve 50–70% cost efficiencies under proactive FinOps governance.',
            'preview': 'A cloud migration budget estimates only VM compute and disk storage, resulting in a 320% monthly invoice blowout driven by unmonitored cross-zone egress, NAT processing fees, and storage API operations. Implementing Private Service Connect, regional caching, and lifecycle rules restores monthly spend to within budget.',
            'technical': tech3,
            'questions': [
                'How does the transition from CapEx to OpEx change the architectural risk profile of enterprise computing?',
                'What are the six distinct cost dimensions comprising a production Cloud Bill of Materials beyond raw compute?',
                'Why do Google Cloud Billing Budgets and alerts require programmatic automation rather than simple email alerts to prevent runaway spending?'
            ],
            'reference': 'https://docs.cloud.google.com/billing/docs/how-to/estimate-costs#access-pricing-calculator',
            'reference_label': 'Google Cloud Billing — Estimate your monthly costs (accessed 2026-10-04)',
            'scenario': SCENARIOS['topic-03'],
            'lab': LABS['topic-03']
        }
    ]

    data = {
        'contract_version': 2,
        'day': 12,
        'day_padded': '012',
        'title': 'Regions, scaling and economics',
        'work_block': 'Days 1–17 — Foundations',
        'time_estimate': '2–3 hours',
        'prerequisites': 'Day 5 (Network tiers, routing and hybrid connectivity), Day 11 (Cloud service models and responsibility); bring their exit artifacts.',
        'roadmap_practice': "Estimate two deployment locations and compare vertical versus horizontal scaling for the retailer's hypothetical workload.",
        'roadmap_exit': "A location decision with latency, residency, cost and failure-domain assumptions.",
        'part1_html': PART1_HTML,
        'part1_intro': "Day 12 establishes the foundational physical and economic principles of Google Cloud architecture, covering geographic topology (regions, zones, edge PoPs), scaling mechanisms (elasticity vs scalability, vertical vs horizontal), and financial economics (CapEx vs OpEx, pay-as-you-go metering, and Cloud BOM).",
        'part2_intro': "The technical discussions below dissect Google Cloud's physical network backbone and failure isolation domains, the mechanics of autoscaling and downstream connection bottlenecks, and the multi-dimensional economics of Committed Use Discounts, per-second metering, and cloud FinOps.",
        'part3_intro': "Production failure incidents illustrate the operational risks of single-zonal architectures, the fatal feedback loop of uncoordinated autoscaler cascades, and unmonitored egress bandwidth blowouts, coupled with defensible architectural remediations.",
        'part4_intro': "The executable exercises guide the architect through location latency and cost trade-off modeling, a comparative vertical versus horizontal scaling benchmark, and the production of an authoritative location decision artifact.",
        'exit_summary': "Completion of Day 12 delivers an authoritative, verified Location Decision Artifact evaluating deployment regions across latency, data residency, bill-of-materials cost, and failure-domain resilience assumptions for an enterprise retailer.",
        'completion_html': completion_html,
        'access_date': ACCESS_DATE,
        'sources': SOURCES,
        'topics': topics
    }

    return data

def main():
    data = build_data()
    content = f'''#!/usr/bin/env python3
"""Durable specification for Day 12."""

ACCESS_DATE = {repr(ACCESS_DATE)}

SOURCES = {repr(SOURCES)}

DATA = {pprint.pformat(data, indent=2, width=120)}
'''
    with open('scratch/day_data_012.py', 'w') as f:
        f.write(content)
    print("Successfully assembled scratch/day_data_012.py")

if __name__ == '__main__':
    main()
