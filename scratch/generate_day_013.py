"""Day 13 Overview and SVG Diagram Definitions."""

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'Google Cloud Architecture Center — Disaster recovery planning guide: How RTO limits product choices (accessed 2026-10-04)',
        'https://docs.cloud.google.com/architecture/disaster-recovery#how_rto_limits_product_choices'
    ),
    'topic-02': (
        'Google Cloud Compute Engine — Managed instance groups: Support for stateful workloads (accessed 2026-10-04)',
        'https://docs.cloud.google.com/compute/docs/instance-groups#support_for_stateful_workloads'
    )
}

PART1_HTML = '''<article class="topic-card overview" id="topic-01-overview">
<h3>High availability vs fault tolerance vs disaster recovery (three different things)</h3>
<p><strong class="keyword">Resilience architectures</strong> are governed by three distinct operational disciplines: High Availability (HA), Fault Tolerance (FT), and Disaster Recovery (DR). High availability designs minimize unplanned downtime through redundant components and automated failover, fault tolerance guarantees continuous uninterrupted operation with zero data loss across component failures, and disaster recovery reconstitutes critical systems after catastrophic regional disruptions. Understanding how Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO) dictate product selection separates professional cloud architects from naive builders.</p>
<p><strong class="side-heading">Why today:</strong> Conflating an available replica with a recoverable backup leads to catastrophic data loss when logical corruption or human error replicates instantly across high-availability nodes.</p>
<p><strong class="side-heading">Where it sits:</strong> Sits at the core of infrastructure reliability engineering, establishing the recovery boundaries between Compute Engine regional MIGs, Cloud SQL HA pairs, and cross-region backups.</p>
<p class="problem-preview">Problem preview: A rogue migration script drops an enterprise production table across a high-availability database cluster, propagating the drop command to active read replicas within 200 milliseconds. The engineering team must execute a point-in-time recovery from an immutable backup archive to recover $850,000 in lost transaction records within a 2-hour RTO window.</p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>Stateless vs stateful applications (this decides almost every HA design)</h3>
<p><strong class="keyword">Application state architecture</strong> dictates every downstream high-availability, autoscaling, and disaster-recovery design decision in cloud systems. Stateless applications treat local runtime instances as ephemeral and interchangeable workers, externalizing all customer sessions and persistence into managed distributed data tiers. Stateful applications maintain authoritative client state, local disk bindings, or ordered lifecycle identities on specific instances, requiring specialized storage attachment and persistent IP reservation.</p>
<p><strong class="side-heading">Why today:</strong> Designing an application as stateless unlocks sub-minute horizontal elasticity and zero-downtime rolling updates, while misunderstanding state placement causes data corruption during autoscaling events.</p>
<p><strong class="side-heading">Where it sits:</strong> Directs compute selection across Google Cloud, determining whether services run on stateless Cloud Run containers and regional MIGs or require Stateful Managed Instance Groups and Kubernetes StatefulSets.</p>
<p class="problem-preview">Problem preview: An order-processing service caches pending fulfillment tokens in local worker process memory to avoid remote database latency, but crashes under an unhandled exception. Because pending transaction tokens were not externalized to Memorystore Redis or Cloud SQL, 1,420 uncommitted customer orders vanish permanently upon VM restart.</p>
</article>'''

# Figure 13.1: HA vs FT vs DR
FIG_13_1_HTML = '''<figure id="fig-13-1" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day13-fig1-title day13-fig1-desc" viewBox="0 0 940 360" width="940" height="360" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day13-fig1-title">High Availability, Fault Tolerance, and Disaster Recovery Architectures with RTO and RPO Objectives</title>
<desc id="day13-fig1-desc">A three-tier architectural diagram contrasting High Availability multi-zone failover, Fault Tolerance continuous dual-active replication, and Disaster Recovery cross-region backup reconstitution, featuring authentic Google Cloud and generic icons.</desc>
<defs>
<marker id="day13-arr1" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day13-sync1" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#34d399"/></marker>
<marker id="day13-dr1" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#fbbf24"/></marker>
</defs>

<!-- Column 1: High Availability (HA) -->
<rect x="20" y="25" width="280" height="295" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/gcp/legacy/cloud-load-balancing.svg" x="35" y="38" width="24" height="24"/>
<text x="165" y="52" fill="#38bdf8" font-size="13" font-weight="700" text-anchor="middle">HIGH AVAILABILITY (HA)</text>
<text x="165" y="70" fill="#94a3b8" font-size="10.5" text-anchor="middle">Multi-Zone Redundancy &amp; Auto-Failover</text>

<rect x="35" y="85" width="250" height="60" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="45" y="95" width="20" height="20"/>
<text x="75" y="108" fill="#fce7f3" font-size="10.5" font-weight="600">Regional MIG (us-central1)</text>
<text x="75" y="124" fill="#94a3b8" font-size="9.5">Auto-healing across zones a, b, c</text>
<text x="75" y="138" fill="#38bdf8" font-size="9.5">Brief failover interruption (RTO &lt; 60s)</text>

<rect x="35" y="155" width="250" height="60" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/cloud-sql.svg" x="45" y="165" width="20" height="20"/>
<text x="75" y="178" fill="#fce7f3" font-size="10.5" font-weight="600">Cloud SQL HA Instance</text>
<text x="75" y="194" fill="#94a3b8" font-size="9.5">Synchronous regional standby disk</text>
<text x="75" y="208" fill="#34d399" font-size="9.5">RPO = 0 (Committed data retained)</text>

<rect x="35" y="225" width="250" height="80" rx="6" fill="#1c2128" stroke="#475569" stroke-width="1"/>
<text x="45" y="244" fill="#38bdf8" font-size="10" font-weight="700">HA Trade-off Profile:</text>
<text x="45" y="262" fill="#cbd5e1" font-size="9.5">• Target: 99.9%–99.99% availability</text>
<text x="45" y="278" fill="#cbd5e1" font-size="9.5">• Failure Scope: Survives single zone loss</text>
<text x="45" y="294" fill="#cbd5e1" font-size="9.5">• Cost: Moderate (+ inter-zone egress)</text>

<!-- Column 2: Fault Tolerance (FT) -->
<rect x="330" y="25" width="280" height="295" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/policy.svg" x="345" y="38" width="24" height="24"/>
<text x="475" y="52" fill="#34d399" font-size="13" font-weight="700" text-anchor="middle">FAULT TOLERANCE (FT)</text>
<text x="475" y="70" fill="#94a3b8" font-size="10.5" text-anchor="middle">Zero-Downtime Continuous Active-Active</text>

<rect x="345" y="85" width="250" height="60" rx="6" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/cloud-spanner.svg" x="355" y="95" width="20" height="20"/>
<text x="385" y="108" fill="#fce7f3" font-size="10.5" font-weight="600">Cloud Spanner (Multi-Region)</text>
<text x="385" y="124" fill="#94a3b8" font-size="9.5">Synchronous Paxos consensus</text>
<text x="385" y="138" fill="#34d399" font-size="9.5">RTO = 0 (Zero failover downtime)</text>

<rect x="345" y="155" width="250" height="60" rx="6" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/generic/decision.svg" x="355" y="165" width="20" height="20"/>
<text x="385" y="178" fill="#fce7f3" font-size="10.5" font-weight="600">Active-Active Dual Hot Paths</text>
<text x="385" y="194" fill="#94a3b8" font-size="9.5">Live redundant packet streams</text>
<text x="385" y="208" fill="#34d399" font-size="9.5">RPO = 0 (Strict serializability)</text>

<rect x="345" y="225" width="250" height="80" rx="6" fill="#1c2128" stroke="#475569" stroke-width="1"/>
<text x="355" y="244" fill="#34d399" font-size="10" font-weight="700">FT Trade-off Profile:</text>
<text x="355" y="262" fill="#cbd5e1" font-size="9.5">• Target: 99.999% (Five-9s) SLA</text>
<text x="355" y="278" fill="#cbd5e1" font-size="9.5">• Failure Scope: Completely seamless failover</text>
<text x="355" y="294" fill="#cbd5e1" font-size="9.5">• Cost: High (Multi-node active duplication)</text>

<!-- Column 3: Disaster Recovery (DR) -->
<rect x="640" y="25" width="280" height="295" rx="8" fill="#161b22" stroke="#fbbf24" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-storage.svg" x="655" y="38" width="24" height="24"/>
<text x="785" y="52" fill="#fbbf24" font-size="13" font-weight="700" text-anchor="middle">DISASTER RECOVERY (DR)</text>
<text x="785" y="70" fill="#94a3b8" font-size="10.5" text-anchor="middle">Cross-Region Reconstitution &amp; Backups</text>

<rect x="655" y="85" width="250" height="60" rx="6" fill="#21262d" stroke="#fbbf24" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/cloud-storage.svg" x="665" y="95" width="20" height="20"/>
<text x="695" y="108" fill="#fce7f3" font-size="10.5" font-weight="600">Dual-Region Bucket (nam4)</text>
<text x="695" y="124" fill="#94a3b8" font-size="9.5">Turbo replication across distant regions</text>
<text x="695" y="138" fill="#fbbf24" font-size="9.5">RPO &lt; 15 min (Replication window)</text>

<rect x="655" y="155" width="250" height="60" rx="6" fill="#21262d" stroke="#fbbf24" stroke-width="1.2"/>
<image href="../assets/icons/generic/outcome.svg" x="665" y="165" width="20" height="20"/>
<text x="695" y="178" fill="#fce7f3" font-size="10.5" font-weight="600">Cross-Region Reconstitution</text>
<text x="695" y="194" fill="#94a3b8" font-size="9.5">Terraform standby cold/warm rebuild</text>
<text x="695" y="208" fill="#fbbf24" font-size="9.5">RTO = 15m–4h (Rebuild / DNS switch)</text>

<rect x="655" y="225" width="250" height="80" rx="6" fill="#1c2128" stroke="#475569" stroke-width="1"/>
<text x="665" y="244" fill="#fbbf24" font-size="10" font-weight="700">DR Trade-off Profile:</text>
<text x="665" y="262" fill="#cbd5e1" font-size="9.5">• Target: Business survival &amp; compliance</text>
<text x="665" y="278" fill="#cbd5e1" font-size="9.5">• Failure Scope: Total continental blackout</text>
<text x="665" y="294" fill="#cbd5e1" font-size="9.5">• Cost: Economical cold storage archives</text>

<!-- Footer Comparison Bar -->
<rect x="20" y="325" width="900" height="24" rx="4" fill="#090d13" stroke="#30363d" stroke-width="1"/>
<text x="160" y="341" fill="#38bdf8" font-size="10" font-weight="600" text-anchor="middle">HA: RTO &lt; 60s, RPO = 0</text>
<text x="470" y="341" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">FT: RTO = 0, RPO = 0</text>
<text x="780" y="341" fill="#fbbf24" font-size="10" font-weight="600" text-anchor="middle">DR: RTO &lt; 2h, RPO &lt; 15m</text>
</svg>
</div>
<figcaption>Figure 13.1: Architectural comparison of High Availability, Fault Tolerance, and Disaster Recovery failure boundaries, accompanied by the operational RTO (downtime duration) and RPO (data currency loss) metric timelines.</figcaption>
</figure>'''

# Figure 13.2: Stateless Worker Tier vs Durable State Store
FIG_13_2_HTML = '''<figure id="fig-13-2" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day13-fig2-title day13-fig2-desc" viewBox="0 0 940 340" width="940" height="340" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day13-fig2-title">Stateless Worker Tier versus Durable State Store and Recovery Lifecycle</title>
<desc id="day13-fig2-desc">An architecture diagram separating the ephemeral stateless worker tier from the authoritative durable database and in-memory cache, illustrating fulfillment deduplication boundaries and independent point-in-time recovery copies, with authentic Google Cloud and generic icons.</desc>
<defs>
<marker id="day13-warr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day13-sarr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#34d399"/></marker>
<marker id="day13-darr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#fbbf24"/></marker>
</defs>

<!-- Boundary 1: Stateless Worker Tier -->
<rect x="20" y="25" width="410" height="285" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-run.svg" x="35" y="38" width="24" height="24"/>
<text x="70" y="54" fill="#38bdf8" font-size="13" font-weight="700">STATELESS COMPUTE TIER</text>
<text x="70" y="70" fill="#94a3b8" font-size="10.5">Ephemeral, Disposable, Horizontally Elastic Workers</text>

<!-- Worker 1 -->
<rect x="35" y="85" width="180" height="75" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="45" y="95" width="20" height="20"/>
<text x="75" y="108" fill="#fce7f3" font-size="11" font-weight="600">Order Worker A</text>
<text x="75" y="124" fill="#94a3b8" font-size="9.5">Instance in Zone 1</text>
<text x="75" y="138" fill="#38bdf8" font-size="9.5">Zero local disk state</text>
<text x="75" y="150" fill="#ef4444" font-size="8.5">Crashable anytime</text>

<!-- Worker 2 -->
<rect x="235" y="85" width="180" height="75" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="245" y="95" width="20" height="20"/>
<text x="275" y="108" fill="#fce7f3" font-size="11" font-weight="600">Order Worker B</text>
<text x="275" y="124" fill="#94a3b8" font-size="9.5">Instance in Zone 2</text>
<text x="275" y="138" fill="#38bdf8" font-size="9.5">Zero local disk state</text>
<text x="275" y="150" fill="#ef4444" font-size="8.5">Crashable anytime</text>

<!-- Invariant box -->
<rect x="35" y="175" width="380" height="120" rx="6" fill="#1c2128" stroke="#475569" stroke-width="1"/>
<text x="45" y="195" fill="#38bdf8" font-size="10.5" font-weight="700">Stateless Worker Properties:</text>
<text x="45" y="214" fill="#cbd5e1" font-size="9.5">• In-flight HTTP requests handled with idempotent retry tokens</text>
<text x="45" y="232" fill="#cbd5e1" font-size="9.5">• No persistent local disk storage; local filesystems are ephemeral</text>
<text x="45" y="250" fill="#cbd5e1" font-size="9.5">• Session state externalized to Memorystore Redis cache</text>
<text x="45" y="268" fill="#cbd5e1" font-size="9.5">• Worker restarts or autoscaling scale-in drops zero committed data</text>
<text x="45" y="286" fill="#34d399" font-size="9.5">✓ Elastic scale: 2 to 100+ instances without state migration toil</text>

<!-- Flow Arrows across boundary -->
<path d="M430,120 L490,120" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#day13-sarr)"/>
<text x="460" y="112" fill="#34d399" font-size="9" text-anchor="middle">Write State</text>

<path d="M430,220 L490,220" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day13-warr)"/>
<text x="460" y="212" fill="#38bdf8" font-size="9" text-anchor="middle">Lookup Cache</text>

<!-- Boundary 2: Durable State & Storage Tier -->
<rect x="500" y="25" width="420" height="285" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-sql.svg" x="515" y="38" width="24" height="24"/>
<text x="550" y="54" fill="#34d399" font-size="13" font-weight="700">DURABLE STATEFUL STORAGE TIER</text>
<text x="550" y="70" fill="#94a3b8" font-size="10.5">Authoritative Ledger, ACID Transactions &amp; Independent Backups</text>

<!-- Cache Node -->
<rect x="515" y="85" width="185" height="65" rx="6" fill="#21262d" stroke="#38bdf8" stroke-width="1.2"/>
<image href="../assets/icons/gcp/legacy/memorystore.svg" x="525" y="95" width="20" height="20"/>
<text x="555" y="108" fill="#fce7f3" font-size="10.5" font-weight="600">Memorystore (Redis)</text>
<text x="555" y="122" fill="#94a3b8" font-size="9">Session cache &amp; rate limit</text>
<text x="555" y="136" fill="#ef4444" font-size="8.5">Volatile (Rebuildable)</text>

<!-- Database Node -->
<rect x="715" y="85" width="190" height="65" rx="6" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/cloud-sql.svg" x="725" y="95" width="20" height="20"/>
<text x="755" y="108" fill="#fce7f3" font-size="10.5" font-weight="600">Cloud SQL (PostgreSQL)</text>
<text x="755" y="122" fill="#94a3b8" font-size="9">Authoritative state ledger</text>
<text x="755" y="136" fill="#34d399" font-size="8.5">ACID Durable commits</text>

<!-- Independent Backup Node -->
<rect x="515" y="165" width="390" height="65" rx="6" fill="#21262d" stroke="#fbbf24" stroke-width="1.2"/>
<image href="../assets/icons/gcp/core/cloud-storage.svg" x="525" y="175" width="20" height="20"/>
<text x="555" y="188" fill="#fce7f3" font-size="10.5" font-weight="600">Cloud Storage Backup Vault (Dual-Region nam4)</text>
<text x="555" y="204" fill="#94a3b8" font-size="9.5">Automated Point-in-Time Recovery (PITR) + Immutable WAL logs</text>
<text x="555" y="218" fill="#fbbf24" font-size="9">Physically independent from active database instances (RTO &lt; 2h, RPO &lt; 5m)</text>

<!-- Deduplication Boundary -->
<rect x="515" y="240" width="390" height="55" rx="6" fill="#1c2128" stroke="#475569" stroke-width="1"/>
<image href="../assets/icons/generic/decision.svg" x="525" y="248" width="18" height="18"/>
<text x="550" y="258" fill="#38bdf8" font-size="9.5" font-weight="700">Deduplication &amp; Idempotency Boundary:</text>
<text x="550" y="274" fill="#cbd5e1" font-size="9">Database primary key (UUIDv4) enforces idempotent fulfillment on retries.</text>
<text x="550" y="286" fill="#34d399" font-size="9">Corrupt writes isolated from backups via 30-day retention lock.</text>
</svg>
</div>
<figcaption>Figure 13.2: Architecture diagram separating the ephemeral stateless worker tier from the authoritative durable database, illustrating the fulfillment deduplication boundary and an independent recovery copy.</figcaption>
</figure>'''

# Figure 13.3: Incident 1 (Shared Database Deletion)
FIG_13_3_HTML = '''<figure id="fig-13-3" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day13-fig3-title day13-fig3-desc" viewBox="0 0 940 320" width="940" height="320" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day13-fig3-title">Shared Database Deletion Incident and Point-in-Time Recovery Remediation</title>
<desc id="day13-fig3-desc">The failed dashed path shows an accidental database deletion instantly propagating across active HA replicas. The corrected solid path shows automated point-in-time recovery and transaction log replay restoring committed order state, with authentic icons.</desc>
<defs>
<marker id="day13-f3-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day13-f3-fail" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"/></marker>
<marker id="day13-f3-pass" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#34d399"/></marker>
</defs>

<!-- Initiating Event -->
<rect x="20" y="110" width="160" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/client.svg" x="35" y="125" width="22" height="22"/>
<text x="95" y="140" fill="#fce7f3" font-size="12" font-weight="700" text-anchor="middle">Rogue Migration</text>
<text x="95" y="160" fill="#94a3b8" font-size="10" text-anchor="middle">Accidental Script</text>
<text x="95" y="176" fill="#f43f5e" font-size="9.5" text-anchor="middle">DROP TABLE orders;</text>

<!-- Failed Path (Upper) -->
<path d="M180,135 L240,75" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#day13-f3-fail)"/>

<rect x="240" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-sql.svg" x="255" y="38" width="22" height="22"/>
<image href="../assets/icons/generic/failure.svg" x="282" y="38" width="20" height="20"/>
<text x="355" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">[FAILED: HA Replica Trap]</text>
<text x="355" y="70" fill="#fce7f3" font-size="10" text-anchor="middle">Synchronous Replication</text>
<text x="355" y="86" fill="#94a3b8" font-size="9.5" text-anchor="middle">DROP replicates in 150ms</text>
<text x="355" y="102" fill="#f43f5e" font-size="9.5" text-anchor="middle">Standby disk mirrors DROP</text>

<path d="M465,72 L525,72" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#day13-f3-fail)"/>

<rect x="525" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/failure.svg" x="540" y="38" width="22" height="22"/>
<text x="637" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">EXACT FAILURE POINT</text>
<text x="637" y="70" fill="#f43f5e" font-size="10" text-anchor="middle">All 2 HA nodes lose data</text>
<text x="637" y="86" fill="#f43f5e" font-size="9.5" text-anchor="middle">HTTP 500 Outage on checkout</text>
<text x="637" y="102" fill="#94a3b8" font-size="9.5" text-anchor="middle">Replica != Backup</text>

<!-- Corrected Path (Lower) -->
<path d="M180,180 L240,240" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#day13-f3-pass)"/>

<rect x="240" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-storage.svg" x="255" y="208" width="22" height="22"/>
<image href="../assets/icons/generic/decision.svg" x="282" y="208" width="20" height="20"/>
<text x="355" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">[CORRECTED: PITR Vault]</text>
<text x="355" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Continuous WAL Archiving</text>
<text x="355" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">Cloud Storage backup bucket</text>
<text x="355" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Immutable retention policy</text>

<path d="M465,242 L525,242" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#day13-f3-pass)"/>

<rect x="525" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/policy.svg" x="540" y="208" width="22" height="22"/>
<text x="637" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">POINT-IN-TIME REPLAY</text>
<text x="637" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Target: T-minus 1 minute</text>
<text x="637" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">WAL replayed up to 14:21:59</text>
<text x="637" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">RPO &lt; 60s; Zero orders lost</text>

<!-- Outcome Verification Node -->
<path d="M750,242 L790,175" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day13-f3-arr)"/>

<rect x="780" y="110" width="145" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/outcome.svg" x="795" y="125" width="22" height="22"/>
<text x="852" y="140" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle">VERIFICATION</text>
<text x="852" y="158" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">RTO &lt; 45 minutes</text>
<text x="852" y="174" fill="#fce7f3" font-size="9" text-anchor="middle">Restored &amp; Verified</text>
<text x="852" y="188" fill="#94a3b8" font-size="9" text-anchor="middle">Storefront Operational</text>
</svg>
</div>
<figcaption>Figure 13.3: Supplied facts: An accidental database deletion caused checkout data loss even though two Order API workers remained healthy. Architectural inference: High availability preserves compute routes but does not protect against data deletion. Expected post-fix behavior: Point-in-time backup restoration combined with transaction log replay restores committed order state within RTO and RPO limits while enforcing fulfillment deduplication.</figcaption>
</figure>'''

# Figure 13.4: Incident 2 (Process-Memory State Deduplication)
FIG_13_4_HTML = '''<figure id="fig-13-4" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day13-fig4-title day13-fig4-desc" viewBox="0 0 940 320" width="940" height="320" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day13-fig4-title">Process-Memory State Deduplication Incident and Durable Invariant Remediation</title>
<desc id="day13-fig4-desc">The failed dashed path shows an in-memory deduplication set vanishing upon worker crash, causing duplicate payment fulfillment on retry. The corrected solid path shows database primary key uniqueness enforcing idempotent deduplication, with authentic icons.</desc>
<defs>
<marker id="day13-f4-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
<marker id="day13-f4-fail" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#f43f5e"/></marker>
<marker id="day13-f4-pass" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#34d399"/></marker>
</defs>

<!-- Initiating Event -->
<rect x="20" y="110" width="160" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/client.svg" x="35" y="125" width="22" height="22"/>
<text x="95" y="140" fill="#fce7f3" font-size="12" font-weight="700" text-anchor="middle">Payment Retry</text>
<text x="95" y="160" fill="#94a3b8" font-size="10" text-anchor="middle">Network Hiccup</text>
<text x="95" y="176" fill="#38bdf8" font-size="9.5" text-anchor="middle">HTTP POST /checkout</text>

<!-- Failed Path (Upper) -->
<path d="M180,135 L240,75" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#day13-f4-fail)"/>

<rect x="240" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/gcp/core/compute-engine.svg" x="255" y="38" width="22" height="22"/>
<image href="../assets/icons/generic/failure.svg" x="282" y="38" width="20" height="20"/>
<text x="355" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">[FAILED: In-Memory State]</text>
<text x="355" y="70" fill="#fce7f3" font-size="10" text-anchor="middle">Worker keeps local set()</text>
<text x="355" y="86" fill="#94a3b8" font-size="9.5" text-anchor="middle">Out-of-memory OOM crash</text>
<text x="355" y="102" fill="#f43f5e" font-size="9.5" text-anchor="middle">Deduplication cache lost</text>

<path d="M465,72 L525,72" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#day13-f4-fail)"/>

<rect x="525" y="25" width="225" height="95" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/failure.svg" x="540" y="38" width="22" height="22"/>
<text x="637" y="52" fill="#f43f5e" font-size="11" font-weight="700" text-anchor="middle">EXACT FAILURE POINT</text>
<text x="637" y="70" fill="#f43f5e" font-size="10" text-anchor="middle">Worker reboots clean</text>
<text x="637" y="86" fill="#f43f5e" font-size="9.5" text-anchor="middle">Retry re-executes payment</text>
<text x="637" y="102" fill="#94a3b8" font-size="9.5" text-anchor="middle">Customer charged twice ($120)</text>

<!-- Corrected Path (Lower) -->
<path d="M180,180 L240,240" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#day13-f4-pass)"/>

<rect x="240" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/gcp/core/cloud-sql.svg" x="255" y="208" width="22" height="22"/>
<image href="../assets/icons/generic/decision.svg" x="282" y="208" width="20" height="20"/>
<text x="355" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">[CORRECTED: External State]</text>
<text x="355" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">Stateless Worker Pattern</text>
<text x="355" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">Idempotency key passed</text>
<text x="355" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Cloud SQL UNIQUE (token)</text>

<path d="M465,242 L525,242" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#day13-f4-pass)"/>

<rect x="525" y="195" width="225" height="95" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/policy.svg" x="540" y="208" width="22" height="22"/>
<text x="637" y="222" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">IDEMPOTENT LOCK</text>
<text x="637" y="240" fill="#fce7f3" font-size="10" text-anchor="middle">ON CONFLICT DO NOTHING</text>
<text x="637" y="256" fill="#94a3b8" font-size="9.5" text-anchor="middle">Duplicate retry rejected</text>
<text x="637" y="272" fill="#34d399" font-size="9.5" text-anchor="middle">Existing receipt returned</text>

<!-- Outcome Verification Node -->
<path d="M750,242 L790,175" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#day13-f4-arr)"/>

<rect x="780" y="110" width="145" height="95" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/outcome.svg" x="795" y="125" width="22" height="22"/>
<text x="852" y="140" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle">VERIFICATION</text>
<text x="852" y="158" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">HTTP 200 Success</text>
<text x="852" y="174" fill="#fce7f3" font-size="9" text-anchor="middle">Exactly-Once Charge</text>
<text x="852" y="188" fill="#94a3b8" font-size="9" text-anchor="middle">Zero Duplication</text>
</svg>
</div>
<figcaption>Figure 13.4: Supplied facts: An API worker crash caused an in-memory deduplication set to be lost, triggering a duplicate fulfillment upon event replay. Architectural inference: Replaceable stateless workers must never store authoritative business state in process memory. Expected post-fix behavior: Enforcing primary key uniqueness in a durable database guarantees idempotent replay handling and prevents duplicate fulfillment.</figcaption>
</figure>'''
