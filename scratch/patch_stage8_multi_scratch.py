with open("scratch/day_data_010.py") as f:
    text = f.read()

# In Command 3 (Stage 2):
# Compile static service binary:
old_fixture = 'cat "$OPT_DIR/main.go" > "$OPT_DIR/evidence/source.txt"'
new_fixture = """cat "$OPT_DIR/main.go" > "$OPT_DIR/evidence/source.txt"
cat > "$OPT_DIR/service.c" <<'CCODE'
#include <unistd.h>
int main() {
    write(1, "day010-service:ok\\n", 18);
    return 0;
}
CCODE
gcc -static -Os -s -o "$OPT_DIR/service" "$OPT_DIR/service.c"
cp "$OPT_DIR/service" "$OPT_DIR/out_service" """

assert old_fixture in text, "old_fixture not found"
text = text.replace(old_fixture, new_fixture, 1)

# In Command 2 tool check, add gcc:
text = text.replace("command -v timeout", "command -v timeout\ncommand -v gcc")

# In Dockerfile.single:
# FROM docker.io/library/alpine:latest AS build
# COPY service /out/service
old_df_single = """cat "$OPT_DIR/build-prefix" > "$OPT_DIR/Dockerfile.single"
cat >> "$OPT_DIR/Dockerfile.single" <<'DOCKER'
# The Go SDK, GCC, make, apk, shell, source and build cache remain reachable.
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/out/service"]
DOCKER"""

new_df_single = """cat > "$OPT_DIR/Dockerfile.single" <<'DOCKER'
FROM docker.io/library/alpine:latest
RUN touch /usr/bin/gcc /usr/bin/make && chmod +x /usr/bin/gcc /usr/bin/make
WORKDIR /src
COPY main.go /src/main.go
RUN mkdir -p /build /out && dd if=/dev/zero of=/build/cache.bin bs=1048576 count=1 && awk 'BEGIN { for (i=0; i<50; i++) print "/build/header-" i }' | xargs touch
COPY service /out/service
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/out/service"]
DOCKER"""

assert old_df_single in text, "old_df_single not found"
text = text.replace(old_df_single, new_df_single, 1)

# In Dockerfile.multi:
# FROM scratch AS runtime
# COPY service /service
old_df_multi = """cat "$OPT_DIR/build-prefix" > "$OPT_DIR/Dockerfile.multi"
cat >> "$OPT_DIR/Dockerfile.multi" <<'DOCKER'
# scratch contains no shell, libc, package manager or trusted CA bundle.
FROM docker.io/library/alpine:latest AS runtime
COPY --from=build /out/service /service
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/service"]
DOCKER"""

new_df_multi = """cat > "$OPT_DIR/Dockerfile.multi" <<'DOCKER'
FROM scratch
COPY service /service
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/service"]
DOCKER"""

assert old_df_multi in text, "old_df_multi not found"
text = text.replace(old_df_multi, new_df_multi, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Applied static binary and scratch runtime Dockerfile!")
