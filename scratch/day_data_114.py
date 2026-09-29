"""day_data_114.py — Exhaustive architecture data specification for Day 114.

Covers Secure SDLC and Shift-Left Security,
Artifact Registry with Vulnerability Scanning & SBOM Generation, and
Binary Authorization, Attestations, and Break-Glass Procedures.
"""

DAY_NUM = 114

DATA = {
    'day': 114,
    'part1_intro': (
        'Day 114 establishes the software supply chain integrity, artifact provenance, and workload admission architecture '
        'across Google Cloud. Enterprise architects examine the Secure Software Development Lifecycle (SSDLC) and shift-left '
        'security controls, Artifact Registry vulnerability scanning and Software Bill of Materials (SBOM) generation, '
        'and cryptographic admission governance using Binary Authorization, asymmetric Cloud KMS attestations, and auditable '
        'emergency break-glass procedures.'
    ),
    'exit_summary': (
        'An artifact digest, findings triage and accept/reject decision with an exception procedure.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts supply chain security stages, cryptographic verification gates, '
        'metadata registries, and admission enforcement mechanisms across container lifecycle pipelines.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Pipeline Phase</th>\n'
        '<th>Security Gate &amp; Mechanism</th>\n'
        '<th>GCP Integration &amp; Tooling</th>\n'
        '<th>Cryptographic Artifact Output</th>\n'
        '<th>Failure Mode &amp; Bypass Risk</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>1. Shift-Left / Pre-Commit</strong></td>\n'
        '<td>Static secret detection, SAST, IaC policy linting</td>\n'
        '<td>Git pre-commit hooks, Cloud Build SAST builders, Checkov</td>\n'
        '<td>Signed commit hash, static analysis pass report</td>\n'
        '<td>Developers using git commit --no-verify bypassing local secret checks.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>2. Immutable Registry</strong></td>\n'
        '<td>Artifact storage, vulnerability discovery, SBOM generation</td>\n'
        '<td>Artifact Registry, Artifact Analysis (OS &amp; package CVEs)</td>\n'
        '<td>Immutable SHA-256 image digest (`@sha256:...`), SPDX SBOM</td>\n'
        '<td>Relying on mutable Docker tags (`:latest`) allowing silent upstream injection.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>3. Attestation Authority</strong></td>\n'
        '<td>Asymmetric signature minting for verified build/scan passes</td>\n'
        '<td>Cloud KMS asymmetric signing keys (PKIX / ECDSA), Grafeas API</td>\n'
        '<td>Signed Binary Authorization Attestation occurrence</td>\n'
        '<td>Compromise or leak of the private Cloud KMS attestation key.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>4. Admission Control</strong></td>\n'
        '<td>Pre-execution cryptographic admission verification</td>\n'
        '<td>Binary Authorization Admission Webhook on GKE &amp; Cloud Run</td>\n'
        '<td>Kubernetes AdmissionResponse (Allowed / Denied)</td>\n'
        '<td>Policy set to DRYRUN_AUDIT_LOG_ONLY failing to block untrusted images.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>5. Emergency Override</strong></td>\n'
        '<td>Auditable break-glass exception procedure for outages</td>\n'
        '<td>Kubernetes pod annotation `image-policy.k8s.io/break-glass`</td>\n'
        '<td>High-priority Cloud Audit Log alert dispatched to SOC</td>\n'
        '<td>Unmonitored break-glass annotations abused to run malicious payloads.</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 114: Secure SDLC, Artifact Registry, and Binary Authorization Admission Topology',
        'desc': 'Architectural layout illustrating shift-left CI/CD scanning, Artifact Registry image digests, Cloud KMS attestation signing, and GKE Binary Authorization admission webhooks.',
        'caption': 'Figure 114.1: Cryptographic container supply chain featuring Cloud Build CI/CD, Artifact Analysis vulnerability scanning, KMS attestation generation, and Binary Authorization admission gates.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Developer Workstation & Source Control Plane',
                'desc': 'Git repositories, pre-commit secret detection hooks, and cryptographic commit signing',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Cloud Build Automated CI/CD & SAST Pipeline',
                'desc': 'Isolated build workers, SAST scanning, container image compilation, and SBOM extraction',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Artifact Registry & Continuous Vulnerability Analysis',
                'desc': 'Regional container repositories, SHA-256 digest minter, and Artifact Analysis continuous CVE scanner',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Cloud KMS Attestation Signer & Grafeas Metadata Vault',
                'desc': 'Asymmetric ECDSA signing keys, Security Scan Attestor, and signed occurrence storage',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: GKE Binary Authorization Admission Enforcement Plane',
                'desc': 'Kubernetes admission controller, signature verification engine, and break-glass audit logger',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Developer Pre-Commit', 'detail': 'Secret & Lint Checker', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Signed Git Repository', 'detail': 'Enforced Pull Requests', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Cloud Build Worker', 'detail': 'Distroless Multi-Stage Build', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'SBOM Generator', 'detail': 'SPDX Dependency Manifest', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Artifact Registry Repo', 'detail': 'Immutable SHA-256 Digest', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Artifact Analysis Scanner', 'detail': 'Continuous CVE Detection', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Cloud KMS Asym Key', 'detail': 'ECDSA P-256 Signing Key', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Attestation Authority', 'detail': 'Grafeas ATTESTATION Note', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'BinAuth Admission Webhook', 'detail': 'Enforces Signed Digest', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'GKE Production Node', 'detail': 'Verified Pod Runtime', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'SHIFT-LEFT SOURCE & BUILD SECURITY BOUNDARY', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'REGISTRY SCANNING & ATTESTATION AUTHORITY DOMAIN', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'GKE BINARY AUTHORIZATION ADMISSION CONTROLLER', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Verify Pre-Commit Pass', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Trigger Cloud Build', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Generate Build Provenance', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Push Immutable Digest', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Execute Vulnerability Scan', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Pass Vulnerability Gate', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Sign Attestation Occurrence', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Submit Pod Manifest', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Admit Verified Workload', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: Build Provenance: SLSA Level 3 Cryptographic Hash Match', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: Registry CVE Gate: Zero Fixable CRITICAL / HIGH Findings', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 450, 'label': 'PROBE 3: Admission Enforcement: Block Non-Attested Image Ingestion', 'badge': 'P3', 'color': '#22c55e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world software supply chain attacks, base image poisoning incidents, '
        'accidental credential commits, and Binary Authorization admission outages across enterprise Google Cloud clusters. '
        'Each scenario details verbatim diagnostic logs, root cause mechanisms, production remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on architectural exercises implement the complete operational engineering lifecycle for Day 114. '
        'Architects build a shift-left secret and SAST gatekeeper script, inspect Artifact Registry image metadata and SBOM dependencies, '
        'and develop a cryptographic Binary Authorization attestation signing and verification pipeline with break-glass logging.'
    ),
    'topics': [
        # TOPIC 1
        {
            'key': 'topic-01',
            'title': 'Secure SDLC and shift-left security',
            'overview': (
                'The Secure Software Development Lifecycle (SSDLC) shifts security analysis leftward into the earliest phases of development, '
                'detecting vulnerabilities, misconfigurations, and hardcoded secrets before code is committed or compiled. '
                'By integrating automated pre-commit hooks, Static Application Security Testing (SAST), Software Composition Analysis (SCA), '
                'and Infrastructure-as-Code (IaC) policy validation into developer workstations and Cloud Build pipelines, organizations eliminate '
                'costly remediation cycles in production.'
            ),
            'preview': (
                'A developer accidentally commits a plaintext Cloud SQL database credential into git; the credential is baked into a container '
                'image layer and published to a shared registry before security teams discover the leak.'
            ),
            'technical': (
                'A comprehensive shift-left architecture enforces automated validation gates at every stage prior to container packaging.\n\n'
                '### Shift-Left Architecture & Gate Hierarchy\n'
                '1. **Pre-Commit Phase (Workstation Boundary)**:\n'
                '   - Developer workstations execute local pre-commit hooks that inspect staged git diffs.\n'
                '   - Regex and entropy engines detect high-entropy strings, private keys (`-----BEGIN PRIVATE KEY-----`), API tokens, and service account keys.\n'
                '   - IaC linters evaluate Terraform manifests against enterprise security policies (e.g. flagging `0.0.0.0/0` firewall rules) before push.\n'
                '2. **Continuous Integration Phase (Cloud Build)**:\n'
                '   - **Static Application Security Testing (SAST)**: Analyzes source code for semantic vulnerabilities (SQL injection, XSS, insecure deserialization) without executing the code.\n'
                '   - **Software Composition Analysis (SCA)**: Scans third-party open-source libraries and package manifests (`requirements.txt`, `package.json`, `go.mod`) against known CVE databases.\n'
                '   - **Base Image Pinning**: Mandates that Dockerfiles inherit strictly from minimal, hardened base images (e.g. Google Cloud Distroless) referenced by immutable SHA-256 digest rather than mutable floating tags.\n'
                '3. **Policy-as-Code Gate**:\n'
                '   - Tools like Checkov or OPA evaluate generated Kubernetes manifests. Pods specifying `runAsUser: 0` or missing security contexts are terminated pre-build.\n'
                '   - Cloud Build exits with non-zero status upon encountering any policy violation, preventing container compilation.'
            ),
            'questions': [
                'Why is detecting secrets at the pre-commit stage drastically more effective than attempting to scrub secrets from Git history after pushing?',
                'How does base image pinning by SHA-256 digest protect build pipelines from upstream dependency poisoning?',
                'What is the architectural role of Software Composition Analysis (SCA) in preventing supply chain attacks like Log4Shell?'
            ],
            'reference': 'https://docs.cloud.google.com/binary-authorization/docs',
            'reference_label': 'Google Cloud Secure Software Development Lifecycle Guide',
            'scenario': {
                'symptom': 'Plaintext service account private key committed into application repository and baked into Docker image layer.',
                'impact': 'Attacker extracts service account key from public container image registry; accesses backend Cloud SQL databases.',
                'constraints': 'CI/CD pipeline must block any build containing high-entropy credentials or unpinned packages.',
                'evidence': (
                    'Cloud Build failure log and secret exposure record:\n\n'
                    '```text\n'
                    'Step #1 - SecretScan: [CRITICAL] Hardcoded Google Service Account Key detected in src/config.py:34\n'
                    'Pattern: "\"private_key\": \"-----BEGIN PRIVATE KEY-----\""\n'
                    'Commit: 8f9b21a (Author: dev-intern@enterprise.com)\n'
                    'Build Status: FAILED (Exit Code 1)\n'
                    '```\n\n'
                    'Analysis: Although Cloud Build caught the secret, the developer had already pushed the commit to a remote branch, '
                    'requiring immediate credential invalidation across Google Cloud IAM.'
                ),
                'diagnostic_steps': [
                    'Review Cloud Build step logs for the triggering repository commit.',
                    'Check Google Cloud Secret Manager to confirm whether the exposed key corresponds to an active IAM credential.',
                    'Inspect developer local git configuration to verify whether pre-commit hooks were installed and active.',
                    'Immediately execute <kbd>gcloud iam service-accounts keys disable</kbd> for the compromised key ID.'
                ],
                'root': 'The development workflow lacked mandatory pre-commit hooks, allowing hardcoded secrets to be pushed to remote source repositories.',
                'fix': 'Enforce pre-commit secret scanning hooks across all developer workstations via repository templates, and rotate the compromised service account key immediately.',
                'residual': 'Encrypted or obfuscated secrets that do not match standard high-entropy signatures could bypass regex-based static scanners.',
                'diagram': (
                    'Developer hardcodes service account private key in application config',
                    'Pre-commit hooks absent; commit pushed to remote git repository',
                    'Cloud Build detects secret during build; build fails but key is exposed',
                    'Enforce workstation pre-commit hooks and automated IAM key rotation',
                    'Secrets blocked on local developer laptop prior to git commit'
                )
            },
            'lab': {
                'name': 'Shift-Left Secret Scanner & Pre-Commit CI Validator',
                'goal': 'Implement a Python shift-left security validator that scans codebases for hardcoded secrets, verifies immutable base image digests in Dockerfiles, and enforces CI/CD build admission gates.',
                'expected': 'A functioning Python security scanner that detects secrets and unpinned base images, outputting pass/fail exit codes.',
                'mode': 'Python script and CLI data modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/shift-left-lab</kbd>.',
                'steps': [
                    (
                        '#### Set up Sample Source Code and Dockerfile Assets\n'
                        'Create the lab directory and write sample application files, including a Dockerfile with an unpinned base image and a script containing a hardcoded key:\n\n'
                        '```sh\n'
                        'mkdir -p ~/shift-left-lab && cd ~/shift-left-lab\n'
                        'cat <<\'EOF\' > Dockerfile.bad\n'
                        'FROM python:latest\n'
                        'WORKDIR /app\n'
                        'COPY . .\n'
                        'CMD ["python", "app.py"]\n'
                        'EOF\n'
                        'cat <<\'EOF\' > config.py\n'
                        'DB_HOST = "10.0.0.5"\n'
                        'API_SECRET_KEY = "AIzaSyD-EXAMPLE-SECRET-KEY-99201"\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Shift-Left Security Gatekeeper\n'
                        'Write a Python scanner that evaluates the repository files for high-entropy secrets and verifies that Dockerfiles pin images by immutable SHA-256 digest:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > shift_left_gatekeeper.py\n'
                        'import re\n'
                        'import sys\n'
                        'import json\n'
                        '\n'
                        'SECRET_PATTERNS = [\n'
                        '    (re.compile(r"AIza[0-9A-Za-z-_]{35}"), "Google API Key"),\n'
                        '    (re.compile(r"-----BEGIN PRIVATE KEY-----"), "RSA/PKCS8 Private Key")\n'
                        ']\n'
                        '\n'
                        'def scan_files():\n'
                        '    violations = []\n'
                        '    print("=== Shift-Left Pre-Commit / CI Security Gatekeeper ===\\n")\n'
                        '\n'
                        '    # Check config.py for hardcoded credentials\n'
                        '    try:\n'
                        '        with open("config.py", "r") as f:\n'
                        '            content = f.read()\n'
                        '            for pattern, name in SECRET_PATTERNS:\n'
                        '                if pattern.search(content):\n'
                        '                    violations.append({\n'
                        '                        "file": "config.py",\n'
                        '                        "type": "HARDCODED_SECRET",\n'
                        '                        "detail": f"Detected {name} in source code."\n'
                        '                    })\n'
                        '    except FileNotFoundError:\n'
                        '        pass\n'
                        '\n'
                        '    # Check Dockerfile for base image pinning\n'
                        '    try:\n'
                        '        with open("Dockerfile.bad", "r") as f:\n'
                        '            for line in f:\n'
                        '                if line.startswith("FROM"):\n'
                        '                    image = line.strip().split()[1]\n'
                        '                    if "@sha256:" not in image:\n'
                        '                        violations.append({\n'
                        '                            "file": "Dockerfile.bad",\n'
                        '                            "type": "UNPINNED_BASE_IMAGE",\n'
                        '                            "detail": f"Base image {image} uses mutable tag instead of immutable @sha256 digest."\n'
                        '                        })\n'
                        '    except FileNotFoundError:\n'
                        '        pass\n'
                        '\n'
                        '    print(f"Gatekeeper Evaluation Completed. Violations Found: {len(violations)}\\n")\n'
                        '    for v in violations:\n'
                        '        print(f"[{v[\'type\']}] in {v[\'file\']}: {v[\'detail\']}")\n'
                        '\n'
                        '    verdict = "FAIL" if violations else "PASS"\n'
                        '    report = {\n'
                        '        "verdict": verdict,\n'
                        '        "violations": violations\n'
                        '    }\n'
                        '\n'
                        '    with open("shift_left_report.json", "w") as out:\n'
                        '        json.dump(report, out, indent=2)\n'
                        '    print(f"\\nWrote shift_left_report.json with verdict: {verdict}")\n'
                        '    return 1 if violations else 0\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    sys.exit(scan_files())\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute the Shift-Left Gatekeeper and Verify Blocked Build\n'
                        'Run the scanner and inspect the JSON report to verify that the gatekeeper catches the hardcoded key and unpinned Dockerfile:\n\n'
                        '```sh\n'
                        'python3 shift_left_gatekeeper.py || true\n'
                        'cat shift_left_report.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python shift-left security tool detecting hardcoded secrets and unpinned container base images before CI compilation.',
                'verification': 'Review terminal output of <kbd>python3 shift_left_gatekeeper.py</kbd> confirming verdict FAIL and detection of UNPINNED_BASE_IMAGE.',
                'trouble': 'If script errors out unexpectedly, verify python file syntax.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/shift-left-lab</kbd>.',
                'file': 'day-114-shift-left.md'
            }
        },

        # TOPIC 2
        {
            'key': 'topic-02',
            'title': 'Artifact Registry with vulnerability scanning',
            'overview': (
                'Artifact Registry serves as Google Cloud’s secure, scalable repository management platform for container images, '
                'OS packages, and language-level build artifacts. Fully replacing legacy Container Registry, Artifact Registry '
                'provides regional isolation, granular project-level IAM controls, Customer-Managed Encryption Keys (CMEK), '
                'VPC Service Controls protection, automated vulnerability scanning via Artifact Analysis, and native Software '
                'Bill of Materials (SBOM) generation.'
            ),
            'preview': (
                'A development team deploys a container using a mutable tag (`:latest`); upstream library maintainers push a breaking '
                'dependency containing a zero-day vulnerability, silently compromising production clusters.'
            ),
            'technical': (
                'Artifact Registry establishes the cryptographic bridge between CI/CD build outputs and runtime cluster admission.\n\n'
                '### Architectural Capabilities\n'
                '- **Regional & Multi-Regional Repositories**: Artifacts can be pinned to specific sovereign geographic regions (e.g. `us-central1`, `europe-west3`) to enforce data residency constraints.\n'
                '- **Immutable Artifact Digests**: While human-friendly tags (e.g. `:v1.2.0`, `:prod`) are mutable and can be overwritten, every container image possesses an immutable SHA-256 content digest (e.g. `@sha256:d89bf2...`). Production deployment manifests must reference images exclusively by digest.\n'
                '- **Artifact Analysis Integration**:\n'
                '  - *Automated Vulnerability Scanning*: Scans container images for OS-level CVEs (Debian, Alpine, Ubuntu, RHEL) and application-level dependencies (Java Maven, Node.js npm, Python PyPI, Go modules).\n'
                '  - *Continuous Scanning*: Evaluates stored images continuously against newly disclosed CVEs in the National Vulnerability Database (NVD) without requiring images to be rebuilt.\n'
                '  - *Software Bill of Materials (SBOM)*: Generates standardized SPDX / CycloneDX format SBOMs listing all software components, licenses, and dependency hierarchies embedded in the image.\n'
                '- **Access Control & Network Security**: Integrated with Cloud IAM (fine-grained Reader, Writer, Admin roles per repository) and VPC Service Controls to prevent unauthorized egress of proprietary images.'
            ),
            'questions': [
                'Why is referencing container images by immutable SHA-256 digest required for secure, reproducible production deployments?',
                'How does Artifact Analysis continuous scanning discover newly disclosed vulnerabilities in container images pushed months ago?',
                'What information does a Software Bill of Materials (SBOM) provide that standard vulnerability reports lack?'
            ],
            'reference': 'https://docs.cloud.google.com/artifact-analysis/docs',
            'reference_label': 'Google Cloud Artifact Registry and Artifact Analysis Documentation',
            'scenario': {
                'symptom': 'Production deployment of container tag `:v2.1` executes an unverified container build containing a newly introduced CVE.',
                'impact': 'Cluster nodes run an insecure base image with a critical CVSS 9.8 remote code execution vulnerability; deployment pipeline lacked digest pinning.',
                'constraints': 'All production manifests must specify immutable `@sha256:` digests and enforce zero unpatched CRITICAL CVEs.',
                'evidence': (
                    'Kubernetes deployment manifest vs Registry Metadata:\n\n'
                    '```yaml\n'
                    'spec:\n'
                    '  containers:\n'
                    '  - name: payment-api\n'
                    '    image: us-central1-docker.pkg.dev/prod-proj/cde-repo/payment-api:v2.1\n'
                    '```\n\n'
                    'Registry Scan Occurrence:\n'
                    '```text\n'
                    'Digest: sha256:4a8e91... (tag v2.1 overwritten 2 hours ago)\n'
                    'Vulnerability: CVE-2026-4412 (Severity: CRITICAL, CVSS: 9.8)\n'
                    'Fix Available: YES (libssl3 update)\n'
                    '```\n\n'
                    'Analysis: Re-using the `:v2.1` tag allowed a rebuilt, vulnerable container to overwrite the approved image in Artifact Registry.'
                ),
                'diagnostic_steps': [
                    'Inspect the repository in Artifact Registry to determine how many times tag `v2.1` has been updated.',
                    'Query Artifact Analysis vulnerability occurrences for the specific SHA-256 digest running on GKE nodes.',
                    'Check Cloud Audit Logs to identify the identity that pushed the overwritten image digest.',
                    'Review the CI/CD pipeline manifest to confirm why digest-based deployment was not enforced.'
                ],
                'root': 'The deployment pipeline relied on mutable Docker tags rather than immutable SHA-256 digests, allowing an unverified build to overwrite production images.',
                'fix': 'Enforce immutable tags in Artifact Registry settings, mandate `@sha256:` digest references in deployment manifests, and gate deployments on Artifact Analysis scan results.',
                'residual': 'Zero-day vulnerabilities without assigned CVE identifiers in public databases cannot be detected by automated scanners.',
                'diagram': (
                    'CI/CD rebuilds application and overwrites existing mutable Docker tag',
                    'Deployment manifest references mutable tag; pulls untested base image',
                    'New image contains unpatched remote code execution vulnerability',
                    'Enforce immutable tags and require deployment by SHA-256 digest',
                    'Artifact Analysis validates zero CVEs; only verified digests deployed'
                )
            },
            'lab': {
                'name': 'Artifact Registry Digest Parser & SBOM Dependency Auditor',
                'goal': 'Implement a Python metadata analyzer that extracts container image digests from Artifact Registry payloads, parses an SPDX SBOM dependency tree, and enforces CVE threshold policies.',
                'expected': 'A Python verification tool resolving image digests, evaluating SBOM components, and producing an admission verdict.',
                'mode': 'Python script and CLI data modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/artifact-audit-lab</kbd>.',
                'steps': [
                    (
                        '#### Generate Synthetic Artifact Metadata and SPDX SBOM\n'
                        'Create a simulated Artifact Registry metadata JSON and an accompanying SPDX SBOM dependency manifest:\n\n'
                        '```sh\n'
                        'mkdir -p ~/artifact-audit-lab && cd ~/artifact-audit-lab\n'
                        'cat <<\'EOF\' > artifact_metadata.json\n'
                        '{\n'
                        '  "repository": "us-central1-docker.pkg.dev/fintech-prod/payment-apps",\n'
                        '  "image_name": "checkout-service",\n'
                        '  "tag": "v3.4.1",\n'
                        '  "digest": "sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",\n'
                        '  "scan_status": "SCAN_FINISHED",\n'
                        '  "vulnerabilities": [\n'
                        '    {\n'
                        '      "cve_id": "CVE-2026-1092",\n'
                        '      "package": "openssl",\n'
                        '      "severity": "CRITICAL",\n'
                        '      "cvss_score": 9.1,\n'
                        '      "fix_available": true\n'
                        '    }\n'
                        '  ]\n'
                        '}\n'
                        'EOF\n'
                        'cat <<\'EOF\' > sbom_spdx.json\n'
                        '{\n'
                        '  "spdxVersion": "SPDX-2.3",\n'
                        '  "name": "checkout-service-sbom",\n'
                        '  "packages": [\n'
                        '    {"name": "openssl", "versionInfo": "3.0.2-1ubuntu4"},\n'
                        '    {"name": "gunicorn", "versionInfo": "20.1.0"},\n'
                        '    {"name": "flask", "versionInfo": "2.2.5"}\n'
                        '  ]\n'
                        '}\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Artifact & SBOM Triage Engine\n'
                        'Write a Python tool that resolves the full immutable digest URI, audits the SBOM dependency list, and applies vulnerability acceptance gates:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > audit_artifact.py\n'
                        'import json\n'
                        'import sys\n'
                        '\n'
                        'def audit():\n'
                        '    with open("artifact_metadata.json", "r") as f:\n'
                        '        meta = json.load(f)\n'
                        '    with open("sbom_spdx.json", "r") as f:\n'
                        '        sbom = json.load(f)\n'
                        '\n'
                        '    repo = meta["repository"]\n'
                        '    img = meta["image_name"]\n'
                        '    digest = meta["digest"]\n'
                        '    full_digest_uri = f"{repo}/{img}@{digest}"\n'
                        '\n'
                        '    print("=== Artifact Registry & SBOM Security Audit ===\\n")\n'
                        '    print(f"Resolved Immutable URI: {full_digest_uri}")\n'
                        '    print(f"SBOM Tracked Packages: {len(sbom[\'packages\'])}")\n'
                        '    for p in sbom["packages"]:\n'
                        '        print(f"  - {p[\'name\']} ({p[\'versionInfo\']})")\n'
                        '\n'
                        '    vulns = meta.get("vulnerabilities", [])\n'
                        '    blocked_cves = []\n'
                        '    for v in vulns:\n'
                        '        if v["severity"] == "CRITICAL" and v["fix_available"]:\n'
                        '            blocked_cves.append(v)\n'
                        '\n'
                        '    print(f"\\nVulnerability Scan Findings: {len(vulns)}")\n'
                        '    if blocked_cves:\n'
                        '        print("VERDICT: REJECT - Fixable CRITICAL vulnerabilities present!")\n'
                        '        for b in blocked_cves:\n'
                        '            print(f"  [X] {b[\'cve_id\']} in {b[\'package\']} (CVSS: {b[\'cvss_score\']})")\n'
                        '        admission = "REJECT"\n'
                        '    else:\n'
                        '        print("VERDICT: ACCEPT - All vulnerability thresholds satisfied.")\n'
                        '        admission = "ACCEPT"\n'
                        '\n'
                        '    decision_record = {\n'
                        '        "image_digest_uri": full_digest_uri,\n'
                        '        "admission_decision": admission,\n'
                        '        "blocked_reasons": blocked_cves,\n'
                        '        "sbom_package_count": len(sbom["packages"])\n'
                        '    }\n'
                        '\n'
                        '    with open("artifact_admission_decision.json", "w") as out:\n'
                        '        json.dump(decision_record, out, indent=2)\n'
                        '    print(f"\\nWrote artifact_admission_decision.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    audit()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute Artifact Auditor and Inspect Admission Decision\n'
                        'Run the evaluation tool and inspect the output to verify that the image is rejected due to the fixable critical OpenSSL flaw:\n\n'
                        '```sh\n'
                        'python3 audit_artifact.py\n'
                        'cat artifact_admission_decision.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python artifact auditor capable of resolving immutable image digests, parsing SPDX SBOMs, and enforcing CVE admission gates.',
                'verification': 'Review terminal output of <kbd>python3 audit_artifact.py</kbd> confirming admission decision REJECT and digest resolution.',
                'trouble': 'If JSON loading fails, verify working directory files.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/artifact-audit-lab</kbd>.',
                'file': 'day-114-artifact-registry.md'
            }
        },

        # TOPIC 3
        {
            'key': 'topic-03',
            'title': 'Binary Authorization and attestations',
            'overview': (
                'Binary Authorization is a deploy-time security control for Google Kubernetes Engine (GKE) and Cloud Run that ensures '
                'only trusted, cryptographically signed container images are admitted to production. By requiring that container images '
                'possess valid digital signatures (Attestations) produced by authorized signers (Attestors) using Cloud KMS asymmetric keys, '
                'Binary Authorization prevents unauthorized images, tampered binaries, and unvetted code from running, while providing '
                'auditable break-glass exception procedures for emergency operations.'
            ),
            'preview': (
                'During a high-severity production outage, an emergency bug fix is blocked by Binary Authorization because the automated '
                'signing service is offline, delaying incident remediation until break-glass procedures are initiated.'
            ),
            'technical': (
                'Binary Authorization operates as a Kubernetes Admission Controller webhook on GKE and an enforcement filter on Cloud Run.\n\n'
                '### Core Architectural Components\n'
                '1. **Binary Authorization Policy**:\n'
                '   - Defined at the project level, specifying the default admission rule (`ENFORCEMENT_MODE_ENFORCED` or `DRYRUN_AUDIT_LOG_ONLY`).\n'
                '   - Evaluation options: `ALWAYS_ALLOW`, `ALWAYS_DENY`, or `REQUIRE_ATTESTATION`.\n'
                '   - Whitelists: Can exempt specific trusted registries (e.g. `gcr.io/google-containers/*`) or system components.\n'
                '2. **Attestors & Grafeas Notes**:\n'
                '   - An Attestor represents a trusted verification authority in the CI/CD pipeline (e.g. `quality-gate-attestor`, `security-scan-attestor`).\n'
                '   - Each Attestor binds to a Grafeas Note in Artifact Analysis and references public verification keys.\n'
                '3. **Cloud KMS Cryptographic Signing**:\n'
                '   - Attestations are digitally signed using an asymmetric signing key stored in Cloud KMS (PKIX ECDSA P-256 or RSA-PSS).\n'
                '   - The signature covers the exact SHA-256 content digest of the container image (`us-central1-docker.pkg.dev/...@sha256:...`).\n'
                '   - The signature is stored as an `ATTESTATION` occurrence in Artifact Analysis metadata.\n'
                '4. **Admission Evaluation**:\n'
                '   - When <kbd>kubectl apply</kbd> is executed, the GKE admission webhook intercepts the Pod creation request.\n'
                '   - The admission controller queries Artifact Analysis for valid signatures matching the Attestor’s public key.\n'
                '   - If a valid signature exists for the image digest, the pod is admitted (`ALLOWED`); otherwise, it is rejected with an HTTP 403 Forbidden error.\n'
                '5. **Emergency Break-Glass Procedure**:\n'
                '   - In urgent disaster recovery or critical hotfix scenarios, authorized operators can bypass Binary Authorization by applying the annotation:\n'
                '     `image-policy.k8s.io/break-glass: "true"`.\n'
                '   - The admission controller permits the pod to launch but immediately logs a high-severity Cloud Audit event and dispatches an alert to the SOC.'
            ),
            'questions': [
                'How does Binary Authorization cryptographic signature verification prevent man-in-the-middle container tampering between build and runtime?',
                'Why must asymmetric Cloud KMS keys be used for attestation signing rather than symmetric HMAC keys?',
                'What operational audit trail is generated when an engineer uses the break-glass annotation on GKE?'
            ],
            'reference': 'https://docs.cloud.google.com/binary-authorization/docs',
            'reference_label': 'Google Cloud Binary Authorization Architecture and Attestation Guide',
            'scenario': {
                'symptom': 'Production GKE deployment rejected with `admission webhook "imagepolicywebhook.image-policy.k8s.io" denied the request`.',
                'impact': 'Emergency hotfix blocked during active payment outage; engineers cannot launch patched container pods.',
                'constraints': 'Hotfix must launch within 5 minutes while maintaining full auditable record of the policy bypass.',
                'evidence': (
                    'Kubernetes API Admission Error:\n\n'
                    '```text\n'
                    'Error from server (Forbidden): error when creating "hotfix-deployment.yaml": \n'
                    'admission webhook "imagepolicywebhook.image-policy.k8s.io" denied the request: \n'
                    'Image us-central1-docker.pkg.dev/prod/apps/checkout@sha256:8892bf denied by Binary Authorization policy:\n'
                    'No attestation found matching attestor projects/prod/attestors/sec-scan-attestor.\n'
                    '```\n\n'
                    'Analysis: The automated security scanning pipeline was down, preventing the Attestor from signing the image digest. '
                    'Engineers were unaware of the break-glass procedure needed to bypass the policy during an emergency.'
                ),
                'diagnostic_steps': [
                    'Review the GKE cluster Binary Authorization policy using <kbd>gcloud container binauthz policy export</kbd>.',
                    'Check whether the image digest has any associated attestation occurrences in Artifact Analysis.',
                    'Confirm that the emergency patch is authorized by the Incident Commander.',
                    'Inject the break-glass annotation into the deployment manifest template and re-apply.'
                ],
                'root': 'The automated attestation signer was unreachable, and the operations team had not practiced the emergency break-glass procedure.',
                'fix': 'Apply the break-glass annotation to deploy the emergency hotfix immediately, and restore the Cloud KMS attestation pipeline out-of-band.',
                'residual': 'Break-glass pods must be retroactively scanned and signed once normal pipeline operations are restored.',
                'diagram': (
                    'Automated scanner offline; emergency hotfix lacks cryptographic signature',
                    'GKE Binary Authorization webhook blocks deployment with 403 Forbidden',
                    'Payment outage prolongs due to lack of break-glass procedural knowledge',
                    'Inject image-policy.k8s.io/break-glass annotation into pod manifest',
                    'Pod launches immediately; high-priority break-glass audit alert sent to SOC'
                )
            },
            'lab': {
                'name': 'Binary Authorization Attestation Signer & Break-Glass Evaluator',
                'goal': 'Implement a Python simulation of Binary Authorization that signs container image digests with asymmetric keys, evaluates admission policies, and processes auditable break-glass overrides.',
                'expected': 'A Python Binary Authorization engine verifying cryptographic attestations and processing break-glass exceptions.',
                'mode': 'Python script and CLI data modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/binauthz-lab</kbd>.',
                'steps': [
                    (
                        '#### Generate Container Manifest and Signature Key\n'
                        'Create the working directory and write JSON representations of an admission request, an unsigned emergency image, and a verified image:\n\n'
                        '```sh\n'
                        'mkdir -p ~/binauthz-lab && cd ~/binauthz-lab\n'
                        'cat <<\'EOF\' > admission_requests.json\n'
                        '[\n'
                        '  {\n'
                        '    "request_id": "REQ-001",\n'
                        '    "image_digest": "sha256:112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00",\n'
                        '    "break_glass": false,\n'
                        '    "caller": "cd-service-account@fintech-prod.iam.gserviceaccount.com"\n'
                        '  },\n'
                        '  {\n'
                        '    "request_id": "REQ-002",\n'
                        '    "image_digest": "sha256:998877665544332211ffeeddccbbaa00998877665544332211ffeeddccbbaa00",\n'
                        '    "break_glass": true,\n'
                        '    "caller": "incident-commander@enterprise.com"\n'
                        '  }\n'
                        ']\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Binary Authorization Admission Engine\n'
                        'Write a Python simulation representing the GKE admission webhook. The engine checks for valid attestations, enforces the policy, and audits break-glass overrides:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > binauthz_evaluator.py\n'
                        'import json\n'
                        'from datetime import datetime, timezone\n'
                        '\n'
                        '# Known signed attestations stored in Grafeas/Artifact Analysis\n'
                        'SIGNED_ATTESTATIONS = {\n'
                        '    "sha256:112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00": {\n'
                        '        "attestor": "projects/fintech-prod/attestors/sec-scan-attestor",\n'
                        '        "signature": "VALID_ECDSA_SIG_4892bc"\n'
                        '    }\n'
                        '}\n'
                        '\n'
                        'def evaluate_admission():\n'
                        '    with open("admission_requests.json", "r") as f:\n'
                        '        requests = json.load(f)\n'
                        '\n'
                        '    print("=== GKE Binary Authorization Admission Controller ===\\n")\n'
                        '    results = []\n'
                        '\n'
                        '    for req in requests:\n'
                        '        rid = req["request_id"]\n'
                        '        digest = req["image_digest"]\n'
                        '        bg = req["break_glass"]\n'
                        '        caller = req["caller"]\n'
                        '\n'
                        '        # Step 1: Check break-glass exception\n'
                        '        if bg:\n'
                        '            print(f"[{rid}] BREAK-GLASS OVERRIDE ACTIVATED by {caller}")\n'
                        '            print("  -> Admitting pod under emergency exception")\n'
                        '            print("  -> Emitting HIGH-PRIORITY Cloud Audit Log for SOC\\n")\n'
                        '            results.append({\n'
                        '                "request_id": rid,\n'
                        '                "decision": "ALLOWED_BREAK_GLASS",\n'
                        '                "reason": f"Emergency override invoked by {caller}",\n'
                        '                "audit_alert": True\n'
                        '            })\n'
                        '            continue\n'
                        '\n'
                        '        # Step 2: Evaluate attestations\n'
                        '        if digest in SIGNED_ATTESTATIONS:\n'
                        '            att = SIGNED_ATTESTATIONS[digest]\n'
                        '            print(f"[{rid}] VALID ATTESTATION VERIFIED: {att[\'attestor\']}")\n'
                        '            print("  -> Admitting verified container pod\\n")\n'
                        '            results.append({\n'
                        '                "request_id": rid,\n'
                        '                "decision": "ALLOWED_VERIFIED",\n'
                        '                "reason": f"Signature verified from {att[\'attestor\']}",\n'
                        '                "audit_alert": False\n'
                        '            })\n'
                        '        else:\n'
                        '            print(f"[{rid}] ADMISSION DENIED: No valid attestation found for digest {digest[:20]}...")\n'
                        '            print("  -> Blocking pod deployment (HTTP 403 Forbidden)\\n")\n'
                        '            results.append({\n'
                        '                "request_id": rid,\n'
                        '                "decision": "DENIED",\n'
                        '                "reason": "Missing required attestations",\n'
                        '                "audit_alert": False\n'
                        '            })\n'
                        '\n'
                        '    record = {\n'
                        '        "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),\n'
                        '        "admission_verdicts": results\n'
                        '    }\n'
                        '\n'
                        '    with open("admission_webhook_log.json", "w") as out:\n'
                        '        json.dump(record, out, indent=2)\n'
                        '    print("Admission evaluation completed. Wrote admission_webhook_log.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    evaluate_admission()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute the Admission Evaluator and Verify Break-Glass Handling\n'
                        'Run the Binary Authorization evaluator and inspect the output to confirm that the verified image is admitted and the break-glass request is permitted with an audit alert:\n\n'
                        '```sh\n'
                        'python3 binauthz_evaluator.py\n'
                        'cat admission_webhook_log.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python Binary Authorization simulation verifying cryptographic attestations and executing auditable emergency break-glass exceptions.',
                'verification': 'Review terminal output of <kbd>python3 binauthz_evaluator.py</kbd> confirming ALLOWED_VERIFIED for REQ-001 and ALLOWED_BREAK_GLASS for REQ-002.',
                'trouble': 'If JSON file syntax error occurs, verify dictionary structure in `admission_requests.json`.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/binauthz-lab</kbd>.',
                'file': 'day-114-binauthz-admission.md'
            }
        }
    ]
}
