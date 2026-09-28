part2_svg = """
<figure class="diagram-figure">
<svg role="img" aria-labelledby="d57-arch-title d57-arch-desc" viewBox="0 0 1060 620" width="100%" height="auto" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d57-arch-title">Hybrid BGP Dynamic Routing, On-Prem PGA Access &amp; Failover Fabric</title>
<desc id="d57-arch-desc">Comprehensive architectural diagram showing on-premises data center routers peering with dual Cloud Routers over primary Dedicated Interconnect (MED 100) and backup HA VPN (MED 200), custom route advertisement of restricted.googleapis.com (199.36.153.4/30), on-premises DNS forwarding, Andromeda SDN line-rate forwarding, and VPC workloads.</desc>
<defs>
<marker id="d57-m-primary" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
<marker id="d57-m-backup" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/>
</marker>
<marker id="d57-m-pga" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#38bdf8"/>
</marker>
<marker id="d57-m-bgp" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#c084fc"/>
</marker>
</defs>

<!-- Outer Canvas Boundary -->
<rect x="15" y="15" width="1030" height="590" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
<text x="35" y="42" fill="#f8fafc" font-size="16" font-weight="700">Hybrid BGP Dynamic Routing, On-Prem PGA Access &amp; Failover Fabric</text>
<text x="35" y="60" fill="#94a3b8" font-size="12">Deterministic MED Path Steering, Custom VIP Route Advertisement, On-Prem DNS Forwarding &amp; VPC-SC Security Perimeter</text>

<!-- Legend in top-right -->
<g transform="translate(620, 28)">
<line x1="0" y1="12" x2="25" y2="12" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d57-m-primary)"/>
<text x="32" y="16" fill="#86efac" font-size="10">Primary Path (MED 100)</text>
<line x1="140" y1="12" x2="165" y2="12" stroke="#f59e0b" stroke-width="2.5" marker-end="url(#d57-m-backup)"/>
<text x="172" y="16" fill="#fcd34d" font-size="10">Standby (MED 200)</text>
<line x1="260" y1="12" x2="285" y2="12" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#d57-m-pga)"/>
<text x="292" y="16" fill="#7dd3fc" font-size="10">PGA Flow</text>
<line x1="345" y1="12" x2="370" y2="12" stroke="#c084fc" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#d57-m-bgp)"/>
<text x="377" y="16" fill="#d8b4fe" font-size="10">BGP Control</text>
</g>

<!-- Column 1: Enterprise On-Premises Data Center -->
<rect x="35" y="80" width="245" height="505" rx="6" fill="#090d16" stroke="#475569" stroke-width="1.5"/>
<text x="50" y="105" fill="#f1f5f9" font-size="13" font-weight="700">Enterprise On-Premises DC</text>
<text x="50" y="122" fill="#94a3b8" font-size="11">ASN 65001 · Private LAN 172.16.0.0/16</text>

<!-- On-Prem PGA Client / Analytics Worker -->
<rect x="50" y="135" width="215" height="75" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
<text x="60" y="155" fill="#38bdf8" font-size="11" font-weight="700">Analytics Worker / PGA Client</text>
<text x="60" y="172" fill="#cbd5e1" font-size="10">IP: 172.16.10.50 | Port 443 Egress</text>
<text x="60" y="188" fill="#94a3b8" font-size="10">Queries storage.googleapis.com</text>
<text x="60" y="202" fill="#34d399" font-size="10">Routes via PGA VIP 199.36.153.4</text>

<!-- On-Prem DNS Server / Forwarder -->
<rect x="50" y="220" width="215" height="85" rx="4" fill="#1e293b" stroke="#60a5fa" stroke-width="1"/>
<text x="60" y="240" fill="#60a5fa" font-size="11" font-weight="700">Enterprise DNS Forwarder</text>
<text x="60" y="256" fill="#cbd5e1" font-size="10">IP: 172.16.0.10 (BIND / RPZ Policy)</text>
<text x="60" y="272" fill="#fcd34d" font-size="10">CNAME: *.googleapis.com -&gt;</text>
<text x="60" y="286" fill="#cbd5e1" font-size="10">restricted.googleapis.com (199.36.153.4/30)</text>
<text x="60" y="299" fill="#94a3b8" font-size="9">Prevents Public Internet DNS Leaks</text>

<!-- Stateful Perimeter Firewall -->
<rect x="50" y="315" width="215" height="70" rx="4" fill="#1e293b" stroke="#f43f5e" stroke-width="1"/>
<text x="60" y="335" fill="#fb7185" font-size="11" font-weight="700">Stateful Core Firewall Pair</text>
<text x="60" y="352" fill="#cbd5e1" font-size="10">State Sync across Interconnect/VPN</text>
<text x="60" y="368" fill="#f43f5e" font-size="10">Drops asymmetric TCP unestablished flows</text>

<!-- On-Prem Border Routers -->
<rect x="50" y="395" width="215" height="85" rx="4" fill="#1e293b" stroke="#3b82f6" stroke-width="1"/>
<text x="60" y="415" fill="#60a5fa" font-size="11" font-weight="700">Border Router R1 (Primary)</text>
<text x="60" y="431" fill="#cbd5e1" font-size="10">eBGP ASN 65001 | 100G Interconnect</text>
<text x="60" y="447" fill="#22c55e" font-size="10">Advertises MED 100 to GCP</text>
<text x="60" y="463" fill="#94a3b8" font-size="10">BFD Enabled: min-rx/tx 300ms, mult 3</text>

<rect x="50" y="490" width="215" height="85" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
<text x="60" y="510" fill="#fcd34d" font-size="11" font-weight="700">Border Router R2 (Standby)</text>
<text x="60" y="526" fill="#cbd5e1" font-size="10">eBGP ASN 65001 | Dual IPsec Tunnels</text>
<text x="60" y="542" fill="#f59e0b" font-size="10">Advertises MED 200 to GCP</text>
<text x="60" y="558" fill="#94a3b8" font-size="10">MSS Clamping: 1360 bytes (MTU 1440)</text>

<!-- Column 2: Hybrid Transit Fabric -->
<rect x="295" y="80" width="225" height="505" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
<text x="310" y="105" fill="#38bdf8" font-size="13" font-weight="700">Hybrid Transit Fabric</text>
<text x="310" y="122" fill="#94a3b8" font-size="11">Dual Physical &amp; Logical Paths</text>

<!-- Primary Dedicated Interconnect -->
<rect x="305" y="135" width="205" height="175" rx="4" fill="#132337" stroke="#22c55e" stroke-width="1.5"/>
<text x="315" y="155" fill="#4ade80" font-size="11" font-weight="700">Primary: Dedicated Interconnect</text>
<text x="315" y="172" fill="#cbd5e1" font-size="10">Bandwidth: 100 Gbps Optical Circuit</text>
<text x="315" y="188" fill="#38bdf8" font-size="10">Colo: Equinix Ashburn (EAD-1)</text>
<text x="315" y="204" fill="#cbd5e1" font-size="10">VLAN Attachment: vlan-ashburn-01</text>
<text x="315" y="220" fill="#22c55e" font-size="10">Active BGP Peer: MED 100</text>
<text x="315" y="236" fill="#cbd5e1" font-size="10">MTU: 1500 / 8896 Jumbo Frames</text>
<text x="315" y="252" fill="#38bdf8" font-size="10">PGA VIP 199.36.153.4/30 Advertised</text>
<text x="315" y="268" fill="#cbd5e1" font-size="10">Egress Cost: $0.02 / GB</text>
<text x="315" y="284" fill="#a7f3d0" font-size="10">Deterministic &lt;1.5ms Latency</text>

<!-- Backup Cloud HA VPN Gateway -->
<rect x="305" y="330" width="205" height="175" rx="4" fill="#2a1d12" stroke="#f59e0b" stroke-width="1.5"/>
<text x="315" y="350" fill="#fcd34d" font-size="11" font-weight="700">Backup: Cloud HA VPN</text>
<text x="315" y="367" fill="#cbd5e1" font-size="10">Bandwidth: 3 Gbps / Tunnel (ECMP)</text>
<text x="315" y="383" fill="#cbd5e1" font-size="10">Dual Public Interfaces (99.99% SLA)</text>
<text x="315" y="399" fill="#f59e0b" font-size="10">Standby BGP Peer: MED 200</text>
<text x="315" y="415" fill="#f87171" font-size="10">MTU: 1440 bytes (ESP Encapsulation)</text>
<text x="315" y="431" fill="#fcd34d" font-size="10">Mandatory TCP MSS Clamping (1360)</text>
<text x="315" y="447" fill="#cbd5e1" font-size="10">Internet Transit Egress: $0.085 / GB</text>
<text x="315" y="463" fill="#94a3b8" font-size="10">Jitter: 15ms-45ms (Public Internet)</text>
<text x="315" y="479" fill="#38bdf8" font-size="10">PGA VIP 199.36.153.4/30 Ingested</text>

<rect x="305" y="520" width="205" height="55" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="315" y="540" fill="#94a3b8" font-size="10" font-weight="600">Dynamic Failover Engine</text>
<text x="315" y="556" fill="#cbd5e1" font-size="10">BFD Sub-Second Failure Trip (&lt;900ms)</text>

<!-- Column 3: Google Cloud Edge & Control Plane -->
<rect x="535" y="80" width="240" height="505" rx="6" fill="#090d16" stroke="#475569" stroke-width="1.5"/>
<text x="550" y="105" fill="#f1f5f9" font-size="13" font-weight="700">Google Cloud Edge &amp; Control</text>
<text x="550" y="122" fill="#94a3b8" font-size="11">SDN Separation · ASN 16550</text>

<!-- Cloud Router 1 -->
<rect x="545" y="135" width="220" height="110" rx="4" fill="#1e293b" stroke="#3b82f6" stroke-width="1"/>
<text x="555" y="155" fill="#60a5fa" font-size="11" font-weight="700">Cloud Router 1 (us-central1)</text>
<text x="555" y="172" fill="#cbd5e1" font-size="10">Control Plane Daemon (Bird/Quagga)</text>
<text x="555" y="188" fill="#22c55e" font-size="10">Interconnect Peer: MED 100</text>
<text x="555" y="204" fill="#38bdf8" font-size="10">Custom Advert: 10.10.0.0/16, 199.36.153.4/30</text>
<text x="555" y="220" fill="#cbd5e1" font-size="10">Learned Route Quota: 100 Prefixes</text>
<text x="555" y="236" fill="#60a5fa" font-size="10">BFD Enabled: 300ms x 3 Multiplier</text>

<!-- Cloud Router 2 -->
<rect x="545" y="255" width="220" height="80" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
<text x="555" y="275" fill="#fcd34d" font-size="11" font-weight="700">Cloud Router 2 (us-central1)</text>
<text x="555" y="291" fill="#cbd5e1" font-size="10">VPN Peer: MED 200 (Standby)</text>
<text x="555" y="307" fill="#38bdf8" font-size="10">Custom Advert: 10.10.0.0/16, 199.36.153.4/30</text>
<text x="555" y="323" fill="#94a3b8" font-size="10">Keepalive 20s | Hold Timer 60s</text>

<!-- Andromeda SDN Fabric -->
<rect x="545" y="345" width="220" height="110" rx="4" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
<text x="555" y="365" fill="#c7d2fe" font-size="11" font-weight="700">Andromeda SDN Controller</text>
<text x="555" y="382" fill="#cbd5e1" font-size="10">Data Plane Separation (No Bottleneck)</text>
<text x="555" y="398" fill="#a5b4fc" font-size="10">Compiles BGP Routes into Host Flow Tables</text>
<text x="555" y="414" fill="#cbd5e1" font-size="10">Line-Rate Wire Forwarding in vSwitch</text>
<text x="555" y="430" fill="#34d399" font-size="10">Sub-Microsecond Transit Latency</text>
<text x="555" y="446" fill="#cbd5e1" font-size="10">Direct Host-to-Edge Encapsulation</text>

<!-- Cloud NAT Gateway -->
<rect x="545" y="465" width="220" height="105" rx="4" fill="#1e293b" stroke="#06b6d4" stroke-width="1"/>
<text x="555" y="485" fill="#22d3ee" font-size="11" font-weight="700">Cloud NAT Gateway (nat-gw-prod)</text>
<text x="555" y="501" fill="#cbd5e1" font-size="10">Dynamic Port Allocation Enabled</text>
<text x="555" y="517" fill="#38bdf8" font-size="10">Min Ports Per VM: 1024 (avoid 64 limit)</text>
<text x="555" y="533" fill="#cbd5e1" font-size="10">Max Ports: 4096 | Dedicated IP Pool</text>
<text x="555" y="549" fill="#94a3b8" font-size="9">Protects against OUT_OF_RESOURCES</text>

<!-- Column 4: Google Cloud VPC & Private APIs -->
<rect x="790" y="80" width="240" height="505" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
<text x="805" y="105" fill="#38bdf8" font-size="13" font-weight="700">Google Cloud VPC &amp; PGA Target</text>
<text x="805" y="122" fill="#94a3b8" font-size="11">Production VPC · us-central1</text>

<!-- VPC Workloads Subnet -->
<rect x="800" y="135" width="220" height="120" rx="4" fill="#1e293b" stroke="#3b82f6" stroke-width="1"/>
<text x="810" y="155" fill="#60a5fa" font-size="11" font-weight="700">Production Workload Subnet</text>
<text x="810" y="172" fill="#cbd5e1" font-size="10">CIDR: 10.10.0.0/16 (us-central1)</text>
<text x="810" y="188" fill="#94a3b8" font-size="10">GKE Node Pools &amp; Core Microservices</text>
<text x="810" y="204" fill="#cbd5e1" font-size="10">Cloud SQL Private IP: 10.10.50.12</text>
<text x="810" y="220" fill="#34d399" font-size="10">Symmetric Return via Andromeda</text>
<text x="810" y="236" fill="#60a5fa" font-size="10">MTU: 1460 / 1500 bytes</text>

<!-- Restricted Google APIs VIP -->
<rect x="800" y="265" width="220" height="145" rx="4" fill="#052e16" stroke="#22c55e" stroke-width="1.5"/>
<text x="810" y="285" fill="#4ade80" font-size="11" font-weight="700">Restricted Google API VIP</text>
<text x="810" y="302" fill="#86efac" font-size="10">VIP: 199.36.153.4/30 (restricted.googleapis.com)</text>
<text x="810" y="318" fill="#cbd5e1" font-size="10">Target Services:</text>
<text x="820" y="334" fill="#38bdf8" font-size="10">• Cloud Storage (GCS) Buckets</text>
<text x="820" y="350" fill="#38bdf8" font-size="10">• BigQuery Enterprise Analytics</text>
<text x="820" y="366" fill="#38bdf8" font-size="10">• Cloud KMS Cryptographic Keys</text>
<text x="810" y="382" fill="#cbd5e1" font-size="10">Non-routable over public internet</text>
<text x="810" y="398" fill="#4ade80" font-size="10">Symmetric Return to On-Prem 172.16.0.0/16</text>

<!-- VPC Service Controls Perimeter -->
<rect x="800" y="420" width="220" height="150" rx="4" fill="#2d1537" stroke="#d946ef" stroke-width="1.5"/>
<text x="810" y="440" fill="#f0abfc" font-size="11" font-weight="700">VPC Service Controls Perimeter</text>
<text x="810" y="457" fill="#e879f9" font-size="10">Service Perimeter: sp_prod_data</text>
<text x="810" y="473" fill="#cbd5e1" font-size="10">Enforces Zero Data Exfiltration</text>
<text x="810" y="489" fill="#f0abfc" font-size="10">Restricted VIP Binds to Perimeter</text>
<text x="810" y="505" fill="#f87171" font-size="10">Blocks Public Internet API Ingress</text>
<text x="810" y="521" fill="#cbd5e1" font-size="10">Validates On-Prem Client IP &amp; IAM Token</text>
<text x="810" y="537" fill="#34d399" font-size="10">Audit Logs: Access Approved</text>
<text x="810" y="553" fill="#94a3b8" font-size="9">Rejects non-whitelisted GCP projects</text>

<!-- Connecting Path Lines -->
<!-- 1. Primary Dedicated Interconnect Line: On-Prem R1 -> Interconnect -> Cloud Router 1 / Andromeda -->
<path d="M 265 435 L 305 220" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d57-m-primary)"/>
<path d="M 510 220 L 545 190" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d57-m-primary)"/>
<path d="M 765 190 L 800 190" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d57-m-primary)"/>

<!-- 2. PGA Client Flow: Worker -> DNS -> R1 -> Interconnect -> Andromeda -> Restricted VIP -->
<path d="M 155 210 L 155 220" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#d57-m-pga)"/>
<path d="M 265 175 C 290 175, 290 240, 305 240" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#d57-m-pga)"/>
<path d="M 510 240 C 530 240, 530 380, 545 380" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#d57-m-pga)"/>
<path d="M 765 380 C 785 380, 785 320, 800 320" fill="none" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#d57-m-pga)"/>

<!-- 3. Standby HA VPN Line: On-Prem R2 -> HA VPN -> Cloud Router 2 -->
<path d="M 265 530 L 305 415" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#d57-m-backup)"/>
<path d="M 510 415 L 545 295" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#d57-m-backup)"/>

<!-- 4. BGP Control Plane Peering Line: Router R1/R2 to Cloud Router 1/2 -->
<path d="M 265 450 C 285 450, 520 230, 545 210" fill="none" stroke="#c084fc" stroke-width="1.5" stroke-dasharray="4,4" marker-end="url(#d57-m-bgp)"/>
</svg>
<figcaption>Figure 57.1: Enterprise Hybrid Dynamic Routing and On-Premises Private Google Access Fabric. <strong>Supplied facts:</strong> Dedicated Interconnect operates as primary transit (MED 100) and Cloud HA VPN acts as standby (MED 200). On-premises hosts access Google APIs via restricted VIP <code>199.36.153.4/30</code> without internet transit. <strong>Architectural inference:</strong> Cloud Router separates control plane from Andromeda SDN line-rate forwarding. Custom BGP advertisements guide on-prem traffic to the private VIP, while BFD sub-second timers prevent hold timer blackholes. <strong>Expected post-fix behavior:</strong> API requests route over private optical fiber into VPC-SC protected storage buckets with deterministic sub-millisecond jitter and automatic sub-second failover.</figcaption>
</figure>
"""
print("Part 2 SVG defined, length:", len(part2_svg))
