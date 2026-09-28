part3_html = """
<section id="part-3" class="part">
<h2>3 · Field case incidents and solutions</h2>

<article id="topic-01-problem" class="topic-card">
<h3>Asymmetric Routing Blackhole and 60-Second Hold Timer Stall During Primary Interconnect Flap · field case</h3>
<p><strong>Situation and impact:</strong> Brightloaf's hybrid payment processing platform links on-premises core banking mainframe ledgers with cloud microservices in <code>us-central1</code>. Primary transit operates across a 100G Dedicated Interconnect circuit in Ashburn (EAD-1); backup transit operates across a dual-tunnel Cloud HA VPN gateway. During routine patch panel re-cabling in the on-premises data center, a technician accidentally bounced the primary optical fiber pair. The Cloud Router was configured with default advertised route priority <code>100</code> on both Interconnect and VPN, while the on-premises border router advertised MED <code>50</code> on Interconnect and MED <code>100</code> on VPN. When the optic was pulled, the on-premises router immediately withdrew the Interconnect route and shifted all outbound traffic to HA VPN (MED 100). However, because the link failure occurred behind an intermediate unmanaged DWDM multiplexer, Google's edge interface remained physically UP and never received a clean BGP NOTIFICATION message. Cloud Router continued forwarding return traffic into the dead Interconnect circuit for the full <strong>60-second BGP hold timer window</strong>. Even worse, once the hold timer expired and Cloud Router shifted return traffic to the VPN, the on-premises stateful core firewalls dropped all return packets because the forward TCP SYN had bypassed the VPN interface (asymmetric routing). All hybrid payment transactions failed for 8 minutes, stranding $340,000 in checkout transactions during morning rush hour.</p>

<p><strong>Constraints:</strong> Must achieve sub-second failover (&lt;1s) on physical transport drops without manual intervention; must guarantee symmetric bidirectional traffic across hybrid interfaces to prevent stateful firewall connection drops; must maintain 99.99% availability SLA.</p>

<p><strong>Diagnostic sequence and root cause:</strong></p>
<ol>
<li>Inspected BGP peering status on Cloud Router:
<pre><code>gcloud compute routers get-status router-prod-us-central1 \\
  --region=us-central1 \\
  --format="yaml(result.bgpPeerStatus)"</code></pre>
The peer status for <code>peer-interconnect-01</code> remained in state <code>UP</code> for 58 seconds after the physical fiber was disconnected, actively counting down the 60-second hold timer before transitioning to <code>HOLD_TIMER_EXPIRED</code>.
</li>
<li>Analyzed packet traces on on-premises firewall:
<pre><code># Monitor firewall drops on VPN interface:
tcpdump -nn -i eth1 "tcp[tcpflags] & (tcp-rst|tcp-fin) != 0" -c 100</code></pre>
Firewall logs revealed tens of thousands of <code>DROP_OUT_OF_STATE</code> errors on the VPN interface (<code>eth1</code>). Return packets arriving on the VPN interface matched no established state table entry because the original SYN traversed the Interconnect interface (<code>eth0</code>).
</li>
</ol>
<p><strong>Root cause:</strong> Lack of Bidirectional Forwarding Detection (BFD) forced failure detection to rely on standard 60-second BGP hold timers. Furthermore, asymmetric route priority (GCP Cloud Router advertised equal MED 100 on both paths) prevented symmetric failover, and firewall zones were unclustered.</p>

<p><strong>Defensible remediation:</strong></p>
<ol>
<li>Configured deterministic MED on Cloud Router: Interconnect peer metric 100, Backup VPN peer metric 200:
<pre><code>gcloud compute routers update-bgp-peer router-prod-us-central1 \\
  --peer-name=peer-interconnect-01 \\
  --advertised-route-priority=100 \\
  --region=us-central1

gcloud compute routers update-bgp-peer router-prod-us-central1 \\
  --peer-name=peer-vpn-tunnel-01 \\
  --advertised-route-priority=200 \\
  --region=us-central1</code></pre>
</li>
<li>Enabled BFD on Cloud Router BGP peer with 300ms receive/transmit intervals and multiplier 3:
<pre><code>gcloud compute routers update-bgp-peer router-prod-us-central1 \\
  --peer-name=peer-interconnect-01 \\
  --bfd-min-receive-interval=300 \\
  --bfd-min-transmit-interval=300 \\
  --bfd-multiplier=3 \\
  --region=us-central1</code></pre>
</li>
<li>Configured on-premises firewalls with asymmetric connection state sharing or unified hybrid security zones.</li>
</ol>

<figure class="diagram-figure">
<svg role="img" aria-labelledby="d57-i1-title d57-i1-desc" viewBox="0 0 980 280" width="100%" height="auto" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d57-i1-title">Incident 1: BGP Asymmetric Routing Blackhole vs Deterministic MED and BFD Failover</title>
<desc id="d57-i1-desc">Diagram showing failed path where uncoordinated MED caused asymmetric routing and a 60s hold timer blackout, followed by corrected path with symmetric MED 100/200 and sub-second BFD convergence.</desc>
<defs>
<marker id="d57-i1-mf" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/>
</marker>
<marker id="d57-i1-mc" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
</defs>

<!-- Failed Path Box -->
<rect x="20" y="20" width="940" height="110" rx="6" fill="#1e1b2e" stroke="#f43f5e" stroke-width="1.5"/>
<text x="35" y="45" fill="#f43f5e" font-size="13" font-weight="700">FAILED PATH: Asymmetric Routing &amp; 60s Hold Timer Blackhole (Optic Pulled)</text>

<rect x="40" y="60" width="220" height="50" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="50" y="80" fill="#f1f5f9" font-size="11" font-weight="600">On-Prem Host</text>
<text x="50" y="96" fill="#94a3b8" font-size="10">Outbound: HA VPN (MED 100)</text>

<rect x="330" y="60" width="240" height="50" rx="4" fill="#4c0519" stroke="#f43f5e" stroke-width="1.5"/>
<text x="340" y="80" fill="#fda4af" font-size="11" font-weight="700">Dead Interconnect Path</text>
<text x="340" y="96" fill="#fecdd3" font-size="10">GCP holds route for 60s (No BFD)</text>

<rect x="680" y="60" width="260" height="50" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1"/>
<text x="690" y="80" fill="#f1f5f9" font-size="11" font-weight="600">Stateful On-Prem Firewall</text>
<text x="690" y="96" fill="#f43f5e" font-size="10">DROP_OUT_OF_STATE (Asymmetric)</text>

<path d="M 260 85 L 330 85" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d57-i1-mf)"/>
<path d="M 570 85 L 680 85" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d57-i1-mf)"/>

<!-- Corrected Path Box -->
<rect x="20" y="145" width="940" height="115" rx="6" fill="#0f291e" stroke="#22c55e" stroke-width="1.5"/>
<text x="35" y="170" fill="#4ade80" font-size="13" font-weight="700">CORRECTED PATH: BFD Sub-Second Detection (&lt;900ms) with Deterministic Symmetric MED</text>

<rect x="40" y="185" width="220" height="55" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="50" y="205" fill="#f1f5f9" font-size="11" font-weight="600">On-Prem Host</text>
<text x="50" y="221" fill="#86efac" font-size="10">Outbound: HA VPN (MED 200)</text>

<rect x="330" y="185" width="240" height="55" rx="4" fill="#064e3b" stroke="#34d399" stroke-width="1.5"/>
<text x="340" y="205" fill="#a7f3d0" font-size="11" font-weight="700">Cloud Router BFD</text>
<text x="340" y="221" fill="#cbd5e1" font-size="10">Withdraws route in &lt;900ms</text>

<rect x="680" y="185" width="260" height="55" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="690" y="205" fill="#f1f5f9" font-size="11" font-weight="600">Stateful Core Firewall</text>
<text x="690" y="221" fill="#86efac" font-size="10">Symmetric Flow: Established</text>

<path d="M 260 212 L 330 212" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d57-i1-mc)"/>
<path d="M 570 212 L 680 212" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d57-i1-mc)"/>

<!-- Verify Boundary -->
<rect x="320" y="180" width="260" height="65" rx="6" fill="none" stroke="#f59e0b" stroke-width="1" stroke-dasharray="4,4"/>
<text x="325" y="172" fill="#fbbf24" font-size="10" font-weight="600">VERIFY BOUNDARY: BFD 300ms x 3 Multiplier</text>
</svg>
<figcaption>Figure 57.2: Incident 1 Root Cause and Remediation. <strong>Supplied facts:</strong> BGP hold timer (60s) delayed route withdrawal during primary link bounce, while asymmetric MED caused on-prem stateful firewalls to drop return packets. <strong>Architectural inference:</strong> BFD enables sub-second link failure detection (900ms), while aligning advertised route priority ensures deterministic symmetric routing across hybrid links. <strong>Expected post-fix behavior:</strong> BFD detects transport failure in 880ms; Cloud Router immediately withdraws Interconnect routes; traffic shifts symmetrically to HA VPN with zero connection drops.</figcaption>
</figure>

<p><strong>Verification:</strong> Simulated an optic failure on the primary circuit; BFD detected packet loss in 880ms; Cloud Router withdrew the Interconnect route in 910ms; traffic shifted to HA VPN with 0 dropped TCP connections and symmetric firewall session traversal.</p>

<p><strong>Alternative and residual risk:</strong> Ensure on-premises edge router hardware supports BFD hardware offload; verify that backup HA VPN capacity (3 Gbps) can handle peak failover bursts without throttling.</p>
</article>

<article id="topic-02-problem" class="topic-card">
<h3>On-Premises Private Google Access DNS and VIP Routing Breakdown · field case</h3>
<p><strong>Situation and impact:</strong> Brightloaf deployed an on-premises night-batch analytics worker cluster in Chicago to extract 45 TB of historical customer financial ledgers and stream them into BigQuery and Cloud Storage for regulatory audit archiving. Security architecture mandated that no customer data may transit the public internet and enclosed the GCP environment within a strict VPC Service Controls (VPC-SC) perimeter. When the midnight batch jobs executed, 100% of workers failed with <code>google.api_core.exceptions.GoogleAPICallError: 403 Request is prohibited by organization's policy (VPC Service Controls violation)</code> and <code>Connection timed out</code> errors. The automated audit reporting missed the mandatory 06:00 UTC market reconciliation window, prompting a formal regulatory investigation and an automatic $250,000 late-filing statutory fine.</p>

<p><strong>Constraints:</strong> Must reach Cloud Storage and BigQuery strictly across private Cloud Interconnect; must strictly enforce VPC-SC perimeter policy with zero internet egress; must support enterprise-wide DNS resolution without breaking public Google SaaS services (e.g., Google Workspace).</p>

<p><strong>Diagnostic sequence and root cause:</strong></p>
<ol>
<li>Executed DNS resolution test from on-premises analytics host:
<pre><code># Test DNS resolution for Google API:
getent hosts storage.googleapis.com</code></pre>
Returned public IP addresses: <code>142.250.190.112</code> and <code>142.250.190.48</code>.
</li>
<li>Inspected routing path on on-premises border router:
<pre><code># Check kernel routing table for public IP:
netstat -rn | grep 142.250</code></pre>
No specific route existed for <code>142.250.190.112</code>; the kernel routed packets out the default gateway <code>0.0.0.0/0</code> via the corporate public ISP link.
</li>
<li>Inspected Cloud Router advertised routes:
<pre><code>gcloud compute routers get-status router-prod-us-central1 \\
  --region=us-central1 \\
  --format="yaml(result.bestRoutesForRouter)"</code></pre>
Cloud Router was operating in <code>DEFAULT</code> advertisement mode, announcing only internal VPC subnets (<code>10.10.0.0/16</code>). The restricted VIP <code>199.36.153.4/30</code> was never advertised.
</li>
</ol>
<p><strong>Root cause:</strong> On-premises DNS lacked conditional forwarding / RPZ rules for <code>*.googleapis.com</code>, resolving queries to public Google VIPs. Furthermore, Cloud Router did not advertise <code>199.36.153.4/30</code> via custom route advertisements. Consequently, traffic routed out the public internet gateway, where Google's edge recognized the request as external to the VPC-SC perimeter and rejected it with HTTP 403.</p>

<p><strong>Defensible remediation:</strong></p>
<ol>
<li>Configured Cloud Router to advertise <code>199.36.153.4/30</code> as a custom IP range over Dedicated Interconnect:
<pre><code>gcloud compute routers update router-prod-us-central1 \\
  --advertisement-mode=CUSTOM \\
  --set-advertisement-ranges=10.10.0.0/16,199.36.153.4/30 \\
  --region=us-central1</code></pre>
</li>
<li>Configured on-premises DNS server with a response policy zone for <code>googleapis.com</code>:
<pre><code># BIND RPZ Zone definition:
# CNAME *.googleapis.com -> restricted.googleapis.com
# A restricted.googleapis.com -> 199.36.153.4, 199.36.153.5, 199.36.153.6, 199.36.153.7</code></pre>
</li>
<li>Updated on-premises perimeter egress firewall to permit TCP port 443 to <code>199.36.153.4/30</code>.</li>
</ol>

<figure class="diagram-figure">
<svg role="img" aria-labelledby="d57-i2-title d57-i2-desc" viewBox="0 0 980 280" width="100%" height="auto" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d57-i2-title">Incident 2: PGA Public DNS Resolution Drop vs Custom Route Ingestion and VPC-SC Compliance</title>
<desc id="d57-i2-desc">Diagram showing failed path where on-prem client resolved public IPs and routed to internet NAT triggering VPC-SC access denial, followed by corrected path with DNS CNAME override and Cloud Router custom advertisement of 199.36.153.4/30.</desc>
<defs>
<marker id="d57-i2-mf" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/>
</marker>
<marker id="d57-i2-mc" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
</defs>

<!-- Failed Path Box -->
<rect x="20" y="20" width="940" height="110" rx="6" fill="#1e1b2e" stroke="#f43f5e" stroke-width="1.5"/>
<text x="35" y="45" fill="#f43f5e" font-size="13" font-weight="700">FAILED PATH: Public DNS Resolution Leaks to Internet Gateway (VPC-SC Perimeter Rejection)</text>

<rect x="40" y="60" width="220" height="50" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="50" y="80" fill="#f1f5f9" font-size="11" font-weight="600">On-Prem Analytics Host</text>
<text x="50" y="96" fill="#94a3b8" font-size="10">Resolves public IP (142.250.x.x)</text>

<rect x="330" y="60" width="240" height="50" rx="4" fill="#4c0519" stroke="#f43f5e" stroke-width="1.5"/>
<text x="340" y="80" fill="#fda4af" font-size="11" font-weight="700">Corporate Internet Gateway</text>
<text x="340" y="96" fill="#fecdd3" font-size="10">Routes out Default ISP 0.0.0.0/0</text>

<rect x="680" y="60" width="260" height="50" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1"/>
<text x="690" y="80" fill="#f1f5f9" font-size="11" font-weight="600">Google API Front-End</text>
<text x="690" y="96" fill="#f43f5e" font-size="10">HTTP 403 VPC-SC Perimeter Block</text>

<path d="M 260 85 L 330 85" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d57-i2-mf)"/>
<path d="M 570 85 L 680 85" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d57-i2-mf)"/>

<!-- Corrected Path Box -->
<rect x="20" y="145" width="940" height="115" rx="6" fill="#0f291e" stroke="#22c55e" stroke-width="1.5"/>
<text x="35" y="170" fill="#4ade80" font-size="13" font-weight="700">CORRECTED PATH: DNS RPZ CNAME Override to 199.36.153.4/30 &amp; Cloud Interconnect Transit</text>

<rect x="40" y="185" width="220" height="55" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="50" y="205" fill="#f1f5f9" font-size="11" font-weight="600">On-Prem Analytics Host</text>
<text x="50" y="221" fill="#86efac" font-size="10">Resolves restricted VIP 199.36.153.4</text>

<rect x="330" y="185" width="240" height="55" rx="4" fill="#064e3b" stroke="#34d399" stroke-width="1.5"/>
<text x="340" y="205" fill="#a7f3d0" font-size="11" font-weight="700">Dedicated Interconnect</text>
<text x="340" y="221" fill="#cbd5e1" font-size="10">Cloud Router advertises /30</text>

<rect x="680" y="185" width="260" height="55" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="690" y="205" fill="#f1f5f9" font-size="11" font-weight="600">VPC-SC Perimeter</text>
<text x="690" y="221" fill="#86efac" font-size="10">HTTP 200 OK (Wire-Speed GCS)</text>

<path d="M 260 212 L 330 212" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d57-i2-mc)"/>
<path d="M 570 212 L 680 212" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d57-i2-mc)"/>

<!-- Verify Boundary -->
<rect x="320" y="180" width="260" height="65" rx="6" fill="none" stroke="#f59e0b" stroke-width="1" stroke-dasharray="4,4"/>
<text x="325" y="172" fill="#fbbf24" font-size="10" font-weight="600">VERIFY BOUNDARY: Custom /30 BGP Route Ingested</text>
</svg>
<figcaption>Figure 57.3: Incident 2 Root Cause and Remediation. <strong>Supplied facts:</strong> Analytics servers resolved public Google IPs and routed over public internet gateways, failing VPC Service Controls perimeter checks. <strong>Architectural inference:</strong> On-prem DNS conditional forwarding rewrites requests to restricted VIP <code>199.36.153.4/30</code>, which Cloud Router dynamically advertises over Interconnect. <strong>Expected post-fix behavior:</strong> Google API calls route entirely over private optical circuits directly to VPC-SC protected BigQuery and Cloud Storage buckets at 9.8 Gbps.</figcaption>
</figure>

<p><strong>Verification:</strong> Performed DNS query on analytics host; resolved to <code>199.36.153.4</code>. Traceroute confirmed path traversed Dedicated Interconnect into Google Cloud edge. Uploaded a 5 GB test parquet object to Cloud Storage inside the VPC-SC perimeter; succeeded with HTTP 200 in 4.2 seconds at 9.8 Gbps line rate.</p>

<p><strong>Alternative and residual risk:</strong> Services that are NOT supported by VPC Service Controls cannot be accessed via <code>restricted.googleapis.com</code>; if non-VPC-SC APIs are required, they must use <code>private.googleapis.com</code> (<code>199.36.153.8/30</code>) or Private Service Connect endpoints.</p>
</article>

<article id="topic-03-problem" class="topic-card">
<h3>Hybrid Bandwidth Collapse, MTU Clamping Blackhole, and NAT Port Pressure · field case</h3>
<p><strong>Situation and impact:</strong> Brightloaf initiated an automated database synchronization migrating 40 TB of on-premises VMware databases to Google Cloud SQL and Cloud Storage. To save initial setup costs, engineering routed the replication over a 3 Gbps Cloud HA VPN tunnel. During the first evening sync, database replication collapsed to under 12 Mbps with 68% packet loss. Hundreds of replication threads hung indefinitely immediately following the TLS handshake (SYN packets succeeded, but subsequent 16 KB database payload packets disappeared). Concurrently, secondary payment microservices sharing the hybrid gateway began failing with <code>504 Gateway Timeout</code> and <code>EADDRNOTAVAIL: Cannot assign requested address</code>. The 40 TB replication stalled for 14 hours, while the cloud billing dashboard reported an unexpected $84,000 monthly internet egress spike.</p>

<p><strong>Constraints:</strong> Must achieve line-rate transfer throughput capable of finishing 40 TB nightly transfers in &lt;10 hours; must eliminate MTU packet blackholing across hybrid boundaries; must resolve Cloud NAT port exhaustion without dropping microservice traffic.</p>

<p><strong>Diagnostic sequence and root cause:</strong></p>
<ol>
<li>Performed Path MTU Discovery test across the hybrid tunnel using ping with Don't Fragment (DF) flag:
<pre><code># Test 1500-byte MTU (1472 payload + 28 header):
ping -c 3 -M do -s 1472 10.10.10.5

# Test 1440-byte MTU (1412 payload + 28 header):
ping -c 3 -M do -s 1412 10.10.10.5</code></pre>
Result: The 1472-byte payload failed with 100% loss, while the 1412-byte payload succeeded. Packets larger than 1440 bytes were being discarded by the IPsec gateway, and the enterprise firewall was blocking incoming ICMP Type 3 Code 4 messages, causing a silent MTU blackhole.
</li>
<li>Checked Cloud NAT metrics in Cloud Monitoring:
<code>dropped_sent_packets_count</code> spiked to 42,000 packets/sec with reason <code>OUT_OF_RESOURCES</code>. Cloud NAT's static allocation of 64 ports per VM was overwhelmed by thousands of concurrent database synchronization threads.
</li>
<li>Analyzed cost economics: 40 TB/day sustained over Cloud VPN incurred standard internet egress fees ($0.085/GB * 40,000 GB = $3,400/day = $102,000/month egress), whereas a 10G Dedicated Interconnect ($1,750/mo port fee + $0.02/GB egress = $2,550/mo total) would save over $99,000/month.
</li>
</ol>
<p><strong>Root cause:</strong> Missing TCP MSS clamping caused large database payload packets (>1440 bytes) to be silently dropped by the VPN gateway. Furthermore, Cloud NAT 64-port default allocation exhausted ephemeral source ports, and Cloud VPN was misapplied to a bulk data migration workload that economically and architecturally required Dedicated Interconnect.</p>

<p><strong>Defensible remediation:</strong></p>
<ol>
<li>Configured TCP MSS clamping to 1360 bytes on the on-premises VPN interface:
<pre><code># Configure MSS Clamping on border router:
# Cisco IOS / Quagga configuration:
interface Tunnel1
 ip tcp adjust-mss 1360</code></pre>
</li>
<li>Updated Cloud NAT to enable dynamic port allocation with a minimum of 1024 ports per VM:
<pre><code>gcloud compute routers nats update nat-gw-prod \\
  --router=router-prod-us-central1 \\
  --region=us-central1 \\
  --min-ports-per-vm=1024 \\
  --enable-dynamic-port-allocation</code></pre>
</li>
<li>Provisioned 10G Dedicated Interconnect to replace VPN for primary data replication, natively supporting 1500-byte MTU and slashing data egress rates to $0.02/GB.</li>
</ol>

<figure class="diagram-figure">
<svg role="img" aria-labelledby="d57-i3-title d57-i3-desc" viewBox="0 0 980 280" width="100%" height="auto" style="background:#121526;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="d57-i3-title">Incident 3: VPN MTU Blackhole and NAT Port Exhaustion vs Interconnect 10G and Dynamic Port Sizing</title>
<desc id="d57-i3-desc">Diagram showing failed path where 1500-byte packets dropped silently in 1440-byte VPN tunnel and Cloud NAT 64-port exhaustion dropped connections, followed by corrected path with TCP MSS clamping, 10G Dedicated Interconnect, and dynamic NAT port allocation.</desc>
<defs>
<marker id="d57-i3-mf" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/>
</marker>
<marker id="d57-i3-mc" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
<polygon points="0 0, 8 4, 0 8" fill="#22c55e"/>
</marker>
</defs>

<!-- Failed Path Box -->
<rect x="20" y="20" width="940" height="110" rx="6" fill="#1e1b2e" stroke="#f43f5e" stroke-width="1.5"/>
<text x="35" y="45" fill="#f43f5e" font-size="13" font-weight="700">FAILED PATH: 1500B MTU Tunnel Blackhole &amp; Cloud NAT Port Exhaustion (64 Ports/VM)</text>

<rect x="40" y="60" width="220" height="50" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
<text x="50" y="80" fill="#f1f5f9" font-size="11" font-weight="600">Replication Host (1500B)</text>
<text x="50" y="96" fill="#94a3b8" font-size="10">TCP SYN OK, Data Dropped</text>

<rect x="330" y="60" width="240" height="50" rx="4" fill="#4c0519" stroke="#f43f5e" stroke-width="1.5"/>
<text x="340" y="80" fill="#fda4af" font-size="11" font-weight="700">1440B VPN Tunnel</text>
<text x="340" y="96" fill="#fecdd3" font-size="10">PMTUD Blackhole (ICMP Filtered)</text>

<rect x="680" y="60" width="260" height="50" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1"/>
<text x="690" y="80" fill="#f1f5f9" font-size="11" font-weight="600">Cloud NAT Gateway</text>
<text x="690" y="96" fill="#f43f5e" font-size="10">OUT_OF_RESOURCES (64 Ports)</text>

<path d="M 260 85 L 330 85" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d57-i3-mf)"/>
<path d="M 570 85 L 680 85" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#d57-i3-mf)"/>

<!-- Corrected Path Box -->
<rect x="20" y="145" width="940" height="115" rx="6" fill="#0f291e" stroke="#22c55e" stroke-width="1.5"/>
<text x="35" y="170" fill="#4ade80" font-size="13" font-weight="700">CORRECTED PATH: Dedicated Interconnect 10G (1500B MTU) &amp; Dynamic NAT Port Sizing (1024 Ports)</text>

<rect x="40" y="185" width="220" height="55" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="50" y="205" fill="#f1f5f9" font-size="11" font-weight="600">Replication Host</text>
<text x="50" y="221" fill="#86efac" font-size="10">MSS Clamped / 1500B Wire</text>

<rect x="330" y="185" width="240" height="55" rx="4" fill="#064e3b" stroke="#34d399" stroke-width="1.5"/>
<text x="340" y="205" fill="#a7f3d0" font-size="11" font-weight="700">10G Dedicated Interconnect</text>
<text x="340" y="221" fill="#cbd5e1" font-size="10">9.4 Gbps Sustained Throughput</text>

<rect x="680" y="185" width="260" height="55" rx="4" fill="#0f172a" stroke="#22c55e" stroke-width="1.5"/>
<text x="690" y="205" fill="#f1f5f9" font-size="11" font-weight="600">Cloud NAT Gateway</text>
<text x="690" y="221" fill="#86efac" font-size="10">Dynamic 1024-4096 Ports/VM</text>

<path d="M 260 212 L 330 212" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d57-i3-mc)"/>
<path d="M 570 212 L 680 212" fill="none" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d57-i3-mc)"/>

<!-- Verify Boundary -->
<rect x="320" y="180" width="260" height="65" rx="6" fill="none" stroke="#f59e0b" stroke-width="1" stroke-dasharray="4,4"/>
<text x="325" y="172" fill="#fbbf24" font-size="10" font-weight="600">VERIFY BOUNDARY: 1500B Wire MTU &amp; Port Reservation</text>
</svg>
<figcaption>Figure 57.4: Incident 3 Root Cause and Remediation. <strong>Supplied facts:</strong> IPsec 1440-byte MTU caused Path MTU blackholes on bulk replication payloads, while Cloud NAT 64-port allocation dropped concurrent connections. <strong>Architectural inference:</strong> Enforcing TCP MSS clamping (1360 bytes) eliminates PMTUD hangs, while migrating bulk data to 10G Dedicated Interconnect provides 1500-byte MTU and slashes egress costs. <strong>Expected post-fix behavior:</strong> Replication throughput increases from 12 Mbps to 9.4 Gbps; 40 TB sync finishes in 9.8 hours; Cloud NAT zero drops with 1024 ports per VM.</figcaption>
</figure>

<p><strong>Verification:</strong> Ran MTU discovery up to 1440 bytes on VPN and verified MSS clamping negotiated 1360 bytes on all TCP handshakes; 0 dropped packets. After Dedicated Interconnect cutover, transfer throughput reached 9.4 Gbps sustained; 40 TB backup completed in 9.8 hours; egress billing dropped by 74%.</p>

<p><strong>Alternative and residual risk:</strong> Ensure on-premises core switching supports jumbo frames (8896 bytes) end-to-end if jumbo MTU is enabled on Interconnect; otherwise maintain 1500-byte MTU on VLAN attachments.</p>
</article>
</section>
"""
print("Part 3 defined, length:", len(part3_html))
