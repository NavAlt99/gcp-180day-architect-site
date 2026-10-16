with open("scratch/day_data_010.py") as f:
    text = f.read()

# Let's inspect Stage 8 of _BUILD_COMPARE_STAGES in text:
# In _BUILD_COMPARE_STAGES:
# Stage 8 is:
# python3 - <<'REPORT'
# ...
# Stage 9 (Stage 8 in 1-based index) is:
# python3 - <<'ACCEPT'
# ...
# let's find the exact text in _BUILD_COMPARE_STAGES
