# Docker Development Setup Guide

This guide will help you set up and test the AI Agents System using Docker for a complete, isolated development environment.

## Prerequisites

- Docker Desktop or Docker Engine + Docker Compose
- Git
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ai-agents-system
```

### 2. Configure Environment

```bash
# Copy the development environment template
cp config/development.env .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Build and Start

```bash
# Build the development environment
make build

# Start supporting services (Redis, PostgreSQL)
make up

# Start the web interface
make web
```

Access the web interface at: **http://localhost:5000**

## Available Commands

### Setup Commands
```bash
make build          # Build Docker development environment
make up             # Start Redis and PostgreSQL services
make down           # Stop all services
make clean          # Clean up Docker resources
```

### Development Commands
```bash
make web            # Start web interface (localhost:5000)
make demo           # Run interactive CLI demo
make test           # Run test suite
make shell          # Open interactive shell in container
```

### Utility Commands
```bash
make logs           # Show application logs
make check          # Run system health check
make dev            # Quick start: build + up + web
make test-all       # Full test: build + up + test
```

## Development Workflow

### Testing the AI Agents

1. **Web Interface Testing**
   ```bash
   make web
   ```
   - Open http://localhost:5000
   - Enter a research topic (e.g., "Artificial Intelligence in Healthcare")
   - Watch the multi-agent workflow in action
   - Review the generated reports

2. **CLI Demo Testing**
   ```bash
   make demo
   ```
   - Interactive command-line demonstration
   - Choose from predefined topics or enter custom ones
   - See agent collaboration in terminal

3. **System Testing**
   ```bash
   make test
   ```
   - Run the complete test suite
   - Verify all agents are working correctly

### Development Shell Access

```bash
make shell
```

Inside the container, you can:
- Explore the codebase: `ls -la src/`
- Run individual agents: `python -m src.agents.research.research_agent`
- Check configurations: `python scripts/setup.py`
- Install additional packages: `pip install package_name`

### Monitoring and Debugging

```bash
# Real-time logs
make logs

# Health check
make check

# Container status
docker-compose ps
```

## Project Structure in Docker

```
/app/                           # Container working directory
├── src/                        # Source code (mounted from host)
│   ├── agents/                 # AI agent modules
│   ├── core/                   # Core orchestration
│   └── interfaces/             # Web and CLI interfaces
├── config/                     # Configuration files
├── scripts/                    # Utility scripts
├── tests/                      # Test suite
├── requirements/               # Python dependencies
├── logs/                       # Application logs
├── data/                       # Runtime data
└── exports/                    # Generated reports
```

## Environment Configuration

Key environment variables in `.env`:

```bash
# Required - Get from OpenAI
OPENAI_API_KEY=your_api_key_here

# Model configuration
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.7

# Agent behavior
MAX_RESEARCH_SOURCES=10
QUALITY_THRESHOLD=0.75

# Services (automatically configured for Docker)
REDIS_URL=redis://redis:6379/0
DATABASE_URL=postgresql://ai_user:ai_password@postgres:5432/ai_agents
```

## Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   ```bash
   # Check what's using the port
   lsof -i :5000
   
   # Kill the process or change the port in docker-compose.yml
   ```

2. **OpenAI API errors**
   ```bash
   # Verify your API key is set correctly
   make shell
   echo $OPENAI_API_KEY
   ```

3. **Permission errors**
   ```bash
   # Fix file permissions
   chmod +x scripts/docker-start.sh
   ```

4. **Container won't start**
   ```bash
   # Check logs
   docker-compose logs ai-agents
   
   # Rebuild with no cache
   make clean
   make build
   ```

### Reset Everything

```bash
# Complete reset
make clean
docker system prune -a
make build
make up
```

## Testing Specific Features

### Research Agent
```bash
make shell
python -c "
from src.agents.research import ResearchAgent
import asyncio

async def test():
    agent = ResearchAgent()
    result = await agent.process({'topic': 'Machine Learning'})
    print(result.output)

asyncio.run(test())
"
```

### Multi-Agent Workflow
```bash
make shell
python -c "
from src.core.orchestrator import AgentOrchestrator
import asyncio

async def test():
    orchestrator = AgentOrchestrator()
    result = await orchestrator.execute_research_workflow(
        topic='AI in Healthcare',
        depth='medium',
        content_type='comprehensive_report'
    )
    print(f'Completed in {result.total_execution_time:.2f}s')

asyncio.run(test())
"
```

## Production Deployment

Once everything works in Docker:

1. **Test the production Docker image**
   ```bash
   docker build -f Dockerfile -t ai-agents:prod .
   docker run -p 5000:5000 --env-file .env ai-agents:prod
   ```

2. **Deploy with confidence** knowing the system works in Docker

## Next Steps

- Once Docker setup is working perfectly, GitHub Actions CI/CD will be much easier
- The same Docker configuration can be used for staging and production
- All dependencies and configurations are locked and reproducible 