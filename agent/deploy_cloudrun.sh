#!/bin/bash

# Health Intelligence Hub - Cloud Run Deployment Script
# This script builds and deploys the application to Google Cloud Run

set -e

# Configuration
PROJECT_ID="qwiklabs-gcp-04-91797af16116"
SERVICE_NAME="health-intelligence-hub"
REGION="us-central1"
IMAGE_NAME="health-intelligence-hub"
REPOSITORY="c2-healthcare-agent"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🏥 Health Intelligence Hub - Cloud Run Deployment${NC}"
echo "=================================================="

# Check if required environment variables are set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo -e "${RED}❌ Error: GOOGLE_API_KEY environment variable is not set${NC}"
    echo "Please set your Google API key:"
    echo "export GOOGLE_API_KEY=your-api-key"
    exit 1
fi

if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo -e "${YELLOW}⚠️  Warning: GOOGLE_CLOUD_PROJECT not set, using default: $PROJECT_ID${NC}"
    export GOOGLE_CLOUD_PROJECT=$PROJECT_ID
fi

if [ -z "$GOOGLE_CLOUD_LOCATION" ]; then
    echo -e "${YELLOW}⚠️  Warning: GOOGLE_CLOUD_LOCATION not set, using default: $REGION${NC}"
    export GOOGLE_CLOUD_LOCATION=$REGION
fi

echo -e "${GREEN}✅ Environment variables configured${NC}"
echo "Project ID: $PROJECT_ID"
echo "Service Name: $SERVICE_NAME"
echo "Region: $REGION"

# Authenticate with Google Cloud
echo -e "${BLUE}🔐 Authenticating with Google Cloud...${NC}"
gcloud auth login --no-launch-browser
gcloud config set project $PROJECT_ID

# Configure Docker to use gcloud credentials for Artifact Registry
echo -e "${BLUE}🐳 Configuring Docker for Artifact Registry...${NC}"
gcloud auth configure-docker us-docker.pkg.dev

# Build the Docker image
echo -e "${BLUE}🔨 Building Docker image...${NC}"
docker buildx build --platform linux/amd64 -t $IMAGE_NAME:latest .

# Tag the image for Artifact Registry
echo -e "${BLUE}🏷️  Tagging image for Artifact Registry...${NC}"
docker tag $IMAGE_NAME:latest us-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:latest

# Push the image to Artifact Registry
echo -e "${BLUE}📤 Pushing image to Artifact Registry...${NC}"
docker push us-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:latest

# Deploy to Cloud Run
echo -e "${BLUE}🚀 Deploying to Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
    --image us-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:latest \
    --platform managed \
    --project=$PROJECT_ID \
    --region=$REGION \
    --allow-unauthenticated \
    --timeout=300 \
    --memory=2048Mi \
    --cpu=2 \
    --cpu-boost \
    --min-instances=0 \
    --max-instances=10 \
    --concurrency=80 \
    --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION

# Get the service URL
echo -e "${BLUE}🔗 Getting service URL...${NC}"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region=$REGION --format 'value(status.url)')

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo "=================================================="
echo -e "${GREEN}🌐 Service URL: $SERVICE_URL${NC}"
echo -e "${GREEN}📊 Health Intelligence Hub is now live!${NC}"
echo "=================================================="

# Test the deployment
echo -e "${BLUE}🧪 Testing deployment...${NC}"
if curl -f -s "$SERVICE_URL/health" > /dev/null; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
    echo "Please check the Cloud Run logs:"
    echo "gcloud run services logs read $SERVICE_NAME --region=$REGION"
fi

echo -e "${BLUE}📋 Useful commands:${NC}"
echo "View logs: gcloud run services logs read $SERVICE_NAME --region=$REGION"
echo "Update service: ./deploy_cloudrun.sh"
echo "Delete service: gcloud run services delete $SERVICE_NAME --region=$REGION"

echo -e "${GREEN}🎉 Health Intelligence Hub is ready for use!${NC}"
