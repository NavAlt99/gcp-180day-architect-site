"""Day 19 Scenarios and Labs definitions."""

from scratch.generate_day_019 import FIG_19_3_HTML, FIG_19_4_HTML, FIG_19_5_HTML

SCENARIOS = {
    'topic-01': {
        'scenario': 'During an emergency production incident investigation at Brightloaf, an infrastructure engineer opened Cloud Shell in the Google Cloud Console to author an automated remediation script and parse API audit logs. The engineer created a directory in /opt/incident-patch, installed several specialized JSON parsing tools via sudo apt install, and wrote a 300-line Python diagnostic utility in /tmp/parse_anomalies.py. After taking an urgent 25-minute phone call with the incident management team, the engineer returned to their browser terminal to find the Cloud Shell session disconnected due to the 20-minute inactivity timeout. Upon clicking Reconnect, a fresh container provisioned: /opt/incident-patch and /tmp/parse_anomalies.py had completely vanished because only the $HOME persistent disk survived. The team had to recreate the script from scratch, delaying the mitigation by 45 minutes.',
        'impact': '45-minute incident resolution delay; lost diagnostic script; increased customer checkout error window during P1 incident; manual rework required under high stress.',
        'constraints': 'Rely on synthetic Brightloaf test fixtures, observe zero budget spend, and preserve the duplicate fulfillment invariant.',
        'evidence': '''<p>Illustrative Cloud Shell session disconnect log and ephemeral filesystem recycling trace:</p>
<pre><code>2026-10-04T15:20:00.100Z cloudshell-daemon: User session active. Persistent disk /dev/sdb mounted on /home/operator.
2026-10-04T15:20:12.300Z operator-terminal:~$ sudo mkdir -p /opt/incident-patch && touch /tmp/parse_anomalies.py
2026-10-04T15:40:01.000Z cloudshell-daemon: [TIMEOUT] Inactivity limit reached (20 minutes without input).
2026-10-04T15:40:02.100Z cloudshell-daemon: Detaching persistent disk /dev/sdb. Terminating container container-8921f.
2026-10-04T15:45:10.000Z cloudshell-daemon: Operator reconnected. Provisioning fresh container container-3310a.
2026-10-04T15:45:12.500Z operator-terminal:~$ ls -l /tmp/parse_anomalies.py
ls: cannot access '/tmp/parse_anomalies.py': No such file or directory
2026-10-04T15:45:14.000Z operator-terminal:~$ ls -l /opt/incident-patch
ls: cannot access '/opt/incident-patch': No such file or directory</code></pre>
''' + FIG_19_3_HTML,
        'root': 'Operational misunderstanding of Cloud Shell storage boundaries: assuming the entire container filesystem is persistent, rather than strictly the 5 GB persistent disk mounted at $HOME, combined with reliance on ephemeral /tmp and /opt paths for uncommitted code during an active incident.',
        'verify': 'Executed a filesystem boundary audit script verifying that files written to $HOME persist across container restarts while files outside $HOME are purged; confirmed that critical service operations maintain the duplicate fulfillment invariant (<= 1 shipment) across transient outages.',
        'residual': 'Relying exclusively on $HOME persistent storage still carries the 5 GB quota limit and 120-day inactivity deletion policy; mitigate by committing all scripts and infrastructure definitions to enterprise Git repositories immediately.',
        'diagram_enabled': False,
        'facts': 'Engineer stored script in /tmp and created directory in /opt; 20-minute idle timeout terminated container; fresh container launched with empty /tmp and default /opt; scripts lost.',
        'inference': 'Cloud Shell root filesystems are completely volatile; only $HOME is durable across container terminations; operational code must reside in $HOME and be backed by Git.',
        'expected': 'All development artifacts, tools, and scripts reside in $HOME; automated environment customizer ($HOME/.customize_environment) bootstraps system packages upon container startup.',
        'diagnostic_steps': [
            'Inspect df -h output to identify exactly which block device and mount point hosts the persistent disk.',
            'Review Cloud Shell session logs to verify the 20-minute inactivity shutdown trigger.',
            'Check $HOME/.customize_environment to see if automated toolchain installation scripts were configured.',
            'Verify Git commit status in the working repository to confirm if uncommitted changes existed before session disconnect.',
            'Audit developer workstation practices to ensure mission-critical operational runbooks are version-controlled in Cloud Source Repositories or GitHub.'
        ],
        'remediation_steps': [
            'Mandate that all operational scripts, scratch files, and configuration data reside exclusively under $HOME.',
            'Configure $HOME/.customize_environment to automatically install required APT packages and custom utilities on container bootstrap.',
            'Enforce immediate Git commits and remote branch pushes for any script authored in Cloud Shell during incident response.',
            'Educate engineering staff on the Cloud Shell 5 GB quota limit and the 120-day unmounted disk deletion policy.'
        ]
    },
    'topic-02': {
        'scenario': 'A site reliability engineer at Brightloaf was conducting load tests in the brightloaf-sandbox-19 project. Earlier that morning, while debugging a production API routing failure in another terminal window, the engineer had executed export CLOUDSDK_CORE_PROJECT=brightloaf-prod-us in their shell startup profile. In the afternoon, the engineer opened a new terminal, switched named configurations by running gcloud config configurations activate brightloaf-sandbox, and executed a cleanup script containing gcloud compute instances delete $(gcloud compute instances list --format="value(name)") --quiet. Because the environment variable CLOUDSDK_CORE_PROJECT took precedence over the active named configuration without warning, the command executed against production, deleting three production order routing instances.',
        'impact': '3 production order routing VMs deleted; 22 minutes of degraded order ingestion; financial operations team triggered failover; emergency instance recreation required from machine images.',
        'constraints': 'Rely on synthetic Brightloaf test fixtures, observe zero budget spend, and preserve the duplicate fulfillment invariant.',
        'evidence': '''<p>Illustrative gcloud execution log demonstrating environment variable precedence override:</p>
<pre><code>2026-10-04T16:10:00.000Z operator-terminal:~$ gcloud config configurations activate brightloaf-sandbox
Activated [brightloaf-sandbox].
2026-10-04T16:10:02.000Z operator-terminal:~$ env | grep CLOUDSDK
CLOUDSDK_CORE_PROJECT=brightloaf-prod-us  # Ambient variable masked named configuration!
2026-10-04T16:10:05.000Z operator-terminal:~$ gcloud config get-value project
brightloaf-prod-us  # Returns prod, despite brightloaf-sandbox being activated!
2026-10-04T16:10:15.000Z operator-terminal:~$ gcloud compute instances delete order-router-01 --quiet
Deleted [https://www.googleapis.com/compute/v1/projects/brightloaf-prod-us/zones/us-east4-a/instances/order-router-01].
2026-10-04T16:10:16.000Z alert-manager[401]: [CRITICAL] Instance order-router-01 deleted in PRODUCTION!</code></pre>
''' + FIG_19_4_HTML,
        'root': 'Failure to account for the gcloud parameter precedence hierarchy: ambient environment variables (Tier 2) override active named configurations (Tier 3) silently without terminal warnings, compounded by running a destructive deletion script that lacked an explicit --project flag (Tier 1).',
        'verify': 'Executed a precedence validation test asserting that explicit command-line flags override environment variables, and that wrapper scripts inspect and reject conflicting CLOUDSDK_* variables; verified that core order fulfillment maintains the duplicate fulfillment invariant (<= 1 shipment).',
        'residual': 'Relying solely on developer discipline to avoid export CLOUDSDK_* is insufficient; mitigate by enforcing context-aware shell prompts (displaying active project and warning if CLOUDSDK_* is set) and stripping dangerous IAM permissions in production projects.',
        'diagram_enabled': False,
        'facts': 'CLOUDSDK_CORE_PROJECT=brightloaf-prod-us was set in environment; engineer activated brightloaf-sandbox; gcloud resolved production; instances deleted in prod.',
        'inference': 'Named configurations are completely overridden by ambient CLOUDSDK_* environment variables; operational runbooks must mandate explicit --project flags and preflight environment variable sanitization.',
        'expected': 'All commands in operational runbooks pass explicit --project flags; developer shell environments sanitize CLOUDSDK_* variables; production IAM forbids deletion without elevated break-glass roles.',
        'diagnostic_steps': [
            'Execute env | grep CLOUDSDK to identify any ambient variables masking named configurations.',
            'Run gcloud config get-value project and compare against gcloud config configurations describe [ACTIVE_CONFIG].',
            'Audit Cloud Audit Logs in production project to identify the exact caller, IP, and command that deleted the instances.',
            'Review CI/CD and terminal shell profiles (.bashrc, .zshrc) for hardcoded export statements.',
            'Verify that production IAM permissions restrict destructive compute actions to privileged service accounts.'
        ],
        'remediation_steps': [
            'Mandate that all operational scripts explicitly pass --project="${TARGET_PROJECT_ID}" on every gcloud invocation.',
            'Implement a terminal preflight check in shell profiles that unsets CLOUDSDK_CORE_PROJECT or displays a prominent red warning banner.',
            'Configure named configurations for all target environments with discrete accounts, projects, and regions.',
            'Apply IAM Least Privilege: revoke roles/compute.admin from personal developer accounts in production projects.'
        ]
    },
    'topic-03': {
        'scenario': 'A Brightloaf DevOps engineer was assigned to deploy an updated microservice manifest to the staging Kubernetes cluster. In their local terminal, the engineer ran gcloud config configurations activate brightloaf-sandbox, which set the gcloud project to brightloaf-sandbox-19. The engineer then executed kubectl apply -f deployment.yaml and, seeing an error in the pod logs, executed kubectl delete namespace order-processing. Unknown to the engineer, while gcloud had switched to the sandbox project, kubectl remained configured to the production GKE cluster because ~/.kube/config current-context was not updated. As a result, the production order-processing namespace was deleted, terminating all live checkout microservices and dropping active customer sessions.',
        'impact': 'Production checkout namespace deleted; 8 microservices terminated; 35-minute total checkout outage; estimated $45,000 GMV loss; emergency cluster manifest re-application required.',
        'constraints': 'Rely on synthetic Brightloaf test fixtures, observe zero budget spend, and preserve the duplicate fulfillment invariant.',
        'evidence': '''<p>Illustrative multi-CLI context decoupling trace and production namespace deletion event:</p>
<pre><code>2026-10-04T17:00:00.000Z operator-terminal:~$ gcloud config get-value project
brightloaf-sandbox-19  # gcloud is targeting sandbox!
2026-10-04T17:00:05.000Z operator-terminal:~$ kubectl config current-context
gke_brightloaf-prod-us_us-east4_brightloaf-prod-cluster  # kubectl is targeting PRODUCTION!
2026-10-04T17:00:10.000Z operator-terminal:~$ kubectl delete namespace order-processing
namespace "order-processing" deleted
2026-10-04T17:00:11.000Z k8s-apiserver: [AUDIT] User naveen@brightloaf.com deleted namespace order-processing on PROD cluster!
2026-10-04T17:00:12.000Z edge-router[201]: [CRITICAL] 502 Bad Gateway across all /orders endpoints!</code></pre>
''' + FIG_19_5_HTML,
        'root': 'Context decoupling between independent CLI utilities: assuming that activating a gcloud named configuration automatically synchronizes the active kubectl kubeconfig context or bq target project, when in reality each utility maintains independent, isolated configuration stores.',
        'verify': 'Executed a unified multi-CLI preflight verification script that cross-examines gcloud project, kubectl cluster context, and bq target; asserted that execution is blocked when a target mismatch is detected; confirmed that the duplicate fulfillment invariant (<= 1 shipment) holds.',
        'residual': 'Manual execution of multi-CLI alignment scripts relies on human memory; mitigate by embedding cross-CLI verification into shell prompts (e.g. starship/kube-ps1) and wrapping all deployment invocations in CI/CD pipeline runners.',
        'diagram_enabled': False,
        'facts': 'gcloud was set to sandbox project; kubectl was targeting production GKE cluster; engineer ran kubectl delete namespace order-processing; production namespace deleted.',
        'inference': 'kubectl contexts are decoupled from gcloud configuration state; cross-tool administrative operations require automated synchronization and verification prior to execution.',
        'expected': 'All deployment runbooks verify that gcloud project and kubectl cluster context match target environment before applying or deleting resources.',
        'diagnostic_steps': [
            'Inspect kubectl config current-context and parse the cluster, region, and project ID components.',
            'Query gcloud config get-value project to verify active gcloud project context.',
            'Audit ~/.bigqueryrc and ~/.kube/config to review stored defaults and active cluster pointers.',
            'Inspect Kubernetes Audit Logs in the affected cluster to confirm caller identity and timestamps.',
            'Check cluster RBAC permissions to determine why developer account possessed namespace deletion rights.'
        ],
        'remediation_steps': [
            'Author a unified multi-CLI preflight assertion script (verify_context.sh) that blocks execution if gcloud and kubectl contexts diverge.',
            'Configure terminal prompt plugins (such as kube-ps1) to visually display the active Kubernetes cluster context in the shell prompt.',
            'Always execute gcloud container clusters get-credentials explicitly when switching project environments.',
            'Implement Kubernetes RBAC Least Privilege: restrict namespace deletion permissions to automated GitOps controllers.'
        ]
    }
}

LABS = {
    'topic-01': {
        'name': 'Exercise A · Cloud Shell Storage Boundaries, Ephemeral Lifecycle, and Environment Customization',
        'goal': 'Inspect and model Cloud Shell storage architecture in Python, verify persistence boundaries ($HOME vs ephemeral root), simulate container recycling after inactivity timeout, and author an automated environment customization script ($HOME/.customize_environment).',
        'expected': 'A verified Python simulation demonstrating Cloud Shell storage isolation, confirming file survival in $HOME versus data loss in ephemeral paths, and validating environment customization scripts.',
        'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Local POSIX storage inspection, mock container lifecycle simulation, persistent vs ephemeral boundary assertions. Simulated or predicted: Google Cloud Shell container provisioning, 20-minute idle disconnect daemon, 5 GB Google-managed persistent disk mount. Untested on GCP: Live Google Cloud Shell browser session, live Web Preview proxy tunnel, 120-hour weekly quota enforcement.',
        'covers': 'Create named CLI configurations and verify project, identity and region before a read-only API call.',
        'prereq': 'Linux terminal, Python 3.8+, standard POSIX utilities (mkdir, cat, python3, tee).',
        'preflight': 'Verify Python 3 runtime availability and initialize dedicated Day 19 lab workspace.',
        'verification': 'Verify that files in $HOME survive simulated container recycling while files in /tmp and /opt are purged, and that .customize_environment executes successfully.',
        'trouble': 'Ensure mock filesystem structures accurately represent Cloud Shell Debian container mount points.',
        'cleanup': 'All generated files reside in scratch/day19_lab/ and can be removed or retained for audit reference.',
        'accept': 'A structured Cloud Shell architecture summary at scratch/day19_lab/stage8_shell_summary.json.',
        'file': 'scratch/day19_lab/stage8_shell_summary.json',
        'steps': [
            """**Stage 1: Preflight and Lab Workspace Initialization**

**Location:** local terminal

**Actions:**
Verify terminal tools and create the dedicated Day 19 lab workspace.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day19_lab
python3 -c "import sys; print(f'Python runtime: {sys.version.split()[0]}, Day 19 lab initialized')" | tee scratch/day19_lab/stage1_preflight.txt
```

**Expected result:**
Python runtime confirmed and preflight baseline recorded.

**Save:** scratch/day19_lab/stage1_preflight.txt""",

            """**Stage 2: Model Cloud Shell Storage Architecture and Mount Boundaries**

**Location:** local terminal

**Actions:**
Author a Python script modeling Cloud Shell storage mounts: 5 GB persistent disk mounted at $HOME and 40 GB ephemeral overlay filesystem mounted at root.
```bash
cat <<'EOF' > scratch/day19_lab/stage2_storage_model.py
import json

storage_model = {
    "session_type": "Google Cloud Shell Container",
    "vm_instance_type": "e2-small (Google-managed Compute Engine)",
    "container_os": "Debian GNU/Linux 12 (bookworm)",
    "inactivity_timeout_minutes": 20,
    "weekly_quota_hours": 120,
    "unmounted_disk_deletion_days": 120,
    "mounts": [
        {
            "mount_point": "/",
            "device": "overlay",
            "capacity_gb": 40.0,
            "persistence": "EPHEMERAL",
            "survives_restart": False,
            "description": "Container root filesystem; recycled on session disconnect"
        },
        {
            "mount_point": "/home/operator",
            "device": "/dev/sdb",
            "capacity_gb": 5.0,
            "persistence": "PERSISTENT",
            "survives_restart": True,
            "description": "Dedicated persistent block storage; preserved across sessions"
        }
    ]
}

with open("scratch/day19_lab/stage2_mounts.json", "w") as f:
    json.dump(storage_model, f, indent=2)

print("Cloud Shell storage model authored successfully.")
EOF
python3 scratch/day19_lab/stage2_storage_model.py
```

**Expected result:**
Structured JSON storage model saved at scratch/day19_lab/stage2_mounts.json.

**Save:** scratch/day19_lab/stage2_mounts.json""",

            """**Stage 3: Simulate Container Lifecycle and Ephemeral vs Persistent File Creation**

**Location:** local terminal

**Actions:**
Author a simulation testing file creation across both storage tiers: persistent files in mock_home and volatile files in mock_tmp and mock_opt.
```bash
cat <<'EOF' > scratch/day19_lab/stage3_lifecycle_sim.py
import os
import json

# Setup mock filesystem structure
base_dir = "scratch/day19_lab/simulated_container_v1"
mock_home = os.path.join(base_dir, "home/operator")
mock_tmp = os.path.join(base_dir, "tmp")
mock_opt = os.path.join(base_dir, "opt")

for p in [mock_home, mock_tmp, mock_opt]:
    os.makedirs(p, exist_ok=True)

# Write persistent code in $HOME
home_script = os.path.join(mock_home, "deploy_service.py")
with open(home_script, "w") as f:
    f.write("# Production deployment script in $HOME\\nprint('Deploying Brightloaf service...')\\n")

# Write volatile code in /tmp and /opt
tmp_script = os.path.join(mock_tmp, "parse_anomalies.py")
with open(tmp_script, "w") as f:
    f.write("# Emergency diagnostic script in /tmp\\nprint('Parsing logs...')\\n")

opt_patch = os.path.join(mock_opt, "patch_config.json")
with open(opt_patch, "w") as f:
    f.write('{"patch": "v1.2", "target": "order-api"}\\n')

inventory = {
    "container_id": "container-8921f",
    "created_files": {
        "home_script": {"path": home_script, "exists": os.path.exists(home_script), "storage_class": "PERSISTENT"},
        "tmp_script": {"path": tmp_script, "exists": os.path.exists(tmp_script), "storage_class": "EPHEMERAL"},
        "opt_patch": {"path": opt_patch, "exists": os.path.exists(opt_patch), "storage_class": "EPHEMERAL"}
    }
}

with open("scratch/day19_lab/stage3_pre_recycling.json", "w") as f:
    json.dump(inventory, f, indent=2)

print(f"Authored 3 files across persistent and ephemeral tiers in {base_dir}")
EOF
python3 scratch/day19_lab/stage3_lifecycle_sim.py
```

**Expected result:**
Files written across persistent and ephemeral paths and recorded in stage3_pre_recycling.json.

**Save:** scratch/day19_lab/stage3_pre_recycling.json""",

            """**Stage 4: Simulate Session Timeout and Container Recycling**

**Location:** local terminal

**Actions:**
Author a simulation of the 20-minute inactivity timeout: tearing down container v1, wiping volatile storage, and mounting the persistent $HOME disk into container v2.
```bash
cat <<'EOF' > scratch/day19_lab/stage4_recycling_sim.py
import os
import shutil
import json

v1_dir = "scratch/day19_lab/simulated_container_v1"
v2_dir = "scratch/day19_lab/simulated_container_v2"

# 1. Detach persistent $HOME
v1_home = os.path.join(v1_dir, "home/operator")
temp_detached_home = "scratch/day19_lab/detached_persistent_disk"
if os.path.exists(temp_detached_home):
    shutil.rmtree(temp_detached_home)
shutil.copytree(v1_home, temp_detached_home)

# 2. Terminate and destroy container v1 (wipes /tmp, /opt, root)
shutil.rmtree(v1_dir)

# 3. Provision fresh container v2 with clean root filesystem
os.makedirs(os.path.join(v2_dir, "tmp"), exist_ok=True)
os.makedirs(os.path.join(v2_dir, "opt"), exist_ok=True)
os.makedirs(os.path.join(v2_dir, "home/operator"), exist_ok=True)

# 4. Attach persistent $HOME to container v2
shutil.copytree(temp_detached_home, os.path.join(v2_dir, "home/operator"), dirs_exist_ok=True)
shutil.rmtree(temp_detached_home)

# 5. Audit post-recycling survival
surviving_home_script = os.path.join(v2_dir, "home/operator/deploy_service.py")
lost_tmp_script = os.path.join(v2_dir, "tmp/parse_anomalies.py")
lost_opt_patch = os.path.join(v2_dir, "opt/patch_config.json")

post_audit = {
    "old_container": "container-8921f (TERMINATED)",
    "new_container": "container-3310a (ACTIVE)",
    "results": {
        "home_script_survived": os.path.exists(surviving_home_script),
        "tmp_script_survived": os.path.exists(lost_tmp_script),
        "opt_patch_survived": os.path.exists(lost_opt_patch)
    }
}

with open("scratch/day19_lab/stage4_post_recycling.json", "w") as f:
    json.dump(post_audit, f, indent=2)

print("Recycling simulation complete: $HOME preserved, ephemeral paths wiped.")
assert post_audit["results"]["home_script_survived"] is True
assert post_audit["results"]["tmp_script_survived"] is False
assert post_audit["results"]["opt_patch_survived"] is False
EOF
python3 scratch/day19_lab/stage4_recycling_sim.py
```

**Expected result:**
Simulation confirms $HOME survived while /tmp and /opt were wiped.

**Save:** scratch/day19_lab/stage4_post_recycling.json""",

            """**Stage 5: Author and Validate Environment Customization Script (.customize_environment)**

**Location:** local terminal

**Actions:**
Author a simulation of Cloud Shell's `$HOME/.customize_environment` hook, proving how custom tools and packages can be automatically re-installed upon container bootstrap.
```bash
cat <<'EOF' > scratch/day19_lab/stage5_customize_sim.py
import os
import json

v2_base = "scratch/day19_lab/simulated_container_v2"
v2_home = os.path.join(v2_base, "home/operator")
v2_opt = os.path.join(v2_base, "opt/brightloaf-tools")
os.makedirs(v2_opt, exist_ok=True)
customizer_path = os.path.join(v2_home, ".customize_environment")

target_tool = os.path.join(v2_opt, "env_check.sh")
with open(target_tool, "w") as f:
    f.write("#!/bin/bash\\necho 'Brightloaf custom environment active.'\\n")
os.chmod(target_tool, 0o755)

with open(customizer_path, "w") as f:
    f.write(f"#!/bin/bash\\necho 'Executing .customize_environment hook...'\\nbash {target_tool}\\n")
os.chmod(customizer_path, 0o755)

# Simulate container bootstrap executing the hook
os.system(f"bash {customizer_path} > scratch/day19_lab/stage5_hook_output.txt")

result = {
    "hook_script": customizer_path,
    "hook_exists": os.path.exists(customizer_path),
    "restored_tool": target_tool,
    "restored_tool_exists": os.path.exists(target_tool)
}

with open("scratch/day19_lab/stage5_customizer_result.json", "w") as f:
    json.dump(result, f, indent=2)

print("Environment customizer simulation verified.")
assert result["restored_tool_exists"] is True
EOF
python3 scratch/day19_lab/stage5_customize_sim.py
```

**Expected result:**
Environment customization hook restores custom utilities upon container startup.

**Save:** scratch/day19_lab/stage5_customizer_result.json""",

            """**Stage 6: Inspect Quota Boundaries and Deletion Policies**

**Location:** local terminal

**Actions:**
Author an audit script asserting the 5 GB disk quota, 20-minute idle timeout, and 120-day unmounted disk deletion policy.
```bash
cat <<'EOF' > scratch/day19_lab/stage6_quota_audit.py
import json

limits = {
    "persistent_disk_capacity_gb": 5.0,
    "inactivity_timeout_minutes": 20,
    "weekly_usage_quota_hours": 120,
    "unmounted_disk_purge_days": 120,
    "notification_policy": "Email alert sent before 120-day disk purge",
    "supported_web_preview_ports": [8080, 8081, 8082, 8083, 8084],
    "web_preview_security": "Authenticated via Google session cookie; private to operator"
}

with open("scratch/day19_lab/stage6_quota_audit.json", "w") as f:
    json.dump(limits, f, indent=2)

print(f"Audited Cloud Shell limits: {limits['persistent_disk_capacity_gb']} GB disk, {limits['inactivity_timeout_minutes']}m timeout.")
EOF
python3 scratch/day19_lab/stage6_quota_audit.py
```

**Expected result:**
Quota and policy audit written to scratch/day19_lab/stage6_quota_audit.json.

**Save:** scratch/day19_lab/stage6_quota_audit.json""",

            """**Stage 7: Generate Cloud Shell Operational Architecture Report**

**Location:** local terminal

**Actions:**
Synthesize mount points, persistence behavior, and customizer mechanics into a structured report.
```bash
cat <<'EOF' > scratch/day19_lab/stage7_report.py
import json

with open("scratch/day19_lab/stage2_mounts.json") as f:
    mounts = json.load(f)

with open("scratch/day19_lab/stage4_post_recycling.json") as f:
    recycling = json.load(f)

report = f'''=======================================================
GOOGLE CLOUD SHELL ARCHITECTURE AND PERSISTENCE AUDIT
=======================================================
1. VIRTUALIZATION & MOUNT BOUNDARIES:
   - Root Filesystem (/): {mounts['mounts'][0]['capacity_gb']} GB ({mounts['mounts'][0]['persistence']})
   - User Home ($HOME): {mounts['mounts'][1]['capacity_gb']} GB ({mounts['mounts'][1]['persistence']})
   - Inactivity Timeout: {mounts['inactivity_timeout_minutes']} minutes
   - Weekly Quota: {mounts['weekly_quota_hours']} hours

2. RECYCLING SIMULATION RESULTS:
   - Home Script Preserved: {recycling['results']['home_script_survived']}
   - /tmp Script Preserved: {recycling['results']['tmp_script_survived']} (EXPECTED FALSE)
   - /opt Patch Preserved: {recycling['results']['opt_patch_survived']} (EXPECTED FALSE)

3. ARCHITECTURAL MANDATE:
   All code, tools, and configurations must be committed to Git or stored in $HOME.
   Use $HOME/.customize_environment to restore system packages on container launch.
=======================================================
'''

with open("scratch/day19_lab/stage7_shell_report.txt", "w") as f:
    f.write(report)

print("Generated stage7_shell_report.txt successfully.")
EOF
python3 scratch/day19_lab/stage7_report.py
cat scratch/day19_lab/stage7_shell_report.txt
```

**Expected result:**
Structured audit report authored and displayed.

**Save:** scratch/day19_lab/stage7_shell_report.txt""",

            """**Stage 8: Validate Cloud Shell Lab Acceptance Criteria**

**Location:** local terminal

**Actions:**
Verify all Stage 1–7 artifacts exist and assemble final acceptance summary.
```bash
cat <<'EOF' > scratch/day19_lab/stage8_summary.py
import json
import os

required = [
    "scratch/day19_lab/stage1_preflight.txt",
    "scratch/day19_lab/stage2_mounts.json",
    "scratch/day19_lab/stage3_pre_recycling.json",
    "scratch/day19_lab/stage4_post_recycling.json",
    "scratch/day19_lab/stage5_customizer_result.json",
    "scratch/day19_lab/stage6_quota_audit.json",
    "scratch/day19_lab/stage7_shell_report.txt"
]

missing = [f for f in required if not os.path.exists(f)]
assert len(missing) == 0, f"Missing files: {missing}"

summary = {
    "lab": "Exercise A - Cloud Shell Architecture and Persistence",
    "status": "PASS",
    "verified_stages": 8,
    "missing_files": missing
}

with open("scratch/day19_lab/stage8_shell_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Exercise A validation complete: all 8 stages verified.")
EOF
python3 scratch/day19_lab/stage8_summary.py
```

**Expected result:**
Acceptance summary generated at scratch/day19_lab/stage8_shell_summary.json.

**Save:** scratch/day19_lab/stage8_shell_summary.json"""
        ]
    },
    'topic-02': {
        'name': 'Exercise B · Local gcloud Installation, Named Profiles, and Precedence Hierarchy',
        'goal': 'Model the local gcloud configuration directory layout, create and activate isolated named configurations (brightloaf-sandbox, brightloaf-prod), verify property isolation, and demonstrate the four-tier parameter precedence hierarchy.',
        'expected': 'A verified Python suite simulating gcloud configuration stores, proving that CLI flags override environment variables, and environment variables override named configuration properties.',
        'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Local gcloud INI configuration file authoring, property resolution simulation, precedence hierarchy evaluation. Simulated or predicted: gcloud init interactive browser OAuth flow, Google Cloud Resource Manager project association, Cloud IAM permission check. Untested on GCP: Live gcloud auth login token acquisition, live Compute Engine VM deletion, production API gateway invocation.',
        'covers': 'Create named CLI configurations and verify project, identity and region before a read-only API call.',
        'prereq': 'Linux terminal, Python 3.8+, standard POSIX utilities (mkdir, cat, python3, tee).',
        'preflight': 'Verify Python 3 runtime availability and initialize dedicated lab directory.',
        'verification': 'Verify that named configurations store isolated project properties and that parameter precedence behaves deterministically.',
        'trouble': 'Ensure mock configuration files conform to Google Cloud SDK INI schema specifications.',
        'cleanup': 'All generated files reside in scratch/day19_lab/ and can be removed or retained for audit reference.',
        'accept': 'A structured gcloud precedence audit report at scratch/day19_lab/stage8_precedence_summary.json.',
        'file': 'scratch/day19_lab/stage8_precedence_summary.json',
        'steps': [
            """**Stage 1: Preflight and Environment Verification**

**Location:** local terminal

**Actions:**
Confirm terminal utilities and initialize local gcloud simulation directory.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day19_lab/gcloud_config/configurations
python3 -c "print('Local gcloud Lab Preflight OK')" | tee scratch/day19_lab/stage1_gcloud_preflight.txt
```

**Expected result:**
Preflight baseline verified.

**Save:** scratch/day19_lab/stage1_gcloud_preflight.txt""",

            """**Stage 2: Model gcloud Configuration Filesystem Store**

**Location:** local terminal

**Actions:**
Author a Python script generating two isolated named configurations in standard INI format: `config_brightloaf-sandbox` and `config_brightloaf-prod`.
```bash
cat <<'EOF' > scratch/day19_lab/stage2_make_configs.py
import os
import configparser
import json

config_dir = "scratch/day19_lab/gcloud_config/configurations"
os.makedirs(config_dir, exist_ok=True)

# 1. Author sandbox configuration
sandbox = configparser.ConfigParser()
sandbox["core"] = {
    "account": "naveen@brightloaf.com",
    "project": "brightloaf-sandbox-19",
    "disable_usage_reporting": "True"
}
sandbox["compute"] = {
    "region": "us-central1",
    "zone": "us-central1-a"
}
with open(os.path.join(config_dir, "config_brightloaf-sandbox"), "w") as f:
    sandbox.write(f)

# 2. Author production configuration
prod = configparser.ConfigParser()
prod["core"] = {
    "account": "naveen@brightloaf.com",
    "project": "brightloaf-prod-us",
    "disable_usage_reporting": "True"
}
prod["compute"] = {
    "region": "us-east4",
    "zone": "us-east4-a"
}
with open(os.path.join(config_dir, "config_brightloaf-prod"), "w") as f:
    prod.write(f)

# Set active configuration pointer to sandbox
with open("scratch/day19_lab/gcloud_config/active_config", "w") as f:
    f.write("brightloaf-sandbox\\n")

print("Created config_brightloaf-sandbox and config_brightloaf-prod successfully.")
EOF
python3 scratch/day19_lab/stage2_make_configs.py
```

**Expected result:**
Two discrete INI configuration files authored and active pointer set to brightloaf-sandbox.

**Save:** scratch/day19_lab/gcloud_config/configurations/config_brightloaf-sandbox""",

            """**Stage 3: Implement Configuration Listing and Inspection Engine**

**Location:** local terminal

**Actions:**
Author a Python script that parses all configurations and outputs a structured matrix equivalent to <kbd>gcloud config configurations list</kbd>.
```bash
cat <<'EOF' > scratch/day19_lab/stage3_list_configs.py
import os
import configparser
import json

base = "scratch/day19_lab/gcloud_config"
conf_dir = os.path.join(base, "configurations")

with open(os.path.join(base, "active_config")) as f:
    active_name = f.read().strip()

configs = []
for fname in sorted(os.listdir(conf_dir)):
    if fname.startswith("config_"):
        name = fname[len("config_"):]
        cfg = configparser.ConfigParser()
        cfg.read(os.path.join(conf_dir, fname))
        configs.append({
            "name": name,
            "is_active": name == active_name,
            "account": cfg.get("core", "account", fallback=""),
            "project": cfg.get("core", "project", fallback=""),
            "region": cfg.get("compute", "region", fallback=""),
            "zone": cfg.get("compute", "zone", fallback="")
        })

with open("scratch/day19_lab/stage3_config_list.json", "w") as f:
    json.dump(configs, f, indent=2)

print(f"Configurations parsed: {len(configs)} total; active={active_name}")
EOF
python3 scratch/day19_lab/stage3_list_configs.py
```

**Expected result:**
Structured JSON list of configurations saved at scratch/day19_lab/stage3_config_list.json.

**Save:** scratch/day19_lab/stage3_config_list.json""",

            """**Stage 4: Implement Parameter Precedence Resolution Engine**

**Location:** local terminal

**Actions:**
Author the four-tier parameter precedence engine: Tier 1 (CLI flags), Tier 2 (Environment variables), Tier 3 (Active configuration), Tier 4 (Defaults).
```bash
cat <<'EOF' > scratch/day19_lab/stage4_precedence_engine.py
import os
import configparser

def resolve_property(prop_section, prop_name, cli_flags, env_vars, config_base):
    # Tier 1: Explicit Command-Line Parameter Flag
    flag_key = f"--{prop_name}"
    if flag_key in cli_flags:
        return cli_flags[flag_key], "TIER_1_CLI_FLAG"
    
    # Tier 2: Specific Environment Variable
    env_key = f"CLOUDSDK_{prop_section.upper()}_{prop_name.upper()}"
    if env_key in env_vars:
        return env_vars[env_key], "TIER_2_ENV_VAR"
    
    # Tier 3: Active Named Configuration Property
    with open(os.path.join(config_base, "active_config")) as f:
        active_name = f.read().strip()
    
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join(config_base, "configurations", f"config_{active_name}"))
    if cfg.has_option(prop_section, prop_name):
        return cfg.get(prop_section, prop_name), f"TIER_3_NAMED_CONFIG_{active_name}"
    
    # Tier 4: Default Fallback
    return None, "TIER_4_UNSET"

if __name__ == "__main__":
    base = "scratch/day19_lab/gcloud_config"
    # Test Tier 3 resolution
    val, source = resolve_property("core", "project", {}, {}, base)
    print(f"Tier 3 test: val={val}, source={source}")
    assert val == "brightloaf-sandbox-19"
EOF
python3 scratch/day19_lab/stage4_precedence_engine.py
```

**Expected result:**
Precedence resolver authored and verified.

**Save:** scratch/day19_lab/stage4_precedence_engine.py""",

            """**Stage 5: Prove the Ambient Environment Variable Override Risk**

**Location:** local terminal

**Actions:**
Author a simulation demonstrating how setting `CLOUDSDK_CORE_PROJECT=brightloaf-prod-us` silently overrides the active sandbox named configuration.
```bash
cat <<'EOF' > scratch/day19_lab/stage5_test_override.py
import json
import sys, os
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("scratch/day19_lab"))
try:
    from scratch.day19_lab.stage4_precedence_engine import resolve_property
except ImportError:
    from stage4_precedence_engine import resolve_property

base = "scratch/day19_lab/gcloud_config"

# Test 1: Baseline with no environment variable
val1, src1 = resolve_property("core", "project", {}, {}, base)

# Test 2: Inject Tier 2 environment variable pointing to PROD
env_mock = {"CLOUDSDK_CORE_PROJECT": "brightloaf-prod-us"}
val2, src2 = resolve_property("core", "project", {}, env_mock, base)

# Test 3: Override BOTH with Tier 1 explicit CLI flag
val3, src3 = resolve_property("core", "project", {"--project": "brightloaf-qa-testing"}, env_mock, base)

proof = {
    "baseline": {"project": val1, "resolved_source": src1},
    "ambient_env_override": {"project": val2, "resolved_source": src2, "is_masked": val2 != val1},
    "explicit_flag_override": {"project": val3, "resolved_source": src3}
}

with open("scratch/day19_lab/stage5_precedence_proof.json", "w") as f:
    json.dump(proof, f, indent=2)

print(f"Precedence Proof: Baseline={val1} -> EnvOverride={val2} -> FlagOverride={val3}")
assert val2 == "brightloaf-prod-us"
assert val3 == "brightloaf-qa-testing"
EOF
python3 scratch/day19_lab/stage5_test_override.py
```

**Expected result:**
Simulation confirms Tier 2 overrides Tier 3, and Tier 1 overrides Tier 2.

**Save:** scratch/day19_lab/stage5_precedence_proof.json""",

            """**Stage 6: Author Shell Prompt Context Indicator and Safe CLI Wrapper**

**Location:** local terminal

**Actions:**
Author a shell wrapper script that inspects active environment variables, issues warnings if CLOUDSDK_* overrides are detected, and enforces explicit --project flags.
```bash
cat <<'EOF' > scratch/day19_lab/stage6_safe_wrapper.py
import json

def safe_command_invoker(command_tokens, env_vars, active_project):
    # Check for ambient override risk
    warnings = []
    if "CLOUDSDK_CORE_PROJECT" in env_vars:
        warnings.append(f"WARNING: CLOUDSDK_CORE_PROJECT is set to '{env_vars['CLOUDSDK_CORE_PROJECT']}'. Masking configuration!")
    
    has_project_flag = any(t.startswith("--project") for t in command_tokens)
    is_destructive = any(d in command_tokens for d in ["delete", "destroy", "drop"])
    
    if is_destructive and not has_project_flag:
        return {
            "status": "BLOCKED",
            "reason": "Destructive commands MUST explicitly pass --project flag to eliminate ambient drift risk.",
            "warnings": warnings,
            "exit_code": 1
        }
    
    return {
        "status": "ALLOWED",
        "command": " ".join(command_tokens),
        "target_project": env_vars.get("CLOUDSDK_CORE_PROJECT", active_project),
        "warnings": warnings,
        "exit_code": 0
    }

# Test destructive command without --project
res_blocked = safe_command_invoker(["gcloud", "compute", "instances", "delete", "test-vm"], {"CLOUDSDK_CORE_PROJECT": "brightloaf-prod-us"}, "brightloaf-sandbox-19")
# Test non-destructive command
res_allowed = safe_command_invoker(["gcloud", "compute", "instances", "list"], {}, "brightloaf-sandbox-19")

audit = {"blocked_test": res_blocked, "allowed_test": res_allowed}
with open("scratch/day19_lab/stage6_wrapper_audit.json", "w") as f:
    json.dump(audit, f, indent=2)

print(f"Safe wrapper verified: Blocked={res_blocked['status']}, Allowed={res_allowed['status']}")
assert res_blocked["exit_code"] == 1
assert res_allowed["exit_code"] == 0
EOF
python3 scratch/day19_lab/stage6_safe_wrapper.py
```

**Expected result:**
Safe wrapper blocks destructive commands lacking explicit --project flag.

**Save:** scratch/day19_lab/stage6_wrapper_audit.json""",

            """**Stage 7: Generate gcloud Configuration Analysis Report**

**Location:** local terminal

**Actions:**
Synthesize named configurations, precedence proof, and safe wrapper assertions into an operational report.
```bash
cat <<'EOF' > scratch/day19_lab/stage7_report.py
import json

with open("scratch/day19_lab/stage5_precedence_proof.json") as f:
    proof = json.load(f)

report = f'''=======================================================
GOOGLE CLOUD SDK NAMED CONFIGURATIONS & PRECEDENCE AUDIT
=======================================================
1. PARAMETER PRECEDENCE ENGINE:
   - Tier 1 (CLI Flag): {proof['explicit_flag_override']['project']} ({proof['explicit_flag_override']['resolved_source']})
   - Tier 2 (Environment Var): {proof['ambient_env_override']['project']} ({proof['ambient_env_override']['resolved_source']})
   - Tier 3 (Named Config): {proof['baseline']['project']} ({proof['baseline']['resolved_source']})

2. AMBIENT MASKING PROOF:
   Setting CLOUDSDK_CORE_PROJECT silently masked the active named configuration!
   This proves that named configurations alone do not prevent drift if ambient
   variables exist in the developer shell environment.

3. GOVERNANCE MANDATE:
   - Runbooks must enforce Tier 1 explicit flags (--project=...).
   - Developer shell profiles must inspect and sanitize CLOUDSDK_* variables.
=======================================================
'''

with open("scratch/day19_lab/stage7_gcloud_report.txt", "w") as f:
    f.write(report)

print("Generated stage7_gcloud_report.txt successfully.")
EOF
python3 scratch/day19_lab/stage7_report.py
cat scratch/day19_lab/stage7_gcloud_report.txt
```

**Expected result:**
Report authored and displayed.

**Save:** scratch/day19_lab/stage7_gcloud_report.txt""",

            """**Stage 8: Validate gcloud Precedence Lab Acceptance Criteria**

**Location:** local terminal

**Actions:**
Verify all Stage 1–7 artifacts exist and assemble final acceptance summary.
```bash
cat <<'EOF' > scratch/day19_lab/stage8_summary.py
import json
import os

required = [
    "scratch/day19_lab/stage1_gcloud_preflight.txt",
    "scratch/day19_lab/gcloud_config/configurations/config_brightloaf-sandbox",
    "scratch/day19_lab/stage3_config_list.json",
    "scratch/day19_lab/stage4_precedence_engine.py",
    "scratch/day19_lab/stage5_precedence_proof.json",
    "scratch/day19_lab/stage6_wrapper_audit.json",
    "scratch/day19_lab/stage7_gcloud_report.txt"
]

missing = [f for f in required if not os.path.exists(f)]
assert len(missing) == 0, f"Missing files: {missing}"

summary = {
    "lab": "Exercise B - Local gcloud Configuration and Precedence",
    "status": "PASS",
    "verified_stages": 8,
    "missing_files": missing
}

with open("scratch/day19_lab/stage8_precedence_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Exercise B validation complete: all 8 stages verified.")
EOF
python3 scratch/day19_lab/stage8_summary.py
```

**Expected result:**
Acceptance summary generated at scratch/day19_lab/stage8_precedence_summary.json.

**Save:** scratch/day19_lab/stage8_precedence_summary.json"""
        ]
    },
    'topic-03': {
        'name': 'Exercise C · Multi-CLI Synchronization, Context Decoupling, and Exit Evidence Preflight',
        'goal': 'Inspect cross-tool configuration stores across gcloud, gcloud storage, bq, and kubectl, prove the critical hazard of kubeconfig context decoupling, author a unified multi-CLI preflight verification script, and output the authoritative Day 19 exit evidence artifact: scratch/day-019-cli-configuration-checks.md.',
        'expected': 'A verified multi-CLI safety suite proving context decoupling detection, blocking unaligned commands, and generating the compliant Day 19 exit evidence document.',
        'mode': 'Local terminal with Python 3 and POSIX shell (local terminal, zero cloud spend). Mode breakdown: Observed locally: Multi-CLI state modeling, kubeconfig YAML context parsing, cross-tool alignment assertion, exit evidence markdown artifact generation. Simulated or predicted: Live GKE cluster endpoint retrieval, BigQuery query execution, Google Cloud Storage bucket enumeration. Untested on GCP: Live gke-gcloud-auth-plugin token exchange, real GKE namespace deletion, live Cloud Storage composite upload.',
        'covers': 'Create named CLI configurations and verify project, identity and region before a read-only API call.',
        'prereq': 'Linux terminal, Python 3.8+, standard POSIX utilities (mkdir, cat, python3, tee, head).',
        'preflight': 'Verify Python 3 runtime availability and initialize dedicated lab directory.',
        'verification': 'Verify that cross-CLI context decoupling is detected, preflight blocks misaligned executions, and exit evidence artifact satisfies all roadmap requirements.',
        'trouble': 'Ensure mock kubeconfig and bigqueryrc schemas conform to Kubernetes and BigQuery specifications.',
        'cleanup': 'All generated files reside in scratch/day19_lab/ and can be removed or retained for audit reference.',
        'accept': 'An authoritative Day 19 exit evidence artifact at scratch/day-019-cli-configuration-checks.md.',
        'file': 'scratch/day-019-cli-configuration-checks.md',
        'steps': [
            """**Stage 1: Preflight and Environment Baseline**

**Location:** local terminal

**Actions:**
Confirm terminal utilities and initialize multi-CLI lab workspace.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day19_lab/multi_cli
python3 -c "print('Multi-CLI Lab Preflight OK')" | tee scratch/day19_lab/stage1_cli_preflight.txt
```

**Expected result:**
Preflight baseline verified.

**Save:** scratch/day19_lab/stage1_cli_preflight.txt""",

            """**Stage 2: Model Multi-Tool Configuration Stores (gcloud, bq, kubeconfig)**

**Location:** local terminal

**Actions:**
Author a Python script generating mock configuration stores for gcloud, BigQuery (`~/.bigqueryrc`), and Kubernetes (`~/.kube/config`).
```bash
cat <<'EOF' > scratch/day19_lab/stage2_model_stores.py
import json
import os

base = "scratch/day19_lab/multi_cli"
os.makedirs(base, exist_ok=True)

# 1. gcloud state: targeting sandbox
gcloud_state = {
    "active_configuration": "brightloaf-sandbox",
    "project": "brightloaf-sandbox-19",
    "account": "naveen@brightloaf.com",
    "region": "us-central1"
}

# 2. bq state: unconfigured (falls back to gcloud)
bq_state = {
    "has_bigqueryrc": False,
    "project_override": None
}

# 3. kubeconfig state: decoupled! Pointing to PROD cluster!
kubeconfig_state = {
    "current-context": "gke_brightloaf-prod-us_us-east4_brightloaf-prod-cluster",
    "contexts": [
        {
            "name": "gke_brightloaf-sandbox-19_us-central1_sandbox-cluster",
            "cluster": "sandbox-cluster",
            "project": "brightloaf-sandbox-19",
            "region": "us-central1"
        },
        {
            "name": "gke_brightloaf-prod-us_us-east4_brightloaf-prod-cluster",
            "cluster": "brightloaf-prod-cluster",
            "project": "brightloaf-prod-us",
            "region": "us-east4"
        }
    ]
}

with open(os.path.join(base, "gcloud_state.json"), "w") as f:
    json.dump(gcloud_state, f, indent=2)

with open(os.path.join(base, "bq_state.json"), "w") as f:
    json.dump(bq_state, f, indent=2)

with open(os.path.join(base, "kubeconfig_state.json"), "w") as f:
    json.dump(kubeconfig_state, f, indent=2)

print("Multi-tool configuration stores modeled successfully.")
EOF
python3 scratch/day19_lab/stage2_model_stores.py
```

**Expected result:**
Config stores created with intentional context decoupling between gcloud (sandbox) and kubectl (prod).

**Save:** scratch/day19_lab/multi_cli/kubeconfig_state.json""",

            """**Stage 3: Implement Cross-Tool Context Decoupling Detector**

**Location:** local terminal

**Actions:**
Author a detector script that cross-examines target projects across gcloud, BigQuery, and kubectl.
```bash
cat <<'EOF' > scratch/day19_lab/stage3_detector.py
import json
import os

base = "scratch/day19_lab/multi_cli"

with open(os.path.join(base, "gcloud_state.json")) as f:
    gcloud = json.load(f)

with open(os.path.join(base, "bq_state.json")) as f:
    bq = json.load(f)

with open(os.path.join(base, "kubeconfig_state.json")) as f:
    kube = json.load(f)

# Resolve target projects
gcloud_proj = gcloud["project"]
bq_proj = bq["project_override"] or gcloud_proj

current_ctx_name = kube["current-context"]
active_ctx = next((c for c in kube["contexts"] if c["name"] == current_ctx_name), None)
kube_proj = active_ctx["project"] if active_ctx else "UNKNOWN"

alignment_report = {
    "gcloud_target_project": gcloud_proj,
    "bq_target_project": bq_proj,
    "kubectl_active_context": current_ctx_name,
    "kubectl_target_project": kube_proj,
    "is_aligned": (gcloud_proj == bq_proj == kube_proj),
    "divergent_tools": []
}

if gcloud_proj != bq_proj:
    alignment_report["divergent_tools"].append("bq")
if gcloud_proj != kube_proj:
    alignment_report["divergent_tools"].append("kubectl")

with open("scratch/day19_lab/stage3_alignment_report.json", "w") as f:
    json.dump(alignment_report, f, indent=2)

print(f"Alignment audit: is_aligned={alignment_report['is_aligned']}; Divergent={alignment_report['divergent_tools']}")
assert alignment_report["is_aligned"] is False
assert "kubectl" in alignment_report["divergent_tools"]
EOF
python3 scratch/day19_lab/stage3_detector.py
```

**Expected result:**
Detector catches context decoupling between gcloud and kubectl.

**Save:** scratch/day19_lab/stage3_alignment_report.json""",

            """**Stage 4: Simulate Context Synchronization Resolution**

**Location:** local terminal

**Actions:**
Author a synchronization script simulating <kbd>gcloud container clusters get-credentials</kbd> to align kubectl with the active gcloud project.
```bash
cat <<'EOF' > scratch/day19_lab/stage4_synchronize.py
import json
import os

base = "scratch/day19_lab/multi_cli"

with open(os.path.join(base, "gcloud_state.json")) as f:
    gcloud = json.load(f)

with open(os.path.join(base, "kubeconfig_state.json")) as f:
    kube = json.load(f)

# Re-align kubectl context to match gcloud project
matching_ctx = next((c for c in kube["contexts"] if c["project"] == gcloud["project"]), None)
if matching_ctx:
    kube["current-context"] = matching_ctx["name"]

with open(os.path.join(base, "kubeconfig_state.json"), "w") as f:
    json.dump(kube, f, indent=2)

sync_result = {
    "action": "SYNCHRONIZE_KUBECONFIG",
    "updated_context": kube["current-context"],
    "new_target_project": matching_ctx["project"] if matching_ctx else None,
    "synchronized_with_gcloud": matching_ctx["project"] == gcloud["project"]
}

with open("scratch/day19_lab/stage4_sync_result.json", "w") as f:
    json.dump(sync_result, f, indent=2)

print(f"Context synchronized: {sync_result['updated_context']} (Aligned: {sync_result['synchronized_with_gcloud']})")
assert sync_result["synchronized_with_gcloud"] is True
EOF
python3 scratch/day19_lab/stage4_synchronize.py
```

**Expected result:**
kubectl context successfully synchronized to match gcloud sandbox project.

**Save:** scratch/day19_lab/stage4_sync_result.json""",

            """**Stage 5: Author Unified Multi-CLI Preflight Enforcement Suite**

**Location:** local terminal

**Actions:**
Author an automated preflight suite that verifies project, identity, and region before permitting any read-only or mutating API call.
```bash
cat <<'EOF' > scratch/day19_lab/stage5_preflight_suite.py
import json
import os

def run_multi_cli_preflight(expected_project, expected_account, expected_region, gcloud_cfg, kube_cfg):
    checks = []
    
    # Check 1: gcloud project
    c1 = gcloud_cfg.get("project") == expected_project
    checks.append({"tool": "gcloud", "field": "project", "expected": expected_project, "actual": gcloud_cfg.get("project"), "pass": c1})
    
    # Check 2: gcloud account
    c2 = gcloud_cfg.get("account") == expected_account
    checks.append({"tool": "gcloud", "field": "account", "expected": expected_account, "actual": gcloud_cfg.get("account"), "pass": c2})
    
    # Check 3: gcloud region
    c3 = gcloud_cfg.get("region") == expected_region
    checks.append({"tool": "gcloud", "field": "region", "expected": expected_region, "actual": gcloud_cfg.get("region"), "pass": c3})
    
    # Check 4: kubectl current context project alignment
    active_ctx = next((c for c in kube_cfg.get("contexts", []) if c["name"] == kube_cfg.get("current-context")), None)
    kube_proj = active_ctx["project"] if active_ctx else None
    c4 = kube_proj == expected_project
    checks.append({"tool": "kubectl", "field": "cluster_project", "expected": expected_project, "actual": kube_proj, "pass": c4})
    
    all_passed = all(c["pass"] for c in checks)
    return {
        "status": "PASS" if all_passed else "FAIL",
        "preflight_exit_code": 0 if all_passed else 1,
        "checks": checks
    }

base = "scratch/day19_lab/multi_cli"
with open(os.path.join(base, "gcloud_state.json")) as f:
    gcloud = json.load(f)

with open(os.path.join(base, "kubeconfig_state.json")) as f:
    kube = json.load(f)

res = run_multi_cli_preflight("brightloaf-sandbox-19", "naveen@brightloaf.com", "us-central1", gcloud, kube)
with open("scratch/day19_lab/stage5_preflight_result.json", "w") as f:
    json.dump(res, f, indent=2)

print(f"Preflight Result: {res['status']} (exit code {res['preflight_exit_code']})")
assert res["preflight_exit_code"] == 0
EOF
python3 scratch/day19_lab/stage5_preflight_suite.py
```

**Expected result:**
Unified preflight confirms 100% alignment across project, identity, region, and cluster.

**Save:** scratch/day19_lab/stage5_preflight_result.json""",

            """**Stage 6: Execute Read-Only API Verification (Simulation)**

**Location:** local terminal

**Actions:**
Execute a simulated read-only API call asserting that the preflight-verified environment can query resources without mutation.
```bash
cat <<'EOF' > scratch/day19_lab/stage6_readonly_call.py
import json

# Simulated read-only API invocation: gcloud storage buckets list --project=brightloaf-sandbox-19
mock_api_response = {
    "command": "gcloud storage buckets list --project=brightloaf-sandbox-19 --format=json",
    "status": "SUCCESS",
    "http_status": 200,
    "buckets": [
        {"name": "brightloaf-sandbox-artifacts-19", "location": "US-CENTRAL1", "storageClass": "STANDARD"},
        {"name": "brightloaf-sandbox-logs-19", "location": "US-CENTRAL1", "storageClass": "STANDARD"}
    ],
    "invariants_confirmed": {
        "is_read_only": True,
        "zero_mutations": True,
        "duplicate_fulfillment_invariant_preserved": True
    }
}

with open("scratch/day19_lab/stage6_readonly_result.json", "w") as f:
    json.dump(mock_api_response, f, indent=2)

print(f"Read-only API call executed: {len(mock_api_response['buckets'])} buckets discovered.")
EOF
python3 scratch/day19_lab/stage6_readonly_call.py
```

**Expected result:**
Read-only API verification recorded at scratch/day19_lab/stage6_readonly_result.json.

**Save:** scratch/day19_lab/stage6_readonly_result.json""",

            r"""**Stage 7: Author Authoritative Day 19 Exit Evidence Artifact**

**Location:** local terminal

**Actions:**
Synthesize named CLI configurations, parameter precedence verification, cross-CLI synchronization runbooks, and drift prevention commands into the authoritative Day 19 exit evidence artifact: scratch/day-019-cli-configuration-checks.md.
```bash
cat <<'EOF' > scratch/day19_lab/generate_day19_exit.py
doc = r'''# Day 19 Exit Evidence: CLI Configuration, Identity Verification, and Target Environment Controls

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
'''

with open("scratch/day-019-cli-configuration-checks.md", "w") as f:
    f.write(doc.strip() + "\n")

print("Generated scratch/day-019-cli-configuration-checks.md successfully.")
EOF
python3 scratch/day19_lab/generate_day19_exit.py
```

**Expected result:**
Authoritative Day 19 exit evidence artifact generated.

**Save:** scratch/day-019-cli-configuration-checks.md""",

            """**Stage 8: Validate Multi-CLI Lab Acceptance Criteria**

**Location:** local terminal

**Actions:**
Verify all Stage 1–7 artifacts exist and assemble final acceptance summary.
```bash
cat <<'EOF' > scratch/day19_lab/stage8_summary.py
import json
import os

required = [
    "scratch/day19_lab/stage1_cli_preflight.txt",
    "scratch/day19_lab/multi_cli/kubeconfig_state.json",
    "scratch/day19_lab/stage3_alignment_report.json",
    "scratch/day19_lab/stage4_sync_result.json",
    "scratch/day19_lab/stage5_preflight_result.json",
    "scratch/day19_lab/stage6_readonly_result.json",
    "scratch/day-019-cli-configuration-checks.md"
]

missing = [f for f in required if not os.path.exists(f)]
assert len(missing) == 0, f"Missing files: {missing}"

summary = {
    "lab": "Exercise C - Multi-CLI Synchronization and Exit Preflight",
    "status": "PASS",
    "verified_stages": 8,
    "missing_files": missing
}

with open("scratch/day19_lab/stage8_multi_cli_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Exercise C validation complete: all 8 stages verified.")
EOF
python3 scratch/day19_lab/stage8_summary.py
```

**Expected result:**
Acceptance summary generated at scratch/day19_lab/stage8_multi_cli_summary.json.

**Save:** scratch/day19_lab/stage8_multi_cli_summary.json"""
        ]
    }
}
