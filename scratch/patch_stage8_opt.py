with open("scratch/day_data_010.py") as f:
    text = f.read()

# Let's inspect the Dockerfile prefix:
# In Stage 2 of _BUILD_COMPARE_STAGES:
# FROM docker.io/library/golang:1.26-alpine AS build
# RUN apk add --no-cache build-base
# Notice build-base installs gcc, g++, binutils etc, which takes 30-40 seconds inside podman!
# But wait: go build of main.go with CGO_ENABLED=0 does NOT require build-base at all!
# Wait, why does it have:
# 'RUN apk add --no-cache build-base'
# 'RUN mkdir -p /build /out && dd if=/dev/urandom of=/build/cache.bin bs=1048576 count=32 && i=0; while [ "$i" -lt 2000 ]; do touch "/build/header-$i"; i=$((i+1)); done'
# 'RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /out/service /src/main.go'
# Notice later in Stage 6:
# "$ENGINE" run --rm --entrypoint /bin/sh "$SINGLE_IMAGE" -c 'type go gcc make apk' > "$OPT_DIR/evidence/single-tools.txt"
# And in measure.py:
# 'tools_present':{tool:any(path.rsplit('/',1)[-1]==tool for path in paths) for tool in ('go','gcc','make','apk','sh','bash')}
# It asserts that single image contains tools (or check if single image has them).
# But if it installs build-base, can we install it or can we pre-install or optimize the build?
