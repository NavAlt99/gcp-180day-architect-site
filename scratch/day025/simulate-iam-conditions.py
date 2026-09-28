#!/usr/bin/env python3
"""
simulate-iam-conditions.py - IAM Policy v3 & CEL Condition Evaluation Engine
Tests allowed and denied operations against temporal and resource-name conditions.
"""
from datetime import datetime, timezone
import json

# IAM Policy Document Schema Version 3
POLICY_V3 = {
    "version": 3,
    "etag": "BwZ1a2b3c4d=",
    "bindings": [
        {
            "role": "roles/clouddeploy.releaser",
            "members": ["serviceAccount:sa-deploy@brightloaf-prod.iam.gserviceaccount.com"],
            "condition": {
                "title": "emergency_maintenance_window",
                "description": "Permit release creation during emergency window in UTC",
                "expression": "request.time < timestamp('2026-09-28T04:00:00Z')"
            }
        },
        {
            "role": "roles/pubsub.publisher",
            "members": ["serviceAccount:order-ingest@brightloaf-prod.iam.gserviceaccount.com"],
            "condition": {
                "title": "prod_orders_topic_only",
                "description": "Restrict publishing to prod-orders topics only",
                "expression": "resource.name.startsWith('projects/_/topics/prod-orders')"
            }
        }
    ]
}

def evaluate_request(principal, role, req_time_iso, resource_name):
    req_time = datetime.fromisoformat(req_time_iso.replace("Z", "+00:00"))
    
    for binding in POLICY_V3["bindings"]:
        if binding["role"] == role and principal in binding["members"]:
            cond = binding.get("condition")
            if not cond:
                return True, "ALLOWED (Unconditional Binding)"
            
            expr = cond["expression"]
            # Evaluate temporal condition
            if "request.time < timestamp(" in expr:
                cutoff_str = expr.split("'")[1].replace("Z", "+00:00")
                cutoff_time = datetime.fromisoformat(cutoff_str)
                if req_time < cutoff_time:
                    return True, f"ALLOWED (Condition Passed: {cond['title']})"
                else:
                    return False, f"DENIED (Condition Expired: req_time={req_time_iso} >= cutoff={cutoff_str})"
            
            # Evaluate resource name prefix condition
            if "resource.name.startsWith(" in expr:
                prefix = expr.split("'")[1]
                if resource_name.startswith(prefix):
                    return True, f"ALLOWED (Condition Passed: prefix match '{prefix}')"
                else:
                    return False, f"DENIED (Condition Failed: '{resource_name}' does not start with '{prefix}')"
                    
    return False, "DENIED (No matching binding found)"

def run_test_suite():
    tests = [
        {
            "name": "Test 1: SRE Deployer during maintenance window (ALLOWED)",
            "principal": "serviceAccount:sa-deploy@brightloaf-prod.iam.gserviceaccount.com",
            "role": "roles/clouddeploy.releaser",
            "req_time": "2026-09-27T19:00:00Z",
            "resource": "projects/brightloaf-prod-fulfillment/deliveryPipelines/prod-pipe",
            "expect_allow": True
        },
        {
            "name": "Test 2: SRE Deployer after maintenance window expires (DENIED)",
            "principal": "serviceAccount:sa-deploy@brightloaf-prod.iam.gserviceaccount.com",
            "role": "roles/clouddeploy.releaser",
            "req_time": "2026-09-28T05:00:00Z",
            "resource": "projects/brightloaf-prod-fulfillment/deliveryPipelines/prod-pipe",
            "expect_allow": False
        },
        {
            "name": "Test 3: Ingestion SA publishing to authorized prod-orders topic (ALLOWED)",
            "principal": "serviceAccount:order-ingest@brightloaf-prod.iam.gserviceaccount.com",
            "role": "roles/pubsub.publisher",
            "req_time": "2026-09-27T12:00:00Z",
            "resource": "projects/_/topics/prod-orders-v1",
            "expect_allow": True
        },
        {
            "name": "Test 4: Ingestion SA publishing to unauthorized internal-audit topic (DENIED)",
            "principal": "serviceAccount:order-ingest@brightloaf-prod.iam.gserviceaccount.com",
            "role": "roles/pubsub.publisher",
            "req_time": "2026-09-27T12:00:00Z",
            "resource": "projects/_/topics/internal-audit-log",
            "expect_allow": False
        }
    ]

    print("=== Google Cloud IAM Policy v3 Condition Simulator ===")
    for t in tests:
        allowed, reason = evaluate_request(t["principal"], t["role"], t["req_time"], t["resource"])
        status = "PASS" if allowed == t["expect_allow"] else "FAIL"
        print(f"\n[{status}] {t['name']}")
        print(f"  Result: {'ALLOW' if allowed else 'DENY'}")
        print(f"  Reason: {reason}")
        assert allowed == t["expect_allow"], f"Test failed: expected {t['expect_allow']} got {allowed}"
    
    print("\n[ALL TEST SUITE SCENARIOS PASSED]")

if __name__ == "__main__":
    run_test_suite()
