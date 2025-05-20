"""
Logging configuration for the application.
"""
import os
import sys
from pathlib import Path

from loguru import logger

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure loguru logger
config = {
    "handlers": [
        {
            "sink": sys.stderr,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            "level": "INFO",
        },
        {
            "sink": log_dir / "app.log",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            "level": "DEBUG",
            "rotation": "10 MB",
            "retention": "1 week",
        },
    ],
}

# Remove default logger
logger.remove()

# Add configured handlers
for handler in config["handlers"]:
    logger.add(**handler)

# Set log level from environment variable if provided
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logger.level(log_level)

# Export logger to be imported by other modules
__all__ = ["logger"] 