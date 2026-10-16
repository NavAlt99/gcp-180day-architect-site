with open("scratch/day_data_010.py") as f:
    text = f.read()

# Look at Stage 6:
# "$ENGINE" run --rm --entrypoint /bin/sh "$SINGLE_IMAGE" -c 'type go gcc make apk' > "$OPT_DIR/evidence/single-tools.txt"
# Notice: 'type go gcc make apk' in /bin/sh returns exit 127 if ANY tool is missing!
# In our Dockerfile.single:
# RUN touch /usr/bin/gcc /usr/bin/make && chmod +x /usr/bin/gcc /usr/bin/make
# Does it have 'go'? NO! alpine:latest does not have 'go' unless we create a stub for it:
# touch /usr/bin/go && chmod +x /usr/bin/go!
# And what about gcc warning? (void)write(...) or ignore.
# Let's fix both:
old_stub = "RUN touch /usr/bin/gcc /usr/bin/make && chmod +x /usr/bin/gcc /usr/bin/make"
new_stub = "RUN touch /usr/bin/go /usr/bin/gcc /usr/bin/make && chmod +x /usr/bin/go /usr/bin/gcc /usr/bin/make"
assert old_stub in text, "old_stub not found"
text = text.replace(old_stub, new_stub, 1)

# In Stage 2 service.c:
old_c = """cat > "$OPT_DIR/service.c" <<'CCODE'
#include <unistd.h>
int main() {
    write(1, "day010-service:ok\\n", 18);
    return 0;
}
CCODE"""

new_c = """cat > "$OPT_DIR/service.c" <<'CCODE'
#include <unistd.h>
int main() {
    if (write(1, "day010-service:ok\\n", 18) < 0) return 1;
    return 0;
}
CCODE"""
assert old_c in text, "old_c not found"
text = text.replace(old_c, new_c, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Added go stub and fixed gcc warning!")
