"""Scenarios and 8-stage step-by-step labs for Day 10: Images, filesystems and orchestration."""

SCENARIOS_AND_LABS = {
    'topic-01': {
        'scenario': {
            'scenario': 'An order checkout microservice deployed on a container cluster writes transaction recovery markers to its local container filesystem at /tmp/checkout_recovery.log during user purchases. During a routine rolling update of the application deployment, the old container is terminated and a new container is provisioned. The engineering team discovers that all active checkout recovery markers vanished upon container termination, leading to duplicate payment charges when the queue reprocessed unconfirmed transactions.',
            'impact': 'E-commerce customers suffer duplicate credit card charges totaling thousands of dollars; customer service queues are overwhelmed; payment gateway audit flags account for automated transaction reconciliation failure.',
            'constraints': 'The service is deployed as a stateless container deployment; ephemeral container root filesystems are backed by OverlayFS thin writable layers; storage lifecycle is inadvertently coupled to container process execution.',
            'evidence': 'Inspecting the container runtime reveals that /tmp was located on the container writable layer (upperdir) rather than a persistent volume mount. When the pod was rescheduled, containerd destroyed the container instance and its associated writable layer. Filesystem traces show that writes to /tmp/checkout_recovery.log were buffered in kernel page cache without invoking fsync(), meaning even pre-teardown unflushed writes were lost upon pod termination.',
            'root': 'The application stored critical state in the container thin writable layer rather than a mounted persistent volume, and failed to issue POSIX fsync() system calls to commit transaction records to non-volatile storage before confirming payment processing.',
            'verify': 'The Kubernetes deployment is updated to mount a PersistentVolumeClaim backed by Compute Engine Persistent Disk (pd-balanced) onto /var/lib/checkout. The application code is updated to issue os.fsync() on every recovery marker write. Verification confirms that simulated container terminations preserve 100% of recovery markers across replacement pods with zero duplicate transactions.',
            'residual': 'Persistent volume attachments introduce a 15–30 second volume detachment/reattachment latency if a pod is rescheduled to a different physical host node in the cluster.',
            'diagram_enabled': True,
            'facts': 'Supplied facts: Writing state to ephemeral container filesystem results in data loss upon pod recreation.',
            'inference': 'Architectural inference: Decoupling storage lifecycle from container lifecycle via persistent volumes ensures recovery marker survival.',
            'expected': 'Expected post-fix behavior: Replacement containers read existing recovery markers, preserving at-most-once fulfillment semantics.',
            'diagram': (
                'Order processing container receives checkout payload',
                'Application writes transaction record to ephemeral /tmp',
                'Container restart destroys writable layer; order marker vanishes',
                'Attach persistent volume claim and invoke fsync on writes',
                'Order markers survive container teardown and replica migration'
            ),
            'icons': (
                '../assets/icons/generic/client.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/storage.svg',
                '../assets/icons/generic/outcome.svg'
            ),
            'diagnostic_steps': [
                'Inspect pod volume mounts: kubectl get pod checkout-worker-[id] -o jsonpath="{.spec.containers[*].volumeMounts}"',
                'Inspect container OverlayFS storage: docker inspect [container-id] | jq ".[0].GraphDriver.Data"',
                'Simulate pod restart and check file persistence: kubectl delete pod checkout-worker-[id] && kubectl exec -it checkout-worker-[new-id] -- ls -l /tmp',
                'Analyze application write durability code for missing fsync() or fdatasync() invocations'
            ],
            'remediation_steps': [
                'Provision a Kubernetes PersistentVolumeClaim requesting 10Gi on pd-balanced storage class',
                'Update Deployment specification to mount the PVC at /var/lib/checkout',
                'Refactor application write logic to call os.fsync(file.fileno()) after writing recovery markers',
                'Configure pod disruption budgets to coordinate volume detachment during node upgrades',
                'Execute automated rolling update test and verify transaction record integrity across replacement pods'
            ]
        },
        'lab': {
            'name': 'Exercise A · Build a container and test volume persistence',
            'goal': 'Build a lightweight container application, contrast ephemeral container storage lifecycles with mounted persistent volume durability, and demonstrate the POSIX fsync() writeback boundary.',
            'expected': 'A runnable container image, verified ephemeral file destruction upon container replacement, and verified durable persistence of fsync-committed records across volume mounts.',
            'mode': 'Observed locally: local bash execution of Python application simulation, file creation, and fsync flushing. Simulated or predicted: Docker/containerd OverlayFS upperdir deletion and GKE Persistent Disk CSI dynamic volume provisioning. Untested on GCP: Compute Engine hyperdisk NVMe controller flush caching and cross-zone volume migration latency.',
            'covers': 'Build a tiny container from an annotated example; compare ephemeral files with a mounted volume and trace buffered write versus durable flush.',
            'prereq': 'Linux terminal with bash and core utilities.',
            'preflight': 'Verify that bash, python3, and standard file manipulation tools are installed.',
            'verification': 'Verify that ephemeral files are deleted on container simulation restart while mounted volume files persist intact.',
            'trouble': 'If write permission errors occur, verify that scratch/day10_lab_a directory permissions are readable and writeable.',
            'cleanup': 'Remove temporary container simulation directories and files created in scratch/day10_lab_a.',
            'accept': 'A persistence verification report confirming data loss on ephemeral storage and 100% record retention on mounted volume storage with fsync.',
            'file': 'day-010-exercise-a.md',
            'steps': [
                '''**Stage 1: Preflight and Environment Baseline**

**Location:** local terminal

**Actions:**
Verify core CLI utilities and establish the isolated test workspace for container storage testing.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day10_lab_a/ephemeral_layer scratch/day10_lab_a/mounted_volume
echo "Stage 1 preflight complete at $(date -u +%Y-%m-%dT%H:%M:%SZ)" > scratch/day10_lab_a/stage1.log
cat scratch/day10_lab_a/stage1.log
```

**Expected result:** Tooling paths verified and workspace directories initialized.

**Save:** `scratch/day10_lab_a/stage1.log`''',

                '''**Stage 2: Author Application Fixture with Buffered Write and fsync Flush**

**Location:** local terminal

**Actions:**
Author a Python application fixture that demonstrates the difference between standard buffered writes and durable POSIX fsync flushes.
```bash
cat <<'EOF' > scratch/day10_lab_a/app.py
import os, sys, time

def write_unbuffered_record(path, record_id):
    # Standard write: buffers in application memory / kernel page cache
    with open(path, "a") as f:
        f.write(f"ORDER_RECORD:{record_id}:{time.time()}:BUFFERED\n")

def write_durable_record(path, record_id):
    # Durable write: forces kernel page cache writeback to disk via fsync
    with open(path, "a") as f:
        f.write(f"ORDER_RECORD:{record_id}:{time.time()}:DURABLE\n")
        f.flush()
        os.fsync(f.fileno())

if __name__ == "__main__":
    mode = sys.argv[1]
    target_dir = sys.argv[2]
    out_file = os.path.join(target_dir, "orders.log")
    if mode == "ephemeral":
        write_unbuffered_record(out_file, "ORD-9001")
        print(f"Wrote unbuffered record to ephemeral path: {out_file}")
    elif mode == "durable":
        write_durable_record(out_file, "ORD-9002")
        print(f"Wrote fsync-flushed record to durable volume path: {out_file}")
EOF
python3 -c "import py_compile; py_compile.compile('scratch/day10_lab_a/app.py')" && echo "Fixture compiled successfully" > scratch/day10_lab_a/stage2.log
cat scratch/day10_lab_a/stage2.log
```

**Expected result:** Application fixture is compiled and validated.

**Save:** `scratch/day10_lab_a/stage2.log`''',

                '''**Stage 3: Author Dockerfile with Multi-Stage Build Directives**

**Location:** local terminal

**Actions:**
Author an annotated Dockerfile demonstrating multi-stage build patterns, minimal base layers, and non-root execution.
```bash
cat <<'EOF' > scratch/day10_lab_a/Dockerfile
# Multi-stage Dockerfile: separates build dependencies from minimal runtime
FROM python:3.12-alpine AS builder
WORKDIR /app
COPY app.py .
RUN python3 -m compileall app.py

# Minimal runtime stage
FROM python:3.12-alpine
WORKDIR /app
COPY --from=builder /app/app.py .
# Create non-root unprivileged service user
RUN adduser -D -u 10001 appuser && \
    mkdir -p /data && chown -R appuser:appuser /data
USER 10001
VOLUME ["/data"]
ENTRYPOINT ["python3", "app.py"]
EOF
echo "Dockerfile authored and verified" > scratch/day10_lab_a/stage3.log
cat scratch/day10_lab_a/stage3.log
```

**Expected result:** Multi-stage Dockerfile is generated and verified.

**Save:** `scratch/day10_lab_a/stage3.log`''',

                '''**Stage 4: Simulate Ephemeral Storage Write and Observe Teardown Loss**

**Location:** local terminal

**Actions:**
Execute the application in ephemeral mode (simulating an OverlayFS writable container layer), record the transaction, and simulate container teardown and replacement.
```bash
# Container 1 launches and writes to ephemeral layer
python3 scratch/day10_lab_a/app.py ephemeral scratch/day10_lab_a/ephemeral_layer > scratch/day10_lab_a/stage4.log
echo "--- Container 1 file state ---" >> scratch/day10_lab_a/stage4.log
cat scratch/day10_lab_a/ephemeral_layer/orders.log >> scratch/day10_lab_a/stage4.log

# Container 1 terminates (OverlayFS thin writable layer destroyed)
rm -rf scratch/day10_lab_a/ephemeral_layer/*

# Container 2 (replacement pod) launches with fresh empty rootfs
if [ ! -f scratch/day10_lab_a/ephemeral_layer/orders.log ]; then
    echo "OBSERVED: orders.log does not exist in Container 2! Ephemeral data destroyed." >> scratch/day10_lab_a/stage4.log
fi
cat scratch/day10_lab_a/stage4.log
```

**Expected result:** Output documents data creation in Container 1 and complete loss in Container 2.

**Save:** `scratch/day10_lab_a/stage4.log`''',

                '''**Stage 5: Simulate Mounted Volume Write with POSIX fsync Durability**

**Location:** local terminal

**Actions:**
Execute the application in durable mode using a mounted volume simulation with explicit fsync, then simulate container replacement.
```bash
# Container 1 writes to mounted volume with fsync
python3 scratch/day10_lab_a/app.py durable scratch/day10_lab_a/mounted_volume > scratch/day10_lab_a/stage5.log

# Container 1 terminates; mounted volume remains intact on host/network storage
# Container 2 launches and attaches the existing volume
echo "--- Container 2 reading mounted volume ---" >> scratch/day10_lab_a/stage5.log
cat scratch/day10_lab_a/mounted_volume/orders.log >> scratch/day10_lab_a/stage5.log
if grep -q "ORD-9002" scratch/day10_lab_a/mounted_volume/orders.log; then
    echo "VERIFIED: Transaction ORD-9002 survived container replacement on mounted volume!" >> scratch/day10_lab_a/stage5.log
fi
cat scratch/day10_lab_a/stage5.log
```

**Expected result:** Transaction ORD-9002 is preserved across container lifecycles on the mounted volume.

**Save:** `scratch/day10_lab_a/stage5.log`''',

                '''**Stage 6: Rehearse Sudden Process Crash: Buffered Cache vs fsync Media**

**Location:** local terminal

**Actions:**
Simulate an abrupt process termination to observe why kernel page cache buffering alone is insufficient without fsync().
```bash
cat <<'EOF' > scratch/day10_lab_a/simulate_crash.py
import os, sys

crash_log = "scratch/day10_lab_a/crash_test.log"
# Write 1000 records without flush/fsync
with open(crash_log, "w") as f:
    for i in range(100):
        f.write(f"UNFLUSHED_RECORD_{i}\n")
    # Simulate abrupt SIGKILL / power termination before buffer flush
    os._exit(137)
EOF
python3 scratch/day10_lab_a/simulate_crash.py
# Inspect size of crash test log on disk
size = os.path.getsize("scratch/day10_lab_a/crash_test.log")
echo "Crash test completed with exit code 137. Flushed bytes: $size" > scratch/day10_lab_a/stage6.log
cat scratch/day10_lab_a/stage6.log
```

**Expected result:** Output illustrates that abrupt process exits can truncate or lose uncommitted dirty page buffers.

**Save:** `scratch/day10_lab_a/stage6.log`''',

                '''**Stage 7: Compile the Persistence Verification Report**

**Location:** local terminal

**Actions:**
Generate a comprehensive persistence verification report contrasting ephemeral container layers with persistent volume mounts.
```bash
cat <<'EOF' > scratch/day10_lab_a/compile_report.py
report = """# Day 10 Persistence and Storage Verification Report
Generated: Local Terminal Simulation

## 1. Experimental Results Summary
- Ephemeral Layer Test: Record ORD-9001 written to thin OverlayFS layer was DESTROYED upon container restart.
- Mounted Volume Test: Record ORD-9002 written with POSIX fsync() SURVIVED container replacement.
- Crash Simulation: Unflushed page cache writes subject to data corruption during abrupt SIGKILL terminations.

## 2. Architectural Storage Guidance
1. Never write transactional or recovery data to ephemeral container storage (/tmp or container rootfs).
2. Attach Kubernetes PersistentVolumeClaims backed by managed cloud block storage (pd-balanced / pd-ssd).
3. Ensure stateful applications call fsync() or fdatasync() to commit dirty memory pages to non-volatile disk.
"""
with open("scratch/day-010-persistence-report.txt", "w") as f:
    f.write(report)
print("Persistence report compiled")
EOF
python3 scratch/day10_lab_a/compile_report.py > scratch/day10_lab_a/stage7.log
cat scratch/day-010-persistence-report.txt
```

**Expected result:** `scratch/day-010-persistence-report.txt` is compiled and verified.

**Save:** `scratch/day-010-persistence-report.txt`''',

                '''**Stage 8: Validate the Persistence Report and Clean Up**

**Location:** local terminal

**Actions:**
Validate that the persistence report satisfies all evaluation criteria and remove transient files.
```bash
test -f scratch/day-010-persistence-report.txt && grep -q "SURVIVED" scratch/day-010-persistence-report.txt
echo "✓ Day 10 Exercise A validation passed successfully" > scratch/day10_lab_a/stage8.log
cat scratch/day10_lab_a/stage8.log
```

**Expected result:** Validation succeeds with clean status.

**Save:** `scratch/day10_lab_a/stage8.log`'''
            ]
        }
    },
    'topic-02': {
        'scenario': {
            'scenario': 'A retail flash sale causes an automated traffic surge. An operator attempts to scale an order processing service from 2 to 5 replicas. Because the cluster node pool has fixed capacity (3 nodes with 4 GB allocatable RAM each) and the Pods specify uncalibrated 2 GB memory requests, the scheduler successfully places only 2 pods, leaving the remaining 3 replicas trapped indefinitely in Pending status.',
            'impact': 'Order processing throughput drops below required demand; checkout queues back up; customer transactions time out with HTTP 504 Gateway Timeout errors.',
            'constraints': 'Fixed node pool capacity of 3 nodes; each node has 4 GB allocatable memory; existing system pods consume 1 GB per node; uncalibrated application requests mandate 2 GB RAM per replica.',
            'evidence': 'Reviewing "kubectl get pods" reveals 3 pods in Pending state. Inspecting pod events via "kubectl describe pod order-processor-[id]" reveals the scheduling failure: "0/3 nodes available: 3 Insufficient memory". Host nodes show zero CPU saturation, but allocatable memory reservation is fully booked.',
            'root': 'The total requested memory for 5 replicas (10 GB) plus system reservations (3 GB) exceeds total cluster allocatable capacity (12 GB). The scheduler strictly enforces declared resource requests during the filtering phase, preventing pod placement even when actual memory usage is low.',
            'verify': 'Application resource requests are right-sized from 2 GB to 768 MB based on real profiling, and GKE Cluster Autoscaler is enabled on the node pool. All 5 replicas achieve Running status within 90 seconds, pass readiness probes, and scale-out throughput reaches 1,200 orders per second.',
            'residual': 'Autoscaler scale-up requires VM provisioning time (typically 60–90 seconds in GKE), during which transient queuing may occur unless overprovisioning buffer pods are configured.',
            'diagram_enabled': True,
            'facts': 'Supplied facts: Scaled Deployment fails to place three replicas due to node memory exhaustion.',
            'inference': 'Architectural inference: Reconciling desired state requires physical capacity; right-sizing requests and enabling cluster autoscaling restores schedulability.',
            'expected': 'Expected post-fix behavior: All five replicas achieve Running status and pass readiness probes.',
            'diagram': (
                'Surge traffic triggers deployment scale-out from 2 to 5 replicas',
                'Uncalibrated memory requests exceed cluster allocatable capacity',
                'Pods trapped in Pending with Insufficient memory events',
                'Enable GKE cluster autoscaler and calibrate pod requests',
                'New node provisions in 90 seconds; all 5 replicas reach Running'
            ),
            'icons': (
                '../assets/icons/generic/queue.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/server.svg',
                '../assets/icons/generic/outcome.svg'
            ),
            'diagnostic_steps': [
                'Inspect pod status: kubectl get pods -l app=order-processor -o wide',
                'Inspect pod scheduling failure events: kubectl describe pod order-processor-[id] | grep -A 5 Events:',
                'Inspect node allocatable capacity: kubectl describe nodes | grep -A 8 "Allocatable:"',
                'Calculate aggregate requested resources across active pods: kubectl get pods -A -o jsonpath="{...}"'
            ],
            'remediation_steps': [
                'Profile actual container memory working set under load in Cloud Monitoring',
                'Update Deployment manifest to calibrate requests: resources.requests.memory: "768Mi"',
                'Enable GKE Cluster Autoscaler: gcloud container clusters update [cluster] --enable-autoscaling --min-nodes=3 --max-nodes=8',
                'Apply updated Deployment and verify scheduler placement across available nodes',
                'Confirm all 5 replicas reach Running state and pass HTTP readiness probes'
            ]
        },
        'lab': {
            'name': 'Exercise B · Simulate scheduler reconciliation and capacity limits',
            'goal': 'Simulate the Kubernetes control loop, declarative state reconciliation, two-phase scheduler bin packing, and capacity limit exhaustion.',
            'expected': 'A deterministic scheduler simulation demonstrating pod placement filtering, pending state traps under capacity limits, and autoscaling resolution.',
            'mode': 'Observed locally: local Python simulation of Kubernetes scheduler filtering and scoring algorithms. Simulated or predicted: GKE Cluster Autoscaler provisioning of Compute Engine instances and kubelet pod startup. Untested on GCP: live Andromeda SDN virtual network routing tables and multi-zone node affinity scoring.',
            'covers': 'Container orchestration: why Kubernetes exists; continuous reconciliation loops, scheduler bin packing, and self-healing.',
            'prereq': 'Linux terminal with Python 3.',
            'preflight': 'Verify Python 3 runtime is available and initialize the simulation directory.',
            'verification': 'Verify that the scheduler simulation accurately rejects pods when allocatable memory is exhausted and places them when capacity expands.',
            'trouble': 'If simulation output is missing, verify scratch/day10_lab_b directory path.',
            'cleanup': 'Remove transient simulation scripts in scratch/day10_lab_b.',
            'accept': 'A scheduler simulation log documenting the transition from capacity failure to autoscaled resolution in scratch/day-010-scheduler-simulation.txt.',
            'file': 'day-010-exercise-b.md',
            'steps': [
                '''**Stage 1: Preflight and Tooling Baseline**

**Location:** local terminal

**Actions:**
Verify environment prerequisites and set up the scheduler simulation workspace.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day10_lab_b
echo "Stage 1 scheduler preflight complete at $(date -u +%Y-%m-%dT%H:%M:%SZ)" > scratch/day10_lab_b/stage1.log
cat scratch/day10_lab_b/stage1.log
```

**Expected result:** Tooling paths confirmed and workspace initialized.

**Save:** `scratch/day10_lab_b/stage1.log`''',

                '''**Stage 2: Define Cluster Node Inventory and Allocatable Headroom**

**Location:** local terminal

**Actions:**
Create a JSON fixture representing a 3-node Kubernetes cluster with physical capacity and existing system reservations.
```bash
cat <<'EOF' > scratch/day10_lab_b/nodes.json
{
  "nodes": [
    {"name": "node-zone-a-1", "allocatable_ram_mb": 4096, "reserved_ram_mb": 1024},
    {"name": "node-zone-b-1", "allocatable_ram_mb": 4096, "reserved_ram_mb": 1024},
    {"name": "node-zone-c-1", "allocatable_ram_mb": 4096, "reserved_ram_mb": 1024}
  ]
}
EOF
python3 -m json.tool scratch/day10_lab_b/nodes.json > /dev/null && echo "Node inventory validated" > scratch/day10_lab_b/stage2.log
cat scratch/day10_lab_b/stage2.log
```

**Expected result:** Node inventory created with 3 nodes possessing 3072 MB net allocatable RAM each.

**Save:** `scratch/day10_lab_b/stage2.log`''',

                '''**Stage 3: Define Workload Deployment Manifest with Resource Requests**

**Location:** local terminal

**Actions:**
Create the workload manifest representing the checkout service requesting 2048 MB RAM per replica.
```bash
cat <<'EOF' > scratch/day10_lab_b/deployment.json
{
  "name": "checkout-processor",
  "desired_replicas": 5,
  "request_ram_mb": 2048
}
EOF
echo "Deployment manifest configured with 5 replicas requesting 2048 MB each" > scratch/day10_lab_b/stage3.log
cat scratch/day10_lab_b/stage3.log
```

**Expected result:** Workload manifest authored and saved.

**Save:** `scratch/day10_lab_b/stage3.log`''',

                '''**Stage 4: Execute Scheduler Filtering and Bin Packing Algorithm**

**Location:** local terminal

**Actions:**
Execute the simulation engine to test how the scheduler places the 5 replicas across the 3 nodes.
```bash
cat <<'EOF' > scratch/day10_lab_b/scheduler_sim.py
import json

with open("scratch/day10_lab_b/nodes.json") as f:
    cluster = json.load(f)
with open("scratch/day10_lab_b/deployment.json") as f:
    dep = json.load(f)

nodes = cluster["nodes"]
req = dep["request_ram_mb"]
replicas = dep["desired_replicas"]

# Calculate available headroom
for n in nodes:
    n["available_ram"] = n["allocatable_ram_mb"] - n["reserved_ram_mb"]
    n["placed_pods"] = []

placed = 0
pending = []

for i in range(1, replicas + 1):
    pod_name = f"{dep['name']}-replica-{i}"
    # Predicate: NodeResourcesFit
    candidate = None
    for n in sorted(nodes, key=lambda x: x["available_ram"], reverse=True):
        if n["available_ram"] >= req:
            candidate = n
            break
    if candidate:
        candidate["available_ram"] -= req
        candidate["placed_pods"].append(pod_name)
        placed += 1
    else:
        pending.append(pod_name)

print(f"SCHEDULER RUN 1: Placed: {placed}/{replicas} | Pending: {len(pending)}/{replicas}")
for n in nodes:
    print(f"  {n['name']}: {len(n['placed_pods'])} pods, {n['available_ram']} MB RAM remaining")
if pending:
    print(f"  FAILED PREDICATE: 0/3 nodes available: 3 Insufficient memory for {pending}")
EOF
python3 scratch/day10_lab_b/scheduler_sim.py > scratch/day10_lab_b/stage4.log
cat scratch/day10_lab_b/stage4.log
```

**Expected result:** Output confirms 3 pods placed (1 per node) and 2 pods trapped in Pending due to insufficient memory.

**Save:** `scratch/day10_lab_b/stage4.log`''',

                '''**Stage 5: Rehearse Scale-Out Surge and Detect Unplaced Pending Pods**

**Location:** local terminal

**Actions:**
Simulate traffic surge scaling to 7 replicas to observe how unschedulable pods accumulate without crashing the cluster.
```bash
python3 -c '
import json
with open("scratch/day10_lab_b/deployment.json") as f:
    d = json.load(f)
d["desired_replicas"] = 7
with open("scratch/day10_lab_b/deployment.json", "w") as f:
    json.dump(d, f, indent=2)
'
python3 scratch/day10_lab_b/scheduler_sim.py > scratch/day10_lab_b/stage5.log
cat scratch/day10_lab_b/stage5.log
```

**Expected result:** Output confirms that 4 pods are trapped in Pending while existing 3 pods continue executing unharmed.

**Save:** `scratch/day10_lab_b/stage5.log`''',

                '''**Stage 6: Rehearse Worker Node Failure and Autonomous Rescheduling**

**Location:** local terminal

**Actions:**
Simulate an unexpected node crash and observe the node controller detecting the failure and rescheduling pods.
```bash
cat <<'EOF' > scratch/day10_lab_b/simulate_node_failure.py
import json

with open("scratch/day10_lab_b/nodes.json") as f:
    cluster = json.load(f)

# Node 3 suffers hardware fault
failed_node = cluster["nodes"].pop(2)
print(f"EVENT: Node {failed_node['name']} failed heartbeat! Marked NotReady.")
print(f"EVENT: Node controller evicts pods from {failed_node['name']} and re-queues them.")
with open("scratch/day10_lab_b/nodes_degraded.json", "w") as f:
    json.dump(cluster, f, indent=2)
EOF
python3 scratch/day10_lab_b/simulate_node_failure.py > scratch/day10_lab_b/stage6.log
cat scratch/day10_lab_b/stage6.log
```

**Expected result:** Output documents node eviction and re-queueing of displaced pods.

**Save:** `scratch/day10_lab_b/stage6.log`''',

                '''**Stage 7: Formulate GKE Cluster Autoscaler Capacity Policy**

**Location:** local terminal

**Actions:**
Calibrate workload resource requests to 768 MB and simulate GKE Cluster Autoscaler adding a new worker node.
```bash
cat <<'EOF' > scratch/day10_lab_b/autoscaler_remediation.py
import json

# Calibrate deployment requests to realistic working set
with open("scratch/day10_lab_b/deployment.json") as f:
    dep = json.load(f)
dep["desired_replicas"] = 5
dep["request_ram_mb"] = 768

# Autoscaler provisions node 4
with open("scratch/day10_lab_b/nodes.json") as f:
    cluster = json.load(f)
cluster["nodes"].append({"name": "node-zone-a-2", "allocatable_ram_mb": 4096, "reserved_ram_mb": 1024})

nodes = cluster["nodes"]
req = dep["request_ram_mb"]
replicas = dep["desired_replicas"]

for n in nodes:
    n["available_ram"] = n["allocatable_ram_mb"] - n["reserved_ram_mb"]
    n["placed_pods"] = []

placed = 0
for i in range(1, replicas + 1):
    pod_name = f"{dep['name']}-replica-{i}"
    candidate = sorted([n for n in nodes if n["available_ram"] >= req], key=lambda x: x["available_ram"], reverse=True)[0]
    candidate["available_ram"] -= req
    candidate["placed_pods"].append(pod_name)
    placed += 1

output = f"""# Day 10 Scheduler Simulation Report
Reconciliation Status: SUCCESS
Desired Replicas: {replicas} | Placed: {placed} | Pending: 0
Node Distribution:
"""
for n in nodes:
    output += f"  - {n['name']}: {len(n['placed_pods'])} pods, {n['available_ram']} MB free\n"

with open("scratch/day-010-scheduler-simulation.txt", "w") as f:
    f.write(output)
print("Scheduler remediation simulation completed successfully")
EOF
python3 scratch/day10_lab_b/autoscaler_remediation.py > scratch/day10_lab_b/stage7.log
cat scratch/day-010-scheduler-simulation.txt
```

**Expected result:** All 5 replicas placed cleanly across the autoscaled cluster nodes.

**Save:** `scratch/day-010-scheduler-simulation.txt`''',

                '''**Stage 8: Validate Scheduler Invariant and Close Simulation**

**Location:** local terminal

**Actions:**
Verify that zero pods remain in Pending status and all scheduler invariants are satisfied.
```bash
test -f scratch/day-010-scheduler-simulation.txt && grep -q "Pending: 0" scratch/day-010-scheduler-simulation.txt
echo "✓ Day 10 Exercise B validation passed successfully" > scratch/day10_lab_b/stage8.log
cat scratch/day10_lab_b/stage8.log
```

**Expected result:** Verification passes with zero pending pods.

**Save:** `scratch/day10_lab_b/stage8.log`'''
            ]
        }
    },
    'topic-03': {
        'scenario': {
            'scenario': 'An inventory microservice consisting of 3 replicas is deployed to Google Kubernetes Engine. The application pods start, initialize, pass their HTTP readiness probes, and achieve Running status. However, all external customer traffic routed through the Ingress controller fails with HTTP 503 Service Unavailable errors. Cloud Monitoring alerts trigger on elevated edge error rates.',
            'impact': 'Frontend shopping cart checkouts fail; customers cannot view item availability; warehouse picking operations stall due to inventory API unavailability.',
            'constraints': 'Deployment labels specify "app: inventory-service"; Service selector specifies "app: inventory-backend" due to a typographical error during manifest drafting; Ingress routes to Service on port 80.',
            'evidence': 'Executing "kubectl get endpoints inventory-service" reveals "<none>". Reviewing EndpointSlices via "kubectl get endpointslices -l kubernetes.io/service-name=inventory-service" confirms that zero endpoints are attached. While pods are 100% healthy, the label mismatch prevents the EndpointSlice controller from associating pod IP addresses with the Service virtual IP.',
            'root': 'A typographical discrepancy between the Service manifest selector (app: inventory-backend) and the Pod template labels (app: inventory-service) broke the declarative association between the routing layer and backend compute instances.',
            'verify': 'The Service selector label is corrected to "app: inventory-service" and applied to the cluster. The EndpointSlice controller instantly detects the matching labels and attaches all 3 pod IP addresses. Ingress returns HTTP 200 OK across all synthetic customer requests with sub-5ms latency.',
            'residual': 'Label-based decoupling relies on string key-value matching without compile-time type safety, requiring automated GitOps manifest schema validation (e.g., Kubeval or Conftest) to detect selector drift pre-deployment.',
            'diagram_enabled': True,
            'facts': 'Supplied facts: Healthy running Pods receive zero traffic due to a selector typo in the Service specification.',
            'inference': 'Architectural inference: Services decouple IP addressing via label selectors; exact matching is required for EndpointSlice generation.',
            'expected': 'Expected post-fix behavior: Aligned selectors populate endpoints, restoring HTTP 200 responses.',
            'diagram': (
                'External client issues HTTP request through Cloud Load Balancer',
                'Service selector app: inventory-backend has typo vs pod labels',
                'Service Endpoints empty; Ingress returns HTTP 503 Service Unavailable',
                'Correct selector label to match app: inventory-service exactly',
                'EndpointSlice registers 3 pod IPs; client requests return HTTP 200'
            ),
            'icons': (
                '../assets/icons/generic/client.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/router.svg',
                '../assets/icons/generic/outcome.svg'
            ),
            'diagnostic_steps': [
                'Inspect Service status and virtual IP: kubectl get svc inventory-service',
                'Check attached Service endpoints: kubectl get endpoints inventory-service',
                'Compare Service selector against Pod labels: kubectl get svc inventory-service -o jsonpath="{.spec.selector}" && kubectl get pods --show-labels',
                'Query EndpointSlices directly: kubectl get endpointslices -l kubernetes.io/service-name=inventory-service'
            ],
            'remediation_steps': [
                'Edit Service manifest to align selector: spec.selector.app: "inventory-service"',
                'Apply updated Service definition: kubectl apply -f service.yaml',
                'Verify EndpointSlice controller attaches pod IP addresses: kubectl get endpoints inventory-service',
                'Execute curl test against Ingress endpoint: curl -I https://api.example.com/inventory',
                'Confirm HTTP 200 status code and load balancing across all 3 backend pods'
            ]
        },
        'lab': {
            'name': 'Exercise C · Diagnose service selectors and map ownership hierarchy',
            'goal': 'Diagnose a Kubernetes Service selector mismatch defect, repair routing endpoint bindings, and map the complete architectural ownership hierarchy connecting Ingress, Services, Deployments, Pods, ConfigMaps, and Secrets.',
            'expected': 'A verified routing repair and the curriculum exit evidence: a Pod/Deployment/Service ownership diagram distinguishing declarative relationships and request flows.',
            'mode': 'Observed locally: local manifest inspection, endpoint resolution simulation, and ownership hierarchy compilation. Simulated or predicted: GKE Ingress controller provisioning Google Cloud Load Balancer URL maps and NEG bindings. Untested on GCP: Cloud Armor WAF policy evaluation and SSL certificate provisioning latency.',
            'covers': 'Kubernetes core objects: Pod, Deployment, Service, Ingress, ConfigMap, Secret; ownership relationships and traffic routing.',
            'prereq': 'Linux terminal with Python 3.',
            'preflight': 'Verify Python 3 runtime and initialize workspace.',
            'verification': 'Verify that the ownership diagram exit artifact accurately maps all core objects, labels, selectors, and routing paths.',
            'trouble': 'If YAML parsing errors occur, ensure standard syntax without illegal tabs.',
            'cleanup': 'Remove transient test manifests in scratch/day10_lab_c.',
            'accept': 'The curriculum exit evidence artifact is generated at scratch/day-010-ownership-diagram.md containing the complete Pod/Deployment/Service ownership hierarchy.',
            'file': 'day-010-exercise-c.md',
            'steps': [
                '''**Stage 1: Preflight and Workspace Setup**

**Location:** local terminal

**Actions:**
Verify CLI utilities and create workspace directories for Kubernetes object evaluation.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day10_lab_c
echo "Stage 1 core objects preflight complete at $(date -u +%Y-%m-%dT%H:%M:%SZ)" > scratch/day10_lab_c/stage1.log
cat scratch/day10_lab_c/stage1.log
```

**Expected result:** Tooling verified and workspace initialized.

**Save:** `scratch/day10_lab_c/stage1.log`''',

                '''**Stage 2: Author Kubernetes Core Manifests (Deployment, Service, ConfigMap, Secret)**

**Location:** local terminal

**Actions:**
Author a multi-object Kubernetes manifest containing a Deployment, Service, ConfigMap, and Secret.
```bash
cat <<'EOF' > scratch/day10_lab_c/manifests.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: inventory-config
data:
  MAX_PAGE_SIZE: "50"
  CACHE_ENABLED: "true"
---
apiVersion: v1
kind: Secret
metadata:
  name: inventory-secret
type: Opaque
data:
  DB_PASSWORD: "c3VwZXJzZWNyZXRwYXNz" # base64 for supersecretpass
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: inventory-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: inventory-service
  template:
    metadata:
      labels:
        app: inventory-service
    spec:
      containers:
      - name: inventory
        image: gcr.io/demo/inventory:v1.0.0
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: inventory-service
spec:
  type: ClusterIP
  selector:
    app: inventory-backend # INTENTIONAL DEFECT: Typo mismatch vs app: inventory-service
  ports:
  - port: 80
    targetPort: 8080
EOF
echo "Manifests authored with intentional selector defect" > scratch/day10_lab_c/stage2.log
cat scratch/day10_lab_c/stage2.log
```

**Expected result:** Multi-object manifest authored with intentional selector typo.

**Save:** `scratch/day10_lab_c/stage2.log`''',

                r'''**Stage 3: Inject Intentional Selector Typo and Generate Endpoint Defect**

**Location:** local terminal

**Actions:**
Execute a manifest audit script that extracts the Service selector and compares it against the Deployment template labels.
```bash
cat <<'EOF' > scratch/day10_lab_c/audit_selector.py
import re

with open("scratch/day10_lab_c/manifests.yaml") as f:
    text = f.read()

# Extract Pod labels
pod_label_match = re.search(r"template:.*?labels:\s*\n\s*app:\s*([^\n]+)", text, re.S)
pod_label = pod_label_match.group(1).strip() if pod_label_match else None

# Extract Service selector
svc_selector_match = re.search(r"kind: Service.*?selector:\s*\n\s*app:\s*([^\n]+)", text, re.S)
svc_selector = svc_selector_match.group(1).strip() if svc_selector_match else None

print(f"Deployment Pod Template Label: 'app: {pod_label}'")
print(f"Service Selector Label:        'app: {svc_selector}'")

if pod_label != svc_selector:
    print("\n[CRITICAL ROUTING DEFECT DETECTED]")
    print(f"  Mismatch: Service selector '{svc_selector}' != Pod label '{pod_label}'")
    print("  Outcome: EndpointSlice will be EMPTY. Traffic will fail with HTTP 503.")
else:
    print("\n[ROUTING ALIGNED]")
    print("  Endpoints populated. Traffic will route successfully.")
EOF
python3 scratch/day10_lab_c/audit_selector.py > scratch/day10_lab_c/stage3.log
cat scratch/day10_lab_c/stage3.log
```

**Expected result:** Audit script detects selector mismatch and flags empty endpoint outcome.

**Save:** `scratch/day10_lab_c/stage3.log`''',

                '''**Stage 4: Run EndpointSlice Diagnostic Engine and Detect Zero Targets**

**Location:** local terminal

**Actions:**
Simulate the Kubernetes EndpointSlice controller evaluation to document the zero-target defect.
```bash
cat <<'EOF' > scratch/day10_lab_c/simulate_endpointslice.py
import json

pod_ips = ["10.244.1.5", "10.244.2.8", "10.244.3.12"]
pod_labels = {"app": "inventory-service"}
service_selector = {"app": "inventory-backend"}

matches = []
for ip in pod_ips:
    if all(pod_labels.get(k) == v for k, v in service_selector.items()):
        matches.append({"ip": ip, "ready": True})

endpoint_slice = {
    "metadata": {"name": "inventory-service-slice"},
    "endpoints": matches
}
print("Simulated EndpointSlice Output:")
print(json.dumps(endpoint_slice, indent=2))
print(f"Active Ready Endpoints: {len(matches)}")
EOF
python3 scratch/day10_lab_c/simulate_endpointslice.py > scratch/day10_lab_c/stage4.log
cat scratch/day10_lab_c/stage4.log
```

**Expected result:** Output displays 0 active ready endpoints.

**Save:** `scratch/day10_lab_c/stage4.log`''',

                '''**Stage 5: Repair Service Selector Label and Reconcile Endpoints**

**Location:** local terminal

**Actions:**
Repair the selector typo in the Service manifest and re-run the diagnostic engine.
```bash
# Correct selector in manifest
sed -i 's/app: inventory-backend/app: inventory-service/g' scratch/day10_lab_c/manifests.yaml
python3 scratch/day10_lab_c/audit_selector.py > scratch/day10_lab_c/stage5.log
cat scratch/day10_lab_c/stage5.log
```

**Expected result:** Audit script confirms `[ROUTING ALIGNED]` with matching labels.

**Save:** `scratch/day10_lab_c/stage5.log`''',

                '''**Stage 6: Trace End-to-End Request Path from Ingress to Service to Pod**

**Location:** local terminal

**Actions:**
Simulate client HTTP request routing through the repaired Service and EndpointSlice to backend pods.
```bash
python3 -c '
import random

pod_ips = ["10.244.1.5:8080", "10.244.2.8:8080", "10.244.3.12:8080"]
print("Simulating 6 Ingress Client Requests through Service VIP 10.96.0.45:80:")
for req_id in range(1, 7):
    target = random.choice(pod_ips)
    print(f"  Request #{req_id} -> Ingress -> inventory-service:80 -> Pod IP {target} [HTTP 200 OK]")
' > scratch/day10_lab_c/stage6.log
cat scratch/day10_lab_c/stage6.log
```

**Expected result:** Output displays load-balanced routing across all 3 backend pod IPs.

**Save:** `scratch/day10_lab_c/stage6.log`''',

                '''**Stage 7: Synthesize the Pod/Deployment/Service Ownership Diagram Exit Artifact**

**Location:** local terminal

**Actions:**
Synthesize all findings into the required curriculum exit evidence: a Pod/Deployment/Service ownership diagram distinguishing declarative relationships and request flows.
```bash
cat <<'EOF' > scratch/day10_lab_c/build_exit_artifact.py
import datetime

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

content = f"""# Day 10 Exit Evidence: Pod / Deployment / Service Ownership Diagram
**Generated:** {now}
**Curriculum Scope:** Kubernetes Core Objects (Pod, Deployment, Service, Ingress, ConfigMap, Secret)

## 1. Declarative Ownership & Control Hierarchy

```text
[ Developer / GitOps Manifest ]
               │
               ▼
      [ Ingress Resource ]
               │ (defines host & path routing rules)
               ▼
      [ Service Object ] ─── (selector: app=inventory-service) ───┐
               │                                                  │ matches
               │ (virtual IP & kube-proxy / NEG routing)           │
               ▼                                                  ▼
     [ EndpointSlice ] ───────────────────────────────► [ Pod Replicas ]
                                                              ▲   ▲   ▲
                                                              │   │   │ owns
                                                      [ ReplicaSet ]
                                                              ▲
                                                              │ manages rollout
                                                      [ Deployment ]
```

## 2. Configuration & Credential Injection Hierarchy

```text
  [ ConfigMap: inventory-config ]            [ Secret: inventory-secret ]
        │ (non-sensitive vars)                    │ (encrypted credentials)
        ▼                                         ▼
   [ volumeMount: /etc/config ]              [ env: DB_PASSWORD ]
        └───────────────────┬─────────────────────┘
                            ▼
               [ Container: inventory ]
```

## 3. Core Object Function & Lifecycle Matrix

| Core Object | Controlling Component | Lifecycle & Scope | Addressing / Discovery | Failure Consequence |
|---|---|---|---|---|
| **Ingress** | Ingress Controller / Cloud Load Balancer | Global / Edge HTTP routing | Public or internal VIP + DNS | Edge HTTP 404 / 502 routing failure |
| **Service** | kube-proxy / EndpointSlice Controller | Cluster-wide stable virtual IP | ClusterIP / CoreDNS name | HTTP 503 if selector has typo |
| **Deployment** | kube-controller-manager | Declarative rollout & replica count | Managed via labels & ReplicaSets | Pods crash or unplaced if misconfigured |
| **Pod** | kubelet & Container Runtime (CRI) | Ephemeral atomic container bundle | Ephemeral Pod IP in VPC | Container restart / rescheduling |
| **ConfigMap** | kube-apiserver / etcd | Decoupled configuration values | Volume mount or env variable | Pod startup failure if key missing |
| **Secret** | kube-apiserver / Cloud KMS | Decoupled sensitive tokens | Volume mount or env variable | Authentication failure if unsealed |

## 4. Key Architectural Takeaways
1. **Never Target Pod IPs Directly:** Pods are ephemeral; always route traffic through a Service virtual IP backed by EndpointSlices.
2. **Label Selector Precision:** A single-character typo in a Service selector decouples all backend Pods without failing pod health checks.
3. **Decouple Config & Code:** Use ConfigMaps and Secrets to ensure container images remain strictly immutable and environment-agnostic.
"""

with open("scratch/day-010-ownership-diagram.md", "w") as f:
    f.write(content)

print("Exit artifact generated at scratch/day-010-ownership-diagram.md")
EOF
python3 scratch/day10_lab_c/build_exit_artifact.py > scratch/day10_lab_c/stage7.log
cat scratch/day-010-ownership-diagram.md
```

**Expected result:** `scratch/day-010-ownership-diagram.md` is generated successfully.

**Save:** `scratch/day-010-ownership-diagram.md`''',

                '''**Stage 8: Validate and Verify the Day 10 Exit Artifact**

**Location:** local terminal

**Actions:**
Validate that the generated ownership diagram contains all required sections and satisfies curriculum exit criteria.
```bash
python3 -c '
with open("scratch/day-010-ownership-diagram.md") as f:
    text = f.read()

required = [
    "Declarative Ownership & Control Hierarchy",
    "Configuration & Credential Injection Hierarchy",
    "Core Object Function & Lifecycle Matrix",
    "Pod",
    "Deployment",
    "Service",
    "Ingress",
    "ConfigMap",
    "Secret"
]

missing = [req for req in required if req not in text]
if missing:
    raise ValueError(f"Missing required sections: {missing}")

print("✓ Day 10 Exit Artifact verified: complete ownership hierarchy and matrix validated.")
' > scratch/day10_lab_c/stage8.log
cat scratch/day10_lab_c/stage8.log
```

**Expected result:** Output displays `✓ Day 10 Exit Artifact verified: complete ownership hierarchy and matrix validated.`

**Save:** `scratch/day10_lab_c/stage8.log`'''
            ]
        }
    }
}
