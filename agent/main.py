"""
Main entry point for Cloud Run deployment
Runs the Streamlit Health Intelligence Hub application
"""
import os
import sys

# Ensure Streamlit uses the PORT environment variable from Cloud Run
port = int(os.getenv("PORT", 8080))
os.environ["STREAMLIT_SERVER_PORT"] = str(port)
os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

# Run Streamlit app
if __name__ == "__main__":
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", "app.py", "--server.port", str(port), "--server.address", "0.0.0.0"]
    sys.exit(stcli.main())
