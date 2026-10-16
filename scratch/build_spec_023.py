#!/usr/bin/env python3
"""Build complete durable specification for Day 23: Organization policies and lifecycle."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent

# Read SVGs from scratch/day023/
fig1 = (ROOT / 'scratch/day023/fig1.html').read_text().strip()
fig2 = (ROOT / 'scratch/day023/fig2.html').read_text().strip()
fig3 = (ROOT / 'scratch/day023/fig3.html').read_text().strip()
fig4 = (ROOT / 'scratch/day023/fig4.html').read_text().strip()
fig5 = (ROOT / 'scratch/day023/fig5.html').read_text().strip()

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'Google Cloud Resource Manager Documentation: The project resource (accessed 2026-10-04)',
        'https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#projects'
    ),
    'topic-02': (
        'Google Cloud Resource Manager Documentation: The folder resource (accessed 2026-10-04)',
        'https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#folders'
    ),
    'topic-03': (
        'Google Cloud Organization Policy Documentation: Constraints (accessed 2026-10-04)',
        'https://cloud.google.com/resource-manager/docs/organization-policy/overview#constraints'
    ),
}

# ─────────────────────────────────────────────────────────────────────────────
# PART 1 OVERVIEW HTML
# ─────────────────────────────────────────────────────────────────────────────
PART1_HTML = '''<article class="topic-card" id="topic-01-overview">
<h3>Project lifecycle</h3>
<p><strong class="keyword">Project Lifecycle and Lien Protection</strong> govern the deterministic operational state transitions of Google Cloud project containers from initial provisioning through active utilization to permanent retirement. A project progresses through three distinct lifecycle states in Cloud Resource Manager: <code>ACTIVE</code> (operational workloads, enabled APIs, and active billing), <code>DELETE_REQUESTED</code> (a mandatory 30-day soft recovery window where compute instances halt, external IPs detach, and billing decouples, while persistent disks and configuration metadata remain frozen in storage), and <code>DELETED</code> (permanent cryptographic erasure across storage systems and irreversible retirement of the globally unique Project ID). To protect mission-critical production workloads against automated script errors or administrative accidents, enterprise architects enforce <strong>Project Liens</strong> (<code>resourcemanager.lien</code>) that programmatically block deletion requests at the admission boundary until explicitly released by authorized governance principals.</p>
<p><strong class="side-heading">Why today:</strong> Decommissioning automation, CI/CD pruning scripts, and operator errors routinely target projects for teardown; understanding project liens and the 30-day recovery window prevents permanent data loss and guarantees rapid operational restoration.</p>
<p><strong class="side-heading">Where it sits:</strong> Sits at the container management boundary within Cloud Resource Manager, directly downstream of Day 21 project identifiers and Day 22 additive inheritance rules.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> An automated infrastructure cleanup script targeting ephemeral test environments accidentally executes a project shutdown API call against BrightLoaf's unshielded shared artifact registry project. Because no protective project lien was configured, the project immediately entered pending deletion and detached service account credentials, halting automated container deployments and blocking critical hotfixes across 450 franchise bakery point-of-sale systems during peak morning trading.</p>
<div class="study-prompts">
<p><strong class="side-heading">Architectural questions for study:</strong></p>
<ul>
<li>What exact infrastructure events occur when a project enters the <code>DELETE_REQUESTED</code> state, and why are external static IP reservations released immediately?</li>
<li>How do Project Liens provide non-negotiable deletion protection that even principals holding <code>roles/owner</code> or <code>roles/resourcemanager.organizationAdmin</code> cannot bypass without explicit lien removal?</li>
<li>What operational steps and billing re-linking procedures are required during the 30-day window to restore a soft-deleted project to full production readiness?</li>
</ul>
</div>
</article>
<article class="topic-card" id="topic-02-overview">
<h3>Designing a hierarchy for prod/staging/dev and for multi-team companies</h3>
<p><strong class="keyword">Multi-Tier Resource Hierarchy Architecture</strong> establishes the structural folder topologies beneath the Organization root to balance administrative autonomy, operational agility, and strict environment isolation across enterprise business units. Cloud architects evaluate three foundational topologies: <strong>Environment-First</strong> (top-level folders represent lifecycle stages such as <code>/Production</code>, <code>/Staging</code>, and <code>/Development</code>), <strong>Team-First</strong> (top-level folders represent autonomous business units or product lines such as <code>/Retail-Bakery</code> and <code>/Supply-Chain</code> with environments nested underneath), and <strong>Hybrid Matrix</strong> models. The chosen topology dictates how IAM role bindings propagate additively down the container tree, how centralized Organization Policy guardrails cascade, and how Shared VPC host networks interconnect distributed workloads without cross-environment security leakage.</p>
<p><strong class="side-heading">Why today:</strong> Multi-team enterprises inevitably suffer permission sprawl and security breaches if the resource hierarchy is organized ad-hoc, making deliberate folder design essential before deploying complex workloads.</p>
<p><strong class="side-heading">Where it sits:</strong> Bridges organizational identity from Day 21 with today's Organization Policy guardrails, defining the exact structural pathways along which policies inherit down to leaf projects.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> An engineering team adopts a flat team-first folder structure that places staging and production workloads under a shared departmental container, inadvertently inheriting developer administrative permissions directly into live order processing clusters. A developer running a high-concurrency performance benchmark against an assumed staging endpoint directed millions of synthetic transactions into the production database, exhausting connection pools and causing thousands of retail bakery customers to experience failed checkout screens.</p>
<div class="study-prompts">
<p><strong class="side-heading">Architectural questions for study:</strong></p>
<ul>
<li>Why does the additive nature of Google Cloud IAM inheritance mandate isolating production and non-production workloads into sibling folder branches rather than parent-child hierarchies?</li>
<li>What are the governance, compliance, and billing trade-offs between an Environment-First folder model and a Team-First (Business Unit) folder model?</li>
<li>How do Shared VPC network boundaries and Organization Policy constraint inheritance interact across multi-team folder structures?</li>
</ul>
</div>
</article>
<article class="topic-card" id="topic-03-overview">
<h3>Organization Policy Service (constraints that restrict what can be done, regardless of IAM)</h3>
<p><strong class="keyword">Organization Policy Service Guardrails</strong> provide centralized programmatic governance constraints that enforce non-negotiable security and compliance boundaries across the Google Cloud resource hierarchy. Unlike IAM—which governs identities and evaluates who is authorized to invoke an API—Organization Policies govern cloud resources and define what configurations are legally permitted to exist, regardless of the caller's administrative role. Constraints operate as either <strong>Boolean Constraints</strong> (enforcing binary restrictions such as disabling external IP addresses via <code>constraints/compute.vmExternalIpAccess</code>) or <strong>List Constraints</strong> (enforcing allowed or denied sets of values such as restricting resource deployment locations via <code>constraints/gcp.resourceLocations</code>). Organization policies evaluate at admission time at the API gateway, acting as an absolute programmatic veto that overrides IAM allow bindings.</p>
<p><strong class="side-heading">Why today:</strong> Even the most restrictive IAM least-privilege policies cannot prevent an authorized project administrator or compromised automation pipeline from provisioning workloads with public internet IPs or violating geographic data residency regulations.</p>
<p><strong class="side-heading">Where it sits:</strong> Operates at the admission control boundary of the Google Cloud API gateway, intercepting resource creation and mutation requests before they reach downstream compute, network, or storage control planes.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A data science contractor possessing legitimate project administrative credentials attempts to provision an unshielded compute instance with an ephemeral public IP address in an overseas region to process raw franchise sales records. Lacking centralized organization policy guardrails, the public instance was deployed and immediately detected by automated internet port scanners, exposing unencrypted order transaction logs and triggering an emergency forensic audit for cross-border regulatory compliance violations.</p>
<div class="study-prompts">
<p><strong class="side-heading">Architectural questions for study:</strong></p>
<ul>
<li>How does the admission-time interception of Organization Policy Service differ from IAM evaluation in the Google Cloud API gateway request lifecycle?</li>
<li>What are the structural syntax differences and operational behaviors between Boolean constraints and List constraints across container tiers?</li>
<li>How do inheritance rules—specifically <code>inheritFromParent</code>, policy merging, and explicit overrides—function down nested folder hierarchies, and how do architects safely simulate rollbacks?</li>
</ul>
</div>
</article>'''

# ─────────────────────────────────────────────────────────────────────────────
# COMPLETION HTML
# ─────────────────────────────────────────────────────────────────────────────
COMPLETION_HTML = '''<div class="completion-card">
<h3>Day 23 Completion Checklist &amp; Verification Evidence</h3>
<p>To satisfy the Day 23 exit criteria, verify the following operational and architectural evidence artifacts:</p>
<ul class="checklist">
<li><input type="checkbox" id="check-23-1"> <label for="check-23-1">Project lifecycle state machine modeled: verified transitions across ACTIVE, DELETE_REQUESTED (30-day soft recovery), and permanent DELETED states.</label></li>
<li><input type="checkbox" id="check-23-2"> <label for="check-23-2">Project Lien protection enforced: demonstrated that <code>resourcemanager.projects.delete</code> liens reject deletion calls at the API gateway.</label></li>
<li><input type="checkbox" id="check-23-3"> <label for="check-23-3">Hierarchy topologies benchmarked: modeled Environment-First, Team-First, and Hybrid Matrix folder patterns to prevent cross-environment IAM bleed.</label></li>
<li><input type="checkbox" id="check-23-4"> <label for="check-23-4">Organization Policy admission evaluated: asserted that Boolean and List constraints act as hard vetoes overriding IAM caller roles.</label></li>
<li><input type="checkbox" id="check-23-5"> <label for="check-23-5">Resource prediction matrix executed: verified TEST-01 through TEST-04 predictions for location and external IP constraints with simulated rollback.</label></li>
<li><input type="checkbox" id="check-23-6"> <label for="check-23-6">Exit evidence artifact generated: saved authoritative Organization Policy test and Project Lifecycle report at <code>scratch/day-023-org-policy-test-and-lifecycle-report.md</code>.</label></li>
</ul>
</div>'''

print("Part 1 and Completion HTML ready")
