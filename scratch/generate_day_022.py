"""Day 22 generation module: Sources, access dates, overviews, questions, and render functions."""

from scratch.day_022_svgs import (
    FIG_22_1_HTML,
    FIG_22_2_HTML,
    FIG_22_3_HTML,
    FIG_22_4_HTML
)

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'Google Cloud Resource Manager Documentation: Benefits of the organization resource (accessed 2026-10-04)',
        'https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#benefits_of_the_organization_resource'
    ),
    'topic-02': (
        'Google Cloud Resource Manager Documentation: Tags and labels (accessed 2026-10-04)',
        'https://cloud.google.com/resource-manager/docs/tags/tags-overview#tags_and_labels'
    )
}

PART1_HTML_DATA = {
    'topic-01': {
        'title': 'Resources and inheritance (policies flow downward and are additive for IAM)',
        'keyword': 'Hierarchical IAM Policy Inheritance and Additive Union Flow',
        'overview': (
            '<strong class="keyword">Hierarchical IAM Policy Inheritance and Additive Union Flow</strong> govern access control '
            'across the Google Cloud resource hierarchy. Identity and Access Management policies flow strictly downward from the '
            'Organization apex through Folders to Projects and individual Leaf Resources. The fundamental mathematical principle '
            'is that IAM allow policies are additive: effective permissions on a target resource represent the union of all role '
            'bindings assigned at the resource itself, its parent project, and every ancestor folder up to the organization root. '
            'Standard allow bindings have zero subtractive capability: an allow permission granted at an ancestor cannot be revoked '
            'or restricted by a child binding, requiring explicit IAM Deny policies to establish non-negotiable negative boundaries.'
        ),
        'preview': (
            'A franchise infrastructure administrator assigns the broad roles/editor role to an external contractor group at the parent Analytics folder level while attempting to restrict them with a roles/viewer role on the child production order project. '
            'Because IAM allow bindings are strictly additive across the hierarchy, the contractor automation script retained full write privileges, accidentally dropping the primary production fulfillment queue table and halting morning bakery order processing across 450 franchise stores.'
        ),
        'questions': [
            'Why does the mathematical union evaluation of Google Cloud IAM allow policies make it impossible for a project-level binding to revoke permissions inherited from an ancestor folder?',
            'How do IAM Deny policies enforce non-negotiable negative security constraints down the resource hierarchy, and what is their evaluation precedence relative to allow rules?',
            'What specific architectural strategies—such as folder environment segregation and Google Groups delegation—protect enterprise estates from accidental privilege escalation?'
        ]
    },
    'topic-02': {
        'title': 'Labels vs tags vs network tags (three different things, often confused)',
        'keyword': 'Three-Plane Metadata Taxonomy: Labels, Tags, and Network Tags',
        'overview': (
            '<strong class="keyword">Three-Plane Metadata Taxonomy: Labels, Tags, and Network Tags</strong> categorizes the three '
            'distinct metadata mechanisms in Google Cloud across their respective architectural control planes. Resource Labels '
            'are client-managed key-value strings attached directly to individual resources for cost attribution, BigQuery billing '
            'export grouping, and script filtering. Resource Manager Tags are strongly typed, centrally governed resources created '
            'under the Organization or Folder tree, inherited down the container hierarchy, and evaluated within IAM Conditions and '
            'Organization Policies. Network Tags are ephemeral, unvalidated string attributes attached strictly to Compute Engine VM '
            'instances for VPC firewall packet filtering and route matching.'
        ),
        'preview': (
            'A DevOps automation script applies resource labels with role: order-db to production database virtual machines, expecting VPC firewall rules targeting the order-db tag to restrict inbound connections to port 5432. '
            'Because VPC firewalls evaluate network tags rather than resource labels, the database instances received zero tag-based firewall filtering and defaulted to an open internal subnet rule, exposing raw customer payment tokens to a compromised staging development container and triggering an immediate regulatory audit.'
        ),
        'questions': [
            'What are the critical architectural boundaries separating Resource Labels, Resource Manager Tags, and Network Tags across billing, IAM governance, and VPC firewall data planes?',
            'Why are Resource Labels completely ineffective for VPC packet filtering or IAM access control, and what security risks emerge when engineers conflate them?',
            'How do Resource Manager Tags integrate with Common Expression Language (CEL) conditions in IAM policies and Organization Policies to enforce conditional access down the resource tree?'
        ]
    }
}

def render_part1_html():
    cards = []
    for key in ['topic-01', 'topic-02']:
        d = PART1_HTML_DATA[key]
        q_items = ''.join(f'<li>{q}</li>' for q in d['questions'])
        cards.append(f'''<article class="topic-card" id="{key}-overview">
<h3>{d['title']}</h3>
<p><strong class="side-heading">What it is:</strong> {d['overview']}</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> {d['preview']}</p>
<div class="study-prompts">
<p><strong class="side-heading">Architectural questions for study:</strong></p>
<ul>
{q_items}
</ul>
</div>
</article>''')
    return '\n'.join(cards)

def render_completion_html():
    return '''<div class="completion-card">
<h3>Day 22 Completion Checklist &amp; Verification Evidence</h3>
<p>To satisfy the Day 22 exit criteria, verify the following operational and architectural evidence artifacts:</p>
<ul class="checklist">
<li><input type="checkbox" id="check-22-1"> <label for="check-22-1">Additive IAM inheritance mathematically evaluated: modeled cumulative permissions across Organization, Folder, and Project tiers.</label></li>
<li><input type="checkbox" id="check-22-2"> <label for="check-22-2">IAM Deny guardrails evaluated: demonstrated that Deny policies take precedence over inherited allow bindings and cannot be overridden by child projects.</label></li>
<li><input type="checkbox" id="check-22-3"> <label for="check-22-3">Three-plane metadata taxonomy validated: mapped distinct boundaries for Resource Labels, Resource Manager Tags, and Compute Engine Network Tags.</label></li>
<li><input type="checkbox" id="check-22-4"> <label for="check-22-4">VPC packet filtering rules verified: asserted that firewall rules evaluate Network Tags and Secure Tags rather than Resource Labels.</label></li>
<li><input type="checkbox" id="check-22-5"> <label for="check-22-5">Resource Manager Tag IAM condition verified: evaluated CEL expressions for tag-based conditional role binding down the hierarchy.</label></li>
<li><input type="checkbox" id="check-22-6"> <label for="check-22-6">Exit evidence artifact generated: saved authoritative inheritance calculation and tagging taxonomy guide at <code>scratch/day-022-inheritance-and-tagging-guide.md</code>.</label></li>
</ul>
</div>'''
