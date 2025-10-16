from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from health_agent import root_agent

adk_health_agent = ADKAgent(
    adk_agent=root_agent,
    app_name="health_agent",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)


app = FastAPI(title="ADK Health Agent")

# Add CORS middleware to allow UI to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your UI domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the ADK endpoint
add_adk_fastapi_endpoint(app, adk_health_agent, path="/")

if __name__ == "__main__":
    import os
    import uvicorn

    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY environment variable not set!")
        print("   Set it with: export GOOGLE_API_KEY='your-key-here'")
        print("   Get a key from: https://makersuite.google.com/app/apikey")
        print()

    # Use API_PORT for the API server, PORT is for the UI
    port = int(os.getenv("API_PORT", os.getenv("PORT", 8080)))
    uvicorn.run(app, host="0.0.0.0", port=port)
