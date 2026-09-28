# Day 28 Exit Artifact: Cost Attribution Worksheet & Duplicate Event Handling Behavior

**Generated:** 2026-09-27T11:05:51.307082+00:00  
**Cloud Billing Account:** `01A2B3-4C5D6E-7F8G9H`  
**Dataset Reference:** `brightloaf-billing.billing_export.gcp_billing_export_resource_v1_*`  
**Objective:** An attribution worksheet and notification handling behavior for duplicate events.

---

## 1. Departmental Cost Attribution Worksheet

Summary of resource-level costs unrolled from BigQuery detailed billing export records:

| Cost Center / Dimension | Environment | Allocated Spend (USD) | Department Share (%) | Label Governance Status |
|:---|:---|---:|---:|:---|
| **cc-bakery-ops** (Bakery Operations) | Production | $5,411.25 | 32.3% | Compliant (100% Labeled) |
| **cc-ecommerce** (Digital Storefront) | Production & Dev | $4,410.70 | 26.3% | Compliant (100% Labeled) |
| **cc-growth-mktg** (Growth & Marketing) | Staging | $1,420.30 | 8.5% | Compliant (100% Labeled) |
| **UNALLOCATED_SHARED_DEBT** (Orphan Compute) | Unspecified | $5,500.00 | 32.9% | **Non-Compliant (Audit Triggered)** |
| **TOTAL CONSOLIDATED SPEND** | **All Tiers** | **$16,742.25** | **100.0%** | **Overall Labeled: 67.1%** |

### Granular Resource Line Items:
| Resource ID | GCP Service | Project ID | Cost Center | Environment | Cost (USD) |
|:---|:---|:---|:---|:---|---:|
| `cr-order-ingestion-prod-01` | Cloud Run | `brightloaf-order-prod` | `cc-bakery-ops` | production | $1,840.50 |
| `csql-order-db-primary` | Cloud SQL | `brightloaf-order-prod` | `cc-bakery-ops` | production | $2,450.00 |
| `gce-dispatch-optimizer-worker` | Compute Engine | `brightloaf-order-prod` | `cc-bakery-ops` | production | $1,120.75 |
| `cr-storefront-web-prod` | Cloud Run | `brightloaf-ecommerce-prod` | `cc-ecommerce` | production | $3,180.20 |
| `memcache-recommender-prod` | Memorystore | `brightloaf-ecommerce-prod` | `cc-ecommerce` | production | $820.00 |
| `gce-customer-portal-dev` | Compute Engine | `brightloaf-ecommerce-dev` | `cc-ecommerce` | development | $410.50 |
| `bq-growth-abtesting-lakehouse` | BigQuery | `brightloaf-analytics-staging` | `cc-growth-mktg` | staging | $1,420.30 |
| `gke-adhoc-batch-pool` | GKE | `brightloaf-shared-infra` | *UNALLOCATED* | *unspecified* | $3,650.00 |
| `bq-unpartitioned-analysis-spike`| BigQuery | `brightloaf-shared-infra` | *UNALLOCATED* | *unspecified* | $1,850.00 |

---

## 2. Notification Handling Behavior for Duplicate Pub/Sub Events

Google Cloud Billing guarantees **at-least-once** delivery over Cloud Pub/Sub. The automated budget remediation consumer enforces the following deterministic handling behavior:

```
[Incoming Pub/Sub Message]
         │
         ▼
[Extract Envelope Properties]
  • budgetDisplayName: "brightloaf-core-monthly"
  • costIntervalStart: "2026-09-01T00:00:00Z"
  • alertThresholdExceeded: 1.0
         │
         ▼
[Compute Composite Idempotency Key]
  dedup_key = f"{budgetDisplayName}#{costIntervalStart}#{alertThresholdExceeded:.2f}"
         │
         ▼
[Query Persistent State Store (Firestore / Redis)]
   ├── Exists (Status == COMPLETED)?
   │     └──► Log: "[IDEMPOTENT_DROP] Duplicate event detected. ACK returned without action."
   │          Acknowledge message (Pub/Sub ACK) -> DROP ACTION
   │
   └── Not Found?
         ├── Atomic Write: Set dedup_key -> "PROCESSING" with 45-day TTL
         ├── Safety Filter: Verify target resource labels (env != 'production')
         ├── Execute Remediation: Scale down development workers only
         ├── Finalize State: Set dedup_key -> "COMPLETED"
         └── Acknowledge message (Pub/Sub ACK)
```

### Safety & Invariant Attestation:
1. **Duplicate Fulfillment Invariant (&le; 1 physical fulfillment per unique order ID):** Automated quota, throttling, or billing remediation workflows explicitly exclude resources tagged `env: production` and `service: order-ingestion`. Retries and duplicate events can never freeze order intake or disrupt fulfillment reconciliation.
2. **Deterministic Deduplication:** Duplicate redeliveries resulting from network delays or acknowledgment timeouts (such as `ps-msg-101-retry` and `ps-msg-103-redelivered`) are intercepted by the state store, returning immediate Pub/Sub ACKs without modifying infrastructure.
3. **Auditability:** All deduplication events emit structured log records to Cloud Logging (`DUPLICATE_EVENT_DROPPED`) with timestamp, previous processing reference, and zero-action confirmation.

---
**Attested by:** Brightloaf FinOps Engineering & Cloud Architecture Review Board
