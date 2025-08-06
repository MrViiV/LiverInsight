#!/usr/bin/env python3
"""
Startup script for the ML service
"""

import subprocess
import sys
import os

def start_ml_service():
    """Start the ML service using uvicorn"""
    try:
        # Change to project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Start the ML service
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "ml_service.model_server:app", 
            "--host", "0.0.0.0", 
            "--port", "8001", 
            "--reload"
        ]
        
        print("Starting ML service on port 8001...")
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\nML service stopped.")
    except Exception as e:
        print(f"Error starting ML service: {e}")

if __name__ == "__main__":
    start_ml_service()