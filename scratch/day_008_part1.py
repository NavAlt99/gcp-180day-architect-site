"""Technical discussion for Topic 1: CPU scheduling, memory, OOM, and PSI."""

TOPIC_01_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li>CPU scheduling algorithms, run queues, and CFS context switching</li>
<li>Virtual memory architecture, MMU page tables, and page fault dynamics</li>
<li>Memory hierarchy: active/inactive RAM, page cache, dirty writeback, and swap space</li>
<li>Out-Of-Memory (OOM) killer mechanics, badness heuristics, and cgroup memory boundaries</li>
<li>Pressure Stall Information (PSI): quantifying CPU, memory, and I/O starvation</li>
</ul>

<h4>CPU scheduling algorithms, run queues, and CFS context switching</h4>
<p><strong class="side-heading">What it is in general:</strong> The Linux kernel allocates processor cores among runnable threads using the <strong class="keyword">Completely Fair Scheduler</strong> (CFS, evolved into EEVDF in newer kernels). CFS models an "ideal multi-tasking CPU" on hardware by assigning each thread a virtual runtime (<code>vruntime</code>) metric representing the scaled processor execution time it has consumed. Threads with smaller <code>vruntime</code> values take priority on red-black run queues. When the kernel interrupts a running thread to dispatch another, it executes a <strong class="keyword">Context Switch</strong>: flushing CPU hardware registers, swapping kernel stack pointers, updating CPU program counters, and invalidating Translation Lookaside Buffer (TLB) virtual memory address mappings. Context switches divide into <strong class="keyword">Voluntary Switches</strong> (where a thread blocks waiting for I/O, locks, or timers) and <strong class="keyword">Involuntary Switches</strong> (where a thread exhausts its allocated scheduling time slice or is preempted by a higher-priority task).</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Saturated host CPUs manifest as high run queue depths (load average exceeding physical core counts) and elevated involuntary context switching rates. High context switching rates degrade performance because cache lines are constantly evicted from L1/L2 hardware caches. Architects must separate compute saturation (tasks actively executing instruction pipelines) from scheduling starvation (tasks queued and waiting for access to physical cores).</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine shared-core machine types (such as <code>e2-micro</code>, <code>e2-small</code>, and <code>e2-medium</code>) rely on CPU hypervisor time-sharing and burst allowances. If an e2 shared-core VM exhausts its CPU credit balance, the KVM hypervisor throttles physical CPU execution timeslices, creating severe scheduler wait stalls inside the guest OS that mimic hardware saturation. In contrast, dedicated Compute Engine C2, C3, and N2 machine types provide dedicated hardware execution threads and NUMA alignment. Primary documentation: <a href="https://man7.org/linux/man-pages/man7/sched.7.html#DESCRIPTION">sched(7) Linux CPU scheduling overview description (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man7/sched.7.html#DESCRIPTION">sched(7) completely fair scheduling and priority policies (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man8/vmstat.8.html#DESCRIPTION">vmstat(8) system activity and context switch reporting (accessed 2026-10-04)</a>.</p>

<h4>Virtual memory architecture, MMU page tables, and page fault dynamics</h4>
<p><strong class="side-heading">What it is in general:</strong> Linux user-space processes do not interact directly with physical RAM. Instead, each process operates inside an isolated virtual address space governed by the CPU's <strong class="keyword">Memory Management Unit</strong> (MMU). The kernel organizes virtual memory into fixed-size units known as <strong class="keyword">Memory Pages</strong> (standard 4 KB architectures, or 2 MB / 1 GB HugePages). Virtual addresses map to physical memory frames via hierarchical page tables. When a thread accesses a virtual page that has not yet been mapped to a physical frame, the MMU triggers a CPU hardware interrupt called a <strong class="keyword">Page Fault</strong>. Page faults divide into two critical operational classes:
<br>1. <strong class="keyword">Minor Page Faults:</strong> The requested memory page is already resident in physical RAM (for example, shared library text segments or freshly allocated anonymous memory claimed via <code>malloc</code>) and the kernel satisfies the fault simply by establishing a page table entry without triggering disk I/O.
<br>2. <strong class="keyword">Major Page Faults:</strong> The requested page is absent from physical RAM and must be read synchronously from backing storage (such as disk swap space or an executable binary on a persistent filesystem), causing the requesting thread to block until storage I/O completes.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> A spike in minor page faults indicates high process allocation churn or fork-exec activity, typically consuming modest CPU overhead. In contrast, an elevated rate of major page faults signals memory starvation: the working set of the workload exceeds available physical RAM, forcing the kernel to fetch swapped or unmapped memory from disk, inducing catastrophic latency tail events.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine Persistent Disks (standard PD, balanced PD, SSD PD) have bounded IOPS and read throughput ratings governed by provisioned disk size. A workload that incurs continuous major page faults on a Compute Engine instance with standard HDD storage quickly exhausts disk IOPS quotas, causing the entire VM to stall as threads freeze in uninterruptible sleep (D state) awaiting page reads. Primary documentation: <a href="https://docs.kernel.org/admin-guide/mm/concepts.html#page-cache">Linux kernel memory concepts — virtual memory and page cache (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.kernel.org/admin-guide/mm/concepts.html#page-cache">Linux kernel memory concepts — address spaces and page allocation (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man5/proc_meminfo.5.html#DESCRIPTION">proc_meminfo(5) kernel memory counters description (accessed 2026-10-04)</a>.</p>

<h4>Memory hierarchy: active/inactive RAM, page cache, dirty writeback, and swap space</h4>
<p><strong class="side-heading">What it is in general:</strong> The Linux memory subsystem classifies physical RAM into active/inactive anonymous allocations and file-backed memory. Unused physical memory is automatically utilized by the kernel as <strong class="keyword">Page Cache</strong>, storing recently read and written filesystem blocks in RAM to avoid expensive persistent disk transactions. When applications write to files, modifications remain buffered in RAM as <strong class="keyword">Dirty Pages</strong> until kernel flush daemons (<code>kswapd</code> and writeback threads) asynchronously flush them to persistent storage. Consequently, examining raw free memory (<code>MemFree</code> in <code>/proc/meminfo</code>) frequently reveals low single-digit gigabytes on healthy production nodes. The crucial metric is <strong class="keyword">MemAvailable</strong>, which estimates the total memory available for starting new applications without swapping, taking into account reclaimable page cache and dentries. <strong class="keyword">Swap Space</strong> provides disk-backed overflow storage for anonymous memory pages, allowing the kernel to evict cold process heap allocations to preserve page cache for hot I/O paths.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Naive monitoring rules that trigger alerts when "Free RAM" drops below 10% produce widespread false positives because the Linux kernel deliberately fills idle RAM with reclaimable page cache. Conversely, systems without configured swap space or with aggressive memory consumption experience sudden catastrophic crashes rather than gradual degradation. Architects rely on <code>MemAvailable</code> and kernel reclaim rates rather than raw <code>MemFree</code> to evaluate true host memory headroom.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud public VM images for Debian, Ubuntu, and CentOS are distributed with swap space disabled by default to prevent unpredictable latency degradation on network-attached Persistent Disks. In high-throughput streaming and database workloads (e.g. Kafka or PostgreSQL on Compute Engine), architects configure kernel dirty page ratios (<code>vm.dirty_ratio</code> and <code>vm.dirty_background_ratio</code>) to ensure dirty memory writeback occurs smoothly without choking Persistent Disk write queues. Primary documentation: <a href="https://man7.org/linux/man-pages/man5/proc_meminfo.5.html#DESCRIPTION">proc_meminfo(5) memory distribution and page cache metrics (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man5/proc_meminfo.5.html#DESCRIPTION">proc_meminfo(5) MemAvailable and page cache fields (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man8/vmstat.8.html#DESCRIPTION">vmstat(8) memory and swap transfer reporting (accessed 2026-10-04)</a>.</p>

<h4>Out-Of-Memory (OOM) killer mechanics, badness heuristics, and cgroup memory boundaries</h4>
<p><strong class="side-heading">What it is in general:</strong> When physical memory and swap exhaustion prevents the kernel from fulfilling an urgent memory allocation request, the kernel invokes the <strong class="keyword">Out-Of-Memory (OOM) Killer</strong> to prevent a complete system deadlock. The kernel scans all running processes and computes an internal "badness" heuristic score (exposed via <code>/proc/[pid]/oom_score</code>), prioritizing processes consuming massive proportions of RAM while having low privilege or run time. System administrators can influence this choice by writing to <code>/proc/[pid]/oom_score_adj</code> (-1000 immunizes a critical process like sshd or systemd, while +1000 targets sacrificial workers). Crucially, in modern containerized operating systems, memory enforcement operates at both the host VM level and the <strong class="keyword">Control Group</strong> (cgroup v1/v2) boundary. In cgroups v2, the kernel enforces limits such as <code>memory.high</code> (throttling and asynchronous reclaim) and <code>memory.max</code> (hard ceiling triggering a cgroup-level OOM killer). When a process inside a cgroup exceeds its <code>memory.max</code>, the kernel terminates the container process even if the underlying host VM has hundreds of gigabytes of unallocated physical RAM.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Containerized applications running on Kubernetes (GKE) or container runtimes frequently crash with exit status 137 (SIGKILL issued by OOM). Blindly upsizing host VMs does not resolve container OOM terminations if the pod specification or container manifest specifies an inadequate container memory limit. Architects must inspect cgroup <code>memory.events</code> and kernel dmesg logs to distinguish container-level quota violations from host-wide physical exhaustion.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Kubernetes Engine (GKE) nodes utilize cgroup v2 on modern Container-Optimized OS (COS) images. When a pod exceeds its configured container memory limit, the Linux kernel terminates the offending process and GKE records an <code>OOMKilled</code> status event. If the host VM itself runs low on memory, the GKE kubelet eviction manager intervenes before the kernel OOM killer, evicting pods based on Quality of Service (QoS) classes (BestEffort before Burstable before Guaranteed). Primary documentation: <a href="https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION">proc(5) process oom_score and oom_score_adj description (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION">proc(5) oom_score heuristics and adjustments (accessed 2026-10-04)</a>; <a href="https://docs.kernel.org/admin-guide/mm/concepts.html#page-cache">Linux kernel memory concepts — OOM handling (accessed 2026-10-04)</a>.</p>

<h4>Pressure Stall Information (PSI): quantifying CPU, memory, and I/O starvation</h4>
<p><strong class="side-heading">What it is in general:</strong> Traditional utilization metrics (such as CPU percentage or free memory) describe current resource usage but fail to indicate whether workloads are actually delayed or impaired by resource shortages. <strong class="keyword">Pressure Stall Information</strong> (PSI) is a Linux kernel accounting facility that directly tracks the percentage of wall-clock time that tasks spend stalled while waiting for congested CPU, memory, or block I/O resources. Exposed through pseudo-files in <code>/proc/pressure/{cpu,memory,io}</code> and inside cgroup directories, PSI reports two distinct starvation levels:
<br>1. <strong class="keyword">some:</strong> The percentage of time in which at least one non-idle task was stalled waiting for the contended resource (indicating micro-contention and beginning latency degradation).
<br>2. <strong class="keyword">full:</strong> The percentage of time in which <em>all</em> non-idle tasks were simultaneously stalled waiting for the resource (indicating complete workload paralysis, such as during synchronous memory reclaim or storage thrashing).
PSI provides rolling moving averages over 10-second, 60-second, and 300-second windows alongside cumulative total stall time in microseconds.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> PSI allows architects to establish automated, proactive health checks and auto-scaling triggers. Rather than waiting for a fatal OOM kill or severe API timeout, monitoring agents trigger proactive traffic draining or horizontal pod autoscaling when <code>memory:some</code> or <code>cpu:some</code> pressure exceeds defined operational thresholds (such as 10% over a 60-second window).</p>
<p><strong class="side-heading">Relevance to GCP:</strong> The Google Cloud Ops Agent collects Linux PSI metrics directly and streams them to Cloud Monitoring dashboards. Compute Engine autoscalers and GKE custom metric horizontal pod autoscalers (HPAs) can query PSI stall rates to scale application clusters dynamically based on real hardware contention rather than inaccurate CPU utilization averages. Primary documentation: <a href="https://docs.kernel.org/accounting/psi.html#pressure-interface">Linux kernel documentation — Pressure Stall Information interface (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://docs.kernel.org/accounting/psi.html#pressure-interface">Linux PSI interface and cgroup monitoring (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION">proc(5) pressure accounting pseudo-filesystem (accessed 2026-10-04)</a>.</p>

<div class="table-responsive">
<table class="table">
<caption>Resource signal decision map: distinguishing execution saturation, scheduling starvation, and boundary limits.</caption>
<thead>
<tr>
<th>Signal</th>
<th>What it supports</th>
<th>What it does not prove</th>
<th>Next comparison</th>
</tr>
</thead>
<tbody>
<tr>
<td>CPU PSI (<code>some</code> / <code>full</code>)</td>
<td>Quantifies exact percentage of time runnable tasks stalled waiting for available CPU cores</td>
<td>Does not identify which specific application thread or algorithm is consuming CPU cycles</td>
<td>Inspect runnable thread count, thread priority, cgroup CPU quota, and application flame graphs</td>
</tr>
<tr>
<td>Minor / Major Page Faults</td>
<td>Measures rate of virtual page table resolution (minor: in RAM; major: disk read required)</td>
<td>Does not prove an imminent OOM kill or distinguish normal code startup from storage thrashing</td>
<td>Correlate major fault rate with Persistent Disk IOPS limits, swap activity, and memory reclaim</td>
</tr>
<tr>
<td><code>MemAvailable</code> vs Page Cache</td>
<td>Estimates actual RAM capacity reclaimable for applications without invoking swap</td>
<td>Does not prove whether a specific container or cgroup has exceeded its local memory limit</td>
<td>Compare host-level <code>MemAvailable</code> against container cgroup <code>memory.current</code> and <code>memory.max</code></td>
</tr>
<tr>
<td>Cgroup <code>memory.events</code></td>
<td>Records discrete kernel events: <code>high</code>, <code>max</code>, and <code>oom_kill</code> occurrences inside a cgroup</td>
<td>Does not prove that the underlying host VM ran out of physical memory</td>
<td>Examine host <code>/proc/meminfo</code> to verify if exhaustion was host-wide or isolated to a container limit</td>
</tr>
</tbody>
</table>
</div>

{FIG_8_1_HTML}

<p><strong class="side-heading">Concrete example:</strong> A compute-intensive order batch processor runs inside a container on a 16 GB host VM. SREs observe order latency jumping from 50 ms to 1,200 ms. Querying <code>/proc/pressure/cpu</code> reveals <code>some avg10=28.40</code> and <code>/proc/pressure/memory</code> shows <code>some avg10=0.00</code>. Concurrently, <code>vmstat 1</code> reports involuntary context switches spiking to 14,000/sec while run queue depth (<code>r</code>) reaches 18 on an 8-core host. This isolates the root cause directly to CPU scheduling starvation and time slice preemption rather than memory thrashing, proving that increasing VM memory would be completely ineffective while adjusting CPU limits or thread concurrency resolves the issue.</p>

<p><strong class="side-heading">Evidence limit:</strong> Resource utilization metrics, context switch counters, and free memory graphs provide diagnostic telemetry but cannot prove causal performance degradation without correlating timestamped Pressure Stall Information, cgroup limit boundaries, and application response latency.</p>
'''
