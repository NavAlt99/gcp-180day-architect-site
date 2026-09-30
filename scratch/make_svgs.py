def get_topology_svg():
    return '''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg aria-labelledby="d1-top-title d1-top-desc" height="auto" role="img" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;" viewbox="0 0 1120 690" width="100%">
<title id="d1-top-title">Day 1 local workspace process flow, artifact storage, and governance boundary</title>
<desc id="d1-top-desc">Architecture topology showing three distinct tiers: Command Ingress and Planning Demand (Tier 1), Runtime Execution and Artifact Repository (Tier 2), and Governance, Integrity and Replay Invariants (Tier 3), connected by exact vertical drops into component centers, with system probes and verification boundaries.</desc>
<defs>
<marker id="d1-top-arr-ok" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#22c55e" points="0 0, 8 4, 0 8"></polygon></marker>
<marker id="d1-top-arr-fail" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#f43f5e" points="0 0, 8 4, 0 8"></polygon></marker>
<marker id="d1-top-arr-warn" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#f59e0b" points="0 0, 8 4, 0 8"></polygon></marker>
<marker id="d1-top-arr-blue" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#38bdf8" points="0 0, 8 4, 0 8"></polygon></marker>
</defs>

<!-- TIER 1: COMMAND INGRESS & DEMAND (y=55..147) -->
<rect fill="#1e3a5f" height="92" opacity="0.45" rx="6" width="1080" x="20" y="55"></rect>
<rect fill="#090d16" height="18" rx="4" stroke="#7dd3fc" stroke-opacity="0.3" stroke-width="1" width="1080" x="20" y="55"></rect>
<text fill="#7dd3fc" font-family="monospace" font-size="9.5" font-weight="bold" x="32" y="68">DEMAND &amp; COMMAND INGRESS (TIER 1)</text>
<text fill="#94a3b8" font-family="monospace" font-size="8.5" text-anchor="end" x="1086" y="68">developer terminal · shell parser · stream binding · budget target</text>

<!-- Tier 1 Cards: Centers at x=150, 420, 692.5, 965 -->
<rect fill="#1e293b" height="45" rx="4" stroke="#38bdf8" stroke-width="1.5" width="200" x="50" y="88"></rect>
<text fill="#38bdf8" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="150" y="106">Developer Terminal</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="150" y="122">Interactive Bash / CLI input</text>

<rect fill="#1e293b" height="45" rx="4" stroke="#38bdf8" stroke-width="1.5" width="210" x="315" y="88"></rect>
<text fill="#38bdf8" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="420" y="106">Shell Parser &amp; Env</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="420" y="122">PATH resolution · env vars</text>

<rect fill="#1e293b" height="45" rx="4" stroke="#38bdf8" stroke-width="1.5" width="215" x="585" y="88"></rect>
<text fill="#38bdf8" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="692.5" y="106">Stream Bindings</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="692.5" y="122">stdin (0) · stdout (1) · stderr (2)</text>

<rect fill="#1e293b" height="45" rx="4" stroke="#38bdf8" stroke-width="1.5" width="210" x="860" y="88"></rect>
<text fill="#38bdf8" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="965" y="106">Study &amp; Budget Policy</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="965" y="122">Weekly hours &amp; $50 lab target</text>

<!-- Horizontal flow lines in Tier 1 -->
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="250" x2="315" y1="110" y2="110"></line>
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="525" x2="585" y1="110" y2="110"></line>
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="800" x2="860" y1="110" y2="110"></line>

<!-- EXACT VERTICAL DROPS (x1=x2) FROM TIER 1 TO TIER 2 -->
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="150" x2="150" y1="133" y2="220"></line>
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="420" x2="420" y1="133" y2="220"></line>
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="692.5" x2="692.5" y1="133" y2="220"></line>
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="965" x2="965" y1="133" y2="220"></line>

<!-- TIER 2: RUNTIME EXECUTION & ARTIFACT REPOSITORY (y=185..395) -->
<rect fill="#064e3b" height="210" opacity="0.45" rx="6" width="1080" x="20" y="185"></rect>
<rect fill="#090d16" height="18" rx="4" stroke="#6ee7b7" stroke-opacity="0.3" stroke-width="1" width="1080" x="20" y="185"></rect>
<text fill="#6ee7b7" font-family="monospace" font-size="9.5" font-weight="bold" x="32" y="198">RUNTIME EXECUTION &amp; ARTIFACT REPOSITORY (TIER 2)</text>
<text fill="#94a3b8" font-family="monospace" font-size="8.5" text-anchor="end" x="1086" y="198">POSIX child process · volatile $? · git objects · local storage</text>

<!-- Tier 2 Upper Cards: y=220..275 -->
<rect fill="#1e293b" height="55" rx="4" stroke="#6ee7b7" stroke-width="1.5" width="200" x="50" y="220"></rect>
<text fill="#6ee7b7" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="150" y="242">POSIX Child Process</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="150" y="260">fork() &amp; execve() execution</text>

<rect fill="#1e293b" height="55" rx="4" stroke="#6ee7b7" stroke-width="1.5" width="210" x="315" y="220"></rect>
<text fill="#6ee7b7" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="420" y="242">Volatile Exit Register</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="420" y="260">Ephemeral $? register</text>

<rect fill="#1e293b" height="55" rx="4" stroke="#6ee7b7" stroke-width="1.5" width="215" x="585" y="220"></rect>
<text fill="#6ee7b7" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="692.5" y="242">Observation File</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="692.5" y="260">command-observation.txt</text>

<rect fill="#1e293b" height="55" rx="4" stroke="#6ee7b7" stroke-width="1.5" width="210" x="860" y="220"></rect>
<text fill="#6ee7b7" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="965" y="242">Synthetic Order Fixture</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="965" y="260">fixtures/synthetic-order.json</text>

<!-- Tier 2 Lower Cards: y=318..373 -->
<rect fill="#121526" height="55" rx="4" stroke="#38bdf8" stroke-width="1.5" width="230" x="175" y="318"></rect>
<text fill="#38bdf8" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="290" y="340">Signal Trap &amp; Exit Handler</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="290" y="358">status=$? immediately trapped</text>

<rect fill="#121526" height="55" rx="4" stroke="#38bdf8" stroke-width="1.5" width="240" x="675" y="318"></rect>
<text fill="#38bdf8" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="795" y="340">Git Index &amp; Object Store</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="795" y="358">Staged blobs &amp; commit objects</text>

<!-- Connecting lines inside Tier 2 -->
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.0" x1="150" x2="230" y1="275" y2="318"></line>
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.0" x1="420" x2="350" y1="275" y2="318"></line>
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.0" x1="692.5" x2="740" y1="275" y2="318"></line>
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.0" x1="965" x2="850" y1="275" y2="318"></line>
<line marker-end="url(#d1-top-arr-blue)" stroke="#38bdf8" stroke-dasharray="4,3" stroke-width="2.0" x1="405" x2="675" y1="345" y2="345"></line>

<!-- EXACT VERTICAL DROPS (x1=x2) FROM TIER 2 TO TIER 3 -->
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="160" x2="160" y1="373" y2="465"></line>
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="425" x2="425" y1="373" y2="465"></line>
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="700" x2="700" y1="373" y2="465"></line>
<line marker-end="url(#d1-top-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="967.5" x2="967.5" y1="373" y2="465"></line>

<!-- TIER 3: GOVERNANCE, INTEGRITY & REPLAY INVARIANTS (y=435..550) -->
<rect fill="#422006" height="115" opacity="0.45" rx="6" width="1080" x="20" y="435"></rect>
<rect fill="#090d16" height="18" rx="4" stroke="#fdba74" stroke-opacity="0.3" stroke-width="1" width="1080" x="20" y="435"></rect>
<text fill="#fdba74" font-family="monospace" font-size="9.5" font-weight="bold" x="32" y="448">GOVERNANCE, INTEGRITY &amp; REPLAY INVARIANTS (TIER 3)</text>
<text fill="#94a3b8" font-family="monospace" font-size="8.5" text-anchor="end" x="1086" y="448">exit status verification · clean git status · zero PII · alerts-only budget</text>

<!-- Invariant verification boundary enclosing Tier 3 -->
<rect fill="none" height="128" rx="4" stroke="#f59e0b" stroke-dasharray="5,3" stroke-width="2" width="1045" x="35" y="426"></rect>
<rect fill="#0f172a" height="17" rx="3" stroke="#f59e0b" stroke-width="1.5" width="410" x="660" y="546"></rect>
<text fill="#f59e0b" font-family="monospace" font-size="8.5" font-weight="bold" text-anchor="middle" x="865" y="558">INVARIANT VERIFICATION BOUNDARY: EVIDENCE &amp; GOVERNANCE ENFORCED</text>

<!-- Tier 3 Cards: Centers at x=160, 425, 700, 967.5 -->
<rect fill="#1e293b" height="50" rx="4" stroke="#fdba74" stroke-width="1.5" width="220" x="50" y="465"></rect>
<text fill="#fdba74" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="160" y="486">Exit Status Gate</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="160" y="504">assert status == 0</text>

<rect fill="#1e293b" height="50" rx="4" stroke="#fdba74" stroke-width="1.5" width="220" x="315" y="465"></rect>
<text fill="#fdba74" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="425" y="486">Clean Git Tree Guard</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="425" y="504">git status --porcelain == 0</text>

<rect fill="#1e293b" height="50" rx="4" stroke="#fdba74" stroke-width="1.5" width="230" x="585" y="465"></rect>
<text fill="#fdba74" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="700" y="486">Budget &amp; Teardown Charter</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="700" y="504">Alerts-only awareness &amp; owner</text>

<rect fill="#1e293b" height="50" rx="4" stroke="#fdba74" stroke-width="1.5" width="215" x="860" y="465"></rect>
<text fill="#fdba74" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" x="967.5" y="486">Idempotent Replay Key</text>
<text fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle" x="967.5" y="504">Single fulfillment per order</text>

<!-- In-Diagram Probe badges -->
<circle cx="420" cy="220" fill="#38bdf8" opacity="0.95" r="10" stroke="#ffffff" stroke-width="1.5"></circle>
<text fill="white" font-family="monospace" font-size="8" font-weight="bold" text-anchor="middle" x="420" y="223">P1</text>
<circle cx="795" cy="318" fill="#22c55e" opacity="0.95" r="10" stroke="#ffffff" stroke-width="1.5"></circle>
<text fill="white" font-family="monospace" font-size="8" font-weight="bold" text-anchor="middle" x="795" y="321">P2</text>
<circle cx="967.5" cy="465" fill="#f59e0b" opacity="0.95" r="10" stroke="#ffffff" stroke-width="1.5"></circle>
<text fill="white" font-family="monospace" font-size="8" font-weight="bold" text-anchor="middle" x="967.5" y="468">P3</text>

<!-- SYSTEM PROBE PANEL (y=585..637) -->
<rect fill="#090d16" height="52" opacity="0.95" rx="4" stroke="#1e293b" stroke-width="1" width="1100" x="10" y="585"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="10" font-weight="bold" x="24" y="601">SYSTEM PROBES &amp; INVARIANT VERIFICATION CHECKPOINTS:</text>
<circle cx="32" cy="618" fill="#38bdf8" r="7"></circle>
<text fill="white" font-family="monospace" font-size="7.5" font-weight="bold" text-anchor="middle" x="32" y="621">P1</text>
<text fill="#38bdf8" font-family="monospace" font-size="9" x="44" y="621">P1: Trap $? register immediately before executing any subsequent logging or diagnostic commands</text>
<circle cx="430" cy="618" fill="#22c55e" r="7"></circle>
<text fill="white" font-family="monospace" font-size="7.5" font-weight="bold" text-anchor="middle" x="430" y="621">P2</text>
<text fill="#22c55e" font-family="monospace" font-size="9" x="442" y="621">P2: Verify working tree cleanliness (git status --porcelain) and commit object hash</text>
<circle cx="785" cy="618" fill="#f59e0b" r="7"></circle>
<text fill="white" font-family="monospace" font-size="7.5" font-weight="bold" text-anchor="middle" x="785" y="621">P3</text>
<text fill="#f59e0b" font-family="monospace" font-size="9" x="797" y="621">P3: Enforce synthetic data boundary (zero PII) and durable event replay idempotency</text>

<!-- LEGEND BAR (y=646..682) -->
<rect fill="#0f172a" height="36" opacity="0.8" rx="4" stroke="#1e293b" width="1100" x="10" y="646"></rect>
<line stroke="#22c55e" stroke-width="2.5" x1="22" x2="62" y1="664" y2="664"></line>
<text fill="#22c55e" font-family="monospace" font-size="11" x="68" y="668">CORRECTED / AUTHORIZED</text>
<line stroke="#f43f5e" stroke-dasharray="6,4" stroke-width="2" x1="250" x2="290" y1="664" y2="664"></line>
<text fill="#f43f5e" font-family="monospace" font-size="11" x="296" y="668">FAILED / DENIED</text>
<rect fill="none" height="12" stroke="#f59e0b" stroke-dasharray="4,2" stroke-width="2" width="12" x="460" y="658"></rect>
<text fill="#f59e0b" font-family="monospace" font-size="11" x="480" y="668">VERIFY BOUNDARY</text>
<circle cx="670" cy="664" fill="#f43f5e" r="6"></circle>
<text fill="#f43f5e" font-family="monospace" font-size="11" x="682" y="668">FI = Fault Injection Point</text>
</svg></div>
<figcaption>Figure 1.1: Local workspace process flow, artifact storage, and governance boundary for Day 1. It demonstrates where evidence capture and policy controls belong; it does not prove cloud infrastructure health, remote API acceptance, or automated billing termination.</figcaption>
</figure>'''

def get_incident_svg_1():
    return '''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg aria-labelledby="d1-case-1-title d1-case-1-desc" height="auto" role="img" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;" viewbox="0 0 1020 455" width="100%">
<title id="d1-case-1-title">Case 1 · Process exit status capture vs uncaptured command failure in release gate</title>
<desc id="d1-case-1-desc">Dual-lane incident diagram comparing a failed path where volatile exit status is overwritten by logging, leading to a false-positive release gate pass, against a corrected path where the exit code and output are immediately trapped and validated.</desc>
<defs>
<marker id="d1-case-1-arr-ok" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#22c55e" points="0 0, 8 4, 0 8"></polygon></marker>
<marker id="d1-case-1-arr-fail" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#f43f5e" points="0 0, 8 4, 0 8"></polygon></marker>
<marker id="d1-case-1-arr-warn" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#f59e0b" points="0 0, 8 4, 0 8"></polygon></marker>
</defs>
<!-- Header Bar -->
<rect fill="#1e293b" height="26" opacity="0.8" rx="4" width="990" x="15" y="10"></rect>
<text fill="#cbd5e1" font-family="monospace" font-size="11" font-weight="bold" x="25" y="27">INCIDENT COMPARISON: Local workspace and evidence repository · Process exit status capture</text>

<!-- UPPER LANE: FAILED PATH -->
<rect fill="#180b12" height="175" rx="6" stroke="#881337" stroke-width="1.5" width="990" x="15" y="44"></rect>
<rect fill="#2d0b13" height="20" rx="3" stroke="#f43f5e" stroke-width="1" width="220" x="25" y="52"></rect>
<text fill="#f43f5e" font-family="monospace" font-size="9" font-weight="bold" text-anchor="middle" x="135" y="66">FAILED PATH · UNMITIGATED CASCADE</text>

<!-- Node 1: Trigger -->
<g transform="translate(150, 140)">
<rect fill="#121526" height="100" rx="4" stroke="#94a3b8" stroke-width="1.5" width="230" x="-115" y="-50"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">1. INITIATING EVENT</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Release gate runs pre-deploy</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">schema check command;</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">process returns exit code 1</text>
<rect fill="#1e293b" height="16" rx="2" width="140" x="-70" y="24"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[UNTRAPPED STATUS]</text>
</g>

<!-- Arrow 1 -> 2 -->
<line marker-end="url(#d1-case-1-arr-fail)" stroke="#f43f5e" stroke-dasharray="6,4" stroke-width="2.5" x1="270" x2="350" y1="140" y2="140"></line>
<text fill="#f43f5e" font-family="monospace" font-size="8" text-anchor="middle" x="310" y="132">TRIGGERS</text>

<!-- Node 2: Root Cause Defect -->
<g transform="translate(480, 140)">
<rect fill="#2a0a10" height="100" rx="4" stroke="#f43f5e" stroke-width="2" width="240" x="-120" y="-50"></rect>
<circle cx="-100" cy="-34" fill="#f43f5e" r="8"></circle>
<text fill="white" font-family="monospace" font-size="8" font-weight="bold" text-anchor="middle" x="-100" y="-31">FI</text>
<text fill="#f43f5e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="10" y="-30">2. ROOT CAUSE DEFECT</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Wrapper runs logging command</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">immediately after check,</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">overwriting $? register with 0</text>
<rect fill="#3b0d18" height="16" rx="2" width="140" x="-70" y="24"></rect>
<text fill="#fda4af" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[VOLATILE OVERWRITE]</text>
</g>

<!-- Arrow 2 -> 3 -->
<line marker-end="url(#d1-case-1-arr-fail)" stroke="#f43f5e" stroke-dasharray="6,4" stroke-width="2.5" x1="605" x2="685" y1="140" y2="140"></line>
<text fill="#f43f5e" font-family="monospace" font-size="8" text-anchor="middle" x="645" y="132">CASCADES</text>

<!-- Node 3: Impact -->
<g transform="translate(820, 140)">
<rect fill="#380914" height="100" rx="4" stroke="#f43f5e" stroke-width="2" width="250" x="-125" y="-50"></rect>
<text fill="#f43f5e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">3. IMPACT &amp; DEGRADATION</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Gate reports success; broken</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">schema deployed to staging;</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">Order API crashes in runtime</text>
<rect fill="#4c0519" height="16" rx="2" width="150" x="-75" y="24"></rect>
<text fill="#fda4af" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[SILENT CORRUPTION]</text>
</g>

<!-- LOWER LANE: CORRECTED PATH -->
<rect fill="#061f15" height="175" rx="6" stroke="#065f46" stroke-width="1.5" width="990" x="15" y="230"></rect>
<rect fill="#064e3b" height="20" rx="3" stroke="#22c55e" stroke-width="1" width="230" x="25" y="238"></rect>
<text fill="#22c55e" font-family="monospace" font-size="9" font-weight="bold" text-anchor="middle" x="140" y="252">CORRECTED PATH · ENFORCED CONTROL</text>

<!-- Node 1: Same Trigger -->
<g transform="translate(150, 326)">
<rect fill="#121526" height="100" rx="4" stroke="#94a3b8" stroke-width="1.5" width="230" x="-115" y="-50"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">1. SAME TRIGGER EVENT</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Release gate runs pre-deploy</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">schema check command;</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">process returns exit code 1</text>
<rect fill="#1e293b" height="16" rx="2" width="140" x="-70" y="24"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[IDENTICAL INPUT]</text>
</g>

<!-- Arrow 1 -> 2 -->
<line marker-end="url(#d1-case-1-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="270" x2="350" y1="326" y2="326"></line>
<text fill="#22c55e" font-family="monospace" font-size="8" text-anchor="middle" x="310" y="318">INTERCEPT</text>

<!-- Invariant boundary enclosing Card 2 and 3 -->
<rect fill="none" height="150" rx="6" stroke="#f59e0b" stroke-dasharray="5,3" stroke-width="1.5" width="645" x="345" y="244"></rect>
<text fill="#f59e0b" font-family="monospace" font-size="9" font-weight="bold" text-anchor="middle" x="668" y="256">INVARIANT VERIFICATION BOUNDARY: GUARDRAIL ENFORCED</text>

<!-- Node 2: Defensive Control -->
<g transform="translate(480, 326)">
<rect fill="#064e3b" height="100" rx="4" stroke="#22c55e" stroke-width="2" width="240" x="-120" y="-50"></rect>
<text fill="#22c55e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">2. DEFENSIVE CONTROL</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Trap status=$? immediately;</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">redirect stdout/stderr to file;</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">assert $status -eq 0 gate</text>
<rect fill="#022c22" height="16" rx="2" width="150" x="-75" y="24"></rect>
<text fill="#6ee7b7" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[TRAPPED &amp; PERSISTED]</text>
</g>

<!-- Arrow 2 -> 3 -->
<line marker-end="url(#d1-case-1-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="605" x2="685" y1="326" y2="326"></line>
<text fill="#22c55e" font-family="monospace" font-size="8" text-anchor="middle" x="645" y="318">PRESERVES</text>

<!-- Node 3: Outcome -->
<g transform="translate(820, 326)">
<rect fill="#022c22" height="100" rx="4" stroke="#22c55e" stroke-width="2" width="250" x="-125" y="-50"></rect>
<text fill="#22c55e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">3. VERIFIED OUTCOME</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Non-zero status halts release;</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">error artifact recorded;</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">zero staging corruption</text>
<rect fill="#064e3b" height="16" rx="2" width="150" x="-75" y="24"></rect>
<text fill="#6ee7b7" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[GATE DEFENDED]</text>
</g>

<!-- Legend Bar -->
<rect fill="#0f172a" height="32" rx="4" stroke="#1e293b" stroke-width="1" width="990" x="15" y="414"></rect>
<line stroke="#22c55e" stroke-width="2.5" x1="28" x2="60" y1="430" y2="430"></line>
<text fill="#22c55e" font-family="monospace" font-size="10" x="66" y="434">CORRECTED PATH</text>
<line stroke="#f43f5e" stroke-dasharray="4,3" stroke-width="2" x1="200" x2="232" y1="430" y2="430"></line>
<text fill="#f43f5e" font-family="monospace" font-size="10" x="238" y="434">FAILED PATH</text>
<rect fill="none" height="12" stroke="#f59e0b" stroke-dasharray="4,2" stroke-width="1.5" width="12" x="360" y="424"></rect>
<text fill="#f59e0b" font-family="monospace" font-size="10" x="380" y="434">VERIFICATION BOUNDARY</text>
<circle cx="560" cy="430" fill="#f43f5e" r="5"></circle>
<text fill="#f43f5e" font-family="monospace" font-size="10" x="572" y="434">FI = Fault Injection Point</text>
</svg></div>
<figcaption><strong>Supplied facts:</strong> Pre-deployment schema check exited with code 1; wrapper shell script executed an uncaptured echo statement immediately after, resetting $? to 0; release pipeline evaluated the reset status and triggered deployment.<br/><strong>Architectural inference:</strong> The shell status parameter $? is an ephemeral single-value register overwritten by every foreground command; without immediate variable assignment or set -e / pipefail enforcement, process failure signals are destroyed.<br/><strong>Expected post-fix behavior:</strong> The wrapper script binds status immediately (<code>status=$?</code>), redirects process streams to a timestamped file, and evaluates the preserved status to abort deployment deterministically on non-zero exit.</figcaption>
</figure>'''

def get_incident_svg_2():
    return '''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg aria-labelledby="d1-case-2-title d1-case-2-desc" height="auto" role="img" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;" viewbox="0 0 1020 455" width="100%">
<title id="d1-case-2-title">Case 2 · Calendar-driven progression vs capacity-based competence baseline</title>
<desc id="d1-case-2-desc">Dual-lane incident diagram contrasting an unmitigated progression where calendar days are mistaken for technical mastery against an enforced baseline gate where advancement requires verified artifacts.</desc>
<defs>
<marker id="d1-case-2-arr-ok" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#22c55e" points="0 0, 8 4, 0 8"></polygon></marker>
<marker id="d1-case-2-arr-fail" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#f43f5e" points="0 0, 8 4, 0 8"></polygon></marker>
<marker id="d1-case-2-arr-warn" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#f59e0b" points="0 0, 8 4, 0 8"></polygon></marker>
</defs>
<!-- Header Bar -->
<rect fill="#1e293b" height="26" opacity="0.8" rx="4" width="990" x="15" y="10"></rect>
<text fill="#cbd5e1" font-family="monospace" font-size="11" font-weight="bold" x="25" y="27">INCIDENT COMPARISON: Study sessions and learning baseline · Capacity vs calendar pacing</text>

<!-- UPPER LANE: FAILED PATH -->
<rect fill="#180b12" height="175" rx="6" stroke="#881337" stroke-width="1.5" width="990" x="15" y="44"></rect>
<rect fill="#2d0b13" height="20" rx="3" stroke="#f43f5e" stroke-width="1" width="220" x="25" y="52"></rect>
<text fill="#f43f5e" font-family="monospace" font-size="9" font-weight="bold" text-anchor="middle" x="135" y="66">FAILED PATH · UNMITIGATED CASCADE</text>

<!-- Node 1: Trigger -->
<g transform="translate(150, 140)">
<rect fill="#121526" height="100" rx="4" stroke="#94a3b8" stroke-width="1.5" width="230" x="-115" y="-50"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">1. INITIATING EVENT</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Roadmap calendar shows 17 days</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">elapsed; engineer possesses</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">only 4 hours study per week</text>
<rect fill="#1e293b" height="16" rx="2" width="140" x="-70" y="24"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[CALENDAR TRACKING]</text>
</g>

<!-- Arrow 1 -> 2 -->
<line marker-end="url(#d1-case-2-arr-fail)" stroke="#f43f5e" stroke-dasharray="6,4" stroke-width="2.5" x1="270" x2="350" y1="140" y2="140"></line>
<text fill="#f43f5e" font-family="monospace" font-size="8" text-anchor="middle" x="310" y="132">TRIGGERS</text>

<!-- Node 2: Root Cause Defect -->
<g transform="translate(480, 140)">
<rect fill="#2a0a10" height="100" rx="4" stroke="#f43f5e" stroke-width="2" width="240" x="-120" y="-50"></rect>
<circle cx="-100" cy="-34" fill="#f43f5e" r="8"></circle>
<text fill="white" font-family="monospace" font-size="8" font-weight="bold" text-anchor="middle" x="-100" y="-31">FI</text>
<text fill="#f43f5e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="10" y="-30">2. ROOT CAUSE DEFECT</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Readiness inferred from dates;</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">prerequisite exercises skipped;</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">"familiar" rated as competence</text>
<rect fill="#3b0d18" height="16" rx="2" width="140" x="-70" y="24"></rect>
<text fill="#fda4af" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[UNVERIFIED SKILL]</text>
</g>

<!-- Arrow 2 -> 3 -->
<line marker-end="url(#d1-case-2-arr-fail)" stroke="#f43f5e" stroke-dasharray="6,4" stroke-width="2.5" x1="605" x2="685" y1="140" y2="140"></line>
<text fill="#f43f5e" font-family="monospace" font-size="8" text-anchor="middle" x="645" y="132">CASCADES</text>

<!-- Node 3: Impact -->
<g transform="translate(820, 140)">
<rect fill="#380914" height="100" rx="4" stroke="#f43f5e" stroke-width="2" width="250" x="-125" y="-50"></rect>
<text fill="#f43f5e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">3. IMPACT &amp; DEGRADATION</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Assigned to VPC migration;</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">fails to diagnose route drop;</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">migration cutover slips 2 weeks</text>
<rect fill="#4c0519" height="16" rx="2" width="150" x="-75" y="24"></rect>
<text fill="#fda4af" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[CASCADE FAILURE]</text>
</g>

<!-- LOWER LANE: CORRECTED PATH -->
<rect fill="#061f15" height="175" rx="6" stroke="#065f46" stroke-width="1.5" width="990" x="15" y="230"></rect>
<rect fill="#064e3b" height="20" rx="3" stroke="#22c55e" stroke-width="1" width="230" x="25" y="238"></rect>
<text fill="#22c55e" font-family="monospace" font-size="9" font-weight="bold" text-anchor="middle" x="140" y="252">CORRECTED PATH · ENFORCED CONTROL</text>

<!-- Node 1: Same Trigger -->
<g transform="translate(150, 326)">
<rect fill="#121526" height="100" rx="4" stroke="#94a3b8" stroke-width="1.5" width="230" x="-115" y="-50"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">1. SAME TRIGGER EVENT</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Roadmap calendar shows 17 days</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">elapsed; engineer possesses</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">only 4 hours study per week</text>
<rect fill="#1e293b" height="16" rx="2" width="140" x="-70" y="24"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[IDENTICAL CAPACITY]</text>
</g>

<!-- Arrow 1 -> 2 -->
<line marker-end="url(#d1-case-2-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="270" x2="350" y1="326" y2="326"></line>
<text fill="#22c55e" font-family="monospace" font-size="8" text-anchor="middle" x="310" y="318">INTERCEPT</text>

<!-- Invariant boundary enclosing Card 2 and 3 -->
<rect fill="none" height="150" rx="6" stroke="#f59e0b" stroke-dasharray="5,3" stroke-width="1.5" width="645" x="345" y="244"></rect>
<text fill="#f59e0b" font-family="monospace" font-size="9" font-weight="bold" text-anchor="middle" x="668" y="256">INVARIANT VERIFICATION BOUNDARY: GUARDRAIL ENFORCED</text>

<!-- Node 2: Defensive Control -->
<g transform="translate(480, 326)">
<rect fill="#064e3b" height="100" rx="4" stroke="#22c55e" stroke-width="2" width="240" x="-120" y="-50"></rect>
<text fill="#22c55e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">2. DEFENSIVE CONTROL</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Model calendar pace via formula;</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">gate advancement on committed</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">exit artifacts; log skill proof</text>
<rect fill="#022c22" height="16" rx="2" width="150" x="-75" y="24"></rect>
<text fill="#6ee7b7" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[CAPACITY-GATED MODEL]</text>
</g>

<!-- Arrow 2 -> 3 -->
<line marker-end="url(#d1-case-2-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="605" x2="685" y1="326" y2="326"></line>
<text fill="#22c55e" font-family="monospace" font-size="8" text-anchor="middle" x="645" y="318">PRESERVES</text>

<!-- Node 3: Outcome -->
<g transform="translate(820, 326)">
<rect fill="#022c22" height="100" rx="4" stroke="#22c55e" stroke-width="2" width="250" x="-125" y="-50"></rect>
<text fill="#22c55e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">3. VERIFIED OUTCOME</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Gaps identified &amp; remediated;</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">competence demonstrated;</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">cutover executes smoothly</text>
<rect fill="#064e3b" height="16" rx="2" width="150" x="-75" y="24"></rect>
<text fill="#6ee7b7" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[PREDICTABLE EXECUTION]</text>
</g>

<!-- Legend Bar -->
<rect fill="#0f172a" height="32" rx="4" stroke="#1e293b" stroke-width="1" width="990" x="15" y="414"></rect>
<line stroke="#22c55e" stroke-width="2.5" x1="28" x2="60" y1="430" y2="430"></line>
<text fill="#22c55e" font-family="monospace" font-size="10" x="66" y="434">CORRECTED PATH</text>
<line stroke="#f43f5e" stroke-dasharray="4,3" stroke-width="2" x1="200" x2="232" y1="430" y2="430"></line>
<text fill="#f43f5e" font-family="monospace" font-size="10" x="238" y="434">FAILED PATH</text>
<rect fill="none" height="12" stroke="#f59e0b" stroke-dasharray="4,2" stroke-width="1.5" width="12" x="360" y="424"></rect>
<text fill="#f59e0b" font-family="monospace" font-size="10" x="380" y="434">VERIFICATION BOUNDARY</text>
<circle cx="560" cy="430" fill="#f43f5e" r="5"></circle>
<text fill="#f43f5e" font-family="monospace" font-size="10" x="572" y="434">FI = Fault Injection Point</text>
</svg></div>
<figcaption><strong>Supplied facts:</strong> The 180-day curriculum covers an estimated 485.5 to 665.0 hours of study; the operator had 4 available weekly study hours; foundational networking and Linux units were marked complete based on elapsed calendar dates without committed artifacts.<br/><strong>Architectural inference:</strong> Pacing is governed by hours available divided by content volume, not elapsed calendar days; treating conceptual familiarity as demonstrated capability bypasses essential feedback loops and leads to operational failure in subsequent architectural layers.<br/><strong>Expected post-fix behavior:</strong> Weekly hours are modeled explicitly (estimating 121.4 to 166.2 weeks at 4 hrs/wk), skills are rated Demonstrated only with committed artifact proof, and remediation blocks are scheduled before starting dependent curriculum days.</figcaption>
</figure>'''

def get_incident_svg_3():
    return '''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg aria-labelledby="d1-case-3-title d1-case-3-desc" height="auto" role="img" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;" viewbox="0 0 1020 455" width="100%">
<title id="d1-case-3-title">Case 3 · PII leakage and runaway spend vs synthetic data and cleanup governance</title>
<desc id="d1-case-3-desc">Dual-lane incident diagram comparing an unmitigated sandbox test using real customer data and unmonitored resources against an enforced governance charter requiring synthetic data, stable replay keys, and owned teardown.</desc>
<defs>
<marker id="d1-case-3-arr-ok" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#22c55e" points="0 0, 8 4, 0 8"></polygon></marker>
<marker id="d1-case-3-arr-fail" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#f43f5e" points="0 0, 8 4, 0 8"></polygon></marker>
<marker id="d1-case-3-arr-warn" markerheight="8" markerwidth="8" orient="auto" refx="7" refy="4"><polygon fill="#f59e0b" points="0 0, 8 4, 0 8"></polygon></marker>
</defs>
<!-- Header Bar -->
<rect fill="#1e293b" height="26" opacity="0.8" rx="4" width="990" x="15" y="10"></rect>
<text fill="#cbd5e1" font-family="monospace" font-size="11" font-weight="bold" x="25" y="27">INCIDENT COMPARISON: Synthetic data, budget and cleanup ownership · Sandbox governance</text>

<!-- UPPER LANE: FAILED PATH -->
<rect fill="#180b12" height="175" rx="6" stroke="#881337" stroke-width="1.5" width="990" x="15" y="44"></rect>
<rect fill="#2d0b13" height="20" rx="3" stroke="#f43f5e" stroke-width="1" width="220" x="25" y="52"></rect>
<text fill="#f43f5e" font-family="monospace" font-size="9" font-weight="bold" text-anchor="middle" x="135" y="66">FAILED PATH · UNMITIGATED CASCADE</text>

<!-- Node 1: Trigger -->
<g transform="translate(150, 140)">
<rect fill="#121526" height="100" rx="4" stroke="#94a3b8" stroke-width="1.5" width="230" x="-115" y="-50"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">1. INITIATING EVENT</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Test lab imports customer DB export;</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">sets $50 billing budget alert;</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">spins up high-memory VMs</text>
<rect fill="#1e293b" height="16" rx="2" width="140" x="-70" y="24"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[UNSAFE INGESTION]</text>
</g>

<!-- Arrow 1 -> 2 -->
<line marker-end="url(#d1-case-3-arr-fail)" stroke="#f43f5e" stroke-dasharray="6,4" stroke-width="2.5" x1="270" x2="350" y1="140" y2="140"></line>
<text fill="#f43f5e" font-family="monospace" font-size="8" text-anchor="middle" x="310" y="132">TRIGGERS</text>

<!-- Node 2: Root Cause Defect -->
<g transform="translate(480, 140)">
<rect fill="#2a0a10" height="100" rx="4" stroke="#f43f5e" stroke-width="2" width="240" x="-120" y="-50"></rect>
<circle cx="-100" cy="-34" fill="#f43f5e" r="8"></circle>
<text fill="white" font-family="monospace" font-size="8" font-weight="bold" text-anchor="middle" x="-100" y="-31">FI</text>
<text fill="#f43f5e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="10" y="-30">2. ROOT CAUSE DEFECT</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Budget alert assumed to stop VMs;</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">no cleanup owner; non-idempotent</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">consumer fulfills replay twice</text>
<rect fill="#3b0d18" height="16" rx="2" width="140" x="-70" y="24"></rect>
<text fill="#fda4af" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[MISSING CONTROLS]</text>
</g>

<!-- Arrow 2 -> 3 -->
<line marker-end="url(#d1-case-3-arr-fail)" stroke="#f43f5e" stroke-dasharray="6,4" stroke-width="2.5" x1="605" x2="685" y1="140" y2="140"></line>
<text fill="#f43f5e" font-family="monospace" font-size="8" text-anchor="middle" x="645" y="132">CASCADES</text>

<!-- Node 3: Impact -->
<g transform="translate(820, 140)">
<rect fill="#380914" height="100" rx="4" stroke="#f43f5e" stroke-width="2" width="250" x="-125" y="-50"></rect>
<text fill="#f43f5e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">3. IMPACT &amp; DEGRADATION</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Real PII leaked in open bucket;</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">$1,400 weekend spend overrun;</text>
<text fill="#fda4af" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">duplicate orders charged</text>
<rect fill="#4c0519" height="16" rx="2" width="150" x="-75" y="24"></rect>
<text fill="#fda4af" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[BREACH &amp; FINANCIAL LOSS]</text>
</g>

<!-- LOWER LANE: CORRECTED PATH -->
<rect fill="#061f15" height="175" rx="6" stroke="#065f46" stroke-width="1.5" width="990" x="15" y="230"></rect>
<rect fill="#064e3b" height="20" rx="3" stroke="#22c55e" stroke-width="1" width="230" x="25" y="238"></rect>
<text fill="#22c55e" font-family="monospace" font-size="9" font-weight="bold" text-anchor="middle" x="140" y="252">CORRECTED PATH · ENFORCED CONTROL</text>

<!-- Node 1: Same Trigger -->
<g transform="translate(150, 326)">
<rect fill="#121526" height="100" rx="4" stroke="#94a3b8" stroke-width="1.5" width="230" x="-115" y="-50"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">1. SAME TRIGGER EVENT</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Test lab imports customer DB export;</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">sets $50 billing budget alert;</text>
<text fill="#cbd5e1" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">spins up high-memory VMs</text>
<rect fill="#1e293b" height="16" rx="2" width="140" x="-70" y="24"></rect>
<text fill="#94a3b8" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[IDENTICAL REQUIREMENT]</text>
</g>

<!-- Arrow 1 -> 2 -->
<line marker-end="url(#d1-case-3-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="270" x2="350" y1="326" y2="326"></line>
<text fill="#22c55e" font-family="monospace" font-size="8" text-anchor="middle" x="310" y="318">INTERCEPT</text>

<!-- Invariant boundary enclosing Card 2 and 3 -->
<rect fill="none" height="150" rx="6" stroke="#f59e0b" stroke-dasharray="5,3" stroke-width="1.5" width="645" x="345" y="244"></rect>
<text fill="#f59e0b" font-family="monospace" font-size="9" font-weight="bold" text-anchor="middle" x="668" y="256">INVARIANT VERIFICATION BOUNDARY: GUARDRAIL ENFORCED</text>

<!-- Node 2: Defensive Control -->
<g transform="translate(480, 326)">
<rect fill="#064e3b" height="100" rx="4" stroke="#22c55e" stroke-width="2" width="240" x="-120" y="-50"></rect>
<text fill="#22c55e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">2. DEFENSIVE CONTROL</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Mandate synthetic JSON fixtures;</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">assign named cleanup owner;</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">enforce 1 fulfillment per order</text>
<rect fill="#022c22" height="16" rx="2" width="150" x="-75" y="24"></rect>
<text fill="#6ee7b7" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[GOVERNANCE CHARTER]</text>
</g>

<!-- Arrow 2 -> 3 -->
<line marker-end="url(#d1-case-3-arr-ok)" stroke="#22c55e" stroke-width="2.5" x1="605" x2="685" y1="326" y2="326"></line>
<text fill="#22c55e" font-family="monospace" font-size="8" text-anchor="middle" x="645" y="318">PRESERVES</text>

<!-- Node 3: Outcome -->
<g transform="translate(820, 326)">
<rect fill="#022c22" height="100" rx="4" stroke="#22c55e" stroke-width="2" width="250" x="-125" y="-50"></rect>
<text fill="#22c55e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" x="0" y="-30">3. VERIFIED OUTCOME</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="-6">Zero customer PII exposed;</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="10">teardown checklist verified;</text>
<text fill="#6ee7b7" font-family="monospace" font-size="11" text-anchor="middle" x="0" y="26">replay deduplicated cleanly</text>
<rect fill="#064e3b" height="16" rx="2" width="150" x="-75" y="24"></rect>
<text fill="#6ee7b7" font-family="monospace" font-size="8" text-anchor="middle" x="0" y="36">[SAFE &amp; BOUNDED LAB]</text>
</g>

<!-- Legend Bar -->
<rect fill="#0f172a" height="32" rx="4" stroke="#1e293b" stroke-width="1" width="990" x="15" y="414"></rect>
<line stroke="#22c55e" stroke-width="2.5" x1="28" x2="60" y1="430" y2="430"></line>
<text fill="#22c55e" font-family="monospace" font-size="10" x="66" y="434">CORRECTED PATH</text>
<line stroke="#f43f5e" stroke-dasharray="4,3" stroke-width="2" x1="200" x2="232" y1="430" y2="430"></line>
<text fill="#f43f5e" font-family="monospace" font-size="10" x="238" y="434">FAILED PATH</text>
<rect fill="none" height="12" stroke="#f59e0b" stroke-dasharray="4,2" stroke-width="1.5" width="12" x="360" y="424"></rect>
<text fill="#f59e0b" font-family="monospace" font-size="10" x="380" y="434">VERIFICATION BOUNDARY</text>
<circle cx="560" cy="430" fill="#f43f5e" r="5"></circle>
<text fill="#f43f5e" font-family="monospace" font-size="10" x="572" y="434">FI = Fault Injection Point</text>
</svg></div>
<figcaption><strong>Supplied facts:</strong> A training lab utilized a 50,000-record real order export with customer PII; a $50 Cloud Billing budget alert was set; high-capacity compute instances ran over a weekend; event consumer re-processed events on failure.<br/><strong>Architectural inference:</strong> Cloud Billing budgets are strictly alert mechanisms and do not terminate compute or storage by default; un-scrubbed datasets in disposable projects violate compliance boundaries; and streaming consumers without deduplication state trigger duplicate fulfillments.<br/><strong>Expected post-fix behavior:</strong> Exercises use synthetic JSON fixtures with synthetic identifiers only; every lab has a named human owner and reverse-dependency deletion checklist; and consumers enforce an idempotent check preserving exactly one business fulfillment per order.</figcaption>
</figure>'''
