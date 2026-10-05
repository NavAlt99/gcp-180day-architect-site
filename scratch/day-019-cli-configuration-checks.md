# Day 19 Exit Evidence: CLI Configuration, Identity Verification, and Target Environment Controls

## Executive Summary
This document establishes the verified operational exit evidence for Day 19 (Block 2: Cloud Environment and Identity). It documents an authoritative catalog of commands and operational runbooks that reliably identify the target cloud environment, verify authenticated identity and geographical region, eliminate ambient parameter drift, and prevent accidental cross-project switches across `gcloud`, `gcloud storage`, `bq`, and `kubectl`.

---

## 1. Verified Target Environment Identification Commands

To eliminate reliance on implicit ambient state, cloud architects execute the following deterministic inspection commands:

~~~bash
# 1. Audit active gcloud named configuration and associated properties
$ gcloud config configurations list
NAME                IS_ACTIVE  ACCOUNT                PROJECT                COMPUTE_DEFAULT_ZONE  COMPUTE_DEFAULT_REGION
brightloaf-sandbox  True       naveen@brightloaf.com  brightloaf-sandbox-19  us-central1-a         us-central1
brightloaf-prod     False      naveen@brightloaf.com  brightloaf-prod-us     us-east4-a            us-east4

# 2. Inspect active core project identifier directly
$ gcloud config get-value project
brightloaf-sandbox-19

# 3. Inspect active authenticated principal identity
$ gcloud config get-value account
naveen@brightloaf.com

# 4. Inspect active default Compute Engine region and zone
$ gcloud config get-value compute/region
us-central1
$ gcloud config get-value compute/zone
us-central1-a

# 5. Audit ambient environment variables for dangerous precedence overrides
$ env | grep -E '^CLOUDSDK_' || echo "No ambient CLOUDSDK overrides present."
No ambient CLOUDSDK overrides present.
~~~

---

## 2. Multi-CLI Context Alignment Matrix

Independent command-line tools maintain distinct configuration files. The following matrix documents their configuration stores and deterministic audit commands:

| Tool | Domain | Configuration Store | Environment Inspection Command | Project Alignment Check |
| :--- | :--- | :--- | :--- | :--- |
| **gcloud CLI** | Control Plane | `~/.config/gcloud/configurations/` | `gcloud config get-value project` | Core active project |
| **gcloud storage** | Cloud Storage | Inherits gcloud store | `gcloud storage ls --project=[PROJECT]` | Matches gcloud active project |
| **bq CLI** | BigQuery | `~/.bigqueryrc` (fallback: gcloud) | `bq show --format=prettyjson` | Inspects `.project_id` property |
| **kubectl** | GKE / K8s | `~/.kube/config` (Kubeconfig context) | `kubectl config current-context` | Must parse `gke_[PROJECT]_[REGION]_[CLUSTER]` |

---

## 3. Accidental Project Switch Prevention Runbook

To prevent catastrophic cross-project accidents (such as running destructive commands against production while believing a sandbox profile is active), architects mandate the following three technical controls:

### Technical Control 1: Mandatory Explicit Parameter Flags
All automated deployment scripts, CI/CD pipelines, and maintenance runbooks must explicitly pass Tier 1 parameter flags rather than relying on ambient configuration state:
~~~bash
# MANDATORY RUNBOOK STANDARD: Explicit --project and --region flags
TARGET_PROJECT="brightloaf-sandbox-19"
TARGET_REGION="us-central1"

gcloud compute instances list \
  --project="${TARGET_PROJECT}" \
  --filter="zone:(${TARGET_REGION}*)"

# Destructive commands REQUIRE explicit confirmation and explicit project targeting
gcloud compute instances delete instance-test-01 \
  --project="${TARGET_PROJECT}" \
  --zone="${TARGET_REGION}-a" \
  --quiet
~~~

### Technical Control 2: Context-Aware Shell Prompt (PS1)
Configure developer terminal environments to visually highlight the active project context and warn if production is active:
~~~bash
# Embed into ~/.bashrc or ~/.zshrc
format_cloud_prompt() {
    local p=$(gcloud config get-value project 2>/dev/null)
    local k=$(kubectl config current-context 2>/dev/null | awk -F'_' '{print $2}')
    
    # Alert if kubectl and gcloud diverge
    if [[ -n "$k" && "$k" != "$p" ]]; then
        echo -e "\033[1;33m[MISMATCH: gcloud=${p} | k8s=${k}]\033[0m\$ "
    elif [[ "$p" =~ prod ]]; then
        echo -e "\033[1;31m[PROD: ${p}]\033[0m\$ "
    else
        echo -e "\033[1;32m[SANDBOX: ${p}]\033[0m\$ "
    fi
}
PS1='$(format_cloud_prompt)'
~~~

### Technical Control 3: Pre-Execution Environment Sanitization
Sanitize the shell environment prior to executing sensitive administrative workflows to ensure ambient variables do not override named configurations:
~~~bash
# Preflight environment sanitizer
unset CLOUDSDK_CORE_PROJECT
unset CLOUDSDK_COMPUTE_REGION
unset CLOUDSDK_COMPUTE_ZONE
unset BIGQUERY_PROJECT
~~~

---

## 4. Multi-CLI Synchronization Script (`verify_and_sync.sh`)

~~~bash
#!/usr/bin/env bash
set -euo pipefail

TARGET_ENV="${1:-sandbox}"

if [[ "$TARGET_ENV" == "sandbox" ]]; then
    DESIRED_PROJECT="brightloaf-sandbox-19"
    DESIRED_CLUSTER="sandbox-cluster"
    DESIRED_REGION="us-central1"
    DESIRED_CONFIG="brightloaf-sandbox"
elif [[ "$TARGET_ENV" == "prod" ]]; then
    DESIRED_PROJECT="brightloaf-prod-us"
    DESIRED_CLUSTER="brightloaf-prod-cluster"
    DESIRED_REGION="us-east4"
    DESIRED_CONFIG="brightloaf-prod"
else
    echo "Unknown environment: $TARGET_ENV" && exit 1
fi

echo "Switching named gcloud configuration to [${DESIRED_CONFIG}]..."
gcloud config configurations activate "${DESIRED_CONFIG}"

echo "Synchronizing kubectl credentials for cluster [${DESIRED_CLUSTER}]..."
gcloud container clusters get-credentials "${DESIRED_CLUSTER}" \
    --region="${DESIRED_REGION}" \
    --project="${DESIRED_PROJECT}"

echo "======================================================="
echo "VERIFYING CONTEXT SYNCHRONIZATION:"
echo "gcloud Project: $(gcloud config get-value project)"
echo "kubectl Context: $(kubectl config current-context)"
echo "Target Region:  $(gcloud config get-value compute/region)"
echo "======================================================="
~~~

---

## 5. Architectural Approval and Sign-Off
- **Lead Cloud Architect:** Lead Infrastructure & Governance
- **Curriculum Day:** Day 19 (CLI configuration and identity checks)
- **Status:** APPROVED AND VERIFIED FOR OPERATIONAL ONBOARDING
