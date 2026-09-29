"""Day 121 data specification: runtime, analytics and carbon cost drivers."""

DATA = {
    'day': 121,
    'part1_intro': (
        'Day 121 turns the Day 119–120 cost baseline into a workload-driver model. '
        'Start with workload shape and the unit being served: requests, Pod-hours, scanned TiB, slot-hours, '
        'or a completed batch. Trace each unit through the service control that changes capacity, then state '
        'the signal that would show whether the control worked. This makes a quiet-period scale-down, a '
        'node-packing adjustment, a partition predicate and a regional carbon comparison answerable with '
        'evidence rather than with product averages. Use the supplied figures as synthetic practice inputs; '
        'validate all prices, workload distributions, service coverage and carbon-report boundaries against '
        'the actual workload and current documentation.'
    ),
    'exit_summary': (
        'A cost-driver worksheet comparing serverless runtime, packed and autoscaled GKE capacity, '
        'BigQuery scan and capacity models, plus stated Carbon Footprint scope and placement assumptions. '
        'Record explicit low/base/high quantities and mark every price as an assumption to validate in the later BigQuery lab.'
    ),
    'part2_intro': (
        'Follow each workload from demand to billable quantity, then identify the control and its limit. '
        'The path diagram is a conceptual worksheet, not a deployed topology or a price quote.'
    ),
    'arch_table_html': '''<div class="table-container"><table><thead><tr><th>Path and owner</th><th>Quantity that moves cost</th><th>Control point</th><th>Observable evidence</th><th>Limit or trade-off</th></tr></thead><tbody>
<tr><td>Cloud Run request serving<br>Owner: service team</td><td>Request volume and duration; instance CPU/memory time; minimum instances; concurrency; request-based or instance-based billing mode</td><td>Scale to zero for idle request workloads; set minimum capacity only for a measured latency/background-work need; tune safe concurrency; cap service instances against downstream connection capacity</td><td>Correlate request count, active/idle instance count, configured minimum/maximum, concurrency, latency percentiles, errors and database connections over matching windows</td><td>Zero minimum can expose cold-start latency; warm instances cost through quiet intervals. A cap can queue requests or surface 429s, and a per-revision cap is not necessarily a whole-service total during traffic splits or rollouts.</td></tr>
<tr><td>GKE Standard scheduling<br>Owner: platform and workload teams</td><td>Pod CPU/memory requests, node type and count-hours, system overhead, workload baseline and unused allocatable capacity</td><td>Set requests from representative use; pack compatible Pods; use HPA for replicas and Cluster Autoscaler for nodes; choose pool shapes and minimums; protect critical Pods with disruption controls</td><td>Compare allocatable, requested and used CPU/memory; packing/fragmentation; pending Pods; node hours; autoscaler events; PDB and affinity blockers</td><td>Small requests can overpack and increase throttling, OOM or latency; large requests strand capacity. Autoscaling follows scheduling feasibility and constraints, not a promise that every temporarily idle node disappears immediately.</td></tr>
<tr><td>BigQuery on-demand analysis<br>Owner: data team</td><td>Bytes processed per query × executions over the period; columns read; partition/block pruning</td><td>Estimate with dry run; use a partition filter and select required columns; apply maximum bytes billed where appropriate; compare equivalent output</td><td>Record estimated bytes, actual bytes processed, query plan, slot time, result rows and repeated-run count. Price formula: processed TiB × dated assumed unit rate.</td><td>LIMIT restricts returned rows, not necessarily scanned bytes. Dry-run estimate is not the complete project bill; storage, streaming, network and other work are separate.</td></tr>
<tr><td>BigQuery capacity pricing<br>Owner: data platform and finance</td><td>Provisioned or autoscaled slot capacity over time; utilization and queued concurrency</td><td>Model slot-hours for a representative workload and compare with on-demand bytes pricing; inspect reservation assignments and autoscaling behavior</td><td>Record slot-hours, utilization, idle share, queued jobs, slot time, workload mix and same-period on-demand estimate</td><td>Predictable capacity can reduce price variance but has idle-capacity risk; more slots do not guarantee faster work. Capacity and scan efficiency remain separate levers.</td></tr>
<tr><td>Carbon Footprint report<br>Owner: sustainability and FinOps</td><td>Allocated emissions for covered product use, aggregated by project, product, region and month under the selected method</td><td>State metric (location-based or market-based), reporting month, projects, product coverage and allocation scope before making a claim</td><td>Retain report filters, published methodology version/context, region breakdown, coverage gaps and change over a comparable period</td><td>Customer-specific report data is not third-party assured. Scope excludes some activities and does not automatically equal a complete customer lifecycle inventory.</td></tr>
<tr><td>Feasible regional placement<br>Owner: architecture, data governance and service owner</td><td>Work completed, utilization, transfer path, recovery replication and report values for the same period</td><td>Apply residency and availability gates first; compare regions that meet constraints using equivalent output, deadline and workload assumptions</td><td>Document supported service/region, data location approval, latency, RTO/RPO, transfer volume, completion time and comparable report boundary</td><td>A lower regional estimate alone does not prove lower total workload emissions. Transfer, redundancy, low utilization or an infeasible residency choice can reverse or invalidate the decision.</td></tr>
</tbody></table></div>''',
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 121 workload quantities and cost control points',
        'desc': 'Conceptual paths map request demand to serverless instances, Kubernetes Pods and nodes, BigQuery scan or slots, and carbon reporting with a verification boundary around measured quantities and assumptions.',
        'caption': 'Conceptual cost-driver map for Day 121. It shows where measurements and controls belong; it does not prove prices, query execution, cluster utilization, or emissions for a real project.',
        'width': 1120, 'height': 690,
        'layers': [
            {'name': 'DEMAND AND INPUTS', 'x': 20, 'y': 55, 'w': 1080, 'h': 92, 'fill': '#1e3a5f', 'title_color': '#7dd3fc', 'desc': 'requests · Pods · SQL · location'},
            {'name': 'RUNTIME AND ANALYTICS', 'x': 20, 'y': 185, 'w': 1080, 'h': 210, 'fill': '#064e3b', 'title_color': '#6ee7b7', 'desc': 'metering depends on service model'},
            {'name': 'MEASUREMENT AND DECISION', 'x': 20, 'y': 435, 'w': 1080, 'h': 115, 'fill': '#422006', 'title_color': '#fdba74', 'desc': 'compare normalized quantities and constraints'},
        ],
        'components': [
            {'x': 55, 'y': 88, 'w': 180, 'h': 45, 'name': 'Demand profile', 'detail': 'rate · burst · idle', 'stroke': '#38bdf8'},
            {'x': 320, 'y': 88, 'w': 180, 'h': 45, 'name': 'Workload shape', 'detail': 'state · CPU · latency', 'stroke': '#38bdf8'},
            {'x': 585, 'y': 88, 'w': 205, 'h': 45, 'name': 'Data and query', 'detail': 'bytes · partitions · slots', 'stroke': '#38bdf8'},
            {'x': 855, 'y': 88, 'w': 205, 'h': 45, 'name': 'Region and period', 'detail': 'eligibility · residency', 'stroke': '#38bdf8'},
            {'x': 55, 'y': 220, 'w': 215, 'h': 65, 'name': 'Cloud Run', 'detail': 'instances · concurrency', 'stroke': '#22c55e'},
            {'x': 330, 'y': 220, 'w': 215, 'h': 65, 'name': 'GKE Pods', 'detail': 'requests · packing', 'stroke': '#22c55e'},
            {'x': 610, 'y': 220, 'w': 205, 'h': 65, 'name': 'GKE nodes', 'detail': 'autoscale · idle headroom', 'stroke': '#22c55e'},
            {'x': 860, 'y': 220, 'w': 200, 'h': 65, 'name': 'BigQuery', 'detail': 'scan bytes or slots', 'stroke': '#22c55e'},
            {'x': 170, 'y': 320, 'w': 250, 'h': 52, 'name': 'Carbon Footprint', 'detail': 'reported estimate by scope', 'stroke': '#f59e0b'},
            {'x': 590, 'y': 320, 'w': 290, 'h': 52, 'name': 'Billing and runtime evidence', 'detail': 'labels · metrics · query estimates', 'stroke': '#f59e0b'},
            {'x': 220, 'y': 468, 'w': 280, 'h': 58, 'name': 'Comparable cost model', 'detail': 'low / base / high quantities', 'stroke': '#fdba74'},
            {'x': 620, 'y': 468, 'w': 280, 'h': 58, 'name': 'Decision with guardrails', 'detail': 'SLO · limits · uncertainty', 'stroke': '#fdba74'},
        ],
        'flows': [
            {'x1': 235, 'y1': 110, 'x2': 320, 'y2': 110, 'label': 'profile', 'type': 'ok'},
            {'x1': 500, 'y1': 110, 'x2': 585, 'y2': 110, 'label': 'shape', 'type': 'ok'},
            {'x1': 790, 'y1': 110, 'x2': 855, 'y2': 110, 'label': 'scope', 'type': 'ok'},
            {'x1': 145, 'y1': 133, 'x2': 145, 'y2': 220, 'label': 'request demand', 'type': 'ok'},
            {'x1': 415, 'y1': 133, 'x2': 415, 'y2': 220, 'label': 'pod needs', 'type': 'ok'},
            {'x1': 710, 'y1': 133, 'x2': 710, 'y2': 220, 'label': 'query workload', 'type': 'ok'},
            {'x1': 960, 'y1': 133, 'x2': 960, 'y2': 220, 'label': 'location', 'type': 'warn'},
            {'x1': 270, 'y1': 252, 'x2': 330, 'y2': 252, 'label': 'scales', 'type': 'ok'},
            {'x1': 545, 'y1': 252, 'x2': 610, 'y2': 252, 'label': 'schedules', 'type': 'ok'},
            {'x1': 415, 'y1': 285, 'x2': 295, 'y2': 320, 'label': 'eligible usage', 'type': 'warn'},
            {'x1': 710, 'y1': 285, 'x2': 735, 'y2': 320, 'label': 'telemetry', 'type': 'ok'},
            {'x1': 420, 'y1': 346, 'x2': 590, 'y2': 346, 'label': 'compare evidence', 'type': 'ok'},
            {'x1': 735, 'y1': 372, 'x2': 735, 'y2': 468, 'label': 'validated inputs', 'type': 'ok'},
            {'x1': 500, 'y1': 497, 'x2': 620, 'y2': 497, 'label': 'review trade-offs', 'type': 'ok'},
        ],
        'boundaries': [{'x': 35, 'y': 425, 'w': 1045, 'h': 135, 'label': 'ESTIMATES ONLY · VALIDATE PRICES, SCOPE AND WORKLOAD'}],
        'probes': [
            {'cx': 258, 'cy': 233, 'label': 'P1: Compare idle hours, concurrency, latency and maximum instances', 'color': '#38bdf8'},
            {'cx': 858, 'cy': 263, 'label': 'P2: Record dry-run bytes, partitions and pricing assumption', 'color': '#22c55e'},
            {'cx': 1040, 'cy': 133, 'label': 'P3: Confirm reporting scope, period and location eligibility', 'color': '#f59e0b'},
        ],
    },
    'part3_intro': (
        'These are synthetic Brightloaf planning cases, not observed production incidents. Supplied quantities are scenario facts; '
        'the causal explanation is an architectural inference to test with billing, runtime, query and reporting evidence.'
    ),
    'part4_intro': (
        'Complete both exercises offline with the Day 119 cost baseline and Day 120 storage/network/database proposal available. '
        'No Google Cloud project or chargeable resource is needed. Keep estimates separate from measured results.'
    ),
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Runtime utilization, query scans and capacity cost drivers',
            'overview': (
                'This topic joins three cost paths that share one discipline: model billable demand from workload evidence. '
                'For Cloud Run, request volume, active instance time, minimum instances and concurrency interact; scale to zero can '
                'reduce idle serving time while cold starts or a required warm floor can increase latency or cost. In GKE, Pod requests '
                'and schedulability influence packing and node count; HPA changes Pod replicas while Cluster Autoscaler changes node '
                'capacity, subject to disruption budgets and scale-down constraints. BigQuery introduces bytes processed for on-demand '
                'queries and slot capacity for capacity pricing. Partition filters can reduce scanned bytes, while LIMIT alone does not '
                'guarantee fewer bytes. These distinctions prepare the later BigQuery lab without treating today’s example prices as current quotes.'
            ),
            'preview': (
                'A synthetic Brightloaf workload shows a low average CPU graph but a long idle tail, bursty requests, and a query estimate that scans 2.4 TiB before partition pruning.'
                ' The team may choose the wrong runtime or commit to capacity, creating avoidable spend or latency and queueing during peaks.'
            ),
            'technical': (
                '#### Cloud Run: demand, concurrency and retained capacity\n'
                'Cloud Run scales service instances against request concurrency and CPU signals, within configured minimum and maximum '
                'bounds. With a zero minimum, idle request-serving capacity can scale down; the next request can pay a cold-start latency '
                'cost. A nonzero minimum holds warm capacity and can keep the service responsive, but it retains a billable floor even when '
                'demand is quiet. A background worker is a different shape from an HTTP request service: if work must continue with no '
                'incoming request, the design needs an explicit always-on or wake-up mechanism and an appropriate billing mode. Do not infer '
                'worker utilization from request count alone.\n\n'
                'Concurrency is a packing control, not a free discount. Raising the maximum requests per instance can serve more requests '
                'with fewer instances, but simultaneous work competes for CPU, memory, locks and downstream connections. Lower concurrency '
                'can reduce per-request contention and latency while increasing instance count and instance-time. Tune it with a repeatable '
                'load profile that includes request mix, payload size, think time and steady-state plus burst phases. Track p50/p95/p99 '
                'latency, errors, throttling, instance count, active/idle time and connection pool saturation. The service-level maximum '
                'can shield a database from a connection surge; when the cap is reached, queued work or request failures are the cost of '
                'that protection. Maximums may be scoped per revision, so rollout and traffic split behavior belongs in the model.\n\n'
                'For an approximate request-based comparison, record the number of active instance-seconds and the CPU/memory shape during '
                'the measurement period; keep request charges and free-tier assumptions as separate line items to validate. For instance-based '
                'billing, instance lifetime is the relevant time boundary, including permitted background processing. Do not price a service '
                'from a single utilization snapshot: align the measured interval with request volume, latency and scale events.\n\n'
                '#### GKE Standard: Pod packing and node autoscaling\n'
                'The scheduler places Pods using their resource requests, not the application’s measured average use. Requests therefore '
                'control how many Pods fit on a node and which nodes must remain. Oversized requests create fragmentation: total cluster '
                'capacity can appear available while a Pod cannot fit the remaining shape on any individual node. Undersized requests can '
                'pack tightly but lead to CPU contention, memory pressure, eviction or latency regressions. Compare requested resources with '
                'allocatable resources, then compare both with measured use over a representative peak and trough. Keep daemon/system Pod '
                'overhead, pool shape, taints, affinity and zonal spread visible in the worksheet.\n\n'
                'The controls own different decisions. Horizontal Pod Autoscaler changes desired Pod replicas using resource or custom '
                'metrics. Cluster Autoscaler in Standard node pools reacts to Pods that cannot schedule and simulation of whether nodes can '
                'be removed; it changes node capacity, not the application’s replica target. A PDB, local storage, affinity rule or system '
                'Pod can make a node non-removable. Packing compatible workloads and selecting node shapes that match request profiles can '
                'lower node-hours, but reducing minimum nodes too far removes burst headroom and failure-domain slack. Track HPA desired/current '
                'replicas, pending-Pod duration, node count by pool and zone, allocatable/requested/used CPU and memory, autoscaler events, '
                'PDB status and node-hours. Explain any time lag between falling utilization and scale-down rather than assuming instant removal.\n\n'
                'A useful utilization measure has an explicit denominator. For example, request utilization = requested CPU / allocatable CPU '
                'helps describe scheduler packing, while measured CPU / allocatable CPU describes observed use; these answer different questions. '
                'Do not call unused requested capacity “free headroom” when it prevents a node from being removed. Conversely, a fully packed '
                'cluster can cost less per hour yet have less surge capacity and more noisy-neighbor risk.\n\n'
                '#### BigQuery: on-demand scans versus capacity\n'
                'For on-demand analysis, bytes processed are the main query cost driver. A partitioned table only prunes partitions when the '
                'query’s filter can be applied to the partitioning column; a predicate wrapped in an incompatible expression may not prune as '
                'expected. Columnar reads also mean selecting a subset of columns can matter. A LIMIT caps returned rows, not necessarily bytes '
                'read to produce them. A dry run estimates bytes before execution; after running, inspect actual bytes, slot time, the execution '
                'graph and output correctness. Maximum bytes billed is a guardrail for qualifying on-demand queries, not a replacement for '
                'query design.\n\n'
                'Capacity pricing changes the unit of comparison to allocated slot capacity over time. It can make a recurring, concurrent '
                'workload easier to budget, but slots are shared among assigned jobs and unused capacity has an opportunity cost. Higher slot '
                'availability does not guarantee a faster query; query plan shape, shuffle, skew and I/O still matter. Compare the same job '
                'mix over the same time window using processed bytes, slot time, reservation or autoscaling slot-hours, idle share and queued '
                'jobs. Keep storage, ingestion and network costs outside the query-compute comparison unless explicitly added.\n\n'
                'Worked scan example (synthetic): one report scans 2.4 TiB without a date partition predicate. If a correct date filter '
                'prunes 87.5%, the estimate is 2.4 × (1 − 0.875) = 0.3 TiB. At an explicitly assumed unit price R per TiB, one execution '
                'models as 2.4R versus 0.3R. At 10,000 equivalent executions, that is 24,000 versus 3,000 TiB processed and 24,000R versus '
                '3,000R; validate the assumed pruning with a dry run and result comparison. For a separate synthetic capacity case, 100 average '
                'slots held for 720 hours equal 72,000 slot-hours. Compare useful slot time and queued concurrency against a dated assumed '
                'slot-hour rate S; this is not a Google Cloud price quote and does not show that 100 slots are sufficient.\n\n'
                'When normalizing the three paths, hold useful output and service objectives constant. Runtime spending can be represented '
                'as active instance-hours × dated shape rate plus separately identified request or minimum-capacity terms; GKE as node-hours by '
                'pool × dated node rate plus any separately billed control-plane or storage terms; BigQuery on-demand as processed TiB × R, '
                'or capacity as slot-hours × S. Each formula is a structure for inserting validated price data, not a complete invoice.\n\n'
                'Written sources checked 2026-09-29: Google Cloud documents [Cloud Run instance autoscaling and scale-to-zero](https://docs.cloud.google.com/run/docs/about-instance-autoscaling), '
                '[Cloud Run concurrency tuning](https://docs.cloud.google.com/run/docs/tips/general#optimize_concurrency), '
                '[GKE cost optimization and cluster autoscaling](https://docs.cloud.google.com/kubernetes-engine/docs/best-practices/cost-optimization), '
                '[BigQuery pricing models and byte controls](https://cloud.google.com/bigquery/pricing), and '
                '[BigQuery estimate and control costs](https://docs.cloud.google.com/bigquery/docs/best-practices-costs) plus '
                '[BigQuery slots and capacity allocation](https://docs.cloud.google.com/bigquery/docs/slots).'
            ),
            'questions': [
                'Which observation distinguishes a utilization problem from a burst or cold-start problem?',
                'What scheduling constraint or disruption policy is keeping GKE nodes from scaling down?',
                'How many bytes does a representative query process before and after a partition predicate, and what utilization would make reserved capacity economical?'
            ],
            'reference': 'https://docs.cloud.google.com/bigquery/docs/best-practices-costs',
            'reference_label': 'Google Cloud: Estimate and control BigQuery costs, including dry-run byte estimates and capacity pricing (section checked 2026-09-29)',
            'scenario': {
                'scenario': 'Synthetic Brightloaf planning case, assembled for analysis rather than taken from production: the HTTP order API receives sharp daytime bursts and a long quiet window, while analytics runs 10,000 equivalent monthly reports over a partitioned event table. For comparison only, assume 2.4 TiB scanned per report without a date predicate, 87.5% pruning when the predicate is correct, 22 idle hours per day, and two serving candidates: Cloud Run with no minimum instances versus a small warm floor, and a GKE Standard pool with capacity provisioned for the peak. These values are scenario inputs, not Google Cloud usage or prices.',
                'impact': 'Three distinct defects could hide under the same monthly-total line: a zero-minimum Cloud Run service may reduce idle instance time but violate the cold-start objective; an always-warm floor may meet latency while paying through 22 quiet hours per day; and GKE requests that do not fit node shapes can strand capacity or prevent scale-down. Separately, a missing partition predicate leaves the scan at 2.4 TiB rather than the synthetic 0.3 TiB estimate, so 10,000 comparable runs imply 24,000 versus 3,000 TiB processed before price is applied. Without separated evidence, the team may reduce infrastructure at the cost of errors or continue paying for an inefficient query.',
                'constraints': 'The API must meet its agreed p95 cold-start and steady-state latency objectives, preserve peak throughput, and keep maximum database connections within the database budget. GKE must retain failure-domain and disruption headroom; a single-zone packed design is not an acceptable saving. Analytics output and row-level correctness must remain equal after query changes. No rates are official: insert a dated price assumption later and keep storage, ingestion, network and operations visible as separate categories.',
                'facts': 'Synthetic scenario facts only: 2.4 TiB estimated query scan without the filter; 87.5% assumed pruning when the correct date predicate is present; 10,000 monthly executions; 22 idle hours per day. These values are deliberately supplied inputs, not production observations, guaranteed query estimates, current tariffs or promised savings.',
                'inference': 'Potential causal chain to test: query omits a usable partition predicate → all date partitions remain eligible for scanning → bytes per execution stay near the unfiltered estimate → repeated execution multiplies the on-demand quantity. Independently, utilization averaged across busy and idle windows obscures minimum-capacity cost and cold-start risk; in GKE, mismatched requests and node shapes can fragment capacity and leave otherwise idle nodes non-removable. Confirm each link with query estimates and execution details, matched-window service metrics, scheduler state, autoscaler events and billing data before assigning causality.',
                'expected': 'A corrected worksheet has separate rows for Cloud Run active/idle time, GKE node-hours and BigQuery bytes/slot-hours; it computes 0.3 TiB per filtered scan and 3,000 TiB over 10,000 equivalent reports under the assumed pruning; and it names the latency, correctness, database-connection and disruption guardrails. It does not claim cash savings until rates and observed behavior are validated.',
                'evidence': '**Evidence boundary:** this is a tabletop case. Supplied synthetic inputs are 2.4 TiB per unfiltered execution, 87.5% assumed pruning, 10,000 executions and 22 quiet hours/day. Derived quantity: 2.4 × 0.125 = 0.3 TiB per filtered execution; monthly example quantity is 24,000 TiB before pruning versus 3,000 TiB after assumed pruning. No live dry run, runtime trace, cluster inventory or billing export has been observed. The lab’s later evidence fields must replace assumptions with same-period results.',
                'diagnostic_steps': [
                    'Separate reported facts, synthetic values and assumptions. Align service telemetry, query execution and billing export to the same region and time window; record each unit and denominator.',
                    'For Cloud Run, compare revisions and note minimum/maximum settings, billing mode, request count, instance count, concurrency, idle intervals, latency percentiles, 429/error rate and backing-database connections. Distinguish warm-floor spend from active request time.',
                    'For GKE, calculate requested / allocatable and used / allocatable CPU and memory by node pool. Check Pod fit, fragmentation, pending-Pod duration, node-hours, HPA target/current replicas, PDB status, affinity and autoscaler scale-down events.',
                    'For BigQuery, dry-run the same query with and without the partition predicate; ensure filters and selected columns preserve the same result semantics. After an authorized later run, compare actual processed bytes, query plan, slot time and result rows.',
                    'Trace the causal chain separately for runtime, scheduler and query: symptom → quantity → responsible control/boundary → corroborating signal. Reject a root cause if one of its required links lacks evidence.',
                    'Recalculate low/base/high totals with consistent traffic and output. Keep Cloud Run shape/time, GKE node-hours, BigQuery scan or slot-hours, and omitted storage/network costs in separate rows.',
                    'Write the approval test: change one lever at a time; require unchanged result correctness and agreed latency/reliability objectives; include rollback condition and price-validity date.'
                ],
                'root': 'Architectural inference and causal test: (1) a report aggregates work over the whole month and hides the busy/quiet distribution; (2) the Cloud Run choice therefore uses average CPU or monthly cost without isolating cold-start requests and idle-time behavior; (3) the GKE choice uses node count without examining request-based placement and scale-down blockers; (4) the query estimate omits a partition-pruning check; (5) all three are then valued with unaligned billing bases. This model explains the estimate only if the corresponding metrics and query evidence confirm each step. Alternative explanations include changed traffic mix, cold cache, data growth, new reservation assignments, system-Pod overhead or simply an incorrect assumed rate.',
                'fix': 'Correct the model before changing production configuration. For BigQuery, add a semantically correct partition predicate and required-column projection, capture a dry run, compare actual processed bytes and output correctness, and compare on-demand bytes cost with representative slot-hours at dated prices. For Cloud Run, tune concurrency only after a load test proves stable application and database behavior; choose the minimum floor from the latency objective and cap maximum instances against downstream limits. For GKE, right-size requests from representative peaks, pack compatible workloads without crossing failure-domain requirements, and review PDB/affinity constraints before autoscaler changes. Stage one lever at a time and preserve rollback values.',
                'verify': 'BigQuery evidence for the later lab: retain the exact SQL and table partition field, dry-run bytes for filtered/unfiltered variants, actual bytes processed after an authorized run, query plan/slot time, and checksums or equivalent row counts for result correctness. Runtime evidence: replay an identical request trace and compare p95/p99 latency, cold-start subset, errors/429s, instance time and database connections. GKE evidence: compare requested/allocatable/used CPU and memory, pending-Pod wait, node-hours, disruption status and scale events. Cost passes only if normalized spend falls under validated rates while workload output, SLO and recovery guardrails remain satisfied.',
                'residual': 'A dry run does not price storage, ingestion, network or every job class; query caching and changed data distributions can alter execution. Runtime tests may miss rare bursts or long-tail state, and autoscaler behavior can lag or be blocked by constraints. GKE packing can reduce spare capacity and amplify correlated failure. Rates, free allowances, quotas and service behavior change. Preserve a dated assumption ledger and revalidate with the actual project’s billing export before presenting savings as realized.',
                'diagram': ('Burst and idle traffic plus unfiltered analytical query arrive', 'Model mixes active runtime, unused node capacity and query billing bases', 'Idle spend or scan bytes exceed the estimate while peak latency remains unmeasured', 'Use partition filters, right-sized requests, packing and bounded scaling with SLO guardrails', 'Compare measured latency, correctness, bytes and billable hours on matched workloads')
            },
            'lab': {
                'name': 'Runtime and scan cost-driver worksheet',
                'file': 'day-121-runtime-cost-drivers.md',
                'goal': 'Build an auditable low/base/high workload-cost model for Cloud Run, GKE Standard and BigQuery. Trace every figure to a measured quantity, supplied synthetic value or dated price assumption, and preserve equal output and service objectives.',
                'expected': 'A saved worksheet contains separate runtime, node and query cost lines; the synthetic query calculation yields 0.3 TiB and 3,000 TiB/month after assumed pruning; a capacity alternative uses slot-hours; each model has units, boundaries, guardrails, confidence and a named validation step.',
                'mode': 'Offline tabletop worksheet; no cloud changes or spend.',
                'prereq': 'Day 119 dated cost baseline and Day 120 savings proposal; local editor or spreadsheet.',
                'preflight': 'Open the Day 119 baseline and Day 120 proposal. In a local spreadsheet or text note, record the review date, currency, region, evaluation window, workload owner and source artifact. Mark 2.4 TiB, 87.5% pruning, 10,000 runs and 22 quiet hours/day as supplied synthetic inputs. Do not enter credentials, access a production dataset or treat assumed rates as current prices. Set a common comparison window and output unit before calculating.',
                'steps': [
                    'Create a worksheet named “Runtime and query cost drivers” with one section each for Cloud Run, GKE Standard, BigQuery on-demand and BigQuery capacity. Each line must have quantity, unit, time window, formula, price source, included costs, excluded costs, confidence and evidence state (observed, synthetic, assumed, validate). Keep compute, storage, network and support costs in separate lines. State what “one unit of useful work” means for the chosen service, such as one successfully served order request or one completed analytics report.',
                    'Cloud Run section: record requests by hour or representative interval, request duration, concurrency distribution, active/idle instance observations, CPU/memory shape, billing mode, configured minimum and maximum, p95/p99 latency, errors and downstream connections. Calculate active instance-hours from the supplied trace when available; do not turn the 22-hour quiet period into a bill amount until billing mode and minimum-instance treatment are confirmed. Create two rows for zero minimum and warm floor, then state the cold-start/latency objective each row must meet.',
                    'GKE section: create one row per node pool. Record machine shape, allocatable CPU/memory, Pod requests, daemon/system overhead, requested and measured utilization, node count by zone, node-hours, pending-Pod time, autoscaler events and PDB/affinity constraints. Calculate requested-to-allocatable and used-to-allocatable ratios separately. Write the packing hypothesis (which Pods can share the node shape) and the failure-domain or burst headroom that must remain.',
                    'BigQuery scan section: calculate 2.4 TiB × (1 − 0.875) = 0.3 TiB per filtered report. For 10,000 equivalent reports, calculate 24,000 TiB unfiltered and 3,000 TiB under the supplied pruning assumption. Show the 87.5% reduction in processed quantity separately from money. Model on-demand query cost as scanned TiB × dated assumed rate R; leave R blank until sourced and dated. Note that output rows must remain equivalent and LIMIT is not the pruning mechanism.',
                    'BigQuery capacity section: use the explicit synthetic example of 100 average slots × 720 hours = 72,000 slot-hours. Compare it against the expected monthly job mix using observed or explicitly assumed useful slot time, idle share, queued jobs, concurrency and a dated assumed rate S. Add a decision field for workload steadiness and utilization evidence. Do not infer reservation break-even until both R and S are sourced and the job mix is representative.',
                    'Set three scenarios without mixing units: low (lower measured request/scan volume), base (representative period), high (peak/burst or larger data volume). For every scenario hold output correctness and latency/reliability guardrails constant, list which quantities changed and calculate cost only where rate input is valid. Add sensitivity notes: warm floor changes instance time; request shape changes concurrency; Pod requests change packability; date filter changes scan bytes; slot reservation size changes capacity-hours.',
                    'Review the calculation using two independent checks: re-derive every quantity from its unit and denominator, then trace each price to a dated official price source or mark “to validate.” Do not claim total savings if a required category is missing. Include a rollback condition for any later configuration change, such as p95 breach, elevated 429/errors, pending Pods or a result mismatch.',
                    'Write the Day 122 handoff: exact SQL/table/partition field to dry-run later, scan estimates before/after, actual bytes processed after an authorized execution, equivalent result comparison, and which billing-export rows would validate the applicable price. Mark all live observations as pending; this tabletop lab does not create them.'
                ],
                'verification': 'Recalculate the synthetic scan quantities independently: 2.4 × 0.125 = 0.3 TiB; multiply by 10,000 to get 3,000 TiB. Confirm the capacity unit: 100 slots × 720 hours = 72,000 slot-hours. Each runtime row has a matching time period, service mode, traffic quantity and guardrail; Cloud Run and GKE alternatives deliver the same useful work. Verify that unknown prices stay blank/assumed and are not reported as savings.',
                'accept': 'Save `day-121-runtime-cost-drivers.md` as the Day 121 cost-driver worksheet. Acceptance requires separate Cloud Run, GKE, BigQuery scan and slot-capacity lines; low/base/high quantities; source/confidence labels; a latency/capacity/correctness constraint; explicit synthetic calculations; omissions and a Day 122 validation checklist.',
                'trouble': 'If comparing models is ambiguous, align the same workload output, region and period. If scan bytes do not change after a partition predicate, verify the table partition field, predicate semantics, selected columns and dry-run estimate; do not “fix” the discrepancy by assuming a pruning percentage. If GKE reports unused CPU but no node scale-down, inspect requests, fragmentation, PodDisruptionBudget, local storage, affinity and system overhead. If Cloud Run cost/latency moves unexpectedly, separate cold-start requests, minimum instances, billing mode and revision traffic split. If a price is unavailable, keep the quantity calculation and leave the money field unpriced.',
                'cleanup': 'No resources are created. Keep the worksheet as the Day 121 exit artifact; remove only disposable copies.'
            }
        },
        {
            'key': 'topic-02',
            'title': 'Carbon Footprint reporting boundaries and placement assumptions',
            'overview': (
                'Carbon Footprint provides customer-specific greenhouse-gas reporting for supported Google Cloud usage under a published '
                'methodology. The report boundary matters: the product, project, region and month shown are part of the claim, while excluded '
                'products, embodied hardware impacts, other cloud providers, customer devices and application lifecycle effects are outside '
                'that reporting boundary unless explicitly covered by the methodology. Low-carbon placement is a conditional design option: '
                'confirm that the region supports the workload, residency and latency requirements, and compare the applicable reporting data '
                'and period. A carbon-free energy percentage or a region-level estimate does not by itself prove lower total emissions for '
                'a specific workload or justify violating availability, data location or recovery objectives.'
            ),
            'preview': (
                'A synthetic architecture review claims that moving every batch job to a region with a lower dashboard estimate will reduce total emissions.'
                ' The comparison may omit product coverage, workload utilization, transfer, resilience and residency constraints, leading to an unsupported sustainability decision.'
            ),
            'technical': (
                '#### Define the reporting object before comparing regions\n'
                'Treat Carbon Footprint as a customer-specific allocation estimate under a published accounting method, not a direct meter '
                'attached to one application. Save the report period, project filter, product/SKU coverage, region grouping, displayed metric '
                'and whether the figure is location-based or market-based. The methodology explains allocation from shared infrastructure and '
                'product usage into customer products, projects and regions, then aggregation at monthly granularity. A report row therefore '
                'inherits scope and allocation assumptions; it is not automatically a per-request or per-batch measurement. Changes to data '
                'sources or methodology may also adjust current or historical reported values.\n\n'
                'Location-based Scope 2 reflects electricity generation sources at a location and does not include Google’s carbon-free '
                'electricity purchases. Market-based Scope 2 applies those purchases using the market-based approach. The methodology uses '
                'hourly grid emission factors for location-based electricity reporting, while market-based factors are annual. Those metrics '
                'answer different accounting questions and should not be mixed in one before/after comparison. Monthly aggregation smooths '
                'short-term variation, so a monthly dashboard value cannot by itself justify a specific hour-of-day scheduling claim.\n\n'
                'The published report includes Google Cloud data-center operational sources such as on-site fuel and refrigerants, product '
                'electricity including cooling and lighting, embodied lifecycle emissions for data-center equipment and buildings, employee '
                'travel/commuting associated with data centers, transmission/distribution losses, and fuel supply chain emissions as described '
                'by the methodology. It excludes some activities, including small deployments at ISP partners, Google networking equipment '
                'outside data centers, downstream end-of-life emissions of data-center equipment/buildings, and embodied emissions for grid '
                'generation facilities/equipment. Treat these as reporting boundaries, not a claim that excluded effects are zero. Product '
                'coverage is not universal where SKU-to-service attribution is unavailable. Customer-specific report data is not third-party '
                'verified or assured; methodology review is not the same as assurance of each customer report.\n\n'
                '#### Low-carbon placement is a gated architecture decision\n'
                'A candidate location first has to support the services, required data location, connectivity, key dependencies and recovery '
                'design. Apply hard gates for residency, sovereignty, user latency, availability, RTO/RPO, capacity and operational ownership. '
                'Only then compare candidate report values for equivalent useful work and the same period. A region-level average is an input '
                'to a placement discussion, not proof that an individual workload will emit less there. Include changes to utilization, idle '
                'capacity, retries, cross-region reads/writes, replication, network path and completion time. Moving compute nearer data can '
                'reduce transfer, but moving data or adding replicas may increase it; write the actual data-flow assumption.\n\n'
                'For deferrable batch work, a schedule shift is feasible only if the completion deadline, queue growth, freshness contract, '
                'retry window and dependency availability permit it. A delayed batch can increase backlog and lengthen resource lifetime; '
                'parallelizing it later may cause a demand spike. Do not make a placement or schedule recommendation from a CFE percentage '
                'or a single regional ranking without verifying metric definition, report granularity and workload boundary. Keep cost and '
                'carbon values side by side because a placement change may affect both differently.\n\n'
                'A scoped comparison statement should name: (1) the report metric and period, (2) selected projects and covered products, '
                '(3) feasible regions after architecture gates, (4) equal useful output and execution window, (5) transfer/replication and '
                'utilization assumptions, and (6) unresolved exclusions. The resulting claim is “the reported estimate for this boundary '
                'changed under these assumptions,” not “the workload’s total lifecycle footprint is lower.”\n\n'
                'Written sources checked 2026-09-29: [View Carbon Footprint data](https://docs.cloud.google.com/carbon-footprint/docs/view-carbon-data?hl=en) describes estimated values for covered services and the dashboard’s region/project/product breakdowns; '
                '[Carbon Footprint methodology and boundaries](https://docs.cloud.google.com/carbon-footprint/docs/methodology) defines included and excluded activities and reporting limitations; '
                '[Services covered by Carbon Footprint](https://docs.cloud.google.com/carbon-footprint/docs/covered-services?hl=en) is a dated coverage list that must be checked for the workload. The exact workload-level impact remains an estimate that requires evidence and an explicit boundary.'
            ),
            'questions': [
                'Which products, projects, regions and months are represented in the report, and which are outside its boundary?',
                'Does the alternative placement preserve data residency, user latency, availability, RTO and RPO?',
                'Are both options compared for the same useful workload, utilization and transfer assumptions?'
            ],
            'reference': 'https://docs.cloud.google.com/carbon-footprint/docs/view-carbon-data?hl=en',
            'reference_label': 'Google Cloud: View Carbon Footprint data, metric tabs and region/project/product charts (section checked 2026-09-29)',
            'scenario': {
                'scenario': 'Synthetic Brightloaf case: an architecture review considers moving a monthly batch from Region A to Region B after a Carbon Footprint dashboard shows a lower location-based regional estimate for one reporting month in B. The proposed memo calls this “a reduction in the workload’s total emissions.” The packet does not yet identify product coverage, selected project filters, transfer/replication volume, completion time, data residency decision or whether the same amount of output completed in each region.',
                'impact': 'The claim could overstate what the report measures, and a move could add cross-region transfers, replication, idle capacity or retries. A seemingly greener placement could be impossible under residency rules, miss a freshness deadline, weaken the recovery plan or increase operational cost without reducing the stated workload’s emissions.',
                'constraints': 'Keep data within the approved jurisdiction; preserve the current RTO/RPO and service availability objective; finish the batch before the same freshness deadline; compare equal useful output over equivalent report periods; disclose product coverage and exclusions. No region ranking or numeric emission value is supplied here, and this is not an observed customer incident.',
                'facts': 'Supplied tabletop facts only: two candidate regions; one month of regional Carbon Footprint information; one displayed location-based estimate is lower; product coverage, selected project scope, equal workload completion, transfer, residency and recovery checks are missing. No dashboard result was opened or independently measured for this exercise.',
                'inference': 'The memo’s causal leap is from “one reported regional estimate is lower” to “this application’s total lifecycle emissions will fall.” The leap is unsupported because the report is allocated at product/project/region and monthly granularity, may not cover every SKU, and excludes activities in its methodology. A move can alter utilization, transfer, retries or replicas. These effects may change a workload-level comparison or make the destination infeasible; their direction cannot be inferred from the single displayed estimate.',
                'expected': 'A defensible review narrows the statement to the selected report metric, month, projects and covered products; screens candidate regions against architecture constraints; normalizes the work completed and its transfer/recovery overhead; and labels missing evidence. It recommends no placement change until data, service and sustainability owners accept the bounded evidence.',
                'evidence': '**Evidence boundary:** this is a supplied tabletop observation, not a live dashboard inspection. The only known report fact is that one selected location-based regional estimate appears lower for one month. Follow-up evidence must include the project/product filters and coverage, same-period regional values and metric definition, completed workload units and deadline, transfer/replication quantities, and approved residency/RTO/RPO. Leave unavailable fields unknown; do not interpolate missing values as zero.',
                'diagnostic_steps': [
                    'Quote the claim precisely and define the denominator: reported kg CO2e per month, per completed batch, or another explicitly supported unit. Do not label a report row as total lifecycle emissions.',
                    'Capture report month, selected projects, covered products/SKUs, region attribution and metric type (location-based or market-based). Use the methodology section to list included and excluded activity classes.',
                    'Separate what the displayed report actually establishes from what the proposal infers about the application. Check that the workload uses covered products and that project labels/scope include its resources.',
                    'Apply hard feasibility gates for residency, service availability in the region, user/data locality, dependency topology, RTO/RPO, replication design and batch deadline. Mark rejected locations and the exact failed gate.',
                    'For feasible candidates, compare equal completed outputs over equivalent periods. Add utilization, idle capacity, retry behavior, data movement, replicas and completion time as measured, assumed or unknown fields.',
                    'Run a sensitivity check: identify which unknown (coverage, transfer, utilization, recovery copy, or timing) could reverse the conclusion; do not make a numeric adjustment without evidence.',
                    'Draft a bounded finding with owner, evidence needed, decision status and review date. Keep the current approved placement until required evidence and approvals exist.'
                ],
                'root': 'Architectural inference: (1) the review packet contains a single lower location-based regional estimate for one month; (2) the memo omits the selected products/projects and methodology exclusions; (3) it compares region labels rather than equal useful workload and complete transfer/recovery paths; (4) it generalizes an allocated monthly report into a workload-specific total-emissions claim. This reasoning explains the unsupported conclusion; it does not show which region is better. A changed report filter, product mix, monthly variability, transfer path or recovery copy could alter the apparent result.',
                'fix': 'Rewrite the decision as a scoped hypothesis. Identify the report metric and month, selected projects and covered products, included/excluded sources, and uncertainty from the published methodology. First reject locations that fail residency, service, latency, RTO/RPO or deadline gates. For the remaining options, normalize completed workload, runtime utilization, retries and transfer/replication assumptions; state which fields are evidence versus unknown. Ask the sustainability owner to confirm report interpretation, the data owner to approve location and the service owner to accept resilience and latency. Stage measurement or a limited approved experiment before migration.',
                'verify': 'Reopen the methodology and report filters; reproduce the comparison for the same month, projects, products and metric type; verify that the workload’s SKUs are represented; compare equal batch completion and deadline; measure or bound inter-region transfer and replication; and review the service SLO and recovery plan. The acceptance statement must say what was observed, what was inferred, what remains outside report scope, and who approved the decision. Do not claim third-party assurance: customer-specific Carbon Footprint data is not assured.',
                'residual': 'A monthly aggregate can hide short-lived and hourly variation; regional averages do not resolve every workload-specific effect. Product mapping can leave usage uncovered, methodology/data-source changes can revise results, and the published boundary excludes some impacts. Transfer, additional replicas, lower utilization and retries are only accounted for if the comparison measures them. Retain the date, methodology reference, report filters and owner sign-off with the ADR so a future review can reproduce the same scoped claim.',
                'diagram': ('A dashboard shows a lower regional estimate for one month', 'Review assumes report covers all workload emissions and equal useful output', 'Placement recommendation may omit product exclusions, data transfer or residency', 'Define report boundary and compare only feasible regions for equivalent work', 'Publish a scoped estimate with owner approval and explicit remaining uncertainties')
            },
            'lab': {
                'name': 'Carbon reporting boundary and feasible-placement review',
                'file': 'day-121-carbon-boundary.md',
                'goal': 'Produce a reviewable Carbon Footprint boundary ledger and a placement decision record that separates the reported estimate from workload-level inference, filters out infeasible regions, and identifies owner approvals.',
                'expected': 'A dated boundary and metric statement, a same-period/equal-work comparison for feasible placements, included/excluded scope, evidence-versus-inference labels, sensitivity questions, owner sign-offs and explicit unknowns.',
                'mode': 'Offline tabletop review of supplied synthetic facts; do not access a production Carbon Footprint dashboard.',
                'prereq': 'Day 73 data/hybrid placement artifact and Day 119–120 cost evidence; Carbon Footprint methodology link in Part 2.',
                'preflight': 'Use the supplied tabletop statement and official methodology link; this lab does not require a live dashboard. Record which prior Day 73 placement/residency artifact and Day 119–120 cost assumptions apply. If an owner later repeats the exercise in an authorized project, they must first confirm identity, project, API, IAM, organization policy, location, inventory, billing and permission; no cloud access or resource creation is part of today’s exercise.',
                'steps': [
                    'Create a boundary ledger with fields for report month, selected organization/project filters, covered products/SKUs, region attribution, metric type, methodology/version context, included activity, excluded activity, data source, confidence and reviewer. Cite the methodology section for every statement about included or excluded emissions. Add a separate column for “claim supported?” so an uncovered product cannot silently inherit another product’s value.',
                    'Enter only the supplied tabletop observation: “two regions; one month; one location-based displayed estimate appears lower.” Mark it as a synthetic observation. Leave numeric report values, project selections and product coverage blank/unknown; do not fabricate a dashboard export. In a “known / unknown / owner” register, assign each missing filter, product mapping and workload quantity to the person who could supply it.',
                    'Use the methodology to distinguish location-based and market-based reporting. Write what each metric means, whether carbon-free electricity purchases are reflected, and why hourly versus annual factors and monthly aggregation affect the time resolution. Do not combine metric types or make an hourly claim from a monthly aggregate. Identify which interpretation is suitable for the organization’s stated reporting question, then record who owns that accounting choice.',
                    'Draw the workload boundary on paper: compute, storage, database, user traffic, source and destination data, replicas, retries and upstream/downstream services. Mark which resources change region and which stay fixed. Compare this boundary with the Carbon Footprint product/SKU coverage; list unmapped components and excluded activity classes explicitly instead of assigning them zero emissions.',
                    'Build a placement gate table for each candidate region: supported services; data residency and sovereignty; user/data locality; latency; network path; availability; RTO/RPO; recovery replication; capacity; batch deadline and freshness. Mark each gate pass/fail/unknown and name the accountable owner. Any hard-gate fail makes the candidate infeasible regardless of its report value. Include the evidence artifact needed for each pass (policy/approval, service availability, latency result, recovery test or capacity signal).',
                    'For options that pass, normalize to identical useful work and period. Record completed batches/rows or another workload unit, runtime hours and utilization, retries, idle capacity, data transfer, replication and cost as measured/assumed/unknown. State the evidence source for every measured field and explain how a missing field might change the decision. Keep the displayed report metric as its own column; do not add unlike measures into one arithmetic total without a documented, valid method.',
                    'Run a sensitivity review without inventing emissions factors: list the unknowns most likely to reverse the ranking, such as uncovered product use, extra replication, a different metric type, lower destination utilization or a longer completion window. For every unknown, name the exact measurement/report filter/approval that would resolve it, the owner, and whether the decision can be made before that evidence arrives. Then ask a peer: Are these the same projects/products/month? Did both placements complete equivalent work under the same resilience and deadline constraints? Which excluded or unknown effect could change the conclusion? Record the objection and either add evidence or narrow the claim; reviewer agreement is not independent verification of the data.',
                    'Write the bounded decision paragraph (“the selected report estimates… for projects/products… in month…”) and its non-claim (“this does not establish total lifecycle emissions for the application”). Record hold/move/measure decision, owner, conditions, approver, review date and reversal trigger. Assemble the evidence register with official source/access date, supplied scenario fact, architecture inference, missing item, action owner and decision effect. Require sustainability interpretation, data-location approval and service/recovery approval before any future placement change; leave the current approved deployment in place until that evidence and authorization exist.'
                ],
                'verification': 'A peer reviewer can locate the report month, selected projects, coverage and metric; distinguish methodology facts from workload assumptions; see each hard placement gate; confirm equal output and period for viable options; and identify who must resolve each unknown. The conclusion contains no unsupported numerical emissions reduction and makes no assurance claim.',
                'accept': 'Save `day-121-carbon-boundary.md` and attach it to the Day 121 cost-driver worksheet. It must include the method/scope ledger, feasible-placement gate table, same-work comparison fields, evidence register, uncertainty/sensitivity list, bounded claim and owner/approval path.',
                'trouble': 'If the regional result looks decisive, verify that metric type, month, project selection and covered products match. If the workload’s products may be absent from the report, mark coverage unresolved. If a location fails residency, service support or recovery, mark it infeasible rather than averaging away the constraint. If output differs or transfer/retry behavior is unknown, do not compare the reported value as if it were a normalized workload result.',
                'cleanup': 'No dashboard export, credential or cloud resource is created. Retain only the tabletop note and link it to the exit worksheet.'
            }
        }
    ]
}
