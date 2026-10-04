"""Day 19 generation module: Sources, access dates, overviews, questions, and visual imports."""

from scratch.day_019_svgs import (
    FIG_19_1_HTML,
    FIG_19_2_HTML,
    FIG_19_3_HTML,
    FIG_19_4_HTML,
    FIG_19_5_HTML
)

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'Google Cloud Shell Documentation: Persistent disk storage (accessed 2026-10-04)',
        'https://cloud.google.com/shell/docs/how-cloud-shell-works#persistent_disk_storage'
    ),
    'topic-02': (
        'Google Cloud SDK Documentation: Multiple configurations (accessed 2026-10-04)',
        'https://cloud.google.com/sdk/docs/configurations#multiple_configurations'
    ),
    'topic-03': (
        'Google Cloud SDK Documentation: Default components (accessed 2026-10-04)',
        'https://cloud.google.com/sdk/docs/components#default_components'
    )
}

PART1_HTML_DATA = {
    'topic-01': {
        'title': 'Cloud Shell (persistent 5 GB home directory, preinstalled tools)',
        'keyword': 'Google Cloud Shell',
        'overview': (
            '<strong class="keyword">Google Cloud Shell</strong> provisions a browser-based, managed Debian Linux '
            'execution environment equipped with a persistent 5 GB $HOME directory, preinstalled developer toolchains, '
            'and ambient Google authentication. It provides an instant administrative terminal directly within the '
            'Google Cloud Console, isolating developer sessions while enforcing strict storage persistence boundaries.'
        ),
        'preview': (
            'An engineer authored automated scripts in ephemeral container storage during an urgent troubleshooting session, '
            'only to have all uncommitted tooling wiped when the 20-minute inactivity timeout recycled the container. '
            'The business suffered a multi-hour delay in incident triage and lost operational automation due to confusing '
            'ephemeral container root storage with the persistent home directory.'
        ),
        'questions': [
            'How does Cloud Shell decouple container runtime lifecycle from user home persistence, and what specific storage limits (5 GB $HOME, 120-day unmounted deletion policy) govern session durability?',
            'In what enterprise scenarios should a cloud architect mandate local workstation CLI configurations or Compute Engine bastion hosts over browser-based Cloud Shell sessions?'
        ]
    },
    'topic-02': {
        'title': 'Install and configure <kbd>gcloud</kbd> locally (<kbd>gcloud init</kbd>, <kbd>gcloud config</kbd>, named…',
        'keyword': 'Local gcloud CLI Configuration',
        'overview': (
            '<strong class="keyword">Local gcloud CLI Configuration</strong> enables cloud architects to manage multiple '
            'isolated Google Cloud environments through named configurations, switching contexts atomically without '
            'leaking credentials across projects. The SDK resolves parameter properties through a strict four-tier '
            'precedence hierarchy that dictates whether flags, environment variables, or profile settings govern execution.'
        ),
        'preview': (
            'A platform engineer executed an infrastructure deletion script in a sandbox terminal where an ambient environment '
            'variable had been left set to the production project. '
            'Because environment variables silently override active named configurations without warning, production database '
            'instances were deleted and caused a severe customer-facing outage.'
        ),
        'questions': [
            'How does the gcloud CLI resolve property precedence across command-line flags, environment variables, active named configurations, and default properties?',
            'What architectural governance mechanisms (such as context-aware shell prompts, CI/CD wrapper assertions, and IAM privilege boundaries) reliably prevent accidental project switching?'
        ]
    },
    'topic-03': {
        'title': 'Other CLIs',
        'keyword': 'Specialized Cloud Command-Line Tools',
        'overview': (
            '<strong class="keyword">Specialized Cloud Command-Line Tools</strong> including <kbd>gcloud storage</kbd>, '
            '<kbd>bq</kbd>, and <kbd>kubectl</kbd> provide domain-optimized interfaces for object storage, analytical data '
            'warehousing, and container orchestration across Google Cloud. Each tool maintains its own distinct configuration '
            'store, creating a hazardous context decoupling risk if target projects and clusters are not actively synchronized.'
        ),
        'preview': (
            'A developer switched their gcloud CLI context to a development sandbox and executed a Kubernetes deletion '
            'command without realizing that kubeconfig remained connected to production. '
            'The production order-processing namespace was terminated because kubectl cluster contexts operate completely '
            'decoupled from ambient gcloud configuration state.'
        ),
        'questions': [
            'What specific architectural and throughput advantages (parallel composite uploads, C++ fast-path shim) does gcloud storage deliver over legacy gsutil?',
            'How can cloud platform engineers implement a unified preflight verification script that asserts project, identity, and cluster target consistency across gcloud, bq, and kubectl before permitting mutating commands?'
        ]
    }
}

def render_part1_html():
    cards = []
    for key, val in PART1_HTML_DATA.items():
        card = f'''<article class="topic-card overview" id="{key}-overview">
<h3>{val['title']}</h3>
<p>{val['overview']}</p>
<p><strong class="side-heading">Why today:</strong> Day 19 establishes command-line workstation standards, persistent identity validation, and context switching safety required to operate securely across multi-project environments.</p>
<p><strong class="side-heading">Where it sits:</strong> Sits on developer workstations, Cloud Shell containers, and CI/CD runners dispatching authenticated API requests to Google Cloud.</p>
<p class="problem-preview">Problem preview: {val['preview']}</p>
</article>'''
        cards.append(card)
    return "\n\n".join(cards)

def render_completion_html():
    return '''<div class="completion-box" id="completion-box-019">
<h3>Day 19 Acceptance Checklist</h3>
<ul class="checklist">
<li><input type="checkbox" id="check-19-1"> <label for="check-19-1">Cloud Shell boundaries verified: mapped 5 GB persistent $HOME disk versus ephemeral 40 GB container root, 20m idle timeout, and $HOME/.customize_environment hook.</label></li>
<li><input type="checkbox" id="check-19-2"> <label for="check-19-2">Named configurations operational: authored isolated profiles (brightloaf-sandbox, brightloaf-prod) and verified atomic switching via gcloud config configurations activate.</label></li>
<li><input type="checkbox" id="check-19-3"> <label for="check-19-3">Precedence hierarchy proven: verified that CLI flags override environment variables, and CLOUDSDK_* variables silently override active named profiles.</label></li>
<li><input type="checkbox" id="check-19-4"> <label for="check-19-4">Context decoupling mastered: proved that kubectl kubeconfig and bq config stores are independent of gcloud and require explicit synchronization.</label></li>
<li><input type="checkbox" id="check-19-5"> <label for="check-19-5">Drift prevention enforced: configured context-aware shell prompts (PS1) and mandated explicit Tier 1 --project parameter flags in all runbooks.</label></li>
<li><input type="checkbox" id="check-19-6"> <label for="check-19-6">Exit evidence artifact verified: authored authoritative Day 19 CLI Configuration, Identity Verification, and Target Environment Controls Artifact.</label></li>
</ul>
<div class="completion-actions" style="margin-top:1.5rem;display:flex;gap:1rem;">
<button class="btn btn-primary" id="btn-read-019" onclick="this.classList.toggle('completed');this.textContent=this.classList.contains('completed')?'✓ Read Day 19 Completed':'Mark Day 19 as Read';">Mark Day 19 as Read</button>
<button class="btn btn-secondary" id="btn-artifact-019" onclick="this.classList.toggle('verified');this.textContent=this.classList.contains('verified')?'✓ Exit Artifact Verified':'Verify Exit Artifact';">Verify Exit Artifact</button>
</div>
</div>'''
