# syntax=docker/dockerfile:1
# Multi-stage Dockerfile for Cloud Run
# Builds and runs both API server (FastAPI) and UI (Next.js)

# --- Stage 1: Build Python Backend ---
FROM python:3.12-slim AS python-builder

WORKDIR /agent

# Install uv
RUN pip install uv

# Copy dependency files and source code
COPY agent/pyproject.toml agent/uv.lock ./
COPY agent/data_agent ./data_agent
COPY agent/health_agent ./health_agent
COPY agent/insights_agent ./insights_agent
COPY agent/search_agent ./search_agent
COPY agent/maps_agent ./maps_agent
COPY agent/api_server ./api_server
COPY agent/README.md ./
RUN uv sync --frozen --no-dev

# --- Stage 2: Build Next.js Frontend ---
FROM node:20-slim AS node-builder

WORKDIR /ui

# Copy package files and scripts
COPY health-agent/package.json ./
COPY health-agent/scripts ./scripts

# Install ALL dependencies including devDependencies (needed for build)
RUN npm install --ignore-scripts

# Copy frontend source
COPY health-agent/ ./

# Build Next.js app
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# --- Stage 3: Runtime Image ---
FROM python:3.12-slim

WORKDIR /app

# Install Node.js and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy Python virtual environment and dependencies
COPY --from=python-builder /agent/.venv /app/agent/.venv
COPY --from=python-builder /agent /app/agent/

# Copy Next.js build output and dependencies
COPY --from=node-builder /ui/.next /app/ui/.next
COPY --from=node-builder /ui/node_modules /app/ui/node_modules
COPY --from=node-builder /ui/package.json /app/ui/package.json
COPY --from=node-builder /ui/next.config.ts /app/ui/next.config.ts
COPY --from=node-builder /ui/public /app/ui/public

# Copy startup script
COPY agent/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# DO NOT copy .env; mount at runtime

EXPOSE 8080
ENV PORT=8080
ENV API_PORT=8081
ENV ADK_HOST=0.0.0.0
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Environment variables (set these at runtime for security)
# GOOGLE_API_KEY - Required: Your Google API key
# GOOGLE_CLOUD_PROJECT - Required: Your GCP project ID
# GOOGLE_CLOUD_LOCATION - Required: GCP region (e.g., us-central1)

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1

# Use startup script to run both API server and UI
ENTRYPOINT ["/app/start.sh"]
