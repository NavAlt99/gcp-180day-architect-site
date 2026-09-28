with open('scratch/day021/fig3.html') as f:
    fig3 = f.read()
with open('scratch/day021/fig4.html') as f:
    fig4 = f.read()
with open('scratch/day021/fig5.html') as f:
    fig5 = f.read()

part3 = """    <section class="part" id="part-3" aria-labelledby="part-3-title">
      <h2 id="part-3-title">3 · Real-world field problems and incident handling</h2>

      <article class="topic-card" id="topic-01-problem">
        <h3>Incident exercise · Rogue project creation outside organization node bypasses security baseline</h3>
        
        <p><strong>Symptom:</strong> During a quarterly security audit, Brightloaf's central cybersecurity team discovered an active PostgreSQL database instance exposed directly to the public internet on port 5432, containing mirrored franchise order telemetry and customer store coordinates. The instance was not listed in central asset inventories, audit log streams to the corporate SIEM were missing, and the project owner was listed as an external contractor's personal Gmail account who had departed the organization three weeks prior.</p>

        <p><strong>Operational and business constraints:</strong> Brightloaf must maintain strict compliance with franchise privacy agreements and ISO 27001 standards. Any infrastructure hosting customer order data must enforce the corporate baseline: zero public IP access, centralized audit log ingestion, and mandatory customer-managed encryption keys. Crucially, when reconciling orders mirrored to this external database back into the central order ledger, the fulfillment processor must ensure that no orders are re-dispatched to commercial baking lines.</p>

        <p><strong>Evidence:</strong> Inspecting the rogue project using administrative CLI calls revealed that it had no parent organization and sat outside corporate policy boundaries:</p>
        <pre><code class="language-bash">$ gcloud projects describe brightloaf-analytics-shadow
createTime: '2026-08-10T14:22:19.491Z'
lifecycleState: ACTIVE
name: Brightloaf Analytics Shadow
parent: null
projectId: brightloaf-analytics-shadow
projectNumber: '482910481920'

$ gcloud org-policies list --project=brightloaf-analytics-shadow
Listed 0 items.

$ gcloud compute instances describe shadow-db-node --zone=us-central1-a --format="get(networkInterfaces[0].accessConfigs[0].natIP)"
35.192.44.182</code></pre>

        <p><strong>Root cause:</strong> The contractor provisioned the project using an unmanaged personal Google identity rather than an authenticated corporate Cloud Identity account (<code>@brightloaf.com</code>). Because the project was created without specifying an Organization parent, it operated as an unmanaged island. The corporate Organization Policy restricting external IP assignments (<code>constraints/compute.vmExternalIpAccess</code>) and the aggregated Cloud Audit Log sink never applied to the standalone project.</p>

        <p><strong>Diagnostic sequence (5 steps):</strong></p>
        <ol>
          <li><strong>Interrogate project lineage and parent container:</strong> Execute project inspection commands to verify whether the <code>parent</code> field references <code>organizations/892019481029</code> or evaluates to <code>null</code>.</li>
          <li><strong>Audit active organization policies:</strong> Check effective constraint enforcement across the project to confirm policy inheritance status.</li>
          <li><strong>Inspect network ingress boundaries:</strong> Identify all compute instances and database instances possessing public NAT IP addresses.</li>
          <li><strong>Execute project migration into corporate organization:</strong> Initiate a project move into the corporate Organization node under a quarantined folder using Resource Manager project move operations.</li>
          <li><strong>Validate fulfillment transaction deduplication during data recovery:</strong> Replay buffered order transaction logs from the contractor's database into the core fulfillment system, verifying that the database primary key constraint on <code>order_id</code> halts duplicate baking tickets.</li>
        </ol>

        <p><strong>Defensible solution:</strong> Have the Cloud Identity Super Administrator claim ownership of the contractor's project by linking billing and initiating a project move into <code>organizations/892019481029</code> under <code>folders/quarantine</code>. Once moved, the inherited corporate organization policies immediately block public IP assignments. Reconfigure firewalls to remove the public IP, redirect traffic over Private Service Connect, and bind the project to the centralized audit logging sink.</p>

        <p><strong>Verification:</strong> Verify that the project now reports the corporate Organization as its parent, that external IP policies are enforced, and that reconciliation replays preserve single fulfillment:</p>
        <pre><code class="language-bash">$ gcloud projects describe brightloaf-analytics-shadow --format="yaml(parent)"
parent:
  id: '892019481029'
  type: organization

$ gcloud compute instances describe shadow-db-node --zone=us-central1-a --format="get(networkInterfaces[0].accessConfigs)"
[]

$ python3 scripts/reconcile_shadow_orders.py
[RECONCILE] Processing 450 orders from shadow analytics database...
[RECONCILE] Dispatched 12 new unfulfilled orders.
[RECONCILE] Caught 438 duplicate order IDs (DB UNIQUE constraint triggered).
[RECONCILE] Duplicate baking dispatches suppressed: 438.
[ASSERTION] Invariant Verified: Total Physical Fulfillments == 1 per order. Status: PASS.</code></pre>

        <p><strong>Residual risk:</strong> Moving a project between organization hierarchies can temporarily interrupt IAM service account authentications if service accounts rely on cross-project bindings tied to old billing identities. Perform migrations during scheduled maintenance windows.</p>

__FIG3__

      </article>

      <article class="topic-card" id="topic-02-problem">
        <h3>Incident exercise · Flat folder structure leads to catastrophic IAM privilege inheritance leakage</h3>
        
        <p><strong>Symptom:</strong> At 10:15 UTC, Brightloaf's automated order dispatch service crashed with database catalog errors: <code>relation "order_fulfillments" does not exist</code>. In-flight bakery delivery dispatching halted across all 32 regional fulfillment centers. Investigation revealed that an automated integration test script running on a junior developer's workstation had executed a complete database reset command (<code>DROP TABLE order_fulfillments CASCADE;</code>) against the <strong>production</strong> database instead of staging.</p>

        <p><strong>Operational and business constraints:</strong> Bakery production runs on tight, temperature-sensitive fermentation schedules. An outage halting order dispatch risks spoiling 50,000 unbaked loaves across regional facilities. The platform must maintain total environment isolation so that developer credentials can never execute mutating actions against production infrastructure, while ensuring that the fulfillment engine recovers without double-fulfilling pending morning orders.</p>

        <p><strong>Evidence:</strong> Querying effective IAM permissions on the production project revealed that developers had full Editor access inherited from a shared parent folder:</p>
        <pre><code class="language-bash">$ gcloud projects get-ancestors brightloaf-fulfillment-prod
ID                  TYPE          NAME
brightloaf-fulfillment-prod project       brightloaf-fulfillment-prod
918274019283        folder        Order-Fulfillment
892019481029        organization  brightloaf.com

$ gcloud resource-manager folders get-iam-policy 918274019283
bindings:
- members:
  - group:developers@brightloaf.com
  role: roles/editor</code></pre>

        <p><strong>Root cause:</strong> The architecture team adopted a flat folder hierarchy where a single folder named <code>Order-Fulfillment</code> contained both <code>brightloaf-fulfillment-dev</code> and <code>brightloaf-fulfillment-prod</code>. When onboarding the development team, an administrator granted <code>roles/editor</code> on the <code>Order-Fulfillment</code> folder. Because IAM permissions in Google Cloud are strictly additive downward, every developer group member inherited full Editor privileges on the production project, completely bypassing local environment separation.</p>

        <p><strong>Diagnostic sequence (5 steps):</strong></p>
        <ol>
          <li><strong>Trace resource lineage and folder ancestry:</strong> Run ancestor discovery commands on the production project to map the entire container inheritance path.</li>
          <li><strong>Audit folder-level IAM bindings:</strong> Extract IAM policies from all parent folders to detect overly permissive role grants (e.g. <code>roles/editor</code> or <code>roles/owner</code>).</li>
          <li><strong>Restore production database from PITR snapshot:</strong> Execute Point-in-Time Recovery on the Cloud SQL instance to reinstate dropped tables to the state immediately preceding the 10:15 UTC drop.</li>
          <li><strong>Restructure folder hierarchy to Environment-First:</strong> Move production and development projects into separate, isolated top-level folders (<code>/Production</code> and <code>/Non-Production</code>).</li>
          <li><strong>Verify order replay deduplication invariant:</strong> Replay buffered order messages from the message queue, verifying that the restored fulfillment table with a unique order constraint rejects duplicate writes.</li>
        </ol>

        <p><strong>Defensible solution:</strong> Adopt an Environment-First folder hierarchy. Create two top-level sibling folders: <code>/Production</code> and <code>/Non-Production</code>. Move <code>brightloaf-fulfillment-prod</code> under <code>/Production</code> and <code>brightloaf-fulfillment-dev</code> under <code>/Non-Production</code>. Strip all mutating roles from the folder level; grant <code>roles/viewer</code> at parent folders for observability, and bind <code>roles/editor</code> exclusively to non-production leaf projects.</p>

        <p><strong>Verification:</strong> Re-run test scripts using developer credentials against the production project and confirm that access is denied with HTTP 403, while staging operations succeed:</p>
        <pre><code class="language-bash">$ gcloud compute instances list --project=brightloaf-fulfillment-prod --account=dev@brightloaf.com
ERROR: (gcloud.compute.instances.list) User [dev@brightloaf.com] does not have permission to access projects instance [brightloaf-fulfillment-prod] (HTTP 403: PERMISSION_DENIED)

$ python3 tests/test_order_dedup.py --project brightloaf-fulfillment-prod
[TEST] Replaying order: ORD-10928
[DB] Primary key order_id already exists. Duplicate fulfillment suppressed.
[PASS] Invariant Verified: fulfillment_count == 1</code></pre>

        <p><strong>Residual risk:</strong> Service accounts deployed inside CI/CD pipelines require granular scoped permissions per project rather than folder-wide access tokens to prevent automation credentials from leaking across environments.</p>

__FIG4__

      </article>

      <article class="topic-card" id="topic-03-problem">
        <h3>Incident exercise · Project name substitution breaks cross-project Pub/Sub service agent IAM grant</h3>
        
        <p><strong>Symptom:</strong> Following a landing zone Terraform deployment, Brightloaf's automated fulfillment event pipeline failed. Customer orders placed through the retail mobile app were acknowledged with HTTP 200, but regional bakeries received zero baking tickets. Cloud Monitoring alerted on thousands of messages accumulating in Pub/Sub dead-letter queues (DLQs) with error reason: <code>PERMISSION_DENIED: Cloud KMS key decryption rejected for service agent</code>.</p>

        <p><strong>Operational and business constraints:</strong> During peak morning hours, Brightloaf dispatches 3,000 orders every 15 minutes. Dead-letter queue buildup delays delivery schedules, backing up supply chains. When draining and replaying the accumulated DLQ messages, the system must maintain the core business invariant that each order is physically fulfilled exactly once.</p>

        <p><strong>Evidence:</strong> Inspecting the Terraform IAM policy binding in source control revealed an invalid service account email constructed using the mutable project name:</p>
        <pre><code class="language-bash"># Terraform defect in main.tf
resource "google_kms_crypto_key_iam_member" "pubsub_decrypter" {
  crypto_key_id = google_kms_crypto_key.order_key.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:service-${var.project_name}@gcp-sa-pubsub.iam.gserviceaccount.com"
}
# Where var.project_name = "Brightloaf Order Prod"</code></pre>
        <pre><code class="language-bash">$ gcloud kms keys get-iam-policy order-key --location=us-central1 --keyring=order-ring
bindings: []
# IAM grant was rejected by the API because "service-Brightloaf Order Prod@..." contains spaces!</code></pre>

        <p><strong>Root cause:</strong> The Terraform module author conflated the <strong>Project Name</strong> with the <strong>Project Number</strong>. Google-managed service agents follow an immutable naming format derived strictly from the 12-digit integer Project Number (<code>service-&lt;PROJECT_NUMBER&gt;@gcp-sa-pubsub.iam.gserviceaccount.com</code>). Substituting the user-friendly project name produced an invalid email string with spaces, causing Terraform IAM deployment failures that left the Pub/Sub service agent unauthorized to decrypt Cloud KMS keys.</p>

        <p><strong>Diagnostic sequence (5 steps):</strong></p>
        <ol>
          <li><strong>Inspect dead-letter queue rejection attributes:</strong> Query Cloud Monitoring and dead-letter message metadata to confirm the exact KMS decryption failure code.</li>
          <li><strong>Audit KMS key IAM policy bindings:</strong> Interrogate the target encryption key to verify whether the Google-managed Pub/Sub service agent holds the <code>roles/cloudkms.cryptoKeyEncrypterDecrypter</code> role.</li>
          <li><strong>Resolve true immutable Project Number:</strong> Execute project inspection commands to query the 12-digit <code>projectNumber</code> attribute.</li>
          <li><strong>Correct Terraform service agent derivation:</strong> Refactor Terraform configurations to read <code>data.google_project.project.number</code> dynamically instead of using string project names.</li>
          <li><strong>Drain dead-letter queue and verify fulfillment invariant:</strong> Replay dead-lettered messages through the order processor, verifying that the database fulfillment table with unique constraints prevents any double fulfillment.</li>
        </ol>

        <p><strong>Defensible solution:</strong> Update the Terraform infrastructure configuration to reference <code>data.google_project.current.number</code>, dynamically generating the correct service agent email: <code>service-892019481029@gcp-sa-pubsub.iam.gserviceaccount.com</code>. Apply the IAM role grant to the Cloud KMS key. Trigger the Pub/Sub dead-letter redelivery workflow to drain buffered orders into the processing pipeline.</p>

        <p><strong>Verification:</strong> Confirm that the KMS key IAM policy contains the valid service agent and verify that DLQ redeliveries drain cleanly with single fulfillment:</p>
        <pre><code class="language-bash">$ gcloud kms keys get-iam-policy order-key --location=us-central1 --keyring=order-ring --format="yaml(bindings)"
bindings:
- members:
  - serviceAccount:service-892019481029@gcp-sa-pubsub.iam.gserviceaccount.com
  role: roles/cloudkms.cryptoKeyEncrypterDecrypter

$ python3 scripts/drain_dlq.py --subscription orders-sub
[DRAIN] Processing 3,000 dead-lettered order events...
[KMS] Decryption successful with key order-key.
[DISPATCH] 3,000 orders dispatched to bakery queues.
[REPLAY TEST] Replayed test message ORD-30192; caught duplicate key in DB.
[ASSERTION] Invariant Verified: All 3,000 orders fulfilled exactly once. Status: PASS.</code></pre>

        <p><strong>Residual risk:</strong> Key decryption grants take up to 60 seconds to propagate across regional KMS HSM clusters. Allow a brief propagation buffer before resuming high-throughput order publishing.</p>

__FIG5__

      </article>
    </section>
"""

part3 = part3.replace('__FIG3__', fig3).replace('__FIG4__', fig4).replace('__FIG5__', fig5)

with open('scratch/day021/part3.html', 'w') as f:
    f.write(part3)

print('Part 3 written, length:', len(part3))
