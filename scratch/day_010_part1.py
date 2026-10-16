"""Part 2 technical discussion for Topic 1: Docker."""

TOPIC_01_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ol>
<li>OCI Image Layers, Inodes, and the Copy-on-Write (OverlayFS) Rootfs</li>
<li>Dockerfile Directives and Buildkit Layer Caching Architecture</li>
<li>Container Registries, Content Addressability, and Artifact Registry</li>
<li>Bind Mounts vs Volumes vs Ephemeral Container Storage</li>
<li>POSIX Filesystem Semantics: Page Cache, sync(), and fsync() Durability</li>
</ol>

<h4>OCI Image Layers, Inodes, and the Copy-on-Write (OverlayFS) Rootfs</h4>
<p><strong class="side-heading">What it is in general:</strong> An Open Container Initiative (<strong class="keyword">OCI</strong>) container image is an immutable collection of tarball archives containing filesystem diffs, an image configuration JSON blob, and a cryptographic manifest. When a container runtime (such as containerd or Docker) launches a container, it constructs the container's root filesystem using a union filesystem driver, predominantly <strong class="keyword">OverlayFS</strong>. OverlayFS merges multiple underlying read-only image layers (referred to as <kbd>lowerdir</kbd>) with a single ephemeral, writable top layer (<kbd>upperdir</kbd>) and an internal coordination directory (<kbd>workdir</kbd>) into a single unified mount point (<kbd>merged</kbd>). Filesystem metadata and disk allocation are tracked via index nodes (<strong class="keyword">inodes</strong>). When a process reads a file, OverlayFS looks top-down through the layers and reads directly from the lowest read-only layer where the file exists. When a process attempts to modify a file belonging to a lower layer, OverlayFS performs a <strong class="keyword">Copy-on-Write</strong> (CoW) operation: it copies the entire file up to <kbd>upperdir</kbd> before permitting modifications, allocating a new inode in the writable layer while leaving the base image layer unchanged.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Union filesystem dynamics dictate container runtime performance and node storage stability. Performing heavy random writes or appending to massive log files inside the thin writable layer causes severe disk fragmentation, inode exhaustion, and significant I/O latency due to the synchronous copy-up overhead of large files. Furthermore, because <kbd>upperdir</kbd> is bound to the container's lifecycle, any file written to the container layer is deleted permanently when the container is replaced or rescheduled by Kubernetes. Architects must mandate that all stateful write paths bypass the CoW layer entirely via external volume mounts.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Kubernetes Engine (GKE) nodes running Container-Optimized OS (COS) mount the local boot disk with OverlayFS backed by <kbd>ext4</kbd>. When multiple Pods on a GKE node pull the same base image (such as Debian or distroless), the node stores only a single copy of each layer digest in the local containerd snapshotter, saving gigabytes of disk space across collocated workloads. GKE Node Auto-repair monitors local inode exhaustion on the node root filesystem and drains unhealthy nodes if rogue containers consume all available filesystem inodes.</p>

<h4>Dockerfile Directives and Buildkit Layer Caching Architecture</h4>
<p><strong class="side-heading">What it is in general:</strong> A <strong class="keyword">Dockerfile</strong> is a text manifest specifying the sequential assembly instructions used by container build engines (such as Docker BuildKit or Kaniko) to produce an OCI image. Each directive that modifies filesystem state (<kbd>FROM</kbd>, <kbd>COPY</kbd>, <kbd>ADD</kbd>, <kbd>RUN</kbd>) generates a new immutable filesystem layer. Build engines utilize content-addressable layer caching: before executing a directive, the builder calculates a SHA-256 cache key based on the instruction string and the checksums of any input files. If an exact cache hit exists in the local or remote cache, the builder skips execution and reuses the cached layer digest. If any layer cache is invalidated (for example, if a source code file copied via <kbd>COPY . .</kbd> changes), all subsequent layers are invalidated and must be rebuilt sequentially. Multi-stage builds separate build-time dependencies (compilers, SDKs, test suites) from final runtime artifacts, drastically reducing attack surfaces and final image sizes.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Dockerfile design directly impacts CI/CD pipeline velocity, network egress bandwidth, and security vulnerability profiles. Ordering directives from least-frequently changing (base OS packages, language dependencies) to most-frequently changing (application source code) maximizes layer cache hit rates, dropping build times from 10 minutes to 15 seconds. Employing multi-stage builds ensures that compilers, debug symbols, and package managers (e.g., <kbd>gcc</kbd>, <kbd>npm</kbd>, <kbd>pip</kbd>) are excluded from production containers, preventing attackers from compiling exploits inside compromised production pods.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud Build uses Kaniko and BuildKit cache backends to build container images directly on Google Cloud infrastructure. Google provides minimal, secure "Distroless" base images that contain only the runtime application and its immediate runtime dependencies—omitting package managers, shells, and standard Linux utilities—which integrate seamlessly into Artifact Registry vulnerability scanning to maintain high security compliance across GKE and Cloud Run deployments.</p>

<h4>Container Registries, Content Addressability, and Artifact Registry</h4>
<p><strong class="side-heading">What it is in general:</strong> A <strong class="keyword">container registry</strong> is an OCI-compliant distributed content-addressable storage service that stores, versions, and serves container image layers and manifests. Images are addressed not merely by mutable human-readable tags (such as <kbd>:latest</kbd> or <kbd>:v1.2.0</kbd>), but by their immutable cryptographic digest: the SHA-256 hash of the image manifest (e.g., <kbd>sha256:7b9...8f4</kbd>). When a container runtime pulls an image, it retrieves the manifest, checks which layer digests already exist in its local snapshotter, and downloads only the missing layer blobs in parallel. Content addressability ensures that if two distinct images share identical base layers, the registry and node store and transfer that layer blob exactly once.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Relying on mutable image tags (such as deploying <kbd>my-app:prod</kbd>) introduces non-deterministic deployment failures: different nodes in a Kubernetes cluster can pull different underlying image digests under the same tag, causing phantom bugs and impossible rollbacks. Enterprise architecture standards mandate referencing container images by their cryptographic SHA-256 digest in production Kubernetes manifests to guarantee immutability, auditability, and binary reproducibility across staging and production environments.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud <strong class="keyword">Artifact Registry</strong> is the enterprise evolution of Container Registry (GCR), providing regional and multi-regional OCI repositories with native IAM integration, customer-managed encryption keys (CMEK), and automated Container Analysis vulnerability scanning. Artifact Registry integrates natively with Google Cloud Binary Authorization, allowing architects to enforce deploy-time policy controls: GKE clusters automatically reject Pod deployments whose container images lack cryptographic provenance attestations signed by approved CI/CD build keys.</p>

<h4>Bind Mounts vs Volumes vs Ephemeral Container Storage</h4>
<p><strong class="side-heading">What it is in general:</strong> Container runtimes provide three distinct storage mechanisms to expose filesystems to containerized processes:
1. <strong class="keyword">Ephemeral container storage</strong>: the default writable OverlayFS layer (<kbd>upperdir</kbd>). Data written here is strictly bound to the container lifecycle; when the container process terminates or the pod is rescheduled, all written data is permanently deleted.
2. <strong class="keyword">Bind mounts</strong>: an exact file or directory on the host operating system is mounted directly into the container filesystem namespace (<kbd>mount --bind</kbd>). The container process reads and writes directly to host storage, bypassing OverlayFS CoW entirely.
3. <strong class="keyword">Named volumes</strong>: managed storage directories created and governed by the container runtime or storage plugin (in Kubernetes, PersistentVolumes managed by Container Storage Interface, <strong class="keyword">CSI</strong>, drivers). Volumes decouple the storage lifecycle entirely from container and node lifecycles, enabling independent backup, snapshotting, and reattachment across different physical hosts.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Choosing the wrong storage abstraction leads to immediate disaster. Storing transactional state in ephemeral storage guarantees data loss during routine rolling updates or node maintenance. Using bind mounts couples the container to specific host filesystem paths, breaking container portability and violating cluster security policies. Architects must mandate named volumes backed by managed network block storage for stateful workloads (databases, message brokers) while treating ephemeral container storage strictly as disposable scratch space.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> GKE utilizes the Google Compute Engine Persistent Disk CSI Driver to dynamically provision zonal and regional Persistent Disks (<kbd>pd-balanced</kbd>, <kbd>pd-ssd</kbd>, <kbd>hyperdisk-balanced</kbd>) in response to Kubernetes PersistentVolumeClaims (PVCs). GKE also provides the Cloud Storage FUSE CSI driver to mount Cloud Storage buckets as filesystems directly inside Pods, and the Filestore CSI driver for multi-writer NFS shared filesystem access across hundreds of distributed pods.</p>

<h4>POSIX Filesystem Semantics: Page Cache, sync(), and fsync() Durability</h4>
<p><strong class="side-heading">What it is in general:</strong> In modern operating systems, when an application invokes the standard POSIX <kbd>write()</kbd> system call, data is NOT written immediately to physical storage hardware. Instead, the Linux kernel copies the data into volatile kernel RAM known as the <strong class="keyword">page cache</strong>, marks the memory pages as "dirty", and returns success to the application in microseconds. The kernel's background flusher threads (<kbd>kworker</kbd> / <kbd>flusher</kbd>) periodically flush dirty pages to disk asynchronously based on sysctl thresholds (<kbd>vm.dirty_background_ratio</kbd>). If the host operating system crashes or power fails before dirty pages are flushed, all buffered data is permanently lost. To guarantee that data has physically reached non-volatile persistent media, the application must issue explicit POSIX synchronization calls:
<kbd>sync()</kbd> schedules all dirty page cache buffers across the entire system for writeback;
<strong class="keyword">fsync()</strong> flushes all modified in-core data and filesystem metadata for a specific file descriptor to non-volatile storage and blocks until the physical disk controller confirms persistence; and
<kbd>fdatasync()</kbd> flushes only the modified data and necessary retrieval metadata (omitting timestamps), reducing disk I/O operations.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Understanding POSIX persistence semantics is critical when designing stateful systems on cloud infrastructure. High-throughput ingestion microservices that buffer records in RAM without invoking <kbd>fsync()</kbd> will report successful transaction writes to clients, only to suffer silent data corruption or loss when the cloud provider executes live migration or preempts a spot instance. Architects must ensure database engines (PostgreSQL, MySQL, Kafka) configure Write-Ahead Logging (WAL) with calibrated <kbd>fsync</kbd> commit intervals, and recognize that cloud block storage latency is directly tied to IOPS and sync flush throughput.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine Persistent Disks (PD) and Hyperdisk volumes emulate SCSI/NVMe storage controllers that acknowledge <kbd>fsync()</kbd> flushes only when data has been written to redundant non-volatile physical storage across Google's storage network. In GKE, write-heavy databases that issue frequent <kbd>fsync()</kbd> calls require <kbd>pd-ssd</kbd> or <kbd>hyperdisk-balanced</kbd> volumes with high provisioned IOPS to avoid queue depth saturation and transaction commit latency spikes.</p>

{FIG_10_1_HTML}

<div class="topic-card">
<table>
<caption>Table 10.1: Container Storage Abstractions and Persistence Characteristics</caption>
<thead>
<tr>
<th>Storage Layer</th>
<th>Lifecycle &amp; Scope</th>
<th>Filesystem Mechanism</th>
<th>Durability Guarantee</th>
<th>GCP CSI / Service Equivalent</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Ephemeral Container Layer</strong></td>
<td>Bound to container process; deleted upon pod restart</td>
<td>OverlayFS thin writable layer (<kbd>upperdir</kbd>)</td>
<td>Zero durability; volatile to container crashes</td>
<td>Local node root disk (<kbd>/var/lib/containerd</kbd>)</td>
</tr>
<tr>
<td><strong>EmptyDir Volume</strong></td>
<td>Bound to Pod lifecycle; deleted when Pod is deleted</td>
<td>Host filesystem directory or in-memory <kbd>tmpfs</kbd></td>
<td>Survives container restarts within the same Pod</td>
<td>GKE local SSD or ephemeral node storage</td>
</tr>
<tr>
<td><strong>PersistentVolume (Block)</strong></td>
<td>Independent of Pod/node lifecycle; durable network storage</td>
<td>Direct block device format (<kbd>ext4</kbd>/<kbd>xfs</kbd>)</td>
<td>Full durability; requires <kbd>fsync()</kbd> to commit</td>
<td>GKE Compute Engine PD CSI Driver (<kbd>pd-balanced</kbd>)</td>
</tr>
<tr>
<td><strong>Shared Volume (NFS)</strong></td>
<td>Shared across multiple pods concurrently (<kbd>ReadWriteMany</kbd>)</td>
<td>Network File System (NFSv3 / NFSv4)</td>
<td>Centralized durability across multi-zone nodes</td>
<td>GKE Filestore CSI Driver / Managed Filestore</td>
</tr>
<tr>
<td><strong>Object Storage Mount</strong></td>
<td>Global scale; blob storage mounted as POSIX directory</td>
<td>FUSE userspace filesystem mapping to object APIs</td>
<td>Object-level durability; non-standard POSIX semantics</td>
<td>GKE Cloud Storage FUSE CSI Driver</td>
</tr>
</tbody>
</table>
</div>

<p><strong class="side-heading">Concrete example:</strong> Consider an order processing microservice that generates transaction verification tokens before dispatching payment events. In the legacy version, the developer writes tokens to <kbd>/tmp/tokens.log</kbd> inside the container without mounting a volume. When GKE triggers a rolling update to deploy a new container version, Kubernetes terminates the old pod, destroying its OverlayFS writable layer. The new replacement pod starts with an empty <kbd>/tmp</kbd>, leaving incoming checkout verification requests with missing token files and causing duplicate customer charges. The architect remediates the service by attaching a Kubernetes PersistentVolumeClaim backed by <kbd>pd-balanced</kbd> mounted to <kbd>/var/lib/tokens</kbd>. Furthermore, the application code is updated to invoke <kbd>os.fsync(f.fileno())</kbd> immediately after appending each token record. When the pod is redeployed, the Persistent Disk dynamically unmounts from the old node, reattaches to the replacement pod's node, and all transaction tokens are read intact, preserving at-most-once payment processing.</p>

<p><strong class="side-heading">Evidence limit:</strong> Observing successful execution of an application <kbd>write()</kbd> system call proves data transfer into the operating system kernel's memory page cache; it does NOT prove that data has been committed to non-volatile physical storage media without verifying that <kbd>fsync()</kbd> completed successfully without returning <kbd>EIO</kbd> or <kbd>EROFS</kbd> errors.</p>
'''
