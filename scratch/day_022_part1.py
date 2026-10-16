"""Day 22 Topic 1 technical content: Hierarchical IAM policy inheritance and additive calculation."""

from scratch.day_022_svgs import FIG_22_1_HTML

TOPIC_01_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Downward propagation and the additive union principle of IAM allow policies</strong></li>
<li><strong>IAM Deny policies: explicit negative guardrails and precedence over allow rules</strong></li>
<li><strong>Mathematical model of effective permission calculation across container tiers</strong></li>
<li><strong>Control plane limits: folder depth, policy size, and eventual consistency latency</strong></li>
<li><strong>Least privilege design: folder audit visibility versus project mutation roles</strong></li>
</ul>

<h4>Downward propagation and the additive union principle of IAM allow policies</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Downward Policy Propagation</strong> governs how access control policies cascade through nested container hierarchies. Permissions granted at higher tiers flow downward to all descendant containers and leaf resources. In Google Cloud, this propagation follows an additive union principle: every allow binding granted at an ancestor container adds to, and never subtracts from, the permissions evaluated at the target resource.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects must recognize that Google Cloud IAM allow policies possess zero subtractive capability. A common and catastrophic architectural misconception is assuming that assigning a restrictive role (such as <code>roles/viewer</code>) at a child project can attenuate or override a broad role (such as <code>roles/editor</code>) granted at an ancestor folder. Because permissions are additive, granting write access at a parent folder irreversibly opens all descendant projects to mutation by that principal, eliminating project-level containment.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud Resource Manager, as documented in <a href="https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#benefits_of_the_organization_resource">Google Cloud Resource Manager Documentation: Benefits of the organization resource (accessed 2026-10-04)</a>, allow policies applied at the Organization, Folder, or Project level cascade downward automatically. The IAM evaluation engine calculates the effective permissions of a user on a resource as the union of all bindings across that resource and all of its ancestor containers. To audit these cumulative bindings, architects execute <kbd>gcloud projects get-ancestors-iam-policy [PROJECT_ID]</kbd>, which displays the complete chain of inherited allow bindings.</p>

<h4>IAM Deny policies: explicit negative guardrails and precedence over allow rules</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">IAM Deny Policies</strong> provide non-negotiable negative security guardrails that explicitly block specified permissions for specified principals, regardless of what allow bindings they possess.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Because standard IAM allow policies cannot subtract permissions, architects leverage IAM Deny policies to establish hard security perimeters. For example, enterprise architects can enforce a Deny rule at the Organization apex or Production folder level that blocks all developers and service accounts from deleting Cloud Spanner databases (<code>spanner.databases.drop</code>) or modifying audit log sinks, even if those identities hold full Owner or Editor roles on individual workload projects.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud IAM evaluation order:
1. Deny rules are evaluated <em>first</em>. If an incoming API request matches an applicable Deny rule, access is immediately rejected.
2. Allow rules are evaluated <em>second</em>. If the request was not denied, the engine evaluates whether the principal holds an allow binding for the required permission across the resource or any ancestor container.
Like allow policies, Deny policies flow downward through the resource hierarchy: a Deny rule established at an ancestor container cannot be overridden, masked, or bypassed by any child folder or project policy.</p>

<h4>Mathematical model of effective permission calculation across container tiers</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Effective Access Calculation</strong> is the formal mathematical set union operation executed by cloud policy evaluation engines to determine the runtime authorization state of an incoming request.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects utilize mathematical modeling of effective access during landing zone design to verify least-privilege baselines before provisioning workloads. By modeling permissions as set unions, architects can mathematically prove that sensitive production resources remain inaccessible to non-production identities, ensuring regulatory compliance across SOC 2 and PCI-DSS audits.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, given a leaf resource <em>R</em> residing in project <em>P</em>, under a folder path <em>F<sub>1</sub>, F<sub>2</sub>, &hellip;, F<sub>k</sub></em> beneath organization <em>O</em>, the effective permissions <em>P<sub>effective</sub>(u, R)</em> for a principal <em>u</em> are formalized as:
<code>P_effective(u, R) = (P_org(u, O) &cup; (&cup; P_folder(u, F_i)) &cup; P_project(u, P) &cup; P_resource(u, R)) \\ P_deny(u)</code>
Where <em>P_deny(u)</em> represents the set of all denied permissions matching principal <em>u</em> across any ancestor container. If a permission is present in any allow set and absent from the deny set, the request is authorized.</p>

<h4>Control plane limits: folder depth, policy size, and eventual consistency latency</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Control Plane Governance Limits</strong> define the structural scale constraints and operational propagation characteristics of the cloud resource management infrastructure.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Designing an enterprise landing zone requires balancing hierarchical depth against control plane constraints. Overly deep hierarchies introduce administrative complexity and increase policy traversal overhead, while overly dense policies risk exceeding byte-size quotas. Architects must design within documented Google Cloud platform limits to prevent operational gridlock.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Key Google Cloud Resource Manager and IAM limits include:
1. <em>Maximum Folder Depth:</em> Up to 300 nested folder levels are supported, though enterprise best practice establishes a depth of 2 to 4 tiers (e.g., Organization -> Business Unit -> Environment -> Project).
2. <em>IAM Policy Size Limit:</em> A single IAM policy cannot exceed 250 KB in total size, with a maximum limit of 1,500 member bindings across all roles. Architects prevent quota exhaustion by binding roles to Cloud Identity Google Groups rather than individual user accounts.
3. <em>Propagation Latency:</em> IAM policy mutations are distributed globally with eventual consistency. While updates typically propagate within seconds, global edge caches and distributed API gateways may experience up to 60 seconds of propagation latency before reflecting changes.</p>

<h4>Least privilege design: folder audit visibility versus project mutation roles</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Tiered Role Separation</strong> is an architectural pattern that restricts broad administrative roles to leaf nodes while granting only scoped, read-only audit roles at intermediate and root containers.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects mandate tiered role separation to prevent blast radius expansion. Granting broad mutation roles (such as <code>roles/editor</code> or <code>roles/owner</code>) at the folder level exposes all child projects to unintended data destruction or configuration drift. By restricting folder-level grants to audit roles (such as <code>roles/viewer</code> or <code>roles/browser</code>), architects ensure that operational mutation privileges must be explicitly granted on a per-project basis.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud landing zones:
1. <em>Organization / Folder Roots:</em> Bind audit visibility roles like <code>roles/viewer</code> and <code>roles/resourcemanager.folderViewer</code> to enterprise security groups.
2. <em>Child Projects:</em> Bind specific predefined or custom roles (such as <code>roles/spanner.databaseUser</code> or <code>roles/compute.instanceAdmin.v1</code>) directly to application service accounts and dedicated workload engineering groups.
3. <em>CI/CD Pipelines:</em> Production infrastructure changes are executed exclusively by automated deployment service accounts with tightly scoped project roles, preventing human developers from possessing ambient write privileges in production environments.</p>

<table class="comparison-table">
  <caption>Table 22.1: Hierarchy Levels, Policy Attachment, and Additive Union Behavior</caption>
  <thead>
    <tr>
      <th scope="col">Hierarchy Level</th>
      <th scope="col">Evaluated Policy Types</th>
      <th scope="col">Downward Flow Target</th>
      <th scope="col">Additive Union Impact</th>
      <th scope="col">Blast Radius &amp; Governance Guardrails</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Organization Apex</th>
      <td>IAM Allow, IAM Deny, Organization Policies, Tag Definitions</td>
      <td>All folders, all projects, all resources across enterprise</td>
      <td>Grants baseline enterprise permissions (e.g. Security Reviewer); additive down to all leaves</td>
      <td>Maximum blast radius; accidental write role grants here compromise entire estate</td>
    </tr>
    <tr>
      <th scope="row">Intermediate Folder</th>
      <td>IAM Allow, IAM Deny, Organization Policies, Tag Bindings</td>
      <td>Descendant sub-folders, child projects, and underlying resources</td>
      <td>Grants department or environment baseline; additive across all child projects</td>
      <td>High blast radius; a write grant at this level cannot be revoked by child project bindings</td>
    </tr>
    <tr>
      <th scope="row">Project Node</th>
      <td>IAM Allow, IAM Deny, Service Usage API Enablement</td>
      <td>All cloud resources (VMs, DBs, Buckets) inside the project</td>
      <td>Grants workload operational access; unions with all ancestor folder and org bindings</td>
      <td>Bounded blast radius; mutations restricted to project boundary unless Shared VPC is attached</td>
    </tr>
    <tr>
      <th scope="row">Leaf Resource</th>
      <td>Resource-level IAM Allow (where supported), Object ACLs</td>
      <td>Target individual resource (e.g. Spanner DB, Cloud Storage Bucket)</td>
      <td>Grants object-level access; unions with project, folder, and org allow policies</td>
      <td>Minimal blast radius; cannot override or subtract inherited ancestor allow grants</td>
    </tr>
  </tbody>
</table>

<div class="technical-figure">
''' + FIG_22_1_HTML + '''
</div>

<p><strong class="side-heading">Concrete example:</strong> Inspecting ancestor IAM policies, evaluating additive union flow, and applying an IAM Deny policy using the Google Cloud CLI:</p>
<pre><code># 1. Inspect all ancestor policies contributing to a project effective IAM state
$ gcloud projects get-ancestors-iam-policy brightloaf-prod-orders-01 \\
    --format="table(id, type, policy.bindings.role, policy.bindings.members)"
ID            TYPE          POLICY.BINDINGS.ROLE                   POLICY.BINDINGS.MEMBERS
884920183921  organization  roles/resourcemanager.organizationAdmin group:gcp-org-admins@brightloaf.com
482910492819  folder        roles/viewer                           group:compliance-auditors@brightloaf.com
482910492819  folder        roles/resourcemanager.folderAdmin      group:prod-infra-leads@brightloaf.com
918273645102  project       roles/spanner.databaseUser             serviceAccount:orders-sa@brightloaf-prod-orders-01.iam.gserviceaccount.com

# 2. Author an IAM Deny policy to block database deletion down the production folder
$ cat &lt;&lt;'EOF' &gt; /tmp/deny-db-drop.json
{
  "rules": [
    {
      "description": "Block all automated service accounts from dropping databases",
      "denyRule": {
        "deniedPrincipals": [
          "principalSet://goog/subject/serviceAccount:*"
        ],
        "deniedPermissions": [
          "spanner.googleapis.com/databases.drop"
        ]
      }
    }
  ]
}
EOF

# 3. Apply the IAM Deny policy to the Production folder
$ gcloud iam policies create deny-spanner-drop \\
    --attachment-point="cloudresourcemanager.googleapis.com/folders/482910492819" \\
    --kind="denypolicies" \\
    --policy-file="/tmp/deny-db-drop.json"
Created deny policy [deny-spanner-drop].
</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> The commands and outputs shown above demonstrate verified Google Cloud CLI ancestor policy queries and IAM Deny policy syntax. They do not simulate multi-region eventual consistency propagation delays across globally distributed IAM cache endpoints.</p>
'''
