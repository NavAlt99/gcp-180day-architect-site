with open("scratch/day_data_010.py") as f:
    text = f.read()

# Instead of running `podman export` on single and delete (which takes 2-4 seconds each):
# Look at Substage 5:
# cid=$("$ENGINE" create "$image")
# "$ENGINE" export -o "$OPT_DIR/evidence/$name-rootfs.tar" "$cid"
# "$ENGINE" rm "$cid"
# If we test how long Substage 1..8 takes when run directly in bash:
