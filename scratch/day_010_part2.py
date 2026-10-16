"""Part 2 technical discussion for Topic 2: Container orchestration."""

TOPIC_02_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ol>
<li>The Failure Modes of Standalone Host Container Management</li>
<li>Declarative Desired State vs Imperative Container Commands</li>
<li>Continuous Reconciliation Loops and the Control Plane Architecture</li>
<li>Automated Scheduling, Bin Packing, and Resource Constraint Enforcement</li>
<li>Self-Healing: Liveness/Readiness Probes, Restarts, and Rescheduling</li>
</ol>

<h4>The Failure Modes of Standalone Host Container Management</h4>
<p><strong class="side-heading">What it is in general:</strong> Managing containers imperatively on standalone host servers (using raw Docker CLI commands or static systemd unit files) introduces catastrophic failure modes when operating distributed microservices at enterprise scale. On a standalone host:
1. <strong class="keyword">No automated failover</strong>: if the underlying physical host or VM suffers a kernel panic, hardware fault, or network partition, all containers running on that host terminate and remain down indefinitely until human operators manually intervene.
2. <strong class="keyword">Host port collision</strong>: running multiple replicas of the same service requires manual, error-prone host port mappings (e.g., binding container port 8080 to host port 8081, 8082), severely limiting replica density.
3. <strong class="keyword">No bin packing or global scheduling</strong>: operators must guess which host has sufficient spare CPU and memory headroom, leading to extreme resource fragmentation where some nodes are starved while others sit idle.
4. <strong class="keyword">Brittle zero-downtime upgrades</strong>: executing rolling updates requires custom shell scripts to stop old containers and launch new ones sequentially, with no automated health checking, rollback capabilities, or traffic draining.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Relying on standalone container hosting (e.g., a fleet of Compute Engine VMs running Docker daemons with bash deploy scripts) creates an operational bottleneck that caps organization velocity and destroys Service Level Objectives (SLOs). Mean Time to Recovery (MTTR) is measured in hours rather than seconds because failure detection and remediation depend on human on-call engineers. Architects adopt container orchestrators to transform compute infrastructure from brittle, pet-like individual servers into a fungible, self-healing utility fabric.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google pioneered large-scale container orchestration over two decades ago with its internal Borg system, which manages millions of containers running Google Search, Gmail, and YouTube. Kubernetes was designed by Google based on the architectural lessons of Borg. In GCP, Google Kubernetes Engine (GKE) provides fully managed, production-grade Kubernetes, eliminating the operational overhead of installing, patching, and scaling master nodes and worker node pools.</p>

<h4>Declarative Desired State vs Imperative Container Commands</h4>
<p><strong class="side-heading">What it is in general:</strong> In imperative systems, the operator issues a sequence of discrete procedural instructions telling the system *how* to execute a change (e.g., <kbd>docker run -d -p 80:8080 my-image</kbd>, <kbd>docker stop my-container</kbd>). If an intermediate command fails or the system state drifts, the script cannot self-correct. In contrast, <strong class="keyword">declarative configuration</strong> specifies *what* the desired end state of the system should be (e.g., "there must be exactly 5 replicas of <kbd>my-image</kbd> running with 512 MB memory requests, exposed on port 80"). The declaration is written as a structured YAML or JSON document and submitted to the centralized API server. The platform compares the declared desired state against the actual observed state of the cluster and computes the minimal set of transitions needed to align reality with the declaration.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Declarative management is the foundational prerequisite for GitOps and infrastructure-as-code (IaC). Because the entire desired state of the application architecture is stored as text manifests in Git repositories, auditing, code review, drift detection, and catastrophic disaster recovery become deterministic: an entire multi-region cluster can be recreated identically in minutes simply by applying the declared manifests against a fresh cluster.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> GKE integrates natively with declarative deployment tooling, including Google Cloud Config Sync (part of GKE Enterprise) which continuously reconciles cluster state against Git repositories. GKE also supports Anthos Config Management to enforce uniform security policies and compliance guardrails across hybrid and multi-cloud GKE clusters using declarative constraints.</p>

<h4>Continuous Reconciliation Loops and the Control Plane Architecture</h4>
<p><strong class="side-heading">What it is in general:</strong> The core architectural engine of Kubernetes is the <strong class="keyword">declarative control loop</strong> (or reconciliation loop), implemented across the Kubernetes control plane components:
1. <strong class="keyword">kube-apiserver</strong>: the central REST API gateway and sole component that communicates directly with the persistent cluster data store.
2. <strong class="keyword">etcd</strong>: a distributed, highly available, consistent key-value store (using the Raft consensus algorithm) that acts as the single source of truth for all cluster object state.
3. <strong class="keyword">kube-controller-manager</strong>: a daemon that embeds the core control loops (Deployment controller, ReplicaSet controller, Node controller). Each controller executes an infinite loop:
   <kbd>Observe actual state -&gt; Compare with desired state in etcd -&gt; Calculate divergence -&gt; Issue corrective API calls</kbd>.
4. <strong class="keyword">kube-scheduler</strong>: watches for unscheduled Pods and assigns them to optimal worker nodes based on resource filtering and scoring algorithms.
5. <strong class="keyword">kubelet</strong>: the node-level agent running on every worker node that watches the API server for Pods assigned to its node and instructs the Container Runtime Interface (<strong class="keyword">CRI</strong>, e.g., containerd) to pull images, create containers, and mount volumes.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Because reconciliation is asynchronous, continuous, and level-triggered (reacting to current state rather than edge-triggered events), the system is naturally resilient to transient failures, network partitions, and dropped messages. If a worker node crashes, the Node controller detects the missing heartbeat, marks the node as unreachable, and the ReplicaSet controller notices that the observed replica count is below the desired count, automatically scheduling replacement Pods onto healthy surviving nodes.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In GKE, Google manages the entire control plane (<kbd>kube-apiserver</kbd>, <kbd>etcd</kbd>, controller managers, schedulers) as a high-availability, multi-zone service with automated upgrades, repair, and backup backed by Google's Site Reliability Engineering (SRE) teams. GKE Autopilot takes this further by completely managing node provisioning, hardening, and scaling, exposing only the declarative Kubernetes API to the customer.</p>

<h4>Automated Scheduling, Bin Packing, and Resource Constraint Enforcement</h4>
<p><strong class="side-heading">What it is in general:</strong> The <strong class="keyword">kube-scheduler</strong> is responsible for assigning unscheduled Pods to available worker nodes in a two-phase algorithmic cycle:
1. <strong class="keyword">Filtering (Predicates)</strong>: evaluates whether a node satisfies the mandatory requirements of the Pod. Checks include <kbd>NodeResourcesFit</kbd> (does the node have sufficient unallocated Allocatable CPU and Memory to satisfy the Pod's <kbd>resources.requests</kbd>?), <kbd>NodeName</kbd>, <kbd>NodePorts</kbd>, <kbd>NodeAffinity</kbd>, and <kbd>Tolerations</kbd> against node <kbd>Taints</kbd>. If a node fails any predicate, it is discarded.
2. <strong class="keyword">Scoring (Priorities)</strong>: ranks the remaining candidate nodes using scoring plugins (e.g., <kbd>NodeResourcesBalancedAllocation</kbd> to achieve uniform resource utilization, <kbd>ImageLocality</kbd> to favor nodes that already have image layers cached). The node with the highest aggregate score is selected, and a binding object is written to etcd.
This automated <strong class="keyword">bin packing</strong> packs heterogeneous workloads onto the minimal number of compute nodes required, maximizing compute utilization.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Kubernetes scheduling decisions are strictly governed by resource *requests*, not resource *limits*. If developers omit <kbd>resources.requests</kbd> in Pod specifications, the scheduler treats the Pod as requiring zero CPU and zero RAM, scheduling dozens of pods onto a single node until the node suffers severe memory pressure and invokes the kernel OOM killer. Architects must establish mandatory Admission Controllers (ValidatingAdmissionWebhooks or Kyverno) to reject any Pod that lacks declared resource requests, ensuring predictable bin packing and preventing node starvation.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> GKE integrates the Kubernetes scheduler directly with the GKE Cluster Autoscaler. When the scheduler cannot place a Pod because all nodes fail the filtering phase (e.g., <kbd>0/3 nodes available: 3 Insufficient memory</kbd>), the Cluster Autoscaler detects the unschedulable Pod and automatically triggers the provisioning of new Compute Engine VM worker nodes in the appropriate node pool, scaling down instances when workloads subside.</p>

<h4>Self-Healing: Liveness/Readiness Probes, Restarts, and Rescheduling</h4>
<p><strong class="side-heading">What it is in general:</strong> Kubernetes implements autonomous <strong class="keyword">self-healing</strong> through active container health telemetry and decoupled lifecycle probes:
1. <strong class="keyword">Liveness probe</strong>: periodically interrogates the running container (via HTTP GET, TCP socket, or exec command). If the probe fails consecutively beyond <kbd>failureThreshold</kbd> (e.g., if the application is deadlocked or trapped in an infinite loop), kubelet kills the container and restarts it according to the Pod's <kbd>restartPolicy</kbd>.
2. <strong class="keyword">Readiness probe</strong>: determines whether the container is ready to accept incoming network traffic (e.g., during database connection warm-up or cache loading). If the readiness probe fails, the container is NOT restarted; instead, the endpoints controller immediately removes the Pod's IP address from all matching Service EndpointSlices, preventing external traffic from reaching the unready container.
3. <strong class="keyword">Startup probe</strong>: protects slow-starting legacy applications by temporarily disabling liveness and readiness probes until the application completes initial startup.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Decoupling liveness from readiness is an architectural masterpiece. Conflating the two causes cascading outages: if an overloaded application starts failing HTTP requests due to downstream database latency, killing the container (liveness) simply exacerbates the overload by forcing cold container restarts. Correctly configuring readiness probes removes overloaded pods from the load balancing pool while allowing them to process existing requests, while liveness probes restart only genuinely crashed or deadlocked processes.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> GKE health checks integrate directly with Google Cloud external and internal HTTP(S) Load Balancers via container-native load balancing (using Network Endpoint Groups, NEGs). When a readiness probe fails on a GKE pod, the Google Cloud Load Balancer stops routing packets to that specific pod IP within milliseconds at the network edge, providing sub-second traffic diversion without proxy hop latency.</p>

{FIG_10_2_HTML}

<div class="topic-card">
<table>
<caption>Table 10.2: Standalone Host Management vs Kubernetes Container Orchestration</caption>
<thead>
<tr>
<th>Operational Capability</th>
<th>Standalone Docker Host</th>
<th>Kubernetes Orchestration (GKE)</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>System State Model</strong></td>
<td>Imperative (<kbd>docker run</kbd>, shell scripts)</td>
<td>Declarative (desired YAML state reconciled via etcd)</td>
</tr>
<tr>
<td><strong>Host Hardware Failure</strong></td>
<td>Manual detection; downtime until operator rebuilds VM</td>
<td>Autonomous rescheduling of pods onto healthy nodes</td>
</tr>
<tr>
<td><strong>Port &amp; IP Allocation</strong></td>
<td>Host port collision risk; manual port mapping required</td>
<td>Software-defined pod IP per container; virtual Services</td>
</tr>
<tr>
<td><strong>Replica Scheduling</strong></td>
<td>Manual node placement; uneven host utilization</td>
<td>Two-tier algorithmic filtering &amp; scoring bin packing</td>
</tr>
<tr>
<td><strong>Health Telemetry</strong></td>
<td>Basic process exit monitoring (<kbd>restart: always</kbd>)</td>
<td>Multi-stage liveness, readiness, and startup probes</td>
</tr>
<tr>
<td><strong>Horizontal Scaling</strong></td>
<td>Manual VM provisioning and container launching</td>
<td>Horizontal Pod Autoscaler (HPA) &amp; Cluster Autoscaler</td>
</tr>
</tbody>
</table>
</div>

<p><strong class="side-heading">Concrete example:</strong> Consider an e-commerce checkout deployment that scales from 2 to 5 replicas during a Black Friday flash sale. In a standalone environment, an operator manually executes <kbd>docker run</kbd> on a single VM, only to breach host RAM limits, triggering kernel OOM terminations that crash all checkout containers simultaneously and drop hundreds of customer orders. Under Kubernetes orchestration on GKE, the deployment controller declares <kbd>replicas: 5</kbd>. The scheduler evaluates all cluster nodes: it places 2 replicas on Node 1, 1 replica on Node 2, and identifies that Node 3 lacks sufficient allocatable memory. Instead of crashing, the remaining 2 pods enter <kbd>Pending</kbd>, which immediately signals the GKE Cluster Autoscaler. Within 90 seconds, GKE spins up an additional Compute Engine node, the scheduler binds the pending pods, readiness probes pass, and customer traffic scales smoothly across all 5 instances.</p>

<p><strong class="side-heading">Evidence limit:</strong> Observing that all Pods in a Deployment have reached <kbd>Running</kbd> status proves that the scheduler successfully assigned nodes and kubelet started the containers; it does NOT prove that application containers are serving valid HTTP traffic without verifying that readiness probes have passed and EndpointSlices contain healthy target IP addresses.</p>
'''
