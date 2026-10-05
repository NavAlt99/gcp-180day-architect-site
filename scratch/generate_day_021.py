"""Day 21 generation module: Sources, access dates, overviews, questions, and visual imports."""

from scratch.day_021_svgs import (
    FIG_21_1_HTML,
    FIG_21_2_HTML,
    FIG_21_3_HTML,
    FIG_21_4_HTML,
    FIG_21_5_HTML
)

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'Google Cloud Resource Manager Documentation: The organization resource (accessed 2026-10-04)',
        'https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#organizations'
    ),
    'topic-02': (
        'Google Cloud Resource Manager Documentation: The folder resource (accessed 2026-10-04)',
        'https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#folders'
    ),
    'topic-03': (
        'Google Cloud Resource Manager Documentation: The project resource (accessed 2026-10-04)',
        'https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#projects'
    )
}

PART1_HTML_DATA = {
    'topic-01': {
        'title': 'Organization node (tied to Cloud Identity or Google Workspace domain)',
        'keyword': 'Organization Node and Cloud Identity Architecture',
        'overview': (
            '<strong class="keyword">Organization Node and Cloud Identity Architecture</strong> establish the root anchor '
            'of trust for all Google Cloud resources. The Organization resource represents an enterprise customer and is bound '
            'one-to-one with a DNS-verified Google Workspace or Cloud Identity domain. It provides centralized visibility and control '
            'over all descendant folders, projects, and resources, enabling security teams to enforce Organization Policies, '
            'audit centralized access logs, and prevent the creation of unmanaged orphan projects.'
        ),
        'preview': (
            'A contractor provisioned a cloud project using a personal Gmail account and launched untagged database instances for rapid testing. '
            'Because the orphan project operated outside corporate organization node boundaries, security teams lacked visibility into unencrypted storage buckets and experienced data recovery failure when the contractor departed.'
        ),
        'questions': [
            'How does the one-to-one binding between a Cloud Identity domain and an Organization node enforce administrative boundaries across enterprise cloud estates?',
            'What specific governance capabilities—such as Organization Policies, Resource Manager IAM roles, and centralized billing—are inaccessible when projects lack an Organization parent?',
            'How does the Organization Administrator role separate directory lifecycle governance from individual cloud workload management?'
        ]
    },
    'topic-02': {
        'title': 'Folders (mapping to departments, environments or teams)',
        'keyword': 'Folder Hierarchy and Policy Inheritance',
        'overview': (
            '<strong class="keyword">Folder Hierarchy and Policy Inheritance</strong> provide logical grouping mechanisms '
            'below the Organization node, allowing enterprises to organize projects by business unit, department, or lifecycle environment. '
            'IAM permissions and Organization Policies inherit downward through the folder tree additively: a role granted at a parent folder '
            'cannot be revoked or restricted at a child project. Structuring folders into clean environment boundaries (such as Production '
            'versus Non-Production) prevents privilege escalation and isolates sensitive production infrastructure.'
        ),
        'preview': (
            'An operations team placed both staging and production projects under a shared engineering folder and granted developers the editor role at the folder level. '
            'During routine staging maintenance, a junior engineer accidentally selected the production project from the ambient console picker and dropped a core transactional database.'
        ),
        'questions': [
            'Why does the additive nature of Google Cloud IAM inheritance require placing production and staging workloads into sibling folders rather than nested hierarchies?',
            'What are the trade-offs between an environment-first folder structure (Production vs Non-Production) and a business-unit-first structure (Retail vs Wholesale)?',
            'How do Organization Policy inheritance rules (such as policy merging versus explicit inheritance override) govern security guardrails across folder subtrees?'
        ]
    },
    'topic-03': {
        'title': 'Projects',
        'keyword': 'Project Identifiers and Operating Boundaries',
        'overview': (
            '<strong class="keyword">Project Identifiers and Operating Boundaries</strong> define the foundational unit of '
            'resource ownership, billing attribution, API enablement, and IAM boundary enforcement in Google Cloud. Every project is '
            'defined by a triad of identifiers: a mutable, human-friendly Project Name; a globally unique, immutable, customer-selected '
            'Project ID; and a globally unique, immutable, Google-assigned numerical Project Number. Conflating these three identifiers '
            'in automation runbooks or IAM bindings causes critical operational failures, particularly when configuring Google-managed service agent identities.'
        ),
        'preview': (
            'A DevOps engineer configured cross-project Cloud KMS decryption permissions for an automated Pub/Sub topic using the human-readable project display name. '
            'Because Google-managed service agents require the immutable 12-digit project number rather than the display name, the decryption binding failed and thousands of incoming bakery orders were routed to dead-letter queues.'
        ),
        'questions': [
            'What are the critical architectural differences between Project ID, Project Name, and Project Number across billing, API endpoints, and IAM bindings?',
            'Why do Google-managed service agent email addresses (such as service-[PROJECT_NUMBER]@gcp-sa-pubsub.iam.gserviceaccount.com) strictly require the project number rather than the project ID?',
            'What operational and architectural boundaries (such as VPC networks, billing accounts, and quota pools) are strictly isolated at the project boundary?'
        ]
    }
}

def render_part1_html():
    cards = []
    for key in ['topic-01', 'topic-02', 'topic-03']:
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
<h3>Day 21 Completion Checklist &amp; Verification Evidence</h3>
<p>To satisfy the Day 21 exit criteria, verify the following operational and architectural evidence artifacts:</p>
<ul class="checklist">
<li><input type="checkbox" id="check-21-1"> <label for="check-21-1">Organization root node audited: inspected directory domain binding, primary domain verification, and root IAM roles.</label></li>
<li><input type="checkbox" id="check-21-2"> <label for="check-21-2">Multi-tier folder hierarchy designed: segregated Production and Non-Production environments to prevent IAM privilege leakage.</label></li>
<li><input type="checkbox" id="check-21-3"> <label for="check-21-3">Project identifiers triad validated: mapped Project Name, Project ID, and Project Number, and verified Google-managed service agent derivation.</label></li>
<li><input type="checkbox" id="check-21-4"> <label for="check-21-4">Additive IAM policy inheritance calculated: verified that folder-level grants inherit to child projects without downward restriction.</label></li>
<li><input type="checkbox" id="check-21-5"> <label for="check-21-5">Landing zone architecture documented: authored authoritative landing-zone draft with stable IDs, environment boundaries, and operating responsibilities.</label></li>
<li><input type="checkbox" id="check-21-6"> <label for="check-21-6">Exit evidence artifact generated: saved verified landing-zone design at <code>scratch/day-021-landing-zone-draft.md</code>.</label></li>
</ul>
</div>'''
