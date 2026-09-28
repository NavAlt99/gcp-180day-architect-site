#!/usr/bin/env python3
"""
impersonate-sa.py - Service Account Impersonation Simulator
Demonstrates ephemeral token minting and dual-principal audit logging.
"""
from datetime import datetime, timezone, timedelta
import secrets
import json

class IAMCredentialsService:
    def __init__(self):
        # Service Account IAM Policies (Who can impersonate)
        self.sa_policies = {
            "sa-fulfillment-worker@brightloaf-prod-orders.iam.gserviceaccount.com": {
                "token_creators": [
                    "user:sre-lead@brightloaf.com",
                    "serviceAccount:ci-runner@brightloaf-ops.iam.gserviceaccount.com"
                ]
            }
        }

    def generate_access_token(self, caller_principal, target_sa, scopes, lifetime_seconds=3600):
        policy = self.sa_policies.get(target_sa)
        if not policy:
            raise PermissionError(f"Target service account {target_sa} does not exist.")
        
        if caller_principal not in policy["token_creators"]:
            raise PermissionError(
                f"Principal {caller_principal} lacks roles/iam.serviceAccountTokenCreator on {target_sa}"
            )

        lifetime = min(lifetime_seconds, 3600)
        now = datetime.now(timezone.utc)
        expire_time = now + timedelta(seconds=lifetime)
        
        # Ephemeral OAuth2 Bearer Token
        token = "ya29.c." + secrets.token_urlsafe(48)
        
        # Dual-Principal Audit Log Entry
        audit_log = {
            "protoPayload": {
                "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "authenticationInfo": {
                    "principalEmail": caller_principal,
                    "serviceAccountDelegationInfo": [
                        { "firstPartyPrincipal": { "principalEmail": target_sa } }
                    ]
                },
                "serviceName": "iamcredentials.googleapis.com",
                "methodName": "google.iam.credentials.v1.IAMCredentials.GenerateAccessToken",
                "resourceName": f"projects/-/serviceAccounts/{target_sa}",
                "status": { "code": 0 }
            },
            "timestamp": now.isoformat()
        }

        return {
            "accessToken": token,
            "expireTime": expire_time.isoformat(),
            "auditLog": audit_log
        }

def main():
    iam = IAMCredentialsService()
    target_sa = "sa-fulfillment-worker@brightloaf-prod-orders.iam.gserviceaccount.com"
    caller = "user:sre-lead@brightloaf.com"
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]

    print(f"=== Service Account Impersonation Request ===")
    print(f"Caller Principal : {caller}")
    print(f"Target SA        : {target_sa}")
    print(f"Requested Scopes : {scopes}\n")

    result = iam.generate_access_token(caller, target_sa, scopes, 3600)
    print(f"[IMPERSONATION SUCCESSFUL]")
    print(f"Ephemeral Access Token : {result['accessToken'][:22]}...")
    print(f"Token Expiration UTC   : {result['expireTime']}")
    print(f"\n[DUAL-PRINCIPAL CLOUD AUDIT LOG]:")
    print(json.dumps(result['auditLog'], indent=2))

    # Test Unauthorized Caller
    print("\n=== Testing Unauthorized Caller Impersonation ===")
    bad_caller = "user:contractor@brightloaf.com"
    try:
        iam.generate_access_token(bad_caller, target_sa, scopes)
    except PermissionError as e:
        print(f"[EXPECTED REJECTION]: {e}")

if __name__ == "__main__":
    main()
