with open("scratch/day_data_010.py") as f:
    text = f.read()

# Notice in Stage 1 preflight of _BUILD_COMPARE_STAGES:
# In Command 2:
# What if we save the already pulled golang image to a local archive in scratch/ once, or load it with `$ENGINE load`?
# In `scratch/`, we can have `golang-cached.tar`!
# Let's see: `podman save -o scratch/day010-golang-base.tar docker.io/library/golang:1.26-alpine` takes 1.8 seconds!
# And `$ENGINE load -i scratch/day010-golang-base.tar` inside run_labs takes 1.5 seconds!
# That completely eliminates the 30-second internet pull!
