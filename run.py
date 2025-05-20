#!/usr/bin/env python
"""
Run script for the Protein Information Explorer.
"""
import argparse
import os
import sys

from loguru import logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Protein Information Explorer")
    parser.add_argument(
        "--port", type=int, default=8050, help="Port to run the application on"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Run the application in debug mode"
    )
    parser.add_argument(
        "--log-level", type=str, default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    
    args = parser.parse_args()
    
    # Set environment variables
    os.environ["PORT"] = str(args.port)
    os.environ["DEBUG"] = str(args.debug).lower()
    os.environ["LOG_LEVEL"] = args.log_level.upper()
    
    logger.info(f"Starting application with: port={args.port}, debug={args.debug}, log_level={args.log_level}")
    
    try:
        # Import and run the application
        from src.app import app
        
        app.run_server(
            debug=args.debug,
            port=args.port,
            host="0.0.0.0",
        )
    except ImportError as e:
        logger.error(f"Error importing application: {e}")
        logger.error("Make sure you have installed all dependencies with: poetry install")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running application: {e}")
        sys.exit(1) 