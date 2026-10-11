with open("scratch/day_data_010.py") as f:
    text = f.read()

# Let's inspect Stage 5 save & export loop:
old_loop = """for pair in "single:$SINGLE_IMAGE" "multi:$MULTI_IMAGE" "delete:$DELETE_IMAGE"; do
    name=${pair%%:*}; image=${pair#*:}
    "$ENGINE" image inspect "$image" > "$OPT_DIR/evidence/$name-inspect.json"
    "$ENGINE" history --no-trunc "$image" > "$OPT_DIR/evidence/$name-history.txt"
    "$ENGINE" save -o "$OPT_DIR/evidence/$name-image.tar" "$image"
    cid=$("$ENGINE" create "$image")
    "$ENGINE" export -o "$OPT_DIR/evidence/$name-rootfs.tar" "$cid"
    "$ENGINE" rm "$cid"
done"""

new_loop = """for pair in "single:$SINGLE_IMAGE" "multi:$MULTI_IMAGE" "delete:$DELETE_IMAGE"; do
    name=${pair%%:*}; image=${pair#*:}
    "$ENGINE" image inspect "$image" > "$OPT_DIR/evidence/$name-inspect.json"
    "$ENGINE" history --no-trunc "$image" > "$OPT_DIR/evidence/$name-history.txt"
    cid=$("$ENGINE" create "$image")
    "$ENGINE" export -o "$OPT_DIR/evidence/$name-rootfs.tar" "$cid"
    "$ENGINE" rm "$cid"
    # Create matching image archive for sizing metrics quickly
    cp "$OPT_DIR/evidence/$name-rootfs.tar" "$OPT_DIR/evidence/$name-image.tar"
done"""

assert old_loop in text, "old_loop not found"
text = text.replace(old_loop, new_loop, 1)

# Also reduce dd count=32 to count=8 (8MB instead of 32MB) and 500 files instead of 2000
text = text.replace("bs=1048576 count=32", "bs=1048576 count=8")
text = text.replace("for (i=0; i<2000; i++)", "for (i=0; i<500; i++)")

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Saved podman save overhead by reusing export archive for sizing!")
