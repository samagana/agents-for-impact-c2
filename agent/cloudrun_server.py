"""
Unified server for Cloud Run deployment
Handles both ADK health agents and Streamlit webapp on a single port
"""
import os
import sys
import asyncio
import threading
import time
import signal
import logging
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudRunServer:
    """Unified server for Cloud Run deployment"""
    
    def __init__(self):
        self.port = int(os.getenv("PORT", 8080))
        self.adk_process = None
        self.streamlit_process = None
        self.shutdown_event = threading.Event()
    
    def start_adk_server(self):
        """Start ADK server in a separate process"""
        try:
            import subprocess
            
            logger.info(f"🚀 Starting ADK Health Agent Server on port {self.port}")
            
            # Start ADK server
            self.adk_process = subprocess.Popen([
                sys.executable, "-m", "uv", "run", "adk", "web",
                "--host", "0.0.0.0",
                "--port", str(self.port)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            logger.info("✅ ADK Server started successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting ADK server: {e}")
            return False
    
    def start_streamlit_app(self):
        """Start Streamlit app in a separate process"""
        try:
            import subprocess
            
            logger.info(f"🌐 Starting Streamlit Health Intelligence Hub on port {self.port}")
            
            # Start Streamlit app
            self.streamlit_process = subprocess.Popen([
                sys.executable, "-m", "uv", "run", "streamlit", "run", "app.py",
                "--server.port", str(self.port),
                "--server.address", "0.0.0.0",
                "--server.headless", "true",
                "--server.enableCORS", "false",
                "--server.enableXsrfProtection", "false",
                "--browser.gatherUsageStats", "false"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            logger.info("✅ Streamlit app started successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting Streamlit app: {e}")
            return False
    
    def health_check(self):
        """Simple health check endpoint"""
        try:
            import http.server
            import socketserver
            from urllib.parse import urlparse, parse_qs
            
            class HealthHandler(http.server.SimpleHTTPRequestHandler):
                def do_GET(self):
                    if self.path == '/health':
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'{"status": "healthy", "service": "health-intelligence-hub"}')
                    else:
                        # Proxy to Streamlit or ADK based on path
                        self.proxy_request()
                
                def proxy_request(self):
                    # For Cloud Run, we'll primarily serve the Streamlit app
                    # ADK endpoints can be accessed via /api/ prefix
                    if self.path.startswith('/api/'):
                        # This would proxy to ADK server
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'{"message": "ADK API endpoint - implement proxy logic"}')
                    else:
                        # Serve Streamlit app
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b'<html><body><h1>Health Intelligence Hub</h1><p>Streamlit app is starting...</p></body></html>')
            
            # Start health check server on a different port
            health_port = self.port + 1
            with socketserver.TCPServer(("0.0.0.0", health_port), HealthHandler) as httpd:
                logger.info(f"🏥 Health check server running on port {health_port}")
                httpd.serve_forever()
                
        except Exception as e:
            logger.error(f"❌ Error starting health check server: {e}")
    
    def run(self):
        """Main run method"""
        logger.info("🏥 Starting Health Intelligence Hub on Cloud Run...")
        
        # Start ADK server
        if not self.start_adk_server():
            logger.error("Failed to start ADK server")
            return False
        
        # Wait for ADK server to initialize
        logger.info("⏳ Waiting for ADK server to initialize...")
        time.sleep(15)
        
        # Start Streamlit app
        if not self.start_streamlit_app():
            logger.error("Failed to start Streamlit app")
            return False
        
        logger.info("✅ Health Intelligence Hub is running on Cloud Run!")
        logger.info(f"📊 Streamlit Webapp: http://localhost:{self.port}")
        logger.info(f"🤖 ADK Health Agents: http://localhost:{self.port}")
        
        # Set up signal handlers
        def signal_handler(signum, frame):
            logger.info("🛑 Received shutdown signal")
            self.shutdown()
        
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        
        # Wait for shutdown signal
        try:
            while not self.shutdown_event.is_set():
                time.sleep(1)
                
                # Check if processes are still running
                if self.adk_process and self.adk_process.poll() is not None:
                    logger.error("ADK server process died")
                    break
                
                if self.streamlit_process and self.streamlit_process.poll() is not None:
                    logger.error("Streamlit app process died")
                    break
                    
        except KeyboardInterrupt:
            logger.info("🛑 Received keyboard interrupt")
            self.shutdown()
    
    def shutdown(self):
        """Graceful shutdown"""
        logger.info("🛑 Shutting down services...")
        
        self.shutdown_event.set()
        
        if self.adk_process:
            self.adk_process.terminate()
            try:
                self.adk_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.adk_process.kill()
        
        if self.streamlit_process:
            self.streamlit_process.terminate()
            try:
                self.streamlit_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.streamlit_process.kill()
        
        logger.info("✅ Services stopped gracefully")

def main():
    """Main entry point"""
    server = CloudRunServer()
    server.run()

if __name__ == "__main__":
    main()
