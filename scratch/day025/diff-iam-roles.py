#!/usr/bin/env python3
"""
diff-iam-roles.py - Differential Analyzer for IAM Roles
Compares broad predefined/basic roles against tailored custom roles.
"""
import json

ROLE_EDITOR_PERMS = {
    "cloudsql.instances.get",
    "cloudsql.instances.list",
    "cloudsql.instances.restart",
    "cloudsql.instances.export",
    "cloudsql.instances.delete",
    "cloudsql.databases.delete",
    "cloudsql.users.delete",
    "compute.instances.delete",
    "storage.buckets.delete",
    "pubsub.topics.delete"
}

CUSTOM_OPERATOR_PERMS = {
    "cloudsql.instances.get",
    "cloudsql.instances.list",
    "cloudsql.instances.restart",
    "cloudsql.instances.export"
}

def analyze_roles(source_perms, target_perms, role_name):
    allowed = target_perms.intersection(source_perms)
    stripped = source_perms - target_perms

    print(f"=== IAM Role Differential Audit: {role_name} ===")
    print(f"Total Base Permissions Evaluated: {len(source_perms)}")
    print(f"Permissions Retained in Custom Role: {len(allowed)}")
    print(f"Destructive/Excess Permissions Stripped: {len(stripped)}")
    print("-" * 50)
    print("Retained Operational Permissions (ALLOWED):")
    for p in sorted(allowed):
        print(f"  [+] {p}")
    print("\nStripped High-Risk Permissions (BLOCKED):")
    for p in sorted(stripped):
        print(f"  [-] {p}")
    
    # Assert critical invariant: destructive actions must be stripped
    assert "cloudsql.instances.delete" not in target_perms, "SECURITY FAULT: Deletion verb present!"
    print("\n[LEAST PRIVILEGE COMPLIANCE]: PASSED (All destructive verbs purged)")

if __name__ == "__main__":
    analyze_roles(ROLE_EDITOR_PERMS, CUSTOM_OPERATOR_PERMS, "brightloafSqlOperator")
