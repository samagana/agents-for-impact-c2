# Google Agents for Impact - Squad C2

## Pre-requisites
1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Copy `agent/.env.template` to `agent/.env` and fill in the values.
3. Run the following to start the ADK web session
```
cd agent
uv run adk web
```
4. Install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk)
5. Authenticate to Google Cloud
```
gcloud auth login
gcloud auth application-default login
gcloud config set project qwiklabs-gcp-04-91797af16116
```
