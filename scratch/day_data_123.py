"""Day 123 specification: cache correctness, load behavior, and measured diagnosis."""

DAY_NUM = 123


def stages(items):
    return [f"#### Stage {i}: {title}\n\n{detail}" for i, (title, detail) in enumerate(items, 1)]


DATA = {
    "day": 123,
    "part1_intro": (
        "Caching can shorten a request path only when the saved work is real, the cached value is safe to reuse, and the cache "
        "continues to behave under skewed demand. Begin with a baseline that separates application CPU, memory pressure, backing-store "
        "I/O, network time, and cache behavior. Then compare cache-aside and write-through, define freshness and invalidation ownership, "
        "and test a hot-key expiry without turning a miss into a stampede. CDN, application memory, Memorystore, and BigQuery BI Engine "
        "solve different access patterns; none is a general-purpose replacement for a slow or incorrect backing system. All Brightloaf "
        "examples and lab values are synthetic."
    ),
    "exit_summary": (
        "A repeatable local hit/miss and hot-key expiry result; a cache-aside versus write-through comparison; a freshness and "
        "invalidation ADR with owner, TTL rationale, stampede control, load evidence, and residual risk; and a diagnosis separating "
        "measured facts from predictions."
    ),
    "part2_intro": (
        "Follow one request from client or edge through the application cache to its authoritative source. The table and diagram show "
        "decision boundaries and evidence to collect; they do not claim a particular workload will benefit from caching."
    ),
    "arch_table_html": """<div class="table-container"><table><thead><tr><th>Layer or choice</th><th>Mechanism and owner</th><th>Useful evidence</th><th>Limit or trade-off</th></tr></thead><tbody>
<tr><td>Baseline diagnosis</td><td>Service owner traces p50/p95/p99, request rate, errors, CPU, memory/GC, network and backing-store latency before changing design.</td><td>Same request mix and concurrency; cache disabled or bypassed in a controlled local comparison; record source reads and result correctness.</td><td>Low cache hit ratio alone does not prove a cache is needed; high hit ratio can still hide stale or unrepresentative traffic.</td></tr>
<tr><td>Cache-aside</td><td>Application checks cache; on miss it reads source and populates cache. Application owns key, TTL, negative-cache policy and invalidation.</td><td>Hit/miss, source-read rate, load latency, stale age, eviction and miss concurrency.</td><td>Simple and source remains authoritative, but concurrent misses can duplicate work and invalidation can lag.</td></tr>
<tr><td>Write-through</td><td>Write path updates source and cache under an explicitly designed ordering/error policy; service owner owns consistency contract.</td><td>Write success and partial-failure handling; read-after-write behavior; source/cache version or generation.</td><td>Can reduce post-write stale reads, but adds write-path coupling/latency and does not by itself make two systems atomic.</td></tr>
<tr><td>Choose a cache boundary</td><td>CDN for cacheable HTTP responses at edge; process memory for instance-local reuse; Memorystore for shared low-latency key/value state; BI Engine for eligible BigQuery analytics.</td><td>Cacheability headers/key variation; origin requests; per-instance warm state; Redis hit/memory/eviction metrics; BI Engine acceleration evidence.</td><td>Different ownership, freshness and failure modes. CDN must not expose personalized data; process caches fragment across instances; managed caches have capacity and network boundaries; BI Engine is query-specific.</td></tr>
<tr><td>Freshness and load control</td><td>Set TTL from business tolerance; invalidate on authoritative change where practical; jitter expiries, coalesce misses, or serve bounded stale data only when policy allows.</td><td>Observed stale-age distribution, expiry burst, source QPS, queueing and correctness checks through the full expiry window.</td><td>Long TTL lowers source load but widens staleness; short TTL improves freshness but can raise origin load. Stale-on-error is a product decision.</td></tr>
</tbody></table></div>""",
    "arch_diagram": {
        "type": "topology",
        "title": "Day 123 request path, cache freshness and diagnosis boundaries",
        "desc": "A request flows from a client through an optional CDN to an application that checks a local or shared cache before the authoritative source; metrics and correctness checks govern policy and invalidation decisions.",
        "caption": "Figure 123.1: Conceptual cache decision path and evidence boundary. It does not establish workload cacheability, production hit rate, freshness, or performance improvement.",
        "width": 1120, "height": 620,
        "layers": [
            {"name": "REQUEST AND EDGE: CACHE ONLY RESPONSES SAFE TO SHARE", "x": 20, "y": 35, "w": 1080, "h": 95, "fill": "#1e3a5f", "title_color": "#7dd3fc", "desc": "HTTP cache keys · headers · identity scope"},
            {"name": "APPLICATION POLICY: KEY · TTL · INVALIDATION · COALESCING", "x": 20, "y": 170, "w": 1080, "h": 115, "fill": "#064e3b", "title_color": "#6ee7b7", "desc": "cache-aside or explicit write-through policy"},
            {"name": "AUTHORITATIVE DATA AND OBSERVABILITY", "x": 20, "y": 330, "w": 1080, "h": 100, "fill": "#422006", "title_color": "#fdba74", "desc": "source remains authority; cache may be unavailable"},
            {"name": "DECISION AND ACCEPTANCE BOUNDARY", "x": 20, "y": 470, "w": 1080, "h": 105, "fill": "#3f1d2e", "title_color": "#fda4af", "desc": "compare equal traffic and validate freshness"},
        ],
        "components": [
            {"x": 55, "y": 65, "w": 200, "h": 48, "name": "Client", "detail": "request + identity", "stroke": "#38bdf8"},
            {"x": 340, "y": 65, "w": 240, "h": 48, "name": "Optional CDN", "detail": "shareable HTTP response", "stroke": "#38bdf8"},
            {"x": 690, "y": 65, "w": 300, "h": 48, "name": "HTTP key / cache policy", "detail": "vary · directives · freshness", "stroke": "#38bdf8"},
            {"x": 95, "y": 205, "w": 240, "h": 54, "name": "Application", "detail": "check key · validate scope", "stroke": "#22c55e"},
            {"x": 440, "y": 205, "w": 245, "h": 54, "name": "Cache", "detail": "local or shared · TTL", "stroke": "#22c55e"},
            {"x": 790, "y": 205, "w": 245, "h": 54, "name": "Miss control", "detail": "jitter · coalesce · bound", "stroke": "#22c55e"},
            {"x": 190, "y": 365, "w": 290, "h": 52, "name": "Authoritative source", "detail": "database / service / warehouse", "stroke": "#f59e0b"},
            {"x": 650, "y": 365, "w": 320, "h": 52, "name": "Signals + correctness", "detail": "latency · reads · stale age · errors", "stroke": "#f59e0b"},
            {"x": 165, "y": 500, "w": 300, "h": 52, "name": "ADR decision", "detail": "tolerance · owner · rollback", "stroke": "#f43f5e"},
            {"x": 650, "y": 500, "w": 320, "h": 52, "name": "Acceptance evidence", "detail": "same load · correct response · bounded risk", "stroke": "#f43f5e"},
        ],
        "flows": [
            {"x1": 255, "y1": 89, "x2": 340, "y2": 89, "label": "HTTP request", "type": "ok"},
            {"x1": 580, "y1": 89, "x2": 690, "y2": 89, "label": "cache policy", "type": "ok"},
            {"x1": 460, "y1": 113, "x2": 215, "y2": 205, "label": "forward miss", "type": "ok"},
            {"x1": 335, "y1": 232, "x2": 440, "y2": 232, "label": "lookup / fill", "type": "ok"},
            {"x1": 685, "y1": 232, "x2": 790, "y2": 232, "label": "miss burst", "type": "warn"},
            {"x1": 560, "y1": 259, "x2": 330, "y2": 365, "label": "authoritative read/write", "type": "ok"},
            {"x1": 480, "y1": 391, "x2": 650, "y2": 391, "label": "measure + reconcile", "type": "ok"},
            {"x1": 805, "y1": 417, "x2": 465, "y2": 500, "label": "review evidence", "type": "warn"},
            {"x1": 465, "y1": 526, "x2": 650, "y2": 526, "label": "approve / revise", "type": "ok"},
        ],
        "boundaries": [
            {"x": 34, "y": 455, "w": 1050, "h": 135, "label": "VERIFY BOUNDARY · FASTER RESPONSE DOES NOT PROVE FRESHNESS OR CORRECTNESS"},
        ],
        "probes": [
            {"cx": 100, "cy": 170, "label": "P1: Identity and cache-key scope must match", "color": "#38bdf8"},
            {"cx": 1050, "cy": 315, "label": "P2: Observe miss burst, memory, eviction and source load", "color": "#22c55e"},
            {"cx": 565, "cy": 455, "label": "P3: Check stale age and business tolerance", "color": "#f59e0b"},
        ],
    },
    "part3_intro": "The following are synthetic Brightloaf cases for causal analysis, not claims of observed production incidents. Each separates supplied signals from architectural inference and specifies the evidence needed to confirm or reject the proposed cause.",
    "part4_intro": "Use local Python standard-library exercises and a tabletop ADR. Do not provision Memorystore, CDN, BI Engine, databases, or paid load generators. Synthetic timings and request counts are teaching inputs; label outputs from a local run as local observations and unexecuted production behavior as predictions.",
    "topics": [
        {
            "key": "topic-01",
            "title": "Caching behavior: hit ratio, freshness and hot-key load",
            "overview": (
                "A cache stores reusable results closer to a reader to avoid repeating work at an authoritative source. Cache-aside makes "
                "the application check, fill, and expire entries; write-through couples cache updates to a write path but does not make "
                "the source and cache one atomic transaction. TTL bounds age only if its clock and semantics are understood; invalidation "
                "must define who acts after source changes. Hot keys concentrate demand, while an expiry or cold start can send many "
                "simultaneous misses to the source. Day 123 puts these mechanics under load and relates them to stale-data tolerance. "
                "CDN, application cache, Memorystore and BI Engine are selected for different data and request boundaries."
            ),
            "preview": "Brightloaf's popular product key expires during a demand burst and every worker reads the database at once. The database queues checkout reads, raising customer latency and threatening order completion.",
            "technical": """## Cache-aside and write-through are consistency choices

In cache-aside, a reader checks the cache, reads the source on a miss, then populates the cache. The source remains authoritative, but two callers can miss together and duplicate the source read. A writer normally commits to the source and then invalidates or refreshes the cache. If the process fails between these operations, stale data can remain; use a version, outbox, or retryable invalidation design when the business invariant requires stronger repair behavior. Negative caching can protect a source from repeated not-found lookups, but its TTL must not delay visibility of a newly created record.

Write-through describes a write path that updates the cache as part of handling a source write. It can make subsequent reads fresher when ordering and failure recovery are designed, but the systems do not become transactionally atomic by naming the pattern. Decide what happens when the source commit succeeds and the cache update fails, or vice versa. For correctness-sensitive records such as price, inventory reservation, or order state, read the authoritative version or use a transactionally safe design; a cache should not invent authority.

## TTL, invalidation and stale-data tolerance

Choose freshness from a business rule, not a convenient round number. State maximum acceptable age, whether stale reads are allowed during source failure, and the behavior after deletion or permission change. TTL is a backstop, not proof that data is fresh: time-to-live begins at a particular write/fill event, and a value can become stale before expiry. Invalidation can reduce that window but introduces a delivery path that must be observed, retried, and reconciled. Add jitter to similar expirations so a batch of keys does not all expire together.

## Load, hot keys and stampedes

A hot key has a disproportionate share of requests. Measure per-key skew carefully without logging sensitive key values. On expiry, cold start, eviction, or cache outage, cache-aside readers can stampede the source. Candidate controls include per-key request coalescing (single-flight), bounded concurrency, short randomized backoff, prewarming, or serving a bounded stale value where the product explicitly permits it. Each changes a different part of the failure mode. A process-local lock only coordinates one instance; a shared lock adds its own availability and timeout problem. Do not use an unbounded stale response for authorization, inventory, or other correctness-sensitive values.

## Compare boundaries, not product names

An HTTP CDN cache can offload globally repeated cacheable responses when headers, key variation, identity, and invalidation are safe. An in-process cache avoids a network hop but fragments across instances and disappears on restart. Memorystore provides a shared managed Redis endpoint, while the application still owns key design, TTL, source-of-truth behavior, memory sizing, eviction response, and fallback. BI Engine accelerates eligible BigQuery analytics with reserved in-memory capacity; it is not an application key/value cache. Diagnose CPU, allocation/GC, network, disk and database waits first. A lower response time at one layer is not proof of lower end-to-end p95 or a safe freshness contract.""",
            "questions": [
                "Which business values can be stale, and what is their maximum tolerated age?",
                "Who owns source commit, cache update/invalidation retry, and reconciliation?",
                "What happens to source QPS and database queueing on simultaneous misses or cache loss?",
                "Does the access pattern fit a CDN response, process-local value, shared key/value cache, or analytical acceleration?",
                "Which CPU, memory, network, I/O and backing-store signals establish that caching addresses the bottleneck?",
            ],
            "reference": "https://docs.cloud.google.com/memorystore/docs/redis/memory-management-best-practices",
            "reference_label": "Google Cloud Memorystore for Redis: memory management, TTL and hit-ratio guidance (accessed 2026-09-29)",
            "scenario": {
                "scenario": "Synthetic Brightloaf load replay shows a high request concentration on one product key. The key expires at the same time across workers, the local harness records concurrent source reads, and the simulated source queue grows.",
                "impact": "The cache may reduce ordinary read load while synchronized expiry temporarily increases database work and p95 latency. Customer impact is a predicted checkout delay; no production incident is asserted.",
                "constraints": "Inventory and price have explicit freshness needs; stale inventory must not authorize overselling. The source database remains authoritative. The exercise has no production telemetry or cloud cache.",
                "evidence": "Supplied synthetic facts: one hot key, synchronized expiry, concurrent miss readers, increased simulated source queue. Confirming evidence would include time-aligned cache hit/miss and expiry counts, per-key skew with safe aggregation, source QPS/queue depth, p95/p99 latency, and correctness comparisons against source versions.",
                "root": "Architectural inference: synchronized expiration plus uncoordinated cache-aside misses can explain a burst of duplicate source reads. A local model can demonstrate the mechanism, but it cannot prove the production cause or quantify cloud behavior.",
                "diagnostic_steps": [
                    "Align load-generator, application, cache and database clocks; split warm hits, cold misses, expiry misses, evictions and cache errors.",
                    "Compare request rate and distinct keys with source reads. A high overall hit ratio can conceal one overloaded hot key.",
                    "Inspect cache memory, TTL distribution and eviction signals alongside source CPU, connection queue and read latency; check CPU/GC and network wait before blaming storage.",
                    "Compare returned value version and age to the authoritative record. Trace invalidation completion and failure/retry counts.",
                    "Run a bounded local replay with an identical key distribution and concurrency for baseline, jitter, and per-key coalescing; separate measured local timings from predicted production outcomes.",
                ],
                "remediation_steps": [
                    "Set TTL from the named freshness requirement and add randomized jitter; do not apply a generic stale-serving policy to inventory or authorization data.",
                    "Coalesce same-key misses or otherwise bound source concurrency, with timeout and fallback behavior. Ensure coordination scope matches the number of application instances.",
                    "Make source writes authoritative and invalidation retryable/observable; include a version or reconciliation path for partial failure.",
                    "Adopt the least complex suitable cache boundary, then rerun the same workload and verify source load, tail latency, freshness, error rate, and business correctness together.",
                ],
                "verify": "For the local harness, compare backing reads per request and maximum simultaneous reads across identical workloads; prove the chosen mitigation lowers duplicate reads and assert the returned source version satisfies the stated freshness rule. Production improvement remains unverified until matched telemetry and correctness checks exist.",
                "residual": "Jitter and coalescing reduce a burst but do not repair bad keys, unbounded working sets, source slowness, cache outages, or invalidation loss. A hot-key mitigation can shift load and needs representative skew and multi-instance tests.",
                "facts": "Synthetic case facts are one hot key, synchronized expiry, simultaneous misses and a simulated source queue increase; these are supplied for analysis only.",
                "inference": "Expiry-driven duplicate reads are a plausible mechanism. Production causality and impact require matched cache, application, database and correctness telemetry.",
                "expected": "The same synthetic input is replayed with and without a named mitigation; measured local source-read and concurrency deltas plus freshness assertions are recorded.",
                "diagram": ("Hot key expires during burst", "Workers miss without coalescing", "Source reads and queue rise", "Jitter TTL and bound same-key misses", "Check source load and freshness invariant"),
            },
            "lab": {
                "name": "Measure cache hit/miss behavior and contain a hot-key stampede",
                "goal": "Use a deterministic, local-only model to compare cache-aside and write-through behavior, expire a hot key, test one stampede mitigation, and record freshness trade-offs.",
                "expected": "A repeatable local run log with request/hit/miss/source-read counts, hot-key concurrency comparison, cache-aside versus write-through table, and a freshness/invalidation decision.",
                "mode": "offline Python 3 standard library; synthetic deterministic simulation only",
                "prereq": "Day 122 workload/unit-cost worksheet; Day 63 cache invalidation notes; local Python 3 and text editor",
                "preflight": "Use a disposable local directory, confirm `python3 --version`, and mark every generated value synthetic. Fix the key distribution, request count, concurrency, clock/timing assumptions, and source-read counter before each run. Do not use cloud credentials or create resources.",
                "trouble": "If the run is nondeterministic, use the fixed seed and same worker count; if hit ratio improves while stale assertions fail, correctness is a failing result; if your lock is process-local, state that it does not coordinate multiple service instances.",
                "cleanup": "No cloud resources are created. Keep the final worksheet, script and run output as exit evidence; remove disposable copies and verify no credentials or customer data entered the directory.",
                "file": "day-123-cache-correctness-lab.md",
                "steps": stages([
                    ("Preflight the workload and freshness contract", "Create `day-123-cache-correctness-lab.md`. Record Python version, synthetic-data notice, one request window, concurrency, key distribution (including hot-key share), authoritative source, maximum tolerated age for product and inventory, and the correctness check. State explicitly that production telemetry and cloud resources are out of scope."),
                    ("Prepare deterministic source and request fixtures", "Create `cache_stampede.py` in the disposable directory using this standard-library-only harness. It synchronizes cold misses so the unmitigated run reliably demonstrates duplicate source reads, then repeats with per-key coalescing.\n\n```python\nfrom concurrent.futures import ThreadPoolExecutor\nfrom threading import Barrier, Lock\nfrom time import sleep\n\nWORKERS = 12\nsource_reads = 0\nactive_reads = 0\nmax_active_reads = 0\ncounts_lock = Lock()\n\ndef source_read():\n    global source_reads, active_reads, max_active_reads\n    with counts_lock:\n        source_reads += 1\n        active_reads += 1\n        max_active_reads = max(max_active_reads, active_reads)\n    sleep(0.01)  # synthetic source latency; not a cloud measurement\n    with counts_lock:\n        active_reads -= 1\n    return {\"sku-42\": {\"version\": 7, \"value\": \"in-stock\"}}[\"sku-42\"]\n\ndef run(mode):\n    global source_reads, active_reads, max_active_reads\n    source_reads = active_reads = max_active_reads = 0\n    cache = {}\n    start = Barrier(WORKERS)\n    all_missed = Barrier(WORKERS) if mode == \"uncoordinated\" else None\n    key_lock = Lock()\n\n    def request():\n        start.wait()  # align the synthetic burst\n        value = cache.get(\"sku-42\")\n        if value is not None:\n            return value\n        if all_missed is not None:\n            all_missed.wait()  # hold every caller at the same cold miss\n            value = source_read()\n            cache[\"sku-42\"] = value\n            return value\n        with key_lock:  # single-process single-flight demonstration\n            value = cache.get(\"sku-42\")  # second check after waiting\n            if value is None:\n                value = source_read()\n                cache[\"sku-42\"] = value\n            return value\n\n    with ThreadPoolExecutor(max_workers=WORKERS) as pool:\n        results = list(pool.map(lambda _: request(), range(WORKERS)))\n    assert len(results) == WORKERS\n    assert all(result[\"version\"] == 7 for result in results)\n    print(f\"{mode}: requests={len(results)}, source_reads={source_reads}, max_parallel_source_reads={max_active_reads}, version=7\")\n    return source_reads, max_active_reads\n\nif __name__ == \"__main__\":\n    uncoordinated = run(\"uncoordinated\")\n    coalesced = run(\"coalesced\")\n    assert uncoordinated[0] == WORKERS\n    assert coalesced[0] == 1\n    print(\"PASS: coalescing reduced this synthetic cold-key burst to one source read.\")\n```\n\nThe harness deliberately makes all uncoordinated requests miss together; it demonstrates a mechanism, not a realistic cache hit ratio or production throughput. Keep the same `WORKERS`, source delay, key, and source version across both runs."),
                    ("Author the cache policy and comparison plan", "Write two policy descriptions before coding: cache-aside (miss reads source then fills) and write-through (source write with defined cache update ordering and partial-failure response). Specify TTL, jitter range, invalidation owner, stale-read rule, cache-error fallback, and which metrics decide the comparison. Do not describe the policies as atomic."),
                    ("Execute warm, miss and expiry scenarios", "Run the cold hot-key burst and coalesced repeat from the local file. The harness prints deterministic request/source-read counts; its wall-clock timings are intentionally not used as latency results. Then extend the worksheet with a warm-cache pass (all callers reuse version 7), an expiry event (remove the key), and a source update to version 8. Record hit/miss counts and returned versions for each pass; distinguish the script's direct observation from these additional worksheet predictions.\n\n```sh\npython3 cache_stampede.py\n```"),
                    ("Inspect expected state and correctness", "Check that a warm hit returns the cached version, a miss returns and fills from the authoritative source, and an expiry forces refresh. Compare observed local source reads and p50/p95/p99 against the cold baseline. Assert product and inventory values obey their separately stated freshness rules; mark each result as local observation."),
                    ("Rehearse one bounded stampede mitigation", "Replay only the hot-key expiry with randomized TTL jitter and a per-key single-flight/coalescing control. Keep the worker count and request distribution fixed. Measure simultaneous source reads and source queue proxy before and after. Record that a process-local lock proves only single-process behavior; predict, but do not claim, its multi-instance behavior."),
                    ("Diagnose the evidence and draft the invalidation ADR", "Use the results to decide whether the dominant issue is misses, hot-key skew, source I/O, CPU/GC, memory eviction, network, or an invalidation gap. Draft the ADR with context, chosen policy, TTL and stale tolerance, invalidation owner/retry, stampede guard, rejected alternative, measured evidence, predicted behavior, rollout guardrail, rollback trigger and residual risk. Do not infer production benefit from simulator timings."),
                    ("Close the exercise and preserve evidence", "Rerun the fixed input once to confirm the artifact reproduces the same counts; verify the eight stages are complete, results distinguish local observations from predictions, and no unsafe stale inventory rule was accepted. Save the script, input fixture, run log, comparison and ADR in the artifact. Remove only disposable generated files; no cloud cleanup is needed."),
                ]),
                "verification": "Acceptance requires the same request/key mix in baseline and mitigated run; explicit hit, miss, source-read and same-key concurrency counters; a passing freshness assertion; a cache-aside/write-through comparison; and a decision record that separates local observation from production prediction.",
                "accept": "Artifact `day-123-cache-correctness-lab.md` includes latency/load results, the cache-aside versus write-through comparison, and an invalidation ADR with freshness owner and residual risk.",
            },
        },
        {
            "key": "topic-02",
            "title": "Diagnose cache value with CPU, memory and I/O evidence",
            "overview": (
                "Assisted diagnostics returns on Day 168, but this day establishes the evidence a diagnostic must use: a defined request "
                "population, baseline latency and throughput, resource saturation, cache behavior, and source-system work. A cache is one "
                "candidate explanation among CPU computation, garbage collection, memory pressure, network delay, database queueing, and "
                "disk or query I/O. Product dashboards can accelerate a suitable class of requests—for example, CDN for cacheable HTTP "
                "responses or BI Engine for eligible BigQuery analytics—but their own hit/acceleration signals and cost boundaries differ. "
                "This topic connects today's measured cache experiment to the broader diagnostics review later in the roadmap."
            ),
            "preview": "A dashboard shows lower application latency after a cache is enabled, while database wait and end-to-end p95 remain unchanged. The team may fund the wrong layer and leave the customer's slow path unresolved.",
            "technical": """## Diagnose before selecting a cache

Hold request mix, concurrency, payload size, region, data freshness, and observation window constant. Record throughput, errors and latency percentiles with spans across client, edge, application, cache and backing store. Compare cache hit/miss and source-read counts with CPU utilization/queue, memory/GC or eviction, network wait, database connection/queue, and disk/query I/O. Percentiles and time alignment matter: aggregate average CPU can hide one saturated worker, and a cache hit ratio can hide a few very expensive misses.

A useful hypothesis predicts a measurable change. If a repeated read dominates database service time, a safe cache should reduce source reads for the same workload while maintaining correctness. If latency is dominated by serialization CPU, cache insertion may add memory and CPU cost without helping. If the database is waiting on disk, a cached subset could help only if those reads are reused; changing the storage tier is a separate intervention. Change one variable at a time, retain a rollback path, and compare end-to-end as well as component latency.

## Choose the product boundary that matches the access pattern

Cloud CDN caches HTTP responses according to cacheability, response directives, configured behavior and cache key. Verify whether responses can be shared across callers, whether headers vary by identity or content negotiation, and how invalidation works. Application memory keeps values near a process but is not shared and starts cold on replacement. Memorystore is a managed shared data structure service; monitor memory, hit ratio, evictions, write behavior, and network path. BigQuery BI Engine reserves in-memory capacity to accelerate eligible analytical query stages; unsupported or unaccelerated stages can use regular BigQuery execution. None of these mechanisms changes the underlying workload contract.

## Evidence limits and assisted diagnosis

Document signal provenance: local measurement, supplied metric sample, documentation, or tabletop prediction. A diagnostic assistant can summarize signals or suggest a hypothesis, but it cannot turn incomplete telemetry into proof. Preserve query/request identifiers carefully, avoid exposing secrets or personal data, and independently check its suggestion against source metrics and business correctness. Day 168 returns to assisted diagnostics; today produce a clean baseline and an explicit evidence gap list that a future tool or operator can inspect.""",
            "questions": [
                "Which span or wait dominates end-to-end tail latency, and what source metric supports that?",
                "Did request mix, concurrency, freshness, payload and region remain constant between measurements?",
                "Are CPU, memory/GC, network, database queue and I/O signals synchronized with the cache observation?",
                "Does a CDN response have a safe shared cache key, or does identity/content variation prevent reuse?",
                "For BI Engine, are the tested queries and reservations eligible, and is accelerated execution actually observed?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/performance-optimization",
            "reference_label": "Google Cloud Well-Architected Framework: Performance optimization process and monitoring (accessed 2026-09-29)",
            "scenario": {
                "scenario": "Synthetic Brightloaf dashboard evidence shows application p50 falls after enabling a cache, but end-to-end p95 is flat and the source still reports high I/O wait. The measurements were collected over different request mixes.",
                "impact": "The apparent local improvement could be a workload-composition effect, while customers still experience a slow tail. Scaling the cache without isolating the dominant wait may add cost and operational load without meeting the service objective.",
                "constraints": "Only a synthetic summary is supplied; there are no raw traces, synchronized clocks, or matched load tests. Do not claim causal production findings or a specific savings percentage.",
                "evidence": "Supplied synthetic facts: p50 fell, end-to-end p95 stayed flat, I/O wait remained high, and request mixes differ. Needed evidence: matched replay; trace spans; cache hit/miss and source reads; CPU, memory/GC, network and storage/database waits; error rate; and correctness/freshness checks.",
                "root": "Architectural inference: the before/after comparison is confounded by request mix, and the unchanged tail plus continued I/O wait means cache benefit is unproven. Establishing the dominant bottleneck requires matched, time-aligned evidence.",
                "diagnostic_steps": [
                    "Reject the unmatched p50 comparison as causal evidence. Write down which request, payload, concurrency and cache-state populations differ.",
                    "Build a request-level timeline from client through edge, app, cache, database/query and storage; identify queueing and span gaps for p95/p99 requests.",
                    "Align resource signals over the same interval: CPU and run queue, memory/GC, cache hit/miss/evictions, source reads, connections, network wait and database/disk I/O.",
                    "Check response correctness and age against authoritative source versions; split cacheable and personalized traffic and check key variation.",
                    "Repeat a bounded matched local workload with cache bypassed and enabled; label measurements, supplied facts, and remaining production unknowns distinctly.",
                ],
                "remediation_steps": [
                    "Collect a same-workload baseline with trace sampling and synchronized timestamps before selecting an optimization.",
                    "If repeated source reads dominate and freshness permits, run one bounded cache policy trial; if storage or query I/O dominates, profile that path and consider its specific remediation instead.",
                    "For a CDN candidate, verify response cache directives, identity safety, key variation and invalidation. For BI Engine, verify query eligibility and acceleration evidence. For Memorystore, include hit/memory/eviction and network signals.",
                    "Keep rollback criteria tied to p95/p99, errors, source saturation, stale-age and cost; verify over an equivalent window and traffic mix.",
                ],
                "verify": "The local comparison uses identical generated requests, concurrency, key distribution, cache warm state definition and freshness assertions; it records end-to-end and component percentiles plus resource/source counters. Any production claim remains pending matched production telemetry.",
                "residual": "Local simulation omits real network, database storage, runtime scheduling and managed-service behavior. Sampling, clock skew, workload drift and low-frequency key popularity can still conceal the actual production bottleneck.",
                "facts": "Synthetic input reports lower application p50, unchanged end-to-end p95, high I/O wait and unmatched request mixes.",
                "inference": "The comparison is confounded and caching has not been shown to resolve the tail. A matched experiment and trace-level evidence are required.",
                "expected": "A workload-matched baseline and evidence map distinguish the dominant measured wait from unverified hypotheses before any product decision.",
                "diagram": ("Cache enabled; workload differs", "Only app p50 compared", "End-to-end tail and I/O persist", "Match traffic; correlate spans and signals", "Accept only a measured, correct improvement"),
            },
            "lab": {
                "name": "Build a matched bottleneck evidence sheet and select a cache boundary",
                "goal": "Separate measured observations from causal claims, compare candidate cache boundaries, and write a bounded decision using a fixed synthetic workload.",
                "expected": "An evidence matrix, same-load comparison, selection/rejection rationale for CDN, process cache, Memorystore and BI Engine where relevant, and a short invalidation/diagnostic ADR addendum.",
                "mode": "offline analysis and tabletop design; no Google Cloud calls or provisioning",
                "prereq": "Day 94 CPU, memory and I/O evidence; Day 122 workload assumptions; Day 123 topic 1 local run log if available",
                "preflight": "Open the Day 94 evidence and topic 1 output. If unavailable, use the supplied synthetic sample in this exercise and label it as a fixture. Create a fresh worksheet; state the user objective, latency objective, freshness boundary, matching window and no-cloud/no-credential constraint.",
                "trouble": "Do not use a p50 change to claim p95 improvement. If an observation lacks time window, workload, source, or unit, classify it as unusable until clarified. Do not assume CDN or BI Engine behavior from product names alone.",
                "cleanup": "No resources, reservations, projects, or service APIs are touched. Retain the evidence sheet and ADR with the Day 123 artifact; discard only scratch copies.",
                "file": "day-123-cache-correctness-lab.md",
                "steps": stages([
                    ("Preflight the evidence sources and boundaries", "Create a section named `diagnosis`. Identify which inputs are Day 94 measurements, topic 1 local observations, supplied synthetic facts, documentation, or predictions. Fix the target request population, region assumption, concurrency, time window, freshness constraint, and end-to-end objective before comparing values."),
                    ("Prepare the baseline signal inventory", "Create rows for throughput, error rate, p50/p95/p99, cache hits/misses/evictions, source reads/queue, CPU/run queue, memory/GC, network wait, database wait, and disk/query I/O. For each add unit, timestamp/window, owner, provenance, and missing-data marker. Use the supplied p50-down/p95-flat/high-I/O sample only as synthetic input."),
                    ("Author competing bottleneck hypotheses", "Write at least three testable explanations: reusable source reads dominate; storage/database I/O dominates; or workload mix/CPU/GC/network explains the apparent latency change. For each, predict which span or counter changes under a controlled cache comparison and name one observation that would disprove it."),
                    ("Execute the matched comparison on paper or local data", "If topic 1's deterministic run is available, copy its cache-off/on results and confirm request mix, key distribution, worker count and freshness checks match. Otherwise perform a tabletop comparison using the synthetic sample, marking every cell `prediction`. Do not invent percentiles or claim a measured production improvement."),
                    ("Inspect end-to-end state and choose candidate fit", "Map the dominant observed or unknown step to the user journey. For CDN assess shareable HTTP response and key safety; for process memory assess instance-local reuse; for Memorystore assess shared key/value needs, memory/eviction and network; for BI Engine assess BigQuery analytical queries and acceleration evidence. Record which candidates do not fit and why."),
                    ("Rehearse a bounded confounder or failure", "Challenge the decision with one changed condition: personalized response, stale inventory, cold cache after restart, eviction/memory pressure, unsupported BI query, or I/O-bound source. Predict the first signal to change, user effect, safe fallback, and which freshness/correctness guardrail must remain true. Keep this a tabletop prediction."),
                    ("Diagnose provenance and draft the decision record", "Classify each conclusion as local observation, supplied fact, documentation, inference, or prediction. Select one next measurement or one bounded trial; specify matched inputs, owner, telemetry, stale-age/error/p95 rollback thresholds, cost boundary, and unresolved gaps. State that assisted diagnostics on Day 168 may suggest hypotheses but evidence ownership remains with the service team."),
                    ("Close out the evidence package", "Check for a matched workload definition, signal provenance, at least one falsifiable hypothesis, product-fit comparison, and a bounded verification/rollback plan. Save the evidence matrix and ADR addendum into `day-123-cache-correctness-lab.md`; note that no cloud resources were created and record any missing Day 94/topic 1 prerequisite evidence."),
                ]),
                "verification": "The artifact makes no causal claim from the unmatched p50 example, distinguishes all observation types, compares cache candidates against their workload boundary, and defines an end-to-end/freshness guardrail for any future controlled trial.",
                "accept": "Add the evidence matrix and diagnostic decision to `day-123-cache-correctness-lab.md`; together with Topic 1 it supports the roadmap latency/load result, policy comparison and invalidation ADR.",
            },
        },
    ],
}
