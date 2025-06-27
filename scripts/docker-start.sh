#!/bin/bash
set -e

echo "AI Agents Development Environment"
echo "================================="

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp config/development.env .env
    echo "WARNING: Please set your OPENAI_API_KEY in .env file"
fi

# Run system check
echo "Running system check..."
python scripts/setup.py || echo "WARNING: Setup check completed with warnings"

# Start the application based on command
case "$1" in
    "web")
        echo "Starting web interface..."
        python -m src.interfaces.web.app
        ;;
    "demo")
        echo "Running CLI demo..."
        python -m src.interfaces.cli.demo
        ;;
    "test")
        echo "Running tests..."
        python -m pytest tests/ -v
        ;;
    "shell")
        echo "Starting interactive shell..."
        /bin/bash
        ;;
    *)
        echo "Usage: $0 {web|demo|test|shell}"
        echo "Available commands:"
        echo "  web   - Start web interface on port 5000"
        echo "  demo  - Run interactive CLI demo"
        echo "  test  - Run test suite"
        echo "  shell - Start interactive shell"
        exit 1
        ;;
esac 