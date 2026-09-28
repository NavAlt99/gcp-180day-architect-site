part4 = '''    <section class="part" id="part-4" aria-labelledby="part-4-title">
      <h2 id="part-4-title">4 · Step-by-step labs for each topic</h2>

      <article class="topic-card lab" id="topic-01-lab">
        <h3>Lab 20.1 · API enablement inspection, client library simulation, and asynchronous LRO polling engine</h3>
        
        <p><strong>Goal:</strong> Inspect API enablement via Service Usage, simulate an asynchronous Cloud SQL provisioning operation returning an LRO handle, and author a robust Python exponential backoff polling script with randomized jitter to prevent premature execution.</p>
        <p><strong>Expected result:</strong> A verified local LRO mock server, an automated polling client implementing exponential backoff with jitter, and verified positive and negative test traces.</p>
        <p><strong>Mode:</strong> Local Python and bash exercise · <strong>Prerequisite:</strong> Python 3 runtime and standard libraries.</p>

        <h4>Preflight check</h4>
        <p>Verify Python 3 availability and create a clean working directory:</p>
        <pre><code class="language-bash">python3 --version
mkdir -p "$HOME/lro-polling-lab"
cd "$HOME/lro-polling-lab"</code></pre>

        <h4>Exact execution sequence</h4>
        <ol>
          <li>
            <p><strong>Inspect service enablement concepts:</strong> Verify the command structure used to list and enable Google Cloud services via the <code>serviceusage</code> API:</p>
            <pre><code class="language-bash"># Audit active gcloud service listing command (demonstration syntax)
echo "Command to inspect enabled services: gcloud services list --enabled"
echo "Command to enable SQL Admin API:     gcloud services enable sqladmin.googleapis.com"</code></pre>
          </li>
          <li>
            <p><strong>Author mock LRO API server:</strong> Create a Python HTTP server that simulates an asynchronous Cloud SQL instance creation endpoint returning an operation handle:</p>
            <pre><code class="language-bash">cat << 'EOF' > "$HOME/lro-polling-lab/mock_lro_server.py"
import http.server, socketserver, json, time, sys

polls_count = 0
inject_error = False

if len(sys.argv) > 1 and sys.argv[1] == "--inject-error":
    inject_error = True

class LROHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global polls_count
        polls_count += 1
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        # Complete operation after 4 polling requests
        if polls_count < 4:
            response = {
                "name": "operations/sql-instance-op-40291",
                "done": False,
                "metadata": {"type": "CREATE_INSTANCE", "state": "PENDING_CREATE"}
            }
        else:
            if inject_error:
                response = {
                    "name": "operations/sql-instance-op-40291",
                    "done": True,
                    "error": {
                        "code": 409,
                        "message": "RESOURCE_ALREADY_EXISTS: Instance brightloaf-orders-db already exists."
                    }
                }
            else:
                response = {
                    "name": "operations/sql-instance-op-40291",
                    "done": True,
                    "response": {
                        "instance": "brightloaf-orders-db",
                        "state": "RUNNABLE",
                        "ip": "10.0.1.5"
                    }
                }
        self.wfile.write(json.dumps(response).encode())

with socketserver.TCPServer(("127.0.0.1", 8089), LROHandler) as httpd:
    httpd.handle_request()
    httpd.handle_request()
    httpd.handle_request()
    httpd.handle_request()
EOF</code></pre>
          </li>
          <li>
            <p><strong>Author exponential backoff LRO polling engine:</strong> Author <code>poll_lro.py</code> incorporating exponential backoff, randomized jitter, and error verification:</p>
            <pre><code class="language-bash">cat << 'EOF' > "$HOME/lro-polling-lab/poll_lro.py"
#!/usr/bin/env python3
import urllib.request, json, time, random, sys

def poll_operation(endpoint_url, initial_delay=0.5, multiplier=1.5, jitter_ratio=0.2, max_delay=5.0, max_attempts=10):
    delay = initial_delay
    for attempt in range(1, max_attempts + 1):
        try:
            req = urllib.request.Request(endpoint_url)
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e:
            print(f"[POLL ERROR] Request failed on attempt {attempt}: {e}")
            sys.exit(1)

        is_done = data.get("done", False)
        print(f"[POLL #{attempt}] Operation: {data.get('name')} | done: {is_done}")

        if is_done:
            if "error" in data:
                err = data["error"]
                print(f"[LRO FAILED] Error {err.get('code')}: {err.get('message')}", file=sys.stderr)
                return False, data
            print(f"[LRO SUCCESS] Operation completed successfully! Details: {data.get('response')}")
            return True, data

        # Calculate backoff delay with jitter
        jitter = delay * jitter_ratio * (random.random() * 2 - 1)
        sleep_time = min(delay + jitter, max_delay)
        print(f"[BACKOFF] Sleeping {sleep_time:.2f}s before next poll...")
        time.sleep(sleep_time)
        delay = min(delay * multiplier, max_delay)

    print("[TIMEOUT] Maximum polling attempts exceeded.", file=sys.stderr)
    return False, None

if __name__ == "__main__":
    url = "http://127.0.0.1:8089/operations/sql-instance-op-40291"
    success, result = poll_operation(url)
    if not success:
        sys.exit(1)
    print("[PIPELINE PASS] Instance is fully initialized. Safe to run migrations.")
EOF
chmod +x "$HOME/lro-polling-lab/poll_lro.py"</code></pre>
          </li>
          <li>
            <p><strong>Execute positive test run:</strong> Launch the mock server and execute the polling client, verifying successful completion:</p>
            <pre><code class="language-bash"># Start mock server in background
python3 "$HOME/lro-polling-lab/mock_lro_server.py" &
SERVER_PID=$!
sleep 1

# Execute polling engine
python3 "$HOME/lro-polling-lab/poll_lro.py"

# Cleanup server
kill $SERVER_PID 2>/dev/null || true</code></pre>
          </li>
          <li>
            <p><strong>Execute negative test run:</strong> Launch mock server with an injected error, verifying that the polling engine intercepts the failure:</p>
            <pre><code class="language-bash"># Start mock server with error injection
python3 "$HOME/lro-polling-lab/mock_lro_server.py" --inject-error &
SERVER_PID=$!
sleep 1

# Assert that polling engine detects error and exits non-zero
! python3 "$HOME/lro-polling-lab/poll_lro.py"

# Cleanup server
kill $SERVER_PID 2>/dev/null || true</code></pre>
          </li>
        </ol>

        <h4>Verification and acceptance</h4>
        <p>Confirm that the positive test logs display successful status progression and operation completion:</p>
        <pre><code class="language-bash">[POLL #1] Operation: operations/sql-instance-op-40291 | done: False
[BACKOFF] Sleeping 0.52s before next poll...
[POLL #2] Operation: operations/sql-instance-op-40291 | done: False
[BACKOFF] Sleeping 0.74s before next poll...
[POLL #3] Operation: operations/sql-instance-op-40291 | done: False
[BACKOFF] Sleeping 1.15s before next poll...
[POLL #4] Operation: operations/sql-instance-op-40291 | done: True
[LRO SUCCESS] Operation completed successfully! Details: {'instance': 'brightloaf-orders-db', 'state': 'RUNNABLE', 'ip': '10.0.1.5'}
[PIPELINE PASS] Instance is fully initialized. Safe to run migrations.</code></pre>

        <div class="callout caution">
          <strong>Troubleshooting</strong>
          <p>If port 8089 is unavailable, modify the port number in both <code>mock_lro_server.py</code> and <code>poll_lro.py</code> to another available local port such as 8099.</p>
        </div>

        <div class="callout">
          <strong>Cleanup and cost</strong>
          <p>Remove the working directory using <code>rm -rf "$HOME/lro-polling-lab"</code>. Zero cloud charges incurred.</p>
        </div>

        <label class="check"><input type="checkbox" data-progress="lab-20-topic-01"> I completed and verified the asynchronous LRO polling engine exercise</label>
      </article>

      <article class="topic-card lab" id="topic-02-lab">
        <h3>Lab 20.2 · Pub/Sub emulator setup, endpoint redirection, and four-service limitation matrix auditing</h3>
        
        <p><strong>Goal:</strong> Launch a local Pub/Sub emulator listener, configure client library environment redirection via <code>PUBSUB_EMULATOR_HOST</code>, publish and pull messages, verify consumer idempotency against simulated at-least-once message replay, and generate the required four-service limitations matrix artifact.</p>
        <p><strong>Expected result:</strong> A verified local Pub/Sub emulator test run, consumer idempotency proof preserving single fulfillment, and the generated markdown matrix artifact (<code>day-020-four-service-matrix.md</code>).</p>
        <p><strong>Mode:</strong> Local Python and bash simulation · <strong>Prerequisite:</strong> Python 3 runtime.</p>

        <h4>Preflight check</h4>
        <p>Verify Python 3 availability and create a temporary working directory:</p>
        <pre><code class="language-bash">python3 --version
mkdir -p "$HOME/emulator-lab"
cd "$HOME/emulator-lab"</code></pre>

        <h4>Exact execution sequence</h4>
        <ol>
          <li>
            <p><strong>Author lightweight Pub/Sub emulator mock:</strong> Create an in-memory Pub/Sub service listening on port 8085 supporting topic creation, publishing, and subscription pulling:</p>
            <pre><code class="language-bash">cat << 'EOF' > "$HOME/emulator-lab/pubsub_emulator.py"
import http.server, socketserver, json, sys

topics = set()
messages = []

class PubSubHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode() if content_length > 0 else "{}"
        data = json.loads(body)

        if "/topics/" in self.path and not self.path.endswith(":publish"):
            topic_name = self.path.split("/topics/")[-1]
            topics.add(topic_name)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"name": topic_name}).encode())

        elif self.path.endswith(":publish"):
            for msg in data.get("messages", []):
                messages.append(msg)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"messageIds": ["msg-101", "msg-102"]}).encode())

        elif self.path.endswith(":pull"):
            self.send_response(200)
            self.end_headers()
            received = []
            for idx, msg in enumerate(messages):
                received.append({"ackId": f"ack-{idx}", "message": msg})
            self.wfile.write(json.dumps({"receivedMessages": received}).encode())
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(("127.0.0.1", 8085), PubSubHandler) as httpd:
    httpd.serve_forever()
EOF</code></pre>
          </li>
          <li>
            <p><strong>Start emulator and configure environment redirection:</strong> Launch the emulator daemon in the background and configure the official client redirection variable:</p>
            <pre><code class="language-bash"># Start local emulator daemon
python3 "$HOME/emulator-lab/pubsub_emulator.py" &
EMULATOR_PID=$!
sleep 1

# Export client library endpoint redirection
export PUBSUB_EMULATOR_HOST=127.0.0.1:8085
echo "PASS: PUBSUB_EMULATOR_HOST set to $PUBSUB_EMULATOR_HOST"</code></pre>
          </li>
          <li>
            <p><strong>Author consumer idempotency test script:</strong> Author a test script simulating order event publication, consumer processing, and message replay deduplication:</p>
            <pre><code class="language-bash">cat << 'EOF' > "$HOME/emulator-lab/test_pubsub_idempotency.py"
#!/usr/bin/env python3
import urllib.request, json, os, sys

emulator_host = os.environ.get("PUBSUB_EMULATOR_HOST", "127.0.0.1:8085")
base_url = f"http://{emulator_host}"

# 1. Create topic
req = urllib.request.Request(f"{base_url}/v1/projects/brightloaf-test/topics/orders", data=b"{}", headers={'Content-Type': 'application/json'})
urllib.request.urlopen(req)

# 2. Publish order event
order_payload = {"data": "eydvcmRlcl9pZCc6ICdPUkQtOTkyODEnLCAnYmFrZXJ5JzogJ0Jha2VyeS0wNCd9"}
req = urllib.request.Request(
    f"{base_url}/v1/projects/brightloaf-test/topics/orders:publish",
    data=json.dumps({"messages": [order_payload]}).encode(),
    headers={'Content-Type': 'application/json'}
)
urllib.request.urlopen(req)

# 3. Simulate consumer with atomic deduplication
fulfilled_orders = set()
fulfillment_dispatches = 0

def process_order_message(order_id):
    global fulfillment_dispatches
    print(f"[CONSUMER] Received order event: {order_id}")
    # Idempotency Guard (simulating DB UNIQUE constraint)
    if order_id in fulfilled_orders:
        print(f"[IDEMPOTENCY] Order {order_id} already fulfilled! Suppressing physical dispatch.")
        return False
    fulfilled_orders.add(order_id)
    fulfillment_dispatches += 1
    print(f"[DISPATCH] Issued physical baking ticket #TK-{fulfillment_dispatches} for {order_id}")
    return True

# Simulate at-least-once message delivery: 1 initial delivery + 2 replays
order_id = "ORD-99281"
print("[TEST] Delivering message 1 (Initial)...")
process_order_message(order_id)

print("[TEST] Delivering message 2 (At-least-once network replay)...")
process_order_message(order_id)

print("[TEST] Delivering message 3 (Consumer crash timeout replay)...")
process_order_message(order_id)

print(f"[AUDIT] Total Deliveries: 3 | Physical Fulfillments: {fulfillment_dispatches}")
assert fulfillment_dispatches == 1, "Invariant breach: duplicate fulfillment occurred!"
print("[PASS] Duplicate fulfillment invariant preserved: fulfillment_count == 1")
EOF
chmod +x "$HOME/emulator-lab/test_pubsub_idempotency.py"</code></pre>
          </li>
          <li>
            <p><strong>Execute consumer idempotency simulation:</strong> Run the simulation and verify that duplicate order deliveries are caught and discarded:</p>
            <pre><code class="language-bash">python3 "$HOME/emulator-lab/test_pubsub_idempotency.py"</code></pre>
          </li>
          <li>
            <p><strong>Generate the four-service limitations matrix artifact:</strong> Create the required daily evidence artifact detailing emulator divergence points:</p>
            <pre><code class="language-bash">cat << 'EOF' > "$HOME/emulator-lab/day-020-four-service-matrix.md"
# Day 20 · Four-Service Emulator Limitations & Architectural Divergence Matrix

## 1. Cloud Pub/Sub Emulator
* **Endpoint / Protocol:** Port 8085 (gRPC / REST).
* **Storage Model:** In-memory volatile Java heap.
* **Documented Divergences:**
  1. Does not simulate multi-zone partition loss or distributed consensus delays.
  2. Acknowledgment timeouts are masked by sub-millisecond local loopback latency.
  3. Push endpoints require local reverse proxying.
* **Architectural Risk:** Assuming single-delivery semantics without consumer idempotency keys causes duplicate fulfillments in production.

## 2. Cloud Firestore Emulator
* **Endpoint / Protocol:** Port 8080 (REST / gRPC).
* **Storage Model:** Ephemeral memory (supports `--export-on-exit` and `--import-data`).
* **Documented Divergences:**
  1. Composite index enforcement is relaxed; queries execute locally without requiring composite index definitions.
  2. Does not simulate multi-region Paxos quorum latency.
* **Architectural Risk:** Deploying unindexed complex queries causes production API rejections.

## 3. Cloud Spanner Emulator
* **Endpoint / Protocol:** Port 9010 (gRPC) / 9020 (REST).
* **Storage Model:** Single-process C++ application backed by SQLite.
* **Documented Divergences:**
  1. **Lacks TrueTime support**: Uses local system clock without commit wait ($2\epsilon$) uncertainty intervals.
  2. Does not simulate distributed Paxos consensus or split-brain leader elections.
  3. Query execution plans and latencies are non-representative of distributed Spanner clusters.
* **Architectural Risk:** Assuming local SQLite latency and concurrency reflect production multi-node transactional scaling.

## 4. Cloud Bigtable Emulator
* **Endpoint / Protocol:** Port 8086 (gRPC).
* **Storage Model:** In-memory Go hash structures.
* **Documented Divergences:**
  1. Does not simulate tablet splitting, LSM compaction cycles, or SSD performance limits.
  2. Key range hotspotting cannot be detected.
  3. Security and IAM authorization checks are entirely bypassed.
* **Architectural Risk:** Deploying sequential row key designs that create catastrophic hotspotting under production workloads.
EOF

# Display generated matrix
cat "$HOME/emulator-lab/day-020-four-service-matrix.md"</code></pre>
          </li>
        </ol>

        <h4>Verification and acceptance</h4>
        <p>Confirm that the simulation completes with verified single fulfillment and that the matrix artifact is created:</p>
        <pre><code class="language-bash">[TEST] Delivering message 1 (Initial)...
[CONSUMER] Received order event: ORD-99281
[DISPATCH] Issued physical baking ticket #TK-1 for ORD-99281
[TEST] Delivering message 2 (At-least-once network replay)...
[CONSUMER] Received order event: ORD-99281
[IDEMPOTENCY] Order ORD-99281 already fulfilled! Suppressing physical dispatch.
[TEST] Delivering message 3 (Consumer crash timeout replay)...
[CONSUMER] Received order event: ORD-99281
[IDEMPOTENCY] Order ORD-99281 already fulfilled! Suppressing physical dispatch.
[AUDIT] Total Deliveries: 3 | Physical Fulfillments: 1
[PASS] Duplicate fulfillment invariant preserved: fulfillment_count == 1</code></pre>

        <div class="callout caution">
          <strong>Troubleshooting</strong>
          <p>If the emulator process does not start, verify that port 8085 is not already in use by querying open sockets with the <code>netstat -tlpn</code> command or checking background processes.</p>
        </div>

        <div class="callout">
          <strong>Cleanup and cost</strong>
          <p>Kill the background emulator process with <code>kill $EMULATOR_PID 2>/dev/null || true</code>. Unset <code>PUBSUB_EMULATOR_HOST</code>. Remove the temporary directory with <code>rm -rf "$HOME/emulator-lab"</code>. Zero cloud charges incurred.</p>
        </div>

        <label class="check"><input type="checkbox" data-progress="lab-20-topic-02"> I completed and verified the Pub/Sub emulator and four-service matrix exercise</label>
      </article>
    </section>
'''

with open('scratch/day020/part4.html', 'w') as f:
    f.write(part4)

print('Part 4 written, length:', len(part4))
