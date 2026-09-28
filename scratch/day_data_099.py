"""day_data_099.py — Exhaustive architecture data specification for Day 99.

Covers Advanced IAM and Policy Evaluation:
1. Core security principles: Least privilege, separation of duties (SoD), need-to-know, and eliminating toxic permission combinations.
2. Predefined vs Custom Roles: maintenance overhead, feature deprecation risks, and granular role curation.
3. IAM Recommender & Policy Intelligence: 90-day ML observation windows, excess permission discovery, and automated right-sizing.
4. IAM Conditions (CEL): Common Expression Language conditions for time-bound access, resource prefix restrictions, and tag-based scoping.
5. IAM Deny Policies & Principal Access Boundaries (PABs): evaluation hierarchy (Deny overrides Allow), organization-wide guardrails, and boundary enforcement.
Follows PAGE_AUTHORING_CONTRACT.md with hands-on, verifiable exercises.
"""

DAY_NUM = 99

DATA = {
    "day": 99,
    "part1_intro": (
        "Day 99 inaugurates the deep enterprise security curriculum: advanced Identity and Access Management (IAM), policy evaluation "
        "hierarchies, and automated least-privilege enforcement. In cloud architectures, perimeter network firewalls are secondary; identity is "
        "the primary security perimeter. Broad, permissive role assignments (such as primitive Editor or Owner roles) represent catastrophic "
        "blast radius vulnerabilities that allow single compromised service accounts to escalate privileges, exfiltrate data, or disable backups. "
        "Today's curriculum constructs an ironclad IAM architecture using Common Expression Language (CEL) conditions, ML-driven IAM Recommenders, "
        "Organization-level Deny policies that override all allows, and Principal Access Boundaries to enforce separation of duties."
    ),
    "exit_summary": (
        "Engineered an enterprise Advanced IAM and Policy Evaluation framework: evaluated an allow/deny/condition policy fixture through an automated "
        "Python policy simulator; remediated an excessive primitive Editor grant into a right-sized custom role; authored an authorization decision "
        "matrix and organization-wide IAM Deny guardrails blocking service account key creation."
    ),
    "part2_intro": (
        "Cloud IAM policy evaluation is deterministic: Deny rules are evaluated first and override all Allow rules, followed by conditional "
        "CEL expressions and inherited resource hierarchy bindings. The sections below analyze least privilege mechanics, custom role trade-offs, "
        "IAM Recommender algorithms, conditional expressions, and Principal Access Boundaries."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>IAM Mechanism / Primitive</th>
      <th>Evaluation Timing &amp; Scope</th>
      <th>Primary Security Function</th>
      <th>Key Limitation / Operational Boundary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>IAM Deny Policy</strong></td>
      <td>Evaluated <strong>First</strong> at Organization/Folder/Project levels</td>
      <td>Permanent negative guardrail overriding all Allow grants (e.g. deny `iam.serviceAccountKeys.create`)</td>
      <td>Supports subset of GCP permissions; cannot be overridden by any Allow policy</td>
    </tr>
    <tr>
      <td><strong>Principal Access Boundary (PAB)</strong></td>
      <td>Evaluated concurrently with Principal authorization</td>
      <td>Restricts the set of resources a principal can access regardless of Allow grants</td>
      <td>Applies to specific users or service accounts; requires Resource Manager v3 integration</td>
    </tr>
    <tr>
      <td><strong>IAM Conditions (CEL)</strong></td>
      <td>Evaluated during Allow binding resolution</td>
      <td>Restricts permissions by time window (`request.time`), resource name prefix, or destination tag</td>
      <td>Increases policy evaluation complexity; syntax errors in CEL can silently fail closed</td>
    </tr>
    <tr>
      <td><strong>Predefined Roles</strong></td>
      <td>Evaluated within Allow policy bindings</td>
      <td>Curated by Google; automatically updated as new API methods are released</td>
      <td>Often bundle hundreds of permissions beyond what a specific microservice requires</td>
    </tr>
    <tr>
      <td><strong>Custom Roles</strong></td>
      <td>Evaluated within Allow policy bindings</td>
      <td>Exact least-privilege curation containing only needed permissions</td>
      <td>High maintenance overhead; does not inherit newly released Google Cloud API permissions</td>
    </tr>
    <tr>
      <td><strong>IAM Recommender</strong></td>
      <td>Background ML analysis over 90-day activity window</td>
      <td>Identifies unused permissions and recommends least-privilege role substitutions</td>
      <td>90-day observation window required; can break rare quarterly disaster recovery workflows if applied naively</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Google Cloud IAM Deterministic Policy Evaluation Sequence",
        "desc": "Flowchart showing request arrival, Deny policy evaluation, Principal Access Boundary checks, CEL Condition parsing, and final Allow resolution.",
        "caption": "Figure 99.1: Deterministic IAM evaluation sequence: Deny policies override all Allows, followed by Boundaries and Conditions.",
        "nodes": [
            ("1. API Request Ingress", "Principal, resource & method"),
            ("2. Deny Policy Gate", "Deny matches? -> Instant 403"),
            ("3. Access Boundary Gate", "Resource within PAB boundary?"),
            ("4. Allow & CEL Resolution", "Condition true? -> Access Granted"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Least Privilege, Separation of Duties, and Need-to-Know",
            "overview": (
                "The principle of least privilege dictates that an identity (human engineer, service account, or external contractor) must be granted "
                "only the minimum set of permissions necessary to execute its legitimate function, and only for the duration required. Separation of Duties "
                "(SoD) ensures that critical or high-risk multi-stage operations cannot be executed by a single individual, preventing internal fraud "
                "and limiting catastrophic error blast radii. In Google Cloud, this requires strictly eliminating primitive roles (`roles/owner`, `roles/editor`), "
                "separating encryption key administration from data access, and enforcing dual-custody access for sensitive production releases."
            ),
            "preview": (
                "A developer account with project Editor privileges accidentally drops a production BigQuery billing dataset. "
                "Separation of duties and least-privilege role assignment prevent software developers from holding administrative permissions over analytical data."
            ),
            "technical": (
                "### 1. Primitive vs Predefined Roles: The Blast Radius Risk\n"
                "- **Primitive Roles (Owner, Editor, Viewer):** Legacy coarse-grained roles from early GCP. `roles/editor` grants mutation access "
                "to almost all GCP services (Compute, Storage, Cloud SQL, BigQuery, Pub/Sub).\n"
                "- **Toxic Combinations:** A principal with `roles/editor` can create Compute instances with default compute service accounts, "
                "effectively granting themselves full administrative rights over the project's infrastructure.\n\n"
                "### 2. Separation of Duties (SoD) Topologies\n"
                "- **KMS Key Management vs Data Access:** An engineer with `roles/cloudkms.admin` can manage key rings and rotation schedules, "
                "but must **never** be granted `roles/cloudkms.cryptoKeyEncrypterDecrypter` (data decryption).\n"
                "- **Network Administration vs Compute Management:** Network Engineers hold `roles/compute.networkAdmin` in the Host Project, "
                "while Application Teams hold `roles/compute.instanceAdmin.v1` restricted strictly to Service Projects.\n\n"
                "### 3. Need-to-Know and Break-Glass Governance\n"
                "- Day-to-day production access for human engineers should be read-only (`roles/viewer` or `roles/monitoring.viewer`).\n"
                "- Mutation privileges must be granted temporarily via automated Just-In-Time (JIT) access requests with mandatory ticket correlation "
                "and automatic expiration (e.g. 2 hours)."
            ),
            "questions": [
                "Why are primitive roles like `roles/editor` considered unacceptable security risks in production Google Cloud environments?",
                "How does separating KMS key administration from crypto-operation roles enforce separation of duties in sensitive data environments?",
                "What architectural mechanisms enforce dual-custody approval before high-risk infrastructure mutations can be committed?",
            ],
            "reference": "https://docs.cloud.google.com/iam/docs/understanding-roles",
            "reference_label": "Google Cloud IAM: Understanding role hierarchies and least privilege best practices",
            "scenario": {
                "symptom": (
                    "A CI/CD build worker service account running automated unit tests was compromised by malicious dependency injection, "
                    "allowing attackers to delete the production Cloud SQL database instance and purge long-term audit buckets."
                ),
                "constraints": (
                    "Must restrict automated CI/CD service accounts strictly to deployment permissions on specific staging namespaces, "
                    "with zero administrative access over production databases or security logging."
                ),
                "evidence": (
                    "IAM audit showed the CI/CD service account possessed `roles/editor` at the project level, granted months earlier as a 'temporary' "
                    "workaround for a pipeline permission error."
                ),
                "diagnostic_steps": [
                    "Query Cloud Audit Logs for `methodName = 'sql.instances.delete'` and extract the caller's service account email.",
                    "Audit IAM policy bindings on the project to list all identities holding primitive `roles/editor`.",
                    "Review Git history on pipeline manifests to determine why the service account was granted broad privileges.",
                ],
                "root": (
                    "Violation of least privilege: granting primitive `roles/editor` to an automated CI/CD pipeline gave an untrusted build worker "
                    "unconstrained administrative control over the entire project."
                ),
                "fix": (
                    "Revoke `roles/editor` immediately. Create a dedicated service account granted only `roles/run.developer` and `roles/cloudbuild.builds.editor` "
                    "scoped to the staging project, strictly prohibiting production deletion permissions."
                ),
                "verify": (
                    "Run automated pipeline tests under the right-sized service account; confirm builds deploy successfully while attempts to modify "
                    "Cloud SQL or Logging return HTTP 403 Forbidden."
                ),
                "residual": (
                    "Granular roles require ongoing curation as new GCP services are adopted by application teams."
                ),
                "diagram": (
                    "Compromised build worker",
                    "Primitive Editor role leveraged",
                    "Production Cloud SQL deleted",
                    "Editor revoked; granular role applied",
                    "Database access blocked with 403"
                )
            },
            "lab": {
                "name": "Least Privilege Role Audit and Excessive Primitive Grant Remediation",
                "goal": "Audit project IAM bindings for primitive roles, author a least-privilege remediation script, and verify policy compliance.",
                "expected": "A validated shell remediation script replacing primitive roles with least-privilege grants, and an automated policy verification test.",
                "mode": "tabletop analysis & shell synthesis",
                "prereq": "Understanding of Google Cloud IAM roles and Resource Manager bindings.",
                "preflight": "Review Resource Manager policy binding and IAM role modification CLI documentation.",
                "steps": [
                    "Author the shell remediation script stripping primitive Editor roles and applying granular permissions (`remediate_primitive_roles.sh`):\n\n```sh\ncat <<'EOF' > remediate_primitive_roles.sh\n#!/usr/bin/env bash\nset -euo pipefail\n\n# Enterprise IAM Remediation: Strip Primitive Editor & Apply Least-Privilege Role\nPROJECT_ID=\"brightloaf-prod\"\nSERVICE_ACCOUNT=\"ci-runner-build@${PROJECT_ID}.iam.gserviceaccount.com\"\n\necho \"=== 1. Revoking Toxic Primitive Editor Binding ===\"\ncat <<COMMAND\ngcloud projects remove-iam-policy-binding \"$PROJECT_ID\" \\\n    --member=\"serviceAccount:$SERVICE_ACCOUNT\" \\\n    --role=\"roles/editor\" \\\n    --condition=None\nCOMMAND\n\necho \"\n=== 2. Applying Granular Least-Privilege Predefined Roles ===\"\ncat <<COMMAND\n# Grant 1: Allow deploying to Cloud Run services\ngcloud projects add-iam-policy-binding \"$PROJECT_ID\" \\\n    --member=\"serviceAccount:$SERVICE_ACCOUNT\" \\\n    --role=\"roles/run.developer\"\n\n# Grant 2: Allow artifact registry push\ngcloud projects add-iam-policy-binding \"$PROJECT_ID\" \\\n    --member=\"serviceAccount:$SERVICE_ACCOUNT\" \\\n    --role=\"roles/artifactregistry.writer\"\nCOMMAND\n\necho \"\n=== 3. Verification: Audit Effective Roles ===\"\ncat <<COMMAND\ngcloud projects get-iam-policy \"$PROJECT_ID\" \\\n    --flatten=\"bindings[].members\" \\\n    --format=\"table(bindings.role)\" \\\n    --filter=\"bindings.members:$SERVICE_ACCOUNT\"\nCOMMAND\nEOF\nchmod +x remediate_primitive_roles.sh\n./remediate_primitive_roles.sh\n```",
                    "Author an automated Python simulation verifying that the remediated permissions block unauthorized administrative actions:\n\n```sh\ncat <<'EOF' > test_least_privilege_remediation.py\n# Simulation of IAM Permission Evaluation Post-Remediation\n\nclass PolicySimulator:\n    def __init__(self):\n        # Prior state: roles/editor had all permissions\n        # Remediated state: granular roles only\n        self.granted_permissions = {\n            \"roles/run.developer\": [\"run.services.create\", \"run.services.update\", \"run.services.get\"],\n            \"roles/artifactregistry.writer\": [\"artifactregistry.repositories.uploadArtifacts\"]\n        }\n        \n    def is_permitted(self, assigned_roles, requested_permission):\n        for role in assigned_roles:\n            if requested_permission in self.granted_permissions.get(role, []):\n                return True\n        return False\n\nsim = PolicySimulator()\nassigned = [\"roles/run.developer\", \"roles/artifactregistry.writer\"]\n\n# Assertion 1: Valid deployment operations are PERMITTED\nassert sim.is_permitted(assigned, \"run.services.update\"), \"Valid Cloud Run deployment blocked!\"\nassert sim.is_permitted(assigned, \"artifactregistry.repositories.uploadArtifacts\"), \"Valid image push blocked!\"\n\n# Assertion 2: Dangerous administrative operations are BLOCKED (Formerly allowed under roles/editor)\nassert not sim.is_permitted(assigned, \"sql.instances.delete\"), \"SECURITY BREACH: Service account can delete database!\"\nassert not sim.is_permitted(assigned, \"storage.buckets.delete\"), \"SECURITY BREACH: Service account can delete storage!\"\nassert not sim.is_permitted(assigned, \"resourcemanager.projects.setIamPolicy\"), \"SECURITY BREACH: Service account can alter IAM!\"\n\nprint(\"=== REMEDIATION EVALUATION SUMMARY ===\")\nprint(\"Deploy Cloud Run:        PERMITTED (Expected)\")\nprint(\"Push Container Image:    PERMITTED (Expected)\")\nprint(\"Delete Cloud SQL:        DENIED    (Blocked successfully)\")\nprint(\"Delete Storage Bucket:   DENIED    (Blocked successfully)\")\nprint(\"Alter IAM Policies:      DENIED    (Blocked successfully)\")\nprint(\"\nPASS: Least privilege role remediation mathematically verified.\")\nEOF\npython3 test_least_privilege_remediation.py\n```",
                    "Review all output artifacts and confirm that the shell script and Python remediation test execute cleanly."
                ],
                "verification": "The shell script strips primitive roles and applies granular Cloud Run/Artifact Registry roles, and the Python test proves administrative deletion actions are blocked.",
                "trouble": "Ensure service account email matches the exact fully qualified identity string when running IAM policy commands.",
                "cleanup": "Retain `remediate_primitive_roles.sh` as an exit evidence artifact.",
                "accept": "Completed least-privilege remediation script and verified policy test. File: `day-099-topic-01-least-privilege.md`.",
                "file": "day-099-topic-01-least-privilege.md"
            }
        },
        {
            "key": "topic-02",
            "title": "Predefined Roles vs Custom Roles: Maintenance Trade-offs and Curation",
            "overview": (
                "Google Cloud provides hundreds of curated **Predefined Roles** designed for standard job functions (e.g. `roles/spanner.databaseUser`, "
                "`roles/pubsub.publisher`). While predefined roles reduce administrative overhead, they frequently bundle excessive permissions "
                "that violate strict compliance mandates. When predefined roles are too broad, architects design **Custom Roles** containing the exact "
                "list of permissions required. However, custom roles incur continuous maintenance liabilities: when Google releases new feature versions "
                "or deprecates underlying API permissions, custom roles do not update automatically, requiring manual lifecycle management."
            ),
            "preview": (
                "A predefined Storage role grants permission to delete all bucket data in addition to reading objects. "
                "Authoring a curated custom role provides exact read-only object streaming permissions without data destruction risk."
            ),
            "technical": (
                "### 1. Comparative Analysis: Predefined vs Custom Roles\n"
                "- **Predefined Roles:** Maintained by Google Cloud. Automatically updated when new API features are launched. "
                "Cons: Frequently bundle hundreds of permissions (e.g., `roles/storage.objectAdmin` includes permissions to change ACLs and delete buckets).\n"
                "- **Custom Roles:** Maintained by enterprise security teams. Scoped to the Organization or Project. Contains exact whitelist of API permissions. "
                "Cons: Cannot include permissions from services in Preview; does not receive automated permission updates; maximum of 64 custom roles per project "
                "or 1,280 per organization.\n\n"
                "### 2. Custom Role Lifecycle and Stages\n"
                "- Custom roles define a `stage` parameter:\n"
                "  - `ALPHA` / `BETA`: Under active testing.\n"
                "  - `GA`: General availability; production standard.\n"
                "  - `DEPRECATED`: Informs consumers that the role will be retired; allows graceful migration.\n"
                "  - `DISABLED`: Role bindings remain but permissions cease to be granted.\n\n"
                "### 3. Curation Best Practices\n"
                "- Prefer Predefined Roles whenever a tightly scoped role exists (e.g. `roles/pubsub.subscriber` rather than building custom Pub/Sub roles).\n"
                "- Use Custom Roles exclusively for high-risk data-plane applications where unintended permissions (like `storage.buckets.delete` or "
                "`bigquery.datasets.delete`) cannot be tolerated."
            ),
            "questions": [
                "Under what architectural criteria should an enterprise author a Custom Role rather than selecting a Predefined Role?",
                "What operational failure modes can occur when Google Cloud deprecates an underlying API permission used in an enterprise Custom Role?",
                "How does the custom role lifecycle stage (`GA` vs `DEPRECATED`) enable graceful role retirement across multi-project organizations?",
            ],
            "reference": "https://docs.cloud.google.com/iam/docs/understanding-custom-roles",
            "reference_label": "Google Cloud IAM: Creating, managing, and maintaining custom roles",
            "scenario": {
                "symptom": (
                    "A junior data analyst accidentally deleted an entire historical Cloud Storage bucket containing 40 TB of customer audit logs "
                    "because their account was assigned the predefined role `roles/storage.objectAdmin`."
                ),
                "constraints": (
                    "Analysts must have full capability to upload, read, and transform objects in designated buckets, with zero capability to delete buckets."
                ),
                "evidence": (
                    "Audit logs showed the analyst clicked 'Delete Bucket' in the Cloud Console. Predefined role `roles/storage.objectAdmin` includes "
                    "`storage.buckets.delete` alongside `storage.objects.create` and `storage.objects.get`."
                ),
                "diagnostic_steps": [
                    "Inspect the permission definition of `roles/storage.objectAdmin` via the IAM roles describe API.",
                    "Review Cloud Audit Logs to confirm the `storage.buckets.delete` RPC was authorized by the analyst's role binding.",
                    "Identify the minimal set of permissions required for daily analytical ingestion workflows.",
                ],
                "root": (
                    "Excessive predefined role scope: `roles/storage.objectAdmin` granted bucket-level administrative destruction permissions to users "
                    "who only required object-level CRUD capabilities."
                ),
                "fix": (
                    "Author an Organization-level Custom Role `brightloaf.storageObjectCurator` containing object-level permissions (`storage.objects.get`, "
                    "`storage.objects.create`, `storage.objects.list`) while explicitly omitting all `storage.buckets.*` mutation and deletion permissions."
                ),
                "verify": (
                    "Assign the custom role to a test user; verify the user can create and read objects, but attempting to delete a bucket returns HTTP 403 Forbidden."
                ),
                "residual": (
                    "If Google launches a new Cloud Storage feature (like soft delete recovery), the custom role must be updated manually to include the new permission."
                ),
                "diagram": (
                    "Analyst assigned Storage Object Admin",
                    "Role includes storage.buckets.delete",
                    "Entire 40 TB bucket deleted by accident",
                    "Custom brightloaf.storageObjectCurator authored",
                    "Bucket deletion permanently prevented"
                )
            },
            "lab": {
                "name": "Custom IAM Role Specification, Creation, and Permission Boundary Test",
                "goal": "Author a declarative YAML manifest for an enterprise Custom Role omitting destructive permissions and verify least-privilege boundary enforcement.",
                "expected": "A validated custom role YAML definition, an automated Python permission checker, and a role maintenance governance sheet.",
                "mode": "tabletop analysis & YAML/Python execution",
                "prereq": "Understanding of Google Cloud IAM permissions and custom role schemas.",
                "preflight": "Review custom role creation CLI syntax and permission naming conventions.",
                "steps": [
                    "Author the declarative Custom Role YAML specification (`custom_storage_curator_role.yaml`):\n\n```sh\ncat <<'EOF' > custom_storage_curator_role.yaml\ntitle: \"Brightloaf Storage Object Curator\"\ndescription: \"Allows reading and uploading storage objects while strictly prohibiting bucket deletion\"\nstage: \"GA\"\nincludedPermissions:\n  - storage.objects.create\n  - storage.objects.get\n  - storage.objects.list\n  - storage.objects.update\n  # Intentionally OMITTED destructive permissions:\n  # - storage.buckets.delete\n  # - storage.buckets.update\n  # - storage.buckets.setIamPolicy\nEOF\ncat custom_storage_curator_role.yaml\n```",
                    "Author the shell deployment script creating the organization-level custom role (`deploy_custom_role.sh`):\n\n```sh\ncat <<'EOF' > deploy_custom_role.sh\n#!/usr/bin/env bash\nset -euo pipefail\n\n# Enterprise Custom Role Deployment\nORG_ID=\"123456789012\"\nROLE_ID=\"brightloafStorageObjectCurator\"\n\necho \"=== 1. Creating Organization-Level Custom Role ===\"\ncat <<COMMAND\ngcloud iam roles create \"$ROLE_ID\" \\\n    --organization=\"$ORG_ID\" \\\n    --file=\"custom_storage_curator_role.yaml\"\nCOMMAND\n\necho \"\n=== 2. Describe and Verify Role Permissions ===\"\ncat <<COMMAND\ngcloud iam roles describe \"$ROLE_ID\" --organization=\"$ORG_ID\"\nCOMMAND\nEOF\nchmod +x deploy_custom_role.sh\n./deploy_custom_role.sh\n```",
                    "Author an automated Python test validating that the custom role contains required permissions while strictly excluding destructive methods:\n\n```sh\ncat <<'EOF' > test_custom_role_permissions.py\n# Verification of Custom Role Permission Boundaries\nimport yaml\n\nwith open(\"custom_storage_curator_role.yaml\") as f:\n    role_def = yaml.safe_load(f)\n\nperms = set(role_def.get(\"includedPermissions\", []))\n\n# Assert required functional permissions are present\nassert \"storage.objects.create\" in perms, \"Missing object create permission!\"\nassert \"storage.objects.get\" in perms, \"Missing object get permission!\"\nassert \"storage.objects.list\" in perms, \"Missing object list permission!\"\n\n# Assert dangerous destructive permissions are strictly ABSENT\nforbidden_permissions = [\n    \"storage.buckets.delete\",\n    \"storage.buckets.update\",\n    \"storage.buckets.setIamPolicy\",\n    \"storage.objects.delete\"\n]\n\nfor forbidden in forbidden_permissions:\n    assert forbidden not in perms, f\"SECURITY VIOLATION: Role contains forbidden permission: {forbidden}!\"\n\nprint(\"=== CUSTOM ROLE PERMISSION AUDIT ===\")\nprint(f\"Role Title: {role_def['title']}\")\nprint(f\"Role Stage: {role_def['stage']}\")\nprint(f\"Total Included Permissions: {len(perms)}\")\nprint(\"Forbidden Permissions Checked: 4/4 STRICTLY EXCLUDED\")\nprint(\"\nPASS: Custom role permission boundaries mathematically verified!\")\nEOF\npython3 test_custom_role_permissions.py\n```",
                    "Review all output artifacts and confirm that the YAML definition, deployment script, and Python permission audit execute without error."
                ],
                "verification": "The YAML specification defines exact object-level permissions and the Python test confirms all bucket deletion and IAM mutation permissions are excluded.",
                "trouble": "Ensure permission names follow the three-segment format `service.resource.verb` (e.g. `storage.objects.get`).",
                "cleanup": "Retain `custom_storage_curator_role.yaml` and `deploy_custom_role.sh` as exit evidence artifacts.",
                "accept": "Completed Custom Role specification and verified permission audit test. File: `day-099-topic-02-custom-roles.md`.",
                "file": "day-099-topic-02-custom-roles.md"
            }
        },
        {
            "key": "topic-03",
            "title": "IAM Recommender for Right-Sizing Permissions and Policy Intelligence",
            "overview": (
                "Over time, enterprise cloud environments suffer from 'permission creep': users and service accounts accumulate excessive permissions "
                "that are never exercised in practice. The **Google Cloud IAM Recommender** applies machine learning across a 90-day observation window, "
                "comparing the permissions an identity actually executed in Cloud Audit Logs against the permissions granted by its assigned roles. "
                "It calculates an excess permission score and automatically generates a right-sized role recommendation. SREs can inspect these recommendations "
                "via the Policy Intelligence API or apply them automatically to shrink the organization's attack surface."
            ),
            "preview": (
                "A backend microservice uses only 3 permissions out of the 1,200 permissions granted by primitive Editor. "
                "The IAM Recommender identifies the 99.8% excess permission ratio and provides an automated, non-breaking right-sizing recommendation."
            ),
            "technical": (
                "### 1. Recommender Algorithm and Observation Window\n"
                "- **The 90-Day Sliding Window:** The Recommender analyzes historical API calls captured in Cloud Audit Logs over the preceding 90 days.\n"
                "- **Security Insight Scoring:** For each IAM binding, the Recommender calculates the ratio of used permissions to total granted permissions:\n"
                "  $$\\text{Excess Ratio} = 1.0 - \\left( \\frac{\\text{Unique Permissions Exercised}}{\\text{Total Permissions Granted}} \\right)$$\n"
                "- If the excess ratio exceeds 80% with zero critical operations exercised, the Recommender flags the identity as an over-privileged security risk.\n\n"
                "### 2. Recommendation Subtypes and Risk Levels\n"
                "- **Role Replacement:** Suggests replacing a broad role (`roles/editor`) with one or more specific predefined roles (e.g. `roles/pubsub.publisher` and `roles/datastore.user`).\n"
                "- **Role Revocation:** If an identity has exercised zero permissions over 90 days, the Recommender suggests complete revocation of the binding.\n\n"
                "### 3. Operational Caveats and Guardrails\n"
                "- **Disaster Recovery Blind Spot:** Rare operations executed only during annual Game Days or emergency disaster recovery drills will not appear "
                "in a 90-day log window. Blindly applying recommendations can break emergency failover capabilities.\n"
                "- **Pre-Commit Verification:** High-risk recommendations must be reviewed by security leads before automated terraform application."
            ),
            "questions": [
                "How does the IAM Recommender determine which permissions were actively exercised by a service account over the preceding 90 days?",
                "Why can blindly applying IAM Recommender proposals break rare operational workflows such as disaster recovery failovers?",
                "What is the difference between a Role Replacement recommendation and a Role Revocation recommendation?",
            ],
            "reference": "https://docs.cloud.google.com/recommender/docs/recommenders/iam-recommender",
            "reference_label": "Google Cloud Recommender: IAM role recommendations and Policy Intelligence API",
            "scenario": {
                "symptom": (
                    "Security audit detected that 140 service accounts across the engineering organization were assigned `roles/owner` or `roles/editor`, "
                    "posing an acute compliance failure under SOC 2 Type II trust criteria."
                ),
                "constraints": (
                    "Must right-size service account permissions across all 140 identities without disrupting running production microservices."
                ),
                "evidence": (
                    "The IAM Recommender identified that 138 of the 140 service accounts exercised fewer than 6 unique permissions over the last 90 days, "
                    "with an average excess permission score of 99.4%."
                ),
                "diagnostic_steps": [
                    "Query the Recommender API for `google.iam.role.Recommender` across the organization.",
                    "Review the recommended role replacements for each service account.",
                    "Cross-reference recommendations against documented disaster recovery runbooks to ensure no rare failover permissions are stripped.",
                ],
                "root": (
                    "Permission creep and convenience-driven provisioning: initial developer setup used broad primitive roles and was never audited."
                ),
                "fix": (
                    "Script an automated migration applying the Recommender's proposed predefined role replacements. Mark applied recommendations "
                    "as `CLAIMED` and `SUCCEEDED` in the Recommender API."
                ),
                "verify": (
                    "Inspect IAM policy bindings post-remediation; confirm all 140 service accounts possess only the recommended granular roles. "
                    "Run automated regression tests to verify zero microservice disruptions."
                ),
                "residual": (
                    "Periodic review cycles (quarterly) are required to capture new service accounts provisioned by growing engineering teams."
                ),
                "diagram": (
                    "140 service accounts with Editor",
                    "Recommender analyzes 90-day audit logs",
                    "99.4% excess permissions detected",
                    "Granular role substitutions applied",
                    "Attack surface reduced by 99%; 0 outages"
                )
            },
            "lab": {
                "name": "IAM Recommender API Analysis and Automated Role Right-Sizing Simulation",
                "goal": "Author a script querying IAM Recommender recommendations and build an automated simulation parsing excess permission scores and applying right-sized substitutions.",
                "expected": "A validated shell script querying the Recommender API and an executable Python script calculating excess permission scores and executing role replacement.",
                "mode": "tabletop analysis & Python execution",
                "prereq": "Understanding of IAM Recommender schemas and Policy Intelligence.",
                "preflight": "Review Recommender API CLI documentation and command syntax.",
                "steps": [
                    "Author the shell script querying the IAM Recommender for active role recommendations (`query_iam_recommender.sh`):\n\n```sh\ncat <<'EOF' > query_iam_recommender.sh\n#!/usr/bin/env bash\nset -euo pipefail\n\n# Query IAM Recommender for Over-Privileged Role Bindings\nPROJECT_ID=\"brightloaf-prod\"\nLOCATION=\"global\"\nRECOMMENDER=\"google.iam.role.Recommender\"\n\necho \"=== Querying Active IAM Role Recommendations ===\"\ncat <<COMMAND\ngcloud recommender recommendations list \\\n    --project=\"$PROJECT_ID\" \\\n    --location=\"$LOCATION\" \\\n    --recommender=\"$RECOMMENDER\" \\\n    --format=\"table(name, primaryImpact.securityProjection.riskLevel, content.overview.recommendedAction)\"\nCOMMAND\nEOF\nchmod +x query_iam_recommender.sh\n./query_iam_recommender.sh\n```",
                    "Author an automated Python simulation calculating excess permission scores and executing non-breaking role replacement:\n\n```sh\ncat <<'EOF' > simulate_iam_recommender.py\n# Simulation of IAM Recommender Evaluation and Right-Sizing Engine\nimport json\n\nclass IdentityRoleAudit:\n    def __init__(self, principal, current_role, total_permissions_in_role, exercised_permissions):\n        self.principal = principal\n        self.current_role = current_role\n        self.total_granted = total_permissions_in_role\n        self.exercised = set(exercised_permissions)\n        \n    def calculate_excess_ratio(self):\n        used_count = len(self.exercised)\n        return round((1.0 - (used_count / self.total_granted)), 4)\n        \n    def recommend_replacement(self):\n        ratio = self.calculate_excess_ratio()\n        if ratio > 0.90:\n            # High-risk over-privileged identity: suggest replacement\n            return {\n                \"action\": \"REPLACE_ROLE\",\n                \"principal\": self.principal,\n                \"remove_role\": self.current_role,\n                \"add_role\": \"roles/pubsub.publisher\",\n                \"excess_score\": f\"{ratio * 100:.2f}%\",\n                \"risk_level\": \"CRITICAL\"\n            }\n        return {\"action\": \"MAINTAIN_ROLE\", \"risk_level\": \"LOW\"}\n\n# Scenario: Order Publisher Service Account assigned primitive roles/editor (1,200 permissions), but only uses 2\naudit = IdentityRoleAudit(\n    principal=\"serviceAccount:order-publisher@brightloaf-prod.iam.gserviceaccount.com\",\n    current_role=\"roles/editor\",\n    total_permissions_in_role=1200,\n    exercised_permissions=[\"pubsub.topics.publish\", \"pubsub.topics.get\"]\n)\n\nrecommendation = audit.recommend_replacement()\nprint(\"=== IAM RECOMMENDER ANALYSIS RESULT ===\")\nprint(json.dumps(recommendation, indent=2))\n\nassert recommendation[\"action\"] == \"REPLACE_ROLE\", \"Recommender failed to recommend replacement!\"\nassert recommendation[\"add_role\"] == \"roles/pubsub.publisher\", \"Incorrect replacement role suggested!\"\nprint(\"\nPASS: IAM Recommender excess permission score and role right-sizing validated successfully.\")\nEOF\npython3 simulate_iam_recommender.py\n```",
                    "Review all output artifacts and confirm that the shell script and Python simulation execute cleanly."
                ],
                "verification": "The shell script targets the standard Recommender API path and the Python simulation calculates the exact excess ratio and suggests the least-privilege replacement role.",
                "trouble": "Ensure Recommender API (`recommender.googleapis.com`) is enabled in the target project before executing queries.",
                "cleanup": "Retain `query_iam_recommender.sh` as an exit evidence artifact.",
                "accept": "Completed Recommender query script and verified right-sizing simulation. File: `day-099-topic-03-iam-recommender.md`.",
                "file": "day-099-topic-03-iam-recommender.md"
            }
        },
        {
            "key": "topic-04",
            "title": "IAM Conditions: Time, Resource, and Attribute-Based Access Control",
            "overview": (
                "IAM Conditions allow security architects to define conditional attribute-based access control (ABAC) using the Common Expression Language (CEL). "
                "Rather than granting static, permanent permissions, a conditional IAM binding takes effect only when specific boolean criteria are met—such as "
                "a temporary time window (`request.time < timestamp('...')`), a specific resource name prefix (`resource.name.startsWith('...')`), "
                "or a validated client IP range. IAM Conditions enable automated break-glass access, restrict storage administrator permissions to "
                "dev/staging buckets, and ensure production deployments are restricted to business hours."
            ),
            "preview": (
                "An engineer needs temporary 2-hour access to inspect production database logs during an incident. "
                "Configuring an IAM condition automatically revokes the role binding when the expiration timestamp elapses, requiring zero manual cleanup."
            ),
            "technical": (
                "### 1. Common Expression Language (CEL) Syntax in Cloud IAM\n"
                "- CEL expressions evaluate to a boolean (`true` or `false`). If true, the permission is granted; if false, the binding is ignored.\n"
                "- **Available Attributes:**\n"
                "  - `request.time`: Timestamp of the API call.\n"
                "  - `resource.name`: Fully qualified GCP resource path (e.g. `//storage.googleapis.com/projects/_/buckets/brightloaf-staging-*`).\n"
                "  - `resource.type`: Resource API type (e.g. `compute.googleapis.com/Instance`).\n"
                "  - `resource.tagValue`: Tags attached to the resource.\n\n"
                "### 2. Core Conditional Patterns\n"
                "- **Time-Bound (Temporary Break-Glass) Access:**\n"
                "  `request.time >= timestamp('2026-09-28T14:00:00Z') && request.time < timestamp('2026-09-28T16:00:00Z')`\n"
                "- **Resource Prefix Isolation:**\n"
                "  `resource.type == 'storage.googleapis.com/Bucket' && resource.name.startsWith('projects/_/buckets/brightloaf-dev-')`\n"
                "- **IP-Restricted Access (Context-Aware Access):** Enforces that access is granted only when the caller's IP matches corporate VPN gateways.\n\n"
                "### 3. Fail-Closed Behavior and Limits\n"
                "- If a CEL expression encounters an un-parseable condition or missing attribute, it **fails closed** (access is denied).\n"
                "- A single IAM policy binding can contain at most one condition expression."
            ),
            "questions": [
                "How do time-bound CEL conditions eliminate the operational risk of orphaned permissions after emergency incident remediation?",
                "What failure mode occurs if a CEL expression attempts to evaluate an attribute that does not exist on the target resource?",
                "How can resource prefix matching in IAM conditions enforce environment isolation across development and production buckets?",
            ],
            "reference": "https://docs.cloud.google.com/iam/docs/conditions-overview",
            "reference_label": "Google Cloud IAM: Overview of IAM Conditions and CEL expression syntax",
            "scenario": {
                "symptom": (
                    "A contractor granted 4-hour emergency debugging access to production Cloud SQL during a Sev-1 incident retained their administrative "
                    "database credentials for 9 months after their contract ended, violating SOC 2 compliance."
                ),
                "constraints": (
                    "Must establish an automated break-glass provisioning model that enforces automatic permission expiration without relying on manual revocation."
                ),
                "evidence": (
                    "IAM policy review showed the contractor's email held `roles/cloudsql.admin` without any condition block or expiration timestamp attached."
                ),
                "diagnostic_steps": [
                    "Audit project IAM policy bindings via the Resource Manager get-iam-policy API filtered by contractor domain.",
                    "Review incident ticket history to verify when the emergency access was requested.",
                    "Confirm whether an automated revocation workflow or calendar reminder failed to trigger.",
                ],
                "root": (
                    "Static role assignment without temporal boundaries: relying on human memory to revoke emergency permissions guarantees orphaned access."
                ),
                "fix": (
                    "Apply emergency role bindings exclusively with time-bound CEL conditions: `request.time < timestamp('2026-09-28T16:00:00Z')`. "
                    "The role automatically ceases to grant access the instant the timestamp passes."
                ),
                "verify": (
                    "Simulate an API call before the timestamp (access granted) and after the timestamp (access denied with 403 Forbidden)."
                ),
                "residual": (
                    "Expired conditional bindings remain visible in the IAM policy JSON until cleaned up; however, they cannot authorize any actions."
                ),
                "diagram": (
                    "Emergency incident declared",
                    "Time-bound CEL condition applied",
                    "Engineer accesses DB for 2 hours",
                    "Expiration timestamp elapses (16:00)",
                    "Access automatically revokes; 0 orphan grants"
                )
            },
            "lab": {
                "name": "Time-Bound and Resource-Scoped IAM Condition Implementation",
                "goal": "Author production IAM configuration scripts applying time-bound and prefix-scoped CEL conditions and verify evaluation logic via Python.",
                "expected": "A validated shell deployment script applying CEL conditions and an executable Python CEL evaluator proving access cutoff.",
                "mode": "tabletop analysis & Python execution",
                "prereq": "Understanding of CEL expressions and IAM policy binding syntax.",
                "preflight": "Review conditional IAM policy binding parameters and CEL condition syntax.",
                "steps": [
                    "Author the shell script applying a time-bound break-glass IAM condition (`apply_conditional_iam_grant.sh`):\n\n```sh\ncat <<'EOF' > apply_conditional_iam_grant.sh\n#!/usr/bin/env bash\nset -euo pipefail\n\n# Enterprise Conditional IAM Grant Deployment\nPROJECT_ID=\"brightloaf-prod\"\nENGINEER_EMAIL=\"oncall-sre@brightloaf.com\"\nEXPIRATION=\"2026-09-28T18:00:00Z\"\n\necho \"=== Applying Time-Bound Break-Glass IAM Condition ===\"\ncat <<COMMAND\ngcloud projects add-iam-policy-binding \"$PROJECT_ID\" \\\n    --member=\"user:$ENGINEER_EMAIL\" \\\n    --role=\"roles/cloudsql.admin\" \\\n    --condition=\"expression=request.time < timestamp('$EXPIRATION'),title=emergency_break_glass,description=Emergency 2-hour debugging access\"\nCOMMAND\n\necho \"\n=== Applying Resource Prefix Scoped IAM Condition ===\"\ncat <<COMMAND\ngcloud projects add-iam-policy-binding \"$PROJECT_ID\" \\\n    --member=\"user:$ENGINEER_EMAIL\" \\\n    --role=\"roles/storage.admin\" \\\n    --condition=\"expression=resource.name.startsWith('projects/_/buckets/brightloaf-staging-'),title=staging_only_storage,description=Restrict storage admin to staging buckets\"\nCOMMAND\nEOF\nchmod +x apply_conditional_iam_grant.sh\n./apply_conditional_iam_grant.sh\n```",
                    "Author an automated Python simulation modeling CEL condition evaluation against current time and resource names:\n\n```sh\ncat <<'EOF' > evaluate_cel_conditions.py\n# Simulation of Google Cloud IAM Common Expression Language (CEL) Evaluation\nimport datetime\n\ndef evaluate_time_condition(request_time_iso, expiration_iso):\n    req_dt = datetime.datetime.fromisoformat(request_time_iso.replace(\"Z\", \"+00:00\"))\n    exp_dt = datetime.datetime.fromisoformat(expiration_iso.replace(\"Z\", \"+00:00\"))\n    return req_dt < exp_dt\n\ndef evaluate_resource_condition(resource_name, allowed_prefix):\n    return resource_name.startswith(allowed_prefix)\n\nEXPIRATION_TIME = \"2026-09-28T18:00:00Z\"\nSTAGING_PREFIX = \"projects/_/buckets/brightloaf-staging-\"\n\n# Test 1: Access during emergency window (15:30 UTC)\nreq1_time = \"2026-09-28T15:30:00Z\"\nis_valid1 = evaluate_time_condition(req1_time, EXPIRATION_TIME)\nprint(f\"Request at {req1_time} (Before Expiration): {'PERMITTED' if is_valid1 else 'DENIED'}\")\nassert is_valid1, \"Valid emergency access was incorrectly denied!\"\n\n# Test 2: Access after emergency window (18:05 UTC)\nreq2_time = \"2026-09-28T18:05:00Z\"\nis_valid2 = evaluate_time_condition(req2_time, EXPIRATION_TIME)\nprint(f\"Request at {req2_time} (After Expiration):  {'PERMITTED' if is_valid2 else 'DENIED'}\")\nassert not is_valid2, \"Expired emergency access was incorrectly permitted!\"\n\n# Test 3: Resource prefix validation on Staging bucket\nres_staging = \"projects/_/buckets/brightloaf-staging-media\"\nis_staging_ok = evaluate_resource_condition(res_staging, STAGING_PREFIX)\nprint(f\"Access to {res_staging}: {'PERMITTED' if is_staging_ok else 'DENIED'}\")\nassert is_staging_ok, \"Staging bucket access was denied!\"\n\n# Test 4: Resource prefix validation on Prod bucket\nres_prod = \"projects/_/buckets/brightloaf-prod-media\"\nis_prod_ok = evaluate_resource_condition(res_prod, STAGING_PREFIX)\nprint(f\"Access to {res_prod}:    {'PERMITTED' if is_prod_ok else 'DENIED'}\")\nassert not is_prod_ok, \"Prod bucket access should be blocked by prefix condition!\"\n\nprint(\"\nPASS: CEL condition evaluation logic mathematically verified!\")\nEOF\npython3 evaluate_cel_conditions.py\n```",
                    "Review all output artifacts and confirm that the shell script and Python CEL evaluation simulator execute cleanly."
                ],
                "verification": "The shell script applies valid CEL syntax with timestamp and prefix checks, and the Python test confirms automatic access cutoff when the expiration window passes.",
                "trouble": "Ensure timestamps in CEL conditions adhere to RFC 3339 format enclosed in `timestamp('...')`.",
                "cleanup": "Retain `apply_conditional_iam_grant.sh` as an exit evidence artifact.",
                "accept": "Completed conditional IAM script and verified CEL simulation. File: `day-099-topic-04-iam-conditions.md`.",
                "file": "day-099-topic-04-iam-conditions.md"
            }
        },
        {
            "key": "topic-05",
            "title": "IAM Deny Policies and Principal Access Boundaries",
            "overview": (
                "For over a decade, Google Cloud IAM was additive: an Allow rule granted at any hierarchy level gave permanent access regardless of "
                "child project configuration. **IAM Deny Policies** introduce absolute negative guardrails that override all Allow policies, ensuring that "
                "even a Project Owner cannot perform specific high-risk operations. Complementing Deny policies, **Principal Access Boundaries (PABs)** "
                "restrict the set of resources an identity can access across the entire cloud estate, preventing compromised service accounts or rogue "
                "contractors from touching production assets regardless of what permissions they hold."
            ),
            "preview": (
                "An attacker gains Project Owner credentials and attempts to create a persistent service account private key to maintain access. "
                "An Organization Deny policy permanently blocks service account key creation across all projects, thwarting persistence."
            ),
            "technical": (
                "### 1. Deterministic Policy Evaluation Hierarchy\n"
                "- When an API call arrives at Google Cloud, the IAM evaluation engine evaluates rules in strict sequence:\n"
                "  1. **Deny Policy Check:** Evaluates Deny policies from Organization &rarr; Folder &rarr; Project. If any Deny matches the principal, "
                "resource, and permission, the request is **immediately terminated with HTTP 403 Forbidden**. Allow rules are never evaluated.\n"
                "  2. **Principal Access Boundary (PAB) Check:** Confirms the target resource is explicitly listed within the principal's allowed boundary.\n"
                "  3. **Allow Policy & Condition Check:** Evaluates Allow bindings from Organization down to Resource. If matching permission is found "
                "and any attached CEL conditions evaluate to `true`, access is granted.\n\n"
                "### 2. Anatomy of an IAM Deny Policy\n"
                "- Deny policies are managed via the IAM deny-policies API:\n"
                "  - `deniedPrincipals`: Who is blocked (e.g. `principalSet://goog/public:all`).\n"
                "  - `exceptionPrincipals`: Whitelisted emergency bypass identities (e.g. break-glass break-glass-admin@brightloaf.com).\n"
                "  - `deniedPermissions`: Exact API permissions blocked (e.g. `iam.googleapis.com/serviceAccountKeys.create`).\n"
                "  - `denialCondition`: Optional CEL condition restricting when the deny applies.\n\n"
                "### 3. Principal Access Boundaries (PABs)\n"
                "- A Principal Access Boundary policy binds to an identity, declaring a strict resource envelope:\n"
                "  `allowedResources: ['//cloudresourcemanager.googleapis.com/projects/brightloaf-staging-*']`.\n"
                "- Even if the identity is granted `roles/owner` in `brightloaf-prod`, the PAB intercepts and blocks the call."
            ),
            "questions": [
                "Why do IAM Deny policies take precedence over all Allow policies across the Google Cloud resource hierarchy?",
                "How does an organization-level Deny policy on `iam.serviceAccountKeys.create` eliminate credential exfiltration vulnerabilities?",
                "What is the architectural distinction between a resource-level Deny policy and a Principal Access Boundary?",
            ],
            "reference": "https://docs.cloud.google.com/iam/docs/deny-overview",
            "reference_label": "Google Cloud IAM: Deny policies overview, syntax, and evaluation rules",
            "scenario": {
                "symptom": (
                    "Security Operations detected an unknown IP address downloading 500 GiB of data using a service account private key file (`key.json`) "
                    "that had been created by a developer 8 months prior and leaked in a public GitHub repository."
                ),
                "constraints": (
                    "Must enforce an organization-wide ban on user-managed service account key creation while permitting workload identity federation."
                ),
                "evidence": (
                    "Cloud Audit Logs showed `CreateServiceAccountKey` was invoked 12 times in the last year across various child projects by developers "
                    "bypassing corporate Single Sign-On."
                ),
                "diagnostic_steps": [
                    "Audit existing service account keys via the service account keys list API across all projects.",
                    "Review organization policy constraints (`iam.disableServiceAccountKeyCreation`).",
                    "Inspect IAM Deny policies defined at the organization root.",
                ],
                "root": (
                    "Absence of negative guardrails: relying on developers to follow policy guidelines without enforcing an architectural Deny policy "
                    "allowed private key credential generation."
                ),
                "fix": (
                    "Deploy an Organization IAM Deny Policy blocking `iam.googleapis.com/serviceAccountKeys.create` for all principals except the automated "
                    "Terraform deployment pipeline. Enforce the `iam.disableServiceAccountKeyCreation` Org Policy constraint."
                ),
                "verify": (
                    "Attempt to generate a service account key using Project Owner credentials; verify the API returns HTTP 403 with message: "
                    "`Access denied by Deny Policy`."
                ),
                "residual": (
                    "Deny policies do not automatically delete existing historical keys; an active remediation script must revoke pre-existing keys."
                ),
                "diagram": (
                    "Developer attempts to create service account key",
                    "Organization Deny Policy intercepts request",
                    "Key creation blocked with 403 Forbidden",
                    "Zero downloadable private keys exist",
                    "Workload Identity Federation enforced"
                )
            },
            "lab": {
                "name": "Organization IAM Deny Policy Specification and Policy Evaluation Simulator",
                "goal": "Author a declarative organization IAM Deny policy JSON blocking service account key creation and simulate deterministic policy evaluation.",
                "expected": "A validated Deny policy JSON manifest, an executable Python evaluation engine proving Deny overrides Allow, and an authorization matrix.",
                "mode": "tabletop analysis & JSON/Python execution",
                "prereq": "Understanding of Google Cloud Resource Manager and IAM Deny policies.",
                "preflight": "Review IAM deny-policies CLI documentation and schema.",
                "steps": [
                    "Author the declarative Organization IAM Deny policy JSON manifest (`org_deny_key_creation.json`):\n\n```sh\ncat <<'EOF' > org_deny_key_creation.json\n{\n  \"name\": \"policies/org-deny-sa-key-creation\",\n  \"displayName\": \"Block Service Account Key Creation Organization-Wide\",\n  \"rules\": [\n    {\n      \"denyRule\": {\n        \"deniedPrincipals\": [\n          \"principalSet://goog/public:all\"\n        ],\n        \"exceptionPrincipals\": [\n          \"principal://iam.googleapis.com/projects/123456789012/locations/global/workloadIdentityPools/github-actions/subject/repo:brightloaf/infra\"\n        ],\n        \"deniedPermissions\": [\n          \"iam.googleapis.com/serviceAccountKeys.create\"\n        ],\n        \"denialCondition\": {\n          \"title\": \"always_deny_key_creation\",\n          \"expression\": \"true\"\n        }\n      }\n    }\n  ]\n}\nEOF\ncat org_deny_key_creation.json\n```",
                    "Author an automated Python simulation verifying the deterministic IAM evaluation order (Deny overrides Allow):\n\n```sh\ncat <<'EOF' > simulate_deterministic_iam.py\n# Deterministic IAM Policy Evaluation Engine (Deny overrides Allow)\n\nclass IAMDecisionEngine:\n    def __init__(self, deny_rules, allow_rules):\n        self.deny_rules = deny_rules\n        self.allow_rules = allow_rules\n        \n    def evaluate_request(self, principal, permission):\n        # Step 1: Evaluate Deny Policies First\n        for rule in self.deny_rules:\n            if permission in rule[\"denied_permissions\"]:\n                if principal not in rule.get(\"exceptions\", []):\n                    return False, f\"DENIED by Deny Policy '{rule['name']}' (Deny overrides Allow)\"\n                    \n        # Step 2: Evaluate Allow Policies (Only reached if no Deny matched)\n        for allow in self.allow_rules:\n            if permission in allow[\"permissions\"]:\n                return True, f\"ALLOWED by Role Binding '{allow['role']}'\"\n                \n        return False, \"DENIED: No matching Allow rule found (Implicit Deny)\"\n\ndeny_rules = [\n    {\n        \"name\": \"org-deny-sa-key-creation\",\n        \"denied_permissions\": [\"iam.serviceAccountKeys.create\"],\n        \"exceptions\": [\"serviceAccount:break-glass-admin@brightloaf.com\"]\n    }\n]\n\n# User holds primitive roles/owner which normally allows all permissions\nallow_rules = [\n    {\n        \"role\": \"roles/owner\",\n        \"permissions\": [\n            \"iam.serviceAccountKeys.create\",\n            \"compute.instances.create\",\n            \"storage.buckets.create\"\n        ]\n    }\n]\n\nengine = IAMDecisionEngine(deny_rules, allow_rules)\n\n# Case 1: Project Owner attempts to create a Compute VM (Allowed)\nallowed_vm, msg_vm = engine.evaluate_request(\"user:project-owner@brightloaf.com\", \"compute.instances.create\")\nprint(f\"Create VM Request:       {msg_vm}\")\nassert allowed_vm, \"VM creation should be allowed!\"\n\n# Case 2: Project Owner attempts to create a Service Account Key (Blocked by Deny Policy despite Owner role)\nallowed_key, msg_key = engine.evaluate_request(\"user:project-owner@brightloaf.com\", \"iam.serviceAccountKeys.create\")\nprint(f\"Create SA Key Request:   {msg_key}\")\nassert not allowed_key, \"Deny policy failed to block SA key creation!\"\nassert \"Deny overrides Allow\" in msg_key, \"Evaluation order incorrect!\"\n\n# Case 3: Whitelisted Emergency Break-Glass identity creates SA Key (Allowed by Exception)\nallowed_bg, msg_bg = engine.evaluate_request(\"serviceAccount:break-glass-admin@brightloaf.com\", \"iam.serviceAccountKeys.create\")\nprint(f\"Break-Glass Key Request: {msg_bg}\")\nassert allowed_bg, \"Break-glass exception should be allowed!\"\n\nprint(\"\nPASS: Deterministic IAM policy evaluation sequence verified successfully!\")\nEOF\npython3 simulate_deterministic_iam.py\n```",
                    "Author the complete authorization decision matrix fulfilling Day 99 exit evidence (`day-099-topic-05-decision-matrix.md`):\n\n```sh\ncat <<'EOF' > day-099-topic-05-decision-matrix.md\n# Day 99: Enterprise Authorization Decision Matrix & Remediation Certificate\n\n## 1. Deterministic Evaluation Decision Matrix\n| Requesting Principal | Target Permission | Attached Allow Roles | Organization Deny Rule | CEL Condition | Evaluation Decision & Rationale |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n| `dev@brightloaf.com` | `compute.instances.create` | `roles/editor` | None | None | **PERMITTED:** Standard allow binding. |\n| `owner@brightloaf.com` | `iam.serviceAccountKeys.create`| `roles/owner` | `org-deny-sa-key-creation` | None | **DENIED:** Deny policy overrides Owner Allow. |\n| `break-glass@brightloaf`| `iam.serviceAccountKeys.create`| `roles/owner` | Exception identity | None | **PERMITTED:** Whitelisted exception in Deny rule. |\n| `oncall@brightloaf.com`| `cloudsql.admin` | `roles/cloudsql.admin` | None | `request.time < 18:00` | **PERMITTED (if <18:00):** CEL condition satisfied. |\n| `oncall@brightloaf.com`| `cloudsql.admin` | `roles/cloudsql.admin` | None | `request.time >= 18:00`| **DENIED:** CEL condition expired (fail-closed). |\n\n## 2. Corrected Excessive Grant Record\n- **Identified Violation:** CI/CD runner `ci-runner-build@brightloaf-prod.iam.gserviceaccount.com` assigned primitive `roles/editor` (1,200 permissions).\n- **Excess Permission Ratio:** **99.6%** (Only 5 permissions exercised in 90 days).\n- **Remediation Executed:** Primitive `roles/editor` revoked; replaced with granular predefined roles `roles/run.developer` and `roles/artifactregistry.writer`.\n- **Residual Verification:** Microservice deployment passes; database and security deletion requests return HTTP 403 Forbidden.\nEOF\ncat day-099-topic-05-decision-matrix.md\n```",
                    "Review all output artifacts and confirm that the Deny policy JSON, Python evaluation engine, and authorization decision matrix fulfill Day 99 Exit evidence criteria."
                ],
                "verification": "The Deny policy JSON conforms to the standard Google Cloud schema, the Python simulation proves Deny precedence over primitive Owner Allows, and the decision matrix documents all evaluation paths.",
                "trouble": "Ensure permission names in Deny policies use the full resource service prefix (e.g. `iam.googleapis.com/serviceAccountKeys.create`).",
                "cleanup": "Retain `org_deny_key_creation.json` and `day-099-topic-05-decision-matrix.md` as exit evidence artifacts.",
                "accept": "Completed Organization Deny policy specification and verified authorization decision matrix. File: `day-099-topic-05-deny-policies.md`.",
                "file": "day-099-topic-05-deny-policies.md"
            }
        }
    ]
}
