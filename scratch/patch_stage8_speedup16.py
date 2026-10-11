with open("scratch/day_data_010.py") as f:
    text = f.read()

# Look at Command 2:
# In Command 2, add:
# command -v timeout
# in the preflight tool checks!
old_preflight = "command -v mktemp"
new_preflight = "command -v mktemp\ncommand -v timeout"
if old_preflight in text:
    text = text.replace(old_preflight, new_preflight, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Added command -v timeout to preflight!")
