"""Day 12 generator constants, SVG templates, and overview definitions."""

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        f'Google Cloud Compute Engine — Regions and zones (accessed {ACCESS_DATE})',
        'https://docs.cloud.google.com/compute/docs/regions-zones#choose'
    ),
    'topic-02': (
        f'Google Cloud Compute Engine — Autoscaling groups of instances (accessed {ACCESS_DATE})',
        'https://docs.cloud.google.com/compute/docs/autoscaler#autoscaling_policy'
    ),
    'topic-03': (
        f'Google Cloud Billing — Estimate your monthly costs (accessed {ACCESS_DATE})',
        'https://docs.cloud.google.com/billing/docs/how-to/estimate-costs#access-pricing-calculator'
    )
}

PART1_HTML = '''<article class="topic-card overview" id="topic-01-overview">
<h3>Regions, zones, multi-region and edge locations</h3>
<p><strong class="keyword">Geographic infrastructure scoping</strong> defines how Google Cloud partitions physical computing resources into global, regional, zonal, and edge tiers. A region represents an independent geographic area composed of three or more fault-isolated zones connected by low-latency private fiber, while multi-region locations provide cross-region geographic redundancy for data persistence, and edge Points of Presence (PoPs) deliver traffic caching and Anycast routing closer to end users.</p>
<p><strong class="side-heading">Why today:</strong> Selecting deployment regions dictates end-user round-trip latency, regulatory data residency compliance, disaster recovery resilience, and inter-region network egress costs.</p>
<p><strong class="side-heading">Where it sits:</strong> Forms the physical deployment baseline for every cloud architecture, establishing the failure domains that prevent localized physical disruptions from cascading into global service outages.</p>
<p class="problem-preview">Problem preview: An e-commerce platform deployed all web application servers and database replicas inside a single Google Cloud zone (us-central1-a) to eliminate inter-zonal egress costs. When an unexpected physical power transformer failure knocked out that single zone, the entire shopping cart service remained offline for four hours.</p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>Elasticity vs scalability, vertical vs horizontal scaling</h3>
<p><strong class="keyword">Workload scaling architecture</strong> establishes how systems accommodate fluctuating traffic demands without service degradation or prohibitive financial waste. Scalability represents the structural capacity of an architecture to handle increased workload volume, whereas elasticity is the dynamic ability to automatically provision and deprovision compute resources in real time to match instantaneous demand curves.</p>
<p><strong class="side-heading">Why today:</strong> Cloud architects must choose between scaling up (vertical scaling with machine resizing downtime and hardware ceilings) and scaling out (horizontal scaling with stateless Managed Instance Groups and autoscaling feedback loops).</p>
<p><strong class="side-heading">Where it sits:</strong> Governs compute resource orchestration, linking application statelessness and Cloud Load Balancing to automated instance lifecycle management and downstream database connection capacities.</p>
<p class="problem-preview">Problem preview: A retail booking engine experiencing a viral flash sale attempted to scale horizontally from 10 to 120 Compute Engine instances within three minutes. Because the autoscaler spawned instances without pre-warming or downstream connection pooling, 120 new web nodes exhausted PostgreSQL database connection limits and caused total checkout failure.</p>
</article>

<article class="topic-card overview" id="topic-03-overview">
<h3>CapEx vs OpEx, pay-as-you-go economics</h3>
<p><strong class="keyword">Cloud economic models</strong> transform enterprise financial architecture by shifting IT infrastructure expenditure from upfront Capital Expenditure (CapEx) to dynamic, consumption-based Operational Expenditure (OpEx). Instead of purchasing depreciating on-premises physical hardware amortized over five years, organizations leverage utility-based per-second metering, Committed Use Discounts (CUDs), and elastic resource allocation.</p>
<p><strong class="side-heading">Why today:</strong> Estimating realistic cloud production costs requires building a comprehensive Cloud Bill of Materials (BOM) that accounts for compute, storage tiers, network egress, and backing services rather than raw virtual machine cores alone.</p>
<p><strong class="side-heading">Where it sits:</strong> Connects technical architectural decisions directly to corporate finance, ensuring infrastructure designs remain financially sustainable, compliant with enterprise budgets, and protected against unmonitored spend spikes.</p>
<p class="problem-preview">Problem preview: An enterprise estimated its cloud migration cost based strictly on raw Compute Engine vCPU and memory pricing calculator figures. At month-end, the actual cloud invoice exceeded initial projections by 320% due to unexpected cross-region network egress, Persistent Disk snapshot storage, and unbudgeted NAT gateway processing fees.</p>
</article>
'''

# Figure 12.1
FIG_12_1_HTML = '''<figure id="fig-12-1" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day12-geo-hierarchy-title day12-geo-hierarchy-desc" viewBox="0 0 940 370" width="940" height="370" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day12-geo-hierarchy-title">Google Cloud Infrastructure Scope Hierarchy and Request Routing Boundaries</title>
<desc id="day12-geo-hierarchy-desc">Architectural diagram illustrating the geographic hierarchy of Google Cloud services from Global Edge PoPs to Regional Managed Instance Groups, Zonal compute/database instances, and Multi-region storage with clear latency and data residency boundaries, featuring authentic icons.</desc>
<defs>
<marker id="day12-geo-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day12-sync-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#34d399"/></marker>
</defs>

<!-- Column 1: Global Edge Tier -->
<rect x="20" y="25" width="205" height="305" rx="10" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/internet.svg" x="35" y="38" width="24" height="24"/>
<text x="130" y="48" fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">GLOBAL EDGE TIER</text>
<text x="130" y="65" fill="#38bdf8" font-size="10.5" text-anchor="middle">Anycast Edge PoPs</text>

<rect x="35" y="80" width="175" height="60" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/generic/router.svg" x="45" y="90" width="20" height="20"/>
<text x="125" y="102" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">Cloud CDN &amp; WAF</text>
<text x="125" y="122" fill="#94a3b8" font-size="9.5" text-anchor="middle">Cloud Armor DDoS Mitigation</text>

<rect x="35" y="150" width="175" height="60" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/generic/load-balancer.svg" x="45" y="160" width="20" height="20"/>
<text x="125" y="172" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">Global External LB</text>
<text x="125" y="192" fill="#94a3b8" font-size="9.5" text-anchor="middle">Single Anycast Virtual IP</text>

<text x="122" y="245" fill="#38bdf8" font-size="10" font-weight="600" text-anchor="middle">Ingress Latency: &lt; 25 ms</text>
<text x="122" y="265" fill="#94a3b8" font-size="9.5" text-anchor="middle">Terminates TCP/TLS at Edge</text>
<text x="122" y="285" fill="#94a3b8" font-size="9" text-anchor="middle">Private Google Fiber Transit</text>

<!-- Column 2: Regional Tier -->
<rect x="250" y="25" width="220" height="305" rx="10" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="265" y="38" width="24" height="24"/>
<text x="365" y="48" fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">REGIONAL TIER</text>
<text x="365" y="65" fill="#34d399" font-size="10.5" text-anchor="middle">e.g., us-central1 (Iowa)</text>

<rect x="265" y="80" width="190" height="60" rx="6" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/generic/load-balancer.svg" x="275" y="90" width="20" height="20"/>
<text x="365" y="102" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">Regional Managed MIG</text>
<text x="365" y="122" fill="#94a3b8" font-size="9.5" text-anchor="middle">Even Instance Distribution</text>

<rect x="265" y="150" width="190" height="60" rx="6" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/generic/database.svg" x="275" y="160" width="20" height="20"/>
<text x="365" y="172" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">Cloud SQL High Availability</text>
<text x="365" y="192" fill="#94a3b8" font-size="9.5" text-anchor="middle">Sync Standby in Zone B</text>

<text x="360" y="245" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">Failure Boundary: Regional</text>
<text x="360" y="265" fill="#94a3b8" font-size="9.5" text-anchor="middle">99.99% Availability Target</text>
<text x="360" y="285" fill="#94a3b8" font-size="9" text-anchor="middle">Inter-Zone Latency: &lt; 1.5 ms</text>

<!-- Column 3: Zonal Tier -->
<rect x="495" y="25" width="205" height="305" rx="10" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/server.svg" x="510" y="38" width="24" height="24"/>
<text x="605" y="48" fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">ZONAL TIER</text>
<text x="605" y="65" fill="#f43f5e" font-size="10.5" text-anchor="middle">e.g., us-central1-a</text>

<rect x="510" y="80" width="175" height="60" rx="6" fill="#21262d" stroke="#f43f5e" stroke-width="1.2"/>
<image href="../assets/icons/generic/server.svg" x="520" y="90" width="20" height="20"/>
<text x="600" y="102" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">Single Compute Instance</text>
<text x="600" y="122" fill="#f43f5e" font-size="9.5" text-anchor="middle">Single Point of Failure</text>

<rect x="510" y="150" width="175" height="60" rx="6" fill="#21262d" stroke="#f43f5e" stroke-width="1.2"/>
<image href="../assets/icons/generic/storage.svg" x="520" y="160" width="20" height="20"/>
<text x="600" y="172" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">Zonal Persistent Disk</text>
<text x="600" y="192" fill="#94a3b8" font-size="9.5" text-anchor="middle">Bound to Zone Data Center</text>

<text x="597" y="245" fill="#f43f5e" font-size="10" font-weight="600" text-anchor="middle">Failure Boundary: Zonal</text>
<text x="597" y="265" fill="#94a3b8" font-size="9.5" text-anchor="middle">99.5% - 99.9% Single VM SLA</text>
<text x="597" y="285" fill="#f43f5e" font-size="9" text-anchor="middle">Vulnerable to Zone Power Loss</text>

<!-- Column 4: Multi-Region Tier -->
<rect x="725" y="25" width="195" height="305" rx="10" fill="#161b22" stroke="#eab308" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-storage.svg" x="740" y="38" width="24" height="24"/>
<text x="825" y="48" fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">MULTI-REGION</text>
<text x="825" y="65" fill="#eab308" font-size="10.5" text-anchor="middle">e.g., US Multi-Region</text>

<rect x="735" y="80" width="175" height="60" rx="6" fill="#21262d" stroke="#eab308" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/cloud-storage.svg" x="745" y="90" width="20" height="20"/>
<text x="825" y="102" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">Cloud Storage (US)</text>
<text x="825" y="122" fill="#94a3b8" font-size="9.5" text-anchor="middle">Geo-redundant Bucket</text>

<rect x="735" y="150" width="175" height="60" rx="6" fill="#21262d" stroke="#eab308" stroke-width="1.2"/>
<image href="../assets/icons/generic/database.svg" x="745" y="160" width="20" height="20"/>
<text x="825" y="172" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">Cloud Spanner (nam3)</text>
<text x="825" y="192" fill="#94a3b8" font-size="9.5" text-anchor="middle">Witness + Read Replicas</text>

<text x="822" y="245" fill="#eab308" font-size="10" font-weight="600" text-anchor="middle">Disaster Recovery SLA</text>
<text x="822" y="265" fill="#94a3b8" font-size="9.5" text-anchor="middle">Survives Complete Region Outage</text>
<text x="822" y="285" fill="#94a3b8" font-size="9" text-anchor="middle">Cross-Region Latency: 35-70 ms</text>

<!-- Flow Arrows across Tiers -->
<path d="M225 110 L250 110" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day12-geo-arrow)"/>
<path d="M470 180 L495 180" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#day12-sync-arrow)"/>
<path d="M700 180 L725 180" fill="none" stroke="#eab308" stroke-width="2" marker-end="url(#day12-geo-arrow)"/>

<!-- Bottom Summary Banner -->
<rect x="20" y="338" width="900" height="24" rx="4" fill="#161b22"/>
<text x="470" y="354" fill="#94a3b8" font-size="10" text-anchor="middle">Geographic scope balances failure domain isolation and low-latency client access against cross-zone and cross-region egress networking costs.</text>
</svg>
</div>
<figcaption>Figure 12.1: Google Cloud Infrastructure Scope Hierarchy and Request Routing Boundaries. Global Anycast Edge PoPs terminate user connections and route requests across private fiber to Regional Managed Instance Groups, which distribute stateless compute across independent Zonal failure domains backed by Multi-Region storage replication.</figcaption>
</figure>'''

# Figure 12.2
FIG_12_2_HTML = '''<figure id="fig-12-2" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day12-scaling-loop-title day12-scaling-loop-desc" viewBox="0 0 940 370" width="940" height="370" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day12-scaling-loop-title">Vertical versus Horizontal Scaling Architecture and Autoscaling Control Loop</title>
<desc id="day12-scaling-loop-desc">Diagram contrasting vertical scaling limitations with horizontal Managed Instance Group autoscaling, depicting the closed metric feedback loop, scale-in controls, and downstream database connection ceiling, featuring authentic icons.</desc>
<defs>
<marker id="day12-scale-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day12-loop-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#eab308"/></marker>
</defs>

<!-- Left Box: Vertical Scaling -->
<rect x="20" y="25" width="310" height="305" rx="10" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/server.svg" x="35" y="38" width="24" height="24"/>
<text x="175" y="48" fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">VERTICAL SCALING (SCALE UP)</text>
<text x="175" y="65" fill="#f43f5e" font-size="10.5" text-anchor="middle">Single Host Machine Resizing</text>

<!-- Vertical Visual Steps -->
<rect x="40" y="80" width="270" height="42" rx="4" fill="#21262d" stroke="#475569" stroke-width="1.2"/>
<text x="175" y="98" fill="#94a3b8" font-size="10.5" text-anchor="middle">Small: e2-standard-4 (4 vCPU, 16 GB)</text>
<text x="175" y="114" fill="#38bdf8" font-size="9" text-anchor="middle">Normal Baseline Traffic</text>

<rect x="40" y="130" width="270" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1.2"/>
<text x="175" y="148" fill="#fce7f3" font-size="10.5" text-anchor="middle">Large: e2-standard-16 (16 vCPU, 64 GB)</text>
<text x="175" y="164" fill="#f43f5e" font-size="9" text-anchor="middle">Requires VM STOP + Machine Edit + START Downtime</text>

<rect x="40" y="180" width="270" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1.2"/>
<text x="175" y="198" fill="#fce7f3" font-size="10.5" text-anchor="middle">Max Ceiling: c3-standard-176</text>
<text x="175" y="214" fill="#f43f5e" font-size="9" text-anchor="middle">Hardware Ceiling Reached · Cannot Scale Further</text>

<rect x="40" y="235" width="270" height="80" rx="4" fill="#2c0b0e" stroke="#f43f5e" stroke-width="1"/>
<image href="../assets/icons/generic/failure.svg" x="50" y="245" width="18" height="18"/>
<text x="180" y="258" fill="#f43f5e" font-size="10" font-weight="700" text-anchor="middle">Architectural Flaws</text>
<text x="175" y="276" fill="#fce7f3" font-size="9" text-anchor="middle">• Maintenance requires planned reboot outage</text>
<text x="175" y="292" fill="#fce7f3" font-size="9" text-anchor="middle">• Single Zonal failure domain (No HA protection)</text>
<text x="175" y="308" fill="#fce7f3" font-size="9" text-anchor="middle">• Idle cost during night/weekend demand troughs</text>

<!-- Right Box: Horizontal Scaling & Closed Loop -->
<rect x="350" y="25" width="570" height="305" rx="10" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="365" y="38" width="24" height="24"/>
<text x="635" y="48" fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">HORIZONTAL SCALING (SCALE OUT) &amp; CLOSED AUTOSCALING LOOP</text>
<text x="635" y="65" fill="#34d399" font-size="10.5" text-anchor="middle">Regional Managed Instance Group (MIG) + Cloud Load Balancing</text>

<!-- Load Balancer Node -->
<rect x="370" y="85" width="140" height="65" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/generic/load-balancer.svg" x="380" y="95" width="20" height="20"/>
<text x="440" y="110" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">Regional LB</text>
<text x="440" y="128" fill="#94a3b8" font-size="9.5" text-anchor="middle">Round-Robin Ingress</text>

<!-- Compute Engine Pool -->
<rect x="545" y="85" width="180" height="65" rx="6" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="555" y="95" width="20" height="20"/>
<text x="635" y="110" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">MIG Worker Pool</text>
<text x="635" y="128" fill="#34d399" font-size="9.5" text-anchor="middle">Min: 2 · Target: 60% · Max: 40</text>

<!-- Monitoring & Autoscaler Controller -->
<rect x="755" y="85" width="150" height="65" rx="6" fill="#21262d" stroke="#eab308" stroke-width="1.2"/>
<image href="../assets/icons/generic/monitoring.svg" x="765" y="95" width="20" height="20"/>
<text x="830" y="110" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">MIG Autoscaler</text>
<text x="830" y="128" fill="#eab308" font-size="9.5" text-anchor="middle">CPU &amp; Latency Signals</text>

<!-- Downstream Database -->
<rect x="460" y="210" width="230" height="65" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/generic/database.svg" x="470" y="220" width="20" height="20"/>
<text x="575" y="235" fill="#fce7f3" font-size="11" font-weight="600" text-anchor="middle">Cloud SQL Primary + PgBouncer</text>
<text x="575" y="255" fill="#94a3b8" font-size="9.5" text-anchor="middle">Connection Pool Limit: 500 max conns</text>

<!-- Closed Loop Arrows -->
<path d="M510 115 L545 115" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day12-scale-arrow)"/>
<path d="M725 115 L755 115" fill="none" stroke="#eab308" stroke-width="2" marker-end="url(#day12-loop-arrow)"/>
<path d="M830 150 L830 185 L635 185 L635 150" fill="none" stroke="#eab308" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#day12-loop-arrow)"/>
<path d="M635 150 L635 210" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#day12-scale-arrow)"/>

<!-- Bottleneck Label -->
<rect x="710" y="215" width="195" height="55" rx="4" fill="#1e293b" stroke="#f43f5e" stroke-width="1"/>
<text x="807" y="234" fill="#f43f5e" font-size="10" font-weight="700" text-anchor="middle">Downstream Ceiling</text>
<text x="807" y="252" fill="#94a3b8" font-size="9" text-anchor="middle">Must cap max instances to protect DB</text>

<!-- Bottom Summary Banner -->
<rect x="20" y="338" width="900" height="24" rx="4" fill="#161b22"/>
<text x="470" y="354" fill="#94a3b8" font-size="10" text-anchor="middle">Horizontal autoscaling dynamically provisions stateless instances in response to telemetry, while PgBouncer shields downstream databases from connection exhaustion.</text>
</svg>
</div>
<figcaption>Figure 12.2: Vertical versus Horizontal Scaling Architecture and Autoscaling Control Loop. Left: Vertical scaling suffers from reboot downtime, single-zone failure domain risks, and fixed hardware ceilings. Right: Horizontal scaling distributes stateless compute across regional zones using a closed-loop autoscaler, bounded by downstream database connection pooling.</figcaption>
</figure>'''

# Figure 12.3
FIG_12_3_HTML = '''<figure id="fig-12-3" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day12-economics-title day12-economics-desc" viewBox="0 0 940 370" width="940" height="370" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day12-economics-title">CapEx Fixed Capacity versus OpEx Elastic Pay-As-You-Go Economics and Cloud Bill of Materials</title>
<desc id="day12-economics-desc">Comparison chart showing CapEx on-premises fixed provisioning waste versus cloud OpEx elastic demand tracking, paired with the comprehensive six-part Cloud Bill of Materials required for production budgeting, featuring authentic icons.</desc>
<defs>
<marker id="day12-econ-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
</defs>

<!-- Left Box: CapEx vs OpEx Demand Curves -->
<rect x="20" y="25" width="440" height="305" rx="10" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/decision.svg" x="35" y="38" width="24" height="24"/>
<text x="240" y="48" fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">CAPEX VS OPEX INFRASTRUCTURE COST DYNAMICS</text>
<text x="240" y="65" fill="#38bdf8" font-size="10.5" text-anchor="middle">Fixed Provisioning vs Elastic Consumption Tracking</text>

<!-- Graph axes -->
<line x1="60" y1="280" x2="420" y2="280" stroke="#475569" stroke-width="1.5"/>
<line x1="60" y1="280" x2="60" y2="90" stroke="#475569" stroke-width="1.5"/>
<text x="425" y="284" fill="#94a3b8" font-size="9">Time</text>
<text x="45" y="85" fill="#94a3b8" font-size="9">Cost</text>

<!-- CapEx Fixed Line -->
<line x1="60" y1="120" x2="420" y2="120" stroke="#f43f5e" stroke-width="2.5"/>
<text x="240" y="112" fill="#f43f5e" font-size="10" font-weight="700" text-anchor="middle">CapEx: Fixed Provisioned Capacity (Peak Headroom)</text>

<!-- Wasted Capacity Shading -->
<path d="M60 120 Q120 220 180 230 T300 240 T420 140 L420 120 L60 120 Z" fill="#f43f5e" fill-opacity="0.15"/>
<text x="240" y="165" fill="#f43f5e" font-size="11" font-weight="600" text-anchor="middle">IDLE WASTE (Unused Paid Compute)</text>

<!-- Actual Demand Curve -->
<path d="M60 250 Q120 230 180 230 T300 240 T380 130 T420 140" fill="none" stroke="#34d399" stroke-width="2.5"/>
<text x="140" y="260" fill="#34d399" font-size="10" font-weight="600">Actual Workload Demand</text>

<!-- OpEx Shading -->
<text x="240" y="305" fill="#38bdf8" font-size="10" text-anchor="middle">OpEx Pay-as-you-go scales linearly with actual customer traffic</text>

<!-- Right Box: Cloud Bill of Materials (BOM) -->
<rect x="480" y="25" width="440" height="305" rx="10" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/artifact.svg" x="495" y="38" width="24" height="24"/>
<text x="700" y="48" fill="#fce7f3" font-size="13" font-weight="700" text-anchor="middle">PRODUCTION CLOUD BILL OF MATERIALS (BOM)</text>
<text x="700" y="65" fill="#34d399" font-size="10.5" text-anchor="middle">6 Essential Cost Dimensions Beyond Raw Virtual Machines</text>

<!-- BOM Cost Cards -->
<rect x="500" y="80" width="195" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="510" y="90" width="20" height="20"/>
<text x="595" y="98" fill="#fce7f3" font-size="10" font-weight="600" text-anchor="middle">1. Compute (vCPU/RAM)</text>
<text x="595" y="112" fill="#94a3b8" font-size="8.5" text-anchor="middle">On-demand vs CUD (1/3 yr)</text>

<rect x="705" y="80" width="195" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/generic/storage.svg" x="715" y="90" width="20" height="20"/>
<text x="802" y="98" fill="#fce7f3" font-size="10" font-weight="600" text-anchor="middle">2. Persistent Storage</text>
<text x="802" y="112" fill="#94a3b8" font-size="8.5" text-anchor="middle">Balanced SSD + Snapshots</text>

<rect x="500" y="132" width="195" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/generic/router.svg" x="510" y="142" width="20" height="20"/>
<text x="595" y="150" fill="#fce7f3" font-size="10" font-weight="600" text-anchor="middle">3. Network Egress</text>
<text x="595" y="164" fill="#94a3b8" font-size="8.5" text-anchor="middle">Inter-zone ($0.01) · Internet ($0.08)</text>

<rect x="705" y="132" width="195" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/generic/load-balancer.svg" x="715" y="142" width="20" height="20"/>
<text x="802" y="150" fill="#fce7f3" font-size="10" font-weight="600" text-anchor="middle">4. Load Balancer &amp; NAT</text>
<text x="802" y="164" fill="#94a3b8" font-size="8.5" text-anchor="middle">Forwarding rules + processed GB</text>

<rect x="500" y="184" width="195" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/cloud-storage.svg" x="510" y="194" width="20" height="20"/>
<text x="595" y="202" fill="#fce7f3" font-size="10" font-weight="600" text-anchor="middle">5. Object Storage (GCS)</text>
<text x="595" y="216" fill="#94a3b8" font-size="8.5" text-anchor="middle">Standard/Nearline + Class A/B Ops</text>

<rect x="705" y="184" width="195" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/generic/database.svg" x="715" y="194" width="20" height="20"/>
<text x="802" y="202" fill="#fce7f3" font-size="10" font-weight="600" text-anchor="middle">6. Managed Database</text>
<text x="802" y="216" fill="#94a3b8" font-size="8.5" text-anchor="middle">Cloud SQL HA vCPU + Storage + PITR</text>

<rect x="500" y="238" width="400" height="75" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
<text x="700" y="256" fill="#38bdf8" font-size="10.5" font-weight="700" text-anchor="middle">Cost Governance Best Practice</text>
<text x="700" y="274" fill="#fce7f3" font-size="9" text-anchor="middle">• Cloud Billing alerts send notifications but DO NOT halt resources</text>
<text x="700" y="290" fill="#fce7f3" font-size="9" text-anchor="middle">• Use Pub/Sub + Cloud Functions to automate hard spend controls</text>
<text x="700" y="304" fill="#fce7f3" font-size="9" text-anchor="middle">• Apply CUDs strictly to steady-state baseline compute (e.g. 60%)</text>

<!-- Bottom Summary Banner -->
<rect x="20" y="338" width="900" height="24" rx="4" fill="#161b22"/>
<text x="470" y="354" fill="#94a3b8" font-size="10" text-anchor="middle">Eliminating on-premises CapEx waste requires disciplined OpEx budgeting across compute, storage, egress, and managed database services.</text>
</svg>
</div>
<figcaption>Figure 12.3: CapEx Fixed Capacity versus OpEx Elastic Pay-As-You-Go Economics and Cloud Bill of Materials. Left: CapEx models waste budget paying for idle headroom during off-peak hours, whereas cloud OpEx scales with customer traffic. Right: A production cloud Bill of Materials mandates comprehensive modeling across compute, disk IOPS, network egress, and database licensing.</figcaption>
</figure>'''

# Figure 12.4 (Incident 1)
FIG_12_4_HTML = '''<figure id="fig-12-4" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day12-case-1-title day12-case-1-desc" viewBox="0 0 940 320" width="940" height="320" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day12-case-1-title">Single Zonal Failure Incident and Multi-Zone Regional MIG Remediation</title>
<desc id="day12-case-1-desc">The failed dashed path shows all instances colocated in us-central1-a failing during power failure. The corrected solid path distributes instances evenly across three regional zones with automatic failover, featuring authentic icons.</desc>
<defs>
<marker id="day12-case-1-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day12-case-1-arr-fail" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"/></marker>
</defs>

<!-- Initiating Event -->
<rect x="20" y="110" width="160" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/client.svg" x="35" y="125" width="22" height="22"/>
<text x="95" y="140" fill="#fce7f3" font-size="12" font-weight="700" text-anchor="middle">Retail Orders</text>
<text x="95" y="160" fill="#94a3b8" font-size="10" text-anchor="middle">Peak Traffic</text>
<text x="95" y="176" fill="#38bdf8" font-size="10" text-anchor="middle">POST /checkout</text>

<!-- Failed Lane: Node 2 -->
<rect x="230" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/server.svg" x="245" y="38" width="22" height="22"/>
<image href="../assets/icons/generic/failure.svg" x="272" y="38" width="20" height="20"/>
<text x="345" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">[FAILED: Single Zone MIG]</text>
<text x="345" y="70" fill="#fce7f3" font-size="10" text-anchor="middle">100% compute in us-central1-a</text>
<text x="345" y="86" fill="#94a3b8" font-size="9.5" text-anchor="middle">Transformer power failure</text>
<text x="345" y="102" fill="#f43f5e" font-size="9.5" text-anchor="middle">Fault injection: zonal blackout</text>

<!-- Failed Lane: Node 3 -->
<rect x="505" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/failure.svg" x="520" y="38" width="22" height="22"/>
<text x="617" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">EXACT FAILURE POINT</text>
<text x="617" y="70" fill="#f43f5e" font-size="10" text-anchor="middle">Complete Storefront Outage</text>
<text x="617" y="86" fill="#f43f5e" font-size="9.5" text-anchor="middle">HTTP 502 Bad Gateway (4h)</text>
<text x="617" y="102" fill="#94a3b8" font-size="9.5" text-anchor="middle">$180,000 lost revenue</text>

<!-- Corrected Lane: Node 4 -->
<rect x="230" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="245" y="208" width="22" height="22"/>
<image href="../assets/icons/generic/decision.svg" x="272" y="208" width="20" height="20"/>
<text x="345" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">[CORRECTED: Regional MIG]</text>
<text x="345" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Even split across zones a, b, f</text>
<text x="345" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">Cloud SQL cross-zone replica</text>
<text x="345" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Automatic health failover</text>

<!-- Corrected Lane: Node 5 -->
<rect x="505" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/policy.svg" x="520" y="208" width="22" height="22"/>
<text x="617" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">CORRECTED CONTROL</text>
<text x="617" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">LB routes around dead zone a</text>
<text x="617" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">Remaining zones absorb load</text>
<text x="617" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Zero human intervention needed</text>

<!-- Outcome Verification Node -->
<rect x="770" y="110" width="150" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/outcome.svg" x="785" y="125" width="22" height="22"/>
<text x="845" y="140" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle">VERIFICATION</text>
<text x="845" y="158" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">Continuous Uptime</text>
<text x="845" y="174" fill="#94a3b8" font-size="9.5" text-anchor="middle">HTTP 200 OK</text>
<text x="845" y="190" fill="#94a3b8" font-size="9.5" text-anchor="middle">Zero dropped carts</text>

<!-- Flow Paths -->
<path d="M180 135 L225 80" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#day12-case-1-arr-fail)"/>
<path d="M455 72 L495 72" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#day12-case-1-arr-fail)"/>
<path d="M180 175 L225 230" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day12-case-1-arr)"/>
<path d="M455 242 L495 242" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day12-case-1-arr)"/>
<path d="M730 242 L765 175" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day12-case-1-arr)"/>

<text x="470" y="310" fill="#94a3b8" font-size="10" text-anchor="middle">Dashed pink line (--&gt;) = single zone failure · Solid blue/green line (—&gt;) = regional multi-zone automated failover</text>
</svg>
</div>
<figcaption>Figure 12.4: Single Zonal Failure Incident and Multi-Zone Regional MIG Remediation. Supplied facts: Hosting an entire e-commerce workload in a single zone eliminated inter-zone networking fees but resulted in a 4-hour total outage during a facility disruption. Architectural inference: Regional Managed Instance Groups spread stateless instances across zones, enabling automatic traffic rerouting. Expected post-fix behavior: Zone loss triggers automatic health check rerouting with 100% transaction survival.</figcaption>
</figure>'''

# Figure 12.5 (Incident 2)
FIG_12_5_HTML = '''<figure id="fig-12-5" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day12-case-2-title day12-case-2-desc" viewBox="0 0 940 320" width="940" height="320" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day12-case-2-title">Flash-Sale Autoscaler Saturation and Pre-Warmed Scaling Remediation</title>
<desc id="day12-case-2-desc">The failed dashed path shows an autoscaler lagging during sudden 10x traffic spikes and exhausting database connection pools. The corrected solid path combines pre-warmed capacity schedules with PgBouncer connection pooling, featuring authentic icons.</desc>
<defs>
<marker id="day12-case-2-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day12-case-2-arr-fail" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"/></marker>
</defs>

<!-- Initiating Event -->
<rect x="20" y="110" width="160" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/client.svg" x="35" y="125" width="22" height="22"/>
<text x="95" y="140" fill="#fce7f3" font-size="12" font-weight="700" text-anchor="middle">Flash Sale Spike</text>
<text x="95" y="160" fill="#94a3b8" font-size="10" text-anchor="middle">10x Traffic in 60s</text>
<text x="95" y="176" fill="#38bdf8" font-size="10" text-anchor="middle">12,000 req/sec</text>

<!-- Failed Lane: Node 2 -->
<rect x="230" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/monitoring.svg" x="245" y="38" width="22" height="22"/>
<image href="../assets/icons/generic/failure.svg" x="272" y="38" width="20" height="20"/>
<text x="345" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">[FAILED: Pure Reactive Scale]</text>
<text x="345" y="70" fill="#fce7f3" font-size="10" text-anchor="middle">VM spin-up takes 180s</text>
<text x="345" y="86" fill="#94a3b8" font-size="9.5" text-anchor="middle">Direct DB connection per VM</text>
<text x="345" y="102" fill="#f43f5e" font-size="9.5" text-anchor="middle">Fault injection: DB pool exhaustion</text>

<!-- Failed Lane: Node 3 -->
<rect x="505" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/failure.svg" x="520" y="38" width="22" height="22"/>
<text x="617" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">EXACT FAILURE POINT</text>
<text x="617" y="70" fill="#f43f5e" font-size="10" text-anchor="middle">PostgreSQL Connection Crash</text>
<text x="617" y="86" fill="#f43f5e" font-size="9.5" text-anchor="middle">"FATAL: too many connections"</text>
<text x="617" y="102" fill="#94a3b8" font-size="9.5" text-anchor="middle">503 Service Unavailable errors</text>

<!-- Corrected Lane: Node 4 -->
<rect x="230" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="245" y="208" width="22" height="22"/>
<image href="../assets/icons/generic/decision.svg" x="272" y="208" width="20" height="20"/>
<text x="345" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">[CORRECTED: Scheduled Scale]</text>
<text x="345" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Pre-warmed minimum instances</text>
<text x="345" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">PgBouncer connection proxy</text>
<text x="345" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Memorystore session caching</text>

<!-- Corrected Lane: Node 5 -->
<rect x="505" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/policy.svg" x="520" y="208" width="22" height="22"/>
<text x="617" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">CORRECTED CONTROL</text>
<text x="617" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Immediate sub-second service</text>
<text x="617" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">DB connections capped at 250</text>
<text x="617" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Controlled scale-in dampening</text>

<!-- Outcome Verification Node -->
<rect x="770" y="110" width="150" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/outcome.svg" x="785" y="125" width="22" height="22"/>
<text x="845" y="140" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle">VERIFICATION</text>
<text x="845" y="158" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">Flash Sale Success</text>
<text x="845" y="174" fill="#94a3b8" font-size="9.5" text-anchor="middle">Latency &lt; 180 ms</text>
<text x="845" y="190" fill="#94a3b8" font-size="9.5" text-anchor="middle">Zero 503 errors</text>

<!-- Flow Paths -->
<path d="M180 135 L225 80" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#day12-case-2-arr-fail)"/>
<path d="M455 72 L495 72" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#day12-case-2-arr-fail)"/>
<path d="M180 175 L225 230" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day12-case-2-arr)"/>
<path d="M455 242 L495 242" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day12-case-2-arr)"/>
<path d="M730 242 L765 175" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day12-case-2-arr)"/>

<text x="470" y="310" fill="#94a3b8" font-size="10" text-anchor="middle">Dashed pink line (--&gt;) = autoscaler lag &amp; DB connection crash · Solid blue/green line (—&gt;) = pre-warmed scaling with PgBouncer pooling</text>
</svg>
</div>
<figcaption>Figure 12.5: Flash-Sale Autoscaler Saturation and Pre-Warmed Scaling Remediation. Supplied facts: Reactive autoscalers require 2-3 minutes to initialize VMs, causing packet drops during instantaneous traffic spikes and overwhelming downstream database connections. Architectural inference: Pre-scheduled scaling combined with connection multiplexing shields stateful backends. Expected post-fix behavior: Sub-200ms response times during promotional launches.</figcaption>
</figure>'''

# Figure 12.6 (Incident 3)
FIG_12_6_HTML = '''<figure id="fig-12-6" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day12-case-3-title day12-case-3-desc" viewBox="0 0 940 320" width="940" height="320" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day12-case-3-title">Cost Estimation Omission Failure and Bill of Materials Remediation</title>
<desc id="day12-case-3-desc">The failed dashed path shows budgeting based only on raw vCPU/RAM leading to a 320% budget overrun. The corrected solid path implements a 6-part Bill of Materials with hard budget alerts and CUD commitments, featuring authentic icons.</desc>
<defs>
<marker id="day12-case-3-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day12-case-3-arr-fail" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"/></marker>
</defs>

<!-- Initiating Event -->
<rect x="20" y="110" width="160" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/artifact.svg" x="35" y="125" width="22" height="22"/>
<text x="95" y="140" fill="#fce7f3" font-size="12" font-weight="700" text-anchor="middle">Annual IT Budget</text>
<text x="95" y="160" fill="#94a3b8" font-size="10" text-anchor="middle">Cloud Migration</text>
<text x="95" y="176" fill="#38bdf8" font-size="10" text-anchor="middle">$15,000/mo cap</text>

<!-- Failed Lane: Node 2 -->
<rect x="230" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/decision.svg" x="245" y="38" width="22" height="22"/>
<image href="../assets/icons/generic/failure.svg" x="272" y="38" width="20" height="20"/>
<text x="345" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">[FAILED: Incomplete BOM]</text>
<text x="345" y="70" fill="#fce7f3" font-size="10" text-anchor="middle">Modeled only vCPU + RAM</text>
<text x="345" y="86" fill="#94a3b8" font-size="9.5" text-anchor="middle">Ignored egress &amp; Cloud NAT</text>
<text x="345" y="102" fill="#f43f5e" font-size="9.5" text-anchor="middle">Fault injection: omitted data transfer</text>

<!-- Failed Lane: Node 3 -->
<rect x="505" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/failure.svg" x="520" y="38" width="22" height="22"/>
<text x="617" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">EXACT FAILURE POINT</text>
<text x="617" y="70" fill="#f43f5e" font-size="10" text-anchor="middle">320% Invoice Shock ($48,000)</text>
<text x="617" y="86" fill="#f43f5e" font-size="9.5" text-anchor="middle">$19k cross-region egress bill</text>
<text x="617" y="102" fill="#94a3b8" font-size="9.5" text-anchor="middle">CFO freezes infrastructure project</text>

<!-- Corrected Lane: Node 4 -->
<rect x="230" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/policy.svg" x="245" y="208" width="22" height="22"/>
<image href="../assets/icons/generic/decision.svg" x="272" y="208" width="20" height="20"/>
<text x="345" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">[CORRECTED: Comprehensive BOM]</text>
<text x="345" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Models compute, egress, NAT, disk</text>
<text x="345" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">3-year CUD on baseline (55% off)</text>
<text x="345" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Colocate services in same region</text>

<!-- Corrected Lane: Node 5 -->
<rect x="505" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/decision.svg" x="520" y="208" width="22" height="22"/>
<text x="617" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">CORRECTED CONTROL</text>
<text x="617" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Hard budget alerts via Pub/Sub</text>
<text x="617" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">Automated non-prod scale-down</text>
<text x="617" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Cost accurately matches $14,200/mo</text>

<!-- Outcome Verification Node -->
<rect x="770" y="110" width="150" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/outcome.svg" x="785" y="125" width="22" height="22"/>
<text x="845" y="140" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle">VERIFICATION</text>
<text x="845" y="158" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">Predictable Spend</text>
<text x="845" y="174" fill="#94a3b8" font-size="9.5" text-anchor="middle">Under Budget Target</text>
<text x="845" y="190" fill="#94a3b8" font-size="9.5" text-anchor="middle">Zero invoice surprises</text>

<!-- Flow Paths -->
<path d="M180 135 L225 80" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#day12-case-3-arr-fail)"/>
<path d="M455 72 L495 72" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#day12-case-3-arr-fail)"/>
<path d="M180 175 L225 230" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day12-case-3-arr)"/>
<path d="M455 242 L495 242" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day12-case-3-arr)"/>
<path d="M730 242 L765 175" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day12-case-3-arr)"/>

<text x="470" y="310" fill="#94a3b8" font-size="10" text-anchor="middle">Dashed pink line (--&gt;) = omitted egress costs &amp; budget blowout · Solid blue/green line (—&gt;) = 6-part BOM with CUDs and budget governance</text>
</svg>
</div>
<figcaption>Figure 12.6: Cost Estimation Omission Failure and Bill of Materials Remediation. Supplied facts: Omitting inter-region network egress, NAT gateway bandwidth fees, and storage operations from initial cost models caused a 320% budget overrun. Architectural inference: Production FinOps models must incorporate all six dimensions of the Cloud Bill of Materials and apply Committed Use Discounts to steady-state baselines. Expected post-fix behavior: Monthly spend remains within 5% of model predictions.</figcaption>
</figure>'''
