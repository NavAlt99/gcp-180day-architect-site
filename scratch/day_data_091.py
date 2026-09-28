"""day_data_091.py — Exhaustive architecture data specification for Day 91.

Covers Backups and Replication Correctness:
1. Cold, warm, and hot DR sites in hybrid enterprise environments (BGP path prepending, HA VPN/Interconnect, identity sync).
2. Backup strategies: persistent disk snapshots, database Point-In-Time Recovery (PITR), object versioning, immutable WORM vaults.
3. Google Cloud Backup and DR Service (centralized SLA management, application-consistent agent capture, instant mount recovery).
4. Data replication mechanics: synchronous vs asynchronous replication, network speed-of-light boundaries, and RPO trade-offs.
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 91

DATA = {
    "day": 91,
    "part1_intro": (
        "Day 91 investigates the deep technical mechanics of state protection: backup architectures, point-in-time recovery, "
        "and physical data replication correctness. In disaster recovery, compute runtimes are commodity and ephemeral; data integrity "
        "is permanent and irreplaceable. Conflating backups with replication is a catastrophic architectural flaw: replication protects "
        "against localized hardware failure by mirroring state, but instantly mirrors software corruption, ransomware, and administrative "
        "accidents to all replicas. Backups create immutable point-in-time historical snapshots to reverse corruption, but incur non-zero RTO "
        "and RPO during restoration. Today's curriculum establishes hybrid DR connectivity across on-premises and Google Cloud, designs "
        "multi-tiered backup strategies (incorporating database Point-In-Time Recovery and WORM retention locks), explores Google Cloud "
        "Backup and DR Service for application-consistent centralized capture, and measures the immutable laws of physics distinguishing "
        "synchronous distributed consensus (RPO = 0) from asynchronous replication streams."
    ),
    "exit_summary": (
        "Engineered an enterprise data protection and recovery correctness framework: established hybrid cloud disaster recovery patterns "
        "over Dedicated Interconnect with BGP failover; configured multi-tier backup policies combining Cloud SQL Point-In-Time Recovery (PITR) "
        "and GCS WORM Object Retention Locks; evaluated Google Cloud Backup and DR Service for instant-mount database restoration; authored "
        "a comprehensive Recovery Point Report empirically comparing committed, replicated, and restored transactional state."
    ),
    "part2_intro": (
        "True data resilience requires layering continuous replication for availability alongside decoupled, immutable backups for survivability. "
        "The sections below analyze hybrid networking models, snapshot virtualization engines, and replication consistency constraints."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Protection Mechanism</th>
      <th>Replication / Capture Type</th>
      <th>Effective RPO Window</th>
      <th>Effective RTO Window</th>
      <th>Primary Threat Mitigated</th>
      <th>Inherent Limitation / Trade-Off</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Regional Persistent Disk</strong></td>
      <td>Synchronous block-level (Dual AZ)</td>
      <td><strong>RPO = 0</strong></td>
      <td><strong>&lt; 60 seconds</strong> (Zonal failover)</td>
      <td>Storage chassis or single-zone failure</td>
      <td>Confined to single region; mirrors filesystem corruption instantly</td>
    </tr>
    <tr>
      <td><strong>Cloud SQL PITR (WAL Archive)</strong></td>
      <td>Continuous write-ahead transaction log streaming</td>
      <td><strong>&lt; 1 second</strong> (Up to failure second)</td>
      <td><strong>30 – 120 minutes</strong> (Replay time)</td>
      <td>Accidental <code>DROP TABLE</code> or logical data corruption</td>
      <td>Restores to a new database instance; requires connection reconfiguration</td>
    </tr>
    <tr>
      <td><strong>Cross-Region Read Replica</strong></td>
      <td>Asynchronous database replication</td>
      <td><strong>Seconds to minutes</strong> (Byte lag)</td>
      <td><strong>5 – 15 minutes</strong> (Promotion)</td>
      <td>Total regional cloud facility disaster</td>
      <td>Non-zero RPO; un-replicated write-ahead logs lost upon primary destruction</td>
    </tr>
    <tr>
      <td><strong>Immutable GCS Retention (WORM)</strong></td>
      <td>Periodic object export with compliance lock</td>
      <td><strong>Scheduled interval</strong> (e.g. 4–24 hours)</td>
      <td><strong>Hours to days</strong> (Download &amp; re-index)</td>
      <td>Ransomware, rogue administrator, credential compromise</td>
      <td>Storage cannot be deleted or shortened under any circumstances until retention expires</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 91: Dual-Track Data Protection: Continuous Replication vs Immutable Backup",
        "desc": "Architectural separation between synchronous write replication for high availability and decoupled immutable snapshots for recovery.",
        "caption": "Figure 91.1: State protection architecture separating live low-latency replication from decoupled, tamper-proof archival backups.",
        "nodes": [
            ("1. Application Writes", "Synchronous Local Commit\\nBlock & Memory Ingress"),
            ("2. Live Replication", "Cross-Region Replica / Spanner\\nProtects Infrastructure Faults"),
            ("3. WAL / PITR Archival", "Continuous Log Streaming\\nProtects Logical Corruption"),
            ("4. Immutable Vault (WORM)", "Backup & DR Service / GCS Lock\\nProtects Ransomware & Deletion"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Cold, warm and hot DR sites in hybrid setups",
            "preview": (
                "An enterprise running an on-premises core banking system attempts failover to a warm Google Cloud DR site during a data center "
                "flood, but cross-site BGP routing routes return traffic back to the submerged data center due to asymmetric routing paths."
            ),
            "overview": (
                "Hybrid disaster recovery connects on-premises enterprise data centers with Google Cloud virtual private clouds (VPCs) "
                "to provide off-site survivability. In a **Cold Hybrid DR** configuration, minimal infrastructure is pre-provisioned in GCP; "
                "data backups are shipped across Cloud Interconnect or HA VPN into Cloud Storage, and compute is instantiated via Infrastructure "
                "as Code upon disaster declaration. In a **Warm Hybrid DR** setup, core network transit, directory authentication (Active Directory / "
                "Cloud Identity), and asynchronous database read replicas run continuously in GCP at reduced scale. In a **Hot Hybrid DR** "
                "architecture, both the on-premises facility and Google Cloud simultaneously process production workloads. The central engineering "
                "challenge in hybrid DR is managing BGP routing failover (utilizing Multi-Exit Discriminators [MED] and AS-Path prepending on Cloud Routers), "
                "preventing asymmetric traffic loops, and establishing secure hybrid identity synchronization."
            ),
            "technical": (
                "### 1. Hybrid Connectivity Architecture and BGP Routing Controls\n"
                "- **Dual Dedicated/Partner Interconnect:** High-availability hybrid setups require redundant 10Gbps or 100Gbps Cloud Interconnects "
                "terminating in separate metropolitan edge facilities (Metros) into redundant on-premises routers.\n"
                "- **BGP Route Steering via AS-Path Prepending and MED:** When on-premises is primary, Cloud Routers advertise GCP prefixes to "
                "on-premises with higher Multi-Exit Discriminator (MED) values or prepended Autonomous System (AS) hops, signaling that the on-premises "
                "path is preferred. Upon failover, on-premises BGP withdraws its primary routes or prepends its own AS-path 3 to 5 times, steering "
                "global traffic seamlessly to Google Cloud's Anycast ingress.\n"
                "- **Asymmetric Routing Hazards:** If ingress enters Google Cloud via Anycast ALB but egress traffic to corporate databases attempts "
                "to route over an uncoordinated secondary VPN tunnel, stateful firewalls drop packets. Equal-Cost Multi-Path (ECMP) must be coordinated "
                "with connection-tracking firewalls.\n\n"
                "### 2. Hybrid Identity and Secret Synchronization\n"
                "- **Active Directory Federation:** Identity must survive total on-premises datacenter loss. Deploy redundant Cloud Identity / Active "
                "Directory domain controllers on Compute Engine VMs in the cloud VPC, synchronizing continuously with on-premises primary DCs.\n"
                "- **Secret Synchronization:** Use Google Cloud Secret Manager replication to maintain secrets across hybrid boundaries, ensuring "
                "database credentials, TLS private keys, and API tokens match between on-premises and GCP runtimes."
            ),
            "questions": [
                "How does BGP Multi-Exit Discriminator (MED) steering coordinate traffic flow between on-premises primary and cloud secondary sites?",
                "What causes stateful firewall drops during asymmetric routing transitions in a hybrid DR failover?",
                "Why must Active Directory domain controllers be pre-deployed in the cloud VPC for warm hybrid disaster recovery?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/dr-scenarios#hybrid_scenarios",
            "reference_label": "Google Cloud Architecture: Hybrid disaster recovery architectures and networking topology",
            "scenario": {
                "symptom": (
                    "During a power transformer explosion at Brightloaf's primary on-premises distribution center, engineers triggered failover "
                    "to their warm standby environment in Google Cloud. While web servers launched and connected to cloud database replicas, "
                    "warehouse workers could not scan pallets because cloud application VMs were unable to authenticate users against the on-premises "
                    "Active Directory server that was offline in the dark datacenter."
                ),
                "constraints": (
                    "Must establish complete operational independence in the cloud DR environment, ensuring identity and network transit function without on-premises dependencies."
                ),
                "evidence": (
                    "Application logs showed hundreds of `Kerberos KDC unreachable` and `LDAP bind timeout: 10.100.4.15:389` errors. "
                    "All application servers in GCP were configured with hardcoded IP addresses of on-premises domain controllers."
                ),
                "diagnostic_steps": [
                    "Inspect application configuration files to identify dependencies on on-premises infrastructure IPs.",
                    "Verify Active Directory domain controller placement, replication status, and DNS SRV record resolution inside the GCP VPC.",
                    "Test hybrid network latency and routing reachability between GCP subnets and on-premises core services.",
                ],
                "root": (
                    "Incomplete hybrid DR architecture: the team replicated compute and database layers into GCP but failed to deploy redundant "
                    "Cloud Identity / Active Directory domain controllers inside the cloud VPC, leaving the cloud environment critically dependent "
                    "on the crashed on-premises facility."
                ),
                "fix": (
                    "Deploy two redundant Active Directory Domain Controllers on Compute Engine in `us-central1` across separate zones. Configure "
                    "continuous multi-master AD replication over Cloud Interconnect. Update cloud DHCP and application DNS configurations to query "
                    "local cloud domain controllers first."
                ),
                "verify": (
                    "Sever the hybrid Cloud Interconnect connection in staging; confirm that application VMs in GCP authenticate users, resolve Kerberos "
                    "tickets, and execute transactions with zero dependency on the on-premises network."
                ),
                "residual": (
                    "Password changes made on-premises while disconnected will require reconciliation upon network restoration."
                ),
                "diagram": (
                    "On-prem datacenter loses power",
                    "GCP warm standby boots VMs",
                    "Auth stalls: on-prem AD dead",
                    "Redundant AD DCs deployed in GCP",
                    "Autonomous cloud authentication"
                ),
                "facts": "Cloud warm standby failed because authentication servers existed solely in the on-premises facility that lost power.",
                "inference": "A disaster recovery environment is only as independent as its authentication and name resolution dependencies.",
                "expected": "Cloud DR site contains local domain controllers and services, enabling complete standalone operation during datacenter loss."
            },
            "lab": {
                "name": "Hybrid Cloud BGP Routing and Identity Autonomous Verification",
                "file": "day-091-topic-01-hybrid-dr.md",
                "goal": "Author a hybrid cloud disaster recovery runbook defining Cloud Router BGP failover policies and autonomous identity deployment.",
                "expected": "A comprehensive configuration guide detailing Cloud Router MED settings, BGP route advertisements, and AD domain controller topology.",
                "mode": "tabletop analysis & command synthesis",
                "prereq": "Understanding of BGP routing and Cloud Interconnect.",
                "preflight": "Review Cloud Router documentation on MED and AS-path prepending.",
                "steps": [
                    "Author the hybrid disaster recovery networking and identity runbook:\n\n```sh\ncat <<'EOF' > day-091-topic-01-hybrid-dr.md\n# Day 91: Hybrid Cloud DR Networking & Autonomous Identity Runbook\n\n## 1. Network Topology & BGP Steering\n- **Primary Facility:** On-Premises Equinix Ashburn (AS 65001)\n- **Secondary Recovery Site:** Google Cloud `us-east1` (AS 16550)\n- **Interconnect:** Dual 10G Dedicated Interconnects via Cloud Router\n\n## 2. Cloud Router BGP Failover Configuration\n\n### Step 1: Configure Cloud Router with Standby BGP Priority (High MED)\n```bash\n# Configure Cloud Router in us-east1\ngcloud compute routers create cr-hybrid-dr-east \\\n    --network=brightloaf-vpc \\\n    --region=us-east1 \\\n    --asn=16550\n\n# Configure BGP peer with high MED (1000 = lower priority than on-prem 100)\ngcloud compute routers add-bgp-peer cr-hybrid-dr-east \\\n    --region=us-east1 \\\n    --peer-name=onprem-peer-primary \\\n    --peer-asn=65001 \\\n    --interface=cr-vlan-east-1 \\\n    --advertised-route-priority=1000\n```\n\n### Step 2: Emergency Failover Activation (Lower MED / Active Priority)\n```bash\n# During declared disaster, elevate GCP route priority over BGP\ngcloud compute routers update-bgp-peer cr-hybrid-dr-east \\\n    --region=us-east1 \\\n    --peer-name=onprem-peer-primary \\\n    --advertised-route-priority=100\n```\n\n## 3. Autonomous Cloud Identity Deployment Architecture\nTo eliminate operational dependency on on-premises domain controllers:\n1. Deploy two `e2-standard-4` VMs in `us-east1-b` and `us-east1-c` running Windows Server 2022.\n2. Promote both instances to Active Directory Domain Controllers in forest `corp.brightloaf.com`.\n3. Configure Cloud DNS Private Zones to direct all cloud VPC DNS queries to local DC IPs (`10.10.1.10`, `10.10.2.10`).\n4. Establish continuous one-way / two-way AD directory synchronization.\nEOF\ncat day-091-topic-01-hybrid-dr.md\n```",
                    "Verify the configuration uses BGP route priority (MED) to coordinate primary and standby network paths.",
                    "Verify the identity architecture specifies redundant local domain controllers to avoid cross-premises authentication failures.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains valid gcloud Cloud Router BGP commands, and defines an autonomous hybrid identity design."
                ),
                "trouble": "Ensure Cloud Router ASN matches your Google Cloud BGP configuration and does not conflict with on-premises AS numbers.",
                "cleanup": "Retain `day-091-topic-01-hybrid-dr.md` as an exit evidence artifact.",
                "accept": "Completed hybrid DR architecture runbook with verified BGP steering and identity controls."
            }
        },
        {
            "key": "topic-02",
            "title": "Backup strategies",
            "preview": (
                "A compromised administrative service account deletes production Cloud SQL databases and backups, "
                "leaving the enterprise unable to recover because snapshots were stored in the same project without retention locks."
            ),
            "overview": (
                "An enterprise backup strategy is the final line of defense against catastrophic data loss, accidental operational deletion, "
                "and ransomware encryption. A comprehensive cloud backup architecture integrates multiple distinct primitives: "
                "**Compute Engine Persistent Disk Snapshots** (differential block captures stored across multi-region GCS buckets), "
                "**Database Point-In-Time Recovery (PITR)** (continuous write-ahead transaction log archiving enabling exact-second recovery), "
                "**Object Versioning and Soft Delete** (protecting object storage from accidental overwrites and malicious deletions), "
                "**Cross-Region Copy Policies** (hedging against regional storage facility destruction), and **Immutable Backups** "
                "(enforcing Write-Once-Read-Many [WORM] compliance locks that prevent deletion even by the Google Cloud Project Owner or Google Support)."
            ),
            "technical": (
                "### 1. Compute Engine Persistent Disk Snapshots\n"
                "- **Differential Mechanics:** The initial snapshot captures all allocated blocks on the disk; subsequent snapshots are strictly "
                "incremental, capturing only modified blocks. Snapshots can be stored in a single region or multi-region (e.g. `us` or `eu`).\n"
                "- **Instant Snapshots:** Provide near-instantaneous recovery (RTO in seconds) by capturing local disk metadata pointers in the same "
                "zone, ideal for pre-deployment safety checkpoints.\n"
                "- **Snapshot Schedules and Resource Policies:** Automate daily/hourly capture, set retention windows (e.g. keep daily for 14 days, "
                "weekly for 8 weeks), and specify target storage locations.\n\n"
                "### 2. Database Point-In-Time Recovery (PITR)\n"
                "- **How PITR Operates:** Cloud SQL and AlloyDB capture a daily automated base backup and continuously stream Write-Ahead Logs (WAL) "
                "or binary logs to Cloud Storage. To recover from a human error (such as an accidental `DELETE FROM users;` at 14:22:15), the administrator "
                "restores to timestamp `14:22:14`.\n"
                "- **Restoration Mechanics:** PITR always creates a *new* database instance; it never overwrites the existing instance in place. "
                "This ensures the compromised or damaged database remains preserved for post-incident forensic investigation.\n\n"
                "### 3. Object Versioning, Soft Delete, and Immutable WORM Locks\n"
                "- **Object Versioning:** Retains previous generations of Cloud Storage objects whenever overwritten or deleted. Pair with Lifecycle "
                "Rules to automatically expire noncurrent generations after 30 days.\n"
                "- **Soft Delete:** Retains deleted objects in a dormant state for a configurable retention window (default 7 days, up to 90 days), "
                "allowing emergency recovery without restoring from external backups.\n"
                "- **Bucket Lock & Retention Policies (WORM):** Implements regulatory compliance (SEC Rule 17a-4, FINRA). Once locked in "
                "`Compliance` mode, *no identity*—including the Super Admin or Google Support—can delete objects or shorten the retention period "
                "until the duration expires, neutralizing ransomware and insider threats."
            ),
            "questions": [
                "Why does restoring a database via Point-In-Time Recovery (PITR) always create a new database instance rather than overwriting in place?",
                "What is the difference in operational protection between Cloud Storage Soft Delete and Bucket Lock (WORM) retention?",
                "How do differential snapshot storage mechanics optimize both backup speed and monthly Cloud Storage expenditure?",
            ],
            "reference": "https://docs.cloud.google.com/backup-disaster-recovery/docs",
            "reference_label": "Google Cloud Backup and DR: Enterprise data protection policies, snapshot lifecycle, and WORM compliance",
            "scenario": {
                "symptom": (
                    "During a malicious insider attack, a rogue DevOps engineer utilized compromised credentials to execute an instance deletion operation "
                    "on Brightloaf's primary transactional database and immediately deleted all associated automated backups in the project. "
                    "The business was unable to process transactions for 3 days."
                ),
                "constraints": (
                    "Must establish tamper-proof, immutable backup retention that cannot be deleted or purged by compromised project-level credentials."
                ),
                "evidence": (
                    "Audit logs showed the caller used `roles/owner` on the project to delete the database and invoke the database backup deletion API. "
                    "Because automated backups were tied to the lifecycle of the instance, deleting the instance permanently purged all backups."
                ),
                "diagnostic_steps": [
                    "Inspect Cloud Audit Logs for `cloudsql.instances.delete` and `cloudsql.backupRuns.delete` operations to trace caller identity.",
                    "Review IAM role assignments and identify all service accounts and users possessing administrative delete permissions.",
                    "Audit backup storage locations and cross-project backup isolation configurations.",
                ],
                "root": (
                    "Single point of operational failure: database backups were co-located within the same project and administrative boundary "
                    "as the production workload, lacking cross-project isolation and immutable WORM retention locks."
                ),
                "fix": (
                    "Implement a dedicated, isolated 'Backup Vault Project' with restricted IAM access (no project owner role granted to DevOps). "
                    "Export daily database backups to a Cloud Storage bucket governed by a locked WORM Retention Policy (30-day compliance lock). "
                    "Enable Cloud Storage Soft Delete (14-day hold) across all backup buckets."
                ),
                "verify": (
                    "Attempt to execute an object deletion or bucket purge using a Project Owner service account in the staging backup vault; "
                    "confirm Google Cloud rejects the deletion with HTTP 403 BucketLockRetentionPolicyViolation."
                ),
                "residual": (
                    "WORM retention locked storage cannot be freed early; incorrect retention policies will incur non-refundable storage charges."
                ),
                "diagram": (
                    "Compromised admin deletes DB",
                    "Automated backups purged with DB",
                    "Total 3-day business outage",
                    "Isolated Backup Vault Project deployed",
                    "WORM lock blocks deletion attempts"
                ),
                "facts": "Project Owner deleted both Cloud SQL instance and backups because all assets shared a single IAM security boundary.",
                "inference": "Backups kept within the same IAM realm as production assets provide zero protection against credential compromise.",
                "expected": "Backups reside in an isolated project with WORM retention locks that reject all administrative deletion requests."
            },
            "lab": {
                "name": "Immutable Backup Vault and Cloud SQL PITR Restoration Runbook",
                "file": "day-091-topic-02-backup-vault.md",
                "goal": "Author and verify an immutable backup vault architecture with WORM retention locks and a Point-In-Time Recovery runbook.",
                "expected": "A comprehensive configuration guide with exact gcloud commands establishing retention locks and testing PITR restoration.",
                "mode": "tabletop analysis & command synthesis",
                "prereq": "Understanding of Cloud Storage security and database logging.",
                "preflight": "Review Cloud Storage bucket lock documentation and PITR command parameters.",
                "steps": [
                    "Author the backup vault architecture and PITR restoration runbook:\n\n```sh\ncat <<'EOF' > day-091-topic-02-backup-vault.md\n# Day 91: Immutable Backup Vault & Cloud SQL PITR Runbook\n\n## 1. Multi-Tier Backup Architecture Specification\n- **Primary Workload Project:** `brightloaf-prod`\n- **Dedicated Vault Project:** `brightloaf-backup-vault` (Strictly isolated IAM boundary)\n- **WORM Retention Policy:** 30 days mandatory compliance hold\n- **Point-In-Time Recovery:** Enabled on all production Cloud SQL instances with 7-day WAL retention\n\n## 2. Configuration & Execution Commands\n\n### Step 1: Create Isolated Immutable Storage Vault\n```bash\n# Create multi-region backup bucket in dedicated vault project\ngcloud storage buckets create gs://brightloaf-immutable-backups \\\n    --project=brightloaf-backup-vault \\\n    --location=US \\\n    --uniform-bucket-level-access\n\n# Set 30-day retention policy (WORM)\ngcloud storage buckets retention-policy set gs://brightloaf-immutable-backups \\\n    --retention-period=30d\n\n# Lock the retention policy into COMPLIANCE mode (Irreversible!)\ngcloud storage buckets retention-policy lock gs://brightloaf-immutable-backups\n```\n\n### Step 2: Configure Cloud SQL Point-In-Time Recovery\n```bash\n# Enable automated backups and continuous write-ahead binary logging\ngcloud sql instances patch brightloaf-db-primary \\\n    --project=brightloaf-prod \\\n    --backup-start-time=02:00 \\\n    --enable-bin-log \\\n    --enable-point-in-time-recovery\n```\n\n### Step 3: Execute Point-In-Time Recovery to Historical Timestamp\n```bash\n# Restore database to exact second prior to accidental data corruption\ngcloud sql instances clone brightloaf-db-primary brightloaf-db-restored \\\n    --project=brightloaf-prod \\\n    --point-in-time=\"2026-09-28T14:22:14.000Z\"\n\n# Confirm restored clone instance is RUNNABLE\ngcloud sql instances describe brightloaf-db-restored \\\n    --project=brightloaf-prod \\\n    --format='value(state)'\n```\n\n## 3. Tamper-Resistance Verification Drill\n```bash\n# Attempt to delete test object from locked vault (Must fail with 403)\ngcloud storage rm gs://brightloaf-immutable-backups/test-backup.tar.gz\n# Expected result: HTTP 403 Forbidden - Retention policy prevents object deletion\n```\nEOF\ncat day-091-topic-02-backup-vault.md\n```",
                    "Verify the commands specify the complete workflow: bucket creation -> WORM lock -> PITR clone.",
                    "Verify the runbook enforces cross-project isolation between production and the backup vault.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains valid gcloud storage lock and SQL clone commands, and specifies cross-project isolation."
                ),
                "trouble": "Never execute retention policy lock commands in a production environment without senior executive approval, as it cannot be undone.",
                "cleanup": "Retain `day-091-topic-02-backup-vault.md` as an exit evidence artifact.",
                "accept": "Completed backup vault specification with validated Point-In-Time Recovery commands."
            }
        },
        {
            "key": "topic-03",
            "title": "Backup and DR Service",
            "preview": (
                "An enterprise running mission-critical SAP HANA and Oracle databases on Google Cloud relies on custom shell scripts for backups, "
                "leading to silent snapshot corruption and an 18-hour restore window when scripts fail to quiesce the database engine."
            ),
            "overview": (
                "**Google Cloud Backup and DR Service** (formerly Actifio) provides a centralized, enterprise-grade management plane for data protection "
                "across heterogeneous hybrid workloads. Unlike basic snapshot scripts, Backup and DR Service is **application-consistent**: it deploys "
                "lightweight agents that communicate directly with underlying database engines (SAP HANA, Oracle, Microsoft SQL Server, PostgreSQL, MySQL) "
                "and hypervisors (VMware Engine, Compute Engine) to quiesce databases, flush memory buffers, and capture transaction-consistent states. "
                "Its revolutionary capability is **instant mount recovery**: instead of copying terabytes of data across the network (which takes hours), "
                "the service mounts a virtual disk directly from the snapshot pool to a target VM in under five minutes, achieving near-zero RTO for "
                "multi-terabyte enterprise databases."
            ),
            "technical": (
                "### 1. Architectural Components of Backup and DR Service\n"
                "- **Management Console:** A centralized SaaS control plane hosted in Google Cloud for defining global SLA policies, role-based "
                "access control (RBAC), and compliance reporting.\n"
                "- **Backup/Recovery Appliances (BPA):** Dedicated virtual appliances deployed in specific regions and VPCs that orchestrate local "
                "snapshot ingestion, deduplication, and lifecycle management.\n"
                "- **Application-Aware Agents:** Installed on guest VMs (Linux/Windows) to coordinate with database APIs (e.g. Oracle VSS/RMAN, "
                "SAP HANA hdbsql) to trigger write-quiescing and log truncation prior to snapshot capture.\n\n"
                "### 2. 'Incremental Forever' and Storage Virtualization\n"
                "- **Incremental Forever Capture:** After an initial baseline ingestion, only modified blocks are ever transferred over the network, "
                "minimizing CPU, network, and storage consumption.\n"
                "- **Snapshot Pool Virtualization:** Snapshots are synthesized into full virtual disk images. When an administrator requests a restore, "
                "the service exposes the virtual disk as an iSCSI or NFS mount to the target VM. The database boots instantly from the mount without "
                "waiting for physical data movement.\n\n"
                "### 3. Backup Vaults and Immutable Protection\n"
                "- **Air-Gapped Backup Vaults:** Backup data can be stored in Google-managed or customer-managed Backup Vaults isolated in dedicated "
                "projects, immune to ransomware infections on the host compute tier.\n"
                "- **Granular SLA Profiles:** Define unified policies: e.g., Gold SLA = snapshot every 4 hours, retain for 14 days, replicate to "
                "secondary region every 12 hours, archive to cold vault monthly for 7 years."
            ),
            "questions": [
                "How does application-consistent quiescing prevent database corruption during snapshot capture compared to crash-consistent disk snapshots?",
                "What is the mechanical difference between instant-mount recovery and traditional physical data restoration?",
                "Why does the 'incremental forever' architecture reduce cross-region data transfer egress costs?",
            ],
            "reference": "https://docs.cloud.google.com/backup-disaster-recovery/docs/concepts/overview",
            "reference_label": "Google Cloud Backup and DR Service: Enterprise architecture, SLA profiles, and instant mount recovery",
            "scenario": {
                "symptom": (
                    "During a quarterly disaster recovery audit, Brightloaf's SAP HANA ERP database failed its restoration drill. "
                    "The restored database instance failed to start, throwing `corruption in redo log segment 0x4F8A` because the automated "
                    "snapshot script took a standard Compute Engine disk snapshot while high-volume transactions were actively writing in memory."
                ),
                "constraints": (
                    "Must achieve application-consistent database snapshots without halting production transactions, and reduce restoration RTO to under 15 minutes."
                ),
                "evidence": (
                    "Database diagnostic logs revealed that uncommitted in-flight memory transactions were lost during the crash-consistent snapshot. "
                    "The standard snapshot captured disk blocks out of sync with memory buffers, causing database engine startup failure."
                ),
                "diagnostic_steps": [
                    "Inspect database engine error logs during boot to locate corrupted block offsets and transaction sequence numbers.",
                    "Review existing backup cron scripts to verify if `hdbsql` quiesce commands were issued prior to snapshot triggering.",
                    "Measure historical restoration time for a 4TB database using standard disk snapshot restoration.",
                ],
                "root": (
                    "Architectural flaw: the engineering team used crash-consistent disk snapshots instead of application-consistent database backups. "
                    "Without quiescing the database engine, the snapshot captured a corrupted state."
                ),
                "fix": (
                    "Deploy Google Cloud Backup and DR Service. Install the application-aware agent on the SAP HANA instance, configure a Gold SLA "
                    "profile orchestrating automated database quiescing and log backup, and implement instant mount recovery for disaster drills."
                ),
                "verify": (
                    "Execute an automated disaster recovery drill using Backup and DR Service; verify the 4TB database mounts to a standby VM in "
                    "4 minutes and 12 seconds with zero corrupted log segments, passing complete database consistency checks."
                ),
                "residual": (
                    "Backup and DR Service appliances require dedicated virtual machine compute and storage overhead in the management VPC."
                ),
                "diagram": (
                    "Crash-consistent snapshot taken",
                    "Redo log corrupted during write",
                    "SAP HANA fails to boot in drill",
                    "Backup & DR Service deployed",
                    "App-consistent instant mount in 4m"
                ),
                "facts": "4TB database failed recovery because raw disk snapshots captured in-flight writes without quiescing database memory buffers.",
                "inference": "Crash-consistent snapshots are insufficient for enterprise relational databases; application consistency is mandatory.",
                "expected": "Backup and DR Service coordinates with database engines to capture clean, instantly mountable recovery images."
            },
            "lab": {
                "name": "Backup and DR Service Architecture & SLA Profile Design",
                "file": "day-091-topic-03-backup-dr-service.md",
                "goal": "Author an enterprise data protection specification establishing Backup and DR Service appliances, SLA policies, and instant mount runbooks.",
                "expected": "A comprehensive architectural guide detailing agent configuration, SLA policy rules, and mount-based recovery steps.",
                "mode": "tabletop analysis & policy synthesis",
                "prereq": "Understanding of relational database architecture and storage virtualization.",
                "preflight": "Review Google Cloud Backup and DR documentation on appliance deployment and SLA rules.",
                "steps": [
                    "Author the Backup and DR Service architecture and SLA policy document:\n\n```sh\ncat <<'EOF' > day-091-topic-03-backup-dr-service.md\n# Day 91: Backup and DR Service Architecture & SLA Policy Framework\n\n## 1. Enterprise Architecture Deployment\n- **Management Console:** Google-managed multi-tenant SaaS control plane\n- **Backup/Recovery Appliance (BPA):** Deployed in `mgmt-vpc-us-central1`\n- **Target Workloads:** Oracle Database, PostgreSQL, SAP HANA, GCE Compute VMs\n- **Storage Vault:** Customer-Managed Backup Vault in project `brightloaf-vault`\n\n## 2. Standardized SLA Profiles Matrix\n\n| SLA Tier | Target Workloads | Snapshot Frequency | Local Retention | Cross-Region Replication | Cold Archive Retention |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n| **Platinum** | Core SAP HANA, Oracle Financials | Every 2 Hours | 14 Days | Continuous (to `us-east1`) | 7 Years (WORM Vault) |\n| **Gold** | E-commerce DBs, Customer Auth | Every 4 Hours | 14 Days | Daily (to `us-east1`) | 1 Year |\n| **Silver** | Batch Analytics, Staging DBs | Daily at 01:00 | 7 Days | None | None |\n| **Bronze** | Stateless App VM Disks | Weekly | 14 Days | None | None |\n\n## 3. Instant Mount Recovery Runbook\n\n### Step 1: Query Available Application-Consistent Recovery Points\n```bash\n# List consistent application recovery snapshots via API\ngcloud backup-dr backup-vaults list \\\n    --location=us-central1 \\\n    --project=brightloaf-vault\n```\n\n### Step 2: Trigger Instant Mount to Target Recovery VM\n```bash\n# Present virtual disk snapshot directly to target compute instance via iSCSI\ngcloud backup-dr restore instant-mount \\\n    --workload-id=\"sap-hana-prod\" \\\n    --snapshot-id=\"snap-20260928-1200\" \\\n    --target-instance=\"sap-hana-recovery-node\" \\\n    --region=us-central1\n```\n\n### Step 3: Verify Database Mount & Integrity\n```bash\n# Confirm filesystem is mounted and database engine boots cleanly\ngcloud compute ssh sap-hana-recovery-node --command=\"df -h /hana/data && hdbuserstore list\"\n```\nEOF\ncat day-091-topic-03-backup-dr-service.md\n```",
                    "Verify the SLA profile matrix defines clear retention tiers and replication frequencies.",
                    "Verify the instant mount runbook contrasts virtual disk mounting against physical network data copies.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains a structured SLA profile matrix, and details an instant mount recovery procedure."
                ),
                "trouble": "Ensure network firewall rules allow TCP ports 5106 and 3260 between the Backup Appliance and target database hosts.",
                "cleanup": "Retain `day-091-topic-03-backup-dr-service.md` as an exit evidence artifact.",
                "accept": "Completed Backup and DR Service architecture guide with validated SLA tiers and mount workflows."
            }
        },
        {
            "key": "topic-04",
            "title": "Data replication",
            "preview": (
                "An architect promises executive stakeholders an RPO of zero across continents using asynchronous database read replicas, "
                "leading to a crisis when a trans-Atlantic fiber cut forces a failover that permanently loses 4 minutes of customer orders."
            ),
            "overview": (
                "Data replication is the ongoing process of copying data between multiple distinct storage devices, zones, or regions. "
                "The fundamental architectural choice is between **synchronous replication** and **asynchronous replication**, a decision governed "
                "by the immutable laws of physics and network latency. In synchronous replication, a write transaction is not confirmed to the "
                "client until it has been committed and acknowledged by secondary storage nodes, guaranteeing **RPO = 0** at the cost of higher "
                "write latency. In asynchronous replication, writes are confirmed immediately upon local commit, and data is transferred to secondary "
                "replicas out of band; this optimizes write performance but guarantees an **RPO > 0** equal to the replication lag. Architects must "
                "empirically measure committed versus replicated records to construct an accurate Recovery Point Report."
            ),
            "technical": (
                "### 1. Synchronous Replication Mechanics and Latency Trade-Offs\n"
                "- **Regional Persistent Disk (Regional PD):** Synchronously mirrors disk blocks across two zones within the same region. Every write "
                "operation issues two parallel network writes; the primary kernel waits for both acknowledgments before returning success to the caller. "
                "Round-trip latency overhead is typically 1 to 2 milliseconds. Guarantees RPO = 0 during zonal collapse.\n"
                "- **Cloud Spanner Multi-Region Paxos:** Uses Google's proprietary TrueTime atomic clocks and distributed Paxos consensus. Write transactions "
                "require a majority quorum of voting replicas (e.g. 2 out of 3 voting zones across multiple regions). Delivers global external consistency "
                "and RPO = 0 across regions, with write latency governed by the speed of light between regions (typically 30–60ms).\n\n"
                "### 2. Asynchronous Replication and Replication Lag (RPO > 0)\n"
                "- **Cross-Region Database Replicas (Cloud SQL / AlloyDB):** The primary commits transactions to its local Write-Ahead Log (WAL) and "
                "immediately returns success. An asynchronous replication stream transmits WAL records to the secondary region. Under heavy write loads "
                "or network congestion, **replication lag** accumulates.\n"
                "- **The RPO Breach Scenario:** If the primary region collapses while replication lag is 12 seconds, all transactions committed "
                "in those 12 seconds are permanently orphaned upon failover promotion. The business experiences an RPO of 12 seconds.\n\n"
                "### 3. Asynchronous Object and File Replication\n"
                "- **Cloud Storage Dual-Region & Turbo Replication:** Standard dual-region buckets replicate objects asynchronously with a 99.9% "
                "SLA to replicate 100% of objects within 12 hours. Turbo Replication provides a 100% SLA to replicate 100% of objects across regions "
                "in under **15 minutes**, reducing object storage RPO to 15 minutes."
            ),
            "questions": [
                "Why is it mathematically impossible to achieve an RPO of zero with asynchronous cross-region replication during an unannounced primary crash?",
                "How does Cloud Spanner utilize TrueTime to achieve external consistency without two-phase commit locking across reads?",
                "Under what operational conditions does Cloud Storage Turbo Replication justify its additional premium replication cost?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/dr-scenarios#data_replication",
            "reference_label": "Google Cloud Architecture: Data replication strategies, synchronous vs asynchronous trade-offs",
            "scenario": {
                "symptom": (
                    "During a regional network outage in `us-central1`, Brightloaf promoted a cross-region Cloud SQL read replica in `us-east1`. "
                    "When normal operations resumed, customer support received 418 complaints from shoppers whose credit cards were charged "
                    "but whose order confirmations vanished from the database."
                ),
                "constraints": (
                    "Must audit and report the exact data delta between committed, replicated, and restored records to quantify true operational RPO."
                ),
                "evidence": (
                    "Database log telemetry revealed that replication lag spiked to 28 seconds immediately before the primary region network severed. "
                    "Promoting the replica orphaned 418 transactions that existed on the primary disk but had not yet arrived at the replica."
                ),
                "diagnostic_steps": [
                    "Extract the last committed transaction ID on the primary database WAL logs.",
                    "Extract the last applied transaction ID on the promoted secondary database.",
                    "Calculate the missing transaction set: `Missing = Committed_{primary} - Applied_{replica}`.",
                ],
                "root": (
                    "Misunderstanding of replication boundaries: leadership assumed cross-region replicas provided zero data loss, failing to account "
                    "for the 28-second asynchronous replication lag during emergency replica promotion."
                ),
                "fix": (
                    "Produce an authoritative Recovery Point Report distinguishing synchronous layers (Regional PD / Spanner) from asynchronous replicas. "
                    "For order checkout, migrate transactional tables to Cloud Spanner (guaranteeing RPO = 0 across regions) or implement an asynchronous "
                    "reconciliation queue in Cloud Pub/Sub that replays missing orders upon primary recovery."
                ),
                "verify": (
                    "Run an automated data loss simulation in staging: issue continuous writes while severing network to replica; verify telemetry "
                    "accurately calculates byte lag, transaction delta, and exact data loss duration."
                ),
                "residual": (
                    "Migrating from Cloud SQL to Cloud Spanner requires application refactoring to eliminate foreign key constraints and handle distributed query planning."
                ),
                "diagram": (
                    "418 writes committed locally",
                    "Async lag: 28 seconds",
                    "Primary severed; replica promoted",
                    "Spanner multi-region Paxos adopted",
                    "Synchronous writes: RPO = 0"
                ),
                "facts": "418 transactions were lost during failover because Cloud SQL cross-region replication is asynchronous with a 28s lag.",
                "inference": "Asynchronous replication trades data loss (RPO > 0) for low write latency; it cannot guarantee zero data loss.",
                "expected": "Mission-critical ledgers deploy synchronous consensus (Spanner) while secondary services accept bounded asynchronous RPO."
            },
            "lab": {
                "name": "Recovery-Point Report & Replication Audit Experiment",
                "file": "day-091-topic-04-rpo-report.md",
                "goal": "Author a comprehensive Recovery-Point Report distinguishing synchronous from asynchronous replication and verifying data consistency.",
                "expected": "A detailed analytical report and Python verification script comparing committed, replicated, and restored transaction counts.",
                "mode": "tabletop analysis & script synthesis",
                "prereq": "Completion of Exercises 1, 2, and 3.",
                "preflight": "Review database transaction log formats and replication telemetry metrics.",
                "steps": [
                    "Author the Recovery-Point Report and data auditing simulation:\n\n```sh\ncat <<'EOF' > day-091-topic-04-rpo-report.md\n# Day 91: Recovery-Point Report: Replication vs Backup Retention\n\n## 1. Executive Summary & Architectural Findings\nThis report audits the state protection posture of Brightloaf's transactional retail platform. Empirical analysis confirms that asynchronous cross-region replication inherently permits transactional loss during unannounced regional failures. To satisfy executive compliance mandates, we establish explicit RPO boundaries across storage layers.\n\n## 2. Replication Mechanism Comparison Matrix\n\n| Storage Layer | Technology Used | Replication Type | Observed Latency Overhead | Observed Failover RPO | Loss Risk during Hard Crash |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n| **Zonal Compute Disks** | Regional Persistent Disk | Synchronous (Dual-AZ) | +1.2 ms | **RPO = 0** | Zero data loss within region |\n| **Global Database** | Cloud Spanner Multi-Region | Synchronous (Multi-Region Paxos) | +38.5 ms | **RPO = 0** | Zero data loss globally |\n| **Relational Database** | Cloud SQL Cross-Region | Asynchronous (WAL Stream) | +0.0 ms | **RPO = 15 – 45 seconds** | High (Unapplied WALs lost) |\n| **Object Storage** | GCS Dual-Region (Standard) | Asynchronous Object Sync | +0.0 ms | **RPO < 12 Hours** | Moderate (Recent uploads delayed) |\n| **Object Storage Turbo** | GCS Turbo Replication | Asynchronous Fast Sync | +0.0 ms | **RPO < 15 Minutes** | Low (99.9% replicated in <15m) |\n| **Backup Retention** | GCS WORM Vault Archive | Scheduled Export (Daily) | None (Out of band) | **RPO = 24 Hours** | Predictable (State as of 02:00) |\n\n## 3. Synthetic Transaction Reconciliation Audit Script\n```python\n# Audit script to reconcile committed vs replicated vs restored records\nimport time\n\ncommitted_records = [\n    {\"id\": 1001, \"user\": \"alice\", \"amount\": 45.00, \"time\": \"14:22:01\"},\n    {\"id\": 1002, \"user\": \"bob\", \"amount\": 120.50, \"time\": \"14:22:08\"},\n    {\"id\": 1003, \"user\": \"charlie\", \"amount\": 18.25, \"time\": \"14:22:15\"},\n    {\"id\": 1004, \"user\": \"dana\", \"amount\": 99.00, \"time\": \"14:22:25\"}, # In flight\n    {\"id\": 1005, \"user\": \"evan\", \"amount\": 210.00, \"time\": \"14:22:28\"}, # In flight\n]\n\n# Asynchronous replica state at time of primary failure (14:22:20)\nreplicated_records = committed_records[:3]\n\n# Backup restored from nightly snapshot (02:00:00)\nrestored_backup_records = [] # Empty baseline before morning transactions\n\nprint(\"=== RECOVERY POINT AUDIT REPORT ===\")\nprint(f\"Total Committed Transactions: {len(committed_records)}\")\nprint(f\"Total Replicated in Secondary: {len(replicated_records)}\")\nprint(f\"Orphaned Un-Replicated Records: {len(committed_records) - len(replicated_records)}\")\n\nlost_ids = [r['id'] for r in committed_records if r not in replicated_records]\nprint(f\"Lost Transaction IDs (RPO Breach): {lost_ids}\")\nprint(f\"Calculated RPO Gap: 8 seconds (from 14:22:20 to 14:22:28)\")\nEOF\npython3 -c \"with open('day-091-topic-04-rpo-report.md') as f: print('Report created successfully, length:', len(f.read()))\"\n```",
                    "Verify the Recovery-Point Report clearly distinguishes synchronous from asynchronous replication across all storage technologies.",
                    "Verify the reconciliation script demonstrates the exact mechanism of orphaned records during asynchronous failover.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains a structured replication comparison matrix, and includes a working data loss calculation script."
                ),
                "trouble": "Ensure the reconciliation calculation properly identifies missing transaction records based on timestamp gaps.",
                "cleanup": "Retain `day-091-topic-04-rpo-report.md` as an exit evidence artifact.",
                "accept": "Completed Recovery-Point Report with verified replication and backup audit data."
            }
        }
    ]
}
