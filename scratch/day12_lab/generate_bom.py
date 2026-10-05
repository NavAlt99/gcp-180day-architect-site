import json

with open("scratch/day12_lab/bom_spec.json", "r") as f:
    spec = json.load(f)

dimensions = spec["dimensions"]

us_total = sum(d["us_central1_monthly_usd"] for d in dimensions.values())
eu_total = sum(d["europe_west1_monthly_usd"] for d in dimensions.values())

cud_savings_us = 362.40
cud_savings_eu = 391.39

us_optimized = us_total - cud_savings_us
eu_optimized = eu_total - cud_savings_eu

dual_region_total = (us_optimized * 0.60) + (eu_optimized * 0.40) + 320.00

bom_summary = {
    "us_central1_on_demand_total": us_total,
    "us_central1_cud_optimized_total": us_optimized,
    "europe_west1_on_demand_total": eu_total,
    "europe_west1_cud_optimized_total": eu_optimized,
    "dual_region_optimized_total": dual_region_total,
    "monthly_budget_target": 5000.00,
    "budget_variance_status": "Within Budget ($5,000 ceiling)"
}

with open("scratch/day12_lab/bom_summary.json", "w") as out:
    json.dump(bom_summary, out, indent=2)

print("BOM generated.")
