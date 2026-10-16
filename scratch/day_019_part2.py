"""Day 19 Topic 2 technical content module."""

from scratch.generate_day_019 import FIG_19_2_HTML

TOPIC_02_TECH = '''
<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Local gcloud installation architecture and SDK directory structure</strong></li>
<li><strong>Core credential bootstrapping with gcloud init and gcloud auth</strong></li>
<li><strong>Named CLI configurations (gcloud config configurations) for multi-tenant isolation</strong></li>
<li><strong>Active configuration properties (project, account, compute/region, compute/zone)</strong></li>
<li><strong>Configuration precedence hierarchy (CLI flags > environment variables > active configuration > default properties)</strong></li>
</ul>

<h3>Local gcloud installation architecture and SDK directory structure</h3>
<p><strong class="side-heading">What it is in general:</strong> A <strong class="keyword">cloud SDK local installation</strong> bundles core executable binaries, modular component managers, client libraries, and local state directories into a standardized filesystem layout on the operator's workstation.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects must establish standardized workstation baseline standards. Understanding where the SDK stores binaries (e.g. <code>/usr/local/google-cloud-sdk/bin</code> or OS package manager paths) versus where user-specific credential tokens and named configuration files reside (<code>~/.config/gcloud</code> on POSIX systems or <code>%APPDATA%\\gcloud</code> on Windows) ensures that workstation backup and disk sanitization procedures do not unintentionally expose or destroy administrative credentials.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud CLI stores configuration state in the user configuration directory under <code>~/.config/gcloud/configurations/</code>. Each named configuration is stored as a plain INI-formatted text file (e.g. <code>config_default</code>, <code>config_sandbox</code>, <code>config_prod</code>). The active configuration pointer is tracked in <code>~/.config/gcloud/active_config</code>. Cached OAuth 2.0 refresh tokens, SQLite database caches, and component installation manifests reside in <code>~/.config/gcloud/credentials.db</code> and related subdirectories.</p>

<h3>Core credential bootstrapping with gcloud init and gcloud auth</h3>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Credential bootstrapping</strong> executes an interactive or automated OAuth 2.0 authorization code flow, exchanging operator credentials for revocable access tokens and linking the identity to a default cloud workspace.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects must distinguish between user authentication (<kbd>gcloud auth login</kbd>) and service account authentication (<kbd>gcloud auth activate-service-account</kbd>). For human engineers, interactive browser-based OAuth flows ensure multifactor authentication (MFA) and Identity and Access Management (IAM) conditional access policies are enforced; for unattended automation, short-lived OIDC workload identity federation or encrypted service account key files are required.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Executing <kbd>gcloud init</kbd> performs an end-to-end bootstrap: it launches a browser for Google account login, authorizes the Google Cloud SDK application, lists available projects associated with the account, sets the default project, and prompts for default Compute Engine region and zone preferences. For programmatic scripting without opening a browser, engineers use <kbd>gcloud auth login --no-launch-browser</kbd> or authorize Application Default Credentials (ADC) via <kbd>gcloud auth application-default login</kbd>, which generates <code>~/.config/gcloud/application_default_credentials.json</code> used by client libraries.</p>

<h3>Named CLI configurations (gcloud config configurations) for multi-tenant isolation</h3>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Named CLI configurations</strong> are discrete, isolated property profiles that encapsulate credentials, project identifiers, default regions, and endpoint configurations, allowing operators to switch working contexts atomically without re-authenticating.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Operating across enterprise environments (e.g. development sandboxes, staging clusters, production systems) demands strict context isolation. Without named configurations, an engineer troubleshooting production who switches their default project must manually remember to switch it back, creating high probability of human error. Named configurations allow architects to establish clean operational boundaries: activating a configuration activates all associated project, account, and regional properties simultaneously.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> As documented in <a href="https://cloud.google.com/sdk/docs/configurations#multiple_configurations">Google Cloud SDK Documentation: Multiple configurations (accessed 2026-10-04)</a>, Google Cloud CLI provides first-class configuration management:
<kbd>gcloud config configurations create [NAME]</kbd> creates a new profile;
<kbd>gcloud config configurations activate [NAME]</kbd> switches the active context;
<kbd>gcloud config configurations list</kbd> displays all configured profiles along with their active status and property values.
Architects enforce establishing distinct configurations (e.g. <code>brightloaf-sandbox</code> and <code>brightloaf-prod</code>) so that credentials, projects, and regions never cross-pollinate.</p>

<h3>Active configuration properties (project, account, compute/region, compute/zone)</h3>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Active configuration properties</strong> define key-value parameters that configure default behavior, target API namespaces, and geographical placement for CLI commands that do not explicitly pass inline parameter flags.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects must establish organizational standards for property definitions. Specifying default regions (e.g. <code>compute/region = us-central1</code>) prevents engineers from accidentally provisioning compute instances in expensive or unapproved geographical regions. However, architects must mandate that critical operational scripts never rely on ambient property defaults, but explicitly declare parameters to ensure deterministic execution.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Properties are partitioned into sections: <code>core/project</code> specifies the active Google Cloud project ID; <code>core/account</code> specifies the authenticated user or service account identity; <code>compute/region</code> and <code>compute/zone</code> designate default Compute Engine geography. Operators query and modify properties via <kbd>gcloud config set &lt;section&gt;/&lt;property&gt; &lt;value&gt;</kbd>, <kbd>gcloud config get-value &lt;property&gt;</kbd>, and <kbd>gcloud config list</kbd>. Properties set in a named configuration apply only while that configuration is active.</p>

<h3>Configuration precedence hierarchy (CLI flags > environment variables > active configuration > default properties)</h3>
<p><strong class="side-heading">What it is in general:</strong> A <strong class="keyword">configuration precedence hierarchy</strong> evaluates potential parameter sources in a strictly defined order, resolving the final parameter value used to execute the underlying API call.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Understanding the precedence hierarchy is vital for debugging operational failures and designing fail-safe automation. If an engineer sets an ambient environment variable in their workstation shell, that environment variable overrides the active named configuration without warning. If the engineer then switches configurations expecting to target a sandbox, the CLI will continue sending requests to the environment variable's target project.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> The Google Cloud CLI evaluates parameter values using four strict tiers of precedence, ordered from highest to lowest:
<ol>
  <li><strong>Tier 1: Explicit Command-Line Parameter Flags:</strong> Arguments passed directly to the command (e.g. <code>--project=brightloaf-sandbox-19</code>, <code>--region=us-central1</code>) take absolute precedence over all other settings.</li>
  <li><strong>Tier 2: Environment Variables:</strong> Specific environment variables (e.g. <code>CLOUDSDK_CORE_PROJECT</code>, <code>CLOUDSDK_COMPUTE_REGION</code>) override any values defined in configuration files.</li>
  <li><strong>Tier 3: Active Named Configuration Properties:</strong> Properties defined in the currently activated configuration file in <code>~/.config/gcloud/configurations/config_&lt;name&gt;</code>.</li>
  <li><strong>Tier 4: Default Property Fallbacks:</strong> Hardcoded SDK defaults or unset property values that prompt interactive confirmation if required.</li>
</ol></p>

<p><strong class="side-heading">Comparative Analysis: Named Configurations vs Environment Variables vs Command-Line Parameter Flags</strong></p>
<table class="comparison-table">
  <thead>
    <tr>
      <th>Operational Metric</th>
      <th>Named Configurations</th>
      <th>Environment Variables</th>
      <th>Command-Line Parameter Flags</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Precedence Rank</strong></td>
      <td>Tier 3 (Lowest of explicit choices)</td>
      <td>Tier 2 (Intermediate precedence)</td>
      <td>Tier 1 (Highest / Absolute precedence)</td>
    </tr>
    <tr>
      <td><strong>Scope & Durability</strong></td>
      <td>Persistent across terminal restarts (stored on disk)</td>
      <td>Process / session-scoped (volatile unless in .bashrc)</td>
      <td>Single command execution invocation only</td>
    </tr>
    <tr>
      <td><strong>Multi-Property Bundling</strong></td>
      <td>Bundles account, project, region, zone atomically</td>
      <td>Requires setting individual variables manually</td>
      <td>Requires explicit flags per command invocation</td>
    </tr>
    <tr>
      <td><strong>Primary Use Case</strong></td>
      <td>Interactive daily workstation environment switching</td>
      <td>CI/CD build pipelines and container runtime injection</td>
      <td>Operational runbooks, automated scripts, audit scripts</td>
    </tr>
    <tr>
      <td><strong>Risk Profile</strong></td>
      <td>Low: explicit activation via gcloud config</td>
      <td>High: silent ambient masking across subshells</td>
      <td>Zero: completely deterministic and self-documenting</td>
    </tr>
  </tbody>
</table>

<div class="technical-figure">
''' + FIG_19_2_HTML + '''
</div>

<p><strong class="side-heading">Concrete example:</strong> Creating named configurations for sandbox and production environments, inspecting property precedence, and observing environment variable overrides:</p>
<pre><code># 1. Create and configure sandbox named profile
$ gcloud config configurations create brightloaf-sandbox
Created [brightloaf-sandbox].
Activated [brightloaf-sandbox].

$ gcloud config set core/project brightloaf-sandbox-19
$ gcloud config set core/account naveen@brightloaf.com
$ gcloud config set compute/region us-central1
$ gcloud config set compute/zone us-central1-a

# 2. Create and configure production named profile
$ gcloud config configurations create brightloaf-prod
Created [brightloaf-prod].
Activated [brightloaf-prod].

$ gcloud config set core/project brightloaf-prod-us
$ gcloud config set core/account naveen@brightloaf.com
$ gcloud config set compute/region us-east4
$ gcloud config set compute/zone us-east4-a

# 3. List all configurations and observe active indicator
$ gcloud config configurations list
NAME                IS_ACTIVE  ACCOUNT                PROJECT                COMPUTE_DEFAULT_ZONE  COMPUTE_DEFAULT_REGION
brightloaf-prod     True       naveen@brightloaf.com  brightloaf-prod-us     us-east4-a            us-east4
brightloaf-sandbox  False      naveen@brightloaf.com  brightloaf-sandbox-19  us-central1-a         us-central1

# 4. Demonstrate Precedence: Switch to sandbox, but observe environment variable override!
$ gcloud config configurations activate brightloaf-sandbox
Activated [brightloaf-sandbox].

$ gcloud config get-value project
brightloaf-sandbox-19  # Expected sandbox project

# Inject Tier 2 environment variable
$ export CLOUDSDK_CORE_PROJECT=brightloaf-prod-us
$ gcloud config get-value project
brightloaf-prod-us  # OVERRIDDEN by CLOUDSDK_CORE_PROJECT!

# Inject Tier 1 parameter flag: overrides BOTH environment variable and configuration
$ gcloud config get-value project --project=brightloaf-qa-testing
brightloaf-qa-testing  # Resolved Tier 1 explicit flag!

# Clean up volatile environment variable
$ unset CLOUDSDK_CORE_PROJECT</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> Environment variables (such as <code>CLOUDSDK_CORE_PROJECT</code>) completely supersede active named configuration settings without warning or terminal notification. If an engineer forgets an exported variable in their active shell session, all subsequent commands will execute against the environment variable target regardless of what <kbd>gcloud config configurations activate</kbd> reports.</p>
'''
