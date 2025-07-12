import os 
import json
import mlflow
import pandas as pd
from loguru import logger


def find_run_path(run_id, mlruns_path="mlruns"):
    for experiment_id in os.listdir(mlruns_path):
        exp_path = os.path.join(mlruns_path, experiment_id)
        if not os.path.isdir(exp_path):
            continue
        run_dir = os.path.join(exp_path, run_id)
        if os.path.exists(run_dir):
            return os.path.join(run_dir, "artifacts", "model")
    raise FileNotFoundError(f"Run ID {run_id} not found in mlruns folder")

def load_best_model_local():
    with open("src/artifacts/best_model.json") as f:
        metadata = json.load(f)

    run_id = metadata["run_id"]
    model_local_path = find_run_path(run_id)
    logger.info(f"Loading model from: {model_local_path}")

    model = mlflow.pyfunc.load_model(model_local_path)
    logger.info("Model loaded successfully!")
    return model


def load_best_model():
    # Set tracking URI based on environment
    if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        # In Lambda, disable MLflow tracking entirely
        mlflow.set_tracking_uri("")
        # Disable MLflow tracing to avoid filesystem issues
        os.environ["MLFLOW_TRACKING_DISABLE"] = "true"
    else:
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
    
    # mlflow.set_tracking_uri("http://mlflow:5000")

    # Load the best model metadata from the saved file
    with open("src/artifacts/best_model.json") as f:
        metadata = json.load(f)
    logger.info(f"metadata: {metadata}")
    
    # Load the model from MLflow using the run ID and model name
    model_uri = f"runs:/{metadata['run_id']}/model"
    logger.info(f"model_uri: {model_uri}")

    model = mlflow.pyfunc.load_model(model_uri)
    logger.info("Model loaded successfully!")
    return model

class ModelPredictor:
    """
    Class to handle feature engineering, model loading, and prediction.
    """

    def __init__(self, feature_engineer):
        
        print(os.listdir())
        logger.info(f"os.listdir(): {os.listdir()}")
        # Load the model directly within the class from the load_best_model function
        try:
            if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
                # In Lambda, use local path approach
                self.model = load_best_model_local()
            else:
                # Locally, use MLflow tracking approach
                self.model = load_best_model()
        except Exception as e:
            logger.error(f"Error in ModelPredictor: {str(e)}")
            # Fallback to local approach
            self.model = load_best_model_local()
        self.feature_engineer = feature_engineer

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data using the FeatureEngineer object.
        """
        return self.feature_engineer.inference(data)

    def predict(self, data: pd.DataFrame) -> list:
        """
        Preprocess the input data, make predictions using the model, and return the results.
        """
        # Preprocess the input data
        processed_data = self.preprocess_data(data)
        
        # Make predictions using the model
        predictions = self.model.predict(processed_data)
        
        return list(predictions)