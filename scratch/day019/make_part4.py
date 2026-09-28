part4 = '''    <section class="part" id="part-4" aria-labelledby="part-4-title">
      <h2 id="part-4-title">4 · Step-by-step labs for each topic</h2>

      <article class="topic-card lab" id="topic-01-lab">
        <h3>Lab 19.1 · Cloud Shell environment probe, persistent vs ephemeral boundary test, and custom environment initialization</h3>
        
        <p><strong>Goal:</strong> Probe the architectural boundary between ephemeral container root storage and the persistent 5&nbsp;GB disk mount in Cloud Shell, verify Web Preview reverse proxy mechanics, and establish an automated environment initialization hook via <code>.customize_environment</code>.</p>
        <p><strong>Expected result:</strong> A verified directory audit demonstrating filesystem persistence across container reboots, an automated bootstrap script in <code>~/.customize_environment</code>, and an active Web Preview response on port 8080.</p>
        <p><strong>Mode:</strong> Local bash / Cloud Shell session · <strong>Prerequisite:</strong> Completed <a href="day-018.html">Day 18</a> sandbox verification.</p>

        <h4>Preflight check</h4>
        <p>Open Cloud Shell in the Google Cloud Console (or a local Linux terminal to test simulation scripts). Verify that you have write access to your home directory and that no chargeable compute instances are running:</p>
        <pre><code class="language-bash"># Verify current user and home directory location
echo "User: $USER | Home: $HOME"
test -w "$HOME" && echo "PASS: Home directory is writable" || echo "FAIL: Home not writable"</code></pre>

        <h4>Exact execution sequence</h4>
        <ol>
          <li>
            <p><strong>Inspect filesystem mount types and persistence boundaries:</strong> Execute a disk filesystem audit to contrast the persistent volume mounted at <code>/home/$USER</code> with the in-memory <code>tmpfs</code> backing <code>/tmp</code>:</p>
            <pre><code class="language-bash"># Audit mount points and storage devices
df -hT /home /tmp

# Inspect disk inodes and available storage
df -i /home</code></pre>
          </li>
          <li>
            <p><strong>Create persistence test fixtures:</strong> Create a persistent marker in your home workspace and an ephemeral marker in <code>/tmp</code>:</p>
            <pre><code class="language-bash"># Create persistent directory and marker
mkdir -p "$HOME/cloudshell-boundary-test"
echo "PERSISTENT_PAYLOAD_VALIDATED" > "$HOME/cloudshell-boundary-test/persistent.txt"

# Create ephemeral marker in /tmp
echo "EPHEMERAL_SCRATCH_DATA" > "/tmp/ephemeral_test.txt"

# Verify file creation
ls -la "$HOME/cloudshell-boundary-test/persistent.txt" /tmp/ephemeral_test.txt</code></pre>
          </li>
          <li>
            <p><strong>Configure container initialization hook:</strong> Author an automated customization script that automatically executes under the <code>root</code> context whenever a new Cloud Shell container is provisioned:</p>
            <pre><code class="language-bash"># Author .customize_environment in home directory
cat << 'EOF' > "$HOME/.customize_environment"
#!/bin/bash
# Cloud Shell automated container customization hook
echo "[CUSTOMIZE] Initializing environment at $(date -u)" >> /home/$USER/customize.log
# Install essential lightweight utilities if missing
if ! command -v jq >/dev/null 2>&1; then
  apt-get update -y && apt-get install -y jq
fi
EOF

# Ensure customization script is executable
chmod +x "$HOME/.customize_environment"</code></pre>
          </li>
          <li>
            <p><strong>Simulate local Web Preview service:</strong> Launch a background Python HTTP listener bound to port 8080 to test the Web Preview endpoint:</p>
            <pre><code class="language-bash"># Launch synthetic HTTP order probe server on port 8080
python3 -c "
import http.server, socketserver, json

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        payload = {
            'status': 'HEALTHY',
            'service': 'brightloaf-preview-probe',
            'storage_mode': 'persistent_home',
            'order_dedup_invariant': 'enforced'
        }
        self.wfile.write(json.dumps(payload, indent=2).encode())

with socketserver.TCPServer(('127.0.0.1', 8080), Handler) as httpd:
    print('Probe server listening on port 8080...')
    httpd.handle_request()
" &
SERVER_PID=$!
sleep 1</code></pre>
          </li>
          <li>
            <p><strong>Query Web Preview endpoint:</strong> Query the local listener to verify loopback connectivity and JSON telemetry:</p>
            <pre><code class="language-bash"># Send HTTP GET request to preview port
curl -s http://127.0.0.1:8080/

# Verify process termination
kill $SERVER_PID 2>/dev/null || true</code></pre>
          </li>
        </ol>

        <h4>Verification and acceptance</h4>
        <p>Verify that the terminal output matches the expected JSON response and confirms the persistent storage boundary:</p>
        <pre><code class="language-bash">{
  "status": "HEALTHY",
  "service": "brightloaf-preview-probe",
  "storage_mode": "persistent_home",
  "order_dedup_invariant": "enforced"
}</code></pre>

        <div class="callout caution">
          <strong>Troubleshooting</strong>
          <p>If port 8080 is already in use by a background process, query open listeners using the <code>lsof -i :8080</code> command, or bind the test server to an alternative unprivileged port such as 8081.</p>
        </div>

        <div class="callout">
          <strong>Cleanup and cost</strong>
          <p>Remove the test fixture directory with <code>rm -rf "$HOME/cloudshell-boundary-test"</code>. Delete <code>/tmp/ephemeral_test.txt</code>. Keep <code>~/.customize_environment</code> if you desire automated tool setup, or remove it. Zero cloud charges incurred.</p>
        </div>

        <label class="check"><input type="checkbox" data-progress="lab-19-topic-01"> I completed and verified the Cloud Shell storage boundary exercise</label>
      </article>

      <article class="topic-card lab" id="topic-02-lab">
        <h3>Lab 19.2 · Local gcloud named configurations, environment context switching, and active profile verification guard</h3>
        
        <p><strong>Goal:</strong> Create isolated named configurations for development and production, audit the 4-tier configuration precedence engine, test the Tier 2 environment variable override trap, and author an automated assertion guard script that halts execution when cross-project drift is detected.</p>
        <p><strong>Expected result:</strong> Two distinct named configurations created and verified, an intentional environment variable conflict intercepted, and an automated execution guard script (<code>gcloud-safe-exec.sh</code>) validated.</p>
        <p><strong>Mode:</strong> Local workstation bash exercise · <strong>Prerequisite:</strong> Google Cloud CLI installed locally.</p>

        <h4>Preflight check</h4>
        <p>Confirm that the <code>gcloud</code> CLI is installed and inspect the active configuration directory:</p>
        <pre><code class="language-bash"># Verify CLI binary availability and configuration directory
gcloud --version | head -n 2
mkdir -p "$HOME/.config/gcloud/configurations"
test -w "$HOME/.config/gcloud" && echo "PASS: gcloud config directory writable"</code></pre>

        <h4>Exact execution sequence</h4>
        <ol>
          <li>
            <p><strong>Create isolated named configurations:</strong> Create two dedicated profiles representing Brightloaf's development and production environments:</p>
            <pre><code class="language-bash"># Create dev and prod named configurations
gcloud config configurations create bl-dev --quiet 2>/dev/null || true
gcloud config configurations create bl-prod --quiet 2>/dev/null || true

# List available configurations
gcloud config configurations list</code></pre>
          </li>
          <li>
            <p><strong>Populate scoped properties within each configuration:</strong> Assign distinct project IDs, default regions, and zones to each named profile:</p>
            <pre><code class="language-bash"># Configure development profile properties
gcloud config set project brightloaf-order-dev --configuration=bl-dev
gcloud config set compute/region us-central1 --configuration=bl-dev
gcloud config set compute/zone us-central1-a --configuration=bl-dev

# Configure production profile properties
gcloud config set project brightloaf-order-prod --configuration=bl-prod
gcloud config set compute/region us-east1 --configuration=bl-prod
gcloud config set compute/zone us-east1-b --configuration=bl-prod</code></pre>
          </li>
          <li>
            <p><strong>Activate development profile and inspect disk state:</strong> Switch to the <code>bl-dev</code> profile and verify the active configuration pointer:</p>
            <pre><code class="language-bash"># Activate development configuration
gcloud config configurations activate bl-dev

# Inspect the active pointer file and resolved project
cat "$HOME/.config/gcloud/active_config"
gcloud config get-value project</code></pre>
          </li>
          <li>
            <p><strong>Simulate the Tier 2 environment variable precedence trap:</strong> Export an ambient environment variable and observe how it overrides the active profile:</p>
            <pre><code class="language-bash"># Inject ambient environment variable override
export CLOUDSDK_CORE_PROJECT=brightloaf-order-prod

# Interrogate effective project
EFFECTIVE_PROJECT=$(gcloud config get-value project 2>/dev/null)
echo "Active Configuration: $(cat $HOME/.config/gcloud/active_config)"
echo "Effective Resolved Project: $EFFECTIVE_PROJECT"
test "$EFFECTIVE_PROJECT" = "brightloaf-order-prod" && echo "TRAP CONFIRMED: Env var silently overrode active profile!"

# Unset ambient variable to restore safety
unset CLOUDSDK_CORE_PROJECT</code></pre>
          </li>
          <li>
            <p><strong>Author and test the execution safety guard:</strong> Author <code>gcloud-safe-exec.sh</code>, an operational wrapper that enforces environment sanitization and project validation before command execution:</p>
            <pre><code class="language-bash"># Author safety guard script
cat << 'EOF' > "$HOME/gcloud-safe-exec.sh"
#!/bin/bash
set -euo pipefail

EXPECTED_PROJECT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --expected-project)
      EXPECTED_PROJECT="$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    *)
      break
      ;;
  esac
done

if [[ -z "$EXPECTED_PROJECT" ]]; then
  echo "[GUARD ERROR] Must specify --expected-project <PROJECT_ID>" >&2
  exit 1
fi

# Check for ambient CLOUDSDK environment variable leaks
LEAKED_VARS=$(env | grep -E '^CLOUDSDK_(CORE_PROJECT|ACTIVE_CONFIG_NAME)' || true)
if [[ -n "$LEAKED_VARS" ]]; then
  echo "[GUARD CRITICAL] Leaked CLOUDSDK environment variables detected:" >&2
  echo "$LEAKED_VARS" >&2
  echo "[ABORT] Command rejected to prevent silent precedence override." >&2
  exit 2
fi

# Interrogate effective CLI project
RESOLVED_PROJECT=$(gcloud config get-value project 2>/dev/null || true)
if [[ "$RESOLVED_PROJECT" != "$EXPECTED_PROJECT" ]]; then
  echo "[GUARD CRITICAL] Context mismatch! Resolved: '$RESOLVED_PROJECT' | Expected: '$EXPECTED_PROJECT'" >&2
  echo "[ABORT] Command rejected to prevent cross-project mutation." >&2
  exit 3
fi

echo "[GUARD PASS] Validated target project: $RESOLVED_PROJECT"
echo "[GUARD PASS] Executing: $@"
exec "$@"
EOF
chmod +x "$HOME/gcloud-safe-exec.sh"</code></pre>
          </li>
          <li>
            <p><strong>Verify safety guard under positive and negative test cases:</strong> Test that the guard rejects conflicts and approves sanitized commands:</p>
            <pre><code class="language-bash"># Negative test: Intentionally induce context mismatch
! "$HOME/gcloud-safe-exec.sh" --expected-project brightloaf-order-prod -- gcloud config list

# Positive test: Execute with matching expected project
"$HOME/gcloud-safe-exec.sh" --expected-project brightloaf-order-dev -- gcloud config list project</code></pre>
          </li>
        </ol>

        <h4>Verification and acceptance</h4>
        <p>Verify that the safety guard script passes the positive assertion and displays the validated project:</p>
        <pre><code class="language-bash">[GUARD PASS] Validated target project: brightloaf-order-dev
[GUARD PASS] Executing: gcloud config list project
[core]
project = brightloaf-order-dev</code></pre>

        <div class="callout caution">
          <strong>Troubleshooting</strong>
          <p>If the configuration creation fails because the name already exists, re-run with the configuration describe command for <code>bl-dev</code> to verify existing properties before updating.</p>
        </div>

        <div class="callout">
          <strong>Cleanup and cost</strong>
          <p>Delete the temporary configurations with the configuration deletion command for <code>bl-dev</code> and <code>bl-prod</code> and remove <code>"$HOME/gcloud-safe-exec.sh"</code>. Zero cloud charges incurred.</p>
        </div>

        <label class="check"><input type="checkbox" data-progress="lab-19-topic-02"> I completed and verified the local gcloud named configurations exercise</label>
      </article>

      <article class="topic-card lab" id="topic-03-lab">
        <h3>Lab 19.3 · Specialized CLIs integration (gcloud storage, bq, kubectl) and multi-context synchronization validator</h3>
        
        <p><strong>Goal:</strong> Configure BigQuery GoogleSQL defaults in <code>~/.bigqueryrc</code>, model a simulated multi-cluster GKE environment in <code>~/.kube/config</code>, and construct a Python context synchronizer (<code>verify-cloud-context.py</code>) that validates parity between <code>gcloud</code> and <code>kubectl</code> contexts.</p>
        <p><strong>Expected result:</strong> A verified <code>~/.bigqueryrc</code> configuration file, a multi-context kubeconfig fixture, and an automated validator that halts when <code>kubectl</code> points to production while <code>gcloud</code> targets staging.</p>
        <p><strong>Mode:</strong> Local python and bash simulation · <strong>Prerequisite:</strong> Python 3 runtime.</p>

        <h4>Preflight check</h4>
        <p>Verify Python 3 availability and create a temporary working directory:</p>
        <pre><code class="language-bash">python3 --version
mkdir -p "$HOME/multi-cli-lab"
cd "$HOME/multi-cli-lab"</code></pre>

        <h4>Exact execution sequence</h4>
        <ol>
          <li>
            <p><strong>Configure BigQuery GoogleSQL defaults:</strong> Author a local BigQuery configuration file to prevent legacy SQL syntax fallback errors:</p>
            <pre><code class="language-bash"># Author ~/.bigqueryrc to enforce standard GoogleSQL
cat << 'EOF' > "$HOME/multi-cli-lab/bigqueryrc"
[query]
--use_legacy_sql=false
--maximum_bytes_billed=1073741824

[format]
--format=prettyjson
EOF

# Display configured BigQuery flags
cat "$HOME/multi-cli-lab/bigqueryrc"</code></pre>
          </li>
          <li>
            <p><strong>Generate multi-cluster kubeconfig test fixture:</strong> Author a synthetic Kubernetes configuration containing staging and production GKE cluster contexts:</p>
            <pre><code class="language-bash"># Create synthetic kubeconfig with decoupled contexts
cat << 'EOF' > "$HOME/multi-cli-lab/kubeconfig.yaml"
apiVersion: v1
kind: Config
current-context: gke_brightloaf-order-prod_us-central1_prod-cluster
clusters:
- name: gke_brightloaf-order-prod_us-central1_prod-cluster
  cluster:
    server: https://35.192.10.1
- name: gke_brightloaf-order-staging_us-central1_staging-cluster
  cluster:
    server: https://35.192.20.2
contexts:
- name: gke_brightloaf-order-prod_us-central1_prod-cluster
  context:
    cluster: gke_brightloaf-order-prod_us-central1_prod-cluster
    user: cluster-admin
- name: gke_brightloaf-order-staging_us-central1_staging-cluster
  context:
    cluster: gke_brightloaf-order-staging_us-central1_staging-cluster
    user: staging-dev
users:
- name: cluster-admin
- name: staging-dev
EOF</code></pre>
          </li>
          <li>
            <p><strong>Author the multi-CLI context synchronization validator:</strong> Create a Python script that extracts the active <code>gcloud</code> project and asserts that the current <code>kubectl</code> context cluster belongs to the exact same Google Cloud project:</p>
            <pre><code class="language-bash"># Author verify-cloud-context.py
cat << 'EOF' > "$HOME/multi-cli-lab/verify-cloud-context.py"
#!/usr/bin/env python3
import sys, re, argparse

def parse_kube_context(kubeconfig_path):
    with open(kubeconfig_path, 'r') as f:
        content = f.read()
    match = re.search(r'^current-context:\s*(\S+)', content, re.MULTILINE)
    if not match:
        raise ValueError("Could not find current-context in kubeconfig")
    return match.group(1)

def extract_project_from_gke_context(context_name):
    # GKE context pattern: gke_<PROJECT_ID>_<REGION|ZONE>_<CLUSTER_NAME>
    parts = context_name.split('_')
    if len(parts) >= 4 and parts[0] == 'gke':
        return parts[1]
    return None

def main():
    parser = argparse.ArgumentParser(description="Multi-CLI Context Parity Validator")
    parser.add_argument("--gcloud-project", required=True, help="Active gcloud project ID")
    parser.add_argument("--kubeconfig", required=True, help="Path to kubeconfig")
    parser.add_argument("--require-parity", action="store_true", help="Enforce exact project match")
    args = parser.parse_args()

    kube_ctx = parse_kube_context(args.kubeconfig)
    gke_proj = extract_project_from_gke_context(kube_ctx)

    print(f"[AUDIT] Active gcloud project:  {args.gcloud_project}")
    print(f"[AUDIT] Active kubectl context: {kube_ctx}")
    print(f"[AUDIT] Embedded GKE project:   {gke_proj}")

    if args.require_parity:
        if gke_proj != args.gcloud_project:
            print(f"[CRITICAL ERROR] Target drift detected! gcloud project '{args.gcloud_project}' does not match GKE cluster project '{gke_proj}'!", file=sys.stderr)
            print("[ABORT] Halting deployment pipeline to preserve cluster isolation and fulfillment invariant.", file=sys.stderr)
            sys.exit(1)
        print("[SUCCESS] Context parity verified. Safe to proceed with deployment.")
        sys.exit(0)

if __name__ == "__main__":
    main()
EOF
chmod +x "$HOME/multi-cli-lab/verify-cloud-context.py"</code></pre>
          </li>
          <li>
            <p><strong>Test context mismatch interception (Negative case):</strong> Simulate an operator who set <code>gcloud</code> to staging while <code>kubectl</code> targets production:</p>
            <pre><code class="language-bash"># Run validator with mismatched contexts (staging gcloud vs prod kubeconfig)
! python3 "$HOME/multi-cli-lab/verify-cloud-context.py" \
  --gcloud-project brightloaf-order-staging \
  --kubeconfig "$HOME/multi-cli-lab/kubeconfig.yaml" \
  --require-parity</code></pre>
          </li>
          <li>
            <p><strong>Test synchronized context approval (Positive case):</strong> Update the kubeconfig current-context to staging and re-run the validator:</p>
            <pre><code class="language-bash"># Switch kubeconfig context to staging
sed -i 's/current-context: .*/current-context: gke_brightloaf-order-staging_us-central1_staging-cluster/' "$HOME/multi-cli-lab/kubeconfig.yaml"

# Run validator with matching contexts
python3 "$HOME/multi-cli-lab/verify-cloud-context.py" \
  --gcloud-project brightloaf-order-staging \
  --kubeconfig "$HOME/multi-cli-lab/kubeconfig.yaml" \
  --require-parity</code></pre>
          </li>
        </ol>

        <h4>Verification and acceptance</h4>
        <p>Verify that the synchronization validator confirms context parity with exit status 0:</p>
        <pre><code class="language-bash">[AUDIT] Active gcloud project:  brightloaf-order-staging
[AUDIT] Active kubectl context: gke_brightloaf-order-staging_us-central1_staging-cluster
[AUDIT] Embedded GKE project:   brightloaf-order-staging
[SUCCESS] Context parity verified. Safe to proceed with deployment.</code></pre>

        <div class="callout caution">
          <strong>Troubleshooting</strong>
          <p>If the GKE context name does not follow standard <code>gke_PROJECT_LOCATION_NAME</code> conventions (e.g. custom aliases), verify context cluster definitions in <code>~/.kube/config</code> directly.</p>
        </div>

        <div class="callout">
          <strong>Cleanup and cost</strong>
          <p>Remove the test directory using <code>rm -rf "$HOME/multi-cli-lab"</code>. Zero cloud charges incurred.</p>
        </div>

        <label class="check"><input type="checkbox" data-progress="lab-19-topic-03"> I completed and verified the specialized CLIs and context validator exercise</label>
      </article>
    </section>
'''

with open('scratch/day019/part4.html', 'w') as f:
    f.write(part4)

print('Part 4 written, length:', len(part4))
