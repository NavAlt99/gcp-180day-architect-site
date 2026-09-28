#!/usr/bin/env python3
"""
Lab 29.2: BigQuery Detailed Billing Export Query Simulator
Queries synthetic gcp_billing_export_resource_v1_* records, aggregates gross/credit/net spend,
and isolates orphaned high-cost resources by fully qualified resource URI.
"""

import json
import os
from datetime import datetime, timezone

def load_detailed_billing_records():
    """Generates synthetic BigQuery detailed billing export records."""
    return [
        {
            "billing_account_id": "01A2B3-4C5D6E-7F8G9H",
            "service": {"id": "6F81-5844-456A", "description": "Compute Engine"},
            "sku": {"id": "D264-16A5-420E", "description": "SSD Total Persistent Disk"},
            "usage_start_time": "2026-09-01T00:00:00Z",
            "usage_end_time": "2026-09-30T23:59:59Z",
            "project": {"id": "brightloaf-fulfillment-prod", "name": "Fulfillment Production"},
            "resource": {
                "name": "//compute.googleapis.com/projects/brightloaf-fulfillment-prod/zones/us-central1-b/disks/disk-pvc-88a2-orphan",
                "global_name": "projects/brightloaf-fulfillment-prod/zones/us-central1-b/disks/disk-pvc-88a2-orphan"
            },
            "location": {"region": "us-central1", "zone": "us-central1-b"},
            "cost": 3480.00,
            "currency": "USD",
            "credits": [],
            "status": "unattached"
        },
        {
            "billing_account_id": "01A2B3-4C5D6E-7F8G9H",
            "service": {"id": "6F81-5844-456A", "description": "Compute Engine"},
            "sku": {"id": "9B07-7FE3-8BA6", "description": "N2 Custom Instance Core running in Americas"},
            "usage_start_time": "2026-09-01T00:00:00Z",
            "usage_end_time": "2026-09-30T23:59:59Z",
            "project": {"id": "brightloaf-fulfillment-prod", "name": "Fulfillment Production"},
            "resource": {
                "name": "//compute.googleapis.com/projects/brightloaf-fulfillment-prod/zones/us-central1-a/instances/dispatch-worker-01",
                "global_name": "projects/brightloaf-fulfillment-prod/zones/us-central1-a/instances/dispatch-worker-01"
            },
            "location": {"region": "us-central1", "zone": "us-central1-a"},
            "cost": 2150.00,
            "currency": "USD",
            "credits": [{"name": "Committed Use Discount: CPU", "amount": -645.00}],
            "status": "active"
        },
        {
            "billing_account_id": "01A2B3-4C5D6E-7F8G9H",
            "service": {"id": "24E6-581D-38E5", "description": "BigQuery"},
            "sku": {"id": "2837-2E89-FE11", "description": "Analysis"},
            "usage_start_time": "2026-09-01T00:00:00Z",
            "usage_end_time": "2026-09-30T23:59:59Z",
            "project": {"id": "brightloaf-analytics-prod", "name": "Analytics Production"},
            "resource": {
                "name": "//bigquery.googleapis.com/projects/brightloaf-analytics-prod/queries/job-adhoc-geo-demand-spike",
                "global_name": "projects/brightloaf-analytics-prod/queries/job-adhoc-geo-demand-spike"
            },
            "location": {"region": "us-central1", "zone": None},
            "cost": 4200.00,
            "currency": "USD",
            "credits": [],
            "status": "completed"
        },
        {
            "billing_account_id": "01A2B3-4C5D6E-7F8G9H",
            "service": {"id": "A482-126A-8E40", "description": "Cloud Run"},
            "sku": {"id": "8431-7290-7F11", "description": "CPU Allocation Time"},
            "usage_start_time": "2026-09-01T00:00:00Z",
            "usage_end_time": "2026-09-30T23:59:59Z",
            "project": {"id": "brightloaf-order-prod", "name": "Order Intake Production"},
            "resource": {
                "name": "//run.googleapis.com/projects/brightloaf-order-prod/locations/us-central1/services/order-ingestion-api",
                "global_name": "projects/brightloaf-order-prod/locations/us-central1/services/order-ingestion-api"
            },
            "location": {"region": "us-central1", "zone": None},
            "cost": 1820.50,
            "currency": "USD",
            "credits": [{"name": "Free Tier Allowance", "amount": -20.50}],
            "status": "active"
        }
    ]

def execute_cost_query(records):
    """Simulates SQL GROUP BY project, service, sku, resource.name."""
    results = []
    for r in records:
        gross = r["cost"]
        credit_sum = sum(c["amount"] for c in r.get("credits", []))
        net = gross + credit_sum
        results.append({
            "project_id": r["project"]["id"],
            "service": r["service"]["description"],
            "sku": r["sku"]["description"],
            "resource_uri": r["resource"]["name"],
            "zone": r["location"]["zone"] or "regional",
            "gross_cost": gross,
            "credits": credit_sum,
            "net_cost": net,
            "status": r["status"]
        })
    return results

def main():
    print("================================================================================")
    print("  BRIGHTLOAF BIGQUERY DETAILED BILLING EXPORT SQL QUERY SIMULATOR              ")
    print("================================================================================")
    records = load_detailed_billing_records()
    results = execute_cost_query(records)

    total_gross = sum(row["gross_cost"] for row in results)
    total_credits = sum(row["credits"] for row in results)
    total_net = sum(row["net_cost"] for row in results)

    print(f"\n--- Resource-Level Cost Ledger ---")
    for r in results:
        print(f"Project:  {r['project_id']}")
        print(f"Service:  {r['service']:<16} | SKU: {r['sku']}")
        print(f"Resource: {r['resource_uri']}")
        print(f"Zone:     {r['zone']:<14} | Status: {r['status']}")
        print(f"Cost:     Gross: ${r['gross_cost']:>8,.2f} | Credits: ${r['credits']:>8,.2f} | Net: ${r['net_cost']:>8,.2f}")
        print("-" * 80)

    print(f"\nTOTAL ACCOUNT EXPENDITURE:")
    print(f"  Gross List Price:  ${total_gross:>10,.2f} USD")
    print(f"  Applied Credits:   ${total_credits:>10,.2f} USD")
    print(f"  Net Payable Cost:  ${total_net:>10,.2f} USD")

    os.makedirs("scratch/day029", exist_ok=True)
    out_file = "scratch/day029/cost-query-results.json"
    with open(out_file, "w") as f:
        json.dump({"summary": {"gross": total_gross, "credits": total_credits, "net": total_net}, "rows": results}, f, indent=2)
    print(f"\nQuery results saved to: {out_file}")

if __name__ == "__main__":
    main()
