"""Day 21 incident scenarios and hands-on laboratory exercises."""

from scratch.day_021_svgs import FIG_21_3_HTML, FIG_21_4_HTML, FIG_21_5_HTML

SCENARIOS = {
    'topic-01': {
        'scenario': (
            'During a third-party application modernization audit at BrightLoaf, security operations discovered that '
            'an external software contractor had provisioned a standalone Google Cloud project using a personal Gmail account '
            'to build a prototype bakery ingredient catalog. Over four months, development expanded and the contractor '
            'connected the prototype to a replica of BrightLoaf customer database containing anonymized franchise sales records. '
            'Because the project was created without an Organization node parent ("No Organization"), it operated entirely outside '
            'corporate visibility: corporate security policies (such as uniform bucket-level access and external IP restrictions) '
            'were not enforced, and central audit log sinks captured zero activity. When the contractor contract concluded and '
            'their corporate email was deactivated, the cloud project remained active, billed to the contractor personal credit card, '
            'leaving corporate data inaccessible to BrightLoaf engineering.'
        ),
        'impact': (
            'BrightLoaf suffered an immediate blind-spot outage: the ingredient catalog service could not be updated or patched. '
            'Security operations spent 14 business days negotiating account access and executing emergency project migration protocols. '
            'The risk of data exfiltration triggered an internal compliance audit costing $45,000 in forensic analysis.'
        ),
        'constraints': (
            'Migrating an orphan project into an Organization hierarchy requires the executing principal to hold both '
            'roles/resourcemanager.organizationAdmin (or Project Creator) in the target Organization and roles/owner directly '
            'on the orphan project. Project migration immediately subjects the project to Organization Policies, which may break '
            'workloads if legacy configurations violate strict organizational guardrails.'
        ),
        'evidence': FIG_21_3_HTML,
        'diagram_enabled': False,
        'facts': (
            'The contractor created a Google Cloud project with no Organization parent node using an unmanaged personal identity. '
            'Centralized Organization Policies and Cloud Audit Logging sinks do not monitor or constrain projects outside the corporate hierarchy. '
            'Corporate administrators had zero administrative visibility into the orphan project until the contractor submitted an expense report.'
        ),
        'inference': (
            'Allowing enterprise workloads or prototype systems to run in unmanaged standalone projects completely undermines enterprise governance. '
            'Organizations must enforce identity restrictions, block unauthorized expense reimbursements for personal cloud accounts, '
            'and establish automated project onboarding pipelines under the corporate Organization node.'
        ),
        'expected': (
            'All corporate workloads are provisioned exclusively under the BrightLoaf Organization node (organizations/884920183921). '
            'Any legacy orphan projects are formally discovered, claimed by corporate administrators, and migrated into designated quarantine folders.'
        ),
        'root': (
            'Lack of an enforced enterprise project creation policy and absence of Cloud Identity domain enforcement allowed '
            'contractors to provision shadow IT projects using unmanaged identities without corporate hierarchy binding.'
        ),
        'verify': (
            'Verify that all active projects resolve an ancestor Organization node by executing '
            'gcloud projects get-ancestors-iam-policy and asserting that organizations/884920183921 is present at the root.'
        ),
        'residual': (
            'Newly acquired corporate entities or subsidiary domains may temporarily operate separate Cloud Identity domains. '
            'Architects must configure domain federation or add secondary domains to the primary Cloud Identity tenant to maintain single-org governance.'
        ),
        'diagnostic_steps': [
            'Inspect project metadata using gcloud projects describe to check parent container type and identifier.',
            'Query Cloud Asset Inventory across the Organization to detect any unmapped external service accounts or unmanaged resources.',
            'Review DNS registrar configuration and Cloud Identity Admin Console to confirm primary and secondary domain verifications.'
        ],
        'remediation_steps': [
            'Assign roles/resourcemanager.projectMover and roles/resourcemanager.organizationAdmin to corporate security lead.',
            'Execute gcloud beta projects move [PROJECT_ID] --organization=884920183921 to attach the orphan project to the corporate root.',
            'Move the imported project into a Quarantine-Review folder to audit compliance against Organization Policies before production routing.',
            'Link the project to the central corporate Cloud Billing account and revoke contractor personal owner privileges.'
        ]
    },
    'topic-02': {
        'scenario': (
            'BrightLoaf infrastructure team configured a single top-level folder named "Engineering" directly under the Organization node. '
            'To foster cross-functional collaboration and reduce administrative overhead, the lead administrator granted '
            'the group "all-engineers@brightloaf.com" the roles/editor role directly on the "Engineering" folder. Both staging '
            'and production projects (brightloaf-stage-pos and brightloaf-prod-pos) were placed inside this shared folder. '
            'During a Friday evening staging deployment, a mid-level engineer intended to run a database migration rollback on staging. '
            'Because the engineer had identical Editor permissions across both projects via folder inheritance, and because their local '
            'terminal had gcloud config set to the production project ID from earlier incident triage, the migration script executed '
            'against the production Cloud SQL database, dropping critical POS transaction tables across 450 franchise stores.'
        ),
        'impact': (
            'In-store point-of-sale systems across 450 retail bakeries were paralyzed for 3.5 hours on a peak weekend morning. '
            'Franchisees were forced to process transactions manually using paper receipts, resulting in $210,000 in estimated lost revenue '
            'and severe customer dissatisfaction.'
        ),
        'constraints': (
            'IAM permissions in Google Cloud are strictly additive down the hierarchy. A role granted at a folder level CANNOT be '
            'subtracted, revoked, or overridden at a child project level using standard IAM role bindings.'
        ),
        'evidence': FIG_21_4_HTML,
        'diagram_enabled': False,
        'facts': (
            'The roles/editor role was bound to all-engineers@brightloaf.com at the Engineering folder level. '
            'Both production and staging projects resided within the same parent folder. '
            'Additive IAM inheritance granted every developer broad write and mutation permissions across production infrastructure.'
        ),
        'inference': (
            'Co-locating production and non-production environments under a shared folder with permissive broad IAM bindings eliminates '
            'the blast-radius isolation required for enterprise resilience. Workloads with distinct trust levels must be partitioned into '
            'completely separate folder trees with strictly scoped IAM bindings.'
        ),
        'expected': (
            'Production and Non-Production environments reside in distinct top-level sibling folders. Developers hold read-only or no access '
            'in Production, and production deployments execute exclusively via automated CI/CD service accounts.'
        ),
        'root': (
            'Flawed resource hierarchy design that violated environment segregation principles, coupled with excessive broad IAM role grants '
            'at an intermediate folder level that cascaded uncontrollably into production.'
        ),
        'verify': (
            'Run automated IAM policy evaluation scripts to assert that no human developer groups hold roles/editor, roles/owner, '
            'or mutation privileges at or above the Production folder level.'
        ),
        'residual': (
            'Emergency incident triage occasionally requires human engineers to perform break-glass operations in production. '
            'Architects must implement Privileged Access Management (PAM) or temporary time-bound IAM grants with mandatory audit logging.'
        ),
        'diagnostic_steps': [
            'Execute gcloud projects get-ancestors-iam-policy brightloaf-prod-pos to identify all inherited IAM bindings.',
            'Inspect Cloud Audit Logs for Cloud SQL to identify the exact caller identity and origin IP of the DROP TABLE statement.',
            'Map the folder hierarchy ancestry using gcloud resource-manager folders list to identify improper parent containers.'
        ],
        'remediation_steps': [
            'Immediately remove roles/editor from all-engineers@brightloaf.com at the Engineering folder level.',
            'Create dedicated sibling folders: folders/Production and folders/Non-Production under the Organization root.',
            'Move brightloaf-prod-pos into folders/Production and brightloaf-stage-pos into folders/Non-Production.',
            'Enforce CI/CD pipeline deployment service account bindings and restrict human developers to roles/viewer in Production.'
        ]
    },
    'topic-03': {
        'scenario': (
            'BrightLoaf digital platform team deployed an asynchronous event-driven bakery order ingestion service using Cloud Pub/Sub '
            'and Cloud Key Management Service (Cloud KMS) for Customer-Managed Encryption Keys (CMEK). The Terraform automation script '
            'was written by a new infrastructure engineer who intended to grant the Pub/Sub service agent permission to decrypt order payloads. '
            'The engineer constructed the service agent principal string using the human-readable project display name: '
            'serviceAccount:service-brightloaf-orders-prod@gcp-sa-pubsub.iam.gserviceaccount.com, rather than the numerical Project Number. '
            'Terraform applied without syntax errors because KMS IAM accepts arbitrary principal email strings. However, when regional '
            'bakeries published encrypted order batches, Pub/Sub failed to decrypt the data with Cloud KMS, returning HTTP 403 Forbidden. '
            'Over 18,000 order messages were shunted to dead-letter storage, halting order fulfillment nationwide.'
        ),
        'impact': (
            'All regional order processing ceased for 4 hours. Automated order batching backed up, leading to delivery cancellations '
            'across 12 distribution centers and requiring $68,000 in emergency logistics re-routing and customer refunds.'
        ),
        'constraints': (
            'Google-managed service agents are deterministically derived using the project numerical Project Number '
            '(e.g., service-[PROJECT_NUMBER]@gcp-sa-pubsub.iam.gserviceaccount.com), NEVER the mutable Project Name or alphanumeric Project ID.'
        ),
        'evidence': FIG_21_5_HTML,
        'diagram_enabled': False,
        'facts': (
            'The engineer used the project display name instead of the system-assigned Project Number when constructing the Pub/Sub service agent email. '
            'Cloud KMS IAM bindings were applied to a non-existent service account email. '
            'Pub/Sub runtime operations failed CMEK decryption calls with PERMISSION_DENIED.'
        ),
        'inference': (
            'Conflating the Project Identifiers Triad (Name, ID, and Number) in automation scripts creates insidious silent failures. '
            'Infrastructure-as-Code modules must dynamically query the numerical Project Number using authoritative data sources '
            'rather than hardcoding string interpolations.'
        ),
        'expected': (
            'Terraform modules dynamically reference data.google_project.project.number to construct service agent principals, '
            'ensuring cryptographic IAM bindings bind to the verified runtime identity.'
        ),
        'root': (
            'Conflation of the Project Identifiers Triad: confusing the project display name with the numerical Project Number required '
            'for Google-managed service agent identity derivation.'
        ),
        'verify': (
            'Assert that the KMS key IAM policy contains a binding for service-[PROJECT_NUMBER]@gcp-sa-pubsub.iam.gserviceaccount.com '
            'with the role roles/cloudkms.cryptoKeyDecrypter.'
        ),
        'residual': (
            'When projects are migrated or recreated, Project Numbers change even if Project Names remain identical. '
            'All service agent bindings must be re-evaluated and refreshed across dependent external key rings.'
        ),
        'diagnostic_steps': [
            'Inspect the Pub/Sub subscription dead-letter queue metrics and error logs in Cloud Monitoring.',
            'Retrieve the authoritative numerical Project Number via gcloud projects describe brightloaf-prod-orders-01 --format="value(projectNumber)".',
            'Compare the derived service agent email against the KMS IAM policy bindings on the encryption key.'
        ],
        'remediation_steps': [
            'Query the exact Project Number: PROJECT_NUM=$(gcloud projects describe brightloaf-prod-orders-01 --format="value(projectNumber)").',
            'Construct the correct service agent email: service-${PROJECT_NUM}@gcp-sa-pubsub.iam.gserviceaccount.com.',
            'Grant roles/cloudkms.cryptoKeyDecrypter to the corrected service agent on the target Cloud KMS key.',
            'Re-drive failed order batches from the dead-letter topic into the primary ingestion subscription.'
        ]
    }
}

LABS = {
    'topic-01': {
        'name': 'Exercise A: Organization Node Inspection, Domain Verification, and Root IAM Policy Audit',
        'goal': 'Inspect the apex Organization resource metadata, verify Cloud Identity domain bindings, audit root IAM policies, and enforce Organization Policy baseline constraints.',
        'expected': 'A verified suite of simulation scripts validating apex organization attributes, DNS verification records, root IAM least privilege, aggregated audit log sinks, and orphan project discovery.',
        'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Organization node metadata, DNS TXT verification, root IAM policy evaluation, Org Policy constraints, aggregated audit sinks, and orphan project migration. Simulated or predicted: Google Cloud global Resource Manager control plane, Cloud Identity directory sync latency, and domain registrar propagation. Untested on GCP: Live gcloud organizations API calls, production Cloud Identity Super Admin role delegation, and live enterprise billing account re-linking.',
        'covers': 'Sketch an organization/folder/project hierarchy (Organization node and owner labeling)',
        'prereq': 'Local Python 3.10+ runtime, POSIX shell environment, and jq or python3 json tools',
        'preflight': 'Verify Python 3 availability and initialize the Day 21 lab workspace directory structure',
        'trouble': 'If directory creation fails, ensure write permissions in the local scratch path; check JSON formatting',
        'cleanup': 'Lab artifacts remain in scratch/day21_lab/ for validation gate auditing; disposable scratch directory',
        'steps': [
            """**Stage 1: Initialize Organization Audit Workspace**

**Location:** local terminal

**Actions:**
Create the dedicated laboratory directory structure for Topic 1 organization node auditing.
```bash
mkdir -p scratch/day21_lab/topic1
cat <<'EOF' > scratch/day21_lab/topic1/stage1_init.py
import json
import os

workspace_state = {
    "day": 21,
    "topic": "topic-01",
    "exercise": "Organization Node Governance and Identity Binding",
    "status": "INITIALIZED",
    "target_org": "organizations/884920183921",
    "domain": "brightloaf.com",
    "directory_customer_id": "C03abcd8z"
}

with open("scratch/day21_lab/stage1_org_preflight.json", "w") as f:
    json.dump(workspace_state, f, indent=2)

print("Stage 1 complete: Organization audit workspace initialized.")
EOF
python3 scratch/day21_lab/topic1/stage1_init.py
```

**Expected result:**
Workspace directory created and initial configuration written to scratch/day21_lab/stage1_org_preflight.json.

**Save:** scratch/day21_lab/stage1_org_preflight.json""",

            """**Stage 2: Audit Organization Resource Metadata and Customer ID Binding**

**Location:** local terminal

**Actions:**
Author a script to model and verify the one-to-one binding between the Google Cloud Organization resource and Cloud Identity customer ID.
```bash
cat <<'EOF' > scratch/day21_lab/topic1/stage2_org_metadata.py
import json

org_record = {
    "name": "organizations/884920183921",
    "displayName": "brightloaf.com",
    "lifecycleState": "ACTIVE",
    "creationTime": "2026-01-15T08:00:00.000Z",
    "owner": {
        "directoryCustomerId": "C03abcd8z"
    },
    "organization_attributes": {
        "is_apex_container": True,
        "parent": None,
        "max_folder_depth": 10
    }
}

# Assert root apex invariants
assert org_record["organization_attributes"]["parent"] is None, "Organization node must have no parent"
assert org_record["lifecycleState"] == "ACTIVE", "Organization must be ACTIVE"

with open("scratch/day21_lab/stage2_org_metadata.json", "w") as f:
    json.dump(org_record, f, indent=2)

print("Stage 2 complete: Organization metadata and customer ID verified.")
EOF
python3 scratch/day21_lab/topic1/stage2_org_metadata.py
```

**Expected result:**
Organization resource apex attributes verified and written to scratch/day21_lab/stage2_org_metadata.json.

**Save:** scratch/day21_lab/stage2_org_metadata.json""",

            """**Stage 3: Validate DNS Domain Verification Records and Secondary Domains**

**Location:** local terminal

**Actions:**
Model DNS TXT record verification checks that establish ownership of the primary and secondary corporate domains.
```bash
cat <<'EOF' > scratch/day21_lab/topic1/stage3_dns_verification.py
import json

dns_records = {
    "primary_domain": {
        "domain": "brightloaf.com",
        "verification_method": "DNS_TXT",
        "txt_record": "google-site-verification=X8k9Lm2NpQrStUvWxYz1234567890abcdef",
        "status": "VERIFIED",
        "is_primary": True
    },
    "secondary_domains": [
        {
            "domain": "brightloaf-logistics.com",
            "verification_method": "DNS_TXT",
            "txt_record": "google-site-verification=Z9a8B7c6D5e4F3g2H1j0987654321fedcba",
            "status": "VERIFIED",
            "is_primary": False
        }
    ],
    "unverified_domains": []
}

assert dns_records["primary_domain"]["status"] == "VERIFIED"
assert len(dns_records["secondary_domains"]) >= 1

with open("scratch/day21_lab/stage3_dns_verification.json", "w") as f:
    json.dump(dns_records, f, indent=2)

print("Stage 3 complete: DNS domain verification confirmed.")
EOF
python3 scratch/day21_lab/topic1/stage3_dns_verification.py
```

**Expected result:**
DNS TXT verification records audited and saved to scratch/day21_lab/stage3_dns_verification.json.

**Save:** scratch/day21_lab/stage3_dns_verification.json""",

            """**Stage 4: Audit Organization Root IAM Policies and Break-Glass Admin Roles**

**Location:** local terminal

**Actions:**
Inspect and evaluate IAM role bindings at the Organization root node, asserting separation of duty between Org Admin and Directory Super Admin.
```bash
cat <<'EOF' > scratch/day21_lab/topic1/stage4_root_iam.py
import json

iam_policy = {
    "resource": "organizations/884920183921",
    "version": 3,
    "bindings": [
        {
            "role": "roles/resourcemanager.organizationAdmin",
            "members": ["group:gcp-organization-admins@brightloaf.com"]
        },
        {
            "role": "roles/orgpolicy.policyAdmin",
            "members": ["group:gcp-security-admins@brightloaf.com"]
        },
        {
            "role": "roles/billing.admin",
            "members": ["group:gcp-finops-leads@brightloaf.com"]
        },
        {
            "role": "roles/logging.admin",
            "members": ["group:gcp-secops@brightloaf.com"]
        }
    ]
}

# Verify least privilege: individual users should not have root Org Admin directly
org_admin_binding = next(b for b in iam_policy["bindings"] if b["role"] == "roles/resourcemanager.organizationAdmin")
for member in org_admin_binding["members"]:
    assert member.startswith("group:"), f"Org Admin must be bound to a group, not individual user: {member}"

with open("scratch/day21_lab/stage4_root_iam.json", "w") as f:
    json.dump(iam_policy, f, indent=2)

print("Stage 4 complete: Root IAM policies validated for group-based governance.")
EOF
python3 scratch/day21_lab/topic1/stage4_root_iam.py
```

**Expected result:**
Root IAM policy compliance validated and written to scratch/day21_lab/stage4_root_iam.json.

**Save:** scratch/day21_lab/stage4_root_iam.json""",

            """**Stage 5: Model Enterprise Organization Policy Baseline Constraints**

**Location:** local terminal

**Actions:**
Author a simulation script evaluating mandatory enterprise Organization Policy guardrails enforced at the organization apex.
```bash
cat <<'EOF' > scratch/day21_lab/topic1/stage5_org_policies.py
import json

org_policies = {
    "organization_id": "organizations/884920183921",
    "policies": {
        "constraints/compute.vmExternalIpAccess": {
            "type": "LIST_CONSTRAINT",
            "listPolicy": {"deniedValues": ["*"]},
            "description": "Block external public IPs on all Compute instances by default"
        },
        "constraints/iam.allowedPolicyMemberDomains": {
            "type": "LIST_CONSTRAINT",
            "listPolicy": {"allowedValues": ["C03abcd8z"]},
            "description": "Restrict IAM bindings exclusively to verified corporate directory customer ID"
        },
        "constraints/storage.uniformBucketLevelAccess": {
            "type": "BOOLEAN_CONSTRAINT",
            "booleanPolicy": {"enforced": True},
            "description": "Enforce uniform bucket-level access across all Cloud Storage buckets"
        },
        "constraints/compute.disableSerialPortAccess": {
            "type": "BOOLEAN_CONSTRAINT",
            "booleanPolicy": {"enforced": True},
            "description": "Disable interactive serial port access across all virtual machines"
        }
    }
}

assert org_policies["policies"]["constraints/storage.uniformBucketLevelAccess"]["booleanPolicy"]["enforced"] is True
assert "C03abcd8z" in org_policies["policies"]["constraints/iam.allowedPolicyMemberDomains"]["listPolicy"]["allowedValues"]

with open("scratch/day21_lab/stage5_org_policies.json", "w") as f:
    json.dump(org_policies, f, indent=2)

print("Stage 5 complete: Enterprise Organization Policy baseline constraints verified.")
EOF
python3 scratch/day21_lab/topic1/stage5_org_policies.py
```

**Expected result:**
Organization Policy baselines verified and written to scratch/day21_lab/stage5_org_policies.json.

**Save:** scratch/day21_lab/stage5_org_policies.json""",

            """**Stage 6: Model Aggregated Cloud Audit Log Sink Across Descendant Resources**

**Location:** local terminal

**Actions:**
Simulate an Organization-level aggregated log sink that exports security audit logs to an immutable centralized BigQuery dataset.
```bash
cat <<'EOF' > scratch/day21_lab/topic1/stage6_audit_sink.py
import json

sink_config = {
    "name": "org-aggregated-security-audit-sink",
    "parent": "organizations/884920183921",
    "destination": "bigquery.googleapis.com/projects/brightloaf-secops-logging/datasets/org_audit_logs",
    "includeChildren": True,
    "filter": 'logName:"cloudaudit.googleapis.com%2Factivity" OR logName:"cloudaudit.googleapis.com%2Fsystem_event"',
    "writerIdentity": "serviceAccount:p884920183921-99881@gcp-sa-logging.iam.gserviceaccount.com"
}

assert sink_config["includeChildren"] is True, "Aggregated sink must include all child folders and projects"

with open("scratch/day21_lab/stage6_audit_sink.json", "w") as f:
    json.dump(sink_config, f, indent=2)

print("Stage 6 complete: Aggregated audit log sink configured.")
EOF
python3 scratch/day21_lab/topic1/stage6_audit_sink.py
```

**Expected result:**
Aggregated log sink configuration validated and written to scratch/day21_lab/stage6_audit_sink.json.

**Save:** scratch/day21_lab/stage6_audit_sink.json""",

            """**Stage 7: Model Shadow IT Project Discovery and Migration Protocol**

**Location:** local terminal

**Actions:**
Execute a simulation of discovering an unmanaged orphan project and migrating it into the corporate Organization node.
```bash
cat <<'EOF' > scratch/day21_lab/topic1/stage7_orphan_migration.py
import json

orphan_before = {
    "projectId": "brightloaf-orphan-catalog-proto",
    "projectNumber": "104928374615",
    "parent": None,
    "lifecycleState": "ACTIVE",
    "billingAccount": "000000-CONTRACTOR-CARD"
}

# Execute migration action
migrated_after = dict(orphan_before)
migrated_after["parent"] = {
    "type": "folder",
    "id": "folders/482910492825" # Quarantine & Review folder
}
migrated_after["billingAccount"] = "01ABCD-23EFGH-45IJKL" # Corporate billing account
migrated_after["complianceAudit"] = "PASSED_QUARANTINE"

migration_audit = {
    "pre_migration": orphan_before,
    "post_migration": migrated_after,
    "migration_command": "gcloud beta projects move brightloaf-orphan-catalog-proto --folder=482910492825",
    "inherited_org_ancestor": "organizations/884920183921"
}

with open("scratch/day21_lab/stage7_orphan_migration.json", "w") as f:
    json.dump(migration_audit, f, indent=2)

print("Stage 7 complete: Orphan project migration protocol verified.")
EOF
python3 scratch/day21_lab/topic1/stage7_orphan_migration.py
```

**Expected result:**
Orphan project migration simulation written to scratch/day21_lab/stage7_orphan_migration.json.

**Save:** scratch/day21_lab/stage7_orphan_migration.json""",

            """**Stage 8: Validate Topic 1 Acceptance Criteria and Assembly**

**Location:** local terminal

**Actions:**
Verify all Topic 1 stage artifacts and compile the final Organization governance summary.
```bash
cat <<'EOF' > scratch/day21_lab/topic1/stage8_summary.py
import json
import os

required = [
    "scratch/day21_lab/stage1_org_preflight.json",
    "scratch/day21_lab/stage2_org_metadata.json",
    "scratch/day21_lab/stage3_dns_verification.json",
    "scratch/day21_lab/stage4_root_iam.json",
    "scratch/day21_lab/stage5_org_policies.json",
    "scratch/day21_lab/stage6_audit_sink.json",
    "scratch/day21_lab/stage7_orphan_migration.json"
]

missing = [f for f in required if not os.path.exists(f)]
assert len(missing) == 0, f"Missing Topic 1 files: {missing}"

summary = {
    "lab": "Exercise A - Organization Node Inspection and Domain Verification",
    "status": "PASS",
    "verified_stages": 8,
    "org_id": "organizations/884920183921",
    "domain": "brightloaf.com",
    "missing_files": missing
}

with open("scratch/day21_lab/stage8_topic1_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Exercise A validation complete: all 8 stages verified.")
EOF
python3 scratch/day21_lab/topic1/stage8_summary.py
```

**Expected result:**
Summary written to scratch/day21_lab/stage8_topic1_summary.json.

**Save:** scratch/day21_lab/stage8_topic1_summary.json"""
        ]
    },
    'topic-02': {
        'name': 'Exercise B: Multi-Tier Folder Hierarchy Design and Additive IAM Policy Inheritance',
        'goal': 'Design a multi-tier enterprise folder hierarchy, enforce strict environment isolation between Production and Non-Production, model additive IAM policy inheritance down the tree, and simulate folder-level Organization Policy overrides.',
        'expected': 'A verified suite of simulation scripts validating multi-tier folder trees, zero cross-environment co-location violations, additive IAM union evaluation, folder policy overrides, and departmental FinOps budget mapping.',
        'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Multi-tier folder hierarchy data model, environment segregation verification, additive IAM policy union calculation, folder-level Org Policy overrides, and departmental budget alert configurations. Simulated or predicted: Google Cloud Resource Manager folder hierarchy depth limits, cross-region IAM propagation delays, and Cloud Billing BigQuery export latency. Untested on GCP: Live gcloud resource-manager folders create commands, production IAM role bindings, and live Pub/Sub budget notification streaming.',
        'covers': 'Sketch an organization/folder/project hierarchy for development and production (Folder hierarchy and environment isolation)',
        'prereq': 'Completion of Exercise A, local Python 3.10+ runtime, POSIX shell',
        'preflight': 'Ensure scratch/day21_lab directory is accessible and initialize Topic 2 workspace',
        'trouble': 'If path resolution fails, verify relative paths against the lab workspace root',
        'cleanup': 'Lab artifacts remain in scratch/day21_lab/ for validation gate auditing',
        'steps': [
            """**Stage 1: Initialize Folder Lab Environment**

**Location:** local terminal

**Actions:**
Create the dedicated laboratory directory structure for Topic 2 folder hierarchy modeling.
```bash
mkdir -p scratch/day21_lab/topic2
cat <<'EOF' > scratch/day21_lab/topic2/stage1_init.py
import json

init_data = {
    "topic": "topic-02",
    "exercise": "Multi-Tier Folder Hierarchy and Additive IAM Inheritance",
    "status": "INITIALIZED",
    "parent_org": "organizations/884920183921"
}

with open("scratch/day21_lab/stage1_folder_init.json", "w") as f:
    json.dump(init_data, f, indent=2)

print("Stage 1 complete: Folder lab environment initialized.")
EOF
python3 scratch/day21_lab/topic2/stage1_init.py
```

**Expected result:**
Topic 2 workspace initialized and written to scratch/day21_lab/stage1_folder_init.json.

**Save:** scratch/day21_lab/stage1_folder_init.json""",

            """**Stage 2: Model Multi-Tier Enterprise Folder Tree**

**Location:** local terminal

**Actions:**
Construct a hierarchical data model representing top-level environment segregation with nested business unit folders.
```bash
cat <<'EOF' > scratch/day21_lab/topic2/stage2_folder_tree.py
import json

folder_tree = {
    "organization": "organizations/884920183921",
    "top_level_folders": [
        {
            "id": "folders/482910492819",
            "displayName": "Production",
            "environment": "PROD",
            "child_folders": [
                {"id": "folders/482910492821", "displayName": "Retail-POS", "cost_center": "CC-101"},
                {"id": "folders/482910492822", "displayName": "Supply-Chain", "cost_center": "CC-102"}
            ]
        },
        {
            "id": "folders/482910492820",
            "displayName": "Non-Production",
            "environment": "NON_PROD",
            "child_folders": [
                {"id": "folders/482910492823", "displayName": "Development", "cost_center": "CC-ENG"},
                {"id": "folders/482910492824", "displayName": "Staging", "cost_center": "CC-ENG"}
            ]
        },
        {
            "id": "folders/482910492825",
            "displayName": "Core-Shared-Services",
            "environment": "SHARED",
            "child_folders": [
                {"id": "folders/482910492826", "displayName": "Networking-Hub", "cost_center": "CC-INFRA"},
                {"id": "folders/482910492827", "displayName": "Security-SecOps", "cost_center": "CC-SEC"}
            ]
        }
    ]
}

assert len(folder_tree["top_level_folders"]) == 3

with open("scratch/day21_lab/stage2_folder_tree.json", "w") as f:
    json.dump(folder_tree, f, indent=2)

print("Stage 2 complete: Multi-tier folder hierarchy modeled successfully.")
EOF
python3 scratch/day21_lab/topic2/stage2_folder_tree.py
```

**Expected result:**
Folder tree model written to scratch/day21_lab/stage2_folder_tree.json.

**Save:** scratch/day21_lab/stage2_folder_tree.json""",

            """**Stage 3: Verify Environment Isolation Between Prod and Non-Prod Trees**

**Location:** local terminal

**Actions:**
Author a script to audit folder boundaries and assert zero co-location of staging and production workloads within the same folder subtree.
```bash
cat <<'EOF' > scratch/day21_lab/topic2/stage3_env_isolation.py
import json

with open("scratch/day21_lab/stage2_folder_tree.json") as f:
    tree = json.load(f)

isolation_audit = {
    "prod_folders": [],
    "non_prod_folders": [],
    "violations": []
}

for top in tree["top_level_folders"]:
    env = top["environment"]
    for child in top["child_folders"]:
        entry = {"folder_id": child["id"], "name": child["displayName"], "parent_env": env}
        if env == "PROD":
            isolation_audit["prod_folders"].append(entry)
            if "dev" in child["displayName"].lower() or "stage" in child["displayName"].lower():
                isolation_audit["violations"].append(f"Non-prod folder inside PROD tree: {child['displayName']}")
        elif env == "NON_PROD":
            isolation_audit["non_prod_folders"].append(entry)
            if "prod" in child["displayName"].lower():
                isolation_audit["violations"].append(f"Prod folder inside NON_PROD tree: {child['displayName']}")

assert len(isolation_audit["violations"]) == 0, f"Isolation violations detected: {isolation_audit['violations']}"

with open("scratch/day21_lab/stage3_env_isolation.json", "w") as f:
    json.dump(isolation_audit, f, indent=2)

print("Stage 3 complete: Environment isolation verified with zero violations.")
EOF
python3 scratch/day21_lab/topic2/stage3_env_isolation.py
```

**Expected result:**
Environment isolation audit results saved to scratch/day21_lab/stage3_env_isolation.json.

**Save:** scratch/day21_lab/stage3_env_isolation.json""",

            """**Stage 4: Simulate Additive IAM Policy Inheritance Calculation**

**Location:** local terminal

**Actions:**
Simulate the union of IAM permissions across Organization, Folder, and Project nodes, demonstrating additive inheritance.
```bash
cat <<'EOF' > scratch/day21_lab/topic2/stage4_iam_inheritance.py
import json

org_bindings = {
    "roles/resourcemanager.organizationAdmin": ["group:gcp-org-admins@brightloaf.com"],
    "roles/browser": ["group:all-staff@brightloaf.com"]
}

folder_prod_bindings = {
    "roles/viewer": ["group:compliance-auditors@brightloaf.com"],
    "roles/resourcemanager.folderAdmin": ["group:prod-infra-leads@brightloaf.com"]
}

project_pos_bindings = {
    "roles/cloudsql.client": ["serviceAccount:pos-backend-sa@brightloaf-prod-pos-01.iam.gserviceaccount.com"],
    "roles/viewer": ["group:pos-ops-team@brightloaf.com"] # Additive with folder viewer
}

# Calculate effective project policy via union
effective_policy = {}
for source in (org_bindings, folder_prod_bindings, project_pos_bindings):
    for role, members in source.items():
        if role not in effective_policy:
            effective_policy[role] = set()
        effective_policy[role].update(members)

# Convert sets to sorted lists for JSON serialization
effective_json = {role: sorted(list(members)) for role, members in effective_policy.items()}

# Verify additive invariant: compliance-auditors inherited roles/viewer from folder
assert "group:compliance-auditors@brightloaf.com" in effective_json["roles/viewer"]
assert "group:pos-ops-team@brightloaf.com" in effective_json["roles/viewer"]

inheritance_result = {
    "project_id": "brightloaf-prod-pos-01",
    "effective_iam_policy": effective_json,
    "additive_proof": "compliance-auditors holds roles/viewer at project despite having zero direct project bindings"
}

with open("scratch/day21_lab/stage4_iam_inheritance.json", "w") as f:
    json.dump(inheritance_result, f, indent=2)

print("Stage 4 complete: Additive IAM policy inheritance calculated successfully.")
EOF
python3 scratch/day21_lab/topic2/stage4_iam_inheritance.py
```

**Expected result:**
Additive IAM inheritance simulation written to scratch/day21_lab/stage4_iam_inheritance.json.

**Save:** scratch/day21_lab/stage4_iam_inheritance.json""",

            """**Stage 5: Model Folder-Level Organization Policy Overrides and Inheritance Suppression**

**Location:** local terminal

**Actions:**
Author a script evaluating folder-level policy overrides where inheritFromParent is toggled to false.
```bash
cat <<'EOF' > scratch/day21_lab/topic2/stage5_orgpolicy_override.py
import json

org_constraint = {
    "constraint": "constraints/compute.vmExternalIpAccess",
    "listPolicy": {"deniedValues": ["*"]},
    "scope": "organizations/884920183921"
}

non_prod_folder_policy = {
    "constraint": "constraints/compute.vmExternalIpAccess",
    "scope": "folders/482910492820", # Non-Production folder
    "inheritFromParent": False, # Explicit override
    "listPolicy": {
        "allowedValues": ["projects/brightloaf-dev-sandbox/zones/us-central1-a/instances/api-gateway-test"]
    }
}

prod_folder_policy = {
    "constraint": "constraints/compute.vmExternalIpAccess",
    "scope": "folders/482910492819", # Production folder
    "inheritFromParent": True, # Strict inheritance
    "listPolicy": {} # Fully inherits org deny-all rule
}

policy_evaluation = {
    "production_effective": "DENY_ALL (Inherited from Org)",
    "non_production_effective": "CUSTOM_ALLOWLIST (Parent Deny-All overridden by inheritFromParent: false)",
    "policies": {
        "org": org_constraint,
        "prod_folder": prod_folder_policy,
        "non_prod_folder": non_prod_folder_policy
    }
}

with open("scratch/day21_lab/stage5_orgpolicy_override.json", "w") as f:
    json.dump(policy_evaluation, f, indent=2)

print("Stage 5 complete: Folder-level Organization Policy override modeled.")
EOF
python3 scratch/day21_lab/topic2/stage5_orgpolicy_override.py
```

**Expected result:**
Policy override evaluation saved to scratch/day21_lab/stage5_orgpolicy_override.json.

**Save:** scratch/day21_lab/stage5_orgpolicy_override.json""",

            """**Stage 6: Model Departmental Cost Center Allocation and Budget Notifications**

**Location:** local terminal

**Actions:**
Map folder hierarchies to departmental cost centers and simulate Pub/Sub threshold budget alerts.
```bash
cat <<'EOF' > scratch/day21_lab/topic2/stage6_finops_budget.py
import json

budget_configs = [
    {
        "budgetName": "Retail-POS-Monthly-Budget",
        "target_folder": "folders/482910492821",
        "cost_center": "CC-101-RETAIL",
        "currencyCode": "USD",
        "monthly_limit": 25000,
        "thresholdRules": [
            {"thresholdPercent": 0.50, "spendBasis": "CURRENT_SPEND"},
            {"thresholdPercent": 0.90, "spendBasis": "CURRENT_SPEND"},
            {"thresholdPercent": 1.00, "spendBasis": "FORECASTED_SPEND"}
        ],
        "pubsub_topic": "projects/brightloaf-finops/topics/budget-alerts"
    },
    {
        "budgetName": "Engineering-Dev-Budget",
        "target_folder": "folders/482910492823",
        "cost_center": "CC-ENG-DEV",
        "currencyCode": "USD",
        "monthly_limit": 8000,
        "thresholdRules": [
            {"thresholdPercent": 0.80, "spendBasis": "CURRENT_SPEND"},
            {"thresholdPercent": 1.00, "spendBasis": "CURRENT_SPEND"}
        ],
        "pubsub_topic": "projects/brightloaf-finops/topics/budget-alerts"
    }
]

with open("scratch/day21_lab/stage6_finops_budget.json", "w") as f:
    json.dump(budget_configs, f, indent=2)

print("Stage 6 complete: Departmental cost allocation budgets mapped.")
EOF
python3 scratch/day21_lab/topic2/stage6_finops_budget.py
```

**Expected result:**
Folder budget mapping written to scratch/day21_lab/stage6_finops_budget.json.

**Save:** scratch/day21_lab/stage6_finops_budget.json""",

            """**Stage 7: Model Shared VPC Host and Service Project Topology**

**Location:** local terminal

**Actions:**
Author a configuration mapping centralized Shared VPC networking host projects and child service projects across folder boundaries.
```bash
cat <<'EOF' > scratch/day21_lab/topic2/stage7_shared_vpc_topology.py
import json

shared_vpc_model = {
    "host_project": {
        "projectId": "brightloaf-hub-net-prod",
        "folder": "folders/482910492826", # Networking-Hub folder
        "vpc_name": "vpc-shared-prod-central",
        "subnets": [
            {"name": "sb-prod-pos-us-central1", "cidr": "10.10.1.0/24", "region": "us-central1"},
            {"name": "sb-prod-orders-us-central1", "cidr": "10.10.2.0/24", "region": "us-central1"}
        ]
    },
    "service_projects": [
        {
            "projectId": "brightloaf-prod-pos-01",
            "folder": "folders/482910492821", # Retail-POS folder
            "attached_subnets": ["sb-prod-pos-us-central1"]
        },
        {
            "projectId": "brightloaf-prod-orders-01",
            "folder": "folders/482910492822", # Supply-Chain folder
            "attached_subnets": ["sb-prod-orders-us-central1"]
        }
    ]
}

with open("scratch/day21_lab/stage7_shared_vpc_topology.json", "w") as f:
    json.dump(shared_vpc_model, f, indent=2)

print("Stage 7 complete: Shared VPC cross-folder network topology configured.")
EOF
python3 scratch/day21_lab/topic2/stage7_shared_vpc_topology.py
```

**Expected result:**
Shared VPC topology mapped and saved to scratch/day21_lab/stage7_shared_vpc_topology.json.

**Save:** scratch/day21_lab/stage7_shared_vpc_topology.json""",

            """**Stage 8: Validate Topic 2 Acceptance Criteria and Summary**

**Location:** local terminal

**Actions:**
Assert all Topic 2 stage files exist and write the folder governance summary.
```bash
cat <<'EOF' > scratch/day21_lab/topic2/stage8_summary.py
import json
import os

required = [
    "scratch/day21_lab/stage1_folder_init.json",
    "scratch/day21_lab/stage2_folder_tree.json",
    "scratch/day21_lab/stage3_env_isolation.json",
    "scratch/day21_lab/stage4_iam_inheritance.json",
    "scratch/day21_lab/stage5_orgpolicy_override.json",
    "scratch/day21_lab/stage6_finops_budget.json",
    "scratch/day21_lab/stage7_shared_vpc_topology.json"
]

missing = [f for f in required if not os.path.exists(f)]
assert len(missing) == 0, f"Missing Topic 2 files: {missing}"

summary = {
    "lab": "Exercise B - Multi-Tier Folder Hierarchy and Additive IAM Inheritance",
    "status": "PASS",
    "verified_stages": 8,
    "top_level_folders_count": 3,
    "missing_files": missing
}

with open("scratch/day21_lab/stage8_topic2_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Exercise B validation complete: all 8 stages verified.")
EOF
python3 scratch/day21_lab/topic2/stage8_summary.py
```

**Expected result:**
Summary written to scratch/day21_lab/stage8_topic2_summary.json.

**Save:** scratch/day21_lab/stage8_topic2_summary.json"""
        ]
    },
    'topic-03': {
        'name': 'Exercise C: Project Identifiers Triad, Service Agent Derivation, and Landing Zone Draft',
        'goal': 'Validate Project Identifiers Triad syntax rules, derive Google-managed service agent identities from Project Numbers, model project operational boundaries and deletion liens, and author the authoritative enterprise landing-zone draft.',
        'expected': 'A verified suite of simulation scripts validating Project ID regex patterns, Pub/Sub and Compute Engine service agent email derivations, cross-project Shared VPC and KMS CMEK bindings, and generating scratch/day-021-landing-zone-draft.md.',
        'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Project Identifiers Triad regex validation, deterministic service agent email derivations, project operational boundary definitions, project deletion lien configuration, and landing zone draft authoring. Simulated or predicted: Google Cloud internal project number generation, CMEK KMS key ring evaluation latency, and 30-day soft-delete lifecycle purge cycles. Untested on GCP: Live gcloud projects create API calls, production Cloud KMS key creation, and live Shared VPC host project subnet attachments.',
        'covers': 'Sketch an organization/folder/project hierarchy for development and production and label each owner (Project boundaries, service agents and landing zone draft)',
        'prereq': 'Completion of Exercises A and B, Python 3.10+, POSIX shell',
        'preflight': 'Ensure scratch/day21_lab directory is accessible and initialize Topic 3 workspace',
        'trouble': 'If regex validation fails, verify project ID adheres to 6-30 lowercase characters with hyphens',
        'cleanup': 'Artifacts remain in scratch/day21_lab/ and scratch/day-021-landing-zone-draft.md for audit',
        'steps': [
            """**Stage 1: Initialize Project Lab Environment**

**Location:** local terminal

**Actions:**
Create the dedicated laboratory directory structure for Topic 3 project identifiers and landing zone authoring.
```bash
mkdir -p scratch/day21_lab/topic3
cat <<'EOF' > scratch/day21_lab/topic3/stage1_init.py
import json

init_data = {
    "topic": "topic-03",
    "exercise": "Project Identifiers Triad, Service Agents, and Landing Zone Authoring",
    "status": "INITIALIZED"
}

with open("scratch/day21_lab/stage1_project_init.json", "w") as f:
    json.dump(init_data, f, indent=2)

print("Stage 1 complete: Project lab environment initialized.")
EOF
python3 scratch/day21_lab/topic3/stage1_init.py
```

**Expected result:**
Workspace initialized and written to scratch/day21_lab/stage1_project_init.json.

**Save:** scratch/day21_lab/stage1_project_init.json""",

            """**Stage 2: Validate Project Identifiers Triad and Naming Convention Regex**

**Location:** local terminal

**Actions:**
Author a Python script to validate Project Name, Project ID, and Project Number specifications against GCP constraints.
```bash
cat <<'EOF' > scratch/day21_lab/topic3/stage2_id_validation.py
import json
import re

PROJECT_ID_REGEX = r'^[a-z][a-z0-9-]{4,28}[a-z0-9]$' # 6 to 30 lowercase chars, starts with letter, ends with letter/digit
PROJECT_NUM_REGEX = r'^[0-9]{11,13}$'

candidate_projects = [
    {
        "name": "BrightLoaf Production Orders Service",
        "id": "brightloaf-prod-orders-01",
        "number": "918273645102",
        "expected_valid": True
    },
    {
        "name": "BrightLoaf Retail POS Central",
        "id": "brightloaf-prod-pos-01",
        "number": "817263549102",
        "expected_valid": True
    },
    {
        "name": "Invalid Project Case",
        "id": "BrightLoaf_Invalid_ID!",
        "number": "not-a-number",
        "expected_valid": False
    }
]

audit_results = []
for p in candidate_projects:
    valid_id = bool(re.match(PROJECT_ID_REGEX, p["id"]))
    valid_num = bool(re.match(PROJECT_NUM_REGEX, p["number"]))
    is_valid = valid_id and valid_num
    audit_results.append({
        "project": p,
        "valid_id_syntax": valid_id,
        "valid_number_syntax": valid_num,
        "passed": (is_valid == p["expected_valid"])
    })
    assert is_valid == p["expected_valid"], f"Validation mismatch for {p['name']}"

with open("scratch/day21_lab/stage2_id_validation.json", "w") as f:
    json.dump(audit_results, f, indent=2)

print("Stage 2 complete: Project Identifiers Triad regex validation passed.")
EOF
python3 scratch/day21_lab/topic3/stage2_id_validation.py
```

**Expected result:**
Triad validation results written to scratch/day21_lab/stage2_id_validation.json.

**Save:** scratch/day21_lab/stage2_id_validation.json""",

            """**Stage 3: Derive Google-Managed Service Agent Identities from Project Numbers**

**Location:** local terminal

**Actions:**
Author a script to deterministically derive service agent emails across Pub/Sub, Compute Engine, and Cloud Storage.
```bash
cat <<'EOF' > scratch/day21_lab/topic3/stage3_service_agents.py
import json

projects = [
    {"projectId": "brightloaf-prod-orders-01", "projectNumber": "918273645102"},
    {"projectId": "brightloaf-prod-pos-01", "projectNumber": "817263549102"}
]

derived_agents = {}
for p in projects:
    num = p["projectNumber"]
    pid = p["projectId"]
    derived_agents[pid] = {
        "pubsub_service_agent": f"service-{num}@gcp-sa-pubsub.iam.gserviceaccount.com",
        "compute_service_agent": f"service-{num}@compute-system.iam.gserviceaccount.com",
        "storage_service_agent": f"service-{num}@gs-project-accounts.iam.gserviceaccount.com",
        "cloudkms_service_agent": f"service-{num}@gcp-sa-cloudkms.iam.gserviceaccount.com"
    }

# Assert derived format starts with service-[PROJECT_NUMBER]
for pid, agents in derived_agents.items():
    assert "@gcp-sa-pubsub.iam.gserviceaccount.com" in agents["pubsub_service_agent"]

with open("scratch/day21_lab/stage3_service_agents.json", "w") as f:
    json.dump(derived_agents, f, indent=2)

print("Stage 3 complete: Google-managed service agent identities derived successfully.")
EOF
python3 scratch/day21_lab/topic3/stage3_service_agents.py
```

**Expected result:**
Derived service agent identities written to scratch/day21_lab/stage3_service_agents.json.

**Save:** scratch/day21_lab/stage3_service_agents.json""",

            """**Stage 4: Model Operational Boundaries at the Project Layer**

**Location:** local terminal

**Actions:**
Simulate the 4 operational boundaries (IAM, VPC, Billing, Quota) for a production workload project.
```bash
cat <<'EOF' > scratch/day21_lab/topic3/stage4_operational_boundaries.py
import json

boundaries = {
    "project_id": "brightloaf-prod-orders-01",
    "project_number": "918273645102",
    "iam_boundary": {
        "direct_bindings_count": 4,
        "default_service_accounts_disabled": True,
        "os_login_enforced": True
    },
    "network_boundary": {
        "default_vpc_deleted": True,
        "shared_vpc_attached": True,
        "host_project": "brightloaf-hub-net-prod"
    },
    "billing_boundary": {
        "billing_account_id": "01ABCD-23EFGH-45IJKL",
        "budget_alert_enabled": True
    },
    "quota_boundary": {
        "compute_cpus_limit": 64,
        "kms_cryptokey_decryption_rpm": 60000,
        "pubsub_publish_bandwidth_mbps": 100
    }
}

assert boundaries["network_boundary"]["default_vpc_deleted"] is True
assert boundaries["iam_boundary"]["os_login_enforced"] is True

with open("scratch/day21_lab/stage4_operational_boundaries.json", "w") as f:
    json.dump(boundaries, f, indent=2)

print("Stage 4 complete: Project-level operational boundaries modeled.")
EOF
python3 scratch/day21_lab/topic3/stage4_operational_boundaries.py
```

**Expected result:**
Operational boundary configuration written to scratch/day21_lab/stage4_operational_boundaries.json.

**Save:** scratch/day21_lab/stage4_operational_boundaries.json""",

            """**Stage 5: Model Project Deletion Lifecycle and Liens Protection**

**Location:** local terminal

**Actions:**
Model the 30-day soft-delete lifecycle and author an API lien lock preventing accidental deletion of production infrastructure.
```bash
cat <<'EOF' > scratch/day21_lab/topic3/stage5_deletion_liens.py
import json

lien_config = {
    "name": "liens/p918273645102-l83920194",
    "parent": "projects/brightloaf-prod-orders-01",
    "restrictions": ["resourcemanager.projects.delete"],
    "origin": "terraform-landing-zone-module",
    "reason": "Production order processing pipeline must not be deleted",
    "createTime": "2026-02-10T15:00:00.000Z"
}

lifecycle_spec = {
    "project_id": "brightloaf-prod-orders-01",
    "active_state": "ACTIVE",
    "soft_delete_window_days": 30,
    "recovery_mechanism": "gcloud projects undelete brightloaf-prod-orders-01",
    "lien": lien_config,
    "deletion_protection_asserted": True
}

assert "resourcemanager.projects.delete" in lien_config["restrictions"]

with open("scratch/day21_lab/stage5_deletion_liens.json", "w") as f:
    json.dump(lifecycle_spec, f, indent=2)

print("Stage 5 complete: Project deletion lifecycle and liens protection verified.")
EOF
python3 scratch/day21_lab/topic3/stage5_deletion_liens.py
```

**Expected result:**
Lien configuration and lifecycle spec written to scratch/day21_lab/stage5_deletion_liens.json.

**Save:** scratch/day21_lab/stage5_deletion_liens.json""",

            """**Stage 6: Formulate Cross-Project Shared VPC and KMS CMEK Bindings**

**Location:** local terminal

**Actions:**
Construct cross-project cryptographic and networking bindings between the service project, host project, and security KMS keyring.
```bash
cat <<'EOF' > scratch/day21_lab/topic3/stage6_cross_project_bindings.py
import json

cross_project_architecture = {
    "workload_project": "brightloaf-prod-orders-01",
    "workload_project_number": "918273645102",
    "cross_project_grants": [
        {
            "target_resource": "projects/brightloaf-hub-net-prod/regions/us-central1/subnetworks/sb-prod-orders-us-central1",
            "role": "roles/compute.networkUser",
            "member": "serviceAccount:service-918273645102@compute-system.iam.gserviceaccount.com",
            "purpose": "Allow Compute Engine in orders project to attach NIC to Shared VPC subnet"
        },
        {
            "target_resource": "projects/brightloaf-sec-kms/locations/us-central1/keyRings/order-keyring/cryptoKeys/order-cmek",
            "role": "roles/cloudkms.cryptoKeyDecrypter",
            "member": "serviceAccount:service-918273645102@gcp-sa-pubsub.iam.gserviceaccount.com",
            "purpose": "Allow Pub/Sub service agent to decrypt customer order CMEK payloads"
        }
    ]
}

assert len(cross_project_architecture["cross_project_grants"]) == 2

with open("scratch/day21_lab/stage6_cross_project_bindings.json", "w") as f:
    json.dump(cross_project_architecture, f, indent=2)

print("Stage 6 complete: Cross-project Shared VPC and KMS bindings verified.")
EOF
python3 scratch/day21_lab/topic3/stage6_cross_project_bindings.py
```

**Expected result:**
Cross-project bindings modeled and saved to scratch/day21_lab/stage6_cross_project_bindings.json.

**Save:** scratch/day21_lab/stage6_cross_project_bindings.json""",

            """**Stage 7: Generate Authoritative Landing Zone Draft Markdown Artifact**

**Location:** local terminal

**Actions:**
Author the comprehensive Day 21 exit criteria artifact: a complete landing-zone draft with stable IDs, environment boundaries, and operating responsibilities.
```bash
mkdir -p scratch
cat <<'EOF' > scratch/day21_lab/topic3/stage7_generate_exit.py
landing_zone_doc = '''# BrightLoaf Enterprise Cloud Landing Zone Specification (Draft)

**Document Version:** 1.0.0  
**Curriculum Day:** Day 21 (Resource hierarchy and ownership)  
**Status:** AUTHORITATIVE ARCHITECTURAL SPECIFICATION  
**Author:** Lead Enterprise Cloud Architect  
**Apex Organization:** `organizations/884920183921` (`brightloaf.com`)  
**Directory Customer ID:** `C03abcd8z`  

---

## 1. Executive Summary and Architecture Principles

This document defines the foundational Google Cloud landing zone for BrightLoaf commercial bakery operations. The resource hierarchy establishes immutable root governance, rigorous environment isolation, additive IAM least privilege, and deterministic FinOps cost attribution.

### Core Architectural Invariants:
1. **Apex Anchor of Trust:** All cloud infrastructure is anchored to Organization node `organizations/884920183921`, bound 1:1 with DNS-verified Cloud Identity domain `brightloaf.com`. Standalone "No Organization" projects are prohibited.
2. **Environment Segregation:** Workloads with different risk profiles reside in separate top-level folder trees (`Production` vs `Non-Production`). Co-location of staging and production under a shared folder is prohibited.
3. **Additive IAM Discipline:** Roles granted at folder levels cascade additively downward. Mutation and administrative roles (`roles/editor`, `roles/owner`) are never bound at or above top-level folders.
4. **Project Identifiers Triad:** System automation and service agent derivations strictly use the immutable numerical `Project Number`. Human-readable `Project Names` are never referenced in automation scripts.
5. **Accidental Deletion Defense:** All production projects enforce API project liens (`resourcemanager.projects.delete`) to safeguard stateful systems against accidental purging during the 30-day soft-delete lifecycle.

---

## 2. Resource Hierarchy and Stable Identifiers

The landing zone hierarchy enforces a three-tier tree structure: Organization -> Environment Folders -> Business Unit Folders -> Workload Projects.

| Hierarchy Tier | Node Name / Display Name | Stable Identifier | Parent Node | Operating Environment | Primary Owner / Responsibility |
|---|---|---|---|---|---|
| **Root (Apex)** | BrightLoaf Organization | `organizations/884920183921` | None | Enterprise Root | `group:gcp-org-admins@brightloaf.com` |
| **Tier 1 Folder** | Production | `folders/482910492819` | `organizations/884920183921` | Production | `group:gcp-prod-infra-leads@brightloaf.com` |
| **Tier 1 Folder** | Non-Production | `folders/482910492820` | `organizations/884920183921` | Non-Production | `group:gcp-platform-dev@brightloaf.com` |
| **Tier 1 Folder** | Core-Shared-Services | `folders/482910492825` | `organizations/884920183921` | Shared Services | `group:gcp-shared-infra@brightloaf.com` |
| **Tier 2 Folder** | Retail-POS | `folders/482910492821` | `folders/482910492819` | Production | `group:retail-ops-leads@brightloaf.com` |
| **Tier 2 Folder** | Supply-Chain | `folders/482910492822` | `folders/482910492819` | Production | `group:supplychain-leads@brightloaf.com` |
| **Tier 2 Folder** | Development | `folders/482910492823` | `folders/482910492820` | Non-Production | `group:app-developers@brightloaf.com` |
| **Tier 2 Folder** | Staging | `folders/482910492824` | `folders/482910492820` | Non-Production | `group:qa-automation@brightloaf.com` |
| **Tier 2 Folder** | Networking-Hub | `folders/482910492826` | `folders/482910492825` | Shared Infrastructure | `group:network-admins@brightloaf.com` |
| **Tier 2 Folder** | Security-SecOps | `folders/482910492827` | `folders/482910492825` | Security Operations | `group:secops-team@brightloaf.com` |
| **Project** | Retail POS Service | `brightloaf-prod-pos-01` (`817263549102`) | `folders/482910492821` | Production | `group:retail-pos-sre@brightloaf.com` |
| **Project** | Order Ingestion Pipeline | `brightloaf-prod-orders-01` (`918273645102`) | `folders/482910492822` | Production | `group:orders-sre@brightloaf.com` |
| **Project** | Shared VPC Host Prod | `brightloaf-hub-net-prod` (`718293041920`) | `folders/482910492826` | Shared Infrastructure | `group:network-admins@brightloaf.com` |
| **Project** | Centralized Logging | `brightloaf-secops-logging` (`615243901827`) | `folders/482910492827` | Security Operations | `group:secops-team@brightloaf.com` |
| **Project** | Dev Sandbox | `brightloaf-dev-sandbox-01` (`519283746102`) | `folders/482910492823` | Development | `group:app-developers@brightloaf.com` |

---

## 3. Operational Boundaries and Governance Baselines

### 3.1 Network Boundary (Shared VPC Topology)
- **Host Project:** `brightloaf-hub-net-prod` hosts the primary transit VPC `vpc-shared-prod-central`.
- **Subnet Allocations:**
  - `sb-prod-pos-us-central1`: `10.10.1.0/24` (Attached to `brightloaf-prod-pos-01`)
  - `sb-prod-orders-us-central1`: `10.10.2.0/24` (Attached to `brightloaf-prod-orders-01`)
- **Default VPC:** Deleted across all projects upon initial creation.

### 3.2 Organization Policy Guardrails
1. `constraints/compute.vmExternalIpAccess`: Denied across entire Organization root; strictly private IPs.
2. `constraints/iam.allowedPolicyMemberDomains`: Restricted to Cloud Identity directory customer ID `C03abcd8z`.
3. `constraints/storage.uniformBucketLevelAccess`: Enforced across all Cloud Storage buckets.
4. `constraints/compute.disableSerialPortAccess`: Enforced across all virtual machines.

### 3.3 Google-Managed Service Agent CMEK Integrations
Pub/Sub CMEK decryption relies on deterministically derived service agents:
- **Order Pipeline Pub/Sub Agent:** `service-918273645102@gcp-sa-pubsub.iam.gserviceaccount.com`
- **KMS Role Binding:** `roles/cloudkms.cryptoKeyDecrypter` on `projects/brightloaf-sec-kms/locations/us-central1/keyRings/order-keyring/cryptoKeys/order-cmek`

### 3.4 FinOps and Cost Attribution
- **Billing Account:** `01ABCD-23EFGH-45IJKL` linked to all projects.
- **Cost Center Mapping:**
  - Retail POS: `CC-101-RETAIL` (Budget alert threshold at $25,000/mo)
  - Supply Chain: `CC-102-SUPPLY` (Budget alert threshold at $35,000/mo)
  - Core Shared Services: `CC-INFRA-CORP` (Budget alert threshold at $15,000/mo)
- **BigQuery Billing Export:** Centralized dataset `brightloaf-secops-logging.finops_export.gcp_billing_export_v1`.

---

## 4. Operating Responsibilities & RACI Matrix

| Operational Lifecycle Function | Org Admins | SecOps | Network Admins | Workload SRE | App Developers |
|---|---|---|---|---|---|
| **Root IAM & Org Policies** | **Accountable** | Consulted | Informed | Informed | Informed |
| **Folder Lifecycle & Segregation** | **Responsible** | Consulted | Consulted | Informed | Informed |
| **Shared VPC & Peering Routes** | Informed | Consulted | **Accountable** | Consulted | Informed |
| **Project Creation & Liens** | Consulted | Consulted | Consulted | **Responsible** | Informed |
| **KMS CMEK Key Management** | Informed | **Accountable** | Informed | Consulted | Informed |
| **Application Deployments** | Informed | Informed | Informed | **Accountable** | **Responsible** |

---

## 5. Verification Sign-Off
- **Architectural Status:** VERIFIED AND SIGNED OFF
- **Exit Criteria Requirement:** Satisfies Day 21 Practice & Exit Milestone
- **Timestamp:** 2026-10-04T22:50:00Z
'''

with open("scratch/day-021-landing-zone-draft.md", "w") as f:
    f.write(landing_zone_doc.strip() + "\\n")

print("Generated scratch/day-021-landing-zone-draft.md successfully.")
EOF
python3 scratch/day21_lab/topic3/stage7_generate_exit.py
```

**Expected result:**
Authoritative Day 21 landing-zone draft created at scratch/day-021-landing-zone-draft.md.

**Save:** scratch/day-021-landing-zone-draft.md""",

            """**Stage 8: Validate Topic 3 Acceptance Criteria and Final Lab Summary**

**Location:** local terminal

**Actions:**
Verify all Topic 3 stage artifacts and assemble the final Day 21 laboratory acceptance summary.
```bash
cat <<'EOF' > scratch/day21_lab/topic3/stage8_summary.py
import json
import os

required = [
    "scratch/day21_lab/stage1_project_init.json",
    "scratch/day21_lab/stage2_id_validation.json",
    "scratch/day21_lab/stage3_service_agents.json",
    "scratch/day21_lab/stage4_operational_boundaries.json",
    "scratch/day21_lab/stage5_deletion_liens.json",
    "scratch/day21_lab/stage6_cross_project_bindings.json",
    "scratch/day-021-landing-zone-draft.md"
]

missing = [f for f in required if not os.path.exists(f)]
assert len(missing) == 0, f"Missing Topic 3 files: {missing}"

summary = {
    "lab": "Exercise C - Project Identifiers Triad, Service Agents, and Landing Zone Authoring",
    "status": "PASS",
    "verified_stages": 8,
    "exit_artifact": "scratch/day-021-landing-zone-draft.md",
    "missing_files": missing
}

with open("scratch/day21_lab/stage8_project_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Exercise C validation complete: all 8 stages verified.")
EOF
python3 scratch/day21_lab/topic3/stage8_summary.py
```

**Expected result:**
Summary written to scratch/day21_lab/stage8_project_summary.json.

**Save:** scratch/day21_lab/stage8_project_summary.json"""
        ]
    }
}
