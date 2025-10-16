# Cloud Run Deployment Instructions

## Prerequisites
- Docker installed
- gcloud CLI installed and authenticated
- GCP project with billing enabled
- Container Registry API enabled

## Build and Deploy Steps

### 1. Set Environment Variables
```bash
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"
export SERVICE_NAME="agents-for-impact"
```

### 2. Build the Docker Image
```bash
cd agents-for-impact-c2
docker buildx build --platform linux/amd64 -t $SERVICE_NAME:latest .
```

### 3. Tag the Image
```bash
# For Artifact Registry (recommended)
docker tag $SERVICE_NAME:latest us-docker.pkg.dev/$PROJECT_ID/$SERVICE_NAME/$SERVICE_NAME:latest

# OR for Container Registry (legacy)
docker tag $SERVICE_NAME:latest gcr.io/$PROJECT_ID/$SERVICE_NAME:latest
```

### 4. Push to Google Container Registry or Artifact Registry
```bash
# For Artifact Registry
docker push us-docker.pkg.dev/$PROJECT_ID/$SERVICE_NAME/$SERVICE_NAME:latest

# OR for Container Registry
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest
```

### 5. Deploy to Cloud Run
```bash
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --min-instances 0 \
  --set-env-vars="NODE_ENV=production,PORT=8080,API_PORT=8081,ADK_HOST=0.0.0.0,NEXT_TELEMETRY_DISABLED=1,GOOGLE_API_KEY=your-api-key,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION"
```

### 6. Update Deployment (after code changes)
```bash
# Rebuild
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:latest .

# Push
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest

# Redeploy (Cloud Run will automatically pull the new image)
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
  --region $REGION
```

## Required Environment Variables

Set these during deployment:

- `GOOGLE_API_KEY` - Your Google API key (required)
- `GOOGLE_CLOUD_PROJECT` - Your GCP project ID (required)
- `GOOGLE_CLOUD_LOCATION` - GCP region like us-central1 (required)
- `PORT` - Port for the UI (default: 8080)
- `API_PORT` - Port for the API server (default: 8081)

## What's Running

The container runs:
1. **API Server** (FastAPI) - Backend agents on port 8081
2. **UI Server** (Next.js) - Frontend on port 8080

Both services start automatically via the `start.sh` script.

## Troubleshooting

### View Logs
```bash
gcloud run services logs read $SERVICE_NAME --region $REGION
```

### Check Service Status
```bash
gcloud run services describe $SERVICE_NAME --region $REGION
```

### Test Locally First
```bash
# Build
docker build -t agents-for-impact:local .

# Run with environment variables
docker run -p 8080:8080 \
  -e GOOGLE_API_KEY=your-key \
  -e GOOGLE_CLOUD_PROJECT=your-project \
  -e GOOGLE_CLOUD_LOCATION=us-central1 \
  agents-for-impact:local
```

## Notes

- The Dockerfile uses multi-stage builds to optimize image size
- The build context must be the `agents-for-impact-c2/agent` directory
- Make sure to set all required environment variables
- Cloud Run will handle scaling automatically based on traffic
