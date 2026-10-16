"""Day 19 SVGs wrapped in figure containers with non-empty figcaptions."""

FIG_19_1_HTML = '''<figure class="diagram-container">
<svg role="img" aria-labelledby="fig19-1-title fig19-1-desc" viewBox="0 0 960 520" width="960" height="520" xmlns="http://www.w3.org/2000/svg">
      <title id="fig19-1-title">Cloud Shell Virtual Architecture, Storage Boundaries, and Web Preview Lifecycle</title>
      <desc id="fig19-1-desc">Architectural diagram contrasting the ephemeral Debian Compute Engine VM runtime with the persistent 5 GB home directory disk, web preview proxying, and session expiration boundaries.</desc>
      <defs>
        <linearGradient id="p19-f1-bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#090d16"/>
          <stop offset="100%" stop-color="#121526"/>
        </linearGradient>
        <linearGradient id="p19-f1-panel" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#1e293b" stop-opacity="0.8"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0.9"/>
        </linearGradient>
        <marker id="p19-f1-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/>
        </marker>
        <marker id="p19-f1-arrow-warn" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#f59e0b"/>
        </marker>
        <marker id="p19-f1-arrow-err" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"/>
        </marker>
        <marker id="p19-f1-arrow-ok" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"/>
        </marker>
      </defs>

      <!-- Background -->
      <rect width="960" height="520" rx="12" fill="url(#p19-f1-bg)" stroke="#1e293b" stroke-width="1"/>

      <!-- Title Header -->
      <text x="480" y="32" fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle">Figure 19.1: Cloud Shell Virtual Architecture &amp; Persistence Boundary</text>
      <text x="480" y="50" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle">Debian VM Runtime Lifecycle · 5 GB Persistent Home Mount · Web Preview Proxy · 20-Minute Idle Purge</text>

      <!-- Client Layer (Top Left) -->
      <rect x="30" y="75" width="250" height="140" rx="8" fill="url(#p19-f1-panel)" stroke="#38bdf8" stroke-width="1.5"/>
      <rect x="30" y="75" width="250" height="28" rx="8" fill="#38bdf8" fill-opacity="0.15"/>
      <text x="42" y="94" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Client Layer (Browser)</text>
      <text x="42" y="122" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• Cloud Console Terminal UI (xterm.js)</text>
      <text x="42" y="142" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• Google Identity Auth Cookie (OAuth 2.0)</text>
      <text x="42" y="162" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• Web Preview Client (Port 8080 / custom)</text>
      <text x="42" y="182" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• Boost Mode Request (2x vCPU/RAM, 24h)</text>

      <!-- Google-Managed Control Plane (Top Center-Right) -->
      <rect x="330" y="75" width="600" height="140" rx="8" fill="url(#p19-f1-panel)" stroke="#6366f1" stroke-width="1.5"/>
      <rect x="330" y="75" width="600" height="28" rx="8" fill="#6366f1" fill-opacity="0.15"/>
      <text x="342" y="94" fill="#818cf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Google Cloud Shell Control Plane (Tenant Infrastructure)</text>
      
      <!-- Sub-blocks inside Control Plane -->
      <rect x="345" y="115" width="170" height="85" rx="6" fill="#090d16" stroke="#475569" stroke-width="1"/>
      <text x="355" y="135" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">SSH Gateway</text>
      <text x="355" y="155" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">• Mutual TLS Terminal Tunnel</text>
      <text x="355" y="172" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">• User Credential Injector</text>
      <text x="355" y="189" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">• Auto-reconnect Manager</text>

      <rect x="530" y="115" width="185" height="85" rx="6" fill="#090d16" stroke="#475569" stroke-width="1"/>
      <text x="540" y="135" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Web Preview Proxy</text>
      <text x="540" y="155" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">• Port 8080 &amp; 1024-65535 Tunnel</text>
      <text x="540" y="172" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">• Auth Verification Filter</text>
      <text x="540" y="189" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">• URL: *.cloudshell.dev</text>

      <rect x="730" y="115" width="185" height="85" rx="6" fill="#090d16" stroke="#f59e0b" stroke-width="1"/>
      <text x="740" y="135" fill="#fbbf24" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Session Watchdog</text>
      <text x="740" y="155" fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10">• 20-min Inactivity Timer</text>
      <text x="740" y="172" fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10">• 12-hour Absolute Max Cap</text>
      <text x="740" y="189" fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10">• 50-hr Weekly Rolling Limit</text>

      <!-- Connectors Client to Control Plane -->
      <path d="M 280 135 L 343 135" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#p19-f1-arrow)"/>
      <path d="M 280 165 L 528 165" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#p19-f1-arrow)"/>

      <!-- Lower Section: Ephemeral VM Container Environment -->
      <rect x="30" y="240" width="900" height="250" rx="10" fill="#0b1120" stroke="#334155" stroke-width="1.5"/>
      <text x="45" y="262" fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="14" font-weight="bold">Cloud Shell Execution Runtime (Debian Compute Engine VM Instance)</text>
      <text x="600" y="262" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">Default: e2-medium (1 vCPU, 4GB RAM) · Boost: 2 vCPU, 8GB RAM</text>

      <!-- Box 1: Ephemeral Filesystem (Left) -->
      <rect x="50" y="280" width="400" height="190" rx="8" fill="#1e1418" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="6 4"/>
      <rect x="50" y="280" width="400" height="28" rx="8" fill="#ef4444" fill-opacity="0.15"/>
      <text x="62" y="299" fill="#f87171" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Root &amp; System Filesystem (/) — EPHEMERAL</text>
      <text x="62" y="328" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• /tmp (temporary compiler artifacts &amp; sockets)</text>
      <text x="62" y="348" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• /usr/local/bin (manually installed apt/pip packages)</text>
      <text x="62" y="368" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• /etc/environment &amp; system-wide daemon configs</text>
      <text x="62" y="388" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• Docker daemon storage (/var/lib/docker images)</text>
      <rect x="62" y="410" width="376" height="45" rx="4" fill="#450a0a" stroke="#b91c1c" stroke-width="1"/>
      <text x="72" y="428" fill="#fca5a5" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">[LIFECYCLE BOUNDARY: DISCARDED ON IDLE TIMEOUT]</text>
      <text x="72" y="444" fill="#fecaca" font-family="system-ui, sans-serif" font-size="10">All changes outside /home/naveen vanish when VM is recycled.</text>

      <!-- Box 2: Persistent Volume (Right) -->
      <rect x="510" y="280" width="400" height="190" rx="8" fill="#09261a" stroke="#22c55e" stroke-width="1.5"/>
      <rect x="510" y="280" width="400" height="28" rx="8" fill="#22c55e" fill-opacity="0.15"/>
      <text x="522" y="299" fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Persistent Storage (/home/naveen) — 5 GB DISK</text>
      <text x="522" y="328" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• User dotfiles (.bashrc, .profile, .gitconfig)</text>
      <text x="522" y="348" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• Local source repositories &amp; workspace code</text>
      <text x="522" y="368" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• Custom bootstrap: /home/naveen/.customize_environment</text>
      <text x="522" y="388" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">• Local gcloud active state (~/.config/gcloud)</text>
      <rect x="522" y="410" width="376" height="45" rx="4" fill="#052e16" stroke="#15803d" stroke-width="1"/>
      <text x="532" y="428" fill="#86efac" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">[STORAGE INVARIANT: SURVIVES VM REBOOTS]</text>
      <text x="532" y="444" fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="10">Remounts automatically. Scheduled for purge after 120 days idle.</text>

      <!-- Link from Control Plane to VM -->
      <path d="M 430 200 L 430 238" fill="none" stroke="#818cf8" stroke-width="2" marker-end="url(#p19-f1-arrow)"/>
      <path d="M 822 200 L 822 232 L 250 232 L 250 278" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#p19-f1-arrow-err)"/>
    </svg>
<figcaption><strong>Figure 19.1: Cloud Shell Virtual Architecture, Storage Boundaries, and Web Preview Lifecycle.</strong>
    Illustrates the separation between the ephemeral Debian Compute Engine container runtime and the persistent 5&nbsp;GB user disk mounted at <code>/home/naveen</code>.
    <br><strong>Supplied facts:</strong> Ephemeral root filesystems are destroyed upon 20-minute idle disconnects or 12-hour session limits; persistent storage retains user dotfiles and repository checkouts across VM reboots.
    <br><strong>Architectural inference:</strong> Any tooling or dependencies compiled directly into <code>/tmp</code> or <code>/usr/local</code> will be lost upon reconnection unless codified into <code>/home/naveen/.customize_environment</code> or user-level persistent paths.
    <br><strong>Expected post-fix behavior:</strong> Development environments maintain repeatable setup scripts within <code>/home/naveen</code>, ensuring zero MTTR penalties during emergency operational sessions.</figcaption>
</figure>'''

FIG_19_2_HTML = '''<figure class="diagram-container">
<svg role="img" aria-labelledby="fig19-2-title fig19-2-desc" viewBox="0 0 960 540" width="960" height="540" xmlns="http://www.w3.org/2000/svg">
      <title id="fig19-2-title">gcloud Context Precedence Engine and Named Profile Resolution Hierarchy</title>
      <desc id="fig19-2-desc">Detailed sequence diagram illustrating the four-tier resolution ladder of the Google Cloud CLI, showing how command-line flags, environment variables, named configurations, and defaults dictate the effective project and identity.</desc>
      <defs>
        <linearGradient id="p19-f2-bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#090d16"/>
          <stop offset="100%" stop-color="#121526"/>
        </linearGradient>
        <linearGradient id="p19-f2-tier" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#1e293b"/>
          <stop offset="100%" stop-color="#0f172a"/>
        </linearGradient>
        <marker id="p19-f2-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/>
        </marker>
        <marker id="p19-f2-arrow-warn" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#f59e0b"/>
        </marker>
        <marker id="p19-f2-arrow-ok" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"/>
        </marker>
      </defs>

      <rect width="960" height="540" rx="12" fill="url(#p19-f2-bg)" stroke="#1e293b" stroke-width="1"/>

      <!-- Title Header -->
      <text x="480" y="32" fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle">Figure 19.2: gcloud Context Precedence Engine &amp; Resolution Hierarchy</text>
      <text x="480" y="50" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle">Four-Tier Evaluation Order · Silent Environment Variable Overrides · Effective Target Verification</text>

      <!-- Invocations on Left -->
      <rect x="30" y="80" width="230" height="100" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="42" y="104" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">CLI Command Invocations</text>
      <text x="42" y="128" fill="#cbd5e1" font-family="monospace" font-size="11">gcloud compute instances list</text>
      <text x="42" y="146" fill="#94a3b8" font-family="monospace" font-size="10">--project=brightloaf-prod</text>
      <text x="42" y="164" fill="#64748b" font-family="system-ui, sans-serif" font-size="10">Initiated by operator or script</text>

      <!-- Four Tier Ladder in Center -->
      <g transform="translate(300, 75)">
        <!-- Tier 1 -->
        <rect x="0" y="0" width="380" height="75" rx="6" fill="url(#p19-f2-tier)" stroke="#22c55e" stroke-width="1.5"/>
        <text x="15" y="22" fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Tier 1: Explicit Command Flags (Priority 1 — Highest)</text>
        <text x="15" y="42" fill="#cbd5e1" font-family="monospace" font-size="11">--project, --account, --configuration, --zone</text>
        <text x="15" y="60" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Unconditionally overrides all environment variables and saved profiles.</text>

        <!-- Tier 2 -->
        <rect x="0" y="90" width="380" height="85" rx="6" fill="#1e1810" stroke="#f59e0b" stroke-width="1.5"/>
        <text x="15" y="112" fill="#fbbf24" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Tier 2: Environment Variables (Priority 2)</text>
        <text x="15" y="132" fill="#fde68a" font-family="monospace" font-size="11">CLOUDSDK_CORE_PROJECT, CLOUDSDK_ACTIVE_CONFIG_NAME</text>
        <text x="15" y="150" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">Overrides active named configuration files silently within current shell.</text>
        <text x="15" y="165" fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">[CRITICAL RISK: Inherited session exports cause silent context drift]</text>

        <!-- Tier 3 -->
        <rect x="0" y="190" width="380" height="110" rx="6" fill="url(#p19-f2-tier)" stroke="#38bdf8" stroke-width="1.5"/>
        <text x="15" y="212" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Tier 3: Active Named Configuration (Priority 3)</text>
        <text x="15" y="232" fill="#cbd5e1" font-family="monospace" font-size="11">~/.config/gcloud/active_config &rarr; config_NAME</text>
        <text x="15" y="252" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">[core] project = brightloaf-staging, account = dev@brightloaf.com</text>
        <text x="15" y="270" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">[compute] region = us-central1, zone = us-central1-a</text>
        <text x="15" y="288" fill="#64748b" font-family="system-ui, sans-serif" font-size="10">Activated via: gcloud config configurations activate &lt;name&gt;</text>

        <!-- Tier 4 -->
        <rect x="0" y="315" width="380" height="65" rx="6" fill="url(#p19-f2-tier)" stroke="#64748b" stroke-width="1"/>
        <text x="15" y="335" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Tier 4: SDK Installation Defaults (Priority 4 — Fallback)</text>
        <text x="15" y="355" fill="#64748b" font-family="system-ui, sans-serif" font-size="10">System-wide fallbacks (e.g. usage reporting, prompt confirmations)</text>
        <text x="15" y="370" fill="#64748b" font-family="system-ui, sans-serif" font-size="10">Fails with missing project error if tiers 1-3 provide no project ID.</text>
      </g>

      <!-- Flow Lines from Invocations into Ladder -->
      <path d="M 260 130 L 298 130" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#p19-f2-arrow)"/>

      <!-- Output / Resolved Context on Right -->
      <rect x="720" y="80" width="210" height="180" rx="8" fill="#0b1626" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="732" y="104" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Resolved Context State</text>
      <text x="732" y="128" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Project ID:</text>
      <text x="732" y="144" fill="#38bdf8" font-family="monospace" font-size="11">brightloaf-prod</text>
      <text x="732" y="166" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Active Account:</text>
      <text x="732" y="182" fill="#f8fafc" font-family="monospace" font-size="10">ci-runner@iam...</text>
      <text x="732" y="204" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Compute Region:</text>
      <text x="732" y="220" fill="#f8fafc" font-family="monospace" font-size="10">us-central1</text>
      <text x="732" y="245" fill="#4ade80" font-family="system-ui, sans-serif" font-size="10">Verified via: config get-value</text>

      <!-- Target API on Lower Right -->
      <rect x="720" y="285" width="210" height="170" rx="8" fill="#0d1f12" stroke="#22c55e" stroke-width="1.5"/>
      <text x="732" y="309" fill="#4ade80" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Target Google API</text>
      <text x="732" y="332" fill="#cbd5e1" font-family="monospace" font-size="10">POST /compute/v1/projects/</text>
      <text x="732" y="348" fill="#38bdf8" font-family="monospace" font-size="10">brightloaf-prod/...</text>
      <text x="732" y="375" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">OAuth 2.0 Bearer Token</text>
      <text x="732" y="395" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Quota Project Header</text>
      <text x="732" y="425" fill="#22c55e" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">[EXECUTION DISPATCHED]</text>

      <!-- Connecting Ladder to Output -->
      <path d="M 680 115 L 718 115" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#p19-f2-arrow)"/>
      <path d="M 825 260 L 825 283" fill="none" stroke="#22c55e" stroke-width="2" marker-end="url(#p19-f2-arrow-ok)"/>

      <!-- Lower Warning Banner across bottom -->
      <rect x="30" y="475" width="900" height="50" rx="6" fill="#261208" stroke="#f59e0b" stroke-width="1"/>
      <text x="45" y="496" fill="#fbbf24" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Operational Invariant: Never assume active named configuration guarantees target project.</text>
      <text x="45" y="513" fill="#fed7aa" font-family="system-ui, sans-serif" font-size="10">Scripts and CI jobs must either pass explicit --project flags or run a preflight assertion checking gcloud config get-value project against expected target.</text>
    </svg>
<figcaption><strong>Figure 19.2: gcloud Context Precedence Engine and Named Profile Resolution Hierarchy.</strong>
    Maps the evaluation order used by the Google Cloud CLI to resolve project IDs, authenticated accounts, and compute locations before dispatching API calls.
    <br><strong>Supplied facts:</strong> Explicit command-line flags (Tier 1) take highest precedence, followed by environment variables (Tier 2), active named configuration profiles (Tier 3), and system defaults (Tier 4).
    <br><strong>Architectural inference:</strong> Exporting <code>CLOUDSDK_CORE_PROJECT</code> in a shell session silently overrides any profile activated via named configuration profiles, creating an operational trap during cross-environment migrations.
    <br><strong>Expected post-fix behavior:</strong> Automation scripts explicitly pass <code>--project</code> or sanitize ambient environment variables prior to dispatching mutations, ensuring strict project boundary isolation.</figcaption>
</figure>'''

FIG_19_3_HTML = '''<figure class="diagram-container">
<svg role="img" aria-labelledby="fig19-3-title fig19-3-desc" viewBox="0 0 960 520" width="960" height="520" xmlns="http://www.w3.org/2000/svg">
      <title id="fig19-3-title">Incident 19.1: Ephemeral Filesystem Recycling vs Persistent Disk Isolation in Cloud Shell</title>
      <desc id="fig19-3-desc">Incident flow contrasting an emergency hotfix built in ephemeral /tmp wiped by an idle session recycle versus a durable hotfix workspace in /home/naveen with automated environment bootstrapping.</desc>
      <defs>
        <linearGradient id="p19-f3-bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#090d16"/>
          <stop offset="100%" stop-color="#121526"/>
        </linearGradient>
        <marker id="p19-f3-arrow-err" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"/>
        </marker>
        <marker id="p19-f3-arrow-ok" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"/>
        </marker>
      </defs>

      <rect width="960" height="520" rx="12" fill="url(#p19-f3-bg)" stroke="#1e293b" stroke-width="1"/>

      <!-- Title Header -->
      <text x="480" y="32" fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle">Figure 19.3: Incident Flow · Ephemeral Filesystem Recycling vs. Persistent Workspace</text>
      <text x="480" y="50" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle">Cloud Shell Inactivity Purge · Hotfix Loss in /tmp · Idempotent Fulfillment Invariant Defense</text>

      <!-- Event Trigger (Left) -->
      <rect x="30" y="80" width="210" height="160" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="42" y="104" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Trigger: Morning Surge</text>
      <text x="42" y="128" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">06:45 UTC Outage</text>
      <text x="42" y="146" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Brightloaf Order API</text>
      <text x="42" y="164" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Fulfillment worker stalled</text>
      <text x="42" y="186" fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10">SRE opens Cloud Shell</text>
      <text x="42" y="204" fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10">to compile hotfix binary</text>

      <!-- FAILED PATH (Top Branch) -->
      <g transform="translate(270, 80)">
        <rect x="0" y="0" width="380" height="160" rx="8" fill="#1a0f12" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="7 5"/>
        <text x="15" y="24" fill="#f87171" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">[FAILED PATH: Ephemeral Path Build &amp; Idle Timeout]</text>
        <text x="15" y="46" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">1. SRE installs tools into /usr/local/bin</text>
        <text x="15" y="64" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">2. Compiles hotfix patch directly in /tmp/patch-build</text>
        <text x="15" y="84" fill="#fca5a5" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">3. SRE joins 30-min call; 20-min idle timeout triggers!</text>
        <text x="15" y="102" fill="#ef4444" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">FAIL POINT: VM recycled; /tmp and /usr/local wiped clean!</text>
        <text x="15" y="122" fill="#f87171" font-family="system-ui, sans-serif" font-size="10">4. SRE attempts blind recompile with unpinned libs</text>
        <text x="15" y="140" fill="#f87171" font-family="system-ui, sans-serif" font-size="10">MTTR doubled; replay risked duplicate fulfillment!</text>
      </g>

      <!-- CORRECTED PATH (Bottom Branch) -->
      <g transform="translate(270, 270)">
        <rect x="0" y="0" width="380" height="160" rx="8" fill="#09261a" stroke="#22c55e" stroke-width="1.5"/>
        <text x="15" y="24" fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">[CORRECTED PATH: Persistent Disk &amp; Environment Hook]</text>
        <text x="15" y="46" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">1. Tool bootstrap placed in ~/.customize_environment</text>
        <text x="15" y="64" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">2. Source &amp; build artifacts placed in /home/naveen/workspace</text>
        <text x="15" y="84" fill="#86efac" font-family="system-ui, sans-serif" font-size="10">3. Inactivity recycle unmounts 5 GB disk safely</text>
        <text x="15" y="102" fill="#22c55e" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">CONTROL: Disk remounts; bootstrap auto-provisions runtime</text>
        <text x="15" y="122" fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="10">4. Automated test verifies UNIQUE(order_id) constraint</text>
        <text x="15" y="140" fill="#4ade80" font-family="system-ui, sans-serif" font-size="10">Deterministic hotfix deployed with 0 replay duplicates.</text>
      </g>

      <!-- Arrows from Trigger to Paths -->
      <path d="M 240 140 L 268 140" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#p19-f3-arrow-err)"/>
      <path d="M 135 240 L 135 350 L 268 350" fill="none" stroke="#22c55e" stroke-width="2" marker-end="url(#p19-f3-arrow-ok)"/>

      <!-- Verification Boundary on Right -->
      <g transform="translate(690, 80)">
        <rect x="0" y="0" width="240" height="350" rx="8" fill="#0d1527" stroke="#38bdf8" stroke-width="1.5"/>
        <text x="15" y="24" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Verification Boundary</text>
        
        <rect x="15" y="40" width="210" height="85" rx="6" fill="#1e1418" stroke="#ef4444" stroke-width="1"/>
        <text x="25" y="58" fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">Failed State Inspection:</text>
        <text x="25" y="75" fill="#fca5a5" font-family="monospace" font-size="9">$ ls /tmp/patch-build</text>
        <text x="25" y="90" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9">No such file or directory</text>
        <text x="25" y="106" fill="#ef4444" font-family="system-ui, sans-serif" font-size="9">Hotfix &amp; logs lost permanently</text>

        <rect x="15" y="140" width="210" height="120" rx="6" fill="#09261a" stroke="#22c55e" stroke-width="1"/>
        <text x="25" y="158" fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">Corrected State Inspection:</text>
        <text x="25" y="175" fill="#86efac" font-family="monospace" font-size="9">$ test -f ~/workspace/hotfix</text>
        <text x="25" y="190" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9">Artifacts verified intact (5GB PD)</text>
        <text x="25" y="206" fill="#86efac" font-family="monospace" font-size="9">$ python3 test_replay.py</text>
        <text x="25" y="222" fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="9">200 OK: 1 fulfillment recorded</text>
        <text x="25" y="238" fill="#4ade80" font-family="system-ui, sans-serif" font-size="9">Replay rejected duplicate (409)</text>

        <rect x="15" y="275" width="210" height="60" rx="6" fill="#1e293b" stroke="#64748b" stroke-width="1"/>
        <text x="25" y="295" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">Invariant Preserved:</text>
        <text x="25" y="312" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9">Order fulfillment count &le; 1</text>
        <text x="25" y="326" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="9">Survives container recycling</text>
      </g>

      <!-- Connectors to Verification -->
      <path d="M 650 160 L 688 160" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="7 5" marker-end="url(#p19-f3-arrow-err)"/>
      <path d="M 650 350 L 688 350" fill="none" stroke="#22c55e" stroke-width="2" marker-end="url(#p19-f3-arrow-ok)"/>

      <!-- Bottom Banner -->
      <rect x="30" y="460" width="900" height="45" rx="6" fill="#111827" stroke="#334155" stroke-width="1"/>
      <text x="45" y="480" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">Architectural Rule: Never compile or store state in /tmp or /usr/local inside Cloud Shell. Bind persistent workflows to /home/naveen.</text>
      <text x="45" y="495" fill="#64748b" font-family="system-ui, sans-serif" font-size="10">Ensure all emergency recovery binaries validate transactional deduplication keys before dispatching physical inventory.</text>
    </svg>
<figcaption><strong>Figure 19.3: Incident Flow · Ephemeral Filesystem Recycling vs. Persistent Workspace.</strong>
    Contrasts an unrecoverable operational failure in ephemeral storage with a resilient persistent disk workflow during an emergency hotfix.
    <br><strong>Supplied facts:</strong> Cloud Shell sessions terminate after 20 minutes of inactivity; ephemeral directories (<code>/tmp</code>, <code>/usr/local</code>) are purged immediately when the backing container is recycled.
    <br><strong>Architectural inference:</strong> Placing emergency compilation scripts in <code>/tmp</code> without persistent source checkouts doubles recovery time during live outages, jeopardizing order deduplication controls.
    <br><strong>Expected post-fix behavior:</strong> Hotfix development is strictly confined to <code>/home/naveen</code> with automated environment bootstrapping via <code>.customize_environment</code>, ensuring all builds execute idempotent verification tests before deployment.</figcaption>
</figure>'''

FIG_19_4_HTML = '''<figure class="diagram-container">
<svg role="img" aria-labelledby="fig19-4-title fig19-4-desc" viewBox="0 0 960 520" width="960" height="520" xmlns="http://www.w3.org/2000/svg">
      <title id="fig19-4-title">Incident 19.2: Environment Variable Precedence Override in Multi-Project gcloud CLI Execution</title>
      <desc id="fig19-4-desc">Incident flow depicting how an ambient CLOUDSDK_CORE_PROJECT environment variable silently overrode an active named configuration, triggering an accidental production bucket deletion.</desc>
      <defs>
        <linearGradient id="p19-f4-bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#090d16"/>
          <stop offset="100%" stop-color="#121526"/>
        </linearGradient>
        <marker id="p19-f4-arrow-err" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"/>
        </marker>
        <marker id="p19-f4-arrow-ok" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"/>
        </marker>
      </defs>

      <rect width="960" height="520" rx="12" fill="url(#p19-f4-bg)" stroke="#1e293b" stroke-width="1"/>

      <!-- Title Header -->
      <text x="480" y="32" fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle">Figure 19.4: Incident Flow · Ambient Environment Variable Silent Override</text>
      <text x="480" y="50" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle">Tier 2 Env Variable vs. Tier 3 Named Profile · Cross-Project Blast Radius · Idempotency Invariant Check</text>

      <!-- Event Trigger (Left) -->
      <rect x="30" y="80" width="210" height="160" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="42" y="104" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Trigger: Shell Reuse</text>
      <text x="42" y="128" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">09:15 UTC Shell Session</text>
      <text x="42" y="146" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Morning CI test ran:</text>
      <text x="42" y="164" fill="#f59e0b" font-family="monospace" font-size="9">export CLOUDSDK_CORE_PROJECT</text>
      <text x="42" y="180" fill="#f59e0b" font-family="monospace" font-size="9">=brightloaf-prod</text>
      <text x="42" y="204" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Operator activates bl-dev</text>
      <text x="42" y="222" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">and runs cleanup script</text>

      <!-- FAILED PATH (Top Branch) -->
      <g transform="translate(270, 80)">
        <rect x="0" y="0" width="380" height="160" rx="8" fill="#1a0f12" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="7 5"/>
        <text x="15" y="24" fill="#f87171" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">[FAILED PATH: Silent Tier 2 Override Routes to Prod]</text>
        <text x="15" y="46" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">1. Active profile set to: config_brightloaf-dev</text>
        <text x="15" y="64" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">2. Script runs storage bucket cleanup without flags</text>
        <text x="15" y="84" fill="#fca5a5" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">3. CLI evaluates: Tier 2 (Env Var) beats Tier 3 (Profile)!</text>
        <text x="15" y="102" fill="#ef4444" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">FAIL POINT: Production order replay archive bucket purged!</text>
        <text x="15" y="122" fill="#f87171" font-family="system-ui, sans-serif" font-size="10">4. Backup worker triggered order replay from secondary log</text>
        <text x="15" y="140" fill="#f87171" font-family="system-ui, sans-serif" font-size="10">Database UNIQUE constraint halted duplicate fulfillment.</text>
      </g>

      <!-- CORRECTED PATH (Bottom Branch) -->
      <g transform="translate(270, 270)">
        <rect x="0" y="0" width="380" height="160" rx="8" fill="#09261a" stroke="#22c55e" stroke-width="1.5"/>
        <text x="15" y="24" fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">[CORRECTED PATH: Environment Purge &amp; Assertion Guard]</text>
        <text x="15" y="46" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">1. Wrapper script executes: unset CLOUDSDK_CORE_PROJECT</text>
        <text x="15" y="64" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">2. Assert: target == expected</text>
        <text x="15" y="84" fill="#86efac" font-family="system-ui, sans-serif" font-size="10">3. Script passes explicit --project=brightloaf-dev</text>
        <text x="15" y="102" fill="#22c55e" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">CONTROL: Tier 1 flag guarantees target regardless of env vars</text>
        <text x="15" y="122" fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="10">4. Production buckets remain completely untouched</text>
        <text x="15" y="140" fill="#4ade80" font-family="system-ui, sans-serif" font-size="10">Cleanup dispatches strictly to development sandbox.</text>
      </g>

      <!-- Arrows from Trigger to Paths -->
      <path d="M 240 140 L 268 140" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#p19-f4-arrow-err)"/>
      <path d="M 135 240 L 135 350 L 268 350" fill="none" stroke="#22c55e" stroke-width="2" marker-end="url(#p19-f4-arrow-ok)"/>

      <!-- Verification Boundary on Right -->
      <g transform="translate(690, 80)">
        <rect x="0" y="0" width="240" height="350" rx="8" fill="#0d1527" stroke="#38bdf8" stroke-width="1.5"/>
        <text x="15" y="24" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Verification Boundary</text>
        
        <rect x="15" y="40" width="210" height="85" rx="6" fill="#1e1418" stroke="#ef4444" stroke-width="1"/>
        <text x="25" y="58" fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">Failed State Inspection:</text>
        <text x="25" y="75" fill="#fca5a5" font-family="monospace" font-size="9">$ printenv | grep CLOUDSDK</text>
        <text x="25" y="90" fill="#fca5a5" font-family="monospace" font-size="9">CLOUDSDK_CORE_PROJECT=prod</text>
        <text x="25" y="106" fill="#ef4444" font-family="system-ui, sans-serif" font-size="9">Active profile bypassed silently!</text>

        <rect x="15" y="140" width="210" height="120" rx="6" fill="#09261a" stroke="#22c55e" stroke-width="1"/>
        <text x="25" y="158" fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">Corrected State Inspection:</text>
        <text x="25" y="175" fill="#86efac" font-family="monospace" font-size="9">$ ./gcloud-safe-exec.sh</text>
        <text x="25" y="190" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9">[PASS] No CLOUDSDK env leak</text>
        <text x="25" y="206" fill="#86efac" font-family="monospace" font-size="9">[PASS] Target: brightloaf-dev</text>
        <text x="25" y="222" fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="9">[PASS] Exit Code: 0</text>
        <text x="25" y="238" fill="#4ade80" font-family="system-ui, sans-serif" font-size="9">Zero production impact</text>

        <rect x="15" y="275" width="210" height="60" rx="6" fill="#1e293b" stroke="#64748b" stroke-width="1"/>
        <text x="25" y="295" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">Invariant Preserved:</text>
        <text x="25" y="312" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9">Replay check: 0 duplicates</text>
        <text x="25" y="326" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="9">Fulfillment count &le; 1 maintained</text>
      </g>

      <!-- Connectors to Verification -->
      <path d="M 650 160 L 688 160" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="7 5" marker-end="url(#p19-f4-arrow-err)"/>
      <path d="M 650 350 L 688 350" fill="none" stroke="#22c55e" stroke-width="2" marker-end="url(#p19-f4-arrow-ok)"/>

      <!-- Bottom Banner -->
      <rect x="30" y="460" width="900" height="45" rx="6" fill="#111827" stroke="#334155" stroke-width="1"/>
      <text x="45" y="480" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">Architectural Rule: Never rely solely on named configuration activation in automated scripts.</text>
      <text x="45" y="495" fill="#64748b" font-family="system-ui, sans-serif" font-size="10">Always pass explicit Tier 1 flags (--project) or sanitize the execution environment before mutating cloud state.</text>
    </svg>
<figcaption><strong>Figure 19.4: Incident Flow · Ambient Environment Variable Silent Override.</strong>
    Traces how an inherited shell environment variable subverted the active named configuration profile, directing destructive deletions to production.
    <br><strong>Supplied facts:</strong> <code>CLOUDSDK_CORE_PROJECT</code> occupies Tier 2 in the precedence engine; active named profiles occupy Tier 3; unhandled environment exports silently supersede profile activation.
    <br><strong>Architectural inference:</strong> Destructive infrastructure scripts that omit explicit <code>--project</code> parameters will execute against whatever ambient project is exported in the shell, bypassing named profile intentions.
    <br><strong>Expected post-fix behavior:</strong> Automation wrappers scrub <code>CLOUDSDK_*</code> variables and explicitly assert project target identity before running commands, while database uniqueness constraints protect against replay fulfillment duplication.</figcaption>
</figure>'''

FIG_19_5_HTML = '''<figure class="diagram-container">
<svg role="img" aria-labelledby="fig19-5-title fig19-5-desc" viewBox="0 0 960 520" width="960" height="520" xmlns="http://www.w3.org/2000/svg">
      <title id="fig19-5-title">Incident 19.3: Kubeconfig Context Decoupling and Cross-Project Cluster Misdirection</title>
      <desc id="fig19-5-desc">Incident flow illustrating how switching gcloud project failed to update kubectl current-context, causing experimental staging manifests with disabled deduplication to be applied to production GKE.</desc>
      <defs>
        <linearGradient id="p19-f5-bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#090d16"/>
          <stop offset="100%" stop-color="#121526"/>
        </linearGradient>
        <marker id="p19-f5-arrow-err" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"/>
        </marker>
        <marker id="p19-f5-arrow-ok" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"/>
        </marker>
      </defs>

      <rect width="960" height="520" rx="12" fill="url(#p19-f5-bg)" stroke="#1e293b" stroke-width="1"/>

      <!-- Title Header -->
      <text x="480" y="32" fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle">Figure 19.5: Incident Flow · Multi-CLI Context Decoupling &amp; GKE Target Drift</text>
      <text x="480" y="50" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle">gcloud Project Switch vs. ~/.kube/config Current Context · Deduplication Invariant Defense</text>

      <!-- Event Trigger (Left) -->
      <rect x="30" y="80" width="210" height="160" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="42" y="104" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Trigger: Release Staging</text>
      <text x="42" y="128" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">14:20 UTC Release Window</text>
      <text x="42" y="146" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Operator sets project:</text>
      <text x="42" y="164" fill="#38bdf8" font-family="monospace" font-size="9">gcloud &rarr; bl-staging</text>
      <text x="42" y="186" fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10">Runs kubectl deployment</text>
      <text x="42" y="204" fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10">for bakery fulfillment</text>

      <!-- FAILED PATH (Top Branch) -->
      <g transform="translate(270, 80)">
        <rect x="0" y="0" width="380" height="160" rx="8" fill="#1a0f12" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="7 5"/>
        <text x="15" y="24" fill="#f87171" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">[FAILED PATH: Decoupled Kubeconfig Directs Staging to Prod]</text>
        <text x="15" y="46" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">1. gcloud points to brightloaf-staging</text>
        <text x="15" y="64" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">2. ~/.kube/config current-context still points to prod-cluster!</text>
        <text x="15" y="84" fill="#fca5a5" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">3. kubectl apply deployed staging pods with cache disabled!</text>
        <text x="15" y="102" fill="#ef4444" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">FAIL POINT: Staging pods replaced live production pods!</text>
        <text x="15" y="122" fill="#f87171" font-family="system-ui, sans-serif" font-size="10">4. Concurrent consumers attempted duplicate order dispatch</text>
        <text x="15" y="140" fill="#f87171" font-family="system-ui, sans-serif" font-size="10">Database atomic row locks &amp; UNIQUE constraint blocked duplicates.</text>
      </g>

      <!-- CORRECTED PATH (Bottom Branch) -->
      <g transform="translate(270, 270)">
        <rect x="0" y="0" width="380" height="160" rx="8" fill="#09261a" stroke="#22c55e" stroke-width="1.5"/>
        <text x="15" y="24" fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">[CORRECTED PATH: Synchronized Context Switcher &amp; GKE Check]</text>
        <text x="15" y="46" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">1. Unified script checks active project &amp; cluster context parity</text>
        <text x="15" y="64" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10">2. Refreshes credentials: gcloud container clusters get-credentials</text>
        <text x="15" y="84" fill="#86efac" font-family="system-ui, sans-serif" font-size="10">3. Explicit flag passed: kubectl --context=staging-cluster</text>
        <text x="15" y="102" fill="#22c55e" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">CONTROL: Pre-flight validator asserts cluster matches project</text>
        <text x="15" y="122" fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="10">4. Rollback verified: prod-cluster runs certified release image</text>
        <text x="15" y="140" fill="#4ade80" font-family="system-ui, sans-serif" font-size="10">Staging pods deploy strictly to isolated staging namespace.</text>
      </g>

      <!-- Arrows from Trigger to Paths -->
      <path d="M 240 140 L 268 140" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#p19-f5-arrow-err)"/>
      <path d="M 135 240 L 135 350 L 268 350" fill="none" stroke="#22c55e" stroke-width="2" marker-end="url(#p19-f5-arrow-ok)"/>

      <!-- Verification Boundary on Right -->
      <g transform="translate(690, 80)">
        <rect x="0" y="0" width="240" height="350" rx="8" fill="#0d1527" stroke="#38bdf8" stroke-width="1.5"/>
        <text x="15" y="24" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Verification Boundary</text>
        
        <rect x="15" y="40" width="210" height="85" rx="6" fill="#1e1418" stroke="#ef4444" stroke-width="1"/>
        <text x="25" y="58" fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">Failed State Inspection:</text>
        <text x="25" y="75" fill="#fca5a5" font-family="monospace" font-size="9">$ kubectl config current-context</text>
        <text x="25" y="90" fill="#fca5a5" font-family="monospace" font-size="9">gke_brightloaf-prod_..._prod</text>
        <text x="25" y="106" fill="#ef4444" font-family="system-ui, sans-serif" font-size="9">Context decoupled from gcloud!</text>

        <rect x="15" y="140" width="210" height="120" rx="6" fill="#09261a" stroke="#22c55e" stroke-width="1"/>
        <text x="25" y="158" fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">Corrected State Inspection:</text>
        <text x="25" y="175" fill="#86efac" font-family="monospace" font-size="9">$ ./verify-cloud-context.py</text>
        <text x="25" y="190" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9">gcloud project: bl-staging</text>
        <text x="25" y="206" fill="#86efac" font-family="monospace" font-size="9">kubectl context: bl-staging</text>
        <text x="25" y="222" fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="9">[MATCH] Synchronization verified</text>
        <text x="25" y="238" fill="#4ade80" font-family="system-ui, sans-serif" font-size="9">Production cluster protected</text>

        <rect x="15" y="275" width="210" height="60" rx="6" fill="#1e293b" stroke="#64748b" stroke-width="1"/>
        <text x="25" y="295" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">Invariant Preserved:</text>
        <text x="25" y="312" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9">SQL row lock halted double fulfillment</text>
        <text x="25" y="326" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="9">Physical bakery dispatch &le; 1</text>
      </g>

      <!-- Connectors to Verification -->
      <path d="M 650 160 L 688 160" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="7 5" marker-end="url(#p19-f5-arrow-err)"/>
      <path d="M 650 350 L 688 350" fill="none" stroke="#22c55e" stroke-width="2" marker-end="url(#p19-f5-arrow-ok)"/>

      <!-- Bottom Banner -->
      <rect x="30" y="460" width="900" height="45" rx="6" fill="#111827" stroke="#334155" stroke-width="1"/>
      <text x="45" y="480" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">Architectural Rule: Never assume kubectl tracks gcloud project changes. Always inspect kubectl config current-context.</text>
      <text x="45" y="495" fill="#64748b" font-family="system-ui, sans-serif" font-size="10">Ensure database-tier uniqueness constraints back up application-layer deduplication against accidental staging cross-talk.</text>
    </svg>
<figcaption><strong>Figure 19.5: Incident Flow · Multi-CLI Context Decoupling &amp; GKE Target Drift.</strong>
    Demonstrates how the decoupling between <code>gcloud</code> configuration and <code>~/.kube/config</code> misrouted staging Kubernetes manifests to the production cluster.
    <br><strong>Supplied facts:</strong> <code>kubectl</code> determines target clusters entirely from <code>~/.kube/config</code>; changing the active <code>gcloud</code> project does not alter the Kubernetes current context.
    <br><strong>Architectural inference:</strong> Deploying experimental microservice manifests with deduplication caching disabled to production will cause concurrent fulfillment races unless defended by the database layer.
    <br><strong>Expected post-fix behavior:</strong> Multi-CLI automation scripts strictly enforce context parity between <code>gcloud</code> and <code>kubectl</code>, while database unique constraints protect Brightloaf's single-fulfillment invariant.</figcaption>
</figure>'''

