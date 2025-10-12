#!/usr/bin/env python3
"""
Start the WebSocket server for conversational AI
This runs alongside the main FastAPI server
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from conversational_ai import start_websocket_server

if __name__ == "__main__":
    print("🚀 Starting Conversational AI WebSocket Server on port 8080...")
    print("📞 Ready to handle real-time conversations with Marcus!")
    asyncio.run(start_websocket_server(host="0.0.0.0", port=8080))
