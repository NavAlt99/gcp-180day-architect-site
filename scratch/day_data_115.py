"""day_data_115.py — Exhaustive architecture data specification for Day 115.

Covers SLSA Levels, Software Supply Chain Concepts & SBOMs,
Secrets Management in CI/CD Pipelines, and
Container Hardening (Distroless Images, Non-Root Execution, Read-Only Filesystems).
"""

DAY_NUM = 115

DATA = {
    'day': 115,
    'part1_intro': (
        'Day 115 establishes container workload hardening, software supply chain security standards (SLSA), '
        'and secure CI/CD pipeline architecture across Google Cloud. Enterprise architects examine the Supply-chain '
        'Levels for Software Artifacts (SLSA v1.0) framework and build provenance generation in Cloud Build, '
        'zero-trust secrets governance across build and deploy pipelines (preventing secrets leaks in image layers), '
        'and defense-in-depth container runtime hardening using Google Distroless base images, non-root user execution, '
        'and read-only root filesystems.'
    ),
    'exit_summary': (
        'A hardened manifest/image diff and explanation of SBOM, provenance and remaining runtime risks.'
    ),
    'part2_intro': (
        'The technical comparison below contrasts container base image patterns, build isolation levels, '
        'secret injection mechanisms, and runtime security postures across production workload architectures.'
    ),
    'arch_table_html': (
        '<div class="table-container">\n'
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Hardening Dimension</th>\n'
        '<th>Traditional Anti-Pattern</th>\n'
        '<th>Hardened Production Pattern</th>\n'
        '<th>GCP Implementation &amp; Tooling</th>\n'
        '<th>Residual Runtime Risk</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td><strong>1. Supply Chain Integrity</strong></td>\n'
        '<td>Unsigned manual local builds pushed to registry</td>\n'
        '<td>SLSA Level 3 hermetic build provenance</td>\n'
        '<td>Cloud Build signed in-toto provenance &amp; slsa-verifier</td>\n'
        '<td>Compromise of upstream source git repository prior to build trigger.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>2. Base Image Footprint</strong></td>\n'
        '<td>Full Linux OS distributions (Ubuntu, Debian) with package managers</td>\n'
        '<td>Google Distroless container images (no shell, no apt)</td>\n'
        '<td>gcr.io/distroless/static-debian12, distroless/python3</td>\n'
        '<td>Application runtime memory flaws (e.g. buffer overflows) remain exploitable.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>3. User Privilege Boundary</strong></td>\n'
        '<td>Containers running as UID 0 (root) by default</td>\n'
        '<td>Dedicated non-root user (e.g. UID 65532:65532)</td>\n'
        '<td>`securityContext.runAsNonRoot: true`, `runAsUser: 65532`</td>\n'
        '<td>Kernel vulnerability escapes affecting the host Linux kernel.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>4. Filesystem Immutability</strong></td>\n'
        '<td>Writable root filesystem allowing malware drop</td>\n'
        '<td>Strict read-only root filesystem with ephemeral tmpfs</td>\n'
        '<td>`readOnlyRootFilesystem: true`, `emptyDir: {medium: "Memory"}`</td>\n'
        '<td>Attacker can still manipulate data written to explicit tmpfs mounts.</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td><strong>5. CI/CD Secret Lifecycle</strong></td>\n'
        '<td>Hardcoded credentials or `ARG`/`ENV` secrets in Dockerfile</td>\n'
        '<td>Dynamic runtime secret mounts via Secret Manager</td>\n'
        '<td>Secret Manager CSI Driver, Cloud Build `availableSecrets`</td>\n'
        '<td>Overly permissive IAM roles allowing service accounts to read unrelated secrets.</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    ),
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 115: SLSA Level 3 Provenance, Secret Isolation, and Container Hardening Topology',
        'desc': 'Architectural layout illustrating Cloud Build SLSA provenance generation, Secret Manager integration, Distroless container packaging, and GKE non-root admission enforcement.',
        'caption': 'Figure 115.1: End-to-end container hardening architecture featuring hermetic Cloud Build workers, in-toto SLSA attestations, Secret Manager CSI injection, and non-root read-only runtime pods.',
        'width': 1100,
        'height': 640,
        'layers': [
            {
                'name': 'LAYER 1: Source Control & SLSA Provenance Verification Plane',
                'desc': 'Signed git commits, tamper-evident webhook triggers, and SLSA Level 3 build provenance',
                'y': 10,
                'h': 90,
                'stroke': '#38bdf8',
                'fill': '#0c1e38',
                'title_color': '#38bdf8'
            },
            {
                'name': 'LAYER 2: Cloud Build Isolated Worker & Secret Manager Integration',
                'desc': 'Ephemeral build environments, Secret Manager dynamic injection, and Dockerfile multi-stage builds',
                'y': 115,
                'h': 90,
                'stroke': '#818cf8',
                'fill': '#141838',
                'title_color': '#818cf8'
            },
            {
                'name': 'LAYER 3: Distroless Container Packaging & Immutable Digest Minters',
                'desc': 'Google Distroless base images, elimination of shells/package managers, and SHA-256 digest creation',
                'y': 220,
                'h': 90,
                'stroke': '#f59e0b',
                'fill': '#261a08',
                'title_color': '#f59e0b'
            },
            {
                'name': 'LAYER 4: Artifact Registry & SPDX SBOM Metadata Vault',
                'desc': 'Continuous vulnerability scanning, SBOM dependency trees, and signed provenance attestations',
                'y': 325,
                'h': 90,
                'stroke': '#f43f5e',
                'fill': '#2a0a14',
                'title_color': '#f43f5e'
            },
            {
                'name': 'LAYER 5: GKE Hardened Runtime & Security Context Boundary',
                'desc': 'Non-root execution (UID 65532), read-only root filesystems, dropped capabilities, and tmpfs scratch',
                'y': 430,
                'h': 90,
                'stroke': '#22c55e',
                'fill': '#072417',
                'title_color': '#22c55e'
            }
        ],
        'components': [
            {'name': 'Signed Git Repository', 'detail': 'SLSA Source Tracked', 'x': 80, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'SLSA L3 Provenance', 'detail': 'in-toto Attestation Minter', 'x': 420, 'y': 30, 'w': 260, 'h': 52, 'stroke': '#38bdf8', 'fill': '#0e294b'},
            {'name': 'Cloud Build Worker', 'detail': 'Ephemeral VM Isolation', 'x': 80, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Secret Manager Mount', 'detail': 'No Layer Leakage', 'x': 420, 'y': 135, 'w': 260, 'h': 52, 'stroke': '#818cf8', 'fill': '#191c4d'},
            {'name': 'Distroless Image Base', 'detail': 'Zero Shell / Zero Package Mgr', 'x': 80, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Immutable Digest Minter', 'detail': '@sha256 Content Addressed', 'x': 420, 'y': 240, 'w': 260, 'h': 52, 'stroke': '#f59e0b', 'fill': '#38230a'},
            {'name': 'Artifact Registry Repo', 'detail': 'Vulnerability Analysis Active', 'x': 80, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'SPDX SBOM Index', 'detail': 'Transitive Dependency Tree', 'x': 420, 'y': 345, 'w': 260, 'h': 52, 'stroke': '#f43f5e', 'fill': '#3d101d'},
            {'name': 'Non-Root Pod Context', 'detail': 'runAsUser: 65532', 'x': 80, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'},
            {'name': 'Read-Only Filesystem', 'detail': 'Tmpfs Scratch Mounted', 'x': 420, 'y': 450, 'w': 260, 'h': 52, 'stroke': '#22c55e', 'fill': '#0b3824'}
        ],
        'boundaries': [
            {'label': 'SUPPLY CHAIN PROVENANCE & BUILD SECURITY BOUNDARY', 'x': 60, 'y': 20, 'w': 640, 'h': 195, 'color': '#38bdf8'},
            {'label': 'IMMUTABLE PACKAGING & VULNERABILITY AUDIT DOMAIN', 'x': 60, 'y': 230, 'w': 640, 'h': 195, 'color': '#f59e0b'},
            {'label': 'HARDENED RUNTIME WORKLOAD SECURITY ENCLAVE', 'x': 60, 'y': 440, 'w': 640, 'h': 195, 'color': '#22c55e'}
        ],
        'flows': [
            {'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'label': 'Attest Git Commit Hash', 'type': 'ok'},
            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'label': 'Dispatch Ephemeral Build', 'type': 'ok'},
            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'label': 'Inject Secret at Runtime', 'type': 'ok'},
            {'x1': 210, 'y1': 187, 'x2': 210, 'y2': 240, 'label': 'Package into Distroless', 'type': 'ok'},
            {'x1': 340, 'y1': 266, 'x2': 420, 'y2': 266, 'label': 'Mint SHA-256 Digest', 'type': 'ok'},
            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'label': 'Push to Artifact Registry', 'type': 'ok'},
            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'label': 'Generate SPDX SBOM', 'type': 'ok'},
            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'label': 'Deploy Hardened Pod', 'type': 'ok'},
            {'x1': 340, 'y1': 476, 'x2': 420, 'y2': 476, 'label': 'Lock Read-Only Root FS', 'type': 'ok'}
        ],
        'probes': [
            {'cx': 80, 'cy': 135, 'label': 'PROBE 1: Build Layer Audit: Zero Hardcoded Secret Invariants', 'badge': 'P1', 'color': '#38bdf8'},
            {'cx': 80, 'cy': 240, 'label': 'PROBE 2: Binary Analysis: Zero Package Managers or Shell Binaries', 'badge': 'P2', 'color': '#f59e0b'},
            {'cx': 80, 'cy': 450, 'label': 'PROBE 3: Runtime Security Context: Verify UID != 0 & Read-Only FS', 'badge': 'P3', 'color': '#22c55e'}
        ]
    },
    'part3_intro': (
        'The following field investigations analyze real-world software supply chain compromises, leaked container layer secrets, '
        'and container escape vulnerabilities resulting from running as root with writable filesystems. '
        'Each scenario details verbatim diagnostic logs, root cause mechanisms, production remediation scripts, and dual-lane failed/corrected flow diagrams.'
    ),
    'part4_intro': (
        'These hands-on architectural exercises implement the complete operational engineering lifecycle for Day 115. '
        'Architects author an in-toto SLSA Level 3 build provenance validator, inspect container image layer histories for secret leakage, '
        'and construct a hardened multi-stage Distroless Dockerfile paired with a Kubernetes read-only non-root security context manifest.'
    ),
    'topics': [
        # TOPIC 1
        {
            'key': 'topic-01',
            'title': 'SLSA levels, software supply chain concepts, SBOMs',
            'overview': (
                'The Supply-chain Levels for Software Artifacts (SLSA) framework provides a comprehensive specification for software supply chain '
                'integrity. As modern attacks shift from exploiting production vulnerabilities to poisoning upstream dependencies and build systems, '
                'organizations must establish verifiable provenance for every container artifact. Google Cloud Build supports SLSA Level 3 compliance '
                'out of the box, generating signed in-toto provenance metadata detailing the source repository, commit hash, builder identity, '
                'and compilation parameters.'
            ),
            'preview': (
                'A rogue dependency update injects malicious code during build time; because build provenance is absent, security teams cannot '
                'determine which production container digests contain the poisoned commit.'
            ),
            'technical': (
                'Securing the software supply chain requires cryptographic traceability across code, dependencies, build systems, and deployment engines.\n\n'
                '### SLSA Framework Levels & Invariants\n'
                '1. **SLSA Build Level 1 (Build Script & Provenance)**:\n'
                '   - The build process is automated via a build script (e.g. `cloudbuild.yaml`).\n'
                '   - Provenance is generated, describing how the artifact was produced and listing top-level inputs.\n'
                '2. **SLSA Build Level 2 (Hosted Build Service & Signed Provenance)**:\n'
                '   - The build runs on a dedicated hosted service (Cloud Build) rather than an individual developer workstation.\n'
                '   - Provenance is generated and digitally signed directly by the build platform using a platform-managed key.\n'
                '3. **SLSA Build Level 3 (Hardened & Hermetic Isolation)**:\n'
                '   - The build executes in an ephemeral, isolated environment (Cloud Build isolated worker pool) preventing cross-build contamination.\n'
                '   - Hermetic builds ensure all inputs, compilers, and dependencies are explicitly declared and resolved before execution.\n'
                '   - Provenance is verifiable independently: users can verify the cryptographic signature using tools like `slsa-verifier` against Google’s public certificate authority.\n\n'
                '### Software Bill of Materials (SBOM)\n'
                '- **Standardized Formats**: SPDX (Software Package Data Exchange) and CycloneDX.\n'
                '- **Granular Inventory**: Documents every OS package (dpkg, rpm, apk) and language runtime library (npm, PyPI, Maven, Go modules) embedded in the container.\n'
                '- **Vulnerability Correlation**: When a new zero-day (such as CVE-2026-X) is disclosed, security teams query the SBOM database in Artifact Analysis to identify every affected image digest in seconds, without needing to perform slow filesystem scans across running pods.'
            ),
            'questions': [
                'What specific threats does SLSA Level 3 build provenance mitigate that traditional unit testing and SAST scanning miss?',
                'How does an in-toto signed provenance statement allow admission controllers to verify that an image was compiled strictly from an authorized GitHub commit?',
                'What is the operational advantage of storing SPDX SBOM metadata alongside container image digests in Artifact Registry?'
            ],
            'reference': 'https://slsa.dev/spec/',
            'reference_label': 'Supply-chain Levels for Software Artifacts (SLSA) Specification',
            'scenario': {
                'symptom': 'Production cluster runs an unauthorized container build containing code that never existed in the official Git repository.',
                'impact': 'Backdoor embedded in API server; attacker exfiltrates database records via hidden HTTP endpoint; origin of build unknown.',
                'constraints': 'All production workloads must prove SLSA Level 3 provenance originating from the main branch before admission.',
                'evidence': (
                    'Container Admission Verification failure:\n\n'
                    '```text\n'
                    'ERROR: Verification failed for us-central1-docker.pkg.dev/prod/api@sha256:d82bf1\n'
                    'slsa-verifier: no in-toto provenance attestation found.\n'
                    'Builder Identity: UNKNOWN (Built locally on developer workstation)\n'
                    'Source Commit: UNVERIFIABLE\n'
                    '```\n\n'
                    'Analysis: An engineer built and pushed a container image directly from their local laptop using personal credentials, '
                    'bypassing Cloud Build and injecting unreviewed testing code into production.'
                ),
                'diagnostic_steps': [
                    'Extract the container image digest from the running Kubernetes pod manifest.',
                    'Execute <kbd>gcloud artifacts docker images describe [DIGEST] --show-provenance</kbd> to inspect provenance metadata.',
                    'Check Artifact Registry IAM policies to identify which identities have `roles/artifactregistry.writer` permissions.',
                    'Verify that Binary Authorization policies enforce `slsa-provenance` attestations.'
                ],
                'root': 'Artifact Registry allowed direct image pushes from developer user accounts, allowing untracked local builds to bypass Cloud Build SLSA provenance generation.',
                'fix': 'Revoke human write access to production Artifact Registry repositories, restrict image pushing strictly to the Cloud Build service account, and enforce SLSA Level 3 verification in Binary Authorization.',
                'residual': 'Compromised developer credentials with git push access could still commit malicious code directly to source control.',
                'diagram': (
                    'Developer builds container locally on laptop and pushes directly to registry',
                    'Image lacks SLSA provenance and build metadata; unreviewed code deployed',
                    'Hidden backdoor activates in production; forensic team cannot trace origin',
                    'Restrict registry write access to Cloud Build; enforce SLSA L3 verification',
                    'Only images built in hermetic Cloud Build pipelines with signed provenance admitted'
                )
            },
            'lab': {
                'name': 'SLSA Build Provenance Generator & In-Toto Validator',
                'goal': 'Implement a Python SLSA Level 3 provenance parser and verification engine that inspects in-toto build statements, verifies builder identities, and enforces repository commit traceability.',
                'expected': 'A Python SLSA validation script verifying cryptographic provenance invariants and detecting untrusted build origins.',
                'mode': 'Python script and CLI data modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/slsa-provenance-lab</kbd>.',
                'steps': [
                    (
                        '#### Generate Synthetic SLSA in-toto Provenance Payload\n'
                        'Create the working directory and write a simulated in-toto SLSA Level 3 provenance statement and an unsigned artifact metadata file:\n\n'
                        '```sh\n'
                        'mkdir -p ~/slsa-provenance-lab && cd ~/slsa-provenance-lab\n'
                        'cat <<\'EOF\' > slsa_provenance.json\n'
                        '{\n'
                        '  "_type": "https://in-toto.io/Statement/v0.1",\n'
                        '  "subject": [\n'
                        '    {\n'
                        '      "name": "us-central1-docker.pkg.dev/fintech-prod/apps/payment-api",\n'
                        '      "digest": {\n'
                        '        "sha256": "8a72b91c89f1d0123456789abcdef0123456789abcdef0123456789abcdef012"\n'
                        '      }\n'
                        '    }\n'
                        '  ],\n'
                        '  "predicateType": "https://slsa.dev/provenance/v0.2",\n'
                        '  "predicate": {\n'
                        '    "builder": {\n'
                        '      "id": "https://cloudbuild.googleapis.com/GoogleHostedWorker"\n'
                        '    },\n'
                        '    "buildType": "https://cloudbuild.googleapis.com/CloudBuildYaml@v1",\n'
                        '    "invocation": {\n'
                        '      "configSource": {\n'
                        '        "uri": "git+https://github.com/fintech-enterprise/payment-api",\n'
                        '        "digest": {\n'
                        '          "sha1": "7c9a12b4e5f67890123456789012345678901234"\n'
                        '        },\n'
                        '        "entryPoint": "cloudbuild.yaml"\n'
                        '      }\n'
                        '    },\n'
                        '    "buildConfig": {\n'
                        '      "slsaLevel": 3,\n'
                        '      "hermetic": true\n'
                        '    }\n'
                        '  }\n'
                        '}\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the SLSA Provenance Verification Tool\n'
                        'Write a Python tool that evaluates the provenance document against enterprise supply chain policies (builder ID, git repository URI, and hermetic invariants):\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > verify_slsa.py\n'
                        'import json\n'
                        'import sys\n'
                        '\n'
                        'TRUSTED_BUILDER = "https://cloudbuild.googleapis.com/GoogleHostedWorker"\n'
                        'TRUSTED_REPO_PREFIX = "git+https://github.com/fintech-enterprise/"\n'
                        '\n'
                        'def verify_provenance():\n'
                        '    with open("slsa_provenance.json", "r") as f:\n'
                        '        statement = json.load(f)\n'
                        '\n'
                        '    print("=== Verifying SLSA Level 3 Build Provenance ===\\n")\n'
                        '    pred = statement.get("predicate", {})\n'
                        '    builder_id = pred.get("builder", {}).get("id")\n'
                        '    repo_uri = pred.get("invocation", {}).get("configSource", {}).get("uri", "")\n'
                        '    commit = pred.get("invocation", {}).get("configSource", {}).get("digest", {}).get("sha1", "")\n'
                        '    slsa_level = pred.get("buildConfig", {}).get("slsaLevel", 0)\n'
                        '    hermetic = pred.get("buildConfig", {}).get("hermetic", False)\n'
                        '\n'
                        '    violations = []\n'
                        '    if builder_id != TRUSTED_BUILDER:\n'
                        '        violations.append(f"UNTRUSTED BUILDER: {builder_id} (Expected {TRUSTED_BUILDER})")\n'
                        '    if not repo_uri.startswith(TRUSTED_REPO_PREFIX):\n'
                        '        violations.append(f"UNTRUSTED REPO: {repo_uri}")\n'
                        '    if slsa_level < 3:\n'
                        '        violations.append(f"INSUFFICIENT SLSA LEVEL: Level {slsa_level} (Requires Level 3)")\n'
                        '    if not hermetic:\n'
                        '        violations.append("NON-HERMETIC BUILD: Dependencies not isolated")\n'
                        '\n'
                        '    print(f"Artifact Subject: {statement[\'subject\'][0][\'name\']}")\n'
                        '    print(f"Digest: {statement[\'subject\'][0][\'digest\'][\'sha256\']}")\n'
                        '    print(f"Builder ID: {builder_id}")\n'
                        '    print(f"Source Git Commit: {commit}")\n'
                        '    print(f"Evaluated SLSA Level: {slsa_level} (Hermetic: {hermetic})\\n")\n'
                        '\n'
                        '    if violations:\n'
                        '        print("VERDICT: PROVENANCE VERIFICATION FAILED [!]")\n'
                        '        for v in violations:\n'
                        '            print(f"  - {v}")\n'
                        '        verdict = "REJECT"\n'
                        '    else:\n'
                        '        print("VERDICT: PROVENANCE VERIFIED (SLSA L3 Compliant) [OK]")\n'
                        '        verdict = "ACCEPT"\n'
                        '\n'
                        '    report = {\n'
                        '        "verdict": verdict,\n'
                        '        "builder": builder_id,\n'
                        '        "source_commit": commit,\n'
                        '        "slsa_level": slsa_level,\n'
                        '        "violations": violations\n'
                        '    }\n'
                        '    with open("slsa_verification_report.json", "w") as out:\n'
                        '        json.dump(report, out, indent=2)\n'
                        '    print("\\nWrote slsa_verification_report.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    verify_provenance()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute the SLSA Validator and Inspect Verification Output\n'
                        'Run the verification tool and inspect the generated report to confirm that the build provenance fulfills all SLSA Level 3 invariants:\n\n'
                        '```sh\n'
                        'python3 verify_slsa.py\n'
                        'cat slsa_verification_report.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python SLSA provenance verification tool confirming in-toto build metadata, builder identity, and hermetic compilation invariants.',
                'verification': 'Review terminal output of <kbd>python3 verify_slsa.py</kbd> confirming VERDICT: PROVENANCE VERIFIED (SLSA L3 Compliant).',
                'trouble': 'If JSON loading fails, verify file creation in working directory.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/slsa-provenance-lab</kbd>.',
                'file': 'day-115-slsa-provenance.md'
            }
        },

        # TOPIC 2
        {
            'key': 'topic-02',
            'title': 'Secrets in CI/CD (never in code or images)',
            'overview': (
                'Securing sensitive credentials, private keys, and API tokens across the Continuous Integration and Continuous Deployment '
                'lifecycle requires eliminating static secrets from source code, Dockerfiles, and intermediate container filesystem layers. '
                'Google Cloud provides integrated secrets governance through Secret Manager, Cloud Build native secret bindings, and '
                'Docker BuildKit secret mounts, ensuring credentials exist strictly in ephemeral memory during execution and never persist '
                'into published container images.'
            ),
            'preview': (
                'A developer passes an enterprise GitHub personal access token using a standard `ARG GITHUB_TOKEN` in a Dockerfile; '
                'the token is exposed to all developers who pull the resulting image via <kbd>docker history</kbd> inspection.'
            ),
            'technical': (
                'Container image layers are immutable tar archives. Merely deleting a file in a subsequent Dockerfile instruction does not '
                'remove it from the image—the file remains permanently embedded in the earlier intermediate layer history.\n\n'
                '### Anti-Patterns vs Secure Ingestion Patterns\n'
                '1. **Anti-Pattern 1: Dockerfile `ENV` or `ARG` Secrets**:\n'
                '   - Using `ARG NPM_TOKEN` or `ENV DB_PASSWORD=xyz` persists the variable directly into image manifest metadata and filesystem layer diffs.\n'
                '   - Anyone with read access to the image can execute <kbd>docker history --no-trunc [IMAGE]</kbd> or inspect layer tarballs to recover the secret in cleartext.\n'
                '2. **Anti-Pattern 2: `COPY`ing Secret Files then `rm`ing Them**:\n'
                '   - Executing `COPY id_rsa /root/.ssh/id_rsa && npm install && rm /root/.ssh/id_rsa` creates a persistent image layer containing the private SSH key.\n'
                '3. **Secure Pattern 1: Cloud Build Native Secret Manager Integration**:\n'
                '   - In `cloudbuild.yaml`, declare `availableSecrets` referencing Secret Manager resource URIs.\n'
                '   - Map secrets directly to environment variables or secret volumes attached exclusively to designated build steps:\n'
                '   ```yaml\n'
                '   availableSecrets:\n'
                '     secretManager:\n'
                '     - versionName: projects/$PROJECT_ID/secrets/npm-token/versions/latest\n'
                '       env: \'NPM_TOKEN\'\n'
                '   ```\n'
                '4. **Secure Pattern 2: BuildKit Build-Time Secret Mounts**:\n'
                '   - Use Docker BuildKit syntax `# syntax=docker/dockerfile:1.4` and mount secrets at compile time:\n'
                '   `RUN --mount=type=secret,id=npm_token npm install`.\n'
                '   - The secret file is mounted in memory strictly for the duration of the command and is never committed to any layer.\n'
                '5. **Secure Pattern 3: Runtime Workload Identity & CSI Secret Store**:\n'
                '   - In production GKE, avoid baking secrets into container environments altogether. Inject secrets dynamically at runtime '
                '   using the Secret Manager CSI Driver mounting secrets as volatile in-memory `tmpfs` volumes.'
            ),
            'questions': [
                'Why does executing `RUN rm /secret.key` in a Dockerfile fail to eliminate the secret from the published container image?',
                'How does Docker BuildKit `--mount=type=secret` guarantee that temporary credentials are never stored in intermediate layer tarballs?',
                'What is the operational function of the Secret Manager CSI Driver in eliminating static Kubernetes secret objects from etcd?'
            ],
            'reference': 'https://docs.cloud.google.com/binary-authorization/docs',
            'reference_label': 'Google Cloud Secret Manager and Cloud Build Integration Guide',
            'scenario': {
                'symptom': 'Security audit discovers production database master passwords exposed in public container registry layers.',
                'impact': 'Third-party auditors discover active database credentials using <kbd>docker history</kbd>; immediate emergency database password rotation mandated.',
                'constraints': 'CI/CD pipeline must fail immediately if any `ARG` or `ENV` instruction contains sensitive keywords.',
                'evidence': (
                    'Docker history inspection output:\n\n'
                    '```text\n'
                    'IMAGE          CREATED        CREATED BY                                      SIZE\n'
                    '8a72b91c89f1   2 hours ago    ARG DB_PASS=super_secret_pg_pass_99201           0B\n'
                    '3e41c098a72b   2 hours ago    ENV DATABASE_URL=postgresql://admin:$DB_PASS@... 0B\n'
                    '```\n\n'
                    'Analysis: The build script passed credentials via Docker build-args, permanently baking the secret into the image metadata.'
                ),
                'diagnostic_steps': [
                    'Execute <kbd>docker history --no-trunc [IMAGE_NAME]</kbd> to inspect the full compilation command history.',
                    'Review the Dockerfile source code for `ARG` and `ENV` statements matching credential patterns.',
                    'Check Secret Manager to verify if an existing managed secret was bypassed.',
                    'Audit Cloud Build step logs to see how variables were passed to the <kbd>docker build</kbd> command.'
                ],
                'root': 'Developers used `ARG` and `ENV` instructions in Dockerfiles to configure database connections, permanently exposing credentials in container layer metadata.',
                'fix': 'Refactor the Dockerfile to eliminate `ARG`/`ENV` secrets, configure Cloud Build `availableSecrets` with Secret Manager, and inject credentials dynamically at runtime via Secret Manager CSI.',
                'residual': 'Application logs emitted during runtime startup must be audited to ensure credentials are not dumped to stdout.',
                'diagram': (
                    'Developer passes database password via ARG instruction in Dockerfile',
                    'Docker engine bakes password into image layer metadata and history',
                    'Security auditor inspects container history and recovers database password',
                    'Refactor build to use Secret Manager and BuildKit --mount=type=secret',
                    'Secrets kept strictly in memory during build; zero credentials stored in layers'
                )
            },
            'lab': {
                'name': 'Container Image Layer Secret Auditor & BuildKit Sanitizer',
                'goal': 'Implement a Python container layer inspection script that analyzes image layer metadata, detects exposed secrets in Docker history, and validates declarative Secret Manager CI/CD configurations.',
                'expected': 'A Python security tool detecting embedded layer secrets and validating hardened Dockerfile configurations.',
                'mode': 'Python script and CLI data modeling',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/cicd-secrets-lab</kbd>.',
                'steps': [
                    (
                        '#### Generate Synthetic Docker Layer History Manifest\n'
                        'Create the working directory and write JSON representations of an insecure container image layer history and a hardened multi-stage build manifest:\n\n'
                        '```sh\n'
                        'mkdir -p ~/cicd-secrets-lab && cd ~/cicd-secrets-lab\n'
                        'cat <<\'EOF\' > image_history.json\n'
                        '[\n'
                        '  {\n'
                        '    "layer_id": "sha256:layer-001",\n'
                        '    "created_by": "/bin/sh -c #(nop) ADD file:abc in /",\n'
                        '    "size": 45000000\n'
                        '  },\n'
                        '  {\n'
                        '    "layer_id": "sha256:layer-002",\n'
                        '    "created_by": "|1 GITHUB_TOKEN=ghp_992019482019481029384756 /bin/sh -c npm install",\n'
                        '    "size": 12500000\n'
                        '  },\n'
                        '  {\n'
                        '    "layer_id": "sha256:layer-003",\n'
                        '    "created_by": "ENV DB_PASSWORD=prod_pg_password_9921",\n'
                        '    "size": 0\n'
                        '  }\n'
                        ']\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement the Layer History Secret Scanner\n'
                        'Write a Python tool that inspects the layer history, identifies leaked credentials, and evaluates a declarative `cloudbuild.yaml` for native Secret Manager integration:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > scan_layer_secrets.py\n'
                        'import json\n'
                        'import re\n'
                        'import sys\n'
                        '\n'
                        'SECRET_REGEXES = [\n'
                        '    (re.compile(r"GITHUB_TOKEN=[a-zA-Z0-9_-]+"), "Exposed GitHub Personal Access Token"),\n'
                        '    (re.compile(r"DB_PASSWORD=[a-zA-Z0-9_-]+"), "Exposed Database Password in ENV"),\n'
                        '    (re.compile(r"ghp_[a-zA-Z0-9]{36}"), "GitHub Token Pattern")\n'
                        ']\n'
                        '\n'
                        'def inspect_layers():\n'
                        '    with open("image_history.json", "r") as f:\n'
                        '        layers = json.load(f)\n'
                        '\n'
                        '    print("=== Container Image Layer History Secret Audit ===\\n")\n'
                        '    findings = []\n'
                        '\n'
                        '    for idx, layer in enumerate(layers, 1):\n'
                        '        cmd = layer.get("created_by", "")\n'
                        '        lid = layer.get("layer_id", "")\n'
                        '        for pattern, desc in SECRET_REGEXES:\n'
                        '            match = pattern.search(cmd)\n'
                        '            if match:\n'
                        '                findings.append({\n'
                        '                    "layer_index": idx,\n'
                        '                    "layer_id": lid,\n'
                        '                    "finding": desc,\n'
                        '                    "snippet": match.group(0)[:30] + "..."\n'
                        '                })\n'
                        '\n'
                        '    print(f"Total Layers Analyzed: {len(layers)}")\n'
                        '    print(f"Secret Exposures Discovered: {len(findings)}\\n")\n'
                        '    for f in findings:\n'
                        '        print(f"[CRITICAL] Layer #{f[\'layer_index\']} ({f[\'layer_id\']}):")\n'
                        '        print(f"  Type: {f[\'finding\']}")\n'
                        '        print(f"  Snippet: {f[\'snippet\']}\\n")\n'
                        '\n'
                        '    verdict = "REJECT" if findings else "PASS"\n'
                        '    report = {\n'
                        '        "verdict": verdict,\n'
                        '        "findings_count": len(findings),\n'
                        '        "findings": findings\n'
                        '    }\n'
                        '    with open("layer_audit_report.json", "w") as out:\n'
                        '        json.dump(report, out, indent=2)\n'
                        '    print(f"Audit completed with verdict: {verdict}. Wrote layer_audit_report.json.")\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    inspect_layers()\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Execute Layer Scanner and Inspect Audit Report\n'
                        'Run the scanner and inspect the output to verify that leaked build-args and ENV credentials are detected and rejected:\n\n'
                        '```sh\n'
                        'python3 scan_layer_secrets.py\n'
                        'cat layer_audit_report.json\n'
                        '```'
                    )
                ],
                'accept': 'Validated Python container layer scanner identifying embedded secrets in image build histories and enforcing Secret Manager best practices.',
                'verification': 'Review terminal output of <kbd>python3 scan_layer_secrets.py</kbd> confirming discovery of GitHub token and database password with verdict REJECT.',
                'trouble': 'If JSON file cannot be loaded, verify syntax of `image_history.json`.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/cicd-secrets-lab</kbd>.',
                'file': 'day-115-cicd-secrets.md'
            }
        },

        # TOPIC 3
        {
            'key': 'topic-03',
            'title': 'Container hardening (distroless images, non-root users, read-only filesystems)',
            'overview': (
                'Container runtime hardening establishes defense-in-depth within Kubernetes pods, ensuring that even if an attacker '
                'achieves remote code execution through an application-level vulnerability, they are trapped in a restricted, unprivileged '
                'sandbox. Enterprise container hardening rests on three fundamental pillars: Google Distroless base images (eliminating shells '
                'and package managers), enforcing non-root user execution (preventing root privilege escalation), and locking the container '
                'filesystem in read-only mode with dedicated temporary memory scratch spaces.'
            ),
            'preview': (
                'An attacker exploits an arbitrary code execution vulnerability in a Node.js web pod; because the container runs as root with '
                'a writable root filesystem, the attacker downloads a cryptominer binary and establishes a persistence backdoor.'
            ),
            'technical': (
                'Container hardening dramatically reduces the attack surface and renders common post-exploitation tactics ineffective.\n\n'
                '### The Three Pillars of Container Hardening\n'
                '1. **Google Distroless Container Images**:\n'
                '   - Standard base images (Ubuntu, Debian, Alpine) contain hundreds of unnecessary utilities: package managers (`apt`, `apk`), '
                '   interactive shells (`/bin/sh`, `/bin/bash`), network tools (`curl`, `wget`, `nc`), and system libraries.\n'
                '   - Google Distroless images (`gcr.io/distroless/static-debian12`, `distroless/python3`, `distroless/java17-debian12`) contain '
                '   **only** the application binary, its runtime dependencies, and minimal root certificates.\n'
                '   - Without a shell or package manager, attackers cannot execute shell injection payloads, download second-stage malware, or spawn reverse shells.\n'
                '2. **Non-Root User Execution**:\n'
                '   - By default, containers run as UID 0 (`root`). If a container escapes or mounts host paths, root in the container can compromise the host kernel.\n'
                '   - In the Dockerfile: Specify a high-numbered non-root UID (e.g. `USER 65532:65532` in Distroless, or `USER 10001:10001`).\n'
                '   - In the Kubernetes Manifest: Enforce `securityContext.runAsNonRoot: true` and `securityContext.runAsUser: 65532`. Policy Controller admission webhooks reject any manifest omitting these fields.\n'
                '3. **Read-Only Root Filesystem with tmpfs Scratch**:\n'
                '   - Enforcing `securityContext.readOnlyRootFilesystem: true` locks the container filesystem in read-only mode.\n'
                '   - Attackers cannot write binaries to `/tmp`, modify configuration files in `/etc`, or overwrite web assets in `/var/www`.\n'
                '   - Applications requiring writable scratch space (for temporary buffers or PID files) mount ephemeral `emptyDir` volumes backed by RAM (`medium: "Memory"`).'
            ),
            'questions': [
                'How does eliminating shells (`/bin/sh`, `/bin/bash`) in Distroless base images prevent command injection exploitation?',
                'Why is running as non-root critical even when containers operate inside isolated Linux namespaces?',
                'What is the operational pattern for supporting applications that require temporary scratch files while enforcing a read-only root filesystem?'
            ],
            'reference': 'https://docs.cloud.google.com/binary-authorization/docs',
            'reference_label': 'Google Cloud Container Workload Hardening and Distroless Guide',
            'scenario': {
                'symptom': 'Web pod compromised via command injection; attacker downloads malware binary to /tmp and runs it as root.',
                'impact': 'Attacker modifies cluster node configuration and pivots laterally; incident detection delayed due to standard shell usage.',
                'constraints': 'All production pods must run as non-root with read-only root filesystems and zero installed shell binaries.',
                'evidence': (
                    'Runtime Container Threat Detection finding:\n\n'
                    '```json\n'
                    '{\n'
                    '  "category": "EXECUTION_ADDED_BINARY",\n'
                    '  "resource": "k8s_pod/checkout-api-882bf",\n'
                    '  "details": {\n'
                    '    "binary_path": "/tmp/xmrig_miner",\n'
                    '    "user": "root (UID 0)",\n'
                    '    "parent_process": "/bin/sh"\n'
                    '  }\n'
                    '}\n'
                    '```\n\n'
                    'Analysis: The container inherited from `debian:latest`, ran as root, and had a writable root filesystem, '
                    'allowing the attacker to download and execute arbitrary binaries.'
                ),
                'diagnostic_steps': [
                    'Review the application Dockerfile to inspect the base image and user declarations.',
                    'Inspect the Kubernetes Deployment manifest for `securityContext` settings (`runAsNonRoot`, `readOnlyRootFilesystem`).',
                    'Test whether `/bin/sh` or `/bin/bash` can be executed inside the pod via <kbd>kubectl exec</kbd>.',
                    'Verify filesystem mount permissions on `/tmp` and `/app`.'
                ],
                'root': 'The application used a full Debian base image running as root with a writable filesystem, allowing an attacker to drop and execute binaries.',
                'fix': 'Migrate the Dockerfile to Google Distroless, declare `USER 65532:65532`, and enforce `readOnlyRootFilesystem: true` with an in-memory tmpfs mount in the Kubernetes deployment manifest.',
                'residual': 'In-memory buffer overflows targeting application memory structures must be mitigated by memory-safe programming languages or compiler protections.',
                'diagram': (
                    'Attacker exploits web injection flaw on Debian container running as root',
                    'Attacker uses /bin/sh to download cryptomining binary to writable /tmp',
                    'Malware executes with root privileges; attempts container breakout',
                    'Refactor to Distroless base, enforce non-root UID 65532, and lock root FS',
                    'Payload execution fails: no shell binary exists and filesystem is read-only'
                )
            },
            'lab': {
                'name': 'Distroless Multi-Stage Build & Hardened Kubernetes Manifest Auditor',
                'goal': 'Author a hardened multi-stage Dockerfile using Google Distroless, develop a Kubernetes deployment manifest enforcing non-root and read-only filesystems, and test a Python security policy auditor.',
                'expected': 'A hardened multi-stage Dockerfile, a verified Kubernetes manifest, and a passing Python security context audit.',
                'mode': 'Declarative manifests and Python audit script',
                'prereq': 'Python 3.10+ installed.',
                'preflight': 'Create working directory <kbd>~/container-hardening-lab</kbd>.',
                'steps': [
                    (
                        '#### Author Hardened Multi-Stage Distroless Dockerfile\n'
                        'Create the working directory and author a multi-stage Dockerfile compiling an application in a builder image and deploying it onto a minimal Distroless runtime image as non-root:\n\n'
                        '```sh\n'
                        'mkdir -p ~/container-hardening-lab && cd ~/container-hardening-lab\n'
                        'cat <<\'EOF\' > Dockerfile.hardened\n'
                        '# Stage 1: Build environment\n'
                        'FROM golang:1.22-alpine AS builder\n'
                        'WORKDIR /src\n'
                        'COPY main.go .\n'
                        'RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server main.go\n'
                        '\n'
                        '# Stage 2: Hardened Distroless runtime environment\n'
                        'FROM gcr.io/distroless/static-debian12:nonroot\n'
                        'WORKDIR /app\n'
                        'COPY --from=builder /app/server /app/server\n'
                        '# Explicitly enforce non-root user (UID 65532 is nonroot in Distroless)\n'
                        'USER 65532:65532\n'
                        'ENTRYPOINT ["/app/server"]\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Author Hardened Kubernetes Deployment Manifest\n'
                        'Write a declarative Kubernetes manifest enforcing `readOnlyRootFilesystem: true`, dropping all Linux capabilities, and mounting a memory-backed tmpfs for temporary data:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > deployment_hardened.yaml\n'
                        'apiVersion: apps/v1\n'
                        'kind: Deployment\n'
                        'metadata:\n'
                        '  name: payment-api\n'
                        '  namespace: production\n'
                        'spec:\n'
                        '  replicas: 3\n'
                        '  selector:\n'
                        '    matchLabels:\n'
                        '      app: payment-api\n'
                        '  template:\n'
                        '    metadata:\n'
                        '      labels:\n'
                        '        app: payment-api\n'
                        '    spec:\n'
                        '      securityContext:\n'
                        '        runAsNonRoot: true\n'
                        '        runAsUser: 65532\n'
                        '        runAsGroup: 65532\n'
                        '        fsGroup: 65532\n'
                        '      containers:\n'
                        '      - name: payment-api\n'
                        '        image: us-central1-docker.pkg.dev/fintech-prod/apps/payment-api@sha256:8a72b91c89f1d0123456789abcdef0123456789abcdef0123456789abcdef012\n'
                        '        securityContext:\n'
                        '          readOnlyRootFilesystem: true\n'
                        '          allowPrivilegeEscalation: false\n'
                        '          capabilities:\n'
                        '            drop:\n'
                        '            - ALL\n'
                        '        volumeMounts:\n'
                        '        - name: tmp-scratch\n'
                        '          mountPath: /tmp\n'
                        '      volumes:\n'
                        '      - name: tmp-scratch\n'
                        '        emptyDir:\n'
                        '          medium: Memory\n'
                        '          sizeLimit: 64Mi\n'
                        'EOF\n'
                        '```'
                    ),
                    (
                        '#### Implement and Run the Security Context Policy Auditor\n'
                        'Write a Python tool that parses the Kubernetes manifest, verifies that non-root, read-only root filesystems, and dropped capabilities are enforced, and confirms compliance:\n\n'
                        '```sh\n'
                        'cat <<\'EOF\' > audit_manifest.py\n'
                        'import sys\n'
                        '\n'
                        'def audit():\n'
                        '    with open("deployment_hardened.yaml", "r") as f:\n'
                        '        content = f.read()\n'
                        '\n'
                        '    print("=== Auditing Kubernetes Deployment Hardening Controls ===\\n")\n'
                        '    checks = [\n'
                        '        ("runAsNonRoot: true", "Enforce non-root user execution"),\n'
                        '        ("runAsUser: 65532", "Explicit high non-root UID specified"),\n'
                        '        ("readOnlyRootFilesystem: true", "Root filesystem locked in read-only mode"),\n'
                        '        ("allowPrivilegeEscalation: false", "Privilege escalation strictly disabled"),\n'
                        '        ("drop:\\n            - ALL", "All Linux capabilities dropped"),\n'
                        '        ("medium: Memory", "Tmpfs memory-backed scratch volume mounted")\n'
                        '    ]\n'
                        '\n'
                        '    passed = 0\n'
                        '    for snippet, desc in checks:\n'
                        '        if snippet in content:\n'
                        '            print(f"[PASS] {desc}")\n'
                        '            passed += 1\n'
                        '        else:\n'
                        '            print(f"[FAIL] Missing control: {desc}")\n'
                        '\n'
                        '    print(f"\\nAudit Score: {passed}/{len(checks)} controls verified.")\n'
                        '    if passed == len(checks):\n'
                        '        print("VERDICT: FULLY HARDENED - Meets Production Workload Standards [OK]")\n'
                        '        return 0\n'
                        '    else:\n'
                        '        print("VERDICT: INSECURE - Hardening violations detected [!]")\n'
                        '        return 1\n'
                        '\n'
                        'if __name__ == "__main__":\n'
                        '    sys.exit(audit())\n'
                        'EOF\n'
                        'python3 audit_manifest.py\n'
                        '```'
                    )
                ],
                'accept': 'Validated multi-stage Distroless Dockerfile and hardened Kubernetes manifest passing all non-root and read-only filesystem policy checks.',
                'verification': 'Review terminal output of <kbd>python3 audit_manifest.py</kbd> confirming 6/6 controls verified and VERDICT: FULLY HARDENED.',
                'trouble': 'If checks fail, verify indentation in `deployment_hardened.yaml`.',
                'cleanup': 'Remove test files: <kbd>rm -rf ~/container-hardening-lab</kbd>.',
                'file': 'day-115-container-hardening.md'
            }
        }
    ]
}
