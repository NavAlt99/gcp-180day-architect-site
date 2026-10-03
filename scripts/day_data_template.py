"""day_data_template.py — Specification Template for Day Authoring.

Standard: Days 40–50 Architectural Benchmark (e.g., day-044, day-045, day-050).
Copy this template to scratch/day_data_{DAY:03d}.py, fill in the fields, and run:
    python3 scripts/author_engine.py --day {DAY}

================================================================================
CRITICAL AUTHORING MANDATES (NON-NEGOTIABLE):
================================================================================
Follow PAGE_AUTHORING_CONTRACT.md for the complete shared requirements.
For every topic's Part 2 discussion, first list all in-scope subtopics, then discuss
each in order with explicit explanations of: what it is in general, its relevance
to a cloud architect across providers, and its particular application to GCP.
Give each subtopic a plain-language definition, expanded acronyms, mechanism, concrete example, and relevant source;
do not invent a GCP service equivalent when the concept has none.
Use <strong class="keyword"> for selected paragraph terms and <strong class="side-heading"> for blue bold labels.
ONLY diagram actual multi-step sequences, packet traversal, or request/response lifecycles.
Omit diagrams for definitions, static features, and configuration topics. Explicitly set
scenario["diagram_enabled"] = False for nonqualifying topics, True for qualifying ones.
Leave ARCH_DIAGRAM/ARCH_SVG_HTML empty when no Part 2 flow qualifies.
Each lab stage needs execution location, commands/full files or numbered manual steps,
exact inputs, observable result, and evidence to save. Cover local and GCP execution
where applicable; manual steps need a relevant official procedure link as well.
Run scripts/check_study_links.py --day {DAY} after building and review source relevance.
Every node in every topology and incident diagram must have a readable label and
an appropriate icon: official product icons for GCP services, network component
icons for generic infrastructure, and concept icons for events/decisions/outcomes.
Record icon sources, keep assets local or embedded, and verify mapping and layout.

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
   - Only when the Diagram Generation Rule qualifies: dual-lane incident SVG flow.

3. PART 4 (EXACTLY 8 LAB EXECUTION STAGES):
   - ZERO DIFFICULTY LABELS: Under no circumstance include "Beginner", "Intermediate",
     "Advanced", "Level 1/2/3", or similar difficulty markers.
   - Each exercise must contain exactly eight clearly titled execution stages, modeled on Day 96:
       Stage 1: Preflight & Assumption / Environment Validation
       Stage 2: Prepare Target, Inputs, or Backing Resources
       Stage 3: Author the Plan, Configuration, or Analysis
       Stage 4: Execute or Simulate the Planned Work
       Stage 5: Inspect Expected State & Verify Outcomes
       Stage 6: Rehearse a Bounded Failure, Edge Case, or Decision Challenge
       Stage 7: Diagnose Evidence & Record Remediation / Decision
       Stage 8: Cleanup or Exercise Closeout
     Adapt labels and actions to the topic. Each stage must have a real action and observable result: exact runnable commands/file
     contents when appropriate, or exact inputs plus a concrete worksheet/calculation/decision output for local/tabletop work.
     Headings alone, generic “review/analyze/verify” directions, and placeholders are insufficient. Local/tabletop labs must remain
     local/tabletop and must not invent cloud provisioning, deployment, or fault injection. Put artifact acceptance criteria after
     the eight stages in the lab's acceptance field/callout.
   - Make all eight stages substantive, but use code blocks only when commands or multi-line file contents serve the exercise; local/tabletop work may use analysis tables, checklists, or decision records instead.
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
# Architecture Diagram for Part 2 (Mandatory Day 121 Standard Schema):
# Multi-tier topology with generous non-overlapping tiers (1120x690), exact vertical drops (x1 == x2),
# verified boundary boxes, strategic probe pins, and bottom checkpoints panel.
ARCH_DIAGRAM = {
    "type": "topology",
    "title": "Enterprise System Architecture & Boundary Enforcement Topology",
    "desc": "Multi-tier operational architecture showing infrastructure layers, security perimeters, and request flows.",
    "caption": "Figure: Infrastructure layers, request flows, and boundary verification.",
    "width": 1120,
    "height": 690,
    "layers": [
        {"name": "INGRESS / DEMAND & INPUTS", "desc": "requests · identities · workloads · policies", "x": 20, "y": 55, "w": 1080, "h": 92, "fill": "#1e3a5f", "title_color": "#7dd3fc"},
        {"name": "MANAGED RUNTIME & DATA PLANE", "desc": "sandboxed compute · service mesh · persistence tier", "x": 20, "y": 185, "w": 1080, "h": 210, "fill": "#064e3b", "title_color": "#6ee7b7"},
        {"name": "GOVERNANCE, AUDIT & POLICY DECISION", "desc": "immutable audit vault · telemetry · admission control", "x": 20, "y": 435, "w": 1080, "h": 115, "fill": "#422006", "title_color": "#fdba74"},
    ],
    "components": [
        # Tier 1 Components (Ingress & Demand)
        {"x": 55, "y": 88, "w": 180, "h": 45, "name": "Client Ingress", "detail": "TLS 1.3 · Anycast ALB", "stroke": "#38bdf8"},
        {"x": 320, "y": 88, "w": 180, "h": 45, "name": "Identity Boundary", "detail": "OIDC · Workload Identity", "stroke": "#38bdf8"},
        {"x": 585, "y": 88, "w": 205, "h": 45, "name": "Workload Dispatch", "detail": "Rate limiting · Concurrency", "stroke": "#38bdf8"},
        {"x": 855, "y": 88, "w": 205, "h": 45, "name": "Regional Context", "detail": "Residency · Quotas", "stroke": "#38bdf8"},

        # Tier 2 Components - Row 1 (Core Services & Platform)
        {"x": 55, "y": 220, "w": 215, "h": 65, "name": "Cloud Run Services", "detail": "Scale-to-zero · Sandboxed", "stroke": "#22c55e"},
        {"x": 330, "y": 220, "w": 215, "h": 65, "name": "GKE Microservices", "detail": "Autopilot · Pod Packing", "stroke": "#22c55e"},
        {"x": 610, "y": 220, "w": 205, "h": 65, "name": "Database Tier", "detail": "Cloud SQL / Spanner HA", "stroke": "#22c55e"},
        {"x": 860, "y": 220, "w": 200, "h": 65, "name": "Analytics Engine", "detail": "BigQuery · Partitioned", "stroke": "#22c55e"},

        # Tier 2 Components - Row 2 (Telemetry & Security State)
        {"x": 170, "y": 320, "w": 250, "h": 52, "name": "Telemetry & Observability", "detail": "Cloud Logging · Trace · Metrics", "stroke": "#f59e0b"},
        {"x": 590, "y": 320, "w": 290, "h": 52, "name": "Security & Cost Accounting", "detail": "KMS · Cloud Armor · FinOps Scope", "stroke": "#f59e0b"},

        # Tier 3 Components (Policy & Decision Guardrails)
        {"x": 220, "y": 468, "w": 280, "h": 58, "name": "Policy & Decision Matrix", "detail": "Org Policies · IAM Invariants", "stroke": "#fdba74"},
        {"x": 620, "y": 468, "w": 280, "h": 58, "name": "Enforced Verification Gate", "detail": "SLO · Automated Rollback", "stroke": "#fdba74"},
    ],
    "flows": [
        # Tier 1 Horizontal Transitions
        {"x1": 235, "y1": 110, "x2": 320, "y2": 110, "label": "auth", "type": "ok"},
        {"x1": 500, "y1": 110, "x2": 585, "y2": 110, "label": "dispatch", "type": "ok"},
        {"x1": 790, "y1": 110, "x2": 855, "y2": 110, "label": "scope", "type": "ok"},

        # Tier 1 to Tier 2 Exact Vertical Drops (x1 == x2)
        {"x1": 145, "y1": 133, "x2": 145, "y2": 220, "label": "HTTP traffic", "type": "ok"},
        {"x1": 415, "y1": 133, "x2": 415, "y2": 220, "label": "gRPC / mTLS", "type": "ok"},
        {"x1": 710, "y1": 133, "x2": 710, "y2": 220, "label": "SQL queries", "type": "ok"},
        {"x1": 960, "y1": 133, "x2": 960, "y2": 220, "label": "sync stream", "type": "warn"},

        # Tier 2 Internal Routing
        {"x1": 270, "y1": 252, "x2": 330, "y2": 252, "label": "egress", "type": "ok"},
        {"x1": 545, "y1": 252, "x2": 610, "y2": 252, "label": "persist", "type": "ok"},
        {"x1": 415, "y1": 285, "x2": 295, "y2": 320, "label": "traces", "type": "warn"},
        {"x1": 710, "y1": 285, "x2": 735, "y2": 320, "label": "audit log", "type": "ok"},
        {"x1": 420, "y1": 346, "x2": 590, "y2": 346, "label": "reconcile", "type": "ok"},

        # Tier 2 to Tier 3 Flow
        {"x1": 735, "y1": 372, "x2": 735, "y2": 468, "label": "verified audit", "type": "ok"},
        {"x1": 500, "y1": 497, "x2": 620, "y2": 497, "label": "enforce gate", "type": "ok"},
    ],
    "boundaries": [
        {"x": 35, "y": 425, "w": 1045, "h": 135, "label": "VERIFICATION BOUNDARY · INVARIANTS & POLICY GATES ENFORCED", "color": "#f59e0b"},
    ],
    "probes": [
        {"cx": 258, "cy": 233, "label": "P1: Ingress Rate & Concurrency Gate", "color": "#38bdf8"},
        {"cx": 858, "cy": 263, "label": "P2: Audit Log & Telemetry Verification", "color": "#22c55e"},
        {"cx": 1040, "cy": 133, "label": "P3: Organization Policy / Residency Check", "color": "#f59e0b"},
    ],
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
            "diagram_enabled": False,  # Set True only for a qualifying sequence/packet/lifecycle topic.
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

        # PART 4: Exactly 8 topic-adapted execution stages; acceptance follows the stage list.
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
            "accept": (
                "Save the verified execution record for the topic exit artifact, including the successful volume-mount check, "
                "the zero-secret-in-environment check, the observed failure and recovery evidence, and confirmation that all "
                "temporary resources were removed."
            )
        }
    }
]
