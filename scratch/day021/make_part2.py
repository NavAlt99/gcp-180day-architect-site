with open('scratch/day021/fig1.html') as f:
    fig1 = f.read()
with open('scratch/day021/fig2.html') as f:
    fig2 = f.read()

part2 = f'''    <section class="part" id="part-2" aria-labelledby="part-2-title">
      <h2 id="part-2-title">2 · Architecture, control flow, boundaries, and limits</h2>

      <article class="topic-card" id="topic-01-technical">
        <h3>Organization node architecture, Cloud Identity domain binding, and root governance</h3>
        <p>The Google Cloud resource hierarchy provides a logical container tree that establishes ownership, access control inheritance, billing associations, and organizational policy boundaries. At the apex of this hierarchy sits the <strong>Organization node</strong> (<code>organizations/&lt;org_id&gt;</code>).</p>

        <h4>Domain Binding &amp; Super Admin Separation</h4>
        <p>The Organization node is not an arbitrary cloud construct created ad-hoc; it is strictly anchored 1:1 to a verified primary domain in <strong>Cloud Identity</strong> or <strong>Google Workspace</strong>. Domain ownership is verified cryptographically via DNS TXT records. Once verified, Google Cloud automatically provisions the Organization resource.</p>
        <p>A fundamental architectural separation exists between domain administration and cloud resource governance:</p>
        <ul>
          <li><strong>Super Administrator (Cloud Identity / Google Workspace):</strong> Owns user provisioning, group memberships, two-factor authentication enforcement, and initial cloud onboarding. Super Admins assign the initial Google Cloud organization roles.</li>
          <li><strong>Organization Administrator (<code>roles/resourcemanager.organizationAdmin</code>):</strong> Operates strictly within Google Cloud. Owns the resource container tree, folder structuring, organizational policies, and billing account associations. The Organization Administrator cannot reset user passwords or manage email accounts in Google Workspace.</li>
        </ul>

        <h4>Root Governance Capabilities</h4>
        <p>The Organization node enables three enterprise control capabilities that cannot exist on standalone, unmanaged projects:</p>
        <ol>
          <li><strong>Organization Policy Service:</strong> Applies centralized, programmatic guardrails (e.g. <code>constraints/compute.vmExternalIpAccess</code> or <code>constraints/gcp.resourceLocations</code>) that restrict what developers can do across all descendant folders and projects, regardless of their IAM roles.</li>
          <li><strong>Aggregated Cloud Audit Log Sinks:</strong> Configures centralized log exports at the root node that automatically capture and route administrative write and data-access audit logs from all projects into a locked security information and event management (SIEM) project.</li>
          <li><strong>Root Project Recovery &amp; Orphan Prevention:</strong> Eliminates orphaned projects. If a project creator leaves the enterprise, the Organization Administrator retains root ownership and can reassign project ownership or shut down rogue resources.</li>
        </ol>

        <div class="table-wrap">
          <table>
            <caption>Organization Node Governance Boundaries and Identity Bindings</caption>
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
                <td>Corporate DNS Domain (e.g. <code>brightloaf.com</code>)</td>
                <td>Super Administrator</td>
                <td>Directory-wide user accounts and security groups</td>
                <td>Domain expiration or DNS hijacking compromises cloud identity root.</td>
              </tr>
              <tr>
                <th scope="row">Organization Node</th>
                <td>1:1 Cloud Identity Domain Binding</td>
                <td><code>roles/resourcemanager.organizationAdmin</code></td>
                <td>Root of all folders, projects, and billing linkages</td>
                <td>Assigning broad primitive roles (e.g. Owner) at root creates universal blast radius.</td>
              </tr>
              <tr>
                <th scope="row">Aggregated Audit Sink</th>
                <td>Organization Logging Service Agent</td>
                <td><code>roles/logging.configWriter</code></td>
                <td>Captures audit events from all child containers</td>
                <td>Storage sink misconfiguration can cause compliance audit data loss.</td>
              </tr>
              <tr>
                <th scope="row">Org Policy Service</th>
                <td>Resource Manager Constraints Engine</td>
                <td><code>roles/orgpolicy.policyAdmin</code></td>
                <td>Enforces boolean and list constraints downward</td>
                <td>Overly restrictive root policies can break legitimate regional deployments.</td>
              </tr>
            </tbody>
          </table>
        </div>

{fig1}

        <div class="further-study">
          <h4>Further Study · Primary Documentation</h4>
          <ul>
            <li><a href="https://cloud.google.com/resource-manager/docs/creating-managing-organization" target="_blank" rel="noopener noreferrer">Google Cloud Documentation: Creating and Managing Organizations</a></li>
            <li><a href="https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy" target="_blank" rel="noopener noreferrer">Google Cloud Documentation: Resource Hierarchy Overview</a></li>
          </ul>
        </div>
      </article>

      <article class="topic-card" id="topic-02-technical">
        <h3>Folders and multi-environment hierarchy segregation</h3>
        <p>Folders (<code>folders/&lt;folder_id&gt;</code>) are organizational containers nested beneath the Organization node. They enable architects to group related projects together to establish unified security baselines, delegate administration, and control cost aggregation.</p>

        <h4>Hierarchy Architecture Patterns: Environment-First vs. Business-Unit</h4>
        <p>When designing an enterprise landing zone, architects generally select between two foundational structural patterns:</p>
        <ul>
          <li><strong>Pattern A: Environment-First (Industry Best Practice):</strong> The top-level folders beneath the Organization node reflect lifecycle environments: <code>/Production</code>, <code>/Non-Production</code>, and <code>/Shared-Services</code>. Business units (e.g. <code>/Retail</code>, <code>/Bakery-Dispatch</code>) sit as child folders underneath each environment.
            <br><em>Advantage:</em> Guarantees absolute isolation between production and non-production. Developer credentials, test service accounts, and experimental policies applied in <code>/Non-Production</code> can never leak into production.</li>
          <li><strong>Pattern B: Business-Unit First:</strong> Top-level folders reflect company divisions (e.g. <code>/Retail-Franchise</code>, <code>/Supply-Chain</code>), with <code>/Prod</code> and <code>/Dev</code> nested inside each unit.
            <br><em>Trade-off:</em> Aligns with departmental cost centers, but increases the risk that an administrator accidentally grants broad permissions at the department folder, inadvertently compromising the nested production projects.</li>
        </ul>

        <h4>The Additive IAM Inheritance Evaluation Ladder</h4>
        <p>The defining rule of Google Cloud access control is that <strong>IAM permissions are strictly additive down the hierarchy</strong>. Effective permissions on any resource represent the mathematical union of all IAM policy bindings defined on that resource and all of its ancestor containers (Project, Folders, and Organization).</p>
        <p><strong>The Negative Permission Trap:</strong> <em>There is no concept of a "deny" in standard IAM role bindings.</em> If a developer group is granted <code>roles/editor</code> on a parent folder, granting that group <code>roles/viewer</code> on a child project does NOT restrict their access. The user retains full Editor rights on the child project because the folder-level grant remains active in the policy union.</p>

        <div class="table-wrap">
          <table>
            <caption>Folder Hierarchy Structuring Strategies &amp; Inheritance Patterns</caption>
            <thead>
              <tr>
                <th scope="col">Design Dimension</th>
                <th scope="col">Environment-First Model</th>
                <th scope="col">Business-Unit First Model</th>
                <th scope="col">Inheritance Behavior</th>
                <th scope="col">Architectural Recommendation</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th scope="row">Top-Level Grouping</th>
                <td><code>/Production</code>, <code>/Non-Prod</code></td>
                <td><code>/Retail</code>, <code>/Logistics</code></td>
                <td>Policies inherit to all child branches</td>
                <td>Adopt Environment-First to guarantee production blast radius containment.</td>
              </tr>
              <tr>
                <th scope="row">IAM Role Scope</th>
                <td>Strict SRE roles on Prod; Dev roles on Non-Prod</td>
                <td>Departmental leads hold folder roles</td>
                <td>Union evaluation (Role on Parent + Role on Child)</td>
                <td>Never grant mutating roles (Editor/Owner) at folder level; assign at project level.</td>
              </tr>
              <tr>
                <th scope="row">Org Policy Scope</th>
                <td>Uniform security posture per stage</td>
                <td>Policies customized per department</td>
                <td>Inherited by default; can override or merge</td>
                <td>Enforce restrictive policies on <code>/Production</code>; permit sandboxing in <code>/Non-Prod</code>.</td>
              </tr>
              <tr>
                <th scope="row">Nesting Limits</th>
                <td>2 to 4 levels recommended</td>
                <td>3 to 5 levels common</td>
                <td>Maximum 300 levels supported by API</td>
                <td>Limit hierarchy depth to 3 levels to maintain cognitive clarity and auditability.</td>
              </tr>
            </tbody>
          </table>
        </div>

{fig2}

        <div class="further-study">
          <h4>Further Study · Primary Documentation</h4>
          <ul>
            <li><a href="https://cloud.google.com/resource-manager/docs/creating-managing-folders" target="_blank" rel="noopener noreferrer">Google Cloud Documentation: Creating and Managing Folders</a></li>
          </ul>
        </div>
      </article>

      <article class="topic-card" id="topic-03-technical">
        <h3>Projects: Project ID vs. project name vs. project number</h3>
        <p>A Project is the foundational container for all cloud infrastructure. A virtual machine, Cloud SQL instance, or GKE cluster cannot exist outside a project. Enterprise architects must rigorously distinguish between the three distinct identifiers associated with every Google Cloud project.</p>

        <h4>The Project Identifiers Triad</h4>
        <ol>
          <li><strong>Project ID (Immutable &amp; Globally Unique):</strong>
            <ul>
              <li><em>Format:</em> 6 to 30 characters consisting of lowercase letters, digits, and hyphens. Must begin with a letter.</li>
              <li><em>Characteristics:</em> Chosen by the administrator at creation. It is <strong>globally unique</strong> across all Google Cloud customers worldwide. Once created, a Project ID can never be modified.</li>
              <li><em>Use Cases:</em> Specified in all <code>gcloud</code> commands (<code>--project=&lt;id&gt;</code>), REST API URLs, Terraform configurations, and billing export queries.</li>
            </ul>
          </li>
          <li><strong>Project Name (Mutable &amp; User-Friendly):</strong>
            <ul>
              <li><em>Format:</em> 1 to 63 characters (can include spaces, mixed casing, and special characters).</li>
              <li><em>Characteristics:</em> A descriptive label chosen for display purposes. It is <strong>not globally unique</strong>; multiple projects can share the exact same name. It can be changed at any time by project editors.</li>
              <li><em>Use Cases:</em> Console navigation, billing reports, and human-readable dashboards. Never use Project Name in automation scripts or API calls.</li>
            </ul>
          </li>
          <li><strong>Project Number (Immutable &amp; Globally Unique Integer):</strong>
            <ul>
              <li><em>Format:</em> A 12-digit integer (e.g. <code>892019481029</code>).</li>
              <li><em>Characteristics:</em> Assigned automatically by Google Cloud during project provisioning. It is globally unique, permanent, and immutable.</li>
              <li><em>Use Cases:</em> Essential for internal Google Cloud operations, audit log routing, cross-project service linking, and <strong>Google-managed service agents</strong>.</li>
            </ul>
          </li>
        </ol>

        <h4>Google-Managed Service Agent Conventions</h4>
        <p>When Google Cloud services perform background operations on a customer\\'s behalf (e.g. Cloud Pub/Sub decrypting data with Cloud KMS, or Cloud Build pushing images to Artifact Registry), Google provisions a <strong>Google-managed service agent</strong> inside the project. These service accounts follow a strict naming convention derived directly from the <strong>Project Number</strong>:</p>
        <p><code>service-&lt;PROJECT_NUMBER&gt;@gcp-sa-pubsub.iam.gserviceaccount.com</code></p>
        <p>Attempting to construct service agent email addresses using the Project Name or Project ID results in invalid identities, failing cross-project IAM grants and breaking asynchronous event-driven pipelines.</p>

        <div class="table-wrap">
          <table>
            <caption>Project Identifiers Triad and Lifecycle Characteristics</caption>
            <thead>
              <tr>
                <th scope="col">Identifier</th>
                <th scope="col">Global Uniqueness</th>
                <th scope="col">Mutability</th>
                <th scope="col">Character Constraints</th>
                <th scope="col">Primary Operational Use Case</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th scope="row">Project ID</th>
                <td>Globally unique across all GCP tenants</td>
                <td><strong>Immutable</strong> (permanent once created)</td>
                <td>6–30 chars; lowercase, digits, hyphens; starts with letter</td>
                <td>CLI commands (<code>--project</code>), Terraform provider, REST API endpoints.</td>
              </tr>
              <tr>
                <th scope="row">Project Name</th>
                <td>Non-unique (can be duplicated)</td>
                <td><strong>Mutable</strong> (can be changed anytime)</td>
                <td>1–63 chars; mixed casing, spaces allowed</td>
                <td>Console UI display, human-readable billing views. Never in scripts.</td>
              </tr>
              <tr>
                <th scope="row">Project Number</th>
                <td>Globally unique across all GCP tenants</td>
                <td><strong>Immutable</strong> (assigned by Google)</td>
                <td>12-digit integer (system assigned)</td>
                <td>Google service agent identities (<code>service-NUM@...</code>), audit logs.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="further-study">
          <h4>Further Study · Primary Documentation</h4>
          <ul>
            <li><a href="https://cloud.google.com/resource-manager/docs/creating-managing-projects" target="_blank" rel="noopener noreferrer">Google Cloud Documentation: Creating and Managing Projects</a></li>
          </ul>
        </div>
      </article>
    </section>
'''

with open('scratch/day021/part2.html', 'w') as f:
    f.write(part2)

print('Part 2 written, length:', len(part2))
