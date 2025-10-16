# syntax=docker/dockerfile:1
# --- Builder image ---
FROM python:3.12-slim AS builder

WORKDIR /agent

# Install uv
RUN pip install uv

# Copy dependency files and source code
COPY pyproject.toml uv.lock ./
COPY data_agent ./data_agent
COPY health_agent ./health_agent
COPY insights_agent ./insights_agent
COPY README.md ./
RUN uv sync --frozen --no-dev

# --- Runtime image ---
FROM python:3.12-slim

WORKDIR /agent

# Install system dependencies for Streamlit and Cloud Run
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy installed dependencies and virtual environment from builder
COPY --from=builder /agent/.venv /agent/.venv
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv

# Copy application code
COPY . .
# DO NOT copy .env; set environment variables at runtime

# Cloud Run specific configuration
# Cloud Run expects the service to listen on the PORT environment variable
ENV PORT=8080

# Streamlit configuration
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Environment variables (set these at runtime for security)
# GOOGLE_API_KEY - Required: Your Google API key
# GOOGLE_CLOUD_PROJECT - Required: Your GCP project ID
# GOOGLE_CLOUD_LOCATION - Required: GCP region (e.g., us-central1)

# Expose port for Cloud Run
EXPOSE 8080

# Run Streamlit app via main.py
CMD ["uv", "run", "python", "main.py"]
