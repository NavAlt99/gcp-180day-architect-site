with open('scratch/day019/fig3.html') as f:
    fig3 = f.read()
with open('scratch/day019/fig4.html') as f:
    fig4 = f.read()
with open('scratch/day019/fig5.html') as f:
    fig5 = f.read()

part3 = f'''    <section class="part" id="part-3" aria-labelledby="part-3-title">
      <h2 id="part-3-title">3 · Real-world field problems and incident handling</h2>

      <article class="topic-card" id="topic-01-problem">
        <h3>Incident exercise · Cloud Shell ephemeral disk recycling wipes uncommitted emergency patch</h3>
        
        <p><strong>Symptom:</strong> During a morning peak delivery surge at 06:45 UTC, Brightloaf\\'s automated bread fulfillment queue stalled due to an unhandled serialization bug in the order dispatch worker. An on-call site reliability engineer launched Cloud Shell to compile and deploy an emergency binary patch. After compiling the binary in <code>/tmp/patch-build</code> and installing required toolchains into <code>/usr/local/bin</code>, the engineer joined a 30-minute operational conference call with franchise managers. Upon returning to the browser terminal, Cloud Shell had timed out due to 20 minutes of inactivity. When the engineer reconnected, a new container booted; <code>/tmp</code> and <code>/usr/local/bin</code> were empty, all compiled artifacts and diagnostic toolchains were gone, and the recovery had to start from scratch.</p>

        <p><strong>Operational and business constraints:</strong> Brightloaf operates on strict morning delivery Service Level Objectives (SLOs), requiring orders received by 06:00 to be dispatched to bakery distribution trucks by 07:30. Every 15-minute delay risks franchise delivery window penalties of $25,000 across 32 regional fulfillment centers. Furthermore, any hotfix applied to the fulfillment processor must strictly preserve the architectural invariant that replaying an order event never triggers duplicate physical baking batches or double-fulfills an order.</p>

        <p><strong>Evidence:</strong> Inspecting the newly reincarnated Cloud Shell instance revealed that the container ID had changed and uptime was less than 60 seconds:</p>
        <pre><code class="language-bash">$ uptime
 07:22:14 up 1 min,  1 user,  load average: 0.12, 0.08, 0.02
$ ls -la /tmp/patch-build
ls: cannot access &#39;/tmp/patch-build&#39;: No such file or directory
$ which custom-dispatch-builder
custom-dispatch-builder not found
$ df -hT /home/$USER /tmp
Filesystem     Type   Size  Used Avail Use% Mounted on
/dev/sdb       ext4   4.8G  1.2G  3.4G  27% /home/dev_brightloaf_com
tmpfs          tmpfs  2.0G     0  2.0G   0% /tmp</code></pre>

        <p><strong>Root cause:</strong> The engineer treated Cloud Shell as a persistent virtual workstation rather than an ephemeral container. The root filesystem (<code>/</code>), system directories (<code>/usr/local</code>), and scratch storage (<code>/tmp</code>) reside on temporary container overlay and memory mounts that are discarded when the Cloud Shell session watchdog triggers the 20-minute idle termination. Only the 5&nbsp;GB volume mounted at <code>/home/$USER</code> is persistent.</p>

        <p><strong>Diagnostic sequence (5 steps):</strong></p>
        <ol>
          <li><strong>Audit filesystem mount hierarchy:</strong> Execute <code>df -hT</code> to verify the exact device and mount point boundaries between ephemeral <code>tmpfs</code> overlays and the persistent disk backing <code>/home/$USER</code>.</li>
          <li><strong>Check container lifecycle and uptime markers:</strong> Run <code>uptime</code> and examine <code>/var/log/dmesg</code> to determine whether a container restart occurred during the idle period.</li>
          <li><strong>Identify uncommitted build artifacts:</strong> Compare persistent repository checkouts under <code>/home/$USER/workspace/</code> against references to <code>/tmp</code> in local shell history.</li>
          <li><strong>Codify container bootstrap automation:</strong> Author an initialization script at <code>/home/$USER/.customize_environment</code> to automate any required system packages upon container provisioning.</li>
          <li><strong>Execute order replay invariant test:</strong> Before deploying the compiled hotfix to production, run a dry-run replay test using synthetic order payloads, verifying that the database fulfillment table with a unique order ID constraint explicitly rejects duplicate processing attempts.</li>
        </ol>

        <p><strong>Defensible solution:</strong> Re-establish the hotfix build entirely within <code>/home/$USER/workspace/hotfix-build/</code>. Create an automated environment customization script at <code>/home/$USER/.customize_environment</code> with executable permissions, ensuring that required build toolchains are automatically installed as root if the container is recycled. Finally, implement an end-to-end integration test verifying that order replays reject duplicate fulfillment records.</p>

        <p><strong>Verification:</strong> Terminate the Cloud Shell container explicitly using the Cloud Console menu, re-open the terminal, and verify that the build environment auto-provisions and that compiled binaries in <code>~/workspace</code> remain intact:</p>
        <pre><code class="language-bash">$ ls -la /home/$USER/workspace/hotfix-build/bin/order-dispatcher
-rwxr-xr-x 1 dev_brightloaf_com dev_brightloaf_com 18452240 Sep 27 07:28 /home/$USER/workspace/hotfix-build/bin/order-dispatcher
$ python3 /home/$USER/workspace/hotfix-build/tests/test_fulfillment_dedup.py
[TEST] Replaying order payload ID: ORD-99281-REPLAY
[TEST] First delivery dispatch: 200 OK (Fulfillment recorded)
[TEST] Second delivery dispatch: 409 Conflict (Duplicate order_id rejected by DB constraint)
[PASS] Invariant verified: Fulfillment count == 1</code></pre>

        <p><strong>Residual risk:</strong> While user files in <code>/home/$USER</code> survive session timeouts, Cloud Shell imposes a hard 50-hour weekly quota and an absolute 12-hour session cutoff. If an operator exceeds 50 hours of usage within a rolling seven-day window, Cloud Shell access will be blocked until the quota clears, requiring local workstation failover procedures.</p>

{fig3}

      </article>

      <article class="topic-card" id="topic-02-problem">
        <h3>Incident exercise · Ambient environment variable overrides gcloud named configuration</h3>
        
        <p><strong>Symptom:</strong> A DevOps engineer opened a terminal window on their workstation to execute a routine staging cleanup script intended to purge ephemeral test storage buckets and reset staging database fixtures. The engineer ran the configuration activation command to switch to the <code>brightloaf-dev</code> named configuration and verified that the profile was marked active. However, when the cleanup script executed, it wiped the <strong>production</strong> order replay staging bucket, destroying thousands of archived payment reconciliation receipts.</p>

        <p><strong>Operational and business constraints:</strong> Brightloaf must maintain complete payment reconciliation logs for seven years to comply with financial auditing regulations and franchise settlement agreements. An outage that destroys production reconciliation buckets forces manual payment reconstruction, delaying weekly franchisee disbursement checks and incurring external audit penalties. Critically, during bucket restoration and re-ingestion, the order fulfillment engine must ensure that previously processed orders are not re-executed by downstream automated bakery systems.</p>

        <p><strong>Evidence:</strong> Running diagnostic inspections inside the active shell revealed an active configuration targeting development, but an ambient environment variable pointing directly to production:</p>
        <pre><code class="language-bash">$ gcloud config configurations list
NAME            IS_ACTIVE  ACCOUNT                    PROJECT              COMPUTE_DEFAULT_ZONE  COMPUTE_DEFAULT_REGION
brightloaf-dev  True       dev@brightloaf.com         brightloaf-dev-9182  us-central1-a          us-central1
brightloaf-prod False      deployer@brightloaf.com    brightloaf-prod-001  us-central1-b          us-central1

$ env | grep CLOUDSDK
CLOUDSDK_CORE_PROJECT=brightloaf-prod-001

$ gcloud config get-value project
Your active configuration is: [brightloaf-dev]
brightloaf-prod-001</code></pre>

        <p><strong>Root cause:</strong> Earlier that morning, the engineer had executed a CI debug script in the same terminal session that contained <code>export CLOUDSDK_CORE_PROJECT=brightloaf-prod-001</code>. In <code>gcloud</code>\\'s property precedence ladder, Tier 2 environment variables silently take precedence over Tier 3 active named configuration profiles. When the cleanup script ran the <code>gcloud</code> storage remove command without an explicit <code>--project</code> flag, the command resolved <code>brightloaf-prod-001</code> despite the active profile indicating <code>brightloaf-dev</code>.</p>

        <p><strong>Diagnostic sequence (5 steps):</strong></p>
        <ol>
          <li><strong>Interrogate active profile vs effective property resolution:</strong> Compare the output of the configuration list command against the effective project returned by the <code>gcloud</code> project query command.</li>
          <li><strong>Audit process environment variables:</strong> Search for active <code>CLOUDSDK_*</code> exports in the current shell environment using <code>env | grep CLOUDSDK</code>.</li>
          <li><strong>Trace CLI precedence resolution:</strong> Correlate the observed project ID against the 4-tier precedence engine (Flags &gt; Env Vars &gt; Named Config &gt; Defaults).</li>
          <li><strong>Sanitize environment and implement safety guard:</strong> Author a shell wrapper (<code>gcloud-safe-exec.sh</code>) that purges ambient <code>CLOUDSDK_*</code> variables and enforces target project validation before executing mutating commands.</li>
          <li><strong>Verify database fulfillment invariant during reconciliation recovery:</strong> Replay archived order records from database change-data-capture logs, verifying that the unique primary key constraint on order fulfillment IDs prevents any double-fulfillment during the data recovery window.</li>
        </ol>

        <p><strong>Defensible solution:</strong> Unset the leaked environment variable immediately using <code>unset CLOUDSDK_CORE_PROJECT</code>. Configure the shell prompt (<code>PS1</code>) to evaluate and display the effective resolved project dynamically on every command line. Refactor all administrative scripts to pass explicit Tier 1 flags (<code>--project=&quot;$TARGET_PROJECT&quot;</code>) or include an automated preflight assertion halting execution if the resolved project does not match the script\\'s intended scope.</p>

        <p><strong>Verification:</strong> Test the safety guard script with an intentional environment variable injection and verify that execution is halted with an explicit error before any cloud API call is made:</p>
        <pre><code class="language-bash">$ export CLOUDSDK_CORE_PROJECT=brightloaf-prod-001
$ ./gcloud-safe-exec.sh --expected-project brightloaf-dev-9182 -- gcloud storage ls
[GUARD ERROR] Environment variable CLOUDSDK_CORE_PROJECT overrides active profile!
[GUARD ERROR] Target: brightloaf-prod-001 | Expected: brightloaf-dev-9182
[ABORT] Mutating execution halted before API dispatch. Exit Code: 1

$ unset CLOUDSDK_CORE_PROJECT
$ ./gcloud-safe-exec.sh --expected-project brightloaf-dev-9182 -- gcloud storage ls
[GUARD CHECK] Active Project: brightloaf-dev-9182 | Expected: brightloaf-dev-9182
[GUARD CHECK] No conflicting CLOUDSDK environment variables detected.
gs://brightloaf-dev-temp-bucket/</code></pre>

        <p><strong>Residual risk:</strong> While wrapper scripts and shell prompt indicators prevent manual mistakes, team members running unmonitored ad-hoc commands without wrappers can still introduce silent overrides. Organization policies restricting service account permissions per workstation are required for comprehensive defense-in-depth.</p>

{fig4}

      </article>

      <article class="topic-card" id="topic-03-problem">
        <h3>Incident exercise · Kubectl context decoupling routes staging deployment to production GKE cluster</h3>
        
        <p><strong>Symptom:</strong> A Brightloaf release engineer prepared to test an experimental release of the bakery order fulfillment microservice featuring aggressive multi-threaded order queue consumption and a disabled Redis deduplication cache. The engineer ran the configuration activation command to set the <code>gcloud</code> active project to <code>brightloaf-staging</code> and confirmed with Compute Engine VM listing commands that the active project was indeed staging. The engineer then ran the <code>kubectl</code> manifest deployment command. Within minutes, production bakery dispatch alerts fired: live orders were experiencing race conditions, customer support was flooded with duplicate baking reports, and the production fulfillment service had been overwritten with the staging container image.</p>

        <p><strong>Operational and business constraints:</strong> Brightloaf\\'s operational core invariant mandates that no order can ever result in multiple physical fulfillment dispatches, regardless of network retries, pod restarts, or concurrent consumer threads. A deployment that disables deduplication caching poses an immediate threat of over-baking and inventory destruction across regional facilities.</p>

        <p><strong>Evidence:</strong> Checking the Kubernetes context revealed that while <code>gcloud</code> was targeting staging, <code>kubectl</code>\\'s current context remained tethered to the production cluster:</p>
        <pre><code class="language-bash">$ gcloud config get-value project
brightloaf-staging-4029

$ kubectl config current-context
gke_brightloaf-prod-001_us-central1_brightloaf-prod-cluster

$ kubectl get pods -l app=fulfillment-dispatcher -o wide
NAME                                     READY   STATUS    RESTARTS   AGE   NODE
fulfillment-dispatcher-78c8df689-x8q2l   1/1     Running   0          3m    gke-brightloaf-prod-pool-1</code></pre>

        <p><strong>Root cause:</strong> The engineer operated under the mistaken assumption that switching the active Google Cloud CLI project automatically switches the Kubernetes context. In reality, <code>kubectl</code> operates independently, resolving cluster endpoints and credentials exclusively from <code>~/.kube/config</code>. Changing the active <code>gcloud</code> project does not touch the <code>current-context</code> field in <code>~/.kube/config</code>.</p>

        <p><strong>Diagnostic sequence (5 steps):</strong></p>
        <ol>
          <li><strong>Audit current kubectl context against gcloud profile:</strong> Compare the <code>kubectl</code> context inspection command against the <code>gcloud</code> project query command to detect context drift.</li>
          <li><strong>Inspect active GKE deployment image and replicas:</strong> Run the <code>kubectl</code> JSONPath image query command to verify the exact image running in the cluster.</li>
          <li><strong>Perform emergency rollback:</strong> Execute a rollout undo command on the production deployment to reinstate the certified stable image immediately.</li>
          <li><strong>Verify database-level fulfillment idempotency defense:</strong> Inspect the PostgreSQL database logs to confirm that the row-level lock (<code>SELECT ... FOR UPDATE</code>) and primary key constraint on <code>order_id</code> blocked concurrent duplicate inserts despite the disabled application cache.</li>
          <li><strong>Implement synchronized multi-CLI context switcher:</strong> Create an automated context synchronization tool (<code>verify-cloud-context.py</code>) that validates that the active <code>gcloud</code> project matches the GKE cluster project embedded in the <code>kubectl</code> context before allowing deployments.</li>
        </ol>

        <p><strong>Defensible solution:</strong> Immediately execute a rollback on the production Kubernetes deployment using an explicit context parameter to restore the certified image. Synchronize the local kubeconfig using the cluster credential retrieval command. Establish an automated deployment gate that requires explicit context flags or fails if <code>kubectl</code>\\'s current context project does not match the intended deployment target.</p>

        <p><strong>Verification:</strong> Confirm that the production pods have returned to the stable version, and run the multi-context verification tool to prove that context mismatches are rejected:</p>
        <pre><code class="language-bash">$ kubectl --context=gke_brightloaf-prod-001_us-central1_brightloaf-prod-cluster rollout undo deployment/fulfillment-dispatcher
deployment.apps/fulfillment-dispatcher rolled back

$ kubectl --context=gke_brightloaf-prod-001_us-central1_brightloaf-prod-cluster get deployment fulfillment-dispatcher
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
fulfillment-dispatcher   8/8     8            8           42d

$ python3 scripts/verify-cloud-context.py --require-project brightloaf-staging-4029
[CHECK] gcloud active project: brightloaf-staging-4029
[CHECK] kubectl current context: gke_brightloaf-prod-001_us-central1_brightloaf-prod-cluster
[MISMATCH ERROR] kubectl context points to brightloaf-prod-001 while gcloud is set to brightloaf-staging-4029!
[ABORT] Deployment aborted to prevent cross-project cluster mutation. Exit Code: 1</code></pre>

        <p><strong>Residual risk:</strong> Developers switching contexts across multiple terminal tabs can still experience drift if one tab executes credential updates while another relies on an outdated terminal buffer. Employing terminal status line plugins that display both <code>gcloud</code> project and <code>kubectl</code> context is strongly advised.</p>

{fig5}

      </article>
    </section>
'''

with open('scratch/day019/part3.html', 'w') as f:
    f.write(part3)

print('Part 3 written, length:', len(part3))
