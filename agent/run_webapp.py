#!/usr/bin/env python3
"""
Startup script to run both ADK server and Streamlit webapp
"""
import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def run_adk_server():
    """Run the ADK server in the background"""
    print("🚀 Starting ADK Health Agent Server...")
    try:
        # Run ADK server
        process = subprocess.Popen([
            sys.executable, "-m", "uv", "run", "adk", "web", 
            "--host", "0.0.0.0", "--port", "8080"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ ADK Server started on http://localhost:8080")
        return process
    except Exception as e:
        print(f"❌ Error starting ADK server: {e}")
        return None

def run_streamlit_app():
    """Run the Streamlit webapp"""
    print("🌐 Starting Streamlit Health Intelligence Hub...")
    try:
        # Run Streamlit app
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ])
        
        print("✅ Streamlit app started on http://localhost:8501")
        return process
    except Exception as e:
        print(f"❌ Error starting Streamlit app: {e}")
        return None

def main():
    """Main function to start both services"""
    print("🏥 Health Intelligence Hub - Starting Services")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Error: app.py not found. Please run this script from the agent directory.")
        sys.exit(1)
    
    # Start ADK server
    adk_process = run_adk_server()
    if not adk_process:
        print("❌ Failed to start ADK server. Exiting.")
        sys.exit(1)
    
    # Wait a bit for ADK server to start
    print("⏳ Waiting for ADK server to initialize...")
    time.sleep(5)
    
    # Start Streamlit app
    streamlit_process = run_streamlit_app()
    if not streamlit_process:
        print("❌ Failed to start Streamlit app. Exiting.")
        adk_process.terminate()
        sys.exit(1)
    
    print("\n🎉 Health Intelligence Hub is now running!")
    print("=" * 50)
    print("📊 Streamlit Webapp: http://localhost:8501")
    print("🤖 ADK Health Agents: http://localhost:8080")
    print("=" * 50)
    print("Press Ctrl+C to stop both services")
    
    def signal_handler(sig, frame):
        print("\n🛑 Shutting down services...")
        if adk_process:
            adk_process.terminate()
        if streamlit_process:
            streamlit_process.terminate()
        print("✅ Services stopped.")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Wait for processes
        while True:
            if adk_process.poll() is not None:
                print("❌ ADK server stopped unexpectedly")
                break
            if streamlit_process.poll() is not None:
                print("❌ Streamlit app stopped unexpectedly")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
