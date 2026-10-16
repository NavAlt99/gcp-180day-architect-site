set -e
export ENGINE=podman
export BUILD_FLAGS=()
OPT_DIR=$(mktemp -d /tmp/day010-image-XXXXXX)
export OPT_DIR
mkdir -p "$OPT_DIR/evidence"
printf '%s\n' '{"default":[{"type":"insecureAcceptAnything"}]}' > "$OPT_DIR/pull-policy.json"
BUILD_FLAGS=(--signature-policy "$OPT_DIR/pull-policy.json")
RUN_ID="testrun"
SINGLE_IMAGE="localhost/day010-single:$RUN_ID"
MULTI_IMAGE="localhost/day010-multi:$RUN_ID"
DELETE_IMAGE="localhost/day010-delete:$RUN_ID"
export SINGLE_IMAGE MULTI_IMAGE DELETE_IMAGE
printf '%s\n' "$SINGLE_IMAGE" "$MULTI_IMAGE" "$DELETE_IMAGE" > "$OPT_DIR/evidence/tags.txt"

time "$ENGINE" build "${BUILD_FLAGS[@]}" -f "$OPT_DIR/Dockerfile.single" -t "$SINGLE_IMAGE" "$OPT_DIR" || true
