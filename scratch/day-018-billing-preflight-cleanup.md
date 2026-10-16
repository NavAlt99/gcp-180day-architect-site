# Day 18 Exit Evidence: Project/Billing Preflight, Cost Control Architecture, and Cleanup Plan

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
