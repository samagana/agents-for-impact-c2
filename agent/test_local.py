#!/usr/bin/env python3
"""
Local testing script for Health Intelligence Hub
Tests both the FastAPI server and Streamlit app locally
"""
import subprocess
import sys
import time
import requests
import webbrowser
from pathlib import Path
import os

def test_fastapi_server():
    """Test the FastAPI server locally"""
    print("🚀 Testing FastAPI server...")
    
    try:
        # Start FastAPI server
        process = subprocess.Popen([
            sys.executable, "-m", "uv", "run", "python", "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        print("⏳ Waiting for FastAPI server to start...")
        time.sleep(10)
        
        # Test health endpoint
        try:
            response = requests.get("http://localhost:8080/health", timeout=5)
            if response.status_code == 200:
                print("✅ FastAPI server is running!")
                print(f"📊 Health check response: {response.json()}")
                return process
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to FastAPI server: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting FastAPI server: {e}")
        return None

def test_streamlit_app():
    """Test the Streamlit app locally"""
    print("🌐 Testing Streamlit app...")
    
    try:
        # Start Streamlit app
        process = subprocess.Popen([
            sys.executable, "-m", "uv", "run", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for app to start
        print("⏳ Waiting for Streamlit app to start...")
        time.sleep(15)
        
        # Test if app is accessible
        try:
            response = requests.get("http://localhost:8501", timeout=5)
            if response.status_code == 200:
                print("✅ Streamlit app is running!")
                return process
            else:
                print(f"❌ Streamlit app check failed: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to Streamlit app: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting Streamlit app: {e}")
        return None

def test_docker_local():
    """Test using Docker locally"""
    print("🐳 Testing with Docker...")
    
    try:
        # Build Docker image
        print("🔨 Building Docker image...")
        build_result = subprocess.run([
            "docker", "build", "-t", "health-intelligence-hub:local", "."
        ], capture_output=True, text=True)
        
        if build_result.returncode != 0:
            print(f"❌ Docker build failed: {build_result.stderr}")
            return None
        
        print("✅ Docker image built successfully!")
        
        # Run Docker container
        print("🚀 Starting Docker container...")
        run_result = subprocess.run([
            "docker", "run", "-d",
            "--name", "health-hub-test",
            "-p", "8080:8080",
            "--env-file", ".env",
            "health-intelligence-hub:local"
        ], capture_output=True, text=True)
        
        if run_result.returncode != 0:
            print(f"❌ Docker run failed: {run_result.stderr}")
            return None
        
        print("✅ Docker container started!")
        print("⏳ Waiting for container to initialize...")
        time.sleep(20)
        
        # Test health endpoint
        try:
            response = requests.get("http://localhost:8080/health", timeout=10)
            if response.status_code == 200:
                print("✅ Docker container is running!")
                print(f"📊 Health check response: {response.json()}")
                return "docker"
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to Docker container: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Error with Docker testing: {e}")
        return None

def test_docker_compose():
    """Test using Docker Compose"""
    print("🐳 Testing with Docker Compose...")
    
    try:
        # Start services with docker-compose
        print("🚀 Starting services with docker-compose...")
        compose_result = subprocess.run([
            "docker-compose", "up", "-d"
        ], capture_output=True, text=True)
        
        if compose_result.returncode != 0:
            print(f"❌ Docker Compose failed: {compose_result.stderr}")
            return None
        
        print("✅ Docker Compose services started!")
        print("⏳ Waiting for services to initialize...")
        time.sleep(30)
        
        # Test health endpoint
        try:
            response = requests.get("http://localhost:8501", timeout=10)
            if response.status_code == 200:
                print("✅ Docker Compose services are running!")
                return "docker-compose"
            else:
                print(f"❌ Service check failed: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to services: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Error with Docker Compose testing: {e}")
        return None

def cleanup_process(process):
    """Clean up a subprocess"""
    if process:
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()

def cleanup_docker():
    """Clean up Docker resources"""
    try:
        subprocess.run(["docker", "stop", "health-hub-test"], capture_output=True)
        subprocess.run(["docker", "rm", "health-hub-test"], capture_output=True)
        print("🧹 Docker container cleaned up")
    except:
        pass

def cleanup_docker_compose():
    """Clean up Docker Compose resources"""
    try:
        subprocess.run(["docker-compose", "down"], capture_output=True)
        print("🧹 Docker Compose services cleaned up")
    except:
        pass

def main():
    """Main testing function"""
    print("🏥 Health Intelligence Hub - Local Testing")
    print("=" * 50)
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("Please create a .env file with your environment variables:")
        print("GOOGLE_API_KEY=your-api-key")
        print("GOOGLE_CLOUD_PROJECT=your-project-id")
        print("GOOGLE_CLOUD_LOCATION=us-central1")
        return
    
    print("Available testing options:")
    print("1. FastAPI server only")
    print("2. Streamlit app only")
    print("3. Both FastAPI and Streamlit")
    print("4. Docker container")
    print("5. Docker Compose")
    print("6. All tests")
    
    choice = input("\nSelect testing option (1-6): ").strip()
    
    processes = []
    
    try:
        if choice in ["1", "3", "6"]:
            fastapi_process = test_fastapi_server()
            if fastapi_process:
                processes.append(fastapi_process)
                print("🌐 FastAPI server: http://localhost:8080")
                print("📚 API docs: http://localhost:8080/docs")
        
        if choice in ["2", "3", "6"]:
            streamlit_process = test_streamlit_app()
            if streamlit_process:
                processes.append(streamlit_process)
                print("🌐 Streamlit app: http://localhost:8501")
        
        if choice in ["4", "6"]:
            docker_result = test_docker_local()
            if docker_result:
                print("🌐 Docker container: http://localhost:8080")
        
        if choice in ["5", "6"]:
            compose_result = test_docker_compose()
            if compose_result:
                print("🌐 Docker Compose: http://localhost:8501")
        
        if choice == "6":
            print("\n🎉 All tests completed!")
            print("=" * 50)
            print("🌐 Access URLs:")
            print("  - FastAPI server: http://localhost:8080")
            print("  - Streamlit app: http://localhost:8501")
            print("  - API docs: http://localhost:8080/docs")
            print("  - Health check: http://localhost:8080/health")
        
        # Keep services running
        if processes or choice in ["4", "5"]:
            print("\n✅ Services are running! Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping services...")
    
    finally:
        # Cleanup
        for process in processes:
            cleanup_process(process)
        
        if choice in ["4", "6"]:
            cleanup_docker()
        
        if choice in ["5", "6"]:
            cleanup_docker_compose()
        
        print("🧹 Cleanup completed")

if __name__ == "__main__":
    main()
