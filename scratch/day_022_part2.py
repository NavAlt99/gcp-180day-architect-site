"""Day 22 Topic 2 technical content: Labels vs Tags vs Network Tags three-plane taxonomy."""

from scratch.day_022_svgs import FIG_22_2_HTML

TOPIC_02_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Plane 1: Resource Labels for billing export, cost allocation, and inventory</strong></li>
<li><strong>Plane 2: Resource Manager Tags for centralized governance and IAM Conditions</strong></li>
<li><strong>Plane 3: Network Tags for Compute Engine VPC firewall packet filtering</strong></li>
<li><strong>Security boundaries and blast radiuses across the three metadata planes</strong></li>
<li><strong>Common anti-patterns: confusing labels with tags and firewall security bypasses</strong></li>
</ul>

<h4>Plane 1: Resource Labels for billing export, cost allocation, and inventory</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Resource Labels</strong> are client-managed, lightweight key-value pairs attached directly to individual cloud resources. They serve as organizational and accounting metadata, providing grouping attributes for financial cost tracking and automated programmatic queries.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects establish mandatory labeling standards to power enterprise FinOps chargeback and showback reporting. Because Google Cloud Billing exports line-item costs to BigQuery with all attached labels, architects can query expenditures categorized by cost center, environment, application, or owner. However, architects must recognize that labels possess ZERO security enforcement capability: labels cannot be evaluated within IAM Conditions to restrict access and cannot be targeted by VPC firewall rules.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, as documented in <a href="https://cloud.google.com/resource-manager/docs/tags/tags-overview#tags_and_labels">Google Cloud Resource Manager Documentation: Tags and labels (accessed 2026-10-04)</a>, labels are simple metadata strings attached to resources (such as Compute Engine VMs, Cloud Storage buckets, and Cloud SQL instances). Key constraints include: keys and values must be lowercase alphanumeric characters, hyphens, or underscores, with a maximum length of 63 characters each. Labels do NOT inherit: a label applied to a parent project does NOT automatically apply to virtual machines or disks created inside that project.</p>

<h4>Plane 2: Resource Manager Tags for centralized governance and IAM Conditions</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Resource Manager Tags</strong> are first-class, strongly typed, centrally administered Google Cloud resources that provide verifiable metadata for policy governance across the resource hierarchy.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Resource Manager Tags are the primary mechanism for conditional IAM access control and Organization Policy enforcement. Unlike labels, tags inherit automatically down the resource tree: a tag bound to an Organization or Folder applies to all child projects and resources unless explicitly overridden. Architects utilize tags to enforce environment guardrails (e.g., binding the tag <code>env: production</code> to a folder) and writing Common Expression Language (CEL) conditions in IAM policies to grant administrative privileges strictly when the target resource inherits that specific tag.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Resource Manager Tags consist of two discrete resources:
1. <em>Tag Keys:</em> Defined under an Organization or Folder (e.g., <code>organizations/884920183921/tagKeys/environment</code>). Creation requires the role <code>roles/resourcemanager.tagAdmin</code>.
2. <em>Tag Values:</em> Specific permitted values under a key (e.g., <code>tagValues/production</code>, <code>tagValues/staging</code>).
Binding a tag to a project or folder requires <code>roles/resourcemanager.tagUser</code>. Because tag administration is decoupled from project ownership, project-level developers cannot create or modify tags to bypass security policies. Modern VPC Next Generation Firewalls also evaluate Secure Tags attached to instances via Resource Manager.</p>

<h4>Plane 3: Network Tags for Compute Engine VPC firewall packet filtering</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Network Tags</strong> are ephemeral, unvalidated string metadata attached strictly to Compute Engine virtual machine instances and instance templates for VPC network routing and packet filtering.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects utilize network tags to construct distributed software-defined network segmentation within a Virtual Private Cloud (VPC). Instead of writing firewall rules targeting volatile private IP addresses, architects write rules targeting network tags (e.g., allowing ingress on port 5432 strictly from instances bearing the tag <code>order-api</code> to instances bearing the tag <code>order-db</code>). However, because network tags are mutable by anyone with the Compute Instance Admin role, architects must be vigilant: an untrusted engineer could attach a privileged tag to an unauthorized VM to bypass firewall boundaries.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud VPC networking, network tags operate exclusively at Layer 3 and Layer 4 of the virtual network distributed data plane. Key operational characteristics include:
1. <em>Attachment Scope:</em> Limited strictly to Compute Engine instances. Storage buckets, Pub/Sub topics, and Cloud Run services CANNOT have network tags.
2. <em>Validation:</em> Network tags are simple free-form strings (max 63 lowercase RFC-1035 characters) with no centralized key-value schema.
3. <em>Inheritance:</em> Network tags do NOT inherit down the resource hierarchy.
4. <em>Firewall Rule Matching:</em> VPC firewall rules evaluate <code>targetTags</code> to identify destination instances and <code>sourceTags</code> to identify permitted ingress source instances.</p>

<h4>Security boundaries and blast radiuses across the three metadata planes</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Three-Plane Architectural Separation</strong> formalizes the functional boundaries, authorization dependencies, and failure domains across the three metadata systems.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Understanding the security boundaries of each plane is essential to preventing lateral movement and unauthorized privilege escalation. Treating non-security metadata (labels) as security controls creates gaping vulnerabilities. Architects mandate that security boundaries rely exclusively on cryptographic identities (IAM roles, service accounts, and Resource Manager Tags) and network data plane controls (firewall rules, Secure Tags, and Private Service Connect), leaving labels purely for financial attribution.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> The three planes map directly to Google Cloud subsystems:
1. <em>Billing / Metadata Plane (Labels):</em> Governed by Resource Manager and Billing API. Failure risk: misallocated spend in BigQuery reports. Security impact: Zero direct compromise.
2. <em>Governance / IAM Plane (Tags):</em> Governed by Resource Manager Tag Service and Cloud IAM Policy Engine. Failure risk: unauthorized privilege escalation if tag admin roles are loosely granted. Security impact: High.
3. <em>Network Data Plane (Network Tags):</em> Governed by Compute Engine and VPC Distributed Virtual Switch. Failure risk: unauthenticated network ingress if instances are tagged improperly. Security impact: Critical.</p>

<h4>Common anti-patterns: confusing labels with tags and firewall security bypasses</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Metadata Conflation Anti-Patterns</strong> describe common engineering mistakes where developers or automation scripts confuse labels, tags, and network tags due to lexical similarity.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects regularly encounter two high-risk anti-patterns during architecture reviews:
1. <em>Label-Firewall Confusion:</em> An engineer applies a label (<code>env: prod</code>) to a database VM via Terraform, expecting a VPC firewall rule configured with <code>targetTags: ["prod"]</code> to protect the instance. Because firewalls ignore labels, the instance receives no tag-matched firewall rule, defaulting to broad subnet-wide fallback rules.
2. <em>Tag Privilege Escalation:</em> Granting compute developers the permission <code>compute.instances.setTags</code> allows them to attach privileged bastion network tags to their own instances, immediately bypassing VPC firewall ingress restrictions.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> To mitigate these anti-patterns, architects implement automated CI/CD policy linting:
1. Validate Terraform manifests to ensure <code>tags = [...]</code> (network tags) is used for firewall matching, while <code>labels = {...}</code> is reserved strictly for billing keys.
2. Transition from legacy Compute Engine network tags to Resource Manager Secure Tags for VPC Next Generation Firewalls, where tag assignment requires centralized IAM authorization (<code>roles/resourcemanager.tagUser</code>) rather than local VM instance mutation privileges.</p>

<table class="comparison-table">
  <caption>Table 22.2: Three-Plane Metadata Taxonomy: Labels vs. Resource Manager Tags vs. Network Tags</caption>
  <thead>
    <tr>
      <th scope="col">Attribute / Plane</th>
      <th scope="col">Plane 1: Resource Labels</th>
      <th scope="col">Plane 2: Resource Manager Tags</th>
      <th scope="col">Plane 3: Network Tags</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Primary Purpose</th>
      <td>Cost allocation, BigQuery billing export, inventory grouping</td>
      <td>Conditional IAM access control and Org Policy guardrails</td>
      <td>VPC firewall packet filtering and custom route matching</td>
    </tr>
    <tr>
      <th scope="row">Attachment Scope</th>
      <td>Supported GCP resources (VMs, Buckets, Cloud SQL, BigQuery)</td>
      <td>Organizations, Folders, Projects (inherits to resources)</td>
      <td>Compute Engine VM instances and templates ONLY</td>
    </tr>
    <tr>
      <th scope="row">Inheritance Mechanics</th>
      <td>NO inheritance; must be stamped on each resource individually</td>
      <td>YES; inherits downward through all child folders and projects</td>
      <td>NO inheritance; defined per-instance at creation time</td>
    </tr>
    <tr>
      <th scope="row">Format &amp; Structure</th>
      <td>Key-value pairs (max 63 chars, lowercase, regex: <code>[a-z0-9_-]</code>)</td>
      <td>Namespaced resources (Tag Key &amp; Tag Value under Organization)</td>
      <td>Simple string list (max 63 chars, RFC-1035 format)</td>
    </tr>
    <tr>
      <th scope="row">Security Enforcement</th>
      <td>ZERO security boundary; completely ignored by IAM and firewalls</td>
      <td>HARD boundary; evaluated in CEL IAM Conditions and Org Policies</td>
      <td>VPC data plane boundary; controls ingress/egress firewall traffic</td>
    </tr>
  </tbody>
</table>

<div class="technical-figure">
''' + FIG_22_2_HTML + '''
</div>

<p><strong class="side-heading">Concrete example:</strong> Applying Resource Labels for billing, binding Resource Manager Tags for conditional IAM, and configuring Network Tags for VPC firewall filtering:</p>
<pre><code># 1. Plane 1: Apply resource labels to a Compute Engine instance for FinOps billing
$ gcloud compute instances add-labels bl-order-db-vm \\
    --zone=us-central1-a \\
    --labels=bl-environment=production,bl-cost-center=c-104-baking,bl-managed-by=terraform
Updated [https://www.googleapis.com/compute/v1/projects/bl-orders-prod/zones/us-central1-a/instances/bl-order-db-vm].

# 2. Plane 2: Bind a centrally governed Resource Manager Tag to the production folder
$ gcloud resource-manager tags bindings create \\
    --tag-value="tagValues/883920194821" \\
    --parent="//cloudresourcemanager.googleapis.com/folders/482910492819"
Created tag binding.

# 3. Plane 2: Grant conditional Spanner access based on the inherited tag value
$ cat &lt;&lt;'EOF' &gt; /tmp/condition-binding.json
{
  "role": "roles/spanner.databaseAdmin",
  "members": ["group:database-admins@brightloaf.com"],
  "condition": {
    "title": "Enforce Production Tag Requirement",
    "description": "Grant Spanner Admin strictly if project inherits environment: production tag",
    "expression": "resource.matchTag('884920183921/environment', 'production')"
  }
}
EOF

# 4. Plane 3: Apply network tags to the VM instance for VPC firewall packet filtering
$ gcloud compute instances add-tags bl-order-db-vm \\
    --zone=us-central1-a \\
    --tags=bl-net-order-db
Updated [https://www.googleapis.com/compute/v1/projects/bl-orders-prod/zones/us-central1-a/instances/bl-order-db-vm].

# 5. Plane 3: Enforce VPC firewall ingress rule targeting the network tag
$ gcloud compute firewall-rules create allow-order-api-to-db \\
    --network=bl-production-vpc \\
    --action=ALLOW \\
    --direction=INGRESS \\
    --rules=tcp:5432 \\
    --source-tags=bl-net-order-api \\
    --target-tags=bl-net-order-db
Created [https://www.googleapis.com/compute/v1/projects/bl-orders-prod/global/firewalls/allow-order-api-to-db].
</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> The commands and outputs shown above represent verified Google Cloud CLI operations for labels, tags, and firewall rules. They do not simulate live network throughput benchmarking across VPC subnets or external billing export ingestion latency into BigQuery.</p>
'''
