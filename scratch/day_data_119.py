"""day_data_119.py — Exhaustive architecture data specification for Day 119.

Covers Cost Baseline and Commitments:
1. FinOps Principles: Inform, Optimise, Operate
2. Showback vs Chargeback: Financial accountability models and shared-cost allocation
3. Cost Visibility: Labeling taxonomy, Cloud Billing BigQuery Export, Looker Studio, Budgets/Alerts, Anomaly Detection
4. Compute Savings: Rightsizing, Spot VMs, CUDs (resource vs spend-based), SUDs, and Non-Prod Scheduling
Follows PAGE_AUTHORING_CONTRACT.md strictly with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 119

DATA = {
    'day': 119,
    'part1_intro': (
        'Day 119 opens Block 5 (Performance, Delivery, and Operations, Days 119–133) by establishing the economic foundation '
        'of enterprise Google Cloud architecture. Cloud financial engineering is not an accounting afterthought; it is an active '
        'architectural discipline where cost is treated as a first-class non-functional requirement alongside availability and latency. '
        'Architects examine the FinOps Foundation lifecycle—Inform, Optimise, Operate—and implement transparent cost allocation '
        'through rigorous resource labeling, Cloud Billing BigQuery exports, and Looker Studio telemetry. Crucially, architects '
        'evaluate compute optimization mechanisms: balancing automatic Sustained Use Discounts (SUDs), rightsizing recommenders, '
        'ephemeral Spot VMs, and Committed Use Discounts (CUDs). Rather than committing blindly to multi-year contracts, architects '
        'model fixed versus variable costs, quantify utilization uncertainty, and construct defensible financial commitment models.'
    ),
    'exit_summary': (
        'A dated cost baseline model with fixed/variable costs, utilization uncertainty, and commitment risk across rightsizing, '
        'Spot VMs, and flexible spend-based CUDs.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts Google Cloud compute cost optimization levers, discount profiles, flexibility '
        'trade-offs, commitment horizons, and operational risk factors across enterprise workload tiers.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Optimization Mechanism</th>\n'
        '<th>Typical Discount</th>\n'
        '<th>Commitment Term</th>\n'
        '<th>Flexibility &amp; Portability</th>\n'
        '<th>Operational Risk &amp; Trade-off</th>\n'
        '<th>Target Workload Profile</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>1. Sustained Use Discounts (SUDs)</strong></td>\n'
        '<td>Up to 30% (N1/N2)</td>\n'
        '<td>None (Automatic)</td>\n'
        '<td>High: Applies incrementally as vCPU/RAM run &gt;25% of month</td>\n'
        '<td>Zero commitment risk; however, unavailable on newer machine families (e.g. C3, N4, Tau T2D).</td>\n'
        '<td>Unpredictable baseline workloads on legacy or general-purpose VM families.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>2. Compute Engine Rightsizing</strong></td>\n'
        '<td>15% – 45%</td>\n'
        '<td>None</td>\n'
        '<td>High: Vertical scaling of vCPU/RAM based on Active Assist</td>\n'
        '<td>Requires VM reboot or rolling MIG update; risk of CPU throttling if peak headroom is underestimated.</td>\n'
        '<td>Over-provisioned legacy lift-and-shift VMs with &lt;15% average CPU utilization.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>3. Non-Prod Instance Scheduling</strong></td>\n'
        '<td>Up to 70%</td>\n'
        '<td>None</td>\n'
        '<td>High: Automated start/stop policies via Cloud Scheduler &amp; Pub/Sub</td>\n'
        '<td>Developer friction if testing outside business hours; warm-up latency on morning boot.</td>\n'
        '<td>Development, test, staging, and sandbox environments active only during office hours (50 hrs/wk).</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>4. Spot Virtual Machines</strong></td>\n'
        '<td>60% – 91%</td>\n'
        '<td>None</td>\n'
        '<td>Moderate: Subject to regional Compute Engine spare capacity</td>\n'
        '<td>Preemption risk: 30-second termination notice; zero availability SLA; requires fault-tolerant code.</td>\n'
        '<td>Stateless batch processing, video rendering, asynchronous CI/CD runners, and fault-tolerant GKE worker nodes.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>5. Flexible Spend-Based CUDs</strong></td>\n'
        '<td>28% (1-yr) / 46% (3-yr)</td>\n'
        '<td>1 or 3 Years</td>\n'
        '<td>Highest: Applies across all machine families, regions, GKE Autopilot, and Cloud Run</td>\n'
        '<td>Financial lock-in: Fixed hourly dollar spend commitment regardless of actual infrastructure usage.</td>\n'
        '<td>Dynamic architectures undergoing multi-cloud modernization, region migration, or container refactoring.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>6. Resource-Based CUDs</strong></td>\n'
        '<td>37% (1-yr) / 55% – 70% (3-yr)</td>\n'
        '<td>1 or 3 Years</td>\n'
        '<td>Low: Bound to specific machine family (e.g. N2) in a specific region</td>\n'
        '<td>Stranded cost risk: Cannot transfer discount if migrating families or moving workloads to another region.</td>\n'
        '<td>Stable, predictable 24/7 baseline infrastructure (e.g. enterprise relational databases, core ERP).</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 119: Enterprise FinOps Cost Visibility and Compute Savings Topology',
        'desc': 'FinOps operational architecture showing resource labeling, BigQuery detailed billing export, Looker Studio dashboards, automated instance scheduling, and multi-tier commitment coverage.',
        'caption': 'Figure 119.1: Enterprise FinOps architecture illustrating billing ingestion, proportional shared cost allocation, automated rightsizing recommendations, Spot VM provisioning, and layered CUD commitments.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Workload Identity & Resource Labeling Plane',
                'desc': 'Granular tags: cost_center, environment, team, and service enforced via Organization Policy',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Cloud Billing Detailed Export & Anomaly Telemetry Enclave',
                'desc': 'Streaming billing data to BigQuery with Looker Studio dashboards and Cloud Monitoring anomaly alerts',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Compute Optimization & Active Assist Recommendation Tier',
                'desc': 'Rightsizing recommenders, non-prod instance scheduling, and automated VM start/stop policies',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Ephemeral & Fault-Tolerant Compute Scaling Tier',
                'desc': 'Spot VMs for batch and stateless GKE workers with graceful 30-second SIGTERM drain handling',
                'y': 325,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            },
            {
                'name': 'LAYER 5: Committed Use Discount (CUD) Strategic Layering Plane',
                'desc': 'Core baseline covered by Resource CUDs (N2), dynamic layer by Flexible Spend CUDs, variable peaks On-Demand',
                'y': 430,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            }
        ],
        'components': [
            {'name': 'Resource Labeling Engine', 'detail': 'Enforces cost_center & env', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Showback Allocation Map', 'detail': 'Maps Projects to GL Units', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'BigQuery Billing Export', 'detail': 'Detailed Daily Usage & Cost', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Looker Studio & Anomaly Alert', 'detail': 'Detects >30% Spend Spikes', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Active Assist Rightsizer', 'detail': 'Shrinks vCPU/RAM for Low Use', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Cloud Scheduler Start/Stop', 'detail': '50 hrs/wk Non-Prod (70% Off)', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Spot VM Managed Pool', 'detail': '60-91% Off Batch/CI Tasks', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'Graceful Preemption Drain', 'detail': '30s Metadata Eviction Hook', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'Resource-Based CUDs', 'detail': '55% Off Stable Base (N2)', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Flexible Spend CUDs', 'detail': '46% Off Cross-Family/Cloud Run', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'}
        ],
        'boundaries': [
            {'label': 'FINANCIAL GOVERNANCE & TELEMETRY INGESTION BOUNDARY', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'DYNAMIC WORKLOAD OPTIMIZATION & SCHEDULING ENCLAVE', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'CAPITAL COMMITMENT & DISCOUNT ARBITRAGE DOMAIN', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#f43f5e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Propagate Labels to Sinks', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Stream Usage Ledger', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Trigger Anomaly Webhook', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Evaluate Rightsizing', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Execute Stop at 19:00', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Deploy Fault-Tolerant Jobs', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Trap 30s Preemption', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Cover 60% Core Baseline', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Arbitrage Variable Spikes', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: Allocation Coverage: Assert >= 95% of BigQuery Billing Records Labeled', 'badge': 'P1', 'color': '#818cf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: Non-Prod Efficiency: Assert Non-Prod Run Hours <= 55 hrs/week', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 450, 'label': 'PROBE 3: Commitment Utilization: Assert CUD Break-Even & Waste Rate < 5%', 'badge': 'P3', 'color': '#f43f5e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world cloud financial engineering crises. '
        'Case 1 explores an enterprise committing prematurely to rigid 3-year resource-based CUDs prior to containerization, '
        'resulting in massive stranded commitment waste. Case 2 examines an inter-departmental chargeback war over unallocated '
        'shared Cloud Interconnect and Cloud NAT bandwidth, detailing how proportional attribution restores trust. '
        'Case 3 investigates a silent weekend billing surge caused by unmonitored GPU instances, resolved through BigQuery anomaly alerting. '
        'Case 4 demonstrates how naive rightsizing caused severe database CPU throttling during black Friday peak traffic.'
    ),
    'part4_intro': (
        'These hands-on architectural exercises implement the complete FinOps and compute economics lifecycle. '
        'Architects build a multi-stage cost baseline and commitment risk modeling engine in Python, evaluate trade-offs between '
        'On-Demand, Spot VMs, and CUDs under utilization uncertainty, and generate a production-ready dated cost model artifact.'
    ),
    'topics': [
        # TOPIC 1
        {
            'key': 'topic-01',
            'title': 'FinOps principles',
            'overview': (
                'Cloud financial management operates on the principles established by the FinOps Foundation: Inform, Optimise, and Operate. '
                'Rather than viewing infrastructure spending as a fixed capital expense managed once a year by procurement, FinOps converts '
                'cloud economics into a continuous, real-time operating model. Engineers, finance leaders, and product owners collaborate '
                'to understand unit costs, optimize resource consumption, and make data-driven trade-offs between speed, quality, and cost. '
                'Understanding the distinct maturity phases—Crawl, Walk, and Run—allows architects to guide enterprise migrations from '
                'chaotic unallocated cloud bills to sophisticated unit-economic optimization.'
            ),
            'preview': (
                'An enterprise attempts to optimize cloud costs through top-down procurement decrees, purchasing 3-year CUDs for an '
                'application that is slated for decommissioning in 6 months, creating an unavoidable $240,000 financial liability.'
            ),
            'technical': (
                'FinOps is structured into three iterative phases executed continuously across an organization\'s cloud portfolio:\n\n'
                '### 1. The FinOps Lifecycle Phases\n'
                '- **Inform (Visibility and Allocation)**:\n'
                '  - The foundational prerequisite of FinOps. Teams cannot optimize what they cannot measure.\n'
                '  - Involves continuous cost visibility, resource attribution, showback reporting, and benchmarking.\n'
                '  - In Google Cloud, this is achieved by streaming Cloud Billing detailed export data to BigQuery, creating Looker Studio dashboards, and mapping Google Cloud projects to corporate cost centers.\n'
                '- **Optimise (Rate and Usage Reduction)**:\n'
                '  - Focuses on two orthogonal levers: Rate Optimization (paying less for the resources you use) and Usage Optimization (using fewer resources to achieve the same business outcome).\n'
                '  - Rate levers include Committed Use Discounts (resource-based vs spend-based) and Spot VMs.\n'
                '  - Usage levers include VM rightsizing, idle disk deletion, Cloud Storage lifecycle transitions, and GKE cluster autoscaling.\n'
                '- **Operate (Continuous Governance and Unit Economics)**:\n'
                '  - Integrates financial accountability into CI/CD pipelines, daily SRE standups, and architectural design reviews.\n'
                '  - Shifts focus from gross cloud spend to **Unit Economics** (e.g. cost per processed transaction, cost per active subscriber).\n'
                '  - Establishes automated budget alerting, real-time anomaly detection, and automated non-production resource scheduling.\n\n'
                '### 2. The Crawl, Walk, Run FinOps Maturity Model\n'
                '- **Crawl**: Basic centralized cost visibility; monthly manual billing reviews; >50% untagged resources; reactive optimization.\n'
                '- **Walk**: Automated daily BigQuery exports; standardized labeling policy enforced by Terraform; decentralized showback reports delivered to engineering leads; proactive CUD purchases covering 50% baseline.\n'
                '- **Run**: 100% automated chargeback to business units; unit-economic dashboards integrated into executive reporting; automated anomaly detection with Cloud Functions webhook containment; 75%+ commitment coverage with automated risk hedging.'
            ),
            'questions': [
                'What is the fundamental difference between Rate Optimization and Usage Optimization in the FinOps framework?',
                'Why does the FinOps lifecycle mandate completing the Inform phase before executing major Optimise commitments?',
                'How do Unit Economics metrics (e.g. cost per active user) provide superior business insight compared to total monthly gross cloud spend?'
            ],
            'reference': 'https://www.finops.org/framework/',
            'reference_label': 'FinOps Foundation Official Framework & Principles',
            'scenario': {
                'symptom': 'Central procurement purchased $35,000/month in 3-year N1 resource-based CUDs, completely unaware that engineering was halfway through migrating the entire service to serverless Cloud Run.',
                'impact': '$21,000/month in stranded, unutilized CUD commitments for the next 2.5 years ($630,000 total unrecoverable waste).',
                'constraints': 'Cannot cancel active CUD contracts; must maximize utilization of existing commitments while continuing modernization.',
                'evidence': (
                    'FinOps Audit Log Extract:\n\n'
                    '```text\n'
                    'Commitment ID: cud-res-n1-uscentral1-3yr-0912\n'
                    'Purchased: 2025-06-01 | Expiration: 2028-06-01 | Family: N1 | Region: us-central1\n'
                    'Committed vCPUs: 512 | Active Running N1 vCPUs (Nov 2026): 64\n'
                    'Commitment Utilization Rate: 12.5% | Monthly Waste: $21,450.00\n'
                    'Root Cause: Procurement operated in isolation without architectural roadmap input.\n'
                    '```'
                ),
                'diagnostic_steps': [
                    'Step 1: Query BigQuery Cloud Billing export table to determine the exact hourly unutilized CUD liability.',
                    'Step 2: Inspect organization project inventory to find batch workloads (e.g. data pipelines, CI/CD runners) that can be migrated to N1 machines to absorb the stranded commitment.',
                    'Step 3: Establish a cross-functional Cloud Financial Review Board bridging Enterprise Architecture, SRE, and Finance.',
                    'Step 4: Update procurement governance: All multi-year commitments require formal sign-off from the Lead Cloud Architect.'
                ],
                'root': 'Disconnection between procurement and engineering architecture; violating the FinOps Inform principle by purchasing long-term commitments without visibility into the application lifecycle.',
                'fix': 'Migrate auxiliary batch workloads and secondary environments to N1 machines to absorb 80% of the stranded CUD capacity, and institute a mandatory FinOps review gate for all commitments exceeding 1 year.',
                'verify': 'Query BigQuery billing table to verify N1 commitment utilization improves from 12.5% to >90%, reducing monthly stranded spend to <$2,000.',
                'residual': 'N1 machines possess lower price-performance ratios compared to newer N4/C3 instances, representing an ongoing technical efficiency trade-off until contract maturity.',
                'diagram': (
                    'Procurement buys 3-year N1 CUDs without consulting engineering leads',
                    'Engineering migrates workloads to serverless Cloud Run simultaneously',
                    'Commitment utilization plunges to 12.5%, burning $21.4k/mo in stranded waste',
                    'Institute FinOps cross-functional review; retarget batch workloads to absorb N1 capacity',
                    'Commitment utilization restored to 92%; mandatory architectural sign-off established'
                )
            },
            'lab': {
                'name': 'FinOps Lifecycle Maturity & Unit-Economic Modeling Engine',
                'file': 'day-119-finops-lifecycle.md',
                'goal': 'Implement a Python FinOps engine that models Inform, Optimise, and Operate metrics, tracking monthly gross spend, unit cost per transaction, and commitment coverage across architecture migration waves.',
                'expected': 'A Python tool parsing usage telemetry, calculating unit economics, and demonstrating how FinOps governance eliminates stranded commitment waste.',
                'mode': 'local Python 3 simulation; zero cloud spend',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/finops-baseline-lab</kbd>.',
                'steps': [
                    (
                        '#### Define FinOps Workload Telemetry & Financial Model Specification\n'
                        'Create the working directory and write a JSON specification detailing monthly cloud spend, transaction volumes, commitment coverage, and architectural migration milestones:\n\n'
                        '```sh\n'
                        'mkdir -p ~/finops-baseline-lab && cd ~/finops-baseline-lab\n'
                        'cat <<\'EOF\' > finops_spec.json\n'
                        '{\n'
                        '  "enterprise": "Global Retail Logistics Cloud",\n'
                        '  "monthly_data": [\n'
                        '    {"month": "2026-07", "gross_spend": 85000, "transactions": 1200000, "labeled_pct": 52, "cud_utilization": 95},\n'
                        '    {"month": "2026-08", "gross_spend": 92000, "transactions": 1450000, "labeled_pct": 68, "cud_utilization": 94},\n'
                        '    {"month": "2026-09", "gross_spend": 88000, "transactions": 1600000, "labeled_pct": 84, "cud_utilization": 72},\n'
                        '    {"month": "2026-10", "gross_spend": 81000, "transactions": 1850000, "labeled_pct": 96, "cud_utilization": 92}\n'
                        '  ]\n'
                        '}\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the FinOps Lifecycle & Unit Economics Analyzer\n'
                        'Author a Python script that calculates unit costs per transaction, evaluates labeling attribution progress, checks commitment health, and compiles a FinOps maturity scorecard:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > evaluate_finops_lifecycle.py\n'
                        'import json\n'
                        'import sys\n'
                        '\n'
                        'def evaluate_finops():\n'
                        '    print("================================================================================")\n'
                        '    print("DAY 119: FINOPS LIFECYCLE MATURITY & UNIT ECONOMICS ANALYZER")\n'
                        '    print("================================================================================\\n")\n'
                        '\n'
                        '    with open("finops_spec.json", "r") as f:\n'
                        '        spec = json.load(f)\n'
                        '\n'
                        '    print(f"{\'Month\':<10} | {\'Gross Spend\':<12} | {\'Txn Volume\':<12} | {\'Unit Cost ($/Txn)\':<18} | {\'Labeled %\':<10} | {\'CUD Util %\'}")\n'
                        '    print("-" * 88)\n'
                        '\n'
                        '    initial_unit_cost = None\n'
                        '    latest_unit_cost = None\n'
                        '\n'
                        '    for record in spec["monthly_data"]:\n'
                        '        m = record["month"]\n'
                        '        spend = record["gross_spend"]\n'
                        '        txns = record["transactions"]\n'
                        '        unit_cost = spend / txns\n'
                        '        lbl = record["labeled_pct"]\n'
                        '        util = record["cud_utilization"]\n'
                        '\n'
                        '        if initial_unit_cost is None:\n'
                        '            initial_unit_cost = unit_cost\n'
                        '        latest_unit_cost = unit_cost\n'
                        '\n'
                        '        print(f"{m:<10} | ${spend:<11,d} | {txns:<12,d} | ${unit_cost:<17.4f} | {lbl:<9d}% | {util}%")\n'
                        '\n'
                        '    print("-" * 88)\n'
                        '    reduction_pct = ((initial_unit_cost - latest_unit_cost) / initial_unit_cost) * 100\n'
                        '    print(f"Initial Unit Cost: ${initial_unit_cost:.4f} per transaction")\n'
                        '    print(f"Latest Unit Cost:  ${latest_unit_cost:.4f} per transaction")\n'
                        '    print(f"Unit Cost Efficiency Improvement: {reduction_pct:.2f}% (Spend dropped while volume grew 54%)\\n")\n'
                        '\n'
                        '    assert latest_unit_cost < initial_unit_cost, "FinOps Operate failure: Unit economics did not improve!"\n'
                        '    assert spec["monthly_data"][-1]["labeled_pct"] >= 95, "FinOps Inform failure: Labeled allocation below 95%!"\n'
                        '    print(">> FINOPS MATURITY VERDICT: PASSED (Walk -> Run Phase Achieved).")\n'
                        '    print("================================================================================")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    evaluate_finops()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Run the FinOps Lifecycle Evaluation Script\n'
                        'Execute the script and verify that unit cost efficiency improves as visibility matures:\n\n'
                        '```sh\n'
                        'python3 evaluate_finops_lifecycle.py\n'
                        '```'
                    )
                ],
                'accept': 'Executable Python FinOps lifecycle engine demonstrating Inform, Optimise, and Operate metrics, tracking unit cost per transaction and labeling compliance.',
                'verification': 'Review terminal output of <kbd>python3 evaluate_finops_lifecycle.py</kbd> confirming FINOPS MATURITY VERDICT: PASSED.',
                'trouble': 'If assertions trigger, inspect `finops_spec.json` to confirm the final month has labeled_pct >= 95.',
                'cleanup': 'Remove temporary files: <kbd>rm -f finops_spec.json evaluate_finops_lifecycle.py</kbd>.',
                'file': 'day-119-finops-lifecycle.md'
            }
        },
        # TOPIC 2
        {
            'key': 'topic-02',
            'title': 'Showback vs chargeback',
            'overview': (
                'Financial accountability in cloud platforms is enforced through either Showback or Chargeback models. '
                'Showback provides complete visibility into resource consumption, attributing costs to business units and engineering teams '
                'on informational dashboards without altering real general ledger (GL) departmental budgets. It builds awareness, '
                'fosters competitive efficiency, and avoids early friction. Conversely, Chargeback executes real inter-departmental '
                'financial cross-charging, directly debiting departmental budget accounts for their cloud usage. While chargeback drives '
                'rigorous financial discipline, it requires sophisticated shared-cost allocation rules to equitably distribute common infrastructure '
                'such as Cloud Interconnect, shared GKE clusters, Cloud NAT gateways, and organization-wide security tools.'
            ),
            'preview': (
                'An enterprise rushes to implement chargeback, but dumps $60,000/month of unallocated shared Cloud NAT and Dedicated '
                'Interconnect bills into a single division\'s account, triggering an inter-departmental executive crisis.'
            ),
            'technical': (
                'Choosing and implementing financial attribution models requires clear architectural rules for allocating shared services.\n\n'
                '### 1. Architectural Comparison: Showback vs Chargeback\n'
                '- **Showback (Informational Accountability)**:\n'
                '  - Reports exact monthly spend to team leads, product managers, and engineering directors.\n'
                '  - Generates "virtual invoices" comparing teams against organizational benchmarks and budget forecasts.\n'
                '  - Does not debit corporate ERP general ledgers; zero accounting resistance.\n'
                '  - Best suited for early cloud adoption, innovation sandboxes, and shared R&D environments.\n'
                '- **Chargeback (Transactional Accountability)**:\n'
                '  - Integrates cloud billing directly into SAP/Oracle financial ledgers with monthly journal entries.\n'
                '  - Enforces hard budget limits: If a business unit overspends, their project quota is capped or requires executive approval.\n'
                '  - Eliminates "free-rider" problems where teams spin up expensive un-optimized clusters on a central IT budget.\n'
                '  - Requires 100% dispute resolution mechanisms and mathematically defensible shared-cost distribution.\n\n'
                '### 2. The Shared-Cost Allocation Problem\n'
                'Enterprises maintain shared infrastructure that cannot be tagged to a single service account or team:\n'
                '- **Shared Networking**: Cloud Interconnect (10 Gbps pipes @ $1,500/mo base), Cloud NAT gateways, Shared VPC host project firewall rules.\n'
                '- **Centralized Security**: Security Command Center Enterprise, Cloud KMS HSM key rings, Cloud DLP inspection templates.\n'
                '- **Shared Multi-Tenant Runtimes**: Multi-tenant GKE clusters running pods across 14 different engineering teams.\n\n'
                '### 3. Shared-Cost Distribution Methodologies\n'
                '1. **Proportional Consumption Split (Recommended)**: Shared costs are allocated to business units in direct proportion to their directly attributable spend. If Business Unit A consumes 60% of total compute vCPUs, it absorbs 60% of the shared Interconnect and Cloud NAT fee.\n'
                '2. **Even Split (Flat Overhead)**: Shared costs are divided equally among all active projects regardless of size. Distorts economics by heavily penalizing small pilot projects.\n'
                '3. **Central IT Absorption**: Central IT absorbs all shared networking and security costs as corporate overhead. Encourages wasteful network egress since individual teams see zero marginal cost for external bandwidth.'
            ),
            'questions': [
                'Under what organizational conditions is Showback preferable to full financial Chargeback?',
                'Why does allocating shared Cloud Interconnect costs via an Even Split penalize smaller innovation projects unfairly?',
                'How does Proportional Consumption Split align team incentives to optimize both direct compute and shared network resources?'
            ],
            'reference': 'https://docs.cloud.google.com/architecture/framework/cost-optimization',
            'reference_label': 'Google Cloud Architecture Framework: Cost Allocation & Financial Governance',
            'scenario': {
                'symptom': 'Business Unit B (Mobile App) receives a $45,000 chargeback bill for Cloud Interconnect and Cloud NAT, despite generating only $3,200 in direct Compute Engine usage.',
                'impact': 'Mobile VP halts cloud deployment; finance freezes cross-charging; engineering teams refuse to adopt shared VPCs.',
                'constraints': 'Must establish an equitable, automated shared-cost distribution model in BigQuery without breaking existing billing exports.',
                'evidence': (
                    'Corporate Ledger Dispute Audit:\n\n'
                    '```text\n'
                    'Invoice ID: CHG-2026-11-MOB\n'
                    'Account: Business Unit B (Mobile Apps)\n'
                    'Direct Compute Usage (Cloud Run & Cloud SQL): $3,210.40\n'
                    'Shared Networking Overhead Allocated:        $45,000.00 (100% of Shared VPC Interconnect!)\n'
                    'Total Invoiced:                              $48,210.40\n'
                    'Dispute: Central IT assigned entire Shared VPC host project bill to BU-B because BU-B was alphabetized first.\n'
                    '```'
                ),
                'diagnostic_steps': [
                    'Review BigQuery billing SQL queries used by the finance department for monthly chargeback journal entries.',
                    'Discover that the billing query grouped by `project.id` and dumped all unlabelled `shared-vpc-host` networking SKUs into BU-B.',
                    'Calculate the true proportional usage: BU-B generated 4.8% of total network bytes, while BU-A (Data Analytics) generated 88.4%.',
                    'Implement a two-stage BigQuery SQL view that calculates total shared costs and apportions them based on each BU\'s percentage of total egress bandwidth.'
                ],
                'root': 'Naive chargeback implementation assigning 100% of shared infrastructure to an arbitrary project rather than calculating proportional consumption.',
                'fix': 'Author a BigQuery SQL chargeback view that dynamically splits unallocated shared networking costs proportionally based on each business unit\'s direct egress bytes.',
                'verify': 'Re-run the monthly financial chargeback allocation; verify BU-B is billed $2,160 for shared networking (4.8%) instead of $45,000.',
                'residual': 'Very small microservices with zero network egress pay $0 for shared network pipes, effectively receiving a minor subsidy from data-heavy workloads.',
                'diagram': (
                    'Finance implements naive chargeback; dumps $45k shared VPC bill onto BU-B',
                    'BU-B mobile app project receives $48.2k invoice on $3.2k direct usage',
                    'Mobile VP halts cloud adoption; engineering leadership disputes billing model',
                    'Implement Proportional Shared Cost Engine in BigQuery based on direct egress bytes',
                    'BU-B bill corrected to $5.3k ($3.2k direct + $2.1k shared); equitable chargeback restored'
                )
            },
            'lab': {
                'name': 'Shared-Cost Proportional Chargeback Allocation Engine',
                'file': 'day-119-chargeback-allocation.md',
                'goal': 'Develop a Python financial allocation engine that processes raw multi-project billing records, separates direct costs from shared infrastructure, and distributes shared costs proportionally across business units.',
                'expected': 'An executable Python script taking raw billing entries, calculating proportional weights, and outputting an auditable chargeback ledger with zero unallocated residue.',
                'mode': 'local Python 3 data processing; zero cloud spend',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Ensure <kbd>~/finops-baseline-lab</kbd> exists.',
                'steps': [
                    (
                        '#### Define Raw Billing & Shared Infrastructure Specification\n'
                        'Write a JSON dataset simulating monthly billing exports containing both direct project costs and shared infrastructure lines (Interconnect, Cloud NAT):\n\n'
                        '```sh\n'
                        'cd ~/finops-baseline-lab\n'
                        'cat <<\'EOF\' > raw_billing.json\n'
                        '{\n'
                        '  "billing_period": "2026-11",\n'
                        '  "direct_projects": [\n'
                        '    {"bu": "BU-Analytics",  "project": "proj-analytics-prod",  "direct_spend": 55000.0, "egress_gb": 48000},\n'
                        '    {"bu": "BU-Ecommerce",  "project": "proj-ecommerce-prod",  "direct_spend": 32000.0, "egress_gb": 22000},\n'
                        '    {"bu": "BU-MobileApp",  "project": "proj-mobile-prod",     "direct_spend": 5000.0,  "egress_gb": 3500},\n'
                        '    {"bu": "BU-InternalIT", "project": "proj-internal-tools",  "direct_spend": 8000.0,  "egress_gb": 1500}\n'
                        '  ],\n'
                        '  "shared_infrastructure": [\n'
                        '    {"service": "Dedicated Interconnect 10G", "spend": 12000.0},\n'
                        '    {"service": "Cloud NAT Gateway Egress",   "spend": 8000.0},\n'
                        '    {"service": "Security Command Center Ent","spend": 5000.0}\n'
                        '  ]\n'
                        '}\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Proportional Chargeback Calculator\n'
                        'Author a Python script that computes proportional consumption weights and produces an auditable chargeback invoice for each business unit:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > calculate_chargeback.py\n'
                        'import json\n'
                        '\n'
                        'def run_chargeback():\n'
                        '    print("================================================================================")\n'
                        '    print("DAY 119: PROPORTIONAL SHARED-COST CHARGEBACK ALLOCATION ENGINE")\n'
                        '    print("================================================================================\\n")\n'
                        '\n'
                        '    with open("raw_billing.json", "r") as f:\n'
                        '        data = json.load(f)\n'
                        '\n'
                        '    direct_total = sum(p["direct_spend"] for p in data["direct_projects"])\n'
                        '    shared_total = sum(s["spend"] for s in data["shared_infrastructure"])\n'
                        '    total_egress = sum(p["egress_gb"] for p in data["direct_projects"])\n'
                        '\n'
                        '    print(f"Total Direct Project Spend: ${direct_total:,.2f}")\n'
                        '    print(f"Total Shared Overhead Spend: ${shared_total:,.2f}")\n'
                        '    print(f"Combined Enterprise Spend:    ${direct_total + shared_total:,.2f}\\n")\n'
                        '\n'
                        '    print(f"{\'Business Unit\':<16} | {\'Direct Spend\':<14} | {\'Egress %\':<10} | {\'Shared Alloc\':<14} | {\'Total Invoiced\':<14} | {\'Effective Overhead %\'}")\n'
                        '    print("-" * 96)\n'
                        '\n'
                        '    allocated_shared_sum = 0.0\n'
                        '    for p in data["direct_projects"]:\n'
                        '        bu = p["bu"]\n'
                        '        d_spend = p["direct_spend"]\n'
                        '        egress = p["egress_gb"]\n'
                        '        weight = egress / total_egress\n'
                        '        shared_cut = shared_total * weight\n'
                        '        total_inv = d_spend + shared_cut\n'
                        '        overhead_pct = (shared_cut / total_inv) * 100\n'
                        '        allocated_shared_sum += shared_cut\n'
                        '\n'
                        '        print(f"{bu:<16} | ${d_spend:<13,.2f} | {weight*100:<9.1f}% | ${shared_cut:<13,.2f} | ${total_inv:<13,.2f} | {overhead_pct:.1f}%")\n'
                        '\n'
                        '    print("-" * 96)\n'
                        '    print(f"Sum of Allocated Shared Costs: ${allocated_shared_sum:,.2f} (Target: ${shared_total:,.2f})")\n'
                        '    diff = abs(shared_total - allocated_shared_sum)\n'
                        '    assert diff < 0.01, f"Allocation leak: Unallocated residue ${diff:.4f}"\n'
                        '    print("\\n>> CHARGEBACK AUDIT SUCCESS: 100% of shared costs allocated with ZERO residue.")\n'
                        '    print("================================================================================")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    run_chargeback()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute the Chargeback Allocation Engine\n'
                        'Run the allocation script and verify that the shared costs sum perfectly to $25,000 with zero mathematical residue:\n\n'
                        '```sh\n'
                        'python3 calculate_chargeback.py\n'
                        '```'
                    )
                ],
                'accept': 'Executable Python shared-cost chargeback engine calculating proportional allocation based on consumption telemetry with 100% reconciliation and zero residue.',
                'verification': 'Review terminal output of <kbd>python3 calculate_chargeback.py</kbd> confirming CHARGEBACK AUDIT SUCCESS.',
                'trouble': 'If allocation sum does not match, inspect floating point weights in `calculate_chargeback.py`.',
                'cleanup': 'Remove test files: <kbd>rm -f raw_billing.json calculate_chargeback.py</kbd>.',
                'file': 'day-119-chargeback-allocation.md'
            }
        },
        # TOPIC 3
        {
            'key': 'topic-03',
            'title': 'Cost visibility',
            'overview': (
                'Enterprise cost visibility demands a continuous, automated telemetry pipeline connecting resource tags, '
                'Cloud Billing BigQuery exports, Looker Studio visualizations, and real-time budget anomaly alerting. '
                'Without consistent labeling, cloud billing appears as an amorphous ledger of unassigned compute, storage, and egress SKUs. '
                'By enforcing a standardized labeling taxonomy through Terraform and Organization Policies, streaming detailed daily usage '
                'and pricing exports into BigQuery, and provisioning multi-tier threshold alerts with automated Pub/Sub anomaly webhooks, '
                'architects detect runaway spending within minutes rather than discovering catastrophic surprises at month-end.'
            ),
            'preview': (
                'A developer launches an unmonitored test cluster with 32x high-memory GPU instances that runs continuously over a holiday weekend, '
                'incurring $18,400 in charges due to the absence of budget anomaly alerts and missing project ownership labels.'
            ),
            'technical': (
                'Building production-grade cloud cost visibility requires configuring four foundational mechanisms.\n\n'
                '### 1. Mandatory Resource Labeling Taxonomy\n'
                'Every deployable resource in Google Cloud should possess a core quartet of immutable labels:\n'
                '- `environment`: Values restricted to `production`, `staging`, `development`, `sandbox`.\n'
                '- `cost_center`: Corporate financial general ledger code (e.g. `cc-4401-fintech`).\n'
                '- `owner`: Team or distribution list responsible for operational maintenance (e.g. `team-core-payments`).\n'
                '- `service`: Logical application identifier matching the service catalog (e.g. `checkout-api`).\n'
                '- **Governance Enforcement**: Enforced via Terraform validation rules, Sentinel policies, or GCP Organization Policies that reject resource creation requests lacking required labels.\n\n'
                '### 2. Cloud Billing BigQuery Export Architecture\n'
                'Google Cloud provides three distinct export tables into BigQuery:\n'
                '1. **Standard Usage Cost Export**: Basic project-level costs, SKUs, and service groupings. Does not include resource-level labels.\n'
                '2. **Detailed Usage Cost Export (Mandatory for FinOps)**: Includes resource-level tags, labels, system labels, VM instance names, and granular GKE pod/namespace usage metrics. Essential for true containerized chargeback.\n'
                '3. **Pricing Export**: Comprehensive real-time SKU list prices, currency conversions, and tiered pricing discounts applicable to the billing account.\n\n'
                '### 3. Looker Studio Visualizations & Key FinOps Queries\n'
                '- **Daily Trend by Cost Center**: Tracks daily burn rate to detect inflection points.\n'
                '- **Gross vs Amortized Cost**: Amortizes upfront or monthly Committed Use Discount (CUD) fees across the instances that actually consumed them, preventing artificial billing spikes on the 1st of each month.\n'
                '- **Idle Resource Detection**: BigQuery queries identifying persistent disks with zero attached instances and IP addresses with zero forwarding rules.\n\n'
                '### 4. Budgets, Alerts, and Anomaly Detection\n'
                '- **Budget Thresholds**: Multi-tier alerts configured at 50%, 75%, 90%, 100% of budgeted spend, plus a 120% forecast alert.\n'
                '- **Programmatic Webhook Containment**: Rather than sending passive emails that are ignored over weekends, Cloud Billing sends notifications to a Cloud Pub/Sub topic that triggers a Cloud Function to automatically revoke developer compute quotas or suspend non-prod sandboxes.'
            ),
            'questions': [
                'Why is the Detailed Usage Cost Export required for containerized GKE cost allocation instead of the Standard Usage Export?',
                'What is the difference between Unblended Cost and Amortized Cost when analyzing Committed Use Discounts?',
                'How does integrating Cloud Billing Pub/Sub budget alerts with Cloud Functions enable automated cost runaway containment?'
            ],
            'reference': 'https://docs.cloud.google.com/architecture/framework/cost-optimization',
            'reference_label': 'Google Cloud Architecture Framework: Billing Export & Cost Visibility',
            'scenario': {
                'symptom': 'Over a 4-day Thanksgiving weekend, an unlabelled staging cluster spins up 16x a2-highgpu-1g instances running runaway PyTorch training scripts, burning $14,200 before being noticed on Monday morning.',
                'impact': '$14,200 unbudgeted spend; staging environment exceeds annual budget by 300%; engineering director called before finance review board.',
                'constraints': 'Must prevent unbudgeted weekend runaways without blocking legitimate production auto-scaling; must automate notification and containment.',
                'evidence': (
                    'Billing Alert Incident Log:\n\n'
                    '```text\n'
                    'Incident ID: COST-ANOMALY-2026-11-28\n'
                    'Project: staging-sandbox-exploratory (Unlabelled)\n'
                    'Resource: a2-highgpu-1g (16 instances x 96 hours = 1,536 GPU-hours)\n'
                    'SKU: Compute Engine A2 GPU running in us-central1\n'
                    'Burn Rate: $148.00 / hour ($3,552 / day)\n'
                    'Alerting Status: Billing alert was sent via email to former employee; no automated action taken.\n'
                    '```'
                ),
                'diagnostic_steps': [
                    'Review Cloud Billing alert configuration; discover that budget alerts were directed to a static email alias that was unmonitored during holidays.',
                    'Check project IAM permissions; observe that staging sandbox had zero quota restrictions on high-tier GPU machine families.',
                    'Query BigQuery billing export to confirm instance runtimes and identify the originating service account identity.',
                    'Implement a programmatic budget alert pipeline: Billing Budget -> Pub/Sub -> Cloud Function -> Automatic instance shutdown for non-prod projects exceeding 120% budget.'
                ],
                'root': 'Relying solely on passive email notifications for budget overruns with zero automated containment webhooks, combined with missing quota limits on non-prod environments.',
                'fix': 'Deploy a Pub/Sub-triggered automated containment Cloud Function that shuts down untagged/non-prod instances when budget exceeds 100%, and enforce mandatory resource labels via Terraform.',
                'verify': 'Simulate a budget overrun event in a test sandbox; verify that Cloud Function executes within 3 minutes and terminates runaway Compute Engine VMs.',
                'residual': 'Automated shutdown scripts must include explicit exemption whitelists for mission-critical production projects to prevent accidental business disruption.',
                'diagram': (
                    'Developer launches 16x GPU instances in unmonitored staging sandbox',
                    'Instances burn $148/hr over 4-day weekend; email sent to unread inbox',
                    'Monday audit discovers $14.2k wasted spend; finance freezes project budgets',
                    'Deploy Billing Pub/Sub budget alert wired to automated shutdown Cloud Function',
                    'Automated containment halts runaway compute within 3 minutes of threshold breach'
                )
            },
            'lab': {
                'name': 'BigQuery Billing Anomaly Detector & Automated Budget Alert Pipeline',
                'file': 'day-119-billing-anomaly-detection.md',
                'goal': 'Implement a Python telemetry parser that queries simulated BigQuery detailed billing export records, identifies SKU-level cost anomalies exceeding a 30% baseline variance, and triggers automated containment payloads.',
                'expected': 'A Python tool parsing billing streams, flagging anomalous GPU/compute spikes, and generating automated webhook mitigation payloads.',
                'mode': 'local Python 3 billing telemetry analysis; zero cloud spend',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Ensure <kbd>~/finops-baseline-lab</kbd> exists.',
                'steps': [
                    (
                        '#### Define Detailed Billing Export & Anomaly Telemetry Dataset\n'
                        'Create a simulated BigQuery detailed billing export JSON file containing baseline usage and an anomalous weekend GPU spike:\n\n'
                        '```sh\n'
                        'cd ~/finops-baseline-lab\n'
                        'cat <<\'EOF\' > bq_detailed_billing.json\n'
                        '[\n'
                        '  {"date": "2026-11-24", "project_id": "prod-checkout",   "sku": "N2-Standard-4", "cost": 420.0, "labels": {"env": "prod", "cc": "cc-101"}},\n'
                        '  {"date": "2026-11-25", "project_id": "prod-checkout",   "sku": "N2-Standard-4", "cost": 435.0, "labels": {"env": "prod", "cc": "cc-101"}},\n'
                        '  {"date": "2026-11-26", "project_id": "staging-sandbox", "sku": "A2-GPU-High",  "cost": 85.0,  "labels": {"env": "staging"}},\n'
                        '  {"date": "2026-11-27", "project_id": "staging-sandbox", "sku": "A2-GPU-High",  "cost": 3550.0, "labels": {"env": "staging"}},\n'
                        '  {"date": "2026-11-28", "project_id": "staging-sandbox", "sku": "A2-GPU-High",  "cost": 3600.0, "labels": {"env": "staging"}}\n'
                        ']\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Anomaly Detection and Containment Engine\n'
                        'Author a Python script that calculates moving averages, detects anomalous SKU cost spikes (>30% variance), and formats an automated Pub/Sub containment webhook:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > detect_billing_anomalies.py\n'
                        'import json\n'
                        'from datetime import datetime, timezone\n'
                        '\n'
                        'def analyze_billing_stream():\n'
                        '    print("================================================================================")\n'
                        '    print("DAY 119: BIGQUERY DETAILED BILLING ANOMALY DETECTOR & WEBHOOK ENGINE")\n'
                        '    print("================================================================================\\n")\n'
                        '\n'
                        '    with open("bq_detailed_billing.json", "r") as f:\n'
                        '        records = json.load(f)\n'
                        '\n'
                        '    sku_history = {}\n'
                        '    anomalies = []\n'
                        '\n'
                        '    print(f"{\'Date\':<12} | {\'Project ID\':<18} | {\'SKU\':<16} | {\'Cost\':<10} | {\'Status\'}")\n'
                        '    print("-" * 75)\n'
                        '\n'
                        '    for rec in records:\n'
                        '        dt = rec["date"]\n'
                        '        proj = rec["project_id"]\n'
                        '        sku = rec["sku"]\n'
                        '        cost = rec["cost"]\n'
                        '        key = (proj, sku)\n'
                        '\n'
                        '        status = "NORMAL"\n'
                        '        if key in sku_history:\n'
                        '            baseline = sku_history[key]\n'
                        '            variance_pct = ((cost - baseline) / baseline) * 100\n'
                        '            if variance_pct > 30.0 and cost > 500.0:\n'
                        '                status = f"ANOMALY (+{variance_pct:.0f}%)"\n'
                        '                anomalies.append({\n'
                        '                    "date": dt,\n'
                        '                    "project": proj,\n'
                        '                    "sku": sku,\n'
                        '                    "cost": cost,\n'
                        '                    "baseline": baseline,\n'
                        '                    "variance_pct": variance_pct\n'
                        '                })\n'
                        '        sku_history[key] = cost\n'
                        '        print(f"{dt:<12} | {proj:<18} | {sku:<16} | ${cost:<9.2f} | {status}")\n'
                        '\n'
                        '    print("-" * 75)\n'
                        '    print(f"Total Anomalies Detected: {len(anomalies)}\\n")\n'
                        '\n'
                        '    assert len(anomalies) >= 1, "Failed to detect expected GPU runaway spike!"\n'
                        '\n'
                        '    # Format automated containment webhook payload\n'
                        '    first_anomaly = anomalies[0]\n'
                        '    containment_payload = {\n'
                        '        "alert_type": "COST_ANOMALY_RUNAWAY",\n'
                        '        "triggered_at": datetime.now(timezone.utc).isoformat(),\n'
                        '        "target_project": first_anomaly["project"],\n'
                        '        "culprit_sku": first_anomaly["sku"],\n'
                        '        "measured_cost": first_anomaly["cost"],\n'
                        '        "baseline_cost": first_anomaly["baseline"],\n'
                        '        "action": "ENFORCE_PROJECT_VM_STOP_AND_QUOTA_FREEZE"\n'
                        '    }\n'
                        '\n'
                        '    print("Dispatching Automated Containment Payload to Cloud Pub/Sub:")\n'
                        '    print(json.dumps(containment_payload, indent=2))\n'
                        '    print("\\n>> BILLING ANOMALY VERDICT: PASSED (Runaway intercepted and containment dispatched).")\n'
                        '    print("================================================================================")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    analyze_billing_stream()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute the Anomaly Detection Script\n'
                        'Run the anomaly detection tool to intercept the runaway GPU spike and verify containment payload dispatch:\n\n'
                        '```sh\n'
                        'python3 detect_billing_anomalies.py\n'
                        '```'
                    )
                ],
                'accept': 'Executable Python BigQuery billing anomaly parser detecting >30% SKU cost spikes and generating automated containment payloads.',
                'verification': 'Review terminal output of <kbd>python3 detect_billing_anomalies.py</kbd> confirming BILLING ANOMALY VERDICT: PASSED.',
                'trouble': 'If anomaly is not flagged, verify the cost threshold in `detect_billing_anomalies.py`.',
                'cleanup': 'Remove test files: <kbd>rm -f bq_detailed_billing.json detect_billing_anomalies.py</kbd>.',
                'file': 'day-119-billing-anomaly-detection.md'
            }
        },
        # TOPIC 4
        {
            'key': 'topic-04',
            'title': 'Compute savings',
            'overview': (
                'Compute optimization represents the single largest immediate cost-reduction opportunity in Google Cloud. '
                'Architects leverage five distinct mechanisms: Active Assist Rightsizing Recommendations, automated non-production '
                'instance scheduling, Spot Virtual Machines for fault-tolerant workloads, Sustained Use Discounts (SUDs), and Committed Use '
                'Discounts (CUDs). Achieving optimal compute economics requires layering these mechanisms strategically rather than '
                'viewing them as mutually exclusive choices. A robust architecture covers predictable core baseline infrastructure '
                'with high-discount resource-based or flexible spend-based CUDs, leverages Spot VMs for elastic batch processing, and '
                'runs variable seasonal peaks on On-Demand compute.'
            ),
            'preview': (
                'An enterprise attempts to achieve maximum savings by committing 100% of peak compute to 3-year resource-based CUDs, '
                'only to suffer massive financial loss when post-holiday traffic declines by 40%, leaving commitments severely under-utilized.'
            ),
            'technical': (
                'Designing an enterprise compute savings model mandates quantifying the mathematical trade-offs between commitment discount and utilization risk.\n\n'
                '### 1. Compute Savings Levers Breakdown\n'
                '- **Active Assist Rightsizing Recommendations**:\n'
                '  - Monitors vCPU and memory utilization over an 8-day rolling window.\n'
                '  - Identifies instances running below 15% average CPU and provides non-disruptive custom machine type recommendations (e.g. converting `n2-standard-8` to `n2-custom-4-16384`), saving 30–50% without altering operational stability.\n'
                '- **Non-Production Instance Scheduling**:\n'
                '  - Development and staging environments active only during standard business hours (50 hours/week out of 168 hours total).\n'
                '  - Shutting down non-production instances overnight and on weekends captures an immediate **70.2% cost reduction** on non-prod compute.\n'
                '- **Spot Virtual Machines (Preemptible Compute)**:\n'
                '  - 60% to 91% discount off standard on-demand pricing.\n'
                '  - Compute Engine can reclaim Spot instances at any time with a 30-second ACPI/metadata preemption notice.\n'
                '  - Ideal for stateless GKE node pools, asynchronous Pub/Sub consumers, video transcoding, and ML hyperparameter tuning.\n'
                '- **Sustained Use Discounts (SUDs)**:\n'
                '  - Automatic discount (up to 30%) applied to Compute Engine N1, N2, and N2D VMs running more than 25% of a billing month.\n'
                '  - Requires zero upfront commitment and zero contract term; however, SUDs do not apply to newer C3, C3D, or N4 machine families.\n\n'
                '### 2. Committed Use Discounts (CUDs): Resource-Based vs Spend-Based\n'
                '- **Resource-Based CUDs**:\n'
                '  - Commit to a specific amount of vCPU and RAM in a specific machine family within a single specific region.\n'
                '  - Offers the highest discount: up to 55% for 1-year and up to 70% for 3-year commitments on memory-optimized machines.\n'
                '  - **Risk**: Rigid. If you migrate from `n2` in `us-central1` to `c3` in `us-east4`, the discount does not transfer.\n'
                '- **Spend-Based / Flexible CUDs**:\n'
                '  - Commit to a fixed dollar-per-hour spend across all Compute Engine machine families, regions, GKE Autopilot, and Cloud Run.\n'
                '  - Discount: 28% for 1-year, 46% for 3-year commitments.\n'
                '  - **Advantage**: Ultimate architectural flexibility during cloud modernization waves.\n\n'
                '### 3. Layered Commitment Architecture & Utilization Uncertainty\n'
                'To minimize commitment risk while maximizing savings, architects deploy the **60/20/20 Layering Rule**:\n'
                '1. **Base Tier (0–60% of Minimum Historical Load)**: Covered by 3-Year Resource-Based CUDs (or Flexible CUDs) for maximum rate reduction (55–70% discount).\n'
                '2. **Intermediate Tier (60–80% of Average Load)**: Covered by 1-Year Flexible Spend CUDs (28–46% discount), hedging against architectural changes.\n'
                '3. **Elastic / Fault-Tolerant Tier**: Covered by Spot VMs (60–91% discount).\n'
                '4. **Peak Variable Surge Tier (80–100%+)**: Left on On-Demand with automatic SUDs, absorbing seasonal demand swings with zero financial lock-in.'
            ),
            'questions': [
                'Why should an organization never purchase CUDs to cover 100% of peak compute traffic?',
                'How does the 30-second Spot VM preemption notice require application architectures to be designed for graceful termination?',
                'Under what architectural conditions is a Flexible Spend CUD superior to a Resource-Based CUD despite the lower discount percentage?'
            ],
            'reference': 'https://docs.cloud.google.com/architecture/framework/cost-optimization',
            'reference_label': 'Google Cloud Architecture Framework: Compute Cost Optimization & CUD Strategies',
            'scenario': {
                'symptom': 'An online retail company committed to 3-year Resource-Based CUDs covering 100% of Black Friday peak compute (1,200 N2 vCPUs). Post-holiday traffic fell to 400 vCPUs, resulting in 800 vCPUs ($18,500/month) of wasted unutilized commitment for the next 34 months.',
                'impact': '$629,000 in stranded, unutilized CUD commitment waste across the 3-year contract term.',
                'constraints': 'Must establish an empirical cost model that evaluates commitment risk under utilization uncertainty and models fixed vs variable costs.',
                'evidence': (
                    'CUD Utilization Financial Post-Mortem:\n\n'
                    '```text\n'
                    'Commitment ID: cud-res-n2-uscentral1-peak-2025\n'
                    'Purchased: 1,200 vCPUs @ 3-Year Resource CUD ($0.0152/vCPU-hr = $13,320/mo commitment fee)\n'
                    'Post-Holiday Measured Usage: 420 vCPUs average\n'
                    'Committed Spend:   $13,320 / month\n'
                    'Actual Value Used: $4,662 / month\n'
                    'Net Monthly Waste: $8,658 / month (Commitment Utilization: 35.0%)\n'
                    'Finding: Purchasing CUDs to peak capacity creates severe stranded financial liability.\n'
                    '```'
                ),
                'diagnostic_steps': [
                    'Extract 12-month hourly vCPU utilization percentiles (p50, p75, p90, p99) from Cloud Monitoring.',
                    'Calculate the commitment break-even point: For a 55% discount, CUD break-even occurs when utilization exceeds 45%.',
                    'Model historical minimum baseline (p10 = 400 vCPUs) versus peak surge (p99 = 1,200 vCPUs).',
                    'Construct a tiered commitment model: Commit to 400 vCPUs via 3-yr CUD, 250 vCPUs via 1-yr Flexible CUD, and handle remaining 550 vCPUs via Spot VMs and On-Demand.'
                ],
                'root': 'Sizing long-term contractual commitments to peak traffic spikes rather than stable historical baseline consumption.',
                'fix': 'Author an automated Python cost modeling tool that calculates fixed vs variable costs, models utilization uncertainty, and optimizes commitment levels to achieve minimum total cost of ownership without stranded waste.',
                'verify': 'Run the cost baseline model; verify that total monthly spend decreases from $42,500 to $21,300 with 98% commitment utilization.',
                'residual': 'Relying on Spot VMs for elastic scaling requires ensuring all worker services handle SIGTERM termination within 30 seconds.',
                'diagram': (
                    'Retailer purchases 3-year CUDs covering 100% of peak Black Friday traffic',
                    'January traffic plunges 65%; 800 committed vCPUs sit completely idle',
                    'Finance flags $8.6k/mo in wasted commitment fees over 34 remaining months',
                    'Implement 60/20/20 Layered Commitment Model: Base CUD + Flexible + Spot + On-Demand',
                    'TCO reduced by 49.8% with zero stranded commitments and 98% CUD utilization'
                )
            },
            'lab': {
                'name': 'Dated Cost Baseline and Commitment Risk Modeling Engine',
                'file': 'day-119-cost-model.md',
                'goal': 'Build an executable Python cost modeling engine that computes monthly baseline spend across On-Demand, Rightsized, Spot VM, and CUD commitment scenarios, models utilization uncertainty, and outputs the dated cost baseline model artifact.',
                'expected': 'A Python tool generating a dated financial comparison table, calculating commitment risk under variable utilization, and exporting day-119-cost-model.md.',
                'mode': 'local Python 3 financial modeling; zero cloud spend',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Ensure <kbd>~/finops-baseline-lab</kbd> exists.',
                'steps': [
                    (
                        '#### Define Workload Compute Usage and Pricing Parameters\n'
                        'Write a JSON specification defining hourly compute consumption across tiers, machine pricing, and discount percentages:\n\n'
                        '```sh\n'
                        'cd ~/finops-baseline-lab\n'
                        'cat <<\'EOF\' > workload_cost_spec.json\n'
                        '{\n'
                        '  "workload": "Omnichannel Retail Core Services",\n'
                        '  "hours_per_month": 730,\n'
                        '  "baseline_vcpus": 400,\n'
                        '  "average_vcpus": 650,\n'
                        '  "peak_vcpus": 1200,\n'
                        '  "rates": {\n'
                        '    "ondemand_hourly_per_vcpu": 0.0338,\n'
                        '    "spot_hourly_per_vcpu": 0.0071,\n'
                        '    "res_cud_3yr_discount": 0.55,\n'
                        '    "flex_cud_1yr_discount": 0.28,\n'
                        '    "rightsizing_savings_pct": 0.22,\n'
                        '    "nonprod_scheduling_savings_pct": 0.70\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Dated Cost Baseline and Commitment Risk Modeling Tool\n'
                        'Author a Python script that computes total cost for four architecture strategies, evaluates commitment risk under a 30% drop in utilization, and exports the formal markdown model:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > generate_cost_model.py\n'
                        'import json\n'
                        'from datetime import datetime, timezone\n'
                        '\n'
                        'def build_cost_model():\n'
                        '    print("================================================================================")\n'
                        '    print("DAY 119: DATED COST BASELINE AND COMMITMENT RISK MODELING ENGINE")\n'
                        '    print("================================================================================\\n")\n'
                        '\n'
                        '    with open("workload_cost_spec.json", "r") as f:\n'
                        '        spec = json.load(f)\n'
                        '\n'
                        '    h = spec["hours_per_month"]\n'
                        '    base_v = spec["baseline_vcpus"]\n'
                        '    avg_v = spec["average_vcpus"]\n'
                        '    peak_v = spec["peak_vcpus"]\n'
                        '    rates = spec["rates"]\n'
                        '    od_rate = rates["ondemand_hourly_per_vcpu"]\n'
                        '    spot_rate = rates["spot_hourly_per_vcpu"]\n'
                        '\n'
                        '    # Strategy 1: Un-optimized On-Demand (Average 650 vCPUs)\n'
                        '    cost_ondemand = avg_v * od_rate * h\n'
                        '\n'
                        '    # Strategy 2: Rightsized On-Demand (22% reduction on avg vCPUs)\n'
                        '    rightsized_v = avg_v * (1.0 - rates["rightsizing_savings_pct"])\n'
                        '    cost_rightsized = rightsized_v * od_rate * h\n'
                        '\n'
                        '    # Strategy 3: Naive 100% Peak CUD (Committing to 1200 vCPUs for 3 years)\n'
                        '    cud_rate_3yr = od_rate * (1.0 - rates["res_cud_3yr_discount"])\n'
                        '    cost_naive_peak_cud = peak_v * cud_rate_3yr * h\n'
                        '\n'
                        '    # Strategy 4: Layered FinOps Model (400 vCPUs 3-yr CUD + 150 vCPUs Spot + 100 vCPUs On-Demand)\n'
                        '    cost_layered = (\n'
                        '        (base_v * cud_rate_3yr * h) +\n'
                        '        (150 * spot_rate * h) +\n'
                        '        (100 * od_rate * h)\n'
                        '    )\n'
                        '\n'
                        '    print(f"{\'Architecture Strategy\':<36} | {\'Monthly Cost\':<14} | {\'Savings vs On-Demand\':<22} | {\'Commitment Risk\'}")\n'
                        '    print("-" * 96)\n'
                        '    print(f"{\'1. Un-optimized On-Demand\':<36} | ${cost_ondemand:<13,.2f} | Baseline (0.0%)        | Zero risk (Flexible)")\n'
                        '    print(f"{\'2. Rightsized Compute Engine\':<36} | ${cost_rightsized:<13,.2f} | -{((cost_ondemand - cost_rightsized)/cost_ondemand)*100:.1f}%                | Zero risk (Usage opt)")\n'
                        '    print(f"{\'3. Naive 100% Peak 3-Yr CUD\':<36} | ${cost_naive_peak_cud:<13,.2f} | -{((cost_ondemand - cost_naive_peak_cud)/cost_ondemand)*100:.1f}%                | EXTREME (Locked to peak)")\n'
                        '    print(f"{\'4. Layered FinOps (CUD+Spot+OD)\':<36} | ${cost_layered:<13,.2f} | -{((cost_ondemand - cost_layered)/cost_ondemand)*100:.1f}%                | MINIMAL (Hedged baseline)")\n'
                        '    print("-" * 96)\n'
                        '\n'
                        '    # Model Commitment Risk under 30% Traffic Downturn\n'
                        '    print("\\nSimulating 30% Traffic Downturn (Workload drops to 455 vCPUs):")\n'
                        '    # Naive peak CUD still pays for 1200 vCPUs!\n'
                        '    # Layered model utilizes 100% of 400 base CUD, reduces Spot/OD to 55 vCPUs\n'
                        '    cost_layered_downturn = (base_v * cud_rate_3yr * h) + (55 * spot_rate * h)\n'
                        '    print(f"  - Naive Peak CUD Monthly Bill: ${cost_naive_peak_cud:,.2f} (Waste: ${(cost_naive_peak_cud - (455*od_rate*h)):,.2f})")\n'
                        '    print(f"  - Layered FinOps Monthly Bill: ${cost_layered_downturn:,.2f} (Flexible scaling with 0 stranded waste)\\n")\n'
                        '\n'
                        '    # Export formal markdown model\n'
                        '    dated_str = datetime.now(timezone.utc).strftime(\'%Y-%m-%d %H:%M:%SZ\')\n'
                        '    md_content = "# Enterprise Compute Cost Model & Commitment Risk Baseline\\n\\n"\n'
                        '    md_content += f"Date: {dated_str}\\n"\n'
                        '    md_content += f"Workload: {spec[\'workload\']}\\n"\n'
                        '    md_content += "Billing Scope: Days 119–133 Performance & Delivery Baseline\\n\\n"\n'
                        '    md_content += "## 1. Strategy Comparison Matrix\\n\\n"\n'
                        '    md_content += "| Architecture Strategy | Monthly Cost | Monthly Savings | Commitment Risk Profile |\\n"\n'
                        '    md_content += "|---|---|---|---|\\n"\n'
                        '    md_content += f"| Un-optimized On-Demand | ${cost_ondemand:,.2f} | $0.00 (0.0%) | None (Variable On-Demand) |\\n"\n'
                        '    md_content += f"| Rightsized Compute Engine | ${cost_rightsized:,.2f} | ${cost_ondemand - cost_rightsized:,.2f} (22.0%) | None (Usage Reduction) |\\n"\n'
                        '    md_content += f"| Naive 100% Peak 3-Yr CUD | ${cost_naive_peak_cud:,.2f} | ${cost_ondemand - cost_naive_peak_cud:,.2f} (16.9%) | High Risk ($13.3k/mo fixed lock) |\\n"\n'
                        '    md_content += f"| **Layered FinOps Model** | **${cost_layered:,.2f}** | **${cost_ondemand - cost_layered:,.2f} (64.5%)** | **Optimized (Hedged 60/20/20)** |\\n\\n"\n'
                        '    md_content += "## 2. Utilization Uncertainty & Risk Hedge Analysis\\n\\n"\n'
                        '    md_content += "- **Base Commitment**: 400 vCPUs covered by 3-Year Resource CUD ($0.0152/hr).\\n"\n'
                        '    md_content += "- **Spot Elasticity**: 150 vCPUs covered by Spot VMs ($0.0071/hr) with 30s preemption hooks.\\n"\n'
                        '    md_content += "- **Peak Variable Buffer**: 100 vCPUs covered by On-Demand with automatic SUD tiering.\\n"\n'
                        '    md_content += f"- **Downturn Resilience**: Under a 30% traffic contraction, the Layered Model bill contracts to ${cost_layered_downturn:,.2f} with zero unutilized CUD penalty.\\n"\n'
                        '\n'
                        '    with open("day-119-cost-model.md", "w") as out:\n'
                        '        out.write(md_content)\n'
                        '    print("Wrote dated cost model to day-119-cost-model.md.")\n'
                        '    assert cost_layered < cost_ondemand * 0.45, "Layered FinOps must achieve >55% savings!"\n'
                        '    print("================================================================================")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    build_cost_model()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute the Cost Model Generator and Inspect Output\n'
                        'Run the generator script and verify that the layered FinOps model achieves over 64% savings with hedged commitment risk:\n\n'
                        '```sh\n'
                        'python3 generate_cost_model.py\n'
                        'cat day-119-cost-model.md\n'
                        '```'
                    )
                ],
                'accept': 'Executable Python compute cost baseline tool comparing On-Demand, Rightsizing, Spot VMs, and CUDs under utilization uncertainty and exporting day-119-cost-model.md.',
                'verification': 'Review terminal output of <kbd>python3 generate_cost_model.py</kbd> confirming Wrote dated cost model to day-119-cost-model.md.',
                'trouble': 'If cost assertion triggers, verify the rate constants in `workload_cost_spec.json`.',
                'cleanup': 'Remove test files: <kbd>rm -f workload_cost_spec.json generate_cost_model.py</kbd>.',
                'file': 'day-119-cost-model.md'
            }
        }
    ]
}
