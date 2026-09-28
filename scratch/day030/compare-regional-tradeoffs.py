#!/usr/bin/env python3
"""
Lab 30.1: Multi-Criteria Regional Trade-Off Evaluation & Org Policy Simulation
Compares candidate Google Cloud regions across latency, pricing, CFE%, hardware
availability, and compliance, then tests Organization Policy location enforcement.
"""

import sys
import json

REGIONAL_PROFILES = {
    "us-central1": {
        "name": "Iowa, USA",
        "zones": ["us-central1-a", "us-central1-b", "us-central1-c", "us-central1-f"],
        "zone_count": 4,
        "latency_midwest_ms": 15,
        "compute_cost_multiplier": 1.00,  # Tier 1 baseline
        "storage_cost_per_gb_month": 0.020,
        "carbon_cfe_pct": 64,
        "accelerator_availability": ["TPU v5p", "TPU v5e", "NVIDIA H100", "NVIDIA A100", "NVIDIA L4"],
        "compliance_domains": ["US-Commercial", "FedRAMP-High", "HIPAA"],
        "eu_gdpr_adequate": False,
        "eu_location_group": False,
    },
    "us-east4": {
        "name": "Northern Virginia, USA",
        "zones": ["us-east4-a", "us-east4-b", "us-east4-c"],
        "zone_count": 3,
        "latency_midwest_ms": 32,
        "compute_cost_multiplier": 1.08,  # Tier 2 (+8%)
        "storage_cost_per_gb_month": 0.023,
        "carbon_cfe_pct": 51,
        "accelerator_availability": ["NVIDIA A100", "NVIDIA L4", "NVIDIA T4"],
        "compliance_domains": ["US-Commercial", "FedRAMP-High", "HIPAA"],
        "eu_gdpr_adequate": False,
        "eu_location_group": False,
    },
    "europe-west3": {
        "name": "Frankfurt, Germany",
        "zones": ["europe-west3-a", "europe-west3-b", "europe-west3-c"],
        "zone_count": 3,
        "latency_midwest_ms": 105,
        "compute_cost_multiplier": 1.12,  # Tier 2 (+12%)
        "storage_cost_per_gb_month": 0.023,
        "carbon_cfe_pct": 76,
        "accelerator_availability": ["NVIDIA A100", "NVIDIA L4"],
        "compliance_domains": ["EU-GDPR", "German-BaFin", "BSI-C5"],
        "eu_gdpr_adequate": True,
        "eu_location_group": True,
    }
}

def compare_regions(primary="us-central1", secondary="europe-west3"):
    print("=" * 80)
    print("GOOGLE CLOUD MULTI-CRITERIA REGIONAL COMPARISON")
    print(f"Comparing Candidate A [{primary}] vs Candidate B [{secondary}]")
    print("=" * 80)

    p_data = REGIONAL_PROFILES[primary]
    s_data = REGIONAL_PROFILES[secondary]

    print(f"\n1. GEOGRAPHY & FAULT ISOLATION:")
    print(f"  • {primary} ({p_data['name']}): {p_data['zone_count']} zones ({', '.join(p_data['zones'])})")
    print(f"  • {secondary} ({s_data['name']}): {s_data['zone_count']} zones ({', '.join(s_data['zones'])})")

    print(f"\n2. CLIENT LATENCY TO MIDWEST US RETAIL HUBS:")
    print(f"  • {primary}: {p_data['latency_midwest_ms']} ms RTT (Optimal for US operations)")
    print(f"  • {secondary}: {s_data['latency_midwest_ms']} ms RTT (High transatlantic penalty)")

    print(f"\n3. COST DIFFERENTIAL (RELATIVE TO TIER 1 BASELINE):")
    print(f"  • {primary}: {p_data['compute_cost_multiplier']:.2f}x compute baseline | ${p_data['storage_cost_per_gb_month']:.3f}/GB-mo storage")
    print(f"  • {secondary}: {s_data['compute_cost_multiplier']:.2f}x compute baseline | ${s_data['storage_cost_per_gb_month']:.3f}/GB-mo storage")
    cost_diff = (s_data['compute_cost_multiplier'] - p_data['compute_cost_multiplier']) * 100
    print(f"  --> Variance: {secondary} is {cost_diff:+.1f}% vs {primary}")

    print(f"\n4. SUSTAINABILITY & CLEAN ENERGY:")
    print(f"  • {primary}: {p_data['carbon_cfe_pct']}% CFE (Carbon Free Energy)")
    print(f"  • {secondary}: {s_data['carbon_cfe_pct']}% CFE (Carbon Free Energy)")
    cfe_diff = s_data['carbon_cfe_pct'] - p_data['carbon_cfe_pct']
    print(f"  --> Carbon Advantage: {secondary} has {cfe_diff:+d}% higher CFE rating")

    print(f"\n5. COMPLIANCE & DATA SOVEREIGNTY:")
    print(f"  • {primary}: Domains: {', '.join(p_data['compliance_domains'])} | EU GDPR In-Country: {p_data['eu_gdpr_adequate']}")
    print(f"  • {secondary}: Domains: {', '.join(s_data['compliance_domains'])} | EU GDPR In-Country: {s_data['eu_gdpr_adequate']}")

    print("\n" + "=" * 80)

def simulate_org_policy_check(resource_type, requested_region, policy_allowed_groups):
    """
    Simulates Google Cloud Resource Locations Organization Policy enforcement
    (constraints/gcp.resourceLocations).
    """
    is_in_eu_group = REGIONAL_PROFILES.get(requested_region, {}).get("eu_location_group", False)

    allowed = False
    for rule in policy_allowed_groups:
        if rule == "in:europe-locations" and is_in_eu_group:
            allowed = True
            break
        elif rule == requested_region:
            allowed = True
            break

    return allowed

def run_policy_simulations():
    print("\nSIMULATING ORGANIZATION POLICY: constraints/gcp.resourceLocations")
    print("Folder: folders/58920194812 (Brightloaf European Expansion)")
    print("Enforced Rule: allowed_values = ['in:europe-locations']\n")

    test_cases = [
        ("Cloud SQL Instance", "us-east4", ["in:europe-locations"]),
        ("Cloud SQL Instance", "europe-west3", ["in:europe-locations"]),
        ("Cloud Storage Bucket", "us-central1", ["in:europe-locations"]),
        ("Compute Engine MIG", "europe-west3", ["in:europe-locations"]),
    ]

    for res, region, policy in test_cases:
        permitted = simulate_org_policy_check(res, region, policy)
        status = "PASSED (DEPLOYED)" if permitted else "BLOCKED (POLICY VIOLATION)"
        color_code = "\033[92m" if permitted else "\033[91m"
        reset_code = "\033[0m"
        print(f"  • Resource: {res:22} | Region: {region:14} -> {color_code}{status}{reset_code}")
        if not permitted:
            print(f"    ERROR 403: Constraint constraints/gcp.resourceLocations violated for location '{region}'.")

    print("\nPolicy evaluation completed with 100% deterministic guardrail verification.")

if __name__ == "__main__":
    compare_regions("us-central1", "europe-west3")
    compare_regions("us-central1", "us-east4")
    run_policy_simulations()
