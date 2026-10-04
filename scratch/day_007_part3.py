#!/usr/bin/env python3
"""Topic 3 technical text for Day 7."""

TOPIC_03_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ol>
<li>Shell startup, environment inheritance, and subshell isolation</li>
<li>Parameter expansion, strict quoting, and word splitting vulnerabilities</li>
<li>Control structures: loops (for, while), conditionals ([[ ... ]]), and pattern matching</li>
<li>Process execution, pipelines (set -o pipefail), and exit status evaluation ($?)</li>
<li>Defensive scripting standards: set -euo pipefail, trap handlers, and secure parsing of structured payloads (JSON)</li>
</ol>

<h4>Shell startup, environment inheritance, and subshell isolation</h4>
<p><strong class="side-heading">What it is in general:</strong> When a Linux shell starts, it determines execution context based on invocation flags: an <strong class="keyword">interactive login shell</strong> reads <code>/etc/profile</code> and <code>~/.bash_profile</code>, while an <strong class="keyword">interactive non-login shell</strong> reads <code>~/.bashrc</code>. Non-interactive script executions run with a minimal environment, inheriting only variables explicitly marked for export via <kbd>export VAR=val</kbd>. Subshells—spawned via parentheses <code>( command )</code>, command substitutions <code>$( command )</code>, or asynchronous background jobs <code>&amp;</code>—receive a duplicate of the parent process memory space but cannot mutate parent shell variables, working directories, or file descriptors.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects frequently encounter script failures caused by divergent environment assumptions between interactive developer testing and automated cloud execution (e.g. systemd services, cron jobs, or container entrypoints) that execute non-login shells lacking custom <code>PATH</code> entries or proxy configurations.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine instance startup scripts execute non-interactively as the root user directly from the Google Cloud Guest Agent environment. They do not source user profile scripts: all paths, credentials, and environment variables must be declared explicitly within the script. Primary documentation: <a href="https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION">bash(1) GNU Bourne-Again SHell description (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION">bash(1) INVOCATION and ENVIRONMENT sections (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man1/env.1.html#DESCRIPTION">env(1) environment export command (accessed 2026-10-04)</a>.</p>

<h4>Parameter expansion, strict quoting, and word splitting vulnerabilities</h4>
<p><strong class="side-heading">What it is in general:</strong> The bash execution parser processes command lines through a deterministic multi-stage sequence: brace expansion, tilde expansion, parameter/variable expansion, command substitution, arithmetic expansion, <strong class="keyword">word splitting</strong>, and pathname expansion (globbing). Crucially, unquoted variables (e.g. <code>$filename</code>) are subjected to word splitting based on the Internal Field Separator (<code>IFS</code>, default space, tab, newline). If a variable contains spaces or glob characters, unquoted expansion splits a single semantic argument into multiple distinct tokens, causing catastrophic command line misinterpretation. Wrapping variables in double quotes (<code>"$var"</code>) preserves whitespace and treats the expansion as a single atomic token.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Failure to quote variables is the single most common vulnerability in infrastructure automation scripts, causing accidental deletion of root directories (e.g. <kbd>rm -rf "$TARGET_DIR/"</kbd> expanding to <kbd>rm -rf /</kbd> when unquoted and unset) and shell injection vulnerabilities in cloud CI/CD runners.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud Deploy, Cloud Build, and Cloud Shell automations, build scripts handle dynamic branch names, commit messages, and artifact tags containing special characters. Strict quoting ensures automated cloud pipelines do not fail or trigger argument injection attacks. Primary documentation: <a href="https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION">bash(1) PARAMETER EXPANSION and Word Splitting (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION">bash(1) QUOTING mechanisms and escape sequences (accessed 2026-10-04)</a>.</p>

<h4>Control structures: loops (for, while), conditionals ([[ ... ]]), and pattern matching</h4>
<p><strong class="side-heading">What it is in general:</strong> Bash provides robust control flow mechanisms: conditional branching evaluates status expressions using the modern compound test command <strong class="keyword">[[ expression ]]</strong>, which prevents word splitting, handles empty strings safely, and supports extended regular expression matching via the <code>=~</code> operator (unlike legacy POSIX <code>[ expression ]</code>). Iterative loops process collections: <kbd>for item in "${array[@]}"</kbd> safely iterates over array elements preserving spaces, while <kbd>while IFS= read -r line</kbd> processes line-oriented streaming input from files or pipes without trimming whitespace or interpreting backslashes.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Infrastructure scripts parse complex outputs from cloud CLI tools (e.g. list of VM instances, storage buckets, or firewall rules). Robust loops and regex conditionals prevent scripts from stalling or silently executing against malformed records.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Shell scripts automating Google Cloud tasks parse JSON output from <kbd>gcloud</kbd> commands. Utilizing modern bash conditionals and array loops allows architects to construct resilient operational runbooks. Primary documentation: <a href="https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION">bash(1) Compound Commands and Conditional Constructs (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION">bash(1) Pattern Matching and Regular Expressions (accessed 2026-10-04)</a>.</p>

<h4>Process execution, pipelines (set -o pipefail), and exit status evaluation ($?)</h4>
<p><strong class="side-heading">What it is in general:</strong> In Linux, every process termination reports an integer <strong class="keyword">exit status</strong> between 0 and 255: exit code 0 signifies success, while any non-zero value indicates an error. In a standard shell pipeline (<kbd>cmd1 | cmd2 | cmd3</kbd>), bash executes each command concurrently in separate subshells and reports only the exit status of the <em>last</em> command in the pipeline (<code>cmd3</code>). If an upstream command fails (e.g. <code>cmd1</code> crashes with error), the failure is completely masked if <code>cmd3</code> succeeds. Enabling <kbd>set -o pipefail</kbd> forces the pipeline to return the exit code of the rightmost command that exited with a non-zero status.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Masked pipeline failures in CI/CD build scripts lead to false-positive deployment approvals: an image compilation or security scan pipeline like <kbd>security-scan app | grep -v WARNING</kbd> reports exit code 0 even if the scanner fails catastrophically, deploying uninspected vulnerabilities into production.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Cloud Build pipeline steps execute containerized shell commands where exit code 0 signals stage completion. Configuring <kbd>set -o pipefail</kbd> in all Cloud Build step scripts ensures that failed data extractions or failed <kbd>gcloud</kbd> commands halt the pipeline immediately. Primary documentation: <a href="https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION">bash(1) Pipelines and Exit Status ($?) (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION">bash(1) PIPESTATUS array and process substitution (accessed 2026-10-04)</a>.</p>

<h4>Defensive scripting standards: set -euo pipefail, trap handlers, and secure parsing of structured payloads (JSON)</h4>
<p><strong class="side-heading">What it is in general:</strong> Production-grade bash scripts adhere to <strong class="keyword">Defensive Scripting Standards</strong> by declaring <kbd>set -euo pipefail</kbd> at the header:
<ul>
<li><code>-e</code> (errexit): abort immediately if any command returns a non-zero exit status.</li>
<li><code>-u</code> (nounset): abort if an unset variable is referenced, catching typos and missing parameters.</li>
<li><code>-o pipefail</code>: propagate pipeline failure codes.</li>
</ul>
Furthermore, scripts register <strong class="keyword">trap</strong> handlers (<kbd>trap cleanup EXIT ERR</kbd>) to ensure temporary files, lock files, and background child processes are deterministically cleaned up on normal termination or abnormal crash. Finally, scripts must never use unsafe string manipulation or regex parsing for structured payloads like JSON: they must delegate parsing to dedicated, hardened utilities like <code>jq</code> or Python's <code>json</code> module, validating schema compliance and failing explicitly on missing or malformed fields.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Defensive scripting prevents automated infrastructure scripts from continuing in partially applied, corrupt states. Strict schema validation of JSON configurations ensures invalid parameters are rejected before modifying cloud resources.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Enterprise GCP infrastructure-as-code deployment wrappers, Terraform automation wrappers, and Cloud Run container startup scripts employ strict defensive bash headers to ensure idempotent, fail-fast operations. Primary documentation: <a href="https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION">bash(1) SHELL BUILTIN COMMANDS (set, trap) (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man1/bash.1.html#DESCRIPTION">bash(1) Signals and TRAPS (accessed 2026-10-04)</a>.</p>

<table><caption>Shell expansion order and defensive controls</caption>
<thead><tr><th>Phase</th><th>Mechanism</th><th>Common Defect</th><th>Defensive Control</th></tr></thead>
<tbody>
<tr><td>Parameter Expansion</td><td>$VAR and ${VAR:-default}</td><td>Unset variable treated as empty string</td><td>Enable set -u (nounset).</td></tr>
<tr><td>Word Splitting</td><td>IFS character tokenization</td><td>Paths with spaces split into multiple args</td><td>Wrap all variable expansions in double quotes: "$VAR".</td></tr>
<tr><td>Pipeline Status</td><td>cmd1 | cmd2</td><td>Upstream failure masked by downstream command</td><td>Enable set -o pipefail.</td></tr>
<tr><td>Payload Parsing</td><td>JSON / YAML text processing</td><td>Fragile regex parsing breaks on schema changes</td><td>Delegate to jq or python3 json validator.</td></tr>
</tbody></table>

{FIG_7_3_HTML}

<p><strong class="side-heading">Concrete example:</strong> An administrative automation script parses synthetic JSON service configurations:
<pre><code>#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="$1"
# Parse JSON safely using python3 json parser; validate required fields
PORT=$(python3 -c "import json, sys; d=json.load(open(sys.argv[1])); assert 'port' in d; print(d['port'])" "$CONFIG_FILE")
echo "Valid configuration: Service port is $PORT"</code></pre>
If an invalid JSON file lacking the <code>port</code> key or containing broken syntax is passed, the Python helper raises an assertion error or JSONDecodeError, exits with status 1, and the shell's <code>-e</code> flag halts execution immediately before any downstream deployment action is executed.</p>
<p><strong class="side-heading">Evidence limit:</strong> A script passing preflight validation and exiting with status 0 proves that input syntax complied with the parser's schema and required fields were present; it does not prove that network ports are open on the firewall or that downstream external APIs are operational.</p>'''

print("Topic 3 tech defined.")
