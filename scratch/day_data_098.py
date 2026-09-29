"""day_data_098.py — Exhaustive architecture data specification for Day 98.

Covers Recovery Acceptance, Invariants, and Representative Recovery Paths.
"""

DAY_NUM = 98

DATA = {'day': 98,
 'part1_intro': 'Day 98 establishes the rigorous operational and mathematical acceptance gates required before '
                'declaring a database restore or disaster recovery failover successful. In enterprise systems, '
                'completing a database restore command is merely the initial step; production traffic must never be '
                'released until data integrity invariants, replication parity, and application connection health are '
                "empirically verified. Today's curriculum builds a comprehensive Disaster Recovery Acceptance "
                'Framework: validating transaction consistency, measuring observed RTO and RPO against contractual '
                'SLAs, comparing Cloud SQL Regional HA with Cross-Region Replica Promotion, and executing automated '
                'post-failover acceptance tests defending the core single-fulfillment business invariant.',
 'exit_summary': 'Executed an enterprise Database Restore and Failover Acceptance drill: measured empirical recovery '
                 'duration (RTO = 84s) and data loss (RPO = 0s); authored and verified an executable failover runbook '
                 'comparing Cloud SQL Regional HA against Cross-Region Promotion; validated mathematical ledger '
                 'balance conservation and the single-fulfillment invariant with explicit distinctions between lab '
                 'metrics and production enterprise boundaries.',
 'part2_intro': 'Disaster recovery acceptance bridges infrastructure automation with application correctness. The '
                'sections below analyze acceptance test mechanics, invariant verification math, and the technical '
                'trade-offs distinguishing synchronous Regional HA from asynchronous cross-region promotion.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Recovery Architecture / Topology</th>\n'
                    '      <th>Replication Mechanics &amp; Protocol</th>\n'
                    '      <th>Measured RPO (Data Loss)</th>\n'
                    '      <th>Measured RTO (Recovery Time)</th>\n'
                    '      <th>Failover Trigger &amp; Operational Trade-off</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>Cloud SQL Regional HA</strong></td>\n'
                    '      <td>Synchronous block-level replication via Regional Persistent Disk across 2 zones</td>\n'
                    '      <td><strong>RPO = 0</strong> (Zero committed transaction loss)</td>\n'
                    '      <td><strong>RTO = 60–120s</strong> (Automated failover &amp; crash recovery replay)</td>\n'
                    '      <td>Fully automated via Google Cloud control plane; protects against single-zone outage; '
                    'identical regional pricing premium</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Cross-Region Read Replica Promotion</strong></td>\n'
                    '      <td>Asynchronous database replication (PostgreSQL streaming / MySQL binary logs)</td>\n'
                    '      <td><strong>RPO = Seconds to Minutes</strong> (Proportional to network byte lag)</td>\n'
                    '      <td><strong>RTO = 5–15 minutes</strong> (Manual or semi-automated promote command + DNS '
                    'cutover)</td>\n'
                    '      <td>Manual or scripted decision; protects against total multi-zone regional catastrophe; '
                    'requires reverse-replication rebuild to fail back</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Point-in-Time Recovery (PITR Backup)</strong></td>\n'
                    '      <td>Full daily snapshot base backup + continuous Write-Ahead Log (WAL) archive</td>\n'
                    '      <td><strong>RPO &lt; 5 minutes</strong> (To the specific second prior to corruption)</td>\n'
                    '      <td><strong>RTO = 30–90 minutes</strong> (Provision new instance + restore storage + replay '
                    'WAL)</td>\n'
                    '      <td>Human-authorized disaster response; used for accidental table drop, ransomware, or '
                    'schema corruption; provisions a new instance IP</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 98: Disaster Recovery Acceptance, Data Invariants, and Replica Promotion',
                  'desc': 'Architectural topology showing database replication, automated replica promotion, DNS/PSC '
                          'endpoint failover, and cryptographic invariant verification.',
                  'caption': 'Figure 98.1: Multi-region database disaster recovery architecture with Cloud SQL '
                             'cross-region promotion, automated endpoint redirection, and invariant acceptance '
                             'auditing.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Client Application Traffic & Connection Routing',
                              'desc': 'Application pods, connection pool management, and Cloud SQL Auth Proxy',
                              'y': 10,
                              'h': 90,
                              'stroke': '#38bdf8',
                              'fill': '#0c1e38',
                              'title_color': '#38bdf8'},
                             {'name': 'LAYER 2: Primary Database & Asynchronous WAL Replication',
                              'desc': 'Cloud SQL Primary in us-central1 with binary logging and continuous replication',
                              'y': 115,
                              'h': 90,
                              'stroke': '#818cf8',
                              'fill': '#141838',
                              'title_color': '#818cf8'},
                             {'name': 'LAYER 3: Cross-Region Standby Replica & Backup Snapshot Fabric',
                              'desc': 'Cross-region read replica in us-east1 and automated PITR storage',
                              'y': 220,
                              'h': 90,
                              'stroke': '#f59e0b',
                              'fill': '#261a08',
                              'title_color': '#f59e0b'},
                             {'name': 'LAYER 4: Automated Failover & Replica Promotion Controller',
                              'desc': 'gcloud replica promotion orchestrator, DNS failover, and PSC endpoint switch',
                              'y': 325,
                              'h': 90,
                              'stroke': '#f43f5e',
                              'fill': '#2a0a14',
                              'title_color': '#f43f5e'},
                             {'name': 'LAYER 5: SRE Invariant Verification, RTO/RPO & Recovery Acceptance',
                              'desc': 'Cryptographic row hashing, ledger reconciliation, and formal acceptance report',
                              'y': 430,
                              'h': 90,
                              'stroke': '#22c55e',
                              'fill': '#072417',
                              'title_color': '#22c55e'}],
                  'components': [{'name': 'App Connection Pool',
                                  'detail': 'HikariCP Dynamic DNS',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'Cloud SQL Auth Proxy',
                                  'detail': 'Encrypted TCP Sidecar',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#38bdf8',
                                  'fill': '#0e294b'},
                                 {'name': 'Primary DB (us-central1)',
                                  'detail': 'HA Cloud SQL Master',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'WAL Binlog Stream',
                                  'detail': 'Cross-Region Streaming',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#818cf8',
                                  'fill': '#191c4d'},
                                 {'name': 'Replica (us-east1)',
                                  'detail': 'Synchronized Read Node',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Automated Backups',
                                  'detail': '7-Day Point-in-Time Logs',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f59e0b',
                                  'fill': '#38230a'},
                                 {'name': 'Promotion Orchestrator',
                                  'detail': 'Promote to Standalone Master',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'PSC / DNS Endpoint Switch',
                                  'detail': 'Private DNS CNAME Update',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#f43f5e',
                                  'fill': '#3d101d'},
                                 {'name': 'Invariant Check Suite',
                                  'detail': 'Ledger Balance & Row Hashes',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'},
                                 {'name': 'Recovery Acceptance Sign-Off',
                                  'detail': 'RTO < 90s, RPO < 5s Proof',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'stroke': '#22c55e',
                                  'fill': '#0b3824'}],
                  'boundaries': [{'label': 'CLIENT APPLICATION & PROXY ROUTING PERIMETER',
                                  'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'color': '#38bdf8'},
                                 {'label': 'REGIONAL REPLICATION & RECOVERY FABRIC',
                                  'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#818cf8'},
                                 {'label': 'PROMOTION ORCHESTRATION & INVARIANT AUDIT VAULT',
                                  'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'color': '#22c55e'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Forward Connection', 'type': 'ok'},
                            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Route SQL to Primary', 'type': 'ok'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'label': 'Stream WAL Binary Log',
                             'type': 'ok'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'label': 'Apply to East Replica',
                             'type': 'ok'},
                            {'x1': 340,
                             'y1': 266,
                             'x2': 420,
                             'y2': 266,
                             'label': 'Primary Region Outage',
                             'type': 'fail'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'label': 'Execute Replica Promotion',
                             'type': 'ok'},
                            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Update DNS Target', 'type': 'ok'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'label': 'Verify Data Invariants',
                             'type': 'ok'},
                            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Sign Off Acceptance', 'type': 'ok'}],
                  'probes': [{'cx': 420,
                              'cy': 135,
                              'label': 'PROBE 1: Replication Lag Delta (<1.2s)',
                              'badge': 'P1',
                              'color': '#38bdf8'},
                             {'cx': 80,
                              'cy': 345,
                              'label': 'PROBE 2: Promotion Execution Time (<90s)',
                              'badge': 'P2',
                              'color': '#f59e0b'},
                             {'cx': 80,
                              'cy': 450,
                              'label': 'PROBE 3: Invariant Ledger Balance Assert (Net Zero)',
                              'badge': 'P3',
                              'color': '#22c55e'}]},
 'topics': [{'key': 'topic-01',
             'title': 'Recovery Acceptance Criteria After Backup Restore or Replica Promotion',
             'overview': 'Declaring a database recovered requires satisfying explicit, objective acceptance criteria '
                         'spanning network, security, and data layers. Too often, teams celebrate when a backup '
                         'restore or replica promotion operation completes successfully in the CLI, only to direct '
                         'user traffic to an instance that lacks necessary IAM service account bindings, has outdated '
                         'read-only parameters, or contains corrupted foreign key indexes. An enterprise acceptance '
                         'checklist enforces sequential verification gates before read-write connection pools are '
                         're-opened to client traffic.',
             'preview': 'A promoted read replica accepts traffic while still configured in read-only transaction mode, '
                        'causing all customer checkout writes to fail. Pre-traffic recovery acceptance gates verify '
                        'read-write status and connection pool reconnection before opening application ingress.',
             'technical': '### 1. The Four-Stage Recovery Acceptance Pipeline\n'
                          '- **Stage 1: Infrastructure Readiness Gate:**\n'
                          '  - Verify database instance status is `RUNNABLE` via the instance describe API.\n'
                          '  - Confirm Private Service Access (PSA) VPC peering IP address is reachable from '
                          'application subnets.\n'
                          '  - Verify SSL/TLS certificates and Cloud SQL Auth Proxy client authorization tokens.\n'
                          '- **Stage 2: Engine Configuration & Mode Gate:**\n'
                          '  - In promoted replicas, assert the database engine has disabled standby mode: `SHOW '
                          'transaction_read_only;` must return `off`.\n'
                          '  - Check `max_connections`, `shared_buffers`, and active connection headroom.\n'
                          '- **Stage 3: Application Health Gate:**\n'
                          '  - Execute lightweight diagnostic query: `SELECT 1;`.\n'
                          '  - Test connection pool draining and recycling: ensure application pods re-establish live '
                          'sockets without stale connection errors.\n'
                          '- **Stage 4: Post-Restore Binary Log & Replication Stream Gate:**\n'
                          '  - If promoted to primary, ensure automated backups and point-in-time recovery (WAL '
                          'archiving) are re-enabled immediately.\n'
                          '  - A newly promoted primary is un-backed-up until a fresh base snapshot completes; running '
                          'without backups creates severe residual risk.',
             'questions': ['Why must a promoted replica immediately have automated backups and WAL archiving '
                           're-enabled before opening production write traffic?',
                           'What hidden configuration states (such as `transaction_read_only = on`) can cause a '
                           'promoted replica to reject application writes?',
                           'How does the Cloud SQL Auth Proxy handle automatic connection recovery when a primary '
                           'instance changes IP addresses during failover?'],
             'reference': 'https://docs.cloud.google.com/sql/docs/postgres/high-availability',
             'reference_label': 'Google Cloud SQL: High availability configuration and post-failover recovery '
                                'mechanics',
             'scenario': {'symptom': 'Following an emergency cross-region replica promotion during a regional outage, '
                                     'all Brightloaf customer checkout transactions threw HTTP 500 errors with '
                                     'database exception: `ERROR: cannot execute INSERT in a read-only transaction`.',
                          'constraints': 'Must automate post-promotion acceptance checks so that transaction '
                                         'read-write mode is verified before application pods switch database '
                                         'endpoints.',
                          'evidence': 'Production database error log following replica promotion:\n'
                                      '\n'
                                      '```text\n'
                                      "2026-09-29T12:04:12Z [INFO] Cloud SQL: Instance 'prod-db-east1' promoted to "
                                      'master successfully.\n'
                                      '2026-09-29T12:04:30Z [DBA] Verified manual query: SELECT 1; -> SUCCESS. Marked '
                                      'recovery complete.\n'
                                      '2026-09-29T12:05:10Z [CRITICAL] App Engine API: Connection refused: '
                                      '10.128.0.5:5432 (old central1 master IP)\n'
                                      '2026-09-29T12:06:00Z [CRITICAL] 503 Service Unavailable spike: 100% of customer '
                                      'checkouts failing\n'
                                      '```\n'
                                      '\n'
                                      'App deployment analysis: Hardcoded static IP `10.128.0.5` in Kubernetes '
                                      'ConfigMap instead of Private DNS name `db.prod.internal`.',
                          'diagnostic_steps': ['Execute direct psql query against promoted instance: `SELECT '
                                               'pg_is_in_recovery();`.',
                                               'Inspect application pod datasource configuration and environment '
                                               'variable overrides.',
                                               'Review application error logs in Logs Explorer for specific database '
                                               'SQL state codes (`25006`).'],
                          'root': 'Unverified application datasource binding: the database had promoted correctly to '
                                  'primary, but the application connection pool was configured with read-only session '
                                  'flags, rejecting all insert operations.',
                          'fix': 'Incorporate an automated pre-flight acceptance probe in the deployment script that '
                                 "executes a transactional insert/delete test using the application's primary "
                                 'datasource credentials before updating Cloud DNS or Kubernetes service selectors.',
                          'verify': 'Run automated acceptance probe script; confirm it executes a canary write '
                                    'transaction, verifies `pg_is_in_recovery() = false`, and returns exit code 0 '
                                    'before traffic shifting occurs.',
                          'residual': 'Cross-region promotion breaks the original replication link; a new replica must '
                                      'be provisioned in the primary region to re-establish HA.',
                          'diagram': ('East replica promoted to standalone master',
                                      'App pods configured with static central IP',
                                      'Apps fail to connect -> 100% outage persists',
                                      'Use Private DNS CNAME and automated write probe',
                                      'DNS switches in 30s; apps resume transactions')},
             'lab': {'name': 'Database Recovery Acceptance Probe and Pre-Traffic Verification Script',
                     'goal': 'Author an automated Python acceptance verification runner that validates database '
                             'readiness, read-write state, and connection pool health.',
                     'expected': 'An executable Python script executing the 4 recovery acceptance stages and '
                                 'outputting a structured acceptance certificate.',
                     'mode': 'local script execution',
                     'prereq': 'Understanding of relational database transactions and failover mechanics.',
                     'preflight': 'Ensure Python 3 standard library is present; no external packages needed.',
                     'steps': ['#### Stage 1: Pre-Flight Database Endpoint & Connection Inventory\n'
                               'Inspect application database connection string configuration to ensure dynamic DNS '
                               'endpoint usage:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_db_endpoints.py\n"
                               'db_config = {\n'
                               "    'endpoint_type': 'PRIVATE_DNS_CNAME',\n"
                               "    'dns_name': 'db.prod.gcp.internal',\n"
                               "    'primary_ip': '10.128.0.5',\n"
                               "    'replica_ip': '10.142.0.8',\n"
                               "    'max_connection_lifetime_sec': 60 # Forces DNS re-resolution\n"
                               '}\n'
                               "print('[PREFLIGHT] Auditing database connection pool settings:')\n"
                               'for k, v in db_config.items():\n'
                               "    print(f'  • {k}: {v}')\n"
                               "assert db_config['endpoint_type'] == 'PRIVATE_DNS_CNAME', 'Static IP violates DR "
                               "recovery standards!'\n"
                               'EOF\n'
                               'python3 check_db_endpoints.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Replica Health Inspection\n'
                               'Verify cross-region read replica replication lag before initiating promotion:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_replica_status.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Verifying database CLI tooling..."\n'
                               'python3 -c "import time; print(\'[PASS] Python timing engine ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_replica_status.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Automated Recovery Acceptance Suite\n'
                               'Author a Python test suite that validates read/write capabilities, sequence '
                               'increments, and table locks on a promoted instance:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > recovery_acceptance_suite.py\n"
                               'import time\n'
                               '\n'
                               'class PromotedDatabaseAcceptance:\n'
                               '    def __init__(self, host, is_read_only=False):\n'
                               '        self.host = host\n'
                               '        self.is_read_only = is_read_only\n'
                               '\n'
                               '    def run_acceptance_checks(self):\n'
                               "        print(f'[ACCEPTANCE] Running battery on {self.host}...')\n"
                               '        # Check 1: Liveness ping\n'
                               "        print('  • Step 1: Liveness ping (SELECT 1) -> PASS')\n"
                               '        # Check 2: Read-write verification\n'
                               '        if self.is_read_only:\n'
                               "            raise PermissionError('FAIL: Instance is still read-only replica!')\n"
                               "        print('  • Step 2: DML Write test (INSERT INTO canary_heartbeat) -> PASS')\n"
                               '        # Check 3: Sequence increment\n'
                               "        print('  • Step 3: Sequence increment verification -> PASS')\n"
                               '        # Check 4: Connection drain check\n'
                               "        print('  • Step 4: Active connection pool capacity -> PASS')\n"
                               '        return True\n'
                               '\n'
                               "if __name__ == '__main__':\n"
                               "    suite = PromotedDatabaseAcceptance('db-east1-promoted.internal', "
                               'is_read_only=False)\n'
                               '    assert suite.run_acceptance_checks()\n'
                               "    print('[PASS] Database recovery acceptance criteria 100% satisfied.')\n"
                               'EOF\n'
                               'python3 recovery_acceptance_suite.py\n'
                               '```',
                               '#### Stage 4: Execution & DNS Switch Simulation\n'
                               'Author a script simulating DNS CNAME update pointing to the promoted instance:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_dns_failover.py\n"
                               'import time\n'
                               '\n'
                               "dns_zones = {'db.prod.gcp.internal': '10.128.0.5'} # Primary\n"
                               "print(f'[DNS STATUS] Current A Record: db.prod.gcp.internal -> "
                               '{dns_zones["db.prod.gcp.internal"]}\')\n'
                               '\n'
                               '# Perform failover switch\n'
                               "print('[FAILOVER] Updating Cloud DNS record to promoted replica...')\n"
                               "dns_zones['db.prod.gcp.internal'] = '10.142.0.8' # East replica\n"
                               'time.sleep(0.2)\n'
                               "print(f'[DNS STATUS] Updated A Record: db.prod.gcp.internal -> "
                               '{dns_zones["db.prod.gcp.internal"]}\')\n'
                               "assert dns_zones['db.prod.gcp.internal'] == '10.142.0.8'\n"
                               "print('[DNS PASS] Dynamic routing successfully shifted to promoted database.')\n"
                               'EOF\n'
                               'python3 simulate_dns_failover.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Premature Promotion Guard Chaos Test\n'
                               'Simulate an attempted promotion of a replica with active read-only flag and assert '
                               'acceptance failure:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_read_only_rejection.py\n"
                               'from recovery_acceptance_suite import PromotedDatabaseAcceptance\n'
                               '\n'
                               'try:\n'
                               "    bad_suite = PromotedDatabaseAcceptance('unpromoted-replica.internal', "
                               'is_read_only=True)\n'
                               '    bad_suite.run_acceptance_checks()\n'
                               "    raise AssertionError('Acceptance suite failed to reject read-only replica!')\n"
                               'except PermissionError as e:\n'
                               "    print(f'[CHAOS TEST PASS] Acceptance suite correctly blocked unpromoted node: "
                               "{e}')\n"
                               'EOF\n'
                               'python3 test_read_only_rejection.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Cloud Monitoring Failover Metric\n'
                               'Author a Cloud Monitoring Alert Policy tracking database write latency after '
                               'promotion:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_db_write_latency.json\n"
                               '{\n'
                               '  "displayName": "ALERT: Post-Promotion DB Write Latency Spike",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "Cloud SQL write query latency > 500ms",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": '
                               '"metric.type=\\"cloudsql.googleapis.com/database/postgresql/transaction_lock_wait_time\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 500.0,\n'
                               '        "duration": "60s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] Authored alert_db_write_latency.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Promotion Criteria Assertions\n'
                               'Execute automated test validating recovery acceptance certificate generation:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_recovery_certificate.py\n"
                               "with open('recovery_acceptance_suite.py') as f:\n"
                               '    code = f.read()\n'
                               '\n'
                               "assert 'SELECT 1' in code\n"
                               "assert 'canary_heartbeat' in code\n"
                               "assert 'is_read_only' in code\n"
                               "print('[ASSERT PASS] Recovery acceptance battery criteria strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_recovery_certificate.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary verification manifests:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_acceptance_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 98 Topic 1 test scripts..."\n'
                               'rm -f check_db_endpoints.py check_replica_status.sh recovery_acceptance_suite.py '
                               'simulate_dns_failover.py test_read_only_rejection.py assert_recovery_certificate.py\n'
                               'echo "[CLEANUP] Retaining alert policy: alert_db_write_latency.json"\n'
                               'echo "[CLEANUP PASS] Recovery acceptance lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_acceptance_lab.sh\n'
                               '```'],
                     'verification': 'The Python acceptance engine verifies recovery mode, read-write status, '
                                     'connection headroom, and canary transaction execution before certifying '
                                     'readiness.',
                     'trouble': 'Ensure canary transaction cleans up its temporary test rows so no synthetic probe '
                                'artifacts remain in production schemas.',
                     'cleanup': 'Retain `verify_recovery_acceptance.py` as an exit evidence artifact.',
                     'accept': 'Completed database recovery acceptance probe and verified execution certificate. File: '
                               '`day-098-topic-01-recovery-acceptance.md`.',
                     'file': 'day-098-topic-01-recovery-acceptance.md'}},
            {'key': 'topic-02',
             'title': 'Verifying Data Invariants, Recovery Time (RTO), and Data Loss (RPO)',
             'overview': 'After a database restore or failover, infrastructure metrics measure duration and connection '
                         'counts, but only application-level data invariants prove whether data corruption or '
                         'transaction loss occurred. A business invariant is an immutable truth that must hold across '
                         'all operational states: in banking, total debits must equal total credits; in e-commerce, '
                         'every paid order must be fulfilled exactly once and inventory count plus items sold must '
                         'equal total initial stock. Verifying these invariants against post-restore data provides '
                         'empirical proof of actual Recovery Point Objective (RPO) and confirms zero customer '
                         'financial harm.',
             'preview': 'A database restore finishes in 10 minutes, but 45 in-flight payment records lack '
                        'corresponding fulfillment entries. Running post-restore invariant reconciliation scripts '
                        'isolates unfulfilled transactions and measures actual data loss.',
             'technical': '### 1. Mathematical Definitions of RTO and RPO\n'
                          '- **Recovery Time Objective (RTO):** The maximum tolerable elapsed time between the '
                          'declaration of disaster and the full restoration of production read-write capability: '
                          '$\\text{RTO} = T_{\\text{restored}} - T_{\\text{disaster}}$.\n'
                          '- **Recovery Point Objective (RPO):** The maximum acceptable data loss measured in time '
                          'backward from the disaster event: $\\text{RPO} = T_{\\text{disaster}} - '
                          'T_{\\text{last\\_committed\\_data\\_preserved}}$.\n'
                          '\n'
                          '### 2. Core Business Invariant Verification\n'
                          '- **Invariant 1: Conservation of Account Balances:**\n'
                          '  $$\\sum \\text{Customer Balances} + \\sum \\text{Pending Escrow} = \\text{Total Ledger '
                          'Cash}$$\n'
                          '- **Invariant 2: Strict Single Fulfillment:**\n'
                          '  $$\\forall \\text{order} \\in \\text{Orders}: '
                          '\\text{count}(\\text{fulfillments}(\\text{order})) = 1 \\iff \\text{order.status} = '
                          "\\text{'PAID'}$$\n"
                          '  Every paid order must have exactly one warehouse dispatch record; zero paid orders may '
                          'have duplicate or zero dispatches.\n'
                          '- **Invariant 3: Inventory Stock Parity:**\n'
                          '  $$\\text{Current Stock} + \\sum \\text{Shipped Quantities} = \\text{Initial Stock}$$\n'
                          '\n'
                          '### 3. Auditing Alerting Behavior During Failover\n'
                          '- When a database fails over, dozens of downstream microservices experience temporary '
                          'connection pool drops.\n'
                          '- **Alert Fatigue Prevention:** SLO burn-rate alerts must distinguish between an acute '
                          '60-second failover window (which burns a minor fraction of the 30-day error budget) and an '
                          'unrecovered, catastrophic total outage. If the failover completes within the contractual '
                          'RTO (e.g. <120s), incident managers should receive informational updates while on-call '
                          'escalation pages are held until RTO thresholds are breached.',
             'questions': ['What is the mathematical difference between infrastructure restoration time (RTO) and '
                           'transactional data loss (RPO)?',
                           'How does verifying application-level data invariants prove data consistency beyond '
                           'low-level database page checksums?',
                           'Why should alert policies incorporate grace periods matching the expected database HA '
                           'failover duration?'],
             'reference': 'https://sre.google/sre-book/data-integrity/',
             'reference_label': 'Google Site Reliability Engineering: Data integrity, verification, and recovery '
                                'principles',
             'scenario': {'symptom': 'Following an unexpected Cloud SQL zonal failover, warehouse dispatch operators '
                                     'reported that 28 orders placed immediately prior to the failover were dispatched '
                                     'twice, while 14 customer credit cards were charged without an order record being '
                                     'created.',
                          'constraints': 'Must establish an automated invariant verification script that reconciles '
                                         'payment gateway ledgers against database order records immediately '
                                         'post-failover.',
                          'evidence': 'Post-restore reconciliation audit log:\n'
                                      '\n'
                                      '```text\n'
                                      '2026-09-29T14:15:00Z [AUDIT] Running ledger integrity checksum query...\n'
                                      'Ledger sum: credits = $14,921,800.00 | debits = $14,918,400.00\n'
                                      'VARIANCE DETECTED: -$3,400.00 discrepancy across 14 transactions!\n'
                                      'Root cause: PITR restore timestamp set to 14:00:00 UTC, cutting off in-flight '
                                      'transactions committed at 14:00:02 UTC.\n'
                                      '```',
                          'diagnostic_steps': ['Query the database for orphan payment tokens lacking corresponding '
                                               'order IDs.',
                                               'Audit warehouse dispatch records grouped by `order_id` to identify '
                                               'duplicate entries.',
                                               'Reconcile payment gateway settlement reports against database ledger '
                                               'tables.'],
                          'root': 'Non-atomic transactional boundaries: decoupled database writes without cross-table '
                                  'atomic locks allowed transient failover disconnects to corrupt business state '
                                  'consistency.',
                          'fix': 'Enclose order creation, inventory deduction, and payment capture inside an atomic '
                                 'database transaction. Implement post-failover invariant verification scripts that '
                                 'audit data integrity before opening ingress.',
                          'verify': 'Trigger a simulated failover; execute the invariant reconciliation script; '
                                    'confirm 100% of orders satisfy the single-fulfillment invariant with zero '
                                    'duplicate dispatches and zero orphan charges.',
                          'residual': 'External third-party payment gateways operate outside the local database ACID '
                                      'boundary; distributed two-phase commit or transactional outbox patterns are '
                                      'required.',
                          'diagram': ('PITR restore executed to approximate time',
                                      'In-flight commits truncated by 2 seconds',
                                      '$3,400 balance discrepancy in general ledger',
                                      'Verify cryptographic row-hash invariants before traffic cutover',
                                      'Discrepancy caught and reconciled with zero financial loss')},
             'lab': {'name': 'Data Invariant Reconciliation Engine and RTO/RPO Measurement Script',
                     'goal': 'Author an executable Python script calculating empirical RTO and RPO and verifying the '
                             'single-fulfillment business invariant across a simulated failover.',
                     'expected': 'A runnable Python script executing invariant mathematical audits and outputting an '
                                 'RTO/RPO measurement certificate.',
                     'mode': 'local script execution',
                     'prereq': 'Understanding of business invariants, data integrity, and RTO/RPO calculations.',
                     'preflight': 'Ensure Python 3 standard library is present; no external packages required.',
                     'steps': ['#### Stage 1: Pre-Flight Financial Invariant & Cryptographic Hash Discovery\n'
                               'Catalog core business data invariants that must remain balanced across disaster '
                               'recovery events:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > catalog_invariants.py\n"
                               'invariants = {\n'
                               "    'ledger_net_balance': 'sum(debits) - sum(credits) == 0.00',\n"
                               "    'customer_balance_checksum': 'sum(account.balance) == sum(ledger.net)',\n"
                               "    'foreign_key_orphans': 'count(orders without valid user_id) == 0'\n"
                               '}\n'
                               "print('[PREFLIGHT] Required Data Invariants for Recovery Certification:')\n"
                               'for k, v in invariants.items():\n'
                               "    print(f'  • {k}: {v}')\n"
                               'EOF\n'
                               'python3 catalog_invariants.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Checksum Engine Verification\n'
                               'Verify SHA-256 cryptographic hashing capabilities in local environment:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_hash_engine.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Verifying cryptographic hashing toolset..."\n'
                               'python3 -c "import hashlib; print(\'[PASS] hashlib SHA-256 ready.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_hash_engine.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Cryptographic Data Invariant Engine\n'
                               'Author a Python verification engine calculating cryptographic row-level hash chains '
                               'and ledger balance assertions:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > data_invariant_verifier.py\n"
                               'import hashlib\n'
                               '\n'
                               'def compute_table_hash(rows):\n'
                               '    """Compute deterministic merkle hash of database rows."""\n'
                               '    hasher = hashlib.sha256()\n'
                               "    for row in sorted(rows, key=lambda x: x['id']):\n"
                               '        line = f"{row[\'id\']}:{row[\'debit\']}:{row[\'credit\']}\\n"\n'
                               "        hasher.update(line.encode('utf-8'))\n"
                               '    return hasher.hexdigest()\n'
                               '\n'
                               'def verify_ledger_invariants(rows):\n'
                               "    total_debits = sum(r['debit'] for r in rows)\n"
                               "    total_credits = sum(r['credit'] for r in rows)\n"
                               '    variance = total_debits - total_credits\n'
                               '    return variance == 0.0, variance\n'
                               '\n'
                               "if __name__ == '__main__':\n"
                               '    sample_ledger = [\n'
                               "        {'id': 1, 'debit': 100.0, 'credit': 0.0},\n"
                               "        {'id': 2, 'debit': 0.0, 'credit': 100.0},\n"
                               "        {'id': 3, 'debit': 250.50, 'credit': 250.50}\n"
                               '    ]\n'
                               '    balanced, var = verify_ledger_invariants(sample_ledger)\n'
                               "    assert balanced, f'Ledger imbalance: {var}'\n"
                               '    thash = compute_table_hash(sample_ledger)\n'
                               "    print(f'[INVARIANT PASS] Ledger balanced (Variance: ${var:.2f}). Table Hash: "
                               "{thash[:16]}...')\n"
                               'EOF\n'
                               'python3 data_invariant_verifier.py\n'
                               '```',
                               '#### Stage 4: Execution & RTO/RPO Timeline Verification\n'
                               'Simulate an outage recovery timeline calculating actual RTO and RPO against target '
                               'SLA:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > evaluate_rto_rpo.py\n"
                               "sla_targets = {'max_rto_sec': 120, 'max_rpo_sec': 5}\n"
                               '\n'
                               '# Simulated recovery metrics\n'
                               'recovery_metrics = {\n'
                               "    'outage_detected_ts': 1700000000,\n"
                               "    'failover_completed_ts': 1700000085, # 85s RTO\n"
                               "    'last_committed_tx_ts': 1700000000,\n"
                               "    'last_recovered_tx_ts': 1700000000  # 0s RPO (zero loss)\n"
                               '}\n'
                               '\n'
                               "actual_rto = recovery_metrics['failover_completed_ts'] - "
                               "recovery_metrics['outage_detected_ts']\n"
                               "actual_rpo = recovery_metrics['last_committed_tx_ts'] - "
                               "recovery_metrics['last_recovered_tx_ts']\n"
                               '\n'
                               "print(f'[METRICS EVAL] Actual RTO: {actual_rto}s (SLA Target: "
                               '{sla_targets["max_rto_sec"]}s) -> PASS\')\n'
                               "print(f'[METRICS EVAL] Actual RPO: {actual_rpo}s (SLA Target: "
                               '{sla_targets["max_rpo_sec"]}s) -> PASS\')\n'
                               "assert actual_rto <= sla_targets['max_rto_sec']\n"
                               "assert actual_rpo <= sla_targets['max_rpo_sec']\n"
                               'EOF\n'
                               'python3 evaluate_rto_rpo.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Corruption Intercept Chaos Test\n'
                               'Inject artificial variance into financial transactions and assert that the invariant '
                               'engine catches the discrepancy:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_variance_detection.py\n"
                               'from data_invariant_verifier import verify_ledger_invariants\n'
                               '\n'
                               'corrupted_ledger = [\n'
                               "    {'id': 1, 'debit': 100.0, 'credit': 0.0},\n"
                               "    {'id': 2, 'debit': 0.0, 'credit': 95.0} # $5 missing!\n"
                               ']\n'
                               'balanced, var = verify_ledger_invariants(corrupted_ledger)\n'
                               "assert not balanced, 'Failed to detect corrupted ledger transaction!'\n"
                               "print(f'[CHAOS TEST PASS] Invariant engine intercepted ledger discrepancy: ${var:.2f} "
                               "delta.')\n"
                               'EOF\n'
                               'python3 test_variance_detection.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Invariant Alerting Manifest\n'
                               'Author a Cloud Monitoring Alert Policy alerting whenever invariant audit jobs report '
                               'variance:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > alert_data_invariants.json\n"
                               '{\n'
                               '  "displayName": "CRITICAL: Data Invariant Variance Detected",\n'
                               '  "combiner": "OR",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "Ledger balance discrepancy count > 0",\n'
                               '      "conditionThreshold": {\n'
                               '        "filter": "metric.type=\\"custom.googleapis.com/dr/invariant_variance\\"",\n'
                               '        "comparison": "COMPARISON_GT",\n'
                               '        "thresholdValue": 0.0,\n'
                               '        "duration": "0s",\n'
                               '        "trigger": {"count": 1}\n'
                               '      }\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'echo "[OBSERVABILITY] Authored alert_data_invariants.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Checksum Invariant Assertions\n'
                               'Execute automated test validating cryptographic determinism:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_checksum_determinism.py\n"
                               'from data_invariant_verifier import compute_table_hash\n'
                               '\n'
                               "data1 = [{'id': 1, 'debit': 50.0, 'credit': 50.0}]\n"
                               "data2 = [{'id': 1, 'debit': 50.0, 'credit': 50.0}]\n"
                               'assert compute_table_hash(data1) == compute_table_hash(data2)\n'
                               "print('[ASSERT PASS] Cryptographic invariant hashing is strictly deterministic.')\n"
                               'EOF\n'
                               'python3 assert_checksum_determinism.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary invariant audit tools:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_invariants_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 98 Topic 2 test scripts..."\n'
                               'rm -f catalog_invariants.py check_hash_engine.sh data_invariant_verifier.py '
                               'evaluate_rto_rpo.py test_variance_detection.py assert_checksum_determinism.py\n'
                               'echo "[CLEANUP] Retaining alert policy: alert_data_invariants.json"\n'
                               'echo "[CLEANUP PASS] Invariants lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_invariants_lab.sh\n'
                               '```'],
                     'verification': 'The Python script calculates exact RTO and RPO metrics, confirms invariant '
                                     'compliance, and the report clearly delineates lab observations from production '
                                     'scale.',
                     'trouble': 'Ensure `last_committed_epoch` accurately reflects the timestamp of the latest '
                                'persistent transaction to prevent artificial RPO calculations.',
                     'cleanup': 'Retain `audit_data_invariants.py` and `day-098-topic-02-rto-rpo-report.md` as exit '
                                'evidence artifacts.',
                     'accept': 'Completed invariant audit script and verified RTO/RPO report. File: '
                               '`day-098-topic-02-invariant-audit.md`.',
                     'file': 'day-098-topic-02-invariant-audit.md'}},
            {'key': 'topic-03',
             'title': 'Executing One Representative Recovery Path and Comparing Alternatives',
             'overview': 'A resilient architecture maintains distinct recovery paths optimized for different disaster '
                         'scopes. **Cloud SQL Regional High Availability** is the primary intra-regional recovery '
                         'path, providing fully automated, zero-data-loss failover across zones within seconds. '
                         'Conversely, **Cross-Region Read Replica Promotion** is the catastrophic recovery path '
                         'invoked only when an entire geographical cloud region experiences sustained, catastrophic '
                         'failure. Understanding the exact mechanical trade-offs between these two paths—and executing '
                         'one representative path while documenting the operational runbook for the alternative—is an '
                         'essential competency for Google Cloud Professional Architects.',
             'preview': 'An operational team panics during a single-zone network blip and executes a manual '
                        'cross-region promotion, causing unnecessary data loss and breaking replication. Strict '
                        'runbooks govern when to rely on automatic Regional HA versus when to trigger manual '
                        'cross-region disaster recovery.',
             'technical': '### 1. Comparative Analysis of Recovery Paths\n'
                          '- **Path A: Cloud SQL Regional High Availability (Representative Path Executed):**\n'
                          '  - **Topology:** Primary instance in Zone A, Standby instance in Zone B, sharing a '
                          'synchronized Regional Persistent Disk.\n'
                          '  - **Failover Trigger:** Automated heartbeats detected by Google Cloud control plane. If '
                          'the primary VM fails for >60s, the control plane attaches the regional disk to the standby '
                          'VM and redirects the regional static IP.\n'
                          '  - **RPO & RTO:** RPO = 0; RTO = 60–120 seconds.\n'
                          '  - **Failback:** Completely seamless; once Zone A recovers, it automatically synchronizes '
                          'as the new standby.\n'
                          '- **Path B: Cross-Region Replica Promotion (Alternative Path Detailed):**\n'
                          '  - **Topology:** Primary in `us-central1`, asynchronous Read Replica in `us-east1` '
                          "replicating over Google's global fiber backbone.\n"
                          '  - **Failover Trigger:** Human-in-the-loop operational decision. Promoted via the Cloud '
                          'SQL replica promotion API.\n'
                          '  - **RPO & RTO:** RPO = Asynchronous replication byte lag (typically 1–10 seconds); RTO = '
                          '5–15 minutes (provisioning standalone metadata, promoting instance, updating application '
                          'DNS).\n'
                          '  - **Failback Complexity:** High; promoting a replica permanently severs replication. To '
                          'fail back, SREs must provision a new replica in `us-central1`, wait for full initial data '
                          'synchronization, and execute a scheduled maintenance cutover.',
             'questions': ['Under what exact operational criteria should an organization trigger cross-region replica '
                           'promotion instead of waiting for Regional HA failover?',
                           'Why does promoting a cross-region read replica permanently sever replication, and what '
                           'steps are required to fail back?',
                           'How does Regional Persistent Disk synchronous replication guarantee RPO=0 during an '
                           'unexpected zonal hypervisor crash?'],
             'reference': 'https://docs.cloud.google.com/sql/docs/postgres/replication/cross-region-replicas',
             'reference_label': 'Google Cloud SQL: Cross-region replication, promotion runbooks, and disaster recovery '
                                'planning',
             'scenario': {'symptom': 'During a localized power blip affecting a single zone in Iowa (`us-central1-a`), '
                                     'an on-call engineer panicked and executed a cross-region promotion command to '
                                     'North Virginia (`us-east1`), causing $15,000 in un-replicated transaction data '
                                     'loss and a 6-hour database re-sync ordeal.',
                          'constraints': 'Must establish strict operational runbook guardrails that forbid manual '
                                         'cross-region promotion for single-zone incidents.',
                          'evidence': 'Disaster recovery decision log during regional outage:\n'
                                      '\n'
                                      '```text\n'
                                      '10:00:12Z [Incident Lead] Primary database in us-central1 unresponsive.\n'
                                      "10:01:00Z [DBA-A] Proposes snapshot restore from yesterday's 23:00 backup (est: "
                                      '4.5 hours, RPO: 11 hours loss).\n'
                                      "10:01:30Z [SRE Lead] Overrules: Hot standby replica 'prod-db-east1' "
                                      'synchronized with 0.4s lag!\n'
                                      '10:02:15Z [SRE Lead] Promotes replica -> Master active in 75 seconds. RTO: '
                                      '2m03s, RPO: 0.4s.\n'
                                      '```',
                          'diagnostic_steps': ['Review Cloud Audit Logs to check who invoked '
                                               '`sql.instances.promoteReplica`.',
                                               'Inspect Cloud SQL replication lag metrics '
                                               '`cloudsql.googleapis.com/database/replication/replica_byte_lag` prior '
                                               'to promotion.',
                                               'Verify the status of the regional standby instance in '
                                               '`us-central1-b`.'],
                          'root': 'Lack of operational runbook clarity: the responder did not understand that Regional '
                                  'HA automatically handles zonal loss with zero data loss, mistakenly invoking a '
                                  'destructive cross-region disaster recovery protocol.',
                          'fix': 'Enforce a mandatory 15-minute observation window and Incident Commander '
                                 'authorization before cross-region promotion can be invoked. Document the exact '
                                 'decision matrix in the Disaster Recovery runbook.',
                          'verify': 'Simulate single-zone failure; verify Regional HA completes within 90s with zero '
                                    'data loss. Confirm runbook prevents replica promotion.',
                          'residual': 'If an entire cloud region suffers complete fiber severance lasting >4 hours, '
                                      'cross-region promotion remains the sole recovery mechanism.',
                          'diagram': ('Regional cloud outage severs primary master',
                                      'Cold restore would cause 4.5h downtime & 11h data loss',
                                      'SRE executes warm replica promotion instead',
                                      'Promote cross-region replica with gcloud sql instances promote',
                                      'Full production recovery achieved in 75 seconds')},
             'lab': {'name': 'Cloud SQL Regional HA Failover Drill and Cross-Region Promotion Runbook',
                     'goal': 'Execute the representative Regional HA failover simulation and author the complete '
                             'operational runbook for cross-region disaster recovery.',
                     'expected': 'A validated execution script for Regional HA failover, a comparative decision '
                                 'matrix, and a cross-region promotion runbook.',
                     'mode': 'tabletop analysis & shell synthesis',
                     'prereq': 'Understanding of Cloud SQL HA commands and cross-region replication.',
                     'preflight': 'Review Cloud SQL failover and replica promotion CLI operations.',
                     'steps': ['#### Stage 1: Pre-Flight Recovery Path Decision Matrix\n'
                               'Catalog trade-offs between Warm Replica Promotion versus Cold Snapshot Point-in-Time '
                               'Restore:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > compare_recovery_paths.py\n"
                               'paths = {\n'
                               "    'Replica Promotion': {'RTO': '60-120 seconds', 'RPO': '< 1 second', 'Cost': "
                               "'Continuous running replica'},\n"
                               "    'Point-in-Time Restore': {'RTO': '1-6 hours', 'RPO': '0 seconds (within binlog "
                               "retention)', 'Cost': 'Storage only'},\n"
                               "    'Nightly Backup Restore': {'RTO': '2-8 hours', 'RPO': 'Up to 24 hours', 'Cost': "
                               "'Minimal snapshot cost'}\n"
                               '}\n'
                               "print('[PREFLIGHT] Architecture Disaster Recovery Decision Matrix:')\n"
                               'for k, v in paths.items():\n'
                               '    print(f\'  • {k:24s} | RTO: {v["RTO"]:14s} | RPO: {v["RPO"]:10s}\')\n'
                               'EOF\n'
                               'python3 compare_recovery_paths.py\n'
                               '```',
                               '#### Stage 2: Environment Preflight & Replica Readiness Verification\n'
                               'Verify Cloud SQL instance configuration and replication status:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > check_cloudsql_prereqs.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Verifying Cloud SQL promotion execution environment..."\n'
                               'python3 -c "import sys; print(f\'[PASS] Python runtime '
                               '{sys.version_info.major}.{sys.version_info.minor} verified.\')"\n'
                               'echo "[PASS] Preflight inspection complete."\n'
                               'EOF\n'
                               'bash check_cloudsql_prereqs.sh\n'
                               '```',
                               '#### Stage 3: Core Implementation: Cloud SQL Replica Promotion Script\n'
                               'Author a production bash automation script executing the replica promotion command '
                               'sequence:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > promote_replica.sh\n"
                               '#!/usr/bin/env bash\n'
                               '# Production Cloud SQL Cross-Region Replica Promotion Automation\n'
                               'set -euo pipefail\n'
                               '\n'
                               'INSTANCE_NAME="prod-db-east1"\n'
                               'PROJECT_ID="prod-database-fleet"\n'
                               '\n'
                               'echo "[STEP 1] Verifying replication status on ${INSTANCE_NAME}..."\n'
                               '# In real execution: gcloud sql instances describe ${INSTANCE_NAME} '
                               '--project=${PROJECT_ID}\n'
                               'echo "[PASS] Replica status is RUNNING with replication lag < 1s."\n'
                               '\n'
                               'echo "[STEP 2] Executing replica promotion..."\n'
                               '# Command: gcloud sql instances promote-replica ${INSTANCE_NAME} '
                               '--project=${PROJECT_ID} --quiet\n'
                               'echo "[PROMOTION] Initiated promotion of ${INSTANCE_NAME} to standalone primary '
                               'master."\n'
                               '\n'
                               'echo "[STEP 3] Updating Cloud DNS record..."\n'
                               'echo "[PASS] DNS db.prod.internal updated to promoted instance IP."\n'
                               'echo "[SUCCESS] Recovery path execution completed successfully."\n'
                               'EOF\n'
                               'chmod +x promote_replica.sh\n'
                               'bash promote_replica.sh\n'
                               '```',
                               '#### Stage 4: Execution & Alternative Path Simulation (PITR Comparison)\n'
                               'Simulate the time required for alternative point-in-time restore across database disk '
                               'sizes:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > simulate_pitr_timeline.py\n"
                               'def compute_pitr_duration_minutes(disk_size_gb, restore_rate_mb_s=150):\n'
                               '    total_mb = disk_size_gb * 1024\n'
                               '    seconds = total_mb / restore_rate_mb_s\n'
                               '    return seconds / 60\n'
                               '\n'
                               "print('[ANALYSIS] Estimated Point-in-Time Restore (PITR) RTO Duration:')\n"
                               'for size in [50, 200, 1000, 5000]:\n'
                               '    rto_min = compute_pitr_duration_minutes(size)\n'
                               "    print(f'  • {size:4d} GB Database -> Estimated Restore RTO: {rto_min:.1f} minutes "
                               "({rto_min/60:.2f} hours)')\n"
                               'EOF\n'
                               'python3 simulate_pitr_timeline.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Replication Lag Exceeded Tabletop\n'
                               'Simulate an attempted promotion when replication lag is excessively high (>60s) and '
                               'test safety block:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > test_lag_guardrail.py\n"
                               'def evaluate_promotion_safety(lag_seconds, max_tolerated_lag=10.0):\n'
                               '    if lag_seconds > max_tolerated_lag:\n'
                               "        raise RuntimeError(f'PROMOTION BLOCKED: Replication lag {lag_seconds}s > max "
                               "{max_tolerated_lag}s! High RPO data loss risk.')\n"
                               "    return '[SAFE] Replication lag acceptable for immediate promotion.'\n"
                               '\n'
                               'try:\n'
                               '    evaluate_promotion_safety(lag_seconds=85.0)\n'
                               'except RuntimeError as e:\n'
                               "    print(f'[SAFETY PASS] Orchestrator intercepted dangerous promotion: {e}')\n"
                               'EOF\n'
                               'python3 test_lag_guardrail.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Replication Lag Dashboard Manifest\n'
                               'Author a Cloud Monitoring Dashboard monitoring cross-region replication lag:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > replication_lag_dashboard.json\n"
                               '{\n'
                               '  "displayName": "Cloud SQL Cross-Region Replication Lag SRE",\n'
                               '  "gridLayout": {\n'
                               '    "widgets": [\n'
                               '      {\n'
                               '        "title": "Seconds Behind Master",\n'
                               '        "xyChart": {\n'
                               '          "dataSets": [\n'
                               '            {"timeSeriesQuery": {"timeSeriesFilter": {"filter": '
                               '"metric.type=\\"cloudsql.googleapis.com/database/replication/replica_lag\\""}}}\n'
                               '          ]\n'
                               '        }\n'
                               '      }\n'
                               '    ]\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'echo "[DASHBOARD] Authored replication_lag_dashboard.json"\n'
                               '```',
                               '#### Stage 7: Automated Verification & Promotion Script Assertions\n'
                               'Execute automated test validating promotion script safety clauses:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > assert_promotion_script.py\n"
                               "with open('promote_replica.sh') as f:\n"
                               '    script = f.read()\n'
                               '\n'
                               "assert 'promote-replica' in script\n"
                               "assert 'set -euo pipefail' in script\n"
                               "assert 'Cloud DNS' in script\n"
                               "print('[ASSERT PASS] Promotion script safety syntax strictly verified.')\n"
                               'EOF\n'
                               'python3 assert_promotion_script.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author teardown script removing temporary drill files:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_recovery_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               'echo "Cleaning up Day 98 Topic 3 test scripts..."\n'
                               'rm -f compare_recovery_paths.py check_cloudsql_prereqs.sh promote_replica.sh '
                               'simulate_pitr_timeline.py test_lag_guardrail.py assert_promotion_script.py\n'
                               'echo "[CLEANUP] Retaining dashboard manifest: replication_lag_dashboard.json"\n'
                               'echo "[CLEANUP PASS] Recovery path execution lab teardown completed successfully."\n'
                               'EOF\n'
                               'bash teardown_recovery_lab.sh\n'
                               '```'],
                     'verification': 'The shell script models the representative Regional HA failover path and the '
                                     'Markdown runbook provides a complete decision matrix and multi-step cross-region '
                                     'promotion procedure.',
                     'trouble': 'Ensure `availabilityType: REGIONAL` is set in instance template before triggering '
                                'instance failover.',
                     'cleanup': 'Retain `execute_regional_ha_drill.sh` and `day-098-topic-03-cross-region-runbook.md` '
                                'as exit evidence artifacts.',
                     'accept': 'Completed Regional HA execution script and verified cross-region disaster recovery '
                               'runbook. File: `day-098-topic-03-failover-paths.md`.',
                     'file': 'day-098-topic-03-failover-paths.md'}}],
 'part3_intro': 'The following field cases analyze high-impact disaster recovery failures across Cloud SQL and '
                'enterprise data stores: a cross-region read replica promotion that succeeded at the database tier but '
                'paralyzed production workloads because application connection pools retained hardcoded primary IP '
                'addresses, a hasty point-in-time restore that was prematurely approved following a superficial ping '
                'test, leaving silent primary key sequence gaps and financial ledger corruptions, and a critical '
                'operational blunder where an engineering team initiated a 4.5-hour snapshot restore during a regional '
                'outage despite having a warm, synchronized cross-region read replica ready for 90-second promotion. '
                'Each case delivers verbatim terminal logs, database error codes, diagnostic commands, root cause '
                'analysis, defensible remediations, and dual-lane failed/corrected flow diagrams.',
 'part4_intro': 'These hands-on exercises implement the comprehensive 8-stage operational engineering lifecycle for '
                'Day 98. Engineers construct automated recovery acceptance test suites validating read/write readiness '
                'and connection routing, author data invariant verification engines asserting cryptographic row-hash '
                'integrity and transaction ledger balance across RTO/RPO boundaries, and execute a representative '
                'Cloud SQL cross-region replica promotion recovery path while contrasting trade-offs against '
                'point-in-time restores.'}
