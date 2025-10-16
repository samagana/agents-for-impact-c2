#!/usr/bin/env python3
"""
Minimal FastAPI server for testing
"""
import os
from fastapi import FastAPI
import uvicorn

# Create FastAPI app
app = FastAPI(title="Health Intelligence Hub Test")

@app.get("/")
async def root():
    return {"message": "Health Intelligence Hub is running!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "health-intelligence-hub-test",
        "version": "1.0.0"
    }

@app.get("/test")
async def test_endpoint():
    return {"test": "success"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting minimal FastAPI server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
