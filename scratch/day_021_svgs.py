"""Day 21 SVGs wrapped in figure containers with non-empty figcaptions."""

FIG_21_1_HTML = '''<figure class="diagram-container">
<svg aria-labelledby="fig21-1-title fig21-1-desc" height="520" role="img" viewbox="0 0 960 520" width="960" xmlns="http://www.w3.org/2000/svg">
<title id="fig21-1-title">Google Cloud Enterprise Resource Hierarchy &amp; Domain Binding Architecture</title>
<desc id="fig21-1-desc">Architectural diagram of the Google Cloud four-tier resource hierarchy rooted in Cloud Identity domain verification, showing Organization, Folders, Projects, and Resources.</desc>
<defs>
<lineargradient id="p21-f1-bg" x1="0%" x2="100%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#090d16"></stop>
<stop offset="100%" stop-color="#121526"></stop>
</lineargradient>
<lineargradient id="p21-f1-panel" x1="0%" x2="0%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#1e293b" stop-opacity="0.8"></stop>
<stop offset="100%" stop-color="#0f172a" stop-opacity="0.9"></stop>
</lineargradient>
<marker id="p21-f1-arrow" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"></path>
</marker>
<marker id="p21-f1-arrow-down" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#818cf8"></path>
</marker>
</defs>
<rect fill="url(#p21-f1-bg)" height="520" rx="12" stroke="#1e293b" stroke-width="1" width="960"></rect>
<!-- Header -->
<text fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" x="480" y="32">Figure 21.1: Google Cloud Enterprise Resource Hierarchy &amp; Domain Anchor</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" x="480" y="50">Cloud Identity Domain Binding · Organization Node Root · Folder Trees · Projects &amp; Leaf Resources</text>
<!-- Cloud Identity Anchor (Top Left) -->
<g transform="translate(30, 75)">
<rect fill="#0d1626" height="120" rx="8" stroke="#38bdf8" stroke-width="1.5" width="250" x="0" y="0"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">Cloud Identity / Workspace</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="46">Domain: brightloaf.com</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="15" y="64">DNS TXT Record Verified</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="15" y="84">Identity Source (Users &amp; Groups)</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" x="15" y="102">Super Admin: admin@brightloaf.com</text>
</g>
<!-- Organization Node (Top Center-Right) -->
<g transform="translate(320, 75)">
<rect fill="url(#p21-f1-panel)" height="120" rx="8" stroke="#6366f1" stroke-width="1.5" width="610" x="0" y="0"></rect>
<text fill="#818cf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" x="20" y="24">Organization Node (organizations/892019481029)</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11" x="20" y="46">• Root of Trust for all IAM permissions and Org Policies</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11" x="20" y="66">• Role: roles/resourcemanager.organizationAdmin</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11" x="20" y="86">• Global Org Policies (e.g. constraints/compute.vmExternalIpAccess)</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11" x="20" y="104">• Aggregated Cloud Audit Log Sink → Central Security Project</text>
</g>
<!-- Link from Domain to Org Node -->
<path d="M 280 135 L 318 135" fill="none" marker-end="url(#p21-f1-arrow)" stroke="#38bdf8" stroke-width="2"></path>
<!-- Folder Layer (Middle) -->
<g transform="translate(30, 220)">
<rect fill="#0b1120" height="110" rx="8" stroke="#818cf8" stroke-width="1.5" width="900" x="0" y="0"></rect>
<text fill="#818cf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" x="20" y="24">Folder Layer (Structural Administrative Boundaries)</text>
<!-- Folder 1: Production -->
<rect fill="#1e1418" height="60" rx="6" stroke="#ef4444" stroke-width="1" width="260" x="30" y="38"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" x="42" y="58">Folder: /Production</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="42" y="74">Restricted IAM: SRE &amp; CI/CD Only</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9" x="42" y="88">Org Policy: No External IPs Enforced</text>
<!-- Folder 2: Non-Production -->
<rect fill="#09261a" height="60" rx="6" stroke="#22c55e" stroke-width="1" width="260" x="320" y="38"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" x="332" y="58">Folder: /Non-Production</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="332" y="74">Delegated: Dev &amp; Staging Teams</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9" x="332" y="88">Sandbox spend caps &amp; auto-shutdown</text>
<!-- Folder 3: Shared-Services -->
<rect fill="#1e1b2e" height="60" rx="6" stroke="#a855f7" stroke-width="1" width="260" x="610" y="38"></rect>
<text fill="#c084fc" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" x="622" y="58">Folder: /Shared-Services</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="622" y="74">Hub VPC, CI Runners, Artifacts</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9" x="622" y="88">Network &amp; Security Team Owners</text>
</g>
<!-- Connecting Downward Arrows Org to Folders -->
<path d="M 625 195 L 625 218" fill="none" marker-end="url(#p21-f1-arrow-down)" stroke="#818cf8" stroke-width="2"></path>
<!-- Projects & Resources Layer (Bottom) -->
<g transform="translate(30, 350)">
<rect fill="#090d16" height="100" rx="8" stroke="#334155" stroke-width="1.5" width="900" x="0" y="0"></rect>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="20" y="22">Projects Layer (Billing &amp; Resource Containers)</text>
<!-- Prod Project -->
<rect fill="#111827" height="55" rx="6" stroke="#475569" stroke-width="1" width="260" x="30" y="32"></rect>
<text fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="42" y="48">brightloaf-fulfillment-prod</text>
<text fill="#38bdf8" font-family="monospace" font-size="9" x="42" y="62">Num: 109283719283 · Cloud SQL &amp; GKE</text>
<text fill="#22c55e" font-family="system-ui, sans-serif" font-size="8" x="42" y="76">UNIQUE(order_id) Invariant Active</text>
<!-- Staging Project -->
<rect fill="#111827" height="55" rx="6" stroke="#475569" stroke-width="1" width="260" x="320" y="32"></rect>
<text fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="332" y="48">brightloaf-fulfillment-stage</text>
<text fill="#38bdf8" font-family="monospace" font-size="9" x="332" y="62">Num: 849102948192 · Staging Pods</text>
<text fill="#f59e0b" font-family="system-ui, sans-serif" font-size="8" x="332" y="76">Automated Integration Replays</text>
<!-- Hub Project -->
<rect fill="#111827" height="55" rx="6" stroke="#475569" stroke-width="1" width="260" x="610" y="32"></rect>
<text fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="622" y="48">brightloaf-network-hub</text>
<text fill="#38bdf8" font-family="monospace" font-size="9" x="622" y="62">Num: 391827401928 · Shared VPC</text>
<text fill="#a855f7" font-family="system-ui, sans-serif" font-size="8" x="622" y="76">Cross-Project Peering Subnets</text>
</g>
<!-- Connecting Downward Arrows Folders to Projects -->
<path d="M 160 330 L 160 348" fill="none" marker-end="url(#p21-f1-arrow-down)" stroke="#818cf8" stroke-width="1.5"></path>
<path d="M 450 330 L 450 348" fill="none" marker-end="url(#p21-f1-arrow-down)" stroke="#818cf8" stroke-width="1.5"></path>
<path d="M 740 330 L 740 348" fill="none" marker-end="url(#p21-f1-arrow-down)" stroke="#818cf8" stroke-width="1.5"></path>
<!-- Bottom Banner -->
<rect fill="#111827" height="42" rx="6" stroke="#334155" stroke-width="1" width="900" x="30" y="465"></rect>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" x="45" y="485">Architectural Rule: IAM permissions are strictly additive down the hierarchy. An allowance at a parent folder cannot be revoked by a child project.</text>
<text fill="#64748b" font-family="system-ui, sans-serif" font-size="10" x="45" y="498">Always isolate production and development environments into dedicated, sibling folder branches.</text>
</svg>
<figcaption>
<strong>Figure 21.1: Google Cloud Enterprise Resource Hierarchy &amp; Domain Anchor.</strong>
    Illustrates the four-tier resource hierarchy model starting from DNS-verified Cloud Identity domain binding, descending through Organization, Folder groupings, Projects, and leaf resources.
    <br/><strong>Supplied facts:</strong> The Organization node is bound 1:1 to a verified Cloud Identity domain; IAM roles and Org Policy constraints inherit downward.
    <br/><strong>Architectural inference:</strong> Placing production and staging workloads in sibling folders prevents privilege leakage and enforces separate organizational policy constraints.
    <br/><strong>Expected post-fix behavior:</strong> Enterprise landing zones isolate environments into structured folder hierarchies, guaranteeing that non-production developer credentials cannot modify production assets.
  </figcaption>
</figure>'''

FIG_21_2_HTML = '''<figure class="diagram-container">
<svg aria-labelledby="fig21-2-title fig21-2-desc" height="520" role="img" viewbox="0 0 960 520" width="960" xmlns="http://www.w3.org/2000/svg">
<title id="fig21-2-title">Folder Hierarchy Patterns &amp; Policy Inheritance Evaluation Tree</title>
<desc id="fig21-2-desc">Comparison of environment-first versus business-unit-first folder structuring models and the additive IAM evaluation ladder down the resource tree.</desc>
<defs>
<lineargradient id="p21-f2-bg" x1="0%" x2="100%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#090d16"></stop>
<stop offset="100%" stop-color="#121526"></stop>
</lineargradient>
<marker id="p21-f2-arrow" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"></path>
</marker>
<marker id="p21-f2-arrow-ok" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"></path>
</marker>
</defs>
<rect fill="url(#p21-f2-bg)" height="520" rx="12" stroke="#1e293b" stroke-width="1" width="960"></rect>
<!-- Title Header -->
<text fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" x="480" y="32">Figure 21.2: Folder Hierarchy Structuring &amp; Additive IAM Inheritance</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" x="480" y="50">Environment-First vs Business-Unit Models · Union Evaluation of IAM Policies · Org Policy Override Rules</text>
<!-- Left Model: Environment-First (Recommended) -->
<g transform="translate(30, 75)">
<rect fill="#0d1626" height="360" rx="8" stroke="#22c55e" stroke-width="1.5" width="430" x="0" y="0"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" x="20" y="25">Pattern A: Environment-First (Recommended)</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="20" y="45">Strict security isolation; policies applied uniformly per lifecycle stage.</text>
<!-- Org Root -->
<rect fill="#1e293b" height="35" rx="4" stroke="#38bdf8" stroke-width="1" width="160" x="135" y="60"></rect>
<text fill="#f8fafc" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" text-anchor="middle" x="215" y="82">Organization: Root</text>
<!-- Tier 1 Folders -->
<rect fill="#1e1418" height="45" rx="4" stroke="#ef4444" stroke-width="1" width="120" x="20" y="120"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" text-anchor="middle" x="80" y="140">/Production</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="8" text-anchor="middle" x="80" y="155">Strict SRE IAM</text>
<rect fill="#09261a" height="45" rx="4" stroke="#22c55e" stroke-width="1" width="120" x="155" y="120"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" text-anchor="middle" x="215" y="140">/Non-Prod</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="8" text-anchor="middle" x="215" y="155">Developer IAM</text>
<rect fill="#1e1b2e" height="45" rx="4" stroke="#a855f7" stroke-width="1" width="120" x="290" y="120"></rect>
<text fill="#c084fc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" text-anchor="middle" x="350" y="140">/Core-Shared</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="8" text-anchor="middle" x="350" y="155">Net &amp; Sec IAM</text>
<!-- Child Projects under Non-Prod -->
<rect fill="#111827" height="40" rx="4" stroke="#475569" stroke-width="1" width="130" x="80" y="195"></rect>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" font-weight="bold" text-anchor="middle" x="145" y="214">proj-order-dev</text>
<text fill="#22c55e" font-family="system-ui, sans-serif" font-size="8" text-anchor="middle" x="145" y="228">Inherits Dev Editor</text>
<rect fill="#111827" height="40" rx="4" stroke="#475569" stroke-width="1" width="130" x="220" y="195"></rect>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" font-weight="bold" text-anchor="middle" x="285" y="214">proj-order-stage</text>
<text fill="#22c55e" font-family="system-ui, sans-serif" font-size="8" text-anchor="middle" x="285" y="228">Inherits Dev Viewer</text>
<!-- Summary of Pattern A -->
<rect fill="#052e16" height="85" rx="4" stroke="#15803d" stroke-width="1" width="390" x="20" y="260"></rect>
<text fill="#86efac" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="30" y="280">ADVANTAGES OF ENVIRONMENT-FIRST:</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="30" y="298">• Zero risk of developer permissions leaking into production</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="30" y="314">• Organizational security constraints applied uniformly per stage</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="30" y="330">• Easy mapping to compliance boundaries (e.g. PCI-DSS, SOC2)</text>
</g>
<!-- Right Model: Additive Policy Evaluation Engine -->
<g transform="translate(500, 75)">
<rect fill="#1e1518" height="360" rx="8" stroke="#f59e0b" stroke-width="1.5" width="430" x="0" y="0"></rect>
<text fill="#fbbf24" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" x="20" y="25">IAM Policy Inheritance Mechanics</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="20" y="45">Effective permissions = UNION of all policy bindings down the path.</text>
<rect fill="#111827" height="55" rx="4" stroke="#6366f1" stroke-width="1" width="390" x="20" y="65"></rect>
<text fill="#818cf8" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="30" y="84">1. Organization Policy Binding:</text>
<text fill="#cbd5e1" font-family="monospace" font-size="9" x="30" y="102">alice@brightloaf.com → roles/resourcemanager.organizationViewer</text>
<rect fill="#111827" height="55" rx="4" stroke="#22c55e" stroke-width="1" width="390" x="20" y="130"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="30" y="149">2. Folder Policy Binding (/Non-Prod):</text>
<text fill="#cbd5e1" font-family="monospace" font-size="9" x="30" y="167">alice@brightloaf.com → roles/editor</text>
<rect fill="#111827" height="55" rx="4" stroke="#38bdf8" stroke-width="1" width="390" x="20" y="195"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="30" y="214">3. Project Policy Binding (proj-order-dev):</text>
<text fill="#cbd5e1" font-family="monospace" font-size="9" x="30" y="232">alice@brightloaf.com → roles/viewer</text>
<!-- Evaluation Output -->
<rect fill="#261208" height="85" rx="4" stroke="#b45309" stroke-width="1" width="390" x="20" y="260"></rect>
<text fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="30" y="280">EFFECTIVE PERMISSION EVALUATION:</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="9" x="30" y="298">• Project Viewer DOES NOT restrict Folder Editor role!</text>
<text fill="#fde68a" font-family="system-ui, sans-serif" font-size="9" x="30" y="314">• Effective access on proj-order-dev = roles/editor (Full Write!)</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="30" y="330">• Rule: IAM cannot restrict access granted higher in the tree.</text>
</g>
<!-- Bottom Banner -->
<rect fill="#111827" height="45" rx="6" stroke="#334155" stroke-width="1" width="900" x="30" y="460"></rect>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" x="45" y="480">Architectural Rule: Never assign permissive broad roles (e.g. Editor) at the Folder or Organization level.</text>
<text fill="#64748b" font-family="system-ui, sans-serif" font-size="10" x="45" y="495">Keep folder-level grants restricted to administrative oversight roles (Viewer, Security Reviewer); assign mutating roles strictly at leaf Projects.</text>
</svg>
<figcaption>
<strong>Figure 21.2: Folder Hierarchy Structuring &amp; Additive IAM Inheritance.</strong>
    Compares the environment-first folder architecture with business-unit models and visualizes the additive nature of IAM role inheritance down the resource tree.
    <br/><strong>Supplied facts:</strong> IAM policies are evaluated as a union: granting a role on a parent folder grants that role on all descendant projects; child projects cannot deny or restrict parent grants.
    <br/><strong>Architectural inference:</strong> Granting developer write roles at a parent folder containing both staging and production projects inevitably leads to accidental production mutations.
    <br/><strong>Expected post-fix behavior:</strong> Organizations structure folders by environment stage (/Production, /Non-Production), reserving parent folder grants for read-only telemetry and binding write access strictly at project boundaries.
  </figcaption>
</figure>'''

FIG_21_3_HTML = '''<figure class="diagram-container">
<svg aria-labelledby="fig21-3-title fig21-3-desc" height="520" role="img" viewbox="0 0 960 520" width="960" xmlns="http://www.w3.org/2000/svg">
<title id="fig21-3-title">Incident 21.1: Rogue Unmanaged Project vs. Organization-Governed Node Migration</title>
<desc id="fig21-3-desc">Incident flow contrasting an unmanaged cloud project created outside the organization node bypassing security policies versus an organization-governed project with enforced security guardrails.</desc>
<defs>
<lineargradient id="p21-f3-bg" x1="0%" x2="100%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#090d16"></stop>
<stop offset="100%" stop-color="#121526"></stop>
</lineargradient>
<marker id="p21-f3-arrow-err" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"></path>
</marker>
<marker id="p21-f3-arrow-ok" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"></path>
</marker>
</defs>
<rect fill="url(#p21-f3-bg)" height="520" rx="12" stroke="#1e293b" stroke-width="1" width="960"></rect>
<!-- Title Header -->
<text fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" x="480" y="32">Figure 21.3: Incident Flow · Rogue Unmanaged Project Creation vs. Org Governance</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" x="480" y="50">Personal Gmail Shadow IT · Bypassed Org Policies · Cloud Identity Root Enforcement</text>
<!-- Event Trigger (Left) -->
<rect fill="#1e293b" height="160" rx="8" stroke="#38bdf8" stroke-width="1.5" width="210" x="30" y="80"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="42" y="104">Trigger: Shadow IT</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="42" y="128">Contractor creates project</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="42" y="146">using personal Gmail:</text>
<text fill="#f59e0b" font-family="monospace" font-size="9" x="42" y="164">dev.contractor@gmail.com</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="42" y="186">Orphan project sits</text>
<text fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10" x="42" y="204">outside organization node</text>
<!-- FAILED PATH (Top Branch) -->
<g transform="translate(270, 80)">
<rect fill="#1a0f12" height="160" rx="8" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="1.5" width="380" x="0" y="0"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">[FAILED PATH: Unmanaged Orphan Project Security Breach]</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="46">1. Project parent = No Organization (Orphan)</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="64">2. Org policies (constraints/compute.vmExternalIp) absent!</text>
<text fill="#fca5a5" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="84">3. Contractor deploys database with public 0.0.0.0 IP</text>
<text fill="#ef4444" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="102">FAIL POINT: Port 5432 exposed; automated scanners probe data!</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" x="15" y="122">4. Contractor departs; corporate admins locked out</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" x="15" y="140">Replay check: Central DB unique constraint blocked duplicates.</text>
</g>
<!-- CORRECTED PATH (Bottom Branch) -->
<g transform="translate(270, 270)">
<rect fill="#09261a" height="160" rx="8" stroke="#22c55e" stroke-width="1.5" width="380" x="0" y="0"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">[CORRECTED PATH: Cloud Identity Enforced Organization]</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="46">1. Project moved into org: gcloud beta projects move</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="64">2. Parent set to: organizations/892019481029</text>
<text fill="#86efac" font-family="system-ui, sans-serif" font-size="10" x="15" y="84">3. Org policy blocks external IP creation automatically</text>
<text fill="#22c55e" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="102">CONTROL: Central audit sink aggregates all operational logs</text>
<text fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="10" x="15" y="122">4. Admin ownership retained via Cloud Identity groups</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" x="15" y="140">Zero orphan exposure; single fulfillment invariant held.</text>
</g>
<!-- Arrows from Trigger to Paths -->
<path d="M 240 140 L 268 140" fill="none" marker-end="url(#p21-f3-arrow-err)" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="2"></path>
<path d="M 135 240 L 135 350 L 268 350" fill="none" marker-end="url(#p21-f3-arrow-ok)" stroke="#22c55e" stroke-width="2"></path>
<!-- Verification Boundary on Right -->
<g transform="translate(690, 80)">
<rect fill="#0d1527" height="350" rx="8" stroke="#38bdf8" stroke-width="1.5" width="240" x="0" y="0"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" x="15" y="24">Verification Boundary</text>
<rect fill="#1e1418" height="85" rx="6" stroke="#ef4444" stroke-width="1" width="210" x="15" y="40"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="58">Failed State Inspection:</text>
<text fill="#fca5a5" font-family="monospace" font-size="9" x="25" y="75">$ gcloud projects describe rogue</text>
<text fill="#fca5a5" font-family="monospace" font-size="9" x="25" y="90">parent: null (No Org)</text>
<text fill="#ef4444" font-family="system-ui, sans-serif" font-size="9" x="25" y="106">Zero audit visibility!</text>
<rect fill="#09261a" height="120" rx="6" stroke="#22c55e" stroke-width="1" width="210" x="15" y="140"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="158">Corrected State Inspection:</text>
<text fill="#86efac" font-family="monospace" font-size="9" x="25" y="175">$ gcloud projects describe bl-analytics</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="25" y="190">parent: organizations/892019...</text>
<text fill="#86efac" font-family="monospace" font-size="9" x="25" y="206">$ gcloud org-policies check</text>
<text fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="9" x="25" y="222">[ENFORCED] vmExternalIpAccess</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="9" x="25" y="238">Audit logs streaming to SIEM</text>
<rect fill="#1e293b" height="60" rx="6" stroke="#64748b" stroke-width="1" width="210" x="15" y="275"></rect>
<text fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="295">Invariant Preserved:</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9" x="25" y="312">Central DB unique constraint</text>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="9" x="25" y="326">Order fulfillment count ≤ 1</text>
</g>
<!-- Connectors to Verification -->
<path d="M 650 160 L 688 160" fill="none" marker-end="url(#p21-f3-arrow-err)" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="1.5"></path>
<path d="M 650 350 L 688 350" fill="none" marker-end="url(#p21-f3-arrow-ok)" stroke="#22c55e" stroke-width="2"></path>
<!-- Bottom Banner -->
<rect fill="#111827" height="45" rx="6" stroke="#334155" stroke-width="1" width="900" x="30" y="460"></rect>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" x="45" y="480">Architectural Rule: Never permit corporate workloads to run in standalone projects outside the Organization node.</text>
<text fill="#64748b" font-family="system-ui, sans-serif" font-size="10" x="45" y="495">Bind project creation permissions exclusively to corporate Cloud Identity groups to maintain enterprise governance.</text>
</svg>
<figcaption>
<strong>Figure 21.3: Incident Flow · Rogue Unmanaged Project Creation vs. Org Governance.</strong>
    Contrasts a security exposure caused by an orphan project created outside corporate boundaries with an organization-anchored project enforcing centralized guardrails.
    <br/><strong>Supplied facts:</strong> Projects created by personal accounts lack an Organization parent, bypassing organizational constraints and central audit logging.
    <br/><strong>Architectural inference:</strong> Unmanaged shadow IT projects expose infrastructure to automated scanners and risk data loss when contractors depart.
    <br/><strong>Expected post-fix behavior:</strong> Projects are moved under the corporate Organization node, inheriting external IP blocks and centralized audit logging, while database deduplication preserves fulfillment invariants.
  </figcaption>
</figure>'''

FIG_21_4_HTML = '''<figure class="diagram-container">
<svg aria-labelledby="fig21-4-title fig21-4-desc" height="520" role="img" viewbox="0 0 960 520" width="960" xmlns="http://www.w3.org/2000/svg">
<title id="fig21-4-title">Incident 21.2: Flat Folder Permission Leakage vs. Segregated Lifecycle Hierarchy</title>
<desc id="fig21-4-desc">Incident flow illustrating how a flat folder containing both production and development projects leaked editor permissions into production, leading to an accidental database drop, and how environment-first folder segregation corrected the defect.</desc>
<defs>
<lineargradient id="p21-f4-bg" x1="0%" x2="100%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#090d16"></stop>
<stop offset="100%" stop-color="#121526"></stop>
</lineargradient>
<marker id="p21-f4-arrow-err" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"></path>
</marker>
<marker id="p21-f4-arrow-ok" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"></path>
</marker>
</defs>
<rect fill="url(#p21-f4-bg)" height="520" rx="12" stroke="#1e293b" stroke-width="1" width="960"></rect>
<!-- Title Header -->
<text fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" x="480" y="32">Figure 21.4: Incident Flow · Flat Folder Permission Leakage vs. Environment Segregation</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" x="480" y="50">Additive IAM Union Trap · Flat Folder Over-Privilege · Environment Sibling Separation</text>
<!-- Event Trigger (Left) -->
<rect fill="#1e293b" height="160" rx="8" stroke="#38bdf8" stroke-width="1.5" width="210" x="30" y="80"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="42" y="104">Trigger: Onboarding</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="42" y="128">Junior dev granted:</text>
<text fill="#f59e0b" font-family="monospace" font-size="9" x="42" y="146">roles/editor on folder</text>
<text fill="#f59e0b" font-family="monospace" font-size="9" x="42" y="164">/Order-Fulfillment</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="42" y="186">Folder holds both</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="42" y="204">dev and prod projects!</text>
<!-- FAILED PATH (Top Branch) -->
<g transform="translate(270, 80)">
<rect fill="#1a0f12" height="160" rx="8" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="1.5" width="380" x="0" y="0"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">[FAILED PATH: Additive IAM Grants Accidental Prod Write]</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="46">1. Dev group assigned roles/editor on /Order-Fulfillment</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="64">2. Additive IAM propagates Editor role to ALL child projects</text>
<text fill="#fca5a5" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="84">3. Dev executes local staging test script: DROP TABLE</text>
<text fill="#ef4444" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="102">FAIL POINT: Script connects to production DB; tables dropped!</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" x="15" y="122">4. Morning bakery dispatch halted; loyalty data corrupted</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" x="15" y="140">DB row-lock stopped duplicate order re-execution.</text>
</g>
<!-- CORRECTED PATH (Bottom Branch) -->
<g transform="translate(270, 270)">
<rect fill="#09261a" height="160" rx="8" stroke="#22c55e" stroke-width="1.5" width="380" x="0" y="0"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">[CORRECTED PATH: Environment Sibling Segregation]</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="46">1. Top-level folders segregated: /Production and /Non-Prod</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="64">2. Devs granted Editor strictly on /Non-Prod folder branch</text>
<text fill="#86efac" font-family="system-ui, sans-serif" font-size="10" x="15" y="84">3. Production folder locked to automated SRE service principals</text>
<text fill="#22c55e" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="102">CONTROL: Test scripts targeting prod fail with 403 Forbidden</text>
<text fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="10" x="15" y="122">4. Zero chance of permission leakage across lifecycle boundaries</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" x="15" y="140">Production integrity and single fulfillment invariant preserved.</text>
</g>
<!-- Arrows from Trigger to Paths -->
<path d="M 240 140 L 268 140" fill="none" marker-end="url(#p21-f4-arrow-err)" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="2"></path>
<path d="M 135 240 L 135 350 L 268 350" fill="none" marker-end="url(#p21-f4-arrow-ok)" stroke="#22c55e" stroke-width="2"></path>
<!-- Verification Boundary on Right -->
<g transform="translate(690, 80)">
<rect fill="#0d1527" height="350" rx="8" stroke="#38bdf8" stroke-width="1.5" width="240" x="0" y="0"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" x="15" y="24">Verification Boundary</text>
<rect fill="#1e1418" height="85" rx="6" stroke="#ef4444" stroke-width="1" width="210" x="15" y="40"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="58">Failed State Inspection:</text>
<text fill="#fca5a5" font-family="monospace" font-size="9" x="25" y="75">$ gcloud asset search-all-iam</text>
<text fill="#fca5a5" font-family="monospace" font-size="9" x="25" y="90">devs: roles/editor on prod!</text>
<text fill="#ef4444" font-family="system-ui, sans-serif" font-size="9" x="25" y="106">Inherited from shared folder</text>
<rect fill="#09261a" height="120" rx="6" stroke="#22c55e" stroke-width="1" width="210" x="15" y="140"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="158">Corrected State Inspection:</text>
<text fill="#86efac" font-family="monospace" font-size="9" x="25" y="175">$ gcloud projects get-iam-policy prod</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="25" y="190">devs: NONE (Zero access)</text>
<text fill="#86efac" font-family="monospace" font-size="9" x="25" y="206">$ test_dev_access.sh</text>
<text fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="9" x="25" y="222">HTTP 403: PERMISSION_DENIED</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="9" x="25" y="238">Production protected 100%</text>
<rect fill="#1e293b" height="60" rx="6" stroke="#64748b" stroke-width="1" width="210" x="15" y="275"></rect>
<text fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="295">Invariant Preserved:</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9" x="25" y="312">DB rollback restored data</text>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="9" x="25" y="326">Single fulfillment invariant held</text>
</g>
<!-- Connectors to Verification -->
<path d="M 650 160 L 688 160" fill="none" marker-end="url(#p21-f3-arrow-err)" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="1.5"></path>
<path d="M 650 350 L 688 350" fill="none" marker-end="url(#p21-f3-arrow-ok)" stroke="#22c55e" stroke-width="2"></path>
<!-- Bottom Banner -->
<rect fill="#111827" height="45" rx="6" stroke="#334155" stroke-width="1" width="900" x="30" y="460"></rect>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" x="45" y="480">Architectural Rule: Never mix development and production projects inside the same parent folder.</text>
<text fill="#64748b" font-family="system-ui, sans-serif" font-size="10" x="45" y="495">Always employ an Environment-First top-level folder hierarchy to prevent additive IAM permissions from compromising production.</text>
</svg>
<figcaption>
<strong>Figure 21.4: Incident Flow · Flat Folder Permission Leakage vs. Environment Segregation.</strong>
    Traces how an unsegregated folder structure allowed developer editor permissions to inherit into production, causing a catastrophic database deletion, and how environment-first separation corrected the defect.
    <br/><strong>Supplied facts:</strong> IAM permissions are additive; assigning roles/editor at a parent folder grants write privileges across all child projects.
    <br/><strong>Architectural inference:</strong> Placing staging and production in a single folder makes accidental cross-environment destruction inevitable during routine testing.
    <br/><strong>Expected post-fix behavior:</strong> Folders are structured strictly by environment stage (/Production, /Non-Production), with developer write grants bounded exclusively to non-production leaf nodes.
  </figcaption>
</figure>'''

FIG_21_5_HTML = '''<figure class="diagram-container">
<svg aria-labelledby="fig21-5-title fig21-5-desc" height="520" role="img" viewbox="0 0 960 520" width="960" xmlns="http://www.w3.org/2000/svg">
<title id="fig21-5-title">Incident 21.3: Project Identifier Conflation &amp; Service Agent Resolution Failure</title>
<desc id="fig21-5-desc">Incident flow depicting how using a mutable project name instead of an immutable project number in cross-project IAM grants broke Google-managed Pub/Sub service agent authentication, dead-lettering bakery orders.</desc>
<defs>
<lineargradient id="p21-f5-bg" x1="0%" x2="100%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#090d16"></stop>
<stop offset="100%" stop-color="#121526"></stop>
</lineargradient>
<marker id="p21-f5-arrow-err" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"></path>
</marker>
<marker id="p21-f5-arrow-ok" markerheight="6" markerwidth="6" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M 0 1 L 10 5 L 0 9 z" fill="#22c55e"></path>
</marker>
</defs>
<rect fill="url(#p21-f5-bg)" height="520" rx="12" stroke="#1e293b" stroke-width="1" width="960"></rect>
<!-- Title Header -->
<text fill="#e2e8f0" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" x="480" y="32">Figure 21.5: Incident Flow · Project Name Conflation &amp; Service Agent Failure</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" x="480" y="50">Project Name vs. Project Number · Service Agent Identity Derivation · Dead-Letter Queue Recovery</text>
<!-- Event Trigger (Left) -->
<rect fill="#1e293b" height="160" rx="8" stroke="#38bdf8" stroke-width="1.5" width="210" x="30" y="80"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="42" y="104">Trigger: Cross-Project IAM</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="42" y="128">Terraform configures:</text>
<text fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10" x="42" y="146">Pub/Sub KMS Decryption</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="42" y="164">Script uses project_name:</text>
<text fill="#f59e0b" font-family="monospace" font-size="9" x="42" y="182">"Brightloaf Order Prod"</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" x="42" y="204">Instead of project_number</text>
<!-- FAILED PATH (Top Branch) -->
<g transform="translate(270, 80)">
<rect fill="#1a0f12" height="160" rx="8" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="1.5" width="380" x="0" y="0"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">[FAILED PATH: Invalid Service Agent Name Breaks KMS Access]</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="46">1. Constructed identity: service-Brightloaf Order Prod@...</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="64">2. IAM API rejects email address with spaces and uppercase</text>
<text fill="#fca5a5" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="84">3. Pub/Sub cannot acquire Cloud KMS decryption key</text>
<text fill="#ef4444" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="102">FAIL POINT: Messages fail decryption; routed to Dead-Letter Queue!</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" x="15" y="122">4. 3,000 bakery delivery orders halted on Friday morning</text>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" x="15" y="140">Recovery replay preserved single fulfillment invariant via DB constraint.</text>
</g>
<!-- CORRECTED PATH (Bottom Branch) -->
<g transform="translate(270, 270)">
<rect fill="#09261a" height="160" rx="8" stroke="#22c55e" stroke-width="1.5" width="380" x="0" y="0"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" x="15" y="24">[CORRECTED PATH: Dynamic Project Number Resolution]</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="46">1. Terraform queries: data.google_project.project.number</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="10" x="15" y="64">2. Resolves immutable number: 892019481029</text>
<text fill="#86efac" font-family="system-ui, sans-serif" font-size="10" x="15" y="84">3. Constructs: service-892019481029@gcp-sa-pubsub.iam...</text>
<text fill="#22c55e" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="15" y="102">CONTROL: Valid service agent granted roles/cloudkms.cryptoKeyEncrypterDecrypter</text>
<text fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="10" x="15" y="122">4. DLQ messages replayed cleanly; orders dispatched smoothly</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" x="15" y="140">Database unique constraint guarantees zero double fulfillments.</text>
</g>
<!-- Arrows from Trigger to Paths -->
<path d="M 240 140 L 268 140" fill="none" marker-end="url(#p21-f5-arrow-err)" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="2"></path>
<path d="M 135 240 L 135 350 L 268 350" fill="none" marker-end="url(#p21-f5-arrow-ok)" stroke="#22c55e" stroke-width="2"></path>
<!-- Verification Boundary on Right -->
<g transform="translate(690, 80)">
<rect fill="#0d1527" height="350" rx="8" stroke="#38bdf8" stroke-width="1.5" width="240" x="0" y="0"></rect>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" x="15" y="24">Verification Boundary</text>
<rect fill="#1e1418" height="85" rx="6" stroke="#ef4444" stroke-width="1" width="210" x="15" y="40"></rect>
<text fill="#f87171" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="58">Failed IAM State:</text>
<text fill="#fca5a5" font-family="monospace" font-size="9" x="25" y="75">Error: Invalid member email</text>
<text fill="#fca5a5" font-family="monospace" font-size="9" x="25" y="90">service-Brightloaf Order...</text>
<text fill="#ef4444" font-family="system-ui, sans-serif" font-size="9" x="25" y="106">KMS decryption blocked!</text>
<rect fill="#09261a" height="120" rx="6" stroke="#22c55e" stroke-width="1" width="210" x="15" y="140"></rect>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="158">Corrected IAM State:</text>
<text fill="#86efac" font-family="monospace" font-size="9" x="25" y="175">$ gcloud projects describe</text>
<text fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9" x="25" y="190">projectNumber: 892019481029</text>
<text fill="#86efac" font-family="monospace" font-size="9" x="25" y="206">$ gcloud kms check-iam</text>
<text fill="#bbf7d0" font-family="system-ui, sans-serif" font-size="9" x="25" y="222">service-892019... has Decrypter</text>
<text fill="#4ade80" font-family="system-ui, sans-serif" font-size="9" x="25" y="238">DLQ queue drained to 0</text>
<rect fill="#1e293b" height="60" rx="6" stroke="#64748b" stroke-width="1" width="210" x="15" y="275"></rect>
<text fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" x="25" y="295">Invariant Preserved:</text>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9" x="25" y="312">Replayed DLQ orders: 3,000</text>
<text fill="#38bdf8" font-family="system-ui, sans-serif" font-size="9" x="25" y="326">Physical dispatches ≤ 1 each</text>
</g>
<!-- Connectors to Verification -->
<path d="M 650 160 L 688 160" fill="none" marker-end="url(#p21-f5-arrow-err)" stroke="#ef4444" stroke-dasharray="7 5" stroke-width="1.5"></path>
<path d="M 650 350 L 688 350" fill="none" marker-end="url(#p21-f5-arrow-ok)" stroke="#22c55e" stroke-width="2"></path>
<!-- Bottom Banner -->
<rect fill="#111827" height="45" rx="6" stroke="#334155" stroke-width="1" width="900" x="30" y="460"></rect>
<text fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" x="45" y="480">Architectural Rule: Google-managed service agents strictly derive from the Project Number, never the Project Name or Project ID.</text>
<text fill="#64748b" font-family="system-ui, sans-serif" font-size="10" x="45" y="495">Always resolve project numbers programmatically when configuring cross-project service-to-service IAM bindings.</text>
</svg>
<figcaption>
<strong>Figure 21.5: Incident Flow · Project Name Conflation &amp; Service Agent Failure.</strong>
    Demonstrates how confusing the project display name with the immutable project number broke Google-managed Pub/Sub service agent KMS decryption grants, resulting in message dead-lettering.
    <br/><strong>Supplied facts:</strong> Project names are mutable strings allowing spaces and mixed case; Google-managed service agent identities strictly require the 12-digit Project Number.
    <br/><strong>Architectural inference:</strong> Using project names in automation variables generates invalid IAM member emails, breaking asynchronous service authorizations.
    <br/><strong>Expected post-fix behavior:</strong> Infrastructure scripts dynamically query the project number, establishing valid service agent bindings and allowing replayed dead-letter messages to fulfill cleanly with zero duplicate transactions.
  </figcaption>
</figure>'''

