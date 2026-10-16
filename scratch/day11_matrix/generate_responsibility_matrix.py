import json

with open("scratch/day11_matrix/tasks_taxonomy.json") as f:
    tasks = json.load(f)

matrix_rows = []
for t in tasks:
    tid = t["task_id"]
    name = t["task_name"]
    cat = t["category"]
    
    if tid == "TASK-OSP-01":
        vm_owner = "Google Cloud SRE"
        container_owner = "Google Cloud SRE"
        saas_owner = "Google Cloud SRE"
    elif tid == "TASK-OSP-02":
        vm_owner = "Customer DevOps / SysAdmin"
        container_owner = "Google Cloud SRE (Worker Nodes)"
        saas_owner = "Google Cloud SRE (Fully Abstracted)"
    elif tid == "TASK-SEC-01":
        vm_owner = "Customer SecOps / IAM Admin"
        container_owner = "Customer SecOps / IAM Admin"
        saas_owner = "Customer Workspace / Data Admin"
    elif tid == "TASK-SEC-02":
        vm_owner = "Customer App Engineering"
        container_owner = "Customer App Engineering"
        saas_owner = "Google Cloud SRE (Turnkey Software)"
    elif tid == "TASK-SEC-03":
        vm_owner = "Customer Network / Cloud Armor"
        container_owner = "Customer Network / Cloud Armor"
        saas_owner = "Google Cloud SRE (Front-End Mesh)"
    elif tid == "TASK-REC-01":
        vm_owner = "Google Cloud SRE (Persistent Disk)"
        container_owner = "Google Cloud SRE (Storage Mesh)"
        saas_owner = "Google Cloud SRE (Colossus Storage)"
    elif tid == "TASK-REC-02":
        vm_owner = "Customer SRE (Automated Snapshots)"
        container_owner = "Customer SRE (Volume / DB Backups)"
        saas_owner = "Customer Admin (Data Retention / Vault)"
    elif tid == "TASK-REC-03":
        vm_owner = "Customer Enterprise Architect"
        container_owner = "Customer Enterprise Architect"
        saas_owner = "Customer Enterprise Architect"
        
    matrix_rows.append({
        "task_id": tid,
        "category": cat,
        "task_name": name,
        "vm_owner": vm_owner,
        "container_owner": container_owner,
        "saas_owner": saas_owner
    })

with open("scratch/day11_matrix/responsibility_matrix.json", "w") as jf:
    json.dump(matrix_rows, jf, indent=2)

with open("scratch/day11_matrix/responsibility_matrix.md", "w") as mf:
    mf.write("# Cloud Shared Responsibility Matrix\n\n")
    mf.write("| Category | Task ID | Task Description | VM Example (Compute Engine) | Managed-Container Example (Cloud Run) | SaaS Example (Workspace / BigQuery) |\n")
    mf.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
    for r in matrix_rows:
        mf.write(f"| {r['category']} | {r['task_id']} | {r['task_name']} | **{r['vm_owner']}** | **{r['container_owner']}** | **{r['saas_owner']}** |\n")

print("Successfully generated responsibility_matrix.json and responsibility_matrix.md")
