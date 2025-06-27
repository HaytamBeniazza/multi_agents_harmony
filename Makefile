# AI Agents System - Development Makefile

.PHONY: help build up down web demo test shell logs clean

# Default target
help:
	@echo "AI Agents Development Commands"
	@echo "============================="
	@echo ""
	@echo "Setup:"
	@echo "  build     - Build Docker development environment"
	@echo "  up        - Start all services (Redis, PostgreSQL, AI Agents)"
	@echo "  down      - Stop all services"
	@echo ""
	@echo "Development:"
	@echo "  web       - Start web interface (localhost:5000)"
	@echo "  demo      - Run interactive CLI demo"
	@echo "  test      - Run test suite"
	@echo "  shell     - Open interactive shell in container"
	@echo ""
	@echo "Utilities:"
	@echo "  logs      - Show application logs"
	@echo "  clean     - Clean up Docker resources"
	@echo "  check     - Run system health check"
	@echo ""

# Build development environment
build:
	@echo "Building AI Agents development environment..."
	docker-compose build --no-cache

# Start all services
up:
	@echo "Starting AI Agents system..."
	docker-compose up -d redis postgres
	@echo "Services started. Use 'make web' to start the AI agents."

# Stop all services
down:
	@echo "Stopping AI Agents system..."
	docker-compose down

# Start web interface
web:
	@echo "Starting AI Agents web interface..."
	@echo "Access at: http://localhost:5000"
	docker-compose run --rm --service-ports ai-agents ./start.sh web

# Run CLI demo
demo:
	@echo "Starting AI Agents CLI demo..."
	docker-compose run --rm ai-agents ./start.sh demo

# Run tests
test:
	@echo "Running AI Agents test suite..."
	docker-compose run --rm ai-agents ./start.sh test

# Open interactive shell
shell:
	@echo "Opening interactive shell..."
	docker-compose run --rm ai-agents ./start.sh shell

# Show logs
logs:
	@echo "Showing AI Agents logs..."
	docker-compose logs -f ai-agents

# Health check
check:
	@echo "Running system health check..."
	docker-compose run --rm ai-agents python scripts/setup.py

# Clean up
clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v
	docker system prune -f
	@echo "Cleanup complete."

# Quick start for development
dev: build up web

# Full system test
test-all: build up test 