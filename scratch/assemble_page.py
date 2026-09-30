#!/usr/bin/env python3
import sys
from pathlib import Path
import scratch.make_svgs as svgs

# Read head & header
orig_text = Path("content/day-001-page.html").read_text(encoding="utf-8")
header_end = orig_text.find("</header>") + len("</header>")
head_and_header = orig_text[:header_end]

footer_start = orig_text.find('<footer class="site-footer">')
footer_and_end = orig_text[footer_start:]

body_parts = []

# Hero
body_parts.append('''
  <main id="main" class="container day" data-day="1" data-prev="" data-next="day-002.html" data-index="../index.html">
    <div class="crumb"><a href="../index.html">Roadmap Index</a> / <a href="../index.html#block-foundations">Days 1–17 — Foundations</a> / Day 1 of 180</div>
    <section class="hero">
      <div class="pills"><span class="pill accent">Day 1</span><span class="pill">2–3 hours</span><span class="pill">Local exercise</span><span class="pill">Topics 002 · 010</span></div>
      <h1>Day 1 — Local workspace and learning baseline</h1>
      <p class="lead"><strong>Outcome:</strong> Create a disposable local evidence repository, capture process exit codes and standard streams, calculate realistic curriculum pacing against available study hours, and establish a sandbox governance charter with synthetic data boundaries and cleanup accountability.</p>
      <p><strong>Entry prerequisites:</strong> None. Begin with an operational POSIX shell (Bash), an editor, Git, and Python 3. A Google Cloud account and cloud billing credentials are not required until Day 18.</p>
      <div class="callout success"><strong>Exit artifact</strong><p>A versioned README with available study hours, environment profile, evidence-based baseline skills, sandbox budget target, and cleanup owner, accompanied by committed terminal observation files and synthetic order fixtures.</p></div>
      <p class="small">This page uses local exercises and illustrative Brightloaf scenarios. A local terminal observation demonstrates workstation-level mechanics but does not prove remote cloud configuration or production infrastructure health.</p>
    </section>

    <aside class="toc" aria-label="On this page"><strong>On this page</strong>
      <a href="#part-1">1 · Topics</a><a href="#part-2">2 · Technical discussion</a><a href="#part-3">3 · Problems and solutions</a><a href="#part-4">4 · Labs</a>
      <div class="toc-topic"><span>Local workspace and evidence repository</span><a href="#workspace-repo-overview">overview</a> · <a href="#workspace-repo-technical">discussion</a> · <a href="#workspace-repo-problem">problem</a> · <a href="#workspace-repo-lab">lab</a></div>
      <div class="toc-topic"><span>Study sessions and learning baseline</span><a href="#learning-baseline-overview">overview</a> · <a href="#learning-baseline-technical">discussion</a> · <a href="#learning-baseline-problem">problem</a> · <a href="#learning-baseline-lab">lab</a></div>
      <div class="toc-topic"><span>Synthetic data, budget and cleanup ownership</span><a href="#budget-cleanup-overview">overview</a> · <a href="#budget-cleanup-technical">discussion</a> · <a href="#budget-cleanup-problem">problem</a> · <a href="#budget-cleanup-lab">lab</a></div>
    </aside>
''')

# Part 1
body_parts.append('''
    <section id="part-1" class="part"><h2>1 · Topics of the day</h2>
      <article id="workspace-repo-overview" class="topic-card"><span id="topic-01-overview" aria-hidden="true"></span><h3>Local workspace and evidence repository</h3>
        <p><strong>What it is:</strong> A dedicated, isolated directory on the developer workstation where the POSIX shell executes commands, the operating system kernel manages child process lifecycles and standard streams (stdin, stdout, stderr), and Git records cryptographic, immutable snapshots of filesystem state. In this environment, a process exit code (exposed in Bash as the <code>$?</code> parameter) supplies the machine contract for execution status, while captured output streams provide the qualitative telemetry necessary to audit system state.</p>
        <p><strong>Why today and system location:</strong> Day 1 establishes the local workstation and operator evidence boundary before any remote Google Cloud API, identity provider, or billing account is touched on Day 18. Codifying rigorous command logging, stream redirection, and Git commit conventions today guarantees that every subsequent exercise across all 180 days produces defensible, auditable evidence rather than unverified terminal recollections.</p>
        <p><strong>Problem preview:</strong> An operator runs an infrastructure validation script before a release gate but fails to persist standard streams or trap the process exit code. Downstream deployment fails in production, leaving responders unable to verify whether the initial validation succeeded or silently faulted.</p>
      </article>

      <article id="learning-baseline-overview" class="topic-card"><span id="topic-02-overview" aria-hidden="true"></span><h3>Study sessions and learning baseline</h3>
        <p><strong>What it is:</strong> A capacity-driven curriculum planning model that decouples the 180 modular study units from calendar days, calculating estimated completion time dynamically from measured weekly study hours. It establishes a rigorous tri-state competence evaluation framework—New, Familiar, and Demonstrated—where a skill is classified as Demonstrated only when supported by a committed, reproducible terminal log or architectural artifact.</p>
        <p><strong>Why today and system location:</strong> This baseline model is authored directly into the root repository <code>README.md</code> at the outset of the curriculum. Establishing honest capacity planning and evidence criteria today prevents prerequisite collapse, ensuring that core Linux process isolation and networking fundamentals are genuinely mastered before cloud-native architectures are tackled.</p>
        <p><strong>Problem preview:</strong> A learner attempts to progress at a pace of one curriculum unit per calendar day despite having only four hours of available study time each week. Prerequisite gaps accumulate unnoticed, causing cascade failures when diagnosing distributed systems later in the roadmap.</p>
      </article>

      <article id="budget-cleanup-overview" class="topic-card"><span id="topic-03-overview" aria-hidden="true"></span><h3>Synthetic data, budget and cleanup ownership</h3>
        <p><strong>What it is:</strong> A governance charter that strictly forbids production customer data in training sandboxes in favor of synthetic schemas, establishes explicit financial boundaries using Google Cloud Billing budgets, and assigns human accountability for resource teardown. It explicitly acknowledges that Cloud Billing budget alerts are advisory monitoring events rather than automated spend kill-switches, and enforces a durable replay-key invariant that prevents duplicate business fulfillments during event processing.</p>
        <p><strong>Why today and system location:</strong> Sandbox safety rules and cleanup accountability must be committed to version control before provisioning any live cloud resources on Day 18. Instituting these controls today ensures that future experimentation with Compute Engine, GKE, and serverless runtimes remains bounded in cost and immune to accidental PII disclosures.</p>
        <p><strong>Problem preview:</strong> An engineer seeds an experimental cloud environment with an unscrubbed customer order export and relies on an advisory budget alert to prevent billing overruns. Sensitive customer records are exposed in an unmonitored test project while idle virtual machines continue racking up charges past the budget threshold.</p>
      </article>
    </section>
''')

# Part 2
body_parts.append('''
    <section id="part-2" class="part"><h2>2 · Technical discussion</h2>
      <article id="workspace-repo-technical" class="topic-card"><span id="topic-01-technical" aria-hidden="true"></span><h3>Local workspace and evidence repository</h3>
        <p>The POSIX shell environment provides the execution baseline for cloud engineering. When a command is invoked, the shell parses tokens, resolves aliases and functions, performs PATH lookups for external binaries, and prepares file descriptors. For external commands, the shell executes <code>fork()</code> to clone the parent environment and <code>execve()</code> to replace the child address space with the executable image. The kernel establishes standard stream descriptors: descriptor 0 (standard input), descriptor 1 (standard output), and descriptor 2 (standard error). When the child terminates via <code>exit_group()</code>, the kernel reaps the process table entry and exposes an 8-bit unsigned status byte (0–255) to the parent via <code>waitpid()</code>.</p>
        <p>In Bash and POSIX-compliant shells, this status is captured in the volatile special parameter <code>$?</code>. A return value of <code>0</code> signifies successful completion according to the program contract, while non-zero values (1–255) denote specific error states (such as exit 127 for binary not found, or 126 for non-executable permissions). However, <code>$?</code> is critically volatile: <em>every</em> executed command—including subsequent debugging, logging, or echo statements—immediately overwrites this register. In automated pipelines and manual operations alike, failure to assign <code>status=$?</code> immediately after invocation destroys the failure signal, converting fatal errors into silent false-positive successes.</p>
        <p>The local filesystem and version control system impose distinct ownership boundaries. The local developer owns the workspace directory and working tree files. Git organizes state into three tiers: the working tree (mutable files on disk), the index/staging area (the proposed commit snapshot), and the object database under <code>.git/objects/</code> containing immutable, cryptographically hashed blobs, trees, and commit objects. Merely running a command in a terminal captures nothing into Git; conversely, a Git commit snapshot proves only that specific file contents existed at a recorded commit timestamp, not that a cloud infrastructure service was operational. Terminal stdout and stderr must be intentionally redirected into persistent evidence files and staged before Git can track them.</p>

        <table><caption>Day 1 architectural boundaries, control paths, and failure signals</caption><thead><tr><th>Architectural Boundary</th><th>Control &amp; Data Path</th><th>Ownership Domain</th><th>Enforcement Mechanism</th><th>Observable Failure Signals</th><th>Architectural Limit / Trade-off</th></tr></thead><tbody>
          <tr><td>Local Shell &amp; Environment</td><td>Input tokens → PATH resolution → environment variable expansion</td><td>Operator / Session</td><td>POSIX shell parser, shell options (<code>set -euo pipefail</code>)</td><td>Exit code 127 (binary missing); exit code 126 (unexecutable); unbound variable errors</td><td>Shell configuration is local and non-portable unless containerized or scripted.</td></tr>
          <tr><td>POSIX Process Subsystem</td><td><code>fork()</code> clone → <code>execve()</code> replacement → file descriptor table (0, 1, 2)</td><td>Kernel / Child Process</td><td>Kernel isolation, file descriptor redirection (<code>&gt;</code>, <code>2&gt;&amp;1</code>, pipes)</td><td>Exit code &gt; 0; broken pipe (SIGPIPE / 141); out of memory killer (SIGKILL / 137)</td><td>Status 0 verifies exit contract only; does not prove functional data validity.</td></tr>
          <tr><td>Status Register (<code>$?</code>)</td><td>Child termination → <code>waitpid()</code> status return → shell parameter assignment</td><td>POSIX Shell Runtime</td><td>Immediate variable capture (<code>status=$?</code>) or shell trap handlers</td><td>Register reset to 0 by intervening commands; masked failures in un-piped subshells</td><td>Register is ephemeral; a single logging statement destroys diagnostic history.</td></tr>
          <tr><td>Evidence Storage</td><td>Stream redirection → filesystem buffers → persistent file</td><td>Local Filesystem / OS</td><td>File write permissions, filesystem sync, integrity checks</td><td>Disk quota full; truncated output files; unbuffered write loss on crash</td><td>Terminal ANSI color escapes and control codes can corrupt plain-text diffs.</td></tr>
          <tr><td>Git Object Database</td><td>Working tree → index staging → object commit tree</td><td>Local Git Repository</td><td>SHA-1 / SHA-256 content hashing, tree immutability</td><td>Dirty working tree; merge conflicts; untracked modified files</td><td>Local commits are not remote backups; committing credentials leaks secrets permanently.</td></tr>
          <tr><td>Curriculum Capacity Model</td><td>Weekly hours allocation → complexity division → calendar pacing</td><td>Learner / Governance</td><td>Formula bounds (485.5h–665.0h) and tri-state skill gating</td><td>Prerequisite failure cascades; burnout; unearned advancement claims</td><td>Mathematical pacing is an estimate; does not account for unexpected life disruptions.</td></tr>
          <tr><td>Synthetic Data Boundary</td><td>Schema design → deterministic fixture synthesis → JSON validation</td><td>Security / Architecture</td><td>JSON Schema constraints, synthetic identifiers, zero PII checks</td><td>Schema validation error; customer PII patterns detected in logs or fixtures</td><td>Synthetic data cannot replicate subtle real-world production data edge cases.</td></tr>
          <tr><td>Cloud Billing Guardrail</td><td>Spend accumulation → Cloud Monitoring threshold → notification dispatch</td><td>FinOps / Project Owner</td><td>Billing budget rules, Pub/Sub topic events, email channels</td><td>Budget alert emails fired; unexpected spend velocity; quota exhaustion</td><td>Alerts notify humans; they do not automatically shut down compute resources.</td></tr>
        </tbody></table>
''')

# Insert Topology SVG
body_parts.append(svgs.get_topology_svg())

body_parts.append('''
        <div class="callout"><strong>Worked example to read before the lab</strong><p>This script executes an isolated Python command, traps its exit status into an explicit variable before any other command can run, and asserts that the status equals zero. Read and understand this sequence before executing the lab:</p><pre><code class="language-bash">python3 -c 'print("day-1-baseline-verification")'
status=$?
printf 'captured_exit_status: %s\\n' "$status"
if [ "$status" -ne 0 ]; then
  printf 'FATAL: Baseline command failed with exit code %s\\n' "$status" &gt;&amp;2
  exit "$status"
fi</code></pre><p>Expected output: <code>day-1-baseline-verification</code> followed by <code>captured_exit_status: 0</code>. If a non-zero exit status occurs, execution stops immediately before corrupted state can propagate.</p></div>
        <div class="further"><h4>Further Study</h4><p><a href="https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html#Exit-Status" rel="noopener noreferrer">GNU Bash Manual, §3.7.5 Exit Status</a> (verified 2026-09-26) defines the formal specification for shell exit statuses, command evaluation, and signal offsets. <a href="https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository" rel="noopener noreferrer">Pro Git, §2.2 Git Basics - Recording Changes to the Repository</a> (verified 2026-09-26) details the mechanics of staging files, index transitions, and commit immutability.</p></div>
      </article>

      <article id="learning-baseline-technical" class="topic-card"><span id="topic-02-technical" aria-hidden="true"></span><h3>Study sessions and learning baseline</h3>
        <p>Curriculum design in technical architecture requires separating curriculum units from elapsed calendar time. The 180 study units in this roadmap represent discrete, dense packages of architectural analysis, hands-on lab implementation, and validation gating. Aggregating the estimated study and lab durations across all units yields an estimated total effort envelope of 485.5 hours (minimum focused path) to 665.0 hours (comprehensive analysis including remediation). Treating one unit as equivalent to one calendar day implies an intensity of 2.7 to 3.7 hours every day without interruption for six consecutive months—a pacing model that leads directly to skipped labs, superficial skimming, and prerequisite debt.</p>
        <p>Architectural pacing must be calculated mathematically from the learner's actual weekly study capacity ($H$):</p>
        <pre><code class="language-text">Estimated Calendar Weeks = Curriculum Hours / Available Weekly Hours (H)
Minimum Pace Weeks = 485.5 / H
Maximum Pace Weeks = 665.0 / H</code></pre>
        <p>For an engineer with 8 available study hours per week, the roadmap spans 60.7 to 83.1 calendar weeks (approximately 14 to 19 months), before factoring in remediation cycles. Attempting to force an 8-hour weekly capacity into an arbitrary 6-month calendar deadline forces the omission of failure rehearsals and tabletop analysis.</p>
        <p>To prevent unverified progression, every skill topic throughout the 180 days is audited against an objective tri-state evaluation model:</p>
        <ul>
          <li><strong>New (Unstudied):</strong> The topic has not been engaged, or the learner cannot articulate its architectural mechanisms, boundaries, and failure signals.</li>
          <li><strong>Familiar (Conceptual Comprehension):</strong> The learner understands the terminology, can explain trade-offs and control flows verbally, and can identify appropriate cloud services, but has not personally executed or debugged the implementation.</li>
          <li><strong>Demonstrated (Auditable Competence):</strong> The learner has executed the implementation in a terminal, observed and recorded expected state, rehearsed bounded failure modes, and committed a reproducible artifact (command log, configuration manifest, or architectural decision record) to version control.</li>
        </ul>
        <p>On Day 1, local shell operations and Git commits transition to Demonstrated once the lab exercises complete. Cloud IAM, VPC peering, and Kubernetes remain classified as New; no cloud infrastructure has been provisioned, and claiming competence without artifact evidence violates architectural integrity.</p>
        <div class="further"><h4>Further Study</h4><p><a href="https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html#Exit-Status" rel="noopener noreferrer">GNU Bash Manual, §3.7.5 Exit Status</a> (verified 2026-09-26) reinforces why automated assertions and exit evaluations form the foundation of objective competence testing.</p></div>
      </article>

      <article id="budget-cleanup-technical" class="topic-card"><span id="topic-03-technical" aria-hidden="true"></span><h3>Synthetic data, budget and cleanup ownership</h3>
        <p>Cloud sandboxes must be governed under strict architectural constraints to prevent financial liability and data privacy violations. Two non-negotiable rules govern all hands-on exercises: synthetic data usage and explicit cleanup ownership.</p>
        <p>The synthetic data boundary mandates that production customer information, personally identifiable information (PII), live API keys, and real database dumps must never be imported into development or learning projects. Instead, schemas are modeled using invented, deterministic records (e.g., Brightloaf mock fixtures such as customer ID <code>SYNTHETIC-CUSTOMER-001</code> and SKU <code>BREAD-001</code>). In distributed architectures and event-driven pipelines, synthetic records must incorporate durable idempotency keys (such as <code>event_id</code> and <code>order_id</code>). Downstream processing consumers must maintain a deduplication check to enforce that duplicate delivery of an identical event payload results in exactly one business fulfillment, preventing duplicate shipments or multiple billing deductions during network replay.</p>
        <p>Google Cloud Billing budgets provide financial monitoring across cloud billing accounts and projects. A budget specifies a target amount (e.g., $50.00 USD/month) and evaluates actual and forecasted spend against configured threshold rules (such as 50%, 90%, and 100%). However, an architect must understand the technical boundary of standard billing budgets: <strong>budgets and budget alerts do not stop infrastructure or shut down virtual machines</strong>. A budget alert publishes metrics to Cloud Monitoring and sends notification emails or Cloud Pub/Sub messages. Without a custom programmatic receiver (such as a Cloud Function or Cloud Run service configured to disable billing or delete project resources), compute instances, persistent disks, and network gateways continue accruing hourly charges indefinitely regardless of budget thresholds.</p>
        <p>Consequently, cost control requires explicit human ownership. Before executing any future cloud lab, the learner must document: (1) target project ID, (2) provisioned resource names and regions, (3) dependency hierarchy, and (4) estimated hourly burn. Following lab verification, teardown must execute in strict reverse dependency order (dependents destroyed before dependencies, such as deleting Compute instances before subnets, and subnets before VPCs), followed by an inventory audit command confirming zero active resources.</p>
        <div class="further"><h4>Further Study</h4><p><a href="https://docs.cloud.google.com/billing/docs/how-to/budgets" rel="noopener noreferrer">Google Cloud Billing Documentation: Create, edit, or delete budgets and budget alerts</a> (verified 2026-09-26) details budget threshold rules, notification channels, and programmatic Pub/Sub integrations.</p></div>
      </article>
    </section>
''')

# Part 3
body_parts.append('''
    <section id="part-3" class="part"><h2>3 · Real-world problems and solutions</h2>
      <article id="workspace-repo-problem" class="topic-card"><span id="topic-01-problem" aria-hidden="true"></span><h3>Case 1 · Uncaptured Exit Status in CI/CD Release Gate</h3>
        <p><strong>Symptoms and observable evidence:</strong> In a production deployment pipeline for Brightloaf's retail ordering platform, an automated pre-deployment validation hook executed a database migration dry-run script (<code>validate_schema.sh</code>). The script encountered a syntax error and terminated with exit code 1. However, the wrapper pipeline script immediately executed an uncaptured logging statement: <code>echo "Validation script execution completed"</code>. The pipeline evaluation checked <code>$?</code> at the end of the step, observed <code>0</code> (the exit status of the <code>echo</code> command), and marked the validation stage as successful. The deployment proceeded to stage corrupt schema definitions into the staging environment, triggering immediate HTTP 500 errors across all active Order API instances.</p>
        <p><strong>Business and operational constraints:</strong> Brightloaf requires strict deployment gating where any schema or infrastructure mismatch halts releases automatically. Operational response time was impaired because deployment logs recorded "Validation completed successfully," misleading responders into investigating database connectivity rather than the failed schema script.</p>
        <p><strong>Causal root-cause reasoning:</strong> The shell variable <code>$?</code> is an ephemeral, volatile single-value register in memory. It retains the status of <em>only</em> the immediately preceding command. Because the wrapper script did not trap <code>status=$?</code> immediately after the validation command, the subsequent execution of <code>echo</code> destroyed the failure signal. The supplied facts prove the process returned code 1; architectural inference confirms that the un-trapped pipeline masked the defect.</p>
        <p><strong>Defensible engineering fix:</strong> Re-engineer the shell wrapper script to enforce strict exit trapping and pipeline failure propagation: (1) activate <code>set -euo pipefail</code> at the script header, ensuring any unhandled non-zero exit aborts the shell immediately; (2) explicitly capture <code>status=$?</code> into a named variable immediately following critical invocations; (3) redirect all stdout and stderr streams to a versioned, timestamped evidence file; and (4) assert that <code>[ "$status" -eq 0 ]</code> before executing any subsequent workflow stages.</p>
        <p><strong>Verification and evidence plan:</strong> Author an automated regression harness that simulates a failed migration script exiting with code 1. Verify that the wrapper script traps code 1, logs the standard error output to <code>evidence.log</code>, prints a fatal exit message, and terminates the pipeline with exit status 1 before deployment triggers.</p>
        <p><strong>Residual risk and ongoing guardrails:</strong> A script running under <code>set -e</code> can still mask errors if a failing command is executed inside an <code>if</code> condition or before an <code>||</code> operator. Ongoing pipeline linting with tools like ShellCheck must be integrated into repository pre-commit hooks to detect un-trapped pipeline commands.</p>
''')

body_parts.append(svgs.get_incident_svg_1())

body_parts.append('''
      </article>

      <article id="learning-baseline-problem" class="topic-card"><span id="topic-02-problem" aria-hidden="true"></span><h3>Case 2 · Calendar-Driven Progression Mistaken for Competence Baseline</h3>
        <p><strong>Symptoms and observable evidence:</strong> Brightloaf's cloud engineering management assigned an internal engineer to lead the architectural cutover of their production VPC interconnect and private DNS peering. The assignment was made because the engineer's calendar indicated that 12 weeks had elapsed since they started an internal cloud architecture training program. However, during the cutover window, a BGP route advertisement priority conflict caused traffic blackholing. The lead engineer was unable to interpret packet traces, verify routing table entries via the CLI, or diagnose asymmetric return paths, resulting in a 4-hour production outage and emergency rollback.</p>
        <p><strong>Business and operational constraints:</strong> Cutover windows require rapid, deterministic failure diagnosis under tight SLAs. The organization assumed that elapsed calendar duration correlated directly with technical competence, having established no objective evidence gates or artifact verification milestones.</p>
        <p><strong>Causal root-cause reasoning:</strong> The engineer had 4 hours of study availability per week, meaning 12 calendar weeks yielded only 48 hours of study time—less than 10% of the comprehensive curriculum. Because progress was tracked by calendar date rather than completed, committed artifacts, the engineer skimmed complex networking modules without performing hands-on packet inspection or failure injection labs. "Familiarity" with terminology was mistaken for operational capability.</p>
        <p><strong>Defensible engineering fix:</strong> Overhaul technical progression governance: (1) mandate mathematical capacity modeling where curriculum pacing is calculated from verified weekly study hours; (2) institute the tri-state competence evaluation framework (New, Familiar, Demonstrated); (3) require that no engineer be assigned to architectural cutovers without committed terminal evidence, reproducible configuration scripts, and documented failure rehearsal logs in their evidence repository; and (4) allocate explicit 20% remediation buffers for complex networking and distributed systems topics.</p>
        <p><strong>Verification and evidence plan:</strong> Perform an objective baseline review of the engineer's repository. Verify that prior to scheduling the next cutover, the engineer reproduces the BGP route priority conflict in a local or simulated lab environment, captures route tables and packet flow telemetry, and commits an architectural post-mortem and remediation runbook.</p>
        <p><strong>Residual risk and ongoing guardrails:</strong> Self-reporting of study hours and skill ratings can suffer from optimism bias. Periodic peer reviews of committed lab evidence and structured tabletop failure challenges must serve as exit gates before production cutover authorizations.</p>
''')

body_parts.append(svgs.get_incident_svg_2())

body_parts.append('''
      </article>

      <article id="budget-cleanup-problem" class="topic-card"><span id="topic-03-problem" aria-hidden="true"></span><h3>Case 3 · Production Customer Export Leak and Runaway Sandbox Billing</h3>
        <p><strong>Symptoms and observable evidence:</strong> An engineer preparing a proof-of-concept for Brightloaf's order streaming service exported 50,000 real customer records from production—including customer names, physical addresses, and order histories—and loaded them into a Google Cloud Storage bucket in a personal sandbox project. To test streaming throughput, the engineer launched two <code>n2-standard-16</code> Compute Engine instances with attached SSDs. The engineer configured a $50/month Cloud Billing budget alert. Over the weekend, the budget alert fired at 100%, sending an email notification to the engineer's inbox. Because no one monitored the inbox over the weekend, the instances continued running, accruing $1,400 in compute and network egress charges. Furthermore, during a mock failure recovery drill, an order consumer re-processed the event stream without idempotency deduplication, creating 12,000 duplicate fulfillment orders in the test database.</p>
        <p><strong>Business and operational constraints:</strong> The company faced regulatory notification obligations due to customer PII residing in an unmonitored sandbox project. In addition, the unexpected billing spike depleted the team's monthly discretionary innovation budget.</p>
        <p><strong>Causal root-cause reasoning:</strong> The incident resulted from three compounding failures: (1) importing real customer data into an unmonitored sandbox instead of using synthetic data fixtures; (2) relying on an advisory Cloud Billing budget alert under the false assumption that it would stop compute resources when the budget was exceeded; and (3) designing an event consumer without a durable deduplication key, violating the business invariant of exactly one fulfillment per order.</p>
        <p><strong>Defensible engineering fix:</strong> Establish a binding Sandbox Governance Charter: (1) enforce an absolute prohibition against production data in non-production environments, mandating synthetic JSON fixtures with zero PII; (2) implement a mandatory teardown checklist requiring reverse-dependency resource deletion following every lab session; (3) assign a named human cleanup owner accountable for project inventory; and (4) refactor event consumers to enforce an idempotent deduplication invariant: check whether <code>event_id</code> or <code>order_id</code> has already been fulfilled in a durable database before processing fulfillment logic, rejecting duplicates immediately.</p>
        <p><strong>Verification and evidence plan:</strong> Inspect the repository for committed synthetic fixtures (<code>fixtures/synthetic-order.json</code>) and verify that automated regex scanners find zero real credit card, email, or address patterns. Run an automated replay test passing duplicate event payloads to the consumer; assert that the first event succeeds and the second event is logged as a duplicate with zero secondary fulfillments created.</p>
        <p><strong>Residual risk and ongoing guardrails:</strong> Manual teardown checklists rely on human diligence. Future cloud projects (from Day 18 onwards) must incorporate automated project-level scheduled shutdown functions (via Cloud Scheduler and Cloud Functions) and Organization Policy constraints that prevent public bucket creation.</p>
''')

body_parts.append(svgs.get_incident_svg_3())

body_parts.append('''
      </article>
    </section>
''')

# Part 4: Step-by-Step Labs
body_parts.append('''
    <section id="part-4" class="part"><h2>4 · Step-by-step labs</h2>
      <article id="workspace-repo-lab" class="topic-card lab"><span id="topic-01-lab" aria-hidden="true"></span><h3>Exercise 1: Local Workspace Initialization, Exit Status Capture, and Evidence Repository</h3>
        <p><strong>Goal:</strong> Initialize a dedicated local Git repository, execute an external Python command via a hardened shell harness, capture process standard streams and immediate exit codes, and commit the verified observation artifact.</p>
        <p><strong>Expected result:</strong> An initialized Git repository at <code>$HOME/gcp-architect-learning</code> containing a committed <code>command-observation.txt</code> capturing exit status 0 and a clean Git status.</p>
        <p><strong>Mode:</strong> local Linux shell &amp; tabletop analysis · <strong>Prerequisite:</strong> Standard Bash shell, Git, and Python 3 installed.</p>
        <p><strong>Preflight:</strong> Verify that local tools are operational and the target directory does not conflict with existing files.</p>

        <h4>Exact execution</h4>
        <ol>
          <li><h4>Stage 1: Preflight and Environment Validation</h4>
            <p>Verify that Bash, Git, and Python 3 binaries are present in the system PATH and print their versions:</p>
            <pre><code class="language-bash">bash -c '
command -v bash
command -v git
command -v python3
git --version
python3 --version
'</code></pre>
            <p>Expected output: valid file paths for all three tools, Git version 2.x+, and Python version 3.8+.</p>
          </li>

          <li><h4>Stage 2: Target Directory and Workspace Preparation</h4>
            <p>Ensure the target repository path does not already exist, create the directory structure, and initialize the Git repository:</p>
            <pre><code class="language-bash">bash -c '
WORKSPACE="$HOME/gcp-architect-learning"
if [ -d "$WORKSPACE" ]; then
  echo "Target directory $WORKSPACE already exists; preserving existing state."
else
  mkdir -p "$WORKSPACE"
  cd "$WORKSPACE"
  git init
  echo "Initialized empty Git repository in $WORKSPACE"
fi
'</code></pre>
            <p>Expected output: confirmation that the repository was initialized in <code>$HOME/gcp-architect-learning</code>.</p>
          </li>

          <li><h4>Stage 3: Configuration and Script Authoring</h4>
            <p>Author an execution harness script <code>run_and_capture.sh</code> that executes an external command, captures stdout/stderr, and immediately traps <code>status=$?</code> before any other command can overwrite it:</p>
            <pre><code class="language-bash">cat &lt;&lt;\'EOF_SCRIPT\' &gt; "$HOME/gcp-architect-learning/run_and_capture.sh"
#!/usr/bin/env bash
set -uo pipefail

TARGET_CMD="${1:-python3 -c 'print(\\"baseline-signal-ok\\")'}"
OBSERVATION_FILE="$HOME/gcp-architect-learning/command-observation.txt"

echo "Executing: $TARGET_CMD"
eval "$TARGET_CMD" &gt; /tmp/cmd_stdout.tmp 2&gt; /tmp/cmd_stderr.tmp
status=$?

{
  echo "=== COMMAND OBSERVATION ==="
  echo "Timestamp: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  echo "Command: $TARGET_CMD"
  echo "Exit Status: $status"
  echo "--- STDOUT ---"
  cat /tmp/cmd_stdout.tmp
  echo "--- STDERR ---"
  cat /tmp/cmd_stderr.tmp
} &gt; "$OBSERVATION_FILE"

rm -f /tmp/cmd_stdout.tmp /tmp/cmd_stderr.tmp
echo "Execution complete; status=$status saved to $OBSERVATION_FILE"
exit "$status"
EOF_SCRIPT
chmod +x "$HOME/gcp-architect-learning/run_and_capture.sh"</code></pre>
            <p>Expected output: executable script created at <code>$HOME/gcp-architect-learning/run_and_capture.sh</code>.</p>
          </li>

          <li><h4>Stage 4: Execution of Baseline Process and Exit Status Capture</h4>
            <p>Execute the authored harness with a baseline Python print command to record normal zero-exit behavior:</p>
            <pre><code class="language-bash">bash "$HOME/gcp-architect-learning/run_and_capture.sh" "python3 -c 'print(\\"day-1-baseline-signal\\")'"</code></pre>
            <p>Expected output: <code>baseline-signal</code> printed, status=0 reported, and output persisted.</p>
          </li>

          <li><h4>Stage 5: Expected State Inspection and Outcome Verification</h4>
            <p>Inspect the generated observation file to verify that the exit status and stdout streams were recorded accurately:</p>
            <pre><code class="language-bash">cat "$HOME/gcp-architect-learning/command-observation.txt"
grep -q "Exit Status: 0" "$HOME/gcp-architect-learning/command-observation.txt" &amp;&amp; echo "ASSERTION PASS: Exit status is 0"
grep -q "day-1-baseline-signal" "$HOME/gcp-architect-learning/command-observation.txt" &amp;&amp; echo "ASSERTION PASS: Stdout matched"</code></pre>
            <p>Expected output: two <code>ASSERTION PASS</code> messages confirming correct status capture and stream logging.</p>
          </li>

          <li><h4>Stage 6: Bounded Failure Rehearsal and Edge-Case Handling</h4>
            <p>Rehearse a bounded failure by executing a command that explicitly exits with non-zero code 42, verifying that the harness preserves the non-zero status without crashing or masking:</p>
            <pre><code class="language-bash">bash "$HOME/gcp-architect-learning/run_and_capture.sh" "python3 -c 'import sys; sys.stderr.write(\\"injected-error\\\\n\\"); sys.exit(42)'" || test_status=$?
echo "Harness returned test_status: ${test_status:-0}"
grep "Exit Status: 42" "$HOME/gcp-architect-learning/command-observation.txt"
grep "injected-error" "$HOME/gcp-architect-learning/command-observation.txt"</code></pre>
            <p>Expected output: test_status 42 reported, observation file contains <code>Exit Status: 42</code> and <code>injected-error</code> in stderr.</p>
          </li>

          <li><h4>Stage 7: Evidence Diagnosis, Remediation, and Git Staging</h4>
            <p>Re-run the baseline command to restore a passing observation artifact, create the initial repository README, and stage both files into Git:</p>
            <pre><code class="language-bash">bash "$HOME/gcp-architect-learning/run_and_capture.sh" "python3 -c 'print(\\"day-1-baseline-signal\\")'"
cat &lt;&lt;EOF &gt; "$HOME/gcp-architect-learning/README.md"
# GCP Architect Learning Evidence

- Environment: $(uname -s) $(uname -m)
- Local Shell: $(basename "$SHELL")
- Workspace: $HOME/gcp-architect-learning
EOF
git -C "$HOME/gcp-architect-learning" add README.md command-observation.txt run_and_capture.sh</code></pre>
            <p>Expected output: passing baseline restored, README.md created, files staged in Git.</p>
          </li>

          <li><h4>Stage 8: Repository State Verification and Clean Teardown</h4>
            <p>Commit the staged files with an explicit author identity, verify that the Git working tree is completely clean, and display the commit log:</p>
            <pre><code class="language-bash">git -C "$HOME/gcp-architect-learning" -c user.name="Learner" -c user.email="learner@example.invalid" commit -m "Record Day 1 local baseline and exit capture harness"
if [ -z "$(git -C "$HOME/gcp-architect-learning" status --porcelain)" ]; then
  echo "VERIFICATION PASS: Git working tree is clean."
else
  echo "VERIFICATION FAIL: Working tree is dirty." &gt;&amp;2
fi
git -C "$HOME/gcp-architect-learning" log -1 --oneline</code></pre>
            <p>Expected output: commit subject recorded, <code>VERIFICATION PASS</code> printed, clean working tree confirmed.</p>
          </li>
        </ol>

        <div class="callout success"><strong>Expected result / acceptance</strong><p>The Git repository contains a clean committed state with <code>run_and_capture.sh</code>, <code>command-observation.txt</code>, and <code>README.md</code>. Process exit status 0 and stream contents are verified.</p><p><strong>Artifact acceptance:</strong> File <code>command-observation.txt</code> exists, records status 0, and matches the commit hash in the Git log.</p></div>
        <div class="callout caution"><strong>Troubleshooting</strong><p>If Git complains about missing user name or email, use the <code>-c user.name=... -c user.email=...</code> options as demonstrated to commit without altering global workstation Git settings.</p></div>
        <div class="callout"><strong>Cleanup and cost</strong><p>Retain the repository at <code>$HOME/gcp-architect-learning</code> as the persistent foundation for all subsequent day labs. No cloud resources created; zero cost accrued.</p></div>
        <label class="check"><input data-progress="lab-1-topic-01" type="checkbox"/> I completed and checked this topic exercise</label>
      </article>

      <article id="learning-baseline-lab" class="topic-card lab"><span id="topic-02-lab" aria-hidden="true"></span><h3>Exercise 2: Study Capacity Calculation, Calendar Pacing, and Skills Baseline Worksheet</h3>
        <p><strong>Goal:</strong> Calculate realistic curriculum calendar ranges based on empirical weekly study hours, evaluate baseline technical skills under the tri-state evidence model, and commit the planning charter to the evidence repository.</p>
        <p><strong>Expected result:</strong> A mathematical pacing table and tri-state skills matrix committed to <code>$HOME/gcp-architect-learning/README.md</code>.</p>
        <p><strong>Mode:</strong> local Python calculation &amp; evidence worksheet · <strong>Prerequisite:</strong> Completed Exercise 1 repository.</p>
        <p><strong>Preflight:</strong> Verify that the repository created in Exercise 1 is accessible and clean.</p>

        <h4>Exact execution</h4>
        <ol>
          <li><h4>Stage 1: Preflight and Capacity Parameter Validation</h4>
            <p>Verify repository existence and test Python calculation capability:</p>
            <pre><code class="language-bash">test -d "$HOME/gcp-architect-learning/.git" &amp;&amp; echo "Repository verified."
python3 -c 'print("Python math environment ready.")'</code></pre>
            <p>Expected output: <code>Repository verified.</code> and <code>Python math environment ready.</code>.</p>
          </li>

          <li><h4>Stage 2: Input Data Preparation and Available Hours Audit</h4>
            <p>Define available weekly study hours (default example: 8.0 hours/week) and define the curriculum hours envelope:</p>
            <pre><code class="language-bash">cat &lt;&lt;\'EOF_JSON\' &gt; "$HOME/gcp-architect-learning/pacing_params.json"
{
  "weekly_available_hours": 8.0,
  "curriculum_min_hours": 485.5,
  "curriculum_max_hours": 665.0,
  "remediation_contingency_pct": 0.20
}
EOF_JSON
cat "$HOME/gcp-architect-learning/pacing_params.json"</code></pre>
            <p>Expected output: JSON parameters file verified on disk.</p>
          </li>

          <li><h4>Stage 3: Calculation Script Authoring</h4>
            <p>Author a Python script <code>calculate_capacity.py</code> to compute pacing ranges, buffer margins, and generate formatted Markdown for the README:</p>
            <pre><code class="language-bash">cat &lt;&lt;\'EOF_PY\' &gt; "$HOME/gcp-architect-learning/calculate_capacity.py"
import json
from pathlib import Path

params_path = Path("pacing_params.json")
with open(params_path) as f:
    params = json.load(f)

h = float(params["weekly_available_hours"])
min_h = float(params["curriculum_min_hours"])
max_h = float(params["curriculum_max_hours"])
contingency = float(params["remediation_contingency_pct"])

min_weeks = min_h / h
max_weeks = max_h / h
buffered_min_weeks = min_weeks * (1.0 + contingency)
buffered_max_weeks = max_weeks * (1.0 + contingency)

markdown_output = f"""
## Study Capacity and Learning Baseline

- **Available Weekly Study Hours:** {h:g} hours/week
- **Curriculum Total Effort:** {min_h} to {max_h} hours across 180 study units
- **Nominal Calendar Pacing:** {min_weeks:.1f} to {max_weeks:.1f} calendar weeks ({min_weeks/4.33:.1f} to {max_weeks/4.33:.1f} months)
- **Remediation-Buffered Pacing (+20%):** {buffered_min_weeks:.1f} to {buffered_max_weeks:.1f} calendar weeks
- **Governance Rule:** Study units are units of work, not consecutive calendar dates.

### Initial Technical Skills Inventory (Tri-State Model)

| Skill Domain | Status | Evidence Artifact / Verification |
| :--- | :--- | :--- |
| Local POSIX Shell &amp; Exit Status Capture | Demonstrated | Committed run_and_capture.sh and command-observation.txt |
| Git Index Staging &amp; Commit History | Demonstrated | Committed Day 1 local evidence repository |
| Capacity-Based Pacing &amp; Pacing Model | Demonstrated | Committed calculate_capacity.py and parameters |
| Synthetic Data Design &amp; Schema Validation | In Progress | Day 1 Exercise 3 synthetic order fixture |
| Google Cloud IAM &amp; Resource Hierarchy | New | Unstudied; begins Day 18 |
| VPC Networking &amp; Hybrid Connectivity | New | Unstudied; begins Day 2 / Day 22 |
| Google Kubernetes Engine &amp; Cloud Run | New | Unstudied; begins Day 68 |
"""

print(f"Computed nominal pace: {min_weeks:.1f} - {max_weeks:.1f} weeks at {h:g} hrs/wk")
with open("pacing_summary.md", "w") as f:
    f.write(markdown_output)
EOF_PY</code></pre>
            <p>Expected output: script authored at <code>$HOME/gcp-architect-learning/calculate_capacity.py</code>.</p>
          </li>

          <li><h4>Stage 4: Execution of Pacing Analysis</h4>
            <p>Execute the calculation script inside the repository directory:</p>
            <pre><code class="language-bash">cd "$HOME/gcp-architect-learning"
python3 calculate_capacity.py</code></pre>
            <p>Expected output: <code>Computed nominal pace: 60.7 - 83.1 weeks at 8 hrs/wk</code>.</p>
          </li>

          <li><h4>Stage 5: Expected State Inspection and Skills Baseline Mapping</h4>
            <p>Inspect the generated markdown to verify calculation accuracy and skill audit ratings:</p>
            <pre><code class="language-bash">cat "$HOME/gcp-architect-learning/pacing_summary.md"
grep -q "60.7 to 83.1 calendar weeks" "$HOME/gcp-architect-learning/pacing_summary.md" &amp;&amp; echo "ASSERTION PASS: Pacing calculation verified."</code></pre>
            <p>Expected output: markdown table displayed, assertion passes.</p>
          </li>

          <li><h4>Stage 6: Bounded Failure Rehearsal: Schedule Slip &amp; Remediation Stress Test</h4>
            <p>Simulate a constrained study scenario where weekly capacity drops from 8 hours to 4 hours, and verify that the model recalculates the extended timeline without altering curriculum depth:</p>
            <pre><code class="language-bash">cd "$HOME/gcp-architect-learning"
python3 -c '
import json
with open("pacing_params.json") as f:
    p = json.load(f)
p["weekly_available_hours"] = 4.0
min_w = p["curriculum_min_hours"] / 4.0
max_w = p["curriculum_max_hours"] / 4.0
print(f"STRESS TEST: At 4.0 hrs/wk, pace expands to {min_w:.1f} - {max_w:.1f} weeks ({min_w/4.33:.1f} - {max_w/4.33:.1f} months).")
'</code></pre>
            <p>Expected output: <code>STRESS TEST: At 4.0 hrs/wk, pace expands to 121.4 - 166.2 weeks (28.0 - 38.4 months).</code></p>
          </li>

          <li><h4>Stage 7: Evidence Diagnosis and README Incorporation</h4>
            <p>Append the validated pacing summary and skills inventory to the root <code>README.md</code>:</p>
            <pre><code class="language-bash">cd "$HOME/gcp-architect-learning"
cat pacing_summary.md &gt;&gt; README.md
git add README.md calculate_capacity.py pacing_params.json</code></pre>
            <p>Expected output: updated README with pacing summary, files staged.</p>
          </li>

          <li><h4>Stage 8: Version Control Commit and Baseline Closeout</h4>
            <p>Commit the capacity plan and verify clean repository status:</p>
            <pre><code class="language-bash">cd "$HOME/gcp-architect-learning"
git -c user.name="Learner" -c user.email="learner@example.invalid" commit -m "Record Day 1 study capacity and skills baseline"
if [ -z "$(git status --porcelain)" ]; then
  echo "VERIFICATION PASS: Working tree is clean."
fi
git log -2 --oneline</code></pre>
            <p>Expected output: commit subject recorded, clean status verified.</p>
          </li>
        </ol>

        <div class="callout success"><strong>Expected result / acceptance</strong><p>The committed <code>README.md</code> contains weekly available hours, estimated calendar range, remediation contingency, and tri-state skills ratings.</p><p><strong>Artifact acceptance:</strong> File <code>README.md</code> includes calculated week ranges and skills inventory; Git history shows clean commit.</p></div>
        <div class="callout caution"><strong>Troubleshooting</strong><p>If Python raises a division by zero error, verify that <code>weekly_available_hours</code> in <code>pacing_params.json</code> is strictly greater than 0.</p></div>
        <div class="callout"><strong>Cleanup and cost</strong><p>Retain the pacing scripts and README in the repository; zero cloud spend accrued.</p></div>
        <label class="check"><input data-progress="lab-1-topic-02" type="checkbox"/> I recorded my real hours and evidence-based skill baseline</label>
      </article>

      <article id="budget-cleanup-lab" class="topic-card lab"><span id="topic-03-lab" aria-hidden="true"></span><h3>Exercise 3: Synthetic Data Fixture Authoring, Idempotent Event Replay, and Sandbox Budget Governance</h3>
        <p><strong>Goal:</strong> Author a valid synthetic order fixture adhering to zero-PII principles, implement an automated test verifying idempotent event replay deduplication, and codify a sandbox budget and cleanup charter in version control.</p>
        <p><strong>Expected result:</strong> A validated synthetic JSON fixture at <code>fixtures/synthetic-order.json</code>, an idempotency replay simulation script, and a sandbox governance charter in <code>README.md</code>.</p>
        <p><strong>Mode:</strong> local JSON schema validation &amp; governance charter · <strong>Prerequisite:</strong> Completed Exercises 1 and 2.</p>
        <p><strong>Preflight:</strong> Verify Python <code>json</code> module and confirm working tree cleanliness.</p>

        <h4>Exact execution</h4>
        <ol>
          <li><h4>Stage 1: Preflight and Environment Inspection</h4>
            <p>Verify that Python's standard <code>json</code> module is available and inspect working directory:</p>
            <pre><code class="language-bash">cd "$HOME/gcp-architect-learning"
python3 -c 'import json; print("Standard library json module ready.")'
test -f README.md &amp;&amp; echo "Target README verified."</code></pre>
            <p>Expected output: confirmation that JSON module is ready and README is verified.</p>
          </li>

          <li><h4>Stage 2: Fixture Schema and Target Directory Preparation</h4>
            <p>Create the <code>fixtures</code> directory to house synthetic test data:</p>
            <pre><code class="language-bash">mkdir -p "$HOME/gcp-architect-learning/fixtures"
echo "Created fixtures directory."</code></pre>
            <p>Expected output: <code>Created fixtures directory.</code>.</p>
          </li>

          <li><h4>Stage 3: Synthetic Order Fixture Authoring</h4>
            <p>Author <code>fixtures/synthetic-order.json</code> using strictly synthetic Brightloaf business entities and explicit event replay keys:</p>
            <pre><code class="language-bash">cat &lt;&lt;\'EOF_ORDER\' &gt; "$HOME/gcp-architect-learning/fixtures/synthetic-order.json"
{
  "event_id": "evt-2026-09-29-synthetic-001",
  "order_id": "bl-ord-synthetic-8821",
  "timestamp": "2026-09-29T12:00:00Z",
  "customer": {
    "customer_id": "cust-synth-402",
    "customer_type": "retail_synthetic",
    "region": "us-central1"
  },
  "line_items": [
    {
      "item_sku": "SKU-SOURDOUGH-01",
      "quantity": 24,
      "unit_price_usd": 4.50
    },
    {
      "item_sku": "SKU-BRIOCHE-02",
      "quantity": 12,
      "unit_price_usd": 6.00
    }
  ],
  "total_amount_usd": 180.00,
  "currency": "USD",
  "fulfillment_status": "PENDING"
}
EOF_ORDER</code></pre>
            <p>Expected output: valid synthetic JSON fixture written to <code>fixtures/synthetic-order.json</code>.</p>
          </li>

          <li><h4>Stage 4: Execution of Schema Validation and PII Audit</h4>
            <p>Execute a Python audit script verifying JSON syntax and asserting that no production PII patterns exist:</p>
            <pre><code class="language-bash">python3 -c '
import json, re
with open("$HOME/gcp-architect-learning/fixtures/synthetic-order.json".replace("$HOME", "'"$HOME"'")) as f:
    data = json.load(f)

# Assert mandatory schema keys
assert "event_id" in data and "order_id" in data
assert "total_amount_usd" in data
assert data["total_amount_usd"] == 180.00

# PII regex scan (email, ssn, phone patterns)
raw = json.dumps(data)
assert not re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", raw), "PII violation: Email found"
assert not re.search(r"\\b\\d{3}-\\d{2}-\\d{4}\\b", raw), "PII violation: SSN found"
print("ASSERTION PASS: Synthetic schema valid; zero PII detected.")
'</code></pre>
            <p>Expected output: <code>ASSERTION PASS: Synthetic schema valid; zero PII detected.</code>.</p>
          </li>

          <li><h4>Stage 5: Expected State Inspection: Idempotent Event Replay Simulation</h4>
            <p>Author and execute an idempotency simulation testing duplicate event replay against an in-memory processed-event ledger, verifying that the order is fulfilled exactly once:</p>
            <pre><code class="language-bash">cat &lt;&lt;\'EOF_REPLAY\' &gt; "$HOME/gcp-architect-learning/test_replay.py"
import json
from pathlib import Path

fixture_path = Path("fixtures/synthetic-order.json")
with open(fixture_path) as f:
    event = json.load(f)

processed_events = set()
fulfillment_ledger = []

def process_order_event(evt):
    eid = evt["event_id"]
    oid = evt["order_id"]
    if eid in processed_events:
        return {"status": "DUPLICATE_REJECTED", "event_id": eid, "action": "NOOP"}
    processed_events.add(eid)
    fulfillment_ledger.append({"order_id": oid, "amount": evt["total_amount_usd"]})
    return {"status": "FULFILLED", "event_id": eid, "action": "INVENTORY_RESERVED"}

# Initial event arrival
res1 = process_order_event(event)
# Replay event arrival (network retry / duplicate delivery)
res2 = process_order_event(event)

print(f"Arrival 1: status={res1['status']}, action={res1['action']}")
print(f"Arrival 2 (Replay): status={res2['status']}, action={res2['action']}")
print(f"Total business fulfillments executed: {len(fulfillment_ledger)}")

assert res1["status"] == "FULFILLED"
assert res2["status"] == "DUPLICATE_REJECTED"
assert len(fulfillment_ledger) == 1, "FATAL: Duplicate business fulfillment executed!"
print("ASSERTION PASS: Idempotent event replay contract verified.")
EOF_REPLAY
cd "$HOME/gcp-architect-learning"
python3 test_replay.py</code></pre>
            <p>Expected output: Arrival 1 FULFILLED, Arrival 2 DUPLICATE_REJECTED, Total fulfillments = 1, assertion passes.</p>
          </li>

          <li><h4>Stage 6: Bounded Failure Rehearsal: Alert-Only Budget Runaway Modeling</h4>
            <p>Simulate a budget overrun scenario demonstrating why standard Google Cloud Billing budgets do not halt compute spending without automated scripts:</p>
            <pre><code class="language-bash">cat &lt;&lt;\'EOF_BUDGET\' &gt; "$HOME/gcp-architect-learning/simulate_budget_drift.py"
budget_target = 50.00
hourly_instance_cost = 0.76  # n2-standard-16 illustrative rate ($/hr)
hours_weekend = 60.0         # Friday 6pm to Monday 6am

weekend_spend = hourly_instance_cost * hours_weekend * 2  # 2 active nodes
total_spend = weekend_spend

print(f"Configured Budget Target: ${budget_target:.2f}")
print(f"Accrued Weekend Spend: ${total_spend:.2f}")
print(f"Budget Threshold Exceeded: {total_spend > budget_target}")
print("OBSERVATION: Cloud Billing budget alert sends email notification at $50.00;")
print("WITHOUT programmatic shutdown, VMs continue running, generating ${:.2f} overrun.".format(total_spend - budget_target))
EOF_BUDGET
cd "$HOME/gcp-architect-learning"
python3 simulate_budget_drift.py</code></pre>
            <p>Expected output: calculation displaying the $41.20 overrun beyond the $50 target, demonstrating why cleanup ownership is essential.</p>
          </li>

          <li><h4>Stage 7: Sandbox Governance Charter Authoring</h4>
            <p>Append the formal Sandbox Governance Charter to the repository <code>README.md</code>:</p>
            <pre><code class="language-bash">cd "$HOME/gcp-architect-learning"
cat &lt;&lt;\'EOF_CHARTER\' &gt;&gt; README.md

## Sandbox Governance &amp; Cost Control Charter

- **Monthly Sandbox Spend Target:** $50.00 USD
- **Alert Thresholds:** 50% ($25.00), 90% ($45.00), 100% ($50.00)
- **Designated Cleanup Owner:** Learner (Primary Operational Accountability)
- **Synthetic Data Boundary:** Production customer records and live secrets are strictly prohibited. All lab fixtures must reside in `fixtures/` with zero PII.
- **Billing Budget Limitation Notice:** Google Cloud Billing budgets are notification-only mechanisms. They do not automatically terminate compute, storage, or networking resources.
- **Pre-Lab Requirement:** Before provisioning resources in Day 18+ cloud labs, document target project, resource IDs, regions, and estimated burn rate.
- **Teardown Protocol:** Always delete resources in reverse dependency order (compute instances before subnets, subnets before VPCs). Execute inventory commands post-teardown to confirm clean project state.
- **Idempotency Invariant:** All event-driven consumers must enforce durable deduplication on `event_id` to guarantee exactly one business fulfillment per order.
EOF_CHARTER
git add README.md fixtures/synthetic-order.json test_replay.py simulate_budget_drift.py</code></pre>
            <p>Expected output: governance charter appended to README.md and all files staged in Git.</p>
          </li>

          <li><h4>Stage 8: Final Repository Staging, Commit, and Clean Verification</h4>
            <p>Commit the synthetic fixture and governance charter, confirming zero uncommitted files remain:</p>
            <pre><code class="language-bash">cd "$HOME/gcp-architect-learning"
git -c user.name="Learner" -c user.email="learner@example.invalid" commit -m "Record Day 1 sandbox charter, synthetic fixtures, and idempotency tests"
if [ -z "$(git status --porcelain)" ]; then
  echo "VERIFICATION PASS: All Day 1 learning evidence committed; working tree is clean."
fi
git log -3 --oneline</code></pre>
            <p>Expected output: commit subject recorded, <code>VERIFICATION PASS</code> printed, clean tree confirmed.</p>
          </li>
        </ol>

        <div class="callout success"><strong>Expected result / acceptance</strong><p>Synthetic fixture <code>fixtures/synthetic-order.json</code> parses cleanly with zero PII, <code>test_replay.py</code> asserts single business fulfillment under duplicate delivery, and the sandbox charter is committed.</p><p><strong>Artifact acceptance:</strong> Valid synthetic order fixture, passing idempotency script, and committed sandbox charter in <code>README.md</code>.</p></div>
        <div class="callout caution"><strong>Troubleshooting</strong><p>Ensure JSON fixtures use double quotes around keys and string values. Single quotes are invalid JSON syntax and will fail parsing.</p></div>
        <div class="callout"><strong>Cleanup and cost</strong><p>Retain the synthetic fixtures and idempotency scripts in Git. No cloud infrastructure created; total cloud spend for Day 1 is $0.00.</p></div>
        <label class="check"><input data-progress="lab-1-topic-03" type="checkbox"/> I committed the synthetic fixture and sandbox charter</label>
      </article>
    </section>
''')

# Completion section
body_parts.append('''
    <section class="completion"><h2>Daily evidence</h2>
      <p>Keep the local Git repository at <code>$HOME/gcp-architect-learning</code> intact. It contains your committed <code>README.md</code> (with study capacity calculations, tri-state skills inventory, and sandbox charter), <code>run_and_capture.sh</code> with <code>command-observation.txt</code>, and <code>fixtures/synthetic-order.json</code> with the verified idempotency replay test. These artifacts serve as the concrete entrance prerequisite for the upcoming foundations days.</p>
      <label class="check"><input type="checkbox" data-progress="read-1"> I reviewed all four parts</label>
      <label class="check"><input type="checkbox" data-progress="artifact-1"> I saved and checked the Day 1 exit artifact</label>
    </section>
    <nav class="pager" aria-label="Day pagination"><a href="../index.html">Roadmap index<small>Browse all study days</small></a><a href="day-002.html">Day 2 →<small>IP addressing and packet paths</small></a></nav>
    <p class="shortcut">Keyboard: N or ] next · I index</p>
  </main>
''')

full_html = head_and_header + "".join(body_parts) + "\n" + footer_and_end

out_path = Path("content/day-001-page.html")
out_path.write_text(full_html, encoding="utf-8")
print(f"Wrote {len(full_html)} bytes to {out_path}")
