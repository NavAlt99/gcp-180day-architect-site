"""day_data_template.py — Specification Template for Day Authoring.

Standard: Days 40–50 Architectural Benchmark (e.g., day-044, day-045, day-050).
Copy this template to scratch/day_data_{DAY:03d}.py, fill in the fields, and run:
    python3 scripts/author_engine.py --day {DAY}

================================================================================
CRITICAL AUTHORING MANDATES (NON-NEGOTIABLE):
================================================================================
1. 1:1 COVERAGE:
   - If the syllabus specifies N topics (typically 4 to 6), TOPICS must contain
     exactly N entries.
   - Every single topic MUST have a dedicated, unmerged Part 3 Field Case and
     a dedicated, unmerged Part 4 Hands-On Lab Exercise (N problems, N exercises).

2. PART 3 (REAL-WORLD FIELD INCIDENTS):
   - Enterprise context: Brightloaf e-commerce, banking, logistics, or data platform.
   - Concrete SLO burn rate, failure symptoms, dollar/transaction impact.
   - VERBATIM EVIDENCE: Raw terminal logs, Kubelet events, JSON Cloud Logging audit
     payloads, curl output, or stack traces inside code blocks.
   - Deep systems root cause: Kernel cgroups, CFS quotas, IAM token refresh lifetimes,
     BGP routing dynamics, TLS handshakes, or control/data plane divergence.
   - Multi-step diagnostic sequence and defensible tactical + strategic remediation.
   - Dual-lane Incident SVG flow (5 nodes: Event -> Failure -> Impact -> Fix -> Outcome).

3. PART 4 (8-STAGE OPERATIONAL LAB LIFECYCLE):
   - ZERO DIFFICULTY LABELS: Under no circumstance include "Beginner", "Intermediate",
     "Advanced", "Level 1/2/3", or similar difficulty markers.
   - Every exercise must progress through the standard 8-stage engineering lifecycle:
       Stage 1: Preflight & Environment Validation (env vars, APIs, IAM permissions)
       Stage 2: Target / Backing Infrastructure Provisioning (service accounts, secrets, buckets)
       Stage 3: Production Manifest Authoring (multi-resource YAML / Terraform / JSON configs)
       Stage 4: Workload Deployment & Orchestration (kubectl apply, gcloud deploy, terraform apply)
       Stage 5: Runtime Inspection & Verification (exec, curl assertions, log queries)
       Stage 6: Chaos / Fault Injection & Failure Rehearsal (breaking dependency, revoking token)
       Stage 7: Triage, Troubleshooting & Remediation Patch (identifying error and fixing)
       Stage 8: Cleanup & Resource Teardown (step-by-step removal, zero orphaned costs)
       Stage 9: Artifact Acceptance Criteria (saving verified proof into daily markdown artifact)
   - Code density: 6 to 10 distinct code blocks per exercise (matching Day 44/45/50).
   - High-contrast callout boxes for Acceptance (.callout.success), Troubleshooting (.callout.caution),
     and Cleanup/Cost (.callout).

4. VALIDATOR COMPLIANCE:
   - All runnable commands outside code blocks MUST use <kbd>command</kbd> (never bare <code>).
   - All code blocks must use <pre><code class="language-...">.
   - Every lab must retain its data-progress checkbox: lab-{DAY:03d}-{key}.
================================================================================
"""

DAY = 0  # e.g., 101
WORK_BLOCK = ""  # e.g., "Operations, Reliability, and SRE Architecture"

PART1_INTRO = (
    "Comprehensive introduction to today's architecture themes, operational constraints, "
    "and system boundaries."
)

EXIT_SUMMARY = (
    "Production-grade exit artifacts demonstrating verifiable policy enforcement, "
    "failure mode resilience, and architectural compliance."
)

# Optional comparison/architecture table in Part 2
ARCH_TABLE_HTML = """
<table>
<caption>Enterprise Architectural Comparison and Trade-offs</caption>
<thead>
<tr>
  <th scope="col">Design Option / Strategy</th>
  <th scope="col">Google Cloud Implementation</th>
  <th scope="col">Data Plane & Control Plane Boundary</th>
  <th scope="col">Primary Advantage</th>
  <th scope="col">Trade-off & Failure Blast Radius</th>
</tr>
</thead>
<tbody>
<tr>
  <th scope="row">Pattern A</th>
  <td>Cloud Armor + Managed Protection Plus + Global External ALB</td>
  <td>Edge Envoy proxy layer with anycast routing</td>
  <td>Sub-second DDoS mitigation before traffic reaches backend VPC</td>
  <td>Increased ingress egress billing; false-positive rate tuning overhead</td>
</tr>
<tr>
  <th scope="row">Pattern B</th>
  <td>PSC Service Attachments + Regional Internal ALBs</td>
  <td>Direct SDN encapsulation across VPC boundaries</td>
  <td>Zero public IP exposure, strict IAM consumer accept policies</td>
  <td>Transitive routing limitations; requires dedicated NAT subnet planning</td>
</tr>
</tbody>
</table>
"""

# Architecture Diagram Options for Part 2:
# Option 1: Full bespoke raw SVG markup (Day 65/67 caliber)
# ARCH_SVG_HTML = """<figure class="diagram-container">...</figure>"""
#
# Option 2: Structured multi-tier topology (layers, components, flows, boundaries, probes)
ARCH_DIAGRAM = {
    "type": "topology",
    "title": "Enterprise System Architecture & Boundary Enforcement Topology",
    "desc": "Multi-tier operational architecture showing infrastructure layers, security perimeters, and request flows.",
    "caption": "Figure: Infrastructure layers, request flows, and verification boundaries.",
    "width": 1100,
    "height": 640,
    "layers": [
        {"name": "LAYER 1: Ingress / Edge Perimeter", "desc": "Global External ALB, Cloud Armor, SSL Termination", "fill": "#1e3a5f", "y": 10, "h": 90},
        {"name": "LAYER 2: Service Mesh & Routing", "desc": "Anthos / GKE Gateway API, Dataplane V2", "fill": "#0c2838", "y": 110, "h": 90},
        {"name": "LAYER 3: Compute & Workload Runtime", "desc": "GKE Autopilot, Cloud Run, Workload Identity", "fill": "#064e3b", "y": 210, "h": 90},
        {"name": "LAYER 4: Persistence & Data Tier", "desc": "Cloud Spanner, Cloud SQL, Secret Manager", "fill": "#1e1b4b", "y": 310, "h": 90},
        {"name": "LAYER 5: Observability & Security Vault", "desc": "Cloud Logging Aggregated Sinks, BigQuery Audit Vault", "fill": "#3b0764", "y": 410, "h": 90},
    ],
    "components": [
        {"id": "alb", "name": "Global External ALB", "detail": "Anycast Ingress (TLS 1.3)", "x": 100, "y": 30, "w": 240, "h": 50, "fill": "#0f2338", "stroke": "#38bdf8"},
        {"id": "armor", "name": "Cloud Armor Policy", "detail": "WAF & Adaptive Protection", "x": 420, "y": 30, "w": 260, "h": 50, "fill": "#0f2338", "stroke": "#38bdf8"},
        {"id": "gw", "name": "GKE Gateway Controller", "detail": "Envoy Layer 7 Routing", "x": 420, "y": 130, "w": 260, "h": 50, "fill": "#0f2338", "stroke": "#38bdf8"},
        {"id": "pods", "name": "Workload Pods (mTLS)", "detail": "Dataplane V2 eBPF Policies", "x": 420, "y": 230, "w": 260, "h": 50, "fill": "#093322", "stroke": "#22c55e"},
        {"id": "db", "name": "Cloud Spanner Instance", "detail": "Regional High-Availability", "x": 420, "y": 330, "w": 260, "h": 50, "fill": "#1e1b4b", "stroke": "#a855f7"},
        {"id": "logs", "name": "Aggregated Log Sink", "detail": "Central Security Archive", "x": 750, "y": 430, "w": 260, "h": 50, "fill": "#280a3c", "stroke": "#c084fc"},
    ],
    "flows": [
        {"x1": 340, "y1": 55, "x2": 420, "y2": 55, "type": "ok", "label": "HTTPS:443"},
        {"x1": 550, "y1": 80, "x2": 550, "y2": 130, "type": "ok", "label": "Internal VPC"},
        {"x1": 550, "y1": 180, "x2": 550, "y2": 230, "type": "ok", "label": "eBPF Pod Ingress"},
        {"x1": 550, "y1": 280, "x2": 550, "y2": 330, "type": "ok", "label": "gRPC / IAM Token"},
        {"x1": 680, "y1": 255, "x2": 750, "y2": 455, "type": "ok", "label": "Audit Telemetry"},
    ],
    "boundaries": [
        {"x": 60, "y": 14, "w": 300, "h": 76, "label": "PUBLIC EDGE PERIMETER", "color": "#f59e0b"},
        {"x": 60, "y": 214, "w": 300, "h": 76, "label": "ZERO-TRUST WORKLOAD PERIMETER", "color": "#10b981"},
    ],
    "probes": [
        {"cx": 550, "cy": 105, "label": "FI-1: Ingress Gateway Intercept", "color": "#f43f5e"},
        {"cx": 550, "cy": 205, "label": "FI-2: eBPF Policy Denial", "color": "#f43f5e"},
    ]
}

# Standard 1:1 Topics Definition
# IMPORTANT: Provide one full block per topic covered in the day's brief.
TOPICS = [
    {
        "key": "topic-01",
        "title": "Topic Title Matching Syllabus (e.g., Organization Policy Enforcement)",
        "preview": (
            "Sentence 1 describing a concrete technical symptom or decision. "
            "Sentence 2 describing its direct user or business impact."
        ),
        "overview": (
            "Define the mechanism, ownership boundary, service model, and fundamental behavior. "
            "Keep teaching prose concise and non-repetitive."
        ),
        "technical": (
            "Explain control and data plane mechanics, limits, failure boundaries, and trade-offs.\n\n"
            "- **Control Plane Boundary:** Deep explanation of configuration propagation and API limits.\n"
            "- **Data Plane Path:** Packet or token evaluation path, kernel/driver behavior, latency.\n"
            "- **Failure & Recovery Dynamics:** Behavior during network splits or quota exhaustion."
        ),
        "questions": [
            "Architectural evaluation question 1 examining trade-offs?",
            "Architectural evaluation question 2 regarding failure blast radius?",
            "Architectural evaluation question 3 focused on auditability?",
        ],
        "reference": "https://cloud.google.com/resource-manager/docs/organization-policy/overview",
        "reference_label": "Google Cloud Resource Manager: Organization Policy Documentation",

        # PART 3: Realistic Operational Incident (Day 40-50 Standard)
        "scenario": {
            "scenario": (
                "Brightloaf's regional fulfillment service experienced severe order processing degradations "
                "following a cluster configuration update. The incident triggered high-priority P1 alerts "
                "across the site reliability team."
            ),
            "symptom": (
                "Workload pods entered CrashLoopBackOff with HTTP 500 errors returned to the checkout service, "
                "causing 14% of cart checkouts to fail over a 32-minute window."
            ),
            "impact": (
                "SLO burn rate spiked to 18x normal baseline. 2,400 orders stalled in unfulfilled state, "
                "costing an estimated $42,000 in lost revenue and SLA credit penalties."
            ),
            "constraints": (
                "Zero plaintext credentials in process memory or source control; maintain PCI-DSS strict "
                "compliance; zero maintenance window downtime allowed for active order pipelines."
            ),
            # MANDATORY: Verbatim error logs, terminal transcripts, or JSON payloads
            "evidence": (
                "Running `<kbd>kubectl describe pod order-fulfillment-7f89d-x4w8k</kbd>` and inspecting node events revealed:\n\n"
                "```text\n"
                "Events:\n"
                "  Type     Reason       Age                From               Message\n"
                "  ----     ------       ----               ----               -------\n"
                "  Normal   Scheduled    4m12s              default-scheduler  Successfully assigned default/order-fulfillment-7f89d-x4w8k to gke-prod-pool-1\n"
                "  Warning  FailedMount  28s (x8 over 4m)   kubelet            MountVolume.SetUp failed for volume \"vault-token\": rpc error: code = PermissionDenied desc = Service account does not have access\n"
                "  Warning  Failed       12s (x3 over 90s)  kubelet            Error: container create failed: stat /etc/secrets/token: no such file or directory\n"
                "```\n\n"
                "Inspection of Cloud Logging JSON payload confirmed IAM identity mismatch:\n\n"
                "```json\n"
                "{\n"
                "  \"protoPayload\": {\n"
                "    \"@type\": \"type.googleapis.com/google.cloud.audit.AuditLog\",\n"
                "    \"status\": {\"code\": 7, \"message\": \"PERMISSION_DENIED: Caller brightloaf-gke@brightloaf-prod.iam.gserviceaccount.com lacks roles/secretmanager.secretAccessor\"},\n"
                "    \"methodName\": \"google.cloud.secretmanager.v1.SecretManagerService.AccessSecretVersion\"\n"
                "  }\n"
                "}\n"
                "```"
            ),
            "root": (
                "The deployment pipeline updated the Kubernetes ServiceAccount without updating the corresponding "
                "Google Cloud IAM Workload Identity binding. When the CSI Secret Store driver requested a short-lived "
                "OAuth2 token from the GKE metadata server, Cloud IAM rejected the impersonation request, causing the "
                "CSI node daemon to fail volume mount setup."
            ),
            "diagnostic_steps": [
                "Step 1: Check pod status and events via <kbd>kubectl describe pod -l app=order-fulfillment</kbd> to identify MountVolume failure signatures.",
                "Step 2: Inspect GKE metadata server audit logs in Cloud Logging using filter `protoPayload.methodName=\"AccessSecretVersion\"` to observe HTTP 403 / Code 7 errors.",
                "Step 3: Validate Workload Identity KSA-to-GSA annotation via <kbd>kubectl get serviceaccount fulfillment-ksa -o yaml</kbd> and check IAM binding with <kbd>gcloud iam service-accounts get-iam-policy</kbd>.",
                "Step 4: Execute token inspection test inside a diagnostic pod to verify metadata server response."
            ],
            "fix": (
                "Tactical Fix: Immediately bind the Kubernetes ServiceAccount to the Google ServiceAccount via "
                "<kbd>gcloud iam service-accounts add-iam-policy-binding</kbd> with `roles/iam.workloadIdentityUser`.\n\n"
                "Strategic Fix: Author declarative Terraform configuration enforcing Workload Identity binding as an atomic "
                "module, preventing deployment of Kubernetes manifests before Cloud IAM policy propagation completes."
            ),
            "verify": (
                "Confirm that all fulfillment pods transition to `Running (1/1)` state within 60 seconds of applying the binding. "
                "Verify volume mount via `<kbd>kubectl exec -it deployment/order-fulfillment -- ls -la /etc/secrets</kbd>` and "
                "assert zero PERMISSION_DENIED events in Cloud Logging."
            ),
            "residual": (
                "Workload Identity token generation incurs a 20ms metadata server latency during cold-start pod creation. "
                "Application retry loops must incorporate exponential backoff with jitter to prevent metadata server throttling "
                "during massive node surge events."
            ),
            # 5-node flow for Incident SVG
            "diagram": (
                "Workload Identity drift during deployment",
                "CSI driver secret volume mount failed",
                "Pod enters CrashLoop; checkout 500 spike",
                "Add workloadIdentityUser IAM role binding",
                "Pod mounts secret volume & recovers"
            )
        },

        # PART 4: 8-Stage Hands-On Operational Engineering Lab (Day 40-50 Standard)
        "lab": {
            "name": "Production Workload Identity Federation & Secret Volume Mounting",
            "file": "day-000-topic-01.md",
            "goal": (
                "Configure Workload Identity Federation, author a SecretProviderClass manifest, deploy a zero-trust "
                "workload mounting Cloud Secret Manager volumes, and execute a controlled chaos fault injection drill."
            ),
            "expected": (
                "A running workload mounting secrets as an ephemeral volume, with zero plaintext secrets in etcd or process "
                "environment tables, verified automated recovery under token revocation chaos."
            ),
            "mode": "tabletop analysis & production CLI / YAML execution",
            "prereq": "Prior day exit artifacts, active GCP project, kubectl, gcloud CLI",
            "preflight": (
                "Verify GCP project environment variables, authenticated identity, and required API enablement: "
                "container.googleapis.com, secretmanager.googleapis.com, iam.googleapis.com."
            ),
            "steps": [
                (
                    "**Stage 1: Preflight & Environment Validation**\n"
                    "- Set target environment variables and enable required GCP service APIs:\n\n"
                    "```sh\n"
                    "export PROJECT_ID=\"brightloaf-prod\"\n"
                    "export REGION=\"us-central1\"\n"
                    "export CLUSTER_NAME=\"brightloaf-gke\"\n"
                    "export KSA_NAME=\"order-fulfillment-ksa\"\n"
                    "export GSA_NAME=\"order-fulfillment-gsa\"\n"
                    "\n"
                    "gcloud config set project ${PROJECT_ID}\n"
                    "gcloud services enable container.googleapis.com secretmanager.googleapis.com iam.googleapis.com\n"
                    "```"
                ),
                (
                    "**Stage 2: Target / Backing Infrastructure Provisioning**\n"
                    "- Provision the Google Service Account and create an encrypted secret in Secret Manager:\n\n"
                    "```sh\n"
                    "# 1. Create dedicated Google Service Account\n"
                    "gcloud iam service-accounts create ${GSA_NAME} \\\n"
                    "    --description=\"GSA for Order Fulfillment Microservice\" \\\n"
                    "    --display-name=\"Order Fulfillment GSA\"\n"
                    "\n"
                    "# 2. Create target database credentials in Secret Manager\n"
                    "printf \"SuperSecretOrderDB_2026!\" | gcloud secrets create order-db-password \\\n"
                    "    --data-file=- \\\n"
                    "    --replication-policy=\"automatic\"\n"
                    "\n"
                    "# 3. Grant Secret Accessor role to the GSA\n"
                    "gcloud secrets add-iam-policy-binding order-db-password \\\n"
                    "    --member=\"serviceAccount:${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com\" \\\n"
                    "    --role=\"roles/secretmanager.secretAccessor\"\n"
                    "```"
                ),
                (
                    "**Stage 3: Production Manifest Authoring (Multi-Resource YAML)**\n"
                    "- Author the Kubernetes ServiceAccount with Workload Identity annotation and the CSI `SecretProviderClass` manifest:\n\n"
                    "```sh\n"
                    "cat <<EOF > secret-provider-class.yaml\n"
                    "apiVersion: v1\n"
                    "kind: ServiceAccount\n"
                    "metadata:\n"
                    "  name: ${KSA_NAME}\n"
                    "  namespace: default\n"
                    "  annotations:\n"
                    "    iam.gke.io/gcp-service-account: ${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com\n"
                    "---\n"
                    "apiVersion: secrets-store.csi.x-k8s.io/v1\n"
                    "kind: SecretProviderClass\n"
                    "metadata:\n"
                    "  name: order-secret-provider\n"
                    "  namespace: default\n"
                    "spec:\n"
                    "  provider: gcp\n"
                    "  parameters:\n"
                    "    secrets: |\n"
                    "      - resourceName: \"projects/${PROJECT_ID}/secrets/order-db-password/versions/latest\"\n"
                    "        path: \"db-password.txt\"\n"
                    "EOF\n"
                    "cat secret-provider-class.yaml\n"
                    "```"
                ),
                (
                    "**Stage 4: Workload Deployment & Orchestration**\n"
                    "- Author and apply the deployment manifest that mounts the CSI volume:\n\n"
                    "```sh\n"
                    "cat <<'EOF' > fulfillment-deployment.yaml\n"
                    "apiVersion: apps/v1\n"
                    "kind: Deployment\n"
                    "metadata:\n"
                    "  name: order-fulfillment\n"
                    "  namespace: default\n"
                    "spec:\n"
                    "  replicas: 2\n"
                    "  selector:\n"
                    "    matchLabels:\n"
                    "      app: order-fulfillment\n"
                    "  template:\n"
                    "    metadata:\n"
                    "      labels:\n"
                    "        app: order-fulfillment\n"
                    "    spec:\n"
                    "      serviceAccountName: order-fulfillment-ksa\n"
                    "      containers:\n"
                    "      - name: app\n"
                    "        image: mirror.gcr.io/library/busybox:1.36\n"
                    "        command: [\"sh\", \"-c\", \"while true; do cat /etc/secrets/db-password.txt; sleep 30; done\"]\n"
                    "        volumeMounts:\n"
                    "        - name: secret-mount\n"
                    "          mountPath: \"/etc/secrets\"\n"
                    "          readOnly: true\n"
                    "      volumes:\n"
                    "      - name: secret-mount\n"
                    "        csi:\n"
                    "          driver: secrets-store.csi.k8s.io\n"
                    "          readOnly: true\n"
                    "          volumeAttributes:\n"
                    "            secretProviderClass: \"order-secret-provider\"\n"
                    "EOF\n"
                    "kubectl apply -f secret-provider-class.yaml\n"
                    "kubectl apply -f fulfillment-deployment.yaml\n"
                    "```"
                ),
                (
                    "**Stage 5: Runtime Inspection & Multi-Layer Verification**\n"
                    "- Verify pod status, inspect the mounted secret file, and prove zero plaintext environment leaks:\n\n"
                    "```sh\n"
                    "# 1. Confirm pods reach Running (1/1) status\n"
                    "kubectl get pods -l app=order-fulfillment\n"
                    "POD_NAME=$(kubectl get pods -l app=order-fulfillment -o jsonpath='{.items[0].metadata.name}')\n"
                    "\n"
                    "# 2. Read mounted secret from container filesystem\n"
                    "kubectl exec ${POD_NAME} -- cat /etc/secrets/db-password.txt\n"
                    "\n"
                    "# 3. Assert zero plaintext credentials in environment variables\n"
                    "kubectl exec ${POD_NAME} -- env | grep -E -i 'pass|secret|token' || echo 'PASSED: No secrets in env'\n"
                    "```"
                ),
                (
                    "**Stage 6: Chaos / Fault Injection & Failure Rehearsal**\n"
                    "- Intentionally revoke the IAM role binding and observe failure behavior on new pod replicas:\n\n"
                    "```sh\n"
                    "# Simulate IAM policy drift by revoking Secret Accessor role\n"
                    "gcloud secrets remove-iam-policy-binding order-db-password \\\n"
                    "    --member=\"serviceAccount:${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com\" \\\n"
                    "    --role=\"roles/secretmanager.secretAccessor\"\n"
                    "\n"
                    "# Delete a pod to force GKE scheduler to recreate it\n"
                    "kubectl delete pod ${POD_NAME}\n"
                    "\n"
                    "# Observe MountVolume.SetUp failure event\n"
                    "sleep 10\n"
                    "kubectl get events -n default --field-selector reason=FailedMount | tail -n 5\n"
                    "```"
                ),
                (
                    "**Stage 7: Triage, Troubleshooting & Remediation Patch**\n"
                    "- Diagnose the error signature from events and apply the remediation patch:\n\n"
                    "```sh\n"
                    "# Re-grant the required IAM policy binding\n"
                    "gcloud secrets add-iam-policy-binding order-db-password \\\n"
                    "    --member=\"serviceAccount:${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com\" \\\n"
                    "    --role=\"roles/secretmanager.secretAccessor\"\n"
                    "\n"
                    "# Confirm reconciliation and pod recovery\n"
                    "kubectl rollout status deployment/order-fulfillment --timeout=60s\n"
                    "kubectl get pods -l app=order-fulfillment\n"
                    "```"
                ),
                (
                    "**Stage 8: Cleanup & Resource Teardown**\n"
                    "- Teardown manifests and delete test resources to avoid orphaned costs:\n\n"
                    "```sh\n"
                    "kubectl delete -f fulfillment-deployment.yaml --ignore-not-found\n"
                    "kubectl delete -f secret-provider-class.yaml --ignore-not-found\n"
                    "gcloud secrets delete order-db-password --quiet\n"
                    "gcloud iam service-accounts delete ${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com --quiet\n"
                    "rm -f secret-provider-class.yaml fulfillment-deployment.yaml\n"
                    "```"
                ),
                (
                    "**Stage 9: Artifact Acceptance**\n"
                    "- Save the verified execution log proving zero environment variable leaks and successful volume mount "
                    "into `day-000-topic-01.md`."
                )
            ],
            "verification": (
                "Verified file mount at `/etc/secrets/db-password.txt` populated directly from Secret Manager via CSI, "
                "with zero plaintext passwords in process environment tables, and confirmed automated recovery post-IAM patch."
            ),
            "trouble": (
                "If pod reports `MountVolume.SetUp failed for volume \"secret-mount\"`: Check that Workload Identity is enabled "
                "on the GKE node pool. Verify that the KSA is correctly annotated with `iam.gke.io/gcp-service-account`, and run "
                "`gcloud iam service-accounts get-iam-policy` to confirm `roles/iam.workloadIdentityUser` binding exists."
            ),
            "cleanup": (
                "Deleting the Secret Manager secret and GKE deployment eliminates ongoing API and storage costs. "
                "Secret Manager charges $0.18/version/month and $0.06 per 10,000 API operations."
            ),
            "accept": "Artifact acceptance criteria verified and documented with zero lingering resources."
        }
    }
]
