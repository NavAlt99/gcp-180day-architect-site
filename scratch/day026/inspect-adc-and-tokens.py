#!/usr/bin/env python3
"""
inspect-adc-and-tokens.py
Demonstrates ADC discovery hierarchy and parses Access Tokens vs OIDC ID Tokens.
Generates the Day 26 Exit Artifact: authentication-flow-guide.md
"""
import base64
import json
import os
from datetime import datetime, timezone, timedelta

def simulate_adc_resolution():
    steps = [
        {"step": 1, "source": "GOOGLE_APPLICATION_CREDENTIALS", "status": "CHECKING", "found": False},
        {"step": 2, "source": "gcloud user credentials (~/.config/gcloud/...)", "status": "CHECKING", "found": False},
        {"step": 3, "source": "Compute Engine Metadata Server (169.254.169.254)", "status": "CHECKING", "found": True}
    ]
    return steps

def generate_mock_tokens():
    now = datetime.now(timezone.utc)
    exp = now + timedelta(hours=1)
    
    # 1. OAuth2 Access Token (Opaque)
    access_token = "ya29.c.b0AXv0zTOrientedAccessToken1234567890abcdef"
    
    # 2. OIDC ID Token (JWT: Header.Payload.Signature)
    header = {"alg": "RS256", "typ": "JWT", "kid": "cert-key-2026"}
    payload = {
        "iss": "https://accounts.google.com",
        "sub": "1098234710928347190",
        "aud": "https://order-ingest-prod-xyz.run.app",
        "email": "sa-store-gateway@brightloaf-prod.iam.gserviceaccount.com",
        "email_verified": True,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp())
    }
    
    def b64url(data):
        return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip("=")
    
    id_token = f"{b64url(header)}.{b64url(payload)}.MOCK_CRYPTOGRAPHIC_SIGNATURE_BYTES"
    return access_token, id_token, payload

def compile_exit_artifact(access_token, id_token, id_payload):
    artifact_content = f"""# Day 26 Exit Artifact: Authentication & Token Flow Architecture

**Generated:** {datetime.now(timezone.utc).isoformat()}
**Objective:** An authentication flow separating authentication from authorization and access tokens from ID tokens; never save tokens.

---

## 1. Application Default Credentials (ADC) Search Chain

Google Cloud client libraries locate credentials automatically without hardcoding paths or secrets:

```
[Application Default Credentials (ADC) Resolution Flow]
   │
   ├─► 1. Check GOOGLE_APPLICATION_CREDENTIALS environment variable
   │       └── If set, read file path (Service Account key, external workforce config)
   │
   ├─► 2. Check well-known User ADC configuration
   │       └── Location: ~/.config/gcloud/application_default_credentials.json
   │
   ├─► 3. Query Compute Engine Metadata Server (Production Standard)
   │       └── URL: http://metadata.google.internal/computeMetadata/v1/
   │       └── Header: Metadata-Flavor: Google
   │       └── Output: Ephemeral 1-hour OAuth2 token minted for attached identity
   │
   └─► 4. Fail: Raise DefaultCredentialsError
```

---

## 2. Separation of Authentication vs. Authorization

| Dimension | OAuth2 Access Token (Authorization) | OpenID Connect ID Token (Authentication) |
|:---|:---|:---|
| **Core Question** | *What is this caller permitted to do?* | *Who is this caller, and who is this token meant for?* |
| **Target Destination** | Google Cloud APIs (`*.googleapis.com`) | Cloud Run, Cloud Functions, API Gateway |
| **Token Structure** | Opaque bearer string (`ya29...`) | Signed JSON Web Token (`Header.Payload.Signature`) |
| **Key Attribute** | Scopes: `https://www.googleapis.com/auth/cloud-platform` | Audience: `aud` must match destination URL |
| **Validation Entity** | Google Cloud API Gateway & IAM Policy Engine | Target Microservice / Cloud Run Envoy Ingress |
| **Storage Rule** | **In-memory only; never persist to disk** | **In-memory only; never persist to disk** |

---

## 3. Dissected OIDC ID Token Claims

```json
{{
  "iss": "{id_payload['iss']}",
  "sub": "{id_payload['sub']}",
  "aud": "{id_payload['aud']}",
  "email": "{id_payload['email']}",
  "email_verified": true,
  "iat": {id_payload['iat']},
  "exp": {id_payload['exp']}
}}
```

### Critical Security Assertions:
1. **Audience Verification (`aud`):** Cloud Run rejects any request where the ID token audience claim does not strictly match its fully qualified service URL (`https://order-ingest-prod-xyz.run.app`).
2. **Key Avoidance Policy:** All credentials are dynamically generated via IAM impersonation or attached metadata identity. Zero static JSON keys are written to disk or configuration repositories.
3. **Duplicate Fulfillment Invariant Protection (&le; 1 Physical Fulfillment):** Edge gateways utilize ephemeral ID tokens to authenticate against Cloud Run; requests pass through idempotent ingestion filters preventing duplicate re-deliveries during network retries.

**Attested by:** Brightloaf Enterprise Cloud Security Team
"""

    os.makedirs("scratch/day026", exist_ok=True)
    artifact_path = "scratch/day026/authentication-flow-guide.md"
    with open(artifact_path, "w") as f:
        f.write(artifact_content)
    print(f"=== Successfully Compiled Exit Artifact: {artifact_path} ===")

def main():
    print("=== ADC Resolution & Token Anatomy Dissector ===")
    steps = simulate_adc_resolution()
    for s in steps:
        print(f"Step {s['step']}: {s['source']} -> {'FOUND (ACTIVE)' if s['found'] else 'SKIPPED'}")
    
    access_tok, id_tok, id_payload = generate_mock_tokens()
    print(f"\nOAuth2 Access Token Sample : {access_tok[:20]}...")
    print(f"OIDC ID Token Sample       : {id_tok[:25]}...")
    print(f"Decoded ID Token Audience  : {id_payload['aud']}")
    print(f"Decoded ID Token Subject   : {id_payload['email']}")

    compile_exit_artifact(access_tok, id_tok, id_payload)

if __name__ == "__main__":
    main()
