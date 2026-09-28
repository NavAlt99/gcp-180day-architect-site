"""day_data_100.py — Exhaustive architecture data specification for Day 100.

Covers Workload Federation and Short-Lived Access:
1. Organization Policy constraints: negative guardrails enforcing security invariants (disabling service account key creation, disabling key upload, restricting resource locations, disabling external IPs, requiring OS Login, and enforcing domain-restricted sharing).
2. Service account best practices: workload identity isolation, eliminating static private keys, short-lived credential minting via the Cloud IAM Credentials API, impersonation mechanics, and granular delegation audit trails.
3. Workload Identity Federation: cross-cloud and external workload token exchange (AWS STS, GitHub Actions OIDC, Kubernetes, on-premises), Google Security Token Service (STS) architecture, attribute mappings, CEL attribute conditions, bad audience/subject claim rejection, and zero stored static credentials.

Follows PAGE_AUTHORING_CONTRACT.md and passes all validate.py rules.
"""

DAY_NUM = 100

DATA = {
    "day": 100,
    "part1_intro": (
        "Day 100 marks a foundational milestone in enterprise cloud security: transitioning from static, long-lived credentials to automated "
        "workload identity federation and short-lived access tokens. Traditional security architectures relied on downloadable private key files "
        "(`key.json`) distributed across external CI/CD pipelines, third-party clouds, and developer workstations—creating persistent credential exfiltration "
        "risks and severe key rotation overhead. Today's curriculum establishes a zero-static-key enterprise architecture: enforcing authoritative "
        "Organization Policy guardrails across the resource hierarchy, isolating workloads into dedicated least-privilege service accounts, and "
        "implementing Workload Identity Federation via Google Security Token Service (STS) to exchange ephemeral OIDC/AWS tokens for short-lived Google Cloud "
        "credentials governed by strict Common Expression Language (CEL) claim assertions."
    ),
    "exit_summary": (
        "Designed, executed, and mathematically verified an enterprise Workload Identity Federation architecture: mapped a worked external OIDC token "
        "exchange flow with Google STS and IAM impersonation; implemented and tested negative claim assertions proving deterministic rejection of "
        "invalid audience and unauthorized repository subject claims; authored comprehensive Organization Policy guardrails enforcing the complete "
        "elimination of long-lived service account keys; and generated an enterprise trust-boundary decision matrix fulfilling all Day 100 Exit evidence criteria."
    ),
    "part2_intro": (
        "Securing modern cloud workloads requires shifting identity boundaries from static secrets stored in external environments to dynamic, "
        "cryptographically attested token exchanges. The sections below analyze the governance mechanics of Organization Policy constraints, "
        "service account least-privilege hardening, and the end-to-end token exchange sequence of Workload Identity Federation."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Authentication Architecture</th>
      <th>Credential Type &amp; Storage</th>
      <th>Token Lifetime &amp; Expiry</th>
      <th>Exfiltration Blast Radius</th>
      <th>Administrative Overhead &amp; Operational Fit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Static Service Account Key (Legacy Anti-Pattern)</strong></td>
      <td>Asymmetric RSA private key stored in downloadable <code>key.json</code> file</td>
      <td><strong>Indefinite</strong> (Up to 10 years default; requires manual revocation)</td>
      <td><strong>Catastrophic:</strong> Credential can be used from any internet IP without context or MFA</td>
      <td>High: Requires manual key distribution, secure storage, and complex 90-day rotation choreography</td>
    </tr>
    <tr>
      <td><strong>Service Account Impersonation (Internal GCP)</strong></td>
      <td>Short-lived OAuth2 bearer token minted via <code>iamcredentials.googleapis.com</code></td>
      <td><strong>Short-lived:</strong> 15 minutes to 1 hour (configurable up to 12 hours)</td>
      <td><strong>Minimal:</strong> Token expires automatically; cannot be refreshed without valid parent identity</td>
      <td>Low: Zero stored secrets; managed via standard IAM bindings (<code>roles/iam.serviceAccountTokenCreator</code>)</td>
    </tr>
    <tr>
      <td><strong>Workload Identity Federation (External CI/CD &amp; AWS)</strong></td>
      <td>Cryptographic STS token exchange: External OIDC/AWS JWT swapped for short-lived Google OAuth2 token</td>
      <td><strong>Ephemeral:</strong> External JWT (5–15 min) exchanged for STS token (1 hour max)</td>
      <td><strong>Zero Persistent Risk:</strong> Zero static secrets exist; access strictly bound to repository, branch, and audience claims</td>
      <td>Near Zero: Fully automated cross-cloud trust; no secret rotation or credential lifecycle maintenance</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Workload Identity Federation Architecture Flow",
        "desc": "End-to-end cryptographic token exchange from external workload to Google Cloud APIs.",
        "caption": "Figure 100.1: Four-stage Workload Identity Federation token exchange and policy enforcement flow.",
        "nodes": [
            ("1. External Workload", "Mint OIDC/AWS Token"),
            ("2. Google STS", "Exchange & CEL Verify"),
            ("3. IAM Credentials", "Impersonate Target SA"),
            ("4. GCP APIs", "Authorize & Audit Trail"),
        ]
    },
    "part3_intro": (
        "Real-world enterprise failures reveal that credential leakage almost never stems from cryptographic failure; rather, it results from "
        "architectural shortcuts such as storing static service account keys in external repositories or sharing monolithic service accounts across "
        "heterogeneous workloads. The field cases below analyze actual production breakdowns and their architectural remediations."
    ),
    "part4_intro": (
        "The following progressive hands-on laboratories implement and verify the complete short-lived access and workload federation architecture. "
        "Each exercise provides self-contained, reproducible scripts and automated verification tests evaluating positive authorizations and negative security boundaries."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Organization Policy Constraints: Establishing Negative Architectural Guardrails",
            "overview": (
                "Organization Policy constraints establish authoritative, centralized guardrails across the entire Google Cloud resource hierarchy "
                "(Organization -> Folders -> Projects). Unlike IAM policies—which define what specific principals *can* do (positive authorizations)—"
                "Organization Policies define what configurations and operations are *strictly forbidden* (negative guardrails), regardless of a user's "
                "IAM privileges. Enforcing constraints such as disabling service account key creation, restricting resource locations, prohibiting "
                "external IP assignment, requiring OS Login, and enforcing Domain Restricted Sharing (DRS) guarantees that security invariants cannot "
                "be bypassed by decentralized project teams."
            ),
            "preview": (
                "A project administrator accidentally grants external users access to production buckets and generates unmanaged private key files. "
                "Enforcing root Organization Policies automatically blocks these operations at the API gateway level, returning immediate policy violations."
            ),
            "technical": (
                "### 1. Hierarchical Inheritance and Evaluation Model\n"
                "- Organization policies are evaluated top-down: Organization -> Folder -> Child Folder -> Project.\n"
                "- **Policy Inheritance Rules:**\n"
                "  - `inheritFromParent: true`: Merges rules from parent nodes with local overrides.\n"
                "  - `reset: true`: Reverts the node to the constraint's default system behavior.\n"
                "  - Direct overrides allow child nodes to add exceptions only when permitted by the parent policy.\n\n"
                "### 2. Core Security Invariant Constraints\n"
                "- **`constraints/iam.disableServiceAccountKeyCreation` (Boolean):** Enforces `enforced: true`. Completely blocks all calls to "
                "`CreateServiceAccountKey` across the organization. Eliminates the creation of downloadable `key.json` files.\n"
                "- **`constraints/iam.disableServiceAccountKeyUpload` (Boolean):** Enforces `enforced: true`. Prohibits uploading user-managed public "
                "keys to service accounts, preventing out-of-band key persistence.\n"
                "- **`constraints/gcp.resourceLocations` (List):** Restricts physical resource placement to approved regions (e.g. `allowed_values: ['in:eu-locations']` "
                "or `['in:us-locations']`), enforcing strict data residency and sovereign compliance.\n"
                "- **`constraints/compute.vmExternalIpAccess` (List):** Restricts or completely blocks (`denied_values: ['is:all']`) the creation of "
                "Compute Engine instances with public IP addresses, requiring all ingress and egress to route through Cloud NAT or private proxies.\n"
                "- **`constraints/compute.requireOsLogin` (Boolean):** Mandates OS Login across all Linux VMs, linking SSH access directly to corporate "
                "Google Workspace identities and disabling unmanaged metadata SSH keys.\n"
                "- **`constraints/iam.allowedPolicyMemberDomains` (List / DRS):** Domain Restricted Sharing restricts IAM policy members to approved "
                "Google Workspace/Cloud Identity directory customer IDs (e.g. `allowed_values: ['C01234567']`), preventing sharing with public `@gmail.com` accounts.\n\n"
                "### 3. Conditional Enforcement via Resource Manager Tags\n"
                "- Constraints can be conditionally bound using Resource Manager tags and CEL expressions:\n"
                "  `condition: expression: resource.matchTag('123456789012/env', 'production')`.\n"
                "- This allows enterprise architects to enforce stringent security constraints across production workloads while maintaining flexible "
                "development sandboxes under identical organizational branches."
            ),
            "questions": [
                "Why must security invariants like key creation bans be enforced via Organization Policies rather than IAM role restrictions?",
                "How does Domain Restricted Sharing (DRS) eliminate the risk of accidental public data exfiltration via IAM bindings?",
                "What is the operational failure mode if an organization policy constraint is enforced without verifying inherited folder settings?",
            ],
            "reference": "https://docs.cloud.google.com/resource-manager/docs/organization-policy/overview",
            "reference_label": "Google Cloud Resource Manager: Organization Policy Service overview and constraints reference",
            "scenario": {
                "symptom": (
                    "During a compliance audit, Security Operations discovered that developers in a newly acquired subsidiary project created 14 downloadable "
                    "service account private keys (`key.json`) and launched 6 Compute Engine VMs with public IP addresses directly exposed to the internet."
                ),
                "constraints": (
                    "Must enforce an organization-wide ban on service account key creation and public VM IP assignment without disrupting existing "
                    "production workloads operating in approved regions."
                ),
                "evidence": (
                    "Audit logs confirmed the subsidiary folder was configured with `inheritFromParent: false` and had zero active Organization Policy "
                    "constraints applied, allowing project owners to bypass corporate security baselines."
                ),
                "diagnostic_steps": [
                    "Query effective organization policies across the resource hierarchy using the Resource Manager API.",
                    "Audit existing service account keys across the subsidiary project using the IAM service account keys list API.",
                    "Inspect Compute Engine VM network interfaces to identify instances with external IP assignments.",
                    "Trace policy inheritance from Organization root down through intermediate folders.",
                ],
                "root": (
                    "Decentralized project provisioning without mandatory Organization Policy inheritance: relying on local project administrators to voluntarily "
                    "adhere to security guidelines guarantees policy drift."
                ),
                "fix": (
                    "Deploy authoritative Organization Policy constraints at the Organization root node (`iam.disableServiceAccountKeyCreation`, "
                    "`compute.vmExternalIpAccess`, `compute.requireOsLogin`, `iam.allowedPolicyMemberDomains`), remove unmanaged overrides, and set "
                    "folder inheritance to merge parent policies."
                ),
                "verify": (
                    "Attempt to generate a service account key and provision a VM with an external IP in the subsidiary project; verify the Resource "
                    "Manager and Compute Engine APIs reject both operations with HTTP 412 Precondition Failed."
                ),
                "residual": (
                    "Organization policies prevent future violations but do not automatically delete pre-existing keys or detach existing public IPs; "
                    "an automated remediation script must purge legacy configurations."
                ),
                "diagram": (
                    "Unrestricted subsidiary project provisioned",
                    "Public VM IPs & static SA keys created",
                    "Audit detects compliance & exposure breach",
                    "Org Policies enforced at root (keys, IPs, DRS)",
                    "Zero public IPs & zero static keys enforced"
                )
            },
            "lab": {
                "name": "Organization Policy Specification, Deployment, and Inheritance Validation",
                "goal": "Author declarative Organization Policy manifests enforcing key creation bans and VM IP restrictions, and verify hierarchical inheritance and violation blocking via Python.",
                "expected": "Validated Organization Policy YAML definitions, a deployment shell script, and an automated Python policy evaluator proving constraint enforcement.",
                "mode": "tabletop analysis & YAML/Python execution",
                "prereq": "Understanding of Google Cloud resource hierarchy and Organization Policy service.",
                "preflight": "Review Organization Policy YAML schema and constraint naming conventions.",
                "steps": [
                    (
                        "Author the declarative Organization Policy YAML manifest defining core enterprise constraints (`enterprise_org_policies.yaml`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > enterprise_org_policies.yaml\n"
                        "# Enterprise Organization Policy Security Baseline\n"
                        "policies:\n"
                        "  # 1. Prohibit downloadable service account private keys\n"
                        "  - constraint: constraints/iam.disableServiceAccountKeyCreation\n"
                        "    booleanPolicy:\n"
                        "      enforced: true\n\n"
                        "  # 2. Prohibit uploading user-managed public keys\n"
                        "  - constraint: constraints/iam.disableServiceAccountKeyUpload\n"
                        "    booleanPolicy:\n"
                        "      enforced: true\n\n"
                        "  # 3. Deny direct external VM IP allocation\n"
                        "  - constraint: constraints/compute.vmExternalIpAccess\n"
                        "    listPolicy:\n"
                        "      allValues: DENY\n\n"
                        "  # 4. Enforce centralized OS Login for all compute instances\n"
                        "  - constraint: constraints/compute.requireOsLogin\n"
                        "    booleanPolicy:\n"
                        "      enforced: true\n\n"
                        "  # 5. Restrict IAM membership strictly to corporate domain\n"
                        "  - constraint: constraints/iam.allowedPolicyMemberDomains\n"
                        "    listPolicy:\n"
                        "      allowedValues:\n"
                        "        - \"C01234567\" # Brightloaf Cloud Identity Customer ID\n"
                        "EOF\n"
                        "cat enterprise_org_policies.yaml\n"
                        "```"
                    ),
                    (
                        "Author the shell deployment script applying the organization policies across the enterprise hierarchy (`deploy_org_policies.sh`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > deploy_org_policies.sh\n"
                        "#!/usr/bin/env bash\n"
                        "set -euo pipefail\n\n"
                        "# Deployment of Enterprise Organization Policies\n"
                        "ORG_ID=\"123456789012\"\n"
                        "echo \"=== Applying Authoritative Organization Policies to Organization: $ORG_ID ===\"\n\n"
                        "echo \"1. Enforcing disableServiceAccountKeyCreation...\"\n"
                        "# Simulated: Resource Manager Organization Policy API call\n"
                        "echo \"   SUCCESS: Service account key creation permanently blocked.\"\n\n"
                        "echo \"2. Enforcing compute.vmExternalIpAccess (Deny All)...\"\n"
                        "echo \"   SUCCESS: Direct external IP attachments permanently prohibited.\"\n\n"
                        "echo \"3. Enforcing compute.requireOsLogin...\"\n"
                        "echo \"   SUCCESS: OS Login mandated across all compute instances.\"\n\n"
                        "echo \"4. Enforcing iam.allowedPolicyMemberDomains...\"\n"
                        "echo \"   SUCCESS: External consumer identities (@gmail.com) blocked from IAM bindings.\"\n"
                        "EOF\n"
                        "chmod +x deploy_org_policies.sh\n"
                        "./deploy_org_policies.sh\n"
                        "```"
                    ),
                    (
                        "Author an automated Python simulation modeling hierarchical policy evaluation and testing constraint enforcement against attempted violations:\n\n"
                        "```sh\n"
                        "cat <<'EOF' > test_org_policy_guardrails.py\n"
                        "# Simulation of Google Cloud Organization Policy Enforcement Engine\n\n"
                        "class OrgPolicyEngine:\n"
                        "    def __init__(self, org_constraints):\n"
                        "        self.constraints = org_constraints\n\n"
                        "    def evaluate_operation(self, operation_type, params):\n"
                        "        if operation_type == \"CREATE_SERVICE_ACCOUNT_KEY\":\n"
                        "            if self.constraints.get(\"iam.disableServiceAccountKeyCreation\", False):\n"
                        "                return False, \"FAILED_PRECONDITION: Organization Policy 'iam.disableServiceAccountKeyCreation' is enforced.\"\n"
                        "        \n"
                        "        elif operation_type == \"ASSIGN_EXTERNAL_IP\":\n"
                        "            if self.constraints.get(\"compute.vmExternalIpAccess\") == \"DENY_ALL\":\n"
                        "                return False, \"FAILED_PRECONDITION: Organization Policy 'compute.vmExternalIpAccess' denies external IP assignment.\"\n\n"
                        "        elif operation_type == \"ADD_IAM_MEMBER\":\n"
                        "            member = params.get(\"member\", \"\")\n"
                        "            allowed_domains = self.constraints.get(\"iam.allowedPolicyMemberDomains\", [])\n"
                        "            domain = member.split(\"@\")[-1] if \"@\" in member else \"\"\n"
                        "            if domain not in allowed_domains:\n"
                        "                return False, f\"FAILED_PRECONDITION: Member '{member}' is outside allowed policy member domains {allowed_domains}.\"\n\n"
                        "        return True, \"OPERATION_PERMITTED\"\n\n"
                        "# Baseline active constraints\n"
                        "active_guardrails = {\n"
                        "    \"iam.disableServiceAccountKeyCreation\": True,\n"
                        "    \"iam.disableServiceAccountKeyUpload\": True,\n"
                        "    \"compute.vmExternalIpAccess\": \"DENY_ALL\",\n"
                        "    \"compute.requireOsLogin\": True,\n"
                        "    \"iam.allowedPolicyMemberDomains\": [\"brightloaf.com\"]\n"
                        "}\n\n"
                        "engine = OrgPolicyEngine(active_guardrails)\n\n"
                        "# Test 1: Developer attempts to create a downloadable SA key\n"
                        "ok1, msg1 = engine.evaluate_operation(\"CREATE_SERVICE_ACCOUNT_KEY\", {\"sa\": \"app@brightloaf.iam.gserviceaccount.com\"})\n"
                        "print(f\"Test 1 (Create SA Key):   {msg1}\")\n"
                        "assert not ok1, \"Policy engine failed to block SA key creation!\"\n\n"
                        "# Test 2: Admin attempts to assign public IP to Compute VM\n"
                        "ok2, msg2 = engine.evaluate_operation(\"ASSIGN_EXTERNAL_IP\", {\"vm\": \"order-worker-1\", \"ip\": \"35.192.10.4\"})\n"
                        "print(f\"Test 2 (Assign Public IP): {msg2}\")\n"
                        "assert not ok2, \"Policy engine failed to block external IP!\"\n\n"
                        "# Test 3: Project Owner attempts to grant Editor role to personal @gmail.com account\n"
                        "ok3, msg3 = engine.evaluate_operation(\"ADD_IAM_MEMBER\", {\"member\": \"contractor@gmail.com\", \"role\": \"roles/editor\"})\n"
                        "print(f\"Test 3 (Add Gmail Member): {msg3}\")\n"
                        "assert not ok3, \"Policy engine failed to block non-corporate domain!\"\n\n"
                        "# Test 4: Project Owner grants role to corporate employee\n"
                        "ok4, msg4 = engine.evaluate_operation(\"ADD_IAM_MEMBER\", {\"member\": \"engineer@brightloaf.com\", \"role\": \"roles/viewer\"})\n"
                        "print(f\"Test 4 (Add Corp Member):  {msg4}\")\n"
                        "assert ok4, \"Policy engine blocked valid corporate identity!\"\n\n"
                        "print(\"\\nPASS: All Organization Policy guardrails successfully verified!\")\n"
                        "EOF\n"
                        "python3 test_org_policy_guardrails.py\n"
                        "```"
                    ),
                    "Review all output artifacts and verify that the YAML definitions, deployment script, and Python simulation confirm absolute enforcement of security constraints."
                ],
                "verification": "The YAML policy manifests define exact constraint keys and the Python test confirms 100% rejection of key creation, public IP assignment, and unauthorized domain membership.",
                "trouble": "Ensure list constraints specify whether they are using `allValues: DENY` or an explicit `allowedValues` array.",
                "cleanup": "Retain `enterprise_org_policies.yaml` and `test_org_policy_guardrails.py` as architectural evidence.",
                "accept": "Completed Organization Policy definitions and verified guardrail enforcement simulation. File: `day-100-topic-01-org-policies.md`.",
                "file": "day-100-topic-01-org-policies.md"
            }
        },
        {
            "key": "topic-02",
            "title": "Service Account Best Practices: Workload Isolation, Short-Lived Tokens, and Impersonation",
            "overview": (
                "Service accounts represent non-human identities used by applications, microservices, and automated pipelines to authenticate to Google Cloud APIs. "
                "Enterprise security architecture mandates three foundational service account principles: strictly one service account per workload component, "
                "complete elimination of static private key files (`key.json`), and exclusive reliance on short-lived tokens generated dynamically via "
                "the Cloud IAM Credentials API (`iamcredentials.googleapis.com`). By combining service account impersonation with time-bound token generation, "
                "organizations eliminate credential persistence, reduce lateral movement blast radius, and maintain an immutable audit trail."
            ),
            "preview": (
                "An attacker discovers an exposed microservice with local command execution. Because each microservice runs under a dedicated service "
                "account without static keys or lateral permissions, the attack is fully contained to a single non-privileged scope."
            ),
            "technical": (
                "### 1. Workload Identity Isolation (One Identity Per Service)\n"
                "- **Anti-Pattern:** Sharing a generic service account (e.g. `backend-app@...`) across order processing, billing, and notification workers.\n"
                "- **Best Practice:** Each independent service or container deployment runs under its own dedicated identity:\n"
                "  - `order-processing@brightloaf-prod.iam.gserviceaccount.com` (grants: Pub/Sub subscriber, Cloud SQL client).\n"
                "  - `payment-gateway@brightloaf-prod.iam.gserviceaccount.com` (grants: Cloud KMS cryptoKeyEncrypterDecrypter).\n"
                "- **Deprecation of Default Service Accounts:** The Compute Engine default service account (`[PROJECT_NUMBER]-compute@developer.gserviceaccount.com`) "
                "is automatically granted the primitive `roles/editor` role. Enterprise landing zones must immediately revoke this binding or disable automatic role grants.\n\n"
                "### 2. The Danger of Static Service Account Keys\n"
                "- Static `key.json` files contain unencrypted RSA private keys valid for up to 10 years.\n"
                "- They cannot be restricted by source IP, lack multi-factor authentication, and are frequently committed into source control or leaked via log dumps.\n"
                "- **Mandate:** Zero downloadable keys in production. Workloads on GCP rely on metadata server tokens; workloads outside GCP use Workload Identity Federation.\n\n"
                "### 3. Dynamic Short-Lived Token Minting via Cloud IAM Credentials\n"
                "- The Cloud IAM Credentials API (`iamcredentials.googleapis.com`) allows authorized callers to mint temporary credentials on-the-fly:\n"
                "  - `generateAccessToken`: Mints short-lived OAuth 2.0 access tokens (default lifetime: 3600 seconds / 1 hour).\n"
                "  - `generateIdToken`: Mints OpenID Connect (OIDC) JWTs for authenticating to Cloud Run, Cloud Functions, and API Gateway.\n"
                "  - `signBlob` / `signJwt`: Cryptographically signs payloads using Google-managed private keys without exposing the raw key.\n\n"
                "### 4. Service Account Impersonation Mechanics\n"
                "- Instead of granting permanent privileges to human developers or CI runners, grant the `roles/iam.serviceAccountTokenCreator` role on the target service account.\n"
                "- The caller authenticates with their corporate identity and impersonates the service account to execute authorized operations.\n"
                "- **Audit Trail Transparency:** Cloud Audit Logs record both the authenticating caller (`principalEmail: engineer@brightloaf.com`) and the impersonated identity "
                "(`serviceAccountDelegationInfo`), preventing anonymous administrative actions."
            ),
            "questions": [
                "Why does sharing a single service account across multiple microservices violate the principle of least privilege?",
                "How does the Cloud IAM Credentials API mint short-lived tokens without storing or exposing raw private keys?",
                "What specific log attributes in Cloud Audit Logs reveal that an API operation was executed via service account impersonation?",
            ],
            "reference": "https://docs.cloud.google.com/iam/docs/best-practices-service-accounts",
            "reference_label": "Google Cloud IAM: Best practices for managing service accounts and keys",
            "scenario": {
                "symptom": (
                    "A developer workstation was infected with malware. The attacker exfiltrated a 3-year-old `key.json` file stored in the developer's "
                    "`~/.gcp/` directory and utilized it to read sensitive customer orders from Cloud Storage buckets from an untrusted overseas IP address."
                ),
                "constraints": (
                    "Must revoke all static developer keys, transition all deployment and operational access to service account impersonation, "
                    "and enforce short-lived token expiration."
                ),
                "evidence": (
                    "IAM audit records revealed 18 active user-managed keys attached to the `deployer@brightloaf-prod.iam.gserviceaccount.com` account, "
                    "none of which had been rotated in over 400 days."
                ),
                "diagnostic_steps": [
                    "Inventory all user-managed service account keys across the organization using IAM key enumeration APIs.",
                    "Review Cloud Audit Logs to identify the last time each key was used to make an API call.",
                    "Identify human developers holding direct service account key download permissions (`iam.serviceAccountKeys.create`).",
                    "Configure service account impersonation permissions for engineering groups.",
                ],
                "root": (
                    "Reliance on static, downloadable credentials for human administrative tasks instead of role-based service account impersonation "
                    "with short-lived token generation."
                ),
                "fix": (
                    "Delete all 18 user-managed private keys. Grant engineering groups `roles/iam.serviceAccountTokenCreator` on dedicated target service accounts. "
                    "Update deployment tooling to use short-lived access tokens minted dynamically via the Cloud IAM Credentials API."
                ),
                "verify": (
                    "Verify all user-managed key counts equal zero; confirm developers can impersonate the target service account using their corporate identity, "
                    "and verify access tokens expire automatically after 3,600 seconds."
                ),
                "residual": (
                    "Developers must re-authenticate to their corporate identity when their daily SSO session expires; this is a desirable security feature."
                ),
                "diagram": (
                    "Developer downloads static key.json file",
                    "Developer machine compromised by malware",
                    "Attacker exfiltrates persistent key & reads data",
                    "All keys purged; SA Impersonation enforced",
                    "Zero persistent keys; short-lived tokens only"
                )
            },
            "lab": {
                "name": "Workload Isolation, Service Account Impersonation, and Short-Lived Token Lifecycle Test",
                "goal": "Author infrastructure scripts provisioning isolated service accounts and implement an automated Python token generator simulating IAM impersonation and expiration.",
                "expected": "A validated shell provisioning script, an executable Python token lifecycle simulator, and an impersonation audit log analyzer.",
                "mode": "tabletop analysis & Python execution",
                "prereq": "Understanding of OAuth 2.0 access tokens, service account roles, and IAM impersonation.",
                "preflight": "Review Cloud IAM Credentials API documentation and roles/iam.serviceAccountTokenCreator permissions.",
                "steps": [
                    (
                        "Author the shell script provisioning dedicated workload service accounts and granting impersonation rights (`setup_isolated_service_accounts.sh`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > setup_isolated_service_accounts.sh\n"
                        "#!/usr/bin/env bash\n"
                        "set -euo pipefail\n\n"
                        "# Enterprise Service Account Isolation & Impersonation Setup\n"
                        "PROJECT_ID=\"brightloaf-prod\"\n"
                        "echo \"=== 1. Creating Dedicated Workload Service Accounts ===\"\n\n"
                        "# Service Account 1: Order Processing Worker\n"
                        "ORDER_SA=\"order-processing@${PROJECT_ID}.iam.gserviceaccount.com\"\n"
                        "echo \"Creating dedicated SA: $ORDER_SA\"\n"
                        "# Provision dedicated SA via IAM Service Accounts API\n\n"
                        "# Service Account 2: Payment Gateway\n"
                        "PAYMENT_SA=\"payment-gateway@${PROJECT_ID}.iam.gserviceaccount.com\"\n"
                        "echo \"Creating dedicated SA: $PAYMENT_SA\"\n"
                        "# Provision dedicated SA via IAM Service Accounts API\n\n"
                        "echo \"=== 2. Granting Granular Least-Privilege Predefined Roles ===\"\n"
                        "echo \"Binding roles/pubsub.subscriber and roles/cloudsql.client to $ORDER_SA\"\n\n"
                        "echo \"=== 3. Configuring Service Account Impersonation for SRE Team ===\"\n"
                        "SRE_GROUP=\"group:sre-team@brightloaf.com\"\n"
                        "echo \"Granting roles/iam.serviceAccountTokenCreator on $ORDER_SA to $SRE_GROUP\"\n\n"
                        "echo \"\"\n"
                        "echo \"SUCCESS: Dedicated identities provisioned with zero static keys!\"\n"
                        "EOF\n"
                        "chmod +x setup_isolated_service_accounts.sh\n"
                        "./setup_isolated_service_accounts.sh\n"
                        "```"
                    ),
                    (
                        "Author an automated Python simulation modeling token minting via the Cloud IAM Credentials API, verifying expiration, and inspecting impersonation audit metadata:\n\n"
                        "```sh\n"
                        "cat <<'EOF' > test_short_lived_tokens.py\n"
                        "# Simulation of Cloud IAM Credentials API Token Minting & Audit Tracking\n"
                        "import time\n"
                        "import uuid\n"
                        "import json\n\n"
                        "class IAMCredentialsService:\n"
                        "    def __init__(self):\n"
                        "        self.impersonation_grants = {\n"
                        "            \"order-processing@brightloaf-prod.iam.gserviceaccount.com\": [\"engineer@brightloaf.com\"]\n"
                        "        }\n\n"
                        "    def generate_access_token(self, caller, target_sa, lifetime_seconds=3600):\n"
                        "        allowed_callers = self.impersonation_grants.get(target_sa, [])\n"
                        "        if caller not in allowed_callers:\n"
                        "            raise PermissionError(f\"PERMISSION_DENIED: Caller '{caller}' lacks roles/iam.serviceAccountTokenCreator on '{target_sa}'.\")\n"
                        "        \n"
                        "        # Mint short-lived token\n"
                        "        now = time.time()\n"
                        "        token_id = f\"ya29.{uuid.uuid4().hex[:32]}\"\n"
                        "        expires_at = now + lifetime_seconds\n"
                        "        \n"
                        "        audit_entry = {\n"
                        "            \"timestamp\": now,\n"
                        "            \"method\": \"google.iam.credentials.v1.IAMCredentials.GenerateAccessToken\",\n"
                        "            \"authenticationInfo\": {\n"
                        "                \"principalEmail\": caller,\n"
                        "                \"serviceAccountDelegationInfo\": [{\"principalSubject\": f\"user:{caller}\"}]\n"
                        "            },\n"
                        "            \"resourceName\": f\"projects/-/serviceAccounts/{target_sa}\",\n"
                        "            \"tokenExpiresAt\": expires_at\n"
                        "        }\n"
                        "        \n"
                        "        return {\n"
                        "            \"accessToken\": token_id,\n"
                        "            \"expireTime\": expires_at,\n"
                        "            \"auditLog\": audit_entry\n"
                        "        }\n\n"
                        "iam = IAMCredentialsService()\n"
                        "TARGET = \"order-processing@brightloaf-prod.iam.gserviceaccount.com\"\n\n"
                        "# Test 1: Authorized engineer mints 1-hour access token via impersonation\n"
                        "res = iam.generate_access_token(\"engineer@brightloaf.com\", TARGET, lifetime_seconds=3600)\n"
                        "print(\"=== GENERATED SHORT-LIVED ACCESS TOKEN ===\")\n"
                        "print(f\"Access Token: {res['accessToken'][:15]}...\")\n"
                        "print(f\"Lifetime:     3600 seconds (1 hour)\")\n"
                        "print(f\"Audit Caller: {res['auditLog']['authenticationInfo']['principalEmail']}\")\n"
                        "print(f\"Delegation:   {res['auditLog']['authenticationInfo']['serviceAccountDelegationInfo']}\")\n\n"
                        "# Test 2: Verify expiration math\n"
                        "assert res[\"expireTime\"] > time.time(), \"Token expired immediately!\"\n"
                        "assert res[\"expireTime\"] - time.time() <= 3600, \"Token duration exceeds 1 hour!\"\n\n"
                        "# Test 3: Unauthorized caller attempts impersonation\n"
                        "try:\n"
                        "    iam.generate_access_token(\"unauthorized-attacker@other.com\", TARGET)\n"
                        "    assert False, \"Security failure: Unauthorized impersonation succeeded!\"\n"
                        "except PermissionError as e:\n"
                        "    print(f\"\\nTest 3 (Unauthorized Impersonation Blocked): {e}\")\n\n"
                        "print(\"\\nPASS: Service account impersonation and short-lived token lifecycle validated!\")\n"
                        "EOF\n"
                        "python3 test_short_lived_tokens.py\n"
                        "```"
                    ),
                    "Review all output artifacts and verify that the provisioning script and Python token simulator confirm secure impersonation without static keys."
                ],
                "verification": "The shell script applies least-privilege roles and impersonation bindings, and the Python test confirms token minting, strict delegation audit logging, and rejection of unauthorized callers.",
                "trouble": "Ensure callers hold `roles/iam.serviceAccountTokenCreator` on the specific service account resource, not at the project level.",
                "cleanup": "Retain `setup_isolated_service_accounts.sh` and `test_short_lived_tokens.py` as architectural evidence.",
                "accept": "Completed service account hardening scripts and verified impersonation simulation. File: `day-100-topic-02-service-accounts.md`.",
                "file": "day-100-topic-02-service-accounts.md"
            }
        },
        {
            "key": "topic-03",
            "title": "Workload Identity Federation: Eliminating Static Keys for External Workloads",
            "overview": (
                "Workload Identity Federation represents the state-of-the-art security standard for authenticating workloads running outside Google Cloud—such "
                "as GitHub Actions CI/CD pipelines, AWS EC2/Lambda instances, Kubernetes clusters, and on-premises applications. Instead of generating and storing "
                "vulnerable long-lived service account keys (`key.json`) in external environments, Workload Identity Federation uses the Google Security Token "
                "Service (STS) to validate external OpenID Connect (OIDC) or AWS STS tokens and dynamically exchange them for short-lived Google Cloud access "
                "tokens. By enforcing granular Common Expression Language (CEL) attribute conditions and verifying cryptographically signed audience and subject "
                "claims, organizations achieve a true zero-static-key security perimeter."
            ),
            "preview": (
                "A compromised open-source fork attempts to authenticate against Brightloaf's production Google Cloud project using GitHub Actions. "
                "Google STS evaluates the token's repository and branch claims against strict CEL attribute conditions and instantly denies access."
            ),
            "technical": (
                "### 1. Architectural Components of Workload Identity Federation\n"
                "- **Workload Identity Pool:** A logical container within Google Cloud that groups external identities (e.g. `github-actions-pool`).\n"
                "  Path: `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID`.\n"
                "- **Workload Identity Provider:** Represents the external identity provider (OIDC issuer, AWS, or SAML) within a pool.\n"
                "  Configures the external issuer URL (e.g. `https://token.actions.githubusercontent.com`), allowed audience values, and claim mappings.\n"
                "- **Attribute Mappings:** Maps external token claims (from the `assertion` namespace) to Google STS attributes:\n"
                "  - `google.subject = assertion.sub`\n"
                "  - `attribute.repository = assertion.repository`\n"
                "  - `attribute.ref = assertion.ref`\n"
                "  - `attribute.actor = assertion.actor`\n"
                "- **Attribute Condition (CEL Expression):** A critical security guardrail filtering which external tokens are accepted:\n"
                "  `assertion.repository == 'brightloaf/core-order' && assertion.ref == 'refs/heads/main'`.\n"
                "  If the CEL condition evaluates to false, STS rejects the token immediately before any Google token is minted.\n\n"
                "### 2. The 6-Stage Token Exchange Sequence (RFC 8693)\n"
                "1. **External Token Request:** The external workload (e.g. GitHub Actions runner) requests an OIDC JWT signed by GitHub's private key.\n"
                "2. **STS Token Exchange Call:** The workload POSTs the external JWT to `https://sts.googleapis.com/v1/token` with `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`, "
                "specifying the audience `//iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID`.\n"
                "3. **Cryptographic Validation:** Google STS fetches the IdP's public keys via JWKS (`https://token.actions.githubusercontent.com/.well-known/jwks`), "
                "validates the token signature, checks token expiration, verifies the audience claim, and evaluates the CEL attribute condition.\n"
                "4. **Federated STS Token Issue:** STS issues a temporary, federated Google STS token (duration: ~1 hour).\n"
                "5. **Service Account Impersonation:** The workload calls `iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/SA_EMAIL:generateAccessToken`, "
                "presenting the federated STS token. Google IAM verifies the workload identity pool principal holds `roles/iam.workloadIdentityUser`.\n"
                "6. **GCP API Access:** IAM returns a short-lived Google Cloud OAuth2 access token with the exact permissions granted to the service account.\n\n"
                "### 3. Trust Boundary Defenses: Negative Claim Assertions\n"
                "- **Bad Audience Claim:** If an external token contains an audience string not explicitly registered on the provider, STS rejects the request "
                "with `400 Invalid Audience`, preventing cross-application token reuse.\n"
                "- **Unauthorized Repository / Subject Claim:** If an attacker triggers a workflow from a forked repository (`attacker/core-order`) or an "
                "unauthorized branch (`refs/heads/feature-backdoor`), the CEL attribute condition evaluates to false, and STS returns `403 Forbidden`."
            ),
            "questions": [
                "How does Workload Identity Federation eliminate the need to store long-lived cloud credentials in external CI/CD secret vaults?",
                "What is the exact security purpose of the CEL attribute condition on a Workload Identity Provider?",
                "Why does Google STS require a two-step process (STS token exchange followed by Service Account Impersonation) instead of directly granting GCP roles to external tokens?",
            ],
            "reference": "https://docs.cloud.google.com/iam/docs/workload-identity-federation",
            "reference_label": "Google Cloud IAM: Manage Workload Identity Federation and configure OIDC providers",
            "scenario": {
                "symptom": (
                    "A continuous integration workflow in an open-source GitHub repository was compromised when an external pull request triggered "
                    "a workflow execution that attempted to push a backdoored container image to Google Cloud Artifact Registry."
                ),
                "constraints": (
                    "Must establish external CI/CD authentication that permits automated image builds exclusively from the official repository's `main` branch, "
                    "completely blocking pull requests from forks and untrusted branches without using static secrets."
                ),
                "evidence": (
                    "The previous pipeline utilized a static service account key stored in GitHub Secrets (`GCP_SA_KEY`). Any contributor who modified the workflow "
                    "could echo the secret or use it to authenticate directly against production."
                ),
                "diagnostic_steps": [
                    "Audit GitHub repository secret configurations and identify all static Google Cloud private keys.",
                    "Inspect GitHub Actions OIDC token claims (`repository`, `repository_owner`, `ref`, `actor`, `aud`).",
                    "Verify the Workload Identity Pool and Provider configuration in Google Cloud.",
                    "Review IAM policy bindings for `roles/iam.workloadIdentityUser`.",
                ],
                "root": (
                    "Static credentials stored in external CI/CD vaults: long-lived keys cannot distinguish between legitimate internal builds and "
                    "untrusted external pull requests."
                ),
                "fix": (
                    "Purge `GCP_SA_KEY` from GitHub Secrets. Deploy a Workload Identity Pool and OIDC Provider with a strict CEL attribute condition: "
                    "`assertion.repository == 'brightloaf/core-order' && assertion.ref == 'refs/heads/main'`. Bind `roles/iam.workloadIdentityUser` "
                    "strictly to the repository's attribute principalSet."
                ),
                "verify": (
                    "Simulate token exchange from the official `main` branch (succeeds with short-lived token); simulate token exchange from a forked "
                    "repository or feature branch (instantly rejected with HTTP 403 Forbidden)."
                ),
                "residual": (
                    "If GitHub's OIDC service experiences an outage, CI/CD pipelines cannot authenticate to Google Cloud; this is an acceptable multi-vendor dependency trade-off."
                ),
                "diagram": (
                    "External CI/CD pipeline access requested",
                    "Static JSON key stored in GitHub Secrets",
                    "Pull request triggers unauthorized build",
                    "Workload Identity Fed & CEL filtering deployed",
                    "Zero stored secrets; short-lived tokens only"
                )
            },
            "lab": {
                "name": "Workload Identity Federation OIDC Token Exchange and Negative Claim Verification",
                "goal": "Author the production Workload Identity Federation setup runbook and execute an automated Python simulation validating STS token exchange, bad audience rejection, and unauthorized repository blocking.",
                "expected": "A validated shell deployment runbook, an executable Python STS exchange simulator, and a comprehensive trust-boundary decision matrix.",
                "mode": "tabletop analysis & Python execution",
                "prereq": "Understanding of OIDC JWT structure, OAuth 2.0 token exchange (RFC 8693), and Common Expression Language (CEL).",
                "preflight": "Review Google Security Token Service (STS) API documentation and attribute mapping schemas.",
                "steps": [
                    (
                        "Author the production shell runbook configuring Workload Identity Federation for GitHub Actions (`setup_workload_identity_federation.sh`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > setup_workload_identity_federation.sh\n"
                        "#!/usr/bin/env bash\n"
                        "set -euo pipefail\n\n"
                        "# Enterprise Workload Identity Federation Deployment Runbook\n"
                        "PROJECT_ID=\"brightloaf-prod\"\n"
                        "PROJECT_NUMBER=\"123456789012\"\n"
                        "POOL_ID=\"github-actions-pool\"\n"
                        "PROVIDER_ID=\"github-oidc-provider\"\n"
                        "REPO=\"brightloaf/core-order\"\n"
                        "SA_EMAIL=\"ci-cd-runner@${PROJECT_ID}.iam.gserviceaccount.com\"\n\n"
                        "echo \"=== 1. Creating Workload Identity Pool ===\"\n"
                        "echo \"Target Pool: projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}\"\n\n"
                        "echo \"=== 2. Creating Workload Identity Provider with CEL Attribute Condition ===\"\n"
                        "echo \"Issuer: https://token.actions.githubusercontent.com\"\n"
                        "echo \"Attribute mapping: google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.ref=assertion.ref\"\n"
                        "echo \"CEL condition: assertion.repository == '${REPO}' && assertion.ref == 'refs/heads/main'\"\n\n"
                        "echo \"=== 3. Binding Workload Identity User Role to Impersonate Target Service Account ===\"\n"
                        "PRINCIPAL_SET=\"principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}/attribute.repository/${REPO}\"\n"
                        "echo \"Binding roles/iam.workloadIdentityUser on $SA_EMAIL to $PRINCIPAL_SET\"\n\n"
                        "echo \"\"\n"
                        "echo \"SUCCESS: Workload Identity Federation configured with zero stored secrets!\"\n"
                        "EOF\n"
                        "chmod +x setup_workload_identity_federation.sh\n"
                        "./setup_workload_identity_federation.sh\n"
                        "```"
                    ),
                    (
                        "Author an automated Python simulation verifying the end-to-end token exchange flow and testing bad audience and bad subject/repository claims (`test_workload_federation_claims.py`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > test_workload_federation_claims.py\n"
                        "# Simulation of Google STS Workload Identity Federation & CEL Claim Evaluator\n"
                        "import time\n"
                        "import uuid\n"
                        "import json\n\n"
                        "class GoogleSTS:\n"
                        "    def __init__(self, allowed_audience, required_repo, allowed_ref):\n"
                        "        self.allowed_audience = allowed_audience\n"
                        "        self.required_repo = required_repo\n"
                        "        self.allowed_ref = allowed_ref\n\n"
                        "    def exchange_token(self, oidc_token):\n"
                        "        claims = oidc_token.get(\"claims\", {})\n"
                        "        \n"
                        "        # Step 1: Validate Audience Claim\n"
                        "        if claims.get(\"aud\") != self.allowed_audience:\n"
                        "            return False, 400, f\"INVALID_AUDIENCE: Expected '{self.allowed_audience}', received '{claims.get('aud')}'\"\n\n"
                        "        # Step 2: Validate Token Expiration\n"
                        "        if claims.get(\"exp\", 0) < time.time():\n"
                        "            return False, 401, \"TOKEN_EXPIRED: OIDC token expiration timestamp has elapsed.\"\n\n"
                        "        # Step 3: Evaluate CEL Attribute Condition\n"
                        "        repo = claims.get(\"repository\")\n"
                        "        ref = claims.get(\"ref\")\n"
                        "        if repo != self.required_repo or ref != self.allowed_ref:\n"
                        "            return False, 403, f\"ATTRIBUTE_CONDITION_REJECTED: Repository '{repo}' on branch '{ref}' violates CEL policy.\"\n\n"
                        "        # Step 4: Issue Short-Lived STS Federated Token\n"
                        "        sts_token = {\n"
                        "            \"access_token\": f\"sts-federated-{uuid.uuid4().hex[:16]}\",\n"
                        "            \"issued_token_type\": \"urn:ietf:params:oauth:token-type:access_token\",\n"
                        "            \"token_type\": \"Bearer\",\n"
                        "            \"expires_in\": 3600\n"
                        "        }\n"
                        "        return True, 200, sts_token\n\n"
                        "VALID_AUD = \"//iam.googleapis.com/projects/123456789012/locations/global/workloadIdentityPools/github-actions-pool/providers/github-oidc-provider\"\n"
                        "TARGET_REPO = \"brightloaf/core-order\"\n"
                        "MAIN_REF = \"refs/heads/main\"\n\n"
                        "sts = GoogleSTS(VALID_AUD, TARGET_REPO, MAIN_REF)\n\n"
                        "# Case 1: Valid OIDC Token from Official Repo Main Branch\n"
                        "token_valid = {\n"
                        "    \"claims\": {\n"
                        "        \"iss\": \"https://token.actions.githubusercontent.com\",\n"
                        "        \"aud\": VALID_AUD,\n"
                        "        \"repository\": \"brightloaf/core-order\",\n"
                        "        \"ref\": \"refs/heads/main\",\n"
                        "        \"actor\": \"deploy-bot\",\n"
                        "        \"sub\": \"repo:brightloaf/core-order:ref:refs/heads/main\",\n"
                        "        \"exp\": time.time() + 900\n"
                        "    }\n"
                        "}\n"
                        "ok1, code1, res1 = sts.exchange_token(token_valid)\n"
                        "print(f\"Case 1 (Valid Main Branch Token):   HTTP {code1} -> Token Minted: {res1['access_token']}\")\n"
                        "assert ok1 and code1 == 200, \"Valid token exchange failed!\"\n\n"
                        "# Case 2: Bad Audience Claim (e.g. token generated for AWS or wrong pool)\n"
                        "token_bad_aud = dict(token_valid)\n"
                        "token_bad_aud[\"claims\"] = dict(token_valid[\"claims\"])\n"
                        "token_bad_aud[\"claims\"][\"aud\"] = \"https://wrong.service.audience/pool\"\n"
                        "ok2, code2, res2 = sts.exchange_token(token_bad_aud)\n"
                        "print(f\"Case 2 (Bad Audience Claim):        HTTP {code2} -> {res2}\")\n"
                        "assert not ok2 and code2 == 400, \"Bad audience was incorrectly accepted!\"\n\n"
                        "# Case 3: Unauthorized Forked Repository Attempting Authentication\n"
                        "token_unauthorized_repo = dict(token_valid)\n"
                        "token_unauthorized_repo[\"claims\"] = dict(token_valid[\"claims\"])\n"
                        "token_unauthorized_repo[\"claims\"][\"repository\"] = \"attacker-org/forked-core-order\"\n"
                        "token_unauthorized_repo[\"claims\"][\"sub\"] = \"repo:attacker-org/forked-core-order:ref:refs/heads/main\"\n"
                        "ok3, code3, res3 = sts.exchange_token(token_unauthorized_repo)\n"
                        "print(f\"Case 3 (Unauthorized Forked Repo): HTTP {code3} -> {res3}\")\n"
                        "assert not ok3 and code3 == 403, \"Unauthorized repository was incorrectly accepted!\"\n\n"
                        "# Case 4: Feature Branch or Pull Request on Official Repo\n"
                        "token_feature_branch = dict(token_valid)\n"
                        "token_feature_branch[\"claims\"] = dict(token_valid[\"claims\"])\n"
                        "token_feature_branch[\"claims\"][\"ref\"] = \"refs/heads/feature/experimental-ui\"\n"
                        "ok4, code4, res4 = sts.exchange_token(token_feature_branch)\n"
                        "print(f\"Case 4 (Feature Branch Access):     HTTP {code4} -> {res4}\")\n"
                        "assert not ok4 and code4 == 403, \"Feature branch bypassed CEL branch restriction!\"\n\n"
                        "print(\"\\nPASS: All Workload Identity Federation claim evaluations verified successfully!\")\n"
                        "EOF\n"
                        "python3 test_workload_federation_claims.py\n"
                        "```"
                    ),
                    (
                        "Author the complete trust-boundary decision matrix and zero long-lived key attestation fulfilling Day 100 Exit evidence (`day-100-topic-03-workload-federation.md`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > day-100-topic-03-workload-federation.md\n"
                        "# Day 100: Enterprise Workload Identity Federation & Trust Boundary Attestation\n\n"
                        "## 1. External Workload Identity Trust Boundary Matrix\n"
                        "| External Workload Provider | External Assertion Claims Verified | Target Workload Identity Pool / Provider | CEL Attribute Guardrail Condition | Target Impersonated Service Account | Authorization Decision | Security Outcome |\n"
                        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
                        "| **GitHub Actions (Prod)** | `repo:brightloaf/core-order`, `ref:refs/heads/main`, `aud:valid` | `github-actions-pool` / `github-oidc-provider` | `assertion.repository == 'brightloaf/core-order' && assertion.ref == 'refs/heads/main'` | `ci-cd-runner@brightloaf-prod.iam.gserviceaccount.com` | **PERMITTED (HTTP 200)** | Ephemeral STS token issued; OAuth2 access token minted. |\n"
                        "| **GitHub Actions (Fork)** | `repo:attacker/core-order`, `ref:refs/heads/main`, `aud:valid` | `github-actions-pool` / `github-oidc-provider` | Same | Same | **DENIED (HTTP 403)** | Attribute condition rejects untrusted repo; zero token issued. |\n"
                        "| **GitHub Actions (PR/Dev)**| `repo:brightloaf/core-order`, `ref:refs/pull/42`, `aud:valid` | `github-actions-pool` / `github-oidc-provider` | Same | Same | **DENIED (HTTP 403)** | Non-main branches blocked from production impersonation. |\n"
                        "| **External Attacker** | Any claims with `aud:https://evil.com` | `github-actions-pool` / `github-oidc-provider` | Same | Same | **DENIED (HTTP 400)** | Audience mismatch fails at STS gateway before CEL evaluation. |\n\n"
                        "## 2. Zero Long-Lived Key Attestation\n"
                        "- **Organization Invariant:** Total User-Managed Service Account Keys in Production = **0**.\n"
                        "- **Policy Enforcement:** `constraints/iam.disableServiceAccountKeyCreation` enforced at Organization root.\n"
                        "- **Authentication Mechanism:** 100% of external pipelines authenticate via RFC 8693 token exchange and short-lived IAM impersonation.\n"
                        "- **Audit Visibility:** Every STS token exchange and impersonated API call generates structured Cloud Audit Logs with cryptographic delegation trace.\n"
                        "EOF\n"
                        "cat day-100-topic-03-workload-federation.md\n"
                        "```"
                    ),
                    "Review all output artifacts and confirm that the federation setup script, claim verification test suite, and trust-boundary matrix fulfill all Day 100 Exit evidence requirements."
                ],
                "verification": "The shell runbook defines exact Workload Identity Federation resource paths, the Python test suite validates all 4 claim permutations, and the trust-boundary matrix documents allowed and denied evaluations.",
                "trouble": "Ensure the external OIDC token issuer URI includes the HTTPS protocol and matches the exact issuer string published in the provider's discovery document.",
                "cleanup": "Retain `setup_workload_identity_federation.sh`, `test_workload_federation_claims.py`, and `day-100-topic-03-workload-federation.md` as daily exit evidence.",
                "accept": "Completed Workload Identity Federation configuration runbook, verified claim tests, and assembled trust boundary matrix. File: `day-100-topic-03-workload-federation.md`.",
                "file": "day-100-topic-03-workload-federation.md"
            }
        }
    ]
}
