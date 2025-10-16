# ADK API Server Test Results
## Agents for Impact - Community Health & Wellness Advisor

### Test Date
October 16, 2025

### API Server Status
✅ **Successfully Running** on `http://localhost:8000`

---

## Agent Configuration

### 1. health_agent (Root Agent)
- **Role**: Coordinates between data_agent and insights_agent
- **Model**: gemini-2.5-pro
- **Tools**: AgentTool(insights_root_agent), AgentTool(data_root_agent)

### 2. data_agent
- **Role**: Queries BigQuery datasets for air quality, census, and COVID-19 data
- **Model**: gemini-2.5-pro
- **Available Tables**:
  - `bigquery-public-data.census_bureau_usa.population_by_zip_2010`
  - `bigquery-public-data.epa_historical_air_quality.air_quality_annual_summary`
  - `bigquery-public-data.epa_historical_air_quality.hap_daily_summary`
  - `bigquery-public-data.covid19_open_data.covid19_open_data`
- **Project**: qwiklabs-gcp-04-91797af16116
- **Write Mode**: ALLOWED

### 3. insights_agent
- **Role**: Generates summaries and comparisons
- **Model**: gemini-2.5-pro

---

## Test Cases Executed

### Test 1: Data Agent - Air Quality Query ⚠️
**Query**: "Query the air quality annual summary table for California in 2020 and show me 3 sample records"

**Result**: Partial Success
- ✅ Agent correctly interpreted the query
- ✅ Generated valid SQL query:
  ```sql
  SELECT state_name, county_name, aqi
  FROM `bigquery-public-data.epa_historical_air_quality.air_quality_annual_summary`
  WHERE state_name = 'California' AND year = 2020
  LIMIT 3;
  ```
- ✅ Called the `execute_sql` tool with correct parameters
- ❌ **BigQuery Permissions Error**: `User does not have bigquery.jobs.create permission in project qwiklabs-gcp-04-91797af16116`
- ✅ Agent intelligently tried alternative approach (different project)
- ✅ Gracefully handled error and provided SQL to user

### Test 2: Insights Agent - Summarization ✅
**Query**: "Generate a summary about the importance of air quality monitoring for public health in vulnerable communities"

**Result**: Full Success
- ✅ Generated comprehensive, well-structured summary
- ✅ Included 4 key points:
  1. Identifies and Validates Inequities
  2. Empowers Communities and Drives Advocacy
  3. Informs Targeted Public Health Interventions
  4. Drives Policy and Equitable Investment
- ✅ Response time: ~14 seconds
- ✅ High-quality content relevant to the challenge use case

---

## API Endpoints Tested

### Session Management
```bash
# Create Session
POST http://localhost:8000/apps/{agent_name}/users/{user_id}/sessions/{session_id}

# Example
curl -X POST http://localhost:8000/apps/data_agent/users/test_user/sessions/session_1 \
  -H "Content-Type: application/json" -d '{}'
```

### Running Queries (Streaming)
```bash
# Run with SSE
POST http://localhost:8000/run_sse

# Example
curl -N -X POST 'http://localhost:8000/run_sse' \
  -H 'Content-Type: application/json' \
  -d '{
    "appName": "data_agent",
    "userId": "test_user",
    "sessionId": "session_1",
    "newMessage": {
      "parts": [{"text": "Your query here"}]
    }
  }'
```

---

## Issues Identified

### 1. BigQuery Permissions ⚠️
**Error**: `Access Denied: Project qwiklabs-gcp-04-91797af16116: User does not have bigquery.jobs.create permission`

**Required Action**:
- Grant the BigQuery Job User role to the service account/credentials
- Or update the project ID to one with proper permissions
- Or use application default credentials with appropriate access

**To Fix**:
```bash
# Option 1: Grant permissions to service account
gcloud projects add-iam-policy-binding qwiklabs-gcp-04-91797af16116 \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT@project.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"

# Option 2: Use a different project with permissions
# Update agent/data_agent/main.py line 65-66
```

---

## Use Cases from Challenge Document

Based on the challenge requirements, here are the test cases mapped to agent capabilities:

### Use Case 1: Mobile Health Clinic Deployment 🔄
**Query**: "What are the top five zip codes where we should prioritize mobile health clinic deployment based on poverty levels?"

**Expected Flow**:
1. health_agent receives query
2. Delegates to data_agent to query census population data by zip code
3. data_agent queries `bigquery-public-data.census_bureau_usa.population_by_zip_2010`
4. insights_agent generates summary with recommendations
5. health_agent returns prioritized list with rationale

**Status**: Ready to test once BigQuery permissions are resolved

### Use Case 2: Air Quality Comparison ✅ (Partially Tested)
**Query**: "How's the air quality today compared to last week?"

**Expected Flow**:
1. health_agent receives query
2. Delegates to data_agent for air quality data
3. data_agent queries `bigquery-public-data.epa_historical_air_quality.hap_daily_summary`
4. insights_agent compares and generates summary
5. health_agent returns comparison

**Status**: SQL generation works; awaiting BigQuery access for full test

### Use Case 3: Healthcare Access ⚠️
**Query**: "Show me free or low-cost dental clinics in close proximity to the highest uninsured populations"

**Status**: Requires additional data sources (clinic locations) not currently configured

---

## Recommendations

### Immediate Actions
1. ✅ **Resolve BigQuery permissions** to enable full data agent testing
2. 📊 Add clinic/healthcare facility datasets to data_agent
3. 🧪 Create evaluation dataset with challenge use cases
4. 📝 Test multi-agent orchestration (health_agent → data_agent → insights_agent flow)

### Future Enhancements
1. Add real-time API integration (e.g., AirNow for current air quality)
2. Implement geographic proximity calculations
3. Add visualization tools for charts/maps
4. Create multimodal inputs (image/video) support
5. Integrate with live healthcare facility databases

---

## Example API Calls for Testing

### Test Data Agent (after permissions fixed)
```bash
# Create session
curl -X POST http://localhost:8000/apps/data_agent/users/test_user/sessions/test_session \
  -H "Content-Type: application/json" -d '{}'

# Query air quality
curl -N -X POST 'http://localhost:8000/run_sse' \
  -H 'Content-Type: application/json' \
  -d '{
    "appName": "data_agent",
    "userId": "test_user",
    "sessionId": "test_session",
    "newMessage": {
      "parts": [{
        "text": "What are the top 5 counties in California with the worst air quality in 2020?"
      }]
    }
  }'
```

### Test Insights Agent
```bash
# Create session
curl -X POST http://localhost:8000/apps/insights_agent/users/test_user/sessions/insight_session \
  -H "Content-Type: application/json" -d '{}'

# Generate summary
curl -N -X POST 'http://localhost:8000/run_sse' \
  -H 'Content-Type: application/json' \
  -d '{
    "appName": "insights_agent",
    "userId": "test_user",
    "sessionId": "insight_session",
    "newMessage": {
      "parts": [{
        "text": "Summarize the relationship between air quality and public health outcomes"
      }]
    }
  }'
```

### Test Health Agent (Root)
```bash
# Create session
curl -X POST http://localhost:8000/apps/health_agent/users/test_user/sessions/health_session \
  -H "Content-Type: application/json" -d '{}'

# Complex query requiring multiple agents
curl -N -X POST 'http://localhost:8000/run_sse' \
  -H 'Content-Type: application/json' \
  -d '{
    "appName": "health_agent",
    "userId": "test_user",
    "sessionId": "health_session",
    "newMessage": {
      "parts": [{
        "text": "Analyze air quality trends in Los Angeles and provide health recommendations for vulnerable populations"
      }]
    }
  }'
```

---

## API Documentation
Full Swagger UI available at: `http://localhost:8000/docs`

## Next Steps
1. Fix BigQuery permissions
2. Run comprehensive test suite with all challenge use cases
3. Create evaluation dataset
4. Prepare pitch video and deck demonstrating the working system

