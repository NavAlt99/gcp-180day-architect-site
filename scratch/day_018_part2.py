"""Day 18 Topic 2 technical discussion."""

TOPIC_02_TECH = '''
<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Always Free Tier Architecture: Perpetual Allowances vs Promotional Credit</strong></li>
<li><strong>Regional SKU Constraints: Compute Engine e2-micro and Regional Cloud Storage Placement</strong></li>
<li><strong>The Budget Alert Misconception: Notification Events vs Programmatic Hard Spend Caps</strong></li>
<li><strong>Programmatic Spend Capping: Pub/Sub Events, Cloud Functions, and Billing API Disconnection</strong></li>
<li><strong>Continuous Cost Monitoring: Quota Management, Billing Alerts, and Anomaly Detection</strong></li>
</ul>

<p>Operating cost-effective sandbox and production environments in Google Cloud requires mastering the precise boundaries of the Always Free tier and dispelling widespread operational misconceptions regarding budget notifications (<a href="https://cloud.google.com/free/docs/free-cloud-features#free-tier-usage-limits" rel="noopener noreferrer">Google Cloud Free Documentation: Free Tier usage limits (accessed 2026-10-04)</a>). Understanding recurring service allowances, strict regional SKU eligibility rules, and the vital architectural distinction between passive advisory alerts and active programmatic kill-switches allows a cloud architect to deploy experimental workloads safely without incurring runaway cloud invoices.</p>

<h3>Always Free Tier Architecture: Perpetual Allowances vs Promotional Credit</h3>

<p><strong class="side-heading">What it is in general:</strong>
The <strong class="keyword">Google Cloud Free Tier</strong> encompasses two fundamentally distinct mechanisms:
(1) <em>Promotional Free Trial Credit:</em> A one-time grant of $300 USD valid for 90 days across nearly all Google Cloud services;
(2) <em>Always Free Allowances:</em> A recurring set of non-expiring monthly usage quotas across specific core infrastructure services.
Unlike the temporary promotional credit, Always Free allowances renew automatically at the beginning of each calendar month for the lifetime of the account. As long as an organization\'s resource consumption remains within published SKU, regional, and quantitative parameters, Google meters the usage at $0.00 on monthly billing statements.</p>

<p><strong class="side-heading">Relevance to a cloud architect:</strong>
Architects leverage the Always Free tier to host continuous lightweight utility services, development testbeds, telemetry ingest pipelines, and monitoring probes at zero infrastructure cost. However, treating Always Free as an unconstrained license to build is dangerous: any resource consumption that exceeds the exact monthly threshold—or violates specified regional restrictions—is billed immediately at standard on-demand pay-as-you-go rates. Architects must design automated quota monitors to prevent slight operational overages from generating commercial invoices.</p>

<p><strong class="side-heading">Relevance to GCP:</strong>
Google Cloud publishes exact monthly Always Free quotas across primary infrastructure products:
(1) <strong class="keyword">Compute Engine:</strong> 1 non-preemptible <kbd>e2-micro</kbd> VM instance per month (744 hours), 30 GB-months of Standard Persistent Disk, and 1 GB of outbound network egress per month to North America;
(2) <strong class="keyword">Cloud Storage:</strong> 5 GB-months of Standard Regional storage, 5,000 Class A (write/mutate) operations, and 50,000 Class B (read) operations;
(3) <strong class="keyword">Cloud Run:</strong> 2 million requests per month, 360,000 GB-seconds of memory, and 180,000 vCPU-seconds;
(4) <strong class="keyword">BigQuery:</strong> 1 TB of query data scanning per month and 10 GB of active storage.</p>

<h3>Regional SKU Constraints: Compute Engine e2-micro and Regional Cloud Storage Placement</h3>

<p><strong class="side-heading">What it is in general:</strong>
A fundamental architectural constraint of Google Cloud Always Free allowances is strict <strong class="keyword">geographic regional eligibility</strong>. Services eligible for free consumption are not universally free across all Google Cloud regions worldwide. In Compute Engine and Cloud Storage, Always Free quotas apply <em>exclusively</em> to specific designated United States regions:
(1) <kbd>us-central1</kbd> (Iowa, USA);
(2) <kbd>us-east1</kbd> (South Carolina, USA);
(3) <kbd>us-west1</kbd> (Oregon, USA).
Furthermore, Cloud Storage eligibility requires provisioning pure <em>Regional</em> buckets; multi-region and dual-region buckets are ineligible for Always Free allowances.</p>

<p><strong class="side-heading">Relevance to a cloud architect:</strong>
Regional placement errors represent one of the most common causes of unexpected sandbox billing. If an engineer provisions an <kbd>e2-micro</kbd> instance in <kbd>europe-west1</kbd> (Belgium) or <kbd>asia-east1</kbd> (Taiwan)—or creates a multi-region <kbd>US</kbd> Cloud Storage bucket—Google Cloud does not apply the Always Free discount. Instead, the full hourly compute runtime and storage capacity are billed at regular regional list prices. Architects must enforce Organization Policies or Terraform validation rules that restrict sandbox deployments strictly to eligible regions.</p>

<p><strong class="side-heading">Relevance to GCP:</strong>
To prevent regional misplacement in Google Cloud environments, architects configure <strong class="keyword">Resource Location Restriction Organization Policies</strong> (<kbd>constraints/gcp.resourceLocations</kbd>). By applying this constraint to training sandbox folders, administrators restrict compute and storage provisioning strictly to <kbd>in:us-central1-locations, in:us-east1-locations, in:us-west1-locations</kbd>. Any automated or manual attempt to instantiate infrastructure outside these approved zones is blocked instantly at the Cloud Resource Manager API gateway before resources are created.</p>

<h3>The Budget Alert Misconception: Notification Events vs Programmatic Hard Spend Caps</h3>

<p><strong class="side-heading">What it is in general:</strong>
The most pervasive and expensive operational misconception among cloud newcomers is assuming that a <strong class="keyword">Cloud Billing Budget Alert</strong> functions as an automatic financial circuit breaker or hard spend cap. In Google Cloud, a standard budget alert is <em>exclusively an advisory notification mechanism</em>. When actual or forecasted monthly spending crosses configured percentage thresholds (such as 50%, 90%, 100%, or 120% of an allocated target), Google Cloud dispatches alert emails to designated billing administrators and optionally publishes a JSON event payload to Cloud Monitoring or Cloud Pub/Sub.</p>

<p><strong class="side-heading">Relevance to a cloud architect:</strong>
Architects must internalize and communicate the critical principle: <strong>Budget alerts do not stop running resources.</strong> Google Cloud will never automatically terminate virtual machines, delete persistent disks, drop BigQuery tables, or throttle API traffic simply because a budget alert threshold has been breached. If an experimental GPU cluster or runaway recursive Cloud Function script is left running, compute hours continue to accumulate and billable charges continue to mount indefinitely until an operator manually intervenes. Relying on passive budget alerts over a weekend can easily turn a $50 sandbox experiment into a $2,000 corporate credit card surprise.</p>

<p><strong class="side-heading">Relevance to GCP:</strong>
Understanding this distinction is a core concept evaluated across the <strong class="keyword">Google Cloud Digital Leader</strong> and Professional Cloud Architect curricula. Google Cloud intentionally decouples budget alerts from automated workload disruption to prevent inadvertent production downtime: Google will not assume the liability of terminating live customer-facing business services due to a miscalculated budget estimate. Establishing financial ceilings requires architects to deliberately build active programmatic enforcement mechanisms.</p>

<h3>Programmatic Spend Capping: Pub/Sub Events, Cloud Functions, and Billing API Disconnection</h3>

<p><strong class="side-heading">What it is in general:</strong>
To enforce a true, automated, <strong class="keyword">programmatic hard spend cap</strong>, architects implement an event-driven remediation pipeline. Google Cloud Budgets support linking budget alerts directly to a Google Cloud <strong class="keyword">Pub/Sub topic</strong>. Whenever budget thresholds are evaluated (typically multiple times per day), the billing engine publishes a structured JSON message containing the budget display name, the current accrued cost amount, the budget limit amount, and the currency code. An automated subscriber process inspects this event and takes programmatic action when spend exceeds 100%.</p>

<p><strong class="side-heading">Relevance to a cloud architect:</strong>
Architects design the remediation logic based on workload criticality:
(1) <em>Targeted Workload Halting (Moderate):</em> A serverless Cloud Function receives the Pub/Sub event, calls the Compute Engine API (<kbd>instances.stop</kbd>), and shuts down non-essential compute instances while preserving persistent disk data and relational databases;
(2) <em>Nuclear Kill-Switch (Strict Sandbox Capping):</em> For disposable student or intern sandboxes where financial limits are absolute, the Cloud Function invokes the Cloud Billing API (<kbd>projects.billingInfo.update</kbd>) to programmatically clear the linked billing account (<kbd>billingAccountName: ""</kbd>). This disconnects the project from billing, immediately suspending all billable APIs and terminating all compute instances.</p>

<p><strong class="side-heading">Relevance to GCP:</strong>
Implementing the programmatic hard cap requires configuring specific IAM permissions for the automation service account:
(1) The Cloud Function service account must be granted <kbd>roles/billing.admin</kbd> or <kbd>roles/billing.projectManager</kbd> on the Cloud Billing Account to modify project billing linkages;
(2) Architects must document the operational recovery runbook: unlinking billing releases ephemeral external IP addresses on Compute Engine instances and suspends Cloud DNS resolution. When restoring the project, administrators must re-link billing via <kbd>gcloud billing projects link</kbd> and verify service endpoints.</p>

<h3>Continuous Cost Monitoring: Quota Management, Billing Alerts, and Anomaly Detection</h3>

<p><strong class="side-heading">What it is in general:</strong>
Comprehensive financial governance combines reactive budget alerts with proactive <strong class="keyword">Service Quota Management</strong> and real-time cost anomaly detection. Google Cloud Quotas enforce hard limits on the number of specific resources (e.g. total vCPUs, GPU types, persistent disk gigabytes, static IP addresses) that can be provisioned within a single project or region. While quotas primarily serve as platform capacity and security guardrails, they function effectively as pre-provisioning cost bounds.</p>

<p><strong class="side-heading">Relevance to a cloud architect:</strong>
Architects use quota management as a preventive cost control. In training sandboxes and exploratory projects, architects deliberately reduce project-level compute quotas to zero for expensive machine families: setting GPU quotas (<kbd>NVIDIA-T4-GPUS</kbd>) and high-vCPU quotas (<kbd>CPUS_ALL_REGIONS</kbd>) to minimal thresholds prevents engineers from accidentally or maliciously launching high-cost instances. Cost anomaly detection in Cloud Billing continuously analyzes historical consumption trends, triggering early warning notifications when daily spend deviates sharply from baseline expectations.</p>

<p><strong class="side-heading">Relevance to GCP:</strong>
In Google Cloud, quotas are administered through the <strong class="keyword">Cloud Quotas API</strong> and the Google Cloud Console Quotas page. Google Cloud Cost Management also provides native Cost Anomaly Detection, utilizing machine learning algorithms to identify sudden spend surges (such as anomalous Cloud Storage network egress or rapid BigQuery slot consumption) and alerting operations teams hours before standard monthly budget thresholds would be triggered.</p>

{FIG_18_2_HTML}

<p><strong class="side-heading">Comparative Architectural Analysis:</strong></p>
<table>
<caption>Table 18.2: Always Free Resource Limits, Qualifying Regional Constraints, and Overuse Impacts</caption>
<thead>
<tr>
<th scope="col">Service</th>
<th scope="col">Always Free Monthly Allowance</th>
<th scope="col">Qualifying Geographic Region</th>
<th scope="col">Overuse Consequence</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Compute Engine</strong></td>
<td>1 e2-micro VM, 30 GB standard disk, 1 GB egress</td>
<td><kbd>us-central1</kbd>, <kbd>us-east1</kbd>, <kbd>us-west1</kbd> only</td>
<td>Billed at ~$0.0084/hr per additional VM hour</td>
</tr>
<tr>
<td><strong>Cloud Storage</strong></td>
<td>5 GB-months Standard, 5k Class A, 50k Class B</td>
<td><kbd>us-central1</kbd>, <kbd>us-east1</kbd>, <kbd>us-west1</kbd> (Regional only)</td>
<td>Billed at ~$0.020/GB/month for excess storage</td>
</tr>
<tr>
<td><strong>Cloud Run</strong></td>
<td>2M requests, 360k GB-sec, 180k vCPU-sec</td>
<td>All global Cloud Run regions</td>
<td>Billed at standard execution tier rates</td>
</tr>
<tr>
<td><strong>BigQuery</strong></td>
<td>1 TB query analysis, 10 GB active storage</td>
<td>Global BigQuery multi-regions</td>
<td>Billed at $6.25 per TB scanned beyond 1 TB</td>
</tr>
<tr>
<td><strong>Budget Alert</strong></td>
<td>Unlimited notification alerts</td>
<td>Global billing scope</td>
<td><strong>Zero workload enforcement</strong>; spend continues</td>
</tr>
</tbody>
</table>

<p><strong class="side-heading">Concrete example:</strong>
An ML engineering team at Brightloaf runs a synthetic NLP testing pipeline in sandbox project <kbd>brightloaf-sandbox-18</kbd>. A developer mistakenly configures an automated training script to spin up four <kbd>a2-highgpu-1g</kbd> GPU instances costing $14.68/hour to run over a holiday weekend, believing that their configured $50 budget alert will protect them. At 3.4 hours into the test, spend crosses $50.00: Google Cloud sends an automated email notification to an unmonitored shared inbox. Because no programmatic kill-switch is configured, the instances compute for 72 consecutive hours, accumulating $1,057.00 in charges. Had the team subscribed an automated Cloud Function to the budget Pub/Sub topic to execute <kbd>gcloud compute instances stop</kbd> upon receiving <kbd>costAmount &gt; budgetAmount</kbd>, the workload would have been paused at hour 3.5, capping total expenditure at $51.38.</p>

<p><strong>Evidence limit:</strong> This technical analysis defines the resource limits, geographic parameters, and notification mechanisms of the Google Cloud Always Free Tier and Cloud Billing Budgets based strictly on Google Cloud documentation. Real-time billing metering, network egress pricing adjustments, and live API invocations reflect Google Cloud published regional rate cards.</p>

<p>Authoritative documentation section: <a href="https://cloud.google.com/free/docs/free-cloud-features#free-tier-usage-limits" rel="noopener noreferrer">Google Cloud Free Documentation: Free Tier usage limits (accessed 2026-10-04)</a>.</p>
'''
