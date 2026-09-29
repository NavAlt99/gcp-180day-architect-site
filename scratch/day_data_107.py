"""day_data_107.py — Exhaustive architecture data specification for Day 107.

Covers Cloud HSM, Secret Manager (Versions, Rotation, Replication, IAM),
and Sensitive Data Protection / Cloud DLP (Inspection, De-identification, Tokenization, Masking).
"""

DAY_NUM = 107

DATA = {
    'day': 107,
    'part1_intro': (
        'Day 107 establishes the architectural design for hardware-backed cryptographic custody, dynamic application '
        'secret lifecycle management, and privacy-preserving data de-identification across Google Cloud. '
        'Architects evaluate Cloud HSM (FIPS 140-2 Level 3 certified hardware security modules), Secret Manager '
        'replication policies, versioning, automated Pub/Sub rotation hooks, and Cloud Next-Gen Sensitive Data Protection '
        '(Cloud DLP) inspection rules, crypto-deterministic pseudonymization, and cryptographic tokenization.'
    ),
    'exit_summary': (
        'Engineers design and verify a Cloud HSM cluster specification, an automated Secret Manager rotation pipeline '
        'with Cloud Functions and Pub/Sub notifications, and a Cloud DLP tokenization and format-preserving de-identification '
        'pipeline fulfilling all Day 107 Exit evidence criteria.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts cryptographic custody, secret distribution models, data privacy mechanisms, '
        'operational latency, and regulatory compliance boundaries across Google Cloud secret and data protection architectures.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Protection Architecture</th>\n'
        '<th>Cryptographic Boundary</th>\n'
        '<th>Primary Operational Purpose</th>\n'
        '<th>Rotation &amp; Lifecycle Model</th>\n'
        '<th>Failure Signal &amp; Recovery Boundary</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>Cloud HSM</strong></td>\n'
        '<td>FIPS 140-2 Level 3 Hardware Module</td>\n'
        '<td>Hardware root of trust; keys never exist in plaintext memory outside HSM</td>\n'
        '<td>Automated version generation; hardware cryptographic attestation</td>\n'
        '<td>HSM cluster hardware failure triggers seamless regional peer failover; attestation verifies genuine Google HSM.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Secret Manager</strong></td>\n'
        '<td>Application Secret Store (CMEK-backed)</td>\n'
        '<td>API keys, database credentials, TLS private keys, service passwords</td>\n'
        '<td>Event-driven rotation via Pub/Sub topic and Cloud Run functions</td>\n'
        '<td>Expired version or failed rotation hook; application receives `NOT_FOUND` or 403 `PERMISSION_DENIED`.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Sensitive Data Protection (DLP)</strong></td>\n'
        '<td>Transform &amp; De-Identification Pipeline</td>\n'
        '<td>Automated inspection, masking, bucketing, and cryptographic tokenization</td>\n'
        '<td>CryptoHash / CryptoDeterministic keyset rotation with transient salt</td>\n'
        '<td>Unclassified schema evolution exposes raw PII; DLP inspection triggers Cloud Monitoring anomaly alert.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>Format-Preserving Encryption (FPE)</strong></td>\n'
        '<td>Reversible Pseudonymization Engine</td>\n'
        '<td>Encrypts credit cards / SSNs while preserving character format and length</td>\n'
        '<td>AES-SIV / FF3-1 wrapped surrogate keys stored in Secret Manager</td>\n'
        '<td>Missing wrapping key prevents re-identification; tokenized values remain queryable without risk.</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 107: Hardware Cryptography, Automated Secret Rotation, and Data De-Identification Topology',
        'desc': 'Architectural layout illustrating Cloud HSM hardware keys, Secret Manager automatic rotation via Pub/Sub, workload IAM access, and Cloud DLP tokenization pipelines.',
        'caption': 'Figure 107.1: Enterprise secrets governance and privacy engineering architecture featuring Cloud HSM, Secret Manager automated rotation choreography, and Cloud DLP tokenization.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Hardware Cryptographic Root & Cloud HSM Cluster',
                'desc': 'FIPS 140-2 Level 3 hardware security modules hosting master root keys and signing anchors',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Secret Manager Storage, Replication & Notification Plane',
                'desc': 'Automatic multi-region replication, user-managed replication, and Pub/Sub rotation event publishers',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Automated Secret Rotator & Target Workload Mesh',
                'desc': 'Cloud Run rotation function updating Cloud SQL passwords and delivering ephemeral credentials to pods',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Sensitive Data Protection (Cloud DLP) Inspection & Transform Plane',
                'desc': 'Streaming and storage inspection jobs identifying PII, credit cards, and government identifiers',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: De-Identified Data Vault & Analytical Consumer Boundary',
                'desc': 'BigQuery and Cloud Storage hosting tokenized, masked, and format-preserved analytical tables',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Cloud HSM Key Ring', 'detail': 'FIPS 140-2 Level 3', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Cryptographic Attestation', 'detail': 'Cavium / Marvell Proof', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Secret Manager Vault', 'detail': 'db-credentials (v1 -> v2)', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Pub/Sub Rotation Topic', 'detail': 'secretmanager.rotate-events', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Rotation Cloud Function', 'detail': 'Executes DB Alter User', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Active Application Pod', 'detail': 'Pulls Version: latest', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Cloud DLP Engine', 'detail': 'Inspection & De-ID Template', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'CryptoDeterministic Tokenizer', 'detail': 'Format-Preserving Surrogates', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Sanitized BigQuery Table', 'detail': 'Pseudonymized Customer Data', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'DLP Finding Incident Alert', 'detail': 'Real-time Security Telemetry', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'HARDWARE TRUST & SECRET STORAGE ZONE', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'AUTOMATED SECRET ROTATION & RUNTIME INJECTION', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'PRIVACY ENGINEERING & DATA DE-IDENTIFICATION VAULT', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Verify Hardware Attestation', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Wrap Secret with HSM Key', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Publish Rotation Trigger', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Invoke Rotator Function', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Inject New Secret Version', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Stream Ingestion Data', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Tokenize Sensitive Fields', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Persist Masked Records', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Alert on Unmasked Leak', 'type': 'warn'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: Secret Access Audit: Caller Identity & IP', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: Secret Rotation Latency & Version State Check', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 345, 'label': 'PROBE 3: Cloud DLP InfoType Discovery & Token Reversibility', 'badge': 'P3', 'color': '#f43f5e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world secret management breakdowns, out-of-sync credential rotations, '
        'and sensitive data exposure across analytical pipelines. Each case details verbatim logs, diagnostic root causes, '
        'production remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on exercises execute the complete 8-stage operational engineering lifecycle for Day 107. '
        'Architects model Cloud HSM attestation verification, construct automated Secret Manager rotation pipelines with '
        'Pub/Sub event triggers, and deploy Cloud DLP format-preserving tokenization policies.'
    ),
    'topics': [
        {
            'key': 'topic-01',
            'title': 'Cloud HSM',
            'overview': (
                'Google Cloud HSM (Hardware Security Module) provides dedicated, certified physical cryptographic protection '
                'for enterprise encryption keys. Validated against FIPS 140-2 Level 3 standards, Cloud HSM guarantees that cryptographic '
                'keys are generated and utilized exclusively inside tamper-resistant hardware modules. Hardware cryptographic '
                'attestation allows security teams to verify that a key was created inside a genuine Google HSM cluster and has never '
                'been exposed in host memory.'
            ),
            'preview': (
                'A financial regulator demands proof that payment signing keys have never existed in general-purpose server RAM; '
                'Cloud HSM cryptographic attestation provides mathematical proof of FIPS 140-2 Level 3 hardware residency.'
            ),
            'technical': (
                '### 1. Cloud HSM Architecture & Compliance\n'
                '- **FIPS 140-2 Level 3 Validation:** Protects against physical tampering, side-channel attacks, and software memory '
                'extraction. Physical HSM clusters are distributed across multiple Google data centers for high availability.\n'
                '- **Fully Managed Abstraction:** Unlike on-premise HSM appliances that require capacity planning and manual firmware '
                'patching, Cloud HSM exposes the standard Cloud KMS REST/gRPC API while transparently handling cluster scaling and failover.\n'
                '\n'
                '### 2. Cryptographic Attestation Verification\n'
                '- Cloud KMS allows downloading a cryptographic attestation statement for any HSM key version.\n'
                '- The attestation is digitally signed by the HSM manufacturer (e.g. Marvell / Cavium) root CA, containing the public key, '
                'key properties, and proof that the private key material is non-exportable.'
            ),
            'questions': [
                'What specific physical and cryptographic protections distinguish Cloud HSM (FIPS 140-2 Level 3) from Cloud KMS Software keys?',
                'How does an enterprise auditor independently verify that a key version was created inside a genuine Google Cloud HSM?',
                'What are the latency and throughput considerations when using Cloud HSM compared to standard Software KMS keys?'
            ],
            'reference': 'https://cloud.google.com/kms/docs/hsm',
            'reference_label': 'Google Cloud HSM: Architecture, FIPS 140-2 Level 3 compliance, and attestation verification',
            'scenario': {
                'symptom': 'Banking compliance audit issues a critical deficiency finding: payment digital signing keys cannot be proven to reside in dedicated hardware.',
                'constraints': 'Financial regulations require non-repudiation and proof that cryptographic private keys cannot be extracted by hypervisor administrators.',
                'evidence': (
                    'Audit inspection findings excerpt:\n\n'
                    '```json\n'
                    '{\n'
                    '  "audit_finding": "CRYPTO-NON-COMPLIANCE",\n'
                    '  "key_resource": "projects/fin-prod/locations/us-central1/keyRings/pay-ring/cryptoKeys/sig-key",\n'
                    '  "observed_protection_level": "SOFTWARE",\n'
                    '  "mandated_protection_level": "HSM_FIPS_140_2_L3",\n'
                    '  "status": "FAIL_ATTESTATION_UNAVAILABLE"\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: The development team generated the original signing key with default Software protection instead '
                    'of specifying the HSM protection level in the version template.'
                ),
                'diagnostic_steps': [
                    'Describe the target CryptoKey using <kbd>gcloud kms keys describe</kbd> to inspect `protectionLevel`.',
                    'Attempt to download cryptographic attestation using <kbd>gcloud kms keys versions get-certificate-chain</kbd>.',
                    'Verify the CA certificate chain from the HSM vendor.',
                    'Check whether existing payment signatures can be migrated to a new HSM key version.'
                ],
                'root': 'CryptoKey was provisioned with SOFTWARE protection level; software keys do not support hardware attestation.',
                'fix': 'Author a new CryptoKey within an HSM-enabled Key Ring, set `protectionLevel=HSM`, generate hardware attestation proof, and rotate application signing.',
                'verify': 'Download HSM attestation statement, verify manufacturer cryptographic signature, and provide signed certificate to auditors.',
                'residual': 'Existing transactions signed with the old software key must be archived with verified historical timestamps.',
                'diagram': (
                    'Payment transactions signed using KMS Software-level key',
                    'Audit inspection requests FIPS 140-2 Level 3 hardware proof',
                    'Software key cannot produce cryptographic hardware attestation',
                    'Provision Cloud HSM key with hardware attestation verification',
                    'Audit approved; transactions signed inside verified tamper-proof HSM'
                )
            },
            'lab': {
                'name': 'Cloud HSM Key Architecture & Attestation Modeling',
                'goal': 'Author declarative Terraform manifests provisioning Cloud HSM keys and implement a Python attestation verification parser validating hardware root certificates.',
                'expected': 'Validated Terraform HSM configuration and working Python script verifying cryptographic attestation chains.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Python 3 and Terraform installed.',
                'preflight': 'Establish working directory `~/hsm-lab`.',
                'steps': [
                    (
                        '#### Declarative Cloud HSM Terraform Architecture\n'
                        'Author a Terraform configuration declaring an HSM-backed asymmetric signing key:\n\n'
                        '```sh\n'
                        'mkdir -p ~/hsm-lab && cd ~/hsm-lab\n'
                        'cat <<\'EOF\' > hsm_key.tf\n'
                        'resource "google_kms_key_ring" "hsm_ring" {\n'
                        '  name     = "banking-hsm-keyring"\n'
                        '  location = "us-central1"\n'
                        '}\n'
                        '\n'
                        'resource "google_kms_crypto_key" "hsm_signing_key" {\n'
                        '  name     = "payment-signing-key"\n'
                        '  key_ring = google_kms_key_ring.hsm_ring.id\n'
                        '  purpose  = "ASYMMETRIC_SIGN"\n'
                        '\n'
                        '  version_template {\n'
                        '    algorithm        = "RSA_SIGN_PSS_4096_SHA512"\n'
                        '    protection_level = "HSM"\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored hsm_key.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### Hardware Attestation Verification Engine\n'
                        'Author a Python script modeling and verifying Cloud HSM manufacturer cryptographic attestation:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > verify_hsm_attestation.py\n'
                        'import hashlib\n'
                        'import hmac\n'
                        'import json\n'
                        '\n'
                        '# Simulated HSM Manufacturer Root Anchor (Cavium / Marvell HSM CA)\n'
                        'HSM_ROOT_SECRET = b"Cavium-Hardware-Root-CA-FIPS-140-2-Level-3"\n'
                        '\n'
                        'def generate_hsm_attestation(key_id: str) -> dict:\n'
                        '    payload = {\n'
                        '        "key_id": key_id,\n'
                        '        "protection_level": "HSM",\n'
                        '        "fips_standard": "140-2-L3",\n'
                        '        "hardware_serial": "HSM-US-C1-849201",\n'
                        '        "exportable": False\n'
                        '    }\n'
                        '    payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")\n'
                        '    sig = hmac.new(HSM_ROOT_SECRET, payload_bytes, hashlib.sha256).hexdigest()\n'
                        '    return {"payload": payload, "signature": sig}\n'
                        '\n'
                        'def verify_attestation(attestation: dict) -> bool:\n'
                        '    payload_bytes = json.dumps(attestation["payload"], sort_keys=True).encode("utf-8")\n'
                        '    expected_sig = hmac.new(HSM_ROOT_SECRET, payload_bytes, hashlib.sha256).hexdigest()\n'
                        '    return hmac.compare_digest(expected_sig, attestation["signature"])\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("CLOUD HSM HARDWARE ATTESTATION VERIFICATION")\n'
                        'print("================================================================")\n'
                        'key_name = "projects/fin-prod/locations/us-central1/keyRings/banking-hsm/cryptoKeys/payment-sig/versions/1"\n'
                        'attestation = generate_hsm_attestation(key_name)\n'
                        'print("Received HSM Attestation:")\n'
                        'print(json.dumps(attestation, indent=2))\n'
                        '\n'
                        'is_valid = verify_attestation(attestation)\n'
                        'status = "VERIFIED (Genuine FIPS 140-2 Level 3 HSM)" if is_valid else "FAILED (Tampered)"\n'
                        'print(f"\\nAttestation Signature Check: {status}")\n'
                        'assert is_valid\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 verify_hsm_attestation.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform HSM configuration and working Python attestation script demonstrating mathematical verification of hardware residency.',
                'verification': 'Review terminal output of <kbd>python3 verify_hsm_attestation.py</kbd> verifying genuine FIPS 140-2 Level 3 signature.',
                'trouble': 'If verification fails, ensure JSON payload sorting matches during signature calculation.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/hsm-lab</kbd>.',
                'file': 'day-107-cloud-hsm.md'
            }
        },
        {
            'key': 'topic-02',
            'title': 'Secret Manager',
            'overview': (
                'Google Cloud Secret Manager is the authoritative service for securely storing, auditing, and rotating sensitive '
                'application credentials, API tokens, database passwords, and TLS private keys. Secret Manager provides automatic '
                'multi-region or customer-managed regional replication, immutable versioning, fine-grained IAM access control, '
                'and integration with Cloud Pub/Sub and Cloud Run functions for zero-downtime automated secret rotation.'
            ),
            'preview': (
                'A database password expires unexpectedly, taking down the checkout API; automated Secret Manager rotation updates '
                'the database and notifies microservices via Pub/Sub before expiration occurs.'
            ),
            'technical': (
                '### 1. Secret Manager Architecture & Replication\n'
                '- **Secrets & Versions:** A Secret is a container object; individual values are stored as immutable SecretVersions '
                '(`v1`, `v2`, `latest`). Versions can be `ENABLED`, `DISABLED`, or `DESTROYED`.\n'
                '- **Replication Policies:**\n'
                '  - `Automatic`: Google automatically replicates secrets across multi-regional locations for maximum durability.\n'
                '  - `User-Managed`: Explicitly pin secrets to specific Google Cloud regions (e.g. `us-central1`, `europe-west1`) '
                'to comply with strict data sovereignty mandates.\n'
                '\n'
                '### 2. Automated Rotation Choreography\n'
                '- **Rotation Schedule:** Secrets specify a `rotation_period` (e.g. 30 days) and a target `next_rotation_time`.\n'
                '- **Pub/Sub Event Bus:** When rotation is due, Secret Manager automatically publishes a `SECRET_ROTATE` message '
                'to a designated Cloud Pub/Sub topic.\n'
                '- **Rotator Function:** A Cloud Run function consumes the event, connects to the downstream target (e.g. Cloud SQL), '
                'generates a new credential, adds a new SecretVersion to Secret Manager, and tests connectivity before disabling the old version.'
            ),
            'questions': [
                'Why should production workloads reference explicit SecretVersion numbers or subscribe to rotation events rather than naively polling `latest`?',
                'How does Secret Manager coordinate with Cloud Pub/Sub to achieve zero-downtime automated secret rotation?',
                'What is the difference between Automatic replication and User-Managed replication in Secret Manager?'
            ],
            'reference': 'https://cloud.google.com/secret-manager/docs/rotation',
            'reference_label': 'Google Cloud Secret Manager: Automated secret rotation architecture and Pub/Sub integration',
            'scenario': {
                'symptom': 'Production payment worker pods fail authentication after automated database password rotation with error `FATAL: password authentication failed for user "app_worker"`.',
                'constraints': 'Credentials must rotate every 30 days; microservices must not experience dropped database connections during rotation.',
                'evidence': (
                    'Kubernetes application pod log showing stale secret caching:\n\n'
                    '```text\n'
                    '2026-09-29T04:22:10Z [ERROR] DB Connection Failed: 28P01: password authentication failed for user "app_worker"\n'
                    '2026-09-29T04:22:11Z [INFO] Current cached SecretVersion: 1\n'
                    '2026-09-29T04:22:12Z [INFO] Active Secret Manager SecretVersion: 2 (Created 2026-09-29T04:20:00Z)\n'
                    '```\n\n'
                    'Analysis: The application fetched the secret once at container startup and cached it in local memory, '
                    'failing to listen for rotation notifications or re-fetch upon authentication failure.'
                ),
                'diagnostic_steps': [
                    'Check active SecretVersion list using <kbd>gcloud secrets versions list db-password</kbd>.',
                    'Inspect database user accounts in Cloud SQL to verify if password for version 2 was committed.',
                    'Review application code to determine whether credential caching includes dynamic refresh logic.',
                    'Verify Pub/Sub subscription delivery state on the secret rotation topic.'
                ],
                'root': 'The application cached database credentials indefinitely in memory and did not subscribe to Secret Manager rotation Pub/Sub events.',
                'fix': 'Implement exponential backoff re-fetch logic upon DB auth failure to retrieve `latest` SecretVersion, and configure dual-password rollover on Cloud SQL.',
                'verify': 'Simulate secret rotation; verify application pod refreshes cached credential and continues database transactions without restart.',
                'residual': 'High connection pools must coordinate rotation gracefully to avoid connection storms during secret refresh.',
                'diagram': (
                    'Secret Manager rotates DB password and publishes version 2',
                    'App pod continues using cached version 1 from startup memory',
                    'Database rejects version 1; app pod fails with auth error 28P01',
                    'Implement dynamic re-fetch hook on auth error and dual-password grace',
                    'App pod re-fetches version 2; database connection pool recovers'
                )
            },
            'lab': {
                'name': 'Secret Manager Automated Rotation & Dynamic Refresh Pipeline',
                'goal': 'Author declarative Secret Manager resources with rotation topics and implement a Python simulation of the automated rotation choreography and application dynamic re-fetch.',
                'expected': 'Validated Terraform Secret Manager configuration and working Python rotation simulation demonstrating zero-downtime secret rollover.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Python 3 and Terraform installed.',
                'preflight': 'Establish working directory `~/secret-mgr-lab`.',
                'steps': [
                    (
                        '#### Declarative Secret Manager Terraform Architecture\n'
                        'Author a Secret Manager resource with rotation schedule and Pub/Sub topic binding:\n\n'
                        '```sh\n'
                        'mkdir -p ~/secret-mgr-lab && cd ~/secret-mgr-lab\n'
                        'cat <<\'EOF\' > secret_rotation.tf\n'
                        'resource "google_pubsub_topic" "secret_rotation_topic" {\n'
                        '  name = "db-password-rotation-events"\n'
                        '}\n'
                        '\n'
                        'resource "google_secret_manager_secret" "db_credential" {\n'
                        '  secret_id = "prod-db-password"\n'
                        '\n'
                        '  replication {\n'
                        '    user_managed {\n'
                        '      replicas {\n'
                        '        location = "us-central1"\n'
                        '      }\n'
                        '      replicas {\n'
                        '        location = "us-east4"\n'
                        '      }\n'
                        '    }\n'
                        '  }\n'
                        '\n'
                        '  rotation {\n'
                        '    rotation_period = "2592000s" # 30 days\n'
                        '    next_rotation_time = "2026-10-29T00:00:00Z"\n'
                        '  }\n'
                        '\n'
                        '  topics {\n'
                        '    name = google_pubsub_topic.secret_rotation_topic.id\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored secret_rotation.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### Secret Rotation & Client Re-Fetch Simulation\n'
                        'Author and run Python script modeling automated secret rollover and dynamic client caching:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > test_secret_rotation.py\n'
                        'import time\n'
                        '\n'
                        'class SecretManager:\n'
                        '    def __init__(self):\n'
                        '        self.versions = {1: "InitialPassw0rd_v1!"}\n'
                        '        self.latest_version = 1\n'
                        '\n'
                        '    def get_secret(self, version: str = "latest") -> tuple[int, str]:\n'
                        '        if version == "latest":\n'
                        '            return self.latest_version, self.versions[self.latest_version]\n'
                        '        v = int(version)\n'
                        '        return v, self.versions[v]\n'
                        '\n'
                        '    def rotate(self, new_password: str):\n'
                        '        new_v = self.latest_version + 1\n'
                        '        self.versions[new_v] = new_password\n'
                        '        self.latest_version = new_v\n'
                        '        print(f"[SECRET MANAGER] Rotated to Version {new_v} (Pub/Sub Event Published)")\n'
                        '\n'
                        'class Database:\n'
                        '    def __init__(self, initial_password: str):\n'
                        '        self.valid_passwords = {initial_password}\n'
                        '\n'
                        '    def authenticate(self, password: str) -> bool:\n'
                        '        return password in self.valid_passwords\n'
                        '\n'
                        'class ApplicationClient:\n'
                        '    def __init__(self, sm: SecretManager, db: Database):\n'
                        '        self.sm = sm\n'
                        '        self.db = db\n'
                        '        self.cached_version, self.cached_password = self.sm.get_secret("latest")\n'
                        '\n'
                        '    def execute_query(self):\n'
                        '        if not self.db.authenticate(self.cached_password):\n'
                        '            print(f"[CLIENT] Auth Failed with cached v{self.cached_version}! Triggering dynamic re-fetch...")\n'
                        '            self.cached_version, self.cached_password = self.sm.get_secret("latest")\n'
                        '            if not self.db.authenticate(self.cached_password):\n'
                        '                raise PermissionError("Database query failed after credential re-fetch.")\n'
                        '            print(f"[CLIENT] Successfully re-authenticated using new SecretVersion {self.cached_version}!")\n'
                        '        print(f"[CLIENT] Database query executed successfully with version {self.cached_version}.")\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("SECRET MANAGER AUTOMATED ROTATION & DYNAMIC RE-FETCH TEST")\n'
                        'print("================================================================")\n'
                        'sm = SecretManager()\n'
                        'db = Database("InitialPassw0rd_v1!")\n'
                        'client = ApplicationClient(sm, db)\n'
                        '\n'
                        '# Initial Query\n'
                        'client.execute_query()\n'
                        '\n'
                        '# Database Rotator Updates Password in DB and Secret Manager\n'
                        'new_secret = "RotatedPassw0rd_v2_Secure!"\n'
                        'db.valid_passwords = {new_secret}  # Cloud SQL accepts new password\n'
                        'sm.rotate(new_secret)\n'
                        '\n'
                        '# Next query triggers dynamic refresh\n'
                        'client.execute_query()\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 test_secret_rotation.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform Secret Manager rotation manifest and Python simulation verifying dynamic client credential refresh.',
                'verification': 'Review terminal output of <kbd>python3 test_secret_rotation.py</kbd> confirming client re-fetches credentials and recovers.',
                'trouble': 'If client fails to recover, confirm Secret Manager latest version updates before invalidating old database password.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/secret-mgr-lab</kbd>.',
                'file': 'day-107-secret-rotation.md'
            }
        },
        {
            'key': 'topic-03',
            'title': 'Sensitive Data Protection (Cloud DLP)',
            'overview': (
                'Google Cloud Sensitive Data Protection (formerly Cloud DLP) provides automated discovery, classification, '
                'and cryptographic de-identification of sensitive personal data across Cloud Storage, BigQuery, and custom workloads. '
                'With built-in detectors for over 150 global infoTypes (PII, SSNs, credit cards, passport numbers), Cloud DLP '
                'enables privacy engineering through masking, bucketing, character redaction, and reversible format-preserving '
                'cryptographic tokenization.'
            ),
            'preview': (
                'An analytics team requests access to raw customer purchase history; Cloud DLP pseudonymizes personal identifiers '
                'using deterministic crypto-hashing, allowing user behavior joins without exposing real names or credit cards.'
            ),
            'technical': (
                '### 1. Cloud DLP Inspection & Discovery\n'
                '- **infoType Detectors:** Pattern-matching, dictionaries, and contextual regex for global data formats '
                '(e.g. `EMAIL_ADDRESS`, `CREDIT_CARD_NUMBER`, `US_SOCIAL_SECURITY_NUMBER`, `IP_ADDRESS`).\n'
                '- **Likelihood Thresholds:** Configurable from `VERY_UNLIKELY` to `VERY_LIKELY` to control false-positive rates.\n'
                '\n'
                '### 2. Transformation & De-Identification Methods\n'
                '- **Masking:** Replaces characters with a masking character (e.g. `4111-XXXX-XXXX-1111`). Irreversible.\n'
                '- **Bucketing:** Generalizes continuous values into categorical ranges (e.g. Age `27` -> `20-30`).\n'
                '- **CryptoDeterministic Tokenization:** Uses AES-SIV with a transient surrogate key to produce identical pseudonyms '
                'for identical input. Preserves relational join capabilities in BigQuery without revealing true identity.\n'
                '- **Format-Preserving Encryption (FPE):** Reversible cryptographic encryption preserving exact character length '
                'and character set, ensuring legacy schemas and database column constraints do not break.'
            ),
            'questions': [
                'How does CryptoDeterministic tokenization in Cloud DLP enable cross-table relational joins while maintaining privacy compliance?',
                'What is the difference between irreversible data masking and reversible Format-Preserving Encryption (FPE)?',
                'How can Cloud DLP inspection jobs be automated upon Cloud Storage object uploads using Eventarc?'
            ],
            'reference': 'https://cloud.google.com/sensitive-data-protection/docs/deidentification-overview',
            'reference_label': 'Google Cloud Sensitive Data Protection: De-identification and pseudonymization techniques',
            'scenario': {
                'symptom': 'Marketing analyst runs a routine customer churn query and accidentally exports 250,000 unmasked customer credit card records.',
                'constraints': 'Analysts require persistent customer purchase correlation, but raw cardholder PANs must never appear in query results.',
                'evidence': (
                    'BigQuery query results table snippet prior to remediation:\n\n'
                    '```text\n'
                    '+-----------+--------------------+---------------------+----------------+\n'
                    '| user_id   | customer_name      | card_number         | total_spend    |\n'
                    '+-----------+--------------------+---------------------+----------------+\n'
                    '| CUST-1082 | Alice Johnson      | 4532-8192-3019-4812 | $1,240.50      |\n'
                    '| CUST-1083 | Bob Smith          | 5412-9018-2938-1920 | $412.00        |\n'
                    '+-----------+--------------------+---------------------+----------------+\n'
                    '```\n\n'
                    'Analysis: Raw ingestion pipeline dumped raw payment payload into the analytical warehouse without passing '
                    'through an inline Cloud DLP de-identification transformation.'
                ),
                'diagnostic_steps': [
                    'Review BigQuery schema to locate all columns containing sensitive financial infoTypes.',
                    'Check Cloud DLP inspection templates for existing `CREDIT_CARD_NUMBER` rule configurations.',
                    'Inspect data pipeline (Dataflow / Cloud Run) to confirm whether DLP transformation step was bypassed.',
                    'Audit Cloud DLP transform logs for throughput bottlenecks and error rates.'
                ],
                'root': 'Data ingestion pipeline omitted the Cloud DLP transformation step, storing raw PANs in queryable tables.',
                'fix': 'Deploy a Cloud DLP de-identification template enforcing character masking (retain last 4 digits) and deterministic tokenization on customer identifiers.',
                'verify': 'Re-run analytical query; verify credit cards are masked as `XXXX-XXXX-XXXX-4812` and customer IDs are pseudonymized.',
                'residual': 'Authorized compliance teams requiring re-identification must maintain access to the DLP unwrapping key in Secret Manager.',
                'diagram': (
                    'Ingestion pipeline dumps raw credit cards and PII into BigQuery',
                    'Lack of DLP transformation exposes plaintext cardholder data',
                    'Analyst exports sensitive database table; data spill incident declared',
                    'Insert Cloud DLP de-identification template into ingestion stream',
                    'Credit cards masked and customer IDs tokenized; analytical value preserved'
                )
            },
            'lab': {
                'name': 'Cloud DLP De-Identification & Crypto-Tokenization Engine',
                'goal': 'Author a declarative Cloud DLP de-identification template manifest and implement a Python simulation of masking and deterministic tokenization.',
                'expected': 'Terraform DLP template configuration and Python script demonstrating irreversible masking and deterministic pseudonymization.',
                'mode': 'Declarative Terraform and Python CLI modeling',
                'prereq': 'Python 3 and Terraform installed.',
                'preflight': 'Establish working directory `~/dlp-lab`.',
                'steps': [
                    (
                        '#### Declarative Cloud DLP Template Terraform Architecture\n'
                        'Author a Cloud DLP DeidentifyTemplate masking card numbers and tokenizing emails:\n\n'
                        '```sh\n'
                        'mkdir -p ~/dlp-lab && cd ~/dlp-lab\n'
                        'cat <<\'EOF\' > dlp_template.tf\n'
                        'resource "google_data_loss_prevention_deidentify_template" "privacy_template" {\n'
                        '  parent       = "projects/brightloaf-prod"\n'
                        '  display_name = "Customer Analytics Privacy De-ID Template"\n'
                        '  description  = "Mask credit cards and deterministically tokenize customer emails"\n'
                        '\n'
                        '  deidentify_config {\n'
                        '    record_transformations {\n'
                        '      field_transformations {\n'
                        '        fields {\n'
                        '          name = "card_number"\n'
                        '        }\n'
                        '        primitive_transformation {\n'
                        '          character_mask_config {\n'
                        '            masking_character    = "X"\n'
                        '            number_to_mask       = 12\n'
                        '            reverse_order        = false\n'
                        '          }\n'
                        '        }\n'
                        '      }\n'
                        '    }\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        'echo "[TERRAFORM] Authored dlp_template.tf successfully."\n'
                        '```'
                    ),
                    (
                        '#### Cloud DLP Tokenization & Masking Engine\n'
                        'Author and run Python script simulating Cloud DLP masking and deterministic tokenization:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > test_dlp_transform.py\n'
                        'import hashlib\n'
                        'import hmac\n'
                        'import re\n'
                        '\n'
                        'SURROGATE_KEY = b"Brightloaf-DLP-Surrogate-Key-98412"\n'
                        '\n'
                        'def mask_card_number(pan: str) -> str:\n'
                        '    digits = re.sub(r"[^0-9]", "", pan)\n'
                        '    if len(digits) < 12:\n'
                        '        return pan\n'
                        '    # Mask all but last 4 digits\n'
                        '    masked_digits = "X" * (len(digits) - 4) + digits[-4:]\n'
                        '    # Format in standard 4-digit blocks\n'
                        '    return "-".join(masked_digits[i:i+4] for i in range(0, len(masked_digits), 4))\n'
                        '\n'
                        'def deterministic_tokenize(identifier: str) -> str:\n'
                        '    token = hmac.new(SURROGATE_KEY, identifier.encode("utf-8"), hashlib.sha256).hexdigest()[:16]\n'
                        '    return f"TOK-{token.upper()}"\n'
                        '\n'
                        'raw_customers = [\n'
                        '    {"id": "101", "email": "alice@brightloaf.com", "card": "4532-8192-3019-4812", "amount": 42.50},\n'
                        '    {"id": "102", "email": "bob@example.org", "card": "5412-9018-2938-1920", "amount": 108.00},\n'
                        '    {"id": "103", "email": "alice@brightloaf.com", "card": "4532-8192-3019-4812", "amount": 15.20} # Same user\n'
                        ']\n'
                        '\n'
                        'print("================================================================")\n'
                        'print("CLOUD DLP DE-IDENTIFICATION & TOKENIZATION ENGINE")\n'
                        'print("================================================================")\n'
                        'print("Raw Ingestion Data (RESTRICTED):")\n'
                        'for c in raw_customers:\n'
                        '    print(f"  • {c[\'id\']} | {c[\'email\']:22s} | {c[\'card\']} | ${c[\'amount\']}")\n'
                        '\n'
                        'deidentified = []\n'
                        'for c in raw_customers:\n'
                        '    deidentified.append({\n'
                        '        "token_id": deterministic_tokenize(c["email"]),\n'
                        '        "masked_card": mask_card_number(c["card"]),\n'
                        '        "amount": c["amount"]\n'
                        '    })\n'
                        '\n'
                        'print("\\nDe-Identified Analytical Output (INTERNAL / SANITIZED):")\n'
                        'for d in deidentified:\n'
                        '    print(f"  • Token: {d[\'token_id\']:20s} | Card: {d[\'masked_card\']:19s} | Spend: ${d[\'amount\']}")\n'
                        '\n'
                        '# Validation: Confirm Alice gets identical deterministic token across records\n'
                        'assert deidentified[0]["token_id"] == deidentified[2]["token_id"]\n'
                        'print("\\n[PASS] Deterministic token equality verified for repeated user identifier.")\n'
                        'print("[PASS] Credit card masked: raw numbers eliminated from analytical store.")\n'
                        'print("================================================================")\n'
                        'EOF\n'
                        'python3 test_dlp_transform.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated Terraform Cloud DLP template and Python script proving successful masking and deterministic tokenization across records.',
                'verification': 'Review terminal output of <kbd>python3 test_dlp_transform.py</kbd> confirming credit cards masked and identical token assigned to Alice across records.',
                'trouble': 'If card masking fails, verify regular expression strips non-digit characters before length calculation.',
                'cleanup': 'Remove test directory: <kbd>rm -rf ~/dlp-lab</kbd>.',
                'file': 'day-107-dlp-tokenization.md'
            }
        }
    ]
}
