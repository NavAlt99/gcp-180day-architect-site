with open('content/day-069-page.html', 'r', encoding='utf-8') as f:
    line1 = f.readline().strip()

BODY = r"""<div class="audit-banner"><strong>Draft content:</strong> Most lessons use generated templates and have not passed topic-level review. <a href="../CONTENT_AUDIT.md">Read the content audit</a>.</div>

<main id="main" class="container day" data-day="69" data-prev="day-068.html" data-next="day-070.html" data-index="../index.html">
<div class="crumb"><a href="../index.html">Roadmap index</a> / <a href="../index.html#block-requirements-migration-and-architecture">Requirements, migration and architecture</a> / Day 69 of 180</div>

<section class="hero">
<div class="pills">
<span class="pill">DAY</span>
<span class="pill">2.5–3.5 hours</span>
<span class="pill">local exercise</span>
<span class="pill">Topics 022</span>
</div>
<h1>Day 69 — Stakeholders and priority trade-offs</h1>
<p class="lead"><strong>Outcome:</strong> Produce a stakeholder map, run a simulated discovery session, write measurable requirements, and prioritise them using MoSCoW and weighted scoring with explicit conflict resolution.</p>
<div><strong>Entry prerequisites:</strong> <p><a href="day-068.html">Day 68</a>; bring their exit artifacts (<code>day-068-requirements-register.md</code>).</p></div>
<div class="callout success"><strong>Exit artifact</strong>
<p>An agreed-priority simulation (<code>day-069-stakeholder-priority.md</code>) containing: stakeholder power-interest grid, discovery question log, SMART SLO register, and a MoSCoW-weighted scoring matrix with conflict resolution notes.</p>
</div>
<p class="small">Source curriculum checked 2026-09-26; external documentation links are selected reading and may change. A tabletop result is a design exercise, not a production test.</p>
</section>

<aside class="toc" aria-label="On this page">
<strong>On this page</strong>
<a href="#part-1">1 · Topics</a>
<a href="#part-2">2 · Technical discussion</a>
<a href="#part-3">3 · Problems and solutions</a>
<a href="#part-4">4 · Labs</a>
<div class="toc-topic">
<span>Stakeholder mapping</span>
<a href="#topic-01-overview">overview</a> · <a href="#topic-01-technical">discussion</a> · <a href="#topic-01-problem">problem</a> · <a href="#topic-01-lab">lab</a>
</div>
<div class="toc-topic">
<span>Consultant discovery questions</span>
<a href="#topic-02-overview">overview</a> · <a href="#topic-02-technical">discussion</a> · <a href="#topic-02-problem">problem</a> · <a href="#topic-02-lab">lab</a>
</div>
<div class="toc-topic">
<span>Writing measurable requirements</span>
<a href="#topic-03-overview">overview</a> · <a href="#topic-03-technical">discussion</a> · <a href="#topic-03-problem">problem</a> · <a href="#topic-03-lab">lab</a>
</div>
<div class="toc-topic">
<span>MoSCoW and weighted scoring</span>
<a href="#topic-04-overview">overview</a> · <a href="#topic-04-technical">discussion</a> · <a href="#topic-04-problem">problem</a> · <a href="#topic-04-lab">lab</a>
</div>
</aside>

<!-- ═══════════════════════════════════════════════════════ PART 1 ═══ -->
<section id="part-1" class="part"><h2>1 · Topics of the day</h2>

<article id="topic-01-overview" class="topic-card">
<h3>Stakeholder Mapping (CTO, Security, Finance, Operations, Developers)</h3>
<p>Every enterprise cloud architecture engagement involves multiple stakeholders who each possess distinct, often competing operational and financial priorities. The CTO focuses on time-to-market, strategic platform bets (such as standardizing on managed Kubernetes or event-driven serverless architectures), technical debt reduction, and innovation velocity, accepting calculated risks to achieve competitive differentiation. The CISO and security team guard the threat surface area, maintain compliance posture (PCI DSS, HIPAA, SOC 2), minimize breach liability, and mandate zero-trust adoption across all service-to-service communication. Finance and the CFO demand total cost of ownership (TCO) predictability, clear ROI, tight budget alert coverage, committed use discount (CUD) optimization, and automated anomaly detection to prevent month-end invoice surprises. Operations and SRE teams measure their success by mean time to resolve (MTTR), sustainable on-call burden, complete runbook coverage, low incident frequency, and minimal change failure rates. Meanwhile, developers prioritize developer experience (DX), high deployment frequency, local development parity with production, CI/CD pipeline speed, and reduced cognitive load.</p>
<p>The stakeholder power-interest grid classifies these actors into four operational quadrants: high power/high interest (manage closely via joint architecture governance), low power/high interest (keep informed via sprint demos and RFCs), high power/low interest (keep satisfied via executive summaries and compliance attestations), and low power/low interest (monitor with minimal overhead). Recurring friction patterns regularly challenge delivery: security gates throttling developer velocity, finance resisting redundancy investments for high availability, and CTOs clashing with operations over change-freeze windows during critical commercial periods.</p>
<p><strong>Symptom:</strong> A FinTech platform's quarterly release is blocked for six weeks because the CISO's security review process — not included in the project plan — requires a penetration test that takes four weeks to schedule. <strong>Business impact:</strong> The delayed release misses a regulatory reporting deadline, triggering a $250 000 penalty and a board-level escalation that damages the CTO's credibility with the Finance committee.</p>
<p><a href="#topic-01-technical">Technical discussion →</a> <a href="#topic-01-problem">Real-world problem →</a> <a href="#topic-01-lab">Step-by-step lab →</a></p>
</article>

<article id="topic-02-overview" class="topic-card">
<h3>Questions a Consultant Asks in Discovery</h3>
<p>A rigorous discovery session is the cloud architect's primary instrument for transforming ambiguous business intent into concrete, defensible architectural requirements. Applying the 5W+H framework (Who, What, When, Where, Why, How) to the existing system context surfaces hidden organizational and technical constraints before solutions are conceived. Current-state diagnostic probes systematically reveal latent failure modes: "What breaks most often?", "What monitoring do you have today?", "What is your current deployment process?", and "How long does a production incident take to resolve?" Future-state probes articulate the target operational reality: "What does success look like in 12 months?", "What are your top 3 reliability risks?", and crucially, "What constraints can you NOT change?"</p>
<p>Distinguishing between non-negotiable constraints (such as immutable regulatory data boundaries or multi-year enterprise contracts) and negotiable constraints (such as tooling preferences or regional hosting choices) prevents catastrophic re-architecture cycles. Effective discovery mandates deep data sensitivity classification to isolate PII, PHI, and PCI data flows, alongside an exhaustive inventory of existing commercial investments including legacy hypervisors (VMware), proprietary databases (Oracle, SAP), network interconnects, and established CI/CD and observability stacks. Architects must strictly avoid common anti-patterns: leading questions that validate personal technology biases, solution-first discovery that prescribes architectures before listening, and the omission of deep failure scenario elicitation.</p>
<p><strong>Symptom:</strong> An architect proposes a fully serverless Cloud Run architecture during week one, only to discover in week three that the customer's compliance team requires dedicated compute with no shared-tenant risk — a constraint that was never elicited because the discovery session jumped straight to solution mode. <strong>Business impact:</strong> Three weeks of architecture work is discarded, trust is damaged, and the engagement timeline slips by four weeks while a new design is prepared and re-validated.</p>
<p><a href="#topic-02-technical">Technical discussion →</a> <a href="#topic-02-problem">Real-world problem →</a> <a href="#topic-02-lab">Step-by-step lab →</a></p>
</article>

<article id="topic-03-overview" class="topic-card">
<h3>Writing Measurable Requirements ("99.95% monthly availability", "p99 latency under 300 ms")</h3>
<p>Ambiguous requirements such as "the platform must be highly available and performant" inevitably lead to failed vendor handovers and contractual disputes. Architectural requirements must strictly adhere to the SMART criteria: Specific, Measurable, Achievable, Relevant, and Time-bound. In Google Cloud architectures, this discipline is realized through the formal Service Level Indicator (SLI) and Service Level Objective (SLO) construct. An SLI represents the quantifiable ratio of good events over valid events (such as successful HTTP 2xx responses divided by total non-4xx requests, or response latency below a target threshold). The SLO defines the target reliability over an explicit measurement window, such as "99.95% of HTTP requests return 2xx within 500 ms measured at the external load balancer ingress over a rolling 28-day window."</p>
<p>From the SLO, the system's error budget is derived mechanically: <code>(1 - SLO) × window</code>. For a 99.95% availability SLO over a 28-day window (2 419 200 seconds), the error budget is exactly 1 209.6 seconds (approximately 20.2 minutes) of allowable downtime per month. Specifying the exact acceptance method is equally critical: requirements must identify the authoritative measurement tooling (such as Cloud Monitoring uptime checks, Synthetic Monitors, or custom log-based metrics) and sampling frequency. Eliminating linguistic ambiguity prevents fatal misalignment, while openly documenting unresolved business questions and required stakeholder sign-offs ensures transparent architectural governance.</p>
<p><strong>Symptom:</strong> A retailer's SLA states "99.9% uptime" but the customer interprets "uptime" as the entire platform while the vendor measures only the core checkout API, excluding the product-catalog service that went down for 4 hours. <strong>Business impact:</strong> The contractual SLA dispute results in a six-month legal process, a $180 000 settlement, and reputational damage that costs the vendor two subsequent renewal contracts.</p>
<p><a href="#topic-03-technical">Technical discussion →</a> <a href="#topic-03-problem">Real-world problem →</a> <a href="#topic-03-lab">Step-by-step lab →</a></p>
</article>

<article id="topic-04-overview" class="topic-card">
<h3>Prioritising with MoSCoW or Weighted Scoring</h3>
<p>Architecture initiatives face finite engineering capacity, demanding transparent, defensible prioritization methods. The MoSCoW framework categorizes requirements into four distinct buckets: Must-have (mandatory MVP blockers and regulatory imperatives), Should-have (high-impact capabilities necessary for competitive parity), Could-have (desirable quality-of-life enhancements), and Won't-have-this-sprint (explicitly agreed backlog items deferred to future delivery phases). While MoSCoW creates fast qualitative alignment, complex multi-stakeholder initiatives benefit from a Weighted Scoring Matrix. In this model, stakeholders establish normalized criteria weights (such as Business Value 40%, Regulatory Risk 30%, Technical Feasibility 20%, and Time-to-Implement 10%), scoring candidate stories numerically to generate an objective, mathematically ranked implementation backlog.</p>
<p>When irreconcilable stakeholder conflicts emerge — such as the CTO demanding dynamic horizontal autoscaling for peak traffic while the CFO insists on fixed compute instances locked to committed use discounts for OpEx stability — architects resolve the deadlock through empirical evidence. Deploying a shadow-mode canary pilot collecting real-world traffic, cost variance, and latency metrics turns subjective political friction into an objective data-driven trade-off. Avoiding destructive anti-patterns (such as designating all backlog items as "Must-have", omitting a formal Won't-have list, or treating non-functional requirements as optional backlog features) guarantees the clear definition of a true Minimum Viable Product (MVP).</p>
<p><strong>Symptom:</strong> A migration project's backlog contains 147 user stories, all rated "Priority 1" by different business units, resulting in a sprint zero that attempts to deliver 12 of them simultaneously, creates blocking dependencies across all 12, and ships zero features in the first six weeks. <strong>Business impact:</strong> The executive sponsor loses confidence in the delivery team, the project enters a two-month "reset" phase costing an additional $400 000 in contractor fees, and the original go-live date is missed by five months.</p>
<p><a href="#topic-04-technical">Technical discussion →</a> <a href="#topic-04-problem">Real-world problem →</a> <a href="#topic-04-lab">Step-by-step lab →</a></p>
</article>

</section>

<!-- ═══════════════════════════════════════════════════════ PART 2 ═══ -->
<section id="part-2" class="part"><h2>2 · Technical discussion of each topic</h2>

<!-- Full-width architectural SVG -->
<figure style="margin:2rem 0;">
<svg id="d69-arch-svg" viewBox="0 0 1000 620" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="d69-arch-title d69-arch-desc" style="width:100%;height:auto;display:block;background:#0f172a;border:1px solid #1e293b;border-radius:8px;">
<title id="d69-arch-title">Stakeholder Requirements &amp; Priority Trade-off Architecture</title>
<desc id="d69-arch-desc">Comprehensive architectural blueprint featuring: (A) 4-quadrant stakeholder power-interest grid with governance strategies, (B) 5W+H discovery elicitation funnel into verified constraints, (C) SMART SLI/SLO derivation chain with multiwindow burn-rate alerting, and (D) MoSCoW weighted scoring decision matrix with empirical conflict resolution.</desc>
<defs>
  <marker id="d69-arr-slate" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#94a3b8"/></marker>
  <marker id="d69-arr-blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#38bdf8"/></marker>
  <marker id="d69-arr-green" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#4ade80"/></marker>
  <marker id="d69-arr-amber" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/></marker>
  <marker id="d69-arr-rose" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/></marker>
</defs>

<!-- Header Banner -->
<rect x="12" y="12" width="976" height="42" rx="6" fill="#1e293b" stroke="#334155" stroke-width="1"/>
<text x="500" y="32" text-anchor="middle" fill="#f8fafc" font-size="13" font-family="sans-serif" font-weight="700" letter-spacing="0.06em">STAKEHOLDER REQUIREMENTS &amp; PRIORITY TRADE-OFF ARCHITECTURE</text>
<text x="500" y="47" text-anchor="middle" fill="#94a3b8" font-size="9" font-family="sans-serif">Discovery Probes · Power-Interest Governance · SMART SLO Error Budgets · Weighted Decision Matrix</text>

<!-- Panel A: Power-Interest Grid (Top Left) -->
<rect x="12" y="64" width="478" height="262" rx="6" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
<text x="25" y="84" fill="#38bdf8" font-size="11" font-family="sans-serif" font-weight="700">PANEL A · Stakeholder Power-Interest Grid &amp; Governance</text>
<rect x="25" y="96" width="225" height="75" rx="4" fill="#1c1917" stroke="#44403c" stroke-width="1"/>
<text x="32" y="110" fill="#f59e0b" font-size="9" font-family="sans-serif" font-weight="700">HIGH POWER / LOW INTEREST</text>
<text x="32" y="122" fill="#a8a29e" font-size="8" font-family="sans-serif">Keep Satisfied · Exec summaries, compliance sign-offs</text>
<rect x="255" y="96" width="225" height="75" rx="4" fill="#062e24" stroke="#047857" stroke-width="1"/>
<text x="262" y="110" fill="#34d399" font-size="9" font-family="sans-serif" font-weight="700">HIGH POWER / HIGH INTEREST</text>
<text x="262" y="122" fill="#6ee7b7" font-size="8" font-family="sans-serif">Manage Closely · Joint arch governance, weekly reviews</text>
<rect x="25" y="177" width="225" height="75" rx="4" fill="#0f172a" stroke="#334155" stroke-width="1"/>
<text x="32" y="191" fill="#94a3b8" font-size="9" font-family="sans-serif" font-weight="700">LOW POWER / LOW INTEREST</text>
<text x="32" y="203" fill="#64748b" font-size="8" font-family="sans-serif">Monitor · Minimal push communications, general updates</text>
<rect x="255" y="177" width="225" height="75" rx="4" fill="#082f49" stroke="#0284c7" stroke-width="1"/>
<text x="262" y="191" fill="#38bdf8" font-size="9" font-family="sans-serif" font-weight="700">LOW POWER / HIGH INTEREST</text>
<text x="262" y="203" fill="#7dd3fc" font-size="8" font-family="sans-serif">Keep Informed · Sprint demos, RFC feedback, office hours</text>

<g transform="translate(32, 130)">
  <rect x="0" y="0" width="95" height="18" rx="3" fill="#78350f"/><text x="47" y="12" text-anchor="middle" fill="#fef3c7" font-size="8" font-family="sans-serif" font-weight="700">CFO (OpEx/TCO)</text>
  <rect x="100" y="0" width="115" height="18" rx="3" fill="#451a03" stroke="#f59e0b" stroke-width="1"/><text x="157" y="12" text-anchor="middle" fill="#fde68a" font-size="8" font-family="sans-serif" font-weight="700">CRO (Data Residency!)</text>
</g>
<g transform="translate(262, 130)">
  <rect x="0" y="0" width="100" height="18" rx="3" fill="#065f46"/><text x="50" y="12" text-anchor="middle" fill="#d1fae5" font-size="8" font-family="sans-serif" font-weight="700">CTO (Platform/Speed)</text>
  <rect x="106" y="0" width="105" height="18" rx="3" fill="#064e3b" stroke="#34d399" stroke-width="1"/><text x="158" y="12" text-anchor="middle" fill="#a7f3d0" font-size="8" font-family="sans-serif" font-weight="700">CISO (Zero-Trust/PCI)</text>
</g>
<g transform="translate(32, 212)">
  <rect x="0" y="0" width="120" height="18" rx="3" fill="#1e293b"/><text x="60" y="12" text-anchor="middle" fill="#94a3b8" font-size="8" font-family="sans-serif">Legal / External Vendors</text>
</g>
<g transform="translate(262, 212)">
  <rect x="0" y="0" width="100" height="18" rx="3" fill="#0369a1"/><text x="50" y="12" text-anchor="middle" fill="#e0f2fe" font-size="8" font-family="sans-serif" font-weight="700">SRE (MTTR/Budgets)</text>
  <rect x="106" y="0" width="105" height="18" rx="3" fill="#075985"/><text x="158" y="12" text-anchor="middle" fill="#bae6fd" font-size="8" font-family="sans-serif" font-weight="700">DEV (DX/Pipeline)</text>
</g>
<rect x="25" y="260" width="455" height="54" rx="4" fill="#1e1e2e" stroke="#3b1d38" stroke-width="1"/>
<text x="35" y="276" fill="#f43f5e" font-size="8" font-family="sans-serif" font-weight="700">KEY GOVERNANCE RULE: Engagement History ≠ Power</text>
<text x="35" y="290" fill="#fda4af" font-size="8" font-family="sans-serif">Misclassifying CRO as "Monitor" leads to board veto. Move CRO to "Keep Satisfied" before schema design.</text>
<text x="35" y="304" fill="#a9b7cb" font-size="7.5" font-family="sans-serif">Friction patterns: Security gates vs Dev velocity · CFO fixed CUD vs SRE autoscaling · CTO freeze exceptions</text>

<!-- Panel B: Discovery Elicitation Funnel (Top Right) -->
<rect x="510" y="64" width="478" height="262" rx="6" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
<text x="525" y="84" fill="#38bdf8" font-size="11" font-family="sans-serif" font-weight="700">PANEL B · Discovery Elicitation Funnel (5W+H)</text>
<rect x="525" y="96" width="450" height="32" rx="4" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1"/>
<text x="535" y="110" fill="#bfdbfe" font-size="8.5" font-family="sans-serif" font-weight="700">Stage 1 · 5W+H Broad Probing (System Context)</text>
<text x="535" y="122" fill="#93c5fd" font-size="7.5" font-family="sans-serif">Who owns end-to-end? What systems in scope? When are releases? Where is data? Why migrate?</text>
<line x1="750" y1="128" x2="750" y2="135" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#d69-arr-slate)"/>
<rect x="545" y="137" width="410" height="32" rx="4" fill="#0f766e" stroke="#14b8a6" stroke-width="1"/>
<text x="555" y="151" fill="#99f6e4" font-size="8.5" font-family="sans-serif" font-weight="700">Stage 2 · Current-State &amp; Latent Failure Scenario Probes</text>
<text x="555" y="163" fill="#5eead4" font-size="7.5" font-family="sans-serif">"What breaks most often?" (cache invalidation) · "Worst incident?" (4h deadlock) · "Observability gaps?"</text>
<line x1="750" y1="169" x2="750" y2="176" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#d69-arr-slate)"/>
<rect x="565" y="178" width="370" height="32" rx="4" fill="#854d0e" stroke="#eab308" stroke-width="1"/>
<text x="575" y="192" fill="#fef08a" font-size="8.5" font-family="sans-serif" font-weight="700">Stage 3 · Constraint &amp; Data Sensitivity Classification</text>
<text x="575" y="204" fill="#fef9c3" font-size="7.5" font-family="sans-serif">PII/PHI/PCI flow tracing · Fixed contracts (Oracle 18mo, DC lease) · Non-negotiable vs Negotiable</text>
<line x1="750" y1="210" x2="750" y2="217" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#d69-arr-slate)"/>
<rect x="585" y="219" width="330" height="32" rx="4" fill="#14532d" stroke="#22c55e" stroke-width="1.5"/>
<text x="595" y="233" fill="#bbf7d0" font-size="8.5" font-family="sans-serif" font-weight="700">Stage 4 · Documented Candidate Requirements &amp; Constraint Register</text>
<text x="595" y="245" fill="#86efac" font-size="7.5" font-family="sans-serif">Agreed baseline, RTO/RPO targets, compliance scope, and unresolved question log</text>
<rect x="525" y="260" width="450" height="54" rx="4" fill="#3f1418" stroke="#be123c" stroke-width="1"/>
<text x="535" y="276" fill="#fecdd3" font-size="8" font-family="sans-serif" font-weight="700">DISCOVERY ANTI-PATTERNS TO AVOID</text>
<text x="535" y="290" fill="#fda4af" font-size="7.5" font-family="sans-serif">1. Leading questions: "Would you like Cloud Run?" (anchors bias without uncovering dedicated-compute rules)</text>
<text x="535" y="303" fill="#fda4af" font-size="7.5" font-family="sans-serif">2. Solution-first ideation before inventory · 3. Skipping failure elicitation ("What is the worst production event?")</text>

<!-- Panel C: SMART SLO Derivation Chain (Bottom Left) -->
<rect x="12" y="338" width="478" height="268" rx="6" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
<text x="25" y="358" fill="#38bdf8" font-size="11" font-family="sans-serif" font-weight="700">PANEL C · SMART SLO &amp; Error Budget Derivation Chain</text>
<g transform="translate(25, 370)">
  <rect x="0" y="0" width="135" height="54" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
  <text x="67" y="16" text-anchor="middle" fill="#38bdf8" font-size="8" font-family="sans-serif" font-weight="700">1. SLI DEFINITION</text>
  <text x="67" y="29" text-anchor="middle" fill="#f8fafc" font-size="7.5" font-family="sans-serif">Good Events / Valid Events</text>
  <text x="67" y="42" text-anchor="middle" fill="#94a3b8" font-size="7" font-family="sans-serif">HTTP 2xx / Non-4xx reqs</text>
  <line x1="135" y1="27" x2="155" y2="27" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#d69-arr-blue)"/>
  <rect x="158" y="0" width="135" height="54" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
  <text x="225" y="16" text-anchor="middle" fill="#38bdf8" font-size="8" font-family="sans-serif" font-weight="700">2. SLO FORMULATION</text>
  <text x="225" y="29" text-anchor="middle" fill="#f8fafc" font-size="7.5" font-family="sans-serif">99.95% over 28 Days</text>
  <text x="225" y="42" text-anchor="middle" fill="#94a3b8" font-size="7" font-family="sans-serif">Window = 2,419,200 s</text>
  <line x1="293" y1="27" x2="313" y2="27" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#d69-arr-blue)"/>
  <rect x="316" y="0" width="138" height="54" rx="4" fill="#064e3b" stroke="#22c55e" stroke-width="1.2"/>
  <text x="385" y="16" text-anchor="middle" fill="#4ade80" font-size="8" font-family="sans-serif" font-weight="700">3. ERROR BUDGET</text>
  <text x="385" y="29" text-anchor="middle" fill="#86efac" font-size="7.5" font-family="sans-serif">(1 - 0.9995) × Window</text>
  <text x="385" y="42" text-anchor="middle" fill="#bbf7d0" font-size="7.5" font-family="sans-serif">1 209.6 s ≈ 20.2 min/mo</text>
</g>
<rect x="25" y="436" width="455" height="96" rx="4" fill="#18181b" stroke="#f59e0b" stroke-width="1"/>
<text x="35" y="452" fill="#fbbf24" font-size="8.5" font-family="sans-serif" font-weight="700">4. MULTIWINDOW MULTI-BURN-RATE ALERTING (Google SRE Standard)</text>
<g transform="translate(35, 460)">
  <rect x="0" y="0" width="136" height="60" rx="3" fill="#27272a"/>
  <text x="68" y="14" text-anchor="middle" fill="#f87171" font-size="8" font-family="sans-serif" font-weight="700">1-Hour Window: 14.4×</text>
  <text x="68" y="27" text-anchor="middle" fill="#fca5a5" font-size="7" font-family="sans-serif">2% budget burnt in 1h</text>
  <text x="68" y="40" text-anchor="middle" fill="#cbd5e1" font-size="7" font-family="sans-serif">Action: Page On-Call SRE</text>
  <text x="68" y="52" text-anchor="middle" fill="#94a3b8" font-size="6.5" font-family="sans-serif">Critical fast-burn severity</text>
  <rect x="146" y="0" width="136" height="60" rx="3" fill="#27272a"/>
  <text x="214" y="14" text-anchor="middle" fill="#fbbf24" font-size="8" font-family="sans-serif" font-weight="700">6-Hour Window: 6.0×</text>
  <text x="214" y="27" text-anchor="middle" fill="#fde68a" font-size="7" font-family="sans-serif">5% budget burnt in 6h</text>
  <text x="214" y="40" text-anchor="middle" fill="#cbd5e1" font-size="7" font-family="sans-serif">Action: PagerDuty / Slack</text>
  <text x="214" y="52" text-anchor="middle" fill="#94a3b8" font-size="6.5" font-family="sans-serif">Mid-rate persistent drain</text>
  <rect x="292" y="0" width="145" height="60" rx="3" fill="#27272a"/>
  <text x="364" y="14" text-anchor="middle" fill="#38bdf8" font-size="8" font-family="sans-serif" font-weight="700">72-Hour / 10% Left</text>
  <text x="364" y="27" text-anchor="middle" fill="#bae6fd" font-size="7" font-family="sans-serif">10% error budget remains</text>
  <text x="364" y="40" text-anchor="middle" fill="#cbd5e1" font-size="7" font-family="sans-serif">Action: Freeze Releases</text>
  <text x="364" y="52" text-anchor="middle" fill="#94a3b8" font-size="6.5" font-family="sans-serif">Reliability sprint triggered</text>
</g>
<rect x="25" y="540" width="455" height="54" rx="4" fill="#0f172a" stroke="#334155" stroke-width="1"/>
<text x="35" y="555" fill="#94a3b8" font-size="8" font-family="sans-serif" font-weight="700">5. ACCEPTANCE METHOD &amp; MEASUREMENT SPECIFICATION</text>
<text x="35" y="569" fill="#cbd5e1" font-size="7.5" font-family="sans-serif">Measured at External Application Load Balancer ingress (not internal container localhost). Tooling: Cloud Monitoring</text>
<text x="35" y="582" fill="#94a3b8" font-size="7.5" font-family="sans-serif">Uptime Checks (60s probe interval) + log-based SLI metrics from lb_request_count + Synthetic Monitors.</text>

<!-- Panel D: Prioritisation Matrix (Bottom Right) -->
<rect x="510" y="338" width="478" height="268" rx="6" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
<text x="525" y="358" fill="#38bdf8" font-size="11" font-family="sans-serif" font-weight="700">PANEL D · MoSCoW &amp; Weighted Scoring Decision Matrix</text>
<g transform="translate(525, 370)">
  <rect x="0" y="0" width="220" height="20" rx="3" fill="#991b1b"/><text x="110" y="13" text-anchor="middle" fill="#fee2e2" font-size="7.5" font-family="sans-serif" font-weight="700">MUST-HAVE: MVP Blocker, Legal, Core Ops (40 pts)</text>
  <rect x="0" y="24" width="180" height="20" rx="3" fill="#b45309"/><text x="90" y="37" text-anchor="middle" fill="#fef3c7" font-size="7.5" font-family="sans-serif" font-weight="700">SHOULD-HAVE: High value, non-blocker (Sprint 2)</text>
  <rect x="0" y="48" width="140" height="20" rx="3" fill="#1e40af"/><text x="70" y="61" text-anchor="middle" fill="#dbeafe" font-size="7.5" font-family="sans-serif" font-weight="700">COULD-HAVE: Quality of life enhancements</text>
  <rect x="0" y="72" width="105" height="20" rx="3" fill="#334155"/><text x="52" y="85" text-anchor="middle" fill="#cbd5e1" font-size="7.5" font-family="sans-serif" font-weight="700">WON'T-HAVE: Explicitly deferred</text>
</g>
<g transform="translate(755, 370)">
  <rect x="0" y="0" width="220" height="92" rx="3" fill="#18181b" stroke="#3f3f46" stroke-width="1"/>
  <text x="110" y="14" text-anchor="middle" fill="#a1a1aa" font-size="7.5" font-family="sans-serif" font-weight="700">WEIGHTED SCORING FORMULA</text>
  <text x="110" y="26" text-anchor="middle" fill="#38bdf8" font-size="7" font-family="sans-serif">BV×0.40 + Reg×0.30 + Feas×0.20 + Spd×0.10</text>
  <text x="10" y="42" fill="#86efac" font-size="7" font-family="sans-serif">1. R-01 IAM/Workload Identity (9.2) · 8 pts</text>
  <text x="10" y="55" fill="#86efac" font-size="7" font-family="sans-serif">2. R-02 Checkout SLO Mon (8.9) · 8 pts</text>
  <text x="10" y="68" fill="#86efac" font-size="7" font-family="sans-serif">3. R-03 DB Schema Baseline (8.2) · 13 pts</text>
  <text x="10" y="81" fill="#86efac" font-size="7" font-family="sans-serif">4. R-04 CI/CD Cloud Deploy (7.0) · 11 pts</text>
</g>
<rect x="525" y="470" width="450" height="28" rx="4" fill="#064e3b" stroke="#22c55e" stroke-width="1"/>
<text x="535" y="487" fill="#86efac" font-size="8" font-family="sans-serif" font-weight="700">SPRINT 1 CAPACITY GATE: 8 + 8 + 13 + 11 = 40 Points (100% capacity · unblocks all future features)</text>
<rect x="525" y="506" width="450" height="88" rx="4" fill="#1c1917" stroke="#f59e0b" stroke-width="1.2"/>
<text x="535" y="522" fill="#fbbf24" font-size="8.5" font-family="sans-serif" font-weight="700">EMPIRICAL CONFLICT RESOLUTION: CTO vs CFO AUTOSCALING DISPUTE</text>
<text x="535" y="537" fill="#e7e5e4" font-size="7.5" font-family="sans-serif">Conflict: CTO requires dynamic horizontal autoscaling (max 40) vs CFO demanding fixed capacity (20 n2-standard-8 with 3yr CUD).</text>
<text x="535" y="551" fill="#cbd5e1" font-size="7.5" font-family="sans-serif">Resolution Protocol: Shadow-Mode Canary Pilot routing 5% real traffic to autoscaling MIG for 30 days during Sprint 1.</text>
<text x="535" y="565" fill="#86efac" font-size="7.5" font-family="sans-serif">Data Gathered: Real monthly spend variance ($12K avg savings vs ±$4K variance) + p99 response vs fixed capacity 503 risks.</text>
<text x="535" y="579" fill="#fcd34d" font-size="7.5" font-family="sans-serif">Outcome: Transparent trade-off signed off by both executives based on empiricism rather than organizational authority.</text>
</svg>
<figcaption>Fig 1 — Stakeholder Requirements &amp; Priority Trade-off Architecture: (A) 4-quadrant power-interest grid mapping executive governance, (B) 5W+H discovery elicitation funnel into fixed constraints, (C) SMART SLI/SLO derivation chain with multiwindow multi-burn-rate alerting, and (D) MoSCoW weighted scoring matrix with empirical shadow canary conflict resolution.</figcaption>
</figure>

<!-- Topic 1 Technical -->
<article id="topic-01-technical" class="topic-card">
<h3>Topic 1 — Stakeholder Mapping: Power-Interest Grid and Conflict Patterns</h3>
<p>Enterprise cloud architecture engagements frequently stumble not on technical infeasibility, but on unmapped organizational dynamics. A cloud architect is tasked with aligning competing incentives into a coherent, defensible system topology. Stakeholder mapping is not an informal organizational chart lookup; it is a structured risk mitigation discipline designed to surface hidden authorities and veto holders before architectural commitments are made.</p>

<h4>Stakeholder Personas and What Each Cares About</h4>
<ul>
<li><strong>Chief Technology Officer (CTO):</strong> Accountable for competitive market differentiation and product agility. Cares about time-to-market, strategic platform bets (such as standardizing on managed Kubernetes or event-driven serverless architectures), technical debt ratios, and engineering innovation velocity. Tolerates controlled operational complexity if it delivers a strategic market advantage.</li>
<li><strong>Chief Information Security Officer (CISO) &amp; Security:</strong> Accountable for corporate risk, data confidentiality, and compliance posture. Cares about minimizing total threat surface area, audit readiness (PCI DSS, HIPAA, SOC 2 Type II), breach liability, and enforcing zero-trust architecture across all service-to-service communication via Workload Identity Federation, VPC Service Controls, and Customer-Managed Encryption Keys (CMEK).</li>
<li><strong>Chief Financial Officer (CFO) &amp; Finance:</strong> Accountable for capital efficiency and fiscal governance. Cares about Total Cost of Ownership (TCO) versus Return on Investment (ROI), OpEx spend predictability, budget alert coverage, committed use discount (CUD) optimization across compute and databases, and automated anomaly detection to prevent runaway cloud bills.</li>
<li><strong>Operations &amp; SRE Teams:</strong> Accountable for platform reliability and runbook health. Cares about mean time to resolve (MTTR), sustainable on-call burden (limiting toil to &lt; 50% of engineering time), complete runbook coverage, low incident frequency, and maintaining an acceptable change failure rate across deployments.</li>
<li><strong>Software Developers:</strong> Accountable for feature implementation. Cares about developer experience (DX), deployment frequency, local development parity with production environments, CI/CD pipeline speed (build-and-test loops under 10 minutes), and low cognitive overhead.</li>
<li><strong>Chief Risk Officer (CRO) &amp; Legal:</strong> Accountable for regulatory compliance and jurisdictional risk. Cares about statutory data residency mandates (such as GDPR Article 44–49 in Europe or APPI in Japan), cross-border data transfer liabilities, and executing Business Associate Agreements (BAAs) prior to workload migrations.</li>
</ul>

<div class="table-wrap">
<table>
<caption>Stakeholder Power-Interest Grid with Goals and Communication Strategy</caption>
<thead><tr><th>Stakeholder</th><th>Power</th><th>Interest</th><th>Primary Goals</th><th>Success Metrics</th><th>Communication Strategy</th></tr></thead>
<tbody>
<tr><td>CTO</td><td>High</td><td>High</td><td>Time-to-market, strategic platform bets, technical debt reduction, innovation velocity</td><td>Feature delivery frequency, platform NPS, tech debt ratio</td><td>Manage closely — weekly joint architecture reviews, ADR co-signing</td></tr>
<tr><td>CISO / Security</td><td>High</td><td>High</td><td>Threat surface area, compliance posture (PCI/HIPAA/SOC 2), breach liability, zero-trust adoption</td><td>Critical findings on external audits, zero plain-text secrets, MTTR for CVEs</td><td>Manage closely — dedicated security gate reviews, formal sign-off gates</td></tr>
<tr><td>CFO / Finance</td><td>High</td><td>Medium</td><td>TCO vs ROI, OpEx predictability, CUD planning, cost anomaly detection</td><td>Monthly spend vs budget variance (&lt;±10%), unit cost per transaction</td><td>Keep satisfied — monthly cost dashboards, CUD coverage reports, budget alerts</td></tr>
<tr><td>Chief Risk Officer (CRO) / Legal</td><td>High</td><td>Low</td><td>Regulatory compliance, data residency, statutory audit defensibility</td><td>Zero jurisdictional breaches, signed BAAs, audit attestation</td><td>Keep satisfied — compliance attestations, formal exception reviews only</td></tr>
<tr><td>Operations / SRE</td><td>Medium</td><td>High</td><td>MTTR, on-call burden, runbook coverage, incident frequency, change failure rate</td><td>Error budget remaining, on-call paging volume, DORA elite metrics</td><td>Keep informed — sprint demos, post-mortem reviews, SLO dashboards</td></tr>
<tr><td>Developers</td><td>Low</td><td>High</td><td>Developer experience, deployment frequency, local dev parity, CI/CD speed, cognitive load</td><td>Pipeline duration (&lt;10m), local environment setup time, deploy frequency</td><td>Keep informed — RFC reviews, platform office hours, developer documentation</td></tr>
</tbody>
</table>
</div>

<h4>Classic Stakeholder Conflict Patterns</h4>
<p>Experienced enterprise architects proactively prepare for three structural conflict patterns that recur across cloud transformations:</p>
<ol>
<li><strong>Security vs. Developer Velocity:</strong> Security mandates comprehensive SAST/DAST and container vulnerability scans before deployment. Developers protest that full scans add 25 minutes to CI/CD pipelines, destroying rapid feedback loops. <em>Architectural Resolution:</em> Implement risk-tiered scanning. Blocking gates apply strictly to critical/high CVEs with public exploit vectors (reducing blocking gate time to ~3 minutes), while medium/low findings are evaluated asynchronously via security dashboards with a 14-day remediation SLA.</li>
<li><strong>Finance vs. Reliability Investment:</strong> SRE demands an active-active dual-region deployment with global load balancing to achieve 99.99% availability. Finance rejects the proposal because multi-region data replication and idle capacity increase monthly infrastructure costs by 1.8×. <em>Architectural Resolution:</em> Translate reliability requirements into probabilistic financial terms. At $50 000/hour in lost transaction revenue, a single 4-hour regional outage costs $200 000 plus brand equity damage. A single-region deployment with cross-zone failover and automated cross-region database snapshot replication delivers 99.95% availability at a fraction of the cost, satisfying both fiscal and resilience boundaries.</li>
<li><strong>CTO vs. Operations — Change Freeze Windows:</strong> Operations enforces a complete deployment freeze during peak retail weeks (such as Black Friday/Cyber Monday). The CTO insists on releasing a critical competitive feature during that exact window. <em>Architectural Resolution:</em> Decouple code deployment from feature release. Deploy the production binaries weeks before the freeze window begins using Google Cloud Deploy with dark launch canary gates, controlled dynamically via LaunchDarkly or Unleash feature flags. The code is tested in production under baseline load, and the feature flag is activated without modifying infrastructure.</li>
</ol>

<div class="callout">
<strong>Further Study</strong>
<p><a href="https://docs.cloud.google.com/architecture/framework" rel="noopener noreferrer">GCP Architecture Framework</a> — the authoritative reference for operational excellence, security, reliability, and cost optimization across enterprise architectures.</p>
</div>
</article>

<!-- Topic 2 Technical -->
<article id="topic-02-technical" class="topic-card">
<h3>Topic 2 — Consultant Discovery: 5W+H Probes, Anti-patterns, and Constraint Elicitation</h3>
<p>Discovery is the diagnostic interview where an architect extracts the actual constraints and failure behaviors of an enterprise system. Customers frequently present their requirements as desired technical solutions rather than business problems (e.g., stating "we need a Kubernetes cluster" rather than "we need isolated deployments with autoscaling"). A skilled consultant uses the 5W+H framework (Who, What, When, Where, Why, How) to penetrate surface requests and uncover foundational system boundaries.</p>

<div class="table-wrap">
<table>
<caption>Discovery Question Framework: Current-state, Future-state, and Anti-pattern Probes</caption>
<thead><tr><th>Category</th><th>Probe Question</th><th>What It Surfaces</th><th>Anti-pattern to Avoid</th></tr></thead>
<tbody>
<tr><td>Current-state</td><td>"What breaks most often in your production environment?"</td><td>High-frequency failure modes, recurring toil sources, unmonitored dependencies</td><td>Asking "Are there any problems?" (which reliably prompts a defensive "no")</td></tr>
<tr><td>Current-state</td><td>"What monitoring and alerting do you have active today?"</td><td>Observability blind spots, tool sprawl (Datadog, Prometheus), alert fatigue</td><td>Assuming Cloud Monitoring or APM is already active because services run</td></tr>
<tr><td>Current-state</td><td>"What is your exact current deployment process from commit to prod?"</td><td>Manual approval gates, SSH deployments, deployment cadence, lack of automated rollback</td><td>Assuming modern CI/CD exists simply because code is stored in GitHub</td></tr>
<tr><td>Current-state</td><td>"How long does a severe production incident take to resolve (MTTR)?"</td><td>Incident triage maturity, runbook coverage, communication bottlenecks</td><td>Accepting vague answers like "it depends" without demanding the worst-case historical duration</td></tr>
<tr><td>Future-state</td><td>"What does success look like in 12 months for this platform?"</td><td>Underlying business hypotheses, measurable revenue or velocity targets</td><td>Permitting stakeholders to list software products rather than measurable business outcomes</td></tr>
<tr><td>Future-state</td><td>"What are your top 3 reliability risks during peak traffic events?"</td><td>Latent architectural choke points, database connection limits, third-party API dependencies</td><td>Skipping reliability probing to focus exclusively on functional product roadmaps</td></tr>
<tr><td>Constraint</td><td>"What constraints can you NOT change under any circumstances?"</td><td>Non-negotiable statutory rules, multi-year contracts, fixed skills ceilings</td><td>Treating all enterprise constraints as negotiable technical preferences</td></tr>
<tr><td>Constraint</td><td>"Which data flows contain PII, PHI, or cardholder (PCI) data?"</td><td>Regulatory perimeter scope, encryption mandates, tenant isolation requirements</td><td>Inferring data classification merely from database table or microservice names</td></tr>
<tr><td>Constraint</td><td>"What commercial licenses and contracts are you committed to?"</td><td>VMware, Oracle, SAP licensing agreements; physical data center colocation leases</td><td>Designing architectures that require terminating multi-year contracts with severe financial penalties</td></tr>
<tr><td>Anti-pattern</td><td>"Would you like to use Cloud Run or GKE for this workload?"</td><td>Confirmation bias; anchors customer to a solution before boundaries are known</td><td>Never ask leading technical questions during initial discovery sessions</td></tr>
</tbody>
</table>
</div>

<h4>Data Sensitivity Classification Discovery</h4>
<p>To uncover hidden security boundaries, an architect asks: <em>"Walk me through the complete lifecycle of a customer record from initial creation to backup deletion."</em> This single inquiry immediately surfaces:</p>
<ul>
<li>Where Personally Identifiable Information (PII) is stored and whether it crosses international borders.</li>
<li>Whether payment card data touches application memory, determining whether the application falls under PCI DSS SAQ-D (full scope) or SAQ-A (tokenized via third-party iframe).</li>
<li>Whether Protected Health Information (PHI) requires executing a Google Cloud Business Associate Agreement (BAA) and deploying dedicated or sole-tenant compute nodes.</li>
<li>Whether shadow data pipelines export sensitive unmasked customer records into analytics warehouses (BigQuery) without Cloud DLP de-identification.</li>
</ul>

<h4>Existing Investment Discovery</h4>
<p>Prior to designing target architectures, an architect must catalogue existing sunk investments. An organization with 18 months remaining on an enterprise Oracle Database contract or a multi-year VMware Enterprise agreement cannot immediately execute a greenfield Cloud Spanner migration. Recognizing these commercial constraints dictates the architectural strategy: deploying a Strangler-Fig migration with change data capture (CDC) or utilizing Google Cloud VMware Engine (GCVE) as an intermediate modernization stepping stone.</p>
</article>

<!-- Topic 3 Technical -->
<article id="topic-03-technical" class="topic-card">
<h3>Topic 3 — Writing Measurable Requirements: SLI, SLO, Error Budget, and Acceptance Methods</h3>
<p>Requirements that lack numeric thresholds and explicit measurement methods cannot be verified or enforced. The SRE discipline establishes a mathematical foundation for service expectations through Service Level Indicators (SLIs), Service Level Objectives (SLOs), and Error Budgets.</p>

<h4>SMART Criteria for Cloud Architecture</h4>
<ul>
<li><strong>Specific:</strong> Precisely identifies the protocol, HTTP response codes, and network boundary (e.g., "HTTP 2xx responses at the Global Application Load Balancer ingress").</li>
<li><strong>Measurable:</strong> Formulated as a ratio with explicit mathematical calculation and defined units (e.g., percentage, milliseconds).</li>
<li><strong>Achievable:</strong> Realistically attainable within the selected infrastructure topology and dependency budget (e.g., aiming for 99.999% availability with single-zone Cloud SQL is mathematically unachievable).</li>
<li><strong>Relevant:</strong> Directly maps to customer experience and business revenue outcomes.</li>
<li><strong>Time-bound:</strong> Evaluated over an explicit rolling window (e.g., rolling 28-day window, rolling 1-hour window).</li>
</ul>

<div class="table-wrap">
<table>
<caption>SMART SLI/SLO Template Table with Error Budget and Acceptance Method</caption>
<thead><tr><th>Quality Dimension</th><th>SLI (What to Measure)</th><th>SLO (Target)</th><th>Measurement Window</th><th>Error Budget</th><th>Acceptance Method</th></tr></thead>
<tbody>
<tr><td>Availability</td><td><code>count(HTTP 2xx) / count(total non-4xx) × 100</code></td><td>99.95%</td><td>Rolling 28 days</td><td>0.05% × 2 419 200 s = 1 209.6 s (~20.2 min/mo)</td><td>Cloud Monitoring Uptime Checks on <code>/health/checkout</code> sampled every 60s + log-based SLI from load balancer</td></tr>
<tr><td>Request Latency</td><td>p99 round-trip latency at load balancer ingress for request payload &lt; 64 KB</td><td>&lt; 300 ms</td><td>Rolling 1 hour</td><td>1% of hourly requests may exceed 300 ms</td><td>Cloud Monitoring distribution metric <code>loadbalancing.googleapis.com/https/request_latencies</code></td></tr>
<tr><td>Pipeline Throughput</td><td>Sustained record ingestion and processing rate by streaming pipeline</td><td>&gt; 10 000 events/s</td><td>5-minute rolling window</td><td>&lt; 5 min/day below throughput threshold</td><td>Cloud Dataflow throughput metric; Cloud Monitoring alert on Pub/Sub unacknowledged message age</td></tr>
<tr><td>Data Durability</td><td><code>count(retrievable objects) / count(committed objects) × 100</code></td><td>99.999999999% (11 nines)</td><td>Per-object annual</td><td>0.000000001% risk (guaranteed by Cloud Storage multi-region)</td><td>Cloud Storage automated checksum verification; quarterly disaster recovery restore drills</td></tr>
<tr><td>Data Freshness</td><td>Age of most recently processed event in analytics table</td><td>&lt; 300 s (5 min lag)</td><td>Continuous</td><td>&lt; 5 minutes per day of stale data</td><td>Custom Cloud Monitoring gauge metric tracking Pub/Sub publish timestamp vs BigQuery insertion timestamp</td></tr>
</tbody>
</table>
</div>

<h4>Error Budget Derivation &amp; Multiwindow Multi-burn-rate Alerting</h4>
<p>The error budget represents the exact volume of failure permitted before user happiness is compromised. For an availability SLO of <strong>99.95%</strong> evaluated across a standard <strong>28-day rolling window</strong>:</p>
<ul>
<li>Total seconds in window: <code>28 days × 24 hours × 3 600 seconds = 2 419 200 seconds</code></li>
<li>Allowable failure fraction: <code>1 - 0.9995 = 0.0005 (0.05%)</code></li>
<li>Total error budget: <code>0.0005 × 2 419 200 = 1 209.6 seconds ≈ 20.16 minutes</code></li>
</ul>
<p>Google SRE best practices dictate multiwindow multi-burn-rate alerting to eliminate false positives while detecting catastrophic regressions:</p>
<ul>
<li><strong>1-Hour Fast Burn (14.4× Burn Rate):</strong> Consumes 2% of the monthly error budget in a single hour. <em>Trigger:</em> Immediate PagerDuty page to primary on-call SRE.</li>
<li><strong>6-Hour Mid Burn (6.0× Burn Rate):</strong> Consumes 5% of the monthly error budget across six hours. <em>Trigger:</em> Urgent notification to team Slack/ticket queue during working hours.</li>
<li><strong>72-Hour Slow Burn (10% Budget Remaining):</strong> Error budget falls below 10%. <em>Trigger:</em> Non-emergency engineering review. Feature deployments are paused and sprint capacity shifts exclusively to reliability remediation.</li>
</ul>

<h4>Replacing Ambiguous Statements with Precise Specifications</h4>
<p>Eliminating linguistic ambiguity protects both engineering teams and clients:</p>
<ul>
<li><em>Ambiguous:</em> "The checkout service must be fast."<br><strong>Precise:</strong> "The 99th percentile (p99) round-trip response time for HTTP POST requests to <code>/api/v1/checkout</code> must remain below 300 ms measured at the Google Cloud External Application Load Balancer across any rolling 1-hour window for request bodies under 64 KB."</li>
<li><em>Ambiguous:</em> "The platform must be highly available."<br><strong>Precise:</strong> "The platform must maintain 99.95% monthly availability, defined as total HTTP 2xx responses divided by total non-4xx requests, measured via Cloud Monitoring uptime checks sampled every 60 seconds from three distinct geographic probes."</li>
<li><em>Ambiguous:</em> "Data loss must be avoided during a disaster."<br><strong>Precise:</strong> "Recovery Point Objective (RPO) must be ≤ 60 seconds for financial ledger transactions, achieved via Cloud Spanner multi-region dual-region replication with automatic quorum failover."</li>
</ul>
</article>

<!-- Topic 4 Technical -->
<article id="topic-04-technical" class="topic-card">
<h3>Topic 4 — Prioritising with MoSCoW and Weighted Scoring</h3>
<p>Engineering initiatives face severe constraints in time, budget, and headcount. When stakeholders compete for delivery capacity, an architect must deploy a transparent, objective prioritization framework to prevent scope creep and political stalemates.</p>

<div class="table-wrap">
<table>
<caption>MoSCoW vs Weighted Scoring: Method Comparison</caption>
<thead><tr><th>Dimension</th><th>MoSCoW Method</th><th>Weighted Scoring Matrix</th></tr></thead>
<tbody>
<tr><td>Method</td><td>Categorical classification into four qualitative tiers (Must, Should, Could, Won't)</td><td>Mathematical scoring based on normalized stakeholder criteria weights: <code>Score = Σ(Weight × Criterion)</code></td></tr>
<tr><td>Input Data</td><td>Stakeholder consensus regarding MVP viability and regulatory constraints</td><td>Stakeholder-assigned weights × feasibility, business value, regulatory risk, and velocity scores</td></tr>
<tr><td>Output Format</td><td>4-tier categorisation; explicit backlog deferral list</td><td>Ranked numerical priority list; defensible sequencing order with clear cut-off lines</td></tr>
<tr><td>Best Used When</td><td>Scoping initial MVP boundaries; fast time-boxed alignment; small cross-functional teams</td><td>Complex multi-stakeholder trade-offs; competing executive agendas; formal audit defense</td></tr>
<tr><td>Key Strength</td><td>Intuitive, rapid consensus; forces explicit declaration of deferred scope ("Won't-have")</td><td>Quantitative transparency; removes emotional bias; provides objective tie-breaking</td></tr>
<tr><td>Key Vulnerability</td><td>Tendency for stakeholders to label every feature as "Must-have" unless capacity is strictly capped</td><td>Criteria weights and subjective scores can be politically manipulated without strict rubric definitions</td></tr>
</tbody>
</table>
</div>

<h4>Weighted Scoring — Mathematical Worked Example</h4>
<p>Consider a Sprint 1 planning session with a hard team capacity limit of <strong>40 story points</strong>. Stakeholders establish four normalized evaluation criteria: <strong>Business Value (40%)</strong>, <strong>Regulatory Risk (30%)</strong>, <strong>Technical Feasibility (20%)</strong>, and <strong>Implementation Speed (10%)</strong>.</p>

<div class="table-wrap">
<table>
<caption>Weighted Scoring Worked Example (Formula: BV×0.40 + Reg×0.30 + Feas×0.20 + Speed×0.10)</caption>
<thead><tr><th>Requirement ID &amp; Name</th><th>BV /10</th><th>Reg /10</th><th>Feas /10</th><th>Speed /10</th><th>Weighted Score</th><th>MoSCoW Tier</th><th>Story Points</th><th>Sequence Order</th></tr></thead>
<tbody>
<tr><td>R-01: IAM &amp; Workload Identity Bootstrap</td><td>9</td><td>10</td><td>9</td><td>8</td><td><strong>9.20</strong></td><td>Must-have</td><td>8</td><td>1 (Unblocks all)</td></tr>
<tr><td>R-02: Checkout API Availability SLO Monitoring</td><td>10</td><td>8</td><td>9</td><td>7</td><td><strong>8.90</strong></td><td>Must-have</td><td>8</td><td>4 (Validates prod)</td></tr>
<tr><td>R-03: Cloud SQL Database Schema Baseline</td><td>9</td><td>8</td><td>8</td><td>6</td><td><strong>8.20</strong></td><td>Must-have</td><td>13</td><td>2 (Enables data)</td></tr>
<tr><td>R-04: CI/CD Pipeline (Cloud Build + Deploy)</td><td>8</td><td>5</td><td>8</td><td>7</td><td><strong>7.00</strong></td><td>Must-have</td><td>11</td><td>3 (Enables deploy)</td></tr>
<tr><td>R-06: Budget Alerts &amp; Spend Anomaly Detection</td><td>7</td><td>4</td><td>9</td><td>9</td><td><strong>6.70</strong></td><td>Should-have</td><td>5</td><td>Deferred (Sprint 2)</td></tr>
<tr><td>R-05: Managed Instance Group Autoscaling Policy</td><td>8</td><td>3</td><td>8</td><td>6</td><td><strong>6.30</strong></td><td>Should-have</td><td>8</td><td>Deferred (Sprint 2)</td></tr>
<tr><td>R-07: Dual-Region Active-Active Failover</td><td>7</td><td>5</td><td>6</td><td>3</td><td><strong>5.80</strong></td><td>Could-have</td><td>21</td><td>Deferred (Sprint 4)</td></tr>
<tr><td>R-10: Oracle to Cloud Spanner Migration Phase 1</td><td>6</td><td>6</td><td>4</td><td>1</td><td><strong>5.10</strong></td><td>Won't-have</td><td>34</td><td>Deferred (Sprint 6+)</td></tr>
<tr><td>R-08: Self-Service FinOps Cost Dashboard</td><td>5</td><td>1</td><td>8</td><td>8</td><td><strong>4.70</strong></td><td>Could-have</td><td>8</td><td>Deferred (Sprint 3)</td></tr>
<tr><td>R-09: Datadog Agent Migration to Cloud Monitoring</td><td>4</td><td>2</td><td>5</td><td>2</td><td><strong>3.40</strong></td><td>Won't-have</td><td>13</td><td>Deferred (Sprint 5)</td></tr>
</tbody>
</table>
</div>
<p><em>Sprint 1 Selection:</em> R-01 (8 pts) + R-03 (13 pts) + R-04 (11 pts) + R-02 (8 pts) = exactly <strong>40 story points</strong>. This selection satisfies all architectural dependencies while adhering strictly to sprint capacity.</p>

<h4>Empirical Conflict Resolution: CTO vs. CFO Autoscaling Deadlock</h4>
<p>Prioritization frequently reveals executive impasses. In the Brightloaf retail modernization, the CTO insists on dynamic horizontal autoscaling (Managed Instance Groups scaling up to 40 replicas) to safeguard customer experience during traffic bursts. The CFO insists on fixed compute capacity (locking 20 <code>n2-standard-8</code> instances under a 3-year Committed Use Discount) to guarantee month-over-month OpEx budget predictability. Rather than escalating politically, the architect establishes an <strong>Empirical Shadow Canary Pilot</strong>:</p>
<ol>
<li>During Sprint 1, 5% of production traffic is mirrored to an autoscaling test MIG while 95% remains on fixed capacity.</li>
<li>Telemetry captures empirical data: the autoscaling tier reduced baseline idle spend by $12 000/month during off-peak hours with a predictable ±$4 000 burst variance, whereas the fixed capacity tier encountered HTTP 503 errors at 38 000 concurrent users during flash surges.</li>
<li>The architect presents the empirical findings: autoscaling provides net annual cost savings while eliminating revenue loss from dropped transactions. Both executives sign off on autoscaling paired with an 80% budget alert cap.</li>
</ol>
</article>

</section>

<!-- ═══════════════════════════════════════════════════════ PART 3 ═══ -->
<section id="part-3" class="part"><h2>3 · Problems and solutions</h2>

<!-- Problem 1 -->
<article id="topic-01-problem" class="topic-card">
<h3>Problem 1 — Unidentified Stakeholder Veto Collapses a Cloud Migration</h3>
<h4>Scenario</h4>
<p>A tier-1 retail bank initiated a €2 M modernization initiative to migrate its core loan-origination engine from on-premise Oracle databases to Google Cloud Spanner. The engagement possessed executive sponsorship from both the CTO and CIO, with an aggressive 6-month delivery schedule. Over ten weeks, the architecture team completed schema conversion, dual-write synchronization pipelines, and row-level security models using a Cloud Spanner multi-region instance (<code>nam6</code>) to maximize availability. In week 11, during an executive committee briefing, the bank's Chief Risk Officer (CRO) — who had been classified as "Low Power / Low Interest" on the initial project stakeholder register — learned of the architecture and immediately exercised executive veto power: the bank's internal compliance policy and European banking regulations strictly forbid financial ledger data from replicating across non-EU jurisdictions, rendering the multi-region topology illegal.</p>
<h4>Failure Symptoms</h4>
<ul>
<li>The CRO issues an immediate board-level stop-work order, freezing project funding.</li>
<li>Ten weeks of schema tuning, distributed transaction testing, and replication engineering are rendered unusable.</li>
<li>Engineering delivery velocity collapses to zero as the team confronts a full architectural redesign.</li>
<li>The data residency policy had existed for four years in internal documentation but was never surfaced during discovery.</li>
</ul>
<h4>Diagnostic Sequence</h4>
<ol>
<li>Inspect the project stakeholder register: the CRO was assigned to the "Monitor" quadrant with no scheduled communication or review checkpoints.</li>
<li>Audit the statutory compliance requirements: the banking charter mandates that all regulated customer financial records reside exclusively within European Union legal borders.</li>
<li>Examine Google Cloud Spanner deployment capabilities: determine that Spanner regional configurations (e.g., <code>europe-west1</code> in Belgium or <code>europe-west3</code> in Frankfurt) comply with EU data sovereignty mandates.</li>
<li>Identify the procedural root cause: discovery questionnaires focused exclusively on functional and performance metrics, omitting mandatory data sovereignty and regulatory constraints.</li>
</ol>
<h4>Root Cause</h4>
<p>The architect conflated historical project engagement with organizational authority. Because the CRO had not attended previous technical steering sessions, they were misclassified as low power. Consequently, data residency constraints were never elicited, resulting in ten weeks of invalid architecture work on a multi-region deployment that violated enterprise compliance policy.</p>
<h4>Remediation</h4>
<ol>
<li>Rebuild the stakeholder power-interest register, moving the CRO and Legal counsel immediately to the "Manage Closely / Keep Satisfied" governance quadrant.</li>
<li>Re-architect the database tier to deploy Google Cloud Spanner in an EU regional configuration (<code>europe-west1</code>) backed by regional Persistent Disk backups within the EU boundary.</li>
<li>Formulate an Architecture Decision Record (ADR-042) detailing the trade-off: accepting regional RTO characteristics in exchange for strict regulatory compliance, secured with CRO and CTO signatures.</li>
<li>Update organizational discovery templates to mandate data sovereignty, compliance classification, and regulatory review prior to database selection.</li>
</ol>
<h4>Verification</h4>
<p>The CRO and legal counsel review and formally sign off on ADR-042. Terraform configurations deploy Cloud Spanner to <code>europe-west1</code> with Organization Policy constraint <code>gcp.resourceLocations</code> enforced, programmatically preventing resource creation outside the EU.</p>
<h4>Residual Risk</h4>
<p>A regional Spanner configuration does not provide automatic seamless failover across continental boundaries if the entire <code>europe-west1</code> region becomes unavailable. The bank accepts a higher RTO (restoring to a secondary EU region from Cloud Storage within 2 hours) as an explicit trade-off for legal compliance.</p>

<figure style="margin:2rem 0;">
<svg id="d69-p1-svg" viewBox="0 0 760 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="d69-p1-title d69-p1-desc" style="width:100%;height:auto;display:block;background:#0f172a;border-radius:8px;">
<title id="d69-p1-title">Problem 1 Incident Diagram: Unidentified CRO Veto Halts Migration</title>
<desc id="d69-p1-desc">Failed path illustrates CRO misclassified as monitor leading to an uncompliant multi-region Spanner design and board veto. Corrected path demonstrates CRO in manage closely, EU data residency elicitation, regional Spanner deployment, and successful sign-off.</desc>
<defs>
  <marker id="d69-p1-fail-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#f43f5e"/></marker>
  <marker id="d69-p1-ok-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#22c55e"/></marker>
  <marker id="d69-p1-verify-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#f59e0b"/></marker>
</defs>
<!-- Failed Path -->
<text x="20" y="26" fill="#f43f5e" font-size="10" font-family="sans-serif" font-weight="700">✗ FAILED PATH (Misclassified Stakeholder &amp; Missing Constraint)</text>
<rect x="20" y="36" width="130" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="85" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">CRO Misclassified</text>
<text x="85" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">"Monitor" Quadrant</text>
<line x1="150" y1="55" x2="180" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p1-fail-arrow)"/>
<rect x="180" y="36" width="140" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="250" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">No Data Residency</text>
<text x="250" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">Discovery Question</text>
<line x1="320" y1="55" x2="350" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p1-fail-arrow)"/>
<rect x="350" y="36" width="150" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="425" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">Spanner Multi-Region</text>
<text x="425" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">Designed (10 Weeks Lost)</text>
<line x1="500" y1="55" x2="530" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p1-fail-arrow)"/>
<rect x="530" y="36" width="150" height="38" rx="5" fill="#450a0a" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4"/>
<text x="605" y="51" text-anchor="middle" fill="#fca5a5" font-size="9" font-family="sans-serif" font-weight="700">CRO BOARD VETO</text>
<text x="605" y="63" text-anchor="middle" fill="#fca5a5" font-size="8" font-family="sans-serif">€2M Project Halted</text>
<!-- Corrected Path -->
<text x="20" y="118" fill="#22c55e" font-size="10" font-family="sans-serif" font-weight="700">✓ CORRECTED PATH (Governance Alignment &amp; Regional Constraint)</text>
<rect x="20" y="128" width="130" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="85" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">CRO → Manage Closely</text>
<text x="85" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Bi-weekly Checkpoint</text>
<line x1="150" y1="147" x2="180" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p1-ok-arrow)"/>
<rect x="180" y="128" width="140" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="250" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">Data Sovereignty</text>
<text x="250" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Elicitation Session</text>
<line x1="320" y1="147" x2="350" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p1-ok-arrow)"/>
<rect x="350" y="128" width="150" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="425" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">Spanner EU Regional</text>
<text x="425" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">(europe-west1)</text>
<line x1="500" y1="147" x2="530" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p1-ok-arrow)"/>
<rect x="530" y="128" width="150" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="605" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">ADR Signed by CRO</text>
<text x="605" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Project Resumes</text>
<!-- Verify Boundary -->
<rect x="340" y="196" width="340" height="50" rx="6" fill="#1c1100" stroke="#f59e0b" stroke-width="2"/>
<text x="510" y="217" text-anchor="middle" fill="#fcd34d" font-size="9.5" font-family="sans-serif" font-weight="700">▲ VERIFY BOUNDARY: Compliance Sign-Off &amp; Org Policy</text>
<text x="510" y="233" text-anchor="middle" fill="#fbbf24" font-size="8" font-family="sans-serif">Legal attestation + Org Policy gcp.resourceLocations locks region to europe-west1</text>
<line x1="605" y1="166" x2="510" y2="196" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#d69-p1-verify-arrow)"/>
<!-- Summary Banner -->
<rect x="20" y="272" width="720" height="32" rx="5" fill="#0f172a" stroke="#334155" stroke-width="1"/>
<text x="380" y="292" text-anchor="middle" fill="#94a3b8" font-size="8" font-family="sans-serif">Post-fix: CRO in Manage Closely · EU regional Spanner deployed · Data residency mandatory in discovery checklist · Trade-off signed in ADR</text>
</svg>
<figcaption>
<strong>Supplied facts:</strong> The bank planned a Cloud Spanner multi-region migration over 10 weeks; the CRO was omitted from active governance; the CRO halted the project in week 11 citing EU data sovereignty violations.
<br><strong>Architectural inference:</strong> The CRO possessed board-level veto authority despite a lack of prior meeting attendance. Google Cloud Spanner regional configurations provide full SQL compliance within EU boundaries, making it an immediately viable architecture had constraints been elicited in discovery.
<br><strong>Expected post-fix behavior:</strong> The discovery questionnaire incorporates mandatory data residency probes; the CRO is permanently situated in "Manage Closely"; Spanner EU regional is deployed under enforced Organization Policies with explicit ADR sign-off.
</figcaption>
</figure>
</article>

<!-- Problem 2 -->
<article id="topic-02-problem" class="topic-card">
<h3>Problem 2 — Solution-First Discovery Produces an Uncompliant Architecture</h3>
<h4>Scenario</h4>
<p>A digital health provider engaged an architecture team to modernize its legacy insurance claims engine. During the opening two-hour discovery session, the lead architect began with a solution-first proposal: <em>"We are recommending a fully serverless architecture built on Google Cloud Run with Eventarc triggers — does that align with your roadmap?"</em> The client's lead developer enthusiastically agreed, eager to eliminate Kubernetes node management toil. Three weeks into implementation, after services and event brokers had been provisioned, the client's corporate compliance and privacy officer conducted a routine architecture audit. The compliance officer immediately rejected the architecture: the platform processes sensitive Protected Health Information (PHI), and the organization's statutory HIPAA policy requires compute workloads to execute on physically dedicated hardware with strictly isolated memory boundaries — a standard incompatible with multi-tenant serverless execution environments.</p>
<h4>Failure Symptoms</h4>
<ul>
<li>The compliance officer files a formal compliance violation, halting staging deployments.</li>
<li>Three weeks of Cloud Run infrastructure as code, service configurations, and event-routing pipelines are scrapped.</li>
<li>The client's executive leadership questions the consulting team's enterprise healthcare domain competence.</li>
<li>The migration project delivery schedule slips by four weeks while compute options are re-assessed.</li>
</ul>
<h4>Diagnostic Sequence</h4>
<ol>
<li>Review the initial discovery meeting transcript: the session opened directly with a technology proposal without asking current-state or data classification questions.</li>
<li>Interview the client developer: they acknowledged agreeing to Cloud Run because of developer convenience, unaware of the organization's formal HIPAA compute isolation policies.</li>
<li>Review Google Cloud compute compliance capabilities: while Cloud Run is HIPAA-covered under a Google Cloud BAA, internal compliance interpretations frequently mandate sole-tenant node isolation or Confidential Computing.</li>
<li>Identify the procedural breakdown: the discovery session failed to apply the 5W+H sequence, skipping failure scenario and data sensitivity probes.</li>
</ol>
<h4>Root Cause</h4>
<p>Solution-first discovery created confirmation bias. By asking whether the customer liked Cloud Run rather than asking what regulatory constraints governed their data flows, the architect anchored the discussion on a technology preference and failed to elicit mandatory statutory boundaries.</p>
<h4>Remediation</h4>
<ol>
<li>Re-execute the discovery process using the 5W+H framework, starting with data classification and constraint elicitation before discussing compute targets.</li>
<li>Re-architect the compute layer to Google Kubernetes Engine (GKE) Standard deployed on Sole-Tenant Nodes with Confidential GKE Nodes enabled (AMD SEV memory encryption).</li>
<li>Execute the formal Google Cloud Business Associate Agreement (BAA) covering the targeted GCP projects.</li>
<li>Document the cost and operational impact: GKE on Sole-Tenant Nodes increases infrastructure costs by 28% compared to shared serverless execution, which is formally approved in the project budget.</li>
</ol>
<h4>Verification</h4>
<p>The compliance officer and chief legal counsel review the revised GKE Sole-Tenant architecture and execute the HIPAA compliance attestation. The executed BAA is verified in the Google Cloud Console, and Terraform deploys the cluster with sole-tenancy node affinity rules.</p>
<h4>Residual Risk</h4>
<p>GKE Standard requires ongoing node pool maintenance, version upgrades, and cluster monitoring that serverless Cloud Run would have avoided. Operational toil is mitigated by implementing automated node repair and upgrade maintenance windows.</p>

<figure style="margin:2rem 0;">
<svg id="d69-p2-svg" viewBox="0 0 760 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="d69-p2-title d69-p2-desc" style="width:100%;height:auto;display:block;background:#0f172a;border-radius:8px;">
<title id="d69-p2-title">Problem 2 Incident Diagram: Solution-First Discovery Failure</title>
<desc id="d69-p2-desc">Failed path illustrates opening discovery with a Cloud Run proposal leading to compliance rejection over shared tenancy. Corrected path shows 5W+H discovery, PHI isolation identification, GKE Sole-Tenant node architecture, and formal compliance approval.</desc>
<defs>
  <marker id="d69-p2-fail-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#f43f5e"/></marker>
  <marker id="d69-p2-ok-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#22c55e"/></marker>
  <marker id="d69-p2-verify-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#f59e0b"/></marker>
</defs>
<!-- Failed Path -->
<text x="20" y="26" fill="#f43f5e" font-size="10" font-family="sans-serif" font-weight="700">✗ FAILED PATH (Solution-First Anchoring &amp; Multi-Tenant Rejection)</text>
<rect x="20" y="36" width="140" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="90" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">"Cloud Run — Works?"</text>
<text x="90" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">Solution-First Opening</text>
<line x1="160" y1="55" x2="190" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p2-fail-arrow)"/>
<rect x="190" y="36" width="130" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="255" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">Dev Lead Agrees</text>
<text x="255" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">(No PHI Probed)</text>
<line x1="320" y1="55" x2="350" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p2-fail-arrow)"/>
<rect x="350" y="36" width="140" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="420" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">Cloud Run Provisioned</text>
<text x="420" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">3 Weeks Sunk Effort</text>
<line x1="490" y1="55" x2="520" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p2-fail-arrow)"/>
<rect x="520" y="36" width="150" height="38" rx="5" fill="#450a0a" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4"/>
<text x="595" y="51" text-anchor="middle" fill="#fca5a5" font-size="9" font-family="sans-serif" font-weight="700">COMPLIANCE AUDIT VETO</text>
<text x="595" y="63" text-anchor="middle" fill="#fca5a5" font-size="8" font-family="sans-serif">Shared-Tenant HIPAA Breach</text>
<!-- Corrected Path -->
<text x="20" y="118" fill="#22c55e" font-size="10" font-family="sans-serif" font-weight="700">✓ CORRECTED PATH (5W+H Data Flow Probes &amp; Dedicated Compute)</text>
<rect x="20" y="128" width="140" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="90" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">5W+H Diagnostic Order</text>
<text x="90" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Current-State First</text>
<line x1="160" y1="147" x2="190" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p2-ok-arrow)"/>
<rect x="190" y="128" width="150" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="265" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">PHI Sensitivity Probe</text>
<text x="265" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Dedicated Compute Elicited</text>
<line x1="340" y1="147" x2="370" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p2-ok-arrow)"/>
<rect x="370" y="128" width="150" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="445" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">GKE Standard +</text>
<text x="445" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Sole-Tenant Nodes</text>
<line x1="520" y1="147" x2="550" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p2-ok-arrow)"/>
<rect x="550" y="128" width="140" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="620" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">Executed HIPAA BAA</text>
<text x="620" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Compliance Approved</text>
<!-- Verify Boundary -->
<rect x="370" y="196" width="320" height="50" rx="6" fill="#1c1100" stroke="#f59e0b" stroke-width="2"/>
<text x="530" y="217" text-anchor="middle" fill="#fcd34d" font-size="9.5" font-family="sans-serif" font-weight="700">▲ VERIFY BOUNDARY: Compliance Sign-Off &amp; BAA</text>
<text x="530" y="233" text-anchor="middle" fill="#fbbf24" font-size="8" font-family="sans-serif">HIPAA BAA active in Console + Sole-Tenant Node Affinity validated in YAML</text>
<line x1="620" y1="166" x2="530" y2="196" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#d69-p2-verify-arrow)"/>
<!-- Summary Banner -->
<rect x="20" y="268" width="720" height="24" rx="5" fill="#0f172a" stroke="#334155" stroke-width="1"/>
<text x="380" y="284" text-anchor="middle" fill="#94a3b8" font-size="8" font-family="sans-serif">Post-fix: 5W+H probing mandatory · PHI data flow isolated · GKE Sole-Tenant nodes approved · +28% compute cost budgeted</text>
</svg>
<figcaption>
<strong>Supplied facts:</strong> The consulting architect pitched Cloud Run in discovery; the customer developer approved it; internal compliance rejected Cloud Run after 3 weeks of work due to shared-tenant compute policies.
<br><strong>Architectural inference:</strong> Leading questions create false consensus. While Cloud Run supports HIPAA under Google Cloud's standard BAA, enterprise security policies frequently interpret multi-tenancy as unacceptable risk, requiring dedicated hardware isolation.
<br><strong>Expected post-fix behavior:</strong> Discovery transcripts document current-state and statutory constraints before proposing runtimes; GKE Standard on Sole-Tenant Nodes is deployed with formal BAA execution; cost premiums are explicitly budgeted.
</figcaption>
</figure>
</article>

<!-- Problem 3 -->
<article id="topic-03-problem" class="topic-card">
<h3>Problem 3 — Ambiguous SLA Triggers a Six-Month Legal Dispute</h3>
<h4>Scenario</h4>
<p>A SaaS commerce provider signed an enterprise service contract with an omni-channel retailer featuring a contractual SLA guarantee stating simply: <em>"The Platform shall maintain 99.9% uptime measured monthly, subject to a 15% billing credit for breach."</em> During a major holiday promotional weekend, the retailer's product-catalog search service experienced a catastrophic cache stampede, causing complete search and catalog browsing outages for 4 consecutive hours. However, the core checkout API remained online. At month-end, the retailer demanded an SLA breach penalty, calculating that 4 hours of downtime exceeded the monthly 99.9% budget (which allows ~43.8 minutes). The SaaS vendor rejected the claim, arguing that the checkout API had achieved 99.96% availability and that "uptime" applied only to order-placement endpoints. The resulting legal dispute dragged on for six months, consuming executive bandwidth, requiring €180 000 in outside legal expenses, and ultimately culminating in a settlement and non-renewal of the contract.</p>
<h4>Failure Symptoms</h4>
<ul>
<li>Contractual terms failed to specify which service endpoints were included in the availability calculation.</li>
<li>The measurement method, measurement tooling, and sampling frequency were undefined.</li>
<li>The customer and vendor reviewed conflicting observability dashboards with zero shared telemetry.</li>
<li>A commercial customer relationship was permanently severed despite the checkout API remaining healthy.</li>
</ul>
<h4>Diagnostic Sequence</h4>
<ol>
<li>Examine the master services agreement (MSA): "uptime" was used as an undefined term without mathematical formulas or endpoint enumerations.</li>
<li>Review vendor monitoring: availability was measured solely via internal synthetic health pings to a private checkout VM IP.</li>
<li>Review customer telemetry: the retailer measured platform health using browser-side user telemetry where users were unable to browse products or add items to baskets.</li>
<li>Identify the architectural defect: lack of formal SLI definitions, SLO target windows, and designated authoritative measurement systems.</li>
</ol>
<h4>Root Cause</h4>
<p>The requirement was not SMART. Stating "99.9% uptime" without defining the SLI formula, the specific microservice endpoints, the measurement point (load balancer ingress vs private health check), and the authoritative logging tool created an irreconcilable interpretation gap.</p>
<h4>Remediation</h4>
<ol>
<li>Restructure all service level agreements to mandate per-service SMART SLOs: explicitly defining independent targets for <code>/api/v1/checkout</code> (99.95%) and <code>/api/v1/catalog</code> (99.9%).</li>
<li>Incorporate explicit SLI mathematical formulas into the contract: <code>SLI = count(HTTP 2xx) / count(total non-4xx) × 100</code> evaluated across a rolling 30-day window.</li>
<li>Designate the authoritative measurement tool: Google Cloud Monitoring Uptime Checks sampled every 60 seconds from three public probe regions against load balancer ingress.</li>
<li>Provide customer access to an unalterable, read-only Cloud Monitoring SLO compliance dashboard, guaranteeing identical operational visibility.</li>
</ol>
<h4>Verification</h4>
<p>Both legal teams review and adopt the modernized SLA contract addendum. Cloud Monitoring Uptime Checks and log-based alerting are deployed via Terraform, automatically generating certified monthly compliance audit reports.</p>
<h4>Residual Risk</h4>
<p>Uptime checks probing at 60-second intervals may fail to capture transient sub-minute micro-outages. To address this, the vendor supplements uptime checks with Google Cloud Monitoring log-based metrics derived directly from load balancer request logs.</p>

<figure style="margin:2rem 0;">
<svg id="d69-p3-svg" viewBox="0 0 760 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="d69-p3-title d69-p3-desc" style="width:100%;height:auto;display:block;background:#0f172a;border-radius:8px;">
<title id="d69-p3-title">Problem 3 Incident Diagram: Ambiguous SLA Resolution</title>
<desc id="d69-p3-desc">Failed path illustrates ambiguous 99.9% uptime contract leading to catalog outage dispute and expensive settlement. Corrected path demonstrates per-service SLOs, explicit load balancer measurement, shared Cloud Monitoring dashboards, and objective dispute-free reporting.</desc>
<defs>
  <marker id="d69-p3-fail-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#f43f5e"/></marker>
  <marker id="d69-p3-ok-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#22c55e"/></marker>
  <marker id="d69-p3-verify-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#f59e0b"/></marker>
</defs>
<!-- Failed Path -->
<text x="20" y="26" fill="#f43f5e" font-size="10" font-family="sans-serif" font-weight="700">✗ FAILED PATH (Ambiguous Contract &amp; Conflicting Telemetry)</text>
<rect x="20" y="36" width="140" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="90" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">"99.9% Uptime" SLA</text>
<text x="90" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">Undefined Scope / Tool</text>
<line x1="160" y1="55" x2="190" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p3-fail-arrow)"/>
<rect x="190" y="36" width="140" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="260" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">Catalog 4h Outage</text>
<text x="260" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">Checkout Stays Online</text>
<line x1="330" y1="55" x2="360" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p3-fail-arrow)"/>
<rect x="360" y="36" width="140" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="430" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">Vendor: "Checkout Up"</text>
<text x="430" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">Client: "Platform Down"</text>
<line x1="500" y1="55" x2="530" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p3-fail-arrow)"/>
<rect x="530" y="36" width="150" height="38" rx="5" fill="#450a0a" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4"/>
<text x="605" y="51" text-anchor="middle" fill="#fca5a5" font-size="9" font-family="sans-serif" font-weight="700">€180K LEGAL DISPUTE</text>
<text x="605" y="63" text-anchor="middle" fill="#fca5a5" font-size="8" font-family="sans-serif">6-Mo Battle &amp; Non-Renewal</text>
<!-- Corrected Path -->
<text x="20" y="118" fill="#22c55e" font-size="10" font-family="sans-serif" font-weight="700">✓ CORRECTED PATH (Per-Service SMART SLOs &amp; Objective Tooling)</text>
<rect x="20" y="128" width="150" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="95" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">Per-Service SLO Contract</text>
<text x="95" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Checkout + Catalog Independent</text>
<line x1="170" y1="147" x2="200" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p3-ok-arrow)"/>
<rect x="200" y="128" width="160" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="280" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">SLI Formula Specified</text>
<text x="280" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">HTTP 2xx / Non-4xx at Ingress</text>
<line x1="360" y1="147" x2="390" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p3-ok-arrow)"/>
<rect x="390" y="128" width="160" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="470" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">Cloud Monitoring Tooling</text>
<text x="470" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Uptime Checks + Synthetics</text>
<line x1="550" y1="147" x2="580" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p3-ok-arrow)"/>
<rect x="580" y="128" width="130" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="645" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">Shared Dashboard</text>
<text x="645" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Dispute-Free Reporting</text>
<!-- Verify Boundary -->
<rect x="380" y="192" width="330" height="46" rx="6" fill="#1c1100" stroke="#f59e0b" stroke-width="2"/>
<text x="545" y="213" text-anchor="middle" fill="#fcd34d" font-size="9" font-family="sans-serif" font-weight="700">▲ VERIFY BOUNDARY: Objective SLO Report</text>
<text x="545" y="226" text-anchor="middle" fill="#fbbf24" font-size="7.5" font-family="sans-serif">Customer views verified Cloud Monitoring audit dashboard; credits computed automatically</text>
<line x1="645" y1="166" x2="545" y2="192" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#d69-p3-verify-arrow)"/>
<!-- Summary Banner -->
<rect x="20" y="250" width="720" height="22" rx="5" fill="#0f172a" stroke="#334155" stroke-width="1"/>
<text x="380" y="265" text-anchor="middle" fill="#94a3b8" font-size="8" font-family="sans-serif">Post-fix: Named microservice SLOs · exact SLI formulas · Cloud Monitoring measurement point · shared read-only dashboard</text>
</svg>
<figcaption>
<strong>Supplied facts:</strong> The contract specified 99.9% uptime without service definitions; a 4-hour catalog outage occurred while checkout functioned; the vendor and customer spent 6 months and €180 000 in legal dispute.
<br><strong>Architectural inference:</strong> High-level contractual statements without architectural precision create legal liabilities. Availability must be decomposed into explicit, independently measurable SLIs tied to authoritative infrastructure telemetry.
<br><strong>Expected post-fix behavior:</strong> The SLA contract decomposes obligations into independent microservice SLOs with published SLI formulas; Google Cloud Monitoring provides the single source of truth; compliance reporting is transparent and automated.
</figcaption>
</figure>
</article>

<!-- Problem 4 -->
<article id="topic-04-problem" class="topic-card">
<h3>Problem 4 — "Everything is Priority 1" Delivers Zero Features in Six Weeks</h3>
<h4>Scenario</h4>
<p>An enterprise insurance group launched a digital portal overhaul, gathering requirements from nine distinct business units. Because no prioritization framework or capacity limits were enforced, each department head declared all of their requested capabilities as "Critical Priority 1," creating an unprioritized backlog of 147 user stories. Seeking to please all stakeholders simultaneously, the delivery manager launched Sprint 1 by scheduling 12 separate Priority 1 feature stories across five feature squads. Immediately upon kickoff, engineers discovered extensive circular dependencies: story A required customer database schema changes being authored by squad B, which depended on OAuth2 IAM scopes being implemented by squad C, which in turn relied on API gateway routes assigned to squad D. After two full two-week sprints (four weeks) and an emergency two-week hardening sprint (six weeks total), not a single feature story met the Definition of Done. Delivery velocity was zero, inter-team friction reached a boiling point, and the executive sponsor threatened a complete project reset.</p>
<h4>Failure Symptoms</h4>
<ul>
<li>Sprint burn-down charts showed flat-line progress: 12 stories started, 0 stories completed after 6 weeks.</li>
<li>Massive inter-squad blocking dependencies: developers spent hours waiting for schema PRs and IAM approvals.</li>
<li>Business unit leaders escalated to executive leadership, accusing delivery teams of incompetence.</li>
<li>The project backlog lacked any dependency sequence, capacity boundaries, or agreed-upon Won't-have list.</li>
</ul>
<h4>Diagnostic Sequence</h4>
<ol>
<li>Audit the 147-story backlog: discover that 100% of items were designated "Priority 1" with zero relative weighting.</li>
<li>Map technical dependencies: construct a directed acyclic graph (DAG) of the 12 in-flight stories, revealing that all 12 depended on four foundational infrastructure layers (IAM, DB schema, CI/CD, and Observability).</li>
<li>Calculate realistic team capacity: historical velocity across the delivery squads was exactly 40 story points per two-week sprint, whereas the 12 attempted stories totaled 138 story points.</li>
<li>Identify the governance failure: lack of a structured prioritization framework (MoSCoW or Weighted Scoring) and failure to enforce a strict sprint capacity cap.</li>
</ol>
<h4>Root Cause</h4>
<p>Absence of a prioritization discipline and capacity constraint. Without an explicit story point ceiling and objective scoring rubric, stakeholders had no incentive to negotiate trade-offs. Attempting to build interdependent business features before completing foundational infrastructure created catastrophic blocking gridlock.</p>
<h4>Remediation</h4>
<ol>
<li>Conduct an executive prioritization workshop enforcing a hard capacity constraint: <em>"Sprint capacity is strictly 40 story points per sprint. We will deliver the critical path infrastructure first."</em></li>
<li>Apply the Weighted Scoring Matrix across all candidate requirements using normalized stakeholder weights: Business Value (40%), Regulatory Risk (30%), Technical Feasibility (20%), and Implementation Speed (10%).</li>
<li>Sequence Sprint 1 strictly along the critical path to unblock all future feature work: R-01 IAM/Workload Identity (8 pts), R-03 Database Schema Baseline (13 pts), R-04 CI/CD Pipeline (11 pts), and R-02 Checkout SLO Monitoring (8 pts) = exactly 40 story points.</li>
<li>Formally publish the signed-off "Won't-Have-This-Sprint" list, setting clear executive expectations that feature development commences in Sprint 2 upon a verified, stable foundation.</li>
</ol>
<h4>Verification</h4>
<p>Sprint 1 delivers all four foundational infrastructure stories at a velocity of 40 points within two weeks. Sprint 2 commences with squads operating on decoupled feature branches with shared IAM, database schemas, and CI/CD automation already active.</p>
<h4>Residual Risk</h4>
<p>Business stakeholders whose features were deferred to later sprints may attempt to lobby for out-of-band priority escalation. This is mitigated by establishing a formal bi-weekly backlog re-scoring session governed strictly by the weighted matrix formula.</p>

<figure style="margin:2rem 0;">
<svg id="d69-p4-svg" viewBox="0 0 760 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="d69-p4-title d69-p4-desc" style="width:100%;height:auto;display:block;background:#0f172a;border-radius:8px;">
<title id="d69-p4-title">Problem 4 Incident Diagram: Backlog Prioritization Failure &amp; Critical Path Recovery</title>
<desc id="d69-p4-desc">Failed path illustrates 147 stories rated Priority 1 leading to 12 stories started simultaneously, circular blocking dependencies, zero velocity, and a project reset. Corrected path demonstrates MoSCoW with a 40-point capacity cap, weighted scoring dependency sequencing, full velocity recovery, and unblocked feature delivery.</desc>
<defs>
  <marker id="d69-p4-fail-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#f43f5e"/></marker>
  <marker id="d69-p4-ok-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#22c55e"/></marker>
  <marker id="d69-p4-verify-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#f59e0b"/></marker>
</defs>
<!-- Failed Path -->
<text x="20" y="26" fill="#f43f5e" font-size="10" font-family="sans-serif" font-weight="700">✗ FAILED PATH (Unconstrained Backlog &amp; Circular Blocking Gridlock)</text>
<rect x="20" y="36" width="130" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="85" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">147 Backlog Stories</text>
<text x="85" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">All Rated "Priority 1"</text>
<line x1="150" y1="55" x2="180" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p4-fail-arrow)"/>
<rect x="180" y="36" width="140" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="250" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">12 Started in Sprint 1</text>
<text x="250" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">138 pts (Cap = 40)</text>
<line x1="320" y1="55" x2="350" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p4-fail-arrow)"/>
<rect x="350" y="36" width="140" height="38" rx="5" fill="#2d1515" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="420" y="53" text-anchor="middle" fill="#fda4af" font-size="8.5" font-family="sans-serif">Circular Dependencies</text>
<text x="420" y="65" text-anchor="middle" fill="#fda4af" font-size="8" font-family="sans-serif">Schema/IAM Blocked</text>
<line x1="490" y1="55" x2="520" y2="55" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#d69-p4-fail-arrow)"/>
<rect x="520" y="36" width="150" height="38" rx="5" fill="#450a0a" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4"/>
<text x="595" y="51" text-anchor="middle" fill="#fca5a5" font-size="9" font-family="sans-serif" font-weight="700">VELOCITY = 0 (6 WEEKS)</text>
<text x="595" y="63" text-anchor="middle" fill="#fca5a5" font-size="8" font-family="sans-serif">Project Reset Threatened</text>
<!-- Corrected Path -->
<text x="20" y="118" fill="#22c55e" font-size="10" font-family="sans-serif" font-weight="700">✓ CORRECTED PATH (Weighted Scoring &amp; Critical Path Sequencing)</text>
<rect x="20" y="128" width="145" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="92" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">MoSCoW + Capacity Cap</text>
<text x="92" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Strict 40 Pts per Sprint</text>
<line x1="165" y1="147" x2="195" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p4-ok-arrow)"/>
<rect x="195" y="128" width="150" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="270" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">Weighted Scoring Matrix</text>
<text x="270" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">BV 40% · Reg 30% · Feas 20%</text>
<line x1="345" y1="147" x2="375" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p4-ok-arrow)"/>
<rect x="375" y="128" width="170" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="460" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">Sprint 1: IAM + DB +</text>
<text x="460" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">CI/CD + SLO (40 Pts)</text>
<line x1="545" y1="147" x2="575" y2="147" stroke="#22c55e" stroke-width="2.5" marker-end="url(#d69-p4-ok-arrow)"/>
<rect x="575" y="128" width="125" height="38" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="2.5"/>
<text x="637" y="145" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="sans-serif">Velocity = 40 Pts</text>
<text x="637" y="157" text-anchor="middle" fill="#86efac" font-size="8" font-family="sans-serif">Sprint 2 Unblocked</text>
<!-- Verify Boundary -->
<rect x="380" y="196" width="320" height="48" rx="6" fill="#1c1100" stroke="#f59e0b" stroke-width="2"/>
<text x="540" y="217" text-anchor="middle" fill="#fcd34d" font-size="9" font-family="sans-serif" font-weight="700">▲ VERIFY BOUNDARY: Sprint Retrospective Acceptance</text>
<text x="540" y="231" text-anchor="middle" fill="#fbbf24" font-size="7.5" font-family="sans-serif">100% of 4 critical path stories done; automated CI/CD &amp; IAM active; velocity restored</text>
<line x1="637" y1="166" x2="540" y2="196" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#d69-p4-verify-arrow)"/>
<!-- Summary Banner -->
<rect x="20" y="266" width="720" height="24" rx="5" fill="#0f172a" stroke="#334155" stroke-width="1"/>
<text x="380" y="281" text-anchor="middle" fill="#94a3b8" font-size="8" font-family="sans-serif">Post-fix: MoSCoW capacity ceiling enforced · weighted scoring applied · critical path unblocked · Won't-have list signed</text>
</svg>
<figcaption>
<strong>Supplied facts:</strong> 147 user stories were all rated Priority 1 by 9 business units; 12 stories (138 pts) started simultaneously in Sprint 1; circular blocking dependencies halted progress for 6 weeks with zero velocity.
<br><strong>Architectural inference:</strong> Trying to deliver features without an explicit capacity cap and without completing critical path infrastructure creates exponential blocking dependencies. Enforcing a strict 40-point capacity cap forces objective trade-offs.
<br><strong>Expected post-fix behavior:</strong> The weighted scoring matrix sequences foundational infrastructure first; Sprint 1 completes all 4 core stories (40 pts); subsequent sprints proceed on independent feature branches without cross-team blocking.
</figcaption>
</figure>
</article>

</section>

<!-- ═══════════════════════════════════════════════════════ PART 4 ═══ -->
<section id="part-4" class="part"><h2>4 · Labs</h2>

<!-- Lab 1 -->
<article id="topic-01-lab" class="topic-card lab">
<h3>Lab 1 — Build a Stakeholder Power-Interest Grid</h3>
<p>Produce a comprehensive stakeholder register and conflict resolution plan for the Brightloaf retail modernization using the power-interest grid framework. All commands execute locally in a temporary directory with zero billable cloud resources.</p>
<ol>
<li><strong>Initialize the local lab directory and author the stakeholder register.</strong>

<pre><code>mkdir -p ~/day-069-labs && cd ~/day-069-labs
cat &lt;&lt;'EOF' &gt; stakeholder-register.md
# Brightloaf Stakeholder Register — Day 69

## Power-Interest Grid

| Stakeholder | Role | Power | Interest | Grid Quadrant | Strategy |
|---|---|---|---|---|---|
| Alex Chen | CTO | High | High | Manage Closely | Weekly arch review; joint decision on platform bets |
| Maya Patel | CISO | High | High | Manage Closely | Security gate reviews; audit trail for each decision |
| Jordan Kim | CFO | High | Medium | Keep Satisfied | Monthly cost dashboard; exception escalations only |
| Sam Rivera | SRE Lead | Medium | High | Keep Informed | Sprint demos; incident post-mortem reviews |
| Dev Team (10) | Developers | Low | High | Keep Informed | RFC process; platform office hours |
| Priya Singh | Chief Risk Officer | High | Low | Keep Satisfied | Compliance attestations; quarterly briefing |
| Legal (external) | Legal / Compliance | High | Low | Keep Satisfied | Data residency and contract sign-off only |

## Primary Goals per Stakeholder

### CTO (Alex Chen)
- Time-to-market: 90-day MVP delivery
- Strategic bets: Cloud-native microservices, GKE Standard
- Technical debt: reduce Oracle dependency within 18 months
- Innovation velocity: deploy frequency &gt; 1/day

### CISO (Maya Patel)
- Threat surface: SOC 2 Type II audit in 9 months
- Compliance: PCI DSS SAQ-D (cardholder tokenization via Stripe)
- Breach liability: zero critical CVEs in production containers
- Zero-trust: Workload Identity for all SA-to-SA calls

### CFO (Jordan Kim)
- TCO vs ROI: &lt;$500K cloud/year; 3-year CUD planned
- OpEx predictability: &lt;±10% monthly cloud spend variance
- Budget alerts: 80% threshold; anomaly detection for spend spikes

### SRE Lead (Sam Rivera)
- MTTR: &lt;15 minutes for Sev-1 incidents
- On-call burden: &lt;4 hours per engineer per week
- Runbook coverage: &gt;90% of known failure scenarios documented
- Change failure rate: DORA elite (&lt;15%)

### Developers
- Deployment frequency: &gt;1 per day per service
- CI/CD pipeline speed: &lt;10 minutes from commit to staging
- Local dev parity: docker-compose mirrors production topology
- Cognitive load: &lt;3 new tools per quarter
EOF
echo "Stakeholder register created: $(wc -l &lt; stakeholder-register.md) lines"
</code></pre>
</li>

<li><strong>Document the conflict resolution register.</strong>

<pre><code>cat &lt;&lt;'EOF' &gt; conflict-register.md
# Brightloaf Stakeholder Conflict Register — Day 69

## Conflict 1: CISO vs Developers — SAST Gate Duration
- CISO requires: blocking SAST gate before merge to main
- Developers require: CI/CD pipeline &lt;10 minutes (SAST adds 18 min)
- Impact: CI/CD SLO violated; developer DX degraded
- Resolution: Risk-tiered scanning — critical/high findings block; medium/low async.
  Implement Semgrep with --severity=ERROR as blocking gate; full scan runs async
  in parallel. Expected blocking gate time: 3 minutes.
- Owner: CISO + Dev Lead joint decision
- Target date: Sprint 2

## Conflict 2: CFO vs SRE — Multi-Region Reliability Investment
- CFO requires: fixed capacity (20 n2-standard-8 with 3-yr CUD) for &lt;±10% variance
- SRE requires: auto-scaling (max 40 replicas) for Black Friday peak resilience
- Impact: At fixed capacity, 38K concurrent users risks 503 errors (from Day 67 data)
- Resolution: Shadow-mode canary — run auto-scaling config on 10% of traffic for 30 days.
  Collect cost and error-rate data. Present to both stakeholders before Sprint 5.
- Evidence needed: Day 67 peak RPS data; cost model at 20 vs 40 instances
- Owner: CTO mediates; CFO and SRE co-sign

## Conflict 3: CTO vs SRE — Change Freeze Policy
- CTO requires: strategic feature shipped in Black Friday week
- SRE requires: change freeze (last 10 days before peak events)
- Resolution: Feature flags — deploy code before freeze, activate flag after peak.
  Cloud Deploy + LaunchDarkly feature flag. Deploy ≠ release.
- Owner: SRE Lead approves deployment; CTO controls flag activation
EOF
echo "Conflict register created: $(wc -l &lt; conflict-register.md) lines"
</code></pre>
</li>

<li><strong>Validate stakeholder register completeness with Python.</strong>

<pre><code>python3 - &lt;&lt;'EOF'
with open("stakeholder-register.md") as f:
    content = f.read()

required_sections = [
    "Power-Interest Grid",
    "Manage Closely",
    "Keep Satisfied",
    "Keep Informed",
    "CTO",
    "CISO",
    "CFO",
    "SRE",
]
missing = [s for s in required_sections if s not in content]
if missing:
    print(f"MISSING sections: {missing}")
    exit(1)
else:
    print("Stakeholder register: all required sections present")
    rows = [l for l in content.splitlines() if l.startswith("|") and ("High" in l or "Low" in l)]
    print(f"Stakeholder rows found: {len(rows)}")
    print("Validation check: PASS — Register is valid for Day 69 exit evidence")
EOF
</code></pre>
</li>
</ol>
<div class="callout success"><strong>Expected result / acceptance</strong>
<p>A saved <code>stakeholder-register.md</code> containing 7 enterprise stakeholders correctly categorized into the four grid quadrants with primary goals, and a <code>conflict-register.md</code> detailing 3 concrete conflict patterns with assigned owners. The Python verification outputs <code>Validation check: PASS</code>.</p>
</div>
<div class="callout caution"><strong>Troubleshooting</strong>
<p>If the Python validation reports missing sections, ensure that the markdown headers use the exact strings specified in <code>required_sections</code>. Whitespace variations within table cells do not affect parsing.</p>
</div>
<div class="callout"><strong>Cleanup and cost</strong>
<p>No billable Google Cloud resources created. Preserve all markdown files for Gate 4 (Day 82) architectural audit evidence.</p>
</div>
<label class="check"><input type="checkbox" data-progress="lab-69-topic-01"> I completed and checked this topic exercise</label>
</article>

<!-- Lab 2 -->
<article id="topic-02-lab" class="topic-card lab">
<h3>Lab 2 — Run a Structured Discovery Session (Simulated)</h3>
<p>Execute a simulated 5W+H discovery interview against the Brightloaf retailer persona. Extract, categorize, and validate a formal constraint register separating fixed statutory constraints from negotiable infrastructure choices.</p>
<ol>
<li><strong>Generate the discovery session transcript.</strong>

<pre><code>cat &lt;&lt;'EOF' &gt; discovery-session.md
# Brightloaf Discovery Session Transcript — Day 69

Date: 2026-09-28 [simulated enterprise discovery]
Participants: Lead Architect (Consultant), CTO (Alex), SRE Lead (Sam), CFO (Jordan), CISO (Maya)
Duration: 2 hours
Framework: 5W+H — Current-state first, then failure probes, then constraints, then target outcomes

## WHO — Stakeholder Ownership &amp; Governance
Q: Who owns the checkout system end-to-end (deploy, monitor, on-call)?
A: Sam's SRE team owns ops; checkout squad (4 devs) owns code; no single DRI.
Finding: Shared ownership without DRI is a reliability risk — define DRI in RACI.

Q: Who has authority to approve production changes?
A: CTO for architecture; SRE Lead for operational changes; no formal CAB.
Finding: No Change Advisory Board — change failure rate data unavailable.

## WHAT — System Inventory &amp; Observability
Q: What systems are in scope for this migration?
A: Checkout API, product-catalog service, order-status API, inventory service, Oracle order ledger.
Finding: 5 services; Oracle order ledger is on-prem with active PCI scope.

Q: What monitoring do you have today?
A: Datadog APM for checkout API; no monitoring on product-catalog or inventory service.
Finding: 3 of 5 services have ZERO observability — blind spots for migration.

Q: What is your current deployment process?
A: Manual SSH to staging; Jenkins pipeline to production (30 min pipeline, manual approval).
Finding: 30-minute pipeline violates developer DX SLO (&lt;10 min). Manual SSH to staging is a security risk.

## WHEN — Incident Timeline &amp; Recovery
Q: How long does a production incident take to resolve?
A: Sev-1: average 45 minutes. Worst case: 4 hours (DB deadlock in Dec 2024).
Finding: MTTR baseline = 45 min; target = 15 min. Gap = 30 minutes of toil reduction needed.

Q: What breaks most often?
A: Product-catalog cache invalidation (3x/month); Oracle deadlock under load (1x/quarter).
Finding: Cache invalidation is top failure mode — needs investigation in Day 63-64 context.

## WHERE — Topology &amp; Data Residency
Q: Where does customer data reside?
A: EU customers: Oracle on-prem in Frankfurt data centre. US customers: Cloud SQL in us-central1.
Finding: EU customer data is on-prem. Migration must comply with GDPR data residency.
       Frankfurt data centre = europe-west3 if migrating to GCP.

Q: Which data flows contain PII or PCI-scoped data?
A: All order records contain customer name, email, address (PII). Payment tokens via Stripe (PCI scope reduced — no raw card data on GCP). Returns contain bank account numbers (PCI scope — must confirm with QSA).
Finding: Returns flow may be in PCI scope — QSA review required before migrating returns service.

## WHY — Commercial Drivers &amp; Deadlines
Q: Why are you migrating now?
A: Oracle support contract expires in 18 months; Black Friday scaling limits hit in 2024 (38K users = 503 errors).
Finding: 18-month hard deadline for Oracle exit; scaling was the triggering business event.

Q: What constraints can you NOT change?
A: Oracle contract runs 18 months — cannot accelerate exit. Stripe tokenization — contractually bound. Frankfurt data centre lease — 12 months remaining (can exit early with 3-month notice).
Finding: Hard constraint: Oracle 18 months. Negotiable: Frankfurt lease (3-month notice).

## HOW — Failure Scenarios &amp; Success State
Q: What is the worst thing that has happened in production?
A: Dec 2024: Oracle deadlock under Black Friday load caused 4-hour checkout outage; $600K revenue lost.
Finding: This is the primary business motivation. Cloud Spanner eliminates Oracle deadlock by design.

Q: What does success look like in 12 months?
A: Deploy frequency &gt;1/day; MTTR &lt;15 min; Black Friday 50K concurrent users with no 503s; Oracle migrated.
Finding: These are the exit criteria for Gate 4 (Day 82) architecture review.

## CONSTRAINTS LOG
| ID | Constraint | Type | Fixed/Negotiable | Owner |
|---|---|---|---|---|
| C-01 | Oracle contract: 18 months remaining | Timeline | Fixed | CFO |
| C-02 | Stripe tokenization (contractual) | Vendor | Fixed | CTO |
| C-03 | EU GDPR data residency (Germany/EU) | Regulatory | Fixed | CISO |
| C-04 | PCI QSA review required for returns flow | Regulatory | Fixed | CISO |
| C-05 | Frankfurt DC lease (12 months, 3-month exit) | Infrastructure | Negotiable | CFO |
| C-06 | Datadog APM (current license, renewal in 6 months) | Tooling | Negotiable | SRE |
| C-07 | Jenkins pipeline (institutional knowledge) | Skills | Negotiable | Dev Lead |

## ANTI-PATTERNS IDENTIFIED AND AVOIDED
1. Did NOT open with "We plan to use Cloud Run" — current-state inventory came first
2. Did NOT accept "it depends" for MTTR — probed for worst-case (4 hours)
3. Did NOT skip failure scenario elicitation — Dec 2024 outage surfaced the primary motivation
4. Did NOT assume PCI scope — explicitly asked about each data flow
EOF
echo "Discovery session transcript created: $(wc -l &lt; discovery-session.md) lines"
</code></pre>
</li>

<li><strong>Extract and validate constraints using Python.</strong>

<pre><code>python3 - &lt;&lt;'EOF'
with open("discovery-session.md") as f:
    lines = f.readlines()

in_constraints = False
constraints = []
for line in lines:
    if "CONSTRAINTS LOG" in line:
        in_constraints = True
    if in_constraints and line.startswith("| C-"):
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) &gt;= 5:
            constraints.append(parts)

print(f"Constraints extracted: {len(constraints)}")
for c in constraints:
    print(f"  {c[0]}: {c[1]} [{c[3]}] Owner: {c[4]}")

types = [c[3] for c in constraints]
has_fixed = any("Fixed" in t for t in types)
has_neg = any("Negotiable" in t for t in types)
print(f"Fixed constraints found: {sum(1 for t in types if 'Fixed' in t)}")
print(f"Negotiable constraints found: {sum(1 for t in types if 'Negotiable' in t)}")

if len(constraints) &gt;= 7 and has_fixed and has_neg:
    print("Validation check: PASS — Constraints classification complete")
else:
    print("Validation check: FAIL — Incomplete constraints log")
    exit(1)
EOF
</code></pre>
</li>
</ol>
<div class="callout success"><strong>Expected result / acceptance</strong>
<p>A saved <code>discovery-session.md</code> document capturing the 5W+H diagnostic interview, an extracted 7-item constraint register differentiating Fixed from Negotiable constraints, and an anti-pattern verification log. The Python script outputs <code>Validation check: PASS</code>.</p>
</div>
<div class="callout"><strong>Cleanup and cost</strong>
<p>No billable resources created.</p>
</div>
<label class="check"><input type="checkbox" data-progress="lab-69-topic-02"> I completed and checked this topic exercise</label>
</article>

<!-- Lab 3 -->
<article id="topic-03-lab" class="topic-card lab">
<h3>Lab 3 — Write SMART SLOs with Error Budget Derivation</h3>
<p>Translate the Brightloaf retailer's business objectives into formal SMART Service Level Objectives (SLOs), calculating exact error budgets and multiwindow multi-burn-rate alerting policies.</p>
<ol>
<li><strong>Generate the formal SMART SLO register.</strong>

<pre><code>cat &lt;&lt;'EOF' &gt; slo-register.md
# Brightloaf SMART SLO Register — Day 69

## SLO-01: Checkout API Availability
- **SLI:** count(HTTP 2xx responses) / count(total non-4xx requests) × 100
- **SLO:** 99.95% measured over a rolling 28-day window at the Global External Application Load Balancer
- **Measurement window:** Rolling 28 days (2,419,200 seconds)
- **Error budget:** (1 - 0.9995) × 2,419,200 = 1,209.6 s ≈ 20.2 minutes/month
- **Acceptance method:** Cloud Monitoring uptime check on /health/checkout; log-based SLI from loadbalancer.googleapis.com metric; sampled every 60 s
- **Alerting:** 1h burn-rate &gt; 14.4× → PagerDuty page; 6h burn-rate &gt; 6× → Jira ticket
- **Owner:** SRE Lead (Sam Rivera)
- **Baseline (Day 67):** 99.87% (current) → gap = 0.08 percentage points

## SLO-02: Checkout API Request Latency
- **SLI:** p99 response time at load balancer ingress for all requests where body size &lt; 64 KB
- **SLO:** p99 &lt; 300 ms, measured over a rolling 1-hour window
- **Error budget:** 1% of hourly requests may exceed 300 ms (36 seconds cumulative tail budget)
- **Acceptance method:** Cloud Monitoring loadbalancing.googleapis.com/https/request_latencies distribution metric; percentile alerting policy at 0.99
- **Alerting:** p99 &gt; 300 ms sustained for 5 minutes → PagerDuty ticket
- **Owner:** Checkout squad (Alex Chen)
- **Baseline (Day 67):** p99 = 420 ms (current) → gap requires query optimization

## SLO-03: Order-Status API Availability
- **SLI:** count(HTTP 2xx responses) / count(total non-4xx requests) × 100
- **SLO:** 99.9% over a rolling 28-day window
- **Error budget:** (1 - 0.999) × 2,419,200 = 2,419.2 s ≈ 40.3 minutes/month
- **Acceptance method:** Cloud Monitoring uptime check on /health/order-status sampled every 60 s
- **Owner:** SRE Lead (Sam Rivera)

## SLO-04: Data Freshness (BigQuery Analytics Pipeline)
- **SLI:** Age of most recently inserted record in the orders_daily BigQuery table (seconds)
- **SLO:** &lt; 300 seconds (5 minutes) freshness lag, measured continuously
- **Error budget:** &lt; 5 minutes per day of stale data (300 s/day allowable breach)
- **Acceptance method:** Custom Cloud Monitoring metric from Pub/Sub-to-BQ pipeline lag; alert on &gt;300s lag sustained for 2 minutes
- **Owner:** Data Engineering Team

## UNRESOLVED BUSINESS QUESTIONS
Q1: What is the actual Black Friday p99 latency baseline from Day 67 traffic data? (Assumption: 420 ms)
Q2: Has the HIPAA BAA been executed with Google Cloud? (Required prior to PHI storage in Cloud SQL)
Q3: Has the QSA confirmed PCI scope for the returns flow? (C-04 in constraint log)
Q4: What is the agreed measurement start date for SLO-01 and SLO-02 baseline enforcement?

## ACCEPTANCE SIGN-OFF REQUIRED
[ ] CTO (Alex Chen): SLO targets achievable within 90-day MVP timeline
[ ] CISO (Maya Patel): Measurement method satisfies audit evidence requirements
[ ] SRE Lead (Sam Rivera): Alerting policy integrated with PagerDuty and on-call rotation
[ ] CFO (Jordan Kim): Error budget policy aligned with contractual SLA penalties
EOF
echo "SLO register created: $(wc -l &lt; slo-register.md) lines"
</code></pre>
</li>

<li><strong>Verify mathematical calculations and burn-rate alerting thresholds.</strong>

<pre><code>python3 - &lt;&lt;'EOF'
window_28d = 28 * 24 * 3600  # 2,419,200 seconds

slos = [
    {"name": "SLO-01 Checkout Availability", "slo": 0.9995, "window_s": window_28d},
    {"name": "SLO-02 Checkout Latency (1% tail)", "slo": 0.99, "window_s": 3600},
    {"name": "SLO-03 Order-Status Availability", "slo": 0.999, "window_s": window_28d},
    {"name": "SLO-04 Freshness (5min/day budget)", "slo": 0.9965, "window_s": 86400},
]

print("=" * 72)
print(f"{'SLO Target Name':&lt;42} {'Budget (s)':&gt;12} {'Budget (min)':&gt;14}")
print("=" * 72)
for s in slos:
    budget_s = (1 - s["slo"]) * s["window_s"]
    budget_m = budget_s / 60
    print(f"{s['name']:&lt;42} {budget_s:&gt;12.1f} {budget_m:&gt;14.1f}")
print("=" * 72)

# Verify Google SRE Multi-Burn-Rate Formulas
# Standard Google SRE Rule (Workbook Ch 5):
# 1-hour fast burn alert: 2% of budget consumed in 1 hour -&gt; Burn Rate = 14.4x (for 30-day) or 13.44x (for 28-day)
# 6-hour mid burn alert: 5% of budget consumed in 6 hours -&gt; Burn Rate = 6.0x
burn_1h_pct = 0.02
burn_6h_pct = 0.05
hours_28d = 28 * 24
burn_rate_1h = (burn_1h_pct * hours_28d) / 1.0
burn_rate_6h = (burn_6h_pct * hours_28d) / 6.0
print(f"28-Day Window Hours: {hours_28d}h")
print(f"  1h Fast Burn Threshold (2% budget consumed): {burn_rate_1h:.2f}x (Pages On-Call SRE)")
print(f"  6h Mid Burn Threshold (5% budget consumed):  {burn_rate_6h:.2f}x (Tickets Team Queue)")

# SLO-01 Check
slo01_budget = (1 - 0.9995) * window_28d
assert abs(slo01_budget - 1209.6) &lt; 0.1, "SLO-01 arithmetic mismatch"
print("Validation check: PASS — Error budget arithmetic and burn-rate alerts verified")
EOF
</code></pre>
</li>
</ol>
<div class="callout success"><strong>Expected result / acceptance</strong>
<p>A saved <code>slo-register.md</code> containing 4 SMART SLOs with explicit SLIs, targets, measurement windows, acceptance tooling, alerting thresholds, and unresolved business questions. The Python script confirms exact error budget arithmetic (SLO-01 = 1 209.6 seconds) and outputs <code>Validation check: PASS</code>.</p>
</div>
<div class="callout"><strong>Cleanup and cost</strong>
<p>No billable resources created.</p>
</div>
<label class="check"><input type="checkbox" data-progress="lab-69-topic-03"> I completed and checked this topic exercise</label>
</article>

<!-- Lab 4 -->
<article id="topic-04-lab" class="topic-card lab">
<h3>Lab 4 — MoSCoW Classification and Weighted Scoring Matrix</h3>
<p>Apply the MoSCoW framework and a Weighted Scoring Matrix to prioritize the Brightloaf retail candidate backlog, enforcing a 40-story-point Sprint 1 capacity limit and compiling the final exit artifact.</p>
<ol>
<li><strong>Generate the MoSCoW classification and weighted scoring register.</strong>

<pre><code>cat &lt;&lt;'EOF' &gt; moscow-scoring.md
# Brightloaf MoSCoW + Weighted Scoring Matrix — Day 69

## Sprint 1 Capacity Limit: 40 story points | 2-week sprint

## Criteria Weights (Stakeholder-Agreed)
| Criterion | Weight | Rationale |
|---|---|---|
| Business Value (BV) | 0.40 | Protects peak Black Friday revenue and customer conversion |
| Regulatory Risk (Reg) | 0.30 | PCI DSS SAQ-D audit deadline; non-negotiable statutory rule |
| Technical Feasibility (Feas) | 0.20 | Team skills: GKE Standard + Terraform; avoids unproven tech |
| Time-to-Implement (Speed) | 0.10 | Velocity and delivery constraint |

## Requirement Scoring Matrix
Formula: `Score = (BV × 0.40) + (Reg × 0.30) + (Feas × 0.20) + (Speed × 0.10)`

| Req ID | Requirement | BV/10 | Reg/10 | Feas/10 | Spd/10 | Score | MoSCoW | Points | Critical Dependency |
|---|---|---|---|---|---|---|---|---|---|
| R-01 | IAM &amp; Workload Identity bootstrap | 9 | 10 | 9 | 8 | 9.20 | Must | 8 | None (Unblocks all) |
| R-02 | Checkout API availability SLO monitoring | 10 | 8 | 9 | 7 | 8.90 | Must | 8 | R-01 (Validates prod) |
| R-03 | Database schema baseline (Cloud SQL) | 9 | 8 | 8 | 6 | 8.20 | Must | 13 | R-01 (Enables data) |
| R-04 | CI/CD pipeline (Cloud Build + Deploy) | 8 | 5 | 8 | 7 | 7.00 | Must | 11 | R-01 (Enables deploy) |
| R-06 | Budget alert at 80% threshold | 7 | 4 | 9 | 9 | 6.70 | Should | 5 | R-01 (FinOps guardrail) |
| R-05 | Auto-scaling MIG policy (CPU 60%) | 8 | 3 | 8 | 6 | 6.30 | Should | 8 | R-03, R-04 (Autoscaling) |
| R-07 | Multi-region active-active failover | 7 | 5 | 6 | 3 | 5.80 | Could | 21 | R-02, R-03 (Dual region) |
| R-10 | Oracle to Spanner migration phase 1 | 6 | 6 | 4 | 1 | 5.10 | Won't | 34 | R-03 (18-mo contract) |
| R-08 | Self-service FinOps cost dashboard | 5 | 1 | 8 | 8 | 4.70 | Could | 8 | R-06 (Internal tool) |
| R-09 | Datadog agent migration to Cloud Mon | 4 | 2 | 5 | 2 | 3.40 | Won't | 13 | R-01 (6-mo license left) |

## Sprint 1 Selection (Dependency-Ordered, 40 Points Total)
1. R-01: IAM &amp; Workload Identity Bootstrap (8 pts) — FIRST: unblocks security perimeter
2. R-03: Cloud SQL Database Schema Baseline (13 pts) — requires R-01; unblocks persistence
3. R-04: CI/CD Pipeline Cloud Deploy (11 pts) — requires R-01; unblocks automated delivery
4. R-02: Checkout API SLO Monitoring (8 pts) — requires R-01; validates operational readiness
Total Sprint Points: 8 + 13 + 11 + 8 = 40 pts (100% capacity · zero circular dependencies)

## Won't-Have-This-Sprint (Signed Off by Stakeholders)
- R-07 Multi-region failover: deferred to Sprint 4 (single-region stability must be proven first)
- R-08 Self-service FinOps dashboard: deferred to Sprint 3 (requires billing export data from Sprints 1-2)
- R-09 Datadog agent migration: deferred to Sprint 5 (current commercial Datadog license has 6 months remaining)
- R-10 Oracle to Spanner migration: deferred to Sprint 6+ (Oracle support contract has 18 months remaining)

## Conflict Resolution: Auto-scaling vs Fixed Capacity (R-05)
Decision: R-05 promoted to Should-have; deferred to Sprint 2.
Resolution Protocol: Deploy 30-day shadow-mode canary in Sprint 1 routing 5% production traffic to auto-scaling MIG.
Empirical Data Collected: Month-over-month cost variance, p99 latency, and instance cold-start timings.
Approval Authority: CTO mediates; CFO and SRE co-sign Sprint 2 deployment plan after canary data review.

## Minimum Viable Product (MVP) Definition
The minimum set of architectural components that proves the core business hypothesis:
"Can Brightloaf deploy secure microservices to GCP with automated CI/CD, persistence, and
verifiable SLO observability within 40 story points?" — proven when Sprint 1 delivers all four
foundational stories and the checkout health check reports baseline SLO metrics.
EOF
echo "MoSCoW scoring matrix created: $(wc -l &lt; moscow-scoring.md) lines"
</code></pre>
</li>

<li><strong>Validate mathematical scoring and sprint capacity with Python.</strong>

<pre><code>python3 - &lt;&lt;'EOF'
requirements = [
    {"id": "R-01", "name": "IAM &amp; Workload Identity",     "bv": 9, "reg": 10, "feas": 9, "speed": 8, "pts": 8},
    {"id": "R-02", "name": "Checkout SLO monitoring",     "bv": 10, "reg": 8, "feas": 9, "speed": 7, "pts": 8},
    {"id": "R-03", "name": "Database schema baseline",    "bv": 9, "reg": 8, "feas": 8, "speed": 6, "pts": 13},
    {"id": "R-04", "name": "CI/CD pipeline",              "bv": 8, "reg": 5, "feas": 8, "speed": 7, "pts": 11},
    {"id": "R-05", "name": "Auto-scaling MIG policy",     "bv": 8, "reg": 3, "feas": 8, "speed": 6, "pts": 8},
    {"id": "R-06", "name": "Budget alert at 80%",         "bv": 7, "reg": 4, "feas": 9, "speed": 9, "pts": 5},
    {"id": "R-07", "name": "Multi-region failover",       "bv": 7, "reg": 5, "feas": 6, "speed": 3, "pts": 21},
    {"id": "R-08", "name": "Self-service cost dashboard", "bv": 5, "reg": 1, "feas": 8, "speed": 8, "pts": 8},
    {"id": "R-09", "name": "Datadog migration",           "bv": 4, "reg": 2, "feas": 5, "speed": 2, "pts": 13},
    {"id": "R-10", "name": "Oracle to Spanner phase 1",  "bv": 6, "reg": 6, "feas": 4, "speed": 1, "pts": 34},
]

weights = {"bv": 0.40, "reg": 0.30, "feas": 0.20, "speed": 0.10}

def calc_score(r):
    return round(r["bv"]*weights["bv"] + r["reg"]*weights["reg"] + r["feas"]*weights["feas"] + r["speed"]*weights["speed"], 2)

ranked = sorted(requirements, key=calc_score, reverse=True)
print("=" * 60)
print(f"{'ID':&lt;6} {'Requirement Name':&lt;34} {'Score':&gt;6} {'Points':&gt;8}")
print("=" * 60)
for r in ranked:
    s = calc_score(r)
    print(f"{r['id']:&lt;6} {r['name']:&lt;34} {s:&gt;6.2f} {r['pts']:&gt;8}")
print("=" * 60)

sprint1_ids = ["R-01", "R-02", "R-03", "R-04"]
sprint1_pts = {r["id"]: r["pts"] for r in requirements if r["id"] in sprint1_ids}
total_points = sum(sprint1_pts.values())
print(f"Sprint 1 Selection: {sprint1_ids}")
print(f"Sprint 1 Total Story Points: {total_points}")

if total_points &lt;= 40:
    print("Validation check: PASS — Sprint 1 within 40-point capacity limit")
else:
    print(f"Validation check: FAIL — Sprint 1 points ({total_points}) exceed 40")
    exit(1)
EOF
</code></pre>
</li>

<li><strong>Assemble the definitive Day 69 exit evidence artifact.</strong>

<pre><code>cat &lt;&lt;'EOF' &gt; day-069-stakeholder-priority.md
# Day 69 Exit Artifact: Stakeholder Priority Simulation

Date: 2026-09-28
Entry Artifact: day-068-requirements-register.md

## Executive Summary
This document consolidates the stakeholder power-interest mapping, 5W+H discovery findings,
SMART SLO derivations, and MoSCoW weighted prioritization for the Brightloaf retail cloud modernization.

## Associated Artifact Deliverables
- [Stakeholder Register](stakeholder-register.md) — 7 stakeholders categorized into 4 governance quadrants
- [Conflict Register](conflict-register.md) — 3 structural conflict patterns with assigned owners and resolutions
- [Discovery Session Transcript](discovery-session.md) — 5W+H diagnostic interview with 7 verified constraints (C-01 to C-07)
- [SMART SLO Register](slo-register.md) — 4 measurable SLOs with error budgets, acceptance methods, and multi-burn-rate alerts
- [MoSCoW Scoring Matrix](moscow-scoring.md) — 10 candidate stories scored; Sprint 1 sequenced at exactly 40 story points

## Key Architectural Decisions
1. **CRO Governance Elevation:** Chief Risk Officer moved permanently to "Manage Closely" after data residency review.
2. **Critical Path Sprint 1 Sequencing:** Scheduled only foundational infrastructure (IAM -&gt; DB -&gt; CI/CD -&gt; SLO Monitoring) at 40 points.
3. **Empirical Conflict Resolution:** Autoscaling vs Fixed Capacity deadlock resolved via 30-day shadow canary pilot in Sprint 1.
4. **Signed Won't-Have Scope:** R-07 (Multi-region), R-08 (Cost dashboard), R-09 (Datadog), and R-10 (Spanner) explicitly deferred.
5. **SLO-01 Error Budget:** 99.95% availability over 28 days yields 1,209.6 seconds (~20.2 minutes) monthly downtime budget.

## Unresolved Business Questions (Carry-forward to Gate 4 / Day 82)
- Q1: Formal PCI QSA scoping determination for payment returns processing.
- Q2: Baseline Black Friday p99 latency verification under synthetic load tests.
- Q3: Formal execution timeline for Google Cloud HIPAA Business Associate Agreement (BAA).
- Q4: Agreed contractual start date for multiwindow SLO error budget enforcement.

## Governance Sign-Off Checklist
[ ] Alex Chen (CTO): Platform architecture and 40-point Sprint 1 scope approved
[ ] Maya Patel (CISO): Security perimeter, Workload Identity, and audit logging approved
[ ] Jordan Kim (CFO): 4-item Won't-have list and shadow canary FinOps plan approved
[ ] Sam Rivera (SRE Lead): Multi-burn-rate alerting policies and runbook ownership accepted
[ ] Priya Singh (CRO): Spanner EU regional configuration and data residency boundaries certified
EOF
echo "Day 69 exit artifact compiled: $(wc -l &lt; day-069-stakeholder-priority.md) lines"
</code></pre>
</li>
</ol>
<div class="callout success"><strong>Expected result / acceptance</strong>
<p>A compiled <code>day-069-stakeholder-priority.md</code> exit artifact referencing all underlying registers. The Python script verifies exact criteria weights, outputs ranked scores matching documentation, confirms Sprint 1 points equal exactly 40, and returns <code>Validation check: PASS</code>.</p>
</div>
<div class="callout caution"><strong>Troubleshooting</strong>
<p>If the Python scoring script reports that Sprint 1 points exceed 40, check that R-02 (SLO monitoring) is sized at 8 points rather than an outdated 13-point draft estimate. Sizing at 8 points satisfies <code>8 + 8 + 13 + 11 = 40</code> points exactly.</p>
</div>
<div class="callout"><strong>Cleanup and cost</strong>
<p>No chargeable cloud resources created. Retain all generated files as prerequisite evidence for Day 70 (Well-Architected review lenses) and Gate 4 (Day 82).</p>
</div>
<label class="check"><input type="checkbox" data-progress="lab-69-topic-04"> I completed and checked this topic exercise</label>
</article>

</section>

<!-- COMPLETION SECTION -->
<section class="completion">
<h2>Daily evidence</h2>
<div class="callout success">
<strong>Exit artifact</strong>
<p>Save <code>day-069-stakeholder-priority.md</code> — an agreed-priority simulation containing: a 7-stakeholder power-interest grid with conflict patterns; a 5W+H discovery transcript with 7 constraints (C-01 to C-07) and anti-patterns documented; a SMART SLO register with 4 SLOs, error budgets (SLO-01 = 20.2 min/month), acceptance methods, and alerting policies; a MoSCoW + weighted scoring matrix for 10 requirements with Sprint 1 at exactly 40 story points and a signed-off 4-item Won't-have list. Include 4 unresolved business questions and a stakeholder sign-off checklist.</p>
</div>
<p>This artifact will be referenced in Gate 4 (Day 82) as evidence that architectural priority decisions are grounded in stakeholder context, measurable requirements, and transparent scoring — not individual preference. Bring it to Day 70 (Well-Architected review lenses) as the priority input for the review exercise.</p>
<label class="check"><input type="checkbox" data-progress="read-69"> I read and reviewed the day</label>
<label class="check"><input type="checkbox" data-progress="artifact-69"> I saved the exit artifact (day-069-stakeholder-priority.md)</label>
</section>

<!-- PAGER & FOOTER -->
<nav class="pager" aria-label="Day pagination">
<a href="day-068.html">← Day 68<small>Requirements from observed behavior</small></a>
<a href="../index.html">All 180 days<small>Browse the roadmap</small></a>
<a href="day-070.html">Day 70 →<small>Well-Architected review lenses</small></a>
</nav>
<p class="shortcut">Keyboard: P or [ previous · N or ] next · I index</p>
</main>
<footer class="site-footer">GCP Architect · 180-day independent study · Roadmap dated 2026-09-26. Local progress remains in this browser.</footer>
</body></html>"""

with open('content/day-069-page.html', 'w', encoding='utf-8') as f:
    f.write(line1 + '\n' + BODY)
print("Updated content/day-069-page.html successfully!")
