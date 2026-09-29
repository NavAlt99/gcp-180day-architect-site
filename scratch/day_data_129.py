"""Day 129 authoring specification: release rollback and delivery measures."""

DAY = 129
WORK_BLOCK = "Performance, delivery and operations"

PART1_INTRO = (
    "Today connects release mechanics to observable delivery performance. A safe release "
    "keeps a known-good state recoverable, detects harmful change with user-relevant signals, "
    "and routes remediation to an accountable operator. The exercises use synthetic local "
    "data: no cloud project, deployment, or production traffic is touched."
)
EXIT_SUMMARY = (
    "A rollback trace naming the candidate, failed signal, chosen known-good revision, "
    "decision timestamps, and post-rollback check; a metric sheet with service boundary, "
    "window, numerator, denominator, and values labeled simulated; and a test/identity "
    "responsibility map that distinguishes local evidence from cloud integration evidence."
)
PART2_INTRO = (
    "Release choice, test depth, identity boundaries, and delivery measurement form one "
    "control loop. The diagram shows the decision path; it does not claim that a local "
    "simulation proves Cloud Deploy behavior, cloud IAM correctness, or production safety."
)
PART3_INTRO = (
    "The two cases are explicitly synthetic planning exercises. Their numbers and event "
    "records are supplied inputs, not claims about observed Brightloaf production. Root "
    "cause statements are architectural inferences from those inputs."
)
PART4_INTRO = (
    "Run both exercises locally with Python's standard library. Each has exactly eight "
    "execution stages and produces inspectable evidence. The release exercise simulates "
    "traffic and rollback; the pipeline exercise calculates metrics and separates test "
    "responsibilities. Neither creates cloud resources or injects faults into a service."
)

ARCH_TABLE_HTML = """
<table>
<caption>Release control path, owner, signal, and proof boundary</caption>
<thead><tr><th scope="col">Path stage</th><th scope="col">Owner and control</th><th scope="col">Evidence and decision</th><th scope="col">Boundary / trade-off</th></tr></thead>
<tbody>
<tr><th scope="row">Build and test</th><td>Pipeline identity runs unit, integration, security and bounded load checks; artifact is tied to an immutable revision.</td><td>Test report, source revision, artifact digest, build identity and policy result.</td><td>Unit tests are fast and isolated; they cannot establish live dependency behavior. Build identity permissions define the blast radius of build configuration or source compromise.</td></tr>
<tr><th scope="row">Progressive exposure</th><td>Release controller or operator moves traffic in bounded steps; canary owner watches service SLI and business invariant.</td><td>Revision, traffic share, error/latency/fulfillment signals, gate result and timestamps.</td><td>Canary limits exposure only when representative traffic, adequate sample size, and an independent gate exist. A passing synthetic test is not a canary observation.</td></tr>
<tr><th scope="row">Rollback and recovery</th><td>Release controller creates a new rollout from a known-good release; service owner verifies recovery and data compatibility.</td><td>Rollback rollout ID, target revision, restored SLI, and incident timeline.</td><td>Rollback restores executable code, not necessarily mutated data or external side effects. Schema expansion, idempotency and forward-compatible changes must be planned separately.</td></tr>
<tr><th scope="row">Delivery measures</th><td>Service team defines event boundaries, window, exclusions and accountable data source.</td><td>Per-service throughput and instability measures with count, denominator and recovery duration.</td><td>Aggregated metrics can hide service-level risk; changing definitions or mixing services breaks trend comparability.</td></tr>
</tbody></table>
"""

ARCH_DIAGRAM = {
    "type": "topology",
    "title": "Day 129 release, verification, rollback and measurement path",
    "desc": "A source revision passes test and identity gates, is promoted through progressive traffic exposure, and is either verified or rolled back to a known-good release; telemetry feeds service-level delivery measures.",
    "caption": "Scope: logical release controls and evidence ownership. The path does not prove that any named cloud configuration is enabled, that a local test models production, or that rollback reverses data changes.",
    "width": 1100,
    "height": 690,
    "layers": [
        {"name": "1 · SOURCE, TEST AND BUILD IDENTITY", "desc": "revision → tests → immutable artifact", "y": 12, "h": 94, "fill": "#1e3a5f"},
        {"name": "2 · RELEASE CONTROL AND TRAFFIC", "desc": "rolling / blue-green / canary / flag", "y": 126, "h": 110, "fill": "#0c2838"},
        {"name": "3 · SERVICE AND BUSINESS SIGNALS", "desc": "health, latency, errors, fulfillment", "y": 256, "h": 110, "fill": "#064e3b"},
        {"name": "4 · INCIDENT EVIDENCE AND DELIVERY MEASURES", "desc": "one service · explicit window and denominator", "y": 386, "h": 110, "fill": "#3b0764"},
    ],
    "components": [
        {"id": "src", "name": "Commit + digest", "detail": "immutable revision identity", "x": 60, "y": 34, "w": 190, "h": 54},
        {"id": "tests", "name": "Ordered test gates", "detail": "unit / integration / security / load", "x": 310, "y": 34, "w": 250, "h": 54},
        {"id": "iam", "name": "Build identity", "detail": "only required resource permissions", "x": 635, "y": 34, "w": 250, "h": 54, "stroke": "#f59e0b"},
        {"id": "roll", "name": "Release controller", "detail": "promote bounded traffic stages", "x": 140, "y": 152, "w": 245, "h": 58},
        {"id": "canary", "name": "Candidate + stable", "detail": "known-good remains addressable", "x": 485, "y": 152, "w": 255, "h": 58, "stroke": "#22c55e"},
        {"id": "gate", "name": "Health and business gate", "detail": "error, latency, order invariant", "x": 820, "y": 152, "w": 240, "h": 58, "stroke": "#f59e0b"},
        {"id": "svc", "name": "User-facing service", "detail": "SLI + correctness signals", "x": 330, "y": 282, "w": 300, "h": 58, "stroke": "#22c55e"},
        {"id": "audit", "name": "Rollback trace", "detail": "revision, signal, time, outcome", "x": 80, "y": 412, "w": 300, "h": 58, "stroke": "#c084fc"},
        {"id": "metric", "name": "Delivery measures", "detail": "window + numerator + denominator", "x": 650, "y": 412, "w": 330, "h": 58, "stroke": "#c084fc"},
    ],
    "flows": [
        {"x1": 250, "y1": 61, "x2": 310, "y2": 61, "type": "ok", "label": "same revision"},
        {"x1": 560, "y1": 61, "x2": 635, "y2": 61, "type": "warn", "label": "authorized"},
        {"x1": 435, "y1": 88, "x2": 260, "y2": 152, "type": "ok", "label": "verified artifact"},
        {"x1": 385, "y1": 181, "x2": 485, "y2": 181, "type": "ok", "label": "stage traffic"},
        {"x1": 740, "y1": 181, "x2": 820, "y2": 181, "type": "warn", "label": "evaluate gate"},
        {"x1": 930, "y1": 210, "x2": 630, "y2": 282, "type": "ok", "label": "observe user impact"},
        {"x1": 485, "y1": 210, "x2": 480, "y2": 240, "type": "fail", "label": "bad signal: rollback"},
        {"x1": 480, "y1": 240, "x2": 650, "y2": 181, "type": "ok", "label": "known-good rollout"},
        {"x1": 480, "y1": 340, "x2": 230, "y2": 412, "type": "ok", "label": "timeline evidence"},
        {"x1": 630, "y1": 340, "x2": 800, "y2": 412, "type": "ok", "label": "classified events"},
    ],
    "boundaries": [
        {"x": 40, "y": 18, "w": 1020, "h": 82, "label": "PIPELINE TRUST BOUNDARY · IDENTITY PERMISSIONS APPLY HERE", "color": "#f59e0b"},
        {"x": 455, "y": 137, "w": 625, "h": 86, "label": "RELEASE GATE · PROMOTE ONLY WITH ACCEPTED SIGNALS", "color": "#f59e0b"},
    ],
    "probes": [
        {"cx": 560, "cy": 180, "label": "P1: Candidate error and latency gate", "color": "#f43f5e"},
        {"cx": 630, "cy": 315, "label": "P2: User-visible service invariant", "color": "#f43f5e"},
    ],
}

TOPICS = [
    {
        "key": "topic-01",
        "title": "Rolling, blue/green, canary and feature-flag release choices",
        "preview": "A canary shows a rising checkout error rate while the stable revision remains healthy. If promotion continues, affected orders and support demand rise with the exposed traffic share.",
        "overview": (
            "A release strategy controls how executable revisions become user-visible. Rolling replaces instances in batches; blue/green keeps two environments available and shifts traffic; canary exposes a bounded share or cohort before promotion; a feature flag changes behavior at runtime without replacing the artifact. These mechanisms solve different problems: deployment changes code placement, while a flag controls a code path that must already exist. Day 129 adds the operational decision: define a measurable stop condition, preserve a known-good revision, and rehearse recovery."
        ),
        "technical": """### Control flow and release boundary

The pipeline produces an artifact tied to a source revision and digest. A release controller deploys that artifact to a target, and a traffic or instance controller changes exposure. Health checks answer whether a process responds; they do not establish that checkout correctness, latency, or data invariants remain acceptable. The service owner must select signals that reflect user outcomes and establish who can stop promotion.

| Strategy | Exposure mechanism | Useful when | Main trade-off |
|---|---|---|---|
| Rolling | Replace instances in bounded batches | Capacity supports overlap and versions remain compatible | Old and new code coexist; rollback may require another rollout and enough spare capacity |
| Blue/green | Keep two environments, switch a routing boundary | Fast traffic reversal and environment isolation justify duplicate capacity | Higher temporary capacity; state/schema changes can outlive the old environment |
| Canary | Route a small cohort/share, evaluate, then advance | A signal can be measured on representative traffic before broad exposure | Small samples can miss rare failures; routing and analysis gates must be real and independent |
| Feature flag | Select a behavior branch at runtime | Decouple release from gradual behavior enablement | Flag state, stale branches and combinations create operational debt; flag rollback is not artifact rollback |

Cloud Deploy represents rollback as a new rollout based on a previous release. That provides a deployment trace, but does not reverse external side effects or database migrations. Make changes expand/contract compatible where practical, preserve idempotency, and decide whether rollback, flag disablement, or forward fix is safe for the specific state transition. A rollback gate should check the same revision and target identity, stop further promotion, and verify a user-level invariant after the recovery action.

The local lab models only a deterministic decision function: supplied percentages and error rates drive a simulated gate. A disposable cloud integration could establish API configuration, IAM authorization and actual controller-created rollout resources; it still would not establish production representativeness or prove that a schema change is reversible.""",
        "questions": [
            "Which observable user-facing signal stops promotion, and what sample size or evaluation window makes it meaningful?",
            "Can the previous binary run against the current schema and side effects without duplicating fulfillment?",
            "Who has authority to halt promotion, choose rollback versus forward fix, and confirm recovery?",
        ],
        "reference": "https://docs.cloud.google.com/deploy/docs/deployment-strategies",
        "reference_label": "Google Cloud Deploy: deployment strategies and canary behavior (checked 2026-09-29)",
        "scenario": {
            "scenario": "Synthetic Brightloaf planning case: revision r42 is promoted to 20% of checkout traffic after the fast unit and integration gates pass. The next observation window reports a 12% checkout error rate for r42 versus 0.4% on r41. This is a supplied tabletop fixture, not an observed incident.",
            "impact": "At the stated synthetic traffic share, 20 of every 100 requests are exposed to r42; if promotion reaches 100%, the potential blast radius grows fivefold. A failed order response may still have created an external payment or fulfillment side effect, so an error count alone cannot prove that retrying is safe.",
            "constraints": "Keep one fulfillment per order; stop additional promotion immediately; keep the known-good revision addressable; recovery must be visible in a rollout trace; no destructive database rollback is assumed.",
            "evidence": "```text\nCASE FIXTURE — synthetic values, not production telemetry\ntarget=checkout-prod\nstable_revision=r41\ncandidate_revision=r42\ncanary_share=20%\nr41_requests=2500 r41_5xx=10 error_rate=0.40%\nr42_requests=500 r42_5xx=60 error_rate=12.00%\nthreshold=2.00% for one 1-minute window\nfulfillment_invariant=one successful fulfillment per order_id\n```",
            "root": "The supplied numbers cross the stated 2% candidate error threshold by a factor of six. The defensible inference is to halt promotion and assess rollback. The fixture does not establish whether errors arose before or after a payment side effect; order IDs and downstream fulfillment records must be reconciled before replay.",
            "diagnostic_steps": [
                "Compare candidate and stable request counts and error numerators over the same one-minute windows; preserve the revision and traffic-share labels.",
                "Check the promotion event timeline to confirm that the candidate actually received 20% and no later phase was advanced.",
                "For failed order IDs, join request, payment and fulfillment records by idempotency key; separate failed response from failed transaction.",
                "Record whether an approved rollback can run against current data and whether any schema or external side effect makes forward repair safer.",
            ],
            "fix": "Stop promotion, preserve the observed metrics and rollout identifiers, then create a rollback rollout to the last known-good release if compatibility checks pass. Keep the candidate artifact and logs for diagnosis. Verify error rate and order correctness after traffic returns; if data compatibility is uncertain, disable the risky behavior or forward-fix under an explicit incident decision.",
            "verify": "In the local simulation, the gate rejects r42 at 20% and reports r41 as the selected known-good revision. A real service acceptance check would require error and latency recovery plus a reconciliation that each order has no more than one fulfillment; local output cannot supply that evidence.",
            "residual": "Rollback may leave schema changes, queued work, cache state or external payments behind. Canary sampling can also miss rare failures, and a single rollback duration can conceal the time spent detecting, deciding, and verifying recovery.",
            "facts": "The percentages, revision identifiers, counts and error threshold above are synthetic case inputs supplied for the lesson.",
            "inference": "The threshold breach warrants halting promotion; safe rollback depends on compatibility and side-effect reconciliation, neither of which is established by the fixture.",
            "expected": "Expected tabletop result: no further promotion, a recorded rollback decision, and a separate correctness check before retrying affected orders.",
            "diagram": ("r42 receives 20% traffic and crosses threshold", "Promotion gate was absent or ignored", "Potential checkout failures and duplicate retry risk", "Halt promotion; roll back only after compatibility check", "Known-good serving restored; reconcile order invariant"),
        },
        "lab": {
            "name": "Local canary gate and rollback trace rehearsal",
            "file": "day-129-topic-01-rollback-trace.md",
            "goal": "Execute a deterministic local release simulation that rejects a bad revision, selects the retained known-good revision, and records a reviewable rollback trace.",
            "expected": "A JSON rollback trace and terminal output identify candidate r42, the threshold breach, r41 as the prior good revision, simulated timestamps, and the verification boundary.",
            "mode": "Local Python standard-library simulation; no deployment, cloud access, or real traffic.",
            "prereq": "Python 3.10 or newer, a shell, and an empty working directory. No network or third-party packages are required.",
            "preflight": "Run the version and working-directory commands in Stage 1. All input values are synthetic, so do not replace them with customer traffic or production identifiers.",
            "steps": [
                """**Stage 1: Preflight the local runtime and isolated workspace**

Run the following from the repository root. Expected result: Python 3.10+ and a newly created empty directory; no cloud credentials are read.

```sh
python3 --version
test ! -e .day129-topic1 || { printf 'Remove or preserve existing .day129-topic1 before starting\\n' >&2; exit 1; }
mkdir .day129-topic1
find .day129-topic1 -maxdepth 1 -type f -print
```""",
                """**Stage 2: Prepare the known-good and candidate inputs**

Write the exact synthetic release observations and threshold. Expected result: the file contains r41, r42, the 20% share, 12% candidate error rate, and the 2% stop threshold.

```sh
cd .day129-topic1
cat > releases.json <<'EOF'
{
  "target": "checkout-sim",
  "stable": {"revision": "r41", "known_good": true, "error_rate": 0.004},
  "candidate": {"revision": "r42", "known_good": false, "traffic_share": 0.20, "error_rate": 0.12},
  "max_error_rate": 0.02,
  "simulated_start": "2026-09-29T10:00:00Z",
  "simulated_detection_minutes": 2,
  "simulated_rollback_minutes": 3,
  "verification": {"orders_checked": 100, "duplicate_fulfillments": 0}
}
EOF
python3 -m json.tool releases.json
cd ..
```""",
                """**Stage 3: Author the gate and trace generator**

Create a deterministic program that refuses promotion above threshold and requires a known-good target. Expected result: the source compiles without output or syntax errors.

```sh
cd .day129-topic1
cat > rollback_sim.py <<'PY'
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

def decide(data, missing_known_good=False):
    candidate = data["candidate"]
    stable = data["stable"]
    if candidate["error_rate"] > data["max_error_rate"]:
        action = "ROLLBACK"
        target = None if missing_known_good else stable["revision"]
    else:
        action, target = "PROMOTE", candidate["revision"]
    if action == "ROLLBACK" and (missing_known_good or not stable["known_good"]):
        action, target = "HOLD_NO_SAFE_TARGET", None
    start = datetime.fromisoformat(data["simulated_start"].replace("Z", "+00:00"))
    detected = start + timedelta(minutes=data["simulated_detection_minutes"])
    restored = detected + timedelta(minutes=data["simulated_rollback_minutes"])
    return {
        "target": data["target"], "candidate_revision": candidate["revision"],
        "candidate_error_rate": candidate["error_rate"],
        "threshold": data["max_error_rate"], "decision": action,
        "rollback_to": target, "detected_at": detected.isoformat(),
        "simulated_restored_at": restored.isoformat(),
        "simulated_recovery_minutes_after_detection": data["simulated_rollback_minutes"],
        "verification_boundary": "simulation only; no service or order database was queried",
    }

parser = argparse.ArgumentParser()
parser.add_argument("--missing-known-good", action="store_true")
args = parser.parse_args()
data = json.loads(Path("releases.json").read_text())
result = decide(data, args.missing_known_good)
Path("rollback-trace.json").write_text(json.dumps(result, indent=2) + "\\n")
print(json.dumps(result, indent=2))
PY
python3 -m py_compile rollback_sim.py
cd ..
```""",
                """**Stage 4: Execute the bad-revision decision and simulated rollback**

Run the gate against the prepared inputs. Expected result: `decision` is `ROLLBACK`, `rollback_to` is `r41`, and the trace file is created. Values remain explicitly simulated.

```sh
cd .day129-topic1
python3 rollback_sim.py
test -s rollback-trace.json && echo 'PASS: rollback trace created'
cd ..
```""",
                """**Stage 5: Inspect the target, timestamps and correctness boundary**

Assert the result using Python's standard library. Expected result: all three assertions pass; the script does not claim to verify a live order system.

```sh
cd .day129-topic1
python3 - <<'PY'
import json
trace = json.load(open("rollback-trace.json"))
assert trace["decision"] == "ROLLBACK"
assert trace["rollback_to"] == "r41"
assert trace["simulated_recovery_minutes_after_detection"] == 3
assert "simulation only" in trace["verification_boundary"]
print("PASS: rejected candidate, selected r41, preserved simulation boundary")
PY
cd ..
```""",
                """**Stage 6: Rehearse loss of the safe rollback target**

Simulate a missing known-good release. Expected result: the gate refuses to guess a target and returns `HOLD_NO_SAFE_TARGET`; it must never promote the bad candidate.

```sh
cd .day129-topic1
python3 rollback_sim.py --missing-known-good
python3 - <<'PY'
import json
trace = json.load(open("rollback-trace.json"))
assert trace["decision"] == "HOLD_NO_SAFE_TARGET"
assert trace["rollback_to"] is None
print("PASS: unsafe rollback target causes hold")
PY
cd ..
```""",
                """**Stage 7: Diagnose evidence and preserve the decision record**

Compare the candidate rate with the threshold and capture the event inputs, action and local boundary in a handoff note. Expected result: the note states `12% > 2%`, the selected recovery action, and that live telemetry and order reconciliation remain unverified.

```sh
cd .day129-topic1
cat > rollback-review.txt <<'EOF'
Synthetic input: candidate r42 error rate 12%; threshold 2%; exposure 20%.
Decision: stop promotion; rollback to r41 only when compatibility and side effects are checked.
Local execution: HOLD test passed when the known-good target was removed.
Unverified outside this simulation: Cloud Deploy rollout, live SLIs, schema compatibility, payment and fulfillment reconciliation.
EOF
cat rollback-review.txt
cd ..
```""",
                """**Stage 8: Close out and remove only the disposable exercise directory**

List the evidence, then remove the directory created in Stage 1. Expected result: the three evidence files are listed before cleanup and the directory is absent afterward.

```sh
cd .day129-topic1
ls -l releases.json rollback_sim.py rollback-trace.json rollback-review.txt
cd ..
rm -r .day129-topic1
test ! -e .day129-topic1 && echo 'PASS: local exercise files removed'
```""",
            ],
            "verification": "The JSON assertions in Stage 5 and Stage 6 verify the deterministic gate behavior and fail-safe edge case. Cloud controller rollout, actual service SLIs, data compatibility and order correctness require a separately authorized disposable integration environment and are deliberately outside this local exercise.",
            "trouble": "If source compilation fails, confirm the file was copied exactly and Python 3.10+ is active. If JSON parsing fails, rerun the Stage 2 heredoc exactly. The missing-target rehearsal overwrites the trace with a hold decision; rerun Stage 4 before capturing the normal rollback trace.",
            "cleanup": "No cloud resource or network request is created. Stage 8 removes only `.day129-topic1`, the directory created by this lab; copy the evidence files elsewhere before cleanup if retaining them.",
            "accept": "Retain a rollback trace containing candidate revision, threshold and observed simulated rate, decision, target known-good revision, detection and restore timestamps, plus the failure-mode hold result. Label every value simulated and attach the explicit cloud/data correctness verification boundary.",
        },
    },
    {
        "key": "topic-02",
        "title": "Test responsibilities, least-privilege pipeline identity and delivery metrics",
        "preview": "A build trigger can execute repository-controlled steps with its configured service account, while the same pipeline reports only an aggregate success count. Excess permissions widen compromise impact, and ambiguous metrics hide which service or denominator changed.",
        "overview": (
            "A delivery pipeline separates checks by the defect class and boundary each can expose: unit tests isolate logic; integration tests exercise selected dependency contracts; security checks inspect code, dependencies, configuration or artifacts; load tests probe capacity and latency under a stated workload. The pipeline identity is the principal whose permissions build steps can exercise, so its grant set should be limited to the target resources and actions required. Delivery measures then describe the service's change flow and instability using explicit events and windows. Day 129 ties these concerns to a recoverable release and evidence that can be compared over time."
        ),
        "technical": """### Checks, identity and measures have separate owners

The source event selects a revision; the build system evaluates the configured steps under a build execution identity; artifact publication and deployment may use separate identities. A trigger that runs untrusted changes with broad permissions can turn repository write access into build-time authority. Prefer a user-managed identity for the pipeline, scope grants to the needed artifact repository or target, keep deployment authority separate when possible, and record the source revision, artifact digest, identity and gate results together. Secret values do not belong in logs or ordinary build variables.

| Check | Failure class it can reveal | Input and evidence | Boundary |
|---|---|---|---|
| Unit | Function or component logic | Deterministic fixtures; test report for revision | Mocks do not establish dependency behavior or runtime wiring |
| Integration | Contract, serialization, auth or dependency wiring | Controlled emulator/test endpoint; dependency/version and result | Emulator behavior may differ from service control plane, IAM, quotas or managed runtime |
| Security | Known vulnerable dependency, exposed secret, unsafe config or policy violation | Scanner version, ruleset, artifact/revision and findings | Tool coverage and false negatives remain; approval does not prove absence of risk |
| Load | Saturation, latency, queueing or resource limits under a workload | Load shape, duration, environment, percentiles and abort thresholds | A local load model is not production capacity evidence; cloud results depend on topology, quotas and representative data |

Keep these signals and decisions tied to one service and a stable event definition. DORA's current guide names change lead time, deployment frequency, failed deployment recovery time, change fail rate, and deployment rework rate. Compute each from an explicit observation window and event population. For example, change fail rate is failed deployments requiring immediate intervention divided by all deployments in the same service/window; recovery time begins at impairment caused by a deployment and ends when service is restored. Report counts alongside rates: one failure in four deployments is 25%, but it is not a precise long-term estimate. Do not use a lower failure rate as a target if failures are under-reported.

This lab uses four supplied deployment records to calculate metrics and validates a permission matrix by inspection. It cannot prove Cloud Build's actual service account selection, IAM effective policy, scanner coverage, emulator fidelity, or cloud load behavior. A disposable cloud integration can inspect those specific boundaries, subject to identity, API, project, billing and cleanup checks. For current metric definitions, see [DORA's software delivery performance metrics guide](https://dora.dev/guides/dora-metrics/) (checked 2026-09-29).""",
        "questions": [
            "Which exact source revision, artifact digest, execution identity and target can be joined across the test and rollout records?",
            "What permissions does each pipeline phase need, and which untrusted inputs can cause that identity to act?",
            "Are metric events scoped to one service and a fixed window, with exclusions and both numerator and denominator retained?",
        ],
        "reference": "https://docs.cloud.google.com/build/docs/cloud-build-service-account",
        "reference_label": "Google Cloud Build: choose and scope the build service account (checked 2026-09-29)",
        "scenario": {
            "scenario": "Synthetic delivery review fixture: four checkout deployments occurred during a 14-day window. One required immediate rollback. The event export records commit-to-production durations of 5, 9, 12 and 2 hours, and the failed deployment was restored 45 minutes after the first user-impact signal. A draft pipeline matrix gives its build identity project-wide Editor. These are supplied values, not measured Brightloaf data.",
            "impact": "The single intervention is 1/4 or 25% change fail rate for this small sample. A project-wide Editor grant gives the build identity permissions unrelated to its build job, increasing the effect of compromised source or configuration. Combining several services or changing the denominator would make this baseline misleading.",
            "constraints": "Preserve the four-deployment window and its service scope; distinguish measurement from target-setting; do not imply the sample is statistically stable. Keep build, artifact publication and production deployment authority explicit and avoid broad project roles where a resource-specific grant is sufficient.",
            "evidence": "```text\nCASE FIXTURE — all events and grants below are synthetic\nservice=checkout | window=2026-09-15..2026-09-28 (14 days)\ndeployments=4 | failed deployments requiring immediate intervention=1\ncommit_to_production_hours=[5, 9, 12, 2]\nfailed_revision_user_impact=10:00Z | service_restored=10:45Z\nbuild_identity_grant=roles/editor at project scope\nreported monthly deployments=8 (not part of this 14-day window)\n```",
            "root": "From the stated records, deployments per 14 days equal four, change fail rate equals one intervention-requiring deployment divided by four deployments, and failed deployment recovery duration is 45 minutes. The median commit-to-production duration is seven hours. The project-wide Editor grant is broader than evidence in the fixture shows the build needs. This analysis cannot establish the real effective policy or the current pipeline identity.",
            "diagnostic_steps": [
                "Filter the event records to service `checkout` and the inclusive 14-day window; count eligible deployments before calculating any rate.",
                "Confirm that the failed deployment is counted once, and that recovery ends at restored service rather than at the time the rollback command was issued.",
                "Sort the four lead-time observations and compute the median from the middle pair; keep the individual values with the result.",
                "Split build, artifact-write and deploy actions by principal and target resource; replace the proposed project-wide grant only after required permissions are evidenced.",
            ],
            "fix": "Replace the aggregate dashboard with a per-service metric record that saves event definition, date window, deployment count, intervention count, duration endpoints and lead-time observations. For identity, inventory the actual build steps and resource targets, assign a dedicated user-managed execution service account, and grant only the required scoped permissions; use separate deployment authority when the flow permits. Re-run the pipeline and verify the selected principal and access outcome in cloud audit/build records before claiming the real grant is least-privilege.",
            "verify": "The local exercise should produce deployment frequency 4 per 14 days, change fail rate 25%, failed deployment recovery time 45 minutes, and median change lead time 7 hours, each labeled synthetic. Its permission matrix must mark project-wide Editor as rejected and leave the exact replacement roles pending evidence from actual build steps and resource scopes.",
            "residual": "Four deployments are too few to treat 25% as a stable team benchmark. Metric quality depends on consistent event classification and incident timestamps. A custom role can still be overbroad, and a successful local permission worksheet cannot show Cloud Build's effective permissions.",
            "facts": "All time values, counts, service labels and IAM grants are synthetic inputs defined for this case.",
            "inference": "The calculated result supports a baseline record and a least-privilege review; it does not prove a real project policy or recommend a universal performance target.",
            "expected": "Expected tabletop result: a reproducible per-service metric row and a permission review request that names actions/resources before changing IAM.",
            "diagram": ("Trigger runs repository revision with broad Editor identity", "Build trust and metric event boundaries are unclear", "Compromise blast radius widens; delivery trend cannot guide action", "Scope identity by action/resource and define service-level denominators", "Auditable pipeline evidence and comparable labeled metrics"),
        },
        "lab": {
            "name": "Local delivery-metric calculator and pipeline trust-boundary worksheet",
            "file": "day-129-topic-02-delivery-measures.md",
            "goal": "Calculate delivery measures from a fixed synthetic service window and produce a least-privilege review matrix plus test-boundary notes.",
            "expected": "A JSON report calculates deployment count 4, change fail rate 25%, failed deployment recovery time 45 minutes and median lead time 7 hours; a written matrix rejects project-wide Editor and names evidence still needed to select scoped roles.",
            "mode": "Local Python standard-library calculation and tabletop identity review; no cloud project, API or IAM policy is changed.",
            "prereq": "Python 3.10+ and a shell. The inputs and permissions are synthetic. Do not paste credentials, tokens, project IDs or customer data into the files.",
            "preflight": "Confirm Python 3 and the exercise starts in the intended repository directory. The exercise checks arithmetic and review logic only; actual IAM and Cloud Build identity are outside the local boundary.",
            "steps": [
                """**Stage 1: Preflight the interpreter and set the evidence boundary**

Run the commands from the repository root. Expected result: Python 3.10+ is available and the local exercise directory is empty.

```sh
python3 --version
test ! -e .day129-topic2 || { printf 'Remove or preserve existing .day129-topic2 before starting\\n' >&2; exit 1; }
mkdir .day129-topic2
find .day129-topic2 -maxdepth 1 -type f -print
```""",
                """**Stage 2: Prepare the fixed deployment event and role inputs**

Write the exact four-event dataset and role proposal. Expected result: JSON contains one service and a single 14-day observation window.

```sh
cd .day129-topic2
cat > delivery-events.json <<'EOF'
{
  "service": "checkout",
  "window_days": 14,
  "draft_monthly_deployment_count_not_in_window": 8,
  "deployments": [
    {"revision":"r38","lead_hours":5,"intervention":false},
    {"revision":"r39","lead_hours":9,"intervention":true,"impact_at":"2026-09-29T10:00:00Z","restored_at":"2026-09-29T10:45:00Z"},
    {"revision":"r40","lead_hours":12,"intervention":false},
    {"revision":"r41","lead_hours":2,"intervention":false}
  ],
  "proposed_build_grant": {"role":"roles/editor","scope":"project"},
  "observed_build_actions": ["read_source", "run_tests", "write_artifact"]
}
EOF
python3 -m json.tool delivery-events.json
cd ..
```""",
                """**Stage 3: Author the calculator and responsibility matrix**

Create a program that calculates the supplied measures and tests each check against its intended boundary. Expected result: both files compile/parse before execution.

```sh
cd .day129-topic2
cat > metrics.py <<'PY'
import json
from datetime import datetime
from pathlib import Path
from statistics import median

d = json.loads(Path("delivery-events.json").read_text())
events = d["deployments"]
failed = [e for e in events if e["intervention"]]
lead = [e["lead_hours"] for e in events]
restore_minutes = None
if failed:
    impact = datetime.fromisoformat(failed[0]["impact_at"].replace("Z", "+00:00"))
    restored = datetime.fromisoformat(failed[0]["restored_at"].replace("Z", "+00:00"))
    restore_minutes = int((restored - impact).total_seconds() / 60)
report = {
    "service": d["service"],
    "window_days": d["window_days"],
    "deployment_count": len(events),
    "deployment_frequency_per_14_days": len(events) * 14 / d["window_days"],
    "change_fail_rate": len(failed) / len(events),
    "failed_deployment_recovery_minutes": restore_minutes,
    "median_change_lead_hours": median(lead),
    "lead_time_observations_hours": sorted(lead),
    "label": "synthetic local calculation; not production measurement",
}
Path("metrics-report.json").write_text(json.dumps(report, indent=2) + "\\n")
print(json.dumps(report, indent=2))
PY
cat > responsibility.csv <<'EOF'
check,defect_boundary,local evidence,cloud evidence not established here
unit,isolated logic,fixture test result,production runtime behavior
integration,selected dependency contract,emulator or controlled endpoint result,managed service IAM quota and control-plane parity
security,known scanner rules and policy,tool/version/findings on exact revision,absence of unknown vulnerabilities
load,capacity under defined workload,load shape and local latency output,production capacity and quota behavior
build identity,actions against resource targets,action-to-resource review matrix,effective Cloud Build principal and IAM policy
EOF
python3 -m py_compile metrics.py
python3 -c 'import csv; list(csv.DictReader(open("responsibility.csv"))); print("PASS: responsibility matrix parses")'
cd ..
```""",
                """**Stage 4: Execute the metric calculation and inspect its labeled output**

Run the calculator. Expected result includes count `4`, frequency `4.0` per 14 days, failure rate `0.25`, recovery `45` minutes, and median lead time `7.0` hours.

```sh
cd .day129-topic2
python3 metrics.py
cd ..
```""",
                """**Stage 5: Verify the formulas and denominator from the source events**

Assert each value from the written dataset rather than a manually copied dashboard number. Expected result: every assertion passes and the synthetic label is present.

```sh
cd .day129-topic2
python3 - <<'PY'
import json
r = json.load(open("metrics-report.json"))
assert r["deployment_count"] == 4
assert r["deployment_frequency_per_14_days"] == 4.0
assert r["change_fail_rate"] == 0.25
assert r["failed_deployment_recovery_minutes"] == 45
assert r["median_change_lead_hours"] == 7.0
assert "synthetic" in r["label"]
print("PASS: service window, numerator, denominator and values agree")
PY
cd ..
```""",
                """**Stage 6: Rehearse a denominator and identity edge case**

Compare the fixed 14-day deployment count with the supplied draft monthly count of eight; then score the proposed project-wide Editor grant against the listed build actions. Expected result: reject mixing the monthly figure into the 14-day rate and flag Editor as broader than the listed evidence supports.

```sh
cd .day129-topic2
python3 - <<'PY'
import json
d = json.load(open("delivery-events.json"))
per_14_days = len(d["deployments"]) * 14 / d["window_days"]
assert per_14_days == 4
assert d["proposed_build_grant"] == {"role":"roles/editor", "scope":"project"}
assert d["draft_monthly_deployment_count_not_in_window"] == 8
print("EDGE: use 4 eligible deployments, not the unrelated monthly count 8")
print("EDGE: reject project-wide Editor pending action/resource-level permission evidence")
PY
cd ..
```""",
                """**Stage 7: Diagnose the evidence gaps and record the review decision**

Write a decision note with exact test boundaries, role evidence gaps and metric definitions. Expected result: the note identifies one service, 14 days, `1/4`, 45 minutes from impact to restored service, and requires cloud policy inspection before any IAM grant is selected.

```sh
cd .day129-topic2
cat > delivery-review.txt <<'EOF'
Synthetic checkout baseline: 4 deployments / 14 days; 1 required immediate intervention; change fail rate = 1/4 = 25%.
Failed deployment recovery: user impact at 10:00Z; service restored at 10:45Z; duration = 45 minutes.
Median commit-to-production lead time: median([2, 5, 9, 12]) = 7 hours.
Unit checks do not prove integration; emulators do not prove managed cloud IAM/quota/runtime behavior; local load does not prove production capacity.
Reject project-wide Editor as unsupported by this action list. Inventory actual artifact write target and required permissions; inspect effective principal/policy before selecting scoped grants.
All values are synthetic. This local lab does not inspect Cloud Build, IAM, scanners, or production.
EOF
cat delivery-review.txt
cd ..
```""",
                """**Stage 8: Close out and remove the disposable local evidence directory**

List the report and worksheet, then remove only the directory created in Stage 1. Expected result: evidence appears in the listing and the exercise directory is absent after cleanup.

```sh
cd .day129-topic2
ls -l delivery-events.json metrics.py metrics-report.json responsibility.csv delivery-review.txt
cd ..
rm -r .day129-topic2
test ! -e .day129-topic2 && echo 'PASS: local exercise files removed'
```""",
            ],
            "verification": "Stages 4–6 calculate and assert values from the written records. The responsibility matrix distinguishes local unit/integration/security/load evidence from a cloud integration check. Actual Cloud Build identity and effective IAM policy remain unverified until inspected in a disposable or approved project.",
            "trouble": "If the metric assertions fail, inspect `delivery-events.json` and make sure the four records and 14-day window match Stage 2. The median is the mean of 5 and 9 hours. A 25% rate is a four-event sample, not a universal benchmark or target. Do not grant project-wide Editor just to make the worksheet pass.",
            "cleanup": "No cloud calls or chargeable resources are involved. Stage 8 removes only `.day129-topic2`; retain copies of the JSON, CSV and decision note before cleanup if needed for the Day 129 exit pack.",
            "accept": "Keep the metric JSON and review note with service, period, deployment count, intervention numerator, recovery endpoints, lead-time observations and explicit synthetic label. Include the check-boundary matrix and a least-privilege proposal that names required actions/resources plus the cloud evidence still needed. Do not claim the local lab verified the actual pipeline identity or IAM policy.",
        },
    },
]
