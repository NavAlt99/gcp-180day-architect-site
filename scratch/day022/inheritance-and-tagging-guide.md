# Brightloaf Enterprise Cloud: Inheritance and Tagging Taxonomy Guide
**Document Version:** 1.0.0 | **Date:** 2026-09-27 | **Scope:** All Google Cloud Workloads

## 1. Executive Summary and Core Architectural Invariants
This document defines Brightloaf's authoritative standard for resource metadata, access control inheritance, and network packet filtering across Google Cloud. It establishes concrete rules for **Resource Labels**, **Resource Manager Tags**, and **Compute Engine Network Tags**, preventing operational conflation and security vulnerabilities.

### Core Business Invariant:
> **Duplicate Fulfillment Invariant:** Replaying an order or recovering dropped network connections must never cause a second physical fulfillment (<= 1 physical fulfillment per unique order ID). Deduplication tokens and idempotent database mutations must remain protected by least-privilege IAM and strict network isolation.

---

## 2. Mathematical Inheritance Calculation Matrix
Google Cloud IAM allow policies are strictly additive ($P_{effective} = \bigcup P_{ancestors}$). Standard allow bindings have no subtractive capability.

| Hierarchy Tier | Resource Identifier | Bound IAM Role | Injected Permissions | Cumulative Effective Permissions |
| :--- | :--- | :--- | :--- | :--- |
| **Organization** | `organizations/714029482103` | `roles/securityReviewer` | `iam.roles.list`, `iam.serviceAccounts.list`, `resourcemanager.organizations.get` | 3 baseline read permissions |
| **Folder Tier 1** | `folders/839102482019` (`/Production`) | None (Zero default broad roles) | (none) | 3 baseline read permissions |
| **Project Tier** | `projects/bl-order-fulfill-prod` | Custom: `roles/spannerViewer` | `spanner.databases.get`, `spanner.databases.select`, `spanner.sessions.create` | 6 permissions (Scoped least privilege) |
| **Leaf Resource**| `databases/orders-db` | None | (none) | 6 permissions |
| **Guardrail** | Organization Deny Policy | `deny: spanner.databases.drop` | Blocks drop across all automated service accounts | Hard stop overriding any inherited allow |

---

## 3. The Three-Plane Metadata Taxonomy

### Plane 1: Resource Labels (Operations and Cloud Billing)
- **Attachment Target:** All supported GCP resources (VMs, Buckets, Cloud SQL, BigQuery, Disks).
- **Inheritance:** NONE (Per-resource attribute; must be stamped during resource instantiation).
- **Format:** Lowercase alphanumeric with hyphens or underscores (Max 63 characters).
- **Mandatory Label Schema:**
  - `bl-environment`: `production` | `staging` | `development`
  - `bl-cost-center`: `c-104-baking` | `c-105-logistics` | `c-106-franchise`
  - `bl-application-id`: `bl-order-api` | `bl-order-fulfillment` | `bl-inventory`
  - `bl-data-classification`: `pci-token` | `confidential` | `internal`
  - `bl-managed-by`: `terraform`
- **Use Case:** BigQuery Cloud Billing breakdown queries and automated resource lifecycle pruning.
- **Security Boundary:** ZERO. Labels do NOT enforce IAM or VPC firewalls.

### Plane 2: Resource Manager Tags (Governance and Conditional IAM)
- **Attachment Target:** Organizations, Folders, Projects.
- **Inheritance:** YES (Inherits automatically down the container tree).
- **Format:** Centralized namespaced keys: `organizations/714029482103/tagKeys/env`.
- **Authorized Values:** `production`, `staging`, `development`.
- **Governance Roles:** Only principals with `roles/resourcemanager.tagAdmin` create tags; binding requires `roles/resourcemanager.tagUser`.
- **IAM Condition Integration:**
  ```cel
  // Grants Spanner Admin strictly if the project or folder inherits tag env: production
  resource.matchTag('714029482103/env', 'production')
  ```
- **Security Boundary:** HARD BOUNDARY. Protected against tampering by project-level developers.

### Plane 3: Network Tags (Compute Engine VPC Packet Filtering)
- **Attachment Target:** Compute Engine VM instances and Instance Templates ONLY.
- **Inheritance:** NONE (Per-VM instance string).
- **Format:** Lowercase RFC-1035 alphanumeric with hyphens (Max 63 characters).
- **Standardized Network Tags:**
  - `bl-net-order-api`: For frontend API ingress instances.
  - `bl-net-order-db`: For backend database listeners (Port 5432).
  - `bl-net-bastion-mgmt`: For authorized management bastion hosts.
- **VPC Firewall Rule Enforcement:**
  - Ingress to `targetTags: ["bl-net-order-db"]` on `tcp:5432` strictly requires `sourceTags: ["bl-net-order-api"]`.
  - Non-production subnets and developer bastions lack `bl-net-order-api` and are dropped by default.
- **Security Limitation:** Mutable via `compute.instances.setTags`. Must transition to Resource Manager Secure Tags for Next-Gen Firewalls in PCI zones.

---

## 4. Concrete Terraform Implementation Template
```hcl
# Example Production Database Provisioning with Strict 3-Plane Metadata

resource "google_compute_instance" "production_database" {
  name         = "bl-order-db-prod-vm"
  machine_type = "n2-standard-4"
  zone         = "us-central1-a"
  project      = "bl-order-fulfill-prod"

  # Plane 1: Labels for Billing and Inventory
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

# Plane 2: Resource Manager Tag Binding (IAM and Policy Governance)
resource "google_tags_tag_binding" "db_env_binding" {
  parent    = "//cloudresourcemanager.googleapis.com/projects/bl-order-fulfill-prod"
  tag_value = "tagValues/847192039481" # Corresponds to env: production
}

# Targeted VPC Firewall Rule utilizing Network Tags
resource "google_compute_firewall" "allow_db_from_api" {
  name        = "allow-order-db-from-api"
  network     = "bl-production-vpc"
  project     = "bl-order-fulfill-prod"
  description = "Restricts PostgreSQL 5432 ingress to verified API instances only"

  target_tags = ["bl-net-order-db"]
  source_tags = ["bl-net-order-api"]

  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }
}
```

---
*End of Specification. Verified against Google Cloud Resource Manager, IAM, and VPC Documentation.*
