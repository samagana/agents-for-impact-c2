# syntax=docker/dockerfile:1

# --- Frontend Builder ---
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Install pnpm
RUN npm install -g pnpm

# Copy frontend files
COPY health-agent/package.json health-agent/pnpm-lock.yaml ./
COPY health-agent/src ./src
COPY health-agent/public ./public
COPY health-agent/next.config.ts health-agent/tsconfig.json health-agent/postcss.config.mjs ./
COPY health-agent/.eslintrc* ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Build Next.js app
RUN pnpm build

# --- Backend Builder ---
FROM python:3.12-slim AS backend-builder

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

# --- Runtime image ---
FROM python:3.12-slim

WORKDIR /app

# Install Node.js runtime for frontend
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Install pnpm
RUN npm install -g pnpm

# Copy backend code first
COPY agent/ /agent/

# Copy backend virtual environment (after code to avoid being overwritten)
COPY --from=backend-builder /agent/.venv /agent/.venv

# Copy frontend build output
COPY --from=frontend-builder /app/frontend/.next /app/frontend/.next
COPY --from=frontend-builder /app/frontend/public /app/frontend/public
COPY --from=frontend-builder /app/frontend/package.json /app/frontend/package.json
COPY --from=frontend-builder /app/frontend/node_modules /app/frontend/node_modules

# Copy startup script
COPY agent/scripts/start.sh /app/scripts/start.sh
RUN chmod +x /app/scripts/start.sh

EXPOSE 3000 8000

# Environment variables (set these at runtime for security)
# GOOGLE_API_KEY - Required: Your Google API key
# GOOGLE_CLOUD_PROJECT - Required: Your GCP project ID
# GOOGLE_CLOUD_LOCATION - Required: GCP region (e.g., us-central1)

ENV BACKEND_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=http://localhost:8000

CMD ["/app/scripts/start.sh"]
