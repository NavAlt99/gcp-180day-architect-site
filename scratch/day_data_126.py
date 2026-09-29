"""Day 126 Terraform baseline and state boundaries.

All cases are synthetic. The runnable Terraform lab uses only Terraform's
built-in terraform_data resource and local state; GCS/IAM scenarios are tabletop.
"""

DAY_NUM = 126


def lab(name, goal, expected, prereq, preflight, steps, verification, accept, trouble, cleanup, file):
    return {
        "name": name,
        "goal": goal,
        "expected": expected,
        "mode": "Local Terraform CLI with built-in terraform_data and local state; remote GCS design is tabletop; no cloud resources or spend",
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
    "day": 126,
    "part1_intro": (
        "Day 126 establishes a small, reviewable Terraform baseline before the curriculum moves to testing, drift and recovery on Day 127. "
        "The useful unit is not a pile of HCL: it is a versioned configuration whose provider selection, inputs, outputs, module boundary, "
        "plan and state ownership can be explained. We use a local built-in resource for executable evidence, then reason explicitly about "
        "what changes when state moves to a Google Cloud Storage backend. Terraform state can contain sensitive values and determines which "
        "real objects a plan may change, so environment isolation, access and recovery are architectural concerns. All Brightloaf examples and "
        "values on this page are synthetic teaching fixtures, not production observations."
    ),
    "exit_summary": (
        "A versioned minimal Terraform module, successful local validation and plan/apply/recreation evidence, plus a redacted environment/state "
        "isolation diagram that identifies GCS bucket and prefix boundaries, state writers/readers, locking, versioning and import ownership. "
        "No cloud resource is created; remote backend decisions are documented as design evidence."
    ),
    "part2_intro": (
        "Follow the path from HCL and pinned dependencies through module inputs, provider operations, plan review and state persistence. "
        "Terraform configuration describes desired objects; providers translate resource blocks to APIs; state maps configuration addresses "
        "to remote identities and records values used for future plans. A plan is a proposed change based on refreshed remote observations and "
        "state, not a guarantee that apply will succeed or that an unreviewed target is safe. The diagram separates a local practice run from "
        "the remote GCS control and recovery boundary."
    ),
    "arch_table_html": '''<div class="table-container"><table><thead><tr><th>Boundary</th><th>Owner / mechanism</th><th>Observable evidence</th><th>Limit / decision</th></tr></thead><tbody>
<tr><td>Root module and providers</td><td>Configuration owner declares Terraform CLI constraints, provider source/version constraints, provider configuration and root inputs. Reusable child modules declare their own provider requirements.</td><td>Dependency initialization resolves providers; the committed <code>.terraform.lock.hcl</code> records selected builds; configuration validation checks structure.</td><td>Version constraints and lock files solve different jobs: constraints describe compatible versions; the lock file records selections. They do not make an unreviewed provider trustworthy or pin remote module sources automatically.</td></tr>
<tr><td>Resource graph and plan</td><td>Terraform core evaluates expressions and dependencies; provider schemas plan resource-specific changes. Reviewers own target identity, destructive-change scrutiny and approval.</td><td>Plan reports create/update/destroy actions, values known after apply and dependencies. A saved plan can be inspected and applied as a reviewed artifact.</td><td>Plan is based on current inputs, provider behavior and refresh results. Remote changes can occur after planning; the apply still needs correct identity, authorization and API availability.</td></tr>
<tr><td>Module boundary</td><td>Root module passes typed inputs to child module; child exposes a deliberate output surface and owns its internal resource addresses.</td><td>Inputs, validation, outputs and resource addresses are visible in version control; callers depend on outputs instead of reaching into module internals.</td><td>Modules do not isolate state by themselves. Multiple modules in one root normally share that root configuration's state and blast radius.</td></tr>
<tr><td>State and environment isolation</td><td>One state owner and backend key/prefix per independently governed environment or stack. GCS bucket IAM and prefix organization constrain access; backend supports state locking.</td><td>Backend identity, prefix, principal set, lock behavior, object version history and state serial are documented and checked before writes.</td><td>Prefix is a naming boundary, not a substitute for bucket IAM. Workspaces can separate state instances but do not automatically provide authorization or distinct credentials.</td></tr>
<tr><td>Import and ownership transfer</td><td>Resource owner first writes matching configuration, then imports the real object to one intended Terraform address and reviews the next plan.</td><td>Import changes Terraform's state mapping; the following plan should show no unintended replacement or deletion and should reconcile configuration with the actual object.</td><td>Import does not generate a complete desired configuration in every workflow and does not prove ownership is exclusive. Concurrent tools or duplicate state entries can cause conflicting writes.</td></tr>
</tbody></table></div>''',
    "arch_diagram": {
        "type": "topology",
        "title": "Day 126 Terraform configuration, plan, and state ownership boundaries",
        "desc": "A versioned root module declares provider requirements, variables, child module inputs and outputs. Terraform core and the provider produce a reviewed plan before apply. The resulting state is either local disposable practice state or, in a separate architecture, a GCS backend with a distinct environment prefix, IAM writers, locking and object version history.",
        "caption": "Figure 126.1: Conceptual ownership path for a Terraform change and its state. The local lab does not exercise GCS locking, IAM or recovery; the diagram does not prove remote permissions, isolation or successful apply.",
        "width": 1120, "height": 600,
        "layers": [
            {"name": "VERSIONED INPUT · CLI / PROVIDER CONSTRAINTS · REVIEWED CODE", "y": 24, "h": 86, "fill": "#102b46", "title_color": "#7dd3fc", "desc": "root module · variables · child module contract · lock file"},
            {"name": "TERRAFORM CORE · GRAPH · REFRESH · PLAN REVIEW", "y": 145, "h": 86, "fill": "#073b33", "title_color": "#6ee7b7", "desc": "evaluate dependencies and compare declared, state and observed objects"},
            {"name": "PROVIDER API BOUNDARY · APPLY ONLY AFTER TARGET AND PLAN REVIEW", "y": 266, "h": 86, "fill": "#422006", "title_color": "#fdba74", "desc": "provider identity and permissions determine which remote objects can change"},
            {"name": "STATE OWNER · ENVIRONMENT KEY · LOCK · VERSIONED RECOVERY", "y": 387, "h": 86, "fill": "#27204b", "title_color": "#c4b5fd", "desc": "local exercise state or separately protected GCS bucket and prefix"},
            {"name": "ACCEPTANCE · REPRODUCIBLE PLAN · OWNERSHIP / LIMITS RECORDED", "y": 508, "h": 70, "fill": "#3b182c", "title_color": "#fda4af", "desc": "configuration, plan, state boundary and next verification handoff"},
        ],
        "components": [
            {"x": 55, "y": 48, "w": 230, "h": 46, "name": "Root configuration", "detail": "required_version · inputs", "stroke": "#38bdf8"},
            {"x": 355, "y": 48, "w": 220, "h": 46, "name": "Provider lock", "detail": "source · constraint · checksum", "stroke": "#38bdf8"},
            {"x": 650, "y": 48, "w": 260, "h": 46, "name": "Child module", "detail": "typed input · output contract", "stroke": "#38bdf8"},
            {"x": 55, "y": 169, "w": 250, "h": 46, "name": "Terraform graph", "detail": "addresses · dependencies", "stroke": "#22c55e"},
            {"x": 380, "y": 169, "w": 250, "h": 46, "name": "Refresh + plan", "detail": "proposed create/update/delete", "stroke": "#22c55e"},
            {"x": 700, "y": 169, "w": 260, "h": 46, "name": "Human review", "detail": "identity · scope · blast radius", "stroke": "#22c55e"},
            {"x": 55, "y": 290, "w": 250, "h": 46, "name": "Local lab", "detail": "terraform_data only", "stroke": "#f59e0b"},
            {"x": 380, "y": 290, "w": 250, "h": 46, "name": "Provider operation", "detail": "no cloud provider in lab", "stroke": "#f59e0b"},
            {"x": 700, "y": 290, "w": 260, "h": 46, "name": "Remote boundary", "detail": "API identity · authorization", "stroke": "#f59e0b"},
            {"x": 55, "y": 411, "w": 250, "h": 46, "name": "dev / test prefix", "detail": "separate state ownership", "stroke": "#a78bfa"},
            {"x": 380, "y": 411, "w": 250, "h": 46, "name": "GCS backend", "detail": "locking · object versions", "stroke": "#a78bfa"},
            {"x": 700, "y": 411, "w": 260, "h": 46, "name": "IAM boundary", "detail": "named state writers/readers", "stroke": "#a78bfa"},
            {"x": 200, "y": 525, "w": 280, "h": 40, "name": "Saved evidence", "detail": "config · plan · recreate result", "stroke": "#f472b6"},
            {"x": 570, "y": 525, "w": 340, "h": 40, "name": "Handoff", "detail": "redacted isolation diagram · caveats", "stroke": "#f472b6"},
        ],
        "flows": [
            {"x1": 285, "y1": 71, "x2": 355, "y2": 71, "label": "resolve", "type": "ok"},
            {"x1": 575, "y1": 71, "x2": 650, "y2": 71, "label": "pass input", "type": "ok"},
            {"x1": 305, "y1": 192, "x2": 380, "y2": 192, "label": "evaluate", "type": "ok"},
            {"x1": 630, "y1": 192, "x2": 700, "y2": 192, "label": "review", "type": "ok"},
            {"x1": 305, "y1": 313, "x2": 380, "y2": 313, "label": "plan", "type": "ok"},
            {"x1": 630, "y1": 313, "x2": 700, "y2": 313, "label": "authorized API", "type": "warn"},
            {"x1": 305, "y1": 434, "x2": 380, "y2": 434, "label": "backend object", "type": "ok"},
            {"x1": 630, "y1": 434, "x2": 700, "y2": 434, "label": "policy", "type": "ok"},
            {"x1": 480, "y1": 545, "x2": 570, "y2": 545, "label": "record", "type": "ok"},
            {"x1": 820, "y1": 215, "x2": 820, "y2": 290, "label": "approved apply", "type": "warn"},
            {"x1": 500, "y1": 336, "x2": 500, "y2": 411, "label": "state write", "type": "ok"},
        ],
        "boundaries": [
            {"x": 40, "y": 132, "w": 1015, "h": 110, "label": "PLAN BOUNDARY · PROPOSED CHANGE IS EVIDENCE FOR REVIEW, NOT A GUARANTEE OF SAFE APPLY"},
            {"x": 40, "y": 374, "w": 1015, "h": 108, "label": "STATE BOUNDARY · PREFIX NAMESPACING DOES NOT REPLACE IAM OR A RECOVERY POLICY"},
        ],
        "probes": [
            {"cx": 1058, "cy": 118, "label": "P1: confirm CLI, provider source and lock-file diff", "color": "#38bdf8"},
            {"cx": 1058, "cy": 250, "label": "P2: inspect target identity and every destructive plan action", "color": "#f59e0b"},
            {"cx": 1058, "cy": 380, "label": "P3: check writer set, environment prefix, lock and versions", "color": "#a78bfa"},
        ],
    },
    "part3_intro": (
        "These synthetic Brightloaf cases show how Terraform mistakes cross from code into operational ownership. Evidence is labeled as a "
        "supplied fixture; causal statements are hypotheses until confirmed by a controlled plan or backend inspection. Each incident separates "
        "symptoms, constraints, diagnosis, correction and residual uncertainty. No scenario claims a real production event."
    ),
    "part4_intro": (
        "Complete three topic exercises with explicit eight-stage execution. Exercise 1 uses Terraform's built-in terraform_data resource and "
        "a local state file so plan, apply, output, change and destroy are executable without Google Cloud credentials or provider downloads. "
        "Exercises 2 and 3 use exact synthetic records and worksheets to test state boundary and ownership reasoning without provisioning GCS, "
        "importing real resources, editing shared state or rehearsing a destructive cloud change. Each exercise produces an artifact for the "
        "Day 126 exit evidence; acceptance criteria follow its eight stages."
    ),
    "topics": [
        {
            "key": "topic-01", "title": "Terraform providers, resources, variables, outputs, modules and plan/apply",
            "overview": (
                "Terraform is a declarative infrastructure tool: a root module combines provider requirements, provider configuration, input "
                "variables, resources, child modules and outputs into a dependency graph. The plan command proposes operations from "
                "configuration, state and provider refresh; Apply performs an approved plan and updates state. This belongs today "
                "because later platform automation depends on a reproducible baseline and clear ownership. The root-module owner chooses target "
                "identity and reviews the complete plan; reusable child modules expose deliberate inputs and outputs. A module is a code boundary, "
                "not automatically an authorization or state boundary."
            ),
            "preview": "A plan unexpectedly proposes replacing a shared network because the caller passed the wrong environment input. A reviewed module interface and explicit target checks prevent a practice change from interrupting customer traffic.",
            "technical": """## Provider and configuration selection

Terraform core parses HCL and builds a dependency graph; provider plugins implement resource-specific planning and API operations. A root configuration declares the Terraform CLI version in `required_version`, provider source and accepted provider versions in `required_providers`, and the provider configuration used by resources. Initialization resolves providers and records selected checksums in `.terraform.lock.hcl`; commit that file for repeatable local or CI initialization. Constraints express a compatibility range; the lock file records selected builds. Reusable modules declare provider requirements but normally receive provider configurations from the root module.

## Variables, resources, modules and outputs

Input variables are the caller's typed contract. Validation can reject invalid values before provider operations. Resources represent managed objects; references between resources create graph dependencies, and explicit `depends_on` should be reserved for dependencies Terraform cannot infer from references. A child module packages configuration with declared inputs and outputs. It can reduce duplication and make interfaces reviewable, but it does not create a separate state file or IAM boundary. Outputs expose the minimum value callers need; mark sensitive outputs carefully, remembering that sensitivity redacts common display paths but does not remove the value from state.

## Plan and apply as a review gate

Format source, initialize dependencies, run structural validation, and plan with explicit environment inputs. Review the project/account/region, resource addresses, replacements and deletes, unknown-after-apply values, dependency changes and provider lock-file diff. For higher assurance, save the plan and apply that saved artifact after approval. A plan can become stale as infrastructure changes; provider/API failures or policy checks can still reject apply. Do not approve a plan solely because the summary says one change.

## Limits and ownership

Terraform state maps resource addresses to remote IDs and retains values needed to plan. Configuration and state can diverge; someone may change resources out of band. State sensitivity means code review alone is insufficient: restrict state access, avoid secrets in outputs, and treat local state and plan files as sensitive artifacts. Resource owners define lifecycle and service constraints; platform owners define provider sources, module patterns and execution identity; reviewers validate environment and impact. The local lab below proves Terraform language flow for a built-in resource only. It cannot prove Google provider behavior, API permissions or a real cloud plan.

References: [Terraform provider requirements and dependency lock file](https://developer.hashicorp.com/terraform/language/providers/requirements) and [Terraform resources and configuration](https://developer.hashicorp.com/terraform/language/resources/configure).""",
            "questions": [
                "Which exact root inputs determine the project, region, environment and resource name?",
                "Does the lock-file diff match the reviewed provider constraint change, and was initialization reproducible?",
                "Which planned replacements or deletes cross ownership boundaries, and who must approve them?",
                "Which data is persisted in state even if the CLI marks an output sensitive?",
            ],
            "reference": "https://developer.hashicorp.com/terraform/language/providers/requirements",
            "reference_label": "Terraform provider requirements and dependency lock file (accessed 2026-09-29)",
            "scenario": {
                "scenario": "Synthetic supplied fixture: a Brightloaf staging plan shows one replacement of a shared VPC and one subnet deletion. The developer intended to recreate a disposable local exercise resource; the plan was generated with an inherited production project variable. No apply occurred in this scenario.",
                "impact": "If approved, the replacement could sever service connectivity and the subnet deletion could disrupt workloads. An unexpected plan also weakens reviewer trust and delays a safe release.",
                "constraints": "Preserve the shared network and existing workloads; use a disposable local target for practice; one state owner per environment; do not claim an apply or outage occurred.",
                "evidence": "Synthetic plan fixture: target variable resolves to prod-project; one shared VPC replacement; one subnet deletion; intended change was local terraform_data exercise. No API call or apply evidence is supplied.",
                "root": "Likely control failure: the root input/environment selection was not verified before planning, and the reviewer lacked a target and destructive-action check. The plan output proves proposed changes for the selected context, not that any resource was changed.",
                "diagnostic_steps": [
                    "Read the effective workspace, backend and all variable sources; record the selected project/region/environment before reading individual actions.",
                    "Trace each replacement and deletion to its resource address, configuration diff, state address and provider-reported change reason.",
                    "Compare the intended exercise scope with the full plan; stop if any unrelated shared resource appears and regenerate only after the target is corrected.",
                ],
                "remediation_steps": [
                    "Use an explicit disposable root directory and explicit input file; reject any target outside the declared lab environment before planning.",
                    "Keep shared infrastructure in its own reviewed configuration and state ownership boundary; do not use broad shared-state plans for a small local exercise.",
                    "Require a reviewer to confirm target identity and inspect every replacement/deletion; preserve the original plan artifact and annotate why it was rejected.",
                ],
                "verify": "Re-run fmt, init, validate and plan from the intended local directory. The revised plan must contain only the expected terraform_data create or update; record the exact environment, address and action. No cloud provider or API call is involved.",
                "residual": "A clean local plan does not verify Google provider behavior, IAM, quotas, APIs, policy enforcement or concurrent cloud changes. A remote change can occur between plan and apply.",
                "diagram": ["Inherited variable selects production target", "Plan includes VPC replacement and subnet deletion", "Reviewer stops before apply; no cloud change", "Correct explicit local root and verify target", "Local plan contains only intended built-in resource"],
                "facts": "Plan contents and selected target are synthetic supplied fixture values; no apply or outage occurred.",
                "inference": "A missing target assertion and review gap plausibly explain the unrelated proposed changes; inspect variable provenance before assigning individual responsibility.",
                "expected": "A rejected-plan record, explicit target guard, and a local plan whose resource actions match the exercise scope.",
            },
            "lab": lab(
                "Build and review a local Terraform module",
                "Create a minimal child module using only terraform_data, pin the Terraform CLI compatibility range, run a local plan and apply, inspect outputs and resource state, change one input, then destroy the disposable object.",
                "A committed-quality local module, lock file, successful fmt/init/validate/plan/apply evidence, output and state inspection, changed-input plan, and cleanup record.",
                "Terraform CLI 1.x installed locally; shell and editor; no cloud account, credentials or external providers required. Carry Day 14 Git/API artifact for versioned evidence.",
                "Run `terraform version`; use a new writable directory; confirm there is no GCP provider or backend block in the supplied files. Do not run these commands in a shared Terraform root. Record the CLI version and date.",
                [
                    ("Preflight the local runtime", "Create the isolated directory and record CLI availability. Expected: Terraform prints its installed version; if command is missing, stop and retain a design-only artifact rather than silently installing software.\n\n```sh\nmkdir -p day126-topic01-local/module\ncd day126-topic01-local\nterraform version\n```"),
                    ("Prepare the minimal module files", """Write the exact child module and root files. `terraform_data` is built into Terraform, so this configuration needs no provider download and creates no cloud object.\n\n```sh\ncat > main.tf <<'EOF'\nterraform {\n  required_version = ">= 1.4.0, < 2.0.0"\n}\n\nvariable "environment" {\n  type        = string\n  description = "Disposable exercise environment"\n  default     = "lab"\n  validation {\n    condition     = contains(["lab", "test"], var.environment)\n    error_message = "environment must be lab or test"\n  }\n}\n\nmodule "baseline" {\n  source      = "./module"\n  environment = var.environment\n}\n\noutput "exercise_id" {\n  value = module.baseline.exercise_id\n}\nEOF\ncat > module/main.tf <<'EOF'\nvariable "environment" {\n  type = string\n}\n\nresource "terraform_data" "baseline" {\n  input = {\n    name        = "brightloaf-${var.environment}-baseline"\n    environment = var.environment\n    owner       = "day126-lab"\n  }\n}\n\noutput "exercise_id" {\n  value = terraform_data.baseline.id\n}\nEOF\n```"""),
                    ("Author and format the dependency-free plan", "Format, initialize and validate. Because the only resource is built in, init should not need to install a provider. Then create a plan file and inspect the human-readable summary. Expected result is one planned `terraform_data.baseline` creation and an output known after apply.\n\n```sh\nterraform fmt -recursive\nterraform init\nterraform validate\nterraform plan -out=baseline.tfplan\nterraform show baseline.tfplan\n```"),
                    ("Execute the reviewed local change", "Read the displayed plan and confirm the only address is `module.baseline.terraform_data.baseline`, environment is `lab`, and no destroy or replacement is proposed. Apply the saved plan. Expected output: one object added; this is local Terraform state only.\n\n```sh\nterraform apply baseline.tfplan\nterraform output -raw exercise_id\nprintf '\\n'\n```"),
                    ("Inspect the resulting state and recreate plan", """List the state address and show the resource's recorded input. Then run a fresh plan: with unchanged configuration the expected summary is no changes. Record command output in `evidence.txt`; omit any sensitive data (this fixture contains none).\n\n```sh\nterraform state list\nterraform state show module.baseline.terraform_data.baseline\nterraform plan -detailed-exitcode\nprintf 'plan_exit=%s\\n' "$?"\n```"""),
                    ("Challenge a bounded input edge case", "Pass the disallowed value `prod`. Validation must reject the value before any apply. Then plan with `test`; the plan should show an in-place update of the local terraform_data input, not a cloud resource operation.\n\n```sh\nterraform plan -var='environment=prod'\nterraform plan -var='environment=test' -out=test.tfplan\nterraform show test.tfplan\n```"),
                    ("Diagnose evidence and record the decision", "Create an evidence note from exact command results. Record that `prod` failed the variable validation; `lab` created one local object; the no-change plan used detailed exit code 0; and `test` proposes a local data change. State what this experiment cannot show: provider APIs, remote backend locking, IAM, import, cloud drift.\n\n```sh\ncat > evidence.txt <<'EOF'\nScope: local Terraform CLI; built-in terraform_data; no cloud provider/API.\nCLI version: RECORD terraform version output\nInitial plan: one module.baseline.terraform_data.baseline create\nApply: RECORD added/changed/destroyed counts\nUnchanged plan: exit 0 means no changes\nInvalid input prod: variable validation rejected it; no apply run\nTest input: inspect saved plan; local terraform_data only\nLimit: does not test GCS backend, IAM, Google provider, import, or drift.\nEOF\n```"""),
                    ("Close out and preserve reproducible evidence", "Destroy only the disposable local terraform_data object, confirm no managed addresses remain, and keep source plus redacted command evidence as the artifact. Expected destroy count is one; no cloud billing or remote state is involved.\n\n```sh\nterraform destroy -auto-approve\nterraform state list\ncd ..\n```"),
                ],
                "Expected observations: init identifies no external provider requirement; validate succeeds; first plan proposes one local address; apply creates it; output is non-empty; unchanged detailed plan exits 0; invalid input fails validation; changed input updates the local object; destroy leaves no state addresses. Capture actual local output, do not copy illustrative values as results.",
                "Accept the files `main.tf`, `module/main.tf`, `.terraform.lock.hcl` if generated, and `evidence.txt`; include actual CLI version and command results, module input/output contract, approved plan scope and cleanup confirmation. Redact local paths or identifiers if needed. Map to Exit evidence: versioned IaC, plan/recreation evidence and isolation diagram.",
                "If Terraform is older than the declared range, do not lower the constraint silently; record the mismatch. If init tries to download a provider, inspect the configuration for an unintended provider. A nonzero `plan -detailed-exitcode` can mean changes (2) or error (1); inspect diagnostics before recording. Never apply the `prod` input.",
                "The exercise destroys only its disposable local terraform_data resource and retains source/evidence. Remove the temporary directory after committing or copying the accepted artifact. No cloud resources, APIs, billing or credentials are used.",
                "day-126-topic-01-local-module.md",
            ),
        },
        {
            "key": "topic-02", "title": "State, environment boundaries, GCS backend, locking, versioning, access, imports and pinning",
            "overview": (
                "Terraform state is the mapping between configuration addresses and managed objects, along with values needed to plan changes. "
                "The GCS backend stores a state object under a configured bucket and prefix and supports locking; object versioning is a recovery "
                "control recommended by the backend documentation. This belongs today because a correct module can still damage the wrong "
                "environment if teams share state ownership or credentials. State owners define bucket, prefix, IAM, backup/recovery and change "
                "process; resource teams own configuration and import reconciliation. A prefix helps organize state but IAM is enforced at the "
                "bucket/object boundary available to the platform; versioning does not replace restrictive access or a tested recovery procedure."
            ),
            "preview": "Two pipelines point to the same bucket and prefix, and both propose updates against one shared state lineage. A distinct backend key and bounded writer set prevent cross-environment changes that could expose data or interrupt service.",
            "technical": """## State is operational authority

State binds a Terraform resource address to a real object identifier and records attributes needed to plan. It may contain credentials or other sensitive values produced by providers even when normal output is redacted. Restrict access to state and saved plans; avoid embedding secret material in inputs or outputs. The state lineage distinguishes a state history and its serial advances as writes occur. Manual state push can overwrite data and should be treated as a recovery operation with verified backup, lineage and serial, not routine workflow.

## Remote GCS backend and environment isolation

The GCS backend uses a pre-existing bucket and a configured prefix; backend configuration is selected during Terraform initialization. HashiCorp documents support for state locking and recommends Cloud Storage object versioning for recovery from accidental deletion or human error. Backend initialization does not make an environment boundary by itself. Give dev, test and prod independently governed prefixes or buckets according to operational and IAM requirements; define distinct state writers, narrowly scoped readers, execution identities and protected promotion. Bucket IAM and organization controls determine access. Avoid treating workspace names, directory names or prefixes as an authorization mechanism.

Backend configuration should avoid credentials in source. Operators must verify active account, project, backend bucket and prefix before backend initialization, state migration or any write. A backend initialization with the state-migration option copies existing state to the configured backend and needs a deliberate migration plan and backup. Concurrent writers should rely on backend locking; do not disable locking to “fix” a wait. `force-unlock` is only for a lock known to belong to the operator after automatic unlock failure, because unlocking another active run permits simultaneous state writers.

## Provider and module version controls

Set a supported Terraform CLI range, provider source addresses and compatible provider constraints. Commit `.terraform.lock.hcl` for root configurations to retain selected provider versions and checksums; upgrade intentionally by changing constraints and reviewing lock updates. Shared modules should state the minimum provider functionality they require while the root caller controls tested upper bounds. Registry module versions are separate from provider pins. Version policy makes builds more reproducible, but not deterministic across every external API or a changed remote object.

## Import is ownership adoption, not discovery magic

Import maps an existing remote object into a chosen resource address. Write and review matching configuration first, confirm the target identity and that no other state owns it, import through a configuration import block or CLI flow, then plan and reconcile differences before future apply. Import does not mean the configuration is complete or that a bulk-generated module is safe. The next plan is the key evidence: unexpected replacement, deletion or unrelated changes indicate a bad address/configuration, missing attributes or competing ownership. Keep this page's import exercise tabletop; real import requires an authorized disposable object, current API/IAM checks and a backup.

References: [GCS backend configuration, locking and object versioning](https://developer.hashicorp.com/terraform/language/backend/gcs), [Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking), and [Google Cloud resource import](https://docs.cloud.google.com/docs/terraform/resource-management/import?hl=en).""",
            "questions": [
                "What bucket/prefix is active, which principal can write it, and are object versions retained under an approved policy?",
                "How are prod and test isolated beyond naming, and what evidence proves a run selected the intended backend?",
                "Who owns recovery approval, and how will lineage, serial and lock ownership be checked before restore or force-unlock?",
                "After import, does the next plan converge without replacing the existing object or managing it from another state?",
            ],
            "reference": "https://developer.hashicorp.com/terraform/language/backend/gcs",
            "reference_label": "Terraform GCS backend: state prefix, locking and object-versioning guidance (accessed 2026-09-29)",
            "scenario": {
                "scenario": "Synthetic supplied fixture: Brightloaf's test and production pipeline definitions both show bucket `bl-state-example` and prefix `terraform/shared`. A permission worksheet lists the same broad pipeline service account as writer for both environments. Object versioning is reported enabled, but no restore rehearsal or run identity log is supplied.",
                "impact": "A test apply could write state that maps production addresses, while a production run could overwrite test assumptions. Broad access expands the impact of a compromised or misconfigured pipeline; version history helps recovery but does not prevent unauthorized writes.",
                "constraints": "Do not access a real bucket. Preserve production data and single ownership of each managed resource. Access must be least privilege, recovery controlled and environment selection observable.",
                "evidence": "Supplied synthetic worksheet: same bucket and prefix in test/prod configs; same broad writer service account; object versioning enabled; no restore rehearsal or execution identity log. These are fixture facts only.",
                "root": "The documented configuration collapses two independent environment state boundaries into one key and does not establish separate writer identities. Versioning addresses recoverability after some object changes; it neither separates environments nor prevents concurrent or unauthorized writes.",
                "diagnostic_steps": [
                    "Compare backend bucket, prefix/workspace, effective project and pipeline identity for every environment configuration; flag exact duplicate state coordinates.",
                    "Build a principal-to-action matrix for state read, write, object version access and lock operations; distinguish named deployer identities from human break-glass readers.",
                    "Check versioning/retention settings, audit evidence, migration owner, backup location and last restore rehearsal; mark all missing items as unknown rather than assumed safe.",
                ],
                "remediation_steps": [
                    "Assign unique state coordinates and documented ownership to test and prod; choose per-environment buckets or prefixes only with bucket IAM and organization policy that prevent cross-environment writes.",
                    "Replace the shared broad writer with environment-specific execution identities and narrow the state access set; require explicit target checks before init and plan.",
                    "Keep object versioning under an approved retention policy and rehearse recovery on a disposable copied state; test locking with an authorized parallel-run simulation before production adoption.",
                ],
                "verify": "A tabletop re-review must show distinct state coordinates, non-overlapping write principals, read access justified by role, version retention owner, locking assumptions, and a documented restore drill. No GCS calls are made by the exercise.",
                "residual": "The worksheet cannot prove actual IAM inheritance, bucket retention, backend runtime behavior or restore success. These require read-only inspection and a controlled disposable backend test before operational use.",
                "diagram": ["Test and prod configs share bucket and prefix", "Same pipeline identity can write both state contexts", "Versioning exists but restore and IAM are unverified", "Separate backend coordinates and execution identities", "Tabletop access matrix supports isolated state ownership"],
                "facts": "Bucket/prefix equality, broad service account and versioning status are synthetic supplied worksheet facts; restore and logs are absent.",
                "inference": "The shared coordinates and writer appear to erase environment separation; no evidence establishes an actual state overwrite or production impact.",
                "expected": "A redacted environment/state diagram with unique coordinates, named writer/read roles, locking/versioning assumptions and recovery evidence gaps.",
            },
            "lab": lab(
                "Design an isolated GCS state access boundary",
                "Use a fixed synthetic backend and identity fixture to produce an environment isolation diagram, backend-key table, access decision matrix, and migration/recovery checklist without connecting to Google Cloud.",
                "A precise, redacted design identifies distinct test/prod state coordinates, authorized writers/readers, locking/versioning controls, migration preconditions and evidence still requiring real verification.",
                "Day 34 identity and project-boundary artifact; familiarity with Terraform state and GCS IAM concepts. Spreadsheet or text editor; no gcloud/Terraform cloud credentials.",
                "Use only the fixture below. Confirm no cloud CLI command or bucket access is part of this lab. Treat all principal names and bucket IDs as fictional labels, not actual identities. Inputs: test and prod currently use `gs://bl-state-example/terraform/shared`; writer `sa-tf-pipeline@example.invalid`; object versioning is marked enabled; restore rehearsal unknown.",
                [
                    ("Preflight the fixture and risk scope", "Create a worksheet and copy the exact supplied fields. Count the current state coordinates: bucket plus prefix gives one shared coordinate used by two environments. Expected result: one duplicate coordinate finding; no network or API operation.\n\n```text\nEnvironment | Bucket | Prefix           | Writer                         | Versioning | Restore\ntest        | bl-state-example | terraform/shared | sa-tf-pipeline@example.invalid | enabled    | unknown\nprod        | bl-state-example | terraform/shared | sa-tf-pipeline@example.invalid | enabled    | unknown\n```"),
                    ("Prepare proposed environment coordinates", "Choose a design for the exercise and write the mapping. For this fixture use `terraform/test` and `terraform/prod` prefixes, then explicitly mark that prefixes alone do not prove IAM isolation. Expected result: two unique coordinates, one bucket, additional bucket IAM enforcement required.\n\n```text\ntest -> gs://bl-state-example/terraform/test\nprod -> gs://bl-state-example/terraform/prod\nAssumption: bucket-level IAM policy can distinguish object/prefix access only if the selected IAM design and conditions support it; validate exact policy semantics before deployment.\n```"),
                    ("Author the access decision matrix", "Fill each cell with allow/deny/unknown for the proposed design. Required roles are environment-specific pipeline writer, platform state administrator, and auditor. State should not be readable by unrelated workload identities. Mark lock/update permissions and version recovery permissions for validation against current Cloud Storage and Terraform backend requirements.\n\n```text\nPrincipal role | test state read/write | prod state read/write | lock/version action | evidence needed\ntest deployer  | allow / allow         | deny / deny           | test only          | effective IAM policy\nprod deployer  | deny / deny           | allow / allow         | prod only          | effective IAM policy\nplatform admin | approved break-glass | approved break-glass | recovery only      | approval + audit log\nauditor         | read only if required | read only if required | no write           | audit purpose\n```"),
                    ("Execute the isolation analysis", "Apply three checks to the proposed table: (1) count unique bucket/prefix pairs, expected 2; (2) count principals with write in both environments, expected 0; (3) count unknown operational controls. Record the results and list IAM conditions, lock behavior and object version access as items to verify in an authorized disposable project.\n\n```text\nUnique backend coordinates: 2\nCross-environment writers: 0\nCloud controls not verified here: effective IAM, lock contention behavior, version retention, audit logging, restore procedure\n```"),
                    ("Inspect expected state and verify boundaries", "Draw the data-flow diagram: test runner -> test prefix; prod runner -> prod prefix; each state write -> lock/version history; human recovery role -> approval boundary. Add a separate resource ownership column so one real resource address belongs to one state. Expected: no arrow from the test runner to prod state and no resource duplicated across states."),
                    ("Challenge the versioning edge case", "Given this event card—`test deployer accidentally writes a bad test state object; object versioning is enabled; prod state lives under its own prefix`—write the safest recovery choice and two preconditions. Expected: inspect and recover the prior test object version only after identifying exact object, serial/lineage and a controlled recovery owner; do not copy test state over prod. Note versioning alone does not prove retention or correct IAM."),
                    ("Diagnose and record the decision", "Write a 5-row decision record: observed fixture fact, proposed boundary, writer set, recovery mechanism, and unresolved validation. For each proposed control name evidence: effective policy export, backend init/lock test on disposable state, object version inventory, and restore rehearsal record. Mark all as not verified locally."),
                    ("Close out and save the redacted design", "Save the coordinate table, access matrix, diagram and decision record as `day-126-state-boundary.md`. Include the exact statement: `Tabletop design only; no bucket was inspected or changed.` Retain the artifact for the Day 126 exit package; remove no shared state because none was accessed."),
                ],
                "Check two unique backend coordinates; zero shared writers; one resource owner per state; version history is a recovery aid, not an isolation control; effective permissions and lock behavior remain unverified until a disposable authorized backend test.",
                "Accept `day-126-state-boundary.md` with current versus proposed bucket/prefix map, access matrix, environment-state diagram, ownership rule, locking/versioning and recovery design, and explicit unverified items. No credentials, bucket names from real projects or state contents may be included.",
                "If prefix-conditioned IAM cannot be proven for the chosen policy model, propose separate buckets or a verified alternative instead of assuming isolation. Object versioning needs lifecycle/retention review. A lock wait is not permission to disable locking or force-unlock another operator.",
                "Tabletop only; no cloud resources, costs, credentials or state files. Keep the design artifact and discard any scratch copy containing real identities before sharing.",
                "day-126-topic-02-state-boundary.md",
            ),
        },
        {
            "key": "topic-03", "title": "Drift, recovery and testing handoff to Day 127",
            "overview": (
                "Drift describes disagreement between declared configuration and infrastructure observed during refresh; recovery restores a "
                "trusted state/configuration relationship after a failed write, accidental change or backend problem. Day 126 establishes the "
                "state boundary and evidence needed to test those cases; Day 127 performs drift, policy, test and recovery practice. This "
                "boundary matters because refreshing, importing, restoring an old version and applying configuration have different effects. "
                "The state owner coordinates recovery, the resource owner confirms intended infrastructure, and reviewers preserve lineage and "
                "serial evidence. A plan can reveal differences but cannot itself decide whether configuration or a manual change is authoritative."
            ),
            "preview": "A plan proposes restoring a manually changed firewall rule while a service owner says the change was an approved emergency. Applying automatically would undo a live mitigation, delaying recovery and risking a broader outage.",
            "technical": """## Keep detection separate from correction

Terraform refresh reads provider-visible values for managed resources and compares them with configuration and state during planning. A proposed update can indicate drift, an intentional configuration edit, provider normalization, a missing attribute or an observation failure. Record the address, remote change, plan action, owner and maintenance/incident context before choosing a correction. `-refresh-only` can update state to reflect remote changes without changing infrastructure, but that may formalize an out-of-band value and should be reviewed. Import is for adopting an existing object; it is not the same as drift reconciliation.

## Recovery requires trusted evidence

GCS object versioning can provide prior state object generations, but selecting a generation and restoring it is a state write with consequences. First establish correct backend coordinates and identity, stop concurrent writers, preserve a copy, compare object generation, Terraform state lineage and serial, identify the last known-good configuration and applied plan, then rehearse against a disposable copy. A stale state may omit objects that still exist; a stale configuration may recreate or delete them. Never restore a production state object simply because its timestamp looks right. Avoid routine `state push` and `force-unlock`; both bypass normal workflows or safety boundaries.

## Tests and policy checks define acceptable changes

Separate static checks (`fmt`, `validate`, module tests, policy rules) from provider-backed integration checks and post-apply verification. A passing static test does not establish permissions, API availability or real-world resource behavior. Define fixtures for allowed and denied values, required labels, regions and destructive plans. Policy ownership should be explicit: platform guardrails constrain the permitted envelope; workload teams own application requirements. Use ephemeral isolated backends for destructive import, drift or recovery rehearsals, then capture command outputs, state generation and cleanup.

## Day 127 handoff

Bring the module and provider lock file, intended environment inputs, plan evidence, state isolation diagram, resource ownership list, and a redacted statement of locking/versioning assumptions. Day 127 will exercise drift detection, safe import, tests and recovery using disposable state. Today does not mutate a real resource or state. Google Cloud's Terraform guidance distinguishes API enablement from resource import: an enabled API is service access readiness; importing adopts an existing resource into state. Neither action proves the other.

References: [Google Cloud Terraform API and import distinctions](https://docs.cloud.google.com/docs/terraform/understanding-apis-and-terraform) and [Terraform state locking and force-unlock safety](https://developer.hashicorp.com/terraform/language/state/locking).""",
            "questions": [
                "Does the planned difference come from configuration, out-of-band change, normalization or incomplete provider observation?",
                "Who owns the object and confirms whether the remote value is approved before reconciliation?",
                "What exact lineage, serial, object generation, backup and writer-stop evidence would make recovery safe to rehearse?",
                "Which assertions are static unit checks and which need an isolated provider-backed integration environment?",
            ],
            "reference": "https://docs.cloud.google.com/docs/terraform/understanding-apis-and-terraform",
            "reference_label": "Google Cloud: API enablement and resource import are different operations (accessed 2026-09-29)",
            "scenario": {
                "scenario": "Synthetic supplied fixture: a Terraform plan for Brightloaf proposes changing firewall ingress from `10.20.0.0/16` to `0.0.0.0/0`. A change ticket says an emergency access change may have been made, but the ticket owner, timestamp, and deployed policy export are missing. No plan apply or incident outcome is supplied.",
                "impact": "The plan could either remove an emergency access path or preserve an unintended public ingress rule. Guessing which side is authoritative can extend an incident or expose a service.",
                "constraints": "Protect service availability and least-privilege access; don't apply, refresh-only apply, import or restore state in the exercise. Day 127 owns hands-on drift/recovery testing.",
                "evidence": "Synthetic plan fixture: proposed CIDR change from 10.20.0.0/16 to 0.0.0.0/0; ticket mentions emergency change; owner, timestamp and deployed firewall export are absent. No production outcome is established.",
                "root": "Cause is undetermined. Possibilities include approved out-of-band emergency action, accidental broadening, configuration error or provider observation issue. The supplied evidence is insufficient to decide which value is correct.",
                "diagnostic_steps": [
                    "Pause writes; capture plan, backend identity, resource address, state lineage/serial and provider refresh diagnostics without editing state.",
                    "Ask the service and security owners for incident/change ticket identity, approval, timeline and deployed firewall policy export; compare rule priority, direction, targets and effective policy.",
                    "Inspect source history and last applied plan to distinguish intended configuration change from remote-only drift; document missing evidence and who can supply it.",
                ],
                "remediation_steps": [
                    "Do not choose an ingress CIDR by guess. If the emergency value is confirmed and must remain, update reviewed configuration to reflect the approved intended state; if it was unauthorized, use the incident owner's approved containment and correction procedure.",
                    "Re-run a refreshed plan after owners reconcile facts; require the plan to show only the reviewed firewall action and obtain security/service approval before apply.",
                    "Schedule the Day 127 disposable drift/import/recovery rehearsal using copied synthetic state and an explicit stop condition; preserve current state evidence before any recovery action.",
                ],
                "verify": "Acceptance requires a signed decision tying the intended CIDR to the approved ticket, a reviewed plan with no unrelated changes, and a post-change check against the effective firewall policy. This page performs none of those cloud checks.",
                "residual": "No ticket owner, timestamp, policy export, apply result or live telemetry is supplied. The synthetic worksheet cannot determine whether the broader rule exists or was approved; that remains an owner-led investigation.",
                "diagram": ["Plan proposes ingress change; ticket hints emergency action", "Owner, timeline, and actual policy export are missing", "Either automatic revert or retain could worsen risk", "Pause writes and establish approved intended state", "Reconcile config then review narrow plan with service/security owners"],
                "facts": "The plan delta and incomplete ticket are synthetic supplied fixture facts only.",
                "inference": "An emergency out-of-band change is possible, but evidence does not establish it or establish a root cause.",
                "expected": "A no-write decision record with evidence gaps, named owners, a safe plan-review gate and Day 127 disposable rehearsal handoff.",
            },
            "lab": lab(
                "Prepare the drift and recovery evidence handoff",
                "Classify a supplied plan difference, list the evidence needed before correction, and create a bounded Day 127 test/recovery plan using explicit synthetic state metadata.",
                "A no-write drift decision record, source-labeled fact/inference table, safe investigation sequence and a recovery rehearsal checklist with stop criteria.",
                "Day 125 exit capacity evidence and Day 126 topic 1 local module artifact; no cloud permissions or Terraform state file required.",
                "Use only the fixture: config CIDR `10.20.0.0/16`; refreshed plan value `0.0.0.0/0`; change ticket says emergency edit possible; owner/time/effective rule export missing. Confirm this is a worksheet exercise and no state push, force-unlock or apply is allowed.",
                [
                    ("Preflight the no-write decision", "Create a blank table with columns `supplied fact`, `inference`, `missing evidence`, `owner`, `write permitted?`. Enter the four fixture facts exactly and mark all writes `no` until the owner and effective rule are established. Expected: no fabricated incident outcome.") ,
                    ("Prepare the resource and ownership record", "Fill this resource record for the fixture. Mark fields absent from the prompt as unknown rather than inventing IDs. Expected: one resource address under investigation, service/security owner unknown, state owner unknown.\n\n```text\nResource address: google_compute_firewall.<unknown>\nConfigured ingress CIDR: 10.20.0.0/16\nRefreshed plan value: 0.0.0.0/0\nChange ticket: mentioned; identifier and timestamp unknown\nEffective deployed policy export: missing\nState lineage / serial / backend generation: not supplied\n```"),
                    ("Author a bounded evidence plan", "Write a four-item request list: ticket ID/approver/time; effective firewall policy export; prior reviewed configuration/plan; backend and resource ownership evidence. For each item name the owner and the decision it supports. Add stop conditions: active incident without incident commander, unknown backend, or any concurrent writer means no state action.") ,
                    ("Execute the tabletop triage sequence", "Apply the sequence to the fixture: pause writes; capture current plan and state metadata read-only; compare ticket timeline with deployed policy; ask owners whether broad CIDR is approved; record either `approved emergency change`, `unauthorized change`, or `undetermined`. Because evidence is missing, expected classification is `undetermined` and no apply.") ,
                    ("Inspect the expected record", "Check your table against these expected outputs: (1) facts contain only the given CIDRs/ticket note; (2) root cause is `undetermined`; (3) no restore/import/apply is authorized; (4) a refreshed plan and effective-policy comparison are required after owner decision. Correct any unsupported claim.") ,
                    ("Challenge a bounded recovery edge case", "Use this explicitly hypothetical card: `A copied disposable state has lineage L-test, serial 8; the selected prior GCS object version has lineage L-test, serial 7; no writer is active.` Decide whether the copy may be used in a test rehearsal. Expected: yes, only in the disposable rehearsal after backup and owner approval; never push serial 7 over shared/prod state. Record that lineage/serial metadata alone do not prove matching remote objects.") ,
                    ("Diagnose and record the handoff", "Complete a decision record with one row each for fact, hypothesis, evidence needed, owner, permitted next action and abort condition. Specify Day 127 follow-up: inject drift only into a disposable object, detect via plan, test correction, and recover only from a copied disposable state while capturing lineage, serial and object generation.") ,
                    ("Close out and preserve the evidence", "Save `day-126-drift-handoff.md` with the explicit label `tabletop; no write or live resource inspection`. Include the unresolved condition, next owner, evidence request list, recovery rehearsal boundary and Day 127 handoff artifacts. No cloud cleanup is needed.") ,
                ],
                "The correct current disposition is `undetermined; pause writes`. Expected worksheet has four fixture facts, no invented root cause, no authorized cloud operation, explicit owner/evidence requests, and only a disposable-state Day 127 recovery plan.",
                "Accept `day-126-drift-handoff.md` with fact/inference separation, resource/state ownership gaps, no-write decision, named evidence requests, stop conditions, hypothetical copied-state metadata analysis, and Day 127 rehearsal handoff. This is not evidence that drift or recovery was run against Google Cloud.",
                "Do not interpret a `refresh-only` plan as harmless: applying it changes state. A prior state object may be stale or omit remote objects; verify lineage, serial and generation and use a disposable copy. Never use force-unlock to bypass unknown ownership.",
                "Tabletop only. Retain the handoff document; no Terraform state or cloud object was read or modified. No state cleanup, API enablement or cost is involved.",
                "day-126-topic-03-drift-handoff.md",
            ),
        },
    ],
}
