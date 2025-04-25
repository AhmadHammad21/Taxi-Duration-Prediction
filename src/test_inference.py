import mlflow
import pandas as pd
from features.feature_pipeline import FeatureEngineer
from inference.predict import ModelPredictor

if __name__ == "__main__":
    # Initialize the FeatureEngineer object
    feature_engineer = FeatureEngineer()

    # Initialize the ModelPredictor with the FeatureEngineer instance
    model_predictor = ModelPredictor(feature_engineer=feature_engineer)

    # Prepare input data
    new_data = {
        "PULocationID": [186, 298],
        "DOLocationID": [79, 50],
        "trip_distance": [4, 10]
    }
    new_data_df = pd.DataFrame(new_data)

    # Predict using the model
    predictions = model_predictor.predict(new_data_df)
    
    # Output predictions
    print("Predictions:", predictions)