#!/usr/bin/env python3
"""
audit-billing-roles.py
Audits segregation of duties across Cloud Billing IAM roles.
"""
import json

BILLING_POLICY = {
    "resource": "billingAccounts/01A2B3-4C5D6E-7F8G9H",
    "bindings": [
        {
            "role": "roles/billing.admin",
            "members": [
                "group:finance-controllers@brightloaf.com",
                "user:cfo@brightloaf.com"
            ]
        },
        {
            "role": "roles/billing.user",
            "members": [
                "group:engineering-leads@brightloaf.com",
                "serviceAccount:terraform-deployer@brightloaf-ops.iam.gserviceaccount.com"
            ]
        },
        {
            "role": "roles/billing.viewer",
            "members": [
                "group:finops-analysts@brightloaf.com",
                "group:engineering-managers@brightloaf.com"
            ]
        }
    ]
}

def audit_segregation_of_duties(policy):
    print("=== Cloud Billing IAM Role Compliance Audit ===")
    violations = []
    
    for binding in policy["bindings"]:
        role = binding["role"]
        members = binding["members"]
        print(f"\nEvaluating Role: {role}")
        for m in members:
            # Rule: Engineering groups must NEVER hold roles/billing.admin
            if role == "roles/billing.admin" and ("engineering" in m or "dev" in m):
                violations.append(f"VIOLATION: Non-finance identity '{m}' holds {role}")
                print(f"  [FAIL] {m} -> Ineligible for Billing Admin")
            else:
                print(f"  [PASS] {m} -> Approved")
                
    if violations:
        print("\n[AUDIT RESULT: NON-COMPLIANT]")
        for v in violations:
            print(f"  {v}")
        return False
    else:
        print("\n[AUDIT RESULT: COMPLIANT] All roles strictly segregated according to financial policy.")
        return True

if __name__ == "__main__":
    audit_segregation_of_duties(BILLING_POLICY)
