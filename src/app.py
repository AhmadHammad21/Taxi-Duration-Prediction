from fastapi import FastAPI
from .routes import base, taxi
from contextlib import asynccontextmanager
# from config.config import config
# from config.settings import settings
from .features.feature_pipeline import FeatureEngineer
from .inference.predict import ModelPredictor
from .utils.logging_config import setup_logging


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