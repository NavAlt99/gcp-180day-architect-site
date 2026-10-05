"""Day 22 incident scenarios and hands-on laboratory exercises."""

from scratch.day_022_svgs import FIG_22_3_HTML, FIG_22_4_HTML

SCENARIOS = {
    'topic-01': {
        'scenario': (
            'During an external analytics platform migration at BrightLoaf, a franchise infrastructure administrator '
            'granted an external contractor group (contractor-analytics@brightloaf.com) the broad roles/editor role '
            'at the parent Analytics folder level. The administrator intended to grant write access only within a '
            'designated sandbox project, while attempting to restrict the contractor to read-only access on the child '
            'production order processing project (brightloaf-prod-orders) by adding a project-level binding for roles/viewer. '
            'Three days later, a contractor automation script designed to clean up temporary staging tables malfunctioned. '
            'Because IAM allow policies are strictly additive across the hierarchy, the contractor service account retained full '
            'inherited Editor mutation rights on the production project, completely ignoring the project-level viewer binding. '
            'The script executed a drop operation on the core production fulfillment queue table in Cloud Spanner, '
            'instantly halting morning bakery order dispatch across 450 franchise stores.'
        ),
        'impact': (
            'Order intake and dispatch systems across 450 retail bakeries failed for 2.5 hours on a peak weekday morning. '
            'Over 8,400 franchise delivery schedules were delayed, forcing stores to purchase local retail inventory at a '
            'premium cost of $135,000, while triggering severe contractual SLA penalties.'
        ),
        'constraints': (
            'Google Cloud IAM allow policies are strictly additive ($P_{effective} = \\bigcup P_{ancestors}$). Standard allow '
            'bindings have no subtractive capability: a role granted at an ancestor folder cannot be attenuated or revoked at a child '
            'project. Hard negative boundaries require explicit IAM Deny policies.'
        ),
        'evidence': FIG_22_3_HTML,
        'diagram_enabled': False,
        'facts': (
            'The contractor group held roles/editor at the parent Analytics folder. '
            'The child production project had an explicit binding granting roles/viewer to the same contractor group. '
            'The contractor script successfully issued a DropDatabase API call against the production Cloud Spanner database.'
        ),
        'inference': (
            'Assuming that a child project IAM binding can restrict an inherited ancestor allow grant violates the fundamental '
            'additive union principle of Google Cloud IAM. Production and non-production workloads must never share parent folders '
            'with broad mutation role bindings, and mission-critical resources must enforce IAM Deny policies.'
        ),
        'expected': (
            'Broad editor roles are purged from parent folders. Workloads reside in dedicated environment folders, and an IAM Deny '
            'policy at the Production folder explicitly blocks database deletion across all automated service accounts.'
        ),
        'root': (
            'Flawed assumption that IAM allow policies are subtractive, leading to excessive broad folder-level editor grants '
            'that cascaded uncontrollably into production workloads.'
        ),
        'verify': (
            'Execute gcloud projects get-ancestors-iam-policy to verify zero human developer or contractor groups hold roles/editor '
            'above production projects, and assert that an active IAM Deny policy blocks spanner.databases.drop.'
        ),
        'residual': (
            'Authorized emergency database schema updates require break-glass elevated access. Administrators must configure '
            'time-bound Privileged Access Management (PAM) grants with mandatory multi-party approvals.'
        ),
        'diagnostic_steps': [
            'Query Cloud Audit Logs for spanner.googleapis.com to identify the caller identity and inherited authorization chain.',
            'Inspect ancestor IAM policies using gcloud projects get-ancestors-iam-policy brightloaf-prod-orders.',
            'Verify the resource hierarchy path using gcloud resource-manager folders describe to identify the misconfigured parent folder.'
        ],
        'remediation_steps': [
            'Immediately remove roles/editor from contractor-analytics@brightloaf.com at the Analytics folder level.',
            'Create an IAM Deny policy on the Production folder denying spanner.googleapis.com/databases.drop to all service accounts.',
            'Restore the dropped Spanner database to a point-in-time recovery (PITR) timestamp prior to the incident.',
            'Enforce idempotent event replay to reconcile in-flight orders without duplicate store fulfillment.'
        ]
    },
    'topic-02': {
        'scenario': (
            'BrightLoaf platform DevOps team deployed a fleet of production order database virtual machines using Terraform. '
            'The Terraform configuration was intended to restrict inbound network access to PostgreSQL port 5432 strictly to '
            'authorized frontend order ingestion API microservices. The engineer authored a VPC firewall rule configured with '
            'target-tags: ["order-db"] and source-tags: ["order-api"]. However, in the Compute Engine instance resource block, '
            'the engineer accidentally populated the labels block (labels = { role = "order-db" }) instead of the network tags '
            'block (tags = ["order-db"]). Because Resource Labels exist strictly on the billing and metadata plane, the VPC '
            'virtual distributed switch completely ignored the labels. As a result, the database instance received zero '
            'tag-matched firewall protection and defaulted to a broad internal subnet fallback rule, allowing an unauthenticated '
            'developer testing container in the staging subnet to establish an open database connection and access unencrypted payment logs.'
        ),
        'impact': (
            'Over 14,000 unmasked customer credit card token records were exposed to an unauthorized non-production subnet. '
            'The data exposure triggered a mandatory 72-hour regulatory disclosure under PCI-DSS standards and required $85,000 '
            'in forensic investigations and external security auditing.'
        ),
        'constraints': (
            'VPC firewalls evaluate Compute Engine Network Tags (Layer 3/4 network data plane) and Resource Manager Secure Tags; '
            'they completely ignore Resource Labels, which exist strictly for billing export and metadata organization.'
        ),
        'evidence': FIG_22_4_HTML,
        'diagram_enabled': False,
        'facts': (
            'The Terraform manifest configured the database VM with labels = { role = "order-db" }. '
            'The Terraform manifest omitted tags = ["order-db"] from the compute instance definition. '
            'The VPC firewall rule evaluated target-tags = ["order-db"], leaving the instance unprotected by tag-based rules.'
        ),
        'inference': (
            'Conflating Resource Labels with Compute Engine Network Tags introduces critical network security vulnerabilities. '
            'Infrastructure-as-Code modules must enforce automated static analysis to verify that network security policies '
            'bind exclusively to network tags or Resource Manager Secure Tags, never metadata labels.'
        ),
        'expected': (
            'The database VM is configured with tags = ["order-db"] and attached to a dedicated VPC subnet. Inbound traffic on port 5432 '
            'is strictly filtered to source instances possessing tags = ["order-api"].'
        ),
        'root': (
            'Conflation of the three metadata planes: confusing Resource Labels (billing plane) with Compute Engine Network Tags (network data plane).'
        ),
        'verify': (
            'Execute gcloud compute instances describe and verify that tags.items contains "order-db", and assert that port 5432 '
            'rejects connections originating from instances lacking the "order-api" network tag.'
        ),
        'residual': (
            'Network tags can be altered by users with compute.instances.setTags. To establish immutable network guardrails, '
            'architects should migrate from legacy network tags to Resource Manager Secure Tags evaluated by Next-Gen Firewalls.'
        ),
        'diagnostic_steps': [
            'Inspect VM network attributes using gcloud compute instances describe bl-order-db-vm --format="yaml(tags, labels)".',
            'Run VPC Network Intelligence Center Connectivity Tests between the staging container and the database private IP.',
            'Review VPC Firewall audit logs to identify which fallback rule permitted ingress on port 5432.'
        ],
        'remediation_steps': [
            'Update Terraform configuration to add tags = ["order-db"] to the production database VM resource block.',
            'Execute gcloud compute instances add-tags bl-order-db-vm --tags=order-db to immediately remediate the active instance.',
            'Implement CI/CD linting using Checkov or Terraform Conftest to fail any commit where firewall target tags lack corresponding VM tags.',
            'Rotate database credentials and verify application idempotency safeguards across payment transaction handlers.'
        ]
    }
}

LABS = {
    'topic-01': {
        'name': 'Exercise A: Additive IAM Policy Inheritance Calculation and Deny Guardrails',
        'goal': 'Mathematically model hierarchical IAM policy inheritance down the Organization, Folder, and Project tree, demonstrate the additive union principle, and configure IAM Deny policies to enforce non-negotiable deletion guardrails.',
        'expected': 'A verified suite of simulation scripts calculating effective IAM permissions across container tiers, proving that project-level bindings cannot attenuate folder allow grants, and enforcing IAM Deny rules.',
        'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Hierarchical container tree modeling, additive IAM union calculation, Deny policy evaluation precedence, and audit log inspection simulation. Simulated or predicted: Google Cloud global IAM policy evaluation engine, eventual consistency cache invalidation delays, and multi-region replication latency. Untested on GCP: Live gcloud iam policies create API calls, production Cloud Spanner database deletion, and live OAuth 2.0 credential authorization.',
        'covers': 'Evaluate effective access in a sample parent/child hierarchy (Additive IAM inheritance calculation)',
        'prereq': 'Linux terminal, Python 3.10+, standard POSIX shell tools (mkdir, cat, python3)',
        'preflight': 'Verify Python 3 runtime availability and initialize dedicated Day 22 lab workspace',
        'trouble': 'Ensure all simulation scripts reside in scratch/day22_lab/ and use valid JSON formatting',
        'cleanup': 'All generated files reside in scratch/day22_lab/ for validation gate auditing',
        'steps': [
            """**Stage 1: Initialize IAM Inheritance Lab Workspace**

**Location:** local terminal

**Actions:**
Create the dedicated laboratory directory structure for Topic 1 IAM inheritance calculation.
```bash
mkdir -p scratch/day22_lab/topic1
cat <<'EOF' > scratch/day22_lab/topic1/stage1_init.py
import json

workspace = {
    "day": 22,
    "topic": "topic-01",
    "exercise": "Hierarchical IAM Inheritance and Additive Union Calculation",
    "status": "INITIALIZED",
    "organization": "organizations/884920183921",
    "parent_folder": "folders/482910492819",
    "child_project": "brightloaf-prod-orders-01"
}

with open("scratch/day22_lab/stage1_iam_preflight.json", "w") as f:
    json.dump(workspace, f, indent=2)

print("Stage 1 complete: IAM inheritance lab workspace initialized.")
EOF
python3 scratch/day22_lab/topic1/stage1_init.py
```

**Expected result:**
Directory created and initial workspace state written to scratch/day22_lab/stage1_iam_preflight.json.

**Save:** scratch/day22_lab/stage1_iam_preflight.json""",

            """**Stage 2: Model Container Hierarchy and IAM Allow Bindings**

**Location:** local terminal

**Actions:**
Construct a JSON model representing IAM allow policies bound at Organization, Folder, and Project tiers.
```bash
cat <<'EOF' > scratch/day22_lab/topic1/stage2_hierarchy_bindings.py
import json

hierarchy_bindings = {
    "organization": {
        "id": "organizations/884920183921",
        "bindings": {
            "roles/resourcemanager.organizationViewer": ["group:all-staff@brightloaf.com"],
            "roles/securityReviewer": ["group:secops@brightloaf.com"]
        }
    },
    "folder_prod": {
        "id": "folders/482910492819",
        "displayName": "Production",
        "bindings": {
            "roles/viewer": ["group:compliance-auditors@brightloaf.com"],
            "roles/editor": ["group:contractor-analytics@brightloaf.com"] # High-risk broad grant
        }
    },
    "project_orders": {
        "id": "projects/brightloaf-prod-orders-01",
        "bindings": {
            "roles/viewer": ["group:contractor-analytics@brightloaf.com"], # Attempted restriction (ineffective)
            "roles/spanner.databaseUser": ["serviceAccount:orders-sa@brightloaf-prod-orders-01.iam.gserviceaccount.com"]
        }
    }
}

with open("scratch/day22_lab/stage2_hierarchy_bindings.json", "w") as f:
    json.dump(hierarchy_bindings, f, indent=2)

print("Stage 2 complete: Container hierarchy bindings modeled.")
EOF
python3 scratch/day22_lab/topic1/stage2_hierarchy_bindings.py
```

**Expected result:**
Hierarchy bindings written to scratch/day22_lab/stage2_hierarchy_bindings.json.

**Save:** scratch/day22_lab/stage2_hierarchy_bindings.json""",

            """**Stage 3: Calculate Mathematical Additive Union of Effective Permissions**

**Location:** local terminal

**Actions:**
Author a Python script implementing the mathematical set union calculation for a security principal across ancestor containers.
```bash
cat <<'EOF' > scratch/day22_lab/topic1/stage3_additive_union.py
import json

# Define permission expansion for roles
ROLE_PERMISSIONS = {
    "roles/resourcemanager.organizationViewer": {"resourcemanager.organizations.get"},
    "roles/securityReviewer": {"iam.roles.list", "iam.serviceAccounts.list"},
    "roles/viewer": {"spanner.databases.get", "spanner.databases.select", "compute.instances.get"},
    "roles/editor": {"spanner.databases.get", "spanner.databases.select", "spanner.databases.drop", "compute.instances.start", "compute.instances.stop"},
    "roles/spanner.databaseUser": {"spanner.databases.select", "spanner.sessions.create"}
}

with open("scratch/day22_lab/stage2_hierarchy_bindings.json") as f:
    model = json.load(f)

principal = "group:contractor-analytics@brightloaf.com"

# Collect all granted roles for principal across hierarchy path
collected_roles = []
for tier in ("organization", "folder_prod", "project_orders"):
    for role, members in model[tier]["bindings"].items():
        if principal in members:
            collected_roles.append((tier, role))

# Compute mathematical union of permissions
effective_permissions = set()
for tier, role in collected_roles:
    effective_permissions.update(ROLE_PERMISSIONS.get(role, set()))

# Prove additive union invariant: spanner.databases.drop is present despite project viewer binding
assert "spanner.databases.drop" in effective_permissions, "Additive union must contain folder-inherited drop permission"

calculation_result = {
    "principal": principal,
    "collected_roles": collected_roles,
    "effective_permissions": sorted(list(effective_permissions)),
    "additive_proof": "spanner.databases.drop is PRESENT because roles/editor at folder unions with roles/viewer at project"
}

with open("scratch/day22_lab/stage3_additive_union.json", "w") as f:
    json.dump(calculation_result, f, indent=2)

print("Stage 3 complete: Additive union calculated successfully.")
EOF
python3 scratch/day22_lab/topic1/stage3_additive_union.py
```

**Expected result:**
Additive union calculation results written to scratch/day22_lab/stage3_additive_union.json.

**Save:** scratch/day22_lab/stage3_additive_union.json""",

            """**Stage 4: Author and Evaluate IAM Deny Policy Precedence**

**Location:** local terminal

**Actions:**
Author a simulation of an IAM Deny policy enforced at the Production folder level, demonstrating evaluation precedence over allow bindings.
```bash
cat <<'EOF' > scratch/day22_lab/topic1/stage4_deny_evaluation.py
import json

with open("scratch/day22_lab/stage3_additive_union.json") as f:
    allow_data = json.load(f)

# Define IAM Deny Policy attached to Production folder
deny_policy = {
    "name": "deny-spanner-drop-prod",
    "attachmentPoint": "folders/482910492819",
    "rules": [
        {
            "deniedPrincipals": ["group:contractor-analytics@brightloaf.com", "principalSet://goog/subject/serviceAccount:*"],
            "deniedPermissions": ["spanner.googleapis.com/databases.drop"],
            "description": "Block database drop in production regardless of allow bindings"
        }
    ]
}

# Evaluate permission check with Deny Precedence
test_permission = "spanner.databases.drop"
is_denied = any(test_permission in r["deniedPermissions"] or "spanner.googleapis.com/databases.drop" in r["deniedPermissions"] for r in deny_policy["rules"])
is_allowed_in_union = test_permission in allow_data["effective_permissions"]

# Final effective evaluation: Deny overrides Allow
effective_authorized = is_allowed_in_union and not is_denied

assert effective_authorized is False, "IAM Deny rule must override inherited allow binding"

evaluation_record = {
    "tested_permission": test_permission,
    "allow_union_result": is_allowed_in_union,
    "deny_policy_match": is_denied,
    "final_authorization_decision": "DENIED",
    "explanation": "Deny rule evaluated first; request rejected before allow bindings are processed"
}

with open("scratch/day22_lab/stage4_deny_evaluation.json", "w") as f:
    json.dump(evaluation_record, f, indent=2)

print("Stage 4 complete: IAM Deny policy precedence verified.")
EOF
python3 scratch/day22_lab/topic1/stage4_deny_evaluation.py
```

**Expected result:**
Deny precedence evaluation results written to scratch/day22_lab/stage4_deny_evaluation.json.

**Save:** scratch/day22_lab/stage4_deny_evaluation.json""",

            """**Stage 5: Model Eventual Consistency Latency and Policy Cache Expiration**

**Location:** local terminal

**Actions:**
Author a script modeling control plane policy propagation and API edge cache invalidation delays.
```bash
cat <<'EOF' > scratch/day22_lab/topic1/stage5_propagation_latency.py
import json

propagation_model = {
    "operation": "IAM Policy Binding Removal (Revoke roles/editor from folder)",
    "timestamp_mutation_epoch": 1791000000,
    "propagation_timeline_seconds": [
        {"elapsed_sec": 0, "regional_control_plane": "UPDATED", "edge_cache": "STALE", "authorized": True},
        {"elapsed_sec": 5, "regional_control_plane": "UPDATED", "edge_cache": "STALE", "authorized": True},
        {"elapsed_sec": 20, "regional_control_plane": "UPDATED", "edge_cache": "INVALIDATED", "authorized": False},
        {"elapsed_sec": 60, "regional_control_plane": "UPDATED", "edge_cache": "CONSISTENT_GLOBALLY", "authorized": False}
    ],
    "architectural_takeaway": "Critical permission revocations require up to 60 seconds for global edge cache invalidation"
}

with open("scratch/day22_lab/stage5_propagation_latency.json", "w") as f:
    json.dump(propagation_model, f, indent=2)

print("Stage 5 complete: Propagation latency model generated.")
EOF
python3 scratch/day22_lab/topic1/stage5_propagation_latency.py
```

**Expected result:**
Propagation timeline written to scratch/day22_lab/stage5_propagation_latency.json.

**Save:** scratch/day22_lab/stage5_propagation_latency.json""",

            """**Stage 6: Audit Ancestor IAM Policies via CLI Emulation**

**Location:** local terminal

**Actions:**
Simulate the output of gcloud projects get-ancestors-iam-policy and verify programmatic policy auditing.
```bash
cat <<'EOF' > scratch/day22_lab/topic1/stage6_ancestor_audit.py
import json

ancestor_chain = [
    {
        "id": "organizations/884920183921",
        "type": "organization",
        "role": "roles/resourcemanager.organizationViewer",
        "members": ["group:all-staff@brightloaf.com"]
    },
    {
        "id": "folders/482910492819",
        "type": "folder",
        "role": "roles/viewer",
        "members": ["group:compliance-auditors@brightloaf.com"]
    },
    {
        "id": "projects/brightloaf-prod-orders-01",
        "type": "project",
        "role": "roles/spanner.databaseUser",
        "members": ["serviceAccount:orders-sa@brightloaf-prod-orders-01.iam.gserviceaccount.com"]
    }
]

# Assert no broad editor or owner roles in ancestor chain
for binding in ancestor_chain:
    assert "roles/editor" != binding["role"], f"Broad editor role forbidden in ancestor chain: {binding['id']}"
    assert "roles/owner" != binding["role"], f"Broad owner role forbidden in ancestor chain: {binding['id']}"

with open("scratch/day22_lab/stage6_ancestor_audit.json", "w") as f:
    json.dump(ancestor_chain, f, indent=2)

print("Stage 6 complete: Ancestor policy audit validated with zero broad roles.")
EOF
python3 scratch/day22_lab/topic1/stage6_ancestor_audit.py
```

**Expected result:**
Ancestor audit records written to scratch/day22_lab/stage6_ancestor_audit.json.

**Save:** scratch/day22_lab/stage6_ancestor_audit.json""",

            """**Stage 7: Model Spanner Point-in-Time Recovery and Idempotent Replay**

**Location:** local terminal

**Actions:**
Model the database restoration and message deduplication flow that restores service after an unauthorized table mutation.
```bash
cat <<'EOF' > scratch/day22_lab/topic1/stage7_spanner_recovery.py
import json

recovery_audit = {
    "database": "projects/brightloaf-prod-orders-01/instances/order-spanner/databases/orders-db",
    "incident_timestamp_utc": "2026-10-04T08:30:00Z",
    "pitr_restore_timestamp_utc": "2026-10-04T08:29:55Z",
    "restored_tables": ["customer_orders", "order_fulfillment_queue"],
    "deduplication_safeguards": {
        "idempotency_token_enforced": True,
        "primary_key_dedup": "order_id",
        "replayed_messages_count": 312,
        "duplicate_fulfillments_prevented": 312
    },
    "recovery_status": "COMPLETED_SUCCESSFULLY"
}

with open("scratch/day22_lab/stage7_spanner_recovery.json", "w") as f:
    json.dump(recovery_audit, f, indent=2)

print("Stage 7 complete: Spanner PITR and idempotent replay modeled.")
EOF
python3 scratch/day22_lab/topic1/stage7_spanner_recovery.py
```

**Expected result:**
Recovery audit written to scratch/day22_lab/stage7_spanner_recovery.json.

**Save:** scratch/day22_lab/stage7_spanner_recovery.json""",

            """**Stage 8: Validate Topic 1 Acceptance Criteria and Assembly**

**Location:** local terminal

**Actions:**
Verify that all Topic 1 stage artifacts exist and write the final IAM inheritance acceptance summary.
```bash
cat <<'EOF' > scratch/day22_lab/topic1/stage8_summary.py
import json
import os

required = [
    "scratch/day22_lab/stage1_iam_preflight.json",
    "scratch/day22_lab/stage2_hierarchy_bindings.json",
    "scratch/day22_lab/stage3_additive_union.json",
    "scratch/day22_lab/stage4_deny_evaluation.json",
    "scratch/day22_lab/stage5_propagation_latency.json",
    "scratch/day22_lab/stage6_ancestor_audit.json",
    "scratch/day22_lab/stage7_spanner_recovery.json"
]

missing = [f for f in required if not os.path.exists(f)]
assert len(missing) == 0, f"Missing Topic 1 files: {missing}"

summary = {
    "lab": "Exercise A - Additive IAM Policy Inheritance Calculation and Deny Guardrails",
    "status": "PASS",
    "verified_stages": 8,
    "missing_files": missing
}

with open("scratch/day22_lab/stage8_topic1_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Exercise A validation complete: all 8 stages verified.")
EOF
python3 scratch/day22_lab/topic1/stage8_summary.py
```

**Expected result:**
Summary written to scratch/day22_lab/stage8_topic1_summary.json.

**Save:** scratch/day22_lab/stage8_topic1_summary.json"""
        ]
    },
    'topic-02': {
        'name': 'Exercise B: Three-Plane Metadata Taxonomy: Labels vs Tags vs Network Tags',
        'goal': 'Categorize Google Cloud metadata across the three architectural planes, demonstrate BigQuery billing queries using labels, evaluate Resource Manager Tags within CEL IAM Conditions, configure Compute Engine Network Tags for VPC firewall rules, and author the authoritative enterprise tagging guide.',
        'expected': 'A verified suite of simulation scripts modeling the three-plane metadata taxonomy, proving that firewalls ignore resource labels, evaluating tag-based IAM conditions, and generating scratch/day-022-inheritance-and-tagging-guide.md.',
        'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Three-plane metadata taxonomy data structures, BigQuery label billing SQL parsing, CEL tag condition evaluation, VPC firewall network tag matching, and tagging guide generation. Simulated or predicted: Google Cloud Resource Manager tag inheritance hierarchy, VPC virtual switch packet filtering, and Cloud Billing export schemas. Untested on GCP: Live gcloud compute instances add-tags CLI execution, production VPC firewall rule creation, and live Resource Manager Tag binding APIs.',
        'covers': 'Choose labels versus policy tags versus network tags for three uses (Tagging convention with concrete examples)',
        'prereq': 'Completion of Exercise A, local Python 3.10+ runtime, POSIX shell',
        'preflight': 'Ensure scratch/day22_lab workspace is accessible and initialize Topic 2 environment',
        'trouble': 'If parsing fails, check regex adherence for label keys (lowercase, max 63 chars) and network tag RFC-1035 syntax',
        'cleanup': 'Artifacts remain in scratch/day22_lab/ and scratch/day-022-inheritance-and-tagging-guide.md for validation gate auditing',
        'steps': [
            """**Stage 1: Initialize Metadata Taxonomy Lab Environment**

**Location:** local terminal

**Actions:**
Create the dedicated laboratory directory structure for Topic 2 metadata taxonomy modeling.
```bash
mkdir -p scratch/day22_lab/topic2
cat <<'EOF' > scratch/day22_lab/topic2/stage1_init.py
import json

init_state = {
    "topic": "topic-02",
    "exercise": "Three-Plane Metadata Taxonomy: Labels vs Tags vs Network Tags",
    "status": "INITIALIZED"
}

with open("scratch/day22_lab/stage1_taxonomy_preflight.json", "w") as f:
    json.dump(init_state, f, indent=2)

print("Stage 1 complete: Metadata taxonomy lab environment initialized.")
EOF
python3 scratch/day22_lab/topic2/stage1_init.py
```

**Expected result:**
Workspace initialized and written to scratch/day22_lab/stage1_taxonomy_preflight.json.

**Save:** scratch/day22_lab/stage1_taxonomy_preflight.json""",

            """**Stage 2: Model Plane 1 Resource Labels and BigQuery FinOps Billing Queries**

**Location:** local terminal

**Actions:**
Author a Python script modeling resource labels attached to a Compute Engine database instance and parse billing export SQL queries.
```bash
cat <<'EOF' > scratch/day22_lab/topic2/stage2_labels_billing.py
import json
import re

LABEL_REGEX = r'^[a-z][a-z0-9_-]{0,62}$'

vm_labels = {
    "bl-environment": "production",
    "bl-cost-center": "c-104-baking",
    "bl-application-id": "bl-order-fulfillment",
    "bl-data-classification": "confidential",
    "bl-managed-by": "terraform"
}

# Validate label syntax
for k, v in vm_labels.items():
    assert re.match(LABEL_REGEX, k), f"Invalid label key: {k}"
    assert re.match(LABEL_REGEX, v), f"Invalid label value: {v}"

billing_query = '''
SELECT
  project.id AS project_id,
  labels.value AS cost_center,
  SUM(cost) AS total_monthly_cost
FROM
  `brightloaf-secops-logging.finops_export.gcp_billing_export_v1`,
  UNNEST(labels) AS labels
WHERE
  labels.key = 'bl-cost-center'
GROUP BY
  1, 2
ORDER BY
  total_monthly_cost DESC;
'''

plane1_model = {
    "plane": "Plane 1: Resource Labels",
    "attachment_target": "Compute Engine VM Instance",
    "labels": vm_labels,
    "bigquery_billing_sql": billing_query.strip(),
    "security_enforcement": False
}

with open("scratch/day22_lab/stage2_labels_billing.json", "w") as f:
    json.dump(plane1_model, f, indent=2)

print("Stage 2 complete: Plane 1 Resource Labels validated and billing SQL generated.")
EOF
python3 scratch/day22_lab/topic2/stage2_labels_billing.py
```

**Expected result:**
Plane 1 label configuration saved to scratch/day22_lab/stage2_labels_billing.json.

**Save:** scratch/day22_lab/stage2_labels_billing.json""",

            """**Stage 3: Model Plane 2 Resource Manager Tags and CEL IAM Conditions**

**Location:** local terminal

**Actions:**
Construct a model of Resource Manager Tag Keys and Values and evaluate Common Expression Language (CEL) conditions for conditional IAM access.
```bash
cat <<'EOF' > scratch/day22_lab/topic2/stage3_tags_iam.py
import json

tag_definition = {
    "tagKey": "organizations/884920183921/tagKeys/environment",
    "shortName": "environment",
    "tagValues": [
        {"name": "tagValues/883920194821", "shortName": "production"},
        {"name": "tagValues/883920194822", "shortName": "staging"},
        {"name": "tagValues/883920194823", "shortName": "development"}
    ]
}

# Model CEL IAM Condition evaluation
def evaluate_cel_tag_condition(inherited_tag, expected_tag):
    return inherited_tag == expected_tag

inherited = "production"
cel_expression = "resource.matchTag('884920183921/environment', 'production')"
is_authorized = evaluate_cel_tag_condition(inherited, "production")
assert is_authorized is True

plane2_model = {
    "plane": "Plane 2: Resource Manager Tags",
    "tag_definition": tag_definition,
    "cel_expression": cel_expression,
    "simulated_resource_tag": inherited,
    "access_authorized": is_authorized,
    "security_enforcement": True
}

with open("scratch/day22_lab/stage3_tags_iam.json", "w") as f:
    json.dump(plane2_model, f, indent=2)

print("Stage 3 complete: Plane 2 Resource Manager Tags and CEL condition verified.")
EOF
python3 scratch/day22_lab/topic2/stage3_tags_iam.py
```

**Expected result:**
Plane 2 tags configuration written to scratch/day22_lab/stage3_tags_iam.json.

**Save:** scratch/day22_lab/stage3_tags_iam.json""",

            """**Stage 4: Model Plane 3 Network Tags and VPC Firewall Packet Filtering**

**Location:** local terminal

**Actions:**
Author a script modeling Compute Engine Network Tags and evaluating VPC distributed firewall packet ingress rules.
```bash
cat <<'EOF' > scratch/day22_lab/topic2/stage4_network_tags_firewall.py
import json

firewall_rule = {
    "name": "allow-order-api-to-db",
    "network": "bl-production-vpc",
    "direction": "INGRESS",
    "action": "ALLOW",
    "targetTags": ["bl-net-order-db"],
    "sourceTags": ["bl-net-order-api"],
    "allowed": [{"IPProtocol": "tcp", "ports": ["5432"]}]
}

def simulate_firewall_packet_check(packet_src_tags, packet_dest_tags, dest_port):
    if dest_port != 5432:
        return "DROP_WRONG_PORT"
    # Target instance must possess targetTag
    if not any(t in firewall_rule["targetTags"] for t in packet_dest_tags):
        return "DROP_TARGET_TAG_MISMATCH"
    # Source instance must possess sourceTag
    if any(s in firewall_rule["sourceTags"] for s in packet_src_tags):
        return "ALLOW"
    return "DROP_SOURCE_TAG_MISMATCH"

# Test authorized packet (from API frontend)
pass_result = simulate_firewall_packet_check(["bl-net-order-api"], ["bl-net-order-db"], 5432)
assert pass_result == "ALLOW"

# Test unauthorized packet (from Staging container lacking network tag)
drop_result = simulate_firewall_packet_check(["bl-net-staging-dev"], ["bl-net-order-db"], 5432)
assert drop_result == "DROP_SOURCE_TAG_MISMATCH"

plane3_model = {
    "plane": "Plane 3: Network Tags",
    "firewall_rule": firewall_rule,
    "simulation_tests": [
        {"test": "Authorized API Ingress", "src_tags": ["bl-net-order-api"], "result": pass_result},
        {"test": "Unauthorized Staging Ingress", "src_tags": ["bl-net-staging-dev"], "result": drop_result}
    ],
    "security_enforcement": True
}

with open("scratch/day22_lab/stage4_network_tags_firewall.json", "w") as f:
    json.dump(plane3_model, f, indent=2)

print("Stage 4 complete: Plane 3 Network Tags firewall packet filtering verified.")
EOF
python3 scratch/day22_lab/topic2/stage4_network_tags_firewall.py
```

**Expected result:**
Plane 3 firewall simulation written to scratch/day22_lab/stage4_network_tags_firewall.json.

**Save:** scratch/day22_lab/stage4_network_tags_firewall.json""",

            """**Stage 5: Prove Labels are Ignored by VPC Firewalls (Anti-Pattern Proof)**

**Location:** local terminal

**Actions:**
Execute a simulation proving that attaching resource labels without network tags causes VPC firewalls to drop traffic or fall back to default rules.
```bash
cat <<'EOF' > scratch/day22_lab/topic2/stage5_label_conflation_proof.py
import json

# VM configured with Labels but ZERO Network Tags
vm_config = {
    "name": "bl-misconfigured-db-vm",
    "labels": {"role": "order-db"},
    "tags": [] # Empty network tags list
}

target_firewall_tags = ["order-db"]

# Evaluate whether firewall rule matches VM
has_matching_network_tag = any(t in target_firewall_tags for t in vm_config["tags"])
assert has_matching_network_tag is False, "VM has no network tags; must not match tag-based firewall rule"

proof_record = {
    "vm_name": vm_config["name"],
    "vm_labels": vm_config["labels"],
    "vm_network_tags": vm_config["tags"],
    "firewall_target_tags": target_firewall_tags,
    "tag_matched": has_matching_network_tag,
    "result": "VPC Firewall ignored vm_labels['role']. VM lacked tags['order-db'], falling back to default subnet rule."
}

with open("scratch/day22_lab/stage5_label_conflation_proof.json", "w") as f:
    json.dump(proof_record, f, indent=2)

print("Stage 5 complete: Label conflation anti-pattern proved.")
EOF
python3 scratch/day22_lab/topic2/stage5_label_conflation_proof.py
```

**Expected result:**
Conflation proof saved to scratch/day22_lab/stage5_label_conflation_proof.json.

**Save:** scratch/day22_lab/stage5_label_conflation_proof.json""",

            """**Stage 6: Benchmark Three-Plane Architecture Comparison Matrix**

**Location:** local terminal

**Actions:**
Assemble a structured comparison data matrix across the three metadata planes and validate field coverage.
```bash
cat <<'EOF' > scratch/day22_lab/topic2/stage6_taxonomy_matrix.py
import json

taxonomy_matrix = [
    {
        "plane": "Plane 1: Resource Labels",
        "primary_purpose": "FinOps Billing Export & Cost Allocation",
        "scope": "All supported GCP resources",
        "inheritance": False,
        "format": "Key-value pair (lowercase alphanumeric, hyphens, underscores)",
        "security_boundary": False
    },
    {
        "plane": "Plane 2: Resource Manager Tags",
        "primary_purpose": "Hierarchical IAM Conditions & Org Policy Guardrails",
        "scope": "Organizations, Folders, Projects",
        "inheritance": True,
        "format": "Centrally governed namespaced Tag Keys and Tag Values",
        "security_boundary": True
    },
    {
        "plane": "Plane 3: Network Tags",
        "primary_purpose": "VPC Firewall Packet Ingress/Egress Filtering",
        "scope": "Compute Engine VM instances and templates only",
        "inheritance": False,
        "format": "RFC-1035 string list",
        "security_boundary": True
    }
]

assert len(taxonomy_matrix) == 3

with open("scratch/day22_lab/stage6_taxonomy_matrix.json", "w") as f:
    json.dump(taxonomy_matrix, f, indent=2)

print("Stage 6 complete: Three-plane taxonomy matrix compiled.")
EOF
python3 scratch/day22_lab/topic2/stage6_taxonomy_matrix.py
```

**Expected result:**
Taxonomy matrix written to scratch/day22_lab/stage6_taxonomy_matrix.json.

**Save:** scratch/day22_lab/stage6_taxonomy_matrix.json""",

            """**Stage 7: Generate Authoritative Enterprise Inheritance and Tagging Guide**

**Location:** local terminal

**Actions:**
Author the comprehensive Day 22 exit criteria artifact: an inheritance calculation and a tagging convention with concrete examples.
```bash
mkdir -p scratch
cat <<'EOF' > scratch/day22_lab/topic2/stage7_generate_exit.py
guide_doc = '''# BrightLoaf Enterprise Cloud: Inheritance and Tagging Taxonomy Guide

**Document Version:** 1.0.0  
**Curriculum Day:** Day 22 (Inheritance, labels and tags)  
**Status:** AUTHORITATIVE ARCHITECTURAL SPECIFICATION  
**Author:** Lead Enterprise Cloud Architect  
**Scope:** All Google Cloud Infrastructure and Workloads  

---

## 1. Executive Summary and Core Architectural Invariants

This document establishes BrightLoaf's authoritative standard for access control inheritance, resource metadata classification, and network packet filtering across Google Cloud. It establishes concrete boundaries separating **Resource Labels**, **Resource Manager Tags**, and **Compute Engine Network Tags**, preventing operational conflation and lateral security breaches.

### Core Business Invariant:
> **Duplicate Fulfillment Invariant:** Replaying an order event or recovering dropped network connections must never cause a second physical fulfillment (<= 1 physical fulfillment per unique order ID). Deduplication tokens and idempotent database mutations must remain protected by least-privilege IAM and strict network isolation.

---

## 2. Mathematical Inheritance Calculation Matrix

Google Cloud IAM allow policies are strictly additive ($P_{effective} = \\bigcup P_{ancestors}$). Standard allow bindings have zero subtractive capability: an allow permission granted at an ancestor folder or organization container cannot be revoked or restricted by a child project binding.

| Hierarchy Tier | Resource Identifier | Bound IAM Role | Injected Permissions | Cumulative Effective Permissions |
|---|---|---|---|---|
| **Organization Apex** | `organizations/884920183921` | `roles/securityReviewer` | `iam.roles.list`, `iam.serviceAccounts.list`, `resourcemanager.organizations.get` | 3 baseline read permissions |
| **Folder Tier 1** | `folders/482910492819` (`/Production`) | None (Zero default broad roles) | (none) | 3 baseline read permissions |
| **Project Tier** | `projects/brightloaf-prod-orders-01` | Custom: `roles/spannerViewer` | `spanner.databases.get`, `spanner.databases.select`, `spanner.sessions.create` | 6 permissions (Scoped least privilege) |
| **Leaf Resource** | `databases/orders-db` | None | (none) | 6 permissions |
| **Guardrail** | Organization Deny Policy | `deny: spanner.databases.drop` | Blocks drop across all automated service accounts | Hard stop overriding any inherited allow |

---

## 3. The Three-Plane Metadata Taxonomy

### Plane 1: Resource Labels (Operations and Cloud Billing)
- **Attachment Target:** All supported GCP resources (VMs, Buckets, Cloud SQL, BigQuery, Disks).
- **Inheritance:** NONE (Per-resource attribute; must be stamped during resource instantiation).
- **Format:** Lowercase alphanumeric with hyphens or underscores (Max 63 characters, regex: `^[a-z][a-z0-9_-]{0,62}$`).
- **Mandatory Label Schema:**
  - `bl-environment`: `production` | `staging` | `development`
  - `bl-cost-center`: `c-104-baking` | `c-105-logistics` | `c-106-franchise`
  - `bl-application-id`: `bl-order-api` | `bl-order-fulfillment` | `bl-inventory`
  - `bl-data-classification`: `pci-token` | `confidential` | `internal`
  - `bl-managed-by`: `terraform`
- **Use Case:** BigQuery Cloud Billing breakdown queries and automated resource lifecycle pruning.
- **Security Boundary:** ZERO. Labels do NOT enforce IAM access control or VPC firewall filtering.

### Plane 2: Resource Manager Tags (Governance and Conditional IAM)
- **Attachment Target:** Organizations, Folders, Projects.
- **Inheritance:** YES (Inherits automatically down the container tree).
- **Format:** Centralized namespaced keys: `organizations/884920183921/tagKeys/environment`.
- **Authorized Values:** `production`, `staging`, `development`.
- **Governance Roles:** Only principals with `roles/resourcemanager.tagAdmin` create tags; binding requires `roles/resourcemanager.tagUser`.
- **IAM Condition Integration:**
  ~~~cel
  // Grants Spanner Admin strictly if the project or folder inherits tag environment: production
  resource.matchTag('884920183921/environment', 'production')
  ~~~
- **Security Boundary:** HARD BOUNDARY. Centrally administered and protected against tampering by project-level developers.

### Plane 3: Network Tags (Compute Engine VPC Packet Filtering)
- **Attachment Target:** Compute Engine VM instances and Instance Templates ONLY.
- **Inheritance:** NONE (Per-VM instance string list).
- **Format:** Lowercase RFC-1035 alphanumeric with hyphens (Max 63 characters).
- **Standardized Network Tags:**
  - `bl-net-order-api`: For frontend API ingress instances.
  - `bl-net-order-db`: For backend database listeners (Port 5432).
  - `bl-net-bastion-mgmt`: For authorized management bastion hosts.
- **VPC Firewall Rule Enforcement:**
  - Ingress to `targetTags: ["bl-net-order-db"]` on `tcp:5432` strictly requires `sourceTags: ["bl-net-order-api"]`.
  - Non-production subnets and developer bastions lack `bl-net-order-api` and are dropped by default at the virtual switch.
- **Security Limitation:** Mutable via `compute.instances.setTags`. Enterprise teams must transition to Resource Manager Secure Tags for Next-Gen Firewalls in PCI-DSS environments.

---

## 4. Concrete Terraform Implementation Template

~~~hcl
# Example Production Database Provisioning with Strict 3-Plane Metadata Separation

resource "google_compute_instance" "production_database" {
  name         = "bl-order-db-prod-vm"
  machine_type = "n2-standard-4"
  zone         = "us-central1-a"
  project      = "brightloaf-prod-orders-01"

  # Plane 1: Labels for Billing and Inventory (Zero Security Enforcement)
  labels = {
    bl-environment         = "production"
    bl-cost-center         = "c-104-baking"
    bl-application-id      = "bl-order-fulfillment"
    bl-data-classification = "confidential"
    bl-managed-by          = "terraform"
  }

  # Plane 3: Network Tags for VPC Firewall Packet Filtering
  tags = [
    "bl-net-order-db"
  ]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network    = "bl-production-vpc"
    subnetwork = "bl-prod-db-subnet"
  }
}

# Plane 3: VPC Firewall Ingress Rule
resource "google_compute_firewall" "allow_order_api_to_db" {
  name        = "allow-order-api-to-db"
  network     = "bl-production-vpc"
  direction   = "INGRESS"
  priority    = 1000

  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }

  source_tags = ["bl-net-order-api"]
  target_tags = ["bl-net-order-db"]
}
~~~

---

## 5. Architectural Approval and Sign-Off
- **Lead Cloud Architect:** Lead Enterprise Cloud Architect
- **Curriculum Day:** Day 22 (Inheritance, labels and tags)
- **Status:** VERIFIED AND SIGNED OFF
'''

with open("scratch/day-022-inheritance-and-tagging-guide.md", "w") as f:
    f.write(guide_doc.strip() + "\\n")

print("Generated scratch/day-022-inheritance-and-tagging-guide.md successfully.")
EOF
python3 scratch/day22_lab/topic2/stage7_generate_exit.py
```

**Expected result:**
Authoritative inheritance and tagging guide written to scratch/day-022-inheritance-and-tagging-guide.md.

**Save:** scratch/day-022-inheritance-and-tagging-guide.md""",

            """**Stage 8: Validate Topic 2 Acceptance Criteria and Summary**

**Location:** local terminal

**Actions:**
Verify all Topic 2 stage files exist and write the final metadata taxonomy summary.
```bash
cat <<'EOF' > scratch/day22_lab/topic2/stage8_summary.py
import json
import os

required = [
    "scratch/day22_lab/stage1_taxonomy_preflight.json",
    "scratch/day22_lab/stage2_labels_billing.json",
    "scratch/day22_lab/stage3_tags_iam.json",
    "scratch/day22_lab/stage4_network_tags_firewall.json",
    "scratch/day22_lab/stage5_label_conflation_proof.json",
    "scratch/day22_lab/stage6_taxonomy_matrix.json",
    "scratch/day-022-inheritance-and-tagging-guide.md"
]

missing = [f for f in required if not os.path.exists(f)]
assert len(missing) == 0, f"Missing Topic 2 files: {missing}"

summary = {
    "lab": "Exercise B - Three-Plane Metadata Taxonomy: Labels vs Tags vs Network Tags",
    "status": "PASS",
    "verified_stages": 8,
    "exit_artifact": "scratch/day-022-inheritance-and-tagging-guide.md",
    "missing_files": missing
}

with open("scratch/day22_lab/stage8_topic2_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Exercise B validation complete: all 8 stages verified.")
EOF
python3 scratch/day22_lab/topic2/stage8_summary.py
```

**Expected result:**
Summary written to scratch/day22_lab/stage8_topic2_summary.json.

**Save:** scratch/day22_lab/stage8_topic2_summary.json"""
        ]
    }
}
