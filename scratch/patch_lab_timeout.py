with open("scratch/day_data_010.py") as f:
    text = f.read()

# Let's inspect Stage 1 of _BUILD_COMPARE_STAGES:
# If podman/docker takes time pulling golang:1.26-alpine or compiling,
# let's see how long single-build took:
# In the previous run_labs run, it pulled golang:1.26-alpine and ran apk add --no-cache build-base which took over 60s total.
