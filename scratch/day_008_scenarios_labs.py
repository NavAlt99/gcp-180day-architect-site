"""Scenarios and labs for Day 8: CPU, memory, and diagnostic signals."""

SCENARIOS_AND_LABS = {
    'topic-01': {
        'scenario': {
            'scenario': 'Host resize misses a smaller cgroup OOM boundary',
            'impact': 'Production payment worker containers intermittently crash and restart during peak transaction processing, dropping active customer checkout sessions.',
            'constraints': 'Do not induce actual host-wide memory exhaustion or crash production VMs; preserve restart timestamps and process IDs; do not modify cgroup memory limits before capturing baseline values.',
            'evidence': '''**illustrative supplied records**

```text
[Host Monitoring Alert] Host free memory below 8% (Host MemTotal: 16,384 MB, MemFree: 1,120 MB)
[SRE Action] Upgraded Compute Engine instance from n2-standard-4 (16 GB) to n2-standard-8 (32 GB)
[Worker Crash Log] Process terminated abruptly at 2026-10-04T10:14:22Z; exit status 137 (SIGKILL)
[Kernel dmesg] [18492.104] Memory cgroup out of memory: Killed process 4182 (order-worker) total-vm:812044kB, anon-rss:518420kB, file-rss:1240kB, shmem-rss:0kB
[Kernel dmesg] [18492.105] oom_reaper: reaped process 4182 (order-worker), now anon-rss:0kB
[Cgroup Telemetry] /sys/fs/cgroup/payment.slice/memory.max: 536870912 (512 MB)
[Cgroup Telemetry] /sys/fs/cgroup/payment.slice/memory.events: oom 14, oom_kill 14
[Host /proc/meminfo at crash]
MemTotal:       32890412 kB
MemFree:         4128904 kB
MemAvailable:   26840112 kB
Cached:         22104880 kB
```''',
            'root': 'The worker process was constrained within a cgroup v2 container slice with memory.max configured to 512 MB. While the host VM initially showed low MemFree due to 12 GB of reclaimable page cache, the host actually had ample available memory (14 GB MemAvailable). Blindly resizing the host VM to 32 GB did not alter the 512 MB container cgroup limit, so the kernel OOM killer continued terminating the container whenever its anonymous memory footprint exceeded 512 MB.',
            'verify': 'Correlate the container restart timestamp directly with cgroup memory.events counters rather than host-level graphs. Reconfigure the container memory.max limit from 512 MB to 1024 MB, verify that the cgroup oom_kill counter stops incrementing, and observe stable worker execution without crashes.',
            'residual': 'Increasing container memory ceilings addresses immediate OOM termination but does not resolve underlying memory leaks if the application heap grows monotonically; heap profiling must be scheduled to establish true steady-state memory requirements.',
            'diagram_enabled': True,
            'facts': 'Worker process killed with signal 137; kernel dmesg confirms cgroup OOM invocation for process 4182; host MemAvailable was over 26 GB; cgroup memory.max was strictly set to 512 MB.',
            'inference': 'The memory exhaustion event occurred strictly at the cgroup boundary (512 MB) rather than the physical VM host boundary.',
            'expected': 'Correlating cgroup memory.events with process restart timestamps pinpoints the container limit; adjusting the cgroup boundary eliminates the crash.',
            'diagnostic_steps': [
                'Inspect container exit status (exit 137 indicates SIGKILL from kernel OOM killer).',
                'Inspect host-level /proc/meminfo to verify host MemAvailable vs MemFree.',
                'Examine cgroup memory.events for the workload slice to inspect oom and oom_kill counters.',
                'Inspect kernel dmesg for "Memory cgroup out of memory: Killed process" entries.'
            ],
            'remediation_steps': [
                'Capture baseline cgroup memory.max and peak container RSS usage.',
                'Reconfigure container manifest memory.max limit to provide adequate operational headroom.',
                'Verify container stability and confirm cgroup memory.events oom_kill counter remains static.'
            ],
            'diagram': (
                "Peak load surge",
                "Cgroup quota mismatch",
                "Worker killed (exit 137)",
                "Resize cgroup memory.max",
                "Stable execution verified"
            ),
            'icons': [
                '../assets/icons/generic/event.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/decision.svg',
                '../assets/icons/generic/outcome.svg'
            ]
        },
        'lab': {
            'name': 'Resource telemetry baseline and OOM/PSI diagnostic classification',
            'goal': 'Measure a bounded local CPU task, inspect host memory and page cache metrics, and classify supplied OOM and PSI telemetry without exhausting host resources.',
            'expected': 'Accurate recording of process CPU time vs wall time, calculation of reclaimable page cache from /proc/meminfo, and structured classification of supplied OOM/PSI incident logs.',
            'mode': 'Observed locally: local CPU task and memory metrics. Simulated or predicted: synthetic OOM and PSI log classification. Untested on GCP: Compute Engine hypervisor credit throttling.',
            'covers': 'Observe a bounded local CPU task and inspect memory/page-cache metrics; explain supplied OOM and PSI examples without exhausting the host.',
            'prereq': 'Local Linux bash terminal with Python 3 and standard procfs (/proc).',
            'preflight': 'Verify python3, coreutils, and read access to /proc/meminfo and /proc/pressure/.',
            'verification': 'Validate that script reports wall time ~0.5s, /proc/meminfo calculates MemAvailable, and diagnostic parser correctly classifies the cgroup OOM failure.',
            'trouble': 'If /proc/pressure is unavailable (older kernel), the diagnostic script falls back gracefully to simulated PSI inputs.',
            'cleanup': 'Remove the temporary lab directory and all generated log artifacts.',
            'accept': 'Comprehensive resource baseline report ($LAB_DIR/resource_baseline_report.md) generated with all calculations and classifications verified.',
            'file': 'day-008-topic-01.md',
            'steps': [
                '''**Stage 1: Preflight environment and diagnostic tool check**

**Location:** local bash terminal

Verify that Python 3 and basic Linux inspection utilities are available, and check read accessibility of `/proc/meminfo` and `/proc/pressure`:

```bash
command -v python3 >/dev/null && echo "PASS: python3 is available"
command -v grep >/dev/null && echo "PASS: grep is available"
command -v cat >/dev/null && echo "PASS: cat is available"

test -r /proc/meminfo && echo "PASS: /proc/meminfo is readable"
if [ -d /proc/pressure ]; then
  echo "PASS: /proc/pressure is supported by kernel"
else
  echo "NOTE: /proc/pressure not present on host kernel; synthetic PSI fallback will be utilized"
fi
```

**Expected result:** Tool checks confirm python3, grep, and /proc/meminfo accessibility.

**Save:** none''',

                '''**Stage 2: Establish isolated lab workspace and capture host baseline**

**Location:** local bash terminal

Initialize an isolated workspace in scratch directory and record host CPU and memory baselines:

```bash
LAB_DIR="/home/naveen/GitRepos/Projects/GCP/RoadMap/gcp-180day-architect-site/scratch/day_008_lab_t1"
mkdir -p "$LAB_DIR"
cd "$LAB_DIR"

echo "=== Host Baseline Architecture ===" | tee "$LAB_DIR/host_baseline.log"
uname -srm | tee -a "$LAB_DIR/host_baseline.log"
nproc | xargs -I{} echo "CPU Cores: {}" | tee -a "$LAB_DIR/host_baseline.log"
uptime | tee -a "$LAB_DIR/host_baseline.log"
```

**Expected result:** Workspace directory created and initial host hardware parameters logged.

**Save:** `$LAB_DIR/host_baseline.log`''',

                '''**Stage 3: Author bounded CPU and context switch measurement script**

**Location:** local bash terminal

Create a Python script that executes an intensive compute loop bounded strictly to 0.5 seconds of wall-clock time, recording wall time, process CPU time, and involuntary/voluntary context switches via `resource.getrusage`:

```bash
cat > "$LAB_DIR/bounded_cpu_bench.py" <<'EOF'
import resource
import time
import sys

# Record starting resource counters
start_wall = time.perf_counter()
start_cpu = time.process_time()
ru_start = resource.getrusage(resource.RUSAGE_SELF)

# Execute bounded workload for exactly 0.5 seconds
deadline = start_wall + 0.5
work_iterations = 0
while time.perf_counter() < deadline:
    work_iterations += 1

# Record ending resource counters
end_wall = time.perf_counter()
end_cpu = time.process_time()
ru_end = resource.getrusage(resource.RUSAGE_SELF)

wall_duration = end_wall - start_wall
cpu_duration = end_cpu - start_cpu
vol_cs = ru_end.ru_nvcsw - ru_start.ru_nvcsw
invol_cs = ru_end.ru_nivcsw - ru_start.ru_nivcsw

# Format and report results
print("=== Bounded CPU Execution Telemetry ===")
print(f"Wall Time Seconds:          {wall_duration:.4f}")
print(f"Process CPU Time Seconds:   {cpu_duration:.4f}")
print(f"Work Iterations Completed:  {work_iterations}")
print(f"Voluntary Context Switches:   {vol_cs}")
print(f"Involuntary Context Switches: {invol_cs}")
print(f"CPU Utilization Ratio:      {(cpu_duration / wall_duration) * 100:.1f}%")

if wall_duration < 0.45 or wall_duration > 0.65:
    print("FATAL: Wall duration outside bounded 0.5s tolerance")
    sys.exit(1)

print("PASS: Bounded CPU benchmark completed within safe tolerance.")
EOF
```

**Expected result:** Script written to `$LAB_DIR/bounded_cpu_bench.py`.

**Save:** `$LAB_DIR/bounded_cpu_bench.py`''',

                '''**Stage 4: Execute bounded CPU workload and log telemetry**

**Location:** local bash terminal

Run the bounded benchmark script and save execution metrics:

```bash
python3 "$LAB_DIR/bounded_cpu_bench.py" | tee "$LAB_DIR/cpu_telemetry.log"
```

**Expected result:** Workload terminates within ~0.50 seconds wall time, logging high CPU utilization and context switches without stalling the host.

**Save:** `$LAB_DIR/cpu_telemetry.log`''',

                '''**Stage 5: Inspect virtual memory, page cache, and MemAvailable**

**Location:** local bash terminal

Create and execute a memory analyzer that parses `/proc/meminfo` to extract physical RAM allocation, page cache buffers, and calculate true reclaimable memory:

```bash
cat > "$LAB_DIR/parse_meminfo.py" <<'EOF'
import sys

fields = {}
with open('/proc/meminfo', 'r') as f:
    for line in f:
        parts = line.split(':')
        if len(parts) == 2:
            key = parts[0].strip()
            val_parts = parts[1].strip().split()
            fields[key] = int(val_parts[0]) # values in kB

mem_total = fields.get('MemTotal', 0)
mem_free = fields.get('MemFree', 0)
mem_avail = fields.get('MemAvailable', 0)
cached = fields.get('Cached', 0)
buffers = fields.get('Buffers', 0)
swap_total = fields.get('SwapTotal', 0)
swap_free = fields.get('SwapFree', 0)

reclaimable_cache = cached + buffers
pct_free = (mem_free / mem_total) * 100 if mem_total else 0
pct_avail = (mem_avail / mem_total) * 100 if mem_total else 0

print("=== Linux Kernel Memory Telemetry (/proc/meminfo) ===")
print(f"Total Physical Memory:   {mem_total / 1024:.1f} MB ({mem_total / (1024*1024):.2f} GB)")
print(f"Raw Free Memory:         {mem_free / 1024:.1f} MB ({pct_free:.1f}%)")
print(f"Page Cache & Buffers:    {reclaimable_cache / 1024:.1f} MB")
print(f"Available Memory:        {mem_avail / 1024:.1f} MB ({pct_avail:.1f}%)")
print(f"Swap Total:              {swap_total / 1024:.1f} MB")
print(f"Swap Free:               {swap_free / 1024:.1f} MB")
print("-" * 55)
print(f"Diagnostic Insight: MemAvailable is {mem_avail / (mem_free or 1):.1f}x larger than raw MemFree.")
print("Conclusion: Evaluating memory health on MemFree alone generates severe false alarms.")
EOF
python3 "$LAB_DIR/parse_meminfo.py" | tee "$LAB_DIR/memory_telemetry.log"
```

**Expected result:** Output displays memory breakdown, confirming `MemAvailable` accounts for reclaimable page cache and exceeds raw `MemFree`.

**Save:** `$LAB_DIR/memory_telemetry.log`''',

                '''**Stage 6: Rehearse classification of supplied OOM and PSI telemetry**

**Location:** local bash terminal

Create and execute a telemetry classifier script that parses supplied incident fixtures (dmesg OOM logs and `/proc/pressure` metrics), distinguishing container cgroup quota limits from host-wide memory exhaustion:

```bash
cat > "$LAB_DIR/classify_incident.py" <<'EOF'
import sys

supplied_dmesg = """
[18492.104] Memory cgroup out of memory: Killed process 4182 (order-worker) total-vm:812044kB, anon-rss:518420kB, file-rss:1240kB, shmem-rss:0kB
[18492.105] oom_reaper: reaped process 4182 (order-worker), now anon-rss:0kB
"""

supplied_cgroup_events = """
low 0
high 0
max 14
oom 14
oom_kill 14
"""

supplied_psi_memory = """
some avg10=22.45 avg60=14.20 avg300=5.10 total=48201944
full avg10=18.12 avg60=11.05 avg300=3.80 total=31204550
"""

supplied_psi_cpu = """
some avg10=0.00 avg60=0.00 avg300=0.00 total=1240
"""

print("=== Diagnostic Classification of Incident Telemetry ===")

# Check for Cgroup OOM
is_cgroup_oom = "Memory cgroup out of memory" in supplied_dmesg
oom_kills = 0
for line in supplied_cgroup_events.strip().splitlines():
    if line.startswith("oom_kill"):
        oom_kills = int(line.split()[1])

# Parse Memory PSI
mem_some_10 = 0.0
mem_full_10 = 0.0
for line in supplied_psi_memory.strip().splitlines():
    if line.startswith("some"):
        mem_some_10 = float(line.split("avg10=")[1].split()[0])
    elif line.startswith("full"):
        mem_full_10 = float(line.split("avg10=")[1].split()[0])

print(f"1. Cgroup Boundary Violation:   {'DETECTED' if is_cgroup_oom else 'ABSENT'}")
print(f"2. Recorded Cgroup OOM Kills:    {oom_kills}")
print(f"3. Memory PSI 'some' (10s avg):  {mem_some_10}%")
print(f"4. Memory PSI 'full' (10s avg):  {mem_full_10}%")
print(f"5. CPU PSI 'some' (10s avg):     0.0%")
print("-" * 55)

if is_cgroup_oom and oom_kills > 0 and mem_some_10 > 10.0:
    print("CLASSIFICATION: SEVERE CGROUP MEMORY EXHAUSTION DETECTED.")
    print("RECOMMENDATION: Resize container cgroup memory.max; host VM resize will NOT resolve this.")
else:
    print("CLASSIFICATION: Inconclusive or normal state.")
    sys.exit(1)
EOF
python3 "$LAB_DIR/classify_incident.py" | tee "$LAB_DIR/incident_classification.log"
```

**Expected result:** Classifier identifies cgroup OOM boundary violation and severe memory pressure, outputting the correct architectural recommendation.

**Save:** `$LAB_DIR/incident_classification.log`''',

                r'''**Stage 7: Diagnose evidence and compile resource baseline report**

**Location:** local bash terminal

Synthesize the CPU execution telemetry, physical memory breakdown, and incident classifications into a comprehensive resource baseline audit report:

```bash
cat > "$LAB_DIR/resource_baseline_report.md" <<EOF
# System Resource Baseline and Diagnostic Signal Report

## 1. System Baseline Summary
- **Timestamp:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Architecture:** $(uname -m)
- **Kernel Version:** $(uname -r)
- **Host CPU Cores:** $(nproc)

## 2. Bounded CPU Workload Telemetry
$(cat "$LAB_DIR/cpu_telemetry.log")

## 3. Host Memory Distribution
$(cat "$LAB_DIR/memory_telemetry.log")

## 4. Predicted Symptoms: CPU Throttling vs Memory Pressure
| Diagnostic Symptom | CPU Quota Throttling | Memory Pressure / OOM |
| :--- | :--- | :--- |
| **Primary Telemetry** | CPU PSI (\`cpu:some\`) elevated; high run queue | Memory PSI (\`memory:some\`, \`memory:full\`) elevated |
| **Process State** | Tasks runnable but delayed in scheduler queue | Tasks blocked in uninterruptible sleep (D) reclaiming RAM |
| **Context Switching** | Elevated involuntary context switches (\`ru_nivcsw\`) | Low CPU activity; high major page faults |
| **Crash Signature** | Does not terminate process; causes latency spikes | Process terminated abruptly with exit code 137 (SIGKILL) |
| **Kernel Log Proof** | CPU CFS bandwidth throttling counters increment | \`Memory cgroup out of memory: Killed process\` in dmesg |
| **Corrective Action** | Increase cgroup CPU quota / provision dedicated cores | Increase cgroup \`memory.max\` or fix application memory leak |

## 5. Verification Conclusion
The evidence establishes that MemAvailable accounts for reclaimable page cache and confirms that container cgroup memory.max limits operate independently of host VM physical memory capacity.
EOF
cat "$LAB_DIR/resource_baseline_report.md"
```

**Expected result:** Markdown report compiles all test findings and clearly distinguishes CPU throttling from memory pressure symptoms.

**Save:** `$LAB_DIR/resource_baseline_report.md`''',

                '''**Stage 8: Clean up lab workspace**

**Location:** local bash terminal

Remove temporary benchmark scripts and data files:

```bash
rm -rf "$LAB_DIR"
echo "PASS: Day 8 Topic 1 lab workspace cleaned up successfully."
```

**Expected result:** Workspace directory removed; environment clean.

**Save:** none'''
            ]
        }
    },

    'topic-02': {
        'scenario': {
            'scenario': 'Text search misses structured 503 records',
            'impact': 'Silent customer order checkout failures accumulate undetected in production payment gateways because monitoring alerts rely on string matching rather than HTTP status codes.',
            'constraints': 'Preserve raw historical log fixtures unchanged; do not run unapproved packet captures on shared network interfaces; validate log schema before asserting health.',
            'evidence': '''**illustrative supplied records**

```text
[Synthetic Log Fixture: /var/log/orders.jsonl]
{"timestamp":"2026-10-04T10:00:01Z","order_id":"ord-101","status":200,"latency_ms":42,"region":"us-central1"}
{"timestamp":"2026-10-04T10:00:02Z","order_id":"ord-102","status":503,"latency_ms":1250,"region":"us-central1","gateway":"auth-v2","detail":"upstream_connect_timeout"}
{"timestamp":"2026-10-04T10:00:03Z","order_id":"ord-103","status":200,"latency_ms":38,"region":"us-central1"}

[Naive Operator Triage via Grep]
$ grep -i "error" /var/log/orders.jsonl
(no output returned, exit status 1)

[Operator Conclusion Reported on Incident Bridge]
"Log inspection complete: 0 errors detected in /var/log/orders.jsonl. Outage report is a false alarm."

[Simultaneous Customer Telemetry]
Payment Gateway Error Rate: 33.3% checkout failures; HTTP 503 Service Unavailable returned to clients.
```''',
            'root': 'The operational monitoring filter utilized unstructured text grepping for the literal substring "error". The application generates structured JSON logs where failure events are encoded as numeric integer fields (`"status": 503`) accompanied by operational reason strings (`"upstream_connect_timeout"`). Because the record omitted the exact literal string "error", the flat text search returned an empty result, leading the operator to erroneously declare zero customer failures.',
            'verify': 'Replace unstructured text regex filtering with structured JSON parsing using `jq` or Python JSON processors selecting records where `.status >= 500`. The parser immediately isolates order `ord-102` with status 503 and latency 1250ms, proving failure occurrence.',
            'residual': 'Testing numeric HTTP status codes detects application and gateway errors but does not catch semantic payload failures that return HTTP 200 with an embedded business rejection; application-level schema assertions must complement HTTP status filtering.',
            'diagram_enabled': True,
            'facts': 'Fixture contains 3 JSON orders, one of which failed with status 503; grep for "error" returns 0 lines; customers experienced 33% transaction failures.',
            'inference': 'Flat text pattern searching fails on structured JSON logs because numeric status codes and non-"error" reason codes bypass substring filters.',
            'expected': 'Schema-aware JSON evaluation extracts the failed record and isolates the exact failure timestamp and gateway timeout cause.',
            'diagnostic_steps': [
                'Inspect log file formatting to confirm serialization structure (JSON Lines format).',
                'Execute unstructured grep to reproduce the false-negative observation.',
                'Execute structured jq/Python filter to query numeric status field for values >= 500.',
                'Map downstream network boundaries (DNS, socket, packet, HTTP) to investigate gateway timeout.'
            ],
            'remediation_steps': [
                'Decommission unstructured regex log alerts across monitoring dashboards.',
                'Implement structured JSON query filters targeting numeric status fields (e.g. status >= 500).',
                'Deploy synthetic endpoint validation scripts asserting on HTTP response codes.'
            ],
            'diagram': (
                "Customer checkout failure",
                "Substring text search",
                "Silent false negative",
                "Schema-aware JSON filter",
                "100% 5xx errors isolated"
            ),
            'icons': [
                '../assets/icons/generic/artifact.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/decision.svg',
                '../assets/icons/generic/outcome.svg'
            ]
        },
        'lab': {
            'name': 'Diagnostic toolchain evaluation: structured parsing vs network boundary isolation',
            'goal': 'Demonstrate why unstructured text search fails on structured JSON logs, implement schema-aware filtering, and map diagnostic network tools across isolation boundaries.',
            'expected': 'Proof of false-negative outcome with grep, successful 100% extraction of failure records with structured parser, and inspection of local socket states via ss.',
            'mode': 'Observed locally: log parsing, Python JSON filtering, and local ss socket inspection. Simulated or predicted: network packet flow mapping. Untested on GCP: live VPC packet mirroring.',
            'covers': 'grep/sed/awk/jq and curl/dig/ss/tcpdump as diagnostic tools. Learn to interpret one signal at a time.',
            'prereq': 'Local Linux bash terminal with Python 3, grep, and ss.',
            'preflight': 'Verify grep, python3, and ss availability in PATH.',
            'verification': 'Validate that grep returns 0 matches while structured parser outputs ord-102 with status 503.',
            'trouble': 'If ss requires root privileges for process mapping, execute with -tln to view listening sockets without PID flags.',
            'cleanup': 'Remove synthetic log fixtures and diagnostic scripts.',
            'accept': 'Comprehensive diagnostic toolchain report ($LAB_DIR/diagnostic_toolchain_report.md) generated and verified.',
            'file': 'day-008-topic-02.md',
            'steps': [
                '''**Stage 1: Preflight environment and command check**

**Location:** local bash terminal

Confirm availability of core utilities used across the diagnostic sequence:

```bash
command -v grep >/dev/null && echo "PASS: grep is available"
command -v sed >/dev/null && echo "PASS: sed is available"
command -v awk >/dev/null && echo "PASS: awk is available"
command -v python3 >/dev/null && echo "PASS: python3 is available"
command -v ss >/dev/null && echo "PASS: ss is available"
```

**Expected result:** All diagnostic tools confirmed present in system PATH.

**Save:** none''',

                '''**Stage 2: Create synthetic structured log fixture**

**Location:** local bash terminal

Initialize a test workspace and create a synthetic JSON Lines (`.jsonl`) order log fixture with varied HTTP statuses and field order:

```bash
LAB_DIR="/home/naveen/GitRepos/Projects/GCP/RoadMap/gcp-180day-architect-site/scratch/day_008_lab_t2"
mkdir -p "$LAB_DIR"
cd "$LAB_DIR"

cat > "$LAB_DIR/orders.jsonl" <<'EOF'
{"timestamp":"2026-10-04T10:00:01Z","order_id":"ord-101","status":200,"latency_ms":42,"region":"us-central1"}
{"timestamp":"2026-10-04T10:00:02Z","order_id":"ord-102","status":503,"latency_ms":1250,"region":"us-central1","detail":"upstream_connect_timeout"}
{"timestamp":"2026-10-04T10:00:03Z","order_id":"ord-103","status":200,"latency_ms":38,"region":"us-central1"}
{"timestamp":"2026-10-04T10:00:04Z","order_id":"ord-104","status":404,"latency_ms":12,"region":"us-east1","detail":"item_not_found"}
{"timestamp":"2026-10-04T10:00:05Z","order_id":"ord-105","status":500,"latency_ms":890,"region":"us-central1","detail":"database_deadlock"}
EOF

cat "$LAB_DIR/orders.jsonl"
```

**Expected result:** Synthetic log fixture created with 5 structured order records.

**Save:** `$LAB_DIR/orders.jsonl`''',

                '''**Stage 3: Demonstrate false-negative failure mode of unstructured grep**

**Location:** local bash terminal

Execute naive text searches across the log fixture to demonstrate why flat text search fails on structured data:

```bash
echo "=== Test 1: Searching for literal 'error' ==="
if grep -i "error" "$LAB_DIR/orders.jsonl"; then
  echo "Found errors via text search"
else
  echo "RESULT: grep found 0 matches (exit code 1)."
  echo "EXPLANATION: None of the records contain the literal string 'error', despite 503 and 500 failures!"
fi

echo "=== Test 2: Naive regex search for '503' ==="
grep "503" "$LAB_DIR/orders.jsonl"
echo "EXPLANATION: While this finds line 2, it would also falsely match user ID 'user_503' or latency '503ms'!"
```

**Expected result:** Literal grep for "error" returns zero records, proving the diagnostic blind spot.

**Save:** `$LAB_DIR/grep_test.log`''',

                '''**Stage 4: Author and execute schema-aware structured JSON parser**

**Location:** local bash terminal

Implement a structured Python filter that validates JSON syntax and selects records using numeric comparison (`status >= 500`):

```bash
cat > "$LAB_DIR/parse_orders.py" <<'EOF'
import json
import sys

log_file = sys.argv[1] if len(sys.argv) > 1 else "orders.jsonl"
total_records = 0
failed_records = []

with open(log_file, 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        total_records += 1
        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"ERROR: Corrupted JSON on line {line_num}: {e}")
            continue

        status = record.get("status")
        # Strict numeric filtering
        if isinstance(status, int) and status >= 500:
            failed_records.append(record)

print(f"Total Records Analyzed:     {total_records}")
print(f"5xx Server Errors Detected: {len(failed_records)}")
print("-" * 55)
for rec in failed_records:
    print(f"FAILED ORDER: {rec.get('order_id')} | Status: {rec.get('status')} | Latency: {rec.get('latency_ms')}ms | Reason: {rec.get('detail')}")

if len(failed_records) == 2:
    print("\nPASS: Successfully isolated 100% of server errors (ord-102 and ord-105).")
else:
    print(f"\nFATAL: Expected 2 failed records, found {len(failed_records)}")
    sys.exit(1)
EOF
python3 "$LAB_DIR/parse_orders.py" "$LAB_DIR/orders.jsonl" | tee "$LAB_DIR/structured_parse.log"
```

**Expected result:** Parser extracts ord-102 (503) and ord-105 (500) accurately using numeric criteria.

**Save:** `$LAB_DIR/structured_parse.log`''',

                '''**Stage 5: Inspect local socket state machine using ss**

**Location:** local bash terminal

Query Linux kernel socket tables to observe active TCP sockets, listening ports, and queue depths:

```bash
echo "=== Active TCP Listening Sockets ===" | tee "$LAB_DIR/sockets.log"
ss -tln | tee -a "$LAB_DIR/sockets.log"

echo "=== Socket Summary Statistics ===" | tee -a "$LAB_DIR/sockets.log"
ss -s | tee -a "$LAB_DIR/sockets.log"
```

**Expected result:** Output displays kernel socket summary and listening TCP endpoints with zero Recv-Q congestion.

**Save:** `$LAB_DIR/sockets.log`''',

                '''**Stage 6: Rehearse network diagnostic boundary isolation mapping**

**Location:** local bash terminal

Create an automated boundary tester script that documents the ordered diagnostic workflow:

```bash
cat > "$LAB_DIR/boundary_tester.py" <<'EOF'
boundaries = [
    {"stage": 1, "boundary": "DNS Resolution", "tool": "dig +short api.example.com", "validates": "Hostname maps to valid IP address"},
    {"stage": 2, "boundary": "TCP Socket Establishment", "tool": "ss -tna | grep <IP>:<PORT>", "validates": "TCP SYN/ACK handshake completed (ESTAB)"},
    {"stage": 3, "boundary": "Packet Interface Path", "tool": "tcpdump -nn -c 5 host <IP>", "validates": "Packets physically reaching local network interface"},
    {"stage": 4, "boundary": "Application Transport / TLS", "tool": "curl -Iv https://api.example.com", "validates": "TLS certificate verified and HTTP status received"},
    {"stage": 5, "boundary": "Structured Payload Schema", "tool": "python3 / jq select(.status >= 500)", "validates": "Payload contains valid JSON and parses status codes"}
]

print("=== Standard Operating Procedure: Boundary-Ordered Diagnostics ===")
for b in boundaries:
    print(f"Stage {b['stage']}: [{b['boundary']}]")
    print(f"  Command:   {b['tool']}")
    print(f"  Validates: {b['validates']}")
print("-" * 65)
print("Diagnostic Principle: Test one boundary at a time; never jump to application conclusions before transport proof.")
EOF
python3 "$LAB_DIR/boundary_tester.py" | tee "$LAB_DIR/boundary_sop.log"
```

**Expected result:** Structured diagnostic sequence printed, outlining boundary separation principles.

**Save:** `$LAB_DIR/boundary_sop.log`''',

                r'''**Stage 7: Diagnose evidence and compile diagnostic toolchain report**

**Location:** local bash terminal

Compile the comparative log parsing results and boundary diagnostics into a comprehensive operational audit report:

```bash
cat > "$LAB_DIR/diagnostic_toolchain_report.md" <<EOF
# Command-Line Diagnostic Toolchain Audit Report

## 1. Summary
- **Timestamp:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Investigator:** Site Reliability Engineering
- **Target Fixture:** \`orders.jsonl\` (5 structured records)

## 2. Text Search vs Structured Parsing Comparison
| Tool / Methodology | Query Syntax | Result Observed | Accuracy Assessment |
| :--- | :--- | :--- | :--- |
| **Naive Grep** | \`grep -i "error"\` | 0 records returned (exit 1) | **FALSE NEGATIVE**: Missed all 5xx outages |
| **Positional Regex** | \`grep "503"\` | 1 record returned | **FRAGILE**: Matches non-status numbers |
| **Structured JSON** | \`select(.status >= 500)\` | 2 records returned (\`ord-102\`, \`ord-105\`) | **100% ACCURATE**: Schema-validated |

## 3. Network Boundary Tool Selection
- **DNS Boundary:** Use \`dig\` to verify resolver answers independently of transport.
- **Kernel Socket Boundary:** Use \`ss -tln\` to verify local port binding and backlog queue depth.
- **Packet Interface Boundary:** Use \`tcpdump\` with BPF filters to verify physical interface transit.
- **Application Boundary:** Use \`curl -v\` to isolate TLS negotiation from HTTP status handling.

## 4. Conclusion
Unstructured text searching must never be used as an acceptance gate for structured JSON telemetry. Diagnostic procedures must test boundaries hierarchically from DNS through socket, packet, transport, and schema validation.
EOF
cat "$LAB_DIR/diagnostic_toolchain_report.md"
```

**Expected result:** Comprehensive markdown report generated comparing parsing methods and boundary isolation.

**Save:** `$LAB_DIR/diagnostic_toolchain_report.md`''',

                '''**Stage 8: Clean up lab workspace**

**Location:** local bash terminal

Remove temporary fixtures and testing scripts:

```bash
rm -rf "$LAB_DIR"
echo "PASS: Day 8 Topic 2 lab workspace cleaned up successfully."
```

**Expected result:** Workspace directory removed; environment clean.

**Save:** none'''
            ]
        }
    }
}
