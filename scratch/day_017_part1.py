"""Part 1 and top-level HTML content for Day 17."""

PART1_INTRO = (
    "A rigorous synthesis of Block 1 foundations (Days 1–16) covering end-to-end "
    "request processing, POSIX system mechanics, network protocols, relational state persistence, "
    "and the five-dimension Gate 1 evaluation framework."
)

PART2_INTRO = (
    "An exhaustive technical deep dive into foundational request path mechanics, relational "
    "ACID transaction rollbacks, failure taxonomy, weak explanation remediation, and the "
    "Gate 1 objective scoring rubric."
)

PART3_INTRO = (
    "Two diagnostic operational case studies analyzing an overlapping CIDR subnet routing collision "
    "with DNS search loops, and an unconstrained message replay incident violating the duplicate "
    "fulfillment invariant."
)

PART4_INTRO = (
    "Hands-on executable laboratory exercises reproducing the end-to-end local request flow, "
    "proving atomic SQL rollbacks, conducting a five-dimension rubric audit, and authoring the "
    "scored Gate 1 checklist and pass decision."
)

EXIT_SUMMARY = (
    "Completion of Day 17 produces verified exit evidence consisting of a scored Gate 1 checklist, "
    "corrected foundation evidence, and an explicit pass or repeat decision recorded in "
    "scratch/day-017-g1-checklist.md."
)

PART1_HTML = """<article class="topic-card" id="topic-01-overview">
<h3>Prerequisite review and remediation</h3>
<p><strong class="side-heading">What it is:</strong> <strong class="keyword">Foundation Synthesis and Prerequisite Remediation</strong> conducts a comprehensive review and systematic repair of the core operating system, networking, and data persistence primitives mastered across Block 1 (Days 1–16). Before advancing to Google Cloud identity and resource hierarchy in Block 2, architects must demonstrate flawless end-to-end mastery: tracing an incoming request through DNS resolution, IP subnet routing, TLS 1.3 termination, POSIX containerized process execution, Twelve-Factor configuration and structured logging, and ACID-compliant relational transactions. Checkpoint days strictly forbid the introduction of new cloud services or external concepts, focusing entirely on recalling foundational invariants and systematically upgrading any shallow, ambiguous, or incomplete explanations from prior lab exercises.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> An e-commerce bakery ordering service experiences intermittent 10,000 ms database connection timeouts following an uncoordinated container network reconfiguration. Because engineers lacked end-to-end visibility into overlapping RFC 1918 CIDR allocations and DNS search domain loops, morning bread orders across 42 commercial hubs stalled, halting delivery schedules and triggering customer SLA penalties.</p>
<div class="study-prompts">
<p><strong class="side-heading">Architectural questions for study:</strong></p>
<ul>
<li>How do lower-level operating system and networking primitives (POSIX signals, cgroups, TCP sockets, and DNS resolvers) dictate the reliability boundaries of higher-level cloud managed services?</li>
<li>Why does relational state persistence require schema-level unique constraints and atomic transaction boundaries rather than relying on application-tier or message-broker deduplication?</li>
<li>What specific architectural hazards emerge when technical teams advance to cloud infrastructure without proving reproducible mastery over foundational networking and rollback mechanisms?</li>
</ul>
</div>
</article>
<article class="topic-card" id="topic-02-overview">
<h3>Use the matching gate criteria in the Gates section</h3>
<p><strong class="side-heading">What it is:</strong> <strong class="keyword">Gate 1 Evaluation Criteria and Pass/Repeat Governance</strong> applies the formal five-dimension assessment rubric from the Gates section to evaluate readiness for Block 2 (Cloud environment and identity). Candidates evaluate their cumulative Block 1 portfolio across Correctness (technical and mathematical precision), Traceability (mapping implementations to architectural requirements), Evidence Quality (reproducible timestamped outputs and exit codes), Recovery Reasoning (predicting failure modes and verifying clean rollbacks), and Communication (concise business and operational trade-off framing). To secure an authoritative PASS decision, every dimension must score at least 2 out of 3, with a composite score of at least 12 out of 15, and non-negotiable verification that the duplicate fulfillment invariant (&le; 1 physical fulfillment per unique order ID) is preserved.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> An infrastructure candidate attempts to advance to cloud identity topics despite submitting unverified database rollback logs and vague network routing explanations. Without enforcing rigorous rubric gating, subtle gaps in transaction isolation and CIDR subnet math compound into critical security vulnerabilities and production data corruption during cloud landing zone deployment.</p>
<div class="study-prompts">
<p><strong class="side-heading">Architectural questions for study:</strong></p>
<ul>
<li>How does a quantitative five-dimension rubric prevent subjective bias and technical debt accumulation during architectural capability assessments?</li>
<li>What are the non-negotiable operational criteria that distinguish an acceptable architectural artifact from an unverified or hand-waving explanation?</li>
<li>Why must an architectural checkpoint enforce an explicit pass or repeat decision, and how does targeted remediation repair identified weaknesses without discarding valid work?</li>
</ul>
</div>
</article>"""

COMPLETION_HTML = """<div class="completion-card">
<h3>Day 17 Completion Checklist &amp; Gate 1 Exit Evidence</h3>
<p>To satisfy the Gate 1 exit criteria and authorize progression to Block 2, verify the following operational and architectural evidence artifacts:</p>
<ul class="checklist">
<li><input type="checkbox" id="check-17-1"> <label for="check-17-1">End-to-end request flow reproduced locally: verified DNS lookup, TCP/HTTP intake, POSIX process execution, and Twelve-Factor validation.</label></li>
<li><input type="checkbox" id="check-17-2"> <label for="check-17-2">Relational transaction rollback demonstrated: proved atomic rollback without orphaned child rows or phantom state.</label></li>
<li><input type="checkbox" id="check-17-3"> <label for="check-17-3">Duplicate fulfillment invariant verified: demonstrated that schema UNIQUE(order_id) constraints suppress duplicate message replays (&le; 1 physical fulfillment).</label></li>
<li><input type="checkbox" id="check-17-4"> <label for="check-17-4">Prior Block 1 artifacts audited: systematically reviewed exit evidence from Day 5 (Shell), Day 8 (Networking), Day 10 (State), and Day 16 (SQL).</label></li>
<li><input type="checkbox" id="check-17-5"> <label for="check-17-5">Weakest explanation identified and repaired: authored comprehensive technical remediation replacing ambiguous claims with verified mechanisms.</label></li>
<li><input type="checkbox" id="check-17-6"> <label for="check-17-6">Five-dimension rubric scored: evaluated all dimensions (Correctness, Traceability, Evidence Quality, Recovery Reasoning, Communication) with every score &ge; 2 and total &ge; 12/15.</label></li>
<li><input type="checkbox" id="check-17-7"> <label for="check-17-7">Authoritative Gate 1 checklist generated: saved scored audit and formal pass decision at <code>scratch/day-017-g1-checklist.md</code>.</label></li>
</ul>
</div>"""
