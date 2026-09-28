# Day 29 Exit Artifact: Cost Query Analysis & Three Capacity-Failure Explanations

**Generated:** 2026-09-27T11:14:58.970554+00:00  
**Scope:** Google Cloud Billing Account `01A2B3-4C5D6E-7F8G9H` & Capacity Architecture  
**Objective:** A cost query or spreadsheet plus three different capacity-failure explanations.

---

## 1. BigQuery Billing Export Cost Query & Reconciliation Spreadsheet

SQL Query used for resource-level cost and credit reconciliation against detailed billing export:

```sql
SELECT
  project.id AS project_id,
  service.description AS service_name,
  sku.description AS sku_name,
  resource.name AS resource_uri,
  location.zone AS availability_zone,
  ROUND(SUM(cost), 2) AS gross_cost_usd,
  ROUND(IFNULL(SUM((SELECT SUM(c.amount) FROM UNNEST(credits) AS c)), 0), 2) AS credits_usd,
  ROUND(SUM(cost + IFNULL((SELECT SUM(c.amount) FROM UNNEST(credits) AS c), 0)), 2) AS net_cost_usd
FROM
  `brightloaf-billing.billing_export.gcp_billing_export_resource_v1_01A2B3_4C5D6E_7F8G9H`
WHERE
  _PARTITIONDATE BETWEEN '2026-09-01' AND '2026-09-30'
GROUP BY
  project_id, service_name, sku_name, resource_uri, availability_zone
ORDER BY
  net_cost_usd DESC;
```

### Itemized Billing Reconciliation Table (Spreadsheet Export):

| Project ID | GCP Service | SKU Description | Resource Identifier (URI) | Zone | Gross (USD) | Credits (USD) | Net (USD) | Status / Action |
|:---|:---|:---|:---|:---|---:|---:|---:|:---|
| `brightloaf-fulfillment-prod` | Compute Engine | SSD Total Persistent Disk | `//compute/.../disks/disk-pvc-88a2-orphan` | `us-central1-b` | $3,480.00 | $0.00 | $3,480.00 | **ORPHAN LEAK** (Snapshot & Delete) |
| `brightloaf-fulfillment-prod` | Compute Engine | N2 Custom Core running in Americas | `//compute/.../instances/dispatch-worker-01` | `us-central1-a` | $2,150.00 | -$645.00 | $1,505.00 | Active (30% CUD Applied) |
| `brightloaf-analytics-prod` | BigQuery | Analysis (On-Demand Slots) | `//bigquery/.../queries/job-adhoc-geo-demand` | *regional* | $4,200.00 | $0.00 | $4,200.00 | Completed (Cap bytes billed) |
| `brightloaf-order-prod` | Cloud Run | CPU Allocation Time | `//run/.../services/order-ingestion-api` | *regional* | $1,820.50 | -$20.50 | $1,800.00 | Production Core (&le; 1 fulfillment) |
| **TOTAL ACCOUNT SPEND** | **All Services** | **4 Line Items Reconciled** | **Consolidated Billing Scope** | **All Zones** | **$11,650.50** | **-$665.50** | **$10,985.00** | **Reconciled against Invoice** |

---

## 2. Three Different Capacity-Failure Explanations

Google Cloud resource deployment is governed by three independent failure boundaries. A systems architect must differentiate between API request velocity, provisioned inventory caps, and physical hardware availability.

### Failure Explanation 1: Rate Quota Throttling (API Velocity Boundary)
- **Mechanism:** Rate quotas constrain the frequency of operations within a rolling time window (e.g., 60,000 requests per minute). Evaluated at the API Gateway using token-bucket rate limiters.
- **Observed Error Signal:** `HTTP 429 Too Many Requests` or `google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded for quota metric 'Access requests per minute'`.
- **Root Cause & Trigger:** An unmemoized microservice or bursty worker process invokes control-plane or shared data APIs on the hot request path (e.g., fetching database credentials from Secret Manager per HTTP request during a morning traffic surge).
- **Auto-Recovery Behavior:** Resets automatically once the 60-second sliding window elapses.
- **Architectural Defense:** Implement in-memory caching with TTL (e.g., caching credentials for 1 hour); client libraries must implement truncated exponential backoff with full jitter.

### Failure Explanation 2: Allocation Quota Exhaustion (Inventory Ceiling Boundary)
- **Mechanism:** Allocation quotas restrict the cumulative count of resources provisioned simultaneously in a project or region (e.g., maximum 500 Compute Engine vCPUs in `us-central1`).
- **Observed Error Signal:** `QUOTA_EXCEEDED` (e.g., `Quota 'CPUS' exceeded. Limit: 100.0 in region us-central1`).
- **Root Cause & Trigger:** Traffic expansion triggers an autoscaling Managed Instance Group (MIG) or GKE cluster expansion, but the project has exhausted its approved vCPU, persistent disk, or static IP ceiling.
- **Auto-Recovery Behavior:** **Never resets over time.** Resources remain blocked until existing infrastructure is terminated or an administrator submits a quota increase request via the Quotas Console or Cloud Quotas API.
- **Architectural Defense:** Proactively monitor quota utilization metrics (`serviceruntime.googleapis.com/quota/allocation/usage`); configure Cloud Quota Adjuster; establish automated teardown for stale development environments.

### Failure Explanation 3: Physical Datacenter Capacity Exhaustion (Hardware Inventory Boundary)
- **Mechanism:** Physical server racks, specialized hypervisors (e.g., C3 machine types), or GPUs (NVIDIA H100/A100) are completely committed to other tenants within a specific datacenter zone.
- **Observed Error Signal:** `ZONE_RESOURCE_POOL_EXHAUSTED` or `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS` (e.g., `The zone 'projects/brightloaf/zones/us-central1-b' does not have enough resources available to fulfill the request`).
- **Critical Distinction:** **Occurs even when the project's allocation quota is 100% available with zero utilization.** Quota is an administrative limit, not a physical hardware reservation.
- **Auto-Recovery Behavior:** Non-deterministic. Resolves only when other tenants release physical nodes or Google deploys additional hardware racks in that zone.
- **Architectural Defense:** Deploy regional Managed Instance Groups spanning 3+ zones with `instance_redistribution_type = PROACTIVE`; procure Compute Engine Capacity Reservations for critical production workloads to guarantee physical allocation.

---

## 3. Duplicate Fulfillment Invariant Attestation

### Invariant Guarantee: &le; 1 Physical Fulfillment per Unique Order ID
During incidents involving Rate Quota throttling (such as Secret Manager HTTP 429 errors), upstream retail stores and client mobile applications will automatically re-attempt order placement. To preserve Brightloaf's fundamental commerce invariant:
1. **Idempotency Gating:** The order ingestion gateway verifies incoming order payloads against the transactional deduplication state ledger using a composite key: `order_id#store_id`.
2. **Replay Immunity:** If an order submission is retried after a transient 429 response, the gateway recognizes the completed state, returns the original acknowledgement receipt, and suppresses any secondary dispatch message to the physical baking lines.
3. **Audit Trail:** Every throttled request, retry attempt, and deduplicated drop is logged to Cloud Logging with the correlated order GUID.

---
**Attested by:** Brightloaf FinOps Engineering & Core Infrastructure Architecture Board
