"""Day 128: Build and deployment pipeline. Brightloaf data are synthetic."""
DAY_NUM = 128

def lab(name, goal, expected, prereq, preflight, steps, verification, accept, trouble, cleanup, file):
    return {"name": name, "goal": goal, "expected": expected,
            "mode": "Offline local exercise using synthetic data; no cloud APIs, provisioning, credentials, or spend",
            "prereq": prereq, "preflight": preflight,
            "steps": [f"#### {title}\n\n{body}" for title, body in steps],
            "verification": verification, "accept": accept,
            "trouble": trouble, "cleanup": cleanup, "file": file}

def step(title, command, result):
    return (title, f"""```bash
{command}
```

Expected observation: {result}""")

DATA = {
    "day": 128,
    "part1_intro": (
        "Day 128 connects a reviewed source revision to the exact bytes and target that serve users. Source policy establishes a reviewable history; "
        "Cloud Build evaluates a selected revision under a build identity; Artifact Registry stores and resolves versioned packages or images; Cloud Deploy "
        "records releases, rollouts, target progression and approvals. Bring the Day 127 test/recovery artifact and Day 114 release-integrity evidence. "
        "The exercises are local and synthetic so the identity and evidence chain can be repeated without a cloud project."
    ),
    "exit_summary": (
        "A reproducible local pipeline run linking source revision, passing test evidence and artifact digest; a staged-promotion diagram; an approval/identity "
        "boundary; and a short list of managed-target properties that still need a controlled Cloud Build, Artifact Registry or Cloud Deploy rehearsal."
    ),
    "part2_intro": (
        "Follow the source SHA through the event trigger, configured build steps, artifact digest, registry policy, release and target rollout. At each handoff, "
        "name the owner, identity and evidence. The diagram is a conceptual control path. Local checks prove only their own files and state model, not managed-service "
        "IAM, private-pool connectivity, registry retention, approval enforcement or runtime health."
    ),
    "arch_table_html": '''<div class="table-container"><table><thead><tr><th>Boundary</th><th>Owner / control</th><th>Evidence</th><th>Limit / trade-off</th></tr></thead><tbody>
<tr><td>Source and review</td><td>Application team owns repository, branch strategy, review and required checks; source-connection owner grants build read access.</td><td>Repository, event, commit SHA, reviewer/check result, protection policy, connection identity.</td><td>A branch name or tag can move. Green review is useful only when the build records the exact reviewed revision.</td></tr>
<tr><td>Build trigger and worker</td><td>Platform team owns event filters, substitutions, build config, pool/location and dedicated build service account.</td><td>Build ID, source SHA, config revision, substitutions, pool, identity, step logs/status and digest.</td><td>Private pool requires compatible region and configured DNS/routes/firewall/egress. Caches speed builds but never replace required tests or source provenance.</td></tr>
<tr><td>Artifact repository</td><td>Build identity writes; deployment/runtime identities read; platform owner selects standard, remote or virtual mode and cleanup policy.</td><td>Fully qualified artifact, digest, tag mapping, provenance, repository IAM, policy dry-run and target-to-digest inventory.</td><td>Tags can be mutable; a digest identifies bytes but does not prove trusted origin. Cleanup policy does not inherently know which artifact is deployed.</td></tr>
<tr><td>Release and target</td><td>Cloud Deploy pipeline owns progression, targets and rollout; application owner defines health evidence; approver accepts production risk.</td><td>Release/pipeline revision, digest, target, rollout state, approval actor/time, health result and rollback reference.</td><td>Promotion or successful rollout is not proof of user correctness. Rollback creates a new rollout from a prior release and cannot reverse incompatible data changes automatically.</td></tr>
<tr><td>Cross-stage identity</td><td>Release owner joins source SHA, build ID, artifact digest and target rollout; security owner defines least privilege and bypass review.</td><td>One release record with immutable identifiers, approval evidence, verification boundary and rollback plan.</td><td>Matching names/timestamps are not cryptographic provenance; digest and authorized build/promotion records must join.</td></tr>
</tbody></table></div>''',
    "arch_diagram": {
        "type": "topology", "title": "Day 128 source-to-target pipeline and trust boundaries",
        "desc": "Reviewed source commit triggers a Cloud Build run under a dedicated identity and selected worker pool. Ordered tests and packaging produce an artifact digest. Artifact Registry controls publishing, reading, dependency proxying and retention. Cloud Deploy creates releases and target rollouts with production approval and rollback. The local lab stops before all managed Google Cloud boundaries.",
        "caption": "Figure 128.1. Source-to-target delivery control path. This conceptual diagram shows evidence and ownership boundaries; local exercises do not prove Cloud Build, Artifact Registry, Cloud Deploy or runtime behavior in a live project.",
        "width": 1120, "height": 610,
        "layers": [
            {"name":"REVIEWED SOURCE · CHANGE CONTROL","y":25,"h":88,"fill":"#102b46","title_color":"#7dd3fc","desc":"Git host · commit SHA · required checks"},
            {"name":"BUILD CONTROL PLANE · EXECUTION IDENTITY","y":145,"h":98,"fill":"#073b33","title_color":"#6ee7b7","desc":"event · substitutions · pool · ordered steps"},
            {"name":"ARTIFACT AND PROVENANCE BOUNDARY","y":275,"h":90,"fill":"#422006","title_color":"#fdba74","desc":"digest · ACL · retention · dependency proxy"},
            {"name":"RELEASE PROGRESSION · TARGET CONTROL","y":395,"h":112,"fill":"#27204b","title_color":"#c4b5fd","desc":"release · rollout · approval · verification"},
            {"name":"EXIT EVIDENCE","y":535,"h":52,"fill":"#3b182c","title_color":"#fda4af","desc":"source SHA → build ID → digest → target state"}],
        "components": [
            {"x":45,"y":53,"w":215,"h":46,"name":"PR + protected branch","detail":"review · checks · SHA","stroke":"#38bdf8"},
            {"x":370,"y":53,"w":240,"h":46,"name":"Source connection","detail":"GitHub / GitLab / supported host","stroke":"#38bdf8"},
            {"x":720,"y":53,"w":330,"h":46,"name":"Push / PR event","detail":"branch and path filters","stroke":"#38bdf8"},
            {"x":55,"y":174,"w":220,"h":48,"name":"Cloud Build trigger","detail":"event SHA · substitutions","stroke":"#22c55e"},
            {"x":330,"y":174,"w":245,"h":48,"name":"Private/default worker","detail":"network · region · build SA","stroke":"#22c55e"},
            {"x":635,"y":174,"w":180,"h":48,"name":"Test gate","detail":"fail closed","stroke":"#22c55e"},
            {"x":865,"y":174,"w":190,"h":48,"name":"Package + digest","detail":"inputs retained","stroke":"#22c55e"},
            {"x":65,"y":302,"w":245,"h":46,"name":"Artifact Registry","detail":"writer / reader · cleanup","stroke":"#f59e0b"},
            {"x":415,"y":302,"w":245,"h":46,"name":"Pinned digest","detail":"same bytes promoted","stroke":"#f59e0b"},
            {"x":765,"y":302,"w":280,"h":46,"name":"Cloud Deploy release","detail":"rendered deployment intent","stroke":"#f59e0b"},
            {"x":65,"y":432,"w":185,"h":48,"name":"Test target","detail":"health / smoke","stroke":"#c084fc"},
            {"x":365,"y":432,"w":195,"h":48,"name":"Approval gate","detail":"named reviewer","stroke":"#f59e0b"},
            {"x":665,"y":432,"w":195,"h":48,"name":"Production target","detail":"same digest","stroke":"#22c55e"},
            {"x":925,"y":432,"w":135,"h":48,"name":"Rollback","detail":"new rollout","stroke":"#f43f5e"},
            {"x":245,"y":542,"w":630,"h":34,"name":"SHA · build · digest · approval · rollout · verification","detail":"release evidence record","stroke":"#fda4af"}],
        "flows": [
            {"x1":260,"y1":76,"x2":370,"y2":76,"label":"reviewed revision","type":"ok"},
            {"x1":610,"y1":76,"x2":720,"y2":76,"label":"event","type":"ok"},
            {"x1":850,"y1":99,"x2":165,"y2":174,"label":"select SHA","type":"ok"},
            {"x1":275,"y1":198,"x2":330,"y2":198,"label":"run","type":"ok"},
            {"x1":575,"y1":198,"x2":635,"y2":198,"label":"steps","type":"ok"},
            {"x1":815,"y1":198,"x2":865,"y2":198,"label":"pass","type":"ok"},
            {"x1":960,"y1":222,"x2":190,"y2":302,"label":"publish","type":"ok"},
            {"x1":310,"y1":325,"x2":415,"y2":325,"label":"resolve bytes","type":"ok"},
            {"x1":660,"y1":325,"x2":765,"y2":325,"label":"release input","type":"ok"},
            {"x1":890,"y1":348,"x2":155,"y2":432,"label":"test rollout","type":"ok"},
            {"x1":250,"y1":455,"x2":365,"y2":455,"label":"health","type":"ok"},
            {"x1":560,"y1":455,"x2":665,"y2":455,"label":"approve","type":"ok"},
            {"x1":860,"y1":455,"x2":925,"y2":455,"label":"new rollback rollout","type":"warn"},
            {"x1":465,"y1":480,"x2":540,"y2":542,"label":"retain","type":"ok"}],
        "boundaries": [
            {"x":30,"y":132,"w":1060,"h":123,"label":"BUILD BOUNDARY · IDENTITY AND NETWORK CONTROL EXECUTION"},
            {"x":30,"y":385,"w":1060,"h":136,"label":"PROMOTION BOUNDARY · APPROVAL AND TARGET HEALTH"}],
        "probes": [
            {"cx":1065,"cy":116,"label":"P1: compare event and fetched SHA","color":"#38bdf8"},
            {"cx":1065,"cy":258,"label":"P2: inspect step, SA, pool, digest","color":"#22c55e"},
            {"cx":1065,"cy":375,"label":"P3: compare repository ACL and digest","color":"#f59e0b"},
            {"cx":1065,"cy":520,"label":"P4: approval identity and rollout health","color":"#c084fc"}],
    },
    "part3_intro": (
        "These Brightloaf cases are synthetic exercises, not observed incidents. Supplied fixture facts are separated from causal inference. A failure is "
        "established only where evidence shows the chain stopped; a green build, registry tag or rollout state alone does not prove artifact provenance or user behavior."
    ),
    "part4_intro": (
        "Complete four offline exercises in sequence: local Git history, a deterministic build/test gate, artifact-retention analysis, and staged-promotion "
        "state transitions. Each exercise has eight execution stages with explicit inputs and results. No exercise provisions Google Cloud resources."
    ),
    "topics": [
        {
            "key":"topic-01", "title":"Source repositories, change review and branching strategy",
            "overview":("Source control records who changed which files, on which parent revision, and which review/check policy allowed a change into a release branch. "
                "GitHub and GitLab are common hosted choices; check current availability before selecting any managed source product for a new system. Trunk-based work "
                "uses short branches and fast checks; release branches support maintained release lines but create backport and divergence work. Repository administrators "
                "own protected-branch policy, application teams own commit quality, and a build connection should have only needed source access. This comes first because later "
                "build and deployment evidence must identify the reviewed revision."),
            "preview":"A pull request is green on commit `a81c2e0`, then a newer commit lands before a trigger fetches the branch head. The artifact may contain unreviewed bytes, leaving operators unable to attribute or safely roll back the release.",
            "technical":"""## Source event and immutable revision

A source provider emits a push, tag, or pull-request event. Trigger filters decide whether it starts a build. Bind the build to the event commit SHA and record it with the build ID; resolving a movable branch name later can race with a newer push. Review policy commonly requires approvals and named status checks on a protected default or release branch. Inspect who can bypass those controls and whether new commits invalidate stale approvals. GitHub and GitLab implement the details differently, so retain the effective host policy rather than assuming a feature name means identical enforcement.

Branching is a coordination choice. Trunk-based development reduces long-lived divergence but needs small changes, reliable tests and feature controls for incomplete work. Release branches isolate stabilization but require a reviewed backport/forward-port policy. Tags help people name releases, but a mutable tag is weaker evidence than a commit SHA. Version build and deployment configuration along with source; substitutions or out-of-band trigger settings can also change output.

The source boundary ends at the revision fetched and authorized by the connection. It does not prove dependencies are immutable, tests are meaningful, or output bytes came from that revision. Capture event SHA, fetched SHA, review/check result, connection identity and bypass audit. Local Git shows commit ancestry, not hosted protection or managed source identity. Source choice also depends on organization controls, identity federation, residency and integration support.

References: [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [GitLab protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/), and [Cloud Build trigger events and source filters](https://docs.cloud.google.com/build/docs/automating-builds/create-manage-triggers). Accessed 2026-09-29.""",
            "questions":["Does the build record the event SHA or only a movable branch name?","Who can bypass review/check rules, and where is that action audited?","Who owns release-branch backports and measures divergence?","Which build-affecting files and trigger settings are versioned?"],
            "reference":"https://docs.cloud.google.com/build/docs/automating-builds/create-manage-triggers",
            "reference_label":"Cloud Build trigger configuration, source events and revision filters (accessed 2026-09-29)",
            "scenario":{
                "scenario":"Synthetic fixture: checks pass for commit `a81c2e0`; build record stores only branch `main`; later commit `f42b910` appears; image is tagged `latest`; no reviewer record accompanies the artifact.",
                "impact":"Operators cannot establish whether the image contains the reviewed change. `latest` may point to different bytes during recovery, delaying service restoration and leaving the audit incomplete.",
                "constraints":"Preserve synthetic evidence. Do not force-push, rewrite shared history, or infer built commit from tag time. No actual provider/build log is supplied.",
                "evidence":"Known: checks attach to a81c2e0, build stores main, latest is used, and reviewer record is absent. Unknown: checkout trace, provenance, branch protection export, digest and whether f42b910 changes runtime behavior.",
                "root":"The source-to-build revision link is missing. A moving-head fetch is plausible but not established; incomplete logging or a separate invocation are alternatives. The raw event and checkout trace identify which occurred.",
                "diagnostic_steps":["Preserve event payload, trigger config, build ID, source audit record and checkout log; compare event SHA with fetched SHA.","Inspect review/check and bypass policy for both commits, including whether new commits invalidate approvals.","Resolve artifact digest and compare it with build provenance; do not treat `latest` as content identity."],
                "remediation_steps":["Pause promotion while retaining evidence; bind trigger execution to event revision and record repository, SHA and build ID.","Rebuild the approved SHA after required checks; publish a unique release label plus digest and provenance.","Enforce source-host checks and alert when resolved SHA is missing or mismatches the event. Define backport ownership for any release branches."],
                "verify":"Use a fixture where event SHA is a81c2e0 and branch head is f42b910. Acceptance is a build record containing a81c2e0 and a digest tied to that run. Local Git does not prove hosted rules.",
                "residual":"SHA linkage does not pin transitive dependencies or establish code safety. Lockfiles, provenance verification and host audit settings need separate evidence.",
                "diagram":("PR checks pass for a81c2e0","Build records main without fetched SHA","Digest/review attribution unknown","Bind build to event SHA and retain review","Same SHA maps to immutable digest"),
                "facts":"Synthetic fixture only: review applies to a81c2e0; build stores main; latest is mutable; artifact has no reviewer record.",
                "inference":"Revision linkage is missing. A different revision may have been built, but facts do not prove it.",
                "expected":"Rerun records event SHA and ties output digest to the checked revision."
            },
            "lab": lab("Local Git event-SHA and merge rehearsal", "Create a local repository, short feature branch, merge, and bounded conflict; preserve real commit IDs.", "A Git history and evidence note show base, feature, merge and conflict-resolution commits; hosted protection remains explicitly untested.", "Bring Day 127 test/recovery artifact and Day 114 release notes; Git and Python 3 locally.", "Use a disposable empty `day128-source-lab`; no remote or credentials.", [
                step("Stage 1: Check tools and workspace", "git --version\npython3 --version\nmkdir -p day128-source-lab && cd day128-source-lab\ntest ! -e service.txt", "tools are present and the target is empty"),
                step("Stage 2: Prepare the baseline source", "git init -b main\nprintf 'service=checkout\\napi_version=1\\nhealth=/healthz\\n' > service.txt\ngit add service.txt\ngit -c user.name=Learner -c user.email=learner@example.invalid commit -m baseline\ngit rev-parse HEAD > base.sha", "base.sha contains the baseline commit ID"),
                step("Stage 3: Create a reviewable feature revision", "git switch -c feature/health\nprintf 'status=200\\n' >> service.txt\ngit add service.txt\ngit -c user.name=Learner -c user.email=learner@example.invalid commit -m health-contract\ngit rev-parse HEAD > feature.sha", "feature.sha differs from base.sha and contains the added status"),
                step("Stage 4: Execute the planned merge", "git switch main\ngit merge --no-ff feature/health -m reviewed-health-change\ngit log --graph --oneline --all", "merge commit shows both parent histories"),
                ("Stage 5: Verify ancestry with an assertion", """```bash
python3 - <<'PY'
import subprocess
p = subprocess.check_output(['git','rev-list','--parents','-n','1','HEAD'],text=True).split()
assert len(p) == 3, p
assert open('base.sha').read().strip() in subprocess.check_output(['git','rev-list','--all'],text=True)
print('PASS: merge has two parents; base commit remains reachable')
PY
```

Expected observation: assertion prints PASS."""),
                step("Stage 6: Rehearse a bounded merge conflict", "git switch -c feature/version\nsed -i 's/api_version=1/api_version=2/' service.txt\ngit add service.txt && git -c user.name=Learner -c user.email=learner@example.invalid commit -m feature-v2\ngit switch main\nsed -i 's/api_version=1/api_version=3/' service.txt\ngit add service.txt && git -c user.name=Learner -c user.email=learner@example.invalid commit -m main-v3\ngit merge feature/version || true\ngit status --short", "Git marks service.txt as conflicted; this is a local exercise"),
                step("Stage 7: Resolve from an explicit decision", "printf 'service=checkout\\napi_version=3\\nhealth=/healthz\\nstatus=200\\n' > service.txt\ngit add service.txt\ngit -c user.name=Learner -c user.email=learner@example.invalid commit -m resolve-to-v3\nprintf 'resolution=choose v3 after synthetic owner review\\n' > source-evidence.txt\ngit rev-parse HEAD >> source-evidence.txt\ngit status --short", "tree is clean and evidence records selected value and resolution commit"),
                step("Stage 8: Close out and retain evidence", "git branch --merged main\ngit branch -d feature/health feature/version\ngit log --oneline --graph --all > source-history.txt\ncat source-evidence.txt", "merged branches are removed; repository, history and evidence remain"),
            ], "Stage 5 proves local ancestry. Stage 6 must show a conflict; Stage 7 names the chosen version and commit. State that hosted review and trigger identity were not exercised.", "Retain repository, source-history.txt, source-evidence.txt and all commit IDs; never claim hosted review. Exit mapping: source evidence establishes a traceable local revision/merge; hosted review and trigger linkage remain unverified.", "If init branch flag is unsupported, rename the initial branch to main. Keep the exact api_version=1 input for Stage 6.", "No cloud resources. Keep the repo for exit evidence; delete only after exporting its evidence.", "day128-source-lab/source-evidence.txt")
        },
        {
            "key":"topic-02", "title":"Cloud Build triggers, build steps, private pools, caching and substitutions",
            "overview":("Cloud Build turns a source event and versioned build configuration into isolated builder steps. A trigger selects event type/revision and may supply substitutions; "
                "the trigger's service account is the build execution identity, while a default or private worker pool supplies the execution and network context. Private pools help reach "
                "private dependencies, but region, DNS, routes, firewall, egress, source access and repository IAM still need deliberate configuration. Step ordering must reflect shared inputs; "
                "caches speed repeat work but cannot replace tests or provenance. This topic follows source because it governs how a checked revision becomes an artifact."),
            "preview":"A pull-request build enters a private pool but times out resolving `packages.internal`; a mismatched region and missing resolved substitutions make the failing boundary unclear. The release window slips while retries consume build capacity.",
            "technical":"""## Trigger input, execution identity, and ordered work

A Cloud Build trigger filters push, tag, or pull-request events and chooses a build configuration. Built-in substitutions can expose event/repository/commit information; trigger-specific substitutions can parameterize environment or image name. Treat them as untrusted inputs: validate allowed values and never put secrets in substitutions or logs. Trigger-invoked builds use the service account selected on the trigger, so grant that identity only the source-read, log-write, repository-write or deployment actions required for its steps. Keep build and deploy permissions separate where possible.

The config lists containerized steps, arguments, environment, volumes, dependencies, timeouts and outputs. Steps sharing generated files need ordering; independent work can run in parallel only when it has no unsafe shared state. A required test must gate packaging and publication. Capture step status, exit code, duration and logs. Default workers suit public build dependencies; a private pool provides a controlled VPC-connected build environment, but private DNS, routing, firewall/egress, source reachability, repository endpoints, pool project and region still determine connectivity. For a trigger using a private pool, verify regional compatibility and that the selected identity can use the pool.

Cache is an acceleration input. Docker layer cache requires a previously built image and only benefits unchanged lower layers; Cloud Storage caching supports other builders but adds storage permissions and lifecycle. Invalidate on lockfile, base image or toolchain changes; compare a clean build when investigating nondeterminism. A cache hit is not a passing test. For reproducibility retain source SHA, config revision, builder identity/image, substitutions, pool, step outcomes, artifact digest and build ID. Limits include mutable external dependencies, quotas/timeouts, transient worker/network errors and log retention.

The failure signals are trigger status, resolved revision/substitutions, step-level DNS/connection errors, pool location, build identity, cache hit/miss and published digest. Diagnose the first failed edge; a successful build does not prove a managed target is healthy.

References: [Cloud Build config schema](https://docs.cloud.google.com/build/docs/build-config-file-schema), [trigger configuration](https://docs.cloud.google.com/build/docs/automating-builds/create-manage-triggers), [private pools](https://docs.cloud.google.com/build/docs/private-pools/run-builds-in-private-pool), [substitutions](https://docs.cloud.google.com/build/docs/configuring-builds/substitute-variable-values), [build caching limits](https://docs.cloud.google.com/build/docs/optimize-builds/speeding-up-builds). Accessed 2026-09-29.""",
            "questions":["Which exact event SHA, config revision and substitution map entered the run?","Which identities can read source, write artifacts and deploy?","From the chosen pool, which DNS, route, firewall and IAM edges reach dependencies?","Which cache inputs invalidate on lockfile/toolchain changes, and can a clean build reproduce the digest?"],
            "reference":"https://docs.cloud.google.com/build/docs/private-pools/run-builds-in-private-pool",
            "reference_label":"Cloud Build private pool execution and configuration (accessed 2026-09-29)",
            "scenario":{"scenario":"Synthetic fixture: checkout succeeds, then `install-dependencies` times out resolving `packages.internal`. The run does not retain resolved substitutions; trigger and private pool are reported in different regions.",
                "impact":"Tests and artifact publication do not complete; retries delay the release and obscure whether DNS, region, route, firewall, identity or endpoint state caused the failure.",
                "constraints":"Do not bypass private egress controls or allow publication after failed tests. No real project, network, IAM or billing evidence is supplied.",
                "evidence":"Known: checkout passed; private hostname resolution timed out; trigger/pool regions differ; substitutions are missing. Unknown: exact regions/config versions, DNS visibility, route/firewall, identity, endpoint health and cache state.",
                "root":"The observed failure is name resolution at dependency fetch. Region mismatch is a configuration concern, but DNS visibility, egress, endpoint availability or substitution may be causal; current evidence cannot distinguish them.",
                "diagnostic_steps":["Preserve build ID, trigger/config revision, event SHA, substitutions, pool project/region and service account; compare region requirements.","Inspect private DNS visibility, then route/peering and firewall/egress, then endpoint health from the selected pool; preserve timestamps and exact errors.","Check source/artifact IAM and dependency authentication; compare cached and clean attempts only when policy permits."],
                "remediation_steps":["Keep publication gated. Choose a compatible pool/trigger region and repair only the evidenced DNS, route, firewall or identity boundary.","Version trigger/build config and record allowed substitutions; rerun the same source SHA with tests mandatory before packaging.","Add private-pool connectivity preflight and alerts for step-specific resolution failures. Do not silently replace private access with public egress."],
                "verify":"Local harness must show captured source/environment, passing ordered checks, and no artifact after a forced test failure. A managed run must additionally verify actual pool, region, DNS and IAM evidence.",
                "residual":"Local execution cannot prove private-pool connectivity, Cloud Build IAM, quota, caching behavior or charges.",
                "diagram":("PR selects a build","Private dependency DNS fails","Test and publish are skipped","Fix evidenced boundary and preserve inputs","Same SHA publishes only after checks pass"),
                "facts":"Synthetic fixture: source checkout succeeds, dependency DNS times out, regions differ, substitutions are absent.",
                "inference":"DNS visibility, region selection, route/firewall, endpoint, credentials or substitution may explain the error; cause remains unconfirmed.",
                "expected":"Corrected run records context and passes dependencies/tests; failed tests still block publication."},
            "lab":lab("Local build/test/package gate with captured substitutions","Run a standard-library harness in dependency-check, unit-test, package order, then force a negative test.","Passing run records source label, environment, ordered steps and SHA-256; negative run fails and leaves no package.","Python 3, Day 127 test artifact, Day 114 release-integrity evidence.","New empty `day128-build-lab`; local only, no YAML parser, cloud API, private pool or credentials.",[
                step("Stage 1: Preflight Python and workspace","python3 --version\nmkdir -p day128-build-lab && cd day128-build-lab\ntest ! -e runner.py && mkdir -p src tests out","new local workspace exists"),
                step("Stage 2: Prepare exact source and test input","cat > src/service.py <<'EOF'\ndef health(environment):\n    return {'service':'checkout','environment':environment,'status':200}\nEOF\ncat > tests/test_service.py <<'EOF'\nfrom src.service import health\nassert health('staging') == {'service':'checkout','environment':'staging','status':200}\nprint('PASS: staging health')\nEOF\ntouch src/__init__.py","staging/status 200 expectation is recorded"),
                step("Stage 3: Author the plan and executable runner","cat > plan.json <<'EOF'\n{\"source\":\"fixture-sha-001\",\"environment\":\"staging\",\"steps\":[\"dependency-check\",\"unit-test\",\"package\"]}\nEOF\ncat > runner.py <<'PY'\nimport hashlib,json,subprocess,sys\nfrom pathlib import Path\np=json.loads(Path('plan.json').read_text()); results=[]\nfor name in p['steps']:\n if name=='dependency-check':\n  assert Path('src/service.py').exists(); results.append({'step':name,'status':'PASS'})\n elif name=='unit-test':\n  r=subprocess.run([sys.executable,'tests/test_service.py'],capture_output=True,text=True); print(r.stdout,end='')\n  if r.returncode: Path('out/artifact.json').unlink(missing_ok=True); results.append({'step':name,'status':'FAIL'}); Path('out/run.json').write_text(json.dumps({'source':p['source'],'steps':results},indent=2)); raise SystemExit(1)\n  results.append({'step':name,'status':'PASS'})\n elif name=='package':\n  h=hashlib.sha256(Path('src/service.py').read_bytes()).hexdigest(); Path('out/artifact.json').write_text(json.dumps({'source':p['source'],'environment':p['environment'],'sha256':h})+'\\n'); results.append({'step':name,'status':'PASS','sha256':h})\nPath('out/run.json').write_text(json.dumps({'source':p['source'],'environment':p['environment'],'steps':results},indent=2)); print('BUILD PASS:',','.join(x['step'] for x in results))\nPY","runner enforces step order and exits before package on failed test"),
                step("Stage 4: Execute the planned build","python3 runner.py","output ends `BUILD PASS: dependency-check,unit-test,package`"),
                ("Stage 5: Inspect outcome and recompute digest","""```bash
python3 - <<'PY'
import hashlib,json
from pathlib import Path
r=json.loads(Path('out/run.json').read_text()); a=json.loads(Path('out/artifact.json').read_text())
h=hashlib.sha256(Path('src/service.py').read_bytes()).hexdigest()
assert [s['step'] for s in r['steps']]==['dependency-check','unit-test','package']
assert all(s['status']=='PASS' for s in r['steps']) and a['sha256']==h==r['steps'][-1]['sha256']
print('PASS: step order, substitution and digest match')
PY
```

Expected observation: all checks pass and independently computed source digest matches the package."""),
                step("Stage 6: Exercise the failing-test gate","cp tests/test_service.py tests/good.py\nsed -i s/200/503/ tests/test_service.py\npython3 runner.py || echo 'EXPECTED: test failed'\ntest ! -e out/artifact.json && echo 'PASS: no artifact published'","runner exits nonzero and artifact does not exist"),
                step("Stage 7: Diagnose and remediate the test input","mv tests/good.py tests/test_service.py\npython3 runner.py\npython3 -c \"import json; r=json.load(open('out/run.json')); assert len(r['steps'])==3 and all(x['status']=='PASS' for x in r['steps']); print('PASS: corrected run')\"\nprintf 'failure=test blocked package; remediation=restore status 200\\n' > out/remediation.txt","corrected test yields complete passing record and remediation note"),
                step("Stage 8: Close out with retained evidence","sha256sum out/artifact.json out/run.json\nfind out -maxdepth 1 -type f -print | sort","artifact, execution record and remediation evidence remain in out")
            ],"Stage 5 verifies order and digest. Stage 6 must fail closed; Stage 7 must pass after restoration. Mark managed service behavior untested.","Keep plan, runner, passing run.json, artifact digest, negative-case remediation and source revision label. Exit mapping: run record plus recomputed digest and negative-gate evidence form the reproducible pipeline run.","Runner uses Python standard library. The negative test changes expected 200 to 503; inspect the file if no failure occurs. No Cloud Build YAML is executed.","No chargeable resources. Retain the local evidence directory; remove only after exporting artifacts.","day128-build-lab/out/run.json")
        },
        {
            "key":"topic-03", "title":"Artifact Registry repositories, digest identity, cleanup and dependency proxies",
            "overview":("Artifact Registry provides a durable handoff for owned packages and images. Standard repositories store published versions; remote repositories cache upstream packages; "
                "virtual repositories present a single endpoint across configured standard/remote upstreams, with priority controlling lookup. Repository owners set location, format, mode, IAM and cleanup; "
                "the build identity writes and deploy/runtime identities read. Tags are useful labels but may move; promote by digest to keep the exact bytes stable. Cleanup must retain artifacts still deployed or eligible for rollback. This follows build because the registry is the publication, access and retention boundary."),
            "preview":"An age-based cleanup rule selects an untagged digest that production still runs, while a mutable `stable` tag points to a newer image. The recovery candidate disappears and service restoration may require a non-reproducible rebuild.",
            "technical":"""## Repository mode, resolution and retention

A repository is configured for an artifact format and location, with a supported mode. Standard repositories hold owned published artifacts. Remote repositories proxy and cache an upstream version after first retrieval; the cache improves availability and control but does not itself establish that a dependency is approved. Virtual repositories present one endpoint across standard/remote upstreams. Explicit priorities matter: validate that a private package cannot be shadowed by a public package with the same name. Document the fully qualified repository path so build, deploy and runtime clients resolve the intended source.

For images, a tag is a readable name, while a digest identifies bytes. Tags can move unless immutable-tag settings apply; record the tag for humans and digest for deployment. Give publisher identities write access and deploy/runtime principals only read access. Avoid granting repository administration to the build merely to publish. Capture upload/download and policy changes in audit evidence.

Cleanup policies select versions by age, tag state/prefix and other criteria. Keep policies protect matching artifacts from a delete rule; overlaps and policy order must be evaluated against the actual repository contents. Cleanup is not deployment-aware by itself. Join target inventory to digests, preserve current and agreed rollback releases, use dry-run before deletion, and require an owner to approve the exact candidate set. Review retention duration against incident recovery window, release cadence, regional access, provenance retention, vulnerability response and package consumers. A digest may remain listed but still be unusable if IAM or regional access is broken.

Signals include repository mode/location, tag-to-digest mapping, deployed digest, remote cache miss/upstream error, virtual priority, artifact IAM, cleanup dry-run candidates and audit records. A digest proves byte identity, not trusted origin; build provenance and source linkage complete the chain.

References: [repository modes and creation](https://docs.cloud.google.com/artifact-registry/docs/repositories/create-repos), [remote repository caching](https://docs.cloud.google.com/artifact-registry/docs/repositories/remote-overview), [virtual repository creation and priority](https://docs.cloud.google.com/artifact-registry/docs/repositories/virtual-repo), [cleanup policy precedence](https://docs.cloud.google.com/artifact-registry/docs/repositories/cleanup-policy-overview), [configure cleanup policies](https://docs.cloud.google.com/artifact-registry/docs/repositories/cleanup-policy). Accessed 2026-09-29.""",
            "questions":["Does deployment resolve by immutable digest or a mutable tag?","What repository mode and priority resolves the package name?","Can cleanup select a live or rollback digest, and what dry-run evidence exists?","Which identity may publish, read, change policy or delete versions?"],
            "reference":"https://docs.cloud.google.com/artifact-registry/docs/repositories/cleanup-policy-overview",
            "reference_label":"Artifact Registry cleanup policy precedence and supported repositories (accessed 2026-09-29)",
            "scenario":{"scenario":"Synthetic fixture: digest aaa is reported deployed, untagged and 45 days old; bbb is a prior known-good rollback candidate, untagged and 80 days old; ccc is a new candidate and `stable` points to it. Proposed policy deletes untagged versions older than 30 days.",
                "impact":"Applying the rule could remove deployed bytes and a rollback option while leaving a movable `stable` label as misleading evidence.",
                "constraints":"No policy is applied from the fixture. Preserve active and recovery candidates until owners confirm inventory; records are not a live repository snapshot.",
                "evidence":"Known: aaa deployed/untagged/45d; bbb rollback/untagged/80d; ccc candidate; stable->ccc; age cutoff 30d. Unknown: current policy dry run, consumers, repository mode/location, digest provenance, immutable-tag setting and inventory freshness.",
                "root":"The risk is that cleanup selection lacks deployment references. Age and tag state alone can select an active digest. The `stable` mapping does not retain old bytes. Stale or incomplete inventory may miss additional consumers.",
                "diagnostic_steps":["Export policy/mode, digest-tag mappings, cleanup mode, audit events and timestamped target-to-digest inventory.","Evaluate every active and rollback digest against all keep/delete rules; inspect overlaps and identity allowed to delete.","Check provenance and reader permissions for active/recovery digests and list any consumer not represented by the inventory."],
                "remediation_steps":["Keep deletion disabled or dry-run until the full consumer inventory is reconciled; add explicit keep handling for live/recovery digest references.","Have service owners review exact dry-run candidates and retention window; record approver and rollback source before enabling cleanup.","Promote by digest, persist target-to-digest inventory, and review cleanup results plus audit evidence after the policy takes effect."],
                "verify":"Fixture must retain aaa and bbb, and list ddd (only if unreferenced and matching) as a candidate pending approval. A live rehearsal requires disposable repository, real dry run and inventory review; not performed here.",
                "residual":"Cleanup policies cannot infer workload references unless supplied by an external inventory process. Stale inventory or lost reader access can still make a retained artifact unusable.",
                "diagram":("Age rule selects active digest aaa","Policy lacks deployment-aware keep set","Active bytes and recovery option at risk","Join target inventory; review keep rules","Active and rollback digests stay available"),
                "facts":"Synthetic records specify active aaa and rollback bbb are untagged and older than 30 days; stable currently labels ccc.",
                "inference":"Without a keep-set join, the proposed age rule selects active and rollback records; live matching results are unknown.",
                "expected":"Reviewed dry-run retains live/recovery digests and treats only unreferenced versions as pending candidates."},
            "lab":lab("Local digest inventory and cleanup policy safety model","Evaluate synthetic digest records against age deletion and active/rollback references; show how missing inventory changes the candidate set.","Report protects active and rollback digests, identifies only unreferenced old bytes as candidate, and fails a deliberately incomplete keep set.","Day 128 build digest and Day 114 release-integrity notes; Python 3.","Fresh `day128-registry-lab`; offline fixture only. Do not run gcloud, upload artifacts, enable APIs or change a real cleanup policy.",[
                step("Stage 1: Preflight and isolate the policy fixture","python3 --version\nmkdir -p day128-registry-lab && cd day128-registry-lab\ntest ! -e evaluator.py && mkdir out","Python available; new output folder created"),
                step("Stage 2: Prepare exact artifact and target inventory","cat > inventory.json <<'EOF'\n{\"cutoff_days\":30,\"active\":\"aaa\",\"rollback\":[\"bbb\"],\"artifacts\":[{\"digest\":\"aaa\",\"age\":45,\"tags\":[]},{\"digest\":\"bbb\",\"age\":80,\"tags\":[]},{\"digest\":\"ccc\",\"age\":2,\"tags\":[\"stable\"]},{\"digest\":\"ddd\",\"age\":70,\"tags\":[]}]}\nEOF\ncat inventory.json","aaa deployed, bbb rollback, ccc stable candidate, ddd unreferenced; age threshold is 30d"),
                step("Stage 3: Author the local policy evaluator","cat > evaluator.py <<'PY'\nimport json\nfrom pathlib import Path\ni=json.loads(Path('inventory.json').read_text()); keep={i['active'],*i['rollback']}; rows=[]\nfor a in i['artifacts']:\n if a['digest'] in keep: action='KEEP: active or rollback reference'\n elif not a['tags'] and a['age']>i['cutoff_days']: action='CANDIDATE: owner review required'\n else: action='KEEP: age rule does not match'\n rows.append(f\"{a['digest']} | {action}\")\nPath('out/report.txt').write_text('\\n'.join(rows)+'\\n'); print('\\n'.join(rows))\nPY","evaluator joins deployment references before age/tag criteria"),
                step("Stage 4: Execute the policy analysis","python3 evaluator.py","aaa and bbb are kept, ccc is kept, and only ddd is a deletion candidate"),
                ("Stage 5: Verify exact expected state","""```bash
python3 - <<'PY'
from pathlib import Path
r=Path('out/report.txt').read_text()
assert 'aaa | KEEP:' in r and 'bbb | KEEP:' in r
assert 'ccc | KEEP:' in r and 'ddd | CANDIDATE:' in r
print('PASS: active and rollback digests protected; one unreferenced candidate')
PY
```

Expected observation: four inventory records yield three keeps and one candidate."""),
                step("Stage 6: Challenge an incomplete rollback inventory","cp inventory.json inventory.good.json\npython3 -c \"import json; p='inventory.json'; d=json.load(open(p)); d['rollback']=[]; open(p,'w').write(json.dumps(d))\"\npython3 evaluator.py\ngrep 'bbb | CANDIDATE:' out/report.txt","bbb becomes an age-rule candidate when its rollback reference is omitted"),
                step("Stage 7: Diagnose and restore the keep reference","mv inventory.good.json inventory.json\npython3 evaluator.py\ngrep 'bbb | KEEP:' out/report.txt\nprintf 'decision=retain aaa active and bbb rollback; review ddd before deletion\\n' > out/review.txt","report protects bbb again and review note names candidate"),
                step("Stage 8: Close the exercise with policy evidence","sha256sum inventory.json evaluator.py out/report.txt\ncat out/review.txt","inventory, evaluator, report and decision note retained")
            ],"Stage 5 checks expected candidate set; Stage 6 demonstrates missing inventory risk; Stage 7 restores protection. Label as local model, not Artifact Registry behavior.","Retain inventory, evaluator, report, checksums and review decision naming active/rollback digests and candidate. Exit mapping: the digest inventory and candidate review support the staged-promotion diagram; live cleanup-policy behavior remains unverified.","If the negative case does not expose bbb, ensure bbb has no tag and is older than the 30-day cutoff. Never apply this model output to a repository.","No artifacts uploaded/deleted. Keep synthetic files as evidence; remove only disposable copies after exporting.","day128-registry-lab/out/report.txt")
        },
        {
            "key":"topic-04", "title":"Cloud Deploy delivery pipelines, targets, promotion, approvals and rollback",
            "overview":("Cloud Deploy models target progression as releases and rollouts. A pipeline defines target order; release captures rendered deployment intent and references an artifact; each rollout applies it to a target. "
                "Promotion creates a rollout at the next target, which may wait for human or integrated approval. Platform owners define targets/execution identities; application owners define health evidence and compatibility; approvers accept risk at an explicit boundary. Rollback creates a new rollout from a previously successful release; it cannot by itself reverse a schema change or external side effect. This closes the source/build/registry chain with a target and recovery decision."),
            "preview":"Release r-204 passed test at digest aaa, but mutable label v2.4 now resolves to digest ccc when production approval is pending. Approval based on the label may deploy bytes that never passed the test target, creating customer risk.",
            "technical":"""## Release progression and approval boundary

A delivery pipeline defines ordered targets and optional deployment strategies. Target configuration names the destination and execution requirements. A release captures rendered manifests and pipeline context; a rollout executes the release at a target. Promotion normally creates a rollout to the next target; inspect a pipeline-mismatch warning because an existing release remains associated with its original pipeline instance. Record release, target and pipeline revision with every decision.

Approval is a gate, not proof of correctness. A target can require approval; the reviewer should inspect source SHA, build ID, exact artifact digest, rendered diff, prior-target health, change record and recovery plan. Separate the identity permitted to request promotion, the deployment execution identity, and approver where practical. Record who approved/rejected and why. Automatic promotion shortens lead time but requires equivalent automated checks and clear stop conditions.

Rollout completion is control-plane evidence, not end-user correctness. Set target acceptance using health checks, smoke tests, latency/error signals and business invariants. Canary/staged rollout limits exposure only when traffic routing, metric windows and abort thresholds are real. Rollback creates another rollout from a previous successful release; it does not undo data migrations, queued events, secret changes or external side effects. Use expand/migrate/contract sequencing and decide whether rollback, forward fix or data recovery is safe for current state.

Signals include release/pipeline revision, target, rollout phase/job, pending/approved/rejected state, manifest diff, deployed digest and application health. Diagnose whether the first failure occurred at authorization, approval, target execution, verification or application behavior. Day 128's local state model does not provision GKE, Cloud Run or another managed target.

References: [pipeline and target configuration](https://docs.cloud.google.com/deploy/docs/create-pipeline-targets), [promotion and approvals](https://docs.cloud.google.com/deploy/docs/promote-release), [rollout management](https://docs.cloud.google.com/deploy/docs/deployment-strategies/manage-rollout), and [rollback behavior](https://docs.cloud.google.com/deploy/docs/roll-back). Accessed 2026-09-29.""",
            "questions":["Does production use the exact digest verified in the prior target?","What release, manifest diff and health evidence must the approver inspect?","Which identity requests, executes and approves rollout?","Can the prior release run safely against current schema and external state?"],
            "reference":"https://docs.cloud.google.com/deploy/docs/promote-release",
            "reference_label":"Cloud Deploy release promotion and rollout approval (accessed 2026-09-29)",
            "scenario":{"scenario":"Synthetic fixture: r-204 passed test at digest aaa; mutable tag v2.4 now maps to ccc; r-203 production used bbb. Production approval is pending, but the ticket lacks digest comparison, health threshold and schema compatibility evidence.",
                "impact":"Approval by release label could deploy bytes different from the tested release. If new code changed stored data, restoring older code may not restore a compatible state.",
                "constraints":"No actual promotion or approval. Preserve service and evidence. The fixture does not show why the tag moved or whether the migration is backward compatible.",
                "evidence":"Known: test r-204/aaa; v2.4/ccc; prod r-203/bbb; approval pending; ticket lacks digest/health/schema. Unknown: release provenance, manifests, live target state, pipeline revision, migration and approver permissions.",
                "root":"The approval packet cannot establish artifact continuity or recovery compatibility. Tag movement, packaging mismatch, or separate rebuild may explain the digest delta; none is proven.",
                "diagnostic_steps":["Freeze decision and compare release metadata, pipeline instance, rendered manifest, source/build provenance and registry digest.","Inspect current production target inventory, rollout history, approval identity, health evidence and stop signals.","Ask service/data owner whether prior release runs against current schema/state and what invariant guides rollback versus forward fix."],
                "remediation_steps":["Do not approve while mismatch remains unexplained; create a reviewed release bound to the approved source and digest rather than silently retagging.","Require approval record to name source SHA, build, digest, target, pipeline revision, health, schema compatibility, approver and abort plan.","If unhealthy, have incident/data owner choose rollback or forward fix; verify service and data behavior after the rollout and retain the recovery record."],
                "verify":"State model blocks production while pending, rejects digest ccc when test used aaa, then records named approval and rollback as a new rollout to prior r-203/bbb. Managed rehearsal must inspect actual Cloud Deploy state and target health.",
                "residual":"Digest continuity and approval do not guarantee business correctness. Metrics may lag, and code rollback cannot reverse all data or external side effects.",
                "diagram":("Test release passes with digest aaa","v2.4 now resolves to ccc","Pending approval may send untested bytes","Block and reconcile digest/schema evidence","Approved digest; recovery is a new rollout"),
                "facts":"Synthetic facts: r-204 test digest aaa, tag v2.4 maps ccc, r-203 prod bbb, approval lacks evidence.",
                "inference":"Artifact change or tag movement is possible but not diagnosed; approval must wait for evidence.",
                "expected":"Only the tested digest passes approval; rollback references prior release in a new rollout and verifies current-state compatibility."},
            "lab":lab("Local staged-promotion and rollback state model","Advance one synthetic release from test to approval-gated production, reject changed digest, and record recovery as a new rollout.","Ledger records test success, production pending, digest mismatch rejection, named approval and separate rollback to previous release.","Day 128 build record and registry inventory; Python 3 standard library.","Fresh `day128-deploy-lab`; all names/digests synthetic. No pipeline, target, IAM binding or runtime is created.",[
                step("Stage 1: Preflight the state-model workspace","python3 --version\nmkdir -p day128-deploy-lab && cd day128-deploy-lab\ntest ! -e releases.json && mkdir out","fresh offline directory and Python available"),
                step("Stage 2: Prepare release and target fixture","cat > releases.json <<'EOF'\n{\"pipeline\":\"fixture-7\",\"targets\":[\"test\",\"production\"],\"approval_required\":[\"production\"],\"previous\":{\"id\":\"r-203\",\"digest\":\"bbb\"},\"candidate\":{\"id\":\"r-204\",\"digest\":\"aaa\",\"tested_at\":\"test\"},\"tag\":{\"v2.4\":\"ccc\"}}\nEOF\ncat releases.json","previous prod is bbb, tested candidate is aaa, movable tag resolves ccc, production requires approval"),
                step("Stage 3: Author guarded rollout logic","cat > rollout.py <<'PY'\nimport json\nfrom pathlib import Path\nc=json.loads(Path('releases.json').read_text()); r=[]\ndef deploy(rel,target,digest,approved=False):\n if digest!=rel['digest']: raise ValueError('digest mismatch')\n state='PENDING_APPROVAL' if target in c['approval_required'] and not approved else 'SUCCEEDED'\n r.append({'release':rel['id'],'target':target,'digest':digest,'state':state})\ndeploy(c['candidate'],'test','aaa'); deploy(c['candidate'],'production','aaa')\nPath('out/ledger.json').write_text(json.dumps(r,indent=2)+'\\n')\nprint('test=SUCCEEDED production=PENDING_APPROVAL')\nPY\npython3 rollout.py","guard compares digest and records required approval state"),
                step("Stage 4: Execute staged release simulation","python3 rollout.py && cat out/ledger.json","r-204/aaa test succeeds and production remains pending"),
                ("Stage 5: Verify digest continuity and approval boundary","""```bash
python3 - <<'PY'
import json
r=json.load(open('out/ledger.json')); assert r[0]['digest']==r[1]['digest']=='aaa'
assert r[0]['state']=='SUCCEEDED' and r[1]['state']=='PENDING_APPROVAL'
assert json.load(open('releases.json'))['tag']['v2.4']!='aaa'
print('PASS: production held; mutable tag cannot replace tested digest')
PY
```

Expected observation: assertion passes with same tested digest and pending production state."""),
                step("Stage 6: Challenge with mutable-tag substitution","python3 - <<'PY'\nimport json\nc=json.load(open('releases.json'))\ntry:\n assert c['tag']['v2.4']==c['candidate']['digest'], 'tag digest differs from test digest'\nexcept AssertionError as e: print('EXPECTED BLOCK:',e)\nelse: raise SystemExit('ERROR: changed digest accepted')\nPY","attempt to use ccc instead of tested aaa is rejected"),
                step("Stage 7: Record approval and prior-release rollback","python3 - <<'PY'\nimport json\nfrom pathlib import Path\nr=json.load(open('out/ledger.json')); c=json.load(open('releases.json'))\nr += [{'release':'r-204','target':'production','digest':'aaa','state':'SUCCEEDED','approval':'synthetic-approval-17'}, {'release':'r-203','target':'production','digest':'bbb','state':'SUCCEEDED','kind':'new rollback rollout','rollback_from':'r-204'}]\nPath('out/ledger.json').write_text(json.dumps(r,indent=2)+'\\n')\nassert r[-2]['approval']=='synthetic-approval-17' and r[-1]['rollback_from']=='r-204'\nPath('out/review.txt').write_text('approver=synthetic-approval-17\\nhealth_gate=required for managed target\\nschema_compatibility=owner evidence required\\n')\nprint('PASS: approval and distinct rollback rollout recorded')\nPY","candidate approval is named; rollback is a separate rollout to r-203/bbb"),
                step("Stage 8: Close out with retained rollout evidence","python3 -c \"import json; r=json.load(open('out/ledger.json')); assert len(r)==4; print('PASS: 4 rollout records')\"\ncat out/ledger.json out/review.txt","ledger shows test, pending gate, approval, and new rollback; all states are local simulation"),
            ],"Assert same digest from test to production; challenge tag substitution; record approval and distinct rollback. State that actual managed target was not used.","Retain fixture, guarded script, rollout ledger, approval note and a limitation statement identifying the intended managed target rehearsal. Exit mapping: the digest continuity and staged rollout ledger provide the promotion artifact; a real target rehearsal is still required to claim managed deployment evidence.","Synthetic data only; use a fresh directory if ledger contains stale rows. Real identity, permission, target, region, API, billing and rollback requirements must be checked before a future authorized cloud lab.","No Google Cloud resources created. Keep ledger and decision evidence for exit artifact.","day128-deploy-lab/out/ledger.json")
        },
    ],
}
