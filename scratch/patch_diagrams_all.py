with open("scratch/day_data_010.py") as f:
    text = f.read()

# 1. SVG 3 (reconcile): widen viewBox from 940 to 980
text = text.replace('viewbox="0 0 940 300"', 'viewbox="0 0 980 300"')

# 2. SVG 4 (objects): widen viewBox from 940 to 980
text = text.replace('viewbox="0 0 940 320"', 'viewbox="0 0 980 320"')

# 3. SVG 5, 7, 9: widen viewBox from 940 to 1020
text = text.replace('viewbox="0 0 940 310"', 'viewbox="0 0 1020 310"')

# Shorten colliding texts in SVG 5 & SVG 9:
# SVG 5:
# '[FAILED: Ephemeral Layer]' -> '[FAILED: Ephemeral]'
# '[CORRECTED: Persistent Vol]' -> '[CORRECTED: PVC]'
text = text.replace('[FAILED: Ephemeral Layer]', '[FAILED: Ephemeral]')
text = text.replace('[CORRECTED: Persistent Vol]', '[CORRECTED: PVC]')

# SVG 9:
# '[CORRECTED: Matched Label Selector]' -> '[CORRECTED: Label Match]'
text = text.replace('[CORRECTED: Matched Label Selector]', '[CORRECTED: Label Match]')

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Diagram patches applied successfully.")
