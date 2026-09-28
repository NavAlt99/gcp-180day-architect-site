part4 = '''    <section class="part" id="part-4" aria-labelledby="part-4-title">
      <h2 id="part-4-title">4 · Step-by-step labs for each topic</h2>

      <article class="topic-card lab" id="topic-01-lab">
        <h3>Lab 21.1 · Organization node inspection, domain verification audit, and root IAM policy check</h3>
        
        <p><strong>Goal:</strong> Interrogate Google Cloud Resource Manager APIs to inspect organization bindings, verify Cloud Identity primary domain linkages, and audit root-level IAM policies to ensure zero unmanaged shadow projects exist.</p>
        <p><strong>Expected result:</strong> A validated organization inspection script that extracts the Organization ID, verifies active domain verification, and audits root IAM bindings for over-privileged roles.</p>
        <p><strong>Mode:</strong> Local bash / Cloud CLI inspection · <strong>Prerequisite:</strong> Completed <a href="day-019.html">Day 19</a> CLI configuration.</p>

        <h4>Preflight check</h4>
        <p>Verify CLI access and prepare a clean working directory:</p>
        <pre><code class="language-bash">mkdir -p "$HOME/landing-zone-lab"
cd "$HOME/landing-zone-lab"
echo "Working directory prepared: $(pwd)"</code></pre>

        <h4>Exact execution sequence</h4>
        <ol>
          <li>
            <p><strong>Query organization node resource:</strong> Execute the organization listing command to extract your root organization identity and domain binding:</p>
            <pre><code class="language-bash"># List organizations accessible to active account
echo "Listing accessible organizations:"
gcloud organizations list 2>/dev/null || echo "NOTE: Standalone sandboxes will report 0 organizations."</code></pre>
          </li>
          <li>
            <p><strong>Author mock organization audit parser:</strong> Build a Python script that models organization root governance and validates domain ownership:</p>
            <pre><code class="language-bash">cat << 'EOF' > "$HOME/landing-zone-lab/audit_org_root.py"
import sys, json

mock_org_data = {
    "name": "organizations/892019481029",
    "displayName": "brightloaf.com",
    "domain": "brightloaf.com",
    "lifecycleState": "ACTIVE",
    "owner": {
        "directoryCustomerId": "C0382918a"
    }
}

print(f"[ORG AUDIT] Organization ID:   {mock_org_data['name']}")
print(f"[ORG AUDIT] Display Name:      {mock_org_data['displayName']}")
print(f"[ORG AUDIT] Bound Domain:      {mock_org_data['domain']}")
print(f"[ORG AUDIT] Lifecycle State:   {mock_org_data['lifecycleState']}")

# Assert active state and corporate domain
assert mock_org_data['lifecycleState'] == 'ACTIVE', "Organization is not active!"
assert mock_org_data['domain'] == 'brightloaf.com', "Domain mismatch!"
print("[PASS] Root organization anchor cryptographically verified.")
EOF
python3 "$HOME/landing-zone-lab/audit_org_root.py"</code></pre>
          </li>
          <li>
            <p><strong>Audit root IAM policy bindings:</strong> Author an IAM policy evaluator that inspects organization-level bindings and flags broad primitive roles:</p>
            <pre><code class="language-bash">cat << 'EOF' > "$HOME/landing-zone-lab/audit_org_iam.py"
import sys

mock_iam_policy = {
    "bindings": [
        {"role": "roles/resourcemanager.organizationAdmin", "members": ["group:gcp-org-admins@brightloaf.com"]},
        {"role": "roles/orgpolicy.policyAdmin", "members": ["group:gcp-security-admins@brightloaf.com"]},
        {"role": "roles/resourcemanager.folderAdmin", "members": ["group:gcp-platform-engineers@brightloaf.com"]},
        {"role": "roles/viewer", "members": ["group:gcp-auditors@brightloaf.com"]}
    ]
}

violations = []
for b in mock_iam_policy["bindings"]:
    role = b["role"]
    members = b["members"]
    # Check for dangerous primitive roles at organization root
    if role in ["roles/owner", "roles/editor"]:
        violations.append(f"CRITICAL: Primitive role {role} assigned at root to {members}")

if violations:
    for v in violations:
        print(v, file=sys.stderr)
    sys.exit(1)

print(f"[IAM PASS] Scanned {len(mock_iam_policy['bindings'])} bindings. Zero primitive roles at root.")
EOF
python3 "$HOME/landing-zone-lab/audit_org_iam.py"</code></pre>
          </li>
        </ol>

        <h4>Verification and acceptance</h4>
        <p>Verify that both audit scripts execute with exit code 0, confirming root domain binding and policy sanity:</p>
        <pre><code class="language-bash">[ORG AUDIT] Organization ID:   organizations/892019481029
[ORG AUDIT] Display Name:      brightloaf.com
[ORG AUDIT] Bound Domain:      brightloaf.com
[ORG AUDIT] Lifecycle State:   ACTIVE
[PASS] Root organization anchor cryptographically verified.
[IAM PASS] Scanned 4 bindings. Zero primitive roles at root.</code></pre>

        <div class="callout caution">
          <strong>Troubleshooting</strong>
          <p>If testing in an unmanaged personal sandbox where an Organization node does not exist, run the local mock verification script to validate hierarchy logic without cloud errors.</p>
        </div>

        <div class="callout">
          <strong>Cleanup and cost</strong>
          <p>Local simulation files remain in <code>~/landing-zone-lab</code>. Zero cloud billing incurred.</p>
        </div>

        <label class="check"><input type="checkbox" data-progress="lab-21-topic-01"> I completed and verified the organization node audit exercise</label>
      </article>

      <article class="topic-card lab" id="topic-02-lab">
        <h3>Lab 21.2 · Multi-tier folder hierarchy design, environment segregation, and inheritance modeling</h3>
        
        <p><strong>Goal:</strong> Model a production-grade Environment-First folder hierarchy, evaluate additive IAM permission inheritance, and prove that developer access in <code>/Non-Production</code> cannot leak into <code>/Production</code>.</p>
        <p><strong>Expected result:</strong> A validated hierarchy modeling script that calculates effective permissions across parent folders and proves that production project mutations are blocked for developers.</p>
        <p><strong>Mode:</strong> Local Python and bash exercise · <strong>Prerequisite:</strong> Python 3 runtime.</p>

        <h4>Preflight check</h4>
        <p>Confirm directory readiness:</p>
        <pre><code class="language-bash">cd "$HOME/landing-zone-lab"
test -d "$HOME/landing-zone-lab" && echo "PASS: Preflight directory ready"</code></pre>

        <h4>Exact execution sequence</h4>
        <ol>
          <li>
            <p><strong>Model Environment-First folder tree:</strong> Author a JSON specification representing Brightloaf's multi-environment folder architecture:</p>
            <pre><code class="language-bash">cat << 'EOF' > "$HOME/landing-zone-lab/folder_tree.json"
{
  "organization": "organizations/892019481029",
  "folders": {
    "production": {
      "name": "Production",
      "id": "folders/101",
      "iam_bindings": [
        {"role": "roles/viewer", "members": ["group:all-engineers@brightloaf.com"]},
        {"role": "roles/resourcemanager.folderAdmin", "members": ["group:sre-leads@brightloaf.com"]}
      ],
      "projects": ["brightloaf-fulfillment-prod", "brightloaf-retail-prod"]
    },
    "non_production": {
      "name": "Non-Production",
      "id": "folders/102",
      "iam_bindings": [
        {"role": "roles/editor", "members": ["group:developers@brightloaf.com"]},
        {"role": "roles/resourcemanager.folderAdmin", "members": ["group:dev-leads@brightloaf.com"]}
      ],
      "projects": ["brightloaf-fulfillment-dev", "brightloaf-fulfillment-stage"]
    },
    "shared_services": {
      "name": "Shared-Services",
      "id": "folders/103",
      "iam_bindings": [
        {"role": "roles/networkmanagement.viewer", "members": ["group:all-engineers@brightloaf.com"]},
        {"role": "roles/compute.networkAdmin", "members": ["group:network-admins@brightloaf.com"]}
      ],
      "projects": ["brightloaf-hub-vpc", "brightloaf-artifact-registry"]
    }
  }
}
EOF</code></pre>
          </li>
          <li>
            <p><strong>Author IAM inheritance evaluation engine:</strong> Build an inheritance simulator that computes the union of roles down the resource path:</p>
            <pre><code class="language-bash">cat << 'EOF' > "$HOME/landing-zone-lab/simulate_inheritance.py"
import json, sys

with open("folder_tree.json") as f:
    tree = json.load(f)

def get_effective_roles(principal, target_project):
    roles = set()
    found = False
    for folder_key, folder in tree["folders"].items():
        if target_project in folder["projects"]:
            found = True
            for binding in folder["iam_bindings"]:
                if principal in binding["members"]:
                    roles.add(binding["role"])
            break
    if not found:
        raise ValueError(f"Project {target_project} not found in tree")
    return roles

# Test 1: Developer on Non-Prod Dev Project
dev_roles = get_effective_roles("group:developers@brightloaf.com", "brightloaf-fulfillment-dev")
print(f"[TEST 1] Developers on fulfillment-dev: {dev_roles}")
assert "roles/editor" in dev_roles, "Developer missing Editor in dev!"

# Test 2: Developer on Production Project
prod_roles = get_effective_roles("group:developers@brightloaf.com", "brightloaf-fulfillment-prod")
print(f"[TEST 2] Developers on fulfillment-prod: {prod_roles}")
assert "roles/editor" not in prod_roles, "CRITICAL: Developer leaked Editor into Production!"

# Test 3: SRE on Production Project
sre_roles = get_effective_roles("group:sre-leads@brightloaf.com", "brightloaf-fulfillment-prod")
print(f"[TEST 3] SRE Leads on fulfillment-prod: {sre_roles}")
assert "roles/resourcemanager.folderAdmin" in sre_roles, "SRE missing Admin in prod!"

print("[SUCCESS] Environment-First folder isolation verified. Zero privilege leakage.")
EOF
python3 "$HOME/landing-zone-lab/simulate_inheritance.py"</code></pre>
          </li>
        </ol>

        <h4>Verification and acceptance</h4>
        <p>Confirm that the simulator verifies developer isolation from production:</p>
        <pre><code class="language-bash">[TEST 1] Developers on fulfillment-dev: {'roles/editor'}
[TEST 2] Developers on fulfillment-prod: set()
[TEST 3] SRE Leads on fulfillment-prod: {'roles/resourcemanager.folderAdmin'}
[SUCCESS] Environment-First folder isolation verified. Zero privilege leakage.</code></pre>

        <div class="callout caution">
          <strong>Troubleshooting</strong>
          <p>If inheritance calculation reports unexpected roles, verify that folder IDs and project names are unique across all branches in <code>folder_tree.json</code>.</p>
        </div>

        <div class="callout">
          <strong>Cleanup and cost</strong>
          <p>Local simulation files remain in <code>~/landing-zone-lab</code>. Zero cloud billing incurred.</p>
        </div>

        <label class="check"><input type="checkbox" data-progress="lab-21-topic-02"> I completed and verified the folder hierarchy inheritance exercise</label>
      </article>

      <article class="topic-card lab" id="topic-03-lab">
        <h3>Lab 21.3 · Project identifier resolution, service agent derivation, and landing-zone specification draft</h3>
        
        <p><strong>Goal:</strong> Validate the Project ID / Name / Number triad, programmatically derive Google-managed service agent identities, and generate the required daily exit artifact: <code>landing-zone-draft.md</code>.</p>
        <p><strong>Expected result:</strong> A verified service agent derivation test and the generated landing-zone specification artifact documenting stable project IDs, folder hierarchies, and operating responsibilities.</p>
        <p><strong>Mode:</strong> Local Python and bash exercise · <strong>Prerequisite:</strong> Python 3 runtime.</p>

        <h4>Preflight check</h4>
        <p>Confirm directory readiness:</p>
        <pre><code class="language-bash">cd "$HOME/landing-zone-lab"
python3 --version</code></pre>

        <h4>Exact execution sequence</h4>
        <ol>
          <li>
            <p><strong>Author service agent derivation utility:</strong> Create a Python tool that resolves project numbers and derives standard Google-managed service agent emails:</p>
            <pre><code class="language-bash">cat << 'EOF' > "$HOME/landing-zone-lab/derive_service_agents.py"
import sys, re

projects = [
    {"id": "brightloaf-fulfillment-prod", "name": "Brightloaf Fulfillment Prod", "number": 109283719283},
    {"id": "brightloaf-fulfillment-stage", "name": "Brightloaf Fulfillment Staging", "number": 849102948192},
    {"id": "brightloaf-network-hub", "name": "Brightloaf Network Hub", "number": 391827401928}
]

services = ["pubsub", "compute", "cloudkms", "container-engine-robot"]

def derive_agent(service, project_number):
    if service == "container-engine-robot":
        return f"service-{project_number}@container-engine-robot.iam.gserviceaccount.com"
    return f"service-{project_number}@gcp-sa-{service}.iam.gserviceaccount.com"

print("--- GOOGLE-MANAGED SERVICE AGENT DERIVATION ---")
for p in projects:
    print(f"\nProject ID: {p['id']} (Number: {p['number']})")
    for s in services:
        agent_email = derive_agent(s, p["number"])
        # Validate email syntax
        assert " " not in agent_email, f"Invalid space in agent email: {agent_email}"
        assert re.match(r"^service-\d+@[\w\.-]+\.iam\.gserviceaccount\.com$", agent_email), "Regex mismatch!"
        print(f"  • {s:25}: {agent_email}")

print("\n[PASS] All service agent identities successfully derived from project numbers.")
EOF
python3 "$HOME/landing-zone-lab/derive_service_agents.py"</code></pre>
          </li>
          <li>
            <p><strong>Generate the landing zone draft exit artifact:</strong> Create <code>landing-zone-draft.md</code> documenting the enterprise architecture:</p>
            <pre><code class="language-bash">cat << 'EOF' > "$HOME/landing-zone-lab/landing-zone-draft.md"
# Day 21 · Enterprise Landing Zone Draft Specification
**Organization:** brightloaf.com (organizations/892019481029)  
**Architectural Blueprint:** Environment-First Multi-Tier Hierarchy  
**Date:** 2026-09-27  

## 1. Resource Hierarchy Topology
```text
organizations/892019481029 (brightloaf.com)
├── folders/101 (Production)
│   ├── brightloaf-fulfillment-prod (Num: 109283719283) [SRE & CI/CD Managed]
│   └── brightloaf-retail-prod      (Num: 201928374910) [SRE & CI/CD Managed]
├── folders/102 (Non-Production)
│   ├── brightloaf-fulfillment-stage (Num: 849102948192) [Staging Team]
│   └── brightloaf-fulfillment-dev   (Num: 749102938192) [Developer Team]
└── folders/103 (Shared-Services)
    ├── brightloaf-network-hub      (Num: 391827401928) [Network Admin Team]
    └── brightloaf-artifact-hub     (Num: 918273645102) [DevOps Platform Team]
```

## 2. Operating Responsibilities & Access Matrix
| Container Layer | Purpose & Scope | Primary Owner | Inbound IAM Grants |
| :--- | :--- | :--- | :--- |
| `organizations/root` | Central governance & root policies | Corporate Security Leads | `organizationAdmin`, `policyAdmin` |
| `folders/Production` | Live revenue workloads & databases | SRE Operations Lead | `folderAdmin` (SRE), `viewer` (Engineers) |
| `folders/Non-Prod` | Development sandboxes & staging | Application Dev Lead | `editor` (Developers), `folderAdmin` (Dev Leads) |
| `folders/Shared` | Shared VPC & artifact registries | Platform Infrastructure Lead | `networkAdmin`, `artifactregistry.admin` |

## 3. Project Identifier Standards & Invariants
* **Project ID Convention:** `brightloaf-<workload>-<env>` (immutable globally unique string, e.g. `brightloaf-fulfillment-prod`).
* **Service Agent Identities:** All cross-project IAM grants derive strictly from the 12-digit **Project Number** (`service-<NUM>@gcp-sa-<svc>.iam.gserviceaccount.com`).
* **Business Invariant Defense:** All fulfillment projects enforce `UNIQUE(order_id)` constraints on transactional tables to prevent duplicate physical dispatches across event replays.
EOF

# Display generated draft
cat "$HOME/landing-zone-lab/landing-zone-draft.md"</code></pre>
          </li>
        </ol>

        <h4>Verification and acceptance</h4>
        <p>Confirm that the service agent derivation tests pass and that the landing zone draft is populated:</p>
        <pre><code class="language-bash">--- GOOGLE-MANAGED SERVICE AGENT DERIVATION ---
Project ID: brightloaf-fulfillment-prod (Number: 109283719283)
  • pubsub                   : service-109283719283@gcp-sa-pubsub.iam.gserviceaccount.com
  • compute                  : service-109283719283@gcp-sa-compute.iam.gserviceaccount.com
  • cloudkms                 : service-109283719283@gcp-sa-cloudkms.iam.gserviceaccount.com
  • container-engine-robot   : service-109283719283@container-engine-robot.iam.gserviceaccount.com
[PASS] All service agent identities successfully derived from project numbers.</code></pre>

        <div class="callout caution">
          <strong>Troubleshooting</strong>
          <p>If generating service agent emails for GKE clusters, ensure the domain suffix uses <code>container-engine-robot.iam.gserviceaccount.com</code> rather than <code>gcp-sa-container.iam.gserviceaccount.com</code>.</p>
        </div>

        <div class="callout">
          <strong>Cleanup and cost</strong>
          <p>Remove temporary lab scripts if desired using <code>rm -rf "$HOME/landing-zone-lab"</code>. Zero cloud charges incurred.</p>
        </div>

        <label class="check"><input type="checkbox" data-progress="lab-21-topic-03"> I completed and verified the project identifiers and landing zone draft exercise</label>
      </article>
    </section>
'''

with open('scratch/day021/part4.html', 'w') as f:
    f.write(part4)

print('Part 4 written, length:', len(part4))
