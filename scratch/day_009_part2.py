"""Part 2 technical discussion for Topic 2: Container isolation: namespaces, cgroups, seccomp and capabilities."""

TOPIC_02_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ol>
<li>Linux Kernel Namespaces (PID, NET, MNT, IPC, UTS, and USER)</li>
<li>Control Groups v2 (cgroups v2) Resource Accounting and Quota Limits</li>
<li>Seccomp (Secure Computing Mode) System Call Filtering and BPF Profiles</li>
<li>POSIX Capabilities and Least-Privilege Process Execution</li>
<li>Defense-in-Depth Container Sandboxing: gVisor, Cloud Run, and GKE Node Isolation</li>
</ol>

<h4>Linux Kernel Namespaces (PID, NET, MNT, IPC, UTS, and USER)</h4>
<p><strong class="side-heading">What it is in general:</strong> A Linux <strong class="keyword">namespace</strong> is a kernel feature that wraps a global system resource in an abstraction such that processes within the namespace see only their own isolated instance of that resource. The Linux kernel provides eight distinct namespaces (documented in <kbd>namespaces(7)</kbd>):
<strong>PID</strong> (Process ID) namespaces isolate process ID numbering, allowing a containerized process to be PID 1 while appearing as an ordinary unprivileged PID on the host;
<strong>NET</strong> (Network) namespaces isolate network devices, IP routing tables, port bindings, and firewall rules via virtual ethernet pairs (<kbd>veth</kbd>);
<strong>MNT</strong> (Mount) namespaces provide isolated filesystem mount points, typically configured via <kbd>pivot_root</kbd> to provide an independent root filesystem;
<strong>IPC</strong> (Inter-Process Communication) namespaces isolate System V IPC objects and POSIX message queues;
<strong>UTS</strong> (UNIX Timesharing) namespaces isolate system hostnames and NIS domain names;
<strong>USER</strong> namespaces map user and group IDs (e.g., UID 0 inside the container maps to an unprivileged UID 100000 on the host);
<strong>CGROUP</strong> namespaces isolate the cgroup hierarchy view; and
<strong>TIME</strong> namespaces isolate clock offsets.
Processes transition or join namespaces via the <kbd>clone()</kbd>, <kbd>unshare()</kbd>, and <kbd>setns()</kbd> system calls, and their active namespaces are reflected as symbolic links under <kbd>/proc/[pid]/ns/</kbd>.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Namespaces establish the illusion of an independent computer for containerized applications, but they do NOT enforce security boundaries or resource quotas. A process in a private PID namespace cannot see neighboring processes, but if an application inside a container exploits a kernel vulnerability (e.g., a buffer overflow in the network stack or filesystem driver), it compromises the shared host kernel directly. Architects must understand that namespaces control visibility, not privilege or resource consumption.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Kubernetes Engine (GKE), Pods are groups of containers that share common namespaces: containers in the same Pod share the same Network namespace (allowing them to communicate over <kbd>localhost</kbd>) and IPC namespace, while maintaining independent Mount namespaces. Cloud Run automatically wraps serverless container instances in dedicated namespaces to ensure customer requests execute in isolated runtime environments on Google-managed infrastructure.</p>

<h4>Control Groups v2 (cgroups v2) Resource Accounting and Quota Limits</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Control Groups v2 (cgroups v2)</strong> is the unified Linux kernel mechanism that partitions, prioritizes, and limits the hardware resource consumption (CPU, memory, I/O, PIDs) of process hierarchies. While cgroups v1 suffered from multiple disjoint hierarchies and broken memory-I/O coordination, cgroups v2 enforces a single unified hierarchy mounted at <kbd>/sys/fs/cgroup</kbd> with strict top-down resource distribution. Resource allocation is governed by controller interface files:
<kbd>cpu.max</kbd> configures CPU bandwidth using Completely Fair Scheduler (CFS) quotas (e.g., <kbd>50000 100000</kbd> restricts a cgroup to 0.5 CPU cores per 100 ms period);
<kbd>memory.max</kbd> establishes a hard memory consumption ceiling;
<kbd>memory.high</kbd> serves as a soft limit triggering proactive memory reclaim;
<kbd>memory.current</kbd> reports active memory usage;
<kbd>memory.events</kbd> tracks allocation failures, high-water mark breaches, and kernel Out-Of-Memory (<strong class="keyword">OOM</strong>) kills; and
<kbd>pids.max</kbd> caps the number of active tasks to prevent fork bombs.
When a cgroup breaches its hard <kbd>memory.max</kbd> limit and the kernel cannot reclaim sufficient anonymous memory or page cache, the kernel invokes the cgroup-aware OOM killer to terminate processes inside that specific cgroup with exit code 137 (<kbd>SIGKILL</kbd>), leaving the rest of the host operating system completely unaffected.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cgroup limits are the exact technical mechanism underlying Kubernetes resource requests and limits (<kbd>resources.requests</kbd> and <kbd>resources.limits</kbd>). Misunderstanding cgroups v2 leads to common operational blunders: when an application crashes with exit code 137, operators frequently inspect host memory metrics and observe 80% free RAM, erroneously concluding that memory pressure did not occur. Architects must monitor cgroup-specific metrics (<kbd>memory.events</kbd> and container metrics in Cloud Monitoring) rather than host-wide metrics to diagnose throttling and OOM terminations accurately.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Modern GKE clusters running Container-Optimized OS (COS) with containerd utilize cgroups v2 by default. GKE translates Pod CPU and memory limits directly into cgroups v2 filesystem entries under <kbd>/sys/fs/cgroup/kubepods.slice/</kbd>. Google Cloud Monitoring integrates cgroup metrics directly into GKE observability dashboards, exposing container CPU throttling percentages and memory utilization against defined resource limits.</p>

<h4>Seccomp (Secure Computing Mode) System Call Filtering and BPF Profiles</h4>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Seccomp</strong> (Secure Computing Mode) is a Linux kernel security facility that restricts the system calls a process can issue. The Linux kernel exposes over 450 distinct system calls; an ordinary containerized web application requires fewer than 70. Seccomp-BPF uses Berkeley Packet Filter (BPF) bytecode programs attached to the process via <kbd>prctl(PR_SET_SECCOMP)</kbd> or the <kbd>seccomp()</kbd> system call to inspect system call numbers and argument registers before the kernel executes them. If a process attempts an unauthorized system call (such as <kbd>reboot</kbd>, <kbd>kexec_load</kbd>, or <kbd>ptrace</kbd>), the seccomp filter instantly takes action: returning an error code (such as <kbd>EPERM</kbd>), killing the thread with <kbd>SIGSYS</kbd>, or killing the entire process with <kbd>SECCOMP_RET_KILL_PROCESS</kbd>. Seccomp filters are inherited across <kbd>fork()</kbd> and cannot be disabled once installed.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Seccomp serves as the primary line of defense against Linux kernel privilege escalation exploits. Nearly all kernel privilege escalation CVEs involve obscure, legacy, or poorly tested system calls (e.g., <kbd>bpf()</kbd>, <kbd>userfaultfd()</kbd>, <kbd>keyctl()</kbd>). By applying a strict seccomp profile that blocks non-essential system calls, architects eliminate over 80% of potential kernel attack surfaces, ensuring that even if an attacker achieves arbitrary code execution inside a container, they cannot trigger vulnerabilities in dormant kernel code paths.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> GKE deploys with the default Docker/containerd seccomp profile enabled across all node pools, which blocks approximately 60 hazardous system calls (including <kbd>sys_chroot</kbd>, <kbd>kcmp</kbd>, and <kbd>mount</kbd>). For workloads with elevated compliance requirements, GKE supports custom seccomp profiles deployed via the Kubernetes Security Profiles Operator (SPO) or GKE node image customization.</p>

<h4>POSIX Capabilities and Least-Privilege Process Execution</h4>
<p><strong class="side-heading">What it is in general:</strong> Traditional UNIX partitioned process privileges into a coarse binary model: unprivileged processes (UID &gt; 0) with restricted access, and superuser root (UID 0) with absolute, omnipotent system power. Linux <strong class="keyword">POSIX capabilities</strong> break down root privilege into approximately 40 distinct, fine-grained permission bits (documented in <kbd>capabilities(7)</kbd>). For example:
<kbd>CAP_NET_BIND_SERVICE</kbd> allows binding to privileged ports below 1024;
<kbd>CAP_NET_ADMIN</kbd> allows configuring network interfaces and firewall routing tables;
<kbd>CAP_SYS_ADMIN</kbd> grants a broad range of administrative operations (often called "the new root");
<kbd>CAP_SYS_MODULE</kbd> allows inserting and removing kernel modules; and
<kbd>CAP_CHOWN</kbd> allows modifying file ownership.
Each Linux process maintains four capability sets: Effective (<kbd>CapEff</kbd>), Permitted (<kbd>CapPrm</kbd>), Inheritable (<kbd>CapInh</kbd>), and Bounding (<kbd>CapBnd</kbd>), inspectable in <kbd>/proc/[pid]/status</kbd>. Container runtimes strip the vast majority of capabilities from container processes, retaining only a minimal set (such as <kbd>CAP_CHOWN</kbd>, <kbd>CAP_NET_BIND_SERVICE</kbd>, <kbd>CAP_SETUID</kbd>) and dropping dangerous bits like <kbd>CAP_SYS_ADMIN</kbd> and <kbd>CAP_SYS_MODULE</kbd>.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Even if a container runs as UID 0 (root), dropping capabilities prevents the process from compromising the host. A containerized process running as root without <kbd>CAP_SYS_MODULE</kbd> cannot load rootkits; without <kbd>CAP_NET_ADMIN</kbd> it cannot reconfigure host routing; without <kbd>CAP_SYS_RAWIO</kbd> it cannot write to physical storage devices. Architects should enforce the security principle of least privilege by dropping all capabilities by default (<kbd>capabilities: drop: ["ALL"]</kbd>) in Kubernetes security contexts and adding back only the specific bits strictly necessary for the application.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> GKE Autopilot enforces strict capability guardrails by default, rejecting Pods that attempt to request <kbd>CAP_SYS_ADMIN</kbd>, <kbd>CAP_SYS_MODULE</kbd>, or host path volume mounts. In standard GKE, Google Cloud Security Command Center (SCC) continuously audits running container workloads and raises high-severity findings if containers run with privileged flags or excessive capability sets.</p>

<h4>Defense-in-Depth Container Sandboxing: gVisor, Cloud Run, and GKE Node Isolation</h4>
<p><strong class="side-heading">What it is in general:</strong> Because standard containers share the host Linux kernel, defense-in-depth requires isolating container execution boundaries beyond standard namespaces and cgroups. <strong class="keyword">Container sandboxing</strong> introduces an intermediary virtualization or emulation boundary between the application and the host kernel. Google's open-source <strong class="keyword">gVisor</strong> is a user-space application kernel (written in Go) that implements the Linux system call interface. When an application runs inside a gVisor sandbox, its system calls are not executed by the host kernel; instead, gVisor's userspace kernel (<kbd>Sentry</kbd>) intercepts and implements over 300 Linux system calls in safe userspace memory. Storage and network operations are mediated through a separate process (<kbd>Gofer</kbd>). Even if an attacker executes malicious shellcode or exploits an unpatched Linux kernel zero-day vulnerability, the exploit strikes gVisor's memory-safe Go runtime rather than the host Linux kernel.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Multi-tenant SaaS architectures, customer-supplied code execution platforms (such as code evaluation runners or CI/CD pipelines), and AI agent execution environments present extreme security risks. Running untrusted third-party code in standard containers on a shared Kubernetes node is an architectural hazard because a single kernel vulnerability leads to cluster-wide compromise. Architects must mandate sandboxed runtimes (such as gVisor or microVMs like Firecracker) or dedicated virtual machine node pools to isolate untrusted customer workloads securely.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Cloud Run executes all container instances inside gVisor sandboxes by default, providing enterprise-grade multi-tenant workload isolation on Google's serverless infrastructure. In GKE, architects can enable GKE Sandbox on any node pool with a single configuration flag (<kbd>--sandbox type=gvisor</kbd>), allowing Pods with the runtime class <kbd>runtimeClassName: gvisor</kbd> to run alongside standard containers while enjoying hardware-like isolation without the boot latency of full virtual machines.</p>

{FIG_9_2_HTML}

<div class="topic-card">
<table>
<caption>Table 9.2: The Four Pillars of Linux Container Isolation</caption>
<thead>
<tr>
<th>Subsystem</th>
<th>Primary Function</th>
<th>Kernel Inspection Mechanism</th>
<th>Failure or Violation Symptom</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Namespaces</strong></td>
<td>Visibility filtering (PID, NET, MNT, IPC, UTS, USER)</td>
<td><kbd>readlink /proc/$$/ns/*</kbd></td>
<td>Process cannot see or address foreign processes or network interfaces</td>
</tr>
<tr>
<td><strong>cgroups v2</strong></td>
<td>Resource quota enforcement (CPU, Memory, I/O, PIDs)</td>
<td><kbd>/sys/fs/cgroup/memory.max</kbd>, <kbd>memory.events</kbd></td>
<td>OOM kill (exit 137, <kbd>oom_kill +1</kbd>) or CPU throttling (<kbd>cpu.stat</kbd>)</td>
</tr>
<tr>
<td><strong>Seccomp</strong></td>
<td>System call filtering via BPF bytecode programs</td>
<td><kbd>grep Seccomp /proc/$$/status</kbd></td>
<td>Immediate process abort (<kbd>SIGSYS</kbd>) or permission error (<kbd>EPERM</kbd>)</td>
</tr>
<tr>
<td><strong>Capabilities</strong></td>
<td>Deconstruction of root privileges into ~40 discrete bits</td>
<td><kbd>grep CapEff /proc/$$/status</kbd> (<kbd>capsh --decode</kbd>)</td>
<td>Privileged operation rejected (<kbd>Operation not permitted</kbd>)</td>
</tr>
</tbody>
</table>
</div>

<p><strong class="side-heading">Concrete example:</strong> Consider a production document processing container running on GKE that generates PDF reports. The container is configured with a cgroups v2 memory limit of 512 MB (<kbd>memory.max = 536870912</kbd>). When an unexpected batch of 50 complex architectural diagrams is queued, the application attempts to buffer uncompressed raster images in memory, driving memory usage up to 513 MB. The host server possesses 64 GB of physical RAM with 48 GB completely unallocated. However, because cgroups v2 enforces local limits independently of host headroom, the kernel invokes the cgroup OOM killer, dispatches <kbd>SIGKILL</kbd> to the worker process, increments <kbd>oom_kill</kbd> in <kbd>/sys/fs/cgroup/memory.events</kbd>, and records exit code 137 in Kubernetes. The architect refactors the application to stream document generation directly to Cloud Storage via chunked byte buffers, capping active working set memory at 180 MB and eliminating OOM kills without requiring costly VM resizing.</p>

<p><strong class="side-heading">Evidence limit:</strong> Inspecting namespace links in <kbd>/proc/$$/ns/</kbd> and confirming zero dropped capabilities in <kbd>/proc/$$/status</kbd> proves that a container process is executing within restricted visibility and privilege contexts; it does not prove complete security against side-channel microarchitectural attacks (such as cache timing or branch prediction leaks) on shared CPU cores without hardware-enforced CPU core pinning and hypervisor or sandboxed kernel boundaries.</p>
'''
