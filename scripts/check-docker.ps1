#!/usr/bin/env pwsh

Write-Host "AI Agents System - Docker Environment Check" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker is installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
}

# Check if Docker daemon is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker daemon is not running." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please start Docker Desktop:" -ForegroundColor Yellow
    Write-Host "  1. Open Docker Desktop from the Start menu" -ForegroundColor Yellow
    Write-Host "  2. Wait for Docker Desktop to fully start (usually 30-60 seconds)" -ForegroundColor Yellow
    Write-Host "  3. You'll see the Docker whale icon in your system tray when it's ready" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "If Docker Desktop is already running, try restarting it." -ForegroundColor Yellow
    exit 1
}

# Check if Docker Compose is available
try {
    $composeVersion = docker-compose --version 
    Write-Host "✅ Docker Compose is available: $composeVersion" -ForegroundColor Green
} catch {
    try {
        $composeVersion = docker compose version
        Write-Host "✅ Docker Compose is available: $composeVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Docker Compose is not available." -ForegroundColor Red
        Write-Host ""
        Write-Host "Docker Compose should be included with Docker Desktop."
        exit 1
    }
}

Write-Host ""
Write-Host "Docker Environment Information:" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
docker --version
docker-compose --version 2>$null
if ($LASTEXITCODE -ne 0) {
    docker compose version
}

Write-Host ""
Write-Host "System Resources:" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
$drive = (Get-Location).Drive
$freeSpace = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='$($drive.Name)'" | Select-Object -ExpandProperty FreeSpace
$freeSpaceGB = [math]::Round($freeSpace / 1GB, 2)
Write-Host "Available disk space on $($drive.Name): $freeSpaceGB GB"

Write-Host ""
Write-Host "🎉 Docker environment is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Ensure you have an OpenAI API key set in .env file" -ForegroundColor Yellow
Write-Host "2. Run: make build (or docker-compose build ai-agents)" -ForegroundColor Yellow
Write-Host "3. Run: make up (or docker-compose up -d redis postgres)" -ForegroundColor Yellow
Write-Host "4. Run: make web (or docker-compose run --rm --service-ports ai-agents ./start.sh web)" -ForegroundColor Yellow 