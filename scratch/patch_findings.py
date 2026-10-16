import re
import urllib.parse
from bs4 import BeautifulSoup
from pathlib import Path

spec_path = "scratch/day_data_010.py"
spec_text = open(spec_path).read()

# ==========================================
# Finding F7: Scenarios Evidence limit & illustrative log labels
# ==========================================
# In Topic 1 scenario:
old_s1 = "Evidence:</strong></p>\n<p>Inspecting the container runtime reveals"
new_s1 = "Evidence:</strong> (illustrative logs)</p>\n<p>Inspecting the container runtime reveals"
if old_s1 in spec_text:
    spec_text = spec_text.replace(old_s1, new_s1, 1)

old_s1_end = "preserving at-most-once fulfillment semantics.</figcaption>\n</figure>"
new_s1_end = "preserving at-most-once fulfillment semantics.</figcaption>\n</figure>\n<p><strong class=\"side-heading\">Evidence limit:</strong> The incident trace and simulated container failure reflect local execution assumptions and architectural modeling rather than a production outage trace.</p>"
if old_s1_end in spec_text:
    spec_text = spec_text.replace(old_s1_end, new_s1_end, 1)

# In Topic 2 scenario:
old_s2 = "Evidence:</strong></p>\n<p>Node resource metrics"
new_s2 = "Evidence:</strong> (illustrative logs)</p>\n<p>Node resource metrics"
if old_s2 in spec_text:
    spec_text = spec_text.replace(old_s2, new_s2, 1)

old_s2_end = "rescheduling prevents cluster-wide downtime.</figcaption>\n</figure>"
new_s2_end = "rescheduling prevents cluster-wide downtime.</figcaption>\n</figure>\n<p><strong class=\"side-heading\">Evidence limit:</strong> The scheduler placement failure models memory starvation under a simulated FIFO queue; it does not represent live GKE cluster autoscaler or upstream kube-scheduler plugin execution.</p>"
if old_s2_end in spec_text:
    spec_text = spec_text.replace(old_s2_end, new_s2_end, 1)

# In Topic 3 scenario:
old_s3 = "Evidence:</strong></p>\n<p>Examining the EndpointSlice"
new_s3 = "Evidence:</strong> (illustrative logs)</p>\n<p>Examining the EndpointSlice"
if old_s3 in spec_text:
    spec_text = spec_text.replace(old_s3, new_s3, 1)

old_s3_end = "restoring traffic routing.</figcaption>\n</figure>"
new_s3_end = "restoring traffic routing.</figcaption>\n</figure>\n<p><strong class=\"side-heading\">Evidence limit:</strong> The routing defect isolates the label selector mapping; live Google Cloud Load Balancer health checks and Cloud Armor rules were not executed.</p>"
if old_s3_end in spec_text:
    spec_text = spec_text.replace(old_s3_end, new_s3_end, 1)

print("Scenarios updated (F7)")

# ==========================================
# Findings F2-F6: SVG viewBox & collision adjustments
# ==========================================
# SVG 3: day10-reconcile-desc / day10-reconcile-title
# viewbox="0 0 940 300" -> viewbox="0 0 980 300"
spec_text = spec_text.replace('viewbox="0 0 940 300"', 'viewbox="0 0 980 300"')

# SVG 4: day10-objects-title
# viewbox="0 0 940 320" -> viewbox="0 0 980 320"
spec_text = spec_text.replace('viewbox="0 0 940 320"', 'viewbox="0 0 980 320"')

# SVG 5: day10-volume-incident-title
# viewbox="0 0 940 310" -> viewbox="0 0 1020 310"
# and icon overlap:
# image at (503, 38) and (503, 193) with width 22, text at (342, 46) and (342, 201)
# Move the image or text: in SVG 5, let's see how rect and text are positioned:
# <text x="342" y="46" fill="#f43f5e" ...>[FAILED: Ephemeral Layer]</text>
# Let's inspect SVG 5 in spec_text.
