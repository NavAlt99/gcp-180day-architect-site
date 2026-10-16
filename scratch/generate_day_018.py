"""Day 18 Overview and SVG Diagram Definitions."""

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'Google Cloud Free Documentation: Google Cloud Free Trial (accessed 2026-10-04)',
        'https://cloud.google.com/free/docs/free-cloud-features#free-trial'
    ),
    'topic-02': (
        'Google Cloud Free Documentation: Free Tier usage limits (accessed 2026-10-04)',
        'https://cloud.google.com/free/docs/free-cloud-features#free-tier-usage-limits'
    ),
    'topic-03': (
        'Resource Manager Documentation: Find the project name, number, and ID (accessed 2026-10-04)',
        'https://cloud.google.com/resource-manager/docs/view-update-projects#identifying_projects'
    )
}

PART1_HTML = '''<article class="topic-card overview" id="topic-01-overview">
<h3>Google Cloud accounts and the Free Trial</h3>
<p><strong class="keyword">Google Cloud Accounts</strong> bind corporate or individual identities to Google Cloud resources through linked Cloud Billing Accounts. The 90-day Free Trial provides $300 in promotional credit for proof-of-concept evaluations across Compute Engine, Cloud Storage, BigQuery, and managed services without incurring automatic charges upon expiration unless explicitly upgraded. Establishing isolated billing boundaries and verifying billing health before provisioning infrastructure protects sandbox environments from unexpected operational suspensions.</p>
<p><strong class="side-heading">Why today:</strong> Day 18 begins Block 2 (Cloud environment and identity, Days 18–35), establishing foundational commercial boundaries and billing governance required before provisioning cloud infrastructure.</p>
<p><strong class="side-heading">Where it sits:</strong> Cloud Billing Accounts sit at the administrative root of commercial relationships, linked to projects via Cloud Resource Manager.</p>
<p class="problem-preview">Problem preview: An expired corporate payment method on an unmonitored billing account triggers automated suspension across training sandbox projects, instantly terminating running compute instances. Without redundant payment routing and billing preflight verification, sudden cloud account lockouts disrupt engineering onboarding and delay critical project timelines.</p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>Google Cloud Free Tier and monthly limits</h3>
<p><strong class="keyword">Always Free Tier</strong> allowances provide non-expiring monthly usage quotas across core services, including one <kbd>e2-micro</kbd> instance in qualifying US regions, 5 GB-months of regional Cloud Storage, and 1 TB of BigQuery query analysis. Crucially, Google Cloud budget alerts are passive notifications that do not halt running instances or block API calls when thresholds are crossed. Implementing programmatic financial controls requires event-driven kill-switches rather than relying on advisory email warnings.</p>
<p><strong class="side-heading">Why today:</strong> Distinguishing between promotional credits, Always Free limits, and billable compute usage prevents catastrophic billing surprises during hands-on cloud training.</p>
<p><strong class="side-heading">Where it sits:</strong> Evaluated continuously by Google Cloud's billing meter and Cloud Monitoring quota subsystem against published regional SKUs.</p>
<p class="problem-preview">Problem preview: A training pipeline exceeds its monthly Always Free Compute Engine quota by running an oversized VM in a non-qualifying region, incurring unexpected daily billing charges. Misinterpreting passive budget alert emails as automated hard spend caps leads to budget exhaustion and unexpected corporate credit card overages.</p>
</article>

<article class="topic-card overview" id="topic-03-overview">
<h3>Google Cloud Console navigation and project selection</h3>
<p><strong class="keyword">Project Context Management</strong> governs all operator and automation interactions across the Google Cloud Console, <kbd>gcloud</kbd> CLI, and Terraform. Projects provide complete administrative, networking, and IAM isolation, identified by mutable Project Names, globally unique immutable Project IDs, and system-assigned numeric Project Numbers. Guarding against ambient project context drift ensures administrative commands target intended training sandboxes rather than production systems.</p>
<p><strong class="side-heading">Why today:</strong> All cloud commands execute within an active project context; conflating mutable names with immutable IDs or operating in the wrong ambient context creates severe security and operational risks.</p>
<p><strong class="side-heading">Where it sits:</strong> Governs operator workflows across Google Cloud Console, Cloud Resource Manager, and Cloud Shell execution environments.</p>
<p class="problem-preview">Problem preview: An engineer executing a resource cleanup command from Cloud Shell targets the production project instead of the training sandbox due to ambient project context drift. Conflating project display names with immutable project IDs risks accidental deletion of production microservice endpoints, creating immediate customer checkout outages.</p>
</article>'''

# Figure 18.1: Resource Hierarchy & Billing Association
FIG_18_1_HTML = '''<figure id="fig-18-1" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day18-hier-title day18-hier-desc" viewBox="0 0 940 370" width="940" height="370" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day18-hier-title">Google Cloud Resource Hierarchy, Billing Account Association, and Project Boundaries</title>
<desc id="day18-hier-desc">Architectural diagram illustrating the Google Cloud resource hierarchy from Organization through Folders to Projects, demonstrating project identifier uniqueness, billing account linking, and IAM policy inheritance.</desc>
<defs>
<marker id="day18-hier-arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#38bdf8"/></marker>
<marker id="day18-bill-arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#22c55e"/></marker>
</defs>

<!-- Organization Node -->
<rect x="330" y="25" width="280" height="60" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="1.5"/>
<image href="../assets/icons/generic/policy.svg" x="345" y="38" width="22" height="22"/>
<text x="480" y="47" fill="#f8fafc" font-size="11" font-weight="700" text-anchor="middle">ORGANIZATION (Root Node)</text>
<text x="480" y="62" fill="#38bdf8" font-size="9" text-anchor="middle">brightloaf.com · Domain Identity Root</text>
<text x="480" y="74" fill="#a9b7cb" font-size="8" text-anchor="middle">Inherits Organization Policies &amp; Central IAM</text>

<!-- Connect Org to Folders -->
<path d="M410,85 L260,115" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#day18-hier-arrow)"/>
<path d="M530,85 L680,115" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#day18-hier-arrow)"/>

<!-- Folders -->
<rect x="120" y="115" width="280" height="55" rx="6" fill="#161b22" stroke="#475569" stroke-width="1.5"/>
<text x="135" y="135" fill="#f8fafc" font-size="10" font-weight="700">FOLDER: Production Environment</text>
<text x="135" y="150" fill="#a9b7cb" font-size="8">ID: folders/7012938102 · Department Policy Guard</text>

<rect x="540" y="115" width="280" height="55" rx="6" fill="#161b22" stroke="#475569" stroke-width="1.5"/>
<text x="555" y="135" fill="#f8fafc" font-size="10" font-weight="700">FOLDER: Training &amp; Sandbox</text>
<text x="555" y="150" fill="#a9b7cb" font-size="8">ID: folders/9284019283 · Ephemeral Study Scope</text>

<!-- Connect Folders to Projects -->
<path d="M260,170 L260,200" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#day18-hier-arrow)"/>
<path d="M680,170 L680,200" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#day18-hier-arrow)"/>

<!-- Projects (Core Focus) -->
<rect x="70" y="200" width="380" height="145" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="1.5"/>
<image href="../assets/icons/gcp/legacy/project.svg" x="85" y="210" width="20" height="20"/>
<text x="115" y="224" fill="#f43f5e" font-size="10.5" font-weight="700">PROJECT: brightloaf-prod-us</text>
<text x="85" y="244" fill="#e2e8f0" font-size="9">Project Name: "Brightloaf Production Main"</text>
<text x="85" y="258" fill="#a9b7cb" font-size="8">Project ID (Globally Unique, Immutable): brightloaf-prod-us</text>
<text x="85" y="271" fill="#a9b7cb" font-size="8">Project Number (System Assigned): 104928374619</text>
<rect x="85" y="278" width="350" height="55" rx="4" fill="#1e293b" stroke="#334155"/>
<text x="95" y="294" fill="#22c55e" font-size="8">Linked Billing Account: 01A2B3-4C5D6E-7F8G9H (Active)</text>
<text x="95" y="308" fill="#e2e8f0" font-size="8">Resources: Cloud Run (Order API), Cloud SQL, Pub/Sub</text>
<text x="95" y="322" fill="#a9b7cb" font-size="8">Enforces duplicate fulfillment invariant (&lt;= 1 physical shipment)</text>

<rect x="490" y="200" width="380" height="145" rx="8" fill="#161b22" stroke="#22c55e" stroke-width="1.5"/>
<image href="../assets/icons/gcp/legacy/project.svg" x="505" y="210" width="20" height="20"/>
<text x="535" y="224" fill="#22c55e" font-size="10.5" font-weight="700">PROJECT: brightloaf-sandbox-18</text>
<text x="505" y="244" fill="#e2e8f0" font-size="9">Project Name: "Naveen Study Sandbox Day 18"</text>
<text x="505" y="258" fill="#a9b7cb" font-size="8">Project ID (Globally Unique, Immutable): brightloaf-sandbox-18</text>
<text x="505" y="271" fill="#a9b7cb" font-size="8">Project Number (System Assigned): 859201948271</text>
<rect x="505" y="278" width="350" height="55" rx="4" fill="#1e293b" stroke="#334155"/>
<text x="515" y="294" fill="#22c55e" font-size="8">Linked Billing Account: Free Trial / Cloud Billing Credit</text>
<text x="515" y="308" fill="#e2e8f0" font-size="8">Resources: e2-micro instance (Always Free), Cloud Shell</text>
<text x="515" y="322" fill="#f59e0b" font-size="8">Budget Notification: $50 threshold (Alert != Hard Cap)</text>

<!-- Central Billing Account Box -->
<rect x="350" y="145" width="240" height="42" rx="6" fill="#090d16" stroke="#22c55e" stroke-width="1.5"/>
<image href="../assets/icons/gcp/legacy/free-trial.svg" x="360" y="153" width="24" height="24"/>
<text x="480" y="162" fill="#22c55e" font-size="9" font-weight="700" text-anchor="middle">CLOUD BILLING ACCOUNT</text>
<text x="480" y="176" fill="#a9b7cb" font-size="8" text-anchor="middle">01A2B3-4C5D6E-7F8G9H (Corporate)</text>
<path d="M410,187 L370,200" stroke="#22c55e" stroke-width="1.5" marker-end="url(#day18-bill-arrow)"/>
<path d="M530,187 L570,200" stroke="#22c55e" stroke-width="1.5" marker-end="url(#day18-bill-arrow)"/>
</svg>
</div>
<figcaption>Figure 18.1: Google Cloud resource hierarchy and billing association. The Organization node anchors enterprise domain policies, decomposing downward into Folders (Production vs Training) and individual Projects. Each Project possesses an immutable, globally unique Project ID, a system-generated Project Number, and a mutable display name. A single Cloud Billing Account connects across multiple projects to fund resource consumption, while project boundaries establish complete IAM, networking, and quota isolation.</figcaption>
</figure>'''

# Figure 18.2: Always Free Boundaries & Budget Alert vs Hard Cap
FIG_18_2_HTML = '''<figure id="fig-18-2" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day18-cost-title day18-cost-desc" viewBox="0 0 940 330" width="940" height="330" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day18-cost-title">Free Tier Boundaries, Consumption Tracking, and Budget Alert Mechanisms</title>
<desc id="day18-cost-desc">Architecture diagram contrasting the Always Free tier resource boundaries with the Cloud Billing Budget Alert notification pipeline, demonstrating why budget alerts notify operators but do not stop billable resources.</desc>

<!-- Left Panel: Always Free Tier Limits -->
<rect x="20" y="25" width="440" height="285" rx="8" fill="#161b22" stroke="#475569" stroke-width="1.5"/>
<image href="../assets/icons/gcp/legacy/free-trial.svg" x="35" y="38" width="22" height="22"/>
<text x="65" y="47" fill="#f8fafc" font-size="11" font-weight="700">GOOGLE CLOUD ALWAYS FREE BOUNDARIES</text>
<text x="65" y="63" fill="#a9b7cb" font-size="9">Monthly allowances that never expire (subject to regional rules)</text>

<!-- e2-micro -->
<rect x="35" y="78" width="410" height="48" rx="4" fill="#1e293b" stroke="#334155"/>
<image href="../assets/icons/gcp/legacy/compute-engine.svg" x="45" y="85" width="18" height="18"/>
<text x="70" y="95" fill="#38bdf8" font-size="9" font-weight="700">Compute Engine (1 e2-micro VM)</text>
<text x="70" y="108" fill="#e2e8f0" font-size="8.5">• 1 e2-micro instance/month in us-central1, us-east1, us-west1</text>
<text x="70" y="120" fill="#a9b7cb" font-size="8">• 30 GB standard persistent disk · 1 GB egress/month to North America</text>

<!-- Cloud Storage -->
<rect x="35" y="134" width="410" height="48" rx="4" fill="#1e293b" stroke="#334155"/>
<image href="../assets/icons/gcp/legacy/cloud-storage.svg" x="45" y="141" width="18" height="18"/>
<text x="70" y="151" fill="#38bdf8" font-size="9" font-weight="700">Cloud Storage (5 GB-Months Standard)</text>
<text x="70" y="164" fill="#e2e8f0" font-size="8.5">• 5 GB Standard Storage in US regions (us-central1, us-east1, us-west1)</text>
<text x="70" y="176" fill="#a9b7cb" font-size="8">• 5,000 Class A operations (PUT/POST) · 50,000 Class B operations (GET)</text>

<!-- Cloud Run & Functions -->
<rect x="35" y="190" width="410" height="48" rx="4" fill="#1e293b" stroke="#334155"/>
<text x="45" y="207" fill="#38bdf8" font-size="9" font-weight="700">Serverless (Cloud Run &amp; Cloud Functions)</text>
<text x="45" y="220" fill="#e2e8f0" font-size="8.5">• 2,000,000 requests/month · 360,000 GB-seconds memory allocation</text>
<text x="45" y="232" fill="#a9b7cb" font-size="8">• 180,000 vCPU-seconds · Always Free egress within same region</text>

<!-- BigQuery -->
<rect x="35" y="246" width="410" height="52" rx="4" fill="#1e293b" stroke="#334155"/>
<text x="45" y="263" fill="#38bdf8" font-size="9" font-weight="700">BigQuery &amp; Cloud Logging</text>
<text x="45" y="276" fill="#e2e8f0" font-size="8.5">• 1 TB querying/month · 10 GB active storage</text>
<text x="45" y="289" fill="#a9b7cb" font-size="8">• 50 GB Cloud Logging ingestion/month free of charge</text>

<!-- Right Panel: Budget Alert vs Hard Cap -->
<rect x="480" y="25" width="440" height="285" rx="8" fill="#161b22" stroke="#475569" stroke-width="1.5"/>
<image href="../assets/icons/generic/decision.svg" x="495" y="38" width="22" height="22"/>
<text x="525" y="47" fill="#f8fafc" font-size="11" font-weight="700">BUDGET ALERTS VS PROGRAMMATIC KILL-SWITCH</text>
<text x="525" y="63" fill="#a9b7cb" font-size="9">Budget alerts notify people; they do not halt running resources</text>

<!-- Alert Flow (Passive) -->
<rect x="495" y="80" width="410" height="85" rx="4" fill="#1e293b" stroke="#f59e0b"/>
<image href="../assets/icons/generic/monitoring.svg" x="505" y="88" width="16" height="16"/>
<text x="528" y="98" fill="#f59e0b" font-size="9" font-weight="700">STANDARD BUDGET ALERT (NOTIFICATION ONLY)</text>
<text x="505" y="114" fill="#e2e8f0" font-size="8.5">Target: $50 budget · Thresholds: 50%, 90%, 100%</text>
<text x="505" y="128" fill="#a9b7cb" font-size="8.5">Triggers: Email to Billing Admins &amp; Cloud Monitoring Alert</text>
<text x="505" y="143" fill="#f43f5e" font-size="8.5" font-weight="700">CRITICAL FACT: RESOURCES CONTINUE RUNNING!</text>
<text x="505" y="157" fill="#fce7f3" font-size="8">Billing charges accrue continuously until manual human intervention.</text>

<!-- Programmatic Cap (Active) -->
<rect x="495" y="180" width="410" height="118" rx="4" fill="#1e293b" stroke="#22c55e"/>
<image href="../assets/icons/generic/policy.svg" x="505" y="188" width="16" height="16"/>
<text x="528" y="198" fill="#22c55e" font-size="9" font-weight="700">PROGRAMMATIC HARD CAP ARCHITECTURE</text>
<text x="505" y="214" fill="#e2e8f0" font-size="8.5">1. Budget publishes to Google Cloud Pub/Sub topic.</text>
<text x="505" y="228" fill="#e2e8f0" font-size="8.5">2. Cloud Function / Cloud Run subscriber receives budget event.</text>
<text x="505" y="242" fill="#e2e8f0" font-size="8.5">3. When spend &gt; 100%, script calls Cloud Billing API:</text>
<text x="505" y="256" fill="#38bdf8" font-size="8.5">   projects.billingInfo.update(billingAccountName="")</text>
<text x="505" y="272" fill="#22c55e" font-size="8.5" font-weight="700">RESULT: Unlinks billing, shutting down all paid VMs instantly.</text>
<text x="505" y="286" fill="#a9b7cb" font-size="8">Protects budget from runaway loops; requires deliberate restoration plan.</text>
</svg>
</div>
<figcaption>Figure 18.2: Google Cloud Free Tier boundaries and cost control mechanics. Left: Monthly Always Free allowances across Compute Engine, Cloud Storage, Serverless runtimes, and BigQuery. Right: Architectural distinction between standard Cloud Billing budget alerts (which send passive email/PubSub notifications without interrupting workloads) and automated programmatic kill-switches (which invoke the Cloud Billing API to disable project billing when financial thresholds are breached).</figcaption>
</figure>'''

# Figure 18.3: Incident 1 - Billing Account Disconnection
FIG_18_3_HTML = '''<figure id="fig-18-3" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day18-inc1-title day18-inc1-desc" viewBox="0 0 940 330" width="940" height="330" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day18-inc1-title">Incident Diagram: Billing Account Disconnection Suspends Active Workloads</title>
<desc id="day18-inc1-desc">Incident diagram showing how an expired credit card or severed billing account link halts active cloud resources, contrasted with active multi-payment billing linkage and preflight health checks.</desc>
<defs>
<marker id="day18-bill-fail" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#f43f5e"/></marker>
<marker id="day18-bill-corr" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#22c55e"/></marker>
</defs>

<!-- Intake / Trigger -->
<rect x="20" y="25" width="180" height="280" rx="8" fill="#161b22" stroke="#475569" stroke-width="1.5"/>
<text x="110" y="50" fill="#f8fafc" font-size="10" font-weight="700" text-anchor="middle">BILLING LIFECYCLE EVENT</text>
<text x="110" y="65" fill="#a9b7cb" font-size="9" text-anchor="middle">Payment Authorization</text>
<rect x="30" y="80" width="160" height="55" rx="4" fill="#1e293b" stroke="#334155"/>
<text x="40" y="98" fill="#e2e8f0" font-size="9">Primary Payment Method</text>
<text x="40" y="112" fill="#f59e0b" font-size="8.5">Corporate Credit Card</text>
<text x="40" y="125" fill="#f43f5e" font-size="8.5">Card Expired / Charge Denied</text>

<!-- FAILED PATH (Top) -->
<rect x="230" y="25" width="690" height="130" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="1.5"/>
<text x="245" y="47" fill="#f43f5e" font-size="10" font-weight="700">[FAILED PATH: Severed billing link cascades into instant service shutdown]</text>
<rect x="245" y="60" width="190" height="55" rx="4" fill="#1e293b" stroke="#f43f5e"/>
<text x="255" y="78" fill="#f43f5e" font-size="9" font-weight="700">1. Payment Failure</text>
<text x="255" y="92" fill="#fce7f3" font-size="8.5">No backup payment method</text>
<text x="255" y="105" fill="#f43f5e" font-size="8.5">Billing Account CLOSED</text>

<path d="M435,87 L470,87" stroke="#f43f5e" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#day18-bill-fail)"/>

<rect x="470" y="60" width="200" height="55" rx="4" fill="#1e293b" stroke="#f43f5e"/>
<text x="480" y="78" fill="#f43f5e" font-size="9" font-weight="700">2. Project Billing Disabled</text>
<text x="480" y="92" fill="#fce7f3" font-size="8.5">billingEnabled = false</text>
<text x="480" y="105" fill="#f43f5e" font-size="8.5">API access suspended</text>

<path d="M670,87 L700,87" stroke="#f43f5e" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#day18-bill-fail)"/>

<rect x="700" y="60" width="205" height="85" rx="4" fill="#3b1d38" stroke="#f43f5e"/>
<text x="710" y="78" fill="#f43f5e" font-size="9" font-weight="700">CATASTROPHIC OUTAGE</text>
<text x="710" y="92" fill="#fce7f3" font-size="8.5">• All VMs forcibly stopped</text>
<text x="710" y="106" fill="#fce7f3" font-size="8.5">• Cloud Run returns HTTP 403</text>
<text x="710" y="120" fill="#fce7f3" font-size="8.5">• External IP addresses released</text>
<text x="710" y="134" fill="#fce7f3" font-size="8.5">• Study environment offline</text>

<path d="M190,110 L230,87" stroke="#f43f5e" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#day18-bill-fail)"/>

<!-- CORRECTED PATH (Bottom) -->
<rect x="230" y="175" width="690" height="130" rx="8" fill="#161b22" stroke="#22c55e" stroke-width="1.5"/>
<text x="245" y="197" fill="#22c55e" font-size="10" font-weight="700">[CORRECTED PATH: Backup payment method + automated billing preflight check]</text>
<rect x="245" y="210" width="190" height="55" rx="4" fill="#1e293b" stroke="#334155"/>
<text x="255" y="228" fill="#38bdf8" font-size="9" font-weight="700">1. Redundant Payment Routing</text>
<text x="255" y="242" fill="#e2e8f0" font-size="8.5">Primary card fails -&gt; Fallback</text>
<text x="255" y="255" fill="#22c55e" font-size="8.5">Secondary card charged</text>

<path d="M435,237 L470,237" stroke="#22c55e" stroke-width="2" marker-end="url(#day18-bill-corr)"/>

<rect x="470" y="210" width="200" height="55" rx="4" fill="#1e293b" stroke="#334155"/>
<text x="480" y="228" fill="#38bdf8" font-size="9" font-weight="700">2. Preflight Billing Verification</text>
<text x="480" y="242" fill="#e2e8f0" font-size="8.5">gcloud billing projects describe</text>
<text x="480" y="255" fill="#22c55e" font-size="8.5">billingEnabled == true</text>

<path d="M670,237 L700,237" stroke="#22c55e" stroke-width="2" marker-end="url(#day18-bill-corr)"/>

<rect x="700" y="210" width="205" height="85" rx="4" fill="#052e16" stroke="#22c55e"/>
<text x="710" y="228" fill="#22c55e" font-size="9" font-weight="700">UNINTERRUPTED AVAILABILITY</text>
<text x="710" y="242" fill="#dcfce7" font-size="8.5">✓ Zero unexpected shutdowns</text>
<text x="710" y="256" fill="#dcfce7" font-size="8.5">✓ Workloads remain online</text>
<text x="710" y="270" fill="#dcfce7" font-size="8.5">✓ Proactive billing alert sent</text>
<text x="710" y="284" fill="#dcfce7" font-size="8.5">✓ Invariants strictly preserved</text>

<path d="M190,120 L230,237" stroke="#22c55e" stroke-width="2" marker-end="url(#day18-bill-corr)"/>
</svg>
</div>
<figcaption>Figure 18.3: Supplied facts: A training sandbox environment suffered unexpected resource termination when billing was disabled following an expired corporate card. Architectural inference: When a Cloud Billing Account enters suspended status, Google Cloud terminates paid compute services and revokes API permissions within minutes. Expected post-fix behavior: Configuring automated backup payment methods and embedding billing health verification into deployment preflight scripts ensures continuous environment availability.</figcaption>
</figure>'''

# Figure 18.4: Incident 2 - Budget Alert Misconception
FIG_18_4_HTML = '''<figure id="fig-18-4" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day18-inc2-title day18-inc2-desc" viewBox="0 0 940 330" width="940" height="330" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day18-inc2-title">Incident Diagram: Budget Alert Misconception Leads to Cloud Spend Overrun</title>
<desc id="day18-inc2-desc">Diagnostic incident diagram illustrating how treating budget alerts as hard spend caps allowed runaway compute benchmarking to rack up unexpected charges, contrasted with a programmatic Pub/Sub billing kill-switch.</desc>
<defs>
<marker id="day18-cost-fail" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#f43f5e"/></marker>
<marker id="day18-cost-corr" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#22c55e"/></marker>
</defs>

<!-- Intake / Trigger -->
<rect x="20" y="25" width="180" height="280" rx="8" fill="#161b22" stroke="#475569" stroke-width="1.5"/>
<text x="110" y="50" fill="#f8fafc" font-size="10" font-weight="700" text-anchor="middle">BENCHMARK WORKLOAD</text>
<text x="110" y="65" fill="#a9b7cb" font-size="9" text-anchor="middle">Stress Testing Script</text>
<rect x="30" y="80" width="160" height="55" rx="4" fill="#1e293b" stroke="#334155"/>
<text x="40" y="98" fill="#e2e8f0" font-size="9">Spins up 4x a2-highgpu</text>
<text x="40" y="112" fill="#38bdf8" font-size="8.5">Cost: $14.68 / hour</text>
<text x="40" y="125" fill="#a9b7cb" font-size="8.5">Team assumes $50 cap</text>

<!-- FAILED PATH (Top) -->
<rect x="230" y="25" width="690" height="130" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="1.5"/>
<text x="245" y="47" fill="#f43f5e" font-size="10" font-weight="700">[FAILED PATH: Passive budget alert sends unread email while VMs run continuously]</text>
<rect x="245" y="60" width="190" height="55" rx="4" fill="#1e293b" stroke="#f43f5e"/>
<text x="255" y="78" fill="#f43f5e" font-size="9" font-weight="700">1. Spend Crosses $50</text>
<text x="255" y="92" fill="#fce7f3" font-size="8.5">Budget Alert triggers at 3.4 hrs</text>
<text x="255" y="105" fill="#f59e0b" font-size="8.5">Email sent to billing-admin</text>

<path d="M435,87 L470,87" stroke="#f43f5e" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#day18-cost-fail)"/>

<rect x="470" y="60" width="200" height="55" rx="4" fill="#1e293b" stroke="#f43f5e"/>
<text x="480" y="78" fill="#f43f5e" font-size="9" font-weight="700">2. No Automated Action</text>
<text x="480" y="92" fill="#fce7f3" font-size="8.5">Email unread over weekend</text>
<text x="480" y="105" fill="#f43f5e" font-size="8.5">VMs continue computing 72h</text>

<path d="M670,87 L700,87" stroke="#f43f5e" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#day18-cost-fail)"/>

<rect x="700" y="60" width="205" height="85" rx="4" fill="#3b1d38" stroke="#f43f5e"/>
<text x="710" y="78" fill="#f43f5e" font-size="9" font-weight="700">FINANCIAL OVERRUN</text>
<text x="710" y="92" fill="#fce7f3" font-size="8.5">• Billed $1,400+ on credit card</text>
<text x="710" y="106" fill="#fce7f3" font-size="8.5">• Budget exceeded by 2,800%</text>
<text x="710" y="120" fill="#fce7f3" font-size="8.5">• Team reprimanded for waste</text>
<text x="710" y="134" fill="#fce7f3" font-size="8.5">• Alert was NOT a hard cap!</text>

<path d="M190,110 L230,87" stroke="#f43f5e" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#day18-cost-fail)"/>

<!-- CORRECTED PATH (Bottom) -->
<rect x="230" y="175" width="690" height="130" rx="8" fill="#161b22" stroke="#22c55e" stroke-width="1.5"/>
<text x="245" y="197" fill="#22c55e" font-size="10" font-weight="700">[CORRECTED PATH: Programmatic Pub/Sub alert + automated instance shutdown]</text>
<rect x="245" y="210" width="190" height="55" rx="4" fill="#1e293b" stroke="#334155"/>
<text x="255" y="228" fill="#38bdf8" font-size="9" font-weight="700">1. Pub/Sub Notification</text>
<text x="255" y="242" fill="#e2e8f0" font-size="8.5">Budget emits JSON to Pub/Sub</text>
<text x="255" y="255" fill="#22c55e" font-size="8.5">costAmount &gt; budgetAmount</text>

<path d="M435,237 L470,237" stroke="#22c55e" stroke-width="2" marker-end="url(#day18-cost-corr)"/>

<rect x="470" y="210" width="200" height="55" rx="4" fill="#1e293b" stroke="#22c55e"/>
<text x="480" y="228" fill="#22c55e" font-size="9" font-weight="700">2. Automated Cloud Function</text>
<text x="480" y="242" fill="#e2e8f0" font-size="8.5">gcloud compute instances stop</text>
<text x="480" y="255" fill="#22c55e" font-size="8.5">Halts expensive GPU workers</text>

<path d="M670,237 L700,237" stroke="#22c55e" stroke-width="2" marker-end="url(#day18-cost-corr)"/>

<rect x="700" y="210" width="205" height="85" rx="4" fill="#052e16" stroke="#22c55e"/>
<text x="710" y="228" fill="#22c55e" font-size="9" font-weight="700">SPEND STRICTLY BOUNDED</text>
<text x="710" y="242" fill="#dcfce7" font-size="8.5">✓ Total bill capped at $52.10</text>
<text x="710" y="256" fill="#dcfce7" font-size="8.5">✓ Zero unmonitored charges</text>
<text x="710" y="270" fill="#dcfce7" font-size="8.5">✓ Quota caps prevent respin</text>
<text x="710" y="284" fill="#dcfce7" font-size="8.5">✓ Cloud Digital Leader value</text>

<path d="M190,120 L230,237" stroke="#22c55e" stroke-width="2" marker-end="url(#day18-cost-corr)"/>
</svg>
</div>
<figcaption>Figure 18.4: Supplied facts: An unconstrained GPU benchmark ran over a weekend, accumulating over $1,400 in charges despite a $50 budget alert having been configured. Architectural inference: Google Cloud budget alerts are passive notifications that do not interrupt running instances or prevent API requests. Expected post-fix behavior: Coupling Cloud Billing budget Pub/Sub messages with an automated Cloud Function that stops instances or unlinks billing programmatically enforces hard financial boundaries.</figcaption>
</figure>'''

# Figure 18.5: Incident 3 - Project Context Drift
FIG_18_5_HTML = '''<figure id="fig-18-5" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day18-inc3-title day18-inc3-desc" viewBox="0 0 940 330" width="940" height="330" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day18-inc3-title">Incident Diagram: Project Context Drift Deploys Resources to Wrong Environment</title>
<desc id="day18-inc3-desc">Diagnostic incident diagram illustrating how ambient project state in Cloud Shell caused a destructive deletion intended for a sandbox to terminate a production service, contrasted with deterministic project pinning and IAM service boundary guards.</desc>
<defs>
<marker id="day18-drift-fail" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#f43f5e"/></marker>
<marker id="day18-drift-corr" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#22c55e"/></marker>
</defs>

<!-- Operator Terminal -->
<rect x="20" y="25" width="180" height="280" rx="8" fill="#161b22" stroke="#475569" stroke-width="1.5"/>
<text x="110" y="50" fill="#f8fafc" font-size="10" font-weight="700" text-anchor="middle">OPERATOR TERMINAL</text>
<text x="110" y="65" fill="#a9b7cb" font-size="9" text-anchor="middle">Cloud Shell Session</text>
<rect x="30" y="80" width="160" height="65" rx="4" fill="#1e293b" stroke="#334155"/>
<text x="40" y="98" fill="#e2e8f0" font-size="9">Intended Target:</text>
<text x="40" y="112" fill="#38bdf8" font-size="8.5">brightloaf-sandbox-18</text>
<text x="40" y="125" fill="#f59e0b" font-size="8.5">Destructive command:</text>
<text x="40" y="137" fill="#f43f5e" font-size="8.5">gcloud run services delete</text>

<!-- FAILED PATH (Top) -->
<rect x="230" y="25" width="690" height="130" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="1.5"/>
<text x="245" y="47" fill="#f43f5e" font-size="10" font-weight="700">[FAILED PATH: Ambient project context set to production without explicit flag]</text>
<rect x="245" y="60" width="200" height="55" rx="4" fill="#1e293b" stroke="#f43f5e"/>
<text x="255" y="78" fill="#f43f5e" font-size="9" font-weight="700">1. Ambient gcloud Context</text>
<text x="255" y="92" fill="#fce7f3" font-size="8.5">gcloud config get-value project</text>
<text x="255" y="105" fill="#f43f5e" font-size="8.5">Returns: brightloaf-prod-us</text>

<path d="M445,87 L480,87" stroke="#f43f5e" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#day18-drift-fail)"/>

<rect x="480" y="60" width="190" height="55" rx="4" fill="#1e293b" stroke="#f43f5e"/>
<text x="490" y="78" fill="#f43f5e" font-size="9" font-weight="700">2. Command Executed</text>
<text x="490" y="92" fill="#fce7f3" font-size="8.5">Omits explicit --project flag</text>
<text x="490" y="105" fill="#f43f5e" font-size="8.5">Targets prod-order-api</text>

<path d="M670,87 L700,87" stroke="#f43f5e" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#day18-drift-fail)"/>

<rect x="700" y="60" width="205" height="85" rx="4" fill="#3b1d38" stroke="#f43f5e"/>
<text x="710" y="78" fill="#f43f5e" font-size="9" font-weight="700">PRODUCTION OUTAGE</text>
<text x="710" y="92" fill="#fce7f3" font-size="8.5">• Production Order API deleted</text>
<text x="710" y="106" fill="#fce7f3" font-size="8.5">• Customer checkout broken</text>
<text x="710" y="120" fill="#fce7f3" font-size="8.5">• Emergency redeployment needed</text>
<text x="710" y="134" fill="#fce7f3" font-size="8.5">• Caused by project picker drift</text>

<path d="M190,110 L230,87" stroke="#f43f5e" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#day18-drift-fail)"/>

<!-- CORRECTED PATH (Bottom) -->
<rect x="230" y="175" width="690" height="130" rx="8" fill="#161b22" stroke="#22c55e" stroke-width="1.5"/>
<text x="245" y="197" fill="#22c55e" font-size="10" font-weight="700">[CORRECTED PATH: Explicit --project parameter + PS1 context prompt + IAM boundaries]</text>
<rect x="245" y="210" width="200" height="55" rx="4" fill="#1e293b" stroke="#334155"/>
<text x="255" y="228" fill="#38bdf8" font-size="9" font-weight="700">1. Context-Aware PS1 Prompt</text>
<text x="255" y="242" fill="#e2e8f0" font-size="8.5">Prompt displays active project</text>
<text x="255" y="255" fill="#22c55e" font-size="8.5">operator@sandbox-18:~$</text>

<path d="M445,237 L480,237" stroke="#22c55e" stroke-width="2" marker-end="url(#day18-drift-corr)"/>

<rect x="480" y="210" width="190" height="55" rx="4" fill="#1e293b" stroke="#22c55e"/>
<text x="490" y="228" fill="#22c55e" font-size="9" font-weight="700">2. Mandatory --project Flag</text>
<text x="490" y="242" fill="#e2e8f0" font-size="8.5">Explicit CLI project binding</text>
<text x="490" y="255" fill="#22c55e" font-size="8.5">IAM denies cross-project write</text>

<path d="M670,237 L700,237" stroke="#22c55e" stroke-width="2" marker-end="url(#day18-drift-corr)"/>

<rect x="700" y="210" width="205" height="85" rx="4" fill="#052e16" stroke="#22c55e"/>
<text x="710" y="228" fill="#22c55e" font-weight="700">DETERMINISTIC CONTROL</text>
<text x="710" y="242" fill="#dcfce7" font-size="8.5">✓ Sandbox resource isolated</text>
<text x="710" y="256" fill="#dcfce7" font-size="8.5">✓ Production untouched</text>
<text x="710" y="270" fill="#dcfce7" font-size="8.5">✓ Zero accidental deletions</text>
<text x="710" y="284" fill="#dcfce7" font-size="8.5">✓ Order invariant preserved</text>

<path d="M190,120 L230,237" stroke="#22c55e" stroke-width="2" marker-end="url(#day18-drift-corr)"/>
</svg>
</div>
<figcaption>Figure 18.5: Supplied facts: An engineer intending to clean up a test service in a development sandbox accidentally executed a deletion command against production due to ambient Cloud Shell configuration. Architectural inference: Relying on implicit gcloud CLI project defaults across multi-tenant environments invites destructive human error. Expected post-fix behavior: Enforcing explicit --project flags in automation, displaying active project IDs in shell prompts, and restricting production IAM privileges ensures strict environment segregation.</figcaption>
</figure>'''
