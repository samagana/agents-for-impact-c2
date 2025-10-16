# Running with Docker

## Build the Docker Image
```sh
cd agent
# Build the Docker image with a tag, e.g., adk-agent:latest
docker build -t adk-agent:latest .
```

## Run the App in a Container
```sh
# Provide your .env file by mounting it at runtime. Adjust the path to your .env as needed.
docker run --env-file .env -p 8080:8080 adk-agent:latest
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
docker tag adk-agent:latest us-docker.pkg.dev/qwiklabs-gcp-04-91797af16116/c2-healthcare-agent/adk-agent:latest

# Push the image
docker push us-docker.pkg.dev/qwiklabs-gcp-04-91797af16116/c2-healthcare-agent/adk-agent:latest
```

**Note:** The .env file is NOT included in the Docker image. Supply secrets via `--env-file`, Docker secrets, or environment variables as appropriate for your deployment.
