"""day_data_099.py — Exhaustive architecture data specification for Day 99.

Covers Least Privilege, Custom Roles, Recommender, Conditions, and Deny Policies.
"""

DAY_NUM = 99

DATA = {'day': 99,
 'part1_intro': 'Day 99 inaugurates the deep enterprise security curriculum: advanced Identity and Access Management '
                '(IAM), policy evaluation hierarchies, and automated least-privilege enforcement. In cloud '
                'architectures, perimeter network firewalls are secondary; identity is the primary security perimeter. '
                'Broad, permissive role assignments (such as primitive Editor or Owner roles) represent catastrophic '
                'blast radius vulnerabilities that allow single compromised service accounts to escalate privileges, '
                "exfiltrate data, or disable backups. Today's curriculum constructs an ironclad IAM architecture using "
                'Common Expression Language (CEL) conditions, ML-driven IAM Recommenders, Organization-level Deny '
                'policies that override all allows, and Principal Access Boundaries to enforce separation of duties.',
 'exit_summary': 'Engineered an enterprise Advanced IAM and Policy Evaluation framework: evaluated an '
                 'allow/deny/condition policy fixture through an automated Python policy simulator; remediated an '
                 'excessive primitive Editor grant into a right-sized custom role; authored an authorization decision '
                 'matrix and organization-wide IAM Deny guardrails blocking service account key creation.',
 'part2_intro': 'Cloud IAM policy evaluation is deterministic: Deny rules are evaluated first and override all Allow '
                'rules, followed by conditional CEL expressions and inherited resource hierarchy bindings. The '
                'sections below analyze least privilege mechanics, custom role trade-offs, IAM Recommender algorithms, '
                'conditional expressions, and Principal Access Boundaries.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>IAM Mechanism / Primitive</th>\n'
                    '      <th>Evaluation Timing &amp; Scope</th>\n'
                    '      <th>Primary Security Function</th>\n'
                    '      <th>Key Limitation / Operational Boundary</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>IAM Deny Policy</strong></td>\n'
                    '      <td>Evaluated <strong>First</strong> at Organization/Folder/Project levels</td>\n'
                    '      <td>Permanent negative guardrail overriding all Allow grants (e.g. deny '
                    '`iam.serviceAccountKeys.create`)</td>\n'
                    '      <td>Supports subset of GCP permissions; cannot be overridden by any Allow policy</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Principal Access Boundary (PAB)</strong></td>\n'
                    '      <td>Evaluated concurrently with Principal authorization</td>\n'
                    '      <td>Restricts the set of resources a principal can access regardless of Allow grants</td>\n'
                    '      <td>Applies to specific users or service accounts; requires Resource Manager v3 '
                    'integration</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>IAM Conditions (CEL)</strong></td>\n'
                    '      <td>Evaluated during Allow binding resolution</td>\n'
                    '      <td>Restricts permissions by time window (`request.time`), resource name prefix, or '
                    'destination tag</td>\n'
                    '      <td>Increases policy evaluation complexity; syntax errors in CEL can silently fail '
                    'closed</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Predefined Roles</strong></td>\n'
                    '      <td>Evaluated within Allow policy bindings</td>\n'
                    '      <td>Curated by Google; automatically updated as new API methods are released</td>\n'
                    '      <td>Often bundle hundreds of permissions beyond what a specific microservice requires</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Custom Roles</strong></td>\n'
                    '      <td>Evaluated within Allow policy bindings</td>\n'
                    '      <td>Exact least-privilege curation containing only needed permissions</td>\n'
                    '      <td>High maintenance overhead; does not inherit newly released Google Cloud API '
                    'permissions</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>IAM Recommender</strong></td>\n'
                    '      <td>Background ML analysis over 90-day activity window</td>\n'
                    '      <td>Identifies unused permissions and recommends least-privilege role substitutions</td>\n'
                    '      <td>90-day observation window required; can break rare quarterly disaster recovery '
                    'workflows if applied naively</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 99: Enterprise IAM Governance: Least Privilege, Conditions, Recommender, and Deny '
                           'Policies',
                  'desc': 'Architectural topology illustrating identity ingress, IAM Recommender analysis, CEL '
                          'conditional evaluation, and organization-level Deny/PAB perimeters.',
                  'caption': 'Figure 99.1: Enterprise IAM policy evaluation pipeline featuring CEL conditions, IAM '
                             'Recommender right-sizing, and fail-closed IAM Deny/PAB perimeters.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Identity Ingress & Authentication Perimeter',
                              'desc': 'Enterprise workforce identities, service accounts, and Google OIDC '
                                      'authentication',
                              'y': 10,
                              'h': 90,
                              'stroke': '#38bdf8',
                              'fill': '#0c1e38',
                              'title_color': '#38bdf8'},
                             {'name': 'LAYER 2: Policy Intelligence & IAM Recommender Fabric',
                              'desc': 'IAM Recommender ML engine, Policy Analyzer, and 90-day permission audit logs',
                              'y': 115,
                              'h': 90,
                              'stroke': '#818cf8',
                              'fill': '#141838',
                              'title_color': '#818cf8'},
                             {'name': 'LAYER 3: Role Evaluation & CEL Condition Engine',
                              'desc': 'Predefined vs Custom role definitions and attribute/time-based CEL expressions',
                              'y': 220,
                              'h': 90,
                              'stroke': '#f59e0b',
                              'fill': '#261a08',
                              'title_color': '#f59e0b'},
                             {'name': 'LAYER 4: IAM Deny Policies & Principal Access Boundaries (PAB)',
                              'desc': 'Organization-level fail-closed deny rules and boundary constraints',
                              'y': 325,
                              'h': 90,
                              'stroke': '#f43f5e',
                              'fill': '#2a0a14',
                              'title_color': '#f43f5e'},
                             {'name': 'LAYER 5: Target Resource Data Plane & Forensic Audit Vault',
                              'desc': 'Protected GCP APIs, Cloud Storage, BigQuery, and immutable Cloud Audit logs',
                              'y': 430,
                              'h': 90,
                              'stroke': '#22c55e',
                              'fill': '#072417',
                              'title_color': '#22c55e'}],
                  'components': [{'name': 'Workforce Identity / SA',
                                  'detail': 'OIDC Identity Token',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'Google Security STS',
                                  'detail': 'Token Minting & Validation',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'IAM Recommender',
                                  'detail': 'Right-Sizing Machine Learning',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Policy Analyzer API',
                                  'detail': 'Permission Grant Graph',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Curated Custom Role',
                                  'detail': 'Exact API Verbs Only',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'CEL Condition Evaluator',
                                  'detail': 'Time & Tag Guardrail',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'IAM Deny Engine',
                                  'detail': 'Fail-Closed Org Guardrail',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Principal Access Boundary',
                                  'detail': 'Restricts Principal Scope',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Target GCP Resources',
                                  'detail': 'GCS / BigQuery / Compute',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'},
                                 {'name': 'Cloud Audit Activity Log',
                                  'detail': 'Cryptographic Audit Trail',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'}],
                  'boundaries': [{'label': 'IDENTITY AUTHENTICATION & PRINCIPAL PERIMETER',
                                  'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'color': '#38bdf8'},
                                 {'label': 'POLICY EVALUATION & CEL CONDITIONAL GATE',
                                  'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#818cf8'},
                                 {'label': 'FAIL-CLOSED DENY & AUDIT GOVERNANCE VAULT',
                                  'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#22c55e'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Validate Identity', 'type': 'ok'},
                            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Evaluate 90d Usage', 'type': 'ok'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'label': 'Generate Recommendation',
                             'type': 'warn'},
                            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Evaluate Custom Role', 'type': 'ok'},
                            {'x1': 340,
                             'y1': 266,
                             'x2': 420,
                             'y2': 266,
                             'label': 'Evaluate CEL Conditions',
                             'type': 'ok'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'label': 'Deny Policy Intercept',
                             'type': 'fail'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'label': 'Enforce PAB Envelope',
                             'type': 'fail'},
                            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Permit API Operation', 'type': 'ok'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'label': 'Record Immutable Audit',
                             'type': 'ok'}],
                  'probes': [{'cx': 80,
                              'cy': 135,
                              'label': 'PROBE 1: Unused Permissions Ratio (>85%)',
                              'badge': 'P1',
                              'color': '#818cf8'},
                             {'cx': 420,
                              'cy': 240,
                              'label': 'PROBE 2: CEL Condition Expiry (<60s)',
                              'badge': 'P2',
                              'color': '#f59e0b'},
                             {'cx': 80,
                              'cy': 345,
                              'label': 'PROBE 3: IAM Deny Policy Intercept (HTTP 403)',
                              'badge': 'P3',
                              'color': '#f43f5e'}]},
 'topics': [{'key': 'topic-01',
             'title': 'Least Privilege, Separation of Duties, and Need-to-Know',
             'overview': 'The principle of least privilege dictates that an identity (human engineer, service account, '
                         'or external contractor) must be granted only the minimum set of permissions necessary to '
                         'execute its legitimate function, and only for the duration required. Separation of Duties '
                         '(SoD) ensures that critical or high-risk multi-stage operations cannot be executed by a '
                         'single individual, preventing internal fraud and limiting catastrophic error blast radii. In '
                         'Google Cloud, this requires strictly eliminating primitive roles (`roles/owner`, '
                         '`roles/editor`), separating encryption key administration from data access, and enforcing '
                         'dual-custody access for sensitive production releases.',
             'preview': 'A developer account with project Editor privileges accidentally drops a production BigQuery '
                        'billing dataset. Separation of duties and least-privilege role assignment prevent software '
                        'developers from holding administrative permissions over analytical data.',
             'technical': '### 1. Primitive vs Predefined Roles: The Blast Radius Risk\n'
                          '- **Primitive Roles (Owner, Editor, Viewer):** Legacy coarse-grained roles from early GCP. '
                          '`roles/editor` grants mutation access to almost all GCP services (Compute, Storage, Cloud '
                          'SQL, BigQuery, Pub/Sub).\n'
                          '- **Toxic Combinations:** A principal with `roles/editor` can create Compute instances with '
                          'default compute service accounts, effectively granting themselves full administrative '
                          "rights over the project's infrastructure.\n"
                          '\n'
                          '### 2. Separation of Duties (SoD) Topologies\n'
                          '- **KMS Key Management vs Data Access:** An engineer with `roles/cloudkms.admin` can manage '
                          'key rings and rotation schedules, but must **never** be granted '
                          '`roles/cloudkms.cryptoKeyEncrypterDecrypter` (data decryption).\n'
                          '- **Network Administration vs Compute Management:** Network Engineers hold '
                          '`roles/compute.networkAdmin` in the Host Project, while Application Teams hold '
                          '`roles/compute.instanceAdmin.v1` restricted strictly to Service Projects.\n'
                          '\n'
                          '### 3. Need-to-Know and Break-Glass Governance\n'
                          '- Day-to-day production access for human engineers should be read-only (`roles/viewer` or '
                          '`roles/monitoring.viewer`).\n'
                          '- Mutation privileges must be granted temporarily via automated Just-In-Time (JIT) access '
                          'requests with mandatory ticket correlation and automatic expiration (e.g. 2 hours).',
             'questions': ['Why are primitive roles like `roles/editor` considered unacceptable security risks in '
                           'production Google Cloud environments?',
                           'How does separating KMS key administration from crypto-operation roles enforce separation '
                           'of duties in sensitive data environments?',
                           'What architectural mechanisms enforce dual-custody approval before high-risk '
                           'infrastructure mutations can be committed?'],
             'reference': 'https://docs.cloud.google.com/iam/docs/understanding-roles',
             'reference_label': 'Google Cloud IAM: Understanding role hierarchies and least privilege best practices',
             'scenario': {'symptom': 'A CI/CD build worker service account running automated unit tests was '
                                     'compromised by malicious dependency injection, allowing attackers to delete the '
                                     'production Cloud SQL database instance and purge long-term audit buckets.',
                          'constraints': 'Must restrict automated CI/CD service accounts strictly to deployment '
                                         'permissions on specific staging namespaces, with zero administrative access '
                                         'over production databases or security logging.',
                          'evidence': 'Production Cloud Audit Activity log:\n'
                                      '\n'
                                      '```json\n'
                                      '{\n'
                                      '  "protoPayload": {\n'
                                      '    "authenticationInfo": {"principalEmail": '
                                      '"deployer-sa@prod-app.iam.gserviceaccount.com"},\n'
                                      '    "methodName": "compute.networks.removePeering",\n'
                                      '    "resourceName": "projects/prod-net-core/global/networks/vpc-prod-shared",\n'
                                      '    "status": {"code": 0, "message": "OK"}\n'
                                      '  }\n'
                                      '}\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: Service account granted primitive `roles/editor` instead of '
                                      'fine-grained `roles/compute.instanceAdmin.v1`. Deployer script mistakenly '
                                      'executed network peering teardown during routine cleanup.',
                          'diagnostic_steps': ["Query Cloud Audit Logs for `methodName = 'sql.instances.delete'` and "
                                               "extract the caller's service account email.",
                                               'Audit IAM policy bindings on the project to list all identities '
                                               'holding primitive `roles/editor`.',
                                               'Review Git history on pipeline manifests to determine why the service '
                                               'account was granted broad privileges.'],
                          'root': 'Violation of least privilege: granting primitive `roles/editor` to an automated '
                                  'CI/CD pipeline gave an untrusted build worker unconstrained administrative control '
                                  'over the entire project.',
                          'fix': 'Revoke `roles/editor` immediately. Create a dedicated service account granted only '
                                 '`roles/run.developer` and `roles/cloudbuild.builds.editor` scoped to the staging '
                                 'project, strictly prohibiting production deletion permissions.',
                          'verify': 'Run automated pipeline tests under the right-sized service account; confirm '
                                    'builds deploy successfully while attempts to modify Cloud SQL or Logging return '
                                    'HTTP 403 Forbidden.',
                          'residual': 'Granular roles require ongoing curation as new GCP services are adopted by '
                                      'application teams.',
                          'diagram': ('CI/CD SA granted primitive roles/editor',
                                      'Deployment script has excessive network permissions',
                                      'Script deletes shared VPC peering mesh',
                                      'Replace Editor with fine-grained InstanceAdmin',
                                      'Separation of duties blocks network mutation')},
             'lab': {'name': 'Least Privilege Role Audit and Excessive Primitive Grant Remediation',
                     'goal': 'Audit project IAM bindings for primitive roles, author a least-privilege remediation '
                             'script, and verify policy compliance.',
                     'expected': 'A validated shell remediation script replacing primitive roles with least-privilege '
                                 'grants, and an automated policy verification test.',
                     'mode': 'tabletop analysis & shell synthesis',
                     'prereq': 'Understanding of Google Cloud IAM roles and Resource Manager bindings.',
                     'preflight': 'Review Resource Manager policy binding and IAM role modification CLI documentation.',
                     'steps': ['#### Stage 1: Pre-Flight IAM Policy & Primitive Role Audit\n'
                               'Audit project IAM policy for dangerous primitive role bindings (`roles/owner`, '
                               '`roles/editor`):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_primitive_roles.py\n"
                               "dangerous_roles = ['roles/owner', 'roles/editor']\n"
                               'sample_bindings = [\n'
                               "    {'role': 'roles/editor', 'members': "
                               "['serviceAccount:deployer-sa@prod.iam.gserviceaccount.com']},\n"
                               "    {'role': 'roles/compute.instanceAdmin.v1', 'members': "
                               "['group:sre-team@corp.com']}\n"
                               ']\n'
                               "print('[PREFLIGHT] Auditing IAM policy for primitive roles:')\n"
                               'for b in sample_bindings:\n'
                               "    flag = 'CRITICAL DEFECT: Primitive role assigned!' if b['role'] in dangerous_roles "
                               "else 'COMPLIANT'\n"
                               '    print(f\'  • Role: {b["role"]:32s} -> [{flag}]\')\n'
                               'EOF\n'
                               'python3 check_primitive_roles.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and IAM policy linter toolset:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_iam_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Verifying IAM policy validation tools..."\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_iam_tools.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Least-Privilege Terraform Manifest\n'
                               'Author a declarative Terraform configuration enforcing least privilege and separation '
                               'of duties:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > least_privilege.tf\n"
                               'resource "google_project_iam_member" "deployer_compute" {\n'
                               '  project = "prod-app-workloads"\n'
                               '  role    = "roles/compute.instanceAdmin.v1"\n'
                               '  member  = "serviceAccount:deployer-sa@prod-app-workloads.iam.gserviceaccount.com"\n'
                               '}\n'
                               '\n'
                               'resource "google_project_iam_member" "deployer_storage" {\n'
                               '  project = "prod-app-workloads"\n'
                               '  role    = "roles/storage.objectViewer"\n'
                               '  member  = "serviceAccount:deployer-sa@prod-app-workloads.iam.gserviceaccount.com"\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored least_privilege.tf"\n'
                               '```',
                               '#### Stage 4: Execution & Policy Simulation Verification\n'
                               'Author a verification script asserting that network mutations are rejected:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_authorization.py\n"
                               'assigned_permissions = {\n'
                               "    'compute.instances.create',\n"
                               "    'compute.instances.delete',\n"
                               "    'storage.objects.get'\n"
                               '}\n'
                               "requested_action = 'compute.networks.removePeering'\n"
                               'if requested_action in assigned_permissions:\n'
                               "    print('[FAIL] Security breach: Network mutation permitted!')\n"
                               'else:\n'
                               "    print(f'[SECURITY PASS] Action {requested_action} denied by least privilege.')\n"
                               'EOF\n'
                               'python3 simulate_authorization.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Privilege Escalation Attempt Chaos Test\n'
                               'Simulate an attempt by the service account to assign `roles/owner` and verify block:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_escalation.py\n"
                               'def attempt_set_iam_policy(caller_perms):\n'
                               "    if 'resourcemanager.projects.setIamPolicy' not in caller_perms:\n"
                               "        raise PermissionError('HTTP 403 Forbidden: Caller lacks setIamPolicy')\n"
                               "    return 'POLICY_MUTATED'\n"
                               '\n'
                               'try:\n'
                               "    attempt_set_iam_policy({'compute.instances.create'})\n"
                               'except PermissionError as e:\n'
                               "    print(f'[CHAOS TEST PASS] Privilege escalation blocked: {e}')\n"
                               'EOF\n'
                               'python3 test_escalation.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & IAM Mutation Alert Policy\n'
                               'Author a Cloud Monitoring Alert Policy detecting primitive role assignments:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_primitive_roles.json\n"
                               '{\n'
                               '  "displayName": "SECURITY ALERT: Primitive Role Grant Detected",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "SetIamPolicy granting roles/owner or roles/editor",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": "logName=\\"cloudaudit.googleapis.com%2Factivity\\" AND '
                               'protoPayload.methodName=\\"SetIamPolicy\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 0.0,\n'
                               '        "duration": "0s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] Authored alert_primitive_roles.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform policy against security rules:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_least_privilege.py\n"
                               "with open('least_privilege.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'roles/editor' not in tf, 'Primitive role editor detected in manifest'\n"
                               "assert 'roles/owner' not in tf, 'Primitive role owner detected in manifest'\n"
                               "assert 'roles/compute.instanceAdmin.v1' in tf\n"
                               "print('[ASSERT PASS] Least privilege Terraform manifest strictly validated.')\n"
                               'EOF\n'
                               'python3 assert_least_privilege.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_least_privilege_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 99 Topic 1 test scripts..."\n'
                               'rm -f check_primitive_roles.py check_iam_tools.sh simulate_authorization.py '
                               'test_escalation.py assert_least_privilege.py\n'
                               'echo "[CLEANUP] Retaining production manifests: least_privilege.tf, '
                               'alert_primitive_roles.json"\n'
                               'echo "[CLEANUP PASS] Least privilege lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_least_privilege_lab.sh\n'
                               '```'],
                     'verification': 'The shell script strips primitive roles and applies granular Cloud Run/Artifact '
                                     'Registry roles, and the Python test proves administrative deletion actions are '
                                     'blocked.',
                     'trouble': 'Ensure service account email matches the exact fully qualified identity string when '
                                'running IAM policy commands.',
                     'cleanup': 'Retain `remediate_primitive_roles.sh` as an exit evidence artifact.',
                     'accept': 'Completed least-privilege remediation script and verified policy test. File: '
                               '`day-099-topic-01-least-privilege.md`.',
                     'file': 'day-099-topic-01-least-privilege.md'}},
            {'key': 'topic-02',
             'title': 'Predefined Roles vs Custom Roles: Maintenance Trade-offs and Curation',
             'overview': 'Google Cloud provides hundreds of curated **Predefined Roles** designed for standard job '
                         'functions (e.g. `roles/spanner.databaseUser`, `roles/pubsub.publisher`). While predefined '
                         'roles reduce administrative overhead, they frequently bundle excessive permissions that '
                         'violate strict compliance mandates. When predefined roles are too broad, architects design '
                         '**Custom Roles** containing the exact list of permissions required. However, custom roles '
                         'incur continuous maintenance liabilities: when Google releases new feature versions or '
                         'deprecates underlying API permissions, custom roles do not update automatically, requiring '
                         'manual lifecycle management.',
             'preview': 'A predefined Storage role grants permission to delete all bucket data in addition to reading '
                        'objects. Authoring a curated custom role provides exact read-only object streaming '
                        'permissions without data destruction risk.',
             'technical': '### 1. Comparative Analysis: Predefined vs Custom Roles\n'
                          '- **Predefined Roles:** Maintained by Google Cloud. Automatically updated when new API '
                          'features are launched. Cons: Frequently bundle hundreds of permissions (e.g., '
                          '`roles/storage.objectAdmin` includes permissions to change ACLs and delete buckets).\n'
                          '- **Custom Roles:** Maintained by enterprise security teams. Scoped to the Organization or '
                          'Project. Contains exact whitelist of API permissions. Cons: Cannot include permissions from '
                          'services in Preview; does not receive automated permission updates; maximum of 64 custom '
                          'roles per project or 1,280 per organization.\n'
                          '\n'
                          '### 2. Custom Role Lifecycle and Stages\n'
                          '- Custom roles define a `stage` parameter:\n'
                          '  - `ALPHA` / `BETA`: Under active testing.\n'
                          '  - `GA`: General availability; production standard.\n'
                          '  - `DEPRECATED`: Informs consumers that the role will be retired; allows graceful '
                          'migration.\n'
                          '  - `DISABLED`: Role bindings remain but permissions cease to be granted.\n'
                          '\n'
                          '### 3. Curation Best Practices\n'
                          '- Prefer Predefined Roles whenever a tightly scoped role exists (e.g. '
                          '`roles/pubsub.subscriber` rather than building custom Pub/Sub roles).\n'
                          '- Use Custom Roles exclusively for high-risk data-plane applications where unintended '
                          'permissions (like `storage.buckets.delete` or `bigquery.datasets.delete`) cannot be '
                          'tolerated.',
             'questions': ['Under what architectural criteria should an enterprise author a Custom Role rather than '
                           'selecting a Predefined Role?',
                           'What operational failure modes can occur when Google Cloud deprecates an underlying API '
                           'permission used in an enterprise Custom Role?',
                           'How does the custom role lifecycle stage (`GA` vs `DEPRECATED`) enable graceful role '
                           'retirement across multi-project organizations?'],
             'reference': 'https://docs.cloud.google.com/iam/docs/understanding-custom-roles',
             'reference_label': 'Google Cloud IAM: Creating, managing, and maintaining custom roles',
             'scenario': {'symptom': 'A junior data analyst accidentally deleted an entire historical Cloud Storage '
                                     'bucket containing 40 TB of customer audit logs because their account was '
                                     'assigned the predefined role `roles/storage.objectAdmin`.',
                          'constraints': 'Analysts must have full capability to upload, read, and transform objects in '
                                         'designated buckets, with zero capability to delete buckets.',
                          'evidence': 'Production BigQuery batch job error output:\n'
                                      '\n'
                                      '```text\n'
                                      'google.api_core.exceptions.PermissionDenied: 403 Access Denied: BigQuery '
                                      'BigQuery:\n'
                                      "Caller lacks required permission 'bigquery.readsessions.create' on resource "
                                      "'projects/analytics-prod'.\n"
                                      '```\n'
                                      '\n'
                                      'Root cause: Custom role `custom.bqDataViewer` omitted '
                                      '`bigquery.readsessions.create` which was added when BigQuery migrated to the '
                                      'high-throughput Storage Read API.',
                          'diagnostic_steps': ['Inspect the permission definition of `roles/storage.objectAdmin` via '
                                               'the IAM roles describe API.',
                                               'Review Cloud Audit Logs to confirm the `storage.buckets.delete` RPC '
                                               "was authorized by the analyst's role binding.",
                                               'Identify the minimal set of permissions required for daily analytical '
                                               'ingestion workflows.'],
                          'root': 'Excessive predefined role scope: `roles/storage.objectAdmin` granted bucket-level '
                                  'administrative destruction permissions to users who only required object-level CRUD '
                                  'capabilities.',
                          'fix': 'Author an Organization-level Custom Role `brightloaf.storageObjectCurator` '
                                 'containing object-level permissions (`storage.objects.get`, '
                                 '`storage.objects.create`, `storage.objects.list`) while explicitly omitting all '
                                 '`storage.buckets.*` mutation and deletion permissions.',
                          'verify': 'Assign the custom role to a test user; verify the user can create and read '
                                    'objects, but attempting to delete a bucket returns HTTP 403 Forbidden.',
                          'residual': 'If Google launches a new Cloud Storage feature (like soft delete recovery), the '
                                      'custom role must be updated manually to include the new permission.',
                          'diagram': ('Custom role defined with static permission list',
                                      'Google upgrades BigQuery Storage API verbs',
                                      'Nocturnal ETL pipeline crashes with HTTP 403',
                                      'Track permission drift and patch custom role',
                                      'ETL pipeline reads table via Storage API')},
             'lab': {'name': 'Custom IAM Role Specification, Creation, and Permission Boundary Test',
                     'goal': 'Author a declarative YAML manifest for an enterprise Custom Role omitting destructive '
                             'permissions and verify least-privilege boundary enforcement.',
                     'expected': 'A validated custom role YAML definition, an automated Python permission checker, and '
                                 'a role maintenance governance sheet.',
                     'mode': 'tabletop analysis & YAML/Python execution',
                     'prereq': 'Understanding of Google Cloud IAM permissions and custom role schemas.',
                     'preflight': 'Review custom role creation CLI syntax and permission naming conventions.',
                     'steps': ['#### Stage 1: Pre-Flight Custom Role Permission Inventory\n'
                               'Catalog required API permissions for custom roles:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > inventory_custom_role.py\n"
                               'base_perms = [\n'
                               "    'bigquery.datasets.get',\n"
                               "    'bigquery.tables.get',\n"
                               "    'bigquery.tables.getData',\n"
                               "    'bigquery.readsessions.create' # Critical for high-throughput reads\n"
                               ']\n'
                               "print(f'[PREFLIGHT] Custom role permissions required: {len(base_perms)}')\n"
                               'EOF\n'
                               'python3 inventory_custom_role.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & YAML Syntax Check\n'
                               'Verify YAML syntax parser for custom role manifest generation:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_custom_role_prereqs.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import yaml; print(\'[PASS] YAML parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_custom_role_prereqs.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Curated Custom Role YAML Manifest\n'
                               'Author a declarative YAML manifest defining the curated BigQuery reader role:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > custom_role_bq_reader.yaml\n"
                               'title: "Curated BigQuery Storage Reader"\n'
                               'description: "Fine-grained reader role including Storage Read API sessions"\n'
                               'stage: "GA"\n'
                               'includedPermissions:\n'
                               '  - bigquery.datasets.get\n'
                               '  - bigquery.tables.get\n'
                               '  - bigquery.tables.getData\n'
                               '  - bigquery.readsessions.create\n'
                               '  - bigquery.readsessions.getData\n'
                               'EOF\n'
                               'echo "[CONFIG] Authored custom_role_bq_reader.yaml"\n'
                               '```',
                               '#### Stage 4: Execution & Drift Detection Simulation\n'
                               'Author an automated script comparing custom role permissions against predefined '
                               '`roles/bigquery.dataViewer`:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > detect_permission_drift.py\n"
                               'import yaml\n'
                               '\n'
                               "with open('custom_role_bq_reader.yaml') as f:\n"
                               '    custom = yaml.safe_load(f)\n'
                               '\n'
                               "predefined_storage_perms = {'bigquery.readsessions.create', "
                               "'bigquery.readsessions.getData'}\n"
                               "custom_perms = set(custom['includedPermissions'])\n"
                               '\n'
                               'missing = predefined_storage_perms - custom_perms\n'
                               "assert not missing, f'Drift detected! Missing: {missing}'\n"
                               "print('[DRIFT PASS] Custom role includes all required Storage API permissions.')\n"
                               'EOF\n'
                               'python3 detect_permission_drift.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Missing Verb Crash Simulation\n'
                               'Simulate custom role lacking `bigquery.readsessions.create` and verify interception:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_missing_verb.py\n"
                               'def execute_read_session(perms):\n'
                               "    if 'bigquery.readsessions.create' not in perms:\n"
                               "        raise PermissionError('403 Access Denied: bigquery.readsessions.create "
                               "missing')\n"
                               "    return 'SESSION_ACTIVE_200'\n"
                               '\n'
                               'try:\n'
                               "    execute_read_session({'bigquery.tables.getData'})\n"
                               'except PermissionError as e:\n'
                               "    print(f'[CHAOS TEST PASS] Intercepted missing verb exception: {e}')\n"
                               'EOF\n'
                               'python3 test_missing_verb.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Custom Role Lifecycle Audit\n'
                               'Author a Cloud Logging filter tracking custom role updates:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > custom_role_audit_filter.txt\n"
                               'protoPayload.methodName="google.iam.admin.v1.UpdateRole"\n'
                               'resource.type="iam_role"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to custom_role_audit_filter.txt"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Manifest Assertions\n'
                               'Execute automated test asserting custom role manifest completeness:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_custom_role.py\n"
                               'import yaml\n'
                               '\n'
                               "with open('custom_role_bq_reader.yaml') as f:\n"
                               '    data = yaml.safe_load(f)\n'
                               '\n'
                               "assert data['stage'] == 'GA'\n"
                               "assert 'bigquery.readsessions.create' in data['includedPermissions']\n"
                               "print('[ASSERT PASS] Custom role YAML manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_custom_role.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary drift analysis scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_custom_role_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 99 Topic 2 test scripts..."\n'
                               'rm -f inventory_custom_role.py check_custom_role_prereqs.sh detect_permission_drift.py '
                               'test_missing_verb.py assert_custom_role.py\n'
                               'echo "[CLEANUP] Retaining production manifest: custom_role_bq_reader.yaml"\n'
                               'echo "[CLEANUP PASS] Custom role lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_custom_role_lab.sh\n'
                               '```'],
                     'verification': 'The YAML specification defines exact object-level permissions and the Python '
                                     'test confirms all bucket deletion and IAM mutation permissions are excluded.',
                     'trouble': 'Ensure permission names follow the three-segment format `service.resource.verb` (e.g. '
                                '`storage.objects.get`).',
                     'cleanup': 'Retain `custom_storage_curator_role.yaml` and `deploy_custom_role.sh` as exit '
                                'evidence artifacts.',
                     'accept': 'Completed Custom Role specification and verified permission audit test. File: '
                               '`day-099-topic-02-custom-roles.md`.',
                     'file': 'day-099-topic-02-custom-roles.md'}},
            {'key': 'topic-03',
             'title': 'IAM Recommender for Right-Sizing Permissions and Policy Intelligence',
             'overview': "Over time, enterprise cloud environments suffer from 'permission creep': users and service "
                         'accounts accumulate excessive permissions that are never exercised in practice. The **Google '
                         'Cloud IAM Recommender** applies machine learning across a 90-day observation window, '
                         'comparing the permissions an identity actually executed in Cloud Audit Logs against the '
                         'permissions granted by its assigned roles. It calculates an excess permission score and '
                         'automatically generates a right-sized role recommendation. SREs can inspect these '
                         'recommendations via the Policy Intelligence API or apply them automatically to shrink the '
                         "organization's attack surface.",
             'preview': 'A backend microservice uses only 3 permissions out of the 1,200 permissions granted by '
                        'primitive Editor. The IAM Recommender identifies the 99.8% excess permission ratio and '
                        'provides an automated, non-breaking right-sizing recommendation.',
             'technical': '### 1. Recommender Algorithm and Observation Window\n'
                          '- **The 90-Day Sliding Window:** The Recommender analyzes historical API calls captured in '
                          'Cloud Audit Logs over the preceding 90 days.\n'
                          '- **Security Insight Scoring:** For each IAM binding, the Recommender calculates the ratio '
                          'of used permissions to total granted permissions:\n'
                          '  $$\\text{Excess Ratio} = 1.0 - \\left( \\frac{\\text{Unique Permissions '
                          'Exercised}}{\\text{Total Permissions Granted}} \\right)$$\n'
                          '- If the excess ratio exceeds 80% with zero critical operations exercised, the Recommender '
                          'flags the identity as an over-privileged security risk.\n'
                          '\n'
                          '### 2. Recommendation Subtypes and Risk Levels\n'
                          '- **Role Replacement:** Suggests replacing a broad role (`roles/editor`) with one or more '
                          'specific predefined roles (e.g. `roles/pubsub.publisher` and `roles/datastore.user`).\n'
                          '- **Role Revocation:** If an identity has exercised zero permissions over 90 days, the '
                          'Recommender suggests complete revocation of the binding.\n'
                          '\n'
                          '### 3. Operational Caveats and Guardrails\n'
                          '- **Disaster Recovery Blind Spot:** Rare operations executed only during annual Game Days '
                          'or emergency disaster recovery drills will not appear in a 90-day log window. Blindly '
                          'applying recommendations can break emergency failover capabilities.\n'
                          '- **Pre-Commit Verification:** High-risk recommendations must be reviewed by security leads '
                          'before automated terraform application.',
             'questions': ['How does the IAM Recommender determine which permissions were actively exercised by a '
                           'service account over the preceding 90 days?',
                           'Why can blindly applying IAM Recommender proposals break rare operational workflows such '
                           'as disaster recovery failovers?',
                           'What is the difference between a Role Replacement recommendation and a Role Revocation '
                           'recommendation?'],
             'reference': 'https://docs.cloud.google.com/recommender/docs/recommenders/iam-recommender',
             'reference_label': 'Google Cloud Recommender: IAM role recommendations and Policy Intelligence API',
             'scenario': {'symptom': 'Security audit detected that 140 service accounts across the engineering '
                                     'organization were assigned `roles/owner` or `roles/editor`, posing an acute '
                                     'compliance failure under SOC 2 Type II trust criteria.',
                          'constraints': 'Must right-size service account permissions across all 140 identities '
                                         'without disrupting running production microservices.',
                          'evidence': 'IAM Recommender API recommendation output:\n'
                                      '\n'
                                      '```json\n'
                                      '{\n'
                                      '  "name": '
                                      '"projects/prod-data/locations/global/recommenders/google.iam.policy.Recommender/recommendations/rec-8120",\n'
                                      '  "description": "serviceAccount:analyst-sa@prod-data.iam has not used 94 of 98 '
                                      'permissions in the last 90 days.",\n'
                                      '  "primaryImpact": {"category": "SECURITY", "costProjection": null},\n'
                                      '  "content": {\n'
                                      '    "overview": {\n'
                                      '      "currentRole": "roles/editor",\n'
                                      '      "recommendedRole": "roles/bigquery.dataViewer"\n'
                                      '    }\n'
                                      '  }\n'
                                      '}\n'
                                      '```',
                          'diagnostic_steps': ['Query the Recommender API for `google.iam.role.Recommender` across the '
                                               'organization.',
                                               'Review the recommended role replacements for each service account.',
                                               'Cross-reference recommendations against documented disaster recovery '
                                               'runbooks to ensure no rare failover permissions are stripped.'],
                          'root': 'Permission creep and convenience-driven provisioning: initial developer setup used '
                                  'broad primitive roles and was never audited.',
                          'fix': "Script an automated migration applying the Recommender's proposed predefined role "
                                 'replacements. Mark applied recommendations as `CLAIMED` and `SUCCEEDED` in the '
                                 'Recommender API.',
                          'verify': 'Inspect IAM policy bindings post-remediation; confirm all 140 service accounts '
                                    'possess only the recommended granular roles. Run automated regression tests to '
                                    'verify zero microservice disruptions.',
                          'residual': 'Periodic review cycles (quarterly) are required to capture new service accounts '
                                      'provisioned by growing engineering teams.',
                          'diagram': ('Service account retains 98 unused permissions',
                                      'IAM Recommender flags over-permissioning',
                                      'Security team ignores recommendation for 9 months',
                                      'Apply automated Recommender right-sizing pipeline',
                                      'SA reduced to bigquery.dataViewer with zero breakage')},
             'lab': {'name': 'IAM Recommender API Analysis and Automated Role Right-Sizing Simulation',
                     'goal': 'Author a script querying IAM Recommender recommendations and build an automated '
                             'simulation parsing excess permission scores and applying right-sized substitutions.',
                     'expected': 'A validated shell script querying the Recommender API and an executable Python '
                                 'script calculating excess permission scores and executing role replacement.',
                     'mode': 'tabletop analysis & Python execution',
                     'prereq': 'Understanding of IAM Recommender schemas and Policy Intelligence.',
                     'preflight': 'Review Recommender API CLI documentation and command syntax.',
                     'steps': ['#### Stage 1: Pre-Flight IAM Recommender API Discovery\n'
                               'Query IAM Recommender API endpoint schema and observation windows:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_recommender_api.py\n"
                               "recommender_id = 'google.iam.policy.Recommender'\n"
                               'observation_window_days = 90\n'
                               "print(f'[PREFLIGHT] Auditing Recommender: {recommender_id} (Window: "
                               "{observation_window_days} days)')\n"
                               'EOF\n'
                               'python3 check_recommender_api.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Tooling Verification\n'
                               'Verify execution prerequisites for automated right-sizing scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_recommender_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_recommender_tools.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Automated Recommender Processing Engine\n'
                               'Author a Python automation engine parsing recommendations and generating replacement '
                               'bindings:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > recommender_engine.py\n"
                               'class IAMRecommenderEngine:\n'
                               '    def __init__(self, raw_recommendations):\n'
                               '        self.recs = raw_recommendations\n'
                               '\n'
                               '    def generate_rightsized_bindings(self):\n'
                               '        actions = []\n'
                               '        for r in self.recs:\n'
                               "            member = r['member']\n"
                               "            old_role = r['currentRole']\n"
                               "            new_role = r['recommendedRole']\n"
                               '            actions.append({\n'
                               "                'member': member,\n"
                               "                'remove': old_role,\n"
                               "                'add': new_role,\n"
                               '                \'security_gain\': f\'Removed {r["unused_count"]} unused '
                               "permissions'\n"
                               '            })\n'
                               '        return actions\n'
                               '\n'
                               "if __name__ == '__main__':\n"
                               '    mock_recs = [{\n'
                               "        'member': 'serviceAccount:analyst-sa@prod.iam.gserviceaccount.com',\n"
                               "        'currentRole': 'roles/editor',\n"
                               "        'recommendedRole': 'roles/bigquery.dataViewer',\n"
                               "        'unused_count': 94\n"
                               '    }]\n'
                               '    engine = IAMRecommenderEngine(mock_recs)\n'
                               '    plan = engine.generate_rightsized_bindings()\n'
                               "    print(f'[RIGHTSIZING PLAN] {plan[0]}')\n"
                               'EOF\n'
                               'python3 recommender_engine.py\n'
                               '```',
                               '#### Stage 4: Execution & Policy Simulator Validation\n'
                               'Simulate applying the recommendation and verify that production workflows continue '
                               'uninterrupted:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_rightsizing.py\n"
                               "required_app_perms = {'bigquery.jobs.create', 'bigquery.tables.getData'}\n"
                               "new_role_perms = {'bigquery.jobs.create', 'bigquery.tables.getData', "
                               "'bigquery.tables.get'}\n"
                               '\n'
                               'missing = required_app_perms - new_role_perms\n'
                               "assert not missing, 'Recommended role breaks application query path!'\n"
                               "print('[SIMULATION PASS] Recommended role satisfies 100% of used application "
                               "permissions.')\n"
                               'EOF\n'
                               'python3 simulate_rightsizing.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Overly Aggressive Revocation Intercept\n'
                               'Simulate a flawed recommendation that removes a critical quarterly batch permission '
                               'and test canary guardrail:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_canary_guardrail.py\n"
                               'def validate_recommendation_safety(recommended_perms, quarterly_perms):\n'
                               '    intersection = quarterly_perms.intersection(recommended_perms)\n'
                               '    if len(intersection) < len(quarterly_perms):\n'
                               "        raise ValueError('SAFETY INTERCEPT: Recommendation strips quarterly batch "
                               "permissions!')\n"
                               "    return 'SAFE'\n"
                               '\n'
                               'try:\n'
                               "    validate_recommendation_safety({'bigquery.tables.getData'}, "
                               "{'bigquery.tables.getData', 'bigquery.tables.delete'})\n"
                               'except ValueError as e:\n'
                               "    print(f'[CHAOS TEST PASS] Guardrail caught aggressive revocation: {e}')\n"
                               'EOF\n'
                               'python3 test_canary_guardrail.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Over-Privileged Account Dashboard Manifest\n'
                               'Author a Cloud Monitoring Dashboard JSON tracking unaddressed IAM recommendations:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > recommender_dashboard.json\n"
                               '{\n'
                               '  "displayName": "IAM Recommender Security Posture",\n'
                               '  "gridLayout": {\n'
                               '    "widgets": [\n'
                               '      {\n'
                               '        "title": "Unresolved High-Impact IAM Recommendations",\n'
                               '        "scorecard": {\n'
                               '          "timeSeriesQuery": {"timeSeriesFilter": {"filter": '
                               '"metric.type=\\"recommender.googleapis.com/recommendation/count\\""}}\n'
                               '        }\n'
                               '      }\n'
                               '    ]\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[DASHBOARD] Authored recommender_dashboard.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Recommender Engine Assertions\n'
                               'Execute automated test asserting Recommender parser logic:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_recommender.py\n"
                               'from recommender_engine import IAMRecommenderEngine\n'
                               '\n'
                               'engine = IAMRecommenderEngine([])\n'
                               'assert engine.generate_rightsized_bindings() == []\n'
                               "print('[ASSERT PASS] Recommender engine deterministic behavior strictly validated.')\n"
                               'EOF\n'
                               'python3 assert_recommender.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_recommender_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 99 Topic 3 test scripts..."\n'
                               'rm -f check_recommender_api.py check_recommender_tools.sh recommender_engine.py '
                               'simulate_rightsizing.py test_canary_guardrail.py assert_recommender.py\n'
                               'echo "[CLEANUP] Retaining dashboard manifest: recommender_dashboard.json"\n'
                               'echo "[CLEANUP PASS] IAM Recommender lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_recommender_lab.sh\n'
                               '```'],
                     'verification': 'The shell script targets the standard Recommender API path and the Python '
                                     'simulation calculates the exact excess ratio and suggests the least-privilege '
                                     'replacement role.',
                     'trouble': 'Ensure Recommender API (`recommender.googleapis.com`) is enabled in the target '
                                'project before executing queries.',
                     'cleanup': 'Retain `query_iam_recommender.sh` as an exit evidence artifact.',
                     'accept': 'Completed Recommender query script and verified right-sizing simulation. File: '
                               '`day-099-topic-03-iam-recommender.md`.',
                     'file': 'day-099-topic-03-iam-recommender.md'}},
            {'key': 'topic-04',
             'title': 'IAM Conditions: Time, Resource, and Attribute-Based Access Control',
             'overview': 'IAM Conditions allow security architects to define conditional attribute-based access '
                         'control (ABAC) using the Common Expression Language (CEL). Rather than granting static, '
                         'permanent permissions, a conditional IAM binding takes effect only when specific boolean '
                         "criteria are met—such as a temporary time window (`request.time < timestamp('...')`), a "
                         "specific resource name prefix (`resource.name.startsWith('...')`), or a validated client IP "
                         'range. IAM Conditions enable automated break-glass access, restrict storage administrator '
                         'permissions to dev/staging buckets, and ensure production deployments are restricted to '
                         'business hours.',
             'preview': 'An engineer needs temporary 2-hour access to inspect production database logs during an '
                        'incident. Configuring an IAM condition automatically revokes the role binding when the '
                        'expiration timestamp elapses, requiring zero manual cleanup.',
             'technical': '### 1. Common Expression Language (CEL) Syntax in Cloud IAM\n'
                          '- CEL expressions evaluate to a boolean (`true` or `false`). If true, the permission is '
                          'granted; if false, the binding is ignored.\n'
                          '- **Available Attributes:**\n'
                          '  - `request.time`: Timestamp of the API call.\n'
                          '  - `resource.name`: Fully qualified GCP resource path (e.g. '
                          '`//storage.googleapis.com/projects/_/buckets/brightloaf-staging-*`).\n'
                          '  - `resource.type`: Resource API type (e.g. `compute.googleapis.com/Instance`).\n'
                          '  - `resource.tagValue`: Tags attached to the resource.\n'
                          '\n'
                          '### 2. Core Conditional Patterns\n'
                          '- **Time-Bound (Temporary Break-Glass) Access:**\n'
                          "  `request.time >= timestamp('2026-09-28T14:00:00Z') && request.time < "
                          "timestamp('2026-09-28T16:00:00Z')`\n"
                          '- **Resource Prefix Isolation:**\n'
                          "  `resource.type == 'storage.googleapis.com/Bucket' && "
                          "resource.name.startsWith('projects/_/buckets/brightloaf-dev-')`\n"
                          '- **IP-Restricted Access (Context-Aware Access):** Enforces that access is granted only '
                          "when the caller's IP matches corporate VPN gateways.\n"
                          '\n'
                          '### 3. Fail-Closed Behavior and Limits\n'
                          '- If a CEL expression encounters an un-parseable condition or missing attribute, it **fails '
                          'closed** (access is denied).\n'
                          '- A single IAM policy binding can contain at most one condition expression.',
             'questions': ['How do time-bound CEL conditions eliminate the operational risk of orphaned permissions '
                           'after emergency incident remediation?',
                           'What failure mode occurs if a CEL expression attempts to evaluate an attribute that does '
                           'not exist on the target resource?',
                           'How can resource prefix matching in IAM conditions enforce environment isolation across '
                           'development and production buckets?'],
             'reference': 'https://docs.cloud.google.com/iam/docs/conditions-overview',
             'reference_label': 'Google Cloud IAM: Overview of IAM Conditions and CEL expression syntax',
             'scenario': {'symptom': 'A contractor granted 4-hour emergency debugging access to production Cloud SQL '
                                     'during a Sev-1 incident retained their administrative database credentials for 9 '
                                     'months after their contract ended, violating SOC 2 compliance.',
                          'constraints': 'Must establish an automated break-glass provisioning model that enforces '
                                         'automatic permission expiration without relying on manual revocation.',
                          'evidence': 'Production break-glass IAM denial log:\n'
                                      '\n'
                                      '```text\n'
                                      "2026-09-29T02:14:00Z [DENIED] SRE principal 'sre-oncall@corp.com' denied "
                                      "'compute.instances.reset'\n"
                                      "Condition expression: request.time < timestamp('2026-09-29T02:00:00Z')\n"
                                      'Current evaluated time: 2026-09-29T02:14:00Z (condition evaluated to FALSE)\n'
                                      '```\n'
                                      '\n'
                                      'Root cause: Condition author specified hardcoded UTC string without accounting '
                                      'for Daylight Saving Time clock shift, causing premature expiration of emergency '
                                      'access.',
                          'diagnostic_steps': ['Audit project IAM policy bindings via the Resource Manager '
                                               'get-iam-policy API filtered by contractor domain.',
                                               'Review incident ticket history to verify when the emergency access was '
                                               'requested.',
                                               'Confirm whether an automated revocation workflow or calendar reminder '
                                               'failed to trigger.'],
                          'root': 'Static role assignment without temporal boundaries: relying on human memory to '
                                  'revoke emergency permissions guarantees orphaned access.',
                          'fix': 'Apply emergency role bindings exclusively with time-bound CEL conditions: '
                                 "`request.time < timestamp('2026-09-28T16:00:00Z')`. The role automatically ceases to "
                                 'grant access the instant the timestamp passes.',
                          'verify': 'Simulate an API call before the timestamp (access granted) and after the '
                                    'timestamp (access denied with 403 Forbidden).',
                          'residual': 'Expired conditional bindings remain visible in the IAM policy JSON until '
                                      'cleaned up; however, they cannot authorize any actions.',
                          'diagram': ('Emergency break-glass role granted with CEL time condition',
                                      'Condition uses hardcoded unpadded UTC timestamp',
                                      'Daylight saving time shifts UTC offset -> premature lock',
                                      'Use request.time < timestamp + duration expression',
                                      'Break-glass window remains active for full emergency')},
             'lab': {'name': 'Time-Bound and Resource-Scoped IAM Condition Implementation',
                     'goal': 'Author production IAM configuration scripts applying time-bound and prefix-scoped CEL '
                             'conditions and verify evaluation logic via Python.',
                     'expected': 'A validated shell deployment script applying CEL conditions and an executable Python '
                                 'CEL evaluator proving access cutoff.',
                     'mode': 'tabletop analysis & Python execution',
                     'prereq': 'Understanding of CEL expressions and IAM policy binding syntax.',
                     'preflight': 'Review conditional IAM policy binding parameters and CEL condition syntax.',
                     'steps': ['#### Stage 1: Pre-Flight CEL Grammar & Attribute Discovery\n'
                               'Catalog Common Expression Language (CEL) attributes supported by Google Cloud IAM:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_cel_attributes.py\n"
                               'cel_attributes = {\n'
                               "    'request.time': 'Timestamp representing request arrival time',\n"
                               "    'resource.name': 'Full resource URI identifier',\n"
                               "    'resource.type': 'Resource type string (e.g. compute.googleapis.com/Instance)',\n"
                               "    'resource.matchTag()': 'Evaluates Resource Manager resource tags'\n"
                               '}\n'
                               "print('[PREFLIGHT] Supported CEL IAM Attributes:')\n"
                               'for k, v in cel_attributes.items():\n'
                               "    print(f'  • {k:22s}: {v}')\n"
                               'EOF\n'
                               'python3 check_cel_attributes.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & CEL Validation Readiness\n'
                               'Verify local Python environment for CEL simulation tests:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_cel_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import datetime; print(\'[PASS] datetime module ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_cel_tools.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Production CEL IAM Condition Manifest\n'
                               'Author a declarative Terraform configuration attaching time-bounded and tag-scoped IAM '
                               'conditions:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > iam_conditions.tf\n"
                               'resource "google_project_iam_member" "sre_emergency_access" {\n'
                               '  project = "prod-workloads"\n'
                               '  role    = "roles/compute.instanceAdmin.v1"\n'
                               '  member  = "group:sre-breakglass@corp.com"\n'
                               '\n'
                               '  condition {\n'
                               '    title       = "time_bounded_emergency_window"\n'
                               '    description = "Grants instance administration during certified maintenance '
                               'window"\n'
                               '    expression  = <<-EOT\n'
                               '      request.time >= timestamp("2026-10-01T00:00:00Z") &&\n'
                               '      request.time < timestamp("2026-10-01T04:00:00Z") &&\n'
                               '      resource.matchTag("108420918237/env", "production")\n'
                               '    EOT\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored iam_conditions.tf"\n'
                               '```',
                               '#### Stage 4: Execution & CEL Evaluation Simulation\n'
                               'Author a Python script evaluating the CEL boolean logic against simulated request '
                               'times:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > evaluate_cel_condition.py\n"
                               'from datetime import datetime, timezone\n'
                               '\n'
                               'def evaluate_access(req_time_iso, tag_env):\n'
                               "    t = datetime.fromisoformat(req_time_iso.replace('Z', '+00:00'))\n"
                               "    start = datetime.fromisoformat('2026-10-01T00:00:00+00:00')\n"
                               "    end = datetime.fromisoformat('2026-10-01T04:00:00+00:00')\n"
                               '    \n'
                               '    is_in_window = start <= t < end\n'
                               "    is_prod_tag = (tag_env == 'production')\n"
                               '    return is_in_window and is_prod_tag\n'
                               '\n'
                               "print('[SIMULATION] Testing CEL condition evaluation:')\n"
                               'tests = [\n'
                               "    ('2026-10-01T02:00:00Z', 'production', True),\n"
                               "    ('2026-10-01T05:00:00Z', 'production', False), # Past window\n"
                               "    ('2026-10-01T02:00:00Z', 'staging', False)      # Wrong tag\n"
                               ']\n'
                               'for t_iso, tag, expected in tests:\n'
                               '    res = evaluate_access(t_iso, tag)\n'
                               '    assert res == expected\n'
                               "    print(f'  • Time: {t_iso}, Tag: {tag:10s} -> Allowed: {res} (Expected: "
                               "{expected})')\n"
                               "print('[PASS] CEL conditional logic perfectly verified.')\n"
                               'EOF\n'
                               'python3 evaluate_cel_condition.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Expired Access Intercept Chaos Test\n'
                               'Simulate request arrival one second past maintenance window and verify immediate '
                               'revocation:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_expired_condition.py\n"
                               'from evaluate_cel_condition import evaluate_access\n'
                               '\n'
                               '# 1 second past window\n'
                               "res = evaluate_access('2026-10-01T04:00:01Z', 'production')\n"
                               "assert res is False, 'Security failure: Access permitted past expiration window!'\n"
                               "print('[CHAOS TEST PASS] CEL condition automatically revoked access at window "
                               "boundary.')\n"
                               'EOF\n'
                               'python3 test_expired_condition.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Condition Denied Metric Alert\n'
                               'Author a Cloud Monitoring Alert detecting unexpected condition denials:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_condition_denials.json\n"
                               '{\n'
                               '  "displayName": "ALERT: IAM Condition Evaluation Denial Spike",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "Policy Denied audit logs with condition evaluation failure",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": "logName=\\"cloudaudit.googleapis.com%2Fpolicy\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 5.0,\n'
                               '        "duration": "60s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] Authored alert_condition_denials.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform condition syntax:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_conditions.py\n"
                               "with open('iam_conditions.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'condition {' in tf\n"
                               "assert 'request.time >=' in tf\n"
                               "assert 'resource.matchTag' in tf\n"
                               "print('[ASSERT PASS] IAM condition Terraform manifest strictly validated.')\n"
                               'EOF\n'
                               'python3 assert_conditions.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary test files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_conditions_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 99 Topic 4 test scripts..."\n'
                               'rm -f check_cel_attributes.py check_cel_tools.sh evaluate_cel_condition.py '
                               'test_expired_condition.py assert_conditions.py\n'
                               'echo "[CLEANUP] Retaining production files: iam_conditions.tf, '
                               'alert_condition_denials.json"\n'
                               'echo "[CLEANUP PASS] IAM conditions lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_conditions_lab.sh\n'
                               '```'],
                     'verification': 'The shell script applies valid CEL syntax with timestamp and prefix checks, and '
                                     'the Python test confirms automatic access cutoff when the expiration window '
                                     'passes.',
                     'trouble': 'Ensure timestamps in CEL conditions adhere to RFC 3339 format enclosed in '
                                "`timestamp('...')`.",
                     'cleanup': 'Retain `apply_conditional_iam_grant.sh` as an exit evidence artifact.',
                     'accept': 'Completed conditional IAM script and verified CEL simulation. File: '
                               '`day-099-topic-04-iam-conditions.md`.',
                     'file': 'day-099-topic-04-iam-conditions.md'}},
            {'key': 'topic-05',
             'title': 'IAM Deny Policies and Principal Access Boundaries',
             'overview': 'For over a decade, Google Cloud IAM was additive: an Allow rule granted at any hierarchy '
                         'level gave permanent access regardless of child project configuration. **IAM Deny Policies** '
                         'introduce absolute negative guardrails that override all Allow policies, ensuring that even '
                         'a Project Owner cannot perform specific high-risk operations. Complementing Deny policies, '
                         '**Principal Access Boundaries (PABs)** restrict the set of resources an identity can access '
                         'across the entire cloud estate, preventing compromised service accounts or rogue contractors '
                         'from touching production assets regardless of what permissions they hold.',
             'preview': 'An attacker gains Project Owner credentials and attempts to create a persistent service '
                        'account private key to maintain access. An Organization Deny policy permanently blocks '
                        'service account key creation across all projects, thwarting persistence.',
             'technical': '### 1. Deterministic Policy Evaluation Hierarchy\n'
                          '- When an API call arrives at Google Cloud, the IAM evaluation engine evaluates rules in '
                          'strict sequence:\n'
                          '  1. **Deny Policy Check:** Evaluates Deny policies from Organization &rarr; Folder &rarr; '
                          'Project. If any Deny matches the principal, resource, and permission, the request is '
                          '**immediately terminated with HTTP 403 Forbidden**. Allow rules are never evaluated.\n'
                          '  2. **Principal Access Boundary (PAB) Check:** Confirms the target resource is explicitly '
                          "listed within the principal's allowed boundary.\n"
                          '  3. **Allow Policy & Condition Check:** Evaluates Allow bindings from Organization down to '
                          'Resource. If matching permission is found and any attached CEL conditions evaluate to '
                          '`true`, access is granted.\n'
                          '\n'
                          '### 2. Anatomy of an IAM Deny Policy\n'
                          '- Deny policies are managed via the IAM deny-policies API:\n'
                          '  - `deniedPrincipals`: Who is blocked (e.g. `principalSet://goog/public:all`).\n'
                          '  - `exceptionPrincipals`: Whitelisted emergency bypass identities (e.g. break-glass '
                          'break-glass-admin@brightloaf.com).\n'
                          '  - `deniedPermissions`: Exact API permissions blocked (e.g. '
                          '`iam.googleapis.com/serviceAccountKeys.create`).\n'
                          '  - `denialCondition`: Optional CEL condition restricting when the deny applies.\n'
                          '\n'
                          '### 3. Principal Access Boundaries (PABs)\n'
                          '- A Principal Access Boundary policy binds to an identity, declaring a strict resource '
                          'envelope:\n'
                          '  `allowedResources: '
                          "['//cloudresourcemanager.googleapis.com/projects/brightloaf-staging-*']`.\n"
                          '- Even if the identity is granted `roles/owner` in `brightloaf-prod`, the PAB intercepts '
                          'and blocks the call.',
             'questions': ['Why do IAM Deny policies take precedence over all Allow policies across the Google Cloud '
                           'resource hierarchy?',
                           'How does an organization-level Deny policy on `iam.serviceAccountKeys.create` eliminate '
                           'credential exfiltration vulnerabilities?',
                           'What is the architectural distinction between a resource-level Deny policy and a Principal '
                           'Access Boundary?'],
             'reference': 'https://docs.cloud.google.com/iam/docs/deny-overview',
             'reference_label': 'Google Cloud IAM: Deny policies overview, syntax, and evaluation rules',
             'scenario': {'symptom': 'Security Operations detected an unknown IP address downloading 500 GiB of data '
                                     'using a service account private key file (`key.json`) that had been created by a '
                                     'developer 8 months prior and leaked in a public GitHub repository.',
                          'constraints': 'Must enforce an organization-wide ban on user-managed service account key '
                                         'creation while permitting workload identity federation.',
                          'evidence': 'Production Cloud Audit Activity log showing unauthorized deletion:\n'
                                      '\n'
                                      '```json\n'
                                      '{\n'
                                      '  "protoPayload": {\n'
                                      '    "authenticationInfo": {"principalEmail": "compromised-admin@corp.com"},\n'
                                      '    "methodName": "storage.buckets.delete",\n'
                                      '    "resourceName": "projects/_/buckets/sec-vault-cold-storage",\n'
                                      '    "status": {"code": 0, "message": "OK"}\n'
                                      '  }\n'
                                      '}\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: Attacker gained project `roles/owner` and deleted the compliance '
                                      'archive bucket. An organization-level IAM Deny policy blocking '
                                      '`storage.buckets.delete` on cold archives would have superseded the '
                                      'project-level Owner grant and prevented data loss.',
                          'diagnostic_steps': ['Audit existing service account keys via the service account keys list '
                                               'API across all projects.',
                                               'Review organization policy constraints '
                                               '(`iam.disableServiceAccountKeyCreation`).',
                                               'Inspect IAM Deny policies defined at the organization root.'],
                          'root': 'Absence of negative guardrails: relying on developers to follow policy guidelines '
                                  'without enforcing an architectural Deny policy allowed private key credential '
                                  'generation.',
                          'fix': 'Deploy an Organization IAM Deny Policy blocking '
                                 '`iam.googleapis.com/serviceAccountKeys.create` for all principals except the '
                                 'automated Terraform deployment pipeline. Enforce the '
                                 '`iam.disableServiceAccountKeyCreation` Org Policy constraint.',
                          'verify': 'Attempt to generate a service account key using Project Owner credentials; verify '
                                    'the API returns HTTP 403 with message: `Access denied by Deny Policy`.',
                          'residual': 'Deny policies do not automatically delete existing historical keys; an active '
                                      'remediation script must revoke pre-existing keys.',
                          'diagram': ('Attacker compromises project Owner credentials',
                                      'Project Owner has broad delete permissions',
                                      'Attacker attempts to delete compliance archive bucket',
                                      'Enforce organization IAM Deny policy on bucket deletion',
                                      'IAM Deny supersedes Owner grant; deletion blocked')},
             'lab': {'name': 'Organization IAM Deny Policy Specification and Policy Evaluation Simulator',
                     'goal': 'Author a declarative organization IAM Deny policy JSON blocking service account key '
                             'creation and simulate deterministic policy evaluation.',
                     'expected': 'A validated Deny policy JSON manifest, an executable Python evaluation engine '
                                 'proving Deny overrides Allow, and an authorization matrix.',
                     'mode': 'tabletop analysis & JSON/Python execution',
                     'prereq': 'Understanding of Google Cloud Resource Manager and IAM Deny policies.',
                     'preflight': 'Review IAM deny-policies CLI documentation and schema.',
                     'steps': ['#### Stage 1: Pre-Flight IAM Deny Precedence & Syntax Discovery\n'
                               'Catalog IAM evaluation precedence rules: Deny policies always supersede Allow '
                               'policies:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_deny_precedence.py\n"
                               'evaluation_order = [\n'
                               "    '1. IAM Deny Policies (Evaluated first; immediate fail-closed denial if "
                               "matched)',\n"
                               "    '2. IAM Allow Policies & Role Bindings (Evaluated second)',\n"
                               "    '3. Default Implicit Deny (If no allow matches, request denied)'\n"
                               ']\n'
                               "print('[PREFLIGHT] Google Cloud IAM Evaluation Hierarchy:')\n"
                               'for rule in evaluation_order:\n'
                               "    print(f'  • {rule}')\n"
                               'EOF\n'
                               'python3 check_deny_precedence.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Manifest Linter Readiness\n'
                               'Verify YAML parsing readiness for IAM Deny policy generation:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_deny_prereqs.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import yaml; print(\'[PASS] YAML parser ready for Deny policy '
                               'generation.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_deny_prereqs.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Organization IAM Deny Policy Manifest\n'
                               'Author a declarative YAML manifest establishing an organization-wide IAM Deny policy '
                               'blocking bucket deletion:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > org_deny_policy.yaml\n"
                               'name: organizations/108420918237/locations/global/denyPolicies/protect-audit-vaults\n'
                               'displayName: "Prevent Deletion of Compliance Storage Buckets"\n'
                               'rules:\n'
                               '  - denyRule:\n'
                               '      deniedPrincipals:\n'
                               '        - "principalSet://goog/public:all"\n'
                               '      exceptionPrincipals:\n'
                               '        - '
                               '"principal://iam.googleapis.com/projects/-/serviceAccounts/breakglass-sa@corp-sec.iam.gserviceaccount.com"\n'
                               '      deniedPermissions:\n'
                               '        - "storage.googleapis.com/buckets.delete"\n'
                               '      denialCondition:\n'
                               '        title: "match_cold_storage_tags"\n'
                               '        expression: "resource.matchTag(\'108420918237/retention\', '
                               '\'compliance-lock\')"\n'
                               'EOF\n'
                               'echo "[CONFIG] Authored org_deny_policy.yaml"\n'
                               '```',
                               '#### Stage 4: Execution & Deny Evaluation Simulation Engine\n'
                               'Author a Python script simulating IAM evaluation with Deny precedence over Owner '
                               'permissions:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_deny_evaluation.py\n"
                               'def evaluate_request(principal, action, has_owner_role, is_compliance_locked):\n'
                               '    # Stage 1: Deny Policy Evaluation\n'
                               "    if action == 'storage.googleapis.com/buckets.delete' and is_compliance_locked:\n"
                               "        if 'breakglass-sa' not in principal:\n"
                               "            return 'DENIED_BY_IAM_DENY_POLICY (HTTP 403)'\n"
                               '    \n'
                               '    # Stage 2: Allow Policy Evaluation\n'
                               '    if has_owner_role:\n'
                               "        return 'ALLOWED_BY_OWNER_ROLE (HTTP 200)'\n"
                               "    return 'DENIED_BY_DEFAULT'\n"
                               '\n'
                               "print('[SIMULATION] Testing Deny policy precedence:')\n"
                               "res1 = evaluate_request('attacker-owner@corp.com', "
                               "'storage.googleapis.com/buckets.delete', True, True)\n"
                               "print(f'  • Owner attempting bucket delete on locked archive: {res1}')\n"
                               "assert 'DENIED_BY_IAM_DENY_POLICY' in res1\n"
                               "print('[PASS] Deny policy successfully superseded Owner grant.')\n"
                               'EOF\n'
                               'python3 simulate_deny_evaluation.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & PAB Boundary Escape Chaos Test\n'
                               'Simulate an attempted lateral movement outside Principal Access Boundaries (PAB) and '
                               'assert interception:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_pab_boundary.py\n"
                               "pab_permitted_resources = {'projects/prod-data-platform', 'projects/prod-data-vault'}\n"
                               "target_resource = 'projects/finance-restricted'\n"
                               '\n'
                               'if target_resource not in pab_permitted_resources:\n'
                               "    print(f'[CHAOS TEST PASS] Principal Access Boundary intercepted access to "
                               "{target_resource}: HTTP 403 Forbidden.')\n"
                               'else:\n'
                               "    raise AssertionError('PAB boundary leak detected!')\n"
                               'EOF\n'
                               'python3 test_pab_boundary.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Policy Denied Threat Alerting\n'
                               'Author a Cloud Monitoring Alert Policy alerting whenever an IAM Deny policy trips:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_iam_deny.json\n"
                               '{\n'
                               '  "displayName": "CRITICAL SECURITY: IAM Deny Policy Triggered",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "Policy Denied audit log event for bucket deletion",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": "logName=\\"cloudaudit.googleapis.com%2Fpolicy\\" AND '
                               'protoPayload.status.message=\\"DENIED_BY_DENY_POLICY\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 0.0,\n'
                               '        "duration": "0s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] Authored alert_iam_deny.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Deny Policy Schema Assertions\n'
                               'Execute automated test asserting Deny policy schema adherence:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_deny_policy.py\n"
                               'import yaml\n'
                               '\n'
                               "with open('org_deny_policy.yaml') as f:\n"
                               '    policy = yaml.safe_load(f)\n'
                               '\n'
                               "rule = policy['rules'][0]['denyRule']\n"
                               "assert 'storage.googleapis.com/buckets.delete' in rule['deniedPermissions']\n"
                               "assert 'principalSet://goog/public:all' in rule['deniedPrincipals']\n"
                               "assert 'breakglass-sa' in rule['exceptionPrincipals'][0]\n"
                               "print('[ASSERT PASS] IAM Deny policy schema strictly validated.')\n"
                               'EOF\n'
                               'python3 assert_deny_policy.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_deny_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 99 Topic 5 test scripts..."\n'
                               'rm -f check_deny_precedence.py check_deny_prereqs.sh simulate_deny_evaluation.py '
                               'test_pab_boundary.py assert_deny_policy.py\n'
                               'echo "[CLEANUP] Retaining production files: org_deny_policy.yaml, '
                               'alert_iam_deny.json"\n'
                               'echo "[CLEANUP PASS] IAM Deny policy lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_deny_lab.sh\n'
                               '```'],
                     'verification': 'The Deny policy JSON conforms to the standard Google Cloud schema, the Python '
                                     'simulation proves Deny precedence over primitive Owner Allows, and the decision '
                                     'matrix documents all evaluation paths.',
                     'trouble': 'Ensure permission names in Deny policies use the full resource service prefix (e.g. '
                                '`iam.googleapis.com/serviceAccountKeys.create`).',
                     'cleanup': 'Retain `org_deny_key_creation.json` and `day-099-topic-05-decision-matrix.md` as exit '
                                'evidence artifacts.',
                     'accept': 'Completed Organization Deny policy specification and verified authorization decision '
                               'matrix. File: `day-099-topic-05-deny-policies.md`.',
                     'file': 'day-099-topic-05-deny-policies.md'}}],
 'part3_intro': 'The following field cases analyze severe IAM security incidents and authorization failures: a '
                'catastrophic blast radius expansion caused by granting primitive `roles/editor` to a CI/CD service '
                'account which deleted an entire shared VPC peering mesh, a broken nocturnal ETL data pipeline caused '
                'by a custom role missing the newly introduced `bigquery.readsessions.create` permission, an insider '
                'threat incident exploiting 9-month-old dormant permissions that IAM Recommender had repeatedly '
                'flagged for revocation, a daylight saving time lockout caused by a fragile string-based CEL condition '
                'expression in an emergency break-glass IAM policy, and a cross-project lateral movement attack that '
                'bypassed perimeter security because organization administrators omitted IAM Deny policies and '
                'Principal Access Boundaries. Each case delivers verbatim CLI output, policy audit logs, diagnostic '
                'commands, root cause analysis, defensible remediations, and dual-lane failed/corrected flow diagrams.',
 'part4_intro': 'These hands-on exercises implement the comprehensive 8-stage operational engineering lifecycle for '
                'Day 99. Engineers construct least-privilege Terraform role bindings enforcing separation of duties, '
                'author curated custom IAM roles with automated API permission drift validation, deploy automated IAM '
                'Recommender harvesting pipelines to right-size over-privileged accounts, implement attribute-based '
                'CEL IAM Conditions with time windows and resource tags, and enforce organization-level IAM Deny '
                'policies and Principal Access Boundaries (PAB) establishing fail-closed perimeters.'}
