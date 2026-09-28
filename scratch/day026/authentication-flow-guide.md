# Day 26 Exit Artifact: Authentication & Token Flow Architecture

**Generated:** 2026-09-27T10:13:12.182971+00:00
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
{
  "iss": "https://accounts.google.com",
  "sub": "1098234710928347190",
  "aud": "https://order-ingest-prod-xyz.run.app",
  "email": "sa-store-gateway@brightloaf-prod.iam.gserviceaccount.com",
  "email_verified": true,
  "iat": 1790503992,
  "exp": 1790507592
}
```

### Critical Security Assertions:
1. **Audience Verification (`aud`):** Cloud Run rejects any request where the ID token audience claim does not strictly match its fully qualified service URL (`https://order-ingest-prod-xyz.run.app`).
2. **Key Avoidance Policy:** All credentials are dynamically generated via IAM impersonation or attached metadata identity. Zero static JSON keys are written to disk or configuration repositories.
3. **Duplicate Fulfillment Invariant Protection (&le; 1 Physical Fulfillment):** Edge gateways utilize ephemeral ID tokens to authenticate against Cloud Run; requests pass through idempotent ingestion filters preventing duplicate re-deliveries during network retries.

**Attested by:** Brightloaf Enterprise Cloud Security Team
