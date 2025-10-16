# Running with Docker

## Build the Docker Image
```sh
cd agent
# Build the Docker image for linux/amd64 (required for Cloud Run)
docker buildx build --platform linux/amd64 -t c2-healthcare-agent:latest .
```

## Run the App in a Container

### Option 1: Using .env file (Recommended for local development)
```sh
# Provide your .env file at runtime
docker run --env-file .env -p 8080:8080 c2-healthcare-agent:latest
```

### Option 2: Set environment variables individually
```sh
docker run -p 8080:8080 \
  -e GOOGLE_API_KEY=your-api-key \
  -e GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-04-91797af16116 \
  -e GOOGLE_CLOUD_LOCATION=us-central1 \
  c2-healthcare-agent:latest
```

By default, the service runs on port 8080 inside the container.

## Access the Application
Once the container is running, access the application at:
```
http://localhost:8080
```

## Push to Google Artifact Registry
To push the image to Google Artifact Registry:

```sh
# Authenticate with Google Cloud
gcloud auth login

# Configure Docker to use gcloud credentials for Artifact Registry
gcloud auth configure-docker us-docker.pkg.dev

# Build, tag, and push in one command
docker buildx build --platform linux/amd64 -t c2-healthcare-agent:latest . && \
docker tag c2-healthcare-agent:latest us-docker.pkg.dev/qwiklabs-gcp-04-91797af16116/c2-healthcare-agent/c2-healthcare-agent:latest && \
docker push us-docker.pkg.dev/qwiklabs-gcp-04-91797af16116/c2-healthcare-agent/c2-healthcare-agent:latest
```

## Deploy to Google Cloud Run

### Option 1: Automated Deployment (Recommended)
Use the provided deployment script for easy deployment:

```sh
# Set your environment variables
export GOOGLE_API_KEY=your-api-key
export GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-04-91797af16116
export GOOGLE_CLOUD_LOCATION=us-central1

# Run the deployment script
./deploy_cloudrun.sh
```

### Option 2: Manual Deployment
Deploy the containerized application to Cloud Run with appropriate resources:

```sh
# Build, tag, and push in one command
docker buildx build --platform linux/amd64 -t health-intelligence-hub:latest . && \
docker tag health-intelligence-hub:latest us-docker.pkg.dev/qwiklabs-gcp-04-91797af16116/c2-healthcare-agent/health-intelligence-hub:latest && \
docker push us-docker.pkg.dev/qwiklabs-gcp-04-91797af16116/c2-healthcare-agent/health-intelligence-hub:latest

# Deploy to Cloud Run
gcloud run deploy health-intelligence-hub \
    --image us-docker.pkg.dev/qwiklabs-gcp-04-91797af16116/c2-healthcare-agent/health-intelligence-hub:latest \
    --platform managed \
    --project=qwiklabs-gcp-04-91797af16116 \
    --region us-central1 \
    --allow-unauthenticated \
    --timeout=300 \
    --memory=2048Mi \
    --cpu=2 \
    --cpu-boost \
    --min-instances=0 \
    --max-instances=10 \
    --concurrency=80 \
    --set-env-vars GOOGLE_API_KEY=your-api-key,GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-04-91797af16116,GOOGLE_CLOUD_LOCATION=us-central1
```

Replace `your-api-key` with your actual Google API key.

**Important:** When setting environment variables:
- Do NOT use quotes around values in the `--set-env-vars` command
- Example: `GOOGLE_API_KEY=AIzaSy...` ✅ (correct)
- Example: `GOOGLE_API_KEY="AIzaSy..."` ❌ (incorrect - will cause "API key not valid" error)

**Note:** The deployment requires:
- **Memory:** 2048Mi (to handle BigQuery and AI model operations, avoid 512Mi default limit)
- **CPU:** 2 cores (for better performance)
- **CPU Boost:** Enabled (to speed up container startup)
- **Timeout:** 300 seconds (to allow for model initialization)
- **Concurrency:** 80 (for optimal performance)
- **Auto-scaling:** 0-10 instances based on demand
**Note:** The .env file is NOT included in the Docker image. Supply secrets via `--env-file`, Docker secrets, or environment variables as appropriate for your deployment.
