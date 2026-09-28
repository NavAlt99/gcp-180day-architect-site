# Brightloaf Enterprise Cloud: Workforce Identity Matrix
**Document Version:** 1.0.0 | **Date:** 2026-09-27 | **Scope:** Google Cloud IAM & Workforce Architecture

## 1. Executive Summary & Core Architectural Invariants
This document defines Brightloaf's authoritative identity matrix across all Google Cloud environments. It categorizes workforce human principals, automated workload service accounts, organizational Google Groups, and external partner identities, enforcing the strict architectural mandate that **IAM roles must be assigned to Google Groups, never to individual user accounts**.

### Core Business Invariant:
> **Duplicate Fulfillment Invariant:** Replaying an order, rotating credentials, or executing identity offboarding must never cause a second physical fulfillment (<= 1 physical fulfillment per unique order ID). Deduplication tokens and idempotent database mutations remain protected across all identity transitions.

---

## 2. Workforce Identity Matrix: People, Workloads, Groups, and Externals

| Category | Principal Type / Syntax | Identity Provider | Associated IAM Roles | Target Resource Scope | Security Governance & MFA |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **People (Workforce)** | `group:pos-engineers@brightloaf.com` | Cloud Identity / Okta | `roles/viewer`, `roles/logging.viewer` | `/Non-Production/POS` | Hardware FIDO2 Security Key; SSO |
| **People (SRE / Ops)** | `group:pos-sre@brightloaf.com` | Cloud Identity / Okta | `roles/monitoring.editor`, `roles/clouddebugger.user` | `/Production/POS` | Break-Glass PAM with Time-Bound Lease |
| **Workloads (App)** | `serviceAccount:order-api-sa@bl-prod.iam.gserviceaccount.com` | Google Cloud IAM | `roles/spanner.databaseUser`, `roles/pubsub.publisher` | `bl-order-fulfill-prod` | Workload Identity Federation (No JSON keys) |
| **Workloads (CI/CD)**| `serviceAccount:pos-deployer-sa@bl-prod.iam.gserviceaccount.com` | Google Cloud IAM | `roles/container.developer`, `roles/artifactregistry.writer` | `bl-pos-production` | GitHub Actions OIDC Short-Lived Tokens |
| **Groups (Functional)**| `group:franchise-auditors@brightloaf.com` | Cloud Identity | `roles/bigquery.dataViewer` | `bl-analytics-prod` | Enforces corporate directory membership |
| **External Identities**| `group:contractor-logistics@brightloaf.com` | Managed Cloud Identity | Custom: `roles/logisticsViewer` | `bl-logistics-prod` | Managed corporate domain only (Zero @gmail) |

---

## 3. Direct User to Group Consolidation Audit
- **Pre-Migration IAM Policy Size:** 251,480 bytes (1,488 member bindings; exceeded 250 KB limit).
- **Post-Migration IAM Policy Size:** 4,820 bytes (14 Google Group bindings).
- **Compression Ratio:** 98.1% policy size reduction.
- **Orphan Accounts Pruned:** 42 departed contractors and former employees.

---

## 4. Domain Restricted Sharing & Public Access Prevention
1. **Domain Restricted Sharing:** `constraints/iam.allowedPolicyMemberDomains` enforced at Org root (Customer ID: `C01234567`). Blocks consumer `@gmail.com` accounts.
2. **Public Access Prevention (PAP):** `constraints/storage.publicAccessPrevention` enforced on all buckets. Blocks `allUsers` and `allAuthenticatedUsers`.

---
*End of Matrix. Verified against Google Cloud Resource Manager, Cloud Identity, and IAM APIs.*
