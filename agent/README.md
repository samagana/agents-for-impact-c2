# Running with Docker

## Build the Docker Image
```sh
cd agent
# Build the Docker image
docker build -t c2-healthcare-agent:latest .
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

# Tag the image for Artifact Registry
docker tag c2-healthcare-agent:latest us-docker.pkg.dev/qwiklabs-gcp-04-91797af16116/c2-healthcare-agent/c2-healthcare-agent:latest

# Push the image
docker push us-docker.pkg.dev/qwiklabs-gcp-04-91797af16116/c2-healthcare-agent/c2-healthcare-agent:latest
```

**Note:** The .env file is NOT included in the Docker image. Supply secrets via `--env-file`, Docker secrets, or environment variables as appropriate for your deployment.
