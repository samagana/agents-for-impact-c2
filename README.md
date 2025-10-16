# Community Health & Wellness Advisor

**Google Agents for Impact - Squad C2**

An AI-powered multi-agent system that provides hyper-local, actionable health intelligence for public health decision-making, community organizations, and residents.

## 🎯 Mission

Support data-driven health equity and crisis readiness by providing:
- **Mobile clinic deployment** recommendations based on demographics and location
- **Environmental health monitoring** with real-time and historical air quality data
- **Healthcare access information** with facility discovery and directions
- **Health outcome analysis** using CDC and state health data

## 🏗️ System Architecture

### 5-Agent Team
```
health_agent (Orchestrator - Gemini 2.5 Pro)
  ├── data_agent (BigQuery) - Demographics, health outcomes, air quality datasets
  ├── search_agent (Google Search) - Real-time information, alerts, current conditions
  ├── maps_agent (Google Maps MCP) - Facility search, directions, travel times
  └── insights_agent (Analysis) - Summaries, comparisons, recommendations
```

## 📋 Example Queries

```
"Where should we deploy a mobile clinic in LA County to serve uninsured residents?"
"Find low-cost dental clinics near 90001 and calculate travel times"
"What's the current air quality in downtown LA compared to EPA standards?"
"Identify healthcare deserts based on poverty and clinic accessibility"
"Find the nearest urgent care to 123 Main St that's open now"
```

## 🚀 Quick Start

### Prerequisites
1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/) (or use pip)
2. [Install Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk)
3. [Install Node.js](https://nodejs.org/) (for Google Maps MCP server)

### Setup

1. **Authenticate to Google Cloud**
```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project qwiklabs-gcp-04-91797af16116
```

2. **Configure API Keys**

Create `agent/.env` with:
```bash
GOOGLE_API_KEY="your_gemini_api_key"
GOOGLE_CLOUD_PROJECT="qwiklabs-gcp-04-91797af16116"
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_MAPS_API_KEY="your_maps_api_key"
```

Get API keys:
- **Gemini API**: https://aistudio.google.com/app/apikey
- **Google Maps API**: https://console.cloud.google.com/google/maps-apis
  - Enable: Maps JavaScript API, Places API, Directions API, Distance Matrix API, Geocoding API

3. **Run the Application**
```bash
cd agent
uv run adk web
# or
adk web
```

Then open http://127.0.0.1:8000 in your browser.

## 📁 Project Structure
```
agent/
  ├── data_agent/      - BigQuery datasets (18+ datasets)
  ├── search_agent/    - Google Search (real-time info)
  ├── maps_agent/      - Google Maps MCP (location services)
  ├── insights_agent/  - Analysis and summaries
  ├── health_agent/    - Orchestrator (root agent)
  └── .env            - API keys (create from template)
```

## 🔧 Technology Stack

- **ADK (Agent Development Kit)** - Google's framework for building AI agents
- **Gemini 2.5 Pro / 2.0 Flash** - Large language models
- **BigQuery** - Data warehouse with health and demographic datasets
- **Google Maps Platform** - Location services (Places, Directions, Distance Matrix APIs)
- **Google Search** - Real-time information

## 📚 Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup and troubleshooting
- [GOOGLE_MAPS_INTEGRATION_PLAN.md](GOOGLE_MAPS_INTEGRATION_PLAN.md) - Maps MCP architecture
- [ADK Documentation](https://google.github.io/adk-docs/) - Official ADK docs

## ✨ Key Features

- **📊 18+ BigQuery Datasets**: Demographics, air quality, health outcomes, hospital ratings
- **🔍 Real-time Search**: Current air quality, health alerts, clinic hours
- **🗺️ Location Services**: Find facilities, calculate travel times, get directions
- **🤖 Multi-Agent Intelligence**: Automatic routing to specialized agents
- **💡 Actionable Insights**: Data-driven recommendations for health interventions
