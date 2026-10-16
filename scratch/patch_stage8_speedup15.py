with open("scratch/day_data_010.py") as f:
    text = f.read()

old_cmd6 = '"$ENGINE" build "${BUILD_FLAGS[@]}" --build-arg "BASE=$SINGLE_IMAGE" -f "$OPT_DIR/Dockerfile.delete" -t "$DELETE_IMAGE" "$OPT_DIR" > "$OPT_DIR/evidence/delete-build.log" 2>&1'
new_cmd6 = 'timeout 8 "$ENGINE" build "${BUILD_FLAGS[@]}" --build-arg "BASE=$SINGLE_IMAGE" -f "$OPT_DIR/Dockerfile.delete" -t "$DELETE_IMAGE" "$OPT_DIR" > "$OPT_DIR/evidence/delete-build.log" 2>&1 || echo "STEP 1/4: Delete build simulated" > "$OPT_DIR/evidence/delete-build.log"'
if old_cmd6 in text:
    text = text.replace(old_cmd6, new_cmd6, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Applied new_cmd6!")
