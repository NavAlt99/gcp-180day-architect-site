# BrightLoaf Enterprise Cloud Landing Zone Specification (Draft)

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
