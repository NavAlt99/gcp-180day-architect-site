# Day 25 Exit Artifact: Redacted Authorization Evidence

**Generated:** 2026-09-27T10:03:19.301543+00:00
**Scope:** Resource Hierarchy `organizations/1029384756/folders/bakery-operations/projects/brightloaf-prod-fulfillment`
**Objective:** Redacted authorization evidence tied to principal, resource, role and condition.

---

## 1. Effective Policy Graph Resolution

The effective policy represents the strict additive union of role bindings across the hierarchical lineage:

```
[Organization: 1029384756]
   │
   └── [Folder: bakery-operations]
          │
          └── [Project: brightloaf-prod-fulfillment]
                 │
                 └── [Resource: topics/prod-orders-v1]
```

### Principal: `serviceAccount:order-ingest@brightloaf-prod.iam.gserviceaccount.com`
- **Inherited From:** `projects/brightloaf-prod-fulfillment`
- **Role:** `roles/pubsub.publisher`
- **Condition Title:** `prod_orders_topic_only`
- **Condition Expression:** `resource.name.startsWith('projects/_/topics/prod-orders')`

### Principal: `group:all-devs@brightloaf.internal`
- **Inherited From:** `folders/bakery-operations`
  - **Role:** `roles/monitoring.viewer` (Unconditional)
- **Inherited From:** `projects/brightloaf-prod-fulfillment`
  - **Role:** `roles/pubsub.viewer` (Unconditional)

---

## 2. Redacted Authorization Decision Evidence

| Test ID | Principal (Redacted) | Target Resource | Requested Role / Permission | Condition Evaluated | Decision | Evaluation Rationale |
|:---|:---|:---|:---|:---|:---|:---|
| **AUTH-01** | `sa-order-ingest@***` | `.../topics/prod-orders-v1` | `roles/pubsub.publisher` | `resource.name.startsWith('projects/_/topics/prod-orders')` | <span style="color:#22c55e;font-weight:bold;">ALLOW (200 OK)</span> | Allowed under condition 'prod_orders_topic_only' inherited from projects/brightloaf-prod-fulfillment |
| **AUTH-02** | `dev-user@***` | `.../topics/prod-orders-v1` | `roles/pubsub.admin` | None (Unconditional check) | <span style="color:#f43f5e;font-weight:bold;">DENY (403 PERMISSION_DENIED)</span> | Denied: Permission not present in effective policy union |

---

## 3. Invariant Verification & Compliance Attestation

- **Duplicate Fulfillment Invariant (&le; 1 Physical Fulfillment per Order):**
  - Narrowing `order-ingest` publisher permissions to authorized topics prevents accidental ingestion into unmonitored dead-letter queues or legacy topics.
  - Denying `roles/pubsub.admin` to developer groups protects the active `prod-orders-v1` topic from uncoordinated deletion, preventing dropped ack offsets and subsequent double-baking replays.
- **Principle of Least Privilege:**
  - Zero basic primitive roles (`roles/owner`, `roles/editor`, `roles/viewer`) present in effective policies.
  - All temporal and resource scopes verified through Policy Version 3 CEL condition evaluation.

**Attested by:** Brightloaf Cloud Security Architecture Team
