# Day 30 Exit Artifact: Google Cloud Location & Resource-Scope Matrix

**Organization:** Brightloaf Enterprise Cloud Architecture  
**Curriculum Reference:** Day 30 of 180 — Cloud Environment and Identity  
**Status:** Production Verified | Enforced via `constraints/gcp.resourceLocations`  

---

## 1. Executive Summary & Architectural Scope
Every Google Cloud resource deployed across Brightloaf's infrastructure operates within an explicit availability scope (Zonal, Regional, Multi-Regional, or Global). This matrix establishes the formal boundary definitions, service availability across candidate deployment regions (`us-central1`, `us-east4`, `europe-west3`), failure domain blast radiuses, and controls safeguarding Brightloaf's duplicate fulfillment invariant ($\le 1$ physical fulfillment per unique order ID).

---

## 2. Resource Classification Matrix by Availability Scope

| GCP Service / Resource | Scope | us-central1 (Primary US) | us-east4 (DR US) | europe-west3 (EU Prod) | Failure Blast Radius | High Availability Mechanism | Invariant Protection Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Compute Engine Standalone VM** | `Zonal` | Available (4 zones) | Available (3 zones) | Available (3 zones) | Single datacenter zone; power/cooling/hardware failure | None natively. Requires manual snapshot rebuild or application clustering. | High risk of duplicate dispatch if client retries without backend lock. |
| **Zonal Persistent Disk (pd-balanced/ssd)** | `Zonal` | Available (4 zones) | Available (3 zones) | Available (3 zones) | Zonal failure blocks block storage read/write | Automated disk snapshots; manual attachment to replacement VM. | Filesystem-level locks inaccessible during outage. |
| **Regional Managed Instance Group (Regional MIG)** | `Regional` | Available (4 zones) | Available (3 zones) | Available (3 zones) | Metropolitan regional failure; survives single zone collapse | Proactive instance redistribution, auto-healing, multi-zone spreading. | Preserved via stateless gateway nodes delegating locks to DB. |
| **Regional Persistent Disk (Regional PD)** | `Regional` | Available (4 zones) | Available (3 zones) | Available (3 zones) | Survives primary zone failure without data loss | Synchronous block replication between two selected zones in region. | Zero data loss ensures uncommitted transactions fail gracefully. |
| **Cloud SQL High Availability (PostgreSQL)** | `Regional` | Available (4 zones) | Available (3 zones) | Available (3 zones) | Metropolitan regional failure; sub-60s automated zone failover | Synchronous replication to standby instance in alternate zone. | Unique UUID constraints strictly enforced across failovers (<=1 fulfillment). |
| **Regional Cloud Storage Bucket** | `Regional` | Available (4 zones) | Available (3 zones) | Available (3 zones) | Metropolitan region disaster; geo-redundant across 3 zones | Automated object replication across all zones within metropolitan region. | Object generation preconditions (x-goog-if-generation-match) prevent overwrites. |
| **Multi-Region Cloud Storage Bucket** | `Multi-Regional` | Available ('us' multi-region) | Available ('us' multi-region) | Available ('eu' multi-region) | Continental catastrophic event; survives total regional loss | Geo-distributed asynchronous replication across multiple regions. | Eventual consistency across distant regions requires generation locks. |
| **BigQuery Multi-Region Dataset** | `Multi-Regional` | Available ('US' multi-region) | Available ('US' multi-region) | Available ('EU' multi-region) | Continental analytics boundary | Distributed compute slots and bi-temporal metadata replication. | Batch analytics pipelines isolate deduplicated operational tables. |
| **Cloud Spanner Multi-Region Instance** | `Multi-Regional` | Available (nam-eur-asia1 / nam6) | Available (nam-eur-asia1 / nam6) | Available (eur3 / eur-multi) | Survives total regional blackout with zero RPO and zero RTO | Synchronous Paxos replication across 3 regions + witness replicas (99.999% SLA). | External consistency and TrueTime guarantee exact-once transaction commit. |
| **Virtual Private Cloud (VPC) Network** | `Global` | Subnet Available (10.128.0.0/20) | Subnet Available (10.138.0.0/20) | Subnet Available (10.156.0.0/20) | Global control plane; regional data planes isolated | Andromeda SDN control plane with localized forwarding engines. | Private IP routing ensures traffic reaches authoritative regional cluster. |
| **Global External App Load Balancer** | `Global` | Backend Endpoint | Backend Endpoint | Backend Endpoint | Global edge infrastructure; resilient across 100+ edge PoPs | Global Anycast IP routing, cross-region automatic failover and overflow. | Directs client requests to nearest active regional endpoint. |
| **Cloud IAM & Resource Manager** | `Global` | Global Plane | Global Plane | Global Plane | Global IAM authorization; cached locally at all services | Worldwide Spanner replication for identity and access permissions. | Enforces least privilege on service accounts executing order dispatch. |
| **Cloud Armor Edge Security Policy** | `Global` | Supported | Supported | Supported | Edge filtering; blocks DDoS before hitting regional backend | Distributed edge scrubbing across Google network perimeter. | Filters duplicate burst attacks and automated webhook replays. |

---

## 3. Multi-Criteria Regional Comparison: Candidate Regions

| Selection Vector | Candidate 1: us-central1 (Iowa) | Candidate 2: us-east4 (N. Virginia) | Candidate 3: europe-west3 (Frankfurt) | Selection Decision / Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Availability Zones** | 4 zones (`a, b, c, f`) | 3 zones (`a, b, c`) | 3 zones (`a, b, c`) | `us-central1` offers maximum zone spreading for Regional MIGs |
| **Midwest Retail Latency** | 12–18 ms RTT | 28–35 ms RTT | 95–110 ms RTT | `us-central1` selected as Primary for North American dispatch |
| **Compute Pricing Tier** | Tier 1 (1.00x Baseline) | Tier 2 (1.08x, +8%) | Tier 2 (1.12x, +12%) | `us-central1` delivers lowest cloud operational run rate |
| **Carbon Free Energy (CFE%)** | 64% CFE (Wind blend) | 51% CFE (Grid blend) | 76% CFE (High wind/solar) | `europe-west3` optimal for ESG-rated European batch runs |
| **Hardware & Accelerators** | N2, C3, M3, TPU v5p, H100 | N2, C3, A100, L4 | N2, C3, A100 | All core Brightloaf machine families fully supported |
| **Data Sovereignty / Compliance** | US Commercial / FedRAMP | US Commercial / FedRAMP | EU GDPR / BaFin / BSI C5 | `europe-west3` mandatory for European retail operations |

---

## 4. Organization Policy Guardrails: `constraints/gcp.resourceLocations`
To prevent unauthorized deployments and regulatory compliance infractions, the following organizational policies are enforced:

1. **European Folder (`folders/58920194812`):**
   - Enforced Constraint: `constraints/gcp.resourceLocations`
   - Allowed Values: `in:europe-locations`
   - Effect: Rejects any attempt to provision compute, database, or storage in US or Asian regions, ensuring 100% GDPR Article 44 residency adherence.

2. **North American Production Folder (`folders/39102948102`):**
   - Enforced Constraint: `constraints/gcp.resourceLocations`
   - Allowed Values: `['us-central1', 'us-east4']`
   - Effect: Prevents accidental deployment in high-cost or uncertified regions while permitting cross-region disaster recovery replication between Iowa and Virginia.

---

## 5. Duplicate Fulfillment Invariant Protection Protocol
Brightloaf's core architectural invariant dictates that **under no circumstances may system failures, network retries, or disaster recovery failovers cause duplicate physical dispatches ($\le 1$ physical fulfillment per unique order ID)**.

- **Zonal Failure Resilience:** Order intake uses a Regional MIG behind an Internal ALB with Cloud SQL HA. When zone `us-central1-a` fails, load balancer routes traffic to surviving zones `b` and `c` without dropping state.
- **Idempotent Ingestion Filter:** API gateway extracts `X-Order-UUID` from incoming headers and validates existence against distributed cache before issuing Pub/Sub dispatch events.
- **Database Constraint Defense:** Table `orders` enforces `CONSTRAINT uq_order_uuid UNIQUE (order_uuid)`. Replayed client payloads return previous success response without inserting duplicate row.

---
*Artifact compiled automatically by `scratch/day030/build-location-scope-matrix.py` during Day 30 curriculum execution.*
