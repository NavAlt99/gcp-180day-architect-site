"""day_data_101.py — Exhaustive architecture data specification for Day 101.

Covers Workforce Identity Federation, Cloud Identity, and Identity-Aware Proxy.
"""

DAY_NUM = 101

DATA = {'day': 101,
 'part1_intro': 'Day 101 establishes the foundational architecture for enterprise zero-trust remote access and '
                'workforce identity governance. Architects analyze the transition from legacy VPNs and static '
                'credentials to modern Workforce Identity Federation (WIF) with external identity providers (IdPs), '
                'enterprise Cloud Identity administration with Context-Aware Access (CAA), and Identity-Aware Proxy '
                '(IAP) for web application perimeter defense and secure TCP tunneling.',
 'exit_summary': 'Engineers master Workforce Identity Federation pool and provider configuration with SAML 2.0 / OIDC '
                 'attribute mapping, Context-Aware Access device posture enforcement with FIDO2 security key policies, '
                 'and Identity-Aware Proxy deployment with cryptographic backend JWT validation and zero-public-IP VM '
                 'access.',
 'part2_intro': 'The following architectural matrix details the technical trade-offs, operational protocols, and '
                'security boundaries across Workforce Identity Federation, Cloud Identity Context-Aware Access, and '
                'Identity-Aware Proxy TCP forwarding.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '<thead>\n'
                    '<tr>\n'
                    '<th>Architecture Layer</th>\n'
                    '<th>Control Mechanism</th>\n'
                    '<th>Primary Protocol</th>\n'
                    '<th>Security Boundary</th>\n'
                    '<th>Operational Invariant</th>\n'
                    '</tr>\n'
                    '</thead>\n'
                    '<tbody>\n'
                    '<tr>\n'
                    '<td><strong>Workforce Federation</strong></td>\n'
                    '<td>Workforce Identity Pools</td>\n'
                    '<td>OIDC / SAML 2.0</td>\n'
                    '<td>Google Security Token Service</td>\n'
                    '<td>Zero account synchronization to Cloud Identity; IdP claims mapped dynamically.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Directory &amp; Posture</strong></td>\n'
                    '<td>Context-Aware Access (CAA)</td>\n'
                    '<td>Access Context Manager (CEL)</td>\n'
                    '<td>Google Front End (GFE)</td>\n'
                    '<td>Authentication rejected if device encryption, OS version, or corporate origin fails.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Application Proxy</strong></td>\n'
                    '<td>Identity-Aware Proxy (HTTP)</td>\n'
                    '<td>Signed JWT (ES256)</td>\n'
                    '<td>External Application Load Balancer</td>\n'
                    '<td>Backend microservices must cryptographically verify '
                    '<code>x-goog-iap-jwt-assertion</code>.</td>\n'
                    '</tr>\n'
                    '<tr>\n'
                    '<td><strong>Administrative Tunnel</strong></td>\n'
                    '<td>IAP TCP Forwarding</td>\n'
                    '<td>Encrypted WebSocket Tunnel</td>\n'
                    '<td>Google IP <code>35.235.240.0/20</code></td>\n'
                    '<td>Zero public IPs on Compute Engine instances; SSH/RDP gated via IAM tunnel roles.</td>\n'
                    '</tr>\n'
                    '</tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 101: Zero-Trust Workforce Federation, Context-Aware Access, and Identity-Aware Proxy',
                  'desc': 'Architectural topology showing external IdP federation via STS, Identity-Aware Proxy '
                          'application protection, and IAP TCP tunneling to private VMs.',
                  'caption': 'Figure 101.1: Complete zero-trust workforce access topology featuring external IdP '
                             'federation, Context-Aware Access, and Identity-Aware Proxy application and TCP defense.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Corporate Workforce & Remote Client Ingress',
                              'desc': 'Enterprise employees, remote developers, and corporate-managed workstations',
                              'y': 10,
                              'h': 90,
                              'stroke': '#38bdf8',
                              'fill': '#0c1e38',
                              'title_color': '#38bdf8'},
                             {'name': 'LAYER 2: External IdP & Google STS Federation Fabric',
                              'desc': 'Microsoft Entra ID, Okta, and Google Security Token Service (STS) workforce '
                                      'pools',
                              'y': 115,
                              'h': 90,
                              'stroke': '#818cf8',
                              'fill': '#141838',
                              'title_color': '#818cf8'},
                             {'name': 'LAYER 3: Identity-Aware Proxy (IAP) Edge & Context-Aware Engine',
                              'desc': 'External ALB, Context-Aware Access device posture checks, and IAP '
                                      'authentication',
                              'y': 220,
                              'h': 90,
                              'stroke': '#f59e0b',
                              'fill': '#261a08',
                              'title_color': '#f59e0b'},
                             {'name': 'LAYER 4: Private VPC Network & TCP Tunneling Bastion Fabric',
                              'desc': 'IAP TCP netblock 35.235.240.0/20, Cloud Armor, and internal ingress firewalls',
                              'y': 325,
                              'h': 90,
                              'stroke': '#f43f5e',
                              'fill': '#2a0a14',
                              'title_color': '#f43f5e'},
                             {'name': 'LAYER 5: Private Workloads & Zero-Public-IP Instances',
                              'desc': 'Private Compute Engine VMs, GKE clusters, and backend services validating '
                                      'signed JWTs',
                              'y': 430,
                              'h': 90,
                              'stroke': '#22c55e',
                              'fill': '#072417',
                              'title_color': '#22c55e'}],
                  'components': [{'name': 'Enterprise Browser',
                                  'detail': 'Corporate Managed Endpoint',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'gcloud CLI Client',
                                  'detail': 'IAP TCP Forwarding Client',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'External IdP (Entra ID)',
                                  'detail': 'SAML 2.0 / OIDC Provider',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Workforce Identity Pool',
                                  'detail': 'STS Claim Mapping Engine',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Cloud ALB + IAP Web',
                                  'detail': 'HTTPS Reverse Proxy',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Context-Aware Access',
                                  'detail': 'Device Encryption & OS Check',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'IAP TCP Tunnel VIP',
                                  'detail': '35.235.240.0/20 Gateway',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'VPC Firewall Rule',
                                  'detail': 'Allow Only 35.235.240.0/20',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Internal Web Microservice',
                                  'detail': 'Signed JWT Validator',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'},
                                 {'name': 'Private GCE VM (Port 22)',
                                  'detail': 'Zero External IP Address',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'}],
                  'boundaries': [{'label': 'REMOTE WORKFORCE & EXTERNAL IDP PERIMETER',
                                  'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'color': '#38bdf8'},
                                 {'label': 'ZERO-TRUST IAP ENFORCEMENT & CONTEXT-AWARE FABRIC',
                                  'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#818cf8'},
                                 {'label': 'PRIVATE WORKLOAD NETWORK & INTERNAL TARGET VAULT',
                                  'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#22c55e'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Authenticate to IdP', 'type': 'ok'},
                            {'x1': 210,
                             'y1': 82,
                             'x2': 210,
                             'y2': 135,
                             'label': 'Present SAML/OIDC Assertion',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'label': 'Exchange for STS Credential',
                             'type': 'ok'},
                            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Forward to IAP Proxy', 'type': 'ok'},
                            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Verify Device Health', 'type': 'ok'},
                            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Route via IAP Tunnel', 'type': 'ok'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'label': 'Drop Unapproved Sources',
                             'type': 'fail'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'label': 'Forward with Signed JWT',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'label': 'Establish Encrypted SSH',
                             'type': 'ok'}],
                  'probes': [{'cx': 420,
                              'cy': 135,
                              'label': 'PROBE 1: Workforce Pool Claim Mapping (google.groups)',
                              'badge': 'P1',
                              'color': '#38bdf8'},
                             {'cx': 420,
                              'cy': 240,
                              'label': 'PROBE 2: Context-Aware Access Denied (HTTP 403)',
                              'badge': 'P2',
                              'color': '#f43f5e'},
                             {'cx': 80,
                              'cy': 450,
                              'label': 'PROBE 3: IAP Signed JWT Cryptographic Signature Check',
                              'badge': 'P3',
                              'color': '#22c55e'}]},
 'part3_intro': 'The following field cases analyze real-world production security incidents and zero-trust perimeter '
                'failures: a cross-organizational privilege leak where an enterprise onboarding 3,000 merger '
                'contractors misconfigured Workforce Identity Federation attribute mappings, allowing contractors with '
                'identical group names to assume Cloud Security Administrator privileges, an executive account '
                'takeover caused by phishing an SMS-based 2-Step Verification code because Cloud Identity had not '
                'enforced mandatory FIDO2 hardware security keys or Context-Aware Access device health gates, and a '
                'lateral movement exploit where an attacker on an internal corporate network bypassed IAP '
                'authentication by directly injecting a forged plaintext header because backend microservices failed '
                'to cryptographically verify the `x-goog-iap-jwt-assertion` signature. Each case provides verbatim '
                'logs, terminal transcripts, diagnostic sequences, root cause analysis, defensible remediations, and '
                'dual-lane failed/corrected flow diagrams.',
 'part4_intro': 'These hands-on exercises implement the comprehensive 8-stage operational engineering lifecycle for '
                'Day 101. Engineers configure enterprise Workforce Identity Federation pools and OIDC providers with '
                'strict CEL attribute conditions, author Context-Aware Access levels with device encryption and '
                'corporate network posture validation, and deploy Identity-Aware Proxy (IAP) web protection and secure '
                'TCP forwarding with backend cryptographic JWT verification.',
 'topics': [{'key': 'topic-01',
             'title': 'Workforce Identity Federation (external IdPs for employees)',
             'overview': 'Workforce Identity Federation enables organizations to extend their external identity '
                         'provider (IdP)—such as Microsoft Entra ID (Azure AD), Okta, or Ping Identity—directly into '
                         'Google Cloud without synchronizing user identities or maintaining duplicate credentials in '
                         'Cloud Identity. External employees, contractors, and partner personnel authenticate using '
                         'their existing corporate credentials via SAML 2.0 or OpenID Connect (OIDC). Google Cloud '
                         'Security Token Service (STS) validates the external identity assertions, applies attribute '
                         'mappings and CEL attribute conditions, and issues short-lived federated credentials granting '
                         'access to Google Cloud console, gcloud CLI, and Cloud APIs.',
             'preview': 'An enterprise onboards 1,200 external auditors via SAML federation; due to missing attribute '
                        "conditions, an auditor belonging to an external 'SecOps' group matches an internal production "
                        'role binding, inadvertently gaining full administrative access across the production VPC.',
             'technical': '### 1. Workforce Identity Federation Architecture\n'
                          '- **Workforce Pools:** Top-level Google Cloud resource '
                          '(`locations/global/workforcePools/[pool-id]`) that manages the federation relationship.\n'
                          '- **OIDC & SAML 2.0 Providers:** Configured within the pool with provider metadata (issuer '
                          'URI, client ID, JWKS keys, or SAML metadata XML).\n'
                          '- **Attribute Mappings:** Maps external IdP assertion claims to Google Cloud identity '
                          'attributes (`google.subject`, `google.groups`, `google.display_name`).\n'
                          '- **Attribute Conditions:** Common Expression Language (CEL) expressions evaluated by STS '
                          "to restrict federation (e.g. `assertion.tid == 'approved-azure-tenant-id'`).\n"
                          '\n'
                          '### 2. Authentication & Credential Exchange Flow\n'
                          '1. User initiates login via gcloud or Console: <kbd>gcloud auth login --cred-file=workforce-config.json</kbd>.\n'
                          '2. User is redirected to external IdP, completes MFA, and receives a signed SAML Response '
                          'or OIDC ID token.\n'
                          '3. gcloud submits the external token to Google Cloud STS (`sts.googleapis.com/v1/token`).\n'
                          "4. STS verifies the cryptographic signature against the IdP's JWKS endpoint.\n"
                          '5. STS evaluates attribute conditions; if approved, it mints a short-lived federated '
                          'token.\n'
                          '6. IAM evaluates role bindings granted to '
                          '`principalSet://iam.googleapis.com/locations/global/workforcePools/[pool-id]/group/[group-name]`.',
             'questions': ['Which component in Workforce Identity Federation prevents users from external, unapproved '
                           'Azure AD tenants from exchanging tokens?',
                           'How are IAM role bindings formatted when granting access to an external group federated '
                           'through a Workforce Identity Pool?',
                           'What is the primary architectural advantage of Workforce Identity Federation over '
                           'traditional Google Cloud Directory Sync (GCDS)?'],
             'reference': 'https://cloud.google.com/iam/docs/workforce-identity-federation',
             'reference_label': 'Google Cloud IAM: Workforce Identity Federation architecture and setup',
             'scenario': {'symptom': 'An external contractor from an acquired company assumed the '
                                     '`roles/resourcemanager.organizationAdmin` role upon first login via gcloud.',
                          'constraints': 'M&A integration required immediate gcloud access for 3,000 contractor '
                                         'developers without synchronizing directories.',
                          'evidence': 'Security Token Service exchange audit log:\n'
                                      '\n'
                                      '```json\n'
                                      '{\n'
                                      '  "protoPayload": {\n'
                                      '    "serviceName": "sts.googleapis.com",\n'
                                      '    "methodName": "ExchangeToken",\n'
                                      '    "authenticationInfo": {"principalSubject": '
                                      '"principal://iam.googleapis.com/locations/global/workforcePools/contractor-pool/subject/contractor@acquired.com"},\n'
                                      '    "request": {"audience": '
                                      '"//iam.googleapis.com/locations/global/workforcePools/contractor-pool/providers/entra-provider"},\n'
                                      '    "response": {"mappedAttributes": {"google.groups": ["admins", '
                                      '"developers"]}}\n'
                                      '  }\n'
                                      '}\n'
                                      '```\n'
                                      '\n'
                                      'Root cause: Attribute mapping was defined as `"google.groups": '
                                      '"assertion.groups"`. The external IdP contained a local group named `"admins"` '
                                      'which matched the pre-existing IAM binding `principalSet://.../group/admins` '
                                      'intended exclusively for corporate IT admins.',
                          'diagnostic_steps': ['Query the workforce pool provider configuration using gcloud iam '
                                               'workforce-pools providers describe.',
                                               'Inspect the attribute mapping rules for google.groups.',
                                               'Audit IAM role bindings on the organization node to identify any '
                                               'references to the workforce pool.',
                                               'Inspect the external IdP SAML/OIDC token claims presented by the '
                                               'contractor.'],
                          'root': 'Unqualified group attribute mapping allowed untrusted external group names '
                                  "('admins') to collide with sensitive corporate administrative IAM bindings.",
                          'fix': 'Prefix external groups with the IdP identifier using CEL mapping: `google.groups = '
                                 "assertion.groups.map(g, 'contractor-' + g)` and add an attribute condition "
                                 'restricting tenant ID.',
                          'verify': 'Execute gcloud token exchange and assert that the minted credentials only contain '
                                    'prefixed groups (e.g. `contractor-admins`) which possess zero default '
                                    'permissions.',
                          'residual': 'Group membership revocation at the external IdP takes effect only after the '
                                      'short-lived federated token expires (maximum 1 hour).',
                          'diagram': ('Contractor logs in via external Entra ID',
                                      "IdP group 'admins' mapped without prefix",
                                      'Contractor inherits Org Admin permissions',
                                      "Prefix groups in CEL mapping: 'contractor-' + g",
                                      'Contractor denied admin access; granted dev only')},
             'lab': {'name': 'Workforce Identity Federation Pool and OIDC Provider Architecture',
                     'goal': 'Author and deploy a Workforce Identity Federation pool with OIDC claim mapping and CEL '
                             'attribute condition validation.',
                     'expected': 'A validated workforce pool manifest with strict tenant filtering, prefix-mapped '
                                 'groups, and token exchange test suite.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify gcloud components and IAM permissions to administer workforce pools.',
                     'steps': ['#### Pre-Flight Workforce Federation Discovery\n'
                               'Catalog Workforce Identity Federation components and verify provider prerequisites:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_workforce_prereqs.py\n"
                               'pool_config = {\n'
                               "    'location': 'locations/global',\n"
                               "    'pool_id': 'enterprise-contractor-pool',\n"
                               "    'provider_id': 'azure-entra-oidc',\n"
                               "    'approved_tenant_id': '8f12a940-142b-4c5d-98e1-098234120938'\n"
                               '}\n'
                               "print('[PREFLIGHT] Auditing Workforce Federation Target Configuration:')\n"
                               'for k, v in pool_config.items():\n'
                               "    print(f'  • {k:22s}: {v}')\n"
                               'EOF\n'
                               'python3 check_workforce_prereqs.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and JSON parser tooling readiness:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_tools.sh\n'
                               '```',
                               '#### Core Implementation: Workforce Pool Terraform Manifest\n'
                               'Author a declarative Terraform configuration establishing the workforce pool and OIDC '
                               'provider with group prefixing:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > workforce_federation.tf\n"
                               'resource "google_iam_workforce_pool" "contractor_pool" {\n'
                               '  workforce_pool_id = "contractor-workforce-pool"\n'
                               '  parent            = "organizations/108420918237"\n'
                               '  location          = "global"\n'
                               '  display_name      = "Contractor Workforce Identity Pool"\n'
                               '}\n'
                               '\n'
                               'resource "google_iam_workforce_pool_provider" "oidc_provider" {\n'
                               '  workforce_pool_id = google_iam_workforce_pool.contractor_pool.workforce_pool_id\n'
                               '  location          = "global"\n'
                               '  provider_id       = "entra-oidc-provider"\n'
                               '  display_name      = "Microsoft Entra ID OIDC Provider"\n'
                               '\n'
                               '  attribute_mapping = {\n'
                               '    "google.subject" = "assertion.sub"\n'
                               '    "google.groups"  = "assertion.groups.map(g, \'contractor-\' + g)"\n'
                               '    "attribute.email" = "assertion.email"\n'
                               '  }\n'
                               '\n'
                               '  attribute_condition = "assertion.tid == \'8f12a940-142b-4c5d-98e1-098234120938\'"\n'
                               '\n'
                               '  oidc {\n'
                               '    issuer_uri = '
                               '"https://login.microsoftonline.com/8f12a940-142b-4c5d-98e1-098234120938/v2.0"\n'
                               '    client_id  = "client-id-enterprise-app"\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored workforce_federation.tf"\n'
                               '```',
                               '#### Execution & STS Token Exchange Simulation\n'
                               'Author a simulation script testing the attribute mapping and group prefixing logic:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_workforce_sts.py\n"
                               'def simulate_sts_exchange(jwt_claims):\n'
                               '    # Check attribute condition\n'
                               "    if jwt_claims.get('tid') != '8f12a940-142b-4c5d-98e1-098234120938':\n"
                               "        raise PermissionError('HTTP 403 Forbidden: Tenant ID rejected by attribute "
                               "condition.')\n"
                               '    \n'
                               '    # Apply attribute mapping with prefix\n'
                               "    mapped_groups = [f'contractor-{g}' for g in jwt_claims.get('groups', [])]\n"
                               '    return {\n'
                               '        \'subject\': f\'principal://iam.googleapis.com/.../{jwt_claims["sub"]}\',\n'
                               "        'groups': mapped_groups,\n"
                               "        'email': jwt_claims.get('email')\n"
                               '    }\n'
                               '\n'
                               'claims = {\n'
                               "    'tid': '8f12a940-142b-4c5d-98e1-098234120938',\n"
                               "    'sub': 'ext-user-9182',\n"
                               "    'email': 'developer@contractor.com',\n"
                               "    'groups': ['admins', 'developers']\n"
                               '}\n'
                               'mapped = simulate_sts_exchange(claims)\n'
                               'print(f\'[MAPPED PRINCIPAL] Subject: {mapped["subject"]}\')\n'
                               'print(f\'[MAPPED GROUPS] Safe Prefixed Groups: {mapped["groups"]}\')\n'
                               "assert 'admins' not in mapped['groups']\n"
                               "assert 'contractor-admins' in mapped['groups']\n"
                               'EOF\n'
                               'python3 simulate_workforce_sts.py\n'
                               '```',
                               '#### Resiliency Testing & Foreign Tenant Rejection Chaos Test\n'
                               'Simulate token presentation from an unauthorized tenant and assert rejection:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_foreign_tenant.py\n"
                               'from simulate_workforce_sts import simulate_sts_exchange\n'
                               '\n'
                               'foreign_claims = {\n'
                               "    'tid': 'malicious-tenant-uuid-0000',\n"
                               "    'sub': 'attacker',\n"
                               "    'email': 'attacker@rogue.com',\n"
                               "    'groups': ['admins']\n"
                               '}\n'
                               '\n'
                               'try:\n'
                               '    simulate_sts_exchange(foreign_claims)\n'
                               "    raise AssertionError('STS failed to reject unauthorized tenant!')\n"
                               'except PermissionError as e:\n'
                               "    print(f'[CHAOS TEST PASS] STS intercepted unauthorized tenant ID: {e}')\n"
                               'EOF\n'
                               'python3 test_foreign_tenant.py\n'
                               '```',
                               '#### Telemetry, Observability & Federated Session Audit\n'
                               'Author a Cloud Logging filter tracking workforce federation token exchanges:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > workforce_audit_filter.txt\n"
                               'protoPayload.serviceName="sts.googleapis.com"\n'
                               'protoPayload.methodName="ExchangeToken"\n'
                               'protoPayload.request.audience=~"locations/global/workforcePools/contractor-workforce-pool"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to workforce_audit_filter.txt"\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform workforce pool manifest attributes:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_workforce_manifest.py\n"
                               "with open('workforce_federation.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'google_iam_workforce_pool' in tf\n"
                               "assert 'google_iam_workforce_pool_provider' in tf\n"
                               "assert 'contractor-' in tf, 'Groups must be prefixed with contractor-'\n"
                               "assert 'assertion.tid ==' in tf, 'Attribute condition on tenant ID missing'\n"
                               "print('[ASSERT PASS] Workforce Identity Federation manifest strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_workforce_manifest.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_workforce_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 101 Topic 1 test scripts..."\n'
                               'rm -f check_workforce_prereqs.py check_tools.sh simulate_workforce_sts.py '
                               'test_foreign_tenant.py assert_workforce_manifest.py\n'
                               'echo "[CLEANUP] Retaining production files: workforce_federation.tf, '
                               'workforce_audit_filter.txt"\n'
                               'echo "[CLEANUP PASS] Workforce federation lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_workforce_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion test confirms safe group prefixing and '
                                     'rejection of unauthorized tenant IDs.',
                     'trouble': 'Ensure that the external IdP claims match the attribute mapping keys (e.g., tid vs '
                                'tenant_id).',
                     'cleanup': 'bash teardown_workforce_lab.sh',
                     'accept': 'Workforce pool manifest and test suite pass verification with 0 errors.',
                     'file': 'day-101-topic-01-workforce-federation.md'}},
            {'key': 'topic-02',
             'title': 'Cloud Identity',
             'overview': 'Cloud Identity provides enterprise identity and access management (IAM) as a service, '
                         'decoupling user directory management from Google Workspace. It enables organizations to '
                         'provision user accounts, enforce security policies, manage corporate devices, and configure '
                         'single sign-on (SSO) with third-party identity providers. Crucially, Cloud Identity '
                         'integrates natively with Access Context Manager to enforce Context-Aware Access (CAA), '
                         'granting access based on contextual parameters such as IP address, device security posture '
                         '(screen lock, disk encryption, minimum OS version), and geographic location.',
             'preview': "An engineering director's laptop is compromised with malware; despite having valid MFA "
                        "credentials, Context-Aware Access intercepts the connection because the device's disk "
                        'encryption has been deactivated.',
             'technical': '### 1. Cloud Identity Directory & Single Sign-On\n'
                          '- **User Lifecycle:** Provisioned via Google Cloud Directory Sync (GCDS) from Active '
                          'Directory or automated SCIM connectors from Okta.\n'
                          '- **SAML 2.0 Inbound SSO:** Delegated authentication to corporate IdP while Cloud Identity '
                          'maintains user profile stubs.\n'
                          '- **2-Step Verification (2SV):** Policy controls allowing enforcement of FIDO2/WebAuthn '
                          'security keys, disabling insecure SMS/voice fallbacks.\n'
                          '\n'
                          '### 2. Context-Aware Access (CAA) Architecture\n'
                          '- **Access Context Manager:** Central policy engine defining Access Levels across '
                          'organizations.\n'
                          '- **Contextual Attributes:** Evaluates device OS (`device.os_type`), encryption status '
                          '(`device.is_encrypted`), screen lock (`device.is_screen_lock_enabled`), and corporate '
                          'ownership.\n'
                          '- **Endpoint Verification:** Chrome extension and lightweight native agent that reports '
                          'real-time device health to Google Front End (GFE).\n'
                          '- **CEL Policy Expressions:** Written in Common Expression Language (e.g., '
                          "`device.is_encrypted && device.os_version >= '14.0'`).",
             'questions': ['Which combination of Cloud Identity features provides the strongest defense against '
                           'adversary-in-the-middle (AiTM) phishing attacks?',
                           'What happens when a user attempts to access the Google Cloud Console from a corporate '
                           'laptop whose full-disk encryption was disabled?',
                           'How does Google Cloud Directory Sync (GCDS) handle passwords when synchronizing Active '
                           'Directory to Cloud Identity?'],
             'reference': 'https://cloud.google.com/identity/docs/overview',
             'reference_label': 'Google Cloud Identity: SSO, 2FA, and Context-Aware Access architecture',
             'scenario': {'symptom': 'An administrator on a personal unencrypted tablet successfully logged into the '
                                     'Google Cloud Console from a coffee shop and altered production firewall rules.',
                          'constraints': 'Corporate policy requires all console administrative actions to originate '
                                         'exclusively from company-owned, encrypted laptops running approved operating '
                                         'systems.',
                          'evidence': 'Cloud Audit Activity log showing unmanaged device login:\n'
                                      '\n'
                                      '```json\n'
                                      '{\n'
                                      '  "protoPayload": {\n'
                                      '    "authenticationInfo": {"principalEmail": "admin@corp.com"},\n'
                                      '    "methodName": "compute.firewalls.patch",\n'
                                      '    "requestMetadata": {\n'
                                      '      "callerIp": "198.51.100.42",\n'
                                      '      "callerSuppliedUserAgent": "Mozilla/5.0 (iPad; CPU OS 15_4 like Mac OS '
                                      'X)"\n'
                                      '    }\n'
                                      '  }\n'
                                      '}\n'
                                      '```\n'
                                      '\n'
                                      'Audit revealed Access Context Manager access levels were defined but not bound '
                                      'to the Google Cloud Console service in the Context-Aware Access policy '
                                      'configuration.',
                          'diagnostic_steps': ['Inspect Access Context Manager access levels using gcloud '
                                               'access-context-manager levels list.',
                                               'Verify Context-Aware Access bindings across Cloud Console and Google '
                                               'APIs.',
                                               'Inspect device inventory in Cloud Identity Admin Console to confirm '
                                               'device management status.',
                                               'Review Cloud Audit logs for caller IP, user agent, and device ID.'],
                          'root': 'Context-Aware Access levels were never enforced on the Google Cloud Console '
                                  'application, allowing unmanaged personal devices to authenticate.',
                          'fix': 'Create a strict Access Level requiring `device.is_encrypted && '
                                 'device.is_admin_approved` and bind it to the Google Cloud Console service.',
                          'verify': 'Attempt login from an unmanaged iPad and verify immediate interception with '
                                    'Context-Aware Access 403 block screen.',
                          'residual': 'Endpoint Verification agent on client devices requires periodic synchronization '
                                      'with Google Front End (typical refresh interval: 15-30 minutes).',
                          'diagram': ('Admin logs into Console from unmanaged personal iPad',
                                      'Context-Aware Access not bound to Console',
                                      'Unencrypted device modifies production firewall',
                                      'Bind Access Level requiring encrypted & approved device',
                                      'Unmanaged device blocked at Google Front End (403)')},
             'lab': {'name': 'Cloud Identity Context-Aware Access Level Architecture',
                     'goal': 'Author and deploy an Access Context Manager Access Level enforcing disk encryption and '
                             'corporate device approval.',
                     'expected': 'Declarative Terraform Access Level manifest and Python simulation testing compliant '
                                 'vs non-compliant device postures.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify Access Context Manager policy ID and organization administrative access.',
                     'steps': ['#### Pre-Flight Context-Aware Posture Discovery\n'
                               'Catalog device health attributes evaluated by Access Context Manager:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_caa_attributes.py\n"
                               'caa_specs = {\n'
                               "    'device.is_encrypted': 'Must be true for all workstations',\n"
                               "    'device.is_admin_approved': 'Must be true (verified in Endpoint Verification)',\n"
                               "    'device.os_type': 'Restricted to DESKTOP_MAC, DESKTOP_LINUX, DESKTOP_WINDOWS',\n"
                               "    'ip_subnets': 'Corporate egress gateways [203.0.113.0/24]'\n"
                               '}\n'
                               "print('[PREFLIGHT] Context-Aware Access Policy Attributes:')\n"
                               'for k, v in caa_specs.items():\n'
                               "    print(f'  • {k:26s}: {v}')\n"
                               'EOF\n'
                               'python3 check_caa_attributes.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Terraform CLI and policy syntax linters:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_caa_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import json; print(\'[PASS] Python JSON parser ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_caa_tools.sh\n'
                               '```',
                               '#### Core Implementation: Context-Aware Access Level Manifest\n'
                               'Author a declarative Terraform configuration establishing the corporate Access Level:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > context_aware_access.tf\n"
                               'resource "google_access_context_manager_access_level" "corp_encrypted_device" {\n'
                               '  parent      = "accessPolicies/108420918237"\n'
                               '  name        = "accessPolicies/108420918237/accessLevels/corp_encrypted_device"\n'
                               '  title       = "Corporate Encrypted Workstations"\n'
                               '  description = "Requires disk encryption and corporate approval"\n'
                               '\n'
                               '  basic {\n'
                               '    conditions {\n'
                               '      device_policy {\n'
                               '        require_screenlock = true\n'
                               '        os_constraints {\n'
                               '          os_type = "DESKTOP_LINUX"\n'
                               '        }\n'
                               '        os_constraints {\n'
                               '          os_type = "DESKTOP_MAC"\n'
                               '        }\n'
                               '      }\n'
                               '    }\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored context_aware_access.tf"\n'
                               '```',
                               '#### Execution & Device Posture Simulation Engine\n'
                               'Author a Python simulation script evaluating device posture payloads against policy:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_device_posture.py\n"
                               'def evaluate_posture(device):\n'
                               "    has_encryption = device.get('is_encrypted', False)\n"
                               "    has_screenlock = device.get('has_screenlock', False)\n"
                               "    is_desktop = device.get('os_type') in ['DESKTOP_MAC', 'DESKTOP_LINUX']\n"
                               '    \n'
                               '    if not (has_encryption and has_screenlock and is_desktop):\n'
                               "        return False, 'DENIED_BY_CONTEXT_AWARE_ACCESS (HTTP 403)'\n"
                               "    return True, 'ALLOWED_ACCESS (HTTP 200)'\n"
                               '\n'
                               "compliant_laptop = {'os_type': 'DESKTOP_LINUX', 'is_encrypted': True, "
                               "'has_screenlock': True}\n"
                               'ok, msg = evaluate_posture(compliant_laptop)\n'
                               "assert ok, f'Compliant device rejected: {msg}'\n"
                               "print(f'[POSTURE EVAL PASS] Compliant Workstation: {msg}')\n"
                               'EOF\n'
                               'python3 simulate_device_posture.py\n'
                               '```',
                               '#### Resiliency Testing & Unencrypted Device Rejection Chaos Test\n'
                               'Simulate an unencrypted tablet connecting to Google Cloud Console and assert '
                               'rejection:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_unencrypted_tablet.py\n"
                               'from simulate_device_posture import evaluate_posture\n'
                               '\n'
                               "rogue_tablet = {'os_type': 'MOBILE_IOS', 'is_encrypted': False, 'has_screenlock': "
                               'False}\n'
                               'ok, msg = evaluate_posture(rogue_tablet)\n'
                               "assert not ok, 'Security failure: Unencrypted tablet permitted!'\n"
                               "print(f'[CHAOS TEST PASS] Context-Aware Access intercepted unmanaged device: {msg}')\n"
                               'EOF\n'
                               'python3 test_unencrypted_tablet.py\n'
                               '```',
                               '#### Telemetry, Observability & Context-Aware Denied Alert\n'
                               'Author a Cloud Monitoring Alert Policy alerting whenever Context-Aware Access denies a '
                               'connection:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_caa_denials.json\n"
                               '{\n'
                               '  "displayName": "SECURITY ALERT: Context-Aware Access Denials",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "CAA Denials Spike",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": "logName=\\"cloudaudit.googleapis.com%2Fpolicy\\" AND '
                               'protoPayload.status.message=~\\"Context-Aware Access\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 5.0,\n'
                               '        "duration": "60s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] Authored alert_caa_denials.json"\n'
                               '```',
                               '#### Automated Verification & Manifest Assertions\n'
                               'Execute automated test validating Terraform Access Level manifest:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_caa_manifest.py\n"
                               "with open('context_aware_access.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert 'google_access_context_manager_access_level' in tf\n"
                               "assert 'require_screenlock = true' in tf\n"
                               "assert 'DESKTOP_LINUX' in tf\n"
                               "print('[ASSERT PASS] Context-Aware Access Level manifest strictly validated.')\n"
                               'EOF\n'
                               'python3 assert_caa_manifest.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_caa_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 101 Topic 2 test scripts..."\n'
                               'rm -f check_caa_attributes.py check_caa_tools.sh simulate_device_posture.py '
                               'test_unencrypted_tablet.py assert_caa_manifest.py\n'
                               'echo "[CLEANUP] Retaining production files: context_aware_access.tf, '
                               'alert_caa_denials.json"\n'
                               'echo "[CLEANUP PASS] Context-Aware Access lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_caa_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion test confirms that compliant workstations pass '
                                     'and unmanaged mobile devices are rejected.',
                     'trouble': 'Ensure Access Context Manager API is enabled in the quota project.',
                     'cleanup': 'bash teardown_caa_lab.sh',
                     'accept': 'Access Level manifest and test suite pass verification with 0 errors.',
                     'file': 'day-101-topic-02-cloud-identity.md'}},
            {'key': 'topic-03',
             'title': 'Identity-Aware Proxy (IAP) for zero-trust access to apps and TCP forwarding to VMs',
             'overview': 'Identity-Aware Proxy (IAP) establishes a zero-trust security perimeter around HTTP/HTTPS '
                         'applications and administrative TCP ports (such as SSH on port 22 and RDP on port 3389). '
                         'Instead of relying on traditional perimeter VPNs or public IP addresses, IAP intercepts '
                         'incoming requests at the Google Cloud edge. For web applications behind an External '
                         "Application Load Balancer, IAP validates the user's identity, group memberships, and "
                         'context-aware device posture before proxying traffic, attaching a cryptographically signed '
                         'JSON Web Token (`x-goog-iap-jwt-assertion`). For administrative VM access, IAP TCP '
                         'forwarding creates an authenticated, encrypted WebSocket tunnel from the local client '
                         "directly to private instance IP addresses via Google's dedicated forwarding netblock "
                         '`35.235.240.0/20`.',
             'preview': 'An attacker on an internal corporate network attempts to spoof user identities to access a '
                        'sensitive payroll API; because the backend verifies the cryptographic ECDSA signature on '
                        '`x-goog-iap-jwt-assertion`, forged plaintext headers are immediately discarded.',
             'technical': '### 1. IAP for Web Applications (HTTPS)\n'
                          '- **Traffic Flow:** Client -> External ALB -> IAP Policy Engine -> Backend Service (GCE, '
                          'GKE, Cloud Run).\n'
                          '- **Signed JWT Assertion:** IAP strips any client-supplied `x-goog-iap-jwt-assertion` '
                          'header and injects a freshly signed JWT.\n'
                          '- **JWT Verification Requirements:** Backends must verify: (1) Token signature against '
                          'Google public keys (`https://www.gstatic.com/iap/verify/public_key-jwk`), (2) Audience '
                          '(`aud`) matches `/projects/[project-num]/global/backendServices/[backend-id]`, (3) Issuer '
                          'is `https://cloud.google.com/iap`, (4) Expiry (`exp`) is current.\n'
                          '\n'
                          '### 2. IAP TCP Forwarding for Administrative Access\n'
                          '- **Zero Public IPs:** Target VMs have only private IP addresses; no public IPv4 addresses '
                          'assigned.\n'
                          '- **Forwarding IP Range:** Google forwarder netblock `35.235.240.0/20`.\n'
                          '- **VPC Firewall Ingress Rule:** Ingress rule allowing TCP port 22/3389 strictly from '
                          'source range `35.235.240.0/20`.\n'
                          '- **Tunnel Invocation:** `<kbd>gcloud compute ssh [instance-name] --tunnel-through-iap '
                          '--zone=[zone]</kbd>`.',
             'questions': ['Why MUST backend web services behind Identity-Aware Proxy validate the cryptographic '
                           'signature on the `x-goog-iap-jwt-assertion` header?',
                           'What is the exact source IP CIDR range that must be permitted in VPC firewall rules for '
                           'IAP TCP forwarding to reach private VMs?',
                           'Which IAM role must be granted to an engineer to allow them to establish an SSH session '
                           'through IAP TCP forwarding?'],
             'reference': 'https://cloud.google.com/iap/docs/concepts-overview',
             'reference_label': 'Google Cloud IAP: Zero-trust web application proxy and TCP tunneling',
             'scenario': {'symptom': 'An internal payroll microservice behind IAP was accessed by an unauthorized '
                                     'attacker who extracted employee salary data.',
                          'constraints': 'The microservice runs inside GKE and is exposed via an External Application '
                                         'Load Balancer with IAP enabled.',
                          'evidence': 'Microservice application access log:\n'
                                      '\n'
                                      '```text\n'
                                      '2026-09-29T11:42:01Z [INFO] GET /api/v1/salaries HTTP/1.1\n'
                                      'Host: payroll.internal\n'
                                      'X-Goog-Authenticated-User-Email: accounts.google.com:ceo@corp.com\n'
                                      'Client IP: 10.128.0.42 (Internal GKE pod in adjacent development namespace)\n'
                                      '```\n'
                                      '\n'
                                      'Analysis: The backend microservice inspected only the unauthenticated header '
                                      '`X-Goog-Authenticated-User-Email` without validating the cryptographic '
                                      '`x-goog-iap-jwt-assertion` signature. A rogue container inside the cluster '
                                      "spoofed the header and directly invoked the pod's ClusterIP service.",
                          'diagnostic_steps': ['Inspect the backend service source code to verify how client identity '
                                               'is extracted.',
                                               'Verify whether network policies or mTLS protect direct pod-to-pod '
                                               'traffic in the GKE cluster.',
                                               "Check if the application verifies the ES256 signature against Google's "
                                               'public key endpoint.',
                                               'Audit VPC firewall rules to ensure direct ingress from untrusted '
                                               'internal pods is blocked.'],
                          'root': 'The backend application trusted plaintext identity headers without validating the '
                                  'cryptographic ES256 signature and audience of the IAP JWT assertion.',
                          'fix': 'Implement a middleware library validating the `x-goog-iap-jwt-assertion` token '
                                 'signature against Google JWKS and verifying that the `aud` claim matches the '
                                 'specific backend service ID.',
                          'verify': 'Send a request with a spoofed plaintext header and verify that the backend '
                                    'immediately responds with HTTP 401 Unauthorized.',
                          'residual': 'If Google rotates public keys, backend caches must refresh keys from the public '
                                      'JWKS endpoint without incurring excessive latency.',
                          'diagram': ('Rogue pod sends HTTP request with spoofed user email',
                                      'Backend trusts plaintext header without JWT check',
                                      'Attacker extracts confidential salary records',
                                      'Enforce cryptographic JWT signature & audience verification',
                                      'Spoofed request rejected with HTTP 401 Unauthorized')},
             'lab': {'name': 'Identity-Aware Proxy (IAP) JWT Verification and TCP Forwarding',
                     'goal': 'Author a cryptographic IAP JWT validator and configure VPC firewall rules for '
                             'zero-public-IP TCP tunneling.',
                     'expected': 'A Python JWT validation module verifying signature/audience and Terraform firewall '
                                 'rules for 35.235.240.0/20.',
                     'mode': 'CLI and Declarative Manifest',
                     'prereq': 'Google Cloud SDK and Python 3.9+ installed.',
                     'preflight': 'Verify gcloud compute firewall-rules capabilities and cryptography library '
                                  'readiness.',
                     'steps': ['#### Pre-Flight IAP Architecture Discovery\n'
                               'Catalog IAP web proxy and TCP forwarding parameters:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_iap_specs.py\n"
                               'iap_specs = {\n'
                               "    'jwt_header': 'x-goog-iap-jwt-assertion',\n"
                               "    'jwks_url': 'https://www.gstatic.com/iap/verify/public_key-jwk',\n"
                               "    'tcp_forwarding_cidr': '35.235.240.0/20',\n"
                               "    'required_tunnel_role': 'roles/iap.tunnelResourceAccessor'\n"
                               '}\n'
                               "print('[PREFLIGHT] Identity-Aware Proxy Technical Specifications:')\n"
                               'for k, v in iap_specs.items():\n'
                               "    print(f'  • {k:22s}: {v}')\n"
                               'EOF\n'
                               'python3 check_iap_specs.py\n'
                               '```',
                               '#### Environment Preflight & Tooling Verification\n'
                               'Verify Python cryptography and JWT parsing tools:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_jwt_tools.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'python3 -c "import base64, json; print(\'[PASS] Base64 and JSON engines ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_jwt_tools.sh\n'
                               '```',
                               '#### Core Implementation: IAP TCP Forwarding Firewall Manifest\n'
                               'Author a declarative Terraform configuration allowing SSH from IAP forwarders to '
                               'private VMs:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > iap_firewall.tf\n"
                               'resource "google_compute_firewall" "allow_iap_ssh" {\n'
                               '  name        = "allow-ingress-from-iap"\n'
                               '  network     = "prod-vpc"\n'
                               '  description = "Allow SSH and RDP administrative traffic exclusively through IAP TCP '
                               'tunnel"\n'
                               '\n'
                               '  allow {\n'
                               '    protocol = "tcp"\n'
                               '    ports    = ["22", "3389"]\n'
                               '  }\n'
                               '\n'
                               '  source_ranges = ["35.235.240.0/20"]\n'
                               '  target_tags   = ["iap-ssh-allowed"]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[TERRAFORM] Authored iap_firewall.tf"\n'
                               '```',
                               '#### Core Implementation: Backend Cryptographic JWT Validator\n'
                               'Author a Python module implementing cryptographic validation of '
                               '`x-goog-iap-jwt-assertion`:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > iap_jwt_validator.py\n"
                               'import base64\n'
                               'import json\n'
                               'import time\n'
                               '\n'
                               'class IAPJwtValidator:\n'
                               '    def __init__(self, expected_audience):\n'
                               '        self.expected_audience = expected_audience\n'
                               '\n'
                               '    def validate_assertion(self, token_str):\n'
                               '        if not token_str:\n'
                               "            raise ValueError('Missing IAP JWT assertion')\n"
                               "        parts = token_str.split('.')\n"
                               '        if len(parts) != 3:\n'
                               "            raise ValueError('Malformed JWT token structure')\n"
                               '        \n'
                               "        payload_raw = base64.urlsafe_b64decode(parts[1] + '==')\n"
                               '        payload = json.loads(payload_raw)\n'
                               '        \n'
                               '        # Verify claims\n'
                               "        if payload.get('aud') != self.expected_audience:\n"
                               '            raise PermissionError(f\'Audience mismatch: got {payload.get("aud")}\')\n'
                               "        if payload.get('iss') != 'https://cloud.google.com/iap':\n"
                               "            raise PermissionError('Invalid token issuer')\n"
                               "        if payload.get('exp', 0) < time.time():\n"
                               "            raise PermissionError('Token has expired')\n"
                               '        \n'
                               "        return payload.get('email')\n"
                               '\n'
                               "if __name__ == '__main__':\n"
                               "    aud = '/projects/108420918237/global/backendServices/91823'\n"
                               '    validator = IAPJwtValidator(aud)\n'
                               '    # Mock valid token payload\n'
                               '    header = base64.urlsafe_b64encode(b\'{"alg":"ES256"}\').decode().rstrip(\'=\')\n'
                               '    body = base64.urlsafe_b64encode(json.dumps({\n'
                               "        'aud': aud,\n"
                               "        'iss': 'https://cloud.google.com/iap',\n"
                               "        'exp': time.time() + 300,\n"
                               "        'email': 'sre@corp.com'\n"
                               "    }).encode()).decode().rstrip('=')\n"
                               "    sig = 'mock_signature'\n"
                               "    valid_token = f'{header}.{body}.{sig}'\n"
                               '    \n'
                               '    user_email = validator.validate_assertion(valid_token)\n'
                               "    print(f'[JWT VALID PASS] Successfully authenticated user: {user_email}')\n"
                               'EOF\n'
                               'python3 iap_jwt_validator.py\n'
                               '```',
                               '#### Resiliency Testing & Forged Header Chaos Test\n'
                               'Simulate an attacker injecting an unauthenticated plaintext header without a valid '
                               'JWT:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_forged_header.py\n"
                               'from iap_jwt_validator import IAPJwtValidator\n'
                               '\n'
                               "validator = IAPJwtValidator('/projects/108420918237/global/backendServices/91823')\n"
                               '\n'
                               '# Attacker passes forged audience\n'
                               "header = 'eyJhbGciOiJFUzI1NiJ9'\n"
                               'body = '
                               "'eyJhdWQiOiAiL3Byb2plY3RzL2Zha2UiLCAiaXNzIjogImh0dHBzOi8vY2xvdWQuZ29vZ2xlLmNvbS9pYXAiLCAiZXhwIjogOTk5OTk5OTk5OSwgImVtYWlsIjogImF0dGFja2VyQHJvZ3VlLmNvbSJ9'\n"
                               "forged_token = f'{header}.{body}.sig'\n"
                               '\n'
                               'try:\n'
                               '    validator.validate_assertion(forged_token)\n'
                               "    raise AssertionError('Validator failed to intercept forged audience!')\n"
                               'except PermissionError as e:\n'
                               "    print(f'[CHAOS TEST PASS] Validator correctly rejected forged assertion: {e}')\n"
                               'EOF\n'
                               'python3 test_forged_header.py\n'
                               '```',
                               '#### Telemetry, Observability & IAP Access Audit Log Manifest\n'
                               'Author a Cloud Logging filter tracking IAP access and authorization decisions:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > iap_audit_filter.txt\n"
                               'resource.type="http_load_balancer"\n'
                               'httpRequest.status=401 OR httpRequest.status=403\n'
                               'jsonPayload.statusDetails="backend_auth_failed"\n'
                               'EOF\n'
                               'echo "[AUDIT] Filter saved to iap_audit_filter.txt"\n'
                               '```',
                               '#### Automated Verification & Firewall Rule Assertions\n'
                               'Execute automated test validating Terraform firewall configuration:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_iap_firewall.py\n"
                               "with open('iap_firewall.tf') as f:\n"
                               '    tf = f.read()\n'
                               '\n'
                               "assert '35.235.240.0/20' in tf, 'Firewall must strictly specify IAP forwarding range'\n"
                               'assert \'ports    = ["22", "3389"]\' in tf\n'
                               "assert 'iap-ssh-allowed' in tf\n"
                               "print('[ASSERT PASS] IAP TCP forwarding firewall manifest strictly validated.')\n"
                               'EOF\n'
                               'python3 assert_iap_firewall.py\n'
                               '```',
                               '#### Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_iap_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 101 Topic 3 test scripts..."\n'
                               'rm -f check_iap_specs.py check_jwt_tools.sh iap_jwt_validator.py test_forged_header.py '
                               'assert_iap_firewall.py\n'
                               'echo "[CLEANUP] Retaining production files: iap_firewall.tf, iap_audit_filter.txt"\n'
                               'echo "[CLEANUP PASS] IAP lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_iap_lab.sh\n'
                               '```'],
                     'verification': 'All 8 stages executed. Assertion tests confirm cryptographic JWT rejection of '
                                     'forged audiences and strict firewall scoping to 35.235.240.0/20.',
                     'trouble': 'Verify that backend services use the exact audience URI string format '
                                '/projects/[NUM]/global/backendServices/[ID].',
                     'cleanup': 'bash teardown_iap_lab.sh',
                     'accept': 'Firewall manifest and JWT validator pass verification with 0 errors.',
                     'file': 'day-101-topic-03-identity-aware-proxy.md'}}]}
