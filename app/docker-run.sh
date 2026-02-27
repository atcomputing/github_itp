#!/usr/bin/env bash
#
# Simple Docker run script for In The Picture application
#
# Usage:
#   ./docker-run.sh          # Build and run container
#   ./docker-run.sh --stop   # Stop and remove container

set -e

CONTAINER_NAME="inthepicture-app"
IMAGE_NAME="inthepicture:latest"
PORT="5001"

# Parse arguments
if [ "$1" == "--stop" ]; then
    echo "Stopping container..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    echo "✅ Container stopped and removed"
    exit 0
fi

# Build image
echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .

# Stop existing container if running
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

# Run container
echo "Starting container..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$PORT:$PORT" \
    "$IMAGE_NAME"

echo ""
echo "✅ Container started successfully!"
echo ""
echo "Access app at: http://localhost:$PORT"
echo ""
echo "Useful commands:"
echo "  docker logs $CONTAINER_NAME       # View logs"
echo "  docker logs -f $CONTAINER_NAME    # Follow logs"
echo "  docker stop $CONTAINER_NAME       # Stop container"
echo "  ./docker-run.sh --stop            # Stop and remove"
echo ""
