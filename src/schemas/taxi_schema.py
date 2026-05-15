from typing import Optional

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    PULocationID: str
    DOLocationID: str
    trip_distance: Optional[float] = Field(default=None, gt=0, le=100)


class DistanceInput(BaseModel):
    PULocationID: str
    DOLocationID: str
