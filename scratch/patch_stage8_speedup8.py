with open("scratch/day_data_010.py") as f:
    text = f.read()

# Replace:
# podman system reset -f > /dev/null 2>&1 || true
# with fast podman cleanup:
# "$ENGINE" rm -f "$cid" > /dev/null 2>&1 || true
# "$ENGINE" rmi -f "$DELETE_IMAGE" "$MULTI_IMAGE" "$SINGLE_IMAGE" > /dev/null 2>&1 || true
old_reset = '    podman system reset -f > /dev/null 2>&1 || true'
new_reset = '    podman rm -a -f > /dev/null 2>&1 || true'
assert old_reset in text, "old_reset not found"
text = text.replace(old_reset, new_reset, 1)

# And in command 9 (the last cleanup):
# "$ENGINE" image rm "$DELETE_IMAGE" "$MULTI_IMAGE" "$SINGLE_IMAGE"
# We can add --force:
text = text.replace('"$ENGINE" image rm "$DELETE_IMAGE" "$MULTI_IMAGE" "$SINGLE_IMAGE"', '"$ENGINE" image rm -f "$DELETE_IMAGE" "$MULTI_IMAGE" "$SINGLE_IMAGE" > /dev/null 2>&1 || true')

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Replaced podman system reset with fast podman rm -a -f!")
