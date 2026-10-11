with open("scratch/day_data_010.py") as f:
    text = f.read()

# Topic 1 scenario:
old_s1 = "Evidence:</strong></p>\n<p>Inspecting the container runtime reveals"
new_s1 = "Evidence:</strong> (illustrative logs)</p>\n<p>Inspecting the container runtime reveals"
if old_s1 in text:
    text = text.replace(old_s1, new_s1, 1)

old_s1_end = "preserving at-most-once fulfillment semantics.</figcaption>\n</figure>"
new_s1_end = "preserving at-most-once fulfillment semantics.</figcaption>\n</figure>\n<p><strong class=\"side-heading\">Evidence limit:</strong> The incident trace and simulated container failure reflect local execution assumptions and architectural modeling rather than a live production outage trace.</p>"
if old_s1_end in text:
    text = text.replace(old_s1_end, new_s1_end, 1)

# Topic 2 scenario:
old_s2 = "Evidence:</strong></p>\n<p>Node resource metrics"
new_s2 = "Evidence:</strong> (illustrative logs)</p>\n<p>Node resource metrics"
if old_s2 in text:
    text = text.replace(old_s2, new_s2, 1)

old_s2_end = "rescheduling prevents cluster-wide downtime.</figcaption>\n</figure>"
new_s2_end = "rescheduling prevents cluster-wide downtime.</figcaption>\n</figure>\n<p><strong class=\"side-heading\">Evidence limit:</strong> The scheduler placement failure models memory starvation under a simulated FIFO queue; it does not represent live GKE cluster autoscaler or upstream kube-scheduler plugin execution.</p>"
if old_s2_end in text:
    text = text.replace(old_s2_end, new_s2_end, 1)

# Topic 3 scenario:
old_s3 = "Evidence:</strong></p>\n<p>Examining the EndpointSlice"
new_s3 = "Evidence:</strong> (illustrative logs)</p>\n<p>Examining the EndpointSlice"
if old_s3 in text:
    text = text.replace(old_s3, new_s3, 1)

old_s3_end = "restoring traffic routing.</figcaption>\n</figure>"
new_s3_end = "restoring traffic routing.</figcaption>\n</figure>\n<p><strong class=\"side-heading\">Evidence limit:</strong> The routing defect isolates the label selector mapping; live Google Cloud Load Balancer health checks and Cloud Armor rules were not executed.</p>"
if old_s3_end in text:
    text = text.replace(old_s3_end, new_s3_end, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Scenarios patched successfully.")
