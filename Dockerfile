# AI Agents System - Production Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements/production.txt requirements/production.txt
COPY requirements/base.txt requirements/base.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/production.txt

# Copy application code
COPY src/ src/
COPY config/ config/
COPY scripts/ scripts/
COPY pyproject.toml ./
COPY README.md ./

# Create non-root user
RUN useradd --create-home --shell /bin/bash ai_user && \
    chown -R ai_user:ai_user /app
USER ai_user

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/system_metrics')" || exit 1

# Default command
CMD ["python", "-m", "src.interfaces.web.app"] 