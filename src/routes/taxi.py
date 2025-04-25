import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist
import yaml


# Load configuration
with open("../../config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load the model
model_path = Path(config["model"]["model_path"])
if not model_path.exists():
    raise FileNotFoundError(f"Model file not found: {model_path}")

with open(model_path, "rb") as f:
    model = pickle.load(f)

# Create FastAPI app
app = FastAPI(
    title="ML Model API",
    description="API for ML model predictions",
    version="0.1.0",
)


# Define request data model
class PredictionInput(BaseModel):
    features: conlist(float, min_items=1)


# Define response data model
class PredictionOutput(BaseModel):
    prediction: int
    probability: float


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Welcome to the ML Model API"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    """Make a prediction with the ML model."""
    try:
        # Convert input data to numpy array
        features = np.array(input_data.features).reshape(1, -1)
        
        # Make prediction
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][prediction])
        
        return {
            "prediction": prediction,
            "probability": probability
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)