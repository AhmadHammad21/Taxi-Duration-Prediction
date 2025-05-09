from fastapi import FastAPI
from .routes import base, taxi
# from config.config import config
# from config.settings import settings
from .features.feature_pipeline import FeatureEngineer
from .inference.predict import ModelPredictor


async def lifespan(app: FastAPI):
    
    app.feature_engineer = FeatureEngineer()

    app.model_predictor = ModelPredictor(
        feature_engineer=app.feature_engineer
    )
    yield  # This is where FastAPI runs the application


app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(taxi.taxi_router)