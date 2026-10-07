"""Durable data specification for Day 6: Shell, processes and services."""

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'chmod(2) Linux manual page description (accessed 2026-10-04)',
        'https://man7.org/linux/man-pages/man2/chmod.2.html#DESCRIPTION'
    ),
    'topic-02': (
        'systemd.service(5) Linux manual page description (accessed 2026-10-04)',
        'https://man7.org/linux/man-pages/man5/systemd.service.5.html#DESCRIPTION'
    )
}

FIG_6_1_HTML = '''<figure class="diagram-figure"><p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p><svg aria-labelledby="day6-perm-title day6-perm-desc" role="img" viewbox="0 0 940 290" xmlns="http://www.w3.org/2000/svg"><title id="day6-perm-title">User-space file request crossing the kernel permission boundary</title><desc id="day6-perm-desc">The Order API process requests config.json. The kernel checks process credentials, path traversal and the selected owner, group or other mode before the filesystem returns data or permission denied.</desc><defs><marker id="day6-perm-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker></defs><rect fill="#121526" height="132" rx="10" stroke="#38bdf8" stroke-width="2" width="210" x="20" y="38"></rect><image href="../assets/icons/generic/user.svg" x="35" y="52" width="26" height="26" preserveAspectRatio="xMidYMid meet"/><rect fill="#121526" height="132" rx="10" stroke="#f43f5e" stroke-width="2" width="366" x="286" y="38"></rect><image href="../assets/icons/generic/policy.svg" x="301" y="52" width="26" height="26" preserveAspectRatio="xMidYMid meet"/><rect fill="#121526" height="132" rx="10" stroke="#34d399" stroke-width="2" width="210" x="708" y="38"></rect><image href="../assets/icons/generic/storage.svg" x="723" y="52" width="26" height="26" preserveAspectRatio="xMidYMid meet"/><g fill="#fce7f3" font-size="15" font-weight="700" text-anchor="middle"><text x="135" y="73">User space</text><text x="479" y="73">Kernel checks</text><text x="823" y="73">Filesystem result</text></g><g fill="#a9b7cb" font-size="12" text-anchor="middle"><text x="125" y="106">Order API process</text><text x="125" y="135">open(config.json)</text><text x="469" y="103">effective UID / groups</text><text x="469" y="128">parent directory search</text><text x="469" y="153">owner · group · other bits</text><text x="813" y="106">file descriptor</text><text x="813" y="135">or EACCES</text></g><g fill="none" marker-end="url(#day6-perm-arrow)" stroke="#38bdf8" stroke-width="2"><path d="M230 104 L280 104"></path><path d="M652 104 L702 104"></path></g><line stroke="#f43f5e" stroke-dasharray="6 5" x1="257" x2="257" y1="22" y2="190"></line><text fill="#f43f5e" font-size="12" text-anchor="middle" x="257" y="218">system-call boundary</text><text fill="#a9b7cb" font-size="12" text-anchor="middle" x="470" y="258">A successful administrator read does not prove the service identity can read the same path.</text></svg><figcaption>Figure 6.1: The conceptual access path separates the user-space caller from kernel enforcement. It omits filesystem-specific ACL and security-module details that must be inspected when ordinary mode bits do not explain the result.</figcaption></figure>'''

FIG_6_2_HTML = '''<figure class="diagram-figure"><p class="diagram-scroll-hint">Swipe horizontally to view the full diagram.</p><svg aria-labelledby="day6-service-title day6-service-desc" role="img" viewbox="0 0 940 315" xmlns="http://www.w3.org/2000/svg"><title id="day6-service-title">Boot-to-service control flow and process streams</title><desc id="day6-service-desc">Systemd starts a unit, the kernel creates the worker process, file descriptors zero through two connect input and logs, and SIGTERM allows cleanup before exit while SIGKILL bypasses application cleanup.</desc><defs><marker id="day6-service-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker></defs><g fill="#121526" stroke-width="2"><rect height="122" rx="10" stroke="#38bdf8" width="205" x="18" y="42"></rect><image href="../assets/icons/generic/server.svg" x="28" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/><rect height="122" rx="10" stroke="#38bdf8" width="205" x="274" y="42"></rect><image href="../assets/icons/generic/artifact.svg" x="284" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/><rect height="122" rx="10" stroke="#34d399" width="205" x="530" y="42"></rect><image href="../assets/icons/gcp/core/compute-engine.svg" x="540" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/><rect height="122" rx="10" stroke="#f43f5e" width="136" x="786" y="42"></rect><image href="../assets/icons/generic/monitoring.svg" x="796" y="54" width="24" height="24" preserveAspectRatio="xMidYMid meet"/></g><g fill="#fce7f3" font-size="15" font-weight="700" text-anchor="middle"><text x="130" y="76">Boot target</text><text x="386" y="76">systemd unit</text><text x="642" y="76">Worker process</text><text x="864" y="76">Journal</text></g><g fill="#a9b7cb" font-size="12" text-anchor="middle"><text x="120" y="108">dependency order</text><text x="120" y="137">requested state</text><text x="376" y="108">start / stop / restart</text><text x="376" y="137">tracks main PID</text><text x="632" y="108">fd 0 input</text><text x="632" y="132">fd 1 stdout</text><text x="632" y="154">fd 2 stderr</text><text x="854" y="112">timestamps</text><text x="854" y="137">unit + PID</text></g><g fill="none" marker-end="url(#day6-service-arrow)" stroke="#38bdf8" stroke-width="2"><path d="M223 103 L268 103"></path><path d="M479 103 L524 103"></path><path d="M735 103 L780 103"></path></g><path d="M632 194 L632 242" marker-end="url(#day6-service-arrow)" stroke="#34d399" stroke-width="3"></path><path d="M632 194 C705 208 740 219 786 242" stroke="#f43f5e" stroke-dasharray="7 5" stroke-width="3"></path><g font-size="12" text-anchor="middle"><text fill="#34d399" x="548" y="222">SIGTERM → handler → exit</text><text fill="#f43f5e" x="770" y="222">SIGKILL → immediate stop</text><text fill="#a9b7cb" x="632" y="282">The wait status and logs explain termination; the durable store explains business completion.</text></g></svg><figcaption>Figure 6.2: The service manager, kernel process, streams and journal provide different evidence. The two shutdown paths are conceptual; actual timeout and restart policy come from the unit configuration.</figcaption></figure>'''

FIG_6_3_HTML = '''<figure class="diagram-figure"><p class="diagram-scroll-hint">Swipe horizontally to view the full incident diagram.</p><svg aria-labelledby="day6-perm-incident-title day6-perm-incident-desc" role="img" viewbox="0 0 940 390" xmlns="http://www.w3.org/2000/svg"><title id="day6-perm-incident-title">Order API configuration permission incident before and after repair</title><desc id="day6-perm-incident-desc">Before repair, the service user reaches config.json but owner-only mode permits only the deployment administrator, so the kernel returns EACCES. After repair, a restricted order-api group has directory search and file read permission, and a read as the service identity verifies the boundary.</desc><defs><marker id="day6-perm-incident-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker></defs><text fill="#f43f5e" font-size="15" font-weight="700" x="24" y="35">BEFORE · failing path</text><g fill="#121526" stroke-width="2"><rect height="100" rx="10" stroke="#38bdf8" width="210" x="24" y="56"></rect><image href="../assets/icons/generic/user.svg" x="36" y="68" width="22" height="22" preserveAspectRatio="xMidYMid meet"/><rect height="100" rx="10" stroke="#38bdf8" width="260" x="294" y="56"></rect><image href="../assets/icons/generic/storage.svg" x="306" y="68" width="22" height="22" preserveAspectRatio="xMidYMid meet"/><rect height="100" rx="10" stroke="#f43f5e" width="300" x="614" y="56"></rect><image href="../assets/icons/generic/failure.svg" x="626" y="68" width="22" height="22" preserveAspectRatio="xMidYMid meet"/></g><g fill="#fce7f3" font-size="14" font-weight="700" text-anchor="middle"><text x="139" y="88">Order API</text><text x="434" y="88">/srv/brightloaf/order-api</text><text x="774" y="88">config.json · admin:admin 0600</text></g><g fill="#a9b7cb" font-size="12" text-anchor="middle"><text x="129" y="122">identity: order-api</text><text x="424" y="122">directory traversal checked</text><text fill="#f43f5e" x="764" y="122">DENY · EACCES at file</text></g><g fill="none" marker-end="url(#day6-perm-incident-arrow)" stroke="#38bdf8" stroke-width="2"><path d="M234 106 L288 106"></path><path d="M554 106 L608 106"></path></g><line stroke="#a9b7cb" stroke-dasharray="5 5" x1="24" x2="914" y1="192" y2="192"></line><text fill="#34d399" font-size="15" font-weight="700" x="24" y="226">AFTER · corrected and verified path</text><g fill="#121526" stroke-width="2"><rect height="100" rx="10" stroke="#38bdf8" width="210" x="24" y="247"></rect><image href="../assets/icons/generic/user.svg" x="36" y="259" width="22" height="22" preserveAspectRatio="xMidYMid meet"/><rect height="100" rx="10" stroke="#34d399" width="260" x="294" y="247"></rect><image href="../assets/icons/generic/policy.svg" x="306" y="259" width="22" height="22" preserveAspectRatio="xMidYMid meet"/><rect height="100" rx="10" stroke="#34d399" width="300" x="614" y="247"></rect><image href="../assets/icons/generic/outcome.svg" x="626" y="259" width="22" height="22" preserveAspectRatio="xMidYMid meet"/></g><g fill="#fce7f3" font-size="14" font-weight="700" text-anchor="middle"><text x="139" y="279">Order API</text><text x="434" y="279">restricted order-api group</text><text x="774" y="279">config.json · root:order-api 0640</text></g><g fill="#a9b7cb" font-size="12" text-anchor="middle"><text x="129" y="313">test as service identity</text><text x="424" y="313">directory search granted</text><text x="764" y="313">ALLOW · file read only</text></g><g fill="none" marker-end="url(#day6-perm-incident-arrow)" stroke="#38bdf8" stroke-width="2"><path d="M234 297 L288 297"></path><path d="M554 297 L608 297"></path></g><text fill="#a9b7cb" font-size="12" text-anchor="middle" x="470" y="378">Verification ends at a controlled read as order-api; application readiness is checked separately.</text></svg><figcaption>Figure 6.3: Supplied incident example. The before row shows the asserted identity mismatch; the after row shows one least-privilege repair and its verification boundary. Scope is limited to POSIX mode bits and directory search rights; the diagram does not prove that extended ACLs, SELinux contexts, or mount options permit access. Actual ownership and ACL choices must follow the host deployment policy.</figcaption></figure>'''

FIG_6_4_HTML = '''<figure class="diagram-figure"><p class="diagram-scroll-hint">Swipe horizontally to view the full incident diagram.</p><svg aria-labelledby="day6-worker-incident-title day6-worker-incident-desc" role="img" viewbox="0 0 940 430" xmlns="http://www.w3.org/2000/svg"><title id="day6-worker-incident-title">Fulfillment replay incident before and after idempotency repair</title><desc id="day6-worker-incident-desc">Before repair, worker A performs fulfillment and is killed before recording completion, so replay to worker B causes a second fulfillment. After repair, the worker claims a durable event key before the effect, passes that key to the fulfillment boundary, and makes replay wait or return the stored outcome.</desc><defs><marker id="day6-worker-incident-arrow" markerheight="8" markerwidth="10" orient="auto" refx="9" refy="4"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"></path></marker></defs><text fill="#f43f5e" font-size="15" font-weight="700" x="22" y="33">BEFORE · duplicate side effect</text><g fill="#121526" stroke-width="2"><rect height="106" rx="10" stroke="#38bdf8" width="180" x="22" y="52"></rect><image href="../assets/icons/generic/event.svg" x="34" y="64" width="22" height="22" preserveAspectRatio="xMidYMid meet"/><rect height="106" rx="10" stroke="#f43f5e" width="180" x="250" y="52"></rect><image href="../assets/icons/generic/server.svg" x="262" y="64" width="22" height="22" preserveAspectRatio="xMidYMid meet"/><rect height="106" rx="10" stroke="#f43f5e" width="180" x="478" y="52"></rect><image href="../assets/icons/generic/queue.svg" x="490" y="64" width="22" height="22" preserveAspectRatio="xMidYMid meet"/><rect height="106" rx="10" stroke="#f43f5e" width="212" x="706" y="52"></rect><image href="../assets/icons/generic/failure.svg" x="718" y="64" width="22" height="22" preserveAspectRatio="xMidYMid meet"/></g><g fill="#fce7f3" font-size="14" font-weight="700" text-anchor="middle"><text x="122" y="84">Event E-481</text><text x="350" y="84">Worker A</text><text x="578" y="84">Broker replay</text><text x="822" y="84">Worker B</text></g><g fill="#a9b7cb" font-size="12" text-anchor="middle"><text x="112" y="118">delivery 1</text><text x="340" y="114">fulfill, then SIGKILL</text><text x="340" y="136">no completion record</text><text x="568" y="118">delivery 2 · same key</text><text fill="#f43f5e" x="812" y="114">fulfills again</text><text x="812" y="136">DUPLICATE</text></g><g fill="none" marker-end="url(#day6-worker-incident-arrow)" stroke="#38bdf8" stroke-width="2"><path d="M202 105 L244 105"></path><path d="M430 105 L472 105"></path><path d="M658 105 L700 105"></path></g><line stroke="#a9b7cb" stroke-dasharray="5 5" x1="22" x2="918" y1="194" y2="194"></line><text fill="#34d399" font-size="15" font-weight="700" x="22" y="228">AFTER · one durable business decision</text><g fill="#121526" stroke-width="2"><rect height="112" rx="10" stroke="#38bdf8" width="180" x="22" y="248"></rect><image href="../assets/icons/generic/event.svg" x="34" y="260" width="22" height="22" preserveAspectRatio="xMidYMid meet"/><rect height="112" rx="10" stroke="#34d399" width="180" x="250" y="248"></rect><image href="../assets/icons/generic/database.svg" x="262" y="260" width="22" height="22" preserveAspectRatio="xMidYMid meet"/><rect height="112" rx="10" stroke="#34d399" width="180" x="478" y="248"></rect><image href="../assets/icons/generic/server.svg" x="490" y="260" width="22" height="22" preserveAspectRatio="xMidYMid meet"/><rect height="112" rx="10" stroke="#34d399" width="212" x="706" y="248"></rect><image href="../assets/icons/generic/outcome.svg" x="718" y="260" width="22" height="22" preserveAspectRatio="xMidYMid meet"/></g><g fill="#fce7f3" font-size="14" font-weight="700" text-anchor="middle"><text x="122" y="281">Event E-481</text><text x="350" y="281">Idempotency store</text><text x="578" y="281">Fulfillment</text><text x="822" y="281">Replay E-481</text></g><g fill="#a9b7cb" font-size="12" text-anchor="middle"><text x="112" y="316">stable event key</text><text x="340" y="312">claim key before effect</text><text x="340" y="334">processing → done</text><text x="568" y="316">use the same key once</text><text x="812" y="312">key claimed or done</text><text x="812" y="334">wait or stored result</text></g><g fill="none" marker-end="url(#day6-worker-incident-arrow)" stroke="#38bdf8" stroke-width="2"><path d="M202 304 L244 304"></path><path d="M430 304 L472 304"></path><path d="M658 304 L700 304"></path></g><text fill="#a9b7cb" font-size="12" text-anchor="middle" x="470" y="400">Verification injects the same key twice and observes one committed fulfillment record.</text></svg><figcaption>Figure 6.4: Supplied incident example. The first row shows how termination between a side effect and its record enables a duplicate; the corrected row shows a stable-key state machine. Scope is limited to worker termination and message redelivery; the downstream fulfillment boundary must honor the same key, and the diagram does not prove atomicity in a real store.</figcaption></figure>'''

TOPIC_01_TECH = f'''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ol>
<li>Kernel space versus user space and the system call interface</li>
<li>File system hierarchy, VFS, and path resolution mechanics</li>
<li>POSIX permissions, mode bit octals, and directory search rights</li>
<li>User and group credentials: UID, GID, and supplementary groups</li>
<li>Ownership boundaries, sudo delegation, and least-privilege security</li>
</ol>

<h4>Kernel space versus user space and the system call interface</h4>
<p><strong class="side-heading">What it is in general:</strong> Linux enforces hardware-level CPU privilege rings: Ring 0 hosts the <strong class="keyword">Kernel Space</strong>, with direct, unrestricted execution over CPU registers, virtual memory translation, page tables, interrupts, and physical devices. Ring 3 hosts <strong class="keyword">User Space</strong>, where unprivileged user applications and system daemons execute within isolated virtual address spaces. User-space programs interact with hardware and system resources exclusively through <strong class="keyword">System Calls</strong> (syscalls) such as <code>open()</code>, <code>read()</code>, <code>write()</code>, and <code>fork()</code>, which trigger hardware context switches and trap into the kernel.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects designing compute infrastructure must understand that container engines (e.g., Docker, containerd) share the host Linux kernel; a container is simply an isolated user-space process group governed by cgroups and namespaces. Unlike hypervisor virtual machines with distinct guest kernels, vulnerabilities in the host kernel system call interface can lead to container escape and privilege escalation across multi-tenant workloads.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine instances run dedicated Linux guest kernels inside Google's KVM-based hypervisor. For containerized architectures, Google Kubernetes Engine (GKE) provides GKE Sandbox (using gVisor), which intercepts and virtualizes Linux system calls in user space to prevent container breakouts from compromising the node kernel. Primary documentation: <a href="https://man7.org/linux/man-pages/man2/chmod.2.html#DESCRIPTION">chmod(2) Linux manual page description (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man2/chmod.2.html#DESCRIPTION">chmod(2) description and mode bits (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man7/credentials.7.html#DESCRIPTION">credentials(7) process user and group identifiers (accessed 2026-10-04)</a>.</p>

<h4>File system hierarchy, VFS, and path resolution mechanics</h4>
<p><strong class="side-heading">What it is in general:</strong> Linux structures all stored entities into a single, unified hierarchical tree rooted at <code>/</code>, adhering to the Filesystem Hierarchy Standard (FHS). The kernel provides the <strong class="keyword">Virtual File System</strong> (VFS) abstraction layer, providing uniform system-call semantics regardless of underlying storage formats (ext4, XFS, tmpfs, NFS, or block-backed persistent disks). When resolving a path like <code>/srv/brightloaf/order-api/config.json</code>, the kernel iteratively looks up each directory component (dentry), verifying read and execute permissions on every parent directory in sequence.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Path resolution failure is a common root cause of deployment failures: even if a file has world-readable mode <code>0644</code>, an unprivileged service account cannot open it if any parent directory (e.g. <code>/srv/brightloaf</code>) lacks the execute (traverse) bit for that user or group. Cloud architects design predictable, standard mount points for persistent volumes and ensure container volume mounts do not mask parent directory permissions.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Persistent Disks and Hyperdisks attached to Compute Engine VMs are formatted with Linux filesystems (typically ext4 or XFS) and mounted into the VFS tree. Architects utilize Google Cloud Filestore (managed NFS) or Cloud Storage FUSE to expose shared network storage into local Linux path hierarchies, requiring strict POSIX path and permission synchronization. Primary documentation: <a href="https://man7.org/linux/man-pages/man2/chmod.2.html#DESCRIPTION">chmod(2) directory search semantics (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man2/chmod.2.html#DESCRIPTION">chmod(2) path resolution description (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man7/credentials.7.html#DESCRIPTION">credentials(7) process file system access (accessed 2026-10-04)</a>.</p>

<h4>POSIX permissions, mode bit octals, and directory search rights</h4>
<p><strong class="side-heading">What it is in general:</strong> Standard Linux file permissions are stored as 12 <strong class="keyword">Mode Bits</strong> in the file inode: 3 special bits (setuid, setgid, sticky) and 9 permission bits divided into three classes: <strong class="keyword">Owner</strong> (User), <strong class="keyword">Group</strong>, and <strong class="keyword">Other</strong> (World). Each class has three permissions: Read (<code>r</code>, 4), Write (<code>w</code>, 2), and Execute (<code>x</code>, 1). Crucially, the execute bit on a directory grants <em>search/traverse</em> rights—the ability to pass through the directory to access children. Without execute permission on a directory, no child files can be accessed regardless of their individual file mode bits.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Granting world-writable (<code>0777</code>) permissions to resolve application startup failures is a catastrophic security anti-pattern that violates enterprise compliance (CIS Benchmarks, PCI-DSS). Architects enforce least-privilege mode bits (e.g. <code>0750</code> for directories, <code>0640</code> for configuration files containing credentials, and <code>0600</code> for private keys) and automate permission linting in CI/CD container image pipelines.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine instance startup scripts and automated provisioning tools (Ansible, Terraform, Cloud-init) must set explicit mode bits during deployment. Compute Engine OS Login automatically creates user home directories with <code>0700</code> or <code>0750</code> permissions to isolate multi-user administrative sessions on shared bastion hosts. Primary documentation: <a href="https://man7.org/linux/man-pages/man2/chmod.2.html#DESCRIPTION">chmod(2) POSIX permission bits (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man2/chmod.2.html#DESCRIPTION">chmod(2) mode bit definitions (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man7/credentials.7.html#DESCRIPTION">credentials(7) access control mechanisms (accessed 2026-10-04)</a>.</p>

<h4>User and group credentials: UID, GID, and supplementary groups</h4>
<p><strong class="side-heading">What it is in general:</strong> Every Linux process executes under a set of kernel credentials: a Real User ID (RUID), an <strong class="keyword">Effective User ID</strong> (EUID) used for permission checks, a Real Group ID (RGID), an Effective Group ID (EGID), and an array of <strong class="keyword">Supplementary Groups</strong>. When a process issues an <code>open()</code> system call, the kernel evaluates credentials in strict priority: (1) If process EUID matches file owner UID, owner bits apply; (2) Else if process EGID or any supplementary GID matches file GID, group bits apply; (3) Otherwise, other bits apply. Evaluation stops at the first matching class—if the user matches the owner class and owner bits deny read, group bits are never checked.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Service accounts running microservices must never execute as UID 0 (root). Architects establish dedicated non-login system accounts (e.g. UID 10001, shell <code>/sbin/nologin</code>) and assign supplementary group memberships to grant access to shared configuration or unix sockets, ensuring isolation between distinct microservice daemons on the same virtual host.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud OS Login maps Cloud IAM identities directly to POSIX UIDs and GIDs on Linux VMs. Administrators configure POSIX group membership in Google Workspace or Cloud Identity, allowing seamless role-based access control across fleets of Compute Engine instances without managing local <code>/etc/passwd</code> files. Primary documentation: <a href="https://man7.org/linux/man-pages/man7/credentials.7.html#DESCRIPTION">credentials(7) process credentials and group lists (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man7/credentials.7.html#DESCRIPTION">credentials(7) effective UID and supplementary groups (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man2/chmod.2.html#DESCRIPTION">chmod(2) permission checking order (accessed 2026-10-04)</a>.</p>

<h4>Ownership boundaries, sudo delegation, and least-privilege security</h4>
<p><strong class="side-heading">What it is in general:</strong> Linux file ownership is established by the file's UID and GID, modified via the <code>chown</code> and <code>chgrp</code> system calls (restricted to root). To perform privileged maintenance, Linux systems employ <strong class="keyword">sudo</strong> (superuser do) to temporarily elevate privileges based on rules defined in <code>/etc/sudoers</code>. Sudo delegation allows operators to execute specific commands as root or as service identities without sharing the root password or granting unbounded shell access.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects mandate least privilege by restricting sudo permissions to specific immutable administrative binaries and prohibiting interactive root shells (<kbd>sudo su -</kbd>). Auditing sudo execution via systemd journals and centralized security SIEMs provides tamper-evident logs for SOC2 and ISO 27001 compliance.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud Compute Engine, IAM roles dictate sudo access: users with <code>roles/compute.osAdminLogin</code> are granted passwordless sudo privileges via OS Login PAM configurations, whereas users with <code>roles/compute.osLogin</code> receive standard unprivileged user shells. This decouples cloud IAM administration from local VM credential management. Primary documentation: <a href="https://man7.org/linux/man-pages/man7/credentials.7.html#DESCRIPTION">credentials(7) privilege boundaries (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man7/credentials.7.html#DESCRIPTION">credentials(7) set-user-ID and capability boundaries (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man2/chmod.2.html#DESCRIPTION">chmod(2) ownership and permissions (accessed 2026-10-04)</a>.</p>

<table><caption>File access decision path</caption>
<thead><tr><th>Stage</th><th>Owner</th><th>Evidence</th><th>Limit</th></tr></thead>
<tbody>
<tr><td>Process identity</td><td>Kernel credentials</td><td>Effective UID, GID and supplementary groups</td><td>A username alone does not show every group.</td></tr>
<tr><td>Path resolution</td><td>Kernel VFS and filesystem</td><td>Every directory component exists and is searchable</td><td>Readable file bits cannot repair a blocked parent path.</td></tr>
<tr><td>Mode selection</td><td>File owner and administrator</td><td>Owner, group or other permission class</td><td>Only one class supplies the ordinary mode bits for a check.</td></tr>
<tr><td>Additional controls</td><td>Host security policy</td><td>ACLs, mount state and security-module evidence</td><td>Mode bits are not the complete policy on every host.</td></tr>
</tbody></table>

{FIG_6_1_HTML}

<p><strong class="side-heading">Concrete example:</strong> An automated deployment pipeline copies an application configuration file to <code>/srv/brightloaf/order-api/config.json</code> under the administrative deployment user identity <code>deploy-admin:deploy-admin</code> with mode <code>0600</code> (read/write only for owner). When the systemd service starts, it drops privileges to execute under the dedicated service user <code>order-api</code> (UID 10001, GID 10001). The service attempts to open <code>config.json</code> for reading. The kernel checks process EUID (10001) against file owner UID (10000); they mismatch. The kernel checks process EGID (10001) against file GID (10000); they mismatch. The kernel evaluates the "other" permission class, which is <code>0</code> (no access). The kernel halts the system call and returns <code>EACCES</code> (Permission denied). To remediate without granting world-readable access, the administrator changes group ownership to <code>order-api</code> and sets mode <code>0640</code> (owner read/write, group read, other none), restoring access for the service while protecting credentials from other local accounts.</p>
<p><strong class="side-heading">Evidence limit:</strong> A successful permission check at the file inode verifies only that the process credentials satisfy standard POSIX mode bits; it does not prove that extended filesystem ACLs (facl), SELinux/AppArmor security contexts, read-only filesystem mount flags, or disk quota limits permit the operation.</p>'''

TOPIC_02_TECH = f'''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ol>
<li>Process creation, memory address space, and PID lifecycle</li>
<li>Standard file descriptors (0, 1, 2), pipelines, and I/O redirection</li>
<li>Boot-to-service sequence and systemd unit dependency graph</li>
<li>Signal handling: graceful shutdown (SIGTERM) versus immediate kill (SIGKILL)</li>
<li>Exit codes, wait status, and journal logging with journalctl</li>
</ol>

<h4>Process creation, memory address space, and PID lifecycle</h4>
<p><strong class="side-heading">What it is in general:</strong> A <strong class="keyword">Process</strong> is an executing instance of a program, encapsulating an isolated virtual memory address space (code, data, heap, stack), a set of file descriptors, and kernel execution state. In Linux, new processes are created via the <code>fork()</code> (or <code>clone()</code>) system call, creating a child process that inherits memory pages with copy-on-write (COW) semantics. The child typically invokes <code>execve()</code> to replace its address space with a new executable. Each process receives a unique integer <strong class="keyword">Process ID</strong> (PID) allocated by the kernel, managed under PID 1 (systemd or init), which adopts orphaned processes and reaps terminating zombie processes.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Understanding the process lifecycle is foundational for container and VM architecture. In container environments, PID 1 inside the container namespace must properly forward signals to child processes and reap zombie processes to prevent PID exhaustion. Furthermore, architects size memory limits based on process resident set size (RSS) rather than virtual memory size (VMS) to prevent kernel Out-Of-Memory (OOM) killer terminations.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine virtual machines run systemd as PID 1 to supervise core cloud agents, including the Google Cloud Guest Agent, OS Config Agent, and Google Cloud Ops Agent. On Cloud Run and GKE, application containers run as PID 1, requiring architects to configure proper signal handling for SIGTERM within container entrypoints. Primary documentation: <a href="https://man7.org/linux/man-pages/man5/systemd.service.5.html#DESCRIPTION">systemd.service(5) Linux manual page description (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man5/systemd.service.5.html#DESCRIPTION">systemd.service(5) service process execution (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man7/signal.7.html#DESCRIPTION">signal(7) signal overview and handlers (accessed 2026-10-04)</a>.</p>

<h4>Standard file descriptors (0, 1, 2), pipelines, and I/O redirection</h4>
<p><strong class="side-heading">What it is in general:</strong> When a Linux process initializes, the kernel provides three default <strong class="keyword">File Descriptors</strong> (FDs): <code>0</code> (Standard Input, <em>stdin</em>), <code>1</code> (Standard Output, <em>stdout</em>), and <code>2</code> (Standard Error, <em>stderr</em>). Through <strong class="keyword">Pipelines</strong> (<code>|</code>), the shell connects the stdout of one process to the stdin of another via a unidirectional kernel pipe buffer. Through <strong class="keyword">I/O Redirection</strong> (<code>></code>, <code>>></code>, <code>2>&1</code>), stdout and stderr streams can be redirected to disk files, special character devices (like <code>/dev/null</code>), or Unix domain sockets.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud observability relies on standard stream hygiene: Twelve-Factor Application design mandates that microservices write all diagnostic logs directly to stdout and stderr rather than internal rotating log files. This decouples the application from local disk storage and enables cloud container runtimes and logging agents to aggregate, parse, and forward log streams centrally.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud GKE, Cloud Run, and Compute Engine (via Ops Agent), all bytes written to stdout (fd 1) and stderr (fd 2) are automatically ingested into Google Cloud Logging as structured log entries, with stderr mapped to ERROR severity and stdout mapped to INFO severity. Primary documentation: <a href="https://man7.org/linux/man-pages/man1/journalctl.1.html#DESCRIPTION">journalctl(1) journal stream collection (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man1/journalctl.1.html#DESCRIPTION">journalctl(1) log collection and stdout/stderr capture (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man5/systemd.service.5.html#DESCRIPTION">systemd.service(5) standard output configuration (accessed 2026-10-04)</a>.</p>

<h4>Boot-to-service sequence and systemd unit dependency graph</h4>
<p><strong class="side-heading">What it is in general:</strong> When a Linux virtual machine boots, the kernel mounts the root filesystem and executes PID 1 (<strong class="keyword">systemd</strong>). Systemd organizes services, mount points, sockets, and targets into declarative <strong class="keyword">Unit Files</strong>. Units declare dependencies using directives like <code>Wants=</code>, <code>Requires=</code>, <code>After=</code>, and <code>Before=</code>, compiling an asynchronous directed acyclic graph (DAG) to parallelize service startup while honoring strict ordering requirements (e.g. ensuring <code>network-online.target</code> is reached before launching network daemons).</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Improperly ordered unit dependencies cause sporadic startup failures: if an application service starts before the cloud metadata server or network stack is fully initialized, API credential retrieval fails. Cloud architects author declarative systemd units with explicit retry policies (<code>Restart=on-failure</code>, <code>RestartSec=5s</code>) to ensure resilient recovery during VM reboots or transient infrastructure faults.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine instance templates utilize custom systemd units in startup scripts or golden images to manage application lifecycle. GCP integrates guest shutdown scripts by configuring systemd units ordered before <code>shutdown.target</code>, ensuring graceful teardown during preemptible VM or spot instance termination events. Primary documentation: <a href="https://man7.org/linux/man-pages/man5/systemd.service.5.html#DESCRIPTION">systemd.service(5) unit dependencies and ordering (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man5/systemd.service.5.html#DESCRIPTION">systemd.service(5) service restart policies and targets (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man1/journalctl.1.html#DESCRIPTION">journalctl(1) unit filtering (accessed 2026-10-04)</a>.</p>

<h4>Signal handling: graceful shutdown (SIGTERM) versus immediate kill (SIGKILL)</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Signals</strong> are asynchronous notifications sent by the kernel to a process to notify it of system events. Standard termination proceeds via <strong class="keyword">SIGTERM</strong> (Signal 15): the process can intercept SIGTERM with a custom signal handler, allowing it to stop accepting new requests, drain active database transactions, flush write buffers, remove lockfiles, and exit cleanly. In contrast, <strong class="keyword">SIGKILL</strong> (Signal 9) cannot be caught, blocked, or ignored: the kernel immediately purges the process address space and reclaims resources without allowing any application cleanup.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud platforms frequently terminate processes: rolling container deployments, VM live migrations, spot instance preemptions, and autoscaling scale-downs all trigger process teardown. If microservices do not handle SIGTERM gracefully within the cloud provider's grace period (e.g. 30 seconds on GKE/Cloud Run), the platform issues SIGKILL, truncating active user requests and causing data corruption or duplicate message processing.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> When GKE drains a node or scales down a deployment, it sends SIGTERM to the container, waits for the configured <code>terminationGracePeriodSeconds</code> (default 30s), and sends SIGKILL if the process has not exited. Similarly, Compute Engine Spot VMs receive a preemption notice 30 seconds before termination, allowing systemd services to execute graceful shutdown handlers. Primary documentation: <a href="https://man7.org/linux/man-pages/man7/signal.7.html#DESCRIPTION">signal(7) standard signals and termination semantics (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man7/signal.7.html#DESCRIPTION">signal(7) disposition and actions (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man5/systemd.service.5.html#DESCRIPTION">systemd.service(5) TimeoutStopSec and kill modes (accessed 2026-10-04)</a>.</p>

<h4>Exit codes, wait status, and journal logging with journalctl</h4>
<p><strong class="side-heading">What it is in general:</strong> When a process terminates, it delivers an 8-bit <strong class="keyword">Exit Status</strong> (0–255) to its parent via the <code>wait()</code> system call. By convention, exit code <code>0</code> signifies successful completion, while non-zero codes indicate errors (e.g. <code>1</code> for general error, <code>126</code> for command invoked cannot execute, <code>127</code> for command not found). When a process is killed by an unhandled signal, the shell exit code is <code>128 + signal_number</code> (e.g. <code>143</code> for SIGTERM [128+15], <code>137</code> for SIGKILL [128+9]). Systemd captures stdout/stderr and termination wait statuses in the binary system journal, queried via <strong class="keyword">journalctl</strong>.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Diagnosing distributed system outages requires correlating exit codes and timestamps: an exit code of 137 in Kubernetes or Cloud Run immediately indicates an OOM kill or SIGKILL deadline expiration. Architects leverage centralized structured logging to alert on non-zero exit codes and capture diagnostic traces across large VM fleets.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> The Google Cloud Ops Agent continuously ingests systemd journald logs from Linux VMs into Cloud Logging, allowing operators to filter logs by systemd unit (<code>_SYSTEMD_UNIT=order-api.service</code>) and correlate process exit statuses with host CPU and memory metrics in Cloud Monitoring. Primary documentation: <a href="https://man7.org/linux/man-pages/man1/journalctl.1.html#DESCRIPTION">journalctl(1) journal querying and filtering (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man1/journalctl.1.html#DESCRIPTION">journalctl(1) timestamp and unit options (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man5/systemd.service.5.html#DESCRIPTION">systemd.service(5) SuccessExitStatus configuration (accessed 2026-10-04)</a>.</p>

<table><caption>Service lifecycle evidence</caption>
<thead><tr><th>Layer</th><th>Control or stream</th><th>Useful evidence</th><th>What it does not prove</th></tr></thead>
<tbody>
<tr><td>Shell</td><td>Pipeline, redirection, exit status</td><td>Command status and captured bytes</td><td>Business success.</td></tr>
<tr><td>Kernel</td><td>PID, file descriptors, signal delivery</td><td>Process state and wait status</td><td>That cleanup completed.</td></tr>
<tr><td>Application</td><td>SIGTERM handler and durable commit</td><td>Timestamped cleanup and commit logs</td><td>That replay is harmless without a dedupe record.</td></tr>
<tr><td>Service manager</td><td>Unit dependencies and restart policy</td><td>Active state, main PID and journal</td><td>That every request finished.</td></tr>
</tbody></table>

{FIG_6_2_HTML}

<p><strong class="side-heading">Concrete example:</strong> An asynchronous background worker service processes orders from a queue. When an administrator initiates a rolling deployment, systemd sends SIGTERM to the worker process (PID 4821). The worker's SIGTERM signal handler intercepts the signal, completes the in-flight order transaction, flushes log entries to stdout (fd 1), writes a durable commit record to database storage, and exits cleanly with exit code 0 within 4 seconds. The systemd journal records the timestamped shutdown sequence. Contrastingly, if an administrator executes <code>kill -9 4821</code> (SIGKILL), the kernel abruptly terminates the process: in-flight database transactions abort, uncommitted queue messages remain unacknowledged, and the process exits with status 137, triggering message redelivery and duplicate fulfillment unless guarded by an idempotency key.</p>
<p><strong class="side-heading">Evidence limit:</strong> A process exit status of 0 in systemd or journalctl proves only that the process terminated without reporting an error to the kernel; it does not prove that external database commits succeeded, that downstream network calls completed, or that queue message acknowledgments reached the message broker.</p>'''

PART1_HTML = '''<article class="topic-card overview" id="topic-01-overview">
<h3>Linux kernel vs user space, file system navigation, permissions (chmod, chown), users and…</h3>
<p><strong class="keyword">Linux permissions</strong> enforce mandatory access control boundaries between unprivileged user-space processes and protected kernel resources. Path traversal requires search rights on every parent directory, and process credentials determine mode bit selection before files can be opened.</p>
<p><strong class="side-heading">Why today:</strong> Establishes the foundational host security and access control boundaries governing application processes, container runtimes, and local configuration files.</p>
<p><strong class="side-heading">Where it sits:</strong> Sits at the base of local host operating system management, establishing directory and credential constraints before supervising background processes.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A deployed order processing daemon crashes on startup with an EACCES permission denied error while reading its configuration file. Investigation reveals that the file was created by an administrative deployer with owner-only read permissions, preventing the unprivileged service user from accessing the configuration.</p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>Processes, file descriptors (stdin/stdout/stderr), pipes, redirection, boot-to-service…</h3>
<p><strong class="keyword">Process supervision</strong> governs the execution, I/O streams, and lifecycle transitions of operating system services from initialization to shutdown. Systemd orchestrates unit dependency graphs, tracks process IDs, captures standard streams into system journals, and manages graceful termination via signals.</p>
<p><strong class="side-heading">Why today:</strong> Provides the execution runtime and operational observability model underpinning virtual machine daemons, background workers, and containerized microservices.</p>
<p><strong class="side-heading">Where it sits:</strong> Operates on top of filesystem permissions to govern active daemon execution, directly producing the service lifecycle timestamps required for exit evidence.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> An order fulfillment worker restarted during a deployment generates duplicate customer shipments for in-flight queue messages. A forced SIGKILL termination interrupted the worker after shipping the goods but before committing completion state, causing the message broker to redeliver the unacknowledged event to a replacement instance.</p>
</article>'''

ARCH_DIAGRAM = {}

DATA = {
    'contract_version': 2,
    'roadmap_practice': 'Start and stop a disposable local service, inspect its PID and journal, and compare a graceful stop with a forced termination.',
    'roadmap_exit': 'Commands, exit codes and log timestamps explaining the service lifecycle.',
    'day': 6,
    'work_block': 'Days 1–17 — Foundations',
    'part1_html': PART1_HTML,
    'part1_intro': 'Day 6 explores core operating system concepts, process execution mechanics, POSIX permission boundaries, and systemd service management.',
    'part2_intro': 'Analyze kernel and user space separation, file access resolution, process file descriptors, and graceful signal termination.',
    'part3_intro': 'Investigate operational incident cases demonstrating permission-denied startup failures and ungraceful termination leading to duplicate message processing.',
    'part4_intro': 'Execute structured hands-on laboratories inspecting POSIX file mode bits, controlling disposable background services, and comparing SIGTERM vs SIGKILL.',
    'exit_summary': 'Commands, exit codes and log timestamps explaining the service lifecycle, distinguishing graceful drain from immediate termination.',
    'completion_html': '''<div class="completion-box" id="completion-box-006">
<h3>Day 6 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-6-1"> <label for="check-6-1">Kernel vs user space mastered: system call boundaries, VFS path traversal, and POSIX permission bit evaluation (UID, GID, octal modes).</label></li>
<li><input type="checkbox" id="check-6-2"> <label for="check-6-2">Process management mastered: standard file descriptors (0, 1, 2), process groups, PID 1 responsibility, and systemd unit dependency graphs.</label></li>
<li><input type="checkbox" id="check-6-3"> <label for="check-6-3">Signal lifecycle mastered: SIGTERM graceful shutdown handling vs SIGKILL immediate termination, exit code calculation (128+N), and journalctl query filtering.</label></li>
<li><input type="checkbox" id="check-6-4"> <label for="check-6-4">Practice completed: started and stopped a disposable local worker, monitored PID and journal output, and contrasted graceful stop (exit 0) with SIGKILL (exit 137).</label></li>
<li><input type="checkbox" id="check-6-5"> <label for="check-6-5">Exit evidence verified: compiled chronological commands, exit codes, and timestamped journal entries demonstrating complete service lifecycle control.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-006" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 6 Completed':'Mark Day 6 as Read';">Mark Day 6 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-006" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>''',
    'arch_diagram': ARCH_DIAGRAM,
    'arch_svg_html': '',
    'arch_table_html': '',
    'lab_defaults': {},
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Linux kernel vs user space, file system navigation, permissions (chmod, chown), users and…',
            'anchors': {
                'overview': 'topic-01-overview',
                'technical': 'topic-01-technical',
                'problem': 'topic-01-problem',
                'lab': 'topic-01-lab'
            },
            'overview': 'Linux enforces privilege rings separating user space from kernel space. File access requires execute search permissions on all parent directories, and kernel credential checks evaluate effective UID and GID against inode mode bits.',
            'preview': 'A deployed order processing daemon crashes on startup with an EACCES permission denied error while reading its configuration file. Investigation reveals that the file was created by an administrative deployer with owner-only read permissions, preventing the unprivileged service user from accessing the configuration.',
            'technical': TOPIC_01_TECH,
            'questions': [
                'Why does granting read permission (0644) on a configuration file fail to allow access if a parent directory lacks the execute (0711) bit for the calling user?',
                'In multi-tenant cloud virtual machines, what security vulnerabilities arise from using world-writable permissions (0777) instead of dedicated POSIX group memberships?',
                'How does Google Cloud OS Login translate Cloud IAM permissions into POSIX UID and GID credentials across Linux compute instances?'
            ],
            'reference': 'https://man7.org/linux/man-pages/man2/chmod.2.html#DESCRIPTION',
            'reference_label': 'chmod(2) Linux manual page description (accessed 2026-10-04)',
            'scenario': {
                'scenario': 'Administrator can read; service user receives EACCES',
                'impact': 'Order API service fails to start on virtual machine boot, resulting in service unavailability and blocked checkout processing.',
                'constraints': 'Configuration file contains sensitive database credentials; the service process must execute under an unprivileged service account; world-readable permissions are strictly prohibited.',
                'evidence': f'''**illustrative supplied records**

```text
[Unit Status] order-api.service - Brightloaf Order Processing API
     Loaded: loaded (/etc/systemd/system/order-api.service; enabled; vendor preset: enabled)
     Active: failed (Result: exit-code) since Sun 2026-10-04 08:00:02 UTC; 12s ago
    Process: 3102 ExecStart=/opt/brightloaf/bin/order-api --config /srv/brightloaf/order-api/config.json (code=exited, status=1/FAILURE)
   Main PID: 3102 (code=exited, status=1/FAILURE)

[Journal Output]
Oct 04 08:00:02 gce-prod-app-01 order-api[3102]: [FATAL] Failed to load configuration: open /srv/brightloaf/order-api/config.json: permission denied (errno: EACCES)
Oct 04 08:00:02 gce-prod-app-01 systemd[1]: order-api.service: Main process exited, code=exited, status=1/FAILURE
Oct 04 08:00:02 gce-prod-app-01 systemd[1]: order-api.service: Failed with result 'exit-code'.

[Diagnostic Trace]
$ sudo -u order-api cat /srv/brightloaf/order-api/config.json
cat: /srv/brightloaf/order-api/config.json: Permission denied
$ ls -ld /srv/brightloaf/order-api/config.json
-rw------- 1 deploy-admin deploy-admin 1024 Oct 04 07:55 /srv/brightloaf/order-api/config.json
```

{FIG_6_3_HTML}''',
                'root': 'Permission and ownership mismatch: the configuration file /srv/brightloaf/order-api/config.json was deployed with ownership deploy-admin:deploy-admin and octal mode 0600 (owner read/write only). The order-api systemd service executes under User=order-api and Group=order-api, which matches neither the owner nor group classes, causing the kernel to evaluate the "other" class (mode 0) and reject the open() system call with EACCES.',
                'diagnostic_steps': [
                    'Inspect systemd unit configuration to determine the configured User= and Group= attributes.',
                    'Check file ownership and octal permissions using stat or ls -l on the target configuration file.',
                    'Use namei -l /srv/brightloaf/order-api/config.json to verify search permissions on every directory component in the path.',
                    'Test file readability under the target service user context using sudo -u order-api test -r <file>.'
                ],
                'remediation_steps': [
                    'Change group ownership of the configuration file to the order-api service group: chgrp order-api /srv/brightloaf/order-api/config.json.',
                    'Set mode bits to 0640 (owner read/write, group read, other none): chmod 0640 /srv/brightloaf/order-api/config.json.',
                    'Ensure parent directories have at least mode 0750 with group ownership order-api to grant search traverse rights.',
                    'Restart the service and confirm clean active state: systemctl restart order-api.service.'
                ],
                'verify': 'Running sudo -u order-api cat /srv/brightloaf/order-api/config.json succeeds; order-api.service starts cleanly with status active (running) and main PID logged.',
                'residual': 'Automated deployment pipelines running under deployment agent identities may recreate files with default umask settings, reverting group permissions unless enforced by directory setgid bits or CI/CD deployment scripts.',
                'diagram_enabled': True,
                'diagram': (
                    'Service process startup',
                    'File ownership set to deploy-admin 0600',
                    'EACCES permission denied error',
                    'Change group to order-api mode 0640',
                    'Clean startup and verified read'
                ),
                'icons': [
                    '../assets/icons/generic/event.svg',
                    '../assets/icons/generic/failure.svg',
                    '../assets/icons/generic/failure.svg',
                    '../assets/icons/generic/policy.svg',
                    '../assets/icons/generic/outcome.svg'
                ],
                'facts': 'Supplied incident records: systemd unit failed with status 1/FAILURE; journal logs confirm EACCES on config.json; ls -l shows deploy-admin:deploy-admin 0600.',
                'inference': 'Architectural inference: process credentials determine which permission class applies; owner-only permissions block unprivileged service daemons regardless of parent directory search rights.',
                'expected': 'Expected post-fix behavior: service user order-api successfully opens config.json via group read permission 0640, and service reports active (running).'
            },
            'lab': {
                'name': 'Lab 6.1: Inspect Linux file access controls, user credentials, and permission boundaries',
                'goal': 'Demonstrate file permission evaluation, user and group credential switching, and directory search execution without root privilege escalation.',
                'mode': 'Observed locally: local bash commands execute chmod, chown, stat, and file access tests under isolated test identities. Simulated or predicted: simulated daemon identity switching and permission resolution. Untested on GCP: Compute Engine OS Login PAM module integration, Cloud IAM role translation to POSIX groups, and SELinux/AppArmor mandatory access control enforcement.',
                'covers': 'Start and stop a disposable local service, inspect its PID and journal, and compare a graceful stop with a forced termination (user space credentials and directory permissions)',
                'prereq': 'Python 3.10+, bash shell, coreutils.',
                'preflight': 'Validate python3 and stat command availability, initialize isolated workspace.',
                'verification': 'Inspect file permission evaluation logs and confirm that mode 0640 allows read access while 0600 returns EACCES.',
                'trouble': 'Check directory traverse execute bits (0755 vs 0700) using python os.access checks.',
                'cleanup': 'Delete temporary directory tree and reset environment.',
                'accept': 'The permission evaluator confirms that unprivileged identities are blocked when owner-only mode 0600 is set, and verifies that group read mode 0640 successfully allows reading.',
                'file': 'day-006-topic-01.md',
                'steps': [
                    '''**Stage 1: Preflight environment and tool validation**

**Location:** local bash terminal

Verify required core utilities are available:

```bash
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required"; exit 1; }
command -v stat >/dev/null 2>&1 || { echo "stat utility is required"; exit 1; }
LAB_DIR=$(mktemp -d /tmp/lab_perm.XXXXXX)
export LAB_DIR
cd "$LAB_DIR"
echo "Lab workspace initialized at: $LAB_DIR"
```

**Expected result:** Tools verified, temporary workspace created.

**Save:** `$LAB_DIR/preflight.log`''',

                    '''**Stage 2: Prepare test directory hierarchy and simulated credentials**

**Location:** local bash terminal

Build a multi-level directory hierarchy representing an enterprise deployment:

```bash
mkdir -p "$LAB_DIR/srv/brightloaf/order-api"
cat > "$LAB_DIR/srv/brightloaf/order-api/config.json" <<'EOF'
{
  "database_url": "postgres://order_user:secret_pass@10.50.4.8:5432/orders",
  "log_level": "INFO",
  "port": 8080
}
EOF
chmod 0755 "$LAB_DIR/srv"
chmod 0755 "$LAB_DIR/srv/brightloaf"
chmod 0755 "$LAB_DIR/srv/brightloaf/order-api"
chmod 0600 "$LAB_DIR/srv/brightloaf/order-api/config.json"
stat -c "Path: %n | Mode: %a | User: %U(%u) | Group: %G(%g)" "$LAB_DIR/srv/brightloaf/order-api/config.json"
```

**Expected result:** Directory tree created with config.json mode set to 0600.

**Save:** `$LAB_DIR/initial_stat.log`''',

                    '''**Stage 3: Author plan and permission resolution evaluator**

**Location:** local bash terminal

Create a Python script that models the kernel credential evaluation algorithm:

```bash
cat > "$LAB_DIR/eval_perm.py" <<'EOF'
import os
import stat
import sys

config_path = sys.argv[1]
caller_uid = int(sys.argv[2])
caller_gids = [int(g) for g in sys.argv[3].split(',')]

st = os.stat(config_path)
file_uid = st.st_uid
file_gid = st.st_gid
mode = st.st_mode

# Kernel permission evaluation order:
# 1. Owner class check
if caller_uid == file_uid:
    readable = bool(mode & stat.S_IRUSR)
    matched_class = "Owner (User)"
# 2. Group class check
elif file_gid in caller_gids:
    readable = bool(mode & stat.S_IRGRP)
    matched_class = "Group"
# 3. Other class check
else:
    readable = bool(mode & stat.S_IROTH)
    matched_class = "Other"

print(f"File: {config_path}")
print(f"Mode: {oct(stat.S_IMODE(mode))} | File UID={file_uid} GID={file_gid}")
print(f"Caller: UID={caller_uid} GIDs={caller_gids} => Matched Class: {matched_class}")
if readable:
    print("Outcome: ALLOW (Read granted)")
else:
    print("Outcome: DENY (EACCES: Permission denied)")
EOF
python3 -m py_compile "$LAB_DIR/eval_perm.py"
```

**Expected result:** Permission evaluation engine authored and compiled.

**Save:** `$LAB_DIR/eval_perm.py`''',

                    '''**Stage 4: Execute permission check under service identity**

**Location:** local bash terminal

Simulate the service process running with UID 10001 and GID 10001 against mode 0600:

```bash
cd "$LAB_DIR"
CURRENT_UID=$(id -u)
CURRENT_GID=$(id -g)
# Test 1: Service identity (UID 10001, GID 10001)
python3 eval_perm.py "$LAB_DIR/srv/brightloaf/order-api/config.json" 10001 10001 > test_service_denied.log
cat test_service_denied.log
```

**Expected result:** Output reports Matched Class: Other, Outcome: DENY (EACCES).

**Save:** `$LAB_DIR/test_service_denied.log`''',

                    '''**Stage 5: Inspect expected state and verify access failure**

**Location:** local bash terminal

Confirm the EACCES denial is recorded:

```bash
grep "Outcome: DENY (EACCES" "$LAB_DIR/test_service_denied.log" && echo "PASS: EACCES verified"
```

**Expected result:** Grep matches EACCES denial.

**Save:** `$LAB_DIR/denial_evidence.txt`''',

                    '''**Stage 6: Rehearse directory traverse restriction**

**Location:** local bash terminal

Demonstrate that removing the execute bit from a parent directory blocks access:

```bash
chmod 0644 "$LAB_DIR/srv/brightloaf/order-api" # Remove execute bit
python3 -c '
import os, sys
path = sys.argv[1]
try:
    os.listdir(path)
    print("Directory readable")
except PermissionError:
    print("PASS: Cannot traverse directory without execute bit (EACCES)")
' "$LAB_DIR/srv/brightloaf/order-api" | tee "$LAB_DIR/traverse_test.log"
chmod 0755 "$LAB_DIR/srv/brightloaf/order-api" # Restore execute bit
```

**Expected result:** Traverse permission denial observed when execute bit is missing.

**Save:** `$LAB_DIR/traverse_test.log`''',

                    '''**Stage 7: Diagnose evidence and apply least-privilege remediation**

**Location:** local bash terminal

Simulate assigning group ownership to service group 10001 and mode 0640:

```bash
cd "$LAB_DIR"
# Set mode 0640 (owner read/write, group read, other none)
chmod 0640 "$LAB_DIR/srv/brightloaf/order-api/config.json"
CURRENT_UID=$(id -u)
# Test 2: Service identity (UID 10001, member of GID 10001 and CURRENT_GID)
python3 eval_perm.py "$LAB_DIR/srv/brightloaf/order-api/config.json" 10001 "10001,$CURRENT_GID" > test_service_allowed.log
cat test_service_allowed.log
grep "Outcome: ALLOW" test_service_allowed.log && echo "PASS: Access restored via group read"
```

**Expected result:** Output reports Matched Class: Group, Outcome: ALLOW (Read granted).

**Save:** `$LAB_DIR/test_service_allowed.log`''',

                    '''**Stage 8: Clean up and close out local workspace**

**Location:** local bash terminal

Preserve evidence and delete temporary directory:

```bash
cd /tmp
cp "$LAB_DIR/test_service_allowed.log" /tmp/day_006_perm_evidence.log
rm -rf "$LAB_DIR"
echo "Cleaned up workspace. Evidence preserved at: /tmp/day_006_perm_evidence.log"
```

**Expected result:** Temporary directory removed cleanly.

**Save:** `/tmp/day_006_perm_evidence.log`'''
                ]
            }
        },
        {
            'key': 'topic-02',
            'title': 'Processes, file descriptors (stdin/stdout/stderr), pipes, redirection, boot-to-service…',
            'anchors': {
                'overview': 'topic-02-overview',
                'technical': 'topic-02-technical',
                'problem': 'topic-02-problem',
                'lab': 'topic-02-lab'
            },
            'overview': 'Process supervision governs lifecycle execution, standard stream capture, and termination handling. SIGTERM allows graceful transaction completion and resource cleanup, whereas SIGKILL forces immediate termination and exposes uncommitted state.',
            'preview': 'An order fulfillment worker restarted during a deployment generates duplicate customer shipments for in-flight queue messages. A forced SIGKILL termination interrupted the worker after shipping the goods but before committing completion state, causing the message broker to redeliver the unacknowledged event to a replacement instance.',
            'technical': TOPIC_02_TECH,
            'questions': [
                'Why does a forced SIGKILL (kill -9) bypass application cleanup handlers, and what durable mechanisms protect downstream consumers from duplicate side effects?',
                'How does systemd distinguish between a successful service shutdown (exit status 0) and an abnormal termination (status 137 or 143)?',
                'Why must containerized applications running as PID 1 handle SIGTERM signals explicitly, and what happens if the application fails to exit within the termination grace period?'
            ],
            'reference': 'https://man7.org/linux/man-pages/man5/systemd.service.5.html#DESCRIPTION',
            'reference_label': 'systemd.service(5) Linux manual page description (accessed 2026-10-04)',
            'scenario': {
                'scenario': 'Forced worker stop exposes a duplicate-fulfillment defect',
                'impact': 'Warehouse ships physical goods twice for customer orders, causing inventory discrepancy and financial loss during rolling worker deployments.',
                'constraints': 'Worker deployments must complete within a bounded shutdown window; queue message delivery guarantees at-least-once processing; external carrier API calls cannot be undone.',
                'evidence': f'''**illustrative supplied records**

```text
[Message Broker Log]
2026-10-04T08:15:00.102Z INFO  Queue: orders.fulfillment Event: E-481 Delivery: 1 Assigned to: worker-a (PID 4821)
2026-10-04T08:15:00.350Z INFO  Worker-a: Processing order ORD-9921 for event E-481
2026-10-04T08:15:00.820Z INFO  Worker-a: External shipping label generated with carrier: LBL-774102

[Deployment Automation Log]
2026-10-04T08:15:01.000Z WARN  Deployment script: Force killing worker-a (SIGKILL / kill -9 4821)
2026-10-04T08:15:01.005Z INFO  Kernel: Process 4821 terminated by signal 9 (SIGKILL)

[Broker Replay Log]
2026-10-04T08:15:06.000Z WARN  Broker: Worker-a disconnected without ACK for E-481. Re-queuing unacknowledged event.
2026-10-04T08:15:06.150Z INFO  Queue: orders.fulfillment Event: E-481 Delivery: 2 Assigned to: worker-b (PID 5104)
2026-10-04T08:15:06.390Z INFO  Worker-b: Processing order ORD-9921 for event E-481
2026-10-04T08:15:06.850Z INFO  Worker-b: External shipping label generated with carrier: LBL-774103 [DUPLICATE]
```

{FIG_6_4_HTML}''',
                'root': 'Architectural race condition: Worker A performed the external physical fulfillment side effect before recording completion in a shared idempotency database. When the deployment automation issued SIGKILL, Worker A was terminated instantly without executing signal cleanup or acknowledging the message. The message broker redelivered event E-481 to Worker B, which had no durable record that fulfillment had already occurred, resulting in duplicate fulfillment.',
                'diagnostic_steps': [
                    'Correlate systemd journal shutdown timestamps with worker exit codes (exit 137 indicating SIGKILL).',
                    'Inspect message broker consumer acknowledgments to confirm event E-481 was redelivered following ungraceful worker termination.',
                    'Query database commit records to identify whether fulfillment records exist for ORD-9921 prior to the restart.',
                    'Review worker source code to verify signal handler implementation and idempotency store integration.'
                ],
                'remediation_steps': [
                    'Implement a SIGTERM signal handler in the worker to gracefully complete in-flight messages and stop pulling new work.',
                    'Configure systemd TimeoutStopSec=30s to provide sufficient drain time before issuing SIGKILL.',
                    'Introduce an idempotency key store: worker must claim event E-481 in database prior to external carrier API execution, and subsequent deliveries must detect the existing record and skip fulfillment.',
                    'Ensure external fulfillment API calls pass the event ID as an idempotency key to prevent carrier-side duplication.'
                ],
                'verify': 'Simulating a worker restart during message processing shows that Worker A commits the transaction, or if terminated, Worker B queries the idempotency store, detects the existing claim, and logs a duplicate skip without generating a second shipping label.',
                'residual': 'Idempotency records require cleanup policies (TTL); network partitions between the worker and idempotency store during shutdown can still delay message acknowledgement.',
                'diagram_enabled': True,
                'diagram': (
                    'Worker processing event E-481',
                    'SIGKILL before completion recorded',
                    'Broker redelivers event to Worker B',
                    'Enforce SIGTERM drain & idempotency key',
                    'Single fulfillment verified'
                ),
                'icons': [
                    '../assets/icons/generic/event.svg',
                    '../assets/icons/generic/failure.svg',
                    '../assets/icons/generic/failure.svg',
                    '../assets/icons/generic/policy.svg',
                    '../assets/icons/generic/outcome.svg'
                ],
                'facts': 'Supplied incident records: Worker A terminated with signal 9 (SIGKILL); message broker re-queued unacknowledged event E-481; Worker B generated duplicate shipping label LBL-774103.',
                'inference': 'Architectural inference: SIGKILL prevents in-flight cleanup and message acknowledgment; downstream deduplication requires durable idempotency keys across worker restarts.',
                'expected': 'Expected post-fix behavior: worker handles SIGTERM gracefully to complete fulfillment and ACK, or replay detects stable idempotency key to return stored result without re-executing.'
            },
            'lab': {
                'name': 'Lab 6.2: Supervise local process lifecycle, capture exit statuses, and evaluate graceful versus forced termination',
                'goal': 'Run a disposable service process, handle SIGTERM gracefully vs SIGKILL abruptly, inspect process status in procfs, and record exit codes and timestamped logs.',
                'mode': 'Observed locally: local python worker process handles SIGTERM, records cleanup logs, and exits with code 0, contrasted with SIGKILL immediate termination with exit status 137. Simulated or predicted: simulated systemd TimeoutStopSec watchdog timer. Untested on GCP: live systemd system-level service installation requiring root privileges, journald remote forwarding to Cloud Logging, and Compute Engine guest environment agents.',
                'covers': 'Start and stop a disposable local service, inspect its PID and journal, and compare a graceful stop with a forced termination (service lifecycle and signals)',
                'prereq': 'Python 3.10+, bash shell.',
                'preflight': 'Validate python3 availability and create temporary workspace.',
                'verification': 'Review generated lifecycle log file and verify exit status 0 for SIGTERM versus exit status 137 for SIGKILL.',
                'trouble': 'Inspect background process PID via ps or kill -0 before sending termination signals.',
                'cleanup': 'Terminate any residual background processes and remove workspace directory.',
                'accept': 'The lifecycle verification log captures commands, process IDs, timestamped signals, and explicit exit codes (0 for graceful stop, 137 for SIGKILL).',
                'file': 'day-006-topic-02.md',
                'steps': [
                    '''**Stage 1: Preflight environment and tool validation**

**Location:** local bash terminal

Verify that Python 3 is installed:

```bash
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required"; exit 1; }
python3 --version
LAB_DIR=$(mktemp -d /tmp/lab_proc.XXXXXX)
export LAB_DIR
cd "$LAB_DIR"
echo "Lab workspace initialized at: $LAB_DIR"
```

**Expected result:** Python 3 detected, temporary workspace initialized.

**Save:** `$LAB_DIR/preflight.log`''',

                    '''**Stage 2: Prepare worker daemon with SIGTERM signal handler**

**Location:** local bash terminal

Author a Python worker daemon that logs lifecycle events, catches SIGTERM, and handles graceful cleanup:

```bash
cat > "$LAB_DIR/worker_daemon.py" <<'EOF'
import datetime
import os
import signal
import sys
import time

log_file = open("worker.log", "a", buffering=1)

def ts():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sigterm_handler(signum, frame):
    log_file.write(f"[{ts()}] PID {os.getpid()} received SIGTERM (signal {signum})\n")
    log_file.write(f"[{ts()}] PID {os.getpid()} initiating graceful drain: completing in-flight work...\n")
    time.sleep(1.0) # Simulate draining transactions
    log_file.write(f"[{ts()}] PID {os.getpid()} in-flight transactions drained. Committing state...\n")
    log_file.write(f"[{ts()}] PID {os.getpid()} graceful shutdown complete. Exiting with status 0.\n")
    log_file.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

log_file.write(f"[{ts()}] PID {os.getpid()} worker daemon started. Entering event loop...\n")

counter = 0
while True:
    counter += 1
    log_file.write(f"[{ts()}] PID {os.getpid()} heartbeat tick {counter}\n")
    time.sleep(0.5)
EOF
python3 -m py_compile "$LAB_DIR/worker_daemon.py"
```

**Expected result:** Worker daemon script authored and verified.

**Save:** `$LAB_DIR/worker_daemon.py`''',

                    '''**Stage 3: Author plan and lifecycle capture harness**

**Location:** local bash terminal

Create an execution harness that starts the worker, queries procfs, sends signals, and records exit statuses:

```bash
cat > "$LAB_DIR/run_lifecycle_test.sh" <<'EOF'
#!/bin/bash
set -e
cd "$LAB_DIR"

echo "=== TEST 1: GRACEFUL TERMINATION (SIGTERM) ==="
python3 worker_daemon.py &
WORKER_PID=$!
echo "Started worker with PID: $WORKER_PID"
sleep 1.5

# Inspect procfs
if [ -d "/proc/$WORKER_PID" ]; then
    echo "Process verified running in /proc/$WORKER_PID"
fi

# Send SIGTERM
echo "Sending SIGTERM to PID $WORKER_PID..."
kill -15 "$WORKER_PID"

# Wait for process exit and capture status
set +e
wait "$WORKER_PID"
EXIT_CODE=$?
set -e
echo "Worker PID $WORKER_PID exited with code: $EXIT_CODE"

echo ""
echo "=== TEST 2: FORCED TERMINATION (SIGKILL) ==="
python3 worker_daemon.py &
WORKER_PID2=$!
echo "Started worker with PID: $WORKER_PID2"
sleep 1.0

# Send SIGKILL
echo "Sending SIGKILL (kill -9) to PID $WORKER_PID2..."
kill -9 "$WORKER_PID2"

# Wait for process exit and capture status
set +e
wait "$WORKER_PID2"
EXIT_CODE2=$?
set -e
echo "Worker PID $WORKER_PID2 exited with code: $EXIT_CODE2"
EOF
chmod +x "$LAB_DIR/run_lifecycle_test.sh"
```

**Expected result:** Test harness script authored with executable permissions.

**Save:** `$LAB_DIR/run_lifecycle_test.sh`''',

                    '''**Stage 4: Execute lifecycle test suite**

**Location:** local bash terminal

Execute the test suite and capture console output:

```bash
cd "$LAB_DIR"
./run_lifecycle_test.sh | tee "$LAB_DIR/lifecycle_execution.log"
```

**Expected result:** Output displays PID capture, SIGTERM exit code 0, and SIGKILL exit code 137.

**Save:** `$LAB_DIR/lifecycle_execution.log`''',

                    '''**Stage 5: Inspect expected state and verify exit codes**

**Location:** local bash terminal

Verify that SIGTERM yielded exit code 0 and SIGKILL yielded exit code 137:

```bash
grep "Worker PID .* exited with code: 0" "$LAB_DIR/lifecycle_execution.log" && echo "PASS: Graceful exit code 0 confirmed"
grep "Worker PID .* exited with code: 137" "$LAB_DIR/lifecycle_execution.log" && echo "PASS: Forced kill exit code 137 confirmed"
```

**Expected result:** Both exit codes validated against expected lifecycle criteria.

**Save:** `$LAB_DIR/exit_code_validation.txt`''',

                    '''**Stage 6: Rehearse journal and log timestamp inspection**

**Location:** local bash terminal

Inspect the worker log to verify timestamped graceful shutdown records:

```bash
cat "$LAB_DIR/worker.log"
grep "graceful shutdown complete" "$LAB_DIR/worker.log" && echo "PASS: Graceful cleanup logged"
```

**Expected result:** Log confirms graceful shutdown sequence logged prior to termination.

**Save:** `$LAB_DIR/worker.log`''',

                    '''**Stage 7: Diagnose evidence and compile service lifecycle report**

**Location:** local bash terminal

Compile the final service lifecycle report artifact containing commands, exit codes, and timestamps:

```bash
cat > "$LAB_DIR/service_lifecycle_report.md" <<EOF
# Service Lifecycle and Termination Evidence Report

## Summary
- **Target Workload:** Disposable Local Worker Service (worker_daemon.py)
- **Supervision Model:** Shell job control simulating systemd process manager
- **Timestamp:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Termination Comparison Table

| Termination Type | Signal Sent | Process Action | Observed Exit Code | State Integrity |
|---|---|---|---|---|
| **Graceful Stop** | SIGTERM (15) | Intercepted by handler; drained work; flushed logs | **0** (Success) | Clean commit; zero data loss |
| **Forced Kill** | SIGKILL (9) | Kernel immediate termination; no handler execution | **137** (128+9) | Uncommitted state; requires deduplication |

## Execution Log Excerpts
```text
$(cat "$LAB_DIR/lifecycle_execution.log")
```

## Worker Log Excerpts
```text
$(cat "$LAB_DIR/worker.log")
```
EOF
cat "$LAB_DIR/service_lifecycle_report.md"
```

**Expected result:** Comprehensive markdown lifecycle report generated.

**Save:** `$LAB_DIR/service_lifecycle_report.md`''',

                    '''**Stage 8: Clean up and preserve exit artifact**

**Location:** local bash terminal

Preserve the exit evidence artifact and remove temporary workspace:

```bash
cd /tmp
cp "$LAB_DIR/service_lifecycle_report.md" /tmp/day_006_service_lifecycle_report.md
rm -rf "$LAB_DIR"
echo "Cleaned up workspace. Exit artifact preserved at: /tmp/day_006_service_lifecycle_report.md"
```

**Expected result:** Workspace deleted cleanly; final artifact preserved.

**Save:** `/tmp/day_006_service_lifecycle_report.md`'''
                ]
            }
        }
    ]
}

DATA.update(sources=SOURCES, access_date=ACCESS_DATE)
