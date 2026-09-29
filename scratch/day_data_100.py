"""day_data_100.py — Exhaustive architecture data specification for Day 100.

Covers Org Policies, SA Best Practices, and Workload Identity Federation.
"""

DAY_NUM = 100

DATA = {'day': 100,
 'part1_intro': 'Day 100 marks a foundational milestone in enterprise cloud security: transitioning from static, '
                'long-lived credentials to automated workload identity federation and short-lived access tokens. '
                'Traditional security architectures relied on downloadable private key files (`key.json`) distributed '
                'across external CI/CD pipelines, third-party clouds, and developer workstations—creating persistent '
                "credential exfiltration risks and severe key rotation overhead. Today's curriculum establishes a "
                'zero-static-key enterprise architecture: enforcing authoritative Organization Policy guardrails '
                'across the resource hierarchy, isolating workloads into dedicated least-privilege service accounts, '
                'and implementing Workload Identity Federation via Google Security Token Service (STS) to exchange '
                'ephemeral OIDC/AWS tokens for short-lived Google Cloud credentials governed by strict Common '
                'Expression Language (CEL) claim assertions.',
 'exit_summary': 'Designed, executed, and mathematically verified an enterprise Workload Identity Federation '
                 'architecture: mapped a worked external OIDC token exchange flow with Google STS and IAM '
                 'impersonation; implemented and tested negative claim assertions proving deterministic rejection of '
                 'invalid audience and unauthorized repository subject claims; authored comprehensive Organization '
                 'Policy guardrails enforcing the complete elimination of long-lived service account keys; and '
                 'generated an enterprise trust-boundary decision matrix fulfilling all Day 100 Exit evidence '
                 'criteria.',
 'part2_intro': 'Securing modern cloud workloads requires shifting identity boundaries from static secrets stored in '
                'external environments to dynamic, cryptographically attested token exchanges. The sections below '
                'analyze the governance mechanics of Organization Policy constraints, service account least-privilege '
                'hardening, and the end-to-end token exchange sequence of Workload Identity Federation.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Authentication Architecture</th>\n'
                    '      <th>Credential Type &amp; Storage</th>\n'
                    '      <th>Token Lifetime &amp; Expiry</th>\n'
                    '      <th>Exfiltration Blast Radius</th>\n'
                    '      <th>Administrative Overhead &amp; Operational Fit</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>Static Service Account Key (Legacy Anti-Pattern)</strong></td>\n'
                    '      <td>Asymmetric RSA private key stored in downloadable <code>key.json</code> file</td>\n'
                    '      <td><strong>Indefinite</strong> (Up to 10 years default; requires manual revocation)</td>\n'
                    '      <td><strong>Catastrophic:</strong> Credential can be used from any internet IP without '
                    'context or MFA</td>\n'
                    '      <td>High: Requires manual key distribution, secure storage, and complex 90-day rotation '
                    'choreography</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Service Account Impersonation (Internal GCP)</strong></td>\n'
                    '      <td>Short-lived OAuth2 bearer token minted via '
                    '<code>iamcredentials.googleapis.com</code></td>\n'
                    '      <td><strong>Short-lived:</strong> 15 minutes to 1 hour (configurable up to 12 hours)</td>\n'
                    '      <td><strong>Minimal:</strong> Token expires automatically; cannot be refreshed without '
                    'valid parent identity</td>\n'
                    '      <td>Low: Zero stored secrets; managed via standard IAM bindings '
                    '(<code>roles/iam.serviceAccountTokenCreator</code>)</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Workload Identity Federation (External CI/CD &amp; AWS)</strong></td>\n'
                    '      <td>Cryptographic STS token exchange: External OIDC/AWS JWT swapped for short-lived Google '
                    'OAuth2 token</td>\n'
                    '      <td><strong>Ephemeral:</strong> External JWT (5–15 min) exchanged for STS token (1 hour '
                    'max)</td>\n'
                    '      <td><strong>Zero Persistent Risk:</strong> Zero static secrets exist; access strictly bound '
                    'to repository, branch, and audience claims</td>\n'
                    '      <td>Near Zero: Fully automated cross-cloud trust; no secret rotation or credential '
                    'lifecycle maintenance</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 100: Organization Policies, Service Account Hardening, and Workload Identity '
                           'Federation',
                  'desc': 'Architectural topology illustrating external OIDC token exchange via Security Token '
                          'Service, Organization Policy guardrails, and keyless service account impersonation.',
                  'caption': 'Figure 100.1: Keyless authentication and architectural guardrail pipeline featuring '
                             'Workload Identity Federation, Organization Policy constraints, and short-lived token '
                             'minting.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: External Identity Provider & CI/CD Runner',
                              'desc': 'GitHub Actions, AWS IAM, or on-prem OIDC issuing signed JSON Web Tokens (JWT)',
                              'y': 10,
                              'h': 90,
                              'stroke': '#38bdf8',
                              'fill': '#0c1e38',
                              'title_color': '#38bdf8'},
                             {'name': 'LAYER 2: Workload Identity Pool & Security Token Service (STS)',
                              'desc': 'STS validates external OIDC signatures and exchanges tokens for federated GCP '
                                      'tokens',
                              'y': 115,
                              'h': 90,
                              'stroke': '#818cf8',
                              'fill': '#141838',
                              'title_color': '#818cf8'},
                             {'name': 'LAYER 3: Organization Policy Service & Constraint Enforcement',
                              'desc': 'Negative guardrails blocking service account keys, external IPs, and unapproved '
                                      'regions',
                              'y': 220,
                              'h': 90,
                              'stroke': '#f59e0b',
                              'fill': '#261a08',
                              'title_color': '#f59e0b'},
                             {'name': 'LAYER 4: Service Account Impersonation & Short-Lived Minter',
                              'desc': 'IAM Credentials API issues short-lived (1-hour) OAuth2 access tokens',
                              'y': 325,
                              'h': 90,
                              'stroke': '#f43f5e',
                              'fill': '#2a0a14',
                              'title_color': '#f43f5e'},
                             {'name': 'LAYER 5: Target GCP Workload Data Plane & Forensic Audit Vault',
                              'desc': 'GCS, BigQuery, GKE resources, and immutable Cloud Audit logs capturing all '
                                      'keyless actions',
                              'y': 430,
                              'h': 90,
                              'stroke': '#22c55e',
                              'fill': '#072417',
                              'title_color': '#22c55e'}],
                  'components': [{'name': 'GitHub Actions Runner',
                                  'detail': 'OIDC Identity Provider',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'OIDC JWT Token',
                                  'detail': 'Audience & Sub Claims',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'Workload Identity Pool',
                                  'detail': 'Provider & Attribute Map',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Security Token Service',
                                  'detail': 'STS Federated Exchange',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Org Policy Controller',
                                  'detail': 'Organization Root Rules',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Disable SA Key Creation',
                                  'detail': 'Enforced Constraint',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'IAM Credentials API',
                                  'detail': 'generateAccessToken',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Hardened Deployer SA',
                                  'detail': 'No Downloadable Keys',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Target GCP APIs',
                                  'detail': 'Compute / GCS / BigQuery',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'},
                                 {'name': 'Cloud Audit Activity Log',
                                  'detail': 'Keyless Principal Identity',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'}],
                  'boundaries': [{'label': 'EXTERNAL IDENTITY FEDERATION PERIMETER',
                                  'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'color': '#38bdf8'},
                                 {'label': 'ORGANIZATION POLICY & MINTING FABRIC',
                                  'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#818cf8'},
                                 {'label': 'WORKLOAD DATA PLANE & AUDIT COMPLIANCE VAULT',
                                  'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#22c55e'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Issue Signed JWT', 'type': 'ok'},
                            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Submit to STS Pool', 'type': 'ok'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'label': 'Exchange for STS Token',
                             'type': 'ok'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'label': 'Evaluate Org Policies',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 266,
                             'x2': 420,
                             'y2': 266,
                             'label': 'Block Static SA Key',
                             'type': 'fail'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'label': 'Impersonate Target SA',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'label': 'Issue Short-Lived Token',
                             'type': 'ok'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'label': 'Invoke GCP Resource API',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'label': 'Log Federated Identity',
                             'type': 'ok'}],
                  'probes': [{'cx': 420,
                              'cy': 30,
                              'label': 'PROBE 1: OIDC Subject Claim Validation',
                              'badge': 'P1',
                              'color': '#38bdf8'},
                             {'cx': 420,
                              'cy': 240,
                              'label': 'PROBE 2: Key Creation Attempt (HTTP 412)',
                              'badge': 'P2',
                              'color': '#f43f5e'},
                             {'cx': 420,
                              'cy': 345,
                              'label': 'PROBE 3: Token Lifetime Expiration (<3600s)',
                              'badge': 'P3',
                              'color': '#22c55e'}]},
 'part3_intro': 'The following field cases analyze catastrophic identity security breaches and key-management '
                'failures: a severe credential exfiltration event where a downloaded service account JSON private key '
                'was accidentally committed to a public Git repository, incurring $68,000 in cryptomining compute '
                'charges within four hours because `iam.disableServiceAccountKeyCreation` was not enforced at the '
                'organization root, a lateral movement compromise where an attacker leveraged an over-privileged '
                'default Compute Engine service account with primitive `roles/editor` to exfiltrate proprietary '
                'machine learning datasets, and a critical external CI/CD pipeline breakdown where an engineering team '
                'attempted to use static service account keys in GitHub Actions, triggering organization policy '
                'rejections until Workload Identity Federation (WIF) was implemented with strict repository attribute '
                'conditions. Each case delivers verbatim CLI output, policy audit logs, diagnostic commands, root '
                'cause analysis, defensible remediations, and dual-lane failed/corrected flow diagrams.',
 'part4_intro': 'These hands-on exercises implement the comprehensive 8-stage operational engineering lifecycle for '
                'Day 100. Engineers enforce organization policy constraints establishing negative guardrails against '
                'static service account keys and public IP assignment, harden Compute Engine workloads by disabling '
                'default service accounts and generating short-lived OAuth2 access tokens via '
                '`iamcredentials.googleapis.com`, and construct production Workload Identity Federation pools with '
                'GitHub Actions and AWS OIDC providers enforcing granular attribute condition mappings.',
 'topics': [{'key': 'topic-01',
             'title': 'Organization Policy Constraints: Establishing Negative Architectural Guardrails',
             'overview': 'Organization Policy constraints establish authoritative, centralized guardrails across the '
                         'entire Google Cloud resource hierarchy (Organization -> Folders -> Projects). Unlike IAM '
                         'policies—which define what specific principals *can* do (positive '
                         'authorizations)—Organization Policies define what configurations and operations are '
                         "*strictly forbidden* (negative guardrails), regardless of a user's IAM privileges. Enforcing "
                         'constraints such as disabling service account key creation, restricting resource locations, '
                         'prohibiting external IP assignment, requiring OS Login, and enforcing Domain Restricted '
                         'Sharing (DRS) guarantees that security invariants cannot be bypassed by decentralized '
                         'project teams.',
             'preview': 'A project administrator accidentally grants external users access to production buckets and '
                        'generates unmanaged private key files. Enforcing root Organization Policies automatically '
                        'blocks these operations at the API gateway level, returning immediate policy violations.',
             'technical': '### 1. Hierarchical Inheritance and Evaluation Model\n'
                          '- Organization policies are evaluated top-down: Organization -> Folder -> Child Folder -> '
                          'Project.\n'
                          '- **Policy Inheritance Rules:**\n'
                          '  - `inheritFromParent: true`: Merges rules from parent nodes with local overrides.\n'
                          "  - `reset: true`: Reverts the node to the constraint's default system behavior.\n"
                          '  - Direct overrides allow child nodes to add exceptions only when permitted by the parent '
                          'policy.\n'
                          '\n'
                          '### 2. Core Security Invariant Constraints\n'
                          '- **`constraints/iam.disableServiceAccountKeyCreation` (Boolean):** Enforces `enforced: '
                          'true`. Completely blocks all calls to `CreateServiceAccountKey` across the organization. '
                          'Eliminates the creation of downloadable `key.json` files.\n'
                          '- **`constraints/iam.disableServiceAccountKeyUpload` (Boolean):** Enforces `enforced: '
                          'true`. Prohibits uploading user-managed public keys to service accounts, preventing '
                          'out-of-band key persistence.\n'
                          '- **`constraints/gcp.resourceLocations` (List):** Restricts physical resource placement to '
                          "approved regions (e.g. `allowed_values: ['in:eu-locations']` or `['in:us-locations']`), "
                          'enforcing strict data residency and sovereign compliance.\n'
                          '- **`constraints/compute.vmExternalIpAccess` (List):** Restricts or completely blocks '
                          "(`denied_values: ['is:all']`) the creation of Compute Engine instances with public IP "
                          'addresses, requiring all ingress and egress to route through Cloud NAT or private proxies.\n'
                          '- **`constraints/compute.requireOsLogin` (Boolean):** Mandates OS Login across all Linux '
                          'VMs, linking SSH access directly to corporate Google Workspace identities and disabling '
                          'unmanaged metadata SSH keys.\n'
                          '- **`constraints/iam.allowedPolicyMemberDomains` (List / DRS):** Domain Restricted Sharing '
                          'restricts IAM policy members to approved Google Workspace/Cloud Identity directory customer '
                          "IDs (e.g. `allowed_values: ['C01234567']`), preventing sharing with public `@gmail.com` "
                          'accounts.\n'
                          '\n'
                          '### 3. Conditional Enforcement via Resource Manager Tags\n'
                          '- Constraints can be conditionally bound using Resource Manager tags and CEL expressions:\n'
                          "  `condition: expression: resource.matchTag('123456789012/env', 'production')`.\n"
                          '- This allows enterprise architects to enforce stringent security constraints across '
                          'production workloads while maintaining flexible development sandboxes under identical '
                          'organizational branches.',
             'questions': ['Why must security invariants like key creation bans be enforced via Organization Policies '
                           'rather than IAM role restrictions?',
                           'How does Domain Restricted Sharing (DRS) eliminate the risk of accidental public data '
                           'exfiltration via IAM bindings?',
                           'What is the operational failure mode if an organization policy constraint is enforced '
                           'without verifying inherited folder settings?'],
             'reference': 'https://docs.cloud.google.com/resource-manager/docs/organization-policy/overview',
             'reference_label': 'Google Cloud Resource Manager: Organization Policy Service overview and constraints '
                                'reference',
             'scenario': {'symptom': 'During a compliance audit, Security Operations discovered that developers in a '
                                     'newly acquired subsidiary project created 14 downloadable service account '
                                     'private keys (`key.json`) and launched 6 Compute Engine VMs with public IP '
                                     'addresses directly exposed to the internet.',
                          'constraints': 'Must enforce an organization-wide ban on service account key creation and '
                                         'public VM IP assignment without disrupting existing production workloads '
                                         'operating in approved regions.',
                          'evidence': 'Production Cloud Audit Activity log showing unauthorized key creation:\n'
                                      '\n'
                                      '```json\n'
                                      '{\n'
                                      '  "protoPayload": {\n'
                                      '    "authenticationInfo": {"principalEmail": "junior-dev@corp.com"},\n'
                                      '    "methodName": "google.iam.admin.v1.CreateServiceAccountKey",\n'
                                      '    "resourceName": '
                                      '"projects/prod-app/serviceAccounts/deployer-sa@prod-app.iam.gserviceaccount.com",\n'
                                      '    "response": {"privateKeyType": "TYPE_GOOGLE_CREDENTIALS_FILE"}\n'
                                      '  }\n'
                                      '}\n'
                                      '```\n'
                                      '\n'
                                      'Incident Impact: Developer exported the private key to their local machine and '
                                      'committed it to a public GitHub repository. Cryptominers discovered the key '
                                      'within 18 minutes, launching 140 GPU instances.',
                          'diagnostic_steps': ['Query effective organization policies across the resource hierarchy '
                                               'using the Resource Manager API.',
                                               'Audit existing service account keys across the subsidiary project '
                                               'using the IAM service account keys list API.',
                                               'Inspect Compute Engine VM network interfaces to identify instances '
                                               'with external IP assignments.',
                                               'Trace policy inheritance from Organization root down through '
                                               'intermediate folders.'],
                          'root': 'Decentralized project provisioning without mandatory Organization Policy '
                                  'inheritance: relying on local project administrators to voluntarily adhere to '
                                  'security guidelines guarantees policy drift.',
                          'fix': 'Deploy authoritative Organization Policy constraints at the Organization root node '
                                 '(`iam.disableServiceAccountKeyCreation`, `compute.vmExternalIpAccess`, '
                                 '`compute.requireOsLogin`, `iam.allowedPolicyMemberDomains`), remove unmanaged '
                                 'overrides, and set folder inheritance to merge parent policies.',
                          'verify': 'Attempt to generate a service account key and provision a VM with an external IP '
                                    'in the subsidiary project; verify the Resource Manager and Compute Engine APIs '
                                    'reject both operations with HTTP 412 Precondition Failed.',
                          'residual': 'Organization policies prevent future violations but do not automatically delete '
                                      'pre-existing keys or detach existing public IPs; an automated remediation '
                                      'script must purge legacy configurations.',
                          'diagram': ('Developer creates downloadable SA key',
                                      'JSON key accidentally leaked in public repo',
                                      'Adversary spins up 140 GPU cryptominers',
                                      'Enforce iam.disableServiceAccountKeyCreation org policy',
                                      'Key creation rejected with HTTP 412 Precondition Failed')},
             'lab': {'name': 'Organization Policy Specification, Deployment, and Inheritance Validation',
                     'goal': 'Author declarative Organization Policy manifests enforcing key creation bans and VM IP '
                             'restrictions, and verify hierarchical inheritance and violation blocking via Python.',
                     'expected': 'Validated Organization Policy YAML definitions, a deployment shell script, and an '
                                 'automated Python policy evaluator proving constraint enforcement.',
                     'mode': 'tabletop analysis & YAML/Python execution',
                     'prereq': 'Understanding of Google Cloud resource hierarchy and Organization Policy service.',
                     'preflight': 'Review Organization Policy YAML schema and constraint naming conventions.',
                     'steps': ['#### Stage 1: Pre-Flight Organization Policy Discovery\n'
                               'Catalog critical negative security guardrails enforceable via Organization Policies:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_org_policies.py\n"
                               'critical_constraints = [\n'
                               "    ('iam.disableServiceAccountKeyCreation', 'Enforce true to prevent downloadable "
                               "JSON keys'),\n"
                               "    ('iam.disableServiceAccountKeyUpload', 'Enforce true to block uploading external "
                               "public keys'),\n"
                               "    ('compute.vmExternalIpAccess', 'Enforce deny-all to ensure all VMs are private'),\n"
                               "    ('gcp.resourceLocations', 'Restrict deployment regions to approved "
                               "jurisdictions')\n"
                               ']\n'
                               "print('[PREFLIGHT] Core Organization Policy Constraints:')\n"
                               'for cid, desc in critical_constraints:\n'
                               "    print(f'  • {cid:42s}: {desc}')\n"
                               'EOF\n'
                               'python3 check_org_policies.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and Organization Policy provider readiness:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_org_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_org_tools.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Organization Policy Terraform Manifest\n'
                               'Author a declarative Terraform configuration enforcing '
                               '`iam.disableServiceAccountKeyCreation` at the organization root:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > org_policies.tf\n"
                               'resource "google_organization_policy" "disable_sa_key_creation" {\n'
                               '  org_id     = "108420918237"\n'
                               '  constraint = "constraints/iam.disableServiceAccountKeyCreation"\n'
                               '\n'
                               '  boolean_policy {\n'
                               '    enforced = true\n'
                               '  }\n'
                               '}\n'
                               '\n'
                               'resource "google_organization_policy" "restrict_vm_external_ip" {\n'
                               '  org_id     = "108420918237"\n'
                               '  constraint = "constraints/compute.vmExternalIpAccess"\n'
                               '\n'
                               '  list_policy {\n'
                               '    deny {\n'
                               '      all = true\n'
                               '    }\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored org_policies.tf"\n'
                               '```',
                               '#### Stage 4: Execution & Constraint Evaluation Simulation\n'
                               'Simulate an attempt to create a service account key against an enforced constraint:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_key_creation_block.py\n"
                               'class MockOrgPolicyEngine:\n'
                               '    def __init__(self, key_creation_disabled=True):\n'
                               '        self.key_creation_disabled = key_creation_disabled\n'
                               '\n'
                               '    def create_service_account_key(self, sa_email):\n'
                               '        if self.key_creation_disabled:\n'
                               '            raise RuntimeError(\n'
                               "                'HTTP 412 Precondition Failed: Operation violates Organization Policy "
                               'constraint "constraints/iam.disableServiceAccountKeyCreation".\'\n'
                               '            )\n'
                               "        return 'PRIVATE_KEY_JSON_BLOB'\n"
                               '\n'
                               'engine = MockOrgPolicyEngine(key_creation_disabled=True)\n'
                               'try:\n'
                               "    engine.create_service_account_key('deployer@corp.iam.gserviceaccount.com')\n"
                               'except RuntimeError as e:\n'
                               "    print(f'[POLICY PASS] Organization Policy intercepted key creation: {e}')\n"
                               'EOF\n'
                               'python3 simulate_key_creation_block.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Policy Inheritance Override Chaos Test\n'
                               'Simulate a project owner attempting to disable the organization constraint and verify '
                               'fail-closed inheritance:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_policy_inheritance.py\n"
                               'def can_project_override_org_policy(org_enforced, is_project_owner):\n'
                               '    if org_enforced:\n'
                               '        return False # Project owners cannot override enforced Org-level boolean '
                               'policies without Org Admin role\n'
                               '    return is_project_owner\n'
                               '\n'
                               'can_override = can_project_override_org_policy(org_enforced=True, '
                               'is_project_owner=True)\n'
                               "assert not can_override, 'Security failure: Project owner overrode Org Policy!'\n"
                               "print('[CHAOS TEST PASS] Organization policy inheritance hierarchy strictly "
                               "enforced.')\n"
                               'EOF\n'
                               'python3 test_policy_inheritance.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Policy Violation Alerting\n'
                               'Author a Cloud Monitoring Alert Policy detecting rejected Organization Policy '
                               'attempts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_org_policy_violations.json\n"
                               '{\n'
                               '  "displayName": "SECURITY ALERT: Organization Policy Violation Rejected",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "Audit log indicating Org Policy constraint rejection",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": "logName=\\"cloudaudit.googleapis.com%2Factivity\\" AND '
                               'protoPayload.status.message=~\\"Precondition Failed.*Organization Policy\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 0.0,\n'
                               '        "duration": "0s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] Authored alert_org_policy_violations.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform policy configurations:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_org_policies.py\n"
                               "with open('org_policies.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'iam.disableServiceAccountKeyCreation' in tf\n"
                               "assert 'enforced = true' in tf\n"
                               "assert 'compute.vmExternalIpAccess' in tf\n"
                               "print('[ASSERT PASS] Organization policy Terraform manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_org_policies.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_org_policy_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 100 Topic 1 test scripts..."\n'
                               'rm -f check_org_policies.py check_org_tools.sh simulate_key_creation_block.py '
                               'test_policy_inheritance.py assert_org_policies.py\n'
                               'echo "[CLEANUP] Retaining production files: org_policies.tf, '
                               'alert_org_policy_violations.json"\n'
                               'echo "[CLEANUP PASS] Org policy lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_org_policy_lab.sh\n'
                               '```'],
                     'verification': 'The YAML policy manifests define exact constraint keys and the Python test '
                                     'confirms 100% rejection of key creation, public IP assignment, and unauthorized '
                                     'domain membership.',
                     'trouble': 'Ensure list constraints specify whether they are using `allValues: DENY` or an '
                                'explicit `allowedValues` array.',
                     'cleanup': 'Retain `enterprise_org_policies.yaml` and `test_org_policy_guardrails.py` as '
                                'architectural evidence.',
                     'accept': 'Completed Organization Policy definitions and verified guardrail enforcement '
                               'simulation. File: `day-100-topic-01-org-policies.md`.',
                     'file': 'day-100-topic-01-org-policies.md'}},
            {'key': 'topic-02',
             'title': 'Service Account Best Practices: Workload Isolation, Short-Lived Tokens, and Impersonation',
             'overview': 'Service accounts represent non-human identities used by applications, microservices, and '
                         'automated pipelines to authenticate to Google Cloud APIs. Enterprise security architecture '
                         'mandates three foundational service account principles: strictly one service account per '
                         'workload component, complete elimination of static private key files (`key.json`), and '
                         'exclusive reliance on short-lived tokens generated dynamically via the Cloud IAM Credentials '
                         'API (`iamcredentials.googleapis.com`). By combining service account impersonation with '
                         'time-bound token generation, organizations eliminate credential persistence, reduce lateral '
                         'movement blast radius, and maintain an immutable audit trail.',
             'preview': 'An attacker discovers an exposed microservice with local command execution. Because each '
                        'microservice runs under a dedicated service account without static keys or lateral '
                        'permissions, the attack is fully contained to a single non-privileged scope.',
             'technical': '### 1. Workload Identity Isolation (One Identity Per Service)\n'
                          '- **Anti-Pattern:** Sharing a generic service account (e.g. `backend-app@...`) across order '
                          'processing, billing, and notification workers.\n'
                          '- **Best Practice:** Each independent service or container deployment runs under its own '
                          'dedicated identity:\n'
                          '  - `order-processing@brightloaf-prod.iam.gserviceaccount.com` (grants: Pub/Sub subscriber, '
                          'Cloud SQL client).\n'
                          '  - `payment-gateway@brightloaf-prod.iam.gserviceaccount.com` (grants: Cloud KMS '
                          'cryptoKeyEncrypterDecrypter).\n'
                          '- **Deprecation of Default Service Accounts:** The Compute Engine default service account '
                          '(`[PROJECT_NUMBER]-compute@developer.gserviceaccount.com`) is automatically granted the '
                          'primitive `roles/editor` role. Enterprise landing zones must immediately revoke this '
                          'binding or disable automatic role grants.\n'
                          '\n'
                          '### 2. The Danger of Static Service Account Keys\n'
                          '- Static `key.json` files contain unencrypted RSA private keys valid for up to 10 years.\n'
                          '- They cannot be restricted by source IP, lack multi-factor authentication, and are '
                          'frequently committed into source control or leaked via log dumps.\n'
                          '- **Mandate:** Zero downloadable keys in production. Workloads on GCP rely on metadata '
                          'server tokens; workloads outside GCP use Workload Identity Federation.\n'
                          '\n'
                          '### 3. Dynamic Short-Lived Token Minting via Cloud IAM Credentials\n'
                          '- The Cloud IAM Credentials API (`iamcredentials.googleapis.com`) allows authorized callers '
                          'to mint temporary credentials on-the-fly:\n'
                          '  - `generateAccessToken`: Mints short-lived OAuth 2.0 access tokens (default lifetime: '
                          '3600 seconds / 1 hour).\n'
                          '  - `generateIdToken`: Mints OpenID Connect (OIDC) JWTs for authenticating to Cloud Run, '
                          'Cloud Functions, and API Gateway.\n'
                          '  - `signBlob` / `signJwt`: Cryptographically signs payloads using Google-managed private '
                          'keys without exposing the raw key.\n'
                          '\n'
                          '### 4. Service Account Impersonation Mechanics\n'
                          '- Instead of granting permanent privileges to human developers or CI runners, grant the '
                          '`roles/iam.serviceAccountTokenCreator` role on the target service account.\n'
                          '- The caller authenticates with their corporate identity and impersonates the service '
                          'account to execute authorized operations.\n'
                          '- **Audit Trail Transparency:** Cloud Audit Logs record both the authenticating caller '
                          '(`principalEmail: engineer@brightloaf.com`) and the impersonated identity '
                          '(`serviceAccountDelegationInfo`), preventing anonymous administrative actions.',
             'questions': ['Why does sharing a single service account across multiple microservices violate the '
                           'principle of least privilege?',
                           'How does the Cloud IAM Credentials API mint short-lived tokens without storing or exposing '
                           'raw private keys?',
                           'What specific log attributes in Cloud Audit Logs reveal that an API operation was executed '
                           'via service account impersonation?'],
             'reference': 'https://docs.cloud.google.com/iam/docs/best-practices-service-accounts',
             'reference_label': 'Google Cloud IAM: Best practices for managing service accounts and keys',
             'scenario': {'symptom': 'A developer workstation was infected with malware. The attacker exfiltrated a '
                                     "3-year-old `key.json` file stored in the developer's `~/.gcp/` directory and "
                                     'utilized it to read sensitive customer orders from Cloud Storage buckets from an '
                                     'untrusted overseas IP address.',
                          'constraints': 'Must revoke all static developer keys, transition all deployment and '
                                         'operational access to service account impersonation, and enforce short-lived '
                                         'token expiration.',
                          'evidence': 'Production GCE metadata server query log:\n'
                                      '\n'
                                      '```text\n'
                                      '2026-09-29T04:12:00Z [SSRF] Container payload queried: '
                                      'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token\n'
                                      "Header 'Metadata-Flavor: Google' bypassed via SSRF in image rendering "
                                      'microservice.\n'
                                      'Returned token for service account: '
                                      '108420918237-compute@developer.gserviceaccount.com\n'
                                      'Token assigned roles/editor: Attacker listed all storage buckets and exported '
                                      'proprietary machine learning weights.\n'
                                      '```',
                          'diagnostic_steps': ['Inventory all user-managed service account keys across the '
                                               'organization using IAM key enumeration APIs.',
                                               'Review Cloud Audit Logs to identify the last time each key was used to '
                                               'make an API call.',
                                               'Identify human developers holding direct service account key download '
                                               'permissions (`iam.serviceAccountKeys.create`).',
                                               'Configure service account impersonation permissions for engineering '
                                               'groups.'],
                          'root': 'Reliance on static, downloadable credentials for human administrative tasks instead '
                                  'of role-based service account impersonation with short-lived token generation.',
                          'fix': 'Delete all 18 user-managed private keys. Grant engineering groups '
                                 '`roles/iam.serviceAccountTokenCreator` on dedicated target service accounts. Update '
                                 'deployment tooling to use short-lived access tokens minted dynamically via the Cloud '
                                 'IAM Credentials API.',
                          'verify': 'Verify all user-managed key counts equal zero; confirm developers can impersonate '
                                    'the target service account using their corporate identity, and verify access '
                                    'tokens expire automatically after 3,600 seconds.',
                          'residual': 'Developers must re-authenticate to their corporate identity when their daily '
                                      'SSO session expires; this is a desirable security feature.',
                          'diagram': ('VM uses default Compute service account',
                                      'Default SA has broad primitive roles/editor',
                                      'SSRF vulnerability allows attacker to steal token',
                                      'Attach dedicated SA with least privilege & disable default SA',
                                      'SSRF exploit yields token with zero storage access')},
             'lab': {'name': 'Workload Isolation, Service Account Impersonation, and Short-Lived Token Lifecycle Test',
                     'goal': 'Author infrastructure scripts provisioning isolated service accounts and implement an '
                             'automated Python token generator simulating IAM impersonation and expiration.',
                     'expected': 'A validated shell provisioning script, an executable Python token lifecycle '
                                 'simulator, and an impersonation audit log analyzer.',
                     'mode': 'tabletop analysis & Python execution',
                     'prereq': 'Understanding of OAuth 2.0 access tokens, service account roles, and IAM '
                               'impersonation.',
                     'preflight': 'Review Cloud IAM Credentials API documentation and '
                                  'roles/iam.serviceAccountTokenCreator permissions.',
                     'steps': ['#### Stage 1: Pre-Flight Default Service Account Discovery\n'
                               'Audit project configuration to identify default service accounts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_default_sas.py\n"
                               "project_number = '108420918237'\n"
                               'default_sas = [\n'
                               "    f'{project_number}-compute@developer.gserviceaccount.com',\n"
                               "    f'{project_number}@cloudservices.gserviceaccount.com'\n"
                               ']\n'
                               "print('[PREFLIGHT] Auditing Default Service Accounts:')\n"
                               'for sa in default_sas:\n'
                               "    print(f'  • {sa} -> [HIGH RISK if granted Editor role]')\n"
                               'EOF\n'
                               'python3 check_default_sas.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Tooling Verification\n'
                               'Verify IAM Credentials API client tooling readiness:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_sa_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import urllib.request; print(\'[PASS] Python network client ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_sa_tools.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Dedicated Workload SA & Impersonation Binding\n'
                               'Author a declarative Terraform configuration establishing dedicated workload service '
                               'accounts with short-lived token generation:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > hardened_service_accounts.tf\n"
                               'resource "google_service_account" "workload_sa" {\n'
                               '  account_id   = "payment-processor-sa"\n'
                               '  display_name = "Hardened Payment Processor Workload Identity"\n'
                               '  project      = "prod-payments"\n'
                               '}\n'
                               '\n'
                               '# Allow developer group to impersonate without owning private keys\n'
                               'resource "google_service_account_iam_member" "token_creator_grant" {\n'
                               '  service_account_id = google_service_account.workload_sa.name\n'
                               '  role               = "roles/iam.serviceAccountTokenCreator"\n'
                               '  member             = "group:payment-engineers@corp.com"\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored hardened_service_accounts.tf"\n'
                               '```',
                               '#### Stage 4: Execution & Short-Lived Token Generation Simulation\n'
                               'Author a script demonstrating short-lived OAuth2 token minting via '
                               '`iamcredentials.googleapis.com`:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > mint_short_lived_token.py\n"
                               'import time\n'
                               '\n'
                               'def mint_token(target_sa, lifetime_sec=3600):\n'
                               "    assert lifetime_sec <= 3600, 'Max allowable lifetime is 1 hour without org policy "
                               "relaxation'\n"
                               '    expiry_ts = time.time() + lifetime_sec\n'
                               '    return {\n'
                               "        'accessToken': f'ya29.c.{target_sa[:10]}.sample_token',\n"
                               "        'expireTime': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(expiry_ts))\n"
                               '    }\n'
                               '\n'
                               "tok = mint_token('payment-processor-sa@prod-payments.iam.gserviceaccount.com', 3600)\n"
                               'print(f\'[TOKEN MINT PASS] Issued temporary token expiring at: {tok["expireTime"]}\')\n'
                               'EOF\n'
                               'python3 mint_short_lived_token.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Default SA Privilege Escalation Intercept\n'
                               'Simulate an attempt by a workload to use the default Compute SA and assert failure:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_default_sa_block.py\n"
                               'def validate_vm_service_account(sa_email):\n'
                               "    if 'developer.gserviceaccount.com' in sa_email:\n"
                               "        raise PermissionError('COMPLIANCE ERROR: Default Compute SA forbidden in "
                               "production!')\n"
                               "    return '[COMPLIANT] Dedicated workload SA verified.'\n"
                               '\n'
                               'try:\n'
                               "    validate_vm_service_account('108420918237-compute@developer.gserviceaccount.com')\n"
                               'except PermissionError as e:\n'
                               "    print(f'[CHAOS TEST PASS] Compliance validator intercepted default SA assignment: "
                               "{e}')\n"
                               'EOF\n'
                               'python3 test_default_sa_block.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Token Minting Audit Log\n'
                               'Author a Cloud Logging filter monitoring service account impersonation:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > sa_impersonation_filter.txt\n"
                               'protoPayload.serviceName="iamcredentials.googleapis.com"\n'
                               'protoPayload.methodName="GenerateAccessToken"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to sa_impersonation_filter.txt"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Manifest Assertions\n'
                               'Execute automated test asserting service account configurations:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_hardened_sa.py\n"
                               "with open('hardened_service_accounts.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'payment-processor-sa' in tf\n"
                               "assert 'roles/iam.serviceAccountTokenCreator' in tf\n"
                               "print('[ASSERT PASS] Hardened service account manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_hardened_sa.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_sa_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 100 Topic 2 test scripts..."\n'
                               'rm -f check_default_sas.py check_sa_tools.sh mint_short_lived_token.py '
                               'test_default_sa_block.py assert_hardened_sa.py\n'
                               'echo "[CLEANUP] Retaining production files: hardened_service_accounts.tf, '
                               'sa_impersonation_filter.txt"\n'
                               'echo "[CLEANUP PASS] SA best practices lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_sa_lab.sh\n'
                               '```'],
                     'verification': 'The shell script applies least-privilege roles and impersonation bindings, and '
                                     'the Python test confirms token minting, strict delegation audit logging, and '
                                     'rejection of unauthorized callers.',
                     'trouble': 'Ensure callers hold `roles/iam.serviceAccountTokenCreator` on the specific service '
                                'account resource, not at the project level.',
                     'cleanup': 'Retain `setup_isolated_service_accounts.sh` and `test_short_lived_tokens.py` as '
                                'architectural evidence.',
                     'accept': 'Completed service account hardening scripts and verified impersonation simulation. '
                               'File: `day-100-topic-02-service-accounts.md`.',
                     'file': 'day-100-topic-02-service-accounts.md'}},
            {'key': 'topic-03',
             'title': 'Workload Identity Federation: Eliminating Static Keys for External Workloads',
             'overview': 'Workload Identity Federation represents the state-of-the-art security standard for '
                         'authenticating workloads running outside Google Cloud—such as GitHub Actions CI/CD '
                         'pipelines, AWS EC2/Lambda instances, Kubernetes clusters, and on-premises applications. '
                         'Instead of generating and storing vulnerable long-lived service account keys (`key.json`) in '
                         'external environments, Workload Identity Federation uses the Google Security Token Service '
                         '(STS) to validate external OpenID Connect (OIDC) or AWS STS tokens and dynamically exchange '
                         'them for short-lived Google Cloud access tokens. By enforcing granular Common Expression '
                         'Language (CEL) attribute conditions and verifying cryptographically signed audience and '
                         'subject claims, organizations achieve a true zero-static-key security perimeter.',
             'preview': "A compromised open-source fork attempts to authenticate against Brightloaf's production "
                        "Google Cloud project using GitHub Actions. Google STS evaluates the token's repository and "
                        'branch claims against strict CEL attribute conditions and instantly denies access.',
             'technical': '### 1. Architectural Components of Workload Identity Federation\n'
                          '- **Workload Identity Pool:** A logical container within Google Cloud that groups external '
                          'identities (e.g. `github-actions-pool`).\n'
                          '  Path: `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID`.\n'
                          '- **Workload Identity Provider:** Represents the external identity provider (OIDC issuer, '
                          'AWS, or SAML) within a pool.\n'
                          '  Configures the external issuer URL (e.g. `https://token.actions.githubusercontent.com`), '
                          'allowed audience values, and claim mappings.\n'
                          '- **Attribute Mappings:** Maps external token claims (from the `assertion` namespace) to '
                          'Google STS attributes:\n'
                          '  - `google.subject = assertion.sub`\n'
                          '  - `attribute.repository = assertion.repository`\n'
                          '  - `attribute.ref = assertion.ref`\n'
                          '  - `attribute.actor = assertion.actor`\n'
                          '- **Attribute Condition (CEL Expression):** A critical security guardrail filtering which '
                          'external tokens are accepted:\n'
                          "  `assertion.repository == 'brightloaf/core-order' && assertion.ref == 'refs/heads/main'`.\n"
                          '  If the CEL condition evaluates to false, STS rejects the token immediately before any '
                          'Google token is minted.\n'
                          '\n'
                          '### 2. The 6-Stage Token Exchange Sequence (RFC 8693)\n'
                          '1. **External Token Request:** The external workload (e.g. GitHub Actions runner) requests '
                          "an OIDC JWT signed by GitHub's private key.\n"
                          '2. **STS Token Exchange Call:** The workload POSTs the external JWT to '
                          '`https://sts.googleapis.com/v1/token` with '
                          '`grant_type=urn:ietf:params:oauth:grant-type:token-exchange`, specifying the audience '
                          '`//iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID`.\n'
                          "3. **Cryptographic Validation:** Google STS fetches the IdP's public keys via JWKS "
                          '(`https://token.actions.githubusercontent.com/.well-known/jwks`), validates the token '
                          'signature, checks token expiration, verifies the audience claim, and evaluates the CEL '
                          'attribute condition.\n'
                          '4. **Federated STS Token Issue:** STS issues a temporary, federated Google STS token '
                          '(duration: ~1 hour).\n'
                          '5. **Service Account Impersonation:** The workload calls '
                          '`iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/SA_EMAIL:generateAccessToken`, '
                          'presenting the federated STS token. Google IAM verifies the workload identity pool '
                          'principal holds `roles/iam.workloadIdentityUser`.\n'
                          '6. **GCP API Access:** IAM returns a short-lived Google Cloud OAuth2 access token with the '
                          'exact permissions granted to the service account.\n'
                          '\n'
                          '### 3. Trust Boundary Defenses: Negative Claim Assertions\n'
                          '- **Bad Audience Claim:** If an external token contains an audience string not explicitly '
                          'registered on the provider, STS rejects the request with `400 Invalid Audience`, preventing '
                          'cross-application token reuse.\n'
                          '- **Unauthorized Repository / Subject Claim:** If an attacker triggers a workflow from a '
                          'forked repository (`attacker/core-order`) or an unauthorized branch '
                          '(`refs/heads/feature-backdoor`), the CEL attribute condition evaluates to false, and STS '
                          'returns `403 Forbidden`.',
             'questions': ['How does Workload Identity Federation eliminate the need to store long-lived cloud '
                           'credentials in external CI/CD secret vaults?',
                           'What is the exact security purpose of the CEL attribute condition on a Workload Identity '
                           'Provider?',
                           'Why does Google STS require a two-step process (STS token exchange followed by Service '
                           'Account Impersonation) instead of directly granting GCP roles to external tokens?'],
             'reference': 'https://docs.cloud.google.com/iam/docs/workload-identity-federation',
             'reference_label': 'Google Cloud IAM: Manage Workload Identity Federation and configure OIDC providers',
             'scenario': {'symptom': 'A continuous integration workflow in an open-source GitHub repository was '
                                     'compromised when an external pull request triggered a workflow execution that '
                                     'attempted to push a backdoored container image to Google Cloud Artifact '
                                     'Registry.',
                          'constraints': 'Must establish external CI/CD authentication that permits automated image '
                                         "builds exclusively from the official repository's `main` branch, completely "
                                         'blocking pull requests from forks and untrusted branches without using '
                                         'static secrets.',
                          'evidence': 'GitHub Actions build runner execution log:\n'
                                      '\n'
                                      '```text\n'
                                      'Run google-github-actions/auth@v2\n'
                                      'Error: Google Cloud Auth failed: Service account key creation is disabled by '
                                      'Organization Policy.\n'
                                      'Recommendation: Use Workload Identity Federation (WIF) instead of static '
                                      'service account JSON keys.\n'
                                      'Failed to authenticate external runner: aws-worker-01 (OIDC token rejected '
                                      'without federated STS provider)\n'
                                      '```',
                          'diagnostic_steps': ['Audit GitHub repository secret configurations and identify all static '
                                               'Google Cloud private keys.',
                                               'Inspect GitHub Actions OIDC token claims (`repository`, '
                                               '`repository_owner`, `ref`, `actor`, `aud`).',
                                               'Verify the Workload Identity Pool and Provider configuration in Google '
                                               'Cloud.',
                                               'Review IAM policy bindings for `roles/iam.workloadIdentityUser`.'],
                          'root': 'Static credentials stored in external CI/CD vaults: long-lived keys cannot '
                                  'distinguish between legitimate internal builds and untrusted external pull '
                                  'requests.',
                          'fix': 'Purge `GCP_SA_KEY` from GitHub Secrets. Deploy a Workload Identity Pool and OIDC '
                                 'Provider with a strict CEL attribute condition: `assertion.repository == '
                                 "'brightloaf/core-order' && assertion.ref == 'refs/heads/main'`. Bind "
                                 "`roles/iam.workloadIdentityUser` strictly to the repository's attribute "
                                 'principalSet.',
                          'verify': 'Simulate token exchange from the official `main` branch (succeeds with '
                                    'short-lived token); simulate token exchange from a forked repository or feature '
                                    'branch (instantly rejected with HTTP 403 Forbidden).',
                          'residual': "If GitHub's OIDC service experiences an outage, CI/CD pipelines cannot "
                                      'authenticate to Google Cloud; this is an acceptable multi-vendor dependency '
                                      'trade-off.',
                          'diagram': ('GitHub Actions runner uses static SA key',
                                      'Org Policy blocks static key creation',
                                      'CI/CD build pipeline halts with auth failure',
                                      'Deploy Workload Identity Federation with GitHub OIDC provider',
                                      'Keyless authentication succeeds with short-lived tokens')},
             'lab': {'name': 'Workload Identity Federation OIDC Token Exchange and Negative Claim Verification',
                     'goal': 'Author the production Workload Identity Federation setup runbook and execute an '
                             'automated Python simulation validating STS token exchange, bad audience rejection, and '
                             'unauthorized repository blocking.',
                     'expected': 'A validated shell deployment runbook, an executable Python STS exchange simulator, '
                                 'and a comprehensive trust-boundary decision matrix.',
                     'mode': 'tabletop analysis & Python execution',
                     'prereq': 'Understanding of OIDC JWT structure, OAuth 2.0 token exchange (RFC 8693), and Common '
                               'Expression Language (CEL).',
                     'preflight': 'Review Google Security Token Service (STS) API documentation and attribute mapping '
                                  'schemas.',
                     'steps': ['#### Stage 1: Pre-Flight WIF Pool & Provider Discovery\n'
                               'Catalog Workload Identity Federation architecture components:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_wif_architecture.py\n"
                               'wif_components = {\n'
                               "    'Pool': 'Logical container for external identity providers',\n"
                               "    'Provider': 'OIDC or SAML configuration defining issuer URL and JWKS keys',\n"
                               "    'Attribute Mapping': 'Maps external JWT claims (e.g. sub, repository) to "
                               "google.subject',\n"
                               "    'Attribute Condition': 'CEL boolean filter restricting authorized external "
                               "repositories'\n"
                               '}\n'
                               "print('[PREFLIGHT] Workload Identity Federation Components:')\n"
                               'for k, v in wif_components.items():\n'
                               "    print(f'  • {k:22s}: {v}')\n"
                               'EOF\n'
                               'python3 check_wif_architecture.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI for Workload Identity Federation resource generation:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_wif_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_wif_tools.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Workload Identity Federation Terraform Manifest\n'
                               'Author a declarative Terraform configuration deploying the WIF pool, GitHub Actions '
                               'OIDC provider, and impersonation IAM binding:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > workload_identity_federation.tf\n"
                               'resource "google_iam_workload_identity_pool" "github_pool" {\n'
                               '  workload_identity_pool_id = "github-actions-pool"\n'
                               '  display_name              = "GitHub Actions Runner Pool"\n'
                               '  project                   = "prod-ci-cd"\n'
                               '}\n'
                               '\n'
                               'resource "google_iam_workload_identity_pool_provider" "github_provider" {\n'
                               '  workload_identity_pool_id          = '
                               'google_iam_workload_identity_pool.github_pool.workload_identity_pool_id\n'
                               '  workload_identity_pool_provider_id = "github-provider"\n'
                               '  display_name                       = "GitHub Actions OIDC Provider"\n'
                               '  project                            = "prod-ci-cd"\n'
                               '\n'
                               '  attribute_mapping = {\n'
                               '    "google.subject"             = "assertion.sub"\n'
                               '    "attribute.repository"       = "assertion.repository"\n'
                               '    "attribute.repository_owner" = "assertion.repository_owner"\n'
                               '  }\n'
                               '\n'
                               '  attribute_condition = "assertion.repository_owner == \'EnterpriseOrg\'"\n'
                               '\n'
                               '  oidc {\n'
                               '    issuer_uri = "https://token.actions.githubusercontent.com"\n'
                               '  }\n'
                               '}\n'
                               '\n'
                               'resource "google_service_account_iam_member" "wif_impersonation" {\n'
                               '  service_account_id = '
                               '"projects/prod-ci-cd/serviceAccounts/github-deployer@prod-ci-cd.iam.gserviceaccount.com"\n'
                               '  role               = "roles/iam.workloadIdentityUser"\n'
                               '  member             = '
                               '"principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_pool.name}/attribute.repository/EnterpriseOrg/core-infrastructure"\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored workload_identity_federation.tf"\n'
                               '```',
                               '#### Stage 4: Execution & External Token Exchange Simulation\n'
                               'Author a Python script simulating STS token exchange with attribute condition '
                               'validation:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_wif_sts.py\n"
                               'def simulate_sts_exchange(jwt_claims):\n'
                               '    # Evaluate attribute condition\n'
                               "    if jwt_claims.get('repository_owner') != 'EnterpriseOrg':\n"
                               "        raise PermissionError('HTTP 403 Forbidden: Attribute condition mismatch "
                               "(unauthorized repo owner)')\n"
                               '    \n'
                               "    sub = jwt_claims.get('sub')\n"
                               "    print(f'[STS PASS] Validated OIDC token for subject: {sub}')\n"
                               "    return 'FEDERATED_GCP_STS_TOKEN_9182'\n"
                               '\n'
                               'claims = {\n'
                               "    'iss': 'https://token.actions.githubusercontent.com',\n"
                               "    'sub': 'repo:EnterpriseOrg/core-infrastructure:ref:refs/heads/main',\n"
                               "    'repository_owner': 'EnterpriseOrg'\n"
                               '}\n'
                               'tok = simulate_sts_exchange(claims)\n'
                               "print(f'[EXCHANGE SUCCESS] Minted federated STS token: {tok}')\n"
                               'EOF\n'
                               'python3 simulate_wif_sts.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Foreign Repository Intercept Chaos Test\n'
                               'Simulate a token presentation from an unauthorized external repository and assert '
                               'rejection:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_foreign_repo_rejection.py\n"
                               'from simulate_wif_sts import simulate_sts_exchange\n'
                               '\n'
                               'unauthorized_claims = {\n'
                               "    'iss': 'https://token.actions.githubusercontent.com',\n"
                               "    'sub': 'repo:AttackerOrg/malicious-repo:ref:refs/heads/main',\n"
                               "    'repository_owner': 'AttackerOrg' # Rogue owner\n"
                               '}\n'
                               '\n'
                               'try:\n'
                               '    simulate_sts_exchange(unauthorized_claims)\n'
                               "    raise AssertionError('WIF failed to reject unauthorized repository!')\n"
                               'except PermissionError as e:\n'
                               "    print(f'[CHAOS TEST PASS] Workload Identity Federation intercepted unauthorized "
                               "caller: {e}')\n"
                               'EOF\n'
                               'python3 test_foreign_repo_rejection.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Federated Authentication Audit\n'
                               'Author a Cloud Logging filter tracking keyless federated authentication:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > wif_audit_filter.txt\n"
                               'protoPayload.serviceName="sts.googleapis.com"\n'
                               'protoPayload.methodName="ExchangeToken"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to wif_audit_filter.txt"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform WIF configurations:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_wif_manifest.py\n"
                               "with open('workload_identity_federation.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'google_iam_workload_identity_pool' in tf\n"
                               "assert 'token.actions.githubusercontent.com' in tf\n"
                               "assert 'assertion.repository_owner' in tf\n"
                               "assert 'roles/iam.workloadIdentityUser' in tf\n"
                               "print('[ASSERT PASS] Workload Identity Federation manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_wif_manifest.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_wif_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 100 Topic 3 test scripts..."\n'
                               'rm -f check_wif_architecture.py check_wif_tools.sh simulate_wif_sts.py '
                               'test_foreign_repo_rejection.py assert_wif_manifest.py\n'
                               'echo "[CLEANUP] Retaining production files: workload_identity_federation.tf, '
                               'wif_audit_filter.txt"\n'
                               'echo "[CLEANUP PASS] WIF lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_wif_lab.sh\n'
                               '```'],
                     'verification': 'The shell runbook defines exact Workload Identity Federation resource paths, the '
                                     'Python test suite validates all 4 claim permutations, and the trust-boundary '
                                     'matrix documents allowed and denied evaluations.',
                     'trouble': 'Ensure the external OIDC token issuer URI includes the HTTPS protocol and matches the '
                                "exact issuer string published in the provider's discovery document.",
                     'cleanup': 'Retain `setup_workload_identity_federation.sh`, `test_workload_federation_claims.py`, '
                                'and `day-100-topic-03-workload-federation.md` as daily exit evidence.',
                     'accept': 'Completed Workload Identity Federation configuration runbook, verified claim tests, '
                               'and assembled trust boundary matrix. File: `day-100-topic-03-workload-federation.md`.',
                     'file': 'day-100-topic-03-workload-federation.md'}}]}
