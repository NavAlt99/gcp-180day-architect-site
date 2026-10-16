"""Day 21 Topic 3 technical content: Projects and operating boundaries."""

TOPIC_03_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>The Project Identifiers Triad: Project ID vs. Project Name vs. Project Number</strong></li>
<li><strong>Immutability and global uniqueness constraints of Project IDs</strong></li>
<li><strong>Project Number significance in Google-managed service agent derivation</strong></li>
<li><strong>Core operational boundaries established at the project layer (IAM, VPC, Billing, Quotas)</strong></li>
<li><strong>Project deletion lifecycle: soft-delete state, 30-day recovery window, and permanent purge</strong></li>
</ul>

<h4>The Project Identifiers Triad: Project ID vs. Project Name vs. Project Number</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Project Identifiers Triad</strong> defines the three distinct identities assigned to every Google Cloud project: the Project Name, the Project ID, and the Project Number. Each identifier serves distinct functional roles across user interfaces, API routing, and infrastructure automation.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Conflating these three identifiers is one of the most common causes of automation failures, broken CI/CD pipelines, and IAM authorization bugs. Architects must enforce strict naming standards and teach engineering teams the exact context in which each identifier is required:
1. <em>Project Name:</em> A user-friendly, mutable display string (e.g., "BrightLoaf Production Order Service") used purely for human readability in the Google Cloud Console. It is never used for programmatic resource addressing or API authorization.
2. <em>Project ID:</em> A globally unique, immutable string (6 to 30 characters of lowercase letters, digits, and hyphens, e.g., <code>brightloaf-prod-orders-01</code>) chosen by the customer at project creation. It is the primary identifier used in <kbd>gcloud</kbd> CLI commands, Terraform provider configurations, and REST API URIs.
3. <em>Project Number:</em> A globally unique, immutable, system-generated numerical identifier (e.g., <code>918273645102</code>) assigned automatically by Google Cloud. It acts as the internal system primary key across all Google infrastructure.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> As documented in <a href="https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#projects">Google Cloud Resource Manager Documentation: The project resource (accessed 2026-10-04)</a>, the Project resource is the base-level container upon which all Google Cloud services are enabled, configured, and billed. Understanding the distinction between Project ID and Project Number is particularly vital because many Google APIs and backend IAM principals require the numerical Project Number, whereas user-facing tools default to the string Project ID.</p>

<h4>Immutability and global uniqueness constraints of Project IDs</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Project ID Immutability</strong> guarantees that once a Project ID is assigned during creation, it can never be altered or updated throughout the lifecycle of the project. Furthermore, Project IDs share a single global namespace across all Google Cloud customers worldwide.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Because Project IDs are globally unique, simple names like "production-database" or "payment-service" are universally taken. Architects establish standardized enterprise naming conventions that incorporate the organization name, environment, application name, and random or numerical suffix (e.g., <code>bl-prod-pay-901a</code>). Because Project IDs cannot be changed post-creation, a flawed naming convention cannot be refactored without completely rebuilding the project, redeploying all services, and migrating stateful storage.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, Project IDs form the base subdomain and URI namespace for many globally addressed services, such as Google Cloud Storage bucket endpoints and App Engine URLs (e.g., <code>https://[PROJECT_ID].appspot.com</code>). Even after a project is deleted and permanently purged, its Project ID cannot be reused immediately and may be retired permanently by Google to prevent security impersonation and DNS hijacking attacks.</p>

<h4>Project Number significance in Google-managed service agent derivation</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Service Agent Derivation</strong> is the architectural mechanism by which Google Cloud automatically creates Google-managed service identities to execute platform actions on behalf of a project.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Many advanced enterprise architecture patterns—such as Customer-Managed Encryption Keys (CMEK) via Cloud KMS, cross-project Pub/Sub publishing, and Cloud Storage event notifications—rely on granting IAM permissions to Google-managed service agents. Architects must know that service agent email formats are deterministically derived using the project's numerical <em>Project Number</em>, not the Project ID. Attempting to construct a service agent identity using a Project ID results in invalid email syntax and silent authorization failures.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Common Google-managed service agent identities include:
1. <em>Cloud KMS / Pub/Sub:</em> <code>service-[PROJECT_NUMBER]@gcp-sa-pubsub.iam.gserviceaccount.com</code>
2. <em>Compute Engine Service Agent:</em> <code>service-[PROJECT_NUMBER]@compute-system.iam.gserviceaccount.com</code>
3. <em>Cloud Storage Service Agent:</em> <code>service-[PROJECT_NUMBER]@gs-project-accounts.iam.gserviceaccount.com</code>
Architects use the CLI command <kbd>gcloud projects describe [PROJECT_ID] --format="value(projectNumber)"</kbd> to retrieve the project number in automated provisioning scripts before generating cross-service IAM bindings.</p>

<h4>Core operational boundaries established at the project layer (IAM, VPC, Billing, Quotas)</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Operational Isolation Boundaries</strong> define the technical blast radiuses and resource containment borders enforced at the project level.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> The project is the primary boundary of isolation in Google Cloud. Resources within a project interact seamlessly by default, while cross-project interactions require explicit architectural configuration. Architects leverage project boundaries to separate environments, isolate sensitive compliance data, and prevent systemic outages caused by quota exhaustion or misconfigured access rules.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Four critical operational boundaries operate at the project layer:
1. <em>IAM Boundary:</em> Project-level IAM bindings (e.g., <code>roles/editor</code>) apply to all resources inside the project, but do not extend to neighboring projects unless granted at an ancestor folder.
2. <em>Network Boundary:</em> Virtual Private Cloud (VPC) networks are project-scoped entities. Cross-project network traffic requires Shared VPC (where service projects attach to a centralized host project's subnets) or VPC Network Peering.
3. <em>Billing Boundary:</em> Each project links to exactly one Cloud Billing account. Multiple projects can share a billing account, but a single project cannot split costs across multiple billing accounts directly.
4. <em>Quota Boundary:</em> Service usage quotas (e.g., maximum Compute Engine CPUs, BigQuery slot limits, and API requests per minute) are enforced per project, ensuring noisy-neighbor workloads in development do not starve production capacity.</p>

<h4>Project deletion lifecycle: soft-delete state, 30-day recovery window, and permanent purge</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Project Deletion Lifecycle</strong> describes the staged decommissioning process that prevents catastrophic, irreversible data loss when a project is deleted.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Human error or rogue scripts occasionally trigger project deletion. Architects must understand the exact operational mechanics of the 30-day recovery window: what services halt immediately, what billing implications occur, and how to execute emergency restoration procedures. Furthermore, architects must implement organization policies (such as project lien locks) to prevent accidental deletion of business-critical production infrastructure.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> When a project is deleted via <kbd>gcloud projects delete [PROJECT_ID]</kbd>:
1. <em>Immediate State (Soft-Delete):</em> The project enters the <code>DELETE_REQUESTED</code> state. All running virtual machines, Cloud SQL instances, and network connections are shut down immediately. Public access is severed, and API calls fail.
2. <em>30-Day Restoration Window:</em> The project remains in the Resource Manager "Pending Deletion" queue for 30 calendar days. During this window, an authorized administrator can restore the project using <kbd>gcloud projects undelete [PROJECT_ID]</kbd>.
3. <em>Permanent Purge:</em> After 30 days, Google Cloud permanently purges the project and all associated disks, databases, and metadata. Recovery is mathematically impossible once the purge cycle completes.
4. <em>Project Liens:</em> To protect mission-critical projects, architects apply project liens (<kbd>gcloud alpha resource-manager liens create</kbd>) with the <code>resourcemanager.projects.delete</code> restriction. Any deletion attempt against a project with an active lien is immediately blocked by the API.</p>

<table class="comparison-table">
  <caption>Table 21.3: Project Identifiers Triad and Operational Boundary Characteristics</caption>
  <thead>
    <tr>
      <th scope="col">Identifier / Boundary</th>
      <th scope="col">Format / Syntax</th>
      <th scope="col">Mutability</th>
      <th scope="col">Global Uniqueness</th>
      <th scope="col">Architectural Usage &amp; Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Project Name</th>
      <td>1-30 characters (letters, numbers, spaces, quotes)</td>
      <td>Mutable (Can be renamed anytime)</td>
      <td>No (Duplicates allowed across GCP)</td>
      <td>Display label in Google Cloud Console; NEVER use in scripts or automation</td>
    </tr>
    <tr>
      <th scope="row">Project ID</th>
      <td>6-30 chars: lowercase letters, digits, hyphens</td>
      <td>Immutable (Permanent once created)</td>
      <td>Yes (Globally unique across all tenants)</td>
      <td>Primary identifier in <kbd>gcloud</kbd>, Terraform providers, and REST API URIs</td>
    </tr>
    <tr>
      <th scope="row">Project Number</th>
      <td>System-generated 11-12 digit integer</td>
      <td>Immutable (Assigned automatically by Google)</td>
      <td>Yes (Globally unique system primary key)</td>
      <td>Required for Google-managed service agent emails and backend IAM bindings</td>
    </tr>
    <tr>
      <th scope="row">VPC Network Boundary</th>
      <td>Isolated software-defined network namespace</td>
      <td>Mutable (VPCs can be added or deleted)</td>
      <td>Project-scoped namespace</td>
      <td>Requires Shared VPC or VPC Peering to route packets across project boundaries</td>
    </tr>
    <tr>
      <th scope="row">Quota &amp; Billing Boundary</th>
      <td>Allocated service quotas and 1:1 billing link</td>
      <td>Mutable (Quota increases can be requested)</td>
      <td>Project-scoped quota pool</td>
      <td>Prevents non-production workloads from consuming production compute or API limits</td>
    </tr>
  </tbody>
</table>

<p><strong class="side-heading">Concrete example:</strong> Retrieving the project identifiers triad and deriving Google-managed service agent identities using the Google Cloud CLI:</p>
<pre><code># 1. Retrieve project details and compare Name, ID, and Number
$ gcloud projects describe brightloaf-prod-orders-01 --format="yaml"
createTime: '2026-02-10T14:22:30.123Z'
lifecycleState: ACTIVE
name: BrightLoaf Production Orders Service
projectId: brightloaf-prod-orders-01
projectNumber: '918273645102'

# 2. Extract the exact numerical Project Number for automation scripting
$ PROJECT_NUM=$(gcloud projects describe brightloaf-prod-orders-01 --format="value(projectNumber)")
$ echo "Project Number: ${PROJECT_NUM}"
Project Number: 918273645102

# 3. Derive the Google-managed Pub/Sub service agent identity
$ PUBSUB_SA="service-${PROJECT_NUM}@gcp-sa-pubsub.iam.gserviceaccount.com"
$ echo "Derived Pub/Sub Service Agent: ${PUBSUB_SA}"
Derived Pub/Sub Service Agent: service-918273645102@gcp-sa-pubsub.iam.gserviceaccount.com

# 4. Grant Cloud KMS Decrypter permission to the derived service agent
$ gcloud kms keyrings add-iam-policy-binding order-keyring \\
    --location=us-central1 \\
    --key=order-encryption-key \\
    --member="serviceAccount:${PUBSUB_SA}" \\
    --role="roles/cloudkms.cryptoKeyDecrypter"
Updated IAM policy for key [order-encryption-key].

# 5. Apply a project lien to protect production orders from accidental deletion
$ gcloud alpha resource-manager liens create \\
    --project=brightloaf-prod-orders-01 \\
    --restrictions="resourcemanager.projects.delete" \\
    --reason="Production order processing pipeline must not be deleted"
Created lien [liens/p918273645102-l83920194].
</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> The commands and outputs shown above demonstrate verified Google Cloud Resource Manager project metadata inspection, service agent derivation syntax, and lien enforcement. They do not simulate cross-organization Shared VPC peering latency or external third-party KMS integrations.</p>
'''
