#!/usr/bin/env python3
"""Script to elevate content/day-049-page.html to the highest architectural standard."""
import re
from pathlib import Path
from bs4 import BeautifulSoup

def elevate_day49():
    page_path = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site/content/day-049-page.html")
    html = page_path.read_text()

    # 1. Update Exit Artifact references from day-049-vpc-ip-plan.md to day-049-ip-plan.md
    html = html.replace("day-049-vpc-ip-plan.md", "day-049-ip-plan.md")

    # 2. In Topic 2 Technical Discussion, add Subnet Reserved IP Allocation Table
    old_topic2_text = """<p>Consequently, the usable host capacity for any subnet primary range is calculated as: $$\\text{Usable Hosts} = 2^{(32 - \\text{prefix})} - 4$$</p>"""
    
    new_topic2_table = """<p>Consequently, the usable host capacity for any subnet primary range is calculated as: $$\\text{Usable Hosts} = 2^{(32 - \\text{prefix})} - 4$$</p>

<div class="table-wrap">
<table>
<caption>Table 49.2: Subnet Reserved IP Allocation Table (Primary vs. Secondary &amp; GCP vs. AWS VPC Comparison)</caption>
<thead>
<tr>
<th scope="col">Address Offset / Role</th>
<th scope="col">Example (/24 Subnet)</th>
<th scope="col">Example (/22 Subnet)</th>
<th scope="col">Andromeda SDN Function</th>
<th scope="col">Assignable to Host?</th>
<th scope="col">Secondary Range Behavior</th>
<th scope="col">AWS VPC Comparison</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>First IP (Offset .0)</strong></td>
<td><code>10.10.0.0</code></td>
<td><code>10.10.0.0</code></td>
<td>Network identifier / base subnet address.</td>
<td>No</td>
<td><strong>Usable!</strong> (0 reserved IPs)</td>
<td>Reserved (Network address)</td>
</tr>
<tr>
<td><strong>Second IP (Offset .1)</strong></td>
<td><code>10.10.0.1</code></td>
<td><code>10.10.0.1</code></td>
<td>Local subnet default gateway; virtualized by Andromeda (does not consume VM NIC or respond to ICMP ping).</td>
<td>No</td>
<td><strong>Usable!</strong> (0 reserved IPs)</td>
<td>Reserved (VPC router gateway)</td>
</tr>
<tr>
<td><strong>Third IP (Offset .2)</strong></td>
<td><code>10.10.0.2</code></td>
<td><code>10.10.0.2</code></td>
<td><strong>Fully usable</strong> for Compute Engine VMs and GKE worker nodes.</td>
<td>Yes</td>
<td><strong>Usable!</strong> (0 reserved IPs)</td>
<td>Reserved (AWS DNS resolver)</td>
</tr>
<tr>
<td><strong>Fourth IP (Offset .3)</strong></td>
<td><code>10.10.0.3</code></td>
<td><code>10.10.0.3</code></td>
<td><strong>Fully usable</strong> for Compute Engine VMs and GKE worker nodes.</td>
<td>Yes</td>
<td><strong>Usable!</strong> (0 reserved IPs)</td>
<td>Reserved (Future expansion)</td>
</tr>
<tr>
<td><strong>Second-to-Last IP</strong></td>
<td><code>10.10.0.254</code></td>
<td><code>10.10.3.254</code></td>
<td>Reserved by Google Cloud for DHCP lease server coordination and internal platform capabilities.</td>
<td>No</td>
<td><strong>Usable!</strong> (0 reserved IPs)</td>
<td>Assignable host IP</td>
</tr>
<tr>
<td><strong>Last IP (Broadcast)</strong></td>
<td><code>10.10.0.255</code></td>
<td><code>10.10.3.255</code></td>
<td>RFC standard broadcast address; Andromeda drops layer 2 broadcast frames.</td>
<td>No</td>
<td><strong>Usable!</strong> (0 reserved IPs)</td>
<td>Reserved (Broadcast address)</td>
</tr>
<tr>
<td><strong>Summary Capacity</strong></td>
<td>252 usable hosts</td>
<td>1,020 usable hosts</td>
<td>Formula: 2^(32 &minus; prefix) &minus; 4 for primary ranges.</td>
<td>&mdash;</td>
<td>2^(32 &minus; prefix) (100% usable)</td>
<td>Formula: 2^(32 &minus; prefix) &minus; 5</td>
</tr>
</tbody>
</table>
</div>"""
    if old_topic2_text in html:
        html = html.replace(old_topic2_text, new_topic2_table)
        print("Replaced Topic 2 table")
    else:
        print("WARNING: old_topic2_text not matched!")

    # 3. Update Table numbering
    html = html.replace("<caption>Table 49.2: Comparison: Auto Mode vs. Custom Mode VPCs</caption>",
                        "<caption>Table 49.3: Comparison: Auto Mode vs. Custom Mode VPCs (Enterprise IP Governance &amp; Risk Matrix)</caption>")
    html = html.replace("<caption>Table 49.3: GCP Route Types and Default Precedence</caption>",
                        "<caption>Table 49.4: GCP System vs. Static vs. Dynamic Routes &amp; Next-Hop Selection Matrix</caption>")

    # 4. Expand Routes Table to include next-hop ILB, next-hop IP, next-hop instance, next-hop VPN, and regional vs global dynamic modes
    old_routes_table = """<div class="table-wrap">
<table>
<caption>Table 49.4: GCP System vs. Static vs. Dynamic Routes &amp; Next-Hop Selection Matrix</caption>
<thead>
<tr>
<th scope="col">Route Type</th>
<th scope="col">Destination Range</th>
<th scope="col">Default Priority</th>
<th scope="col">Next Hop</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Default Subnet Route</strong></td>
<td>Primary &amp; Secondary Subnet CIDRs</td>
<td>0</td>
<td>Local VPC network fabric (Andromeda)</td>
</tr>
<tr>
<td><strong>Default Internet Gateway Route</strong></td>
<td><code>0.0.0.0/0</code></td>
<td>1000</td>
<td>Default Internet Gateway</td>
</tr>
<tr>
<td><strong>Custom Static Route</strong></td>
<td>Configured IP range (e.g. <code>192.168.0.0/16</code>)</td>
<td>User-defined (e.g. 100–1000)</td>
<td>Next-hop VM instance, VPN tunnel, or internal load balancer</td>
</tr>
<tr>
<td><strong>Dynamic BGP Route</strong></td>
<td>Learned from on-premises peer via BGP</td>
<td>Determined by BGP MED and Cloud Router base priority</td>
<td>Cloud Interconnect / Cloud VPN tunnel</td>
</tr>
</tbody>
</table>
</div>"""

    new_routes_table = """<div class="table-wrap">
<table>
<caption>Table 49.4: GCP System vs. Static vs. Dynamic Routes &amp; Next-Hop Selection Matrix</caption>
<thead>
<tr>
<th scope="col">Route Category</th>
<th scope="col">Destination Prefix</th>
<th scope="col">Next-Hop Target Type</th>
<th scope="col">Default Priority</th>
<th scope="col">Dynamic Routing Scope</th>
<th scope="col">Andromeda Resolution Behavior</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Default Subnet Route (System)</strong></td>
<td>Primary &amp; Secondary Subnet CIDRs</td>
<td>Local VPC network fabric (Andromeda SDN)</td>
<td>0 (Fixed)</td>
<td>Global across all regions</td>
<td>Always preferred over static and dynamic routes for intra-subnet and cross-subnet communication within the VPC.</td>
</tr>
<tr>
<td><strong>Default Internet Gateway (System)</strong></td>
<td><code>0.0.0.0/0</code></td>
<td><code>default-internet-gateway</code></td>
<td>1000</td>
<td>Global across all regions</td>
<td>Provides direct outbound internet egress; overridden by any custom route to <code>0.0.0.0/0</code> with priority &lt; 1000.</td>
</tr>
<tr>
<td><strong>Custom Static Route (Next-Hop Instance)</strong></td>
<td>Configured CIDR (e.g. <code>192.168.0.0/16</code>)</td>
<td>Specific Compute Engine VM instance / NIC</td>
<td>User-defined (0–65535)</td>
<td>Global or filtered by network tags</td>
<td>Directs traffic to a single Network Virtual Appliance (NVA). If VM fails, traffic blackholes unless managed by external scripts.</td>
</tr>
<tr>
<td><strong>Custom Static Route (Next-Hop IP)</strong></td>
<td>Configured CIDR</td>
<td>Internal IP address in the subnet</td>
<td>User-defined (0–65535)</td>
<td>Global or network tagged</td>
<td>Routes to an IP within the VPC; useful for third-party virtual appliance interfaces and secondary IP addresses.</td>
</tr>
<tr>
<td><strong>Custom Static Route (Next-Hop ILB)</strong></td>
<td>Configured CIDR</td>
<td>Internal Passthrough Network Load Balancer (VIP)</td>
<td>User-defined (0–65535)</td>
<td>Regional (ILB VIP scope)</td>
<td><strong>Enterprise Best Practice:</strong> Routes traffic across a pool of health-checked NVA firewalls with automatic health-based failover.</td>
</tr>
<tr>
<td><strong>Custom Static Route (Next-Hop VPN)</strong></td>
<td>Configured CIDR</td>
<td>Cloud Classic / HA VPN Tunnel</td>
<td>User-defined (0–65535)</td>
<td>Regional or Global</td>
<td>Routes traffic into an IPsec tunnel; static failover requires managing route priorities across redundant tunnels.</td>
</tr>
<tr>
<td><strong>Dynamic BGP Route (Cloud Router — Regional Mode)</strong></td>
<td>Learned from on-premise BGP peer</td>
<td>Cloud Interconnect / Cloud VPN attachment</td>
<td>BGP MED + Base Priority (e.g. 100)</td>
<td><strong>Regional dynamic mode</strong></td>
<td>Only subnets in the Cloud Router's local region learn the route. Workloads in remote regions cannot reach on-prem without regional transit.</td>
</tr>
<tr>
<td><strong>Dynamic BGP Route (Cloud Router — Global Mode)</strong></td>
<td>Learned from on-premise BGP peer</td>
<td>Cloud Interconnect / Cloud VPN attachment</td>
<td>BGP MED + Base Priority (+ metric for remote)</td>
<td><strong>Global dynamic mode</strong></td>
<td><strong>Enterprise Standard:</strong> All subnets across all global regions learn the route. Remote regions automatically add latency metric (typically 200).</td>
</tr>
</tbody>
</table>
</div>"""

    if old_routes_table in html:
        html = html.replace(old_routes_table, new_routes_table)
        print("Replaced Routes table")
    else:
        print("WARNING: old_routes_table not matched!")

    # 5. Replace Part 2 Architecture SVG with complete comprehensive visual
    # Finding current figure with id d49-arch-title
    arch_svg_start = html.find('<!-- Part 2 Architecture SVG -->')
    arch_svg_end = html.find('</figure>', arch_svg_start) + len('</figure>')

    new_arch_svg = """<!-- Part 2 Architecture SVG -->
<figure class="diagram-figure">
<svg role="img" aria-labelledby="d49-arch-title d49-arch-desc" viewBox="0 0 1000 580" width="100%" height="auto" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d49-arch-title">Google Cloud Global VPC, Regional Subnets, GKE Secondary Ranges, Dynamic BGP and Andromeda Precedence Engine</title>
<desc id="d49-arch-desc">Comprehensive architecture diagram showing a global VPC spanning us-central1 and us-east1 over Jupiter and B4 private fiber, regional subnets with primary and secondary IP ranges, Cloud Router dynamic BGP peering with on-premises networks, and the 3-tier Andromeda route selection precedence hierarchy.</desc>
<defs>
<marker id="d49-arch-arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#38bdf8"/>
</marker>
<marker id="d49-arch-g-arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
<marker id="d49-arch-amb-arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/>
</marker>
</defs>

<!-- Global VPC Outer Container -->
<rect x="20" y="20" width="960" height="540" rx="8" fill="#0d111f" stroke="#1e293b" stroke-width="2"/>
<text x="35" y="42" fill="#38bdf8" font-size="13" font-weight="700">GLOBAL VPC NETWORK: brightloaf-enterprise-vpc (Custom Mode, Andromeda SDN Fabric, Global Control Plane)</text>

<!-- Region 1: us-central1 -->
<rect x="35" y="60" width="445" height="270" rx="6" fill="#161b33" stroke="#38bdf8" stroke-width="1.2"/>
<text x="50" y="82" fill="#38bdf8" font-size="12" font-weight="700">REGION: us-central1 (Iowa — Spans Zones a, b, c, f)</text>

<!-- Subnet us-central1 -->
<rect x="50" y="95" width="415" height="220" rx="4" fill="#0d111f" stroke="#1e293b" stroke-width="1"/>
<text x="65" y="115" fill="#fce7f3" font-size="11" font-weight="700">Subnet: prod-us-central1-app (Regional Blast Radius)</text>
<text x="65" y="132" fill="#22c55e" font-size="10">Primary CIDR: 10.10.0.0/22 (1,020 usable VM &amp; Node IPs)</text>

<!-- Primary allocation details -->
<rect x="65" y="142" width="385" height="42" rx="3" fill="#161b33" stroke="#1e293b" stroke-width="1"/>
<text x="75" y="158" fill="#a9b7cb" font-size="9">GCP Reserved: .0 (Net), .1 (GW), .3.254 (Google Reserved), .3.255 (Brdcst)</text>
<text x="75" y="174" fill="#fce7f3" font-size="9">Usable Pool: 10.10.0.2 – 10.10.3.253 (Worker VMs, Internal LBs, Proxies)</text>

<!-- Secondary ranges -->
<rect x="65" y="192" width="385" height="110" rx="3" fill="#122822" stroke="#22c55e" stroke-width="1"/>
<text x="75" y="210" fill="#22c55e" font-size="10" font-weight="700">GKE IP Alias Secondary Ranges (0 Reserved IPs!)</text>
<text x="75" y="228" fill="#fce7f3" font-size="9">• Pod CIDR: 10.20.0.0/16 (65,536 Pod IPs, /24 per node for 110 pods)</text>
<text x="75" y="246" fill="#fce7f3" font-size="9">• Service CIDR: 10.30.0.0/20 (4,096 ClusterIP Service addresses)</text>
<text x="75" y="264" fill="#a9b7cb" font-size="9">VPC-native routing: direct pod-to-pod packet encapsulation</text>
<text x="75" y="282" fill="#38bdf8" font-size="9">Cloud Router: cr-us-central1 (Google ASN 65001, Global Routing Mode)</text>

<!-- Region 2: us-east1 -->
<rect x="520" y="60" width="445" height="270" rx="6" fill="#161b33" stroke="#38bdf8" stroke-width="1.2"/>
<text x="535" y="82" fill="#38bdf8" font-size="12" font-weight="700">REGION: us-east1 (S. Carolina — Spans Zones b, c, d)</text>

<!-- Subnet us-east1 -->
<rect x="535" y="95" width="415" height="220" rx="4" fill="#0d111f" stroke="#1e293b" stroke-width="1"/>
<text x="550" y="115" fill="#fce7f3" font-size="11" font-weight="700">Subnet: prod-us-east1-dr (Regional Blast Radius)</text>
<text x="550" y="132" fill="#22c55e" font-size="10">Primary CIDR: 10.11.0.0/22 (1,020 usable DR &amp; DB IPs)</text>

<!-- Primary allocation details -->
<rect x="550" y="142" width="385" height="42" rx="3" fill="#161b33" stroke="#1e293b" stroke-width="1"/>
<text x="560" y="158" fill="#a9b7cb" font-size="9">GCP Reserved: .0 (Net), .1 (GW), .3.254 (Google Reserved), .3.255 (Brdcst)</text>
<text x="560" y="174" fill="#fce7f3" font-size="9">Usable Pool: 10.11.0.2 – 10.11.3.253 (DR Compute, Replica DBs)</text>

<!-- Secondary ranges -->
<rect x="550" y="192" width="385" height="110" rx="3" fill="#122822" stroke="#22c55e" stroke-width="1"/>
<text x="560" y="210" fill="#22c55e" font-size="10" font-weight="700">GKE IP Alias Secondary Ranges (DR Cluster)</text>
<text x="560" y="228" fill="#fce7f3" font-size="9">• Pod CIDR: 10.21.0.0/16 (65,536 Pod IPs, /24 per node)</text>
<text x="560" y="246" fill="#fce7f3" font-size="9">• Service CIDR: 10.31.0.0/20 (4,096 ClusterIP addresses)</text>
<text x="560" y="264" fill="#a9b7cb" font-size="9">Non-overlapping with us-central1; enables active-active failover</text>
<text x="560" y="282" fill="#38bdf8" font-size="9">Cloud Router: cr-us-east1 (Google ASN 65001, Global Routing Mode)</text>

<!-- Center WAN Backbone Connection -->
<path d="M 480 180 L 520 180" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#d49-arch-arr)"/>
<path d="M 520 200 L 480 200" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#d49-arch-arr)"/>
<rect x="470" y="215" width="60" height="25" rx="3" fill="#0d111f" stroke="#38bdf8" stroke-width="1"/>
<text x="475" y="231" fill="#38bdf8" font-size="8" font-weight="700">B4 WAN</text>

<!-- Hybrid BGP Peering (Bottom Left) -->
<rect x="35" y="345" width="445" height="200" rx="6" fill="#161b33" stroke="#f59e0b" stroke-width="1.2"/>
<text x="50" y="365" fill="#f59e0b" font-size="11" font-weight="700">HYBRID CLOUD ROUTER BGP PEERING (Global Dynamic Routing Mode)</text>
<rect x="50" y="375" width="415" height="155" rx="4" fill="#0d111f" stroke="#1e293b" stroke-width="1"/>
<text x="60" y="393" fill="#fce7f3" font-size="10" font-weight="700">Cloud Router cr-us-central1 (ASN 65001) ⇄ On-Premises Core (ASN 65010)</text>
<text x="60" y="411" fill="#22c55e" font-size="9">• Primary Path: Dedicated Cloud Interconnect (10 Gbps, BGP Base Priority 100)</text>
<text x="60" y="427" fill="#f59e0b" font-size="9">• Backup Path: Cloud HA VPN Tunnel (IPsec 3 Gbps, BGP Base Priority 200)</text>
<text x="60" y="445" fill="#a9b7cb" font-size="9">Dynamic Route Advertisement: Advertises all VPC subnets (10.10.0.0/22, 10.11.0.0/22)</text>
<text x="60" y="463" fill="#a9b7cb" font-size="9">Learned Dynamic Route: 192.168.0.0/16 learned from on-premises datacenter</text>
<text x="60" y="481" fill="#38bdf8" font-size="9">Global Propagation: Remote region us-east1 receives 192.168.0.0/16 with latency metric</text>
<text x="60" y="499" fill="#fce7f3" font-size="9">Failover Mechanism: BGP withdrawal of Interconnect triggers instant VPN failover (&lt;3s)</text>

<!-- Andromeda Route Precedence Engine (Bottom Right) -->
<rect x="520" y="345" width="445" height="200" rx="6" fill="#161b33" stroke="#22c55e" stroke-width="1.2"/>
<text x="535" y="365" fill="#22c55e" font-size="11" font-weight="700">ANDROMEDA DETERMINISTIC ROUTE SELECTION HIERARCHY</text>
<rect x="535" y="375" width="415" height="155" rx="4" fill="#0d111f" stroke="#1e293b" stroke-width="1"/>
<text x="545" y="393" fill="#38bdf8" font-size="10" font-weight="700">1. Longest Prefix Match (LPM) — Most Specific Destination Mask Always Wins</text>
<text x="555" y="409" fill="#fce7f3" font-size="9">10.10.1.50/32 (Host) &gt; 10.10.0.0/22 (Subnet) &gt; 10.0.0.0/8 (Summary) &gt; 0.0.0.0/0</text>
<text x="545" y="431" fill="#f59e0b" font-size="10" font-weight="700">2. Lowest Numerical Priority (Admin Distance) — Resolves Prefix Length Ties</text>
<text x="555" y="447" fill="#fce7f3" font-size="9">Local Subnet (Prio 0) &gt; Interconnect (Prio 100) &gt; VPN (Prio 200) &gt; Internet (Prio 1000)</text>
<text x="545" y="469" fill="#22c55e" font-size="10" font-weight="700">3. Equal-Cost Multi-Path (ECMP) — 5-Tuple Packet Flow Hashing</text>
<text x="555" y="485" fill="#fce7f3" font-size="9">Hashed across src/dst IP, src/dst port, protocol when prefixes and priorities match</text>
<text x="545" y="507" fill="#a9b7cb" font-size="9">Deterministic Resolution: Eliminates routing loops and nondeterministic path selection</text>
</svg>
<figcaption>
<strong>What this depicts:</strong> Enterprise Google Cloud Global VPC architecture. Two regional subnets (<code>us-central1</code> and <code>us-east1</code>) span availability zones within their respective regions, supporting primary host allocations and non-overlapping GKE secondary IP ranges for Pods and Services; Cloud Routers establish hybrid dynamic BGP peering with on-premises data centers under Global Dynamic Routing mode; and Andromeda's distributed routing engine evaluates longest prefix match, administrative priority, and ECMP hashing to enforce deterministic packet forwarding across Google's private optical B4 WAN.<br>
<strong>Scope:</strong> Global VPC networking, regional subnetting boundaries, GKE IP alias calculation, Cloud Router BGP configuration, and Andromeda route resolution hierarchy.<br>
<strong>What it does not prove:</strong> It does not prove that inter-region network latency meets sub-5ms SLAs during transatlantic subsea fiber disruptions, nor does it configure Cloud Armor edge DDoS protection.
</figcaption>
</figure>"""

    if arch_svg_start != -1 and arch_svg_end != -1:
        html = html[:arch_svg_start] + new_arch_svg + html[arch_svg_end:]
        print("Replaced Part 2 Architecture SVG")
    else:
        print("WARNING: arch_svg markers not found!")

    # 6. Elevate Part 3 Incidents 1 to 5 SVGs
    for i in range(1, 6):
        # Update markers and paths
        # Replace marker defs for incident i
        # Replace stroke-dasharray="4,4" with stroke-dasharray="6,4"
        # Replace stroke="#34d399" with stroke="#22c55e" stroke-width="2.5"
        # Replace stroke="#38bdf8" in verify boundary with stroke="#f59e0b" stroke-width="1.8"
        # Ensure unique marker IDs: d49-i{i}-f and d49-i{i}-c
        pass

    # Let's do regex replacements for the incident SVGs
    # Fix dashed stroke-dasharray
    html = re.sub(r'stroke="#f43f5e"\s+stroke-width="2"\s+stroke-dasharray="4,4"',
                  'stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4"', html)
    # Fix corrected stroke-width and color
    html = re.sub(r'stroke="#34d399"\s+stroke-width="2"',
                  'stroke="#22c55e" stroke-width="2.5"', html)
    # Fix corrected marker fill
    html = re.sub(r'<polygon points="0 0, 8 4, 0 8" fill="#34d399"/>',
                  '<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>', html)
    # Fix corrected text and border in incident boxes
    html = html.replace('stroke="#34d399" stroke-width="1.2"', 'stroke="#22c55e" stroke-width="1.2"')
    html = html.replace('stroke="#34d399" stroke-width="1"', 'stroke="#22c55e" stroke-width="1"')
    html = html.replace('fill="#34d399"', 'fill="#22c55e"')

    # Fix Verify Boundary stroke and text color from cyan #38bdf8 to amber #f59e0b in incident SVGs
    html = re.sub(r'<rect x="550" y="140" width="220" height="105" rx="6" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="6,3"/>\s*<text x="560" y="155" fill="#38bdf8" font-size="9" font-weight="700">VERIFY BOUNDARY</text>',
                  '<rect x="550" y="140" width="220" height="105" rx="6" fill="none" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="6,3"/>\n<text x="560" y="155" fill="#f59e0b" font-size="9" font-weight="700">VERIFY BOUNDARY</text>', html)

    # Fix marker URLs in Incidents 3, 4, 5
    # In Incident 3:
    inc3_start = html.find('id="d49-i3-title"')
    if inc3_start != -1:
        inc3_end = html.find('</figure>', inc3_start)
        inc3_chunk = html[inc3_start:inc3_end]
        inc3_chunk_fixed = inc3_chunk.replace('url(#d49-i1-f)', 'url(#d49-i3-f)').replace('url(#d49-i1-c)', 'url(#d49-i3-c)')
        html = html[:inc3_start] + inc3_chunk_fixed + html[inc3_end:]
        print("Fixed Incident 3 markers")

    # In Incident 4:
    inc4_start = html.find('id="d49-i4-title"')
    if inc4_start != -1:
        inc4_end = html.find('</figure>', inc4_start)
        inc4_chunk = html[inc4_start:inc4_end]
        inc4_chunk_fixed = inc4_chunk.replace('url(#d49-i1-f)', 'url(#d49-i4-f)').replace('url(#d49-i1-c)', 'url(#d49-i4-c)')
        html = html[:inc4_start] + inc4_chunk_fixed + html[inc4_end:]
        print("Fixed Incident 4 markers")

    # In Incident 5:
    inc5_start = html.find('id="d49-i5-title"')
    if inc5_start != -1:
        inc5_end = html.find('</figure>', inc5_start)
        inc5_chunk = html[inc5_start:inc5_end]
        inc5_chunk_fixed = inc5_chunk.replace('url(#d49-i1-f)', 'url(#d49-i5-f)').replace('url(#d49-i1-c)', 'url(#d49-i5-c)')
        html = html[:inc5_start] + inc5_chunk_fixed + html[inc5_end:]
        print("Fixed Incident 5 markers")

    # Write out updated content
    page_path.write_text(html)
    print(f"Successfully elevated {page_path} ({len(html)} bytes)")

if __name__ == "__main__":
    elevate_day49()
