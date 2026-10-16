with open("scratch/day_data_010.py") as f:
    text = f.read()

# In Stage 8 (Validate Acceptance Invariants and Cleanup):
# After:
# pathlib.Path('scratch/day-010-image-cleanup.txt').write_text('Lab image tags and export/save archives removed. Shared builder cache and pulled base retained; no global prune.\n')
# CLEAN
# if [ "$ENGINE" = podman ]; then
#     if [ -n "$OPT_PREVIOUS_CONFIG" ]; then
#         export XDG_CONFIG_HOME="$OPT_PREVIOUS_CONFIG"
#     else
#         unset XDG_CONFIG_HOME
#     fi
# fi

old_clean = """CLEAN
if [ "$ENGINE" = podman ]; then
    if [ -n "$OPT_PREVIOUS_CONFIG" ]; then
        export XDG_CONFIG_HOME="$OPT_PREVIOUS_CONFIG"
    else
        unset XDG_CONFIG_HOME
    fi
fi"""

new_clean = """CLEAN
if [ "$ENGINE" = podman ]; then
    podman system reset -f > /dev/null 2>&1 || true
    if [ -n "$OPT_PREVIOUS_CONFIG" ]; then
        export XDG_CONFIG_HOME="$OPT_PREVIOUS_CONFIG"
    else
        unset XDG_CONFIG_HOME
    fi
fi"""

assert old_clean in text, "old_clean not found"
text = text.replace(old_clean, new_clean, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Added podman system reset -f to Stage 8 cleanup!")
