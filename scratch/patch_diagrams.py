with open("scratch/day_data_010.py") as f:
    text = f.read()

# 1. SVG 3 (reconcile): widen viewBox from 940 to 980
text = text.replace('viewbox="0 0 940 300"', 'viewbox="0 0 980 300"')

# 2. SVG 4 (objects): widen viewBox from 940 to 980
text = text.replace('viewbox="0 0 940 320"', 'viewbox="0 0 980 320"')

# 3. SVG 5 (volume incident):
# Widen viewBox from 940 to 1000
text = text.replace('viewbox="0 0 940 310"', 'viewbox="0 0 1000 310"')
# In SVG 5, shorten header strings to avoid colliding with image at x=503:
# '[FAILED: Ephemeral Layer]' -> '[FAILED: Ephemeral]'
# '[CORRECTED: Persistent Vol]' -> '[CORRECTED: PVC]'
text = text.replace("'>[FAILED: Ephemeral Layer]</text>", "'>[FAILED: Ephemeral]</text>")
text = text.replace("'>[CORRECTED: Persistent Vol]</text>", "'>[CORRECTED: PVC Mount]</text>")

# 4. SVG 7 (sched incident):
# Widen viewBox from 940 to 1000
# Notice SVG 7 has viewbox="0 0 940 310" as well, but we already replaced it or need to be careful if there are multiple!
