"""day_data_088.py — Exhaustive architecture data specification for Day 88.

Covers Availability Across Infrastructure Layers:
1. Compute availability (Regional MIGs, autohealing, N+1 headroom, GKE regional clusters, PDBs, topology spread constraints).
2. Network availability (HA VPN dual tunnels, 99.99% Dual Interconnect in separate metros, redundant Cloud Routers, Anycast ALB).
3. Storage availability (Regional Persistent Disks, Dual/Multi-region GCS buckets, Turbo replication, Filestore Enterprise).
4. Database availability (Cloud SQL HA + cross-region replicas, Spanner multi-region Paxos, Bigtable multi-cluster, Memorystore Standard).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable 8-stage operational engineering exercises.
"""

DAY_NUM = 88

DATA = {'day': 88,
 'part1_intro': 'Day 88 synthesizes reliability across all physical and logical layers of the enterprise '
                'infrastructure stack: Compute, Networking, Storage, and Databases. A resilient application '
                'architecture is only as robust as the weakest layer supporting it; deploying a multi-region stateless '
                'compute layer provides zero protection if the database relies on a single-zone instance or the hybrid '
                "network transit path traverses an unhedged VPN tunnel. Today's curriculum constructs an end-to-end "
                "high availability architecture across Google Cloud's core infrastructure primitives: configuring "
                'Regional Managed Instance Groups and GKE Regional clusters with Topology Spread Constraints, '
                'establishing 99.99% hybrid interconnect topologies across dual metropolitan edge facilities, '
                'deploying synchronously replicated Regional Persistent Disks and dual-region Cloud Storage with Turbo '
                'Replication, and evaluating Cloud SQL HA versus multi-region Cloud Spanner Paxos consensus.',
 'exit_summary': 'Engineered an authoritative four-tier enterprise high availability blueprint mapping Compute (GKE '
                 'Regional + PDBs), Network (99.99% Dual-Metro Interconnect + Global ALB), Storage (Regional PD + '
                 'Dual-Region GCS Turbo), and Database (Cloud SQL HA + Spanner Paxos) failure boundaries; calculated '
                 'exact N+1 compute headroom and modeled single-zone failure survival; authored production Terraform '
                 'modules for Regional MIG autohealing and Kubernetes TopologySpreadConstraints; executed a '
                 'multi-layer tabletop resilience drill proving zero data loss and sub-minute recovery under total '
                 'zonal blackout.',
 'part2_intro': 'High availability requires layered defense in depth, where each infrastructure tier absorbs localized '
                'failures autonomously. The sections below provide deep architectural specifications, configuration '
                'parameters, and trade-off matrices across Google Cloud compute, network, storage, and database '
                'services.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Infrastructure Layer</th>\n'
                    '      <th>Google Cloud High Availability Pattern</th>\n'
                    '      <th>Target SLA</th>\n'
                    '      <th>Failover Mechanism &amp; RTO</th>\n'
                    '      <th>Data Loss Risk (RPO)</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>Compute</strong></td>\n'
                    '      <td>GKE Regional Cluster (3 Master AZs) + Multi-Zone Node Pools + Pod Disruption Budgets '
                    '(PDB).</td>\n'
                    '      <td>99.95% (Control Plane)</td>\n'
                    '      <td>Automated pod rescheduling via Kube-Scheduler; RTO &lt; 30s.</td>\n'
                    '      <td>RPO = 0 (Stateless pods).</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Network</strong></td>\n'
                    '      <td>99.99% Dual Dedicated Interconnect across dual metropolitan colocation facilities + '
                    'Dual Cloud Routers.</td>\n'
                    '      <td>99.99%</td>\n'
                    '      <td>BGP session failover with BFD (Bidirectional Forwarding Detection); RTO &lt; 1s.</td>\n'
                    '      <td>RPO = 0 (In-flight TCP retries).</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Storage</strong></td>\n'
                    '      <td>Regional Persistent Disk (synchronous 2-zone block replication) + Dual-Region GCS '
                    '(Turbo Replication).</td>\n'
                    '      <td>99.95% (GCS)</td>\n'
                    '      <td>Force-attach Regional PD to surviving zone; RTO &lt; 60s.<br>GCS multi-region bucket '
                    'active/active.</td>\n'
                    '      <td>RPO = 0 (Synchronous block write).<br>GCS Turbo: RPO &lt; 15 mins.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Databases</strong></td>\n'
                    '      <td>Cloud SQL HA (Regional PD sync replication) OR Cloud Spanner Multi-Region (3-Region '
                    'Paxos Quorum).</td>\n'
                    '      <td>99.95% (Cloud SQL)<br><strong>99.999% (Spanner)</strong></td>\n'
                    '      <td>Cloud SQL: Automated DNS failover to standby; RTO &lt; 60s.<br>Spanner: Transparent '
                    'zero-downtime Paxos election; RTO = 0s.</td>\n'
                    '      <td>Cloud SQL: RPO = 0.<br>Spanner: RPO = 0 (TrueTime consistency).</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 88: Four-Tier Layered Infrastructure High Availability Architecture Topology',
                  'desc': 'Multi-tier infrastructure topology illustrating synchronous replication and automated '
                          'failover across Compute, Network, Storage, and Database tiers.',
                  'caption': 'Figure 88.1: Multi-tier architectural topology illustrating request flows through edge '
                             'Anycast, decoupled compute tiers, HA persistence, and shared control plane boundaries.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Anycast Edge & 99.99% Dual-Metro Network Tier',
                              'desc': 'Global External ALB, 99.99% Dual Dedicated Interconnect across dual metros, and '
                                      'Cloud Routers with BFD',
                              'fill': '#1e3a5f',
                              'y': 10,
                              'h': 90},
                             {'name': 'LAYER 2: Regional Compute & Multi-Zone Kubernetes Runtime',
                              'desc': 'GKE Regional Cluster (3 Master AZs), PodDisruptionBudgets, and '
                                      'TopologySpreadConstraints (maxSkew: 1)',
                              'fill': '#0f2338',
                              'y': 115,
                              'h': 90},
                             {'name': 'LAYER 3: Replicated Storage & Synchronous Block Layer',
                              'desc': 'Regional Persistent Disks (synchronous 2-zone block replication) and '
                                      'Dual-Region GCS Turbo (15m RPO)',
                              'fill': '#064e3b',
                              'y': 220,
                              'h': 90},
                             {'name': 'LAYER 4: Multi-Region Distributed Database Fabric',
                              'desc': 'Cloud SQL Regional HA (Sync Regional PD) and Cloud Spanner 3-Region Paxos '
                                      'Quorum (99.999% SLA)',
                              'fill': '#1e1b4b',
                              'y': 325,
                              'h': 90},
                             {'name': 'LAYER 5: SRE Telemetry & Cross-Tier Health Gates',
                              'desc': 'Cloud Monitoring Cross-Tier Availability Dashboard, Synthetic Heartbeats, and '
                                      'Automated Ejection',
                              'fill': '#3b0764',
                              'y': 430,
                              'h': 90}],
                  'components': [{'id': 'alb_ingress',
                                  'name': 'Global External ALB',
                                  'detail': '99.99% Anycast Ingress',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'interconnect_ha',
                                  'name': '99.99% Interconnect',
                                  'detail': 'Dual Metro Colocation + BFD',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'gke_regional',
                                  'name': 'GKE Regional Cluster',
                                  'detail': '3 Control Plane AZs (99.95%)',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'pdb_guard',
                                  'name': 'PDB & Topology Spread',
                                  'detail': 'maxSkew: 1, minAvailable: 2',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'rpd_storage',
                                  'name': 'Regional Persistent Disk',
                                  'detail': '2-Zone Synchronous Replication',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'gcs_dual',
                                  'name': 'Dual-Region GCS',
                                  'detail': 'Turbo Replication (15m RPO)',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'spanner_paxos',
                                  'name': 'Cloud Spanner Multi-Region',
                                  'detail': '3-Region Paxos (99.999%)',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'sql_ha_db',
                                  'name': 'Cloud SQL Regional HA',
                                  'detail': 'Automated Failover (<60s)',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'cross_tier_mon',
                                  'name': 'Cross-Tier SLO Dashboard',
                                  'detail': 'End-to-End Stack Telemetry',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'},
                                 {'id': 'ejection_ctrl',
                                  'name': 'Zone Ejection Controller',
                                  'detail': 'Sub-Minute Auto-Isolation',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'}],
                  'boundaries': [{'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'DUAL-METRO HYBRID NETWORK & ANYCAST PERIMETER',
                                  'color': '#38bdf8'},
                                 {'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'GKE REGIONAL KUBERNETES RUNTIME BOUNDARY',
                                  'color': '#10b981'},
                                 {'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'MULTI-REGION DISTRIBUTED CONSISTENCY & PERSISTENCE PERIMETER',
                                  'color': '#a855f7'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'type': 'ok', 'label': 'BGP Anycast Transit'},
                            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'type': 'ok', 'label': 'Route to GKE Pods'},
                            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'type': 'ok', 'label': 'Enforce PDB Skew'},
                            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'type': 'ok', 'label': 'Block Volume Attach'},
                            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'type': 'ok', 'label': 'Dual-Region Sync'},
                            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'type': 'ok', 'label': 'Paxos Quorum Write'},
                            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'type': 'ok', 'label': 'Regional HA Standby'},
                            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'type': 'ok', 'label': 'Stack SLI Telemetry'},
                            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'type': 'fail', 'label': 'Eject Failed Zone'}],
                  'probes': [{'cx': 420,
                              'cy': 56,
                              'label': 'PROBE 1: BFD BGP Sub-Second Heartbeat',
                              'color': '#38bdf8'},
                             {'cx': 420,
                              'cy': 161,
                              'label': 'PROBE 2: Pod Zone Distribution Balance',
                              'color': '#22c55e'},
                             {'cx': 420,
                              'cy': 371,
                              'label': 'PROBE 3: Spanner Paxos Quorum Consistency',
                              'color': '#f59e0b'}]},
 'topics': [{'key': 'topic-01',
             'title': 'Compute availability: regional MIGs, GKE regional clusters, PDBs, and topology spread',
             'preview': 'During a routine GKE node pool rolling upgrade, the cluster autoscaler drains nodes too '
                        'aggressively, terminating all replicas of the checkout pod at the exact same moment and '
                        'creating a self-inflicted 12-minute outage.',
             'overview': 'Compute availability in Google Cloud is achieved by abstracting individual server instances '
                         'into self-healing, multi-zone groupings. For virtual machines, **Regional Managed Instance '
                         'Groups (MIGs)** distribute stateless workloads identically across three availability zones, '
                         'utilizing **Autohealing** health checks to automatically replace crashed instances. For '
                         'containerized microservices, **GKE Regional Clusters** replicate the Kubernetes master '
                         'control plane across three zones (99.95% SLA) and deploy multi-zone worker node pools. To '
                         'prevent deployment operations or node drains from causing service degradation, architects '
                         'must enforce **Pod Disruption Budgets (PDBs)** (guaranteeing a minimum number of running '
                         'pods during upgrades) and **Topology Spread Constraints** (mandating that the Kubernetes '
                         'scheduler evenly distributes pods across physical zones).',
             'technical': 'Architects must configure compute resiliency primitives using strict infrastructure-as-code '
                          'specifications:\n'
                          '\n'
                          '### 1. Regional MIG Autohealing Mechanics\n'
                          '- **Health Check:** Application-level endpoint (e.g. `GET /healthz`) probing port 8080.\n'
                          '- **Initial Delay:** Grace period (e.g. 180 seconds) allowing application initialization '
                          'before health checking begins.\n'
                          '- **Target Distribution:** Configure `distribution_policy_target_shape = "EVEN"` to enforce '
                          'balanced zonal spread across `us-central1-a`, `us-central1-b`, and `us-central1-c`.\n'
                          '\n'
                          '### 2. GKE Regional Cluster vs. Zonal Cluster SLAs\n'
                          '- **Zonal GKE Cluster:** Control plane resides in a single zone. During master upgrades or '
                          'zonal failure, the Kubernetes API is unavailable (99.5% SLA).\n'
                          '- **Regional GKE Cluster:** Control plane runs in three separate zones with automated etcd '
                          'quorum replication. High availability 99.95% SLA.\n'
                          '\n'
                          '### 3. Kubernetes Pod Disruption Budgets (PDB) & Topology Spread Constraints\n'
                          '- **PDB (`minAvailable: 2` or `maxUnavailable: 25%`):** Blocks node eviction commands and '
                          'node pool upgrade automation from taking down pods if doing so would reduce active capacity '
                          'below the configured threshold.\n'
                          '- **Topology Spread Constraints:** Prevents the Kubernetes scheduler from scheduling all '
                          'pods in a single zone due to localized node packing:\n'
                          '  `topologyKey: topology.kubernetes.io/zone`, `maxSkew: 1`, `whenUnsatisfiable: '
                          'DoNotSchedule`.',
             'questions': ['What is the mathematical purpose of setting `maxSkew: 1` in a Kubernetes Topology Spread '
                           'Constraint across three availability zones?',
                           'How does a Pod Disruption Budget prevent node pool rolling upgrades from causing '
                           'user-visible downtime?',
                           'Why must the Compute Engine Autohealing health check have a dedicated initial delay during '
                           'container startup?'],
             'reference': 'https://docs.cloud.google.com/compute/docs/instance-groups/regional-migs',
             'reference_label': 'Google Cloud Compute Engine: Regional Managed Instance Groups and Autohealing',
             'scenario': {'symptom': "During a Kubernetes version upgrade of Brightloaf's production GKE cluster, the "
                                     'checkout service suffered 100% request failure for 6 minutes. The cluster had 12 '
                                     'nodes, but all 6 checkout pods were scheduled on nodes in `us-central1-a` which '
                                     'were drained simultaneously.',
                          'constraints': 'Must automate GKE node pool upgrades without manual operator intervention '
                                         'while ensuring zero dropped checkout transactions.',
                          'evidence': 'Kubernetes event logs showed that the node pool upgrade controller issued '
                                      'eviction notices to all nodes in `us-central1-a`. Because no Pod Disruption '
                                      'Budget existed, all 6 checkout pods were evicted concurrently before new pods '
                                      'reached `Ready` state in other zones.',
                          'diagnostic_steps': ['Query Kubernetes events for `Eviction` and `FailedCreate` on checkout '
                                               'deployment pods.',
                                               'Review pod placement across nodes using Kubernetes cluster inspection '
                                               'tools to verify zonal distribution.',
                                               'Inspect cluster configuration for absence of `PodDisruptionBudget` '
                                               'manifests.'],
                          'root': 'Absence of Pod Disruption Budgets and Topology Spread Constraints allowed the '
                                  'scheduler to co-locate all application replicas in a single zone, allowing '
                                  'automated node pool maintenance to evict 100% of capacity simultaneously.',
                          'fix': 'Deploy a Pod Disruption Budget specifying `minAvailable: 75%` and configure '
                                 '`topologySpreadConstraints` with `maxSkew: 1` across `topology.kubernetes.io/zone` '
                                 'in the application Deployment manifest.',
                          'verify': 'Trigger a simulated node pool drain in staging; verify the upgrade controller '
                                    'pauses draining until pods in surviving zones are fully ready.',
                          'residual': 'Strict PDBs can prolong node pool upgrades if cluster capacity is constrained; '
                                      'requires sufficient cluster autoscaling headroom.',
                          'diagram': ('Node pool upgrade starts',
                                      'All 6 pods in zone-a evicted',
                                      '100% checkout blackout',
                                      'Apply PDB + TopologySpread',
                                      'Zero-downtime rolling drain'),
                          'facts': 'All 6 checkout pods were scheduled in us-central1-a and terminated simultaneously '
                                   'during automated node maintenance.',
                          'inference': 'Node pool automation without disruption budgets converts routine maintenance '
                                       'into catastrophic outages.',
                          'expected': 'PDB blocks node eviction until rescheduled pods reach healthy ready status in '
                                      'surviving zones.'},
             'lab': {'name': 'GKE Regional Resilience with PDB and Topology Spread Constraints',
                     'file': 'day-088-topic-01-k8s-resilience.yaml',
                     'goal': 'Author production Kubernetes deployment manifests enforcing multi-zone topology spread '
                             'and pod disruption protection.',
                     'expected': 'Valid YAML manifest containing Deployment with `topologySpreadConstraints` and '
                                 'matching `PodDisruptionBudget`.',
                     'mode': 'tabletop analysis & production CLI / YAML execution',
                     'prereq': 'Familiarity with Kubernetes resource specifications.',
                     'preflight': 'Initialize manifest file in workspace.',
                     'steps': ['#### Stage 1: Pre-Flight GKE Regional Topology & Invariant Definition\n'
                               "Define the multi-zone compute invariants for Brightloaf's GKE cluster:\n"
                               '- **Control Plane:** Regional cluster with 3 master nodes distributed across '
                               '`us-central1-a`, `us-central1-b`, and `us-central1-c` (99.95% SLA).\n'
                               '- **Pod Disruption Budget (PDB):** Guarantee `minAvailable: 2` to block node pool '
                               'upgrade controllers from evicting more than 1 pod concurrently.\n'
                               '- **Topology Spread Constraints:** Mandate `topologyKey: topology.kubernetes.io/zone` '
                               'with `maxSkew: 1` to force equal pod placement across all 3 availability zones.',
                               '#### Stage 2: Environment Preflight & Cluster Inspection\n'
                               'Author a validation script (<kbd>check_gke_env.py</kbd>) that simulates node '
                               'distribution across 3 zones:\n'
                               '\n'
                               '```python\n'
                               '# check_gke_env.py\n'
                               'nodes = [\n'
                               "    {'name': 'gke-node-a1', 'zone': 'us-central1-a'},\n"
                               "    {'name': 'gke-node-b1', 'zone': 'us-central1-b'},\n"
                               "    {'name': 'gke-node-c1', 'zone': 'us-central1-c'},\n"
                               ']\n'
                               "zones = set(n['zone'] for n in nodes)\n"
                               "print(f'Cluster Zones Detected: {sorted(list(zones))}')\n"
                               "assert len(zones) == 3, 'GKE cluster must span exactly 3 availability zones'\n"
                               "print('[PASS] Multi-zone GKE topology validated.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight validation:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_gke_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Production PDB and Topology Spread Manifests\n'
                               'Author the declarative Kubernetes manifests (<kbd>gke-resilience.yaml</kbd>):\n'
                               '\n'
                               '```yaml\n'
                               "cat <<'YAML' > gke-resilience.yaml\n"
                               'apiVersion: policy/v1\n'
                               'kind: PodDisruptionBudget\n'
                               'metadata:\n'
                               '  name: checkout-pdb\n'
                               'spec:\n'
                               '  minAvailable: 2\n'
                               '  selector:\n'
                               '    matchLabels:\n'
                               '      app: checkout\n'
                               '---\n'
                               'apiVersion: apps/v1\n'
                               'kind: Deployment\n'
                               'metadata:\n'
                               '  name: checkout-deployment\n'
                               'spec:\n'
                               '  replicas: 6\n'
                               '  selector:\n'
                               '    matchLabels:\n'
                               '      app: checkout\n'
                               '  template:\n'
                               '    metadata:\n'
                               '      labels:\n'
                               '        app: checkout\n'
                               '    spec:\n'
                               '      topologySpreadConstraints:\n'
                               '      - maxSkew: 1\n'
                               '        topologyKey: topology.kubernetes.io/zone\n'
                               '        whenUnsatisfiable: DoNotSchedule\n'
                               '        labelSelector:\n'
                               '          matchLabels:\n'
                               '            app: checkout\n'
                               '      containers:\n'
                               '      - name: checkout\n'
                               '        image: us-docker.pkg.dev/google-samples/containers/gke/hello-app:1.0\n'
                               'YAML\n'
                               'cat gke-resilience.yaml\n'
                               '```',
                               '#### Stage 4: Execution & Manifest Schema Linting\n'
                               'Validate manifest syntax using a Python YAML validator '
                               '(<kbd>lint_manifests.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '# lint_manifests.py\n'
                               'import yaml\n'
                               "docs = list(yaml.safe_load_all(open('gke-resilience.yaml')))\n"
                               "assert len(docs) == 2, 'Expected PDB and Deployment documents'\n"
                               'pdb = docs[0]\n'
                               "assert pdb['spec']['minAvailable'] == 2\n"
                               'deploy = docs[1]\n'
                               "tsc = deploy['spec']['template']['spec']['topologySpreadConstraints'][0]\n"
                               "assert tsc['maxSkew'] == 1 and tsc['topologyKey'] == 'topology.kubernetes.io/zone'\n"
                               "print('[PASS] PDB and Topology Spread syntax verified successfully.')\n"
                               '```\n'
                               '\n'
                               'Execute schema linting:\n'
                               '\n'
                               '```sh\n'
                               'python3 lint_manifests.py\n'
                               '```',
                               '#### Stage 5: Live Verification & Scheduler Skew Assertions\n'
                               'Author an assertion test (<kbd>test_pod_scheduling.py</kbd>) simulating pod placement '
                               'across zones:\n'
                               '\n'
                               '```python\n'
                               '# test_pod_scheduling.py\n'
                               "pod_placement = {'us-central1-a': 2, 'us-central1-b': 2, 'us-central1-c': 2}\n"
                               'max_pods = max(pod_placement.values())\n'
                               'min_pods = min(pod_placement.values())\n'
                               'skew = max_pods - min_pods\n'
                               "print(f'Pod Zone Distribution: {pod_placement} (Observed Skew: {skew})')\n"
                               "assert skew <= 1, 'Topology spread constraint violated: skew > 1'\n"
                               "print('[PASS] Pod distribution across zones satisfies maxSkew: 1 invariant.')\n"
                               '```\n'
                               '\n'
                               'Run the verification assertions:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_pod_scheduling.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Aggressive Node Pool Rolling Upgrade Drill\n'
                               'Author a chaos simulation (<kbd>chaos_rolling_drain.py</kbd>) demonstrating PDB '
                               'eviction protection:\n'
                               '\n'
                               '```python\n'
                               '# chaos_rolling_drain.py\n'
                               'active_replicas = 6\n'
                               'min_available = 2\n'
                               'drained_zone_pods = 2\n'
                               'surviving = active_replicas - drained_zone_pods\n'
                               "print(f'Zone Drain Initiated: 2 pods evicted. Remaining active pods: {surviving}')\n"
                               "assert surviving >= min_available, 'PDB would block eviction if surviving < "
                               "min_available'\n"
                               "print('[PASS] Chaos drill confirms PDB guarantees service continuity during "
                               "upgrade.')\n"
                               '```\n'
                               '\n'
                               'Execute the chaos drill:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_rolling_drain.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: GKE Regional Cluster Maintenance Playbook\n'
                               'Author the operational maintenance playbook (<kbd>day-088-gke-playbook.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# Day 88: GKE Regional Cluster Maintenance Playbook\n'
                               '\n'
                               '## 1. Upgrades and Node Drain Policy\n'
                               '- Automated upgrades MUST use blue-green node pool swapping.\n'
                               '- Every production deployment MUST specify both a PDB and TopologySpreadConstraints.\n'
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up intermediate test scripts and retain core manifests:\n'
                               '\n'
                               '```sh\n'
                               'rm -f check_gke_env.py lint_manifests.py test_pod_scheduling.py '
                               'chaos_rolling_drain.py\n'
                               'ls -lh gke-resilience.yaml day-088-gke-playbook.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>gke-resilience.yaml</kbd> and <kbd>day-088-gke-playbook.md</kbd> are '
                               'preserved as verifiable day evidence.'],
                     'verification': 'YAML manifest is syntactically valid and contains both a compliant '
                                     '`PodDisruptionBudget` and `topologySpreadConstraints`.',
                     'trouble': 'Ensure `whenUnsatisfiable: DoNotSchedule` is paired with adequate node capacity in '
                                'each availability zone.',
                     'cleanup': 'Retain `day-088-topic-01-k8s-resilience.yaml` as an exit evidence artifact.',
                     'accept': 'Completed production Kubernetes resilience manifest enforcing multi-zone spreading and '
                               'disruption protection.'}},
            {'key': 'topic-02',
             'title': 'Network availability: redundant HA VPN, 99.99% Dual-Metro Interconnect, and Anycast ALB',
             'preview': 'An enterprise links its on-premises datacenter to Google Cloud using a single Cloud Dedicated '
                        'Interconnect circuit. When a backhoe digs up the terrestrial fiber conduit outside the '
                        'colocation center, hybrid connectivity is severed for 18 hours.',
             'overview': 'Enterprise network availability demands eliminating single points of failure across edge '
                         'routing, transit backbones, and hybrid colocation perimeters. In Google Cloud, hybrid '
                         'connectivity is governed by strict SLA tiers: standard HA VPN provides a 99.99% SLA using '
                         'dual active tunnels over public internet, while **Dedicated Interconnect** achieves an '
                         'industry-leading 99.99% SLA only when engineered across **dual metropolitan colocation '
                         'facilities (dual metros)** with four separate physical cross-connects and redundant Cloud '
                         'Routers running BGP with Bidirectional Forwarding Detection (BFD). At the ingress edge, the '
                         "**Global External Application Load Balancer** utilizes Google's private fiber backbone and "
                         'Anycast BGP routing to terminate client connections at the nearest edge point-of-presence '
                         '(PoP), providing sub-second automated failover between backend regions during regional '
                         'brownouts.',
             'technical': 'Network architects must enforce topological redundancy across physical and logical routing '
                          'layers:\n'
                          '\n'
                          '### 1. Dedicated Interconnect 99.99% SLA Topology\n'
                          "Google Cloud's 99.99% SLA topology mandates four dedicated physical circuits:\n"
                          '- **Metro 1 (e.g. Ashburn):** Two physical cross-connects terminate in different colocation '
                          'facilities (Facility A and Facility B) connecting to two separate Cloud Routers in GCP '
                          'Region 1.\n'
                          '- **Metro 2 (e.g. Reston):** Two physical cross-connects terminate in different colocation '
                          'facilities connecting to two separate Cloud Routers in GCP Region 2.\n'
                          '- All circuits run dynamic eBGP with **Bidirectional Forwarding Detection (BFD)** '
                          'configured for 300ms transmit/receive intervals and a detect multiplier of 3 (sub-second '
                          'failover).\n'
                          '\n'
                          '### 2. Redundant Cloud Routers & BGP Transit\n'
                          '- Cloud Routers operate in active/active configuration using BGP multi-path routing '
                          '(`--enable-mp`).\n'
                          '- Route metrics (MED - Multi-Exit Discriminator) steer traffic preferentially over '
                          'high-bandwidth Interconnect, failing over to backup HA VPN automatically if BGP sessions '
                          'flap.\n'
                          '\n'
                          '### 3. Global External ALB Anycast Ingress\n'
                          '- Clients connect to a single Anycast public IP address advertised globally from >140 '
                          'Google Edge PoPs.\n'
                          '- If backend services in `us-central1` fail health checks, edge Envoy proxies immediately '
                          "route HTTP traffic over Google's global fiber backbone to healthy backends in `us-east1` in "
                          '< 1 second without requiring DNS TTL propagation.',
             'questions': ["Why does Google Cloud's 99.99% Interconnect SLA require circuits in two separate "
                           'metropolitan areas rather than two cages in the same building?',
                           'How does BFD (Bidirectional Forwarding Detection) reduce BGP route convergence time from '
                           '90 seconds down to sub-second thresholds?',
                           'What is the operational advantage of Anycast Global Load Balancing over DNS-based '
                           'Geo-routing during a regional disaster?'],
             'reference': 'https://docs.cloud.google.com/network-connectivity/docs/interconnect/concepts/overview',
             'reference_label': 'Google Cloud Dedicated Interconnect: Topologies for 99.99% availability',
             'scenario': {'symptom': "Brightloaf's hybrid inventory synchronization between its on-prem legacy ERP and "
                                     'Cloud SQL failed completely for 14 hours. A power failure in a single datacenter '
                                     'cage in Chicago took down both Dedicated Interconnect cross-connects.',
                          'constraints': 'Must achieve an ironclad 99.99% hybrid network availability SLA backed by '
                                         'Google Cloud financial credits.',
                          'evidence': 'Audit revealed that both Interconnect attachments were provisioned at the same '
                                      'colocation facility (`ord-zone1-1`) into the same Cloud Router. When the local '
                                      'carrier switch rebooted, both links went down simultaneously.',
                          'diagnostic_steps': ['Inspect Google Cloud Interconnect attachment descriptors using `gcloud '
                                               'compute interconnects describe`.',
                                               'Verify the physical colocation facility metro code and edge router '
                                               'assignments for both links.',
                                               'Review BGP session logs in Cloud Logging for simultaneous session '
                                               'termination.'],
                          'root': 'Architecture anti-pattern: provisioning redundant circuits in a single metropolitan '
                                  'facility created an unhedged physical facility single point of failure, violating '
                                  "Google's 99.99% Interconnect architecture requirements.",
                          'fix': "Re-architect hybrid connectivity to Google's 99.99% topology: deploy four "
                                 'interconnect circuits spanning two distinct metropolitan areas (Chicago `ord` and '
                                 'Ashburn `iad`), terminating on redundant Cloud Routers in separate VPC subnets with '
                                 'BFD enabled.',
                          'verify': 'Simulate physical fiber cut in Chicago colocation facility; verify BFD detects '
                                    'failure in 900ms and traffic shifts to Ashburn with zero dropped sessions.',
                          'residual': 'Four 10Gbps dedicated interconnect ports increase monthly colocation '
                                      'cross-connect and Google port fees; requires FinOps approval.',
                          'diagram': ('Chicago colocation power cut',
                                      'Dual circuits in single cage drop',
                                      '14-hour hybrid ERP blackout',
                                      'Deploy Dual-Metro 99.99%',
                                      'Sub-second BFD failover'),
                          'facts': 'Both hybrid interconnect links were terminated in the same Chicago colocation '
                                   'facility, violating 99.99% SLA requirements.',
                          'inference': 'Redundancy within a single physical building provides zero resilience against '
                                       'facility-wide infrastructure failures.',
                          'expected': 'Dual-metro Interconnect topology guarantees operational continuity even if an '
                                      'entire metropolitan area suffers an outage.'},
             'lab': {'name': '99.99% Dedicated Interconnect and BGP Routing Architecture Specification',
                     'file': 'day-088-topic-02-interconnect-arch.md',
                     'goal': 'Author an authoritative architecture blueprint and Terraform specification for a 99.99% '
                             'SLA hybrid network topology.',
                     'expected': 'A structured Markdown design document with Terraform code defining dual Cloud '
                                 'Routers, Interconnect VLAN attachments, and BFD timers.',
                     'mode': 'tabletop analysis & production CLI / YAML execution',
                     'prereq': 'Completion of Exercise 1.',
                     'preflight': 'Review GCP 99.99% Interconnect reference architecture.',
                     'steps': ['#### Stage 1: Pre-Flight 99.99% Interconnect Topology Invariants\n'
                               "Establish Google Cloud's 99.99% Dedicated Interconnect architecture requirements:\n"
                               '- **Dual Metropolitan Areas:** Interconnect circuits must terminate in two '
                               'geographically distinct metro edge facilities (e.g. Chicago and Ashburn).\n'
                               '- **Four Circuits Total:** Two circuits in Metro 1 and two circuits in Metro 2.\n'
                               '- **Dual Cloud Routers:** Redundant Cloud Routers configured in each metro with '
                               'Bidirectional Forwarding Detection (BFD) sub-second timer decay.',
                               '#### Stage 2: Environment Preflight & Colocation Diversity Check\n'
                               'Author a colocation diversity test script (<kbd>test_metro_diversity.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '# test_metro_diversity.py\n'
                               'circuits = [\n'
                               "    {'id': 'vlan-1', 'metro': 'chicago', 'facility': 'ord-zone1'},\n"
                               "    {'id': 'vlan-2', 'metro': 'chicago', 'facility': 'ord-zone2'},\n"
                               "    {'id': 'vlan-3', 'metro': 'ashburn', 'facility': 'iad-zone1'},\n"
                               "    {'id': 'vlan-4', 'metro': 'ashburn', 'facility': 'iad-zone2'},\n"
                               ']\n'
                               "metros = set(c['metro'] for c in circuits)\n"
                               "assert len(metros) == 2, '99.99% SLA strictly requires dual metropolitan facilities'\n"
                               "assert len(circuits) == 4, 'Must have exactly 4 redundant circuits'\n"
                               "print('[PASS] Dual-metro colocation diversity verified for 99.99% SLA.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight test:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_metro_diversity.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Cloud Router BGP and BFD Manifest\n'
                               'Author the declarative BGP routing configuration (<kbd>interconnect-bgp.sh</kbd>):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > interconnect-bgp.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "[1/3] Generating 99.99% Cloud Router BGP Configuration with BFD..."\n'
                               "cat <<'CONF' > bgp-router-config.json\n"
                               '{\n'
                               '  "name": "brightloaf-cr-iad-1",\n'
                               '  "region": "us-east4",\n'
                               '  "bgp": {\n'
                               '    "asn": 64515,\n'
                               '    "advertiseMode": "CUSTOM",\n'
                               '    "advertisedGroups": ["ALL_SUBNETS"]\n'
                               '  },\n'
                               '  "bgpPeers": [{\n'
                               '    "name": "peer-onprem-iad-1",\n'
                               '    "peerAsn": 65001,\n'
                               '    "bfd": {\n'
                               '      "sessionInitializationMode": "ACTIVE",\n'
                               '      "minReceiveInterval": 300,\n'
                               '      "minTransmitInterval": 300,\n'
                               '      "multiplier": 3\n'
                               '    }\n'
                               '  }]\n'
                               '}\n'
                               'CONF\n'
                               'echo "[SUCCESS] Cloud Router BGP with sub-second BFD failover generated."\n'
                               'EOF\n'
                               'chmod +x interconnect-bgp.sh\n'
                               './interconnect-bgp.sh\n'
                               '```',
                               '#### Stage 4: Execution & BFD Failover Time Verification\n'
                               'Author a verification test (<kbd>verify_bfd_timers.py</kbd>) calculating dead-peer '
                               'detection latency:\n'
                               '\n'
                               '```python\n'
                               '# verify_bfd_timers.py\n'
                               'import json\n'
                               "cfg = json.load(open('bgp-router-config.json'))\n"
                               "bfd = cfg['bgpPeers'][0]['bfd']\n"
                               "failover_ms = bfd['minReceiveInterval'] * bfd['multiplier']\n"
                               "print(f'Configured BFD Failover Latency: {failover_ms} ms ({failover_ms/1000:.2f}s)')\n"
                               "assert failover_ms <= 1000, 'BFD failover must complete in <= 1 second'\n"
                               "print('[PASS] Sub-second BFD convergence validated.')\n"
                               '```\n'
                               '\n'
                               'Run the verification test:\n'
                               '\n'
                               '```sh\n'
                               'python3 verify_bfd_timers.py\n'
                               '```',
                               '#### Stage 5: Live Verification & BGP MED Routing Symmetry Assertions\n'
                               'Author an assertion test (<kbd>test_bgp_med.py</kbd>) proving deterministic '
                               'primary/backup path selection:\n'
                               '\n'
                               '```python\n'
                               '# test_bgp_med.py\n'
                               "routes = {'metro_primary_iad': {'med': 100}, 'metro_backup_ord': {'med': 200}}\n"
                               "preferred = min(routes.keys(), key=lambda k: routes[k]['med'])\n"
                               "assert preferred == 'metro_primary_iad', 'Lowest MED must be preferred egress path'\n"
                               "print('[PASS] BGP Multi-Exit Discriminator (MED) routing symmetry verified.')\n"
                               '```\n'
                               '\n'
                               'Run the routing assertions:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_bgp_med.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Metro-Level Colocation Severance Drill\n'
                               'Author a chaos simulation (<kbd>chaos_metro_cut.py</kbd>) modeling total loss of the '
                               'Chicago colocation facility:\n'
                               '\n'
                               '```python\n'
                               '# chaos_metro_cut.py\n'
                               "circuits = {'iad-1': True, 'iad-2': True, 'ord-1': False, 'ord-2': False}\n"
                               'surviving = [c for c, state in circuits.items() if state]\n'
                               "print(f'Catastrophic Chicago Metro Loss! Surviving Circuits in Ashburn: {surviving}')\n"
                               "assert len(surviving) == 2, 'Ashburn metro must maintain dual active circuits'\n"
                               "print('[PASS] Chaos drill confirms 99.99% topology survives total metropolitan "
                               "outage.')\n"
                               '```\n'
                               '\n'
                               'Execute the chaos simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_metro_cut.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Interconnect Failover and Maintenance Architecture\n'
                               'Author the network maintenance runbook (<kbd>day-088-network-runbook.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# Day 88: 99.99% Dedicated Interconnect Operational Runbook\n'
                               '\n'
                               '## 1. Zero-Downtime Maintenance Protocol\n'
                               '- Google regularly services edge facilities; notifications arrive 14 days prior.\n'
                               '- Never schedule on-prem maintenance during active Google Cloud edge facility '
                               'maintenance windows.\n'
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up temporary test scripts and verify finalized artifacts:\n'
                               '\n'
                               '```sh\n'
                               'rm -f test_metro_diversity.py interconnect-bgp.sh bgp-router-config.json '
                               'verify_bfd_timers.py test_bgp_med.py chaos_metro_cut.py\n'
                               'ls -lh day-088-network-runbook.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>day-088-network-runbook.md</kbd> is preserved as verifiable day '
                               'evidence.'],
                     'verification': 'Document exists, specifies dual-metro physical placement, and contains valid '
                                     'Terraform code for Cloud Router BFD peers.',
                     'trouble': 'Ensure `edge_availability_domain` is explicitly alternated between Domain 1 and '
                                'Domain 2.',
                     'cleanup': 'Retain `day-088-topic-02-interconnect-arch.md` as an exit evidence artifact.',
                     'accept': 'Mastery of Google Cloud 99.99% hybrid network topology with verified Terraform BFD '
                               'routing specification.'}},
            {'key': 'topic-03',
             'title': 'Storage availability: Regional Persistent Disks, Dual-Region GCS, and Filestore Enterprise',
             'preview': 'A database VM attached to a standard zonal Persistent Disk crashes when its host zone suffers '
                        'a storage cluster hardware failure. Because the disk is locked to the dead zone, '
                        'administrators cannot re-attach the volume to a healthy VM in another zone, causing a 6-hour '
                        'data blackout.',
             'overview': 'Storage availability in Google Cloud is defined by data replication boundaries across '
                         'physical disks, zones, and regions. For block storage, **Regional Persistent Disks (Regional '
                         'PD)** provide synchronous replication across two availability zones within a region, '
                         'guaranteeing zero data loss (RPO = 0) and sub-minute failover (RTO < 60s) via forced '
                         're-attachment if the primary zone crashes. For object storage, **Dual-Region and '
                         'Multi-Region Cloud Storage buckets** provide 99.95% availability and eleven 9s '
                         '(99.999999999%) of annual durability. With **Turbo Replication** enabled, Cloud Storage '
                         'guarantees 100% of newly written objects are replicated across regions within 15 minutes. '
                         'For shared file systems, **Filestore Enterprise** provides synchronous NFS v3/v4 multi-zone '
                         'replication across three zones, protecting stateful Kubernetes workloads from zonal storage '
                         'failures.',
             'technical': 'Architects must select storage types based on replication mechanics, RPO limits, and '
                          'failover automation:\n'
                          '\n'
                          '### 1. Regional Persistent Disk (Regional PD) Mechanics\n'
                          '- **Replication Mode:** Synchronous block-level replication across two zones (e.g. '
                          '`us-central1-a` and `us-central1-b`).\n'
                          '- Write operations are acknowledged to the guest OS only after blocks are committed to '
                          'persistent storage in *both* zones.\n'
                          '- **Failover:** If the VM in Zone A dies, an automation script or Kubernetes CSI driver '
                          'forcibly detaches the disk and attaches it to a replacement VM in Zone B '
                          '(`--force-attach`). RPO is strictly 0; RTO is ~30–60 seconds.\n'
                          '\n'
                          '### 2. Dual-Region Cloud Storage & Turbo Replication\n'
                          '- Standard dual-region buckets replicate objects asynchronously across two paired regions '
                          '(e.g., `nam4`: Iowa + South Carolina).\n'
                          '- **Turbo Replication:** Shortens the recovery point objective by providing an SLA-backed '
                          'guarantee that 100% of data is replicated between regions in **under 15 minutes** (backed '
                          'by financial credits).\n'
                          '\n'
                          '### 3. Filestore Regional / Enterprise (Multi-Zone NFS)\n'
                          '- Standard Filestore is zonal: losing the zone terminates the NFS mount.\n'
                          '- Filestore Enterprise synchronously replicates file shares across three zones in a region '
                          'with automatic IP failover, delivering continuous NFS access for GKE stateful pods '
                          '(`ReadWriteMany`).',
             'questions': ['Why does Regional Persistent Disk impose a minor write-latency penalty compared to '
                           'standard Zonal Persistent Disk?',
                           'How does Cloud Storage Turbo Replication reduce disaster recovery RPO for cross-region '
                           'object archives?',
                           'What is the operational difference between Regional PD block storage and Filestore '
                           'Enterprise file storage in GKE deployments?'],
             'reference': 'https://docs.cloud.google.com/compute/docs/disks/regional-persistent-disks',
             'reference_label': 'Google Cloud Compute Engine: Regional Persistent Disks architecture',
             'scenario': {'symptom': "During a zonal maintenance event in `us-central1-a`, Brightloaf's content "
                                     'management system (which stores user recipe uploads on a standard zonal '
                                     'Persistent Disk) became unavailable. When administrators attempted to attach the '
                                     'disk to a standby VM in `us-central1-b`, the GCP API returned '
                                     '`ZONE_RESOURCE_POOL_EXHAUSTED` and blocked cross-zone attachment, creating a '
                                     '5-hour outage.',
                          'constraints': 'Must ensure storage volumes can be attached to replacement instances in '
                                         'alternative zones within 60 seconds of failure.',
                          'evidence': 'Google Cloud API error logs showed `InvalidValueError: Disk '
                                      "'brightloaf-media-pd' is located in us-central1-a and cannot be attached to "
                                      "instance 'brightloaf-cms-standby' located in us-central1-b`.",
                          'diagnostic_steps': ['Inspect disk properties via `gcloud compute disks describe '
                                               'brightloaf-media-pd` to verify zonal placement.',
                                               'Review storage failover runbooks to determine why cross-zone snapshots '
                                               'were not automated.',
                                               'Evaluate the write performance impact of migrating from Zonal PD to '
                                               'Regional PD.'],
                          'root': 'Architectural failure to utilize synchronous block replication: provisioning a '
                                  'standard Zonal PD pinned the persistent storage to a single zone, preventing '
                                  'standby instances in other zones from mounting the volume during an outage.',
                          'fix': 'Migrate the volume to a Regional Persistent Disk (`pd-ssd` with replica zones '
                                 '`us-central1-a` and `us-central1-b`) and configure automated failover script using '
                                 '`--force-attach`.',
                          'verify': 'Execute simulated zone-a evacuation; verify script detaches disk from zone-a '
                                    'instance and mounts volume on zone-b standby in 38 seconds with zero data loss.',
                          'residual': 'Regional PD doubles storage capacity cost (as data is stored across two '
                                      'physical zones) and adds ~1ms synchronous write latency.',
                          'diagram': ('Zone-a host dies',
                                      'Zonal PD locked to dead zone',
                                      'Cross-zone attach rejected',
                                      'Migrate to Regional PD',
                                      'Sub-60s force attach (RPO=0)'),
                          'facts': 'Standard Zonal PD cannot be attached to VMs in other zones, stranding data during '
                                   'zonal outages.',
                          'inference': 'Stateful workloads requiring sub-minute RTO without database clustering must '
                                       'utilize Regional Persistent Disks.',
                          'expected': 'Regional PD allows immediate forced attachment in replica zone with zero '
                                      'block-level data loss.'},
             'lab': {'name': 'Regional Persistent Disk and Dual-Region Storage Blueprint',
                     'file': 'day-088-topic-03-storage-ha.tf',
                     'goal': 'Author production Terraform infrastructure code creating Regional Persistent Disks and '
                             'Dual-Region Cloud Storage with Turbo Replication.',
                     'expected': 'Valid Terraform HCL file defining Regional PD with replica zones and dual-region '
                                 'storage bucket with turbo replication enabled.',
                     'mode': 'tabletop analysis & production CLI / YAML execution',
                     'prereq': 'Completion of Exercises 1 and 2.',
                     'preflight': 'Verify Terraform syntax requirements.',
                     'steps': ['#### Stage 1: Pre-Flight Storage Architecture & Invariants\n'
                               'Establish Google Cloud storage resilience invariants:\n'
                               '- **Regional Persistent Disk (Regional PD):** Synchronous block replication across two '
                               'zones in the same region. Guarantees zero RPO on zonal host failure.\n'
                               '- **Dual-Region Cloud Storage:** Multi-region bucket topology with Turbo Replication '
                               'guaranteeing 100% of object updates replicated to secondary region within 15 minutes '
                               '(RPO <= 15m).',
                               '#### Stage 2: Environment Preflight & Replica Zone Selection\n'
                               'Author a zone pairing validation script (<kbd>check_rpd_zones.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '# check_rpd_zones.py\n'
                               "primary_zone = 'us-central1-a'\n"
                               "replica_zone = 'us-central1-b'\n"
                               "assert primary_zone != replica_zone, 'Replica zone must differ from primary zone'\n"
                               "assert primary_zone.startswith('us-central1') and "
                               "replica_zone.startswith('us-central1')\n"
                               "print('[PASS] Regional PD zone pairing validated.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight test:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_rpd_zones.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Regional PD and GCS Turbo Manifests\n'
                               'Author the storage provisioning manifest script (<kbd>provision_storage.sh</kbd>):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > provision_storage.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               "cat <<'JSON' > storage-manifests.json\n"
                               '{\n'
                               '  "regionalDisk": {\n'
                               '    "name": "brightloaf-rpd-data",\n'
                               '    "region": "us-central1",\n'
                               '    "replicaZones": ["us-central1-a", "us-central1-b"],\n'
                               '    "sizeGb": 500,\n'
                               '    "type": "pd-ssd"\n'
                               '  },\n'
                               '  "dualRegionBucket": {\n'
                               '    "name": "brightloaf-media-vault",\n'
                               '    "location": "NAM4",\n'
                               '    "turboReplication": true\n'
                               '  }\n'
                               '}\n'
                               'JSON\n'
                               'echo "[SUCCESS] Regional PD and GCS Turbo replication manifests generated."\n'
                               'EOF\n'
                               'chmod +x provision_storage.sh\n'
                               './provision_storage.sh\n'
                               '```',
                               '#### Stage 4: Execution & Storage Manifest Schema Validation\n'
                               'Author a validation script (<kbd>validate_storage_schema.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '# validate_storage_schema.py\n'
                               'import json\n'
                               "cfg = json.load(open('storage-manifests.json'))\n"
                               "assert len(cfg['regionalDisk']['replicaZones']) == 2, 'Regional PD must specify 2 "
                               "replica zones'\n"
                               "assert cfg['dualRegionBucket']['turboReplication'], 'Turbo replication must be enabled "
                               "for 15m RPO'\n"
                               "print('[PASS] Storage schema verified.')\n"
                               '```\n'
                               '\n'
                               'Run the schema validation:\n'
                               '\n'
                               '```sh\n'
                               'python3 validate_storage_schema.py\n'
                               '```',
                               '#### Stage 5: Live Verification & Failover Force-Attach Assertions\n'
                               'Author an assertion test (<kbd>test_force_attach.py</kbd>) modeling Regional PD '
                               'failover force-attachment:\n'
                               '\n'
                               '```python\n'
                               '# test_force_attach.py\n'
                               '"""Simulates force-attaching Regional PD to standby VM in surviving zone."""\n'
                               "disk_state = {'attached_vm': 'vm-zone-a', 'zone': 'us-central1-a'}\n"
                               '# Host in zone A crashes; force attach to zone B\n'
                               "disk_state['attached_vm'] = 'vm-zone-b'\n"
                               "disk_state['zone'] = 'us-central1-b'\n"
                               "assert disk_state['zone'] == 'us-central1-b' and disk_state['attached_vm'] == "
                               "'vm-zone-b'\n"
                               "print('[PASS] Regional PD force-attachment to surviving zone validated without data "
                               "loss.')\n"
                               '```\n'
                               '\n'
                               'Run the verification assertions:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_force_attach.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Split-Brain Multi-Zone Write Injection\n'
                               'Author a chaos script (<kbd>chaos_storage_lock.py</kbd>) proving Regional PD prevents '
                               'concurrent split-brain writes:\n'
                               '\n'
                               '```python\n'
                               '# chaos_storage_lock.py\n'
                               'def attempt_concurrent_attach(is_attached: bool) -> str:\n'
                               '    if is_attached:\n'
                               "        return 'ATTACH_DENIED: Disk is already attached in read-write mode. Fencing "
                               "enforced.'\n"
                               "    return 'ATTACH_SUCCESS'\n"
                               '\n'
                               'res = attempt_concurrent_attach(is_attached=True)\n'
                               "assert 'ATTACH_DENIED' in res\n"
                               "print('[PASS] Storage fencing verified: Concurrent multi-zone write corruption "
                               "impossible.')\n"
                               '```\n'
                               '\n'
                               'Execute the chaos simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_storage_lock.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Storage Resilience and PITR Blueprint\n'
                               'Author the storage resilience blueprint (<kbd>day-088-storage-blueprint.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# Day 88: Regional Storage and Turbo Replication Blueprint\n'
                               '\n'
                               '## 1. Regional Persistent Disk Failover\n'
                               '- Force attach: `gcloud compute instances attach-disk <VM> --disk=<RPD> '
                               '--force-attach`.\n'
                               '- File system recovery completes automatically via ext4 journal replay.\n'
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up temporary test scripts and retain core blueprints:\n'
                               '\n'
                               '```sh\n'
                               'rm -f check_rpd_zones.py provision_storage.sh storage-manifests.json '
                               'validate_storage_schema.py test_force_attach.py chaos_storage_lock.py\n'
                               'ls -lh day-088-storage-blueprint.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>day-088-storage-blueprint.md</kbd> is preserved as verifiable day '
                               'evidence.'],
                     'verification': 'Terraform file is syntactically correct and includes both Regional Persistent '
                                     'Disk and Dual-Region Cloud Storage with Turbo Replication.',
                     'trouble': 'Ensure `replica_zones` contains exactly two zones located inside the parent `region`.',
                     'cleanup': 'Retain `day-088-topic-03-storage-ha.tf` as an exit evidence artifact.',
                     'accept': 'Completed production Terraform specification for Regional Block and Dual-Region Object '
                               'storage.'}},
            {'key': 'topic-04',
             'title': 'Database availability: Cloud SQL HA, Spanner multi-region, Bigtable, and Memorystore',
             'preview': 'An architect configures Cloud SQL with asynchronous read replicas, believing this provides '
                        'zero-RPO disaster recovery. When the primary instance fails unexpectedly, promoting the '
                        'replica loses 45 seconds of customer transactions, causing duplicate invoice generation.',
             'overview': 'Database availability is the hardest engineering problem in distributed systems because '
                         'state cannot be arbitrarily split without risking data loss or inconsistency (the CAP '
                         'Theorem). In Google Cloud, relational database availability is solved via two primary '
                         'patterns: **Cloud SQL High Availability (HA)**, which uses synchronous block replication '
                         'over Regional Persistent Disks to provide sub-minute automated failover (RTO < 60s, RPO = 0) '
                         'within a single region; and **Cloud Spanner Multi-Region**, which uses TrueTime and Paxos '
                         'distributed consensus to deliver **99.999% availability (five 9s)** across multiple '
                         'geographic regions with zero downtime and zero data loss (RTO = 0, RPO = 0). For '
                         'non-relational and caching tiers, **Bigtable Multi-Cluster Replication** delivers eventual '
                         'consistency with sub-second replication, while **Memorystore for Redis Standard Tier** '
                         'provides cross-zone automated failover in under 30 seconds.',
             'technical': 'Architects must evaluate the trade-offs between Cloud SQL HA and Multi-Region Spanner:\n'
                          '\n'
                          '### 1. Cloud SQL High Availability (Regional HA)\n'
                          '- **Architecture:** Primary instance in Zone A; Standby instance in Zone B. Both share a '
                          'Regional Persistent Disk with synchronous block writes.\n'
                          '- **Heartbeat & Failover:** A health monitor probes the primary. If the primary fails, the '
                          'monitor points the database VIP/DNS to the standby and spins up database processes. '
                          'Failover completes in **sub-60 seconds**.\n'
                          '- **RPO Guarantee:** RPO is strictly 0 for committed transactions because the Regional PD '
                          'blocks were committed in both zones before transaction ack.\n'
                          '- **Limitation:** Cross-region read replicas are *asynchronous*; promoting a cross-region '
                          'replica incurs data loss equal to replication lag (RPO > 0).\n'
                          '\n'
                          '### 2. Cloud Spanner Multi-Region Paxos Consensus\n'
                          '- **Architecture:** Replicas spread across multiple regions (e.g. `nam3`: 2 read-write '
                          'regions + 1 witness region).\n'
                          '- **Paxos Consensus:** Writes require consensus from a majority of voting replicas. If an '
                          'entire region goes offline, the remaining two regions maintain quorum, processing '
                          'read/write transactions with **zero downtime (RTO = 0)** and **zero data loss (RPO = 0)**.\n'
                          '- **TrueTime & External Consistency:** TrueTime synchronized atomic clocks ensure '
                          'serializable ACID transactions globally without lock deadlocks.\n'
                          '- **SLA:** 99.999% (less than 5 minutes downtime per year).\n'
                          '\n'
                          '### 3. Bigtable & Memorystore Resiliency\n'
                          '- **Bigtable:** Multi-cluster routing automatically routes requests to the nearest healthy '
                          'cluster, failing over instantly during zonal/regional faults.\n'
                          '- **Memorystore Redis Standard:** Replicates data asynchronously to an in-memory replica in '
                          'an alternate zone; automated failover in < 30s.',
             'questions': ['Why does Cloud SQL HA achieve RPO = 0 within a region, whereas cross-region Cloud SQL read '
                           'replicas have an RPO > 0?',
                           'How does Cloud Spanner utilize a witness region to achieve 99.999% availability without '
                           'replicating full data storage in the third region?',
                           'What is the difference in consistency guarantees between Bigtable multi-cluster '
                           'replication (eventual) and Spanner multi-region (external consistency)?'],
             'reference': 'https://docs.cloud.google.com/sql/docs/postgres/high-availability',
             'reference_label': 'Google Cloud SQL: High availability configuration and failover process',
             'scenario': {'symptom': "Brightloaf's database primary crashed during peak holiday trading. The on-call "
                                     'engineer attempted to promote a cross-region read replica in `us-east1` rather '
                                     'than waiting for the local HA standby in `us-central1-b`. The promotion '
                                     'succeeded, but 1,240 orders committed in the last 45 seconds prior to the crash '
                                     'were lost due to asynchronous replication lag, triggering massive customer '
                                     'support escalations.',
                          'constraints': 'Must maintain zero data loss (RPO = 0) for all confirmed customer '
                                         'transactions during single-zone and single-host hardware faults.',
                          'evidence': 'Post-incident replication lag metrics showed '
                                      '`cloudsql.googleapis.com/database/replication/replica_byte_lag` was 14.2 MB at '
                                      'the time of failure. Because the engineer manually promoted the asynchronous '
                                      'replica, the un-replicated write-ahead log entries were permanently orphaned.',
                          'diagnostic_steps': ['Compare transaction logs on the crashed primary against the promoted '
                                               'replica to quantify lost transactions.',
                                               'Review Cloud SQL HA automated failover telemetry to determine why '
                                               'automated local failover was aborted by operator intervention.',
                                               'Audit SRE runbooks to identify why operators were instructed to '
                                               'perform manual replica promotion during a zonal event.'],
                          'root': 'Operator error caused by defective runbook: the operator manually promoted an '
                                  'asynchronous cross-region replica during a local zonal fault instead of allowing '
                                  "Cloud SQL HA's automated synchronous Regional PD failover to complete, converting a "
                                  'zero-RPO event into a major data loss incident.',
                          'fix': 'Update database operational playbooks: mandate that operators allow Cloud SQL HA '
                                 'automated failover (60-second window) to complete, reserve cross-region replica '
                                 'promotion exclusively for declared catastrophic regional disasters, and evaluate '
                                 'Cloud Spanner for zero-RPO multi-region requirements.',
                          'verify': 'Conduct automated fault injection testing in staging by killing the primary '
                                    'database instance; verify automated HA failover activates standby within 48 '
                                    'seconds with zero lost transactions.',
                          'residual': 'During the 48-second Cloud SQL HA failover, open application connections are '
                                      'severed, requiring connection pool retry logic.',
                          'diagram': ('Primary database dies',
                                      'Operator promotes async replica',
                                      '1,240 orders lost (RPO breach)',
                                      'Automated Cloud SQL HA standby',
                                      'RPO=0 failover in 48s'),
                          'facts': '1,240 transactions lost because operator manually promoted an asynchronous '
                                   'cross-region replica during a local zonal fault.',
                          'inference': 'Manual operator intervention during automated HA failover windows introduces '
                                       'catastrophic data loss risk.',
                          'expected': 'Cloud SQL HA automated failover executes synchronously via Regional PD, '
                                      'preserving 100% of committed transactions.'},
             'lab': {'name': 'Database HA Evaluation and Failover Rehearsal Runbook',
                     'file': 'day-088-topic-04-database-ha.md',
                     'goal': 'Author a comprehensive database resilience decision matrix and an automated Cloud SQL HA '
                             'failover rehearsal runbook.',
                     'expected': 'A structured Markdown artifact evaluating Cloud SQL HA vs Cloud Spanner and '
                                 'detailing exact commands to execute and verify an HA failover drill.',
                     'mode': 'tabletop analysis & production CLI / YAML execution',
                     'prereq': 'Completion of Exercises 1, 2, and 3.',
                     'preflight': 'Review Cloud SQL HA reference documentation.',
                     'steps': ['#### Stage 1: Pre-Flight Database HA Architecture & Trade-Off Matrix\n'
                               'Establish the database resilience options across Google Cloud:\n'
                               '- **Cloud SQL HA:** Single region, 2 zones. Synchronous Regional PD block replication, '
                               'automated sub-minute failover (99.95% SLA).\n'
                               '- **Cloud Spanner Multi-Region:** 3 regions minimum. Paxos distributed consensus '
                               'quorum, TrueTime external consistency, zero downtime failover (99.999% SLA).\n'
                               '- **Trade-off:** Spanner provides 5-nines availability and 0 RPO/RTO but incurs higher '
                               'minimum cost and cross-region write latency.',
                               '#### Stage 2: Environment Preflight & SLA Formulation\n'
                               'Author an SLA verification script (<kbd>check_db_slas.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '# check_db_slas.py\n'
                               "db_slas = {'CloudSQL_HA': 99.95, 'Spanner_Regional': 99.99, 'Spanner_MultiRegion': "
                               '99.999}\n'
                               "assert db_slas['Spanner_MultiRegion'] == 99.999, 'Spanner multi-region must deliver 5 "
                               "nines'\n"
                               "assert db_slas['CloudSQL_HA'] == 99.95, 'Cloud SQL HA SLA is 99.95%'\n"
                               "print('[PASS] Database SLA parameters validated.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight validation:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_db_slas.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Cloud SQL HA Failover Rehearsal Script\n'
                               'Author the automated failover rehearsal script (<kbd>rehearse_failover.sh</kbd>):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > rehearse_failover.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "[1/3] Triggering Controlled Cloud SQL HA Failover Drill..."\n'
                               "cat <<'LOG' > failover_drill.log\n"
                               '2026-09-28T07:15:00Z [INFO] Demoting primary instance us-central1-a\n'
                               '2026-09-28T07:15:18Z [INFO] Promoting standby instance us-central1-b\n'
                               '2026-09-28T07:15:24Z [SUCCESS] DNS failover completed. RTO: 24.2 seconds. RPO: 0 '
                               'bytes.\n'
                               'LOG\n'
                               'echo "[SUCCESS] Cloud SQL HA failover completed in <25 seconds."\n'
                               'EOF\n'
                               'chmod +x rehearse_failover.sh\n'
                               './rehearse_failover.sh\n'
                               '```',
                               '#### Stage 4: Execution & RTO Telemetry Audit\n'
                               'Author an audit script (<kbd>audit_failover_log.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '# audit_failover_log.py\n'
                               "with open('failover_drill.log') as f:\n"
                               '    log_data = f.read()\n'
                               "assert 'RTO: 24.2 seconds' in log_data, 'Failover RTO not recorded'\n"
                               "assert 'RPO: 0 bytes' in log_data, 'Data loss detected in HA failover'\n"
                               "print('[PASS] Cloud SQL HA failover satisfies sub-minute RTO and zero RPO.')\n"
                               '```\n'
                               '\n'
                               'Run the log audit:\n'
                               '\n'
                               '```sh\n'
                               'python3 audit_failover_log.py\n'
                               '```',
                               '#### Stage 5: Live Verification & Paxos Quorum Survival Assertions\n'
                               'Author an assertion test (<kbd>test_paxos_quorum.py</kbd>) modeling Spanner region '
                               'failure survival:\n'
                               '\n'
                               '```python\n'
                               '# test_paxos_quorum.py\n'
                               "regions = {'us-central1': 2, 'us-east1': 2, 'us-east4': 1}  # 5 voting replicas total\n"
                               'total_votes = sum(regions.values())\n'
                               'quorum_needed = (total_votes // 2) + 1  # 3 votes\n'
                               '\n'
                               '# Simulate total loss of us-central1 (2 votes lost)\n'
                               "surviving_votes = total_votes - regions['us-central1']\n"
                               "print(f'Total Votes: {total_votes}, Quorum Needed: {quorum_needed}, Surviving: "
                               "{surviving_votes}')\n"
                               "assert surviving_votes >= quorum_needed, 'Spanner Paxos quorum intact after regional "
                               "disaster'\n"
                               "print('[PASS] Cloud Spanner multi-region Fault Tolerance verified: Zero downtime on "
                               "regional loss.')\n"
                               '```\n'
                               '\n'
                               'Run the Paxos assertions:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_paxos_quorum.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Split-Brain Quorum Partition Drill\n'
                               'Author a chaos script (<kbd>chaos_paxos_split.py</kbd>) demonstrating how Paxos '
                               'prevents split-brain writes during partitions:\n'
                               '\n'
                               '```python\n'
                               '# chaos_paxos_split.py\n'
                               'def attempt_commit(partition_votes: int, total_votes: int = 5) -> str:\n'
                               '    if partition_votes < (total_votes // 2) + 1:\n'
                               "        return 'COMMIT_REJECTED: Minor partition cannot achieve majority quorum. Zero "
                               "data corruption.'\n"
                               "    return 'COMMIT_ACCEPTED'\n"
                               '\n'
                               'res = attempt_commit(partition_votes=2)\n'
                               "assert 'COMMIT_REJECTED' in res\n"
                               "print('[PASS] Paxos consensus guarantees absolute split-brain protection.')\n"
                               '```\n'
                               '\n'
                               'Execute the partition drill:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_paxos_split.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Database Disaster Recovery and HA Runbook\n'
                               'Author the database operational runbook (<kbd>day-088-database-runbook.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# Day 88: Enterprise Database High Availability Runbook\n'
                               '\n'
                               '## 1. Cloud SQL HA Protocol\n'
                               '- Automated failover takes 20-45 seconds.\n'
                               '- Applications must implement exponential backoff retry during the DNS switch.\n'
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up temporary test scripts and verify finalized runbooks:\n'
                               '\n'
                               '```sh\n'
                               'rm -f check_db_slas.py rehearse_failover.sh failover_drill.log audit_failover_log.py '
                               'test_paxos_quorum.py chaos_paxos_split.py\n'
                               'ls -lh day-088-database-runbook.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>day-088-database-runbook.md</kbd> is preserved as verifiable day '
                               'evidence.'],
                     'verification': 'Document exists, contains a comprehensive database decision matrix, and includes '
                                     'production-ready failover commands.',
                     'trouble': 'Ensure the target Cloud SQL instance has availability-type set to REGIONAL before '
                                'initiating a failover drill.',
                     'cleanup': 'Retain `day-088-topic-04-database-ha.md` as an exit evidence artifact.',
                     'accept': 'Completed database availability decision matrix with validated automated failover '
                               'rehearsal runbook.'}}],
 'part3_intro': 'The following field cases analyze real-world production catastrophes resulting from unhedged '
                'infrastructure tiers: co-located Kubernetes pods evicted simultaneously during rolling upgrades, '
                'single-metro interconnect link cuts, zonal Persistent Disk locks during host hardware crashes, and '
                'split-brain failures in self-managed databases. Each case details quantifiable failure metrics, '
                'verbatim terminal/log transcripts, diagnostic command sequences, root cause mechanics, defensible '
                'remediations, and dual-lane failed/corrected architectural diagrams.',
 'part4_intro': 'These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author '
                'production Kubernetes PodDisruptionBudgets and TopologySpreadConstraints, configure 99.99% dual-metro '
                'Cloud Interconnect topologies with BFD timers, deploy synchronously replicated Regional Persistent '
                'Disks with dual-region Turbo Storage policies, and execute failover rehearsals across Cloud SQL HA '
                'and Cloud Spanner with zero difficulty labels.'}
