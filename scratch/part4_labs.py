part4_html = """
<section id="part-4" class="part">
<h2>4 · Step-by-step labs for each topic</h2>

<article id="topic-01-lab" class="topic-card lab">
<h3>Exercise 1: Cloud Router eBGP Peering, MED Metric Path Steering, and Custom Route Advertisement</h3>
<p><strong>Goal:</strong> Deploy a Cloud Router, establish dynamic eBGP peering sessions with deterministic MED route priority across redundant hybrid interfaces, configure custom BGP route advertisements, and inspect routing table convergence.</p>
<p><strong>Mode:</strong> production practice · <strong>Prerequisite:</strong> Day 56 and Day 51 exit artifacts.</p>
<ol>
<li><strong>Create Cloud Router with Custom ASN and Global Dynamic Routing:</strong>
<pre><code>gcloud compute routers create router-hybrid-prod \\
  --network=vpc-hybrid-prod \\
  --region=us-central1 \\
  --asn=16550</code></pre>
</li>
<li><strong>Create HA VPN Gateway and Redundant Interfaces:</strong>
<pre><code>gcloud compute vpn-gateways create vpn-gw-us-central1 \\
  --network=vpc-hybrid-prod \\
  --region=us-central1</code></pre>
</li>
<li><strong>Add Cloud Router Interfaces and Configure Deterministic BGP MED Priorities:</strong>
<pre><code># Configure primary interface and BGP peer (MED 100):
gcloud compute routers add-interface router-hybrid-prod \\
  --interface-name=if-primary-interconnect \\
  --interconnect-attachment=vlan-ashburn-01 \\
  --region=us-central1

gcloud compute routers add-bgp-peer router-hybrid-prod \\
  --peer-name=peer-interconnect-primary \\
  --interface=if-primary-interconnect \\
  --peer-ip-address=169.254.10.2 \\
  --peer-asn=65001 \\
  --advertised-route-priority=100 \\
  --bfd-min-receive-interval=300 \\
  --bfd-min-transmit-interval=300 \\
  --bfd-multiplier=3 \\
  --region=us-central1

# Configure backup interface and BGP peer (MED 200):
gcloud compute routers add-interface router-hybrid-prod \\
  --interface-name=if-backup-vpn \\
  --vpn-tunnel=tunnel-backup-01 \\
  --region=us-central1

gcloud compute routers add-bgp-peer router-hybrid-prod \\
  --peer-name=peer-vpn-backup \\
  --interface=if-backup-vpn \\
  --peer-ip-address=169.254.20.2 \\
  --peer-asn=65001 \\
  --advertised-route-priority=200 \\
  --region=us-central1</code></pre>
</li>
<li><strong>Configure Custom Route Advertisements for VPC Summary Subnets and PGA VIP:</strong>
<pre><code>gcloud compute routers update router-hybrid-prod \\
  --region=us-central1 \\
  --advertisement-mode=CUSTOM \\
  --set-advertisement-ranges=10.10.0.0/16,199.36.153.4/30</code></pre>
</li>
<li><strong>Inspect Learned BGP Prefixes and Route Health:</strong>
<pre><code>gcloud compute routers get-status router-hybrid-prod \\
  --region=us-central1 \\
  --format="yaml(result.bgpPeerStatus,result.bestRoutesForRouter)"</code></pre>
</li>
</ol>
<div class="callout success">
<strong>Expected result / acceptance</strong>
<p>Cloud Router establishes eBGP peering with ASN 65001. Outbound traffic prefers Dedicated Interconnect (MED 100) and automatically fails over to HA VPN (MED 200) in under 900ms upon BFD trip, while <code>199.36.153.4/30</code> is actively advertised to on-premises routers.</p>
</div>
<div class="callout caution">
<strong>Troubleshooting</strong>
<p>If on-premises firewalls drop return packets, inspect BGP route priority on the customer border router to ensure outbound traffic uses matching MED priorities (100 on Interconnect, 200 on VPN) to prevent asymmetric routing.</p>
</div>
<div class="callout">
<strong>Cleanup and cost</strong>
<p>Remove BGP peers, router interfaces, and Cloud Router instances if created for sandbox testing to avoid ongoing resource allocation charges.</p>
</div>
<label class="check"><input type="checkbox" data-progress="lab-57-topic-01"> I completed and checked this topic exercise</label>
</article>

<article id="topic-02-lab" class="topic-card lab">
<h3>Exercise 2: Private Google Access for On-Premises: DNS Resolution and VIP Route Ingestion</h3>
<p><strong>Goal:</strong> Implement DNS conditional forwarding and response policy overrides for Private Google Access, verify route ingestion of the <code>199.36.153.4/30</code> VIP, and validate TLS connectivity to Cloud Storage within a VPC Service Controls perimeter.</p>
<p><strong>Mode:</strong> production practice · <strong>Prerequisite:</strong> Day 56 and Day 51 exit artifacts.</p>
<ol>
<li><strong>Configure Cloud DNS Inbound Server Policy:</strong>
<pre><code>gcloud compute dns policies create pga-inbound-policy \\
  --networks=vpc-hybrid-prod \\
  --enable-inbound-forwarding</code></pre>
</li>
<li><strong>Create Private Managed DNS Zone Overriding googleapis.com:</strong>
<pre><code>gcloud dns managed-zones create pga-restricted-zone \\
  --dns-name="googleapis.com." \\
  --description="Private Google Access restricted VIP override" \\
  --visibility=private \\
  --networks=vpc-hybrid-prod</code></pre>
</li>
<li><strong>Add CNAME Wildcard and Restricted VIP A Records:</strong>
<pre><code>gcloud dns record-sets create "*.googleapis.com." \\
  --zone=pga-restricted-zone \\
  --type=CNAME \\
  --ttl=300 \\
  --rrdatas="restricted.googleapis.com."

gcloud dns record-sets create "restricted.googleapis.com." \\
  --zone=pga-restricted-zone \\
  --type=A \\
  --ttl=300 \\
  --rrdatas="199.36.153.4,199.36.153.5,199.36.153.6,199.36.153.7"</code></pre>
</li>
<li><strong>Query Inbound DNS Forwarder from On-Premises Client:</strong>
<pre><code># Query Cloud DNS Inbound Resolver IP (e.g., 10.10.0.25):
dig +short storage.googleapis.com @10.10.0.25</code></pre>
</li>
<li><strong>Test Private API Connectivity and Egress Firewall Rules:</strong>
<pre><code># Test TLS Handshake to restricted VIP:
curl -ivs https://storage.googleapis.com/generate_204 \\
  --resolve storage.googleapis.com:443:199.36.153.4</code></pre>
</li>
<li><strong>Configure VPC Firewall Egress Allowance:</strong>
<pre><code>gcloud compute firewall-rules create allow-pga-egress \\
  --network=vpc-hybrid-prod \\
  --direction=EGRESS \\
  --action=ALLOW \\
  --rules=tcp:443 \\
  --destination-ranges=199.36.153.4/30</code></pre>
</li>
</ol>
<div class="callout success">
<strong>Expected result / acceptance</strong>
<p>DNS queries for <code>storage.googleapis.com</code> resolve to <code>199.36.153.4</code>. HTTPS curl requests succeed with HTTP 204 No Content across private hybrid transport into the VPC-SC protected perimeter.</p>
</div>
<div class="callout caution">
<strong>Troubleshooting</strong>
<p>If curl fails with HTTP 403 VPC Service Controls violation, ensure the client IP address (<code>172.16.10.50</code>) is registered as an authorized corporate IP range in the Access Context Manager access level.</p>
</div>
<div class="callout">
<strong>Cleanup and cost</strong>
<p>Deprovision DNS record sets, managed private zones, and inbound server policies to prevent recurring DNS query billing.</p>
</div>
<label class="check"><input type="checkbox" data-progress="lab-57-topic-02"> I completed and checked this topic exercise</label>
</article>

<article id="topic-03-lab" class="topic-card lab">
<h3>Exercise 3: VPN vs Interconnect Performance, MTU Diagnostics, and Cloud NAT Sizing</h3>
<p><strong>Goal:</strong> Perform Path MTU Discovery across hybrid tunnels, implement TCP MSS clamping to prevent packet blackholes, configure Cloud NAT dynamic port allocation, and evaluate cost-crossover economics.</p>
<p><strong>Mode:</strong> production practice · <strong>Prerequisite:</strong> Day 56 and Day 51 exit artifacts.</p>
<ol>
<li><strong>Execute Path MTU Discovery (PMTUD) Across Hybrid Tunnel:</strong>
<pre><code># Test 1500-byte MTU (1472 payload + 28 header):
ping -c 3 -M do -s 1472 10.10.10.5

# Test 1440-byte MTU (1412 payload + 28 header):
ping -c 3 -M do -s 1412 10.10.10.5</code></pre>
</li>
<li><strong>Apply TCP MSS Clamping on Hybrid Border Interface:</strong>
<pre><code># Enforce MSS clamping on Linux router / gateway:
sudo iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu</code></pre>
</li>
<li><strong>Configure Cloud NAT Dynamic Port Allocation to Prevent Resource Exhaustion:</strong>
<pre><code>gcloud compute routers nats create nat-gw-prod \\
  --router=router-hybrid-prod \\
  --region=us-central1 \\
  --auto-allocate-nat-ips \\
  --min-ports-per-vm=1024 \\
  --max-ports-per-vm=4096 \\
  --enable-dynamic-port-allocation</code></pre>
</li>
<li><strong>Calculate Economic Crossover Point Between VPN and Dedicated Interconnect:</strong>
<pre><code># Economic Crossover Model:
# Fixed Dedicated Interconnect Cost: $1,750 (10G Port) + $43.80 (VLAN) = $1,793.80/month
# Fixed Cloud HA VPN Cost: $0.10/hour (Dual Tunnels) = $73.00/month
# Internet Egress Rate: $0.085/GB
# Interconnect Egress Rate: $0.020/GB
# Monthly Crossover (GB) = (1793.80 - 73.00) / (0.085 - 0.020) = 1720.80 / 0.065 = 26,473.8 GB (~26.5 TB)</code></pre>
</li>
</ol>
<div class="callout success">
<strong>Expected result / acceptance</strong>
<p>Ping packets with 1412-byte payload succeed without fragmentation. TCP connections negotiate 1360-byte MSS. Cloud NAT dynamically scales ports up to 4096 without <code>OUT_OF_RESOURCES</code> drops.</p>
</div>
<div class="callout caution">
<strong>Troubleshooting</strong>
<p>If large file transfers hang after initial TLS handshake, verify that intermediate firewalls permit ICMP Type 3 Code 4 packets, or verify that TCP MSS clamping is active on the border interface.</p>
</div>
<div class="callout">
<strong>Cleanup and cost</strong>
<p>Delete Cloud NAT gateways and firewall rules when testing concludes to avoid recurring NAT gateway and static IP reservation costs.</p>
</div>
<label class="check"><input type="checkbox" data-progress="lab-57-topic-03"> I completed and checked this topic exercise</label>
</article>
</section>
"""
print("Part 4 defined, length:", len(part4_html))
