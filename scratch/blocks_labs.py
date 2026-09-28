"""Part 4 hands-on labs and completion section for Day 58."""

PART4_HTML = """<section id="part-4" class="part">
<h2>4 · Step-by-step labs for each topic</h2>

<article id="topic-01-lab" class="topic-card lab">
<h3>Exercise 1: Dual-Region Storage, Turbo Replication, Autoclass Tiering, and POSIX Flush Verification</h3>
<p><strong>Goal:</strong> Deploy a dual-region Cloud Storage bucket with Turbo Replication and Uniform Bucket-Level Access, enable Autoclass with terminal class Archive, configure Object Versioning and Soft Delete, test atomic create-if-not-exists generation preconditions, and benchmark POSIX buffer flushes against Cloud Storage distributed commit semantics.</p>
<p><strong>Mode:</strong> production practice · <strong>Prerequisite:</strong> Day 16, Day 37, and Day 57 exit artifacts.</p>
<ol>
<li><strong>Define Unique Bucket Variables and Environment:</strong>
<pre><code>export PROJECT_ID=$(gcloud config get-value project)
export BUCKET_NAME="brightloaf-durability-${PROJECT_ID}-d58"
export REGION_PRIMARY="us-central1"
export REGION_SECONDARY="us-east1"</code></pre>
</li>
<li><strong>Create Dual-Region Bucket with Uniform Bucket-Level Access:</strong>
<pre><code># Create dual-region bucket in US (us-central1 and us-east1):
gcloud storage buckets create gs://${BUCKET_NAME} \
  --project=${PROJECT_ID} \
  --location=nam4 \
  --default-storage-class=STANDARD \
  --uniform-bucket-level-access</code></pre>
</li>
<li><strong>Enable Turbo Replication for 15-Minute Cross-Region RPO SLA:</strong>
<pre><code># Enable Turbo Replication on dual-region bucket:
gcloud storage buckets update gs://${BUCKET_NAME} \
  --enable-turbo-replication

# Verify Turbo Replication status:
gcloud storage buckets describe gs://${BUCKET_NAME} \
  --format="yaml(rpo)"</code></pre>
</li>
<li><strong>Enable Autoclass Dynamic Lifecycle Management:</strong>
<pre><code># Configure Autoclass with terminal storage class Archive:
gcloud storage buckets update gs://${BUCKET_NAME} \
  --set-autoclass-terminal-storage-class=ARCHIVE

# Verify Autoclass configuration:
gcloud storage buckets describe gs://${BUCKET_NAME} \
  --format="yaml(autoclass)"</code></pre>
</li>
<li><strong>Enable Object Versioning and Inspect Soft Delete Configuration:</strong>
<pre><code># Enable Object Versioning:
gcloud storage buckets update gs://${BUCKET_NAME} \
  --versioning

# Verify Soft Delete retention duration (default 7 days):
gcloud storage buckets describe gs://${BUCKET_NAME} \
  --format="yaml(softDeletePolicy)"</code></pre>
</li>
<li><strong>Execute Atomic Create-If-Not-Exists Write with Generation Precondition:</strong>
<pre><code># Create synthetic order payload:
echo '{"order_id": "ORD-5801", "amount": 420.50, "status": "CONFIRMED"}' > /tmp/order-5801.json

# Upload with precondition x-goog-if-generation-match: 0:
gcloud storage cp /tmp/order-5801.json gs://${BUCKET_NAME}/order-5801.json \
  --if-generation-match=0

# Attempt duplicate upload with same precondition (simulating worker race condition):
# This command is expected to fail with HTTP 412 Precondition Failed:
gcloud storage cp /tmp/order-5801.json gs://${BUCKET_NAME}/order-5801.json \
  --if-generation-match=0 || echo "Atomic precondition successfully rejected race overwrite!"</code></pre>
</li>
<li><strong>Benchmark POSIX Kernel Page Cache Dirty Write vs fdatasync() vs Cloud Storage Ingestion:</strong>
<pre><code># Execute benchmark testing local OS cache dirty buffer vs durable flush:
python3 -c '
import os, time, sys

test_file = "/tmp/posix_durability_bench.dat"
payload = b"X" * (10 * 1024 * 1024) # 10 MB payload

# 1. POSIX asynchronous write to kernel page cache (not durable on disk):
t0 = time.perf_counter()
fd = os.open(test_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
os.write(fd, payload)
t_posix_async = time.perf_counter() - t0

# 2. POSIX explicit fdatasync() commit to physical non-volatile block device:
t1 = time.perf_counter()
os.fdatasync(fd)
os.close(fd)
t_posix_sync = time.perf_counter() - t1

print(f"POSIX async write (RAM page cache): {t_posix_async*1000:.3f} ms")
print(f"POSIX fdatasync() disk commit:      {t_posix_sync*1000:.3f} ms")
print(f"Durability latency ratio:           {t_posix_sync / max(t_posix_async, 1e-6):.1f}x")
'</code></pre>
</li>
<li><strong>Inspect Object Generation, Metageneration, and Checksums:</strong>
<pre><code># Inspect object metadata and generation identifiers:
gcloud storage objects describe gs://${BUCKET_NAME}/order-5801.json \
  --format="yaml(generation,metageneration,crc32cHash,md5Hash,storageClass)"</code></pre>
</li>
</ol>
<div class="callout success">
<strong>Expected result / acceptance</strong>
<p>The dual-region bucket in <code>nam4</code> reports <code>rpo: ASYNC_TURBO</code> with 15-minute RPO. Autoclass is active with terminal class <code>ARCHIVE</code>. The initial object upload succeeds with a distinct generation number, while the duplicate upload with <code>--if-generation-match=0</code> is rejected with <code>HTTP 412 Precondition Failed</code>, verifying atomic idempotency. The POSIX benchmark demonstrates that <code>fdatasync()</code> requires physical disk commitment latency, proving why local dirty page writes must be committed before distributed handoff.</p>
</div>
<div class="callout caution">
<strong>Troubleshooting</strong>
<p>If <code>--enable-turbo-replication</code> fails, ensure the bucket location is an authorized dual-region pair (e.g., <code>nam4</code> or <code>eur4</code>); single-region and continental multi-region buckets do not support Turbo Replication.</p>
</div>
<div class="callout">
<strong>Cleanup and cost</strong>
<p>Delete the uploaded test objects and remove the bucket after completing the exercises to prevent ongoing dual-region storage and replication billing charges.</p>
</div>
<label class="check"><input type="checkbox" data-progress="lab-58-topic-01"> I completed and checked this topic exercise</label>
</article>

<article id="topic-02-lab" class="topic-card lab">
<h3>Exercise 2: WORM Compliance Architecture: Retention Policies, Event-Based Holds, and Bucket Lock Governance</h3>
<p><strong>Goal:</strong> Deploy an isolated compliance sandbox bucket with an unlocked 1-day retention policy, test Event-Based Holds and Temporary Legal Holds, verify deletion rejections, demonstrate hold releases, and execute a formal Tabletop Design Defense for Bucket Lock governance without executing irreversible production locks.</p>
<p><strong>Mode:</strong> production practice · <strong>Prerequisite:</strong> Day 16, Day 37, and Day 57 exit artifacts.</p>
<ol>
<li><strong>Create Isolated Compliance Sandbox Bucket with 1-Day Retention Policy:</strong>
<pre><code>export COMPLIANCE_BUCKET="brightloaf-sec-sandbox-${PROJECT_ID}-d58"

# Create bucket with 1-day (86400 seconds) unlocked retention policy:
gcloud storage buckets create gs://${COMPLIANCE_BUCKET} \
  --project=${PROJECT_ID} \
  --location=us-central1 \
  --uniform-bucket-level-access \
  --retention-period=86400s</code></pre>
</li>
<li><strong>Verify Retention Policy Status and Confirm It Is Unlocked:</strong>
<pre><code>gcloud storage buckets describe gs://${COMPLIANCE_BUCKET} \
  --format="yaml(retentionPolicy)"</code></pre>
Expected output confirms <code>retentionPeriod: '86400'</code> and <code>isLocked: false</code> (permitting testing and subsequent deletion).
</li>
<li><strong>Upload Compliance Record with Event-Based Hold:</strong>
<pre><code># Create synthetic customer loan agreement:
echo '{"account_id": "ACCT-992", "status": "ACTIVE_LOAN", "origination": "2026-09-28"}' > /tmp/loan-992.json

# Upload object with Event-Based Hold enabled:
gcloud storage cp /tmp/loan-992.json gs://${COMPLIANCE_BUCKET}/loan-992.json \
  --event-based-hold

# Verify object hold state:
gcloud storage objects describe gs://${COMPLIANCE_BUCKET}/loan-992.json \
  --format="yaml(eventBasedHold,retentionExpirationTime)"</code></pre>
Notice that <code>retentionExpirationTime</code> is not yet set or remains pending, because the countdown does not tick while the event-based hold is active.
</li>
<li><strong>Attempt Object Deletion to Verify WORM Protection:</strong>
<pre><code># Attempt deletion (expected to fail with HTTP 403 Forbidden):
gcloud storage rm gs://${COMPLIANCE_BUCKET}/loan-992.json || echo "Deletion successfully blocked by Event-Based Hold!"</code></pre>
</li>
<li><strong>Release Event-Based Hold to Trigger Retention Countdown:</strong>
<pre><code># Release Event-Based Hold (simulating loan payoff event):
gcloud storage objects update gs://${COMPLIANCE_BUCKET}/loan-992.json \
  --no-event-based-hold

# Inspect updated object retention countdown:
gcloud storage objects describe gs://${COMPLIANCE_BUCKET}/loan-992.json \
  --format="yaml(eventBasedHold,retentionExpirationTime)"</code></pre>
Output confirms <code>eventBasedHold: false</code> and <code>retentionExpirationTime</code> is now populated exactly 86,400 seconds (24 hours) from the release timestamp.
</li>
<li><strong>Apply Temporary Legal Hold (Litigation Discovery Freeze):</strong>
<pre><code># Place Temporary Hold on object (simulating court subpoena):
gcloud storage objects update gs://${COMPLIANCE_BUCKET}/loan-992.json \
  --temporary-hold

# Verify temporary hold is active:
gcloud storage objects describe gs://${COMPLIANCE_BUCKET}/loan-992.json \
  --format="yaml(temporaryHold)"

# Attempt deletion (blocked regardless of retention policy duration):
gcloud storage rm gs://${COMPLIANCE_BUCKET}/loan-992.json || echo "Deletion successfully blocked by Temporary Legal Hold!"

# Release temporary hold when litigation concludes:
gcloud storage objects update gs://${COMPLIANCE_BUCKET}/loan-992.json \
  --no-temporary-hold</code></pre>
</li>
<li><strong>Execute Tabletop Design Defense for Irreversible Bucket Lock (Design Exercise):</strong>
<pre><code># TABLETOP DEFENSE SCRIPT - DO NOT EXECUTE AGAINST PRODUCTION WITHOUT DUAL-CUSTODY SIGN-OFF:
# 1. Review dry-run locking command:
# gcloud storage buckets update gs://${COMPLIANCE_BUCKET} --lock-retention-policy
#
# 2. Verify architectural safety checklist:
# [x] Retention period verified against statutory rule (e.g., SEC 17a-4: 7 years = 220,752,000s)
# [x] Bucket name verified: MUST NEVER be a sandbox, CI/CD, or staging bucket
# [x] KMS Key verified: Customer-Managed Encryption Key (CMEK) must have automated rotation
# [x] Soak period confirmed: Bucket operated in unlocked state for >= 30 days in production
# [x] Dual-custody authorization hash recorded in corporate compliance repository
#
# Clear the sandbox retention policy so this test bucket can be cleanly deprovisioned:
gcloud storage buckets update gs://${COMPLIANCE_BUCKET} \
  --clear-retention-policy</code></pre>
</li>
</ol>
<div class="callout success">
<strong>Expected result / acceptance</strong>
<p>The compliance test bucket demonstrates complete WORM protection: objects under Event-Based Holds and Temporary Holds reject all deletion attempts with <code>HTTP 403 Forbidden</code>. Releasing the Event-Based Hold accurately initiates the 86,400-second retention countdown. The Tabletop Defense confirms the irreversible nature of Bucket Lock and the dual-custody governance required before locking production buckets.</p>
</div>
<div class="callout caution">
<strong>Troubleshooting</strong>
<p>NEVER run <code>--lock-retention-policy</code> on this test bucket or in a personal sandbox project. Once locked, the policy cannot be cleared, and the bucket cannot be deleted until the retention duration expires.</p>
</div>
<div class="callout">
<strong>Cleanup and cost</strong>
<p>Because the retention policy was cleared in Step 7, delete the synthetic loan record and remove the sandbox bucket to prevent ongoing billing charges:</p>
<pre><code>gcloud storage rm gs://${COMPLIANCE_BUCKET}/loan-992.json
gcloud storage buckets delete gs://${COMPLIANCE_BUCKET}</code></pre>
</div>
<label class="check"><input type="checkbox" data-progress="lab-58-topic-02"> I completed and checked this topic exercise</label>
</article>
</section>

<section class="completion">
<h2>Daily evidence</h2>
<p>Assemble your object lifecycle analysis, dual-region replication benchmarks, WORM compliance architecture, and durable-write vs POSIX cached-write comparisons into an architectural decision record named <code>day-058-storage-durability.md</code>. Document your location choices (Region vs Dual-Region Turbo Replication vs Multi-Region), storage class cost trade-offs and early deletion math, Autoclass tiering policies, versioning and soft-delete recovery windows, Uniform Bucket-Level Access enforcement, POSIX <code>fdatasync()</code> versus Colossus distributed commit semantics, and the governance workflow for irreversible Bucket Lock compliance.</p>
<label class="check"><input type="checkbox" data-progress="read-58"> I read and reviewed the day</label>
<label class="check"><input type="checkbox" data-progress="artifact-58"> I saved the exit artifact</label>
</section>

<nav class="pager" aria-label="Day pagination">
<a href="day-057.html">← Day 57<small>BGP, MTU and NAT diagnosis</small></a>
<a href="../index.html">All 180 days<small>Browse the roadmap</small></a>
<a href="day-059.html">Day 59 →<small>Transfers, block storage and restore</small></a>
</nav>
<p class="shortcut">Keyboard: P or [ previous · N or ] next · I index</p>
</main>
<footer class="site-footer">GCP Architect · 180-day independent study · Roadmap dated 2026-09-26. Local progress remains in this browser.</footer>
</body>
</html>"""
print("blocks_labs.py written")
