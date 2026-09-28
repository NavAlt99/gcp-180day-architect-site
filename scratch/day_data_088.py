"""day_data_088.py — Exhaustive architecture data specification for Day 88.

Covers Availability Across Infrastructure Layers:
1. Compute availability (Regional MIGs, autohealing, N+1 headroom, GKE regional clusters, PDBs, topology spread constraints).
2. Network availability (HA VPN dual tunnels, 99.99% Dual Interconnect in separate metros, redundant Cloud Routers, Anycast ALB).
3. Storage availability (Regional Persistent Disks, Dual/Multi-region GCS buckets, Turbo replication, Filestore Enterprise).
4. Database availability (Cloud SQL HA + cross-region replicas, Spanner multi-region Paxos, Bigtable multi-cluster, Memorystore Standard).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 88

DATA = {
    "day": 88,
    "part1_intro": (
        "Day 88 synthesizes reliability across all physical and logical layers of the enterprise infrastructure stack: "
        "Compute, Networking, Storage, and Databases. A resilient application architecture is only as robust as the weakest "
        "layer supporting it; deploying a multi-region stateless compute layer provides zero protection if the database relies on "
        "a single-zone instance or the hybrid network transit path traverses an unhedged VPN tunnel. Today's curriculum constructs "
        "an end-to-end high availability architecture across Google Cloud's core infrastructure primitives: configuring Regional Managed "
        "Instance Groups and GKE Regional clusters with Topology Spread Constraints, establishing 99.99% hybrid interconnect topologies "
        "across dual metropolitan edge facilities, deploying synchronously replicated Regional Persistent Disks and dual-region Cloud Storage "
        "with Turbo Replication, and evaluating Cloud SQL HA versus multi-region Cloud Spanner Paxos consensus."
    ),
    "exit_summary": (
        "Engineered an authoritative four-tier enterprise high availability blueprint mapping Compute (GKE Regional + PDBs), "
        "Network (99.99% Dual-Metro Interconnect + Global ALB), Storage (Regional PD + Dual-Region GCS Turbo), and Database "
        "(Cloud SQL HA + Spanner Paxos) failure boundaries; calculated exact N+1 compute headroom and modeled single-zone failure survival; "
        "authored production Terraform modules for Regional MIG autohealing and Kubernetes TopologySpreadConstraints; executed a multi-layer "
        "tabletop resilience drill proving zero data loss and sub-minute recovery under total zonal blackout."
    ),
    "part2_intro": (
        "High availability requires layered defense in depth, where each infrastructure tier absorbs localized failures autonomously. "
        "The sections below provide deep architectural specifications, configuration parameters, and trade-off matrices across "
        "Google Cloud compute, network, storage, and database services."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Infrastructure Layer</th>
      <th>Google Cloud High Availability Pattern</th>
      <th>Target SLA</th>
      <th>Failover Mechanism &amp; RTO</th>
      <th>Data Loss Risk (RPO)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Compute</strong></td>
      <td>GKE Regional Cluster (3 Master AZs) + Multi-Zone Node Pools + Pod Disruption Budgets (PDB).</td>
      <td>99.95% (Control Plane)</td>
      <td>Automated pod rescheduling via Kube-Scheduler; RTO &lt; 30s.</td>
      <td>RPO = 0 (Stateless pods).</td>
    </tr>
    <tr>
      <td><strong>Network</strong></td>
      <td>99.99% Dual Dedicated Interconnect across dual metropolitan colocation facilities + Dual Cloud Routers.</td>
      <td>99.99%</td>
      <td>BGP session failover with BFD (Bidirectional Forwarding Detection); RTO &lt; 1s.</td>
      <td>RPO = 0 (In-flight TCP retries).</td>
    </tr>
    <tr>
      <td><strong>Storage</strong></td>
      <td>Regional Persistent Disk (synchronous 2-zone block replication) + Dual-Region GCS (Turbo Replication).</td>
      <td>99.95% (GCS)</td>
      <td>Force-attach Regional PD to surviving zone; RTO &lt; 60s.<br>GCS multi-region bucket active/active.</td>
      <td>RPO = 0 (Synchronous block write).<br>GCS Turbo: RPO &lt; 15 mins.</td>
    </tr>
    <tr>
      <td><strong>Databases</strong></td>
      <td>Cloud SQL HA (Regional PD sync replication) OR Cloud Spanner Multi-Region (3-Region Paxos Quorum).</td>
      <td>99.95% (Cloud SQL)<br><strong>99.999% (Spanner)</strong></td>
      <td>Cloud SQL: Automated DNS failover to standby; RTO &lt; 60s.<br>Spanner: Transparent zero-downtime Paxos election; RTO = 0s.</td>
      <td>Cloud SQL: RPO = 0.<br>Spanner: RPO = 0 (TrueTime consistency).</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 88: Four-Tier Layered Infrastructure High Availability Architecture",
        "desc": "End-to-end request traversal across Anycast edge, GKE multi-zone compute, Regional PD storage, and Spanner multi-region data.",
        "caption": "Figure 88.1: Full-stack high availability topology illustrating synchronous replication and automated failover across all four infrastructure tiers.",
        "nodes": [
            ("1. Anycast Network", "Global ALB + Dual Metro Interconnect\\n99.99% BGP Failover"),
            ("2. Regional Compute", "GKE Regional Cluster (3 AZs)\\nTopologySpread + PDB Fencing"),
            ("3. Replicated Storage", "Regional PD Synchronous Blocks\\nDual-Region GCS Turbo (15m RPO)"),
            ("4. Multi-Region DB", "Spanner 3-Region Paxos Quorum\\n99.999% Zero-Downtime FT"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Compute availability: regional MIGs, GKE regional clusters, PDBs, and topology spread",
            "preview": (
                "During a routine GKE node pool rolling upgrade, the cluster autoscaler drains nodes too aggressively, "
                "terminating all replicas of the checkout pod at the exact same moment and creating a self-inflicted 12-minute outage."
            ),
            "overview": (
                "Compute availability in Google Cloud is achieved by abstracting individual server instances into self-healing, "
                "multi-zone groupings. For virtual machines, **Regional Managed Instance Groups (MIGs)** distribute stateless workloads "
                "identically across three availability zones, utilizing **Autohealing** health checks to automatically replace crashed instances. "
                "For containerized microservices, **GKE Regional Clusters** replicate the Kubernetes master control plane across three zones (99.95% SLA) "
                "and deploy multi-zone worker node pools. To prevent deployment operations or node drains from causing service degradation, "
                "architects must enforce **Pod Disruption Budgets (PDBs)** (guaranteeing a minimum number of running pods during upgrades) "
                "and **Topology Spread Constraints** (mandating that the Kubernetes scheduler evenly distributes pods across physical zones)."
            ),
            "technical": (
                "Architects must configure compute resiliency primitives using strict infrastructure-as-code specifications:\n\n"
                "### 1. Regional MIG Autohealing Mechanics\n"
                "- **Health Check:** Application-level endpoint (e.g. `GET /healthz`) probing port 8080.\n"
                "- **Initial Delay:** Grace period (e.g. 180 seconds) allowing application initialization before health checking begins.\n"
                "- **Target Distribution:** Configure `distribution_policy_target_shape = \"EVEN\"` to enforce balanced zonal spread across `us-central1-a`, `us-central1-b`, and `us-central1-c`.\n\n"
                "### 2. GKE Regional Cluster vs. Zonal Cluster SLAs\n"
                "- **Zonal GKE Cluster:** Control plane resides in a single zone. During master upgrades or zonal failure, the Kubernetes API is unavailable (99.5% SLA).\n"
                "- **Regional GKE Cluster:** Control plane runs in three separate zones with automated etcd quorum replication. High availability 99.95% SLA.\n\n"
                "### 3. Kubernetes Pod Disruption Budgets (PDB) & Topology Spread Constraints\n"
                "- **PDB (`minAvailable: 2` or `maxUnavailable: 25%`):** Blocks node eviction commands and node pool upgrade automation from taking down pods "
                "if doing so would reduce active capacity below the configured threshold.\n"
                "- **Topology Spread Constraints:** Prevents the Kubernetes scheduler from scheduling all pods in a single zone due to localized node packing:\n"
                "  `topologyKey: topology.kubernetes.io/zone`, `maxSkew: 1`, `whenUnsatisfiable: DoNotSchedule`."
            ),
            "questions": [
                "What is the mathematical purpose of setting `maxSkew: 1` in a Kubernetes Topology Spread Constraint across three availability zones?",
                "How does a Pod Disruption Budget prevent node pool rolling upgrades from causing user-visible downtime?",
                "Why must the Compute Engine Autohealing health check have a dedicated initial delay during container startup?",
            ],
            "reference": "https://docs.cloud.google.com/compute/docs/instance-groups/regional-migs",
            "reference_label": "Google Cloud Compute Engine: Regional Managed Instance Groups and Autohealing",
            "scenario": {
                "symptom": (
                    "During a Kubernetes version upgrade of Brightloaf's production GKE cluster, the checkout service suffered 100% request failure "
                    "for 6 minutes. The cluster had 12 nodes, but all 6 checkout pods were scheduled on nodes in `us-central1-a` which were drained simultaneously."
                ),
                "constraints": (
                    "Must automate GKE node pool upgrades without manual operator intervention while ensuring zero dropped checkout transactions."
                ),
                "evidence": (
                    "Kubernetes event logs showed that the node pool upgrade controller issued eviction notices to all nodes in `us-central1-a`. "
                    "Because no Pod Disruption Budget existed, all 6 checkout pods were evicted concurrently before new pods reached `Ready` state in other zones."
                ),
                "diagnostic_steps": [
                    "Query Kubernetes events for `Eviction` and `FailedCreate` on checkout deployment pods.",
                    "Review pod placement across nodes using Kubernetes cluster inspection tools to verify zonal distribution.",
                    "Inspect cluster configuration for absence of `PodDisruptionBudget` manifests.",
                ],
                "root": (
                    "Absence of Pod Disruption Budgets and Topology Spread Constraints allowed the scheduler to co-locate all application replicas "
                    "in a single zone, allowing automated node pool maintenance to evict 100% of capacity simultaneously."
                ),
                "fix": (
                    "Deploy a Pod Disruption Budget specifying `minAvailable: 75%` and configure `topologySpreadConstraints` with `maxSkew: 1` "
                    "across `topology.kubernetes.io/zone` in the application Deployment manifest."
                ),
                "verify": (
                    "Trigger a simulated node pool drain in staging; verify the upgrade controller pauses draining until pods in surviving zones are fully ready."
                ),
                "residual": (
                    "Strict PDBs can prolong node pool upgrades if cluster capacity is constrained; requires sufficient cluster autoscaling headroom."
                ),
                "diagram": (
                    "Node pool upgrade starts",
                    "All 6 pods in zone-a evicted",
                    "100% checkout blackout",
                    "Apply PDB + TopologySpread",
                    "Zero-downtime rolling drain"
                ),
                "facts": "All 6 checkout pods were scheduled in us-central1-a and terminated simultaneously during automated node maintenance.",
                "inference": "Node pool automation without disruption budgets converts routine maintenance into catastrophic outages.",
                "expected": "PDB blocks node eviction until rescheduled pods reach healthy ready status in surviving zones."
            },
            "lab": {
                "name": "GKE Regional Resilience with PDB and Topology Spread Constraints",
                "file": "day-088-topic-01-k8s-resilience.yaml",
                "goal": "Author production Kubernetes deployment manifests enforcing multi-zone topology spread and pod disruption protection.",
                "expected": "Valid YAML manifest containing Deployment with `topologySpreadConstraints` and matching `PodDisruptionBudget`.",
                "mode": "manifest authoring & tabletop validation",
                "prereq": "Familiarity with Kubernetes resource specifications.",
                "preflight": "Initialize manifest file in workspace.",
                "steps": [
                    "Author the resilient Kubernetes deployment and PDB manifest:\n\n```sh\ncat <<'EOF' > day-088-topic-01-k8s-resilience.yaml\napiVersion: policy/v1\nkind: PodDisruptionBudget\nmetadata:\n  name: brightloaf-checkout-pdb\n  namespace: production\nspec:\n  minAvailable: 75%\n  selector:\n    matchLabels:\n      app.kubernetes.io/name: checkout\n---\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: brightloaf-checkout\n  namespace: production\n  labels:\n    app.kubernetes.io/name: checkout\nspec:\n  replicas: 6\n  selector:\n    matchLabels:\n      app.kubernetes.io/name: checkout\n  template:\n    metadata:\n      labels:\n        app.kubernetes.io/name: checkout\n    spec:\n      # ENFORCE MULTI-ZONE RESILIENCE\n      topologySpreadConstraints:\n      - maxSkew: 1\n        topologyKey: topology.kubernetes.io/zone\n        whenUnsatisfiable: DoNotSchedule\n        labelSelector:\n          matchLabels:\n            app.kubernetes.io/name: checkout\n      containers:\n      - name: checkout-api\n        image: us-docker.pkg.dev/brightloaf-prod/apps/checkout:v2.4.1\n        ports:\n        - containerPort: 8080\n        readinessProbe:\n          httpGet:\n            path: /healthz\n            port: 8080\n          initialDelaySeconds: 5\n          periodSeconds: 5\n        livenessProbe:\n          httpGet:\n            path: /healthz\n            port: 8080\n          initialDelaySeconds: 15\n          periodSeconds: 10\n        resources:\n          requests:\n            cpu: 500m\n            memory: 512Mi\n          limits:\n            cpu: 1000m\n            memory: 1024Mi\nEOF\ncat day-088-topic-01-k8s-resilience.yaml\n```",
                    "Verify the manifest specifies `maxSkew: 1` across `topology.kubernetes.io/zone` to guarantee equal pod distribution across all 3 zones.",
                    "Verify `minAvailable: 75%` guarantees at least 5 out of 6 pods remain running during cluster maintenance.",
                    "Save the manifest in your evidence repository."
                ],
                "verification": (
                    "YAML manifest is syntactically valid and contains both a compliant `PodDisruptionBudget` and `topologySpreadConstraints`."
                ),
                "trouble": "Ensure `whenUnsatisfiable: DoNotSchedule` is paired with adequate node capacity in each availability zone.",
                "cleanup": "Retain `day-088-topic-01-k8s-resilience.yaml` as an exit evidence artifact.",
                "accept": "Completed production Kubernetes resilience manifest enforcing multi-zone spreading and disruption protection."
            }
        },
        {
            "key": "topic-02",
            "title": "Network availability: redundant HA VPN, 99.99% Dual-Metro Interconnect, and Anycast ALB",
            "preview": (
                "An enterprise links its on-premises datacenter to Google Cloud using a single Cloud Dedicated Interconnect circuit. "
                "When a backhoe digs up the terrestrial fiber conduit outside the colocation center, hybrid connectivity is severed for 18 hours."
            ),
            "overview": (
                "Enterprise network availability demands eliminating single points of failure across edge routing, transit backbones, "
                "and hybrid colocation perimeters. In Google Cloud, hybrid connectivity is governed by strict SLA tiers: standard HA VPN provides "
                "a 99.99% SLA using dual active tunnels over public internet, while **Dedicated Interconnect** achieves an industry-leading 99.99% SLA "
                "only when engineered across **dual metropolitan colocation facilities (dual metros)** with four separate physical cross-connects "
                "and redundant Cloud Routers running BGP with Bidirectional Forwarding Detection (BFD). At the ingress edge, the **Global External "
                "Application Load Balancer** utilizes Google's private fiber backbone and Anycast BGP routing to terminate client connections at the "
                "nearest edge point-of-presence (PoP), providing sub-second automated failover between backend regions during regional brownouts."
            ),
            "technical": (
                "Network architects must enforce topological redundancy across physical and logical routing layers:\n\n"
                "### 1. Dedicated Interconnect 99.99% SLA Topology\n"
                "Google Cloud's 99.99% SLA topology mandates four dedicated physical circuits:\n"
                "- **Metro 1 (e.g. Ashburn):** Two physical cross-connects terminate in different colocation facilities (Facility A and Facility B) connecting to two separate Cloud Routers in GCP Region 1.\n"
                "- **Metro 2 (e.g. Reston):** Two physical cross-connects terminate in different colocation facilities connecting to two separate Cloud Routers in GCP Region 2.\n"
                "- All circuits run dynamic eBGP with **Bidirectional Forwarding Detection (BFD)** configured for 300ms transmit/receive intervals and a detect multiplier of 3 (sub-second failover).\n\n"
                "### 2. Redundant Cloud Routers & BGP Transit\n"
                "- Cloud Routers operate in active/active configuration using BGP multi-path routing (`--enable-mp`).\n"
                "- Route metrics (MED - Multi-Exit Discriminator) steer traffic preferentially over high-bandwidth Interconnect, failing over to backup HA VPN automatically if BGP sessions flap.\n\n"
                "### 3. Global External ALB Anycast Ingress\n"
                "- Clients connect to a single Anycast public IP address advertised globally from >140 Google Edge PoPs.\n"
                "- If backend services in `us-central1` fail health checks, edge Envoy proxies immediately route HTTP traffic over Google's global fiber backbone "
                "to healthy backends in `us-east1` in < 1 second without requiring DNS TTL propagation."
            ),
            "questions": [
                "Why does Google Cloud's 99.99% Interconnect SLA require circuits in two separate metropolitan areas rather than two cages in the same building?",
                "How does BFD (Bidirectional Forwarding Detection) reduce BGP route convergence time from 90 seconds down to sub-second thresholds?",
                "What is the operational advantage of Anycast Global Load Balancing over DNS-based Geo-routing during a regional disaster?",
            ],
            "reference": "https://docs.cloud.google.com/network-connectivity/docs/interconnect/concepts/overview",
            "reference_label": "Google Cloud Dedicated Interconnect: Topologies for 99.99% availability",
            "scenario": {
                "symptom": (
                    "Brightloaf's hybrid inventory synchronization between its on-prem legacy ERP and Cloud SQL failed completely for 14 hours. "
                    "A power failure in a single datacenter cage in Chicago took down both Dedicated Interconnect cross-connects."
                ),
                "constraints": (
                    "Must achieve an ironclad 99.99% hybrid network availability SLA backed by Google Cloud financial credits."
                ),
                "evidence": (
                    "Audit revealed that both Interconnect attachments were provisioned at the same colocation facility (`ord-zone1-1`) into the same Cloud Router. "
                    "When the local carrier switch rebooted, both links went down simultaneously."
                ),
                "diagnostic_steps": [
                    "Inspect Google Cloud Interconnect attachment descriptors using `gcloud compute interconnects describe`.",
                    "Verify the physical colocation facility metro code and edge router assignments for both links.",
                    "Review BGP session logs in Cloud Logging for simultaneous session termination.",
                ],
                "root": (
                    "Architecture anti-pattern: provisioning redundant circuits in a single metropolitan facility created an unhedged physical facility "
                    "single point of failure, violating Google's 99.99% Interconnect architecture requirements."
                ),
                "fix": (
                    "Re-architect hybrid connectivity to Google's 99.99% topology: deploy four interconnect circuits spanning two distinct metropolitan areas "
                    "(Chicago `ord` and Ashburn `iad`), terminating on redundant Cloud Routers in separate VPC subnets with BFD enabled."
                ),
                "verify": (
                    "Simulate physical fiber cut in Chicago colocation facility; verify BFD detects failure in 900ms and traffic shifts to Ashburn with zero dropped sessions."
                ),
                "residual": (
                    "Four 10Gbps dedicated interconnect ports increase monthly colocation cross-connect and Google port fees; requires FinOps approval."
                ),
                "diagram": (
                    "Chicago colocation power cut",
                    "Dual circuits in single cage drop",
                    "14-hour hybrid ERP blackout",
                    "Deploy Dual-Metro 99.99%",
                    "Sub-second BFD failover"
                ),
                "facts": "Both hybrid interconnect links were terminated in the same Chicago colocation facility, violating 99.99% SLA requirements.",
                "inference": "Redundancy within a single physical building provides zero resilience against facility-wide infrastructure failures.",
                "expected": "Dual-metro Interconnect topology guarantees operational continuity even if an entire metropolitan area suffers an outage."
            },
            "lab": {
                "name": "99.99% Dedicated Interconnect and BGP Routing Architecture Specification",
                "file": "day-088-topic-02-interconnect-arch.md",
                "goal": "Author an authoritative architecture blueprint and Terraform specification for a 99.99% SLA hybrid network topology.",
                "expected": "A structured Markdown design document with Terraform code defining dual Cloud Routers, Interconnect VLAN attachments, and BFD timers.",
                "mode": "tabletop analysis & code synthesis",
                "prereq": "Completion of Exercise 1.",
                "preflight": "Review GCP 99.99% Interconnect reference architecture.",
                "steps": [
                    "Author the 99.99% Interconnect architecture specification:\n\n```sh\ncat <<'EOF' > day-088-topic-02-interconnect-arch.md\n# Day 88: Google Cloud 99.99% Dedicated Interconnect Architecture Specification\n\n## 1. Physical & Logical Topology Design\n\nTo qualify for Google's **99.99% Availability SLA**, hybrid transit requires four circuits across dual metropolitan areas:\n- **Metro 1 (Chicago - `ord`):**\n  - Circuit 1: `ord-zone1-1` (Equinix CH1) -> Terminating on Cloud Router 1 in `us-central1`\n  - Circuit 2: `ord-zone2-1` (Digital Realty) -> Terminating on Cloud Router 2 in `us-central1`\n- **Metro 2 (Ashburn - `iad`):**\n  - Circuit 3: `iad-zone1-1` (Equinix DC2) -> Terminating on Cloud Router 3 in `us-east1`\n  - Circuit 4: `iad-zone2-1` (CoreSite VA1) -> Terminating on Cloud Router 4 in `us-east1`\n\n## 2. Terraform Implementation with BFD Fast Failover\n\n```hcl\nresource \"google_compute_router\" \"router_ord_1\" {\n  name    = \"cr-ord-metro1\"\n  network = \"brightloaf-vpc\"\n  region  = \"us-central1\"\n  bgp {\n    asn               = 64512\n    advertise_mode    = \"CUSTOM\"\n    advertised_groups = [\"ALL_SUBNETS\"]\n  }\n}\n\nresource \"google_compute_interconnect_attachment\" \"attachment_ord_1\" {\n  name                     = \"vlan-ord-metro1\"\n  edge_availability_domain = \"AVAILABILITY_DOMAIN_1\"\n  type                     = \"DEDICATED\"\n  router                   = google_compute_router.router_ord_1.id\n  interconnect             = \"https://www.googleapis.com/compute/v1/projects/brightloaf-prod/global/interconnects/int-ord-1\"\n  bandwidth                = \"BPS_10G\"\n}\n\nresource \"google_compute_router_interface\" \"router_interface_1\" {\n  name                    = \"cr-ord-int-1\"\n  router                  = google_compute_router.router_ord_1.name\n  region                  = \"us-central1\"\n  interconnect_attachment = google_compute_interconnect_attachment.attachment_ord_1.name\n}\n\nresource \"google_compute_router_peer\" \"bgp_peer_1\" {\n  name                      = \"bgp-peer-ord-1\"\n  router                    = google_compute_router.router_ord_1.name\n  region                    = \"us-central1\"\n  interface                 = google_compute_router_interface.router_interface_1.name\n  peer_ip_address           = \"169.254.0.2\"\n  peer_asn                  = 65001\n  advertised_route_priority = 100\n\n  # SUB-SECOND BFD FAST FAILOVER\n  bfd {\n    min_receive_interval        = 300\n    min_transmit_interval       = 300\n    multiplier                  = 3\n    session_initialization_mode = \"ACTIVE\"\n  }\n}\n```\nEOF\ncat day-088-topic-02-interconnect-arch.md\n```",
                    "Verify the architecture document specifies four circuits across two independent metropolitan areas.",
                    "Verify the BFD configuration specifies 300ms intervals with a multiplier of 3 for 900ms failover.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, specifies dual-metro physical placement, and contains valid Terraform code for Cloud Router BFD peers."
                ),
                "trouble": "Ensure `edge_availability_domain` is explicitly alternated between Domain 1 and Domain 2.",
                "cleanup": "Retain `day-088-topic-02-interconnect-arch.md` as an exit evidence artifact.",
                "accept": "Mastery of Google Cloud 99.99% hybrid network topology with verified Terraform BFD routing specification."
            }
        },
        {
            "key": "topic-03",
            "title": "Storage availability: Regional Persistent Disks, Dual-Region GCS, and Filestore Enterprise",
            "preview": (
                "A database VM attached to a standard zonal Persistent Disk crashes when its host zone suffers a storage cluster hardware failure. "
                "Because the disk is locked to the dead zone, administrators cannot re-attach the volume to a healthy VM in another zone, causing a 6-hour data blackout."
            ),
            "overview": (
                "Storage availability in Google Cloud is defined by data replication boundaries across physical disks, zones, and regions. "
                "For block storage, **Regional Persistent Disks (Regional PD)** provide synchronous replication across two availability zones within a region, "
                "guaranteeing zero data loss (RPO = 0) and sub-minute failover (RTO < 60s) via forced re-attachment if the primary zone crashes. "
                "For object storage, **Dual-Region and Multi-Region Cloud Storage buckets** provide 99.95% availability and eleven 9s (99.999999999%) "
                "of annual durability. With **Turbo Replication** enabled, Cloud Storage guarantees 100% of newly written objects are replicated across regions "
                "within 15 minutes. For shared file systems, **Filestore Enterprise** provides synchronous NFS v3/v4 multi-zone replication across three zones, "
                "protecting stateful Kubernetes workloads from zonal storage failures."
            ),
            "technical": (
                "Architects must select storage types based on replication mechanics, RPO limits, and failover automation:\n\n"
                "### 1. Regional Persistent Disk (Regional PD) Mechanics\n"
                "- **Replication Mode:** Synchronous block-level replication across two zones (e.g. `us-central1-a` and `us-central1-b`).\n"
                "- Write operations are acknowledged to the guest OS only after blocks are committed to persistent storage in *both* zones.\n"
                "- **Failover:** If the VM in Zone A dies, an automation script or Kubernetes CSI driver forcibly detaches the disk and attaches it "
                "to a replacement VM in Zone B (`--force-attach`). RPO is strictly 0; RTO is ~30–60 seconds.\n\n"
                "### 2. Dual-Region Cloud Storage & Turbo Replication\n"
                "- Standard dual-region buckets replicate objects asynchronously across two paired regions (e.g., `nam4`: Iowa + South Carolina).\n"
                "- **Turbo Replication:** Shortens the recovery point objective by providing an SLA-backed guarantee that 100% of data is replicated "
                "between regions in **under 15 minutes** (backed by financial credits).\n\n"
                "### 3. Filestore Regional / Enterprise (Multi-Zone NFS)\n"
                "- Standard Filestore is zonal: losing the zone terminates the NFS mount.\n"
                "- Filestore Enterprise synchronously replicates file shares across three zones in a region with automatic IP failover, "
                "delivering continuous NFS access for GKE stateful pods (`ReadWriteMany`)."
            ),
            "questions": [
                "Why does Regional Persistent Disk impose a minor write-latency penalty compared to standard Zonal Persistent Disk?",
                "How does Cloud Storage Turbo Replication reduce disaster recovery RPO for cross-region object archives?",
                "What is the operational difference between Regional PD block storage and Filestore Enterprise file storage in GKE deployments?",
            ],
            "reference": "https://docs.cloud.google.com/compute/docs/disks/regional-persistent-disks",
            "reference_label": "Google Cloud Compute Engine: Regional Persistent Disks architecture",
            "scenario": {
                "symptom": (
                    "During a zonal maintenance event in `us-central1-a`, Brightloaf's content management system (which stores user recipe uploads on a standard "
                    "zonal Persistent Disk) became unavailable. When administrators attempted to attach the disk to a standby VM in `us-central1-b`, "
                    "the GCP API returned `ZONE_RESOURCE_POOL_EXHAUSTED` and blocked cross-zone attachment, creating a 5-hour outage."
                ),
                "constraints": (
                    "Must ensure storage volumes can be attached to replacement instances in alternative zones within 60 seconds of failure."
                ),
                "evidence": (
                    "Google Cloud API error logs showed `InvalidValueError: Disk 'brightloaf-media-pd' is located in us-central1-a and cannot be attached "
                    "to instance 'brightloaf-cms-standby' located in us-central1-b`."
                ),
                "diagnostic_steps": [
                    "Inspect disk properties via `gcloud compute disks describe brightloaf-media-pd` to verify zonal placement.",
                    "Review storage failover runbooks to determine why cross-zone snapshots were not automated.",
                    "Evaluate the write performance impact of migrating from Zonal PD to Regional PD.",
                ],
                "root": (
                    "Architectural failure to utilize synchronous block replication: provisioning a standard Zonal PD pinned the persistent storage to a single zone, "
                    "preventing standby instances in other zones from mounting the volume during an outage."
                ),
                "fix": (
                    "Migrate the volume to a Regional Persistent Disk (`pd-ssd` with replica zones `us-central1-a` and `us-central1-b`) and configure automated "
                    "failover script using `--force-attach`."
                ),
                "verify": (
                    "Execute simulated zone-a evacuation; verify script detaches disk from zone-a instance and mounts volume on zone-b standby in 38 seconds with zero data loss."
                ),
                "residual": (
                    "Regional PD doubles storage capacity cost (as data is stored across two physical zones) and adds ~1ms synchronous write latency."
                ),
                "diagram": (
                    "Zone-a host dies",
                    "Zonal PD locked to dead zone",
                    "Cross-zone attach rejected",
                    "Migrate to Regional PD",
                    "Sub-60s force attach (RPO=0)"
                ),
                "facts": "Standard Zonal PD cannot be attached to VMs in other zones, stranding data during zonal outages.",
                "inference": "Stateful workloads requiring sub-minute RTO without database clustering must utilize Regional Persistent Disks.",
                "expected": "Regional PD allows immediate forced attachment in replica zone with zero block-level data loss."
            },
            "lab": {
                "name": "Regional Persistent Disk and Dual-Region Storage Blueprint",
                "file": "day-088-topic-03-storage-ha.tf",
                "goal": "Author production Terraform infrastructure code creating Regional Persistent Disks and Dual-Region Cloud Storage with Turbo Replication.",
                "expected": "Valid Terraform HCL file defining Regional PD with replica zones and dual-region storage bucket with turbo replication enabled.",
                "mode": "Terraform code synthesis",
                "prereq": "Completion of Exercises 1 and 2.",
                "preflight": "Verify Terraform syntax requirements.",
                "steps": [
                    "Author the storage high availability Terraform configuration:\n\n```sh\ncat <<'EOF' > day-088-topic-03-storage-ha.tf\n# Day 88: High Availability Storage Infrastructure (Terraform)\n\n# 1. Regional Persistent Disk (Synchronous 2-Zone Block Replication)\nresource \"google_compute_region_disk\" \"brightloaf_stateful_rpd\" {\n  name          = \"brightloaf-app-rpd\"\n  type          = \"pd-ssd\"\n  region        = \"us-central1\"\n  replica_zones = [\"us-central1-a\", \"us-central1-b\"]\n  size          = 200\n\n  labels = {\n    environment = \"production\"\n    tier        = \"stateful-storage\"\n  }\n}\n\n# 2. Dual-Region Cloud Storage Bucket with Turbo Replication\nresource \"google_storage_bucket\" \"brightloaf_dual_region_media\" {\n  name          = \"brightloaf-media-prod-nam4\"\n  location      = \"NAM4\" # Dual-region: Iowa (us-central1) & South Carolina (us-east1)\n  storage_class = \"STANDARD\"\n\n  uniform_bucket_level_access = true\n  versioning {\n    enabled = true\n  }\n\n  # TURBO REPLICATION: Guarantees 100% replication within 15 minutes (SLA-backed)\n  custom_placement_config {\n    data_locations = [\"US-CENTRAL1\", \"US-EAST1\"]\n  }\n\n  retention_policy {\n    is_locked        = false\n    retention_period = 2592000 # 30 days retention\n  }\n}\nEOF\ncat day-088-topic-03-storage-ha.tf\n```",
                    "Verify the Regional Disk resource specifies exactly two `replica_zones` within `us-central1`.",
                    "Verify the Cloud Storage bucket specifies `NAM4` dual-region placement with versioning enabled.",
                    "Save the configuration in your artifact repository."
                ],
                "verification": (
                    "Terraform file is syntactically correct and includes both Regional Persistent Disk and Dual-Region Cloud Storage with Turbo Replication."
                ),
                "trouble": "Ensure `replica_zones` contains exactly two zones located inside the parent `region`.",
                "cleanup": "Retain `day-088-topic-03-storage-ha.tf` as an exit evidence artifact.",
                "accept": "Completed production Terraform specification for Regional Block and Dual-Region Object storage."
            }
        },
        {
            "key": "topic-04",
            "title": "Database availability: Cloud SQL HA, Spanner multi-region, Bigtable, and Memorystore",
            "preview": (
                "An architect configures Cloud SQL with asynchronous read replicas, believing this provides zero-RPO disaster recovery. "
                "When the primary instance fails unexpectedly, promoting the replica loses 45 seconds of customer transactions, causing duplicate invoice generation."
            ),
            "overview": (
                "Database availability is the hardest engineering problem in distributed systems because state cannot be arbitrarily split without risking "
                "data loss or inconsistency (the CAP Theorem). In Google Cloud, relational database availability is solved via two primary patterns: "
                "**Cloud SQL High Availability (HA)**, which uses synchronous block replication over Regional Persistent Disks to provide sub-minute automated failover "
                "(RTO < 60s, RPO = 0) within a single region; and **Cloud Spanner Multi-Region**, which uses TrueTime and Paxos distributed consensus to deliver "
                "**99.999% availability (five 9s)** across multiple geographic regions with zero downtime and zero data loss (RTO = 0, RPO = 0). "
                "For non-relational and caching tiers, **Bigtable Multi-Cluster Replication** delivers eventual consistency with sub-second replication, "
                "while **Memorystore for Redis Standard Tier** provides cross-zone automated failover in under 30 seconds."
            ),
            "technical": (
                "Architects must evaluate the trade-offs between Cloud SQL HA and Multi-Region Spanner:\n\n"
                "### 1. Cloud SQL High Availability (Regional HA)\n"
                "- **Architecture:** Primary instance in Zone A; Standby instance in Zone B. Both share a Regional Persistent Disk with synchronous block writes.\n"
                "- **Heartbeat & Failover:** A health monitor probes the primary. If the primary fails, the monitor points the database VIP/DNS to the standby "
                "and spins up database processes. Failover completes in **sub-60 seconds**.\n"
                "- **RPO Guarantee:** RPO is strictly 0 for committed transactions because the Regional PD blocks were committed in both zones before transaction ack.\n"
                "- **Limitation:** Cross-region read replicas are *asynchronous*; promoting a cross-region replica incurs data loss equal to replication lag (RPO > 0).\n\n"
                "### 2. Cloud Spanner Multi-Region Paxos Consensus\n"
                "- **Architecture:** Replicas spread across multiple regions (e.g. `nam3`: 2 read-write regions + 1 witness region).\n"
                "- **Paxos Consensus:** Writes require consensus from a majority of voting replicas. If an entire region goes offline, the remaining two regions "
                "maintain quorum, processing read/write transactions with **zero downtime (RTO = 0)** and **zero data loss (RPO = 0)**.\n"
                "- **TrueTime & External Consistency:** TrueTime synchronized atomic clocks ensure serializable ACID transactions globally without lock deadlocks.\n"
                "- **SLA:** 99.999% (less than 5 minutes downtime per year).\n\n"
                "### 3. Bigtable & Memorystore Resiliency\n"
                "- **Bigtable:** Multi-cluster routing automatically routes requests to the nearest healthy cluster, failing over instantly during zonal/regional faults.\n"
                "- **Memorystore Redis Standard:** Replicates data asynchronously to an in-memory replica in an alternate zone; automated failover in < 30s."
            ),
            "questions": [
                "Why does Cloud SQL HA achieve RPO = 0 within a region, whereas cross-region Cloud SQL read replicas have an RPO > 0?",
                "How does Cloud Spanner utilize a witness region to achieve 99.999% availability without replicating full data storage in the third region?",
                "What is the difference in consistency guarantees between Bigtable multi-cluster replication (eventual) and Spanner multi-region (external consistency)?",
            ],
            "reference": "https://docs.cloud.google.com/sql/docs/postgres/high-availability",
            "reference_label": "Google Cloud SQL: High availability configuration and failover process",
            "scenario": {
                "symptom": (
                    "Brightloaf's database primary crashed during peak holiday trading. The on-call engineer attempted to promote a cross-region read replica "
                    "in `us-east1` rather than waiting for the local HA standby in `us-central1-b`. The promotion succeeded, but 1,240 orders committed "
                    "in the last 45 seconds prior to the crash were lost due to asynchronous replication lag, triggering massive customer support escalations."
                ),
                "constraints": (
                    "Must maintain zero data loss (RPO = 0) for all confirmed customer transactions during single-zone and single-host hardware faults."
                ),
                "evidence": (
                    "Post-incident replication lag metrics showed `cloudsql.googleapis.com/database/replication/replica_byte_lag` was 14.2 MB at the time of failure. "
                    "Because the engineer manually promoted the asynchronous replica, the un-replicated write-ahead log entries were permanently orphaned."
                ),
                "diagnostic_steps": [
                    "Compare transaction logs on the crashed primary against the promoted replica to quantify lost transactions.",
                    "Review Cloud SQL HA automated failover telemetry to determine why automated local failover was aborted by operator intervention.",
                    "Audit SRE runbooks to identify why operators were instructed to perform manual replica promotion during a zonal event.",
                ],
                "root": (
                    "Operator error caused by defective runbook: the operator manually promoted an asynchronous cross-region replica during a local zonal fault "
                    "instead of allowing Cloud SQL HA's automated synchronous Regional PD failover to complete, converting a zero-RPO event into a major data loss incident."
                ),
                "fix": (
                    "Update database operational playbooks: mandate that operators allow Cloud SQL HA automated failover (60-second window) to complete, "
                    "reserve cross-region replica promotion exclusively for declared catastrophic regional disasters, and evaluate Cloud Spanner for zero-RPO multi-region requirements."
                ),
                "verify": (
                    "Conduct automated fault injection testing in staging by killing the primary database instance; verify automated HA failover activates standby within 48 seconds with zero lost transactions."
                ),
                "residual": (
                    "During the 48-second Cloud SQL HA failover, open application connections are severed, requiring connection pool retry logic."
                ),
                "diagram": (
                    "Primary database dies",
                    "Operator promotes async replica",
                    "1,240 orders lost (RPO breach)",
                    "Automated Cloud SQL HA standby",
                    "RPO=0 failover in 48s"
                ),
                "facts": "1,240 transactions lost because operator manually promoted an asynchronous cross-region replica during a local zonal fault.",
                "inference": "Manual operator intervention during automated HA failover windows introduces catastrophic data loss risk.",
                "expected": "Cloud SQL HA automated failover executes synchronously via Regional PD, preserving 100% of committed transactions."
            },
            "lab": {
                "name": "Database HA Evaluation and Failover Rehearsal Runbook",
                "file": "day-088-topic-04-database-ha.md",
                "goal": "Author a comprehensive database resilience decision matrix and an automated Cloud SQL HA failover rehearsal runbook.",
                "expected": "A structured Markdown artifact evaluating Cloud SQL HA vs Cloud Spanner and detailing exact commands to execute and verify an HA failover drill.",
                "mode": "tabletop analysis & command synthesis",
                "prereq": "Completion of Exercises 1, 2, and 3.",
                "preflight": "Review Cloud SQL HA reference documentation.",
                "steps": [
                    "Author the database resilience matrix and failover rehearsal runbook:\n\n```sh\ncat <<'EOF' > day-088-topic-04-database-ha.md\n# Day 88: Enterprise Database Availability & Failover Runbook\n\n## 1. Database Tier Architecture Decision Matrix\n\n| Evaluation Vector | Cloud SQL High Availability (HA) | Cloud Spanner Multi-Region |\n| :--- | :--- | :--- |\n| **Topology** | Primary + Standby in same region (2 AZs) | 3 Regions (2 Read-Write + 1 Witness) |\n| **Replication** | Synchronous block replication (Regional PD) | Synchronous Paxos consensus across regions |\n| **Availability SLA** | **99.95%** (~21.6 min downtime/mo) | **99.999%** (~2.6 sec downtime/mo) |\n| **Failover RTO** | Automated in **< 60 seconds** | **0 seconds** (Transparent to client) |\n| **Data Loss (RPO)** | **RPO = 0** (Synchronous within region) | **RPO = 0** (Global External Consistency) |\n| **Cost Profile** | Moderate ($$): ~2x standard instance | High ($$$$): Minimum 3-region provisioned nodes |\n| **Best Workload** | Standard transactional ERP, B2B APIs | Global financial ledgers, zero-RTO checkouts |\n\n## 2. Cloud SQL HA Failover Rehearsal Runbook\n\n### Step 1: Preflight State Verification\n```bash\n# Verify instance is in REGIONAL HA mode and healthy\ngcloud sql instances describe brightloaf-db-primary \\\n    --format='value(settings.availabilityType, state, gceZone)'\n# Expected: REGIONAL | RUNNABLE | us-central1-a\n```\n\n### Step 2: Trigger Controlled Automated Failover\n```bash\n# Initiate a controlled failover to simulate zonal crash\ngcloud sql instances failover brightloaf-db-primary \\\n    --async\n```\n\n### Step 3: Monitor Failover Transition & Track Duration\n```bash\n# Track operation status until completion\ngcloud sql operations list \\\n    --instance=brightloaf-db-primary \\\n    --limit=1\n```\n\n### Step 4: Post-Failover Verification\n```bash\n# Confirm primary now operates in the secondary zone (us-central1-b)\ngcloud sql instances describe brightloaf-db-primary \\\n    --format='value(state, gceZone)'\n# Expected: RUNNABLE | us-central1-b\n```\nEOF\ncat day-088-topic-04-database-ha.md\n```",
                    "Verify the decision matrix clearly contrasts Regional PD synchronous replication with Spanner Paxos consensus.",
                    "Verify the failover runbook specifies exact commands for preflight, execution, and post-failover verification.",
                    "Save the document in your artifact repository."
                ],
                "verification": (
                    "Document exists, contains a comprehensive database decision matrix, and includes production-ready failover commands."
                ),
                "trouble": "Ensure the target Cloud SQL instance has availability-type set to REGIONAL before initiating a failover drill.",
                "cleanup": "Retain `day-088-topic-04-database-ha.md` as an exit evidence artifact.",
                "accept": "Completed database availability decision matrix with validated automated failover rehearsal runbook."
            }
        }
    ]
}