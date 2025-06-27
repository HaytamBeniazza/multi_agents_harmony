#!/bin/bash

echo "AI Agents System - Docker Environment Check"
echo "==========================================="
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    echo
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running."
    echo
    echo "Please start Docker Desktop:"
    echo "  - Windows: Open Docker Desktop from the Start menu"
    echo "  - macOS: Open Docker Desktop from Applications"
    echo "  - Linux: sudo systemctl start docker"
    echo
    echo "Wait for Docker Desktop to fully start (usually 30-60 seconds)"
    echo "You'll see the Docker icon in your system tray when it's ready."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available."
    echo
    echo "Docker Compose should be included with Docker Desktop."
    echo "If you're using Docker Engine separately, install Docker Compose."
    exit 1
fi

echo "✅ Docker is installed and running"
echo "✅ Docker Compose is available"
echo

# Display Docker info
echo "Docker Environment Information:"
echo "==============================="
docker --version
docker-compose --version 2>/dev/null || docker compose version
echo

# Check available resources
echo "System Resources:"
echo "=================="
echo "Available disk space:"
df -h . 2>/dev/null || dir | findstr "bytes free" 2>/dev/null || echo "Could not check disk space"
echo

echo "🎉 Docker environment is ready!"
echo
echo "Next steps:"
echo "1. Ensure you have an OpenAI API key set in .env file"
echo "2. Run: make build"
echo "3. Run: make up"
echo "4. Run: make web" 