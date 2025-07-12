import os
from loguru import logger
import sys
try:
    from config.settings import settings
except ImportError:
    from src.config.settings import settings


def setup_logging():
    logger.remove()  # Remove default logger

    # Always log to stderr (console)
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )

    # Only add file logging if NOT running in Lambda
    if not os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        logger.add(
            "logs/app.log",
            level=settings.LOG_LEVEL,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="10 MB",
            retention="7 days",
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )


def get_logger():
    return logger 