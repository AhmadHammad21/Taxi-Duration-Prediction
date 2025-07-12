from fastapi import FastAPI
from .routes import base, taxi
from contextlib import asynccontextmanager
# from config.config import config
# from config.settings import settings
from .features.feature_pipeline import FeatureEngineer
from .inference.predict import ModelPredictor
from .utils.logging_config import setup_logging
from mangum import Mangum
import os
import sys


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    app.state.feature_engineer = FeatureEngineer()
    app.state.model_predictor = ModelPredictor(
        feature_engineer=app.state.feature_engineer
    )
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(taxi.taxi_router)

handler = Mangum(app)  # This is the AWS Lambda handler


def setup_logging():
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )

    if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        LOG_FILE = "/tmp/logs/app.log"
        use_enqueue = False  # <--- Disable enqueue in Lambda!
    else:
        LOG_FILE = "logs/app.log"
        use_enqueue = True

    logger.add(
        LOG_FILE,
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="7 days",
        enqueue=use_enqueue,  # <--- Use variable
        backtrace=True,
        diagnose=True,
    )