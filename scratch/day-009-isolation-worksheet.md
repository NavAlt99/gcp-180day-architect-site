# Day 9 Exit Artifact: Isolation Comparison Worksheet
**Generated:** 2026-10-04 05:24:29Z
**Scope:** Distinguishing Resource Enforcement from Security Isolation in Virtual Machines and Containers.

## 1. Subsystem Classification Matrix

| Subsystem | Mechanism | Primary Function | Failure Mode / Boundary Breach | Security Boundary? |
|---|---|---|---|---|
| **Namespaces** | Kernel isolation tags (`/proc/$$/ns/`) | Visibility partitioning (PID, NET, MNT, IPC, UTS, USER) | Information disclosure / cross-namespace leak | No (Visibility only) |
| **cgroups v2** | Resource accounting (`/sys/fs/cgroup`) | Resource quota enforcement (CPU, Memory, I/O, PIDs) | Throttling or OOM kill (exit 137) | No (Resource quota only) |
| **Seccomp** | BPF system call filter (`/proc/$$/status`) | Gating allowable kernel system calls | Syscall rejected (EPERM / SIGSYS) | Yes (Restricts kernel attack surface) |
| **Capabilities** | POSIX privilege bits (`CapEff`) | Deconstructing root privileges | Operation not permitted (EPERM) | Yes (Restricts privileged operations) |
| **Virtual Machine (KVM)** | Hardware VMX/SVM & EPT MMU | Sovereign guest kernel & hardware emulation | Hypervisor escape (extremely rare) | Yes (Cryptographic & hardware enforced) |

## 2. Resource Enforcement vs Security Isolation Analysis

1. **Why Resource Enforcement is Not Security Isolation:**
   - A container with strict cgroups v2 limits (`cpu.max`, `memory.max`) cannot exhaust host memory or starve neighbor CPUs.
   - However, if the container exploits a vulnerability in the shared Linux kernel (e.g. a Dirty Pipe or io_uring privilege escalation), it gains Ring 0 execution on the host regardless of cgroup limits.
   - Therefore, cgroups enforce *resource availability*, not *security isolation*.

2. **Why Namespaces are Not Security Isolation:**
   - Namespaces restrict what a process can see (private PID numbering, private network interfaces).
   - However, system calls issued inside a namespace enter the same shared kernel space as system calls issued by the host root user.
   - Therefore, namespaces enforce *visibility boundaries*, not *privilege containment*.

3. **When to Choose Virtual Machines over Containers:**
   - Workloads requiring custom Linux kernel modules or proprietary device drivers.
   - Untrusted multi-tenant execution where hostile code could execute arbitrary system calls.
   - Compliance mandates requiring hardware-isolated cryptographic boundaries (e.g. Confidential Computing / AMD SEV).

4. **Defense-in-Depth Container Sandboxing:**
   - For container workloads requiring near-VM isolation without VM boot overhead, utilize gVisor (Cloud Run / GKE Sandbox).
   - gVisor runs an independent application kernel in userspace, preventing untrusted system calls from reaching the host Linux kernel.
