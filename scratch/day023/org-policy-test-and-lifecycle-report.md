# Brightloaf Enterprise Cloud: Organization Policy & Lifecycle Report
**Document Version:** 1.0.0 | **Date:** 2026-09-27 | **Scope:** Google Cloud Enterprise Governance

## 1. Executive Summary & Core Architectural Invariant
This document establishes Brightloaf's verified Organization Policy guardrails and Project Lifecycle governance framework. It defines programmatic controls for project creation, liens, soft recovery windows, and admission-time policy enforcement across all enterprise workloads.

### Core Business Invariant:
> **Duplicate Fulfillment Invariant:** Replaying an order, recovering a project, or reconnecting network interfaces must never cause a second physical fulfillment (<= 1 physical fulfillment per unique order ID). Deduplication tokens and idempotent database mutations remain protected across all lifecycle transitions.

---

## 2. Project Lifecycle State Machine Specification
```text
+--------------------+        Lien Blocks Deletion        +-------------------------+
|      ACTIVE        | <--------------------------------- | Deletion Attempt Failed |
| (Normal Operation) |                                    +-------------------------+
+--------------------+
          |
          | projects.delete (Lien Released)
          v
+-----------------------------+     projects.undelete     +--------------------+
|      DELETE_REQUESTED       | ------------------------> |       ACTIVE       |
| (30-Day Soft Recovery Window|    (Billing Re-linked)    | (Normal Operation) |
+-----------------------------+                           +--------------------+
          |
          | Day 31: Expiry
          v
+-----------------------------+
|           DELETED           |
| (Permanent Purge / Shredded)|
+-----------------------------+
```

### Lifecycle Transition Matrix:
1. **ACTIVE -> DELETE_REQUESTED:** Initiated by `projects.delete`. Blocked if any active `resourcemanager.lien` is present. Compute instances stop immediately; billing decouples; external static IPs are released.
2. **DELETE_REQUESTED -> ACTIVE (Recovery):** Initiated by `projects.undelete` within 30 days. Restores project configuration and persistent disks. Billing account must be manually re-linked.
3. **DELETE_REQUESTED -> DELETED (Purge):** Occurs automatically after 30 days. Cryptographic disk wipe; metadata purged; Project ID permanently retired and never reusable.

---

## 3. Organization Policy Test Plan & Admission Evaluation Matrix

### Enforced Constraints:
1. `constraints/compute.vmExternalIpAccess`: Boolean Constraint = Enforce (Deny All External Public IPs).
2. `constraints/gcp.resourceLocations`: List Constraint = Allowed `['in:us-locations']` (`us-central1`, `us-east1`, `us-east4`, `us-west1`).

### Evaluation Results (Predictions vs. Observations):
| Test Case ID | Resource Description | Target Region / Zone | Public IP Requested | Predicted Result | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TEST-01** | Backend Order API VM | `us-central1-a` | False (Internal Only) | ACCEPTED | ACCEPTED | PASS |
| **TEST-02** | Analytics Worker VM  | `us-central1-a` | True  (Public NAT IP) | REJECTED | REJECTED | PASS |
| **TEST-03** | Staging Test VM      | `europe-west3-b` | False (Internal Only) | REJECTED | REJECTED | PASS |
| **TEST-04** | Contractor Test Node | `europe-west3-b` | True  (Public NAT IP) | REJECTED | REJECTED | PASS |

---

## 4. Policy Rollback Simulation & Recovery Plan
In the event that an organization policy constraint disrupts a mission-critical production deployment:
1. **Rollback Execution:** The policy is updated using Terraform or gcloud to inherit from parent (`inheritFromParent: true`) or disabled via `disable-enforce`.
2. **Admission Restored:** Immediate verification confirms that valid temporary configurations succeed without control-plane blockages.
3. **Audit Trail:** All policy modifications are captured in Cloud Audit Activity logs for forensic compliance review.
4. **Invariant Safeguard:** Deduplication tables verify that zero order replay anomalies occurred during the transition window, guaranteeing `<= 1 physical fulfillment per unique order ID`.

---
*End of Report. Verified against Google Cloud Resource Manager and Organization Policy APIs.*
