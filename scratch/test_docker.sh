set -e
if docker info > /dev/null 2>&1; then
    echo "Docker available"
    docker pull golang:1.26-alpine || docker pull golang:alpine
else
    echo "Podman"
fi
