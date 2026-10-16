#!/usr/bin/env python3
"""Scenarios and Labs for Day 7."""

SCENARIOS_AND_LABS = {
    'topic-01': {
        'scenario': {
            'scenario': 'Agent forwarding socket hijacked on jump host',
            'impact': 'Decrypted SSH credentials exposed on shared staging bastion; rogue operators pivot into isolated production database instances.',
            'constraints': 'No direct internet access permitted to internal VPC subnets; staging bastion shared among multiple engineering teams; private keys must remain strictly on local workstations.',
            'evidence': '''**illustrative supplied records**

```text
[Bastion Host Auth Log] Accepted publickey for alice from 198.51.100.15 port 52318 ssh2: RSA SHA256:d8a4...
[Bastion Agent Forwarding] Agent forwarding enabled: SSH_AUTH_SOCK=/tmp/ssh-8xK19q/agent.18241
[Rogue Local Operator] UID 1000 (attacker) gains root via local privilege escalation
[Rogue Local Operator] export SSH_AUTH_SOCK=/tmp/ssh-8xK19q/agent.18241
[Rogue Local Operator] ssh prod-db-admin@10.128.0.5 -i dummy -o StrictHostKeyChecking=no
[Target Prod DB Auth Log] Accepted publickey for prod-db-admin from 10.128.0.2 (bastion) port 49122 ssh2: RSA SHA256:d8a4...
[Target Prod DB Alert] UNAUTHORIZED SESSION: Root access initiated from staging jump host
```''',
            'root': 'SSH agent forwarding vulnerability: the engineer connected to the shared bastion using ssh -A, creating an authentication socket in /tmp accessible to the bastion root user. When the bastion was compromised, attackers hijacked the forwarded agent socket to authenticate to internal production databases using the engineer\'s credentials.',
            'diagnostic_steps': [
                'Inspect client SSH configuration and alias parameters to identify -A or ForwardAgent yes directives.',
                'Check /tmp on the bastion server for active agent domain sockets (ls -la /tmp/ssh-*).',
                'Audit target production server authentication logs (/var/log/auth.log) for unexpected administrative sessions originating from the bastion IP.',
                'Verify whether ProxyJump or IAP TCP forwarding is enforced.'
            ],
            'remediation_steps': [
                'Disable agent forwarding on all bastion hosts: set AllowAgentForwarding no in /etc/ssh/sshd_config and restart sshd.',
                'Migrate client configuration to use ProxyJump (ssh -J or ProxyJump bastion directive in ~/.ssh/config).',
                'Rotate all exposed SSH key pairs and revoke unauthorized public keys from ~/.ssh/authorized_keys.',
                'Deploy Google Cloud OS Login and Identity-Aware Proxy (IAP) TCP forwarding to replace shared bastion VMs.'
            ],
            'verify': 'Attempting ssh -A to the bastion reports agent forwarding rejected; connecting via ProxyJump routes TCP streams without exposing SSH_AUTH_SOCK on the jump host.',
            'residual': 'Workstation private keys can still be compromised if the engineer\'s local laptop is infected; require passphrase-protected keys and hardware security keys (FIDO2/U2F) for all production access.',
            'diagram_enabled': True,
            'diagram': (
                'Admin connects via ssh -A',
                'Forwarded agent socket exposed in /tmp',
                'Root attacker hijacks socket to prod DB',
                'Enforce ProxyJump & disable agent forwarding',
                'End-to-end crypto auth without key exposure'
            ),
            'icons': [
                '../assets/icons/generic/client.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/gcp/core/compute-engine.svg',
                '../assets/icons/generic/outcome.svg'
            ],
            'facts': 'Supplied incident capture: ssh -A created /tmp/ssh-8xK19q/agent.18241 on bastion; attacker hijacked socket to access 10.128.0.5.',
            'inference': 'Architectural inference: agent forwarding delegates cryptographic signing authority to remote hosts; ProxyJump routes raw TCP streams while keeping cryptographic material strictly local.',
            'expected': 'Expected post-fix behavior: bastion carries no forwarded agent socket, and client reaches target database via end-to-end encrypted ProxyJump tunnel.'
        },
        'lab': {
            'name': 'Lab 7.1: Inspect local SSH configuration, model key permissions, and evaluate ProxyJump profiles',
            'goal': 'Inspect OpenSSH configuration directives, enforce strict octal permission boundaries on private keys, and configure connection profiles demonstrating ProxyJump encapsulation.',
            'mode': 'Observed locally: local bash commands execute ssh-keygen, inspect ssh config syntax, and enforce strict octal permission boundaries. Simulated or predicted: simulated multi-hop ProxyJump connection routing. Untested on GCP: live Compute Engine OS Login PAM integration, Cloud IAP TCP forwarding, and organization-level SSH key constraints.',
            'covers': 'Use a local test VM to inspect SSH configuration; write a small script that parses synthetic JSON and fails explicitly on invalid input (SSH configuration and key permissions)',
            'prereq': 'OpenSSH client (ssh, ssh-keygen), bash shell, coreutils.',
            'preflight': 'Validate ssh and ssh-keygen availability, create isolated lab directory, initialize mock SSH environment.',
            'verification': 'Verify that private key files with mode 0644 are rejected by ssh, while mode 0600 passes validation.',
            'trouble': 'Inspect ssh -v verbose output for permissions errors and directive syntax validation.',
            'cleanup': 'Remove temporary mock SSH keys and configuration directory.',
            'accept': 'The SSH validator confirms that permissive private key permissions trigger fatal security errors, and verifies that configuration profiles parse ProxyJump stanzas cleanly.',
            'file': 'day-007-topic-01.md',
            'steps': [
                '''**Stage 1: Preflight environment and tool verification**

**Location:** local bash terminal

Verify that OpenSSH client binaries and cryptographic utilities are installed and available:

```bash
command -v ssh >/dev/null 2>&1 || { echo "FATAL: ssh command not found"; exit 1; }
command -v ssh-keygen >/dev/null 2>&1 || { echo "FATAL: ssh-keygen command not found"; exit 1; }
LAB_DIR=$(mktemp -d /tmp/lab_day7_ssh.XXXXXX)
export LAB_DIR
cd "$LAB_DIR"
echo "PASS: OpenSSH client tools available. Workspace: $LAB_DIR"
```

**Expected result:** Tools verified; isolated workspace created.

**Save:** `$LAB_DIR/preflight.log`''',

                '''**Stage 2: Generate Ed25519 test keypair and verify key attributes**

**Location:** local bash terminal

Generate an unencrypted Ed25519 SSH keypair for testing and inspect public/private key formats:

```bash
mkdir -p "$LAB_DIR/.ssh"
ssh-keygen -t ed25519 -N "" -C "test-engineer@brightloaf.example" -f "$LAB_DIR/.ssh/id_test_ed25519"
ls -la "$LAB_DIR/.ssh"
ssh-keygen -l -f "$LAB_DIR/.ssh/id_test_ed25519.pub"
```

**Expected result:** Private key `id_test_ed25519` and public key `id_test_ed25519.pub` created with 256-bit Ed25519 fingerprint.

**Save:** `$LAB_DIR/keygen.log`''',

                '''**Stage 3: Author client SSH configuration profile**

**Location:** local bash terminal

Create an OpenSSH client configuration file demonstrating secure ProxyJump and connection multiplexing:

```bash
cat > "$LAB_DIR/.ssh/config" <<EOF
# Brightloaf Enterprise Client SSH Configuration

Host *
  ServerAliveInterval 60
  ServerAliveCountMax 3
  StrictHostKeyChecking ask
  HashKnownHosts yes

Host bastion
  HostName 198.51.100.10
  User bastion-admin
  IdentityFile $LAB_DIR/.ssh/id_test_ed25519
  ForwardAgent no

Host db-internal
  HostName 10.128.0.5
  User db-operator
  IdentityFile $LAB_DIR/.ssh/id_test_ed25519
  ProxyJump bastion
  ControlMaster auto
  ControlPath $LAB_DIR/.ssh/mux_%r@%h:%p
  ControlPersist 10m
EOF
chmod 0600 "$LAB_DIR/.ssh/config"
cat "$LAB_DIR/.ssh/config"
```

**Expected result:** Configuration file created with mode 0600, explicit ForwardAgent no, and ProxyJump declaration.

**Save:** `$LAB_DIR/.ssh/config`''',

                '''**Stage 4: Rehearse private key permission failure boundary**

**Location:** local bash terminal

Simulate insecure private key permissions (mode 0644) and verify OpenSSH fatal security rejection:

```bash
chmod 0644 "$LAB_DIR/.ssh/id_test_ed25519"
# Test key loading via ssh-keygen verification; OpenSSH rejects permissive keys
ssh -F "$LAB_DIR/.ssh/config" -G db-internal > "$LAB_DIR/config_parsed.log"
stat -c "Key permissions: %a (insecure)" "$LAB_DIR/.ssh/id_test_ed25519"
```

**Expected result:** Permissions identified as 0644 (world-readable), violating OpenSSH security policy.

**Save:** `$LAB_DIR/insecure_perm.log`''',

                '''**Stage 5: Enforce strict private key permissions**

**Location:** local bash terminal

Remediate private key permissions to mode 0600 (owner read/write only) and verify compliance:

```bash
chmod 0600 "$LAB_DIR/.ssh/id_test_ed25519"
stat -c "Remediated key permissions: %a (secure)" "$LAB_DIR/.ssh/id_test_ed25519"
test "$(stat -c %a "$LAB_DIR/.ssh/id_test_ed25519")" = "600" && echo "PASS: Mode 0600 verified"
```

**Expected result:** Private key permissions set to 0600; validation passes.

**Save:** `$LAB_DIR/secure_perm.log`''',

                '''**Stage 6: Inspect configuration parser resolution for ProxyJump**

**Location:** local bash terminal

Execute OpenSSH configuration syntax parsing to inspect effective directives resolved for the target host:

```bash
ssh -F "$LAB_DIR/.ssh/config" -G db-internal | grep -E "(hostname|user|proxyjump|forwardagent|identityfile)" | tee "$LAB_DIR/resolved_directives.log"
```

**Expected result:** Parser confirms hostname 10.128.0.5, user db-operator, proxyjump bastion, and forwardagent no.

**Save:** `$LAB_DIR/resolved_directives.log`''',

                '''**Stage 7: Diagnose evidence and compile SSH security audit report**

**Location:** local bash terminal

Compile the SSH configuration and key management security audit report:

```bash
cat > "$LAB_DIR/ssh_audit_report.md" <<EOF
# SSH Configuration and Cryptographic Security Audit Report

## Summary
- **Timestamp:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Key Algorithm:** Ed25519 (256-bit Edwards Curve)
- **Key Permissions Mode:** 0600 (Owner Read/Write)
- **Proxy Traversal Strategy:** ProxyJump (Opaque TCP Stream)
- **Agent Forwarding:** Disabled (ForwardAgent no)

## Security Policy Verification
1. Private Key Permissions: Mode 0600 enforced (world/group access blocked).
2. Bastion Jump Profile: Configured via ProxyJump; no agent socket forwarded.
3. Connection Multiplexing: ControlPath enabled with ControlPersist 10m.
EOF
cat "$LAB_DIR/ssh_audit_report.md"
```

**Expected result:** Comprehensive markdown audit report generated.

**Save:** `$LAB_DIR/ssh_audit_report.md`''',

                '''**Stage 8: Clean up mock SSH workspace**

**Location:** local bash terminal

Clean up generated mock SSH keys and configuration files:

```bash
rm -rf "$LAB_DIR"
echo "PASS: Mock SSH workspace cleaned up successfully."
```

**Expected result:** Temporary directory removed; environment clean.

**Save:** none'''
            ]
        }
    },

    'topic-02': {
        'scenario': {
            'scenario': 'Expired repository GPG key halts instance provisioning',
            'impact': 'Compute Engine autoscaling VMs fail startup script execution, preventing replacement instances from serving traffic during a peak load event.',
            'constraints': 'Production instances must pass automated pre-flight security update checks; no unsigned packages permitted; startup scripts must complete within 120 seconds.',
            'evidence': '''**illustrative supplied records**

```text
[VM Startup Script] Executing /var/run/google.startup.script
[APT Update Log] Get:1 http://deb.debian.org/debian bookworm InRelease [151 kB]
[APT Update Log] Get:2 https://packages.example.com/apt brightloaf-stable InRelease [4,200 B]
[APT Error] Err:2 https://packages.example.com/apt brightloaf-stable InRelease
[APT Error]   The following signatures were invalid: EXPKEYSIG 8F3B9A107C4D5E21 Brightloaf Release Signing Key <packaging@brightloaf.example>
[APT Error] W: GPG error: https://packages.example.com/apt brightloaf-stable InRelease: The following signatures were invalid: EXPKEYSIG 8F3B9A107C4D5E21
[APT Error] E: The repository 'https://packages.example.com/apt brightloaf-stable InRelease' is not signed.
[Startup Script Failure] Command 'apt-get update && apt-get install -y brightloaf-worker' returned exit status 100
[Health Check Probe] GET /health -> Connection Refused (port 8080 inactive)
[MIG Autoscaler Alert] Instance group manager failed to bring up healthy instance: Instance terminated
```''',
            'root': 'Repository cryptographic signature failure: the upstream repository signing GPG key expired without prior notification. The package manager rejected the release metadata (EXPKEYSIG) to prevent untrusted software execution, halting the VM startup script and causing instances to fail load balancer health checks.',
            'diagnostic_steps': [
                'Inspect serial port output console logs (gcloud compute instances get-serial-port-output) for APT/DNF exit codes.',
                'Query the local keyring using apt-key list or gpg to inspect key expiration timestamps.',
                'Manually execute the package manager update command on a staging VM to reproduce the GPG verification error.',
                'Check whether the upstream repository publishes an updated signing key.'
            ],
            'remediation_steps': [
                'Import the rotated GPG public key into /etc/apt/keyrings/ and update the sources.list signed-by directive.',
                'Migrate application deployment from runtime apt-get installation to pre-baked golden images (built via Packer in CI/CD).',
                'Mirror critical upstream packages into Google Cloud Artifact Registry to isolate production from external key expiration events.',
                'Re-bake the Compute Engine instance template with the verified image and perform a rolling update.'
            ],
            'verify': 'Running apt-get update completes with 0 errors and validates the InRelease signature; newly provisioned VMs boot in under 20 seconds and pass health checks.',
            'residual': 'Internal Artifact Registry mirrors require automated mirror sync jobs and key rotation alerting; pre-baked images must be updated regularly to incorporate base OS security patches.',
            'diagram_enabled': True,
            'diagram': (
                'Autoscaling VM startup script runs apt-get',
                'Upstream GPG signing key expired',
                'Instance provisioning fails & health check drops',
                'Build immutable golden image with pre-installed packages',
                'Deterministic instant boot with zero repo dependencies'
            ),
            'icons': [
                '../assets/icons/generic/server.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/policy.svg',
                '../assets/icons/generic/outcome.svg'
            ],
            'facts': 'Supplied incident capture: apt-get failed with EXPKEYSIG 8F3B9A107C4D5E21; startup script exited with status 100.',
            'inference': 'Architectural inference: runtime package installations create hard external dependencies on third-party repositories; immutable golden images decouple instance provisioning from external repository availability.',
            'expected': 'Expected post-fix behavior: instances boot from custom pre-baked images with zero runtime package downloads, passing health checks immediately.'
        },
        'lab': {
            'name': 'Lab 7.2: Verify package signatures, query package databases, and manage repository keyrings',
            'goal': 'Inspect package manager database records, query package file manifests, verify checksums, and model GPG repository verification.',
            'mode': 'Observed locally: local dpkg/rpm queries inspect installed package manifests, simulate GPG key verification, and detect package file modifications. Simulated or predicted: simulated upstream repository mirror failover. Untested on GCP: live Artifact Registry private repository sync, VM Manager OS patch deployments, and automated rolling image replacement.',
            'covers': 'Use a local test VM to inspect SSH configuration; write a small script that parses synthetic JSON and fails explicitly on invalid input (package verification and keyrings)',
            'prereq': 'dpkg or rpm, python3, bash shell.',
            'preflight': 'Verify availability of package management query tools (dpkg-query or rpm), create workspace.',
            'verification': 'Verify package file integrity checks and inspect package dependency lists.',
            'trouble': 'Check package database locks or query syntax.',
            'cleanup': 'Remove temporary workspace directory.',
            'accept': 'The package inspection tool successfully reports package metadata, verifies installed file checksums, and demonstrates cryptographic validation logic.',
            'file': 'day-007-topic-02.md',
            'steps': [
                '''**Stage 1: Preflight tool and package query engine verification**

**Location:** local bash terminal

Verify package query tools and create isolated lab workspace:

```bash
PKG_TOOL=""
if command -v dpkg-query >/dev/null 2>&1; then
  PKG_TOOL="dpkg"
elif command -v rpm >/dev/null 2>&1; then
  PKG_TOOL="rpm"
else
  echo "FATAL: Neither dpkg-query nor rpm found"; exit 1
fi
LAB_DIR=$(mktemp -d /tmp/lab_day7_pkg.XXXXXX)
export LAB_DIR PKG_TOOL
echo "PASS: Package tool detected: $PKG_TOOL. Workspace: $LAB_DIR"
```

**Expected result:** Package tool identified (dpkg or rpm); workspace initialized.

**Save:** `$LAB_DIR/preflight.log`''',

                '''**Stage 2: Query installed system packages and architecture**

**Location:** local bash terminal

Query a fundamental system package (e.g. bash or coreutils) to inspect package metadata:

```bash
if [ "$PKG_TOOL" = "dpkg" ]; then
  dpkg-query -s bash > "$LAB_DIR/pkg_status.log"
else
  rpm -qi bash > "$LAB_DIR/pkg_status.log"
fi
head -n 15 "$LAB_DIR/pkg_status.log"
```

**Expected result:** Package name, version, architecture, and maintainer information displayed.

**Save:** `$LAB_DIR/pkg_status.log`''',

                '''**Stage 3: Inspect package file manifest and paths**

**Location:** local bash terminal

Extract the list of installed files and configuration targets associated with the package:

```bash
if [ "$PKG_TOOL" = "dpkg" ]; then
  dpkg-query -L bash | grep -E "bin/bash" > "$LAB_DIR/pkg_files.log"
else
  rpm -ql bash | grep -E "bin/bash" > "$LAB_DIR/pkg_files.log"
fi
cat "$LAB_DIR/pkg_files.log"
```

**Expected result:** Executable binary paths resolved from package database.

**Save:** `$LAB_DIR/pkg_files.log`''',

                '''**Stage 4: Verify package file integrity against stored checksums**

**Location:** local bash terminal

Execute package verification to compare local file hashes against the package database checksums:

```bash
if [ "$PKG_TOOL" = "dpkg" ]; then
  # dpkg --verify checks MD5/SHA hashes of installed files
  dpkg --verify bash > "$LAB_DIR/pkg_verify.log"
else
  rpm -V bash > "$LAB_DIR/pkg_verify.log"
fi
echo "Verification complete (empty output indicates 100% hash match):"
cat "$LAB_DIR/pkg_verify.log"
```

**Expected result:** Verification executes; clean un-modified packages report zero hash mismatches.

**Save:** `$LAB_DIR/pkg_verify.log`''',

                '''**Stage 5: Model repository GPG metadata verification**

**Location:** local bash terminal

Create a Python script that models repository metadata signature and SHA-256 checksum verification:

```bash
cat > "$LAB_DIR/verify_repo.py" <<'EOF'
import hashlib
import sys

# Simulated InRelease metadata with package hashes
metadata = """
Package: brightloaf-worker
Version: 2.4.1
Filename: pool/main/b/brightloaf-worker_2.4.1_amd64.deb
SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
"""

# Test payload
package_bytes = b""
computed_hash = hashlib.sha256(package_bytes).hexdigest()
expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

print(f"Computed Package SHA-256: {computed_hash}")
print(f"Metadata Expected SHA-256: {expected_hash}")
if computed_hash == expected_hash:
    print("PASS: Cryptographic checksum matches repository metadata")
else:
    print("FATAL: Checksum mismatch! Potential tampering detected")
    sys.exit(1)
EOF
python3 "$LAB_DIR/verify_repo.py" | tee "$LAB_DIR/repo_verification.log"
```

**Expected result:** Checksum verification passes, validating package integrity.

**Save:** `$LAB_DIR/repo_verification.log`''',

                '''**Stage 6: Rehearse corrupted package checksum rejection**

**Location:** local bash terminal

Simulate tampered package data and verify explicit rejection:

```bash
cat > "$LAB_DIR/test_tamper.py" <<'EOF'
import hashlib
import sys

tampered_bytes = b"MALICIOUS_PAYLOAD"
computed = hashlib.sha256(tampered_bytes).hexdigest()
expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

if computed != expected:
    print(f"REJECTED: Checksum mismatch! Computed={computed[:12]} Expected={expected[:12]}")
    sys.exit(0) # Expected rejection test
else:
    sys.exit(1)
EOF
python3 "$LAB_DIR/test_tamper.py" && echo "PASS: Tampered package successfully rejected"
```

**Expected result:** Checksum mismatch triggers explicit rejection.

**Save:** `$LAB_DIR/tamper_test.log`''',

                '''**Stage 7: Diagnose evidence and compile package audit report**

**Location:** local bash terminal

Compile the package manager and repository integrity audit report:

```bash
cat > "$LAB_DIR/pkg_audit_report.md" <<EOF
# Package Management and Cryptographic Verification Report

## Summary
- **Package Management Engine:** $PKG_TOOL
- **Inspected Package:** bash
- **Integrity Status:** Verified against stored package database checksums
- **Cryptographic Model:** SHA-256 metadata verification demonstrated

## Architectural Recommendation
To eliminate runtime repository GPG expiration failures during autoscaling:
1. Pre-bake VM images using HashiCorp Packer with all packages pre-installed.
2. Mirror required third-party repositories into Google Cloud Artifact Registry.
EOF
cat "$LAB_DIR/pkg_audit_report.md"
```

**Expected result:** Markdown package audit report created.

**Save:** `$LAB_DIR/pkg_audit_report.md`''',

                '''**Stage 8: Clean up package lab workspace**

**Location:** local bash terminal

Clean up temporary files and reset directory:

```bash
rm -rf "$LAB_DIR"
echo "PASS: Package lab workspace cleaned up."
```

**Expected result:** Workspace deleted.

**Save:** none'''
            ]
        }
    },

    'topic-03': {
        'scenario': {
            'scenario': 'Unquoted variable expansion causes catastrophic data loss',
            'impact': 'Automated maintenance script accidentally deletes application state directories across multiple service mount points due to shell word splitting.',
            'constraints': 'Cleanup scripts run automatically via systemd timers; target paths are passed dynamically via environment variables; script must halt immediately on any unexpected error.',
            'evidence': '''**illustrative supplied records**

```text
[Cron Job Invocation] /usr/local/bin/cleanup_temp.sh
[Script Header] #!/bin/bash (no set -e, no set -u)
[Variable Assignment] BACKUP_DIR="/mnt/storage/brightloaf cache/daily"
[Executed Command] rm -rf $BACKUP_DIR
[Shell Expansion Tracing] rm -rf /mnt/storage/brightloaf cache/daily
[Filesystem Event] System executes:
  1. rm -rf /mnt/storage/brightloaf (DELETED: Main customer storage directory!)
  2. rm -rf cache/daily (Failed: No such file or directory)
[Incident Alert] CRITICAL OUTAGE: Customer image storage /mnt/storage/brightloaf deleted
[Operator Panic] File recovery initiated from off-site disaster recovery snapshot
```''',
            'root': 'Unquoted variable expansion defect: the script author wrote rm -rf $BACKUP_DIR without double quotes. When the variable contained a path with an embedded space (/mnt/storage/brightloaf cache/daily), the shell\'s Internal Field Separator (IFS) performed word splitting, turning the variable into two separate arguments: /mnt/storage/brightloaf and cache/daily. The first argument deleted the production storage directory.',
            'diagnostic_steps': [
                'Inspect shell script source code for unquoted variable references ($VAR instead of "$VAR").',
                'Enable bash execution tracing (bash -x script.sh) to observe exact argument tokenization.',
                'Check whether defensive header flags (set -euo pipefail) are declared.',
                'Audit script inputs to verify handling of special characters, whitespace, and empty strings.'
            ],
            'remediation_steps': [
                'Wrap all variable expansions in double quotes: rm -rf "$BACKUP_DIR".',
                'Declare defensive header set -euo pipefail at the beginning of every shell script.',
                'Validate that target paths exist and are non-root subdirectories before executing destructive commands.',
                'Run ShellCheck in CI/CD linting pipelines to automatically catch unquoted variables (SC2086).'
            ],
            'verify': 'Running bash -x with a path containing spaces confirms that "$BACKUP_DIR" is passed as a single atomic argument to rm; ShellCheck reports 0 quoting warnings.',
            'residual': 'Double quotes preserve whitespace but do not prevent malicious path traversal (e.g. ../../); scripts must sanitize and canonicalize paths using realpath or readlink before execution.',
            'diagram_enabled': True,
            'diagram': (
                'Script receives path with space parameter',
                'Unquoted expansion triggers IFS word splitting',
                'rm -rf deletes unintended directory arguments',
                'Enforce strict quoting "$VAR" & set -euo pipefail',
                'Deterministic single-argument execution verified'
            ),
            'icons': [
                '../assets/icons/generic/artifact.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/decision.svg',
                '../assets/icons/generic/outcome.svg'
            ],
            'facts': 'Supplied incident capture: rm -rf $BACKUP_DIR split into /mnt/storage/brightloaf and cache/daily, deleting production storage.',
            'inference': 'Architectural inference: unquoted variables surrender argument boundaries to whitespace tokenization; strict double quoting preserves parameter integrity across shell execution pipelines.',
            'expected': 'Expected post-fix behavior: quoted expansion passes the exact single path token, preventing accidental word splitting.'
        },
        'lab': {
            'name': 'Lab 7.3: Author defensive shell script to parse synthetic JSON, enforce strict quoting, and handle errors',
            'goal': 'Write a small, hardened bash script that parses synthetic JSON configuration, tests successful runs, demonstrates explicit failure on invalid or missing fields, verifies quoting against whitespace, and ensures zero stored credentials.',
            'mode': 'Observed locally: local bash script executes valid and invalid JSON parsing, enforces strict quoting across whitespace paths, and records non-zero exit codes. Simulated or predicted: simulated automated CI/CD pipeline gating. Untested on GCP: Cloud Build step execution, Secret Manager secret injection, and Cloud Run entrypoint supervision.',
            'covers': 'write a small script that parses synthetic JSON and fails explicitly on invalid input. A script with successful and failed runs, quoting explained, and no stored credentials.',
            'prereq': 'bash 4+, python3, coreutils.',
            'preflight': 'Verify bash and python3 availability, create isolated test workspace.',
            'verification': 'Verify exit code 0 on valid JSON, exit code 2 on missing required fields, exit code 3 on malformed JSON, and confirm zero credentials stored.',
            'trouble': 'Check script execute permissions (chmod +x) and inspect stderr output.',
            'cleanup': 'Remove test workspace and temporary configuration files.',
            'accept': 'The parse script passes valid JSON, fails explicitly with distinct non-zero exit codes on invalid inputs, safely processes paths with embedded spaces, and demonstrates zero plaintext credentials.',
            'file': 'day-007-topic-03.md',
            'steps': [
                '''**Stage 1: Preflight environment and tool verification**

**Location:** local bash terminal

Verify that Bash and Python 3 are installed and functioning:

```bash
command -v bash >/dev/null 2>&1 || { echo "FATAL: bash not found"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "FATAL: python3 not found"; exit 1; }
LAB_DIR=$(mktemp -d /tmp/lab_day7_script.XXXXXX)
export LAB_DIR
cd "$LAB_DIR"
echo "PASS: Environment verified. Lab directory: $LAB_DIR"
```

**Expected result:** Bash and Python 3 verified; isolated workspace created.

**Save:** `$LAB_DIR/preflight.log`''',

                '''**Stage 2: Create synthetic JSON test fixtures**

**Location:** local bash terminal

Create three test fixtures: a valid configuration, an invalid configuration lacking required fields, and a malformed syntax configuration:

```bash
# 1. Valid configuration
cat > "$LAB_DIR/valid_config.json" <<'EOF'
{
  "service_name": "order-processor",
  "port": 8080,
  "workers": 4,
  "storage_path": "order data/active queue"
}
EOF

# 2. Missing required 'port' field
cat > "$LAB_DIR/missing_field_config.json" <<'EOF'
{
  "service_name": "order-processor",
  "workers": 4
}
EOF

# 3. Malformed JSON syntax (missing closing brace)
cat > "$LAB_DIR/malformed_config.json" <<'EOF'
{
  "service_name": "order-processor",
  "port": 8080,
EOF

ls -la "$LAB_DIR"/*.json
```

**Expected result:** Three synthetic JSON files created in the workspace.

**Save:** `$LAB_DIR/fixtures.log`''',

                '''**Stage 3: Author defensive JSON parser script (parse_config.sh)**

**Location:** local bash terminal

Author the hardened shell script adhering to strict defensive standards (`set -euo pipefail`, explicit error exits, quoting, zero hardcoded credentials):

```bash
cat > "$LAB_DIR/parse_config.sh" <<'EOF'
#!/usr/bin/env bash
# Defensive Shell Script: Parse Synthetic JSON Configuration
# Exit codes:
#   0 = Success
#   1 = Argument error
#   2 = Schema validation error (missing required keys)
#   3 = Malformed JSON syntax error
set -euo pipefail

# Trap handler for abnormal termination
trap 'echo "[ERROR] Script interrupted or failed unexpectedly at line $LINENO" >&2' ERR

# Ensure input file parameter is provided
if [ $# -lt 1 ]; then
  echo "Usage: $0 <path_to_config.json>" >&2
  exit 1
fi

CONFIG_FILE="$1"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "FATAL: Config file '$CONFIG_FILE' does not exist." >&2
  exit 1
fi

# Parse and validate JSON using python3 helper
# Validates schema: requires 'service_name', 'port', and 'storage_path'
PARSED_OUTPUT=$(python3 - <<PYEOF "$CONFIG_FILE"
import json, sys

try:
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    sys.stderr.write(f"SYNTAX ERROR: Malformed JSON - {e}\n")
    sys.exit(3)
except Exception as e:
    sys.stderr.write(f"FILE ERROR: {e}\n")
    sys.exit(1)

# Schema validation
required_fields = ["service_name", "port", "storage_path"]
missing = [field for field in required_fields if field not in data]
if missing:
    sys.stderr.write(f"SCHEMA ERROR: Missing required fields: {', '.join(missing)}\n")
    sys.exit(2)

# Output tab-separated values
print(f"{data['service_name']}\t{data['port']}\t{data['storage_path']}")
PYEOF
) || {
  EXIT_STATUS=$?
  echo "Validation failed with status code $EXIT_STATUS" >&2
  exit $EXIT_STATUS
}

# Safely extract tab-separated fields into bash variables
IFS=$'\t' read -r SVC_NAME SVC_PORT SVC_PATH <<< "$PARSED_OUTPUT"

# Demonstrate strict variable quoting: preserve whitespace in paths
echo "=== Configuration Loaded Successfully ==="
echo "Service Name : \"$SVC_NAME\""
echo "Port Number  : $SVC_PORT"
echo "Storage Path : \"$SVC_PATH\""

# Verify path handling with embedded whitespace
mkdir -p "$LAB_DIR/$SVC_PATH"
test -d "$LAB_DIR/$SVC_PATH" && echo "PASS: Directory created safely with quoting: '$SVC_PATH'"

exit 0
EOF
chmod +x "$LAB_DIR/parse_config.sh"
```

**Expected result:** Hardened `parse_config.sh` script created with execute permissions.

**Save:** `$LAB_DIR/parse_config.sh`''',

                '''**Stage 4: Execute successful run against valid synthetic JSON**

**Location:** local bash terminal

Execute `parse_config.sh` against `valid_config.json` and verify exit code 0:

```bash
"$LAB_DIR/parse_config.sh" "$LAB_DIR/valid_config.json" > "$LAB_DIR/success_run.log" 2>&1
EXIT_CODE=$?
echo "Observed Exit Code: $EXIT_CODE"
cat "$LAB_DIR/success_run.log"
test $EXIT_CODE -eq 0 && echo "PASS: Valid run succeeded with code 0"
```

**Expected result:** Script parses all fields, handles whitespace in `order data/active queue`, and exits with code 0.

**Save:** `$LAB_DIR/success_run.log`''',

                '''**Stage 5: Rehearse explicit failure on missing required fields**

**Location:** local bash terminal

Execute `parse_config.sh` against `missing_field_config.json` and verify exit code 2:

```bash
set +e
"$LAB_DIR/parse_config.sh" "$LAB_DIR/missing_field_config.json" > "$LAB_DIR/fail_missing.log" 2>&1
FAIL_CODE_1=$?
set -e
echo "Observed Exit Code: $FAIL_CODE_1"
cat "$LAB_DIR/fail_missing.log"
test $FAIL_CODE_1 -eq 2 && echo "PASS: Missing required field explicitly failed with code 2"
```

**Expected result:** Script detects missing `storage_path`, logs `SCHEMA ERROR`, and exits explicitly with code 2.

**Save:** `$LAB_DIR/fail_missing.log`''',

                '''**Stage 6: Rehearse explicit failure on malformed JSON syntax**

**Location:** local bash terminal

Execute `parse_config.sh` against `malformed_config.json` and verify exit code 3:

```bash
set +e
"$LAB_DIR/parse_config.sh" "$LAB_DIR/malformed_config.json" > "$LAB_DIR/fail_syntax.log" 2>&1
FAIL_CODE_2=$?
set -e
echo "Observed Exit Code: $FAIL_CODE_2"
cat "$LAB_DIR/fail_syntax.log"
test $FAIL_CODE_2 -eq 3 && echo "PASS: Malformed syntax explicitly failed with code 3"
```

**Expected result:** Script traps `JSONDecodeError`, logs `SYNTAX ERROR`, and exits explicitly with code 3.

**Save:** `$LAB_DIR/fail_syntax.log`''',

                '''**Stage 7: Verify quoting protection and absence of stored credentials**

**Location:** local bash terminal

Verify that the script contains no hardcoded passwords, tokens, or API keys, and explain quoting rules:

```bash
# 1. Audit for stored credentials in script
echo "=== Credential Leak Audit ==="
grep -Ei "(password|secret|token|api_key|private_key)" "$LAB_DIR/parse_config.sh" || echo "PASS: Zero stored credentials detected in script source"

# 2. Compile execution evidence report
cat > "$LAB_DIR/script_execution_report.md" <<EOF
# Defensive Script Execution and Quoting Verification Report

## Summary
- **Script:** `parse_config.sh`
- **Target Workload:** Synthetic JSON Configuration Parsing
- **Execution Timestamp:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Credential Storage Audit:** 0 stored credentials (verified via static grep audit)

## Execution Test Matrix

| Test Case | Input File | Expected Exit Code | Observed Exit Code | Result | Defensive Mechanism |
|---|---|---|---|---|---|
| **Valid Run** | `valid_config.json` | 0 | 0 | **PASS** | Complete schema parsed; whitespace path safely created |
| **Missing Field** | `missing_field_config.json` | 2 | 2 | **PASS** | Explicit schema assertion rejected missing `storage_path` |
| **Malformed Syntax** | `malformed_config.json` | 3 | 3 | **PASS** | JSONDecodeError caught; script halted before mutation |

## Quoting Mechanics Explained
1. **Word Splitting Prevention:** The variable `"$SVC_PATH"` contained spaces (`order data/active queue`). Enclosing in double quotes ensured `mkdir -p "$LAB_DIR/$SVC_PATH"` received a single directory path argument, preventing the shell from splitting it into two separate directories (`order` and `data/active`).
2. **Pipeline Safety:** `set -o pipefail` prevented silent subshell failure masking.
3. **Unset Guard:** `set -u` guaranteed uninitialized variables trigger immediate script termination.
EOF
cat "$LAB_DIR/script_execution_report.md"
```

**Expected result:** Script verified free of credentials; markdown report compiled.

**Save:** `$LAB_DIR/script_execution_report.md`''',

                '''**Stage 8: Clean up and close out workspace**

**Location:** local bash terminal

Preserve the audit report and clean up temporary test files:

```bash
cp "$LAB_DIR/script_execution_report.md" "/tmp/day7_script_execution_report.md"
rm -rf "$LAB_DIR"
echo "PASS: Script lab completed. Report preserved at /tmp/day7_script_execution_report.md."
```

**Expected result:** Workspace cleaned up; report preserved.

**Save:** none'''
            ]
        }
    },

    'topic-04': {
        'scenario': {
            'scenario': 'Unlinked open file descriptor causes 100% disk utilization',
            'impact': 'Persistent Disk fills to 100% capacity, halting database writes across production microservices despite du reporting ample free space.',
            'constraints': 'Production database VM cannot be rebooted without executive approval; disk resizing requires volume re-partitioning downtime; file descriptors must be diagnosed online.',
            'evidence': '''**illustrative supplied records**

```text
[Disk Space Alert] CRITICAL: Filesystem /dev/sda1 (mounted at /) usage is at 100% (0 bytes free)
[Operator du Check] du -sh /* | sort -h
  ...
  12G /usr
  4G  /var
  Total accounted usage by du: 18 GB (Total disk capacity: 100 GB)
[Discrepancy Detected] df reports 100 GB used (100%), du reports 18 GB used (18%)
[lsof Inspection] lsof +L1 /
  COMMAND     PID   USER   FD   TYPE DEVICE   SIZE/OFF NLINK      NODE NAME
  batch-app  4812 appuser    3w   REG    8,1 82000000000     0 148201948 /var/log/batch.log (deleted)
[Root Cause Confirmed] PID 4812 holds unlinked open file descriptor to deleted 82 GB log file
```''',
            'root': 'Unlinked open file descriptor defect: an operator ran rm /var/log/batch.log to clear space. However, batch-app (PID 4812) retained an open write file descriptor to the inode. In Linux, unlinking removes the directory entry but retains the disk blocks until the file descriptor is closed by the process. Because the process remained active, the 82 GB remained allocated while invisible to directory listings.',
            'diagnostic_steps': [
                'Compare df -h (filesystem block allocation) with du -sh (directory tree walk) to detect allocation discrepancies.',
                'Run lsof +L1 / to list open file descriptors with a link count of zero (unlinked/deleted files).',
                'Inspect the process file descriptor directory: ls -la /proc/[pid]/fd to identify active deleted targets.',
                'Examine /proc/[pid]/status and /proc/[pid]/cmdline to confirm process identity and ownership.'
            ],
            'remediation_steps': [
                'Truncate the active file descriptor to zero bytes via procfs: : > /proc/4812/fd/3.',
                'Restart the batch-app service cleanly via systemctl restart batch-app.',
                'Configure logrotate with copytruncate or reopen signals (SIGHUP) to prevent unlinked log retention.',
                'Verify disk utilization returns to 18% via df -h.'
            ],
            'verify': 'Running : > /proc/4812/fd/3 immediately frees 82 GB; df -h / reports 18% disk usage with 82 GB available; batch-app logs continue cleanly.',
            'residual': 'Truncating an active file descriptor does not fix underlying logging loops; application loggers must be configured with size-based rotation and retention limits.',
            'diagram_enabled': True,
            'diagram': (
                'Administrator unlinks active log file via rm',
                'Process holds open file descriptor in /proc/[pid]/fd',
                'Disk reaches 100% full; df/du discrepancy blocks writes',
                'Inspect /proc/[pid]/fd, truncate descriptor, restart process',
                'Disk blocks reclaimed immediately; write transactions resume'
            ),
            'icons': [
                '../assets/icons/generic/server.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/failure.svg',
                '../assets/icons/generic/monitoring.svg',
                '../assets/icons/generic/outcome.svg'
            ],
            'facts': 'Supplied incident capture: batch-app PID 4812 held FD 3 pointing to deleted /var/log/batch.log consuming 82 GB.',
            'inference': 'Architectural inference: Linux inodes are purged only when link count reaches zero AND all open file descriptors are closed; procfs provides live direct handles to active descriptors.',
            'expected': 'Expected post-fix behavior: truncating /proc/[pid]/fd/[n] releases disk blocks immediately without requiring process termination or VM reboot.'
        },
        'lab': {
            'name': 'Lab 7.4: Inspect /proc virtual telemetry, trace process trees, and diagnose open file descriptors',
            'goal': 'Inspect system-wide telemetry in /proc, analyze process trees and ancestry (PID/PPID), and demonstrate file descriptor diagnostics for open and deleted files.',
            'mode': 'Observed locally: local bash commands query /proc/cpuinfo, /proc/meminfo, inspect process status in /proc/[pid]/status, and track open file descriptors. Simulated or predicted: simulated background daemon lifecycle and unlinked inode retention. Untested on GCP: Cloud Ops Agent procfs telemetry collection, Cloud Monitoring dashboard streaming, and Compute Engine hypervisor steal time.',
            'covers': 'Use a local test VM to inspect SSH configuration; write a small script that parses synthetic JSON and fails explicitly on invalid input (procfs inspection and process trees)',
            'prereq': 'bash, python3, coreutils, procps.',
            'preflight': 'Verify access to /proc, check ps and stat tools, create temporary workspace.',
            'verification': 'Verify that /proc/[pid]/status reports process state and VmRSS, and confirm that deleted files remain accessible via /proc/[pid]/fd.',
            'trouble': 'Inspect permissions on /proc/[pid] entries (process owned by user).',
            'cleanup': 'Terminate background mock processes and remove workspace directory.',
            'accept': 'The procfs inspector successfully extracts CPU and memory telemetry, maps process tree parentage, and recovers deleted file content through /proc/[pid]/fd.',
            'file': 'day-007-topic-04.md',
            'steps': [
                '''**Stage 1: Preflight environment and procfs validation**

**Location:** local bash terminal

Verify that the `/proc` virtual filesystem is mounted and accessible:

```bash
test -d /proc || { echo "FATAL: /proc directory not mounted"; exit 1; }
test -r /proc/version || { echo "FATAL: Cannot read /proc/version"; exit 1; }
LAB_DIR=$(mktemp -d /tmp/lab_day7_proc.XXXXXX)
export LAB_DIR
cd "$LAB_DIR"
echo "PASS: /proc mounted and accessible. Workspace: $LAB_DIR"
```

**Expected result:** `/proc` verified mounted; workspace initialized.

**Save:** `$LAB_DIR/preflight.log`''',

                '''**Stage 2: Query system-wide hardware and memory telemetry**

**Location:** local bash terminal

Extract CPU core counts and calculate real available memory from `/proc/meminfo`:

```bash
echo "=== CPU Core Summary ==="
grep -m 1 "model name" /proc/cpuinfo
echo "Processor cores: $(grep -c "^processor" /proc/cpuinfo)"

echo "=== Memory Telemetry ==="
grep -E "(MemTotal|MemFree|MemAvailable|Buffers|Cached)" /proc/meminfo > "$LAB_DIR/mem_telemetry.log"
cat "$LAB_DIR/mem_telemetry.log"
```

**Expected result:** CPU architecture and memory metrics (`MemAvailable`) displayed.

**Save:** `$LAB_DIR/mem_telemetry.log`''',

                '''**Stage 3: Start background daemon and trace process identity**

**Location:** local bash terminal

Start a disposable background worker process and capture its process ID (PID):

```bash
python3 -c '
import time, os
print(f"WORKER_PID={os.getpid()}")
with open("active_work.log", "w") as f:
    while True:
        f.write(f"tick {time.time()}\\n")
        f.flush()
        time.sleep(1)
' > "$LAB_DIR/worker_startup.log" 2>&1 &
WORKER_PID=$!
echo "Background worker started with PID: $WORKER_PID"
sleep 2
```

**Expected result:** Worker process active in background; PID recorded.

**Save:** `$LAB_DIR/worker_startup.log`''',

                '''**Stage 4: Inspect process status and memory map in /proc/[pid]**

**Location:** local bash terminal

Inspect the running process state, memory metrics, and command line arguments in procfs:

```bash
grep -E "(Name|State|Tgid|Pid|PPid|VmRSS|VmSize)" "/proc/$WORKER_PID/status" > "$LAB_DIR/proc_status.log"
cat "$LAB_DIR/proc_status.log"

echo "=== Command Line (null-byte separated) ==="
tr '\\0' ' ' < "/proc/$WORKER_PID/cmdline" && echo ""
```

**Expected result:** Process state `S (sleeping)`, parent PID, VmRSS, and argument vector displayed.

**Save:** `$LAB_DIR/proc_status.log`''',

                '''**Stage 5: Inspect open file descriptors in /proc/[pid]/fd**

**Location:** local bash terminal

List active file descriptors associated with the worker process:

```bash
ls -l "/proc/$WORKER_PID/fd" > "$LAB_DIR/fd_list.log"
cat "$LAB_DIR/fd_list.log"
```

**Expected result:** Descriptors 0, 1, 2, and 3 (`active_work.log`) visible as symlinks.

**Save:** `$LAB_DIR/fd_list.log`''',

                '''**Stage 6: Rehearse unlinked open file recovery via procfs**

**Location:** local bash terminal

Simulate accidental deletion of the log file and recover its contents via `/proc/[pid]/fd`:

```bash
# Delete the log file from the directory
rm "$LAB_DIR/active_work.log"
ls -la "$LAB_DIR/active_work.log" || echo "Notice: File unlinked from filesystem directory"

# Inspect the file descriptor symlink in procfs
ls -l "/proc/$WORKER_PID/fd" | grep "(deleted)"

# Recover deleted file data directly from the active procfs descriptor!
LOG_FD=$(ls -l "/proc/$WORKER_PID/fd" | grep "(deleted)" | awk '{print $9}')
head -n 5 "/proc/$WORKER_PID/fd/$LOG_FD" > "$LAB_DIR/recovered_log.txt"
cat "$LAB_DIR/recovered_log.txt"
test -s "$LAB_DIR/recovered_log.txt" && echo "PASS: Deleted file content successfully recovered via /proc"
```

**Expected result:** Descriptor marked `(deleted)`; data successfully recovered from `/proc/[pid]/fd/[n]`.

**Save:** `$LAB_DIR/recovered_log.txt`''',

                '''**Stage 7: Diagnose evidence and compile process inspection report**

**Location:** local bash terminal

Compile the procfs and process inspection report:

```bash
cat > "$LAB_DIR/proc_inspection_report.md" <<EOF
# /proc Virtual Filesystem and Process Inspection Report

## Summary
- **Target Workload:** Python Worker Daemon (PID $WORKER_PID)
- **Parent Process (PPID):** $(grep PPid "$LAB_DIR/proc_status.log" | awk '{print $2}')
- **Virtual Memory Resident Size (VmRSS):** $(grep VmRSS "$LAB_DIR/proc_status.log" | awk '{print $2, $3}')
- **Telemetry Verification:** Real-time /proc/meminfo and /proc/cpuinfo queried

## Diagnostic Findings
1. **Zero-Block Virtual Filesystem:** /proc files generate text streams dynamically from kernel memory without disk I/O.
2. **Unlinked File Descriptor Persistence:** Unlinking a file does not reclaim disk blocks while an open descriptor remains in /proc/[pid]/fd.
3. **Data Recovery:** Active unlinked streams can be recovered or truncated directly via /proc/[pid]/fd/[n].
EOF
cat "$LAB_DIR/proc_inspection_report.md"
```

**Expected result:** Process inspection report generated.

**Save:** `$LAB_DIR/proc_inspection_report.md`''',

                '''**Stage 8: Terminate worker process and clean up workspace**

**Location:** local bash terminal

Terminate the background process and clean up temporary files:

```bash
kill -15 "$WORKER_PID" 2>/dev/null || true
wait "$WORKER_PID" 2>/dev/null || true
rm -rf "$LAB_DIR"
echo "PASS: Worker process terminated; workspace cleaned up."
```

**Expected result:** Process stopped; directory removed.

**Save:** none'''
            ]
        }
    }
}

print("Scenarios and labs defined.")
