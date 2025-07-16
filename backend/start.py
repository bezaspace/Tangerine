#!/usr/bin/env python3
"""
Startup script for the Tangerine Practitioners API
"""
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🍊 Starting Tangerine Practitioners API on {host}:{port}")
    print(f"📱 Make sure to update your React Native app's API URL to: http://YOUR_IP_ADDRESS:{port}")
    print(f"🔧 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )