from loguru import logger
import sys
try:
    from config.settings import settings
except ImportError:
    from src.config.settings import settings


def setup_logging():
    logger.remove()  # Remove default logger
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )
    logger.add(
        settings.LOG_FILE,
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",  # Rotate log file when it reaches 10 MB
        retention="7 days",  # Keep logs for 7 days
        enqueue=True,  # Make logging thread-safe
        backtrace=True,  # Show full stack trace on exceptions
        diagnose=True,  # Add exception variable values
    )


def get_logger():
    return logger 