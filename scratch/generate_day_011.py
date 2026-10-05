"""Day 11 generator constants, SVG templates, and overview definitions."""

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        f'Google Cloud — PaaS vs. IaaS vs. SaaS (accessed {ACCESS_DATE})',
        'https://cloud.google.com/learn/paas-vs-iaas-vs-saas#what-are-iaas-paas-saas-and-caas'
    ),
    'topic-02': (
        f'Google Cloud Architecture Framework — Shared responsibility and shared fate (accessed {ACCESS_DATE})',
        'https://docs.cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate#shared_responsibility'
    )
}

PART1_HTML = '''<article class="topic-card overview" id="topic-01-overview">
<h3>IaaS, PaaS, FaaS, SaaS, and where GCP services fall</h3>
<p><strong class="keyword">Cloud service delivery models</strong> define the demarcation line between customer operational control and provider-managed infrastructure. Infrastructure as a Service (IaaS) provides raw virtualized compute, storage, and networking where the customer manages the entire guest operating system and runtime stack. Platform as a Service (PaaS) and Function as a Service (FaaS) abstract host operating systems and server provisioning into managed container and event-driven execution runtimes, while Software as a Service (SaaS) delivers turnkey enterprise applications where the customer governs only user identity and data access.</p>
<p><strong class="side-heading">Why today:</strong> Selecting between IaaS, PaaS, FaaS, and SaaS determines your team's ongoing maintenance toil, autoscaling responsiveness, disaster recovery mechanics, and security exposure.</p>
<p><strong class="side-heading">Where it sits:</strong> Sits at the foundation of all cloud solution design, dictating whether you patch operating systems on Compute Engine or deploy stateless containers to Cloud Run.</p>
<p class="problem-preview">Problem preview: An order ingestion service hosted on a single Compute Engine virtual machine crashes after a manual operating system update breaks local system libraries during peak holiday traffic. The engineering team re-architects the endpoint onto Google Cloud Run, delegating host operating system patching to Google while eliminating 14 hours of potential downtime.</p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>Shared responsibility model (what Google secures vs what you secure)</h3>
<p><strong class="keyword">The Shared Responsibility Model</strong> establishes the non-negotiable division of security obligations between Google Cloud and the enterprise tenant. Google Cloud guarantees the physical security of data centers, custom Titan silicon verification, KVM hypervisor isolation, and global network encryption (Security OF the Cloud). The customer remains strictly and non-negotiably responsible for IAM role bindings, service account credentials, application source code vulnerabilities, network firewall perimeters, and data recovery lifecycle governance (Security IN the Cloud).</p>
<p><strong class="side-heading">Why today:</strong> Cloud security failures overwhelmingly stem from customer misconfigurations and invalid assumptions regarding provider protections rather than infrastructure flaws.</p>
<p><strong class="side-heading">Where it sits:</strong> Governs every project design, requiring explicit ownership of IAM least privilege, data encryption key lifecycles, and cross-region disaster recovery.</p>
<p class="problem-preview">Problem preview: An engineering team deploying a customer account portal to Cloud Run erroneously assumes that Google Cloud automatically blocks unauthorized public internet requests. Because the team bound allUsers to the run invoker role, unauthenticated internet callers exfiltrate 128,000 sensitive customer records until least privilege OIDC authentication is restored.</p>
</article>
'''

# Figure 11.1
FIG_11_1_HTML = '''<figure id="fig-11-1" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day11-models-title day11-models-desc" viewBox="0 0 940 370" width="940" height="370" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day11-models-title">Cloud service model abstraction spectrum and operational division</title>
<desc id="day11-models-desc">A four-column architectural diagram comparing IaaS, PaaS, FaaS, and SaaS, showing which layers are customer-managed versus Google-managed across the compute stack, with authentic service icons.</desc>
<defs>
<marker id="day11-models-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
</defs>

<!-- Column 1: IaaS -->
<rect x="20" y="25" width="205" height="305" rx="10" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="35" y="38" width="24" height="24"/>
<text x="130" y="48" fill="#fce7f3" font-size="14" font-weight="700" text-anchor="middle">IaaS</text>
<text x="130" y="65" fill="#38bdf8" font-size="11" text-anchor="middle">Compute Engine</text>

<!-- IaaS Layers -->
<rect x="35" y="80" width="175" height="26" rx="4" fill="#38bdf8" fill-opacity="0.2" stroke="#38bdf8" stroke-width="1.2"/>
<text x="122" y="97" fill="#fce7f3" font-size="11" text-anchor="middle">Customer: Data &amp; IAM</text>

<rect x="35" y="112" width="175" height="26" rx="4" fill="#38bdf8" fill-opacity="0.2" stroke="#38bdf8" stroke-width="1.2"/>
<text x="122" y="129" fill="#fce7f3" font-size="11" text-anchor="middle">Customer: App &amp; Runtime</text>

<rect x="35" y="144" width="175" height="26" rx="4" fill="#38bdf8" fill-opacity="0.2" stroke="#38bdf8" stroke-width="1.2"/>
<text x="122" y="161" fill="#fce7f3" font-size="11" text-anchor="middle">Customer: Guest OS Patch</text>

<rect x="35" y="176" width="175" height="42" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="122" y="194" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Hypervisor (KVM)</text>
<text x="122" y="210" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Physical Server</text>

<rect x="35" y="224" width="175" height="34" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="122" y="245" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Physical Network</text>

<text x="122" y="285" fill="#38bdf8" font-size="10" font-weight="600" text-anchor="middle">Customer OS Ownership</text>
<text x="122" y="302" fill="#94a3b8" font-size="9" text-anchor="middle">High Control · High Toil</text>

<!-- Column 2: PaaS / CaaS -->
<rect x="250" y="25" width="205" height="305" rx="10" fill="#161b22" stroke="#f97316" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-run.svg" x="265" y="38" width="24" height="24"/>
<text x="360" y="48" fill="#fce7f3" font-size="14" font-weight="700" text-anchor="middle">PaaS / CaaS</text>
<text x="360" y="65" fill="#f97316" font-size="11" text-anchor="middle">Cloud Run / GKE</text>

<!-- PaaS Layers -->
<rect x="265" y="80" width="175" height="26" rx="4" fill="#f97316" fill-opacity="0.2" stroke="#f97316" stroke-width="1.2"/>
<text x="352" y="97" fill="#fce7f3" font-size="11" text-anchor="middle">Customer: Data &amp; IAM</text>

<rect x="265" y="112" width="175" height="26" rx="4" fill="#f97316" fill-opacity="0.2" stroke="#f97316" stroke-width="1.2"/>
<text x="352" y="129" fill="#fce7f3" font-size="11" text-anchor="middle">Customer: Container Image</text>

<rect x="265" y="144" width="175" height="42" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="352" y="162" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Runtime &amp; Host OS</text>
<text x="352" y="178" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Auto-Scaling Engine</text>

<rect x="265" y="192" width="175" height="34" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="352" y="213" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Physical Hardware</text>

<rect x="265" y="232" width="175" height="26" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="352" y="249" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Physical Network</text>

<text x="352" y="285" fill="#f97316" font-size="10" font-weight="600" text-anchor="middle">Google Manages Host OS</text>
<text x="352" y="302" fill="#94a3b8" font-size="9" text-anchor="middle">Zero Host Patching Toil</text>

<!-- Column 3: FaaS -->
<rect x="480" y="25" width="205" height="305" rx="10" fill="#161b22" stroke="#eab308" stroke-width="2"/>
<image href="../assets/icons/gcp/legacy/cloud-functions.svg" x="495" y="38" width="24" height="24"/>
<text x="590" y="48" fill="#fce7f3" font-size="14" font-weight="700" text-anchor="middle">FaaS</text>
<text x="590" y="65" fill="#eab308" font-size="11" text-anchor="middle">Cloud Run functions</text>

<!-- FaaS Layers -->
<rect x="495" y="80" width="175" height="26" rx="4" fill="#eab308" fill-opacity="0.2" stroke="#eab308" stroke-width="1.2"/>
<text x="582" y="97" fill="#fce7f3" font-size="11" text-anchor="middle">Customer: Data &amp; IAM</text>

<rect x="495" y="112" width="175" height="26" rx="4" fill="#eab308" fill-opacity="0.2" stroke="#eab308" stroke-width="1.2"/>
<text x="582" y="129" fill="#fce7f3" font-size="11" text-anchor="middle">Customer: Function Code</text>

<rect x="495" y="144" width="175" height="42" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="582" y="162" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Buildpack &amp; Runtime</text>
<text x="582" y="178" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Event Dispatching</text>

<rect x="495" y="192" width="175" height="34" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="582" y="213" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Physical Hardware</text>

<rect x="495" y="232" width="175" height="26" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="582" y="249" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Physical Network</text>

<text x="582" y="285" fill="#eab308" font-size="10" font-weight="600" text-anchor="middle">Pure Event Abstraction</text>
<text x="582" y="302" fill="#94a3b8" font-size="9" text-anchor="middle">Scale-to-Zero · Ephemeral</text>

<!-- Column 4: SaaS -->
<rect x="710" y="25" width="210" height="305" rx="10" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/core/bigquery.svg" x="725" y="38" width="24" height="24"/>
<text x="825" y="48" fill="#fce7f3" font-size="14" font-weight="700" text-anchor="middle">SaaS</text>
<text x="825" y="65" fill="#34d399" font-size="11" text-anchor="middle">Workspace / BigQuery</text>

<!-- SaaS Layers -->
<rect x="725" y="80" width="180" height="26" rx="4" fill="#34d399" fill-opacity="0.2" stroke="#34d399" stroke-width="1.2"/>
<text x="815" y="97" fill="#fce7f3" font-size="11" text-anchor="middle">Customer: Users &amp; Data</text>

<rect x="725" y="112" width="180" height="34" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="815" y="129" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Application Software</text>
<text x="815" y="142" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Database Engine</text>

<rect x="725" y="152" width="180" height="34" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="815" y="169" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Patching &amp; Scaling</text>
<text x="815" y="182" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: High Availability</text>

<rect x="725" y="192" width="180" height="34" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="815" y="213" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Physical Hardware</text>

<rect x="725" y="232" width="180" height="26" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="815" y="249" fill="#94a3b8" font-size="10.5" text-anchor="middle">Google: Physical Network</text>

<text x="815" y="285" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">Complete Managed App</text>
<text x="815" y="302" fill="#94a3b8" font-size="9" text-anchor="middle">Tenant Owns Data Access Only</text>

<!-- Bottom Summary Banner -->
<rect x="20" y="338" width="900" height="24" rx="4" fill="#161b22"/>
<text x="470" y="354" fill="#94a3b8" font-size="10" text-anchor="middle">As abstraction shifts from IaaS to SaaS, Google assumes more operational layers, but Customer Data and IAM remain tenant-owned across every tier.</text>
</svg>
</div>
<figcaption>Figure 11.1: Cloud service model abstraction spectrum and operational division. Colored upper blocks depict customer-managed responsibilities, while darker lower blocks show Google-managed platform infrastructure across IaaS, PaaS, FaaS, and SaaS service tiers.</figcaption>
</figure>'''

# Figure 11.2
FIG_11_2_HTML = '''<figure id="fig-11-2" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day11-shared-title day11-shared-desc" viewBox="0 0 940 360" width="940" height="360" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day11-shared-title">Google Cloud shared responsibility and shared fate security boundaries</title>
<desc id="day11-shared-desc">A stacked architectural diagram showing the boundary between Google Cloud infrastructure security and Customer workload security across IaaS, PaaS, and SaaS environments, featuring authentic Google Cloud and generic icons.</desc>
<defs>
<marker id="day11-shared-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
</defs>

<!-- Upper Box: Customer Responsibility -->
<rect x="20" y="20" width="900" height="135" rx="10" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<text x="40" y="44" fill="#f43f5e" font-size="13" font-weight="700">CUSTOMER RESPONSIBILITY (Security IN the Cloud — ALWAYS Tenant Owned)</text>

<!-- Customer Controls Cards -->
<rect x="40" y="58" width="200" height="82" rx="6" fill="#21262d" stroke="#f43f5e" stroke-width="1.2"/>
<image href="../assets/icons/generic/storage.svg" x="52" y="70" width="22" height="22"/>
<text x="82" y="85" font-weight="700" font-size="11" fill="#fce7f3">Data &amp; Encryption</text>
<text x="52" y="108" font-size="10" fill="#94a3b8">CMEK Key Rotation</text>
<text x="52" y="124" font-size="10" fill="#94a3b8">Classification &amp; DLP</text>

<rect x="260" y="58" width="200" height="82" rx="6" fill="#21262d" stroke="#f43f5e" stroke-width="1.2"/>
<image href="../assets/icons/gcp/legacy/identity-and-access-management.svg" x="272" y="70" width="22" height="22"/>
<text x="302" y="85" font-weight="700" font-size="11" fill="#fce7f3">Identity &amp; Access (IAM)</text>
<text x="272" y="108" font-size="10" fill="#94a3b8">Least Privilege Policies</text>
<text x="272" y="124" font-size="10" fill="#94a3b8">Service Account Keys</text>

<rect x="480" y="58" width="200" height="82" rx="6" fill="#21262d" stroke="#f43f5e" stroke-width="1.2"/>
<image href="../assets/icons/generic/endpoint.svg" x="492" y="70" width="22" height="22"/>
<text x="522" y="85" font-weight="700" font-size="11" fill="#fce7f3">Application &amp; Logic</text>
<text x="492" y="108" font-size="10" fill="#94a3b8">Input Validation &amp; Auth</text>
<text x="492" y="124" font-size="10" fill="#94a3b8">Dependency Patching</text>

<rect x="700" y="58" width="200" height="82" rx="6" fill="#21262d" stroke="#f43f5e" stroke-width="1.2"/>
<image href="../assets/icons/generic/firewall.svg" x="712" y="70" width="22" height="22"/>
<text x="742" y="85" font-weight="700" font-size="11" fill="#fce7f3">Network &amp; Firewalls</text>
<text x="712" y="108" font-size="10" fill="#94a3b8">VPC Ingress/Egress Rules</text>
<text x="712" y="124" font-size="10" fill="#94a3b8">Cloud Armor WAF Policies</text>

<!-- Lower Box: Google Responsibility -->
<rect x="20" y="170" width="900" height="135" rx="10" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<text x="40" y="194" fill="#38bdf8" font-size="13" font-weight="700">GOOGLE RESPONSIBILITY (Security OF the Cloud — Provider Guaranteed)</text>

<!-- Google Controls Cards -->
<rect x="40" y="208" width="200" height="82" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/generic/server.svg" x="52" y="220" width="22" height="22"/>
<text x="82" y="235" font-weight="700" font-size="11" fill="#fce7f3">Physical Security</text>
<text x="52" y="258" font-size="10" fill="#94a3b8">Biometric Data Centers</text>
<text x="52" y="274" font-size="10" fill="#94a3b8">Hardware Decommissioning</text>

<rect x="260" y="208" width="200" height="82" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/generic/decision.svg" x="272" y="220" width="22" height="22"/>
<text x="302" y="235" font-weight="700" font-size="11" fill="#fce7f3">Hardware &amp; Silicon</text>
<text x="272" y="258" font-size="10" fill="#94a3b8">Titan Security Chips</text>
<text x="272" y="274" font-size="10" fill="#94a3b8">Cryptographic Root of Trust</text>

<rect x="480" y="208" width="200" height="82" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/generic/policy.svg" x="492" y="220" width="22" height="22"/>
<text x="522" y="235" font-weight="700" font-size="11" fill="#fce7f3">Hypervisor &amp; Runtime</text>
<text x="492" y="258" font-size="10" fill="#94a3b8">KVM Multi-Tenant Isolation</text>
<text x="492" y="274" font-size="10" fill="#94a3b8">Host Kernel Live Migration</text>

<rect x="700" y="208" width="200" height="82" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/generic/router.svg" x="712" y="220" width="22" height="22"/>
<text x="742" y="235" font-weight="700" font-size="11" fill="#fce7f3">Global Fiber Backbone</text>
<text x="712" y="258" font-size="10" fill="#94a3b8">Default WAN Encryption</text>
<text x="712" y="274" font-size="10" fill="#94a3b8">Andromeda SDN Mesh</text>

<!-- Shared Fate Banner -->
<rect x="20" y="320" width="900" height="30" rx="6" fill="#1e293b" stroke="#eab308" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/security-command-center.svg" x="35" y="325" width="20" height="20"/>
<text x="470" y="340" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">Google Cloud Shared Fate: Google provides Security Command Center, secure blueprints, and posture tooling to actively assist customers in fulfilling their security duties.</text>
</svg>
</div>
<figcaption>Figure 11.2: Google Cloud shared responsibility and shared fate security boundaries. Physical security, hardware verification, and hypervisor multi-tenancy are guaranteed by Google, whereas customer identity, data lifecycle, access management, and application runtime remain tenant responsibilities.</figcaption>
</figure>'''

# Figure 11.3 (Incident 1)
FIG_11_3_HTML = '''<figure id="fig-11-3" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day11-model-incident-title day11-model-incident-desc" viewBox="0 0 940 320" width="940" height="320" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day11-model-incident-title">Service model selection mismatch and serverless PaaS remediation</title>
<desc id="day11-model-incident-desc">The failed dashed path shows an unpatched VM webhook failing during manual OS updates. The corrected solid path shows serverless Cloud Run handling webhooks with zero guest OS maintenance, featuring authentic icons.</desc>
<defs>
<marker id="day11-model-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day11-model-fail-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"/></marker>
</defs>

<!-- Initiating Event -->
<rect x="20" y="110" width="160" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/client.svg" x="35" y="125" width="22" height="22"/>
<text x="95" y="140" fill="#fce7f3" font-size="12" font-weight="700" text-anchor="middle">Carrier Webhook</text>
<text x="95" y="160" fill="#94a3b8" font-size="10" text-anchor="middle">Status Ingestion</text>
<text x="95" y="176" fill="#38bdf8" font-size="10" text-anchor="middle">HTTP POST /webhook</text>

<!-- Failed Lane: Node 2 -->
<rect x="230" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="245" y="38" width="22" height="22"/>
<image href="../assets/icons/generic/failure.svg" x="272" y="38" width="20" height="20"/>
<text x="345" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">[FAILED: IaaS Compute Engine]</text>
<text x="345" y="70" fill="#fce7f3" font-size="10" text-anchor="middle">Customer manages guest OS</text>
<text x="345" y="86" fill="#94a3b8" font-size="9.5" text-anchor="middle">Manual apt-get maintenance</text>
<text x="345" y="102" fill="#f43f5e" font-size="9.5" text-anchor="middle">Fault injection: broken glibc</text>

<!-- Failed Lane: Node 3 -->
<rect x="505" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/failure.svg" x="520" y="38" width="22" height="22"/>
<text x="617" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">EXACT FAILURE POINT</text>
<text x="617" y="70" fill="#f43f5e" font-size="10" text-anchor="middle">Ruby runtime crash on reboot</text>
<text x="617" y="86" fill="#f43f5e" font-size="9.5" text-anchor="middle">HTTP 502 Bad Gateway Outage</text>
<text x="617" y="102" fill="#94a3b8" font-size="9.5" text-anchor="middle">14,200 webhook events dropped</text>

<!-- Corrected Lane: Node 4 -->
<rect x="230" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-run.svg" x="245" y="208" width="22" height="22"/>
<image href="../assets/icons/generic/decision.svg" x="272" y="208" width="20" height="20"/>
<text x="345" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">[CORRECTED: PaaS Cloud Run]</text>
<text x="345" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Google manages runtime &amp; host</text>
<text x="345" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">Stateless container contract</text>
<text x="345" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Zero host patching toil</text>

<!-- Corrected Lane: Node 5 -->
<rect x="505" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/policy.svg" x="520" y="208" width="22" height="22"/>
<text x="617" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">CORRECTED CONTROL</text>
<text x="617" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Automated scale-out on traffic</text>
<text x="617" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">Built-in HTTPS load balancing</text>
<text x="617" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Isolated container sandboxes</text>

<!-- Outcome Verification Node -->
<rect x="770" y="110" width="150" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/outcome.svg" x="785" y="125" width="22" height="22"/>
<text x="845" y="140" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle">VERIFICATION</text>
<text x="845" y="158" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">HTTP 200 OK</text>
<text x="845" y="174" fill="#94a3b8" font-size="9.5" text-anchor="middle">Webhook Saved</text>
<text x="845" y="190" fill="#94a3b8" font-size="9" text-anchor="middle">Zero drop rate</text>

<!-- Flow Paths -->
<path d="M180 135 L225 80" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#day11-model-fail-arrow)"/>
<path d="M455 72 L495 72" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#day11-model-fail-arrow)"/>
<path d="M180 175 L225 230" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day11-model-arrow)"/>
<path d="M455 242 L495 242" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day11-model-arrow)"/>
<path d="M730 242 L765 175" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day11-model-arrow)"/>

<text x="470" y="310" fill="#94a3b8" font-size="10" text-anchor="middle">Dashed pink line (--&gt;) = manual IaaS patching failure · Solid blue/green line (—&gt;) = serverless PaaS managed scaling</text>
</svg>
</div>
<figcaption>Figure 11.3: Service model selection mismatch and serverless PaaS remediation. Supplied facts: Deploying a stateless webhook on IaaS creates unnecessary OS maintenance toil that caused an unpatched runtime outage. Architectural inference: Migrating stateless HTTP handlers to PaaS Cloud Run delegates host patching to Google while retaining container portability. Expected post-fix behavior: Webhook requests scale horizontally with zero host maintenance and zero dropped transactions.</figcaption>
</figure>'''

# Figure 11.4 (Incident 2)
FIG_11_4_HTML = '''<figure id="fig-11-4" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day11-resp-incident-title day11-resp-incident-desc" viewBox="0 0 940 320" width="940" height="320" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day11-resp-incident-title">Shared responsibility assumption breach and IAM access remediation</title>
<desc id="day11-resp-incident-desc">The failed dashed path shows an unauthenticated internet caller accessing orders due to allUsers invoker binding. The corrected solid path enforces OIDC token authentication and internal ingress, featuring authentic icons.</desc>
<defs>
<marker id="day11-resp-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day11-resp-fail-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"/></marker>
</defs>

<!-- Initiating Event -->
<rect x="20" y="110" width="160" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/client.svg" x="35" y="125" width="22" height="22"/>
<text x="95" y="140" fill="#fce7f3" font-size="12" font-weight="700" text-anchor="middle">Order Query</text>
<text x="95" y="160" fill="#94a3b8" font-size="10" text-anchor="middle">Untrusted Client</text>
<text x="95" y="176" fill="#38bdf8" font-size="10" text-anchor="middle">GET /orders/{id}</text>

<!-- Failed Lane: Node 2 -->
<rect x="230" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/gcp/legacy/identity-and-access-management.svg" x="245" y="38" width="22" height="22"/>
<image href="../assets/icons/generic/failure.svg" x="272" y="38" width="20" height="20"/>
<text x="345" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">[FAILED: Misconfigured IAM]</text>
<text x="345" y="70" fill="#fce7f3" font-size="10" text-anchor="middle">allUsers -&gt; roles/run.invoker</text>
<text x="345" y="86" fill="#94a3b8" font-size="9.5" text-anchor="middle">Assumed Google blocks callers</text>
<text x="345" y="102" fill="#f43f5e" font-size="9.5" text-anchor="middle">Fault injection: open invoker</text>

<!-- Failed Lane: Node 3 -->
<rect x="505" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/failure.svg" x="520" y="38" width="22" height="22"/>
<text x="617" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">EXACT FAILURE POINT</text>
<text x="617" y="70" fill="#f43f5e" font-size="10" text-anchor="middle">Public Internet Data Leak</text>
<text x="617" y="86" fill="#f43f5e" font-size="9.5" text-anchor="middle">Unauthenticated read succeeds</text>
<text x="617" y="102" fill="#94a3b8" font-size="9.5" text-anchor="middle">Customer PII data exposed</text>

<!-- Corrected Lane: Node 4 -->
<rect x="230" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/legacy/identity-and-access-management.svg" x="245" y="208" width="22" height="22"/>
<image href="../assets/icons/generic/decision.svg" x="272" y="208" width="20" height="20"/>
<text x="345" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">[CORRECTED: Least Privilege]</text>
<text x="345" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Dedicated Service Account</text>
<text x="345" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">OIDC ID Token Validation</text>
<text x="345" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Ingress: Internal + LB only</text>

<!-- Corrected Lane: Node 5 -->
<rect x="505" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/policy.svg" x="520" y="208" width="22" height="22"/>
<text x="617" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">CORRECTED CONTROL</text>
<text x="617" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Unauthenticated Blocked (403)</text>
<text x="617" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">Google IAM enforces auth boundary</text>
<text x="617" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Tenant defines authorized callers</text>

<!-- Outcome Verification Node -->
<rect x="770" y="110" width="150" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/outcome.svg" x="785" y="125" width="22" height="22"/>
<text x="845" y="140" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle">VERIFICATION</text>
<text x="845" y="158" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">Secure Access</text>
<text x="845" y="174" fill="#94a3b8" font-size="9.5" text-anchor="middle">Zero public leaks</text>
<text x="845" y="190" fill="#94a3b8" font-size="9" text-anchor="middle">Audit logs recorded</text>

<!-- Flow Paths -->
<path d="M180 135 L225 80" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#day11-resp-fail-arrow)"/>
<path d="M455 72 L495 72" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#day11-resp-fail-arrow)"/>
<path d="M180 175 L225 230" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day11-resp-arrow)"/>
<path d="M455 242 L495 242" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day11-resp-arrow)"/>
<path d="M730 242 L765 175" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day11-resp-arrow)"/>

<text x="470" y="310" fill="#94a3b8" font-size="10" text-anchor="middle">Dashed pink line (--&gt;) = unauthenticated public data leak · Solid blue/green line (—&gt;) = authenticated OIDC service-to-service access</text>
</svg>
</div>
<figcaption>Figure 11.4: Shared responsibility assumption breach and IAM access remediation. Supplied facts: Assuming managed platform handles authorization leads to dangerous public exposure when allUsers is bound to the invoker role. Architectural inference: Google provides robust IAM primitives, but the tenant is solely responsible for principal assignment and least privilege policy enforcement. Expected post-fix behavior: Unauthenticated requests receive HTTP 403 Forbidden, and access is permitted exclusively via signed OIDC identity tokens.</figcaption>
</figure>'''
