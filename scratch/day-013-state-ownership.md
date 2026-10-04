# Day 13 Exit Evidence: State Ownership Architecture & Recovery Definitions

## Executive Summary
This document establishes the authoritative state ownership model, failure domain boundaries, and recovery vocabulary for OmniCommerce Enterprise. It delineates the architectural division between ephemeral stateless compute workers and durable state stores, defines High Availability, Fault Tolerance, RTO, and RPO with concrete Google Cloud examples, and documents why high-availability replication does not replace point-in-time recovery backups.

---

## 1. State Ownership Architecture Diagram

~~~text
+-----------------------------------------------------------------------------------+
|                            STATE OWNERSHIP ARCHITECTURE                           |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Client Browser ] ---> (Anycast BGP Edge PoP / Cloud Armor / Cloud CDN)        |
|                                         |                                         |
|                                         v (HTTPS Requests + Idempotency Tokens)   |
|  +-----------------------------------------------------------------------------+  |
|  | STATELESS WORKER TIER (Cloud Run / Regional MIG across Zones a, b, c)        |  |
|  | - Ephemeral, disposable worker containers; zero local disk state            |  |
|  | - Scales from 2 to 200 instances dynamically; crash-tolerant                |  |
|  +-----------------------------------------------------------------------------+  |
|               |                                              |                    |
|               | (Session Lookup / Cache)                     | (Committed Writes) |
|               v                                              v                    |
|  +---------------------------+              +----------------------------------+  |
|  | SESSION CACHE TIER        |              | AUTHORITATIVE DATA TIER          |  |
|  | Memorystore (Redis HA)    |              | Cloud SQL PostgreSQL (HA)        |  |
|  | - Shopping carts, sessions|              | - Primary (Zone a)               |  |
|  | - Volatile / Rebuildable  |              | - Synchronous Standby (Zone b)   |  |
|  | - RTO < 30s, RPO = volatile|             | - RTO < 60s, RPO = 0 (ACID)      |  |
|  +---------------------------+              +----------------------------------+  |
|                                                              |                    |
|                                                              | (Continuous WAL)   |
|                                                              v                    |
|                                             +----------------------------------+  |
|                                             | DISASTER RECOVERY VAULT          |  |
|                                             | Cloud Storage Dual-Region (nam4) |  |
|                                             | - Immutable Point-in-Time WAL    |  |
|                                             | - WORM Bucket Lock (30-day)      |  |
|                                             | - RTO < 2h, RPO < 1m (PITR)      |  |
|                                             +----------------------------------+  |
+-----------------------------------------------------------------------------------+
~~~

---

## 2. State Ownership Tier Matrix

| Architectural Tier | GCP Technology | State Classification | Durability Invariant | Failover & Scaling Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Edge Tier** | Cloud CDN / Cloud Armor | Stateless Perimeter | Zero State | Anycast BGP routing to nearest edge PoP |
| **Compute Tier** | Cloud Run / Regional MIG | Ephemeral Workers | Disposable | Sub-minute horizontal scaling; crash-tolerant |
| **Session Cache** | Memorystore (Redis HA) | Volatile Session State | Rebuildable | Dual-zone primary/standby failover (< 30s) |
| **Authoritative Data**| Cloud SQL PostgreSQL HA | Durable ACID State | Permanent | Synchronous zonal disk replication (RTO < 60s, RPO = 0) |
| **Recovery Vault** | Cloud Storage (nam4) | Immutable Historical State| WORM Locked | Dual-region Turbo Replication (RTO < 2h, RPO < 1m) |

---

## 3. Reliability & Recovery Vocabulary Definitions

### 1. High Availability (HA)
- **Definition:** System design ensuring operational uptime (99.9% to 99.99%) through automated redundancy across independent physical failure domains (zones), accepting brief, bounded failover pauses (seconds to minutes).
- **GCP Example:** Regional Managed Instance Groups in `us-central1` spanning zones a, b, and c paired with Cloud SQL HA synchronous standby replication (RTO < 60s, RPO = 0).

### 2. Fault Tolerance (FT)
- **Definition:** System design guaranteeing completely uninterrupted continuous operation with zero perceived downtime and zero data loss (RTO = 0, RPO = 0) despite underlying component failure.
- **GCP Example:** Cloud Spanner multi-region database utilizing distributed Paxos consensus and TrueTime atomic clocks to deliver five-nines (99.999%) availability with zero failover disruption.

### 3. Disaster Recovery (DR)
- **Definition:** The policies and technical capabilities required to reconstitute critical business functions and data following catastrophic regional disruptions.
- **GCP Example:** Asynchronous cross-region replication to `europe-west1` via Cloud Storage dual-region buckets and Cloud SQL Cross-Region Read Replicas (RTO < 2h, RPO < 15m).

### 4. Recovery Point Objective (RPO)
- **Definition:** The maximum acceptable duration of uncommitted or lost transaction data during an outage.
- **GCP Example:** Cloud SQL HA achieves RPO = 0 for single-zone failures via synchronous regional persistent disk commits; cross-region DR achieves RPO < 1 minute via streaming WAL shipping.

### 5. Recovery Time Objective (RTO)
- **Definition:** The maximum acceptable elapsed real time between failure occurrence and full operational service restoration.
- **GCP Example:** Stateless Cloud Run API achieves RTO < 10 seconds via load balancer rerouting; database Point-in-Time Recovery achieves RTO < 45 minutes for full 500 GB storage volume reconstitution.

---

## 4. The Critical Distinction: Available Replica vs Recoverable Backup

| Evaluation Dimension | Available Replica (HA / Read Replica) | Recoverable Backup (PITR Archive) |
| :--- | :--- | :--- |
| **Primary Architectural Purpose** | Live traffic serving, read offloading, node failover | Point-in-time state recovery, historical audit |
| **Data Synchronization** | Real-time streaming (Synchronous or Asynchronous) | Periodic snapshots + continuous immutable WAL |
| **Vulnerability to Logical Corruption**| **CRITICAL VULNERABILITY:** Replicates DROP/TRUNCATE immediately | **PROTECTED:** Isolated from live database mutations |
| **Recovery Time Objective (RTO)** | Seconds to minutes (Rapid promotion) | 30 minutes to 2 hours (Volume restore & replay) |
| **Recovery Point Objective (RPO)** | 0 to seconds (Near real-time) | < 1 minute (Granular second-level replay) |
| **Cost Profile** | Continuous compute + storage + replication egress | Economical object storage (Cloud Storage Nearline/Coldline) |

**Architectural Rule:** *"Replication protects against hardware failure; backups protect against human error and corruption."* Both mechanisms are mandatory in enterprise production architectures.

---

## 5. Architectural Approval and Sign-Off
- **Author Role:** Lead Enterprise Cloud Architect
- **Approval Date:** 2026-10-04
- **Verification Status:** VERIFIED AND APPROVED FOR IMPLEMENTATION
