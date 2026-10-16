"""Day 19 Topic 1 technical content module."""

from scratch.generate_day_019 import FIG_19_1_HTML

TOPIC_01_TECH = '''
<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li><strong>Virtual architecture and lifecycle of Cloud Shell containers</strong></li>
<li><strong>Persistent 5 GB home directory storage and filesystem boundaries</strong></li>
<li><strong>Preinstalled developer toolchains and environment bootstrap</strong></li>
<li><strong>Cloud Shell authorization tokens and ambient credential injection</strong></li>
<li><strong>Cloud Shell Web Preview, ports, and ephemeral session recovery</strong></li>
</ul>

<h3>Virtual architecture and lifecycle of Cloud Shell containers</h3>
<p><strong class="side-heading">What it is in general:</strong> An <strong class="keyword">ephemeral containerized execution environment</strong> provisions a lightweight Linux container dynamically upon user login, attaches pre-allocated network and compute resources, and terminates the container after an idle timeout to optimize cloud multi-tenant density.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects must recognize that ephemeral virtual environments are designed exclusively for interactive administration, rapid prototyping, and transient debugging. They are not enterprise runtime environments, cannot host production microservices, and lack high-availability SLA guarantees. Workloads requiring continuous uptime or guaranteed compute reservations must be hosted on dedicated Compute Engine virtual machines or Google Kubernetes Engine clusters.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Google Cloud, Cloud Shell runs on a custom Debian-based container hosted on an e2-small Compute Engine virtual machine instance. Sessions have an inactivity timeout of 20 minutes: if no keystrokes or terminal input are registered for 20 continuous minutes, Google Cloud automatically tears down the container and detaches the persistent disk. Additionally, Google Cloud enforces a strict weekly usage quota of 120 hours per user; once reached, access is suspended until the weekly quota counter resets on Monday at 00:00 UTC.</p>

<h3>Persistent 5 GB home directory storage and filesystem boundaries</h3>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Filesystem boundary decoupling</strong> separates the volatile operating system root filesystem (which is wiped upon container termination) from a dedicated persistent block storage volume mounted at a specific mount point (such as <code>$HOME</code> or <code>/home/username</code>) across session recycles.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Architects must educate engineering teams regarding storage boundaries. Custom scripts, configuration files, SSH keys, and Git repositories must reside strictly within <code>$HOME</code>. Modifying system packages in <code>/usr/bin</code>, <code>/etc</code>, or writing temporary data to <code>/tmp</code> will not survive session restarts. Furthermore, persistent storage policies require periodic activity to prevent automated garbage collection.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Google Cloud provisions exactly 5 GB of Persistent Disk storage mounted as the user's home directory (<code>$HOME</code>) in Cloud Shell. As documented in <a href="https://cloud.google.com/shell/docs/how-cloud-shell-works#persistent_disk_storage">Google Cloud Shell Documentation: Persistent disk storage (accessed 2026-10-04)</a>, this 5 GB persistent disk is preserved between sessions; however, if a user does not access Cloud Shell for 120 consecutive calendar days, the persistent disk storage is flagged for deletion and all files in <code>$HOME</code> are permanently purged. Google Cloud sends email notifications prior to disk purging.</p>

<h3>Preinstalled developer toolchains and environment bootstrap</h3>
<p><strong class="side-heading">What it is in general:</strong> A <strong class="keyword">pre-packaged developer toolchain</strong> equips a container image with pre-compiled language runtimes, package managers, container runtimes, and cloud management CLIs, allowing engineers to begin administrative work immediately without manual installation overhead.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Preinstalled toolchains standardize administrative operations across distributed engineering teams, eliminating workstation configuration drift and OS incompatibility issues. However, architects must establish environment customization runbooks (using dotfiles such as <code>.bashrc</code> or custom environment startup scripts) that execute inside <code>$HOME</code> upon container initialization, ensuring that bespoke tools or CLI aliases are re-initialized automatically.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Cloud Shell comes pre-loaded with the Google Cloud SDK (<kbd>gcloud</kbd>, <kbd>gsutil</kbd>, <kbd>bq</kbd>), <kbd>kubectl</kbd>, <kbd>docker</kbd>, <kbd>terraform</kbd>, <kbd>git</kbd>, and major language runtimes including Python 3, Java, Go, Node.js, and .NET. To customize the environment permanently across container recycles, users configure the <code>$HOME/.customize_environment</code> script. When Cloud Shell initializes a fresh container image, it automatically detects and executes <code>$HOME/.customize_environment</code> with root privileges, allowing automated installation of custom APT packages or CLI utilities onto the fresh container filesystem.</p>

<h3>Cloud Shell authorization tokens and ambient credential injection</h3>
<p><strong class="side-heading">What it is in general:</strong> <strong class="keyword">Ambient credential injection</strong> automatically provisions short-lived OAuth 2.0 access tokens into the shell runtime based on the authenticated console user identity, eliminating the need to store long-lived service account keys or static credentials on disk.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Cloud architects favor ambient credential injection because it enforces strict identity propagation and adheres to zero-trust principles. Because Cloud Shell inherits the Google account credentials of the operator logged into the Google Cloud Console, all API requests initiated from Cloud Shell are audited in Cloud Audit Logs with the exact principal email, IP address, and caller identity.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> In Cloud Shell, the <kbd>gcloud</kbd> CLI is pre-authenticated with the active Google user account. The ambient environment variable <code>GOOGLE_APPLICATION_CREDENTIALS</code> is not statically configured with a service account JSON file; instead, the Google Cloud CLI uses an internal metadata-like credential helper proxy. When a command executes, Cloud Shell prompts for user authorization via an OAuth consent dialog if an API call requests delegated permissions. Furthermore, Cloud Shell automatically sets the ambient project context to the project selected in the Google Cloud Console header bar.</p>

<h3>Cloud Shell Web Preview, ports, and ephemeral session recovery</h3>
<p><strong class="side-heading">What it is in general:</strong> A <strong class="keyword">web preview proxy mechanism</strong> maps local TCP listening ports on an isolated development container to a secure HTTPS external proxy URL, enabling browser-based visual verification of web servers, API endpoints, or administrative dashboards without exposing public IP addresses.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Web preview proxies allow developers to perform rapid verification of containerized microservices and web user interfaces within secure development boundaries. Architects must ensure engineers understand that preview proxies are private to the authenticated session and cannot be shared publicly with unauthenticated third parties or used as production API gateways.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Cloud Shell features the Web Preview button in its top terminal bar, allowing developers to inspect web applications listening on ports 8080, 8081–8084, or any arbitrary custom port. Google Cloud proxies these requests through <code>https://&lt;port&gt;-dot-&lt;session-id&gt;.googleusercontent.com</code>, authenticating incoming requests against the operator's Google account session cookie. If a session disconnects, reconnecting within the 20-minute window attaches to the active container; beyond 20 minutes, the container terminates and the preview proxy endpoint is destroyed.</p>

<p><strong class="side-heading">Comparative Analysis: Cloud Shell vs Local Workstation CLI vs Compute Engine Bastion Host</strong></p>
<table class="comparison-table">
  <thead>
    <tr>
      <th>Operational Dimension</th>
      <th>Google Cloud Shell</th>
      <th>Local Workstation CLI</th>
      <th>Compute Engine Bastion Host</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Infrastructure Hosting</strong></td>
      <td>Ephemeral Google-managed container (e2-small)</td>
      <td>Developer laptop / local workstation hardware</td>
      <td>Dedicated Compute Engine VM within VPC</td>
    </tr>
    <tr>
      <td><strong>Persistence Boundary</strong></td>
      <td>5 GB persistent disk mounted at $HOME only</td>
      <td>Full local disk persistence (100% durable)</td>
      <td>Persistent Disk (boot disk + attached disks)</td>
    </tr>
    <tr>
      <td><strong>Session Lifetime & Quota</strong></td>
      <td>20-minute idle timeout; 120-hour weekly quota</td>
      <td>Unlimited (governed by developer hardware)</td>
      <td>Continuous 24/7 runtime (billed hourly)</td>
    </tr>
    <tr>
      <td><strong>Credential Management</strong></td>
      <td>Ambient OAuth 2.0 console token injection</td>
      <td><kbd>gcloud auth login</kbd> (stored in ~/.config/gcloud)</td>
      <td>Attached Compute Engine Service Account</td>
    </tr>
    <tr>
      <td><strong>Network Ingress / Access</strong></td>
      <td>Browser-only via HTTPS Google Cloud Console</td>
      <td>Local shell (Terminal, PowerShell, iTerm2)</td>
      <td>SSH via Cloud IAP or VPN tunnel</td>
    </tr>
  </tbody>
</table>

<div class="technical-figure">
''' + FIG_19_1_HTML + '''
</div>

<p><strong class="side-heading">Concrete example:</strong> Inspecting Cloud Shell storage boundaries, environment variables, and pre-authenticated credentials in a live terminal session:</p>
<pre><code># 1. Inspect filesystem mount points: verify $HOME vs ephemeral container root
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
overlay          40G   22G   18G  56% /
/dev/sdb        4.8G  240M  4.4G   6% /home/naveen

# 2. Audit ambient gcloud configuration and active authenticated account
$ gcloud auth list
   Credentialed Accounts
ACTIVE  ACCOUNT
*       naveen@brightloaf.com

# 3. Verify ambient project context set by Google Cloud Console picker
$ gcloud config get-value project
brightloaf-sandbox-19

# 4. Verify pre-installed developer toolchain versions
$ gcloud version --format="value(core)"
496.0.0
$ kubectl version --client --output=yaml | grep gitVersion
  gitVersion: v1.30.2
$ terraform version | head -n 1
Terraform v1.9.5</code></pre>

<p><strong class="side-heading">Evidence limit:</strong> Cloud Shell persistent disk storage is strictly bounded to 5 GB. If storage consumption exceeds 5 GB, commands writing to disk fail with <code>No space left on device</code>. Unmounted persistent disks are permanently deleted after 120 days of inactivity, and running containers terminate after exactly 20 minutes of user inactivity regardless of running background processes.</p>
'''
