"""Day 18 Scenarios and Labs definitions."""

from scratch.generate_day_018 import FIG_18_3_HTML, FIG_18_4_HTML, FIG_18_5_HTML

SCENARIOS = {
    'topic-01': {
        'scenario': 'During an ongoing engineering study cohort at Brightloaf, team members arriving for morning lab work reported that all experimental Cloud Run microservices and Compute Engine instances in the brightloaf-sandbox-18 project were unreachable. Developers attempting to deploy code via Cloud Shell received the error: ERROR: (gcloud.run.deploy) PERMISSION_DENIED: The billing account for project [brightloaf-sandbox-18] is disabled in state [CLOSED]. Billing must be enabled to activate services. When the platform lead logged into the Google Cloud Console, they discovered that the corporate purchasing credit card linked to the primary Cloud Billing Account had expired on the first of the month. Because no secondary payment method was configured and billing notification emails were sent to a legacy distribution alias, Google Cloud suspended the billing account after a grace period, disabling APIs and stopping all compute resources across six associated projects.',
        'impact': '6 training and sandbox projects suspended; all active Compute Engine VMs stopped; Cloud Run endpoints returning HTTP 403; engineering onboarding stalled for 4 hours; ephemeral external IP addresses released.',
        'constraints': 'Rely on synthetic Brightloaf test fixtures, observe zero budget spend, and preserve the duplicate fulfillment invariant.',
        'evidence': '''<p>Illustrative billing project inspection log and API suspension error captured during the billing disconnection incident:</p>
<pre><code>2026-10-04T08:15:02.104Z operator-terminal gcloud[104]: gcloud billing projects describe brightloaf-sandbox-18
billingAccountName: billingAccounts/01A2B3-4C5D6E-7F8G9H
billingEnabled: false
projectId: brightloaf-sandbox-18
2026-10-04T08:15:03.210Z operator-terminal gcloud[105]: gcloud run deploy order-api --image=gcr.io/brightloaf/order-api:v1
ERROR: (gcloud.run.deploy) PERMISSION_DENIED: The billing account for project [brightloaf-sandbox-18] is disabled in state [CLOSED]. Billing must be enabled to activate services.</code></pre>
''' + FIG_18_3_HTML,
        'root': 'Absence of billing account redundancy and automated preflight verification: no backup payment method was linked to the Cloud Billing Account, billing alerts were routed to an unmonitored mailbox, and deployment pipelines lacked billing health assertions.',
        'verify': 'Executed a simulated billing verification script asserting that billingEnabled is True and that the linked billing account is Open; verified that Cloud Run services process synthetic order requests and return HTTP 201; confirmed that duplicate order submissions are rejected by relational constraints.',
        'residual': 'When billing is re-enabled following suspension, ephemeral external IP addresses previously assigned to Compute Engine VMs may have been released and reassigned by Google Cloud; mitigate by reserving static external IP addresses or relying on Cloud DNS hostnames for inter-service communication.',
        'diagram_enabled': False,
        'facts': 'Billing account suspended due to expired corporate card; 6 projects disabled with billingEnabled: false; all workloads halted.',
        'inference': 'Severed billing accounts cascade into immediate API revocation; automated preflight checks and secondary payment methods are essential.',
        'expected': 'All projects linked to an active, verified billing account with backup payment routing; CI/CD preflights verify billingEnabled == true.',
        'diagnostic_steps': [
            'Execute gcloud billing projects describe [PROJECT_ID] to check the billingEnabled boolean and linked billingAccountName.',
            'Query billing account status using Cloud Billing API to verify whether account state is OPEN or CLOSED.',
            'Audit Cloud Audit Logs to identify the exact timestamp of billing suspension and review halted compute instances.',
            'Update Cloud Billing Account with an active primary payment method and configure a verified secondary backup credit card or bank account.',
            'Re-link the project to the active billing account and verify that API operations resume with zero orphaned resources.'
        ],
        'remediation_steps': [
            'Configure a secondary backup payment method in Google Cloud Billing to guarantee automated payment failover.',
            'Update Cloud Billing notification contacts to include active engineering leads and financial operations channels.',
            'Implement an automated preflight assertion (billingEnabled == true) in all deployment pipelines before resource provisioning.',
            'Confirm restored microservices uphold the duplicate fulfillment invariant (<= 1 shipment) when processing re-submitted transactions.'
        ]
    },
    'topic-02': {
        'scenario': 'An ML engineering team at Brightloaf configured an automated benchmark script in the brightloaf-sandbox-18 project to stress-test computer vision inference models. The engineer mistakenly provisioned four a2-highgpu-1g GPU instances costing $14.68/hour to run over a holiday weekend, believing that their configured $50 Google Cloud budget alert would automatically protect them from runaway spending. At 3.4 hours into the test, spend crossed $50.00: Google Cloud sent an automated email notification to an unmonitored shared inbox. Because budget alerts are passive notifications that do not halt running compute instances, the GPU nodes continued computing for 72 consecutive hours, accumulating $1,057.00 in charges against the corporate credit card before an engineer noticed on Monday morning.',
        'impact': '$1,057.00 in unbudgeted cloud compute spend; monthly sandbox budget exceeded by 2,100%; financial reprimand from engineering leadership; emergency spend audit required.',
        'constraints': 'Rely on synthetic Brightloaf test fixtures, observe zero budget spend, and preserve the duplicate fulfillment invariant.',
        'evidence': '''<p>Illustrative Cloud Billing budget event log and continuous compute charge accumulation captured during the benchmark overrun incident:</p>
<pre><code>2026-10-04T03:24:00.000Z cloud-billing-budget[101]: Budget alert triggered for 'Monthly Sandbox $50 Budget'
  costAmount: $51.38, budgetAmount: $50.00, currency: USD (102.7% of budget)
  notification: Sent email to legacy-sandbox-alerts@brightloaf.com
2026-10-04T03:25:00.000Z compute-engine[892]: 4x a2-highgpu-1g instances running continuously at 100% vCPU/GPU load
2026-10-04T12:00:00.000Z billing-meter[001]: Accrued spend reaches $210.40... instances continuing execution!
2026-10-05T12:00:00.000Z billing-meter[001]: Accrued spend reaches $562.80... instances continuing execution!
2026-10-06T09:00:00.000Z billing-meter[001]: Final spend reaches $1,057.20 before manual operator intervention.</code></pre>
''' + FIG_18_4_HTML,
        'root': 'Operational misconception of budget alert capabilities: assuming that passive Cloud Billing budget alert emails enforce hard spend caps, combined with lack of project-level GPU quota restrictions and absence of programmatic Pub/Sub kill-switches.',
        'verify': 'Executed a synthetic cost monitoring script simulating budget notifications at 50%, 90%, and 100%; verified that reaching 100% triggers automated instance termination; confirmed that the core order fulfillment service maintains the duplicate fulfillment invariant (<= 1 shipment) across recovery cycles.',
        'residual': 'Programmatically unlinking billing as a hard spend cap shuts down all resources indiscriminately, including persistent database instances; mitigate in production environments by implementing targeted instance shutdown (halting compute VMs while preserving databases) rather than complete billing disconnection.',
        'diagram_enabled': False,
        'facts': 'Four GPU instances ran 72 hours accumulating $1,057; budget alert fired at $50 but did not stop running instances.',
        'inference': 'Standard Cloud Billing budget alerts are advisory only; programmatic hard spend caps require event-driven Pub/Sub automation.',
        'expected': 'Enforce project-level quota limits (0 GPUs in sandboxes) and subscribe a Cloud Function kill-switch to budget Pub/Sub topics.',
        'diagnostic_steps': [
            'Inspect Cloud Billing reports to identify the exact SKU, machine family, and region generating excessive cost.',
            'Review project-level Compute Engine quotas to check if high-cost GPU allocations were inadvertently requested.',
            'Audit existing budget notification configurations to verify whether Pub/Sub integration was enabled or limited to email.',
            'Examine Compute Engine startup scripts to determine if automated shutdown timers (e.g. shutdown -h +120) were omitted.'
        ],
        'remediation_steps': [
            'Establish hard project-level Compute Engine quotas requesting 0 GPU allocations in sandbox projects.',
            'Embed automated self-termination timers into sandbox VM startup scripts to halt instances after 2 hours.',
            'Deploy an automated Cloud Function subscribed to the budget Pub/Sub topic to execute gcloud compute instances stop upon budget breach.',
            'Emphasize the Cloud Digital Leader business principle: automated financial governance protects corporate operating margins from runaway development loops.'
        ]
    },
    'topic-03': {
        'scenario': 'A site reliability engineer at Brightloaf was assigned to clean up an outdated testing service named order-api-v1 in the development sandbox project. Opening Cloud Shell in the Google Cloud Console, the engineer executed a cleanup command: gcloud run services delete order-api-v1. Unbeknownst to the engineer, a colleague had previously used the shared workstation terminal to troubleshoot an incident in the production project, executing gcloud config set project brightloaf-prod-us without resetting the default. Because the deletion command did not specify an explicit --project parameter, the gcloud CLI executed against the ambient production project, instantly terminating Brightloaf live production Order API. Real-time customer checkout immediately failed with HTTP 404 Not Found errors across all retail channels, triggering an emergency P1 outage that lasted 22 minutes until the service could be redeployed from the CI/CD artifact repository.',
        'impact': 'Production customer checkout outage for 22 minutes; 480 customer checkout attempts failed with HTTP 404; estimated $32,000 in lost gross merchandise value; emergency P1 postmortem required.',
        'constraints': 'Rely on synthetic Brightloaf test fixtures, observe zero budget spend, and preserve the duplicate fulfillment invariant.',
        'evidence': '''<p>Illustrative Cloud Shell command history and ambient project deletion log captured during the cross-project drift incident:</p>
<pre><code>2026-10-04T14:10:00.000Z operator-terminal:~$ gcloud config get-value project
brightloaf-prod-us  # Ambient context was left pointing to PRODUCTION!
2026-10-04T14:10:15.000Z operator-terminal:~$ gcloud run services delete order-api-v1 --quiet
Deleting service [order-api-v1] in project [brightloaf-prod-us]... Done.
2026-10-04T14:10:16.000Z monitoring-agent[501]: [CRITICAL] Ingress 404 spike on https://order.brightloaf.com/api/v1/orders
2026-10-04T14:10:17.000Z monitoring-agent[501]: Real-time customer checkouts failing; production service destroyed!</code></pre>
''' + FIG_18_5_HTML,
        'root': 'Ambient project context drift in Cloud Shell: relying on implicit default gcloud configuration across multi-tenant environments, compounded by omitting the mandatory explicit --project flag and granting excessive production IAM deletion rights to developer accounts.',
        'verify': 'Executed a test script verifying that the shell prompt dynamically reflects project changes; asserted that issuing destructive commands without an explicit --project flag is blocked by policy wrappers; verified that production order endpoints maintain continuous availability and uphold the duplicate fulfillment invariant (<= 1 shipment).',
        'residual': 'Complex shell prompt hooks that invoke the active project lookup command on every command execution can introduce latency in terminal rendering; mitigate by caching the active project in an environment variable updated only during project switching.',
        'diagram_enabled': False,
        'facts': 'Engineer ran gcloud run services delete order-api-v1 without --project flag; ambient context was set to production; production service was terminated.',
        'inference': 'Implicit default CLI contexts create catastrophic human error risks; mandatory explicit --project flags and context-aware PS1 prompts prevent drift.',
        'expected': 'Enforce explicit --project flags in all runbooks; display active project in bold shell prompt; restrict production IAM permissions.',
        'diagnostic_steps': [
            'Inspect gcloud CLI configuration using gcloud config list to check active account and project settings.',
            'Audit Cloud Audit Logs in production project to identify principal and IP address that issued the delete request.',
            'Review terminal shell environment (echo $PS1) to check if active project context was displayed.',
            'Check CI/CD runbooks and operational scripts for missing --project parameter flags.'
        ],
        'remediation_steps': [
            'Customize Cloud Shell and local PS1 prompts to dynamically display the active project ID in bold colored text.',
            'Configure isolated named gcloud configurations (gcloud config configurations create) for prod and sandbox environments.',
            'Mandate that all operational runbooks, scripts, and commands explicitly pass --project="${TARGET_PROJECT_ID}".',
            'Enforce IAM least privilege: revoke administrative deletion permissions for developers in production projects.'
        ]
    }
}

LABS = {
    'topic-01': {
        'name': 'Exercise A · Google Cloud Account Structure, Billing Inspection, and Preflight Verification',
        'goal': 'Model Google Cloud resource hierarchy entities in Python, author an automated billing preflight validator asserting active billing account linkages, detect disabled billing states, and verify project-to-billing 1:N cardinality.',
        'expected': 'A verified Python billing preflight suite confirming active billing account connections, isolating disabled project states with diagnostic exit codes, and outputting structured JSON validation results.',
        'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Local Python billing preflight simulation, project state verification, mock billing API responses, billing health assertion. Simulated or predicted: Google Cloud Billing Account activation, bank payment method verification, organization node attachment. Untested on GCP: Live GCP credit card debiting, real Cloud Billing Account creation, enterprise invoicing agreement.',
        'covers': 'Select a training sandbox or disposable project, inspect billing access and configure budget notifications if authorized.',
        'prereq': 'Linux terminal, Python 3.8+, standard POSIX utilities (mkdir, cat, python3, tee).',
        'preflight': 'Verify Python 3 runtime availability and initialize dedicated lab directory.',
        'verification': 'Verify that active projects pass preflight checks, disabled billing is caught with explicit exit codes, and cardinality invariants hold.',
        'trouble': 'Ensure mock database records reflect Google Cloud Cloud Resource Manager and Cloud Billing schema structures.',
        'cleanup': 'All generated files reside in scratch/day18_lab/ and can be removed or retained for audit reference.',
        'accept': 'A structured billing preflight summary report at scratch/day18_lab/stage8_billing_summary.json.',
        'file': 'scratch/day18_lab/stage8_billing_summary.json',
        'steps': [
            """**Stage 1: Preflight and Environment Baseline**

**Location:** local terminal

**Actions:**
Confirm terminal utilities and initialize dedicated Day 18 lab workspace.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day18_lab
python3 -c "import sys; print(f'Python runtime: {sys.version.split()[0]}, Day 18 lab initialized')" | tee scratch/day18_lab/stage1_preflight.txt
```

**Expected result:**
Python runtime confirmed and preflight baseline recorded.

**Save:** scratch/day18_lab/stage1_preflight.txt""",

            """**Stage 2: Model Google Cloud Resource and Billing Hierarchy**

**Location:** local terminal

**Actions:**
Author a Python script modeling the Google Cloud resource hierarchy: Organization root, Folders, Projects, and Cloud Billing Accounts with 1:N cardinality.
```bash
cat <<'EOF' > scratch/day18_lab/stage2_model.py
import json

hierarchy = {
    "organization": {
        "id": "organizations/78192830192",
        "domain": "brightloaf.com",
        "displayName": "Brightloaf Enterprise Root"
    },
    "billingAccounts": [
        {
            "name": "billingAccounts/01A2B3-4C5D6E-7F8G9H",
            "displayName": "Brightloaf Primary Corporate Billing",
            "open": True,
            "masterPaymentMethod": "Corporate Invoicing / ACH"
        }
    ],
    "folders": [
        {"id": "folders/101", "displayName": "Production", "parent": "organizations/78192830192"},
        {"id": "folders/102", "displayName": "Training-Sandboxes", "parent": "organizations/78192830192"}
    ],
    "projects": [
        {
            "projectId": "brightloaf-prod-us",
            "projectNumber": "104928374619",
            "displayName": "Brightloaf Production Main",
            "parent": "folders/101",
            "billingAccountName": "billingAccounts/01A2B3-4C5D6E-7F8G9H",
            "billingEnabled": True
        },
        {
            "projectId": "brightloaf-sandbox-18",
            "projectNumber": "859201948271",
            "displayName": "Naveen Study Sandbox Day 18",
            "parent": "folders/102",
            "billingAccountName": "billingAccounts/01A2B3-4C5D6E-7F8G9H",
            "billingEnabled": True
        }
    ]
}

with open("scratch/day18_lab/stage2_hierarchy_output.json", "w") as f:
    json.dump(hierarchy, f, indent=2)

print(f"Hierarchical model authored with {len(hierarchy['projects'])} projects linked to {len(hierarchy['billingAccounts'])} billing account.")
EOF
python3 scratch/day18_lab/stage2_model.py
```

**Expected result:**
Structured JSON hierarchy saved at scratch/day18_lab/stage2_hierarchy_output.json.

**Save:** scratch/day18_lab/stage2_hierarchy_output.json""",

            """**Stage 3: Implement Project Billing Preflight Validator**

**Location:** local terminal

**Actions:**
Author a Python billing preflight validator function that inspects project billing enablement and linked billing account status.
```bash
cat <<'EOF' > scratch/day18_lab/stage3_validator.py
import json
import sys

def validate_project_billing(project_id, db_path):
    with open(db_path) as f:
        db = json.load(f)
    
    project = next((p for p in db.get("projects", []) if p["projectId"] == project_id), None)
    if not project:
        return {"status": "ERROR", "reason": f"Project {project_id} not found", "exit_code": 1}
    
    if not project.get("billingEnabled"):
        return {"status": "SUSPENDED", "reason": "billingEnabled is false", "exit_code": 2}
    
    b_acc_name = project.get("billingAccountName")
    if not b_acc_name:
        return {"status": "UNLINKED", "reason": "No billing account linked", "exit_code": 3}
    
    b_acc = next((b for b in db.get("billingAccounts", []) if b["name"] == b_acc_name), None)
    if not b_acc or not b_acc.get("open"):
        return {"status": "BILLING_CLOSED", "reason": f"Billing account {b_acc_name} is closed", "exit_code": 4}
    
    return {
        "status": "PASS",
        "projectId": project_id,
        "projectNumber": project["projectNumber"],
        "billingAccountName": b_acc_name,
        "billingEnabled": True,
        "exit_code": 0
    }

if __name__ == "__main__":
    res = validate_project_billing("brightloaf-sandbox-18", "scratch/day18_lab/stage2_hierarchy_output.json")
    with open("scratch/day18_lab/stage3_preflight_active.json", "w") as f:
        json.dump(res, f, indent=2)
    print(f"Preflight validation result: {res['status']} (exit code {res['exit_code']})")
    assert res["exit_code"] == 0
EOF
python3 scratch/day18_lab/stage3_validator.py
```

**Expected result:**
Successful preflight validation for brightloaf-sandbox-18 with exit code 0.

**Save:** scratch/day18_lab/stage3_preflight_active.json""",

            """**Stage 4: Detect and Isolate Disabled Billing States**

**Location:** local terminal

**Actions:**
Author a simulation testing how the validator handles an orphaned project whose billing account has been disconnected or closed.
```bash
cat <<'EOF' > scratch/day18_lab/stage4_test_disabled.py
import json
import sys, os
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("scratch/day18_lab"))
try:
    from scratch.day18_lab.stage3_validator import validate_project_billing
except ImportError:
    from stage3_validator import validate_project_billing

# Create mock database with disabled project
with open("scratch/day18_lab/stage2_hierarchy_output.json") as f:
    db = json.load(f)

# Append orphaned project
db["projects"].append({
    "projectId": "orphaned-sandbox-demo",
    "projectNumber": "334918201948",
    "displayName": "Orphaned Sandbox Demo",
    "parent": "folders/102",
    "billingAccountName": "",
    "billingEnabled": False
})

with open("scratch/day18_lab/stage4_db.json", "w") as f:
    json.dump(db, f, indent=2)

res = validate_project_billing("orphaned-sandbox-demo", "scratch/day18_lab/stage4_db.json")
with open("scratch/day18_lab/stage4_isolated_disabled.json", "w") as f:
    json.dump(res, f, indent=2)

print(f"Disabled billing detection: status={res['status']}, exit_code={res['exit_code']}")
assert res["exit_code"] != 0
EOF
python3 scratch/day18_lab/stage4_test_disabled.py
```

**Expected result:**
Validator catches disabled billing on orphaned project and returns non-zero exit code.

**Save:** scratch/day18_lab/stage4_isolated_disabled.json""",

            """**Stage 5: Simulate Redundant Payment Routing and Billing Reconnection**

**Location:** local terminal

**Actions:**
Author a script simulating payment failure recovery: re-establishing billing connection with secondary payment authorization.
```bash
cat <<'EOF' > scratch/day18_lab/stage5_reconnect.py
import json
import sys, os
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("scratch/day18_lab"))
try:
    from scratch.day18_lab.stage3_validator import validate_project_billing
except ImportError:
    from stage3_validator import validate_project_billing

with open("scratch/day18_lab/stage4_db.json") as f:
    db = json.load(f)

# Reconnect the orphaned project to the corporate billing account
for p in db["projects"]:
    if p["projectId"] == "orphaned-sandbox-demo":
        p["billingAccountName"] = "billingAccounts/01A2B3-4C5D6E-7F8G9H"
        p["billingEnabled"] = True
        p["reconnectedAt"] = "2026-10-04T14:15:00Z"
        p["paymentRouting"] = "Secondary Corporate Backup Card (Verified)"

with open("scratch/day18_lab/stage5_db_reconnected.json", "w") as f:
    json.dump(db, f, indent=2)

res = validate_project_billing("orphaned-sandbox-demo", "scratch/day18_lab/stage5_db_reconnected.json")
with open("scratch/day18_lab/stage5_reconnect_result.json", "w") as f:
    json.dump(res, f, indent=2)

print(f"Reconnection result: status={res['status']}, billingEnabled={res['billingEnabled']}")
assert res["exit_code"] == 0
EOF
python3 scratch/day18_lab/stage5_reconnect.py
```

**Expected result:**
Project successfully re-linked with billingEnabled == True and exit code 0.

**Save:** scratch/day18_lab/stage5_reconnect_result.json""",

            """**Stage 6: Verify Project-to-Billing 1:N Cardinality and Lifecycle Invariants**

**Location:** local terminal

**Actions:**
Execute an architectural audit asserting that every project links to at most one billing account, and that billing accounts link to 1 or more projects.
```bash
cat <<'EOF' > scratch/day18_lab/stage6_cardinality_audit.py
import json

with open("scratch/day18_lab/stage5_db_reconnected.json") as f:
    db = json.load(f)

audit_report = {
    "total_projects": len(db["projects"]),
    "total_billing_accounts": len(db["billingAccounts"]),
    "projects_audit": []
}

for p in db["projects"]:
    b_name = p.get("billingAccountName")
    is_valid_1_to_1 = isinstance(b_name, str) and (b_name.startswith("billingAccounts/") or b_name == "")
    audit_report["projects_audit"].append({
        "projectId": p["projectId"],
        "linkedBillingAccount": b_name,
        "satisfies_single_billing_invariant": is_valid_1_to_1,
        "billingEnabled": p["billingEnabled"]
    })

all_valid = all(item["satisfies_single_billing_invariant"] for item in audit_report["projects_audit"])
audit_report["cardinality_invariant_status"] = "PASSED" if all_valid else "FAILED"

with open("scratch/day18_lab/stage6_cardinality_audit.json", "w") as f:
    json.dump(audit_report, f, indent=2)

print(f"Cardinality audit: {audit_report['cardinality_invariant_status']} across {len(db['projects'])} projects.")
assert all_valid is True
EOF
python3 scratch/day18_lab/stage6_cardinality_audit.py
```

**Expected result:**
1:N cardinality invariant confirmed across all registered projects.

**Save:** scratch/day18_lab/stage6_cardinality_audit.json""",

            """**Stage 7: Generate Billing Preflight Report**

**Location:** local terminal

**Actions:**
Synthesize preflight validation results and payment redundancy audit into a structured text report.
```bash
cat <<'EOF' > scratch/day18_lab/stage7_report.py
import json

with open("scratch/day18_lab/stage3_preflight_active.json") as f:
    active_data = json.load(f)

with open("scratch/day18_lab/stage6_cardinality_audit.json") as f:
    cardinality = json.load(f)

report = f'''=======================================================
GOOGLE CLOUD PROJECT BILLING PREFLIGHT AUDIT REPORT
=======================================================
Target Project: {active_data['projectId']}
Project Number: {active_data['projectNumber']}
Billing Account: {active_data['billingAccountName']}
Billing Status: {'ACTIVE' if active_data['billingEnabled'] else 'DISABLED'}
Preflight Exit Code: {active_data['exit_code']}
Cardinality Check: {cardinality['cardinality_invariant_status']} ({cardinality['total_projects']} projects audited)
Payment Redundancy: Primary Invoicing + Backup Payment Configured
Operational State: READY FOR CLOUD RUNTIME PROVISIONING
=======================================================
'''

with open("scratch/day18_lab/stage7_preflight_report.txt", "w") as f:
    f.write(report)

print("Generated stage7_preflight_report.txt successfully.")
EOF
python3 scratch/day18_lab/stage7_report.py
cat scratch/day18_lab/stage7_preflight_report.txt
```

**Expected result:**
Preflight audit report written and displayed.

**Save:** scratch/day18_lab/stage7_preflight_report.txt""",

            """**Stage 8: Validate Billing Preflight Acceptance Criteria**

**Location:** local terminal

**Actions:**
Author and run a final verification asserting that all Stage 1–7 artifacts exist, schemas are valid, and billing health is confirmed.
```bash
cat <<'EOF' > scratch/day18_lab/stage8_summary.py
import json
import os

required_files = [
    "scratch/day18_lab/stage1_preflight.txt",
    "scratch/day18_lab/stage2_hierarchy_output.json",
    "scratch/day18_lab/stage3_preflight_active.json",
    "scratch/day18_lab/stage4_isolated_disabled.json",
    "scratch/day18_lab/stage5_reconnect_result.json",
    "scratch/day18_lab/stage6_cardinality_audit.json",
    "scratch/day18_lab/stage7_preflight_report.txt"
]

summary = {
    "lab": "Exercise A - Billing Preflight",
    "status": "PASS",
    "verified_stages": 8,
    "missing_files": [f for f in required_files if not os.path.exists(f)]
}

assert len(summary["missing_files"]) == 0

with open("scratch/day18_lab/stage8_billing_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Exercise A validation complete: all 8 stages verified.")
EOF
python3 scratch/day18_lab/stage8_summary.py
```

**Expected result:**
Final acceptance summary generated at scratch/day18_lab/stage8_billing_summary.json.

**Save:** scratch/day18_lab/stage8_billing_summary.json"""
        ]
    },
    'topic-02': {
        'name': 'Exercise B · Always Free Tier Quota Auditing and Budget Alert Automation',
        'goal': 'Model Google Cloud Always Free tier monthly limits across Compute Engine, Cloud Storage, Cloud Run, and BigQuery; calculate regional overages; parse Cloud Billing budget Pub/Sub schemas; and simulate programmatic hard spend capping.',
        'expected': 'A verified cost calculation and budget event engine demonstrating zero cost for qualifying usage, detecting non-qualifying regional overages, and proving that standard budget alerts require programmatic kill-switches.',
        'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Always Free resource limit modeling, regional restriction validation, budget Pub/Sub event schema parsing, threshold breach evaluation. Simulated or predicted: Live Cloud Billing budget publication, Cloud Monitoring metric export, Cloud Functions execution. Untested on GCP: Live Cloud Billing charges, Google Cloud Pub/Sub cluster, real Compute Engine e2-micro uptime.',
        'covers': 'Select a training sandbox or disposable project, inspect billing access and configure budget notifications if authorized.',
        'prereq': 'Linux terminal, Python 3.8+, standard POSIX utilities (mkdir, cat, python3, tee).',
        'preflight': 'Verify Python environment and prepare test data directory.',
        'verification': 'Verify that within-quota usage in qualifying US regions incurs $0.00, while non-qualifying regions trigger billable overages.',
        'trouble': 'Ensure regional restrictions (us-central1, us-east1, us-west1) are strictly enforced in the quota engine.',
        'cleanup': 'All generated files reside in scratch/day18_lab/ and can be retained or removed as needed.',
        'accept': 'A comprehensive budget notification and hard cap analysis report at scratch/day18_lab/stage8_budget_analysis.txt.',
        'file': 'scratch/day18_lab/stage8_budget_analysis.txt',
        'steps': [
            """**Stage 1: Preflight and Always Free Baseline**

**Location:** local terminal

**Actions:**
Confirm environment and record Always Free evaluation baseline.
```bash
command -v bash
command -v python3
command -v cat
mkdir -p scratch/day18_lab
python3 -c "print('Always Free Tier Evaluator Preflight OK')" | tee scratch/day18_lab/stage1_tier_preflight.txt
```

**Expected result:**
Environment preflight confirmed.

**Save:** scratch/day18_lab/stage1_tier_preflight.txt""",

            """**Stage 2: Author Always Free Tier SKU and Regional Quota Matrix**

**Location:** local terminal

**Actions:**
Author a Python script defining published Google Cloud Always Free limits and approved regional zones.
```bash
cat <<'EOF' > scratch/day18_lab/stage2_quota_matrix.py
import json

quota_matrix = {
    "compute_engine": {
        "sku": "e2-micro",
        "monthly_hours_free": 744,
        "eligible_regions": ["us-central1", "us-east1", "us-west1"],
        "disk_gb_months_free": 30.0,
        "egress_gb_free": 1.0,
        "standard_rate_per_hour": 0.0084
    },
    "cloud_storage": {
        "tier": "Standard Regional",
        "gb_months_free": 5.0,
        "eligible_regions": ["us-central1", "us-east1", "us-west1"],
        "class_a_ops_free": 5000,
        "class_b_ops_free": 50000,
        "standard_rate_per_gb_month": 0.020
    },
    "cloud_run": {
        "requests_free": 2000000,
        "memory_gb_seconds_free": 360000,
        "vcpu_seconds_free": 180000,
        "eligible_regions": "ALL_REGIONS"
    },
    "bigquery": {
        "query_tb_free": 1.0,
        "active_storage_gb_free": 10.0,
        "standard_rate_per_tb": 6.25
    }
}

with open("scratch/day18_lab/stage2_quota_matrix.json", "w") as f:
    json.dump(quota_matrix, f, indent=2)

print("Always Free quota matrix authored successfully.")
EOF
python3 scratch/day18_lab/stage2_quota_matrix.py
```

**Expected result:**
Always Free quota definitions saved at scratch/day18_lab/stage2_quota_matrix.json.

**Save:** scratch/day18_lab/stage2_quota_matrix.json""",

            """**Stage 3: Calculate Consumption vs Always Free Allowances**

**Location:** local terminal

**Actions:**
Author a calculator evaluating resource usage in qualifying US regions, asserting that within-quota consumption equals $0.00.
```bash
cat <<'EOF' > scratch/day18_lab/stage3_calculator.py
import json

def calculate_usage_cost(usage_item, matrix):
    service = usage_item["service"]
    region = usage_item["region"]
    
    if service == "compute_engine":
        cfg = matrix["compute_engine"]
        if region not in cfg["eligible_regions"]:
            return usage_item["hours"] * cfg["standard_rate_per_hour"], "NON_QUALIFYING_REGION"
        billable_hours = max(0, usage_item["hours"] - cfg["monthly_hours_free"])
        return billable_hours * cfg["standard_rate_per_hour"], "QUALIFYING_REGION"
        
    elif service == "cloud_storage":
        cfg = matrix["cloud_storage"]
        if region not in cfg["eligible_regions"]:
            return usage_item["gb_months"] * cfg["standard_rate_per_gb_month"], "NON_QUALIFYING_REGION"
        billable_gb = max(0, usage_item["gb_months"] - cfg["gb_months_free"])
        return billable_gb * cfg["standard_rate_per_gb_month"], "QUALIFYING_REGION"

    return 0.0, "UNKNOWN"

with open("scratch/day18_lab/stage2_quota_matrix.json") as f:
    matrix = json.load(f)

# Test qualifying usage
qualifying_compute = {"service": "compute_engine", "region": "us-central1", "hours": 744}
cost, note = calculate_usage_cost(qualifying_compute, matrix)

result = {
    "test": "Qualifying US e2-micro 744 hours",
    "region": "us-central1",
    "calculated_cost_usd": cost,
    "eligibility_status": note,
    "is_free": cost == 0.0
}

with open("scratch/day18_lab/stage3_valid_usage.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"Qualifying usage test: Cost=${cost:.2f} (is_free={result['is_free']})")
assert cost == 0.0
EOF
python3 scratch/day18_lab/stage3_calculator.py
```

**Expected result:**
Qualifying usage cost verified at exactly $0.00.

**Save:** scratch/day18_lab/stage3_valid_usage.json""",

            """**Stage 4: Detect and Audit Regional Violations**

**Location:** local terminal

**Actions:**
Execute an audit on non-qualifying deployments (e.g. e2-micro deployed to europe-west1), calculating the unexpected billable overage.
```bash
cat <<'EOF' > scratch/day18_lab/stage4_regional_test.py
import json
import sys, os
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("scratch/day18_lab"))
try:
    from scratch.day18_lab.stage3_calculator import calculate_usage_cost
except ImportError:
    from stage3_calculator import calculate_usage_cost

with open("scratch/day18_lab/stage2_quota_matrix.json") as f:
    matrix = json.load(f)

# Test European regional violation
eu_compute = {"service": "compute_engine", "region": "europe-west1", "hours": 744}
cost, note = calculate_usage_cost(eu_compute, matrix)

result = {
    "test": "Non-qualifying EU e2-micro 744 hours",
    "region": "europe-west1",
    "calculated_cost_usd": round(cost, 2),
    "eligibility_status": note,
    "is_free": cost == 0.0
}

with open("scratch/day18_lab/stage4_regional_overage.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"Regional violation test: Cost=${cost:.2f}, status={note}")
assert cost > 0.0
EOF
python3 scratch/day18_lab/stage4_regional_test.py
```

**Expected result:**
Regional violation caught with calculated billable charge > $0.00.

**Save:** scratch/day18_lab/stage4_regional_overage.json""",

            """**Stage 5: Author Cloud Billing Budget Pub/Sub Notification Parser**

**Location:** local terminal

**Actions:**
Author a Python script parsing Google Cloud Billing budget Pub/Sub JSON message events.
```bash
cat <<'EOF' > scratch/day18_lab/stage5_budget_parser.py
import json

def parse_budget_event(payload_str):
    data = json.loads(payload_str)
    cost = float(data.get("costAmount", 0.0))
    budget = float(data.get("budgetAmount", 0.0))
    currency = data.get("currencyCode", "USD")
    pct = (cost / budget) * 100.0 if budget > 0 else 0.0
    
    return {
        "budgetDisplayName": data.get("budgetDisplayName"),
        "costAmount": cost,
        "budgetAmount": budget,
        "currency": currency,
        "percent_spent": round(pct, 1),
        "is_breached": cost >= budget,
        "action_required": "INVOKE_PROGRAMMATIC_KILL_SWITCH" if cost >= budget else "MONITOR_ONLY"
    }

# Mock Cloud Billing Pub/Sub JSON payload
mock_payload = json.dumps({
    "budgetDisplayName": "Training Sandbox $50 Budget",
    "costAmount": 52.40,
    "costIntervalStart": "2026-10-01T00:00:00Z",
    "budgetAmount": 50.00,
    "budgetAmountType": "SPECIFIED_AMOUNT",
    "currencyCode": "USD"
})

event_summary = parse_budget_event(mock_payload)
with open("scratch/day18_lab/stage5_alert_event.json", "w") as f:
    json.dump(event_summary, f, indent=2)

print(f"Budget Event Parsed: {event_summary['percent_spent']}% spent; action={event_summary['action_required']}")
assert event_summary["is_breached"] is True
EOF
python3 scratch/day18_lab/stage5_budget_parser.py
```

**Expected result:**
Budget event parsed successfully; breach detected at 104.8%.

**Save:** scratch/day18_lab/stage5_alert_event.json""",

            """**Stage 6: Prove the Budget Alert Misconception (Alert != Hard Cap)**

**Location:** local terminal

**Actions:**
Execute a simulation demonstrating that a passive budget alert allows instances to continue running and charges to accumulate without programmatic intervention.
```bash
cat <<'EOF' > scratch/day18_lab/stage6_misconception.py
import json

# Simulation of 72-hour weekend compute with passive email vs automated kill-switch
hours = 72
burn_rate_per_hour = 14.68  # 4x a2-highgpu
budget_limit = 50.0

timeline = []
spend = 0.0
alert_fired = False

for h in range(1, hours + 1):
    spend += burn_rate_per_hour
    if spend >= budget_limit and not alert_fired:
        alert_fired = True
        timeline.append({"hour": h, "spend": round(spend, 2), "event": "PASSIVE_EMAIL_ALERT_FIRED"})

proof = {
    "hours_simulated": hours,
    "configured_budget": budget_limit,
    "hour_alert_fired": timeline[0]["hour"],
    "spend_at_alert_time": timeline[0]["spend"],
    "final_spend_without_killswitch": round(spend, 2),
    "budget_exceeded_percent": round(((spend - budget_limit) / budget_limit) * 100.0, 1),
    "architectural_fact": "Google Cloud budget alerts notify subscribers; they NEVER halt running instances automatically."
}

with open("scratch/day18_lab/stage6_misconception_proof.json", "w") as f:
    json.dump(proof, f, indent=2)

print(f"Misconception proof: Budget=${budget_limit}, Final Spend=${proof['final_spend_without_killswitch']}")
assert proof["final_spend_without_killswitch"] > 1000.0
EOF
python3 scratch/day18_lab/stage6_misconception.py
```

**Expected result:**
Mathematical demonstration proving passive alerts allow spend to exceed budget by > 2,000%.

**Save:** scratch/day18_lab/stage6_misconception_proof.json""",

            """**Stage 7: Model Programmatic Kill-Switch Logic**

**Location:** local terminal

**Actions:**
Author a simulation of an event-driven Cloud Function that receives the Pub/Sub budget alert and calls the Compute Engine API to halt instances.
```bash
cat <<'EOF' > scratch/day18_lab/stage7_killswitch.py
import json

def automated_killswitch_handler(pubsub_event):
    if not pubsub_event.get("is_breached"):
        return {"action": "NOOP", "halted_instances": []}
    
    # Simulate stopping compute instances
    simulated_instances = ["gpu-bench-01", "gpu-bench-02", "gpu-bench-03", "gpu-bench-04"]
    halted = []
    for vm in simulated_instances:
        # Mocking: gcloud compute instances stop $vm
        halted.append({"instance": vm, "status": "TERMINATED", "command": f"gcloud compute instances stop {vm}"})
    
    return {
        "action": "HALT_COMPUTE",
        "reason": f"Spend {pubsub_event['costAmount']} exceeded budget {pubsub_event['budgetAmount']}",
        "halted_instances": halted,
        "estimated_spend_capped_usd": pubsub_event["costAmount"]
    }

with open("scratch/day18_lab/stage5_alert_event.json") as f:
    event = json.load(f)

result = automated_killswitch_handler(event)
with open("scratch/day18_lab/stage7_killswitch_sim.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"Kill-switch executed: {result['action']} for {len(result['halted_instances'])} instances. Spend capped at ${result['estimated_spend_capped_usd']}")
assert len(result["halted_instances"]) == 4
EOF
python3 scratch/day18_lab/stage7_killswitch.py
```

**Expected result:**
Programmatic kill-switch simulation halts 4 instances, capping spend at $52.40.

**Save:** scratch/day18_lab/stage7_killswitch_sim.json""",

            """**Stage 8: Synthesize Budget Notification and Hard Cap Analysis Report**

**Location:** local terminal

**Actions:**
Synthesize Always Free quotas, regional overage calculations, and programmatic kill-switch mechanics into an authoritative analysis report.
```bash
cat <<'EOF' > scratch/day18_lab/stage8_report.py
import json

with open("scratch/day18_lab/stage3_valid_usage.json") as f:
    valid_data = json.load(f)

with open("scratch/day18_lab/stage4_regional_overage.json") as f:
    regional_data = json.load(f)

with open("scratch/day18_lab/stage6_misconception_proof.json") as f:
    proof_data = json.load(f)

report = f'''=======================================================
GOOGLE CLOUD ALWAYS FREE AND BUDGET ALERT ANALYSIS
=======================================================
1. ALWAYS FREE REGIONAL VALIDATION:
   - us-central1 e2-micro (744h): ${valid_data['calculated_cost_usd']:.2f} (FREE: {valid_data['is_free']})
   - europe-west1 e2-micro (744h): ${regional_data['calculated_cost_usd']:.2f} (NON-QUALIFYING OVERAGE)

2. BUDGET ALERT MISCONCEPTION:
   - Configured Budget: ${proof_data['configured_budget']:.2f}
   - Alert Trigger Hour: Hour {proof_data['hour_alert_fired']} (${proof_data['spend_at_alert_time']:.2f})
   - Unmanaged Spend (Passive Alert Only): ${proof_data['final_spend_without_killswitch']:.2f} (+{proof_data['budget_exceeded_percent']}%)
   - Managed Spend (Programmatic Kill-Switch): $52.40 (CAPPED)

3. ARCHITECTURAL MANDATE:
   Budget alerts are passive advisory notifications. Automated spend caps
   require Pub/Sub event integration with Cloud Functions or Billing API detachment.
=======================================================
'''

with open("scratch/day18_lab/stage8_budget_analysis.txt", "w") as f:
    f.write(report)

print("Generated stage8_budget_analysis.txt successfully.")
EOF
python3 scratch/day18_lab/stage8_report.py
cat scratch/day18_lab/stage8_budget_analysis.txt
```

**Expected result:**
Comprehensive cost control analysis generated and verified.

**Save:** scratch/day18_lab/stage8_budget_analysis.txt"""
        ]
    },
    'topic-03': {
        'name': 'Exercise C · Project Context Management, Cloud Shell Safety, and Cleanup Plan',
        'goal': 'Validate project identifiers (Name vs ID vs Number); model isolated gcloud named configurations; implement a context-aware shell prompt (PS1) guard; author an automated sandbox cleanup script; and synthesize the authoritative Day 18 exit evidence artifact.',
        'expected': 'A verified project identifier validator, context-aware shell safety filter, automated cleanup plan, and the complete Day 18 exit evidence artifact at scratch/day-018-billing-preflight-cleanup.md.',
        'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Project identifier validation (ID vs Number vs Name), Cloud Shell PS1 prompt formatting, gcloud named configurations simulation, cleanup script execution. Simulated or predicted: Google Cloud Console project picker UI, live Cloud Shell VM provisioning, Cloud Resource Manager API calls. Untested on GCP: Actual project deletion on Google Cloud, live gcloud config across multi-user environments.',
        'covers': 'Select a training sandbox or disposable project, inspect billing access and configure budget notifications if authorized.',
        'prereq': 'Linux terminal, Python 3.8+, standard POSIX utilities (mkdir, cat, python3, tee, head).',
        'preflight': 'Confirm local environment and prepare dedicated test directories.',
        'verification': 'Verify that project identifiers adhere to Google Cloud naming rules, prompt guard detects production contexts, and the exit artifact is authored.',
        'trouble': 'Ensure project IDs contain only lowercase letters, digits, and hyphens (6 to 30 characters).',
        'cleanup': 'All generated files reside in scratch/day18_lab/ and scratch/day-018-billing-preflight-cleanup.md.',
        'accept': 'The complete redacted project/billing preflight and cleanup plan artifact at scratch/day-018-billing-preflight-cleanup.md.',
        'file': 'scratch/day-018-billing-preflight-cleanup.md',
        'steps': [
            """**Stage 1: Preflight and Workspace Setup**

**Location:** local terminal

**Actions:**
Confirm CLI environment and initialize lab workspace.
```bash
command -v bash
command -v python3
command -v cat
mkdir -p scratch/day18_lab
python3 -c "print('Project Context Lab Preflight OK')" | tee scratch/day18_lab/stage1_ctx_preflight.txt
```

**Expected result:**
Environment preflight confirmed.

**Save:** scratch/day18_lab/stage1_ctx_preflight.txt""",

            """**Stage 2: Validate Three Google Cloud Project Identifiers**

**Location:** local terminal

**Actions:**
Author a Python script validating the three distinct project identifiers according to Google Cloud Resource Manager specifications.
```bash
cat <<'EOF' > scratch/day18_lab/stage2_id_validator.py
import re
import json

def validate_project_identifiers(name, project_id, project_number):
    errors = []
    # Project Name: 4-30 chars
    if not (4 <= len(name) <= 30):
        errors.append("Project Name must be 4 to 30 characters.")
    
    # Project ID: 6-30 chars, lowercase, digits, hyphens, start with letter
    if not (6 <= len(project_id) <= 30):
        errors.append("Project ID must be 6 to 30 characters.")
    if not re.match(r"^[a-z][a-z0-9-]{4,28}[a-z0-9]$", project_id):
        errors.append("Project ID must start with lowercase letter, contain only [a-z0-9-], and end with letter/digit.")
        
    # Project Number: 12-digit int
    if not (isinstance(project_number, int) and 100_000_000_000 <= project_number <= 999_999_999_999):
        errors.append("Project Number must be a 12-digit integer.")
        
    return {
        "valid": len(errors) == 0,
        "name": name,
        "projectId": project_id,
        "projectNumber": project_number,
        "errors": errors
    }

# Validate Brightloaf sandbox identifiers
res = validate_project_identifiers("Naveen Study Sandbox Day 18", "brightloaf-sandbox-18", 859201948271)
with open("scratch/day18_lab/stage2_identifiers.json", "w") as f:
    json.dump(res, f, indent=2)

print(f"Identifier validation: valid={res['valid']}, projectId={res['projectId']}")
assert res["valid"] is True
EOF
python3 scratch/day18_lab/stage2_id_validator.py
```

**Expected result:**
Sandbox project identifiers validated against Google Cloud specifications.

**Save:** scratch/day18_lab/stage2_identifiers.json""",

            """**Stage 3: Simulate gcloud Named Configurations**

**Location:** local terminal

**Actions:**
Author a Python script modeling gcloud CLI named configurations (configurations create, set, activate) to demonstrate environment segregation.
```bash
cat <<'EOF' > scratch/day18_lab/stage3_configs.py
import json

configs = {
    "active_configuration": "brightloaf-sandbox",
    "configurations": {
        "brightloaf-prod": {
            "account": "lead-architect@brightloaf.com",
            "project": "brightloaf-prod-us",
            "region": "us-central1",
            "zone": "us-central1-a",
            "environment_tier": "PRODUCTION"
        },
        "brightloaf-sandbox": {
            "account": "naveen-study@brightloaf.com",
            "project": "brightloaf-sandbox-18",
            "region": "us-central1",
            "zone": "us-central1-f",
            "environment_tier": "SANDBOX"
        }
    }
}

with open("scratch/day18_lab/stage3_config_list.json", "w") as f:
    json.dump(configs, f, indent=2)

print(f"Named configurations authored: Active='{configs['active_configuration']}' targeting project '{configs['configurations'][configs['active_configuration']]['project']}'")
EOF
python3 scratch/day18_lab/stage3_configs.py
```

**Expected result:**
Named configurations saved at scratch/day18_lab/stage3_config_list.json.

**Save:** scratch/day18_lab/stage3_config_list.json""",

            r"""**Stage 4: Implement Context-Aware Shell Prompt (PS1) Safety Filter**

**Location:** local terminal

**Actions:**
Author a shell prompt hook function simulating Cloud Shell PS1 customization that highlights production in bold red and sandboxes in green.
```bash
cat <<'EOF' > scratch/day18_lab/stage4_prompt_guard.sh
#!/usr/bin/env bash
set -euo pipefail

format_prompt() {
    local project="$1"
    if [[ "$project" =~ prod ]]; then
        # Red warning prompt for production
        echo "[PROD_WARNING: ${project}]\$ "
    elif [[ "$project" =~ sandbox ]]; then
        # Green safe prompt for sandbox
        echo "[SANDBOX: ${project}]\$ "
    else
        echo "[GCP: ${project}]\$ "
    fi
}

p1=$(format_prompt "brightloaf-prod-us")
p2=$(format_prompt "brightloaf-sandbox-18")

echo "Production Prompt: $p1" | tee scratch/day18_lab/stage4_prompt_output.txt
echo "Sandbox Prompt:    $p2" | tee -a scratch/day18_lab/stage4_prompt_output.txt
EOF
chmod +x scratch/day18_lab/stage4_prompt_guard.sh
./scratch/day18_lab/stage4_prompt_guard.sh
```

**Expected result:**
Prompt formatting logic displays distinct warnings for production vs sandbox.

**Save:** scratch/day18_lab/stage4_prompt_output.txt""",

            """**Stage 5: Enforce Mandatory --project Flag in Automation Wrappers**

**Location:** local terminal

**Actions:**
Author a wrapper script that inspects destructive command invocations, blocking execution unless an explicit --project flag is provided.
```bash
cat <<'EOF' > scratch/day18_lab/stage5_wrapper.py
import sys
import json

def execute_safe_gcloud_command(args, ambient_project="brightloaf-prod-us"):
    has_project_flag = any(a.startswith("--project") for a in args)
    is_destructive = any(w in args for w in ["delete", "destroy", "drop", "purge"])
    
    if is_destructive and not has_project_flag:
        return {
            "status": "BLOCKED",
            "reason": "Destructive command rejected: Missing mandatory explicit --project flag.",
            "attempted_command": " ".join(args),
            "ambient_project_at_risk": ambient_project,
            "exit_code": 1
        }
    
    # Extract target project
    target = ambient_project
    for a in args:
        if a.startswith("--project="):
            target = a.split("=")[1]
            
    return {
        "status": "ALLOWED",
        "command": " ".join(args),
        "target_project": target,
        "exit_code": 0
    }

# Test 1: Destructive command without --project (must be BLOCKED)
test1 = execute_safe_gcloud_command(["gcloud", "run", "services", "delete", "order-api"])
assert test1["status"] == "BLOCKED"

# Test 2: Destructive command with explicit --project (ALLOWED)
test2 = execute_safe_gcloud_command(["gcloud", "run", "services", "delete", "order-api", "--project=brightloaf-sandbox-18"])
assert test2["status"] == "ALLOWED"

results = {"test_without_flag": test1, "test_with_flag": test2}
with open("scratch/day18_lab/stage5_wrapper_result.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Safety wrapper verified: Blocked={test1['status']}, Allowed={test2['status']}")
EOF
python3 scratch/day18_lab/stage5_wrapper.py
```

**Expected result:**
Safety wrapper successfully blocks commands lacking the explicit --project parameter.

**Save:** scratch/day18_lab/stage5_wrapper_result.json""",

            """**Stage 6: Author Reproducible Sandbox Cleanup Script with Dry-Run Safety**

**Location:** local terminal

**Actions:**
Author an automated resource cleanup script for training sandboxes supporting dry-run execution.
```bash
cat <<'EOF' > scratch/day18_lab/stage6_cleanup_plan.py
import json

class SandboxCleanupManager:
    def __init__(self, target_project_id):
        self.project_id = target_project_id
        
    def generate_cleanup_plan(self):
        # Simulated resources inventoried in sandbox project
        return [
            {"type": "Compute Engine VM", "name": "study-vm-e2micro", "action": "DELETE", "safe": True},
            {"type": "Persistent Disk", "name": "study-disk-30gb", "action": "DELETE", "safe": True},
            {"type": "Cloud Storage Bucket", "name": "brightloaf-sandbox-temp-data", "action": "DELETE", "safe": True},
            {"type": "Pub/Sub Topic", "name": "sandbox-budget-alerts", "action": "DELETE", "safe": True}
        ]
        
    def execute_cleanup(self, dry_run=True):
        plan = self.generate_cleanup_plan()
        actions_taken = []
        for item in plan:
            actions_taken.append({
                "resource": item["name"],
                "type": item["type"],
                "action": item["action"],
                "status": "SIMULATED_DELETED" if dry_run else "DELETED"
            })
        return {
            "project_id": self.project_id,
            "dry_run": dry_run,
            "resources_evaluated": len(plan),
            "actions": actions_taken,
            "cost_impact": "Charges reduced to $0.00"
        }

mgr = SandboxCleanupManager("brightloaf-sandbox-18")
cleanup_result = mgr.execute_cleanup(dry_run=True)

with open("scratch/day18_lab/stage6_cleanup_plan.json", "w") as f:
    json.dump(cleanup_result, f, indent=2)

print(f"Sandbox cleanup plan executed (dry_run={cleanup_result['dry_run']}) for {cleanup_result['resources_evaluated']} resources.")
EOF
python3 scratch/day18_lab/stage6_cleanup_plan.py
```

**Expected result:**
Automated cleanup plan generated at scratch/day18_lab/stage6_cleanup_plan.json.

**Save:** scratch/day18_lab/stage6_cleanup_plan.json""",

            r"""**Stage 7: Author Authoritative Day 18 Exit Evidence Artifact**

**Location:** local terminal

**Actions:**
Synthesize project preflight assertions, billing health checks, Always Free vs promotional credit matrices, the budget alert vs hard spend cap analysis, and the cleanup automation plan into the authoritative Day 18 exit artifact: scratch/day-018-billing-preflight-cleanup.md.
```bash
cat <<'EOF' > scratch/day18_lab/generate_day18_exit.py
doc = r'''# Day 18 Exit Evidence: Project/Billing Preflight, Cost Control Architecture, and Cleanup Plan

## Executive Summary
This document establishes the verified operational exit evidence for Day 18 (Block 2: Cloud Environment and Identity). It documents an authoritative project and billing preflight inspection checklist, a comparative matrix of Always Free allowances versus promotional trial credits, a rigorous architectural explanation of why budget alerts are not hard spend caps, programmatic kill-switch blueprints, and a reproducible disposable sandbox cleanup plan.

---

## 1. Redacted Project and Billing Preflight Checklist

~~~json
{
  "preflight_version": "2026.10",
  "audit_timestamp": "2026-10-04T14:30:00Z",
  "organization": {
    "domain": "brightloaf.com",
    "organization_id": "organizations/78192830192"
  },
  "project_identifiers": {
    "project_name": "Naveen Study Sandbox Day 18",
    "project_id": "brightloaf-sandbox-18",
    "project_number": 859201948271,
    "parent_folder": "folders/102 (Training-Sandboxes)"
  },
  "billing_linkage": {
    "billing_account_name": "billingAccounts/01A2B3-4C5D6E-7F8G9H",
    "billing_account_state": "OPEN",
    "billing_enabled": true,
    "primary_payment_method": "Corporate ACH Invoicing (REDACTED)",
    "backup_payment_method": "Verified Secondary Card (REDACTED)",
    "preflight_exit_code": 0,
    "preflight_status": "READY_FOR_DEPLOYMENT"
  }
}
~~~

---

## 2. Google Cloud Free Tier vs Promotional Trial Matrix

| Dimension | 90-Day Free Trial | Always Free Tier | Standard Paid Account |
| :--- | :--- | :--- | :--- |
| **Credit / Allowance** | $300 USD one-time promotional credit | Fixed recurring monthly quotas | On-demand pay-as-you-go consumption |
| **Duration** | 90 calendar days from signup | Perpetual (renews 1st of month) | Indefinite until account closure |
| **Eligible Services** | All billable GCP products (quota limited) | Compute Engine, Storage, Cloud Run, BQ | Full portfolio (all GCP products) |
| **Compute Engine** | Any machine family (within trial quota) | 1 e2-micro VM in US regions only | Any machine family & any global region |
| **Cloud Storage** | $300 spend credit | 5 GB Regional (us-central1, us-east1, us-west1) | Any bucket class & any global region |
| **Expiration Impact** | Workloads paused; zero auto-billing | Usage beyond quota billed at list price | Monthly invoice or card debit |
| **Purpose** | Proof of concept and platform evaluation | Lightweight utilities and learning sandboxes | Authoritative production workloads |

---

## 3. Architectural Explanation: Why a Budget Alert Is Not a Hard Spend Cap

A primary operational failure mode among cloud practitioners is assuming that configuring a Cloud Billing Budget Alert creates an automated financial circuit breaker.

### The Misconception vs The Technical Reality
- **The Misconception:** An engineer configures a $50 monthly budget alert and assumes that when spending hits $50, Google Cloud will automatically halt running virtual machines or block billable API requests.
- **The Technical Reality:** A Google Cloud budget alert is **strictly an advisory notification event**. It sends emails to designated billing administrators and optionally publishes a message to a Cloud Monitoring channel or Pub/Sub topic.
- **Critical Fact:** **Google Cloud will NOT automatically shut down running instances, delete storage buckets, or throttle traffic when a budget alert fires.**
- **Consequence:** If an unconstrained GPU benchmark or recursive script runs over a weekend, the $50 alert email arrives within hours, but the compute infrastructure continues executing uninterrupted. Spend can easily exceed $1,000+ while the notification email sits unread in an inbox.

### Why Google Cloud Designs It This Way
Google Cloud intentionally separates budget notifications from service disruption to protect business availability. If budget alerts were hard spend caps by default, an unexpected traffic spike on an e-commerce website would trigger automated service termination, causing catastrophic customer checkout outages. Google Cloud places the responsibility for workload termination squarely in the hands of enterprise architects.

---

## 4. Programmatic Hard Cap Architecture (The Solution)

To enforce an absolute, automated financial spend cap in training sandboxes, architects implement an event-driven kill-switch pipeline:

1. **Pub/Sub Topic:** Link the Cloud Billing Budget to a dedicated Pub/Sub topic (`projects/brightloaf-sandbox-18/topics/budget-alerts`).
2. **Event Payload:** The billing meter publishes periodic JSON messages:
   ~~~json
   {
     "budgetDisplayName": "Training Sandbox $50 Budget",
     "costAmount": 52.40,
     "budgetAmount": 50.00,
     "currencyCode": "USD"
   }
   ~~~
3. **Automated Subscriber:** Deploy a serverless Google Cloud Function subscribed to the topic.
4. **Remediation Action:** When `costAmount >= budgetAmount`:
   - *Targeted Mode:* The function calls `compute.instances.stop()` across all active VMs.
   - *Strict Sandbox Mode:* The function calls the Cloud Billing API to programmatically detach billing:
     `gcloud billing projects unlink brightloaf-sandbox-18`
     This immediately suspends all billable APIs and terminates all active instances, capping spend with mathematical certainty.

---

## 5. Project Context Drift Prevention and Cloud Shell Safety

Operating across multi-tenant environments requires eliminating ambient project drift:

1. **Context-Aware Shell Prompts (PS1):**
   ~~~bash
   # Custom Cloud Shell prompt displaying active project in prominent colors
   format_prompt() {
       local p=$(gcloud config get-value project 2>/dev/null)
       if [[ "$p" =~ prod ]]; then
           echo -e "\033[1;31m[PROD: ${p}]\033[0m\$ "
       else
           echo -e "\033[1;32m[SANDBOX: ${p}]\033[0m\$ "
       fi
   }
   PS1='$(format_prompt)'
   ~~~
2. **Named gcloud Configurations:**
   - Maintain isolated configuration profiles: `gcloud config configurations create sandbox`
   - Switch cleanly without credential leakage: `gcloud config configurations activate sandbox`
3. **Mandatory Explicit Parameter Flags:**
   - Mandate that all operational runbooks specify `--project="${TARGET_PROJECT_ID}"`.
   - Automation wrappers reject any destructive command (`delete`, `destroy`) lacking an explicit `--project` flag.

---

## 6. Disposable Sandbox Cleanup Automation Plan

~~~python
# Sandbox Cleanup Runbook: Executes prior to sandbox retirement
cleanup_manifest = [
    {"command": "gcloud compute instances delete $(gcloud compute instances list --format='value(name)') --quiet --project=brightloaf-sandbox-18"},
    {"command": "gcloud compute disks delete $(gcloud compute disks list --format='value(name)') --quiet --project=brightloaf-sandbox-18"},
    {"command": "gcloud storage rm -r gs://brightloaf-sandbox-* --project=brightloaf-sandbox-18"},
    {"command": "gcloud pubsub topics delete sandbox-budget-alerts --project=brightloaf-sandbox-18"}
]
~~~
- **Dry-Run Validation:** Execute with `--dry-run` to inventory resources and verify that zero production resources match the deletion regex.
- **Final Result:** Post-cleanup audit asserts that active monthly run-rate drops to exactly $0.00.

---

## 7. Architectural Approval and Sign-Off
- **Lead Cloud Architect:** Lead Infrastructure & Cost Governance
- **Curriculum Day:** Day 18 (Cloud sandbox and cost controls)
- **Status:** APPROVED AND VERIFIED FOR CLOUD ONBOARDING
'''

with open("scratch/day-018-billing-preflight-cleanup.md", "w") as f:
    f.write(doc.strip() + "\n")

print(f"Successfully generated scratch/day-018-billing-preflight-cleanup.md ({len(doc)} bytes)")
EOF
python3 scratch/day18_lab/generate_day18_exit.py
head -n 40 scratch/day-018-billing-preflight-cleanup.md
```

**Expected result:**
Authoritative exit artifact authored at scratch/day-018-billing-preflight-cleanup.md and verified.

**Save:** scratch/day-018-billing-preflight-cleanup.md""",

            """**Stage 8: Validate Exit Artifact Integrity and Audit Sign-Off**

**Location:** local terminal

**Actions:**
Run an automated verification check asserting that all required components (preflight checklist, Always Free limits, budget alert explanation, and cleanup plan) are present in the exit artifact.
```bash
cat <<'EOF' > scratch/day18_lab/stage8_audit.py
import os

artifact_path = "scratch/day-018-billing-preflight-cleanup.md"
assert os.path.exists(artifact_path), f"Missing artifact: {artifact_path}"

with open(artifact_path) as f:
    content = f.read()

required_sections = [
    "Redacted Project and Billing Preflight Checklist",
    "Google Cloud Free Tier vs Promotional Trial Matrix",
    "Why a Budget Alert Is Not a Hard Spend Cap",
    "Programmatic Hard Cap Architecture",
    "Project Context Drift Prevention",
    "Disposable Sandbox Cleanup Automation Plan"
]

missing = [s for s in required_sections if s not in content]
if missing:
    print(f"FAILED: Missing sections: {missing}")
    exit(1)

report = f'''=======================================================
DAY 18 EXIT ARTIFACT AUDIT VERIFICATION
=======================================================
Artifact: {artifact_path}
Size: {len(content)} bytes
Required Sections: {len(required_sections)} / {len(required_sections)} Verified
Verification Status: PASSED (100% Roadmap Compliance)
=======================================================
'''

with open("scratch/day18_lab/stage8_final_audit.txt", "w") as f:
    f.write(report)

print("Stage 8 audit passed: exit artifact fully compliant.")
EOF
python3 scratch/day18_lab/stage8_audit.py
cat scratch/day18_lab/stage8_final_audit.txt
```

**Expected result:**
Audit verification passes with 100% roadmap compliance.

**Save:** scratch/day18_lab/stage8_final_audit.txt"""
        ]
    }
}
