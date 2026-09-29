"""Day 125: profiling, load-based capacity, and ML accelerator sizing.

Cases are synthetic Brightloaf exercises. Labs are local/tabletop, with no
Google Cloud resource creation or claim of production measurements.
"""

DAY_NUM = 125


def lab(name, goal, expected, prereq, preflight, steps, verification, accept, trouble, cleanup, file):
    return {
        "name": name,
        "goal": goal,
        "expected": expected,
        "mode": "Local Python 3 standard library and tabletop analysis; synthetic data; no cloud provisioning or spend",
        "prereq": prereq,
        "preflight": preflight,
        "steps": [f"#### Stage {i}: {title}\n\n{body}" for i, (title, body) in enumerate(steps, 1)],
        "verification": verification,
        "accept": accept,
        "trouble": trouble,
        "cleanup": cleanup,
        "file": file,
    }


DATA = {
    "day": 125,
    "part1_intro": (
        "Day 125 turns a performance complaint into an evidence-backed capacity decision. Start with the same user-visible objective and "
        "workload, then use traces to locate elapsed time, profiles to identify code-level resource consumption, and bounded load "
        "experiments to find a sustainable operating point. For ML, translate model, sequence, batch, concurrency, memory and latency "
        "requirements into accelerator capacity assumptions. The distinction between a measured result and a projection is essential: "
        "profiles are sampled, load tests can miss production distributions, and accelerator availability and efficiency vary by model "
        "and deployment. Brightloaf values below are synthetic teaching inputs, never claims about an observed system."
    ),
    "exit_summary": (
        "A bottleneck diagnosis and capacity recommendation separating measured or supplied inputs from projections: a trace/profile "
        "evidence sheet, a load-test saturation/headroom curve, and an accelerator sizing worksheet with assumptions, limits and a "
        "verification plan. No cluster provisioning is required."
    ),
    "part2_intro": (
        "Read the path from user request or model batch through instrumentation, execution and capacity decision. Profiler attributes "
        "sampled resource use to code; Trace attributes request latency to spans; load tests measure system behavior under a declared "
        "workload; accelerator sizing projects resource fit from model and service requirements. The diagram is conceptual: it contains "
        "no measured Brightloaf telemetry and does not prove a bottleneck, safe capacity or a specific hardware choice."
    ),
    "arch_table_html": '''<div class="table-container"><table><thead><tr><th>Evidence boundary</th><th>Owner and mechanism</th><th>Compare / observable signal</th><th>Limit and decision consequence</th></tr></thead><tbody>
<tr><td>Request path and traces</td><td>Service owner propagates trace context; each instrumented service emits spans to Cloud Trace.</td><td>Root-span latency and child spans for queue, RPC, database, serialization; compare same route, status and workload window.</td><td>Missing context or spans make the path incomplete. A long span locates elapsed time but does not by itself explain CPU, queueing, or cause.</td></tr>
<tr><td>Code resource use</td><td>Runtime owner attaches a supported Profiler agent and tags service/version/zone consistently.</td><td>CPU-time, heap/allocation, wall-time or supported profile type; compare hot frames across representative versions and windows.</td><td>Statistical sampling is not a complete execution trace. Language and profile-type support differ; inspect overhead, sample volume and version before inferring.</td></tr>
<tr><td>Load / saturation boundary</td><td>Test owner defines closed-loop or arrival-rate model, payload mix, ramp, abort limits and a safe isolated target.</td><td>Offered and completed RPS, concurrency, p50/p95/p99, errors, queue age, CPU/memory, dependency utilization.</td><td>Open- and closed-loop tests answer different questions. Client bottlenecks, warm-up, cache, autoscaling and test-data shape can skew results.</td></tr>
<tr><td>Serving capacity and headroom</td><td>Platform and service owners translate a measured sustainable point plus availability/failover reserve into capacity policy.</td><td>Peak and forecast demand, per-instance throughput, autoscale lag, failover load, quota/reservation/region availability.</td><td>Headroom is a policy under stated assumptions, not a universal percentage. A regional or dependency limit may bind before compute.</td></tr>
<tr><td>GPU / TPU fit</td><td>ML platform owner maps model precision, parameter/activation/KV-cache memory, sequence length, batch, concurrency, interconnect and serving target to candidate capacity.</td><td>Peak memory, tokens or examples per second, time-to-first-token, inter-token latency, utilization, OOM/retry behavior and quality parity.</td><td>Peak memory and communication can dominate nominal FLOPs. Candidate generation, framework/kernel support, topology, quota and available stock require current verification.</td></tr>
</tbody></table></div>''',
    "arch_diagram": {
        "type": "topology",
        "title": "Day 125 performance evidence to capacity decision path",
        "desc": "A request and model workload produce traces, statistical profiles, load-test measurements and accelerator memory/throughput evidence. Owners reconcile measured signals with demand and availability assumptions before documenting a capacity recommendation.",
        "caption": "Figure 125.1: Conceptual evidence and ownership path from workload to capacity recommendation. It is not a measured deployment, does not prove causality, and does not establish accelerator availability or forecast accuracy.",
        "width": 1120, "height": 650,
        "layers": [
            {"name": "WORKLOAD CONTRACT · USER OBJECTIVE · MODEL / REQUEST MIX", "y": 24, "h": 88, "fill": "#102b46", "title_color": "#7dd3fc", "desc": "same inputs, correctness, deadlines and demand window"},
            {"name": "OBSERVABILITY · TRACE LATENCY · PROFILE RESOURCE ATTRIBUTION", "y": 145, "h": 95, "fill": "#073b33", "title_color": "#6ee7b7", "desc": "different evidence types; correlate by service/version/time"},
            {"name": "CONTROLLED LOAD · SUSTAINABLE KNEE · DEPENDENCY CEILINGS", "y": 272, "h": 95, "fill": "#422006", "title_color": "#fdba74", "desc": "ramp, errors, percentiles, queues, utilization and aborts"},
            {"name": "ML ACCELERATOR FIT · MEMORY · BATCH · COMMUNICATION", "y": 399, "h": 95, "fill": "#27204b", "title_color": "#c4b5fd", "desc": "model-specific evidence; CPU/GPU/TPU candidate constraints"},
            {"name": "CAPACITY RECOMMENDATION · RESERVE · VALIDATION PLAN", "y": 526, "h": 92, "fill": "#3b182c", "title_color": "#fda4af", "desc": "measured values separate from estimates and open assumptions"},
        ],
        "components": [
            {"x": 45, "y": 48, "w": 215, "h": 48, "name": "API request", "detail": "route · payload · objective", "stroke": "#38bdf8"},
            {"x": 350, "y": 48, "w": 245, "h": 48, "name": "Inference batch", "detail": "model · prompt · sequence", "stroke": "#38bdf8"},
            {"x": 695, "y": 48, "w": 250, "h": 48, "name": "Declared workload", "detail": "rate · concurrency · correctness", "stroke": "#38bdf8"},
            {"x": 65, "y": 169, "w": 265, "h": 48, "name": "Cloud Trace spans", "detail": "where elapsed time occurs", "stroke": "#22c55e"},
            {"x": 420, "y": 169, "w": 265, "h": 48, "name": "Cloud Profiler", "detail": "sampled CPU / memory by code", "stroke": "#22c55e"},
            {"x": 765, "y": 169, "w": 270, "h": 48, "name": "Version + time alignment", "detail": "join evidence; no causal shortcut", "stroke": "#22c55e"},
            {"x": 65, "y": 296, "w": 265, "h": 48, "name": "Load generator", "detail": "ramp · mix · abort rules", "stroke": "#f59e0b"},
            {"x": 420, "y": 296, "w": 265, "h": 48, "name": "Service + dependencies", "detail": "latency · errors · queues", "stroke": "#f59e0b"},
            {"x": 765, "y": 296, "w": 270, "h": 48, "name": "Saturation knee", "detail": "sustainable rate under this test", "stroke": "#f59e0b"},
            {"x": 65, "y": 423, "w": 265, "h": 48, "name": "Model envelope", "detail": "weights · activations · KV cache", "stroke": "#a78bfa"},
            {"x": 420, "y": 423, "w": 265, "h": 48, "name": "Accelerator candidates", "detail": "memory · topology · support", "stroke": "#a78bfa"},
            {"x": 765, "y": 423, "w": 270, "h": 48, "name": "Quality + serving SLO", "detail": "TTFT · token latency · parity", "stroke": "#a78bfa"},
            {"x": 235, "y": 550, "w": 300, "h": 48, "name": "Measured / supplied evidence", "detail": "source and confidence recorded", "stroke": "#f472b6"},
            {"x": 625, "y": 550, "w": 330, "h": 48, "name": "Projection + recommendation", "detail": "headroom · limits · next validation", "stroke": "#f472b6"},
        ],
        "flows": [
            {"x1": 260, "y1": 72, "x2": 350, "y2": 72, "label": "same objective", "type": "ok"},
            {"x1": 595, "y1": 72, "x2": 695, "y2": 72, "label": "defined mix", "type": "ok"},
            {"x1": 330, "y1": 193, "x2": 420, "y2": 193, "label": "correlate", "type": "ok"},
            {"x1": 685, "y1": 193, "x2": 765, "y2": 193, "label": "align version", "type": "ok"},
            {"x1": 330, "y1": 320, "x2": 420, "y2": 320, "label": "offer load", "type": "ok"},
            {"x1": 685, "y1": 320, "x2": 765, "y2": 320, "label": "find knee", "type": "ok"},
            {"x1": 330, "y1": 447, "x2": 420, "y2": 447, "label": "map memory", "type": "ok"},
            {"x1": 685, "y1": 447, "x2": 765, "y2": 447, "label": "verify quality", "type": "ok"},
            {"x1": 535, "y1": 574, "x2": 625, "y2": 574, "label": "label projection", "type": "warn"},
            {"x1": 170, "y1": 344, "x2": 385, "y2": 550, "label": "evidence", "type": "warn"},
            {"x1": 900, "y1": 344, "x2": 820, "y2": 550, "label": "assumptions", "type": "warn"},
        ],
        "boundaries": [
            {"x": 40, "y": 132, "w": 1015, "h": 112, "label": "OBSERVATION BOUNDARY · TRACE LOCATES WAIT; PROFILE ATTRIBUTES SAMPLED RESOURCE USE"},
            {"x": 40, "y": 516, "w": 1015, "h": 100, "label": "DECISION BOUNDARY · MEASUREMENT ENDS; FORECAST / HEADROOM BEGINS"},
        ],
        "probes": [
            {"cx": 1058, "cy": 130, "label": "P1: correlate trace, profile, service version and time window", "color": "#38bdf8"},
            {"cx": 1058, "cy": 263, "label": "P2: stop at declared error / latency / resource abort threshold", "color": "#f59e0b"},
            {"cx": 1058, "cy": 390, "label": "P3: include peak accelerator memory and quality constraints", "color": "#a78bfa"},
        ],
    },
    "part3_intro": (
        "The following Brightloaf cases are constructed teaching scenarios, not observed production incidents. Supplied synthetic values "
        "are evidence only for the exercise; causal statements are explicitly hypotheses until a matched experiment or production "
        "measurement confirms them. Each correction includes an observable acceptance check and residual uncertainty."
    ),
    "part4_intro": (
        "Complete three local/tabletop exercises using synthetic data only. Every exercise has eight stages: validate the environment and "
        "assumptions, prepare inputs, author a plan, execute or simulate, inspect outcomes, challenge a bounded failure or edge case, "
        "record diagnosis and decision, and close out. Do not create cloud resources, inject faults into a live service, or relabel a "
        "projection as a measurement. Save the topic artifacts, then combine them into the Day 125 exit recommendation."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Profiling with Cloud Profiler and Trace",
            "overview": (
                "A trace follows one request across service boundaries and shows where its elapsed time accumulated; a profile samples "
                "resource activity such as CPU or heap use and attributes it to code. Together they connect user-visible delay to "
                "candidate work, but they answer different questions: elapsed time may include waiting while a CPU profile samples "
                "execution. This belongs after Day 124's bottleneck vocabulary because an architect must separate database, network, "
                "queue and application waits before recommending more capacity. Service owners own instrumentation, context propagation, "
                "labels and access; platform owners own collection and data-access boundaries. Support varies by runtime/profile type, "
                "and sampling plus incomplete instrumentation limits conclusions."
            ),
            "preview": "A checkout trace shows a long inventory RPC while a CPU profile shows little application CPU in the same window. Scaling API instances may add cost without shortening the dependency wait, delaying orders and obscuring the inventory team's capacity need.",
            "technical": """## Read traces as elapsed-time evidence

A trace ID joins spans for an end-to-end operation; parent/child relationships provide a request path across instrumented services. Compare the root span with child spans and inspect gaps, RPC client/server pairs, retries, status, and request class. Trace is useful for locating where latency occurs and comparing distributions. It does not prove why a span is slow: a long RPC span could reflect remote work, queueing, network transit, retries, or client-side waiting. Missing propagation can split a request into unrelated traces; sampling and instrumentation policy can make the visible set unrepresentative. Keep identifiers and attributes free of sensitive customer data.

## Use profiles to find sampled resource consumers

Cloud Profiler combines a runtime agent/library with a service interface. Its statistical profiles attribute supported resource samples to stack frames; language and profile-type coverage differ. CPU-time, heap/allocation, wall-time, contention or thread views answer different questions where available. Compare service, version, zone, profile type and time window. A hot frame is a candidate for code investigation, not proof that it is the sole user-visible bottleneck. Sampling can miss rare events, and CPU profiles will not explain time blocked on a remote dependency. Consider collection overhead and whether the workload and version are representative.

## Correlate without conflating signals

Align a trace population and profile window by service/version and workload window; then test a hypothesis with a controlled change while preserving traffic mix and correctness. For example, a long span plus a hot serialization frame suggests a different intervention from a long downstream span with low local CPU. Watch dependency latency, errors, retries, resource saturation and business outcomes after a change. The service team owns code and propagation; the platform team owns runtime support, permissions, quotas and collection policy; the dependency owner must confirm its own evidence. Cloud Trace and Profiler data are retained for finite periods and access is IAM-controlled, so export only what policy permits and keep a reproducible evidence summary.

Official references: [Cloud Profiler overview and supported profile types](https://docs.cloud.google.com/profiler/docs/about-profiler) and [Cloud Trace traces and spans](https://docs.cloud.google.com/trace/docs/traces-and-spans).""",
            "questions": [
                "Which exact span owns most of the user-visible elapsed time, and are gaps or retries present?",
                "Does the profile show CPU, memory, contention or wall-time evidence that matches the trace window and service version?",
                "Which runtime, profile type, sample population and instrumentation gaps limit this conclusion?",
                "What controlled change would distinguish application work from downstream waiting without changing correctness?",
            ],
            "reference": "https://docs.cloud.google.com/profiler/docs/about-profiler",
            "reference_label": "Cloud Profiler overview: components, supported profiles and performance impact (accessed 2026-09-29)",
            "scenario": {
                "scenario": "Synthetic supplied fixture: a checkout root span is 820 ms at p95; its inventory RPC child is 610 ms with a retry attribute. In the matching sample window, application CPU profiles emphasize response serialization, but the fixture supplies no inventory server trace or profile.",
                "impact": "Checkout delay can increase abandonment and retries. The service team cannot claim that its own CPU is the whole cause or size inventory capacity from client-side data alone.",
                "constraints": "Preserve one fulfillment per order; compare only the same route, version, status mix and window; avoid customer identifiers; distinguish fixture facts from inferred causes.",
                "evidence": "Synthetic fixture supplied for this exercise: root p95 820 ms; inventory RPC child 610 ms with one retry; local serialization profile sample share 28%; inventory-side telemetry absent. These values are not production observations.",
                "root": "Hypothesis, not established fact: retry and remote inventory wait dominate this sample's checkout elapsed time, while serialization is a separate local CPU candidate. Client-side spans cannot establish the inventory server cause.",
                "diagnostic_steps": [
                    "Group traces by route, status and release; compare root and child-span distributions and check whether the 610 ms child includes retry time.",
                    "Align profile service/version/window and inspect profile type, sample count and hot stack frames; confirm that serialization is materially CPU-bound.",
                    "Request inventory owner evidence for server spans, queueing, saturation and retry policy; record the missing evidence if unavailable.",
                ],
                "remediation_steps": [
                    "Bound retry attempts and deadline budget at the caller, with jitter where retries are appropriate; do not retry a non-idempotent fulfillment effect without an idempotency key.",
                    "Optimize serialization only if a controlled same-workload comparison shows material CPU or latency improvement; consider caching only with explicit freshness and invalidation rules.",
                    "Coordinate with inventory owner to inspect its server-side span and saturation; keep a dependency timeout/fallback decision explicit.",
                ],
                "verify": "On a matched synthetic or approved test workload, compare trace percentiles, retry counts, error rate, profile samples and order outcomes. Require one fulfillment per order and no increase in inventory errors; label missing server-side evidence.",
                "residual": "A sampled profile can miss rare paths and a client trace cannot localize server work without propagated instrumentation. Production behavior, privacy policy and service-specific collection support require separate review.",
                "diagram": ["Checkout request has a long inventory child span and retry", "Assuming local CPU is the sole cause without server evidence", "Extra API replicas fail to remove remote wait; retries may rise", "Join trace with aligned profile and inventory-side telemetry", "Matched workload confirms where elapsed time and sampled resource use occur"],
                "facts": "The p95, child duration, retry marker and sample share are synthetic supplied exercise values only.",
                "inference": "Remote inventory wait is a candidate dominant delay; lack of server telemetry prevents proving its internal cause.",
                "expected": "A verified recommendation reports measured/supplied facts, hypothesis, matched test plan, one-fulfillment invariant and remaining uncertainty.",
            },
            "lab": lab(
                "Trace-to-profile bottleneck evidence worksheet",
                "Build a reproducible evidence sheet that distinguishes request elapsed-time location from sampled code resource attribution and selects a bounded validation experiment.",
                "A local CSV analysis and Markdown recommendation identify the dominant supplied wait, a separate code-level candidate, missing evidence, and a verification plan.",
                "Day 124 bottleneck taxonomy and Day 97 performance objective artifact; Python 3 standard library and spreadsheet/editor optional.",
                "Use synthetic fixture values from the case only. Confirm local Python 3 works, choose a writable exercise directory, record UTC/local time and workload/version labels, and confirm no project, credentials or live endpoint are involved.",
                [
                    ("Preflight evidence and assumptions", "Create `day-125-topic-01.md`. Record objective, synthetic-data label, route/version/window, profile type, sample limitation, privacy constraint and prior Day 124 objective. Mark supplied values separately from anything locally measured."),
                    ("Prepare the aligned inputs", "Create two small tables: a trace table with root/child duration, retry/status and missing spans; a profile table with service/version, profile type, sample share and capture window. Enter only the supplied synthetic fixture and leave unavailable inventory-side evidence blank with an explicit reason."),
                    ("Author the diagnostic plan", "Write a three-step hypothesis test: segment traces by route/status/release; compare child spans and retry time; align the profile and request inventory-side spans. State the falsifier for the remote-wait hypothesis and the falsifier for CPU-bound serialization."),
                    ("Execute the local evidence join", "Using a spreadsheet or a short standard-library script, join the two tables on service, version and overlapping time window. Produce a concise summary with source labels (supplied, locally calculated, inferred). Do not synthesize a production trace or present fixture arithmetic as observation."),
                    ("Inspect expected state and outcome", "Check that the summary preserves the supplied root and child values, identifies the inventory-side telemetry gap, does not add child durations as if spans were necessarily sequential, and separates the serialization profile candidate from end-to-end latency."),
                    ("Challenge a bounded edge case", "Run a second worksheet pass with one retry removed in the hypothetical trace while keeping all other inputs fixed. Predict which values could change and which remain unknown. This is a tabletop sensitivity check; it does not change a live service."),
                    ("Diagnose and record the decision", "Record the first evidence boundary that blocks attribution, the next owner/evidence needed, a reversible candidate action, acceptance signals (latency, errors, retries and one fulfillment), and residual risk. Label each statement fact, calculation, inference or prediction."),
                    ("Close out and preserve the artifact", "Save the Markdown report and its input table, note that no cloud resource or credential was used, and link the result in the combined Day 125 exit recommendation. Retain synthetic values with their source label."),
                ],
                "Verify trace/profile joins use service, version and overlapping window; check facts remain unchanged; ensure uncertainty about inventory-side cause and sampling is explicit; retain one fulfillment per order.",
                "Accept `day-125-topic-01.md` plus a compact input table with source labels, a trace/profile hypothesis and falsifier, an explicit missing-evidence list, and a bounded validation plan. Include the Day 124 objective and state no production profiling was performed.",
                "If spans do not add to the root duration, inspect concurrency/overlap and gaps instead of forcing a sum. If profile metadata does not align, mark the comparison invalid. If sample share appears causal, rewrite it as an attribution candidate pending controlled validation.",
                "No cloud resources created. Keep the local report as exit evidence; remove only disposable copies and do not include real request IDs, payloads, credentials or customer data.",
                "day-125-topic-01-evidence.md",
            ),
        },
        {
            "key": "topic-02",
            "title": "Load testing to size systems",
            "overview": (
                "Load testing measures how a defined system responds to a defined workload; it does not produce a universal capacity number. "
                "Test shape matters: closed-loop virtual users wait for responses and can reduce offered load as latency rises, while an "
                "arrival-rate test aims to sustain arrivals and exposes queue growth or dropped work. This follows Day 124's latency and "
                "queue diagnosis by finding the operating region where objectives still hold. The test owner must bound target, duration, "
                "concurrency and abort rules; application and dependency owners must monitor their limits. Warm-up, cache, test data, "
                "autoscale delay and shared dependencies can distort results, so preserve the workload contract and include failover and "
                "forecast assumptions in the later capacity estimate."
            ),
            "preview": "A closed-loop test reports stable latency while rising server delay silently reduces its offered request rate. The projected capacity then falls short during a real launch, increasing timeouts and lost checkout attempts.",
            "technical": """## Define the workload contract before running a test

Write the request mix, payload sizes, authentication pattern, read/write ratios, data cardinality, correctness assertions, client locations, arrival model, concurrency/ramp, duration and warm-up. Set success objectives such as latency percentiles and error ratio, plus hard aborts for error rate, latency, queue age, dependency saturation or spend/time. Use an isolated, authorized target and synthetic data. A closed-loop user generator waits for each response, so saturation can lower offered load (coordinated omission); an arrival-rate generator attempts a target rate, but can itself fail to keep up. Record achieved as well as requested load.

## Find a sustainable knee, not a peak number

Ramp in controlled steps and collect offered/completed requests per second, p50/p95/p99, errors, timeouts, queue depth and oldest age, CPU/memory, connection/pool waits and dependency utilization. The saturation knee is workload-specific: beyond it, tail latency, errors or backlog can rise nonlinearly while throughput plateaus. Repeat runs and distinguish cold start from steady state. Autoscaling introduces reaction delay and may shift the knee; a test that stops before scale-out or warms all caches can misstate normal behavior. Abort on predeclared limits; do not use an uncontrolled stress test against production.

## Turn observations into capacity with explicit assumptions

Measure per-instance sustainable throughput under the accepted latency/error objective, then model expected peak arrival rate, deployment rollout overlap, autoscale lag, dependency ceilings, regional failure load and a policy reserve. If one instance handles r requests/s at target quality and demand is d, the arithmetic lower bound ceil(d/r) is not by itself a safe fleet size; account for skew, redundancy, overhead and service limits. Use separate measured and forecast columns. Validate the recommendation in a staged environment and compare actual peak demand with the forecast after release. Google Cloud's performance guidance frames ongoing optimization as allocation, elasticity, modular design and continuous monitoring rather than a one-time benchmark.

References: [Well-Architected Framework performance optimization](https://docs.cloud.google.com/architecture/framework/performance-optimization) and [Cloud Trace: finding and exploring traces](https://docs.cloud.google.com/trace/docs/finding-traces).""",
            "questions": [
                "Is the generator closed-loop or arrival-rate based, and what was the achieved offered rate at each step?",
                "At what load do tail latency, errors or oldest queue age break the objective, even if average latency remains acceptable?",
                "Did warm-up, cache state, client capacity or autoscaler delay change what the test represents?",
                "Which inputs are measured; which demand, failover, rollout and reserve values are projections?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/performance-optimization",
            "reference_label": "Well-Architected Framework: performance optimization (accessed 2026-09-29)",
            "scenario": {
                "scenario": "Synthetic fixture: a checkout load test targets 900 requests/s with a closed-loop generator. At the last ramp, it completes 640 requests/s, p95 latency is 1.8 s, and the waiting queue grows; the report labels the result as 900 requests/s because that was the configured target.",
                "impact": "Capacity is overstated and launch planning may omit instances or backpressure. When real arrivals exceed completions, queue delay and retries can compound and impair checkout.",
                "constraints": "The fixture is synthetic; no actual test ran. Preserve request mix/correctness, use a bounded isolated target, define abort thresholds, and never infer production capacity directly from this dataset.",
                "evidence": "Synthetic fixture supplied for this exercise: configured target 900 requests/s; completed rate 640 requests/s; p95 1.8 s; queue grows at the final step. Client utilization, warm-up, dependency metrics and repeated-run variance are not supplied.",
                "root": "Hypothesis: the report confuses configured target with achieved offered/completed throughput, and the closed-loop generator may reduce load as response time rises. Queue growth is consistent with arrival exceeding service rate but does not identify which component limits service.",
                "diagnostic_steps": [
                    "Reconstruct each ramp step using target arrival, achieved offered rate, completed rate, dropped/failed requests and generator CPU/network capacity.",
                    "Align latency percentiles and error rate with oldest queue age, worker concurrency, CPU/memory and dependency saturation; identify the first objective breach.",
                    "Check warm-up, cache, data mix, autoscale events, repeated-run variance and whether each run used the same test version and target.",
                ],
                "remediation_steps": [
                    "Correct the report to distinguish configured target, achieved offered rate and completed throughput; preserve the closed-loop model label.",
                    "Repeat only in an authorized isolated environment with a declared arrival model, ramp, warm-up, fixed request mix, bounded duration and abort thresholds.",
                    "Choose the sustainable operating point below the measured objective breach, then separately model forecast peak, rollout overlap, dependency ceiling and regional failover reserve.",
                ],
                "verify": "Require repeatable runs whose achieved workload is known, correctness assertions pass, tail latency/errors/queue age remain within the declared objective, and generator utilization is not the limit. Validate the projected fleet in staging; compare later production telemetry without asserting the fixture predicts it.",
                "residual": "The fixture lacks generator utilization, dependency metrics, warm-up state and variance. Environment differences, demand mix, shared limits and scale-out lag can still invalidate capacity projections.",
                "diagram": ["Report records configured 900 requests/s target", "Generator's achieved rate and service completions are not distinguished", "Queue grows while p95 crosses the objective; capacity is overstated", "Repeat bounded test and capture offered, completed, queue and dependency signals", "Sustainable rate and projected reserve remain separately labeled"],
                "facts": "The target, completion rate, p95 and queue growth are supplied synthetic values; no real test was performed.",
                "inference": "Closed-loop under-delivery and a system bottleneck are plausible; the available values cannot name the saturated component.",
                "expected": "A corrected report states achieved load, objective-compliant operating point, test limitations and a separate forecast/headroom calculation.",
            },
            "lab": lab(
                "Synthetic load curve and capacity headroom analysis",
                "Analyze a small synthetic ramp to find the first objective breach, distinguish generator target from achieved throughput, and create a capacity projection with explicit assumptions.",
                "A reproducible local Python analysis or spreadsheet produces a labeled load curve, sustainable operating point, illustrative capacity arithmetic and a list of validation gaps.",
                "Day 124 latency/queue evidence; Day 97 service objective and workload assumptions; Python 3 standard library or spreadsheet.",
                "Use synthetic rows included below; no external target or load generator. Check Python/editor availability and writable path; record objective and abort threshold before calculations. Do not point scripts at a cloud or production endpoint.",
                [
                    ("Preflight workload and safety", "Create `day-125-topic-02.md`. Record the service objective, synthetic-only mode, route mix, arrival model, test duration assumption, correctness invariant, hard stop and target owner. Confirm there is no live endpoint, credential or cloud project in scope."),
                    ("Prepare the synthetic ramp", "Enter rows for configured target / achieved offered / completed RPS / p95 ms / error percent / oldest queue age seconds: (200, 198, 196, 120, 0.1, 0); (400, 395, 390, 180, 0.2, 0); (600, 580, 570, 260, 0.5, 1); (900, 700, 640, 1800, 3.0, 24). Label every value as synthetic fixture data."),
                    ("Author the analysis plan", "Define the acceptance objective for this exercise as p95 <= 300 ms, errors <= 1%, and non-growing queue. Mark the first row breaching any criterion; preserve the distinction between configured target, achieved offered rate and completed rate. Write what extra signals are needed to identify the bottleneck."),
                    ("Execute the local calculation", "Use a spreadsheet or Python 3 standard library to calculate completion-to-achieved ratio for each row and flag objective breaches. Plot or tabulate completed throughput versus achieved load. Add one transparent illustrative sizing example using the highest compliant completed rate, clearly labeled as a lower-bound projection rather than observed fleet capacity."),
                    ("Inspect the expected state", "Verify the final row is not called a 900 RPS achieved result, the 900 target row breaches p95 and errors, the earlier compliant rows are reported accurately, and the queue-growth signal is retained. Confirm the formula uses consistent units and no projection is presented as a measurement."),
                    ("Challenge an edge case", "Repeat the arithmetic after hypothetically removing the final row as a client-generator-limited sample. Keep the row in the evidence, label exclusion as a sensitivity scenario, and record why generator CPU/network plus service dependency metrics would be needed before discarding it."),
                    ("Diagnose and record the capacity decision", "Document the first objective breach, provisional sustainable point, alternative interpretation, missing signals, repeat-test design and later staging verification. Separate measured (none), supplied synthetic fixture, derived arithmetic and forecast assumptions."),
                    ("Close out and preserve evidence", "Save the table/script and Markdown report; include the workload contract, abort gate and projection caveat in the combined Day 125 recommendation. Confirm the exercise created no cloud resources and did not send traffic."),
                ],
                "Recompute the flags from the declared objective; check the final row fails both latency and error criteria and has queue growth; ensure target, offered and completed columns remain distinct and projections are explicitly illustrative.",
                "Accept `day-125-topic-02-capacity.md` and the synthetic input table or script, with objective, first breach, sustainable-point rationale, at least one transparent capacity calculation, missing evidence, abort gate, and separate measurement/projection labels.",
                "If p95 and error thresholds point to different rows, state the stricter first breach. If the queue-age interpretation is unknown, mark it supplied synthetic evidence. If your tool produces a graph without the original rows, save both for auditability.",
                "No load is sent to any service and no cloud resource is created. Keep the synthetic analysis; delete disposable output only. Any future real test requires separate target authorization, environment safety checks and bounded cost controls.",
                "day-125-topic-02-capacity.md",
            ),
        },
        {
            "key": "topic-03",
            "title": "Right-sizing GPUs/TPUs for ML workloads",
            "overview": (
                "Accelerator sizing begins with the workload, not a hardware label: training, fine-tuning, batch inference and interactive "
                "serving impose different compute, memory, communication and latency constraints. Model weights are only one memory term; "
                "activations, optimizer state, KV cache, sequence length, batch/concurrency and runtime overhead can dominate. Distributed "
                "training adds communication and topology constraints, while serving trades throughput batching against time-to-first-token "
                "and inter-token latency. This belongs after measured capacity work because sizing is a projection unless the same model, "
                "precision, software stack and target workload have been benchmarked. ML platform owners check framework support, quota, "
                "region/zone availability and reservation lead time. This day's practice deliberately reviews a supplied example without "
                "provisioning a cluster."
            ),
            "preview": "A team selects a GPU by parameter count alone and omits long-context KV cache and concurrent requests from memory sizing. Requests hit out-of-memory retries or excessive latency, delaying model responses and wasting reserved capacity.",
            "technical": """## Turn workload shape into a memory and service envelope

First classify the job: pretraining/fine-tuning, batch inference, or online serving; record model architecture/version, parameter count, precision/quantization, context and output lengths, batch, concurrent sequences, parallelism and quality constraints. Estimate weights as a starting term only. Include activations and temporary workspaces, optimizer state for training, KV cache for autoregressive serving, framework/runtime overhead and a safety allowance based on actual measurement. KV cache grows with layers, active tokens and concurrent sequences; longer contexts and larger batches increase memory pressure. Do not treat a vendor headline memory figure or parameter count as a fit guarantee.

## Capacity is compute, memory, communication and availability

Compare candidate accelerators against peak memory, sustained tokens/examples per second, time-to-first-token, inter-token latency, batch throughput, model quality and energy/cost policy. For multi-device work, account for tensor/pipeline/data parallelism, all-reduce or other communication, topology/interconnect, host CPU, network and storage feed. A theoretically sufficient device count can underperform if communication or input pipeline dominates. Profile and benchmark the actual model/software stack with representative sequence/batch distributions and warm/cold conditions. Reserve capacity may require a different lead time and access path from ordinary on-demand allocation.

## Make the recommendation conditional and testable

Build candidate rows with assumptions, expected peak memory, performance target, measured versus projected throughput, software compatibility, quota/region/zone status, reservation plan, scaling behavior and failure fallback. Current accelerator generations, machine families, supported topology, stock, quotas and commercial terms change; verify them during planning. AI Hypercomputer's workflow starts by identifying workload and choosing machine type, consumption, deployment and orchestrator, but this exercise stops at design review. A model-quality regression, unsupported kernel, quota shortage or region failure can invalidate a paper fit. Require a representative benchmark and a bounded canary before approving deployment.

References: [AI Hypercomputer: plan and create AI infrastructure](https://docs.cloud.google.com/ai-hypercomputer/docs/process-overview) and [AI Hypercomputer overview](https://docs.cloud.google.com/ai-hypercomputer/docs/overview).""",
            "questions": [
                "Is the job training, batch inference or online serving, and what are its latency and quality objectives?",
                "Which memory terms beyond weights are material for the model, sequence length, batch and concurrency?",
                "What throughput and tail-latency evidence exists for the exact framework, precision, kernels and topology?",
                "Have accelerator support, quota, regional availability and reservation assumptions been checked in current documentation and the target account?",
            ],
            "reference": "https://docs.cloud.google.com/ai-hypercomputer/docs/process-overview",
            "reference_label": "AI Hypercomputer: plan and create AI infrastructure (accessed 2026-09-29)",
            "scenario": {
                "scenario": "Supplied synthetic sizing worksheet: an interactive model is assigned a candidate with sufficient nominal weight memory, but the worksheet omits 32k-token contexts, peak concurrent sequences, KV cache, runtime workspaces and the required time-to-first-token. No candidate hardware benchmark or availability confirmation is supplied.",
                "impact": "The chosen shape may OOM under concurrent long prompts or require aggressive batching that breaches the interactive latency objective. Oversizing based only on a worst-case guess can also waste expensive reserved capacity.",
                "constraints": "Review only; do not provision an accelerator or cluster. Preserve model quality and privacy. Treat candidate specifications, memory estimate and all performance/availability claims as unverified until the exact workload and current documentation are checked.",
                "evidence": "Supplied exercise facts: model type is interactive inference; target context is 32k tokens; the illustrative worksheet includes weights only and omits KV cache, concurrency, workspace and latency measurements. Hardware benchmark, exact model configuration, quota and stock are not supplied.",
                "root": "Hypothesis: the candidate was selected from a weights-only memory estimate, which does not bound peak serving memory or latency at the stated context and concurrency. The fixture cannot prove any candidate is insufficient because critical model and hardware measurements are missing.",
                "diagnostic_steps": [
                    "Request model architecture/version, precision, layers/heads, KV-cache format, maximum prompt/output lengths, expected concurrent sequences, batch policy and runtime overhead measurements.",
                    "Define required TTFT, inter-token latency, throughput, quality parity and OOM/error objectives; calculate a transparent lower-bound memory envelope and label unknown terms.",
                    "Check current supported machine type, accelerator topology, framework/kernel support, quota, region/zone availability and reservation path for the intended project and date.",
                ],
                "remediation_steps": [
                    "Replace the weights-only worksheet with a model-and-serving envelope containing weights, KV cache by context/concurrency, workspaces, runtime and operational reserve; do not invent missing quantities.",
                    "Compare candidates under identical model version, precision, request distribution and quality assertions using a representative bounded benchmark before selecting capacity.",
                    "Document a conditional choice and fallback (smaller context, bounded concurrency/batching, alternative supported shape or graceful rejection) with explicit latency and quality trade-offs.",
                ],
                "verify": "Acceptance requires a measured peak-memory and throughput/latency result from an approved representative benchmark, quality parity, error/OOM check and current availability confirmation. Until then mark candidate results projected/unverified and do not claim a cluster was tested.",
                "residual": "Weights, cache behavior, request skew, runtime kernels, topology, quota, stock and reservation dates can change. Paper calculations support shortlist and questions, not a deployment guarantee.",
                "diagram": ["Candidate chosen from nominal model-weight fit", "Long-context cache and concurrency omitted from memory envelope", "OOM risk or batching harms interactive latency; oversized fallback wastes capacity", "Add memory terms and verify exact model/software on representative workload", "Choose conditionally after quality, latency, quota and availability gates pass"],
                "facts": "The omitted variables and 32k context are supplied synthetic worksheet facts; no real benchmark, quota check or availability check occurred.",
                "inference": "Peak serving memory or latency may exceed the paper estimate; the case does not establish that a named accelerator fails.",
                "expected": "A sizing decision sheet shows formulas/unknowns, candidate comparison, current-documentation checks required, benchmark acceptance gates and no-provisioning limit.",
            },
            "lab": lab(
                "GPU/TPU serving fit review without provisioning",
                "Turn an incomplete weights-only example into a transparent accelerator sizing decision record, identify missing memory and performance terms, and specify the benchmark and availability checks that would close the evidence gap.",
                "A local sizing worksheet distinguishes known inputs, formulas, unknowns and projections; compares at least two conditional options without naming an unverified winner.",
                "Day 124 bottleneck evidence and Day 97 workload/SLO assumptions; no cloud account needed.",
                "Use only the supplied synthetic worksheet description. Confirm the exercise is offline/tabletop, note date for current product checks, and do not enter credentials or create a project, VM, accelerator or cluster. Have an editor or spreadsheet available.",
                [
                    ("Preflight workload and decision boundary", "Create `day-125-topic-03.md`. Record interactive inference, supplied 32k context, quality objective still to be specified, latency metric still to be specified, no-provisioning mode, and which statements are unknown. State that current accelerator specs and stock are not verified in the fixture."),
                    ("Prepare the model and request inputs", "Build a worksheet with rows for weights, KV cache, activations/workspace, runtime overhead, operating reserve, sequence length, output length, concurrent sequences, batch policy and precision. Mark weights-only as supplied; mark all omitted terms unknown instead of fabricating numeric values."),
                    ("Author sizing formulas and candidate plan", "Write a formula outline for total peak memory as the sum of model weights, cache, workspace/activations, runtime and chosen operational allowance; identify the inputs each term requires. Create two generic candidate columns and include memory, throughput, TTFT, inter-token latency, quality, topology/software support, quota and availability."),
                    ("Execute the tabletop comparison", "For each candidate, fill only the evidence available and label all other cells `unknown / verify`. Record how long context and concurrency affect cache, how batching affects throughput and interactive latency, and why no device can yet be selected from the fixture. Do not substitute current machine claims from memory."),
                    ("Inspect expected state and verification gates", "Check weights are not treated as total peak memory; include model quality and latency objectives; separate measured from projected values; and add gates for exact framework/kernel support, representative benchmark, quota, region/zone, reservation lead time and fallback behavior."),
                    ("Challenge a bounded edge case", "Run a sensitivity review with concurrent sequences doubled and then with context capped. Do not insert guessed memory numbers; instead identify which worksheet terms and latency trade-offs would change, and what product/model measurements are needed before recalculating."),
                    ("Diagnose and record the conditional decision", "Write the shortlist condition, reject/hold rationale, missing evidence owner, benchmark protocol, OOM/latency/quality thresholds and availability confirmation step. Explicitly state that this paper exercise does not establish actual device capacity or stock."),
                    ("Close out the review artifact", "Save the worksheet and Markdown decision record; link it into the combined Day 125 recommendation; label the exercise tabletop and record that zero resources were provisioned. Retain the assumptions and open questions for a later approved benchmark."),
                ],
                "Check every estimate has an input/source and units; unknown memory terms remain unknown; candidate choice is conditional; throughput/latency/quality gates and current availability checks are recorded; no cloud resources were created.",
                "Accept `day-125-topic-03-accelerator-sizing.md` and its worksheet with workload classification, memory term ledger, two conditional candidate columns, sensitivity cases, benchmark acceptance criteria, quota/availability check owner and explicit no-provisioning statement.",
                "If weights dominate the worksheet, revisit context, active sequence count, cache representation and workspace. If candidates lack common benchmark data, mark the comparison inconclusive. If availability cannot be confirmed from an authorized account, record that as a blocking assumption, not a negative quota result.",
                "No accelerator or cluster is provisioned, so no cost cleanup is needed. Keep the design artifacts; do not treat speculative values as reservations or share sensitive model/customer inputs.",
                "day-125-topic-03-accelerator-sizing.md",
            ),
        },
    ],
}
