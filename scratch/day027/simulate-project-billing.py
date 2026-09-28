#!/usr/bin/env python3
"""
simulate-project-billing.py
Simulates Cloud Billing project linkage and protection rules.
"""
import json

class CloudBillingManager:
    def __init__(self):
        self.billing_accounts = {
            "01A2B3-4C5D6E-7F8G9H": {"name": "Corporate Master Invoicing", "open": True}
        }
        self.projects = {
            "brightloaf-prod-fulfillment": {
                "billing_account": "01A2B3-4C5D6E-7F8G9H",
                "billing_enabled": True,
                "tags": {"env": "production"}
            },
            "brightloaf-dev-sandbox": {
                "billing_account": "01A2B3-4C5D6E-7F8G9H",
                "billing_enabled": True,
                "tags": {"env": "development"}
            }
        }

    def update_project_billing(self, project_id, new_billing_account, force=False):
        proj = self.projects.get(project_id)
        if not proj:
            raise ValueError(f"Project {project_id} not found.")

        # Safety Check: Prevent accidental unlinking of production projects
        if proj["tags"].get("env") == "production" and not new_billing_account and not force:
            raise PermissionError(
                f"SAFETY POLICY REJECTION: Cannot unlink billing from production project '{project_id}' without break-glass force flag."
            )

        proj["billing_account"] = new_billing_account
        proj["billing_enabled"] = bool(new_billing_account)
        return {
            "name": f"projects/{project_id}/billingInfo",
            "projectId": project_id,
            "billingAccountName": f"billingAccounts/{new_billing_account}" if new_billing_account else "",
            "billingEnabled": proj["billing_enabled"]
        }

def main():
    mgr = CloudBillingManager()
    print("=== Google Cloud Billing Linkage Simulator ===")
    
    # 1. Inspect initial state
    print("[1] Initial State for brightloaf-prod-fulfillment:")
    print(f"    Billing Enabled: {mgr.projects['brightloaf-prod-fulfillment']['billing_enabled']}")
    print(f"    Account        : {mgr.projects['brightloaf-prod-fulfillment']['billing_account']}")

    # 2. Test safe unlinking of dev project
    print("\n[2] Unlinking Dev Sandbox Project:")
    res_dev = mgr.update_project_billing("brightloaf-dev-sandbox", "")
    print(f"    Result: {res_dev['projectId']} -> billingEnabled={res_dev['billingEnabled']}")

    # 3. Test blocked unlinking of production project
    print("\n[3] Attempting Unprotected Unlink of Production Project:")
    try:
        mgr.update_project_billing("brightloaf-prod-fulfillment", "")
    except PermissionError as e:
        print(f"    [POLICY BLOCKED]: {e}")

    # Invariant assertion: Production fulfillment remains funded
    assert mgr.projects["brightloaf-prod-fulfillment"]["billing_enabled"], "CRITICAL: Prod billing disabled!"
    print("\n[INVARIANT VERIFIED]: Production fulfillment remains 100% funded and active.")

if __name__ == "__main__":
    main()
