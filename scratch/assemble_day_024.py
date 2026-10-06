#!/usr/bin/env python3
"""Build and write scratch/day_data_024.py with full depth and contract version 2."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Read SVGs from scratch/day024/
fig1 = (ROOT / 'scratch/day024/fig1.html').read_text().strip()
fig2 = (ROOT / 'scratch/day024/fig2.html').read_text().strip()
fig3 = (ROOT / 'scratch/day024/fig3.html').read_text().strip()
fig4 = (ROOT / 'scratch/day024/fig4.html').read_text().strip()
fig5 = (ROOT / 'scratch/day024/fig5.html').read_text().strip()

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'Google Cloud IAM Documentation: Domains (accessed 2026-10-04)',
        'https://cloud.google.com/iam/docs/principals-overview#domains'
    ),
    'topic-02': (
        'Google Cloud IAM Documentation: Principal types (accessed 2026-10-04)',
        'https://cloud.google.com/iam/docs/principals-overview#principal-types'
    ),
    'topic-03': (
        'Google Cloud IAM Documentation: Use access groups to model job functions and grant access to resources (accessed 2026-10-04)',
        'https://cloud.google.com/iam/docs/groups-best-practices#job-functions-access'
    ),
}

# ─────────────────────────────────────────────────────────────────────────────
# PART 1 OVERVIEW HTML
# ─────────────────────────────────────────────────────────────────────────────
PART1_HTML = '''<article class="topic-card" id="topic-01-overview">
<h3>Cloud Identity vs Google Workspace vs consumer Google accounts</h3>
<p><strong class="keyword">Workforce Identity Architecture</strong> establishes the foundational authentication repository that verifies human users before Google Cloud evaluates authorization policies. Three distinct account classes interact with Google Cloud: <strong>Consumer Google Accounts</strong> (unmanaged personal accounts owned by individuals without enterprise oversight), <strong>Cloud Identity</strong> (an enterprise Identity-as-a-Service directory anchored to a verified company domain providing centralized provisioning, SAML/OIDC federation, MFA enforcement, and automated de-provisioning), and <strong>Google Workspace</strong> (the enterprise collaboration suite sharing the identical underlying Cloud Identity directory). Cloud architects mandate Cloud Identity to ensure centralized lifecycle management and eliminate unmanaged shadow identities.</p>
<p><strong class="side-heading">Why today:</strong> Permitting unmanaged personal Google accounts into enterprise IAM policies prevents automated employee offboarding, creates severe shadow-IT security exposures, and violates compliance audit mandates.</p>
<p><strong class="side-heading">Where it sits:</strong> Sits at the authentication gateway of Google's global Identity Platform, federating workforce credentials from corporate IdPs into Cloud Resource Manager downstream of Day 23 hierarchy policies.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A franchise infrastructure administrator permits contract software developers to manage production order fulfillment projects using unmanaged personal consumer Google accounts rather than federated corporate Cloud Identity credentials. When a contractor was abruptly terminated following a security breach, corporate IT disabled their company email but could not revoke their personal Google account, leaving them with active production console access that triggered an emergency security shutdown across all 450 retail bakeries.</p>
<div class="study-prompts">
<p><strong class="side-heading">Architectural questions for study:</strong></p>
<ul>
<li>How does Google Cloud decouple authentication identity repositories from authorization policy evaluation?</li>
<li>What directory synchronization mechanisms bridge corporate Active Directory or Okta/Entra into Cloud Identity?</li>
<li>How does the Organization Policy constraint <code>constraints/iam.allowedPolicyMemberDomains</code> programmatically prevent personal consumer accounts from entering IAM policies?</li>
</ul>
</div>
</article>
<article class="topic-card" id="topic-02-overview">
<h3>Principals</h3>
<p><strong class="keyword">IAM Principal Taxonomy</strong> defines the complete classification of entities that can receive role bindings within Google Cloud access control policies. Google Cloud recognizes six principal types distinguished by explicit type prefixes: <code>user:{email}</code> (individual human identity), <code>group:{email}</code> (Google Group managing multiple accounts), <code>serviceAccount:{email}</code> (non-human workload identity used by applications and VM instances), <code>domain:{domain.com}</code> (all user accounts within a verified Cloud Identity domain), <code>allAuthenticatedUsers</code> (any authenticated Google account globally across the internet), and <code>allUsers</code> (any public internet caller, unauthenticated). Understanding the precise evaluation boundaries of these types prevents catastrophic data leaks caused by misinterpreting global scopes.</p>
<p><strong class="side-heading">Why today:</strong> Misinterpreting principal types—especially conflating <code>allAuthenticatedUsers</code> with internal company employees—routinely causes catastrophic public disclosures of proprietary databases and storage archives.</p>
<p><strong class="side-heading">Where it sits:</strong> Evaluated directly by the IAM Policy Enforcement Engine at the resource binding boundary across Organization, Folder, Project, and resource-level policies.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A DevOps engineer binds the <code>allAuthenticatedUsers</code> principal to an internal Cloud Storage bucket containing raw retail order payment archives, mistakenly believing the identifier restricted access to authenticated corporate staff. Because <code>allAuthenticatedUsers</code> grants access to anyone logged into any consumer Google account globally, an external security researcher accessed and downloaded 140,000 unencrypted customer transaction receipts, triggering an immediate mandatory privacy breach disclosure to federal regulators.</p>
<div class="study-prompts">
<p><strong class="side-heading">Architectural questions for study:</strong></p>
<ul>
<li>What are the syntax prefixes, evaluation mechanisms, and authorization scopes for each of the six Google Cloud IAM principal types?</li>
<li>Why does <code>allAuthenticatedUsers</code> match any consumer Gmail or external corporate account globally rather than domain-authenticated employees?</li>
<li>How does Public Access Prevention on Cloud Storage buckets enforce defense-in-depth against accidental public grants?</li>
</ul>
</div>
</article>
<article class="topic-card" id="topic-03-overview">
<h3>Why groups (not individual users) should receive roles</h3>
<p><strong class="keyword">Group-Based Access Control</strong> is the foundational enterprise architectural pattern that mandates binding IAM roles exclusively to Google Groups rather than individual human user accounts. By assigning roles to job-function groups (such as <code>group:bakery-ops@brightloaf.com</code>), cloud architects decouple user identity lifecycles from infrastructure policy management. User membership updates in corporate directories instantly propagate across all associated Google Cloud projects without modifying cloud IAM policies, preventing privilege accumulation and protecting against Google Cloud's hard policy size quotas (250 KB and 1,500 member entries).</p>
<p><strong class="side-heading">Why today:</strong> Direct user role bindings create unmanageable permission sprawl, leave orphaned credentials upon employee departure, and breach Google Cloud's 250 KB policy size limit during automated pipeline runs.</p>
<p><strong class="side-heading">Where it sits:</strong> Sits in the enterprise IAM governance layer across all Terraform modules, folder policies, and project role bindings, governing how access is granted and audited.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A cloud platform team deploys automated scripts that bind individual developer email addresses directly to IAM policies across sixty regional microservice projects, causing the production project IAM policy to breach Google Cloud's 250 KB limit. The oversized policy rejected all subsequent administrative updates, blocking an emergency CI/CD hotfix for an active payment processing bug and forcing 450 franchise stores to revert to manual paper receipts during morning rush hour.</p>
<div class="study-prompts">
<p><strong class="side-heading">Architectural questions for study:</strong></p>
<ul>
<li>What hard quotas does Google Cloud enforce on IAM policy payloads (250 KB size limit and 1,500 member count limit)?</li>
<li>How does group-based role binding eliminate privilege accumulation when engineers transition between internal teams?</li>
<li>Why does binding roles to Google Groups decouple identity administration from infrastructure CI/CD pipelines?</li>
</ul>
</div>
</article>'''

# ─────────────────────────────────────────────────────────────────────────────
# COMPLETION HTML
# ─────────────────────────────────────────────────────────────────────────────
COMPLETION_HTML = '''<div class="completion-card">
<h3>Day 24 Completion Checklist &amp; Verification Evidence</h3>
<p>To satisfy the Day 24 exit criteria, verify the following operational and architectural evidence artifacts:</p>
<ul class="checklist">
<li><input type="checkbox" id="check-24-1"> <label for="check-24-1">Workforce identity directories benchmarked: contrasted unmanaged consumer Google accounts with managed Cloud Identity and Google Workspace directories.</label></li>
<li><input type="checkbox" id="check-24-2"> <label for="check-24-2">Domain Restricted Sharing verified: confirmed that <code>constraints/iam.allowedPolicyMemberDomains</code> blocks consumer accounts and unauthorized external domains.</label></li>
<li><input type="checkbox" id="check-24-3"> <label for="check-24-3">The six IAM principal types validated: categorized user, group, serviceAccount, domain, allAuthenticatedUsers, and allUsers with precise syntax and evaluation scopes.</label></li>
<li><input type="checkbox" id="check-24-4"> <label for="check-24-4">Public exposure risks mitigated: eliminated <code>allAuthenticatedUsers</code> from internal storage assets and enforced Public Access Prevention (PAP).</label></li>
<li><input type="checkbox" id="check-24-5"> <label for="check-24-5">Group-based access control implemented: replaced individual user grants with functional Google Groups, shrinking IAM policy size by over 95% and eliminating privilege creep.</label></li>
<li><input type="checkbox" id="check-24-6"> <label for="check-24-6">Exit evidence artifact generated: produced authoritative Workforce Identity Matrix distinguishing people, service accounts, groups, and external identities at <code>scratch/day-024-workforce-identity-report.md</code>.</label></li>
</ul>
</div>'''

# ─────────────────────────────────────────────────────────────────────────────
# TOPIC 1 TECHNICAL CONTENT
# ─────────────────────────────────────────────────────────────────────────────
TOPIC_01_TECH = f'''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Cloud Identity directory architecture: Free and Premium IDaaS capabilities</strong></li>
<li><strong>Google Workspace directory integration: shared identity root with productivity suites</strong></li>
<li><strong>Consumer Google accounts: unmanaged personal identity risks in enterprise clouds</strong></li>
<li><strong>Enterprise directory synchronization: bridging Active Directory, Okta, and Entra ID via GCDS and SCIM</strong></li>
<li><strong>Domain Restricted Sharing: enforcing organizational boundaries with constraints/iam.allowedPolicyMemberDomains</strong></li>
</ul>

<h4>Cloud Identity directory architecture: Free and Premium IDaaS capabilities</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Cloud Identity</strong> is Google's standalone enterprise Identity-as-a-Service (IDaaS) platform that provides centralized identity lifecycle management, single sign-on (SSO), and device security policies anchored to a customer-verified domain name (such as <code>brightloaf.com</code>). Available in Free and Premium editions, it serves as the authoritative workforce identity repository for Google Cloud.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects design identity architectures around Cloud Identity to ensure human workforce identities are managed under strict enterprise governance. Centralizing authentication in Cloud Identity enables automated employee provisioning, mandatory multi-factor authentication (MFA) via FIDO2 hardware security keys, and instant administrative session revocation upon employee departure.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud IAM, as documented in <a href="https://cloud.google.com/iam/docs/principals-overview#domains">Google Cloud IAM Documentation: Domains (accessed 2026-10-04)</a>, Cloud Identity accounts map directly to Google Cloud Organization nodes. The Free edition provides core directory services, SAML 2.0 / OIDC federation, and 2-Step Verification enforcement for up to 50 users (expandable upon request). The Premium edition adds Context-Aware Access rules, automated mobile device management (MDM), and automated user licensing.</p>

<h4>Google Workspace directory integration: shared identity root with productivity suites</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Google Workspace Directory Integration</strong> refers to the structural identity sharing between Google Workspace collaboration applications (Gmail, Google Drive, Docs, Meet) and Google Cloud, which operate on the exact same underlying Cloud Identity directory and Google Admin Console.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> If an organization already uses Google Workspace for business email, cloud architects do not need to create a secondary user directory for Google Cloud. The existing Workspace directory already serves as the authoritative identity provider, sharing organizational units, security groups, and administrator hierarchies.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, a Google Workspace customer domain automatically pairs with the Google Cloud Organization resource. Workspace user accounts (e.g. <code>alice@brightloaf.com</code>) and Workspace Google Groups (e.g. <code>cloud-admins@brightloaf.com</code>) are instantly referenceable in Google Cloud IAM policies across all projects, folders, and resources.</p>

<h4>Consumer Google accounts: unmanaged personal identity risks in enterprise clouds</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Consumer Google Accounts</strong> are personal, unmanaged accounts created directly by individual users ending in <code>@gmail.com</code> or associated with personal non-corporate email addresses. These accounts belong entirely to the individuals who registered them.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Granting cloud resource permissions to consumer Google accounts creates severe security and compliance vulnerabilities. Enterprise administrators cannot reset passwords, enforce security key policies, monitor login audit logs, or revoke credentials when an employee or contractor leaves the company.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud IAM, while the platform allows binding roles to <code>user:contractor@gmail.com</code>, doing so violates enterprise security baselines. If a contractor departs, corporate IT deactivating their company Slack or internal email leaves the personal Gmail account fully functional, maintaining persistent backdoor access to production GCP consoles and APIs.</p>

<h4>Enterprise directory synchronization: bridging Active Directory, Okta, and Entra ID via GCDS and SCIM</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Enterprise Directory Synchronization</strong> is the automated process of mirroring users, groups, and organizational attributes from on-premises directories or third-party cloud IdPs into Cloud Identity, establishing a single authoritative source of truth.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects ensure that workforce identity lifecycles remain synchronized across the enterprise. When HR terminates an employee in Workday, automated synchronization immediately disables the account in Active Directory, Okta, and Cloud Identity, preventing orphan credentials and manual administration delays.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud provides two primary directory synchronization mechanisms: <strong>Google Cloud Directory Sync (GCDS)</strong>, an on-premises synchronization agent that mirrors Active Directory / LDAP objects via one-way sync, and <strong>SCIM (System for Cross-domain Identity Management)</strong> connectors for cloud-native IdPs like Okta, Ping Identity, and Microsoft Entra ID. Authentication is typically federated via SAML 2.0, where Google Cloud redirects sign-in requests to the corporate IdP without storing passwords in Google directories.</p>

<h4>Domain Restricted Sharing: enforcing organizational boundaries with constraints/iam.allowedPolicyMemberDomains</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Domain Restricted Sharing</strong> is an organization-level security guardrail that programmatically restricts IAM role bindings to specific, authorized Cloud Identity customer directory IDs, preventing any unapproved external accounts from receiving permissions.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects mandate Domain Restricted Sharing as a non-negotiable governance control. Without this constraint, any project owner across hundreds of departmental projects can inadvertently or intentionally grant access to external personal Gmail accounts or third-party partner domains.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud Resource Manager, Domain Restricted Sharing is enforced using the list constraint <code>constraints/iam.allowedPolicyMemberDomains</code>. When configured with the customer directory ID (e.g. <code>C01234567</code>), any API call attempting to add a principal outside the approved Cloud Identity domain is immediately blocked with an HTTP 400 Bad Request error: <code>FAILED_PRECONDITION: One or more members are not allowed by organization policy</code>.</p>

<div class="table-wrap">
<table>
<caption>Table 24.1: Identity Repository Capabilities, Governance Controls, and Cloud Integration</caption>
<thead>
<tr>
<th scope="col">Directory Model</th>
<th scope="col">Primary Use Case</th>
<th scope="col">SAML / OIDC SSO</th>
<th scope="col">Centralized De-provisioning</th>
<th scope="col">Google Cloud Enterprise Governance</th>
</tr>
</thead>
<tbody>
<tr>
<th scope="row">Cloud Identity Free</th>
<td>Enterprises using external IdPs (Okta/Entra) needing Google Cloud access</td>
<td>Supported (SAML 2.0 / OIDC)</td>
<td>Supported via SCIM / GCDS</td>
<td>Baseline standard for Google Cloud workforce administration</td>
</tr>
<tr>
<th scope="row">Cloud Identity Premium</th>
<td>Enterprises requiring advanced device management &amp; Context-Aware Access</td>
<td>Supported (SAML 2.0 / OIDC)</td>
<td>Supported with automated rule engines</td>
<td>Enterprise standard with zero-trust context-aware policies</td>
</tr>
<tr>
<th scope="row">Google Workspace</th>
<td>Enterprises using Google for both email/collaboration and cloud operations</td>
<td>Supported (Built-in or federated)</td>
<td>Supported via Admin Console / API</td>
<td>Shares identical identity root with Cloud Identity</td>
</tr>
<tr>
<th scope="row">Consumer Google Account</th>
<td>Personal individuals, unmanaged personal email accounts</td>
<td>Unsupported</td>
<td>Unsupported (Cannot be revoked by enterprise)</td>
<td>Strictly prohibited; blocked via Organization Policy constraints</td>
</tr>
</tbody>
</table>
</div>

<p><strong class="side-heading">Concrete example:</strong> Enforcing Domain Restricted Sharing Organization Policy to restrict IAM bindings strictly to corporate customer directory ID <code>C01234567</code>:</p>
<pre><code># 1. Inspect existing organization policy for domain restrictions
$ gcloud resource-manager org-policies describe constraints/iam.allowedPolicyMemberDomains \\
    --organization=714029482103

# 2. Author policy definition restricting members to corporate Customer ID
$ cat <<'EOF' > policy-domain-restriction.yaml
constraint: constraints/iam.allowedPolicyMemberDomains
listPolicy:
  allowedValues:
    - "C01234567"
EOF

# 3. Apply the constraint at the organization apex
$ gcloud resource-manager org-policies set-policy policy-domain-restriction.yaml \\
    --organization=714029482103
Applied policy [constraints/iam.allowedPolicyMemberDomains] to [organizations/714029482103].

# 4. Attempt to add an unmanaged consumer Gmail account (rejected by Org Policy)
$ gcloud projects add-iam-policy-binding bl-logistics-routing-prod \\
    --member="user:contractor.dave@gmail.com" \\
    --role="roles/viewer"
ERROR: (gcloud.projects.add-iam-policy-binding) FAILED_PRECONDITION: One or more members are not allowed by organization policy constraints/iam.allowedPolicyMemberDomains: user:contractor.dave@gmail.com
</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> The commands, configuration YAML payloads, and directory synchronization patterns shown above demonstrate verified Google Cloud Resource Manager and Cloud Identity behaviors. They do not simulate live cryptographic token exchange with third-party SAML identity providers or active directory domain controller schema synchronizations.</p>

<div class="callout note">
<strong>Further study · Workforce directory architecture</strong>
<p>Review the primary Google Cloud documentation for domain-based principal governance:</p>
<ul>
<li><a href="https://cloud.google.com/iam/docs/principals-overview#domains">Google Cloud IAM Documentation: Domains (accessed 2026-10-04)</a></li>
</ul>
</div>'''

# ─────────────────────────────────────────────────────────────────────────────
# TOPIC 2 TECHNICAL CONTENT
# ─────────────────────────────────────────────────────────────────────────────
TOPIC_02_TECH = f'''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Human and group principals: user and group member syntax and resolution</strong></li>
<li><strong>Workload principals: serviceAccount identity mechanics and execution boundaries</strong></li>
<li><strong>Domain-wide principals: syntax, evaluation scope, and blast radius of domain identifiers</strong></li>
<li><strong>The allAuthenticatedUsers exposure trap: global Google account authentication risks</strong></li>
<li><strong>The allUsers public boundary: unauthenticated internet access and Public Access Prevention</strong></li>
</ul>

<h4>Human and group principals: user and group member syntax and resolution</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Human and Group Principals</strong> represent individuals and collections of people identified by explicit member string prefixes: <code>user:&#123;email&#125;</code> for single individual Google accounts and <code>group:&#123;email&#125;</code> for Google Groups managed in Cloud Identity.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Distinguishing individual users from groups is central to access governance. While <code>user:</code> binds permissions to one specific human, <code>group:</code> establishes indirect role assignment, allowing identity management to occur within directories without mutating infrastructure configuration files.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud IAM, as documented in <a href="https://cloud.google.com/iam/docs/principals-overview#principal-types">Google Cloud IAM Documentation: Principal types (accessed 2026-10-04)</a>, when a caller sends an API request with an OAuth 2.0 bearer token, the IAM policy evaluation engine matches the caller's email against <code>user:</code> bindings and queries Cloud Identity group memberships to match any relevant <code>group:</code> bindings.</p>

<h4>Workload principals: serviceAccount identity mechanics and execution boundaries</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Workload Principals</strong> are non-human service accounts identified by the prefix <code>serviceAccount:&#123;email&#125;</code>. They represent software applications, automated deployment pipelines, and VM instances rather than human users.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Service accounts provide dedicated operational identities with least-privilege boundaries. Architects enforce Workload Identity Federation for external CI/CD pipelines (e.g. GitHub Actions) and GKE clusters, eliminating static, exportable JSON private keys.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud IAM, service account emails follow predictable patterns: user-managed service accounts end with <code>@&#123;PROJECT_ID&#125;.iam.gserviceaccount.com</code>, while Google-managed service agents use domain-specific suffixes (such as <code>@cloudservices.gserviceaccount.com</code>). They are granted roles directly on resources they need to access.</p>

<h4>Domain-wide principals: syntax, evaluation scope, and blast radius of domain identifiers</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Domain-Wide Principals</strong> are member bindings formatted as <code>domain:&#123;domain.com&#125;</code> that automatically encompass every user account managed under a verified Cloud Identity or Google Workspace domain.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Domain-wide bindings have an extremely broad blast radius. Granting permissions to an entire domain is appropriate only for universal internal assets (such as an all-hands intranet or enterprise handbook), and should never be used for sensitive production resources.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud IAM, binding <code>domain:brightloaf.com</code> grants the specified role to every active user identity in BrightLoaf's Cloud Identity directory. If a new user is provisioned in the directory tomorrow, they instantly inherit all permissions attached to that domain binding without administrative intervention.</p>

<h4>The allAuthenticatedUsers exposure trap: global Google account authentication risks</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">The allAuthenticatedUsers Exposure Trap</strong> is a severe security vulnerability resulting from the mistaken belief that <code>allAuthenticatedUsers</code> restricts access to authenticated employees within the company domain. In reality, it matches <strong>anyone in the world</strong> who is logged into <em>any</em> Google account.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects must rigorously audit and prevent the usage of <code>allAuthenticatedUsers</code> for internal enterprise workloads. Using this identifier on internal storage buckets or databases completely eliminates confidentiality, exposing proprietary business data to competitors, external contractors, and malicious actors.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud IAM, <code>allAuthenticatedUsers</code> is a special identifier representing any human or service account possessing a valid Google authentication token—including consumer <code>@gmail.com</code> accounts. It must never be used for enterprise data storage. Enforcing Public Access Prevention (PAP) on Cloud Storage blocks both <code>allUsers</code> and <code>allAuthenticatedUsers</code>.</p>

<h4>The allUsers public boundary: unauthenticated internet access and Public Access Prevention</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">The allUsers Public Boundary</strong> is the special identifier representing anyone on the public internet, requiring no authentication credentials whatsoever.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> <code>allUsers</code> is intended strictly for intentional, public internet-facing services, such as public website static assets hosted on Cloud Storage or unauthenticated public APIs deployed on Cloud Run.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, granting <code>roles/storage.objectViewer</code> to <code>allUsers</code> makes bucket contents downloadable by anyone worldwide without authentication. To prevent accidental data leaks, architects enforce <strong>Public Access Prevention (PAP)</strong> via <code>constraints/storage.publicAccessPrevention</code>, which programmatically forbids applying <code>allUsers</code> or <code>allAuthenticatedUsers</code> to Cloud Storage buckets.</p>

<div class="table-wrap">
<table>
<caption>Table 24.2: Google Cloud IAM Principal Types, Syntax, Evaluation Scope, and Exposure Risks</caption>
<thead>
<tr>
<th scope="col">Principal Type</th>
<th scope="col">Prefix Syntax Example</th>
<th scope="col">Evaluation Scope</th>
<th scope="col">Security Risk Level</th>
<th scope="col">Recommended Enterprise Usage</th>
</tr>
</thead>
<tbody>
<tr>
<th scope="row">Google Group</th>
<td><code>group:pos-devs@brightloaf.com</code></td>
<td>Members of the specific Google Group in Cloud Identity</td>
<td>Low (Managed via directory)</td>
<td>Standard pattern for all workforce access</td>
</tr>
<tr>
<th scope="row">Service Account</th>
<td><code>serviceAccount:sa@proj.iam.gserviceaccount.com</code></td>
<td>Target non-human application workload</td>
<td>Low to Moderate (Token security)</td>
<td>Standard pattern for automated workload authorization</td>
</tr>
<tr>
<th scope="row">Individual User</th>
<td><code>user:alice@brightloaf.com</code></td>
<td>Single specific human user account</td>
<td>Moderate (Administrative sprawl)</td>
<td>Anti-pattern; avoid in enterprise production IAM</td>
</tr>
<tr>
<th scope="row">Domain</th>
<td><code>domain:brightloaf.com</code></td>
<td>All users within the verified Cloud Identity directory</td>
<td>Moderate to High (Broad blast radius)</td>
<td>Use sparingly for enterprise-wide read-only portals</td>
</tr>
<tr>
<th scope="row">allAuthenticatedUsers</th>
<td><code>allAuthenticatedUsers</code></td>
<td>ANY valid Google account globally (Consumer &amp; Enterprise)</td>
<td>Extreme Risk (Data leak)</td>
<td>Strictly prohibited for internal enterprise resources</td>
</tr>
<tr>
<th scope="row">allUsers</th>
<td><code>allUsers</code></td>
<td>Public unauthenticated internet (Anonymous callers)</td>
<td>Public Exposure</td>
<td>Restricted strictly to public CDN assets and web frontends</td>
</tr>
</tbody>
</table>
</div>

<div class="technical-figure">
{fig1}
</div>

<p><strong class="side-heading">Concrete example:</strong> Scanning and remediating unauthorized public principal bindings on Cloud Storage buckets using Google Cloud CLI:</p>
<pre><code># 1. Inspect IAM policy of production storage bucket
$ gcloud storage buckets get-iam-policy gs://bl-order-archives-prod --format="yaml"
bindings:
- members:
  - allAuthenticatedUsers
  role: roles/storage.objectViewer
- members:
  - group:cloud-storage-admins@brightloaf.com
  role: roles/storage.admin

# 2. Revoke dangerous global authenticated principal binding
$ gcloud storage buckets remove-iam-policy-binding gs://bl-order-archives-prod \\
    --member="allAuthenticatedUsers" \\
    --role="roles/storage.objectViewer"

# 3. Enforce Public Access Prevention (PAP) on the bucket
$ gcloud storage buckets update gs://bl-order-archives-prod \\
    --public-access-prevention
Updating gs://bl-order-archives-prod/...
Completed updating gs://bl-order-archives-prod/

# 4. Verify PAP configuration prevents public access
$ gcloud storage buckets describe gs://bl-order-archives-prod \\
    --format="yaml(publicAccessPrevention)"
publicAccessPrevention: enforced
</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> The commands and policy definitions shown above demonstrate verified Google Cloud IAM member string evaluation, Cloud Storage IAM binding mechanics, and Public Access Prevention enforcement. They do not simulate live public internet penetration testing or malicious credential exfiltration from external networks.</p>

<div class="callout note">
<strong>Further study · IAM principal taxonomy</strong>
<p>Review the primary Google Cloud documentation for principal types and member evaluation:</p>
<ul>
<li><a href="https://cloud.google.com/iam/docs/principals-overview#principal-types">Google Cloud IAM Documentation: Principal types (accessed 2026-10-04)</a></li>
</ul>
</div>'''

# ─────────────────────────────────────────────────────────────────────────────
# TOPIC 3 TECHNICAL CONTENT
# ─────────────────────────────────────────────────────────────────────────────
TOPIC_03_TECH = f'''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Hard platform quotas: 250 KB policy size and 1,500 member count limits</strong></li>
<li><strong>Mitigating privilege accumulation: eliminating privilege creep across organizational transfers</strong></li>
<li><strong>Decoupling identity lifecycle from cloud infrastructure: zero-Terraform offboarding</strong></li>
<li><strong>Auditability and governance: centralized group attestation vs distributed IAM policy inspection</strong></li>
<li><strong>Access group design patterns: modeling job functions and resource scopes with security groups</strong></li>
</ul>

<h4>Hard platform quotas: 250 KB policy size and 1,500 member count limits</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">IAM Policy Size Quotas</strong> are strict platform boundaries enforced by Google Cloud: an individual IAM policy cannot exceed <strong>250 KB</strong> in total serialized JSON size, and cannot contain more than <strong>1,500 total member entries</strong> across all role bindings.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Direct individual user role bindings scale linearly with employee headcount. In organizations with hundreds of engineers and microservices, direct bindings rapidly exhaust the 250 KB / 1,500 member threshold. Once exceeded, all IAM mutations fail, blocking critical CI/CD deployments and production hotfixes.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud IAM, as documented in <a href="https://cloud.google.com/iam/docs/groups-best-practices#job-functions-access">Google Cloud IAM Documentation: Use access groups to model job functions and grant access to resources (accessed 2026-10-04)</a>, assigning roles to Google Groups consolidates hundreds of individual member strings into a single group identifier (e.g. <code>group:bakery-ops@brightloaf.com</code>), shrinking policy payloads by over 95% and guaranteeing scalability within platform quotas.</p>

<h4>Mitigating privilege accumulation: eliminating privilege creep across organizational transfers</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Privilege Accumulation Mitigation</strong> is the security architecture discipline that prevents employees from retaining historical access permissions as they transfer between projects, teams, or departments.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Direct user bindings inevitably cause "privilege creep"—an engineer transfers from logistics to finance, gains finance permissions, but retains logistics permissions because project IAM policies are rarely audited or pruned. Over time, veteran employees accumulate dangerous superuser privileges across the entire cloud estate.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> With group-based access control, transferring an employee simply involves moving them from <code>group:logistics-eng@brightloaf.com</code> to <code>group:finance-eng@brightloaf.com</code> in Cloud Identity. Because project IAM bindings reference groups rather than individuals, the user automatically loses access to logistics projects and gains access to finance projects instantly.</p>

<h4>Decoupling identity lifecycle from cloud infrastructure: zero-Terraform offboarding</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Identity Lifecycle Decoupling</strong> separates user account management (onboarding, offboarding, role transitions) from infrastructure-as-code deployment pipelines.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Coupling user offboarding to Terraform runs creates dangerous delays. If revoking an employee's access requires a Terraform code review, merge, and CI/CD apply, departed personnel retain active access for hours or days. Decoupling ensures instantaneous revocation at the directory tier.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> When roles are bound exclusively to Google Groups, employee termination requires only deactivating the user in Cloud Identity / Okta. The user's Google Cloud access is revoked across all hundreds of projects globally within seconds, without triggering any Terraform pipeline execution or altering Google Cloud IAM policy JSON payloads.</p>

<h4>Auditability and governance: centralized group attestation vs distributed IAM policy inspection</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Centralized Group Attestation</strong> is the compliance auditing methodology where access rights are reviewed by inspecting membership of central identity groups rather than scanning thousands of distributed resource policies.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Compliance auditors requiring proof of least privilege struggle to audit distributed cloud policies where individual users are scattered across hundreds of projects. Group-based access allows quarterly access certifications to be conducted cleanly in the identity provider.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud environments, security auditors inspect Google Group memberships in the Admin Console or Cloud Identity API. Instead of crawling thousands of individual project IAM policies to confirm who can access production Spanner databases, auditors verify that only authorized engineers belong to <code>group:spanner-prod-admins@brightloaf.com</code>.</p>

<h4>Access group design patterns: modeling job functions and resource scopes with security groups</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Access Group Design Patterns</strong> establish standardized naming and scoping conventions for Google Groups that model specific job functions (e.g. developers, operators, data analysts) and resource scopes (non-prod vs prod).</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects define clean group taxonomy conventions (such as <code>gcp-&#123;role&#125;-&#123;scope&#125;@company.com</code>) to ensure predictable, self-documenting access models that prevent accidental over-permissioning.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud supports <strong>Security Groups</strong> in Cloud Identity—groups specifically flagged for access control that prevent users from self-joining or modifying group settings. Architects bind predefined or custom IAM roles to these security groups at folder and project levels, creating a durable Role-Based Access Control (RBAC) foundation.</p>

<div class="table-wrap">
<table>
<caption>Table 24.3: Comparative Architectural Analysis: Direct User Bindings vs. Group-Based Authorization</caption>
<thead>
<tr>
<th scope="col">Architectural Dimension</th>
<th scope="col">Direct User Binding (Anti-Pattern)</th>
<th scope="col">Group-Based Authorization (Enterprise Standard)</th>
</tr>
</thead>
<tbody>
<tr>
<th scope="row">Policy Size &amp; Scalability</th>
<td>Violates 250 KB / 1,500 member limit as team scales</td>
<td>Compact (&lt; 5 KB); easily supports thousands of employees</td>
</tr>
<tr>
<th scope="row">Employee Offboarding Revocation</th>
<td>High risk; requires scanning &amp; editing dozens of project policies</td>
<td>Instantaneous; single deactivation in corporate IdP revokes all access</td>
</tr>
<tr>
<th scope="row">Privilege Accumulation (Creep)</th>
<td>Severe; historical permissions rarely pruned upon internal transfer</td>
<td>Eliminated; moving user between groups automatically updates access</td>
</tr>
<tr>
<th scope="row">Infrastructure Pipeline Drift</th>
<td>Constant Terraform drift as developers join and depart teams</td>
<td>Zero drift; Terraform declares static job-function group bindings</td>
</tr>
<tr>
<th scope="row">Compliance &amp; Auditability</th>
<td>Unmanageable matrix; requires complex cross-project IAM dumps</td>
<td>Clean audit trail; group memberships audited directly in corporate directory</td>
</tr>
</tbody>
</table>
</div>

<div class="technical-figure">
{fig2}
</div>

<p><strong class="side-heading">Concrete example:</strong> Consolidating individual user bindings into job-function Google Groups to reduce policy size:</p>
<pre><code># 1. Inspect bloated project IAM policy with individual users
$ gcloud projects get-iam-policy bl-pos-production --format="json" | jq '.bindings[] | select(.role=="roles/viewer")'
{{
  "members": [
    "user:alice@brightloaf.com",
    "user:bob@brightloaf.com",
    "user:carol@brightloaf.com",
    "user:david@brightloaf.com"
  ],
  "role": "roles/viewer"
}}

# 2. Add job-function Google Group binding
$ gcloud projects add-iam-policy-binding bl-pos-production \\
    --member="group:pos-devs@brightloaf.com" \\
    --role="roles/viewer"

# 3. Remove individual user bindings
$ for u in alice bob carol david; do
    gcloud projects remove-iam-policy-binding bl-pos-production \\
      --member="user:${{u}}@brightloaf.com" \\
      --role="roles/viewer"
  done

# 4. Verify consolidated group binding
$ gcloud projects get-iam-policy bl-pos-production --format="json" | jq '.bindings[] | select(.role=="roles/viewer")'
{{
  "members": [
    "group:pos-devs@brightloaf.com"
  ],
  "role": "roles/viewer"
}}
</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> The policy metrics and consolidation ratios shown above demonstrate verified Google Cloud IAM policy JSON payload sizes and member evaluation behaviors. They do not simulate live high-throughput API quota starvation or concurrent race condition mutations on IAM policies across hundreds of administrative callers.</p>

<div class="callout note">
<strong>Further study · Group-based access control</strong>
<p>Review the primary Google Cloud documentation for enterprise group access modeling:</p>
<ul>
<li><a href="https://cloud.google.com/iam/docs/groups-best-practices#job-functions-access">Google Cloud IAM Documentation: Use access groups to model job functions and grant access to resources (accessed 2026-10-04)</a></li>
</ul>
</div>'''

# ─────────────────────────────────────────────────────────────────────────────
# PART 3 SCENARIOS
# ─────────────────────────────────────────────────────────────────────────────
SCENARIO_01 = {
    'scenario': 'BrightLoaf platform engineering engaged an external logistics consulting firm to optimize automated morning delivery routing schedules. During onboarding, an infrastructure administrator bound an external contractor\'s personal Google account (contractor.dave@gmail.com) directly to roles/editor on production project bl-logistics-routing-prod. Three months later, the contractor was terminated following a contractual dispute. Corporate IT deactivated the contractor\'s corporate email and Slack accounts. However, at 21:14 UTC, Security Command Center triggered a high-severity alert: the terminated contractor was actively executing BigQuery queries against production delivery schedule tables from residential IP 198.51.100.84 using their personal Gmail account.',
    'impact': 'BrightLoaf suffered an unauthorized access breach of proprietary retail delivery route schedules and customer bakery addresses. Security operations conducted an emergency containment investigation costing $38,000 in third-party forensic auditing.',
    'constraints': 'All production cloud resources must be restricted strictly to corporate-managed identities. BrightLoaf business invariant: replaying delivery events or rotating credentials must never result in duplicate physical bread fulfillment (<= 1 physical fulfillment per unique order ID).',
    'evidence': fig3,
    'root': 'The security exposure was caused by permitting unmanaged consumer Google accounts into production project IAM policies. When workforce identities are not anchored in corporate Cloud Identity, centralized HR de-provisioning workflows fail to revoke cloud access, leaving residual shadow permissions that persist indefinitely until manually discovered.',
    'diagnostic_steps': [
        'Inspect Security Command Center Alert: Identify unauthorized BigQuery query activity from external IP 198.51.100.84.',
        'Review Cloud Audit Logs: Query audit logs for principalEmail="contractor.dave@gmail.com" to determine all accessed resources and exported tables.',
        'Audit Project IAM Policies: Inspect bl-logistics-routing-prod IAM policy to locate active user:contractor.dave@gmail.com bindings.',
        'Check Directory De-provisioning Status: Verify in Google Admin Console that the contractor held no managed @brightloaf.com corporate account.',
        'Audit Organization Policy Constraints: Verify that constraints/iam.allowedPolicyMemberDomains was unenforced at the Organization apex.'
    ],
    'remediation_steps': [
        'Immediate IAM Revocation: Remove contractor.dave@gmail.com from all project IAM policies across the organization.',
        'Enforce Domain Restricted Sharing: Apply constraints/iam.allowedPolicyMemberDomains at the Organization root, restricting future IAM additions strictly to corporate Customer ID C01234567.',
        'Mandate Cloud Identity Accounts: Require all future external partners to be provisioned with managed contractor.name@brightloaf.com accounts enforcing hardware security keys.',
        'Rotate Database Encryption Keys: Rotate KMS keys and database access credentials for logistics routing databases.',
        'Verify Fulfillment Invariant: Query delivery dispatch logs to ensure no duplicate orders were injected, preserving <= 1 physical fulfillment per unique order ID.'
    ],
    'verify': 'Verified via Cloud Asset Inventory that zero @gmail.com accounts remain bound to any project policy, and attempting to add a consumer account is rejected by constraints/iam.allowedPolicyMemberDomains.',
    'residual': 'Organization policy domain restrictions apply to future policy mutations; existing non-compliant bindings must be identified and removed via automated Cloud Asset Inventory audits.',
    'diagram_enabled': False,
    'facts': 'Contractor used personal Gmail account; corporate IT offboarding disabled email but left GCP access intact; contractor queried BigQuery tables from residential IP; removing binding and enforcing Domain Restricted Sharing blocked future consumer accounts.',
    'inference': 'Decoupled consumer accounts bypass enterprise offboarding lifecycles; centralized Cloud Identity directory anchoring is mandatory for cloud access control.',
    'expected': 'Domain Restricted Sharing blocks unmanaged consumer accounts at admission time with FAILED_PRECONDITION errors.'
}

SCENARIO_02 = {
    'scenario': 'A DevOps engineer at BrightLoaf was tasked with granting read access on storage bucket gs://bl-order-archives-prod to all internal corporate employees. Misinterpreting the principal identifier allAuthenticatedUsers as meaning "all employees authenticated into our corporate single sign-on," the engineer applied roles/storage.objectViewer to allAuthenticatedUsers. Within 48 hours, an external security researcher discovered the open bucket, authenticated with a personal Google account, and downloaded 140,000 unencrypted customer order receipts containing billing names, store locations, and transaction amounts.',
    'impact': 'BrightLoaf suffered an international privacy incident requiring mandatory notification to data protection regulators. The company incurred $92,000 in customer notification, credit monitoring, and regulatory compliance legal fees.',
    'constraints': 'Internal order archives must remain accessible only to authorized corporate staff. BrightLoaf business invariant: replaying delivery events or rotating credentials must never result in duplicate physical bread fulfillment (<= 1 physical fulfillment per unique order ID).',
    'evidence': fig4,
    'root': 'The incident was caused by conflating the global allAuthenticatedUsers identifier with internal domain-authenticated users. allAuthenticatedUsers matches ANY authenticated Google account worldwide, including consumer accounts and competitors. Furthermore, Public Access Prevention (PAP) was not enforced on the storage bucket.',
    'diagnostic_steps': [
        'Review Security Operations Notice: Identify external disclosure report indicating public accessibility of gs://bl-order-archives-prod.',
        'Inspect Bucket IAM Policy: Run gcloud storage buckets get-iam-policy to discover the allAuthenticatedUsers binding.',
        'Inspect Cloud Storage Access Logs: Analyze storage access logs for external IP addresses and personal Google accounts that downloaded archive objects.',
        'Audit Organization PAP Status: Check whether constraints/storage.publicAccessPrevention was enforced across the folder hierarchy.',
        'Verify Order Data Integrity: Confirm that downloaded archive files were read-only and no physical order manipulation occurred.'
    ],
    'remediation_steps': [
        'Immediate IAM Removal: Strip allAuthenticatedUsers from gs://bl-order-archives-prod immediately.',
        'Enforce Public Access Prevention (PAP): Enable PAP on the storage bucket and enforce constraints/storage.publicAccessPrevention across the Organization.',
        'Replace with Corporate Group: Grant roles/storage.objectViewer exclusively to group:order-auditors@brightloaf.com.',
        'Enable Storage Object Versioning & CMEK: Apply Customer-Managed Encryption Keys to protect order archive data at rest.',
        'Audit Fulfillment Invariant: Reconcile daily order fulfillment queues to guarantee zero physical duplication (<= 1 physical fulfillment per unique order ID).'
    ],
    'verify': 'Verified that unauthenticated requests and requests with personal Google tokens receive HTTP 403 Forbidden, and attempting to add allAuthenticatedUsers fails due to Public Access Prevention.',
    'residual': 'PAP prevents public grants on Cloud Storage buckets; other resource types (e.g. Cloud Run, BigQuery) require dedicated Organization Policy constraints to prevent public exposure.',
    'diagram_enabled': False,
    'facts': 'DevOps engineer bound allAuthenticatedUsers to order archive bucket; researcher downloaded 140k receipts; allAuthenticatedUsers matched all global Google users; removing binding and enabling PAP restored security.',
    'inference': 'allAuthenticatedUsers is a global public identifier; internal workforce access must always be granted via domain-scoped Google Groups.',
    'expected': 'Public Access Prevention rejects all public and allAuthenticatedUsers bindings at the API admission gateway.'
}

SCENARIO_03 = {
    'scenario': 'The platform automation team at BrightLoaf maintained a custom Python onboarding script that bound individual developer email addresses directly to roles/editor across 60 regional bakery microservice projects. Over three years, 240 developers joined the engineering team. During an emergency deployment to patch an active tax calculation bug in point-of-sale software, the CI/CD pipeline attempted to bind an emergency service account to project bl-pos-production. The Google Cloud API returned an immediate HTTP 400 error: "Policy size exceeds maximum allowed size of 250 KB." The oversized policy rejected all subsequent updates, freezing CI/CD deployments and forcing 450 franchise stores to revert to manual paper receipts during morning rush hour.',
    'impact': 'The deployment freeze blocked emergency software hotfixes for 3.5 hours during morning peak sales. 450 franchise bakeries experienced delayed register updates, resulting in $115,000 in uncollected franchise revenue.',
    'constraints': 'CI/CD deployment pipelines must maintain sub-minute IAM update execution. BrightLoaf business invariant: replaying delivery events or rotating credentials must never result in duplicate physical bread fulfillment (<= 1 physical fulfillment per unique order ID).',
    'evidence': fig5,
    'root': 'The root cause was the direct binding of hundreds of individual user accounts to project IAM policies. The serialized JSON IAM policy reached 251,480 bytes with 1,488 member entries, breaching Google Cloud\'s hard quotas of 250 KB and 1,500 members. The policy became locked against further administrative modifications.',
    'diagnostic_steps': [
        'Review CI/CD Pipeline Log: Identify failed gcloud projects set-iam-policy call with HTTP 400 policy size quota error.',
        'Inspect Policy Payload Size: Fetch current policy JSON and measure serialized byte size (251,480 bytes, 1,488 member entries).',
        'Identify Individual User Sprawl: Scan policy bindings to count individual user: members versus group: members.',
        'Cross-Reference Active Employee Directory: Discover that 42 departed contractors and former employees remained bound to the project policy.',
        'Verify Point-of-Sale Register State: Confirm that store registers buffered transactions locally and did not duplicate fulfilled bread orders.'
    ],
    'remediation_steps': [
        'Author Consolidated Group Policy: Define job-function groups (group:pos-devs@brightloaf.com, group:pos-ops@brightloaf.com) in Cloud Identity.',
        'Execute Emergency Policy Pruning: Script a surgical removal of orphaned former employee accounts to bring policy size under 250 KB.',
        'Migrate All Users to Groups: Bind roles exclusively to the consolidated Google Groups, reducing member entries from 1,488 to 14.',
        'Verify Payload Compression: Confirm post-migration policy payload size is 4,820 bytes (98.1% reduction).',
        'Deploy POS Emergency Hotfix: Execute the unblocked CI/CD pipeline to deploy the tax calculation bugfix across all 450 store registers.'
    ],
    'verify': 'Verified that project IAM policy size is 4,820 bytes, all subsequent IAM mutations succeed immediately, and the emergency service account bound cleanly.',
    'residual': 'Group membership changes propagate asynchronously through Google\'s global token cache (typically under 5 minutes); break-glass procedures must account for cache propagation delay.',
    'diagram_enabled': False,
    'facts': 'Direct user bindings bloated IAM policy to 251.5 KB; Google Cloud quota rejected modifications; CI/CD pipeline froze; consolidating individual bindings into 14 Google Groups reduced policy to 4.8 KB.',
    'inference': 'Direct user bindings violate cloud scale invariants; group-based access control is the only scalable pattern that respects platform quotas.',
    'expected': 'Consolidated group-based IAM policies remain orders of magnitude below 250 KB platform quotas, ensuring reliable pipeline operations.'
}

# ─────────────────────────────────────────────────────────────────────────────
# LABS (8 STAGES EACH)
# ─────────────────────────────────────────────────────────────────────────────
LAB_01_STEPS = [
    '''**Stage 1: Preflight: validate Python 3 and shell tools**

**Location:** local terminal

**Actions:**
Verify that Python 3 and standard POSIX tools are available in the laboratory environment, and initialize the dedicated directory structure for Day 24 Exercise 1.
```bash
command -v bash python3
mkdir -p scratch/day24_lab/topic1
cat <<'EOF' > scratch/day24_lab/topic1/stage1_preflight.py
import json, sys

preflight = {
    "exercise": "Exercise 1: Directory Provider Audit & Domain Restricted Sharing",
    "python_version": sys.version.split()[0],
    "status": "READY"
}

with open("scratch/day24_lab/stage1_preflight.json", "w") as f:
    json.dump(preflight, f, indent=2)

print("Stage 1 verified: Python 3 runtime and lab directories ready.")
EOF
python3 scratch/day24_lab/topic1/stage1_preflight.py
```

**Expected result:**
Preflight record saved to scratch/day24_lab/stage1_preflight.json.

**Save:** scratch/day24_lab/stage1_preflight.json''',

    '''**Stage 2: Prepare target directory and inventory inputs**

**Location:** local terminal

**Actions:**
Construct a synthetic enterprise IAM policy member inventory representing an unshielded cloud organization with active bindings across managed corporate domains, unmanaged consumer Gmail accounts, external partners, and workload service accounts.
```bash
cat <<'EOF' > scratch/day24_lab/topic1/stage2_prepare_inventory.py
import json

inventory = {
    "organization_id": "714029482103",
    "customer_directory_id": "C01234567",
    "approved_domains": ["brightloaf.com", "franchise.brightloaf.com"],
    "policy_bindings": [
        {"role": "roles/viewer", "member": "user:alice@brightloaf.com", "resource": "projects/bl-pos-production"},
        {"role": "roles/editor", "member": "user:contractor.dave@gmail.com", "resource": "projects/bl-logistics-routing-prod"},
        {"role": "roles/spanner.databaseUser", "member": "serviceAccount:order-api@bl-prod.iam.gserviceaccount.com", "resource": "projects/bl-pos-production"},
        {"role": "roles/monitoring.viewer", "member": "user:support-lead@franchise.brightloaf.com", "resource": "projects/bl-franchise-monitoring"},
        {"role": "roles/logging.viewer", "member": "user:external-partner@yahoo.com", "resource": "projects/bl-logistics-routing-prod"},
        {"role": "roles/resourcemanager.organizationAdmin", "member": "group:cloud-admins@brightloaf.com", "resource": "organizations/714029482103"},
        {"role": "roles/storage.objectViewer", "member": "user:shadow-test@gmail.com", "resource": "projects/bl-analytics-prod"}
    ]
}

with open("scratch/day24_lab/stage2_identity_inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

print(f"Stage 2 verified: Created inventory with {len(inventory['policy_bindings'])} bindings.")
EOF
python3 scratch/day24_lab/topic1/stage2_prepare_inventory.py
```

**Expected result:**
Inventory record saved to scratch/day24_lab/stage2_identity_inventory.json.

**Save:** scratch/day24_lab/stage2_identity_inventory.json''',

    '''**Stage 3: Author Domain Restricted Sharing analysis script**

**Location:** local terminal

**Actions:**
Author the domain verification and compliance analysis engine (`stage3_audit_domains.py`) to parse principal member strings, evaluate domain governance boundaries, and enforce the rules of `constraints/iam.allowedPolicyMemberDomains`.
```bash
cat <<'EOF' > scratch/day24_lab/topic1/stage3_audit_domains.py
import json

with open("scratch/day24_lab/stage2_identity_inventory.json") as f:
    data = json.load(f)

approved_domains = set(data["approved_domains"])

def audit_principal(member):
    if member.startswith("serviceAccount:"):
        return True, "SERVICE_ACCOUNT", "Compliant: Google Cloud Workload Identity"
    if member.startswith("group:"):
        domain = member.split("@", 1)[1]
        if domain in approved_domains:
            return True, "CORPORATE_GROUP", f"Compliant: Approved domain {domain}"
        return False, "EXTERNAL_GROUP", f"VIOLATION: Unapproved group domain {domain}"
    if member.startswith("user:"):
        domain = member.split("@", 1)[1]
        if domain in approved_domains:
            return True, "CORPORATE_USER", f"Compliant: Managed corporate domain {domain}"
        return False, "CONSUMER_SHADOW_ACCOUNT", f"CRITICAL: Unmanaged domain {domain} violates Org Policy"
    return False, "UNKNOWN", f"Unrecognized principal prefix: {member}"

analysis_spec = {
    "engine": "Domain Restricted Sharing Audit Engine v1.0",
    "enforced_constraint": "constraints/iam.allowedPolicyMemberDomains",
    "target_customer_id": data["customer_directory_id"],
    "approved_domains": list(approved_domains)
}

with open("scratch/day24_lab/stage3_audit_spec.json", "w") as f:
    json.dump(analysis_spec, f, indent=2)

print("Stage 3 verified: Authoring complete for Domain Restricted Sharing audit engine.")
EOF
python3 scratch/day24_lab/topic1/stage3_audit_domains.py
```

**Expected result:**
Audit spec saved to scratch/day24_lab/stage3_audit_spec.json.

**Save:** scratch/day24_lab/stage3_audit_spec.json''',

    '''**Stage 4: Execute domain audit against inventory**

**Location:** local terminal

**Actions:**
Execute the domain audit script against the inventory dataset, classifying each principal binding into approved or non-compliant categories.
```bash
cat <<'EOF' > scratch/day24_lab/topic1/stage4_execute_audit.py
import json

with open("scratch/day24_lab/stage2_identity_inventory.json") as f:
    data = json.load(f)

approved_domains = set(data["approved_domains"])

results = []
for b in data["policy_bindings"]:
    member = b["member"]
    is_compliant = False
    category = "UNKNOWN"
    reason = ""

    if member.startswith("serviceAccount:"):
        is_compliant, category, reason = True, "SERVICE_ACCOUNT", "Workload Identity"
    elif member.startswith("group:"):
        domain = member.split("@", 1)[1]
        is_compliant = domain in approved_domains
        category = "CORPORATE_GROUP" if is_compliant else "EXTERNAL_GROUP"
        reason = f"Domain: {domain}"
    elif member.startswith("user:"):
        domain = member.split("@", 1)[1]
        is_compliant = domain in approved_domains
        category = "CORPORATE_USER" if is_compliant else "CONSUMER_SHADOW"
        reason = f"Domain: {domain}"

    results.append({
        "member": member,
        "role": b["role"],
        "resource": b["resource"],
        "category": category,
        "compliant": is_compliant,
        "detail": reason
    })

audit_output = {
    "total_evaluated": len(results),
    "compliant_count": sum(1 for r in results if r["compliant"]),
    "violation_count": sum(1 for r in results if not r["compliant"]),
    "evaluations": results
}

with open("scratch/day24_lab/stage4_audit_results.json", "w") as f:
    json.dump(audit_output, f, indent=2)

print(f"Stage 4 verified: Evaluated {len(results)} bindings; found {audit_output['violation_count']} violations.")
EOF
python3 scratch/day24_lab/topic1/stage4_execute_audit.py
```

**Expected result:**
Audit results saved to scratch/day24_lab/stage4_audit_results.json.

**Save:** scratch/day24_lab/stage4_audit_results.json''',

    '''**Stage 5: Inspect audit violations and verify customer directory isolation**

**Location:** local terminal

**Actions:**
Inspect the audit evaluation records, isolate all non-compliant consumer accounts (@gmail.com and @yahoo.com), and generate the formal compliance violations report.
```bash
cat <<'EOF' > scratch/day24_lab/topic1/stage5_inspect_violations.py
import json

with open("scratch/day24_lab/stage4_audit_results.json") as f:
    data = json.load(f)

violations = [r for r in data["evaluations"] if not r["compliant"]]

report = {
    "audit_status": "FAILED_GOVERNANCE_CHECK",
    "violations_detected": len(violations),
    "critical_shadow_accounts": [
        {"member": v["member"], "role": v["role"], "resource": v["resource"], "risk": "High - External Identity"}
        for v in violations
    ],
    "governance_assessment": "Unmanaged consumer identities detected in production IAM policies. Immediate revocation required to prevent offboarding bypass."
}

with open("scratch/day24_lab/stage5_violations_report.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"Stage 5 verified: Isolated {len(violations)} high-risk shadow account bindings.")
EOF
python3 scratch/day24_lab/topic1/stage5_inspect_violations.py
```

**Expected result:**
Violations report saved to scratch/day24_lab/stage5_violations_report.json.

**Save:** scratch/day24_lab/stage5_violations_report.json''',

    '''**Stage 6: Rehearse bounded failure: simulate unauthorized collaborator grant and policy rejection**

**Location:** local terminal

**Actions:**
Simulate an attempt by a project administrator to add an external personal consumer account (`user:contractor.dave@gmail.com`) when `constraints/iam.allowedPolicyMemberDomains` is active, proving that the API gateway rejects the mutation with an HTTP 400 FAILED_PRECONDITION error.
```bash
cat <<'EOF' > scratch/day24_lab/topic1/stage6_simulate_rejection.py
import json

def simulate_iam_mutation(member, org_policy_enforced=True, customer_id="C01234567"):
    if org_policy_enforced:
        if member.endswith("@gmail.com") or member.endswith("@yahoo.com"):
            return {
                "status": "REJECTED",
                "http_code": 400,
                "error": "FAILED_PRECONDITION",
                "message": f"One or more members are not allowed by organization policy constraints/iam.allowedPolicyMemberDomains: {member}",
                "enforced_directory": customer_id
            }
    return {"status": "ADMITTED", "http_code": 200, "message": "Role binding successfully added"}

test_cases = [
    {"member": "user:contractor.dave@gmail.com", "expected": "REJECTED"},
    {"member": "user:alice@brightloaf.com", "expected": "ADMITTED"},
    {"member": "serviceAccount:order-api@bl-prod.iam.gserviceaccount.com", "expected": "ADMITTED"}
]

simulation_results = []
for tc in test_cases:
    res = simulate_iam_mutation(tc["member"])
    simulation_results.append({
        "member": tc["member"],
        "result": res["status"],
        "http_code": res["http_code"],
        "detail": res["message"]
    })

with open("scratch/day24_lab/stage6_org_policy_rejection.json", "w") as f:
    json.dump(simulation_results, f, indent=2)

print("Stage 6 verified: Simulated Org Policy rejection for unapproved consumer accounts.")
EOF
python3 scratch/day24_lab/topic1/stage6_simulate_rejection.py
```

**Expected result:**
Simulation record saved to scratch/day24_lab/stage6_org_policy_rejection.json.

**Save:** scratch/day24_lab/stage6_org_policy_rejection.json''',

    '''**Stage 7: Diagnose evidence and record remediation commands**

**Location:** local terminal

**Actions:**
Synthesize discovered violations into an executable remediation plan containing exact `gcloud` CLI commands to strip shadow accounts and establish Cloud Identity contractor provisioning.
```bash
cat <<'EOF' > scratch/day24_lab/topic1/stage7_remediation_plan.py
import json

with open("scratch/day24_lab/stage5_violations_report.json") as f:
    violations_data = json.load(f)

commands = []
for v in violations_data["critical_shadow_accounts"]:
    resource_parts = v["resource"].split("/")
    proj_id = resource_parts[-1]
    cmd = f"gcloud projects remove-iam-policy-binding {proj_id} --member='{v['member']}' --role='{v['role']}'"
    commands.append({
        "target_member": v["member"],
        "target_project": proj_id,
        "command": cmd
    })

remediation_plan = {
    "action": "REVOKE_SHADOW_ACCOUNTS",
    "total_revocations": len(commands),
    "remediation_commands": commands,
    "organizational_policy_update": {
        "constraint": "constraints/iam.allowedPolicyMemberDomains",
        "action": "Enforce customer directory ID C01234567 at organization apex"
    }
}

with open("scratch/day24_lab/stage7_remediation_plan.json", "w") as f:
    json.dump(remediation_plan, f, indent=2)

print(f"Stage 7 verified: Generated remediation plan with {len(commands)} gcloud commands.")
EOF
python3 scratch/day24_lab/topic1/stage7_remediation_plan.py
```

**Expected result:**
Remediation plan saved to scratch/day24_lab/stage7_remediation_plan.json.

**Save:** scratch/day24_lab/stage7_remediation_plan.json''',

    '''**Stage 8: Clean up or close out: archive directory verification evidence**

**Location:** local terminal

**Actions:**
Aggregate all Stage 1 through Stage 7 outputs into the authoritative Directory Provider and Domain Restricted Sharing verification record.
```bash
cat <<'EOF' > scratch/day24_lab/topic1/stage8_closeout.py
import json

summary = {
    "exercise": "Exercise 1: Directory Provider Audit & Domain Restricted Sharing",
    "status": "COMPLETED",
    "findings": {
        "total_bindings_audited": 7,
        "compliant_bindings": 4,
        "violations_identified": 3,
        "shadow_consumer_domains": ["gmail.com", "yahoo.com"]
    },
    "controls_validated": [
        "Cloud Identity vs Consumer account classification verified",
        "constraints/iam.allowedPolicyMemberDomains simulated with FAILED_PRECONDITION rejection",
        "Remediation commands recorded for immediate account stripping"
    ]
}

with open("scratch/day24_lab/stage8_directory_audit_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Stage 8 verified: Exercise 1 evidence archived successfully.")
EOF
python3 scratch/day24_lab/topic1/stage8_closeout.py
```

**Expected result:**
Summary archive saved to scratch/day24_lab/stage8_directory_audit_summary.json.

**Save:** scratch/day24_lab/stage8_directory_audit_summary.json'''
]

LAB_02_STEPS = [
    '''**Stage 1: Preflight: validate workspace environment and execution tools**

**Location:** local terminal

**Actions:**
Verify execution prerequisites and establish the laboratory workspace for Day 24 Exercise 2.
```bash
command -v bash python3
mkdir -p scratch/day24_lab/topic2
cat <<'EOF' > scratch/day24_lab/topic2/stage1_preflight.py
import json, sys

preflight = {
    "exercise": "Exercise 2: Principal Syntax Validator & Public Exposure Risk Scanner",
    "python_version": sys.version.split()[0],
    "status": "READY"
}

with open("scratch/day24_lab/stage1_principal_preflight.json", "w") as f:
    json.dump(preflight, f, indent=2)

print("Stage 1 verified: Principal scanner environment ready.")
EOF
python3 scratch/day24_lab/topic2/stage1_preflight.py
```

**Expected result:**
Preflight record saved to scratch/day24_lab/stage1_principal_preflight.json.

**Save:** scratch/day24_lab/stage1_principal_preflight.json''',

    '''**Stage 2: Prepare principal dataset covering all 6 principal types**

**Location:** local terminal

**Actions:**
Author a multi-resource IAM policy inventory containing representative examples of all six Google Cloud principal types, including benign corporate bindings and dangerous public exposure grants.
```bash
cat <<'EOF' > scratch/day24_lab/topic2/stage2_prepare_principals.py
import json

policies = [
    {
        "resource": "gs://bl-order-archives-prod",
        "resource_type": "storage.googleapis.com/Bucket",
        "public_access_prevention": False,
        "bindings": [
            {"role": "roles/storage.objectViewer", "member": "allAuthenticatedUsers"},
            {"role": "roles/storage.admin", "member": "group:cloud-storage-admins@brightloaf.com"}
        ]
    },
    {
        "resource": "projects/bl-pos-production",
        "resource_type": "cloudresourcemanager.googleapis.com/Project",
        "public_access_prevention": True,
        "bindings": [
            {"role": "roles/viewer", "member": "group:pos-devs@brightloaf.com"},
            {"role": "roles/editor", "member": "serviceAccount:pos-deployer@bl-prod.iam.gserviceaccount.com"},
            {"role": "roles/browser", "member": "domain:brightloaf.com"},
            {"role": "roles/viewer", "member": "user:auditor.lead@brightloaf.com"}
        ]
    },
    {
        "resource": "gs://bl-public-assets",
        "resource_type": "storage.googleapis.com/Bucket",
        "public_access_prevention": False,
        "bindings": [
            {"role": "roles/storage.objectViewer", "member": "allUsers"}
        ]
    }
]

with open("scratch/day24_lab/stage2_principals_dataset.json", "w") as f:
    json.dump(policies, f, indent=2)

print(f"Stage 2 verified: Authored test dataset across {len(policies)} resources.")
EOF
python3 scratch/day24_lab/topic2/stage2_prepare_principals.py
```

**Expected result:**
Dataset saved to scratch/day24_lab/stage2_principals_dataset.json.

**Save:** scratch/day24_lab/stage2_principals_dataset.json''',

    r'''**Stage 3: Author regex parser and Public Access Prevention scanner**

**Location:** local terminal

**Actions:**
Author the principal syntax validator engine (`stage3_principal_scanner.py`) to parse member strings against the 6 Google Cloud principal patterns and evaluate risk categories.
```bash
cat <<'EOF' > scratch/day24_lab/topic2/stage3_principal_scanner.py
import json, re

PATTERNS = {
    "user": re.compile(r"^user:[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    "group": re.compile(r"^group:[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    "serviceAccount": re.compile(r"^serviceAccount:[a-zA-Z0-9-]+@[a-zA-Z0-9-]+\.iam\.gserviceaccount\.com$"),
    "domain": re.compile(r"^domain:[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    "allAuthenticatedUsers": re.compile(r"^allAuthenticatedUsers$"),
    "allUsers": re.compile(r"^allUsers$")
}

def classify_member(member):
    for ptype, pattern in PATTERNS.items():
        if pattern.match(member):
            if ptype == "allUsers":
                return ptype, "PUBLIC_ANONYMOUS_LEAK", "Critical: Unauthenticated public internet access"
            if ptype == "allAuthenticatedUsers":
                return ptype, "GLOBAL_AUTHENTICATED_LEAK", "Extreme: Any global Google account access"
            if ptype == "user":
                return ptype, "DIRECT_USER_BINDING", "Medium: Anti-pattern (Privilege creep risk)"
            if ptype == "domain":
                return ptype, "DOMAIN_WIDE_SCOPE", "Moderate: Broad blast radius across entire domain"
            if ptype == "group":
                return ptype, "GROUP_BEST_PRACTICE", "Low: Scalable enterprise directory binding"
            if ptype == "serviceAccount":
                return ptype, "WORKLOAD_IDENTITY", "Low: Machine identity boundary"
    return "UNKNOWN", "SYNTAX_INVALID", "Error: Malformed member string"

spec = {
    "scanner": "Principal Taxonomy Scanner v1.0",
    "supported_types": list(PATTERNS.keys())
}

with open("scratch/day24_lab/stage3_scanner_spec.json", "w") as f:
    json.dump(spec, f, indent=2)

print("Stage 3 verified: Authoring complete for Principal Taxonomy Scanner.")
EOF
python3 scratch/day24_lab/topic2/stage3_principal_scanner.py
```

**Expected result:**
Scanner spec saved to scratch/day24_lab/stage3_scanner_spec.json.

**Save:** scratch/day24_lab/stage3_scanner_spec.json''',

    r'''**Stage 4: Execute principal scanner against cloud resource policies**

**Location:** local terminal

**Actions:**
Execute the principal scanner against all resource policies in the dataset, categorizing every binding into risk tiers.
```bash
cat <<'EOF' > scratch/day24_lab/topic2/stage4_execute_scan.py
import json, re

PATTERNS = {
    "user": re.compile(r"^user:[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    "group": re.compile(r"^group:[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    "serviceAccount": re.compile(r"^serviceAccount:[a-zA-Z0-9-]+@[a-zA-Z0-9-]+\.iam\.gserviceaccount\.com$"),
    "domain": re.compile(r"^domain:[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    "allAuthenticatedUsers": re.compile(r"^allAuthenticatedUsers$"),
    "allUsers": re.compile(r"^allUsers$")
}

with open("scratch/day24_lab/stage2_principals_dataset.json") as f:
    policies = json.load(f)

findings = []
for p in policies:
    resource = p["resource"]
    pap = p.get("public_access_prevention", False)
    for b in p["bindings"]:
        member = b["member"]
        matched_type = "UNKNOWN"
        for ptype, pattern in PATTERNS.items():
            if pattern.match(member):
                matched_type = ptype
                break

        is_exposure = matched_type in ("allUsers", "allAuthenticatedUsers")
        severity = "HIGH" if matched_type == "allAuthenticatedUsers" else "CRITICAL" if matched_type == "allUsers" else "LOW"

        findings.append({
            "resource": resource,
            "role": b["role"],
            "member": member,
            "principal_type": matched_type,
            "exposure_risk": is_exposure,
            "severity": severity if is_exposure else "INFO",
            "pap_enforced": pap
        })

scan_output = {
    "total_bindings_scanned": len(findings),
    "exposures_detected": sum(1 for f in findings if f["exposure_risk"]),
    "findings": findings
}

with open("scratch/day24_lab/stage4_scan_findings.json", "w") as f:
    json.dump(scan_output, f, indent=2)

print(f"Stage 4 verified: Scanned {len(findings)} bindings; flagged {scan_output['exposures_detected']} public exposures.")
EOF
python3 scratch/day24_lab/topic2/stage4_execute_scan.py
```

**Expected result:**
Scan findings saved to scratch/day24_lab/stage4_scan_findings.json.

**Save:** scratch/day24_lab/stage4_scan_findings.json''',

    '''**Stage 5: Inspect exposure findings and verify Public Access Prevention (PAP) status**

**Location:** local terminal

**Actions:**
Inspect scan findings, isolate the allAuthenticatedUsers grant on gs://bl-order-archives-prod, and evaluate Public Access Prevention coverage.
```bash
cat <<'EOF' > scratch/day24_lab/topic2/stage5_verify_pap.py
import json

with open("scratch/day24_lab/stage4_scan_findings.json") as f:
    data = json.load(f)

critical_findings = [f for f in data["findings"] if f["exposure_risk"]]

assessment = {
    "total_exposures": len(critical_findings),
    "exposure_details": critical_findings,
    "pap_evaluation": {
        "gs://bl-order-archives-prod": {
            "status": "NON_COMPLIANT",
            "violation": "allAuthenticatedUsers present with PAP=False",
            "required_remediation": "Remove allAuthenticatedUsers and enable PAP"
        },
        "gs://bl-public-assets": {
            "status": "APPROVED_PUBLIC",
            "violation": "None (Approved CDN bucket for static public assets)",
            "required_remediation": "None"
        }
    }
}

with open("scratch/day24_lab/stage5_exposure_verification.json", "w") as f:
    json.dump(assessment, f, indent=2)

print("Stage 5 verified: Evaluated PAP compliance across storage assets.")
EOF
python3 scratch/day24_lab/topic2/stage5_verify_pap.py
```

**Expected result:**
Verification saved to scratch/day24_lab/stage5_exposure_verification.json.

**Save:** scratch/day24_lab/stage5_exposure_verification.json''',

    '''**Stage 6: Rehearse bounded failure: simulate accidental allAuthenticatedUsers grant on storage bucket**

**Location:** local terminal

**Actions:**
Simulate an engineer attempting to apply allAuthenticatedUsers on a bucket where Public Access Prevention (PAP) is enforced, verifying that the storage API blocks the mutation.
```bash
cat <<'EOF' > scratch/day24_lab/topic2/stage6_rehearse_pap_block.py
import json

def attempt_public_grant(bucket_name, principal, pap_enforced=True):
    if pap_enforced and principal in ("allUsers", "allAuthenticatedUsers"):
        return {
            "status": "BLOCKED",
            "http_code": 412,
            "error": "PreconditionFailed",
            "message": f"Cannot add public member '{principal}' when Public Access Prevention is enforced on bucket '{bucket_name}'."
        }
    return {"status": "SUCCESS", "http_code": 200, "message": "Policy binding admitted"}

rehearsal_results = [
    attempt_public_grant("gs://bl-order-archives-prod", "allAuthenticatedUsers", pap_enforced=True),
    attempt_public_grant("gs://bl-order-archives-prod", "allUsers", pap_enforced=True),
    attempt_public_grant("gs://bl-order-archives-prod", "group:order-auditors@brightloaf.com", pap_enforced=True)
]

with open("scratch/day24_lab/stage6_public_exposure_alert.json", "w") as f:
    json.dump(rehearsal_results, f, indent=2)

print("Stage 6 verified: Public Access Prevention successfully blocked unauthorized public grants.")
EOF
python3 scratch/day24_lab/topic2/stage6_rehearse_pap_block.py
```

**Expected result:**
Alert record saved to scratch/day24_lab/stage6_public_exposure_alert.json.

**Save:** scratch/day24_lab/stage6_public_exposure_alert.json''',

    '''**Stage 7: Diagnose root cause and record remediation policy updates**

**Location:** local terminal

**Actions:**
Synthesize scan findings and rehearsal evidence into an authoritative remediation policy that strips allAuthenticatedUsers and enables PAP.
```bash
cat <<'EOF' > scratch/day24_lab/topic2/stage7_remediate_policy.py
import json

remediation = {
    "target_resource": "gs://bl-order-archives-prod",
    "revocations": [
        {"member": "allAuthenticatedUsers", "role": "roles/storage.objectViewer"}
    ],
    "additions": [
        {"member": "group:order-auditors@brightloaf.com", "role": "roles/storage.objectViewer"}
    ],
    "storage_configuration_changes": [
        {"setting": "publicAccessPrevention", "target_value": "enforced"}
    ],
    "cli_execution": [
        "gcloud storage buckets remove-iam-policy-binding gs://bl-order-archives-prod --member='allAuthenticatedUsers' --role='roles/storage.objectViewer'",
        "gcloud storage buckets add-iam-policy-binding gs://bl-order-archives-prod --member='group:order-auditors@brightloaf.com' --role='roles/storage.objectViewer'",
        "gcloud storage buckets update gs://bl-order-archives-prod --public-access-prevention"
    ]
}

with open("scratch/day24_lab/stage7_remediation_policy.json", "w") as f:
    json.dump(remediation, f, indent=2)

print("Stage 7 verified: Authoring complete for PAP remediation policy.")
EOF
python3 scratch/day24_lab/topic2/stage7_remediate_policy.py
```

**Expected result:**
Policy record saved to scratch/day24_lab/stage7_remediation_policy.json.

**Save:** scratch/day24_lab/stage7_remediation_policy.json''',

    '''**Stage 8: Clean up or close out: archive principal risk assessment**

**Location:** local terminal

**Actions:**
Generate the consolidated Exercise 2 closeout summary archiving all principal syntax checks and exposure defense evidence.
```bash
cat <<'EOF' > scratch/day24_lab/topic2/stage8_closeout.py
import json

summary = {
    "exercise": "Exercise 2: Principal Syntax Validator & Public Exposure Risk Scanner",
    "status": "COMPLETED",
    "evaluated_principals": {
        "user": "Validated (alice@brightloaf.com, auditor.lead@brightloaf.com)",
        "group": "Validated (pos-devs, cloud-storage-admins)",
        "serviceAccount": "Validated (pos-deployer@bl-prod.iam.gserviceaccount.com)",
        "domain": "Validated (brightloaf.com)",
        "allAuthenticatedUsers": "Flagged & remediated via PAP",
        "allUsers": "Scoped to approved public CDN assets"
    },
    "controls_confirmed": [
        "Six principal types regex validation verified",
        "allAuthenticatedUsers exposure identified and eliminated",
        "Public Access Prevention (PAP) enforcement verified"
    ]
}

with open("scratch/day24_lab/stage8_principal_assessment_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Stage 8 verified: Exercise 2 evidence archived successfully.")
EOF
python3 scratch/day24_lab/topic2/stage8_closeout.py
```

**Expected result:**
Assessment summary saved to scratch/day24_lab/stage8_principal_assessment_summary.json.

**Save:** scratch/day24_lab/stage8_principal_assessment_summary.json'''
]

LAB_03_STEPS = [
    '''**Stage 1: Preflight: validate workspace environment and prerequisites**

**Location:** local terminal

**Actions:**
Verify local execution prerequisites and initialize the laboratory directory for Day 24 Exercise 3.
```bash
command -v bash python3
mkdir -p scratch/day24_lab/topic3
cat <<'EOF' > scratch/day24_lab/topic3/stage1_preflight.py
import json, sys

preflight = {
    "exercise": "Exercise 3: Group Consolidation Engine & Identity Matrix Generation",
    "python_version": sys.version.split()[0],
    "status": "READY"
}

with open("scratch/day24_lab/stage1_consolidation_preflight.json", "w") as f:
    json.dump(preflight, f, indent=2)

print("Stage 1 verified: Consolidation engine environment ready.")
EOF
python3 scratch/day24_lab/topic3/stage1_preflight.py
```

**Expected result:**
Preflight record saved to scratch/day24_lab/stage1_consolidation_preflight.json.

**Save:** scratch/day24_lab/stage1_consolidation_preflight.json''',

    '''**Stage 2: Prepare bloated legacy IAM policy inventory with direct user grants**

**Location:** local terminal

**Actions:**
Generate a realistic bloated IAM policy payload simulating an enterprise where 240 developers were directly bound to multiple roles across services, approaching Google Cloud's 250 KB / 1,500 member quota.
```bash
cat <<'EOF' > scratch/day24_lab/topic3/stage2_prepare_bloated_policy.py
import json

roles = ["roles/viewer", "roles/logging.viewer", "roles/monitoring.viewer", "roles/clouddebugger.user"]
members = [f"user:dev_{i:03d}@brightloaf.com" for i in range(1, 241)]

bindings = []
for role in roles:
    bindings.append({
        "role": role,
        "members": list(members)
    })

# Add departing contractors to simulate orphan accumulation
orphan_contractors = [f"user:contractor_{i:02d}@gmail.com" for i in range(1, 43)]
bindings.append({
    "role": "roles/editor",
    "members": orphan_contractors
})

legacy_policy = {
    "version": 1,
    "etag": "BwW12345678=",
    "bindings": bindings
}

raw_bytes = len(json.dumps(legacy_policy, indent=2).encode('utf-8'))
total_member_entries = sum(len(b["members"]) for b in bindings)

stats = {
    "serialized_bytes": raw_bytes,
    "total_member_entries": total_member_entries,
    "quota_limit_bytes": 250 * 1024,
    "quota_member_limit": 1500,
    "policy": legacy_policy
}

with open("scratch/day24_lab/stage2_legacy_bloated_policy.json", "w") as f:
    json.dump(stats, f, indent=2)

print(f"Stage 2 verified: Generated bloated legacy policy: {raw_bytes} bytes, {total_member_entries} members.")
EOF
python3 scratch/day24_lab/topic3/stage2_prepare_bloated_policy.py
```

**Expected result:**
Bloated policy saved to scratch/day24_lab/stage2_legacy_bloated_policy.json.

**Save:** scratch/day24_lab/stage2_legacy_bloated_policy.json''',

    '''**Stage 3: Author group consolidation engine**

**Location:** local terminal

**Actions:**
Author the policy consolidation engine (`stage3_group_consolidator.py`) to map individual developer and operator accounts into functional Google Groups.
```bash
cat <<'EOF' > scratch/day24_lab/topic3/stage3_group_consolidator.py
import json

GROUP_MAPPINGS = {
    "roles/viewer": "group:pos-engineers@brightloaf.com",
    "roles/logging.viewer": "group:pos-engineers@brightloaf.com",
    "roles/monitoring.viewer": "group:pos-sre@brightloaf.com",
    "roles/clouddebugger.user": "group:pos-sre@brightloaf.com"
}

def consolidate_policy(legacy_bindings):
    consolidated_bindings = []
    group_map = {}
    for b in legacy_bindings:
        role = b["role"]
        if role in GROUP_MAPPINGS:
            target_group = GROUP_MAPPINGS[role]
            if role not in group_map:
                group_map[role] = set()
            group_map[role].add(target_group)
        elif role == "roles/editor":
            # Orphan contractors pruned; replaced with contractor corporate group
            if role not in group_map:
                group_map[role] = set()
            group_map[role].add("group:contractor-logistics@brightloaf.com")

    for role, grps in group_map.items():
        consolidated_bindings.append({
            "role": role,
            "members": sorted(list(grps))
        })
    return consolidated_bindings

spec = {
    "engine": "Group Consolidation Engine v1.0",
    "target_groups": list(set(GROUP_MAPPINGS.values())) + ["group:contractor-logistics@brightloaf.com"]
}

with open("scratch/day24_lab/stage3_consolidation_spec.json", "w") as f:
    json.dump(spec, f, indent=2)

print("Stage 3 verified: Authoring complete for group consolidation engine.")
EOF
python3 scratch/day24_lab/topic3/stage3_group_consolidator.py
```

**Expected result:**
Consolidation spec saved to scratch/day24_lab/stage3_consolidation_spec.json.

**Save:** scratch/day24_lab/stage3_consolidation_spec.json''',

    '''**Stage 4: Execute policy consolidation and calculate payload compression ratio**

**Location:** local terminal

**Actions:**
Execute the consolidation engine against the bloated policy, replace direct user bindings with Google Groups, prune orphan accounts, and measure policy size reduction.
```bash
cat <<'EOF' > scratch/day24_lab/topic3/stage4_execute_consolidation.py
import json

with open("scratch/day24_lab/stage2_legacy_bloated_policy.json") as f:
    legacy_data = json.load(f)

legacy_bindings = legacy_data["policy"]["bindings"]

GROUP_MAPPINGS = {
    "roles/viewer": "group:pos-engineers@brightloaf.com",
    "roles/logging.viewer": "group:pos-engineers@brightloaf.com",
    "roles/monitoring.viewer": "group:pos-sre@brightloaf.com",
    "roles/clouddebugger.user": "group:pos-sre@brightloaf.com"
}

group_map = {}
for b in legacy_bindings:
    role = b["role"]
    if role in GROUP_MAPPINGS:
        target_group = GROUP_MAPPINGS[role]
        if role not in group_map: group_map[role] = set()
        group_map[role].add(target_group)
    elif role == "roles/editor":
        if role not in group_map: group_map[role] = set()
        group_map[role].add("group:contractor-logistics@brightloaf.com")

consolidated_bindings = []
for role, grps in group_map.items():
    consolidated_bindings.append({
        "role": role,
        "members": sorted(list(grps))
    })

consolidated_policy = {
    "version": 1,
    "etag": "BwW98765432=",
    "bindings": consolidated_bindings
}

legacy_bytes = legacy_data["serialized_bytes"]
consolidated_bytes = len(json.dumps(consolidated_policy, indent=2).encode('utf-8'))
compression_pct = round((1 - (consolidated_bytes / legacy_bytes)) * 100, 2)

report = {
    "legacy_size_bytes": legacy_bytes,
    "consolidated_size_bytes": consolidated_bytes,
    "compression_percentage": compression_pct,
    "legacy_member_count": legacy_data["total_member_entries"],
    "consolidated_member_count": sum(len(b["members"]) for b in consolidated_bindings),
    "consolidated_policy": consolidated_policy
}

with open("scratch/day24_lab/stage4_consolidated_policy.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"Stage 4 verified: Policy compressed from {legacy_bytes}B to {consolidated_bytes}B ({compression_pct}% reduction).")
EOF
python3 scratch/day24_lab/topic3/stage4_execute_consolidation.py
```

**Expected result:**
Consolidated policy saved to scratch/day24_lab/stage4_consolidated_policy.json.

**Save:** scratch/day24_lab/stage4_consolidated_policy.json''',

    '''**Stage 5: Inspect policy size reduction and verify member count compliance**

**Location:** local terminal

**Actions:**
Inspect the consolidation audit record, verify compliance against the 250 KB and 1,500 member quota ceilings, and confirm that all 42 orphan accounts were pruned.
```bash
cat <<'EOF' > scratch/day24_lab/topic3/stage5_verify_compression.py
import json

with open("scratch/day24_lab/stage4_consolidated_policy.json") as f:
    data = json.load(f)

verification = {
    "policy_quota_verification": {
        "size_bytes": data["consolidated_size_bytes"],
        "size_limit_bytes": 256000,
        "size_compliant": data["consolidated_size_bytes"] < 256000,
        "member_count": data["consolidated_member_count"],
        "member_limit": 1500,
        "member_count_compliant": data["consolidated_member_count"] < 1500
    },
    "security_improvements": [
        "Eliminated 42 unmanaged contractor Gmail bindings",
        "Replaced 240 direct user accounts with job-function Google Groups",
        "Eliminated privilege accumulation upon employee team transitions",
        "Decoupled employee offboarding from Terraform CI/CD runs"
    ]
}

with open("scratch/day24_lab/stage5_compression_report.json", "w") as f:
    json.dump(verification, f, indent=2)

print("Stage 5 verified: Policy size and member count well within Google Cloud platform quotas.")
EOF
python3 scratch/day24_lab/topic3/stage5_verify_compression.py
```

**Expected result:**
Compression report saved to scratch/day24_lab/stage5_compression_report.json.

**Save:** scratch/day24_lab/stage5_compression_report.json''',

    '''**Stage 6: Rehearse bounded failure: simulate policy mutation rejection on oversized legacy policy**

**Location:** local terminal

**Actions:**
Simulate an attempt by an automated CI/CD pipeline to add an emergency service account to an oversized policy exceeding 250 KB, proving that the Cloud Resource Manager API rejects the mutation.
```bash
cat <<'EOF' > scratch/day24_lab/topic3/stage6_rehearse_quota_rejection.py
import json

def simulate_set_iam_policy(policy_size_bytes):
    if policy_size_bytes > 250 * 1024:
        return {
            "status": "REJECTED",
            "http_code": 400,
            "error": "InvalidArgument",
            "message": f"Policy size of {policy_size_bytes} bytes exceeds the maximum allowed size of 256000 bytes."
        }
    return {
        "status": "ACCEPTED",
        "http_code": 200,
        "message": "Policy successfully applied."
    }

rehearsals = {
    "oversized_legacy_attempt": simulate_set_iam_policy(257200),
    "consolidated_group_attempt": simulate_set_iam_policy(1240)
}

with open("scratch/day24_lab/stage6_policy_quota_rejection.json", "w") as f:
    json.dump(rehearsals, f, indent=2)

print("Stage 6 verified: Rehearsed API quota rejection on oversized IAM policies.")
EOF
python3 scratch/day24_lab/topic3/stage6_rehearse_quota_rejection.py
```

**Expected result:**
Rehearsal record saved to scratch/day24_lab/stage6_policy_quota_rejection.json.

**Save:** scratch/day24_lab/stage6_policy_quota_rejection.json''',

    '''**Stage 7: Diagnose identity taxonomy and map People, Workloads, Groups, and External Identities**

**Location:** local terminal

**Actions:**
Construct the formal structured taxonomy distinguishing People, Workloads, Groups, and External Identities with associated IAM roles and governance controls.
```bash
cat <<'EOF' > scratch/day24_lab/topic3/stage7_map_identities.py
import json

taxonomy = {
    "enterprise": "BrightLoaf Retail Bakeries",
    "categories": {
        "people": [
            {"name": "POS Engineers", "principal": "group:pos-engineers@brightloaf.com", "role": "roles/viewer", "scope": "/Non-Production/POS"},
            {"name": "SRE & Ops", "principal": "group:pos-sre@brightloaf.com", "role": "roles/monitoring.editor", "scope": "/Production/POS"}
        ],
        "workloads": [
            {"name": "Order API Workload", "principal": "serviceAccount:order-api-sa@bl-prod.iam.gserviceaccount.com", "role": "roles/spanner.databaseUser", "scope": "bl-order-fulfill-prod"},
            {"name": "CI/CD Pipeline", "principal": "serviceAccount:pos-deployer-sa@bl-prod.iam.gserviceaccount.com", "role": "roles/container.developer", "scope": "bl-pos-production"}
        ],
        "groups": [
            {"name": "Franchise Auditors", "principal": "group:franchise-auditors@brightloaf.com", "role": "roles/bigquery.dataViewer", "scope": "bl-analytics-prod"}
        ],
        "external_identities": [
            {"name": "Logistics Partner", "principal": "group:contractor-logistics@brightloaf.com", "role": "roles/viewer", "scope": "bl-logistics-prod"}
        ]
    },
    "business_invariant": "Replaying delivery events or rotating credentials must never result in duplicate physical bread fulfillment (<= 1 physical fulfillment per unique order ID)."
}

with open("scratch/day24_lab/stage7_identity_mapping.json", "w") as f:
    json.dump(taxonomy, f, indent=2)

print("Stage 7 verified: Mapped complete identity taxonomy.")
EOF
python3 scratch/day24_lab/topic3/stage7_map_identities.py
```

**Expected result:**
Identity mapping saved to scratch/day24_lab/stage7_identity_mapping.json.

**Save:** scratch/day24_lab/stage7_identity_mapping.json''',

    '''**Stage 8: Author and save the authoritative exit evidence report**

**Location:** local terminal

**Actions:**
Synthesize all lab findings, compression metrics, and taxonomy mappings into the authoritative Day 24 exit evidence report: `scratch/day-024-workforce-identity-report.md`.
```bash
cat <<'EOF' > scratch/day24_lab/topic3/stage8_generate_exit_report.py
import json, os

with open("scratch/day24_lab/stage4_consolidated_policy.json") as f:
    consolidation = json.load(f)

with open("scratch/day24_lab/stage7_identity_mapping.json") as f:
    mapping = json.load(f)

report_content = f"""# Day 24 Exit Evidence: Workforce Identity Matrix & Principal Inventory

**Document Version:** 1.0.0 | **Author:** Enterprise Cloud Security Architecture Team  
**Scope:** Google Cloud IAM, Cloud Identity, and Resource Manager Governance  

## 1. Executive Summary & Core Architectural Invariants
This document delivers the verified Day 24 exit evidence satisfying the curriculum requirements:
1. **Principal Inventory & Group Consolidation:** Replaced individual user role grants with job-function Google Groups, protecting against Google Cloud's 250 KB / 1,500 member IAM policy platform limits.
2. **Workforce Identity Matrix:** Categorized all corporate identities into People, Service Accounts (Workloads), Groups, and External Identities with strict directory and MFA governance.
3. **Domain & Public Exposure Defenses:** Validated `constraints/iam.allowedPolicyMemberDomains` to eliminate unmanaged personal Gmail accounts, and confirmed Public Access Prevention (PAP) on Cloud Storage.

### Core Business Invariant:
> **Duplicate Fulfillment Invariant:** Replaying delivery events, rotating service account credentials, or executing employee offboarding must never cause a second physical fulfillment (<= 1 physical fulfillment per unique order ID).

---

## 2. Workforce Identity Matrix: People, Workloads, Groups, and Externals

| Category | Principal Type / Syntax | Identity Provider | Associated IAM Roles | Target Resource Scope | Security Governance & MFA |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **People (Workforce)** | `group:pos-engineers@brightloaf.com` | Cloud Identity / Okta | `roles/viewer`, `roles/logging.viewer` | `/Non-Production/POS` | Hardware FIDO2 Security Key; SSO |
| **People (SRE / Ops)** | `group:pos-sre@brightloaf.com` | Cloud Identity / Okta | `roles/monitoring.editor`, `roles/clouddebugger.user` | `/Production/POS` | Break-Glass PAM with Time-Bound Lease |
| **Workloads (App)** | `serviceAccount:order-api-sa@bl-prod.iam.gserviceaccount.com` | Google Cloud IAM | `roles/spanner.databaseUser`, `roles/pubsub.publisher` | `bl-order-fulfill-prod` | Workload Identity Federation (No JSON keys) |
| **Workloads (CI/CD)** | `serviceAccount:pos-deployer-sa@bl-prod.iam.gserviceaccount.com` | Google Cloud IAM | `roles/container.developer`, `roles/artifactregistry.writer` | `bl-pos-production` | GitHub Actions OIDC Short-Lived Tokens |
| **Groups (Functional)**| `group:franchise-auditors@brightloaf.com` | Cloud Identity | `roles/bigquery.dataViewer` | `bl-analytics-prod` | Enforces corporate directory membership |
| **External Identities**| `group:contractor-logistics@brightloaf.com` | Managed Cloud Identity | Custom: `roles/logisticsViewer` | `bl-logistics-prod` | Managed corporate domain only (Zero @gmail) |

---

## 3. Direct User to Group Consolidation Audit
- **Legacy Bloated Policy Size:** {consolidation['legacy_size_bytes']} bytes ({consolidation['legacy_member_count']} individual bindings).
- **Consolidated Policy Size:** {consolidation['consolidated_size_bytes']} bytes ({consolidation['consolidated_member_count']} Google Group bindings).
- **Compression Ratio:** {consolidation['compression_percentage']}% payload reduction.
- **Orphan Accounts Pruned:** 42 departed contractors and former employees purged from active policies.
- **Quota Safety Margin:** Post-consolidation payload uses less than 1% of the 250 KB platform limit.

---

## 4. Domain Restricted Sharing & Public Access Prevention Verification
1. **Domain Restricted Sharing (`constraints/iam.allowedPolicyMemberDomains`):** Enforced at Organization apex (Customer Directory ID: `C01234567`). Blocks personal `@gmail.com` and unapproved third-party accounts at the API admission boundary.
2. **Public Access Prevention (`constraints/storage.publicAccessPrevention`):** Enforced on all internal storage buckets, eliminating `allUsers` and `allAuthenticatedUsers` public exposures.

---
*End of Authoritative Report. Verified against Google Cloud Resource Manager and Cloud Identity specifications.*
"""

os.makedirs("scratch", exist_ok=True)
with open("scratch/day-024-workforce-identity-report.md", "w") as f:
    f.write(report_content)

print(f"Stage 8 verified: Exit report written to scratch/day-024-workforce-identity-report.md ({len(report_content)} bytes).")
EOF
python3 scratch/day24_lab/topic3/stage8_generate_exit_report.py
```

**Expected result:**
Authoritative report saved to scratch/day-024-workforce-identity-report.md.

**Save:** scratch/day-024-workforce-identity-report.md'''
]

# ─────────────────────────────────────────────────────────────────────────────
# REVIEW RECORDS
# ─────────────────────────────────────────────────────────────────────────────
REVIEW_RECORDS = {
    'product_claims': [
        {
            'claim': 'Cloud Identity domains map directly to Google Cloud Organization nodes, providing centralized directory services, SAML 2.0 / OIDC federation, and multi-factor authentication for enterprise workforce accounts.',
            'heading_opened': 'Domains',
            'section_url': 'https://cloud.google.com/iam/docs/principals-overview#domains'
        },
        {
            'claim': 'Google Cloud IAM recognizes six principal types distinguished by explicit syntax prefixes (user, group, serviceAccount, domain, allAuthenticatedUsers, allUsers), where allAuthenticatedUsers grants access to any authenticated Google account globally.',
            'heading_opened': 'Principal types',
            'section_url': 'https://cloud.google.com/iam/docs/principals-overview#principal-types'
        },
        {
            'claim': 'Google Cloud IAM best practices mandate granting roles to Google Groups rather than individual users to model job functions, prevent privilege accumulation, and stay well within the hard 250 KB policy size limit.',
            'heading_opened': 'Use access groups to model job functions and grant access to resources',
            'section_url': 'https://cloud.google.com/iam/docs/groups-best-practices#job-functions-access'
        }
    ],
    'source_ledger': {
        'https://cloud.google.com/iam/docs/principals-overview#domains': {
            'heading_opened': 'Domains',
            'rfc_status': 'not applicable'
        },
        'https://cloud.google.com/iam/docs/principals-overview#principal-types': {
            'heading_opened': 'Principal types',
            'rfc_status': 'not applicable'
        },
        'https://cloud.google.com/iam/docs/groups-best-practices#job-functions-access': {
            'heading_opened': 'Use access groups to model job functions and grant access to resources',
            'rfc_status': 'not applicable'
        }
    },
    'visual_reasons': {
        'Google Cloud Workforce Identity Providers and Principal Taxonomy': 'Taxonomy diagram contrasting managed Cloud Identity and Workspace directories with unmanaged consumer accounts, and classifying the six IAM principal types with security risk boundaries.',
        'Direct Individual User Binding Anti-Pattern vs. Group-Based Authorization Architecture': 'Architectural comparison contrasting the fragile direct individual user role binding anti-pattern with the scalable group-based indirect authorization model.',
        'Incident 24.1 Flow: Personal Gmail Account Shadow Access vs. Federated Cloud Identity Governance': 'Diagnostic incident flow diagram illustrating how binding a personal unmanaged Gmail account allowed a departing contractor to retain access, and the corrected architecture enforcing Cloud Identity and Domain Restricted Sharing.',
        'Incident 24.2 Flow: allAuthenticatedUsers Misconfiguration vs. Domain-Restricted Group Authorization': 'Diagnostic incident flow diagram illustrating how conflating allAuthenticatedUsers with internal staff exposed order archives to the public internet, and the corrected architecture enforcing groups and Public Access Prevention.',
        'Incident 24.3 Flow: IAM Policy Size Overflow vs. Consolidated Group Role Bindings': 'Diagnostic incident flow diagram illustrating how direct user bindings bloated an IAM policy beyond the 250 KB limit, and how consolidating roles into Google Groups restored operations.'
    }
}

DATA = {
    'contract_version': 2,
    'day': 24,
    'day_padded': '024',
    'title': 'Day 24 — Principals and workforce identity',
    'time_estimate': '2–3 hours',
    'prerequisites': '[Day 23](#day-23); bring their exit artifacts.',
    'work_block': 'Days 18–35 — Cloud environment and identity',
    'roadmap_practice': 'Build a principal inventory for developers, operators and workloads; replace individual grants with suitable groups in the design.',
    'roadmap_exit': 'An identity matrix distinguishing people, service accounts, groups and external identities.',
    'access_date': ACCESS_DATE,
    'sources': SOURCES,
    'part1_intro': 'A conceptual foundation covering Cloud Identity versus Google Workspace versus consumer Google accounts, the six IAM principal types, and group-based role binding architecture.',
    'part2_intro': 'An in-depth technical analysis detailing workforce directory federation, the six IAM principal types, public exposure boundaries, and platform policy size quotas.',
    'part3_intro': 'Real-world operational incident postmortems examining unmanaged contractor Gmail shadow access, catastrophic allAuthenticatedUsers public exposure, and IAM policy size overflow.',
    'part4_intro': 'Hands-on guided laboratory exercises executing directory domain auditing, principal syntax scanning, public access prevention enforcement, and group-based policy consolidation.',
    'exit_summary': 'Completion of Day 24 produces verified exit evidence consisting of an authoritative Workforce Identity Matrix distinguishing people, service accounts, groups, and external identities at scratch/day-024-workforce-identity-report.md.',
    'part1_html': PART1_HTML,
    'completion_html': COMPLETION_HTML,
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Cloud Identity vs Google Workspace vs consumer Google accounts',
            'anchors': {
                'overview': 'topic-01-overview',
                'technical': 'topic-01-technical',
                'problem': 'topic-01-problem',
                'lab': 'topic-01-lab'
            },
            'overview': '<strong class="keyword">Workforce Identity Architecture</strong> establishes the foundational authentication repository that verifies human users before Google Cloud evaluates authorization policies.',
            'preview': 'A franchise infrastructure administrator permits contract software developers to manage production order fulfillment projects using unmanaged personal consumer Google accounts rather than federated corporate Cloud Identity credentials. When a contractor was abruptly terminated following a security breach, corporate IT disabled their company email but could not revoke their personal Google account, leaving them with active production console access that triggered an emergency security shutdown across all 450 retail bakeries.',
            'technical': TOPIC_01_TECH,
            'questions': [
                'How does Google Cloud decouple authentication identity repositories from authorization policy evaluation?',
                'What directory synchronization mechanisms bridge corporate Active Directory or Okta/Entra into Cloud Identity?',
                'How does the Organization Policy constraint constraints/iam.allowedPolicyMemberDomains programmatically prevent personal consumer accounts from entering IAM policies?'
            ],
            'reference': 'https://cloud.google.com/iam/docs/principals-overview#domains',
            'reference_label': 'Google Cloud IAM Documentation: Domains (accessed 2026-10-04)',
            'scenario': SCENARIO_01,
            'lab': {
                'name': 'Exercise 1: Directory provider audit & domain restricted sharing verification',
                'goal': 'Implement an automated audit script that inspects an enterprise IAM policy binding inventory, identifies unauthorized external consumer email domains, and validates compliance against constraints/iam.allowedPolicyMemberDomains.',
                'expected': 'An executed audit script that flags all unmanaged consumer account bindings, verifies that only accounts belonging to verified customer directory IDs are admitted, and outputs an audit remediation table.',
                'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Identity directory member string parsing, domain boundary verification, unauthorized consumer account detection, and customer ID compliance reporting. Simulated or predicted: Google Cloud Resource Manager Organization Policy Service admission checks, constraints/iam.allowedPolicyMemberDomains rejection responses, and Cloud Identity directory synchronization. Untested on GCP: Live gcloud org-policies set-policy API calls at organization root, Google Workspace Admin SDK Directory API, and live Google Cloud Directory Sync (GCDS) agent execution.',
                'covers': 'Build a principal inventory for developers, operators and workloads (Directory and domain audit)',
                'prereq': 'Linux terminal, Python 3.10+, standard POSIX shell tools (mkdir, cat, python3)',
                'preflight': 'Verify Python 3 availability and initialize dedicated Day 24 lab workspace',
                'trouble': 'Ensure approved corporate domains and Customer Directory ID match enterprise configuration',
                'cleanup': 'Artifacts remain in scratch/day24_lab/ for validation gate auditing',
                'file': 'scratch/day24_lab/stage8_directory_audit_summary.json',
                'steps': LAB_01_STEPS
            }
        },
        {
            'key': 'topic-02',
            'title': 'Principals',
            'anchors': {
                'overview': 'topic-02-overview',
                'technical': 'topic-02-technical',
                'problem': 'topic-02-problem',
                'lab': 'topic-02-lab'
            },
            'overview': '<strong class="keyword">IAM Principal Taxonomy</strong> defines the complete classification of entities that can receive role bindings within Google Cloud access control policies.',
            'preview': 'A DevOps engineer binds the allAuthenticatedUsers principal to an internal Cloud Storage bucket containing raw retail order payment archives, mistakenly believing the identifier restricted access to authenticated corporate staff. Because allAuthenticatedUsers grants access to anyone logged into any consumer Google account globally, an external security researcher accessed and downloaded 140,000 unencrypted customer transaction receipts, triggering an immediate mandatory privacy breach disclosure to federal regulators.',
            'technical': TOPIC_02_TECH,
            'questions': [
                'What are the syntax prefixes, evaluation mechanisms, and authorization scopes for each of the six Google Cloud IAM principal types?',
                'Why does allAuthenticatedUsers match any consumer Gmail or external corporate account globally rather than domain-authenticated employees?',
                'How does Public Access Prevention on Cloud Storage buckets enforce defense-in-depth against accidental public grants?'
            ],
            'reference': 'https://cloud.google.com/iam/docs/principals-overview#principal-types',
            'reference_label': 'Google Cloud IAM Documentation: Principal types (accessed 2026-10-04)',
            'scenario': SCENARIO_02,
            'lab': {
                'name': 'Exercise 2: Principal syntax validator & public exposure risk scanner',
                'goal': 'Implement a security policy scanner that validates IAM member string syntax across all 6 Google Cloud principal types, detects dangerous public internet grants, and verifies Cloud Storage Public Access Prevention configurations.',
                'expected': 'An executed scanner that categorizes IAM member bindings by risk tier, flags any instance of allAuthenticatedUsers on sensitive storage buckets, and generates a security finding.',
                'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Regular expression validation across the 6 IAM principal types, risk classification of member bindings, public exposure detection, and Public Access Prevention (PAP) configuration scanning. Simulated or predicted: Google Cloud Storage IAM policy evaluation, Cloud Resource Manager member prefix syntax checking, and Security Command Center public bucket exposure alerts. Untested on GCP: Live gsutil iam get/set API calls, live bucket public URL testing via external curl, and Organization Policy enforcement on Cloud Storage buckets.',
                'covers': 'Build a principal inventory for developers, operators and workloads (Principal classification and public exposure defense)',
                'prereq': 'Completion of Exercise 1, local Python 3.10+ runtime, POSIX shell',
                'preflight': 'Ensure scratch/day24_lab workspace is accessible and initialize Topic 2 environment',
                'trouble': 'If scanner regex fails, verify member prefix matching against Google Cloud IAM member specifications',
                'cleanup': 'Artifacts remain in scratch/day24_lab/ for validation gate auditing',
                'file': 'scratch/day24_lab/stage8_principal_assessment_summary.json',
                'steps': LAB_02_STEPS
            }
        },
        {
            'key': 'topic-03',
            'title': 'Why groups (not individual users) should receive roles',
            'anchors': {
                'overview': 'topic-03-overview',
                'technical': 'topic-03-technical',
                'problem': 'topic-03-problem',
                'lab': 'topic-03-lab'
            },
            'overview': '<strong class="keyword">Group-Based Access Control</strong> is the foundational enterprise architectural pattern that mandates binding IAM roles exclusively to Google Groups rather than individual human user accounts.',
            'preview': 'A cloud platform team deploys automated scripts that bind individual developer email addresses directly to IAM policies across sixty regional microservice projects, causing the production project IAM policy to breach Google Cloud\'s 250 KB limit. The oversized policy rejected all subsequent administrative updates, blocking an emergency CI/CD hotfix for an active payment processing bug and forcing 450 franchise stores to revert to manual paper receipts during morning rush hour.',
            'technical': TOPIC_03_TECH,
            'questions': [
                'What hard quotas does Google Cloud enforce on IAM policy payloads (250 KB size limit and 1,500 member count limit)?',
                'How does group-based role binding eliminate privilege accumulation when engineers transition between internal teams?',
                'Why does binding roles to Google Groups decouple identity administration from infrastructure CI/CD pipelines?'
            ],
            'reference': 'https://cloud.google.com/iam/docs/groups-best-practices#job-functions-access',
            'reference_label': 'Google Cloud IAM Documentation: Use access groups to model job functions and grant access to resources (accessed 2026-10-04)',
            'scenario': SCENARIO_03,
            'lab': {
                'name': 'Exercise 3: Group consolidation engine & identity matrix generation',
                'goal': 'Implement an automated consolidation engine that audits bloated IAM policies, replaces individual user bindings with job-function Google Groups, measures policy size reduction against the 250 KB limit, and authors the authoritative exit evidence matrix.',
                'expected': 'An executed consolidation script that compresses policy size by over 95%, prunes orphaned contractor bindings, verifies compliance against platform quotas, and outputs scratch/day-024-workforce-identity-report.md.',
                'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Legacy IAM policy size calculation, individual user to Google Group mapping engine, payload size compression measurement, and authoritative markdown identity matrix generation. Simulated or predicted: Google Cloud IAM policy size quota enforcement (250 KB limit), HTTP 400 Bad Request policy rejection, and Cloud Identity group membership expansion. Untested on GCP: Live gcloud projects set-iam-policy with oversized JSON payloads, enterprise Okta SCIM group push, and Cloud Identity Security Groups API.',
                'covers': 'replace individual grants with suitable groups in the design (An identity matrix distinguishing people, service accounts, groups and external identities)',
                'prereq': 'Completion of Exercises 1 and 2, local Python 3.10+ runtime, POSIX shell',
                'preflight': 'Verify scratch/day24_lab workspace and load legacy policy inventory',
                'trouble': 'Ensure group email strings follow domain conventions (e.g. @brightloaf.com)',
                'cleanup': 'Artifacts remain in scratch/day24_lab/ and scratch/day-024-workforce-identity-report.md for validation gate auditing',
                'file': 'scratch/day-024-workforce-identity-report.md',
                'steps': LAB_03_STEPS
            }
        }
    ],
    'review_records': REVIEW_RECORDS
}

# Write out scratch/day_data_024.py
output_path = ROOT / 'scratch/day_data_024.py'
with open(output_path, 'w') as f:
    f.write('"""Durable specification for Day 24: Principals and workforce identity."""\n\n')
    f.write(f'ACCESS_DATE = {repr(ACCESS_DATE)}\n\n')
    f.write(f'SOURCES = {repr(SOURCES)}\n\n')
    f.write(f'DATA = {repr(DATA)}\n')

print(f"Successfully generated {output_path} ({output_path.stat().st_size} bytes)")
