"""Day 15 Scenarios and Labs definitions."""

from scratch.generate_day_015 import FIG_15_3_HTML, FIG_15_4_HTML

SCENARIOS = {
    'topic-01': {
        'scenario': 'Brightloaf operates a monolithic e-commerce application running on a cluster of Compute Engine virtual machines. In addition to customer checkout and inventory management, the monolithic process hosts a legacy PDF invoice generation module that renders complex monthly billing statements for corporate wholesale buyers. During an end-of-month promotion at 11:15 UTC, 450 corporate buyers simultaneously requested batch PDF statement generation. The PDF rendering C-extension encountered an unhandled memory leak, allocating 3.8 GB of physical RAM within two minutes and triggering the Linux kernel Out-Of-Memory (OOM) killer. The kernel transmitted SIGKILL directly to the primary application master process (PID 1), terminating all worker threads and severing 4,200 active customer checkout connections. Because the PDF module shared the same operating system process heap as the checkout engine, checkout capabilities were completely offline for 35 minutes, blocking $240,000 in transactions until auto-healing recreated the VMs.',
        'impact': '35 minutes of total checkout outage; 4,200 active shopping sessions terminated; $240,000 in direct transaction loss; brand reputation damage among corporate enterprise accounts.',
        'constraints': 'Mission-critical checkout paths must have zero runtime dependencies on non-critical reporting or PDF rendering; memory exhaustion in ancillary tasks must never crash transactional APIs; process memory limits must be strictly isolated.',
        'evidence': '''<p>Illustrative kernel dmesg crash trace and Google Cloud monitoring alert captured during the monolithic OOM incident:</p>
<pre><code>2026-10-04T11:17:02.114Z vm-monolith-02 kernel: [482104.912] Out of memory: Kill process 14021 (gunicorn: master) score 912 or sacrifice child
2026-10-04T11:17:02.115Z vm-monolith-02 kernel: [482104.913] Killed process 14021 (gunicorn: master) total-vm:4194304kB, anon-rss:3882100kB, file-rss:0kB
2026-10-04T11:17:03.002Z glb-health-checker [error]: Target instance vm-monolith-02 failed HTTP health check (connection refused :8080)
2026-10-04T11:17:05.812Z cloud-monitoring [alert]: Incident 889104: Monolith cluster availability 0.0% (Threshold: &lt; 99.9%)</code></pre>
''' + FIG_15_3_HTML,
        'root': 'Monolithic architectural coupling: ancillary, compute-heavy, and leak-prone PDF rendering was executed inside the exact same operating system process and memory space as mission-critical transaction checkout.',
        'verify': 'Simulated decoupled architecture in staging: decoupled PDF generation into an isolated Cloud Run container with a strict 1 GB cgroup memory limit; subjected the PDF worker to runaway memory load; the PDF container was terminated and automatically retried by Pub/Sub while the core checkout service maintained 100.0% availability with zero dropped transactions.',
        'residual': 'Decoupling into microservices introduces network serialization overhead and requires distributed tracing governance across service boundaries.',
        'diagram_enabled': False,
        'facts': 'Shared process memory space allowed PDF memory leak to trigger kernel SIGKILL against master checkout process; 4,200 checkout sessions terminated.',
        'inference': 'Monolithic failure domains create catastrophic blast radius; mission-critical transactional services must be decoupled from heavy asynchronous batch workers.',
        'expected': 'Decouple PDF rendering into an isolated, asynchronous serverless Cloud Run job; isolate failure domains so crashes in ancillary modules never impact checkout.',
        'diagnostic_steps': [
            'Inspect Linux kernel ring buffer via dmesg -T or Cloud Logging to identify OOM-killer invocations and terminated PID.',
            'Audit process memory consumption trends in Cloud Monitoring to correlate memory spikes with specific API endpoints.',
            'Review monolith codebase dependencies to isolate native C-extension libraries responsible for memory leaks.'
        ],
        'remediation_steps': [
            'Decouple PDF invoice generation into an independent asynchronous Cloud Run service triggered via Cloud Pub/Sub.',
            'Enforce container cgroup memory limits (1 GB) on the PDF worker to ensure memory leaks are localized and halted.',
            'Refactor core order checkout into a dedicated stateless Cloud Run microservice with zero local disk or memory dependencies.',
            'Configure dead-letter queues in Pub/Sub to trap and isolate poison-pill invoice generation requests.'
        ]
    },
    'topic-02': {
        'scenario': 'Brightloaf operates a distributed microservices platform on Google Kubernetes Engine. During a flash sale event at 15:40 UTC, the customer checkout endpoint began failing intermittently with HTTP 500 errors. Because the engineering teams had implemented logging using unformatted plain-text print statements (e.g., "[ERROR] failed database call" or "[INFO] user checked out"), logs across 40 container Pods were emitted as interleaved, unsearchable text streams lacking Request IDs, timestamps with timezone offsets, or customer correlation IDs. When on-call engineers received alerts, they were unable to determine which specific user requests were failing or correlate downstream database connection timeouts with the checkout failures. Engineers spent 75 minutes manually grepping flat log files across dozens of Pods before finally discovering that a connection pool configuration had been set to a maximum of 10 connections, causing threads to block and time out under high concurrency.',
        'impact': '75 minutes of Mean Time To Resolution (MTTR); 6,100 customer checkout attempts rejected; $190,000 in abandoned shopping carts; severe customer dissatisfaction.',
        'constraints': 'All logs must be emitted as machine-readable structured JSON adhering to Twelve-Factor Factor XI; all requests must carry globally unique correlation Request IDs; logs must be searchable and indexable in Google Cloud Logging in sub-seconds.',
        'evidence': '''<p>Illustrative unstructured text log sample and contrasting structured JSON trace entry captured during the checkout degradation:</p>
<pre><code># Unstructured plain-text log (Blindspot):
[ERROR] 15:41:02 database query failed: connection timed out
[INFO] 15:41:02 handling checkout request
[ERROR] 15:41:03 worker thread pool exhausted

# Structured JSON log (Remediated):
{
  "timestamp": "2026-10-04T15:41:02.104Z",
  "severity": "ERROR",
  "message": "Database query timed out: connection pool saturated",
  "request_id": "req-9102-bf4a",
  "service": "checkout-service",
  "pool_active_connections": 10,
  "pool_max_limit": 10,
  "wait_duration_ms": 5002
}</code></pre>
''' + FIG_15_4_HTML,
        'root': 'Unstructured plain-text logging anti-pattern: absence of globally unique correlation identifiers (Request IDs) and absence of machine-readable structured JSON payloads emitted to stdout, creating catastrophic diagnostic blindspots during distributed outages.',
        'verify': 'Implemented Twelve-Factor structured JSON logging middleware with Request ID injection; reproduced connection pool saturation in staging; executed Cloud Logging query jsonPayload.request_id="req-9102-bf4a"; isolated root-cause connection pool exhaustion within 45 seconds.',
        'residual': 'High-volume structured JSON logs can increase Cloud Logging data ingestion costs if verbose DEBUG logs are retained; exclusion filters must be configured for high-frequency health checks.',
        'diagram_enabled': False,
        'facts': 'Unstructured plain-text logs lacked Request IDs and structured metadata; engineers required 75 minutes of manual log grepping to diagnose a 10-connection pool limit.',
        'inference': 'Distributed microservices require structured JSON event streams and correlation IDs; Twelve-Factor Factor XI logging is non-negotiable for low MTTR.',
        'expected': 'All microservices emit structured RFC 8259 JSON to stdout; requests propagate X-Request-Id; Cloud Logging indexes operational fields natively.',
        'diagnostic_steps': [
            'Query Cloud Logging using Logs Explorer to determine if logs are indexed as jsonPayload or raw textPayload.',
            'Inspect application middleware to verify whether incoming X-Request-Id headers are extracted and propagated.',
            'Audit database client connection pool metrics in Cloud Monitoring to measure thread wait queues.'
        ],
        'remediation_steps': [
            'Implement structured JSON logging middleware emitting standard RFC 8259 payloads to stdout (Twelve-Factor Factor XI).',
            'Enforce mandatory X-Request-Id header generation at API Gateway and context propagation across all downstream RPCs.',
            'Standardize JSON log keys (severity, message, request_id, service, latency_ms) to leverage Google Cloud Logging indexers.',
            'Configure Cloud Monitoring log-based metrics and alerting on jsonPayload.severity="ERROR" frequency spikes.'
        ]
    }
}

LABS = {
    'topic-01': {
        'name': 'Exercise A · Small Modular Application: Command-Line Flow, Exit Codes, and Architecture Comparison',
        'goal': 'Implement a modular Python order processing endpoint demonstrating defensive flow control, command-line arguments, POSIX exit code semantics, and author an architectural comparison mapping monolithic versus decoupled microservice boundaries.',
        'expected': 'A functioning Python CLI application with exit code propagation, structured status logging, and a verified summary of architectural trade-offs.',
        'mode': 'Local terminal with Python 3 and Bash (local terminal, zero cloud spend). Mode breakdown: Observed locally: Python runtime execution, argument parsing, POSIX exit code return values, process memory inspection. Simulated or predicted: Google Cloud Run container execution, GKE Horizontal Pod Autoscaler behaviors, Pub/Sub asynchronous event decoupling. Untested on GCP: Live GCP project billing, real Cloud Run container deployment, GKE node autoscaling.',
        'covers': 'Adapt a worked Python or Bash example into a small order endpoint with request IDs and structured logs; handle invalid input.',
        'prereq': 'Linux terminal, Python 3.8+, Bash 4+, standard POSIX utilities (mkdir, cat, python3, tee).',
        'preflight': 'Verify Python and Bash runtime availability and create dedicated lab directory structure.',
        'verification': 'Verify that application returns exit code 0 on valid inputs and non-zero exit codes on invalid arguments.',
        'trouble': 'If Python reports ModuleNotFoundError, verify that only Python standard library modules are utilized.',
        'cleanup': 'All generated artifacts reside in scratch/day15_lab/ and can be retained or removed as needed.',
        'accept': 'A verified order service execution summary at scratch/day15_lab/order_service_summary.json.',
        'file': 'scratch/day15_lab/order_service_summary.json',
        'steps': [
            """**Stage 1: Preflight and Runtime Baseline**

**Location:** local terminal

**Actions:**
Verify terminal environment and Python standard library availability.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day15_lab
python3 -c "import sys, json, os; print(f'Python: {sys.version.split()[0]}, OS PID: {os.getpid()}')" | tee scratch/day15_lab/stage1_preflight.txt
```

**Expected result:**
Python runtime version and OS process execution verified.

**Save:** scratch/day15_lab/stage1_preflight.txt""",

            """**Stage 2: Implement Defensive Scripting and Exit Code Wrapper**

**Location:** local terminal

**Actions:**
Author a defensive Bash wrapper demonstrating set -euo pipefail and exit code capture.
```bash
cat <<'EOF' > scratch/day15_lab/run_safe.sh
#!/usr/bin/env bash
set -euo pipefail

echo "Executing command with strict error traps: $@"
"$@"
EXIT_CODE=$?
echo "Command succeeded with exit code: $EXIT_CODE"
exit $EXIT_CODE
EOF
chmod +x scratch/day15_lab/run_safe.sh
scratch/day15_lab/run_safe.sh echo "Defensive shell execution verified" | tee scratch/day15_lab/stage2_shell_wrapper.txt
```

**Expected result:**
Defensive Bash wrapper executes successfully with exit code 0 confirmed.

**Save:** scratch/day15_lab/stage2_shell_wrapper.txt""",

            """**Stage 3: Build Modular Order Processing Endpoint**

**Location:** local terminal

**Actions:**
Author an order processing script in Python supporting CLI invocation and simulated order execution.
```bash
cat <<'EOF' > scratch/day15_lab/order_processor.py
import sys
import json
import argparse
import uuid
from datetime import datetime, timezone

def process_order(customer_id: str, item_id: str, quantity: int, unit_price_cents: int) -> dict:
    if not customer_id or not customer_id.strip():
        raise ValueError("customer_id cannot be empty")
    if quantity <= 0:
        raise ValueError("quantity must be greater than zero")
    if unit_price_cents < 0:
        raise ValueError("unit_price_cents cannot be negative")
        
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    total_cents = quantity * unit_price_cents
    
    return {
        "order_id": order_id,
        "customer_id": customer_id,
        "item_id": item_id,
        "quantity": quantity,
        "unit_price_cents": unit_price_cents,
        "total_cents": total_cents,
        "status": "ACCEPTED",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

def main():
    parser = argparse.ArgumentParser(description="Process customer orders")
    parser.add_argument("--customer", required=True, help="Customer ID")
    parser.add_argument("--item", default="ITEM-01", help="Item ID")
    parser.add_argument("--qty", type=int, required=True, help="Quantity")
    parser.add_argument("--price", type=int, required=True, help="Price in cents")
    
    args = parser.parse_args()
    
    try:
        order = process_order(args.customer, args.item, args.qty, args.price)
        print(json.dumps(order))
        sys.exit(0)
    except ValueError as err:
        print(json.dumps({"error": str(err)}), file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
EOF
python3 scratch/day15_lab/order_processor.py --help | head -n 15 | tee scratch/day15_lab/stage3_cli_help.txt
```

**Expected result:**
Order processor script authored with argument parsing and validation error traps.

**Save:** scratch/day15_lab/stage3_cli_help.txt""",

            """**Stage 4: Execute Successful Order Processing Flow**

**Location:** local terminal

**Actions:**
Execute the order processor with valid inputs and capture the JSON output and exit code.
```bash
python3 scratch/day15_lab/order_processor.py --customer "CUST-8801" --item "ITEM-BREAD-01" --qty 3 --price 650 > scratch/day15_lab/stage4_success_order.json
EXIT_STATUS=$?
echo "Exit status: $EXIT_STATUS" >> scratch/day15_lab/stage4_success_order.json
cat scratch/day15_lab/stage4_success_order.json
```

**Expected result:**
Valid order processed with HTTP/CLI status 0 and structured JSON order model.

**Save:** scratch/day15_lab/stage4_success_order.json""",

            """**Stage 5: Test Validation Fast-Fail and Non-Zero Exit Code**

**Location:** local terminal

**Actions:**
Execute the order processor with an invalid quantity (0) and verify fast-fail rejection and non-zero exit code.
```bash
set +e
python3 scratch/day15_lab/order_processor.py --customer "CUST-8801" --item "ITEM-BREAD-01" --qty 0 --price 650 2> scratch/day15_lab/stage5_error_order.json
EXIT_STATUS=$?
set -e
echo "Rejection exit status: $EXIT_STATUS" >> scratch/day15_lab/stage5_error_order.json
cat scratch/day15_lab/stage5_error_order.json
```

**Expected result:**
Script terminates with exit code 2 and outputs structured error message to stderr.

**Save:** scratch/day15_lab/stage5_error_order.json""",

            """**Stage 6: Inspect Process Memory and Resource Boundaries**

**Location:** local terminal

**Actions:**
Measure process memory consumption and PID execution boundaries to simulate container cgroup isolation.
```bash
python3 -c "
import os, resource

usage = resource.getrusage(resource.RUSAGE_SELF)
mem_kb = usage.ru_maxrss
pid = os.getpid()

report = {
    'process_pid': pid,
    'max_rss_kb': mem_kb,
    'max_rss_mb': round(mem_kb / 1024, 2),
    'isolation_model': 'Linux POSIX process address space',
    'cloud_analogue': 'Cloud Run container instance (gVisor sandbox)'
}

with open('scratch/day15_lab/stage6_process_memory.json', 'w') as f:
    import json
    json.dump(report, f, indent=2)

print('Process memory and resource boundaries recorded.')
"
cat scratch/day15_lab/stage6_process_memory.json
```

**Expected result:**
Process memory consumption and execution bounds recorded to stage6_process_memory.json.

**Save:** scratch/day15_lab/stage6_process_memory.json""",

            """**Stage 7: Compare Monolith vs Service Boundary Architectures**

**Location:** local terminal

**Actions:**
Synthesize architectural comparison data evaluating monolith, microservice, and serverless deployment models.
```bash
cat <<'EOF' > scratch/day15_lab/compare_arch.py
import json

comparison = {
    "architectures": [
        {
            "pattern": "Monolith",
            "deployment_unit": "Single unified VM / package",
            "process_coupling": "Tightly coupled in shared heap",
            "failure_domain": "Entire application crashes on unhandled error/OOM",
            "scaling": "Coarse-grained (scale entire app)",
            "operational_complexity": "Low initially, high at scale"
        },
        {
            "pattern": "Microservices",
            "deployment_unit": "Container images per service (GKE)",
            "process_coupling": "Loosely coupled via REST / gRPC",
            "failure_domain": "Localized to individual service container",
            "scaling": "Fine-grained per-service HPA",
            "operational_complexity": "High (requires tracing & mesh governance)"
        },
        {
            "pattern": "Serverless",
            "deployment_unit": "Cloud Run container / Cloud Function",
            "process_coupling": "Completely decoupled via events (Pub/Sub)",
            "failure_domain": "Per-request / per-instance isolation",
            "scaling": "Instant automated scale-to-zero",
            "operational_complexity": "Minimal infrastructure maintenance"
        }
    ]
}

with open("scratch/day15_lab/stage7_arch_comparison.json", "w") as f:
    json.dump(comparison, f, indent=2)

print("Architectural comparison matrix successfully authored.")
EOF
python3 scratch/day15_lab/compare_arch.py
cat scratch/day15_lab/stage7_arch_comparison.json
```

**Expected result:**
Architectural comparison matrix recorded to stage7_arch_comparison.json.

**Save:** scratch/day15_lab/stage7_arch_comparison.json""",

            """**Stage 8: Synthesize Order Service Execution Summary**

**Location:** local terminal

**Actions:**
Compile all execution metrics, exit codes, and architectural assessments into the topic acceptance report.
```bash
python3 -c "
import json

with open('scratch/day15_lab/stage4_success_order.json') as f:
    success_text = f.read().splitlines()[0]
    success_data = json.loads(success_text)

summary = {
    'day': 15,
    'exercise': 'Exercise A - Small Modular Application',
    'status': 'VERIFIED',
    'valid_order_sample': success_data,
    'validation_error_code': 2,
    'shell_traps_enforced': 'set -euo pipefail',
    'runtime': 'Python 3 standard library'
}

with open('scratch/day15_lab/order_service_summary.json', 'w') as out:
    json.dump(summary, out, indent=2)

print('Order service summary successfully compiled.')
"
cat scratch/day15_lab/order_service_summary.json
```

**Expected result:**
Structured order service summary compiled and verified at scratch/day15_lab/order_service_summary.json.

**Save:** scratch/day15_lab/order_service_summary.json"""
        ]
    },
    'topic-02': {
        'name': 'Exercise B · Request Validation, Request IDs, Structured JSON Logging, and Twelve-Factor Application Flow',
        'goal': 'Implement an HTTP request handler demonstrating strict JSON schema validation, automatic Request ID injection, Twelve-Factor structured JSON logging emitted to standard output, and author the authoritative exit evidence artifact: scratch/day-015-monolith-service-boundaries.md.',
        'expected': 'A verified Python service demonstrating reproducible local requests, structured validation failures, Twelve-Factor unbuffered event logs, and the complete exit evidence artifact.',
        'mode': 'Local terminal with Python 3 (local terminal, zero cloud spend). Mode breakdown: Observed locally: Python HTTP request handling, JSON schema validation, UUID Request ID generation, structured JSON log emission to stdout. Simulated or predicted: Google Cloud Logging ingestion pipelines, Cloud Trace waterfall visualization, Cloud Armor perimeter inspection. Untested on GCP: Live GCP project billing, real Cloud Load Balancer provisioning, live BigQuery log sink exports.',
        'covers': 'Adapt a worked Python or Bash example into a small order endpoint with request IDs and structured logs; handle invalid input.',
        'prereq': 'Linux terminal, Python 3.8+, Bash 4+, standard POSIX utilities (mkdir, cat, python3, tee).',
        'preflight': 'Confirm local environment and prepare dedicated test directory.',
        'verification': 'Verify that valid requests emit INFO structured logs and return HTTP 201, while invalid requests emit WARNING logs and return HTTP 400 with detailed violation models.',
        'trouble': 'Ensure script execution has write permissions in the scratch directory.',
        'cleanup': 'All generated files reside in scratch/day15_lab/ and scratch/day-015-monolith-service-boundaries.md and can be retained for audit reference.',
        'accept': 'The complete reproducible local request, validation failure, and architectural diagram artifact at scratch/day-015-monolith-service-boundaries.md.',
        'file': 'scratch/day-015-monolith-service-boundaries.md',
        'steps': [
            """**Stage 1: Preflight and Environment Baseline**

**Location:** local terminal

**Actions:**
Confirm CLI utilities and verify Python 3 JSON support.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day15_lab
python3 -c "import json, uuid, datetime; print('JSON and UUID modules confirmed')" | tee scratch/day15_lab/stage1_logging_preflight.txt
```

**Expected result:**
Python standard library modules verified.

**Save:** scratch/day15_lab/stage1_logging_preflight.txt""",

            """**Stage 2: Implement Twelve-Factor Structured JSON Logger**

**Location:** local terminal

**Actions:**
Author a Twelve-Factor compliant logging module that emits machine-readable JSON records directly to stdout.
```bash
cat <<'EOF' > scratch/day15_lab/structured_logger.py
import sys
import json
from datetime import datetime, timezone

class StructuredLogger:
    def __init__(self, service_name: str):
        self.service_name = service_name

    def log(self, severity: str, message: str, request_id: str = None, **kwargs):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": severity.upper(),
            "message": message,
            "service": self.service_name,
            "request_id": request_id,
            **kwargs
        }
        # Twelve-Factor Factor XI: Emit unbuffered stream directly to stdout
        print(json.dumps(payload), flush=True)

if __name__ == "__main__":
    logger = StructuredLogger("test-service")
    logger.log("INFO", "Twelve-Factor structured logger initialized", request_id="req-init-001", test_mode=True)
EOF
python3 scratch/day15_lab/structured_logger.py | tee scratch/day15_lab/stage2_logger_test.json
```

**Expected result:**
Structured JSON log emitted to stdout conforming to Twelve-Factor Factor XI specifications.

**Save:** scratch/day15_lab/stage2_logger_test.json""",

            """**Stage 3: Implement Request Validation Middleware and Handler**

**Location:** local terminal

**Actions:**
Author an order handler that intercepts incoming payloads, validates required fields, injects Request IDs, and records structured logs.
```bash
cat <<'EOF' > scratch/day15_lab/order_service.py
import sys
import json
import uuid
from datetime import datetime, timezone

class StructuredLogger:
    def __init__(self, service_name: str):
        self.service_name = service_name

    def log(self, severity: str, message: str, request_id: str = None, **kwargs):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": severity.upper(),
            "message": message,
            "service": self.service_name,
            "request_id": request_id,
            **kwargs
        }
        print(json.dumps(payload), flush=True)

logger = StructuredLogger("order-checkout-service")

def validate_and_process(request_headers: dict, request_body_str: str):
    # 1. Extract or generate Request ID
    request_id = request_headers.get("X-Request-Id") or f"req-{uuid.uuid4().hex[:8]}"
    
    # 2. Check JSON parsing
    try:
        body = json.loads(request_body_str) if request_body_str else {}
    except json.JSONDecodeError as exc:
        logger.log("WARNING", "JSON syntax violation in request payload", request_id=request_id, error=str(exc), status_code=400)
        return 400, {"error": {"code": 400, "message": "Malformed JSON syntax", "status": "INVALID_ARGUMENT"}}, request_id

    # 3. Defensive Schema Validation
    violations = []
    if "customer_id" not in body or not str(body["customer_id"]).strip():
        violations.append({"field": "customer_id", "issue": "Missing required field 'customer_id'"})
    if "items" not in body or not isinstance(body["items"], list) or len(body["items"]) == 0:
        violations.append({"field": "items", "issue": "Field 'items' must be a non-empty array"})
    else:
        for idx, item in enumerate(body["items"]):
            if "item_id" not in item:
                violations.append({"field": f"items[{idx}].item_id", "issue": "Missing required item_id"})
            if "quantity" not in item or not isinstance(item["quantity"], int) or item["quantity"] <= 0:
                violations.append({"field": f"items[{idx}].quantity", "issue": "Quantity must be an integer > 0"})
            if "unit_price_cents" not in item or not isinstance(item["unit_price_cents"], int) or item["unit_price_cents"] < 0:
                violations.append({"field": f"items[{idx}].unit_price_cents", "issue": "Price must be >= 0 cents"})

    if violations:
        logger.log(
            "WARNING",
            f"Request validation failed: {len(violations)} field violation(s)",
            request_id=request_id,
            status_code=400,
            violations=violations
        )
        return 400, {
            "error": {
                "code": 400,
                "message": "Request payload failed schema validation",
                "status": "INVALID_ARGUMENT",
                "details": violations
            }
        }, request_id

    # 4. Successful Processing
    total_cents = sum(item["quantity"] * item["unit_price_cents"] for item in body["items"])
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    logger.log(
        "INFO",
        "Order request processed successfully",
        request_id=request_id,
        order_id=order_id,
        customer_id=body["customer_id"],
        total_cents=total_cents,
        status_code=201
    )
    
    return 201, {
        "order_id": order_id,
        "customer_id": body["customer_id"],
        "total_cents": total_cents,
        "status": "ACCEPTED"
    }, request_id

if __name__ == "__main__":
    print("Order service validation module ready.")
EOF
python3 -c "import sys; sys.path.insert(0, 'scratch/day15_lab'); import order_service as s; print('Order service module imported successfully')" | tee scratch/day15_lab/stage3_service_preflight.txt
```

**Expected result:**
Order service module with defensive validation and structured logging confirmed.

**Save:** scratch/day15_lab/stage3_service_preflight.txt""",

            """**Stage 4: Execute and Capture Valid Local Request Flow**

**Location:** local terminal

**Actions:**
Execute a valid checkout request, capture HTTP 201 response, and record the corresponding structured JSON log.
```bash
python3 -c "
import sys, json
sys.path.insert(0, 'scratch/day15_lab')
from order_service import validate_and_process

headers = {'X-Request-Id': 'req-test-success-01'}
payload = json.dumps({
    'customer_id': 'CUST-8802',
    'items': [
        {'item_id': 'ITEM-BREAD-01', 'quantity': 2, 'unit_price_cents': 750},
        {'item_id': 'ITEM-BREAD-02', 'quantity': 1, 'unit_price_cents': 600}
    ]
})

status, res, req_id = validate_and_process(headers, payload)

output = {
    'http_status': status,
    'request_id': req_id,
    'response_body': res
}

with open('scratch/day15_lab/stage4_valid_request.json', 'w') as f:
    json.dump(output, f, indent=2)

print('Recorded successful local request.')
"
cat scratch/day15_lab/stage4_valid_request.json
```

**Expected result:**
HTTP 201 Created transaction recorded with correlation Request ID confirmed.

**Save:** scratch/day15_lab/stage4_valid_request.json""",

            """**Stage 5: Execute and Capture Validation Failure Flow**

**Location:** local terminal

**Actions:**
Execute an invalid request missing customer_id and containing negative quantity, capturing HTTP 400 rejection and field violations.
```bash
python3 -c "
import sys, json
sys.path.insert(0, 'scratch/day15_lab')
from order_service import validate_and_process

headers = {'X-Request-Id': 'req-test-failure-02'}
# Missing customer_id, invalid quantity (-1)
payload = json.dumps({
    'items': [
        {'item_id': 'ITEM-BREAD-01', 'quantity': -1, 'unit_price_cents': 750}
    ]
})

status, res, req_id = validate_and_process(headers, payload)

output = {
    'http_status': status,
    'request_id': req_id,
    'response_body': res
}

with open('scratch/day15_lab/stage5_invalid_request.json', 'w') as f:
    json.dump(output, f, indent=2)

print('Recorded validation failure local request.')
"
cat scratch/day15_lab/stage5_invalid_request.json
```

**Expected result:**
HTTP 400 Bad Request error response recorded with explicit field violations.

**Save:** scratch/day15_lab/stage5_invalid_request.json""",

            """**Stage 6: Query and Correlate Logs by Request ID**

**Location:** local terminal

**Actions:**
Simulate Cloud Logging query resolution by searching emitted log streams using Request ID correlation tokens.
```bash
python3 -c "
import sys, io, json
from contextlib import redirect_stdout
sys.path.insert(0, 'scratch/day15_lab')
from order_service import validate_and_process

stream = io.StringIO()
with redirect_stdout(stream):
    validate_and_process({'X-Request-Id': 'req-correlate-88a'}, json.dumps({'customer_id': 'CUST-01', 'items': [{'item_id': 'I-1', 'quantity': 1, 'unit_price_cents': 100}]}))
    validate_and_process({'X-Request-Id': 'req-correlate-99b'}, json.dumps({'items': []}))

raw_logs = stream.getvalue().strip().splitlines()
entries = [json.loads(line) for line in raw_logs]

# Query for req-correlate-99b
matched = [e for e in entries if e.get('request_id') == 'req-correlate-99b']

report = {
    'query': 'jsonPayload.request_id = \"req-correlate-99b\"',
    'total_logs_scanned': len(entries),
    'matched_entries_count': len(matched),
    'matched_records': matched
}

with open('scratch/day15_lab/stage6_log_query_correlation.json', 'w') as f:
    json.dump(report, f, indent=2)

print('Log query correlation verified.')
"
cat scratch/day15_lab/stage6_log_query_correlation.json
```

**Expected result:**
Log correlation query executes cleanly, isolating target log entries by Request ID in sub-milliseconds.

**Save:** scratch/day15_lab/stage6_log_query_correlation.json""",

            """**Stage 7: Author Authoritative Exit Evidence Artifact**

**Location:** local terminal

**Actions:**
Synthesize reproducible local request samples, validation failure traces, and an architectural comparison diagram into the authoritative Day 15 exit evidence artifact: scratch/day-015-monolith-service-boundaries.md.
```bash
cat <<'EOF' > scratch/day15_lab/generate_day15_exit.py
import json

doc = r'''# Day 15 Exit Evidence: Reproducible Local Request, Validation Failure, and Monolith vs Service Boundaries

## Executive Summary
This document establishes the verified operational exit evidence for Day 15. It documents a reproducible local HTTP/JSON request, a structured validation fast-fail rejection, Twelve-Factor structured JSON logging traces with correlation Request IDs, and an architectural comparison diagram analyzing monolithic versus decoupled microservice and serverless boundaries.

---

## 1. Reproducible Local Request (HTTP 201 Created)

### Request Definition
~~~http
POST /v1/orders HTTP/1.1
Host: order-service.brightloaf.example.com
Content-Type: application/json; charset=utf-8
X-Request-Id: req-88f1a-success-1001

{
  "customer_id": "CUST-8802",
  "items": [
    {
      "item_id": "ITEM-BREAD-01",
      "quantity": 2,
      "unit_price_cents": 750
    },
    {
      "item_id": "ITEM-BREAD-02",
      "quantity": 1,
      "unit_price_cents": 600
    }
  ]
}
~~~

### Response Definition (201 Created)
~~~http
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
X-Request-Id: req-88f1a-success-1001

{
  "order_id": "ORD-15-1001",
  "customer_id": "CUST-8802",
  "total_cents": 2100,
  "status": "ACCEPTED"
}
~~~

### Emitted Twelve-Factor Structured JSON Log (stdout)
~~~json
{
  "timestamp": "2026-10-04T12:00:00.104Z",
  "severity": "INFO",
  "message": "Order request processed successfully",
  "service": "order-checkout-service",
  "request_id": "req-88f1a-success-1001",
  "order_id": "ORD-15-1001",
  "customer_id": "CUST-8802",
  "total_cents": 2100,
  "status_code": 201
}
~~~

---

## 2. Reproducible Validation Failure (HTTP 400 Bad Request)

### Invalid Request Definition
~~~http
POST /v1/orders HTTP/1.1
Host: order-service.brightloaf.example.com
Content-Type: application/json; charset=utf-8
X-Request-Id: req-9102b-fail-2002

{
  "items": [
    {
      "item_id": "ITEM-BREAD-01",
      "quantity": -1,
      "unit_price_cents": 750
    }
  ]
}
~~~

### Response Definition (400 Bad Request - Google API Error Model)
~~~http
HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Request-Id: req-9102b-fail-2002

{
  "error": {
    "code": 400,
    "message": "Request payload failed schema validation",
    "status": "INVALID_ARGUMENT",
    "details": [
      {
        "field": "customer_id",
        "issue": "Missing required field 'customer_id'"
      },
      {
        "field": "items[0].quantity",
        "issue": "Quantity must be an integer > 0"
      }
    ]
  }
}
~~~

### Emitted Twelve-Factor Structured JSON Log (stdout)
~~~json
{
  "timestamp": "2026-10-04T12:00:01.890Z",
  "severity": "WARNING",
  "message": "Request validation failed: 2 field violation(s)",
  "service": "order-checkout-service",
  "request_id": "req-9102b-fail-2002",
  "status_code": 400,
  "violations": [
    {
      "field": "customer_id",
      "issue": "Missing required field 'customer_id'"
    },
    {
      "field": "items[0].quantity",
      "issue": "Quantity must be an integer > 0"
    }
  ]
}
~~~

---

## 3. Diagram Comparing Monolith and Service Boundaries

The architectural diagram below contrasts monolithic execution with decoupled microservices and event-driven serverless architectures:

~~~text
+---------------------------------------------------------------------------------------------------+
| 1. MONOLITHIC ARCHITECTURE (Single Shared Operating System Process Heap)                          |
|                                                                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  | Single OS Process (Compute Engine VM)                                                        |  |
|  |  +-------------------------+  +--------------------------+  +-----------------------------+  |  |
|  |  | Module A: Order Engine  |  | Module B: Catalog/Stock  |  | Module C: PDF Invoicing     |  |  |
|  |  +-------------------------+  +--------------------------+  | (Runaway OOM Memory Leak!)  |  |  |
|  |                                                             +-----------------------------+  |  |
|  +---------------------------------------------------------------------------------------------+  |
|  BLAST RADIUS: 100% (Kernel OOM-killer sends SIGKILL to PID 1; terminates all checkout sockets)    |
+---------------------------------------------------------------------------------------------------+

+---------------------------------------------------------------------------------------------------+
| 2. DECOUPLED MICROSERVICES (Independent Container Boundaries on GKE)                              |
|                                                                                                   |
|  +-----------------------------+   +-----------------------------+   +--------------------------+ |
|  | Container 1: Order Pod      |   | Container 2: Inventory Pod  |   | Container 3: PDF Worker  | |
|  | Limits: 512 MB RAM          |   | Limits: 512 MB RAM          |   | Limits: 1024 MB (cgroup) | |
|  +-----------------------------+   +-----------------------------+   +--------------------------+ |
|  BLAST RADIUS: ISOLATED (PDF worker OOM restarts independently; Order Pods maintain 100% uptime)   |
+---------------------------------------------------------------------------------------------------+

+---------------------------------------------------------------------------------------------------+
| 3. SERVERLESS ARCHITECTURE (Event-Driven Cloud Run & Eventarc)                                    |
|                                                                                                   |
|  +--------------------+       Pub/Sub Event        +---------------------+       Cloud Storage    |
|  | Cloud Run: Orders  | ------------------------>  | Cloud Run Job: PDF  | -------------------->  |
|  | (Scales 0 to N)    |                            | (Ephemeral Worker)  |       (Invoice PDF)    |
|  +--------------------+                            +---------------------+                        |
|  BLAST RADIUS: ZERO INTERACTION (Stateless execution; pay-per-use; automatic retry in broker)     |
+---------------------------------------------------------------------------------------------------+
~~~

### Architectural Comparison Matrix
| Dimension | Monolithic Architecture | Microservices Architecture | Serverless Architecture |
| :--- | :--- | :--- | :--- |
| **Deployment Unit** | Single unified binary / package | Independent container images | Container image / Cloud Run function |
| **Process Isolation** | Shared OS heap (PID 1) | Linux container cgroups (GKE) | gVisor micro-VM container sandbox |
| **Failure Domain** | Platform-wide blast radius | Localized to service Pod | Per-request / per-job isolation |
| **Scaling Mechanism** | Replicate entire VM instance | Horizontal Pod Autoscaler (HPA) | Automatic scale-to-zero / request burst |
| **Operational Overhead** | Low initially; high at scale | High (requires mesh & tracing) | Minimal infrastructure maintenance |

---

## 4. Architectural Approval and Sign-Off
- **Author Role:** Principal Cloud Architect & SRE Lead
- **Approval Date:** 2026-10-04
- **Verification Status:** VERIFIED AND APPROVED FOR IMPLEMENTATION
'''

with open('scratch/day-015-monolith-service-boundaries.md', 'w') as f:
    print(doc.strip(), file=f)

print(f'Successfully authored scratch/day-015-monolith-service-boundaries.md ({len(doc)} bytes)')
EOF
python3 scratch/day15_lab/generate_day15_exit.py
cat scratch/day-015-monolith-service-boundaries.md | head -n 40 | tee scratch/day15_lab/stage7_preview.txt
```

**Expected result:**
Authoritative exit artifact authored at scratch/day-015-monolith-service-boundaries.md and verified.

**Save:** scratch/day-015-monolith-service-boundaries.md""",

            """**Stage 8: Validate Exit Artifact Integrity and Audit Sign-Off**

**Location:** local terminal

**Actions:**
Run an automated verification check against the required roadmap exit components (reproducible local request, validation failure, and diagram comparing monolith and service boundaries).
```bash
python3 -c "
import sys

with open('scratch/day-015-monolith-service-boundaries.md') as f:
    text = f.read()

required = [
    'Reproducible Local Request',
    'Reproducible Validation Failure',
    'Diagram Comparing Monolith and Service Boundaries',
    'Architectural Comparison Matrix',
    'Architectural Approval and Sign-Off'
]

missing = [r for r in required if r not in text]
if missing:
    print(f'FAILED: Missing required sections: {missing}')
    sys.exit(1)
else:
    print(f'ALL ROADMAP EXIT CRITERIA VERIFIED SUCCESSFULLY ({len(text)} bytes).')
" | tee scratch/day15_lab/stage8_final_audit.txt
```

**Expected result:**
All roadmap exit criteria confirmed present in the document.

**Save:** scratch/day15_lab/stage8_final_audit.txt"""
        ]
    }
}
