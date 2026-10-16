"""Day 21 Topic 2 technical content: Folders and policy inheritance mechanics."""

from scratch.day_021_svgs import FIG_21_2_HTML

TOPIC_02_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Multi-tier folder hierarchy structuring models (Environment-first vs. Business-unit-first)</strong></li>
<li><strong>Additive IAM policy inheritance mechanics down the resource tree</strong></li>
<li><strong>Environment isolation: segregating Production from Non-Production subtrees</strong></li>
<li><strong>Folder-level Organization Policy enforcement and inheritance overrides</strong></li>
<li><strong>Departmental cost allocation, chargeback, and folder budget boundaries</strong></li>
</ul>

<h4>Multi-tier folder hierarchy structuring models (Environment-first vs. Business-unit-first)</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Folder Hierarchy Structuring</strong> organizes projects into logical management containers underneath the Organization root node. Folders can be nested up to 10 levels deep, allowing enterprises to mirror their operating structure.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects choose between two primary hierarchy structuring topologies:
1. <em>Environment-first (Lifecycle-first):</em> The top level immediately splits into <code>Production</code>, <code>Non-Production</code>, and <code>Shared-Services</code> folders, with business units nested beneath. This prioritizes strict security isolation and guarantees that environment-wide Organization Policies and IAM boundaries apply uniformly across all departments.
2. <em>Business-unit-first (Department-first):</em> The top level splits into business units (e.g., <code>Retail</code>, <code>Finance</code>, <code>Logistics</code>), with lifecycle environments (<code>Dev</code>, <code>Stage</code>, <code>Prod</code>) nested inside each business unit. This optimizes for business autonomy and localized billing delegation, but increases the risk of inconsistent security baselines between departments if production policies must be duplicated across multiple trees.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud Resource Manager, folders are created using the Resource Manager API or CLI via <kbd>gcloud resource-manager folders create</kbd>, as documented in <a href="https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#folders">Google Cloud Resource Manager Documentation: The folder resource (accessed 2026-10-04)</a>. Folders possess unique numerical IDs (such as <code>folders/482910492819</code>) and display names that do not require global uniqueness. Most enterprise architectures adopt a hybrid model: top-level business units containing dedicated environment folders, or an environment-first model where security and compliance guardrails take precedence over divisional autonomy.</p>

<h4>Additive IAM policy inheritance mechanics down the resource tree</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Additive Policy Inheritance</strong> governs how Identity and Access Management permissions flow through the Google Cloud resource hierarchy. IAM policies are strictly additive: permissions granted at a parent node in the hierarchy cannot be revoked, restricted, or subtracted at a child node.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Understanding the additive nature of IAM is critical for cloud architects to prevent accidental privilege escalation. If an engineer or group is granted <code>roles/editor</code> or <code>roles/viewer</code> at a parent folder level, that identity holds that role across every single project inside that folder and all child subfolders. A child project IAM policy cannot specify a "deny" or removal of a role inherited from above. Consequently, architects mandate least privilege at higher nodes (granting only broad read-only audit roles like <code>roles/viewer</code> or specific logging roles at the folder root) while reserving administrative and mutation roles for individual project nodes or tightly scoped child folders.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud IAM evaluation, the effective policy for any resource is the union of the policy set directly on the resource and all policies set on its ancestor parents up to the Organization root. While IAM Deny Policies (introduced in modern Cloud IAM) can place explicit guardrails at folder or org levels to block specific permissions regardless of grants, standard IAM Role bindings remain strictly additive. Architects must audit inherited permissions using Cloud Asset Inventory or the CLI command <kbd>gcloud projects get-ancestors-iam-policy [PROJECT_ID]</kbd> to verify effective access before provisioning workloads.</p>

<h4>Environment isolation: segregating Production from Non-Production subtrees</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Environment Isolation</strong> is the architectural practice of placing workloads with different risk profiles, data classifications, and operational access requirements into completely isolated resource trees.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Mixing production and staging workloads within the same folder inevitably leads to human error and compliance failure. For example, if developers have access to modify infrastructure in staging, and staging shares a parent folder with production, any folder-level role binding leaks into production. Cloud architects segregate production into dedicated folder branches governed by rigorous change management, automated CI/CD service accounts, and restricted human access, while non-production folders provide greater developer freedom and automated teardown capabilities.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, environment isolation at the folder level enables architects to:
1. Isolate Shared VPC host projects: ensure production VPC networks never peer or route into development networks without inspectable firewall boundaries.
2. Apply distinct Cloud Audit Logging configurations: enforce verbose data-access logging across all production projects while suppressing high-volume debug logs in development to optimize logging costs.
3. Enforce separate administrative groups: bind <code>group:prod-ops@brightloaf.com</code> to the <code>Production</code> folder while binding <code>group:all-devs@brightloaf.com</code> strictly to the <code>Non-Production</code> folder.</p>

<h4>Folder-level Organization Policy enforcement and inheritance overrides</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Hierarchical Policy Enforcement</strong> allows security teams to apply targeted operational constraints at intermediate folder levels, tailoring guardrails to specific workload needs while maintaining organization baselines.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> While the Organization root establishes the enterprise security baseline, different environments require different rules. For instance, developers in a sandbox folder may need the ability to test external API integrations using public IP addresses, whereas production virtual machines must be strictly private. Architects leverage folder-level policy overrides to relax or tighten constraints without modifying the root organization policy.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Organization Policies support two inheritance behaviors:
1. <em>Inherit from parent (Merge):</em> By default, list constraints evaluate child values in addition to inherited parent values.
2. <em>Override parent (Replace):</em> A folder policy can explicitly set <code>inheritFromParent: false</code> (or use the CLI flag <code>--no-inherit</code>) to completely replace the inherited constraint rules for its subtree.
For boolean constraints (such as <code>constraints/compute.disableSerialPortAccess</code>), setting the policy to <code>enforce: true</code> at a folder immediately locks down all child projects. Architects must carefully document all inheritance overrides to ensure compliance drift does not compromise sensitive workloads.</p>

<h4>Departmental cost allocation, chargeback, and folder budget boundaries</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Cost Allocation and Chargeback</strong> maps cloud consumption expenditures directly to organizational cost centers, departments, or business units.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects design folder hierarchies not only for security but also for financial governance (FinOps). Cloud billing data exported to BigQuery includes the resource hierarchy path (organization, folder IDs, folder names, and project IDs). By aligning top-level or second-level folders with corporate cost centers (e.g., <code>Cost-Center-104-Logistics</code>), architects enable automated chargeback reporting, departmental budget alerts, and showback dashboards.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud Billing:
1. Billing accounts are attached at the project level, but billing export schemas automatically capture the full folder hierarchy ancestry for every line item.
2. Cloud Billing Budgets can be scoped to specific projects or filtered by resource hierarchy labels.
3. Programmatic budget notifications published to Cloud Pub/Sub allow automated financial governance runbooks—such as disabling billing or scaling down non-critical development instances when a folder budget threshold is exceeded.</p>

<table class="comparison-table">
  <caption>Table 21.2: Folder Hierarchy Structuring Strategies &amp; Inheritance Patterns</caption>
  <thead>
    <tr>
      <th scope="col">Hierarchy Pattern</th>
      <th scope="col">Top-Level Grouping</th>
      <th scope="col">IAM Inheritance Characteristics</th>
      <th scope="col">Org Policy Control</th>
      <th scope="col">FinOps Chargeback Alignment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Environment-First</th>
      <td><code>Production</code>, <code>Non-Production</code>, <code>Shared-Services</code></td>
      <td>Clean blast-radius isolation; zero developer access to production subtree</td>
      <td>Uniform security posture per lifecycle phase; straightforward policy enforcement</td>
      <td>Requires tagging or subfolder aggregation to split departmental spend</td>
    </tr>
    <tr>
      <th scope="row">Business-Unit-First</th>
      <td><code>Retail</code>, <code>Supply-Chain</code>, <code>Customer-Platform</code></td>
      <td>Departmental teams manage own subtrees; risk of granting broad roles at BU root</td>
      <td>Requires duplicating production policy constraints across multiple departmental branches</td>
      <td>Direct 1:1 mapping between top folder and corporate general ledger cost center</td>
    </tr>
    <tr>
      <th scope="row">Hybrid Enterprise</th>
      <td><code>Core-Infrastructure</code> + Department Folders with Env Subfolders</td>
      <td>Shared VPC hosted centrally; workload teams receive scoped project-level roles</td>
      <td>Base policies at Org root; specialized compliance policies on Prod subfolders</td>
      <td>Hierarchical billing export enables both cost-center chargeback and environment analysis</td>
    </tr>
  </tbody>
</table>

<div class="technical-figure">
''' + FIG_21_2_HTML + '''
</div>

<p><strong class="side-heading">Concrete example:</strong> Creating a structured multi-tier folder hierarchy and verifying IAM policy inheritance using the Google Cloud CLI:</p>
<pre><code># 1. Create top-level environment folders under the Organization root
$ gcloud resource-manager folders create \\
    --display-name="Production" \\
    --organization=884920183921
Created [folders/482910492819].

$ gcloud resource-manager folders create \\
    --display-name="Non-Production" \\
    --organization=884920183921
Created [folders/482910492820].

# 2. Grant audit visibility to the compliance team at the Production folder level
$ gcloud resource-manager folders add-iam-policy-binding 482910492819 \\
    --member="group:security-auditors@brightloaf.com" \\
    --role="roles/viewer"
Updated IAM policy for folder [482910492819].

# 3. Create a child project under the Production folder
$ gcloud projects create brightloaf-prod-payments-01 \\
    --folder=482910492819 \\
    --set-as-default
Created [brightloaf-prod-payments-01].

# 4. Verify that security-auditors inherited roles/viewer on the new project
$ gcloud projects get-ancestors-iam-policy brightloaf-prod-payments-01 \\
    --filter="policy.bindings.role:roles/viewer" \\
    --format="table(id, type, policy.bindings.members)"
ID            TYPE    POLICY.BINDINGS.MEMBERS
482910492819  folder  group:security-auditors@brightloaf.com
</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> The commands and outputs shown above illustrate standard Google Cloud Resource Manager folder creation and hierarchical IAM inheritance evaluation. They do not simulate IAM propagation delays across global Google Cloud data centers or third-party directory sync cycles.</p>
'''
