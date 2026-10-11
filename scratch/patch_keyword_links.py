import re
import urllib.parse
from bs4 import BeautifulSoup

spec_path = "scratch/day_data_010.py"
spec_text = open(spec_path).read()

# All 70 key terms from the audit:
terms = [
    'Artifact Registry', 'Bind mounts', 'CFS', 'CMEK', 'CNI', 'COS', 'CRI', 'CSI',
    'Compute Engine', 'Container image construction', 'Container orchestration',
    'Copy-on-Write', 'DNAT', 'Dockerfile', 'EndpointSlices', 'Ephemeral container storage',
    'GCLB', 'GKE Autopilot', 'GKE Cluster Autoscaler (CA)',
    'GKE Container-Native Load Balancing with NEGs',
    'GKE Container-Native Load Balancing with Network Endpoint Groups (NEGs)',
    'GKE Database Encryption (Application-Layer Secrets Encryption)',
    'GKE Ingress (GCE Ingress Controller)', 'GKE Node Auto-Provisioning (NAP)',
    'GKE VPC-Native Clusters', 'GKE Workload Identity', 'GitOps',
    'Google Cloud Config Sync', 'Google Cloud Deploy',
    'Google Cloud Key Management Service (Cloud KMS)',
    'Google Cloud Secret Manager CSI Driver', 'Google Kubernetes Engine (GKE)',
    'IPVS', 'Ingress Controller', 'Kubernetes core objects', 'MTTR', 'MVCC', 'NIC',
    'Named volumes', 'OCI', 'OOM killer', 'OverlayFS', 'PDBs', 'PoPs', 'Pod',
    'Policy Controller (OPA Gatekeeper)', 'QoS', 'RBAC', 'Raft consensus algorithm',
    'ReplicaSets', 'SDN', 'SLOs', 'Service', 'VPC', 'VPC Alias IP ranges',
    'VXLAN / Geneve', 'WAF', 'container registry', 'containerd', 'dockerd', 'etcd',
    'fdatasync', 'fsync()', 'inodes', 'iptables DNAT', 'kube-scheduler',
    'level-triggered control loops', 'page cache', 'runc', 'systemd',
    'three-way merge patch', 'thundering herd', 'x509 client certificates'
]

# We need to wrap each <strong class="keyword">TERM</strong> with <strong class="keyword"><a href="http://www.google.com/search?q=TERM" rel="noopener" target="_blank">TERM</a></strong>
# S3 rule: "when the term sits inside a strong.keyword span, put the anchor inside the span."
# In scratch/day_data_010.py, keywords are defined inside the string literals for DATA['topics'][*]['technical']!
# Let's inspect all <strong class="keyword"> occurrences in spec_text across lines or within lines.

def replace_keyword_span(match):
    prefix = match.group(1) # opening tag including any whitespace/newlines
    term = match.group(2).strip()
    # Check if already has <a>
    if '<a ' in term:
        return match.group(0)
    q = urllib.parse.quote_plus(term)
    link = f'<a href="http://www.google.com/search?q={q}" rel="noopener" target="_blank">{term}</a>'
    return f'{prefix}{link}</strong>'

# Match <strong[\s\n]+class="keyword">TERM</strong>
pattern = re.compile(r'(<strong[\s\n]+class="keyword">)(.*?)</strong>', re.DOTALL)

# Let's test on spec_text:
new_text = pattern.sub(replace_keyword_span, spec_text)
print("Substitutions made:", len(pattern.findall(spec_text)))

with open(spec_path, "w") as f:
    f.write(new_text)

print("Saved updated spec with S3 discovery links!")
