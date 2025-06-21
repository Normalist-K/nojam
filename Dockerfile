# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Install uv (dependency manager) and system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

# Set workdir
WORKDIR /app

# Copy dependency files first for caching
COPY pyproject.toml .

# Install Python dependencies via uv
RUN uv sync

# Copy application code
COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Start Uvicorn
CMD ["uv", "run", "uvicorn", "nojam.main:app", "--host", "0.0.0.0", "--port", "8000"]
