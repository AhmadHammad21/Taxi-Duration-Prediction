import json
import mlflow
import pandas as pd

def load_best_model():
    mlflow.set_tracking_uri("sqlite:///mlflow.db")

    # Load the best model metadata from the saved file
    with open("src/artifacts/best_model.json") as f:
        metadata = json.load(f)
    print(f"metadata: {metadata}")
    
    # Load the model from MLflow using the run ID and model name
    model_uri = f"runs:/{metadata['run_id']}/model"
    print(f"model_uri: {model_uri}")
    model = mlflow.pyfunc.load_model(model_uri)
    
    return model

class ModelPredictor:
    """
    Class to handle feature engineering, model loading, and prediction.
    """

    def __init__(self, feature_engineer):
        # Load the model directly within the class from the load_best_model function
        self.model = load_best_model()  # This dynamically loads the model
        self.feature_engineer = feature_engineer

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data using the FeatureEngineer object.
        """
        return self.feature_engineer.inference(data)

    def predict(self, data: pd.DataFrame):
        """
        Preprocess the input data, make predictions using the model, and return the results.
        """
        # Preprocess the input data
        processed_data = self.preprocess_data(data)
        
        # Make predictions using the model
        predictions = self.model.predict(processed_data)
        
        return predictions