from pydantic import BaseModel

class PredictionInput(BaseModel):
    PULocationID: str
    DOLocationID: str

class DistanceInput(BaseModel):
    PULocationID: str
    DOLocationID: str
