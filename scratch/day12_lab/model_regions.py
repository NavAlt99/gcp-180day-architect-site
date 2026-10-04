import json

with open("scratch/day12_lab/workload_spec.json", "r") as f:
    spec = json.load(f)

results = []
for region_name, rdata in spec["regions"].items():
    weighted_latency = (
        spec["na_users_percent"] * rdata["na_latency_ms"] +
        spec["eu_users_percent"] * rdata["eu_latency_ms"]
    ) / 100.0
    
    compliance = "Compliant" if rdata["gdpr_compliant"] else "Non-Compliant (Requires EU boundary)"
    failure_domain = f"Regional Multi-Zone ({len(rdata['zones'])} zones)"
    
    results.append({
        "region": region_name,
        "location": rdata["location"],
        "zones_count": len(rdata["zones"]),
        "weighted_latency_ms": weighted_latency,
        "na_latency_ms": rdata["na_latency_ms"],
        "eu_latency_ms": rdata["eu_latency_ms"],
        "gdpr_status": compliance,
        "cost_multiplier": rdata["compute_cost_index"],
        "failure_domain": failure_domain
    })

output = {
    "workload": spec["workload_name"],
    "evaluation": results,
    "architectural_recommendation": {
        "strategy": "Dual-Region Hybrid Deployment",
        "frontend": "Global Anycast External Application Load Balancer",
        "na_hub": "us-central1 (60% traffic, optimal compute cost)",
        "eu_hub": "europe-west1 (40% traffic, strictly GDPR compliant)",
        "resiliency": "Survives complete single-region catastrophic failure with automated traffic failover"
    }
}

with open("scratch/day12_lab/regional_location_comparison.json", "w") as out:
    json.dump(output, out, indent=2)

print("Regional comparison generated.")
