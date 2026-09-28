"""Part 3 field case problems for Day 58."""
from blocks_svg import FIG_58_2_INCIDENT_1_SVG, FIG_58_3_INCIDENT_2_SVG

PART3_HTML = f"""<section id="part-3" class="part">
<h2>3 · Real-world problem and solution for each topic</h2>

<article id="topic-01-problem" class="topic-card">
<h3>Cloud Storage Lifecycle Early-Deletion Spirals and POSIX Buffer Inconsistency · field case</h3>
<p><strong>Situation and impact:</strong> Brightloaf's high-frequency order processing platform deploys 60 distributed compute workers in <code>us-central1</code> that ingest customer transactions, generate structured PDF invoices and cryptographic JSON receipts, and archive them to Google Cloud Storage. During a Black Friday flash sale with 120,000 orders per minute, the downstream financial reconciliation pipeline began reporting catastrophic inconsistencies: 1,420 orders appeared in the database but had zero-byte or truncated PDF objects in Cloud Storage, while 380 orders suffered race-condition duplicate fulfillment because worker retries overwrote existing records. Simultaneously, the cloud billing dashboard reported an emergency alert: the storage account incurred $62,000 in unexpected early deletion and data retrieval surcharges within 48 hours. Month-end financial reporting was delayed by 18 hours, prompting executive escalation and immediate infrastructure audit.</p>

<p><strong>Constraints:</strong> Must achieve 100% data durability with zero truncated uploads; must enforce atomic create-if-not-exists semantics to prevent duplicate fulfillment; must eliminate early deletion and retrieval penalties; must maintain 15-minute cross-region disaster recovery RPO across <code>us-central1</code> and <code>us-east1</code> without disrupting line-rate transaction throughput.</p>

<p><strong>Diagnostic sequence and root cause:</strong></p>
<ol>
<li>Inspected the local worker VM filesystem write path:
<pre><code># Check kernel dirty page statistics on worker node:
cat /proc/meminfo | grep -E "Dirty|Writeback"

# Inspect application write logic:
# Worker was writing to /var/log/invoices/order-99124.pdf
# and immediately executing the Cloud Storage upload command before calling fsync()!</code></pre>
Kernel dirty memory hovered at 2.4 GB. When worker nodes were preempted or autoscaled down under load, uncommitted dirty pages in the Linux OS page cache were obliterated before being flushed to persistent disk, resulting in zero-byte or truncated uploads.
</li>
<li>Audited concurrency headers during object uploads:
<pre><code># Check Cloud Storage upload command parameters in worker daemon:
# Worker executed upload without generation preconditions:
gcloud storage cp /tmp/receipt-99124.json gs://brightloaf-orders-us/receipt-99124.json</code></pre>
Missing <code>--if-generation-match=0</code> preconditions allowed parallel retry threads to race and overwrite finalized order receipts without detection, breaking idempotent processing.
</li>
<li>Inspected bucket Object Lifecycle Management (OLM) rules:
<pre><code>gcloud storage buckets describe gs://brightloaf-orders-us \
  --format="yaml(lifecycle)"</code></pre>
An aggressive cost-optimization policy was active:
<pre><code>rule:
- action:
    type: SetStorageClass
    storageClass: COLDLINE
  condition:
    age: 10
    matchesStorageClass:
    - STANDARD</code></pre>
The rule demoted objects to Coldline after only 10 days of age. However, downstream billing audit queries regularly read these objects on days 15 to 30. Each read incurred a Coldline data retrieval charge ($0.02/GB), and subsequent automated monthly rollup jobs deleted the 30-day-old Coldline objects, triggering an early deletion penalty for the remaining 70 days of Coldline's 90-day minimum duration!
</li>
</ol>
<p><strong>Root cause:</strong> Applications conflated POSIX local buffer caching with durable storage, streaming files before calling <code>fdatasync()</code>. Uploads lacked generation preconditions, allowing race-condition overwrites. Furthermore, manual OLM rules aggressively demoted objects into Coldline before their access lifecycle stabilized, creating a devastating cycle of Coldline retrieval fees and 70-day early deletion penalties.</p>

<p><strong>Defensible remediation:</strong></p>
<ol>
<li>Refactored the ingestion worker to enforce POSIX <code>fdatasync()</code> prior to file handoff, or stream directly into Cloud Storage via the Cloud Storage Client Library with in-memory CRC32c validation:
<pre><code># Worker enforces synchronous buffer flush before upload:
python3 -c '
import os, sys
fd = os.open("/tmp/order-99124.pdf", os.O_WRONLY | os.O_CREAT)
os.write(fd, b"CONFIRMED_ORDER_PAYLOAD")
os.fdatasync(fd)  # Commit dirty pages to persistent block media
os.close(fd)
'</code></pre>
</li>
<li>Enforced atomic create-if-not-exists precondition on all object uploads to eliminate duplicate fulfillments:
<pre><code>gcloud storage cp /tmp/order-99124.pdf gs://brightloaf-orders-us/order-99124.pdf \
  --if-generation-match=0</code></pre>
</li>
<li>Migrated the storage bucket to a Dual-Region topology (<code>nam4</code>: <code>us-central1</code> and <code>us-east1</code>) with Turbo Replication enabled to contractually guarantee 15-minute cross-region RPO:
<pre><code>gcloud storage buckets update gs://brightloaf-orders-us \
  --enable-turbo-replication</code></pre>
</li>
<li>Removed manual OLM demotion rules and enabled <strong>Autoclass</strong> with terminal class Archive. This eliminated all manual early deletion risks and enabled zero-fee read promotions back to Standard:
<pre><code>gcloud storage buckets update gs://brightloaf-orders-us \
  --set-autoclass-terminal-storage-class=ARCHIVE</code></pre>
</li>
</ol>

{FIG_58_2_INCIDENT_1_SVG}

<p><strong>Verification:</strong> Simulated worker VM kernel preemption during peak write load: 100% of uploads either completed with verified CRC32c checksums or failed cleanly with retryable errors; zero truncated objects reached the bucket. Parallel race injection with <code>--if-generation-match=0</code> returned <code>HTTP 412 Precondition Failed</code> on the duplicate thread, preventing duplicate fulfillment. In monthly billing audits, reading 45-day-old invoices incurred $0.00 in retrieval fees due to Autoclass auto-promotion, slashing monthly storage expenses by $62,000.</p>

<p><strong>Alternative and residual risk:</strong> For extremely small payloads (&lt;128 KB), the Autoclass management fee ($0.0025 per 1,000 objects/month) should be monitored against raw storage savings; if payloads are minuscule, aggregate them into batched Parquet files prior to upload.</p>
</article>

<article id="topic-02-problem" class="topic-card">
<h3>Unlocked Compliance Archive Purge vs Irreversible Bucket Lock and Legal Holds · field case</h3>
<p><strong>Situation and impact:</strong> Brightloaf Financial Services processes credit transactions subject to SEC Rule 17a-4 and FINRA Rule 4511 compliance, requiring immutable 7-year retention of all trade records and audit logs. The engineering team deployed a dedicated archive bucket (<code>gs://brightloaf-sec-audit-prod</code>) with an unlocked 7-year retention policy (220,752,000 seconds). During a scheduled security key rotation, a compromised CI/CD service account credential with project-wide <code>roles/storage.admin</code> was exploited by an automated ransomware bot. The bot executed a bucket retention clearance command and issued bulk object deletions, purging 18 months of historical compliance ledgers. Two days later, during a routine regulatory audit inquiry, compliance officers discovered the audit records were gone. The firm was hit with an immediate SEC civil enforcement action, mandatory forensic investigation, and statutory non-compliance fines totaling $1,400,000.</p>

<p><strong>Constraints:</strong> Must guarantee mathematical, tamper-proof WORM immutability that withstands compromised administrative credentials; must support indefinite holds on active client accounts; must support litigation holds for legal subpoenas; must institute governance preventing accidental permanent lockouts (e.g. 100-year locks).</p>

<p><strong>Diagnostic sequence and root cause:</strong></p>
<ol>
<li>Queried Cloud Audit Logs to trace the deletion event:
<pre><code>gcloud logging read 'protoPayload.serviceName="storage.googleapis.com" AND protoPayload.methodName=~"storage.buckets.update|storage.objects.delete"' \
  --limit=10 \
  --format="json(protoPayload.authenticationInfo.principalEmail,protoPayload.methodName,protoPayload.request)"</code></pre>
Audit log confirmed: The service account <code>cicd-deployer@brightloaf-prod.iam.gserviceaccount.com</code> called <code>storage.buckets.update</code> with <code>retentionPolicy: null</code>, successfully clearing the retention policy because <code>retentionPolicy.isLocked</code> was <code>false</code>!
</li>
<li>Checked bucket metadata:
<pre><code>gcloud storage buckets describe gs://brightloaf-sec-audit-prod \
  --format="yaml(retentionPolicy)"</code></pre>
Output returned empty:
<pre><code>retentionPolicy: null</code></pre>
Because the retention policy had not been permanently locked with Bucket Lock, an identity with <code>storage.buckets.update</code> was technically permitted to wipe out the policy and purge the objects.
</li>
</ol>
<p><strong>Root cause:</strong> The retention policy was operating in an unlocked state, allowing an administrative identity to strip the policy. Furthermore, permissions were overly broad (service account possessed <code>roles/storage.admin</code> instead of restricted object-creator permissions), and no Event-Based Holds were applied to active account files.</p>

<p><strong>Defensible remediation:</strong></p>
<ol>
<li>Restored deleted objects from the 7-day <strong>Soft Delete</strong> recovery buffer:
<pre><code># Restore soft-deleted compliance objects:
gcloud storage objects restore gs://brightloaf-sec-audit-prod/audit-2025-*.json</code></pre>
</li>
<li>Re-applied the 7-year retention policy (220,752,000 seconds) and enabled Uniform Bucket-Level Access:
<pre><code>gcloud storage buckets update gs://brightloaf-sec-audit-prod \
  --retention-period=220752000s \
  --uniform-bucket-level-access</code></pre>
</li>
<li>Enforced Event-Based Holds on active customer ledgers and Temporary Holds on subpoenaed files:
<pre><code># Set Event-Based Hold on account records:
gcloud storage objects update gs://brightloaf-sec-audit-prod/acct-88192-ledger.json \
  --event-based-hold

# Set Temporary Hold for legal discovery:
gcloud storage objects update gs://brightloaf-sec-audit-prod/subpoena-evidence-*.json \
  --temporary-hold</code></pre>
</li>
<li>Instituted a formal dual-custody governance workflow and permanently locked the retention policy using <strong>Bucket Lock</strong>:
<pre><code># Permanent, irreversible WORM commitment:
gcloud storage buckets update gs://brightloaf-sec-audit-prod \
  --lock-retention-policy</code></pre>
</li>
<li>Applied IAM Conditions restricting retention hold modifications to legal counsel principals, and stripped <code>storage.admin</code> from all CI/CD service accounts.</li>
</ol>

{FIG_58_3_INCIDENT_2_SVG}

<p><strong>Verification:</strong> Simulated a malicious administrative attack: attempted to clear the retention policy; Cloud Storage rejected the call with <code>HTTP 400 Bad Request: Retention policy is locked and cannot be removed or reduced</code>. Attempted to delete an object under the 7-year retention window using a project owner credential; Cloud Storage rejected the deletion with <code>HTTP 403 Forbidden: Object is subject to bucket retention policy or object hold</code>. Verified 100% compliance acceptance during subsequent SEC compliance audit.</p>

<p><strong>Alternative and residual risk:</strong> Before executing <code>--lock-retention-policy</code>, always perform a mandatory 30-day soak period and tabletop review. Once locked, the bucket cannot be deleted until all contained objects expire; locking a staging bucket or applying an errant century-long duration cannot be undone by Google Cloud Support.</p>
</article>
</section>"""
print("blocks_problems.py written")
