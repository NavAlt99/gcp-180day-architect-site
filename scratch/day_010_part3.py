"""Part 2 technical discussion for Topic 3: Kubernetes core objects."""

TOPIC_03_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ol>
<li>Pods: The Atomic Unit of Kubernetes Scheduling and Collocation</li>
<li>Deployments and ReplicaSets: Declarative Rollouts and Rollbacks</li>
<li>Services and EndpointSlices: Stable Networking and Service Discovery</li>
<li>Ingress Controllers and Cloud Load Balancing Integration</li>
<li>ConfigMaps and Secrets: Decoupling Configuration and Sensitive Credentials</li>
</ol>

<h4>Pods: The Atomic Unit of Kubernetes Scheduling and Collocation</h4>
<p><strong class="side-heading">What it is in general:</strong> A <strong class="keyword">Pod</strong> is the smallest deployable and schedulable compute unit in Kubernetes. A Pod encapsulates one or more application containers that share a common context: specifically, they share the same Linux Network namespace (meaning all containers in a Pod share the same IP address and port space, communicating with each other over <kbd>localhost</kbd>), the same IPC namespace, and can mount shared volumes. In contrast, containers within a Pod maintain independent Mount and PID namespaces (unless process namespace sharing is explicitly enabled). Multi-container Pod patterns include the Sidecar (logging/telemetry agents running alongside the main service), the Ambassador (local proxy abstracting external database connections), and the Init Container (runs to completion before main application containers initialize).</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Pods must be designed with single-responsibility principles. Placing multiple unrelated services into the same Pod couples their scaling, lifecycle, and failure domains: if Container A crashes or leaks memory, the entire Pod is terminated or rescheduled. Architects restrict multi-container Pods strictly to tightly coupled helper sidecars (e.g., Envoy proxies in service meshes, cloud storage sync sidecars) while decoupling independent microservices into their own dedicated Pods and Deployments.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In GKE, every Pod receives an IP address natively routable within the Google Cloud Virtual Private Cloud (VPC) through VPC-native clusters (using alias IP ranges). This architecture eliminates double overlay encapsulation (e.g., VXLAN/Geneve overhead), allowing GKE Pods to communicate directly with Compute Engine VMs, Cloud SQL databases, and on-premises systems at native network speeds.</p>

<h4>Deployments and ReplicaSets: Declarative Rollouts and Rollbacks</h4>
<p><strong class="side-heading">What it is in general:</strong> In production Kubernetes, bare Pods are virtually never created directly; instead, they are managed by higher-level controllers. A <strong class="keyword">Deployment</strong> is a declarative object that manages the lifecycle of a stateless application. The Deployment controller does not manage Pods directly; rather, it manages intermediate <strong class="keyword">ReplicaSets</strong>, which in turn ensure that a specified number of identical Pod replicas are running at any given time. When a Deployment is updated (e.g., changing the container image from <kbd>v1</kbd> to <kbd>v2</kbd>), the Deployment controller creates a new ReplicaSet and orchestrates a zero-downtime rolling update based on two parameters:
<kbd>maxSurge</kbd> (how many extra pods can be created above the desired replica count during the update) and
<kbd>maxUnavailable</kbd> (how many pods can be unavailable during the update).
If the new version fails health probes or throws runtime exceptions, Kubernetes supports instant rollback (<kbd>kubectl rollout undo</kbd>) to the previous ReplicaSet revision without rebuilding container images.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Deployments provide the mathematical guarantees governing service availability during production releases. Configuring <kbd>maxSurge: 25%</kbd> and <kbd>maxUnavailable: 0</kbd> ensures that existing traffic capacity is never degraded while new versions are provisioned. For canary and blue-green deployment strategies, architects leverage multiple Deployments with shared Service selectors or service mesh traffic splitters (Istio/Anthos Service Mesh) to route small percentages of live traffic to canary releases before initiating full rollouts.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> GKE integrates Deployment rollouts directly with Cloud Deploy and Cloud Build. Google Cloud Deploy provides managed, continuous delivery pipelines that automate canary progressions, approval gates, and rollback policies across development, staging, and multi-region production GKE clusters.</p>

<h4>Services and EndpointSlices: Stable Networking and Service Discovery</h4>
<p><strong class="side-heading">What it is in general:</strong> Because Kubernetes Pods are ephemeral entities that receive dynamic, unpredictable IP addresses upon creation and destruction, clients cannot connect directly to individual Pod IPs. A <strong class="keyword">Service</strong> provides an immutable, long-lived network abstraction: a stable virtual IP address (ClusterIP), a stable DNS name (e.g., <kbd>my-service.default.svc.cluster.local</kbd>), and load balancing across all matching Pods. The Service identifies target Pods using a key-value <strong class="keyword">label selector</strong> (e.g., <kbd>selector: app: orders</kbd>). The Kubernetes <strong class="keyword">EndpointSlice</strong> controller continuously queries the API server for Pods carrying matching labels and populates the Service's EndpointSlice with the active IP addresses and port combinations of all healthy, ready pods. Under the hood, <kbd>kube-proxy</kbd> translates the Service virtual IP into backend Pod IPs using kernel <kbd>iptables</kbd> or <kbd>IPVS</kbd> connection tracking rules.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> The decoupling of Services from Pod IPs via label selectors is the cornerstone of cloud-native resilience. However, this decoupling introduces a classic operational vulnerability: a single typographical error in a Service selector label (e.g., matching <kbd>app: order</kbd> instead of <kbd>app: orders</kbd>) leaves the EndpointSlice completely empty. The Service continues to exist and resolve in DNS, but all incoming client requests immediately fail with HTTP 503 or connection refused, even while all backend Pods report 100% healthy status. Architects must implement automated manifest linting and integration testing to validate selector alignment before deployment.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In GKE VPC-native clusters, Google Cloud implements container-native load balancing: Google Cloud Load Balancers bypass <kbd>kube-proxy</kbd> iptables entirely, programming network endpoint groups (NEGs) directly with Pod IP addresses. This eliminates double load balancing hops, preserves client source IP addresses, and enables advanced Google Cloud traffic steering at the network perimeter.</p>

<h4>Ingress Controllers and Cloud Load Balancing Integration</h4>
<p><strong class="side-heading">What it is in general:</strong> While a Service operating in <kbd>ClusterIP</kbd> mode provides internal cluster networking, exposing HTTP/HTTPS applications to external Internet clients requires an <strong class="keyword">Ingress</strong> object. An Ingress is an API resource that defines external HTTP routing rules, host-based routing (e.g., <kbd>api.example.com</kbd> vs <kbd>shop.example.com</kbd>), path-based routing (e.g., <kbd>/orders/*</kbd> vs <kbd>/users/*</kbd>), and TLS termination. The Ingress resource alone is merely a static rule declaration; it requires an active <strong class="keyword">Ingress Controller</strong> running in the cluster to translate the declaration into actual proxy configurations (e.g., NGINX, Envoy) or cloud infrastructure load balancers.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Utilizing a centralized Ingress controller is vastly superior to exposing individual microservices via raw <kbd>LoadBalancer</kbd> Services. Creating a <kbd>LoadBalancer</kbd> Service for every microservice provisions a dedicated cloud load balancer and public IP address for each service, multiplying cloud networking costs and complicating centralized TLS certificate management. A unified Ingress controller consolidates hundreds of backend microservices behind a single public IP and unified edge security perimeter.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> The GKE Ingress Controller (GCE Ingress) automatically provisions Google Cloud External HTTP(S) Load Balancers or Internal Application Load Balancers in response to Ingress resources. GKE Ingress natively integrates with Google-managed SSL certificates (automatically provisioning and renewing free Let's Encrypt certificates), Cloud Armor for Layer 7 WAF and DDoS mitigation, and Cloud CDN for edge content caching.</p>

<h4>ConfigMaps and Secrets: Decoupling Configuration and Sensitive Credentials</h4>
<p><strong class="side-heading">What it is in general:</strong> The cloud-native Twelve-Factor App methodology mandates strict separation of configuration code from executable binaries. Kubernetes implements this through two declarative storage objects:
1. <strong class="keyword">ConfigMaps</strong>: store non-confidential configuration data as key-value pairs (e.g., database connection strings, feature flags, application port numbers).
2. <strong class="keyword">Secrets</strong>: store sensitive data (e.g., API keys, database passwords, TLS private keys). By default, Kubernetes stores Secrets as base64-encoded strings in etcd.
Both ConfigMaps and Secrets can be consumed by Pods either as environment variables (<kbd>env</kbd> / <kbd>envFrom</kbd>) or mounted as read-only filesystem volumes (<kbd>volumeMounts</kbd>). Mounted volumes update dynamically in near-real-time when the underlying ConfigMap or Secret is edited in etcd, whereas environment variables require a Pod restart to reflect changes.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Baking configuration values or API tokens into container images is an extreme security and operational anti-pattern. If a database password changes, the team must rebuild, retest, and redeploy container images. More critically, hardcoding credentials in images exposes secrets to anyone with read access to the container registry. Architects mandate injecting all configuration and secrets dynamically at runtime, ensuring that images remain strictly generic, environment-agnostic, and secure across development, staging, and production tiers.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> GKE provides multiple enterprise secret management patterns. By default, GKE supports Database Encryption for etcd, encrypting Secrets at rest using Google Cloud Key Management Service (Cloud KMS) keys. Furthermore, architects leverage the Google Cloud Secret Manager CSI driver and Workload Identity to mount secrets directly from Secret Manager into GKE pods, eliminating the need to store sensitive credentials in etcd altogether.</p>

{FIG_10_3_HTML}

<div class="topic-card">
<table>
<caption>Table 10.3: Kubernetes Core Object Taxonomy and Responsibilities</caption>
<thead>
<tr>
<th>Core Object</th>
<th>Scope &amp; Purpose</th>
<th>Key Configuration Fields</th>
<th>GCP Managed Equivalent / Integration</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Pod</strong></td>
<td>Atomic schedulable container bundle; shared IP &amp; netns</td>
<td><kbd>containers[]</kbd>, <kbd>volumes[]</kbd>, <kbd>restartPolicy</kbd></td>
<td>VPC-native Pod IP via alias IP ranges</td>
</tr>
<tr>
<td><strong>Deployment</strong></td>
<td>Declarative replica management &amp; zero-downtime rollouts</td>
<td><kbd>replicas</kbd>, <kbd>selector</kbd>, <kbd>strategy.rollingUpdate</kbd></td>
<td>Google Cloud Deploy canary pipelines</td>
</tr>
<tr>
<td><strong>Service</strong></td>
<td>Stable virtual IP &amp; load balancing across dynamic pod IPs</td>
<td><kbd>selector</kbd>, <kbd>ports[]</kbd>, <kbd>type: ClusterIP</kbd></td>
<td>Container-native load balancing via NEGs</td>
</tr>
<tr>
<td><strong>Ingress</strong></td>
<td>External HTTP/HTTPS path routing &amp; TLS termination</td>
<td><kbd>rules.http.paths[]</kbd>, <kbd>tls[]</kbd></td>
<td>Google Cloud External HTTP(S) Load Balancer</td>
</tr>
<tr>
<td><strong>ConfigMap</strong></td>
<td>Decoupled non-sensitive runtime configuration parameters</td>
<td><kbd>data{}</kbd>, mounted via <kbd>volumeMounts</kbd> / <kbd>env</kbd></td>
<td>Config Sync / Anthos Config Management</td>
</tr>
<tr>
<td><strong>Secret</strong></td>
<td>Decoupled sensitive credentials, tokens, and certificates</td>
<td><kbd>data{}</kbd> (base64), <kbd>type: Opaque</kbd></td>
<td>Google Cloud Secret Manager CSI Driver</td>
</tr>
</tbody>
</table>
</div>

<p><strong class="side-heading">Concrete example:</strong> Consider an inventory microservice deployed on GKE that consists of 3 replicas. The deployment manifest labels its pods with <kbd>app: inventory-service</kbd>. During a major release, an engineer accidentally edits the Service manifest selector to <kbd>app: inventory-backend</kbd>. When the deployment updates, the pods spin up, initialize successfully, pass their HTTP readiness probes, and achieve <kbd>Running</kbd> status. However, because the Service selector does not match the Pod labels, the EndpointSlice controller clears all IP addresses from the Service's endpoint list. When the Google Cloud Load Balancer forwards external traffic through the Ingress to the Service, the backend target group has zero active endpoints, causing the load balancer to return instant HTTP 503 Service Unavailable errors to all customers. The architect diagnoses the failure by running <kbd>kubectl get endpoints inventory-service</kbd>, identifies the selector typo, aligns the label, and observes instant restoration of HTTP 200 traffic.</p>

<p><strong class="side-heading">Evidence limit:</strong> Verifying that a Kubernetes Service object exists and has an assigned ClusterIP in <kbd>kubectl get svc</kbd> proves that the service resource was registered in etcd; it does NOT prove that traffic is actively routing to application pods without confirming that <kbd>kubectl get endpointslices</kbd> displays ready IP addresses matching running pods.</p>
'''
