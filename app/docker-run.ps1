<#
.SYNOPSIS
    Simple Docker run script for In The Picture application

.DESCRIPTION
    Builds and runs the In The Picture Docker container, or stops it if --Stop is specified.

.PARAMETER Stop
    Stop and remove the container instead of starting it

.EXAMPLE
    .\docker-run.ps1
    Builds and runs the container

.EXAMPLE
    .\docker-run.ps1 -Stop
    Stops and removes the container
#>

param(
    [switch]$Stop
)

$ErrorActionPreference = "Stop"

# Configuration
$CONTAINER_NAME = "github_itp-app"
$IMAGE_NAME = "github_itp:latest"
$PORT = "5001"

# Stop mode
if ($Stop) {
    Write-Host "Stopping container..." -ForegroundColor Yellow

    # Stop container (ignore errors if not running)
    try {
        docker stop $CONTAINER_NAME 2>$null
    } catch {
        # Container not running, that's ok
    }

    # Remove container (ignore errors if doesn't exist)
    try {
        docker rm $CONTAINER_NAME 2>$null
    } catch {
        # Container doesn't exist, that's ok
    }

    Write-Host "Container stopped and removed" -ForegroundColor Green
    exit 0
}

# Build and run mode
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build -t $IMAGE_NAME .

# Stop existing container if running
try {
    docker stop $CONTAINER_NAME 2>$null | Out-Null
} catch {
    # Container not running, that's ok
}

try {
    docker rm $CONTAINER_NAME 2>$null | Out-Null
} catch {
    # Container doesn't exist, that's ok
}

# Run container
Write-Host "Starting container..." -ForegroundColor Yellow
docker run -d `
    --name $CONTAINER_NAME `
    -p "${PORT}:${PORT}" `
    $IMAGE_NAME

Write-Host ""
Write-Host "Container started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Access app at: http://localhost:$PORT" -ForegroundColor Cyan
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  docker logs $CONTAINER_NAME       # View logs"
Write-Host "  docker logs -f $CONTAINER_NAME    # Follow logs"
Write-Host "  docker stop $CONTAINER_NAME       # Stop container"
Write-Host "  .\docker-run.ps1 -Stop            # Stop and remove"
Write-Host ""
