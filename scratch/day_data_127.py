"""Day 127: Terraform testing, drift and recovery.

All Brightloaf records are synthetic. The executable exercise uses only
Terraform's built-in terraform_data resource and local state. Drift/import and
recovery decisions use exact tabletop fixtures; no remote backend is touched.
"""

DAY_NUM = 127


def lab(name, goal, expected, prereq, preflight, steps, verification, accept,
        trouble, cleanup, file):
    return {
        "name": name, "goal": goal, "expected": expected,
        "mode": "Local Terraform CLI with built-in terraform_data and local state; synthetic drift/import/recovery tabletop; no provider downloads, cloud API calls, remote state or spend",
        "prereq": prereq, "preflight": preflight,
        "steps": [f"#### Stage {i}: {title}\n\n{body}" for i, (title, body) in enumerate(steps, 1)],
        "verification": verification, "accept": accept,
        "trouble": trouble, "cleanup": cleanup, "file": file,
    }


DATA = {
    "day": 127,
    "part1_intro": (
        "Day 127 turns the Day 126 Terraform baseline into a controlled change and recovery discipline. The object to protect is the binding "
        "between configuration addresses, Terraform state, and infrastructure observed by a provider. A normal plan refreshes tracked objects "
        "and proposes configuration changes; drift detection is evidence for an owner decision, not permission to overwrite the remote value or "
        "accept it into state. Import adds an existing object to one address after configuration and ownership are established. State recovery "
        "requires a stopped writer set, verified backup and backend identity, and a disposable rehearsal. The executable portion is deliberately "
        "local; the exercise labels provider-backed drift, cloud import and remote recovery as unproven where the environment does not exercise them."
    ),
    "exit_summary": (
        "A drift and recovery runbook, passing local Terraform validation/test evidence, an explicit policy fixture result, and documented state "
        "locking/versioning assumptions. Evidence distinguishes what the local built-in resource proves from what still requires an isolated "
        "provider-backed or remote-backend rehearsal."
    ),
    "part2_intro": (
        "The control path begins with reviewed HCL and a pinned tool/provider set, then validates the configuration and test assertions before "
        "a plan reads state and refreshes managed objects through provider APIs. A reviewer compares the plan with the intended owner-approved "
        "state. An import is a reviewed ownership adoption; a refresh-only apply records observed remote values in state, while a normal apply "
        "tries to converge infrastructure toward configuration. Recovery writes are a separate, exceptional path. The architecture below marks "
        "the local simulation and the remote backend boundary explicitly."
    ),
    "arch_table_html": '''<div class="table-container"><table><thead><tr><th>Boundary</th><th>Owner / mechanism</th><th>Observable evidence</th><th>Limit / trade-off</th></tr></thead><tbody>
<tr><td>Configuration validation and tests</td><td>Module owner declares input constraints, preconditions and test assertions; CI runs formatting, initialization, validation, tests and any policy checks.</td><td>Exit status, test names/results, reviewed source diff and saved plan artifact establish which checks ran.</td><td>Terraform validation checks syntax and internal consistency; it does not validate live APIs, backend permissions or remote objects. Tests can create resources unless mock/local fixtures are used.</td></tr>
<tr><td>State refresh and drift decision</td><td>Terraform core asks the configured provider to read tracked objects; service and infrastructure owners decide whether observed remote values or declared values are authoritative.</td><td>Plan shows out-of-band attribute changes, resource addresses, refresh diagnostics and proposed actions; ticket/policy evidence explains intended state.</td><td>Provider refresh sees only attributes it reads. A plan alone does not say whether a manual change was approved. Refresh-only apply writes state; normal apply may change infrastructure.</td></tr>
<tr><td>Import and ownership</td><td>Resource owner confirms unique remote identity; author writes the destination resource configuration and an import mapping; reviewer inspects the import plan and following convergence plan.</td><td>Destination address, exact provider-specific ID, single-owner check, import plan and post-import no-surprise plan.</td><td>Import adopts state ownership; it does not create complete configuration or prove no other state already manages the object. Some resource types do not support import.</td></tr>
<tr><td>Remote state and recovery</td><td>Backend owner controls bucket/key, execution identities, locking, object versioning, backup and recovery authorization; one writer per state operation.</td><td>Backend coordinates, lock owner/run ID, state lineage and serial, object generation/version, backup checksum and a rehearsed restore record.</td><td>Locking prevents concurrent Terraform writes only when supported and used. Version history helps recover object versions but does not establish correctness. A stale state push can detach or mis-map real objects.</td></tr>
<tr><td>Policy and delivery gates</td><td>Platform/security owners encode mandatory invariants in validation/policy checks and CI; reviewers retain responsibility for plan scope and exceptions.</td><td>Named policy assertions, positive and negative fixtures, CI result and exception owner/expiry.</td><td>Static policy covers only supplied plan/config data and may miss provider behavior or unmodeled attributes. GitOps reconciles declared desired state; it still needs ownership, drift and conflict policy.</td></tr>
<tr><td>Adjacent tools and legacy awareness</td><td>GitOps controllers reconcile repository manifests; Infrastructure Manager executes Terraform configurations on Google Cloud; Ansible/Packer handle configuration/image workflows; Deployment Manager is a legacy awareness item.</td><td>Tool boundary, state owner, reconciliation actor, handoff and decommission/compatibility decision are written down.</td><td>These tools have different execution and ownership models. Day 127 compares the boundaries only; it does not implement or deploy each system.</td></tr>
</tbody></table></div>''',
    "arch_diagram": {
        "type": "topology",
        "title": "Day 127 Terraform validation, drift decision and state recovery boundary",
        "desc": "Reviewed configuration and tests flow through validation and plan review. Provider refresh observes remote objects, after which owners decide whether to reconcile code, infrastructure, or state. Import adopts one verified object address. A separate state owner protects the remote backend with locking, object versions and rehearsed recovery. A local terraform_data lab is shown outside the remote API boundary.",
        "caption": "Figure 127.1: Terraform change and recovery control path. The local lab validates HCL and tests a built-in resource only; it does not prove Google provider refresh, GCS locking/IAM, real import or successful remote recovery.",
        "width": 1120, "height": 520,
        "layers": [
            {"name": "VERSIONED CONFIGURATION · TESTS · POLICY FIXTURES", "y": 24, "h": 78, "fill": "#102b46", "title_color": "#7dd3fc", "desc": "input constraints · ownership · assertions · pinned execution"},
            {"name": "VALIDATE · TEST · PLAN · REVIEW", "y": 133, "h": 78, "fill": "#073b33", "title_color": "#6ee7b7", "desc": "static checks · isolated assertions · refreshed plan · human decision"},
            {"name": "PROVIDER READ / APPLY · IMPORT ADOPTION", "y": 242, "h": 78, "fill": "#422006", "title_color": "#fdba74", "desc": "API observation · approved resource ownership · reviewed change"},
            {"name": "STATE BACKEND · SINGLE WRITER · LOCK · VERSION / BACKUP", "y": 351, "h": 78, "fill": "#27204b", "title_color": "#c4b5fd", "desc": "identity · lineage/serial · object generation · recovery rehearsal"},
            {"name": "EVIDENCE · RUNBOOK · BOUNDED HANDOFF", "y": 460, "h": 44, "fill": "#3b182c", "title_color": "#fda4af", "desc": "pass/fail results · decision owner · known limits"},
        ],
        "components": [
            {"x": 55, "y": 42, "w": 250, "h": 42, "name": "HCL + lock file", "detail": "desired values · addresses", "stroke": "#38bdf8"},
            {"x": 370, "y": 42, "w": 250, "h": 42, "name": "Tests + policy", "detail": "positive / negative fixtures", "stroke": "#38bdf8"},
            {"x": 690, "y": 42, "w": 260, "h": 42, "name": "CI identity", "detail": "least privilege · pinned CLI", "stroke": "#38bdf8"},
            {"x": 55, "y": 150, "w": 245, "h": 42, "name": "Validate + test", "detail": "static + local assertions", "stroke": "#22c55e"},
            {"x": 370, "y": 150, "w": 250, "h": 42, "name": "Refreshed plan", "detail": "config / state / remote diff", "stroke": "#22c55e"},
            {"x": 690, "y": 150, "w": 270, "h": 42, "name": "Owner review", "detail": "accept · correct · investigate", "stroke": "#22c55e"},
            {"x": 55, "y": 259, "w": 245, "h": 42, "name": "Local exercise", "detail": "terraform_data only", "stroke": "#f59e0b"},
            {"x": 370, "y": 259, "w": 250, "h": 42, "name": "Provider boundary", "detail": "read · apply · import", "stroke": "#f59e0b"},
            {"x": 690, "y": 259, "w": 270, "h": 42, "name": "Remote object", "detail": "not contacted by local lab", "stroke": "#f59e0b"},
            {"x": 55, "y": 368, "w": 245, "h": 42, "name": "State identity", "detail": "backend · key · lineage", "stroke": "#a78bfa"},
            {"x": 370, "y": 368, "w": 250, "h": 42, "name": "Lock + writer", "detail": "run ownership · stop gate", "stroke": "#a78bfa"},
            {"x": 690, "y": 368, "w": 270, "h": 42, "name": "Recovery source", "detail": "version · backup · checksum", "stroke": "#a78bfa"},
            {"x": 200, "y": 467, "w": 280, "h": 30, "name": "Runbook", "detail": "safe decision sequence", "stroke": "#f472b6"},
            {"x": 570, "y": 467, "w": 340, "h": 30, "name": "Acceptance pack", "detail": "tests · state assumptions · gaps", "stroke": "#f472b6"},
        ],
        "flows": [
            {"x1": 305, "y1": 63, "x2": 370, "y2": 63, "label": "assert", "type": "ok"},
            {"x1": 620, "y1": 63, "x2": 690, "y2": 63, "label": "run", "type": "ok"},
            {"x1": 300, "y1": 171, "x2": 370, "y2": 171, "label": "checks", "type": "ok"},
            {"x1": 620, "y1": 171, "x2": 690, "y2": 171, "label": "decide", "type": "ok"},
            {"x1": 300, "y1": 280, "x2": 370, "y2": 280, "label": "local only", "type": "warn"},
            {"x1": 620, "y1": 280, "x2": 690, "y2": 280, "label": "authorized API", "type": "warn"},
            {"x1": 300, "y1": 389, "x2": 370, "y2": 389, "label": "exclusive lock", "type": "ok"},
            {"x1": 620, "y1": 389, "x2": 690, "y2": 389, "label": "verified restore", "type": "ok"},
            {"x1": 480, "y1": 482, "x2": 570, "y2": 482, "label": "retain", "type": "ok"},
            {"x1": 815, "y1": 192, "x2": 815, "y2": 242, "label": "owner approval", "type": "warn"},
            {"x1": 495, "y1": 301, "x2": 495, "y2": 351, "label": "state write", "type": "ok"},
        ],
        "boundaries": [
            {"x": 40, "y": 121, "w": 1015, "h": 105, "label": "DECISION BOUNDARY · DETECTED DRIFT DOES NOT IDENTIFY THE AUTHORITATIVE VALUE"},
            {"x": 40, "y": 339, "w": 1015, "h": 102, "label": "RECOVERY BOUNDARY · STOP WRITERS AND VERIFY BACKUP / LINEAGE BEFORE ANY STATE WRITE"},
        ],
        "probes": [
            {"cx": 1058, "cy": 103, "label": "P1: exact CLI / test / policy result", "color": "#38bdf8"},
            {"cx": 1058, "cy": 231, "label": "P2: compare owner intent and refreshed evidence", "color": "#f59e0b"},
            {"cx": 1058, "cy": 344, "label": "P3: check lock, lineage, serial, object version", "color": "#a78bfa"},
        ],
    },
    "part3_intro": (
        "The case below is a synthetic Brightloaf fixture, not a reported production incident. Supplied facts are stated separately from "
        "inference. The evidence supports a safe investigation path but is insufficient to decide whether an emergency firewall value should "
        "be kept or reverted. That distinction matters: drift is a difference among desired configuration, state, and provider-observed object, "
        "while root cause and approved intent require ownership records beyond Terraform output."
    ),
    "part4_intro": (
        "The eight-stage exercise uses a local Terraform root with the built-in terraform_data resource, a terraform test file, a small Python "
        "policy fixture, and explicitly synthetic drift/recovery records. Stages 1–5 produce executable validation and test evidence; stages 6–7 "
        "run bounded negative cases and reason through an import and copied-state recovery record; Stage 8 destroys only the local object. No "
        "Google provider, backend, state push, force-unlock or real out-of-band change is part of this exercise."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Terraform state recovery, drift reconciliation, safe import, validation, policy checks and tests",
            "overview": (
                "Terraform uses configuration to describe intended resources, state to bind resource addresses to object identities, and a "
                "provider to observe and manage remote objects. Validation catches malformed or inconsistent configuration; tests assert "
                "specific behavior; policy checks enforce organization invariants over the data they receive. These belong together today because "
                "a successful baseline can still be unsafe when an operator cannot distinguish drift from intended change or cannot recover "
                "state safely. Configuration owners define desired values and resource addresses; provider owners define what can be read/imported; "
                "backend owners control locking and recovery; service owners resolve intent. GitOps, Infrastructure Manager, Ansible/Packer and "
                "Deployment Manager have different reconciliation and ownership boundaries, so this day compares them without implementing them."
            ),
            "preview": "A refreshed plan reports ingress changed from 10.20.0.0/16 to 0.0.0.0/0 while the emergency ticket has no owner or effective-policy export. Choosing the wrong value could either reopen public access or erase an approved recovery path.",
            "technical": """## Three-way reconciliation: configuration, state, and observed object

Terraform's normal planning flow compares configuration with state and refreshes tracked objects through the configured provider. A changed remote attribute can appear as drift, but the plan shows a difference, not the reason or authorization behind it. The provider can report only fields it reads; unconfigured or untracked objects and provider/API outages limit visibility. Capture the selected workspace/backend, resource address, provider diagnostics, state lineage/serial and the plan before deciding. Refresh-only planning is a review of proposed state updates; only applying that plan writes refreshed values into state. A normal apply instead proposes to make remote objects match configuration. Neither operation is a substitute for the service owner deciding which state is intended.

If an out-of-band change is approved and must remain, update reviewed configuration to encode that intent, then plan again and verify no unintended actions. If it is unauthorized, follow the incident owner’s containment and rollback decision, review the plan, and correct the object only under the applicable change controls. If evidence is incomplete, pause writes. Terraform's deprecated `refresh` command automatically commits refreshed state; prefer reviewable refresh-only planning. A failed read can also look like absence, so verify identity, credentials, region/project and provider diagnostics before interpreting removals.

## Validation, tests, and policy checks

Formatting normalizes source; backend-disabled initialization can prepare a module without connecting to a configured backend; validation checks syntax and internal consistency but not provider APIs, remote permissions or resource state. Planning supplies run-context validation and refresh. Terraform test files (`.tftest.hcl` or `.tftest.json`) can exercise module behavior using plan/apply runs and assertions; tests may create billable infrastructure unless they use isolated mock/local resources, and Terraform attempts cleanup of test resources after each file. Precondition/postcondition/check blocks express assertions in configuration, while external policy gates can enforce broader organization rules. Each gate needs positive and negative fixtures and an owner for exceptions. A green static check cannot prove a live policy works unless a live boundary is tested.

## Safe import and unique ownership

Import adopts an existing remote object into one Terraform address. First verify the exact backend and object ID, establish that no other state or tool claims it, write the destination resource configuration, then plan the import and inspect all resulting changes before applying. The CLI import command maps state but does not author configuration; declarative import blocks make the mapping reviewable in a plan. Import support and identifiers are resource-provider-specific. A subsequent plan is required to find defaults or omitted attributes that would otherwise cause an update or replacement. Import does not prove the imported object is correct, nor that another system has stopped reconciling it.

## State recovery, locking, and recovery evidence

Before state recovery, stop or fence every writer, identify backend/bucket/prefix/workspace, record the lock owner, pull a fresh backup, and preserve lineage, serial, object generation/version and checksums. Compare the candidate version to a known-good plan and object inventory in a disposable copy. Confirm the restore is for the same state lineage and resource ownership before considering a write; capture approval, operator identity and rollback procedure. GCS backend documentation recommends Object Versioning to recover from accidental deletion or human error and supports state locking, but versioning alone neither validates a candidate nor prevents an authorized bad write. A forced state overwrite bypasses safeguards and is not routine; manually releasing a lock can permit concurrent writers if lock ownership is misunderstood. Never point this exercise at a shared backend.

## Operational alternatives and limits

GitOps controllers continuously reconcile repository manifests against clusters; they introduce controller and source-of-truth ownership questions that differ from a one-shot Terraform plan. Google Cloud Infrastructure Manager runs Terraform configurations as a managed service and changes execution/state operations, so verify its current service lifecycle and ownership boundary before adoption. Ansible commonly orchestrates configuration and procedural tasks; Packer builds machine images. Legacy Deployment Manager is an awareness topic for migration/compatibility decisions, not a new implementation choice here. Mixing tools against the same object without an explicit single-owner handoff creates competing reconciliation loops.

The local lab exercises `terraform_data`, Terraform validation/tests, a Python policy fixture and a synthetic state comparison. It does not invoke a Google provider, mutate an object out of band, prove GCS locking/IAM, execute a real import, or push recovered state. A provider-backed rehearsal must be isolated, disposable, explicitly authorized, backed up and cleaned up separately.

References: [Terraform test command and cleanup behavior](https://developer.hashicorp.com/terraform/cli/commands/test), [terraform validate scope](https://developer.hashicorp.com/terraform/cli/commands/validate), [Terraform plan and refresh-only mode](https://developer.hashicorp.com/terraform/cli/commands/plan), [Recover state from backup](https://developer.hashicorp.com/terraform/cli/state/recover), [GCS backend locking and object versioning](https://developer.hashicorp.com/terraform/language/backend/gcs), [Import existing resources](https://developer.hashicorp.com/terraform/cli/import), and [Google Cloud Terraform API and import overview](https://docs.cloud.google.com/docs/terraform/understanding-apis-and-terraform). All accessed 2026-09-29.""",
            "questions": [
                "Which backend, workspace, project, provider identity, address, lineage, serial and remote object version were used to create this plan?",
                "Does the service owner accept the remotely observed value, require Terraform to restore configuration, or need more evidence before choosing?",
                "Can the proposed import ID be tied to one object and one Terraform address, with the next plan free of surprise replacement?",
                "Which writer is fenced, which backup version is known good, and what exact evidence authorizes any recovery write?",
                "Which assertions run as static validation, local test, mock test, policy fixture or live provider check—and what does each leave unproven?",
            ],
            "reference": "https://developer.hashicorp.com/terraform/cli/commands/plan",
            "reference_label": "Terraform plan command, normal and refresh-only planning modes (accessed 2026-09-29)",
            "scenario": {
                "scenario": "Synthetic supplied fixture: a Brightloaf plan proposes changing firewall ingress from `10.20.0.0/16` to `0.0.0.0/0`. A change ticket says an emergency access change may have been made, but the ticket ID, approver, timestamp and effective firewall policy export are absent. The selected backend, resource owner and state metadata are also not supplied. No plan apply or production outcome is established.",
                "impact": "Automatically restoring the narrower CIDR could disrupt an approved recovery action; accepting the wider CIDR could preserve unintended public access. A state restore or import against the wrong backend could break Terraform's mapping to live resources.",
                "constraints": "Preserve availability and least privilege; no real policy edit, import, refresh-only apply, state push or force-unlock is authorized by the fixture. Obtain service, security and state-owner evidence before any write.",
                "evidence": "Fixture facts: configuration contains `10.20.0.0/16`; plan reports remote `0.0.0.0/0`; a ticket mentions possible emergency action. Missing: ticket ID/owner/time, effective policy export, active backend identity, lineage/serial, plan provenance and writer inventory.",
                "root": "Root cause is undetermined. The proposed delta could reflect approved emergency access, an unauthorized change, a configuration regression, an incorrect target/backend, or a provider observation issue. The supplied plan difference cannot distinguish these possibilities.",
                "diagnostic_steps": [
                    "Pause Terraform writers and preserve the original plan/logs; verify account, project, backend key, workspace, provider identity and resource address without changing state.",
                    "Ask the incident commander, network owner and security approver for ticket ID, timeline, intended CIDR, effective firewall policy and any containment action; compare rule direction, target, priority and source ranges.",
                    "Read state lineage/serial and object generation/version, last successful run and reviewed source/plan history; identify every active writer and mark unavailable fields unknown.",
                ],
                "remediation_steps": [
                    "Keep writes paused until owners establish intent and target identity. Do not accept refresh-only state or run normal apply solely to make the diff disappear.",
                    "If the broader rule is approved and should persist, update reviewed configuration to that explicitly authorized value; if it is unauthorized, follow the incident owner's approved containment and correction plan. If unresolved, preserve service/security escalation and make no Terraform write.",
                    "For a separate recovery rehearsal, use a disposable copied state, fenced writers, recorded lineage/serial and verified candidate backup; compare object inventory and the resulting plan before considering a restore.",
                ],
                "verify": "The operational decision is acceptable only when an owner-approved ticket and effective policy establish intended ingress, the reviewed plan targets the verified backend/address and contains no unrelated actions, and a post-change policy check confirms the intended rule. For state recovery, require an isolated copy rehearsal, lineage/serial and version comparison, checksum, lock/writer evidence, approval and post-restore plan. None of those live checks are performed here.",
                "residual": "The fixture supplies no live policy, ticket owner, backend coordinates, state metadata, provider logs or change outcome. It cannot establish whether the public CIDR exists, whether the emergency action was authorized, or whether any state version is safe to restore.",
                "diagram": ["Plan displays a wider ingress value", "Ticket and policy evidence do not establish intent", "Blind reconcile may expose or interrupt service", "Pause writers and identify owner-approved state", "Change only after narrow plan and policy verification"],
                "facts": "Only the two CIDRs and the incomplete-ticket note are supplied synthetic facts; missing identifiers and runtime outcomes remain unknown.",
                "inference": "A manual emergency action is plausible but unproven. Neither the plan nor the ticket note alone determines root cause or the safe target value.",
                "expected": "A no-write decision record, an explicit evidence request list, one named decision owner per gap, and a bounded disposable recovery rehearsal plan.",
            },
            "lab": lab(
                "Detect a synthetic drift signal and rehearse a safe state decision",
                "Run local Terraform validation and tests against a built-in resource, evaluate a policy fixture, then process a fixed drift/import/recovery dataset into a no-write decision and recovery checklist.",
                "A local HCL validation/test transcript, positive and negative policy results, configuration-versus-state comparison, safe import decision, copied-state recovery rehearsal record and cleanup confirmation.",
                "Day 126 local Terraform module/state artifact; Terraform CLI 1.7 or newer for the supplied test syntax; Python 3 standard library; editor and shell. No Google Cloud account or credentials are needed.",
                "Create a new disposable directory. Run `terraform version` and `python3 --version`; stop if Terraform is older than 1.7 or a backend/provider block is added. The exercise uses only built-in `terraform_data`, local state, synthetic records and Python. Never add a Google provider, GCS backend, credential or real resource ID. Stage 1 records tool versions and confirms an empty starting directory.",
                [
                    ("Preflight tools and prove the workspace is isolated", "Create the exercise root and record actual tool versions. The expected observation is Terraform >=1.7, Python 3, an empty new working directory, and no cloud identity/backend configured. If Terraform is unavailable or too old, retain a blocked-tool note and do not silently install or switch tools.\n\n```sh\nmkdir -p day127-drift-recovery/tests\ncd day127-drift-recovery\nterraform version\npython3 --version\ntest -z \"$(find . -mindepth 1 -maxdepth 1 -print -quit)\" && echo 'PASS: empty isolated exercise root'\n```"),
                    ("Prepare local configuration and the synthetic case inputs", "Write a no-provider root using Terraform's built-in `terraform_data`; this makes one local state object and no cloud object. The fixed drift fixture deliberately records the configuration value, observed value and unknown approval separately.\n\n```sh\ncat > main.tf <<'EOF'\nterraform {\n  required_version = \">= 1.7.0, < 2.0.0\"\n}\n\nvariable \"environment\" {\n  type    = string\n  default = \"lab\"\n  validation {\n    condition     = contains([\"lab\", \"test\"], var.environment)\n    error_message = \"environment must be lab or test\"\n  }\n}\n\nresource \"terraform_data\" \"exercise\" {\n  input = {\n    environment = var.environment\n    owner       = \"day127-local-lab\"\n    revision    = 1\n  }\n}\n\noutput \"exercise_owner\" {\n  value = terraform_data.exercise.output.owner\n}\nEOF\ncat > drift-fixture.json <<'EOF'\n{\n  \"resource_address\": \"google_compute_firewall.brightloaf_ingress\",\n  \"configuration_cidr\": \"10.20.0.0/16\",\n  \"provider_observed_cidr\": \"0.0.0.0/0\",\n  \"ticket_id\": null,\n  \"approver\": null,\n  \"effective_policy_export\": null,\n  \"backend_identity\": null,\n  \"decision\": \"undetermined\"\n}\nEOF\n```"),
                    ("Author test assertions and an explicit policy check", "The test assertion exercises a positive local plan; the Python policy fixture has a positive and a negative case for a forbidden public ingress. It tests the rule logic over supplied JSON only, not a Terraform plan or live firewall.\n\n```sh\ncat > tests/exercise.tftest.hcl <<'EOF'\nrun \"lab_resource_has_expected_owner\" {\n  command = plan\n\n  assert {\n    condition     = terraform_data.exercise.input.owner == \"day127-local-lab\"\n    error_message = \"exercise owner must stay local to this lab\"\n  }\n\n  assert {\n    condition     = terraform_data.exercise.input.environment == \"lab\"\n    error_message = \"default target must remain lab\"\n  }\n}\nEOF\ncat > check_policy.py <<'EOF'\nimport json\nimport sys\n\nwith open(sys.argv[1], encoding=\"utf-8\") as source:\n    case = json.load(source)\n\nallowed = case[\"provider_observed_cidr\"] == case[\"configuration_cidr\"]\nif case.get(\"decision\") != \"approved\":\n    allowed = False\nprint(f\"policy_allowed={str(allowed).lower()} decision={case['decision']} observed={case['provider_observed_cidr']}\")\nraise SystemExit(0 if allowed else 2)\nEOF\ncat > policy-approved.json <<'EOF'\n{\n  \"configuration_cidr\": \"10.20.0.0/16\",\n  \"provider_observed_cidr\": \"10.20.0.0/16\",\n  \"decision\": \"approved\"\n}\nEOF\n```"),
                    ("Initialize locally, validate, test, and execute one bounded apply", "Run only local backend initialization. Review the exact root first: the only resource must be built-in `terraform_data.exercise`; there must be no provider requirement, backend block or import block. Then run formatting, validation and tests before the local apply. Expected: validation succeeds, the named test passes, and the plan/apply contains one local resource. Do not interpret this as provider-backed drift evidence.\n\n```sh\nterraform fmt -check -recursive\nterraform init -backend=false\nterraform validate\nterraform test\nterraform plan -out=baseline.tfplan\nterraform show baseline.tfplan\nterraform apply baseline.tfplan\nterraform output -raw exercise_owner\nprintf '\\n'\n```"),
                    ("Inspect state and run the policy fixture", "List the single local address and inspect its state. Run the policy checker on the synthetic emergency case; expected exit 2 and `policy_allowed=false decision=undetermined`. Then run the approved exact-match fixture; expected exit 0 and `policy_allowed=true`. These are Python fixture results, not provider policy enforcement.\n\n```sh\nterraform state list\nterraform state show terraform_data.exercise\npython3 check_policy.py drift-fixture.json; test \"$?\" -eq 2 && echo 'PASS: unresolved drift fails closed'\npython3 check_policy.py policy-approved.json\n```"),
                    ("Challenge invalid input, drift acceptance, and import ownership", "Run a bounded invalid-input plan and confirm it fails validation before apply. For the tabletop drift case, fill the decision note from the exact fixture: observed CIDR differs, ticket/approver/export/backend are unknown, so disposition stays `undetermined` and no write is permitted. For import, record the destination address and the fictional exercise ID shown in the command example, and ownership check `unknown`; therefore do not run import. State that import would require matching configuration, unique ownership, provider-supported ID, reviewed import plan and follow-up plan.\n\n```sh\nif terraform plan -var='environment=prod'; then\n  echo 'ERROR: invalid environment unexpectedly passed'\n  exit 1\nelse\n  echo 'PASS: invalid environment rejected before apply'\nfi\ncat > day127-decision.md <<'EOF'\nClassification: synthetic drift signal; root cause and authoritative value undetermined.\nSupplied: configuration CIDR 10.20.0.0/16; provider observation 0.0.0.0/0; ticket note says emergency action may have happened.\nMissing: ticket ID/approver/time; effective policy export; backend identity; state lineage/serial; unique object owner.\nDecision: pause writes; no normal apply, refresh-only apply, import, state push, or force-unlock.\nImport destination: google_compute_firewall.brightloaf_ingress\nFictional exercise ID: projects/brightloaf-test/global/firewalls/edge-allow\nImport gate: unique owner and target not verified; fictional ID must never be used against a real provider.\nEOF\n```"),
                    ("Diagnose drift evidence and rehearse recovery on a synthetic copy", "Use the supplied recovery record below. Calculate the serial difference and compare lineage and object generation; record that matching lineage and a lower serial do not by themselves prove that a version reflects current remote inventory. Since writer-stop, object inventory, checksum approval and restore-run evidence are absent, decide `do not push`; rehearse comparison on a copy only. Run the assessment script, then append the six recovery gates and evidence limits to the decision record. The expected result is all remote recovery gates remain unproven, so no state write or unlock is allowed.\n\n```sh\ncat > recovery-fixture.json <<'EOF'\n{\n  \"backend\": \"gs://bl-state-example/terraform/test\",\n  \"writers_fenced\": false,\n  \"candidate\": {\"lineage\": \"L-test\", \"serial\": 8, \"object_generation\": \"104\", \"sha256\": \"candidate-checksum-unverified\"},\n  \"known_good\": {\"lineage\": \"L-test\", \"serial\": 7, \"object_generation\": \"101\", \"sha256\": \"backup-checksum-unverified\"},\n  \"inventory_compared\": false,\n  \"owner_approval\": false\n}\nEOF\ncat > assess_recovery.py <<'EOF'\nimport json\n\nwith open(\"recovery-fixture.json\", encoding=\"utf-8\") as source:\n    item = json.load(source)\na, b = item[\"candidate\"], item[\"known_good\"]\nchecks = {\n    \"same_lineage\": a[\"lineage\"] == b[\"lineage\"],\n    \"candidate_serial_newer\": a[\"serial\"] > b[\"serial\"],\n    \"writers_fenced\": item[\"writers_fenced\"],\n    \"inventory_compared\": item[\"inventory_compared\"],\n    \"owner_approval\": item[\"owner_approval\"],\n}\nprint(\"checks=\" + json.dumps(checks, sort_keys=True))\nprint(\"decision=DO_NOT_PUSH; rehearsal only on a separate copy\")\nEOF\npython3 assess_recovery.py\ncat >> day127-decision.md <<'EOF'\nRecovery gates: backend identity=unknown; writers/lock=not fenced; backup checksum=unverified; lineage/serial/version=fixture only; owner approval=absent; inventory/post-restore plan=not run.\nDisposition: no state write or unlock. A real rehearsal must use a separately isolated copied backend/state and named recovery approver.\nLocal evidence: record actual CLI version, validation/test results, plan/apply result, policy fixture exit codes, invalid-input failure, state address, and cleanup result.\nLimits: no Google provider refresh, no real out-of-band mutation/import, no GCS/IAM/locking/version test, no remote recovery.\nEOF\nsed -n '1,200p' day127-decision.md\n```"),
                    ("Destroy the local fixture and close the evidence pack", "Destroy only the single local `terraform_data.exercise` object, confirm state has no addresses, and preserve the source files plus redacted transcript as the exit artifact. Do not delete the accepted decision/runbook files. Expected: destroy reports one object removed and the following state listing prints no resource address.\n\n```sh\nterraform destroy -auto-approve\ntest -z \"$(terraform state list)\" && echo 'PASS: local exercise state is empty'\ncd ..\n```"),
                ],
                "Expected state: one local terraform_data object during the exercise; test assertion passes; invalid environment is rejected; unresolved policy fixture fails closed with exit 2; approved exact-match policy fixture passes; recovery assessment says DO_NOT_PUSH; after cleanup local state is empty. Capture actual outputs. Successful validation and tests do not prove provider, remote backend, live policy or recovery behavior.",
                "Accept `day127-drift-recovery-runbook.md` with actual tool versions and command statuses; formatted/validated configuration and passing Terraform test; policy positive/negative evidence; fact-versus-inference drift record; safe import gate; six recovery gates and lock/versioning assumptions; explicit no-write decision; and cleanup confirmation. Include files `main.tf`, `tests/exercise.tftest.hcl`, `check_policy.py`, fixtures, `day127-decision.md`, and redacted transcript. Map to Exit evidence: drift/recovery runbook, passing validation evidence and documented locking/versioning assumptions.",
                "If the Terraform test file syntax is rejected, check CLI version against the preflight gate. If initialization requests a provider, inspect main.tf for a non-built-in resource or provider block and stop before downloading. A refresh-only plan against this local fixture would not model a real provider read; do not describe it as cloud drift detection. A failed policy check is expected on `undetermined`; exit 2 is the deliberate reject signal. Never run fixture IDs with gcloud or a provider, never force a state overwrite, and never release an unknown lock.",
                "Destroy the local resource from the isolated exercise root and verify the state listing is empty. Keep the accepted source, decision, fixture and redacted evidence outside the transient Terraform directory if needed. No cloud resource, remote state, API enablement, paid service or credential is used.",
                "day-127-drift-recovery-runbook.md",
            ),
        }
    ],
}
