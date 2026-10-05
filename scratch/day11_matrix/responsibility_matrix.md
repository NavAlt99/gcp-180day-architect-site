# Cloud Shared Responsibility Matrix

| Category | Task ID | Task Description | VM Example (Compute Engine) | Managed-Container Example (Cloud Run) | SaaS Example (Workspace / BigQuery) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| OS Patching | TASK-OSP-01 | Physical Host OS & Hypervisor Patching | **Google Cloud SRE** | **Google Cloud SRE** | **Google Cloud SRE** |
| OS Patching | TASK-OSP-02 | Guest Operating System Kernel & Package Updates | **Customer DevOps / SysAdmin** | **Google Cloud SRE (Worker Nodes)** | **Google Cloud SRE (Fully Abstracted)** |
| Application Security | TASK-SEC-01 | IAM Authentication & Role Governance | **Customer SecOps / IAM Admin** | **Customer SecOps / IAM Admin** | **Customer Workspace / Data Admin** |
| Application Security | TASK-SEC-02 | Application Vulnerability & Dependency Scanning | **Customer App Engineering** | **Customer App Engineering** | **Google Cloud SRE (Turnkey Software)** |
| Application Security | TASK-SEC-03 | Network Ingress Filtering & WAF Protection | **Customer Network / Cloud Armor** | **Customer Network / Cloud Armor** | **Google Cloud SRE (Front-End Mesh)** |
| Data Recovery | TASK-REC-01 | Physical Storage Array Bit-Rot & Media Durability | **Google Cloud SRE (Persistent Disk)** | **Google Cloud SRE (Storage Mesh)** | **Google Cloud SRE (Colossus Storage)** |
| Data Recovery | TASK-REC-02 | Logical Backup Schedules & Point-in-Time Recovery | **Customer SRE (Automated Snapshots)** | **Customer SRE (Volume / DB Backups)** | **Customer Admin (Data Retention / Vault)** |
| Data Recovery | TASK-REC-03 | Disaster Recovery Drill & Cross-Region Failover | **Customer Enterprise Architect** | **Customer Enterprise Architect** | **Customer Enterprise Architect** |
