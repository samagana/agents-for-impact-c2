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

# Install uv
RUN pip install uv

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv

# Copy application code
COPY . .
# DO NOT copy .env; mount at runtime

EXPOSE 8080
ENV ADK_HOST=0.0.0.0
ENV ADK_PORT=8080

# Environment variables (set these at runtime for security)
# GOOGLE_API_KEY - Required: Your Google API key
# GOOGLE_CLOUD_PROJECT - Required: Your GCP project ID
# GOOGLE_CLOUD_LOCATION - Required: GCP region (e.g., us-central1)

ENTRYPOINT ["uv", "run", "adk", "web", "--host", "0.0.0.0", "--port", "8080"]
