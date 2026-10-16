import re

with open('scratch/day_data_011.py', 'r') as f:
    text = f.read()

# F1: Split banner text in Figure 11.2
old_f1 = (
    "                          '<text x=\"470\" y=\"340\" fill=\"#fce7f3\" font-size=\"11\" font-weight=\"600\" '\n"
    "                          'text-anchor=\"middle\">Google Cloud Shared Fate: Google provides Security Command Center, '\n"
    "                          'secure blueprints, and posture tooling to actively assist customers in fulfilling their '\n"
    "                          'security duties.</text>\\n'"
)
new_f1 = (
    "                          '<text x=\"470\" y=\"335\" fill=\"#fce7f3\" font-size=\"10\" font-weight=\"600\" '\n"
    "                          'text-anchor=\"middle\">Google Cloud Shared Fate: Google provides Security Command Center, '\n"
    "                          'secure blueprints,</text>\\n'\n"
    "                          '<text x=\"470\" y=\"347\" fill=\"#fce7f3\" font-size=\"10\" font-weight=\"600\" '\n"
    "                          'text-anchor=\"middle\">and posture tooling to actively assist customers in fulfilling their '\n"
    "                          'security duties.</text>\\n'"
)
assert text.count(old_f1) == 1, f"F1 count {text.count(old_f1)}"
text = text.replace(old_f1, new_f1, 1)

# F4: Add linked subtopics to Topic 1 overview
old_f4 = (
    "               '<p class=\"problem-preview\"><strong class=\"side-heading\">Problem preview:</strong> An order ingestion service hosted on a single Compute '\n"
    "               'Engine virtual machine crashes after a manual operating system update breaks local system libraries '\n"
    "               'during peak holiday traffic. The engineering team re-architects the endpoint onto Google Cloud Run, '\n"
    "               'delegating host operating system patching to Google while eliminating 14 hours of potential '\n"
    "               'downtime.</p>\\n'\n"
    "               '</article>\\n'"
)
new_f4 = (
    "               '<p class=\"problem-preview\"><strong class=\"side-heading\">Problem preview:</strong> An order ingestion service hosted on a single Compute '\n"
    "               'Engine virtual machine crashes after a manual operating system update breaks local system libraries '\n"
    "               'during peak holiday traffic. The engineering team re-architects the endpoint onto Google Cloud Run, '\n"
    "               'delegating host operating system patching to Google while eliminating 14 hours of potential '\n"
    "               'downtime.</p>\\n'\n"
    "               '<p><strong class=\"side-heading\">Linked subtopics:</strong></p>\\n'\n"
    "               '<ul><li><a href=\"#topic-01-subtopic-1\">Infrastructure as a Service (IaaS): Virtual Machines, Persistent Disks, and Network Virtualization</a></li>\\n'\n"
    "               '<li><a href=\"#topic-01-subtopic-2\">Platform as a Service (PaaS) and Container as a Service (CaaS): Managed Runtimes and Orchestration</a></li>\\n'\n"
    "               '<li><a href=\"#topic-01-subtopic-3\">Function as a Service (FaaS): Event-Driven Ephemeral Execution</a></li>\\n'\n"
    "               '<li><a href=\"#topic-01-subtopic-4\">Software as a Service (SaaS): Fully Managed Application and Data Solutions</a></li>\\n'\n"
    "               '<li><a href=\"#topic-01-subtopic-5\">The Abstraction Spectrum Decision Matrix: Trade-offs between Operational Control and Development Velocity</a></li></ul>\\n'\n"
    "               '</article>\\n'"
)
assert text.count(old_f4) == 1, f"F4 count {text.count(old_f4)}"
text = text.replace(old_f4, new_f4, 1)

# F5: Add linked subtopics to Topic 2 overview
old_f5 = (
    "               '<p class=\"problem-preview\"><strong class=\"side-heading\">Problem preview:</strong> An engineering team deploying a customer account portal to '\n"
    "               'Cloud Run erroneously assumes that Google Cloud automatically blocks unauthorized public internet '\n"
    "               'requests. Because the team bound allUsers to the run invoker role, unauthenticated internet callers '\n"
    "               'exfiltrate 128,000 sensitive customer records until least privilege OIDC authentication is '\n"
    "               'restored.</p>\\n'\n"
    "               '</article>\\n',"
)
new_f5 = (
    "               '<p class=\"problem-preview\"><strong class=\"side-heading\">Problem preview:</strong> An engineering team deploying a customer account portal to '\n"
    "               'Cloud Run erroneously assumes that Google Cloud automatically blocks unauthorized public internet '\n"
    "               'requests. Because the team bound allUsers to the run invoker role, unauthenticated internet callers '\n"
    "               'exfiltrate 128,000 sensitive customer records until least privilege OIDC authentication is '\n"
    "               'restored.</p>\\n'\n"
    "               '<p><strong class=\"side-heading\">Linked subtopics:</strong></p>\\n'\n"
    "               '<ul><li><a href=\"#topic-02-subtopic-1\">Security OF the Cloud vs Security IN the Cloud: Demarcation of Hardware, Hypervisor, and Tenant Workloads</a></li>\\n'\n"
    "               '<li><a href=\"#topic-02-subtopic-2\">Workload-Specific Responsibility Boundaries across IaaS, PaaS, and SaaS</a></li>\\n'\n"
    "               '<li><a href=\"#topic-02-subtopic-3\">Identity, Access Management (IAM), and Ingress Protection as Customer Invariants</a></li>\\n'\n"
    "               '<li><a href=\"#topic-02-subtopic-4\">Data Protection, Encryption, and Backup Lifecycle Ownership</a></li>\\n'\n"
    "               '<li><a href=\"#topic-02-subtopic-5\">Google Cloud Shared Fate: From Contractual Liability to Collaborative Posture Management</a></li></ul>\\n'\n"
    "               '</article>\\n',"
)
assert text.count(old_f5) == 1, f"F5 count {text.count(old_f5)}"
text = text.replace(old_f5, new_f5, 1)

# F2: Evidence limit for Topic 1
old_f2 = "'residual': 'While host OS patching is delegated entirely to Google Cloud, the development "
new_f2 = "'evidence_limit': 'Evidence limit: The simulated VM segfault and Cloud Run redeployment demonstrate operational maintenance boundaries; they do not reproduce Google Cloud data plane kernel outages or vendor hypervisor faults.',\n             'residual': 'While host OS patching is delegated entirely to Google Cloud, the development "
assert text.count(old_f2) == 1, f"F2 count {text.count(old_f2)}"
text = text.replace(old_f2, new_f2, 1)

# F3: Evidence limit for Topic 2
old_f3 = "'residual': 'Internal service accounts authorized to invoke Cloud Run must be audited "
new_f3 = "'evidence_limit': 'Evidence limit: The Cloud Run allUsers IAM misconfiguration demonstrates tenant access boundary errors; it does not indicate a flaw or failure in Google Cloud IAM infrastructure or OIDC token issuance.',\n             'residual': 'Internal service accounts authorized to invoke Cloud Run must be audited "
assert text.count(old_f3) == 1, f"F3 count {text.count(old_f3)}"
text = text.replace(old_f3, new_f3, 1)

with open('scratch/day_data_011.py', 'w') as f:
    f.write(text)

print("Applied F1, F2, F3, F4, F5 successfully!")
