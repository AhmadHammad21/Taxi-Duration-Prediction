import random
import pandas as pd
from fastapi import APIRouter, Request, status, Request
from fastapi.responses import JSONResponse
from ..schemas.taxi_schema import DistanceInput, PredictionInput
from loguru import logger


taxi_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)


def calculate_fake_distance(pu_id: str, do_id: str) -> float:
    """Simulates a fictional distance between pickup and dropoff locations."""
    seed = hash(f"{pu_id}-{do_id}") % 1000
    random.seed(seed)
    return round(random.uniform(1.0, 30.0), 2)


@taxi_router.post("/predict")
async def predict(request: Request, input_data: PredictionInput):
    """Make a prediction with the ML model."""

    pu_location_id = input_data.PULocationID
    du_location_id = input_data.DOLocationID

    # This should be later calculated through an API
    trip_distance = calculate_fake_distance(pu_location_id, du_location_id) 

    try:
        new_data = {
            "PULocationID": [pu_location_id],
            "DOLocationID": [du_location_id],
            "trip_distance": [trip_distance]
        }
        new_data_df = pd.DataFrame(new_data)

        # Predict using the model
        duration_prediction = request.app.state.model_predictor.predict(new_data_df)
        duration_prediction = float(duration_prediction[0])
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "duration": duration_prediction,
            }
        )

    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "No answer could be generated"
            }
        )


@taxi_router.post("/measure_distance")
async def measure_distance(input_data: DistanceInput):
    """Measure fictional distance between locations."""
    try:
        distance = calculate_fake_distance(input_data.PULocationID, input_data.DOLocationID)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"distance": distance}
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "No answer could be generated"}
        )

