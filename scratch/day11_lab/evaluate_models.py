import json

with open("scratch/day11_lab/workloads.json", "r") as f:
    workloads = json.load(f)

print("=" * 80)
print(f"{'WORKLOAD ID':<12} | {'WORKLOAD NAME':<28} | {'MODEL':<12} | {'GCP SERVICE':<18}")
print("=" * 80)

matrix = []
for w in workloads:
    w_id = w["workload_id"]
    name = w["name"]
    model = w["recommended_model"]
    svc = w["target_gcp_service"]
    print(f"{w_id:<12} | {name:<28} | {model:<12} | {svc:<18}")
    
    if model == "IaaS":
        patch_owner = "Customer DevOps"
        runtime_owner = "Customer DevOps"
        infra_owner = "Google SRE (Hypervisor + HW)"
    elif model in ("PaaS / CaaS", "FaaS"):
        patch_owner = "Google Cloud (Host OS)"
        runtime_owner = "Customer (Container / Code)"
        infra_owner = "Google SRE (Serverless Mesh)"
    else:
        patch_owner = "Google Cloud (Complete App)"
        runtime_owner = "Google Cloud (Managed Engine)"
        infra_owner = "Google SRE (Global Platform)"
        
    matrix.append({
        "workload_id": w_id,
        "name": name,
        "model": model,
        "service": svc,
        "os_patch_owner": patch_owner,
        "app_runtime_owner": runtime_owner,
        "infrastructure_owner": infra_owner
    })

with open("scratch/day11_lab/service_model_decision_matrix.json", "w") as out:
    json.dump(matrix, out, indent=2)

print("=" * 80)
print("Decision matrix written to service_model_decision_matrix.json successfully.")
