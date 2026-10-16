#!/usr/bin/env python3
"""Topic 4 technical text for Day 7."""

TOPIC_04_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ol>
<li>VFS dynamic memory exposition: why /proc consumes zero disk blocks</li>
<li>Process directory structure: /proc/[pid]/status, cmdline, environ, and fd</li>
<li>Process trees, parent-child relationships (PPID), and orphan reaping by PID 1</li>
<li>System-wide kernel telemetry: /proc/cpuinfo, meminfo, stat, and loadavg</li>
<li>Observability and troubleshooting: recovering deleted files via /proc/[pid]/fd and tracking container cgroup boundaries</li>
</ol>

<h4>VFS dynamic memory exposition: why /proc consumes zero disk blocks</h4>
<p><strong class="side-heading">What it is in general:</strong> The <strong class="keyword">/proc filesystem</strong> (procfs) is a pseudo-filesystem created by the Linux kernel that does not exist on any physical block storage device. Mounted at <code>/proc</code> with filesystem type <code>proc</code>, its files and directories are virtual: when a process issues a <kbd>read()</kbd> system call on a file like <code>/proc/meminfo</code>, the kernel traps into custom VFS handler functions in kernel space, formats live in-memory data structures into ASCII text on the fly, and streams the output directly into user space memory buffers. Consequently, <code>stat -c %b /proc/version</code> reports 0 allocated disk blocks, and file sizes are typically reported as 0 bytes despite returning readable text streams.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Understanding procfs is essential for container and VM telemetry: monitoring agents (such as Prometheus node_exporter or Datadog) derive CPU, memory, network, and disk metrics almost exclusively by reading <code>/proc</code> virtual files. Architecting lightweight monitoring requires understanding the CPU context-switch overhead incurred when repeatedly querying thousands of dynamic procfs nodes.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> The Google Cloud Ops Agent (fluentbit and otel collectors) runs on Compute Engine VMs to harvest system health metrics by scraping <code>/proc/stat</code>, <code>/proc/meminfo</code>, and <code>/proc/diskstats</code>, shipping time-series data to Google Cloud Monitoring. Primary documentation: <a href="https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION">proc(5) process information pseudo-filesystem description (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION">proc(5) VFS mount options and file formats (accessed 2026-10-04)</a>.</p>

<h4>Process directory structure: /proc/[pid]/status, cmdline, environ, and fd</h4>
<p><strong class="side-heading">What it is in general:</strong> For every active process running on the system, the kernel creates a numerical sub-directory in <code>/proc/[pid]</code> corresponding to its process ID. Key files within this directory provide deep diagnostic inspection:
<ul>
<li><code>status</code>: human-readable process state, real and effective UIDs/GIDs, memory limits (VmRSS, VmPeak), and signal masks.</li>
<li><code>cmdline</code>: the complete, null-byte-separated argument vector (argv) passed during process invocation.</li>
<li><code>environ</code>: the complete, null-byte-separated environment variable list inherited or set by the process.</li>
<li><code>fd/</code>: a subdirectory containing symbolic links representing every open file descriptor (0=stdin, 1=stdout, 2=stderr, 3+=sockets and files) pointing to the actual target file or network socket inode.</li>
</ul></p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> The <code>/proc/[pid]/environ</code> file exposes a major security boundary: if sensitive secrets (database passwords, API keys) are passed as environment variables, any local user with permissions to read that process's proc directory (or root) can extract credentials in plain text. Architects enforce secrets retrieval via runtime memory or ephemeral tokens rather than static environment variables.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine security audits inspect <code>/proc/[pid]/environ</code> to ensure application service credentials are not exposed to unprivileged users, validating that Secret Manager integration uses secure APIs rather than insecure static environment dumps. Primary documentation: <a href="https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION">proc(5) /proc/[pid]/status and /proc/[pid]/fd descriptions (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION">proc(5) /proc/[pid]/cmdline and /proc/[pid]/environ formatting (accessed 2026-10-04)</a>.</p>

<h4>Process trees, parent-child relationships (PPID), and orphan reaping by PID 1</h4>
<p><strong class="side-heading">What it is in general:</strong> Every Linux process (except PID 1) is spawned by a parent process via <kbd>fork()</kbd> or <kbd>clone()</kbd>, recording the parent's process ID as <strong class="keyword">PPID</strong> (Parent PID). This creates an acyclic hierarchy known as the <strong class="keyword">Process Tree</strong>. When a parent process terminates before its child, the child becomes an <strong class="keyword">orphan</strong>. In standard Linux, orphan processes are immediately adopted by PID 1 (systemd or the container init system). When a child terminates, it enters the <strong class="keyword">zombie</strong> state (defunct), consuming zero CPU and RAM but retaining an entry in the kernel process table until the parent calls <kbd>waitpid()</kbd> to collect its exit status. If PID 1 fails to reap zombies, the process table eventually exhausts all available PIDs, preventing any new processes from launching.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Zombie accumulation is a classic failure mode in lightweight container architectures where applications run directly as PID 1 without an init system (like <code>tini</code> or <code>dumb-init</code>) to reap orphaned child processes spawned by background sub-tasks.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Kubernetes Engine (GKE) and Cloud Run orchestrate containerized workloads: container images must include a proper init reaper or use GKE's native sub-reaping capabilities to prevent zombie PID exhaustion from crashing node operating systems. Primary documentation: <a href="https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION">proc(5) process state characters and zombie descriptions (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man2/waitpid.2.html#DESCRIPTION">waitpid(2) process wait and reaping semantics (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man1/pstree.1.html#DESCRIPTION">pstree(1) process tree visualization (accessed 2026-10-04)</a>.</p>

<h4>System-wide kernel telemetry: /proc/cpuinfo, meminfo, stat, and loadavg</h4>
<p><strong class="side-heading">What it is in general:</strong> Beyond per-process directories, <code>/proc</code> exposes global hardware and kernel performance counters:
<ul>
<li><code>/proc/cpuinfo</code>: microprocessor architecture, core counts, CPU flags, and frequency.</li>
<li><code>/proc/meminfo</code>: real-time memory distribution, distinguishing <code>MemTotal</code>, <code>MemFree</code>, <code>MemAvailable</code> (memory reclaimable without swapping), <code>Buffers</code>, and <code>Cached</code>.</li>
<li><code>/proc/stat</code>: cumulative CPU time spent in user, system, idle, iowait, and steal modes since boot.</li>
<li><code>/proc/loadavg</code>: 1-minute, 5-minute, and 15-minute system load averages, representing the average number of threads in runnable state (R) or uninterruptible sleep (D) waiting on disk I/O.</li>
</ul></p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects utilize <code>MemAvailable</code> rather than <code>MemFree</code> when configuring container memory limits and autoscaling policies: Linux aggressively caches disk I/O in RAM, so <code>MemFree</code> is often near zero even on healthy, high-capacity systems.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine VM instance sizing, Cloud Monitoring metrics, and Cloud Autoscalers rely on kernel telemetry extracted from <code>/proc/stat</code> (for CPU utilization percentages) and <code>/proc/meminfo</code> (for memory pressure alerts). Primary documentation: <a href="https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION">proc(5) /proc/meminfo and /proc/stat definitions (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION">proc(5) /proc/loadavg and runnable thread metrics (accessed 2026-10-04)</a>.</p>

<h4>Observability and troubleshooting: recovering deleted files via /proc/[pid]/fd and tracking container cgroup boundaries</h4>
<p><strong class="side-heading">What it is in general:</strong> In Linux, unlinking a file (<kbd>rm filename</kbd>) decrements the inode's link count but does not delete the data blocks from disk as long as any active process holds an open file descriptor to that inode. If a large log file is accidentally deleted while a daemon is running, the disk space remains consumed, but the file path disappears from directory listings. Administrators can inspect <code>/proc/[pid]/fd</code> to find symbolic links marked <code>(deleted)</code>, read the active data stream, and even recover the deleted data by copying directly from <code>/proc/[pid]/fd/[n]</code> back to a new file path.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Hidden disk exhaustion caused by unlinked open file descriptors is a frequent root cause of production VM outages: <kbd>du -sh *</kbd> reports plenty of free space, but <kbd>df -h</kbd> reports 100% full. Diagnosing this discrepancy requires querying <code>/proc/*/fd</code> via tools like <kbd>lsof +L1</kbd>.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud Persistent Disks, disk full events freeze VM instance writing operations. System reliability engineers utilize <code>/proc</code> descriptor inspection to identify the offending process, truncate the file descriptor via <kbd>&gt; /proc/[pid]/fd/[n]</kbd>, or restart the service to immediately reclaim allocated disk space. Primary documentation: <a href="https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION">proc(5) /proc/[pid]/fd and file descriptor lifecycle (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man8/lsof.8.html#DESCRIPTION">lsof(8) list open files utility description (accessed 2026-10-04)</a>.</p>

<table><caption>Key /proc files and diagnostic functions</caption>
<thead><tr><th>Path</th><th>Kernel Source</th><th>Diagnostic Utility</th><th>Operational Insight</th></tr></thead>
<tbody>
<tr><td>/proc/[pid]/status</td><td>task_struct</td><td>Process state &amp; VmRSS memory</td><td>Detects zombie states and memory footprints.</td></tr>
<tr><td>/proc/[pid]/fd/</td><td>files_struct</td><td>Active file descriptors</td><td>Recovers deleted files and detects descriptor leaks.</td></tr>
<tr><td>/proc/meminfo</td><td>mm zone stats</td><td>MemAvailable calculation</td><td>True available memory excluding page cache.</td></tr>
<tr><td>/proc/stat</td><td>kernel scheduler ticks</td><td>CPU utilization calculation</td><td>Measures user, system, and steal CPU time.</td></tr>
</tbody></table>

{FIG_7_4_HTML}

<p><strong class="side-heading">Concrete example:</strong> An administrative worker process is running and holding an open descriptor to a multi-gigabyte log file at <code>/var/log/worker.log</code>. An operator runs <kbd>rm /var/log/worker.log</kbd> to free up disk space. Running <kbd>df -h /</kbd> reveals the filesystem is still at 98% capacity because the process keeps the inode allocated. The operator runs:
<pre><code># Identify PID holding deleted file descriptor
PID=$(lsof +L1 | grep worker.log | awk '{print $2}')
# Inspect the virtual descriptor in procfs
ls -l "/proc/$PID/fd" | grep "(deleted)"
# Truncate the file descriptor to zero bytes to immediately free disk blocks
: &gt; "/proc/$PID/fd/3"</code></pre>
Truncating the open file descriptor in <code>/proc/$PID/fd/3</code> immediately frees the unlinked disk blocks, reducing filesystem usage from 98% to 15% without interrupting the running service.</p>
<p><strong class="side-heading">Evidence limit:</strong> Observing file descriptors in <code>/proc/[pid]/fd</code> verifies which inode targets the kernel has allocated to a process; it does not prove that the process is actively reading or writing to those descriptors or that data streams are free of application protocol corruption.</p>'''

print("Topic 4 tech defined.")
