#!/usr/bin/env python3
"""
Simple test script to debug the FastAPI server
"""
import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

print("🔍 Testing FastAPI server components...")

try:
    # Test FastAPI import
    from fastapi import FastAPI
    print("✅ FastAPI imported successfully")
    
    # Test uvicorn import
    import uvicorn
    print("✅ Uvicorn imported successfully")
    
    # Test our main module
    import main
    print("✅ Main module imported successfully")
    
    # Test the app object
    app = main.app
    print("✅ FastAPI app object created successfully")
    
    # Test health endpoint function
    from main import health_check
    print("✅ Health check function imported successfully")
    
    # Test if we can create a simple FastAPI app
    test_app = FastAPI()
    
    @test_app.get("/test")
    def test_endpoint():
        return {"status": "ok"}
    
    print("✅ Simple FastAPI app created successfully")
    
    print("\n🎉 All components are working!")
    print("The issue might be in the server startup or routing.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
