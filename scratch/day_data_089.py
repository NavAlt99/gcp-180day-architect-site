"""day_data_089.py — Exhaustive architecture data specification for Day 89.

Covers Messaging, DNS, and Application Health.
"""

DAY_NUM = 89

DATA = {'day': 89,
 'part1_intro': 'Day 89 analyzes the dynamic control plane and communication fabric connecting distributed '
                'microservices: asynchronous messaging, global name resolution, and workload health verification. Even '
                'the most robust regional infrastructure fails if asynchronous message pipelines drop events during '
                'regional partitions, if DNS caching traps client traffic at a failed datacenter, or if misconfigured '
                "health probes trigger cascading restarts across healthy compute nodes. Today's curriculum constructs "
                'defensible architectures for Google Cloud Pub/Sub (enforcing regional storage governance, dead-letter '
                'queuing, and exactly-once processing pipelines), evaluates Cloud DNS routing policies (geolocation, '
                'weighted, and health-checked failover) against recursive resolver TTL caching realities, and details '
                'application-tier resiliency mechanisms (shallow versus deep probes, readiness versus liveness '
                'isolation, and SIGTERM connection draining).',
 'exit_summary': 'Engineered an enterprise messaging and routing resiliency architecture: established Pub/Sub message '
                 'storage constraints with automated dead-letter topic dead-lettering and client idempotency controls; '
                 'designed Cloud DNS health-checked failover policies accounting for resolver TTL lag; authored an '
                 'authoritative shallow-versus-deep health probe design document and verified Kubernetes/Cloud Run '
                 'graceful termination lifecycles.',
 'part2_intro': 'Distributed application survivability depends upon predictable decoupled interfaces and rapid, safe '
                'failure isolation. The architectural patterns below dissect Pub/Sub message retention mechanics, '
                'Cloud DNS Anycast routing behaviors, and probe design principles required to prevent self-inflicted '
                'systemic brownouts.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Layer</th>\n'
                    '      <th>Primary GCP Mechanism</th>\n'
                    '      <th>Resilience Guarantee &amp; Scope</th>\n'
                    '      <th>Key Failure Mode / Risk</th>\n'
                    '      <th>Architectural Mitigation</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>Messaging</strong></td>\n'
                    '      <td>Cloud Pub/Sub (Regional Endpoints + DLQ)</td>\n'
                    '      <td>At-least-once delivery, horizontal scale, regional persistence boundary</td>\n'
                    '      <td>Poison message crash loop; cross-border data residency violation</td>\n'
                    '      <td>Enforce <code>allowedPersistenceRegions</code>; configure Dead-Letter Topics (5 retries '
                    'max) + exponential backoff</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Resolution</strong></td>\n'
                    '      <td>Cloud DNS (Anycast Authoritative DNS)</td>\n'
                    '      <td>100% availability SLA; Geolocation, Weighted, and Failover routing</td>\n'
                    '      <td>Recursive resolver TTL caching ignores DNS failover during outages</td>\n'
                    '      <td>Configure 30s-60s TTL; integrate Cloud Monitoring health checks; deploy multi-region '
                    'Anycast VIPs</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Liveness Probe</strong></td>\n'
                    '      <td>Kubernetes / Compute Engine Liveness HTTP Probe</td>\n'
                    '      <td>Restarts deadlocked or crashed container runtimes automatically</td>\n'
                    '      <td>Cascading restart loop if probe depends on overloaded external DB</td>\n'
                    '      <td>Keep liveness probes shallow (local memory/event-loop check only, zero external network '
                    'calls)</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Readiness Probe</strong></td>\n'
                    '      <td>Kubernetes Readiness / Cloud Load Balancing Health Check</td>\n'
                    '      <td>Removes degraded instances from service endpoints without killing them</td>\n'
                    '      <td>Thundering herd if slow backends are prematurely saturated with traffic</td>\n'
                    '      <td>Combine shallow readiness with warm-up periods; apply client-side circuit breakers and '
                    'load shedding</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 89: Resilient Service Health, Resolution, and Messaging Lifecycle',
                  'desc': 'End-to-end traffic flow showing DNS routing, load balancer probe separation, and '
                          'asynchronous Pub/Sub decoupling.',
                  'caption': 'Figure 89.1: Tri-tier resilience model separating external DNS steering, local '
                             'application probe lifecycles, and asynchronous decoupled messaging.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Anycast Edge & DNS Health-Checked Failover',
                              'desc': 'Cloud DNS 100% SLA Authoritative Zone, Failover Routing Policy (30s TTL), and '
                                      'Anycast Resolution',
                              'fill': '#1e3a5f',
                              'y': 10,
                              'h': 90},
                             {'name': 'LAYER 2: Regional Load Balancing & Ingress Probe Tier',
                              'desc': 'Cloud Load Balancing, Shallow Health Checks (/healthz/shallow), and Connection '
                                      'Draining (30s timeout)',
                              'fill': '#0f2338',
                              'y': 115,
                              'h': 90},
                             {'name': 'LAYER 3: Container Orchestration & Probe Lifecycle Tier',
                              'desc': 'GKE/Cloud Run Workload, Liveness vs Readiness Probe Isolation, and SIGTERM '
                                      'PreStop Drain Hook',
                              'fill': '#064e3b',
                              'y': 220,
                              'h': 90},
                             {'name': 'LAYER 4: Enterprise Asynchronous Messaging Fabric',
                              'desc': 'Cloud Pub/Sub Regional Storage Governance, Dead-Letter Topic (DLQ), and '
                                      'Idempotent Consumers',
                              'fill': '#1e1b4b',
                              'y': 325,
                              'h': 90},
                             {'name': 'LAYER 5: SRE Telemetry & DLQ Quarantine Auditing',
                              'desc': 'Cloud Monitoring Backlog Telemetry, Synthetic Deep Health Probes '
                                      '(/healthz/deep), and PagerDuty Alerts',
                              'fill': '#3b0764',
                              'y': 430,
                              'h': 90}],
                  'components': [{'id': 'cloud_dns_failover',
                                  'name': 'Cloud DNS Failover',
                                  'detail': '100% SLA Anycast Zone (30s TTL)',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'anycast_resolver',
                                  'name': 'Anycast Edge Health',
                                  'detail': 'Cloud Monitoring Health Probing',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'alb_shallow_hc',
                                  'name': 'Regional ALB Ingress',
                                  'detail': 'Shallow Probe (/healthz/shallow)',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'conn_drain_gate',
                                  'name': 'Backend Drain Gate',
                                  'detail': '30s In-Flight Connection Drain',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'k8s_readiness_probe',
                                  'name': 'Readiness Probe Router',
                                  'detail': 'Removes Degraded Pod from Endpoints',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'k8s_liveness_drain',
                                  'name': 'Liveness & SIGTERM',
                                  'detail': 'PreStop Sleep 5s + Clean Process Exit',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'pubsub_regional_topic',
                                  'name': 'Pub/Sub Orders Topic',
                                  'detail': 'allowedPersistenceRegions: us-central1',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'pubsub_dlq_router',
                                  'name': 'Dead-Letter Topic',
                                  'detail': 'Diverts after 5 Failed Attempts',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'dlq_triage_dashboard',
                                  'name': 'DLQ Quarantine Triage',
                                  'detail': 'num_undelivered_messages Alerting',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'},
                                 {'id': 'synthetic_deep_probes',
                                  'name': 'Synthetic Deep Probes',
                                  'detail': '/healthz/deep Dependency Auditing',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'}],
                  'boundaries': [{'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'GLOBAL ANYCAST RESOLUTION & HEALTH CHECK PERIMETER',
                                  'color': '#38bdf8'},
                                 {'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'label': 'APPLICATION INGRESS & CONTAINER RUNTIME PROBE BOUNDARY',
                                  'color': '#10b981'},
                                 {'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'ENTERPRISE ASYNCHRONOUS MESSAGING & DATA BOUNDARY',
                                  'color': '#a855f7'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'type': 'ok', 'label': 'DNS Query Resolution'},
                            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'type': 'ok', 'label': 'Route to Regional VIP'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'type': 'ok',
                             'label': 'Drain Terminating Backends'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'type': 'ok',
                             'label': 'Forward Healthy Requests'},
                            {'x1': 340,
                             'y1': 266,
                             'x2': 420,
                             'y2': 266,
                             'type': 'ok',
                             'label': 'Handle SIGTERM Gracefully'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'type': 'ok',
                             'label': 'Publish Async Checkout Event'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'type': 'fail',
                             'label': 'Divert Poison Pill to DLQ'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'type': 'ok',
                             'label': 'Emit Backlog SLI Telemetry'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'type': 'ok',
                             'label': 'Audit Downstream Dependencies'}],
                  'probes': [{'cx': 420,
                              'cy': 56,
                              'label': 'PROBE 1: DNS Health Check Heartbeat (5s)',
                              'color': '#38bdf8'},
                             {'cx': 210,
                              'cy': 240,
                              'label': 'PROBE 2: Container Readiness Isolation Gate',
                              'color': '#22c55e'},
                             {'cx': 420,
                              'cy': 371,
                              'label': 'PROBE 3: Dead-Letter Queue Diversion Counter',
                              'color': '#ef4444'}]},
 'topics': [{'key': 'topic-01',
             'title': '**Messaging',
             'preview': 'A regional network degradation causes an unhandled payload exception in a payment ingestion '
                        'service, resulting in continuous subscriber container crash loops that exhaust compute '
                        'cluster memory and halt 45,000 pending customer orders.',
             'overview': 'Google Cloud Pub/Sub provides horizontally scalable, globally available asynchronous '
                         "messaging with at-least-once delivery guarantees. Understanding Pub/Sub's architectural "
                         'boundaries is critical for enterprise reliability. By default, Pub/Sub topics have a global '
                         'resource scope, automatically routing message publication and subscription across all Google '
                         'Cloud regions. However, highly regulated workloads subject to data sovereignty mandates '
                         '(e.g. GDPR, HIPAA) require strict message storage policies to restrict persisted data to '
                         'explicitly allowed Google Cloud regions. Furthermore, subscriber resilience requires '
                         'proactive handling of poison pills (malformed payloads that repeatedly trigger subscriber '
                         'crashes) through Dead-Letter Topics (DLQs) and configurable retry delays, coupled with '
                         'client-side deduplication logic to ensure idempotency.',
             'technical': '### 1. Pub/Sub Architectural Scope and Regional Endpoints\n'
                          '- **Global Scope vs Regional Ingress:** Pub/Sub topic and subscription resource IDs exist '
                          'globally within a project (`projects/{project}/topics/{topic}`). In standard mode, '
                          "publishers send traffic to `pubsub.googleapis.com`, which uses Google's global Anycast "
                          'network to terminate TLS at the nearest point of presence (PoP). For strict network '
                          'isolation and compliance, clients can target regional service endpoints (e.g., '
                          '`us-central1-pubsub.googleapis.com`), ensuring that network transit remains strictly within '
                          'the designated geographic boundary.\n'
                          '- **Message Storage Policies (`allowedPersistenceRegions`):** When publishers deliver '
                          'messages, Pub/Sub persists data in at least two zones within an approved region. '
                          'Organizations can enforce an organization policy constraint '
                          '(`constraints/gcp.resourceLocations`) or define custom message storage policies on topics. '
                          'If a publisher sends data while all allowed persistence regions are experiencing '
                          'disruptions, Pub/Sub rejects the write with an error rather than violating data residency '
                          'constraints.\n'
                          '\n'
                          '### 2. Failure Handling, Dead-Letter Topics, and Exponential Backoff\n'
                          '- **Acknowledgment Deadlines:** When a subscriber pulls a message, it has a default '
                          '10-second ack deadline (configurable up to 600 seconds). If the subscriber crashes or fails '
                          'to call `acknowledge()` before the deadline expires, the message is redelivered. '
                          'High-throughput consumers must use automatic deadline extension libraries or manually send '
                          '`modifyAckDeadline` requests for long-running jobs.\n'
                          '- **Dead-Letter Topics (DLQs):** A poison message (e.g., JSON syntax error, unhandled '
                          'schema variation) will crash the subscriber, fail acknowledgment, get redelivered, and '
                          'crash the subscriber indefinitely. By configuring a Dead-Letter Topic and setting '
                          '`maxDeliveryAttempts` (typically 5), Pub/Sub automatically diverts persistently failing '
                          'messages away from the primary subscription, allowing normal traffic to proceed without '
                          'head-of-line blocking.\n'
                          '- **Retry Policies:** Configure exponential backoff (e.g., minimum backoff 10s, maximum '
                          'backoff 600s) on subscriptions to prevent overwhelming downstream microservices during '
                          'service recovery.\n'
                          '\n'
                          '### 3. Idempotency and Ordering Guarantees\n'
                          '- **At-Least-Once Delivery:** Pub/Sub guarantees that every published message is delivered '
                          'at least once. Duplicate deliveries occur when network acknowledgments are dropped, during '
                          'broker rebalancing, or when ack deadlines expire prematurely. Subscribers *must* be '
                          'engineered for idempotency using a deduplication key (e.g., inserting message IDs into '
                          'Redis with a TTL or leveraging relational unique constraints).\n'
                          '- **Message Ordering:** When ordering keys are enabled, Pub/Sub delivers messages with the '
                          'same ordering key strictly in the order they were published. However, if a message with an '
                          'ordering key fails or redelivery is pending, all subsequent messages for that key are '
                          'halted until the head message is acknowledged or routed to a DLQ.',
             'questions': ["What happens when all regions listed in a Pub/Sub topic's message storage policy become "
                           'unavailable?',
                           'Why does ordering key enablement increase latency and head-of-line blocking risk during '
                           'subscriber processing errors?',
                           'How does dead-lettering prevent consumer starvation in high-volume asynchronous '
                           'transaction pipelines?'],
             'reference': 'https://docs.cloud.google.com/pubsub/docs/overview',
             'reference_label': 'Google Cloud Pub/Sub: Service architecture, message storage policies, and reliability '
                                'semantics',
             'scenario': {'symptom': "Brightloaf's asynchronous checkout processing subscription experienced an "
                                     'unhandled null pointer exception caused by a corrupted shopping cart payload. '
                                     'The subscriber worker crashed immediately upon reading the message, failed to '
                                     'acknowledge it, and re-read the same message upon pod restart. Within 20 '
                                     'minutes, 120 worker pods entered CrashLoopBackOff, causing 45,000 valid checkout '
                                     'messages to accumulate in the backlog and delaying order confirmations by 90 '
                                     'minutes.',
                          'constraints': 'Must maintain 99.95% message processing SLA without dropping unprocessable '
                                         'messages, and prevent bad payloads from crashing subscriber pools.',
                          'evidence': 'Cloud Monitoring and container logs captured the cascading poison pill '
                                      'failure:\n'
                                      '\n'
                                      '```\n'
                                      '[2026-09-29T14:02:11.412Z] ERROR [checkout-worker-7f98b6c4-v8k2m] '
                                      'JSONParseException: Unexpected end-of-input at position 1024\n'
                                      '    at com.brightloaf.orders.OrderParser.deserialize(OrderParser.java:84)\n'
                                      '    at '
                                      'com.brightloaf.orders.OrderSubscriber.receiveMessage(OrderSubscriber.java:120)\n'
                                      '[2026-09-29T14:02:11.415Z] FATAL [checkout-worker-7f98b6c4-v8k2m] Thread-4 '
                                      'uncaught exception terminating JVM runtime\n'
                                      '[2026-09-29T14:02:11.902Z] INFO  kubelet Pod checkout-worker-7f98b6c4-v8k2m '
                                      'failed liveness probe, restarting container (restartCount=14)\n'
                                      '$ gcloud monitoring metrics-scopes list ...\n'
                                      'pubsub.googleapis.com/subscription/num_undelivered_messages: 45,820\n'
                                      'pubsub.googleapis.com/subscription/dead_letter_message_count: 0 (No DLQ '
                                      'configured)\n'
                                      'k8s.io/pod/restart_count: 822 restarts across 120 worker pods within 15 '
                                      'minutes\n'
                                      '```',
                          'diagnostic_steps': ['Inspect subscriber application logs to capture the stack trace and '
                                               'offending message payload.',
                                               'Verify subscription configuration to check if dead-lettering and retry '
                                               'policies are enabled.',
                                               'Inspect Pub/Sub backlog metrics to identify processing throughput '
                                               'degradation and redelivery spikes.'],
                          'root': 'The checkout subscription lacked a Dead-Letter Topic and retry policy, causing a '
                                  'single poisoned message to be redelivered indefinitely, starving worker threads and '
                                  'crashing compute nodes in a fatal positive feedback loop.',
                          'fix': 'Configure a Dead-Letter Topic (`checkout-poison-dlq`) with `maxDeliveryAttempts = 5` '
                                 'and a minimum retry backoff of 10s. Implement a defensive JSON schema validator in '
                                 'the subscriber code that traps parsing errors, logs payload telemetry, and sends '
                                 'negative acknowledgments or moves invalid payloads to quarantine.',
                          'verify': 'Publish a synthetic malformed payload to the staging checkout topic; confirm the '
                                    'subscriber attempts processing 5 times with exponential backoff, diverts the '
                                    'message to the DLQ, and continues processing downstream valid messages without '
                                    'pod restarts.',
                          'residual': 'Messages in the Dead-Letter Topic expire after the topic retention period '
                                      '(default 7 days) if an operations alert is not triaged.',
                          'diagram': ('Malformed message published',
                                      'Infinite subscriber crash loop',
                                      '45k messages stuck in backlog',
                                      'Dead-Letter Topic configured',
                                      'DLQ diversion after 5 retries'),
                          'facts': 'A single corrupted payload crashed 120 subscriber pods repeatedly because no '
                                   'Dead-Letter Topic was configured.',
                          'inference': 'Without DLQ circuit breaking, poison messages convert localized data bugs into '
                                       'total pipeline outages.',
                          'expected': 'Poison messages divert to DLQ after 5 attempts; subscriber pods maintain 100% '
                                      'uptime for healthy backlog processing.'},
             'lab': {'name': 'Pub/Sub Dead-Letter Queue and Storage Policy Verification',
                     'file': 'day-089-topic-01-pubsub-resilience.md',
                     'goal': 'Author and verify a resilient Pub/Sub architecture defining regional message storage '
                             'policies, DLQ dead-lettering, and subscriber idempotency.',
                     'expected': 'A comprehensive configuration document and runnable shell script simulating poison '
                                 'message diversion to a dead-letter topic.',
                     'mode': 'tabletop analysis & production CLI / YAML execution',
                     'prereq': 'Understanding of asynchronous event-driven architectures.',
                     'preflight': 'Review Pub/Sub dead-letter documentation and schema validation patterns.',
                     'steps': ['#### Stage 1: Pre-Flight Pub/Sub Topology & Regional Persistence Invariants\n'
                               "Establish the messaging architecture invariants for Brightloaf's checkout pipeline:\n"
                               '- **Topic Scope:** Enterprise regional persistence constrained strictly to '
                               '`us-central1` and `us-east1` to comply with US data sovereignty mandates.\n'
                               '- **Dead-Letter Policy:** Maximum delivery attempts set to `5`. Unprocessable payloads '
                               'are automatically diverted to `orders-dlq` to prevent head-of-line blocking.\n'
                               '- **Subscriber Idempotency:** Subscriptions enforce exponential retry backoff (minimum '
                               '10s, maximum 300s) and consumers execute atomic deduplication before persisting '
                               'records.',
                               '#### Stage 2: Environment Preflight & Ingress Boundary Verification\n'
                               'Author a preflight validation script (<kbd>check_pubsub_env.py</kbd>) verifying '
                               'project variables and IAM roles:\n'
                               '\n'
                               '```python\n'
                               '# check_pubsub_env.py\n'
                               'import os\n'
                               '\n'
                               "project = os.environ.get('PROJECT_ID', 'brightloaf-prod')\n"
                               "allowed_regions = ['us-central1', 'us-east1']\n"
                               "print(f'[PREFLIGHT] Validating Pub/Sub configuration for project: {project}')\n"
                               "print(f'[PREFLIGHT] Target persistence policy: {allowed_regions}')\n"
                               "assert len(allowed_regions) >= 2, 'Must configure multi-region persistence "
                               "redundancy'\n"
                               "print('[PASS] Preflight messaging environment invariants verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight verification:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_pubsub_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Provision Topics & Regional Persistence Policy\n'
                               'Provision the dead-letter topic and the primary checkout topic with regional storage '
                               'constraints:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > provision_pubsub.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'echo "Provisioning Dead-Letter Topic: orders-dlq..."\n'
                               'gcloud pubsub topics create orders-dlq \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --message-retention-duration=14d || true\n'
                               '\n'
                               'echo "Provisioning DLQ Audit Subscription: orders-dlq-sub..."\n'
                               'gcloud pubsub subscriptions create orders-dlq-sub \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --topic=orders-dlq \\\n'
                               '    --ack-deadline=60 || true\n'
                               '\n'
                               'echo "Provisioning Primary Topic with Regional Storage Constraint: orders-v1..."\n'
                               'gcloud pubsub topics create orders-v1 \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --message-storage-policy-allowed-regions=us-central1,us-east1 || true\n'
                               'EOF\n'
                               'chmod +x provision_pubsub.sh\n'
                               './provision_pubsub.sh\n'
                               '```',
                               '#### Stage 4: Execution & IAM Service Agent Permissions Binding\n'
                               'Grant the Google Cloud Pub/Sub service agent authority to publish to the DLQ and '
                               'acknowledge forwarded messages:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > bind_pubsub_iam.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" '
                               "--format='value(projectNumber)')\n"
                               'PUBSUB_SA="service-${PROJECT_NUMBER}@gcp-sa-pubsub.iam.gserviceaccount.com"\n'
                               '\n'
                               'echo "Granting roles/pubsub.publisher on orders-dlq to ${PUBSUB_SA}..."\n'
                               'gcloud pubsub topics add-iam-policy-binding orders-dlq \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --member="serviceAccount:${PUBSUB_SA}" \\\n'
                               '    --role="roles/pubsub.publisher"\n'
                               '\n'
                               'echo "Provisioning Primary Subscription with DLQ policy..."\n'
                               'gcloud pubsub subscriptions create orders-v1-sub \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --topic=orders-v1 \\\n'
                               '    --ack-deadline=30 \\\n'
                               '    --dead-letter-topic=orders-dlq \\\n'
                               '    --max-delivery-attempts=5 \\\n'
                               '    --min-retry-delay=10s \\\n'
                               '    --max-retry-delay=300s || true\n'
                               '\n'
                               'echo "Granting roles/pubsub.subscriber on orders-v1-sub to ${PUBSUB_SA}..."\n'
                               'gcloud pubsub subscriptions add-iam-policy-binding orders-v1-sub \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --member="serviceAccount:${PUBSUB_SA}" \\\n'
                               '    --role="roles/pubsub.subscriber"\n'
                               'EOF\n'
                               'chmod +x bind_pubsub_iam.sh\n'
                               './bind_pubsub_iam.sh\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Poison Payload Chaos Injection\n'
                               'Author a chaos simulation script (<kbd>simulate_poison_pill.py</kbd>) that publishes a '
                               'corrupted payload and simulates subscriber behavior:\n'
                               '\n'
                               '```python\n'
                               '# simulate_poison_pill.py\n'
                               'import json\n'
                               'import time\n'
                               '\n'
                               "print('--- SIMULATING POISON MESSAGE PROCESSING ---')\n"
                               'poison_payload = \'{ "order_id": 9999, "cart": [MALFORMED_JSON_SYNTAX\'  # Corrupted '
                               'JSON\n'
                               'delivery_attempts = 0\n'
                               'max_attempts = 5\n'
                               'routed_to_dlq = False\n'
                               '\n'
                               'while delivery_attempts < max_attempts:\n'
                               '    delivery_attempts += 1\n'
                               "    print(f'[Worker] Received message attempt {delivery_attempts}/{max_attempts}...')\n"
                               '    try:\n'
                               '        json.loads(poison_payload)\n'
                               '    except json.JSONDecodeError as err:\n'
                               "        print(f'[Worker ERROR] Parse failed: {err}. Rejecting ack (nack).')\n"
                               '        time.sleep(0.1)\n'
                               '\n'
                               'if delivery_attempts >= max_attempts:\n'
                               "    print(f'[PubSub Control Plane] Max delivery attempts ({max_attempts}) exceeded.')\n"
                               "    print('[PubSub Control Plane] Forwarding message to orders-dlq topic.')\n"
                               '    routed_to_dlq = True\n'
                               '\n'
                               "assert routed_to_dlq, 'Poison pill must be routed to DLQ after 5 failed attempts'\n"
                               "print('[PASS] Chaos simulation passed: poison pill diverted without worker crash "
                               "loop.')\n"
                               '```\n'
                               '\n'
                               'Execute chaos test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_poison_pill.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Backlog Triage\n'
                               'Inspect Pub/Sub monitoring metrics to verify dead-letter diversion and backlog '
                               'health:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_telemetry.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Simulating Cloud Monitoring MQL query for orders backlog..."\n'
                               "cat <<'MQL'\n"
                               'fetch pubsub_subscription\n'
                               "| metric 'pubsub.googleapis.com/subscription/num_undelivered_messages'\n"
                               "| filter (resource.subscription_id == 'orders-v1-sub')\n"
                               '| group_by [resource.subscription_id], sum(val())\n'
                               'MQL\n'
                               'echo "[METRIC CHECK] num_undelivered_messages = 0"\n'
                               'echo "[METRIC CHECK] dead_letter_message_count = 1"\n'
                               'echo "[OBSERVABILITY PASS] Worker pods maintained 100% liveness without '
                               'CrashLoopBackOff."\n'
                               'EOF\n'
                               'chmod +x verify_telemetry.sh\n'
                               './verify_telemetry.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Deduplication Assertion\n'
                               'Author an automated Python test (<kbd>test_pubsub_resilience.py</kbd>) that validates '
                               'storage policy and subscriber deduplication logic:\n'
                               '\n'
                               '```python\n'
                               '# test_pubsub_resilience.py\n'
                               'import hashlib\n'
                               '\n'
                               'processed_cache = set()\n'
                               '\n'
                               'def process_order(message_id, payload):\n'
                               '    # Idempotent deduplication gate\n'
                               "    msg_hash = hashlib.sha256(f'{message_id}:{payload}'.encode()).hexdigest()\n"
                               '    if msg_hash in processed_cache:\n'
                               "        return 'DUPLICATE_ACK'\n"
                               '    processed_cache.add(msg_hash)\n'
                               "    return 'PROCESSED_OK'\n"
                               '\n'
                               '# Test duplicate redelivery\n'
                               'assert process_order(\'msg-101\', \'{"item":"bread"}\') == \'PROCESSED_OK\'\n'
                               'assert process_order(\'msg-101\', \'{"item":"bread"}\') == \'DUPLICATE_ACK\'\n'
                               'assert len(processed_cache) == 1\n'
                               "print('[ASSERT PASS] Idempotency deduplication logic verified.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_pubsub_resilience.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a safe teardown script removing simulated resources and test artifacts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_pubsub_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 89 Topic 1 test scripts..."\n'
                               'rm -f check_pubsub_env.py provision_pubsub.sh bind_pubsub_iam.sh '
                               'simulate_poison_pill.py verify_telemetry.sh test_pubsub_resilience.py\n'
                               'echo "[CLEANUP] Retaining day-089-topic-01-pubsub-resilience.md evidence '
                               'documentation."\n'
                               'echo "[CLEANUP PASS] Teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_pubsub_lab.sh\n'
                               './teardown_pubsub_lab.sh\n'
                               '```'],
                     'verification': 'Document exists, contains valid gcloud commands for DLQ creation with IAM '
                                     'bindings, and specifies idempotency controls.',
                     'trouble': 'Ensure Pub/Sub Service Agent IAM permissions are assigned before binding the '
                                'dead-letter topic to the subscription.',
                     'cleanup': 'Retain `day-089-topic-01-pubsub-resilience.md` as an exit evidence artifact.',
                     'accept': 'Completed Pub/Sub architecture document with verified DLQ and idempotency patterns.'}},
            {'key': 'topic-02',
             'title': '**DNS',
             'preview': 'A regional database outage forces network engineers to manually update Cloud DNS records, but '
                        'branch offices continue sending requests to the failed region for 45 minutes because local '
                        'corporate resolvers ignore standard TTL expirations.',
             'overview': "Google Cloud DNS provides authoritative domain name resolution backed by Google's global "
                         'Anycast infrastructure, delivering a 100% availability service level agreement (SLA) for '
                         'external public queries. While Cloud DNS authoritative servers never go down, the '
                         'applications relying on DNS for multi-region steering and disaster recovery face major '
                         'operational constraints. Traditional DNS failover relies on Time-To-Live (TTL) values; '
                         'however, recursive DNS resolvers across public ISPs and corporate intranets frequently cache '
                         'responses far longer than the configured TTL, creating unpredictable failover latency. To '
                         'address this, Cloud DNS offers intelligent routing policies—including Geolocation routing, '
                         'Weighted round-robin routing, and Health-Checked Failover routing—which automatically alter '
                         'response records based on backend health without requiring manual operator intervention.',
             'technical': '### 1. Cloud DNS 100% Availability SLA Conditions\n'
                          '- **Authoritative Architecture:** Cloud DNS is hosted across hundreds of Anycast edge '
                          'locations globally. When a client queries `ns-cloud-*.googledomains.com`, BGP routes the '
                          'query to the nearest healthy Google edge node, ensuring instant multi-path redundancy and '
                          'an authoritative uptime SLA of 100%.\n'
                          '- **SLA Scope and Exclusions:** The 100% SLA applies exclusively to the availability of the '
                          'authoritative name server responding to valid DNS queries. It does *not* cover '
                          'misconfigured DNS records, propagation latency caused by third-party recursive resolvers, '
                          'or failures of the underlying target backend services.\n'
                          '\n'
                          '### 2. Cloud DNS Advanced Routing Policies\n'
                          '- **Geolocation Routing:** Directs DNS queries to specific IP endpoints based on the '
                          "geographic origin of the client's query (determined via EDNS Client Subnet - ECS). For "
                          'example, European users resolve to `europe-west1` VIPs while North American users resolve '
                          'to `us-central1` VIPs, reducing round-trip latency.\n'
                          '- **Weighted Round-Robin (WRR):** Enables percentage-based traffic distribution across '
                          'multiple IP targets. This is standard for blue/green environment transitions, regional '
                          'capacity rebalancing, and canary releases (e.g., 95% traffic to `v1`, 5% to `v2`).\n'
                          '- **Failover Routing with Health Checks:** Cloud DNS pairs with Cloud Monitoring regional '
                          'health checks. Architects define a primary target (e.g. `us-central1` ALB VIP) and a backup '
                          'target (e.g. `us-east1` ALB VIP). Cloud Monitoring probes the primary endpoint every 5–10 '
                          'seconds. When health probes fail across consecutive intervals, Cloud DNS automatically '
                          'ceases returning the primary IP and answers subsequent queries exclusively with the backup '
                          'IP.\n'
                          '\n'
                          '### 3. DNS TTL Mechanics and Resolver Realities\n'
                          '- **TTL Trade-Offs:** A low TTL (e.g., 30s or 60s) accelerates failover propagation across '
                          'internet resolvers during disaster recovery. However, low TTL dramatically increases the '
                          'total query volume against Cloud DNS and increases client lookup latency by bypassing local '
                          'resolver caches.\n'
                          '- **Recursive Resolver Non-Compliance:** Even with a 30s TTL, roughly 10%–25% of enterprise '
                          'recursive resolvers enforce a minimum caching floor (often 5 to 15 minutes). Therefore, DNS '
                          'failover alone cannot guarantee sub-minute RTO. For true sub-second failover, architects '
                          'must deploy an Anycast Global External Application Load Balancer (single global VIP with '
                          'multi-region backend services) rather than relying on DNS-based steering.',
             'questions': ["Why does Cloud DNS's 100% availability SLA fail to protect clients from prolonged downtime "
                           'during an unmitigated regional service failure?',
                           'What is the difference in operational failover speed between DNS-based failover and Global '
                           'Anycast Load Balancer failover?',
                           'How does EDNS Client Subnet (ECS) influence Cloud DNS geolocation routing accuracy?'],
             'reference': 'https://docs.cloud.google.com/dns/docs/policies-overview',
             'reference_label': 'Google Cloud DNS: Routing policies, health checks, and failover architecture',
             'scenario': {'symptom': 'During a scheduled data center maintenance event, Brightloaf changed their '
                                     'primary web portal DNS A-record to point to the backup datacenter. While '
                                     'internal engineers observed immediate redirection, 32% of retail store '
                                     'point-of-sale terminals continued attempting to connect to the deactivated '
                                     'primary IP for over 40 minutes, causing point-of-sale checkout stalls.',
                          'constraints': 'Must automate regional failover steering without requiring manual DNS zone '
                                         'edits during unannounced catastrophic outages.',
                          'evidence': 'Authoritative versus recursive DNS resolver diagnostics captured the caching '
                                      'freeze:\n'
                                      '\n'
                                      '```\n'
                                      '$ dig +noall +answer @ns-cloud-a1.googledomains.com api.brightloaf.com\n'
                                      'api.brightloaf.com.   30      IN   A   34.107.20.2 (Authoritative Cloud DNS: '
                                      'Failover to US-East1 ACTIVE)\n'
                                      '\n'
                                      '$ dig +noall +answer @8.8.8.8 api.brightloaf.com\n'
                                      'api.brightloaf.com.   74120   IN   A   34.102.10.1 (ISP / Recursive Cache: '
                                      'Stale US-Central1 OFFLINE)\n'
                                      '\n'
                                      '$ gcloud dns managed-zones describe brightloaf-zone '
                                      "--format='value(description, dnssecConfig.state)'\n"
                                      'Brightloaf Production Anycast Zone  on\n'
                                      'Cloud Monitoring Health Check: primary-regional-hc returned UNHEALTHY at '
                                      '14:00:15 UTC\n'
                                      'Failed transactions: 3,420 point-of-sale timeouts recorded across 140 retail '
                                      'branches\n'
                                      '```',
                          'diagnostic_steps': ['Query authoritative name servers directly using dig with target '
                                               '@ns-cloud-a1.googledomains.com api.brightloaf.com to verify '
                                               'authoritative answer.',
                                               'Query public recursive resolvers (Google 8.8.8.8, Cloudflare 1.1.1.1) '
                                               'to compare TTL countdowns.',
                                               'Audit past DNS record modifications and historical TTL settings in '
                                               'Cloud DNS change logs.'],
                          'root': 'The DNS record TTL was maintained at 86,400 seconds until the moment of failover; '
                                  'DNS TTLs must be lowered days in advance of planned changes, or maintained '
                                  'permanently at 60s with automated health-checked routing policies.',
                          'fix': 'Transition the DNS zone to a Cloud DNS Failover Routing Policy with a permanent '
                                 '30-second TTL, tied to an automated Cloud Monitoring health check probing the '
                                 'primary load balancer VIP. Deploy Global External Application Load Balancing across '
                                 'regions as the primary steering mechanism, reserving DNS failover for catastrophic '
                                 'global control-plane events.',
                          'verify': 'Simulate primary VIP failure in staging by blocking health-check probe ports; '
                                    'verify Cloud DNS automatically switches answer records to the backup VIP within '
                                    '60 seconds across all public recursive test resolvers.',
                          'residual': 'A 30-second TTL increases external DNS query billing volume and slightly '
                                      'increases first-hit client lookup latency.',
                          'diagram': ('24h TTL record cached globally',
                                      'Manual DNS IP change applied',
                                      'Retail terminals cached on old IP',
                                      'Cloud DNS health-checked policy',
                                      'Automated switch in 30s TTL window'),
                          'facts': 'Point-of-sale terminals failed for 40 minutes because the DNS A-record TTL was '
                                   '86,400 seconds at the time of change.',
                          'inference': 'DNS cannot serve as an emergency failover mechanism unless TTLs are '
                                       'consistently short and steering is automated.',
                          'expected': 'Cloud DNS Failover Policy automatically pivots client traffic within 60 seconds '
                                      'of health-check failure.'},
             'lab': {'name': 'Cloud DNS Health-Checked Failover Routing Policy Synthesis',
                     'file': 'day-089-topic-02-dns-routing.md',
                     'goal': 'Author and verify an automated Cloud DNS Failover Routing Policy with health checks and '
                             'short TTL steering.',
                     'expected': 'A comprehensive configuration guide with exact gcloud commands establishing health '
                                 'checks and failover record sets.',
                     'mode': 'tabletop analysis & production CLI / YAML execution',
                     'prereq': 'Understanding of DNS hierarchy and Anycast networking.',
                     'preflight': 'Review Cloud DNS routing policies documentation.',
                     'steps': ['#### Stage 1: Pre-Flight Cloud DNS Invariants & Anycast Architecture\n'
                               "Establish the authoritative DNS resolution invariants for Brightloaf's e-commerce "
                               'API:\n'
                               '- **Authoritative SLA:** Cloud DNS provides a 100% availability SLA for Anycast '
                               'resolution across global edge PoPs.\n'
                               '- **Failover Policy:** Configure Cloud DNS Failover Routing Policy with a permanent '
                               '**30-second TTL** to bound resolver caching delays.\n'
                               '- **Health Integration:** Cloud Monitoring regional HTTP health check targets '
                               '`/healthz/shallow` every 5 seconds. Unhealthy threshold is 2 consecutive failures.',
                               '#### Stage 2: Environment Preflight & Authoritative Zone Inspection\n'
                               'Author a preflight validation script (<kbd>check_dns_env.py</kbd>) that verifies DNS '
                               'zone configuration:\n'
                               '\n'
                               '```python\n'
                               '# check_dns_env.py\n'
                               'zone_config = {\n'
                               "    'name': 'brightloaf-zone',\n"
                               "    'domain': 'brightloaf.com.',\n"
                               "    'target_ttl': 30,\n"
                               "    'routing_policy': 'FAILOVER',\n"
                               '}\n'
                               'print(f\'[PREFLIGHT] Validating DNS Managed Zone: {zone_config["name"]}\')\n'
                               "assert zone_config['target_ttl'] <= 60, 'TTL must be 60 seconds or lower for dynamic "
                               "failover'\n"
                               "assert zone_config['routing_policy'] == 'FAILOVER', 'Policy type must be FAILOVER'\n"
                               "print('[PASS] Preflight DNS invariants validated.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight validation:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_dns_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Cloud Monitoring Regional Health Check\n'
                               'Author the deployment script creating the regional health check for Cloud DNS:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > create_dns_health_check.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'echo "Creating Regional HTTP Health Check for Cloud DNS..."\n'
                               'gcloud compute health-checks create http primary-regional-hc \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --region=us-central1 \\\n'
                               '    --port=80 \\\n'
                               '    --request-path="/healthz/shallow" \\\n'
                               '    --check-interval=5s \\\n'
                               '    --timeout=3s \\\n'
                               '    --unhealthy-threshold=2 \\\n'
                               '    --healthy-threshold=1 || true\n'
                               'EOF\n'
                               'chmod +x create_dns_health_check.sh\n'
                               './create_dns_health_check.sh\n'
                               '```',
                               '#### Stage 4: Execution & Cloud DNS Failover Record Set Deployment\n'
                               'Deploy the Cloud DNS managed zone and the health-checked failover routing policy '
                               'record set:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > deploy_dns_policy.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'echo "Creating Managed DNS Zone brightloaf-zone..."\n'
                               'gcloud dns managed-zones create brightloaf-zone \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --dns-name="brightloaf.com." \\\n'
                               '    --description="Brightloaf Production Anycast Zone" \\\n'
                               '    --dnssec-state=on || true\n'
                               '\n'
                               'echo "Deploying Failover Record Set for api.brightloaf.com..."\n'
                               'gcloud dns record-sets create api.brightloaf.com. \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --zone=brightloaf-zone \\\n'
                               '    --type=A \\\n'
                               '    --ttl=30 \\\n'
                               '    --routing-policy-type=FAILOVER \\\n'
                               '    --routing-policy-data="primary=34.102.10.1,backup=34.107.20.2" \\\n'
                               '    --health-check=primary-regional-hc || true\n'
                               'EOF\n'
                               'chmod +x deploy_dns_policy.sh\n'
                               './deploy_dns_policy.sh\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Failover Chaos Simulation\n'
                               'Author a script (<kbd>simulate_dns_failover.py</kbd>) modeling resolver caching decay '
                               'and traffic steering:\n'
                               '\n'
                               '```python\n'
                               '# simulate_dns_failover.py\n'
                               'import time\n'
                               '\n'
                               "print('--- SIMULATING CLOUD DNS FAILOVER DECAY ---')\n"
                               'timeline = [\n'
                               "    (0, 'Primary VIP 34.102.10.1 experiences outage', 100, 0),\n"
                               "    (10, 'Health check primary-regional-hc marks Primary UNHEALTHY', 100, 0),\n"
                               "    (15, 'Cloud DNS updates authoritative answer to Backup 34.107.20.2', 100, 0),\n"
                               "    (45, 'Compliant ISP resolvers (TTL=30s) expire stale cache', 40, 60),\n"
                               "    (75, '95% of public recursive resolvers updated to Backup VIP', 5, 95),\n"
                               "    (120, '100% of traffic successfully steered to Backup VIP', 0, 100),\n"
                               ']\n'
                               'for sec, event, primary_pct, backup_pct in timeline:\n'
                               "    print(f'T+{sec:03d}s: {event:60s} | Primary: {primary_pct:3d}% | Backup: "
                               "{backup_pct:3d}%')\n"
                               "print('[PASS] Failover timeline modeled within acceptable bounds.')\n"
                               '```\n'
                               '\n'
                               'Execute simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_dns_failover.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & DNS Propagation Verification\n'
                               'Author a verification script querying simulated public resolvers to measure '
                               'propagation latency:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > query_resolvers.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Simulating multi-resolver DNS query audit..."\n'
                               "cat <<'TABLE'\n"
                               'Resolver IP        Resolved Target   TTL Remaining   Status\n'
                               '-----------------------------------------------------------\n'
                               'ns-cloud-a1 (Auth) 34.107.20.2       30s             ACTIVE (Backup)\n'
                               '8.8.8.8 (Google)   34.107.20.2       28s             UPDATED\n'
                               '1.1.1.1 (Cloudfl)  34.107.20.2       27s             UPDATED\n'
                               '9.9.9.9 (Quad9)    34.107.20.2       29s             UPDATED\n'
                               'TABLE\n'
                               'echo "[DNS OBSERVABILITY PASS] Authoritative and public recursive resolvers '
                               'synchronized."\n'
                               'EOF\n'
                               'chmod +x query_resolvers.sh\n'
                               './query_resolvers.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & TTL Assertion\n'
                               'Author an automated test (<kbd>test_dns_invariants.py</kbd>) asserting DNS record TTL '
                               'compliance:\n'
                               '\n'
                               '```python\n'
                               '# test_dns_invariants.py\n'
                               'records = [\n'
                               "    {'name': 'api.brightloaf.com.', 'type': 'A', 'ttl': 30, 'routing': 'FAILOVER'},\n"
                               "    {'name': 'static.brightloaf.com.', 'type': 'CNAME', 'ttl': 300, 'routing': "
                               "'GEO'},\n"
                               ']\n'
                               "failover_records = [r for r in records if r['routing'] == 'FAILOVER']\n"
                               'for r in failover_records:\n'
                               '    assert r[\'ttl\'] <= 60, f\'Failover record {r["name"]} has excessive TTL: '
                               '{r["ttl"]}\'\n'
                               "print('[ASSERT PASS] Failover record TTL verified <= 60 seconds.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_dns_invariants.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_dns_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 89 Topic 2 DNS test scripts..."\n'
                               'rm -f check_dns_env.py create_dns_health_check.sh deploy_dns_policy.sh '
                               'simulate_dns_failover.py query_resolvers.sh test_dns_invariants.py\n'
                               'echo "[CLEANUP] Retaining day-089-topic-02-dns-routing.md evidence documentation."\n'
                               'echo "[CLEANUP PASS] DNS teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_dns_lab.sh\n'
                               './teardown_dns_lab.sh\n'
                               '```'],
                     'verification': 'Document exists, includes valid gcloud DNS routing commands, and details an '
                                     'end-to-end DNS failover recovery timeline.',
                     'trouble': 'Ensure Cloud Monitoring health check is created in the same project and region as the '
                                'primary compute backend.',
                     'cleanup': 'Retain `day-089-topic-02-dns-routing.md` as an exit evidence artifact.',
                     'accept': 'Completed Cloud DNS health-checked routing specification and resolver latency '
                               'analysis.'}},
            {'key': 'topic-03',
             'title': '**Application',
             'preview': "A transient 5-second database lock causes an application's deep health check endpoint to "
                        'fail, triggering Google Cloud Load Balancing to mark all 80 backend instances unhealthy '
                        'simultaneously and plunging the entire site into a total 502 Bad Gateway outage.',
             'overview': 'Application health check design dictates how cloud orchestrators and load balancers detect, '
                         'isolate, and recover from software faults. A fundamental architectural trap in microservice '
                         'design is confounding shallow health checks with deep health checks. A **shallow health '
                         "check** verifies only the immediate process's responsiveness (e.g., HTTP listener alive, "
                         'event loop running, free local memory). A **deep health check** verifies the availability of '
                         'upstream and downstream dependencies (e.g., database connection pools, Redis caches, '
                         'third-party payment gateways). In load balancing and orchestrator restart loops, deep health '
                         'checks introduce catastrophic failure cascades. Furthermore, resilient applications must '
                         'clearly separate **readiness probes** (which control whether an instance receives user '
                         'traffic) from **liveness probes** (which trigger process termination and restart), and must '
                         'implement strict **graceful shutdown** routines to drain in-flight connections when SIGTERM '
                         'signals are issued.',
             'technical': '### 1. Shallow vs Deep Health Checks: Mechanics and Blast Radius\n'
                          '- **The Cascading Outage Anti-Pattern:** Consider a service with 100 instances behind a '
                          'load balancer. If the health check probes `/healthz/deep` which runs `SELECT 1 FROM '
                          'database;`, what happens if the database encounters connection pool exhaustion? All 100 '
                          'instances fail their health check at the exact same moment. The load balancer concludes '
                          'that zero instances are healthy and drops all backend routes, converting a minor database '
                          'slowdown into a complete total application outage.\n'
                          '- **Architectural Rule of Thumb:**\n'
                          "  1. **Load Balancer Health Checks:** Must *always* be shallow. They answer: *'Can this "
                          "specific compute instance parse HTTP requests and accept new socket connections?'*\n"
                          '  2. **Internal Dependency Health Checks:** Deep health checks should be reserved for '
                          'synthetic monitoring, operational dashboards, and administrative triage tools '
                          '(`/healthz/deep`), protected by authentication and decoupled from automatic traffic '
                          'routing.\n'
                          '\n'
                          '### 2. Kubernetes and Container Probe Taxonomy\n'
                          '- **Startup Probe:** Protects slow-starting legacy applications during container '
                          'initialization. Disables liveness and readiness checks until the startup probe succeeds, '
                          'preventing premature process termination.\n'
                          "- **Liveness Probe:** Answers: *'Is the process deadlocked or fatally corrupted?'* If a "
                          'liveness probe fails consecutively, kubelet kills the container and restarts it according '
                          'to its restart policy. Liveness probes must be extremely lightweight and should *never* '
                          'check external network resources.\n'
                          "- **Readiness Probe:** Answers: *'Is the application currently ready to accept user "
                          "requests?'* If a readiness probe fails (e.g., during local cache warming or temporary CPU "
                          'spikes), kubelet removes the Pod IP from the Kubernetes Service endpoints. The container is '
                          '*not* killed, preserving its state while traffic is diverted to other healthy pods.\n'
                          '\n'
                          '### 3. Graceful Shutdown and Connection Draining Mechanics\n'
                          '- **The Termination Sequence:**\n'
                          '  1. Orchestrator (Kubernetes/MIG) sends `SIGTERM` to the container process.\n'
                          '  2. Endpoint controller updates IP tables and Load Balancer begins backend draining.\n'
                          '  3. Application traps `SIGTERM`: stops accepting *new* connections, marks readiness '
                          'endpoint as unhealthy (`503 Service Unavailable`), and allows existing in-flight HTTP '
                          'requests to complete.\n'
                          '  4. After in-flight requests finish or the drain timeout elapses (e.g., 30s), the '
                          'application closes database pools and exits cleanly (exit code 0).\n'
                          '  5. If the application fails to terminate within `terminationGracePeriodSeconds` (e.g., '
                          '45s), the kernel sends `SIGKILL`.',
             'questions': ['Why does configuring a deep health check on a Cloud Load Balancer backend service violate '
                           'fault-isolation boundaries?',
                           'What is the difference in operational outcome when a liveness probe fails versus when a '
                           'readiness probe fails?',
                           "Why must the application's graceful shutdown timeout be coordinated with the load "
                           "balancer's backend connection drain timeout?"],
             'reference': 'https://docs.cloud.google.com/load-balancing/docs/health-check-concepts',
             'reference_label': 'Google Cloud Load Balancing: Health check architecture, probe types, and draining '
                                'behavior',
             'scenario': {'symptom': "During a midday traffic surge, Brightloaf's catalog service experienced a "
                                     'transient 10-second database connection pool saturation. Within 15 seconds, the '
                                     'Cloud Load Balancer marked 100% of catalog instances unhealthy, returning HTTP '
                                     '502 Bad Gateway to all shoppers across Europe and North America for 22 minutes.',
                          'constraints': 'Must maintain service availability during partial dependency degradations '
                                         'and isolate backend container restarts from transient external latency.',
                          'evidence': 'Application telemetry and load balancer access logs captured the cascading '
                                      'eviction:\n'
                                      '\n'
                                      '```\n'
                                      '[2026-09-29T14:02:10.104Z] HTTP 500 GET /healthz - DB pool timeout (borrow '
                                      'connection timeout 5000ms exceeded)\n'
                                      '[2026-09-29T14:02:15.220Z] google-cloud-loadbalancing: BackendService '
                                      "'catalog-backend-service' marked 60/60 backends UNHEALTHY\n"
                                      '[2026-09-29T14:02:15.225Z] HTTP 502 Bad Gateway returned to client '
                                      '198.51.100.44\n'
                                      '[2026-09-29T14:02:16.890Z] kubelet: Liveness probe failed for '
                                      'catalog-pod-4x8k1, restarting container (SIGKILL after 30s timeout)\n'
                                      'Load Balancer backend_status: healthy_backend_ratio = 0.00 across us-central1 '
                                      'and us-east1\n'
                                      'Application instance metrics: CPU 24%, Memory 38% (Compute instances were '
                                      'completely healthy)\n'
                                      '```',
                          'diagnostic_steps': ['Inspect Cloud Load Balancer backend service health metrics '
                                               '(`loadbalancing.googleapis.com/backend_status`).',
                                               'Review application health check handler source code to identify '
                                               'external network and database dependencies.',
                                               'Correlate database slow-query logs and connection pool telemetry with '
                                               'the exact timestamp of load balancer health check failures.'],
                          'root': 'Architectural anti-pattern: the load balancer health check was coupled to a deep '
                                  'database query rather than a shallow local process probe. When the database slowed '
                                  'down, healthy compute instances were prematurely evicted from the load balancer '
                                  'pool.',
                          'fix': 'Split health check endpoints into `/healthz/shallow` (validates HTTP listener and '
                                 'local memory; zero DB calls) and `/healthz/deep` (reports dependency status for '
                                 'monitoring only). Reconfigure Cloud Load Balancing to probe `/healthz/shallow`. '
                                 'Configure Kubernetes readiness probes to handle soft load shedding and liveness '
                                 'probes to monitor process runloops.',
                          'verify': 'Simulate database connection pool exhaustion in staging; confirm that '
                                    '`/healthz/deep` returns 503 while `/healthz/shallow` returns 200 OK. Confirm '
                                    'Cloud Load Balancing continues routing traffic without dropping instances from '
                                    'the backend pool.',
                          'residual': 'Shallow health checks do not detect if a container has lost database '
                                      'connectivity; application code must return clean HTTP 503 or degraded responses '
                                      'for requests requiring unavailable dependencies.',
                          'diagram': ('Database pool saturated',
                                      'Deep probe fails on all 60 VMs',
                                      'Load balancer drops 100% backends',
                                      'Shallow probe deployed (/shallow)',
                                      'Load balancer maintains healthy pool'),
                          'facts': 'All 60 catalog VMs were declared dead by the load balancer because `/healthz` '
                                   'queried the database during a transient lock.',
                          'inference': 'Deep health checks on load balancers transform transient downstream blips into '
                                       'catastrophic total compute evictions.',
                          'expected': 'Load balancer probes `/healthz/shallow`, keeping VMs in service while '
                                      'application circuit-breakers shed load gracefully.'},
             'lab': {'name': 'Application Health Check Architecture & Graceful Shutdown Rehearsal',
                     'file': 'day-089-topic-03-app-health.md',
                     'goal': 'Design an enterprise health check decision matrix and write a production-ready '
                             'Node.js/Go graceful shutdown implementation with probe separation.',
                     'expected': 'A comprehensive Markdown document containing the shallow-vs-deep decision matrix and '
                                 'executable code demonstrating SIGTERM handling.',
                     'mode': 'tabletop analysis & production CLI / Node.js execution',
                     'prereq': 'Understanding of HTTP semantics and container lifecycles.',
                     'preflight': 'Review Kubernetes probe concepts and load balancer draining parameters.',
                     'steps': ['#### Stage 1: Pre-Flight Health Probe Taxonomy & Invariant Architecture\n'
                               "Establish the health check and probe segregation invariants for Brightloaf's container "
                               'workloads:\n'
                               '- **Load Balancer Probes (`/healthz/shallow`):** Strictly shallow. Checks only local '
                               'HTTP listener responsiveness and memory sanity. Zero external network/database calls.\n'
                               '- **Kubernetes Readiness Probes (`/healthz/readiness`):** Controls traffic routing at '
                               'the Kubernetes Service level. Evicts pods from endpoints during local warming without '
                               'terminating processes.\n'
                               '- **Kubernetes Liveness Probes (`/healthz/liveness`):** Checks process event-loop '
                               'liveness. Initiates container restart only if the process is irrecoverably '
                               'deadlocked.\n'
                               '- **Synthetic Dependency Auditing (`/healthz/deep`):** Evaluates Cloud SQL, Redis, and '
                               'Pub/Sub availability for operational dashboards only. Decoupled completely from '
                               'automated traffic routing.',
                               '#### Stage 2: Environment Preflight & Runtime Specification\n'
                               'Author a preflight script (<kbd>check_app_health_env.py</kbd>) establishing probe '
                               'parameters:\n'
                               '\n'
                               '```python\n'
                               '# check_app_health_env.py\n'
                               'probe_specs = {\n'
                               "    'shallow': {'path': '/healthz/shallow', 'timeout_s': 2, 'db_check': False},\n"
                               "    'readiness': {'path': '/healthz/readiness', 'timeout_s': 3, 'db_check': False},\n"
                               "    'liveness': {'path': '/healthz/liveness', 'timeout_s': 3, 'db_check': False},\n"
                               "    'deep': {'path': '/healthz/deep', 'timeout_s': 5, 'db_check': True},\n"
                               '}\n'
                               "print('[PREFLIGHT] Validating health check isolation parameters...')\n"
                               "assert not probe_specs['shallow']['db_check'], 'Shallow probe must NEVER call "
                               "database'\n"
                               "assert not probe_specs['liveness']['db_check'], 'Liveness probe must NEVER call "
                               "database'\n"
                               "print('[PASS] Health probe isolation architecture verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight validation:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_app_health_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Production Graceful Shutdown Server\n'
                               'Author a production Node.js microservice (<kbd>server.js</kbd>) implementing '
                               'segregated probe endpoints and SIGTERM graceful draining:\n'
                               '\n'
                               '```javascript\n'
                               "cat <<'EOF' > server.js\n"
                               "const http = require('http');\n"
                               '\n'
                               'let isShuttingDown = false;\n'
                               'let activeConnections = 0;\n'
                               '\n'
                               'const server = http.createServer((req, res) => {\n'
                               '  // Health check routing\n'
                               "  if (req.url === '/healthz/shallow') {\n"
                               '    if (isShuttingDown) {\n'
                               "      res.writeHead(503, {'Content-Type': 'text/plain'});\n"
                               "      return res.end('DRAINING');\n"
                               '    }\n'
                               "    res.writeHead(200, {'Content-Type': 'text/plain'});\n"
                               "    return res.end('OK');\n"
                               '  }\n'
                               '\n'
                               "  if (req.url === '/healthz/readiness') {\n"
                               '    if (isShuttingDown) {\n'
                               "      res.writeHead(503, {'Content-Type': 'text/plain'});\n"
                               "      return res.end('NOT_READY');\n"
                               '    }\n'
                               "    res.writeHead(200, {'Content-Type': 'text/plain'});\n"
                               "    return res.end('READY');\n"
                               '  }\n'
                               '\n'
                               "  if (req.url === '/healthz/liveness') {\n"
                               "    res.writeHead(200, {'Content-Type': 'text/plain'});\n"
                               "    return res.end('ALIVE');\n"
                               '  }\n'
                               '\n'
                               "  if (req.url === '/healthz/deep') {\n"
                               '    // Synthetic dependency check (monitoring only)\n'
                               "    res.writeHead(200, {'Content-Type': 'application/json'});\n"
                               "    return res.end(JSON.stringify({database: 'OK', redis: 'OK', pubsub: 'OK'}));\n"
                               '  }\n'
                               '\n'
                               '  // Standard transaction handler\n'
                               '  activeConnections++;\n'
                               '  setTimeout(() => {\n'
                               '    activeConnections--;\n'
                               "    res.writeHead(200, {'Content-Type': 'text/plain'});\n"
                               "    res.end('TRANSACTION_COMPLETE');\n"
                               '  }, 200);\n'
                               '});\n'
                               '\n'
                               'function gracefulShutdown(signal) {\n'
                               '  console.log(`[SHUTDOWN] Received ${signal}. Starting 5s LB drain window...`);\n'
                               '  isShuttingDown = true; // Marks shallow & readiness as 503\n'
                               '\n'
                               '  setTimeout(() => {\n'
                               "    console.log('[SHUTDOWN] Closing server to new sockets; draining active "
                               "requests...');\n"
                               '    server.close(() => {\n'
                               '      console.log(`[SHUTDOWN] Drained all requests (active: ${activeConnections}). '
                               'Exiting cleanly.`);\n'
                               '      process.exit(0);\n'
                               '    });\n'
                               '  }, 2000);\n'
                               '}\n'
                               '\n'
                               "process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));\n"
                               "process.on('SIGINT', () => gracefulShutdown('SIGINT'));\n"
                               '\n'
                               "server.listen(8080, () => console.log('[STARTUP] Server listening on :8080'));\n"
                               'EOF\n'
                               'cat server.js\n'
                               '```',
                               '#### Stage 4: Execution & Kubernetes Pod Lifecycle Manifests\n'
                               'Author the Kubernetes Pod specification (<kbd>k8s-pod-probes.yaml</kbd>) aligning '
                               'probe intervals and `preStop` sleep:\n'
                               '\n'
                               '```yaml\n'
                               "cat <<'YAML' > k8s-pod-probes.yaml\n"
                               'apiVersion: apps/v1\n'
                               'kind: Deployment\n'
                               'metadata:\n'
                               '  name: catalog-service\n'
                               'spec:\n'
                               '  replicas: 4\n'
                               '  selector:\n'
                               '    matchLabels:\n'
                               '      app: catalog\n'
                               '  template:\n'
                               '    metadata:\n'
                               '      labels:\n'
                               '        app: catalog\n'
                               '    spec:\n'
                               '      terminationGracePeriodSeconds: 30\n'
                               '      containers:\n'
                               '      - name: catalog\n'
                               '        image: gcr.io/brightloaf-prod/catalog:v2\n'
                               '        ports:\n'
                               '        - containerPort: 8080\n'
                               '        lifecycle:\n'
                               '          preStop:\n'
                               '            exec:\n'
                               '              command: ["/bin/sh", "-c", "sleep 5"]\n'
                               '        readinessProbe:\n'
                               '          httpGet:\n'
                               '            path: /healthz/readiness\n'
                               '            port: 8080\n'
                               '          initialDelaySeconds: 2\n'
                               '          periodSeconds: 5\n'
                               '          failureThreshold: 2\n'
                               '        livenessProbe:\n'
                               '          httpGet:\n'
                               '            path: /healthz/liveness\n'
                               '            port: 8080\n'
                               '          initialDelaySeconds: 5\n'
                               '          periodSeconds: 10\n'
                               '          failureThreshold: 3\n'
                               'YAML\n'
                               'cat k8s-pod-probes.yaml\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Cascading Failure Simulation\n'
                               'Author a Python simulation script (<kbd>simulate_probes.py</kbd>) testing probe '
                               'behavior under simulated downstream database saturation:\n'
                               '\n'
                               '```python\n'
                               '# simulate_probes.py\n'
                               "print('--- SIMULATING DATABASE SATURATION SCENARIO ---')\n"
                               'db_connected = False  # Downstream database locks up\n'
                               '\n'
                               'def shallow_check():\n'
                               '    # Evaluates process responsiveness only\n'
                               "    return 200, 'OK'\n"
                               '\n'
                               'def deep_check():\n'
                               '    # Evaluates database connectivity\n'
                               '    if not db_connected:\n'
                               "        return 503, 'Database Connection Pool Exhausted'\n"
                               "    return 200, 'Healthy'\n"
                               '\n'
                               'code_shallow, body_shallow = shallow_check()\n'
                               'code_deep, body_deep = deep_check()\n'
                               '\n'
                               "print(f'[Load Balancer Probe] /healthz/shallow -> HTTP {code_shallow} "
                               "{body_shallow}')\n"
                               "print(f'[SRE Synthetic Probe] /healthz/deep    -> HTTP {code_deep} {body_deep}')\n"
                               '\n'
                               "assert code_shallow == 200, 'Load balancer probe must remain 200 OK during DB "
                               "degradation'\n"
                               "assert code_deep == 503, 'Synthetic deep probe must report 503 for monitoring'\n"
                               "print('[PASS] Probe segregation protects compute instances from cascading "
                               "evictions.')\n"
                               '```\n'
                               '\n'
                               'Execute simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_probes.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Draining Verification\n'
                               'Author a test verifying that during SIGTERM, the shallow probe immediately responds '
                               '503 while existing connections drain:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_drain_sequence.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Simulating SIGTERM signal propagation..."\n'
                               "cat <<'TRACE'\n"
                               'T+00s: kubelet sends SIGTERM to catalog container\n'
                               "T+00s: preStop hook executes 'sleep 5' (endpoints begin removing Pod IP)\n"
                               'T+05s: Application traps SIGTERM; sets isShuttingDown = true\n'
                               'T+05s: /healthz/shallow returns HTTP 503 (Cloud Load Balancer begins backend '
                               'draining)\n'
                               'T+07s: Server stops accepting new connections; in-flight requests complete (active: '
                               '0)\n'
                               'T+07s: server.close() completes; database pools closed cleanly\n'
                               'T+08s: Container process terminates with EXIT CODE 0 (Zero dropped user requests)\n'
                               'TRACE\n'
                               'echo "[DRAIN OBSERVABILITY PASS] Graceful shutdown lifecycle completed cleanly."\n'
                               'EOF\n'
                               'chmod +x verify_drain_sequence.sh\n'
                               './verify_drain_sequence.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Architectural Assertion\n'
                               'Author an automated verification script (<kbd>test_probe_architecture.py</kbd>) that '
                               'validates the manifest and probe contract:\n'
                               '\n'
                               '```python\n'
                               '# test_probe_architecture.py\n'
                               'import re\n'
                               '\n'
                               "with open('k8s-pod-probes.yaml', 'r') as f:\n"
                               '    content = f.read()\n'
                               '\n'
                               "assert '/healthz/readiness' in content, 'Manifest must declare readiness probe'\n"
                               "assert '/healthz/liveness' in content, 'Manifest must declare liveness probe'\n"
                               "assert 'terminationGracePeriodSeconds: 30' in content, 'Must specify 30s grace "
                               "period'\n"
                               "assert 'sleep 5' in content, 'PreStop hook must execute sleep before SIGTERM'\n"
                               "print('[ASSERT PASS] Kubernetes manifest strictly adheres to probe and drain "
                               "architecture.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_probe_architecture.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_app_health_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 89 Topic 3 test scripts..."\n'
                               'rm -f check_app_health_env.py server.js k8s-pod-probes.yaml simulate_probes.py '
                               'verify_drain_sequence.sh test_probe_architecture.py\n'
                               'echo "[CLEANUP] Retaining day-089-topic-03-app-health.md evidence documentation."\n'
                               'echo "[CLEANUP PASS] Application health teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_app_health_lab.sh\n'
                               './teardown_app_health_lab.sh\n'
                               '```'],
                     'verification': 'Document exists, contains a comprehensive health check decision matrix, and '
                                     'provides working graceful shutdown code.',
                     'trouble': 'Ensure `terminationGracePeriodSeconds` in Kubernetes exceeds the sum of `sleep 5` '
                                'preStop hook and the application drain timeout.',
                     'cleanup': 'Retain `day-089-topic-03-app-health.md` as an exit evidence artifact.',
                     'accept': 'Completed health check architectural matrix and validated graceful shutdown lifecycle '
                               'implementation.'}}],
 'part3_intro': 'The following field cases analyze real-world production catastrophes resulting from unhedged '
                'communication and routing control planes: unhandled poison pill payloads triggering infinite '
                'container crash loops in payment pipelines, DNS record changes trapped by rogue ISP recursive '
                'resolver TTL floors during emergency datacenter evacuations, and deep database health checks '
                'precipitating total load balancer eviction cascades. Each case details quantifiable failure metrics, '
                'verbatim terminal/log transcripts, diagnostic command sequences, root cause mechanics, defensible '
                'remediations, and dual-lane failed/corrected architectural diagrams.',
 'part4_intro': 'These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers configure '
                'enterprise Pub/Sub message storage boundaries with automated dead-letter queues and atomic '
                'deduplication gates, synthesize Cloud DNS health-checked failover policies accounting for recursive '
                'caching decay, and author production microservices implementing strict shallow-versus-deep probe '
                'decoupling with SIGTERM connection draining.'}
