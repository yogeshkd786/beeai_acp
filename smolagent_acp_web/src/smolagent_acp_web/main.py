#!/usr/bin/env python3
"""
ACP-compliant Health Agent Server
Main entry point for the hospital health agent system.
"""

import logging
import os
import sys
from .health_agent_server import create_health_agent_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main function to start the ACP health agent server."""
    try:
        # Create and configure the health agent server
        server = create_health_agent_server()
        
        # Server configuration
        port = 8000
        
        logger.info(f"Starting ACP Health Agent Server on port {port}")
        logger.info("Server supports health-focused question answering for hospital patients")
        logger.info("Available tools: DuckDuckGo Search, Web Page Content Extraction")
        
        # Start the server (this is synchronous)
        server.run(host="0.0.0.0", port=port)
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application failed: {e}")
        sys.exit(1)
