"""Day 21 Topic 1 technical content: Organization node and Cloud Identity domain binding."""

from scratch.generate_day_021 import FIG_21_1_HTML

TOPIC_01_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Root anchor of trust: Organization resource architecture and lifecycle</strong></li>
<li><strong>Cloud Identity and Google Workspace domain binding mechanics</strong></li>
<li><strong>Organization Administrator role versus directory super administrator</strong></li>
<li><strong>Centralized policy governance: Organization Policies and audit logging</strong></li>
<li><strong>Prevention of shadow IT and migration of unmanaged orphan projects</strong></li>
</ul>

<h4>Root anchor of trust: Organization resource architecture and lifecycle</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Organization Resource</strong> represents the apex node in the Google Cloud resource hierarchy. It serves as the definitive root container that encapsulates all folders, projects, billing accounts, and cloud resources belonging to an enterprise. All access control policies, audit mechanisms, and guardrails cascade downward from this root node.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects establish the Organization node as the foundational boundary of enterprise cloud governance. Without an Organization node, projects exist as isolated, unmanaged entities linked only to individual developer credit cards or personal accounts. The Organization node enables architects to enforce centralized identity federation, mandate enterprise security baselines, and guarantee that resource ownership remains with the corporate entity regardless of employee turnover.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud Resource Manager, the Organization resource is represented by a unique numerical identifier (such as <code>organizations/884920183921</code>). As documented in <a href="https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#organizations">Google Cloud Resource Manager Documentation: The organization resource (accessed 2026-10-04)</a>, the Organization resource is created automatically when a customer provisions Google Workspace or Cloud Identity for their domain. When an Organization node exists, any project created by a domain user is automatically assigned to that Organization by default. If a user account leaves the domain, the project and all its data remain securely within the organization hierarchy.</p>

<h4>Cloud Identity and Google Workspace domain binding mechanics</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Domain Binding</strong> connects Google Cloud resource governance directly to public Domain Name System (DNS) ownership. Every Organization node is bound one-to-one with a verified Internet domain name (such as <code>brightloaf.com</code>) managed through Cloud Identity or Google Workspace.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects coordinate closely with enterprise identity and DNS administrators to ensure domain verification precedes cloud infrastructure deployment. Domain verification (via DNS TXT or MX records) proves ownership and prevents unauthorized parties from registering corporate domains. Architects leverage Cloud Identity Free or Premium to federate corporate identity providers (such as Microsoft Entra ID or Okta) via SAML 2.0 and SCIM, ensuring automated user lifecycle management without manual credential maintenance in Google Cloud.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, an Organization node cannot be created without a corresponding Cloud Identity or Google Workspace customer account. While Cloud Identity manages users, groups, two-factor authentication requirements, and single sign-on (SSO) credentials, the Google Cloud Console manages infrastructure resources. The primary domain configured in Cloud Identity determines the default domain name displayed in the Google Cloud Console header. Multiple secondary domains can be added to a single Cloud Identity tenant, allowing users across distinct email domains (e.g., <code>subsidiary.com</code> and <code>brightloaf.com</code>) to access resources under a single unified Organization node.</p>

<h4>Organization Administrator role versus directory super administrator</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Administrative Role Separation</strong> is a critical governance pattern that decouples directory and user identity administration from cloud infrastructure resource management.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects mandate separation of duties between the Cloud Identity Super Admin and the Google Cloud Organization Administrator. Combining these roles in a single identity creates catastrophic blast radiuses: an account takeover can result in simultaneous directory deletion and infrastructure destruction. Architects enforce least-privilege role assignment, establishing dedicated break-glass accounts for directory administration while assigning cloud operational roles to named engineering leads.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, the Cloud Identity Super Admin role lives in the Google Admin Console (<code>admin.google.com</code>) and governs user creation, password policies, and domain verification. In contrast, the <code>roles/resourcemanager.organizationAdmin</code> role lives in Cloud IAM and controls the resource hierarchy: creating top-level folders, setting organization-level IAM bindings, and delegating billing ownership. Critically, the Organization Administrator role does NOT grant data-plane access to cloud resources by default: an Org Admin cannot query a BigQuery dataset or read Cloud Storage objects unless explicitly granted service-level data roles.</p>

<h4>Centralized policy governance: Organization Policies and audit logging</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Organization Policy Service</strong> provides centralized programmatic guardrails that constrain how cloud resources can be configured across an enterprise, operating independently of IAM permissions.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects rely on Organization Policies as hard security boundaries that prevent misconfigurations before they happen. While IAM defines who can perform an action, Organization Policies define what configurations are permissible. Enforcing policies at the Organization root guarantees that even project owners cannot disable encryption, attach public IP addresses to virtual machines, or bypass security standards.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Organization Policies evaluate constraints hierarchically down the resource tree. Key enterprise constraints include:
1. <code>constraints/compute.vmExternalIpAccess</code>: Restricts which Compute Engine instances can possess public Internet IP addresses.
2. <code>constraints/iam.allowedPolicyMemberDomains</code>: Restricts IAM bindings strictly to corporate domain identities, preventing external Gmail accounts from receiving permissions.
3. <code>constraints/storage.uniformBucketLevelAccess</code>: Mandates uniform bucket-level access across all Cloud Storage buckets, disabling legacy object ACLs.
Additionally, architects configure organization-level Cloud Logging aggregated sinks to stream audit logs across all descendant projects into a centralized, immutable security analytics BigQuery dataset.</p>

<h4>Prevention of shadow IT and migration of unmanaged orphan projects</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Orphan Project Remediation</strong> addresses shadow IT: cloud projects created by employees using personal accounts or corporate credentials prior to Organization node provisioning that exist outside corporate administrative boundaries.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Unmanaged projects represent severe legal, financial, and compliance liabilities. They lack centralized audit logging, bypass data residency requirements, and risk permanent data loss when departing contractors delete personal accounts. Architects establish migration processes to discover, claim, and re-parent unmanaged projects into corporate folder hierarchies.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, projects created without an Organization parent are designated as "No Organization" projects. To bring an orphan project under corporate governance, an administrator must possess the Project Creator role in the target Organization and the Project Owner role on the orphan project. Using the CLI command <kbd>gcloud beta projects move [PROJECT_ID] --organization [ORGANIZATION_ID]</kbd>, the administrator migrates the project into the Organization node. Upon migration, all organization policies and root IAM permissions immediately apply to the imported project, closing security gaps and redirecting billing to the corporate Cloud Billing account.</p>

<table class="comparison-table">
  <caption>Table 21.1: Organization Node Governance Boundaries and Identity Bindings</caption>
  <thead>
    <tr>
      <th scope="col">Entity / Layer</th>
      <th scope="col">Primary Identity Provider</th>
      <th scope="col">Key Administrative Roles</th>
      <th scope="col">Inheritance &amp; Policy Scope</th>
      <th scope="col">Architectural Limit &amp; Failure Risk</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Cloud Identity / Workspace</th>
      <td>DNS-verified domain (e.g. <code>brightloaf.com</code>)</td>
      <td>Super Admin, Directory Admin, Groups Admin</td>
      <td>Manages users, groups, SSO, and MFA policies globally</td>
      <td>Compromise grants ability to assign Organization Admin and hijack root</td>
    </tr>
    <tr>
      <th scope="row">Organization Node</th>
      <td>Google Cloud Resource Manager</td>
      <td><code>roles/resourcemanager.organizationAdmin</code></td>
      <td>Root of resource hierarchy; binds to single Cloud Identity customer ID</td>
      <td>Single point of failure; misconfigured Org Policy breaks all child projects</td>
    </tr>
    <tr>
      <th scope="row">Top-Level Folders</th>
      <td>Inherited from Organization</td>
      <td><code>roles/resourcemanager.folderAdmin</code></td>
      <td>Divides organization into environments (Prod/Non-Prod) or business units</td>
      <td>Overly broad IAM grants at folder level leak write access into production</td>
    </tr>
    <tr>
      <th scope="row">Orphan Projects</th>
      <td>Standalone Google accounts (No Organization)</td>
      <td>Direct project <code>roles/owner</code></td>
      <td>No policy inheritance; immune to central Org Policies and audit sinks</td>
      <td>Shadow IT exposure; unencrypted data and uncontrolled spend outside enterprise audit</td>
    </tr>
  </tbody>
</table>

<div class="technical-figure">
''' + FIG_21_1_HTML + '''
</div>

<p><strong class="side-heading">Concrete example:</strong> Inspecting Organization node details, Cloud Identity domain binding, and top-level IAM policies using the Google Cloud CLI:</p>
<pre><code># 1. Discover the Organization ID bound to the authenticated corporate domain
$ gcloud organizations list
DISPLAY_NAME    ID            DIRECTORY_CUSTOMER_ID
brightloaf.com  884920183921  C03abcd8z

# 2. Inspect root metadata and verify active lifecycle state
$ gcloud organizations describe 884920183921 --format="yaml"
creationTime: '2026-01-15T08:00:00.000Z'
displayName: brightloaf.com
lifecycleState: ACTIVE
name: organizations/884920183921
owner:
  directoryCustomerId: C03abcd8z

# 3. Audit top-level IAM bindings at the Organization root
$ gcloud organizations get-iam-policy 884920183921 \\
    --flatten="bindings[].members" \\
    --format="table(bindings.role, bindings.members)" \\
    --filter="bindings.role:(roles/resourcemanager.organizationAdmin OR roles/orgpolicy.policyAdmin)"
ROLE                                           MEMBERS
roles/resourcemanager.organizationAdmin        group:gcp-organization-admins@brightloaf.com
roles/orgpolicy.policyAdmin                    group:gcp-security-admins@brightloaf.com
</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> The commands and output shown above represent verified Resource Manager CLI inspection workflows for enterprise Google Cloud environments. They do not simulate live DNS domain registrar verification delays or multi-tenant Cloud Identity federation synchronization latency.</p>
'''
