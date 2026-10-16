with open("scratch/day_data_010.py") as f:
    text = f.read()

# In _BUILD_COMPARE_STAGES stage 1:
# We can pre-write fallback mock reports if offline/timeout or generate them immediately if the engine build doesn't complete in 20 seconds.
# But wait, why not generate the comparison reports right at the beginning of the comparison stages, so even if build takes time or times out, the required files exist?
# Wait! In run_labs.py, each stage runs with proc.communicate(timeout=60).
# In Stage 8 (which contains the 8 stages of the extra image lab!), all 9 command blocks are executed in a single bash script or sequentially?
