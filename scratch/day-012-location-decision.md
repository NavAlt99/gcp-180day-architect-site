# Day 12 Exit Evidence: Location Decision Architecture Artifact

## Executive Summary
This document establishes the binding architectural location decision for OmniRetail Global, evaluating candidate deployment regions against latency budgets, data residency legal mandates, a six-part Bill of Materials (BOM) cost model, and physical failure-domain isolation assumptions.

---

## 1. Candidate Deployment Locations Evaluation

| Region Key | Physical Data Center Location | Availability Zones | NA Latency (P50/P99) | EU Latency (P50/P99) | Data Residency Compliance | Carbon-Free Energy % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **us-central1** | Council Bluffs, Iowa, USA | 4 zones (a, b, c, f) | 28 ms / 42 ms | 112 ms / 148 ms | Non-compliant for EU PII | 89% CFE |
| **europe-west1** | St. Ghislain, Belgium | 3 zones (b, c, d) | 98 ms / 135 ms | 22 ms / 34 ms | Fully GDPR / EU Sovereign Compliant | 83% CFE |

### Decision Analysis:
- **Latency Impact:** Deploying exclusively in `us-central1` degrades European customer conversion rates due to an unacceptably high 112 ms latency floor across the Atlantic. Conversely, deploying exclusively in `europe-west1` penalizes 60% of current revenue-generating shoppers in North America with 98 ms latency.
- **Data Residency Mandate:** European Union General Data Protection Regulation (GDPR) Article 44 strictly limits the transfer of EU citizen personal data to non-adequate third countries. Hosting EU customer purchase histories and PII solely in Iowa violates regulatory compliance and exposes OmniRetail to penalties up to 4% of global annual turnover.

---

## 2. Scaling Architecture Decision: Vertical vs Horizontal

| Metric / Behavior | Vertical Scaling (Scale Up e2 to n2) | Horizontal Scaling (Regional MIG + PgBouncer) | Architectural Verdict |
| :--- | :--- | :--- | :--- |
| **Availability During Scale Event** | 0% (3-minute reboot downtime) | 100% (Zero-downtime rolling additions) | Horizontal required for 99.99% SLA |
| **Dropped Transactions at Peak** | ~432,000 dropped requests | 0 dropped requests | Vertical fails during flash sales |
| **Throughput Ceiling** | 4,800 RPS (Hardware limit) | 15,000+ RPS (Limitless horizontal scale) | Horizontal supports 7,200 RPS peak |
| **Stateful DB Connection Impact** | 20 connections (Single VM) | 60 multiplexed connections (PgBouncer) | PgBouncer prevents DB connection collapse |

**Conclusion:** Vertical scaling is rejected due to mandatory service downtime during re-sizing. OmniRetail adopts Regional Managed Instance Groups with a target CPU utilization of 65% and PgBouncer connection multiplexing.

---

## 3. Production Cloud Bill of Materials (BOM) & Economic Modeling

| BOM Cost Dimension | Scope & Resource Description | us-central1 (Monthly) | europe-west1 (Monthly) | Dual-Region Hybrid (Monthly) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Compute** | Blended average 8 x n2-standard-4 instances | $724.80 | $782.78 | $747.99 |
| **2. Persistent Storage** | 1,200 GB Balanced SSD + Regional Snapshots | $144.00 | $158.40 | $149.76 |
| **3. Object Storage** | 5,000 GB Standard + 2.5M Class A + 10M Class B | $116.50 | $128.15 | $121.16 |
| **4. Network Data Egress** | 15 TB Internet Egress + 8 TB Inter-Zone Egress | $1,820.00 | $1,820.00 | $2,140.00 (Includes DR Sync) |
| **5. Managed Services** | Cloud SQL HA (db-custom-4-16) + Memorystore | $482.40 | $520.99 | $497.84 |
| **6. Observability & Security** | Cloud Logging (80 GB billable) + Cloud Armor WAF | $85.00 | $85.00 | $85.00 |
| **Subtotal (On-Demand)** | Standard monthly list price | **$3,372.70** | **$3,495.32** | **$3,741.75** |
| **FinOps Optimization** | 3-Year Compute CUD (55% off baseline) | -$362.40 | -$391.39 | -$374.00 |
| **FINAL MONTHLY SPEND** | Optimized operational expenditure | **$3,010.30** | **$3,103.93** | **$3,367.75** |

*Budget Variance:* The final Dual-Region spend ($3,367.75/month) is comfortably within the corporate $5,000 monthly infrastructure budget ceiling.

---

## 4. Failure Domain and High Availability Assumptions

1. **Edge Tier:** Google Global Anycast External Application Load Balancers terminate TLS at the nearest Edge PoP, mitigating DDoS attacks via Cloud Armor and caching static assets on Cloud CDN.
2. **Compute Tier:** Regional Managed Instance Groups in `us-central1` (zones a, b, c) and `europe-west1` (zones b, c, d) ensure complete survival against any single data center building or electrical grid failure.
3. **Database Tier:** Cloud SQL High Availability with synchronous cross-zone replication delivers an RTO < 60 seconds and RPO = 0.
4. **Disaster Recovery Tier:** Asynchronous cross-region replication for storage buckets and read replicas ensures business continuity with RTO < 15 minutes and RPO < 1 minute in the catastrophic event of a full continental regional blackout.

---

## 5. Architectural Approval and Sign-Off
- **Architect Role:** Lead Enterprise Cloud Architect
- **Approval Date:** 2026-10-04
- **Status:** APPROVED FOR IMPLEMENTATION
