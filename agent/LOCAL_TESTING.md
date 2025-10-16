# 🧪 Local Testing Guide

## Quick Start

### Prerequisites
1. **Environment Variables**: Create a `.env` file with:
```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-04-91797af16116
GOOGLE_CLOUD_LOCATION=us-central1
```

2. **Dependencies**: Install dependencies
```bash
cd agent
uv sync
```

## Testing Options

### Option 1: Automated Testing Script (Recommended)
```bash
python test_local.py
```
This script provides interactive options to test different components.

### Option 2: FastAPI Server Only
```bash
# Start FastAPI server
uv run python main.py

# In another terminal, test the API
curl http://localhost:8080/health
curl http://localhost:8080/docs  # API documentation
```

### Option 3: Streamlit App Only
```bash
# Start Streamlit app
uv run streamlit run app.py --server.port 8501

# Open browser to http://localhost:8501
```

### Option 4: Both Services (Original Setup)
```bash
# Start both services
python run_webapp.py

# Or start manually:
# Terminal 1: ADK server
uv run adk web --host 0.0.0.0 --port 8080

# Terminal 2: Streamlit app
uv run streamlit run app.py --server.port 8501
```

### Option 5: Docker Testing
```bash
# Build and run with Docker
docker build -t health-intelligence-hub:local .
docker run -p 8080:8080 --env-file .env health-intelligence-hub:local

# Test the container
curl http://localhost:8080/health
```

### Option 6: Docker Compose
```bash
# Start all services
docker-compose up

# Test the services
curl http://localhost:8501  # Streamlit app
curl http://localhost:8080/health  # FastAPI health check
```

## Testing Endpoints

### FastAPI Endpoints
- **Health Check**: `GET http://localhost:8080/health`
- **API Documentation**: `GET http://localhost:8080/docs`
- **Chat API**: `POST http://localhost:8080/api/chat`
- **Insights API**: `GET http://localhost:8080/api/insights/{location}`
- **Sample Data**: `GET http://localhost:8080/api/sample-data/chronic-disease`

### Streamlit App
- **Main App**: `http://localhost:8501`
- **Dashboard**: Interactive health intelligence dashboard
- **Chat Interface**: Conversational AI for health queries
- **Data Visualization**: Charts, maps, and analytics

## Testing the Chat API

```bash
# Test chat endpoint
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the health risks in San Francisco?",
    "user_role": "Public Health Staff",
    "location": "San Francisco, CA"
  }'
```

## Testing Sample Data

```bash
# Get chronic disease data
curl http://localhost:8080/api/sample-data/chronic-disease

# Get resource data
curl http://localhost:8080/api/sample-data/resources

# Get risk factors
curl http://localhost:8080/api/sample-data/risk-factors
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Find and kill process using port 8080
lsof -ti:8080 | xargs kill -9

# Or use different ports
uv run streamlit run app.py --server.port 8502
```

2. **Environment Variables Not Loaded**
```bash
# Check if .env file exists and has correct format
cat .env

# Load environment variables manually
export GOOGLE_API_KEY=your-key
export GOOGLE_CLOUD_PROJECT=your-project
```

3. **Dependencies Not Installed**
```bash
# Reinstall dependencies
uv sync --reinstall
```

4. **Docker Issues**
```bash
# Clean up Docker resources
docker system prune -a

# Rebuild image
docker build --no-cache -t health-intelligence-hub:local .
```

### Health Checks

```bash
# Check if services are running
curl http://localhost:8080/health
curl http://localhost:8501

# Check Docker containers
docker ps
docker logs health-hub-test

# Check processes
ps aux | grep python
```

## Expected Outputs

### FastAPI Health Check
```json
{
  "status": "healthy",
  "service": "health-intelligence-hub",
  "version": "1.0.0"
}
```

### Chat API Response
```json
{
  "response": "Based on current data, I recommend focusing on diabetes prevention programs in high-risk areas.",
  "user_role": "Public Health Staff",
  "location": "San Francisco, CA"
}
```

### Streamlit App
- Interactive dashboard with health metrics
- Chat interface for health queries
- Data visualization components
- Geographic health mapping

## Performance Testing

```bash
# Load test the API
for i in {1..10}; do
  curl -s http://localhost:8080/health > /dev/null
  echo "Request $i completed"
done

# Test concurrent requests
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message", "user_role": "Residents", "location": "Oakland, CA"}' &
```

## Next Steps

After successful local testing:
1. **Deploy to Cloud Run**: Use `./deploy_cloudrun.sh`
2. **Monitor Performance**: Check logs and metrics
3. **Scale as Needed**: Adjust Cloud Run settings
4. **Add Features**: Extend the application based on feedback

## Support

If you encounter issues:
1. Check the logs: `docker logs health-hub-test`
2. Verify environment variables
3. Test individual components
4. Check network connectivity
5. Review the troubleshooting section above
